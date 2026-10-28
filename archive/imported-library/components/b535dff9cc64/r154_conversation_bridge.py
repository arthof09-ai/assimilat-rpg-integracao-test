"""R154 mobile/chat-facing LEVEL-UP controller (not another chatbot).
Routes prior R124 intents, R147 strict authorization, and R152 previews.
No production writers, no forged host attestation, no background execution.
"""
from __future__ import annotations
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'));sys.path.insert(0,str(ROOT/'history'))
from r147_secure_confirmation import binding,confirm
from r152_generic_structural_adapter import parse_sections,column_config,Hold
from r124_conversation_controller import parse_request

TARGET_R145='3fcc2b324ede81868256e6db67ece28e'
TARGET_R145_VERSION='2026-10-17T12:04:36.271Z'
EVENT_R145='IBX17-R145-CHAT-PREVIEW-20261017-01'
HASH_R145='64f6db1fa69512cfd14ec24bccaeb86e7c109c517dedbd0e2e0498dec32c0e46'

def request(text,*,target_id,parent_id,version,source_version,known_previews):
 intent=parse_request(text)
 if parent_id!='3fbc2b324ede804a95fafcb7b293c92c':return {'status':'HOLD_NON_TEST_TARGET','writes':0}
 if intent['intent']=='CANCEL':return {'status':'CANCELED_PREVIEW_NO_WRITE','writes':0}
 if intent['intent']=='LEVEL_DOWN':return {'status':'AWAITING_LEVEL_DOWN_SPECIFIC_CORRECTIONS','writes':0}
 if intent['intent']=='LEVEL_UP':return {'status':'AWAITING_EXPLICIT_ALLOCATIONS_AND_PREVIEW_CONFIRMATION','levels':intent.get('levels',1),'writes':0}
 if intent['intent'] in ('TRANSFORM_PREVIEW','INSPECT_LAYERS','PREVIEW','QUERY_TRANSACTION','REVISE_PREVIEW'):
  return {'status':'READ_ONLY_INTENT','intent':intent['intent'],'writes':0}
 return {'status':'AWAITING_INTENT','writes':0}

def resume_r145(*,target_id,target_version,host_verifier=None,observed_human_turn=None,signature_b64=None):
 if target_id!=TARGET_R145:return {'status':'WRONG_TARGET_HOLD','writes':0}
 if target_version!=TARGET_R145_VERSION:return {'status':'STALE_REPREVIEW','writes':0}
 if not observed_human_turn or not host_verifier:return {'status':'AWAITING_CONFIRMATION','preview_sha256':HASH_R145,'writes':0,'has_host_attestation':False}
 return {'status':'NEEDS_TRUSTED_HOST_VERIFICATION_NOT_AVAILABLE','writes':0}

def selftest():
 a=request('Suba 3 níveis',target_id='T',parent_id='3fbc2b324ede804a95fafcb7b293c92c',version='v',source_version='v',known_previews=[])
 b=request('Corrigir atributos sem perder nível',target_id='T',parent_id='3fbc2b324ede804a95fafcb7b293c92c',version='v',source_version='v',known_previews=[])
 c=request('Simular transformação',target_id='T',parent_id='3fbc2b324ede804a95fafcb7b293c92c',version='v',source_version='v',known_previews=[])
 d=request('Cancelar prévia',target_id='T',parent_id='3fbc2b324ede804a95fafcb7b293c92c',version='v',source_version='v',known_previews=[])
 assert a['levels']==3 and b['status'].startswith('AWAITING_LEVEL_DOWN') and c['intent']=='TRANSFORM_PREVIEW' and d['writes']==0
 assert request('Suba um nível',target_id='PARTY',parent_id='PARTY',version='v',source_version='v',known_previews=[])['status']=='HOLD_NON_TEST_TARGET'
 assert resume_r145(target_id=TARGET_R145,target_version=TARGET_R145_VERSION)['status']=='AWAITING_CONFIRMATION'
 assert resume_r145(target_id=TARGET_R145,target_version='vNEW')['status']=='STALE_REPREVIEW'
 assert resume_r145(target_id='OTHER',target_version=TARGET_R145_VERSION)['status']=='WRONG_TARGET_HOLD'
 return {'checks':8,'R145':'AWAITING_CONFIRMATION','host_trust':'NOT_AVAILABLE','native_writes':0}
if __name__=='__main__':print(json.dumps(selftest(),ensure_ascii=False))
