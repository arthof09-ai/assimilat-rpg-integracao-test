"""Independent R232 auditor: stdlib sqlite3 RO, no VLAB engine or runner import."""
import sqlite3,json,hashlib,random,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def check(v,msg):
 if not v:raise AssertionError(msg)
def roll(seed,label,n,f):
 h=int.from_bytes(hashlib.sha256(f'R232|{seed}|{label}|{n}d{f}'.encode()).digest(),'big');r=random.Random(h)
 return [r.randint(1,f) for _ in range(n)]
def read(path):
 c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
 try:
  meta=dict(c.execute('select key,value from meta'))
  state=json.loads(meta['state']);events=[]
  for seq,cmd,prev,row_json,row_sha,before_sha,after_sha in c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'):
   row=json.loads(row_json);check(sha(row)==row_sha and row['seq']==seq and row['cmd_id']==cmd and row['prev']==prev,'R18_ROW_SHA');events.append((row,row_sha,before_sha,after_sha))
  pending=c.execute('select count(*) from pending').fetchone()[0]
  return meta,state,events,pending
 finally:c.close()
def audit(root=ROOT,write=True):
 root=Path(root);sb=(root/'sources/R232_VZ_FROZEN_PRIMARY_EXCERPTS.json').read_bytes();pb=(root/'sources/R232_PREREG_BEFORE_EXEC.json').read_bytes()
 src=json.loads(sb);pre=json.loads(pb);SH=hashlib.sha256(sb).hexdigest();PH=hashlib.sha256(pb).hexdigest();sp_by={x['id']:x for x in src['attacks']}
 check(len(sp_by)==4 and len(pre['seeds'])==len(pre['species'])==4,'SPECIES_DENOMINATOR')
 paths=list((root/'evidence/db').glob('*.sqlite'));check(len(paths)==4,'FOUR_NEW_SQLITE')
 result=[]
 for seed,sid in zip(pre['seeds'],pre['species']):
  path=root/'evidence/db'/f'R232_{sid}_S{seed}.sqlite';check(path.exists(),'EXPECTED_DB_MISSING')
  m,state,rows,pending=read(path);check(int(m['revision'])==len(rows)==1 and pending==0,'R18_ONE_VALID_COMMIT')
  row,hash_,before,after=rows[0]
  check(row['prev']==m['genesis'] and hash_==m['head'] and after==sha(state),'R18_HEAD_BEFORE_AFTER')
  check(row['detail']['new_events']==state['native_events'],'R18_EVENT_COMMIT_ATOMIC')
  check(state['phase']=='CENSORED_SINGLE_ATTACK_NOT_FIGHT' and state['seed']==seed and state['synthetic'] is True and state['winner'] is None,'CENSORED_ONLY')
  q=state['r232'];check(q['source_sha']==SH and q['prereg_sha']==PH and q['species_id']==sid and q['seed']==seed,'SOURCE_SHA_PREREG')
  check(q['source_status']=='VZ-PRECREATE-NOT-P4' and q['actor_hp_ca']=='LAB_INTERFACE_STANDINS_1HP_0CA' and q['beast_full_stats']=='UNKNOWN' and q['referenced_target_source']=='VAROK-PROPOSED','NO_CANON_INFERENCE')
  check(state['actors']['BE']['hp']==1 and state['actors']['BE']['ca']=='0' and state['actors']['BE']['standard']==0,'ATTACKER_INTERFACE_PLACEHOLDER')
  sp=sp_by[sid];events=state['native_events'];check(len(events)==2 and [x['seq'] for x in events]==[1,2],'TWO_NATIVE_EVENTS')
  tape,at=events;check(tape['action']=='R232_FROZEN_RNG_TAPE' and tape['species_id']==sid and tape['source_sha']==SH and tape['source_action']==sp['action'] and tape['source_name']==sp['name'],'TAPE_SOURCE_IDENTITY')
  check(tape['critical_evidence']==[3,4,3] and tape['policy']=='DIRECTED_NONCRIT_LAB_ONLY','CRITICAL_DIRECTION')
  an,af=map(int,sp['attack_dice'].split('d'));dn,df=map(int,sp['damage_dice'].split('d'))
  atk_expected=roll(seed,sid+'-ATTACK',an,af);dmg_expected=roll(seed,sid+'-DAMAGE',dn,df)
  check(tape['attack_rolls']==atk_expected and tape['damage_rolls']==dmg_expected,'SHA_RNG_TAPE')
  score=sum(atk_expected)+sp['attack_bonus'];hit=(score>src['reference_target']['ca']);gross=sum(dmg_expected) if hit else 0
  postrd=max(0,gross-src['reference_target']['physical_rd']) if hit else 0;actual=min(postrd,src['reference_target']['hp'])
  check(at['action']=='weapon_attack' and at['from']=='BE' and at['to']=='VAROK' and at['attack_origin']=='NORMAL' and at['critical']=='NONE','ENGINE_NATIVE_STANDARD_NONCRIT')
  check(at['roll_score']==score and at['ca_exact']==str(src['reference_target']['ca']) and at['hit']==hit,'HIT_SOURCE_CA')
  check(at['damage_roll_groups']==[dmg_expected] and at['attack_roll_attempts']==[atk_expected] and at['normal_damage']==sum(dmg_expected),'SOURCE_ATTACK_DICE')
  check(at['raw']==gross and at['rd_applied']==(min(gross,src['reference_target']['physical_rd']) if hit else 0),'RAW_RD_MATH')
  check(at['net']==postrd and at['hp_loss_actual']==actual and at['after_hp']==src['reference_target']['hp']-actual,'POSTRD_HP_MATH')
  check(at['before_hp']==src['reference_target']['hp'] and state['actors']['VAROK']['hp']==at['after_hp'],'TARGET_SNAPSHOT_CONSISTENCY')
  check(q['outcome']['damage']==actual and q['outcome']['varok_hp']==at['after_hp'] and q['outcome']['hit']==hit and q['outcome']['official_benchmark'] is False,'OUTCOME_IS_NOT_CANON')
  result.append({'species':sp['name'],'source_id':sid,'rank':sp['rank'],'seed':seed,'hit':hit,'attack_score':score,'damage_before_rd':gross,'rd':at['rd_applied'],'hp_removed':actual,'full_fight':False})
 # Quarantine preflight failure that occurred before candidate event callback or publication.
 qfiles=list((root/'evidence/quarantine').glob('*.sqlite'));check(len(qfiles)==1,'ONE_V0_QUARANTINE')
 qm,qs,qr,qp=read(qfiles[0]);check(len(qr)==0 and int(qm['revision'])==0 and qp==0,'V0_NEVER_COMMITTED')
 output={'status':'PASS_R232_INDEPENDENT_NAMED_BEAST_ATTACKS_TEST_CONDITIONAL','native_sqlite_valid':4,'commits':4,'events':8,'unique_precreated_beast_names':4,'full_beast_fights':0,'official_battery_D_cells':0,'quarantined_preflight':1,'historical_replays':0,'cases':result}
 if write:(root/'evidence/reports/R232_INDEPENDENT_AUDIT.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(output,ensure_ascii=False,indent=2));return output
if __name__=='__main__':audit()
