"""Verifica CRC, manifesto SHA e contagem de artefatos TEST05 (não altera o ZIP)."""
import sys,hashlib,json,zipfile
from pathlib import Path
name=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent/'PACOTE_TABLETOP_ASSIMILACAO_TEST05_2026-10-22.zip'
with zipfile.ZipFile(name) as z:
 assert z.testzip() is None,'CRC FAIL'
 files=set(z.namelist()); manifest=json.loads(z.read('MANIFESTO_SHA256_TEST05.json'))
 assert len(files)==len(manifest['sha256'])+1,'arquivo sem manifesto ou ausente'
 for path,h in manifest['sha256'].items():
  assert hashlib.sha256(z.read(path)).hexdigest()==h,'SHA FAIL: '+path
 print('PASS ZIP',len(files),'entries; manifest',len(manifest['sha256']),'SHA256')
