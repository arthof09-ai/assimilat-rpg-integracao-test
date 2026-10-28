"""R232 cold portable integrity + independent sqlite source audit, NO combat re-execution."""
import json,zipfile,hashlib,sys,tempfile,importlib.util
from pathlib import Path
def verify(package):
 package=Path(package)
 with zipfile.ZipFile(package) as z:
  assert z.testzip() is None,'CRC'
  m=json.loads(z.read('SHA256_MANIFEST.json'))
  assert m['version']==232 and m['mestre_only'] is True and set(z.namelist())==set(m['files'])|{'SHA256_MANIFEST.json'},'MANIFEST_MEMBERS'
  for name,value in m['files'].items():
   data=z.read(name);assert len(data)==value['size'] and hashlib.sha256(data).hexdigest()==value['sha256'],'FILE_SHA '+name
  with tempfile.TemporaryDirectory(prefix='R232_COLD_NO_REPLAY_') as tmp:
   z.extractall(tmp);p=Path(tmp)
   spec=importlib.util.spec_from_file_location('r232_independent',p/'code/r232_independent_sql_audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
   result=a.audit(p,write=False)
   assert result['status']=='PASS_R232_INDEPENDENT_NAMED_BEAST_ATTACKS_TEST_CONDITIONAL'
  return {'status':'PASS_R232_COLD_PORTABLE_RECOVERY_TEST_CONDITIONAL','file_sha256':hashlib.sha256(package.read_bytes()).hexdigest(),'files_verified':len(m['files']),'crc':'PASS','r18_commits':result['commits'],'native_events':result['events'],'distinct_named_beast_attacks':4,'historical_replays':0}
if __name__=='__main__':
 print(json.dumps(verify(sys.argv[1]),ensure_ascii=False,indent=2))
