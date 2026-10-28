"""R187–R196: additive source-uncertainty experiment using existing v0.8.1+R18.
Liu and Concha are existing Mestre pages. Two unassigned Concha named skills
and Liu Iniciativa are HYPOTHESES, not silently assigned values. Damage typing of
Liu aggregate and Concha bite remains a scenario assumption. No official combat.
"""
import json,sys,copy,random,hashlib,pathlib,itertools
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[2]/'work'
for path in [ROOT/'runtime/r172',ROOT/'runtime/work/fusion_stage12',ROOT/'runtime/native']:
 sys.path.insert(0,str(path))
from vlab_effects_v08 import Combatant,Scene,FrozenRuleEvidence,AbilitySource,ActorActionState,Resistances,EffectBlocked,apply_weapon_attack,begin_source_turn,end_source_turn
import vlab_r18_interactive as r18
from r172_atomic_counter import write_checkpoint
BASE=pathlib.Path(__file__).resolve().parents[1]
PRE=(BASE/'R193_PRE_REGISTRATION.json').read_bytes()
PRESHA=hashlib.sha256(PRE).hexdigest()
VER='R187-R196-MATERIALIZED-BEAST-LIU-CONCHA-V1'
S={
 'LIU': {'name':'Liu Xiaua','role':'ED_PERSONAGEM_MESTRE','level':10,'rank':'Prata 5','page':'https://app.notion.com/p/0b4c2b324ede837cb6be818dc8e36010','edited':'2026-10-01T09:40:50.721Z','hp':235,'pa':73,'ca':46,'rd':10,'dex':16,'rank_dice':2,'init_special':4,'atk_flat':37,'damage_groups':((5,12),(3,8),(1,6)),'damage_flat':45,'tag':'impacto','source_attack':'H - Ataque Basico 2d6+37 (5d12+3d8+1d6+45)','damage_tag_status':'LAB_ASSUMED_PHYSICAL_AGGREGATE_NOT_CERTIFIED'},
 'CONCHA':{'name':'Concha Marinha Luminosa','role':'BEAST_MATERIALIZED_NOT_SPECIFIC_INITIATIVE','level':6,'rank':'Prata 1','page':'https://app.notion.com/p/474c2b324ede82d08ea6819069c17043','edited':'2026-10-01T18:00:38.140Z','hp':210,'pa':70,'ca':40,'rd':15,'dex':27,'rank_dice':2,'init_special':0,'atk_flat':30,'damage_groups':((3,6),),'damage_flat':30,'tag':'perfurante','source_attack':'Mordida: 3d6+FOR; FOR 30; rank Prata1 2d6','damage_tag_status':'LAB_ASSUMED_BITE_PHYSICAL_PERFURANTE_NOT_LITERAL'}
}
EXCERPTS={
'LIU': 'Liu Xiaua Prata5 Vida235 Alma73 CA46 RDF10 DES16 Iniciativa(Des) listed; Instinto Selvagem +4 iniciativa; Ataque Basico 2d6+37 / 5d12+3d8+1d6+45; source 2026-10-01',
'CONCHA':'Concha Marinha Luminosa Prata1 Vida210 Alma70 CA40 FOR30 DES27 CON15 Mordida3d6+FOR; Criação de Besta normal Prata RD15, specific Luta/Iniciativa absent; source 2026-10-01'
}
P={k:FrozenRuleEvidence(v['page'],VER+'-'+k,hashlib.sha256(EXCERPTS[k].encode()).hexdigest(),v['edited'],'REOPENED_NOTION_CURATED_EXCERPT_NOT_BINARY_SIGNATURE') for k,v in S.items()}
A={k:AbilitySource(VER+'-ATT-'+k,'attack','STANDARD',v['page'],P[k].rule_id,'RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='EXISTING-V081-SOURCE-ONLY') for k,v in S.items()}

def dice(seed,who,turn,label,count,faces):
 h=hashlib.sha256(f'{VER}|{seed}|{who}|{turn}|{label}|{count}d{faces}'.encode()).digest()
 r=random.Random(int.from_bytes(h,'big'))
 return [r.randint(1,faces) for _ in range(count)]

def initial_roll(seed,li,bi):
 lr=dice(seed,'LIU',0,'INIT',2,6); br=dice(seed,'CONCHA',0,'INIT',2,6)
 lv=sum(lr)+S['LIU']['dex']+4+li;bv=sum(br)+S['CONCHA']['dex']+bi
 return {'LIU':{'dice':lr,'score':lv,'initiative_special':4,'named_prof_hypothesis':li},'CONCHA':{'dice':br,'score':bv,'named_prof_hypothesis':bi},'tie':lv==bv,'order':(['LIU','CONCHA'] if lv>bv else ['CONCHA','LIU']) if lv!=bv else None}

def geometry():return {'scene_test_only':True,'contact':True,'same_layer':True,'line_of_effect':True,'motion':False,'numeric_reach':None,'policy':'EXPLICIT_MELEE_CONTACT_NO_MOVEMENT','not_campaign_location':True}

def initial(seed,lis,con_i,con_l):
 st=r18.initial('A',seed)
 st.update({'version_description':VER,'pre_reg_sha':PRESHA,'phase':'INIT','winner':None,'end_reason':None,'round':0,'turn':0,'order':[],'active':None,'rolls':None,'geometry':geometry(),'branch':{'liu_named_init':lis,'concha_named_init':con_i,'concha_named_luta':con_l},'history':[],'native_events':[],'scene_category':'ED_VS_MATERIALIZED_BEAST_TEST_WITH_UNDECIDED_PROFICIENCIES_AND_PHYSICAL_TAGS', 'unknowns':['CONCHA_INITIATIVE_TRAINING','CONCHA_LUTA_TRAINING','LIU_INITIATIVE_TRAINING_MARKUP','SOURCE_COMPOSITE_DAMAGE_TAGS','CANONICAL_MATERIALIZED_BEAST_STATUS_NOT_CAMPAIGN_ENCOUNTER'], 'metrics':{'attempts':0,'hits':0,'brut':0,'post_rd':0,'hp_loss':0,'overkill':0,'critical_pos':0,'critical_neg':0},'actors':{}})
 for who,f in S.items():
  c=Combatant(who,f['hp'],f['pa'],f['ca'],0,0,0,0,'TEST-CONTACT-ADJACENT',rank='Prata',maximum_hp=f['hp'],standard=0,movement=0,reaction=1)
  st['actors'][who]={'stats':{'name':f['name'],'role':f['role'],'page':f['page'],'edited':f['edited'],'rank':f['rank'],'source_attack':f['source_attack'],'rd':f['rd'],'rd_authority':'SOURCE_EXPLICIT' if who=='LIU' else 'RULE_DERIVED_PRATA_NORMAL','damage_tag_scope':f['damage_tag_status']},'resource':asdict(c)}
 return st

def gate_geometry(g):
 return g==geometry() and g['contact'] and g['same_layer'] and g['line_of_effect'] and not g['motion']

def scene(st):return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R187-R196-SOURCE-EXPLICIT-LIU-CONCHA-TEST')

def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for k,v in s.actors.items():st['actors'][k]['resource']=asdict(v)

def setup(db,seed,lis,bi,bl):
 r18.init_db(str(db),'A',seed)
 st=initial(seed,lis,bi,bl);c=r18.connect(str(db))
 try:
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(st),))
 finally:c.close()

def start(st,p,seq):
 if st['phase']!='INIT' or not gate_geometry(st['geometry']):raise EffectBlocked('R193_GEOMETRY_NOT_EXPLICIT_CONTACT')
 x=initial_roll(st['seed'],st['branch']['liu_named_init'],st['branch']['concha_named_init'])
 if x['tie']:raise EffectBlocked('INITIATIVE_TIE_RULE_NOT_DOCUMENTED')
 if p!={'initiative':x,'geometry':st['geometry'],'pre_reg_sha':PRESHA}:raise EffectBlocked('INIT_SOURCE_PAYLOAD_DRIFT')
 st['phase']='ACTIVE';st['order']=x['order'];st['round']=1;st['turn']=0;st['active']=x['order'][0];st['rolls']=x
 s=scene(st);s.actors[st['active']].standard=0;ev=begin_source_turn(s,st['active']);sync(st,s)
 return {'kind':'INIT_AND_SOURCE_SCOPE_START','initiative':x,'geometry':geometry(),'new_native_events':[ev]}

def roll_tape(seed,who,turn,weak):
 f=S[who]
 return {'crit':dice(seed,who,turn,'CRIT',3,6), 'hit':dice(seed,who,turn,'HIT',2,6), 'hit_weak':dice(seed,who,turn,'WEAK',2,6), 'damage':[dice(seed,who,turn,'DAMAGE'+str(i),n,faces) for i,(n,faces) in enumerate(f['damage_groups'])]}

def attack(st,p,seq):
 if st['phase']!='ACTIVE' or not gate_geometry(st['geometry']):raise EffectBlocked('SCOPE_NOT_ADMISSIBLE')
 who=st['active'];other='CONCHA' if who=='LIU' else 'LIU';f=S[who];target=S[other]
 turn=1+sum(h['actor']==who for h in st['history'])
 if p.get('actor')!=who or p.get('target')!=other or p.get('turn_number')!=turn or p.get('branch')!=st['branch']:raise EffectBlocked('ACTOR_IDENTITY_DRIFT')
 s=scene(st);actor=s.actors[who];defender=s.actors[other]
 if actor.standard!=1 or actor.hp<=0 or defender.hp<=0:raise EffectBlocked('ACTION_OR_KO')
 weak=10*actor.hp<actor.maximum_hp
 tape=roll_tape(st['seed'],who,turn,weak)
 if tape!=p.get('tape'):raise EffectBlocked('TAPE_DRIFT')
 bonus=f['atk_flat']+(st['branch']['concha_named_luta'] if who=='CONCHA' else 0)
 attempts=[tuple(tape['hit']),tuple(tape['hit_weak'])] if weak else [tuple(tape['hit'])]
 score=(min(map(sum,attempts))+bonus-2) if weak else (sum(tape['hit'])+bonus)
 damage=sum(map(sum,tape['damage']))+f['damage_flat']
 ev_index=len(s.events)
 ev=apply_weapon_attack(s,who,other,source=A[who],state=ActorActionState(who,f['level'],actor.pa,(A[who].action_id,),enemy_ids_visible=(other,)),proofs=(P[who],),roll_score=score,damage=damage,damage_tag=f['tag'],rd=Resistances(general=target['rd'],provenance=('SOURCE_LITERAL_RDF10' if other=='LIU' else 'RULE_DERIVED_CR_BESTA_PRATA15')),
 damage_dice_groups=f['damage_groups'],damage_roll_groups=tuple(tuple(x) for x in tape['damage']),damage_fixed_bonus=f['damage_flat'],critical_sequence=tuple(tape['crit']),attack_roll_attempts=tuple(attempts),attack_bonus=bonus,lab_negative_critical_policy=True)
 end_source_turn(s,who)
 m=st['metrics'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['brut']+=ev['raw'];m['post_rd']+=ev['net'];m['hp_loss']+=ev['hp_loss_actual'];m['overkill']+=ev['overkill'];m['critical_pos']+=int(ev['critical']=='POSITIVE');m['critical_neg']+=int(ev['critical']=='NEGATIVE')
 if defender.hp==0:
  st['phase']='FINISHED';st['winner']=who;st['end_reason']='HP0_TEST_ONLY';st['active']=None;nextturn={'ko':other,'next_turn':None}
 else:
  nextturn=r18._next_turn(st);s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 sync(st,s)
 st['history'].append({'actor':who,'target':other,'turn':turn,'event_seq':ev['seq'],'hit':ev['hit'],'hp_loss':ev['hp_loss_actual']})
 return {'kind':'PHYSICAL_NORMAL_ATTACK_WITH_HYPOTHESIS_SKILL','actor':who,'target':other,'actor_turn':turn,'source_page':f['page'],'target_page':target['page'],'tape':tape,'attack':ev,'new_native_events':copy.deepcopy(s.events[ev_index:]),'nextturn':nextturn,'hp_after':{k:v.hp for k,v in s.actors.items()},'pa_after':{k:v.pa for k,v in s.actors.items()},'branch':st['branch']}

def fight(out,seed,li,bi,bl,max_attacks=30):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
 branch=f'LI{li}_BI{bi}_BL{bl}'
 db=out/f'R193_LIU_CONCHA_SEED{seed}_{branch}.sqlite'
 if db.exists():raise RuntimeError('NO_RUN_ID_REUSE')
 st=initial(seed,li,bi,bl);init=initial_roll(seed,li,bi)
 if init['tie']:
  return {'seed':seed,'branch':branch,'status':'PRE_COMMIT_HOLD','reason':'INITIATIVE_TIE_RULE_UNKNOWN','initiative':init,'db':None}
 setup(db,seed,li,bi,bl)
 r18.event_commit(str(db),f'LAB-CMD-R193-{seed}-{branch}-INIT','INIT_AND_SOURCE_SCOPE_START',{'initiative':init,'geometry':geometry(),'pre_reg_sha':PRESHA},start)
 for a in range(max_attacks):
  st,_,_=r18.load(str(db))
  if st['phase']!='ACTIVE':break
  who=st['active'];other='CONCHA' if who=='LIU' else 'LIU'
  turn=1+sum(h['actor']==who for h in st['history'])
  p={'actor':who,'target':other,'turn_number':turn,'branch':st['branch'],'tape':roll_tape(seed,who,turn,False)}
  r18.event_commit(str(db),f'LAB-CMD-R193-{seed}-{branch}-ATT{a+1:03d}','PHYSICAL_NORMAL_ATTACK',p,attack)
 st,head,rev=r18.load(str(db));write_checkpoint(str(db))
 return {'seed':seed,'branch':branch,'status':st['phase'],'winner':st['winner'],'rounds':st['round'],'attack_attempts':st['metrics']['attempts'],'hp_final':{k:v['resource']['hp'] for k,v in st['actors'].items()},'pa_final':{k:v['resource']['pa'] for k,v in st['actors'].items()},'metrics':st['metrics'],'commits':rev,'native_events':len(st['native_events']),'db':db.name,'head':head}

def run_all():
 pre=json.loads(PRE); out=BASE/'evidence';res=[]
 for group,seeds in pre['seeds'].items():
  for seed in seeds:
   for li,bi,bl in itertools.product((0,2),(0,8),(0,8)):
    try: r=fight(out,seed,li,bi,bl,pre['max_attacks'])
    except Exception as e:r={'seed':seed,'branch':f'LI{li}_BI{bi}_BL{bl}','status':'FAIL_CLOSED','reason':repr(e)}
    r['group']=group;res.append(r)
 (BASE/'evidence/R193_RESULTS.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
 print(json.dumps({'runs':len(res),'status_counts':{k:sum(x['status']==k for x in res) for k in sorted(set(x['status'] for x in res))},'winners':{k:sum(x.get('winner')==k for x in res) for k in ['LIU','CONCHA']},'samples':res[:8]},ensure_ascii=False,indent=2))

if __name__=='__main__':run_all()
