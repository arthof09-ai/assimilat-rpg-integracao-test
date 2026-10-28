#!/usr/bin/env python3
"""R05, extensão aditiva do R04 — decisão expressa do Mestre, sem alterar R04/QMC-02.
Esta camada NÃO ensina ao CRAFT uma tarifa arbitrária para dano/CA/RD/controle.
FONTE DA REGRA: decisão expressa do Mestre no chat de 17/10/2026, R05:
"1 atributo = 5 pontos de PA por dia; itens que não seguem essa regra estão erradas".
Sem escrita Notion, Party, CRAFT produtivo ou receitas.
"""
from __future__ import annotations
import copy,json,re,sys,math,statistics
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'BASELINES'/'R04_EXTRAIDO'/'PA_UNIVERSAL_R04_TEST_20261017'
if not BASE.exists():
    raise RuntimeError('Execute bootstrap_baselines.py antes: baseline R04 original obrigatório')
sys.path.insert(0,str(BASE))
import pa_r04
from pa_r04 import r03

ATTR_RATE=5
RULE_ID='DECISAO_EXPRESSA_MESTRE_CHAT_R05_20261017_ATRIBUTO_5'  # Identificador local de rastreio, NAO ID Notion canonico
RULE_SOURCE='ORDEM_EXPRESSA_MESTRE_NESTA_CONVERSA_20261017'
SCOPE='BONUS_NUMERICO_DE_ATRIBUTO_MANTIDO_DIARIAMENTE'
NO_COST={'dano_passivo_por_acerto','dano_ativo','rd_elemental','rd_universal','rdm','ca','deslocamento_ativo','cura','controle','area','alcance','duracao','reacao','percepcao','salvaguarda','dano_por_turno'}

# Redados da fonte reaberta; AUSÊNCIA de custo PA não equivale a PA=0.
ATTR_ANCHORS=[
 {'uuid':'3c6c2b324ede82baa4a801de533a5975','name':'Amplificador de Atributo','surface':'PARTY_MESTRE_ESPELHO','bonus':{'QUALQUER_ATRIBUTO':3},'max_magnitude':3,'daily_pa_history':15,'kind':'CONFORME','confidence':'DOCUMENTO_ESPELHO','cost_status':'EXPLICITO'},
 {'uuid':'3edc2b324ede815699adc0412e96ea2b','name':'Sabedoria Ancestral','surface':'CATALOGO_MESTRE','bonus':{'SAB':10},'daily_pa_history':20,'max_magnitude':10,'kind':'DIVERGENCIA','confidence':'R-PA-DIA_DEPENDE_FIM_DA_FICHA','cost_status':'R_PA_DIA_SENSIVEL'},
 {'uuid':'3edc2b324ede810daba2cc509677856c','name':'Colar cadente','surface':'CATALOGO_MESTRE','bonus':{'SAB':2},'alternate_conditions':[{'when':'LUZ_DAS_ESTRELAS','bonus':{'SAB':4}}],'daily_pa_history':14,'max_magnitude':4,'kind':'DIVERGENCIA_CONDICIONAL','confidence':'EXPLICITO','cost_status':'EXPLICITO'},
 {'uuid':'0c4c2b324ede83dd8e1881b52a79e326','name':'Amuleto de Inteligência','surface':'PARTY_MESTRE_ESPELHO','bonus':{'INT':10},'daily_pa_history':30,'max_magnitude':10,'kind':'DIVERGENCIA','confidence':'R-PA-DIA','cost_status':'R_PA_DIA_SENSIVEL'},
 {'uuid':'3edc2b324ede81ab9e22e168f6d939a9','name':'Espada do Lendário','surface':'CATALOGO_MESTRE','bonus':{'FOR':60},'daily_pa_history':600,'max_magnitude':60,'kind':'SEM_DIVERGENCIA_DE_PISO','confidence':'RESUMO_R03','cost_status':'EXPLICITO'},
 {'uuid':'a23c2b324ede829bb8168165991577ff','name':'Armadura de Zephyr','surface':'PARTY_MESTRE_ESPELHO','bonus':{'DES':15},'daily_pa_history':90,'max_magnitude':15,'kind':'SEM_DIVERGENCIA_DE_PISO','confidence':'READBACK_R04','cost_status':'EXPLICITO'},
 {'uuid':'a70c2b324ede83c2ac490135cd512e9f','name':'Lâmina Aurora Boreal','surface':'PARTY_MESTRE_ESPELHO','bonus':{'CAR':5,'FOR':7,'CON':3},'daily_pa_history':95,'max_magnitude':15,'kind':'SEM_DIVERGENCIA_DE_PISO','confidence':'READBACK_R04','cost_status':'EXPLICITO'},
 {'uuid':'622c2b324ede8213a609818e7ef09a9a','name':'Bastião de Virilia','surface':'PARTY_MESTRE_ESPELHO','bonus':{'FOR':2},'daily_pa_history':24,'max_magnitude':2,'kind':'SEM_DIVERGENCIA_DE_PISO','confidence':'READBACK_R04','cost_status':'EXPLICITO'},
 {'uuid':'089c2b324ede837c9e590174fcc33291','name':'Couraça de Eos','surface':'PARTY_MESTRE_ESPELHO','bonus':{'SAB':2},'daily_pa_history':24,'max_magnitude':2,'kind':'SEM_DIVERGENCIA_DE_PISO','confidence':'READBACK_R04','cost_status':'EXPLICITO'},
 {'uuid':'56cc2b324ede823586be01440f7a68ef','name':'Bracelete Calma Elemental','surface':'PARTY_MESTRE_ESPELHO','bonus':{'SAB':3},'daily_pa_history':21,'max_magnitude':3,'kind':'SEM_DIVERGENCIA_DE_PISO','confidence':'READBACK_R04','cost_status':'EXPLICITO'},
]


def numeric(n,label='valor'):
    if isinstance(n,bool) or not isinstance(n,(int,float)) or not math.isfinite(n) or n<0:raise ValueError(f'{label}: valor inválido')
    return n

def quote_attribute(bonus:dict,mode='PASSIVO_DIARIO')->dict:
    if not isinstance(bonus,dict) or not bonus:raise ValueError('bônus de atributos obrigatório')
    vals={}
    for k,v in bonus.items():
        name=str(k).upper();numeric(v,name)
        if name not in {'FOR','DES','CON','INT','SAB','CAR','QUALQUER_ATRIBUTO'}:raise ValueError('atributo não reconhecido')
        vals[name]=vals.get(name,0)+v
    if 'QUALQUER_ATRIBUTO' in vals and len(vals)>1:raise ValueError('atributo genérico e específico duplicados')
    if mode!='PASSIVO_DIARIO':
        return {'status':'MODALIDADE_NAO_COBERTA_PELA_REGRA_DIARIA','per_use_pa':None,'daily_pa':None,'rule':RULE_ID}
    components=[{'attribute':k,'bonus':v,'pa_per_point_per_day':ATTR_RATE,'cost_pa_day':v*ATTR_RATE} for k,v in sorted(vals.items())]
    return {'status':'REGRA_EXPRESSA_MESTRE','source':RULE_SOURCE,'rule':RULE_ID,'unit':'PA/dia','scope':SCOPE,
            'components':components,'daily_pa':sum(v['cost_pa_day'] for v in components), 'uncertainty':{'normative':0,'scientific_prediction_error':None},'production_hold':True}


def audit_anchor(x:dict)->dict:
    q=quote_attribute(x['bonus']); scenarios=[{'when':'PADRAO','required_pa_daily':q['daily_pa'],'bonus':x['bonus']}]
    for alt in x.get('alternate_conditions',[]):
        scenarios.append({'when':alt['when'],'required_pa_daily':quote_attribute(alt['bonus'])['daily_pa'],'bonus':alt['bonus']})
    observed=x['daily_pa_history'];issues=[]
    for s in scenarios:
        if observed is not None and observed<s['required_pa_daily']:
            issues.append({'condition':s['when'],'minimum_required_for_attributes':s['required_pa_daily'],
                           'historical_daily':observed,'deficit_pa_day_at_least':s['required_pa_daily']-observed,
                           'issue':'VALOR_HISTORICO_NAO_SATISFAZ_REGRA_MESTRE','other_components':'NAO_PRECIFICADOS'})
    return {**copy.deepcopy(x),'url':'https://app.notion.com/p/'+x['uuid'],'rule':RULE_ID,'scenarios':scenarios,'issues':issues,
            'status':'INCONSISTENTE_COM_REGRA_MESTRE' if issues else 'PISO_ATRIBUTO_COBERTO_SEM_VALIDAR_EXTRAS',
            'historical_unmodified':True,'automatic_write':False,'proposed_total':None if issues else observed,
            'minimum_corrected_pa_day_for_attributes':max(s['required_pa_daily'] for s in scenarios)}


def audit_all()->dict:
    results=[audit_anchor(a) for a in ATTR_ANCHORS]
    return {'rule':RULE_ID,'status':'REGRA_DETERMINADA_PELO_MESTRE_NAO_COEFICIENTE_EMPIRICO',
        'scope':'readback de 10 comparadores seletivos; NÃO varredura exaustiva de todas as fichas',
        'tested_pages':len(results),'conflicted_pages':sum(bool(x['issues']) for x in results),
        'master_conflicted_pages':sum(bool(x['issues']) and x['surface']=='CATALOGO_MESTRE' for x in results),
        'mirror_conflicted_pages':sum(bool(x['issues']) and x['surface']=='PARTY_MESTRE_ESPELHO' for x in results),
        'results':results,'no_write':True}


def component_model(effects:list,scope='CANDIDATO_TEST')->dict:
    """Regra fixa apenas ATRIBUTOS permanentes. Outras parcelas: só fatos ou incógnitas.
    Não soma parcelas historicamente já incluídas nem reprecifica histórico automaticamente.
    """
    if not isinstance(effects,list):raise ValueError('effects deve ser lista')
    if not effects:return {'mode':'PROPOSTA','components':[],'daily_total_pa':None,'daily_pa_subtotal_identified':0,'activation_total_pa_per_use':None,'daily_total_status':'SEM_EFEITOS_DESCRITOS_NAO_INFERIR_ZERO','missing_daily':['DESCRICAO_AUSENTE'],'missing_activation':[], 'no_new_recipe':True,'production_hold':True}
    seen=set();components=[];known_day=0;known_active=0;missing_day=[];missing_active=[]
    attr_agg={};unknown_overlap=False
    for e in effects:
        if not isinstance(e,dict):raise ValueError('efeito inválido')
        eid=e.get('id');
        if not isinstance(eid,str) or not eid or eid in seen:raise ValueError('efeito sem ID ou duplicado')
        seen.add(eid)
        kind=e.get('kind');mode=e.get('mode','PASSIVO_DIARIO');mag=numeric(e.get('magnitude'),eid)
        att=(e.get('attribute') or '').upper()
        origin=e.get('source')
        if kind=='ATRIBUTO':
            if att not in {'FOR','DES','CON','INT','SAB','CAR'}:raise ValueError('atributo inválido')
            if mode=='PASSIVO_DIARIO':
                cost=mag*ATTR_RATE;known_day+=cost
                if att in attr_agg:unknown_overlap=True
                attr_agg[att]=attr_agg.get(att,0)+mag
                stat='REGRA_MESTRE';unit='PA/dia'
            else:
                cost=None;stat='ATIVACAO_ATRIBUTO_SEM_TARIFA_POR_USO';unit='PA/uso';missing_active.append(eid)
        elif kind=='CUSTO_ATIVACAO_HISTORICO':
            if mode!='ATIVO_POR_USO' or not origin or not e.get('literal') or not e.get('authorized_as_historical'):
                raise ValueError('custo histórico exige fonte, literal e modalidade')
            cost=mag;known_active+=cost;unit='PA/uso';stat='HISTORICO_DOCUMENTADO'
        elif kind=='CUSTO_DIARIO_HISTORICO':
            if mode!='AGREGADO_HISTORICO' or not origin or not e.get('literal') or not e.get('authorized_as_historical'):
                raise ValueError('agregado histórico exige fonte e literal')
            cost=mag;unit='PA/dia';stat='AGREGADO_HISTORICO_NAO_SOMAR_COMPONENTES'
        else:
            if kind not in NO_COST:raise ValueError('tipo desconhecido não possui tarifa')
            cost=None;unit='PA/uso' if mode=='ATIVO_POR_USO' else 'PA/dia';stat='PARAMETRO_NAO_IDENTIFICAVEL'
            (missing_active if mode=='ATIVO_POR_USO' else missing_day).append(eid)
        components.append({'id':eid,'kind':kind,'attribute':att or None,'magnitude':mag,'mode':mode,'unit':unit,
                          'pa':cost,'cost_status':stat,'source':origin,'conditions':e.get('conditions'),
                          'frequency':e.get('frequency'),'duration':e.get('duration'),'targets':e.get('targets'),
                          'independence':e.get('independence','NAO_VERIFICADA')})
    hist=[x for x in components if x['kind']=='CUSTO_DIARIO_HISTORICO']
    if len(hist)>1:raise ValueError('agregado histórico repetido')
    if hist:
        daily_total=hist[0]['pa'];total_status='CUSTO_TOTAL_HISTORICO_SEM_RECALCULAR'
        if any(x['kind']=='ATRIBUTO' for x in components):
            # Não somar custos agregados e tarifas novamente; reportar conflito se necessário
            if daily_total<known_day:total_status='HISTORICO_CONFLITANTE_COM_REGRA_DE_ATRIBUTO'
    elif missing_day or unknown_overlap:
        daily_total=None;total_status='TOTAL_NAO_IDENTIFICAVEL'
    elif not attr_agg:
        daily_total=None;total_status='PA_DIARIO_NAO_DOCUMENTADO_NAO_E_ZERO'
    else:daily_total=known_day;total_status='TOTAL_REGRA_MESTRE_APENAS_ATRIBUTOS'
    return {'mode':'PROPOSTA' if scope!='HISTORICO' else 'HISTORICO', 'rule':RULE_ID,'components':components,
        'attr_only_exact_daily':known_day if attr_agg else None,'daily_pa_subtotal_identified':known_day,
        'daily_total_pa':daily_total,'daily_total_status':total_status,
        'activation_known_subtotal_per_use':known_active,'activation_total_pa_per_use':None if missing_active else known_active,
        'missing_daily':missing_day,'missing_activation':missing_active,'possible_double_counting':bool(hist and attr_agg),
        'possible_overlap_or_stacking':unknown_overlap,'no_new_recipe':True,'production_hold':True,
        'confidence':{'attribute_rule':'MESTRE_DETERMINADA','other_rates':'NAO_IDENTIFICADOS'},
        'notion_write':False}


def available_pa_budget(pa_total=None,pa_committed_other=None,pa_free_declared=None,
                        daily_pa=None,activation_pa=None,activation_count=0,semantics='UNKNOWN')->dict:
    if semantics not in {'UNKNOWN','COMMIT','DEBIT'}:raise ValueError('semantics inválida')
    if pa_total is not None:numeric(pa_total,'pa_total')
    if pa_committed_other is not None:numeric(pa_committed_other,'pa_comprometido_outros')
    if pa_free_declared is not None:numeric(pa_free_declared,'pa_livre_declarado')
    if daily_pa is not None:numeric(daily_pa,'pa_diario')
    if activation_pa is not None:numeric(activation_pa,'pa_ativacao')
    if isinstance(activation_count,bool) or not isinstance(activation_count,int) or activation_count<0:raise ValueError('activation count')
    if pa_total is not None and pa_committed_other is not None and pa_committed_other>pa_total:raise ValueError('pa comprometido acima do total')
    computed_free=(pa_total-pa_committed_other) if pa_total is not None and pa_committed_other is not None else None
    if computed_free is not None and pa_free_declared is not None and abs(computed_free-pa_free_declared)>1e-8:
        raise ValueError('PA Livre informado diverge de PA Total - comprometido; reconciliar')
    free=pa_free_declared if pa_free_declared is not None else computed_free
    out={'pa_total':pa_total,'pa_committed_other':pa_committed_other,'pa_free_declared_or_computed':free,
         'known_daily_pa':daily_pa,'known_activation_pa_per_use':activation_pa,'requested_uses':activation_count,
         'daily_semantics':semantics,'spell_exhaustion_rule_extended_to_items':False,
         'item_use_authorized':False,'status':'INDETERMINADO','reason':'semântica diária não canonizada ou parcelas faltantes',
         'free_after_daily_if_commit':None,'free_after_uses_if_commit':None,'free_after_daily_if_debit':None}
    if daily_pa is None or free is None:return out
    if semantics=='COMMIT':
        out['free_after_daily_if_commit']=free-daily_pa if free>=daily_pa else None
        if free<daily_pa:out['status']='INSUFICIENTE_NUMERICAMENTE_NO_CENARIO_COMMIT'
        elif activation_pa is not None:
            left=free-daily_pa-activation_pa*activation_count
            out['free_after_uses_if_commit']=left if left>=0 else None
            out['status']='COBERTURA_NUMERICA_NO_CENARIO_COMMIT' if left>=0 else 'INSUFICIENTE_NUMERICAMENTE_NO_CENARIO_COMMIT'
    elif semantics=='DEBIT':
        out['free_after_daily_if_debit']=free-daily_pa if free>=daily_pa else None
        if free<daily_pa:out['status']='INSUFICIENTE_NUMERICAMENTE_NO_CENARIO_DEBIT'
        elif activation_pa is not None:out['status']='COBERTURA_NUMERICA_CONDICIONAL_DEBIT' if free>=daily_pa+activation_pa*activation_count else 'INSUFICIENTE_NUMERICAMENTE_NO_CENARIO_DEBIT'
    out['reason']='Cenário contábil, não mecanismo canônico de cobrança diária; produção bloqueada'
    return out


def history(identifier):
    """Preserva custo literal mesmo se inválido segundo regra atual; retorna declaração de conflito."""
    h=r03.historical(identifier);h['daily_source_status']='DOCUMENTADO_HISTORICO_NAO_REESCRITO'
    match=next((x for x in ATTR_ANCHORS if x['uuid']==h['id']),None)
    if match:h['audit_attribute_rule']=audit_anchor(match)
    if h['id']=='3edc2b324ede811787a0de913622b14d':
        # R05 corrige leitura R03: literal '35 de PA' não é N PA, e existe metadado de anel posterior.
        h['R05_reconciliation']={'historical_raw':'35 de PA.','pa_daily_status':'INDETERMINADO_NAO_APLICAR_R_PA_DIA_SEM_GATE',
          'reason':'Padrão R-PA-DIA exige N PA isolado ao término da ficha. Literal usa N de PA e há material após; QMC-02 originalmente indeterminado.',
          'R03_value_preserved_for_history':h['pa_daily']['value'],'usable_daily_pa_R05':None}
    return h


def identifiability_matrix():
    return [
        {'parameter':'ATRIBUTO_PERMANENTE','unit':'PA/dia/ponto','value':5,'evidence':'REGRA_EXPRESSA_DO_MESTRE','status':'IDENTIFICADO_POR_AUTORIDADE_NAO_POR_ESTIMACAO','n_pure_master_empirical':0,'n_pure_mirror':1,'n_truly_independent_master_holdout':0,'uncertainty':'normativa=0; previsão para mixes pendente'},
        {'parameter':'DANO_POR_ACERTO','unit':'PA/dia/ponto de dano','value':None,'evidence':'itens compostos, dano condicional, nenhuma diferença isolada independente Mestre','status':'NAO_IDENTIFICAVEL','n_clean_pairs_master':0,'uncertainty':'não quantificável'},
        {'parameter':'DANO_1x_DIA','unit':'PA/uso ou PA/dia','value':None,'evidence':'bônus histórico sem par equivalente passivo/ativo','status':'NAO_IDENTIFICAVEL','n_clean_pairs_master':0,'uncertainty':'não quantificável'},
        {'parameter':'RD_CONTRA_ELEMENTAIS','unit':'PA/dia/ponto RD','value':None,'evidence':'Armadura Guardiã Elemental: +6CA, +8 salvaguarda, RD35, custo conjunto55','status':'NAO_IDENTIFICAVEL','n_clean_pairs_master':0,'uncertainty':'não quantificável'},
        {'parameter':'CA','unit':'PA/dia/ponto CA','value':None,'evidence':'preços de melhorias Espelho não aplicáveis automaticamente ao Mestre','status':'NAO_IDENTIFICAVEL','n_clean_pairs_master':0,'uncertainty':'não quantificável'},
        {'parameter':'ATIVACAO_HISTORICA','unit':'PA/uso','value':None,'evidence':'Bota 5/uso, outras habilidades têm preços literais diferentes','status':'IDENTIFICAVEL_POR_HABILIDADE_HISTORICA_NAO_TARIFA_UNIVERSAL','n_clean_pairs_master':0,'uncertainty':'sem generalização entre habilidades'},
        {'parameter':'DESLOCAMENTO','unit':'PA/m ou PA/dia/m','value':None,'evidence':'Bota tem custos diário/uso e passivos, sem isolamento','status':'NAO_IDENTIFICAVEL','n_clean_pairs_master':0,'uncertainty':'não quantificável'},
        {'parameter':'PROTECAO_RDM_CURA_PERCEPCAO_CONTROLE','unit':'múltiplas','value':None,'evidence':'observações mistas, incompletas ou espelho','status':'NAO_IDENTIFICAVEL','n_clean_pairs_master':0,'uncertainty':'não quantificável'},
        {'parameter':'PA_DIARIO_COMMIT_VS_DEBIT','unit':'regra mecânica','value':None,'evidence':'Sistema de Magia define PA Livre, não classifica universalmente débito diário de todos os itens','status':'SEMANTICA_NAO_RECONCILIADA','uncertainty':'cenários condicionais'},
    ]


def simple_model_validation():
    """Exploratório agrupado (R03 visto antes), NÃO holdout independente.
    Exclui custos por fonte não tipada e fichas em conflito com Mestre.
    """
    from collections import defaultdict
    rows=json.loads((BASE/'CORPUS_ORIGEM_AUDITADA_R04.json').read_text('utf8'))['rows']
    eligible=[]
    for r in rows:
        if r['surface']!='CATALOGO_MESTRE_INDEXADO' or r['pa_daily'] is None:continue
        if r['uuid'] in {'3edc2b324ede811787a0de913622b14d','3edc2b324ede815699adc0412e96ea2b','3edc2b324ede810daba2cc509677856c'}:
            continue
        eligible.append(r)
    groups=defaultdict(list)
    for r in eligible:groups[r['lineage']].append(r)
    groupvals={k:statistics.mean(r['pa_daily'] for r in group) for k,group in groups.items()}
    details=[]
    for g,truth in groupvals.items():
        training=[v for k,v in groupvals.items() if k!=g]
        med=statistics.median(training)
        naive20=20
        details.append({'test_group':g,'n_variants_in_group':len(groups[g]),'observed_pa_daily':truth,
                        'prediction_constant_20':naive20,'prediction_group_held_out_median':med,
                        'abs_err_naive20':abs(truth-naive20),'abs_err_median':abs(truth-med),
                        'abs_rel_err_naive20':abs(truth-naive20)/truth if truth else None,
                        'abs_rel_err_median':abs(truth-med)/truth if truth else None})
    return {'type':'RETROSPECTIVE_GROUP_EXPLORATION_NOT_INDEPENDENT_HOLDOUT','preselected_models':['constant_20','median_train_groups'],
        'n_raw_master_daily_R04':14,'n_excluded_conflict_or_untyped':3,'n_included_pages':len(eligible),
        'n_lineage_groups':len(groupvals),'n_test_predictions':len(details),
        'MAE_constant20':statistics.mean(x['abs_err_naive20'] for x in details),
        'MAE_median_grouped_LOO':statistics.mean(x['abs_err_median'] for x in details),
        'MAPE_constant20':statistics.mean(x['abs_rel_err_naive20'] for x in details),
        'MAPE_median_grouped_LOO':statistics.mean(x['abs_rel_err_median'] for x in details),
        'details':details, 'limitations':['valores históricos já vistos na R03/R04','não testar causalmente famílias de efeitos','censoring e seleção de custos não aleatória','grupo de linhagem provisório','desenvolvimento não independente de holdout']}


def scientific_status():
    return {'rule':RULE_ID,'fixed_attr_5':True,'empirically_estimated_universal_coefficients':0,
        'new_master_catalog_pages_examined':55,'new_master_technique_pages_examined':28,'new_master_consumable_pages_examined':27,'new_master_pages_with_PA_in_readable_text':0,
        'new_independent_master_energy_observations':0,'new_party_pages_examined':17,'new_semicanon_pages_examined':2,
        'n_r03_documented_daily_master':14,'n_r05_unambiguous_explicit_master_daily':12,
        'n_r05_R_PA_DIA_sensitive_master':1,'n_r05_untyped_master_daily_from_R03':1,
        'independent_master_holdout_numeric_n':0,'native_craft_qmc02_approved':False,'production_hold':True,
        'no_new_recipe':True,'no_party_write':True}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['attr','audit','coefficients','validation','status','history']);parser.add_argument('arg',nargs='?');a=parser.parse_args()
    if a.mode=='attr':o=quote_attribute({'DES':float(a.arg or 5)})
    elif a.mode=='audit':o=audit_all()
    elif a.mode=='coefficients':o=identifiability_matrix()
    elif a.mode=='validation':o=simple_model_validation()
    elif a.mode=='history':o=history(a.arg)
    else:o=scientific_status()
    print(json.dumps(o,ensure_ascii=False,indent=2))
