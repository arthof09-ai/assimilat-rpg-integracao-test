"""R240: bounded source-closed Fraco 10% boundary on authentic VLAB R18 clone.
This is a new experimental fixture, NOT a new combat motor and NOT an official R91 cell.
"""
from __future__ import annotations
import json,hashlib,random,sys,copy,math,sqlite3
from fractions import Fraction
from pathlib import Path
from dataclasses import asdict
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'code'));sys.path.insert(0,str(R/'runtime/native'));sys.path.insert(0,str(R/'runtime/fusion_stage12'))
import r234_source_complete_beast_battle as b
from vlab_effects_v08 import Scene,ActorActionState,Resistances,begin_source_turn,end_source_turn,move_via_verified_path,apply_weapon_attack,effective_movement_speed,weak_status,EffectBlocked
j=b.j
PBYTES=(R/'sources/R240_PREREG.json').read_bytes();P=json.loads(PBYTES);PH=hashlib.sha256(PBYTES).hexdigest()
RULEBYTES=(R/'sources/R236_FRACO_RULE_EXCERPT.json').read_bytes();RH=hashlib.sha256(RULEBYTES).hexdigest()
BHB=b.SH
assert P['source_max_hp']==b.BE['C']['hp'] and b.BE['C']['speed']==50

def dice(seed,tag,n,faces):
    key=f'R240|{seed}|C|OWN1|{tag}|{n}d{faces}'
    rng=random.Random(int.from_bytes(hashlib.sha256(key.encode()).digest(),'big'))
    return tuple(rng.randint(1,faces) for _ in range(n))

def initial(seed,arm):
    st=j.initial('A',seed);c=b.c_actor('C');g=b.c_actor('G');c['hp']=arm['hp'];c['position']='(14,0)';g['position']='(13,0)'
    st.update({'scene':f'R240-{arm["id"]}-S{seed}','seed':seed,'phase':'ACTIVE','round':1,'turn':0,'active':'C','order':['C','G'],
       'actors':{'C':c,'G':g},'native_events':[],
       'r240':{'seed':seed,'arm':arm['id'],'source_beast_sha':BHB,'rule_sha':RH,'prereg_sha':PH,
       'source_status':'VZ-PRECREATE-NONP4','initial_hp_croc':arm['hp'],'maxhp':5580,'base_speed':50,
       'own_turns':{'C':0},'official_benchmark':False,'official_death':False,'official_cells':0,
       'negative_critical_policy':'LAB-ONLY','final_effort':False,'outcome':None}})
    return st

def setup(path,seed,arm):
    if path.exists():raise FileExistsError('NO-REPEAT_EXISTING_DB')
    j.init_db(str(path),'A',seed)
    st=initial(seed,arm)
    gen=j.sha({'R240':PH,'R236_rule':RH,'R234_beast':BHB,'seed':seed,'arm':arm['id']})
    c=j.connect(str(path))
    with c:
        for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',gen),('head',gen)]:
            c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
    c.close()

def turn(st,p,rev):
    r=st['r240'];arm=p['arm'];who=p['who'];seed=p['seed'];actor='C'
    if (r['arm'],r['seed'],st['active'],st['phase'],p['prereg_sha'],p['source_sha'],p['rule_sha']) != (arm,seed,who,'ACTIVE',PH,BHB,RH):
        raise ValueError('R240_PREREG_OR_SOURCE_DRIFT')
    if who!='C' or st['turn']!=0 or rev!=1:raise ValueError('R240_ONE_TURN_ONLY')
    actors={k:b.load_actor(v) for k,v in st['actors'].items()};sc=Scene(actors,events=[],seed=seed,provenance='R240_VZ_PRECREATE_NONP4_TEST')
    before={k:{'hp':v.hp,'pa':v.pa,'position':v.position} for k,v in actors.items()}
    begin_source_turn(sc,actor);c=actors[actor]
    speed=effective_movement_speed(c)
    move_via_verified_path(sc,actor,source=b.M,state=ActorActionState(actor,23,c.pa,(b.M.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
        proofs=(b.PM,),destination='(14,1)',path_evidence='R240_EXP_LAB_OPEN_FIELD_1M_WITHIN_2M_ENEMY_RANGE_NOT_WORLD_GRID',travel_cost=Fraction(1),speed=speed)
    if math.dist((14,1),(13,0))>2:raise ValueError('SYNTHETIC_RANGE_NOT_CLOSED')
    weak=weak_status(c)
    hit0=dice(seed,'HIT0',6,6);hit1=dice(seed,'HIT1',6,6)
    attempts=(hit0,hit1) if weak else (hit0,)
    score=(min(sum(x) for x in attempts)-2 if weak else sum(hit0))+b.BE['C']['attack_bonus']
    damage=dice(seed,'DAMAGE',20,10);crit=dice(seed,'CRITICAL',3,6)
    sc.record({'action':'R240_SOURCE_TAPE','by':'C','to':'G','initial_hp':r['initial_hp_croc'],'maxhp':5580,'weak':weak,
       'attack_attempts':attempts,'hit0_common':hit0,'hit1_reserved_draw':hit1,'damage_dice':damage,'critical_sequence':crit,
       'roll_score':score,'source_beast_sha':BHB,'weak_rule_sha':RH,'prereg_sha':PH,
       'source_status':'VZ-PRECREATE-NONP4','official_outcome':False})
    hit=apply_weapon_attack(sc,'C','G',source=b.ATK['C'],state=ActorActionState('C',23,c.pa,(b.ATK['C'].action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('G',)),proofs=(b.PF['C'],),
       roll_score=score,damage=sum(damage),damage_tag=b.BE['C']['damage_type'],rd=Resistances(general=b.BE['G']['rd'],provenance='VZ-SOURCE-RD75-PHYSICAL'),
       damage_dice_groups=((20,10),),damage_roll_groups=(damage,),damage_fixed_bonus=0,critical_sequence=crit,attack_roll_attempts=attempts,attack_bonus=b.BE['C']['attack_bonus'],
       lab_negative_critical_policy=True,final_effort=False)
    end_source_turn(sc,'C')
    st['native_events']=copy.deepcopy(sc.events)
    st['turn']=1;st['phase']='R240_ONE_TURN_TEST_STOP';st['active']=None
    st['actors']={k:{**asdict(v),'ca':str(v.ca),'base_speed':str(v.base_speed)} for k,v in actors.items()}
    r['own_turns']['C']=1;r['outcome']={'weak':weak,'speed_m':str(speed),'attack_score':score,'damage_to_G':hit['hp_loss_actual'],'hit':hit['hit'],
       'phase':st['phase'],'official_benchmark':False,'official_death':False,'official_cells':0}
    return {'events_new':copy.deepcopy(sc.events),'before':before,'after':{k:{'hp':v.hp,'pa':v.pa,'position':v.position} for k,v in actors.items()},
       'weak':weak,'source_speed':str(speed),'attack_score':score,'attack_detail':copy.deepcopy(hit),'phase':st['phase']}

def run():
    out=[]
    for seed in P['seeds']:
        for arm in P['arms']:
            name=f'R240_{arm["id"]}_S{seed}.sqlite'
            db=R/'evidence/db'/name;setup(db,seed,arm)
            payload={'seed':seed,'arm':arm['id'],'who':'C','prereg_sha':PH,'source_sha':BHB,'rule_sha':RH}
            j.event_commit(str(db),f'LAB-CMD-R240-{arm["id"]}-{seed}','R240_WEAK_BOUNDARY_ONE_TURN',payload,turn)
            st,head,rev=j.load(str(db))
            assert rev==1 and st['r240']['outcome']['official_cells']==0
            c=sqlite3.connect(str(db));c.execute('PRAGMA wal_checkpoint(TRUNCATE)');c.close()
            out.append({'seed':seed,'arm':arm['id'],'hp':arm['hp'],'weak':st['r240']['outcome']['weak'],'speed':st['r240']['outcome']['speed_m'],
                        'score':st['r240']['outcome']['attack_score'],'damage':st['r240']['outcome']['damage_to_G'],'hit':st['r240']['outcome']['hit'],
                        'events':len(st['native_events']),'commits':rev,'head':head})
    report={'execution_status':'RUN_COMPLETED_PENDING_INDEPENDENT_AUDIT','arm_runs':len(out),'seed_clusters':len(P['seeds']),
     'native_turns':sum(z['commits'] for z in out),'native_events':sum(z['events'] for z in out),
     'official_cells':0,'terminal_contracts':0,'historical_replays':0,'results':out}
    (R/'reports/R240_RUN_RAW.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False))

if __name__=='__main__':run()
