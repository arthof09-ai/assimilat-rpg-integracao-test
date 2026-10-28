"""Independent COMBINATORIAL diagnostics (not a combat resolver). Canonical rule tables, symbolic caveats."""
from __future__ import annotations
from fractions import Fraction
from math import prod
RANKS=[('BRONZE',1,5,1,6,3,6,5,10,6,0),('PRATA',6,10,2,6,6,6,15,20,8,0),('OURO',11,15,3,6,9,6,25,30,10,0),('OURO_NEGRO',16,20,4,6,12,6,35,40,12,0),('LENDARIO_TITA',21,25,6,6,20,10,75,100,22,1)]

def distribution(n,sides):
 dp=[1]
 for _ in range(n):
  out=[0]*(len(dp)+sides)
  for val,m in enumerate(dp):
   for face in range(1,sides+1):out[val+face]+=m
  dp=out
 return dp

def row(rank):
 name,lo,hi,n_hit,sides_hit,n_dmg,sides_dmg,rd,basehp,prof,titan=rank
 dp=distribution(n_dmg,sides_dmg);tot=sides_dmg**n_dmg
 avg=Fraction(sum(v*c for v,c in enumerate(dp)),tot)
 effective=Fraction(sum(max(0,v-rd)*c for v,c in enumerate(dp)),tot)
 neg=Fraction(sum(c for v,c in enumerate(dp) if v<=rd),tot)
 return {'rank':name,'positions':list(range(lo,hi+1)),'test_pool':f'{n_hit}d{sides_hit}',
   'damage_pool':f'{n_dmg}d{sides_dmg}','normal_or_titan':'TITAN' if titan else 'NORMAL',
   'rd':rd,'general_proficiency':prof,'hp_base':60 if titan else 30,'hp_per_level_rank_component':basehp,
   'source':'Criacao_de_Besta_vigente + Sistema_de_Combate','expected_intrinsic_raw_exact_fraction':str(avg),
   'expected_intrinsic_raw':float(avg),'expected_after_matching_general_rd_exact_fraction':str(effective),
   'expected_after_rd':float(effective),'probability_raw_not_exceed_RD':float(neg),
   'not_attack_probability':True,'not_combat_result':True,'no_attributes_or_armors_assumed':True}

def run():
 rows=[row(x) for x in RANKS]
 transitions=[]
 for cur,nxt in zip(RANKS,RANKS[1:]):
  # Constant CON hypothetical across boundary, no special traits (invalid for Lendario actual bonus accumulation).
  # Numerators are only symbolic coefficients to show discontinuities of the source formulas.
  c_lo,c_hi=cur[1:3];n_lo=nxt[1]
  oldconstant=(60 if cur[-1] else 30)+c_hi*cur[8]
  newconstant=(60 if nxt[-1] else 30)+n_lo*nxt[8]
  transitions.append({'from':cur[0]+'5','to':nxt[0]+'1',
      'fixed_CON_natural_hp_jump_symbolic':f'{newconstant-oldconstant} + CON',
      'only_fixed_CON_no_special_traits_assumption':True,
      'lendar_transition_not_legitimate_full_build_without_retroactive_traits':bool(nxt[-1])})
 return {'schema':'R27_RANK_BOUNDARY_MATH_ONLY','rank_groups_analyzed':len(rows),'rank_star_index_positions':25,
   'complete_actor_builds_above_Bronze1':0,'full_combat_other_ranks':0,'tables':rows,
   'transitions':transitions,'not_25_verified_builds':True,
   'conditions':'Same rank attack vs equal rank general RD; no hit chance, attribute, counteraction or equipment assumed.'}
if __name__=='__main__':
 import json
 print(json.dumps(run(),indent=2,ensure_ascii=False))
