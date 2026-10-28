"""Mutate last R235 event with rebuilt R18 hashes, verify independent auditor rejects. Never replace original admitted DBs."""
import json,hashlib,shutil,tempfile,sqlite3
from pathlib import Path
import r235_independent_readonly_audit as auditor
ROOT=Path(__file__).resolve().parents[1]
def mutate(path,which):
 c=sqlite3.connect(str(path));meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state']);row=json.loads(c.execute('select row_json from events order by seq desc limit 1').fetchone()[0]);spell=st['native_events'][-2];tape=st['native_events'][-3]
 if which=='PA_REFUND':
  st['actors']['G']['pa']+=55;st['r235']['outcome']['pa']['G']+=55
 elif which=='ROUND_UP_ODD':
  assert spell['r223_damage_before_half']%2==1
  spell['raw']+=1
 elif which=='INVALID_SOURCE_PROMOTION':st['r235']['source_status']='P4_FULL_CANON'
 elif which=='FAKE_SAVE_RESULT':tape['save_score']=0
 elif which=='MAGIC_RD_BYPASS':spell['rd_applied']=0;spell['effective']=spell['raw'];spell['hp_after']-=spell['raw'];st['actors']['R']['hp']-=spell['raw'];st['r235']['outcome']['hp']['R']-=spell['raw'];st['r235']['stats']['spell_hp_loss']+=spell['raw']
 else:raise ValueError(which)
 # Every native event mutation is mirrored into R18 last-row detail. This is a fully rewritten last-row SHA,
 # final snapshot SHA and journal head (not just a raw checksum corruption).
 row['detail']['events_new']=st['native_events'][1:]
 row['detail']['gross_damage']=spell['r223_damage_before_half']
 row['after_sha']=auditor.sha(st)
 c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=?',(auditor.can(row),auditor.sha(row),row['after_sha'],row['seq']))
 c.execute('update meta set value=? where key="state"',(auditor.can(st),));c.execute('update meta set value=? where key="head"',(auditor.sha(row),));c.commit();c.close()
def run():
 original=ROOT/'evidence/db/R235_SAVE_FOCUS_S23578001.sqlite';d=ROOT/'evidence/adversarial';d.mkdir(exist_ok=True)
 out=[]
 for name in ['PA_REFUND','ROUND_UP_ODD','INVALID_SOURCE_PROMOTION','FAKE_SAVE_RESULT','MAGIC_RD_BYPASS']:
  copy=d/f'R235_ADV_{name}.sqlite';shutil.copy2(original,copy);mutate(copy,name)
  with tempfile.TemporaryDirectory(prefix='vlab_r235_adv_') as td:
   root=Path(td);(root/'evidence/db').mkdir(parents=True);(root/'sources').symlink_to(ROOT/'sources',target_is_directory=True)
   for path in (ROOT/'evidence/db').glob('*.sqlite'):
    target=root/'evidence/db'/path.name
    if path.name==original.name:shutil.copy2(copy,target)
    else:target.symlink_to(path)
   try:auditor.audit(root,write=False);msg='FALSE_ACCEPT'
   except AssertionError as e:msg=str(e)
  out.append({'mutation':name,'rejected':msg!='FALSE_ACCEPT','reason':msg,'last_row_hash_rebuilt':True,'final_state_hash_rebuilt':True,'no_original_db_write':True})
 if not all(x['rejected'] for x in out):raise AssertionError(out)
 rep={'status':'PASS_R235_INDEPENDENT_ADVERSARIAL_5_OF_5','cases':out};f=ROOT/'evidence/reports/R235_ADVERSARIAL_REHASH.json';f.write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n');print(f.read_text())
if __name__=='__main__':run()
