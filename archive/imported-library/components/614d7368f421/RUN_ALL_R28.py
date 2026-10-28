#!/usr/bin/env python3
"""R28 reproducible test runner; counts unique test methods per suite.
Does not download external data, modify Notion, or promote a release.
"""
from __future__ import annotations
import json,re,subprocess,sys,os,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NATIVE=ROOT/'CRAFT-QMC04'
PA=ROOT/'provider_r27'
PY=sys.executable
SUITES=[
 ('CRAFT-QMC02',NATIVE,[PY,'-m','unittest','discover','-s','QMC-02/qmc02','-p','test_*.py','-q'],37),
 ('CRAFT-QMC03',NATIVE,[PY,'-m','unittest','discover','-s','QMC-03','-p','test_qmc03.py','-q'],40),
 ('CRAFT-QMC04',NATIVE,[PY,'-m','unittest','discover','-s','QMC-04','-p','test_qmc04.py','-q'],50),
 ('CRAFT-QMC05',NATIVE,[PY,'-m','unittest','discover','-s','QMC-05','-p','test_qmc05.py','-q'],47),
 ('CRAFT-R05-PROVIDER-REAL',NATIVE,[PY,'-m','unittest','discover','-s','QMC-05','-p','test_pa_r05_external.py','-q'],5),
 ('CRAFT-QMC05-DELTA01',NATIVE,[PY,'-m','unittest','discover','-s','QMC-05-DELTA','-p','test_qmc05_delta.py','-q'],28),
 ('CRAFT-PA-R28-NATIVO',NATIVE,[PY,'-m','unittest','discover','-s','QMC-05','-p','test_pa_r28_native.py','-q'],30),
 ('PA-R27',PA,[PY,'-m','unittest','-q','test_ponte_pa_craft_r27'],22),
 ('PA-R26',PA,[PY,'-m','unittest','-q','engine_r26.test_r26_decisao'],26),
 ('PA-R22-R25',PA/'engine_r26/baseline_r25',[PY,'-m','unittest','-q','test_r25_qualidade','test_integracao_r24','test_motor_conversacional_r24','test_alcance_mestre_r23','test_ponte_pa_r23','baseline_r22.test_rank_guard_r22'],163),
]
records=[];logs=[]
for name,cwd,cmd,expected in SUITES:
    e=os.environ.copy();e['PA_R05_ROOT']=str(ROOT/'PA_R05_PROVENANCE/PA_UNIVERSAL_R05_TEST_20261017')
    if name=='PA-R26':e['PYTHONPATH']=str(PA/'engine_r26')
    if name=='PA-R22-R25':e['PYTHONPATH']='.:baseline_r22'
    r=subprocess.run(cmd,cwd=cwd,env=e,capture_output=True,text=True)
    std=(r.stdout+'\n'+r.stderr).strip()
    m=re.search(r'Ran\s+(\d+)\s+tests',std)
    counted=int(m.group(1)) if m else -1
    ok=r.returncode==0 and counted==expected and ('OK' in std)
    records.append({'suite':name,'count':counted,'expected':expected,'success':ok,'returncode':r.returncode})
    logs.append('\n=== '+name+' ===\n' + std+'\n')
    print(name, 'PASS' if ok else 'FAIL',f'{counted}/{expected}',flush=True)
    if not ok:
        print(std[-3500:]);break
count=sum(r['count'] for r in records if r['count']>0)
report={'runner_version':'R28-QMC05-PA-NATIVE-1','python':sys.version.split()[0],
        'tests_total':count,'expected_total':sum(r[3] for r in SUITES),
        'all_pass':len(records)==len(SUITES) and all(x['success'] for x in records),
        'suites':records,'no_notional_writes':True,'party_writer':False}
(ROOT/'RUN_ALL_R28_RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(ROOT/'RUN_ALL_R28_STDOUT.log').write_text('\n'.join(logs))
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['all_pass']:raise SystemExit(1)
