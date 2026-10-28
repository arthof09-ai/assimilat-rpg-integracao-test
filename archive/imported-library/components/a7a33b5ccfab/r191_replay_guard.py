"""R191 guard for connected Notion page readback; no Notion write and no host impersonation.
Operates on page content returned by official Notion fetch. Rejects stale, wrong-scope,
consumed, unknown effect, and previously prepared contradictory transactions.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
LAB='3fbc2b324ede804a95fafcb7b293c92c'
class NativeHold(ValueError): pass

@dataclass(frozen=True)
class NativeObservation:
 page_id:str
 parent_id:str
 version:str
 text:str

def active_fields(body):
 head='## IBX17-R190 — DADOS ATIVOS / TEST';tail='## PROVENIÊNCIA E ESCOPO'
 if body.count(head)!=1 or body.count(tail)!=1 or body.find(head)>body.find(tail):raise NativeHold('ACTIVE_SCOPE_AMBIGUOUS')
 active=body.split(head,1)[1].split(tail,1)[0]
 fields={}
 for line in active.splitlines():
  hit=re.fullmatch(r'([A-Z_]+): ([^\n]+)',line)
  if hit:
   k,v=hit.groups()
   if k in fields:raise NativeHold('DUPLICATE_FIELD_'+k)
   fields[k]=v
 return fields

def classify(observation,*,tx,expected_target,expected_pre_version,allow_test_only=True):
 if observation.page_id!=expected_target or observation.parent_id!=LAB:raise NativeHold('TARGET_ANCESTRY_UNPROVED')
 if not allow_test_only:raise NativeHold('PRODUCTION_DENIED')
 fields=active_fields(observation.text)
 if not observation.text.strip().endswith('</details>') or 'HISTÓRICO INTEGRAL R190' not in observation.text:raise NativeHold('HISTORY_MISSING')
 if fields.get('SPIRIT_ACTIVE')!='FALSE':raise NativeHold('SPIRIT_EFFECT_UNKNOWN')
 if fields.get('TX_ID')==tx and fields.get('TX_STATE')=='COMMITTED_AFTER_NATIVE_READBACK' and fields.get('TX_JOURNAL','').startswith('COMMITTED_AFTER_NATIVE_READBACK; tx='+tx+';'):
  return {'decision':'NOOP_ALREADY_CONSUMED_NATIVE','native_writes':0,'replay_allowed':False,'version':observation.version}
 if fields.get('TX_ID')==tx and fields.get('TX_STATE')!='PRE':
  return {'decision':'HOLD_PARTIAL_OR_UNKNOWN_SAME_EVENT','native_writes':0,'replay_allowed':False}
 if observation.version!=expected_pre_version:return {'decision':'HOLD_STALE_PREVIEW_VERSION','native_writes':0,'replay_allowed':False}
 if fields.get('TX_ID')!='NONE' or fields.get('TX_STATE')!='PRE':raise NativeHold('CONFLICTING_FRESH_TRANSACTION')
 return {'decision':'FRESH_TEST_PREVIEW_CANDIDATE','native_writes':0,'replay_allowed':False,'note':'No automatic writer; separate verified authorization required'}

def cancel(observation,*,tx):
 fields=active_fields(observation.text)
 return {'decision':'CANCEL_LOCAL_PREVIEW_ONLY','target':observation.page_id,'tx':tx,'writes':0,'observed_level':fields.get('LEVEL'),'version':observation.version}
