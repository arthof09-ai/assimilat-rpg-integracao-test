"""R122 additive experimental TAP/carry planner; never activates or canonizes spirits."""
from fractions import Fraction
from dataclasses import dataclass,asdict
class Hold(ValueError):pass

def project(actor_level,spirit_cap,bap,*,source_kind='SYNTHETIC_ONLY'):
 if source_kind!='SYNTHETIC_ONLY' or not all(isinstance(x,int) and x>=1 for x in (actor_level,spirit_cap,bap)):raise Hold('INVALID_SOURCE_OR_ORDINAL')
 eff=min(actor_level,spirit_cap);tap=Fraction(bap,2);budget=tap*eff
 return {'actor_level':actor_level,'spirit_cap':spirit_cap,'synthetic_bap':bap,'effective_level':eff,
  'tap_numerator':tap.numerator,'tap_denominator':tap.denominator,
  'budget_unallocated':int(budget),'carry_numerator':(budget-int(budget)).numerator,'carry_denominator':(budget-int(budget)).denominator,
  'activation':'HOLD_BRONZE_PROHIBITED' if actor_level<6 else 'HOLD_SCENE_REST_SPIRIT_SOURCE_T6B_PROOF',
  'spirit_fixture':'SYNTHETIC_MATH_ONLY_NOT_A_CANONICAL_BEAST','distributed_attrs':{},'active':False}

p1=project(1,8,11);p2=project(2,8,11);cap=project(6,4,11)
assert (p1['budget_unallocated'],p1['carry_numerator'],p2['budget_unallocated'],p2['carry_numerator'])==(5,1,11,0)
assert cap['effective_level']==4 and cap['budget_unallocated']==22
assert p1['active'] is False and p2['active'] is False
assert p1['activation']=='HOLD_BRONZE_PROHIBITED'
print('R122 4/4 directed mathematical eligibility assertions PASS')
