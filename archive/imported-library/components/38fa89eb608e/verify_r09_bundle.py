"""Portable integrity only. Does NOT certify 18 scientific gates or Lab runtime."""
from __future__ import annotations
import zipfile,hashlib,json,sys,io

def verify(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None,'CRC FAIL'
        manifest=json.loads(z.read('MANIFEST_R09_SHA256.json'))
        members={n for n in z.namelist() if n!='MANIFEST_R09_SHA256.json'}
        assert set(manifest['file_hashes'])==members,(members^set(manifest['file_hashes']))
        for n,v in manifest['file_hashes'].items():
            b=z.read(n)
            assert hashlib.sha256(b).hexdigest()==v['sha256'] and len(b)==v['bytes'],n
        gate=json.loads(z.read('DMG-F1-R09-GATES-B01-B18-v01.json'))
        assert len(gate['gates'])==18
        assert {x['id'] for x in gate['gates']}=={f'B{i:02d}' for i in range(1,19)}
        assert gate['terminal_certified']==0 and all(not x['terminal_pass'] for x in gate['gates'])
        assert gate['counts']=={'VERIFIED':0,'PARTIAL':10,'BLOCKED':6,'NOT-TESTED':2}
        handoff=json.loads(z.read('DMG-F1-R09-STAGE12-HANDOFF-ENGINEERING-v01.json'))
        assert handoff['stage12']['terminal_contracts']==0
        assert handoff['stage12']['technical_contracts_total']==17
        assert handoff['stage12']['original_engine_v09_binary_available'] is False
        assert handoff['recipient_target']['INSTANCE_ID'] is None
        cases=json.loads(z.read('DMG-F1-R09-STRICT-PREFLIGHT-CASES-v01.json'))
        assert cases['no_engine_runtime_started'] is True
        return {'zip_crc':'PASS','files_hashed':len(members),'B_gates':18,'certified_B':0,'lab_contracts':17,'lab_accepted':0,'status':'DOCUMENT_ONLY_PASS'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python verify_r09_bundle.py ZIP')
    print(json.dumps(verify(sys.argv[1]),ensure_ascii=False,indent=2))
