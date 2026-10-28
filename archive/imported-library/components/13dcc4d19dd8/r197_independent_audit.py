#!/usr/bin/env python3
"""Separated-code source-anchor and math audit for VLAB R197; NO EXTERNAL AUDITOR.

Does not import r197_power_bench or execute battles. Fixed source anchors copied
from page reopens and explicit scope. Checks semantic data even if JSON digests
were recomputed by a forger; source authenticity still requires Notion reread.
"""
import collections,hashlib,json,pathlib,statistics,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent

# Checked against Mestre-page reopens on 2026-10-19. Deliberately sparse, not self-signed by producer.
TRUSTED={
 'CONCHA_P1':('474c2b324ede82d08ea6819069c17043','Prata',1,210,40,30,((3,6),),30),
 'TIGRIS_P1':('725c2b324ede8301baed01d62bd2b8e0','Prata',1,198,33,24,((2,6),),24),
 'LOBO_P1':('be5c2b324ede832e8b7a81c5460571c1','Prata',1,240,34,24,((1,6),),24),
 'CABRA_P1':('b34c2b324ede82a88079016b52ba498e','Prata',1,240,39,25,((2,4),),25),
 'RAIOS_P1':('778c2b324ede83d0a89281a4c12ba768','Prata',1,216,33,23,((2,6),),23),
 'MACACO_P5':('301c2b324ede828caccb813d3979267a','Prata',5,750,67,54,((2,6),),54),
 'BEHEMOTH_P5':('1fdc2b324ede82bd9d4f811abb689440','Prata',5,500,61,15,((3,6),),15),
 'LIU_P5':('0b4c2b324ede837cb6be818dc8e36010','Prata',5,235,46,None,((5,12),(3,8),(1,6)),45),
 'AUREN_L3':('3ebc2b324ede814bb730d47dd7bd5f02','Lendário',3,523,225,None,((8,8),),211)
}
def verify_files(source_path=None,profile_path=None,history_path=None,base_zip_path=None):
    paths={'source':pathlib.Path(source_path or ROOT/'source/R197_SOURCE_SNAPSHOTS.json'),
           'profiles':pathlib.Path(profile_path or ROOT/'evidence/R197_PROFILES.json'),
           'history':pathlib.Path(history_path or ROOT/'evidence/R197_PRIOR_R196_EVIDENCE_READ_ONLY.json'),
           'base_zip':pathlib.Path(base_zip_path or ROOT/'baseline/VLAB_R187_R196_EXACT.zip')}
    s=json.loads(paths['source'].read_text());p=json.loads(paths['profiles'].read_text());h=json.loads(paths['history'].read_text())
    actors=s['actors'];reports=p['actors'];by={a['id']:a for a in actors};br={a['id']:a for a in reports}
    if set(by)!=set(TRUSTED) or len(actors)!=len(TRUSTED) or set(br)!=set(by):raise AssertionError('SOURCE_ID_SET_CHANGED')
    if s['as_of']!='2026-10-19' or p['source_count']!=len(actors):raise AssertionError('SCOPE_MISMATCH')
    accepted=[]
    for k,(uuid,rank,star,hp,ca,stat,groups,flat) in TRUSTED.items():
        a=by[k];r=br[k];at=a['attack']
        if not a['url'].endswith(uuid) or a['rank']!=rank or a['star']!=star or a['hp']!=hp or a['ca']!=ca:
            raise AssertionError('SOURCE_SEMANTIC_ANCHOR_CHANGED:'+k)
        if tuple(tuple(x) for x in at['damage_dice'])!=groups or at['damage_flat']!=flat:raise AssertionError('DAMAGE_TAPE_CHANGED:'+k)
        if stat is not None and a['stats'][at['hit_stat']]!=stat:raise AssertionError('HIT_ATTRIBUTE_CHANGED:'+k)
        expected=flat+sum(n*(f+1)/2 for n,f in groups)
        if r['attack']['mean']!=expected or r['attack']['minimum']!=flat+sum(n for n,f in groups):raise AssertionError('DAMAGE_MATH_CHANGED:'+k)
        if r['source_url']!=a['url'] or r['rank']!=rank or r['star']!=star or r['hp']!=hp or r['ca']!=ca:raise AssertionError('PROFILE_SOURCE_DISCONNECT:'+k)
        if r['rank_reclassification_authorized'] or r['power_index'] is not None:raise AssertionError('UNAUTHORIZED_POWER_PROMOTION:'+k)
        accepted.append(k)
    p1=[by[x] for x in TRUSTED if x.endswith('_P1')]
    if len(p1)!=5:raise AssertionError('DENOMINATOR_WRONG')
    means=[a['attack']['damage_flat']+sum(n*(f+1)/2 for n,f in a['attack']['damage_dice']) for a in p1]
    if statistics.median(means)!=30 or statistics.median(x['hp'] for x in p1)!=216 or statistics.median(x['ca'] for x in p1)!=34:raise AssertionError('P1_REFERENCE_WRONG')
    concha=br['CONCHA_P1'];bt=concha['target_ca_analysis']['branches'];
    # Default profile targets its own CA 40. Formula no critical: 2d6+30 or +38.
    true0=sum(1 for x in range(1,7) for y in range(1,7) if x+y+30>40)/36
    true8=sum(1 for x in range(1,7) for y in range(1,7) if x+y+38>40)/36
    if abs(bt['untrained']['hit_probability_excluding_critical']-true0)>1e-10 or abs(bt['trained_if_confirmed']['hit_probability_excluding_critical']-true8)>1e-10:raise AssertionError('HIT_MATH_MISMATCH')
    if br['MACACO_P5']['peer_cohort']['n']!=1 or br['BEHEMOTH_P5']['peer_cohort']['n']!=1:raise AssertionError('TITAN_POOLING')
    if p['official_contracts_certified']!=0 or p['official_benchmark_cells']!=0 or p['independent_fight_observations_new']!=0:raise AssertionError('MISREPRESENTED_CREDIT')
    bz=hashlib.sha256(paths['base_zip'].read_bytes()).hexdigest()
    if bz!='7dc3a95aafa7dfc4db6ae0d99f7c0474e630ea86f0f70dff4112abf771403786' or h['baseline_zip_sha256']!=bz:raise AssertionError('R196_HISTORICAL_BASELINE_CHANGED')
    if h['seed_blocks']!=5 or h['branches_per_seed']!=8 or h['total_conditional_runs']!=40 or h['winner_LIU']!=40 or h['rounds_observed']!=[3] or len(h['per_seed'])!=5:raise AssertionError('HISTORIC_DENOMINATOR_DRIFT')
    if any(z['runs']!=8 or z['winner_count']!=8 for z in h['per_seed']):raise AssertionError('HISTORIC_BRANCH_DATA_TAMPER')
    return {'status':'PASS_R197_LOCAL_INDEPENDENT_CODE_AUDIT','source_anchors_checked':len(accepted),'same_rank_reference_n':5,
            'historical_r196_sha':bz,'historical_r196_seed_blocks':5,'historical_r196_conditional_runs':40,
            'new_official_benchmarks':0,'new_combat_effects':0,'external_human_audit':False}

def adversarial_cases():
    import copy,tempfile
    s=json.loads((ROOT/'source/R197_SOURCE_SNAPSHOTS.json').read_text());p=json.loads((ROOT/'evidence/R197_PROFILES.json').read_text())
    base=(ROOT/'baseline/VLAB_R187_R196_EXACT.zip')
    h=ROOT/'evidence/R197_PRIOR_R196_EVIDENCE_READ_ONLY.json'
    mutations=[('attack_flat',lambda ss,pp: ss['actors'][0]['attack'].__setitem__('damage_flat',31)),
               ('identity_uuid',lambda ss,pp: ss['actors'][0].__setitem__('url','https://app.notion.com/p/00000000000000000000000000000000')),
               ('hp',lambda ss,pp: ss['actors'][0].__setitem__('hp',9999)),
               ('cohort',lambda ss,pp: pp['actors'][5]['peer_cohort'].__setitem__('n',2)),
               ('official_credit',lambda ss,pp: pp.__setitem__('official_benchmark_cells',1)),
               ('mean',lambda ss,pp: pp['actors'][0]['attack'].__setitem__('mean',99.0)),
               ('hit_prob',lambda ss,pp: pp['actors'][0]['target_ca_analysis']['branches']['untrained'].__setitem__('hit_probability_excluding_critical',1.0))]
    rejects=[]
    with tempfile.TemporaryDirectory() as tmp:
        td=pathlib.Path(tmp)
        for name,mutate in mutations:
            ss=copy.deepcopy(s);pp=copy.deepcopy(p);mutate(ss,pp)
            source=td/f'{name}_s.json';prof=td/f'{name}_p.json';source.write_text(json.dumps(ss));prof.write_text(json.dumps(pp))
            # all local file hashes could be recomputed; semantic check uses separate anchors.
            try:verify_files(source,prof,h,base)
            except AssertionError as e:rejects.append({'name':name,'reject':str(e)})
            else:raise AssertionError('ADVERSARIAL_CLONE_ACCEPTED:'+name)
    return rejects

if __name__=='__main__':
    r=verify_files();r['semantic_clones_rejected']=adversarial_cases();print(json.dumps(r,ensure_ascii=False,indent=2))
