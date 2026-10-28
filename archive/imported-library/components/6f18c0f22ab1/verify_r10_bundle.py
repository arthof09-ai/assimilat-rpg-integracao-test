"""Manifest and whole-gate integrity verifier for R10 delivered ZIP/unpacked folder."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
from json import loads
import sys

def verify(root:Path):
    if root.is_file():
        with ZipFile(root) as z:
            bad=z.testzip()
            if bad:raise AssertionError('ZIP_CRC_FAIL '+bad)
            manifest=loads(z.read('MANIFEST_R10_SHA256.json'))
            for row in manifest['files']:
                a=z.read(row['name']);assert sha256(a).hexdigest()==row['sha256'] and len(a)==row['bytes'],row['name']
            obj=loads(z.read('DMG-F1-R10-GATES-18-ORIGINAIS-v01.json'))
    else:
        manifest=loads((root/'MANIFEST_R10_SHA256.json').read_bytes())
        for row in manifest['files']:
            a=(root/row['name']).read_bytes();assert sha256(a).hexdigest()==row['sha256'] and len(a)==row['bytes'],row['name']
        obj=loads((root/'DMG-F1-R10-GATES-18-ORIGINAIS-v01.json').read_bytes())
    assert len(obj['records'])==18 and obj['certified_whole']==0 and obj['target']==9
    assert [x['id'] for x in obj['records']]==[f'B{i:02d}' for i in range(1,19)]
    assert all(not x['whole_gate_pass'] for x in obj['records'])
    print(f"R10 BUNDLE VERIFIED / {len(manifest['files'])} signed-by-hash members / original 18 gates / 0 terminal PASS / no runtime")
if __name__=='__main__':
    verify(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent)
