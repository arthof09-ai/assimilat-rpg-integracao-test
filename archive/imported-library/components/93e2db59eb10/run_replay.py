from pathlib import Path
import sys,subprocess,json
root=Path(__file__).resolve().parents[1]
def execute(argv):
 p=subprocess.run([sys.executable,*argv],cwd=root,capture_output=True,text=True,timeout=30)
 assert p.returncode==0,p.stderr[-1500:]
 return p.stdout+p.stderr
assert 'MANIFEST PASS' in execute(['code/verify_manifest.py'])
assert 'Ran 46 tests' in execute(['-m','unittest','discover','-s','tests','-p','test_*.py'])
sys.path.insert(0,str(root/'code'))
import enc9_dependency as q
assert q.corpus_report()==json.loads((root/'outputs/enc9_report.json').read_text())
assert q.stress(12)==json.loads((root/'outputs/synthetic_stress.json').read_text())
r=q.corpus_report();assert r['official_enc_corpus_denominator']==9 and r['oil_dependency_count']==8 and r['oil_requirements_for_selected_cases']==8
assert r['real_magic_acts']==0 and r['r48_orders_created']==0
print('REPLAY PASS ENC9/9 8 OIL DEPENDENT / 46 TESTS / 1728 SYNTHETIC / NO PROD')
