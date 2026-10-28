"""Cold native TEST replay. All code/baselines included within final ZIP.
Does not write Notion, Party, official stores, user files or production.
"""
from __future__ import annotations
from pathlib import Path
import tempfile,zipfile,hashlib,shutil,subprocess,sys,json,os
HOME=Path(__file__).resolve().parent
BASE={
 'R40':'899ea34d81025356af26b462272273244c8405f05493f6f664aa05ad9d481f11',
 'R39':'daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32'
}
R39ENV='1d4e43e1f8b21106e0c8fee25bab53a81528e4a903f3184852b768dade48c4ea'
ROOT_BASE={'R40':'CRAFT_PA_R40_RI_RE_R48_ORIGINAL_TEST_20261020.zip',
           'R39':'PA_R39_CONSULTOR_EVIDENCIAS_QUALIFICADAS_TEST_20261020.zip'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def extract(src,dst):
 with zipfile.ZipFile(src) as z:
  if z.testzip():raise RuntimeError('ZIP_CRC_FAIL:'+str(src))
  for n in z.namelist():
   p=Path(n)
   if n.startswith('/') or '..' in p.parts:raise RuntimeError('UNSAFE_ZIP_MEMBER:'+n)
  z.extractall(dst)
def run(args,cwd=None):
 proc=subprocess.run([str(x) for x in args],cwd=cwd,text=True,capture_output=True)
 if proc.returncode:
  raise RuntimeError('REPLAY_FAILED '+repr(args)+'\n'+proc.stdout[-2500:]+'\n'+proc.stderr[-4500:])
 return proc.stdout+'\n'+proc.stderr

def main():
 for kind,f in ROOT_BASE.items():
  expected=BASE[kind]
  actual=sha(HOME/'baselines'/f)
  if actual!=expected:raise RuntimeError('ORIGINAL_BASELINE_SHA_CHANGED:'+f)
 if sha(HOME/'R39_PINGENTE_ENVELOPE_NATIVE.json')!=R39ENV:
  raise RuntimeError('R39_INPUT_ANCHOR_CHANGED')
 with tempfile.TemporaryDirectory(prefix='CRAFT_E21_E30_COLD_') as d:
  tmp=Path(d)
  target=tmp/'runner';target.mkdir()
  for name in ('build_lab_extension.py','r48_pa_gate.py','native_pingente_runner.py','durable_pingente_demo.py','test_native_e21.py','R39_PINGENTE_ENVELOPE_NATIVE.json','R39_SOURCE_READBACK_20261020.json','requery_r39.py'):
   shutil.copy2(HOME/name,target/name)
  (target/'baseline_extracted').mkdir()
  for kind,filename in ROOT_BASE.items():extract(HOME/'baselines'/filename,target/'baseline_extracted'/kind)
  orig=target/'baseline_extracted/R40/R48_ORIGINAL'
  manifest=run([sys.executable,'R40/VERIFY_R40_MANIFEST.py'],cwd=target/'baseline_extracted/R40')
  if 'PASS_MANIFEST_R40 185' not in manifest:raise RuntimeError('R40_MANIFEST')
  canary=run([sys.executable,'R40/EXECUTAR_R48_CANARIO_R40.py',orig],cwd=target/'baseline_extracted/R40')
  c=json.loads(canary);assert c['result']=='PASS_R48_NATIVE_ORIGINAL_CANARY'
  r39=target/'baseline_extracted/R39';runtime=target/'r39_runtime';runtime.mkdir()
  extract(r39/'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip',runtime)
  extract(runtime/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip',runtime/'r28')
  for name in ['AUDITOR_COMPARADORES_R39.py','EVIDENCIAS_MECANICAS_READBACK_R39.json',
               'PINGENTE_R39_INPUT.json','CONSULTA_QUALIFICADA_R39_INPUT.json','test_r39_quality.py']:
   shutil.copy2(r39/name,runtime/name)
  shutil.copy2(HOME/'requery_r39.py',runtime/'requery_r39.py')
  r39tests=run([sys.executable,'-m','unittest','-q','test_r39_quality'],cwd=runtime)
  if 'Ran 32 tests' not in r39tests:raise RuntimeError('R39_32_NOT_CONFIRMED')
  requery=json.loads(run([sys.executable,'requery_r39.py'],cwd=runtime).strip())
  if requery['sha256']!=R39ENV:raise RuntimeError('R39_REQUERY_CHANGED')
  shutil.copytree(orig,target/'native_lab/R48_TEST_EXTENDED')
  run([sys.executable,'build_lab_extension.py'],cwd=target)
  originaltests=run([sys.executable,'-m','unittest','discover','-s','tests','-q'],cwd=target/'native_lab/R48_TEST_EXTENDED')
  if 'Ran 40 tests' not in originaltests:raise RuntimeError('R48_40_NOT_CONFIRMED')
  newtests=run([sys.executable,'-m','unittest','-q','test_native_e21'],cwd=target)
  if 'Ran 28 tests' not in newtests:raise RuntimeError('CRAFT_28_NOT_CONFIRMED')
  run([sys.executable,'native_pingente_runner.py'],cwd=target)
  run([sys.executable,'durable_pingente_demo.py'],cwd=target)
  native=json.loads((target/'results/DURABLE_R48_PINGENTE_RESULTS.json').read_text())
  if native['structural']['status']!='EXPERIMENTAL_QA_PASS' or native['durable_store']['after_seq']!=1:
   raise RuntimeError('R48_NATIVE_EXECUTION_MISSING')
  if not native['replay']['unchanged'] or native['structural']['physical_products']:
   raise RuntimeError('R48_BAD_READBACK_OR_PHYSICAL_PROMOTION')
  report={'replay':'PASS_CRAFT_E21_E30','scope':'TEST_ONLY','archive_integrity':'PASS',
    'r40_manifest_files':185,'r39_qualified_envelope_sha256':R39ENV,
    'r48_original_canary':'PASS','r48_original_regressions':40,'r39_new_regressions':32,
    'craft_extension_new_regressions':28,'tests_distinct':100,
    'r48_extended_pingente':'NATIVE_STRUCTURAL_SYNTHETIC_RECEIPT','batch_id':native['structural']['batch_id'],
    'order_id':native['structural']['order_id'],'r48_head':native['structural']['r48_head'],
    'journal_seq':native['durable_store']['after_seq'],'idempotent':native['replay']['idempotent'],
    'synthetic_sample_count':native['structural']['synthetic_products'],
    'material_products':0,'magic_transfer':'NOT_DEMONSTRATED','official_production':'HOLD',
    'party_changes':False,'first_p0_objective':'PASS_NATIVE_R48_TEST_STRUCTURAL_ONLY'}
 (HOME/'REPLAY_E21_E30_RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
