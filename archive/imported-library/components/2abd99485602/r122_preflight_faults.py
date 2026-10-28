"""Directed fresh negative cases; existing R119 ledgers read-only. Faults are quarantined, never replayed."""
from pathlib import Path
from copy import deepcopy
import subprocess,sqlite3,json,sys,hashlib,os
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r119_integrated_three_actor as r
import vlab_r18_interactive as core

PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R122','seed_base':939100,
 'kind':'new copied SQLite fault/preflight fixtures',
 'cases':['NO_SLOT','R51_NESTED','FAKE_SOURCE_WINDOW','TARGET_ALLY','COUNTER_WITHOUT_DECLARATION','WRONG_ACTIVE','INVALID_REACTION','COMBINED_DOUBLE_TRIGGER','INJECT_AFTER_INTENT','INJECT_AFTER_COMMIT'],
 'inj_strike_seed':939901, 'inj_intent_seed':939902,
 'reuse_r18_atomic_commit':True,'NO_RETRY_UNKNOWN_EFFECT':True,'no_official_credit':True}

def prep(file,seed):
 r.init_db(file,seed);r.command(file,'INIT',{'seed':seed});st,_,_=core.load(file)
 r.command(file,'START',{'actor':st['active']});st,_,_=core.load(file)
 return st

def signature(file):
 with sqlite3.connect(file) as c:
  m=dict(c.execute('select key,value from meta'));events=c.execute('select count(*) from events').fetchone()[0]
  pending=c.execute('select count(*) from pending').fetchone()[0]
  h=hashlib.sha256(file.read_bytes()).hexdigest()
 return {'head':m['head'],'revision':int(m['revision']),'events':events,'pending':pending,'sqlite_sha':h,
   'state_sha':hashlib.sha256(m['state'].encode()).hexdigest()}

def negative(name,mutator,seed):
 file=ROOT/'runs'/f'R122_{name}_{seed}.sqlite'
 st=prep(file,seed)
 a=st['active'];target=r.choose_target(st,a);att=r.atk_payload(st,a,target)
 policy=r.choose_reaction(st,a,target)
 packet={'attack':att,'reaction':policy,'attack_origin':'NORMAL'}
 if policy=='COUNTER':packet['counter']=r.counter_payload(st,target,a)
 packet=mutator(st,deepcopy(packet))
 before=signature(file)
 caught=None
 try:r.command(file,'STRIKE',packet)
 except Exception as ex:caught=str(ex)
 if caught is None:raise AssertionError('REJECTION_NOT_ENFORCED '+name)
 after=signature(file)
 assert before['head']==after['head'] and before['revision']==after['revision']
 assert before['state_sha']==after['state_sha'] and after['pending']==0
 return {'name':name,'file':file.name,'caught':caught,'events_unchanged':True,'pending':0}

def no_slot_after_first_trigger():
 """Two enemy opportunities after one R50 declaration, before A's next own turn."""
 seed=939201;name='NO_SLOT_AFTER_FIRST_TRIGGER';file=ROOT/'runs'/f'R122_{name}_{seed}.sqlite'
 st=prep(file,seed);a=st['active'];assert a=='A'
 target='F1';at=r.atk_payload(st,'A',target)
 r.command(file,'STRIKE',{'attack':at,'reaction':'ESQUIVAR','attack_origin':'NORMAL'})
 r.command(file,'END',{'actor':'A'})
 st,_,_=core.load(file);assert st['active'] in ('F1','F2')
 first=st['active'];r.command(file,'START',{'actor':first})
 st,_,_=core.load(file);at=r.atk_payload(st,first,'A')
 cp=r.counter_payload(st,'A',first)
 r.command(file,'STRIKE',{'attack':at,'reaction':'COUNTER','counter':cp,'attack_origin':'NORMAL'})
 r.command(file,'END',{'actor':first})
 st,_,_=core.load(file)
 assert st['actors']['A']['resource']['reaction']==0
 assert st['active'] in ('F1','F2') and st['active']!=first
 next_actor=st['active'];r.command(file,'START',{'actor':next_actor})
 st,_,_=core.load(file);att=r.atk_payload(st,next_actor,'A');counter=r.counter_payload(st,'A',next_actor)
 bad={'attack':att,'reaction':'COUNTER','counter':counter,'attack_origin':'NORMAL'}
 before=signature(file)
 try:r.command(file,'STRIKE',bad)
 except Exception as ex:err=str(ex)
 else:raise AssertionError('SECOND_COUNTER_SHOULD_REJECT')
 after=signature(file)
 assert err=='NO_REACTION_SLOT_PRE_INTENT' and before['head']==after['head'] and before['state_sha']==after['state_sha'] and after['pending']==0
 return {'name':name,'file':file.name,'caught':err,'events_unchanged':True,'pending':0,
  'first_counter_consumed':True,'second_opportunity_rejected':True}

def work_fail(arg):
 file=Path(arg[0]);kind=arg[1]
 st,_,_=core.load(file);a=st['active'];target=r.choose_target(st,a);atk=r.atk_payload(st,a,target)
 reaction=r.choose_reaction(st,a,target)
 payload={'attack':atk,'reaction':reaction,'attack_origin':'NORMAL'}
 if reaction=='COUNTER':payload['counter']=r.counter_payload(st,target,a)
 r.command(file,'STRIKE',payload,failpoint=kind)

def fault(name,seed,failpoint):
 file=ROOT/'runs'/f'R122_{name}_{seed}.sqlite';st=prep(file,seed)
 pre=signature(file)
 sub=subprocess.run([sys.executable,str(ROOT/'r122_preflight_faults.py'),'--worker',str(file),failpoint],capture_output=True,text=True)
 expect=78 if failpoint=='AFTER_INTENT' else 77
 assert sub.returncode==expect,(sub.returncode,sub.stderr,sub.stdout)
 after=signature(file)
 if failpoint=='AFTER_INTENT':
  assert after['head']==pre['head'] and after['revision']==pre['revision'] and after['pending']==1
  assert after['state_sha']==pre['state_sha'] and after['events']==pre['events']
  try:core.load(file)
  except Exception as ex:assert 'UNKNOWN_EFFECT' in str(ex)
  else:raise AssertionError('UNKNOWN_EFFECT_OPEN_NOT_BLOCKED')
 else:
  assert after['revision']==pre['revision']+1 and after['events']==pre['events']+1 and after['pending']==0
  x,head,rev=core.load(file)
  assert head==after['head'] and rev==after['revision']
  with sqlite3.connect(file) as c:
   e=json.loads(c.execute('select row_json from events where seq=?',(rev,)).fetchone()[0])
   assert e['kind']=='STRIKE'
 return {'name':name,'db':file.name,'fault':failpoint,'exit':sub.returncode,
  'before':pre,'after':after,'classification':'UNKNOWN_EFFECT_HOLD_NO_RETRY' if failpoint=='AFTER_INTENT' else 'COMMIT_EXACTLY_ONCE_REOPENED'}

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='--worker':work_fail(sys.argv[2:]);sys.exit(0)
 p=ROOT/'R122_PREREG_ADVERSARIAL.json';
 if p.exists():assert json.loads(p.read_text())==PREREG
 else:p.write_text(json.dumps(PREREG,ensure_ascii=False,indent=2)+'\n')
 # All these errors must be caught BEFORE a durable intent, no semantic replay.
 mutations=[
 ('NO_SLOT',lambda s,p:{**p,'reaction':'COUNTER','counter':r.counter_payload(s,p['attack']['target'],s['active'])}),
 ('R51_NESTED',lambda s,p:{**p,'attack_origin':'COUNTER'}),
 ('FAKE_SOURCE_WINDOW',lambda s,p:{**p,'reaction':'MISSING_SOURCE'}),
 ('TARGET_ALLY',lambda s,p:{**p,'attack':{**p['attack'],'target':s['active']}}),
 ('COUNTER_WITHOUT_DECLARATION',lambda s,p:{**p,'reaction':'NONE','counter':{'fake':True}}),
 ('WRONG_ACTIVE',lambda s,p:{**p,'attack':{**p['attack'],'actor':'F1'}}),
 ('INVALID_REACTION',lambda s,p:{**p,'reaction':'REFLECT_MAGIC'}),
 ('COMBINED_DOUBLE_TRIGGER',lambda s,p:{**p,'reaction':'COUNTER','attack_origin':'COUNTER', 'counter':r.counter_payload(s,p['attack']['target'],s['active'])}),
 ]
 results=[]
 # Special no-slot case after a correctly established but spent reaction state; mutate source resource in an entirely fresh fixture.
 results.append(no_slot_after_first_trigger())
 for j,(name,m) in enumerate(mutations):
  if name=='NO_SLOT':continue
  try:results.append(negative(name,m,939101+j))
  except Exception as ex:raise RuntimeError(name+' '+str(ex)) from ex
 faults=[fault('AFTER_INTENT',939902,'AFTER_INTENT'),fault('AFTER_COMMIT',939901,'AFTER_COMMIT')]
 data={'operation':PREREG['operation'],'status':'PASS','negative_before_intent':len(results),
       'faults':len(faults),'negative_cases':results,'fault_cases':faults,'reused_original_storage':False,
       'R51':'counter-origin intent DENIED before reservation',
       'R18':'unknown effect left locked; after commit readback exactly once'}
 (ROOT/'R122_ADVERSARIAL_RESULTS.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':data['status'],'negative':len(results),'faults':len(faults),
         'codes':[r['caught'] for r in results],'outcomes':[f['classification'] for f in faults]},indent=2))
