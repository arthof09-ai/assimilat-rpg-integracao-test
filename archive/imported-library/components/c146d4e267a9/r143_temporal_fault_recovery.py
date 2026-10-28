"""R143 injected process faults across source Passo activation. Two new isolated banks.
AFTER_INTENT remains UNKNOWN_EFFECT; AFTER_COMMIT is recovered then new commands END.
"""
import json,hashlib,sqlite3,subprocess,sys
from pathlib import Path
import r138_multiround_native as m
ROOT=Path(__file__).resolve().parent
PRE={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R143',
 'sources':{'Passo':'Feryn 25PA Movement +12m this turn','turn':'Combat rule1 + R18 persistence'},
 'seeds':{'AFTER_INTENT':994211,'AFTER_COMMIT':994212},
 'fixture':'Feryn starts his own turn (action budget1), no initiative certified by fixture',
 'continuation':'AFTER_COMMIT only: FOREGO STANDARD then END and expire Passo',
 'no_repeat':'Do not run generator over any prior pending or command IDs'}

def prereg():
 p=ROOT/'R143_PREREG.json';b=m.can(PRE)
 if p.exists():assert p.read_text()==b
 else:p.write_text(b)

def init(mode,seed):
 run='R143_TEMP_PASSO_'+mode+'_S'+str(seed);db=ROOT/'runs'/(run+'.sqlite')
 if db.exists():raise ValueError('EXISTING_RUN_HOLD')
 m.core.init_db(db,'A',seed);st=m.genesis(run,seed)
 st['phase']='ACTIVE';st['round']=1;st['active']='F1';st['order']=['F1','A','E']
 st['actors']['F1']['resource']['standard']=1;st['actors']['F1']['resource']['movement']=1
 st['actor_turns']['F1']=1
 st['fixture_type']='PRETURN_EXPERIMENTAL_NOT_INITIATIVE_PROOF';st['prereg_sha256']=hashlib.sha256((ROOT/'R143_PREREG.json').read_bytes()).hexdigest()
 head=m.core.sha({'genesis':st,'R143':'TEMPORAL_FAULT_TEST'})
 with m.core.connect(db) as c:
  for k,v in [('scene',st['scene']),('genesis',head),('head',head),('state',m.core.canonical(st))]:
   c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 db.with_suffix('.genesis.json').write_text(m.core.canonical(st)+'\n')
 return db

def raw(db):
 with sqlite3.connect(db) as c:
  meta=dict(c.execute('select key,value from meta'))
  rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
  pending=list(c.execute('select cmd_id from pending'))
 return {'state':json.loads(meta['state']),'revision':int(meta['revision']),
  'events':rows,'pending':pending,'head':meta['head']}

def fault(mode,seed):
 db=ROOT/'runs'/f'R143_TEMP_PASSO_{mode}_S{seed}.sqlite'
 m.command(db,'PASSO',{'actor':'F1','intent':'THIS_TURN_ONLY'},failpoint=mode)

def run():
 prereg();reports=[]
 for mode,seed,expected_return in [('AFTER_INTENT',994211,78),('AFTER_COMMIT',994212,77)]:
  db=init(mode,seed);before=raw(db)
  completed=subprocess.run([sys.executable,str(Path(__file__)),mode,str(seed)],capture_output=True,text=True)
  assert completed.returncode==expected_return,(mode,completed.returncode,completed.stderr)
  after=raw(db)
  assert before['state']['actors']['F1']['resource']['pa']==424
  if mode=='AFTER_INTENT':
   assert after['revision']==0 and after['events']==[] and len(after['pending'])==1
   assert after['state']==before['state'] and after['head']==before['head']
   try:m.core.load(db)
   except Exception as e:assert 'UNKNOWN_EFFECT' in str(e)
   else:raise AssertionError('PENDING_READ_NOT_BLOCKED')
   status='UNKNOWN_EFFECT_HOLD_NO_REPLAY'
  else:
   assert after['revision']==1 and len(after['events'])==1 and after['pending']==[]
   assert after['state']['actors']['F1']['resource']['pa']==399
   assert after['state']['actors']['F1']['resource']['movement']==0
   assert after['state']['temporary']['F1']['bonus_speed_m']==12
   assert m.core.load(db)[2]==1
   # Legal NEW commands after a physically confirmed commit, never a duplicate retry.
   m.command(db,'FOREGO',{'actor':'F1'})
   m.command(db,'END',{'actor':'F1'})
   final=raw(db)
   assert final['revision']==3 and len(final['events'])==3 and final['pending']==[]
   assert final['state']['temporary']=={} and final['state']['actors']['F1']['resource']['pa']==399
   assert final['events'][-1]['detail']['native_actions'][-1]['action']=='EXPIRE_TURN_EFFECT'
   status='RECOVERED_COMMIT_THEN_NEW_TURN_EXPIRY'
  reports.append({'run_id':db.stem,'mode':mode,'process_returncode':completed.returncode,
   'before_revision':before['revision'],'after_revision':after['revision'],
   'final_revision':3 if mode=='AFTER_COMMIT' else 0,
   'pending':len(after['pending']),'status':status,
   'source_db_hash':hashlib.sha256(db.read_bytes()).hexdigest(),
   'no_replayed_command':True})
 out={'stage':'R143','results':reports,'source':'Feryn Passo da Fuligem',
  'writer':'NONE; LOCAL SANDBOX','official_certification':False}
 (ROOT/'R143_FAULT_RESULTS.json').write_text(m.can(out))
 return out
if __name__=='__main__':
 if len(sys.argv)>1:fault(sys.argv[1],int(sys.argv[2]));sys.exit(0)
 print(m.can(run()))
