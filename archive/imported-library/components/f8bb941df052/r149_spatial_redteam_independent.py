"""R149 red-team source prereg SPATIAL fail-closed. Copy-only, never amend R146."""
import hashlib,json,sqlite3,shutil
from pathlib import Path
import r147_cold_metric_independent as c
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'runs'/'R146_MULTI_SOURCE_FERYN_ERISTAN_DEV_S995401.sqlite'
DEST=ROOT/'quarantined'/'R149_SPATIAL_LATE_METRIC_2M_REHASHED.sqlite'

def test():
 if DEST.exists():raise RuntimeError('NO_REPEAT_REDTEAM')
 shutil.copyfile(SOURCE,DEST);shutil.copyfile(SOURCE.with_suffix('.genesis.json'),DEST.with_suffix('.genesis.json'))
 with sqlite3.connect(DEST) as con:
  rows=[json.loads(r[0]) for r in con.execute('SELECT row_json FROM events ORDER BY seq')]
  matches=[r for r in rows if r['kind']=='MOVE_F_AOO_PULSO']
  assert len(matches)==1 and matches[0]['payload']['pulse_distance_m']==3
  matches[0]['payload']['pulse_distance_m']=2
  h=dict(con.execute('SELECT key,value FROM meta'))['genesis']
  for row in rows:
   row['prev']=h;newsha=c.sha(row)
   con.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(h,c.can(row),newsha,row['seq']))
   h=newsha
  con.execute('UPDATE meta SET value=? WHERE key=?',(h,'head'))
 try:c.cold(DEST)
 except AssertionError as ex:
  reason=str(ex)
 else:raise AssertionError('SECURITY_FAIL_SPATIAL_TAMPER_ACCEPTED')
 # Ledger hash chain has been redone so rejection is semantically keyed to physical precondition.
 assert 'topology' in reason or 'spatial' in reason.lower(),reason
 source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 result={'status':'PASS_SPATIAL_SEMANTIC_REJECTION','test_copy':DEST.name,'tamper':'3m PRE-MOVE -> 2m AFTER-MOVE',
  'all_row_sha256_chain_refabricated':'YES_COPY_ONLY','independent_reject_reason':reason,
  'original_R146_sha256':source_hash,'adversarial_copy_sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
  'prior_R138_DO_NOT_REWRITE':True,'official_effects':0}
 (ROOT/'R149_SPATIAL_REDTEAM_RESULT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 return result
if __name__=='__main__':print(json.dumps(test(),indent=2,ensure_ascii=False))
