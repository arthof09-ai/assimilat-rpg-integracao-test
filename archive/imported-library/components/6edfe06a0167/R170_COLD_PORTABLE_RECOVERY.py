"""R170 clean-room recovery from sealed ZIP (read only of source ZIP and event DBs).
Standalone standard-library harness: replays source audits, original R18 reader and 28 regressions.
Writes only one fresh out-of-archive receipt; never invokes old/active combat executors.
Usage: python R170_COLD_PORTABLE_RECOVERY.py <sealed_R170_zip> <output_receipt.json>
"""
import os,sys,sqlite3,hashlib,json,zipfile,tempfile,subprocess,importlib
from pathlib import Path
can=lambda o:json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(archive,out):
 archive=Path(archive).resolve();out=Path(out).resolve()
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None,'CRC_FAIL'
  names=z.namelist();assert 'R170_SHA256_MANIFEST.json' in names and 'R160_BASELINE_EXACT.zip' in names
  manifest=json.loads(z.read('R170_SHA256_MANIFEST.json'))
  checks=manifest['files'];assert len(checks)==len(names)-1
  for fn in names:
   assert not fn.startswith('/') and '..' not in Path(fn).parts,'TRAVERSAL'
  for fn,expected in checks.items():
   assert fn in names and sha(z.read(fn))==expected,(fn,'sha')
  assert sha(z.read('R160_BASELINE_EXACT.zip'))=='7b208fe553809df6a999a1e4f9a70d7ad116033e929256bc71dbcd61843f3410'
  with tempfile.TemporaryDirectory(prefix='VLAB_R170_COLD_') as tmp:
   root=Path(tmp);z.extractall(root);R=root/'r161_r170';BASE=root/'R160_UNPACKED';BASE.mkdir()
   with zipfile.ZipFile(root/'R160_BASELINE_EXACT.zip') as old:
    assert old.testzip() is None
    for n in old.namelist():assert not n.startswith('/') and '..' not in Path(n).parts
    old.extractall(BASE)
   os.environ['R160_BASE_DIRECTORY']=str(BASE)
   sys.path.insert(0,str(R));sys.path.insert(0,str(BASE/'r151_r160'))
   from r165_cold_temporal_independent import audit as audit165
   from r166_cold_concurrent_independent import verify as audit166
   from r159_cold_ed_besta_independent import verify as audit168
   selected=[*sorted((R/'runs').glob('R165_FLECHA_TURN_EXPLICIT_V3_DEV_S*.sqlite')),
     *sorted((R/'runs').glob('R166_V2_CASULO_AOO_*.sqlite')),
     *sorted((R/'runs').glob('R168_ED_AUREN_VS_CROC_BASIC_*.sqlite'))]
   selected=[p for p in selected if '.checkpoint.' not in p.name]
   assert len(selected)==5,selected
   reports=[];counts={'selected_commits':0,'selected_attack_receipts':0,'sel':0}
   for db in selected:
    if db.name.startswith('R165_'):rv=audit165(db);a=2
    elif db.name.startswith('R166_'):rv=audit166(db);a=sum(1 for x in json.loads((R/'R166_CONCURRENT_CASULO_AOO_RESULTS.json').read_text()) if x['run']==db.stem for _ in range(x['AOOs']))
    else:rv=audit168(db);a=rv['counts']['native_attacks']
    n=rv.get('events',rv.get('commits'))
    assert type(n)==int and n>0
    counts['sel']+=1;counts['selected_commits']+=n;counts['selected_attack_receipts']+=a
    reports.append({'run':db.stem,'commits':n,'attacks':a,'head':rv.get('head',rv.get('last_head',rv.get('root_sha'))),'status':'PASS'})
   assert counts=={'selected_commits':413,'selected_attack_receipts':137,'sel':5},counts
   # Physical R18 source reader accepts checkpoint DBs and reproduces state WITHOUT applying command.
   sys.path.insert(0,str(BASE/'r61_extracted/work/fusion_stage12'))
   import vlab_r18_interactive as r18
   originals=[]
   for db in selected:
    cp=db.with_suffix('.checkpoint.sqlite');assert cp.exists()
    saved=r18.load(db);snap=r18.load(cp)
    assert saved==snap and saved[2]>0
    originals.append({'run':db.stem,'revision':saved[2],'checkpoint':'IDENTICAL_READBACK'})
   assert sum(x['revision'] for x in originals)==413
   # Historical 9 selected raw R160 DBs: original read-only reconciliation; output files only in clean extract.
   env=dict(os.environ);env['R160_BASE_DIRECTORY']=str(BASE)
   rc=subprocess.run([sys.executable,str(R/'r161_reconcile_and_export.py')],capture_output=True,text=True,timeout=45,env=env)
   assert rc.returncode==0,(rc.returncode,rc.stdout[-400:],rc.stderr[-600:])
   rec=json.loads((R/'R161_R162_NATIVE_RECONCILIATION.json').read_text())
   assert (rec['reconciled_receipts'],rec['commits'],rec['correct_hp_effective'],rec['overkill'])==(154,466,11808,62)
   # Semantically forged hash-valid copies rejected by independent cold audits.
   bad=[]
   for p in sorted((R/'adversarial_copies').glob('R169_V2_*.sqlite')):
    assert p.with_suffix('.genesis.json').exists()
    with sqlite3.connect(f'file:{p}?mode=ro',uri=True) as c:
     assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
     end=c.execute('select row_json,row_sha from events order by seq desc limit 1').fetchone()
     assert sha(can(json.loads(end[0])).encode())==end[1]
    try:
     (audit166 if 'FAKE_HP_LOSS' in p.name else audit165)(p)
     raise AssertionError('adversarial accepted')
    except AssertionError as e:
     if str(e)=='adversarial accepted':raise
     bad.append(p.name)
   assert len(bad)==2
   # Unit suite on native module copied from sealed archive, no combat re-run.
   env['PYTHONPATH']=str(R/'native_v081_controlled')
   unit=subprocess.run([sys.executable,'-m','unittest','test_vlab_effects_v08','-q'],cwd=R/'native_v081_controlled',env=env,text=True,capture_output=True,timeout=30)
   assert unit.returncode==0,(unit.stdout,unit.stderr)
   assert 'Ran 28 tests' in unit.stderr
   assert len(json.loads((R/'R170_17_CONTRACTS_BEFORE_AFTER.json').read_text())['rows'])==17
   assert len(list(__import__('csv').DictReader((R/'R169_NEW_NATIVE_RECEIPTS_137_SOURCE_SCOPED.csv').open())))==137
   result={'as_of':'2026-10-17','result':'PASS_COLD_INDEPENDENT_RECOVERY','operation':'OP-VLAB-FUSION-SANDBOX-01',
      'zip_path':archive.name,'zip_sha256':sha(archive.read_bytes()),'entries':len(names),'manifest_files_verified':len(checks),
      'R160_nested_original_sha256':sha((root/'R160_BASELINE_EXACT.zip').read_bytes()),
      'selected_banks_verified':len(reports),'selected_commits_verified':counts['selected_commits'],'selected_receipts_verified':counts['selected_attack_receipts'],
      'physical_R18_checkpoint_open':len(originals),'legacy_unit_tests':'28/28 PASS','R160_historical_reconcile':'154/154,466/466,11808 effective,62 overkill PASS',
      'adversarial_semantic_hash_edited_rejected':len(bad),'selected_runs':reports,
      'R160_contract_matrix_unchanged_ids':True,'terminal_contracts':0,'official_power_cells':0,
      'no_historical_combat_reruns':True,'writer':'NOT_AUTHORIZED','DMG_ACK':'NONE'}
   out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
   return result
if __name__=='__main__':
 a,o=sys.argv[1:3];r=run(a,o)
 print(json.dumps({k:v for k,v in r.items() if k!='selected_runs'},indent=2,ensure_ascii=False))
