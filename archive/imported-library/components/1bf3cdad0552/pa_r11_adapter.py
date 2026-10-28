"""PA R11–R18: extensão TEST do consultor R05 e guard R10, sem substituir baselines.
Importa os módulos originais recuperados; nenhum acesso de escrita ao Notion/CRAFT.
"""
from __future__ import annotations
import sys,hashlib,json,re,unicodedata
from pathlib import Path
from decimal import Decimal,InvalidOperation

ROOT=Path(__file__).resolve().parent.parent
R05=ROOT/'PA_UNIVERSAL_R05_TEST_20261017'/'R05_CODE'
R10=ROOT/'R10_READONLY'
for p in (str(R05),str(R10)):
    if p not in sys.path:sys.path.insert(0,p)
import pa_r05  # motor existente, read-only
import consultor_pa_r05  # controlador de contexto histórico R05
from pa_r10_guard import quote_effects,load_r09,correction_preview

CONTRACT='PA-R11-ADAPTER-TEST-1'
RATES={'ATRIBUTO_PERMANENTE':'5','DANO_FIXO_ADICIONAL':'1','DESLOCAMENTO_PERMANENTE_M':'1','BONUS_TESTE_ATAQUE':'1','CA_MAGICA':'1'}

def _n(x,field='valor',zero_ok=True):
    if isinstance(x,bool) or x is None:raise ValueError(f'{field}: número necessário')
    try:d=Decimal(str(x))
    except (InvalidOperation,ValueError):raise ValueError(f'{field}: valor inválido')
    if not d.is_finite() or (d<0 if zero_ok else d<=0):raise ValueError(f'{field}: negativo/não finito')
    return d

def _s(v):return None if v is None else format(v.normalize(),'f')

def estimate(spec:dict)->dict:
    """Estimativa dos efeitos reconhecidos mais modalidade independente, não fechamento implícito."""
    if not isinstance(spec,dict) or spec.get('source_class') not in {'USER_EXPERIMENTAL_SPEC','LOCAL_VERIFIED_EXCERPT'}:
        raise ValueError('fonte tipada obrigatória')
    effects=spec.get('effects',[])
    # R10 is the authoritative arithmetic gate; do not duplicate its tariffs.
    calc=quote_effects(effects,assertion_no_other_effects=spec.get('all_effects_documented') is True)
    # Costs of activation are NEVER inferred from daily tariffs; independent source-typed literals only.
    costs=spec.get('activation_costs',[])
    ids=set();acts=[]
    for c in costs:
        if not isinstance(c,dict) or not c.get('ability_id') or c['ability_id'] in ids:
            raise ValueError('ativação sem ID único')
        ids.add(c['ability_id'])
        if c.get('unit')!='PA/ativação' or c.get('evidence')!='LITERAL_DOCUMENTED' or not c.get('source_url') or not c.get('source_literal'):
            raise ValueError('custo ativação sem modalidade e fonte literal')
        v=_n(c.get('pa'),c['ability_id'])
        acts.append({'ability_id':c['ability_id'],'per_use_pa':_s(v),'source_url':c['source_url'],
                     'evidence':'LITERAL_DOCUMENTED','source_literal':c['source_literal']})
    daily_history=spec.get('historical_daily')
    aggregate=None
    if daily_history is not None:
        if daily_history.get('unit')!='PA/dia' or daily_history.get('evidence')!='LITERAL_DOCUMENTED' or not daily_history.get('source_url') or not daily_history.get('source_literal'):
            raise ValueError('agregado histórico não sustentado')
        aggregate=_n(daily_history.get('pa'),'historical_daily')
    identified=_n(calc['identified_daily_subtotal_pa'])
    conflict=aggregate is not None and aggregate<identified
    # Historical aggregate DOES NOT combine additively with formula-derived components.
    daily_total=calc['daily_total_pa']
    if aggregate is not None:
        daily_total=_s(aggregate) if not conflict else None
    return {'contract':CONTRACT,'source_class':spec['source_class'],'source_url':spec.get('source_url'),
            'components':calc['components'],'identified_daily_subtotal_pa':_s(identified),
            'daily_total_pa':daily_total,'daily_total_basis':('HISTORICO_LITERAL_AGREGADO' if aggregate is not None and not conflict else 'MESTRE_FIVE_RATES_SCOPE_CLOSED' if daily_total is not None else 'INDETERMINADO'),
            'historical_daily_pa':_s(aggregate),'historical_cost_conflict':conflict,
            'activation_costs':acts,'activation_total_pa':None, # not summed across independent abilities
            'maintenance_pa_turn':None, 'unresolved':calc['unresolved'],
            'approval_status':'TEST_ONLY_NO_CANONICAL_WRITE','native_qmc_accepted':False,
            'production_hold':True,'new_recipe_permitted':False,
            'decision_rates':RATES,
            'warnings':(['HISTORICO_MENOR_QUE_SUBTOTAL_TARIFADO'] if conflict else [])+
                        (['ESCOPO_NAO_FECHADO_OU_EFEITOS_SEM_TARIFA'] if calc['daily_total_pa'] is None else [])}

def budget(*,pa_total,committed_in_snapshot,already_includes_item_daily,quoted_item_daily,
           activations=None,already_debited_activation_ids=(),unknown_commitments=False):
    """Orçamento sem dupla subtração. COMMIT de item e cobrança diária DEBIT não são misturados.
    O resultado é cenário contábil TEST e não autorização de uso.
    """
    total=_n(pa_total,'PA Total'); committed=_n(committed_in_snapshot,'PA Comprometido')
    if committed>total:raise ValueError('comprometido superior ao total')
    if not isinstance(already_includes_item_daily,bool):raise ValueError('deve declarar se item já incluído')
    if not isinstance(unknown_commitments,bool):raise ValueError('unknown_commitments booleano')
    free=total-committed
    d=None if quoted_item_daily is None else _n(quoted_item_daily,'PA/dia item')
    if already_includes_item_daily and d is None: raise ValueError('compromisso de item sem valor verificável')
    charge=Decimal(0) if already_includes_item_daily else d
    known_after=None if charge is None or unknown_commitments else free-charge
    prior_debits=tuple(already_debited_activation_ids)
    debited_ids=set(prior_debits)
    if len(debited_ids)!=len(prior_debits):raise ValueError('IDs de débito anteriores duplicados')
    new_ids=set()
    activation_total=Decimal(0)
    for e in activations or []:
        if not isinstance(e,dict) or not e.get('event_id'):
            raise ValueError('evento de ativação sem ID')
        event=e['event_id']
        if event in new_ids:raise ValueError('evento duplicado na solicitação')
        new_ids.add(event)
        if event in debited_ids: continue  # idempotent: previously debited
        activation_total+=_n(e['pa'],'PA ativação')
    rem=None if known_after is None else known_after-activation_total
    return {'status':('INDETERMINADO_POR_CUSTOS_AUSENTES' if rem is None else 'INSUFICIENTE_NO_CENARIO' if rem<0 else 'COBERTURA_NUMERICA_TEST'),
            'pa_total':_s(total),'committed_in_snapshot':_s(committed),'pa_free_snapshot':_s(free),
            'item_already_in_committed':already_includes_item_daily,
            'additional_daily_commitment':_s(charge),'activation_new_debits':_s(activation_total),
            'pa_free_after_scenario':_s(rem) if rem is not None and rem>=0 else None,
            'shortfall':_s(-rem) if rem is not None and rem<0 else None,
            'unknown_commitments':unknown_commitments,'daily_model':'COMMIT_CENARIO_NAO_HOMOLOGADO',
            'item_use_authorized':False,'production_hold':True}

def r09_census(r09_zip):
    rows,gates,m=load_r09(r09_zip)
    # Existing R09 computation is the denominator authority, not a rescore.
    flag_fields=rows[0].keys()
    return {'rows':len(rows),'master':sum(r['origem']=='CATALOGO_MESTRE_INDEXADO' for r in rows),
            'mirror':sum(r['origem']=='PARTY_MESTRE_ESPELHO' for r in rows),
            'identified_at_least_one':m['n_precificavel_r09'],
            'unidentified':len(rows)-m['n_precificavel_r09'],
            'candidates':[correction_preview(x,r09_zip) for x in ('Mira Apurada','Manto de Proteção','Mobilidade')],
            'fields':list(flag_fields),'canonical_changes':0,'identity_and_origin_preserved':True}

def normalize(s):return ''.join(x for x in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(x))

def converse(query:str, *, history_state:dict|None=None):
    """Adaptador de consulta para cinco tarifas, usa estado e lookup históricos do R05 em vez de refazer catálogo."""
    state=history_state or consultor_pa_r05.initial()
    state,old=consultor_pa_r05.interpret(state,query)
    q=normalize(query)
    es=[]
    def add(k,n,**flags):es.append({'id':'fx'+str(len(es)),'kind':k,'magnitude':n,'mode':'PASSIVO_DIARIO',**flags})
    for m in re.finditer(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:em\s+|de\s+)?(?:forca|destreza|constituicao|inteligencia|sabedoria|carisma|for|des|con|int|sab|car)\b',q):
        add('ATRIBUTO_PERMANENTE',m.group(1).replace(',','.'),permanent_confirmed=bool(re.search(r'permanente|continuo|enquanto equipado',q)))
    for m in re.finditer(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:de\s+)?dano(?:\s+fixo)?',q):
        add('DANO_FIXO_ADICIONAL',m.group(1).replace(',','.'),damage_is_fixed=('fixo' in q and ('adicional' in q or 'acrescent' in q)),conditional=('critico' in q or 'uma vez' in q))
    for m in re.finditer(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:m|metros?)\b',q):
        add('DESLOCAMENTO_PERMANENTE_M',m.group(1).replace(',','.'),permanent_confirmed=('permanente' in q))
    for m in re.finditer(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:em\s+|no\s+|nos\s+)?(?:teste|jogadas?)\s+de\s+ataque',q):
        add('BONUS_TESTE_ATAQUE',m.group(1).replace(',','.'),is_attack_test=True)
    for m in re.finditer(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:de\s+|na\s+|em\s+)?ca\b',q):
        mag=m.group(1).replace(',','.')
        if 'estrutural' in q or 'fisica' in q: add('CA_ESTRUTURAL',mag)
        else:add('CA_MAGICA',mag,magical_origin_confirmed=('magica comprovada' in q or 'origem magica comprovada' in q))
    if 'rd' in q: add('RD',re.search(r'rd\s*(\d+)',q).group(1) if re.search(r'rd\s*(\d+)',q) else '1')
    spec={'source_class':'USER_EXPERIMENTAL_SPEC','effects':es,'all_effects_documented': bool(re.search(r'isolad[oa]|somente|apenas|unico efeito',q))}
    result=estimate(spec)
    if not es:
        historical=old['source_historical']
        result['historical_lookup_R05']=historical
        result['original_R05_response']=old['answer']
        if historical:
            day=(historical.get('pa_daily') or {}).get('value')
            ambiguous=bool(historical.get('R05_reconciliation'))
            result['historical_daily_pa']=day if not ambiguous else None
            result['historical_daily_status']=('MODALIDADE_INDETERMINADA' if ambiguous else
                                               'R05_LITERAL_HISTORICO_READONLY' if day is not None else 'INDETERMINADO')
            act=(historical.get('pa_activation') or {}).get('value')
            abilities=historical.get('activation_abilities') or []
            result['historical_activation_pa_values']=[a['value'] for a in abilities] if abilities else ([act] if act is not None else [])
            if day is not None and not ambiguous:
                result['daily_total_pa']=str(day)
                result['daily_total_basis']='HISTORICO_R05_SEM_RECOTACAO'
            result['source_url']=historical.get('url')
            result['historical_source_not_freshly_signed']=True
    return state,result

def craft_handoff(quote:dict, *, source_url=None, source_hash=None, authority='USER_EXPERIMENTAL_SPEC'):
    """Interop proposal for native vendor; SHA only ensures local byte integrity, NOT authenticity."""
    msg={'contract':'QMC-PA-INTERCHANGE-R11-PROPOSAL-TEST','producer':'PA-R05-EXISTING-ENGINE+R10-GUARD+R11-ADAPTER',
         'source_class':authority,'source_url':source_url,'source_sha256_excerpt_untrusted':source_hash,
         'daily_total_pa':quote['daily_total_pa'],'daily_subtotal_pa':quote['identified_daily_subtotal_pa'],
         'daily_total_basis':quote['daily_total_basis'],'activation_costs':quote['activation_costs'],
         'unresolved':quote['unresolved'],'warnings':quote['warnings'],
         'native_accepted':False,'notion_signed':False,'approval_status':'TEST_NO_RELEASE',
         'production_hold':True,'new_recipe_permitted':False,'master_only':True}
    digest=hashlib.sha256(json.dumps(msg,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return {'message':msg,'sha256_local':digest,'sender_validation':'PASS_LOCAL_ONLY','recipient_ack':None,
            'recipient_entrypoint':'QMC-02_EXISTENTE (CRAFT executor deve contratar)',
            'recipient_native_acceptance':'INTERFACE_EXTERNA_NAO_CONTRATADA'}
