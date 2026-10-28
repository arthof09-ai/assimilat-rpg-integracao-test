"""R135 adversarial gates and source-limited RD tests.
All new DBs are lab copies. Verified negatives stop BEFORE R18 durable intent.
Does not claim official combat or general mitigation of mixed tags.
"""
import json,copy,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import r126_native_integration as m
from vlab_effects_v08 import Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,apply_weapon_attack,EffectBlocked
from vlab_rd_v08 import Resistances,DamageComponent,mitigate,RDUnresolved
PREREG={'family':'R135_NEGATIVE_GATES_V081','seed':983211,'focus':'source-physical Capa PA and AoO safe rejection; weak+AoO advantage cancellation; source specific RD Dark','baseline':'R01–R125 preserved','no_repeat':['R123 pending','R130 audit fail','R134 pending']}

def hashes(st):return m.core.sha(st)
def main():
 p=ROOT/'R135_PREREG.json';value=json.dumps(PREREG,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
 if p.exists():assert p.read_text()==value
 else:p.write_text(value)
 db=ROOT/'runs'/'R135_NEGATIVE_PRE_INTENT_983211.sqlite';m.init(db,983211)
 m.command(db,'INIT',{'seed':983211});st,_,_=m.core.load(db)
 assert st['active']=='A'
 m.command(db,'START',{'actor':'A'});st,_,_=m.core.load(db)
 tape=m.attack_tape(st,'A','F1',dis=1)
 orig_state=hashes(st);_,head,rev=m.core.load(db)
 cases=[
  ('ATTACK_TAPE_FALSIFIED','STRIKE',{'attack':{**tape,'score':tape['score']+1},'reaction':'CAPA'}),
  ('ACTOR_SELF_TARGET','STRIKE',{'attack':{**tape,'target':'A'},'reaction':'CAPA'}),
  ('UNKNOWN_REACTION','STRIKE',{'attack':tape,'reaction':'REFLETIR_MAGIA'}),
  ('BAD_MOVEMENT_ORIGIN','MOVE',{'path':['B1','B2'],'to':'B2','forced':False}),
  ('NO_SOURCE_ACTION','GIVE_FREE_PA',{'actor':'F1','amount':99}),
 ]
 results=[]
 for name,kind,payload in cases:
  try:m.command(db,kind,payload)
  except Exception as err:results.append({'name':name,'status':'DENY_PRE_INTENT','type':type(err).__name__,'reason':str(err)})
  else:raise AssertionError('INVALID_ACTION_ACCEPTED:'+name)
  again,h,r=m.core.load(db)
  assert orig_state==hashes(again) and h==head and r==rev
  with m.core.connect(db) as c:assert c.execute('select count(*) from pending').fetchone()[0]==0
 # Input snapshots deliberately corrupted IN MEMORY only, no DB write.
 for name,patch in [('CAPA_PA_34',('pa',34)),('CAPA_REACTION_0',('reaction',0))]:
  clone=copy.deepcopy(st);clone['actors']['F1']['resource'][patch[0]]=patch[1]
  try:m.verify_before(clone,'STRIKE',{'attack':m.attack_tape(clone,'A','F1',dis=1),'reaction':'CAPA'})
  except m.Hold as e:results.append({'name':name,'status':'DENY_BEFORE_INTENT_IN_MEMORY','reason':str(e)})
  else:raise AssertionError('INVALID_CAPA_ACCEPTED:'+name)
 # Missing scene positional source condition explicit; move must not execute.
 clone=copy.deepcopy(st);clone['active']='F1';clone['actors']['F1']['resource']['movement']=1
 for name,body in [('FORCED_MOVEMENT_NO_AUTOMATIC_AOO',{'path':['B1','B2'],'to':'B2','forced':True}),
                   ('UNVERIFIED_PATH',{'path':['B1','B3'],'to':'B2','forced':False})]:
  try:m.verify_before(clone,'MOVE',body)
  except m.Hold as e:results.append({'name':name,'status':'DENY_PRE_INTENT_CONDITION','reason':str(e)})
  else:raise AssertionError('FORCED_OR_FAKE_PATH_ACCEPTED')
 # In-memory source-bound single-component RD unit gates (no attack/source to Dark).
 physical=mitigate((DamageComponent(100,'perfurante','AUREN_FICHE_PHYSICAL'),),Resistances(general=35))
 dark=mitigate((DamageComponent(100,'dark','AUREN_FICHE_RD_DARK'),),Resistances(specific=(('dark',60),)))
 assert physical.effective==65 and dark.effective==40
 blocked=[]
 for name,fn in [
  ('STACKING_GENERAL35_DARK60_HOLD',lambda:mitigate((DamageComponent(100,'dark','AUREN'),),Resistances(general=35,specific=(('dark',60),)))),
  ('MIXED_TAGGED_HIT_HOLD',lambda:mitigate((DamageComponent(60,'perfurante','SRC'),DamageComponent(40,'vento','SRC')),Resistances(general=35)))]:
  try:fn()
  except RDUnresolved as err:blocked.append({'name':name,'reason':str(err)})
  else:raise AssertionError(name+' wrong accept')
 # Weak + AoO Vantagem cancellation: 1 attack tape / net0 rather than two independent rolls.
 actors={'A':Combatant('A',50,719,225,48,24,2,2,'B0',rank='Lendário',standard=0,
  movement=0,reaction=1,maximum_hp=523,base_speed=64),
  'F1':Combatant('F1',479,424,123,24,26,0,2,'B1',rank='Ouro Negro',standard=1,
  movement=1,reaction=1,maximum_hp=479,base_speed=40)}
 scene=Scene(actors,seed=983211,provenance='R135_IN_MEMORY_ONLY')
 source=AbilitySource('R135-A-AOO','attack','REACTION',m.COMBAT,'AOO','RULE-DERIVED',
  target_scope='ENEMY',reaction_trigger='EXIT_ADJACENT',effect_adapter_ready=True,
  effect_adapter_id='V081_SOURCE_AOO')
 state=ActorActionState('A',23,719,(source.action_id,),standard_available=False,
  reaction_available=True,reaction_trigger_observed='EXIT_ADJACENT',enemy_ids_visible=('F1',),
  range_confirmed=True,los_confirmed=True,geometry_confirmed=True)
 proof=(FrozenRuleEvidence(m.COMBAT,'AOO',hashlib.sha256(m.SOURCE['AOO']['excerpt'].encode()).hexdigest(),
 '2026-10-16_SOURCE','R135_GATE'),)
 evt=apply_weapon_attack(scene,'A','F1',source=source,state=state,proofs=proof,
  roll_score=217,damage=243,damage_tag='perfurante',rd=Resistances(general=22),
  damage_dice_groups=((8,8),),damage_roll_groups=((4,4,4,4,4,4,4,4),),
  damage_fixed_bonus=211,critical_sequence=(3,2,4),
  attack_roll_attempts=((4,4,4,4,4,4),),attack_bonus=193,advantage_levels=1,attack_origin='OPPORTUNITY')
 assert evt['weak_attacker'] is True and evt['net_levels']==0 and evt['hit'] is True
 assert scene.actors['A'].reaction==0 and scene.actors['A'].standard==0
 record={'count_pre_intent':len(results),'cases':results,'rd_unit':{'physical_100_rd35_net':physical.effective,
    'dark_100_rd60_net':dark.effective,'source_dark_attack_executed':False,'blocked':blocked},
   'advantage_weak_cancel_unit':{'net_levels':evt['net_levels'],'tapes':len(evt['attack_roll_attempts']),
    'attack_score':evt['roll_score'],'reaction_after':scene.actors['A'].reaction},
   'sqlite_revision_unchanged':rev,'sqlite_head_unchanged':head,'sqlite_pending':0,
   'caution':'RD Dark standalone unit not combat; source stacking and mixed damage still HOLD',
   'legacy_banks_unchanged':True}
 out=ROOT/'R135_NEGATIVE_AND_RD_RESULTS.json';out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(record,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
