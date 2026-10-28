"""R130 add-on three-actor real-source healing demonstration using native V081, R18 and R26.
NO official scene, NO Party writes, NO replacement of R126 or historical banks.
"""
import copy,json,hashlib,sqlite3,sys
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import r126_shared_three_actor as base
from r126_native_integration import core, r26,sc_from,src,proof,attack_tape,P,FERYN,COMBAT
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,
  begin_source_turn,end_source_turn,apply_weapon_attack,apply_reconstituicao_seiva)
EID='3f6c2b324ede819cae98ec0f6a63de76'
EP=dict(source=EID,rank='Ouro Negro',rank_index=20,init_dice=4,init_bonus=30,dex=28,
 hp=630,pa=804,ca=76,con=45,armor=32,fort=2,reflex=0,rd=25,speed=None,
 attack_dice=4,attack_flat=14,damage_dice=((8,10),),damage_flat=26)
TEAM={'A':'ONE','F1':'TWO','E':'TWO'}
PRE={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R130',
 'source_auren':base.AUREN,'source_feryn':FERYN,'source_eristan':EID,
 'ability':'Reconstituição de Seiva—75PA, 8d10+25 healing, ally within 5m, no revival, capped at HPmax; equipment gloves +20 once/cast',
 'experimental_geometry':'E and F1 close <=5m, source-checked fixture; not canonical battlefield location',
 'seed':963211,'family':'development-directed; no blind holdout',
 'participants':['A:Auren','F1:Feryn','E:Eristan'],
 'sequence':['A normal attack F1; no reaction','F1 normal attack A; no reaction','E native heal F1 (75 PA + equipped gloves+20)'],
 'NO_REPEAT':['R01–R125','R126 seeded scenes','R123 UNKNOWN_EFFECT'],
 'source_status':'all three source fiche Master-side (Feryn Eristan proposals), NO player/Party or official rank credit'}

def freeze():
 file=ROOT/'R130_PREREG_HEAL.json';data=json.dumps(PRE,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
 if file.exists():assert file.read_text()==data
 else:file.write_text(data)
 return file

def genesis(db,seed):
 freeze();st=base.snapshot(db.stem,seed);st.update({'stage':'R130','run_id':db.stem,
  'kind':'R130_HEAL_3_ACTOR_MASTER_ONLY','prereg_hash':hashlib.sha256((ROOT/'R130_PREREG_HEAL.json').read_bytes()).hexdigest(),
  'teams':TEAM,'marks':{},'technical_instancing':False,'no_canonical_credit':True,
  'source_fingerprint':core.sha(PRE),'source_healing_status':'PRECREATE_MASTER_ONLY_EXPERIMENTAL'})
 st['actors'].pop('F2');st['action_nonce'].pop('F2');st['actor_turns'].pop('F2')
 c=Combatant('E',EP['hp'],EP['pa'],EP['ca'],EP['con'],EP['armor'],EP['fort'],EP['reflex'],'SOURCE_FIXTURE_NEAR_F1',
  rank=EP['rank'],standard=0,movement=0,reaction=1,maximum_hp=EP['hp'])
 st['actors']['E']={'source':EID,'source_profile':EP,'resource':asdict(c)}
 st['action_nonce']['E']=0;st['actor_turns']['E']=0
 st['actors']['A']['resource']['position']='SOURCE_FIXTURE_ATTACK_F1'
 st['actors']['F1']['resource']['position']='SOURCE_FIXTURE_NEAR_E'
 return st

def init(db,seed):
 if db.exists():raise ValueError('NO_REUSE')
 core.init_db(db,'A',seed);st=genesis(db,seed);h=core.sha({'genesis':st,'lineage':'R18_R26_V081_R130_HEAL'})
 with core.connect(db) as c:
  for k,v in [('scene',st['scene']),('genesis',h),('head',h),('state',core.canonical(st))]:
   c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 db.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')

def team_initiative(st):
 rows=[]
 for actor in ('A','F1','E'):
  p=st['actors'][actor]['source_profile'];d=core.dice(st['seed'],0,'R130-'+actor+'-INIT',p['init_dice'],6)
  rows.append({'id':actor,'source':p['source'],'dice':d,'des':p['dex'],'total':sum(d)+p['init_bonus']})
 def reroll(aid,n):
  p=st['actors'][aid]['source_profile'];return sum(core.dice(st['seed'],n,'R130-'+aid+'-INIT-TIE',p['init_dice'],6))+p['init_bonus']
 return rows,r26.tie_order(rows,reroll)

def local_attack_tape(st,who,target):
 p=st['actors'][who]['source_profile'];n=st['action_nonce'][who]+1;seed=st['seed']
 weak=10*st['actors'][who]['resource']['hp']<p['hp']
 hit=[core.dice(seed,n,f'R130-{who}-HIT-{i}',p['attack_dice'],6) for i in range(2 if weak else 1)]
 crit=[core.dice(seed,n,f'R130-{who}-CRIT-{i}',1,6)[0] for i in range(3)]
 damage=[core.dice(seed,n,f'R130-{who}-DMG-{i}',n0,f0) for i,(n0,f0) in enumerate(p['damage_dice'])]
 score=(min(map(sum,hit))-2 if weak else sum(hit[0]))+p['attack_flat']
 return {'actor':who,'target':target,'nonce':n,'hit_rolls':hit,'crit':crit,'damage_rolls':damage,
  'damage':sum(map(sum,damage))+p['damage_flat'],'score':score,'weak':weak}

def source_attack(st,who,target):
 p=st['actors'][who]['source_profile'];r=st['actors'][who]['resource'];source=AbilitySource(
  f'R130-{who}-NORMAL','attack','STANDARD',p['source'],'NORMAL_ATTACK_REAL_SOURCE','RULE-DERIVED',
  target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081_WEAPON')
 state=ActorActionState(who,p['rank_index'],r['pa'],(source.action_id,),
  standard_available=r['standard']==1,enemy_ids_visible=(target,),range_confirmed=True,
  los_confirmed=True,geometry_confirmed=True)
 pr=(FrozenRuleEvidence(p['source'],'NORMAL_ATTACK_REAL_SOURCE',hashlib.sha256(p['source'].encode()).hexdigest(),
  '2026-10-16_NOTION_READ','R130_FICHE_SOURCE'),)
 return source,state,pr

def heal_spec(st):
 r=st['actors']['E']['resource'];source=AbilitySource('R130-E-RECONSTITUICAO_SEIVA','heal','STANDARD',EID,
  'RECONSTITUICAO_75PA_8D10_25','RULE-DERIVED',required_pa=75,target_scope='ALLY',
  effect_adapter_ready=True,effect_adapter_id='V081_SOURCE_HEAL')
 state=ActorActionState('E',20,r['pa'],(source.action_id,),standard_available=r['standard']==1,
  ally_ids_visible=('F1',),range_confirmed=True,los_confirmed=True,geometry_confirmed=True)
 excerpt='Reconstituição de Seiva Padrão 75PA cura 8d10+25 aliado até5m; Luvas do Vaso da Vida +20PV uma vez por conjuração'
 evidence=(FrozenRuleEvidence(EID,source.rule_id,hashlib.sha256(excerpt.encode()).hexdigest(),
 '2026-10-16_NOTION_READ','R130_HEAL_FICHE_EQUIPMENT'),)
 return source,state,evidence

def action(db,kind,payload):
 st,head,rev=core.load(db);active=st['active']
 if kind=='INIT':
  if st['phase']!='INIT' or payload!={'seed':st['seed']}:raise ValueError('INIT_INVALID')
 elif kind=='START':
  if st['phase']!='ACTIVE' or active!=payload.get('actor') or st['actors'][active]['resource']['standard']!=0:raise ValueError('START_INVALID')
 elif kind=='ATTACK':
  if st['phase']!='ACTIVE' or payload['attack']!=local_attack_tape(st,active,payload['attack']['target']):raise ValueError('ATTACK_TAPE_INVALID')
  if payload['attack']['crit'][:2]==[1,1] and payload['attack']['crit'][2]<=2:raise ValueError('CRITICAL_FAILURE_HOLD_PRE_INTENT')
  if st['actors'][active]['resource']['standard']!=1:raise ValueError('STANDARD_SPENT')
 elif kind=='HEAL':
  r=st['actors'].get('E',{}).get('resource',{})
  if active!='E' or r.get('pa',0)<75 or r.get('standard')!=1 or payload.get('target')!='F1' or not payload.get('range'):
   raise ValueError('HEAL_NOT_LEGAL')
  if st['actors']['F1']['resource']['hp']<=0 or st['actors']['F1']['resource']['hp']>=479:raise ValueError('HEAL_EMPTY_OR_KO')
  if payload.get('dice')!=core.dice(st['seed'],1,'R130-E-HEAL',8,10):raise ValueError('HEAL_TAPE_INVALID')
 elif kind=='END':
  if payload!={'actor':active} or st['actors'][active]['resource']['standard']!=0:raise ValueError('END_INVALID')
 else:raise ValueError('UNKNOWN_KIND')
 id='LAB-CMD-R130-'+core.sha({'run':st['run_id'],'rev':rev,'kind':kind,'payload':payload})[:39]
 def reducer(c,p,seq):
  scene=Scene({aid:Combatant(**v['resource']) for aid,v in c['actors'].items()},seed=c['seed'],
    provenance='R130_3_SOURCED_PRECREATE_MASTER_ONLY');events=[];extras={};aid=c['active']
  if kind=='INIT':
   rows,ordered=team_initiative(c);c['order']=ordered['order'];c['active']=ordered['order'][0];c['round']=1;c['phase']='ACTIVE'
   extras={'initiative':rows,'tie':ordered}
  elif kind=='START':events.append(begin_source_turn(scene,aid));c['actor_turns'][aid]+=1
  elif kind=='ATTACK':
   tape=p['attack'];tar=tape['target'];source,state,proofs=source_attack(c,aid,tar)
   ep=c['actors'][tar]['source_profile'];out=apply_weapon_attack(scene,aid,tar,source=source,state=state,proofs=proofs,
    roll_score=tape['score'],damage=tape['damage'],damage_tag='perfurante',
    rd=base.Resistances(general=ep['rd'],provenance='SOURCE_PHYSICAL'),
    damage_dice_groups=tuple(ep0 for ep0 in c['actors'][aid]['source_profile']['damage_dice']),
    damage_roll_groups=tuple(map(tuple,tape['damage_rolls'])),
    damage_fixed_bonus=c['actors'][aid]['source_profile']['damage_flat'],
    critical_sequence=tuple(tape['crit']),attack_roll_attempts=tuple(map(tuple,tape['hit_rolls'])),
    attack_bonus=c['actors'][aid]['source_profile']['attack_flat'])
   events.append(out);c['action_nonce'][aid]+=1
  elif kind=='HEAL':
   source,state,evidence=heal_spec(c)
   ev=apply_reconstituicao_seiva(scene,'E','F1',source=source,state=state,proofs=evidence,
    dice_rolls=tuple(p['dice']),range_met=p['range'],gloves_equipped=True)
   events.append(ev)
  elif kind=='END':
   events.append(end_source_turn(scene,aid));j=c['order'].index(aid);c['turn_index']+=1
   for off in range(1,4):
    ind=(j+off)%3;next_=c['order'][ind]
    if scene.actors[next_].hp>0:
     c['active']=next_;
     if ind<=j:c['round']+=1
     break
  for k,v in scene.actors.items():
   r=asdict(v);r['ca']=int(r['ca']);r['base_speed']=None;c['actors'][k]['resource']=r
  return {'lineage':'R18_R26_V081_R130_NATIVE_HEAL','native_actions':events,'extra':extras,
   'scope':'MASTER_PRECREATE_3_ACTORS_NOT_CANONICAL'}
 return core.event_commit(db,id,kind,payload,reducer)

def run():
 freeze();runid='R130_HEAL_SOURCE_3ACTOR_S963211';db=ROOT/'runs'/f'{runid}.sqlite';init(db,963211)
 action(db,'INIT',{'seed':963211});commands=[]
 for turn in range(3):
  st,_,_=core.load(db);aid=st['active'];action(db,'START',{'actor':aid});commands.append((aid,'START'))
  st,_,_=core.load(db)
  if aid=='E':
   tape=core.dice(st['seed'],1,'R130-E-HEAL',8,10)
   action(db,'HEAL',{'target':'F1','range':True,'dice':tape});commands.append((aid,'HEAL'))
  else:
   target='F1' if aid=='A' else 'A';tape=local_attack_tape(st,aid,target)
   if tape['crit'][:2]==[1,1] and tape['crit'][2]<=2:raise ValueError('PREREG_SEED_CRITICAL_FAILURE_HOLD')
   action(db,'ATTACK',{'attack':tape});commands.append((aid,'ATTACK'))
  action(db,'END',{'actor':aid});commands.append((aid,'END'))
 st,head,revision=core.load(db);checkpoint=db.with_suffix('.checkpoint.sqlite')
 with sqlite3.connect(db) as src,sqlite3.connect(checkpoint) as dst:src.backup(dst)
 assert core.load(db)==core.load(checkpoint)
 with sqlite3.connect(db) as c:evs=[json.loads(x[0]) for x in c.execute('SELECT row_json FROM events ORDER BY seq')]
 report={'run_id':runid,'seed':st['seed'],'revision':revision,'event_count':len(evs),
  'native_events':sum(len(e['detail']['native_actions']) for e in evs),'commands':commands,
  'hp':{k:x['resource']['hp'] for k,x in st['actors'].items()},
  'pa':{k:x['resource']['pa'] for k,x in st['actors'].items()},
  'healing_events':[v for e in evs for v in e['detail']['native_actions'] if v['action']=='RECONSTITUICAO_SEIVA'],
  'head':head,'not_official':True,'full_combat':False}
 (ROOT/'R130_HEAL_EXECUTION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report

if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
