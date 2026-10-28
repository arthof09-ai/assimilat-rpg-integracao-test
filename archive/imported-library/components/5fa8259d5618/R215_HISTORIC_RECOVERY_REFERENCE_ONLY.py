"""R215 cold, read-only verification. Never executes any runner or historical seed."""
import json,hashlib,sys,zipfile,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASELINE_SHA='72905eac9fd2a1906a35eb0b593ffe57984986c3351f2177107b46a73e44ff0d'
def sh(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
 expected=manifest['files']
 found={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST_SHA256.json'}
 # Readonly verifier can be run from a fresh extracted directory; do not mistake transient __pycache__ for release files.
 found={x for x in found if '__pycache__' not in Path(x).parts and not x.endswith(('-wal','-shm'))}
 assert set(expected)==found, {'missing':sorted(set(expected)-found),'unexpected':sorted(found-set(expected))[:12]}
 bad=[rel for rel,hash in expected.items() if sh(ROOT/rel)!=hash]
 assert not bad,('SHA_MISMATCH',bad)
 assert sh(ROOT/'baseline/R214_VERIFIED_COLD_ARCHIVE.zip')==BASELINE_SHA
 for p in ROOT.rglob('*.zip'):
  with zipfile.ZipFile(p) as z:assert z.testzip() is None,(str(p),'CRC_FAIL')
 res=subprocess.run([sys.executable,str(ROOT/'code/r215_independent_sql_audit.py'),'--readonly'],cwd=ROOT,capture_output=True,text=True,check=True)
 aud=json.loads(res.stdout);stored=json.loads((ROOT/'evidence/R215_INDEPENDENT_SQL_AUDIT.json').read_text())
 for k in ('status','valid','invalid','commits','events','attack_count','guards','guard_prevented','counter_responses','heals','hp_restored','spells'):
  assert aud[k]==stored[k],(k,aud.get(k),stored.get(k))
 assert aud['status']=='PASS' and aud['valid']==24 and aud['invalid']==0
 assert len(aud['paired_guard_checks'])==4 and all(x['offensive_rolls_verified']==8 for x in aud['paired_guard_checks'])
 adversarial=json.loads((ROOT/'evidence/R215_ADVERSARIAL_AUDIT.json').read_text())
 assert adversarial['status']=='PASS_ADVERSARIAL_REBUILT_CHAIN_REJECTED' and len(adversarial['cases'])==7
 print(json.dumps({'status':'PASS_R215_COLD_PORTABLE_RECOVERY_CONDITIONAL',
    'files_sha_pass':len(expected),'baseline_sha':BASELINE_SHA,'cold_sqlite_admitted':aud['valid'],
    'commits':aud['commits'],'events':aud['events'],'paired_seed_pairs':len(aud['paired_guard_checks']),
    'adversarial_rejections_preserved':len(adversarial['cases']),'historical_combat_replays':0},indent=2))
if __name__=='__main__':main()
