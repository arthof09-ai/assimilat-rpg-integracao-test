"""R174: additive Mestre-side TEST fixture on preserved R18 WAL and v0.8.1 adapters.
Varok/Arveth are documented *proposals*, never a canonical ED or official encounter.
This module adds only frozen source snapshots, policy, scheduler handoff, and paid
on-hit source rider to already existing R18/v0.8.1 mechanics.
"""
from __future__ import annotations
import sys,json,pathlib,hashlib,random,copy
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
R173=ROOT/'deps/r173_work'
for x in [R173/'r172_work',R173/'deps/r61_extracted/work/fusion_stage12', R173, R173/'deps/native_v081_controlled']:
 sys.path.insert(0,str(x))
import vlab_effects_v08  # pin preserved native module before R171/R172 importer side effects
import vlab_r18_interactive as r18
import r172_atomic_counter as r172
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,ActorActionState,FrozenRuleEvidence,
    EffectBlocked,Resistances,apply_weapon_attack,react_defensively,begin_source_turn,end_source_turn)

VERSION='R174-ON5-SOURCE-PROPOSAL-TEST-v1'
COMBAT='https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0'
ACTORS={
 'VAROK':{'name':'Sikong Varok','source':'https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091','last_edit':'2026-10-16T10:33:26.087Z','rank':'Ouro Negro 5','level':20,'status':'PROPOSTA_MESTRE_SIDE','hp':734,'pa':324,'ca':83,'con':57,'armor':34,'fort':2,'reflex':0,'rd':35,'init_base':29,'hit_base':100,'damage_n':10,'damage_faces':10,'flat':48,'damage_type':'impacto','weapon':'Machado do Juramento Raiz-Ferro','power':'Quebra do Tronco','power_pa':60,'power_dice':(6,12),'speed_m':None},
 'ARVETH':{'name':'Sikong Arveth','source':'https://app.notion.com/p/3f6c2b324ede8105891fc647242e61ca','last_edit':'2026-10-16T10:33:37.349Z','rank':'Ouro Negro 5','level':20,'status':'PROPOSTA_MESTRE_SIDE','hp':806,'pa':344,'ca':93,'con':57,'armor':32,'fort':2,'reflex':2,'rd':30,'init_base':25,'hit_base':72,'damage_n':8,'damage_faces':10,'flat':35,'damage_type':'perfurante','weapon':'Bastião das Sete Gargantas','power':None,'power_pa':None,'power_dice':None,'speed_m':None}}
EXCERPTS={
 'VAROK':'VIDA 734 | PA livre 324 | CA 83 | CON 57 | Armadura 34 | Fortitude +2 | RD físico35 | Iniciativa 4d6+29 | Machado 4d6+100; 10d10+48 impacto/corte | Quebra após acerto +6d12 impacto por 60 PA, uma vez/cena | reação 1 por rodada',
 'ARVETH':'VIDA 806 | PA livre 344 | CA 93 | CON 57 | Armadura 32 | Fortitude +2 | RD físico30 | Iniciativa 4d6+25 | Bastião 4d6+72; 8d10+35 físico perfurante | reação 1 por rodada',
 'DEFENDER':'Antes do ataque declarar reação | Defender = 6 + CON + Armadura + Fortitude; empate protege | 1 reação por rodada',
 'SOURCE_TURN':'v0.8.1 begin_source_turn reabre 1 ação e 1 reação no inicio autorizado de turno; end_source_turn após ação',
}
PROOFS={}
for who in ACTORS:
 f=ACTORS[who];h=hashlib.sha256(EXCERPTS[who].encode()).hexdigest()
 PROOFS[who]=FrozenRuleEvidence(f['source'],'R174-'+who+'-ATTACK',h,f['last_edit'],'LITERAL_EXCERPT_HASH_NOT_NOTION_BINARY_SIGNATURE')
PROOFS['DEFENDER']=FrozenRuleEvidence(COMBAT,'R174-DEFENDER',hashlib.sha256(EXCERPTS['DEFENDER'].encode()).hexdigest(),'2026-10-07T23:51:04.971Z','EXCERPT_NOT_FULL_PAGE_HASH')
SRC={who:AbilitySource('R174-'+who+'-WEAPON','attack','STANDARD',f['source'],PROOFS[who].rule_id,'RULE-DERIVED',required_pa=0,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081-WEAPON') for who,f in ACTORS.items()}
DEF_SRC=AbilitySource('R174-VAROK-DEFENDER','reaction','REACTION',COMBAT,PROOFS['DEFENDER'].rule_id,'RULE-DERIVED',target_scope='SELF',reaction_trigger='BEFORE-ATTACK',effect_adapter_ready=True,effect_adapter_id='V081-DEFENSE')

def draw(seed,key,n,sides):
 d=hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{sides}'.encode()).digest()
 return [random.Random(int.from_bytes(d,'big')).randint(1,sides) for _ in range(n)] if False else [v for v in _draw(seed,key,n,sides)]
def _draw(seed,key,n,sides):
 d=hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{sides}'.encode()).digest()
 rng=random.Random(int.from_bytes(d,'big'))
 return [rng.randint(1,sides) for _ in range(n)]
def attack_tape(seed,actor,turn):
 f=ACTORS[actor];return {'critical':_draw(seed,f'{actor}-TURN{turn}-CRIT',3,6),
 'hit':_draw(seed,f'{actor}-TURN{turn}-HIT',4,6),
 'hit_weak':_draw(seed,f'{actor}-TURN{turn}-HIT-WEAK',4,6),
 'damage':_draw(seed,f'{actor}-TURN{turn}-DAMAGE',f['damage_n'],f['damage_faces']),
 'power':_draw(seed,f'{actor}-TURN{turn}-POWER',6,12) if actor=='VAROK' else []}

def genesis(seed,policy):
 s=r18.initial('A',seed)
 s.update({'r174_version':VERSION,'r174_policy':policy,'r174_source_status':'TWO_MASTER_SIDE_ENCOUNTER_PROPOSALS_NOT_ED_OR_OFFICIAL',
 'r174_scope':['SOURCE_DERIVED_PHYSICAL_ATTACKS','ONE_PHYSICAL_SOURCE_RIDER_60PA','DEFENDER','NATIVE_TURN_REFRESH','EXPLICIT_INITIAL_ADJACENCY'],
 'r174_unknown':['NO_ADJACENCY_MOVEMENT_OR_RANGE_PATH_EXECUTED','NOT_CANONICAL_NPC_APPLY','NO_INDEPENDENT_HOLDOUT'],
 'r174_native_events':[],'r174_turn_history':[],'r174_power_used':False,'r174_attacks_by_actor':{'VAROK':0,'ARVETH':0},
 'r174_metrics':{'attacks':0,'hits':0,'hp_loss':0,'post_rd':0,'overkill':0,'reaction_spent':0,'defense_prevented_hp':0,'pa_spent':0,'power_uses':0,'crit_positive':0,'crit_negative':0},
 'r174_start':'AT_START_BOTH_ADJACENT_SAME_TEST_ZONE_SOURCE_MELEE_VALID_SCENARIO_INPUT_NO_MOVEMENT',
 'r174_seed_type':'DEV_NOT_HOLDOUT','r174_init':None})
 s.update({'synthetic':True,'source_status':'MESTRE_SOURCE_PROPOSAL_TEST','source_confidence':'SOURCE_DERIVED_NOT_OFFICIAL','actors':{},'order':[],'phase':'INIT','active':None,'round':0,'turn':0})
 for who,f in ACTORS.items():
  res=asdict(Combatant(who,f['hp'],f['pa'],f['ca'],f['con'],f['armor'],f['fort'],f['reflex'],f'ADJACENT_TO_OTHER_{who}',rank='Ouro Negro',maximum_hp=f['hp'],base_speed=None,standard=0,movement=0,reaction=1))
  s['actors'][who]={'name':f['name'],'stats':{'source':f['source'],'source_version':f['last_edit'],'source_kind':f['status'],'rank':f['rank'],'rd_physical':f['rd'],'initiative':'4d6+'+str(f['init_base']),'weapon_attack':'4d6+'+str(f['hit_base']),'weapon':f['weapon']},'resource':res}
 return s

def scene_of(st):
 return Scene({a:Combatant(**copy.deepcopy(o['resource'])) for a,o in st['actors'].items()},events=copy.deepcopy(st['r174_native_events']),seed=st['seed'],provenance='R174-SOURCE-NPCS-PROPOSED-MESTRE-SIDE-NO-CANON')
def sync(st,sc):
 st['r174_native_events']=copy.deepcopy(sc.events)
 for aid,obj in sc.actors.items():st['actors'][aid]['resource']=asdict(obj)

def init_db(db,seed,policy):
 r18.init_db(db,'A',seed)
 c=r18.connect(db)
 try:
  assert c.execute('SELECT COUNT(*) FROM events').fetchone()[0]==0
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(genesis(seed,policy)),))
 finally:c.close()

def do_start(st,p,seq):
 if st['phase']!='INIT' or p!={'mode':'SOURCE_ON5_INITIATIVE_4D6_PLUS_SPECIFIC'}:raise EffectBlocked('start schema')
 rolls=[]
 for who in ('VAROK','ARVETH'):
  t=_draw(st['seed'],f'INIT-{who}',4,6)
  rolls.append({'actor':who,'roll':t,'bonus':ACTORS[who]['init_base'],'total':sum(t)+ACTORS[who]['init_base']})
 if rolls[0]['total']==rolls[1]['total']:raise EffectBlocked('INITIATIVE_TIE_NO_DEFINED_RULE_PRE_INTENT_BLOCK')
 rolls.sort(key=lambda x:-x['total'])
 st['order']=[x['actor'] for x in rolls];st['active']=st['order'][0];st['phase']='ACTIVE';st['round']=1;st['turn']=0;st['r174_init']=rolls
 sc=scene_of(st);entry=begin_source_turn(sc,st['active']);sync(st,sc)
 return {'type':'SOURCE_ON5_INIT','rolls':rolls,'order':st['order'],'first_turn_event':entry,'source_status':st['r174_source_status'],'no_official_effect':True}

def do_attack(st,p,seq):
 if st['phase']!='ACTIVE':raise EffectBlocked('combat not active')
 a=st['active'];d='VAROK' if a=='ARVETH' else 'ARVETH'
 if p['actor']!=a or p['target']!=d or p['policy']!=st['r174_policy'] or p['seed']!=st['seed']:raise EffectBlocked('actor policy mismatch')
 cnt=st['r174_attacks_by_actor'][a]+1
 if p['actor_turn']!=cnt or p['roll_tape']!=attack_tape(st['seed'],a,cnt):raise EffectBlocked('future roll leakage / spoof')
 old_events=st['r174_native_events'];sc=scene_of(st);src=SRC[a];f=ACTORS[a];dd=ACTORS[d];t=p['roll_tape']
 attacker=sc.actors[a];defender=sc.actors[d]
 if attacker.standard!=1 or attacker.hp<=0 or defender.hp<=0:raise EffectBlocked('invalid standard or KO')
 # Decision taken before checking attack dice. Source-based Varok reaction: DEFENDER.
 defense_decided=(d=='VAROK' and st['r174_policy'] in ('DEFEND_VAROK','DEFEND_NO_POWER') and defender.reaction==1)
 critical=tuple(t['critical']);weak=(attacker.hp*10<f['hp']);rolls=(tuple(t['hit']),tuple(t['hit_weak'])) if weak else (tuple(t['hit']),)
 score=(min(map(sum,rolls))+f['hit_base']-2) if weak else sum(t['hit'])+f['hit_base']
 defense=None
 if defense_decided:
  rs=ActorActionState('VAROK',20,defender.pa,(DEF_SRC.action_id,),reaction_trigger_observed='BEFORE-ATTACK',enemy_ids_visible=(a,))
  defense=react_defensively(sc,'VAROK',kind='DEFENDER',attack_score=score,announced_before=True,trigger_source='BEFORE-ATTACK',source=DEF_SRC,state=rs,proofs=(PROOFS['DEFENDER'],))
 # A conditional ON-HIT source rider is selected after the attack roll is available.
 # The single v0.8.1 resolution receives BOTH dice groups so RD is applied ONCE.
 positive=(critical[:2]==(6,6) and critical[2]>=5)
 negative=(critical[:2]==(1,1) and critical[2]<=2)
 would_hit=(score>defender.ca or positive) and not negative
 apply_power=(a=='VAROK' and would_hit and not st['r174_power_used'] and attacker.pa>=60 and st['r174_policy']!='DEFEND_NO_POWER')
 dmg_groups=((f['damage_n'],f['damage_faces']),)+(((6,12),) if apply_power else ())
 dmg_rolls=(tuple(t['damage']),)+((tuple(t['power']),) if apply_power else ())
 raw=sum(sum(v) for v in dmg_rolls)+f['flat']
 action=ActorActionState(a,20,attacker.pa,(src.action_id,),enemy_ids_visible=(d,))
 event=apply_weapon_attack(sc,a,d,source=src,state=action,proofs=(PROOFS[a],),roll_score=score,damage=raw,damage_tag=f['damage_type'],rd=Resistances(general=dd['rd'],provenance='MASTER_SPECIFIC_PHYSICAL_RD'),defense_event=defense,
   damage_dice_groups=dmg_groups,damage_roll_groups=dmg_rolls,damage_fixed_bonus=f['flat'],critical_sequence=critical,
   attack_roll_attempts=rolls,attack_bonus=f['hit_base'],lab_negative_critical_policy=True)
 if apply_power:
  if not event['hit']:raise EffectBlocked('power hit mismatch')
  attacker.pa-=60;st['r174_power_used']=True
  power_event=sc.record({'action':'ON_HIT_ENERGY_RIDER','by':'VAROK','after_attack_seq':event['seq'],'source_page':f['source'],
    'ability':'Quebra do Tronco','trigger':'ATTACK_HIT','cost_pa':60,'power_damage_dice':list(t['power']),
    'included_in_attack_seq':event['seq'],'rd_applied_once':True,'pa_after':attacker.pa})
 else:power_event=None
 event['r174_tx_seq']=seq;event['r174_source_actor']=f['source'];event['r174_source_defender']=dd['source']
 event['r174_source_attack']=f['weapon'];event['r174_paid_power']=bool(apply_power);event['r174_defense_event_seq']=defense['seq'] if defense else None
 end=end_source_turn(sc,a)
 m=st['r174_metrics'];m['attacks']+=1;m['hits']+=int(event['hit']);m['hp_loss']+=event['hp_loss_actual'];m['post_rd']+=event['net'];m['overkill']+=event['overkill'];m['reaction_spent']+=int(bool(defense));m['pa_spent']+=60*int(apply_power);m['power_uses']+=int(apply_power);m['crit_positive']+=int(event['critical']=='POSITIVE');m['crit_negative']+=int(event['critical']=='NEGATIVE')
 if defense and defense['damage_negated'] and event['hit']:
  # Preserved resolver did not call mitigate if prevented; independent auditor checks.
  m['defense_prevented_hp']+=max(0,(sum(t['damage'])+f['flat'])-dd['rd'])
 st['r174_attacks_by_actor'][a]+=1
 if sc.actors[d].hp==0:
  st['phase']='FINISHED';st['winner']=a;st['finish_reason']='HP0_SOURCE_PROPOSAL_TEST';st['active']=None
  scheduler={'next':None,'ko_actor':d,'source_status':'NOT_CAMPAIGN'}
 else:
  scheduler=r18._next_turn(st)
  newcomer=st['active']
  # R18 source-independent handoff opens standard=1. Transfer to the preserved
  # v0.8.1 begin_source_turn (precondition standard=0), which also refreshes reaction.
  # Do not add a second reaction, or refresh until the next actor's own turn.
  sc.actors[newcomer].standard=0
  start=begin_source_turn(sc,newcomer)
  scheduler['native_source_turn_start_seq']=start['seq']
 sync(st,sc)
 events=copy.deepcopy(sc.events[len(old_events):]);detail={'kind':'R174_SOURCE_ATTACK','attacker':a,'target':d,'policy':st['r174_policy'],
  'roll_tape':t,'source':f['source'],'attack':copy.deepcopy(event),'defense':copy.deepcopy(defense) if defense else None,
  'energy_activation':copy.deepcopy(power_event) if power_event else None,'native_events':events,
  'source_turn_end_seq':end['seq'],'scheduler':scheduler,'HP_after':{k:v.hp for k,v in sc.actors.items()},
  'PA_after':{k:v.pa for k,v in sc.actors.items()},'reaction_after':{k:v.reaction for k,v in sc.actors.items()},
  'synthetic':True,'official_effects':0,'source_status':st['r174_source_status']}
 st['r174_turn_history'].append({'tx_seq':seq,'actor':a,'target':d,'attack_seq':event['seq'],
  'hit':event['hit'],'damage_effective':event['net'],'hp_actual':event['hp_loss_actual'],
  'reaction_spent':bool(defense),'power_pa':60 if apply_power else 0,'HP_after':detail['HP_after'],'PA_after':detail['PA_after'],'reaction_after':detail['reaction_after']})
 return detail

def battle(directory,seed,policy,max_attacks=75):
 dr=pathlib.Path(directory);dr.mkdir(parents=True,exist_ok=True)
 db=dr/f'R174_VAROK_ARVETH_{policy}_DEV{seed}.sqlite'
 init_db(db,seed,policy)
 r18.event_commit(db,'LAB-CMD-R174-'+policy+'-INIT','R174_SOURCE_INIT',{'mode':'SOURCE_ON5_INITIATIVE_4D6_PLUS_SPECIFIC'},do_start)
 for idx in range(max_attacks):
  st,_,_=r18.load(db)
  if st['phase']=='FINISHED':break
  a=st['active'];d='VAROK' if a=='ARVETH' else 'ARVETH';n=st['r174_attacks_by_actor'][a]+1
  p={'actor':a,'target':d,'actor_turn':n,'policy':policy,'seed':seed,'roll_tape':attack_tape(seed,a,n)}
  r18.event_commit(db,f'LAB-CMD-R174-{policy}-{idx+1:04d}','R174_SOURCE_ATTACK',p,do_attack)
 st,_,_=r18.load(db);r172.write_checkpoint(db)
 return db,st

def directed(directory):
 # Deterministic discriminant specified BEFORE executing: Arveth hit 4+4+4+4+72=88,
 # Varok CA83 vs Defender99. Same roll tape and HP in BOTH branches.
 dr=pathlib.Path(directory);dr.mkdir(parents=True,exist_ok=True)
 records=[]
 for policy in ('DEFEND_VAROK','HOLD_VAROK'):
  db=dr/f'R174_DIRECTED_DEFENDER_{policy}.sqlite';init_db(db,1740099,policy)
  # Directed isolated event with Varok standard untouched (not a full initiative scene)
  def single(st,p,seq):
   st['phase']='ACTIVE';st['active']='ARVETH';st['order']=['ARVETH','VAROK'];st['round']=1
   s=scene_of(st);s.actors['ARVETH'].standard=1
   defense=None
   if policy=='DEFEND_VAROK':
    state=ActorActionState('VAROK',20,324,(DEF_SRC.action_id,),reaction_trigger_observed='BEFORE-ATTACK',enemy_ids_visible=('ARVETH',))
    defense=react_defensively(s,'VAROK',kind='DEFENDER',attack_score=88,announced_before=True,trigger_source='BEFORE-ATTACK',source=DEF_SRC,state=state,proofs=(PROOFS['DEFENDER'],))
   src=SRC['ARVETH'];a=ActorActionState('ARVETH',20,344,(src.action_id,),enemy_ids_visible=('VAROK',))
   att=apply_weapon_attack(s,'ARVETH','VAROK',source=src,state=a,proofs=(PROOFS['ARVETH'],),roll_score=88,damage=75,damage_tag='perfurante',rd=Resistances(general=35,provenance='VAROK_RDF35'),defense_event=defense,
    damage_dice_groups=((8,10),),damage_roll_groups=((5,5,5,5,5,5,5,5),),damage_fixed_bonus=35,
    critical_sequence=(2,3,4),attack_roll_attempts=((4,4,4,4),),attack_bonus=72)
   sync(st,s)
   st['phase']='FINISHED';st['active']=None;st['winner']=None;st['finish_reason']='DIRECTED_DISCRIMINANT_ONE_HIT_ONLY'
   return {'attack':att,'defense':defense,'events':copy.deepcopy(s.events),'hp_varok':s.actors['VAROK'].hp,'reaction_varok':s.actors['VAROK'].reaction,'scope':'DIRECTED_SOURCE_DISCRIMINANT_NOT_BATTLE'}
  row=r18.event_commit(db,'LAB-CMD-R174-DIRECTED-'+policy,'R174_DIRECTED_PROOF',{'tape':{'attack':[4,4,4,4],'critical':[2,3,4],'damage':[5]*8},'pre_registered':True},single)
  r172.write_checkpoint(db);records.append({'policy':policy,'db':str(db),'receipt':row['detail']})
 return records

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--seed',type=int,default=1740101);o=p.parse_args()
 for pol in ('DEFEND_VAROK','HOLD_VAROK','DEFEND_NO_POWER'):
  db,st=battle(pathlib.Path(o.output)/'duels',o.seed,pol)
  print(json.dumps({'db':str(db),'winner':st['winner'],'phase':st['phase'],'attacks':st['r174_metrics'],'round':st['round'],'HP':{a:v['resource']['hp'] for a,v in st['actors'].items()},'PA':{a:v['resource']['pa'] for a,v in st['actors'].items()}},ensure_ascii=False))
 print(json.dumps({'directed':[{k:v for k,v in x.items() if k!='receipt'} for x in directed(pathlib.Path(o.output)/'directed')]},ensure_ascii=False))
