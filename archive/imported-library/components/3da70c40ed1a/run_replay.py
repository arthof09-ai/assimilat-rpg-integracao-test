import subprocess,sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=root,capture_output=True,text=True)
assert p.returncode==0,(p.stdout,p.stderr)
p=subprocess.run([sys.executable,'-B','code/integrated_gate.py'],cwd=root,capture_output=True,text=True)
assert p.returncode==0,p.stderr
assert json.loads(p.stdout)==json.loads((root/'outputs'/'READONLY_RESULT.json').read_text())
p=subprocess.run([sys.executable,'-B','code/verify_manifest.py'],cwd=root,capture_output=True,text=True)
assert p.returncode==0,p.stderr
print('PASS_H23_VARIANT_INTEGRATION_COLD_REPLAY',p.stdout.strip(),'HOLD_NO_APPLICATION_NO_PARTY_NO_MAGIC')
