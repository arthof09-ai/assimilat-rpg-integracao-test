"""R23 package integrity + historic R22 2286 member byte-preservation."""
from __future__ import annotations
import hashlib,json,sys,zipfile

def sha(blob):return hashlib.sha256(blob).hexdigest()
def verify(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or z.testzip() is not None:
            raise ValueError('R23_DUPLICATE_OR_CRC_INVALID')
        manifest=json.loads(z.read('FILE_MANIFEST_VLAB_R23.json'))
        if manifest['schema']!='VLAB-R23-ADDITIVE-MANIFEST-v1':raise ValueError('SCHEMA_INVALID')
        actual=set(names)-{'FILE_MANIFEST_VLAB_R23.json'}
        if set(manifest['hashes'])!=actual:raise ValueError('R23_MANIFEST_MEMBERS_MISMATCH')
        failed=[p for p,h in manifest['hashes'].items() if sha(z.read(p))!=h]
        if failed:raise ValueError('R23_MEMBER_DIGEST_FAILED:'+str(failed[:3]))
        inherited=manifest['parent_R22_member_hashes']
        if len(inherited)!=2286 or len(inherited)!=manifest['inherited_R22_count']:
            raise ValueError('R22_HISTORY_COUNT_MISMATCH')
        if any(sha(z.read(k))!=h for k,h in inherited.items()):
            raise ValueError('R22_MEMBER_ALTERED')
        if 'FILE_MANIFEST_VLAB_R22.json' not in inherited:raise ValueError('R22_MISSING')
        return {'status':'PASS','zip_entries':len(names),'manifest_verified':len(actual),
            'historical_R22_members_byteidentical':len(inherited),'new_entries':len(names)-len(inherited)-1,
            'CRC':'PASS','terminal_contracts':'0/17','coverage_canonical':'0/1875'}
if __name__=='__main__':
    try:print(json.dumps(verify(sys.argv[1]),sort_keys=True))
    except Exception as ex:
        print(json.dumps({'status':'FAIL','reason':str(ex)}));raise SystemExit(2)
