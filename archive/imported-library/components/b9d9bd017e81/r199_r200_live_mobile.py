"""IBX-17 R199–R200: real-source preview/choice state machine, no native writer.
Caller MUST re-fetch Notion physically before any commit and provide fresh
snapshot, not a boolean or a claimed host attestation.
"""
from __future__ import annotations
from dataclasses import dataclass,field
from copy import deepcopy
from hashlib import sha256
from r198_dynamic_source import ATTRS,SourceSnapshot,SourceHold,rank_at,sha
class GateHold(ValueError):pass
FIXED={'Bronze':4,'Prata':5,'Ouro':6,'Ouro Negro':7,'Lendário':12}

@dataclass
class MobileSession:
 source:SourceSnapshot
 event:str
 levels:int
 choices:list[dict]=field(default_factory=list)
 stage:str='AWAITING_CHOICES'
 preview_data:dict|None=None
 def __post_init__(self):
  if not self.event or not self.event.startswith('IBX17-'):raise GateHold('EVENT_ID_REQUIRED')
  if not isinstance(self.levels,int) or not 1<=self.levels<=5:raise GateHold('BAD_LEVEL_COUNT')
  if self.source.parent_id!='3fbc2b324ede804a95fafcb7b293c92c':raise GateHold('SOURCE_OUTSIDE_LAB')
 def request_choices(self):
  return {'state':self.stage,'source_id':self.source.page_id,'version':self.source.version,'rank':self.source.normal['rank'],'level':self.source.normal['level'],'points_per_level':self.source.normal['normal_rate'],'levels':self.levels,'choices_to_supply':self.levels,'writes':0}
 def cancel(self):
  if self.stage=='NATIVE_COMMITTED':raise GateHold('ALREADY_CONSUMED')
  self.stage='CANCELED';self.preview_data=None;return {'state':'CANCELED','writes':0}
 def revise(self,allocations,mode='FIXED60_EXPLICIT'):
  if self.stage not in ('AWAITING_CHOICES','PREVIEW_READY'):raise GateHold('NOT_REVISING')
  if mode!='FIXED60_EXPLICIT':raise GateHold('ROLL_OR_PERCENTAGE_EVIDENCE_REQUIRED')
  if not isinstance(allocations,list) or len(allocations)!=self.levels:raise GateHold('LEVEL_CHOICE_COUNT_MISMATCH')
  for a in allocations:
   if not isinstance(a,dict) or set(a)!=set(ATTRS) or any(type(v)!=int or v<0 for v in a.values()) or sum(a.values())!=self.source.normal['normal_rate']:
    raise GateHold('ATTRIBUTE_CHOICE_BUDGET_INVALID')
  self.choices=deepcopy(allocations);self.preview_data=self._calculate();self.stage='PREVIEW_READY'
  return self.preview_data
 def _calculate(self):
  src=self.source;n=deepcopy(src.normal);steps=[];holds=[]
  for i,a in enumerate(self.choices,1):
   prior=deepcopy(n);n['level']+=1
   if n['level']>25:raise GateHold('BEYOND_25_NO_RULE')
   newrank=rank_at(n['level'])
   if newrank!=prior['rank']:
    holds.append('RANK_CROSS_REBASE_REQUIRES_SEPARATE_SOURCE_BOUND_RULE')
    # cannot infer additive growth; never form false committed totals
    steps.append({'stage':i,'before':prior,'after':None,'allocation':a,'hold':'RANK_CROSS_PREVIEW_NO_ADDITIVE_MAX'})
    break
   for k,v in a.items():n['natural_attrs'][k]+=v
   n['hp_max']+=FIXED[newrank]+n['natural_attrs']['CON']
   n['pa_max']+=FIXED[newrank]+n['natural_attrs']['INT']
   n['pa_free']=n['pa_max']-n['pa_committed']
   effective={k:n['natural_attrs'][k]+sum(x.get(k,0) for x in src.layers.values()) for k in ATTRS}
   n['ff']=10*(effective['FOR']+effective['DES']+effective['CON'])
   if a['DES']>0:holds.append('CA_DEPENDS_ON_DESTREZA_UNVERIFIED')
   if a['FOR']>0:holds.append('LUTA_DEPENDS_ON_FORCA_UNVERIFIED')
   if n['ff']!=prior['ff']:holds.append('FF_MILESTONE_AND_DERIVATIVES_SOURCE_GATE')
   if n['magic_cd'] is not None:n['magic_cd']+=a['INT']
   steps.append({'stage':i,'before':prior,'after':deepcopy(n),'allocation':a,'growth_fixed':FIXED[newrank], 'life_increment':FIXED[newrank]+n['natural_attrs']['CON'],'soul_increment':FIXED[newrank]+n['natural_attrs']['INT']})
  result={'tx':self.event,'source_id':src.page_id,'source_version':src.version,'source_hash':src.source_hash,'source_fingerprint':src.fingerprint(),'before':src.normal,'after':n if len(steps)==self.levels and all(s.get('after') is not None for s in steps) else None,'steps':steps,'allocations':deepcopy(self.choices),'mode':'FIXED60_EXPLICIT','holds':sorted(set(holds)),'writes':0,'production':False,'party':False,'spirit':'INACTIVE_UNLESS_SOURCE_BOUND_SEPARATE_GATE', 'structure':src.structural}
  result['preview_hash']=sha({k:v for k,v in result.items() if k!='preview_hash'})
  return result
 def revalidate_for_write(self,new_readback:SourceSnapshot,expected_preview_hash:str,*,approval):
  """NO BOOLEAN CERTIFICATION. Returns HOLD/READY_FOR_EXTERNAL_HOST_VERIFICATION.
  Human consent must be an externally observed, post-preview event. This method
  never certifies its authenticity; the connected orchestration must verify it.
  """
  if self.stage!='PREVIEW_READY':raise GateHold('PREVIEW_NOT_READY')
  if self.preview_data['preview_hash']!=expected_preview_hash:raise GateHold('PREVIEW_HASH_CHANGED')
  if new_readback.page_id!=self.source.page_id or new_readback.parent_id!=self.source.parent_id:raise GateHold('READBACK_TARGET_CHANGED')
  if new_readback.version!=self.source.version or new_readback.source_hash!=self.source.source_hash:raise GateHold('STALE_NOTION_SOURCE_RECALCULATE')
  if self.preview_data['holds']:raise GateHold('UNRESOLVED_SOURCE_GATES')
  if approval is None:raise GateHold('AWAITING_REAL_HUMAN_APPROVAL')
  # Do not accept claimant-crafted truth flags, independent of tests/mock.
  raise GateHold('HOST_APPROVAL_PROVENANCE_MUST_BE_VERIFIED_EXTERNALLY_NO_AUTOCOMMIT')

# Physical terminal certificate is derived only from same-page, same-event observed text.
def verify_native_effect(*,before:SourceSnapshot,after:SourceSnapshot,before_body:str,after_body:str,expected_edits:list,tx:str,journal_label:str):
 if before.page_id!=after.page_id or before.parent_id!=after.parent_id:raise GateHold('IDENTITY_CHANGED')
 if before.source_hash!=sha(before_body) or after.source_hash!=sha(after_body):raise GateHold('SOURCE_HASH_CONFLICT')
 if before.version==after.version:raise GateHold('NO_NEW_OBSERVED_VERSION')
 expected=before_body
 for old,new in expected_edits:
  if expected.count(old)!=1:raise GateHold('BEFORE_FIELD_AMBIGUOUS')
  expected=expected.replace(old,new,1)
 # journaling adds extra changes and needs separate exact controlled diff verification.
 if not after_body.startswith(expected):raise GateHold('AFTER_FIELDS_DIFFER_FROM_EXPECTED')
 journal=f'TX_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK; tx={tx}'
 if after_body.count(journal)!=1 or journal_label not in after_body:raise GateHold('JOURNAL_NOT_PHYSICALLY_VERIFIED')
 return {'decision':'NATIVE_AFTER_SELF_REVIEW_ONLY','source':after.page_id,'version':after.version,'tx':tx,'writes':0,'host_attested':False}
