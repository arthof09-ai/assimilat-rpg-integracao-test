"""Rehash-tampered SQL cloned from completed R174 runs, no original DB edited."""
from __future__ import annotations
import pathlib,sqlite3,json,hashlib,shutil,sys
from r174_independent_audit import audit,sha,canon,read_db

def mutate_database(source,target,mode):
 shutil.copy2(source,target)
 c=sqlite3.connect(str(target),isolation_level=None)
 try:
  rows=list(c.execute('select seq,row_json from events order by seq'))
  decoded=[json.loads(v) for _,v in rows]
  if mode=='RD':
   row=next((r for r in reversed(decoded) if r['kind']=='R174_SOURCE_ATTACK' and r['detail']['attack']['rd_applied']>0),None)
   assert row is not None;row['detail']['attack']['rd_applied']=0
  elif mode=='SOURCE':
   row=next(r for r in reversed(decoded) if r['kind']=='R174_SOURCE_ATTACK')
   row['detail']['attack']['r174_source_actor']='https://app.notion.com/p/3f2c2b324ede81f09c48f6e11874cd81'
  elif mode=='PA':
   row=next(r for r in decoded if r['kind']=='R174_SOURCE_ATTACK' and r['detail']['energy_activation'] is not None)
   row['detail']['energy_activation']['cost_pa']=0
  elif mode=='INIT':
   decoded[0]['detail']['rolls'][0]['bonus']+=22
  elif mode=='EVENT_OMISSION':
   row=next(r for r in reversed(decoded) if r['kind']=='R174_SOURCE_ATTACK')
   assert len(row['detail']['native_events'])>=2
   row['detail']['native_events'].pop()
  else:raise ValueError(mode)
  prev=c.execute("select value from meta where key='genesis'").fetchone()[0]
  c.execute('begin immediate')
  for row in decoded:
   row['prev']=prev
   rh=sha(row)
   c.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(prev,canon(row),rh,row['seq']))
   prev=rh
  c.execute("UPDATE meta SET value=? WHERE key='head'",(prev,))
  c.commit()
  checkpoint=pathlib.Path(str(target)+'.checkpoint.json')
  with sqlite3.connect(str(target)) as cx:
   meta=dict(cx.execute('select key,value from meta'))
   ev=[json.loads(t[0]) for t in cx.execute('select row_json from events order by seq')]
  body={'format':'R172_EXPORTED_CHECKPOINT_ONLY','db':target.name,'revision':int(meta['revision']),
   'head':meta['head'],'state':json.loads(meta['state']),'events':ev,'official_effects':0}
  checkpoint.write_text(json.dumps({'body':body,'sha256':sha(body)},sort_keys=True,ensure_ascii=False,indent=2))
 finally:c.close()

def structural_pass(db):
 meta,rows,pending=read_db(db);prev=meta['genesis'];last=None
 assert not pending
 for i,cmd_id,p,t,h,before,after in rows:
  row=json.loads(t);assert row['seq']==i and row['cmd_id']==cmd_id and row['prev']==p==prev and sha(row)==h
  assert row['before_sha']==before and row['after_sha']==after
  if last is not None:assert before==last
  prev=h;last=after
 assert prev==meta['head'] and last==sha(json.loads(meta['state']))
 return True

def main(evidence):
 base=pathlib.Path(evidence)/'duels/R174_VAROK_ARVETH_HOLD_VAROK_DEV1740101.sqlite'
 clones=pathlib.Path(evidence)/'adversarial_clones';clones.mkdir(parents=True,exist_ok=True)
 out=[]
 for mode in ('RD','SOURCE','PA','INIT','EVENT_OMISSION'):
  path=clones/f'R174_ADVERSARIAL_{mode}.sqlite';mutate_database(base,path,mode)
  assert structural_pass(path)
  try:audit(path)
  except (AssertionError,ValueError,KeyError,TypeError) as err:
   out.append({'mode':mode,'structural_rehash':'PASS','semantic_auditor':'REJECT','error_type':type(err).__name__,'commits_reexecuted':0})
  else:raise AssertionError('adulteration escaped independent semantic audit: '+mode)
 path=pathlib.Path(evidence)/'R174_ADVERSARIAL_RESULTS.json';path.write_text(json.dumps({'scope':'TEST_ONLY_SQL_REHASH_CLONES','results':out,'all_rejected':len(out)==5},indent=2,ensure_ascii=False))
 print(path.read_text())

if __name__=='__main__':main(sys.argv[1])
