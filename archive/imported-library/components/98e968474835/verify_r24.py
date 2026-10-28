"""Integrity verifier for R24 immutable files and upstream R23/R22.
Does not connect to Notion or create any 'native snapshot' files.
"""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
EXPECTED_R23='30787845be77e3e6425ea984182e067354caa42e447c7d31bbf60a7b5460d222'
EXPECTED_R22='c0e51ba2b4944413528dc1d5c3c0494afa78e32d13f17d02d5d5fb816866255d'
EXPECTED_GATEWAY='4d35ed1f20616f68b8ed3e17191d92af5ffde909d64e8122cda72ec1df411b69'
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 m=json.loads((ROOT/'MANIFEST_R24.json').read_bytes())
 assert m['schema']=='LEVEL-UP-R24-IMMUTABLE-CHECKSUM-MANIFEST-v1'
 for name,v in m['files'].items():
  p=ROOT/name
  assert p.is_file() and p.stat().st_size==v['bytes'] and sha(p.read_bytes())==v['sha256'],name
 original=(ROOT/'historical/UPSTREAM_R23_VERIFIED_UNMODIFIED.zip').read_bytes()
 assert sha(original)==EXPECTED_R23
 with ZipFile(BytesIO(original)) as z:
  assert z.testzip() is None
  r22=z.read('LEVELUP_R23/historical/UPSTREAM_R22_ORIGINAL_VERIFIED.zip')
  r23m=json.loads(z.read('LEVELUP_R23/MANIFEST_R23.json'))
  assert len(r23m['files'])==7
  for name,v in r23m['files'].items():
   b=z.read('LEVELUP_R23/'+name)
   assert sha(b)==v['sha256'] and len(b)==v['bytes'],name
 assert sha(r22)==EXPECTED_R22
 with ZipFile(BytesIO(r22)) as z:
  assert z.testzip() is None
  g=z.read('levelup_r22_native_capture/historical/VLAB_GATEWAY_R04_REFERENCE_UNMODIFIED.zip')
  assert sha(g)==EXPECTED_GATEWAY
  rm=json.loads(z.read('levelup_r22_native_capture/MANIFEST_R22.json'))
  assert len(rm['files'])==13
  for name,v in rm['files'].items():
   b=z.read('levelup_r22_native_capture/'+name)
   assert sha(b)==v['sha256'] and len(b)==v['bytes'],name
 for forbidden in ('NATIVE_SNAPSHOT_R22.json','NATIVE_READ_RECEIPT_R22.json'):
  assert not list(ROOT.rglob(forbidden)), 'FICTITIOUS_NATIVE_OUTPUT:'+forbidden
 print(json.dumps({'schema':'R24-PRESERVATION-READBACK','manifest_R24':len(m['files']),
  'manifest_R23':7,'manifest_R22':13,'upstream_R23':EXPECTED_R23,
  'upstream_R22':EXPECTED_R22,'gateway_original':EXPECTED_GATEWAY,
  'crc_and_sha':'PASS','fictitious_native_snapshot':'ABSENT','native_capture_performed':False},sort_keys=True))
if __name__=='__main__':main()
