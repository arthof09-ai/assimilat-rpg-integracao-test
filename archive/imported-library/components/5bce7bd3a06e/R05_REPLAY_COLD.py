"""Independent offline cold replay of R05 with intact R04/R39/R28/R27/R26 sources.

Run within an extracted R05 package. No Notion or Party I/O, no productive
writes, no persistent fixture, no external network and no new PA engine.
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE='SOURCE_R04_FROZEN.zip'
SHA_R04='927f3483a4603d9aeae4c17a92772c70bc5936f70908739a61a784d4c03323aa'
SHA_R39='daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32'
SHA_R28='68acc4405250cbf03a89924fa4df1f3d36586f26a5a903610c6600e8f26a391e'

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def extract(p:Path,dst:Path):
 dst.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None, 'BAD_ZIP:'+str(p)
  names=z.namelist();assert len(names)==len(set(names)),'DUPLICATE_ZIP_NAMES'
  for n in names:
   t=(dst/n).resolve();assert t.is_relative_to(dst.resolve()) and not n.startswith('/'),'TRAVERSAL:'+n
  z.extractall(dst)

def verify():
 data=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
 for fname,meta in data['files'].items():
  file=ROOT/fname
  assert file.is_file(), 'MISSING_IN_MANIFEST:'+fname
  b=file.read_bytes()
  assert len(b)==meta['bytes'] and sha(b)==meta['sha256'], 'SHA_MISMATCH:'+fname
 assert sha((ROOT/SOURCE).read_bytes())==SHA_R04
 return len(data['files'])

def replay():
 count=verify()
 with tempfile.TemporaryDirectory(prefix='r05_pa_readonly_') as tm:
  d=Path(tm);r04=d/'R04';extract(ROOT/SOURCE,r04)
  nested=r04/'SOURCE_R39_FROZEN.zip';assert sha(nested.read_bytes())==SHA_R39
  r39=d/'R39';extract(nested,r39)
  r29=d/'R29';extract(r39/'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip',r29)
  nativezip=r29/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip'
  assert sha(nativezip.read_bytes())==SHA_R28
  r28=d/'R28';extract(nativezip,r28)
  provider=r28/'provider_r27'
  assert (provider/'engine_r26/parecer_semicanonico_r26.py').is_file()
  env=os.environ.copy()
  env['R05_R27_ORIGINAL']=str(provider)
  env['R05_R03_ORIGINAL']=str(ROOT/'R03_DEPENDENCIES')
  r=subprocess.run([sys.executable,'-m','unittest','-q','test_r05_catalog'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=75)
  stdout=r.stdout+'\n'+r.stderr
  m=re.search(r'Ran\s+(\d+)\s+tests',stdout)
  assert r.returncode==0 and m and int(m.group(1))==20 and re.search(r'^OK$',stdout,re.M) and 'FAILED' not in stdout, stdout[-2600:]
  # R05 test calls run_native_roster and writes results deterministically; compare
  # to the version stored in the signed manifest (verified before the run).
  data=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
  expected=data['files']['R05_RESULTS_REPRODUCIBLE.json']['sha256']
  actual=sha((ROOT/'R05_RESULTS_REPRODUCIBLE.json').read_bytes())
  assert actual==expected, 'R05_RECOMPUTED_RESULT_DIVERGED'
  report=json.loads((ROOT/'R05_RESULTS_REPRODUCIBLE.json').read_text())
  assert report['source_count']==12
  assert report['native_historical_consultations']==12
  assert report['native_prospective_incomplete_consultations']==12
  assert report['conditional_variants']==6
  assert report['rank_only_canary']['safe_scenario_total'] is None
  assert report['production_status']=='HOLD'
  return {'result':'PASS','scope':'MASTER_ONLY_TEST','manifest_pass_files':count,
      'unit_tests':20,'source_pages':12,'item_catalog_pages':4,'personal_mestre_mirror_pages':8,
      'historic_scenarios':12,'incomplete_scenarios':12,'parametric_attribute_scenarios':6,
      'rank_only_canary':1,'source_R04_sha256':SHA_R04,
      'source_R39_sha256':SHA_R39,'source_R28_sha256':SHA_R28,
      'r26_r27_modified':False,'notion_writes':0,'party_writes':0,
      'production_status':'HOLD','temp_dir_cleaned_on_return':True}

if __name__=='__main__':print(json.dumps(replay(),ensure_ascii=False,indent=2,sort_keys=True))
