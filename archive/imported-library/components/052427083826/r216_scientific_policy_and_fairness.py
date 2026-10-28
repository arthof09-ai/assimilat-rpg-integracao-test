"""Source-independent comparison of stored SQLite R216 PRIMARY vs R216B policy arms and identity-preserving label mirrors.
No combat engine imported and no seeds re-executed. Mirrors test label invariance, NOT initiative-order invariance.
"""
from pathlib import Path
import sqlite3,json,hashlib,statistics
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'evidence/db'
def ck(v,m):
 if not v:raise AssertionError(m)
def read(seed,policy,label='TEAM_A'):
 p=DB/f'R216_TEAM_{policy}_{label}_S{seed}.sqlite';ck(p.is_file(),'DB_MISSING_'+p.name)
 con=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
 try:
  st=json.loads(dict(con.execute('select key,value from meta'))['state']);return st
 finally:con.close()
def tapes(s):
 return {
  'physical':[(e.get('by'),e.get('to'),e['attack_attempts'],e['crit'],e['damage_rolls']) for e in s['native_events'] if e.get('action')=='R215_OFFENSIVE_RNG'],
  'spell':[(e['spell_gross'],e['save_rolls'],e['save_total'],e['position_snapshot'],e['chosen_center']) for e in s['native_events'] if e.get('action')=='R216_GEOMETRY_STATE_DECISION'],
  'spell_damage_tapes':[(e['damage_rolls'],e['raw']) for e in s['native_events'] if e.get('action')=='spell'],
  'enemy_choices':[(e['chosen'],e['observed_heals']) for e in s['native_events'] if e.get('action')=='R216_ENEMY_TARGET_DECISION'],
  'target_hp':{k:a['hp'] for k,a in s['actors'].items()},
  'PA':{k:a['pa'] for k,a in s['actors'].items()}
 }
def main():
 primary=json.loads((ROOT/'evidence/reports/R216_EXECUTION_RESULTS.json').read_text())
 famA=[]
 for seed in [21673002,21673003,21673004]:
  a=read(seed,'PROTECTIVE');b=read(seed,'AGGRESSIVE');fa=tapes(a);fb=tapes(b)
  famA.append({'seed':seed,'terminal_delta_V_protect_minus_aggressive':fa['target_hp']['V']-fb['target_hp']['V'],
   'enemy_R_delta':fa['target_hp']['R']-fb['target_hp']['R'],
   'offensive_rolls_identical_all_actions':fa['physical']==fb['physical'] and fa['spell']==fb['spell'] and fa['spell_damage_tapes']==fb['spell_damage_tapes'],
   'phys_tapes_equal':fa['physical']==fb['physical'],'spell_tapes_equal':fa['spell']==fb['spell'],
   'enemy_choices_identical':fa['enemy_choices']==fb['enemy_choices']})
 famB=[]
 for seed in [21674001,21674002,21674004]:
  a=read(seed,'PROTECTIVE');b=read(seed,'AGGRESSIVE');x=tapes(a);y=tapes(b)
  ck(x['physical']==y['physical'],'R216B_PHYSICAL_RNG_NOT_MATCHED');ck(x['spell']==y['spell'] and x['spell_damage_tapes']==y['spell_damage_tapes'],'R216B_SPELL_RNG_NOT_MATCHED')
  ck([t[0] for t in x['enemy_choices']]==[t[0] for t in y['enemy_choices']],'R216B_TARGET_TRAJECTORY_DIVERGED')
  ck(x['target_hp']['R']==y['target_hp']['R'] and x['target_hp']['E']==y['target_hp']['E'],'R216B_NON_TREATED_TERMINAL_DIFF')
  d=x['target_hp']['V']-y['target_hp']['V'];ck(d>=0,'PROTECTIVE_NEGATIVE_OBSERVATION')
  famB.append({'seed':seed,'terminal_protective_V':x['target_hp']['V'],'terminal_aggressive_V':y['target_hp']['V'],
   'terminal_V_difference':d,'E_PA_protective':x['PA']['E'],'E_PA_aggressive':y['PA']['E'],
   'physical_tapes_identical':True,'spell_tapes_identical':True,'enemy_target_order_identical':True,
   'heals_protective':a['r216']['stats']['heals'],'healing_effective_protective':a['r216']['stats']['healed'],
   'protective_healing_PA':a['r216']['stats']['heal_pa'],'aggressive_healing_PA':b['r216']['stats']['heal_pa'],
   'observed_diff_equals_healed':d==a['r216']['stats']['healed']})
 mirrors=[]
 for seed in [21672001,21672002]:
  a=read(seed,'PROTECTIVE','TEAM_A');b=read(seed,'PROTECTIVE','TEAM_B')
  ck(a['actors']==b['actors'] and a['native_events']==b['native_events'] and a['r216']['stats']==b['r216']['stats'],'PRESENTATION_LABEL_DID_AFFECT_SIM')
  mirrors.append({'seed':seed,'identical_native_events':len(a['native_events']),'actors_equal':True,'stats_equal':True,'scope':'TEAM_LABEL_ONLY; DOES_NOT_SWAP_INITIATIVE'})
 ck(len(famA)==3 and len(famB)==3 and len(mirrors)==2,'DENOMINATOR')
 out={'status':'PASS_R216_SCIENCE_CAUSAL_SUBCOHORT_AND_LABEL_FAIRNESS','primary_complete_pairs':3,'primary_blocked_seed':21673001,
  'primary_pairs':[dict(x,interpretation='DESCRIPTIVE_ONLY_STREAMS_MAY_DIVERGE') for x in famA],
  'common_stream_complete_pairs':3,'common_stream_quarantine_seed':21674003,
  'common_stream_pairs':famB,'delta_V_sum':sum(x['terminal_V_difference'] for x in famB),
  'delta_V_mean':statistics.mean(x['terminal_V_difference'] for x in famB),
  'delta_V_range':[min(x['terminal_V_difference'] for x in famB),max(x['terminal_V_difference'] for x in famB)],
  'effective_heal_total':sum(x['healing_effective_protective'] for x in famB),
  'healing_PA_total':sum(x['protective_healing_PA'] for x in famB),
  'team_presentation_label_mirrors':mirrors,'mirror_independent_seeds':2,'mirror_arms':4,
  'formal_conclusion':'3 paired TEST seeds with action-matched offensive RNG support fixture-scoped controlled comparison. No victory inferred from 4-round censures; not universal, not canonical.',
  'official_benchmark_cells':0,'terminal_contracts':0}
 (ROOT/'evidence/reports/R216_SCIENCE_AND_FAIRNESS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));return out
if __name__=='__main__':
 v=main();print(json.dumps({k:v[k] for k in ['status','primary_complete_pairs','common_stream_complete_pairs','delta_V_sum','delta_V_mean','delta_V_range','effective_heal_total','healing_PA_total','mirror_independent_seeds']},indent=2))
