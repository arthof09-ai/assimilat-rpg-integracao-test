from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).resolve().parent
exclude={'MANIFEST_SHA256_R08.json','pack_r08.py','verificar_p0_r08.py'}
files=[p for p in sorted(D.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in exclude and p.suffix not in {'.zip','.pyc'}]
manifest={'asof':'2026-10-18','scope':'MESTRE-SIDE PA P0 R08 TEST; no Notion edits','n_files':len(files),'files':{str(f.relative_to(D)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(D/'MANIFEST_SHA256_R08.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
out=D.parent/'PA_P0_R08_ORIGINAIS_ATLAS_CORRECOES_TEST_20261018.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':z.write(p,p.relative_to(D))
with zipfile.ZipFile(out,'r') as z: bad=z.testzip();count=len(z.namelist())
print(json.dumps({'zip':str(out),'n_zip':count,'manifest':len(files),'crc_error':bad,'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size},ensure_ascii=False))
assert bad is None
