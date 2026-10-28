"""R28 — QMC05 REAL entrypoint -> PA R27/R26 (MESTRE-SIDE TEST).

Consumes the actual qualified QMC05 `analyze` response. Every assertion about
source effects is grounded in the QMC05 normalized corpus, not a free-text mock.
Historical items NEVER receive new prospective prices or are written to Notion.
A separate, explicitly hypothetical design MAY get an E3 prospective scenario.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import sys
import re
from typing import Any

BASE = Path(__file__).resolve().parents[2] / 'provider_r27'
if not (BASE / 'ponte_pa_craft_r27.py').is_file():
    raise RuntimeError('PACOTE_PA_R27_REAL_AUSENTE: refusing counterfeit provider')
sys.path.insert(0, str(BASE))
from ponte_pa_craft_r27 import consultar_ficha_craft, ContractError, SCHEMA_VERSION  # noqa: E402

SCHEMA = 'QMC05-NATIVO-PA-R28/1.0.0-TEST'
FAMILIES = {
    'ARMA': 'arma', 'ARMADURA': 'armadura', 'ACESSORIO': 'acessório',
    'EQUIPAMENTO': 'equipamento', 'ARTEFATO': 'artefato',
    'INSCRICAO_ENCANTAMENTO': 'inscrição', 'CONSUMIVEL': 'consumível'
}
KNOWN_RANKS = {'Bronze','Prata','Ouro','Ouro Negro','Lendário'}


class R28ContractError(ValueError):
    pass


def _qualified(q: dict):
    if not isinstance(q, dict) or q.get('state') != 'QMC05_PARECER_DOCUMENTAL_TEST':
        raise R28ContractError('QMC05_NATIVO_NAO_QUALIFICOU_FONTE')
    core = q.get('qmc04', {})
    fx = q.get('structured_effects', {})
    if fx.get('status') != 'GROUNDING_APROVADO':
        raise R28ContractError('QMC05_GROUNDING_FALHOU')
    ident = core.get('identity', {})
    if fx.get('item_uuid') != ident.get('uuid'):
        raise R28ContractError('UUID_DIVERGENTE_QMC05')
    url = ident.get('url') or ''
    if 'party' in url.lower() or not re.fullmatch(r'https://app\.notion\.com/p/[0-9a-f]{32}', url):
        raise R28ContractError('FONTE_NAO_MESTRE_QMC05')
    if not core.get('readback', {}).get('complete_content_sha256'):
        raise R28ContractError('HASH_CONTEUDO_FONTE_AUSENTE')
    return core, ident, fx


def _mode(e:dict) -> str | None:
    typ=e.get('mode')
    if typ == 'PASSIVO_EXPLICITO': return 'PASSIVA'
    if typ in ('ATIVO_EXPLICITO','ATIVACAO_DESCRITA_MAS_ACAO_NAO_DEFINIDA'): return 'ATIVA'
    return None


def _label(e:dict)->str:
    s=e['literal'].strip()
    name=s.partition(':')[0].strip(' *') if ':' in s else ''
    if not name or len(name)>120 or name.startswith('+'):
        name='Efeito '+e['effect_id']
    return name+' ['+e['effect_id']+']'


def _documented_costs(q:dict)->dict:
    c=q.get('energy_exchange',{}).get('costs_documented',{})
    return {k:list(c.get(k) or []) for k in ('daily','activation','ambiguous')}


def _num_unique(entries:list)->int|None:
    if len(entries)!=1:return None
    x=entries[0].get('value')
    if type(x) is int and x>=0:return x
    return None


def _historic_wire(ident:dict, fx:dict, costs:dict)->tuple[dict,list]:
    # No ability with an undocumented active/passive mode is coerced.
    abilities=[];unmapped=[]
    for e in fx['effects']:
        m=_mode(e)
        if m is None:
            unmapped.append({'effect_id':e['effect_id'],'literal':e['literal'],
                'mode':e['mode'],'reason':'MODALIDADE_NAO_DOCUMENTADA_NAO_INFERIR'})
            continue
        abilities.append({'nome':_label(e), 'modalidade':m, 'descricao':e['literal'],
            'usos_no_dia':0,'duracao':e['duration'].get('literal'),
            'frequencia':e.get('frequency'), 'condicoes':e.get('conditions'),
            'custo_variavel':None})
    hist={}
    d=_num_unique(costs['daily']); a=_num_unique(costs['activation'])
    if d is not None:hist['pa_por_dia']=d
    if a is not None:hist['pa_por_ativacao']=a
    return {'acao':'CONSULTAR_PA_TEST','item':ident['title'],
        'familia':FAMILIES.get(ident.get('family'),'outro'),
        'rank_item':ident['rank'] if ident.get('rank') in KNOWN_RANKS else None,
        'historico':True,'habilidades':abilities,'bonus':[],
        'pa_historico':hist,'pesquisa':{}},unmapped


def _projection_wire(ident:dict,fx:dict,proposal:dict)->tuple[dict,list]:
    if not isinstance(proposal,dict):raise R28ContractError('PROJETO_NAO_OBJETO')
    if proposal.get('modo')!='PROJETO_E3_TEST':
        raise R28ContractError('PROJETO_SEM_SELO_EXPERIMENTAL')
    if proposal.get('fonte_qmc05_uuid') != ident['uuid']:
        raise R28ContractError('PROJETO_UUID_FONTE_DIVERGENTE')
    if proposal.get('rank_item') not in KNOWN_RANKS:
        raise R28ContractError('PROJETO_RANK_ITEM_AUSENTE')
    if proposal.get('item_novo') == ident['title']:
        raise R28ContractError('PROJETO_NAO_PODE_REPRECIFICAR_ORIGINAL')
    selected=proposal.get('efeitos_selecionados',[])
    if not isinstance(selected,list) or not selected or len(selected)>30:
        raise R28ContractError('PROJETO_DEVE_SELECIONAR_EFEITOS_REAIS')
    fx_map={e['effect_id']:e for e in fx['effects']}
    seen=set();abilities=[];research={};assumptions=[]
    for j,s in enumerate(selected):
        if not isinstance(s,dict):raise R28ContractError('SELECAO_INVALIDA')
        eid=s.get('effect_id')
        if eid in seen or eid not in fx_map:raise R28ContractError('EFEITO_NAO_ORIGINAL_OU_DUPLICADO')
        seen.add(eid);e=fx_map[eid];name=s.get('nome') or _label(e)
        mode=s.get('modalidade') or _mode(e)
        if mode not in ('ATIVA','PASSIVA'):
            raise R28ContractError('MODALIDADE_NAO_JUSTIFICADA')
        if _mode(e) and _mode(e)!=mode:
            raise R28ContractError('MODALIDADE_CONTRARIA_A_FONTE')
        if _mode(e) is None:
            assumptions.append('MODALIDADE_PROPOSTA_NAO_EXPLICITA:'+eid)
        uses=s.get('usos_no_dia',0)
        if type(uses)!=int or uses<0 or (mode=='PASSIVA' and uses):
            raise R28ContractError('USOS_INVALIDOS')
        research_input=s.get('pesquisa')
        if not isinstance(research_input,dict) or not research_input.get('comparadores'):
            raise R28ContractError('PESQUISA_COMPARATIVA_OBRIGATORIA')
        # A comparator's description can be E3, but must refer to a grounded URL.
        for comparison in research_input['comparadores']:
            url=comparison.get('url','') if isinstance(comparison,dict) else ''
            if not re.fullmatch(r'https://app\.notion\.com/p/[0-9a-f]{32}',url):
                raise R28ContractError('COMPARADOR_SEM_FONTE_NOTION')
        abilities.append({'nome':name,'modalidade':mode,'descricao':e['literal'],
            'usos_no_dia':uses,'duracao':e.get('duration',{}).get('literal'),
            'frequencia':e.get('frequency'), 'condicoes':e.get('conditions'),
            'custo_variavel':s.get('custo_variavel')})
        research[name]=research_input
        if e.get('duration',{}).get('status')=='NAO_DOCUMENTADA' and mode=='ATIVA':
            assumptions.append('DURACAO_ATIVA_NAO_DOCUMENTADA:'+eid)
    bonus=proposal.get('bonus_adicionais_propostos',[])
    if bonus:
        assumptions.append('BONUS_NOVO_FORA_DA_FONTE_COMPARADA_SOMENTE_TEST')
    wire={'acao':'CONSULTAR_PA_TEST','item':proposal['item_novo'],
        'familia':proposal.get('familia','outro'),
        'rank_item':proposal['rank_item'],'historico':False,
        'habilidades':abilities,'bonus':bonus,'pesquisa':research}
    return wire,assumptions


def integrar_qualificado(qmc05_output:dict,proposal:dict|None=None)->dict:
    """Real QMC05 output in, R27 external provider called, no Notion write.

    - `hist`: original item is never repriced, even if the R27 engine can quote it.
    - `scenario`: optional new proposed item with QMC05 effects as evidence;
      E3 is a decision proposal, never P4.
    """
    core,ident,fx=_qualified(qmc05_output)
    costs=_documented_costs(qmc05_output)
    hist,unmapped=_historic_wire(ident,fx,costs)
    legacy=consultar_ficha_craft(hist)  # REAL R27 -> R26, historical pricing blocked
    if legacy['custo_pa']['pa_por_dia'] is not None:
        raise R28ContractError('RETROPRECIFICACAO_INADMISSIVEL')
    result={'contrato':SCHEMA,'entrypoint':'QMC05_NATIVE_ENTRYPOINT_PATCH_TEST',
            'provider_contract':SCHEMA_VERSION,
            'call_chain':['qmc05.analyze[ORIGINAL]','qmc05.structured_effects[ORIGINAL]',
                          'pa_r28_native.integrar_qualificado','r27.consultar_ficha_craft',
                          'r26.avaliar'],
            'origem':{'uuid':ident['uuid'],'url':ident['url'],'titulo':ident['title'],
                      'rank_item_original':ident['rank'],'version_as_of':core['readback'].get('source_as_of'),
                      'source_sha256':core['readback']['complete_content_sha256'],
                      'effect_count':len(fx['effects']),'effects':[{'id':e['effect_id'],
                      'literal':e['literal'],'mode':e['mode'],'conditions':e.get('conditions',[]),
                      'duration':e.get('duration'),'documented_costs':e.get('pa_linked_to_same_sentence',[])}
                      for e in fx['effects']]},
            'historico':{'projecao_energetica':None,
                         'pa_documentado':costs,'r27':legacy['custo_pa'],
                         'efeitos_sem_modalidade':unmapped,
                         'alteracao_no_original':False},
            'cenario_novo':None,
            'governanca':{'mestre_side':True,'PARTY_WRITE':False,'primeiro_write':False,
                         'notion_write':False,'craft_f5':'RED_HOLD',
                         'writer_lease_epoch':None,'receitas_criadas':0,
                         'ps_nao_e_p4':True,'nac_pass_producao':'HOLD'}}
    if proposal is not None:
        wire,assumptions=_projection_wire(ident,fx,proposal)
        guess=consultar_ficha_craft(wire)
        result['cenario_novo']={'estado':'PARECER_SEMICANONICO_E3_TEST_NAO_HOMOLOGADO',
            'nunca_e_item_canonico':True,
            'origem_comparada_uuid':ident['uuid'],'assumptions':assumptions,
            'projetado':wire['item'],
            'r27_result':guess,
            'uso_material_permitido':False,
            'confidence_gate':'REVISAR_CONFORME_PR_SC_JIT_E_MESTRE',
            'observacao':'PA R27/R26 PROSPECTIVO; TERMO DE ATIVACAO HERDADO DE R27 SEM PROMOCAO PRODUTIVA'}
    return result


def output_json(qmc05_output:dict, proposal:dict|None=None)->str:
    return json.dumps(integrar_qualificado(qmc05_output,proposal),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
