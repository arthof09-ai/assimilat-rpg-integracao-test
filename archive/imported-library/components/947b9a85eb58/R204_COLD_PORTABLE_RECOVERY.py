#!/usr/bin/env python3
"""VLAB R201-204 cold recovery. NEVER dispatch a battle, never reuse RUN-ID.
Validates package manifest + exact R200 historical ZIP + semantic SQL ledgers read-only.
Expects extracted package root as first argument, or its own parent otherwise.
"""
import pathlib,json,hashlib,sys,importlib.util,collections,re
root=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_R201_R204.json').read_text())
assert manifest['schema']=='VLAB-R201-R204-FROZEN-MANIFEST-1'
items=manifest['files'];assert all('../' not in x and not x.startswith('/') for x in items)
assert len(items)==len(set(items)), 'DUPLICATE_MANIFEST_PATHS'
assert len(items)>150,'EXPECTED_ENTRIES_MISSING'
for name,meta in items.items():
 p=root/name
 assert p.is_file(),f'MISSING_FILE:{name}'
 assert p.stat().st_size==meta['size'],f'SIZE_DRIFT:{name}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'],f'HASH_DRIFT:{name}'
assert (root/'baseline_r200/VLAB_R200_R203_FISICO_GEOMETRIA_COMBATES_MESTRE_ONLY.zip').stat().st_size==18146400
assert hashlib.sha256((root/'baseline_r200/VLAB_R200_R203_FISICO_GEOMETRIA_COMBATES_MESTRE_ONLY.zip').read_bytes()).hexdigest()=='6e462fa907f489ce72a5ee514203c69b995253f15cc2b05273fd44b7b8144f74'
# Import code-separate auditors WITHOUT calling main() and WITHOUT mutating evidence outputs.
semantic=[];cohorts=[]
for cod,subfolder,expected,reportfile in [
 ('r204_readonly_independent_audit','db',24,'R204_INDEPENDENT_AUDIT.json'),
 ('r204_v2_independent_audit','v2_db',32,'R204_V2_INDEPENDENT_AUDIT.json'),
 ('r204_v2b_independent_audit','v2b_db',8,'R204_V2B_INDEPENDENT_AUDIT.json')]:
 f=root/'new/code'/f'{cod}.py'
 spec=importlib.util.spec_from_file_location(f'checker_{cod}',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 dbs=sorted((root/'new/evidence'/subfolder).glob('*.sqlite'))
 assert len(dbs)==expected,f'WRONG_DB_DENOMINATOR_{cod}'
 results=[m.audit(p)for p in dbs]
 report=json.loads((root/'new/evidence'/reportfile).read_text())
 assert report['battles']==expected and report['KO']==expected
 for key,receipt_key in [('commits','commits'),('native_events','native_events'),('magic_casts','magic_casts'),('PA_magic_spent','PA_spent'),('magic_actual_HP_removed','magic_actual_HP_removed'),('distance_refusals','distance_rejections')]:
  assert report[key]==sum(r[receipt_key] for r in results),f'METRIC_DRIFT:{cod}:{key}'
 assert {x['id'] for x in results}=={x['id'] for x in report['records']}
 for r in results:
  saved=next(x for x in report['records'] if x['id']==r['id'])
  assert saved==r,f'SEMANTIC_RECEIPT_DIFFERENCE:{r["id"]}'
 semantic.extend(results)
 cohorts.append({k:report[k] for k in ('status','battles','KO','commits','native_events','magic_casts','PA_magic_spent','magic_actual_HP_removed','distance_refusals')})
assert len(semantic)==64 and len({x['id'] for x in semantic})==64
assert sum(x['commits'] for x in semantic)==995
assert sum(x['native_events'] for x in semantic)==3107
assert sum(x['magic_casts'] for x in semantic)==250
assert sum(x['PA_spent'] for x in semantic)==2000
assert sum(x['magic_actual_HP_removed'] for x in semantic)==5965
assert sum(x['distance_rejections'] for x in semantic)==5
# R201 source legal audit is self-contained; its previous execution result is immutable and source-hashed.
profile_path=root/'new/source/R201_ED_REF_01_SOURCE_PROFILE_SNAPSHOTS.json'
profiles=json.loads(profile_path.read_text());legal=json.loads((root/'new/evidence/R201_ED_REF_01_SOURCE_RULE_AUDIT.json').read_text())
assert legal['status']=='PASS_R201_ED_REF01_SOURCE_RULE_CHECK' and len(profiles)==6
assert legal['source_sha256']==hashlib.sha256(profile_path.read_bytes()).hexdigest()
assert [profiles[str(i)]['natural_hp_max'] for i in range(1,7)]==[26,39,53,69,86,129]
assert [profiles[str(i)]['natural_pa_max'] for i in range(1,7)]==[22,31,42,54,68,116]
assert profiles['6']['ca_physical_exact']=='137/4'
assert legal['native_LEVELUP_engine_called'] is False
v2=sum((x['battles'] for x in cohorts[1:]));v1=cohorts[0]['battles']
assert v1==24 and v2==40
# Browser cannot run combat; check UI has seven tab IDs and direct receipt data, not fabricated python runner.
ui=(root/'new/ui/VLAB_R204_BANCADA_MAGIA_DISTANCIA_CORRIGIDA_OFFLINE.html').read_text()
assert len(re.findall(r'<button\b[^>]*class="tab(?: sel)?"[^>]*data-tab="',ui))==7 and 'data-tab="r204"' in ui and 'CHICOTE DE ÁGUA' in ui
report={'status':'PASS_R204_COLD_PORTABLE_RECOVERY','manifest_files':len(items),
 'baseline_r200_sha256':'6e462fa907f489ce72a5ee514203c69b995253f15cc2b05273fd44b7b8144f74',
 'R204_V1_conditional_fights_preserved':24,'R204_source_attack_corrected_fights':40,
 'R204_total_new_fights':64,'R201_orc_source_snapshots_checked':6,'native_LEVELUP_verified':False,
 'audits':cohorts,'magic_casts_total_ALL_VERSIONS':250,
 'magic_casts_source_corrected_V2_V2B':184,'magic_pa_corrected_V2_V2B':1472,
 'new_battles_reexecuted':0,'historical_battles_reexecuted':0,'old_RUN_ID_reused':0,
 'official_contracts_certified':0,'official_benchmark_cells':0,'production':'HOLD',
 'audit_independence':'SELF_CODE_SEPARATE_NOT_EXTERNAL_NAC_PASS'}
print(json.dumps(report,indent=2,ensure_ascii=False))
