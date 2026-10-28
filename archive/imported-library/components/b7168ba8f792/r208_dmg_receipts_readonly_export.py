from pathlib import Path
import sqlite3,json,csv
root=Path(__file__).resolve().parents[1];out=[]
for p in sorted((root/'evidence/db').glob('R208_NATIVE_PULSO_GLOVES_TEAM2V1_*.sqlite')):
 con=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True)
 try:st=json.loads(dict(con.execute('SELECT key,value FROM meta'))['state'])
 finally:con.close()
 for x in st['native_events']:
  if x['action'] not in ('weapon_attack','PULSO_ESTABILIZACAO'):continue
  typ='HEAL' if x['action']=='PULSO_ESTABILIZACAO' else 'ATTACK'
  out.append({'RUN_ID':p.stem,'seed':st['seed'],'policy':st['r208']['policy'],'event_seq':x['seq'],
   'type':typ,'caster_or_attacker':x.get('from',x.get('by')),'target':x.get('to'),
   'source_status':'PROPOSED_ERISTAN_BEAST_CONDITIONAL','raw':x.get('raw',''),
   'rd':x.get('rd_applied',''),'post_rd':x.get('net',''),'lost_hp':x.get('hp_loss_actual',''),
   'overkill':x.get('overkill',''),'healing_base':x.get('source_base',''),
   'gloves_bonus':x.get('gloves_bonus',''),'healing_gross':x.get('gross_heal',''),
   'healing_actual':x.get('actual_heal',''),'healing_excess':x.get('excess_heal',''),
   'PA_spent':x.get('PA_spent',0),'sample_unit':'PAIRED_SEED'})
assert len(out)==63+16
with (root/'evidence/R208_DMG_READONLY_RECEIPTS.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(len(out))
