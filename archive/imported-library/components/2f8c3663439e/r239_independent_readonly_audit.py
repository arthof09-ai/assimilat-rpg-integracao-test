"""Independent R239 verifier: stdlib only; zero imports from native runner, r234, or R18."""
from __future__ import annotations
import json,hashlib,random,sqlite3,collections,math,sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
def require(cond,why):
 if not cond:raise AssertionError(why)
def can(obj):return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def hash_obj(obj):return hashlib.sha256(can(obj).encode()).hexdigest()
def file_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dice(seed,tag,n,faces):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'R239|{seed}|C|OWN1|{tag}|{n}d{faces}'.encode()).digest(),'big'))
 return [rng.randint(1,faces) for _ in range(n)]
def audit(root=ROOT,write=True,adversarial=False):
 root=Path(root);pre_bytes=(root/'sources/R239_PREREG.json').read_bytes();P=json.loads(pre_bytes);ph=hashlib.sha256(pre_bytes).hexdigest()
 beast_bytes=(root/'sources/R234_BEAST_FROZEN_EXCERPTS.json').read_bytes();be=json.loads(beast_bytes)['beasts'];bh=hashlib.sha256(beast_bytes).hexdigest()
 rule_bytes=(root/'sources/R236_FRACO_RULE_EXCERPT.json').read_bytes();rule=json.loads(rule_bytes);rh=hashlib.sha256(rule_bytes).hexdigest()
 require(P['source_max_hp']==be['C']['hp']==5580 and be['C']['speed']==50,'SOURCE_MAX_AND_SPEED')
 require(rule['source_status']=='PRIMARY_CANON_NORM_RULE_SUBSET' and 'hp < 10%' in rule['description'],'FRACO_SOURCE_DESCRIPTION')
 require(len(P['seeds'])==8 and len(P['arms'])==6 and len(set(P['seeds']))==8 and len({a['id'] for a in P['arms']})==6,'PREREG_DENOMINATOR')
 expect={(s,a['id']) for s in P['seeds'] for a in P['arms']}
 got={p.name for p in (root/'evidence/db').glob('*.sqlite')}
 expected_names={f'R239_{a}_S{s}.sqlite' for s,a in expect}
 require(got==expected_names, 'DENOMINATOR_EXPECTED_48_EXACT')
 byseed=collections.defaultdict(list)
 metrics={'seed_clusters':8,'matched_arms':48,'native_turns':0,'native_events':0,'weak_arms':0,'normal_arms':0,'hits':0,'damage_realized':0,'positive_critical':0,'negative_critical':0,'official_cells':0,'terminal_contracts':0,'official_deaths':0,'historical_replays':0,'pending_intents':0,'sqlite_integrity_pass':0}
 summary=[]
 for seed in P['seeds']:
  for arm in P['arms']:
   aid,hp=arm['id'],arm['hp']; path=root/'evidence/db'/f'R239_{aid}_S{seed}.sqlite'
   c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
   try:
    require(c.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLITE_INTEGRITY');metrics['sqlite_integrity_pass']+=1
    meta=dict(c.execute('SELECT key,value FROM meta'))
    require(c.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==0,'PENDING_INTENT')
    rows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
    require(len(rows)==int(meta['revision'])==1,'R18_ONE_COMMIT')
    s,cmd,prev,body,digest,bef,aft=rows[0];row=json.loads(body)
    require(s==1 and row['seq']==1 and cmd==f'LAB-CMD-R239-{aid}-{seed}' and row['cmd_id']==cmd,'CMD_ID_SEQ')
    require(prev==row['prev']==meta['genesis'] and digest==meta['head']==hash_obj(row),'R18_HASH_CHAIN')
    require(row['before_sha']==bef and row['after_sha']==aft,'R18_BEFORE_AFTER_BIND')
    require(row['synthetic'] is True and row['official_effects']==0 and row['kind']=='R239_WEAK_BOUNDARY_ONE_TURN','LAB_ONLY')
    require(row['payload']=={'seed':seed,'arm':aid,'who':'C','prereg_sha':ph,'source_sha':bh,'rule_sha':rh},'SOURCE_PREREG_PAYLOAD')
    state=json.loads(meta['state']);require(hash_obj(state)==aft,'SNAPSHOT_AFTER_SHA')
    r=state['r239'];require(r['seed']==seed and r['arm']==aid and r['prereg_sha']==ph and r['source_beast_sha']==bh and r['rule_sha']==rh,'SNAPSHOT_FROZEN_INPUTS')
    require(state['synthetic'] is True and state['phase']=='R239_ONE_TURN_TEST_STOP' and state['active'] is None and state['turn']==1 and state['winner'] is None,'STATE_END_NO_KO')
    require(r['initial_hp_croc']==hp and r['maxhp']==5580 and r['source_status']=='VZ-PRECREATE-NONP4','NONP4_AND_START_HP')
    require(r['official_benchmark'] is False and r['official_death'] is False and r['official_cells']==0 and r['final_effort'] is False,'NO_CANONICAL_PROMOTION')
    ev=row['detail']['events_new'];require([z['action'] for z in ev]==['turn_start','move','R239_SOURCE_TAPE','weapon_attack','turn_end'],'ATOMIC_5_EVENT_SEQUENCE')
    require(state['native_events']==ev and [z['seq'] for z in ev]==[1,2,3,4,5],'NO_EVENT_OVERWRITE')
    weak=(hp>0 and 10*hp<5580);speed='25' if weak else '50'
    start,movement,tape,attack,end=ev
    require(start['weak']==weak and start['speed']==speed and start['by']=='C','START_WEAK_SPEED')
    require(movement['by']=='C' and movement['from']=='(14,0)' and movement['to']=='(14,1)' and Fraction(movement['travel_cost'])==1 and movement['speed']==speed,'MOVEMENT_SCALED_AND_GATED')
    require(math.dist((14,1),(13,0))<=2,'CLOSE_MELEE_CONTRACT')
    a0,a1=dice(seed,'HIT0',6,6),dice(seed,'HIT1',6,6);damage=dice(seed,'DAMAGE',20,10);crit=dice(seed,'CRITICAL',3,6)
    attempts=[a0,a1] if weak else [a0];score=min(sum(z) for z in attempts)+134-2 if weak else sum(a0)+134
    require(tape['initial_hp']==hp and tape['maxhp']==5580 and tape['weak']==weak and tape['roll_score']==score,'TAPE_HP_WEAK_SCORE')
    require(tape['attack_attempts']==attempts and tape['hit0_common']==a0 and tape['hit1_reserved_draw']==a1,'MATCHED_RNG_ATTEMPTS')
    require(tape['damage_dice']==damage and tape['critical_sequence']==crit,'MATCHED_DAMAGE_CRIT')
    require(tape['prereg_sha']==ph and tape['source_beast_sha']==bh and tape['weak_rule_sha']==rh and tape['source_status']=='VZ-PRECREATE-NONP4' and tape['official_outcome'] is False,'TAPE_SOURCE_PROVENANCE')
    plus=crit[:2]==[6,6] and crit[2]>=5;minus=crit[:2]==[1,1] and crit[2]<=2
    hit=(score>be['G']['ca'] or plus) and not minus
    raw=(sum(damage)+200*int(plus)) if hit else 0
    rd=min(raw,be['G']['rd']);net=max(raw-rd,0);loss=min(net,be['G']['hp'])
    require(attack['weak_attacker']==weak and attack['net_levels']==(-1 if weak else 0),'NATIVE_WEAK_ATTACK_FLAG')
    require(attack['roll_score']==score and attack['attack_roll_attempts']==attempts and attack['critical_sequence']==crit,'NATIVE_SCORE_AND_RNG')
    require(attack['hit']==hit and attack['raw']==raw and attack['rd_applied']==rd and attack['net']==net,'NATIVE_HIT_RD_DAMAGE')
    require(attack['critical']==('POSITIVE' if plus else 'NEGATIVE' if minus else 'NONE'),'NATIVE_CRITICAL_TAPE')
    require(attack['hp_loss_actual']==loss and attack['before_hp']==be['G']['hp'] and attack['after_hp']==be['G']['hp']-loss and attack['official_death_derived'] is False,'NATIVE_HP_CLAMP_NO_DEATH')
    require(r['outcome']['weak']==weak and r['outcome']['speed_m']==speed and r['outcome']['attack_score']==score and r['outcome']['damage_to_G']==loss and r['outcome']['hit']==hit,'OUTCOME_PROOF')
    require(state['actors']['C']['hp']==hp and state['actors']['G']['hp']==be['G']['hp']-loss and state['actors']['C']['pa']==be['C']['pa'] and state['actors']['G']['pa']==be['G']['pa'],'HP_PA_FINAL_CONSERVATION')
    require(state['actors']['C']['standard']==0 and state['actors']['C']['movement']==0 and state['actors']['C']['position']=='(14,1)','ONE_TURN_ACTION_BUDGET')
    require(row['detail']['source_speed']==speed and row['detail']['weak']==weak and row['detail']['attack_score']==score,'DETAIL_REPLAY')
    metrics['native_turns']+=1;metrics['native_events']+=len(ev);metrics['weak_arms']+=int(weak);metrics['normal_arms']+=int(not weak);metrics['hits']+=int(hit);metrics['damage_realized']+=loss;metrics['positive_critical']+=int(plus);metrics['negative_critical']+=int(minus)
    byseed[seed].append({'arm':aid,'hp':hp,'score':score,'weak':weak,'hit0':a0,'hit1':a1,'damage_dice':damage,'critical':crit})
    summary.append({'seed':seed,'arm':aid,'hp':hp,'weak':weak,'speed':speed,'hit':hit,'damage':loss})
   finally:c.close()
 for seed,batch in byseed.items():
  require(len(batch)==6 and len({z['hp'] for z in batch})==6,'SEED_MATCHED_ARMS')
  for key in ('hit0','hit1','damage_dice','critical'):
   require(all(z[key]==batch[0][key] for z in batch),'CAUSAL_COMMON_RNG_'+key)
  high=[z for z in batch if z['hp']>=558];low=[z for z in batch if z['hp']<558]
  require(len(high)==4 and len(low)==2,'STRICT_10_PERCENT_PARTITION')
  require(len({z['score'] for z in high})==1 and len({z['score'] for z in low})==1,'SCORES_ONLY_CHANGE_AT_WEAK_THRESHOLD')
  require(low[0]['score']<=high[0]['score']-2,'WEAK_MUST_PENALIZE_SCORE')
 require(metrics['weak_arms']==16 and metrics['normal_arms']==32 and metrics['native_events']==240,'GLOBAL_COUNTS')
 out={'gate':'PASS_R239_BOUNDARY_LOCAL_INDEPENDENT_READONLY','counts':metrics,'eight_seed_clusters_not_48_independent':True,
   'scope':'VZ-PRECREATE-NONP4; source-combat-rule subset; one native turn per arm; no official rules changed',
   'negative_critical_consequence':'LAB policy only','official_death_rule':'HOLD','R91':'0/1875','terminal_contracts':'0/17','details':summary}
 if write:(root/'reports/R239_INDEPENDENT_SQL_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='details'},indent=2,ensure_ascii=False))
 return out
if __name__=='__main__':audit()
