#!/usr/bin/env python3
"""Adapter sidecar tested with real recovered QMC-02 code AND PA R03/R04 code.
QMC-02 original files not modified. No network, Notion-write, or recipes.
Native QMC-02 validate_external_pa() is NOT patched and still rejects unfamiliar replies;
sidecar consumes messages under a new named/validated TEST contract only.
"""
from __future__ import annotations
import sys,hashlib,json,copy
from pathlib import Path
P=Path(__file__).resolve().parent
QMC=P/'BASELINE_QMC02/qmc02'
sys.path.insert(0,str(QMC))
import qmc02
import pa_r04 as pa

CONTRACT='QMC-PA-INTERCHANGE-CANDIDATE-1'
RESPONSE='QMC-PA-RESPONSE-R04-TEST-1'

def _sha(data):return hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def _reject(condition,msg):
 if not condition:raise ValueError(msg)

def emit_historical(qmc_source:dict)->dict:
 """Do QMC qualification and PA engine computation on SAME UUID, compare extracted costs.
 Refuse mismatch; never promote excerpts to cryptographically signed Notion snapshot.
 """
 qualified=qmc02.inspect_source(copy.deepcopy(qmc_source))
 _reject(qualified.get('status')=='QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO','QMC não qualificou fonte')
 req=qualified['energy_interface']
 _reject(req.get('contract')==CONTRACT,'contrato QMC diferente')
 qid=req['ITEM-ID'];paquote=pa.r03.historical(qid)
 _reject(qmc02.norm_id(paquote['id'])==qid,'ID divergente')
 _reject(qmc02.norm_id(paquote['url'])==qid,'URL PA divergente')
 observed_daily=[x['value'] for x in qualified['costs']['daily']]
 pday=paquote['pa_daily']['value']
 conflicts=[]
 if observed_daily:
  if len(set(observed_daily))!=1 or pday!=observed_daily[0]:conflicts.append('PA_DIA_LIDO_QMC_DIVERGE_MOTOR')
 elif pday is not None:conflicts.append('PA_DIA_MOTOR_SEM_CORRESPONDENCIA_NO_EXCERTO_QMC')
 observed_acts=[x['value'] for x in qualified['costs']['activation']]
 expected=[v['value'] for v in paquote['activation_abilities']] if paquote['activation_abilities'] else ([paquote['pa_activation']['value']] if paquote['pa_activation']['value'] is not None else [])
 if sorted(observed_acts)!=sorted(expected):conflicts.append('PA_ATIVO_LIDO_QMC_DIVERGE_MOTOR')
 if conflicts:state='CONFLITO_BLOQUEANTE';pa_daily=None;pa_activation=None
 else:state='DOCUMENTO_HISTORICO_RECONCILIADO_TEST';pa_daily=pday;pa_activation=expected
 body={'contract':RESPONSE,'origin_contract':CONTRACT,'request_uuid':qid,'qmc':{
   'module':qualified['identity']['module'],'family':qualified['identity']['family'],'qual_state':qualified['status'],
   'source_url':qualified['identity']['url'],'readback_excerpt_sha256':qualified['provenance']['content_sha256_excerpt'],
   'observed_at':qualified['provenance']['observed_at'],'extraction_scope':qualified['provenance']['excerpt_scope'],
   'qmc_effect_count':len(qualified['effects'])},'pa_engine':{'version':'PA-R04-WRAPPER-R03-v3',
   'source_url':paquote['url'],'source_mode':'HISTORICO','daily_value':pa_daily,'daily_unit':'PA/dia',
   'activation_values':pa_activation,'activation_unit':'PA/uso','daily_semantics':'UNKNOWN_COMMIT_VS_DEBIT',
   'pa_historical_classification':paquote['pa_daily']['classification']},
   'state':state,'conflicts':conflicts,'independent_cost_model_validated':False,'authentic_notionsignature':False,
   'master_only':True,'production_hold':True,'new_recipe_permitted':False,'approval_state':'TEST_NO_RELEASE'}
 return {'message':body,'digest_sha256':_sha(body)}

def emit_candidate(spec:dict)->dict:
 _reject(spec.get('evidence_type')=='USER_EXPERIMENTAL_SPEC','candidate precisa declarar origem experimental')
 quote=pa.proposal(spec)
 body={'contract':RESPONSE,'origin_contract':CONTRACT,'candidate_id':spec.get('candidate_id','TEST_CANDIDATE'),
  'qmc':{'qual_state':'CANDIDATO_EXPERIMENTAL_SEM_FONTE_NOTION','source_url':None,'qmc_effect_count':None,
  'module':None,'family':None},
  'pa_engine':{'version':'PA-R04-WRAPPER-R03-v3','source_mode':'PROPOSTA',
   'daily_value':quote['daily_total_pa'],'daily_unit':'PA/dia','activation_values':None if quote['per_use_total_pa'] is None else [quote['per_use_total_pa']],
   'activation_unit':'PA/uso','component_subtotal':quote['daily_component_subtotal_scenario'],'proposal_detail':quote,
   'daily_semantics':'UNKNOWN_COMMIT_VS_DEBIT'},
  'state':'PROPOSTA_NAO_QUALIFICADA_NEM_CUSTO_HOMOLOGADO','conflicts':[],
  'independent_cost_model_validated':False,'authentic_notionsignature':False,
  'master_only':True,'production_hold':True,'new_recipe_permitted':False,'approval_state':'TEST_NO_RELEASE'}
 return {'message':body,'digest_sha256':_sha(body)}

def qmc_sidecar_receive(payload:dict)->dict:
 """Local QMC consumer, DOES NOT replace QMC-02 native validate_external_pa()"""
 _reject(isinstance(payload,dict) and payload.get('digest_sha256')==_sha(payload.get('message')),'conteúdo alterado / formato ruim')
 m=payload['message']
 _reject(m.get('contract')==RESPONSE and m.get('origin_contract')==CONTRACT,'contrato inválido')
 _reject(m.get('master_only') is True and m.get('production_hold') is True and m.get('new_recipe_permitted') is False,'sinal de produção não autorizado')
 _reject(m.get('approval_state')=='TEST_NO_RELEASE' and m.get('authentic_notionsignature') is False,'autoridade inválida')
 _reject(m.get('state') in {'DOCUMENTO_HISTORICO_RECONCILIADO_TEST','PROPOSTA_NAO_QUALIFICADA_NEM_CUSTO_HOMOLOGADO'},'conflito bloqueante')
 _reject('pa_engine' in m and 'qmc' in m,'campos requeridos')
 quote=m['pa_engine']
 if m['state']=='DOCUMENTO_HISTORICO_RECONCILIADO_TEST':
  _reject(m.get('request_uuid')==qmc02.norm_id(m['qmc']['source_url']),'ID da fonte divergente')
  _reject(qmc02.norm_id(quote['source_url'])==m['request_uuid'],'PA fonte divergente')
  _reject(m['qmc']['qual_state']=='QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO','QMC source unqualified')
  verdict='ACEITO_HISTORICO_TEST_SEM_AUTORIZAR_RECEITA'
 else:
  _reject(quote['source_mode']=='PROPOSTA' and m['qmc']['source_url'] is None,'candidato indevidamente canonizado')
  verdict='ACEITO_CANDIDATO_TEST_SEM_VALIDAR_CUSTO'
 return {'consumer':'QMC02_SIDECAR_R04','receipt_state':verdict,
  'received_digest_sha256':payload['digest_sha256'],'historical_daily_pa':quote.get('daily_value'),
  'uncertain':quote.get('daily_value') is None or not m['independent_cost_model_validated'],
  'source_qualified_by_original_qmc02':m['state']=='DOCUMENTO_HISTORICO_RECONCILIADO_TEST',
  'craft_native_validation':'NAO_ALTERADA; validate_external_pa original continua recusando respostas externas',
  'no_recipe_created':True,'production_hold':True}

def run(source_path:Path,source_uuid:str,candidate_path:Path,output_dir:Path):
 sources=json.loads(source_path.read_text('utf8'))['sources'];match=[s for s in sources if qmc02.norm_id(s['uuid'])==qmc02.norm_id(source_uuid)]
 _reject(len(match)==1,'envelope QMC source missing/duplicated')
 output_dir.mkdir(exist_ok=True,parents=True)
 historic=emit_historical(match[0]);candidate=emit_candidate(json.loads(candidate_path.read_text('utf8')))
 for nm,payload in [('HISTORICO_BOTA',historic),('CANDIDATO_ESPADA',candidate)]:
  (output_dir/(nm+'_REQUEST_RESPONSE.json')).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n','utf8')
  receipt=qmc_sidecar_receive(json.loads((output_dir/(nm+'_REQUEST_RESPONSE.json')).read_text('utf8')))
  (output_dir/(nm+'_QMC_RECEIPT.json')).write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n','utf8')
 return {'historical_receipt':qmc_sidecar_receive(historic),'candidate_receipt':qmc_sidecar_receive(candidate)}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('sources');p.add_argument('uuid');p.add_argument('candidate');p.add_argument('out_dir');a=p.parse_args()
 print(json.dumps(run(Path(a.sources),a.uuid,Path(a.candidate),Path(a.out_dir)),ensure_ascii=False,indent=2))
