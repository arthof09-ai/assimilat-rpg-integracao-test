from pathlib import Path
import json,collections
P=Path(__file__).resolve().parent
r=json.load(open(str(P/'BASELINE_PA_R03/corpus_pa_v3.json')))['items']
classified=[]
for x in r:
 cohort=x['cohort'];id=x['item_id']
 if cohort=='MAPA_T01_54':
  surf='CATALOGO_MESTRE_INDEXADO';basis='MAPA T-01 oficial RPG / Itens; não readback individual neste turno R04'
 elif cohort=='INDEX_INSCRIPTIONS_MATRICES_34':
  surf='CATALOGO_MESTRE_INDEXADO';basis='índices inscrições/matrizes em RPG / Itens, documentos-fonte com campos incompletos'
 elif cohort=='EXTRA_THREE_AND_UPGRADE_TEN':
  surf='PARTY_MESTRE_ESPELHO';basis='index Aprimoramentos e fichas de personagens Party (Mestre — Espelho); path de amostras confirmados no conector'
 elif cohort=='EXTRA_COMPARADORES_7':
  if id in ['3f5c2b324ede81eaa080cad94c16dd3b','3f5c2b324ede818296fbd64921861d83']:
   surf='MESTRE_SEMICANONICO_INCUBACAO';basis='Path Mestre incubação, PROPOSTO; não item canônico publicado'
  else:
   surf='PARTY_MESTRE_ESPELHO';basis='path conector Party Mestre Espelho ou ficha com mesmo ancestral; proibido tratar como observação Mestre autônoma'
 else:surf='INDETERMINADO';basis='coorte desconhecida'
 classified.append({'uuid':id,'title':x['name'],'cohort':cohort,'surface':surf,'basis':basis,'pa_daily':x['pa_daily']['value'],'classification':x['pa_daily']['classification'],'lineage':x['lineage_cluster']})
group={}
for z in classified:
 g=group.setdefault(z['surface'],{'pages':0,'known_daily':0,'explicit_daily':0,'R_PA_DIA':0,'related_clusters':set()})
 g['pages']+=1;g['known_daily']+=z['pa_daily'] is not None
 g['explicit_daily']+=z['classification']=='EXPLICITA';g['R_PA_DIA']+=z['classification']=='REGRA_R_PA_DIA'
 g['related_clusters'].add(z['lineage'])
for g in group.values():g['provisional_clusters']=len(g.pop('related_clusters'))
out={'total_r03_pages':len(classified),'all_uuids_unique':len({z['uuid'] for z in classified})==len(classified),
'groups':group,'daily_master_catalog_known':group['CATALOGO_MESTRE_INDEXADO']['known_daily'],
'competing_authority':'Item em espelho Party não é equiparado automaticamente ao catálogo Mestre; manter dados read-only rotulados como comparador; não misturar holdout por linhagem.',
'physical_scope_limit':'classificação de 88 itens vem de origem/índice e evidência R03; nem os 88 foram reabertos individualmente neste turno.',
'rows':classified}
(P/'CORPUS_ORIGEM_AUDITADA_R04.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n','utf8')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2,ensure_ascii=False))
