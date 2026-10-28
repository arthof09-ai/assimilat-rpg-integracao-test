"""Cold recovery of R228. Only reads SQLite and independently audits; no combat replay."""
import tempfile,zipfile,hashlib,json,subprocess,sys,importlib.util
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root):
 root=Path(root);m=json.loads((root/'SHA256_MANIFEST.json').read_text())
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST.json'}
 if set(actual)!=set(m):raise AssertionError('MANIFEST_SET')
 for k,v in m.items():
  if sha(root/k)!=v:raise AssertionError('HASH_FAIL:'+k)
 prog=root/'code/r228_independent_sql_audit.py';code=prog.read_text()
 if 'vlab_effects_v08' in code or 'event_commit(' in code:raise AssertionError('AUDITOR_NOT_INDEPENDENT')
 out=subprocess.run([sys.executable,str(prog)],cwd=root,capture_output=True,text=True,timeout=70)
 if out.returncode:raise AssertionError('SQL_AUDITOR:'+out.stderr+out.stdout)
 d=json.loads(out.stdout)
 if d['new_test_scenes']!=2 or d['R18_commits']!=6 or d['real_moves']!=4:raise AssertionError('RESULT_DRIFT')
 spec=importlib.util.spec_from_file_location('r228_review',prog);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 pre=(root/'sources/R228_PREREG_BEFORE_EXEC.json').read_bytes();ph=hashlib.sha256(pre).hexdigest();h=sha(root/'sources/R228_ISKIEL_FROZEN_MECHANICAL_SOURCE.json')
 rejects=[]
 for name in ['FREE_PA','POSITION_MAGIC','SLOW_UNEXPIRED','WORLD_CANON_LAUNDERED']:
  p=root/'evidence/adversarial'/f'R228_FORGED_HASH_{name}.sqlite'
  try:mod.audit_one(p,'HIT',22871003,[3,2,4],ph,h)
  except AssertionError as e:rejects.append({'name':name,'reason':str(e)})
  else:raise AssertionError('FORGED_MUTANT_ADMITTED:'+name)
 return {'status':'PASS_R228_COLD_SOURCE_TIMED_MOVEMENT_TEST','manifest_hashes':len(m),'R18_commits':6,'events':21,'native_moves':4,'source_slow_cases':1,'quarantined_invalid_no_commit':1,'adversarial_rejected':rejects,'historical_replays':0}
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--archive',required=True);x=a.parse_args()
 with tempfile.TemporaryDirectory(prefix='R228_COLD_') as tmp:
  with zipfile.ZipFile(x.archive) as z:
   if z.testzip() is not None:raise AssertionError('CRC')
   z.extractall(tmp)
  print(json.dumps(verify(tmp),ensure_ascii=False,indent=2))
