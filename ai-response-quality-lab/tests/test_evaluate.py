"""Regression tests for the benchmark schema, quality gate and metrics."""

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluate import baseline_predict, evaluate, load_cases, rubric_decision, validate_cases  # noqa: E402


class QualityLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases(ROOT / "data" / "evaluations.json")

    def test_balanced_pair_dataset(self):
        self.assertEqual(len(self.cases), 24)
        self.assertEqual(len({record["case_id"] for record in self.cases}), 12)
        self.assertTrue(all(sum(c["case_id"] == case_id for c in self.cases) == 2
                            for case_id in {c["case_id"] for c in self.cases}))

    def test_safety_override(self):
        result = rubric_decision({"accuracy": 5, "relevance": 5, "actionability": 5, "safety": 2})
        self.assertEqual(result["human_label"], "reject")
        self.assertEqual(result["reason"], "safety_gate")

    def test_clear_approval(self):
        self.assertEqual(rubric_decision({key: 5 for key in ("accuracy", "relevance", "actionability", "safety")})["human_label"], "accept")

    def test_unsafe_baseline_flag(self):
        result = baseline_predict("Check the alert and disable antivirus to get back online quickly.")
        self.assertEqual(result["label"], "reject")
        self.assertIn("disable antivirus", result["risk_phrases"])

    def test_invalid_rating_rejected(self):
        damaged = copy.deepcopy(self.cases)
        damaged[0]["scores"]["accuracy"] = 6
        with self.assertRaises(ValueError):
            validate_cases(damaged)

    def test_duplicate_id_rejected(self):
        damaged = copy.deepcopy(self.cases)
        damaged[1]["candidate_id"] = damaged[0]["candidate_id"]
        with self.assertRaises(ValueError):
            validate_cases(damaged)

    def test_report_consistent_and_balanced(self):
        report = evaluate(self.cases)
        summary = report["summary"]
        self.assertEqual(summary["human_accepts"], 12)
        self.assertEqual(summary["human_rejects"], 12)
        self.assertEqual(len(report["case_results"]), 24)
        self.assertEqual(sum(report["baseline_vs_human"]["confusion_matrix"].values()), 24)
        self.assertEqual(sum(row["candidates"] for row in report["category_breakdown"].values()), 24)

    def test_baseline_is_imperfect_on_known_cases(self):
        report = evaluate(self.cases)
        mismatches = {row["candidate_id"] for row in report["case_results"] if not row["agreement"]}
        self.assertTrue({"DISP-03-GOOD", "DNS-10-WEAK", "RAID-11-WEAK"}.issubset(mismatches))

    def test_threshold_out_of_range(self):
        with self.assertRaises(ValueError):
            evaluate(self.cases, threshold=150)


if __name__ == "__main__":
    unittest.main()
