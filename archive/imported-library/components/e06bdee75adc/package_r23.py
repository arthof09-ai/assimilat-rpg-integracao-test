#!/usr/bin/env python3
import zipfile,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'DMG-F1-R23-DOSSIE-DECISORIO-E-B15-v02.zip'
PARENT_SHA='b95b51239ee3e74bf96599a7aa119c73ebb7667a2d434f5f61100a02d6a4d972'
assert hashlib.sha256((ROOT/'R22_ORIGINAL_READONLY.zip').read_bytes()).hexdigest()==PARENT_SHA
files=sorted([p for p in ROOT.iterdir() if p.is_file() and p.name!='manifest_R23_SHA256.json'])
m={'name':'DMG-F1-R23-DOSSIE-DECISORIO-E-B15-v02.zip','version':'R23','operation':'CM-000001/OP-DMG-CORPUS-EMP-01','parent_SHA256':PARENT_SHA,'status':'MASTER_DECISION_PENDING__NO_CANON_WRITE','r13_oracle_sha256':hashlib.sha256((ROOT/'r13_oracle.py').read_bytes()).hexdigest(),'file_count':len(files),'files':{p.name:{'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}}
(ROOT/'manifest_R23_SHA256.json').write_text(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(OUT,'w') as z:
 for p in sorted([p for p in ROOT.iterdir() if p.is_file()]):
  name=f'{ROOT.name}/{p.name}'
  zi=zipfile.ZipInfo(name,date_time=(2026,10,9,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16
  z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=7)
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)+1
print(json.dumps({'package':str(OUT),'SHA256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'bytes':OUT.stat().st_size,'zip_members':len(files)+1,'manifest_files':len(files)},indent=2))
