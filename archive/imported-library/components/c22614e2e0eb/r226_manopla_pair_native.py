"""R226 TEST: source-bound semicanon gear component atop v0.8.1 physical attack, not new damage engine.
Damage physical and lightning split; same hit RNG and physical dice across arms. Slowing until end target next own turn.
"""
import sys,copy,hashlib,json
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r215_integrated_native as old
import vlab_r18_interactive as j
from vlab_effects_v08 import (Combatant,Scene,begin_source_turn,end_source_turn,apply_weapon_attack,ActorActionState,Resistances,DamageComponent,mitigate,effective_movement_speed,EffectBlocked)
P=json.loads((ROOT/'sources/R226_PREREG_BEFORE_EXEC.json').read_text());PB=(ROOT/'sources/R226_PREREG_BEFORE_EXEC.json').read_bytes();PH=hashlib.sha256(PB).hexdigest()
I=json.loads((ROOT/'sources/R226_MANOPLA_PRIMARY_MECHANICAL_EXCERPT.json').read_text());IB=(ROOT/'sources/R226_MANOPLA_PRIMARY_MECHANICAL_EXCERPT.json').read_bytes();IH=hashlib.sha256(IB).hexdigest()
class SourceHold(RuntimeError):pass

def init(db,seed,arm):
    j.init_db(str(db),'A',seed);st=j.initial('A',seed)
    r=old.actor('R');v=old.actor('V');r.standard=0;v.standard=0
    r.position='(0, 0)';v.position='(1.5, 0)'
    # A neutral TEST lower-bound movement speed only; not sourced as Varok's canonical speed.
    v.base_speed="4"
    st.update({'scene':f'R226-MANOPLA-{seed}-{arm}','seed':seed,'phase':'ACTIVE','turn':0,'active':'R','actors':{'R':asdict(r),'V':asdict(v)},'native_events':[],
      'r226':{'pre_sha256':PH,'item_excerpt_sha256':IH,'arm':arm,'item_equipped_both':True,'item_used':False,'item_recovery_rest_verified':False,'physical_chassis_same_in_both':True,'magical_rd_assumption':0,'world_canon':False,'turns':{'R':0,'V':0}}})
    c=j.connect(str(db));h=j.sha({'seed':seed,'pre':PH,'arm':arm,'source':IH})
    with c:
        for k,val in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:c.execute('UPDATE meta SET value=? WHERE key=?',(val,k))
    c.close()

def scene(st):return Scene({k:Combatant(**copy.deepcopy(v)) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R226-MESTRE-TEST-SEMICANON-GEAR-NOT-WORLD-CANON')
def sync(st,s):st['actors']={k:asdict(v) for k,v in s.actors.items()};st['native_events']=copy.deepcopy(s.events)
def prehit(seed):
    r=old.SRC['R'];a=old.dice(seed,'R226-ATTACK-4D6',4,6);crit=old.dice(seed,'R226-CRIT-3D6',3,6)
    score=sum(a)+r['attack_bonus']
    critical=('POSITIVE' if tuple(crit[:2])==(6,6) and crit[2]>=5 else 'NEGATIVE' if tuple(crit[:2])==(1,1) and crit[2]<=2 else 'NONE')
    return a,crit,score,critical

def attack(st,p,rev):
    if st['active']!='R' or st['turn']!=0 or p['seed']!=st['seed'] or p['pre']!=PH or p['item']!=IH:raise SourceHold('NOT_SOURCE_AND_TURN_READY')
    s=scene(st);begin_source_turn(s,'R');r=s.actors['R'];v=s.actors['V']
    dice,crit,score,crit_type=prehit(st['seed']);hit=(score>v.ca or crit_type=='POSITIVE') and crit_type!='NEGATIVE'
    s.record({'action':'R226_ATTACK_HIT_AND_CRITICAL_RNG','by':'R','to':'V','rolls':list(dice),'crit_rolls':list(crit),'roll_score':score,'hit':hit,'critical':crit_type,'stream_tag':'R226-ATTACK-4D6|R226-CRIT-3D6','same_across_arms':True})
    activ=False
    if hit and st['r226']['arm']=='SAME_PHYSICAL_WITH_MAGIC':
        if not st['r226']['item_equipped_both'] or st['r226']['item_used'] or st['r226']['item_recovery_rest_verified']:
            raise SourceHold('ITEM_NOT_ELIGIBLE_OR_ALREADY_USED')
        if I['page_id']!='3f5c2b324ede81f5ac62fb940204cdac' or I['item_requires_pa']!=22 or I['item_attack_bonus_dice']!=[5,8] or I['item_attack_flat']!=3:
            raise SourceHold('ITEM_SOURCE_MISMATCH')
        if r.pa is None or r.pa<22:raise SourceHold('ITEM_PA_INSUFFICIENT')
        r.pa-=22;st['r226']['item_used']=True;activ=True
        s.record({'action':'R226_ITEM_DECLARATION_BEFORE_DAMAGE_RNG','by':'R','to':'V','page_id':I['page_id'],'source_sha256':IH,
          'item_equipped':True,'after_hit':True,'before_damage_rng':True,'pa_spent':22,'no_extra_standard':True,'once_per_8h':True,
          'effect_status':'SEMICANON_TEST_ONLY'})
    phys=old.dice(st['seed'],'R226-PHYSICAL-DAMAGE-8D10',8,10);gross=sum(phys)+35
    lightning=old.dice(st['seed'],'R226-LIGHTNING-DAMAGE-5D8',5,8) if activ else ()
    s.record({'action':'R226_DAMAGE_RNG_AFTER_DECLARATION','by':'R','to':'V','physical_rolls':list(phys),'lightning_rolls':list(lightning),
      'magic_active':activ,'rolls_shared_by_source_event':True})
    standard=old.STANDARD['R']
    receipt=apply_weapon_attack(s,'R','V',source=standard,
      state=ActorActionState('R',20,r.pa,(standard.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('V',)),
      proofs=(old.PROOFS['R'],),roll_score=score,damage=gross,damage_tag='perfurante',rd=Resistances(general=35,provenance='VAROK-PRIMARY-ON5-PHYSICAL-RD'),
      damage_dice_groups=((8,10),),damage_roll_groups=(tuple(phys),),damage_fixed_bonus=35,
      critical_sequence=tuple(crit),attack_roll_attempts=(tuple(dice),),attack_bonus=72,lab_negative_critical_policy=True)
    if activ:
        crit_bonus=40 if receipt['critical']=='POSITIVE' else 0
        magical_gross=sum(lightning)+3+crit_bonus
        lightning_out=mitigate((DamageComponent(magical_gross,'raio','MANOPLA-O3-SOURCE'),),Resistances(general=0,provenance='R226-UNKNOWN_MAGIC_RD_ZERO_ONLY_FOR_TEST'))
        before=v.hp;v.hp=max(0,before-lightning_out.effective)
        applies=bool(lightning_out.effective>0 and v.hp>0)
        if applies:
            if v.timed_source_speed_penalty_m:raise SourceHold('SLOW_STACK_PRECEDENCE_UNRESOLVED')
            v.timed_source_speed_penalty_m=3
        s.record({'action':'R226_ITEM_LIGHTNING_AND_CONDITION','by':'R','to':'V','hit':True,'source':I['page_id'],'trigger_intent_before_rng':True,
          'magic_dice':list(lightning),'magic_raw':magical_gross,'magic_rd':lightning_out.applicable_rd,'magic_effective':lightning_out.effective,
          'hp_before':before,'hp_after':v.hp,'slow_applied':applies,'slow_m':3 if applies else 0,'slow_until':'END_TARGET_NEXT_OWN_TURN',
          'no_extra_attack':True,'physical_receipt_seq':receipt['seq'],'semicanon_TEST':True})
    else:
        s.record({'action':'R226_ITEM_NO_ACTIVATION','by':'R','to':'V','arm':st['r226']['arm'],'hit':hit,'magic_effective':0,'pa_spent':0})
    end_source_turn(s,'R')
    st['active']='V';st['turn']=1;st['r226']['turns']['R']=1;st['r226']['hit']=hit;st['r226']['critical']=crit_type;st['r226']['physical_damage_gross']=gross
    sync(st,s)
    return {'events_added':copy.deepcopy(s.events),'hit':hit,'item_activated':activ,'source_status':'TEST_SEMICANON'}

def target_next_turn(st,p,rev):
    if st['active']!='V' or st['turn']!=1 or p['pre']!=PH:raise SourceHold('BAD_NEXT_TURN')
    s=scene(st);before=len(s.events);v=s.actors['V'];begin_source_turn(s,'V')
    observed=str(effective_movement_speed(v));
    if v.timed_source_speed_penalty_m:
        if v.timed_source_speed_penalty_m!=3 or not any(e['action']=='R226_ITEM_LIGHTNING_AND_CONDITION' and e['slow_applied'] for e in s.events):
            raise SourceHold('SLOW_WITHOUT_SOURCE')
        if observed!='1':raise SourceHold('TEST_MOVEMENT_PENALTY_MISMATCH')
    else:
        if observed!='4':raise SourceHold('TEST_MOVEMENT_BASE_MISMATCH')
    s.record({'action':'R226_SLOWED_TARGET_TURN_OBSERVATION','by':'V','available_speed_in_declared_4m_lab_fixture':observed,
      'source_speed_4m_is_TEST_assumption':True,'no_metric_world_block_mapping':True,'native_speed_gate_exercised':True})
    # No movement is published when path/adjacency and real Varok source speed are unverified.
    v.standard=0;s.record({'action':'R226_STANDARD_PASS_NOT_A_COMBAT_BENCHMARK','by':'V','reason':'NO_ADDITIONAL_SOURCE_BOUND_OFFENSIVE_ACTION_IN_NARROW_ITEM_FIXTURE'})
    end_source_turn(s,'V')
    if v.timed_source_speed_penalty_m:
        v.timed_source_speed_penalty_m=0
        s.record({'action':'R226_SOURCE_ITEM_SLOW_EXPIRES','by':'V','page_id':I['page_id'],'boundary':'END_TARGET_NEXT_OWN_TURN',
          'speed_before':observed,'speed_after':str(effective_movement_speed(v)),'no_free_HP_PA_or_reaction':True})
    st['r226']['turns']['V']=1;st['active']=None;st['phase']='CENSORED_SOURCE_EFFECT_WINDOW';st['turn']=2
    sync(st,s)
    return {'events_added':copy.deepcopy(s.events[before:]),'target_speed_during_turn':observed,'final_speed':str(effective_movement_speed(v))}

def run():
    records=[]
    for seed in P['seeds']:
      for arm in P['arms']:
        db=ROOT/'evidence/db'/f'R226_MANOPLA_{arm}_S{seed}.sqlite'
        if db.exists():raise FileExistsError('R226_RUN_COLLISION')
        init(db,seed,arm)
        j.event_commit(str(db),f'LAB-CMD-R226-{seed}-{arm}-ATTACK','R226_ATTACK_AND_ITEM',{'seed':seed,'pre':PH,'item':IH},attack)
        j.event_commit(str(db),f'LAB-CMD-R226-{seed}-{arm}-TARGET_TURN','R226_NEXT_OWN_TURN',{'pre':PH},target_next_turn)
        st,head,rev=j.load(str(db))
        ev=st['native_events'];we=next(e for e in ev if e['action']=='weapon_attack')
        spell=next((e for e in ev if e['action']=='R226_ITEM_LIGHTNING_AND_CONDITION'),None)
        records.append({'seed':seed,'arm':arm,'db':db.name,'commits':rev,'events':len(ev),'hit':we['hit'],'physical_gross':we['normal_damage'],
          'physical_net':we['hp_loss_actual'],'magic_net':spell['magic_effective'] if spell else 0,
          'item_pa_spent':22 if spell else 0,'slow_applied':bool(spell and spell['slow_applied']),
          'final_HP':{k:v['hp'] for k,v in st['actors'].items()},'final_PA':{k:v['pa'] for k,v in st['actors'].items()},
          'source_window_censored':st['phase']=='CENSORED_SOURCE_EFFECT_WINDOW','head':head})
    pairs=[]
    for seed in P['seeds']:
        l=next(x for x in records if x['seed']==seed and x['arm']==P['arms'][0]);r=next(x for x in records if x['seed']==seed and x['arm']==P['arms'][1])
        assert l['hit']==r['hit'] and l['physical_gross']==r['physical_gross'] and l['physical_net']==r['physical_net']
        pairs.append({'seed':seed,'hit':l['hit'],'extra_hp_removed_by_magic':l['final_HP']['V']-r['final_HP']['V'],
          'magic_net_after_RD':r['magic_net'],'item_PA_spent':r['item_pa_spent'],'slow_applied':r['slow_applied']})
    rep={'status':'R226_TEST_SEMICANON_PAIRED_ITEM_EXECUTED_UNAUDITED','prereg_sha256':PH,'item_primary_excerpt_sha256':IH,
       'runs':records,'pairs':pairs,'historical_replays':0}
    (ROOT/'evidence/reports/R226_EXECUTION_RESULTS.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'arms':len(records),'pairs':len(pairs),'hits':sum(x['hit'] for x in pairs),'extra_magic_hp':sum(x['extra_hp_removed_by_magic'] for x in pairs),
       'item_pa':sum(x['item_PA_spent'] for x in pairs),'slow_activations':sum(x['slow_applied'] for x in pairs),'commits':sum(x['commits'] for x in records),'events':sum(x['events'] for x in records)},indent=2))
if __name__=='__main__':run()
