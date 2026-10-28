"""R200 actual FULL fights: source-derived Orc B1/P1 vs real Bronze Besta/P1 Lobo.
Reuses R198 wrapper, v0.8.1 native damage and R18 SQLite/event_commit. R199 unchanged.
Ring +2 CA and 13PA/day uses NOT-GRADE-CERTIFIED-LAB-PROXY, not a legal rank proof.
"""
from __future__ import annotations
import sys,os,json,hashlib,pathlib,copy
from collections import Counter
from dataclasses import asdict
HERE=pathlib.Path(__file__).resolve().parent
R200=HERE.parent
OLD=R200.parents[0]/'previous'
sys.path.insert(0,str(OLD/'new/code'))
sys.path.insert(0,str(HERE))
import r198_microbenchmark as base
from r200_equipment_and_profiles import build_profile,state,weapon,ff_roll,SOURCES
from vlab_effects_v08 import Combatant,AbilitySource,FrozenRuleEvidence,EffectBlocked
PREPATH=R200/'source/R200_PRE_REG.json'
PRE=json.loads(PREPATH.read_text());PRE_SHA=hashlib.sha256(PREPATH.read_bytes()).hexdigest()

# Strict isolation: change only the imported module in THIS new Python process.
base.VERSION='R200-SOURCE-FROZEN-ED-REF-01-SWORD-PHYSICAL-AND-RING-PROXY-LAB-1'
base.PRE=PRE;base.PRE_SHA=PRE_SHA
base.SOURCE_SHA=hashlib.sha256((json.dumps({'source':PRE['sources'],'actor':'ED-REF-01'})).encode()).hexdigest()

def import_actor(x):
    if x['id'] in base.ACTORS:raise ValueError('R200 ACTOR ID COLLISION')
    base.ACTORS[x['id']]=x
    s=json.dumps({'id':x['id'],'source':x['url'],'attack':x['attack_name'],'dice':x['damage_dice'],'test_assumptions':PRE['assumptions']},sort_keys=True,ensure_ascii=False)
    ev=FrozenRuleEvidence(x['url'],base.VERSION+'-'+x['id'],hashlib.sha256(s.encode()).hexdigest(),x['edited'],'R200-SOURCE-PAGE-REOPENED-NOT-FULLY-PROVEN-ITEM-RANK')
    source=AbilitySource(base.VERSION+'-ATT-'+x['id'],'attack','STANDARD',x['url'],ev.rule_id,'RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='EXISTING-V081-SOURCE-ONLY')
    base.EVIDENCE[x['id']]=ev;base.ABILITY[x['id']]=source

def ref_actor(level):
    p=build_profile(level)
    ident=f'ED-REF-01-{"B1" if level==1 else "P1"}'
    d=p['weapon']['physical_dice']
    return {'id':ident,'kind':'ED_TEST','name':f'ED-REF-01 Orc TEST nível {level}',
        'url':SOURCES['creation'],'edited':'2026-10-09T04:07:06.313Z','rank':'BRONZE' if level==1 else 'PRATA',
        'star':p['rank_star'],'level':level,'hp':p['natural_hp_max'],'maximum_hp':p['natural_hp_max'],
        'pa':p['natural_pa_max'],'ca':float(__import__("fractions").Fraction(p["ca_physical_exact"])), 'dex':p['natural_current']['DES'],
        'init_dice':(1,6) if level==1 else (2,6),
        'initiative_bonus':p['natural_current']['DES']+2,'attack_dice':(1,6) if level==1 else (2,6),
        'attack_bonus':p['natural_current']['FOR']+2,'damage_dice':(d,),
        'damage_flat':p['ff_damage_bonus'],'damage_tag':'cortante','damage_tag_status':'LAB_SWORD_SLASH_TYPED_BY_WEAPON',
        'rd':0,'rd_status':'LAB_UNPUBLISHED_PERSONAL_RD_ZERO','attack_name':f'espada_fisica_{p["rank"]}',
        'ability_scope':'LAB_PROSPECTIVE_CLASSIFIED_PHYSICAL_SWORD; TWO MAGIC STATES DO NOT CHANGE PHYSICAL_DICE',
        'profiles':p}

gal={'id':'GALINHA_B1','kind':'BEAST','name':'Galinha Demoníaca (Galidemus) B1',
    'url':SOURCES['galinha'],'edited':'2026-10-01T18:00:52.905Z','rank':'BRONZE','star':1,'level':1,
    'hp':32,'maximum_hp':32,'pa':32,'ca':21,'dex':13,'init_dice':(1,6),'initiative_bonus':13,
    'attack_dice':(1,6),'attack_bonus':13+6,'damage_dice':((1,4),),'damage_flat':13,
    'damage_tag':'cortante','damage_tag_status':'SOURCE_LITERAL_CORTANTE',
    'rd':5,'rd_status':'BEAST_CREATION_RULE_BRONZE_NORMAL_RD5','attack_name':'Patada 1d4+DES',
    'ability_scope':'SOURCE_ATTACK_PATADA; LAB_HYPOTHESIS_GENERIC_BEAST_PROFICIENCY_IN_LUTA'}
for obj in (ref_actor(1),ref_actor(6),gal):import_actor(obj)
assert 'LOBO_P1' in base.ACTORS
PAIRINGS=tuple(tuple(x)for x in PRE['pairs'])

def init(db,seed,pair,policy):
    base.r18.init_db(str(db),'A',seed)
    st=base.state_genesis(seed,pair)
    st.update({'r200_pre_sha':PRE_SHA,'r200_policy':policy,'r200_provenance':'NEW_ORC_TEST_SOURCE_PLUS_ITEM_PROXY_UNRANKED',
      'scene_id':f'R200-SCENE-{db.stem}', 'ring':{'active':policy=='COM_MAGIA_ITEM_PROXY_UNRANKED_TEST',
          'source':SOURCES['ring'],'source_rank':'UNPUBLISHED','daily_PA_cost_at_entry_TEST':13 if policy!='SEM_MAGIA_ITEM' else 0,
          'equipment_id':'R200-TEST-RING-PROXY-01','original_item_not_modified':True}})
    who=pair[0]
    if policy=='COM_MAGIA_ITEM_PROXY_UNRANKED_TEST':
        resource=st['actors'][who]['resource'];resource['ca']+=2;resource['pa']-=13
        if resource['pa']<0:raise RuntimeError('UNFUNDED_MAGIC_PROXY')
    conn=base.r18.connect(str(db))
    try:
        with conn:conn.execute('UPDATE meta SET value=? WHERE key="state"',(base.r18.canonical(st),))
    finally:conn.close()

def start(st,p,seq):
    if st['r200_pre_sha']!=PRE_SHA or p.get('r200_pre_sha')!=PRE_SHA or p.get('policy')!=st['r200_policy']:raise EffectBlocked('R200_PREREG_DISAGREEMENT')
    return base.start(st,{k:v for k,v in p.items() if k not in ('r200_pre_sha','policy')},seq)

def run(seed,level,policy,output):
    pair=PAIRINGS[0 if level==1 else 1];ident=f'R200_EDREF_L{level}_{pair[1]}_S{seed}_{policy}'
    db=pathlib.Path(output)/(ident+'.sqlite')
    if db.exists():raise RuntimeError('HISTORIC_OR_NEW_RUN_ID_REUSED')
    vals,order=base.roll_initiative(seed,pair)
    if order is None:return {'id':ident,'seed':seed,'level':level,'policy':policy,'status':'PRECOMMIT_TIE_HOLD', 'db':None}
    init(db,seed,pair,policy)
    payload={'initiative':vals,'order':order,'pre_reg_sha':base.PRE_SHA,'source_snap_sha':base.SOURCE_SHA,'r200_pre_sha':PRE_SHA,'policy':policy}
    base.r18.event_commit(str(db),'LAB-CMD-'+ident+'-INIT','R200_SOURCE_SCOPED_INIT',payload,start)
    for i in range(PRE['horizon_attacks']):
        st,_,_=base.r18.load(str(db))
        if st['phase']=='FINISHED':break
        who=st['active'];target=next(x for x in pair if x!=who)
        turn=1+sum(x['actor']==who for x in st['history']);r=st['actors'][who]['resource'];weak=r['hp']>0 and 10*r['hp']<r['maximum_hp']
        p={'actor':who,'target':target,'own_turn':turn,'roll_tape':base.tape(seed,pair,who,turn,weak)}
        base.r18.event_commit(str(db),'LAB-CMD-'+ident+f'-A{i+1:03d}','R200_SOURCE_SWORD_OR_BEAST_ATTACK',p,base.attack)
    st,head,rev=base.r18.load(str(db));base.write_checkpoint(str(db))
    attacks=[e for e in st['native_events'] if e.get('action')=='weapon_attack']
    result={'id':ident,'seed':seed,'level':level,'policy':policy,'status':'FINISHED' if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
       'winner':st['winner'] if st['phase']=='FINISHED' else None,'rounds':st['round'],'rev':rev,'head':head,
       'events':len(st['native_events']),'attacks':len(attacks),'damage_effective_by_actor':{a:sum(e['hp_loss_actual'] for e in attacks if e['from']==a)for a in pair},
       'hits_by_actor':{a:sum(1 for e in attacks if e['from']==a and e['hit'])for a in pair},
       'initial_ca':{'SEM_MAGIA_ITEM':base.ACTORS[pair[0]]['ca'],'COM_MAGIA_ITEM_PROXY_UNRANKED_TEST':base.ACTORS[pair[0]]['ca']+2}[policy],
       'final_hp':{a:s['resource']['hp'] for a,s in st['actors'].items()},
       'final_pa':{a:s['resource']['pa'] for a,s in st['actors'].items()},
       'ring_magic_grade_source':'UNPUBLISHED_NOT_FULLY_LEGAL','magic_pa_at_entry_TEST':13 if policy!='SEM_MAGIA_ITEM' else 0,
       'equipment_physical_unchanged':True,'db':db.name}
    return result

def main():
    output=R200/'evidence/db';output.mkdir(parents=True,exist_ok=True)
    results=[run(seed,level,policy,output)for level in (1,6) for seed in PRE['seeds'] for policy in PRE['policies']]
    (R200/'evidence/R200_EXECUTED_FIGHTS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
    from collections import defaultdict
    agg=defaultdict(Counter)
    for x in results:agg[f'{x["level"]}|{x["policy"]}'].update([x['winner'] if x['status']=='FINISHED' else x['status']])
    print(json.dumps({'runs':len(results),'finished':sum(x['status']=='FINISHED' for x in results),'hold':sum(x['status']=='PRECOMMIT_TIE_HOLD' for x in results),'censored':sum(x['status']=='CENSORED_HORIZON' for x in results),'results':{k:dict(c)for k,c in agg.items()}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
