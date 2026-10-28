#!/usr/bin/env python3
"""Independent R23 recovery, source-byte integrity and narrow decision tests."""
import zipfile,hashlib,json,tempfile,subprocess,sys
from pathlib import Path
ROOT='DMG_R23_DECISORIO_SANDBOX'
PARENT_SHA='b95b51239ee3e74bf96599a7aa119c73ebb7667a2d434f5f61100a02d6a4d972'

def sha(b):return hashlib.sha256(b).hexdigest()
def run(path):
 with tempfile.TemporaryDirectory(prefix='R23_CLEAN_') as td:
  temp=Path(td); root=temp/ROOT
  with zipfile.ZipFile(path) as z:
   assert z.testzip() is None, 'ZIP CRC';entries=z.namelist()
   assert len(entries)==len(set(entries))
   for name in entries:
    pt=Path(name);assert not pt.is_absolute() and '..' not in pt.parts and pt.parts[0]==ROOT,name
   z.extractall(temp)
  m=json.loads((root/'manifest_R23_SHA256.json').read_text(encoding='utf8'))
  observed={p.name for p in root.iterdir() if p.is_file()}
  assert observed==set(m['files'])|{'manifest_R23_SHA256.json'},observed.symmetric_difference(set(m['files'])|{'manifest_R23_SHA256.json'})
  assert len(entries)==len(m['files'])+1
  for name,item in m['files'].items():
   p=root/name;assert p.stat().st_size==item['size'] and sha(p.read_bytes())==item['sha256'],name
  parent=root/'R22_ORIGINAL_READONLY.zip'
  assert sha(parent.read_bytes())==m['parent_SHA256']==PARENT_SHA
  with zipfile.ZipFile(parent) as z:
   assert z.testzip() is None
   assert (root/'r13_oracle.py').read_bytes()==z.read('DMG_R22_DECISIVE_EVIDENCE_SANDBOX/r13_oracle.py')
   parent_verify=temp/'verify_clean_r22.py';parent_verify.write_bytes(z.read('DMG_R22_DECISIVE_EVIDENCE_SANDBOX/verify_clean_r22.py'))
  parent_run=subprocess.run([sys.executable,str(parent_verify),str(parent)],capture_output=True,text=True,check=True,timeout=180)
  parent_report=json.loads(parent_run.stdout)
  assert parent_report['R22_focused_tests']=='34/34 PASS'
  assert parent_report['R21_independent_clean']['unit_tests']=='36/36 PASS'
  assert parent_report['R21_independent_clean']['R14_sha']=='PASS'
  reg=json.loads((root/'R23_DECISION_REGISTER.json').read_text(encoding='utf8'))
  matrix=json.loads((root/'R23_B01_B18_MATRIX.json').read_text(encoding='utf8'))
  b15=json.loads((root/'R23_B15_EVENT_CONTRACT.json').read_text(encoding='utf8'))
  assert len(reg['decisions'])==5 and reg['approval_count']==0 and all(not d['adopted'] for d in reg['decisions'])
  assert len(matrix['rows'])==18 and matrix['certified_total']==1 and matrix['nac_pass_terminal']=='HOLD'
  assert matrix['strict_fights']=={'completed':0,'required':2}
  assert matrix['i0003_original_csv']=={'authenticated':0,'expected':9}
  assert b15['real_events_recovered']==0 and b15['status']=='PROSPECTIVE_PLAN_NOT_EXECUTED'
  # Protection against subtle regression: rebuilding textual/JSON evidence must have bit-identical bytes.
  gen_files=['R23_DECISION_REGISTER.json','R23_SOURCE_PROVENANCE.json','R23_B15_EVENT_CONTRACT.json','R23_B01_B18_MATRIX.json','R23_LIU_STRICT_STATUS.json','R23_I0003_HOLD.json','R23_B01_B18_MATRIX.csv','DOSSIER_DECISORIO_R23.md','PLANO_EVIDENCIA_REAL_B15_R23.md','FOLHA_DECISOES_MESTRE_R23.md','RELATORIO_R23_CONSOLIDADO.md','HANDOFF_R23_FAST_RESUME.md','REGISTRO_LOCAL_R23.json','README_R23.md']
  before={k:sha((root/k).read_bytes()) for k in gen_files}
  p=subprocess.run([sys.executable,'build_r23.py'],cwd=root,capture_output=True,text=True,timeout=35,check=True)
  assert '"R23_BUILD": "PASS"' in p.stdout
  assert all(sha((root/k).read_bytes())==before[k] for k in gen_files),'R23 regeneration changed outputs'
  t=subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_r23_decision_gate.py','-q'],cwd=root,capture_output=True,text=True,timeout=35,check=True)
  assert 'Ran 33 tests' in t.stderr and t.stderr.strip().endswith('OK'),t.stderr
  with zipfile.ZipFile(root/'DOSSIER_DECISORIO_R23.docx') as z:
   assert z.testzip() is None and '[Content_Types].xml' in z.namelist()
   x=z.read('word/document.xml').decode('utf8')
   assert 'DEC-B11-A' in x and 'DEC-B12-B' in x
  return {'r23_zip_sha256':sha(Path(path).read_bytes()),'entries':len(entries),'manifest_files':len(m['files']),'manifest_sha':'PASS','crc':'PASS','parent_r22_sha':'PASS','parent_r22_independent':parent_report['R22_focused_tests'],'nested_r21_clean':parent_report['R21_independent_clean']['unit_tests'],'r13_oracle_immutable':'PASS','r23_focused_tests':'33/33 PASS','regenerated_diffs':0,'docx_internal_crc':'PASS','master_decisions_approved':0,'B01_B18':'1/18 B02 only','i0003_originals':'0/9','strict_fights':'0/2','notion_writes':0,'nac_pass_terminal':'HOLD'}
if __name__=='__main__':print(json.dumps(run(Path(sys.argv[1])),ensure_ascii=False,indent=2,sort_keys=True))
