import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'MANIFEST_SHA256.json').read_text())['files']
a={str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in root.rglob('*') if x.is_file() and '__pycache__' not in x.parts and not x.name.endswith('.pyc') and x.name!='MANIFEST_SHA256.json'}
assert a==m,{'not_in_manifest':list(a.keys()-m.keys()),'mismatches':[k for k in a.keys()&m.keys() if a[k]!=m[k]]}
print('MANIFEST PASS',len(a))
