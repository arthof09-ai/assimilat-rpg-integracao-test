from pathlib import Path
import sqlite3,json,csv
root=Path(__file__).resolve().parents[1];out=[]
for p in sorted((root/'evidence/db').glob('R209_AREA_SPORES_S*.sqlite')):
 con=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True)
 try:st=json.loads(dict(con.execute('SELECT key,value FROM meta'))['state'])
 finally:con.close()
 for x in st['native_events']:
  if x['action'] not in ('weapon_attack','r209_area_cast','r209_area_target'):continue
  out.append({'RUN_ID':p.stem,'seed':st['seed'],'policy':st['r209']['policy'],'event_seq':x['seq'],'action':x['action'],
   'actor':x.get('from',x.get('by')),'target':x.get('to',x.get('target')),
   'source_status':'PROPOSED_ERISTAN_AND_TEST_BEAST','cast_event_seq':x.get('cast_event_seq',''),
   'save_total':x.get('save_total',''),'save_success':x.get('save_success',''),
   'damage_raw':x.get('damage_raw',x.get('raw','')),
   'rd_applied':x.get('rd_magic_applied',x.get('rd_applied','')),
   'after_rd':x.get('damage_after_rd',x.get('net','')),
   'lost_hp':x.get('hp_loss_actual',''),'overkill':x.get('overkill',''),
   'PA_spent':x.get('pa_spent',0),'in_area':x.get('in_area',''),'self_target':x.get('self_target',''),
   'unit_independence':'PAIRED_SEED'})
assert len(out)==156+30+90
with (root/'evidence/R209_DMG_READONLY_RECEIPTS.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(len(out))
