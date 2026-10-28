"""IBX-17 R127 / additive causal writing protocol. No Notion credentials.
Pure receipts/state transitions; connector orchestration is outside this module.
No native operation id invented; self-review is NEVER independent review.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass,asdict
from typing import Any

LAB='3fbc2b324ede804a95fafcb7b293c92c'
PHASES=('INTENT_PREPARED','WRITE_DISPATCHED','WRITE_RESPONSE_OBSERVED','AFTER_READBACK_CONFIRMED','JOURNAL_COMMITTED')
TERMINAL=('RECOVERY_REQUIRED','UNKNOWN_EFFECT')

def canonical(obj:Any)->str:return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(obj:Any)->str:return hashlib.sha256(canonical(obj).encode('utf-8')).hexdigest()
class Hold(ValueError):pass

@dataclass(frozen=True)
class Intent:
 tx_id:str;target_id:str;parent_id:str;pre_version:str;source_version:str;source_hash:str;authority:str;stage:str;before_hash:str;after_hash:str;operator_profile_id:str
 def check(self):
  if self.parent_id!=LAB or self.authority!='LAB_TEST_EXPLICIT_FROM_MESTRE':raise Hold('AUTHORITY_OR_PARENT')
  if any(not v for v in asdict(self).values()):raise Hold('IDENTITY_INCOMPLETE')
  for k in (self.source_hash,self.before_hash,self.after_hash):
   if len(k)!=64 or any(c not in '0123456789abcdef' for c in k):raise Hold('INVALID_SHA256')
  return True

def transition(receipt:dict,phase:str,*,evidence:dict=None)->dict:
 """Never advances after a failed observation or a guessed native write."""
 if phase not in PHASES+TERMINAL:raise Hold('BAD_PHASE')
 old=receipt['phase']; rev={p:i for i,p in enumerate(PHASES)}
 if phase in TERMINAL:
  if old=='JOURNAL_COMMITTED':raise Hold('CANNOT_DEGRADE_TERMINAL')
 elif rev.get(phase,-1)!=rev.get(old,-2)+1:raise Hold('PHASE_ORDER_VIOLATION')
 if phase=='WRITE_RESPONSE_OBSERVED' and not (evidence or {}).get('tool_response_original'):raise Hold('NATIVE_RESPONSE_MISSING')
 if phase=='AFTER_READBACK_CONFIRMED':
  if (evidence or {}).get('observed_hash')!=receipt['intent']['after_hash'] or not (evidence or {}).get('observed_page_version'):raise Hold('AFTER_NOT_PROVEN')
 if phase=='JOURNAL_COMMITTED' and not (evidence or {}).get('journal_readback_version'):raise Hold('JOURNAL_NOT_READBACK')
 x={**receipt,'phase':phase,'history':list(receipt.get('history',[]))+[{'phase':phase,'evidence':evidence or {}}]}
 return x

def review_gate(audit:dict,*,source_page_id:str,source_version:str,evidence_sha:str)->str:
 """Review signature is documentary, not cryptographic. A label cannot create independence."""
 expected={'reviewer_identity','auditor_page_id','examined_page_id','examined_version','evidence_sha','finding','reviewed_at'}
 if not audit or any(not audit.get(k) for k in expected):return 'SELF_REVIEW_ONLY'
 if audit['examined_page_id']!=source_page_id or audit['examined_version']!=source_version or audit['evidence_sha']!=evidence_sha:return 'REVIEW_MISMATCH_HOLD'
 if audit.get('reviewer_identity')==audit.get('executor_identity') or not audit.get('different_author_observed'):return 'SELF_REVIEW_ONLY'
 if not audit.get('auditor_object_readback_verified'):return 'AUDIT_DOC_PENDING'
 return 'EXTERNAL_AUDIT_DOCUMENTED_NOT_CRYPTOGRAPHIC'

def classify_gap(intent:Intent,*,before,after,physical,journal,phase,tool_response,version,observed_version)->str:
 intent.check()
 if version!=observed_version:return 'VERSION_CHANGED_HOLD'
 h=sha(physical)
 if h not in (sha(before),sha(after)):return 'UNKNOWN_EFFECT'
 if h==sha(before) and journal=='COMMITTED':return 'JOURNAL_AHEAD_HOLD'
 if h==sha(after) and journal=='PREPARED':
  if not tool_response or phase not in ('WRITE_RESPONSE_OBSERVED','AFTER_READBACK_CONFIRMED','RECOVERY_REQUIRED'):return 'AFTER_CAUSE_UNPROVEN_HOLD'
  if sha(after)!=intent.after_hash:return 'OTHER_EVENT_COLLISION'
  return 'CAUSAL_JOURNAL_REPAIR_CANDIDATE_SELF_REVIEW'
 if h==sha(after) and journal=='COMMITTED':return 'COMMITTED_AFTER_READBACK_CANDIDATE'
 return 'BEFORE_NOT_APPLIED'

def selftest():
 import dataclasses
 obj={'x':1};aft={'x':2};h=sha({'source':'demo'})
 I=Intent('T','ID',LAB,'v0','RULE@v0',h,'LAB_TEST_EXPLICIT_FROM_MESTRE','NORMAL',sha(obj),sha(aft),'profile-master')
 checks=[]
 def ck(value):checks.append(bool(value));assert value
 ck(I.check())
 r={'intent':asdict(I),'phase':'INTENT_PREPARED','history':[]}
 r=transition(r,'WRITE_DISPATCHED');r=transition(r,'WRITE_RESPONSE_OBSERVED',evidence={'tool_response_original':'{page_id:ID}'})
 ck(r['phase']=='WRITE_RESPONSE_OBSERVED')
 ck(classify_gap(I,before=obj,after=aft,physical=aft,journal='PREPARED',phase=r['phase'],tool_response='{}',version='v1',observed_version='v1').startswith('CAUSAL_'))
 for kw in [{'version':'v1','observed_version':'v2'},{'physical':{'x':3}},{'tool_response':None}]:
  q=dict(before=obj,after=aft,physical=aft,journal='PREPARED',phase=r['phase'],tool_response='{}',version='v1',observed_version='v1');q.update(kw)
  ck(classify_gap(I,**q)!='CAUSAL_JOURNAL_REPAIR_CANDIDATE_SELF_REVIEW')
 ck(review_gate({'reviewer_identity':'X'},source_page_id='ID',source_version='v1',evidence_sha='SHA')=='SELF_REVIEW_ONLY')
 ck(review_gate({'reviewer_identity':'X','auditor_page_id':'P','examined_page_id':'ID','examined_version':'v1','evidence_sha':'SHA','finding':'PASS','reviewed_at':'now','executor_identity':'X','different_author_observed':True,'auditor_object_readback_verified':True},source_page_id='ID',source_version='v1',evidence_sha='SHA')=='SELF_REVIEW_ONLY')
 ck(review_gate({'reviewer_identity':'X','auditor_page_id':'P','examined_page_id':'ID','examined_version':'v1','evidence_sha':'SHA','finding':'PASS','reviewed_at':'now','executor_identity':'Y','different_author_observed':True,'auditor_object_readback_verified':True},source_page_id='ID',source_version='v1',evidence_sha='SHA')=='EXTERNAL_AUDIT_DOCUMENTED_NOT_CRYPTOGRAPHIC')
 for op in ('WRITE_DISPATCHED','JOURNAL_COMMITTED'):
  try:transition(r,op)
  except Hold:ck(True)
  else:ck(False)
 ck(sha(obj)!=sha(aft))
 return len(checks)
if __name__=='__main__':print('R127',selftest(),'direct assertions PASS')
