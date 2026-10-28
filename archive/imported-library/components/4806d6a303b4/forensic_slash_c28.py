"""C28 recheck of source-visible slash annotations from C22 with historical Bagunça comparator.
Literal texts re-read in Mestre Notion 2026-10-21; note source transcription not independent coder.
"""
from pathlib import Path
import csv,json,statistics,re
from fractions import Fraction
P=Path(__file__).resolve().parent.parent;OUT=P/'publication'
base=P/'baseline/C22_ANNOTATIONS_12_RECONCILIATION.csv'
assert base.exists()
rows=list(csv.DictReader(base.open(encoding='utf-8')))
assert len(rows)==12
n_in=0;n_near=0;dif=[]
for r in rows:
 expr=r['literal_formula'];annotation=int(r['annotation']);k=int(re.match(r'(\d+)d12',expr).group(1));fixed=int(expr.split('+')[-1]);mn=k+fixed;mx=12*k+fixed;mu=6.5*k+fixed
 r['verified_bound_min']=mn;r['verified_bound_max']=mx;r['verified_mean']=mu
 r['in_support_verified']='YES' if mn<=annotation<=mx else 'NO'
 r['difference_from_mean']=annotation-mu;r['abs_difference_from_mean']=abs(annotation-mu)
 r['source_url']='https://app.notion.com/p/'+r['source_id']
 r['status']='NORMAL_WITHIN7_OF_MEAN' if mn<=annotation<=mx and abs(annotation-mu)<=7 else 'OUTLIER_OUTSIDE_SUPPORT'
 if mn<=annotation<=mx:n_in+=1;dif.append(abs(annotation-mu))
 if mn<=annotation<=mx and abs(annotation-mu)<=7:n_near+=1
hist={
 'id':'BAGUNCA-HIST-220','source_id':'9f9c2b324ede8213968d810c9988bf59','source_url':'https://app.notion.com/p/9f9c2b324ede8213968d810c9988bf59',
 'family':'Bagunça / Eletroaquarion historical','title_rank':'N/A', 'body_rank':'N/A','effect_name':'AtM','literal_formula':'6d12+110','annotation':220,
 'verified_bound_min':116,'verified_bound_max':182,'verified_mean':149.0,'in_support_verified':'NO','difference_from_mean':71.0,'abs_difference_from_mean':71.0,'status':'HISTORICAL_OUTSIDE_SUPPORT','special':'18 attacks and 10 attacks projections use 220' }
rows.append(hist)
cols=['effect_id','source_id','source_url','family','title_rank','body_rank','effect_name','literal_formula','annotation','verified_bound_min','verified_bound_max','verified_mean','in_support_verified','difference_from_mean','abs_difference_from_mean','status','special']
with (OUT/'C28_C22_12_NOTES_PLUS_HISTORICAL_1_REAUDITED.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader()
 for r in rows:
  r['effect_id']=r.get('effect_id',r.get('id',''))
  w.writerow(r)
assert n_in==11 and n_near==11
assert statistics.median(dif)==2.0 and max(dif)==7.0
assert 6*12+110==182
assert 220-182==38
assert 301-252==49
assert int(220*18)==3960 and int(220*10)==2200
s={
 'G1_slash_annotations':12,'G1_within_support':11,'G1_near_mean_abs_difference_at_most7':11,
 'median_absolute_deviation_of_11_supported_annotations':statistics.median(dif),'maximum_absolute_deviation_of_11_supported_annotations':max(dif),
 'G1_Eletro_O5_10d12plus132_annotation':301,'G1_Eletro_O5_mean':197,'G1_Eletro_O5_max':252,'G1_Eletro_O5_excess_over_max':49,'G1_Eletro_O5_excess_over_mean':104,
 'Bagunca_historical_formula':'6d12+110','G1_same_formula_annotation':147,'Historical_annotation':220,'Historical_max':182,'Historical_mean':149,'Historical_excess_over_max':38,'Historical_difference_same_formula_annotation':73,
 'Historic_18_times_220':3960,'Historic_18_times_149_conditional_all_hits':2682,'Historic_10_times_220':2200,'Historic_10_times_149_conditional_all_hits':1490,
 'relative_inflation_of_220_compared_to_formula_mean':220/149-1,
 'Serpentaqua_O5_FOR_as_written':103,'Serpentaqua_O5_formula_flat_as_written':105,'difference_origin_unclassified':2,
 'status':'TWO_DOCUMENTARY_OVER_SUPPORT_VALUES; no canonical changes, slash semantics inferred not certified; all-hit projections not combats',
 'sources':['https://app.notion.com/p/415c2b324ede83c78b8b01de73516dd6','https://app.notion.com/p/9bac2b324ede8302be0c0135fef4fd15','https://app.notion.com/p/9f9c2b324ede8213968d810c9988bf59','https://app.notion.com/p/d32c2b324ede827391be01c105a1a115'] }
(OUT/'C28_FORENSIC_SLASH_DOSSIER.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(rows)==13
print(json.dumps({'reopened_9_G1_families':'9 source pages','supported11':n_near,'hist220inflationpct':100*s['relative_inflation_of_220_compared_to_formula_mean']},ensure_ascii=False))
