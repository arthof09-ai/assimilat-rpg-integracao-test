"""Cold recovery: verify R212 and embedded R211 bytes, never run any battle."""
from pathlib import Path
import zipfile,json,hashlib,tempfile,subprocess,sys
BASE_SHA='837243621dd3631a0f3b92bbca305fe4f4de29ec9b5ae5e735761d38004505d7'
def verify(p):
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  names=z.namelist();assert len(names)==len(set(names)) and 'MANIFEST_SHA256.json' in names
  man=json.loads(z.read('MANIFEST_SHA256.json'));files=man['files'];assert len(files)==len(names)-1
  for n,h in files.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
  b='baseline/R211_VERIFIED_NOT_REPLAYED.zip';assert hashlib.sha256(z.read(b)).hexdigest()==BASE_SHA
  with tempfile.TemporaryDirectory(prefix='R212_COLD_AUDIT_') as td:
   root=Path(td)
   for info in z.infolist():
    assert not info.filename.startswith('/') and '..' not in Path(info.filename).parts
    z.extract(info,root)
   with zipfile.ZipFile(root/b) as sub:
    assert sub.testzip() is None
    # The earlier checkpoint is not re-executed; cold import is separate from testing.
    for info in sub.infolist():
     assert '..' not in Path(info.filename).parts and not info.filename.startswith('/')
     sub.extract(info,root/'preflight')
   a=subprocess.run([sys.executable,str(root/'new/r212/code/r212_sql_readonly_audit.py')],check=True,capture_output=True,text=True)
   r=json.loads(a.stdout)
   assert r['status']=='PASS_R212_INDEPENDENT_R18_NATIVE_MOVEMENT_RANGED_PHYSICAL_SQLITE_CONDITIONAL_RD'
   assert r['audited_runs']==6 and r['opportunity_attacks']==0
 return {'verdict':'PASS_R212_COLD_PORTABLE_RECOVERY_PARTIAL_SCOPE','entries':len(names),'sha_files':len(files),'audited_runs':6,'historical_replays':0,'aoo_r43':'BLOCKED-SOURCE-ADJACENCY'}
if __name__=='__main__':
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent/'VLAB_R212_NATIVE_PHYSICAL_AFTER_MOVEMENT_COLD_AUDITED_MESTRE_ONLY.zip'
 print(json.dumps(verify(p),ensure_ascii=False,indent=2))
