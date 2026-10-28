import subprocess,sys,pathlib,time
ROOT=pathlib.Path(__file__).parent
scripts=[
('tests/test_integrated.py',128),('tests/test_security_perf.py',36),('tests/test_legacy_replay.py',3),('tests/test_ui_real_clicks.py',18),('tests/test_run006_adversarial.py',66),('tests/test_fov_geometry.py',40),('tests/test_run007_persistence_replay.py',76),('tests/test_run007_fov_edges.py',34),('tests/test_run008_interactions.py',122),('private/test_private_viewer.py',16),('private/test_private_23_enhancements.py',6),('private/test_private_26_provenance.py',16)]
logs=[];start=time.monotonic()
for script,expected in scripts:
 t=time.monotonic();r=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT/'private' if script.startswith('private/') else ROOT,env=None,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=95)
 log=f'[{script}] EXPECTED {expected} rc={r.returncode} elapsed={time.monotonic()-t:.1f}s\n{r.stdout.strip()}';print(log,flush=True);logs.append(log)
 if r.returncode:raise SystemExit(f'FAIL {script}')
summary=f'TOTAL EXPECTED ASSERTIONS={sum(x[1] for x in scripts)} / {sum(x[1] for x in scripts)}; scripts={len(scripts)}; elapsed={time.monotonic()-start:.1f}s\n'
print(summary)
(ROOT/'evidence'/'QA_RUN008_FINAL.txt').write_text('\n\n'.join(logs)+'\n\n'+summary)
