"""Four independent R18 SHA chain reconstructed adulterations, then source auditor must reject.
No writes to originals; temp copies only. No combat engine imports.
"""
import json,sqlite3,hashlib,shutil,tempfile
from pathlib import Path
from r232_independent_sql_audit import audit,sha
ROOT=Path(__file__).resolve().parents[1]
def mutate(path,mode):
 c=sqlite3.connect(path)
 meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state'])
 if mode=='FALSE_HP':
  st['actors']['VAROK']['hp']+=1;st['r232']['outcome']['varok_hp']+=1
 elif mode=='FALSE_P4':st['r232']['source_status']='P4-EXPLICIT-CANON'
 elif mode=='FALSE_DICE':
  st['native_events'][0]['damage_rolls'][0]=1+(st['native_events'][0]['damage_rolls'][0]%10)
 elif mode=='FALSE_RD':
  st['native_events'][1]['rd_applied']=0
 else:raise ValueError(mode)
 newstate=sha(st)
 row=json.loads(c.execute('select row_json from events where seq=1').fetchone()[0]);row['detail']['new_events']=st['native_events']
 row['after_sha']=newstate;row_sha=sha(row)
 with c:
  c.execute('update meta set value=? where key="state"',(json.dumps(st,sort_keys=True,separators=(',',':'),ensure_ascii=False),))
  c.execute('update meta set value=? where key="head"',(row_sha,))
  c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=1',(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False),row_sha,newstate))
 c.close()
def run():
 out={};modes=['FALSE_HP','FALSE_P4','FALSE_DICE','FALSE_RD']
 orig=list((ROOT/'evidence/db').glob('*.sqlite'))
 assert len(orig)==4
 for mode in modes:
  with tempfile.TemporaryDirectory(prefix='R232_HASH_ADVERSARIAL_') as temp:
   r=Path(temp);(r/'sources').mkdir();(r/'evidence/db').mkdir(parents=True);(r/'evidence/quarantine').mkdir()
   for src in (ROOT/'sources').glob('*.json'):shutil.copy2(src,r/'sources'/src.name)
   for db in orig:shutil.copy2(db,r/'evidence/db'/db.name)
   for db in (ROOT/'evidence/quarantine').glob('*.sqlite'):shutil.copy2(db,r/'evidence/quarantine'/db.name)
   mutate(r/'evidence/db'/orig[0].name,mode)
   try:audit(r,write=False)
   except AssertionError as e:out[mode]=str(e)
   else:raise AssertionError('ADVERSARY_NOT_REJECTED_'+mode)
 assert len(out)==4
 p=ROOT/'evidence/reports/R232_ADVERSARIAL_REHASH.json';p.write_text(json.dumps({'status':'PASS_R232_4_OF_4_REHASHED_ILLEGAL_MUTATIONS_REJECTED','cases':out},ensure_ascii=False,indent=2)+'\n')
 print(p.read_text())
if __name__=='__main__':run()
