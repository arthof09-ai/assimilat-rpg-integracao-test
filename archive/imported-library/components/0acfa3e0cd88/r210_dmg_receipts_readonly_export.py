"""Export only existing R210 journal observations; writes a CSV, never fights or sends to DMG."""
from pathlib import Path
import csv,json,sqlite3
ROOT=Path(__file__).resolve().parents[1]
PRE=json.loads((ROOT/'source/R210_SPORES_CENTERS_PREREG.json').read_text())
fields=['run_id','seed','arm','event_seq','action','source_id','actor_id','target_id','source_status','rank_status','radius_m','center_m','target_position','included','own_cast_seq','save_dice','save_total','save_success','raw','rd_magic_test_only','post_rd','effective_hp_loss','overkill','hp_before','hp_after','pa_before','pa_after','pa_paid','damage_type','critical','evidence_class','unit']
rows=[]
for p in sorted((ROOT/'evidence/db').glob('R210_CENTER_SPORES_S*.sqlite')):
 con=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True)
 try:
  st=json.loads(dict(con.execute('SELECT key,value FROM meta'))['state']);policy=st['r210']['policy']
  for ev in st['native_events']:
   if ev['action'] not in ('r210_area_cast','r210_area_target','weapon_attack'):continue
   row={k:'' for k in fields}
   row.update(run_id=p.stem,seed=st['seed'],arm=policy,event_seq=ev['seq'],action=ev['action'],
       source_id=PRE['source'] if ev['action'].startswith('r210') else PRE['beast_source'],
       actor_id=ev.get('by',ev.get('from','')),target_id=ev.get('target',ev.get('to','')),
       source_status='PROPOSED_NPC_AND_CONDITIONAL_BEAST',rank_status='DRACOLION_RANK_CONFLICT',
       evidence_class='LAB_EXECUTED_NOT_CANON',unit='EVENT_INSIDE_RUN_NOT_INDEPENDENT')
   if ev['action']=='r210_area_cast':
    row.update(center_m=json.dumps(ev['center_m']),radius_m=ev['radius_m'],included=json.dumps(ev['in_area']),
        own_cast_seq=ev['seq'],raw=ev['common_roll_total'],pa_before=ev['pa_before'],pa_after=ev['pa_after'],pa_paid=ev['pa_spent'],damage_type='PLANTA')
   elif ev['action']=='r210_area_target':
    row.update(center_m=json.dumps(PRE['centers_m'][policy]),radius_m=5,target_position=json.dumps(ev['position_m']),included='TRUE',
        own_cast_seq=ev['cast_event_seq'],save_dice=json.dumps(ev['save_dice']),save_total=ev['save_total'],save_success=ev['save_success'],
        raw=ev['damage_raw'],rd_magic_test_only=ev['rd_magic_applied'],post_rd=ev['damage_after_rd'],
        effective_hp_loss=ev['hp_loss_actual'],overkill=ev['overkill'],hp_before=ev['hp_before'],hp_after=ev['hp_after'],
        damage_type='PLANTA',critical='NOT_APPLICABLE')
   else:
    row.update(raw=ev['raw'],post_rd=ev['net'],effective_hp_loss=ev['hp_loss_actual'],overkill=ev['overkill'],
      hp_before=ev['before_hp'],hp_after=ev['after_hp'],critical=ev['critical'],damage_type='IMPACTO_PHYSICAL_TEST_CONDITIONAL')
   rows.append(row)
 finally:con.close()
out=ROOT/'evidence/R210_DMG_READONLY_RECEIPTS.csv'
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print({'export':str(out),'rows':len(rows),'no_transmission':True})
