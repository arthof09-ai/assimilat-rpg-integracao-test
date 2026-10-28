#!/usr/bin/env python3
from pathlib import Path
import tempfile,zipfile,json,hashlib,subprocess,sys
DNAME='DMG_R24_DECISIVE_ADDENDUM'
PARENT_SHA='73db7ee5fc0735e8d77282eacec90370448474f58cab66f00bfd056783a029ba'
sha=lambda b:hashlib.sha256(b).hexdigest()
def verify(pkg):
 with tempfile.TemporaryDirectory(prefix='R24_V02_CLEAN_') as td:
  root=Path(td)
  with zipfile.ZipFile(pkg) as z:
   assert z.testzip() is None;names=z.namelist();assert len(set(names))==len(names)
   assert all(not Path(n).is_absolute() and '..' not in Path(n).parts and Path(n).parts[0]==DNAME for n in names)
   z.extractall(root)
  d=root/DNAME
  m=json.loads((d/'manifest_R24_V02_SHA256.json').read_text())
  assert len(names)==len(m['files'])+1
  assert {p.name for p in d.iterdir() if p.is_file()}==set(m['files'])|{'manifest_R24_V02_SHA256.json'}
  for n,meta in m['files'].items():
   b=(d/n).read_bytes();assert len(b)==meta['size'] and sha(b)==meta['sha256'],n
  par=d/'R24_V01_ORIGINAL_READONLY.zip';assert sha(par.read_bytes())==PARENT_SHA==m['parent_sha256']
  with zipfile.ZipFile(par) as z:
   assert z.testzip() is None
   nested=root/'verify_clean_r24.py';nested.write_bytes(z.read('DMG_R24_INDEPENDENT_SANDBOX/verify_clean_r24.py'))
  pr=subprocess.run([sys.executable,str(nested),str(par)],capture_output=True,text=True,timeout=180,check=True)
  pdata=json.loads(pr.stdout);assert pdata['r24_tests']=='30/30 PASS' and pdata['certified']=='1/18 B02 only'
  generated=['R24_V02_JAKU_B15_EVIDENCE.json','R24_V02_PREFERENCIA_B15.md','HANDOFF_R24_V02.md']
  old={n:sha((d/n).read_bytes()) for n in generated}
  br=subprocess.run([sys.executable,'build_r24_v02.py'],cwd=d,capture_output=True,text=True,check=True,timeout=40)
  assert '"R24_V02_BUILD": "PASS"' in br.stdout
  assert old=={n:sha((d/n).read_bytes()) for n in generated},'rebuild differences'
  tt=subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_r24_v02.py','-q'],cwd=d,capture_output=True,text=True,check=True,timeout=40)
  assert 'Ran 15 tests' in tt.stderr and tt.stderr.strip().endswith('OK'),tt.stderr
  return {'zip_sha256':sha(Path(pkg).read_bytes()),'zip_entries':len(names),'manifest_files_verified':len(m['files']),'crc':'PASS','parent_r24_v01_sha':'PASS','r24_v01_recovered':pdata['r24_tests'],'r24_v02_test':'15/15 PASS','nested_r23':pdata['r23_tests'],'nested_r22':pdata['r22_tests'],'nested_r21':pdata['r21_tests'],'new_jaku_owned_gear_source':'DOCUMENTAL_VERIFIED_NOT_SCENE','b15':'PARTIAL','b15_real_events':0,'certification':'1/18 B02 only','strict':'0/2','original_csv':'0/9','master_decisions':'0/5 PENDING','notion_writes':0,'nac_pass':'HOLD'}
if __name__=='__main__':print(json.dumps(verify(Path(sys.argv[1])),indent=2,sort_keys=True))
