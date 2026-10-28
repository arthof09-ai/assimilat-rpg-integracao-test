from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
for path,sha in m['files'].items():
 p=ROOT/path
 assert p.exists(),path
 assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,path
print('MANIFEST_PASS',len(m['files']),'files')
