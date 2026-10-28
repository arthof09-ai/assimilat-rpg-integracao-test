"""R198 MESTRE-SIDE additive source-to-R18 battle adapter: no damage or combat core reimplementation.
R193 architecture reused; strict source and roll tape, append-only sqlite R18.
Specifically a TEST physical baseline. Missing abilities / named proficiency are scoped hypotheses.
"""
from __future__ import annotations
import copy, hashlib, json, pathlib, random, sys, itertools
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
RUNTIME=ROOT.parent/'work'/'runtime'
for sub in ('native','r172','work/fusion_stage12'):sys.path.insert(0,str(RUNTIME/sub))
from vlab_effects_v08 import (Combatant,Scene,FrozenRuleEvidence,AbilitySource,ActorActionState,
    Resistances,EffectBlocked,apply_weapon_attack,begin_source_turn,end_source_turn)
import vlab_r18_interactive as r18
from r172_atomic_counter import write_checkpoint

VERSION='R198-R18-SOURCE-SCOPED-MICROBENCH-1'
PRE=json.loads((ROOT/'source/R198_PRE_REG.json').read_text())
PRE_SHA=hashlib.sha256((ROOT/'source/R198_PRE_REG.json').read_bytes()).hexdigest()
SRC197=json.loads((ROOT.parent/'work/r197/source/R197_SOURCE_SNAPSHOTS.json').read_text())
SOURCE_SHA=hashlib.sha256((ROOT.parent/'work/r197/source/R197_SOURCE_SNAPSHOTS.json').read_bytes()).hexdigest()
EXT=json.loads((ROOT/'source/R198_ACTOR_EXTENSION.json').read_text())['actors']

ACTORS={}
for z in SRC197['actors']:
 if z['id'] not in ('LIU_P5','LOBO_P1','CABRA_P1'):continue
 attack=z['attack'];hp=z['hp']
 ACTORS[z['id']]={'id':z['id'],'kind':z['kind'],'name':z['name'],'url':z['url'],'edited':z['page_last_edited_at'],
 'rank':z['rank'],'star':z['star'],'level':5+z['star'],'hp':hp,'maximum_hp':hp,'pa':z['pa'],'ca':z['ca'],
 'dex':z['stats']['DES'],'init_dice':(2,6),'initiative_bonus':z['stats']['DES']+(4 if z['id']=='LIU_P5' else 0),
 'attack_dice':tuple(attack['hit_test_dice']),
 'attack_bonus':attack['hit_flat_source'] if attack['hit_flat_source'] is not None else z['stats'][attack['hit_stat']],
 'damage_dice':tuple(map(tuple,attack['damage_dice'])),'damage_flat':attack['damage_flat'],
 'damage_tag':'cortante' if z['id']=='CABRA_P1' else 'impacto',
 'damage_tag_status':attack['damage_type'] if z['id']=='CABRA_P1' else 'LAB_PHYSICAL_IMPACT_WHERE_TYPE_UNKNOWN',
 'rd':10 if z['id']=='LIU_P5' else 15,
 'rd_status':'SOURCE_EXPLICIT_RDF10' if z['id']=='LIU_P5' else 'RULE_DERIVED_CONDITIONAL_PRATA_NORMAL',
 'attack_name':attack['name'],'ability_scope':attack['ability_note']}
for x in EXT:
 y=x.copy();y['edited']=y.pop('page_last_edited_at');ACTORS[y['id']]=y
assert set(ACTORS)=={'CAPANGA_P3','LIU_P5','LOBO_P1','CABRA_P1'}

EVIDENCE={}
ABILITY={}
for aid,a in ACTORS.items():
 src_str=json.dumps({'name':a['name'],'url':a['url'],'attack':a['attack_name'],'dice':a['damage_dice'],
 'bonus':a['attack_bonus'],'rd':a['rd'],'tag_status':a['damage_tag_status']},sort_keys=True)
 EVIDENCE[aid]=FrozenRuleEvidence(a['url'],VERSION+'-'+aid,hashlib.sha256(src_str.encode()).hexdigest(),a['edited'],'CURATED_REOPENED_NOTION_FIELDS_NOT_SIGNED_PAGE')
 ABILITY[aid]=AbilitySource(VERSION+'-ATT-'+aid,'attack','STANDARD',a['url'],EVIDENCE[aid].rule_id,'RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='EXISTING-V081-SOURCE-ONLY')

# Full attack tapes are generated BEFORE each native attack, deterministic by identity and own turn.
def dice(seed,pair,who,own_turn,label,n,faces):
 entropy=hashlib.sha256(f'{VERSION}|{seed}|{pair[0]}-{pair[1]}|{who}|{own_turn}|{label}|{n}d{faces}'.encode()).digest()
 r=random.Random(int.from_bytes(entropy,'big'));return [r.randint(1,faces) for _ in range(n)]

def roll_initiative(seed,pair):
 vals={}
 for who in pair:
  z=ACTORS[who];t=dice(seed,pair,who,0,'INIT',*z['init_dice'])
  vals[who]={'roll':t,'bonus':z['initiative_bonus'],'result':sum(t)+z['initiative_bonus'],
  'named_prof_status':'LAB_HYPOTHESIS_UNTRAINED' if who!='LIU_P5' else 'SOURCE_INSTINTO_SELVAGEM_PLUS4'}
 order=sorted(pair,key=lambda x: vals[x]['result'],reverse=True)
 return vals,None if vals[order[0]]['result']==vals[order[1]]['result'] else order

def tape(seed,pair,who,own_turn,weak):
 x=ACTORS[who]
 return {'crit':dice(seed,pair,who,own_turn,'CRIT',3,6),
         'hit':[dice(seed,pair,who,own_turn,'HIT'+str(i),*x['attack_dice']) for i in range(2 if weak else 1)],
         'damage':[dice(seed,pair,who,own_turn,'DMG'+str(i),n,f) for i,(n,f) in enumerate(x['damage_dice'])]}

def state_genesis(seed,pair):
 st=r18.initial('A',seed)
 st.update({'version_description':VERSION,'pre_reg_sha':PRE_SHA,'source_snap_sha':SOURCE_SHA,'seed':seed,
 'pair':list(pair),'phase':'INIT','round':0,'turn':0,'active':None,'order':[],
 'winner':None,'finish_reason':None,'scope':'LAB_SOURCE_PROFILE_BASIC_PHYSICAL_ATTACKS_WITH_EXPLICIT_ASSUMPTIONS',
 'position':{'contact':True,'same_layer':True,'line_of_effect':True,'movement':False,'campaign_location':False},
 'initial_hypotheses':PRE['assumptions'],'history':[],'native_events':[],
 'metrics':{'attempts':0,'hits':0,'crit_positive':0,'crit_negative':0,'damage_gross':0,'post_rd':0,'hp_loss':0,'overkill':0,'pa_spent':0},'actors':{}})
 for who in pair:
  f=ACTORS[who]
  a=Combatant(who,f['hp'],f['pa'],f['ca'],0,0,0,0,'LAB-CONTACT-ADJACENT',rank=f['rank'],maximum_hp=f['maximum_hp'],standard=0,movement=0,reaction=1)
  st['actors'][who]={'stats':{**copy.deepcopy(f),'source_attested_at':f['edited']},'resource':asdict(a)}
 return st

def scene(st):return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},
    events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance=VERSION+'-EXP-NOT-CAMPAIGN')

def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for k,c in s.actors.items():st['actors'][k]['resource']=asdict(c)

def setup(db,seed,pair):
 r18.init_db(str(db),'A',seed);st=state_genesis(seed,pair);conn=r18.connect(str(db))
 try:
  with conn:conn.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(st),))
 finally:conn.close()

def start(st,p,seq):
 if st['phase']!='INIT' or st['pre_reg_sha']!=PRE_SHA or st['source_snap_sha']!=SOURCE_SHA:raise EffectBlocked('SCOPE_DRIFT')
 pair=tuple(st['pair']);val,order=roll_initiative(st['seed'],pair)
 if order is None:raise EffectBlocked('INIT_TIE_UNRESOLVED')
 if p!={'initiative':val,'order':order,'pre_reg_sha':PRE_SHA,'source_snap_sha':SOURCE_SHA}:raise EffectBlocked('INIT_PAYLOAD_DRIFT')
 st['phase']='ACTIVE';st['order']=order;st['round']=1;st['turn']=0;st['active']=order[0];st['initiative_receipt']=val
 s=scene(st);begin_source_turn(s,st['active']);sync(st,s)
 return {'kind':'INIT_START','order':order,'results':val,'new_native_events':copy.deepcopy(s.events)}

def attack(st,p,seq):
 if st['phase']!='ACTIVE' or st['position']!={'contact':True,'same_layer':True,'line_of_effect':True,'movement':False,'campaign_location':False}:
  raise EffectBlocked('SCENE_NOT_SUPPORTED')
 who=st['active'];target=next(x for x in st['pair'] if x!=who)
 own_turn=1+sum(x['actor']==who for x in st['history']);f=ACTORS[who];dst=ACTORS[target]
 if (p.get('actor'),p.get('target'),p.get('own_turn'))!=(who,target,own_turn):raise EffectBlocked('IDENTITY_OR_TURN_DRIFT')
 s=scene(st);a=s.actors[who];d=s.actors[target]
 if a.hp<=0 or d.hp<=0 or a.standard!=1:raise EffectBlocked('KO_OR_ACTION')
 weak=a.hp>0 and 10*a.hp<a.maximum_hp
 t=tape(st['seed'],tuple(st['pair']),who,own_turn,weak)
 if p.get('roll_tape')!=t:raise EffectBlocked('ROLL_TAPE_TAMPER')
 attempts=[tuple(v) for v in t['hit']];bonus=f['attack_bonus'];score=min(map(sum,attempts))+bonus-2 if weak else sum(attempts[0])+bonus
 damage=sum(sum(x) for x in t['damage'])+f['damage_flat']
 oldlen=len(s.events)
 ev=apply_weapon_attack(s,who,target,source=ABILITY[who],state=ActorActionState(who,f['level'],a.pa,(ABILITY[who].action_id,),enemy_ids_visible=(target,)),proofs=(EVIDENCE[who],),
   roll_score=score,damage=damage,damage_tag=f['damage_tag'],rd=Resistances(general=dst['rd'],provenance=dst['rd_status']),
   damage_dice_groups=tuple(f['damage_dice']),damage_roll_groups=tuple(tuple(x) for x in t['damage']),damage_fixed_bonus=f['damage_flat'],
   critical_sequence=tuple(t['crit']),attack_roll_attempts=tuple(attempts),attack_bonus=bonus,lab_negative_critical_policy=True)
 end_source_turn(s,who)
 m=st['metrics'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE');m['damage_gross']+=ev['raw'];m['post_rd']+=ev['net'];m['hp_loss']+=ev['hp_loss_actual'];m['overkill']+=ev['overkill']
 if d.hp==0:
  st['phase']='FINISHED';st['winner']=who;st['finish_reason']='HP0_TEST';st['active']=None;end={'ko':target}
 else:
  end=r18._next_turn(st);s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 sync(st,s)
 st['history'].append({'actor':who,'target':target,'own_turn':own_turn,'event_seq':ev['seq'],'hit':ev['hit'],'critical':ev['critical'],'hp_loss':ev['hp_loss_actual']})
 return {'kind':'SOURCE_SCOPED_BASIC_ATTACK','from':who,'to':target,'own_turn':own_turn,'tape':t,
         'source_page':f['url'],'target_page':dst['url'],'attack':ev,'events_added':copy.deepcopy(s.events[oldlen:]),
         'resources':{x:{'hp':y.hp,'pa':y.pa,'reaction':y.reaction,'standard':y.standard} for x,y in s.actors.items()},'next_turn':end}

def run_one(root,seed,pair,group):
 pair=tuple(pair);id=f'R198_{pair[0]}_VS_{pair[1]}_{seed}'
 db=pathlib.Path(root)/(id+'.sqlite')
 if db.exists():raise RuntimeError('NO_REUSE_RUN_ID')
 ir,order=roll_initiative(seed,pair)
 if order is None:return {'run_id':id,'seed':seed,'group':group,'pair':pair,'status':'PRECOMMIT_TIE_HOLD','winners':None,'db':None}
 setup(db,seed,pair)
 start_payload={'initiative':ir,'order':order,'pre_reg_sha':PRE_SHA,'source_snap_sha':SOURCE_SHA}
 r18.event_commit(str(db),'LAB-CMD-'+id+'-INIT','SOURCE_INIT_AND_POSITION',start_payload,start)
 for seq in range(PRE['scene']['maximum_attacks']):
  st,_,_=r18.load(str(db))
  if st['phase']=='FINISHED':break
  who=st['active'];dst=next(x for x in pair if x!=who)
  own_turn=1+sum(x['actor']==who for x in st['history'])
  weak=st['actors'][who]['resource']['hp']>0 and 10*st['actors'][who]['resource']['hp']<st['actors'][who]['resource']['maximum_hp']
  payload={'actor':who,'target':dst,'own_turn':own_turn,'roll_tape':tape(seed,pair,who,own_turn,weak)}
  r18.event_commit(str(db),'LAB-CMD-'+id+f'-ATK{seq+1:03d}','SOURCE_BASIC_NORMAL_ATTACK',payload,attack)
 st,head,rev=r18.load(str(db));write_checkpoint(str(db))
 outcome=st['phase'] if st['phase']=='FINISHED' else 'CENSORED_HORIZON'
 return {'run_id':id,'seed':seed,'group':group,'pair':list(pair),'status':outcome,'winner':st['winner'] if outcome=='FINISHED' else None,
 'rounds':st['round'],'metrics':st['metrics'],'hp_final':{k:v['resource']['hp'] for k,v in st['actors'].items()},
 'pa_final':{k:v['resource']['pa'] for k,v in st['actors'].items()},'commits':rev,'events':len(st['native_events']),
 'head':head,'db':db.name,'model_scope':st['scope'],'source_sha':SOURCE_SHA,'pre_reg_sha':PRE_SHA}

def run_all(outroot=None):
 out=pathlib.Path(outroot or ROOT/'evidence'/'db');out.mkdir(parents=True,exist_ok=True)
 results=[]
 for group,seeds in PRE['seeds'].items():
  for seed,pair in itertools.product(seeds,PRE['pairs']):
   res=run_one(out,seed,pair,group);results.append(res)
 path=ROOT/'evidence/R198_FIGHT_RESULTS.json';path.write_text(json.dumps(results,ensure_ascii=False,indent=2))
 print(json.dumps({'count':len(results),'status':{s:sum(z['status']==s for z in results) for s in set(z['status'] for z in results)},
 'commits':sum(z.get('commits',0) for z in results),'attacks':sum(z.get('metrics',{}).get('attempts',0) for z in results),'dbs':sum(z.get('db') is not None for z in results)}))
 return results
if __name__=='__main__':run_all()
