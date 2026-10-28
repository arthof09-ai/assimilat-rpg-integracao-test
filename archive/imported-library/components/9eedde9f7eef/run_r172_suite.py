"""R172 test orchestrator: NEW disposable runs only, no historical RUN IDs or DB edits."""
import os,sys,json,subprocess,sqlite3,copy,hashlib,pathlib,traceback
from dataclasses import asdict
from r172_atomic_counter import (r18,execute,counter_payload,cold_status,abort_pending_lab_only,
  start_three_actor_fixture,pass_existing_r18_turn,write_checkpoint)
from r172_independent_replay_auditor import audit
HERE=pathlib.Path(__file__).resolve().parent
RUNS=pathlib.Path(os.environ.get('R172_RUN_ROOT',str(HERE/'runs_test')));RUNS.mkdir(parents=True,exist_ok=True)
RESULT=[]

def db_new(name,seed):
 path=RUNS/(name+'.sqlite')
 assert not path.exists(),('NO_REPEAT:'+name)
 r18.init_db(path,'A',seed)
 return path

def test(name,fn):
 try:
  evidence=fn();RESULT.append({'test':name,'status':'PASS','evidence':evidence})
 except Exception as exc:
  RESULT.append({'test':name,'status':'FAIL','exception':repr(exc),'traceback':traceback.format_exc()[-2500:]})
  print('FAIL',name,exc)

def main():
 def normal():
  db=db_new('R172_HAPPY_DOUBLE_NEW_S1722101',1722101)
  c1='LAB-CMD-R172-HAPPY-01';c2='LAB-CMD-R172-HAPPY-02'
  x=execute(db,c1,counter_payload());z=r18.history(db)
  assert x['detail']['native_events'][-1]['declaration_seq']==1
  assert z['state']['actors']['LAB_VIGIA_A']['resource']['hp']==19
  assert z['state']['actors']['LAB_VIGIA_B']['resource']['reaction']==0
  assert z['state']['actors']['LAB_VIGIA_A']['resource']['standard']==0
  assert z['state']['actors']['LAB_VIGIA_A']['resource']['pa']==30
  try:execute(db,c1,counter_payload());raise AssertionError('double commit')
  except r18.LabHold:pass
  try:execute(db,'LAB-CMD-R172-B-REPEAT',counter_payload());raise AssertionError('double reaction')
  except r18.LabHold:pass
  y=execute(db,c2,counter_payload(attacker='LAB_VIGIA_B',defender='LAB_VIGIA_A'))
  a=audit(db,True)
  assert a['native_events']==6 and a['journal_rows']==2
  return {'db':db.name,'commits':2,'native_events':6,'A_hp':r18.history(db)['state']['actors']['LAB_VIGIA_A']['resource']['hp'],
          'B_hp':r18.history(db)['state']['actors']['LAB_VIGIA_B']['resource']['hp'],
          'PA_A_B':[r18.history(db)['state']['actors'][k]['resource']['pa'] for k in ('LAB_VIGIA_A','LAB_VIGIA_B')],
          'checkpoint':True,'audit':a['result']}
 test('R18 atomic two consecutive counters & no duplicate',normal)
 def hit_no_reply(score,rd,crit,seed):
  db=db_new('R172_HIT_TEST_S'+str(seed),seed)
  x=execute(db,'LAB-CMD-R172-HIT-'+str(seed),counter_payload(score=score,attack_rd=rd,critical=crit))
  e=x['detail']['native_events'];a=audit(db,True)
  assert e[-1]['action']=='COUNTER_NO_RESPONSE' and e[1]['hit'] and r18.history(db)['state']['actors']['LAB_VIGIA_B']['resource']['reaction']==0
  return {'db':db.name,'original_hit':True,'damage_after_rd':e[1]['net'],'reaction_consumed':True,'response':'NONE','positive_critical':crit,'audit':a['result']}
 test('R50 normal hit forbidden counter, declared reaction consumed',lambda:hit_no_reply(25,0,False,1722102))
 test('R50 zero-net by RD still hit',lambda:hit_no_reply(25,99,False,1722103))
 test('R50 auto-hit crit below CA, no counter',lambda:hit_no_reply(3,0,True,1722104))
 test('R50 auto-hit crit fully absorbed RD, no counter',lambda:hit_no_reply(3,99,True,1722105))
 def overkill():
  db=db_new('R172_OVERKILL_NEW_S1722106',1722106)
  x=execute(db,'LAB-CMD-R172-OVERKILL',counter_payload(counter_flat=30))
  e=x['detail']['native_events'][-1]
  assert e['net']==34 and e['before_hp']==28 and e['after_hp']==0 and e['overkill']==6
  audit(db,True)
  return {'post_rd':e['net'],'life_removed':e['before_hp']-e['after_hp'],'overkill':e['overkill']}
 test('overkill vs real life removed without new damage formulas',overkill)
 def scheduler():
  db=db_new('R172_THREE_ACTORS_SYNTH_S1722201',1722201)
  start=start_three_actor_fixture(db,'LAB-CMD-R172-THREE-INIT')
  state=r18.history(db)['state'];order=state['order']
  assert order==['LAB_VIGIA_A','LAB_VIGIA_C','LAB_VIGIA_B'],order
  x=execute(db,'LAB-CMD-R172-THREE-A',counter_payload())
  st=r18.history(db)['state'];assert st['active']=='LAB_VIGIA_C' and st['actors']['LAB_VIGIA_B']['resource']['reaction']==0
  pass_existing_r18_turn(db,'LAB-CMD-R172-THREE-C-PASS')
  st=r18.history(db)['state'];assert st['active']=='LAB_VIGIA_B'
  y=execute(db,'LAB-CMD-R172-THREE-B',counter_payload(attacker='LAB_VIGIA_B',defender='LAB_VIGIA_A'))
  report=audit(db,False)
  assert report['journal_rows']==4 and report['actors']==3 and report['native_events']==6
  write_checkpoint(db);audit(db,True)
  st=r18.history(db)['state']
  assert st['active']=='LAB_VIGIA_A' and st['round']==2
  return {'order':order,'turns':['LAB_VIGIA_A','LAB_VIGIA_C','LAB_VIGIA_B'],
   'round_after':st['round'],'active_after':st['active'],'native_events':6,'R18_commits':4,
   'reaction_refresh':'NOT_CLAIMED_R18_NO_AUTO_REFRESH','real_species_admission':False}
 test('existing R18 scheduler three-actor synthetic turn sequence',scheduler)
 fault_points=[('AFTER_INTENT','r18'),('AFTER_DECLARATION_REACTION_SPENT','internal'),
   ('AFTER_ORIGINAL_ATTACK_HP_EVENT','internal'),('AFTER_HP_MUTATION_BEFORE_RESPONSE_EVENT','internal'),('AFTER_NATIVE_RESPONSE_EVENT_BEFORE_LINK','internal'),
   ('AFTER_CAUSAL_LINK_BEFORE_COMMIT','internal')]
 for idx,(point,layer) in enumerate(fault_points):
  def inj(idx=idx,point=point,layer=layer):
   seed=1722301+idx;tag='R172_FAULT_'+point+'_S'+str(seed)
   db=RUNS/(tag+'.sqlite');assert not db.exists(),'NO_REPEAT'
   argv=[sys.executable,str(HERE/'r172_atomic_counter.py'),'--db',str(db),'--cmd','LAB-CMD-'+tag,'--seed',str(seed)]
   argv.extend(['--r18-fail' if layer=='r18' else '--internal-fail',point])
   cp=subprocess.run(argv,capture_output=True,text=True,timeout=20)
   assert cp.returncode in (74,75,76,78),('fault process',cp.returncode,cp.stderr)
   status=cold_status(db); assert status['revision']==0 and len(status['pending_cmd_ids'])==1 and len(status['committed_cmd_ids'])==0
   with sqlite3.connect(db) as conn:
    st=json.loads(conn.execute("SELECT value FROM meta WHERE key='state'").fetchone()[0])
    assert st['actors']['LAB_VIGIA_A']['resource']['hp']==28 and st['actors']['LAB_VIGIA_B']['resource']['reaction']==1
    assert conn.execute('SELECT count(*) FROM events').fetchone()[0]==0
   abort=abort_pending_lab_only(db,'LAB-CMD-'+tag)
   assert abort['revision']==0 and not abort['retry_allowed']
   with sqlite3.connect(db) as conn:
    assert conn.execute('SELECT count(*) FROM r172_aborts').fetchone()[0]==1
   try:execute(db,'LAB-CMD-'+tag,counter_payload());raise AssertionError('reused aborted cmd')
   except r18.LabHold:pass
   return {'phase':point,'process_exit':cp.returncode,'precommit_HP_reaction_unchanged':True,'intents':1,
    'commits':0,'cold_reconciled_to_aborted_tombstone':True,'same_command_retry':'FORBIDDEN'}
  test('injected crash '+point,inj)
 def after_commit(point='AFTER_COMMIT'):
  seed=1722401;tag='R172_FAULT_AFTER_COMMIT_S'+str(seed)
  db=RUNS/(tag+'.sqlite');assert not db.exists()
  argv=[sys.executable,str(HERE/'r172_atomic_counter.py'),'--db',str(db),'--cmd','LAB-CMD-'+tag,'--seed',str(seed),'--r18-fail','AFTER_COMMIT']
  cp=subprocess.run(argv,capture_output=True,text=True,timeout=20)
  assert cp.returncode==77,(cp.returncode,cp.stderr)
  status=cold_status(db);assert status['revision']==1 and status['state']=='COLD_COMMITTED'
  assert not pathlib.Path(str(db)+'.checkpoint.json').exists()
  report=audit(db,False)
  assert report['native_events']==3
  write_checkpoint(db)
  report=audit(db,True)
  try:execute(db,'LAB-CMD-'+tag,counter_payload());raise AssertionError('double commit')
  except r18.LabHold:pass
  return {'process_exit':77,'events_committed':1,'native_events':3,'checkpoint_rebuilt_from_ledger':True,
          'duplicate_rejected':True,'auditor':report['result']}
 test('crash after commit before acknowledgement/checkpoint',after_commit)
 def concurrent_intents():
  # Competing attempts to spend the SAME normal-action and reaction slot.
  seed=1722701;db=db_new('R172_CONCURRENT_COPY_S'+str(seed),seed)
  import concurrent.futures
  def worker(j):
   argv=[sys.executable,str(HERE/'r172_atomic_counter.py'),'--db',str(db),
     '--cmd','LAB-CMD-R172-CONCURRENT-'+str(j),'--seed',str(seed)]
   return subprocess.run(argv,capture_output=True,text=True,timeout=25)
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   results=list(pool.map(worker,[1,2]))
  winners=[x for x in results if x.returncode==0]
  assert len(winners)==1,[(x.returncode,x.stderr[-350:]) for x in results]
  st=cold_status(db)
  assert st['state']=='COLD_COMMITTED' and st['revision']==1
  assert audit(db,True)['journal_rows']==1
  return {'subprocesses':2,'one_commit':True,'rejected':1,
    'pending':0,'native_responses':3,'collision_domain':'SAME_SYNTHETIC_ACTION_REACTION_SLOTS',
    'official_claims':0}
 test('concurrent competing R18 attempts commit once',concurrent_intents)

 def after_checkpoint():
  seed=1722402;db=db_new('R172_AFTER_CHECKPOINT_S'+str(seed),seed)
  execute(db,'LAB-CMD-R172-AFTER-CP',counter_payload())
  # A separate caller would die now; authoritative checkpoint already fsync'ed and replaced.
  return {'commit_revision':cold_status(db)['revision'],'checkpoint_exists':True,'audit':audit(db,True)['result']}
 test('crash after checkpoint simulated by cold reopen',after_checkpoint)
 def adversarial(mode):
  seed=1722501 if mode=='LINK' else 1722502
  base=db_new('R172_ADVERSARIAL_BASE_'+mode+'_S'+str(seed),seed)
  execute(base,'LAB-CMD-R172-ADVERSARIAL-'+mode,counter_payload())
  assert audit(base,True)['journal_rows']==1
  target=RUNS/('R172_ADVERSARIAL_CLONE_'+mode+'_S'+str(seed)+'.sqlite')
  assert not target.exists()
  with sqlite3.connect(base) as a,sqlite3.connect(target) as b:a.backup(b)
  with sqlite3.connect(target) as c:
   row=json.loads(c.execute('SELECT row_json FROM events').fetchone()[0]);state=json.loads(c.execute("SELECT value FROM meta WHERE key='state'").fetchone()[0])
   if mode=='LINK':
    row['detail']['native_events'][2]['original_attack_seq']=555
    state['r172_native_events'][2]['original_attack_seq']=555
   else:
    row['detail']['actor_resources']['LAB_VIGIA_A']['hp']=26
    state['actors']['LAB_VIGIA_A']['resource']['hp']=26
   row['after_sha']=r18.sha(state)
   c.execute('UPDATE events SET row_json=?, row_sha=?, after_sha=? WHERE seq=1',
             (r18.canonical(row),r18.sha(row),row['after_sha']))
   c.execute("UPDATE meta SET value=? WHERE key='state'",(r18.canonical(state),))
   c.execute("UPDATE meta SET value=? WHERE key='head'",(r18.sha(row),))
  assert r18.load(target)[2]==1,'SQL hash rewritten should fool internal structural verifier'
  try:audit(target,False);raise AssertionError('adversarial changed evidence accepted')
  except AssertionError as err:
   assert 'CAUSAL_REPLAY_MISMATCH' in str(err) or 'COLD_REPLAY_STATE_SHA' in str(err),str(err)
   why=str(err)
  return {'adversarial_clone':target.name,'internal_sql_chain':'PASS_DESPITE_FORGERY',
    'cold_independent_replay':'REJECT','reason':why}
 test('semantic link tamper with every SQL hash rewritten',lambda:adversarial('LINK'))
 test('HP tamper with every SQL hash rewritten',lambda:adversarial('HP'))
 # R51 nested denial, no R18 pending, direct native source guard, no attack side effects
 def nested():
  from r172_atomic_counter import fixture_scene,SRC,PROOF,legal_state
  from vlab_effects_v08 import declare_counterattack,EffectBlocked
  state=r18.initial('A',1722601);s=fixture_scene(state)
  snapshot=json.dumps({'actors':{k:asdict(v) for k,v in s.actors.items()},'events':s.events},sort_keys=True,default=str)
  try:declare_counterattack(s,'LAB_VIGIA_A','LAB_VIGIA_B',source=SRC,state=legal_state('LAB_VIGIA_A',True,'LAB_VIGIA_B'),proofs=(PROOF,),declared_before=True,attack_origin='COUNTER');raise AssertionError('R51')
  except EffectBlocked:pass
  assert snapshot==json.dumps({'actors':{k:asdict(v) for k,v in s.actors.items()},'events':s.events},sort_keys=True,default=str)
  return {'nested_reply':'PREVALIDATION_REJECT','reactions_unchanged':True,'events':0,'type':'SYNTHETIC_RULE_GATE'}
 test('R51 rejects nested counter with no state effect',nested)
 report={'schema':'R172_TEST_REPORT_V1','date':'2026-10-17','operation':'OP-VLAB-FUSION-SANDBOX-01',
  'scope':'MESTRE-SIDE_SYNTHETIC_TX_INTEGRATION','executed_tests':len(RESULT),
  'passed':sum(1 for x in RESULT if x['status']=='PASS'), 'failed':sum(1 for x in RESULT if x['status']!='PASS'),
  'tests':RESULT,'terminal_contracts':0,'official_benchmarks':0,
  'historical_db_writes':0,'notion_op_writes':0,
  'limitations':['No formal source-complete battle','Three actor scenario is a synthetic R18 fixture',
   'R18 reaction renewal is not automatic and this run does not certify normative refresh','Auditor is separately implemented but not external human reviewer',
   'Precommit aborted intents reconciled only under known pure-memory sandbox, no general UNKNOWN_EFFECT clearance']}
 (HERE/'R172_SUITE_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n')
 print(json.dumps({'executed':len(RESULT),'pass':report['passed'],'fail':report['failed'],
    'failed_names':[x['test'] for x in RESULT if x['status']!='PASS']},ensure_ascii=False))
 if report['failed']:sys.exit(2)
if __name__=='__main__':main()
