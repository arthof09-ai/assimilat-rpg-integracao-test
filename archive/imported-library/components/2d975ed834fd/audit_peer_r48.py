"""PA R48 TEST: immutable audit of external independent review vs frozen R45.
Never canonizes, posts externally or mutates source files. Only verified bytes.
"""
from __future__ import annotations
import csv,io,json,zipfile,hashlib,math,collections,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'source' if (ROOT/'source'/'AVALIACAO_INDEPENDENTE_12_ASSIMILACAO_v1_0_MESTRE_ONLY.zip').exists() else Path('/mnt/data')
PEER=BASE/'AVALIACAO_INDEPENDENTE_12_ASSIMILACAO_v1_0_MESTRE_ONLY.zip'
R45=BASE/'PA_IMG26_ATLAS_CRAFT_R45_MESTRE_ONLY_TEST_20261021.zip'
CSV=BASE/'peer_review_preenchido.csv'
REPORT=BASE/'RELATORIO_TECNICO_COMPLETO.md'
EXPECTED_ZIP_SHA='d5fa1054b6e296d893e182a735efb24f2053ffdf28bbcecae7da552318b93435'
RANKS=['Bronze','Prata','Ouro','Ouro Negro','Lendário']

def sha(b):return hashlib.sha256(b).hexdigest()
def bsha(path):return sha(path.read_bytes())

def normalize(s):
    s=s.replace('–','-').replace('—','-').strip()
    r=[x.strip() for x in s.split('-')]
    return r

def read_inputs():
    assert bsha(PEER)==EXPECTED_ZIP_SHA, 'peer ZIP SHA mismatch'
    with zipfile.ZipFile(PEER) as z:
        assert z.testzip() is None, 'peer CRC failed'
        filelist=z.namelist()
        assert len(filelist)==len(set(filelist))==9
        manifest=json.loads(z.read('MANIFEST_SHA256_OUTPUT.json'))['files']
        assert set(manifest)==set(filelist)-{'MANIFEST_SHA256_OUTPUT.json'}
        for name,h in manifest.items():assert sha(z.read(name))==h, 'outer ZIP file SHA failed '+name
        assert z.read('peer_review_preenchido.csv')==CSV.read_bytes()
        assert z.read('RELATORIO_TECNICO_COMPLETO.md')==REPORT.read_bytes()
        frozen=json.loads(z.read('FREEZE_RECORD.json'))
        assert frozen['pre_oracle'] and frozen['count_total']==12
        assert frozen['csv_sha256']==sha(z.read('peer_review_preenchido.csv'))
        assert frozen['report_sha256']==sha(z.read('RELATORIO_TECNICO_COMPLETO.md'))
        for n,v in frozen['files_at_time_of_freeze_sha256'].items():
            assert sha(z.read(n))==v['sha256'] and len(z.read(n))==v['bytes']
        q=json.loads(z.read('QA_RESULTS.json'))
        assert q['passed']==q['total']==21
        inner=z.read('FONTE_ORIGINAL_SEM_GABARITO.zip')
        with zipfile.ZipFile(io.BytesIO(inner)) as az:
            assert az.testzip() is None
            mm=json.loads(az.read('MANIFEST_SHA256.json'))
            assert len(mm)==14
            for n,h in mm.items():assert sha(az.read(n))==h
            image_list=[n for n in mm if n.lower().endswith('.jpg')]
            assert len(image_list)==12
            ids={Path(n).stem for n in image_list}
            assert len(ids)==12
            md={Path(n).stem:(n,h) for n,h in mm.items() if n.endswith('.jpg')}
        rows=list(csv.DictReader(io.StringIO(z.read('peer_review_preenchido.csv').decode('utf-8-sig'))))
        assert len(rows)==len({x['case_id'] for x in rows})==12
        assert {x['case_id'] for x in rows}==ids
        assert all(x['image_sha256']==md[x['case_id']][1] for x in rows)
        assert {x['case_id']:x['proposed_RE'] for x in rows}==frozen['classification_results']
        assert len(frozen['contaminated_ids'])==1
        assert frozen['contaminated_ids']==['TEC-E3532F6A98AC']
        assert [x for x in rows if x['proposed_RE']=='INSUFICIENTE'][0]['case_id']==frozen['contaminated_ids'][0]
    with zipfile.ZipFile(R45) as z:
        assert z.testzip() is None
        freeze_bytes=z.read('FREEZE_RANK_PROPOSALS_BEFORE_ORACLE.json')
        assert sha(freeze_bytes)=='2f1e88e3c7980cf376ed2ec76816dec48d3f4779bec55a9f6e3bf5687e799a5e'
        freeze=json.loads(freeze_bytes)['cases']
        assert len(freeze)==26
        ra={x['case_id']:x for x in freeze}
        assert all(x['case_id'] in ra for x in rows)
    return rows,ra,{'peer_zip_sha':bsha(PEER),'outer_zip_entries':9,'outer_manifest_files':8,'inner_zip_entries':15,'inner_manifest_files':14,'images':12,'freeze_R45_cases':26,'frozen_peer_cases':12,'external_QA_passed_claim':21}

def score(rows,r45):
    eligible=[x for x in rows if x['proposed_RE'] in RANKS]
    n=len(eligible)
    a=[r45[x['case_id']]['proposed_rank'] for x in eligible]
    b=[x['proposed_RE'] for x in eligible]
    equal=sum(x==y for x,y in zip(a,b)); near=sum(abs(RANKS.index(x)-RANKS.index(y))<=1 for x,y in zip(a,b))
    ca=collections.Counter(a);cb=collections.Counter(b)
    pe=sum(ca[k]*cb[k]/n**2 for k in RANKS)
    observed=equal/n
    kappa=(observed-pe)/(1-pe) if pe!=1 else None
    naive=sum(y=='Prata' for y in b)
    in_band=[];naive_band=[]
    disagreements=[]; per=[]
    for x in eligible:
        r=r45[x['case_id']];band=r['candidate_range']; parts=normalize(band)
        low,high=RANKS.index(parts[0]),RANKS.index(parts[-1]);p=RANKS.index(x['proposed_RE'])
        inside=low<=p<=high
        in_band.append(inside);naive_band.append(low<=1<=high)
        if x['proposed_RE'] != r['proposed_rank']:
            disagreements.append({'id':x['case_id'],'title':x['source_title'],'r45':r['proposed_rank'],'peer':x['proposed_RE'],'peer_confidence':x['evidence_level'],'distance':abs(RANKS.index(r['proposed_rank'])-p),'band':band})
        per.append({'id':x['case_id'],'name':x['source_title'],'r45_frozen':r['proposed_rank'],'r45_band':band,'peer_frozen':x['proposed_RE'],'peer_evidence':x['evidence_level'],'within_R45_band':inside,'same_rank':r['proposed_rank']==x['proposed_RE'],'is_blind_declared':x['blind_status'].startswith('SEM_ORACULO')})
    # Wilson confidence interval: agreement, not predictive accuracy; descriptive only
    z=1.95996398454005
    ctr=(observed+z*z/(2*n))/(1+z*z/n)
    mar=(z*math.sqrt((observed*(1-observed)/n)+(z*z/(4*n*n))))/(1+z*z/n)
    return {'n_eligible':n,'n_total':len(rows),'n_contaminated':1,'matching':equal,'observed_agreement':observed,'simple_prata_baseline_hits':naive,'simple_prata_baseline_agreement':naive/n,'rank_prevalence_R45':dict(ca),'rank_prevalence_peer':dict(cb),'chance_agreement':pe,'cohen_nominal_kappa':kappa,'wilson_95_interval_on_agreement_not_accuracy':[ctr-mar,ctr+mar],'within_R45_band':sum(in_band),'naive_Prata_within_R45_band':sum(naive_band),'within_one_rank':near,'discordances':disagreements,'per_case':per,'peer_grade_E2_n':sum(x['evidence_level']=='E2' for x in eligible),'peer_grade_E2_disagree_n':sum(x['evidence_level']=='E2' and r45[x['case_id']]['proposed_rank']!=x['proposed_RE'] for x in eligible),'all_validated_RE':False,'predictive_accuracy':None,'canonizations':0}

if __name__=='__main__':
    rows,r45,src=read_inputs();scores=score(rows,r45)
    output={'protocol':'PA-R48 TEST/forensic: content and frozen-file hashes; not source independence certification','source':src,'metrics':scores,'limitations':['Form validation is not rank accuracy','Second assessor is AI, not independent human','The known contaminated case is excluded from agreement','Comparators may be indirect and must be judged semantically','Original historical rank is not treated as truth','No PA cost or CRAFT material event inferred']}
    path=ROOT/'PEER_R48_CROSSCHECK.json';path.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:scores[k] for k in ['n_eligible','matching','simple_prata_baseline_hits','cohen_nominal_kappa','within_R45_band','naive_Prata_within_R45_band','peer_grade_E2_disagree_n']},ensure_ascii=False,indent=2))
