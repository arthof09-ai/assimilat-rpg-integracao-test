"""Lacra somente arquivos permitidos; nenhuma dependência externa."""
from pathlib import Path
import hashlib,json,zipfile
HERE=Path(__file__).resolve().parent
NAME='PA_10_RODADAS_R05_CATALOGO_REAL_USO_CRAFT_MESTRE_ONLY_TEST_20261024.zip'
files=['SOURCE_R04_FROZEN.zip','R03_DEPENDENCIES/R02_GATE_ENTRADA_TEST.py',
       'R03_DEPENDENCIES/R03_CONSUMIDOR_READONLY_TEST.py',
       'build_fixtures_r05.py','R05_FONTES_TRANSCRITAS_READONLY.json',
       'R05_CONSULTA_CATALOGO_READONLY.py','R05_RESULTS_REPRODUCIBLE.json',
       'test_r05_catalog.py','R05_TEST_RUN.log',
       'R05_FIRST_TEST_FAIL_AUDIT.md','R05_REPLAY_COLD.py',
       'R05_RELATORIO_CATALOGO_MESTRE_ONLY.md',
       'GUIA_PA_CRAFT_CONVERSACIONAL_MESTRE_ONLY.md','README_R05.md',
       'R05_CHECKPOINT_SUCESSAO.md','R05_BUILD_PACKAGE.py']
assert len(files)==len(set(files))
manifest={'artifact':'PA_R05_MASTER_ONLY_TEST','source_R04_sha256':'927f3483a4603d9aeae4c17a92772c70bc5936f70908739a61a784d4c03323aa',
          'time_scope':'2026-10-24','sha256_method':'sha256 original bytes of each included file','files':{}}
for file in files:
 p=HERE/file;assert p.is_file() and not p.is_symlink(),file
 raw=p.read_bytes();manifest['files'][file]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
with zipfile.ZipFile(HERE/NAME,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for file in ['MANIFEST_SHA256.json']+files:
  inf=zipfile.ZipInfo(filename=file,date_time=(2026,10,24,0,0,0))
  inf.compress_type=zipfile.ZIP_DEFLATED
  inf.external_attr=(0o644<<16)
  z.writestr(inf,(HERE/file).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=7)
p=HERE/NAME
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 assert set(z.namelist())==set(files)|{'MANIFEST_SHA256.json'}
 for fname,meta in manifest['files'].items():
  b=z.read(fname)
  assert hashlib.sha256(b).hexdigest()==meta['sha256']
print(json.dumps({'zip':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entries':len(files)+1,'manifest_verified':len(files)},indent=2))
