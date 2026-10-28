"""Controlled extension of the original v0.8.1+R18+R26 lineage, NOT another engine.
R126: 3 actor single-scene source-backed Capa de Poeira (35 PA reaction),
Marca dos Passos Perdidos (25 PA standard), and adjacency AoO with advantage.
ALL states experimental. No canonical changes; no legacy DB is reopened for execution.
"""
import copy,hashlib,json,sqlite3,sys
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r126_shared_three_actor as base
from r126_shared_three_actor import core,r26,Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState
from r126_shared_three_actor import begin_source_turn,end_source_turn,declare_counterattack,execute_declared_counterattack
from vlab_effects_v08 import apply_weapon_attack,apply_capa_poeira,apply_marca_passos,move_via_verified_path,EffectBlocked
from vlab_rd_v08 import Resistances
P=base.PROFILES; COMBAT=base.COMBAT; FERYN=base.FERYN
TOPOLOGY={'B0':['B1'],'B1':['B0','B2'],'B2':['B1','B3'],'B3':['B2']}
SOURCE={
 'CAPA':{'page':FERYN,'excerpt':'Capa de Poeira — 35 PA • Reação. Um ataque físico anunciado contra si. Aplica uma Desvantagem ao teste inimigo; magia sem ataque não é afetada.'},
 'MARCA':{'page':FERYN,'excerpt':'Marca dos Passos Perdidos — 25 PA • Padrão. Um alvo que veja até 30 m. Duração 3 turnos; +10 Percepção e Sobrevivência para localizar pistas, sem revelar posição através de paredes.'},
 'AOO':{'page':COMBAT,'excerpt':'Regra 3: ao sair de um bloco adjacente ao inimigo, Ataque de Oportunidade com Vantagem consome Reação. Afastar-se com segurança: Ação Padrão contra 1 inimigo e Movimento.'},
 'RULES':{'page':COMBAT,'excerpt':'Regra 5: Vantagem e Desvantagem acumulam níveis até 4; cada nível dá uma rolagem extra e bonus/penalidade 2. Regra 6 crítico sequencial.'}}
PREREG={'stage':'R126-R132','baseline':'R01-R125 preserved','date':'2026-10-16',
 'operation':'OP-VLAB-FUSION-SANDBOX-01', 'seed_development':943207,'seed_reserved_not_blind':953209,
 'source':SOURCE,'topology':'one-dimensional abstract B0-B1-B2-B3 blocks, no metric length inference',
 'actors':['A: Auren source original','F1: Feryn technical instance','F2: Feryn technical instance'],
 'policies':['A on turn1 normal attacks F1, F1 Capa as paid REACTION if legal',
  'F1 on turn1 Marca A 25PA, after STANDARD attempt B1->B2, AoO A if available',
  'F2 normal attacks A; A counters only if reaction available',
  'AoO result computed prior to completing movement; KO aborts displacement',
  'movement forced never eligible; safe retreat cancels one named adjacent attacker'],
 'preconditions':['Feryn experimental source fiche is Master-side proposed encounter, not existing campaign combat',
  'A+2xFeryn technical instancing, not balanced two ED party','R18 SQLite WAL','R26 init DES ties',
  'No AoO simultaneous priority delegated or invented','no R123 unknown replays'],
 'scientific':['NO HOLDOUT blind certified','not complete balanced match','Feryn H ability proposed, not canonized source','Marca expiry exact boundary pending, only effect storage proven'],
 'NO_REPEAT':['R01–R125 historical','R123_FRESH_AFTER_INTENT_939906','R124_5X5_CENSORED']}
class Hold(RuntimeError):pass

def _json(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
def register_prereg():
 p=ROOT/'R126_PREREG.json';b=_json(PREREG)
 if p.exists():assert p.read_text()==b
 else:p.write_text(b)
 return p

def proof(page,rule):
 excerpt=SOURCE[rule]['excerpt'] if rule in SOURCE else SOURCE['RULES']['excerpt']
 return (FrozenRuleEvidence(page,rule,hashlib.sha256(excerpt.encode()).hexdigest(),
 '2026-10-16_SOURCED_NOTION','R126_READ_ONLY_VERIFIED_SOURCE'),)

def src(st,actor,target,kind):
 p=P[actor];r=st['actors'][actor]['resource'];phase='TURN';trigger=None;typ='attack';economy='STANDARD';cost=0
 if kind=='CAPA':
  typ='reaction';economy='REACTION';cost=35;trigger='ATTACK_DECLARED';scope='SELF';page=FERYN
 elif kind=='MARCA':
  typ='control';economy='STANDARD';cost=25;scope='ENEMY';page=FERYN
 elif kind=='AOO':
  typ='attack';economy='REACTION';trigger='EXIT_ADJACENT';scope='ENEMY';page=COMBAT
 else:
  typ='attack';economy='STANDARD';scope='ENEMY';page=p['source']
 action=f'R126-{actor}-{kind}'
 source=AbilitySource(action,typ,economy,page,kind if kind in SOURCE else 'RULES','RULE-DERIVED',
 required_pa=cost,target_scope=scope,reaction_trigger=trigger,effect_adapter_ready=True,
 effect_adapter_id='V081_R126_NATIVE_CONTROLLED')
 state=ActorActionState(actor,p['rank_index'],r['pa'],(action,),
 standard_available=r['standard']==1,movement_available=r['movement']==1,
 reaction_available=r['reaction']==1,reaction_trigger_observed=trigger,
 range_confirmed=True,los_confirmed=True,geometry_confirmed=True,
 enemy_ids_visible=(target,) if target else (),ally_ids_visible=())
 return source,state,proof(page,kind if kind in SOURCE else 'RULES')

def move_source(st,actor):
 r=st['actors'][actor]['resource'];page=COMBAT
 source=AbilitySource('R126-'+actor+'-MOVEMENT','move','MOVEMENT',page,'AOO','RULE-DERIVED',
 target_scope='NONE',effect_adapter_ready=True,effect_adapter_id='V081_NATIVE_MOVE')
 state=ActorActionState(actor,P[actor]['rank_index'],r['pa'],(source.action_id,),
  standard_available=r['standard']==1,movement_available=r['movement']==1,
  reaction_available=r['reaction']==1,range_confirmed=True,los_confirmed=True,geometry_confirmed=True)
 return source,state,proof(page,'AOO')

def draws(seed,nonce,actor,kind,n,faces):
 return core.dice(seed,nonce,'R126-'+actor+'-'+kind,n,faces)

def critical(seed,nonce,actor,kind):
 return [draws(seed,nonce,actor,kind+'-CRIT-'+str(j),1,6)[0] for j in range(3)]

def attack_tape(st,actor,target,kind='NORMAL',adv=0,dis=0):
 p=P[actor];nonce=st['action_nonce'][actor]+1;seed=st['seed'];r=st['actors'][actor]['resource']
 weak=10*r['hp']<p['hp'];net=max(-4,min(4,adv-dis-int(weak)))
 hits=[draws(seed,nonce,actor,kind+'-HIT-'+str(j),p['attack_dice'],6) for j in range(1+abs(net))]
 score=(max(map(sum,hits))+2*net if net>0 else min(map(sum,hits))+2*net if net<0 else sum(hits[0]))+p['attack_flat']
 dmg=[draws(seed,nonce,actor,kind+'-DAMAGE-'+str(j),n,f) for j,(n,f) in enumerate(p['damage_dice'])]
 return {'actor':actor,'target':target,'kind':kind,'nonce':nonce,'adv':adv,'dis':dis,'crit':critical(seed,nonce,actor,kind),
 'hit_rolls':hits,'score':score,'dmg_rolls':dmg,'normal_damage':sum(map(sum,dmg))+p['damage_flat'],
 'flat':p['damage_flat'],'bonus':p['attack_flat'],'damage_groups':p['damage_dice'],'weak':weak}

def seed_init(st):
 rows=[]
 for aid,p in P.items():
  dice=draws(st['seed'],0,aid,'INIT',p['init_dice'],6)
  rows.append({'id':aid,'dice':dice,'total':sum(dice)+p['init_bonus'],'des':p['dex'],'source':p['source']})
 def tie(aid,n):
  p=P[aid];return sum(draws(st['seed'],n,aid,'INIT-TIE',p['init_dice'],6))+p['init_bonus']
 return rows,r26.tie_order(rows,tie)

def sc_from(st):
 return Scene({k:Combatant(**v['resource']) for k,v in st['actors'].items()},seed=st['seed'],
 provenance='MESTRE_ONLY_PROPOSAL_TWO_FERYN_TECH_COPIES_NONCANON')

def genesis(run,seed):
 register_prereg()
 st=base.snapshot(run,seed);st.update({'run_id':run,'stage':'R126-R132',
  'prereg_hash':hashlib.sha256((ROOT/'R126_PREREG.json').read_bytes()).hexdigest(),
  'kind':'R126_NATIVE_REACTION_POSITION_PA_INTEGRATED','spatial_topology':TOPOLOGY,
  'marks':{},'mark_tracking_expiry_gate':'PENDING_SOURCE_TURN_BOUNDARY',
  'source_fingerprint':core.sha(SOURCE), 'policy':'PA_REACTION_AOO',
  'ability_events':0,'aoo_events':0,'technical_instancing':True,'no_canonical_credit':True})
 for aid,pos in {'A':'B0','F1':'B1','F2':'B3'}.items():st['actors'][aid]['resource']['position']=pos
 return st

def init(db,seed):
 if db.exists():raise Hold('NO_REUSE_DB')
 core.init_db(db,'A',seed);st=genesis(db.stem,seed)
 anchor=core.sha({'genesis':st,'lineage':'R18_R26_V081_R126'})
 with core.connect(db) as c:
  for key,value in [('scene',st['scene']),('genesis',anchor),('head',anchor),('state',core.canonical(st))]:
   c.execute('UPDATE meta SET value=? WHERE key=?',(value,key))
 db.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')

def _native_strike(sc,candidate,p):
 tape=p['attack'];actor=tape['actor'];target=tape['target'];rr=p['reaction'];native=[]
 react=None
 if rr=='CAPA':
  spec,state,proofs=src(candidate,target,actor,'CAPA')
  react=apply_capa_poeira(sc,target,actor,source=spec,state=state,proofs=proofs,
   attack_score=tape['score']);native.append(react)
 elif rr=='COUNTER':
  spec,state,proofs=src(candidate,target,actor,'COUNTER')
  react=declare_counterattack(sc,target,actor,source=spec,state=state,proofs=proofs,
   declared_before=True,attack_origin='NORMAL');native.append(react)
 else:assert rr=='NONE'
 spec,state,proofs=src(candidate,actor,target,'BASIC')
 ev=apply_weapon_attack(sc,actor,target,source=spec,state=state,proofs=proofs,
  roll_score=tape['score'],damage=tape['normal_damage'],damage_tag='perfurante',
  rd=Resistances(general=P[target]['rd'],provenance='DOCUMENTED_PHYSICAL'),
  defense_event=react if rr=='CAPA' else None,
  damage_dice_groups=tuple(map(tuple,tape['damage_groups'])),
  damage_roll_groups=tuple(map(tuple,tape['dmg_rolls'])),
  damage_fixed_bonus=tape['flat'],critical_sequence=tuple(tape['crit']),
  attack_roll_attempts=tuple(map(tuple,tape['hit_rolls'])),attack_bonus=tape['bonus'],
  disadvantage_levels=tape['dis'],advantage_levels=tape['adv'])
 native.append(ev);candidate['action_nonce'][actor]+=1
 # Optional R50 counterattack is already evidenced R125; do not rerun it to pad counts.
 return native

def verify_before(st,kind,p):
 if kind=='INIT':
  if st['phase']!='INIT' or p!={'seed':st['seed']}:raise Hold('INIT_PREFAIL')
 elif kind=='START':
  aid=p.get('actor');r=st['actors'].get(aid,{}).get('resource',{})
  if aid!=st['active'] or st['phase']!='ACTIVE' or r.get('hp',0)<=0 or r.get('standard')!=0:
   raise Hold('START_PREFAIL')
 elif kind=='STRIKE':
  aid=st['active'];t=p.get('attack',{});target=t.get('target');r=st['actors'][aid]['resource']
  if t.get('actor')!=aid or target not in st['actors'] or st['teams'][target]==st['teams'][aid] or r['standard']!=1 or st['actors'][target]['resource']['hp']<=0:
   raise Hold('STRIKE_ACTOR_TARGET_PREFAIL')
  reaction=p.get('reaction')
  if reaction not in ('NONE','CAPA'):raise Hold('REJECTION_UNSUPPORTED_REACTION')
  if reaction=='CAPA':
   defender=st['actors'][target]['resource']
   if target not in ('F1','F2') or defender['pa']<35 or defender['reaction']!=1:raise Hold('CAPA_RESOURCES_PREFAIL')
  pred=attack_tape(st,aid,target,adv=0,dis=int(reaction=='CAPA'))
  if core.canonical(t)!=core.canonical(pred):raise Hold('STRIKE_RNG_EVIDENCE_MISMATCH')
  if t['crit'][:2]==[1,1] and t['crit'][2]<=2:raise Hold('CRITICAL_FAILURE_CONSEQUENCE_HOLD_PRE_INTENT')
 elif kind=='MARCA':
  aid=st['active'];t=p.get('target')
  if aid!='F1' or t!='A' or st['actors'][aid]['resource']['standard']!=1 or st['actors'][aid]['resource']['pa']<25:
   raise Hold('MARCA_RESOURCES_PREFAIL')
  if not p.get('range_verified') or not p.get('los_verified'):raise Hold('MARCA_RANGE_LOS_HOLD')
  if st['actors'][t]['resource']['hp']<=0:raise Hold('MARCA_NO_TARGET')
 elif kind in ('MOVE','SAFE_MOVE'):
  aid=st['active'];r=st['actors'][aid]['resource']
  if aid!='F1' or st['phase']!='ACTIVE' or r['hp']<=0 or r['movement']!=1 or r['position']!='B1' or p.get('to')!='B2':raise Hold('MOVEMENT_PREFAIL')
  if p.get('forced'):raise Hold('FORCED_MOVEMENT_NO_AOO_PATH')
  if 'B2' not in TOPOLOGY['B1'] or st['actors']['F2']['resource']['position']=='B2':raise Hold('TOPOLOGY_BLOCKED')
  if p.get('path')!=['B1','B2']:raise Hold('PATH_MISMATCH')
  adjacent=(st['actors']['A']['resource']['position'] in TOPOLOGY[r['position']])
  after_adj=(st['actors']['A']['resource']['position'] in TOPOLOGY['B2'])
  if not adjacent or after_adj:raise Hold('NOT_EXITING_ADJACENCY')
  if kind=='SAFE_MOVE':
   if st['actors'][aid]['resource']['standard']!=0 or st.get('safe_named_enemy')!='A':raise Hold('SAFE_DISENGAGE_NOT_DECLARED')
   if 'aoo' in p:raise Hold('SAFE_DISENGAGE_NO_AOO')
  else:
   a=st['actors']['A']['resource'];
   if a['hp']<=0:raise Hold('OPPORTUNITY_ACTOR_DEAD')
   if a['reaction']!=1 and 'aoo' in p:raise Hold('AOO_REACTION_UNAVAILABLE')
   if a['reaction']==1:
    tape=attack_tape(st,'A','F1',kind='AOO',adv=1)
    if core.canonical(p.get('aoo'))!=core.canonical(tape):raise Hold('AOO_PRE_INTENT_RNG_TAPE_BAD')
    if tape['crit'][:2]==[1,1] and tape['crit'][2]<=2:raise Hold('AOO_NEGATIVE_CRIT_HOLD')
 elif kind=='DISENGAGE':
  aid=st['active'];r=st['actors'][aid]['resource']
  if aid!='F1' or r['standard']!=1 or p!={'actor':'F1','enemy':'A'}:raise Hold('DISENGAGE_PREFAIL')
 elif kind=='END':
  aid=st['active'];r=st['actors'][aid]['resource']
  if p!={'actor':aid} or st['phase']!='ACTIVE' or r['standard']!=0:raise Hold('END_PREFAIL')
 else:raise Hold('INVALID_KIND_PREINTENT')

def command(db,kind,payload,failpoint=None):
 st,head,rev=core.load(db);verify_before(st,kind,payload)
 cmd='LAB-CMD-R126-'+core.sha({'run':st['run_id'],'revision':rev,'type':kind,'payload':payload})[:37]
 def runner(candidate,p,seq):
  sc=sc_from(candidate);native=[];extra={};a=candidate['active']
  if kind=='INIT':
   rows,tie=seed_init(candidate);candidate['order']=tie['order'];candidate['active']=tie['order'][0];candidate['phase']='ACTIVE';candidate['round']=1
   extra={'initiative':rows,'tie':tie}
  elif kind=='START':
   native.append(begin_source_turn(sc,a));candidate['actor_turns'][a]+=1
  elif kind=='STRIKE':
   native+=_native_strike(sc,candidate,p)
  elif kind=='MARCA':
   spec,state,proofs=src(candidate,a,p['target'],'MARCA')
   native.append(apply_marca_passos(sc,a,p['target'],source=spec,state=state,proofs=proofs,
    range_met=p['range_verified'],los_met=p['los_verified']))
   candidate['marks']['F1']={'target':'A','bonus':'PERCEPTION_SURVIVAL_ONLY_+10',
    'declared_duration_turns':3,'elapsed_turns':0,'timing':'HOLD_SOURCE_BOUNDARY',
    'source':FERYN,'revision_created':seq};candidate['ability_events']+=1
  elif kind=='DISENGAGE':
   sc.actors[a].standard=0;candidate['safe_named_enemy']='A'
   native.append(sc.record({'action':'SAFE_DISENGAGE','by':a,'against':'A','standard_consumed':1,
    'scope':'ONE_ENEMY_ONLY','source':COMBAT}))
  elif kind in ('MOVE','SAFE_MOVE'):
   if kind=='MOVE' and 'aoo' in p:
    tape=p['aoo'];spec,state,proofs=src(candidate,'A','F1','AOO')
    ev=apply_weapon_attack(sc,'A','F1',source=spec,state=state,proofs=proofs,
      roll_score=tape['score'],damage=tape['normal_damage'],damage_tag='perfurante',
      rd=Resistances(general=P['F1']['rd'],provenance='DOCUMENTED_PHYSICAL'),
      damage_dice_groups=tuple(map(tuple,tape['damage_groups'])),
      damage_roll_groups=tuple(map(tuple,tape['dmg_rolls'])),
      damage_fixed_bonus=tape['flat'],critical_sequence=tuple(tape['crit']),
      attack_roll_attempts=tuple(map(tuple,tape['hit_rolls'])),attack_bonus=tape['bonus'],
      advantage_levels=1,attack_origin='OPPORTUNITY')
    native.append(ev);candidate['action_nonce']['A']+=1;candidate['aoo_events']+=1
   if sc.actors[a].hp>0:
    source,state,proofs=move_source(candidate,a)
    native.append(move_via_verified_path(sc,a,source=source,state=state,proofs=proofs,
      destination='B2',path_evidence='R126_ABSTRACT_EDGE_B1_B2',
      travel_cost=Fraction(1),speed=Fraction(1)))
   else:
    native.append(sc.record({'action':'MOVEMENT_INTERRUPTED_BY_KO','by':a,
      'position_unchanged':True,'no_post_KO_displacement':True}))
  elif kind=='END':
   native.append(end_source_turn(sc,a))
   i=candidate['order'].index(a);candidate['turn_index']+=1
   for offset in range(1,len(candidate['order'])+1):
    j=(i+offset)%len(candidate['order']);who=candidate['order'][j]
    if sc.actors[who].hp>0:
     candidate['active']=who
     if j<=i:candidate['round']+=1
     break
   else:candidate['phase']='CENSORED_NO_LIVING';candidate['active']=None
  for who,actor in sc.actors.items():
   rr=asdict(actor);rr['ca']=int(rr['ca']);rr['base_speed']=int(rr['base_speed']);candidate['actors'][who]['resource']=rr
  return {'lineage':'VLAB_V081_R18_R26_ADD_R126','kind':kind,'native_actions':native,'extra':extra,
    'mode':'MESTRE_ONLY_TECHNICAL_COPIES','contract_ids':['ACTION_CATALOG_AIN01','PA_AND_PREBUFF_COSTS','REACTION_TRIGGER_AND_SINGLE_USE','TURN_SCHEDULER_EVENT_SOURCING','ITEM_EQUIPMENT_AND_ENHANCEMENTS']}
 return core.event_commit(db,cmd,kind,payload,runner,failpoint=failpoint)

def round_one(seed,scenario='INTEGRATED',safe=False):
 register_prereg();out=ROOT/'runs';out.mkdir(exist_ok=True)
 path=out/(f'R126_{scenario}_{seed}.sqlite');init(path,seed)
 command(path,'INIT',{'seed':seed});stats={'seed':seed,'scene':scenario,'source':SOURCE,'run_id':path.stem,'cmds':[],'censored':None}
 # Execute one completed scheduler round, not a full combat.
 for _ in range(3):
  st,_,_=core.load(path);a=st['active']
  if st['actors'][a]['resource']['hp']<=0:break
  command(path,'START',{'actor':a});stats['cmds'].append((a,'START'))
  st,_,_=core.load(path)
  if a=='A':
   target='F1'; reaction='CAPA';tape=attack_tape(st,a,target,dis=1)
   if tape['crit'][:2]==[1,1] and tape['crit'][2]<=2:stats['censored']='CRITICAL_FAILURE_PRE_INTENT';break
   command(path,'STRIKE',{'attack':tape,'reaction':reaction});stats['cmds'].append((a,'STRIKE_CAPA'))
  elif a=='F1':
   if safe:
    command(path,'DISENGAGE',{'actor':'F1','enemy':'A'});stats['cmds'].append((a,'SAFE_DISENGAGE'))
   else:
    command(path,'MARCA',{'target':'A','range_verified':True,'los_verified':True});stats['cmds'].append((a,'MARCA'))
   st,_,_=core.load(path)
   if st['actors'][a]['resource']['hp']>0:
    move={'to':'B2','path':['B1','B2'],'forced':False}
    if not safe and st['actors']['A']['resource']['reaction']==1:
     aoo=attack_tape(st,'A','F1',kind='AOO',adv=1)
     if aoo['crit'][:2]==[1,1] and aoo['crit'][2]<=2:stats['censored']='AOO_CRITICAL_FAILURE_PRE_INTENT';break
     move['aoo']=aoo
    command(path,'SAFE_MOVE' if safe else 'MOVE',move);stats['cmds'].append((a,'MOVE_WITH_AOO' if not safe else 'SAFE_MOVE'))
  elif a=='F2':
   target='A';tape=attack_tape(st,a,target)
   if tape['crit'][:2]==[1,1] and tape['crit'][2]<=2:stats['censored']='CRITICAL_FAILURE_PRE_INTENT';break
   command(path,'STRIKE',{'attack':tape,'reaction':'NONE'});stats['cmds'].append((a,'STRIKE'))
  st,_,_=core.load(path)
  command(path,'END',{'actor':a});stats['cmds'].append((a,'END'))
 st,head,rev=core.load(path)
 check=path.with_suffix('.checkpoint.sqlite')
 with sqlite3.connect(path) as c, sqlite3.connect(check) as dest:c.backup(dest)
 assert core.load(path)==core.load(check)
 with sqlite3.connect(path) as c:rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
 stats.update({'revision':rev,'head':head,'events':len(rows),'native_events':sum(len(x['detail']['native_actions']) for x in rows),
  'pa_spent':sum(x.get('PA_spent',0) for row in rows for x in row['detail']['native_actions']),
  'aoo':st['aoo_events'],'ability_events':st['ability_events'], 'marks':st['marks'],
  'final_positions':{k:v['resource']['position'] for k,v in st['actors'].items()},
  'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},
  'pa':{k:v['resource']['pa'] for k,v in st['actors'].items()},
  'reaction':{k:v['resource']['reaction'] for k,v in st['actors'].items()},
  'phase':'CENSORED' if stats['censored'] else 'ONE_ROUND_TECHNICAL_CHECKPOINT_NOT_FULL_COMBAT',
  'checksum_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
  'checkpoint_sha256':hashlib.sha256(check.read_bytes()).hexdigest()})
 return stats

if __name__=='__main__':
 register_prereg();results=[]
 for s,name,safe in [(943207,'PA_REACTION_AOO_DEV',False),(953209,'SAFE_DISENGAGE_RESERVED_NOT_BLIND',True)]:
  try:results.append(round_one(s,name,safe))
  except Exception as exc:
   results.append({'seed':s,'scene':name,'state':'ERROR_HOLD','exception':repr(exc)})
 (ROOT/'R126_EXECUTIONS.json').write_text(_json(results))
 print(_json(results))
