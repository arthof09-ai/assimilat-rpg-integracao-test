"""IBX-17 R131 / T6-B + T9-A additive safe reserve engine. Synthetic calculation
and causal eligibility only; no Notion writer and no source-less official Spirit.
Distinct from old r112 guard and r122 carry state, both preserved.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict,replace
from fractions import Fraction
from typing import Optional,Mapping
class Hold(ValueError):pass

def fbudget(*,bap:int,actor_level:int,spirit_cap:int):
 if not (isinstance(bap,int) and bap>=0 and 0<=actor_level<=25 and spirit_cap>=0):raise Hold('BAD_BAP_OR_LEVEL')
 effective=min(actor_level,spirit_cap)
 raw=Fraction(bap,2)*effective
 return dict(effective_level=effective,tap_num=bap,tap_den=2,allocatable=raw.numerator//raw.denominator,carry_num=raw.numerator%raw.denominator,carry_den=raw.denominator)

def bonuses(*,normal_hp_max:int,normal_pa_max:int,theoretical_hp_form:int,theoretical_pa_form:int):
 vals=(normal_hp_max,normal_pa_max,theoretical_hp_form,theoretical_pa_form)
 if any(type(x)!=int or x<0 for x in vals):raise Hold('INVALID_MAX')
 return {'spirit_hp_reserve_max':max(0,theoretical_hp_form-normal_hp_max),'spirit_pa_reserve_max':max(0,theoretical_pa_form-normal_pa_max),'normal_max_unchanged':(normal_hp_max,normal_pa_max)}

@dataclass(frozen=True)
class Pools:
 normal_hp:int
 item_temp_hp:int
 spirit_temp_hp:int
 normal_pa:int
 spirit_pa:int
 normal_pa_max:int
 pa_committed:int=0
 form_active:bool=False
 def validate(self):
  if min(self.normal_hp,self.item_temp_hp,self.spirit_temp_hp,self.normal_pa,self.spirit_pa,self.normal_pa_max,self.pa_committed)<0:raise Hold('NEGATIVE_RESOURCE')
  if self.normal_pa>self.normal_pa_max:raise Hold('NORMAL_PA_ABOVE_MAX')
  return self

def damage(p:Pools,points:int):
 p.validate()
 if type(points)!=int or points<0:raise Hold('NEGATIVE_DAMAGE')
 remaining=points
 spirit=min(remaining,p.spirit_temp_hp) if p.form_active else 0;remaining-=spirit
 item=min(remaining,p.item_temp_hp);remaining-=item
 natural=min(remaining,p.normal_hp);remaining-=natural
 return replace(p,spirit_temp_hp=p.spirit_temp_hp-spirit,item_temp_hp=p.item_temp_hp-item,normal_hp=p.normal_hp-natural),{'spirit':spirit,'item':item,'normal':natural,'overkill':remaining}

def check_activation(ctx:Mapping):
 # These are not inferred from elapsed time or page narrative. Real source proof is required.
 required=('actor_id','spirit_id','spirit_source_page','spirit_source_version','source_ability_receipt','assimilation_evidence','scene_id','scene_authority','action_authorized','cost_source_confirmed','spirit_budget_checksum','theoretical_form_hp','theoretical_form_pa','duration_choice_receipt')
 if any(not ctx.get(k) for k in required):return 'HOLD_MISSING_IDENTITY_SOURCE_OR_SCENE'
 if ctx.get('actor_level',0)<6:return 'HOLD_BRONZE_PROHIBITED'
 if ctx.get('already_active'):return 'HOLD_ALREADY_ACTIVE'
 if ctx.get('scene_id') in ctx.get('used_scenes',[]):return 'HOLD_ONE_ACTIVATION_PER_SCENE'
 if ctx.get('last_used_scene') and not ctx.get('short_or_long_rest_completed_after_last_use'):return 'HOLD_REST_NOT_PROVEN'
 if not ctx.get('native_actor_source_bound') and not ctx.get('synthetic_test_scope'):return 'HOLD_UNAUTHENTICATED_SPIRIT'
 if ctx.get('action_kind')!='ACAO_COMPLETA':return 'HOLD_WRONG_ACTION_FOR_PRATA'
 if ctx.get('rank')!='Prata 1':return 'HOLD_RANK_NOT_SCOPED'
 if ctx.get('duration_d6') not in range(1,7):return 'HOLD_DURATION_UNRECORDED'
 if ctx.get('normal_pa_available',0)<40:return 'HOLD_ACTIVATION_COST_UNPAYABLE'
 if ctx.get('activation_receipt_id') in ctx.get('consumed_activation_events',[]):return 'NOOP_ALREADY_CONSUMED'
 return 'ADMISSIBLE_SYNTHETIC_TEST_ONLY' if ctx.get('synthetic_test_scope') else 'ADMISSIBLE_SOURCE_BOUND_PENDING_NATIVE'

def activate_test(p:Pools,*,event:str,ctx:dict,delta:dict):
 gate=check_activation(ctx)
 if gate!='ADMISSIBLE_SYNTHETIC_TEST_ONLY':raise Hold(gate)
 p.validate()
 if p.normal_pa<40:raise Hold('NORMAL_ACTIVATION_PA_NOT_ENOUGH')
 # T9 cost is explicit; generic technique cost priority stays HOLD.
 q=replace(p,normal_pa=p.normal_pa-40,spirit_pa=delta['spirit_pa_reserve_max'],spirit_temp_hp=delta['spirit_hp_reserve_max'],form_active=True)
 new=dict(ctx);new['used_scenes']=list(ctx.get('used_scenes',[]))+[ctx['scene_id']];new['consumed_activation_events']=list(ctx.get('consumed_activation_events',[]))+[event];new['last_used_scene']=ctx['scene_id'];new['already_active']=True
 return q,new

def deactivate(p:Pools,ctx:dict):
 if not p.form_active:raise Hold('NOT_ACTIVE')
 # The spent normal pools are persistent. Inaccessible spirit reserve is *not* restored by deactivation.
 return replace(p,form_active=False,spirit_pa=0,spirit_temp_hp=0),{**ctx,'already_active':False}

def checks():
 import copy
 count=0
 def ck(t):
  nonlocal count
  assert t;count+=1
 ck(fbudget(bap=11,actor_level=1,spirit_cap=8)['carry_num']==1)
 ck(fbudget(bap=11,actor_level=2,spirit_cap=8)['carry_num']==0)
 ck(fbudget(bap=11,actor_level=6,spirit_cap=4)['allocatable']==22)
 d=bonuses(normal_hp_max=300,normal_pa_max=300,theoretical_hp_form=1000,theoretical_pa_form=1000)
 ck(d['spirit_hp_reserve_max']==700 and d['spirit_pa_reserve_max']==700)
 ck(bonuses(normal_hp_max=54,normal_pa_max=142,theoretical_hp_form=50,theoretical_pa_form=130)['spirit_hp_reserve_max']==0)
 p=Pools(normal_hp=20,item_temp_hp=10,spirit_temp_hp=30,normal_pa=85,spirit_pa=50,normal_pa_max=100,form_active=True)
 q,j=damage(p,42);ck(j=={'spirit':30,'item':10,'normal':2,'overkill':0});ck(q.normal_hp==18 and q.spirit_temp_hp==q.item_temp_hp==0)
 inactive=replace(p,form_active=False);_,j=damage(inactive,11);ck(j['spirit']==0 and j['normal']==1)
 ctx={key:'synthetic_test_evidence' for key in ('actor_id','spirit_id','spirit_source_page','spirit_source_version','source_ability_receipt','assimilation_evidence','scene_id','scene_authority','action_authorized','cost_source_confirmed','spirit_budget_checksum','theoretical_form_hp','theoretical_form_pa','duration_choice_receipt')}
 ctx.update(actor_level=6,rank='Prata 1',action_kind='ACAO_COMPLETA',duration_d6=3,normal_pa_available=85,used_scenes=[],last_used_scene=None,synthetic_test_scope=True,activation_receipt_id='SYNTHETIC_EVT_1',consumed_activation_events=[])
 ck(check_activation(ctx)=='ADMISSIBLE_SYNTHETIC_TEST_ONLY')
 for change,want in [({'actor_level':5},'HOLD_BRONZE_PROHIBITED'),({'scene_id':''},'HOLD_MISSING_IDENTITY_SOURCE_OR_SCENE'),({'used_scenes':['synthetic_test_evidence']},'HOLD_ONE_ACTIVATION_PER_SCENE'),({'last_used_scene':'last','short_or_long_rest_completed_after_last_use':False},'HOLD_REST_NOT_PROVEN'),({'normal_pa_available':30},'HOLD_ACTIVATION_COST_UNPAYABLE'),({'action_kind':'ACAO_PADRAO'},'HOLD_WRONG_ACTION_FOR_PRATA'),({'duration_d6':None},'HOLD_DURATION_UNRECORDED'),({'spirit_id':None},'HOLD_MISSING_IDENTITY_SOURCE_OR_SCENE')]:ck(check_activation(ctx|change)==want)
 x,c=activate_test(p,event='SYNTHETIC_EVT_1',ctx=ctx,delta={'spirit_hp_reserve_max':70,'spirit_pa_reserve_max':60});ck(x.normal_pa==45 and x.spirit_temp_hp==70 and x.spirit_pa==60)
 ck(check_activation({**c,'already_active':False})=='HOLD_ONE_ACTIVATION_PER_SCENE')
 y,c=deactivate(x,c);ck(y.normal_pa==45 and y.normal_hp==20 and y.spirit_temp_hp==0)
 ck(check_activation(c|{'scene_id':'new_scene','short_or_long_rest_completed_after_last_use':False})=='HOLD_REST_NOT_PROVEN')
 ck(check_activation(c|{'scene_id':'new_scene','short_or_long_rest_completed_after_last_use':True,'activation_receipt_id':'SYNTHETIC_EVT_1'})=='NOOP_ALREADY_CONSUMED')
 return count
if __name__=='__main__':print('R131',checks(),'direct contracts PASS; source-free campaign activation BLOCKED')
