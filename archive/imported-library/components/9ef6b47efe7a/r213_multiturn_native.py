"""Independent R213 multiturm extension: native R18 scheduler state, v081 turn lifecycle + movement + ranged physical attack.
Not a source-complete balanced duel; target passes; conditional physical damage split; no historical seeds reused.
"""
from __future__ import annotations
import sys,json,hashlib,copy,math,random
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
sys.modules.pop('vlab_effects_v08',None);sys.path.insert(0,str(ROOT/'runtime/native'))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,EffectBlocked,move_via_verified_path,apply_weapon_attack,begin_source_turn,end_source_turn,Resistances)
PRE_BYTES=(ROOT/'sources/R213_MULTITURN_PREREG.json').read_bytes();PRE=json.loads(PRE_BYTES);PHASH=hashlib.sha256(PRE_BYTES).hexdigest()
MOVE_SRC='https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0';RAYA_SRC=PRE['actors']['RAYA']['source']
PM=FrozenRuleEvidence(MOVE_SRC,'R213-OPEN-PATH',hashlib.sha256(MOVE_SRC.encode()).hexdigest(),'2026-10-20','READONLY-NOTION-R213')
PA=FrozenRuleEvidence(RAYA_SRC,'R213-H-ATK',hashlib.sha256(RAYA_SRC.encode()).hexdigest(),'2026-10-20','READONLY-NOTION-R213')
MOVE=AbilitySource('R213-RAYA-MOVE','move','MOVEMENT',MOVE_SRC,PM.rule_id,'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='V081')
ATK=AbilitySource('R213-RAYA-H-ATK','attack','STANDARD',RAYA_SRC,PA.rule_id,'RULE-DERIVED',target_scope='ENEMY',requires_range_check=True,requires_line_of_sight=True,effect_adapter_ready=True,effect_adapter_id='V081')
def roll(seed,step,tag,n,f):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'R213MULTI|{seed}|{step}|{tag}|{n}d{f}'.encode()).digest(),'big'))
 return tuple(rng.randint(1,f) for _ in range(n))
def tape(seed,step):return {'crit':roll(seed,step,'CRIT',3,6),'hit':roll(seed,step,'HIT',6,6),'damage':(roll(seed,step,'DMG0',16,8),roll(seed,step,'DMG1',12,6),roll(seed,step,'DMG2',4,12))}
def init(db,seed):
 j.init_db(str(db),'A',seed);st=j.initial('A',seed)
 st.update({'scene':'R213-MULTITURN-'+str(seed),'seed':seed,'phase':'ACTIVE','active':'RAYA','round':1,'turn':0,'order':['RAYA','ERISTAN'],
  'actors':{},'native_events':[],'r213multi':{'prereg_sha':PHASH,'raya_turns':0,'eristan_passes':0,'moves':0,'attacks':0,'damage':0,'rounds':0,'source_status':'MIXED_DAMAGE_TAG_UNKNOWN_TEST'}})
 for who in ['RAYA','ERISTAN']:
  a=PRE['actors'][who];c=Combatant(who,a['hp'],a.get('pa'),a['ca'],0,0,0,0,'(0, 0)' if who=='RAYA' else '(40, 0)',rank='Lendário' if who=='RAYA' else 'Ouro Negro',standard=1 if who=='RAYA' else 0,movement=1 if who=='RAYA' else 0,reaction=1,maximum_hp=a['hp'],base_speed='68.5' if who=='RAYA' else None)
  st['actors'][who]={'resource':asdict(c),'source':a['source']}
 c=j.connect(str(db))
 with c:
  c.execute('UPDATE meta SET value=? WHERE key="state"',(j.canonical(st),))
  c.execute('UPDATE meta SET value=? WHERE key="scene"',(st['scene'],))
  h=j.sha({'prereg':PHASH,'seed':seed,'scene':st['scene']});c.execute('UPDATE meta SET value=? WHERE key="genesis"',(h,));c.execute('UPDATE meta SET value=? WHERE key="head"',(h,))
 c.close()
def scene(st):return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R213-MULTITURN-TEST-COND')
def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for who,a in s.actors.items():st['actors'][who]['resource']=asdict(a)
def action(st,p,seq):
 if st['phase']!='ACTIVE' or p.get('seed')!=st['seed'] or p.get('sha')!=PHASH or p.get('actor')!=st['active']:raise EffectBlocked('R213_MULTI_PRECONDITION')
 s=scene(st);old=len(s.events)
 if st['active']=='RAYA':
  step=st['r213multi']['raya_turns']+1
  if p.get('step')!=step or step>3:raise EffectBlocked('R213_MULTI_STEP')
  t=tape(st['seed'],step)
  if t['crit'][:2]==(1,1) and t['crit'][2]<=2:raise EffectBlocked('UNRESOLVED_NEG_CRIT')
  a=s.actors['RAYA'];target=s.actors['ERISTAN'];src=(step-1)*5;dst=step*5
  if a.position!=str((src,0)) or a.movement!=1 or a.standard!=1:raise EffectBlocked('RAYA_STATE_DRIFT')
  mv=move_via_verified_path(s,'RAYA',source=MOVE,state=ActorActionState('RAYA',21,a.pa,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),proofs=(PM,),destination=str((dst,0)),path_evidence=f'R213-PREOPEN-STRAIGHT-5M-X-{src}-TO-{dst}-NO-ADJACENCY',travel_cost=Fraction(5),speed=Fraction('68.5'))
  distance=40-dst
  if distance>50 or distance<=0:raise EffectBlocked('RANGE')
  damage=sum(map(sum,t['damage']))+294;score=sum(t['hit'])+245
  ev=apply_weapon_attack(s,'RAYA','ERISTAN',source=ATK,state=ActorActionState('RAYA',21,a.pa,(ATK.action_id,),standard_available=True,movement_available=False,range_confirmed=True,los_confirmed=True,enemy_ids_visible=('ERISTAN',)),proofs=(PA,),roll_score=score,damage=damage,damage_tag='perfurante',rd=Resistances(general=25,provenance='R212-SOURCE-CONDITIONAL-LAB-RD25'),damage_dice_groups=((16,8),(12,6),(4,12)),damage_roll_groups=t['damage'],damage_fixed_bonus=294,critical_sequence=t['crit'],attack_roll_attempts=(t['hit'],),attack_bonus=245,attack_origin='NORMAL')
  end_source_turn(s,'RAYA')
  m=st['r213multi'];m['raya_turns']+=1;m['attacks']+=1;m['moves']+=1;m['damage']+=ev['hp_loss_actual']
  if target.hp==0:st['phase']='FINISHED_KO_TEST_NOT_VICTORY_CANON';st['active']=None;st['finish_reason']='TARGET_HP0_TEST'
  elif step==3:st['phase']='CENSORED_HORIZON';st['active']=None;st['finish_reason']='RAYA_THREE_TURNS'
  else:
   st['active']='ERISTAN';st['turn']=1;begin_source_turn(s,'ERISTAN')
  ret={'move_seq':mv['seq'],'attack_seq':ev['seq'],'hp_loss':ev['hp_loss_actual'],'hp_target_after':target.hp}
 else:
  if p.get('step')!=st['r213multi']['eristan_passes']+1:raise EffectBlocked('PASS_ORDER')
  a=s.actors['ERISTAN']
  if a.standard!=1:raise EffectBlocked('PASS_NOT_READY')
  a.standard=0;s.record({'action':'r213_proposed_npc_standard_pass','by':'ERISTAN','source_limit':'NO_LEGAL_RANGED_ATTACK_SOURCE_IN_THIS_FIXTURE','cost':0})
  end_source_turn(s,'ERISTAN')
  st['r213multi']['eristan_passes']+=1;st['round']+=1;st['turn']=0;st['active']='RAYA';begin_source_turn(s,'RAYA')
  ret={'npc_passed':True,'new_round':st['round']}
 sync(st,s)
 return {'turn_result':ret,'events_added':copy.deepcopy(s.events[old:]),'phase':st['phase'],'next_active':st['active']}
def run(seed):
 ident=f'R213_MULTITURN_S{seed}';db=ROOT/'evidence/db'/(ident+'.sqlite')
 if db.exists():raise RuntimeError('NO_REUSE')
 if any((tape(seed,x)['crit'][:2]==(1,1) and tape(seed,x)['crit'][2]<=2) for x in [1,2,3]):return {'seed':seed,'status':'PRECOMMIT_HOLD_UNRESOLVED_NEG_CRIT'}
 init(db,seed)
 for seq in range(6):
  st,_,_=j.load(db)
  if st['phase']!='ACTIVE':break
  who=st['active'];step=st['r213multi']['raya_turns']+1 if who=='RAYA' else st['r213multi']['eristan_passes']+1
  j.event_commit(str(db),f'LAB-CMD-R213-MULTI-{seed}-TURN{seq}', 'R213_NATIVE_MULTITURN',{'seed':seed,'actor':who,'step':step,'sha':PHASH},action)
 st,head,rev=j.load(db)
 return {'seed':seed,'run_id':ident,'status':st['phase'],'rounds_started':st['round'],'commits':rev,'events':len(st['native_events']),'metrics':st['r213multi'],'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},'head':head,'db':db.name}
def main():
 results=[run(s) for s in PRE['seeds']]
 (ROOT/'evidence/R213_MULTI_RESULTS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False));print(json.dumps(results,indent=2))
if __name__=='__main__':main()
