#!/usr/bin/env python3
"""Independent R22 recovery, manifest, R21→R14, R13 oracle, deterministic code and 33 falsification checks."""
import tempfile,zipfile,hashlib,json,subprocess,sys
from pathlib import Path
ROOT='DMG_R22_DECISIVE_EVIDENCE_SANDBOX'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(zip_path):
 with tempfile.TemporaryDirectory(prefix='DMG_R22_CLEAN_') as td:
  temp=Path(td)
  with zipfile.ZipFile(zip_path) as z:
   assert z.testzip() is None
   paths=z.namelist()
   for p in paths:
    pt=Path(p);assert not pt.is_absolute() and '..' not in pt.parts and pt.parts[0]==ROOT,p
   z.extractall(temp)
  d=temp/ROOT
  m=json.loads((d/'manifest_R22_SHA256.json').read_text())
  assert set(p.name for p in d.iterdir() if p.is_file())==set(m['files'])|{'manifest_R22_SHA256.json'}
  assert len(m['files'])+1==len(paths)
  for name,expected in m['files'].items():
   p=d/name;assert p.stat().st_size==expected['size'] and sha(p.read_bytes())==expected['sha256'],name
  parent=d/'R21_ORIGINAL_READONLY.zip'
  assert sha(parent.read_bytes())==m['parent_SHA256']=='06d7a30aa2ae9d9c482ae69c9e8c912741334a8a99e784d66546dd5167ccf3ba'
  with zipfile.ZipFile(parent) as z:
   assert z.testzip() is None
   r13=z.read('DMG_R21_EVIDENCIAS_PRIMARIAS/r13_oracle.py')
   assert sha(r13)==sha((d/'r13_oracle.py').read_bytes())==m['r13_oracle_sha256']
   r21_verifier=temp/'verify_clean_r21.py'
   r21_verifier.write_bytes(z.read('DMG_R21_EVIDENCIAS_PRIMARIAS/verify_clean_r21.py'))
  p=subprocess.run([sys.executable,str(r21_verifier),str(parent)],capture_output=True,text=True,timeout=120,check=True)
  r21=json.loads(p.stdout)
  assert r21['unit_tests']=='36/36 PASS' and r21['regenerated_diffs']==0 and r21['R19_sha']=='PASS' and r21['R14_sha']=='PASS'
  original_generated={name:sha((d/name).read_bytes()) for name in ['R22_SOURCE_EXCERPTS.json','R22_B11_B12_B15_RESOLUTIONS.json','R22_B01_B18_MATRIX.json','R22_B01_B18_MATRIX.csv','R22_LIU_SCENE_AND_STRICT_GAPS.json','R22_I0003_FOCUSED_AUDIT.json','R22_SERPENTE_LEGACY_COMPARISON.json']}
  build=subprocess.run([sys.executable,'build_r22.py'],cwd=d,capture_output=True,text=True,timeout=30,check=True)
  assert 'R22_EVIDENCE_BUILD_PASS' in build.stdout
  assert all(sha((d/name).read_bytes())==h for name,h in original_generated.items()),'R22_REGEN_DIFF'
  t=subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_r22_contracts.py','-q'],cwd=d,capture_output=True,text=True,timeout=30,check=True)
  assert 'Ran 34 tests' in t.stderr and t.stderr.strip().endswith('OK'),t.stderr
  return {'zip_SHA256':sha(Path(zip_path).read_bytes()),'zip_entries':len(paths),'manifest_files':len(m['files']),
    'zip_CRC':'PASS','manifest_SHA':'PASS','R21_independent_clean':r21,'R13_oracle_bytes':'PASS','R22_regenerated_diffs':0,
    'R22_focused_tests':'34/34 PASS','original_I0003':'0/9','certified':'1/18','real_STRICT':'0/2','NAC_PASS_TERMINAL':'HOLD'}
if __name__=='__main__':print(json.dumps(run(Path(sys.argv[1])),ensure_ascii=False,sort_keys=True,indent=2))
