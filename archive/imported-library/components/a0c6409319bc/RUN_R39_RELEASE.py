#!/usr/bin/env python3
"""Self-contained R39 reproduction; only reads and executes included TEST code locally."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
PARENTS={'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip':'d6d2e3a01d5aa7ec61d737d1297c7f7ea23588814594e3d9c0274495cff766c5',
         'CRAFT_PA_CORRIGENDA_MESTRE_TEST_20261020.zip':'ab880817ca732743011ee1f8f0269e303f6564e3a98c9a50fdf57ef7cd6320fa'}
EXTRA=['AUDITOR_COMPARADORES_R39.py','EVIDENCIAS_MECANICAS_READBACK_R39.json','CONSULTA_QUALIFICADA_R39_INPUT.json',
        'PINGENTE_R39_INPUT.json','test_r39_quality.py','CRIAR_R39_AUDITORIA.py']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def safeextract(zip_path,dest):
  with zipfile.ZipFile(zip_path) as z:
    if z.testzip():raise RuntimeError('CRC_FAIL')
    for x in z.namelist():
      p=Path(x)
      if x.startswith('/') or '..' in p.parts:raise RuntimeError('UNSAFE_ZIP_PATH')
    z.extractall(dest)

def run(cmd,cwd):
  p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
  if p.returncode:raise RuntimeError('FAILED '+str(cmd)+'\n'+(p.stdout+p.stderr)[-4500:])
  return p.stdout+p.stderr

def main():
  for name,expected in PARENTS.items():
    p=ROOT/name
    if not p.exists() or sha(p)!=expected:raise RuntimeError('PARENT_SHA_FAIL:'+name)
  with tempfile.TemporaryDirectory(prefix='pa_r39_replay_') as tmp:
    dest=Path(tmp)/'work';dest.mkdir()
    safeextract(ROOT/'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip',dest)
    for f in EXTRA:shutil.copy2(ROOT/f,dest/f)
    # The R29 runner authenticates and extracts R28, then runs its ten original suites.
    report=run([sys.executable,'RUN_R29_R38.py'],dest)
    old=json.loads((dest/'RUN_R29_R38_RESULT.json').read_text('utf8'))
    assert old['combined_tests']==478 and old['baseline_replayed']['passes']==448
    tests=run([sys.executable,'-m','unittest','-q','test_r39_quality'],dest)
    if 'Ran 32 tests' not in tests or 'OK' not in tests:raise RuntimeError('32_NEW_TESTS_NOT_CONFIRMED')
    source=dest/'r28/provider_r27/engine_r26/parecer_semicanonico_r26.py'
    bridge=dest/'r28/provider_r27/ponte_pa_craft_r27.py'
    before={'r26_sha':sha(source),'r27_sha':sha(bridge)}
    outputs={}
    for test,filename in [('botas','CONSULTA_QUALIFICADA_R39_INPUT.json'),('pingente','PINGENTE_R39_INPUT.json')]:
      out_path=dest/(test+'_receipt.json')
      run([sys.executable,'AUDITOR_COMPARADORES_R39.py','--input-json',filename,'--output',str(out_path)],dest)
      output=json.loads(out_path.read_text('utf8'))
      if (output['pa_por_dia'],output['pa_ativacao_no_cenario'],output['pa_total_cenario'])!=({'botas':(25,6,31),'pingente':(12,14,26)}[test]):
        raise RuntimeError('INTEGRATED_PA_MISMATCH:'+test)
      outputs[test]={'pa_por_dia':output['pa_por_dia'],'pa_ativacoes':output['pa_ativacao_no_cenario'],
                     'pa_total':output['pa_total_cenario'],'evidencias':output['qualidade_r39']['fontes_cotejadas'],
                     'SHA256':sha(out_path)}
    from_run=(dest/'RUN_R29_R38_RESULT.json').read_bytes()
    after={'r26_sha':sha(source),'r27_sha':sha(bridge)}
    if after!=before:raise RuntimeError('UNAUTHORIZED_TARIFF_CHANGE')
    result={'estado':'PASS_EXPERIMENTAL_PA_READONLY','testes_anteriores':478,'testes_novos':32,
        'total_suites_formal_tests':510,'originais_preservados':before,
        'readback_urls_independentes':len({v['url'] for v in json.loads((dest/'EVIDENCIAS_MECANICAS_READBACK_R39.json').read_text())['fontes'].values()}),
        'excertos_mecanicos':len(json.loads((dest/'EVIDENCIAS_MECANICAS_READBACK_R39.json').read_text())['fontes']),
        'fonte_rank_efeito_e0_independente':0,'rank_accuracy_percent':None,
        'recibos':outputs,'runtime_craft':'PROD_HOLD','craft_f5':'RED','c19_021':'UNKNOWN',
        'party_write':False,'notion_write_from_python':False,'historical_repricing':False}
  (ROOT/'RECIBO_REPLAY_R39.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
  print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
if __name__=='__main__':main()
