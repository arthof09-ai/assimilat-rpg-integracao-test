"""R175: Auren (documented ED) x Roc (documented precreation Besta) physical-only TEST.
R18 SQLite event_commit and v0.8.1 apply_weapon_attack are preserved. Two exogenous
initiative-order sensitivity branches (NOT 2 independent observations). No claims
of full admissibility: Roc initiative proficiency and starting geometry UNKNOWN.
"""
import pathlib, sys, json, hashlib, random, copy
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
R173=ROOT/'deps/r173_work'
for folder in (R173/'r172_work',R173/'deps/r61_extracted/work/fusion_stage12',R173,R173/'deps/native_v081_controlled'):
 sys.path.insert(0,str(folder))
import vlab_effects_v08 as native
import vlab_r18_interactive as r18
import r172_atomic_counter as r172
from vlab_effects_v08 import Combatant,Scene,AbilitySource,ActorActionState,FrozenRuleEvidence,EffectBlocked,Resistances,apply_weapon_attack,begin_source_turn,end_source_turn
VERSION='VLAB-R175-ED-BE-SOURCE-PHYSICAL-TEST-v1'
SEED=1750101
ACTORS={
 'AUREN':dict(name='Sikong Auren',role='ED',status='FICHA_MESTRE',rank='Lendario 3',page='https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02',edited='2026-09-30T23:10:35.044Z',hp=523,pa=719,ca=225,rd=35,con=48,armor=24,fort=2,reflex=2,initiative='6d6+166',attack_bonus=193,damage_count=8,damage_faces=8,flat=211,speed=16,weapon='Alvorada Rachada',damage_tag='perfurante'),
 'ROC':dict(name='Roc da Tempestade de Vidro',role='BESTA',status='PRECREATE_BLUEPRINT',rank='Lendario 3',page='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7',edited='2026-10-08T02:25:14.539Z',hp=4200,pa=3740,ca=164,rd=75,con=80,armor=0,fort=0,reflex=0,initiative=None,attack_bonus=150,damage_count=20,damage_faces=10,flat=0,speed=66,weapon='Talao de Vidro',damage_tag='cortante')}
EXCERPTS={
 'AUREN':'Espiritualista Demoníaco Lendário 3 Espírito Falcão Meio Dia | Vida523 | CA225 | RD físico35 | PA livre719 | Iniciativa 6d6+166 | Lança em duelo 6d6+193 | Dano lança 8d8+211 | equipamento Alvorada Rachada',
 'ROC':'BEAST-FULLSPEC-VZ-06 Roc Tempestade de Vidro L3 | Vida4200 | Alma3740 | CA164 | RD75 | Velocidade66 | DES128 | Ataque físico 6d6+150 com DES em talão | Talão de Vidro Padrão 0 PA 20d10 cortante/perfurante | iniciativa específica NÃO fornecida'}
PROOFS={k:FrozenRuleEvidence(v['page'],'R175-'+k+'-PHYSICAL',hashlib.sha256(EXCERPTS[k].encode()).hexdigest(),v['edited'],'EXCERPT_POINTER_NOT_BINARY_NOTION_SIGNATURE') for k,v in ACTORS.items()}
SRC={k:AbilitySource('R175-'+k+'-ATTACK','attack','STANDARD',f['page'],PROOFS[k].rule_id,'RULE-DERIVED',required_pa=0,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081-WEAPON') for k,f in ACTORS.items()}

def dice(seed,key,n,faces):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{faces}'.encode()).digest(),'big'))
 return [rng.randint(1,faces) for _ in range(n)]
def tape(seed,actor,n):
 f=ACTORS[actor];return {'critical':dice(seed,f'{actor}-TURN{n}-CRIT',3,6),
   'hit':dice(seed,f'{actor}-TURN{n}-HIT',6,6),
   'hit_weak':dice(seed,f'{actor}-TURN{n}-HIT-WEAK',6,6),
   'damage':dice(seed,f'{actor}-TURN{n}-DAMAGE',f['damage_count'],f['damage_faces'])}
def init_state(seed,order):
 if order not in ('AUREN_FIRST','ROC_FIRST'):raise ValueError('order')
 st=r18.initial('A',seed)
 st.update({'r175_version':VERSION,'synthetic':True,'source_status':'SOURCE_DOCUMENTED_ED_AND_PRECREATE_BE_SCOPE_CONDITIONAL',
 'source_confidence':'SOURCE_SCOPED_PHYSICAL_ONLY_NOT_FULL_ADMISSIBLE','r175_order_branch':order,
 'r175_unknown':['ROC_INITIATIVE_SKILL_PROFICIENCY','GEOMETRY_SOURCE_OF_INITIAL_ADJACENCY','FULL_ABILITY_REPERTOIRE_NOT_EXERCISED','NO_FORMAL_SOURCE_PROMOTION'],
 'r175_seed_type':'DEV_ONE_SEED_TWO_ORDER_SENSITIVITY_BRANCHES','r175_native_events':[],
 'r175_history':[],'r175_counts':{'attempts':0,'hits':0,'post_rd':0,'hp_loss':0,'overkill':0,'crit_positive':0,'crit_negative':0,'pa_spent':0,'reactions_spent':0},
 'phase':'INIT','actors':{},'round':0,'turn':0,'order':[],'active':None,'winner':None,'finish_reason':None})
 for who,f in ACTORS.items():
  actor=Combatant(who,f['hp'],f['pa'],f['ca'],f['con'],f['armor'],f['fort'],f['reflex'],'EXPERIMENTAL_ADJACENT_CONTACT',rank='Lendario',maximum_hp=f['hp'],base_speed=f['speed'],standard=0,movement=0,reaction=1)
  st['actors'][who]={'name':f['name'],'stats':{'source':f['page'],'edit_time':f['edited'],'role':f['role'],'status':f['status'],'rank':f['rank'],'attack_bonus':f['attack_bonus'],'physical_rd':f['rd'],'weapon':f['weapon'],'initiative':f['initiative']},'resource':asdict(actor)}
 return st

def scene_of(st):
 return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['r175_native_events']),seed=st['seed'],provenance='R175_ED_VS_PRECREATE_BE_CONDITIONAL_MESTRE_SIDE_TEST')
def sync(st,scene):
 st['r175_native_events']=copy.deepcopy(scene.events)
 for k,v in scene.actors.items():st['actors'][k]['resource']=asdict(v)

def init_db(db,seed,order):
 r18.init_db(db,'A',seed)
 con=r18.connect(db)
 try:
  with con:con.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(init_state(seed,order)),))
 finally:con.close()

def start(st,p,seq):
 if st['phase']!='INIT':raise EffectBlocked('already started')
 if p['order']!=st['r175_order_branch']:raise EffectBlocked('init changed')
 st['order']=['AUREN','ROC'] if p['order']=='AUREN_FIRST' else ['ROC','AUREN']
 st['phase']='ACTIVE';st['round']=1;st['turn']=0;st['active']=st['order'][0]
 s=scene_of(st); ev=begin_source_turn(s,st['active']);sync(st,s)
 return {'kind':'EXOGENOUS_INIT_ORDER_SENSITIVITY','order':st['order'],'roc_initiative_proficiency':'UNKNOWN','auren_initiative_formula':'6d6+166','native_events':[ev],'official':False}

def attack(st,p,seq):
 if st['phase']!='ACTIVE':raise EffectBlocked('not active')
 actor=st['active'];defender='AUREN' if actor=='ROC' else 'ROC'
 if p['actor']!=actor or p['target']!=defender or p['seed']!=st['seed']:raise EffectBlocked('identity')
 n=sum(1 for h in st['r175_history'] if h['actor']==actor)+1
 if p['actor_turn']!=n or p['tape']!=tape(st['seed'],actor,n):raise EffectBlocked('roll tape spoof')
 f=ACTORS[actor];fd=ACTORS[defender];t=p['tape'];s=scene_of(st);a=s.actors[actor];d=s.actors[defender]
 if a.standard!=1 or not a.hp or not d.hp:raise EffectBlocked('illegal turn')
 weakness=a.hp*10<f['hp'];attempts=(tuple(t['hit']),tuple(t['hit_weak'])) if weakness else (tuple(t['hit']),)
 score=min(map(sum,attempts))+f['attack_bonus']-2 if weakness else sum(t['hit'])+f['attack_bonus']
 raw=sum(t['damage'])+f['flat']
 start_idx=len(s.events)
 ev=apply_weapon_attack(s,actor,defender,source=SRC[actor],state=ActorActionState(actor,23,a.pa,(SRC[actor].action_id,),enemy_ids_visible=(defender,)),proofs=(PROOFS[actor],),roll_score=score,damage=raw,damage_tag=f['damage_tag'],rd=Resistances(general=fd['rd'],provenance='SOURCE_RD_PHYSICAL'),damage_dice_groups=((f['damage_count'],f['damage_faces']),),damage_roll_groups=(tuple(t['damage']),),damage_fixed_bonus=f['flat'],critical_sequence=tuple(t['critical']),attack_roll_attempts=attempts,attack_bonus=f['attack_bonus'],lab_negative_critical_policy=True)
 end_source_turn(s,actor)
 m=st['r175_counts'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['post_rd']+=ev['net'];m['hp_loss']+=ev['hp_loss_actual'];m['overkill']+=ev['overkill'];m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE')
 if d.hp==0:
  st['phase']='FINISHED';st['active']=None;st['winner']=actor;st['finish_reason']='HP_ZERO_TEST_ONLY'
  scheduling={'ko':defender,'next':None}
 else:
  scheduling=r18._next_turn(st)
  next_actor=st['active'];s.actors[next_actor].standard=0
  start_ev=begin_source_turn(s,next_actor)
  scheduling['native_turn_start_seq']=start_ev['seq']
 sync(st,s)
 detail={'actor':actor,'target':defender,'source_page':f['page'],'target_page':fd['page'],'actor_turn':n,'tape':t,'attack':copy.deepcopy(ev),'new_native_events':copy.deepcopy(s.events[start_idx:]),'HP_after':{k:v.hp for k,v in s.actors.items()},'PA_after':{k:v.pa for k,v in s.actors.items()},'reactions_after':{k:v.reaction for k,v in s.actors.items()},'scheduler':scheduling,'source_status':st['source_status']}
 st['r175_history'].append({'seq':seq,'actor':actor,'hit':ev['hit'],'crit':ev['critical'],'net':ev['net'],'hp_loss':ev['hp_loss_actual'],'overkill':ev['overkill'],'HP_after':detail['HP_after']})
 return detail

def run(directory,order,seed=SEED,max_turns=110):
 directory=pathlib.Path(directory);directory.mkdir(parents=True,exist_ok=True)
 db=directory/f'R175_AUREN_ROC_{order}_DEV{seed}.sqlite'
 init_db(db,seed,order)
 r18.event_commit(db,f'LAB-CMD-R175-{order}-INIT','R175_SOURCE_START',{'order':order},start)
 for idx in range(max_turns):
  st,_,_=r18.load(db)
  if st['phase']=='FINISHED':break
  who=st['active'];n=sum(1 for h in st['r175_history'] if h['actor']==who)+1
  params={'actor':who,'target':'AUREN' if who=='ROC' else 'ROC','seed':seed,'actor_turn':n,'tape':tape(seed,who,n)}
  r18.event_commit(db,f'LAB-CMD-R175-{order}-{idx+1:04d}','R175_SOURCE_PHYSICAL_ATTACK',params,attack)
 st,head,revision=r18.load(db)
 r172.write_checkpoint(db)
 return db,st,head,revision

if __name__=='__main__':
 out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
 for o in ('AUREN_FIRST','ROC_FIRST'):
  db,st,head,rev=run(out,o)
  print(json.dumps({'db':db.name,'phase':st['phase'],'winner':st['winner'],'round':st['round'],'attacks':st['r175_counts'],'HP':{a:v['resource']['hp'] for a,v in st['actors'].items()},'PA':{a:v['resource']['pa'] for a,v in st['actors'].items()},'head':head,'revision':rev},ensure_ascii=False))
