"""R228 source-specific Flecha de Trava combat mobility loop; Mestre-only TEST.
This file does not define canonical block dimensions or Varok's official speed.
"""
from __future__ import annotations
import sys,json,hashlib,copy,random
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
import r214_native_causal_bilateral as old
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,EffectBlocked,
 apply_weapon_attack,apply_flecha_trava_post_hit,expire_flecha_trava_next_turn,
 move_via_verified_path,begin_source_turn,end_source_turn,Resistances,effective_movement_speed)
P=(ROOT/'sources/R228_PREREG_BEFORE_EXEC.json').read_bytes();PR=json.loads(P);PH=hashlib.sha256(P).hexdigest()
S=(ROOT/'sources/R228_ISKIEL_FROZEN_MECHANICAL_SOURCE.json').read_bytes();SH=hashlib.sha256(S).hexdigest();SP=json.loads(S)
PAGE='3f6c2b324ede81a78a59d3d81fd5e966'; COMBAT='3ebc2b324ede81f1be4be8804ac113c0'
PROOF=FrozenRuleEvidence(PAGE,'R228-ISKIEL-FLECHA-READBACK',SH,'2026-10-21','R228-SOURCE-PRIMARY-EXCERPT-ONLY')
SOURCE=AbilitySource('R228-ISKIEL-FLECHA-TRAVA','attack','STANDARD',PAGE,PROOF.rule_id,'RULE-DERIVED',required_pa=55,requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081')
MOVE=AbilitySource('R228-MOVE','move','MOVEMENT',COMBAT,'R228-RULE-MOVE','RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='V081')
MPROOF=FrozenRuleEvidence(COMBAT,MOVE.rule_id,SH,'2026-10-21','R228-FIXTURE-GEOMETRY-CONDITIONAL')

def dice(seed,label,n,faces):
 r=random.Random(int.from_bytes(hashlib.sha256(f'R228|{seed}|{label}|{n}d{faces}'.encode()).digest(),'big'))
 return tuple(r.randint(1,faces) for _ in range(n))

def initial(db,seed,case):
 j.init_db(str(db),'A',seed);s=j.initial('A',seed)
 v=old.source_actor('V','V',[0,0])['resource'];v['pa']=324;v['base_speed']='12';v['standard']=0
 i=Combatant('I',514,484,132,0,0,0,0,'(1.5,0)',rank='Ouro Negro',maximum_hp=514,base_speed='12')
 s.update({'scene':f'R228-{case}-{seed}','seed':seed,'actors':{'I':asdict(i),'V':v},'native_events':[],
 'phase':'ACTIVE','active':'I','round':1,'source_hash':SH,'prereg_hash':PH,
 'r228':{'case':case,'world_canon':False,'target_speed_source':'TEST_FROZEN_12M_NOT_WORLD_RULE',
 'adjacency':'DECLARED_TEST_PRE_AIM_1.5M_NOT_UNIVERSAL','FLECHA_COST':55,'FLECHA_RANK':'ON5',
 'result':None}})
 con=j.connect(str(db));h=j.sha({'prereg':PH,'seed':seed,'case':case})
 with con:
  for k,val in [('state',j.canonical(s)),('scene',s['scene']),('genesis',h),('head',h)]:con.execute('update meta set value=? where key=?',(val,k))
 con.close()

def scene(st):return Scene({k:Combatant(**copy.deepcopy(v)) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R228-FLECHA-TEST-CONDITIONAL')
def sync(st,s):st['actors']={k:asdict(v) for k,v in s.actors.items()};st['native_events']=copy.deepcopy(s.events)

def arrow(st,p,seq):
 if st['phase']!='ACTIVE' or st['active']!='I' or p['ph']!=PH or p['case']!=st['r228']['case']:raise EffectBlocked('SOURCE_PREREG')
 s=scene(st);a=s.actors['I'];d=s.actors['V'];before=len(s.events)
 t=dice(st['seed'],'HIT',4,6);dam=dice(st['seed'],'DAMAGE',8,10);cr=tuple(p['critical'])
 if len(cr)!=3 or any(z<1 or z>6 for z in cr):raise EffectBlocked('critical tape')
 s.record({'action':'R228_FLECHA_DECLARED','by':'I','target':'V','PA_pledged':55,'before_attack_rng':True,'source_page':PAGE})
 s.record({'action':'R228_RNG_TAPE','by':'I','critical':cr,'attack_dice':t,'damage_dice':dam,'source_stream':'SHA256-SEED-ACTION'})
 atk=apply_weapon_attack(s,'I','V',source=SOURCE,
  state=ActorActionState('I',20,a.pa,(SOURCE.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('V',)),
  proofs=(PROOF,),roll_score=sum(t)+101,damage=sum(dam)+33,damage_tag='perfurante',rd=Resistances(general=35,provenance='VAROK-TEST-RD35'),
  damage_dice_groups=((8,10),),damage_roll_groups=(dam,),damage_fixed_bonus=33,
  critical_sequence=cr,attack_roll_attempts=(t,),attack_bonus=101,lab_negative_critical_policy=True)
 f=apply_flecha_trava_post_hit(s,'I','V',atk,source_page=PAGE,cost_pa=55)
 st['r228']['result']={'hit':atk['hit'],'critical':atk['critical'],'physical_loss':atk['hp_loss_actual'],
 'slow':f['slow_applied'],'movement_speed_when_hit':str(effective_movement_speed(d)),'PA_free_after':a.pa}
 st['phase']='TARGET_TURN';st['active']='V';sync(st,s)
 return {'new_events':copy.deepcopy(s.events[before:]),'source_gate':True,'R225_FLOOR_NOT_NEEDED':True}

def target_turn(st,p,seq):
 if st['phase']!='TARGET_TURN' or st['active']!='V' or p['ph']!=PH:raise EffectBlocked('TARGET_TURN_SOURCE')
 s=scene(st);v=s.actors['V'];before=len(s.events)
 begin_source_turn(s,'V')
 speed=effective_movement_speed(v)
 assert speed==(Fraction(6) if st['r228']['result']['hit'] else Fraction(12))
 # Before moving, Varok legally attempts an equipped melee attack at the declared 1.5m fixture distance.
 # The actual attack uses the native resolver, and does not get a fabricated bonus for the source speed effect.
 tr=dice(st['seed'],'VAROK-HIT',4,6);dd=dice(st['seed'],'VAROK-DMG',10,10)
 atk=apply_weapon_attack(s,'V','I',source=old.NORM['V'],
  state=ActorActionState('V',20,v.pa,(old.NORM['V'].action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('I',)),
  proofs=(old.PROOFS['V'],),roll_score=sum(tr)+old.SRC['V']['attack_bonus'],
  damage=sum(dd)+old.SRC['V']['damage_bonus'],damage_tag='impacto',rd=Resistances(general=25,provenance='ISKIEL-FROZEN-RD25'),
  damage_dice_groups=((10,10),),damage_roll_groups=(dd,),damage_fixed_bonus=old.SRC['V']['damage_bonus'],
  critical_sequence=(3,4,3),attack_roll_attempts=(tr,),attack_bonus=old.SRC['V']['attack_bonus'])
 # A source path with cost 5m is legal under both 12m unmodified and 6m slowed.
 ev=move_via_verified_path(s,'V',source=MOVE,
  state=ActorActionState('V',20,v.pa,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
  proofs=(MPROOF,),destination='(5,0)',path_evidence='R228-EXPLICIT-OPEN-TEST-PATH-FIVE-METRES',
  travel_cost=Fraction(5),speed=speed)
 end_source_turn(s,'V')
 if st['r228']['result']['hit']:
  expire_flecha_trava_next_turn(s,'V')
 st['phase']='NEXT_TURN';st['active']='V';st['round']=2
 st['r228']['result'].update({'target_attack_hit':atk['hit'],'target_move_cost':5,'target_speed_during':str(speed),
  'speed_after_expiration':str(effective_movement_speed(v)),'target_hp_after':v.hp})
 sync(st,s)
 return {'new_events':copy.deepcopy(s.events[before:]),'actual_native_attack':1,'move_and_expiry':True}

def next_turn(st,p,seq):
 if st['phase']!='NEXT_TURN' or st['active']!='V' or p['ph']!=PH:raise EffectBlocked('NEXT_TURN_SOURCE')
 s=scene(st);v=s.actors['V'];before=len(s.events)
 begin_source_turn(s,'V')
 speed=effective_movement_speed(v)
 if speed!=12:raise EffectBlocked('SPEED_NOT_RESTORED')
 move_via_verified_path(s,'V',source=MOVE,
  state=ActorActionState('V',20,v.pa,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
  proofs=(MPROOF,),destination='(12,0)',path_evidence='R228-EXPLICIT-OPEN-TEST-PATH-SEVEN-METRES',
  travel_cost=Fraction(7),speed=speed)
 st['phase']='CENSORED_HORIZON';st['active']=None
 st['r228']['result'].update({'next_turn_movement_cost':7,'next_turn_speed':str(speed)})
 sync(st,s)
 return {'new_events':copy.deepcopy(s.events[before:]),'horizon':'AFTER_RESTORED_MOVEMENT'}

def run():
 out=[]
 for p in PR['scenes']:
  case=p['case'];seed=p['seed'];path=ROOT/'evidence/db'/f'R228_{case}_S{seed}.sqlite'
  if path.exists():raise FileExistsError('ID already used:'+str(path))
  initial(path,seed,case)
  for step,fun in [('ARROW',arrow),('TARGET',target_turn),('NEXT',next_turn)]:
   j.event_commit(str(path),f'LAB-CMD-R228-{case}-{seed}-{step}',f'R228_{step}',{'case':case,'ph':PH,'critical':p['critical']},fun)
  st,h,rev=j.load(str(path));out.append({'case':case,'seed':seed,'db':path.name,'head':h,'commits':rev,'events':len(st['native_events']),'result':st['r228']['result'],'phase':st['phase']})
 result={'status':'PASS_R228_SOURCE_FLECHA_TIMED_MOVEMENT_TEST_CONDITIONAL','runs':out,'source_status':'PROPOSED_MESTRE_ONLY','speed_12m':'EXPLICIT_TEST_NOT_CANON','historical_replays':0}
 (ROOT/'evidence/reports/R228_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
