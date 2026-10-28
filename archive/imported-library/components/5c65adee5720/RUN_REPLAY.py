#!/usr/bin/env python3
"""Cold replay. Authenticates archived R39/R48, re-invokes original R39→R34→R27→R26,
then audits the CO-GM adjudicated rule record. Does not simulate or grant magic.
"""
from __future__ import annotations
import hashlib,json,zipfile,tempfile,subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
base=ROOT/'baselines'
r39=base/'PA_R39_CONSULTOR_EVIDENCIAS_QUALIFICADAS_TEST_20261020.zip'
r48=base/'CRAFT_E21_E30_R39_R48_NATIVE_TEST_20261020.zip'
expected={'r39':'daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32','r48':'d0b113244cf590a9c30be34c5893c332a08a8e15daa3c17aa9be4cf5356104f0'}
assert sha(r39)==expected['r39'],'R39_BASELINE_CHANGED'
assert sha(r48)==expected['r48'],'R48_BASELINE_CHANGED'
for p in (r39,r48):
 with zipfile.ZipFile(p) as z:assert z.testzip() is None,'ZIP_CRC_INVALIDO'
with tempfile.TemporaryDirectory(prefix='craft_h1_original_pa_') as scratch:
 tmp=Path(scratch)
 with zipfile.ZipFile(r39) as z:z.extractall(tmp/'r39')
 with zipfile.ZipFile(tmp/'r39'/'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip') as z:z.extractall(tmp/'r29')
 with zipfile.ZipFile(tmp/'r29'/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip') as z:z.extractall(tmp/'r28')
 (tmp/'r29'/'r28').symlink_to('../r28',target_is_directory=True)
 p=tmp/'r39'/'AUDITOR_COMPARADORES_R39.py'
 assert p.is_file()
 env=os.environ.copy();env['PYTHONPATH']=os.pathsep.join(map(str,[tmp/'r39',tmp/'r29',tmp/'r28'/'provider_r27']))
 input_path=ROOT/'H1_R39_CONSULTA_ENTRADA.json'
 body='''import json,sys
from pathlib import Path
from AUDITOR_COMPARADORES_R39 import envelope_craft_qualificado
p=json.loads(Path(sys.argv[1]).read_text('utf8'))
o=envelope_craft_qualificado(p['descricao_original'],p['interpretacao'])
print(json.dumps(o,sort_keys=True,ensure_ascii=False))'''
 cp=subprocess.run([sys.executable,'-c',body,str(input_path)],env=env,capture_output=True,text=True,check=True,timeout=30)
 actual=json.loads(cp.stdout);expected_pa=json.loads((ROOT/'PA_R39_H1_CONSULTA_REAL.json').read_text('utf8'))
 assert actual==expected_pa,'ORIGINAL_PA_REPLAY_MISMATCH'
 assert actual['gate_r39']=='CONSULTA_TEST_PARCIAL_EVIDENCIA_INSUFICIENTE'
 assert all(v is None for v in actual['custo_pa_qualificado'].values())
 print('PA_ORIGINAL_R39_R34_R27_R26_COLD_REPLAY_EXACT_MATCH',actual['id_entrada_sha256'])
# Must use a new process so Python unittest imports case module from provided bundle.
run=subprocess.run([sys.executable,str(ROOT/'audit_scene.py')],text=True,capture_output=True,check=True,timeout=20)
print(run.stderr.strip())
print('R48_HISTORICAL_STORE_READ_ONLY_SEQ1_VERIFIED')
print('PASS_CRAFT_H1_RULE_APPLIED_H2_CONTRACT_PENDING_NO_PARTY_WRITE')
