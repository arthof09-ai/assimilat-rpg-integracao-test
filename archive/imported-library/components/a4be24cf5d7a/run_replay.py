import json,subprocess,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test(cmd):
 p=subprocess.run([sys.executable,*cmd],cwd=ROOT,capture_output=True,text=True)
 print(' '.join(cmd), 'EXIT',p.returncode)
 if p.returncode:
  print(p.stdout);print(p.stderr);raise SystemExit(p.returncode)
 s=p.stdout+p.stderr
 import re
 match=re.search(r'Ran (\d+) tests',s)
 print('TEST_COUNT',match.group(1) if match else 'NA')
 return int(match.group(1)) if match else 0

test(['code/verify_manifest.py'])
new=test(['-m','unittest','discover','-s','tests','-p','test_*.py'])
old=test(['-m','unittest','discover','-s','baseline','-p','test_source_guard.py'])
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('craftdelta',str(ROOT/'code/readiness_delta.py'));m=module_from_spec(spec);spec.loader.exec_module(m)
expected=m.run_actual_readonly()
report=json.loads((ROOT/'outputs/ACTUAL_READONLY_RESULT.json').read_text())
assert report==expected,'ACTUAL_READONLY_RESULT_NONREPRODUCIBLE'
assert not report['source_guard_result']['authorization_to_apply']
assert report['h23']['h23a']=='HOLD_NO_APPLICATION'
assert report['production']=='HOLD' and report['f5']=='RED'
assert report['causal_controls']['count']==16 and report['causal_controls']['observations']==0
assert not report['R48_replayed'] and report['official_recipe_writes']==0
print('PASS_H23_READINESS_COLD_REPLAY',new,old,'NO_MAGIC_NO_STOCK_NO_R48_NO_PARTY')
