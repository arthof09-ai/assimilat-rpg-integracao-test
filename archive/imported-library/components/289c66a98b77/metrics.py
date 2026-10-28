"""Comparação de dois pareceres congelados, NÃO métrica de verdade canônica.

R45 é o arquivo com 26 classificações TEST congeladas.
Peer é um parecer IA separado, com 11/12 casos não expostos conhecidos.
Este módulo é somente Mestre-side e NÃO ajusta modelo nem escreve Notion.
"""
from __future__ import annotations
import csv, io, json, math
from collections import Counter
from itertools import combinations
from pathlib import Path

RANKS=('Bronze','Prata','Ouro','Ouro Negro','Lendário')


def load_inputs(root: Path):
    x=json.loads((root/'r45_frozen.json').read_text(encoding='utf8'))
    with (root/'peer12_frozen.csv').open(encoding='utf-8-sig',newline='') as fh:
        p=list(csv.DictReader(fh))
    lineage=json.loads((root/'lineage26_no_ranks.json').read_text(encoding='utf8'))
    return x,p,lineage


def identity_check(frozen, peer, lineage):
    by={c['case_id']:c for c in frozen['cases']}
    if len(by)!=len(frozen['cases']) or len(by)!=26: raise ValueError('R45_CENSUS_FAILED')
    ids=[c['case_id'] for c in peer]
    if len(ids)!=12 or len(set(ids))!=12 or not set(ids).issubset(by):raise ValueError('PEER_CENSUS_FAILED')
    rows=lineage['images']
    lids=[r['id'] for r in rows]
    if len(rows)!=26 or len(set(lids))!=26 or set(lids)!=set(by):raise ValueError('IMAGE_CENSUS_FAILED')
    for c in peer:
        expected=next(x for x in rows if x['id']==c['case_id'])
        if expected['blind_cohort']!='PEER12' or expected['masked_sha256']!=c['image_sha256']:
            raise ValueError('MASKED_SHA_MISMATCH')
    if {r['id'] for r in rows if r['blind_cohort']=='PEER12'}!=set(ids):raise ValueError('COHORT_MISMATCH')
    return by


def exact_fisher_2x2(table):
    # Conditional hypergeometric two-sided Fisher: probabilities <= observed.
    a,b=table[0];c,d=table[1];r1=a+b;r2=c+d;col1=a+c;n=r1+r2
    def p(k):return math.comb(col1,k)*math.comb(n-col1,r1-k)/math.comb(n,r1)
    low=max(0,r1-(n-col1));hi=min(r1,col1)
    pk=p(a)
    return sum(p(k) for k in range(low,hi+1) if p(k)<=pk+1e-12)


def metrics(frozen, peer, lineage):
    by=identity_check(frozen,peer,lineage)
    usable=[p for p in peer if p['proposed_RE'] in RANKS and 'EXPOSTO' not in p['blind_status'].upper()]
    contaminated=[p['case_id'] for p in peer if p not in usable]
    if len(usable)!=11:raise ValueError('EXPECTED_11_INDEPENDENT_CASES')
    records=[];table=[[0,0],[0,0]]
    for p in usable:
        f=by[p['case_id']]
        r=f['proposed_rank']; y=p['proposed_RE']
        lo,hi=f['candidate_range'].split('–')
        sz=RANKS.index(hi)-RANKS.index(lo)+1
        if sz<=0:raise ValueError('INVALID_RANGE')
        same=(r==y)
        is_e2=p['evidence_level']=='E2'
        if p['evidence_level'] not in ('E2','E3'):raise ValueError('UNEXPECTED_EVIDENCE_KIND')
        table[0 if is_e2 else 1][0 if same else 1]+=1
        records.append({'case_id':p['case_id'],'R45':r,'peer':y,
           'R45_range':f['candidate_range'],'interval_cardinality':sz,
           'peer_evidence':p['evidence_level'],'agree':same,
           'constant_Prata_agree':y=='Prata',
           'ordinal_abs_error_vs_peer':abs(RANKS.index(r)-RANKS.index(y))})
    n=len(records)
    hit=sum(x['agree'] for x in records)
    always_hit=sum(x['constant_Prata_agree'] for x in records)
    ranks=set(x['peer'] for x in records)
    counts={r:sum(x['peer']==r for x in records) for r in RANKS if r in ranks}
    byclass={r:{'n':counts[r], 'R45_recall':sum(x['R45']==r and x['peer']==r for x in records)/counts[r],
                 'constant_Prata_recall':int(r=='Prata')} for r in counts}
    only_r45=sum(x['agree'] and not x['constant_Prata_agree'] for x in records)
    only_base=sum(x['constant_Prata_agree'] and not x['agree'] for x in records)
    # exact McNemar: two-sided Binomial(n_disc, .5) tail, bounded 1.
    ndisc=only_r45+only_base
    mcnemar=min(1.0,2*sum(math.comb(ndisc,i) for i in range(min(only_r45,only_base)+1))/2**ndisc) if ndisc else 1.0
    c45=Counter(x['R45'] for x in records);cp=Counter(x['peer'] for x in records)
    pe=sum(c45[r]*cp[r] for r in RANKS)/n**2
    po=hit/n
    kappa=(po-pe)/(1-pe) if pe<1 else None
    return {'status':'AGREEMENT_ONLY_NOT_ACCURACY', 'n_peer_submitted':len(peer),
        'n_usable':n,'n_exposed_or_abstained':len(contaminated),'exposed_ids':contaminated,
        'hits_R45':hit,'hits_constant_Prata':always_hit,
        'agreement_R45':po,'agreement_constant_Prata':always_hit/n,
        'kappa_nominal_R45_peer':kappa,'class_counts_peer':counts,'by_class':byclass,
        'macro_recall_R45_vs_peer':sum(q['R45_recall'] for q in byclass.values())/len(byclass),
        'macro_recall_constant_Prata_vs_peer':sum(q['constant_Prata_recall'] for q in byclass.values())/len(byclass),
        'paired_R45_only_wins':only_r45,'paired_constant_only_wins':only_base,'mcnemar_exact_p':mcnemar,
        'mean_ordinal_abs_error_R45_vs_peer':sum(x['ordinal_abs_error_vs_peer'] for x in records)/n,
        'evidence_by_agreement':{'rows':['E2','E3'],'cols':['agree','disagree'],'counts':table,
                'Fisher_two_sided_conditional_p':exact_fisher_2x2(table),
                'interpretation':'selection-conditioned exploratory association, not E2 reliability or accuracy'},
        'R45_interval_mean_cardinality':sum(x['interval_cardinality'] for x in records)/n,
        'R45_interval_cardinality_counts':dict(Counter(x['interval_cardinality'] for x in records)),
        'R45_range_includes_Prata_all':all('Prata' in RANKS[RANKS.index(x['R45_range'].split('–')[0]):RANKS.index(x['R45_range'].split('–')[1])+1] for x in records),
        'R45_band_hits_vs_peer':sum(x['peer'] in RANKS[RANKS.index(x['R45_range'].split('–')[0]):RANKS.index(x['R45_range'].split('–')[1])+1] for x in records),
        'records':records,
        'qualifications': ['peer IA rank is not ground truth','selected 12 are historical-label outliers, not random sample',
         'peer E2/E3 do not represent calibrated success probability','no automatic promotion R45/rank/PA','R49 comparisons may inform new model; new model must be frozen before next new independent sample']}


def future_review_protocol(lineage):
    rows=lineage['images'];h=[{'case_id':x['id'],'masked_sha256':x['masked_sha256']} for x in rows if x['blind_cohort']=='HOLDOUT14']
    if len(h)!=14:raise ValueError('HOLDOUT_NOT_14')
    return {'status':'PREREGISTERED_NO_RESULTS','denominator':14,'blinded_manifest':sorted(h,key=lambda x:x['case_id']),
     'before_any_new_peer': ['freeze model code and outputs','do not open original historic rank list',
       'no access to R45/R46/R47/R48/R49 reports by new reviewer','screen Atlas case-specific labels for contamination'],
     'metrics_if_peer_only':['exact agreement','ordinal disagreement','macro recall against peer with NOT_GOLD label',
       'always-Prata comparator','abstention denominator','width/cardinality of uncertainty sets'],
     'metrics_if_authority_adjudicates':['confusion matrix by RE','macro recall','mean ordinal absolute error',
       'coverage and average width of prediction bands','risk at stated abstention coverage'],
     'unresolved':['No newly independent 14-case adjudication has been received','Notion labels historically subjective','No canonical costs PA established'],
     'no_automatic_writes':True}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    a,b,c=load_inputs(root/'inputs')
    dst=root/'outputs';dst.mkdir(exist_ok=True)
    (dst/'metrics_report.json').write_text(json.dumps(metrics(a,b,c),ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
    (dst/'protocol_holdout14.json').write_text(json.dumps(future_review_protocol(c),ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
    print('PASS metrics/protocol; no canon writes')
