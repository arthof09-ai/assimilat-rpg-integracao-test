"""Portable READ-ONLY recovery R223. Only verifies ZIP members and SQLite; no runner."""
from pathlib import Path
import argparse,hashlib,json,sys,subprocess,zipfile,tempfile

def dig(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root):
 root=Path(root)
 if not (root/'SHA256_MANIFEST.json').is_file():raise AssertionError('NO_MANIFEST')
 mapping=json.loads((root/'SHA256_MANIFEST.json').read_text())
 seen={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and x.name!='SHA256_MANIFEST.json' and '__pycache__' not in x.parts}
 assert seen==set(mapping),('ZIP_COVERAGE',len(seen),len(mapping))
 for p,h in mapping.items():assert dig(root/p)==h,('HASH',p)
 code=root/'code/r223_independent_factorial_audit.py'
 assert code.is_file()
 # Python auditor imports only sqlite3/hashlib/json/random. It must not execute any native combat action.
 source=code.read_text();assert 'import vlab_effects' not in source and 'event_commit(' not in source
 env=None
 p=subprocess.run([sys.executable,str(code)],cwd=str(root),capture_output=True,text=True,timeout=120)
 assert p.returncode==0,(p.stdout,p.stderr)
 result=json.loads(p.stdout);assert result['valid']==40 and result['odd_half_floor_spells']==4 and result['commits']==480
 assert result['history_replays']==0
 return {'status':'PASS_R223_COLD_PORTABLE_MASTER_TENTATIVE_TEST_ONLY','hashes':len(mapping),'valid':result['valid'],'blocked':result['blocked'],'complete_factorial_seeds':result['full_factorial_seed_units'],'odd_half_floor_spells':result['odd_half_floor_spells'],'commits':result['commits'],'events':result['events'],'historical_replays':0}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--archive');parser.add_argument('--root');args=parser.parse_args()
 if args.archive:
  with tempfile.TemporaryDirectory(prefix='r223_cold_') as d:
   with zipfile.ZipFile(args.archive) as z:
    assert z.testzip() is None,'CRC_FAIL';z.extractall(d)
   print(json.dumps(verify(Path(d)),ensure_ascii=False,indent=2))
 else:print(json.dumps(verify(Path(args.root)),ensure_ascii=False,indent=2))
