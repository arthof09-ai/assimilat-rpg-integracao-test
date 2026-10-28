"""Independent SQLite-only R230 verifier: read-only, no combat-engine imports."""
import sqlite3,json,hashlib,collections
from pathlib import Path
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def require(v,k):
 if not v:raise AssertionError(k)
def read(db):
 c=sqlite3.connect(f'file:{db}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rows=[]
  for item in c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'):
   s,cmd,prev,rj,rsha,before,after=item;r=json.loads(rj);require(sha(r)==rsha and r['seq']==s and r['cmd_id']==cmd and r['prev']==prev,'R18_ROW_CHAIN');rows.append((r,rsha))
  pending=c.execute('select count(*) from pending').fetchone()[0]
  return m,st,rows,pending
 finally:c.close()
def audit(root=R,write=True):
 root=Path(root);preb=(root/'sources/R230_PREREG_BEFORE_EXEC.json').read_bytes();srcb=(root/'sources/R230_BEAST_SPEED_RULE_EXCERPT.json').read_bytes()
 pre=json.loads(preb);src=json.loads(srcb);ph=hashlib.sha256(preb).hexdigest();sh=hashlib.sha256(srcb).hexdigest()
 assert len(pre['seeds'])==len(pre['rank_stars'])==5
 paths=list((root/'evidence/db').glob('*.sqlite'));require(len(paths)==5,'NUM_VALID_DBS')
 result=[]
 for seed,(rank,star) in zip(pre['seeds'],pre['rank_stars']):
  path=root/'evidence/db'/f'R230_BE_{rank.replace(" ","")}{star}_S{seed}.sqlite'
  require(path.exists(),'DB_MISSING');m,st,rows,pending=read(path)
  require(len(rows)==int(m['revision'])==1 and pending==0,'R18_VALID_COMMIT_ONE')
  rr,rsha=rows[0];require(rr['prev']==m['genesis'] and rsha==m['head'] and rr['after_sha']==sha(st),'R18_META_CHAIN')
  require(st['r230']['seed']==seed and st['phase']=='CENSORED_AFTER_ONE_BE_TURN','TEST_PHASE')
  q=st['r230'];require(q['prereg_sha']==ph and q['source_excerpt_sha']==sh and q['rank']==rank,'SOURCE_BINDING')
  require(q['world_canon'] is False and q['physical_species'] is None and q['beast_stat_origin']=='LAB_DISTRIBUTION_ONLY','SOURCE_NOT_SPECIES')
  is_titan=rank=='Lendário'
  require(q['titan']==is_titan,'TITAN_LEGEND')
  rule=src['titan' if is_titan else 'normal'][rank]
  sp=Fraction(int(rule.split('+')[0]))+Fraction(q['beast_attrs']['DES'],4)
  require(Fraction(q['source_speed_exact'])==sp and q['source_speed_formula']==rule,'NORMATIVE_R8_SPEED')
  events=st['native_events'];require(len(events)==3 and events==rr['detail']['new_events'],'NATIVE_EVENT_CONSISTENCY')
  move,tape,atk=events
  require([e['seq'] for e in events]==[1,2,3],'CAUSAL_SEQ')
  require(move['action']=='move' and move['by']=='BE' and move['from']=='(0,0)' and move['speed']==str(sp),'MOVEMENT_SOURCE')
  require(Fraction(move['travel_cost'])==int(sp) and move['to']==f'({int(sp)},0)' and Fraction(move['travel_cost'])<=sp,'MOVEMENT_WITHIN_SOURCE_SPEED')
  require(tape['action']=='R230_BE_PRE_REGISTERED_RNG_TAPE' and tape['mode']=='DIRECTED_NONCRIT_LAB_ONLY','PRE_ATTACK_TAPE')
  roll=tape['dice_attack'];dd=tape['dice_damage'];critical=tape['dice_critical']
  expected_expr=src['base_damage_titan' if is_titan else 'base_damage_normal'][rank]
  require(q['beast_damage_base']==expected_expr,'NORMATIVE_BASE_DAMAGE')
  n,face=map(int,expected_expr.split('d'));an,af=map(int,q['beast_attack_test_dice'].split('d'))
  require(len(roll)==an and all(1<=i<=af for i in roll),'RANK_ATTACK_DICE')
  require(len(dd)==n and all(1<=i<=face for i in dd),'BASE_DMG_DICE')
  require(critical==[3,4,3],'PREDECLARED_NONCRIT')
  prof=src['prof_titan' if is_titan else 'prof_normal'][rank]
  bonus=q['beast_attrs']['FOR']+prof
  require(q['outcome']['beast_attack_bonus']==bonus and atk['roll_score']==sum(roll)+bonus,'ATTACK_BONUS')
  require(atk['attack_roll_attempts']==[roll] and atk['damage_roll_groups']==[dd],'TAPES_USED_BY_NATIVE')
  require(atk['action']=='weapon_attack' and atk['from']=='BE' and atk['to']=='ED' and atk['critical']=='NONE','NATIVE_BASE_ATTACK')
  require(atk['normal_damage']==sum(dd) and atk['raw']==sum(dd) and atk['rd_applied']==0,'DAMAGE_RD')
  require(atk['hit']==(atk['roll_score']>11) and atk['before_hp']==22,'HIT_CA')
  raw=sum(dd) if atk['hit'] else 0;actual=min(raw,22)
  require(atk['hp_loss_actual']==actual and st['actors']['ED']['hp']==22-actual,'HP_CONSERVATION')
  require(st['actors']['BE']['position']==move['to'] and st['actors']['BE']['movement']==0 and st['actors']['BE']['standard']==0,'ACTIONS_SPENT')
  require(st['actors']['BE']['base_speed']==str(sp) and st['actors']['BE']['hp']==q['beast_hp'],'FINAL_ACTOR')
  require(q['outcome']['ED_hp_after']==22-actual and q['outcome']['attack_net']==actual,'RECEIPT_ACCURACY')
  result.append({'rank':rank,'star':star,'seed':seed,'source_speed':str(sp),'travel_distance':int(sp),'native_events':len(events),'attack_hit':atk['hit'],'damage_to_ED':actual,'lab_actor_zero_hp':st['actors']['ED']['hp']==0})
 quarantines=list((root/'evidence/quarantine').glob('*.sqlite'));require(len(quarantines)==3,'THREE_QUARANTINE_IDS')
 qtable=[]
 for item in quarantines:
  m,st,rows,pending=read(item)
  require(len(rows)==0 and int(m['revision'])==0,'QUAR_NO_VALID_COMMIT')
  require(pending in (0,1),'QUAR_PENDING_CLASS')
  qtable.append({'db':item.name,'pending_intents':pending,'commits':len(rows)})
 out={'status':'PASS_R230_INDEPENDENT_R18_NATIVE_BEAST_SPEED_TEST_CONDITIONAL','valid_r18_db':5,'commits':5,'native_moves':5,'native_physical_attacks':5,
 'source_derived_meters_not_arbitrary':True,'full_sourced_species':0,'official_fights':0,'historical_replays':0,'quarantined':qtable,'cases':result}
 if write:(root/'evidence/reports/R230_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2));return out
if __name__=='__main__':audit()
