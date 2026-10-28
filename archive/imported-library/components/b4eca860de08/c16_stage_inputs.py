#!/usr/bin/env python3
"""Stage READ-ONLY C15 and R205 evidence, checking original archive hashes, no VLAB runner."""
import pathlib,zipfile,hashlib,json,sys,os
W=pathlib.Path(__file__).resolve().parent
root=pathlib.Path(os.environ.get('DMG_C16_INPUT_DIR',str(W.parent/'dmg_c16_inputs')))
files=[('DMG_C15_PRECISAO_SEEDS_CORPUS_20261020_MESTRE_ONLY.zip','1f5d0c16a3a56a978acfc286c1b52886c109786515a06a160096fbf7c21201d5'),('VLAB_R205_DEFESA_DE_VENTO_ANEL_CLASSIFICADO_MESTRE_ONLY.zip','62a9851b3a5ae7919b9225d9379a3d32c8736448e76bfcea4729dcbfe933cead')]
report=[]
for name,expected in files:
 p=root/name
 if not p.is_file():raise FileNotFoundError(f'External archive required at: {p}')
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 assert digest==expected,(name,digest,expected)
 z=zipfile.ZipFile(p);assert z.testzip() is None
 if name.startswith('DMG_C15'):
  manifest=json.loads(z.read('C15_SHA256_MANIFEST.json'))
  for obj in manifest['members']:
   assert hashlib.sha256(z.read(obj['name'])).hexdigest()==obj['sha256']
  names=['C15_R204_SEED_CLUSTER_SUMMARY.csv']
  dest=W/'baseline_c15'
  for fname in names:
   out=dest/fname;out.parent.mkdir(exist_ok=True,parents=True);out.write_bytes(z.read(fname))
  report.append(dict(archive=name,sha256=digest,manifest_verified=len(manifest['members'])))
 else:
  manifest=json.loads(z.read('MANIFEST_SHA256.json'))
  for fname,h in manifest['files'].items():assert hashlib.sha256(z.read(fname)).hexdigest()==h,(fname,h)
  names=[x for x in z.namelist() if x.startswith('new/r205/evidence/db/') and x.endswith('.sqlite')]+['new/r205/evidence/R205_WIND_LIVE_FIGHTS.json','new/r205/evidence/R205_RING_LIVE_FIGHTS.json']
  dest=W/'src_r205'
  for fname in names:
   out=dest/fname;out.parent.mkdir(exist_ok=True,parents=True);out.write_bytes(z.read(fname))
  report.append(dict(archive=name,sha256=digest,manifest_verified=len(manifest['files']),sqlite_readonly_staged=sum(x.endswith('.sqlite') for x in names)))
print(json.dumps(report,indent=2))
