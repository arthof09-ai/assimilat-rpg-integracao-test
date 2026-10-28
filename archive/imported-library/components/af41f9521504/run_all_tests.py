from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[1]
for script in ['test_integrated.py','test_security_perf.py','test_legacy_replay.py','test_ui_real_clicks.py','test_run006_adversarial.py','test_fov_geometry.py','test_run007_persistence_replay.py','test_run007_fov_edges.py','test_run008_interactions.py','test_run009_concurrency_markers.py','test_run009_backup_perf.py','test_run009_seeded_mutations.py','test_phase2_coordinate_redo_ruler.py','test_phase2_seeded_coordinates.py','test_phase2_mutations.py']:
 print('>>>',script,flush=True)
 if subprocess.run([sys.executable,str(r/'tests'/script)],cwd=r).returncode:sys.exit(1)
print('>>> synthetic projection')
sys.exit(subprocess.run(['node',str(r/'tests'/'test_synthetic_projection.js')],cwd=r).returncode)
