#!/usr/bin/env python3
"""R07: exact defensive armor sensitivity, read-only reuse of R06 fixture. MATH_ONLY.
Execute: python3 R07_REPLAY_EXACT.py
"""
from itertools import product
from collections import Counter
from fractions import Fraction as Q
from math import ceil, floor
from pathlib import Path
import json, hashlib
base=Path(__file__).resolve().parent
old=json.loads((base/'R06_RESULTS_FAST.json').read_text(encoding='utf-8'))

def d6(n): return Counter(map(sum,product(range(1,7),repeat=n)))
roll=d6(2)
attacks={
 'patada':{'damage_dice':2,'attack_base':54+6,'body':54,'formula':'2d6+54','source':'301c2b324ede828caccb813d3979267a','type':'impacto físico'},
 'mordida':{'damage_dice':1,'attack_base':54+7,'body':54,'formula':'1d6+54','source':'301c2b324ede828caccb813d3979267a','type':'perfurante físico'},
}

def mean(xs):return sum((Q(v*w) for v,w in xs.items()),Q(0))/sum(xs.values())
def p_hit(attack,ca,delta=0):return Q(sum(w for s,w in roll.items() if s+attack['attack_base']+delta>ca),36)
def damage_dist(attack):return Counter({s+attack['body']:w for s,w in d6(attack['damage_dice']).items()})
def rmode(x,mode):return x if mode=='none' else floor(x) if mode=='floor' else floor(x+Q(1,2)) if mode=='nearest_half_up' else ceil(x)
def reflected_per_hit(attack,phase,rounding,rd_target=25,attacker_rd=0):
 out=Q(0);dist=damage_dist(attack);total=sum(dist.values())
 for gross,w in dist.items():
  net=max(0,gross-rd_target)
  raw=Q(15,100)*(gross if phase=='gross' else net) if net>0 else Q(0)
  rr=rmode(raw,rounding)
  rr_after=max(0,rr-attacker_rd)
  out+=Q(w, total)*rr_after
 return out

def ff(x):return {'fraction':str(x),'decimal':round(float(x),10)}

def calc_shift(d):
 data={}
 for name,a in attacks.items():
  pa=p_hit(a,68,d);pb=p_hit(a,71,d)
  dmg=mean(Counter({g-25:w for g,w in damage_dist(a).items()}))
  assert dmg=={'patada':Q(36),'mordida':Q(65,2)}[name]
  data[name]={'chance_unarmored':ff(pa),'chance_armored':ff(pb),'probability_reduction':ff(pa-pb),'health_before':ff(pa*dmg),'health_after':ff(pb*dmg),'health_avoided':ff((pa-pb)*dmg),'reflection_after_rd_nominal':ff(pb*reflected_per_hit(a,'net','none')),'reflection_from_gross_nominal':ff(pb*reflected_per_hit(a,'gross','none'))}
 return data

sensitivity={str(t):calc_shift(t) for t in range(-8,16)}
# Baseline R06 must reconcile without changing R06 artifact
for x,n in [('Patada','patada'),('Mordida','mordida')]:
 for new,old_key in [('chance_unarmored','p0'),('chance_armored','p1'),('health_before','before'),('health_after','after'),('health_avoided','prevented')]:
  assert sensitivity['0'][n][new]['fraction']==old['scenarios'][x][old_key]['fraction'],(x,new)
old_pa=Q(sensitivity['0']['patada']['chance_unarmored']['fraction']);old_ma=Q(sensitivity['0']['mordida']['chance_unarmored']['fraction'])
new_pa=Q(sensitivity['0']['patada']['chance_armored']['fraction']);new_ma=Q(sensitivity['0']['mordida']['chance_armored']['fraction'])
prob1_before=1-(1-old_pa)*(1-old_ma)
prob1_after=1-(1-new_pa)*(1-new_ma)
assert prob1_before==Q(125,216) and prob1_after==Q(47,432)

res=[]
for t,datum in sensitivity.items():
 v=sum((Q(x['health_avoided']['fraction']) for x in datum.values()),Q(0))
 res.append((v,int(t)))
peak=max(res)
assert peak == (Q(709,24),3)

reflection={}
for basis in ['net','gross']:
 for rounding in ['none','floor','nearest_half_up','ceil']:
  k=basis+'_'+rounding
  totals={}
  for rd in [0,5,7,10,15,35]:
   total=Q(0)
   for a in attacks.values():total+=p_hit(a,71,0)*reflected_per_hit(a,basis,rounding,25,rd)
   totals[str(rd)]=ff(total)
  reflection[k]=totals
assert reflection['net_none']['0']['fraction']=='89/160'
assert Q(reflection['gross_none']['0']['fraction'])==Q(467,480)
for name,values in reflection.items():
 assert Q(values['15']['fraction'])==0, name
assert Q(reflection['net_ceil']['7']['fraction'])==0
assert Q(reflection['gross_ceil']['10']['fraction'])==0

cost=[]
for t in [1,2,3,5,7,8,10]:
 cost.append({'protected_intervals':t,'charge_upkeep_from_activation':20+3*t,'charge_upkeep_from_next_interval':20+3*(t-1),'first_cost_fraction_if_including_first':ff(Q(20,20+3*t)),'expected_hp_prevented_for_identical_R06_pair_each_interval':ff(Q(119,6)*t),'note':'scenario only; an interval is two independent attempts, not a certified combat turn'})

# Alternative attack-test dice when rank conflict: Prata-body 2d6 versus OuroNegro-tree 4d6.
# Damage formulas remain literal sheet values in both alternatives.
rank_test_sensitivity={}
for rank_name,n in [('body_prata_2d6',2),('tree_ouro_negro_4d6',4)]:
 ds=d6(n); den=6**n
 entry={}; hit_list=[]
 for name,a in attacks.items():
  pa=Q(sum(w for s,w in ds.items() if s+a['attack_base']>68),den)
  pb=Q(sum(w for s,w in ds.items() if s+a['attack_base']>71),den)
  harm=Q(36) if name=='patada' else Q(65,2)
  hit_list.append((pa,pb));entry[name]={'p_CA68':ff(pa),'p_CA71':ff(pb),'expected_damage_avoided':ff((pa-pb)*harm),'expected_damage_CA71':ff(pb*harm)}
 rank_test_sensitivity[rank_name]={'by_attack':entry,'total_hp_avoided':ff(sum((Q(e['expected_damage_avoided']['fraction']) for e in entry.values()),Q(0))),'p_at_least_one_hit_CA68':ff(1-(1-hit_list[0][0])*(1-hit_list[1][0])),'p_at_least_one_hit_CA71':ff(1-(1-hit_list[0][1])*(1-hit_list[1][1]))}
assert rank_test_sensitivity['body_prata_2d6']['total_hp_avoided']['fraction']=='119/6'
assert Q(rank_test_sensitivity['tree_ouro_negro_4d6']['total_hp_avoided']['fraction'])==Q(3155,288)

# System-of-Combat critical damage: normal dice+fixed+maximal normal dice value.
# This computes only maxima, without presuming a successful critical or timing.
critical_reflection_bound={}
for name,a in attacks.items():
 max_dice=6*a['damage_dice']
 normal_max=a['body']+max_dice
 crit_max=normal_max+max_dice
 reflect_gross=Q(15,100)*crit_max
 reflect_net=Q(15,100)*max(0,crit_max-25)
 critical_reflection_bound[name]={'normal_max_damage':normal_max,'critical_max_damage':crit_max,'reflection_15pct_max_critical_gross':ff(reflect_gross),'ceiling_gross_reflection_max':ceil(reflect_gross),'ceiling_after_defender_RD25_max':ceil(reflect_net)}
 assert ceil(reflect_gross)<15

# Esquivar uses CA + Reflexo. Below are minimal Reflexo values
# to stop EVERY noncritical attack roll of the named attack, assuming a legal Reaction.
reaction_sensitivity={}
for name,a in attacks.items():
 max_roll=12+a['attack_base']
 reaction_sensitivity[name]={'attack_max_without_critical':max_roll,'minimum_reflexo_at_CA68_to_block_all_noncritical_attempts':max(0,max_roll-68),'minimum_reflexo_at_CA71_to_block_all_noncritical_attempts':max(0,max_roll-71)}
assert reaction_sensitivity['patada']['minimum_reflexo_at_CA71_to_block_all_noncritical_attempts']==1
assert reaction_sensitivity['mordida']['minimum_reflexo_at_CA71_to_block_all_noncritical_attempts']==2

retail={
 'operation':'OP-DMG-CORPUS-EMP-01','round':'R07','classification':'MATH_ONLY','canon_writes':0,
 'sources':{'behemoth':'5dac2b324ede83f39cdb01a904ce3cfd','simio':'301c2b324ede828caccb813d3979267a','combat':'3ebc2b324ede81f1be4be8804ac113c0','besta':'3ebc2b324ede81f4992ac88a3588cacd','magic':'3ebc2b324ede81f7b343f7270ff91373','baseline':'3f2c2b324ede815498cddb7844245f7e'},
 'assumptions':['Two separate attack attempts, hypothetical Símio Luta+6 for Patada and Luta+7 for Mordida','Prata 2d6 versus Behemoth CA68/71, strict greater than and tie favors defense','Damage rolled independently, physical melee, Behemoth normal Ouro RD25, no crit or reactions','Armor is active before tested attempts, no other buffs, no explicit enemy resistance by subtype','Reflections only on positive received damage; raw basis as rival hypothetical alternative','Reflected damage is not intrinsically a magical projectile, no extra invented traits','Attacker RD scenarios only if competence of this mitigation is confirmed','Accuracy shifts are counterfactual and have not been authorized as Símio statistics'],
 'baseline_reused_R06_sha256':hashlib.sha256((base/'R06_RESULTS_FAST.json').read_bytes()).hexdigest(),
 'sensitivity_shared_accuracy_offset':sensitivity,
 'attack_test_rank_conflict_sensitivity':rank_test_sensitivity,
 'critical_reflection_maxima_if_no_other_buffs':critical_reflection_bound,
 'reaction_sensitivity_if_legal_esquivar':reaction_sensitivity,
 'at_least_one_hit_two_independent_attempts':{'without_armor':ff(prob1_before),'with_armor':ff(prob1_after),'absolute_reduction':ff(prob1_before-prob1_after),'relative_reduction':ff((prob1_before-prob1_after)/prob1_before)},
 'peak_armor_health_avoided':{'shared_accuracy_shift':peak[1],'expected_hp_avoided_for_one_each':ff(peak[0])},
 'reflection_R06_accuracy_bases_and_rounding_per_successful_hit':reflection,
 'energetic_sensitivity':cost,
 'normative_findings':['armor +3 CA reflects 15 percent of damage received EXCEPT magic and projectiles, 20PA+3PA per turn','system of magic imposes 1 Standard Action on spells without explicit different time; applicability to specific armor ability is not proven','DMG-RANK v1.1 says return value derives from damage received, no new damage base; no general bypass authorized','combat Esquiva = CA + Reflexo; Defender =6+CON+Armadura+Fortitude; one Reaction in turn; values unavailable','spell reflect reaction for half damage is different from armor passive 15 percent and cannot be imported'],
 'unknown':['official Símio Luta bonuses','Simio rank: title/body Prata5, ancestor OuroNegro5','armor classification as magia or non-spell bestial ability','start timing and upkeep first tick','maintenance action and interruption','whether reflected damage is subject to attacker RD and type/rider','rounding scope and rule','competent reflect source basis gross or net','combat interactions critical/reactions'],
 'falsification_gates':['Without crit/reaction, with shared R06 parameters, CA delta must change probabilities as distribution','If defender with protection takes hits not passing CA71, inspect armor timing or certified mechanics before inferring bug','If a reflected return penetrates a competent attacker RD15 with noncrit gross <=66 and no bypass, inspect rule/rounding/reflection nature; do not presume defect']}
path=base/'R07_RESULTS_EXACT.json';path.write_text(json.dumps(retail,ensure_ascii=False,indent=2),encoding='utf-8')
check=json.loads(path.read_text(encoding='utf-8'))
assert check['peak_armor_health_avoided']==retail['peak_armor_health_avoided']
print(json.dumps({'p_any_before':ff(prob1_before),'p_any_after':ff(prob1_after),'peak':retail['peak_armor_health_avoided'],'rank_alternatives':rank_test_sensitivity,'critical_reflection_bounds':critical_reflection_bound,'reaction_sensitivity':reaction_sensitivity,'sensitivity_selected':{str(i):sensitivity[str(i)] for i in [-5,0,2,3,10]},'reflection':reflection,'cost':cost,'old_sha256':retail['baseline_reused_R06_sha256'],'new_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
print('PASS R07 exact fractions; R06 baseline reconciliation; JSON readback')
