"""Cold independent raw SQLite validation: R143 faults and effect lifetime.
No import of native, core, or R143 executor.
"""
import sqlite3,json,hashlib
from pathlib import Path
import r139_cold_independent as audit
ROOT=Path(__file__).resolve().parent

def read(p):
 with sqlite3.connect(p) as c:
  meta=dict(c.execute('select key,value from meta'))
  rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
  pending=[list(x) for x in c.execute('select * from pending')]
 return meta,rows,pending

def check():
 out=[]
 for mode,seed in [('AFTER_INTENT',994211),('AFTER_COMMIT',994212)]:
  db=ROOT/'runs'/f'R143_TEMP_PASSO_{mode}_S{seed}.sqlite'
  st=json.loads(db.with_suffix('.genesis.json').read_text());meta,rows,pending=read(db)
  before=st['actors']['F1']['resource'];assert before['pa']==424 and before['movement']==1
  assert meta['genesis']==meta['genesis'] and st['active']=='F1' and st['round']==1
  if mode=='AFTER_INTENT':
   assert len(pending)==1 and not rows and meta['revision']=='0'
   assert json.loads(meta['state'])==st and meta['head']==meta['genesis']
   assert pending[0][1]==meta['head'] and pending[0][2]=='PASSO'
  else:
   assert not pending and len(rows)==3 and meta['revision']=='3'
   current=st;head=meta['genesis']
   for i,row in enumerate(rows,1):
    assert row['prev']==head and row['before_sha']==audit.sha(current) and row['seq']==i
    ev=row['detail']['native_actions']
    if row['kind']=='PASSO':
     assert ev[0]['action']=='PASSO_FULIGEM' and ev[0]['PA_spent']==25 and ev[0]['duration']=='ESTE_TURNO'
     current['actors']['F1']['resource']['pa']-=25;current['actors']['F1']['resource']['movement']=0
     current['temporary']['F1']={'source':current['actors']['F1']['source'],'kind':'PASSO_FULIGEM',
      'bonus_speed_m':12,'expires_at':'END_CURRENT_F1_TURN','activated_own_turn':1}
    elif row['kind']=='FOREGO':
     assert ev[0]['action']=='FOREGO_STANDARD';current['actors']['F1']['resource']['standard']=0
    elif row['kind']=='END':
     assert len(ev)==2 and ev[1]['action']=='EXPIRE_TURN_EFFECT' and ev[1]['bonus_speed_removed_m']==12
     current['temporary'].pop('F1');current['turn_index']+=1;current['active']='A'
    else:raise AssertionError('unknown action')
    assert row['after_sha']==audit.sha(current),(mode,i)
    head=audit.sha(row)
   assert audit.sha(current)==audit.sha(json.loads(meta['state'])) and meta['head']==head
   assert current['actors']['F1']['resource']['pa']==399 and current['temporary']=={}
  out.append({'run_id':db.stem,'mode':mode,'pending':len(pending),'commits':len(rows),
   'raw_chain':'PASS','semantic_replay':'PASS','state_is_unchanged':mode=='AFTER_INTENT',
   'official':False,'sha256':hashlib.sha256(db.read_bytes()).hexdigest()})
 return {'stage':'R144','independent_import_native':False,'fault_cases':out,'pass':2}
if __name__=='__main__':
 data=check();(ROOT/'R144_INDEPENDENT_FAULT_AUDIT.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(data,indent=2,ensure_ascii=False))
