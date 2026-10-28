"""R145 chat-facing confirmation adapter to historical R134 engine.
No fabricated user role / trusted turn. R144 structural TEST is real readback target.
"""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parents[1]/'history'
sys.path.insert(0,str(H))
from r134_conversation_authorization import create,present,confirm,prepare_commit,review,Hold
from r127_receipt_protocol import sha

TARGET='3fcc2b324ede81868256e6db67ece28e'
LAB='3fbc2b324ede804a95fafcb7b293c92c'
TX='IBX17-R145-CHAT-PREVIEW-20261017-01'
RULE='3ebc2b324ede81449222f3c06b840613@2026-10-09T04:07:06.313Z'
TARGET_VERSION='2026-10-17T12:04:36.271Z'
PREVIEW={
 'kind':'LAB_TEST_LEVEL_UP_PREVIEW_NOT_PLAYER_CHOICE','tx_id':TX,'target_id':TARGET,
 'from':{'level':17,'rank':'Ouro Negro 2','INT':8,'hp_max':309,'hp_current':240,'pa_max':273,'pa_current':150,'FF':290,'CA':23},
 'to':{'level':18,'rank':'Ouro Negro 3','INT':10,'hp_max':326,'hp_current':240,'pa_max':290,'pa_current':150,'FF':290,'CA':23},
 'candidate_choice':{'+INT':2,'growth':'FIXED60_D12_7','actor':'SYNTHETIC_TEST_ONLY_NOT_PARTY'},
 'preserve':['title +2 SAB synthetic','equipment +3 DES synthetic','FF and CA','root layout with columns/table/toggle','child R144','legacy R89 snapshots'],
 'source_rule':RULE,'page_version':TARGET_VERSION,
 'open_questions':['human confirmation after preview with authority','verify current page version before commit'],
 'write_set_on_confirmation':['root level','root INT','HP max','PA max','linked structural TABLE field with exact unique match'],
 'real_party_write':False,'canonical_spirit_activation':False}

def build():
 c=create(TX,TARGET,LAB,TARGET_VERSION,RULE,PREVIEW,scope='LAB_TEST')
 return present(c)

def selftest():
 c=build();assert c.state=='AWAITING_CONFIRMATION';assert c.preview_hash==sha(PREVIEW)
 assert prepare_commit(c,current_page_version=TARGET_VERSION,source_version=RULE)['decision']=='AWAITING_CONFIRMATION'
 assert prepare_commit(c,current_page_version='STALER',source_version=RULE)['decision']=='STALE_REPREVIEW'
 assert prepare_commit(c,current_page_version=TARGET_VERSION,source_version=RULE,already_consumed=True)['decision']=='NOOP_EVENT_ALREADY_CONSUMED'
 assert review(c,{**PREVIEW,'candidate_choice':{'+INT':1}},RULE,TARGET_VERSION).state=='PREVIEW_READY'
 try:confirm(c,claimed_actor='MESTRE',channel='ChatGPT',observed_human_turn=None,preview=PREVIEW,source_version=RULE,target_version=TARGET_VERSION)
 except Hold:pass
 else:raise AssertionError('accepted artificial confirmation')
 return {'checks':6,'state':c.state,'tx_id':TX,'target':TARGET,'target_version':TARGET_VERSION,'preview_hash':c.preview_hash,'manual_confirmation':'NOT_OBSERVED'}
if __name__=='__main__':
 r=selftest();out=Path(__file__).resolve().parents[1]/'evidence'/'R145_CHAT_PREVIEW_AWAITING_CONFIRMATION.json'
 out.write_text(json.dumps({'result':r,'preview':PREVIEW},indent=2,ensure_ascii=False));print(json.dumps(r,ensure_ascii=False))
