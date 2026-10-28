"""R236 independent SQLite read-only audit of Fraco disadvantage, movement halving, HP0 stop. No runner/native imports."""
import hashlib,json,random,sqlite3,math
from pathlib import Path
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
def check(v,k):
 if not v:raise AssertionError(k)
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def dice(seed,who,own,label,n,f):
 h=int.from_bytes(hashlib.sha256(f'R236|{seed}|{who}|OWN{own}|{label}|{n}d{f}'.encode()).digest(),'big');q=random.Random(h);return [q.randint(1,f) for _ in range(n)]
def read(path):
 c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rows=[]
  for seq,cmd,prev,body,hash_,before,after in c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'):
   row=json.loads(body);check(row['seq']==seq and row['cmd_id']==cmd and row['prev']==prev and row['before_sha']==before and row['after_sha']==after and sha(row)==hash_,'R18_ROW_SHA')
   rows.append((row,hash_))
  return m,st,rows,c.execute('select count(*) from pending').fetchone()[0]
 finally:c.close()
def audit(root=R,write=True):
 root=Path(root)
 ps=(root/'sources/R236_PREREG_BEFORE_EXEC.json').read_bytes();pre=json.loads(ps);ph=hashlib.sha256(ps).hexdigest()
 bs=(root/'sources/R234_BEAST_FROZEN_EXCERPTS.json').read_bytes();be=json.loads(bs)['beasts'];bh=hashlib.sha256(bs).hexdigest()
 rs=(root/'sources/R236_FRACO_RULE_EXCERPT.json').read_bytes();rule=json.loads(rs);rh=hashlib.sha256(rs).hexdigest()
 check(pre['seeds']==[23661001,23661002,23661003,23661004,23661005,23661006] and len(pre['arms'])==2,'SOURCES_FIXED')
 check(pre['initial_hp_croc']==95 and pre['source_maxhp_croc']==5580 and 95*10<5580 and be['C']['hp']==5580,'FRACO_SOURCE_THRESHOLD')
 check(rule['source_status']=='PRIMARY_CANON_NORM_RULE_SUBSET' and rule['description'].startswith('Fraco se hp < 10%'),'CANON_FRACO')
 d=list((root/'evidence/db').glob('*.sqlite'));check(len(d)==12,'DENOMINATOR_12')
 totals={'arms':0,'seed_pairs':6,'commits':0,'native_events':0,'attacks':0,'hits':0,'move':0,'weak_attacks':0,'weak_moves':0,'hp0_lab_stops':0,'blocked_future_turns':0,'actual_hp_loss':0};end=[];streams={}
 for seed in pre['seeds']:
  for arm in pre['arms']:
   f=root/'evidence/db'/f'R236_{arm}_S{seed}.sqlite';check(f.exists(),'EXPECTED_DB')
   m,st,rows,pending=read(f);order=pre['order'][arm];check(pending==0 and len(rows)==int(m['revision'])>0,'R18_VALID_COMMIT_COUNT')
   s=st['r236'];check(s['seed']==seed and s['arm']==arm and s['rule_sha']==rh and s['source_beast_sha']==bh and s['prereg_sha']==ph,'FROZEN_SOURCE_AND_PREREG')
   check(s['source_status']=='VZ-PRECREATE-NONP4' and s['croc_initial_lab_wound_hp']==95 and s['croc_source_max_hp']==5580 and s['final_effort_declared'] is False,'NONCANON_INIT_WOUND_AND_OPTIONAL_FINALE')
   hp={a:(95 if a=='C' else be[a]['hp']) for a in order};pa={a:be[a]['pa'] for a in order};pos={a:'(0,0)' if a=='G' else '(2,0)' if a=='R' else '(14,0)' for a in order};own={a:0 for a in order};revturn=0;trace=[];phead=m['genesis'];last_after=None;hits=0;loss_sum=0;move=0;weak_count=0;weak_move=0
   for row,digest in rows:
    check(row['prev']==phead and (last_after is None or row['before_sha']==last_after),'R18_COMPLETE_CHAIN')
    phead=digest;last_after=row['after_sha'];who=order[(row['seq']-1)%len(order)] if st['phase']=='CENSORED_HORIZON' else order[(row['seq']-1)%len(order)]
    # Before STOP there is always contiguous scheduled actor sequence, no skipped future turn.
    own[who]+=1;turn=own[who];payload=row['payload'];check(payload=={'arm':arm,'seed':seed,'who':who,'own':turn,'prereg_sha':ph,'source_sha':rh},'SCHEDULER_ROUND_AND_SOURCE')
    fresh=row['detail']['events_new'];expected=['turn_start']+(['move'] if turn==1 else [])+['R236_WEAK_SOURCE_RNG_TAPE','weapon_attack','turn_end']
    check([z['action'] for z in fresh]==expected,'NATIVE_ACTION_BUDGET_EVENTS')
    first=fresh[0];weak=hp[who]*10<be[who]['hp'];speed=be[who]['speed']//2 if weak else be[who]['speed']
    check(first['by']==who and first['weak']==weak and Fraction(first['speed'])==Fraction(speed),'START_FRACO_AND_SPEED')
    if turn==1:
     v=fresh[1];to={'G':'(12.5,0)','C':'(14,1)','R':'(15,0)'}[who];cost={'G':'25/2','C':'1','R':'13'}[who]
     check(v['by']==who and v['from']==pos[who] and v['to']==to and v['travel_cost']==cost and Fraction(v['speed'])==Fraction(speed) and Fraction(cost)<=speed,'ACTUAL_MOVEMENT_FRACO_LEGAL')
     pos[who]=to;move+=1;weak_move+=int(weak)
    tap=fresh[-3];atk=fresh[-2];check(tap['by']==who and atk['from']==who and fresh[-1]['by']==who,'SAME_TURN_ACTOR')
    target='C' if who in ('G','R') else 'G'
    check(tap['to']==target and atk['to']==target,'SOURCE_TARGET_POLICY')
    dpos=lambda x:tuple(float(v) for v in x.strip('()').split(','))
    check(math.dist(dpos(pos[who]),dpos(pos[target]))<=2,'DECLARED_MELEE_DISTANCE')
    attempt=(dice(seed,who,turn,'HIT0',6,6),dice(seed,who,turn,'HIT1',6,6)) if weak else (dice(seed,who,turn,'HIT0',6,6),)
    dmg=dice(seed,who,turn,'DAMAGE',20,10);crit=dice(seed,who,turn,'CRITICAL',3,6)
    check(tap['weak']==weak and tap['attack_attempts']==list(attempt) and tap['damage_rolls']==dmg and tap['critical_sequence']==crit and tap['final_effort_not_declared'] is True,'SOURCE_WEAK_RNG_TRACE')
    score=min(sum(t)+be[who]['attack_bonus'] for t in attempt)-2 if weak else sum(attempt[0])+be[who]['attack_bonus']
    positive=crit[:2]==[6,6] and crit[2]>=5;negative=crit[:2]==[1,1] and crit[2]<=2
    hit=(score>be[target]['ca'] or positive) and not negative;raw=(sum(dmg)+200*int(positive)) if hit else 0;rd=min(raw,75);net=max(0,raw-rd);loss=min(net,hp[target]);hits+=int(hit);loss_sum+=loss;weak_count+=int(weak)
    check(tap['roll_score']==score and atk['roll_score']==score and atk['weak_attacker']==weak and atk['net_levels']==(-1 if weak else 0),'NATIVE_DISADVANTAGE_SCORE')
    check(atk['attack_roll_attempts']==list(attempt) and atk['critical_sequence']==crit and atk['critical']==('POSITIVE' if positive else 'NEGATIVE' if negative else 'NONE') and atk['hit']==hit,'CRITICAL_PROOF')
    check(atk['raw']==raw and atk['rd_applied']==rd and atk['net']==net and atk['hp_loss_actual']==loss and atk['overkill']==max(0,net-hp[target]),'HP0_CLAMP_AND_RD')
    check(atk['before_hp']==hp[target] and atk['after_hp']==hp[target]-loss and atk['official_death_derived'] is False,'HP0_NOT_DEATH')
    hp[target]-=loss
    trace.extend(fresh);check([x['seq'] for x in fresh]==list(range(len(trace)-len(fresh)+1,len(trace)+1)),'EVENT_CHAIN_ORDER')
    streams.setdefault((seed,who,turn),{})[arm]=(attempt,dmg,crit)
    check(row['official_effects']==0 and row['synthetic'] is True,'NO_CANON')
    revturn+=1
    if hp[target]==0:check(row==rows[-1][0] and row['detail']['phase']=='STOP_HP0_LAB_ONLY' and row['detail']['active_after'] is None,'IMMEDIATE_HP0_CANCELS_FUTURE_TURNS')
   check(m['head']==phead and row['after_sha']==sha(st),'R18_FINAL_STATE_SHA')
   check(st['native_events']==trace and st['phase']=='STOP_HP0_LAB_ONLY' and st['winner'] is None and st['r236']['outcome']['official_death'] is False,'LAB_STOP_NOT_CANON_KO')
   check({a:st['actors'][a]['hp'] for a in order}==hp and {a:st['actors'][a]['pa'] for a in order}==pa,'FINAL_HP_PA_CONSERVATION')
   check(all(st['actors'][a]['maximum_hp']==be[a]['hp'] and Fraction(st['actors'][a]['base_speed'])==Fraction(be[a]['speed']) and Fraction(st['actors'][a]['ca'])==Fraction(be[a]['ca']) for a in order),'SOURCE_FINAL_MAXHP_CA_SPEED')
   check(st['r236']['own_turns']==own and st['r236']['hits']==hits and st['r236']['actual_hp_loss']==loss_sum and st['r236']['moves']==move and st['r236']['attacks']==len(rows),'RUN_COUNTERS')
   totals['arms']+=1;totals['commits']+=len(rows);totals['native_events']+=len(trace);totals['attacks']+=len(rows);totals['hits']+=hits;totals['move']+=move;totals['weak_attacks']+=weak_count;totals['weak_moves']+=weak_move;totals['hp0_lab_stops']+=1;totals['actual_hp_loss']+=loss_sum;totals['blocked_future_turns']+=6*len(order)-len(rows)
   end.append({'seed':seed,'arm':arm,'turns_before_HP0':len(rows),'C_hp_final':hp['C'],'Grifo_hp_final':hp['G'],'ROC_present':arm.startswith('TEAM'),'weak_croc_turns':own['C']})
 # Shared per-actor/own-turn tape when both actors survived to that turn; never force matching after stop.
 common=0
 for z,arm_tapes in streams.items():
  if len(arm_tapes)==2:
   a,b=pre['arms'];check(arm_tapes[a]==arm_tapes[b],'PAIRED_COMMON_ATTACK_TAPE');common+=1
 assert common>0
 out={'status':'PASS_R236_FRACO_WEAK_HP0_INTERRUPT_NATIVE_CONDITIONAL','counts':totals,'common_tape_actor_turns':common,'source_precreate_not_P4':True,'official_KO':0,'terminal_contracts':0,'official_battery_cells':0,'historical_replays':0,'outcomes':end}
 if write:(root/'evidence/reports/R236_INDEPENDENT_SQL_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2));return out
if __name__=='__main__':audit()
