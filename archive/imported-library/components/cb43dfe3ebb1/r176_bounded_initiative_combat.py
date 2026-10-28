"""R176 additive entry gate + native v0.8.1 / R18 combat; never writes historical banks.
Roc still has NO certified named Initiative proficiency; this implementation proves only
an order that is invariant over *explicitly delimited* ordinary-proficiency hypotheses.
Spatial contact is a scenario precondition, not a historical campaign position.
"""
import sys, json, copy, random, hashlib, pathlib
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
for p in [ROOT/'runtime'/'work'/'fusion_stage12',ROOT/'runtime'/'native',ROOT/'runtime'/'r172']:sys.path.insert(0,str(p))
import vlab_effects_v08 as v081
assert hasattr(v081,'begin_source_turn'), 'V081 module precedence invalid'
import vlab_r18_interactive as r18
from vlab_effects_v08 import Combatant,Scene,AbilitySource,ActorActionState,FrozenRuleEvidence,EffectBlocked,Resistances,apply_weapon_attack,begin_source_turn,end_source_turn
from r172_atomic_counter import write_checkpoint
VERSION='VLAB-R176-GRIFFIN-BOUNDED-INIT-CONTACT-v1'
SEED=1760101
MATRIX={
 'AUREN':dict(name='Sikong Auren',role='ED',status='FICHA_MESTRE',page='https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02',edited='2026-09-30T23:10:35.044Z',hp=523,pa=719,ca=225,rd=35,con=48,armor=24,fort=2,reflex=2,des=164,init_prof=2,base_attack=193,damage_count=8,damage_faces=8,flat=211,speed=16,weapon='Alvorada Rachada',damage_tag='perfurante'),
 'GRIFFIN':dict(name='Grifo-Matriarca de Silica',role='BEAST_PRECREATE',status='PRECREATE_BLUEPRINT',page='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7',edited='2026-10-08T02:25:14.539Z',hp=4315,pa=4016,ca=153,rd=75,con=85,armor=0,fort=0,reflex=0,des=116,init_prof=None,base_attack=138,damage_count=20,damage_faces=10,flat=0,speed=63,weapon='Talao de Silica',damage_tag='cortante')}
PAGES={k:v['page'] for k,v in MATRIX.items()}
SCOPES={
 'AUREN':'FICHA: normal Vida523 CA225 RD fisica35 PA livre719 Iniciativa6d6+166 Lanca6d6+193 Dano8d8+211 bonus Duelista apos 2 turnos +8',
 'GRIFFIN':'BEAST-FULLSPEC-VZ-06: Grifo L3 Vida4315 CA153 RD75 Alma4016 DES116 prof geral+22 ataque Talao6d6+138 dano20d10 cortante/perfurante Padrão 0PA; Iniciativa especial desconhecida'}
PROOFS={k:FrozenRuleEvidence(v['page'],'R176-'+k+'-EXCERPT',hashlib.sha256(SCOPES[k].encode()).hexdigest(),v['edited'],'EXCERPT_POINTER_NOT_BINARY_SIGNATURE') for k,v in MATRIX.items()}
SOURCES={k:AbilitySource('R176-'+k+'-MELEE','attack','STANDARD',v['page'],PROOFS[k].rule_id,'RULE-DERIVED',required_pa=0,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081-WEAPON') for k,v in MATRIX.items()}

def deterministic_dice(seed,key,n,faces):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{faces}'.encode()).digest(),'big'))
 return [rng.randint(1,faces) for _ in range(n)]

def initiative_dice(seed,actor):
 return deterministic_dice(seed,actor+'-INIT',6,6)

def proof_of_order(seed):
 a=initiative_dice(seed,'AUREN');g=initiative_dice(seed,'GRIFFIN')
 a_score=sum(a)+164+2;gr_min=sum(g)+116;gr_max=gr_min+22
 if a_score>gr_max:order=['AUREN','GRIFFIN'];verdict='UNAMBIGUOUS_UNDER_BOUNDED_HYPOTHESES'
 elif gr_min>a_score:order=['GRIFFIN','AUREN'];verdict='UNAMBIGUOUS_UNDER_BOUNDED_HYPOTHESES'
 else:order=None;verdict='HOLD_INITIATIVE_OVERLAP'
 return {'AUREN':{'dice':a,'score':a_score,'source_bonus':2},'GRIFFIN':{'dice':g,'min':gr_min,'max':gr_max,'unresolved_specific_prof':True,'ordinary_proficiency_cap':22},'order':order,'verdict':verdict,'hypothesis':'INIT_BONUS_IN_[0,22]_NO_EXTRA_EXTERNAL_MODIFIERS','NOT':'CERTIFIED_GRIFFIN_INIT_BONUS'}

def tape(seed,who,turn):
 f=MATRIX[who]
 return {'critical':deterministic_dice(seed,f'{who}-TURN{turn}-CRIT',3,6),
 'hit':deterministic_dice(seed,f'{who}-TURN{turn}-HIT',6,6),
 'hit_weak':deterministic_dice(seed,f'{who}-TURN{turn}-HIT-WEAK',6,6),
 'damage':deterministic_dice(seed,f'{who}-TURN{turn}-DAMAGE',f['damage_count'],f['damage_faces'])}

def geometry_gate(geo):
 return (geo.get('scenario_frozen') is True and
    geo.get('relation')=='HITBOX_CONTACT' and geo.get('same_vertical_contact_layer') is True and
    geo.get('moving') is False and geo.get('range_policy')=='CONTACT_ONLY_NO_METRIC_REACH_INFERRED')

def init_state(seed,contact=True):
 st=r18.initial('A',seed)
 st.update({'r176_version':VERSION,'r176_seed_status':'DEVELOPMENT_FROZEN_BEFORE_DICE',
            'r176_unknown':['GRIFFIN_INIT_SKILL_SPECIFIC','GRIFFIN_NOT_PHYSICALLY_PROMOTED','NATURAL_ENCOUNTER_GEOMETRY','COMPLETE_BEHAVIOR_AND_ABILITIES_NOT_EXERCISED'],
            'source_status':'PRECREATE_SOURCE_SCOPED_PHYSICAL_ONLY_NOT_BENCHMARK',
            'source_confidence':'SOURCE_MATH_VERIFIED_SPATIAL_EXPERIMENTAL',
            'r176_geometry':{'scenario_frozen':True,'relation':'HITBOX_CONTACT' if contact else 'DISJOINT',
                'same_vertical_contact_layer':True,'moving':False,'range_policy':'CONTACT_ONLY_NO_METRIC_REACH_INFERRED',
                'plane':'LAB_TEST_NEUTRAL_SURFACE','canonical_reach_metres':None,'no_flying_bonus':True},
            'r176_initiative':None,'r176_events':[],'r176_history':[],
            'r176_counts':{'attempts':0,'hits':0,'post_rd':0,'hp_loss':0,'overkill':0,'crit_positive':0,'crit_negative':0,'pa_spent':0,'reactions_spent':0},
            'phase':'INIT','round':0,'turn':0,'active':None,'order':[],'actors':{},'winner':None,'finish_reason':None})
 for who,f in MATRIX.items():
  c=Combatant(who,f['hp'],f['pa'],f['ca'],f['con'],f['armor'],f['fort'],f['reflex'],'R176_EXPERIMENTAL_CONTACT',rank='Lendario',maximum_hp=f['hp'],base_speed=f['speed'],standard=0,movement=0,reaction=1)
  st['actors'][who]={'name':f['name'],'stats':{'source':f['page'],'edited':f['edited'],'role':f['role'],'status':f['status'],'rank':'Lendario 3','attack_bonus':f['base_attack'],'physical_rd':f['rd'],'weapon':f['weapon'],'initiative_named_prof':f['init_prof'],'des':f['des']},'resource':asdict(c)}
 return st

def native_scene(st):
 return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['r176_events']),seed=st['seed'],provenance='R176_CONTACT_INIT_BOUNDED_SOURCE_SCOPE_TEST')

def sync(st,s):
 st['r176_events']=copy.deepcopy(s.events)
 for k,v in s.actors.items():st['actors'][k]['resource']=asdict(v)

def setup(db,seed=SEED,contact=True):
 r18.init_db(db,'A',seed)
 c=r18.connect(db)
 try:
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(init_state(seed,contact)),))
 finally:c.close()

def start(st,p,seq):
 if st['phase']!='INIT':raise EffectBlocked('ALREADY_STARTED')
 if not geometry_gate(st['r176_geometry']):raise EffectBlocked('SPATIAL_PREFLIGHT_HOLD_NOT_CONTACT')
 proof=proof_of_order(st['seed'])
 if p.get('initiative')!=proof or p.get('seed')!=st['seed'] or proof['order'] is None:raise EffectBlocked('INIT_PROVENANCE_OR_BOUNDS_HOLD')
 st['r176_initiative']=proof;st['order']=list(proof['order']);st['phase']='ACTIVE';st['round']=1;st['turn']=0;st['active']=proof['order'][0]
 s=native_scene(st);e=begin_source_turn(s,st['active']);sync(st,s)
 return {'kind':'BOUNDED_INITIATIVE_SOURCE_GATED','initiative':proof,'order':st['order'],'geometry':copy.deepcopy(st['r176_geometry']),'native_events':[e],
         'warning':'Griffin initiative skill unknown; order certified ONLY under ordinary +0..+22 bounded hypothesis'}

def attack(st,p,seq):
 if st['phase']!='ACTIVE' or not geometry_gate(st['r176_geometry']):raise EffectBlocked('ACTOR_OR_GEOMETRY_HOLD')
 actor=st['active'];target='GRIFFIN' if actor=='AUREN' else 'AUREN'
 if (p.get('actor')!=actor or p.get('target')!=target or p.get('seed')!=st['seed']):raise EffectBlocked('IDENTITY')
 turn=1+sum(h['actor']==actor for h in st['r176_history'])
 if p.get('turn_number')!=turn or p.get('tape')!=tape(st['seed'],actor,turn):raise EffectBlocked('RNG_TAPE_NOT_FROZEN')
 scene=native_scene(st);src=SOURCES[actor];f=MATRIX[actor];fd=MATRIX[target];a=scene.actors[actor];d=scene.actors[target]
 if a.standard!=1 or a.hp<=0 or d.hp<=0:raise EffectBlocked('ACTION_SLOT_OR_KO')
 t=p['tape'];weak=a.hp*10<f['hp'];tries=(tuple(t['hit']),tuple(t['hit_weak'])) if weak else (tuple(t['hit']),)
 duel_bonus=8 if actor=='AUREN' and turn>=3 else 0
 atk_bonus=f['base_attack']+duel_bonus
 score=(min(map(sum,tries))+atk_bonus-2) if weak else sum(t['hit'])+atk_bonus
 raw=sum(t['damage'])+f['flat'];start_at=len(scene.events)
 ev=apply_weapon_attack(scene,actor,target,source=src,state=ActorActionState(actor,23,a.pa,(src.action_id,),enemy_ids_visible=(target,)),
    proofs=(PROOFS[actor],),roll_score=score,damage=raw,damage_tag=f['damage_tag'],rd=Resistances(general=fd['rd'],provenance='SOURCE_PHYSICAL_RD'),
    damage_dice_groups=((f['damage_count'],f['damage_faces']),),damage_roll_groups=(tuple(t['damage']),),damage_fixed_bonus=f['flat'],
    critical_sequence=tuple(t['critical']),attack_roll_attempts=tries,attack_bonus=atk_bonus,lab_negative_critical_policy=True)
 end_source_turn(scene,actor)
 m=st['r176_counts'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['post_rd']+=ev['net'];m['hp_loss']+=ev['hp_loss_actual'];m['overkill']+=ev['overkill'];m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE')
 if d.hp<=0:
  st['phase']='FINISHED';st['winner']=actor;st['active']=None;st['finish_reason']='HP_ZERO_TEST_ONLY';scheduler={'ko':target,'next_turn':None}
 else:
  scheduler=r18._next_turn(st);upcoming=st['active'];scene.actors[upcoming].standard=0;begin_source_turn(scene,upcoming)
 sync(st,scene)
 detail={'actor':actor,'target':target,'actor_turn':turn,'tape':copy.deepcopy(t),'source_page':f['page'],'target_page':fd['page'],
         'mechanical_title_bonus':duel_bonus,'geometry_preflight':'HITBOX_CONTACT','attack':copy.deepcopy(ev),
         'new_native_events':copy.deepcopy(scene.events[start_at:]),'HP_after':{k:v.hp for k,v in scene.actors.items()},
         'PA_after':{k:v.pa for k,v in scene.actors.items()},'reactions_after':{k:v.reaction for k,v in scene.actors.items()},'scheduler':scheduler}
 st['r176_history'].append({'seq':seq,'actor':actor,'target':target,'net':ev['net'],'HP_after':detail['HP_after']})
 return detail

def fight(out_dir,seed=SEED,max_attacks=140):
 out_dir=pathlib.Path(out_dir);out_dir.mkdir(parents=True,exist_ok=True)
 db=out_dir/f'R176_AUREN_GRIFFIN_INIT_BOUNDED_DEV{seed}.sqlite'
 setup(db,seed)
 r18.event_commit(db,f'LAB-CMD-R176-GRIFFIN-{seed}-INIT','R176_INITIATIVE_AND_CONTACT',{'seed':seed,'initiative':proof_of_order(seed)},start)
 for i in range(max_attacks):
  st,_,_=r18.load(db)
  if st['phase']=='FINISHED':break
  who=st['active'];target='GRIFFIN' if who=='AUREN' else 'AUREN';turn=1+sum(h['actor']==who for h in st['r176_history'])
  r18.event_commit(db,f'LAB-CMD-R176-GRIFFIN-{seed}-ATK-{i+1:04d}','R176_PHYSICAL_CONTACT_ATTACK',
     {'actor':who,'target':target,'seed':seed,'turn_number':turn,'tape':tape(seed,who,turn)},attack)
 st,head,rev=r18.load(db);write_checkpoint(db)
 if st['phase']!='FINISHED':raise RuntimeError('CENSORED_HORIZON_NEEDS_REPORT')
 return {'database':db.name,'phase':st['phase'],'winner':st['winner'],'rounds':st['round'],'counts':st['r176_counts'],'hp_final':{k:v['resource']['hp'] for k,v in st['actors'].items()},'pa_final':{k:v['resource']['pa'] for k,v in st['actors'].items()},'commits':rev,'native_events':len(st['r176_events']),'head':head,'initiative':st['r176_initiative']}

if __name__=='__main__':
 import argparse
 pa=argparse.ArgumentParser();pa.add_argument('directory');args=pa.parse_args()
 print(json.dumps(fight(args.directory),indent=2,ensure_ascii=False))
