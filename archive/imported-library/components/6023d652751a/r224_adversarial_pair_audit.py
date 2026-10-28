"""R224 independent adversarial hash-rebuilt clones. Never mutate source experiments."""
from pathlib import Path
import sqlite3,hashlib,json
from r224_independent_pair_audit import ROOT,audit_one

def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def h(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def make(name):
 quarantine=name.startswith('PENDING_');base='R224_HOLDCOMP_STRICT_HOLD_S22453002.sqlite' if quarantine else 'R224_HOLDCOMP_TENTATIVE_FLOOR_S22453002.sqlite'
 src=ROOT/'evidence'/('quarantine' if quarantine else 'db')/base
 dst=ROOT/'evidence/adversarial'/name/base;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists()
 with sqlite3.connect(f'file:{src}?mode=ro&immutable=1',uri=True) as c,sqlite3.connect(dst) as d:c.backup(d)
 with sqlite3.connect(dst) as c:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rev=int(m['revision'])
  if name=='POLICY_CANON_FORGED':st['r224']['world_canon']=True
  elif name=='INIT_ROLL_FORGED':st['r222']['rolls']['V']['dice'][1]=1
  elif name=='PA_DOUBLE_COST':st['actors']['E']['pa']-=80
  elif name=='PREREG_SOURCE_FORGED':st['r224']['prereg_sha256']='0'*64
  elif name=='PENDING_BASE_FORGED':c.execute('update pending set base_head=?',('a'*64,));c.commit();c.execute('pragma wal_checkpoint(TRUNCATE)');return dst
  else:raise ValueError(name)
  row=json.loads(c.execute('select row_json from events where seq=?',(rev,)).fetchone()[0]);row['after_sha']=h(st);rhs=h(row)
  c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=?',(canon(row),rhs,row['after_sha'],rev))
  c.execute('update meta set value=? where key="state"',(canon(st),));c.execute('update meta set value=? where key="head"',(rhs,));c.commit();c.execute('pragma wal_checkpoint(TRUNCATE)')
 return dst

def main():
 ph=hashlib.sha256((ROOT/'sources/R224_PREREG_BEFORE_NEW_COMBATS.json').read_bytes()).hexdigest();out=[]
 for case in ['POLICY_CANON_FORGED','INIT_ROLL_FORGED','PA_DOUBLE_COST','PREREG_SOURCE_FORGED','PENDING_BASE_FORGED']:
  p=make(case)
  try:audit_one(p,ph);raise RuntimeError('AUDIT_FAIL_OPEN:'+case)
  except AssertionError as e:out.append({'case':case,'rejected':True,'cause':str(e),'copy_only':True})
 ob={'status':'PASS_R224_FIVE_ADVERSARIAL_REBUILT_OR_TAMPERED_REJECTED','cases':out}
 (ROOT/'evidence/reports/R224_ADVERSARIAL_AUDIT.json').write_text(json.dumps(ob,ensure_ascii=False,indent=2)+'\n');print(json.dumps(ob,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
