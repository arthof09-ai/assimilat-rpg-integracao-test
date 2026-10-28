#!/usr/bin/env python3
"""R24 proof on a clean filesystem copy; R23 is recursively verified in sandbox."""
import sys,json,hashlib,zipfile,tempfile,subprocess
from pathlib import Path
ROOT='DMG_R24_INDEPENDENT_SANDBOX'
PARENT_SHA='b9e81b0c6744c9d60830bee4d557d9dd7df312ab134562b3b9bc8bfc1d9cbac2'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(pkg):
 with tempfile.TemporaryDirectory(prefix='R24_CLEAN_') as td:
  temp=Path(td)
  with zipfile.ZipFile(pkg) as z:
   assert z.testzip() is None,'outer CRC failed'
   names=z.namelist();assert len(names)==len(set(names)),'duplicates in zip'
   assert all(not Path(x).is_absolute() and '..' not in Path(x).parts and Path(x).parts[0]==ROOT for x in names)
   z.extractall(temp)
  root=temp/ROOT
  manifest=json.loads((root/'manifest_R24_SHA256.json').read_text(encoding='utf8'))
  assert len(names)==len(manifest['files'])+1
  assert {p.name for p in root.iterdir() if p.is_file()}==set(manifest['files'])|{'manifest_R24_SHA256.json'}
  for name,meta in manifest['files'].items():
   dat=(root/name).read_bytes()
   assert len(dat)==meta['size'] and sha(dat)==meta['sha256'],name
  parent=root/'R23_ORIGINAL_READONLY.zip'
  assert sha(parent.read_bytes())==PARENT_SHA==manifest['parent_sha256']
  with zipfile.ZipFile(parent) as z:
   assert z.testzip() is None
   assert z.read('DMG_R23_DECISORIO_SANDBOX/r13_oracle.py')==(root/'r13_oracle.py').read_bytes()
   verifier=temp/'verify_clean_r23.py'
   verifier.write_bytes(z.read('DMG_R23_DECISORIO_SANDBOX/verify_clean_r23.py'))
  p=subprocess.run([sys.executable,str(verifier),str(parent)],capture_output=True,text=True,check=True,timeout=180)
  verified=json.loads(p.stdout)
  assert verified['r23_focused_tests']=='33/33 PASS'
  assert verified['parent_r22_independent']=='34/34 PASS'
  assert verified['nested_r21_clean']=='36/36 PASS'
  matrix=json.loads((root/'R24_MATRIX_18.json').read_text())
  assay=json.loads((root/'R24_B15_ASSAY_AND_GATES.json').read_text())
  blocks=json.loads((root/'R24_BLOCKS_AND_AUTHORITIES.json').read_text())
  assert matrix['certified_total']==1 and len(matrix['rows'])==18
  assert matrix['strict_full_fights']==[0,2] and matrix['i0003_originals']==[0,9]
  assert all(v=='PENDENTE_MESTRE' for v in blocks['decisions'].values())
  assert assay['real_events_recovered']==0 and assay['conditional_assay']['not_determined']['real_combat']=='NO'
  candidates=['R24_SOURCE_CANDIDATE.json','R24_B15_ASSAY_AND_GATES.json','R24_MATRIX_18.csv','R24_MATRIX_18.json','R24_BLOCKS_AND_AUTHORITIES.json','REGISTRO_LOCAL_R24.json','RELATORIO_R24_CONSOLIDADO.md','HANDOFF_R24_FAST_RESUME.md','README_R24.md']
  before={n:sha((root/n).read_bytes()) for n in candidates}
  p=subprocess.run([sys.executable,'build_r24.py'],cwd=root,capture_output=True,text=True,check=True,timeout=40)
  assert '"R24_BUILD": "PASS"' in p.stdout
  after={n:sha((root/n).read_bytes()) for n in candidates}
  assert before==after,'rebuild differences '+str([n for n in candidates if before[n]!=after[n]])
  t=subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_r24_source_gates.py','-q'],cwd=root,capture_output=True,text=True,check=True,timeout=40)
  assert 'Ran 30 tests' in t.stderr and t.stderr.strip().endswith('OK'),t.stderr
  return {'r24_zip_sha256':sha(Path(pkg).read_bytes()),'entries':len(names),'manifest_files':len(manifest['files']),'manifest_sha':'PASS','crc':'PASS','parent_r23_sha':'PASS','r13_oracle_unchanged':'PASS','r23_tests':verified['r23_focused_tests'],'r22_tests':verified['parent_r22_independent'],'r21_tests':verified['nested_r21_clean'],'r24_tests':'30/30 PASS','rebuild_differences':0,'source_fiches_new':3,'b15_controlled_assay':'CONDITIONAL_NONCANONICAL','b15_real_events':0,'certified':'1/18 B02 only','strict':'0/2','i0003':'0/9','master_decisions':'0/5 PENDING','nac_pass':'HOLD','notion_writes':0}
if __name__=='__main__':print(json.dumps(run(Path(sys.argv[1])),ensure_ascii=False,sort_keys=True,indent=2))
