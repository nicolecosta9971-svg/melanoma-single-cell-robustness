"""Entirely synthetic tests; no study-data reads or desired-result assertions."""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from melanoma_portfolio.demo import run, synthetic_samples
from melanoma_portfolio.endpoint import (
    Sample, aggregate_patients, descriptive_summary, pairwise_auc, sample_balance,
)


class EndpointTests(unittest.TestCase):
    def test_equal_percentages_zero(self):
        self.assertEqual(sample_balance(10, 10), 0)

    def test_both_zero_finite_not_biological_absence(self):
        self.assertEqual(sample_balance(0, 0), 0)

    def test_swapping_categories_changes_sign(self):
        self.assertAlmostEqual(sample_balance(20, 10), -sample_balance(10, 20))

    def test_pseudocount_units(self):
        self.assertAlmostEqual(sample_balance(0, 10), math.log2(0.5 / 10.5))

    def test_mean_sample_scores_not_score_of_mean_percentages(self):
        p = aggregate_patients(synthetic_samples())[0]
        expected = (sample_balance(0, 10) + sample_balance(30, 10)) / 2
        self.assertEqual(p.n_samples, 2)
        self.assertAlmostEqual(p.score, expected)
        self.assertLess(p.score, 0)
        self.assertGreater(sample_balance(15, 10), 0)

    def test_repeated_samples_not_new_patients(self):
        summary = descriptive_summary(synthetic_samples())
        self.assertEqual((summary["n_samples"], summary["n_patients"]), (5, 4))
        self.assertEqual((summary["n_R"], summary["n_NR"]), (2, 2))

    def test_order_does_not_change_summary(self):
        self.assertEqual(descriptive_summary(synthetic_samples()), descriptive_summary(reversed(synthetic_samples())))

    def test_duplicate_sample_refused(self):
        with self.assertRaises(ValueError):
            aggregate_patients([synthetic_samples()[0], synthetic_samples()[0]])

    def test_conflicting_response_refused(self):
        with self.assertRaises(ValueError):
            aggregate_patients([Sample("SYNTHETIC_A", "SYNTHETIC_P", "R", 10, 20), Sample("SYNTHETIC_B", "SYNTHETIC_P", "NR", 20, 10)])

    def test_invalid_percentages_refused(self):
        for bad in [float("nan"), float("inf"), -0.1, 101, True, "20", None]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                sample_balance(bad, 0)

    def test_overlapping_disjoint_percentages_refused(self):
        with self.assertRaises(ValueError):
            sample_balance(60, 60)

    def test_empty_samples_refused(self):
        with self.assertRaises(ValueError):
            aggregate_patients([])

    def test_absent_response_group_refused(self):
        with self.assertRaises(ValueError):
            descriptive_summary([Sample("SYNTHETIC_A", "SYNTHETIC_P", "R", 10, 20)])

    def test_unknown_response_refused(self):
        with self.assertRaises(ValueError):
            aggregate_patients([Sample("SYNTHETIC_A", "SYNTHETIC_P", "unknown", 10, 20)])

    def test_blank_identifier_refused(self):
        with self.assertRaises(ValueError):
            aggregate_patients([Sample("", "SYNTHETIC_P", "R", 10, 20)])

    def test_auc_ties(self):
        self.assertEqual(pairwise_auc([1, 2], [1, 3]), 0.375)

    def test_auc_all_ties(self):
        self.assertEqual(pairwise_auc([1, 1], [1, 1]), 0.5)

    def test_auc_all_higher(self):
        self.assertEqual(pairwise_auc([3, 4], [1, 2]), 1)

    def test_auc_group_swap(self):
        self.assertEqual(pairwise_auc([1, 2], [1, 3]) + pairwise_auc([1, 3], [1, 2]), 1)

    def test_auc_invalid_score_refused(self):
        for bad in [float("nan"), float("inf"), True, "1"]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                pairwise_auc([bad], [1])

    def test_summary_has_no_patient_identifiers(self):
        self.assertNotIn("SYNTHETIC_P", str(descriptive_summary(synthetic_samples())))

    def test_no_p_value_in_synthetic_demo(self):
        self.assertIsNone(run()["results"]["p_value"])
        self.assertIn("SYNTHETIC", run()["scope"])


if __name__ == "__main__":
    unittest.main()
