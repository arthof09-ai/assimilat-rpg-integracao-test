#!/usr/bin/env python3
"""VLAB R197 MESTRE-SIDE: thin fast power-assessment adapter, not a combat engine.

Reads original Mestre-page values frozen in versioned JSON. Reuses the
pre-existing VLAB monster_calibration_v01 guard; NEVER updates rank/star.
Recomputes exact 2d6/6d6 attack distributions analytically. Does not import
D&D or price magic-item PA, and does not perform official simulations.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,pathlib,statistics,sys
from fractions import Fraction

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
SOURCES=ROOT/'source'/'R197_SOURCE_SNAPSHOTS.json'
LEGACY=ROOT/'legacy'
sys.path.insert(0,str(LEGACY))
from monster_calibration_v01 import BeastEvaluation,aggregate  # EXISTING guard, unchanged

VERSION='R197-PROFILE-THIN-ADAPTER-v1'

def json_sha(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def load(path=SOURCES):
    p=pathlib.Path(path);sources=json.loads(p.read_text(encoding='utf8'))
    ids=[a['id'] for a in sources['actors']]
    if len(set(ids))!=len(ids):raise ValueError('DUPLICATE_SOURCE_ID')
    for a in sources['actors']:
        if not a['url'].startswith('https://app.notion.com/p/') or not a.get('page_last_edited_at'):
            raise ValueError('PROVENANCE_MISSING')
        if not (isinstance(a['hp'],int) and a['hp']>0 and isinstance(a['ca'],int) and a['ca']>=0):
            raise ValueError('INVALID_SOURCE_STATS')
        if not 1<=a['star']<=5:raise ValueError('INVALID_STAR')
        b=a['attack']
        if not b['damage_dice'] or any(len(g)!=2 or g[0]<=0 or g[1]<2 for g in b['damage_dice']):
            raise ValueError('INVALID_ATTACK_EXPRESSION')
        if b['hit_flat_source'] is None and b['hit_stat'] not in a['stats']:
            raise ValueError('HIT_STAT_MISSING')
        if a['rd_physical']['status'] not in ('SOURCE_EXPLICIT','RULE_DERIVED_CONDITIONAL','UNKNOWN'):
            raise ValueError('INVALID_RD_AUTHORITY')
    return sources

def dice_stats(attack):
    dice=attack['damage_dice'];fixed=attack['damage_flat']
    return {'minimum':fixed+sum(n for n,f in dice),
            'mean':fixed+sum(n*(f+1)/2 for n,f in dice),
            'maximum':fixed+sum(n*f for n,f in dice),
            'expression':attack['damage_literal']}

def dice_sum_prob(n,faces):
    d={0:1}
    for i in range(n):
        q=collections.Counter()
        for k,v in d.items():
            for r in range(1,faces+1):q[k+r]+=v
        d=q
    den=faces**n
    return {k:Fraction(v,den) for k,v in d.items()}

def hit_prob(dice,bonus,target_ca):
    if bonus is None:return None
    n,faces=dice
    return sum((p for result,p in dice_sum_prob(n,faces).items() if result+bonus>target_ca),Fraction(0))

def attack_bonus_branches(a):
    t=a['attack']
    if t['hit_flat_source'] is not None:
        return {'published':{'bonus':t['hit_flat_source'],'status':'SOURCE_EXPLICIT'}}
    base=a['stats'][t['hit_stat']]
    branches={'untrained':{'bonus':base,'status':'LAB_HYPOTHESIS_NO_NAMED_LUTA'}}
    if t['trained_bonus_if_confirmed'] is not None:
        branches['trained_if_confirmed']={'bonus':base+t['trained_bonus_if_confirmed'],'status':'LAB_HYPOTHESIS_PROFICIENCY_IF_NAMED'}
    return branches

def rank_peers(a,all_actors):
    # ED vs Beast never pooled as same cohort: correct denominator is actual peer species.
    return [x for x in all_actors if x['kind']==a['kind'] and x['rank']==a['rank'] and x['star']==a['star'] and x.get('titan_status')==a.get('titan_status')]

def pct_diff(x,base):return None if base==0 else 100*(x/base-1)

def report(a,actors,target_ca=None,target_rd=None):
    attack=a['attack'];damage=dice_stats(attack)
    peer=rank_peers(a,actors)
    med={k:statistics.median([dice_stats(p['attack'])['mean'] if k=='damage_mean' else p[k] for p in peer]) for k in ('damage_mean','hp','ca')}
    vals={'damage_mean':damage['mean'],'hp':a['hp'],'ca':a['ca']}
    compare={k:{'value':vals[k],'sample_median':med[k], 'difference':vals[k]-med[k], 'percent_difference':round(pct_diff(vals[k],med[k]),2)} for k in med}
    ca=target_ca if target_ca is not None else a['ca']
    branches=attack_bonus_branches(a)
    hit={k:{**v,'hit_probability_excluding_critical':float(hit_prob(attack['hit_test_dice'],v['bonus'],ca)),
             'target_ca':ca} for k,v in branches.items()}
    hit_bounds=[v['hit_probability_excluding_critical'] for v in hit.values()]
    rd_scenario=target_rd
    # This is an arithmetic damage projection, NEVER a claim of typed source damage.
    projected={} if target_rd is None else {
        'status':'SCENARIO_ASSUME_ALL_DAMAGE_AFFECTED_BY_THIS_RD',
        'target_rd':target_rd,
        'nominal_mean_minus_rd_floor_zero':None,
        'exact_expected_hit_damage_after_rd':float(expected_post_rd(attack,target_rd)),
        'damage_type_status':attack['damage_type'],
        'caveat':'An analytic what-if; not a mixed damage or critical resolver.'}
    uncertainties=[]
    if attack['hit_flat_source'] is None:
        width=max(hit_bounds)-min(hit_bounds)
        uncertainties.append({'field':'Luta específica','decision_relevance':'HIGH' if width>=.10 else 'LOW_FOR_TARGET_CA', 'effect_at_target_ca':round(width,4), 'note':'Branches assume attribute relevant and prof only if independently recorded.'})
    if attack['damage_type'].startswith('UNKNOWN'):
        uncertainties.append({'field':'Tipagem do dano','decision_relevance':'HIGH_IF_TARGET_HAS_TYPED_RD', 'note':'Nominal damage is valid but post-RD depends on typing.'})
    if 'paralis' in attack['ability_note'].lower() or 'duplo' in attack['name'].lower() or '+2 ataque' in attack['ability_note'].lower():
        uncertainties.append({'field':'Rider/ações especiais','decision_relevance':'SCENARIO_DEPENDENT','note':attack['ability_note']})
    if a['rd_physical']['status']!='SOURCE_EXPLICIT':
        uncertainties.append({'field':'RD do próprio ator','decision_relevance':'HIGH_IF_OPPONENT_DEALS_PHYSICAL_DAMAGE','note':'Rule-derived RD is conditional on applicable variant / traits, never a published character-page literal.'})
    return {
        'id':a['id'],'name':a['name'],'kind':a['kind'],'rank':a['rank'],'star':a['star'],
        'source_url':a['url'],'source_edited':a['page_last_edited_at'],
        'status':'SOURCE_DOCUMENTED_PROFILE_CONDITIONAL_HIT' if a['kind']=='BEAST' else 'SOURCE_DOCUMENTED_PROFILE',
        'hp':a['hp'],'pa':a['pa'],'ca':a['ca'],'rd':a['rd_physical'],
        'attack':{'name':attack['name'],**damage,'damage_type':attack['damage_type'],'cost_pa':attack['cost_pa'],'note':attack['ability_note']},
        'peer_cohort':{'rank':a['rank'],'star':a['star'],'kind':a['kind'],'n':len(peer),'ids':sorted(x['id'] for x in peer),'same_rank_star_only':True,'titan_status':a.get('titan_status','UNKNOWN'),
                       'not_population_census':True},
        'peer_comparison':compare,
        'target_ca_analysis':{'ca':ca,'critical_model':'EXCLUDED_UNRESOLVED_SEPARATE','branches':hit},
        'conditional_rd_projection':projected,
        'uncertainties':uncertainties,'source_conflicts':a.get('source_conflicts',[]),
        'power_index':None,'rank_reclassification_authorized':False,
        'recommendation':recommend(a,compare,len(peer)),
        'assessment_version':VERSION
    }

def expected_post_rd(attack,rd):
    """Exact dice-distribution expected damage after fixed what-if RD, no attack check."""
    if not isinstance(rd,int) or rd<0:raise ValueError('RD must be nonnegative integer')
    d={0:Fraction(1)}
    for n,f in attack['damage_dice']:
        d2=dice_sum_prob(n,f);q=collections.defaultdict(Fraction)
        for i,p in d.items():
            for j,p2 in d2.items():q[i+j]+=p*p2
        d=dict(q)
    return sum((p*max(0,s+attack['damage_flat']-rd) for s,p in d.items()),Fraction(0))

def recommend(a,comparison,n):
    if n<3:return 'REFERENCE_SPARSE: no same-rank distribution conclusion from fewer than 3 examples.'
    d=comparison['damage_mean']['percent_difference']
    if d>0:
        return 'Nominal damage exceeds median of inspected same-rank-star pages; test hit odds and typed RD before any balance adjustment.'
    if d<0:
        return 'Nominal damage below inspected median; first inspect hit odds, defenses, rider effects and play role.'
    return 'Nominal damage equals inspected median; no general power equivalence implied.'

def all_reports(source,ca=None,rd=None):
    actors=source['actors'];return [report(a,actors,target_ca=ca,target_rd=rd) for a in actors]

def legacy_safety_check():
    # Use existing historic calibration validator only for the status guarantee.
    rec=BeastEvaluation('R197-CURATED-NO-RUN','R197-RESEARCH','Prata',1,(), 'HYPOTHETICAL','Prata',1,1,'none','R197',0,'','SOURCE-VALIDATED',None,None,None,None,None,None,'DMG-RANK-01 v1.1','R197_FROZEN','TEST-ONLY')
    result=aggregate([rec])
    assert result['canonical_rank_change_authorized'] is False
    assert result['status']=='EVIDENCE-INSUFFICIENT'
    return {'historical_validator_reused':True,'historical_rank_change_authorized':False,'historical_status':result['status']}

def generate(out=None):
    s=load();a=all_reports(s)
    output={'version':VERSION,'as_of':s['as_of'],'source_snapshot_sha256':json_sha(s),
            'source_count':len(s['actors']),'actors':a,
            'legacy_guard':legacy_safety_check(),
            'official_contracts_certified':0,'official_benchmark_cells':0,
            'independent_fight_observations_new':0,
            'evidence_scope':'RAPID_PROFILE_AND_CONDITIONAL_ANALYTIC_NOT_OFFICIAL_FIGHT',
            'known_battle_r196':s['known_historical_evidence']['r196']}
    if out:pathlib.Path(out).write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
    return output

def main():
    ap=argparse.ArgumentParser(description='R197 Mestre-side quick power assessment, no canonical rank change')
    ap.add_argument('--list',action='store_true');ap.add_argument('--actor');ap.add_argument('--source',default=str(SOURCES));ap.add_argument('--target-ca',type=int);ap.add_argument('--target-rd',type=int)
    ap.add_argument('--output');args=ap.parse_args()
    src=load(args.source);actors=src['actors']
    if args.list:print('\n'.join(f'{a["id"]}: {a["name"]} [{a["rank"]}{a["star"]}]' for a in actors));return
    if args.actor:
        xs=[x for x in actors if x['id']==args.actor]
        if not xs:ap.error('Unknown actor: run --list')
        out=report(xs[0],actors,target_ca=args.target_ca,target_rd=args.target_rd)
    else:
        # Use user-selected source file if supplied; never silently fall back to the demo corpus.
        out=generate() if pathlib.Path(args.source).resolve()==SOURCES.resolve() else {
            'version':VERSION,'source_snapshot_sha256':json_sha(src),'source_count':len(actors),
            'actors':all_reports(src,target_ca=args.target_ca,target_rd=args.target_rd),
            'legacy_guard':legacy_safety_check(), 'official_contracts_certified':0, 'official_benchmark_cells':0,
            'not_canonical':True}
    val=json.dumps(out,ensure_ascii=False,indent=2)
    if args.output:pathlib.Path(args.output).write_text(val,encoding='utf8')
    else:print(val)
if __name__=='__main__':main()
