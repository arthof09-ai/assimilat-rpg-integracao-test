import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
for name,dig in manifest['files'].items():
 p=root/name
 assert p.is_file(), 'MISSING:'+name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==dig, 'MISMATCH:'+name
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc') and p.name!='MANIFEST_SHA256.json'}
assert actual==set(manifest['files']),f'MANIFEST_SCOPE_ERROR extra={actual-set(manifest["files"])} missing={set(manifest["files"])-actual}'
print('PASS_MANIFEST',len(actual))
