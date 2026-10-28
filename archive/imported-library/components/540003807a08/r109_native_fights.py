"""Continuity of original VLAB v0.8.1 and R18 durable event bridge.
Uses a patched COPY of vlab_effects_v08; no custom damage resolver. All
sources are experimental Master-side. Historical SQLite never touched.
"""
from __future__ import annotations
import copy,hashlib,json,sqlite3,sys,collections
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
NATIVE=ROOT/'native_v081_controlled'
STAGE12=ROOT.parent/'r61_extracted'/'work'/'fusion_stage12'
sys.path.insert(0,str(NATIVE));sys.path.insert(1,str(STAGE12))
import vlab_r18_interactive as core
# Stage12 gateway registers its historical rebuilt import paths; force this isolated
# controlled-copy module for NEW events only, leaving Stage12 SQLite core untouched.
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(NATIVE))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,
    ActorActionState,apply_weapon_attack,cast_source_specified_spell,begin_source_turn,end_source_turn,
    weak_status,effective_movement_speed,EffectBlocked)
from vlab_rd_v08 import Resistances

SRC={
 'B':{'name':'Grifo-Matriarca de Sílica L3','page':'3f3c2b324ede813987deda0b382e83c7','hp':4315,'pa':4016,'ca':153,'con':85,'reflex':0,'rd':75,'speed':63,'rank':'Lendário','rank_index':23,'atk':[6,6,138],'dmg':[[20,10]],'flat':0,'tag':'perfurante','spell':'Descarga Curta 14d10 Lightning Padrão 55 PA Reflexo CD94 reduz a metade'},
 'E':{'name':'Sikong Auren L3','page':'3ebc2b324ede814bb730d47dd7bd5f02','hp':523,'pa':719,'ca':225,'con':48,'reflex':2,'rd':35,'speed':64,'rank':'Lendário','rank_index':23,'atk':[6,6,193],'dmg':[[8,8]],'flat':211,'tag':'perfurante'},
 'F':{'name':'Sikong Feryn ON5 (NPC nao ED)','page':'3f6c2b324ede81ce9c61db8127bf0e31','hp':479,'pa':424,'ca':123,'con':24,'reflex':2,'rd':22,'speed':40,'rank':'Ouro Negro','rank_index':20,'atk':[4,6,92],'dmg':[[8,8]],'flat':47,'tag':'perfurante'}
}
SOURCE_TEXT={
 'B':'Grifo-Matriarca de Sílica|L3|Vida4315|Alma4016|CA153|RD75|Talão 6d6+138|20d10 perfurante|Descarga Curta Padrão 55PA 14d10 Lightning Reflexo CD94 reduz metade',
 'E':'Sikong Auren|L3|Vida523|PA719|CA225|RD fisico35|Lanca em duelo 6d6+193|Dano 8d8+211|Reflexo 6d6+166',
 'F':'Sikong Feryn|ON5|Vida479|PA424|CA123|RD22|Presas da Noite 4d6+92|Dano 8d8+47',
 'COMBAT':'Sistema Combate Regra6 critica dano normal + maximo de TODOS dados; Regra7 Fraco abaixo 10 por cento HP, desvantagem e metade deslocamento; Regra 5 -2 e menor de dois rolls',
 'BEAST':'Criacao Besta Regra9 Ouro ou superior abaixo 10 por cento HP pode realizar ataque critico especial e fica um turno imovel'
}
AUTH={'combat':'3ebc2b324ede81f1be4be8804ac113c0','beast':'3ebc2b324ede81f4992ac88a3588cacd',
 'Grifo':'3f3c2b324ede813987deda0b382e83c7', 'Auren':'3ebc2b324ede814bb730d47dd7bd5f02',
 'Feryn':'3f6c2b324ede81ce9c61db8127bf0e31'}
class Reject(ValueError):pass

def profile(actor):return SRC[actor]
def oracle_roll(seed,ix,scenario,actor,kind,count,faces):
    return core.dice(seed,ix,f'R109-{scenario}-{actor}-{kind}',count,faces)

def search_seed():
    """Directed engineering filter, never counted as random holdout."""
    for seed in range(915100,915800):
        if sum(oracle_roll(seed,1,'G_FULL','B','LIGHTNING',14,10))%2:continue
        if any((lambda z:z[:2]==[1,1] and z[2]<=2)([oracle_roll(seed,ix,'G_FULL',a,f'CRIT{j}',1,6)[0] for j in range(3)]) for a in 'BE' for ix in range(1,28)):continue
        for ix in range(2,27):
            crit=[oracle_roll(seed,ix,'G_FULL','B',f'CRIT{j}',1,6)[0] for j in range(3)]
            if crit[:2]==[6,6] and crit[2]>=5:return seed,ix
    raise Reject('DIRECTED_SEED_NOT_FOUND')

def make_prereg():
    seed,idx=search_seed()
    return {'operation':'OP-VLAB-FUSION-SANDBOX-01','baseline':'R01-R107 immutable',
      'stage':'R108-R117_NATIVE_V081_CONTROLLED_COPY', 'sources':AUTH,
      'r18_core':'original vlab_r18_interactive; SQLite only',
      'native_module':'controlled copy of historical vlab_effects_v08; legacy test baseline 28/28',
      'randomness':'experimental deterministic R18 core.dice; never campaign dice',
      'directed_development_seed':seed,'directed_search_range':[915100,915799],
      'directed_selection':'first seed with even 14d10 Lightning and natural 6,6,5|6 Grifo crit within own attack indexes 2..26; NOT INDEPENDENT HOLDOUT',
      'expected_crit_index':idx,'holdout_seed':919801,
      'final_effort_seed':919982,
      'sides':['B_LEFT','E_LEFT'],
      'G_FULL':{'initial':'FULL SOURCE HP/PA, source-legal basic and Lightning, Grifo first exogenous, no reactions or movement',
         'end':'KO or 60 actor turns; weak and native crit tracked; no natural initiative claim'},
      'F_EFFORT':{'initial':'Grifo L3 SOURCE MaxHP4315 but conditioned injured HP436 as LAB mid-scene fixture; Feryn ON5 full',
         'policy':'Feryn attacks first to trigger Fraco; Grifo deliberately elects optional final effort after a successful hit; immobilization for next OWN turn; non-ED technical only'},
      'no_repeat_R93_R95_R103':True,'terminal_claims':0}

PREREG_PATH=ROOT/'R111_PREREG_NATIVE_V081.json'
if PREREG_PATH.exists():PREREG=json.loads(PREREG_PATH.read_text())
else:
    PREREG=make_prereg();PREREG_PATH.write_text(json.dumps(PREREG,ensure_ascii=False,indent=2)+'\n')

def init_db(file,scenario,seed,side):
    if file.exists():raise Reject('NO-REPEAT_EXISTING_DB')
    core.init_db(file,'A',seed)
    s=core.initial('A',seed);s['scene']=f'R111-{scenario}-{seed}-{side}';s['run_id']=s['scene'];s['test_mode']='CONTROLLED_COPY_NATIVE_V081_ONLY';s['stage']='R109';s['phase']='ACTIVE';s['seed']=seed;s['order']=['B','E'] if scenario=='G_FULL' else ['F','B'];s['active']=s['order'][0];s['turn_index']=0;s['action_indexes']={a:0 for a in s['order']};s['winner']=None;s['source_digest']=core.sha(SOURCE_TEXT);s['experiment']={'scene':scenario,'opening':'EXOGENOUS_SOURCE_INITIATIVE_UNPROVEN','side':side,'terminal':False,'compared_as_independent_seed':False}
    actors={}
    for actor in s['order']:
        p=profile(actor)
        c=Combatant(actor,436 if actor=='B' and scenario=='F_EFFORT' else p['hp'],p['pa'],p['ca'],p['con'],0,0,p['reflex'],f'LAB-{side}-{actor}',rank=p['rank'],standard=0,maximum_hp=p['hp'],base_speed=p['speed'],beast_rank_index=p['rank_index'] if actor=='B' else None)
        resource=asdict(c)
        for k in ['ca','base_speed']:
            resource[k]=int(resource[k])
        actors[actor]={'source':p['page'],'stats':{'rank':p['rank'],'damage':p['dmg'],'att':p['atk'],'label':p['name']},'resource':resource}
    s['actors']=actors
    genesis=core.sha({'genesis':s,'source_digest':s['source_digest'],'engine':'R18+NATIVE_V081_CONTROLLED'})
    with core.connect(file) as con:
        for k,v in [('scene',s['scene']),('head',genesis),('genesis',genesis),('state',core.canonical(s))]:
            con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
    file.with_suffix('.genesis.json').write_text(core.canonical(s)+'\n')
    return s

def scene_from(s):return Scene({a:Combatant(**r['resource']) for a,r in s['actors'].items()},seed=s['seed'],provenance='SOURCE_MASTER_SUPPORT_PRECREATE_LAB_ONLY')
def source_and_state(s,actor,target,kind):
    if kind=='SPECIAL':
        p=profile(actor);src=AbilitySource('G-DESCARGA-CURTA','spell','STANDARD',p['page'],'GRIFO_DESCARGA_CURTA','RULE-DERIVED',required_pa=55,target_scope='ENEMY',requires_range_check=True,requires_line_of_sight=True,effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-CAST')
    else:
        p=profile(actor);src=AbilitySource(f'{actor}-BASIC','attack','STANDARD',p['page'],f'{actor}_BASIC_ATTACK','RULE-DERIVED',required_pa=0,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-WEAPON')
    st=ActorActionState(actor,p['rank_index'],s['actors'][actor]['resource']['pa'],(src.action_id,),standard_available=s['actors'][actor]['resource']['standard']==1,movement_available=True,reaction_available=True,range_confirmed=True,los_confirmed=True,geometry_confirmed=True,enemy_ids_visible=(target,))
    if actor=='B':excerpt=SOURCE_TEXT['B']
    else:excerpt=SOURCE_TEXT[actor]
    proof=FrozenRuleEvidence(p['page'],src.rule_id,hashlib.sha256(excerpt.encode()).hexdigest(),'2026-10-16_NOTION_PHYS_READ','R108_LOCAL_SOURCE_EXCERPT_FROZEN')
    return src,st,(proof,)

def attack_inputs(s,actor,target):
    sc=s['experiment']['scene'];ix=s['action_indexes'][actor]+1;p=profile(actor)
    crit=[oracle_roll(s['seed'],ix,sc,actor,f'CRIT{j}',1,6)[0] for j in range(3)]
    weak=s['actors'][actor]['resource']['hp']*10<s['actors'][actor]['resource']['maximum_hp']
    att=[oracle_roll(s['seed'],ix,sc,actor,f'HIT{j}',p['atk'][0],p['atk'][1]) for j in range(2 if weak else 1)]
    score=(min(sum(t) for t in att)-2 if weak else sum(att[0]))+p['atk'][2]
    # The duel title +8 starts on the third own attack; use only Auren against Grifo 1x1.
    passive=(8 if actor=='E' and sc=='G_FULL' and ix>=3 else 0)
    if passive:score+=passive
    damage=[oracle_roll(s['seed'],ix,sc,actor,f'DMG{j}',n,f) for j,(n,f) in enumerate(p['dmg'])]
    return {'actor':actor,'target':target,'ix':ix,'crit':crit,'attack_rolls':att,'score':score,
       'attack_bonus':p['atk'][2]+passive,'passive_bonus':passive,'damage_rolls':damage,
       'dmg':sum(sum(x) for x in damage)+p['flat'],'damage_groups':p['dmg'],'flat':p['flat'],
       'target_ca':profile(target)['ca']}

def special_inputs(s):
    if s['active']!='B':raise Reject('ONLY_GRIFO_SPECIAL')
    dmg=oracle_roll(s['seed'],1,'G_FULL','B','LIGHTNING',14,10)
    save=oracle_roll(s['seed'],1,'G_FULL','E','REFLEXO',6,6)
    # Auren's documented Reflexo shortcut 6d6+166 -> always surpasses 94.
    return {'actor':'B','target':'E','damage_rolls':dmg,'save_rolls':save,'save_bonus':166,'save_cd':94,
            'range_basis':'1.5m straight unobstructed LAB line; actual short-line maximum UNKNOWN',
            'raw':sum(dmg)}

def preflight(s,kind,payload):
    a=s['active']
    if s['phase']!='ACTIVE':raise Reject('NOT_ACTIVE')
    if kind=='TURN_START':
        if payload!={'actor':a}:raise Reject('WRONG_ACTOR_START')
        if s['actors'][a]['resource']['standard']!=0:raise Reject('STANDARD_NOT_SPENT_START')
    elif kind=='TURN_END':
        if payload!={'actor':a}:raise Reject('WRONG_ACTOR_END')
        if s['actors'][a]['resource']['standard']!=0:raise Reject('STANDARD_AVAILABLE_END')
    elif kind=='NATIVE_ATTACK':
        crit=payload.get('crit')
        if isinstance(crit,list) and crit[:2]==[1,1] and crit[2]<=2:raise Reject('CRITICAL_FAILURE_CONSEQUENCE_UNRESOLVED_BEFORE_INTENT')
        if payload.get('actor')!=a or payload.get('target') not in s['actors'] or payload['target']==a:raise Reject('ATTACK_ACTOR_TARGET')
        if s['actors'][a]['resource']['standard']!=1:raise Reject('NO_STANDARD_PRE_INTENT')
        if payload.get('final_effort') and not (a=='B' and s['actors'][a]['resource']['hp']*10<s['actors'][a]['resource']['maximum_hp'] and payload['score']>profile(payload['target'])['ca'] and payload['crit'][:2]!=[6,6]):raise Reject('FINAL_EFFORT_GATE_NO_INTENT')
    elif kind=='NATIVE_SPECIAL':
        if payload.get('actor')!='B' or a!='B' or payload.get('target')!='E':raise Reject('WRONG_SPELL_ACTOR')
        b=s['actors']['B']['resource']
        if b['standard']!=1 or b['pa']<55:raise Reject('SLOT_OR_PA_PRE_INTENT')
        if payload['raw']%2:raise Reject('ODD_HALF_ROUNDING_PRE_INTENT')
        if sum(payload['save_rolls'])+166<=94:raise Reject('SAVE_CONDITION_NOT_SATISFIED')
    else:raise Reject('UNRECOGNIZED_COMMAND')

def commit(db,kind,payload):
    s,head,rev=core.load(db);preflight(s,kind,payload)
    cmd='LAB-CMD-R109-'+core.sha({'run':s['run_id'],'head':head,'rev':rev,'type':kind,'payload':payload})[:38]
    def native_resolve(candidate,p,seq):
        sc=scene_from(candidate);active=candidate['active'];target=p.get('target');data={}
        if kind=='TURN_START':
            if candidate['actors'][active]['resource']['standard']!=0:raise Reject('NOT_STARTABLE')
            evt=begin_source_turn(sc,active)
        elif kind=='TURN_END':
            evt=end_source_turn(sc,active)
        elif kind=='NATIVE_ATTACK':
            src,st,proof=source_and_state(candidate,active,target,'BASIC');rd=Resistances(general=profile(target)['rd'],provenance='SOURCE-ONLY-GENERAL-PHYSICAL')
            evt=apply_weapon_attack(sc,active,target,source=src,state=st,proofs=proof,roll_score=p['score'],damage=p['dmg'],
                damage_tag=profile(active)['tag'],rd=rd,damage_dice_groups=tuple(map(tuple,p['damage_groups'])),
                damage_roll_groups=tuple(map(tuple,p['damage_rolls'])),damage_fixed_bonus=p['flat'],
                critical_sequence=tuple(p['crit']),attack_roll_attempts=tuple(map(tuple,p['attack_rolls'])),attack_bonus=p['attack_bonus'],
                final_effort=p.get('final_effort',False))
            candidate['action_indexes'][active]+=1
        elif kind=='NATIVE_SPECIAL':
            src,st,proof=source_and_state(candidate,active,target,'SPECIAL')
            # General physical/Dark defenses do not apply to Lightning source component.
            rd=Resistances(general=0,specific=(),provenance='TARGET_NO_DECLARED_LIGHTNING_RD_LAB_CONDITIONAL')
            evt=cast_source_specified_spell(sc,active,target,source=src,state=st,proofs=proof,
                damage=p['raw'],damage_tag='raio',rd=rd,explicit_save_effect='SAVE-HALF',
                target_save_exceeds_cd=sum(p['save_rolls'])+166>p['save_cd'],damage_rolls=tuple(p['damage_rolls']),damage_faces=10)
            data={'reflexo_score':sum(p['save_rolls'])+166,'reflexo_rolls':p['save_rolls'],'save_cd':94,'range_gate':'LAB_UNOBSTRUCTED_NEAR_LINE_NOT_OFFICIAL_MAX'}
        else:raise Reject('INVALID_NATIVE_KIND')
        for aid,c in sc.actors.items():
            obj=asdict(c)
            for k in ('ca','base_speed'):obj[k]=int(obj[k]) if obj[k] is not None else None
            candidate['actors'][aid]['resource']=obj
        if kind=='TURN_END':
            candidate['turn_index']+=1
            enemy='E' if active=='B' and 'E' in candidate['actors'] else 'F' if active=='B' else 'B'
            if candidate['actors'][enemy]['resource']['hp']<=0:
                candidate['phase']='FINISHED';candidate['winner']=active;candidate['active']=None
            else:candidate['active']=enemy
        if kind in ('NATIVE_ATTACK','NATIVE_SPECIAL') and candidate['actors'][target]['resource']['hp']==0:
            candidate['winner']=active
            # Turn end is still needed to preserve temporal action budget; finish on end.
        return {'native_action':evt,'source_module_version':__import__('vlab_effects_v08').VERSION,
          'scoped_legacy':False,'component':'v0.8.1 existing source gated adapter','extra':data,
          'actor':active,'target':target,'kind':kind}
    return core.event_commit(db,cmd,kind,payload,native_resolve)

def run_g_full(seed,side,max_actor_turns=60):
    file=ROOT/'r111_runs'/f'R111_FULL_{seed}_{side}.sqlite';file.parent.mkdir(exist_ok=True)
    s=init_db(file,'G_FULL',seed,side);visited=[]
    while True:
        s,_,rev=core.load(file)
        if s['phase']!='ACTIVE' or s['turn_index']>=max_actor_turns:break
        actor=s['active'];target='E' if actor=='B' else 'B'
        commit(file,'TURN_START',{'actor':actor})
        s,_,_=core.load(file)
        if actor=='B' and s['action_indexes']['B']==0:
            ins=special_inputs(s)
            if ins['raw']%2:raise Reject('SOURCE_BOUND_HALF_ODD_SELECTED_SEED')
            commit(file,'NATIVE_SPECIAL',ins)
        else:
            ins=attack_inputs(s,actor,target)
            commit(file,'NATIVE_ATTACK',ins)
        commit(file,'TURN_END',{'actor':actor})
    return summarize(file,'G_FULL',seed,side)

def run_f_effort(seed,side):
    file=ROOT/'r111_runs'/f'R111_EFFORT_{seed}_{side}.sqlite';file.parent.mkdir(exist_ok=True)
    init_db(file,'F_EFFORT',seed,side)
    sequence=['F','B','F','B']
    for actor in sequence:
        s,_,_=core.load(file)
        if s['phase']!='ACTIVE':break
        if s['active']!=actor:raise Reject('TURN_POLICY_ACTOR_MISMATCH')
        target='B' if actor=='F' else 'F'
        commit(file,'TURN_START',{'actor':actor})
        s,_,_=core.load(file)
        ins=attack_inputs(s,actor,target)
        if actor=='B' and s['action_indexes']['B']==0:
            ins['final_effort']=True
        commit(file,'NATIVE_ATTACK',ins)
        commit(file,'TURN_END',{'actor':actor})
    return summarize(file,'F_EFFORT',seed,side)

def summarize(file,scenario,seed,side):
    s,head,revision=core.load(file)
    with sqlite3.connect(file) as c:rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
    con=sqlite3.connect(file);backup=sqlite3.connect(file.with_suffix('.checkpoint.sqlite'))
    try:con.backup(backup)
    finally:con.close();backup.close()
    if core.load(file)!=core.load(file.with_suffix('.checkpoint.sqlite')):raise Reject('CHECKPOINT_DIFF')
    acts=[e for e in rows if e['kind']=='NATIVE_ATTACK'];specials=[e for e in rows if e['kind']=='NATIVE_SPECIAL']
    return {'run_id':s['run_id'],'scenario':scenario,'seed':seed,'side':side,'events':revision,'head':head,
        'phase':s['phase'],'winner':s['winner'],'actor_turns':s['turn_index'],
        'source_basic_attacks':len(acts),'native_specials':len(specials),
        'critical_positive_count':sum(e['detail']['native_action']['critical']=='POSITIVE' for e in acts),
        'weak_attacks':sum(e['detail']['native_action']['weak_attacker'] for e in acts),
        'final_efforts':sum(e['detail']['native_action']['final_effort'] for e in acts),
        'pa_costed':sum(e['detail']['native_action'].get('PA_spent',0) for e in specials),
        'hp_final':{x:round(s['actors'][x]['resource']['hp']) for x in s['actors']},
        'checkpoint':file.with_suffix('.checkpoint.sqlite').name,'ledger':file.name,'terminal':False}

def main():
    results=[]
    for seed in [PREREG['directed_development_seed'],PREREG['holdout_seed']]:
        for side in PREREG['sides']:
            if sum(oracle_roll(seed,1,'G_FULL','B','LIGHTNING',14,10))%2:
                results.append({'seed':seed,'side':side,'status':'ROUNDING_HOLD_NO_INTENT'});continue
            results.append(run_g_full(seed,side))
    for side in PREREG['sides']:
        results.append(run_f_effort(PREREG['final_effort_seed'],side))
    (ROOT/'R109_NEW_NATIVE_BATTLES.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'results':results},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
