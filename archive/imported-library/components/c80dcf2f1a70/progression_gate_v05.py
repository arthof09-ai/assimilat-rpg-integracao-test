"""Mestre's mandatory confirmation of attribute points/level before player evolution.

Does not contact or impersonate players. All evidence must be furnished by the
real player through an authorized channel and reconciled with canonical sources.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict

class ProgressionHold(ValueError):pass

@dataclass(frozen=True)
class RateComponent:
    kind:str
    points_per_level:float
    source:str
    first_valid_level:int=1
    retroactive:bool=False


ALLOWED={'racial','title','permanent_exception','other_verified'}

def prepare_rate_contract(*,character_id:str,player_character:bool,components:list[RateComponent],
                          current_level:int,player_response:dict|None=None,
                          gm_reconciliation_id:str|None=None)->dict:
    if not isinstance(character_id,str) or not character_id.strip():raise ProgressionHold('IDENTITY ausente')
    if type(player_character) is not bool:raise ProgressionHold('Tipo personagem inválido')
    if type(current_level) is not int or current_level<1:raise ProgressionHold('Nível inválido')
    if not isinstance(components,list) or not components:raise ProgressionHold('Sem composição de atributos por nível')
    serial=[];rate=0.0
    for c in components:
        if not isinstance(c,RateComponent) or c.kind not in ALLOWED or not c.source.strip():
            raise ProgressionHold('Fonte/tipo da parcela inválida')
        if c.points_per_level<0 or c.points_per_level>30 or c.first_valid_level<1:
            raise ProgressionHold('Parcela fora do limite')
        if c.first_valid_level>current_level and not c.retroactive:
            raise ProgressionHold('Fonte ainda não adquirida: não antecipar créditos')
        rate+=c.points_per_level
        serial.append(asdict(c))
    if rate%0.5!=0:raise ProgressionHold('Frações de pontos não previstas no contrato: reconciliação')
    status='CANON_RATE_CANDIDATE'
    proof=None
    if player_character:
        if not isinstance(player_response,dict):
            status='HOLD_AWAITING_DIRECT_PLAYER_CONFIRMATION'
        else:
            required={'character_id','total_per_level','evidence_ref','is_direct_player_reply'}
            if set(player_response)!=required or player_response['character_id']!=character_id or player_response['is_direct_player_reply'] is not True:
                raise ProgressionHold('Resposta direta e atribuível à própria player é obrigatória')
            if not isinstance(player_response['evidence_ref'],str) or len(player_response['evidence_ref'])<8:
                raise ProgressionHold('Evidência rastreável da player ausente')
            val=player_response['total_per_level']
            if type(val) not in (float,int) or val<0:
                raise ProgressionHold('Taxa informada inválida')
            proof=player_response['evidence_ref']
            if val!=rate:
                status='HOLD_CONFLICT_PLAYER_VS_SOURCES' if not gm_reconciliation_id else 'RECONCILIATION_PENDING_READBACK'
            else:
                status='RATE_CONFIRMED_BY_PLAYER_NEEDS_OPERATIONAL_AUTHORIZATION'
    return {'character_id':character_id,'current_level':current_level,
            'expected_total_per_level':rate,'component_sources':serial,'status':status,
            'player_evidence_ref':proof,'gemini_or_other_player_impersonation_allowed':False,
            'rate_is_spirit_TAP':False,'write_allowed':False}


def character_template_contract(*,character_id,components):
    """Authoring-time schema for each newly created character; no page creation."""
    x=prepare_rate_contract(character_id=character_id,player_character=False,components=components,current_level=1)
    return {'character_id':character_id,'field_label':'PONTOS DE ATRIBUTOS NORMAIS POR NÍVEL',
            'required':True,'total':x['expected_total_per_level'],
            'provenance':x['component_sources'],'separate_fields':['TAP do Espírito','títulos retroativos','pontos acumulados/livres'],
            'notion_write':False}
