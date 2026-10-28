#!/usr/bin/env python3
"""Run after extracting the C29 ZIP. Recreates ALL deterministic derived CSV/JSON outputs.
Note: authored PSV/decision memo source is hash-verified, not regenerated.
Not a Notion documentary second-reader and not an independent model.
"""
import hashlib,subprocess,sys,tempfile,shutil,zipfile,json
from pathlib import Path
base=Path(__file__).resolve().parents[1]
manifest=json.loads((base/'C29_SHA256_MANIFEST.json').read_text())
assert len(manifest['entries'])>=14
for name,expected in manifest['entries'].items():
 p=base/name;assert p.exists(),name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,('hash',name)
with tempfile.TemporaryDirectory() as d:
 t=Path(d);(t/'src').mkdir();(t/'publication').mkdir()
 for srcname in ['build_c29.py','verify_c29_independent.py']:
  shutil.copy2(base/'src'/srcname,t/'src'/srcname)
 for srcname in ['build_c29.py','verify_c29_independent.py']:
  res=subprocess.run([sys.executable,str(t/'src'/srcname)],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  print(srcname,res.stdout.strip())
 regenerated=[f.name for f in (t/'publication').iterdir()]
 assert len(regenerated)>=10,regenerated
 for name in regenerated:
  x=(t/'publication'/name).read_bytes();y=(base/'publication'/name).read_bytes()
  assert x==y,('not byte-identical',name)
 print('PASS_C29_COLD_REPLAY',len(regenerated),'/',len(regenerated),'regenerated identical; hashed payloads',len(manifest['entries']))
