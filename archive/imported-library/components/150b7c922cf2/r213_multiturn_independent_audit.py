"""Independent READ-ONLY multiturm R18 / v081 source auditor; never imports runner."""
from pathlib import Path
import json,hashlib,sqlite3
ROOT=Path(__file__).resolve().parents[1]
PHASH=hashlib.sha256((ROOT/'sources/R213_MULTITURN_PREREG.json').read_bytes()).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def H(v):return hashlib.sha256(canon(v).encode()).hexdigest()
def check(db):
 c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:
  m=dict(c.execute('select key,value from meta')); st=json.loads(m['state']); rows=c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq').fetchall()
  assert len(rows)==3 and m['revision']=='3' and st['r213multi']['prereg_sha']==PHASH
  prev=m['genesis'];past=None
  for i,(seq,cmd,p,raw,hs,bs,as_) in enumerate(rows):
   row=json.loads(raw)
   assert seq==i+1 and p==prev and hs==H(row) and row['after_sha']==as_ and row['before_sha']==bs
   if past is not None:assert past==bs
   past=as_;prev=hs
  assert prev==m['head'] and past==H(st)
  ev=st['native_events']; assert [e['seq'] for e in ev]==list(range(1,len(ev)+1))
  assert len(ev)==10 and st['phase']=='FINISHED_KO_TEST_NOT_VICTORY_CANON'
  mv=[e for e in ev if e['action']=='move'];at=[e for e in ev if e['action']=='weapon_attack'];bs=[e for e in ev if e['action']=='turn_start'];ends=[e for e in ev if e['action']=='turn_end'];passes=[e for e in ev if e['action']=='r213_proposed_npc_standard_pass']
  assert len(mv)==2 and len(at)==2 and len(bs)==2 and len(ends)==3 and len(passes)==1
  assert mv[0]['to']=='(5, 0)' and mv[1]['to']=='(10, 0)' and [e['by'] for e in bs]==['ERISTAN','RAYA']
  assert at[0]['seq']>mv[0]['seq'] and at[1]['seq']>mv[1]['seq'] and at[1]['seq']>bs[1]['seq']
  assert sum(e['hp_loss_actual'] for e in at)==630
  assert st['actors']['ERISTAN']['resource']['hp']==0 and st['actors']['RAYA']['resource']['hp']==1392
  assert st['actors']['RAYA']['resource']['movement']==0 and st['actors']['RAYA']['resource']['standard']==0
  for e in at:
   assert e['attack_origin']=='NORMAL' and e['advantage_levels']==0 and e['net_levels']==0
   assert e['roll_score']==sum(e['attack_roll_attempts'][0])+245
   assert e['normal_damage']==sum(sum(g) for g in e['damage_roll_groups'])+294
   assert e['after_hp']==max(0,e['before_hp']-e['net']) and e['hp_loss_actual']==e['before_hp']-e['after_hp']
   assert e['rd_applied']==25 and e['hit'] and e['critical']!='NEGATIVE'
  return {'db':db.name,'status':'PASS_MULTITURN_CONDITIONAL','commits':len(rows),'movement':len(mv),'physical_attacks':len(at),'hits':sum(e['hit'] for e in at),'raya_own_turns':2,'eristan_turn_passes':1,'hp_effective':630,'target_ko':True}
 finally:c.close()
def main():
 rows=[check(f) for f in sorted((ROOT/'evidence/db').glob('R213_MULTITURN_*.sqlite'))]
 assert len(rows)==3
 result={'audit':'PASS_R213_MULTITURN_R18_READONLY_INDEPENDENT','scope':'3 seeds, source-conditional, one-sided fixture','rows':rows,'official_victory_claim':False}
 (ROOT/'evidence/R213_MULTITURN_INDEPENDENT_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)); print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
