from __future__ import annotations
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
R=Path(__file__).resolve().parent
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
manifest=json.loads((R/'MANIFEST_SHA256.json').read_text())
for name,digest in manifest['files'].items():
    p=R/name
    if not p.is_file() or sha(p)!=digest:raise RuntimeError('artifact integrity mismatch: '+name)
with tempfile.TemporaryDirectory(prefix='pa-r49d-readonly-') as d:
    x=Path(d)/'copy'
    shutil.copytree(R,x)
    outputs={n:sha(x/n) for n in manifest['outputs']}
    for name in ['metrics.py','craft_design.py']:
        p=subprocess.run([sys.executable,str(x/'src'/name)],capture_output=True,text=True,check=True)
        print(p.stdout.strip())
    for name,dig in outputs.items():
        if sha(x/name)!=dig:raise RuntimeError('non-deterministic output: '+name)
    q=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(x/'tests'),'-q'],capture_output=True,text=True,check=True)
    print(q.stderr.strip())
print('PASS R49D: manifest, outputs deterministic, cold unit tests; zero canon writes')
