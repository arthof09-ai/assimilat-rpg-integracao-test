"""Package immutable prior R101 and original definitions; manifest+CRC, cold test no replays."""
import hashlib,zipfile,json,pathlib,shutil,io,tempfile,subprocess,sys
R=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path('/mnt/data/VLAB_R102_R107_AUDITORIA_17_CONTRATOS_CIENCIA_MESTRE_ONLY.zip')
assert R.exists()
OLD=pathlib.Path('/mnt/data/VLAB_R92_R101_POTENCIA_EQUIVALENTE_2X1_MESTRE_ONLY.zip')
assert OLD.is_file() and hashlib.sha256(OLD.read_bytes()).hexdigest()=='582bc31c08787a8528b7c35fa3c68c202aeaa4f2198a2995bed00a72a6f3b66b'
refs={
 'historical_archive/VLAB_R92_R101_POTENCIA_EQUIVALENTE_2X1_MESTRE_ONLY.zip':OLD,
 'historical_requirements/VLAB_R17_MATRIX_17_MASTER_ONLY.json':R.parent/'r61_extracted/work/reconstruction/r17_delivery/VLAB_R17_MATRIX_17_MASTER_ONLY.json',
 'historical_requirements/VLAB_R18_MATRIX_17_MASTER_ONLY.json':R.parent/'r61_extracted/work/reconstruction/r18_delivery/VLAB_R18_MATRIX_17_MASTER_ONLY.json',
 'historical_requirements/R60_17_CONTRACTS_CROSSWALK.json':R.parent/'r61_extracted/evidence/R60_17_CONTRACTS_CROSSWALK.json',
 'historical_requirements/R70_CROSSWALK_17.json':R.parent/'r71_extracted/R70_CROSSWALK_17.json',
 'historical_requirements/vlab_effects_v08.py':R.parent/'r61_extracted/work/working/historical_v081_verified_original/comestre_vlab/vlab_effects_v08.py',
}
for f in refs.values(): assert f.is_file(), str(f)
# keep all new stage files except this packaging script (which is included as provenance itself).
files={}
for f in R.rglob('*'):
 if f.is_file() and '__pycache__' not in str(f): files['r102_r107/'+str(f.relative_to(R))]=f
files.update(refs)
assert len(files)==len(set(files))
hashes={k:dict(sha256=hashlib.sha256(f.read_bytes()).hexdigest(),size=f.stat().st_size) for k,f in sorted(files.items())}
manifest=dict(operation='OP-VLAB-FUSION-SANDBOX-01',scope='MESTRE-SIDE; R102-R107 additive',
              base_original_sha256=hashlib.sha256(OLD.read_bytes()).hexdigest(),
              files=hashes,terminal_certified=0,canonical_cells_promoted=0, historical_zip_unchanged=True)
M=json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for arc,f in sorted(files.items()): z.write(f,arc)
 z.writestr('MANIFEST_SHA256.json',M)
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 nam=z.namelist(); assert len(nam)==len(files)+1
 parsed=json.loads(z.read('MANIFEST_SHA256.json'))
 for arc,d in parsed['files'].items():
  data=z.read(arc)
  assert hashlib.sha256(data).hexdigest()==d['sha256'] and len(data)==d['size']
 assert hashlib.sha256(z.read('historical_archive/VLAB_R92_R101_POTENCIA_EQUIVALENTE_2X1_MESTRE_ONLY.zip')).hexdigest()==manifest['base_original_sha256']
print(json.dumps({'file':str(OUT),'bytes':OUT.stat().st_size,'entries':len(files)+1,'hashed_files':len(files),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},ensure_ascii=False))
