"""Independent replay of R173 conditional source-scope battle journal.
Does NOT import r173_source_battle or its verdict. Recalculates physics,
resources, policy, RNG and scheduler from frozen source excerpts + SQL rows.
Formal external certification is not implied.
"""
from __future__ import annotations
import json,hashlib,random,pathlib,sqlite3,sys,copy
P=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(P/'deps/r61_extracted/work/fusion_stage12'))
sys.path.insert(0,str(P/'deps/native_v081_controlled'))
# r18 authenticates rows; independent semantic steps below do NOT call producer.
import vlab_r18_interactive as r18

F={
 'AUREN':dict(hp=523,pa=719,ca=225,rd=35,atk=193,enhanced=201,n_hit=6,n_damage=8,s_damage=8,flat=211,source='https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02',tag='perfurante'),
 'LEVIATHAN':dict(hp=6060,pa=4260,ca=110,rd=75,atk=142,enhanced=142,n_hit=6,n_damage=20,s_damage=10,flat=0,source='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7',tag='impacto'),
}
def dice(seed,n,actor,label,num,sides):
 h=hashlib.sha256(f'R173-PREREG-DEV|{seed}|{n}|{actor}|{label}|{num}d{sides}'.encode()).digest()
 r=random.Random(int.from_bytes(h,'big'))
 return [r.randint(1,sides) for _ in range(num)]
def eq(a,b,why):
 if a!=b:raise AssertionError(f'R173_SEMANTIC_MISMATCH_{why}: {a!r} != {b!r}')

def audit(db,checkpoint=True):
 db=pathlib.Path(db)
 history=r18.history(db)
 rows=history['events'];final=history['state'];seed=final['seed'];policy=final['r173_policy']
 if policy not in ('ALWAYS_DODGE','TACTICAL_SAVE'):raise AssertionError('UNKNOWN_POLICY')
 if any(r['kind'] not in ('R173_CONDITIONAL_INIT','R173_SOURCE_ATTACK') for r in rows):raise AssertionError('WRONG_RUN_SCOPE')
 if any(r['kind']=='R173_CONDITIONAL_INIT' for r in rows[1:]) or not rows or rows[0]['kind']!='R173_CONDITIONAL_INIT':raise AssertionError('MISSING_INIT_OR_DUPLICATE')
 with sqlite3.connect(db) as con:
  if con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]:raise AssertionError('UNRESOLVED_PENDING')
 hp={a:f['hp'] for a,f in F.items()};pa={a:f['pa'] for a,f in F.items()};reactions={'AUREN':1,'LEVIATHAN':1}
 raw_total=net_total=loss_total=overkill_total=hit_total=negative=positive=react_total=0
 counts={a:0 for a in F}; hits_by={a:0 for a in F}; event_seq=0;auren_turns=0
 native_list=[]
 eq(rows[0]['payload'],{'order':['AUREN','LEVIATHAN'],'authority':'EXOGENOUS_LAB_CONDITIONAL_NOT_CANON'},'INIT_AUTHORITY')
 eq(rows[0]['detail']['source_battle_admissibility'],'PARTIAL_INITIATIVE_NOT_ADMITTED','INIT_NOT_OFFICIAL')
 active='AUREN';ended=False
 for i,row in enumerate(rows[1:],1):
  if ended:raise AssertionError('POST_KO_ATTACK')
  actor='AUREN' if i%2 else 'LEVIATHAN';target='LEVIATHAN' if actor=='AUREN' else 'AUREN'
  eq(row['kind'],'R173_SOURCE_ATTACK','ROW_KIND');eq(row['payload']['actor'],actor,'ACTOR')
  eq(row['payload']['target'],target,'TARGET');eq(row['payload']['attack_index'],i,'STEP_INDEX')
  eq(row['payload']['policy'],policy,'POLICY');eq(row['payload']['seed'],seed,'SEED')
  info=F[actor];f_target=F[target]
  expect_roll={'crit':dice(seed,i,actor,'crit',3,6),'hit':dice(seed,i,actor,'hit',6,6),
   'hit_weak':dice(seed,i,actor,'weak_hit',6,6),'damage':dice(seed,i,actor,'damage',info['n_damage'],info['s_damage'])}
  eq(row['payload']['roll_tape'],expect_roll,'DICE_GENERATOR')
  crit=expect_roll['crit'];critical='POSITIVE' if crit[:2]==[6,6] and crit[2]>=5 else ('NEGATIVE' if crit[:2]==[1,1] and crit[2]<=2 else 'NONE')
  weak=10*hp[actor]<info['hp']
  bonus=info['enhanced'] if actor=='AUREN' and auren_turns>=2 else info['atk']
  rolls=(expect_roll['hit'],expect_roll['hit_weak']) if weak else (expect_roll['hit'],)
  score=(min(map(sum,rolls))+bonus-2) if weak else sum(rolls[0])+bonus
  want_defense=target=='AUREN' and policy=='ALWAYS_DODGE' and reactions['AUREN']>0
  ev=row['detail']['native_events'];eq(len(ev),2 if want_defense else 1,'EVENT_COUNT')
  if want_defense:
   d=ev[0];eq(d['action'],'ESQUIVAR','DEFENSE_KIND');eq(d['by'],'AUREN','DEFENDER_NAME')
   eq(d['attack_score'],score,'DEFENSE_SCORE');eq(d['defense_exact'],'227','PRECOMPUTED_REFLEX_DEFENSE')
   eq(d['damage_negated'],score<=227,'DEFENSE_OUTCOME')
   eq(d['consumes_reaction'],True,'CONSUMPTION')
   eq(d['r173_response_to_attack_seq'],d['seq']+1,'CAUSAL_LINK')
   reactions['AUREN']-=1;react_total+=1
  v=ev[-1];eq(v['action'],'weapon_attack','ATTACK_ACTION');eq(v['from'],actor,'FROM');eq(v['to'],target,'TO')
  eq(v['r173_defense_event_seq'],ev[0]['seq'] if want_defense else None,'DEFENSE_LINK')
  eq(v['r173_tx_seq'],row['seq'],'TRANSACTION_LINK')
  eq(v['r173_source_page'],info['source'],'PHYSICAL_SOURCE')
  eq(v['roll_score'],score,'HIT_ROLL');eq(v['critical'],critical,'CRITICAL')
  eq(v['attack_roll_attempts'],[list(q) for q in rolls],'HIT_TAPE')
  eq(v['critical_sequence'],crit,'CRITICAL_TAPE')
  eq(v['damage_roll_groups'],[expect_roll['damage']],'DAMAGE_TAPE')
  eq(v['normal_damage'],sum(expect_roll['damage'])+info['flat'],'DAMAGE_FORMULA')
  eq(v['ca_exact'],str(f_target['ca']),'TARGET_CA');eq(v['type'],info['tag'],'DAMAGE_TYPE')
  eq(v['weak_attacker'],weak,'WEAK_STATUS')
  hit=(score>f_target['ca'] or critical=='POSITIVE') and critical!='NEGATIVE'
  eq(v['hit'],hit,'HIT_FLAG')
  dmg=(sum(expect_roll['damage'])+info['flat']+ (info['n_damage']*info['s_damage'] if critical=='POSITIVE' and hit else 0)) if hit and not (want_defense and score<=227) else 0
  rd=f_target['rd'] if dmg else 0
  net=max(0,dmg-rd) if dmg else 0
  loss=min(hp[target],net);over=max(0,net-hp[target]);before=hp[target];hp[target]-=loss
  for k,vv in [('raw',dmg),('rd_applied',rd),('net',net),('before_hp',before),('after_hp',hp[target]),('hp_loss_actual',loss),('overkill',over)]:eq(v[k],vv,'ATTACK_'+k)
  eq(v['defense_negated'],bool(want_defense and score<=227),'DEFENSE_NEGATE')
  for e in ev:
   event_seq+=1;eq(e['seq'],event_seq,'EVENT_SEQUENTIAL');native_list.append(e)
  eq(row['detail']['native_events'],ev,'DETAIL_EVENTS')
  eq(row['detail']['receipt'],v,'DETAIL_RECEIPT')
  eq(row['detail']['HP_after'],hp,'DETAIL_HP');eq(row['detail']['PA_after'],pa,'DETAIL_PA')
  eq(row['detail']['reaction_after'],reactions,'DETAIL_REACTION')
  eq(row['detail']['official_effects'],0,'OFFICIAL_EFFECTS')
  counts[actor]+=1;hits_by[actor]+=int(hit);hit_total+=int(hit)
  raw_total+=dmg;net_total+=net;loss_total+=loss;overkill_total+=over
  negative+=int(critical=='NEGATIVE');positive+=int(critical=='POSITIVE')
  if actor=='AUREN':auren_turns+=1
  if hp[target]==0:
   ended=True;eq(row['detail']['scheduler']['winner'],actor,'WINNER')
  else:
   next_actor='AUREN' if actor=='LEVIATHAN' else 'LEVIATHAN'
   eq(row['detail']['scheduler']['next_turn'],next_actor,'SCHEDULER_NEXT')
  if row['detail']['attack_event_seq']!=v['seq']:raise AssertionError('ATTACK_SEQ')
 eq(final['r173_native_events'],native_list,'FINAL_NATIVE_EVENTS')
 eq(final['phase'],'FINISHED' if ended else 'ACTIVE','FINAL_PHASE')
 if ended:eq(final['winner'],actor,'FINAL_WINNER')
 for a in F:
  eq(final['actors'][a]['resource']['hp'],hp[a],'FINAL_HP_'+a)
  eq(final['actors'][a]['resource']['pa'],pa[a],'FINAL_PA_'+a)
  eq(final['actors'][a]['resource']['reaction'],reactions[a],'FINAL_REACTION_'+a)
 m=final['r173_metrics'];expected={'attacks':len(rows)-1,'hits':hit_total,'raw_hit_damage':raw_total,
  'post_rd':net_total,'hp_loss':loss_total,'overkill':overkill_total,'reactions_spent':react_total,'pa_spent':0,
  'crit_positive':positive,'crit_negative':negative,'attempts_by_actor':counts,'hits_by_actor':hits_by}
 eq(m,expected,'AGGREGATE_METRICS');eq(len(final['r173_turn_history']),len(rows)-1,'TURN_HISTORY')
 if net_total-loss_total!=overkill_total:raise AssertionError('OVERKILL_DECOMPOSITION')
 if checkpoint:
  cp=json.loads(pathlib.Path(str(db)+'.checkpoint.json').read_text())
  eq(cp['sha256'],r18.sha(cp['body']),'CHECKPOINT_HASH')
  eq(cp['body']['state'],final,'CHECKPOINT_STATE')
  eq(cp['body']['events'],rows,'CHECKPOINT_EVENTS')
 return {'status':'PASS_R173_INDEPENDENT_MATH_CAUSAL_REPLAY','source_admissibility':'PHYSICAL_ATTACKS_ONLY;INITIATIVE_EXOGENOUS;RANGE_CONDITIONAL',
  'policy':policy,'seed':seed,'attacks':len(rows)-1,'journal_commits':len(rows),'native_events':len(native_list),
  'HP':hp,'PA':pa,'reaction_left':reactions,'metrics':m,'ended':ended,'winner':final['winner'],
  'formal_external_auditor':False,'official_cells':0,'terminal_contracts':0,'sha':r18.sha(final)}

def semantic_tamper_rehash(original,target):
 """Changes one attack net while recomputing SQL chain without changing HP.
 A structural-only verifier passes; the independent math oracle MUST reject.
 """
 import shutil
 shutil.copy2(original,target)
 con=sqlite3.connect(target)
 try:
  con.execute('BEGIN IMMEDIATE')
  rows=con.execute('SELECT seq,row_json FROM events ORDER BY seq').fetchall();prev=dict(con.execute('SELECT key,value FROM meta'))['genesis']
  for seq,row_json in rows:
   row=json.loads(row_json);row['prev']=prev
   if seq==2:
    row['detail']['receipt']['net']+=1
    row['detail']['native_events'][-1]['net']+=1
   digest=r18.sha(row);con.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(prev,r18.canonical(row),digest,seq));prev=digest
  con.execute('UPDATE meta SET value=? WHERE key="head"',(prev,));con.commit()
 finally:con.close()
 return target

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('db');a=p.parse_args();print(json.dumps(audit(a.db),indent=2,ensure_ascii=False))
