"""Controlled native AoO concurrency R43, 3 source-derived TECHNICAL actors Auren/Feryn/Feryn.
Original v0.8.1 apply_weapon_attack + R18 atomic reducer + R43 DES priority.
"""
import copy,json,sqlite3,hashlib,sys
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import r138_multiround_native as m
from r126_shared_three_actor import PROFILES as ALL_PROFILES
from vlab_effects_v08 import (Scene,Combatant,apply_weapon_attack,begin_source_turn,end_source_turn,move_via_verified_path)
from vlab_rd_v08 import Resistances
core=m.core
P={'A':copy.deepcopy(m.PROFILE['A']),'F1':copy.deepcopy(m.PROFILE['F1']),'F2':copy.deepcopy(ALL_PROFILES['F2'])}
PRE={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R154','source_R43':'https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2',
 'source_rule3':'https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0',
 'priority':'Auren DES164 ahead of Feryn DES80; R43 tie requiring dice not exercised',
 'mover':'F2 TECHNICAL Feryn copy (speed40m), not second canon NPC; voluntary CENTER->OUT path1.5m exact fixture',
 'start_adjacent':['A at LEFT','F1 at RIGHT','F2 at CENTER'], 'end_adjacent':[],
 'outcomes':[{'id':'R154_TWO_AOO_FULL_SOURCE_DEV_S999141','seed':999141,'mover_hp':479},
             {'id':'R154_TWO_AOO_KO_SOURCE_DEV_S999142','seed':999142,'mover_hp':200}],
 'source_hp_reduced_fixture':'KO200 is synthetic mid-battle injured from source MAX479, not an earlier documented fight',
 'constraints':'No AoO on forced movement, no passive double reaction, F2 loses action if KO; metric distance independent of B0–B3, not universal scale',
 'event_semantics':'all AoO and optional move in single R18 transactional commit; no reentry after 0HP; second attacker not consumed if first KO',
 'no_repeat':'R01–R150 and R154 once published'}
(ROOT/'R154_CONCURRENT_AOO_PREREG.json').write_text(json.dumps(PRE,ensure_ascii=False,indent=2)+'\n')

def init(runid,seed,hp):
 db=ROOT/'runs'/f'{runid}.sqlite';db.parent.mkdir(exist_ok=True)
 if db.exists():raise ValueError('NO_REPEAT_DB')
 core.init_db(db,'A',seed);st=core.initial('A',seed)
 st.update({'scene':runid,'run_id':runid,'phase':'ACTIVE','active':'F2','order':['F2','A','F1'],'round':1,
 'turn_index':0,'pre_registered':PRE,'action_nonce':{'A':0,'F1':0,'F2':0},'aoo_trigger_consumed':False,
 'positions':'verified scenario CENTER with LEFT/RIGHT adjacent, OUT not adjacent; independent metric path1.5m',
 'technical_instancing':True,'terminal_contracts':0,'actors':{}})
 for who,p in P.items():
  pos='CENTER' if who=='F2' else 'LEFT' if who=='A' else 'RIGHT'
  c=Combatant(who,hp if who=='F2' else p['hp'],p['pa'],p['ca'],p['con'],p['armor'],p['fort'],p['reflex'],pos,
   rank=p['rank'],standard=0,movement=0,reaction=1,maximum_hp=p['hp'],base_speed=p['speed'])
  st['actors'][who]={'source':p['source'],'source_profile':p,'resource':asdict(c)}
 anchor=core.sha({'genesis':st,'lineage':'R18_R26_V081_R43_CONCURRENT_AOO'})
 with core.connect(db) as c:
  for k,v in [('scene',runid),('genesis',anchor),('head',anchor),('state',core.canonical(st))]:c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 db.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')
 return db

def tape(st,who):
 p=P[who];n=st['action_nonce'][who]+1;seed=st['seed']
 def d(k,c,f):return core.dice(seed,n,'R154-'+who+'-'+k,c,f)
 hits=[d('AOO-HIT-'+str(j),p['attack_dice'],6) for j in range(2)]
 score=max(map(sum,hits))+p['attack_flat']+2
 crit=[d('AOO-CRIT-'+str(j),1,6)[0] for j in range(3)]
 dmg=[d('AOO-DMG-'+str(j),n,f) for j,(n,f) in enumerate(p['damage_dice'])]
 return {'actor':who,'to':'F2','nonce':n,'rolls':hits,'crit':crit,'damage_rolls':dmg,'score':score,'normal_damage':sum(map(sum,dmg))+p['damage_flat']}

def command(db,kind,p):
 st,head,rev=core.load(db)
 if kind=='START':assert p=={'actor':'F2'} and st['actors']['F2']['resource']['standard']==0
 elif kind=='AOO_CHAIN':
  assert st['active']=='F2' and st['actors']['F2']['resource']['movement']==1 and not st['aoo_trigger_consumed']
  assert p['path_distance_m']==1.5 and p['voluntary'] is True and p['order']==['A','F1']
  assert p['tapes']==[tape(st,'A'),tape(st,'F1')]
 elif kind=='PASS':assert st['actors']['F2']['resource']['hp']>0 and st['actors']['F2']['resource']['standard']==1
 elif kind=='END':assert st['actors']['F2']['resource']['standard']==0
 else:raise ValueError('UNKNOWN')
 cmd='LAB-CMD-R154-'+core.sha({'run':st['run_id'],'rev':rev,'kind':kind,'payload':p})[:39]
 def reducer(c,q,seq):
  sc=Scene({who:Combatant(**v['resource']) for who,v in c['actors'].items()},seed=c['seed'],provenance='MESTRE_ONLY_SOURCE_DERIVED_R154_CONCURRENT_AOO')
  events=[];skipped=[]
  if kind=='START':events.append(begin_source_turn(sc,'F2'))
  elif kind=='AOO_CHAIN':
   assert P['A']['dex']>P['F1']['dex']
   for who,entry in zip(q['order'],q['tapes']):
    if sc.actors['F2'].hp<=0:
     skipped.append({'attacker':who,'reason':'MOVING_TARGET_KO_FIRST_AOO','reaction_preserved':sc.actors[who].reaction});continue
    assert sc.actors[who].reaction==1
    # Use action catalog proper SOURCE and REACTION WINDOW from the R138 existing adapter.
    sp,state,pr=m.source_state(c,who,'F2','AOO');pp=P[who]
    ev=apply_weapon_attack(sc,who,'F2',source=sp,state=state,proofs=pr,roll_score=entry['score'],damage=entry['normal_damage'],damage_tag='perfurante',
      rd=Resistances(general=P['F2']['rd'],provenance='DOCUMENTED_PHYSICAL_RD22'),
      damage_dice_groups=tuple(map(tuple,pp['damage_dice'])),damage_roll_groups=tuple(map(tuple,entry['damage_rolls'])),
      damage_fixed_bonus=pp['damage_flat'],critical_sequence=tuple(entry['crit']),attack_roll_attempts=tuple(map(tuple,entry['rolls'])),
      attack_bonus=pp['attack_flat'],advantage_levels=1,attack_origin='OPPORTUNITY',lab_negative_critical_policy=True)
    events.append(ev);c['action_nonce'][who]+=1
   if sc.actors['F2'].hp>0:
    from r126_native_integration import move_source
    # Existing source-gated movement adapter. Explicit 1.5m scene fixture, not per-block scale.
    move_s,move_st,move_proof=move_source(c,'F2')
    events.append(move_via_verified_path(sc,'F2',source=move_s,state=move_st,proofs=move_proof,
      destination='OUT',path_evidence='R154_VERIFIED_SCENE_CENTER_EXIT_OUT_1_5M',travel_cost=Fraction(3,2),speed=Fraction(P['F2']['speed'])))
   c['aoo_trigger_consumed']=True
  elif kind=='PASS':sc.actors['F2'].standard=0;events.append(sc.record({'action':'FOREGO_STANDARD','by':'F2','fixture_only':True}))
  elif kind=='END':events.append(end_source_turn(sc,'F2'));c['phase']='COMPLETE_TECHNICAL_AOO';c['active']=None
  for who,x in sc.actors.items():
   resource=asdict(x);resource['ca']=int(resource['ca']);resource['base_speed']=int(resource['base_speed']) if resource['base_speed'] is not None else None
   c['actors'][who]['resource']=resource
  return {'native_actions':events,'priority':'R43_DES_DESC','skip_reason':skipped,'source':'R18_R26_V081_R43','no_official_result':True}
 return core.event_commit(db,cmd,kind,p,reducer)

def run(runid,seed,hp):
 db=init(runid,seed,hp)
 command(db,'START',{'actor':'F2'})
 st,_,_=core.load(db);command(db,'AOO_CHAIN',{'path_distance_m':1.5,'voluntary':True,'order':['A','F1'],'tapes':[tape(st,'A'),tape(st,'F1')]})
 st,_,_=core.load(db)
 if st['actors']['F2']['resource']['hp']>0:command(db,'PASS',{'actor':'F2'});command(db,'END',{'actor':'F2'})
 st,h,rev=core.load(db)
 with sqlite3.connect(db) as con:rows=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
 ev=[x for row in rows for x in row['detail']['native_actions']]
 with sqlite3.connect(db) as src,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as cp:src.backup(cp)
 assert core.load(db)==core.load(db.with_suffix('.checkpoint.sqlite'))
 return {'run_id':runid,'seed':seed,'rev':rev,'initial_F2_hp':hp,'final_F2_hp':st['actors']['F2']['resource']['hp'],
   'aoo_order_actual':[x['from'] for x in ev if x['action']=='weapon_attack'],
   'aoo_attempts':sum(x['action']=='weapon_attack' for x in ev),
   'A_reaction_remaining':st['actors']['A']['resource']['reaction'],
   'F1_reaction_remaining':st['actors']['F1']['resource']['reaction'],
   'mover_destination':st['actors']['F2']['resource']['position'],
   'first_KO_aborts_rest':hp==200 and st['actors']['F2']['resource']['hp']==0,
   'phase':st['phase'],'head':h,'technical_not_source_complete_multiattack':True}
if __name__=='__main__':
 out=[run(x['id'],x['seed'],x['mover_hp']) for x in PRE['outcomes']]
 (ROOT/'R154_CONCURRENT_AOO_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 for x in out:print(x)
