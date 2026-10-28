"""Cold R172 recovery from standalone sealed ZIP. NO gameplay combat or effect rerun.
It replays technical event calculations from stored commands only in a temporary copy;
no existing DB is updated, no historical RUN-ID retried.
Usage: python R172_COLD_PORTABLE_RECOVERY.py sealed_r172.zip receipt.json
"""
import os,sys,hashlib,json,zipfile,sqlite3,tempfile,pathlib,collections
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def verify_zip(zpath, receipt):
 zpath=Path(zpath).resolve();receipt=Path(receipt).resolve()
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None,'ZIP_CRC'
  names=z.namelist();assert len(names)==len(set(names)),'DUPLICATE_ENTRY'
  assert all(not p.startswith('/') and '..' not in pathlib.PurePosixPath(p).parts for p in names),'TRAVERSAL'
  manifest=json.loads(z.read('R172_SHA256_MANIFEST.json'))
  expected=manifest['files'];assert len(expected)==len(names)-1,(len(expected),len(names))
  assert set(expected)==set(names)-{'R172_SHA256_MANIFEST.json'},'MANIFEST_SET'
  for n,h in expected.items():assert sha(z.read(n))==h,('HASH',n)
  with tempfile.TemporaryDirectory(prefix='VLAB_R172_COLD_') as dirpath:
   root=Path(dirpath);z.extractall(root)
   assert sha((root/'deps/native_v081_controlled/vlab_effects_v08.py').read_bytes())=='4502665346741ff231b79659d881bdac252112f42e91bce7d0747f3e18344dc1'
   assert sha((root/'deps/r61_extracted/work/fusion_stage12/vlab_r18_interactive.py').read_bytes())=='f1336caa0255ab2c6d9e20f2f3f87edf682e97fe6d04c1e2373518d5ae74d368'
   assert sha((root/'deps/R171_counter_causal_guard/r171_counter_causal.py').read_bytes())=='0823ce28be9f48fa415a173775006663e17e0c1ba4f2a0977dcf2e98a749a9ab'
   report=json.loads((root/'r172_work/R172_SUITE_REPORT.json').read_text())
   assert report['executed_tests']==19 and report['passed']==19 and report['failed']==0,'NEW_REGRESSION'
   old=json.loads((root/'evidence/R170_SUCCESSOR_COLD_RECEIPT.json').read_text())
   assert old['result']=='PASS_COLD_INDEPENDENT_RECOVERY' and old['zip_sha256']=='ab34cad5a0b26455f9a0ad659735867fa3a9a430e526e08fa2dcd6a13b776ed0'
   r171=json.loads((root/'evidence/R171_REPORT.json').read_text())
   assert r171['tests_passed']==7 and r171['test_failures']==0
   contract=json.loads((root/'R172_CONTRACT_DELTA_MESTRE_ONLY.json').read_text())
   assert len(contract['rows'])==17 and contract['terminals_after']==0 and contract['benchmark_official_cells_after']==0
   sys.path.insert(0,str(root/'r172_work'))
   from r172_independent_replay_auditor import audit
   from r172_atomic_counter import r18
   banks=sorted((root/'evidence/runs_test_v3').glob('*.sqlite'))
   assert len(banks)==20,len(banks)
   legitimate=[];aborted=[];adversarial=[];total=collections.Counter()
   for db in banks:
    name=db.name
    with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as con:
     assert con.execute('pragma integrity_check').fetchone()[0]=='ok',('SQLITE',name)
     rev=con.execute('SELECT COUNT(*) FROM events').fetchone()[0]
     pcount=con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]
     assert pcount==0,('UNRECONCILED_INTENT',name)
     if 'FAULT_' in name and 'AFTER_COMMIT' not in name:
      ab=con.execute('SELECT cmd_id,status FROM r172_aborts').fetchall()
      assert len(ab)==1 and rev==0 and ab[0][1]=='ABORTED_PURE_MEMORY_NO_EFFECT_RETRY_FORBIDDEN',name
      state=json.loads(con.execute("SELECT value FROM meta WHERE key='state'").fetchone()[0])
      assert state['actors']['LAB_VIGIA_A']['resource']['hp']==28 and state['actors']['LAB_VIGIA_B']['resource']['reaction']==1
      aborted.append(name);continue
    if 'ADVERSARIAL_CLONE_' in name:
     # The internal R18 chain is valid after malicious full hash recomputation;
     # the separately implemented semantic cold replay must find the lie.
     assert r18.load(db)[2]==1,'STRUCTURAL_REHASH_EXPECTED'
     try:audit(db);raise AssertionError('FORGED_EVIDENCE_ACCEPTED:'+name)
     except AssertionError as exc:
      if str(exc).startswith('FORGED_EVIDENCE_ACCEPTED'):raise
      adversarial.append({'db':name,'rejected':'PASS','reason':str(exc)})
     continue
    a=audit(db,check_checkpoint=True)
    total['commits']+=a['journal_rows'];total['native_events']+=a['native_events']
    legitimate.append({'db':name,'revision':a['journal_rows'],'native_events':a['native_events'],'head':a['head']})
   assert (len(legitimate),len(aborted),len(adversarial))==(12,6,2)
   assert total['commits']==16 and total['native_events']==42,total
   kinds=collections.Counter()
   for entry in legitimate:
    db=root/'evidence/runs_test_v3'/entry['db']
    for e in r18.history(db)['events']:kinds[e['kind']]+=1
   assert kinds=={'R172_COUNTER_EXCHANGE':14,'R172_THREE_ACTOR_START':1,'R172_EXISTING_R18_PASS':1},kinds
   result={'as_of':'2026-10-17','result':'PASS_R172_COLD_PORTABLE_RECOVERY','operation':'OP-VLAB-FUSION-SANDBOX-01',
    'R172_zip_sha256':sha(zpath.read_bytes()),'entries':len(names),'manifest_entries_verified':len(expected),
    'R170_prior_integrity_receipt':'PASS_REOPENED','R171_7_tests_receipt':'PASS_REOPENED',
    'R172_reported_tests':'19/19 PASS','physical_independent_cold_replay_banks':len(legitimate),
    'R172_new_valid_sqlite_commits':total['commits'],'new_counter_transactions':kinds['R172_COUNTER_EXCHANGE'],
    'scheduler_control_commits':kinds['R172_THREE_ACTOR_START']+kinds['R172_EXISTING_R18_PASS'],
    'counter_chain_native_events':total['native_events'],'aborted_pure_memory_intents':len(aborted),
    'tampered_hash_valid_clones_rejected':len(adversarial),
    'R170_native_source_sha_verified':True,'R18_source_sha_verified':True,'R171_source_sha_verified':True,
    'original_R170_R171_engines_modified':False,'original_historical_battles_rerun':False,
    'R172_experimental_tests_rerun_on_readback':False,'formal_external_human_audit':False,
    'terminal_contracts':0,'official_benchmark_cells':0,'canon_writes':0,'party_writes':0,
    'writer':'UNVERIFIED_PRODUCTION_HOLD','legitimate_ledgers':legitimate,'tampered_clones':adversarial}
   receipt.parent.mkdir(exist_ok=True,parents=True)
   receipt.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
   return result
if __name__=='__main__':
 zpath,receipt=sys.argv[1:3];r=verify_zip(zpath,receipt)
 print(json.dumps({k:v for k,v in r.items() if k not in ('legitimate_ledgers','tampered_clones')},indent=2,ensure_ascii=False))
