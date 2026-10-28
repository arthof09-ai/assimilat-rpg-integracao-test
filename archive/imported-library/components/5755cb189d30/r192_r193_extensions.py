"""IBX17: extensions reuse R129 contract and R151 spiritual progression.
No Notion writes, no attempt to bypass R129 refused native operation.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'core'/'history'))
sys.path.insert(0,str(ROOT/'core'/'runtime'))
from r129_rank_rebase_contract import BEFORE as R129_PRE,AFTER as R129_AFTER,validate as validate_rank
from r151_integrated_progression import preview as r151
from r148_evidence_binding import fractional_budget

def rank_cross_readonly():
 validate_rank(R129_PRE,R129_AFTER)
 a=R129_PRE;b=R129_AFTER
 return {'status':'RANK_CROSS_SOURCE_BOUND_HISTORICAL_CONTRACT_REUSED_TEST_ONLY','source_fixture':'IBX17-R129-R110','before_level':a['NORMAL']['level'],'after_level':b['NORMAL']['level'],
 'first_rank':a['NORMAL']['rank'],'next_rank':b['NORMAL']['rank'],'attributes_delta':{'INT':b['NORMAL']['attrs']['INT']-a['NORMAL']['attrs']['INT']},
 'hp_before':a['TRANSFORM']['hp_max'],'hp_after':b['TRANSFORM']['hp_max'],'pa_before':a['TRANSFORM']['pa_max'],'pa_after':b['TRANSFORM']['pa_max'],
 'hp_current':b['TRANSFORM']['hp_current'],'pa_current':b['TRANSFORM']['pa_current'],'ff':b['LOCKS']['ff'],
 'native_new_effects':0,'reused_historical_math_not_new_rank_native_certificate':True,'rank_native_class':'HOLD_IF_SECURITY_REFUSED_R129'}

def spirit_nonzero_readonly():
 base={'normal':{'level':17,'rank':'Ouro Negro','natural_attrs':{'FOR':6,'DES':10,'CON':10,'INT':8,'SAB':7,'CAR':4},'hp_max':309,'hp_current':240,'pa_max':273,'pa_current':150,'ff':290},'layers':{'title':{'SAB':2},'equipment':{'DES':3}},
 'spirit_overlay':{'bap_synthetic':11,'cap_ordinal':20,'allocation':{'SAB':93},'distributed_total':93,'carry_numerator':1,'carry_denominator':2,'effective_level':17,'proposed_attribute_for_next_gain':'SAB','active':False},
 'permanent_milestones':{'100':{'choice':'VIDA','rolls':[2,3],'source':'SYNTHETIC_ONLY'}},'consumed_events':[],'history':[]}
 a1=dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0);a2=dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0)
 first=r151(base,event='R193-FRESH-SYNTHETIC-STEP1',allocation=a1)
 assert first['spirit_increment']==6
 second=r151(first['after'],event='R193-FRESH-SYNTHETIC-STEP2',allocation=a2)
 assert second['spirit_increment']==5
 s=second['after'];o=s['spirit_overlay'];n=s['normal']
 assert n['level']==19 and n['hp_max']==343 and n['pa_max']==307
 assert o['distributed_total']==104 and o['carry_numerator']==1 and o['carry_denominator']==2
 assert not o['active'] and o['effective_level']==19 and o['normal_mirrored_attrs']==n['natural_attrs']
 # BAP is synthetic internal; never emit this value in a Party-safe report.
 result={'status':'SPIRIT_TAP_CARRY_TWO_LEVEL_SOURCE_SYNTHETIC_READONLY','levels':[17,18,19],'spirit_distributed_before':93,'spirit_distributed_after':104,'spirit_increment_steps':[6,5],'carry_before':'1/2','carry_after':'1/2','cap_level':20,'effective_level_after':19,'form_active':False,'normal_hp_max_after':343,'normal_pa_max_after':307,'normal_current_hp_after':240,'normal_current_pa_after':150,'source_class':'SYNTHETIC_ONLY','native_writes':0,'transformed_maxima_T6B':'PENDING_SOURCE_BOUND'}
 return result
if __name__=='__main__':print(json.dumps({'R192':rank_cross_readonly(),'R193':spirit_nonzero_readonly()},ensure_ascii=False,indent=2))
