"""R134 conversational state protocol for existing IBX-17 chat flow.
State machine only; no second chatbot, no credentials, no fabricated human turn.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict,replace
from typing import Optional
from r127_receipt_protocol import sha,Hold,LAB

STATES=('REQUESTED','TARGET_RESOLVED','SOURCE_VERIFIED','CHOICES_PENDING','PREVIEW_READY','PREVIEW_PRESENTED','AWAITING_CONFIRMATION','CONFIRMED','CANCELED','STALE_SOURCE','COMMIT_IN_PROGRESS','COMMIT_VERIFIED','RECOVERY_REQUIRED')
@dataclass(frozen=True)
class Conversation:
 tx_id:str
 target_id:str
 target_parent:str
 target_version:str
 source_version:str
 preview_hash:str
 scope:str
 state:str='PREVIEW_PRESENTED'
 human_confirmation:Optional[dict]=None
 written:bool=False

def create(tx_id,target_id,parent,target_version,source_version,preview,scope='LAB_TEST'):
 if parent!=LAB or scope!='LAB_TEST':raise Hold('DESTINATION_FORBIDDEN')
 if not all([tx_id,target_id,target_version,source_version,preview]):raise Hold('MISSING_PREVIEW_IDENTITY')
 return Conversation(tx_id,target_id,parent,target_version,source_version,sha(preview),scope)

def present(c:Conversation):
 if c.state not in ('PREVIEW_PRESENTED','CHOICES_PENDING','PREVIEW_READY'):raise Hold('BAD_PREVIEW_STATE')
 return replace(c,state='AWAITING_CONFIRMATION')

def cancel(c:Conversation):
 if c.written or c.state in ('COMMIT_VERIFIED','COMMIT_IN_PROGRESS'):raise Hold('TOO_LATE_TO_CANCEL_WITHOUT_RECOVERY')
 return replace(c,state='CANCELED')

def review(c:Conversation,preview,source_version,target_version):
 if c.written:raise Hold('ALREADY_WRITTEN')
 if source_version!=c.source_version or target_version!=c.target_version:return replace(c,state='STALE_SOURCE',human_confirmation=None)
 if sha(preview)!=c.preview_hash:return replace(c,state='PREVIEW_READY',preview_hash=sha(preview),human_confirmation=None)
 return c

def confirm(c:Conversation,*,claimed_actor:str,channel:str,observed_human_turn:Optional[dict],preview,source_version,target_version):
 r=review(c,preview,source_version,target_version)
 if r.state!='AWAITING_CONFIRMATION':raise Hold(r.state)
 # Confirmation cannot be synthesized by a function call. A real chat observation
 # must be supplied by a trusted calling layer, with evidence distinguishable
 # from strings authored by this executor. This package cannot verify host IDs.
 if not observed_human_turn or not observed_human_turn.get('trusted_runtime_origin') or not observed_human_turn.get('verbatim_reply') or not observed_human_turn.get('turn_ref'):
  raise Hold('AWAITING_REAL_HUMAN_CONFIRMATION')
 if observed_human_turn.get('previews_seen_hash')!=c.preview_hash or observed_human_turn.get('role')!='user':raise Hold('CONFIRMATION_NOT_BOUND_TO_PREVIEW')
 if claimed_actor not in ('MESTRE',) or channel!='ChatGPT':raise Hold('UNAUTHORIZED_CONFIRMING_ACTOR')
 return replace(r,state='CONFIRMED',human_confirmation={'actor':claimed_actor,'channel':channel,'turn_ref':observed_human_turn['turn_ref'],'preview_hash':c.preview_hash,'scope':c.scope,'host_evidence_status':'EXTERNALLY_ATTESTED_BY_CALLER_NOT_CRYPTOGRAPHIC'})

def prepare_commit(c:Conversation,*,current_page_version:str,source_version:str,already_consumed:bool=False):
 if already_consumed:return {'decision':'NOOP_EVENT_ALREADY_CONSUMED','writes':0}
 if current_page_version!=c.target_version or source_version!=c.source_version:return {'decision':'STALE_REPREVIEW','writes':0}
 if c.state!='CONFIRMED' or not c.human_confirmation:return {'decision':'AWAITING_CONFIRMATION','writes':0}
 return {'decision':'ALLOW_TEST_ONLY_AFTER_NATIVE_REOPEN','target':c.target_id,'preview_hash':c.preview_hash,'writes':'NOT_EXECUTED_BY_THIS_MODULE'}

def tests():
 count=0
 def ck(t):
  nonlocal count
  assert t;count+=1
 preview={'from':16,'to':17,'alloc':[{'CAR':2}],'growth':'FIXED60_D12_7'}
 c=create('E','ID',LAB,'v1','rule_v1',preview)
 ck(c.state=='PREVIEW_PRESENTED')
 c=present(c);ck(c.state=='AWAITING_CONFIRMATION')
 ck(prepare_commit(c,current_page_version='v1',source_version='rule_v1')['decision']=='AWAITING_CONFIRMATION')
 try:confirm(c,claimed_actor='MESTRE',channel='ChatGPT',observed_human_turn=None,preview=preview,source_version='rule_v1',target_version='v1')
 except Hold:ck(True)
 else:raise AssertionError('fake confirmation accepted')
 ck(cancel(c).state=='CANCELED')
 ck(review(c,preview,'rule_v2','v1').state=='STALE_SOURCE')
 ck(review(c,{'from':16,'to':18},'rule_v1','v1').state=='PREVIEW_READY')
 ck(prepare_commit(c,current_page_version='v2',source_version='rule_v1')['decision']=='STALE_REPREVIEW')
 ck(prepare_commit(c,current_page_version='v1',source_version='rule_v1',already_consumed=True)['writes']==0)
 for kwargs in [{'target_parent':'PARTY'},{'scope':'PROD'}]:
  try:create('E','ID',kwargs.get('target_parent',LAB),'v1','rule_v1',preview,scope=kwargs.get('scope','LAB_TEST'))
  except Hold:ck(True)
  else:raise AssertionError('outside lab accepted')
 try:confirm(c,claimed_actor='MESTRE',channel='ChatGPT',observed_human_turn={'role':'user','turn_ref':'FAKE','verbatim_reply':'ok','previews_seen_hash':c.preview_hash},preview=preview,source_version='rule_v1',target_version='v1')
 except Hold:ck(True)
 else:raise AssertionError('untrusted caller accepted')
 return count
if __name__=='__main__':print('R134',tests(),'local direct contract checks PASS; real post-preview reply PENDING')
