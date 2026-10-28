"""Verify immutable R22 payload, historical chain and disclosure boundaries."""
from pathlib import Path
import hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parent
EXPECTED_R21='9ffc9a3ef7905f71108848528ad17765a05c1a0b82fa0dfede355c4de4dbc53f'
EXPECTED_GATEWAY='4d35ed1f20616f68b8ed3e17191d92af5ffde909d64e8122cda72ec1df411b69'
EXPECTED_R20='38020643153d169582600e81245573dea883d72b6e57b5750bb26e527a55b733'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 d=json.loads((ROOT/'MANIFEST_R22.json').read_text())
 assert d['schema']=='LEVELUP-R22-SHA256-MANIFEST'
 for k,v in d['files'].items():
  p=ROOT/k
  assert p.is_file() and len(p.read_bytes())==v['bytes'] and sha(p)==v['sha256'],k
 a=ROOT/'historical/UPSTREAM_R21_UNMODIFIED.zip'
 b=ROOT/'historical/VLAB_GATEWAY_R04_REFERENCE_UNMODIFIED.zip'
 assert sha(a)==EXPECTED_R21 and sha(b)==EXPECTED_GATEWAY
 for path in (a,b):
  with zipfile.ZipFile(path) as z:assert z.testzip() is None
 with zipfile.ZipFile(a) as z:
  name=next(x for x in z.namelist() if x.endswith('UPSTREAM_R20_VERIFIED.zip'))
  assert hashlib.sha256(z.read(name)).hexdigest()==EXPECTED_R20
 assert not list(ROOT.rglob('NATIVE_SNAPSHOT_R22.json'))
 assert not list(ROOT.rglob('NATIVE_READ_RECEIPT_R22.json'))
 print(json.dumps({'manifest':len(d['files']),'sha256':'PASS','R21_R20_GATEWAY':'PASS','no_false_native_snapshot':True}))
if __name__=='__main__':main()
