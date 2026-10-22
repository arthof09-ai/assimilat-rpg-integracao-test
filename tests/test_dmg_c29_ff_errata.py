"""TEST-only guard for consuming additive C29-FF errata without mutating history.

This is not an engine, a canonical rule, or an independent validation of VZ.
"""
import json
from decimal import Decimal
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "experiments" / "dmg_c29" / "errata_ff_c29.json"
TERM = re.compile(r"[+]?\\d+d\\d+|[+-]\\d+")


def conditional_raw_mean(expression):
    """Only basic additive dice mean; does not compute hit, RDF or crit."""
    chunks = TERM.findall(expression)
    if not chunks or "".join(chunks) != expression:
        raise ValueError("UNSUPPORTED_EXPRESSION")
    result = Decimal(0)
    for term in chunks:
        if "d" not in term:
            result += Decimal(term)
        else:
            count, faces = term.lstrip("+").split("d")
            if int(count) < 1 or int(faces) < 2:
                raise ValueError("INVALID_DICE")
            result += Decimal(count) * (Decimal(faces) + 1) / 2
    return result


class TestC29FFConsumption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_scope_stays_test_only(self):
        self.assertIs(self.doc["canonical_change"], False)
        self.assertEqual(self.doc["baseline"], "DMG-RANK-01 v1.1 (unaltered)")
        self.assertEqual(self.doc["f0_state"], "4/8 HOLD")
        self.assertEqual(len(self.doc["cases"]), 3)

    def test_corrected_means(self):
        expected = {
            "darek_normal": "62.5",
            "rhovan_corte_normal": "62.5",
            "rhovan_tempestade_normal": "124.5",
        }
        for c in self.doc["cases"]:
            with self.subTest(case=c["key"]):
                observed = conditional_raw_mean(c["formula"])
                self.assertEqual(observed, Decimal(expected[c["key"]]))
                self.assertEqual(observed, Decimal(c["expected_mean"]))

    def test_stale_formulas_not_current(self):
        for c in self.doc["cases"]:
            with self.subTest(case=c["key"]):
                stale = conditional_raw_mean(c["pre_errata_formula"])
                corrected = conditional_raw_mean(c["formula"])
                self.assertLess(stale, corrected)
                self.assertNotEqual(stale, Decimal(c["expected_mean"]))

    def test_no_double_count_chassis_or_ff(self):
        for c in self.doc["cases"]:
            with self.subTest(case=c["key"]):
                corrected = conditional_raw_mean(c["formula"])
                bonus = corrected - conditional_raw_mean(c["pre_errata_formula"])
                self.assertIn(bonus, (Decimal(3), Decimal(4)))
                self.assertNotEqual(corrected + bonus, Decimal(c["expected_mean"]))

    def test_transform_only_if_activated(self):
        expected = {
            "darek_normal": "64.5",
            "rhovan_corte_normal": "77.5",
            "rhovan_tempestade_normal": "139.5",
        }
        for c in self.doc["cases"]:
            with self.subTest(case=c["key"]):
                transformed = Decimal(c["transformed_mean_if_activated"])
                self.assertEqual(transformed, Decimal(expected[c["key"]]))
                self.assertGreater(transformed, Decimal(c["expected_mean"]))

    def test_fail_closed_unknown_expressions(self):
        for expr in ("", "10d10 + 1d8+3", "10d10*2", "10d0+3", "2d1+7", "2d6-FF"):
            with self.subTest(expression=expr):
                with self.assertRaises(ValueError):
                    conditional_raw_mean(expr)


if __name__ == "__main__":
    unittest.main()
