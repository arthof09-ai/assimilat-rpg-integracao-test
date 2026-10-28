#!/usr/bin/env python3
"""Report observed native receipts, never calculate combat damage; statistics only."""
import sys,json,math,hashlib,statistics,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'work'/'fusion_stage12'))
import vlab_r27_scientific_baseline as v
import vlab_r27_rank_math as ranks
BASE=Path(__file__).parent
ROOT=BASE/'scientific_runs'/'receipts'
OUT=BASE/'scientific_report'
OUT.mkdir(exist_ok=True)

def wilson(k,n,z=1.959963984540054):
 if n==0:return None
 p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den
 h=z/den*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
 return [round(max(0,center-h),5),round(min(1,center+h),5)]

def record(a,b,seed):
 p=ROOT/f'{a}__{b}__SEED_{seed}.json'
 if not p.exists():return None
 obj=json.loads(p.read_text())
 if obj['schema']!='R27_SCIENCE_RUN':raise ValueError('wrong schema '+p.name)
 return obj

def aggreg():
 cells=[];status_count=collections.Counter();runs=[];missing=[]
 for left in v.PROFILES:
  for right in v.PROFILES:
   obs=[]
   for seed in v.SEEDS:
    item=record(left,right,seed)
    if item is None:missing.append([left,right,seed]);continue
    obs.append(item);runs.append(item);status_count[item['status']]+=1
   done=[x for x in obs if x['status'].startswith('COMPLETE')]
   win1=sum(x['winner']=='LAB_PERSONALIZADO_1' for x in done)
   win2=sum(x['winner']=='LAB_PERSONALIZADO_2' for x in done)
   s=collections.Counter(x['status'] for x in obs)
   summary={'cell':left+'__'+right,'left':left,'right':right,'planned':20,
     'observed':len(obs),'complete':len(done),'censored':len(obs)-len(done),
     'left_wins':win1,'right_wins':win2,
     'left_win_fraction_all_attempts':win1/len(obs) if obs else None,
     'left_win_Wilson95_all_attempts':wilson(win1,len(obs)),
     'right_win_fraction_all_attempts':win2/len(obs) if obs else None,
     'censor_fraction_all_attempts':(len(obs)-len(done))/len(obs) if obs else None,
     'completion_fraction':len(done)/len(obs) if obs else None,
     'mean_rounds_completed':statistics.mean(x['summary']['rounds'] for x in done) if done else None,
     'mean_attacks_per_attempt':statistics.mean(x['summary']['attacks'] for x in obs) if obs else None,
     'total_attacks_native':sum(x['summary']['attacks'] for x in obs),
     'total_hits_native':sum(x['summary']['hits'] for x in obs),
     'hit_fraction_of_native_attacks':sum(x['summary']['hits'] for x in obs)/max(1,sum(x['summary']['attacks'] for x in obs)),
     'total_raw_damage_observed':sum(x['summary']['raw_damage'] for x in obs),
     'total_effective_net':sum(x['summary']['net_damage'] for x in obs),
     'total_real_HP_loss':sum(x['summary']['hp_removed'] for x in obs),
     'total_overkill':sum(x['summary']['overkill'] for x in obs),
     'positive_criticals':sum(x['summary']['critical_positive'] for x in obs),
     'negative_criticals':sum(x['summary']['critical_failure'] for x in obs),
     'censor_breakdown':dict(s),'exact_basic_hit_probabilities':v.exact_hit_grid()[left+'__'+right],
     'all_seeds':list(v.SEEDS),'insufficient_for_unconditional_win_probability':bool(len(obs)-len(done))}
   cells.append(summary)
 totals={
  'planned_attempts':v.PRE_REG_ATTEMPTS,'observed_attempts':len(runs),'missing':missing,
  'complete':sum(x['status'].startswith('COMPLETE') for x in runs),
  'censored':sum(not x['status'].startswith('COMPLETE') for x in runs),
  'censor_types':dict(status_count),
  'total_attacks':sum(x['summary']['attacks'] for x in runs),
  'total_hits':sum(x['summary']['hits'] for x in runs),
  'sum_raw_damage_observed':sum(x['summary']['raw_damage'] for x in runs),
  'sum_net_damage':sum(x['summary']['net_damage'] for x in runs),
  'sum_rd_mitigation_actual':sum(x['summary']['raw_damage']-x['summary']['net_damage'] for x in runs),
  'sum_overkill':sum(x['summary']['overkill'] for x in runs),
  'sum_hp_removed':sum(x['summary']['hp_removed'] for x in runs),
  'crit_positive':sum(x['summary']['critical_positive'] for x in runs),
  'crit_negative':sum(x['summary']['critical_failure'] for x in runs),
  'A1_control_events':sum(x['a1_events'] for x in runs),
  'full_canonic_entities':0,'canonic_fights':0,'canonic_1875_credited':0,
  'eligible_conditional_profile_pairs':16,
  'genesis_no_hit_preflight_rejections':sum(x['status']=='CENSORED_PROVABLE_NO_HIT_POTENTIAL' for x in runs),
 }
 # Unique unordered profile pairs have mirrored (left,right) lab fixtures.
 paired=[]
 P=list(v.PROFILES)
 for i,a in enumerate(P):
  for b in P[i+1:]:
   ab=next(x for x in cells if x['left']==a and x['right']==b)
   ba=next(x for x in cells if x['left']==b and x['right']==a)
   paired.append({'unordered_pair':[a,b],
     'A_as_left_wins':ab['left_wins'],'A_as_right_wins':ba['right_wins'],
     'both_directions_n':ab['observed']+ba['observed'],
     'all_conditional_cases_complete':ab['complete']+ba['complete'],
     'censored':ab['censored']+ba['censored'],
     'potential_side_difference_for_A':ab['left_wins']-ba['right_wins'],
     'not_independent_due_seed_pairing':True})
 original=[]
 for seed in v.r25.DEFAULT_SEEDS:
  p=ROOT/f'ORIGINAL_R26__SEED_{seed}.json'
  if p.exists():original.append(json.loads(p.read_text()))
 out={'schema':'R27_SCIENTIFIC_BASELINE_RESULTS_V1','classification':'EXPERIMENTAL_CONDITIONAL_NONCANONICAL',
  'engine':'Historical A1 + v0.7 + v0.8.1 + R18 SQLite via R25/R26 adapters',
  'critical_failure_lab_policy':v.CRIT_FAIL_POLICY,
  'universe':{'profiles':list(v.PROFILES),'ordered_cells':16,'planned_seeds_per_cell':20,
              'planned_total':320,'rank_star':'Bronze1 normal virtual beasts','attributes_per_beast':43,
              'luta_training_allocation_conditional':6,'RD':5,'base_damage':'3d6',
              'no_voluntary_defensive_reaction':True},
  'total':totals,'cells':cells,'side_inverse_comparisons':paired,
  'original_8_seed_comparison':{'seeds':list(v.r25.DEFAULT_SEEDS),
    'r25_completed':5,'r26_completed':7,
    'r27_completed':sum(x['status'].startswith('COMPLETE') for x in original),
    'r27_critical_failures':sum(x['summary']['critical_failure'] for x in original),
    'r27_attacks':sum(x['summary']['attacks'] for x in original),
    'runs':[{'seed':x['seed'],'status':x['status'],'round':x['round_reached'],'winner':x['winner'],
             'attacks':x['summary']['attacks'],'critical_fail':x['summary']['critical_failure'],
             'sqlite_sha256':x['sqlite_sha256']} for x in original]},
  'rank_boundary_combinatorial_diagnostics':ranks.run(),
  'sources':{'Sistema de Combate':'3ebc2b32-4ede-81f1-be4b-e8804ac113c0',
   'Criação de Besta':'3ebc2b32-4ede-81f4-992a-c88a3588cacd','Plano VLAB':'3f3c2b32-4ede-81d4-80db-f11732734463'},
  'warnings':['All custom profile allocation are laboratory choices, NOT original creature sheets',
              'Luta proficiency +6 assigned experimentally, source does not prove actor training',
              'PA cost zero for generic attack from historical test gate, not authoritative named action',
              'Damage type impacto is transport placeholder. Typed special interactions untested.',
              'HP0 lab stop is NOT death adjudication','No defender policy tested in matrix; reaction refresh known but unused',
              'Wilson 95% on winner-count over ALL attempts reports censor and is NOT uncensored combat win probability',
              'Rank mathematics does not represent 25 finished actor builds or cross-rank combats',
              'Uncertain legacy pilot intents retain HOLD; not replayed'],
  'canonical_fight_cells':0}
 (OUT/'R27_SCIENTIFIC_RESULTS_MASTER_ONLY.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
 print(json.dumps({'totals':totals,'seed8':out['original_8_seed_comparison']['r27_completed'],
  'cells':[{'x':c['cell'],'complete':c['complete'],'cens':c['censored'],'w':c['left_wins'],'hits':c['total_hits_native']} for c in cells]},ensure_ascii=False,indent=2))
 return out
if __name__=='__main__':aggreg()
