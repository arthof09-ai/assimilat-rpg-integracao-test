from pathlib import Path
import subprocess,sys,os
root=Path(__file__).resolve().parents[1]
cases=['test_integrated.py','test_security_perf.py','test_legacy_replay.py','test_ui_real_clicks.py','test_run006_adversarial.py','test_fov_geometry.py','test_run007_persistence_replay.py','test_run007_fov_edges.py','test_run008_interactions.py','test_run009_concurrency_markers.py','test_run009_backup_perf.py','test_run009_seeded_mutations.py']
for c in cases:
 print('>>>',c,flush=True)
 ret=subprocess.run([sys.executable,str(root/'tests'/c)],cwd=root)
 if ret.returncode:sys.exit(ret.returncode)
print('>>> projection')
ret=subprocess.run(['node',str(root/'tests'/'test_synthetic_projection.js')],cwd=root)
sys.exit(ret.returncode)
