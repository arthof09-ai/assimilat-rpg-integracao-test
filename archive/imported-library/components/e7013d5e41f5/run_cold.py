from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((R/'MANIFEST_SHA256.json').read_text())
for rel,x in d['files'].items():
 p=R/rel
 if not p.exists() or h(p)!=x:raise ValueError('SHA incorrect: '+rel)
with tempfile.TemporaryDirectory() as tmp:
 x=Path(tmp)/'copy';shutil.copytree(R,x)
 expected=h(x/'outputs'/'comparators_audit.json')
 p=subprocess.run([sys.executable,str(x/'src'/'audit.py')],capture_output=True,text=True,check=True)
 t=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(x/'tests'),'-q'],capture_output=True,text=True,check=True)
 if h(x/'outputs'/'comparators_audit.json')!=expected:raise ValueError('non deterministic output')
 print(p.stdout.strip(),t.stderr.strip(),'no writes to Notion/Party')
