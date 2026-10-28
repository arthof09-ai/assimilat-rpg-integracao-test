"""R211: additive, source-fenced movement plus dynamic area targeting atop R18/v081. Test only."""
from __future__ import annotations
import sys, json, math, copy, hashlib
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'r210'/'code'
sys.path.insert(0,str(BASE))
import r210_ref as ref
from vlab_effects_v08 import move_via_verified_path,EffectBlocked,FrozenRuleEvidence,AbilitySource,ActorActionState,begin_source_turn,end_source_turn
PRE_BYTES=(ROOT/'source/R211_DYNAMIC_CENTER_PREREG.json').read_bytes();PRE=json.loads(PRE_BYTES);PHASH=hashlib.sha256(PRE_BYTES).hexdigest()
core=ref.core;R18=ref.R18;E=ref.E;B1=ref.B1;B2=ref.B2;TRIO=ref.TRIO
VERSION='R211-R18-v081-NATIVE-MOVE-ADAPTIVE-AOE-1'
M_SOURCE=PRE['sources']['combat'];M_BEST=PRE['sources']['beast_speed']
PROOF=FrozenRuleEvidence(M_SOURCE,VERSION+'-MOVE-COMBAT',hashlib.sha256((M_SOURCE+M_BEST+'movement source 1 per turn').encode()).hexdigest(),'2026-10-20','NOTION_READBACK_20261020_R211')
MOVE=AbilitySource(VERSION+'-MOVEMENT','move','MOVEMENT',M_SOURCE,PROOF.rule_id,'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-PATH-MOVE')

def dist2(x,y):return (x[0]-y[0])**2+(x[1]-y[1])**2

def centers(st):
 pos=st['r211']['positions_m']; alive=[w for w in (B1,B2) if st['actors'][w]['resource']['hp']>0]
 opts=[]
 for center in PRE['center_candidates_m']:
  if dist2(center,pos[E])>25**2:continue
  includes=[w for w in TRIO if st['actors'][w]['resource']['hp']>0 and dist2(center,pos[w])<=25]
  enemy=[x for x in includes if x in alive];risk=int(E in includes)
  distance_sum=sum(dist2(center,pos[w]) for w in enemy)
  opts.append({'center':center,'in':includes,'enemy':enemy,'self_risk':risk,'score':[len(enemy),-risk,-distance_sum]})
 if not opts:raise EffectBlocked('NO_ADMISSIBLE_CENTER')
 return opts

def select(st,policy):
 cand=centers(st)
 if policy=='FIXED':
  found=next((x for x in cand if x['center']==[8,0]),None)
  if found is None:raise EffectBlocked('FIXED_CENTER_INVALID')
  return found,cand
 if policy!='ADAPTIVE':raise EffectBlocked('UNKNOWN_POLICY')
 # Policy fixed before seeds. Tie choose smaller center tuple.
 return sorted(cand,key=lambda x:(-x['score'][0],-x['score'][1],-x['score'][2],tuple(x['center'])))[0],cand

def genesis(path,seed,policy):
 R18.init_db(str(path),'A',seed)
 st=core.state_genesis(seed,TRIO)
 st['position']={'contact':False,'same_layer':True,'line_of_effect':True,'movement':True,'campaign_location':False}
 st['r211']={'prereg_sha':PHASH,'version':VERSION,'policy':policy,'positions_m':copy.deepcopy(PRE['position_start_m']),
  'movements':0,'casts':0,'targets':0,'PA_cast':0,'magic_effective':0,'self_damage':0,'beast_damage':0,
  'decisions':[],'patrol':[],'source_limitations':PRE['limits']}
 for who in TRIO:
  a=st['actors'][who]['resource'];a['position']=str(tuple(st['r211']['positions_m'][who]));a['movement']=0
  if who==B1:
   a['base_speed']=27
  elif who==B2:
   a['base_speed']=27
  # E movement not needed in this fixture; no invented speed.
 conn=R18.connect(str(path))
 try:
  with conn:conn.execute('UPDATE meta SET value=? WHERE key="state"',(R18.canonical(st),))
 finally:conn.close()

def init(st,p,seq):
 if st['r211']['prereg_sha']!=PHASH or p.get('r211_sha')!=PHASH:raise EffectBlocked('PREREG_MISMATCH')
 q={k:v for k,v in p.items() if k!='r211_sha'}
 return core.start(st,q,seq)

def advance(st,s,who):
 end_source_turn(s,who)
 if st['phase']=='ACTIVE':
  nxt=R18._next_turn(st)
  s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 else:nxt={'end':'KO'}
 return nxt

def beast_turn(st,p,seq):
 who=st['active'];own=1+sum(h['actor']==who for h in st['history'])
 if st['phase']!='ACTIVE' or who not in (B1,B2) or p!={'actor':who,'turn':own,'policy':'SOURCE_RANGE_PRESERVING_PATROL'}:
  raise EffectBlocked('BEAST_TURN_SCOPE')
 s=core.scene(st);a=s.actors[who];old=len(s.events);out=None
 if who==B1:
  dst=PRE['patrol_own_turn_odd_to'] if own%2 else PRE['patrol_own_turn_even_to']
  src=st['r211']['positions_m'][who];travel=Fraction(str(math.dist(src,dst)))
  if src==dst:raise EffectBlocked('ZERO_PATH')
  if travel>27 or dist2(src,st['r211']['positions_m'][E])<4 or dist2(dst,st['r211']['positions_m'][E])<4:raise EffectBlocked('PATH_OR_AOO_GATE')
  if any(x[0]!=8 for x in (src,dst)):raise EffectBlocked('NOT_PRE_REGISTERED_X8_ROUTE')
  # All points on vertical x=8 remain at least 8m from E; no departure from adjacency.
  if a.movement!=1 or a.base_speed!=27:raise EffectBlocked('MOVE_BUDGET_OR_SPEED')
  proof=f'R211_PRESET_OPEN_STRAIGHT_X8_FROM_{src}_TO_{dst}_AOO_NO_TRIG_DISTANCE_MIN8'
  out=move_via_verified_path(s,who,source=MOVE,
     state=ActorActionState(who,11,a.pa,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
     proofs=(PROOF,),destination=str(tuple(dst)),path_evidence=proof,travel_cost=travel,speed=Fraction(27))
  st['r211']['positions_m'][who]=copy.deepcopy(dst)
  st['r211']['movements']+=1
  st['r211']['patrol'].append({'actor':who,'turn':own,'from':src,'to':dst,'path_m':str(travel),'seq':out['seq']})
  s.record({'action':'r211_path_no_aoo','from_actor':who,'safe_min_distance_to_enemy_m':8,'trigger':'NO_ADJACENT_BLOCK_EXIT','source':M_SOURCE})
 # No legal adjacent attack: B2 at (8,-1), B1 at x=8; E at (0,0). Explicit standard pass.
 if dist2(st['r211']['positions_m'][who],st['r211']['positions_m'][E])<=4:raise EffectBlocked('ADJACENT_ATTACK_NEEDS_OWN_RESOLVER')
 if a.standard!=1:raise EffectBlocked('PASS_STANDARD_UNAVAILABLE')
 a.standard=0;s.record({'action':'r211_beast_standard_pass','by':who,'reason':'OUT_OF_MELEE_REACH_THIS_TEST_FIXTURE','pa_spent':0})
 nxt=advance(st,s,who);core.sync(st,s)
 st['history'].append({'actor':who,'own_turn':own,'action':'MOVE_AND_PASS' if out else 'PASS'})
 return {'kind':'R211_NATIVE_MOVEMENT_BEAST_TURN','events_added':copy.deepcopy(s.events[old:]),'next':nxt}

def cast(st,p,seq):
 who=st['active'];own=1+sum(h['actor']==E for h in st['history'])
 if st['phase']!='ACTIVE' or who!=E or p!={'actor':E,'turn':own,'policy':st['r211']['policy']}:
  raise EffectBlocked('CAST_TURN_SCOPE')
 s=core.scene(st);a=s.actors[E];old=len(s.events)
 if a.standard!=1 or a.hp<=0 or a.pa is None or a.pa<80:raise EffectBlocked('CAST_UNAVAILABLE')
 chosen,candidates=select(st,p['policy']);center=chosen['center'];targets=chosen['in']
 roll=ref.spell_roll(st['seed'],own,'DAMAGE',n=10,faces=10);raw=sum(roll)+10
 pa_pre=a.pa;a.pa-=80;a.standard=0
 decision=s.record({'action':'r211_center_decision','by':E,'turn':own,'policy':p['policy'],
  'state_positions_m':copy.deepcopy(st['r211']['positions_m']),'centers_evaluated':copy.deepcopy(candidates),
  'criterion':PRE['policies'][p['policy']],'center_chosen_m':center,
  'eligible_targets':targets,'excluded_targets':[x for x in TRIO if x not in targets],
  'rng_not_observed':'NO_FUTURE_DAMAGE_OR_SAVES_READ'})
 cast_evt=s.record({'action':'r211_area_cast','by':E,'cast_event_seq':decision['seq'],'center_m':center,
  'spell_source':PRE['sources']['eristan'],'action_economy':'STANDARD','common_roll':roll,
  'raw_spell_damage':raw,'pa_before':pa_pre,'pa_after':a.pa,'pa_cost':80,'target_count':len(targets)})
 m=st['r211'];m['casts']+=1;m['PA_cast']+=80;st['metrics']['pa_spent']+=80
 for target_id in targets:
  target=s.actors[target_id]
  if target.hp<=0:continue
  attrs=ref.PRE['actors'][target_id];dice=ref.spell_roll(st['seed'],own,'SAVE',target_id,*attrs['fortitude_dice']);score=sum(dice)+attrs['CON']
  if score>76:
   if raw%2:raise EffectBlocked('HALF_ODD_ROUNDING_UNKNOWN')
   dmg=raw//2
  else:dmg=raw
  before=target.hp;actual=min(before,dmg);target.hp=max(0,before-dmg)
  ev=s.record({'action':'r211_area_target','cast_seq':cast_evt['seq'],'target':target_id,
    'self_target':target_id==E,'position_m':m['positions_m'][target_id],
    'distance2_to_center':dist2(center,m['positions_m'][target_id]),'radius2':25,
    'save_dice':dice,'save_attribute_pure':attrs['CON'],'save_total':score,'save_success':score>76,
    'save_cd':76,'damage_type':'PLANTA','damage_raw':dmg,'rd_magic':0,
    'rd_status':'UNKNOWN_CANON_ASSUMED_ZERO_LAB','damage_post_rd':dmg,'hp_before':before,
    'hp_after':target.hp,'hp_effective':actual,'overkill':max(0,dmg-before)})
  m['targets']+=1;m['magic_effective']+=actual
  if target_id==E:m['self_damage']+=actual
  else:m['beast_damage']+=actual
 m['decisions'].append({'own_turn':own,'center':center,'positions_m':copy.deepcopy(m['positions_m']),
                        'targets':targets,'event_seq':decision['seq']})
 # No artificial KO win; success if all beasts HP=0; user may be incapacitated if exposed.
 if s.actors[E].hp==0:
  st['phase']='FINISHED';st['winner']='BEAST_SIDE_LAB';st['finish_reason']='ERISTAN_SELF_DAMAGE_HP0';st['active']=None
 elif all(s.actors[k].hp==0 for k in (B1,B2)):
  st['phase']='FINISHED';st['winner']='ERISTAN_SIDE_LAB';st['finish_reason']='BOTH_BEAST_HP0';st['active']=None
 nxt=advance(st,s,E);core.sync(st,s)
 st['history'].append({'actor':E,'own_turn':own,'action':'CAST','center':center,'targets':targets})
 return {'kind':'R211_DYNAMIC_AREA_NATIVE_R18','events_added':copy.deepcopy(s.events[old:]),'next':nxt}

def run(seed,policy):
 ident=f'R211_DYN_AOE_S{seed}_{policy}';db=ROOT/'evidence/db'/f'{ident}.sqlite'
 if db.exists():raise RuntimeError('NO_REUSE_RUN_ID '+ident)
 vals,order=ref.roll_order(seed)
 if order is None:return {'run_id':ident,'seed':seed,'policy':policy,'status':'PRECOMMIT_INIT_TIE_HOLD'}
 genesis(db,seed,policy)
 R18.event_commit(str(db),'LAB-CMD-'+ident+'-INIT','R211_INIT',{ 'initiative':vals,'order':order,'pre_reg_sha':core.PRE_SHA,'source_snap_sha':core.SOURCE_SHA,'r211_sha':PHASH},init)
 for i in range(9):
  st,_,_=R18.load(str(db))
  if st['phase']=='FINISHED':break
  who=st['active'];turn=1+sum(h['actor']==who for h in st['history'])
  if who==E: R18.event_commit(str(db),f'LAB-CMD-{ident}-CAST{i}','R211_AREA_DYNAMIC',{'actor':E,'turn':turn,'policy':policy},cast)
  else:R18.event_commit(str(db),f'LAB-CMD-{ident}-MOVE{i}','R211_MOVE_NATIVE_OR_PASS',{'actor':who,'turn':turn,'policy':'SOURCE_RANGE_PRESERVING_PATROL'},beast_turn)
 st,head,rev=R18.load(str(db));core.write_checkpoint(str(db))
 m=st['r211'];return {'run_id':ident,'seed':seed,'policy':policy,'status':'KO' if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
  'winner':st['winner'] if st['phase']=='FINISHED' else None,'rev':rev,'head':head,'events':len(st['native_events']),
  'casts':m['casts'],'moves':m['movements'],'PA_spent':m['PA_cast'],'targets':m['targets'],
  'beast_hp_effective':m['beast_damage'],'self_hp_effective':m['self_damage'],
  'centers':[x['center'] for x in m['decisions']],'final_hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},'db':db.name}

def main():
 (ROOT/'evidence/db').mkdir(parents=True,exist_ok=True)
 assert select({'r211':{'positions_m':PRE['position_start_m']},'actors':{w:{'resource':{'hp':1}}for w in TRIO}},'ADAPTIVE')[0]['center']==[8,0]
 data=[run(seed,policy) for seed in PRE['seeds'] for policy in PRE['policies']]
 (ROOT/'evidence/R211_COMBAT_RESULTS.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))
 print(json.dumps({'arms':len(data),'committed':sum('db'in x for x in data),'blocked':sum('db'not in x for x in data),
  'moves':sum(x.get('moves',0) for x in data),'casts':sum(x.get('casts',0) for x in data),
  'targets':sum(x.get('targets',0) for x in data),'events':sum(x.get('events',0) for x in data),
  'commits':sum(x.get('rev',0) for x in data)},indent=2))
if __name__=='__main__':main()
