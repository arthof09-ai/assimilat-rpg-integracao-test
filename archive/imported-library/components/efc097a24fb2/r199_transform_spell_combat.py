"""R199 additive TEST source-state/magic adapter. Real combat uses existing v0.8.1
apply_weapon_attack and R18.event_commit; never modifies original modules/DBs.
Specific published Ong NORMAL/TRANSFORMED spell snapshots, hypothesis-gated
assimilation, temporary HP/+PA reserve and expiration. Not normative universal transformation.
"""
from __future__ import annotations
import copy,hashlib,json,pathlib,random,sys
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[3];R199=ROOT/'new/r199'
sys.path.insert(0,str(ROOT/'new/code'))
import r198_magic_spell_pilot as magic
base=magic.base;r18=base.r18
from vlab_effects_v08 import apply_weapon_attack,begin_source_turn,end_source_turn,ActorActionState,Resistances,EffectBlocked
PRE_BYTES=(R199/'source/R199_TRANSFORM_PREREG.json').read_bytes(); PRE=json.loads(PRE_BYTES); PRE_SHA=hashlib.sha256(PRE_BYTES).hexdigest()
PAIR=('ONG_P2','LOBO_P1')
SRC='https://app.notion.com/p/2b6c2b324ede82a2b415019eae21eaf5';RULE='https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9'

def form_die(seed):
 entropy=hashlib.sha256(f'R199|FORM_DURATION|{seed}|ONG_P2|1d6'.encode()).digest()
 return random.Random(int.from_bytes(entropy,'big')).randint(1,6)

def setup(db,seed,policy):
 magic.setup(db,seed,'CAST_WHIP')
 c=r18.connect(str(db))
 try:
  st=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0]); st.update({
   'r199_pre_reg_sha':PRE_SHA,'r199_policy':policy,'r199_source_actor':SRC,
   'r199_scene_id':'LAB-SCENE-'+db.stem,'scope':'R199_ONG_PUBLISHED_FORM_AND_WATER_SPELL_CONDITIONAL',
   'form':{'active':False,'used_scene':False,'duration_roll':None,'remaining':0,'normal_hp':99,'temp_hp':0,
      'normal_pa':91,'additional_pa':0,'transform_count':0,'expire_count':0},
   'r199_events':{'spell_count':0,'spell_hp':0,'transform_activations':0,'transform_expirations':0}})
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(st),))
 finally:c.close()

def start(st,p,seq):
 if p.get('r199_pre_reg_sha')!=PRE_SHA or p.get('r199_policy')!=st['r199_policy']:raise EffectBlocked('R199_PREREG_DRIFT')
 return magic.start(st,{k:v for k,v in p.items() if k not in ('r199_pre_reg_sha','r199_policy')},seq)

def next_after(st,s,who):
 end_source_turn(s,who)
 if st['phase']=='FINISHED':return {'ko':st['winner']}
 nxt=r18._next_turn(st);s.actors[st['active']].standard=0;begin_source_turn(s,st['active'])
 return nxt

def expire(st,s,why):
 f=st['form'];a=s.actors['ONG_P2']
 if not f['active']:raise EffectBlocked('FORM_ALREADY_INACTIVE')
 before={'hp':a.hp,'pa':a.pa,'ca':str(a.ca),'temp_hp':f['temp_hp'],'additional_pa':f['additional_pa']}
 # Expiration discards remaining transformation pool, NEVER normal HP loss or spent normal PA.
 a.hp=f['normal_hp'];a.maximum_hp=99;a.ca=30;a.pa=f['normal_pa'];a.mode='NORMAL';a.form_overlay=None;a.transformation_remaining=None
 f['active']=False;f['remaining']=0;f['temp_hp']=0;f['additional_pa']=0;f['expire_count']+=1
 st['r199_events']['transform_expirations']+=1
 return s.record({'action':'transform_expire','by':'ONG_P2','source':RULE,'why':why,
  'mode_before':'TRANSFORMED','mode_after':'NORMAL','before':before,
  'after':{'hp':a.hp,'pa':a.pa,'ca':str(a.ca)},'used_this_scene':True,
  'no_heal_of_normal_hp':True,'not_canonic_expiry_timing':'AFTER_N_SUBSEQUENT_OWN_TURNS_TEST'})

def transform(st,p,seq):
 f=st['form'];sturn=1+sum(x['actor']=='ONG_P2' for x in st['history'])
 if st['r199_policy']!='ACTIVATE_FORM_AND_CAST' or st['active']!='ONG_P2' or st['phase']!='ACTIVE' or f['used_scene'] or f['active'] or sturn!=1:raise EffectBlocked('TRANSFORM_ELIGIBILITY')
 if p!={'actor':'ONG_P2','action':'TRANSFORM','duration_roll':form_die(st['seed']),'source':RULE}:raise EffectBlocked('TRANSFORM_TAPE_DRIFT')
 s=base.scene(st);a=s.actors['ONG_P2'];old=len(s.events)
 if a.hp!=f['normal_hp'] or a.pa!=f['normal_pa'] or a.standard!=1 or a.movement!=1 or a.pa<40:raise EffectBlocked('FORM_HP_PA_OR_ACTION')
 dur=form_die(st['seed'])+1
 a.standard=0;a.movement=0;a.reaction=0 # explicitly conditional full action policy
 f['normal_pa']-=40;f['additional_pa']=63;f['temp_hp']=54
 a.pa=f['normal_pa']+f['additional_pa'];a.hp=f['normal_hp']+f['temp_hp'];a.maximum_hp=153;a.ca=36;a.mode='TRANSFORMED';a.transformation_remaining=dur
 f.update({'active':True,'used_scene':True,'duration_roll':form_die(st['seed']),'remaining':dur,'transform_count':1})
 st['r199_events']['transform_activations']+=1;st['metrics']['pa_spent']+=40
 ev=s.record({'action':'transform_activate','by':'ONG_P2','source':RULE,'form_source':SRC,'scene_id':st['r199_scene_id'],
  'duration_roll':form_die(st['seed']),'duration_total':dur,'duration_rule':'PRATA_1d6_PLUS1',
  'full_action':True,'rank_minimum':'PRATA_1','one_per_scene':True,'cost':40,
  'normal_pa_before':91,'normal_pa_after':f['normal_pa'],'form_additional_pa_conditional':63,
  'normal_hp_before':f['normal_hp'],'form_temporary_hp_conditional':54,'ca_before':30,'ca_after':36,
  'form_int_before':19,'form_int_after':25,'source_spirit_identity':'BLANK_IN_ORIGINAL_PAGE',
  'eligibility':'LAB_CONDITIONAL_EXISTING_TRANSFORM_TOGGLE_NOT_PROVEN_ASSIMILATION'})
 nxt=next_after(st,s,'ONG_P2');base.sync(st,s)
 st['history'].append({'actor':'ONG_P2','own_turn':1,'action':'TRANSFORM','event_seq':ev['seq']})
 return {'kind':'FORM_ACTIVATE_SOURCE_SNAPSHOT_TEST','event':ev,'added':copy.deepcopy(s.events[old:]),'next_turn':nxt}

def spell(st,p,seq):
 who='ONG_P2';target='LOBO_P1';f=st['form'];turn=1+sum(x['actor']==who for x in st['history'])
 if st['phase']!='ACTIVE' or st['active']!=who:raise EffectBlocked('SPELL_OUT_OF_TURN')
 if f['active'] and st['r199_policy']!='ACTIVATE_FORM_AND_CAST':raise EffectBlocked('FORM_POLICY')
 s=base.scene(st);a=s.actors[who];d=s.actors[target]
 if a.hp<=0 or d.hp<=0 or a.standard!=1 or a.pa<8:raise EffectBlocked('CAST_DISABLED')
 weak=a.hp>0 and 10*a.hp<a.maximum_hp
 tape=base.tape(st['seed'],PAIR,who,turn,weak)
 if p!={'actor':who,'target':target,'own_turn':turn,'roll_tape':tape,'spell':'Chicote de Água','cost':8,'form':f['active']}:raise EffectBlocked('CAST_TAPE_DRIFT')
 bonus=25 if f['active'] else 19;flat=34 if f['active'] else 28
 rolls=tuple(tuple(x) for x in tape['hit']);score=(min(map(sum,rolls))+bonus-2 if weak else sum(rolls[0])+bonus)
 dmg=sum(sum(x)for x in tape['damage'])+flat;old=len(s.events)
 ev=apply_weapon_attack(s,who,target,source=base.ABILITY[who],state=ActorActionState(who,7,a.pa,(base.ABILITY[who].action_id,),enemy_ids_visible=(target,)),proofs=(base.EVIDENCE[who],),
  roll_score=score,damage=dmg,damage_tag='agua',rd=Resistances(general=15,provenance='R198_RULE_DERIVED_PRATA_NORMAL_CONDITIONAL'),
  damage_dice_groups=((8,6),),damage_roll_groups=tuple(tuple(x) for x in tape['damage']),damage_fixed_bonus=flat,
  critical_sequence=tuple(tape['crit']),attack_roll_attempts=rolls,attack_bonus=bonus,lab_negative_critical_policy=True)
 before_pa=a.pa;a.pa-=8
 if f['active']:
  pay_normal=min(8,f['normal_pa']);f['normal_pa']-=pay_normal;f['additional_pa']-=8-pay_normal
 else:f['normal_pa']-=8
 if a.pa!=f['normal_pa']+f['additional_pa']:raise EffectBlocked('PA_POOL_MISMATCH')
 paid=s.record({'action':'spell_pa_cost','by':who,'spell':'Chicote de Água','target':target,
  'source':SRC,'attack_event_seq':ev['seq'],'PA_spent':8,'PA_before':before_pa,'PA_after':a.pa,
  'normal_pa_after':f['normal_pa'],'additional_pa_after':f['additional_pa'],
  'source_form':('TRANSFORMED' if f['active'] else 'NORMAL'),
  'source_bonus':bonus,'source_flat_damage':flat,'source_spell_formula':('8d6+34' if f['active'] else '8d6+28')})
 m=st['metrics'];m['attempts']+=1;m['hits']+=int(ev['hit']);m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE');m['damage_gross']+=ev['raw'];m['post_rd']+=ev['net'];m['hp_loss']+=ev['hp_loss_actual'];m['overkill']+=ev['overkill'];m['pa_spent']+=8
 st['r199_events']['spell_count']+=1;st['r199_events']['spell_hp']+=ev['hp_loss_actual']
 exp_event=None
 if d.hp==0:
  st['phase']='FINISHED';st['winner']=who;st['finish_reason']='HP0_TEST';st['active']=None
  end_source_turn(s,who);nxt={'ko':target}
 else:
  if f['active']:
   f['remaining']-=1;a.transformation_remaining=f['remaining']
   if f['remaining']==0:exp_event=expire(st,s,'DURATION_AFTER_OWN_ACTION_TEST')
  nxt=next_after(st,s,who)
 base.sync(st,s)
 st['history'].append({'actor':who,'own_turn':turn,'action':'SPELL','event_seq':ev['seq'],'form_active_at_cast':p['form']})
 return {'kind':'WATER_WHIP_R199','attack':ev,'paid':paid,'expiration':exp_event,
  'events_added':copy.deepcopy(s.events[old:]),'next_turn':nxt,'form_active_at_cast':p['form'],'resources':{k:{'hp':c.hp,'pa':c.pa}for k,c in s.actors.items()}}

def beast_attack(st,p,seq):
 if st['active']!='LOBO_P1':raise EffectBlocked('BEAST_NOT_ACTIVE')
 f=st['form'];hp_before=st['actors']['ONG_P2']['resource']['hp'];tmp_before=f['temp_hp']
 out=base.attack(st,p,seq)
 if f['active']:
  lost=hp_before-st['actors']['ONG_P2']['resource']['hp']
  shield=min(tmp_before,lost);normal_loss=lost-shield
  f['temp_hp']-=shield;f['normal_hp']-=normal_loss
  if f['normal_hp']<0 or f['temp_hp']<0 or st['actors']['ONG_P2']['resource']['hp']!=f['temp_hp']+f['normal_hp']:raise EffectBlocked('FORM_HP_POOL_DIVERGENCE')
  s=base.scene(st);ev=s.record({'action':'transform_damage_split','by':'ONG_P2','attack_native_seq':out['attack']['seq'],
   'incoming_hp_removed':lost,'temporary_hp_removed':shield,'normal_hp_removed':normal_loss,
   'temporary_hp_remaining':f['temp_hp'],'normal_hp_remaining':f['normal_hp']})
  base.sync(st,s);out['events_added'].append(ev);out['resource_split']=ev
  if st['phase']=='FINISHED':
   # Never permit another action after knockout; record interrupted form in same transaction.
   f['active']=False;f['remaining']=0;st['r199_events']['transform_expirations']+=1;f['expire_count']+=1
   s=base.scene(st);ev2=s.record({'action':'transform_end_on_ko','by':'ONG_P2','reason':'HP0','scene_id':st['r199_scene_id']});base.sync(st,s);out['events_added'].append(ev2)
 else:
  f['normal_hp']=st['actors']['ONG_P2']['resource']['hp']
 return out

def run_one(output,seed,policy):
 ident=f'R199_ONG_LOBO_{seed}_{policy}';db=pathlib.Path(output)/(ident+'.sqlite')
 if db.exists():raise RuntimeError('RUN_ID_ALREADY_USED')
 vals,order=base.roll_initiative(seed,PAIR)
 if order is None:return {'id':ident,'seed':seed,'policy':policy,'status':'PRECOMMIT_TIE_HOLD','reason':'NO_NORMATIVE_INIT_TIE'}
 setup(db,seed,policy)
 r18.event_commit(str(db),'LAB-CMD-'+ident+'-INIT','R199_INIT',{'initiative':vals,'order':order,'pre_reg_sha':base.PRE_SHA,'source_snap_sha':base.SOURCE_SHA,'magic_policy':'CAST_WHIP','r199_pre_reg_sha':PRE_SHA,'r199_policy':policy},start)
 for i in range(PRE['horizon_actions']):
  st,_,_=r18.load(str(db))
  if st['phase']=='FINISHED':break
  who=st['active'];turn=1+sum(h['actor']==who for h in st['history'])
  if who=='LOBO_P1':
   a=st['actors'][who]['resource'];weak=a['hp']>0 and 10*a['hp']<a['maximum_hp']
   payload={'actor':who,'target':'ONG_P2','own_turn':turn,'roll_tape':base.tape(seed,PAIR,who,turn,weak)}
   r18.event_commit(str(db),'LAB-CMD-'+ident+f'-B{i+1:03d}','R199_BEAST_NORMAL_ATTACK',payload,beast_attack)
  elif policy=='ACTIVATE_FORM_AND_CAST' and not st['form']['used_scene']:
   payload={'actor':who,'action':'TRANSFORM','duration_roll':form_die(seed),'source':RULE}
   r18.event_commit(str(db),'LAB-CMD-'+ident+f'-F{i+1:03d}','R199_TRANSFORM_ACTIVATE',payload,transform)
  else:
   a=st['actors'][who]['resource']
   if a['pa']<8:
    payload={'who':who,'reason':'INSUFFICIENT_PA'}
    r18.event_commit(str(db),'LAB-CMD-'+ident+f'-PASS{i+1:03d}','R199_SPELL_NO_PA_PASS',payload,magic.pass_turn)
    continue
   weak=a['hp']>0 and 10*a['hp']<a['maximum_hp']
   payload={'actor':who,'target':'LOBO_P1','own_turn':turn,'roll_tape':base.tape(seed,PAIR,who,turn,weak),'spell':'Chicote de Água','cost':8,'form':st['form']['active']}
   r18.event_commit(str(db),'LAB-CMD-'+ident+f'-S{i+1:03d}','R199_WATER_WHIP',payload,spell)
 st,head,rev=r18.load(str(db));base.write_checkpoint(str(db))
 return {'id':ident,'seed':seed,'policy':policy,'status':st['phase'] if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
  'winner':st['winner'] if st['phase']=='FINISHED' else None,'rounds':st['round'],'commits':rev,'events':len(st['native_events']),
  'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},'pa':{k:v['resource']['pa'] for k,v in st['actors'].items()},
  'metrics':st['metrics'],'r199_events':st['r199_events'],'form':st['form'],'db':db.name,'head':head}

def main():
 out=R199/'evidence/db';out.mkdir(exist_ok=True)
 rec=[run_one(out,seed,policy) for seed in PRE['seeds'] for policy in PRE['policies']]
 (R199/'evidence/R199_TRANSFORM_MAGIC_RESULTS.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False))
 from collections import Counter
 print(json.dumps({'runs':len(rec),'statuses':dict(Counter(x['status'] for x in rec)),
  'winners':dict(Counter(x.get('winner') for x in rec)),'casts':sum(x.get('r199_events',{}).get('spell_count',0) for x in rec),
  'transforms':sum(x.get('r199_events',{}).get('transform_activations',0) for x in rec),'expirations':sum(x.get('r199_events',{}).get('transform_expirations',0) for x in rec)}))
 return rec
if __name__=='__main__':main()
