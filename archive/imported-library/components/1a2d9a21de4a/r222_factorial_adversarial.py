"""R222 fault injection on cloned SQLite only, hash-rebuilt final row; source-factorial
independent audit must detect errors that generic mechanical auditor cannot.
"""
from pathlib import Path
import sqlite3,json,hashlib
from r222_independent_mechanical_audit import audit_one as generic
from r222_independent_factorial_audit import audit_fight,ROOT

def js(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def hs(x):return hashlib.sha256(js(x).encode()).hexdigest()
def fault(name):
 source=ROOT/'evidence/db/R222_FACTOR_INIT_A_ROUND_S22288003.sqlite'
 dest=ROOT/'evidence/adversarial'/f'R222_TAMPER_{name}.sqlite';dest.parent.mkdir(exist_ok=True)
 if dest.exists():return dest
 with sqlite3.connect(source) as a,sqlite3.connect(dest) as b:a.backup(b)
 with sqlite3.connect(dest) as c:
  meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state']);rev=int(meta['revision'])
  if name=='MAPPING_TAG_FALSIFIED':st['r222']['mode']='ABILITY'
  elif name=='INITIATIVE_DICE_FORGED':st['r222']['rolls']['R']['dice'][1]=1
  elif name=='INIT_ORDER_FORGED':st['r222']['order']=['E','V','R']
  elif name=='PREREG_HASH_FORGED':st['r222']['prereg_sha256']='00'*32
  else:raise AssertionError('UNKNOWN_FAULT')
  (text,)=c.execute('select row_json from events where seq=?',(rev,)).fetchone();row=json.loads(text);row['after_sha']=hs(st)
  newrow=hs(row);c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=?',(js(row),newrow,row['after_sha'],rev))
  c.execute('update meta set value=? where key="state"',(js(st),));c.execute('update meta set value=? where key="head"',(newrow,));c.commit()
 with sqlite3.connect(dest) as c:c.execute('pragma wal_checkpoint(TRUNCATE)')
 return dest

def main():
 prereg=ROOT/'sources/R222_PREREG_BEFORE_NEW_COMBATS.json';ph=hashlib.sha256(prereg.read_bytes()).hexdigest();out=[]
 for name in ('MAPPING_TAG_FALSIFIED','INITIATIVE_DICE_FORGED','INIT_ORDER_FORGED','PREREG_HASH_FORGED'):
  p=fault(name);generic_pass=generic(p)['status']=='PASS'
  try:audit_fight(p,ph,known_identity=('INIT_A','ROUND',22288003));rejected=False;why='ESCAPED'
  except AssertionError as e:rejected=True;why=str(e)
  assert generic_pass and rejected,(name,generic_pass,rejected,why)
  out.append({'case':name,'native_mechanical_auditor_PASS':True,'factorial_source_auditor_REJECT':True,'reason':why,'file':p.name})
 obj={'status':'PASS_R222_ADVERSARIAL_HASH_REBUILT_4_OF_4','cases':out,'new_battles':0}
 (ROOT/'evidence/reports/R222_ADVERSARIAL_FACTORIAL.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(obj,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
