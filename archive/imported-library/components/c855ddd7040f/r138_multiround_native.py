"""CM-000006 R138: controlled additive v0.8.1+R18+R26 multi-round driver.
Pure deterministic experimental scenario; no canonical actors instantiated in campaign.
"""
import hashlib,json,sqlite3,copy,sys
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r126_native_integration as old
import r132_heal_corrected as heal
from r126_shared_three_actor import core,r26,Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState
from vlab_effects_v08 import (begin_source_turn,end_source_turn,apply_weapon_attack,apply_capa_poeira,
 apply_marca_passos,apply_reconstituicao_seiva,apply_passo_fuligem,apply_pulso_estabilizacao,
 move_via_verified_path,EffectBlocked)
from vlab_rd_v08 import Resistances
A='A';F='F1';E='E'; ACTORS=(A,F,E)
PROFILE={'A':copy.deepcopy(old.P['A']),'F1':copy.deepcopy(old.P['F1']),'E':copy.deepcopy(heal.EP)}
TEAM={'A':'ONE','F1':'TWO','E':'TWO'}
FERYN=old.FERYN;ERISTAN=heal.EID;COMBAT=old.COMBAT
TOPOLOGY=old.TOPOLOGY
PREREG={
 'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R138-R145','baseline':'R01–R137 IMMUTABLE',
 'runs':[{'id':'R138_MULTI_SOURCE_FERYN_ERISTAN_DEV_S991401','seed':991401,'family':'DEVELOPMENT','horizon_rounds':4},
         {'id':'R138_MULTI_SOURCE_FERYN_ERISTAN_DEV_S991402','seed':991402,'family':'RESERVED_FALLBACK_ONLY','horizon_rounds':4}],
 'source_pages':{'system_combat':COMBAT,'Feryn':FERYN,'Eristan':ERISTAN,'Auren':old.base.AUREN,
 'Mestre_R50_R51':'3f3c2b324ede819496ddd7f93bd7e5d2'},
 'profiles':'Auren L3 and Master-side proposed Feryn ON5 + Eristan ON5; technical instances, not team-equivalent, not canonical snapshots',
 'rule_R26':'individual dice+explicit initiative bonus, DES tie-break then new roll of tied only',
 'source_abilities':{
  'CAPA':'Feryn 35PA Reaction applies disadvantage against announced physical attack',
  'MARCA':'Feryn 25PA Standard +10 ONLY Perception/Survival 3 turns; exact turn expiry HOLD',
  'PASSO':'Feryn 25PA Movement +12m speed DURING THIS TURN; expires at own turn end',
  'RECONSTITUICAO':'Eristan 75PA Standard 8d10+25 HP +20 gloves once, cap max HP, ally within 5m',
  'PULSO':'Eristan 45PA Reaction 3d10+10 after ally suffers damage <=3m; gloves +20 as documented direct healing once, no prevention of lethal',
  'AOO':'combat Rule3 voluntary exit of adjacency, +1 advantage and consumes reaction',
 },
 'experimental_distance_m':{'F-E_before_move':3,'F-E_after_move':2,'F-A_for_marca':1.5},
 'distance_status':'independent scene fixture for specific spell target conditions; B0–B3 topology NOT converted to metres; no line-of-sight beyond fixture',
 'positions':{'A':'B0','F1':'B1','E':'B3'},
 'policy_by_round':{
 '1':{'A':'ATTACK_F_WITH_CAPA','F1':'MARCA_A','E':'HEAL_F'},
 '2':{'A':'FOREGO_STANDARD','F1':'PASSO_MOVEMENT_AND_FOREGO_STANDARD','E':'HEAL_F'},
 '3':{'A':'FOREGO_STANDARD','F1':'EXIT_ADJACENCY_AOO_AND_E_PULSO','E':'HEAL_F'},
 '4':{'A':'MOVE_TO_B1_AND_ATTACK_F_IF_ALIVE','F1':'FOREGO_STANDARD_IF_ALIVE','E':'HEAL_F_IF_ALIVE'},
 },
 'temporal_conventions':{'PASSO':'literal THIS TURN; expire on END own turn',
 'MARCA':'no official three-turn expiration: state persists only as evidence with BOUNDARY_HOLD; never +10 attack; no automatic removal'},
 'RNG':'R18 SHA-to-Python PRNG deterministic experimental; not physical/canon certified',
 'mechanical_limits':['No forced movement','No simultaneous AoO resolution','No beast proficiency inferred',
 'Critical failure stops before intent','No lightning RD assumed','No magical counterattack to Reflex save',
 'Eristan Feryn ON5 do not have Demon Spirits; not A/C official power grade',
 'Battle stops horizon4 as CENSORED, no victory invented'],
 'no_repeat':['R01–R137','R123 AFTER_INTENT','R130 QA_FAIL','R134 AFTER_INTENT','R124 5x5 censored']}

def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
def freeze():
 p=ROOT/'R138_PREREG.json';b=can(PREREG)
 if p.exists():assert p.read_text()==b
 else:p.write_text(b)
 return p

def proof(page,rule):
 return (FrozenRuleEvidence(page,rule,hashlib.sha256((page+'|'+rule+'|R138_REOPENED_SOURCES').encode()).hexdigest(),
  '2026-10-16_NOTION_READ','R138_SOURCE_AUTH'),)

def source_state(st,who,target,kind):
 p=PROFILE[who];r=st['actors'][who]['resource'];action='R138-'+who+'-'+kind
 args={
  'ATTACK':('attack','STANDARD',0,'ENEMY',None),
  'CAPA':('reaction','REACTION',35,'SELF','ATTACK_DECLARED'),
  'MARCA':('control','STANDARD',25,'ENEMY',None),
  'PASSO':('move','MOVEMENT',25,'SELF',None),
  'MOVE':('move','MOVEMENT',0,'NONE',None),
  'AOO':('attack','REACTION',0,'ENEMY','EXIT_ADJACENT'),
  'HEAL':('heal','STANDARD',75,'ALLY',None),
  'PULSO':('heal','REACTION',45,'ALLY','ALLY_AFTER_DAMAGE')}
 typ,economy,cost,scope,trigger=args[kind]
 page=ERISTAN if who=='E' else COMBAT if kind in ('AOO','MOVE') else p['source']
 source=AbilitySource(action,typ,economy,page,'R138-SOURCE-'+kind,'RULE-DERIVED',
  required_pa=cost,target_scope=scope,reaction_trigger=trigger,effect_adapter_ready=True,
  effect_adapter_id='V081_R138_NATIVE_SOURCE')
 state=ActorActionState(who,p['rank_index'],r['pa'],(action,),
  standard_available=r['standard']==1,movement_available=r['movement']==1,
  reaction_available=r['reaction']==1,reaction_trigger_observed=trigger,
  range_confirmed=True,los_confirmed=True,geometry_confirmed=True,
  enemy_ids_visible=(target,) if scope=='ENEMY' else (),ally_ids_visible=(target,) if scope=='ALLY' else ())
 return source,state,proof(page,source.rule_id)

def dice(st,who,kind,nonce,count,faces):
 return core.dice(st['seed'],nonce,'R138-'+who+'-'+kind,count,faces)

def attack_tape(st,who,target,kind='NORMAL',adv=0,dis=0):
 p=PROFILE[who];n=st['action_nonce'][who]+1;r=st['actors'][who]['resource']
 weak=10*r['hp']<p['hp'];net=max(-4,min(4,adv-dis-int(weak)))
 attempts=[dice(st,who,kind+'-HIT-'+str(i),n,p['attack_dice'],6) for i in range(1+abs(net))]
 score=(max(map(sum,attempts))+2*net if net>0 else min(map(sum,attempts))+2*net if net<0 else sum(attempts[0]))+p['attack_flat']
 crit=[dice(st,who,kind+'-CRIT-'+str(i),n,1,6)[0] for i in range(3)]
 damages=[dice(st,who,kind+'-DMG-'+str(i),n,group_n,faces) for i,(group_n,faces) in enumerate(p['damage_dice'])]
 return {'actor':who,'target':target,'nonce':n,'kind':kind,'adv':adv,'dis':dis,
   'hit_rolls':attempts,'score':score,'crit':crit,'dmg_rolls':damages,
   'normal_damage':sum(sum(a) for a in damages)+p['damage_flat']}

def badcrit(t):return t['crit'][:2]==[1,1] and t['crit'][2]<=2

def genesis(runid,seed):
 st=old.base.snapshot(runid,seed)
 st['actors'].pop('F2');st['action_nonce'].pop('F2');st['actor_turns'].pop('F2')
 e=PROFILE['E'];c=Combatant('E',e['hp'],e['pa'],e['ca'],e['con'],e['armor'],e['fort'],e['reflex'],'B3',
  rank=e['rank'],standard=0,movement=0,reaction=1,maximum_hp=e['hp'])
 st['actors']['E']={'source':ERISTAN,'source_profile':copy.deepcopy(e),'resource':asdict(c)}
 st['action_nonce']['E']=0;st['actor_turns']['E']=0
 st['actors']['A']['resource']['position']='B0';st['actors']['F1']['resource']['position']='B1'
 st.update({'stage':'R138-R145','run_id':runid,'scene':runid,'teams':TEAM,'round':0,
  'marks':{},'temporary':{},'ability_nonce':{'E_HEAL':0,'E_PULSO':0},
  'pre_registered_horizon':4,'source_fingerprint':core.sha(PREREG),
  'prereg_sha256':hashlib.sha256(freeze().read_bytes()).hexdigest(),
  'spatial_topology':TOPOLOGY,'technical_instancing':False,'no_canonical_credit':True,
  'temporal_mark_expiration':'HOLD_UNKNOWN_THREE_TURN_BOUNDARY',
  'selected_science':'technical mechanics only, no official power reference'})
 return st

def init(db,seed):
 if db.exists() or db.with_suffix(db.suffix+'-wal').exists():raise ValueError('NO_RESTART_EXISTING_DB')
 core.init_db(db,'A',seed);st=genesis(db.stem,seed)
 anchor=core.sha({'genesis':st,'lineage':'R18_R26_V081_R138_NATIVE_MULTIRROUND'})
 with core.connect(db) as con:
  for k,v in [('scene',st['scene']),('genesis',anchor),('head',anchor),('state',core.canonical(st))]:
   con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 db.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')

def initiative(st):
 rows=[]
 for who in ACTORS:
  p=PROFILE[who];d=dice(st,who,'INIT',0,p['init_dice'],6)
  rows.append({'id':who,'dice':d,'des':p['dex'],'total':sum(d)+p['init_bonus'],'source':p['source']})
 def reroll(aid,n):
  p=PROFILE[aid];return sum(dice(st,aid,'INIT-TIE',n,p['init_dice'],6))+p['init_bonus']
 return rows,r26.tie_order(rows,reroll)

def planned_attack(st,kind,p):
 if kind=='ATTACK':
  target=p['attack']['target'];rt=p.get('reaction','NONE')
  if st['active']!='A' or target!='F1' or rt not in ('CAPA','NONE'):raise ValueError('ATTACK_ACTOR_TARGET')
  if rt=='CAPA' and (st['actors']['F1']['resource']['reaction']!=1 or st['actors']['F1']['resource']['pa']<35):raise ValueError('CAPA_RESOURCES')
  expect=attack_tape(st,'A',target,dis=int(rt=='CAPA'))
 elif kind=='MOVE_F_AOO_PULSO':expect=attack_tape(st,'A','F1',kind='AOO',adv=1)
 else:raise ValueError(kind)
 if core.canonical(p['attack'])!=core.canonical(expect):raise ValueError('ATTACK_TAPE_WRONG')
 if badcrit(expect):raise ValueError('NEGATIVE_CRIT_RULE_HOLD_PRE_INTENT')
 return expect

def verify(st,kind,p):
 if kind=='INIT':
  if st['phase']!='INIT' or p!={'seed':st['seed']}:raise ValueError('INIT_WRONG')
  return
 if st['phase']!='ACTIVE':raise ValueError('NOT_ACTIVE')
 a=st['active'];r=st['actors'][a]['resource']
 if kind=='START':
  if p!={'actor':a} or r['hp']<=0 or r['standard']!=0:raise ValueError('START_WRONG')
 elif kind=='FOREGO':
  if p!={'actor':a} or r['standard']!=1:raise ValueError('FOREGO_WRONG')
 elif kind=='ATTACK':
  if r['standard']!=1 or r['hp']<=0 or st['actors']['F1']['resource']['hp']<=0:raise ValueError('ATTACK_UNAVAILABLE')
  if a!='A' or not (st['actors']['A']['resource']['position'] in TOPOLOGY[st['actors']['F1']['resource']['position']]):raise ValueError('NOT_ADJACENT')
  planned_attack(st,kind,p)
 elif kind=='MARCA':
  if a!='F1' or r['standard']!=1 or r['pa']<25 or st['marks']:raise ValueError('MARCA_DUPLICATE_OR_RESOURCES')
  if p!={'target':'A','distance_m':1.5,'line_of_sight':True}:raise ValueError('MARCA_SOURCE_RANGE_LOS')
 elif kind=='PASSO':
  if a!='F1' or r['movement']!=1 or r['pa']<25 or 'F1' in st['temporary']:raise ValueError('PASSO_RESOURCES')
  if p!={'actor':'F1','intent':'THIS_TURN_ONLY'}:raise ValueError('PASSO_TAPE')
 elif kind=='HEAL':
  if a!='E' or r['standard']!=1 or r['pa']<75:raise ValueError('HEAL_RESOURCE')
  if st['actors']['F1']['resource']['hp']<=0 or st['actors']['F1']['resource']['hp']>=479:raise ValueError('HEAL_TARGET')
  if p.get('target')!='F1' or p.get('distance_m') not in (2,3) or p.get('distance_m')>5:raise ValueError('HEAL_RANGE')
  n=st['ability_nonce']['E_HEAL']+1
  if p.get('dice')!=dice(st,'E','HEAL',n,8,10):raise ValueError('HEAL_TAPE')
 elif kind=='MOVE_F_AOO_PULSO':
  fr=st['actors']['F1']['resource'];ar=st['actors']['A']['resource'];er=st['actors']['E']['resource']
  if a!='F1' or st['round']!=3 or fr['position']!='B1' or fr['movement']!=1 or fr['hp']<=0:
   raise ValueError('F_MOVE_UNAVAILABLE')
  if ar['position']!='B0' or ar['reaction']!=1 or er['reaction']!=1 or er['pa']<45 or er['hp']<=0:
   raise ValueError('AOO_OR_PULSO_UNAVAILABLE')
  if p.get('path')!=['B1','B2'] or p.get('forced') or p.get('pulse_distance_m')!=2:
   raise ValueError('GEOMETRY_OR_FORCE')
  atk=planned_attack(st,kind,p)
  # Strictly the documented A attack always hits F: high numeric score even under reductions;
  # prevalidate survival to ensure reaction cannot be used as resurrection after lethal blow.
  maxcrit=sum(n*f for n,f in PROFILE['A']['damage_dice']) if atk['crit'][:2]==[6,6] and atk['crit'][2]>=5 else 0
  raw=atk['normal_damage']+maxcrit
  estimated=max(0,raw-PROFILE['F1']['rd']) if atk['score']>fr['ca'] or maxcrit else 0
  if estimated>=fr['hp']:raise ValueError('PULSO_CANNOT_RESURRECT_POST_LETHAL_AOO')
  n=st['ability_nonce']['E_PULSO']+1
  if p.get('pulse_dice')!=dice(st,'E','PULSO',n,3,10):raise ValueError('PULSO_TAPE')
 elif kind=='MOVE_A':
  if a!='A' or r['position']!='B0' or r['movement']!=1 or p!={'from':'B0','to':'B1','path':['B0','B1']}:
   raise ValueError('MOVE_A_NOT_LEGAL')
  if st['actors']['F1']['resource']['position']!='B2':raise ValueError('MOVE_A_NOT_REQUIRED')
 elif kind=='END':
  if p!={'actor':a} or r['standard']!=0:raise ValueError('END_WRONG')
 else:raise ValueError('UNKNOWN_ACTION_TYPE')

def source_attack(st,who,target,origin='NORMAL'):
 return source_state(st,who,target,'AOO' if origin=='OPPORTUNITY' else 'ATTACK')

def native_attack(scene,st,tape,reaction='NONE',origin='NORMAL'):
 a=tape['actor'];t=tape['target'];events=[];defence=None
 if reaction=='CAPA':
  ss,act,pro=source_state(st,t,a,'CAPA')
  defence=apply_capa_poeira(scene,t,a,source=ss,state=act,proofs=pro,attack_score=tape['score']);events.append(defence)
 ss,act,pro=source_attack(st,a,t,origin)
 pp=PROFILE[a];tp=PROFILE[t]
 ev=apply_weapon_attack(scene,a,t,source=ss,state=act,proofs=pro,
  roll_score=tape['score'],damage=tape['normal_damage'],damage_tag='perfurante',
  rd=Resistances(general=tp['rd'],provenance='DOCUMENTED_PHYSICAL_TARGET'),
  defense_event=defence,damage_dice_groups=tuple(map(tuple,pp['damage_dice'])),
  damage_roll_groups=tuple(map(tuple,tape['dmg_rolls'])),damage_fixed_bonus=pp['damage_flat'],
  critical_sequence=tuple(tape['crit']),attack_roll_attempts=tuple(map(tuple,tape['hit_rolls'])),
  attack_bonus=pp['attack_flat'],advantage_levels=tape['adv'],disadvantage_levels=tape['dis'],
  attack_origin=origin)
 events.append(ev);st['action_nonce'][a]+=1
 return events

def move_event(scene,st,who,to,path):
 spec,act,pro=source_state(st,who,None,'MOVE')
 # This cost is ONLY a verified topological edge, not an implicit 1-metre conversion.
 return move_via_verified_path(scene,who,source=spec,state=act,proofs=pro,destination=to,
  path_evidence='R138_TOPOLOGICAL_EDGE_'+path[0]+'_'+path[-1]+'_NONMETRIC',
  travel_cost=Fraction(1),speed=Fraction(1))

def command(db,kind,payload,failpoint=None):
 st,head,rev=core.load(db);verify(st,kind,payload)
 cmd='LAB-CMD-R138-'+core.sha({'run':st['run_id'],'revision':rev,'kind':kind,'payload':payload})[:38]
 def reducer(c,p,seq):
  sc=Scene({a:Combatant(**v['resource']) for a,v in c['actors'].items()},seed=c['seed'],
     provenance='R138_MASTER_SIDE_TECHNICAL_PRECREATION_V081_NOT_OFFICIAL')
  ev=[];extra={};a=c['active']
  if kind=='INIT':
   rows,tie=initiative(c);c['order']=tie['order'];c['active']=c['order'][0];c['phase']='ACTIVE';c['round']=1
   extra={'initiative_rows':rows,'tie':tie}
  elif kind=='START':
   ev.append(begin_source_turn(sc,a));c['actor_turns'][a]+=1
   if a=='F1' and c['marks']:
    m=c['marks']['F1'];m['own_turn_started_since_cast']+=1
    if m['own_turn_started_since_cast']>=3:m['expiry_boundary']='HOLD_EXACT_3_TURNS'
  elif kind=='FOREGO':
   sc.actors[a].standard=0;ev.append(sc.record({'action':'FOREGO_STANDARD','by':a,'no_benefit_claimed':True}))
  elif kind=='ATTACK':ev+=native_attack(sc,c,p['attack'],p.get('reaction','NONE'))
  elif kind=='MARCA':
   ss,act,pro=source_state(c,'F1','A','MARCA')
   ev.append(apply_marca_passos(sc,'F1','A',source=ss,state=act,proofs=pro,range_met=True,los_met=True))
   c['marks']['F1']={'target':'A','duration_literal':'3 TURNOS','activation_round':c['round'],
    'own_turn_started_since_cast':0,'source':FERYN,'bonus':'PERCEPTION_SURVIVAL_ONLY_10',
    'expiry_boundary':'HOLD_NO_UNIVERSAL_TURN_RULE','no_attack_bonus':True}
  elif kind=='PASSO':
   ss,act,pro=source_state(c,'F1','F1','PASSO')
   ev.append(apply_passo_fuligem(sc,'F1',source=ss,state=act,proofs=pro))
   c['temporary']['F1']={'source':FERYN,'kind':'PASSO_FULIGEM','bonus_speed_m':12,
    'expires_at':'END_CURRENT_F1_TURN','activated_own_turn':c['actor_turns']['F1']}
  elif kind=='HEAL':
   ss,act,pro=source_state(c,'E','F1','HEAL')
   ev.append(apply_reconstituicao_seiva(sc,'E','F1',source=ss,state=act,proofs=pro,
    dice_rolls=tuple(p['dice']),range_met=True,gloves_equipped=True))
   c['ability_nonce']['E_HEAL']+=1
  elif kind=='MOVE_F_AOO_PULSO':
   ev+=native_attack(sc,c,p['attack'],origin='OPPORTUNITY')
   assert sc.actors['F1'].hp>0
   ss,act,pro=source_state(c,'E','F1','PULSO')
   pulse=apply_pulso_estabilizacao(sc,'E','F1',source=ss,state=act,proofs=pro,
     dice_rolls=tuple(p['pulse_dice']),range_met=True,damage_just_resolved=True,gloves_equipped=True)
   ev.append(pulse);c['ability_nonce']['E_PULSO']+=1
   ev.append(move_event(sc,c,'F1','B2',['B1','B2']))
  elif kind=='MOVE_A':ev.append(move_event(sc,c,'A','B1',['B0','B1']))
  elif kind=='END':
   ev.append(end_source_turn(sc,a))
   if a in c['temporary']:
    temp=c['temporary'].pop(a)
    ev.append(sc.record({'action':'EXPIRE_TURN_EFFECT','by':a,'effect':temp['kind'],
     'effect_source':temp['source'],'expires_at':'END_CURRENT_OWN_TURN',
     'bonus_speed_removed_m':temp['bonus_speed_m']}))
   k=c['order'].index(a);c['turn_index']+=1
   for offset in range(1,len(c['order'])+1):
    j=(k+offset)%len(c['order']);who=c['order'][j]
    if sc.actors[who].hp>0:
     c['active']=who
     if j<=k:c['round']+=1
     break
   else:c['phase']='CENSORED_NO_LIVING';c['active']=None
   if c['round']>c['pre_registered_horizon']:
    c['phase']='CENSORED_HORIZON';c['active']=None;c['winner']=None
  for who,x in sc.actors.items():
   rr=asdict(x);rr['ca']=int(rr['ca']);rr['base_speed']=int(rr['base_speed']) if rr['base_speed'] is not None else None
   c['actors'][who]['resource']=rr
  return {'lineage':'R18_R26_V081_CONTROLLED_ADD_R138','action':kind,
   'native_actions':ev,'extra':extra,'selected_scope':'MULTIRROUND_INTEGRATION_MASTER_TECHNICAL',
   'contracts':['TURN_SCHEDULER_EVENT_SOURCING','BLEED_AND_HEAL_RESTRICTIONS','ACTION_CATALOG_AIN01',
    'PA_AND_PREBUFF_COSTS','REACTION_TRIGGER_AND_SINGLE_USE','ITEM_EQUIPMENT_AND_ENHANCEMENTS']}
 return core.event_commit(db,cmd,kind,payload,reducer,failpoint=failpoint)

def run(seed=991401):
 freeze();item=next(x for x in PREREG['runs'] if x['seed']==seed)
 db=ROOT/'runs'/(item['id']+'.sqlite');init(db,seed)
 command(db,'INIT',{'seed':seed});cmds=[];stop=None
 while True:
  st,_,rev=core.load(db)
  if st['phase']!='ACTIVE':break
  if rev>90:raise ValueError('SAFETY_MAX_90')
  who=st['active'];rd=st['round']
  command(db,'START',{'actor':who});cmds.append((rd,who,'START'))
  st,_,_=core.load(db)
  if who=='A':
   if rd==1:
    tape=attack_tape(st,'A','F1',dis=1)
    if badcrit(tape):stop='CRIT_NEGATIVE_PRE_INTENT';break
    command(db,'ATTACK',{'attack':tape,'reaction':'CAPA'});cmds.append((rd,who,'ATTACK_CAPA'))
   elif rd in (2,3):
    command(db,'FOREGO',{'actor':'A'});cmds.append((rd,who,'FOREGO'))
   elif rd==4:
    command(db,'MOVE_A',{'from':'B0','to':'B1','path':['B0','B1']});cmds.append((rd,who,'MOVE_A'))
    st,_,_=core.load(db)
    tape=attack_tape(st,'A','F1')
    if badcrit(tape):stop='CRIT_NEGATIVE_PRE_INTENT';break
    command(db,'ATTACK',{'attack':tape,'reaction':'NONE'});cmds.append((rd,who,'ATTACK_F'))
  elif who=='F1':
   if rd==1:
    command(db,'MARCA',{'target':'A','distance_m':1.5,'line_of_sight':True});cmds.append((rd,who,'MARCA'))
   elif rd==2:
    command(db,'PASSO',{'actor':'F1','intent':'THIS_TURN_ONLY'});cmds.append((rd,who,'PASSO'))
    command(db,'FOREGO',{'actor':'F1'});cmds.append((rd,who,'FOREGO'))
   elif rd==3:
    tape=attack_tape(st,'A','F1',kind='AOO',adv=1)
    if badcrit(tape):stop='AOO_CRITICAL_FAILURE_PRE_INTENT';break
    n=st['ability_nonce']['E_PULSO']+1
    payload={'attack':tape,'path':['B1','B2'],'forced':False,'pulse_distance_m':2,
     'pulse_dice':dice(st,'E','PULSO',n,3,10)}
    try:command(db,'MOVE_F_AOO_PULSO',payload)
    except ValueError as e:stop='SOURCE_HOLD_'+str(e);break
    cmds.append((rd,who,'MOVE_AOO_PULSO'))
    command(db,'FOREGO',{'actor':'F1'});cmds.append((rd,who,'FOREGO'))
   else:
    command(db,'FOREGO',{'actor':'F1'});cmds.append((rd,who,'FOREGO'))
  elif who=='E':
   st,_,_=core.load(db)
   if st['actors']['F1']['resource']['hp']>0 and st['actors']['F1']['resource']['hp']<479:
    n=st['ability_nonce']['E_HEAL']+1
    payload={'target':'F1','distance_m':3 if rd<3 else 2,
     'dice':dice(st,'E','HEAL',n,8,10)}
    command(db,'HEAL',payload);cmds.append((rd,who,'HEAL'))
   else:
    command(db,'FOREGO',{'actor':'E'});cmds.append((rd,who,'FOREGO'))
  command(db,'END',{'actor':who});cmds.append((rd,who,'END'))
 st,head,rev=core.load(db)
 cp=db.with_suffix('.checkpoint.sqlite')
 with sqlite3.connect(db) as src,sqlite3.connect(cp) as dst:src.backup(dst)
 assert core.load(db)==core.load(cp)
 with sqlite3.connect(db) as con:
  rows=[json.loads(x[0]) for x in con.execute('SELECT row_json FROM events ORDER BY seq')]
 records=[act for row in rows for act in row['detail']['native_actions']]
 stats={'run_id':st['run_id'],'seed':seed,'revision':rev,'phase':st['phase'],'stop':stop,
  'round':st['round'],'event_count':len(rows),'native_events':len(records),
  'actions':{k:sum(x['action']==k for x in records) for k in set(x['action'] for x in records)},
  'PA_spent':sum(x.get('PA_spent',0) for x in records),
  'healed':sum(x.get('actual_healed',x.get('actual_heal',0)) for x in records),
  'actual_HP_lost':sum(x.get('hp_loss_actual',0) for x in records),
  'end_HP':{a:v['resource']['hp'] for a,v in st['actors'].items()},
  'end_PA':{a:v['resource']['pa'] for a,v in st['actors'].items()},
  'end_positions':{a:v['resource']['position'] for a,v in st['actors'].items()},
  'marks':st['marks'],'temp':st['temporary'],'head':head,'cmds':cmds,
  'checkpoint_equal':True,'official_power_cells':0,'terminal_certificates':0,
  'not_win_if_censored':st['phase'].startswith('CENSORED')}
 (ROOT/'R138_EXECUTION.json').write_text(can(stats))
 return stats
if __name__=='__main__':print(can(run()))
