"""Level-up R204/R205 source-bound READ-ONLY extension, no native writes."""
from fractions import Fraction
from dataclasses import dataclass
from r198_dynamic_source import sha
class ExtendedHold(ValueError):pass

SOURCE_RULE5='3ebc2b324ede81449222f3c06b840613'
SOURCE_TRANSFORM='3f2c2b324ede81c0ae0ee4e66212edc9'
SOURCE_VZ='3f2c2b324ede8168b50ee4254134d821'

def rank_cross_preview(*,previous_level,attributes,life_max,pa_max,current_life,current_pa,allocation,source_version):
 if previous_level!=5 or attributes!={'FOR':4,'DES':3,'CON':2,'INT':14,'SAB':6,'CAR':6}:raise ExtendedHold('OTHER_CROSS_REQUIRES_SOURCE')
 if allocation!={'INT':2} or life_max!=42 or pa_max!=86:raise ExtendedHold('R105_FIXTURE_REQUIREMENT')
 if not source_version:raise ExtendedHold('SOURCE_UNOBSERVED')
 if current_life>54 or current_pa>142:raise ExtendedHold('CURRENT_OVER_NEW_MAX')
 return {'scope':'LAB_TEST_PREVIEW_ONLY','rule':'RANK_REBASE_REPLACE_NATURAL','source':SOURCE_RULE5,'source_version':source_version,'before':{'level':5,'rank':'Bronze 5','life_max':42,'pa_max':86,'hp_current':current_life,'pa_current':current_pa},'after':{'level':6,'rank':'Prata 1','INT':16,'life_max':54,'pa_max':142,'hp_current':current_life,'pa_current':current_pa,'spirit_active':False},'negative_cases_rejected':[{'hp':96,'pa':228}],'native_writes':0,'source_rank_gate':'R129_HISTORICAL_HOLD_NO_RETRY'}

def spirit_progression_preview(*,actor_id,spirit_id,source_version,bap,effective_before,effective_after,allocation_before,allocation_after,cap):
 if not source_version:raise ExtendedHold('SOURCE_UNOBSERVED')
 if not actor_id or not spirit_id:raise ExtendedHold('IDENTITY_MISSING')
 if effective_after>cap or effective_before>cap:raise ExtendedHold('ABOVE_SPIRIT_CAP')
 if effective_after!=effective_before+1:raise ExtendedHold('GRANULAR_PROGRESS_ONLY')
 tap=Fraction(bap,2);old_budget=tap*effective_before;new_budget=tap*effective_after
 if sum(allocation_before.values())!=old_budget.numerator//old_budget.denominator:raise ExtendedHold('PRE_DISTRIBUTION_MISMATCH')
 if sum(allocation_after.values())!=new_budget.numerator//new_budget.denominator:raise ExtendedHold('AFTER_DISTRIBUTION_MISMATCH')
 if any(allocation_after[k]<v for k,v in allocation_before.items()):raise ExtendedHold('NEGATIVE_ATTRIBUTE_SPIRIT_DELTA')
 return {'scope':'VZ_SANDBOX_SOURCE_BOUND_READONLY','actor':actor_id,'spirit':spirit_id,'source':SOURCE_VZ,'source_version':source_version,'tap':str(tap),'before':{'effective':effective_before,'budget_distributed':sum(allocation_before.values()),'carry':str(old_budget-int(old_budget))},'after':{'effective':effective_after,'budget_distributed':sum(allocation_after.values()),'carry':str(new_budget-int(new_budget))},'delta':{k:allocation_after[k]-v for k,v in allocation_before.items()},'form_active':False,'pa_spirit_newly_available':False,'native_writes':0,'certified_main_campaign':False}

if __name__=='__main__':
 rc=rank_cross_preview(previous_level=5,attributes={'FOR':4,'DES':3,'CON':2,'INT':14,'SAB':6,'CAR':6},life_max=42,pa_max=86,current_life=20,current_pa=45,allocation={'INT':2},source_version='2026-10-09T04:07:06.313Z')
 a={'FOR':21,'DES':63,'CON':31,'INT':52,'SAB':42,'CAR':11}
 b={'FOR':22,'DES':66,'CON':33,'INT':55,'SAB':44,'CAR':11}
 s=spirit_progression_preview(actor_id='KAEL-VZ-SANDBOX',spirit_id='SERPENTE-VZ-SANDBOX',source_version='2026-10-07T21:52:35.997Z',bap=21,effective_before=21,effective_after=22,allocation_before=a,allocation_after=b,cap=22)
 assert rc['after']['life_max']==54 and rc['after']['pa_max']==142
 assert s['before']['budget_distributed']==220 and s['after']['budget_distributed']==231
 assert s['after']['carry']=='0' and s['before']['carry']=='1/2'
 print('R204_R205_EXTENDED_PREVIEWS_PASS; source_bound_TEST_only, no_native')
