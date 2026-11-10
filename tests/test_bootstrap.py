"""Verify the bootstrap and sensitivity example using invented counts only."""

import json
import math
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from melanoma_portfolio.bootstrap import (
    DEFAULT_PSEUDOCOUNTS_PP,
    CountSample,
    analyze,
    patient_scores,
    run,
    synthetic_count_samples,
)


def hand_cohort():
    # At 0.5 percentage points with 200 immune cells, the sample score is
    # log2((t_count + 1) / (macrophage_count + 1)). Two baseline samples
    # from R-A have scores 0 and 2, giving exactly one patient score of 1.
    return (
        CountSample("fixture-a1", "R-A", "R", 0, 0, 200),
        CountSample("fixture-a2", "R-A", "R", 3, 0, 200),
        CountSample("fixture-b", "R-B", "R", 7, 0, 200),
        CountSample("fixture-c", "NR-C", "NR", 0, 0, 200),
        CountSample("fixture-d", "NR-D", "NR", 3, 0, 200),
    )


def primary_row(report):
    return next(
        row for row in report["sensitivity"]
        if row["pseudocount_pp"] == report["primary_pseudocount_pp"]
    )


class BootstrapTests(unittest.TestCase):
    def test_patient_scores_and_primary_match_hand_calculation(self):
        counts = hand_cohort()
        scores = {record.patient_id: (record.score, record.n_samples)
                  for record in patient_scores(counts)}
        self.assertEqual(
            scores, {"R-A": (1, 2), "R-B": (3, 1), "NR-C": (0, 1), "NR-D": (2, 1)}
        )
        result = analyze(counts, draws=40)
        self.assertEqual(
            (result["n_samples"], result["n_patients"], result["n_R"], result["n_NR"]),
            (5, 4, 2, 2),
        )
        self.assertEqual(primary_row(result)["median_difference_R_minus_NR"], 1)

    def test_unequal_biopsy_yields_do_not_weight_patient_score(self):
        records = (
            CountSample("small", "R-A", "R", 40, 0, 100),
            CountSample("large", "R-A", "R", 0, 100, 1000),
        )
        mean_of_scores = (math.log2(40.5 / 0.5) + math.log2(0.5 / 10.5)) / 2
        pooled_score = math.log2((4000 / 1100 + 0.5) / (10000 / 1100 + 0.5))
        patient, = patient_scores(records)
        self.assertAlmostEqual(patient.score, mean_of_scores)
        self.assertGreater(patient.score, 0)
        self.assertLess(pooled_score, 0)

    def test_replacement_reaches_known_two_by_two_tails(self):
        # Fixed-size resamples from R=[1,3] and NR=[0,2] can attain -1 and 3,
        # each with probability 1/16. Without replacement the median
        # difference is always 1. This known-seed run reaches both tails.
        result = analyze(hand_cohort(), draws=1024, seed=18)
        self.assertEqual(primary_row(result)["bootstrap_95_interval"], [-1, 3])

    def test_strata_and_percentiles_preserve_tied_scores(self):
        # Independent sampling within each stratum preserves a one-unit
        # difference on every draw when its patient scores are constant.
        records = tuple(
            CountSample("sample-" + key, key, response, t, 0, 200)
            for key, response, t in (
                ("A", "R", 1), ("B", "R", 1), ("C", "R", 1),
                ("D", "NR", 0), ("E", "NR", 0),
            )
        )
        result = analyze(records, draws=41, seed=18)
        self.assertEqual((result["n_R"], result["n_NR"]), (3, 2))
        row = primary_row(result)
        self.assertEqual(row["bootstrap_95_interval"], [1, 1])
        self.assertEqual(row["leave_one_patient_out_range"], [1, 1])

    def test_seeded_unequal_strata_and_linear_percentile_interpolation(self):
        counts = hand_cohort() + (CountSample("fixture-e", "NR-E", "NR", 15, 0, 200),)
        # For the 2-by-3 scores R=[1,3] and NR=[0,2,4], seed 1 gives these
        # five sorted resampled differences: -1, 0, 0, 1, 2. The percentile
        # indices (0.1 and 3.9) therefore interpolate to -0.9 and 1.9.
        result = analyze(counts, draws=5, seed=1)
        self.assertEqual((result["n_R"], result["n_NR"]), (2, 3))
        low, high = primary_row(result)["bootstrap_95_interval"]
        self.assertAlmostEqual(low, -0.9)
        self.assertAlmostEqual(high, 1.9)

    def test_seed_and_input_order_reproduce_entire_result(self):
        counts = hand_cohort()
        first = analyze(counts, draws=43, seed=91)
        self.assertEqual(first, analyze(iter(counts), draws=43, seed=91))
        self.assertEqual(first, analyze(reversed(counts), draws=43, seed=91))
        self.assertEqual((first["draws"], first["seed"]), (43, 91))

    def test_seven_pseudocounts_and_whole_patient_omission(self):
        result = analyze(hand_cohort(), draws=64)
        expected = (0.05, 0.1, 0.25, 0.5, 1, 2, 5)
        self.assertEqual(DEFAULT_PSEUDOCOUNTS_PP, expected)
        rows = result["sensitivity"]
        self.assertEqual(tuple(row["pseudocount_pp"] for row in rows), expected)
        self.assertGreater(rows[0]["median_difference_R_minus_NR"],
                           rows[-1]["median_difference_R_minus_NR"])
        self.assertEqual(primary_row(result)["leave_one_patient_out_range"], [0, 2])
        for row in rows:
            with self.subTest(pseudocount=row["pseudocount_pp"]):
                for key in ("bootstrap_95_interval", "leave_one_patient_out_range"):
                    low, high = row[key]
                    self.assertTrue(math.isfinite(low) and math.isfinite(high))
                    self.assertLessEqual(low, high)

    def test_bootstrap_resamples_match_across_pseudocounts(self):
        # Every individual score is either zero or a common positive factor
        # that depends on the setting. With matched resamples, the interval
        # divided by that factor is identical across settings.
        records = tuple(
            CountSample("sample-" + key, key, response, t, 0, 200)
            for key, response, t in (
                ("A", "R", 1), ("B", "R", 1), ("C", "R", 0),
                ("D", "NR", 1), ("E", "NR", 0), ("F", "NR", 0),
            )
        )
        report = analyze(records, draws=7, seed=13)
        baseline = primary_row(report)["bootstrap_95_interval"]
        for row in report["sensitivity"]:
            p = row["pseudocount_pp"]
            factor = math.log2((0.5 + p) / p)
            for actual, expected in zip(row["bootstrap_95_interval"], baseline):
                self.assertAlmostEqual(actual / factor, expected)

    def test_invalid_counts_refused(self):
        record = hand_cohort()[0]
        for kwargs in (
            {"immune_count": 0}, {"immune_count": False}, {"immune_count": 200.0},
            {"t_count": -1}, {"t_count": 0.5}, {"macrophage_count": True},
            {"t_count": 150, "macrophage_count": 51},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                patient_scores((replace(record, **kwargs),))

    def test_invalid_ids_or_response_refused(self):
        record = hand_cohort()[0]
        for kwargs in (
            {"sample_id": ""}, {"patient_id": " "}, {"response": "unclassified"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                patient_scores((replace(record, **kwargs),))

    def test_duplicate_samples_and_conflicting_patient_labels_refused(self):
        first, second, *_ = hand_cohort()
        for record in (first, replace(second, response="NR")):
            with self.subTest(record=record), self.assertRaises(ValueError):
                patient_scores((first, record))

    def test_insufficient_patient_strata_refused_even_with_repeated_samples(self):
        first, second, _, fourth, fifth = hand_cohort()
        for records in ((), (first, second), (first, second, fourth, fifth)):
            with self.subTest(records=records), self.assertRaises(ValueError):
                analyze(records, draws=10)

    def test_invalid_pseudocounts_and_draws_refused(self):
        records = hand_cohort()
        for value in (0, -0.5, math.nan, math.inf, True, "0.5"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                patient_scores(records, pseudocount_pp=value)
        for value in (0, -1, 1, True, 2.5, 100001):
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze(records, draws=value)
        for value in (0.5, False, "18"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze(records, draws=10, seed=value)
        for grid in ((), (0.1, 1), (0.5, 0.5), (0.5, math.inf)):
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                analyze(records, draws=10, pseudocounts_pp=grid)

    def test_fixture_has_deliberate_edge_cases_and_only_aggregate_output(self):
        records = synthetic_count_samples()
        self.assertGreater(len(records), len({row.patient_id for row in records}))
        self.assertGreater(len({row.immune_count for row in records}), 1)
        self.assertTrue(any(row.t_count == 0 for row in records))
        self.assertTrue(any(row.macrophage_count == 0 for row in records))
        patients = patient_scores(records)
        responders = [row.score for row in patients if row.response == "R"]
        nonresponders = [row.score for row in patients if row.response == "NR"]
        self.assertLess(max(min(responders), min(nonresponders)),
                        min(max(responders), max(nonresponders)))
        report = run(draws=32)
        self.assertIn("SYNTHETIC", report["scope"])
        output = json.dumps(report, allow_nan=False)
        for record in records:
            self.assertNotIn(record.sample_id, output)
            self.assertNotIn(record.patient_id, output)

    def test_cli_runs_from_empty_directory_and_reports_requested_settings(self):
        script = ROOT / "scripts/run_bootstrap_demo.py"
        with tempfile.TemporaryDirectory() as cwd:
            completed = subprocess.run(
                [sys.executable, "-I", "-S", "-B", str(script), "--seed", "20", "--draws", "64"],
                cwd=cwd, check=True, capture_output=True, text=True, timeout=15,
            )
        self.assertEqual(json.loads(completed.stdout), run(draws=64, seed=20))
        self.assertEqual(completed.stderr, "")

    def test_cli_refuses_bad_draw_count(self):
        completed = subprocess.run(
            [sys.executable, "-I", "-S", "-B",
             str(ROOT / "scripts/run_bootstrap_demo.py"), "--draws", "0"],
            capture_output=True, text=True, timeout=15,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "")
        self.assertIn("draw", completed.stderr.lower())


if __name__ == "__main__":
    unittest.main()
