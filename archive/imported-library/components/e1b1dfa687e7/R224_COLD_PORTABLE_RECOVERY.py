"""R224 portable recovery: validate hashes, CRC (when archive), READ-ONLY SQLite including UNKNOWN intents."""
from pathlib import Path
import argparse,hashlib,json,sys,subprocess,tempfile,zipfile

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root):
 root=Path(root);mapping=json.loads((root/'SHA256_MANIFEST.json').read_text())
 actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and x.name!='SHA256_MANIFEST.json' and '__pycache__' not in x.parts}
 assert set(mapping)==actual,('MANIFEST_COVERAGE',len(mapping),len(actual))
 for f,h in mapping.items():assert sha(root/f)==h,('HASH_MISMATCH',f)
 src=(root/'code/r224_independent_pair_audit.py').read_text()
 assert 'import vlab_effects' not in src and 'event_commit(' not in src
 r=subprocess.run([sys.executable,str(root/'code/r224_independent_pair_audit.py')],cwd=root,capture_output=True,text=True,timeout=120)
 assert r.returncode==0,(r.stdout,r.stderr)
 m=json.loads(r.stdout)['metrics'];assert m['paired_seed_units']==20 and m['unknown_quarantine_sqlite']==2 and m['valid_terminal_sqlite']==38
 return {'status':'PASS_R224_COLD_PORTABLE_STRICT_HOLD_VS_TEST_FLOOR','hashes':len(mapping),**m}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--archive');a.add_argument('--root');v=a.parse_args()
 if v.archive:
  with tempfile.TemporaryDirectory(prefix='r224_cold_') as d:
   with zipfile.ZipFile(v.archive) as z:assert z.testzip() is None,'BAD_CRC';z.extractall(d)
   print(json.dumps(verify(d),indent=2))
 else:print(json.dumps(verify(v.root),indent=2))
