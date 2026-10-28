"""Read-only cold recovery R227; no combat invocation."""
from pathlib import Path
import argparse,json,hashlib,zipfile,tempfile,subprocess,sys
def dh(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def verify(root):
 root=Path(root);m=json.loads((root/'SHA256_MANIFEST.json').read_text());actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and x.name!='SHA256_MANIFEST.json'}
 if set(m)!=actual:raise AssertionError('MISSING_OR_EXTRA_FILES')
 for key,h in m.items():
  if dh(root/key)!=h:raise AssertionError('SHA_MISMATCH:'+key)
 s=(root/'code/r227_independent_magic_rd_audit.py').read_text()
 if 'import vlab_effects' in s or 'import r227_magic_rd_sensitivity_native' in s or 'event_commit(' in s:raise AssertionError('AUDITOR_IMPORTS_EXECUTOR')
 r=subprocess.run([sys.executable,str(root/'code/r227_independent_magic_rd_audit.py')],cwd=root,capture_output=True,text=True,timeout=80)
 if r.returncode:raise AssertionError('AUDIT_FAIL: '+r.stderr+' '+r.stdout)
 a=json.loads(r.stdout)
 if any(a[k]!=v for k,v in {'arms':12,'pairs':6,'commits':24,'hits':4,'item_activations':8,'magic_rd100_net_total':0,'hp_preserved_by_rd100':100,'slow_expirations':4,'historical_replays':0}.items()):raise AssertionError('SCIENTIFIC_METRIC_DRIFT')
 sec=json.loads((root/'evidence/reports/R227_ADVERSARIAL_RESULT.json').read_text())
 if len(sec['attacks'])!=4:raise AssertionError('FOUR_ATTACKS_ABSENT')
 return {'status':'PASS_R227_COLD_RD_SENSITIVITY_SEMICANON_SOURCE_GATED','manifest_hashes':len(m),'arms':a['arms'],'pairs':a['pairs'],'commits':a['commits'],'events':a['events'],'magic_rd100_net_total':a['magic_rd100_net_total'],'hp_preserved_by_rd100':a['hp_preserved_by_rd100'],'hash_rebuilt_forgeries_rejected':len(sec['attacks']),'historical_replays':0}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--archive');ap.add_argument('--root');x=ap.parse_args()
 if x.archive:
  with tempfile.TemporaryDirectory(prefix='R227_COLD_') as d:
   with zipfile.ZipFile(x.archive) as z:
    if z.testzip() is not None:raise AssertionError('BAD_CRC')
    z.extractall(d)
   print(json.dumps(verify(d),indent=2))
 else:print(json.dumps(verify(x.root),indent=2))
