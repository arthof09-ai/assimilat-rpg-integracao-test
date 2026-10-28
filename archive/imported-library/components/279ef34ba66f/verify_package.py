"""Verify R04 package CRC, allowlisted paths, per-file SHA-256 and manifest."""
import hashlib
import json
import sys
import zipfile
from pathlib import PurePosixPath


def verify(path):
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError('CRC_MISMATCH')
        names=z.namelist()
        if len(names)!=len(set(names)):
            raise ValueError('DUPLICATE_MEMBER')
        for n in names:
            p=PurePosixPath(n)
            if n.startswith('/') or '..' in p.parts or not n.startswith('vlab_gateway_r04/'):
                raise ValueError('UNSAFE_MEMBER_PATH:'+n)
        manifest_name='vlab_gateway_r04/MANIFEST.json'
        manifest=json.loads(z.read(manifest_name))
        expected=set(manifest['files'])
        actual={n[len('vlab_gateway_r04/'): ] for n in names if n!=manifest_name}
        if expected!=actual:
            raise ValueError('MEMBER_SET_MISMATCH')
        for relative,m in manifest['files'].items():
            b=z.read('vlab_gateway_r04/'+relative)
            if len(b)!=m['bytes'] or hashlib.sha256(b).hexdigest()!=m['sha256']:
                raise ValueError('SHA_MISMATCH:'+relative)
        return {'status':'ZIP_CRC_SHA_PASS','files':len(expected),'sha256':hashlib.sha256(open(path,'rb').read()).hexdigest(),
                'tests_declared':manifest['tests']['passed'],'scope':'LOCAL_ONLY_NOTION_OFF'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: verify_package.py <release.zip>')
    print(json.dumps(verify(sys.argv[1]),sort_keys=True,ensure_ascii=False))
