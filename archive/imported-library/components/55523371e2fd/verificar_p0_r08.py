from pathlib import Path
import json,csv,hashlib,collections
D=Path(__file__).resolve().parent
orig=json.loads((D/'ORIGINAIS_CROSSWALK_R08.json').read_text('utf8'))
aud=json.loads((D/'AUDITORIA_94_P0_R08_DERIVADO.json').read_text('utf8'))
axes=json.loads((D/'ATLAS_9x14_EIXOS_R08.json').read_text('utf8'))
ranks=json.loads((D/'ATLAS_9_DISPOSICOES_R08.json').read_text('utf8'))
miss=json.loads((D/'ATLAS_3_SEM_CLASSIFICACAO_R08.json').read_text('utf8'))
patch=json.loads((D/'PATCHES_FICHA_CONTENT_ONLY_NO_WRITE_R08.json').read_text('utf8'))
checks={
 '94_derivados_distintos':len(aud)==94 and len({x['uuid'] for x in aud})==94,
 '14_mestre_80_party':collections.Counter(x['origem'] for x in aud)=={'CATALOGO_MESTRE_INDEXADO':14,'PARTY_MESTRE_ESPELHO':80},
 '80_originais_party_reabertos_vinculados':sum(x['status_original']=='READBACK_ORIGINAL_P0_R08' for x in orig['rows'])==80,
 '80_UUID_originais_unicos':len({x['original_party_uuid'] for x in orig['rows'] if x['original_party_uuid']})==80,
 'atlas9x14':len(ranks)==9 and len(axes)==126 and len({x['uuid'] for x in axes})==9,
 'atlas_nao_promove':all(not x['rank_canonicamente_homologado'] for x in ranks),
 'tres_sem_rank':len(miss)==3 and all(x['rank_final']=='SEM_CLASSIFICACAO_DE_PODER' for x in miss),
 'tres_patches_nao_escritos':len(patch)==3 and all(not x['applied'] and x['sync_status']=='NOT_RUN' for x in patch),
 'nenhuma_claim_writer':all(x['writer_apto'] is False and x['aplicado_notion'] is False for x in aud),
}
if (D/'MANIFEST_SHA256_R08.json').exists():
 m=json.loads((D/'MANIFEST_SHA256_R08.json').read_text('utf8'))
 checks['manifest_arquivos']=all(hashlib.sha256((D/f).read_bytes()).hexdigest()==h for f,h in m['files'].items())
print(json.dumps({'n_checks':len(checks),'checks':checks,'all_pass':all(checks.values()),'scope':'TEST_ONLY_NONCANONICO'},ensure_ascii=False,indent=2))
assert all(checks.values())
