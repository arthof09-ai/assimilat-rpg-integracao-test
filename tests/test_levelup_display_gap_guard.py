"""Adversarial unit tests for classification of known P12 presentation gap."""
import copy
import unittest

from scripts.levelup_display_gap_guard import inspect_p12_profiles, TIERS


def fixture():
    return {"profiles": [
        {"ordinal": i, "rank": TIERS[(i-1)//5],
         "FULL": {"combat_attack_dme_preview_TEST": {
            "physical_attack_expression": f"1d6 + FOR {14+i} + Luta inicial +2",
            "physical_dice": "4d6", "FOR_damage_bonus_applied": 0
         }}}
        for i in range(1, 26)
    ]}


class LegacyDisplayGapTests(unittest.TestCase):
    def test_25_known_anomalies_detected(self):
        self.assertEqual(inspect_p12_profiles(fixture())["legacy_display_gaps"], 25)

    def test_missing_profile_fails_closed(self):
        f = fixture(); f["profiles"].pop()
        with self.assertRaises(AssertionError):
            inspect_p12_profiles(f)

    def test_wrong_rank_fails_closed(self):
        f = fixture(); f["profiles"][5]["rank"] = "BRONZE"
        with self.assertRaises(AssertionError):
            inspect_p12_profiles(f)

    def test_newly_corrected_field_requires_new_baseline(self):
        f = fixture()
        a = f["profiles"][0]["FULL"]["combat_attack_dme_preview_TEST"]
        a["physical_attack_expression"] = a["physical_dice"]
        with self.assertRaises(AssertionError):
            inspect_p12_profiles(f)

    def test_unclassified_mismatch_fails_closed(self):
        f = fixture()
        f["profiles"][0]["FULL"]["combat_attack_dme_preview_TEST"]["physical_attack_expression"] = "UNKNOWN"
        with self.assertRaises(AssertionError):
            inspect_p12_profiles(f)

    def test_for_damage_bonus_rejected(self):
        f = fixture()
        f["profiles"][0]["FULL"]["combat_attack_dme_preview_TEST"]["FOR_damage_bonus_applied"] = 15
        with self.assertRaises(AssertionError):
            inspect_p12_profiles(f)


if __name__ == "__main__":
    unittest.main()
