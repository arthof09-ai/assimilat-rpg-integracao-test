#!/usr/bin/env python3
"""Replay portable R42, original baselines IMMUTABLE, test-only. No Notion mutations."""
import os,sys,json,hashlib,subprocess,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run_cmd(cmd,cwd,env=None):
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
 if p.returncode:raise RuntimeError('FAIL '+str(cmd)+'\n'+p.stdout[-3000:]+'\n'+p.stderr[-3000:])
 return p.stdout+'\n'+p.stderr

def main():
 m=json.loads((ROOT/'MANIFEST_R42.json').read_text())
 for rel,expected in m['files'].items():
  assert sha(ROOT/rel)==expected,('HASH_MISMATCH',rel)
 env=os.environ.copy();env['R42_R48_ORIG']=str(ROOT/'parents'/'r48_original');env['R42_R26_ENGINE']=str(ROOT/'parents'/'engine_r26')
 new=run_cmd([sys.executable,'-m','unittest','test_r42.py','-v'],ROOT,env)
 assert 'Ran 13 tests' in new and 'OK' in new
 r48=run_cmd([sys.executable,'-m','unittest','discover','-s','tests','-v'],ROOT/'parents'/'r48_original',env)
 assert 'Ran 40 tests' in r48 and 'OK' in r48
 with tempfile.TemporaryDirectory(prefix='r42_PA_regress_') as td:
  with zipfile.ZipFile(ROOT/'parents'/'PA_R39_CONSULTOR_EVIDENCIAS_QUALIFICADAS_TEST_20261020.zip') as z:z.extractall(td)
  pa=run_cmd([sys.executable,'RUN_R39_RELEASE.py'],td,env)
  p=json.loads(pa[pa.find('{'):pa.rfind('}')+1]) if '{' in pa else {}
  assert p.get('total_suites_formal_tests')==510,p
 out={'status':'PASS_R42_COLD_TEST','original_sources_verified':len(m['files']),'pa_r39_tests':510,'r48_original_tests':40,
      'r42_new_tests':13,'total_distinct_tests':563,'textual_inscription_benchmark':json.loads((ROOT/'SCORE_R42.json').read_text())['n_cases'],
      'gold_26_techniques_with_image_only':26,'technique_predictions_blind':0,'f5_official':'HOLD',
      'official_qmc05_tee':'NOT_EXECUTED','material_magic_verified':False,'no_official_writes':True}
 print(json.dumps(out,ensure_ascii=False,indent=2))
 return out
if __name__=='__main__':main()
