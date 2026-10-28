#!/usr/bin/env python3
"""C28 scientific portable replay. No Notion/VLAB writes and no combat runners.
Run after extracting the C28 ZIP: python C28_PORTABLE_REPLAY.py.
It checks the manifest of supplied artifacts, re-generates 21 derived files in an
isolated temporary folder, and checks equality to source-bound bundle output.
The three VLAB R205 externally-derived files are hash-audited from ZIP but NOT
re-fetched/re-played without the separate original VLAB archive.
"""
import csv,json,hashlib,sys,subprocess,shutil,tempfile,zipfile
from pathlib import Path
R=Path(__file__).resolve().parent
MAN=json.loads((R/'C28_SHA256_MANIFEST.json').read_text())
def dig(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for entry in MAN['files']:
 p=R/entry['relative_path']
 assert p.is_file(),p
 assert p.stat().st_size==entry['bytes']
 assert dig(p)==entry['sha256'],p
scripts=['build_c28.py','independent_math_c28.py','c28_delivery_stress.py','forensic_slash_c28.py','prepare_report_c28.py']
external={
'publication/C28_VLAB_R205_RING_READONLY_OBSERVATIONS_8.csv',
'publication/C28_VLAB_R205_PAIRED_OUTCOME_4_SEEDS.csv',
'publication/C28_VLAB_R205_READONLY_AUDIT.json'}
with tempfile.TemporaryDirectory(prefix='dmgrank_c28_clean_') as td:
 T=Path(td)
 for folder in ['baseline','work','publication']:
  shutil.copytree(R/folder,T/folder)
 for script in scripts:
  p=subprocess.run([sys.executable,str(T/'work'/script)],cwd=T,text=True,capture_output=True,timeout=240,check=False)
  if p.returncode: raise AssertionError('Script failed: '+script+'\n'+p.stdout+'\n'+p.stderr)
 regenerated=0;external_only=0
 for entry in MAN['files']:
  rel=entry['relative_path']
  if not rel.startswith('publication/'):continue
  if rel in external:external_only+=1;continue
  if dig(T/rel)!=entry['sha256']:raise AssertionError('cold reproduction mismatch: '+rel)
  regenerated+=1
 assert external_only==3
 print(json.dumps({'status':'PASS','manifest_bytes_verified':len(MAN['files']), 'regenerated_publication_identical':regenerated, 'external_VLAB_source_bound_not_independently_regenerated':external_only, 'combat_runners_called':0,'writes_to_Notion':0,'global_NAC_PASS':'HOLD'},ensure_ascii=False))
