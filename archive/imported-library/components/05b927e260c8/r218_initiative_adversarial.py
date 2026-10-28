"""Hash-rebuilt R218 adversarial clones; real read-only initiative auditor must reject; never touches accepted source SQLite."""
from pathlib import Path
import sqlite3,hashlib,json
from r216_independent_readonly_audit import audit_one
from r218_independent_rolled_audit import audit_one_rolled,ROOT

def js(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def hh(v):return hashlib.sha256(js(v).encode()).hexdigest()
def fake(kind):
 src=ROOT/'evidence/db/R218_ROLLED_INIT_A_S21831001.sqlite';dest=ROOT/'evidence/adversarial'/f'R218_ADVERSARIAL_{kind}.sqlite';dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():return dest # already-materialized adversarial clone; do not mutate it twice
 with sqlite3.connect(src) as a,sqlite3.connect(dest) as b:a.backup(b)
 with sqlite3.connect(dest) as c:
  m=dict(c.execute('SELECT key,value FROM meta'));st=json.loads(m['state']);rev=int(m['revision'])
  if kind=='INIT_ROLL_FORGED':st['r218']['rolls']['V']['dice'][0]=1
  elif kind=='DECLARED_ORDER_REVERSED':st['r218']['order']=list(reversed(st['r218']['order']))
  elif kind=='INIT_PRE_HASH_FALSE':st['r218']['prereg_sha256']='00'*32
  else:raise AssertionError(kind)
  (row_json,)=c.execute('SELECT row_json FROM events WHERE seq=?',(rev,)).fetchone();row=json.loads(row_json)
  row['after_sha']=hh(st);newsha=hh(row)
  c.execute('UPDATE events SET row_json=?,row_sha=?,after_sha=? WHERE seq=?',(js(row),newsha,row['after_sha'],rev))
  c.execute('UPDATE meta SET value=? WHERE key="state"',(js(st),));c.execute('UPDATE meta SET value=? WHERE key="head"',(newsha,));c.commit()
 with sqlite3.connect(dest) as c:
  c.execute('PRAGMA wal_checkpoint(TRUNCATE)')
 return dest

def main():
 prereg=ROOT/'sources/R218_PREREG_BEFORE_NEW_COMBATS.json';ph=hashlib.sha256(prereg.read_bytes()).hexdigest();out=[]
 for case in ['INIT_ROLL_FORGED','DECLARED_ORDER_REVERSED','INIT_PRE_HASH_FALSE']:
  p=fake(case)
  generic=audit_one(p)['status']=='PASS'
  try: audit_one_rolled(p,ph,fixture_identity=('INIT_A',21831001));reject=False;why='ESCAPED'
  except AssertionError as e:reject=True;why=str(e)
  assert generic and reject,(case,generic,reject,why)
  out.append({'case':case,'mechanical_auditor_passes':True,'source_initiative_auditor_rejects':True,'reason':why,'db':p.name})
 x={'status':'PASS_R218_INDEPENDENT_INITIATIVE_TAMPER_3_OF_3','cases':out}
 (ROOT/'evidence/reports/R218_ADVERSARIAL_3_OF_3.json').write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(x,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
