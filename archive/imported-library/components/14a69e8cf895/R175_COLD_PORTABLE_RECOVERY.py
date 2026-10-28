"""Cold portable verifier of the R175 package (read-only, no attack execution).
Only stdlib; tests math and causal replay through *independent* checker programs.
"""
import pathlib,json,hashlib,subprocess,sys,csv,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=json.loads((ROOT/'R175_SHA256_MANIFEST.json').read_text())
 for item,h in manifest['files'].items():
  p=ROOT/item
  assert p.is_file() and sha(p)==h,('checksum',item)
 assert sha(ROOT/'baseline/R174_BASELINE_EXACT.zip')=='67458f8b78558286bf6d2a4dee307916a09b373cd03eae03a576484e8b0ac83c'
 with zipfile.ZipFile(ROOT/'baseline/R174_BASELINE_EXACT.zip') as z:assert z.testzip() is None and len(z.namelist())==363
 def run(cmd,expected_ok=True):
  p=subprocess.run([sys.executable,*map(str,cmd)],capture_output=True,text=True)
  assert (p.returncode==0)==expected_ok,('auditor_expected',expected_ok,p.stderr[-800:])
  return json.loads(p.stdout) if expected_ok else {'rejected':True}
 results=run([ROOT/'code/r175_independent_audit.py',ROOT/'evidence/duels_v2'])
 assert results['passed']==2 and sum(i['commits'] for i in results['results'])==109 and sum(i['native_events'] for i in results['results'])==321
 p=next((ROOT/'evidence/counter_v2').glob('*.sqlite'))
 counter=run([ROOT/'code/r175_counter_independent_audit.py',p])
 assert counter['commits']==27 and counter['native_events']==104 and counter['counter_declarations']==13 and counter['counter_responses']==13
 for kind in ('RD','SOURCE'):run([ROOT/'code/r175_independent_audit.py',ROOT/'evidence/tampered'/kind],False)
 with (ROOT/'evidence/R175_DMG_BRIDGE_RECEIPTS_NOT_ACKED.csv').open() as f:r=list(csv.DictReader(f))
 assert len(r)==146 and sum(x['attack_kind']=='R50_R51_COUNTER' for x in r)==13
 cm=json.loads((ROOT/'R175_17_CONTRACT_CROSSWALK.json').read_text())
 assert len(cm['original_id_sequence'])==17 and cm['R175_terminals']==0 and cm['R175_official_cells']==0
 return {'status':'PASS_R175_COLD_PORTABLE_RECOVERY','manifest_hashes':len(manifest['files']),'baseline_R174_sha':sha(ROOT/'baseline/R174_BASELINE_EXACT.zip'),
 'legitimate_databases':3,'commits':136,'native_events':425,'offensive_receipts':146,'dependent_matched_battles':3,'independent_holdout_observations':0,
 'reactions_R50_R51':13,'tampered_rehash_clones_rejected':2,'terminal_contracts':0,'official_benchmark_cells':0,'production':'HOLD'}
if __name__=='__main__':print(json.dumps(main(),indent=2,ensure_ascii=False))
