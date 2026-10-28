"""R166 4-source-actor directed fixture in corrected v0.8.1 + R18. Casulo actual CA/speed, R43 DES AoO, R42 negative/positive.
Not a full combat or ED team benchmark. Original R154/R155 never re-run.
"""
import sys,json,copy,hashlib,sqlite3
from fractions import Fraction
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).parent
STAGE=Path('/mnt/data/vlab_r161_work/baseline_r160/r61_extracted/work/fusion_stage12')
NATIVE=ROOT/'native_v081_controlled'
sys.path.insert(0,str(STAGE));sys.path.insert(0,str(NATIVE))
import vlab_r18_interactive as core
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(NATIVE))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,ActorActionState,FrozenRuleEvidence,
 begin_source_turn,end_source_turn,apply_weapon_attack,apply_casulo_brotos,move_via_verified_path,effective_movement_speed)
from vlab_rd_v08 import Resistances
COMBAT='3ebc2b324ede81f1be4be8804ac113c0';ERISTAN='3f6c2b324ede819cae98ec0f6a63de76';AUREN='3ebc2b324ede814bb730d47dd7bd5f02';FERYN='3f6c2b324ede81ce9c61db8127bf0e31';VAROK='3f6c2b324ede81f49ea9efbe1a811091';OP='3f3c2b324ede819496ddd7f93bd7e5d2'
PROFILES={'E':{'name':'Eristan','hp':630,'pa':804,'ca':76,'con':45,'rd':25,'speed':None,'dex':28,'at':[4,6,30],'damage':[[8,10]],'damage_flat':26,'source':ERISTAN,'rank':'Ouro Negro'},
'A':{'name':'Auren','hp':523,'pa':719,'ca':225,'con':48,'rd':35,'speed':16,'dex':164,'at':[6,6,193],'damage':[[8,8]],'damage_flat':211,'source':AUREN,'rank':'Lendário'},
'F':{'name':'Feryn','hp':479,'pa':424,'ca':123,'con':24,'rd':22,'speed':None,'dex':80,'at':[4,6,92],'damage':[[8,8]],'damage_flat':47,'source':FERYN,'rank':'Ouro Negro'},
'V':{'name':'Varok','hp':734,'pa':324,'ca':83,'con':45,'rd':35,'speed':None,'dex':29,'at':[4,6,100],'damage':[[10,10]],'damage_flat':48,'source':VAROK,'rank':'Ouro Negro'}}
RNG_PREFIX='R166'
def roll(seed,who,term,nonce,n,faces):return core.dice(seed,nonce,f'{RNG_PREFIX}-{who}-{term}',n,faces)
def crit(seed,who):return [roll(seed,who,f'AOO-CRIT-{j}',1,1,6)[0] for j in range(3)]
negseed=[k for k in range(1195001,1205000) if crit(k,'F')[:2]==[1,1] and crit(k,'F')[2]<=2][1]
posseed=next(k for k in range(1205001,1215000) if crit(k,'F')[:2]==[6,6] and crit(k,'F')[2]>=5)
SET=[{'id':f'R166_V2_CASULO_AOO_NEGATIVE_DEV_S{negseed}','seed':negseed,'A_initial_hp':523,'expected':'FIRST_CRITICAL_NEGATIVE_SECOND_AOO_ATTEMPT_MOVE'},
{'id':f'R166_V2_CASULO_AOO_KO_DEV_S{posseed}','seed':posseed,'A_initial_hp':60,'expected':'FIRST_CRITICAL_POSITIVE_KO_NO_SECOND_NO_MOVEMENT'}]
PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R166','baseline':'R01-R160 immutable','source_system_combat':COMBAT,
 'source_R42_R43':OP,'source_cocoon':ERISTAN,'actor_profiles':{w:{'page':p['source'],'rank':p['rank'],'hp':p['hp'],'free_PA':p['pa'],'CA':p['ca'],'DES':p['dex'],'speed':p['speed']} for w,p in PROFILES.items()},
 'four_independent_master_side_characters':['Eristan E (ally healer)','Auren A (ally mover)','Feryn F (enemy AoO)','Varok V (enemy AoO)'],
 'source_cocoon':'Eristan 60 PA, +22 CA and -4m, duration two turns expiry HOLD, Auren within 3m ally',
 'geometry':'Metric independent fixture: Eristan within 3m of Auren, Auren adjacent to Feryn+Varok; voluntary exit path 1.5m, no universal block metre conversion',
 'priority':'R43 Feryn DES80 > Varok DES29; AoO 1 advantage, each reaction once',
 'policy':'E casts Casulo, A begins turn and voluntarily exits adjacency, opportunity chain. Stop technical fixture at interruption, not a full battle.',
 'experimental_injured_fixture':'A_initial_HP60 < source MAX523 but above Fraco (<52.3), not a canonical encounter',
 'directed_seed_selection':'first seed in disjoint ranges with F negative R42 and F positive R42 respectively, not holdout',
 'branches':SET,'NO_REPEAT':['R154/R155','R01-R160']}
PRE=ROOT/'R166_PREREG_CASULO_R43_R42_V2.json'
if PRE.exists():assert json.loads(PRE.read_text())==PREREG
else:PRE.write_text(json.dumps(PREREG,indent=2,ensure_ascii=False)+'\n')

def proof(page,rule):return (FrozenRuleEvidence(page,rule,hashlib.sha256((page+'|'+rule+'|R166').encode()).hexdigest(),'2026-10-17_SOURCE_REOPEN','READ_ONLY_NOT_FULL_SNAPSHOT_FREEZE'),)
def src_state(st,actor,target,kind):
 r=st['actors'][actor]['resource'];p=PROFILES[actor]
 if kind=='CASULO':src=AbilitySource('R166-E-CASULO','control','STANDARD',ERISTAN,'CASULO_BROTOS','RULE-DERIVED',required_pa=60,target_scope='ALLY',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-R166')
 elif kind=='AOO':src=AbilitySource('R166-'+actor+'-AOO','attack','REACTION',COMBAT,'R3_OPPORTUNITY','RULE-DERIVED',required_pa=0,target_scope='ENEMY',reaction_trigger='EXIT_ADJACENT',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-R166')
 elif kind=='MOVE':src=AbilitySource('R166-A-MOVE','move','MOVEMENT',COMBAT,'R3_MOVE','RULE-DERIVED',required_pa=0,target_scope='NONE',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-R166')
 else:raise ValueError(kind)
 scope=src.target_scope;ob=ActorActionState(actor,23 if actor=='A' else 20,r['pa'],(src.action_id,),standard_available=r['standard']==1,
 movement_available=r['movement']==1,reaction_available=r['reaction']==1,reaction_trigger_observed=src.reaction_trigger,
 range_confirmed=True,los_confirmed=True,geometry_confirmed=True,
 enemy_ids_visible=(target,) if scope=='ENEMY' else (),ally_ids_visible=(target,) if scope=='ALLY' else ())
 return src,ob,proof(src.source_page_id,src.rule_id)

def ao_tape(seed,actor):
 p=PROFILES[actor];n=1
 hits=[roll(seed,actor,f'AOO-HIT-{j}',n,p['at'][0],6) for j in range(2)]
 critical=crit(seed,actor)
 dmg=[roll(seed,actor,f'AOO-DMG-{j}',n,c,f) for j,(c,f) in enumerate(p['damage'])]
 return {'who':actor,'nonce':1,'rolls':hits,'crit':critical,'damage_roll_groups':dmg,
 'score':max(map(sum,hits))+p['at'][2]+2,'dmg':sum(map(sum,dmg))+p['damage_flat']}

def init(cfg):
 path=ROOT/'runs'/(cfg['id']+'.sqlite');path.parent.mkdir(exist_ok=True)
 if path.exists():raise ValueError('NO_REPEAT_EXISTING_RUN')
 core.init_db(path,'A',cfg['seed']);s=core.initial('A',cfg['seed'])
 s.update({'scene':cfg['id'],'run_id':cfg['id'],'seed':cfg['seed'],'phase':'ACTIVE_TECHNICAL','active':'E','order':['E','A','F','V'],
 'round':1,'action_nonce':{'E':0,'A':0,'F':0,'V':0},'cocoon':False,'aoo_trigger':False,
 'geometry':'R166_METRIC_1.5M_PATH_SEPARATE_FROM_B0_B3','time_boundary':'CASULO_2_TURN_EXACT_HOLD',
 'prereg_sha256':hashlib.sha256(PRE.read_bytes()).hexdigest(),'actors':{}})
 for name,p in PROFILES.items():
  hp=cfg['A_initial_hp'] if name=='A' else p['hp'];pos={'E':'E_WITHIN_3M_OF_A','A':'CENTER','F':'LEFT','V':'RIGHT'}[name]
  x=Combatant(name,hp,p['pa'],p['ca'],p['con'],0,0,0,pos,rank=p['rank'],standard=0,movement=0,reaction=1,
   maximum_hp=p['hp'],base_speed=p['speed'])
  z=asdict(x);z['ca']=int(z['ca']);z['base_speed']=int(z['base_speed']) if z['base_speed'] is not None else None
  s['actors'][name]={'source':p['source'],'resource':z,'source_profile':p}
 anchor=core.sha({'genesis':s,'lineage':'R18_R26_V081_R166_R42_R43_CASULO'})
 with core.connect(path) as c:
  for k,v in [('scene',cfg['id']),('genesis',anchor),('head',anchor),('state',core.canonical(s))]:c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 path.with_suffix('.genesis.json').write_text(core.canonical(s)+'\n')
 return path

def command(db,kind,payload):
 st,head,rev=core.load(db);who=st['active'];r=st['actors'][who]['resource']
 if kind=='START':assert payload=={'actor':who} and who in ('E','A') and r['standard']==0
 elif kind=='COCOON':assert who=='E' and not st['cocoon'] and r['standard']==1 and r['pa']>=60 and payload=={'target':'A','range_m':3}
 elif kind=='END_E':assert who=='E' and r['standard']==0 and payload=={'actor':'E'}
 elif kind=='AOO_CHAIN':
  assert who=='A' and r['movement']==1 and st['cocoon'] and not st['aoo_trigger']
  assert payload['order']==['F','V'] and payload['voluntary'] and payload['distance_m']==1.5
  assert payload['tapes']==[ao_tape(st['seed'],'F'),ao_tape(st['seed'],'V')]
 else:raise ValueError(kind)
 cmd='LAB-CMD-R166-'+core.sha({'run':st['run_id'],'rev':rev,'kind':kind,'p':payload})[:40]
 def reducer(s,q,seq):
  sc=Scene({who:Combatant(**v['resource']) for who,v in s['actors'].items()},seed=s['seed'],provenance='R166_SOURCE_SCOPED_TECHNICAL_AOO_CASULO')
  e=[];skipped=[];actor=s['active']
  if kind=='START':e.append(begin_source_turn(sc,actor))
  elif kind=='COCOON':
   src,sta,pf=src_state(s,'E','A','CASULO')
   e.append(apply_casulo_brotos(sc,'E','A',source=src,state=sta,proofs=pf,range_m=3,same_caster_effect_active=s['cocoon']))
   s['cocoon']=True
  elif kind=='END_E':
   e.append(end_source_turn(sc,'E'));s['active']='A'
  elif kind=='AOO_CHAIN':
   for attacker,t in zip(q['order'],q['tapes']):
    if sc.actors['A'].hp<=0:
     skipped.append({'attacker':attacker,'reason':'PRIOR_KO_TARGET_NO_LONGER_ELIGIBLE','reaction_preserved':sc.actors[attacker].reaction});continue
    src,sta,pf=src_state(s,attacker,'A','AOO');pp=PROFILES[attacker]
    ev=apply_weapon_attack(sc,attacker,'A',source=src,state=sta,proofs=pf,roll_score=t['score'],damage=t['dmg'],damage_tag=('perfurante' if attacker=='F' else 'impacto'),
     rd=Resistances(general=35,provenance='AUREN_RD_FISICO35'),
     damage_dice_groups=tuple(map(tuple,pp['damage'])),damage_roll_groups=tuple(map(tuple,t['damage_roll_groups'])),
     damage_fixed_bonus=pp['damage_flat'],critical_sequence=tuple(t['crit']),attack_roll_attempts=tuple(map(tuple,t['rolls'])),
     attack_bonus=pp['at'][2],advantage_levels=1,attack_origin='OPPORTUNITY',lab_negative_critical_policy=True)
    e.append(ev);s['action_nonce'][attacker]+=1
   if sc.actors['A'].hp>0:
    src,sta,pf=src_state(s,'A',None,'MOVE')
    e.append(move_via_verified_path(sc,'A',source=src,state=sta,proofs=pf,
      destination='OUT_OF_ADJACENCY',path_evidence='R166_EXPLICIT_METRIC_1_5M_TO_OUT_OF_TWO_ADJACENCIES',
      travel_cost=Fraction(3,2),speed=effective_movement_speed(sc.actors['A'])))
   s['aoo_trigger']=True;s['phase']='TECHNICAL_AOO_PREFIX_COMPLETE';s['active']=None
  for who,x in sc.actors.items():
   z=asdict(x);z['ca']=int(z['ca']);z['base_speed']=int(z['base_speed']) if z['base_speed'] is not None else None
   s['actors'][who]['resource']=z
  return {'native_actions':e,'skipped':skipped,'priority':'R43_DESC_DES_F80_ABOVE_V29',
          'scope':'R166_CA_AOO_CAUSAL_PREFIX_NO_COMBAT_VICTORY','source_authority':[COMBAT,OP,ERISTAN,AUREN,FERYN,VAROK]}
 return core.event_commit(db,cmd,kind,payload,reducer)

def scenario(cfg):
 db=init(cfg)
 for kind,p in [('START',{'actor':'E'}),('COCOON',{'target':'A','range_m':3}),('END_E',{'actor':'E'}),('START',{'actor':'A'})]:command(db,kind,p)
 s,_,_=core.load(db)
 assert s['actors']['A']['resource']['ca']==247 and s['actors']['A']['resource']['cocoon_source_speed_penalty_m']==4
 assert effective_movement_speed(Combatant(**s['actors']['A']['resource']))==12
 command(db,'AOO_CHAIN',{'order':['F','V'],'voluntary':True,'distance_m':1.5,'tapes':[ao_tape(s['seed'],'F'),ao_tape(s['seed'],'V')]})
 s,head,rev=core.load(db)
 with sqlite3.connect(db) as c:rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
 with sqlite3.connect(db) as src,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as cp:src.backup(cp)
 assert core.load(db)==core.load(db.with_suffix('.checkpoint.sqlite'))
 x=[e for row in rows for e in row['detail']['native_actions']]
 att=[a for a in x if a['action']=='weapon_attack']
 return {'run':cfg['id'],'seed':cfg['seed'],'commits':rev,'native_events':len(x),'A_HP_initial':cfg['A_initial_hp'],
 'A_HP_final':s['actors']['A']['resource']['hp'],'cocoon_CA_active':s['actors']['A']['resource']['ca'],
 'cocoon_speed_m':12,'R42_critical_first':att[0]['critical'],'R43_actual_order':[a['from'] for a in att],
 'Varok_reaction_remaining':s['actors']['V']['resource']['reaction'],
 'A_position':s['actors']['A']['resource']['position'],'AOO_net_post_RD':sum(a['net'] for a in att),
 'AOO_actual_HP_lost':sum(a['hp_loss_actual'] for a in att),'AOOs':len(att),
 'Cocoon_PA':60,'temporal_exact_expiry':'HOLD','head':head,'status':'SOURCE_SCOPED_TECHNICAL_PASS_PREFIX_NOT_FULL_BATTLE'}
if __name__=='__main__':
 r=[scenario(cfg) for cfg in SET]
 (ROOT/'R166_CONCURRENT_CASULO_AOO_RESULTS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(r,ensure_ascii=False,indent=2))
