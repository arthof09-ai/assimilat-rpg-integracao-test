from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text('utf8'))
assert manifest['schema']=='CRAFT-E43-E50-H1-H2-MANIFEST-v1'
for rel,hash_ in manifest['sha256'].items():
 p=root/rel
 assert p.is_file(), f'MISSING:{rel}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==hash_,f'CHANGED:{rel}'
print(f'PASS_MANIFEST_{len(manifest["sha256"])}/{len(manifest["sha256"])}')
