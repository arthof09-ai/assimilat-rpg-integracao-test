"""Extract fresh read-only scientific receipts for DMG; never rerun combat."""
from pathlib import Path
import csv,sqlite3,json
root=Path(__file__).resolve().parents[1]
rows=[]
for p in sorted((root/'evidence/db').glob('R207_TEAM_HEAL_2V1_*.sqlite')):
 con=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True)
 try:st=json.loads(dict(con.execute('SELECT key,value FROM meta'))['state'])
 finally:con.close()
 for ev in st['native_events']:
  if ev['action'] not in ('weapon_attack','r207_reactive_heal'):continue
  typ='HEALING' if ev['action']=='r207_reactive_heal' else 'ATTACK'
  rows.append({'case':'R207','run_id':p.stem,'seed':st['seed'],'policy':st['r207']['policy'],
   'event_seq':ev['seq'],'event_type':typ,'actor':ev.get('from',ev.get('by')),
   'target':ev.get('to',ev.get('target')),'source':ev.get('source',st['r207']['source']),
   'source_state':'PROPOSTO_AND_BEAST_CONDITIONAL_TEST','critical':ev.get('critical',''),
   'hit':ev.get('hit',''),'roll_score':ev.get('roll_score',''),
   'ca_exact':ev.get('ca_exact',''),'damage_gross':ev.get('raw',''),
   'rd_applied':ev.get('rd_applied',''),'damage_after_rd':ev.get('net',''),
   'hp_loss_actual':ev.get('hp_loss_actual',''),'overkill':ev.get('overkill',''),
   'heal_nominal':ev.get('heal_nominal',''),'heal_effective':ev.get('heal_effective',''),
   'heal_excess':ev.get('heal_excess',''),'pa_spent':ev.get('pa_spent',0),
   'reaction':ev.get('reaction_spent',0),'scope':'SCIENCE_LOCAL_TEST_NOT_CANONICAL',
   'unit_of_independence':'seed_pair'})
assert len(rows)==156
out=root/'evidence/R207_DMG_READONLY_RECEIPTS.csv'
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(out,len(rows))
