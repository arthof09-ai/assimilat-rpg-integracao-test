"""Cold ZIP + independent source/SQLite audit, NO executor imports or battle replay."""
import argparse,hashlib,json,zipfile,tempfile,subprocess,sys
from pathlib import Path
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root):
 root=Path(root);m=json.loads((root/'SHA256_MANIFEST.json').read_text())
 actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and x.name!='SHA256_MANIFEST.json'}
 if set(m)!=actual:raise AssertionError('MANIFEST_ENTRY_MISMATCH')
 for f,h in m.items():
  if digest(root/f)!=h:raise AssertionError('SHA256_MISMATCH:'+f)
 src=(root/'code/r226_independent_sqlite_pair_audit.py').read_text()
 if 'import vlab_effects' in src or 'import r226_manopla_pair_native' in src or 'event_commit(' in src:raise AssertionError('NOT_INDEPENDENT')
 p=subprocess.run([sys.executable,str(root/'code/r226_independent_sqlite_pair_audit.py')],cwd=root,capture_output=True,text=True,timeout=80)
 if p.returncode:raise AssertionError('READONLY_AUDIT_FAIL:'+p.stdout+' '+p.stderr)
 obj=json.loads(p.stdout)
 if obj['arms']!=16 or obj['pairs']!=8 or obj['item_activations']!=7 or obj['magic_hp_total']!=187:raise AssertionError('EXPECTED_RESULTS_CHANGED')
 report=json.loads((root/'evidence/reports/R226_NEGATIVE_AND_ADVERSARIAL.json').read_text())
 if len(report['hash_rebuilt_adversarial'])!=4 or len(report['in_memory_negative_tests'])!=4:raise AssertionError('CONTROL_EVIDENCE_MISSING')
 return {'status':'PASS_R226_COLD_SOURCE_BOUND_SEMICANON_PAIR_TEST_ONLY','manifest_hashes':len(m),**{k:obj[k] for k in ('arms','pairs','commits','events','hits','item_activations','item_pa_total','magic_hp_total','slow_expirations','historical_replays')}}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--archive');a.add_argument('--root');v=a.parse_args()
 if v.archive:
  with tempfile.TemporaryDirectory(prefix='R226_COLD_') as path:
   with zipfile.ZipFile(v.archive) as z:
    if z.testzip() is not None:raise AssertionError('CRC_FAIL')
    z.extractall(path)
   print(json.dumps(verify(path),ensure_ascii=False,indent=2))
 else:print(json.dumps(verify(v.root),ensure_ascii=False,indent=2))
