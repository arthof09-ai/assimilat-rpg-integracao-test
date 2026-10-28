"""R195 mobile ChatGPT dialogue adapter layered over R151 core, not another engine.
Reads connected source outside Python; all active choices remain revisable until
native dispatch. Chat text never serves as cryptographic HOST attestation.
"""
from __future__ import annotations
from dataclasses import dataclass,field
from copy import deepcopy
from r188_r189_vertical import parse_mobile,initial_test_state,calculate,canonical_hash,LAB,VerticalHold
ATTRS=('FOR','DES','CON','INT','SAB','CAR')
class ConversationHold(ValueError): pass

@dataclass
class MobileSession:
 fixture_id:str
 physical_version:str
 source_binding:str
 tx:str
 allocations:list[dict]|None=None
 stage:str='CREATED'
 frozen_digest:str|None=None
 preview:dict|None=None
 history:list=field(default_factory=list)
 def source(self):return initial_test_state(fixture_id=self.fixture_id)
 def start(self,utterance):
  req=parse_mobile(utterance)
  if req.get('intent')!='LEVEL_UP':raise ConversationHold('NOT_LEVEL_UP_REQUEST')
  self.levels=req['levels'];self.stage='AWAITING_ALLOCATION'
  self.history.append(('REQUEST',utterance))
  return {'state':self.stage,'levels':self.levels,'options_per_level':self.source()['normal']['normal_rate'],'available_attributes':ATTRS,'choice_mode':'ROLL_OR_FIXED60_TEST','writes':0}
 def choose(self,allocations,mode='FIXED60_EXPLICIT'):
  if self.stage not in ('AWAITING_ALLOCATION','PREVIEW_READY'):raise ConversationHold('CHOICE_NOT_ADMISSIBLE')
  if len(allocations)!=self.levels:raise ConversationHold('LEVEL_BUDGET_COUNT_MISMATCH')
  self.allocations=deepcopy(allocations)
  if mode!='FIXED60_EXPLICIT':raise ConversationHold('ROLL_EVIDENCE_NOT_AVAILABLE')
  try:self.preview=calculate(self.source(),tx=self.tx,per_level_allocations=self.allocations,mode=mode)
  except VerticalHold as e:raise ConversationHold(str(e))
  self.frozen_digest=canonical_hash({'source_binding':self.source_binding,'physical_version':self.physical_version,'allocations':self.allocations,'after_hash':self.preview['after_hash'],'tx':self.tx})
  self.stage='PREVIEW_READY';self.history.append(('PREVIEW',self.frozen_digest))
  n=self.preview['after']['normal']
  return {'state':self.stage,'before_level':17,'after_level':n['level'],'choices':self.allocations,'changes':self.preview['changes'],'stepwise':self.preview['steps'],'preview_sha':self.frozen_digest,'current_resources_unaltered':True,'historical_save_required':True,'writes':0}
 def cancel(self):
  if self.stage=='NATIVE_AFTER':raise ConversationHold('CANNOT_CANCEL_CONSUMED_NATIVE_EFFECT')
  self.stage='CANCELED';self.history.append(('CANCEL',None));return {'state':'CANCELED_NO_WRITE','native_writes':0}
 def request_apply(self,utterance,*,target_current_version,observed_host_attestation=False,lab_directive=None):
  if self.stage!='PREVIEW_READY':raise ConversationHold('PREVIEW_NOT_READY')
  if parse_mobile(utterance).get('intent')!='CONFIRM_NO_HOST_ATTESTATION':raise ConversationHold('NOT_CONFIRMATION_TEXT')
  if target_current_version!=self.physical_version:return {'state':'STALE_PREVIEW_MUST_RECALCULATE','write_authorized':False}
  if lab_directive!='DIR-MESTRE-LABS-REPLICAS-20261016-001':return {'state':'LAB_AUTHORITY_NOT_ESTABLISHED','write_authorized':False}
  self.stage='PENDING_CONNECTED_WRITE'
  return {'state':self.stage,'test_authority':'LAB_DIR_MESTRE','dialogue_phrase_is_not_signature':True,'host_attestation':bool(observed_host_attestation),'production_authorized':False,'connected_write_requires_live_parent_version_recheck':True,'preview_sha':self.frozen_digest,'tx':self.tx}
 def observe_after(self,*,physical_after_matches,history_verified,journal_verified):
  if self.stage!='PENDING_CONNECTED_WRITE':raise ConversationHold('NATIVE_DISPATCH_NOT_ADMITTED')
  if not (physical_after_matches and history_verified and journal_verified):
   self.stage='HOLD_PARTIAL_AFTER';return {'state':self.stage,'native_effect_uncertain':True}
  self.stage='NATIVE_AFTER';return {'state':self.stage,'source':'NATIVE_READBACK_SELF_REVIEW','production':False}

def demo():
 s=MobileSession(fixture_id='TEST_NO_NATIVE_WRITE',physical_version='v',source_binding='IBX17-R99',tx='BLIND-LOCAL-TEST')
 a=s.start('Quero subir dois níveis com este personagem')
 choice=[dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0),dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0)]
 b=s.choose(choice)
 revised=[dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0),dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0)]
 c=s.choose(revised)
 d=s.request_apply('confirmo',target_current_version='v',lab_directive='DIR-MESTRE-LABS-REPLICAS-20261016-001')
 assert c['preview_sha']!=b['preview_sha'] and d['state']=='PENDING_CONNECTED_WRITE'
 return {'start':a,'first_preview':b['changes'],'revised_preview':c['changes'],'gate':d,'status':'NO_NATIVE_WRITE_LOCAL_UX_TEST'}
if __name__=='__main__':
 import json
 print(json.dumps(demo(),ensure_ascii=False,indent=2))
