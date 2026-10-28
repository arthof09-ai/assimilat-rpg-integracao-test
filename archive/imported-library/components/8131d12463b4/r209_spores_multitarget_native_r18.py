"""R209 EXP: source-proposed *real battle* area magic with three native R18 actors.
Native v081 Scene / R18 atomic journals reused; only new AoE resolver is add-only.
Not a canonical combat, not the production damage motor.
"""
from __future__ import annotations
from pathlib import Path
import sys,json,hashlib,random,copy,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/mnt/data/vlab/r206runtime/new/code')
import r198_microbenchmark as core
from vlab_effects_v08 import FrozenRuleEvidence,AbilitySource,ActorActionState,Resistances,EffectBlocked,apply_weapon_attack,begin_source_turn,end_source_turn
R18=core.r18
PRE_BYTES=(ROOT/'source/R209_SPORES_AREA_PREREG.json').read_bytes();PRE=json.loads(PRE_BYTES)
PHASH=hashlib.sha256(PRE_BYTES).hexdigest()
E='ERISTAN_ON5_SPORES';B1='DRACOLION_SPORES_A';B2='DRACOLION_SPORES_B';TRIO=(E,B1,B2)
VERSION='R209-SOURCE-AREA-MULTITARGET-R18-V081-v1'

def register():
 for who in TRIO:
  data=PRE['actors'][who];e=(who==E)
  core.ACTORS[who]={'id':who,'kind':'ED' if e else 'BEAST','name':'Sikong Eristan PROPOSTO' if e else 'Dracolion CONDITIONAL '+who[-1],
   'url':PRE['source'] if e else PRE['beast_source'],'edited':'2026-10-20_NOTION_READONLY',
   'rank':'Ouro Negro' if e else 'Ouro','star':5 if e else 1,'level':20 if e else 11,
   'hp':data['hp'],'maximum_hp':data['hp'],'pa':data.get('pa_free',784),'ca':data['CA'],
   'dex':28 if e else 60,'init_dice':(4,6) if e else (3,6),'initiative_bonus':28 if e else 60,
   'attack_dice':(4,6) if e else (3,6),'attack_bonus':0 if e else 60,
   'damage_dice':((1,6),) if e else ((9,6),),'damage_flat':0,'damage_tag':'impacto',
   'rd':25 if e else 25,'rd_status':'ERISTAN_SOURCE_PHYSICAL_RD25_PROPOSAL' if e else 'DRACOLION_RD_CONDITIONAL',
   'damage_tag_status':'LAB_HYPOTHESIS','attack_name':'NOT_USED' if e else 'R205_CONDITIONAL_GENERIC_BASIC'}
  p={'source':core.ACTORS[who]['url'],'name':who,'contract':PRE['spell'] if e else PRE['beast_attack']}
  digest=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
  core.EVIDENCE[who]=FrozenRuleEvidence(core.ACTORS[who]['url'],VERSION+'-'+who,digest,'2026-10-20','R209_PROPOSED_SOURCE_OR_BEAST_CONDITIONAL')
  core.ABILITY[who]=AbilitySource(VERSION+'-BASIC-'+who,'attack','STANDARD',core.ACTORS[who]['url'],core.EVIDENCE[who].rule_id,'RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-WEAPON')
register()

def roll_order(seed):
 vals,order=core.roll_initiative(seed,TRIO)
 return vals,order if len({v['result'] for v in vals.values()})==len(TRIO) else None

def spell_roll(seed,own_turn,kind,target='',n=10,faces=10):
 entropy=hashlib.sha256(f'{VERSION}|{seed}|E_TURN={own_turn}|{kind}|{target}|{n}d{faces}'.encode()).digest()
 rng=random.Random(int.from_bytes(entropy,'big'))
 return [rng.randint(1,faces) for _ in range(n)]

def inside(center,pos,radius):
 return (pos[0]-center[0])**2+(pos[1]-center[1])**2 <= radius**2

def geometry():
 c=PRE['chosen_center_m'];pos=PRE['positions_m'];spell=PRE['spell'];caster=pos[E]
 if (c[0]-caster[0])**2+(c[1]-caster[1])**2 > spell['center_max_distance_m']**2:raise EffectBlocked('CENTER_TOO_FAR')
 targets=[w for w in TRIO if inside(c,pos[w],spell['radius_m'])]
 return targets

def genesis(path,seed,policy):
 R18.init_db(str(path),'A',seed)
 st=core.state_genesis(seed,TRIO)
 st['r209']={'prereg_sha':PHASH,'version':VERSION,'policy':policy,'source':PRE['source'],'ability':PRE['ability'],
   'source_status':PRE['source_status'],'declared_center':PRE['chosen_center_m'],'spell_casts':0,'pa_paid':0,
   'targets_resolved':0,'total_effective':0,'total_raw':0,'self_damage':0,'beast_damage':0,
   'geometry':'REAL_2D_COORDINATE_CHECK','sample_unit':'PAIRED_SEED',
   'save_halving_rounding':'UNRESOLVED_GATE_NOT_EXERCISED_BY_COHORT'}
 conn=R18.connect(str(path))
 try:
  with conn:conn.execute('UPDATE meta SET value=? WHERE key="state"',(R18.canonical(st),))
 finally:conn.close()

def init(st,p,seq):
 if st['r209']['prereg_sha']!=PHASH or p.get('r209_sha')!=PHASH:raise EffectBlocked('PREREG_MISMATCH')
 q={k:v for k,v in p.items() if k!='r209_sha'}
 return core.start(st,q,seq)

def advance(st,s,who):
 end_source_turn(s,who)
 if st['phase']=='ACTIVE':
  ret=R18._next_turn(st)
  s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 else:ret={'end':'KO'}
 return ret

def cast(st,p,seq):
 if st['phase']!='ACTIVE' or st['active']!=E or p.get('actor')!=E or p.get('policy')!='SPELL_ON':raise EffectBlocked('CAST_NOT_ACTIVE')
 own_turn=1+sum(x['actor']==E for x in st['history'])
 if p.get('own_turn')!=own_turn:raise EffectBlocked('TURN_MISMATCH')
 s=core.scene(st);caster=s.actors[E];old=len(s.events)
 if caster.standard!=1 or caster.pa is None or caster.pa<80 or caster.hp<=0:raise EffectBlocked('SPELL_NOT_AVAILABLE')
 targets=geometry()
 if len(targets)<2 or E not in targets:raise EffectBlocked('AREA_INCORRECT')
 rolls=spell_roll(st['seed'],own_turn,'DAMAGE',n=10,faces=10)
 raw=sum(rolls)+10
 before=caster.pa;caster.pa-=80;caster.standard=0
 cast_event=s.record({'action':'r209_area_cast','by':E,'spell':PRE['ability'],'source':PRE['source'],
  'source_status':'PROPOSED_ON5_NOT_OFFICIAL','action_economy':'STANDARD',
  'center_m':PRE['chosen_center_m'],'caster_position_m':PRE['positions_m'][E],
  'center_max_m':25,'radius_m':5,'in_area':targets,'cast_roll_10d10':rolls,'flat':10,
  'common_roll_total':raw,'common_roll_status':'EXPERIMENTAL_SHARED_DAMAGE_PER_SPELL',
  'pa_before':before,'pa_after':caster.pa,'pa_spent':80,
  'half_rounding_status':'HOLD_IF_SAVE_PASSES_WITH_ODD_DAMAGE'})
 r=st['r209'];r['spell_casts']+=1;r['pa_paid']+=80;st['metrics']['pa_spent']+=80
 for who in targets:
  target=s.actors[who]
  if target.hp==0:continue
  cfg=PRE['actors'][who]
  n,faces=cfg['fortitude_dice'];d=spell_roll(st['seed'],own_turn,'SAVE',who,n=n,faces=faces)
  score=sum(d)+cfg['CON']
  succeeded=score>76
  if succeeded and raw%2:raise EffectBlocked('ODD_HALF_ROUNDING_NOT_DEFINED')
  damage=raw//2 if succeeded else raw
  # This cohort exercises failures only; target-specific magical RD is not sourced -> LAB 0.
  rd=0;net=max(0,damage-rd);pre_hp=target.hp;effective=min(net,pre_hp)
  target.hp=max(0,pre_hp-net)
  overkill=max(0,net-pre_hp)
  ev=s.record({'action':'r209_area_target','cast_event_seq':cast_event['seq'],
   'by':E,'target':who,'self_target':who==E,'source':PRE['source'],
   'position_m':PRE['positions_m'][who],
   'distance_squared_to_center':(PRE['positions_m'][who][0]-PRE['chosen_center_m'][0])**2+(PRE['positions_m'][who][1]-PRE['chosen_center_m'][1])**2,
   'radius_squared':25,'save_name':'Fortitude','save_dice':d,'save_dice_n':n,'save_attribute_con':cfg['CON'],
   'save_total':score,'CD':76,'save_success':succeeded,'save_rule':'SCORE_STRICTLY_EXCEEDS_CD',
   'damage_type':'PLANTA','damage_raw':damage,'rd_magic_applied':rd,'damage_after_rd':net,
   'hp_before':pre_hp,'hp_after':target.hp,'hp_loss_actual':effective,'overkill':overkill,
   'critical':'NOT_APPLICABLE_MAGIA','shared_cast_roll':rolls,
   'source_status':'NPC_PROPOSTO_BEAST_HYPOTHESIS'})
  r['targets_resolved']+=1;r['total_effective']+=effective;r['total_raw']+=damage
  if who==E:r['self_damage']+=effective
  else:r['beast_damage']+=effective
 # No target autoexclusion; means explicit self risk. Inactivation only after all simultaneous targets.
 if s.actors[E].hp==0:
  st['phase']='FINISHED';st['winner']='BEAST_SIDE';st['finish_reason']='CASTER_HP_ZERO_IN_AREA_TEST';st['active']=None
 nxt=advance(st,s,E);core.sync(st,s)
 st['history'].append({'actor':E,'own_turn':own_turn,'action':'AREA_SPELL','cast_seq':cast_event['seq'],'targets':len(targets)})
 return {'kind':'R209_NATIVE_R18_ATOMIC_MULTI_TARGET_AREA','cast_seq':cast_event['seq'],'events_added':copy.deepcopy(s.events[old:]),'next_turn':nxt}

def pass_e(st,p,seq):
 own_turn=1+sum(x['actor']==E for x in st['history'])
 if st['phase']!='ACTIVE' or st['active']!=E or p!={'actor':E,'own_turn':own_turn,'policy':'SPELL_OFF'}:raise EffectBlocked('PASS_ILLEGAL')
 s=core.scene(st);c=s.actors[E];old=len(s.events)
 if c.standard!=1 or c.hp<=0:raise EffectBlocked('PASS_NO_ACTION')
 c.standard=0;s.record({'action':'r209_pass','by':E,'pa_spent':0})
 nxt=advance(st,s,E);core.sync(st,s)
 st['history'].append({'actor':E,'own_turn':own_turn,'action':'PASS'})
 return {'kind':'R209_PASS_CONTROL','events_added':copy.deepcopy(s.events[old:]),'next_turn':nxt}

def beast_attack(st,p,seq):
 who=st['active'];own_turn=1+sum(h['actor']==who for h in st['history'])
 if st['phase']!='ACTIVE' or who not in (B1,B2) or p.get('actor')!=who or p.get('target')!=E or p.get('own_turn')!=own_turn:raise EffectBlocked('BEAST_TURN_MISMATCH')
 s=core.scene(st);a=s.actors[who];t=s.actors[E];old=len(s.events)
 if a.hp<=0 or t.hp<=0 or a.standard!=1:raise EffectBlocked('UNAVAILABLE')
 weak=a.hp>0 and 10*a.hp<a.maximum_hp
 tape=core.tape(st['seed'],TRIO,who,own_turn,weak)
 if p.get('roll_tape')!=tape:raise EffectBlocked('TAPE_TAMPER')
 attempts=tuple(tuple(x) for x in tape['hit']);score=(min(map(sum,attempts))+60-2) if weak else sum(attempts[0])+60
 ev=apply_weapon_attack(s,who,E,source=core.ABILITY[who],state=ActorActionState(who,11,a.pa,(core.ABILITY[who].action_id,),enemy_ids_visible=(E,)),
  proofs=(core.EVIDENCE[who],),roll_score=score,damage=sum(sum(x)for x in tape['damage']),damage_tag='impacto',
  rd=Resistances(general=25,provenance='ERISTAN_PHYSICAL_RD25_SOURCE_PROPOSAL'),
  damage_dice_groups=((9,6),),damage_roll_groups=tuple(tuple(x) for x in tape['damage']),damage_fixed_bonus=0,
  critical_sequence=tuple(tape['crit']),attack_roll_attempts=attempts,attack_bonus=60,lab_negative_critical_policy=True)
 m=st['metrics'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE')
 for key,field in [('damage_gross','raw'),('post_rd','net'),('hp_loss','hp_loss_actual'),('overkill','overkill')]:m[key]+=ev[field]
 a.standard=0
 if t.hp==0:
  st['phase']='FINISHED';st['winner']='BEAST_SIDE';st['finish_reason']='E_HP_ZERO_FROM_BEAST_ATTACK';st['active']=None
 nxt=advance(st,s,who);core.sync(st,s)
 st['history'].append({'actor':who,'own_turn':own_turn,'action':'ATTACK','event_seq':ev['seq']})
 return {'kind':'R209_NATIVE_BEAST_TEST_ATTACK','events_added':copy.deepcopy(s.events[old:]),'next_turn':nxt}

def run(seed,policy):
 ident=f'R209_AREA_SPORES_S{seed}_{policy}';db=ROOT/'evidence/db'/(ident+'.sqlite')
 if db.exists():raise RuntimeError('RUN_ID_ALREADY_CONSUMED')
 vals,order=roll_order(seed)
 if order is None:return {'run_id':ident,'seed':seed,'policy':policy,'status':'PRECOMMIT_INIT_TIE_HOLD'}
 genesis(db,seed,policy)
 R18.event_commit(str(db),'LAB-CMD-'+ident+'-INIT','R209_INIT',{ 'initiative':vals,'order':order,'pre_reg_sha':core.PRE_SHA,'source_snap_sha':core.SOURCE_SHA,'r209_sha':PHASH},init)
 for j in range(PRE['max_committed_actor_actions']):
  st,_,_=R18.load(str(db))
  if st['phase']=='FINISHED':break
  who=st['active'];own_turn=1+sum(h['actor']==who for h in st['history'])
  if who==E:
   p={'actor':E,'own_turn':own_turn,'policy':policy}
   if policy=='SPELL_ON' and st['actors'][E]['resource']['pa']>=80:
    R18.event_commit(str(db),f'LAB-CMD-{ident}-CAST-{j:03d}','R209_SOURCE_AREA_MULTI',p,cast)
   else:
    p['policy']='SPELL_OFF';R18.event_commit(str(db),f'LAB-CMD-{ident}-PASS-{j:03d}','R209_SCOPE_PASS',p,pass_e)
  else:
   weak=st['actors'][who]['resource']['hp']>0 and 10*st['actors'][who]['resource']['hp']<st['actors'][who]['resource']['maximum_hp']
   p={'actor':who,'target':E,'own_turn':own_turn,'roll_tape':core.tape(seed,TRIO,who,own_turn,weak)}
   R18.event_commit(str(db),f'LAB-CMD-{ident}-ATK-{j:03d}','R209_BEAST_PHYSICAL',p,beast_attack)
 st,head,rev=R18.load(str(db));core.write_checkpoint(str(db))
 return {'run_id':ident,'seed':seed,'policy':policy,'status':'KO' if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
  'winner':st['winner'],'commits':rev,'events':len(st['native_events']),
  'attacks':sum(e['action']=='weapon_attack' for e in st['native_events']),
  'casts':st['r209']['spell_casts'],'pa_spent':st['r209']['pa_paid'],
  'area_target_events':st['r209']['targets_resolved'],'magic_effective':st['r209']['total_effective'],
  'self_damage':st['r209']['self_damage'],'beast_damage':st['r209']['beast_damage'],
  'final_hp':{w:v['resource']['hp'] for w,v in st['actors'].items()},'head':head,'db':db.name}

def main():
 ROOT.joinpath('evidence/db').mkdir(parents=True,exist_ok=True)
 # Complete preflight without consuming any RUN-ID.
 assert not inside([30,0],PRE['positions_m'][E],25)
 assert set(geometry())==set(TRIO)
 results=[run(seed,pol) for seed in PRE['seeds'] for pol in PRE['policies']]
 (ROOT/'evidence/R209_COMBAT_RESULTS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
 print(json.dumps({'attempted_arms':len(results),'committed':sum('db' in x for x in results),
 'tie_arms':sum(x['status']=='PRECOMMIT_INIT_TIE_HOLD' for x in results),
 'casts':sum(x.get('casts',0) for x in results),'target_resolutions':sum(x.get('area_target_events',0) for x in results),
 'commits':sum(x.get('commits',0) for x in results),'events':sum(x.get('events',0) for x in results),
 'attacks':sum(x.get('attacks',0) for x in results),'KO':sum(x['status']=='KO' for x in results),
 'censored':sum(x['status']=='CENSORED_HORIZON' for x in results)},indent=2))
if __name__=='__main__':main()
