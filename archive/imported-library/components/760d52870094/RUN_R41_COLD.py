#!/usr/bin/env python3
"""Cold recovery runner. Only local Python LAB TEST. Parent copies verified SHA256."""
import hashlib,subprocess,sys,zipfile,os,tempfile,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
PARENTS={'CRAFT_PA_R40_RI_RE_R48_ORIGINAL_TEST_20261020.zip':'899ea34d81025356af26b462272273244c8405f05493f6f664aa05ad9d481f11',
         'PA_R39_CONSULTOR_EVIDENCIAS_QUALIFICADAS_TEST_20261020.zip':'daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32'}
EXPECTED_R48={'r48_factory.py':'872dc5bf1e588a9ba6f4c45421a4dddbbe7d261842a4e951fd684bfc374c6801',
 'r48_store.py':'e6f684e80e0d5c95dff8ea94cbae985b0a8e046b48886d593d6e49534f046bd1'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def extract_zip(p,d):
 with zipfile.ZipFile(p) as z:
  if z.testzip():raise RuntimeError('CRC_FAIL:'+p.name)
  for n in z.namelist():
   q=Path(n)
   if n.startswith('/') or '..' in q.parts:raise RuntimeError('UNSAFE_ZIP_PATH')
  z.extractall(d)
def call(argv,cwd,env=None):
 p=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('FAILED:'+repr(argv)+'\n'+(p.stdout+p.stderr)[-2000:])
 return p.stdout+p.stderr

def main():
 for n,h in PARENTS.items():
  if sha(R/'parents'/n)!=h:raise RuntimeError('ORIGINAL_PARENT_CHANGED:'+n)
 with tempfile.TemporaryDirectory(prefix='R41_COLD_') as tmp:
  root=Path(tmp);extract_zip(R/'parents'/'CRAFT_PA_R40_RI_RE_R48_ORIGINAL_TEST_20261020.zip',root)
  r48=root/'R48_ORIGINAL'
  if not r48.exists():raise RuntimeError('R48_TREE_MISSING')
  for n,h in EXPECTED_R48.items():
   if sha(r48/n)!=h:raise RuntimeError('R48_ORIGINAL_SHA_MISMATCH:'+n)
  src=root/'R41_SRC';shutil.copytree(R/'code',src)
  env={**os.environ,'R41_R48_DIR':str(r48)}
  checks=call([sys.executable,'-m','unittest','discover','-s',str(src),'-p','test_*.py','-v'],src,env)
  if 'Ran 33 tests' not in checks or 'OK' not in checks:raise RuntimeError('R41_DENOMINATOR_CHANGED')
  r48tests=call([sys.executable,'-m','unittest','discover','-s','tests','-v'],r48)
  if 'Ran 40 tests' not in r48tests or 'OK' not in r48tests:raise RuntimeError('R48_BASELINE_INVALID')
  r39=root/'R39';r39.mkdir();extract_zip(R/'parents'/'PA_R39_CONSULTOR_EVIDENCIAS_QUALIFICADAS_TEST_20261020.zip',r39)
  r39replay=call([sys.executable,'RUN_R39_RELEASE.py'],r39)
  j=json.loads((r39/'RECIBO_REPLAY_R39.json').read_text())
  if j['total_suites_formal_tests']!=510:raise RuntimeError('PA_R39_CHANGED')
  after={n:sha(r48/n) for n in EXPECTED_R48}
  if after!=EXPECTED_R48:raise RuntimeError('R48_MUTATED')
  gold=json.loads((src/'RE_E0_26_INDEX_FROM_R40.json').read_text())
  from_metrics={'n_gold_re_labels':len(gold['techniques']),'n_mechanics_extracted_independently':0,
                'n_frozen_blind_rank_predictions':0,'mechanical_accuracy':None}
  result={'status':'PASS_LAB_R41_COLD','original_hashes_unchanged':after,
          'r39_fresh_tests':510,'r48_fresh_tests':40,'r41_fresh_tests':33,'suite_tests_total':583,
          'benchmark':from_metrics,'physical_products':0,'rc5':False,'craft_f5':'RED',
          'writer_lease_fencing_prod':'NOT_DEMONSTRATED','tee_official_craft':'NOT_EXECUTED',
          'target':'LAB-CRAFT-VIGILIA-BOREAL-20261020-001'}
  return result
if __name__=='__main__':print(json.dumps(main(),indent=2,ensure_ascii=False))
