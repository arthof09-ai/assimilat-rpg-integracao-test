#!/usr/bin/env python3
"""Reprodução da matriz de triagem: IDs pré-registrados antes do fetch, classificação da trilha física lida pelo conector.
Captura manual de metadados Notion, não conexão embutida Python/assinatura.
"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent.parent
pre=json.loads((P/'R05_HOLDOUT_PREREG.json').read_text('utf8'))
tech=json.loads((P/'R05_ESCOPOS_MASTER_OUTSIDE_88_PREREG.json').read_text('utf8'))
consum=json.loads((P/'R05_COHORT_CONSUMIVEIS_PRE_REGISTRO.json').read_text('utf8'))
inc={'3f5c2b324ede815181a0e88dd51bd4eb','3f5c2b324ede81bab332f518b2e6a211'}
parties={
'e25c2b324ede82bdb9c1014d4ffc5e76':13,'92bc2b324ede83be863b01a5d6aba48b':8,
'9b7c2b324ede83f4af7e01c90cb6efaf':6,'064c2b324ede8304b2d301e0835cc0c4':8,
'05dc2b324ede8272a0b58113edf5466e':15,'933c2b324ede82d8916481c591f5b842':16,
'2d5c2b324ede8276a13a01d7a4525c74':36,'591c2b324ede838691148122c83c19d5':34,
'ba0c2b324ede834c920d01390e3aac12':12,'426c2b324ede833a89ba81706507f192':8,
'761c2b324ede8201be5081ea69e97f10':10
}
# Essas quantias do Espelho são somente metadados qualitativos: não calibram Mestre.
mirrors=[];incub=[]
for x in pre['candidates']:
 id=x['uuid'];d={'uuid':id,'url':'https://app.notion.com/p/'+id,'name':x['name'],'source_read':'NOTION_MESTRE_READ_ONLY',
 'source_type':'ESPELHO_PARTY' if id not in inc else 'MESTRE_SEMICANONICO',
 'path':'RPG / Party (Mestre — Espelho)' if id not in inc else 'RPG / Itens / Incubação',
 'daily_pa_text_observed_noncalibration':parties.get(id),
 'energy_independent_MASTER_official':False,'notion_sha_signed':False,
 'pa_day_status':'NUMERIC_EXPLICIT_READBACK' if id in parties else 'NAO_REVALIDADO_COMO_CUSTO_DIARIO',
 'experimental_status':'PA_FROM_MIRROR_NOT_MASTER' if id not in inc else 'NO_CALIBRATION_IN_SEMICANON'}
 (incub if id in inc else mirrors).append(d)
records=[{'uuid':u,'url':'https://app.notion.com/p/'+u,'index_url':'https://app.notion.com/p/'+tech['index'],
 'source_path':'RPG / Itens / Técnicas & Pergaminhos','source_domain':'MESTRE_CATALOGO_INDICE','modality':'TECNICA_PERGAMINHO_NAO_EQUIPAMENTO',
 'readback':'FICHA_TEXTO_COM_IMAGEM_DE_MECANICA','pa_numeric_readable':None,'pa_status':'AUSENTE_NO_TEXTO_RECUPERADO',
 'possible_PA_in_unread_image':'NAO_INFERIR','independent_energy_observation':False} for u in tech['uuid']]
consumables=[]
for family,uuids in [('PÍLULAS',consum['pills']),('POÇÕES',consum['potions'])]:
 for u in uuids:
  consumables.append({'uuid':u,'url':'https://app.notion.com/p/'+u,
    'source_path':'RPG / Itens / '+family,'source_domain':'MESTRE_CATALOGO_CONSUMIVEL',
    'modality':'CONSUMIVEL_NAO_EQUIPAMENTO_DIARIO','pa_numeric_readable':None,
    'pa_status':'AUSENTE_NO_TEXTO_RECUPERADO','independent_energy_observation':False})
allrecords=mirrors+incub+records+consumables
out={'as_of':'2026-10-17','source':'Notion Mestre readback nesta sessão e transcrição manual','baseline_count':108,
 'new_physical_uuids':len(allrecords),'total_physical_uuids_examined_in_baseline_plus_expansion':108+len(allrecords),
 'source_denom':{'new_master_catalog_technique_pages':len(records),'new_master_catalog_consumable_pages':len(consumables),'new_master_catalog_pa_numeric_readable':0,
 'new_master_equip_pa_numeric_independent':0,'new_party_mirror_uuids':len(mirrors),'new_semicanonic_uuids':len(incub)},
 'master_numeric_historic_baseline_14_unchanged':True,
 'notion_readback_limit':'Os dados recuperados são conteúdo textual da ferramenta. Muitos efeitos estão somente em imagem, sem leitura mecânica verificável; não aplicar OCR automático.',
 'independence':'UUID distintas, mas nenhuma fonte Mestre nova com PARÂMETRO PA numérico; amostragem textual limitada, não esgotamento global',
 'new_records':allrecords,'no_writes':True,'no_recipe':True}
(P/'RESULTADOS'/'CORPUS_EXPANSAO_R05.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n','utf8')
print(json.dumps(out['source_denom'],ensure_ascii=False))
