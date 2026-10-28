"""R216 adversarial test, fully isolated SQLite clones; rebuilt SHA chain.
Always compares own chain verifier PASS versus mechanically independent auditors FAIL.
Original valid databases never mutated. No historical runner execution.
"""
from pathlib import Path
import sys,sqlite3,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'code'))
from r216_independent_readonly_audit import audit_one
from r216_terrain_control_independent_audit import audit as audit_control
BASE=ROOT/'evidence/db';DEST=ROOT/'evidence/adversarial';DEST.mkdir(exist_ok=True)
def js(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(js(x).encode()).hexdigest()
def select_row(event_list, action):
 matches=[e for e in event_list if e['action']==action]
 if not matches:raise ValueError('ACTION_NOT_IN_LAST_COMMIT: '+action)
 return matches[-1]
def create(name,source,action,field,value,actor_state=False):
 dst=DEST/f'R216_TAMPER_{name}.sqlite'
 if dst.exists():return dst  # Previously generated adversarial clone; never mutate twice
 with sqlite3.connect(source) as inp,sqlite3.connect(dst) as out:inp.backup(out)
 with sqlite3.connect(dst) as c:
  m=dict(c.execute('SELECT key,value FROM meta'));s=json.loads(m['state']);rev=int(m['revision'])
  cmd,rj,before=c.execute('SELECT cmd_id,row_json,before_sha FROM events WHERE seq=?',(rev,)).fetchone();row=json.loads(rj)
  if actor_state:
   s['actors'][action][field]=value
  else:
   e=select_row(row['detail']['events_added'],action);e[field]=value
   ns=select_row(s['native_events'],action)
   assert ns['seq']==e['seq'];ns[field]=value
  row['after_sha']=sha(s);rr=sha(row)
  c.execute('UPDATE events SET row_json=?,row_sha=?,after_sha=? WHERE seq=?',(js(row),rr,row['after_sha'],rev))
  c.execute('UPDATE meta SET value=? WHERE key="state"',(js(s),))
  c.execute('UPDATE meta SET value=? WHERE key="head"',(rr,))
  c.commit()
 return dst

def validate_rebuilt(f):
 c=sqlite3.connect(f)
 try:
  m=dict(c.execute('SELECT key,value FROM meta'));rows=list(c.execute('SELECT seq,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'));prev=m['genesis'];past=None
  for seq,pr,rj,rsha,bef,aft in rows:
   x=json.loads(rj)
   if seq!=x['seq'] or pr!=x['prev'] or pr!=prev or sha(x)!=rsha or bef!=x['before_sha'] or aft!=x['after_sha'] or (past and past!=bef):return False
   prev=rsha;past=aft
  return prev==m['head'] and past==sha(json.loads(m['state']))
 finally:c.close()

def main():
 team=BASE/'R216_TEAM_PROTECTIVE_TEAM_A_S21674001.sqlite'
 inside=BASE/'R216_CTRL_INSIDE_S21676101.sqlite';outside=BASE/'R216_CTRL_OUTSIDE_S21676102.sqlite'
 cases=[
  ('SPORE_NET_DRIFT',team,'spell','effective',999,False,'team'),
  ('SUPPORT_STALE_HP',team,'R216_SUPPORT_OBSERVED_STATE','missing_hp',777,False,'team'),
  ('GEOMETRY_ALLY_HIT',team,'R216_GEOMETRY_STATE_DECISION','included',['R','V'],False,'team'),
  ('SPORE_PA_FAKE',team,'spell','PA_spent',0,False,'team'),
  ('FINAL_REACTION_DRIFT',team,'V','reaction',0,True,'team'),
  ('CONTROL_SAVE_DRIFT',inside,'R216_RAIZES_SAVE_AT_TURN_START','total',100,False,'control'),
  ('CONTROL_FAKE_MOVEMENT',inside,'R216_RAIZES_MOVEMENT_RESTRICTED','movement_legal',True,False,'control')]
 result=[]
 for name,src,act,field,val,astate,kind in cases:
  clone=create(name,src,act,field,val,actor_state=astate)
  chain=validate_rebuilt(clone)
  try:
   if kind=='team':audit_one(clone)
   else:audit_control(clone)
   rejected=False;reason='MECHANICAL_CHECK_FAILED_TO_REJECT'
  except Exception as e:rejected=True;reason=type(e).__name__+': '+str(e)
  result.append({'name':name,'source_db':src.name,'clone':clone.name,'chain_rebuilt_VALID':chain,'mechanically_rejected':rejected,'reason':reason})
  if not chain or not rejected:raise AssertionError('ADVERSARIAL_FAIL '+name)
 obj={'status':'PASS_R216_7_OF_7_HASH_CHAIN_REBUILT_ADVERSARIAL_REJECTIONS','tests':result,'historical_writes':0}
 (ROOT/'evidence/reports/R216_ADVERSARIAL_INTEGRATION.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2))
 print(json.dumps({'status':obj['status'],'names':[(x['name'],x['reason']) for x in result]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
