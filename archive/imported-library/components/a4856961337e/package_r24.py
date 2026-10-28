#!/usr/bin/env python3
"""Build immutable-looking R24 archive; does not touch R23 parent or sources."""
from pathlib import Path
import hashlib,zipfile,json
D=Path(__file__).parent
OUT=D.parent/'DMG-F1-R24-EVIDENCIA-FONTE-E-ENSAIO-CONTROLADO-v01.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
files=sorted(p for p in D.iterdir() if p.is_file() and p.name!='manifest_R24_SHA256.json' and not p.name.endswith('.zip.bak'))
m={'version':'R24-01','operation':'CM-000001 / OP-DMG-CORPUS-EMP-01','parent_sha256':'b9e81b0c6744c9d60830bee4d557d9dd7df312ab134562b3b9bc8bfc1d9cbac2','source_provenance':'SOURCE_DOCUMENT_READ; controlled assay NOT LIVE','files':{p.name:{'size':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in files}}
manifest=D/'manifest_R24_SHA256.json';manifest.write_text(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in files+[manifest]:z.write(p,arcname=D.name+'/'+p.name)
with zipfile.ZipFile(OUT) as z:assert z.testzip() is None
print(json.dumps({'package':str(OUT),'sha256':sha(OUT.read_bytes()),'entries':len(files)+1,'manifest_items':len(files)},indent=2))
