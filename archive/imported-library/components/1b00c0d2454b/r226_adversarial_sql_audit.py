"""R226 forged-hash clones adversarial control. Accepted DBs are never written."""
import json,sqlite3,shutil,hashlib
from pathlib import Path
from r226_independent_sql_audit import one,sha,req,ROOT
P=(ROOT/'sources/R226_PREREG_BEFORE_EXEC.json').read_bytes();PH=hashlib.sha256(P).hexdigest()
I=(ROOT/'sources/R226_MANOPLA_PRIMARY_MECHANICAL_EXCERPT.json').read_bytes();IH=hashlib.sha256(I).hexdigest()
C=ROOT/'evidence/adversarial';C.mkdir(exist_ok=True)
BASE=ROOT/'evidence/db/R226_MANOPLA_SAME_PHYSICAL_WITH_MAGIC_S22681001.sqlite'
CASES={
 'FREE_PA':lambda s:s['actors']['R'].__setitem__('pa',344),
 'HIDDEN_SLOW_PERSISTENCE':lambda s:s['actors']['V'].__setitem__('timed_source_speed_penalty_m',3),
 'FAKE_NONCANON':lambda s:s['r226'].__setitem__('world_canon',True),
 'FORGED_ITEM_ARM':lambda s:s['r226'].__setitem__('arm','SAME_PHYSICAL_NO_MAGIC')}
results=[]
for name,fn in CASES.items():
 dest=C/f'R226_HASH_REBUILT_{name}.sqlite'
 if dest.exists():raise FileExistsError('NEVER_REUSE_ATTACK_CLONE:'+str(dest))
 shutil.copy2(BASE,dest)
 con=sqlite3.connect(dest);m=dict(con.execute('select key,value from meta'));st=json.loads(m['state']);fn(st)
 records=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
 records[-1]['after_sha']=sha(st)
 jsonrow=json.dumps(records[-1],ensure_ascii=False,sort_keys=True,separators=(',',':'))
 h=sha(records[-1])
 with con:
  con.execute('UPDATE events SET row_json=?,row_sha=?,after_sha=? WHERE seq=2',(jsonrow,h,records[-1]['after_sha']))
  con.execute('UPDATE meta SET value=? WHERE key="state"',(json.dumps(st,ensure_ascii=False,sort_keys=True,separators=(',',':')),))
  con.execute('UPDATE meta SET value=? WHERE key="head"',(h,))
 con.close()
 try:one(dest,22681001,'SAME_PHYSICAL_WITH_MAGIC',PH,IH)
 except AssertionError as e:results.append({'case':name,'rejected':True,'reason':str(e)})
 else:raise AssertionError('FORGED_STATE_ACCEPTED:'+name)
ROOT.joinpath('evidence/reports/R226_ADVERSARIAL.json').write_text(json.dumps({'status':'PASS_FORGED_HASH_REJECTION','cases':results},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS_R226_4_HASH_REBUILT_ADVERSARIAL','cases':results},indent=2))
