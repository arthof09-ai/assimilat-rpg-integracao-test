#!/usr/bin/env python3
"""DMG empirical diagnostic. Pure math and read-only physical CSVs. Master-only.
Rebuilds outputs in current directory without Notion writes or changes to prior artifacts.
"""
import collections, csv, hashlib, itertools, json, math, pathlib, re, statistics
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parent
HIST=ROOT/'readonly_sources'
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)
RANK_ENTRY={'Bronze':4,'Prata':14,'Ouro':22,'Ouro Negro':38,'Lendário':58}
RANK_BANDS={'Bronze':[[4,6],[7,9],[10,12],[13,15],[16,18]],'Prata':[[14,18],[19,22],[23,26],[27,31],[32,36]],'Ouro':[[22,28],[29,35],[36,44],[45,52],[53,62]],'Ouro Negro':[[38,48],[49,58],[59,69],[70,82],[83,96]],'Lendário':[[58,72],[73,90],[91,112],[113,136],[137,160]]}
def load_csv(filename):
 with (HIST/filename).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def frac_str(x):return str(x.numerator)+'/'+str(x.denominator)
def dice_pmf(pool):
 dp={0:1}
 for n,faces in pool:
  for _ in range(n):
   nxt=collections.Counter()
   for old,count in dp.items():
    for face in range(1,faces+1):nxt[old+face]+=count
   dp=dict(nxt)
 return dp
def pmf_from_formula(formula,attr=0):
 groups=[(int(n),int(d)) for n,d in re.findall(r'(\d+)\s*[dD]\s*(\d+)',formula)]
 if not groups:raise ValueError(formula)
 if any(n<=0 or d<=0 for n,d in groups):raise ValueError(formula)
 dp=dice_pmf(groups)
 return {k+int(attr):v for k,v in dp.items()}
def metrics(pmf,rd=0):
 total=sum(pmf.values()); avg=Fraction(sum(v*k for k,v in pmf.items()),total)
 net=Fraction(sum(v*max(0,k-rd) for k,v in pmf.items()),total)
 pos=Fraction(sum(v for k,v in pmf.items() if k>rd),total)
 return {'mean':float(avg),'mean_fraction':frac_str(avg),'after_rd':float(net),'after_rd_fraction':frac_str(net),'p_positive_given_effect':float(pos),'p_positive_fraction':frac_str(pos),'min':min(pmf),'max':max(pmf),'microstates':total,'variance':float(Fraction(sum(v*k*k for k,v in pmf.items()),total)-avg*avg)}
def median(vals):return statistics.median(vals) if vals else None
r02=load_csv('R02_DAMAGE_A_B_C.csv');r03=load_csv('R03_INITIAL_DAMAGE.csv');r04=load_csv('R04_ALL_INITIAL_ACTIONS.csv')
A=[x for x in r02 if x['included_in_candidate_nine']=='1']; B=[x for x in r03 if x['rank_triple_concordance'].lower() in ('true','1')];C=r04
assert(len(A),len(B),len(C))==(9,6,29)
cohorts=[]
for k,rr in [('R02_Bronze5_candidate',A),('R03_rank_strict',B)]:
 for x in rr:
  rank='Bronze' if k.startswith('R02') else re.match(r'(Prata|Ouro|Bronze|Lendário|Ouro Negro)',x['rank_title']).group()
  dme=float(x['dme_intrinsic'] if k.startswith('R02') else x['intrinsic_expected'])
  gross=float(x['gross_conditional_on_hit'] if k.startswith('R02') else x['gross_expected'])
  attr=float(x['attribute_printed_value'] if k.startswith('R02') else x['attribute_value'])
  row={'cohort':k,'page_id':x['page_id'],'url':'https://app.notion.com/p/'+x['page_id'],'source_name':x['species'] if k.startswith('R02') else x['species_body'],'ability':x['attack'] if k.startswith('R02') else x['name'],'formula':x['formula_original'] if k.startswith('R02') else x['formula'],'rank_label':x['title_rank'] if k.startswith('R02') else x['rank_title'],'label_authority':'title+body Bronze5; ancestry/identity conflicts preserved' if k.startswith('R02') else 'rank title/body/ancestry three-way concordant','dme_intrinsic':dme,'gross_conditional':gross,'attribute_contribution':attr,'attr_share':attr/gross,'rank_entry_minimum':RANK_ENTRY[rank],'below_band_entry_descriptive':dme<RANK_ENTRY[rank],'already_explicit_source_formula':True,'dmgrank_violation':False}
  # Numerical distribution audit; only exact dice and explicitly printed modifier. No attack/saves or costs implied.
  pmf=pmf_from_formula(row['formula'],attr)
  calc=metrics(pmf)
  assert abs(calc['mean']-gross)<1e-9,(row,calc)
  assert abs(gross-(dme+attr))<1e-9,(row,calc)
  row['PMF_numeric_audit']='PASS';row['roll_microstates']=calc['microstates']
  cohorts.append(row)
cohort_agg={}
for name in ('R02_Bronze5_candidate','R03_rank_strict'):
 zz=[z for z in cohorts if z['cohort']==name]
 cohort_agg[name]={'actions':len(zz),'distinct_page_ids':len(set(z['page_id'] for z in zz)),'median_gross':median([z['gross_conditional'] for z in zz]),'mean_gross':statistics.mean([z['gross_conditional'] for z in zz]),'median_dme':median([z['dme_intrinsic'] for z in zz]),'avg_dme':statistics.mean([z['dme_intrinsic'] for z in zz]),'weighted_attribute_fraction':sum(z['attribute_contribution'] for z in zz)/sum(z['gross_conditional'] for z in zz),'below_entry_count_descriptive_not_violation':sum(z['below_band_entry_descriptive'] for z in zz),'in_band_or_above_count':sum(not z['below_band_entry_descriptive'] for z in zz)}
strict_rank={}
for label in ('Prata 1','Prata 5','Ouro 1'):
 zz=[z for z in cohorts if z['cohort']=='R03_rank_strict' and z['rank_label']==label]
 strict_rank[label]={'effects':len(zz),'distinct_sources':len(set(z['page_id'] for z in zz)),'median_gross':median([z['gross_conditional'] for z in zz]),'gross_mean':statistics.mean(z['gross_conditional'] for z in zz),'dme_mean':statistics.mean(z['dme_intrinsic'] for z in zz),'min_gross':min(z['gross_conditional'] for z in zz),'max_gross':max(z['gross_conditional'] for z in zz)}
# Existing selected R03/R04 53-page census. Never combine with R02 as global prevalence.
attr_rows=[r for r in C if r['attribute_value'].strip()!='']
assert len(attr_rows)==28
src_pages=set(r['page_id'] for r in C)
attr_total=sum(float(r['attribute_value']) for r in attr_rows)
dice_total=sum(float(r['intrinsic_mean']) for r in C)
gross_total=sum(float(r['gross_mean']) for r in C)
assert abs(attr_total-1011)<1e-8
assert abs(dice_total-188.5)<1e-8
assert abs(gross_total-1199.5)<1e-8
source_summary={'R03_R04_exploratory_base':{'source_pages_examined_historical_report':53,'numeric_initial_abilities':len(C),'numeric_formula_distinct_page_ids':len(src_pages),'with_explicit_attribute':len(attr_rows),'without_explicit_attribute':len(C)-len(attr_rows),'numeric_dme_sum':dice_total,'printed_attribute_sum':attr_total,'gross_conditional_sum':gross_total,'weighted_attr_fraction_of_all_numeric':attr_total/gross_total,'selection_not_global_population':True,'rank_conflict_r03_report':'30/36 R03 pages disagree in at least one rank axis; only six three-way concordant initial attacks admitted for strict comparison'}}
# New source selection already fixed in PREREG_SOURCE_SAMPLE.json before Notion body reads.
prereg=json.loads((ROOT/'PREREG_SOURCE_SAMPLE.json').read_text())
# Transcribed from pages actually re-opened; no invented zero damage for missing ability.
metadata={
'Ouro 5':[
('0e2c2b324ede83fa8032016593efec3e','Cervatox','Bronze','Ouro 5','NONE_DAMAGE_NUMERIC'),
('19ec2b324ede8335b35c01fff05380ec','Escarlate Flamejante','Ouro 1','Ouro 5','ONLY_HEALING_1d6_PER_TURN'),
('1ebc2b324ede8281a21201f93a2145fb','Soberano da Luz da Lua','Bronze','Ouro 5','NONE_DAMAGE_NUMERIC'),
('21bc2b324ede83faafda8180fd885936','Leopardo de Lava','Bronze','Ouro 5','NONE_DAMAGE_NUMERIC'),
('21ec2b324ede83ee8652012a90225428','Dragão Unicórnio de Lava','Bronze','Ouro 5','NONE_DAMAGE_NUMERIC'),
('266c2b324ede8327b4e98197278f602b','Felivolante','Lendário','Ouro 5','NONE_DAMAGE_NUMERIC'),
('290c2b324ede838dbde401437cb06f52','Ursocristal','Ouro sem estrela','Ouro 5','NONE_DAMAGE_NUMERIC'),
('2e9c2b324ede829eba23815d22d51794','Aurora Radiante','Prata 5','Ouro 5','TWO_1d6_PLUS_INT_DAMAGE_FORMULAS_AND_NON_DAMAGE_1d4_TRIGGER')],
'Ouro Negro 1':[
('294c2b324ede83cc8529017b8555b5be','Carpe Draco','Lendário','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('619c2b324ede83c095928183a3c1933d','Planta Colossal','Bronze','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('79ec2b324ede830a89b0018dd29fdc38','Espectro de Sangue','Bronze','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('9bfc2b324ede834abefc01308b5f0df9','Borboleta Mística','Bronze','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('a0dc2b324ede823e911801087a7331b0','Cão Infernal de Fogo','Ouro','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('a3dc2b324ede8398b446017325a70d76','Dracolion do Deserto','Ouro','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('a7cc2b324ede831b926c017b7b795f45','Guardião Abissal','Lendário','Ouro Negro 1','NONE_DAMAGE_NUMERIC'),
('b09c2b324ede823592af81fb534d5e4b','Grifo Lupino','Lendário','Ouro Negro 1','NONE_DAMAGE_NUMERIC')],
'Lendário 1':[
('394c2b324ede82a3b9f401465b96f9ed','Guardião Etéreo','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC'),
('631c2b324ede8217bcdc017bb56f36f6','Dracospinus','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC'),
('6c6c2b324ede8295ad98813f0db138f4','Wyvern','Lendário sem estrela','Lendário 4','NONE_DAMAGE_NUMERIC'),
('969c2b324ede8333b4b9016ca2957d3f','Serpente do Trovão','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC'),
('c00c2b324ede8303815881275b2e2993','Dracopássaro das Tempestades','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC'),
('c0bc2b324ede8268897e817868197c29','Serpentes do Equinócio Monstruosas','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC'),
('fc0c2b324ede829c8df481fad592e285','Gigante Glacial','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC'),
('ffec2b324ede8289a99101f42099c55c','Elefante Colossal','Bronze','Lendário 1','NONE_DAMAGE_NUMERIC')]}
new=[]
for k,v in metadata.items():
 assert sorted(x[0] for x in v)==prereg['selected'][k]
 for id,name,body_rank,tree_rank,role in v:
  numeric=2 if role.startswith('TWO_') else 0
  new.append({'id':id,'url':'https://app.notion.com/p/'+id,'stratum_query_title':k,'name_body':name,'body_classification':body_rank,'ancestor_classification':tree_rank,'title':k+' (Titã)' if k=='Lendário 1' and id!='6c6c2b324ede8295ad98813f0db138f4' else k,'name_conflict_status':'PENDING' if name in ['Aurora Radiante','Escarlate Flamejante','Guardião Abissal','Dracospinus','Gigante Glacial'] else 'UNRECONCILED','numeric_offense_complete':numeric,'damage_formula_eligible_for_strict_rank_analysis':False,'role':'QUALITATIVE_DAMAGE_INCOMPLETE' if not numeric else 'MATH_ONLY_WITH_IDENTITY_CONFLICT','observation':role,'source_last_edit_date':'2026-10-01','source_read':'Notion Master fetched 2026-10-16','count_missing_as_zero':False})
assert len(new)==24 and sum(x['numeric_offense_complete'] for x in new)==2
assert len({x['id'] for x in new})==24
prior_ids=set(x['page_id'] for x in r02)|set(x['page_id'] for x in r03)|set(x['page_id'] for x in r04)
assert not any(x['id'] in prior_ids for x in new)
new_summary={'pages_read':len(new),'unique_page_ids':len(new),'offensive_formula_bearing_pages':sum(x['numeric_offense_complete']>0 for x in new),'literal_offensive_formulas':sum(x['numeric_offense_complete'] for x in new),'offensive_formula_missing_pages':sum(x['numeric_offense_complete']==0 for x in new),'strict_rank_eligible_pages':sum(x['damage_formula_eligible_for_strict_rank_analysis'] for x in new),'all_rank_title_body_tree_fully_agree':0,'cohort_status':'PAGES_REOPENED; ID deduplicated against local R02/R03/R04, NOT authenticated as new vs historical L002/L003','query_sorted_before_contents':True,'non_damage_dice_must_not_be_counted':'drop 1d10 quantities and solar healing 1d6 are not offensive formulas','by_stratum':{k:{'pages':len([x for x in new if x['stratum_query_title']==k]),'pages_with_numeric_attack':len([x for x in new if x['stratum_query_title']==k and x['numeric_offense_complete']])} for k in prereg['strata']}}
# Matched expected gross means: sample baseline from actual strictly-audited Prata1 lobo da caverna 2d6+25.
# Alter data/attribute allocation while preserving equal gross mean: 2d6+25 vs 4d6+18 -> both E=32.
variants={
'SOURCE_LUPUS_P1_2d6_plus25':{'formula':'2d6','modifier':25,'source':'https://app.notion.com/p/4bac2b324ede8321af6b01eb96452d04','source_type':'PHYSICAL_SOURCE'},
'LAB_EQUAL_MEAN_4d6_plus18':{'formula':'4d6','modifier':18,'source':'derived controlled counterfactual','source_type':'SYNTHETIC_VARIANT'},
'LAB_ATTR_PLUS5_2d6_plus30':{'formula':'2d6','modifier':30,'source':'derived sensitivity','source_type':'SYNTHETIC_VARIANT'},
'LAB_EXTRA_D6_3d6_plus25':{'formula':'3d6','modifier':25,'source':'derived sensitivity','source_type':'SYNTHETIC_VARIANT'}}
rd_values=[0,5,15,25,30,31,35,40,42,45]
variant_res={}
for name,v in variants.items():
 p=pmf_from_formula(v['formula'],v['modifier'])
 variant_res[name]={'metadata':v,'metrics_by_rd':{str(rd):metrics(p,rd) for rd in rd_values}}
assert variant_res['SOURCE_LUPUS_P1_2d6_plus25']['metrics_by_rd']['0']['mean']==32
assert variant_res['LAB_EQUAL_MEAN_4d6_plus18']['metrics_by_rd']['0']['mean']==32
# Anticipated falsifier for naive mean-only model at sufficiently high physical RD.
assert variant_res['SOURCE_LUPUS_P1_2d6_plus25']['metrics_by_rd']['35']['after_rd']!=variant_res['LAB_EQUAL_MEAN_4d6_plus18']['metrics_by_rd']['35']['after_rd']
assert variant_res['LAB_ATTR_PLUS5_2d6_plus30']['metrics_by_rd']['42']['after_rd']==0
assert variant_res['LAB_EXTRA_D6_3d6_plus25']['metrics_by_rd']['42']['after_rd']>0
# Cross-rank matrix is not a population estimate; DME compatibility is diagnostic and NOT a normative failure.
comparison={'rank_entry_bands_v1_1':RANK_BANDS,'sample_15_actions':{'rows':cohorts,'aggregation':cohort_agg,'rank_strict_six':strict_rank},'r03_r04_29_action_attr_analysis':source_summary,'new_24_page_gap':new_summary,'mechanism_experiments':variant_res,'scientific_interpretation':{'main_caveat':'DMG-RANK v1.1 fills missing effects; explicit preexisting Beast damage has different precedence. Out-of-band existing explicit formula is not violation. Rank Nominal != Rank Efeito; all band checks purely descriptive.','new_24':'Physical pages bear relevant creature descriptions, not zero damage. Raw dice in loot or healing not offense. No three-way-consistent rank for strict inference.','methodical_candidate':'Test variance-aware reporting and rule-scope clarification, not forced global damage recalibration. Need held-out independent family samples to test utility.','v2_status':'NOT_SUPPORTED_BY_CURRENT_EVIDENCE'}}
(OUT/'SOURCE_LEDGER_24.json').write_text(json.dumps(new,ensure_ascii=False,indent=2))
(OUT/'DIAGNOSTIC_RESULTS.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2))
(OUT/'DIAGNOSIS_OVERVIEW.json').write_text(json.dumps({'old_9':cohort_agg['R02_Bronze5_candidate'],'strict_6':cohort_agg['R03_rank_strict'],'older_29':source_summary,'new_24':new_summary,'n_raw_source_unique_r02_r03_r04':len(prior_ids),'analytical_rank_note':'Do NOT sum sources to global corpus; historical L002/L003 membership unknown; new 24 verified distinct vs local R02/R03/R04 only.'},ensure_ascii=False,indent=2))
print(json.dumps({'OLD':cohort_agg,'STRICT_RANK':strict_rank,'R04_29':source_summary,'NEW24':new_summary,'RD35':[{'case':k,'E_net':v['metrics_by_rd']['35']['after_rd'],'p_damage':v['metrics_by_rd']['35']['p_positive_given_effect']} for k,v in variant_res.items()],'RD42':[{'case':k,'E_net':v['metrics_by_rd']['42']['after_rd'],'p_damage':v['metrics_by_rd']['42']['p_positive_given_effect']} for k,v in variant_res.items()]},ensure_ascii=False,indent=2))
