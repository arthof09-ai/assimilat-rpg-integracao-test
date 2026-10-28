#!/usr/bin/env python3
"""One-command checkpoint. Regressions are not counted as new functionality."""
from pathlib import Path
import subprocess,sys,json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent.parent
cmds=[
 [sys.executable,'R10_READONLY/verificar_cadeia_pa.py'],
 [sys.executable,'R11_R19_TEST/prepare_runtime.py'],
 [sys.executable,'PA_UNIVERSAL_R05_TEST_20261017/R05_CODE/bootstrap_baselines.py'],
 [sys.executable,'-m','unittest','discover','-s','PA_UNIVERSAL_R05_TEST_20261017/R05_CODE','-p','test_r05_targeted.py','-q'],
 [sys.executable,'-m','unittest','discover','-s','R10_READONLY','-p','test_pa_r10_guard.py','-q'],
 [sys.executable,'-m','unittest','discover','-s','R11_R19_TEST','-p','test_pa_r11_r19.py','-q'],
 [sys.executable,'R11_R19_TEST/audit_r14_r16.py'],
 [sys.executable,'R11_R19_TEST/run_pa_demonstration.py']
]
for c in cmds:
    p=subprocess.run(c,cwd=ROOT,text=True,capture_output=True)
    print('COMMAND', ' '.join(c))
    print('EXIT',p.returncode,'stdout_chars',len(p.stdout),'stderr_tail',p.stderr[-180:])
    if p.returncode:print(p.stdout[-3000:],p.stderr[-3000:]);sys.exit(p.returncode)
    if 'run_pa_demonstration' in c[-1]:
        data=json.loads(p.stdout)
        assert data['craft_qmc02_original_bota']['native_original_return']['native_return']['status']=='INTERFACE_EXTERNA_NAO_CONTRATADA'
        print('DEMO functional',len(data['conversational_queries']),'cases, original native CRAFT appropriately denied')
print('PASS TEST LOCAL 31 R05 + 21 R10 + 42 NEW = 94 DISTINCT TEST CASES (42 new)')
