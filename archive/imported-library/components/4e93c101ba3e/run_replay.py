from __future__ import annotations
import json,subprocess,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(cmd):
 p=subprocess.run([sys.executable,*cmd],cwd=ROOT,capture_output=True,text=True,timeout=30)
 if p.returncode:
  print(p.stdout,p.stderr)
  raise RuntimeError('REPLAY_FAILURE '+str(cmd))
 return p.stdout+p.stderr

print(run(['code/verify_manifest.py']).strip())
out=run(['-m','unittest','discover','-s','tests','-p','test_*.py'])
assert 'Ran 75 tests' in out and '\nOK' in out,(out[-200:])
import importlib.util
p=ROOT/'code/craft_batch_qa.py'
s=importlib.util.spec_from_file_location('craft_batch_qa',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
actual=m.full_report()
assert actual==json.loads((ROOT/'results/live_documentary_readonly.json').read_text())
assert m.test_linear_demand_properties(20)==json.loads((ROOT/'results/synthetic_arithmetic_stress.json').read_text())
assert actual['literal_qa']['aggregate_exact_matches']==18
assert actual['literal_qa']['aggregate_bom_items']==24
assert actual['portfolio_four_oil_uses']['oil_units_required']==4
assert not actual['reflexo_without_oil']['authorization_to_apply']
assert actual['r48_new_actions']==0 and actual['production']=='HOLD'
assert not actual['p2_guard']['authorization_to_apply']
print('REPLAY PASS / 75 UNIT / 8000 SYNTHETIC VECTORS / 18 OF 24 EXACT MATCH / OIL NEED FOUR / NO MAGIC / NO R48')
