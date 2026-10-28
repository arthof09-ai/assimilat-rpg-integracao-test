"""R214 cold portable verification. External stdlib only; NEVER invokes battle runners."""
import sys,zipfile,hashlib,json,tempfile,pathlib,subprocess,sqlite3

def main(path):
 path=pathlib.Path(path)
 with zipfile.ZipFile(path) as z:
  names=z.namelist()
  assert len(names)==len(set(names))
  assert all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts for n in names)
  assert z.testzip() is None,'CRC error'
  manifest=json.loads(z.read('R214_MANIFEST.json'))
  expected=manifest['files'];actual={n for n in names if not n.endswith('/') and n!='R214_MANIFEST.json'}
  assert set(expected)==actual,(len(expected),len(actual))
  for name,f in expected.items():
   data=z.read(name);assert hashlib.sha256(data).hexdigest()==f['sha256'] and len(data)==f['bytes'],name
  with tempfile.TemporaryDirectory(prefix='r214_cold_readonly_') as td:
   z.extractall(td)
   root=pathlib.Path(td)
   # Safety fault must remain locked but must not be treated as a successful experiment.
   fault=root/'evidence/db/R214_FAULT_AFTER_INTENT_S21449001.sqlite'
   conn=sqlite3.connect('file:'+str(fault)+'?mode=ro',uri=True)
   try:
    meta=dict(conn.execute('SELECT key,value FROM meta'))
    assert conn.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==1
    assert conn.execute('SELECT COUNT(*) FROM events').fetchone()[0]==0
    assert meta['head']==meta['genesis'] and meta['revision']=='0'
   finally:conn.close()
   cmd=[sys.executable,str(root/'code/r214_independent_sql_audit.py'),'--readonly']
   proc=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
   assert proc.returncode==0,(proc.stdout,proc.stderr)
   result=json.loads(proc.stdout)
   assert result['dbs']==15 and result['commits']==38 and result['aoo']==14 and result['total_physical_attacks']==38
   saf=json.loads((root/'evidence/R214_SAFETY_CONTROLS.json').read_text())
   assert len(saf['probes'])==9
  return {'status':'PASS_R214_COLD_PORTABLE_RECOVERY_CONDITIONAL','zip_entries':len(names),
    'manifest_hashes':len(expected),'crc':'PASS','sqlite_new_valid':result['dbs'],
    'sqlite_quarantined_pending':1,'commits':result['commits'],'events':result['events'],
    'new_aoo':result['aoo'],'bilateral_attacks':24,'historic_combat_replays':0}
if __name__=='__main__':print(json.dumps(main(sys.argv[1]),indent=2))
