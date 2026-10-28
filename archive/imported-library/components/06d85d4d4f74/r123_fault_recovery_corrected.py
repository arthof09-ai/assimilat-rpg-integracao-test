"""Fresh R123 crash measurements: explicitly close readers and observe WAL before readback.
Does not invoke any R122 failed fixture or replay pending commands.
"""
import sys,subprocess,sqlite3,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r122_preflight_faults as old
import r119_integrated_three_actor as r
import vlab_r18_interactive as core
PREREG={'stage':'R123','seeds':{'AFTER_INTENT':939906,'AFTER_COMMIT':939907},
 'fresh_fixtures_only':True,'no_retry':True,'intent_policy':'durable SQLite pending, preserve UNKNOWN_EFFECT',
 'after_commit_policy':'exactly one published event, no replay','previous_R122_fault_error':'HOLD_NO_RETRY'}
P=ROOT/'R123_PREREG_CRASH.json'
if P.exists():assert json.loads(P.read_text())==PREREG
else:P.write_text(json.dumps(PREREG,indent=2)+'\n')

def inspect(file):
 with sqlite3.connect(file) as con:
  m=dict(con.execute('select key,value from meta'))
  pd=con.execute('select cmd_id,base_head,kind from pending').fetchall()
  ev=con.execute('select row_json from events order by seq').fetchall()
  state=json.loads(m['state']);rev=int(m['revision'])
 # Context-manager does not close sqlite connections, so do not rely on it for teardown.
 return {'head':m['head'],'revision':rev,'pending':pd,'events':len(ev),
         'snapshot_sha':core.sha(state),'last_row':json.loads(ev[-1][0]) if ev else None}

results=[]
for kind,seed in PREREG['seeds'].items():
 file=ROOT/'runs'/f'R123_FRESH_{kind}_{seed}.sqlite'
 old.prep(file,seed)
 before=inspect(file)
 child=subprocess.run([sys.executable,str(ROOT/'r122_preflight_faults.py'),'--worker',str(file),kind],capture_output=True,text=True)
 wal_before_read=[{'name':f.name,'bytes':f.stat().st_size} for f in file.parent.glob(file.name+'*')]
 after=inspect(file)
 assert child.returncode==(78 if kind=='AFTER_INTENT' else 77),(kind,child.returncode,child.stderr)
 if kind=='AFTER_INTENT':
  if not(len(after['pending'])==1 and after['head']==before['head'] and after['revision']==before['revision'] and after['events']==before['events']):
   status='FAIL_INTENT_DURABILITY'
  else:
   try:core.load(file)
   except Exception as ex:status='PASS_UNKNOWN_EFFECT_LOCKED' if 'UNKNOWN_EFFECT' in str(ex) else 'FAIL_WRONG_ERROR_'+str(ex)
   else:status='FAIL_AUTO_READ_ALLOWED'
 else:
  if after['revision']!=before['revision']+1 or after['events']!=before['events']+1 or after['pending'] or after['last_row']['kind']!='STRIKE':
   status='FAIL_COMMIT_INTEGRITY'
  else:
   try:st,h,rv=core.load(file);status='PASS_EXACTLY_ONCE_REOPENED' if (h,rv)==(after['head'],after['revision']) else 'FAIL_MISMATCH'
   except Exception as ex:status='FAIL_CANNOT_REOPEN_'+str(ex)
 results.append({'kind':kind,'seed':seed,'file':file.name,'exit':child.returncode,
   'WAL_state_at_crash':wal_before_read,'before':{k:v for k,v in before.items() if k!='last_row'},
   'after':{k:v for k,v in after.items() if k!='last_row'},'status':status})

out={'operation':'OP-VLAB-FUSION-SANDBOX-01','R123':results,'status':'PASS' if all(z['status'].startswith('PASS') for z in results) else 'HOLD'}
(ROOT/'R123_NEW_FAULT_RESULTS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':out['status'],'results':[{k:v for k,v in x.items() if k in ('kind','status','seed','WAL_state_at_crash')} for x in results]},indent=2))
