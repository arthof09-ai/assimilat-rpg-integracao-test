"""R196 cold, read-only, source-scope verifier; NEVER executes a combat command."""
from __future__ import annotations
import hashlib,json,pathlib,sys,importlib.util,sqlite3,collections
ROOT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def audit_structural(db):
 c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  rows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  pending=list(c.execute('SELECT * FROM pending'))
 finally:c.close()
 assert not pending
 previous_hash=None;previous_after=None
 for j,(seq,cmd,prev,rowj,rowsha,before,after) in enumerate(rows):
  x=json.loads(rowj)
  assert seq==j+1 and seq==x['seq'] and cmd==x['cmd_id'] and x['prev']==prev and x['before_sha']==before and x['after_sha']==after
  assert sha(canonical(x).encode())==rowsha
  if j:assert prev==previous_hash and before==previous_after
  previous_hash=rowsha;previous_after=after
 assert meta['head']==previous_hash and sha(canonical(json.loads(meta['state'])).encode())==previous_after and int(meta['revision'])==len(rows)
 cp=json.loads((db.parent/(db.name+'.checkpoint.json')).read_text())
 assert sha(canonical(cp['body']).encode())==cp['sha256'] and cp['body']['head']==meta['head'] and cp['body']['revision']==len(rows)
 return len(rows)

def main():
 manifest=json.loads((ROOT/'R196_SHA256_MANIFEST.json').read_text());files=manifest['files']
 assert len(files)==manifest['file_count'] and len(files)>100
 for name,h in files.items():
  p=ROOT/name
  assert p.is_file() and sha(p.read_bytes())==h,(name,'HASH_FAIL')
 assert sha((ROOT/'baseline/VLAB_R177_R186_EXACT_PRESERVED.zip').read_bytes())=='83465276a9b2822cf2791d206dd570b6fe6a9fa5711c85d1cd164ebd4d9ab3b7'
 assert sha((ROOT/'R193_PRE_REGISTRATION.json').read_bytes())=='fc5b4be4191da4f6c4a3cbcfe8a46d96b3a1aef8ed8b0739759b1fc5e03a58b6'
 spec=importlib.util.spec_from_file_location('r194_audit',ROOT/'code/r194_independent_replay.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 paths=sorted((ROOT/'evidence').glob('R193_LIU_CONCHA*.sqlite'))
 assert len(paths)==40
 res=[mod.verify(p) for p in paths]
 assert sum(x['commits']for x in res)==276 and sum(x['native_events']for x in res)==708 and sum(x['attacks']for x in res)==236
 assert len({x['seed'] for x in res})==5 and all(x['winner']=='LIU' and x['rounds']==3 for x in res)
 adversarial=json.loads((ROOT/'evidence/R194_ADVERSARIAL_REPORT.json').read_text());assert adversarial['status']=='PASS'
 negatives=sorted((ROOT/'negative').glob('*/R193_LIU_CONCHA_*.sqlite'))
 assert len(negatives)==10
 for p in negatives:
  audit_structural(p)
  try:mod.verify(p)
  except AssertionError:pass
  else:raise AssertionError(('SEMANTIC_FORGERY_ACCEPTED',p.name))
 cross=json.loads((ROOT/'R195_17_CONTRACT_CROSSWALK.json').read_text());assert len(cross['original_id_sequence'])==len(set(cross['original_id_sequence']))==17
 assert len(cross['rows'])==17 and set(x['id']for x in cross['rows'])==set(cross['original_id_sequence'])
 assert cross['R196_terminals']==0 and cross['official_cells']=={'before':0,'after':0,'denominator':1875} and not any(x['R196_terminal_certified']for x in cross['rows'])
 sm=json.loads((ROOT/'evidence/R194_SCIENTIFIC_SUMMARY.json').read_text());assert sm['experimental_branches']==40 and sm['matched_seed_blocks']==5 and sm['source_fully_admissible_count']==0
 report={'status':'PASS_R196_COLD_PORTABLE_RECOVERY','original_R186_sha_verified':True,'manifest_verified_files':len(files),'legitimate_databases':len(res),'legitimate_commits':276,'native_events':708,'offensive_receipts':236,'distinct_matchups':1,'matched_seed_blocks':5,'branch_analyses':40,'semantic_adversarial_rejections':len(negatives),'adversarial_structural_hash_rechecks':len(negatives),'official_contracts':0,'official_benchmarks':0,'fully_source_admissible':0,'source_unknowns_preserved':True,'combat_commands_executed':0,'external_human_auditor':False}
 print(json.dumps(report,ensure_ascii=False,indent=2));return report
if __name__=='__main__':main()
