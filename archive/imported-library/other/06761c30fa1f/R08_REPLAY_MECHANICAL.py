#!/usr/bin/env python3
"""DMG R08: independently enumerated d6 outcomes, no VLAB execution and no Notion writes.
Reads R07 only for baseline identity/hash; R34–R37 facts are reports in official
OP-VLAB-FUSION-SANDBOX-01, not independently re-executed SQLite by DMG.
"""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent
N=0
def verify(condition,msg):
 global N
 N+=1
 if not condition: raise AssertionError(msg)
def frac(q):return {'fraction':str(q),'decimal':round(float(q),10)}
def die_outcomes(n):return [sum(t) for t in product(range(1,7), repeat=n)]

def calc(attack_for, luta, ca, dmg_for, rd, attack_n=1, damage_n=1):
 attacks=die_outcomes(attack_n);dmg=die_outcomes(damage_n)
 scores=[a+attack_for+luta for a in attacks]
 hits=[v>ca for v in scores]
 net=[max(0,v+dmg_for-rd) for v in dmg]
 return {'attack_score_range':[min(scores),max(scores)],'p_hit':F(sum(hits),len(hits)),'damage_on_hit':F(sum(net),len(net)),'expected_damage_per_attempt':F(sum(hits),len(hits))*F(sum(net),len(net)),'hit_rolls':[a for a in attacks if a+attack_for+luta>ca]}
frig=calc(18,6,20,18,5)
goat=calc(13,6,31,13,5)
goat_vs_goat=calc(13,6,20,13,5)
goat_evaded=calc(13,6,26,13,5)
frig_vs_goat_evasion=calc(18,6,26,18,5)
verify(frig['p_hit']==1,'frig normal basic to goat')
verify(frig['damage_on_hit']==F(33,2),'frig RD5')
verify(goat['p_hit']==0,'goat cannot basic hit CA31')
verify(goat_vs_goat['p_hit']==F(5,6),'goat CA20')
verify(goat_evaded['p_hit']==0,'goat Esquiva26 blocks all ordinary Investida results')
verify(frig_vs_goat_evasion['p_hit']==F(2,3),'frig vs Goat evasion hypothetical extended scope')
# 2 hits kill 38 HP only with two max-damage rolls, assuming adjacent, no reactions, no crit.
frigdmg=[d+18-5 for d in range(1,7)]
prob_two=F(sum((x+y>=38) for x,y in product(frigdmg,repeat=2)),36)
verify(prob_two==F(1,36),'two-action kill')
verify(min(frigdmg)*3>=38,'third successful action always kills')
expected_actions=2*prob_two+3*(1-prob_two)
verify(expected_actions==F(107,36),'expected actions')
# Armor CA marginal under actual two authorized Bronze source attacks (against CA68/71), ignoring crit.
for attribute in [18,13]:
 score=[n+attribute+6 for n in range(1,7)]
 verify(all(s<=68 and s<=71 for s in score),'bronze authorized attack cannot reach Behemoth')
# Titanic Prata vs Titanic Ouro Negro alternatives, reflection upper bound.
body_attack_max={'patada':54+12,'mordida':54+6}
crit_max={'patada':54+12+12,'mordida':54+6+6}
for name in ['patada','mordida']:
 for defender_rd in [30,60]:
  for basis in ['gross_critical','net_after_25']:
   raw=crit_max[name] if basis=='gross_critical' else max(0,crit_max[name]-25)
   reflected=F(15,100)*raw
   ceil=(reflected.numerator+reflected.denominator-1)//reflected.denominator
   verify(ceil<defender_rd,f'{name} upper reflect at RD{defender_rd} {basis}')
# Behemoth CA published supports baseline w/o armoring but rounding is unknown; Simio Titan CA exactly matches 67.
verify(F(10+52)+F(32,5)==F(342,5),'Behemoth theoretical 68.4')
verify(20+40+F(35,5)==67,'Simio titan CA exact')
# Observed VLAB R34 fight from Notion operational record; no independent SQLite verification.
r34=[{'actor':'Frigido','score':26,'net_damage':17,'hp_goat_after':21},
 {'actor':'Cabra','score':23,'net_damage':0,'hp_goat_after':21},
 {'actor':'Frigido','score':30,'net_damage':19,'hp_goat_after':2},
 {'actor':'Cabra','score':21,'net_damage':0,'hp_goat_after':2},
 {'actor':'Frigido','score':28,'net_damage':17,'hp_goat_after':0}]
for e in r34:
 if e['actor']=='Frigido':
  verify(25<=e['score']<=30,'Frigido score observed under source rules')
  verify(14<=e['net_damage']<=19,'Frigido net observed under source rules')
 else:
  verify(20<=e['score']<=25,'Cabra score observed under source rules')
  verify(e['net_damage']==0,'Cabra miss observed')
verify(sum(e['net_damage'] for e in r34)==53,'total native reported net')
verify(sum(1 for e in r34 if e['actor']=='Cabra')==2,'cabras two attempts')
report={
 'operation':'OP-DMG-CORPUS-EMP-01','round':'R08','classification':'MATH_ONLY with documented prior VLAB-native controls','canon_writes':0,
 'R07_baseline_file_sha256':hashlib.sha256((base/'R07_RESULTS_EXACT.json').read_bytes()).hexdigest(),
 'sources':{'simio':'301c2b324ede828caccb813d3979267a','behemoth':'5dac2b324ede83f39cdb01a904ce3cfd','frigido':'f0dc2b324ede820ab9470168d4a53315','cabra':'391c2b324ede8252b0cc810423cdbfa6','combat':'3ebc2b324ede81f1be4be8804ac113c0','besta':'3ebc2b324ede81f4992ac88a3588cacd','magic':'3ebc2b324ede81f7b343f7270ff91373','dmg':'3f2c2b324ede815498cddb7844245f7e','VLAB_authority':'3f3c2b324ede819496ddd7f93bd7e5d2'},
 'simio':{'printed':'Prata 5 (titã), body Prata5 (2d6), tree Ouro Negro5','identity':'macaco rei versus Símio Demoníaco','published_FOR':54,'Force_Titanica':'+2 FOR inclusion/activation unresolved','Luta_attacks':None,'CA_published':67,'CA_titan_formula':67,'Prata_titan_RD':30,'OuroNegro_titan_RD':60,'status':'BLOCKED_NORMATIVE for native encounter with Behemoth'},
 'behemoth':{'CA_published':68,'CA_formula_unrounded':'68.4','armor_CA_if_additional':71,'state_CA_armor_included':None,'RD_Ouro_normal':25,'HP':682,'Alma_published':660,'armor_cost_initial_PA':20,'armor_upkeep_PA_each_turn':3,'armor_pct_reflect':15,'projectiles_magics_reflection_excluded':True,'reflect_on_damage_received_authority':True,'reflect_to_attacker_RD_rule':None,'armor_spell_classification':None,'activation_action':None,'lifetime':None},
 'source_authorized_attack_math':{},
 'native_documented_VLAB_R34':{'seed':347,'reported_native_attacks':r34,'reported_full_fight':True,'reported_rounds':3,'winner':'Frigido','HP_Frigido_end':125,'HP_Cabra_end':0,'total_raw_net_Rabada':53,'Cabra_actual_HP_removed':38,'overkill':15,'DMG_independently_verified_SQLite':False},
 'native_documented_VLAB_R36_R37':{'R36_pairs':4,'reactions':8,'blocked_would_be_hits':7,'wasted_reaction_on_existing_miss':1,'R36_winner_changes':0,'R37_continuous_evasion_censored_trials':2,'R37_censor_rounds_each':8,'R37_HP_unchanged':True,'scope_warning':'Cabra Esquiva26 authorized in specific R36 tests; extension to Frigido pairing requires explicit admission'},
 'new_math':{'p_kill_by_two_Rabadas':frac(prob_two),'p_need_three_Rabadas':frac(1-prob_two),'expected_Rabada_actions_to_defeat_Cabra':frac(expected_actions),'Behemoth_armor_plus3_CA_effect_against_authorized_Bronze_basic_attacks':'zero when no crit/reaction/special bypass: both attack maxima <=30 far below CA68', 'Simio_critical_reflected_15pct_ceiling_upperbound_raw':[12,10],'Titan_prata_or_ouro_negro_RD_if_competent_applied_to_reflect':'zero'},
 'tests_passed':N,'notes':['No new VLAB battle executed','No universal crit effect handled in the basic-hit calculation','Only authorized +6 for Frigido Rabada and Cabra Investida','Besta rank conflicts in tree preserved, R34 individual master rulings authorize their Bronze experimental snapshots','No projection of goat Evasion R36 to Frigido pairing without VLAB admission','No PA as HP proxy']
}
for name,obj in [('Rabada Frigido versus Cabra',frig),('Investida Cabra versus Frigido',goat),('Investida Cabra versus Cabra no reaction',goat_vs_goat),('Investida Cabra versus Cabra Esquiva26',goat_evaded),('Rabada Frigido versus Cabra Esquiva26 hypothetical extension',frig_vs_goat_evasion)]:
 report['source_authorized_attack_math'][name]={k:frac(v) if isinstance(v,F) else v for k,v in obj.items()}
p=base/'R08_RESULTS_MECHANICAL.json'
p.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
# readback
z=json.loads(p.read_text(encoding='utf-8'))
assert z['tests_passed']==N
print('R08_PASS',N,'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
print('R34_PREDICTION',{'frig_hit':str(frig['p_hit']),'frig_expected':str(frig['expected_damage_per_attempt']),'goat_hit':str(goat['p_hit']),'p2actions':str(prob_two),'actions_mean':str(expected_actions)})
