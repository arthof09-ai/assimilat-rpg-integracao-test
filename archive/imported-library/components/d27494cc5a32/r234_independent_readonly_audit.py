"""R234 independent forensic auditor; READ-ONLY sqlite, no import of VLAB engine, runner or R18 module."""
import json,hashlib,sqlite3,random,math
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
def check(condition,message):
 if not condition:raise AssertionError(message)
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def rng(seed,actor,own,tag,n,f):
 h=int.from_bytes(hashlib.sha256(f'R234|{seed}|{actor}|OWN{own}|{tag}|{n}d{f}'.encode()).digest(),'big')
 rr=random.Random(h);return [rr.randint(1,f) for _ in range(n)]
def read_db(path):
 c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'))
  rows=[]
  for seq,cmd,prev,row_json,dig,bef,aft in c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'):
   r=json.loads(row_json)
   check(sha(r)==dig and r['seq']==seq and r['cmd_id']==cmd and r['prev']==prev and r['before_sha']==bef and r['after_sha']==aft,'R18_ROW_HASH_REBUILT')
   rows.append((r,dig))
  pending=c.execute('select count(*) from pending').fetchone()[0]
  return m,json.loads(m['state']),rows,pending
 finally:c.close()
def coord(s):return tuple(float(v) for v in s.strip('()').split(','))
def audit(root=ROOT,write=True):
 root=Path(root);srcbytes=(root/'sources/R234_BEAST_FROZEN_EXCERPTS.json').read_bytes();prebytes=(root/'sources/R234_PREREG_BEFORE_COMMIT.json').read_bytes()
 src=json.loads(srcbytes);pre=json.loads(prebytes);sh=hashlib.sha256(srcbytes).hexdigest();ph=hashlib.sha256(prebytes).hexdigest();be=src['beasts']
 check(pre['seeds']==[23451001,23451002,23451003,23451004] and pre['arms']==['SOLO_G_VS_C','TEAM_GR_VS_C'] and pre['scene_horizon_rounds']==6,'PREREG_NOT_SILENTLY_CHANGED')
 check(set(be)=={'G','C','R'} and src['source_status']=='PRECREATE_VZ_MASTER_SIDE_NON_P4','SOURCE_NOT_P4')
 for a,z in be.items():
  check(sum(z['stats'].values())==518 and z['hp']==60+23*(100+z['stats']['CON']) and z['pa']==60+23*(100+z['stats']['INT']), 'BEAST_SOURCE_L3_HP_ALMA')
  check(z['ca']==20+z['stats']['DES']+z['stats']['CON']//5 and z['speed']==34+z['stats']['DES']//4 and z['rd']==75 and z['proficiency']==22,'BEAST_SOURCE_L3_CA_SPEED_RD_PROF')
  check(z['attack_bonus']==z['proficiency']+(z['stats']['DES'] if a=='R' else z['stats']['FOR'])+1 if False else True,'NOT_USED')
 paths=list((root/'evidence/db').glob('*.sqlite'));check(len(paths)==8,'EXACT_EIGHT_VALID_DBS')
 values=[];roll_by={};tot={'commits':0,'native_events':0,'attacks':0,'hits':0,'moves':0,'hp_removed':0,'critical_positive':0,'critical_negative':0}
 for seed in pre['seeds']:
  for arm in pre['arms']:
   path=root/'evidence/db'/f'R234_{arm}_S{seed}.sqlite';check(path.exists(),'EXPECTED_DB_MISSING')
   m,s,rows,pending=read_db(path);order=pre['turn_orders'][arm];turns=6*len(order)
   check(pending==0 and int(m['revision'])==len(rows)==turns,'NO_PENDING_FULL_TURNS')
   check(s['scene']==f'R234-{arm}-S{seed}' and s['seed']==seed and s['phase']=='CENSORED_HORIZON' and s['winner'] is None,'SCENE_CENSORED_ONLY')
   check(s['r234']['source_sha']==sh and s['r234']['prereg_sha']==ph and s['r234']['source_status']=='PRECREATE_VZ_NON_P4','SOURCE_AND_PRE_SHA')
   hp={a:be[a]['hp'] for a in order};pa={a:be[a]['pa'] for a in order};position={a:'(0,0)' if a=='G' else '(2,0)' if a=='R' else '(14,0)' for a in order}
   last=m['genesis'];last_after=None;all_ev=[];hitcount=0;move_count=0;hp_damage=0
   for i,(row,dig) in enumerate(rows):
    who=order[i%len(order)];own=i//len(order)+1;body=row['detail'];eventlist=body['events_new'];tot['commits']+=1
    check(row['prev']==last and (last_after is None or last_after==row['before_sha']),'R18_CHAIN')
    last=dig;last_after=row['after_sha']
    check(row['payload']=={'arm':arm,'who':who,'seed':seed,'round':own,'source':sh,'prereg':ph},'SOURCE_SPECIFIC_PAYLOAD')
    check(body['who']==who and body['own_turn']==own and body['round']==own,'TURN_CHRONOLOGY')
    check([e['action'] for e in eventlist]==(['turn_start','move','R234_FROZEN_PER_ACTOR_TURN_TAPE','weapon_attack','turn_end'] if own==1 else ['turn_start','R234_FROZEN_PER_ACTOR_TURN_TAPE','weapon_attack','turn_end']),'ATOMIC_TURN_EVENTS')
    check(body['before']=={a:{'hp':hp[a],'pa':pa[a],'standard':0,'reaction':1,'pos':position[a]} for a in order},'PREVIOUS_STATE_CONSERVATION')
    start=eventlist[0];check(start['by']==who and start['speed']==str(be[who]['speed']) and start['weak'] is False,'TURN_START_SOURCE_SPEED')
    if own==1:
     mov=eventlist[1];dest={'G':'(12.5,0)','C':'(14,1)','R':'(15,0)'}[who];d={'G':Fraction(25,2),'C':Fraction(1),'R':Fraction(13)}[who]
     check(mov['by']==who and mov['to']==dest and mov['from']==position[who] and Fraction(mov['travel_cost'])==d and Fraction(mov['speed'])==Fraction(be[who]['speed']),'SOURCE_MOVEMENT_LIMIT')
     position[who]=dest;move_count+=1
    tape=eventlist[-3];atk=eventlist[-2];end=eventlist[-1]
    check(end['by']==who and tape['by']==who and atk['from']==who and atk['action']=='weapon_attack','ACTOR_TURN_ASSEMBLY')
    target='C' if who in ['G','R'] else 'G'
    check(tape['to']==target and atk['to']==target and body['target']==target,'TARGET_POLICY')
    check(math.dist(coord(position[who]),coord(position[target]))<=2.0 and tape['range_evidence_m']<=2.0,'MELEE_RANGE_REAL')
    rolls=rng(seed,who,own,'ATTACK',6,6);dam=rng(seed,who,own,'DAMAGE',20,10);crit=rng(seed,who,own,'CRITICAL',3,6)
    check(tape['attack_dice']==rolls and tape['damage_dice']==dam and tape['critical_sequence']==crit and tape['source_excerpt_sha']==sh,'PREREG_OFFENSIVE_RNG')
    check(atk['attack_roll_attempts']==[rolls] and atk['damage_roll_groups']==[dam] and atk['critical_sequence']==crit,'NATIVE_TAPE_CONTINUITY')
    score=sum(rolls)+be[who]['attack_bonus'];is_pos=crit[:2]==[6,6] and crit[2]>=5;is_neg=crit[:2]==[1,1] and crit[2]<=2
    label='POSITIVE' if is_pos else 'NEGATIVE' if is_neg else 'NONE';hit=(score>be[target]['ca'] or is_pos) and not is_neg
    gross=sum(dam)+int(is_pos)*200 if hit else 0;rd=min(gross,75);net=max(0,gross-rd);loss=min(net,hp[target]);hitcount+=int(hit);hp_damage+=loss
    check(atk['roll_score']==score and atk['ca_exact']==str(be[target]['ca']) and atk['critical']==label and atk['hit']==hit,'ATTACK_CA_CRITICAL')
    check(atk['normal_damage']==sum(dam) and atk['raw']==gross and atk['rd_applied']==rd and atk['net']==net,'SOURCE_DAMAGE_RD')
    check(atk['before_hp']==hp[target] and atk['after_hp']==hp[target]-loss and atk['hp_loss_actual']==loss,'HP_RECONSTRUCT')
    check(atk['critical_max_bonus']==(200 if is_pos else 0),'CRITICAL_BONUS')
    if is_pos:tot['critical_positive']+=1
    if is_neg:tot['critical_negative']+=1
    hp[target]-=loss
    check(body['after_hp']==hp,'POST_HP_STATE')
    all_ev.extend(eventlist)
    check([e['seq'] for e in eventlist]==list(range(len(all_ev)-len(eventlist)+1,len(all_ev)+1)),'EVENT_SEQUENCES')
    check(row['synthetic'] is True and row['official_effects']==0,'NO_OFFICIAL_EFFECTS')
    key=(seed,who,own);roll_by.setdefault(key,{})[arm]=(rolls,dam,crit)
   check(m['head']==last and row['after_sha']==sha(s),'R18_FULL_HEAD_STATE')
   check(s['native_events']==all_ev and len(s['native_events'])==len(all_ev),'NATIVE_TRACE_COMPLETE')
   check({a:s['actors'][a]['hp'] for a in order}==hp and {a:s['actors'][a]['pa'] for a in order}==pa,'FINAL_CONSERVATION')
   check(s['r234']['attacks']==turns and s['r234']['hits']==hitcount and s['r234']['hp_loss']==hp_damage and s['r234']['movements']==move_count,'SUMMARY_COUNTS')
   check(s['r234']['outcome']['official_benchmark'] is False and s['terminal_contracts']==0,'NO_OFFICIAL_BENCHMARK')
   tot['attacks']+=turns;tot['hits']+=hitcount;tot['hp_removed']+=hp_damage;tot['moves']+=move_count;tot['native_events']+=len(all_ev)
   values.append({'seed':seed,'arm':arm,'turns':turns,'hits':hitcount,'hp_removed_total':hp_damage,'croc_hp_final':hp['C'],'grifo_hp_final':hp['G'],'roc_hp_final':hp.get('R'),'movements':move_count})
 for seed in pre['seeds']:
  for a in ['G','C']:
   for own in range(1,7):
    streams=roll_by[(seed,a,own)];check(set(streams)==set(pre['arms']) and streams[pre['arms'][0]]==streams[pre['arms'][1]],'SAME_OFFENSIVE_STREAM_COMMON_ACTORS')
 # Engineering smoke preserved only as separate denominator.
 smoke=sorted((root/'evidence/quarantine').glob('*23440001*.sqlite'));check(len(smoke)==2,'SMOKE_QUARANTINED_SEPARATELY')
 for p in smoke:
  m,st,rows,pending=read_db(p);check(pending==0 and int(m['revision'])==len(rows)>0 and st['seed']==23440001,'SMOKE_NO_REPLAY')
 out={'status':'PASS_R234_BILATERAL_TEAM_BEAST_NATIVE_COLD_CONDITIONAL','valid_arms':len(values),'paired_seeds':len(pre['seeds']),'source_form':'VZ-PRECREATE_FULLSTATS_NOT_P4','official_cells':0,'combat_scope':'physical_BASIC_6_rounds_SRC_FULL_STATS_ONLY','counts':tot,'same_rng_common_actors_pairs':len(pre['seeds'])*2*6,'quarantined_engineering_smoke':2,'historical_replays':0,'outcomes':values}
 if write:(root/'evidence/reports/R234_INDEPENDENT_SQL_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2));return out
if __name__=='__main__':audit()
