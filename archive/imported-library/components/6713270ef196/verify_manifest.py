import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
for name,sha in manifest.items():
 p=ROOT/name
 assert p.is_file(), name
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 assert h==sha,(name,h,sha)
print('PASS_MANIFEST',len(manifest))
