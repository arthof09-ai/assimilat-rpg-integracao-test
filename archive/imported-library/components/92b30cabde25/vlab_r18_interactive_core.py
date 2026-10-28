"""VLAB R18 experimental human-input adapter over the R17 pinned engine.

No alternate combat resolver is implemented. Native source/effect commits go
through UnifiedSyntheticGateway -> Stage11ManualBridge -> v0.8.1 executor.
The UI provides manual external turn declarations, fixture-only 1d6 rolls,
readback, local JSON journal, idempotency and a rollback-by-reconstruction path.
Never an authority for live characters, Notion, or terminal certifications.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from threading import RLock
import copy
import json
import os
import secrets
import uuid

from unified_gateway import UnifiedSyntheticGateway, verify_pins
from vlab_turn_runtime_v09plus_rebuilt import RebuiltManualRuntime
from vlab_effects_v08 import Scene, Combatant, COMBAT_PAGE
from vlab_action_catalog_v01 import AbilitySource, ActorActionState, FrozenRuleEvidence
from vlab_transformation_limit_v09_rebuilt import TransformationUseLedger
from vlab_rd_v08 import Resistances

SCHEMA = "VLAB-R18-HUMAN-COMBAT-EXPERIMENTAL-01"
PROVENANCE = "LAB-TEST-SYNTHETIC-NONCANON"
ACTORS = ("ED", "BE")

# The basic damage formula is a FIXTURE, not a certified character's attack.
# Initiative is SOURCE-RULE-DERIVED but with FIXED experimental dice, avoiding
# a rules decision for an initiative tie until the Mestre decides Q01.
SCENARIOS = {
    "BRONZE_TREINO": {
        "title": "Duelo Bronze — Treinamento",
        "description": "Dois combatentes fictícios. Ataque e dano simplificados; defesa oriunda do motor v0.8.1.",
        "actors": {
            "ED": {"name": "Sentinela Rubra (TESTE)", "hp": 36, "pa": 20, "des": 4, "for": 6, "luta": 3, "con": 4, "armor": 0, "fort": 2, "reflex": 3, "initiative_d6": 5, "damage_bonus": 5},
            "BE": {"name": "Guardião Azul (TESTE)", "hp": 36, "pa": 20, "des": 3, "for": 5, "luta": 3, "con": 3, "armor": 0, "fort": 2, "reflex": 3, "initiative_d6": 2, "damage_bonus": 5},
        },
    },
    "BRONZE_RESISTENCIA": {
        "title": "Duelo Bronze — Resistência",
        "description": "Mais Vida e dano menor; ideal para experimentar as duas reações defensivas.",
        "actors": {
            "ED": {"name": "Exploradora Âmbar (TESTE)", "hp": 54, "pa": 24, "des": 5, "for": 5, "luta": 3, "con": 4, "armor": 0, "fort": 3, "reflex": 4, "initiative_d6": 4, "damage_bonus": 3},
            "BE": {"name": "Batedor Cinza (TESTE)", "hp": 54, "pa": 24, "des": 3, "for": 6, "luta": 2, "con": 5, "armor": 0, "fort": 3, "reflex": 2, "initiative_d6": 2, "damage_bonus": 3},
        },
    },
}

class BattleHold(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(obj):
    return sha256(canonical(obj)).hexdigest()


def instant():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def proof_for(source):
    # An explicitly synthetic reference, never a source freeze or audit receipt.
    fake_source_digest = sha256((source.source_page_id + "|" + source.rule_id + "|LAB-R18-FIXTURE").encode()).hexdigest()
    return FrozenRuleEvidence(source.source_page_id, source.rule_id, fake_source_digest,
                              "LAB-FIXTURE-NOT-SOURCE-FREEZE", "MOCK-LAB-R18")


def source_attack():
    return AbilitySource("ATK", "attack", "STANDARD", COMBAT_PAGE, "ATK",
                         "LAB-ASSUMPTION", required_pa=0, target_scope="ENEMY",
                         effect_adapter_ready=True, effect_adapter_id="LAB-V081-R18-ATTACK")


def source_reaction():
    return AbilitySource("GUARD", "reaction", "REACTION", COMBAT_PAGE, "DEFENSE-TARGET",
                         "LAB-ASSUMPTION", required_pa=0, target_scope="SELF",
                         reaction_trigger="BEFORE-ATTACK", effect_adapter_ready=True,
                         effect_adapter_id="LAB-V081-R18-DEFENSE")


class Runner:
    """A new LAB-only runtime reconstructed from one bounded session ledger."""

    def __init__(self, session):
        verify_pins()  # historical engine and authority gate integrity
        self.session_id = session["session_id"]
        self.scenario = copy.deepcopy(SCENARIOS[session["scenario"]])
        scene_id = "LAB-R18-" + self.session_id
        actors = {}
        for who, data in self.scenario["actors"].items():
            ca = 6 + data["des"] + data["armor"]  # Humano CA rule in Sistema de Combate
            actors[who] = Combatant(who, data["hp"], data["pa"], Fraction(ca),
                                    data["con"], data["armor"], data["fort"],
                                    data["reflex"], "ZONA-" + who, rank="Bronze")
        scene = Scene(actors)
        ledger = TransformationUseLedger(test_fixture_authorized=True)
        for who in ACTORS:
            ledger.register(who)
        self.runtime = RebuiltManualRuntime(scene=scene, ledger=ledger, scene_id=scene_id,
                                             test_fixture_authorized=True)
        self.gateway = UnifiedSyntheticGateway(self.runtime, test_only=True)
        self.attack_spec = source_attack()
        self.defense_spec = source_reaction()
        self.active_count = 0
        self.records = []
        totals = {who: item["des"] + item["initiative_d6"]
                  for who, item in self.scenario["actors"].items()}
        if totals["ED"] == totals["BE"]:
            raise BattleHold("INITIATIVE_TIE_RULE_NOT_APPROVED")
        self.initiative = {"formula": "Bronze: 1d6 + DES + bônus de Iniciativa",
                           "bonus": 0, "dice_classification": "FIXTURE_PREDECLARED_NOT_LIVE_RNG",
                           "rolls": {who: self.scenario["actors"][who]["initiative_d6"] for who in ACTORS},
                           "scores": totals}
        self.order = tuple(sorted(ACTORS, key=lambda x: totals[x], reverse=True))
        self.initial = self.actors_state()

    def actors_state(self):
        result = {}
        for who in ACTORS:
            actor = self.runtime.scene.actors[who]
            data = self.scenario["actors"][who]
            result[who] = {
                "name": data["name"], "hp": actor.hp, "max_hp": data["hp"],
                "pa": actor.pa, "max_pa": data["pa"], "ca": str(actor.ca),
                "for": data["for"], "des": data["des"], "con": data["con"],
                "luta": data["luta"], "fortitude": data["fort"], "reflexo": data["reflex"],
                "standard": actor.standard, "movement": actor.movement,
                "reaction": actor.reaction, "position": actor.position,
                "classification": actor.rank, "provenance": "LAB-FIXTURE-NOT-CHARACTER",
            }
        return result

    def frame(self, actor_id, turn_id):
        actor = self.runtime.scene.actors[actor_id]
        return {
            "actor_id": "LAB-" + actor_id, "scene_id": self.runtime.scene_id,
            "turn_id": turn_id, "external_turn_authority": "LAB-R18-MANUAL-FIXTURE",
            "reaction_slot": "READY" if actor.reaction == 1 else "SPENT",
            "reaction_window": "BEFORE-ATTACK", "equipment_fixture": "EXPLICIT_TEST_ONLY",
            "pa_fixture": actor.pa, "current_turn_start_confirmed": True,
            "origin": PROVENANCE,
        }

    def state_for(self, who, source, is_reaction=False):
        actor = self.runtime.scene.actors[who]
        return ActorActionState(
            actor_id=who, ordinal_level=1, available_pa=actor.pa,
            known_action_ids=(source.action_id,), standard_available=actor.standard == 1,
            movement_available=actor.movement == 1, reaction_available=actor.reaction == 1,
            range_confirmed=True, los_confirmed=True, geometry_confirmed=True,
            environment_contract=True,
            reaction_trigger_observed="BEFORE-ATTACK" if is_reaction else None,
            enemy_ids_visible=tuple(x for x in ACTORS if x != who),
        )

    def winner(self):
        dead = [w for w in ACTORS if self.runtime.scene.actors[w].hp <= 0]
        if not dead:
            return None
        return next(w for w in ACTORS if w not in dead)

    def apply(self, choice):
        """Execute one selected turn in the EXISTING historical source/effect engine."""
        if self.winner() is not None:
            raise BattleHold("EXPERIMENTAL_BATTLE_ALREADY_FINISHED")
        kind = choice["action"]
        if kind not in ("ATTACK", "PASS"):
            raise BattleHold("ACTION_NOT_IMPLEMENTED_IN_R18_ADAPTER")
        who = self.order[self.active_count % 2]
        other = next(x for x in ACTORS if x != who)
        if choice.get("target") != other:
            raise BattleHold("INVALID_OR_WRONG_TARGET")
        if kind == "PASS" and choice.get("reaction", "NONE") != "NONE":
            raise BattleHold("PASS_CANNOT_DECLARE_DEFENDER_REACTION")
        turn = self.active_count + 1
        turn_id = f"LAB-R18-TURN-{turn:04d}"
        start = self.actors_state()
        self.runtime.manual_turn_budget_reset(actor_id=who, turn_id=turn_id,
            external_authority_ref="LAB-R18-HUMAN-TURN-DECLARATION",
            standard=1, movement=1, reaction=1, strict=False)
        receipt = None
        if kind == "ATTACK":
            rolls = choice.get("rolls")
            if (not isinstance(rolls, dict) or set(rolls) != {"attack_d6", "damage_d6"}
                or any(type(v) != int or not 1 <= v <= 6 for v in rolls.values())):
                raise BattleHold("EXPLICIT_AUDITABLE_1D6_ROLLS_REQUIRED")
            reaction = choice.get("reaction", "NONE")
            if reaction not in ("NONE", "DEFENDER", "ESQUIVAR"):
                raise BattleHold("UNKNOWN_DEFENSIVE_REACTION")
            attacker_data = self.scenario["actors"][who]
            score = rolls["attack_d6"] + attacker_data["for"] + attacker_data["luta"]
            raw_damage = rolls["damage_d6"] + attacker_data["damage_bonus"]
            payload = {"roll_score": score, "damage": raw_damage,
                       "damage_tag": "cortante", "rd": Resistances(general=0)}
            event_id = "LAB-EVT-R18-" + choice["request_id"]
            if reaction != "NONE":
                if self.runtime.scene.actors[other].reaction != 1:
                    raise BattleHold("DEFENDER_REACTION_ALREADY_SPENT")
                effect = self.gateway.attack_with_defense(
                    event_id=event_id, attacker_id=who, defender_id=other,
                    attacker_frame=self.frame(who, turn_id),
                    defender_frame=self.frame(other, turn_id),
                    attack_source=self.attack_spec, defense_source=self.defense_spec,
                    attack_state=self.state_for(who, self.attack_spec),
                    defense_state=self.state_for(other, self.defense_spec, True),
                    attack_proofs=(proof_for(self.attack_spec),),
                    defense_proofs=(proof_for(self.defense_spec),),
                    attack_payload=payload, defense_kind=reaction,
                    announced_before=True, trigger_source="BEFORE-ATTACK", strict=False)
            else:
                effect = self.gateway.action(
                    event_id=event_id, actor_id=who, frame=self.frame(who, turn_id),
                    action_id="ATK:" + other, sources=(self.attack_spec,),
                    state=self.state_for(who, self.attack_spec),
                    proofs=(proof_for(self.attack_spec),), payload=payload,
                    manual_turn_start=True, strict=False)
            native = effect["engine_result"]["result"]["effect_event"] if reaction != "NONE" else effect["engine_result"]["result"]["effect_event"]
            receipt = {
                "attack_roll": f"1d6({rolls['attack_d6']}) + FOR {attacker_data['for']} + Luta {attacker_data['luta']} = {score}",
                "damage_roll_fixture": f"1d6({rolls['damage_d6']}) + {attacker_data['damage_bonus']} = {raw_damage}",
                "attack_result": native["attack"] if reaction != "NONE" else native,
                "defense_result": native["reaction"] if reaction != "NONE" else None,
                "gateway_event_sha256": effect["audit"]["sha256"],
                "native_engine_chain_sha256": effect["audit"]["engine_chain"],
                "source": "V081_HISTORIC_NATIVE_EFFECTS_VIA_R17_UNIFIED_SYNTHETIC_GATEWAY",
            }
        else:
            receipt = {"source": "MANUAL_EXTERNAL_TURN_PASS_NO_NATIVE_DAMAGE",
                       "native_engine_chain_sha256": self.runtime.trace[-1]["chain_hash"],
                       "attack_result": None, "defense_result": None}
        self.active_count += 1
        if not self.runtime.validate_trace():
            raise BattleHold("HISTORICAL_ENGINE_TRACE_INVALID")
        checkpoint = self.gateway.checkpoint()
        row = {
            "index": self.active_count, "turn": turn, "turn_id": turn_id,
            "actor_id": who, "target_id": other, "action": kind,
            "reaction": choice.get("reaction", "NONE"),
            "rolls": choice.get("rolls"), "request_id": choice["request_id"],
            "before": start, "after": self.actors_state(), "receipt": receipt,
            "gateway_sha256": checkpoint["sha256"],
            "engine_chain_sha256": checkpoint["engine_tail"],
            "winner": self.winner(),
        }
        row["row_sha256"] = digest(row)
        self.records.append(row)
        return row

    def view(self, session):
        who = self.order[self.active_count % 2] if not self.winner() else None
        next_target = next((w for w in ACTORS if w != who), None) if who else None
        return {
            "schema": SCHEMA, "session_id": self.session_id,
            "scenario_key": session["scenario"],
            "scenario": self.scenario["title"], "description": self.scenario["description"],
            "source_status": "LAB_FIXTURE_ONLY_NOT_STRICT_NOT_CANON",
            "actors": self.actors_state(), "initial_state": self.initial,
            "initiative": self.initiative, "order": list(self.order),
            "turn_number": self.active_count + 1, "active_actor": who,
            "next_target": next_target, "winner": self.winner(),
            "status": "FINISHED_EXPERIMENTAL_HP0" if self.winner() else "ACTIVE_EXPERIMENTAL",
            "events": self.records, "actions_available": ["ATTACK", "PASS"] if who else [],
            "reaction_options": ["NONE", "DEFENDER", "ESQUIVAR"] if who and self.runtime.scene.actors[next_target].reaction else ["NONE"],
            "history_entries_total": len(session["decisions"]),
            "active_events": self.active_count,
            "void_events": session.get("void_events", []),
            "engine_audit": self.gateway.checkpoint(),
            "source_pages": {"combat": COMBAT_PAGE},
            "limitations": [
                "Atores, Vida, Alma e dano são fixtures; nenhum PC/NPC real.",
                "A iniciativa usa dados de cenário fixados para evitar empate não regulamentado.",
                "Ação de ataque calculada como Bronze 1d6+FOR+Luta; dano 1d6+bônus é fixture, não certificado.",
                "DEFENDER/ESQUIVAR v0.8.1 não têm custo universal presumido de 5 PA.",
                "Ausência de efeitos de duração, movimento e magias no primeiro cenário.",
                "HP 0 encerra somente esta fixture; não adjudica morte/cânone.",
                "Recuperação é local e reexecuta apenas a simulação isolada de origem.",
                "0/17 contratos terminais; gateway de produção permanece HOLD.",
            ],
        }


class BattleService:
    """Portable JSON journal + deterministic bounded replay; no external effect path."""

    def __init__(self, data_dir):
        self.dir = Path(data_dir).expanduser().resolve()
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "sessions").mkdir(exist_ok=True)
        self.lock = RLock()
        self.session = None
        self.runner = None
        marker = self.dir / "active.json"
        if marker.exists():
            try:
                current = json.loads(marker.read_text(encoding="utf-8"))
                if current.get("schema") != SCHEMA:
                    raise BattleHold("ACTIVE_MARKER_INVALID")
                self._restore(current["session_id"])
            except Exception as e:
                # Fail closed on unknown/tampered state; do not silently reset it.
                raise BattleHold("RECOVERY_HOLD_INSPECT_DATA_DIRECTORY:" + str(e)) from e
        else:
            self.new("BRONZE_TREINO")

    def _path(self, session_id):
        if not isinstance(session_id, str) or len(session_id) != 32 or not all(c in "0123456789abcdef" for c in session_id):
            raise BattleHold("SESSION_ID_INVALID")
        return self.dir / "sessions" / (session_id + ".json")

    @staticmethod
    def _atomic(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name("." + path.name + "." + uuid.uuid4().hex + ".tmp")
        with open(temporary, "wb") as file:
            file.write(canonical(data) + b"\n")
            file.flush(); os.fsync(file.fileno())
        os.replace(temporary, path)
        try:
            fd = os.open(str(path.parent), os.O_RDONLY)
            try: os.fsync(fd)
            finally: os.close(fd)
        except OSError:
            pass

    def _sealed(self, session):
        return {**session, "sha256": digest(session)}

    def _load(self, path):
        obj = json.loads(path.read_text(encoding="utf-8"))
        seal = obj.pop("sha256", None)
        if not seal or seal != digest(obj):
            raise BattleHold("JOURNAL_INTEGRITY_MISMATCH")
        return obj

    def _replay(self, session):
        runner = Runner(session)
        for entry in session["decisions"]:
            if entry.get("voided", False):
                continue
            if entry["choice"]["request_id"] != entry["request_id"]:
                raise BattleHold("REQUEST_ID_BINDING_MISMATCH")
            got = runner.apply(entry["choice"])
            if got["row_sha256"] != entry["row_sha256"]:
                raise BattleHold("JOURNAL_NATIVE_EFFECT_REPLAY_DIVERGENCE")
        return runner

    def _restore(self, session_id):
        stored = self._load(self._path(session_id))
        if stored.get("schema") != SCHEMA or stored["session_id"] != session_id or stored["scenario"] not in SCENARIOS:
            raise BattleHold("SESSION_SCHEMA_OR_SCENARIO_INVALID")
        runner = self._replay(stored)
        self.session, self.runner = stored, runner
        return self.view()

    def new(self, scenario):
        with self.lock:
            if scenario not in SCENARIOS:
                raise BattleHold("SCENARIO_NOT_FOUND")
            sid = uuid.uuid4().hex
            session = {"schema": SCHEMA, "session_id": sid, "scenario": scenario,
                       "created_at": instant(), "decisions": [], "void_events": [], "undo_requests": []}
            runner = Runner(session)
            self._atomic(self._path(sid), self._sealed(session))
            self._atomic(self.dir / "active.json", {"schema": SCHEMA, "session_id": sid})
            self.session, self.runner = session, runner
            return self.view()

    def view(self):
        with self.lock:
            result = self.runner.view(self.session)
            result["available_scenarios"] = [
                {"key": key, "title": value["title"], "description": value["description"]}
                for key, value in SCENARIOS.items()]
            return result

    def act(self, request):
        with self.lock:
            if not isinstance(request, dict):
                raise BattleHold("ACTION_OBJECT_REQUIRED")
            if set(request) - {"request_id", "action", "reaction", "target"}:
                raise BattleHold("UNKNOWN_ACTION_FIELDS")
            rid = request.get("request_id")
            if (not isinstance(rid, str) or not 8 <= len(rid) <= 120
                or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in rid)):
                raise BattleHold("REQUEST_ID_INVALID")
            prior = next((x for x in self.session["decisions"] if x["request_id"] == rid), None)
            normalized = {"request_id": rid, "action": request.get("action"),
                          "reaction": request.get("reaction", "NONE"), "target": request.get("target")}
            if prior is not None:
                submitted = {k:v for k,v in prior["choice"].items() if k != "rolls"}
                if submitted != normalized:
                    raise BattleHold("DUPLICATE_ID_DIFFERENT_ACTION_DENIED")
                result = self.view();result["deduplicated_request"] = rid
                return result
            if normalized["action"] not in ("ATTACK", "PASS") or normalized["reaction"] not in ("NONE", "DEFENDER", "ESQUIVAR"):
                raise BattleHold("ACTION_OR_REACTION_UNSUPPORTED")
            target = self.runner.view(self.session)["next_target"]
            if normalized["target"] != target:
                raise BattleHold("INVALID_ACTIVE_TARGET")
            if normalized["action"] == "PASS" and normalized["reaction"] != "NONE":
                raise BattleHold("PASS_MUST_HAVE_NO_REACTION")
            if normalized["reaction"] != "NONE" and self.runner.runtime.scene.actors[target].reaction != 1:
                raise BattleHold("DEFENDER_REACTION_UNAVAILABLE")
            choice = dict(normalized)
            if choice["action"] == "ATTACK":
                choice["rolls"] = {"attack_d6": secrets.randbelow(6)+1,
                                   "damage_d6": secrets.randbelow(6)+1}
            # Build an entirely isolated candidate. No mutations to the current
            # simulation are exposed until the JSON journal commits durably.
            candidate_record = {"request_id":rid,"choice":choice,"voided":False}
            candidate_session = copy.deepcopy(self.session)
            candidate_session["decisions"].append(candidate_record)
            candidate_runner = Runner(candidate_session)
            for x in candidate_session["decisions"]:
                if x.get("voided"):
                    continue
                result = candidate_runner.apply(x["choice"])
                if x is candidate_record:
                    x["row_sha256"] = result["row_sha256"]
                    x["applied_at"] = instant()
                elif result["row_sha256"] != x["row_sha256"]:
                    raise BattleHold("CANDIDATE_REPLAY_DIVERGENCE")
            self._atomic(self._path(candidate_session["session_id"]), self._sealed(candidate_session))
            self.session, self.runner = candidate_session, candidate_runner
            return self.view()

    def undo(self, request_id):
        with self.lock:
            if not isinstance(request_id,str) or len(request_id)<8 or len(request_id)>120:
                raise BattleHold("UNDO_ID_INVALID")
            if any(x["request_id"]==request_id for x in self.session["undo_requests"]):
                result=self.view();result["deduplicated_undo"]=request_id;return result
            candidate_session=copy.deepcopy(self.session)
            to_undo=next((x for x in reversed(candidate_session["decisions"]) if not x.get("voided")),None)
            if to_undo is None:
                raise BattleHold("NOTHING_TO_UNDO")
            to_undo["voided"]=True
            to_undo["voided_at"]=instant()
            candidate_session["void_events"].append({"request_id": request_id,
                    "voided_action_request_id":to_undo["request_id"],"at":instant(),
                    "mode":"LOCAL_SANDBOX_RECONSTRUCT_FROM_INITIAL_NO_NATIVE_EFFECT_RETRY"})
            candidate_session["undo_requests"].append({"request_id":request_id})
            candidate_runner=self._replay(candidate_session)
            self._atomic(self._path(candidate_session["session_id"]), self._sealed(candidate_session))
            self.session,self.runner=candidate_session,candidate_runner
            return self.view()

    def recover(self):
        with self.lock:
            return self._restore(self.session["session_id"])

    def receipt(self):
        with self.lock:
            data = self.view()
            history = {"schema": SCHEMA, "session": copy.deepcopy(self.session),
                       "readback": data, "historical_source_sha256": {
                            "R17": "30004e72da2d905badfeaab1dc1a3e245d4f3b1bce0227be2e81504589eec6c0"
                        },
                       "terminals_certified": 0, "official_combat_count": 0,
                       "official_writes": 0, "party_writes": 0, "nac_pass_terminal": "HOLD",
                       "readback_valid": self.runner.runtime.validate_trace()}
            history["receipt_sha256"] = digest(history)
            return history
