"""R198 magic pilot reuses R198 physical adapter (itself R193->v08->R18) and R18 commit.
Not an alternative combat/damage/magic resolver: v0.8.1 native attack resolves water hit/damage,
PA debit and a source-correlated spell_cost event are committed atomically with that result.
Attack-spell critical, cost discount and source range remain explicit TEST hypotheses.
"""
from __future__ import annotations
import copy,json,hashlib,pathlib,itertools,sys
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r198_microbenchmark as base
from vlab_effects_v08 import (AbilitySource,FrozenRuleEvidence,ActorActionState,
 apply_weapon_attack,begin_source_turn,end_source_turn,Resistances,EffectBlocked)
r18=base.r18
MAGIC_PRE=json.loads((ROOT/'source/R198_MAGIC_PRE_REG.json').read_text());MAGIC_SHA=hashlib.sha256((ROOT/'source/R198_MAGIC_PRE_REG.json').read_bytes()).hexdigest()
ONG=json.loads((ROOT/'source/R198_ONG_SOURCE.json').read_text());ONG['source_attested_at']=ONG['edited'];ONG['cost_pa']=8
# Local successor process only; no change to historical R198 records or code.
base.ACTORS['ONG_P2']=ONG
proof_label=json.dumps({k:ONG[k] for k in ['id','name','url','attack_name','edited','pa','ca']},sort_keys=True)
base.EVIDENCE['ONG_P2']=FrozenRuleEvidence(ONG['url'],'R198-ONG-MAGIC-WHIP-ATTACK',hashlib.sha256(proof_label.encode()).hexdigest(),ONG['edited'],'REOPENED_AUTHORIAL_SOURCE_LAB_SPELL_BRIDGE')
base.ABILITY['ONG_P2']=AbilitySource('R198-ONG-WHIP-SPELL-ATTACK-ADAPTER','attack','STANDARD',ONG['url'],base.EVIDENCE['ONG_P2'].rule_id,'RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081-ATTACK_SPELL_BRIDGE_LAB')
PAIR=('ONG_P2','LOBO_P1')

def setup(db,seed,policy):
 r18.init_db(str(db),'A',seed)
 st=base.state_genesis(seed,PAIR)
 st['magic_pre_reg_sha']=MAGIC_SHA;st['magic_policy']=policy;st['model_scope']='LAB_TYPED_WATER_MAGIC_ATTACK_WITH_8PA_AND_ASSUMPTIONS'
 conn=r18.connect(str(db))
 try:
  with conn:conn.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(st),))
 finally:conn.close()

def start(st,p,seq):
 if st['magic_pre_reg_sha']!=MAGIC_SHA or p.get('magic_policy')!=st['magic_policy']:raise EffectBlocked('MAGIC_PREREG_DRIFT')
 d={k:v for k,v in p.items() if k!='magic_policy'}
 return base.start(st,d,seq)

def pass_turn(st,p,seq):
 if st['phase']!='ACTIVE' or st['active']!='ONG_P2' or st['magic_policy'] not in ('DECLINE_WHIP','CAST_WHIP'):raise EffectBlocked('PASS_ILLEGAL')
 if p.get('reason') not in ('POLICY_DECLINES','INSUFFICIENT_PA') or p.get('who')!='ONG_P2':raise EffectBlocked('PASS_PROVENANCE')
 a=st['actors']['ONG_P2']['resource'];needed=(st['magic_policy']=='DECLINE_WHIP' and p['reason']=='POLICY_DECLINES') or (st['magic_policy']=='CAST_WHIP' and a['pa']<8 and p['reason']=='INSUFFICIENT_PA')
 if not needed:raise EffectBlocked('PASS_WHEN_SPELL_LEGAL')
 s=base.scene(st);start_len=len(s.events);caster=s.actors['ONG_P2']
 if caster.standard!=1:raise EffectBlocked('NO_STANDARD')
 caster.standard=0
 ev=s.record({'action':'spell_declined','by':'ONG_P2','policy':st['magic_policy'],'PA_spent':0,'reason':p['reason'],'source':ONG['url']})
 end_source_turn(s,'ONG_P2');nxt=r18._next_turn(st);s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 base.sync(st,s);st['history'].append({'actor':'ONG_P2','target':'LOBO_P1','own_turn':1+sum(x['actor']=='ONG_P2' for x in st['history']), 'event_seq':ev['seq'],'hit':False,'hp_loss':0,'action':'DECLINE_SPELL'})
 return {'kind':'PASS_SPELL','actor':'ONG_P2','policy':st['magic_policy'],'new_native_events':copy.deepcopy(s.events[start_len:]),'pa_after':caster.pa,'next_turn':nxt}

def spell(st,p,seq):
 if st['phase']!='ACTIVE' or st['active']!='ONG_P2' or st['magic_policy']!='CAST_WHIP' or p.get('actor')!='ONG_P2':raise EffectBlocked('MAGIC_ACTION_ILLEGAL')
 sturn=1+sum(x['actor']=='ONG_P2' for x in st['history']);lobo='LOBO_P1'
 s=base.scene(st);a=s.actors['ONG_P2'];t=s.actors[lobo]
 if a.pa<8 or a.standard!=1 or t.hp<=0:raise EffectBlocked('PA_OR_ACTION_INSUFFICIENT')
 weak=10*a.hp<a.maximum_hp and a.hp>0
 tape=base.tape(st['seed'],PAIR,'ONG_P2',sturn,weak)
 if p!={'actor':'ONG_P2','target':lobo,'own_turn':sturn,'roll_tape':tape,'spell':ONG['attack_name'],'source_pa_cost':8}:raise EffectBlocked('MAGIC_TAPE_OR_COST_DRIFT')
 atk_rolls=tuple(tuple(x) for x in tape['hit']);score=(min(map(sum,atk_rolls))+19-2 if weak else sum(atk_rolls[0])+19)
 damage=sum(sum(x) for x in tape['damage'])+28
 oldlen=len(s.events)
 ev=apply_weapon_attack(s,'ONG_P2',lobo,source=base.ABILITY['ONG_P2'],
     state=ActorActionState('ONG_P2',ONG['level'],a.pa,(base.ABILITY['ONG_P2'].action_id,),enemy_ids_visible=(lobo,)),
     proofs=(base.EVIDENCE['ONG_P2'],),roll_score=score,damage=damage,damage_tag='agua',
     rd=Resistances(general=base.ACTORS[lobo]['rd'],provenance='RULE_DERIVED_CONDITIONAL_PRATA_NORMAL'),
     damage_dice_groups=((8,6),),damage_roll_groups=tuple(tuple(x) for x in tape['damage']),damage_fixed_bonus=28,
     critical_sequence=tuple(tape['crit']),attack_roll_attempts=atk_rolls,attack_bonus=19,lab_negative_critical_policy=True)
 pa_before=a.pa;a.pa-=8
 paid=s.record({'action':'spell_pa_cost','by':'ONG_P2','target':lobo,'spell':'Chicote de Água','source':ONG['url'],
   'attack_event_seq':ev['seq'],'PA_spent':8,'PA_before':pa_before,'PA_after':a.pa,
   'cost_source':'LITERAL_8PA_NO_SPECULATIVE_DISCOUNT','attack_spell_bridge':'V081_LAB_CONDITIONAL'})
 end_source_turn(s,'ONG_P2')
 m=st['metrics'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE');m['damage_gross']+=ev['raw'];m['post_rd']+=ev['net'];m['hp_loss']+=ev['hp_loss_actual'];m['overkill']+=ev['overkill'];m['pa_spent']+=8
 if t.hp==0:
  st['phase']='FINISHED';st['winner']='ONG_P2';st['finish_reason']='HP0_LAB_SPELL';st['active']=None;nxt={'ko':lobo}
 else:
  nxt=r18._next_turn(st);s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 base.sync(st,s);st['history'].append({'actor':'ONG_P2','target':lobo,'own_turn':sturn,'event_seq':ev['seq'],'hit':ev['hit'],'hp_loss':ev['hp_loss_actual'],'action':'SPELL_ATTACK'})
 return {'kind':'WHIP_MAGIC_ATTACK_WITH_PA','actor':'ONG_P2','spell_source':ONG['url'],'attack':ev,'PA_debit_event':paid,
  'tape':tape,'PA_paid':8,'new_native_events':copy.deepcopy(s.events[oldlen:]),'next_turn':nxt,
  'hp_after':{x:y.hp for x,y in s.actors.items()},'pa_after':{x:y.pa for x,y in s.actors.items()}}

def run_one(root,seed,policy):
 run=f'R198_MAGIC_ONG_VS_LOBO_{seed}_{policy}';db=pathlib.Path(root)/(run+'.sqlite')
 if db.exists():raise RuntimeError('NO_RUN_ID_REUSE')
 val,order=base.roll_initiative(seed,PAIR)
 if order is None:return {'run_id':run,'policy':policy,'seed':seed,'status':'PRECOMMIT_TIE_HOLD','db':None}
 setup(db,seed,policy)
 r18.event_commit(str(db),'LAB-CMD-'+run+'-INIT','SPELL_SCENE_INIT',{'initiative':val,'order':order,'pre_reg_sha':base.PRE_SHA,'source_snap_sha':base.SOURCE_SHA,'magic_policy':policy},start)
 for i in range(MAGIC_PRE['horizon_attacks']):
  st,_,_=r18.load(str(db))
  if st['phase']=='FINISHED':break
  who=st['active'];own_turn=1+sum(x['actor']==who for x in st['history'])
  if who=='LOBO_P1':
   weak=st['actors'][who]['resource']['hp']>0 and 10*st['actors'][who]['resource']['hp']<st['actors'][who]['resource']['maximum_hp']
   payload={'actor':who,'target':'ONG_P2','own_turn':own_turn,'roll_tape':base.tape(seed,PAIR,who,own_turn,weak)}
   r18.event_commit(str(db),'LAB-CMD-'+run+f'-BASIC{i+1:03d}','SOURCE_BASIC_NORMAL_ATTACK',payload,base.attack)
  elif policy=='DECLINE_WHIP' or st['actors']['ONG_P2']['resource']['pa']<8:
   payload={'who':'ONG_P2','reason':'POLICY_DECLINES' if policy=='DECLINE_WHIP' else 'INSUFFICIENT_PA'}
   r18.event_commit(str(db),'LAB-CMD-'+run+f'-PASS{i+1:03d}','SOURCE_SPELL_DECLINE',payload,pass_turn)
  else:
   weak=st['actors']['ONG_P2']['resource']['hp']>0 and 10*st['actors']['ONG_P2']['resource']['hp']<99
   payload={'actor':'ONG_P2','target':'LOBO_P1','own_turn':own_turn,'roll_tape':base.tape(seed,PAIR,'ONG_P2',own_turn,weak),'spell':ONG['attack_name'],'source_pa_cost':8}
   r18.event_commit(str(db),'LAB-CMD-'+run+f'-SPELL{i+1:03d}','SOURCE_SPELL_WHIP_WITH_PA',payload,spell)
 st,head,rev=r18.load(str(db));base.write_checkpoint(str(db))
 return {'run_id':run,'policy':policy,'seed':seed,'status':st['phase'] if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
  'winner':st['winner'],'rounds':st['round'],'hp_final':{x:v['resource']['hp'] for x,v in st['actors'].items()},
  'pa_final':{x:v['resource']['pa'] for x,v in st['actors'].items()},'metrics':st['metrics'],'commits':rev,'events':len(st['native_events']),
  'spell_count':sum(e['action']=='spell_pa_cost' for e in st['native_events']),'db':db.name,'head':head}

def run_all():
 out=ROOT/'evidence/magic_db';out.mkdir(exist_ok=True)
 res=[run_one(out,seed,policy) for seed,policy in itertools.product(MAGIC_PRE['seeds'],MAGIC_PRE['policies'])]
 (ROOT/'evidence/R198_MAGIC_RESULTS.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
 print(json.dumps({'runs':len(res),'status':{k:sum(x['status']==k for x in res) for k in set(x['status'] for x in res)},'spell_count':sum(x.get('spell_count',0) for x in res),'PA_spent':sum(x.get('metrics',{}).get('pa_spent',0) for x in res),'hits':sum(x.get('metrics',{}).get('hits',0)for x in res)}))
 return res
if __name__=='__main__':run_all()
