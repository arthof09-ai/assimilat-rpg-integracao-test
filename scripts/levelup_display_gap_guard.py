"""Independent TEST-only check of known P12 Orc attack-display defect.

Documents why 2,026 historical P12 unit tests don't certify 25 ficha displays.
Does not patch attributes, perform combat, write Notion or change the motor.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from native_engine_ci import PINS, verify

SOURCE_JSON = "orc25_r216p12_MASTER_CORRECTED/ORC_R216P12_25_NIVEIS_20_TRANSFORMACOES_MASTER_CORRIGIDOS.json"
SOURCE_SHA = "a54467e7786855f05289149ea8f978a3b0a30591549f46f6ab8cdabcc355a7a8"
TIERS = ("BRONZE", "PRATA", "OURO", "OURO_NEGRO", "LENDARIO")


def inspect_p12_profiles(data):
    profiles = data["profiles"]
    if len(profiles) != 25:
        raise AssertionError("P12_EXPECTED_25_PROFILES")
    mismatches = []
    tier_counts = {tier: 0 for tier in TIERS}
    for ordinal, profile in enumerate(profiles, 1):
        if profile["ordinal"] != ordinal or profile["rank"] != TIERS[(ordinal - 1)//5]:
            raise AssertionError("P12_LEVEL_OR_RANK_ORDER_CHANGED")
        tier_counts[profile["rank"]] += 1
        attack = profile["FULL"]["combat_attack_dme_preview_TEST"]
        old = attack["physical_attack_expression"]
        dice = attack["physical_dice"]
        if not (re.fullmatch(r"\d+d6", dice) and attack["FOR_damage_bonus_applied"] == 0):
            raise AssertionError("P12_ATTACK_FIELDS_UNEXPECTED")
        if old != dice:
            if not ("FOR " in old and "Luta" in old and "+" in old):
                raise AssertionError("P12_UNCLASSIFIED_ATTACK_DISPLAY_MISMATCH")
            mismatches.append(ordinal)
    if mismatches != list(range(1,26)):
        raise AssertionError("P12_KNOWN_25_DISPLAY_GAPS_CHANGED_OR_RESOLVED")
    return {"legacy_display_gaps": len(mismatches), "rank_counts": tier_counts}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive.resolve()
    verified = verify(archive, PINS["levelup"])
    with zipfile.ZipFile(archive) as zipped:
        raw = zipped.read(SOURCE_JSON)
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise AssertionError("P12_ORC_VIEW_SOURCE_SHA_MISMATCH")
    result = inspect_p12_profiles(json.loads(raw))
    result.update({
        "status": "KNOWN_P12_PRESENTATION_GAP_NOT_ENGINE_PASS",
        "next": "P13_CORRECTED_VIEW_EXISTS_OUTSIDE_THIS_ZIP__NOT_CI_VERIFIED",
        "verified_zip_member_hashes": verified,
        "notion_writes": 0,
        "canonical_promotion": "HOLD",
    })
    print("::warning::LEVEL-UP P12: 25 legacy attack/damage display fields differ from physical weapon dice. P13 presentation patch is NOT checked by this CI.")
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
