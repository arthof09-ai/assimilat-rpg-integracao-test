"""Derives test power diagnostics and DMG export exclusively from R199 committed SQLite,
using R199 cold audit, not sheet nominal projections or native mutator reruns."""
from __future__ import annotations
import collections,csv,json,pathlib,sqlite3,statistics,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];R199=ROOT/'new/r199'
sys.path.insert(0,str(R199/'code'))
import r199_independent_replay as cold
AUD=json.loads((R199/'evidence/R199_INDEPENDENT_AUDIT.json').read_text());assert AUD['status']=='PASS_R199_COLD_SEMANTIC_AUDIT'

names={'ONG_P2':'Ong Mefita (Prata 2)','CAPANGA_P3':'Capanga 1 (Prata 3)','LOBO_P1':'Lobo da Caverna (Prata 1)'}
sources={'ONG_P2':'https://app.notion.com/p/2b6c2b324ede82a2b415019eae21eaf5','CAPANGA_P3':'https://app.notion.com/p/da3c2b324ede82f0824e01dd062b1911','LOBO_P1':'https://app.notion.com/p/be5c2b324ede832e8b7a81c5460571c1'}
rows=[];dmgs=[]
for aud in AUD['records']:
 db=R199/'evidence/db'/aud['db']
 verify=cold.semantic(db)
 assert verify['sha256']==aud['sha256']
 c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:state=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0])
 finally:c.close()
 attacks=[e for e in state['native_events'] if e['action']=='weapon_attack']
 costs=[e for e in state['native_events'] if e['action']=='spell_pa_cost']
 transform_events=[e for e in state['native_events'] if e['action']=='transform_activate']
 exp=[e for e in state['native_events'] if e['action'] in ('transform_expire','transform_end_on_ko')]
 splits=[e for e in state['native_events'] if e['action']=='transform_damage_split']
 by={a:{'attempted':0,'hits':0,'post_rd':0,'hp_removed':0,'gross':0,'overkill':0,'critical_positive':0,'critical_negative':0} for a in state['pair']}
 for e in attacks:
  a=e['from'];o=by[a];o['attempted']+=1;o['hits']+=int(e['hit']);o['post_rd']+=e['net'];o['gross']+=e['raw'];o['hp_removed']+=e['hp_loss_actual'];o['overkill']+=e['overkill'];o['critical_positive']+=int(e['critical']=='POSITIVE');o['critical_negative']+=int(e['critical']=='NEGATIVE')
  dmgs.append({'run_id':aud['db'].removesuffix('.sqlite'),'seed':aud['seed'],'policy':aud['policy'],'native_seq':e['seq'],
    'attacker':a,'attacker_source':sources[a],'defender':e['to'],'defender_source':sources[e['to']],
    'damage_formula_source':(('8d6' if a=='ONG_P2' else '1d6' if a=='LOBO_P1' else '2d10+2d8') + '+' + str(e['normal_damage']-sum(sum(g) for g in e['damage_roll_groups']))),
    'damage_type':e['type'],'hit':e['hit'],'crit':e['critical'],'raw':e['raw'],'rd':e['rd_applied'],
    'post_rd':e['net'],'hp_removed':e['hp_loss_actual'],'overkill':e['overkill'],
    'source_scope':'TEST_CONDITIONAL_NOT_CANON'})
 rec={'id':aud['db'].removesuffix('.sqlite'),'seed':aud['seed'],'policy':aud['policy'],'pair':state['pair'],
    'names':[names[x] for x in state['pair']],'status':aud['fight_status'],'winner':aud['winner'],'rounds':aud['rounds'],
    'hp_final':aud['hp_final'],'pa_final':{x:state['actors'][x]['resource']['pa']for x in state['pair']},
    'damage_by_actor':by,'attempts':len(attacks),'spell_count':len(costs),'spell_PA':sum(x['PA_spent']for x in costs),
    'magic_hp_removed':sum(e['hp_loss_actual'] for e in attacks if e['from']=='ONG_P2' and e['type']=='agua'),
    'form_count':len(transform_events),'form_expire_count':len(exp),
    'transform_temp_hp_prevented_normal_loss':sum(e['temporary_hp_removed'] for e in splits),
    'transform_PA':sum(e['cost']for e in transform_events),'pa_total_spent':sum(x['PA_spent']for x in costs)+sum(x['cost']for x in transform_events),
    'ability_ancestral_applications':aud['beast_power_uses'],'commits':aud['commits'],'events':aud['native_events'],
    'audit':'PASS_R199_COLD_SEMANTIC_AUDIT','source_assumptions':'R199_PREREG_READ_ONLY'}
 rows.append(rec)

by_policy=collections.defaultdict(list)
for r in rows:by_policy[r['policy']].append(r)
summary={}
for pol,z in by_policy.items():
 winner=collections.Counter(x['winner'] or 'CENSORED' for x in z)
 summary[pol]={'runs':len(z),'wins':dict(winner),'observed_win_rate_by_actor':{actor:sum(x['winner']==actor for x in z)/sum(x['status']=='FINISHED' for x in z) for actor in z[0]['pair'] if sum(x['status']=='FINISHED' for x in z)},
   'mean_rounds_completed_only':round(statistics.mean(x['rounds']for x in z if x['status']=='FINISHED'),2),
   'total_magic_casts':sum(x['spell_count']for x in z),'total_spell_PA':sum(x['spell_PA']for x in z),
   'total_transformations':sum(x['form_count']for x in z),'total_transform_PA':sum(x['transform_PA']for x in z),
   'total_pa_spent':sum(x['pa_total_spent']for x in z)}
# Deltas: true RNG seed count, policies not independent.
deltas=[]
for pair in [['CAST_NORMAL','ACTIVATE_FORM_AND_CAST'],['SOURCE_BASE_STAT_ONLY','ANCESTRAL_PLUS2_IF_NOT_INCLUDED']]:
 a,b=pair
 seeds=sorted(set(x['seed']for x in by_policy[a])&set(x['seed']for x in by_policy[b]))
 items=[]
 for seed in seeds:
  r1=next(x for x in by_policy[a]if x['seed']==seed);r2=next(x for x in by_policy[b]if x['seed']==seed)
  items.append({'seed':seed,'baseline':r1['id'],'treatment':r2['id'],'baseline_winner':r1['winner'],'treatment_winner':r2['winner'],
   'baseline_rounds':r1['rounds'],'treatment_rounds':r2['rounds'],
   'rounds_delta_treatment_minus_baseline':r2['rounds']-r1['rounds'],
   'baseline_hp':r1['hp_final'],'treatment_hp':r2['hp_final'],
   'treatment_spell_pa':r2['spell_PA'],'treatment_transform_pa':r2['transform_PA'],
   'independent_observation_unit':'seed_block_not_policy_run'})
 deltas.append({'policies':pair,'paired_seed_blocks':len(seeds),'records':items})
report={'status':'PASS_R199_EXPERIMENTAL_BENCHMARK_FROM_FIGHTS','operation':'OP-VLAB-FUSION-SANDBOX-01','as_of':'2026-10-19',
 'two_distinct_pairs':True,'actual_fights':len(rows),'distinct_seed_blocks':sum(x['paired_seed_blocks']for x in deltas),
 'nominal_stats_not_claimed_as_combat':'CONFIRMED','official_benchmarks':0,'terminal_contracts':0,
 'policy_summaries':summary,'paired_deltas':deltas,'records':rows,
 'limits':['Lobo natural Besta ability +2 may already be in Forca; treat 2 policies not fully separate species',
   'Ong Spirit identity blank and form +54/+63 baseline incomplete; ON/OFF forms conditional',
   'Critical on attack magic R42 LAB interpretation', 'R198 wolf RD15 and Ong RD0 source-scoped',
   'Two transformed fights censored by horizon, never victories', 'No holdout blind to development; all seeds development benchmarks',
   'Closed-loop adaptive tactical AI beyond fixed policies not exercised','No official benchmark credit']}
(R199/'evidence/R199_BENCHMARK_FROM_REAL_FIGHTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
with (R199/'evidence/R199_DMG_HANDOFF_ATTACK_RECEIPTS.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dmgs[0].keys()));w.writeheader();w.writerows(dmgs)
print(json.dumps({'status':report['status'],'fights':len(rows),'pairs':2,'seed_blocks':report['distinct_seed_blocks'],'attacks':len(dmgs),
 'winner_by_policy':{k:v['wins']for k,v in summary.items()},'casts':sum(x['spell_count']for x in rows),'form_activations':sum(x['form_count']for x in rows)}))
