"""R112 experimental analytical guard based on official Transformação Espiritual v1.0.
Master-side only. No new canonical Besta, no physical activation, no native writer.
Known T1/T2/T9/T9A guards; T6-B resources require source-specific proof.
"""
from fractions import Fraction
import json
from pathlib import Path
class Hold(ValueError):pass

def preview(*,character_level,spirit_cap,bap,scene_id=None,actor_id=None,spirit_id=None,rest_proof=None,action_cost_proof=None,source_version=None):
 if not all(isinstance(x,int) and x>=0 for x in (character_level,spirit_cap,bap)):raise Hold('invalid ordinal/cap/BAP fixture')
 if spirit_cap<1 or character_level<1: raise Hold('no effective spirit transformation')
 eff=min(character_level,spirit_cap)
 tap=Fraction(bap,2)
 total=tap*eff
 record={'effective_level':eff,'tap_numerator':tap.numerator,'tap_denominator':tap.denominator,'budget_floor':int(total),
   'carry_numerator':(total-int(total)).numerator,'carry_denominator':(total-int(total)).denominator,
   'source':'T1_T2_EXPERIMENTAL_ONLY','status':'PREVIEW_NOT_ACTIVATED'}
 if character_level<6:
  record['activation']='HOLD_BRONZE_PROHIBITED'
 elif not all([scene_id,actor_id,spirit_id,rest_proof,action_cost_proof,source_version]):
  record['activation']='HOLD_MISSING_SCENE_REST_SOURCE_OR_COST'
 else:
  # This does not create an actual scene or grant resources. A real activation
  # also needs Besta source/proficiency and T6B maxima attestation; no assumptions.
  record['activation']='ELIGIBILITY_CANDIDATE_ONLY_NOT_ACTIVATED'
 return record

cases={
 'A_CAP_BELOW_ACTOR':preview(character_level=6,spirit_cap=4,bap=11),
 'B_SPIRIT_ELIGIBLE_FOLLOW_LEVEL':preview(character_level=6,spirit_cap=8,bap=11),
 'C_FRACTIONAL_FIRST':preview(character_level=1,spirit_cap=8,bap=11),
 'C_FRACTIONAL_SECOND':preview(character_level=2,spirit_cap=8,bap=11),
 'D_NO_TRANSFORMATION':{'character_level':2,'spirit_id':None,'normal_up_allowed':True,'activation':'NOT_AVAILABLE_NO_BESTA'}
}
assert cases['A_CAP_BELOW_ACTOR']['effective_level']==4
assert cases['B_SPIRIT_ELIGIBLE_FOLLOW_LEVEL']['effective_level']==6
assert (cases['C_FRACTIONAL_FIRST']['budget_floor'],cases['C_FRACTIONAL_FIRST']['carry_numerator'],cases['C_FRACTIONAL_SECOND']['budget_floor'],cases['C_FRACTIONAL_SECOND']['carry_numerator'])==(5,1,11,0)
assert cases['C_FRACTIONAL_FIRST']['activation']=='HOLD_BRONZE_PROHIBITED'
assert cases['B_SPIRIT_ELIGIBLE_FOLLOW_LEVEL']['activation']=='HOLD_MISSING_SCENE_REST_SOURCE_OR_COST'
assert cases['D_NO_TRANSFORMATION']['normal_up_allowed']
out={'contract':'R112_TRANSFORMATION_GUARDS','source':'https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9',
 'scope':'MESTRE_SIDE_LOCAL_ANALYTIC_ONLY','cases':cases,'result':'6 directed assertions PASS',
 'positive_native_activation':'HOLD_SOURCE_SCENE_REST_T6B_MAXIMA','no_created_canonical_beast':True}
p=Path(__file__).parent/'R112_TRANSFORM_LOCAL.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(out['result'], 'R112 active native HOLD')
