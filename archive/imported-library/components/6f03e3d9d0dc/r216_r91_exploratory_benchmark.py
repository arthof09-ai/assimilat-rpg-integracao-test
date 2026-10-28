"""READ-ONLY R91 position-C20 TEST exploratory subset, no canonical matrix mutation."""
import csv,json,sqlite3,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'evidence/db';OUT=ROOT/'evidence/reports'
def state_events(seed,policy):
 f=DB/f'R216_TEAM_{policy}_TEAM_A_S{seed}.sqlite'
 with sqlite3.connect(f'file:{f}?mode=ro',uri=True) as c:
  m=dict(c.execute('SELECT key,value FROM meta'));st=json.loads(m['state']);assert int(m['revision'])==12
  return st,f.name

def execute():
 original=list(csv.DictReader((ROOT/'sources/R82_CORRECTED_BENCHMARK_SCHEMA_PRIMARY_104.csv').open()))
 assert len(original)==104
 row=[r for r in original if r['battery']=='C_BALANCED_TEAM_25' and r['power_position']=='20']
 assert len(row)==1 and row[0]['rank']=='Ouro Negro' and row[0]['star']=='5' and row[0]['reference_homologated']=='0'
 out=[]
 for seed in [21674001,21674002,21674004]:
  for policy in ['PROTECTIVE','AGGRESSIVE']:
   st,f=state_events(seed,policy);ev=st['native_events'];s=st['r216']['stats'];att=[e for e in ev if e['action']=='weapon_attack']
   spell=[e for e in ev if e['action']=='spell'];reactions=[e for e in ev if e['action']=='R215_POST_RD_GUARD']
   heals=[e for e in ev if e['action'] in ('PULSO_ESTABILIZACAO','RECONSTITUICAO_SEIVA')]
   r={'battery':'C_BALANCED_TEAM_25','position':'20','rank':'Ouro Negro','star':'5','cohort_id':'R216_TEST_VAROK_ERISTAN_VS_ARVETH',
      'canonical_source_gate':'SOURCE_MISSING; PROPOSED_NPCS_ONLY','official_homologated':0,
      'seed':seed,'policy':policy,'run_id':f,'outcome':st['phase'],'rounds':4,'turns':st['turn'],
      'V_final_hp':st['actors']['V']['hp'],'R_final_hp':st['actors']['R']['hp'],'E_final_hp':st['actors']['E']['hp'],
      'V_initial_hp':734,'R_initial_hp':806,'E_initial_hp':630,
      'R_HP_removed':806-st['actors']['R']['hp'],'V_terminal_HP_missing':734-st['actors']['V']['hp'],
      'E_terminal_HP_missing':630-st['actors']['E']['hp'],
      'physical_attack_count':len(att),'physical_hits':sum(e['hit'] for e in att),'physical_HP_loss_total':sum(e['hp_loss_actual'] for e in att),
      'spell_cast_count':len(spell),'spell_effective_hp_loss':sum(e['hp_before']-e['hp_after'] for e in spell),
      'guard_reactions':len(reactions),'guard_PA_spent':sum(e['PA_spent'] for e in reactions),
      'guard_damage_prevented':sum(e['reduction'] for e in reactions),
      'heals_count':len(heals),'heal_effective':sum(e.get('actual_heal',e.get('actual_healed',0)) for e in heals),
      'heal_gross':sum(e['gross_heal'] for e in heals),
      'heal_PA_spent':sum(e['PA_spent'] for e in heals),
      'spell_PA_spent':sum(e['PA_spent'] for e in spell),
      'E_terminal_PA':st['actors']['E']['pa'],'V_terminal_PA':st['actors']['V']['pa'],'R_terminal_PA':st['actors']['R']['pa'],
      'movement_events':sum(e['action']=='move' for e in ev),'aoo_events':sum(e['action']=='weapon_attack' and e['attack_origin']=='OPPORTUNITY' for e in ev),
      'censored_not_win':st['phase']=='CENSORED_HORIZON', 'source_geometry':'DECLARED_TEST_ADJACENCY_NOT_CANONICAL_METRIC',
      'magical_RD':'TEST_ZERO_UNVERIFIED_CANONICAL','init_contract':'R215 TEST order V-R-E, unverified representative initiative'}
   out.append(r)
 f=OUT/'R216_R91_C20_EXPLORATORY_READONLY.csv'
 with f.open('w',newline='') as fh:
  w=csv.DictWriter(fh,out[0].keys());w.writeheader();w.writerows(out)
 pairs=[]
 for seed in [21674001,21674002,21674004]:
  a,b=[next(x for x in out if x['seed']==seed and x['policy']==pol) for pol in ['PROTECTIVE','AGGRESSIVE']]
  pairs.append({'seed':seed,'HP_delta_V':a['V_final_hp']-b['V_final_hp'],'support_heal_effective':a['heal_effective'],
    'PA_support_delta':a['heal_PA_spent']-b['heal_PA_spent'],'opponent_HP_equal':a['R_final_hp']==b['R_final_hp'],
    'E_HP_equal':a['E_final_hp']==b['E_final_hp']})
 report={'scope':'R91 C20 candidate experimental evaluation; NOT official cell registration',
  'R82_schema_sha256':hashlib.sha256((ROOT/'sources/R82_CORRECTED_BENCHMARK_SCHEMA_PRIMARY_104.csv').read_bytes()).hexdigest(),
  'R82_rows':104,'selected_baseline':row[0],'source_pages':{'V':'https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091',
    'R':'https://app.notion.com/p/3f6c2b324ede8105891fc647242e61ca','E':'https://app.notion.com/p/3f6c2b324ede819cae98ec0f6a63de76'},
  'comparators':['Varok+Eristan proposed TEST vs Arveth proposed TEST'],
  'independent_seeds':3,'paired_policy_arms':6,'fights_censored':6,'KO':0,
  'paired_outcomes':pairs,'V_HP_preserved_aggregate':sum(x['HP_delta_V'] for x in pairs),
  'incremental_PA_for_support':sum(x['PA_support_delta'] for x in pairs),
  'overclaim_prevention':'No global potency estimate, no win from censures, no homologated C20 or other R91 row, source NPCs proposed, world geometry/initiative not representative.',
  'official_terminal_contracts':0,'official_cells':0,'next_R91_gate':'approved source archetypes/teams, representative initiative, legitimate enemy roster and position/gear, holdout across multiple classes/ranks'}
 (OUT/'R216_R91_C20_RESEARCH_NOTE.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
 print(json.dumps({k:v for k,v in report.items() if k in ['R82_rows','independent_seeds','paired_policy_arms','V_HP_preserved_aggregate','incremental_PA_for_support','official_cells']},indent=2))
if __name__=='__main__':execute()
