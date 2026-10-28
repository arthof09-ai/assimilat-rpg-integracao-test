#!/usr/bin/env python3
"""Independent brute-force audit of core source arithmetic + adversarial source gates.
No imports from REPRODUCE_DIAGNOSTIC.py. File writes only within results/.
"""
import collections,csv,hashlib,itertools,json,pathlib,zipfile,statistics
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parent
T=json.loads((R/'results/DIAGNOSTIC_RESULTS.json').read_text())
L=json.loads((R/'results/SOURCE_LEDGER_24.json').read_text())
P=json.loads((R/'PREREG_SOURCE_SAMPLE.json').read_text())
checks=[]
def check(label,test):
 checks.append({'id':label,'status':'PASS' if test else 'FAIL'})
 if not test:raise AssertionError(label)
check('frozen24_before_body_analysis',P['selection_before_body_fetch'])
check('source_24_unique',len(L)==len({x['id'] for x in L})==24)
check('stratum8x3',all(len([x for x in L if x['stratum_query_title']==s])==8 for s in P['strata']))
check('sampleIDs_exact_preregistered',all(sorted(x['id'] for x in L if x['stratum_query_title']==s)==P['selected'][s] for s in P['strata']))
check('one_damage_source_page',sum(bool(x['numeric_offense_complete']) for x in L)==1)
check('two_num_offensive_formulas',sum(x['numeric_offense_complete'] for x in L)==2)
check('no_rank_strict_for_24',not any(x['damage_formula_eligible_for_strict_rank_analysis'] for x in L))
check('missing_offense_not_imputed_0',all(not x['count_missing_as_zero'] for x in L))
check('healing_not_offense',next(x for x in L if x['name_body']=='Escarlate Flamejante')['numeric_offense_complete']==0)
check('aurora_numeric_not_rank_strict',next(x for x in L if x['name_body']=='Aurora Radiante')['numeric_offense_complete']==2 and not next(x for x in L if x['name_body']=='Aurora Radiante')['damage_formula_eligible_for_strict_rank_analysis'])
# Independently enumerate faces (as opposed to convolution used in main model).
def exact(faces,modifier,rd):
 n=len(faces);count=0;positive=0;damage=0;total=1
 for d in faces:total*=d
 for dice in itertools.product(*[range(1,d+1) for d in faces]):
  attack=sum(dice)+modifier
  if attack>rd:positive+=1
  damage+=max(0,attack-rd)
  count+=1
 assert count==total
 return Fraction(damage,total),Fraction(positive,total)
def arr(formula):
 groups=formula.split('d6');n=int(groups[0]);return [6]*n
V=T['mechanism_experiments']
for key,v in V.items():
 formula=v['metadata']['formula'];mod=v['metadata']['modifier'];faces=arr(formula)
 for rd_s,vals in v['metrics_by_rd'].items():
  rd=int(rd_s);net,pos=exact(faces,mod,rd)
  check(key+f'|RD{rd}|EXPECTED',vals['after_rd_fraction']==f'{net.numerator}/{net.denominator}')
  check(key+f'|RD{rd}|P_POSITIVE',vals['p_positive_fraction']==f'{pos.numerator}/{pos.denominator}')
check('equal_mean_base_vs_var',V['SOURCE_LUPUS_P1_2d6_plus25']['metrics_by_rd']['0']['mean']==V['LAB_EQUAL_MEAN_4d6_plus18']['metrics_by_rd']['0']['mean']==32)
check('different_rd35',V['SOURCE_LUPUS_P1_2d6_plus25']['metrics_by_rd']['35']['after_rd']<V['LAB_EQUAL_MEAN_4d6_plus18']['metrics_by_rd']['35']['after_rd'])
check('highRD42_attr_below',V['LAB_ATTR_PLUS5_2d6_plus30']['metrics_by_rd']['42']['after_rd']==0)
check('highRD42_extra_d6_pos',V['LAB_EXTRA_D6_3d6_plus25']['metrics_by_rd']['42']['after_rd_fraction']=='1/216')
old=T['sample_15_actions'];rows=old['rows']
check('old9_plus_strict6',len(rows)==15)
check('2cohorts_not_pooled',[old['aggregation'][z]['actions'] for z in ['R02_Bronze5_candidate','R03_rank_strict']]==[9,6])
check('old9_page7',len({x['page_id'] for x in rows if x['cohort']=='R02_Bronze5_candidate'})==7)
check('strict6_page6',len({x['page_id'] for x in rows if x['cohort']=='R03_rank_strict'})==6)
check('rank_strict_counts',[old['rank_strict_six'][x]['effects'] for x in ['Prata 1','Prata 5','Ouro 1']]==[3,2,1])
check('band_descriptive_not_normative',all(not x['dmgrank_violation'] and x['already_explicit_source_formula'] for x in rows))
check('below_band_sample7_and6',[old['aggregation'][z]['below_entry_count_descriptive_not_violation'] for z in ['R02_Bronze5_candidate','R03_rank_strict']]==[7,6])
old29=T['r03_r04_29_action_attr_analysis']['R03_R04_exploratory_base']
check('29_numeric_action_26_pages',old29['numeric_initial_abilities']==29 and old29['numeric_formula_distinct_page_ids']==26)
check('28_of29_attribute',old29['with_explicit_attribute']==28)
check('attr_weighted_1011_over1199_5',abs(old29['weighted_attr_fraction_of_all_numeric']-1011/1199.5)<1e-14)
# Input source/checkpoint identity, independently compared to known internal hashes.
zip_path=R/'readonly_sources/DMG-F1-R11-B02-CERTIFICACAO-E-INTEGRACAO-VLAB-R03-v01.zip'
if zip_path.exists():
 with zipfile.ZipFile(zip_path) as z:
  manifest=json.loads(z.read('MANIFEST_R11_SHA256.json'))
  for name,sha in manifest.items():check('R11_MANIFEST_'+name,hashlib.sha256(z.read(name)).hexdigest()==sha)
  mat=json.loads(z.read('DMG-F1-R11-MATRIZ-B01-B18-v01.json'))
  check('R11_B02_only',mat.get('pass_ids')==['B02'] and mat.get('certified_whole')==1)
  records=mat.get('records',[])
  check('R11_18_original_requirements',len(records)==18)
else:check('R11_archived_status_missing',False)
result={'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','total_checks':len(checks),'passes':sum(x['status']=='PASS' for x in checks),'checks':checks,'independent_method':'Brute itertools enumerate each dice face; independently inspect R11 ZIP manifest; no use of main-model functions','limitation':'Checking exact arithmetic cannot verify Notion-source rank authority, combat engine or representativeness','notion_writes':0}
(R/'results/INDEPENDENT_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
