#!/usr/bin/env python3
"""R198 portable COLD verifier — audits existing R18 SQLite; NEVER executes fights."""
import pathlib,json,hashlib,zipfile,sys,importlib.util,collections
ROOT=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((ROOT/'R198_SHA256_MANIFEST.json').read_text())
files=manifest['files']
errors=[]
for relative,expected in files.items():
 path=ROOT/relative
 if not path.is_file():errors.append('MISSING '+relative);continue
 if sha(path.read_bytes())!=expected:errors.append('SHA_DRIFT '+relative)
if errors:raise AssertionError(str(errors[:18]))
assert len(files)==manifest['denominator']
original=ROOT/'baseline/VLAB_R197_POWER_BENCH_MESTRE_ONLY.zip'
assert sha(original.read_bytes())=='6b63f53ea35627f390feee8b695380ee9ea1bba8654c5ca2e0e4447219029602'
with zipfile.ZipFile(original) as z:
 assert z.testzip() is None
 assert sha(z.read('baseline/VLAB_R187_R196_EXACT.zip'))=='7dc3a95aafa7dfc4db6ae0d99f7c0474e630ea86f0f70dff4112abf771403786'
 originalmanifest=json.loads(z.read('R197_SHA256_MANIFEST.json'))
 assert all(sha(z.read(p))==h for p,h in originalmanifest['entries'].items())
for relative,expect in {
 'work/runtime/native/vlab_effects_v08.py':'4502665346741ff231b79659d881bdac252112f42e91bce7d0747f3e18344dc1',
 'work/runtime/work/fusion_stage12/vlab_r18_interactive.py':'f1336caa0255ab2c6d9e20f2f3f87edf682e97fe6d04c1e2373518d5ae74d368',
 'work/runtime/r172/r172_atomic_counter.py':'c6e546481baa2c90eee714dd0ffb573469c418ee0170b5a53ace56fce64b8aa1'
}.items():assert sha((ROOT/relative).read_bytes())==expect,relative

sys.path.insert(0,str(ROOT/'new/code'))
import r198_independent_replay as basic
import r198_magic_independent_audit as magic
ba=[basic.audit(p) for p in sorted((ROOT/'new/evidence/db').glob('R198_*.sqlite'))]
ma=[magic.audit(p) for p in sorted((ROOT/'new/evidence/magic_db').glob('R198_MAGIC*.sqlite'))]
assert len(ba)==38 and sum(z['attacks'] for z in ba)==389 and sum(z['commits'] for z in ba)==427 and sum(z['native_events'] for z in ba)==1167
assert len(ma)==8 and sum(z['casts'] for z in ma)==20 and sum(z['pa_spent'] for z in ma)==160 and sum(z['commits'] for z in ma)==96 and sum(z['events'] for z in ma)==284
b=json.loads((ROOT/'new/evidence/R198_BENCHMARK_RESULTS.json').read_text());m=json.loads((ROOT/'new/evidence/R198_MAGIC_BENCHMARK.json').read_text())
assert len(b['runs'])==40 and b['executed_fights']==38 and b['initiatives_held_pre_commit']==2 and b['official_benchmark_cells']==0 and b['certified_contracts']==0
assert len(m['records'])==8 and m['casts']==20 and m['total_pa_spent']==160
# The fixed precommit initiative holds must not have physical banks and cannot be victories.
assert sum(z.get('db') is None for z in b['runs'])==2
for z in b['runs']:
 if z['status']=='PRECOMMIT_TIE_HOLD':assert z.get('db') is None and z.get('winner') is None
# Replay audit must reject semantically tampered clones even if SQLite row hashes are self-consistent.
neg=json.loads((ROOT/'new/evidence/R198_ADVERSARIAL_REPORT.json').read_text())
rejected=[]
for c in neg['cases']:
 p=ROOT/'new'/c['clone']
 try:(magic.audit if 'MAGIC_' in c['case'] else basic.audit)(p)
 except Exception as exc:rejected.append(c['case'])
 else:raise AssertionError('UNDETECTED_TAMPER '+c['case'])
assert len(rejected)==7 and neg['status']=='PASS_REBUILT_HASH_FORGERY_REJECTED'
# R197 HTML retained as exact byte-identical copy; R198 adds a fourth read-only tab and PA pilot.
assert (ROOT/'work/r197/ui/VLAB_R197_BANCADA_PODER_OFFLINE.html').read_bytes()==zipfile.ZipFile(original).read('ui/VLAB_R197_BANCADA_PODER_OFFLINE.html')
html=(ROOT/'new/ui/VLAB_R198_COMBATES_E_MAGIA_OFFLINE.html').read_text()
assert 'data-tab="combates"' in html
assert 'id="r198-data"' in html and 'r198-magic-data' in html
assert len(json.loads((ROOT/'new/source/R198_ORIGINAL_17_CONTRACT_CROSSWALK_PRESERVED.json').read_text())['original_id_sequence'])==17
assert json.loads((ROOT/'new/source/R198_CONTRACT_AND_BENCHMARK_DELTA.json').read_text())['official_after']==0
out={'status':'PASS_R198_COLD_PORTABLE_RECOVERY','as_of':'2026-10-19','file_hashes':len(files),
 'baseline_R197_sha256':sha(original.read_bytes()),'baseline_R196_nested_sha256':'7dc3a95aafa7dfc4db6ae0d99f7c0474e630ea86f0f70dff4112abf771403786',
 'core_fights':len(ba),'core_attacks':sum(z['attacks'] for z in ba),'core_commits':sum(z['commits'] for z in ba),
 'core_native_events':sum(z['native_events']for z in ba),'initiative_holds_before_commit':2,
 'magic_fights':len(ma),'magic_casts':sum(z['casts']for z in ma),'magic_pa_spent':sum(z['pa_spent']for z in ma),
 'total_completed_fights':len(ba)+len(ma),'total_commits':sum(z['commits']for z in ba)+sum(z['commits']for z in ma),
 'total_native_events':sum(z['native_events']for z in ba)+sum(z['events']for z in ma),
 'forged_hash_clones_semantically_rejected':rejected,'historical_fights_rerun':0,
 'terminal_contracts':0,'official_benchmarks':0,'production':'HOLD','external_audit':False}
print(json.dumps(out,ensure_ascii=False,indent=2))
if len(sys.argv)>1:pathlib.Path(sys.argv[1]).write_text(json.dumps(out,ensure_ascii=False,indent=2))
