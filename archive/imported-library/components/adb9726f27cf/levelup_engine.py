"""LEVEL-UP-ENGINE v0.1, isolated Master-side reference prototype.

Pure planning only: no Notion calls, no writes to Party/O Primeiro, no live randomness.
Sources: IBX-17, Criação de Ficha, Sistema de Transformação Espiritual v1.0.
Design status: CANDIDATE / NOT CANONICAL IMPLEMENTATION.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any

ATTRS = ("FOR", "DES", "CON", "INT", "SAB", "CAR")
RANKS = ("Bronze", "Prata", "Ouro", "Ouro Negro", "Lendário")
DIE_LADDER = (6, 8, 10, 12, 20, 30, 40, 50, 60)
RACE = {
    "Humano": {"points": 2, "vida_shift": 0, "alma_shift": 0},
    "Orc": {"points": 5, "vida_shift": 2, "alma_shift": 0},
    "Abissiano": {"points": 5, "vida_shift": 0, "alma_shift": 2},
    "Asa Prateada": {"points": 4, "vida_shift": 0, "alma_shift": 1},
    "Raça Superior": {"points": 8, "vida_shift": 2, "alma_shift": 2},
}
FIXED_60 = {6: 4, 8: 5, 10: 6, 12: 7, 20: 12, 30: 18, 40: 24, 50: 30, 60: 36}


class InvalidPlan(ValueError):
    """Invalid or inconsistent input: never create a material write from this state."""


def fingerprint(obj: Any) -> str:
    return sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def rank_of(level: int) -> str:
    if type(level) is not int or not 1 <= level <= 25:
        raise InvalidPlan("Nível ordinal deve ser inteiro de 1 a 25")
    return RANKS[(level - 1) // 5]


def rank_index(level: int) -> int:
    rank_of(level)
    return (level - 1) // 5


def die_for(level: int, shift: int = 0) -> int:
    index = rank_index(level) + shift
    if index >= len(DIE_LADDER) or index < 0:
        raise InvalidPlan("Categoria de dado ultrapassa a escada definida")
    return DIE_LADDER[index]


def zeros() -> dict[str, int]:
    return {k: 0 for k in ATTRS}


def clean_attrs(obj: Any, where: str, *, allow_negative: bool = False) -> dict[str, int]:
    if not isinstance(obj, dict) or any(k not in ATTRS for k in obj):
        raise InvalidPlan(f"{where}: deve ser mapa de seis atributos válidos")
    out = zeros()
    for k, v in obj.items():
        if type(v) is not int or (v < 0 and not allow_negative):
            raise InvalidPlan(f"{where}.{k}: inteiro inválido")
        out[k] = v
    return out


def add_attrs(*layers: dict[str, int]) -> dict[str, int]:
    return {k: sum(layer[k] for layer in layers) for k in ATTRS}


def _require_int(v: Any, label: str, minimum: int | None = None) -> int:
    if type(v) is not int or (minimum is not None and v < minimum):
        raise InvalidPlan(f"{label}: inteiro inválido")
    return v


def _dice_value(die: int, track: str, level: int, event: str, request: dict[str, Any]) -> tuple[list[int], str]:
    """Explicitly fixed or externally supplied die faces; no hidden rolls."""
    policies = request.get("policies", {})
    policy = policies.get(track)
    if policy not in ("fixed", "rolled"):
        raise InvalidPlan(f"Política {track}: 'fixed' ou 'rolled' obrigatória")
    n = level if event == "rebase" else 1
    if policy == "fixed":
        return [FIXED_60[die]] * n, "fixed_60_percent"
    values = request.get("rolls", {}).get(str(level), {}).get(event, {}).get(track)
    if not isinstance(values, list) or len(values) != n or any(type(x) is not int or x < 1 or x > die for x in values):
        raise InvalidPlan(f"Rolagens explícitas inválidas: {track}, level={level}, {event}, d{die}, n={n}")
    return values, "explicit_rolls"


def _ca(race: str, a: dict[str, int], armor: int, ca_bonus: int) -> Fraction:
    if race == "Humano":
        return Fraction(6 + a["DES"] + armor + ca_bonus)
    if race == "Orc":
        return Fraction(12 + a["CON"] + armor + ca_bonus) + Fraction(a["DES"], 4)
    if race in ("Abissiano", "Asa Prateada"):
        return Fraction(9 + a["DES"] + armor + ca_bonus)
    if race == "Raça Superior":
        return Fraction(9 + armor + ca_bonus)
    raise InvalidPlan("Raça não suportada")


def _derived(race: str, a: dict[str, int], extras: dict[str, Any], vida: int, alma: int) -> dict[str, Any]:
    ff = (a["FOR"] + a["DES"] + a["CON"]) * 10
    ca = _ca(race, a, extras.get("armor", 0), extras.get("ca_bonus", 0))
    move = (Fraction(8) + Fraction(a["DES"], 4)) if race == "Raça Superior" else None
    return {
        "attributes": a,
        "FF": ff,
        "CA": int(ca) if ca.denominator == 1 else f"{ca.numerator}/{ca.denominator}",
        "CA_requires_rounding_decision": ca.denominator != 1,
        "CD_mágica": extras.get("proficiency_bonus", 0) + a["INT"] + extras.get("cd_bonus", 0),
        "Vida": vida,
        "Alma_PA_Total": alma,
        "PA_Livre_capacidade": alma - extras.get("pa_comprometido", 0),
        "Deslocamento_racial": None if move is None else (int(move) if move.denominator == 1 else f"{move.numerator}/{move.denominator}"),
    }


def _activate_ff_bonuses(derived: dict[str, Any], locks: dict[str, Any]) -> None:
    """Apply only actually active, historically locked milestones to each form."""
    damage = ca_bonus = vida_bonus = count = 0
    ff = derived["FF"]
    if ff < 0:
        raise InvalidPlan("FF negativa exige revisão da ficha")
    for threshold in range(100, ff + 1, 100):
        item = locks.get(str(threshold))
        if not item:
            raise InvalidPlan(f"FF ativa {threshold} sem lock histórico registrado")
        count += 1
        value = sum(item["faces"])
        if item["type"] == "Dano":
            damage += value
        elif item["type"] == "CA":
            ca_bonus += value
        else:
            vida_bonus += value
    derived["FF_marcos_ativos"] = count
    derived["FF_bonus_dano"] = damage
    derived["FF_bonus_CA"] = ca_bonus
    derived["FF_bonus_Vida"] = vida_bonus
    derived["Vida"] += vida_bonus
    ca = Fraction(derived["CA"]) + ca_bonus
    derived["CA"] = int(ca) if ca.denominator == 1 else f"{ca.numerator}/{ca.denominator}"



def _validate_locks(locks: dict[str, Any], high: int) -> None:
    for threshold in range(100, high + 1, 100):
        item = locks.get(str(threshold))
        if not item:
            raise InvalidPlan(f"Marco FF histórico {threshold} não documentado; não inventar/rolar de novo")
        if item.get("type") not in ("Dano", "CA", "Vida"):
            raise InvalidPlan(f"Marco FF {threshold}: escolha inválida")
        faces = item.get("faces")
        dice = 2 if item["type"] == "Vida" else 1
        sides = 6 if item["type"] == "Vida" else 4
        if not isinstance(faces, list) or len(faces) != dice or any(type(v) is not int or not 1 <= v <= sides for v in faces):
            raise InvalidPlan(f"Marco FF {threshold}: faces inválidas")


def _snapshot_validation(state: dict[str, Any]) -> None:
    if state.get("race") not in RACE:
        raise InvalidPlan("Raça fora das cinco definições da fonte")
    level = state.get("level")
    rank_of(level)
    _require_int(state.get("revision"), "revision", 0)
    if not isinstance(state.get("character_id"), str) or not state["character_id"]:
        raise InvalidPlan("ID do personagem obrigatório")
    for section in ("base", "permanent", "equipment", "temporary"):
        clean_attrs(state.get(section), section, allow_negative=(section == "temporary"))
    vital = state.get("vital", {})
    for term in ("vida_inicial", "alma_inicial"):
        _require_int(vital.get(term), term, 0)
    for term in ("vida_growth", "alma_growth"):
        arr = vital.get(term)
        if not isinstance(arr, list) or any(type(x) is not int or x < 0 for x in arr):
            raise InvalidPlan("Histórico de crescimento vital inválido")
        if len(arr) not in (level - 1, level):
            raise InvalidPlan(f"{term}: histórico não corresponde aos níveis conhecidos")
    extras = state.get("extras", {})
    for k in ("armor", "ca_bonus", "cd_bonus", "proficiency_bonus", "vida_extra", "alma_extra", "pa_comprometido"):
        _require_int(extras.get(k, 0), f"extras.{k}")
    _require_int(state.get("unspent_points", 0), "unspent_points", 0)
    _require_int(state.get("ff_high_watermark"), "ff_high_watermark", 0)
    _validate_locks(state.get("ff_locks", {}), state["ff_high_watermark"])
    grants = state.get("progression_grants", [])
    if not isinstance(grants, list) or len({g.get("id") for g in grants if isinstance(g, dict)}) != len(grants):
        raise InvalidPlan("Progressões adicionais: IDs únicos necessários")
    for grant in grants:
        if not isinstance(grant, dict) or not grant.get("id") or grant.get("credit_verified") is not True:
            raise InvalidPlan("Progressão adicional sem ID e crédito historicamente comprovado")
        _require_int(grant.get("points_per_level"), "Pontos por nível de título", 1)
        start = _require_int(grant.get("from_level"), "Início do título", 1)
        credited = _require_int(grant.get("credited_through"), "Último nível já creditado", 0)
        if start > 25 or credited > level:
            raise InvalidPlan("Histórico de título incompatível com nível atual")
    sp = state.get("spirit")
    if sp is not None:
        if not isinstance(sp, dict) or not sp.get("id"):
            raise InvalidPlan("Espírito identificado por ID obrigatório")
        _require_int(sp.get("bap"), "BAP Mestre-only", 0)
        _require_int(sp.get("cap"), "teto do Espírito", 1)
        if sp["cap"] > 25:
            raise InvalidPlan("Espírito acima do nível 25 exige norma específica")
        eff = min(level, sp["cap"])
        budget = sp["bap"] * eff // 2
        overlay = clean_attrs(sp.get("overlay", {}), "spirit.overlay")
        if sum(overlay.values()) > budget:
            raise InvalidPlan("Overlay atual excede orçamento de TAP")
        for term in ("vida_growth", "alma_growth"):
            arr = sp.get(term)
            if not isinstance(arr, list) or any(type(x) is not int or x < 0 for x in arr):
                raise InvalidPlan("Histórico vital transformado inválido")
        if not isinstance(sp.get("abilities", []), list) or not isinstance(sp.get("unlocked", []), list):
            raise InvalidPlan("Catálogo de habilidades do Espírito inválido")


def _get_attrs(state: dict[str, Any], scope: str, overlay: dict[str, int] | None = None) -> dict[str, int]:
    layers = [clean_attrs(state[k], k, allow_negative=(k == "temporary")) for k in ("base", "permanent", "equipment", "temporary")]
    if scope == "intrinsic":
        layers = layers[:1]
    elif scope == "intrinsic_permanent":
        layers = layers[:2]
    elif scope != "active":
        raise InvalidPlan("scope CON/INT requer intrinsic, intrinsic_permanent ou active; decisão não canônica")
    if overlay is not None:
        layers.append(overlay)
    return add_attrs(*layers)


def _changed(before: Any, after: Any) -> dict[str, Any]:
    if not isinstance(before, dict) or not isinstance(after, dict):
        return {} if before == after else {"before": before, "after": after}
    out = {}
    for k in before.keys() | after.keys():
        a, b = before.get(k), after.get(k)
        if a != b:
            out[k] = _changed(a, b)
    return out


def plan_level_up(snapshot: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Deterministic preview, no side effects. Raises InvalidPlan if a gate fails."""
    _snapshot_validation(snapshot)
    previous_hash = fingerprint(snapshot)
    before = deepcopy(snapshot)
    state = deepcopy(snapshot)
    target = request.get("target_level")
    rank_of(target)
    if not snapshot["level"] < target:
        raise InvalidPlan("Destino deve ser maior que nível atual")
    if request.get("expected_revision") != snapshot["revision"]:
        raise InvalidPlan("Fingerprint/revision da ficha divergente: REOPEN antes de tentar gravar")
    if request.get("expected_snapshot_hash") != previous_hash:
        raise InvalidPlan("Hash da ficha divergente: alteração concorrente ou baseline incorreta")
    growth_scope = request.get("growth_stat_scope")
    if growth_scope not in ("intrinsic", "intrinsic_permanent", "active"):
        raise InvalidPlan("É necessário decidir qual camada CON/INT entra na progressão; sem inferência")
    if request.get("spirit_id") != (snapshot.get("spirit") or {}).get("id"):
        raise InvalidPlan("Troca de Espírito requer operação de troca com ledger, não este level-up")
    original_normal = _get_attrs(state, "active")
    initial_extras = state.get("extras", {})
    orig_vital = state["vital"]
    before_normal = _derived(state["race"], original_normal, initial_extras,
                             orig_vital["vida_inicial"] + sum(orig_vital["vida_growth"]) + initial_extras.get("vida_extra", 0),
                             orig_vital["alma_inicial"] + sum(orig_vital["alma_growth"]) + initial_extras.get("alma_extra", 0))
    sp = state.get("spirit")
    before_transform = None
    if sp:
        old_o = clean_attrs(sp["overlay"], "spirit.overlay")
        old_stats = add_attrs(original_normal, old_o)
        sv = state["vital"]["vida_inicial"] + sum(sp["vida_growth"]) + initial_extras.get("vida_extra", 0)
        sa = state["vital"]["alma_inicial"] + sum(sp["alma_growth"]) + initial_extras.get("alma_extra", 0)
        before_transform = _derived(state["race"], old_stats, initial_extras,
                                    max(before_normal["Vida"], sv), max(before_normal["Alma_PA_Total"], sa))
    old_ff = max(before_normal["FF"], before_transform["FF"] if before_transform else 0)
    if snapshot["ff_high_watermark"] < old_ff:
        raise InvalidPlan("FF histórica máxima é inferior à FF da ficha atual; reconciliar ledger antes de evoluir")
    _activate_ff_bonuses(before_normal, snapshot["ff_locks"])
    if before_transform:
        _activate_ff_bonuses(before_transform, snapshot["ff_locks"])
    events = []
    unspent = state.get("unspent_points", 0)
    for grant in state.get("progression_grants", []):
        gap_start = max(grant["from_level"], grant["credited_through"] + 1)
        if gap_start <= snapshot["level"]:
            pending_retroactive = (snapshot["level"] - gap_start + 1) * grant["points_per_level"]
            unspent += pending_retroactive
            events.append({"kind": "previously_uncredited_retroactive_title", "source": grant["id"],
                           "from_level": gap_start, "through_level": snapshot["level"], "amount": pending_retroactive})
            grant["credited_through"] = snapshot["level"]
    for level in range(snapshot["level"] + 1, target + 1):
        preceding = level - 1
        title_points = 0
        for grant in state.get("progression_grants", []):
            if level >= grant["from_level"] and level > grant["credited_through"]:
                title_points += grant["points_per_level"]
                grant["credited_through"] = level
        unspent += RACE[state["race"]]["points"] + title_points
        allocation = clean_attrs(request.get("allocations", {}).get(str(level), {}), f"allocations.{level}")
        points = sum(allocation.values())
        if points > unspent:
            raise InvalidPlan(f"Nível {level}: gastou {points}, disponível {unspent}")
        unspent -= points
        state["base"] = add_attrs(state["base"], allocation)
        events.append({"level": level, "race_budget": RACE[state["race"]]["points"],
                       "verified_title_budget": title_points, "allocation": allocation, "unspent_after": unspent})
        a = _get_attrs(state, growth_scope)
        promoted = rank_index(level) != rank_index(preceding)
        event = "rebase" if promoted else "step"
        for kind, stat in (("vida", "CON"), ("alma", "INT")):
            shift = RACE[state["race"]][kind + "_shift"] + state.get("die_shifts", {}).get(kind, 0)
            die = die_for(level, shift)
            faces, mode = _dice_value(die, kind, level, event, request)
            increments = [v + a[stat] for v in faces]
            key = kind + "_growth"
            if promoted:
                events.append({"level": level, "kind": "rebase_" + kind, "old": state["vital"][key][:], "new": increments[:], "die": die, "mode": mode})
                state["vital"][key] = increments
            else:
                state["vital"][key].append(increments[0])
                events.append({"level": level, "kind": "gain_" + kind, "amount": increments[0], "die": die, "mode": mode})
        if sp:
            eff_old, eff_new = min(preceding, sp["cap"]), min(level, sp["cap"])
            if eff_new > eff_old:
                overlay_add = clean_attrs(request.get("spirit_allocations", {}).get(str(level), {}), f"spirit_allocations.{level}")
                new_budget = sp["bap"] * eff_new // 2
                remaining = new_budget - sum(sp["overlay"].values())
                if sum(overlay_add.values()) > remaining:
                    raise InvalidPlan(f"Nível {level}: alocação do TAP excede {remaining}")
                sp["overlay"] = add_attrs(sp["overlay"], overlay_add)
                events.append({"level": level, "kind": "TAP_allocation", "amount": sum(overlay_add.values()), "available": remaining,
                               "carry_fraction": (sp["bap"] * eff_new % 2) / 2})
                transformed_stats = _get_attrs(state, growth_scope, sp["overlay"])
                trans_promoted = rank_index(eff_new) != rank_index(eff_old)
                trans_event = "rebase" if trans_promoted else "step"
                for kind, stat in (("vida", "CON"), ("alma", "INT")):
                    shift = RACE[state["race"]][kind + "_shift"] + state.get("die_shifts", {}).get(kind, 0) + 1
                    die = die_for(eff_new, shift)
                    name = "transform_" + kind
                    faces, mode = _dice_value(die, name, level, trans_event, request)
                    increments = [v + transformed_stats[stat] for v in faces]
                    key = kind + "_growth"
                    if trans_promoted:
                        events.append({"level": level, "kind": "transform_rebase_" + kind, "old": sp[key][:], "new": increments[:], "die": die, "mode": mode})
                        sp[key] = increments
                    else:
                        sp[key].append(increments[0])
                        events.append({"level": level, "kind": "transform_gain_" + kind, "amount": increments[0], "die": die, "mode": mode})
    if unspent and not request.get("accept_unspent", False):
        raise InvalidPlan(f"Ainda existem {unspent} pontos de atributos sem distribuição; confirme retenção ou distribua")
    state["unspent_points"] = unspent
    state["level"] = target
    scope_a = _get_attrs(state, "active")
    vita = state["vital"]
    extras = state.get("extras", {})
    normal = _derived(state["race"], scope_a, extras,
                      vita["vida_inicial"] + sum(vita["vida_growth"]) + extras.get("vida_extra", 0),
                      vita["alma_inicial"] + sum(vita["alma_growth"]) + extras.get("alma_extra", 0))
    if normal["PA_Livre_capacidade"] < 0:
        raise InvalidPlan("PA comprometido excede novo PA total")
    transformed = None
    if sp:
        eff = min(target, sp["cap"])
        exact_budget = sp["bap"] * eff // 2
        if sum(sp["overlay"].values()) != exact_budget:
            raise InvalidPlan(f"TAP insuficientemente distribuído: {sum(sp['overlay'].values())}/{exact_budget}")
        trans_stats = _get_attrs(state, "active", sp["overlay"])
        trans_life = vita["vida_inicial"] + sum(sp["vida_growth"]) + extras.get("vida_extra", 0)
        trans_soul = vita["alma_inicial"] + sum(sp["alma_growth"]) + extras.get("alma_extra", 0)
        transformed = _derived(state["race"], trans_stats, extras,
                               max(normal["Vida"], trans_life), max(normal["Alma_PA_Total"], trans_soul))
        if transformed["PA_Livre_capacidade"] < 0:
            raise InvalidPlan("PA transformado comprometido excede PA transformado total")
        slots = rank_index(eff) + 1
        abilities = sp.get("abilities", [])
        current = sp.get("unlocked", [])
        if not set(current).issubset(abilities):
            raise InvalidPlan("Habilidades atuais não pertencem ao repertório documentado da Besta")
        chosen = request.get("new_abilities", [])
        if not isinstance(chosen, list) or len(chosen) != len(set(chosen)) or any(x not in abilities or x in current for x in chosen):
            raise InvalidPlan("Novas habilidades inválidas ou duplicadas")
        if len(current) + len(chosen) != min(slots, len(abilities)):
            raise InvalidPlan("Escolha as habilidades liberadas pela categoria efetiva; não inferir prioridade da lista")
        sp["unlocked"] += chosen
        sp["effective_level"] = eff
        sp["tap_carry_half"] = sp["bap"] * eff % 2
    if normal["CA_requires_rounding_decision"] or (transformed and transformed["CA_requires_rounding_decision"]):
        if request.get("fractional_ca_reviewed") is not True:
            raise InvalidPlan("CA fracionária: arredondamento não definido em fonte; requer decisão antes da gravação")
    old_high = state["ff_high_watermark"]
    new_high = max(old_high, normal["FF"], transformed["FF"] if transformed else 0)
    for threshold in range((old_high // 100 + 1) * 100, new_high + 1, 100):
        if str(threshold) in state["ff_locks"]:
            raise InvalidPlan(f"Marco {threshold} duplicado ou high-watermark histórico inconsistente")
        val = request.get("new_ff_locks", {}).get(str(threshold))
        if val is None:
            raise InvalidPlan(f"Marco FF {threshold} exige escolha Dano/CA/Vida e faces da rolagem; não sortear automaticamente")
        state["ff_locks"][str(threshold)] = deepcopy(val)
        events.append({"kind": "FF_lock_new", "threshold": threshold})
    state["ff_high_watermark"] = new_high
    _validate_locks(state["ff_locks"], new_high)
    _activate_ff_bonuses(normal, state["ff_locks"])
    if transformed:
        _activate_ff_bonuses(transformed, state["ff_locks"])
    state["revision"] += 1
    state.setdefault("events", []).append({"kind": "level_up_preview", "from": snapshot["level"], "to": target,
                                           "input_hash": previous_hash, "changes": events})
    changes = {"normal": _changed(before_normal, normal), "transform": _changed(before_transform, transformed)}
    return {
        "status": "SIMULATED_PREVIEW_ONLY",
        "source_snapshot_sha256": previous_hash,
        "proposal_sha256": fingerprint(state),
        "character_id": state["character_id"],
        "from": {"level": snapshot["level"], "rank": rank_of(snapshot["level"])},
        "to": {"level": target, "rank": rank_of(target)},
        "normal": normal,
        "transform": transformed,
        "changes": changes,
        "ff_new_locks": [x for x in state["ff_locks"] if int(x) > old_high],
        "growth_events": events,
        "unspent_points": unspent,
        "proposed_snapshot": state,
        "write_allowed": False,
        "warnings": ["PROTOTIPO: sem adapter físico, sem autorização Party e sem NAC-PASS da implementação",
                     "growth_stat_scope é decisão pendente de canonização; valores da simulação não provam a regra"],
    }


def player_safe_report(preview: dict[str, Any]) -> dict[str, Any]:
    """Explicit whitelist: BAP, formulas, bookkeeping, locks and secrets never exported."""
    n, t = preview["normal"], preview["transform"]
    before_after = preview["changes"]
    return {
        "result": "SIMULAÇÃO — ainda não atualizada no Notion",
        "nível_anterior": preview["from"]["level"],
        "novo_nível": preview["to"]["level"],
        "nova_classificação": preview["to"]["rank"],
        "atributos": n["attributes"],
        "Vida": n["Vida"],
        "Alma": n["Alma_PA_Total"],
        "PA_Livre_capacidade": n["PA_Livre_capacidade"],
        "CA": n["CA"],
        "FF": n["FF"],
        "CD_mágica": n["CD_mágica"],
        "bônus_dano_FF": n["FF_bonus_dano"],
        "transformação": None if not t else {
            "atributos": t["attributes"], "Vida": t["Vida"], "Alma": t["Alma_PA_Total"],
            "PA_Livre_capacidade": t["PA_Livre_capacidade"], "CA": t["CA"], "FF": t["FF"], "CD_mágica": t["CD_mágica"],
            "habilidades": preview["proposed_snapshot"]["spirit"]["unlocked"],
            "bônus_dano_FF": t["FF_bonus_dano"],
        },
        "mudanças_verificáveis_em_simulação": before_after,
        "pontos_normais_retidos": preview["unspent_points"],
    }
