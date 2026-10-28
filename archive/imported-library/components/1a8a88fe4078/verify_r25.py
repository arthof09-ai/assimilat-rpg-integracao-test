#!/usr/bin/env python3
"""R25 archive payload integrity check, no network or Notion writes."""
import json,hashlib,sys,zipfile
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def verify(root):
    root=Path(root);m=json.loads((root/'MANIFEST_R25.json').read_text());files=m['files']
    # Python execution creates non-delivered __pycache__ files; ignore only
    # these generated cache bytes, never source/data payload discrepancies.
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
            and p.name!='MANIFEST_R25.json' and p.suffix!='.pyc'
            and '__pycache__' not in p.parts}
    if actual!=set(files):raise RuntimeError('file set mismatch: '+str((actual-set(files),set(files)-actual)))
    for name,meta in files.items():
        blob=(root/name).read_bytes()
        if len(blob)!=meta['bytes'] or sha(blob)!=meta['sha256']:raise RuntimeError('mismatch: '+name)
    upstream=(root/'historical/UPSTREAM_R24_BYTE_EXACT.zip').read_bytes()
    if sha(upstream)!=m['upstream_R24_sha256']:raise RuntimeError('R24 byte continuity broken')
    with zipfile.ZipFile(root/'historical/UPSTREAM_R24_BYTE_EXACT.zip') as z:
        if z.testzip() is not None:raise RuntimeError('R24 CRC failed')
    return {'status':'PASS_LOCAL_ARTIFACT_ONLY','manifest_files':len(files),'upstream_R24_sha256':sha(upstream)}
if __name__=='__main__':print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),indent=2))
