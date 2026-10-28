"""Portable cold recovery R218. Read-only: does NOT run any combat runner or mutate any SQLite."""
from pathlib import Path
import hashlib,json,zipfile,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from r218_independent_rolled_audit import verify,audit_one_rolled

def main():
 manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
 if not isinstance(manifest,dict) or not manifest:raise AssertionError('MANIFEST_EMPTY')
 for rel,expected in manifest.items():
  path=ROOT/rel
  if not path.is_file():raise AssertionError('FILE_MISSING '+rel)
  if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise AssertionError('SHA_MISMATCH '+rel)
 baseline=ROOT/'baseline/VLAB_R217_ORIGINAL_READ_ONLY.zip'
 if hashlib.sha256(baseline.read_bytes()).hexdigest()!='9eaa0b945f5838f1e5046c00a6bbd5ef6525c807299e4161c9a4a36ff997f666':raise AssertionError('BASELINE_R217_SHA')
 with zipfile.ZipFile(baseline) as z:
  if z.testzip() is not None:raise AssertionError('BASELINE_R217_CRC')
 result=verify(ROOT)
 adv=json.loads((ROOT/'evidence/reports/R218_ADVERSARIAL_3_OF_3.json').read_text())
 ph=hashlib.sha256((ROOT/'sources/R218_PREREG_BEFORE_NEW_COMBATS.json').read_bytes()).hexdigest()
 expected={'INIT_ROLL_FORGED':'R218_INITIATIVE_PRF_FORGED','DECLARED_ORDER_REVERSED':'R218_WRONG_SCHEDULER_ORDER','INIT_PRE_HASH_FALSE':'R218_PRE_HASH_MISMATCH'}
 for case,reason in expected.items():
  p=ROOT/'evidence/adversarial'/f'R218_ADVERSARIAL_{case}.sqlite'
  try:audit_one_rolled(p,ph,fixture_identity=('INIT_A',21831001))
  except AssertionError as e:
   if reason not in str(e):raise AssertionError('TAMPER_WRONG_REASON '+case+' '+str(e))
  else:raise AssertionError('TAMPER_ESCAPED '+case)
 if len(adv['cases'])!=3:raise AssertionError('TAMPER_DENOMINATOR')
 print('PASS_R218_COLD_PORTABLE_SOURCE_ROLLED_INITIATIVE')
 print(json.dumps({'manifest_files':len(manifest),'admitted':result['admitted'],'blocked':result['blocked'],'pairs':result['paired_independent_seeds'],'order_changed_pairs':result['pairs_order_changed'],'terminal_diff_pairs':result['pairs_terminal_HP_different'],'commits':result['commits'],'events':result['events'],'adversarial_rejected':3,'historical_fight_replays':0,'production':'HOLD'},indent=2,ensure_ascii=False))
 return result
if __name__=='__main__':main()
