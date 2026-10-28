"""IBX-17 R03: THREE independent health layers; no Notion writes.

Master direction 2026-10-09: spiritual shielding > item shielding > normal HP.
The shield's *magnitude* comes from verified T6 in an authorized plan, never a
raw beast HP. The rule for REFILL at a later transformation is NOT fixed here.
"""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from typing import Any
from levelup_engine import InvalidPlan

FIELDS = ('normal_current','normal_max','item_current','item_max',
          'spirit_current','spirit_max','transformed')

def validate_layers(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict) or set(state) != set(FIELDS):
        raise InvalidPlan('Estado deve especificar exatamente 3 camadas atuais/máximas e transformed')
    ret=deepcopy(state)
    for prefix in ('normal','item','spirit'):
        now=ret[f'{prefix}_current']; cap=ret[f'{prefix}_max']
        if type(now) is not int or type(cap) is not int or min(now,cap)<0 or now>cap:
            raise InvalidPlan(f'Camada {prefix}: valores inteiros, não negativos e atual <= máximo')
    if type(ret['transformed']) is not bool:
        raise InvalidPlan('transformed deve ser booleano, nunca inferido de texto')
    return ret

def layer_display(state: dict[str, Any]) -> str:
    s=validate_layers(state)
    a=f"{s['normal_current']}/{s['normal_max']}"
    b=f"{s['item_current']}/{s['item_max']} itens"
    c=f"{s['spirit_current']}/{s['spirit_max']} transformação"
    return a+(' | '+c+' | '+b if s['transformed'] else ' | '+b+' | '+c+' (inativa)')

def damage_three_layers(state: dict[str, Any], damage: int) -> dict[str, Any]:
    """Returns audit before/after, consumed damage per layer, and overkill.

    Does not infer dead/dying thresholds or recovery at 0 HP.
    """
    s=validate_layers(state)
    if type(damage) is not int or damage<0:
        raise InvalidPlan('Dano inválido')
    after=deepcopy(s); remaining=damage
    debits={'spirit':0,'item':0,'normal':0}
    order=('spirit','item','normal') if s['transformed'] else ('item','normal')
    for name in order:
        key=f'{name}_current'
        d=min(after[key],remaining)
        after[key]-=d; debits[name]+=d; remaining-=d
    if sum(debits.values())+remaining!=damage:
        raise InvalidPlan('Falha de conservação de dano')
    return {'before':s,'after':after,'damage_requested':damage,
            'debit':debits,'damage_unabsorbed_after_zero':remaining,
            'priority':'spirit > item > normal' if s['transformed'] else 'item > normal',
            'healing':0,'notion_write':False}

def project_after_level(state: dict[str, Any], *, new_normal_max: int,
                        new_item_max: int|None=None, new_spirit_max: int|None=None) -> dict[str, Any]:
    """Level-up changes maxima ONLY; never refills any layer."""
    s=validate_layers(state); out=deepcopy(s)
    for name,requested in (('normal',new_normal_max),('item',new_item_max),('spirit',new_spirit_max)):
        if requested is None:
            continue
        if type(requested) is not int or requested<0:
            raise InvalidPlan(f'Novo máximo {name} inválido')
        out[f'{name}_max']=requested
        out[f'{name}_current']=min(s[f'{name}_current'],requested)
    return {'before':s,'after':out,'heal_on_level':0,'recharge_on_level':0,'notion_write':False}

def project_form_change(state: dict[str, Any], *, transformed: bool, external_gate_checked: bool) -> dict[str, Any]:
    """This only projects layer visibility: activation COST/scene/rest is external.

    Switching forms does not refresh a spent spirit shield. Whether a future,
    newly authorized activation grants a fresh shield requires Mestre ruling.
    """
    s=validate_layers(state)
    if type(transformed) is not bool or external_gate_checked is not True:
        raise InvalidPlan('Troca de forma exige gate externo T9-A verificado')
    out=deepcopy(s); out['transformed']=transformed
    return {'before':s,'after':out,'shield_granted':0,'healing':0,
            'recharge_policy':'PENDENTE_FOR_FUTURE_VALID_ACTIVATION','notion_write':False}

def candidate_spirit_shield_capacity(normal_derived_max: int,
                                     spirit_derived_max: int, *, t6_evidence: bool=False) -> dict[str, Any]:
    """Capacity is delta of two derived maxima; never use beast's raw HP.

    If an old sheet cannot be reconciled, no candidate shield is released for
    any real write, even if the numerical delta is positive.
    """
    if any(type(x) is not int or x<0 for x in (normal_derived_max,spirit_derived_max)):
        raise InvalidPlan('Máximos verificados inválidos')
    if spirit_derived_max<normal_derived_max:
        raise InvalidPlan('Vida transformada não pode violar o piso da forma normal')
    if not t6_evidence:
        raise InvalidPlan('T6 + dados/rank/proveniência e exceções precisam estar reconciliados')
    return {'shield_max_candidate':spirit_derived_max-normal_derived_max,
            'type':'SPIRIT_TEMP_SHIELD','not_bonuses_to_normal_current':True,
            'no_refresh_policy_inferred':True,'notion_write':False}


def _dec(value: Any, name: str) -> Decimal:
    if isinstance(value,bool) or value is None or isinstance(value,float):
        raise InvalidPlan(f'{name}: usar inteiro ou decimal exato em string')
    try:
        x=Decimal(str(value))
        if not x.is_finite() or x<0: raise InvalidPlan(f'{name}: valor não-negativo')
        return x
    except (InvalidOperation, ValueError):
        raise InvalidPlan(f'{name}: número inválido')

def validate_attribute_rate_confirmation(*, character_id: str,
                                         components: list[dict[str, Any]],
                                         player_confirmation: dict[str, Any]) -> dict[str, Any]:
    """Mandatory player validation even if a sheet lists points/level.

    Confirmation does NOT override canonical components: discrepancies HOLD.
    Separate normal points from spirit TAP and source-specific grants.
    """
    if not isinstance(character_id,str) or not character_id.strip():
        raise InvalidPlan('Character ID ausente')
    if not isinstance(components,list) or not components:
        raise InvalidPlan('Fontes verificadas de progressão normal ausentes')
    seen=set(); rate=Decimal(0); normalized=[]
    for c in components:
        if not isinstance(c,dict) or not {'source_id','points_per_level','physically_verified'} <= set(c):
            raise InvalidPlan('Fonte de atributo incompleta')
        src=c['source_id']
        if not isinstance(src,str) or not src.strip() or src in seen or c['physically_verified'] is not True:
            raise InvalidPlan('Fonte repetida, desconhecida ou não verificada')
        seen.add(src);p=_dec(c['points_per_level'],src)
        normalized.append({'source_id':src,'points_per_level':str(p),'retroactive':bool(c.get('retroactive',False))})
        rate+=p
    v=player_confirmation
    needed={'character_id','player_id','confirmed','confirmed_at','confirmed_points_per_level','statement','source'}
    if not isinstance(v,dict) or not needed<=set(v) or v['confirmed'] is not True or v['character_id'] != character_id:
        raise InvalidPlan('Pedir confirmação explícita à player, mesmo quando taxa está no Notion')
    for k in ('player_id','confirmed_at','statement','source'):
        if not isinstance(v[k],str) or not v[k].strip():
            raise InvalidPlan(f'Confirmação da player incompleta: {k}')
    actual=_dec(v['confirmed_points_per_level'],'player total')
    if actual!=rate:
        raise InvalidPlan(f'DIVERGÊNCIA: player declarou {actual}, fontes verificadas somam {rate}; reconciliar com Mestre')
    return {'status':'PLAYER_CONFIRMED_AND_CANON_SOURCES_AGREE',
            'character_id':character_id,'normal_points_per_level':str(rate),
            'sources':normalized,'player_confirmation':deepcopy(v),
            'spirit_tap_must_be_separate':True,'notion_write':False}

def mandatory_new_character_fields() -> dict[str,str]:
    return {'progression_normal_points_per_level':'OBRIGATÓRIO',
            'progression_base_racial_source':'OBRIGATÓRIO',
            'progression_titles_per_level_and_retroactivity':'OBRIGATÓRIO se aplicável',
            'progression_start_level':'OBRIGATÓRIO',
            'progression_spirit_tap':'SEPARADO/MESTRE-SIDE até projeção Party segura',
            'progression_player_confirmation':'OBRIGATÓRIO antes da primeira evolução de player',
            'progression_last_verified':'OBRIGATÓRIO'}
