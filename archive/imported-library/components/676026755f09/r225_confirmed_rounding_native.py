"""R225 isolated source-confirmed floor, source-gated native magical effect + arbitrary physical damage arithmetic.
ONE R18 commit per new independent fixture, never historical reuse.
"""
import sys, copy, json, hashlib
from pathlib import Path
from fractions import Fraction
from dataclasses import asdict
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r215_integrated_native as old
import vlab_r18_interactive as j
from vlab_effects_v08 import Scene,ActorActionState,cast_source_specified_spell,Resistances,DamageComponent,mitigate,EffectBlocked
DEC=json.loads((ROOT/'sources/R225_MASTER_DECISION_SOURCE.json').read_text());PR=json.loads((ROOT/'sources/R225_PREREG_BEFORE_EXEC.json').read_text());PH=hashlib.sha256((ROOT/'sources/R225_PREREG_BEFORE_EXEC.json').read_bytes()).hexdigest()
POL='FLOOR_MASTER_CONFIRMED_TEST';AUTH='USER_MESTRE_CONFIRMED_ALL_COMBAT_DAMAGE_2026-10-21'
def down_damage(numer,denom,kind,authority=AUTH):
    if authority!=AUTH:raise EffectBlocked('source gated Mestre clarification missing')
    if kind not in ('physical','magical','elemental','mixed-component'):raise EffectBlocked('invalid damage type')
    if type(numer)!=int or type(denom)!=int or numer<0 or denom<=0:raise EffectBlocked('invalid damage fraction')
    return Fraction(numer,denom).numerator//Fraction(numer,denom).denominator

def scene(st):
    return Scene({k:old.Combatant(**copy.deepcopy(v)) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R225-TEST-SOURCE-CONFIRMED-NOT-CANON')

def init(db,seed,damage,expected):
    j.init_db(str(db),'A',seed);st=j.initial('A',seed)
    a=old.actor('E');d=old.actor('R');a.standard=1
    st.update({'scene':f'R225-CONFIRMED-{seed}', 'seed':seed,'actors':{'E':asdict(a),'R':asdict(d)},'native_events':[],
      'phase':'ACTIVE','r225':{'decision':DEC['decision_id'],'pre_hash':PH,'expected_raw':expected,'damage':damage,'world_canon':False}})
    con=j.connect(str(db));h=j.sha({'seed':seed,'pre':PH,'run_id':db.name})
    with con:
        for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
    con.close()

def reducer(st,p,rev):
    if p['source']!=DEC['decision_id'] or p['pre']!=PH or st['r225']['damage']!=p['damage']:raise EffectBlocked('R225_SOURCE_GATE')
    s=scene(st);gross=p['damage'];sc=old.SPORES
    before_hp=s.actors['R'].hp;before_pa=s.actors['E'].pa
    e=cast_source_specified_spell(s,'E','R',source=sc,
      state=ActorActionState('E',20,s.actors['E'].pa,(sc.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('R',)),
      proofs=(old.PROOFS['E'],),damage=gross,damage_tag='planta',rd=Resistances(general=0,provenance='R225-NO-MAGICAL-RD-FIXTURE'),
      explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=True,odd_half_rounding_test_policy=POL,
      rounding_decision_source=AUTH,damage_rolls=tuple(p['dice']),damage_faces=10,documented_flat_bonus=10)
    if e['raw']!=p['expected'] or before_hp-s.actors['R'].hp!=p['expected'] or before_pa-s.actors['E'].pa!=80:raise EffectBlocked('R225_SCENE_ARITHMETIC_FAIL')
    st['native_events']=copy.deepcopy(s.events)
    st['actors']={k:asdict(v) for k,v in s.actors.items()};st['phase']='CENSORED_ONE_SPELL';st['r225']['result']=e
    return {'events_added':copy.deepcopy(s.events),'source':'MESTRE_CONFIRM_2026-10-21','no_attack_type_exception':True,'raw':e['raw']}

def run():
    results=[]
    for ix,c in enumerate(PR['new_runs'],1):
        db=ROOT/'evidence/db'/f'{c["id"]}_S{c['seed']}.sqlite'
        if db.exists():raise FileExistsError('RUN_ID_COLLISION:'+db.name)
        init(db,c['seed'],c['damage'],c['expected'])
        j.event_commit(str(db),f'LAB-CMD-R225-CONFIRMED-S{c['seed']}', 'R225_SOURCE_CONFIRMED_SPELL',{'source':DEC['decision_id'],'pre':PH,**c},reducer)
        st,head,rev=j.load(str(db));results.append({'run':c['id'],'seed':c['seed'],'db':db.name,'damage':c['damage'],'net':st['r225']['result']['raw'],'pa_spent':80,'commits':rev,'events':len(st['native_events']),'head':head})
    controls=[]
    for numer,denom,kind,expect in [(61,2,'physical',30),(61,2,'magical',30),(61,2,'elemental',30),(0,2,'physical',0),(1,2,'physical',0),(99,2,'magical',49),(60,2,'elemental',30),(61,2,'mixed-component',30)]:
        observed=down_damage(numer,denom,kind)
        if observed!=expect:raise AssertionError('DOWN_TEST_FAILED')
        controls.append({'kind':kind,'num':numer,'den':denom,'result':observed})
    mitigation=mitigate((DamageComponent(down_damage(61,2,'physical'),'impacto','R225-FIXTURE-PHYSICAL-HALF-ONLY'),),Resistances(general=5,provenance='R225-LAB-READ-ONLY'))
    assert mitigation.effective==25
    # transformation fractional carry is not a damage calculation and retains 5.5.
    from vlab_effects_v08 import AssimilatedSpirit,transformed_budget
    sp=AssimilatedSpirit('R225-TAP-CARRY-TEST',25,Fraction(11),{'FOR':5,'DES':0,'CON':0,'INT':0,'SAB':0,'CAR':0},{'CA':0},'R225-LAB-TEST')
    lv,pts,carry=transformed_budget(1,sp)
    assert (lv,pts,carry)==(1,5,Fraction(1,2))
    negatives=[]
    for name,kw in [('NO_AUTHORITY',{'authority':'NONE'}),('NEG_DAMAGE',{'numer':-1}),('ZERO_DENOM',{'denom':0}),('NON_DAMAGE',{'kind':'TAP'})]:
        d={'numer':61,'denom':2,'kind':'physical'};d.update(kw)
        try:down_damage(**d);raise AssertionError('UNAUTHORIZED_ARITHMETIC_ACCEPTED')
        except EffectBlocked as exc:negatives.append({'name':name,'reject':str(exc)})
    output={'status':'PASS_R225_CONFIRMED_FLOOR_NATIVE_SPELL_AND_TYPED_ARITHMETIC_TEST_ONLY','runs':results,'arithmetical_controls':controls,'mitigation_control':{'pre_rd':30,'rd':5,'net':25},'tap_carry':'1/2_PRESERVED','negative_precommit':negatives,'historical_replay':0}
    (ROOT/'evidence/reports/R225_RESULTS.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'commits':sum(x['commits'] for x in results),'runs':len(results),'controls':len(controls),'negative':len(negatives)},indent=2))
if __name__=='__main__':run()
