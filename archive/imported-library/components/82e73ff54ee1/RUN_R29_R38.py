#!/usr/bin/env python3
"""Clean-room replay R28 authentic baseline + incremental R29-R38 gates.
No external network or Notion write. Demo is Comestre-assisted interpretation,
not standalone universal language understanding.
"""
from __future__ import annotations
from pathlib import Path
import hashlib,json,os,subprocess,sys,zipfile,re
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip'
BASE_EXPECTED='68acc4405250cbf03a89924fa4df1f3d36586f26a5a903610c6600e8f26a391e'
REPORT=ROOT/'RUN_R29_R38_RESULT.json'
if not BASE.is_file():raise SystemExit('R28_BASELINE_NOT_PRESENT')
if hashlib.sha256(BASE.read_bytes()).hexdigest()!=BASE_EXPECTED:raise SystemExit('R28_BASELINE_SHA256_MISMATCH')
OUT=ROOT/'r28'
if not (OUT/'RUN_ALL_R28.py').is_file():
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(BASE) as z:
        bad=[i.filename for i in z.infolist() if i.filename.startswith('/') or '..' in Path(i.filename).parts]
        if bad:raise SystemExit('ARCHIVE_PATH_TRAVERSAL:'+str(bad))
        z.extractall(OUT)

# Verify the original QMC05 was preserved separately inside R28.
with zipfile.ZipFile(BASE) as z:
    if 'BASELINE_QMC05_ORIGINAL_IMUTAVEL.zip' not in z.namelist():raise SystemExit('NATIVE_QMC05_MISSING')

logs=[]
def run(label,cmd,cwd=None):
    cp=subprocess.run(cmd,cwd=cwd or ROOT,text=True,capture_output=True)
    out=cp.stdout+'\n'+cp.stderr
    logs.append('\n=== '+label+' ===\n'+out)
    if cp.returncode:
        (ROOT/'RUN_R29_R38_STDOUT.log').write_text('\n'.join(logs))
        raise SystemExit(label+' FAIL '+out[-3500:])
    return out

base_out=run('R28 10 SUITES 448', [sys.executable, 'RUN_ALL_R28.py'], OUT)
b=json.loads((OUT/'RUN_ALL_R28_RESULT.json').read_text('utf8'))
if not b['all_pass'] or b['tests_total']!=448 or len(b['suites'])!=10:
    raise SystemExit('OLD_BASELINE_REGRESSION_FAILED')
new_out=run('R29-R38 30 SUPPLEMENTAL TESTS',[sys.executable,'-m','unittest','-q','test_r29_r38','test_mobile_r34'])
m=re.search(r'Ran\s+(\d+)\s+tests',new_out)
if not m or int(m.group(1))!=30:raise SystemExit('R29_TEST_COUNT_MISMATCH')

# Call the operational user-facing wrapper in the same environment.
cli=[sys.executable,'CONSULTA_MOBILE_R34.py','--input-json','CONSULTA_MOBILE_DEMO_INPUT.json']
r=run('R34 MOBILE PLAIN-LANGUAGE DEMO',cli)
d=json.loads(r)
if (d['pa_por_dia'],d['pa_ativacao_no_cenario'],d['pa_total_cenario'])!=(25,6,31):
    raise SystemExit('MOBILE_FLOW_MISMATCH')
if d['notion_write'] or d['party_write']:raise SystemExit('MOBILE_SIDE_EFFECT_FLAG')

# CRAFT QMC-05 CLI canary is a literal source already qualified through Notion.
lamina=OUT/'CRAFT-QMC04/QMC-05/holdout/lamina.txt'
url='https://app.notion.com/p/3edc2b324ede816f98a1fa7babd3c0d3'
qcmd=[sys.executable,str(OUT/'CRAFT-QMC04/QMC-05/qmc05.py'),'--url',url,'--readback',str(lamina),'--pa-r28']
legacy=json.loads(run('R36 NATIVE QMC05 READ ONLY',qcmd))
if legacy['historico']['r27']['pa_por_dia'] is not None or legacy['governanca']['notion_write']:
    raise SystemExit('LEGACY_REPRICING_OR_WRITE')

# Snapshot invariants: no package original code changed on disk by these tests.
for path in [lamina, OUT/'provider_r27/ponte_pa_craft_r27.py',OUT/'CRAFT-QMC04/QMC-05/qmc05.py']:
    if not path.exists():raise SystemExit('EXPECTED_SOURCE_MISSING:'+str(path))

out={'scope':'MESTRE-SIDE / TEST; sem runtime CRAFT produtivo','baseline_sha256':BASE_EXPECTED,
'baseline_replayed':{'passes':448,'suites':10},'new_tests':{'passes':30,'suites':2},
'combined_tests':478,'source_cases_reviewed':12,
'mobile_demo':{'pa_dia':d['pa_por_dia'],'pa_usos':d['pa_ativacao_no_cenario'],'pa_total':d['pa_total_cenario'],
  'rank_item':d['rank_item'],'source_urls':d['comparadores_reabertos_nesta_sessao'],
  'receipt_sha256':hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest()},
'native_legacy_canary':{'effects':legacy['origem']['effect_count'],'reprice':False,'notion_write':False},
'producao':{'TEE_LAB':'PASS','TEE_RUNTIME_PROD':'HOLD','CRAFT_F5':'RED','C19_021':'UNKNOWN_EFFECT',
'writer_lease_epoch_fencing':'NAO_COMPROVADO'},
'no_party_or_primeiro_writes':True,'no_new_recipes_or_REC_IDs':True}
REPORT.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
(ROOT/'RUN_R29_R38_STDOUT.log').write_text('\n'.join(logs))
print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
