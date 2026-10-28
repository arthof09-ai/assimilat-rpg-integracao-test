"""IBX-17, v0.2: read-only layer for current resources, pre-evolution save, transformed delta.

No Notion I/O; no canonical status or live writer. Master-side only.
"""
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any
import json
import re
from levelup_engine import InvalidPlan, plan_level_up, rank_of, fingerprint


RESOURCE_FIELDS = ("vida_atual", "vida_maxima", "pa_atual", "pa_capacidade", "vida_temp_atual", "vida_temp_maxima")


def validate_resource_state(state: dict[str, Any]) -> dict[str, int]:
    """Strict: do not read 'Vida 528+20' as current/max without a verified map."""
    if not isinstance(state, dict) or set(state) != set(RESOURCE_FIELDS):
        raise InvalidPlan("Resource state incompleto: exigir atuais e máximos verificados da ficha")
    for k in RESOURCE_FIELDS:
        if type(state[k]) is not int or state[k] < 0:
            raise InvalidPlan(f"{k}: inteiro não negativo obrigatório")
    if state["vida_atual"] > state["vida_maxima"] or state["pa_atual"] > state["pa_capacidade"]:
        raise InvalidPlan("Current > maximum; não escolher valor automaticamente")
    if state["vida_temp_atual"] > state["vida_temp_maxima"]:
        raise InvalidPlan("Vida temporária atual > máximo temporário")
    return deepcopy(state)


def projected_resources(old_resources: dict[str, Any], *, before_max_vida: int,
                        after_max_vida: int, before_pa_capacity: int, after_pa_capacity: int,
                        after_temp_max: int | None = None) -> dict[str, Any]:
    """Level-up changes capacities, never heals current HP/PA or spent temp HP."""
    state = validate_resource_state(old_resources)
    for name, amount, prior in (("vida", before_max_vida, state["vida_maxima"]),
                                ("pa", before_pa_capacity, state["pa_capacidade"])):
        if type(amount) is not int or amount != prior:
            raise InvalidPlan(f"{name} máximo anterior difere do snapshot: RECONCILIAR antes de planejar")
    if any(type(x) is not int or x < 0 for x in (after_max_vida, after_pa_capacity)):
        raise InvalidPlan("Novo máximo inválido")
    if after_temp_max is None:
        after_temp_max = state["vida_temp_maxima"]
    if type(after_temp_max) is not int or after_temp_max < 0:
        raise InvalidPlan("Novo máximo temporário inválido")
    result = deepcopy(state)
    result["vida_maxima"] = after_max_vida
    result["pa_capacidade"] = after_pa_capacity
    result["vida_temp_maxima"] = after_temp_max
    # Loss of capacity does not restore resources and cannot leave a current > max.
    result["vida_atual"] = min(result["vida_atual"], after_max_vida)
    result["pa_atual"] = min(result["pa_atual"], after_pa_capacity)
    result["vida_temp_atual"] = min(result["vida_temp_atual"], after_temp_max)
    return {"before": state, "after": result,
            "display": f"{result['vida_atual']}/{result['vida_maxima']} ({result['vida_temp_atual']}/{result['vida_temp_maxima']})",
            "pa_display": f"{result['pa_atual']}/{result['pa_capacidade']}",
            "healed_by_level": 0, "pa_restored_by_level": 0, "temp_recharged_by_level": 0}


def apply_damage_temporary_first(resources: dict[str, Any], damage: int) -> dict[str, int]:
    """Combat-rule implementation candidate: apply damage to temporary HP first."""
    r = validate_resource_state(resources)
    if type(damage) is not int or damage < 0:
        raise InvalidPlan("Dano inválido")
    consumed_temporary = min(r["vida_temp_atual"], damage)
    r["vida_temp_atual"] -= consumed_temporary
    residual = damage - consumed_temporary
    r["vida_atual"] = max(0, r["vida_atual"] - residual)
    return r


def candidate_temp_hp_from_equipment_con(con_equipment_delta: int, ordinal_level: int, *,
                                         rule_id: str | None = None) -> dict[str, Any]:
    """NOT official: +CON equipment × level, candidate requiring NAC-NORM approval.

    Does not assume the equipment itself heals or creates a current-value refill.
    """
    if rule_id != "PROPOSTA-CON-TEMP-POR-NIVEL":
        raise InvalidPlan("Fórmula de CON equipamento→Vida temporária ainda sem gate normativo")
    if type(con_equipment_delta) is not int or con_equipment_delta < 0:
        raise InvalidPlan("CON do equipamento inválida")
    rank_of(ordinal_level)
    return {"new_temp_hp_max_bonus": con_equipment_delta * ordinal_level,
            "rule_status": "PROPOSTA_MESTRE_PENDENTE_NAC_NORM",
            "formula": "positive_equipment_CON × ordinal_level",
            "not_canonical": True}


def generate_save_manifest(*, character_id: str, before_level: int, after_level: int,
                           notion_page_id: str, source_markup: str, event_id: str,
                           source_scope: str = "PLAYER_SHEET_PREIMAGE") -> dict[str, Any]:
    """Read-only guard for a full pre-evolution historical toggle, not an actual clone.

    The native Notion writer must prove the historical toggle is a lossless copy of all
    nested blocks and referenced content BEFORE touching original stats.
    """
    if not all(isinstance(x, str) and x.strip() for x in (character_id, notion_page_id, event_id, source_markup)):
        raise InvalidPlan("Manifesto exige IDs reais e exportação completa")
    rank_of(before_level)
    rank_of(after_level)
    if after_level <= before_level:
        raise InvalidPlan("Save pré-evolução exige destino maior")
    # No event stamp means a retry is not distinguishable from a second evolution.
    normalized_stamp = "SAVE-LEVEL-UP:" + event_id
    if normalized_stamp in source_markup:
        raise InvalidPlan("SAVE existente com EVENT-ID: verificar antes de repetir")
    image_refs = re.findall(r'!\[[^\]]*\]\([^\)]+\)', source_markup)
    child_links = re.findall(r'<page\s+url="([^"]+)"', source_markup)
    toggles = re.findall(r'<details\b', source_markup)
    # SHA is of the exact received preimage, not a reconstructed 'best effort' text.
    return {"status": "PRE_SAVE_READ_ONLY_PLAN", "write_allowed": False,
            "event_id": event_id, "stamp": normalized_stamp,
            "character_id": character_id, "page_id": notion_page_id,
            "from_level": before_level, "to_level": after_level,
            "save_location": "end_of_existing_player_character_page_as_native_toggle",
            "save_title": f"SAVE PRÉ-EVOLUÇÃO — {rank_of(before_level)} {((before_level-1)%5)+1} — {event_id}",
            "preimage_sha256": sha256(source_markup.encode("utf-8")).hexdigest(),
            "preimage_utf8_bytes": len(source_markup.encode("utf-8")),
            "native_toggles_count": len(toggles), "image_references": len(image_refs),
            "child_pages_referenced": len(child_links),
            "source_scope": source_scope,
            "required_writes": ["reopen source with fresh version fingerprint", "append FULL native-toggle historical copy in same page",
                                "readback verify identical nested content, attached media, child references and checksum",
                                "ONLY THEN alter current-level fields via minimal adapter touch-set",
                                "reopen/verify all changed fields & report"],
            "rollback": "STOP; restore from verified toggle/snapshot only with authorized writer and readback",
            "stop_conditions": ["clone incomplete", "undecodable rich content", "unresolved nested page ownership",
                                "collision/writer unclear", "Mestre-only leakage", "duplicate event_id"],
            "content_available_in_this_plan": False,
            "note": "A source hash does NOT itself prove a Notion toggle cloned the original; full native-block readback required."}


def transformed_bonus_from_preview(preview: dict[str, Any]) -> dict[str, Any]:
    """Compute delta from character's own transformed maximum, NOT beast raw HP/PA."""
    n, t = preview.get("normal"), preview.get("transform")
    if not n or not t:
        return {"status": "SEM_ESPIRITO", "vida_bonus": 0, "alma_bonus": 0}
    life = t["Vida"] - n["Vida"]
    soul = t["Alma_PA_Total"] - n["Alma_PA_Total"]
    if life < 0 or soul < 0:
        raise InvalidPlan("Transformação abaixo do piso normal")
    return {"status": "T6_DELTA_DO_ESTADO_TRANSFORMADO", "vida_bonus": life, "alma_bonus": soul,
            "normal_max_vida": n["Vida"], "transform_max_vida": t["Vida"],
            "normal_max_alma": n["Alma_PA_Total"], "transform_max_alma": t["Alma_PA_Total"],
            "method": "max(0, transformed_derived_max - normal_derived_max)",
            "not_method": "beast_raw_life_or_alma_minus_character_life_or_alma",
            "legacy_match_not_certified": True}


def plan_level_up_v02(snapshot: dict[str, Any], request: dict[str, Any], *,
                      resources: dict[str, Any], raw_page_markup: str,
                      notion_page_id: str, event_id: str) -> dict[str, Any]:
    """Read-only v0.2 orchestration; two phases planned, zero writes performed."""
    before_resource = validate_resource_state(resources)
    preview = plan_level_up(snapshot, request)
    old_normal = preview["normal"]
    old_vida = old_normal["Vida"]
    old_pa = old_normal["PA_Livre_capacidade"]
    # Reconstruct exact pre-level derived state with the normal engine, isolated.
    from levelup_engine import _get_attrs, _derived, _activate_ff_bonuses
    attrs_old = _get_attrs(snapshot, "active")
    v = snapshot["vital"]
    x = snapshot.get("extras", {})
    before = _derived(snapshot["race"], attrs_old, x,
                      v["vida_inicial"] + sum(v["vida_growth"]) + x.get("vida_extra", 0),
                      v["alma_inicial"] + sum(v["alma_growth"]) + x.get("alma_extra", 0))
    _activate_ff_bonuses(before, snapshot["ff_locks"])
    if before_resource["vida_maxima"] != before["Vida"] or before_resource["pa_capacidade"] != before["PA_Livre_capacidade"]:
        raise InvalidPlan("Recursos atuais não reconciliados com valores anteriores: não extrapolar fichas legadas")
    new_resource = projected_resources(before_resource, before_max_vida=before["Vida"],
                                       after_max_vida=old_vida,
                                       before_pa_capacity=before["PA_Livre_capacidade"],
                                       after_pa_capacity=old_pa)
    save = generate_save_manifest(character_id=snapshot["character_id"], before_level=snapshot["level"],
                                  after_level=request["target_level"], notion_page_id=notion_page_id,
                                  source_markup=raw_page_markup, event_id=event_id)
    return {"v01": preview, "resources": new_resource,
            "transformed_additions": transformed_bonus_from_preview(preview),
            "pre_evolution_save": save, "status": "SIMULATED_PREVIEW_ONLY",
            "write_allowed": False,
            "gates_open": {"snapshot_backed_up_in_real_toggle": False,
                           "native_blocks_readback": False,"NAC_NORM_temp_hp": False,
                           "Party_write_authorized": False,"adapter_verified": False},
            "warnings": ["Nunca editar ficha oficial antes do SAVE completo conferido em Notion",
                         "Recursos atuais preservados sem cura/restauração por level",
                         "Vida temporária via CON equipamento aguarda decisão normativa sobre fórmula e renovação"]}
