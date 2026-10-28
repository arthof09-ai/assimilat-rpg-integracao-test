#!/usr/bin/env python3
"""Contrato energético R05: payload para CRAFT, sem invadir QMC-02.
A aprovação nativa da QMC-02 ainda precisa ser implementada PELO executor CRAFT.
Checks locais de identidade não substituem autenticação por Notion nem writer competente.
"""
from __future__ import annotations
import hashlib,json,sys,copy
from pathlib import Path
P=Path(__file__).resolve().parent
BASE=P.parent/'BASELINES'/'R04_EXTRAIDO'/'PA_UNIVERSAL_R04_TEST_20261017'
sys.path.insert(0,str(BASE)); sys.path.insert(0,str(BASE/'BASELINE_QMC02'/'qmc02'))
import qmc02
import pa_r05 as pa

VERSION='QMC-PA-RESPONSE-R05-TEST-1'
ORIGIN='QMC-PA-INTERCHANGE-CANDIDATE-1'

def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf8')).hexdigest()

def numeric_optional(x):
    if x is not None:pa.numeric(x)
    return x

def wrap_qualified_source(src:dict)->dict:
    qualified=qmc02.inspect_source(copy.deepcopy(src))
    if qualified.get('status')!='QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO':raise ValueError('fonte QMC não qualificada')
    iq=qualified['energy_interface'];ident=qualified['identity'];sid=ident['uuid']
    if iq['contract']!=ORIGIN or iq['ITEM-ID']!=sid:raise ValueError('contrato/id')
    actual=pa.history(sid)
    v=actual['pa_daily']['value'];cls=actual['pa_daily']['classification']
    if 'R05_reconciliation' in actual:v=None;cls='MODALIDADE_INDETERMINADA_R05'
    qdaily=[i['value'] for i in qualified['costs']['daily']]
    observed_acts=[i['value'] for i in qualified['costs']['activation']]
    acts=[x['value'] for x in actual['activation_abilities']] if actual['activation_abilities'] else ([actual['pa_activation']['value']] if actual['pa_activation']['value'] is not None else [])
    # QMC-02 extrato é o mesmo item físico, mas o seu parser pode omitir R-PA-DIA. Não alegar paridade onde não há.
    conflicts=[]
    if qdaily and (v is None or any(x!=v for x in qdaily)):conflicts.append('PA_DIA_DIVERGENTE_ENTRE_EXTRATO_E_R05')
    if sorted(observed_acts)!=sorted(acts):conflicts.append('PA_ATIVACOES_DIVERGENTES')
    attr_audit=actual.get('audit_attribute_rule');
    if attr_audit and attr_audit['issues']:conflicts.append('CUSTO_HISTORICO_INCONSISTENTE_COM_REGRA_ATRIBUTOS')
    msg={'contract':VERSION,'origin_contract':ORIGIN,'kind':'HISTORICO','uuid':sid,'source_url':ident['url'],
         'qmc_module':ident['module'],'qmc_family':ident['family'],'qmc_qualifier':'QMC02_ORIGINAL_inspect_source',
         'qualified_excerpt_sha256':qualified['provenance']['content_sha256_excerpt'],
         'qualified_observed_at':qualified['provenance']['observed_at'],'pa_engine':'PA-R05-ATTRIBUTE-MESTRE',
         'daily_pa':v,'daily_unit':'PA/dia','daily_classification':cls,'activation_pa_values':acts,'activation_unit':'PA/uso',
         'attribute_rule':'5 PA/dia por +1 atributo','rule_authority':pa.RULE_ID,'conflicts':conflicts,
         'uncertainty':{'historical_cost':'documented only; conditional when R-PA-DIA','numeric_energy_model':'unvalidated for other effects'},
         'approval_status':'TEST_NO_RELEASE','production_hold':True,'new_recipe_permitted':False,
         'notion_signed':False,'master_only':True}
    return {'message':msg,'digest_sha256':sha(msg)}

def wrap_candidate(candidate:dict)->dict:
    if candidate.get('evidence_type')!='USER_EXPERIMENTAL_SPEC':raise ValueError('candidate origin needed')
    q=pa.component_model(candidate.get('effects',[]));cid=candidate['candidate_id']
    msg={'contract':VERSION,'origin_contract':ORIGIN,'kind':'PROPOSTA','uuid':None,'candidate_id':cid,'source_url':None,
         'qmc_module':candidate.get('qmc_module'),'qmc_family':candidate.get('qmc_family'),
         'qmc_qualifier':'QMC02_ORIGINAL_NAO_QUALIFICOU_CANDIDATO','qualified_excerpt_sha256':None,
         'qualified_observed_at':None,'pa_engine':'PA-R05-ATTRIBUTE-MESTRE',
         'daily_pa':q['daily_total_pa'],'daily_unit':'PA/dia','daily_classification':q['daily_total_status'],
         'activation_pa_values':None if q['activation_total_pa_per_use'] is None else [q['activation_total_pa_per_use']],
         'activation_unit':'PA/uso','components':q['components'],'identified_daily_subtotal':q['daily_pa_subtotal_identified'],
         'rule_authority':pa.RULE_ID,'conflicts':[],'uncertainty':{'missing_daily':q['missing_daily'],
         'missing_activation':q['missing_activation'],'model':'não identificado fora atributos'},
         'approval_status':'TEST_NO_RELEASE','production_hold':True,'new_recipe_permitted':False,
         'notion_signed':False,'master_only':True}
    return {'message':msg,'digest_sha256':sha(msg)}

def strict_local_validation(data:dict)->dict:
    """TEST: filtro local versionado, não endosso nativo QMC ou assinatura da fonte."""
    if not isinstance(data,dict) or set(data)!={'message','digest_sha256'}:raise ValueError('payload')
    msg=data['message']
    if not isinstance(msg,dict) or data['digest_sha256']!=sha(msg):raise ValueError('checksum mutado')
    if msg['contract']!=VERSION or msg['origin_contract']!=ORIGIN:raise ValueError('schema version')
    if msg.get('approval_status')!='TEST_NO_RELEASE' or msg.get('production_hold') is not True or msg.get('new_recipe_permitted') is not False:raise ValueError('produção indevidamente promovida')
    if msg.get('notion_signed') is not False or msg.get('master_only') is not True:raise ValueError('claims de origem')
    if msg.get('rule_authority')!=pa.RULE_ID or msg.get('pa_engine')!='PA-R05-ATTRIBUTE-MESTRE':raise ValueError('autoridade ausente')
    if msg.get('daily_unit')!='PA/dia' or msg.get('activation_unit')!='PA/uso':raise ValueError('unidades inválidas')
    numeric_optional(msg.get('daily_pa'))
    for n in msg.get('activation_pa_values') or []:numeric_optional(n)
    if msg['kind']=='HISTORICO':
        if qmc02.norm_id(msg['source_url'])!=msg['uuid']:raise ValueError('UUID source mismatch')
        if len(str(msg['qualified_excerpt_sha256']))!=64:raise ValueError('sem source fingerprint')
        if msg['qmc_qualifier']!='QMC02_ORIGINAL_inspect_source':raise ValueError('sem qualificação')
        # Independently bind a wire value to the ORIGINAL QMC-02 source pack AND R03 immutable corpus.
        # It is not a Notion digital signature: it prevents local retagging/recomputation of the plain SHA.
        originals=json.loads((BASE/'BASELINE_QMC02'/'qmc02'/'source_readbacks.json').read_text('utf8'))['sources']
        matched=[x for x in originals if qmc02.norm_id(x.get('uuid',''))==msg['uuid']]
        if len(matched)!=1:raise ValueError('ficha não presente no baseline QMC-02 preservado')
        qualification=qmc02.inspect_source(matched[0])
        if qualification.get('status')!='QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO':raise ValueError('qualificação física falhou')
        if msg['qualified_excerpt_sha256']!=qualification['provenance']['content_sha256_excerpt']:
            raise ValueError('fingerprint do extrato divergente do baseline QMC')
        hist=pa.history(msg['uuid'])
        expected_day=None if hist.get('R05_reconciliation') else hist['pa_daily']['value']
        acts=[a['value'] for a in hist['activation_abilities']] if hist['activation_abilities'] else ([hist['pa_activation']['value']] if hist['pa_activation']['value'] is not None else [])
        if msg.get('daily_pa')!=expected_day or sorted(msg.get('activation_pa_values') or [])!=sorted(acts):
            raise ValueError('valor histórico alterado sem corresponder às fontes originais')
        original_conflicts=[]
        if qualification['costs']['daily'] and (expected_day is None or any(y['value']!=expected_day for y in qualification['costs']['daily'])):
            original_conflicts.append('PA_DIA_DIVERGENTE_ENTRE_EXTRATO_E_R05')
        if sorted(y['value'] for y in qualification['costs']['activation'])!=sorted(acts):original_conflicts.append('PA_ATIVACOES_DIVERGENTES')
        audit=hist.get('audit_attribute_rule')
        if audit and audit['issues']:original_conflicts.append('CUSTO_HISTORICO_INCONSISTENTE_COM_REGRA_ATRIBUTOS')
        if sorted(original_conflicts)!=sorted(msg.get('conflicts',[])):
            raise ValueError('conflitos não correspondem a auditoria original')
    elif msg['kind']=='PROPOSTA':
        if msg['source_url'] is not None or msg['uuid'] is not None:raise ValueError('candidato se diz canônico')
        if not msg['candidate_id']:raise ValueError('sem candidato')
        if not isinstance(msg.get('components'),list):raise ValueError('componentes ausentes')
        reparsed=[{'id':e['id'],'kind':e['kind'],'attribute':e.get('attribute'),'magnitude':e['magnitude'],
                   'mode':e['mode'],'source':e.get('source'),'conditions':e.get('conditions'),
                   'frequency':e.get('frequency'),'duration':e.get('duration'),
                   'targets':e.get('targets')} for e in msg['components']]
        # For R05 proposals, only attribute components and unpriced effects are accepted.
        # Historical priced components require more source fields; do not bypass provenance via this route.
        if any(e['kind'] in ('CUSTO_DIARIO_HISTORICO','CUSTO_ATIVACAO_HISTORICO') for e in reparsed):
            raise ValueError('componente histórico em candidato sem verificação de origem')
        independent=pa.component_model(reparsed)
        if (msg['daily_pa']!=independent['daily_total_pa'] or
            msg.get('identified_daily_subtotal')!=independent['daily_pa_subtotal_identified'] or
            msg.get('daily_classification')!=independent['daily_total_status'] or
            msg.get('activation_pa_values')!=(None if independent['activation_total_pa_per_use'] is None else [independent['activation_total_pa_per_use']])):
            raise ValueError('custo proposto adulterado em relação aos componentes declarados')
    else:raise ValueError('source type')
    if msg.get('conflicts'):return {'status':'CONFLITO_HOLD_TEST','can_accept_cost':False,'native_qmc_accepted':False,'safe':True}
    return {'status':'RECEBIDO_R05_TEST_FORA_DO_ENTRYPOINT_NATIVO','can_accept_cost':False,
            'native_qmc_accepted':False,'safe':True,'approved_for_recipe':False,'payload_sha256':data['digest_sha256']}

def native_qmc_probe(data:dict)->dict:
    """Executa o validador ORIGINAL, prova a fronteira sem adulterá-lo."""
    rep=qmc02.validate_external_pa(data['message'])
    return {'entrypoint':'QMC-02_ORIGINAL.validate_external_pa','native_return':rep,
            'native_accepted':False,'expected_gap':'INTERFACE_EXTERNA_NAO_CONTRATADA','baseline_modified':False}

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--out');a=parser.parse_args()
 source=json.loads(Path(a.input).read_text('utf8'))
 if source.get('evidence_type')=='USER_EXPERIMENTAL_SPEC':r=wrap_candidate(source)
 else:r=wrap_qualified_source(source)
 report={'wire':r,'test_receipt':strict_local_validation(r),'native_probe':native_qmc_probe(r)}
 if a.out:Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
