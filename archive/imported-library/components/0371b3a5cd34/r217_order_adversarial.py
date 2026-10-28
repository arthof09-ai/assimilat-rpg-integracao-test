"""Two isolated hash-rebuilt journal clones to prove true chronology metadata gates.
All source evidence remains unchanged. No combat replay.
"""
from pathlib import Path
import sqlite3,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
from r217_independent_order_audit import audit_single_order
from r216_independent_readonly_audit import audit_one

def J(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def H(x):return hashlib.sha256(J(x).encode()).hexdigest()
def create(tag,field,value):
 s=ROOT/'evidence/db/R217_ORDER_V_FIRST_S21782001.sqlite';d=ROOT/'evidence/adversarial'/f'R217_ADVERSARIAL_{tag}.sqlite'
 d.parent.mkdir(parents=True,exist_ok=True)
 if d.exists():return d  # existing adversarial clone, do not apply mutation twice
 with sqlite3.connect(s) as a,sqlite3.connect(d) as b:a.backup(b)
 with sqlite3.connect(d) as c:
  m=dict(c.execute('SELECT key,value FROM meta'));state=json.loads(m['state']);rev=int(m['revision'])
  if field=='order':state['r217']['order']=value
  else:state['r216']['turns']['V']=value
  (rj,)=c.execute('SELECT row_json FROM events WHERE seq=?',(rev,)).fetchone();row=json.loads(rj);row['after_sha']=H(state)
  newrow=H(row);c.execute('UPDATE events SET row_json=?,row_sha=?,after_sha=? WHERE seq=?',(J(row),newrow,row['after_sha'],rev))
  c.execute('UPDATE meta SET value=? WHERE key="state"',(J(state),));c.execute('UPDATE meta SET value=? WHERE key="head"',(newrow,));c.commit()
 # CHECKPOINT the adversarial clone so immutable READ-ONLY auditors see the same published bytes.
 with sqlite3.connect(d) as c:
  c.execute('PRAGMA wal_checkpoint(TRUNCATE)')
  c.execute('PRAGMA journal_mode=DELETE')
 return d

def main():
 prereg=ROOT/'sources/R217_ORDER_PREFLIGHT_PREREG.json';ph=hashlib.sha256(prereg.read_bytes()).hexdigest()
 out=[]
 for tag,field,val in [('FALSE_DECLARED_ORDER','order',['R','V','E']),('FALSE_TURN_ALLOCATION','turns',5)]:
  p=create(tag,field,val)
  with sqlite3.connect(p) as c:
   c.execute('PRAGMA wal_checkpoint(TRUNCATE)')
   c.execute('PRAGMA journal_mode=DELETE')
  # Intentionally R216 generic mechanical audit cannot see R217 scheduler counters.
  generic_pass=audit_one(p)['status']=='PASS'
  try:audit_single_order(p,ph);reject=False;why='ESCAPED'
  except AssertionError as e:reject=True;why=str(e)
  assert generic_pass and reject,tag
  out.append({'name':tag,'generic_mechanical_auditor_PASS':generic_pass,'R217_initiative_auditor_REJECT':reject,'reason':why,'file':p.name})
 obj={'status':'PASS_R217_HASH_REBUILT_SCHEDULER_ADVERSARIAL_2_OF_2','cases':out,'new_combat_executions':0}
 (ROOT/'evidence/reports/R217_ADVERSARIAL_ORDER.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False))
 print(json.dumps(obj,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
