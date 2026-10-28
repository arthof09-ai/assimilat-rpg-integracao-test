"""Additive FULL-STATE Notion-adapter planner and causal recovery validator.
NEVER connects to Notion, modifies RPG or replaces V05/R17/R30. Local TEST-only proof.
"""
import copy,hashlib,json
from dataclasses import dataclass

class Hold(ValueError):pass
LAB_ID='3fbc2b324ede804a95fafcb7b293c92c'

def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()

def fixture_doc(before,descendants=24):
 return {'scope':'TEST','ancestor_lab':LAB_ID,'actor_id':before['NORMAL']['id'],'active':copy.deepcopy(before),
         'history':[],'child_count':descendants,'external_writes':0,'event_log':[],'version':0,
         'equipment_identity':copy.deepcopy(before['NORMAL'].get('attribute_layers',{}))}

def preview(doc,after,event_id,choice_kind='SYNTHETIC_EXPLICIT'):
 if doc['scope']!='TEST' or doc['ancestor_lab']!=LAB_ID or not doc['actor_id'].startswith('SYNTH-'):
  raise Hold('OUTSIDE_TEST_OR_NOT_SYNTHETIC')
 if choice_kind!='SYNTHETIC_EXPLICIT':raise Hold('MISSING_COMPETENT_CHOICE')
 if doc['child_count']<24:raise Hold('NATIVE_CHILD_ABSENT')
 if doc['external_writes']:raise Hold('EXTERNAL_REF_WRITE')
 if doc['active']['NORMAL']['id']!=doc['actor_id'] or after['NORMAL']['id']!=doc['actor_id']:
  raise Hold('IDENTITY_MISMATCH')
 if set(doc['active'])!={'NORMAL','TRANSFORM','LOCKS'} or set(after)!={'NORMAL','TRANSFORM','LOCKS'}:
  raise Hold('THREE_DOC_CONTRACT_MISSING')
 if doc['equipment_identity']!=doc['active']['NORMAL'].get('attribute_layers',{}):
  raise Hold('EQUIPMENT_DRIFT')
 return {'event':event_id,'expected_before':sha(doc['active']),'expected_after':sha(after),
         'previous_version':doc['version'],'expected_children':doc['child_count'],
         'equipment_identity':copy.deepcopy(doc['equipment_identity']),
         'after':copy.deepcopy(after),'authorization':'SYNTHETIC_EXPLICIT'}

def commit(doc,plan,*,fault=None):
 d=copy.deepcopy(doc)
 if any(x['event']==plan['event'] and x['status']=='COMMITTED' for x in d['event_log']):
  if sha(d['active'])==plan['expected_after']:return d,'IDEMPOTENT_NOOP'
  raise Hold('DUPLICATE_EVENT_BUT_STATE_DRIFT')
 if sha(d['active'])!=plan['expected_before'] or d['version']!=plan['previous_version']:
  raise Hold('STALE_PREIMAGE')
 if d['child_count']!=plan['expected_children']:raise Hold('NATIVE_CHILD_DRIFT')
 if d['equipment_identity']!=plan['equipment_identity']:raise Hold('EQUIPMENT_DRIFT')
 if d['external_writes'] or d['scope']!='TEST' or d['ancestor_lab']!=LAB_ID:raise Hold('OUT_OF_BOUND')
 if not plan.get('authorization')=='SYNTHETIC_EXPLICIT':raise Hold('UNKNOWN_DECISION')
 # A durable pre-commit intent lives independently from writes and permits safe retry.
 intent={'event':plan['event'],'status':'PREPARED','before_sha':plan['expected_before'],'after_sha':plan['expected_after']}
 d['event_log'].append(intent)
 if fault=='after_archive':raise Hold('INJECTED_CRASH_AFTER_ARCHIVE_HOLD_BEFORE_EFFECT')
 if fault=='after_some_derivatives':raise Hold('INJECTED_CRASH_BEFORE_SINGLE_ATOMIC_COMMIT')
 if fault=='transform_interrupt':raise Hold('INJECTED_TRANSFORM_CRASH_BEFORE_COMMIT')
 d['history'].append({'event':plan['event'],'version':d['version'],'state':copy.deepcopy(d['active'])})
 d['active']=copy.deepcopy(plan['after']);d['version']+=1
 intent['status']='COMMITTED'
 if sha(d['active'])!=plan['expected_after'] or sha(d['history'][-1]['state'])!=plan['expected_before']:
  raise Hold('POST_COMMIT_READBACK_MISMATCH')
 return d,'COMMITTED'

def recover(preimage,current,plan):
 if sha(current['active'])==plan['expected_before'] and current['version']==plan['previous_version']:
  return 'CLEAN_PREIMAGE_SAFE_TO_RETRY'
 if sha(current['active'])==plan['expected_after'] and any(r['event']==plan['event'] and r['status']=='COMMITTED' for r in current['event_log']):
  return 'COMMITTED_NEVER_REAPPLY'
 return 'UNKNOWN_EFFECT_HOLD_READBACK'
