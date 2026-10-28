"""One-shot package freeze of R118-R125, without invoking experiment runners or modifying historical state."""
from pathlib import Path
import json,zipfile,hashlib,os
OUT=Path('/mnt/data/VLAB_R118_R125_REACOES_SCHEDULER_ESCALA_MESTRE_ONLY.zip')
ROOT=Path('/mnt/data/vlab_succession')
CURRENT=ROOT/'r118_r125'
STAGE=ROOT/'r61_extracted/work/fusion_stage12'
HIST=Path('/mnt/data/VLAB_R108_R117_NATIVE_CRITICO_FRACO_DESCARGA_MESTRE_ONLY.zip')
assert HIST.is_file() and HIST.stat().st_size==11173790
sha=lambda b: hashlib.sha256(b).hexdigest()
assert sha(HIST.read_bytes())=='e57461df692818db820cf96a825a36d1ee4b5c11b19afaae1c835716c06ed2a8'
assert not OUT.exists(), 'NO_OVERWRITE_EXISTING_FREEZE'
files={}
for root,prefix in [(CURRENT,'r118_r125'),(STAGE,'r61_extracted/work/fusion_stage12')]:
 for p in root.rglob('*'):
  if not p.is_file() or '__pycache__' in p.parts or p.name.endswith(('.pyc','-wal','-shm')):continue
  files[prefix+'/'+p.relative_to(root).as_posix()]=p
files['historical_original_R117.zip']=HIST
assert len(files)==len(set(files)) and len(files)>140,len(files)
manifest={arc:{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for arc,p in sorted(files.items())}
with zipfile.ZipFile(OUT,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for arc,p in sorted(files.items()):z.write(p,arc)
 z.writestr('SHA256_FILE_MANIFEST_R125.json',json.dumps({'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R118–R125','baseline':'R01–R117 IMMUTABLE','manifest':manifest,'source_R117_sha256':manifest['historical_original_R117.zip']['sha256'],'contract_terminal':0,'no_notional_writer':True},indent=2,ensure_ascii=False)+'\n')
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 entries=z.namelist();assert len(entries)==len(files)+1 and len(set(entries))==len(entries)
 data=json.loads(z.read('SHA256_FILE_MANIFEST_R125.json'));assert len(data['manifest'])==len(files)
 for arc,expected in data['manifest'].items():
  blob=z.read(arc);assert sha(blob)==expected['sha256'] and len(blob)==expected['bytes'],arc
R={'status':'PASS','zip':str(OUT),'size_bytes':OUT.stat().st_size,'sha256':sha(OUT.read_bytes()),'members':len(entries),'manifest_verified_files':len(files),'crc':'PASS','manifest_file':'SHA256_FILE_MANIFEST_R125.json','historical_R117_sha256':manifest['historical_original_R117.zip']['sha256'],'reader_note':'Archive fresh creation; no runner invoked or historical DB overwritten','terminal_17':0}
Path('/mnt/data/vlab_succession/R125_ZIP_FREEZE_RECEIPT.json').write_text(json.dumps(R,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(R,indent=2,ensure_ascii=False))
