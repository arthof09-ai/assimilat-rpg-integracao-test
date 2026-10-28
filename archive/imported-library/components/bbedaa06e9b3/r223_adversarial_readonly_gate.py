"""Deliberate hash-rebuilt clones. Native journals untouched. Independent auditor must reject."""
import sqlite3,json,hashlib,shutil
from pathlib import Path
from r223_independent_factorial_audit import audit_fight,ROOT
from r223_independent_mechanical_audit import audit_one

def cj(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(cj(x).encode()).hexdigest()

def clone_case(name):
 source=ROOT/'evidence/db/R223_ODD_FLOOR_INIT_A_ROUND_S22381010.sqlite'
 dest=ROOT/'evidence/adversarial'/f'R223_TAMPER_{name}.sqlite';dest.parent.mkdir(exist_ok=True)
 assert source.is_file() and not dest.exists()
 with sqlite3.connect(f'file:{source}?mode=ro&immutable=1',uri=True) as c,sqlite3.connect(dest) as d:c.backup(d)
 with sqlite3.connect(dest) as c:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rev=int(m['revision'])
  if name=='NO_MASTER_POLICY':st['r223']['policy']='CANONICAL'
  elif name=='FALSIFIED_SOURCE':st['r223']['decision_status']='CANON_APPROVED'
  elif name=='HP_DESYNC':st['actors']['R']['hp']+=1
  elif name=='PA_DOUBLE_SPENT':st['actors']['E']['pa']-=80
  elif name=='PREREG_CHANGED':st['r223']['prereg_sha256']='00'*32
  else:raise ValueError(name)
  row=json.loads(c.execute('select row_json from events where seq=?',(rev,)).fetchone()[0]);row['after_sha']=sha(st);rowsha=sha(row)
  c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=?',(cj(row),rowsha,row['after_sha'],rev))
  c.execute('update meta set value=? where key="state"',(cj(st),));c.execute('update meta set value=? where key="head"',(rowsha,))
  c.commit();c.execute('pragma wal_checkpoint(TRUNCATE)')
 return dest

def main():
 ph=hashlib.sha256((ROOT/'sources/R223_PREREG_BEFORE_NEW_COMBATS.json').read_bytes()).hexdigest();out=[]
 for name in ('NO_MASTER_POLICY','FALSIFIED_SOURCE','HP_DESYNC','PA_DOUBLE_SPENT','PREREG_CHANGED'):
  file=clone_case(name)
  try:audit_fight(file,ph,known_identity=('INIT_A','ROUND',22381010));raise AssertionError('AUDITOR_ESCAPED:'+name)
  except AssertionError as e:
   if str(e).startswith('AUDITOR_ESCAPED'):raise
   out.append({'case':name,'rejected':True,'error':str(e),'rebuilt_final_sha':True})
 obj={'status':'PASS_R223_REBUILT_HASH_ATTACKS_REJECTED_5_OF_5','cases':out}
 (ROOT/'evidence/reports/R223_ADVERSARIAL.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(obj,indent=2))
if __name__=='__main__':main()
