"""IBX17 R147 additive replacement of R134.confirm; historical files remain immutable.
Caller-made dictionaries, booleans and arbitrary turn refs have ZERO authorization.
Only Ed25519 host-signature verified against a separately pinned PUBLIC verification key,
for a post-preview user turn and exact preview/source/target can advance; absent actual
host attestation the state remains AWAITING_CONFIRMATION. Test keys are explicitly UNIT.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json,base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
class AuthorizationHold(ValueError):pass

def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(x):return sha256(canon(x)).hexdigest()
@dataclass(frozen=True)
class PreviewBinding:
 event:str; actor:str; conversation_id:str; target_id:str; parent_id:str; target_version:str; source_version:str; choices:dict; preview_hash:str; scope:str; presented_turn_ordinal:int

def binding(event,actor,conversation_id,target_id,parent_id,target_version,source_version,choices,preview,scope,presented_turn_ordinal):
 if scope!='LAB_TEST' or parent_id!='3fbc2b324ede804a95fafcb7b293c92c':raise AuthorizationHold('NON_LAB_SCOPE')
 return PreviewBinding(event,actor,conversation_id,target_id,parent_id,target_version,source_version,choices,digest(preview),scope,presented_turn_ordinal)

class HostAttestationVerifier:
 """Created by external trusted bridge with pinned key. No private key or signer here.
 Test public keys verify syntax, never confer host authority for real commits.
 """
 def __init__(self,public_key_raw:bytes,*,trust_domain:str):
  if trust_domain!='UNIT_TEST_ONLY':raise AuthorizationHold('NO_HOST_PINNED_KEY_REGISTERED')
  self._key=Ed25519PublicKey.from_public_bytes(public_key_raw)
  self._domain=trust_domain
 def verify(self,signature_b64:str,observation:dict)->bool:
  try:self._key.verify(base64.b64decode(signature_b64,validate=True),canon(observation));return True
  except (ValueError,InvalidSignature):return False

def confirm(preview:PreviewBinding,*,observation:dict,signature_b64:str|None,verifier:HostAttestationVerifier|None,current_source_version:str,current_target_version:str,current_choices:dict,already_consumed:bool=False):
 if already_consumed:return {'decision':'NOOP_ALREADY_CONSUMED','write_authorized':False}
 if current_source_version!=preview.source_version or current_target_version!=preview.target_version or current_choices!=preview.choices:return {'decision':'STALE_REPREVIEW','write_authorized':False}
 if not verifier or not signature_b64 or not observation:return {'decision':'AWAITING_HOST_ATTESTATION','write_authorized':False}
 if not verifier.verify(signature_b64,observation):return {'decision':'HOLD_INVALID_SIGNATURE','write_authorized':False}
 expected={'event':preview.event,'actor':preview.actor,'conversation_id':preview.conversation_id,'target_id':preview.target_id,'target_version':preview.target_version,'source_version':preview.source_version,'preview_hash':preview.preview_hash,'choices':preview.choices,'scope':preview.scope,'role':'user'}
 if any(observation.get(k)!=v for k,v in expected.items()):return {'decision':'HOLD_ATTESTED_CLAIM_MISMATCH','write_authorized':False}
 if not isinstance(observation.get('turn_ordinal'),int) or observation['turn_ordinal']<=preview.presented_turn_ordinal:return {'decision':'HOLD_NOT_AFTER_PREVIEW','write_authorized':False}
 if observation.get('decision')=='CANCEL':return {'decision':'CANCELED','write_authorized':False}
 if observation.get('decision')!='CONFIRM':return {'decision':'AWAITING_EXPLICIT_DECISION','write_authorized':False}
 if verifier._domain=='UNIT_TEST_ONLY':return {'decision':'UNIT_TEST_SIGNATURE_VALID_NO_NATIVE_AUTHORITY','write_authorized':False}
 return {'decision':'HOLD_NO_TRUSTED_HOST_CHANNEL','write_authorized':False}

def selftest():
 from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
 from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
 k=Ed25519PrivateKey.generate(); pub=k.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
 v=HostAttestationVerifier(pub,trust_domain='UNIT_TEST_ONLY')
 p=binding('E','MESTRE','C','TARGET','3fbc2b324ede804a95fafcb7b293c92c','v1','rule1',{'INT':2},{'delta':2},'LAB_TEST',12)
 obs=dict(event=p.event,actor=p.actor,conversation_id=p.conversation_id,target_id=p.target_id,target_version=p.target_version,source_version=p.source_version,preview_hash=p.preview_hash,choices=p.choices,scope=p.scope,role='user',turn_ordinal=13,turn_id='TEST_SIGNED',decision='CONFIRM')
 sign=lambda o:base64.b64encode(k.sign(canon(o))).decode()
 run=lambda o,s=None,**kwargs:confirm(p,observation=o,signature_b64=s,verifier=v,current_source_version='rule1',current_target_version='v1',current_choices={'INT':2},**kwargs)
 checks=[]
 def ck(x):assert x;checks.append(1)
 ck(run({**obs,'trusted_runtime_origin':True},None)['decision']=='AWAITING_HOST_ATTESTATION')
 ck(run({**obs,'trusted_runtime_origin':True},'FAKE')['decision']=='HOLD_INVALID_SIGNATURE')
 ck(run(obs,sign(obs))['decision']=='UNIT_TEST_SIGNATURE_VALID_NO_NATIVE_AUTHORITY')
 for changed in ({'turn_ordinal':12},{'target_id':'OTHER'},{'preview_hash':'fake'},{'event':'OLD'},{'actor':'OTHER'},{'conversation_id':'OTHER'},{'choices':{'INT':1}}):
  o=obs|changed;ck(run(o,sign(o))['decision'].startswith('HOLD_'))
 ck(run(obs|{'decision':'CANCEL'},sign(obs|{'decision':'CANCEL'}))['decision']=='CANCELED')
 ck(run(obs,sign(obs),already_consumed=True)['decision']=='NOOP_ALREADY_CONSUMED')
 ck(confirm(p,observation=obs,signature_b64=sign(obs),verifier=v,current_source_version='rule2',current_target_version='v1',current_choices={'INT':2})['decision']=='STALE_REPREVIEW')
 ck(confirm(p,observation=obs,signature_b64=sign(obs),verifier=v,current_source_version='rule1',current_target_version='v2',current_choices={'INT':2})['decision']=='STALE_REPREVIEW')
 ck(confirm(p,observation=obs,signature_b64=sign(obs),verifier=v,current_source_version='rule1',current_target_version='v1',current_choices={'INT':1})['decision']=='STALE_REPREVIEW')
 try:HostAttestationVerifier(pub,trust_domain='HOST_V1')
 except AuthorizationHold:ck(True)
 else:raise AssertionError('caller self-declared HOST_V1')
 try:binding('E','M','C','PARTY','PARTY','v','v',{}, {},'PARTY',12)
 except AuthorizationHold:ck(True)
 else:raise AssertionError('party accepted')
 return {'checks':len(checks),'unit_signed_token':'UNIT_TEST_ONLY_NO_NATIVE_AUTHORITY','host_pinned_key':'NOT_AVAILABLE_IN_THIS_SESSION','R145':'AWAITING_CONFIRMATION'}
if __name__=='__main__':print(json.dumps(selftest(),ensure_ascii=False))
