"""R236 adversarial copies, rebuild final R18 row/head/snapshot hashes. No writer to admitted SQLite."""
import json,sqlite3,shutil,tempfile
from pathlib import Path
import r236_independent_readonly_audit as au
ROOT=Path(__file__).resolve().parents[1]
def alter(path,kind):
 c=sqlite3.connect(str(path));m=dict(c.execute('select key,value from meta'));s=json.loads(m['state']);row=json.loads(c.execute('select row_json from events order by seq desc limit 1').fetchone()[0]);lastatk=s['native_events'][-2]
 if kind=='HP0_FALSE_REVIVAL':s['actors']['C']['hp']=1;s['r236']['outcome']['hp']['C']=1
 elif kind=='CONTINUE_AFTER_HP0':row['detail']['active_after']='G'
 elif kind=='UNJUST_WEAK_SPEED':s['actors']['C']['base_speed']='75'
 elif kind=='FALSIFY_OVERKILL':lastatk['overkill']+=4
 elif kind=='PROMOTE_PRECREATE_TO_P4':s['r236']['source_status']='P4-CANON'
 else:raise ValueError(kind)
 if kind=='FALSIFY_OVERKILL':row['detail']['events_new']=s['native_events'][-len(row['detail']['events_new']):]
 row['after_sha']=au.sha(s)
 c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=?',(au.can(row),au.sha(row),row['after_sha'],row['seq']))
 c.execute('update meta set value=? where key="head"',(au.sha(row),));c.execute('update meta set value=? where key="state"',(au.can(s),));c.commit();c.close()
def run():
 source=ROOT/'evidence/db/R236_SOLO_G_C_WEAK_S23661001.sqlite';dest=ROOT/'evidence/adversarial';dest.mkdir(exist_ok=True);results=[]
 for name in ['HP0_FALSE_REVIVAL','CONTINUE_AFTER_HP0','UNJUST_WEAK_SPEED','FALSIFY_OVERKILL','PROMOTE_PRECREATE_TO_P4']:
  copy=dest/f'R236_ADV_{name}.sqlite';shutil.copy2(source,copy);alter(copy,name)
  with tempfile.TemporaryDirectory(prefix='vlab_r236_adversarial_') as td:
   tmp=Path(td);(tmp/'sources').symlink_to(ROOT/'sources',target_is_directory=True);(tmp/'evidence/db').mkdir(parents=True)
   for f in (ROOT/'evidence/db').glob('*.sqlite'):
    if f.name==source.name:shutil.copy2(copy,tmp/'evidence/db'/f.name)
    else:(tmp/'evidence/db'/f.name).symlink_to(f)
   try:au.audit(tmp,write=False);error='FALSE_ACCEPT'
   except AssertionError as exc:error=str(exc)
  results.append({'case':name,'rejected':error!='FALSE_ACCEPT','reason':error,'final_R18_chain_rehashed':True,'original_db_untouched':True})
 if not all(r['rejected'] for r in results):raise AssertionError(results)
 obj={'status':'PASS_R236_ADVERSARIAL_REHASH_5_OF_5','cases':results};path=ROOT/'evidence/reports/R236_ADVERSARIAL_REHASH.json';path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');print(path.read_text())
if __name__=='__main__':run()
