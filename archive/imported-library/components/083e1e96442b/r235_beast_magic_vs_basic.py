"""R235: source-specified VZ Grifo Lightning standard vs physical basic in new 2x2 TEST factorial; native R18.
Source PRECREATE, not P4; single enemy in declared short-line geometry. No official promotion.
"""
import sys,copy,json,hashlib,random,math
from dataclasses import asdict
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12'),str(ROOT/'code')]
import r234_source_complete_beast_battle as base
# Prior module's native core was source-verified in R234, but no historical R234 seed replay here.
j=base.j
from vlab_effects_v08 import Scene,Combatant,AbilitySource,FrozenRuleEvidence,ActorActionState,Resistances,move_via_verified_path,begin_source_turn,end_source_turn,apply_weapon_attack,cast_source_specified_spell,effective_movement_speed
PRE_B=(ROOT/'sources/R235_PREREG_BEFORE_COMMIT.json').read_bytes();PRE=json.loads(PRE_B);PH=hashlib.sha256(PRE_B).hexdigest()
SRC_B=(ROOT/'sources/R235_GRIFFON_SPELL_SOURCE_EXCERPT.json').read_bytes();SRC=json.loads(SRC_B);SH=hashlib.sha256(SRC_B).hexdigest()
SOURCE_BEAST_HASH=base.SH
SPELL=AbilitySource('R235-GRIFFON-DESCARGA-CURTA','spell','STANDARD',SRC['page_id'],'R235-GRIFFON-SHORT-LINE-CD94','RULE-DERIVED',required_pa=55,requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081')
PROOF=FrozenRuleEvidence(SRC['page_id'],SPELL.rule_id,SH,'2026-10-21','VZ-BEAST-PRIMARY-MECHANICAL-EXCERPT')
def rd_value(arm):return 0 if arm.endswith('_RD0_TEST') else 75
def policy(arm):return 'MIXED' if arm.startswith('MIXED') else 'PHYSICAL'
def rr(seed,who,own,tag,n,f):
 v=int.from_bytes(hashlib.sha256(f'R235|{seed}|{who}|{own}|{tag}|{n}d{f}'.encode()).digest(),'big');r=random.Random(v)
 return tuple(r.randint(1,f) for _ in range(n))
def init_state(seed,arm):
 st=j.initial('A',seed);actors=('G','C') if arm!='SAVE_FOCUS' else ('G','R')
 st.update({'scene':f'R235-{arm}-S{seed}','phase':'ACTIVE','round':1,'turn':0,'order':list(actors),'active':'G','seed':seed,
  'actors':{k:base.c_actor(k) for k in actors},'native_events':[],
  'r235':{'seed':seed,'arm':arm,'prereg_sha':PH,'source_sha':SH,'beast_source_sha':SOURCE_BEAST_HASH,'source_status':'VZ_PRECREATE_NONP4',
  'rd_target':rd_value(arm) if arm!='SAVE_FOCUS' else 75, 'rd_status':'TEST_RD0_COUNTERFACTUAL' if arm.endswith('_RD0_TEST') else 'VZ_SOURCE_RD75',
  'phase':'ACTIVE','stats':{'attacks':0,'hits':0,'spells':0,'save_success':0,'odd_saved':0,'pa_spent':0,'movements':0,'physical_hp_loss':0,'spell_hp_loss':0},'outcome':None}})
 if arm=='SAVE_FOCUS':
  st['actors']['G']['position']='(0,0)';st['actors']['R']['position']='(1,0)'
 return st
def db_start(path,seed,arm):
 j.init_db(str(path),'A',seed);s=init_state(seed,arm);g=j.sha({'r235_prereg':PH,'source_spell':SH,'source_beasts':SOURCE_BEAST_HASH,'seed':seed,'arm':arm})
 c=j.connect(str(path))
 with c:
  for k,v in [('state',j.canonical(s)),('scene',s['scene']),('head',g),('genesis',g)]:c.execute('update meta set value=? where key=?',(v,k))
 c.close()
def native_spell(s,seed,target,own):
 c=s.actors['G'];d=s.actors[target]
 damage_rolls=rr(seed,'G',own,'LIGHTNING_DAMAGE',14,10);save_rolls=rr(seed,target,own,'REFLEX_SAVE',6,6)
 result_score=sum(save_rolls)+base.BE[target]['stats']['DES'];save=result_score>94;gross=sum(damage_rolls)
 s.record({'action':'R235_FROZEN_MAGIC_TAPE','caster':'G','target':target,'own_turn':own,'damage_dice':damage_rolls,'save_dice':save_rolls,'save_score':result_score,'source_cd':94,'source_sha':SH,'save_mechanic':'6d6+pure DES','cost_pa':55,'save_success':save,'save_even_or_odd':'ODD' if gross%2 else 'EVEN','geometry':'LAB_ONE_ENEMY_NEAR_CLOSE_LINE'})
 rd=75 if target=='R' else s._r235_target_rd if hasattr(s,'_r235_target_rd') else 75
 receipt=cast_source_specified_spell(s,'G',target,source=SPELL,state=ActorActionState('G',23,c.pa,(SPELL.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=(target,)),proofs=(PROOF,),
  damage=gross,damage_tag='raio',rd=Resistances(general=rd,provenance='VZ-RD75-GENERAL-PENDING-NORM' if rd else 'NONCANON_RD_ZERO_COUNTERFACTUAL'),
  explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=save,
  odd_half_rounding_test_policy=('FLOOR_MASTER_CONFIRMED_TEST' if save and gross%2 else None),rounding_decision_source=('USER_MESTRE_CONFIRMED_ALL_COMBAT_DAMAGE_2026-10-21' if save and gross%2 else None),
  damage_rolls=damage_rolls,damage_faces=10,documented_flat_bonus=0)
 return receipt,save,gross

def turn(st,p,rev):
 arm=st['r235']['arm'];seed=st['seed'];who=st['active'];rec=st['r235']
 if p!={'prereg_sha':PH,'spell_sha':SH,'seed':seed,'arm':arm,'who':who,'turn':st['turn']+1}:raise ValueError('NO_PREREG_DRIFT')
 s=Scene({k:base.load_actor(v) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=seed,provenance='R235-PRECREATE-SOURCE-TEST-NOT-P4')
 old=len(s.events);own=st['round'];stats=rec['stats']
 begin_source_turn(s,who)
 if own==1:
  dest,dist=base.FIRST_MOVE[who];speed=effective_movement_speed(s.actors[who]);assert dist<=speed
  move_via_verified_path(s,who,source=base.M,state=ActorActionState(who,23,s.actors[who].pa,(base.M.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),proofs=(base.PM,),destination=dest,path_evidence='R235-SOURCE-BEAST-SPEED-OPEN-LAB-NO-EXIT',travel_cost=dist,speed=speed);stats['movements']+=1
 target='C' if who=='G' else 'G'
 if math.dist(base_position(s.actors[who].position),base_position(s.actors[target].position))>2:raise ValueError('R235_SHORT_LINE_TARGET_OUT_OF_DECLARED_CLOSE_RANGE')
 if who=='G' and policy(arm)=='MIXED' and own%2==0:
  # Native Scene is extensible only for declared TEST RD sensitivity. Never persisted as RPG actor attribute.
  s._r235_target_rd=rec['rd_target']
  receipt,save,gross=native_spell(s,seed,'C',own)
  stats['spells']+=1;stats['save_success']+=int(save);stats['odd_saved']+=int(save and gross%2);stats['pa_spent']+=55;stats['spell_hp_loss']+=receipt['hp_before']-receipt['hp_after']
 else:
  z=base.BE[who];dmg=base.roll(seed,who,own,'DAMAGE',20,10);atk=base.roll(seed,who,own,'ATTACK',6,6);crit=base.roll(seed,who,own,'CRITICAL',3,6)
  s.record({'action':'R235_PER_ACTOR_PHYSICAL_TAPE','by':who,'target':target,'own_turn':own,'dice_attack':atk,'dice_damage':dmg,'critical':crit,'source_sha':SOURCE_BEAST_HASH})
  rd=rec['rd_target'] if target=='C' else 75
  receipt=apply_weapon_attack(s,who,target,source=base.ATK[who],state=ActorActionState(who,23,s.actors[who].pa,(base.ATK[who].action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=(target,)),proofs=(base.PF[who],),
  roll_score=sum(atk)+z['attack_bonus'],damage=sum(dmg),damage_tag=z['damage_type'],rd=Resistances(general=rd,provenance='VZ-SOURCE-RD75' if rd else 'LAB-RD0-CONTROL'),
  damage_dice_groups=((20,10),),damage_roll_groups=(dmg,),damage_fixed_bonus=0,critical_sequence=crit,attack_roll_attempts=(atk,),attack_bonus=z['attack_bonus'],lab_negative_critical_policy=True)
  stats['attacks']+=1;stats['hits']+=int(receipt['hit']);stats['physical_hp_loss']+=receipt['hp_loss_actual']
 end_source_turn(s,who)
 st['turn']+=1
 if any(a.hp<=0 for a in s.actors.values()):
  st['phase']='STOP_HP0_LAB_ONLY';st['active']=None;st['finish_reason']='NONCANON_HP0_CUTOFF'
 elif who=='C' and own>=PRE['horizon_rounds']:
  st['phase']='CENSORED_HORIZON';st['active']=None;st['finish_reason']='HORIZON_SIX_ROUNDS'
 else:
  if who=='C':st['round']+=1;st['active']='G'
  else:st['active']='C'
 if st['phase']!='ACTIVE':rec['outcome']={'phase':st['phase'],'hp':{k:x.hp for k,x in s.actors.items()},'pa':{k:x.pa for k,x in s.actors.items()},'official_cells':0}
 rec['phase']=st['phase'];st['actors']={k:{**asdict(v),'ca':str(v.ca),'base_speed':str(v.base_speed)} for k,v in s.actors.items()};st['native_events']=copy.deepcopy(s.events)
 return {'events_new':copy.deepcopy(s.events[old:]),'who':who,'round':own,'phase':st['phase'],'stats':copy.deepcopy(stats)}
def base_position(pos):return tuple(float(v) for v in pos.strip('()').split(','))
def focus(st,p,rev):
 if st['r235']['arm']!='SAVE_FOCUS' or st['phase']!='ACTIVE' or p['prereg_sha']!=PH or p['spell_sha']!=SH:raise ValueError('R235_FOCUS_GATE')
 seed=st['seed'];s=Scene({k:base.load_actor(v) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=seed,provenance='R235-TEST-FOCUS-ODD-HALF-SOURCE-ONLY');begin_source_turn(s,'G')
 before=len(s.events);receipt,success,gross=native_spell(s,seed,'R',1);end_source_turn(s,'G');assert success
 st['phase']='CENSORED_ONE_SPELL';st['active']=None;st['turn']=1;st['r235']['phase']=st['phase'];st['r235']['stats']['spells']=1;st['r235']['stats']['save_success']=1;st['r235']['stats']['odd_saved']=int(gross%2);st['r235']['stats']['pa_spent']=55
 st['r235']['stats']['spell_hp_loss']=receipt['hp_before']-receipt['hp_after'];st['r235']['outcome']={'phase':st['phase'],'hp':{k:v.hp for k,v in s.actors.items()},'pa':{k:v.pa for k,v in s.actors.items()},'official_cells':0}
 st['actors']={k:{**asdict(v),'ca':str(v.ca),'base_speed':str(v.base_speed)} for k,v in s.actors.items()};st['native_events']=copy.deepcopy(s.events)
 return {'events_new':copy.deepcopy(s.events[1:]),'gross_damage':gross,'save_success':success,'rounding':'FLOOR' if gross%2 else 'INTEGER_HALF'}
def setup(path,seed,arm):
 if path.exists():raise FileExistsError('NO_SEED_REUSE')
 j.init_db(str(path),'A',seed);st=init_state(seed,arm);gen=j.sha({'R235':PH,'spell_source':SH,'seed':seed,'arm':arm});c=j.connect(str(path))
 with c:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('head',gen),('genesis',gen)]:c.execute('update meta set value=? where key=?',(v,k))
 c.close()
def run():
 allresults=[]
 for seed in PRE['seeds']:
  for arm in PRE['arms']:
   db=ROOT/'evidence/db'/f'R235_{arm}_S{seed}.sqlite';setup(db,seed,arm)
   for i in range(12):
    st,_,_=j.load(str(db))
    if st['phase']!='ACTIVE':break
    p={'prereg_sha':PH,'spell_sha':SH,'seed':seed,'arm':arm,'who':st['active'],'turn':st['turn']+1}
    j.event_commit(str(db),f'LAB-CMD-R235-{arm}-{seed}-T{i+1}','R235_SOURCE_BEAST_FULL_BATTLE',p,turn)
   st,head,rev=j.load(str(db));allresults.append({'arm':arm,'seed':seed,'commits':rev,'events':len(st['native_events']),'phase':st['phase'],'hp':{k:v['hp'] for k,v in st['actors'].items()},'pa':{k:v['pa'] for k,v in st['actors'].items()},'stats':st['r235']['stats']})
 for seed in PRE['save_focus_seeds']:
  arm='SAVE_FOCUS';db=ROOT/'evidence/db'/f'R235_{arm}_S{seed}.sqlite';setup(db,seed,arm)
  j.event_commit(str(db),f'LAB-CMD-R235-{arm}-{seed}-T1','R235_SOURCE_SAVE_ODD_ROC',{'prereg_sha':PH,'spell_sha':SH,'seed':seed},focus)
  st,head,rev=j.load(str(db));allresults.append({'arm':arm,'seed':seed,'commits':rev,'events':len(st['native_events']),'phase':st['phase'],'hp':{k:v['hp'] for k,v in st['actors'].items()},'pa':{k:v['pa'] for k,v in st['actors'].items()},'stats':st['r235']['stats']})
 (ROOT/'evidence/reports/R235_RUN_RESULTS.json').write_text(json.dumps({'status':'NEEDS_INDEPENDENT_AUDIT','data':allresults,'historical_replays':0},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(allresults,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
