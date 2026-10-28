#!/usr/bin/env python3
"""Offline readback/immutable-history validator for the additive R26 sandbox ZIP."""
import json,hashlib,zipfile,sys
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def check(root):
    root=Path(root); m=json.loads((root/'FILE_MANIFEST_VLAB_R26.json').read_text(encoding='utf8'))
    for name,h in m['content_sha256'].items():
        p=root/name
        if not p.is_file() or sha(p.read_bytes())!=h:raise RuntimeError('CONTENT_MISMATCH:'+name)
    old=json.loads((root/'FILE_MANIFEST_VLAB_R25.json').read_text(encoding='utf8'))
    for name,h in old['all_content_sha256'].items():
        if name not in m['content_sha256'] or m['content_sha256'][name]!=h:
            raise RuntimeError('R25_HISTORICAL_HASH_CHANGED:'+name)
    print('R26 HASH VERIFIED',len(m['content_sha256']),'BASE R25',len(old['all_content_sha256']))
    return True
if __name__=='__main__':check(sys.argv[1] if len(sys.argv)>1 else '.')
