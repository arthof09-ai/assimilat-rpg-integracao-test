"""R204 live source-grounded water spell at real coordinates.
Uses R18 event_commit, R198 native actor/session adapters and v0.8.1 native mitigate.
NO magical critical, universal spell attack roll, invented PA discount, or historical replay.
"""
from __future__ import annotations
import sys,json,hashlib,pathlib,copy,random
from fractions import Fraction
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
PAST=pathlib.Path('/mnt/data/vlab_r200/previous')
sys.path.insert(0,str(PAST/'new/code'))
import r198_magic_spell_pilot as magic
base=magic.base
from vlab_effects_v08 import EffectBlocked, begin_source_turn, end_source_turn
from vlab_rd_v08 import mitigate,DamageComponent,Resistances
R18=base.r18
PREPATH=ROOT/'source/R204_V2_MAGIC_PREREG.json';PRE=json.loads(PREPATH.read_text());PHASH=hashlib.sha256(PREPATH.read_bytes()).hexdigest()
SRC=magic.ONG['url']; RULE='https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373'; M='https://app.notion.com/p/3ffc2b324ede81c5a5c3d56cc6a29f84'
PAIR=('ONG_P2','LOBO_P1');VERSION='R204V2-SOURCE-EXPLICIT-4D6-ATTACK-NO-MAGIC-CRIT-1'

def source_dice(seed,turn):
    def roll(label,n):
        e=f'{VERSION}|{seed}|{PAIR[0]}-{PAIR[1]}|ONG_P2|{turn}|{label}'
        rng=random.Random(int.from_bytes(hashlib.sha256(e.encode()).digest(),'big'))
        return [rng.randint(1,6) for _ in range(n)]
    return {'hit':roll('4d6-ATTACK-SOURCE-EXPLICIT',4),'damage':roll('8d6-DAMAGE-SOURCE-EXPLICIT',8)}

def init(db,seed,distance,policy):
    R18.init_db(str(db),'A',seed)
    st=base.state_genesis(seed,PAIR)
    st.update({'r204_pre_sha':PHASH,'r204_version':VERSION,'r204_policy':policy,
               'geo':{'ONG_P2':['0','0'],'LOBO_P1':[str(distance),'0'],'distance_m':str(distance),
                      'initial_m':str(distance),'specific_spell_range_source':None,'applied_spell_range_m':'9',
                      'boundary_source':M,'geometry':'SINGLE_TARGET','wolf_source_speed_m':'15'},
               'magic_live':{'spell_count':0,'PA_spent':0,'spell_hp_removed':0,'range_refusals':0,'movement_events':0,
                             'never_cast_passes':0,'no_critical_guarantee':True},
               'scope':'LAB_R204_CAUSAL_DISTANCE_CAST_WITH_SOURCE_ACTOR_AND_NATIVE_RD'})
    conn=R18.connect(str(db))
    try:
        with conn:conn.execute('UPDATE meta SET value=? WHERE key="state"',(R18.canonical(st),))
    finally:conn.close()

def start(st,p,seq):
    if st['r204_pre_sha']!=PHASH or p.get('r204_version')!=VERSION:raise EffectBlocked('R204_PREFLIGHT')
    del p['r204_version']
    try:return base.start(st,p,seq)
    finally:p['r204_version']=VERSION

def finish_turn(st,s,actor):
    end_source_turn(s,actor)
    nxt=R18._next_turn(st)
    s.actors[st['active']].standard=0
    begin_source_turn(s,st['active'])
    return nxt

def cast(st,p,seq):
    if st['phase']!='ACTIVE' or st['active']!='ONG_P2' or st['r204_policy']!='CAST_WHEN_IN_RANGE':raise EffectBlocked('NOT_CAST_TURN')
    ares=st['actors']['ONG_P2']['resource'];b=st['actors']['LOBO_P1']['resource']
    distance=Fraction(st['geo']['distance_m'])
    if distance>9:raise EffectBlocked('OUT_OF_RANGE_PRECOMMIT_NO_PA')
    if ares['pa']<8 or ares['standard']!=1 or b['hp']<=0:raise EffectBlocked('NO_PA_OR_ACTION')
    turn=1+sum(h['actor']=='ONG_P2' for h in st['history'])
    rolls=source_dice(st['seed'],turn)
    if p!={'actor':'ONG_P2','target':'LOBO_P1','spell':'Chicote de Água', 'cost':8,'distance_m':str(distance),
           'source_rolls':rolls,'own_turn':turn,'no_critical':True}:raise EffectBlocked('SPELL_PAYLOAD_TAMPER')
    s=base.scene(st);a=s.actors['ONG_P2'];t=s.actors['LOBO_P1'];oldlen=len(s.events)
    score=sum(rolls['hit'])+19
    hit=score>34  # explicit magic attack TEST 4d6+INT vs printed Lobo CA34
    raw=(sum(rolls['damage'])+28) if hit else 0
    outcome=mitigate((DamageComponent(raw,'agua',SRC),),Resistances(general=15 if hit else 0,provenance='BEAST_PRATA_NORMAL_RD_RULE'))
    hp_before=t.hp;loss=min(hp_before,outcome.effective);t.hp-=loss
    overkill=max(0,outcome.effective-hp_before)
    pa_before=a.pa;a.pa-=8;a.standard=0
    spell=s.record({'action':'spatial_magic_effect','by':'ONG_P2','target':'LOBO_P1','source':SRC,'magic_rule':RULE,
       'distance_m':str(distance),'limit_m':'9','geometry':'SINGLE_TARGET','range_source':M,'is_in_range':True,
       'spell_name':'Chicote de Água','action_cost':'STANDARD','PA_cost':8,'PA_before':pa_before,'PA_after':a.pa,
       'rolls':rolls['damage'],'spell_attack_test_literal':'4d6+INT19','dice_expression':'8d6+28','raw':raw,'rd_applied':outcome.applicable_rd,'rd_origin':outcome.rd_origin,
       'net':outcome.effective,'hp_before':hp_before,'hp_after':t.hp,'hp_loss_actual':loss,'overkill':overkill,
       'critical':'NONE','critical_tape':None,'attack_roll':rolls['hit'],'attack_bonus':19,'attack_score':score,'target_ca':34,'hit':hit,'save_roll':None,
       'cost_rule':'8PA_LITERAL','evocation_discount':'NOT_APPLIED_NO_EXPLICIT_SPELL_TAG'})
    paid=s.record({'action':'spell_pa_cost','by':'ONG_P2','spell':'Chicote de Água','target':'LOBO_P1',
       'source':SRC,'spell_effect_seq':spell['seq'],'PA_spent':8,'PA_before':pa_before,'PA_after':a.pa})
    x=st['magic_live'];x['spell_count']+=1;x['PA_spent']+=8;x['spell_hp_removed']+=loss
    m=st['metrics'];m['damage_gross']+=raw;m['post_rd']+=outcome.effective;m['hp_loss']+=loss;m['overkill']+=overkill;m['pa_spent']+=8
    if t.hp==0:
        st['phase']='FINISHED';st['winner']='ONG_P2';st['finish_reason']='SOURCE_SPATIAL_WHIP_HP0';st['active']=None
        end_source_turn(s,'ONG_P2');nxt={'ko':'LOBO_P1'}
    else:nxt=finish_turn(st,s,'ONG_P2')
    base.sync(st,s)
    st['history'].append({'actor':'ONG_P2','own_turn':turn,'target':'LOBO_P1','action':'R204_MAGIC_CAST',
                           'event_seq':spell['seq'],'PA_paid':8,'hp_loss_actual':loss,'distance_m':str(distance)})
    return {'kind':'NATIVE_RD_SPATIAL_MAGIC_CAST','effect':spell,'paid':paid,'new_native_events':copy.deepcopy(s.events[oldlen:]),
           'next_turn':nxt,'PA_paid':8,'HP_removed':loss,'distance_before_m':str(distance)}

def pass_spell(st,p,seq):
    if st['phase']!='ACTIVE' or st['active']!='ONG_P2':raise EffectBlocked('PASS_NOT_ACTIVE')
    ares=st['actors']['ONG_P2']['resource'];distance=Fraction(st['geo']['distance_m']);policy=st['r204_policy']
    reason=('NEVER_CAST_POLICY' if policy=='NEVER_CAST_CONTROL' else
            'OUTSIDE_9M' if distance>9 else 'INSUFFICIENT_PA' if ares['pa']<8 else 'NOT_ALLOWED')
    if reason=='NOT_ALLOWED' or p!={'actor':'ONG_P2','reason':reason,'distance_m':str(distance),'PA_spent':0}:raise EffectBlocked('PASS_FALSE_OR_TAMPER')
    s=base.scene(st);a=s.actors['ONG_P2'];old=len(s.events)
    if a.standard!=1:raise EffectBlocked('NO_STANDARD_FOR_PASS')
    a.standard=0
    ev=s.record({'action':'spatial_spell_declined','by':'ONG_P2','reason':reason,'distance_m':str(distance),
                 'limit_m':'9','PA_spent':0,'no_spell_effect':True,'source':SRC})
    if reason=='OUTSIDE_9M':st['magic_live']['range_refusals']+=1
    if reason=='NEVER_CAST_POLICY':st['magic_live']['never_cast_passes']+=1
    nxt=finish_turn(st,s,'ONG_P2');base.sync(st,s)
    turn=1+sum(h['actor']=='ONG_P2' for h in st['history'])
    st['history'].append({'actor':'ONG_P2','own_turn':turn,'action':'SPATIAL_PASS','event_seq':ev['seq'],'PA_paid':0,'reason':reason})
    return {'kind':'REAL_SPATIAL_SPELL_DECLINED','reason':reason,'new_native_events':copy.deepcopy(s.events[old:]),'next_turn':nxt}

def wolf_action(st,p,seq):
    if st['active']!='LOBO_P1' or st['phase']!='ACTIVE':raise EffectBlocked('BEAST_TURN_REQUIRED')
    dist=Fraction(st['geo']['distance_m']);s=base.scene(st);old=len(s.events);moved=None
    if dist>0:
        if dist>15:raise EffectBlocked('WOLF_CANNOT_CLOSE_15M_WITH_ONE_MOVE')
        wolf=s.actors['LOBO_P1'];wolf.movement=0
        moved=s.record({'action':'spatial_move','by':'LOBO_P1','source':'https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd',
             'speed_m':'15','initial_distance_m':str(dist),'end_distance_m':'0',
             'movement_spent_m':str(dist),'move_budget_used':1,'standard_action_remaining':wolf.standard,
             'movement_and_attack_in_same_turn':'SOURCE_COMBAT_MOVEMENT_PLUS_STANDARD'})
        st['geo']['distance_m']='0';st['geo']['LOBO_P1']=['0','0'];st['magic_live']['movement_events']+=1
        base.sync(st,s)
    who='LOBO_P1';turn=1+sum(x['actor']==who for x in st['history'])
    a=st['actors'][who]['resource'];weak=a['hp']>0 and 10*a['hp']<a['maximum_hp']
    expected={'actor':who,'target':'ONG_P2','own_turn':turn,'roll_tape':base.tape(st['seed'],PAIR,who,turn,weak)}
    if p!=expected:raise EffectBlocked('WOLF_ATTACK_DRIFT')
    out=base.attack(st,p,seq)
    if moved:out['spatial_movement']=moved;out['events_added']=[moved]+out['events_added']
    return out

def run(seed,distance,policy):
    ident=f'R204V2_ONG_LOBO_S{seed}_DIST{str(distance).replace(".","p")}_{policy}'
    outdir=ROOT/'evidence/v2_db';outdir.mkdir(exist_ok=True,parents=True)
    db=outdir/f'{ident}.sqlite'
    if db.exists():raise RuntimeError('RUN-ID-ALREADY-CONSUMED')
    val,order=base.roll_initiative(seed,PAIR)
    if order is None:return {'run_id':ident,'seed':seed,'distance_m':str(distance),'policy':policy,'status':'PRECOMMIT_TIE_HOLD','db':None}
    init(db,seed,distance,policy)
    args={'initiative':val,'order':order,'pre_reg_sha':base.PRE_SHA,'source_snap_sha':base.SOURCE_SHA,'r204_version':VERSION}
    R18.event_commit(str(db),'LAB-CMD-'+ident+'-INIT','R204_SPATIAL_INIT',args,start)
    for i in range(PRE['max_actions_per_scene']):
        st,_,_=R18.load(str(db))
        if st['phase']=='FINISHED':break
        who=st['active']
        if who=='LOBO_P1':
            trn=1+sum(x['actor']==who for x in st['history']);a=st['actors'][who]['resource'];weak=a['hp']>0 and 10*a['hp']<a['maximum_hp']
            pl={'actor':who,'target':'ONG_P2','own_turn':trn,'roll_tape':base.tape(seed,PAIR,who,trn,weak)}
            R18.event_commit(str(db),'LAB-CMD-'+ident+f'-WOLF-{i+1:03d}','R204_BEAST_SPATIAL_MOVE_AND_ATTACK',pl,wolf_action)
        elif policy=='CAST_WHEN_IN_RANGE' and Fraction(st['geo']['distance_m'])<=9 and st['actors'][who]['resource']['pa']>=8:
            trn=1+sum(x['actor']==who for x in st['history'])
            pl={'actor':who,'target':'LOBO_P1','spell':'Chicote de Água','cost':8,'distance_m':st['geo']['distance_m'],
                'source_rolls':source_dice(seed,trn),'own_turn':trn,'no_critical':True}
            R18.event_commit(str(db),'LAB-CMD-'+ident+f'-SPELL-{i+1:03d}','R204_ACTUAL_SOURCE_MAGIC_NO_CRIT',pl,cast)
        else:
            d=Fraction(st['geo']['distance_m']);a=st['actors'][who]['resource']
            reason='NEVER_CAST_POLICY' if policy=='NEVER_CAST_CONTROL' else 'OUTSIDE_9M' if d>9 else 'INSUFFICIENT_PA'
            pl={'actor':who,'reason':reason,'distance_m':str(d),'PA_spent':0}
            R18.event_commit(str(db),'LAB-CMD-'+ident+f'-PASS-{i+1:03d}','R204_SPATIAL_SPELL_REJECT_OR_DECLINE',pl,pass_spell)
    st,head,rev=R18.load(str(db));base.write_checkpoint(str(db))
    z={'run_id':ident,'seed':seed,'policy':policy,'initial_distance_m':str(distance),'status':st['phase'] if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
       'winner':st['winner'] if st['phase']=='FINISHED' else None,'round':st['round'],'commits':rev,'native_events':len(st['native_events']),
       'spell_casts':st['magic_live']['spell_count'],'PA_spell_spent':st['magic_live']['PA_spent'],'HP_removed_by_spell':st['magic_live']['spell_hp_removed'],
       'range_refusals':st['magic_live']['range_refusals'],'wolf_moves':st['magic_live']['movement_events'],
       'wolf_basic_attacks':sum(e['action']=='weapon_attack' for e in st['native_events']),'final_hp':{x:a['resource']['hp'] for x,a in st['actors'].items()},
       'final_pa':{x:a['resource']['pa'] for x,a in st['actors'].items()},'head':head,'db':db.name}
    return z

def main():
    records=[run(s,dis,pol) for s in PRE['seeds'] for dis in PRE['positions_m'] for pol in PRE['policies']]
    (ROOT/'evidence/R204_V2_LIVE_MAGIC_RESULTS.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
    from collections import Counter
    print(json.dumps({'proposed_scenarios':len(records),'committed':sum(x['db']is not None for x in records),
      'KO':sum(x['status']=='FINISHED' for x in records),'censored':sum(x['status']=='CENSORED_HORIZON' for x in records),
      'precommit_tie':sum(x['status']=='PRECOMMIT_TIE_HOLD' for x in records),
      'actual_casts':sum(x.get('spell_casts',0) for x in records),'PA_magic_spent':sum(x.get('PA_spell_spent',0) for x in records),
      'HP_removed_by_spell':sum(x.get('HP_removed_by_spell',0) for x in records),'range_refusals':sum(x.get('range_refusals',0) for x in records),
      'wolf_moves':sum(x.get('wolf_moves',0) for x in records),'winners':dict(Counter(x['winner'] for x in records if x['status']=='FINISHED'))},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
