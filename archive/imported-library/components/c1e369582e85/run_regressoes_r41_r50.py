"""Repeatable read-only local regression matrix across available IBX-17 artifacts."""
from __future__ import annotations
import json, subprocess, re, sys, pathlib, hashlib
ROOT=pathlib.Path('/mnt/data')
CASES=[
 ('R39-local',ROOT/'ibx17_r39_inspect/IBX17_R39_CHECKUP_APROVACAO_HISTORICO_DELTA_20261016/IBX17_R39_DELTA','test_r39_version_gate'),
 ('R39A-local',ROOT/'ibx17_r39a_inline','test_r39a_inline_alternantes'),
 ('R40-local',ROOT/'ibx17_r40_release','test_ibx17_r40_readback_gate'),
 ('R41-extrator',ROOT/'ibx17_r41_r50','test_ibx17_r41_item_provenance'),
 ('R42-preview',ROOT/'ibx17_r41_r50','test_ibx17_r42_preview_bridge'),
 ('R46-child-guard',ROOT/'ibx17_r41_r50','test_ibx17_r46_child_native_guard'),
 ('R38-integracao-dependente',ROOT/'ibx17_r39_inspect/IBX17_R38_BRIDGE_NATIVE_CHAT_MESTRE_SIDE_20261016/IBX17_R38_DELTA','test_ibx17_r38_bridge'),
 ('R36-reader-dependente',ROOT/'ibx17_r39_inspect/IBX17_R36_LEITOR_PROVENIENCIA_DELTA_20261015/IBX17_R36_DELTA','test_r36_reader'),
 ('R36-leveldown-dependente',ROOT/'ibx17_r39_inspect/IBX17_R36_RECONCILIACAO_LEVELDOWN_DELTA_20261015','test_delta_r36'),
]
results=[]
for name,cwd,mod in CASES:
    p=subprocess.run([sys.executable,'-m','unittest','-q',mod],cwd=cwd,text=True,capture_output=True,timeout=25)
    log=p.stdout+p.stderr
    a=re.search(r'Ran (\d+) tests?',log)
    e=re.search(r'FAILED \((?:failures=(\d+), )?errors=(\d+)\)',log)
    n=int(a.group(1)) if a else 0
    errors=int(e.group(2)) if e else (1 if p.returncode else 0)
    results.append({'suite':name,'tests':n,'passed':n-errors if p.returncode else n,
                    'errors':errors,'return_code':p.returncode,
                    'status':'PASS_LOCAL' if p.returncode==0 else 'INCOMPLETE_DEPENDENCY_OR_TEST_ERROR',
                    'log_sha256':hashlib.sha256(log.encode()).hexdigest(),
                    'error_extract':log[-1400:] if p.returncode else ''})
report={'operation':'CM-000001/LEVEL-UP-ENGINE/IBX-17','phase':'R41-R50',
        'environment':'LOCAL_READ_ONLY','results':results,
        'complete_local_pass':sum(x['passed'] for x in results if x['return_code']==0),
        'complete_local_total':sum(x['tests'] for x in results if x['return_code']==0),
        'failed_or_blocked_suite_count':sum(x['return_code']!=0 for x in results),
        'native_NOTION_write_tests_are_not_counted_in_local_total':True,
        'no_game_motor_production_homologation':True}
(ROOT/'ibx17_r41_r50/REGRESSOES_R41_R50_EXECUTADAS.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2,ensure_ascii=False))
for r in results:print(r['suite'],r['status'],f"{r['passed']}/{r['tests']}",f"errors={r['errors']}")
