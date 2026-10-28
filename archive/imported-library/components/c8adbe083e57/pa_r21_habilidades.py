"""PA R21 TEST: habilidades passivas/ativas por rank e custos de ativacao.

Uma extensão COMPATÍVEL com o motor R20 original; nenhuma ficha ou regra oficial escrita.
- Piso do item (R20) SEMPRE se aplica.
- Mestre decidiu: ativa paga floor(passiva/2) por dia, arredondado para baixo.
- Valor das tarifas PASSIVAS P[rank] AINDA PENDENTE; nunca inventar.
- Custos por ativacao sao um vetor distinto e historicos antigos nao sofrem mudanca.
- Rank de cada habilidade precisa ser classificado pelo Atlas, nao inferido do PA.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation, ROUND_FLOOR
from statistics import mean, median, multimode
from collections import Counter
from pa_r20_floor_atlas import FLOORS, RANKS, quote_new_item


def _nonnegative_num(x, name):
    if isinstance(x, bool): raise ValueError(name + ' booleano invalido')
    try: v=Decimal(str(x))
    except (TypeError, ValueError, InvalidOperation): raise ValueError(name + ' invalido')
    if not v.is_finite() or v<0: raise ValueError(name + ' negativo ou nao finito')
    return v


def fee(rank, mode, passive_fees):
    if rank not in FLOORS: raise ValueError('rank de HABILIDADE ausente ou invalido')
    if mode not in ('PASSIVA','ATIVA'):raise ValueError('tipo de habilidade invalido')
    if rank not in passive_fees or passive_fees[rank] is None:
        return None
    val=_nonnegative_num(passive_fees[rank], 'tarifa passiva '+rank)
    if val != val.to_integral_value(): raise ValueError('PA/dia das tarifas deve ser inteiro')
    return int(val if mode=='PASSIVA' else (val/2).to_integral_value(rounding=ROUND_FLOOR))


def quote_item_r21(*, item_rank, abilities, passive_fees=None, attributes=0,
                   fixed_damage=0, movement_m=0, attack_bonus=0, magical_ca=0,
                   other_daily_known=0, effects_complete=True, rank_evidence='E3',
                   strict_rank_gate=True):
    """Camada de habilidades sobre a quote R20: nao substitui o motor de origem.

    Habilidade: id, name, rank, mode, activation_cost (opcional para ATIVA), uses_today,
    rank_evidence (E0..E3), idempotency tokens para evitar usar duas vezes a mesma ativacao.
    Os campos magnitude no item nao repetem uma magnitude ja contabilizada em outra tarifa.
    """
    passive_fees = passive_fees or {}
    if item_rank not in FLOORS: raise ValueError('item_rank nao classificado')
    if not isinstance(abilities, list):raise ValueError('abilities deve ser lista')
    seen=set();charged_events=set();ability_cost_known=Decimal(0); activation_known=Decimal(0)
    unresolved_daily=[];unresolved_activation=[];warnings=[];rows=[]
    order={v:i for i,v in enumerate(RANKS)}
    for index, ability in enumerate(abilities):
        if not isinstance(ability,dict): raise ValueError('habilidade deve ser dict')
        ident=ability.get('id');rank=ability.get('rank');mode=ability.get('mode')
        if not ident or not isinstance(ident,str) or ident in seen:raise ValueError('ID de habilidade duplicado ou ausente')
        seen.add(ident)
        if rank not in FLOORS:raise ValueError('rank da habilidade obrigatorio')
        if order[rank]>order[item_rank]:
            if strict_rank_gate:raise ValueError('habilidade acima de rank do item: revisar Atlas')
            warnings.append('EFEITO_SUPERIOR_A_RI:'+ident)
        evidence=ability.get('rank_evidence','E3')
        if evidence not in ('E0','E1','E2','E3'): raise ValueError('evidencia de rank invalida')
        daily=fee(rank,mode,passive_fees)
        if daily is None:unresolved_daily.append(ident)
        else:ability_cost_known+=Decimal(daily)
        uses=ability.get('uses_today',0)
        if not isinstance(uses,int) or isinstance(uses,bool) or uses<0:raise ValueError('uses_today inteiro nao negativo')
        price=ability.get('activation_cost')
        if mode=='PASSIVA':
            if uses!=0 or price is not None or ability.get('activation_ids'):raise ValueError('passiva nao pode ter ativacao cobrada nesta modalidade')
            activation_today=0
        elif mode=='ATIVA':
            if price is None:
                unresolved_activation.append(ident)
                activation_today=None if uses>0 else 0
            else:
                pv=_nonnegative_num(price,'activation_cost')
                if pv != pv.to_integral_value():raise ValueError('PA/uso deve ser inteiro')
                activation_today=int(pv)*uses
                activation_known+=Decimal(activation_today)
            ids=ability.get('activation_ids')
            if ids is not None:
                if not isinstance(ids,list) or len(ids)!=uses or len(ids)!=len(set(ids)) or any(not isinstance(e,str) or not e for e in ids):
                    raise ValueError('activation_ids deve ser lista unica correspondente aos usos')
                if charged_events.intersection(ids):raise ValueError('mesma ativacao cobrada duas vezes')
                charged_events.update(ids)
        else:raise ValueError('tipo de habilidade desconhecido')
        rows.append({'id':ident,'name':ability.get('name',ident),'rank_da_habilidade':rank,
          'rank_evidence':evidence,'modalidade':mode,'passive_basis_for_rank':passive_fees.get(rank),
          'daily_fee_pa':daily,'activation_per_use_pa':price,'uses_today':uses,
          'activation_today_pa':activation_today})
    core=quote_new_item(rank=item_rank,attributes=attributes,fixed_damage=fixed_damage,
          movement_m=movement_m,attack_bonus=attack_bonus,magical_ca=magical_ca,
          other_daily_known=_nonnegative_num(other_daily_known,'other_daily_known')+ability_cost_known,
          effect_scope_closed=effects_complete and not unresolved_daily,
          rank_evidence=rank_evidence)
    current_total=None if unresolved_daily or not effects_complete else core['daily_total_pa_day']
    act_total=None if any(x['activation_today_pa'] is None for x in rows) else int(activation_known)
    combined=None if current_total is None or act_total is None else current_total+act_total
    return {'source_engine':'pa_r20_floor_atlas.quote_new_item','item_rank':item_rank,
      'floor_item_pa_day':FLOORS[item_rank],
      'passive_fees_are_defined':bool(passive_fees),
      'base_ability_fees_known_total_pa_day':int(ability_cost_known),
      'subtotal_identificado_com_habilidades_pa_day':core['identified_subtotal_pa_day'],
      'daily_lower_bound_pa':core['daily_lower_bound_pa'],
      'daily_total_pa_day':current_total,
      'activation_charges_today_known_pa':int(activation_known),
      'activation_total_today_pa':act_total,
      'total_today_pa':combined,
      'pending_daily_ability_ids':unresolved_daily,
      'pending_activation_tariff_ids':unresolved_activation,
      'ability_breakdown':rows,
      'warnings':warnings,
      'historical_repricing':False,
      'model_status':'TEST_LOCAL_TARIFAS_PASSIVAS_PENDENTES'}


def activation_summary(rows):
    if not rows:raise ValueError('sem observacoes')
    ids=[(r['item_uuid'],r['ability']) for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('habilidade duplicada na amostra')
    values=[int(r['activation_pa']) for r in rows]
    if any(v<0 for v in values):raise ValueError('valor negativo')
    counts=Counter(values)
    s60=[r for r in rows if int(r['activation_pa'])!=60]
    without=[int(r['activation_pa']) for r in s60]
    return {'abilities':len(rows), 'distinct_items':len(set(r['item_uuid'] for r in rows)),
      'min_pa':min(values),'max_pa':max(values),
      'mean_pa':round(mean(values),4),'median_pa':median(values),'mode_pa':multimode(values),
      'histogram':{str(k):v for k,v in sorted(counts.items())},
      'most_frequent_6pa_count':counts[6],
      'without_60':{'n':len(without),'min_pa':min(without),'max_pa':max(without),
                    'mean_pa':round(mean(without),4),'median_pa':median(without)},
      'rank_item_explicit_E0_count':sum(r['item_rank_status']=='E0_DOCUMENTAL' for r in rows),
      'rank_ability_E0_count':sum(r['ability_rank_evidence']=='E0' for r in rows),
      'limitations':['amostra intencional, nao censo global','rank da habilidade separado do item',
        'dados antigos apenas observacionais','custos por turno nao somados com custos por uso']}
