import json
from pathlib import Path

def route(error, *, explicit=True, authenticated=False, target_read=False, writer=False, independent=True, identical_retry=False):
    # Synthetic policy decision harness; intentionally cannot access Notion or modify data.
    if error == 'NONE':
        return 'OPERACIONAL' if explicit and authenticated and target_read else 'INDETERMINADA'
    if error == 'LINK_REQUIRED' and not explicit: return 'CORRIGIR_LINK_ID'
    if error == 'WRONG_LINK': return 'REDESCOBRIR_VINCULO'
    if error == 'NOT_FOUND': return 'DIAGNOSTICAR_DESTINO' if authenticated else 'INVESTIGAR_VINCULO_E_AUTENTICACAO'
    if error == 'WRITE_REQUEST': return 'PERMITIR_MEDIANTE_GATE' if (explicit and authenticated and target_read and writer) else 'NEGAR_ESCRITA'
    if error == 'WRITE_TIMEOUT': return 'READBACK_ANTES_DE_RETRY'
    if error == 'REVOKED': return 'PARAR_SEM_CONTORNO'
    if error == 'TOOL_UNAVAILABLE': return 'CONTINUAR_TEST_SE_AUTORIZADO' if independent else 'BLOQUEADA_OU_INDETERMINADA'
    if error == 'ACCOUNT_CHANGED': return 'INVALIDAR_PREFLIGHT'
    if error == 'NEW_SESSION': return 'REFACER_PREFLIGHT'
    if error == 'REPEATED_ERROR' and identical_retry: return 'PROIBIR_REPETICAO_IDENTICA'
    return 'INVESTIGAR_CAMADA'

cases=[
 ('T01_MULTICONTAS','LINK_REQUIRED',{'explicit':False},'CORRIGIR_LINK_ID'),
 ('T02_OMISSAO_LINK','LINK_REQUIRED',{'explicit':False},'CORRIGIR_LINK_ID'),
 ('T03_LINK_INCORRETO','WRONG_LINK',{},'REDESCOBRIR_VINCULO'),
 ('T04_AUTH_LEITURA_OK','NONE',{'authenticated':True,'target_read':True},'OPERACIONAL'),
 ('T05_NOT_FOUND_AUTENTICADO','NOT_FOUND',{'authenticated':True},'DIAGNOSTICAR_DESTINO'),
 ('T06_MESTRE_PARA_PARTY','NOT_FOUND',{'authenticated':True},'DIAGNOSTICAR_DESTINO'),
 ('T07_PARTY_PARA_MESTRE','NOT_FOUND',{'authenticated':True},'DIAGNOSTICAR_DESTINO'),
 ('T08_FERRAMENTA_INDISPONIVEL','TOOL_UNAVAILABLE',{'independent':False},'BLOQUEADA_OU_INDETERMINADA'),
 ('T09_REVOGACAO','REVOKED',{},'PARAR_SEM_CONTORNO'),
 ('T10_ESCRITA_SEM_WRITER','WRITE_REQUEST',{'authenticated':True,'target_read':True,'writer':False},'NEGAR_ESCRITA'),
 ('T11_TIMEOUT_DE_ESCRITA','WRITE_TIMEOUT',{},'READBACK_ANTES_DE_RETRY'),
 ('T12_MUDANCA_CONTA','ACCOUNT_CHANGED',{},'INVALIDAR_PREFLIGHT'),
 ('T13_SUCESSOR_SEM_CONTEXTO','NEW_SESSION',{},'REFACER_PREFLIGHT'),
 ('T14_TEST_INDEPENDENTE','TOOL_UNAVAILABLE',{'independent':True},'CONTINUAR_TEST_SE_AUTORIZADO'),
 ('T15_RETRY_IDENTICO','REPEATED_ERROR',{'identical_retry':True},'PROIBIR_REPETICAO_IDENTICA'),
 ('T16_ALVO_NAO_LIDO','NONE',{'authenticated':True,'target_read':False},'INDETERMINADA'),
]
rows=[]
for ident,err,kw,expect in cases:
    got=route(err,**kw)
    rows.append({'id':ident,'expected':expect,'observed':got,'pass':got==expect,'method':'MODELO_SIMULADO'})
assert all(row['pass'] for row in rows)
path=Path('/mnt/data/auth_notion_01/AUTH_NOTION_01_STRESS_MODEL_20261022.json')
path.write_text(json.dumps({'scope':'MODELO DE DECISAO SIMULADO. NAO PROVA RUNTIME REAL NEM NAC-PASS S4.','total':len(rows),'passed':len(rows),'cases':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(rows)}/{len(rows)} cenarios de decisao simulados PASS; path={path}')