"""Safe R213 cold recovery. READ-ONLY: manifest, historical pins, SQLite chain/causality. NEVER runs historic or new combat runners."""
from pathlib import Path
import json,hashlib,sys,zipfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
 failures=[]
 for relative, expected in manifest['files'].items():
  p=ROOT/relative
  if not p.is_file() or sha(p)!=expected:failures.append(relative)
 if failures:raise RuntimeError('MANIFEST_MISMATCH:'+repr(failures))
 for rel in manifest['historical_zips']:
  with zipfile.ZipFile(ROOT/rel) as z:
   bad=z.testzip()
   if bad:raise RuntimeError('HISTORIC_CRC_FAIL:'+rel+':'+bad)
 sys.path.insert(0,str(ROOT/'code'))
 from r213_independent_sql_audit import audit
 from r213_multiturn_independent_audit import check
 aoos=[audit(p) for p in sorted((ROOT/'evidence/db').glob('R213_AOO_*.sqlite'))]
 multi=[check(p) for p in sorted((ROOT/'evidence/db').glob('R213_MULTITURN_*.sqlite'))]
 assert len(aoos)==9 and sum(x['status']=='PASS_TEST_CONDITIONAL' for x in aoos)==8
 assert sum(x['status']=='QUARANTINED_PENDING_UNKNOWN_EFFECT' for x in aoos)==1
 assert len(multi)==3 and all(x['status']=='PASS_MULTITURN_CONDITIONAL' for x in multi)
 result={'result':'PASS_R213_COLD_PORTABLE_RECOVERY_CONDITIONAL',
 'manifest_hashes':len(manifest['files']),'historical_crc':len(manifest['historical_zips']),
 'sqlite_valid_aoo':8,'sqlite_quarantined':1,'sqlite_valid_multiturn':3,
 'aoo_count':sum(x.get('attacks',0) for x in aoos),'aoo_hp_loss':sum(x.get('hp_loss',0) for x in aoos),
 'multiturn_attacks':sum(x['physical_attacks'] for x in multi),'combats_reexecuted':0,
 'nac_pass_scope':'TEST_CONDITIONAL','canonical_rank_credit':0}
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return result
if __name__=='__main__':main()
