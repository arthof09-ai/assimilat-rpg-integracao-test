"""Cold recovery only: CRC, sha256, independent SQL audits; NEVER run historical battles."""
from pathlib import Path
import zipfile,hashlib,json,tempfile,subprocess,sys
ROOT=Path(__file__).resolve().parent

def audit_folder(root):
 audit=subprocess.run([sys.executable,str(root/'new/r211/code/r211_independent_sql_readonly_audit.py')],capture_output=True,text=True,check=True)
 d=json.loads(audit.stdout)
 assert d['audit']=='PASS_R211_INDEPENDENT_R18_NATIVE_MOVEMENT_DYNAMIC_CENTER_CAUSAL_SQLITE'
 print(json.dumps(d,ensure_ascii=False,indent=2))
def verify(p):
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  mf=json.loads(z.read('MANIFEST_SHA256.json'))
  files=mf['files'];assert len(files)+1==len(z.namelist())
  for n,h in files.items():
   assert hashlib.sha256(z.read(n)).hexdigest()==h,(n,h)
  assert hashlib.sha256(z.read('baseline/R210_VERIFIED_NOT_REPLAYED.zip')).hexdigest()=='dc76e2b993535761c86d216a6436735fbb65e9136675c44030af6f35981fc2a8'
  with tempfile.TemporaryDirectory(prefix='R211_AUDIT_READONLY_') as td:
   root=Path(td)
   for m in z.infolist():
    assert not m.filename.startswith('/') and '..' not in Path(m.filename).parts
    z.extract(m,root)
   audit_folder(root)
 return {'verdict':'PASS_R211_COLD_PORTABLE_RECOVERY','entries':len(z.namelist()),'files_sha256_checked':len(files),'replayed_historical_combat':0}
if __name__=='__main__':
 p=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'VLAB_R211_DYNAMIC_MOVEMENT_TACTICS_COLD_AUDITED_MESTRE_ONLY.zip'
 print(json.dumps(verify(p),indent=2))
