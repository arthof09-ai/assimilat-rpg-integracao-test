"""VLAB R119 controlled continuation of R117: v0.8.1 effects + R18 commit + R26 tie rules.
Not an official team or new RPG rule; two instances of documented Feryn are technical copies.
"""
from __future__ import annotations
import sys, json, hashlib, sqlite3, copy
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).resolve().parent
NATIVE=ROOT/'native_v081_controlled'
STAGE12=ROOT.parent/'r61_extracted'/'work'/'fusion_stage12'
sys.path.insert(0,str(NATIVE));sys.path.insert(1,str(STAGE12))
import vlab_r18_interactive as core
import vlab_r26_master_rulings as r26
sys.modules.pop('vlab_effects_v08',None);sys.path.insert(0,str(NATIVE))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,
    begin_source_turn,end_source_turn,react_defensively,declare_counterattack,
    execute_declared_counterattack,apply_weapon_attack,EffectBlocked,weak_status)
from vlab_rd_v08 import Resistances

COMBAT='3ebc2b324ede81f1be4b-e8804ac113c0'
AUREN='3ebc2b324ede814bb730d47dd7bd5f02'
FERYN='3f6c2b324ede81ce9c61db8127bf0e31'
PROFILES={
 'A':dict(source=AUREN, rank='Lendário', rank_index=23,init_dice=6,init_bonus=166,dex=164,
  hp=523,pa=719,ca=225,con=48,armor=24,fort=2,reflex=2,rd=35,speed=64,
  attack_dice=6,attack_flat=193,damage_dice=((8,8),),damage_flat=211),
 'F1':dict(source=FERYN,rank='Ouro Negro',rank_index=20,init_dice=4,init_bonus=82,dex=80,
  hp=479,pa=424,ca=123,con=24,armor=26,fort=0,reflex=2,rd=22,speed=40,
  attack_dice=4,attack_flat=92,damage_dice=((8,8),),damage_flat=47),
 'F2':dict(source=FERYN,rank='Ouro Negro',rank_index=20,init_dice=4,init_bonus=82,dex=80,
  hp=479,pa=424,ca=123,con=24,armor=26,fort=0,reflex=2,rd=22,speed=40,
  attack_dice=4,attack_flat=92,damage_dice=((8,8),),damage_flat=47)}
TEAM_MAP={'A':'ONE','F1':'TWO','F2':'TWO'}
AUTH={'CombatRule':COMBAT,'R50_R51':'3f3c2b324ede819496ddd7f93bd7e5d2',
 'R26':'MESTRE-INIT-20261014-DES-THEN-REROLL-ONLY-TIED',
 'Auren':AUREN,'Feryn':FERYN}
PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R118-R125','baseline':'R01-R117 IMMUTABLE',
 'source_authority':AUTH,'engine':'R117 patched original v0.8.1 copied and additively extended; R18 SQLite/R26 tie_order reused',
 'rng':'R18 deterministic SHA dice experimental, not official dice','scenarios':[
 {'name':'THREE_ACTOR_DEV','seed':918201,'validation_family':'development','initial_hp':'SOURCE_FULL',
  'actors':['A','F1','F2'],'teams':{'A':'one','F1':'two','F2':'two'},'max_actions':24},
 {'name':'THREE_ACTOR_RESERVED','seed':928801,'validation_family':'reserved-not-certified-blind','initial_hp':'SOURCE_FULL',
  'actors':['A','F1','F2'],'teams':{'A':'one','F1':'two','F2':'two'},'max_actions':24}],
 'policies':{'A':'Attack F1 then F2; COUNTER against F1/F2 only if reaction available',
  'F1':'ESQUIVAR incoming normal if slot available; basic against A',
  'F2':'DEFENDER incoming normal if slot available; basic against A',
  'initiative':'natural each actor source dice + DES + prof, Mestre R26 tie DES then reroll only tied',
  'reaction':'declared before normal attack; R50 counter only on effective miss; R51 counter cannot trigger counter',
  'turn_refresh':'reaction exactly one at OWN TURN START even if previous spent',
  'death':'technical HP0 removes actor from future turns; scene stops at one faction alive',
  'movement':'not used; terrain/LoS technical source path only; no official geometry claim'},
 'limitations':['F1 F2 same source cloned as technical actor instances only, not real NPC multiplicity',
  'no team-equivalence claim','no Beast natural initiative','no full effects, spells, positional adjudication',
  'risk of critical failure consequence unresolved -> stop before intent','no blind holdout certification',
  'R50/R51 direct Mestre sourced from existing OP but no general rule rewrite'],
 'no_repeat':['R93','R95','R103','R112','R115','R117'],
 'terminal_certificates':0}

class Hold(RuntimeError): pass
def freeze():
 p=ROOT/'R119_PREREG_REACTIONS_SCHEDULER.json'
 if p.exists():
  assert json.loads(p.read_text())==PREREG,'PREREG_MISMATCH'
 else:p.write_text(json.dumps(PREREG,indent=2,ensure_ascii=False)+'\n')
 return p

def rolls(seed,turn,actor,kind,n,faces):
 return core.dice(seed,turn,f'R119-{actor}-{kind}',n,faces)

def snapshot(scene,seed):
 genesis=core.initial('A',seed)
 genesis.update({'scene':scene,'run_id':scene,'kind':'R119_INTEGRATED_TECHNICAL','stage':'R119',
  'phase':'INIT','order':[],'round':0,'turn_index':0,'active':None,'action_nonce':{a:0 for a in PROFILES},
  'actor_turns':{a:0 for a in PROFILES},'winner':None,'defeated':[],'source_fingerprint':core.sha(AUTH),
  'prereg_hash':hashlib.sha256((ROOT/'R119_PREREG_REACTIONS_SCHEDULER.json').read_bytes()).hexdigest(),
  'teams':TEAM_MAP.copy(),'technical_instancing':True,'no_canonical_credit':True})
 genesis['actors']={}
 for aid,p in PROFILES.items():
  c=Combatant(aid,p['hp'],p['pa'],p['ca'],p['con'],p['armor'],p['fort'],p['reflex'],
    f'TECHNICAL-{aid}',rank=p['rank'],standard=0,movement=0,reaction=1,
    maximum_hp=p['hp'],base_speed=p['speed'],beast_rank_index=None)
  genesis['actors'][aid]={'source':p['source'],'source_profile':p.copy(), 'resource':asdict(c)}
 return genesis

def init_db(file,seed):
 if file.exists():raise Hold('NO_RESTART_EXISTING_DB')
 core.init_db(file,'A',seed)
 st=snapshot(file.stem,seed)
 head=core.sha({'R119_genesis':st,'engine':'R18+R26+v081_REACTION_ADD'})
 with core.connect(file) as con:
  for k,v in [('scene',st['scene']),('genesis',head),('head',head),('state',core.canonical(st))]:
   con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 file.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')


def sc_from(st):
 return Scene({k:Combatant(**v['resource']) for k,v in st['actors'].items()},
   seed=st['seed'],provenance='TECHNICAL_INSTANCES_SOURCED_MASTER_ONLY')

def proof(page,rule):
 text=f'{page}|{rule}|direct Notion source reopened 2026-10-16|R119_SOURCE_AUTH'
 return (FrozenRuleEvidence(page,rule,hashlib.sha256(text.encode()).hexdigest(),
      '2026-10-16_NOTION_READ','R119_SOURCE_AUTH'),)

def src_state(st,actor,target,mode,phase='TURN'):
 p=PROFILES[actor]
 if mode=='BASIC':
  src=AbilitySource('R119-'+actor+'-BASIC','attack','STANDARD',p['source'],
   'SOURCED_NORMAL_ATTACK','RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,
   effect_adapter_id='V081_NATIVE_WEAPON')
 elif mode in ('ESQUIVAR','DEFENDER','COUNTER'):
  src=AbilitySource('R119-'+actor+'-'+mode,'reaction','REACTION',COMBAT,
   'R4-'+mode+'-R50-R51','RULE-DERIVED',target_scope='SELF',reaction_trigger='ATTACK_DECLARED',
   effect_adapter_ready=True,effect_adapter_id='V081_NATIVE_REACTION')
 else:raise Hold('INVALID_SOURCE_MODE')
 c=st['actors'][actor]['resource']
 state=ActorActionState(actor,p['rank_index'],c['pa'],(src.action_id,),
   standard_available=c['standard']==1,movement_available=c['movement']==1,
   reaction_available=c['reaction']==1,reaction_trigger_observed='ATTACK_DECLARED' if phase=='REACTION' else None,
   range_confirmed=True,los_confirmed=True,geometry_confirmed=True,
   enemy_ids_visible=(target,) if target else (),ally_ids_visible=())
 return src,state,proof(src.source_page_id,src.rule_id)

def atk_payload(st,actor,target):
 n=st['action_nonce'][actor]+1;seed=st['seed'];p=PROFILES[actor]
 crit=[rolls(seed,n,actor,f'NORMAL-CRIT-{j}',1,6)[0] for j in range(3)]
 is_weak=st['actors'][actor]['resource']['hp']*10 < p['hp']
 hits=[rolls(seed,n,actor,f'NORMAL-HIT-{i}',p['attack_dice'],6) for i in range(2 if is_weak else 1)]
 score=(min(map(sum,hits))-2 if is_weak else sum(hits[0]))+p['attack_flat']
 dmg=[rolls(seed,n,actor,f'NORMAL-DMG-{i}',count,face) for i,(count,face) in enumerate(p['damage_dice'])]
 return {'actor':actor,'target':target,'nonce':n,'crit':crit,'hit_rolls':hits,'score':score,
    'damage_rolls':dmg,'normal_damage':sum(map(sum,dmg))+p['damage_flat'],'damage_groups':p['damage_dice'],
    'flat':p['damage_flat'],'bonus':p['attack_flat'],'is_weak':is_weak}

def counter_payload(st,defender,attacker):
 nonce=st['action_nonce'][defender]+1;seed=st['seed'];p=PROFILES[defender]
 crit=[rolls(seed,nonce,defender,f'COUNTER-CRIT-{j}',1,6)[0] for j in range(3)]
 hits=[rolls(seed,nonce,defender,f'COUNTER-HIT-{i}',p['attack_dice'],6) for i in range(2)]
 dmg=[rolls(seed,nonce,defender,f'COUNTER-DMG-{i}',n,f) for i,(n,f) in enumerate(p['damage_dice'])]
 return {'actor':defender,'target':attacker,'nonce':nonce,'crit':crit,'hit_rolls':hits,
  'dmg_rolls':dmg,'damage_groups':p['damage_dice'],'flat':p['damage_flat'],'bonus':p['attack_flat']}

def normalize_event(ev):
 return dict(ev)

def attack_preflight(st,payload):
 if st['phase']!='ACTIVE':raise Hold('NOT_ACTIVE')
 actor=st['active'];target=payload['attack']['target']
 if payload['attack']['actor']!=actor or st['actors'][actor]['resource']['hp']<=0:
  raise Hold('ACTIVE_ACTOR_INVALID')
 if target not in st['actors'] or st['teams'][target]==st['teams'][actor] or st['actors'][target]['resource']['hp']<=0:
  raise Hold('NO_ALIVE_ENEMY_TARGET')
 if st['actors'][actor]['resource']['standard']!=1:raise Hold('STANDARD_SLOT_ABSENT_PRE_INTENT')
 atk=atk_payload(st,actor,target)
 if atk!=payload['attack']:raise Hold('ATTACK_TAPE_CHANGED_BEFORE_INTENT')
 c=atk['crit']
 if c[:2]==[1,1] and c[2]<=2:raise Hold('CRITICAL_FAILURE_UNRESOLVED_PRE_INTENT')
 policy=payload.get('reaction')
 if policy not in ('NONE','DEFENDER','ESQUIVAR','COUNTER'):raise Hold('UNKNOWN_REACTION')
 defender=st['actors'][target]['resource']
 if policy!='NONE':
  if defender['reaction']!=1:raise Hold('NO_REACTION_SLOT_PRE_INTENT')
  if payload.get('attack_origin','NORMAL')!='NORMAL':raise Hold('R51_NESTED_COUNTER_NO_INTENT')
  if policy=='COUNTER' and defender['hp']*10 < PROFILES[target]['hp']:
   raise Hold('WEAK_COUNTER_ADVANTAGE_UNRESOLVED_PRE_INTENT')
  src_state(st,target,actor,policy,'REACTION')
  if policy=='COUNTER':
   ctr=counter_payload(st,target,actor)
   if ctr!=payload.get('counter'):raise Hold('COUNTER_TAPE_CHANGED')
   if ctr['crit'][:2]==[1,1] and ctr['crit'][2]<=2:raise Hold('COUNTER_CRITICAL_FAILURE_PRE_INTENT')
 elif 'counter' in payload:raise Hold('COUNTER_WITHOUT_DECLARATION')
 return actor,target

def choose_target(st,actor):
 if actor=='A':return 'F1' if st['actors']['F1']['resource']['hp']>0 else 'F2'
 return 'A'

def choose_reaction(st,actor,target):
 if st['actors'][target]['resource']['reaction']<1:return 'NONE'
 if target=='A':return 'COUNTER'
 return 'ESQUIVAR' if target=='F1' else 'DEFENDER'

def command(db,kind,payload,failpoint=None):
 st,head,rev=core.load(db)
 if kind=='INIT':
  if st['phase']!='INIT' or payload!={'seed':st['seed']}:raise Hold('INIT_PREFAIL')
 elif kind=='START':
  if st['phase']!='ACTIVE' or payload!={'actor':st['active']} or st['actors'][st['active']]['resource']['hp']<=0 or st['actors'][st['active']]['resource']['standard']!=0:
   raise Hold('TURN_START_PREFAIL')
 elif kind=='STRIKE':attack_preflight(st,payload)
 elif kind=='END':
  if st['phase']!='ACTIVE' or payload!={'actor':st['active']} or st['actors'][st['active']]['resource']['standard']!=0:
   raise Hold('TURN_END_PREFAIL')
 else:raise Hold('KIND_NOT_ALLOWED')
 cmd='LAB-CMD-R119-'+core.sha({'run':st['run_id'],'revision':rev,'type':kind,'payload':payload})[:38]
 def runner(candidate,p,seq):
  sc=sc_from(candidate);native=[];extra={};a=candidate.get('active')
  if kind=='INIT':
   rows=[]
   for aid in PROFILES:
    info=PROFILES[aid];d=rolls(candidate['seed'],0,aid,'INIT',info['init_dice'],6)
    rows.append({'id':aid,'total':sum(d)+info['init_bonus'],'dice':d,'des':info['dex'],'prof_applied':2,'source':info['source']})
   def reroll(aid,n):
    info=PROFILES[aid]
    return sum(rolls(candidate['seed'],n,aid,'INIT-TIE',info['init_dice'],6))+info['init_bonus']
   t=r26.tie_order(rows,reroll)
   candidate['order']=t['order'];candidate['active']=t['order'][0];candidate['phase']='ACTIVE';candidate['round']=1
   extra={'initiative':rows,'tie_resolution':t}
  elif kind=='START':
   ev=begin_source_turn(sc,a);native.append(normalize_event(ev))
   candidate['actor_turns'][a]+=1
  elif kind=='STRIKE':
   attacker,target=a,p['attack']['target'];tape=p['attack']
   reaction=p['reaction'];react_event=None
   if reaction in ('DEFENDER','ESQUIVAR'):
    src,state,pr=src_state(candidate,target,attacker,reaction,'REACTION')
    react_event=react_defensively(sc,target,kind=reaction,attack_score=tape['score'],
     announced_before=True,trigger_source='ATTACK_DECLARED',source=src,state=state,proofs=pr)
    native.append(normalize_event(react_event))
   elif reaction=='COUNTER':
    src,state,pr=src_state(candidate,target,attacker,'COUNTER','REACTION')
    react_event=declare_counterattack(sc,target,attacker,source=src,state=state,proofs=pr,
      declared_before=True,attack_origin='NORMAL')
    native.append(normalize_event(react_event))
   src,state,pr=src_state(candidate,attacker,target,'BASIC')
   basic=apply_weapon_attack(sc,attacker,target,source=src,state=state,proofs=pr,
      roll_score=tape['score'],damage=tape['normal_damage'],damage_tag='perfurante',
      rd=Resistances(general=PROFILES[target]['rd'],provenance='SOURCE_PHYSICAL_ONLY'),
      defense_event=react_event if reaction in ('DEFENDER','ESQUIVAR') else None,
      damage_dice_groups=tuple(map(tuple,tape['damage_groups'])),
      damage_roll_groups=tuple(map(tuple,tape['damage_rolls'])),
      damage_fixed_bonus=tape['flat'],critical_sequence=tuple(tape['crit']),
      attack_roll_attempts=tuple(map(tuple,tape['hit_rolls'])),attack_bonus=tape['bonus'])
   native.append(normalize_event(basic));candidate['action_nonce'][attacker]+=1
   if reaction=='COUNTER':
    c=p['counter']
    res=execute_declared_counterattack(sc,target,attacker,declaration=react_event,incoming=basic,
      attack_attempts=tuple(map(tuple,c['hit_rolls'])),attack_bonus=c['bonus'],
      critical_sequence=tuple(c['crit']),damage_groups=tuple(map(tuple,c['damage_groups'])),
      damage_roll_groups=tuple(map(tuple,c['dmg_rolls'])),flat=c['flat'],damage_tag='perfurante',
      rd=Resistances(general=PROFILES[attacker]['rd'],provenance='SOURCE_PHYSICAL_ONLY'))
    native.append(normalize_event(res))
    if res['action']=='COUNTER_RESPONSE':candidate['action_nonce'][target]+=1
   extra={'original_actor':attacker,'declared_reaction':reaction,'origin':'NORMAL','R50_R51':True}
  elif kind=='END':
   ev=end_source_turn(sc,a);native.append(normalize_event(ev))
   current=candidate['order'].index(a);candidate['turn_index']+=1
   if all(candidate['actors'][aid]['resource']['hp']<=0 for aid in candidate['actors'] if candidate['teams'][aid]=='ONE'):
    candidate['phase']='FINISHED';candidate['winner']='TWO';candidate['active']=None
   elif all(candidate['actors'][aid]['resource']['hp']<=0 for aid in candidate['actors'] if candidate['teams'][aid]=='TWO'):
    candidate['phase']='FINISHED';candidate['winner']='ONE';candidate['active']=None
   else:
    for offset in range(1,len(candidate['order'])+1):
     ix=(current+offset)%len(candidate['order']);potential=candidate['order'][ix]
     if sc.actors[potential].hp>0:
      candidate['active']=potential
      if ix<=current:candidate['round']+=1
      break
    else:raise Hold('NO_ALIVE_ACTOR')
   extra={'next_actor':candidate['active'],'round_after':candidate['round'],'skipped_KO':[
    k for k,v in candidate['actors'].items() if sc.actors[k].hp<=0]}
  for aid,obj in sc.actors.items():
   r=asdict(obj)
   r['ca']=int(r['ca']);r['base_speed']=int(r['base_speed'])
   candidate['actors'][aid]['resource']=r
  return {'engine':'R117_NATIVE_V081_COPY+R118_REACTIONS','native_actions':native,
          'source_rulings':AUTH,'counter_R50_R51':True,'extra':extra,'command':kind,
          'scope':'LAB_TECHNICAL_NONCANON'}
 return core.event_commit(db,cmd,kind,payload,runner,failpoint=failpoint)

def one(seed,name,max_actions=24):
 file=ROOT/'runs'/f'R119_{name}_{seed}.sqlite'
 init_db(file,seed)
 command(file,'INIT',{'seed':seed})
 ran=0;censor=None
 while ran<max_actions:
  st,_,_=core.load(file)
  if st['phase']!='ACTIVE':break
  a=st['active'];command(file,'START',{'actor':a})
  st,_,_=core.load(file);target=choose_target(st,a)
  attack=atk_payload(st,a,target);reaction=choose_reaction(st,a,target)
  payload={'attack':attack,'reaction':reaction,'attack_origin':'NORMAL'}
  if reaction=='COUNTER':payload['counter']=counter_payload(st,target,a)
  try:command(file,'STRIKE',payload)
  except Hold as ex:
   if 'CRITICAL_FAILURE_UNRESOLVED_PRE_INTENT' in str(ex) or 'COUNTER_CRITICAL_FAILURE_PRE_INTENT' in str(ex):
    censor=str(ex);break
   raise
  command(file,'END',{'actor':a});ran+=1
 st,head,rev=core.load(file)
 checkpoint=file.with_suffix('.checkpoint.sqlite')
 with sqlite3.connect(file) as source,sqlite3.connect(checkpoint) as out:source.backup(out)
 assert core.load(file)==core.load(checkpoint)
 with sqlite3.connect(file) as con:evs=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
 count={kind:sum(kind==v['kind'] for v in evs) for kind in ('INIT','START','STRIKE','END')}
 actions=[y for ev in evs for y in ev['detail']['native_actions']]
 return {'run_id':st['run_id'],'seed':seed,'family':name,'phase':st['phase'] if censor is None else 'CENSORED_PRE_INTENT',
  'censor_reason':censor,'winner':st['winner'],'round':st['round'],'turn_index':st['turn_index'],
  'order':st['order'],'head':head,'revision':rev,'event_kinds':count,
  'reaction_declared':sum(v['action'] in ('ESQUIVAR','DEFENDER','COUNTER_DECLARE') for v in actions),
  'counterresponses':sum(v['action']=='COUNTER_RESPONSE' for v in actions),
  'counter_skipped_hit':sum(v['action']=='COUNTER_NO_RESPONSE' for v in actions),
  'attack_events':sum(v['action']=='weapon_attack' for v in actions),
  'KO':st['defeated'] if st['defeated'] else [a for a in PROFILES if st['actors'][a]['resource']['hp']==0],
  'hp_final':{a:st['actors'][a]['resource']['hp'] for a in PROFILES},
  'reaction_final':{a:st['actors'][a]['resource']['reaction'] for a in PROFILES},
  'file':file.name,'checkpoint_file':checkpoint.name,'official':False}

if __name__=='__main__':
 freeze();results=[one(x['seed'],x['name'],x['max_actions']) for x in PREREG['scenarios']]
 (ROOT/'R119_EXECUTIONS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(results,indent=2,ensure_ascii=False))
