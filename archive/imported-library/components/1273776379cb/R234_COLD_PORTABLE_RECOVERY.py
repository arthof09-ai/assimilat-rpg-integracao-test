"""R234 cold portable verifier: SHA256, independent SQLite-only audit, no fight runner import or replay."""
from pathlib import Path
import json,hashlib,sys,zipfile
ROOT=Path(__file__).resolve().parent
def run():
 m=json.loads((ROOT/'SHA256_MANIFEST.json').read_text());files=m['files'];actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith(('-wal','-shm')) and p.name!='SHA256_MANIFEST.json'}
 if set(files)!=actual:raise AssertionError('MANIFEST_EXACT_SET_MISMATCH '+str(sorted(set(files)^actual)[:10]))
 for rel,hex in files.items():
  p=ROOT/rel
  if hashlib.sha256(p.read_bytes()).hexdigest()!=hex:raise AssertionError('FILE_SHA_MISMATCH '+rel)
 sys.path.insert(0,str(ROOT/'code'))
 from r234_independent_readonly_audit import audit
 x=audit(ROOT,write=False)
 assert x['status']=='PASS_R234_BILATERAL_TEAM_BEAST_NATIVE_COLD_CONDITIONAL' and x['counts']['commits']==120 and x['counts']['native_events']==500
 a=json.loads((ROOT/'evidence/reports/R234_ADVERSARIAL_REHASH.json').read_text());assert a['status']=='PASS_R234_ADVERSARIAL_REHASH_5_OF_5' and all(z['rejected'] for z in a['cases'])
 print('PASS_R234_PORTABLE_COLD_RECOVERY_SOURCE_VZ_CONDITIONAL',len(files),'HASHES',x['valid_arms'],'R18_SQLITE',x['counts']['commits'],'COMMITS',x['counts']['native_events'],'EVENTS','ZERO_REPLAY')
if __name__=='__main__':run()
