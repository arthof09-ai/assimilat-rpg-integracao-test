"""R239 adversarial tests on isolated database copies with selected fully rehashed tampering."""
import json,sqlite3,copy,hashlib,tempfile,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r239_independent_readonly_audit as audit

def ch(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def clone(out):
 (out/'sources').mkdir(parents=True);(out/'evidence/db').mkdir(parents=True)
 for p in (ROOT/'sources').glob('*.json'):shutil.copy2(p,out/'sources'/p.name)
 for p in (ROOT/'evidence/db').glob('*.sqlite'):shutil.copy2(p,out/'evidence/db'/p.name)

def mutate_db(path,fn,rehash=True):
 c=sqlite3.connect(path)
 try:
  meta=dict(c.execute('select key,value from meta'));state=json.loads(meta['state']);row=json.loads(c.execute('select row_json from events').fetchone()[0]);fn(row,state)
  if rehash:
   row['after_sha']=ch(state);rh=ch(row)
   with c:
    c.execute('update events set row_json=?,row_sha=?,after_sha=?',(json.dumps(row,sort_keys=True,ensure_ascii=False,separators=(',',':')),rh,row['after_sha']))
    c.execute('update meta set value=? where key="state"',(json.dumps(state,sort_keys=True,ensure_ascii=False,separators=(',',':')),))
    c.execute('update meta set value=? where key="head"',(rh,))
  else:
   with c:c.execute('update events set row_json=?',(json.dumps(row,sort_keys=True,ensure_ascii=False,separators=(',',':')),))
 finally:c.close()

def main():
 path=ROOT/'evidence/db/R239_BELOW_557_S23931001.sqlite';require=assert_fail
 tests=[
 ('unhashed_event_modification',lambda row,s:row['detail'].__setitem__('attack_score',999),False),
 ('weak_flag_concealment_rehashed',lambda row,s:(row['detail']['events_new'][0].__setitem__('weak',False),s['native_events'][0].__setitem__('weak',False)),True),
 ('weak_speed_cheat_rehashed',lambda row,s:(row['detail']['events_new'][0].__setitem__('speed','50'),s['native_events'][0].__setitem__('speed','50')),True),
 ('attack_damage_forgery_rehashed',lambda row,s:(row['detail']['events_new'][3].__setitem__('raw',777),s['native_events'][3].__setitem__('raw',777)),True),
 ('official_cell_promotion_rehashed',lambda row,s:s['r239'].__setitem__('official_cells',1),True),
 ('official_P4_promotion_rehashed',lambda row,s:s['r239'].__setitem__('source_status','CANONICAL-P4'),True),
 ('source_hash_drift_rehashed',lambda row,s:row['payload'].__setitem__('source_sha','0'*64),True),
 ('tampered_critical_rehashed',lambda row,s:(row['detail']['events_new'][3].__setitem__('critical','POSITIVE'),s['native_events'][3].__setitem__('critical','POSITIVE')),True),
 ('tampered_rng_tape_rehashed',lambda row,s:(row['detail']['events_new'][2].__setitem__('hit0_common',[6,6,6,6,6,6]),s['native_events'][2].__setitem__('hit0_common',[6,6,6,6,6,6])),True),
 ('snapshot_weak_status_cheat_rehashed',lambda row,s:s['r239']['outcome'].__setitem__('weak',False),True),
 ]
 passed=[]
 with tempfile.TemporaryDirectory(prefix='R239_ADVERSARIAL_OUTSIDE_ORIGINAL_') as tmp:
  for i,(label,fn,rehashed) in enumerate(tests):
   dst=Path(tmp)/f'case{i}';clone(dst);mutate_db(dst/'evidence/db'/path.name,fn,rehash=rehashed)
   try:audit.audit(dst,write=False);raise AssertionError('TAMPERING_NOT_DETECTED:'+label)
   except AssertionError as e:
    if str(e).startswith('TAMPERING_NOT_DETECTED'):raise
    passed.append({'test':label,'status':'REJECTED','reason':str(e),'rehashed':rehashed})
  dst=Path(tmp)/'pending';clone(dst)
  c=sqlite3.connect(dst/'evidence/db'/path.name)
  with c:c.execute("INSERT INTO pending VALUES ('INJECTED-PENDING','GARBAGE','EXPLOIT','{}')")
  c.close()
  try:audit.audit(dst,write=False);raise AssertionError('TAMPERING_NOT_DETECTED:PENDING')
  except AssertionError as e:
   if str(e).startswith('TAMPERING_NOT_DETECTED'):raise
   passed.append({'test':'pending_intent_injected','status':'REJECTED','reason':str(e),'rehashed':True})
  dst=Path(tmp)/'source';clone(dst)
  p=dst/'sources/R236_FRACO_RULE_EXCERPT.json';text=p.read_text();p.write_text(text.replace('hp < 10%','hp <= 10%'))
  try:audit.audit(dst,write=False);raise AssertionError('TAMPERING_NOT_DETECTED:SOURCE')
  except AssertionError as e:
   if str(e).startswith('TAMPERING_NOT_DETECTED'):raise
   passed.append({'test':'authority_text_forgery','status':'REJECTED','reason':str(e),'rehashed':True})
 out={'status':'PASS_ALL_ADVERSARIAL_TAMPERS_REJECTED','tests':len(passed),'fully_rehashed_attacks':sum(x['rehashed'] for x in passed),'details':passed,
      'original_databases_modified':False,'scope':'TEST clone only'}
 (ROOT/'reports/R239_ADVERSARIAL_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2))

def assert_fail(msg):raise AssertionError(msg)
if __name__=='__main__':main()
