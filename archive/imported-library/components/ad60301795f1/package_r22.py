#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile, ZIP_DEFLATED
import json,subprocess,sys
HERE=Path(__file__).resolve().parent
ZIP=HERE.parent/'DMG-F1-R22-RESOLUCAO-NORMATIVA-E-CENA-v02.zip'
def hash_file(p):return sha256(p.read_bytes()).hexdigest()
def main():
    run=subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_r22_contracts.py','-q'],cwd=HERE,capture_output=True,text=True)
    assert run.returncode==0 and 'Ran 34 tests' in run.stderr,(run.stderr,run.stdout)
    assert hash_file(HERE/'R21_ORIGINAL_READONLY.zip')=='06d7a30aa2ae9d9c482ae69c9e8c912741334a8a99e784d66546dd5167ccf3ba'
    with ZipFile(HERE/'R21_ORIGINAL_READONLY.zip') as parent:
        assert parent.testzip() is None
        assert hash_file(HERE/'r13_oracle.py')==sha256(parent.read('DMG_R21_EVIDENCIAS_PRIMARIAS/r13_oracle.py')).hexdigest()
    qa={
      'checkpoint':'R22','local_new_tests':'34/34 PASS','parent_R21_clean':'36/36 PASS','parent_R21_zip_SHA256':hash_file(HERE/'R21_ORIGINAL_READONLY.zip'),
      'R13_oracle_byte_identical':True,'notion_primary_full_pages_frozen':False,'notion_canonical_writes':0,
      'science_full_certifications':'1/18 B02 documental','i0003_raw':'0/9','strict_real':'0/2','terminal_nac_pass':'HOLD',
      'gain':'R22 rule DMG-RANK v1.1 §23 closes infinite DoT stacking default; other Decepadora version +30 not Liu +18, axe/sword eligibility audit; B15 typed element mapping clarified',
      'validation_scope':'LOCAL_PACKAGE_AND_SOURCED_SNIPPETS_NOT_OFFICIAL_SCENE'}
    (HERE/'QA_R22_REPORT.json').write_text(json.dumps(qa,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
    artifacts=[p for p in HERE.iterdir() if p.is_file() and p.name not in ('manifest_R22_SHA256.json',)]
    filelist={p.name:{'size':p.stat().st_size,'sha256':hash_file(p)} for p in sorted(artifacts,key=lambda p:p.name)}
    manifest={'name':'DMG-F1-R22','revision':'R22','file_count':len(filelist),'parent_SHA256':hash_file(HERE/'R21_ORIGINAL_READONLY.zip'),
              'r13_oracle_sha256':hash_file(HERE/'r13_oracle.py'),'files':filelist}
    (HERE/'manifest_R22_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
    with ZipFile(ZIP,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted([x for x in HERE.iterdir() if x.is_file()],key=lambda x:x.name):
            z.write(p,arcname=HERE.name+'/'+p.name)
    with ZipFile(ZIP) as z:
        assert z.testzip() is None
    print(json.dumps({'zip':str(ZIP),'zip_SHA256':hash_file(ZIP),'zip_entries':len(filelist)+1,'manifest_files':len(filelist),'r22_tests':'34/34 PASS'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
