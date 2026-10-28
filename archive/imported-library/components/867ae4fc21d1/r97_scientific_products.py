"""Read-only scientific export of admitted R95/R93 cold-PASS experimental subsets."""
from pathlib import Path
import json,hashlib,csv,sqlite3,collections,statistics
R=Path(__file__).resolve().parent
BASE=R.parent/'r91_extracted'/'r82_r91'
A=json.loads((R/'R95_COLD_FIXED_OPENING.json').read_text());T=json.loads((R/'R93_COLD_TEAM_AUDIT.json').read_text());rf=json.loads((R/'R95_SOURCE_FREEZE.json').read_text());tf=json.loads((R/'R93_TEAM_FREEZE.json').read_text())
assert A['all_pass'] and T['all_pass'] and len(A['runs'])==16 and len(T['runs'])==8

def csv_write(name,records,columns):
 with (R/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader();w.writerows(records)

runs=[];attacks=[]
for cohort,d in [('R95_BASIC_FIXED_OPENING',A),('R93_TEAM_2X1_BASIC',T)]:
 for rec in d['runs']:
  if cohort.startswith('R95'):
   matchup=next(m for m in rf['matchups'] if m['id']==rec['matchup_id']);path=R/'r95_runs'/matchup['id']/f"R95BENCH_{rec['seed']}_{rec['side']}.sqlite"
   sf={a:rf['profiles'][matchup[a]]['source'] for a in ('B','E')}
   first=matchup['opening'];beast=rf['profiles'][matchup['B']]['name'];ed=rf['profiles'][matchup['E']]['name']
   row={'run_id':rec['id'],'cohort':cohort,'matchup':rec['matchup_id'],'seed':rec['seed'],'seed_group':rec['group'],'side':rec['side'],'species':beast,'ed':ed,'opening':first,'phase':rec['phase'],'winner':rec['winner'],'events':rec['events'],'attacks':rec['attacks'],'hits':rec['hits'],'hp_B':rec['hp_final']['B'],'hp_E':rec['hp_final']['E'],'turn_limit':60,'initiative_method':'EXOGENOUS_FIXED','source_gate':'ADMISSIBLE_SELECTED_BASIC_FIXED_OPENING','audit':'SEMANTIC_COLD_PASS','independent_group':f"{matchup['B']}|{rec['seed']}"}
  else:
   path=R/'team_runs'/f"R93TEAM_{rec['seed']}_{rec['side']}.sqlite"
   sf={a:tf['profiles'][a]['source'] for a in ('F','V','R')}
   first='ROLLED';beast=tf['profiles']['F']['name'];ed=tf['profiles']['V']['name']+' + '+tf['profiles']['R']['name']
   row={'run_id':rec['run_id'],'cohort':cohort,'matchup':'R93-2X1-TEAM','seed':rec['seed'],'seed_group':rec['cohort'],'side':rec['side'],'species':beast,'ed':ed,'opening':first,'phase':rec['phase'],'winner':rec['winner'],'events':rec['events'],'attacks':rec['attacks'],'hits':rec['hits'],'hp_B':rec['hp_final']['F'],'hp_E':rec['hp_final']['V'],'hp_R':rec['hp_final']['R'],'turn_limit':120,'initiative_method':'ROLLED_BEAST_INIT_TRAINING_UNPROVEN','source_gate':'CONDITIONAL_TEAM_BASIC_ONLY','audit':'SEMANTIC_COLD_PASS','independent_group':f"R93-TEAM|{rec['seed']}"}
  runs.append(row)
  with sqlite3.connect(path) as con:
   assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
   events=[json.loads(x[0]) for x in con.execute('SELECT row_json FROM events ORDER BY seq')]
  for ev in events:
   if ev['kind']=='NORMAL_ATTACK':
    x=ev['detail']['attack'];raw=x['damage_raw'];net=x['damage_net_potential'];actual=x['hp_loss_actual'];atk_src=x['source']; groups=x['damage_groups'];bonus=x['damage_fixed_bonus']
   elif ev['kind']=='TEAM_TURN':
    x=ev['detail']['exchange']['normal'];raw=x['damage_raw'];net=x['damage_net'];actual=x['hp_before']-x['hp_after'];atk_src=sf[x['actor']];pr=tf['profiles'][x['actor']];groups=[pr['damage_dice']];bonus=pr['damage_bonus']
   else:continue
   attacks.append({'run_id':row['run_id'],'cohort':cohort,'matchup':row['matchup'],'seed':row['seed'],'group':row['seed_group'],'side':row['side'],'event_seq':ev['seq'],'actor':x['actor'],'target':x['target'],'actor_source':atk_src,'rank':(rf['profiles'][matchup[x['actor']]]['rank'] if cohort.startswith('R95') else tf['profiles'][x['actor']]['rank']),'dice':json.dumps(groups),'fixed_bonus':bonus,'roll_tape':json.dumps(x['tape'],ensure_ascii=False,separators=(',',':')),'score':x['score'],'ca':x['ca'],'hit':int(x['hit']),'crit_plus':int(x['crit_plus']),'crit_minus':int(x['crit_minus']),'raw':raw,'rd':x['rd'],'mitigation_on_hit':max(0,raw-net),'net_potential':net,'hp_loss_actual':actual,'overkill_potential':max(0,net-actual),'hp_before':x['hp_before'],'hp_after':x['hp_after'],'source_gate':row['source_gate'],'audited':True})
assert len(runs)==24 and len(set(r['run_id'] for r in runs))==24 and len(attacks)==1344
assert sum(r['events'] for r in runs)==2268 and sum(r['attacks'] for r in runs)==len(attacks) and sum(x['hit'] for x in attacks)==710
csv_write('R97_VALIDATED_RUNS_24.csv',runs,['run_id','cohort','matchup','seed','seed_group','side','species','ed','opening','phase','winner','events','attacks','hits','hp_B','hp_E','hp_R','turn_limit','initiative_method','source_gate','audit','independent_group'])
csv_write('R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv',attacks,list(attacks[0].keys()))
# Controlled species*seed*opening, one pair each (mirror)
blocks=[]
for key,group in __import__('itertools').groupby(sorted(runs,key=lambda z:(z['matchup'],z['seed'])),key=lambda z:(z['matchup'],z['seed'])):
 gr=list(group)
 assert len(gr)==2 and gr[0]['phase']==gr[1]['phase'] and gr[0]['winner']==gr[1]['winner'] and gr[0]['attacks']==gr[1]['attacks'] and gr[0]['hits']==gr[1]['hits'],key
 blocks.append({'matchup':key[0],'seed':key[1],'seed_group':gr[0]['seed_group'],'n_mirrors':2,'phase':gr[0]['phase'],'winner':gr[0]['winner'],'attacks_per_mirror':gr[0]['attacks'],'hits_per_mirror':gr[0]['hits'],'hp_B':gr[0]['hp_B'],'hp_E':gr[0]['hp_E'],'hp_R':gr[0].get('hp_R'),'independent_group':gr[0]['independent_group'],'admission':gr[0]['source_gate']})
assert len(blocks)==12
csv_write('R97_PAIRED_BLOCKS_12.csv',blocks,list(blocks[0].keys()))
# Corrected v2 no overwrite original; 27 power levels including special 26/27 > L5, star unknown unless own source
with (BASE/'R82_CORRECTED_BENCHMARK_SCHEMA_PRIMARY_104.csv').open(newline='') as f: base=list(csv.DictReader(f))
assert len(base)==104
for o in base:
 o['schema_version']='R97-27-ORDERED-BEAST-POWER-AUTHORIAL-003'
 if o['battery'].startswith(('B_SINGLE','D_DISTINCT')) and int(o['power_position'])>=26:
  o['rank']='';o['star']=''
  o['next_required']='SPECIAL_POWER_ABOVE_L5_BY_MESTRE_DECISION; NEVER require regular rank/star absent its specific source. ADM=26, Divina=27; no imported modifiers.'
 if o['battery']=='B_SINGLE_BEAST_LINEAGE_27' and int(o['power_position'])==23:
  o['source_identity']='Grifo-Matriarca de Sílica — L3 only; L2 numeric predecessor partially evidenced'
  o['source_status']='SOURCE_DOCUMENTED_CURRENT_L3; L2_HISTORY_PARTIAL; NO_27_STAGE_LINEAGE_YET'
  o['source_gate']='LINEAGE_VERSION_CANDIDATE_NON_HOMOLOGATED'
 if o['battery']=='D_DISTINCT_BEAST_PANEL_27' and int(o['power_position']) in (5,23,27):
  p=int(o['power_position']);name={5:'Frígido Ossário (Bronze 5)',23:'Grifo-Matriarca de Sílica (L3)',27:'Vaelthyr (Besta Divina, source specifies L4)'}[p]
  o['source_identity']=name;o['source_status']='DOCUMENTED_CANDIDATE_NOT_HOMOLOGATED';o['source_gate']='READBACK_SOURCE_ONLY_NO_POWER_PROMOTION'
  if p==27:o['next_required']='Besta Divina occupies power position 27, SUPERIOR Lendário 5; source Vaelthyr documents L4, only where that source specifies it; no separate rank demand.'
 if o['battery']=='A_INDIVIDUAL_ARCHETYPE_ED_25' and int(o['power_position'])==23:
  o['source_identity']='Sikong Auren L3 — duel basic only';o['source_status']='SOURCE_DOCUMENTED_BASIC_BOUNDED';o['experimental_1v1_runs_observed']='16';o['source_gate']='CONDITIONAL_ON_FIXED_OPENING_NOT_FULL_POWER'
 if o['battery']=='C_BALANCED_TEAM_25' and int(o['power_position'])==23:
  o['source_identity']='R93 Auren L3 + Feryn ON5 — 2x1 research, NOT balanced rank reference';o['source_status']='UNBALANCED_2X1_SANDBOX_ONLY';o['source_gate']='NOT_BENCHMARK_REFERENCE';o['next_required']='Source-valid team of same stage and complementary true ED roles; numeric counters, reactions, initiative competence and dynamics'
 o['reference_homologated']='0';o['clone_status']='SOURCE_CANDIDATE' if o['source_identity'] else 'NOT_BUILT'
csv_write('R97_POWER_GRID_104_CORRECTED_V2.csv',base,list(base[0].keys()))
lineage={'anchor_candidate':'Grifo-Matriarca de Sílica','authority':'BEAST-FULLSPEC-VZ-06','current_L3':{'rank':'Lendário 3','attrs':{'FOR':115,'DES':116,'CON':85,'INT':72,'SAB':94,'CAR':36},'attack':'6d6+138','ca':153,'rd':75,'vida':4315},'earlier_L2':{'attrs':{'FOR':110,'DES':112,'CON':80,'INT':70,'SAB':90,'CAR':35},'sum':497,'profile_status':'PARTIAL_SOURCE_RECORDED_IN_FULLSPEC'},'delta_attrs':{'FOR':5,'DES':4,'CON':5,'INT':2,'SAB':4,'CAR':1},'delta_total':21,'no_claim_L2_legal_full_combat':True,'power_grid_positions':27,'ready_legal_stage_profiles':1,'historically_recoverable_partial_predecessor':1,'position26':{'power':'ADM','data':'MISSING SAME_LINEAGE_ADM_PROOF'},'position27':{'power':'Divina','data':'MISSING SAME_LINEAGE_DIVINA_PROOF'}}
(R/'R98_LINEAGE_GRIFO_L2_L3.json').write_text(json.dumps(lineage,indent=2,ensure_ascii=False)+'\n')
beasts=[{'name':'Frígido Ossário','distinct_species':True,'power_position':5,'source':'https://app.notion.com/p/f0dc2b324ede820ab9470168d4a53315','source_status':'B5 original creature; R81 conditional prior, no new duel'},
 {'name':'Grifo-Matriarca de Sílica','distinct_species':True,'power_position':23,'source':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','source_status':'L3 PRECREATE, BASIC 1x1 R95 + TEAM R93, NOT official'},
 {'name':'Crocodilo de Lodo Astral Ancião','distinct_species':True,'power_position':23,'source':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','source_status':'L3 PRECREATE, R95 BASIC CENSORED; overflow at same position not distinct power slot'},
 {'name':'Serpente Prismática Regente','distinct_species':True,'power_position':23,'source':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','source_status':'L3 PRECREATE, 0 R95 combat'},
 {'name':'Roc da Tempestade de Vidro','distinct_species':True,'power_position':23,'source':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','source_status':'L3 PRECREATE, 0 R95 combat'},
 {'name':'Leviatã de Ferro Mnemônico','distinct_species':True,'power_position':24,'source':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','source_status':'L4 PRECREATE, 0 R95 combat'},
 {'name':'Vaelthyr','distinct_species':True,'power_position':27,'source':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','source_status':'Divina L4 per own source, power position 27, 0 benchmark'}]
for b in beasts:b['reference_homologated']=False
(R/'R98_DIVERSE_SPECIES_CANDIDATES_7.json').write_text(json.dumps({'candidates':beasts,'distinct_names':len(set(x['name'] for x in beasts)),'power_positions_with_sources':4,'admitted_basic_new_beast_species':2,'official_27_diverse_references':0,'note':'4 species have same L3 power position, cannot count as 4 populated power cells. No taxonomic duplicates counted.'},indent=2,ensure_ascii=False)+'\n')
# Crosswalk all 17 baseline unchanged; only additive delta evidence
cross=json.loads((BASE/'R91_17_CONTRACTS_RECONCILED.json').read_text())
assert len(cross['contracts'])==17
for c in cross['contracts']:
 c['R92_R101_delta']='Experimental independent semantic R95 source-basic fixed opener + R93 basic team 2x1; no production terminal proof.' if c['id'] in ('BATTLE_1X1_2X1_20X20','TURN_SCHEDULER_EVENT_SOURCING','RNG_REPLAY_STATISTICS','ACTOR_SNAPSHOT_SCENARIO','AUTHORITATIVE_RULES_AND_ADAPTERS') else 'No new terminal proof; R91 preserved.'
 c['terminal_certificate']='HOLD';c['official_promotion']=False
cross['cycle']='R92–R101';cross['terminal_certified']=0;cross['official_benchmark_cells']=0;cross['NAC_PASS_PRODUCTION']='HOLD'
(R/'R101_17_CONTRACTS_RECONCILED.json').write_text(json.dumps(cross,indent=2,ensure_ascii=False)+'\n')
summary={'operation':'OP-VLAB-FUSION-SANDBOX-01','cycle':'R92–R101','R95':{'runs':16,'events':A['total_events'],'attacks':A['total_attacks'],'hits':A['total_hits'],'censored':A['censored_runs'],'source_scenario':'SOURCE-ADMISSIBLE BASIC VS FIXED EXOGENOUS OPENING, NOT NATURAL INITIATIVE','unique_ids':16,'species':2,'seed_blocks':4,'mirror_pairs':8},'R93':{'runs':8,'events':T['events'],'attacks':T['attacks'],'hits':T['hits'],'censored':0,'unique_ids':8,'seed_blocks':4,'mirror_pairs':4,'team_composition':'AUREN_L3 + FERYN_ON5, NOT BALANCED ED TEAM'},'selected_combined':{'runs':24,'unique_run_ids':24,'events':sum(x['events'] for x in runs),'attacks':len(attacks),'hits':sum(x['hit'] for x in attacks),'completed':sum(x['phase']=='COMPLETE' for x in runs),'censored':sum(x['phase']=='CENSORED_HORIZON' for x in runs),'mirror_pairs':len(blocks)},'quarantine':{'R92':'prereg horizon120 vs executed60; technical ledger audit PASS, scientific horizon mismatch HOLD','R94':'prereg120 vs original executed60; interrupted recovery correctly not replayed but continued toward120 causing mirror mismatch; entire group exploratory HOLD','R93_precommit':'invalid cmd prefix initial sqlite genesis rev0 events0 pending0; QUARANTINE NOT RETRIED'},'grid':{'A':25,'B':27,'C':25,'D':27,'total':104,'official_populated':0,'ADM_power_position':26,'Divina_power_position':27},'redteam':{'semantic_mutations_rejected':6,'preflight_rejected':5},'terminal_contracts':0,'official_promotion':False}
(R/'R99_SCIENTIFIC_RECONCILIATION.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'runs':len(runs),'pairs':len(blocks),'attacks':len(attacks),'events':summary['selected_combined']['events'],'hits':summary['selected_combined']['hits'],'R95':A['censored_runs'],'R93':T['censored']},indent=2))
