"""IBX-17 additive causal recovery gate. No network, no writer credentials.
R117 adds repair *decisions*, never treats physical AFTER as causal proof.
Old R107 implementations are retained byte-for-byte in baseline/runtime.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import hashlib, json
ORDER=('NORMAL','TRANSFORM','LOCKS')
class Hold(ValueError):pass

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()

@dataclass(frozen=True)
class RecoveryDecision:
 classification: str
 allowed_write_set: tuple
 target_version: str
 reason: str
 status: str='HOLD'
 def as_dict(self):return self.__dict__ | {'allowed_write_set':list(self.allowed_write_set)}

def classify(*,receipt,physical,journals,final_marker,identity,proof,live_version):
 """Side-effect-free classifier. Requires immutable source identity, lab parent,
 exact actor, source/version, bounded write-set, and a *fresh Notion version*.
 proof keys: per-stage causal receipts, observed event, authorized identity.
 AFTER w/ PREPARED journal requires independent cause proof; no naked relabel.
 """
 required=['event_id','target_id','parent_id','source_version','pre_version','receipt_hash','authority','actor_id']
 if any(not identity.get(k) for k in required):return RecoveryDecision('IDENTITY_MISSING',(),live_version,'Required identity incomplete')
 if identity['authority']!='LAB_TEST_EXPLICIT_FROM_MESTRE' or identity['parent_id']!='3fbc2b324ede804a95fafcb7b293c92c':return RecoveryDecision('AUTHORITY_HOLD',(),live_version,'TEST parent/authority invalid')
 if not live_version or not proof.get('last_read_version') or proof['last_read_version']!=live_version:return RecoveryDecision('STALE_VERSION',(),live_version,'Readback version changed after decision')
 if identity.get('receipt_hash')!=sha(receipt) or set(physical)!=set(ORDER) or set(journals)!=set(ORDER):return RecoveryDecision('RECEIPT_OR_STATE_INCOMPLETE',(),live_version,'Receipt identity/stages not integral')
 if proof.get('target_id')!=identity['target_id'] or proof.get('event_id')!=identity['event_id'] or proof.get('parent_id')!=identity['parent_id']:
  return RecoveryDecision('CAUSAL_IDENTITY_COLLISION',(),live_version,'Proof event/target/parent mismatch')
 if proof.get('source_version')!=identity['source_version'] or proof.get('pre_version')!=identity['pre_version']:
  return RecoveryDecision('CAUSAL_SOURCE_COLLISION',(),live_version,'Proof source/PRE mismatch')
 if proof.get('event_collision') or proof.get('concurrent_edit'):return RecoveryDecision('CONCURRENT_EVENT',(),live_version,'Concurrent mutation or duplicate event')
 s={};j={}
 for k in ORDER:
  h=sha(physical[k]); bh=sha(receipt['before'][k]); ah=sha(receipt['after'][k]);
  if h==bh and h==ah:s[k]='AMBIGUOUS_NOOP'
  elif h==ah:s[k]='AFTER'
  elif h==bh:s[k]='BEFORE'
  else:return RecoveryDecision('UNKNOWN_EFFECT',(),live_version,k+' neither PRE nor AFTER')
  j[k]=journals[k]
  if j[k] not in ('PREPARED','COMMITTED'):return RecoveryDecision('INVALID_JOURNAL',(),live_version,k)
 for k in ORDER:
  if s[k]=='BEFORE' and j[k]=='COMMITTED':return RecoveryDecision('JOURNAL_AHEAD_PHYSICAL',(),live_version,k+' committed but BEFORE')
 if final_marker=='COMMITTED' and any(s[k]=='BEFORE' or j[k]!='COMMITTED' for k in ORDER):return RecoveryDecision('FALSE_TERMINAL_MARKER',(),live_version,'Terminal marker contradicts stages')
 # A committed journal for an equal-state no-op must come with a causal stage receipt.
 for k in ORDER:
  if s[k]=='AMBIGUOUS_NOOP' and j[k]=='COMMITTED' and not proof.get('stage_receipts',{}).get(k):return RecoveryDecision('NOOP_CAUSE_MISSING',(),live_version,k)
 # a journal gap after a native write: require receipts *proving* same event & stage
 gaps=[k for k in ORDER if s[k]=='AFTER' and j[k]=='PREPARED']
 if gaps:
  if len(gaps)>1:return RecoveryDecision('MULTI_JOURNAL_GAP',(),live_version,','.join(gaps))
  k=gaps[0];c=proof.get('stage_receipts',{}).get(k)
  if not c or c.get('event_id')!=identity['event_id'] or c.get('target_id')!=identity['target_id'] or c.get('stage')!=k or c.get('after_hash')!=sha(physical[k]) or not c.get('native_write_receipt_id') or not c.get('before_version') or not c.get('after_version'):
   return RecoveryDecision('AFTER_WITHOUT_CAUSAL_JOURNAL',(),live_version,k+' physical AFTER, durable writer receipt absent')
  if proof.get('proof_review')!='INDEPENDENTLY_VERIFIED':return RecoveryDecision('CAUSE_REVIEW_PENDING',(),live_version,k+' receipt exists but independent verification missing')
  return RecoveryDecision('JOURNAL_REPAIR_CANDIDATE',(f'JOURNAL_{k}',),live_version,'Causal write receipt verified; repair only journal',status='RECOVERY_AUTH_REQUIRED')
 after=[k for k in ORDER if s[k]=='AFTER' or s[k]=='AMBIGUOUS_NOOP' and j[k]=='COMMITTED']
 if after!=list(ORDER[:len(after)]):return RecoveryDecision('NON_PREFIX',(),live_version,'Out of order after state')
 if any(j[k]!='COMMITTED' for k in after):return RecoveryDecision('JOURNAL_GAP',(),live_version,'No evidence of commit')
 if final_marker=='COMMITTED' and len(after)==3:return RecoveryDecision('COMMITTED_NOOP',(),live_version,'No further write authorized',status='PASS')
 if len(after)==3:
  if final_marker not in ('PREPARED','PENDING','IN_PROGRESS'):return RecoveryDecision('UNKNOWN_TERMINAL',(),live_version,'Unrecognized final marker')
  if not proof.get('all_stage_readbacks') or proof.get('proof_review')!='INDEPENDENTLY_VERIFIED':return RecoveryDecision('TERMINAL_REVIEW_PENDING',(),live_version,'All journals committed but cause/reopen review incomplete')
  return RecoveryDecision('MARKER_ONLY_REPAIR_CANDIDATE',('FINAL_MARKER',),live_version,'3/3 AFTER and durable journals; no group writes',status='RECOVERY_AUTH_REQUIRED')
 if any(j[k]!='PREPARED' for k in ORDER[len(after):]):return RecoveryDecision('NON_PREFIX_JOURNAL',(),live_version,'Invalid following stages')
 if final_marker not in ('PREPARED','IN_PROGRESS'):return RecoveryDecision('FINAL_MARKER_INVALID',(),live_version,'Invalid partial marker')
 return RecoveryDecision('PARTIAL_NEXT_STAGE_CANDIDATE',(ORDER[len(after)],),live_version,'Only next stage may be written after authorization',status='RECOVERY_AUTH_REQUIRED')

def authorize_recovery(decision,*,new_live_version,authority,operator,plan_id):
 if decision.status!='RECOVERY_AUTH_REQUIRED' or not decision.allowed_write_set:raise Hold('NOT_RECOVERABLE_BY_GATE')
 if new_live_version!=decision.target_version:raise Hold('STALE_AFTER_CLASSIFICATION')
 if authority!='LAB_TEST_EXPLICIT_FROM_MESTRE' or not operator or not plan_id:raise Hold('NO_RECOVERY_AUTHORITY')
 return {'authorized':True,'target_version':new_live_version,'minimal_writeset':list(decision.allowed_write_set),'plan_id':plan_id,'operator':operator,'no_group_replay':decision.classification in ('MARKER_ONLY_REPAIR_CANDIDATE','JOURNAL_REPAIR_CANDIDATE')}
