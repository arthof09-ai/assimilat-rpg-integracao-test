"""IBX-17 R04: authoritative numeric interpretation, pure local reference.

Official die fixed 60%: ROUND TO NEAREST, d12=7 (NOT historical d12=8).
Source: Criação de Ficha Regra 5 / Transformação Espiritual T6/T6-B/T9-A;
new Mestre express 2026-10-09. NOT a Notion writer or Party permission.
"""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from typing import Any
from levelup_engine import InvalidPlan, DIE_LADDER, FIXED_60, die_for, rank_of
from layered_vital_v03 import validate_layers, damage_three_layers


def _int(v: Any, name: str, lowest: int = 0) -> int:
    if type(v) is not int or v < lowest:
        raise InvalidPlan(f"{name}: inteiro >= {lowest} obrigatório")
    return v


def fixed_die_value(die: int) -> int:
    if type(die) is not int or die not in FIXED_60:
        raise InvalidPlan('Dado fora da escada oficial')
    if FIXED_60[12] != 7:
        raise InvalidPlan('ERRO CRÍTICO: d12 oficial deve permanecer 7, nunca 8')
    return FIXED_60[die]


def progress_max(*, ordinal_level: int, initial_base: int, con_or_int_intrinsic: int,
                 die_shift: int = 0, transform: bool = False,
                 dice_mode: str = 'fixed_60', verified_rolls: list[int] | None = None,
                 permanent_extra: int = 0, source_id: str = '') -> dict[str,Any]:
    """Rebase at present classification, using n*(die+CON/INT)+starting max.

    The caller must separately reconcile initials, CON/INT, shifts and extras;
    this function does NOT claim that a given real character has been reconciled.
    No unverified dice rolls, flat guessing or old d12=8.
    """
    rank_of(ordinal_level)
    _int(initial_base, 'initial_base')
    _int(con_or_int_intrinsic, 'CON/INT intrinsic')
    _int(die_shift, 'die_shift')
    _int(permanent_extra, 'permanent_extra')
    if not isinstance(source_id,str) or not source_id.strip():
        raise InvalidPlan('Proveniência explícita dos componentes é obrigatória')
    if type(transform) is not bool:
        raise InvalidPlan('transform precisa ser bool')
    die=die_for(ordinal_level,die_shift+(1 if transform else 0))
    if dice_mode=='fixed_60':
        if verified_rolls is not None:
            raise InvalidPlan('Não combinar opção fixa e rolagens')
        faces=[fixed_die_value(die)]*ordinal_level
    elif dice_mode=='rolled':
        faces=verified_rolls
        if not isinstance(faces,list) or len(faces)!=ordinal_level or any(type(n) is not int or not 1<=n<=die for n in faces):
            raise InvalidPlan('Rolar requer todos os resultados e sua fonte, não os inventar')
    else:
        raise InvalidPlan('A opção deve ser fixed_60 ou rolled')
    total=initial_base + sum(faces) + ordinal_level*con_or_int_intrinsic + permanent_extra
    return {'status':'SIMULATED_FROM_EXPLICIT_COMPONENTS','source_id':source_id,
            'mode':dice_mode,'rank':rank_of(ordinal_level),'level':ordinal_level,
            'die':die,'die_fixed':fixed_die_value(die) if dice_mode=='fixed_60' else None,
            'initial_base':initial_base,'stat':con_or_int_intrinsic,
            'rolls':list(faces) if dice_mode=='rolled' else None,
            'permanent_extra':permanent_extra,'derived_max':total,'notion_write':False}


def extra_from_maxima(normal_vida_max: int, normal_alma_max: int,
                      spirit_vida_theoretical: int, spirit_alma_theoretical: int,
                      *, source_verified: bool) -> dict[str,Any]:
    for name,n in [('normal_vida_max',normal_vida_max),('normal_alma_max',normal_alma_max),
                   ('spirit_vida_theoretical',spirit_vida_theoretical),
                   ('spirit_alma_theoretical',spirit_alma_theoretical)]:
        _int(n,name)
    if source_verified is not True:
        raise InvalidPlan('Maximas e proveniência precisam ser reconciliadas')
    return {'vida_espiritual_temporaria':max(0,spirit_vida_theoretical-normal_vida_max),
            'alma_pa_adicional':max(0,spirit_alma_theoretical-normal_alma_max),
            'normal_vida_max':normal_vida_max,'normal_alma_max':normal_alma_max,
            'vida_teorica_transformada':spirit_vida_theoretical,
            'alma_teorica_transformada':spirit_alma_theoretical,
            'formula':'max(0, maximum_of_transformed_form - maximum_of_normal_form)',
            'not_from_beast_raw_health':True,'notion_write':False}


def compute_transform_bonus(*, ordinal_level: int, race_vida_shift: int, race_alma_shift: int,
                             initial_vida: int, initial_alma: int,
                             transformed_con: int, transformed_int: int,
                             normal_vida_max: int, normal_alma_max: int,
                             extras_vida: int = 0, extras_alma: int = 0,
                             verified_source_id: str, spirit_cap_level: int,
                             mode: str = 'fixed_60',
                             rolls_vida: list[int] | None = None,
                             rolls_alma: list[int] | None = None) -> dict[str,Any]:
    """Separate health and soul derivations, then subtract actual normal maxima.

    The existing normal maximum can contain *permanent* grants; temporary HP is
    explicitly never included. External bonuses must not be double counted.
    """
    rank_of(spirit_cap_level)
    if spirit_cap_level < ordinal_level:
        raise InvalidPlan("Espírito com teto abaixo do nível atual: T6 exige bônus comprovado; não extrapolar categoria superior")
    life=progress_max(ordinal_level=ordinal_level,initial_base=initial_vida,
                     con_or_int_intrinsic=transformed_con,die_shift=race_vida_shift,
                     transform=True,dice_mode=mode,verified_rolls=rolls_vida,
                     permanent_extra=extras_vida,source_id=verified_source_id+':VIDA')
    soul=progress_max(ordinal_level=ordinal_level,initial_base=initial_alma,
                     con_or_int_intrinsic=transformed_int,die_shift=race_alma_shift,
                     transform=True,dice_mode=mode,verified_rolls=rolls_alma,
                     permanent_extra=extras_alma,source_id=verified_source_id+':ALMA')
    delta=extra_from_maxima(normal_vida_max,normal_alma_max,
                            life['derived_max'],soul['derived_max'],source_verified=True)
    return {'normal_maxima':{'vida':normal_vida_max,'alma':normal_alma_max},
            'transform_calculation':{'vida':life,'alma':soul},'bonus':delta,
            'engine_status':'OFFLINE_CALCULATION_ONLY', 'notion_write':False}


def from_levelup_engine_preview(preview: dict[str,Any], *, evidence_reconciled: bool) -> dict[str,Any]:
    """Use per-level growth history of v01, avoiding retroactive rebases on same rank.

    The engine is preview-only. This function is not a certification of a real
    page; need a verified external snapshot before using its values in game.
    """
    if not isinstance(preview,dict) or preview.get('status')!='SIMULATED_PREVIEW_ONLY':
        raise InvalidPlan('Requer preview legítimo produzido pelo motor de evolução')
    normal=preview.get('normal')
    spirit=preview.get('transform')
    if not isinstance(normal,dict) or not isinstance(spirit,dict):
        raise InvalidPlan('Preview deve conter ficha normal e transformação')
    for key in ('Vida','Alma_PA_Total'):
        if key not in normal or key not in spirit:
            raise InvalidPlan('Máximos das duas formas ausentes')
    extra=extra_from_maxima(normal['Vida'],normal['Alma_PA_Total'],
                            spirit['Vida'],spirit['Alma_PA_Total'],
                            source_verified=evidence_reconciled)
    return {'delta':extra,'from_snapshot_sha256':preview.get('source_snapshot_sha256'),
            'evidence_required':'full_Notion_reopen_not_just_preview',
            'legacy_not_auto_corrected':True,'notion_write':False}


def validate_resource_state(state: dict[str,Any]) -> dict[str,Any]:
    """Physical and spiritual layers, total 5 reserves, separate current/max."""
    mandatory={'normal_current','normal_max','item_current','item_max',
               'spirit_current','spirit_max','transformed',
               'pa_normal_current','pa_normal_max','pa_spirit_current','pa_spirit_max'}
    if not isinstance(state,dict) or set(state)!=mandatory:
        raise InvalidPlan('Estado exige Vida normal/itens/transformada e PA normal/adicional, sem campos desconhecidos')
    hp=validate_layers({k:state[k] for k in ('normal_current','normal_max','item_current',
                                               'item_max','spirit_current','spirit_max','transformed')})
    out={**hp}
    for prefix in ('pa_normal','pa_spirit'):
        curr=_int(state[prefix+'_current'],prefix+'_current')
        cap=_int(state[prefix+'_max'],prefix+'_max')
        if curr>cap:
            raise InvalidPlan(f'{prefix} current > max')
        out[prefix+'_current']=curr;out[prefix+'_max']=cap
    if not out['transformed'] and out['pa_spirit_current']>0:
        raise InvalidPlan('PA de Espírito não pode estar ativo sem transformação')
    if not out['transformed'] and out['spirit_current']>0:
        raise InvalidPlan('Reserva de Vida de Espírito não pode estar ativa fora da forma')
    return out


def damage(state:dict[str,Any],amount:int)->dict[str,Any]:
    s=validate_resource_state(state)
    hp={k:s[k] for k in ('normal_current','normal_max','item_current','item_max',
                         'spirit_current','spirit_max','transformed')}
    x=damage_three_layers(hp,amount)
    return {'before':s,'after':{**s,**x['after']},'debit':x['debit'],
            'unabsorbed_damage':x['damage_unabsorbed_after_zero'],
            'notion_write':False}


def deactivate(state:dict[str,Any])->dict[str,Any]:
    s=validate_resource_state(state)
    if s['transformed'] is not True:
        raise InvalidPlan('Forma já desativada')
    out=deepcopy(s)
    out['transformed']=False
    out['spirit_current']=0
    out['pa_spirit_current']=0
    return {'before':s,'after':out,'lost_unspent_spiritual_hp':s['spirit_current'],
            'lost_unspent_spiritual_pa':s['pa_spirit_current'],
            'no_normal_heal':True,'notion_write':False}


def level_up_maxima(state:dict[str,Any],*,new_normal_vida_max:int,
                    new_normal_pa_max:int,new_item_max:int|None=None,
                    new_spirit_vida_max:int|None=None,
                    new_spirit_pa_max:int|None=None)->dict[str,Any]:
    """Never recharge a spent layer on level-up (including if form stays active)."""
    s=validate_resource_state(state)
    target={'normal_max':new_normal_vida_max,'pa_normal_max':new_normal_pa_max}
    if new_item_max is not None:target['item_max']=new_item_max
    if new_spirit_vida_max is not None:target['spirit_max']=new_spirit_vida_max
    if new_spirit_pa_max is not None:target['pa_spirit_max']=new_spirit_pa_max
    out=deepcopy(s)
    for k,amount in target.items():
        _int(amount,k)
        out[k]=amount
    for curr,cap in [('normal_current','normal_max'),('item_current','item_max'),
                     ('spirit_current','spirit_max'),('pa_normal_current','pa_normal_max'),
                     ('pa_spirit_current','pa_spirit_max')]:
        out[curr]=min(out[curr],out[cap])
    return {'before':s,'after':out,'refill_by_level':0,'notion_write':False}


def _last_event(events:list[dict[str,Any]])->dict[str,Any]|None:
    return events[-1] if events else None


def activate_verified(state: dict[str,Any], ledger: dict[str,Any], *,
                      actor_id:str,scene_id:str,event_id:str,spirit_id:str,
                      new_spirit_hp_max:int,new_spirit_pa_max:int,
                      verified_rest:dict[str,Any]|None=None,
                      activation_cost_paid_evidence:str,
                      provenance:str)->dict[str,Any]:
    """New full spirit reserves ONLY for new legally permitted activation.

    Gate material: ledger/truth of real scene, rest, cost and identity MUST be
    externally verified. This method can validate the supplied evidence's shape
    and replay, but cannot validate actual events in the game. Offline only.
    """
    s=validate_resource_state(state)
    if s['transformed']:
        raise InvalidPlan('É proibida segunda ativação enquanto transformação já ativa')
    for v,k in [(actor_id,'actor_id'),(scene_id,'scene_id'),(event_id,'event_id'),
                (spirit_id,'spirit_id'),(activation_cost_paid_evidence,'activation_cost_paid_evidence'),
                (provenance,'provenance')]:
        if not isinstance(v,str) or not v.strip():
            raise InvalidPlan(k+' ausente')
    _int(new_spirit_hp_max,'new_spirit_hp_max')
    _int(new_spirit_pa_max,'new_spirit_pa_max')
    if not isinstance(ledger,dict) or set(ledger)!={'actor_id','events'} or ledger['actor_id']!=actor_id:
        raise InvalidPlan('Actor ledger inválido ou outro ator')
    events=ledger['events']
    if not isinstance(events,list):
        raise InvalidPlan('Ledger eventos inválido')
    seen_scene=set();seen_event=set()
    for evt in events:
        if not isinstance(evt,dict) or not {'event_id','scene_id','seq','spirit_id'}<=set(evt):
            raise InvalidPlan('Ledger corrompido/incompleto')
        if evt['event_id'] in seen_event or evt['scene_id'] in seen_scene:
            raise InvalidPlan('Ledger inconsistente: ativação duplicada')
        seen_scene.add(evt['scene_id']);seen_event.add(evt['event_id'])
    if event_id in seen_event or scene_id in seen_scene:
        raise InvalidPlan('Replay ou segundo uso da mesma cena rejeitado')
    if any(type(evt['seq']) is not int or evt['seq']<1 or evt['seq']!=i+1 for i,evt in enumerate(events)):
        raise InvalidPlan('Sequência histórica de ativações corrompida')
    seq=len(events)+1
    if events:
        if not isinstance(verified_rest,dict) or set(verified_rest)!={'rest_id','kind','completed','verified','after_activation_seq','duration_hours'}:
            raise InvalidPlan('Nova cena exige evidência física de descanso concluído APÓS a última ativação')
        rest=verified_rest
        if not isinstance(rest['rest_id'],str) or not rest['rest_id'].strip() or rest['kind'] not in ('SHORT','LONG'):
            raise InvalidPlan('Descanso sem ID ou tipo')
        if rest['completed'] is not True or rest['verified'] is not True:
            raise InvalidPlan('Descanso não completado/verificado')
        if type(rest['after_activation_seq']) is not int or rest['after_activation_seq']!=events[-1]['seq']:
            raise InvalidPlan('Descanso não comprovado após último uso')
        try:hours=Decimal(str(rest['duration_hours']))
        except (InvalidOperation,ValueError):raise InvalidPlan('Duração do descanso inválida')
        if not hours.is_finite() or hours<0 or (rest['kind']=='SHORT' and not 4<=hours<=6):
            raise InvalidPlan('Descanso curto aproximadamente 4–6 h; descanso válido precisa conclusão real')
        if rest['rest_id'] in [evt.get('rest_id') for evt in events]:
            raise InvalidPlan('Descanso já utilizado/replay')
        rest_id=rest['rest_id']
    else:
        if verified_rest is not None:
            raise InvalidPlan('Primeira ativação não consome descanso do passado')
        rest_id=None
    out=deepcopy(s)
    out['transformed']=True
    out['spirit_max']=new_spirit_hp_max
    out['spirit_current']=new_spirit_hp_max
    out['pa_spirit_max']=new_spirit_pa_max
    out['pa_spirit_current']=new_spirit_pa_max
    event={'seq':seq,'event_id':event_id,'scene_id':scene_id,'spirit_id':spirit_id,
           'rest_id':rest_id,'source':provenance,'cost_evidence':activation_cost_paid_evidence,
           'refill_spiritual_hp':new_spirit_hp_max,'refill_spiritual_pa':new_spirit_pa_max}
    new_ledger={'actor_id':actor_id,'events':[deepcopy(z) for z in events]+[event]}
    return {'before':s,'after':out,'ledger':new_ledger,'event':event,
            'normal_vida_restored':0,'normal_pa_restored':0,'items_refilled':0,
            'status':'OFFLINE_VALIDATED_GATE_SHAPE_NOT_REAL_WORLD_REST_PROOF','notion_write':False}


def new_ledger(actor_id:str)->dict[str,Any]:
    if not isinstance(actor_id,str) or not actor_id.strip():
        raise InvalidPlan('actor_id obrigatório')
    return {'actor_id':actor_id,'events':[]}
