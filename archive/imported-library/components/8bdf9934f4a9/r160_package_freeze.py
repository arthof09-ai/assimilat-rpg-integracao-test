from pathlib import Path
import zipfile,hashlib,json,os,shutil
ROOT=Path('/mnt/data/vlab_succession');R=ROOT/'r151_r160';old=Path('/mnt/data/VLAB_R146_R150_SPATIAL_CORRECTION_MULTIRROUND_MESTRE_ONLY.zip');out=Path('/mnt/data/VLAB_R151_R160_TACTICAL_R42_R43_CASULO_ED_BE_MESTRE_ONLY.zip')
assert old.is_file()
assert hashlib.sha256(old.read_bytes()).hexdigest()=='911bff3503c734173b8173222faca0fc8f5a592b649f30a640e4dfe2d08e0c1e'
files=[(old,old.name)]
for p in sorted(R.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p.suffix in ('.pyc',) or '.sqlite-' in p.name:continue
 files.append((p,'r151_r160/'+str(p.relative_to(R))))
# Only source-controlled historical Stage12 dependency (no pycache, no generated db) to reproduce R18 and R26.
S=ROOT/'r61_extracted/work/fusion_stage12'
for p in sorted(S.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p.suffix not in ('.py','.json','.md','.txt','.toml','.yaml','.yml'):continue
 files.append((p,'r61_extracted/work/fusion_stage12/'+str(p.relative_to(S))))
# The actual native v0.8.1 sources used from R150 and controlled copy included; previous original nested R150 ZIP.
seen=set();manifest=[]
for p,arc in files:
 assert arc not in seen,arc;seen.add(arc)
 b=p.read_bytes();manifest.append({'path':arc,'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
write={'operation':'OP-VLAB-FUSION-SANDBOX-01','environment':'MESTRE-SIDE','freeze':'R160','original_R150_zip_sha256':'911bff3503c734173b8173222faca0fc8f5a592b649f30a640e4dfe2d08e0c1e','files':manifest,'manifest_entry_count':len(manifest),'authority':'NO_CANON_NOTION_WRITE; NO_WRITER','official_terminal':0,'no_repeat':True,'source_notes':'All adapters technical LAB-only; not rules canonized; R156 pending retained; R159 odd-half stopped.'}
manifest_name='R160_SHA256_MANIFEST.json';readme='''# VLAB R151–R160 | RESTAURAÇÃO SEGURA / MESTRE-ONLY\n\nZIP R150 aninhado intacto; código adicional sob `r151_r160/`, Stage12 R18/R26 sob `r61_extracted/work/fusion_stage12/`. Não escrever no Notion/Party/DMG.\n\n**Primeira ação**: verificar `R160_SHA256_MANIFEST.json` e todos os checksums. **Não executar** os scripts `r151_tactical_native.py`, `r153_casulo_fixture.py`, `r154_concurrent_aoo.py`, `r159_ed_besta_compare.py`, `r159_ed_besta_native.py` em bancos existentes. Intenções R156 UNKNOWN_EFFECT e R159 S998801 odd-half devem ficar intocadas.\n\nAuditores somente-leitura (os scripts stdlib independentes não importam resolvedor):\n- `python r151_r160/r159_cold_tactical_auditor.py`\n- `python r151_r160/r159_cold_ed_besta_independent.py`\n- `python r151_r160/r159_cold_aoo_casulo.py`\n- `python -m unittest discover -s r151_r160/native_v081_controlled -p test_vlab_effects_v08.py -q` (garantir PYTHONPATH para pasta nativa se exigido)\n\nPara reabrir checkpoints já gravados, importar `vlab_r18_interactive` da pasta Stage12 e chamar SOMENTE `load(db)`; a API de commit não deve ser chamada sobre histórico.\n\nO R42 negativo está disponível apenas com `lab_negative_critical_policy=True`. Fora do escopo LAB continua bloqueando antes do efeito. A meia-dano ímpar não recebeu regra de arredondamento. Fonte de Iniciativa Besta não foi inventada.\n\nLeia `R160_PSV_MESTRE_ONLY.md` e `R160_QUARANTINE_UNKNOWN_EFFECT_NO_REPEAT.json` antes de qualquer sucessão.\n'''
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
 for p,arc in files:z.write(p,arc)
 z.writestr(manifest_name,json.dumps(write,ensure_ascii=False,indent=2)+'\n')
 z.writestr('README_R160_SAFE_RESTORE.md',readme)
with zipfile.ZipFile(out) as z:
 bad=z.testzip();assert bad is None,bad
 m=json.loads(z.read(manifest_name)); assert len(m['files'])==len(manifest)
 for f in m['files']:
  b=z.read(f['path']);assert len(b)==f['size'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
 assert hashlib.sha256(z.read(old.name)).hexdigest()==m['original_R150_zip_sha256']
receipt={'path':str(out),'size_bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'manifest_items_verified':len(manifest),'entries':len(manifest)+2,'crc':'PASS','nested_R150':'SHA256_IDENTICAL','readback':'SAME_CONTAINER_NOT_COLD_YET','source_scripts_included':True,'unmodified_R01_R150':'PRESERVED_BY_NESTED_R150','timestamp_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}
(ROOT/'R160_ZIP_FREEZE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
