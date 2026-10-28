import zipfile,json,hashlib
from pathlib import Path
D=Path(__file__).parent
OUT=D.parent/'DMG-F1-R24-EVIDENCIA-EMPIRICA-INDEPENDENTE-v02.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
files=sorted(p for p in D.iterdir() if p.is_file() and p.name!='manifest_R24_V02_SHA256.json')
m={'version':'R24-v02','parent_sha256':'73db7ee5fc0735e8d77282eacec90370448474f58cab66f00bfd056783a029ba','files':{p.name:{'size':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in files},'provenance':'MASTER_SIDE_READ_ONLY; no real event'}
(D/'manifest_R24_V02_SHA256.json').write_text(json.dumps(m,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in files+[D/'manifest_R24_V02_SHA256.json']:z.write(p,arcname=D.name+'/'+p.name)
with zipfile.ZipFile(OUT) as z:assert z.testzip() is None
print(json.dumps({'file':str(OUT),'sha256':sha(OUT.read_bytes()),'entries':len(files)+1},indent=2))
