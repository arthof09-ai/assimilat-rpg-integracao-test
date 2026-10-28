"""Cold recovery R230: manifest, CRC, independent semantic audit, NO COMBAT REPLAY."""
from pathlib import Path
import json,hashlib,zipfile,sys,tempfile,importlib.util
AUDITOR='r230_independent_sql_audit.py'
DEF='audit'

def verify(source):
 source=Path(source);h=hashlib.sha256(source.read_bytes()).hexdigest()
 with zipfile.ZipFile(source) as z:
  assert z.testzip() is None,'CRC';names=set(z.namelist())
  assert 'SHA256_MANIFEST.json' in names,'MANIFEST_ABSENT'
  m=json.loads(z.read('SHA256_MANIFEST.json'));assert m['version']==230 and m['mestre_only'] is True
  assert names==set(m['files'])|{'SHA256_MANIFEST.json'},'EXTRA_OR_MISSING_MEMBER'
  for rel,entry in m['files'].items():
   data=z.read(rel);assert len(data)==entry['size'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'HASH:'+rel
  with tempfile.TemporaryDirectory(prefix='vlab_R230_cold_') as temp:
   z.extractall(temp);p=Path(temp);code=p/'code'/AUDITOR
   spec=importlib.util.spec_from_file_location('aud_r230',code);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
   result=getattr(module,DEF)(p,write=False)
   assert result['status'].startswith('PASS_R230'), 'SEMANTIC_GATE'
   return {'status':'PASS_R230_COLD_PORTABLE_RECOVERY_TEST_CONDITIONAL','zip_sha256':h,'crc':'PASS','manifest_verified':len(m['files']),'semantic_auditor_status':result['status'],'historical_replays':0}
if __name__=='__main__':
 source=sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('VLAB_R230_NATIVE_BEAST_SOURCE_SPEED_COLD_AUDITED_MESTRE_ONLY.zip')
 print(json.dumps(verify(source),ensure_ascii=False,indent=2))
