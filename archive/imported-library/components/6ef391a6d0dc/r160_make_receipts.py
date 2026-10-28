from pathlib import Path
import sqlite3,json,csv,collections,hashlib
R=Path('/mnt/data/vlab_succession/r151_r160');D=R/'runs'
selected=['R157_TACTIC_BASIC_DEV_S997617','R157_TACTIC_WIND_DEV_S997617','R158_NEGATIVE_CRITICAL_TACTIC_DEV_S997946','R153_CASULO_CA_SOURCE_DEV_S999013','R154_TWO_AOO_FULL_SOURCE_DEV_S999141','R154_TWO_AOO_KO_SOURCE_DEV_S999142','R155_AOO_NEGATIVE_R42_R43_DEV_S999353','R159_ED_GRIFO_AUREN_BE_SPECIAL_DEV_S998803','R159_ED_GRIFO_AUREN_BE_BASIC_DEV_S998803']
fields=['ledger_file','run_id','seed','seq_R18','action_index_in_tx','kind','action','actor','target','attack_origin','source_spec','critical','critical_policy','hit','attack_score','target_CA','damage_raw','rd_applied','net_post_RD','hp_effectively_lost','overkill','hp_after','PA_spent','damage_type','save_effect','save_CD','save_score','roll_tape_critical','roll_tape_hit','roll_tape_damage','source_assumption','audit_status','cmd_id','row_SHA256']
def get_genesis(n):
 d=json.loads((D/(n+'.genesis.json')).read_text());return d
results=[];all_commits=0;byrun={}
for run in selected:
 c=sqlite3.connect(D/(run+'.sqlite')); c.row_factory=sqlite3.Row
 rows=c.execute('select seq,cmd_id,row_json,row_sha from events order by seq').fetchall(); all_commits+=len(rows)
 meta={x[0]:x[1] for x in c.execute('select key,value from meta')}; pending=c.execute('select count(*) from pending').fetchone()[0];assert pending==0,(run,pending)
 gen=get_genesis(run); seed=None
 for k in ('seed','seed_int'):
  if k in gen:seed=gen[k]
 if seed is None:
  for k in ('seed','scenario_seed'):
   if k in gen.get('rng',{}):seed=gen['rng'][k]
 if seed is None:
  import re
  seed=int(re.search(r'S(\d+)$',run).group(1))
 ct=collections.Counter();nrec=0
 for sr in rows:
  item=json.loads(sr['row_json']);detail=item.get('detail') or {};native=detail.get('native_actions') or ([] if not detail.get('native_action') else [detail['native_action']]);ct[item['kind']]+=1
  for i,a in enumerate(native):
   if a.get('action') not in ('weapon_attack','spell'):continue
   nrec+=1
   score=a.get('roll_score')
   if a.get('action')=='spell':
    actor=a.get('by'); target=a.get('target');typ=a.get('damage_type');source=a.get('source_rule');hp_after=a.get('hp_after');raw=a.get('raw');hp_before=a.get('hp_before'); actual=a.get('effective'); net=actual
    crit=a.get('critical'); attack_origin='SPELL_NO_PHYSICAL_ATTACK';savecd=detail.get('extra',{}).get('save_cd');savescore=detail.get('extra',{}).get('save_score') or detail.get('extra',{}).get('reflexo_score'); hit='SAVE_EFFECT';ca='';critical_seq=[];atroll=[];droll=a.get('damage_rolls') or []
   else:
    actor=a.get('from');target=a.get('to');typ=a.get('type');source='DOCUMENTED_PHYSICAL_ATTACK';hp_after=a.get('after_hp');raw=a.get('raw');hp_before=a.get('before_hp');actual=a.get('hp_loss_actual');net=a.get('net');crit=a.get('critical');attack_origin=a.get('attack_origin');savecd='';savescore='';hit=a.get('hit');ca=a.get('ca_exact');critical_seq=a.get('critical_sequence') or [];atroll=a.get('attack_roll_attempts') or [];droll=a.get('damage_roll_groups') or []
   assumptions=[]
   if run.startswith('R157') or run.startswith('R158'):
    assumptions=['MESTRE_SIDE_PROPOSED_NPCS','ELEMENTAL_RD_ZERO_LAB_ONLY_IF_SPELL']
   elif run.startswith('R159'):assumptions=['SOURCE_ED_BE_CONDITIONAL','BESTA_INITIATIVE_EXOGENOUS','SHORT_LINE_LAB_1_5m','LIGHTNING_RD_UNDOCUMENTED_NOT_OFFICIAL_ZERO']
   elif run.startswith('R153'):assumptions=['CASULO_2_TURN_EXPIRY_HOLD','ERISTAN_ABSOLUTE_MOVEMENT_UNKNOWN']
   else: assumptions=['TOPOLOGICAL_B0_B3_WITH_LOCAL_METRES_ONLY','R43_DES_PRIORITY']
   results.append(dict(zip(fields,[run+'.sqlite',item.get('payload',{}).get('run_id',run),seed,sr['seq'],i+1,item['kind'],a.get('action'),actor,target,attack_origin,source,crit,a.get('critical_failure_policy'),hit,score,ca,raw,a.get('rd_applied',0),net,actual,a.get('overkill',0),hp_after,a.get('PA_spent',0),typ,a.get('save_effect',''),savecd,savescore,json.dumps(critical_seq),json.dumps(atroll),json.dumps(droll),'|'.join(assumptions),'COLD_TECHNICAL_PASS_NOT_OFFICIAL',sr['cmd_id'],sr['row_sha']])))
 byrun[run]={'commits':len(rows),'native_offenses':nrec,'event_kinds':dict(ct),'pending':pending,'genesis_sha256':hashlib.sha256((D/(run+'.genesis.json')).read_bytes()).hexdigest(),'sqlite_sha256':hashlib.sha256((D/(run+'.sqlite')).read_bytes()).hexdigest()}
 c.close()
assert all_commits==466,(all_commits,byrun)
with (R/'R160_NEW_NATIVE_OFFENSE_RECEIPTS_SOURCE_SCOPED.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(results)
with (R/'R160_SELECTED_LEDGER_COUNTS.json').open('w') as f:json.dump({'selected_ledgers':len(selected),'selected_commits':all_commits,'actual_offense_receipts':len(results),'per_run':byrun,'exclude_from_science':['R156_AFTER_INTENT_PENDING','R159_SPECIAL_S998801_ODD_HALF','R159_BASIC_S998801_UNPAIRED'],'official_benchmark_cells':0},f,indent=2)
print('Physical selected ledgers',len(selected),'commits',all_commits,'offensive native action receipts',len(results));print([(k,v['commits'],v['native_offenses']) for k,v in byrun.items()])
