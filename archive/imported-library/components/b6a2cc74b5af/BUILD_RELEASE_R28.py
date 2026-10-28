from pathlib import Path
import json,hashlib,zipfile,shutil
ROOT=Path(__file__).resolve().parent
DEST=ROOT.parent/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip'
for p in ROOT.rglob('__pycache__'):
    if p.is_dir():shutil.rmtree(p)
for p in ROOT.rglob('*.pyc'):
    if p.is_file():p.unlink()
for p in ROOT.rglob('.DS_Store'):
    if p.is_file():p.unlink()
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST_R28.json')
manifest={'version':'R28-QMC05-NATIVE-PA-1.0.0-TEST','files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
  'asserted_chain':['CRAFT_QMC05_ORIGINAL','R28_NATIVE_ADDON','R27_ORIGINAL','R26_ORIGINAL'],
  'denominator':448,'result':'PASS TEST ONLY','production':'HOLD','party_write':0}
(ROOT/'MANIFEST_R28.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
allfiles=sorted(list(files)+[ROOT/'MANIFEST_R28.json'])
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
    for p in allfiles:
        zi=zipfile.ZipInfo(str(p.relative_to(ROOT)),date_time=(2026,10,20,1,0,0));zi.compress_type=zipfile.ZIP_DEFLATED
        zi.external_attr=0o644<<16
        z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
with zipfile.ZipFile(DEST) as z:
    bad=z.testzip(); names=set(z.namelist()); m=json.loads(z.read('MANIFEST_R28.json'))
    assert bad is None and len(names)==len(allfiles)
    assert len(m['files'])==len(files)
    for fn,h in m['files'].items():assert hashlib.sha256(z.read(fn)).hexdigest()==h,fn
print('ZIP',DEST,'SIZE',DEST.stat().st_size,'SHA256',hashlib.sha256(DEST.read_bytes()).hexdigest(),'HASHED',len(files),'TOTAL',len(allfiles),'CRC_PASS',bad is None)
