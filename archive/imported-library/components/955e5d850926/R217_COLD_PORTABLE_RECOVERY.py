#!/usr/bin/env python3
"""Independent R217 COLD READ-ONLY verification. No fight replay, no original mutations."""
from pathlib import Path
import sys,json,hashlib,zipfile
sys.dont_write_bytecode=True
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from r217_independent_order_audit import verify,audit_single_order
from r216_independent_readonly_audit import audit_one

def ck(cond,msg):
 if not cond:raise AssertionError(msg)
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cold():
 manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text());ck(len(manifest)>40,'MANIFEST_TOO_SMALL')
 for rel,sha in manifest.items():
  p=ROOT/rel;ck(p.is_file() and H(p)==sha,'BAD_MANIFEST_FILE:'+rel)
 ck(len(manifest)==len([p for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST_SHA256.json']),'UNLISTED_ARTIFACT')
 result=verify(ROOT)
 clones=sorted((ROOT/'evidence/adversarial').glob('R217_ADVERSARIAL_*.sqlite'));ck(len(clones)==2,'TAMPER_COUNT')
 preregsha=H(ROOT/'sources/R217_ORDER_PREFLIGHT_PREREG.json')
 for cl in clones:
  ck(audit_one(cl)['status']=='PASS','GENERIC_MECHANICAL_CLONE_SHOULD_PASS')
  try:audit_single_order(cl,preregsha)
  except AssertionError:pass
  else:raise AssertionError('SCHEDULER_TAMPER_WAS_NOT_REJECTED')
 ck(result['valid_runs']==10 and result['independent_seed_pairs']==5 and result['commits']==120 and result['events']==732,'SCIENTIFIC_RECEIPT')
 return {'status':'PASS_R217_COLD_PORTABLE_RECOVERY_INITIATIVE_ORDER_TEST_CONDITIONAL','files_manifest':len(manifest),'new_accepted_runs':10,'independent_seed_pairs':5,'commits':120,'events':732,'quarantines':14,'hash_rebuilt_scheduler_tamper_rejected':2,'historical_replays':0,'production':'HOLD'}
if __name__=='__main__':print(json.dumps(cold(),indent=2,ensure_ascii=False))
