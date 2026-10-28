"""New R134 process-fault probes. Do not retry any pending command.
Reuses R126 integrated native scene and R18 original commit; two NEW DBs.
"""
from pathlib import Path
import json,sqlite3,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r126_native_integration as v

def state(db):
 with sqlite3.connect(db) as con:
  meta=dict(con.execute('select key,value from meta'));return {'revision':int(meta['revision']),
    'state':json.loads(meta['state']),'pending':con.execute('select count(*) from pending').fetchone()[0],
    'event_count':con.execute('select count(*) from events').fetchone()[0], 'head':meta['head']}

def prepare(mode,seed):
 db=ROOT/'runs'/f'R134_{mode}_{seed}.sqlite';v.init(db,seed)
 v.command(db,'INIT',{'seed':seed});st,_,_=v.core.load(db)
 assert st['active']=='A',(st['order'],seed)
 v.command(db,'START',{'actor':'A'});st,_,_=v.core.load(db)
 tape=v.attack_tape(st,'A','F1',dis=1)
 assert not(tape['crit'][:2]==[1,1] and tape['crit'][2]<=2)
 return db,{'attack':tape,'reaction':'CAPA'}

def work(mode,seed):
 db=ROOT/'runs'/f'R134_{mode}_{seed}.sqlite';payload=json.loads((ROOT/'runs'/f'R134_{mode}_{seed}.attack.json').read_text())
 v.command(db,'STRIKE',payload,failpoint=mode)

def audit(db,before,mode):
 after=state(db);a=after['state']['actors'];b=before['state']['actors']
 if mode=='AFTER_INTENT':
  assert after['pending']==1 and after['event_count']==before['event_count']
  assert after['revision']==before['revision'] and after['head']==before['head']
  assert a==b and after['state']==before['state']
 else:
  assert after['pending']==0 and after['event_count']==before['event_count']+1
  assert after['revision']==before['revision']+1 and after['head']!=before['head']
  assert a['F1']['resource']['pa']==b['F1']['resource']['pa']-35
  assert a['F1']['resource']['reaction']==0
  with sqlite3.connect(db) as con:
   e=json.loads(con.execute('select row_json from events order by seq desc limit 1').fetchone()[0])
  assert e['kind']=='STRIKE' and e['detail']['native_actions'][0]['action']=='CAPA_POEIRA'
 return {'run_id':db.stem,'mode':mode,'before_revision':before['revision'],'after_revision':after['revision'],
  'pending':after['pending'],'event_count':after['event_count'],'HP_before':{k:x['resource']['hp'] for k,x in b.items()},
  'HP_after':{k:x['resource']['hp'] for k,x in a.items()},'PA_before':b['F1']['resource']['pa'],
  'PA_after':a['F1']['resource']['pa'],'reaction_after':a['F1']['resource']['reaction'],
  'status':'UNKNOWN_EFFECT_HOLD_NO_REPLAY' if mode=='AFTER_INTENT' else 'POST_COMMIT_REOPEN_ONCE',
  'sha256':hashlib.sha256(db.read_bytes()).hexdigest()}

if __name__=='__main__':
 if len(sys.argv)>1:
  work(sys.argv[1],int(sys.argv[2]));sys.exit(0)
 reports=[]
 for mode,seed,code in [('AFTER_INTENT',973213,78),('AFTER_COMMIT',973214,77)]:
  db,payload=prepare(mode,seed)
  (ROOT/'runs'/f'R134_{mode}_{seed}.attack.json').write_text(json.dumps(payload,indent=2)+'\n')
  before=state(db)
  result=subprocess.run([sys.executable,str(Path(__file__)) ,mode,str(seed)],capture_output=True,text=True)
  assert result.returncode==code,(result.returncode,result.stderr)
  reports.append(audit(db,before,mode))
 out=ROOT/'R134_FAULT_RECOVERY.json';out.write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
