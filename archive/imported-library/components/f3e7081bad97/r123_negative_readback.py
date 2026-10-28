"""R122 negative fixtures: non-persistent preflight re-check only, NEVER re-issue committed commands."""
import sys,json,sqlite3,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r119_integrated_three_actor as r
import vlab_r18_interactive as core

def readfile(file):
 with sqlite3.connect(file) as c:
  m=dict(c.execute('select key,value from meta'));n=c.execute('select count(*) from events').fetchone()[0];p=c.execute('select count(*) from pending').fetchone()[0]
 return {'head':m['head'],'revision':int(m['revision']),'events':n,'pending':p,'state_sha':core.sha(json.loads(m['state']))}

def mutate(name,st,packet):
 a=st['active'];target=packet['attack']['target']
 if name=='R51_NESTED':packet['attack_origin']='COUNTER'
 elif name=='FAKE_SOURCE_WINDOW':packet['reaction']='MISSING_SOURCE'
 elif name=='TARGET_ALLY':packet['attack']['target']=a
 elif name=='COUNTER_WITHOUT_DECLARATION':packet.update({'reaction':'NONE','counter':{'fake':True}})
 elif name=='WRONG_ACTIVE':packet['attack']['actor']='F1'
 elif name=='INVALID_REACTION':packet['reaction']='REFLECT_MAGIC'
 elif name=='COMBINED_DOUBLE_TRIGGER':packet.update({'reaction':'COUNTER','attack_origin':'COUNTER','counter':r.counter_payload(st,target,a)})
 elif name=='NO_SLOT_AFTER_FIRST_TRIGGER':packet.update({'reaction':'COUNTER','counter':r.counter_payload(st,target,a)})
 else:raise RuntimeError(name)
 return packet

out=[]
for file in sorted((ROOT/'runs').glob('R122_*.sqlite')):
 token=file.stem.split('_')
 if ('NO_SLOT_939101' in file.name or 'AFTER_INTENT' in file.name or 'DIAG' in file.name or 'DEBUG' in file.name):continue
 # Only 8 known preflight fixtures, exclude any positive failpoint case.
 if not any(x in file.name for x in ('R51_NESTED','FAKE_SOURCE_WINDOW','TARGET_ALLY','COUNTER_WITHOUT_DECLARATION','WRONG_ACTIVE','INVALID_REACTION','COMBINED_DOUBLE_TRIGGER','NO_SLOT_AFTER_FIRST_TRIGGER')):continue
 before=readfile(file);st,head,rev=core.load(file)
 assert (head,rev)==(before['head'],before['revision']) and before['pending']==0
 a=st['active'];target=r.choose_target(st,a);atk=r.atk_payload(st,a,target)
 policy=r.choose_reaction(st,a,target)
 packet={'attack':atk,'reaction':policy,'attack_origin':'NORMAL'}
 if policy=='COUNTER':packet['counter']=r.counter_payload(st,target,a)
 name=next(k for k in ('NO_SLOT_AFTER_FIRST_TRIGGER','COUNTER_WITHOUT_DECLARATION','COMBINED_DOUBLE_TRIGGER','FAKE_SOURCE_WINDOW','INVALID_REACTION','TARGET_ALLY','WRONG_ACTIVE','R51_NESTED') if k in file.name)
 packet=mutate(name,st,packet)
 try:r.attack_preflight(st,packet)
 except Exception as ex:code=str(ex)
 else:raise AssertionError('NEGATIVE_PREVALIDATION_UNEXPECTEDLY_PASSED '+name)
 after=readfile(file)
 assert after==before,(name,after,before)
 out.append({'case':name,'db':file.name,'status':'PASS_PREINTENT_REJECTED_NO_DB_MUTATION',
  'reason':code,'verified_head':head,'revision':rev,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
assert len(out)==8,len(out)
(ROOT/'R123_8_NEGATIVE_GATES_COLD_READBACK.json').write_text(json.dumps({'total':8,'passed':8,'status':'PASS',
   'method':'no event commits, preflight-only re-evaluation + physical ledger readback','cases':out},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':8,'codes':[x['reason'] for x in out]},indent=2))
