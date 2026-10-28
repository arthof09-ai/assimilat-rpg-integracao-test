"""R228 independent source/turn/physics proof, no native combat engine imports."""
from pathlib import Path
import json,hashlib,sqlite3
ROOT=Path(__file__).resolve().parents[1]
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def req(x,s):
 if not x:raise AssertionError(s)
def audit_one(p,case,seed,critical,ph,sourceh):
 c=sqlite3.connect('file:'+str(p)+'?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state'])
  rows=[json.loads(z[0]) for z in c.execute('select row_json from events order by seq')]
  receipts=list(c.execute('select seq,cmd_id,prev,row_sha,before_sha,after_sha from events order by seq'))
  pending=c.execute('select count(*) from pending').fetchone()[0]
 finally:c.close()
 req(len(rows)==int(m['revision'])==3 and not pending,'THREE_COMMITS')
 prev=m['genesis']
 for idx,(r,receipt) in enumerate(zip(rows,receipts),1):
  req(receipt==(idx,r['cmd_id'],r['prev'],sha(r),r['before_sha'],r['after_sha']),'SQL_EVENT_HASH')
  req(r['prev']==prev and r['official_effects']==0 and r['kind']==('R228_ARROW','R228_TARGET','R228_NEXT')[idx-1],'R18_SEQUENCE')
  prev=sha(r)
 req(prev==m['head'] and sha(st)==rows[-1]['after_sha'],'FINAL_STATE_HASH')
 req(st['phase']=='CENSORED_HORIZON' and st['source_hash']==sourceh and st['prereg_hash']==ph,'PHASE_AND_SOURCES')
 req(st['r228']['world_canon'] is False and st['r228']['target_speed_source']=='TEST_FROZEN_12M_NOT_WORLD_RULE','SOURCE_LIMIT')
 ev=st['native_events'];req(ev==sum([r['detail']['new_events'] for r in rows],[]),'EVENT_COPY')
 for idx,e in enumerate(ev,1):req(idx==e['seq'],'EVENT_SEQ')
 by={}
 for e in ev:by.setdefault(e['action'],[]).append(e)
 dec=by['R228_FLECHA_DECLARED'][0];rng=by['R228_RNG_TAPE'][0];fle=by['FLECHA_TRAVA_SOURCE_POST_HIT'][0];attack=by['weapon_attack'][0]
 req(dec['seq']<rng['seq']<attack['seq']<fle['seq'] and dec['PA_pledged']==55,'DECLARE_BEFORE_DICE')
 req(rng['critical']==critical and attack['critical_sequence']==critical,'PRE_REGISTERED_CRITICAL')
 req(len(rng['attack_dice'])==4 and all(1<=i<=6 for i in rng['attack_dice']),'ATTACK_4D6')
 req(len(rng['damage_dice'])==8 and all(1<=i<=10 for i in rng['damage_dice']),'DAMAGE_8D10')
 req(attack['attack_roll_attempts']==[rng['attack_dice']] and attack['roll_score']==sum(rng['attack_dice'])+101,'NATIVE_HIT_TAPE')
 req(attack['normal_damage']==sum(rng['damage_dice'])+33 and attack['ca_exact']=='83','FF_AND_CA')
 hit=(case=='HIT')
 req(attack['hit']==hit and (attack['critical']=='NEGATIVE')==(case=='NEG_CRIT_MISS'),'ATTACK_OUTCOME')
 net=max(0,attack['normal_damage']-35) if hit else 0
 req(attack['hp_loss_actual']==net and attack['after_hp']==734-net,'PHYSICAL_RD_HP')
 req(fle['pa_spent']==55 and fle['slow_applied']==hit and fle['speed_delta_m']==(-6 if hit else 0),'SOURCE_EFFECT_CHARGE')
 req(st['actors']['I']['pa']==429 and st['actors']['V']['hp']==734-net,'FINAL_PA_HP')
 mov=by['move'];req(len(mov)==2 and mov[0]['by']=='V' and mov[0]['travel_cost']=='5' and mov[1]['travel_cost']=='7','TWO_REAL_NATIVE_MOVEMENTS')
 req(mov[0]['speed']==('6' if hit else '12') and mov[1]['speed']=='12','SOURCE_TIMED_MOBILITY')
 req(mov[0]['from']=='(0, 0)' and mov[0]['to']=='(5,0)' and mov[1]['from']=='(5,0)' and mov[1]['to']=='(12,0)','POSITION_ACTUALLY_UPDATED')
 req(st['actors']['V']['position']=='(12,0)' and st['actors']['V']['timed_source_speed_penalty_m']==0,'FINAL_SPEED_POSITION')
 req(len(by.get('FLECHA_TRAVA_EXPIRES',[]))==(1 if hit else 0),'EXPIRY_INTERVAL')
 if hit:
  expiry=by['FLECHA_TRAVA_EXPIRES'][0]
  req(expiry['seq']>by['turn_end'][0]['seq'] and expiry['seq']<by['turn_start'][-1]['seq'],'EXPIRY_AFTER_TARGET_TURN')
 req(len(by['weapon_attack'])==2 and len(by['turn_start'])==2,'TARGET_ATTACK_AND_TURN_RENEWAL')
 return {'seed':seed,'case':case,'commits':3,'events':len(ev),'source_slow':hit,'target_moved_m':12,'arrow_PA':55,'physical_damage':net,'negative_critical_lab_only':case=='NEG_CRIT_MISS'}
def run(root=ROOT):
 root=Path(root);pre=(root/'sources/R228_PREREG_BEFORE_EXEC.json').read_bytes();p=json.loads(pre);ph=hashlib.sha256(pre).hexdigest()
 sh=hashlib.sha256((root/'sources/R228_ISKIEL_FROZEN_MECHANICAL_SOURCE.json').read_bytes()).hexdigest()
 req(p['candidate']=='R228' and len(p['scenes'])==2,'PREREG')
 files=list((root/'evidence/db').glob('*.sqlite'));req(len(files)==2,'NO_HIDDEN_FILES')
 out=[]
 for s in p['scenes']:
  db=root/'evidence/db'/f'R228_{s["case"]}_S{s["seed"]}.sqlite'
  req(db.exists(),'MISSING_SQLITE')
  out.append(audit_one(db,s['case'],s['seed'],s['critical'],ph,sh))
 q=list((root/'evidence/quarantine').glob('*sqlite'));req(len(q)==1 and 'PRECOMMIT_BAD_CMDID' in q[0].name,'PRECOMMIT_QUARANTINE')
 return {'status':'PASS_R228_INDEPENDENT_NATIVE_FLECHA_MOVEMENT_SQL_TEST','new_test_scenes':2,'native_physical_attacks':4,'real_moves':4,'successful_source_slow':1,'correct_expiries':1,'R18_commits':6,'events':sum(x['events'] for x in out),'quarantined_precommit':1,'historical_replays':0,'runs':out}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
