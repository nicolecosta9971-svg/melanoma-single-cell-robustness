"""Synthetic teaching example for a patient-level immune-balance contrast.

The built-in counts are invented. This module starts *after* cell recovery,
quality control and annotation. It does not select baseline samples, fit
scVI, run CellTypist, or reproduce the melanoma study.
"""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from math import fsum, isfinite, log2
from random import Random
from statistics import median

from .endpoint import Patient

PRIMARY_PSEUDOCOUNT_PP = 0.5
DEFAULT_PSEUDOCOUNTS_PP = (0.05, 0.1, 0.25, PRIMARY_PSEUDOCOUNT_PP, 1.0, 2.0, 5.0)
DEFAULT_DRAWS = 5_000
DEFAULT_SEED = 18
MAX_DRAWS = 100_000


@dataclass(frozen=True)
class CountSample:
    """One already-selected baseline biopsy; counts are nonnegative integers.

    The two cell families are disjoint subsets of ``immune_count``. All
    other recovered immune cells remain in that denominator.
    """

    sample_id: str
    patient_id: str
    response: str
    t_count: int
    macrophage_count: int
    immune_count: int


def _pseudocount(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Pseudocount must be a finite positive number of percentage points")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError("Pseudocount must be finite") from exc
    if not isfinite(value) or value <= 0:
        raise ValueError("Pseudocount must be a finite positive number of percentage points")
    return value


def _prepare(samples: Iterable[CountSample]) -> dict[str, tuple[str, list[tuple[float, float]]]]:
    """Validate biopsies once; preserve one clinical response per patient."""
    groups: dict[str, tuple[str, list[tuple[float, float]]]] = {}
    seen_samples = set()
    for sample in samples:
        if not isinstance(sample, CountSample):
            raise ValueError("Expected CountSample records")
        for identifier in (sample.sample_id, sample.patient_id):
            if not isinstance(identifier, str) or not identifier or identifier != identifier.strip():
                raise ValueError("Sample and patient IDs must be nonempty text without surrounding whitespace")
        if sample.sample_id in seen_samples:
            raise ValueError("Duplicate sample ID")
        seen_samples.add(sample.sample_id)
        if not isinstance(sample.response, str) or sample.response not in ("R", "NR"):
            raise ValueError("Response must be R or NR")

        t, m, total = sample.t_count, sample.macrophage_count, sample.immune_count
        if any(isinstance(count, bool) or not isinstance(count, int) for count in (t, m, total)):
            raise ValueError("Cell counts must be integers, not bools")
        if total <= 0 or t < 0 or m < 0 or t + m > total:
            raise ValueError("Disjoint cell counts must be nonnegative and sum to at most the positive immune total")

        response, percentages = groups.setdefault(sample.patient_id, (sample.response, []))
        if response != sample.response:
            raise ValueError("Conflicting responses within a patient")
        percentages.append((100 * (t / total), 100 * (m / total)))
    if not groups:
        raise ValueError("At least one baseline sample is required")
    return groups


def _log_ratio(t_pp: float, macrophage_pp: float, pseudocount_pp: float) -> float:
    numerator, denominator = t_pp + pseudocount_pp, macrophage_pp + pseudocount_pp
    ratio = numerator / denominator
    if ratio > 0 and isfinite(ratio):
        return log2(ratio)
    # Preserve the same mathematical ratio for a subnormal custom pseudocount.
    return log2(numerator) - log2(denominator)


def _patient_scores(
    groups: dict[str, tuple[str, list[tuple[float, float]]]], pseudocount_pp: float,
) -> tuple[Patient, ...]:
    patients = []
    for patient_id, (response, percentages) in sorted(groups.items()):
        sample_scores = [_log_ratio(t, m, pseudocount_pp) for t, m in percentages]
        score = fsum(sorted(sample_scores)) / len(sample_scores)
        patients.append(Patient(patient_id, response, score, len(sample_scores)))
    return tuple(patients)


def patient_scores(
    samples: Iterable[CountSample], pseudocount_pp: float = PRIMARY_PSEUDOCOUNT_PP,
) -> tuple[Patient, ...]:
    """Convert counts to percentages, then average sample log-ratios by patient.

    Neither cells nor biopsy yield weight the patient score. Input records
    must have been selected as baseline elsewhere. Results sort by patient ID.
    """
    return _patient_scores(_prepare(samples), _pseudocount(pseudocount_pp))


def _contrast(r: tuple[float, ...], nr: tuple[float, ...]) -> float:
    return median(r) - median(nr)


def _stratified_draws(
    n_r: int, n_nr: int, draws: int, seed: int,
) -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    rng = Random(seed)
    for _ in range(draws):
        # Sample indices with replacement within each response group. Keep
        # duplicate draws; deduplicating them would no longer be a bootstrap.
        yield (
            tuple(rng.randrange(n_r) for _ in range(n_r)),
            tuple(rng.randrange(n_nr) for _ in range(n_nr)),
        )


def _linear_percentile(sorted_values: list[float], quantile: float) -> float:
    position = (len(sorted_values) - 1) * quantile
    index = int(position)
    lower, upper = sorted_values[index], sorted_values[min(index + 1, len(sorted_values) - 1)]
    return lower + (position - index) * (upper - lower)


def _leave_one_patient_out(r: tuple[float, ...], nr: tuple[float, ...]) -> list[float]:
    estimates = [_contrast(r[:i] + r[i + 1 :], nr) for i in range(len(r))]
    estimates.extend(_contrast(r, nr[:i] + nr[i + 1 :]) for i in range(len(nr)))
    return [min(estimates), max(estimates)]


def analyze(
    samples: Iterable[CountSample], *, draws: int = DEFAULT_DRAWS, seed: int = DEFAULT_SEED,
    pseudocounts_pp: Iterable[float] = DEFAULT_PSEUDOCOUNTS_PP,
) -> dict[str, object]:
    """Return aggregate patient-level bootstrap and sensitivity results only."""
    if isinstance(draws, bool) or not isinstance(draws, int) or not 2 <= draws <= MAX_DRAWS:
        raise ValueError(f"Bootstrap draws must be an integer between 2 and {MAX_DRAWS}")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("Bootstrap seed must be an integer")
    grid = tuple(_pseudocount(value) for value in pseudocounts_pp)
    if PRIMARY_PSEUDOCOUNT_PP not in grid or len(set(grid)) != len(grid):
        raise ValueError("Pseudocount grid must be unique and include 0.5 percentage points")

    groups = _prepare(samples)
    n_r = sum(response == "R" for response, _ in groups.values())
    n_nr = len(groups) - n_r
    if min(n_r, n_nr) < 2:
        raise ValueError("Need at least two patients per response group for leave-one-patient-out checks")

    score_sets = []
    for pseudocount_pp in grid:
        patients = _patient_scores(groups, pseudocount_pp)
        score_sets.append((
            tuple(patient.score for patient in patients if patient.response == "R"),
            tuple(patient.score for patient in patients if patient.response == "NR"),
        ))

    distributions: list[list[float]] = [[] for _ in grid]
    for r_indexes, nr_indexes in _stratified_draws(n_r, n_nr, draws, seed):
        # Reuse these patient indices across the grid; otherwise simulation
        # noise can masquerade as a change from the pseudocount setting.
        for (r, nr), distribution in zip(score_sets, distributions):
            distribution.append(_contrast(
                tuple(r[i] for i in r_indexes), tuple(nr[i] for i in nr_indexes),
            ))

    sensitivity = []
    for pseudocount_pp, (r, nr), distribution in zip(grid, score_sets, distributions):
        distribution.sort()
        sensitivity.append({
            "pseudocount_pp": pseudocount_pp,
            "median_difference_R_minus_NR": _contrast(r, nr),
            "bootstrap_95_interval": [
                _linear_percentile(distribution, 0.025), _linear_percentile(distribution, 0.975),
            ],
            "leave_one_patient_out_range": _leave_one_patient_out(r, nr),
        })

    return {
        "n_patients": n_r + n_nr,
        "n_samples": sum(len(percentages) for _, percentages in groups.values()),
        "n_R": n_r,
        "n_NR": n_nr,
        "primary_pseudocount_pp": PRIMARY_PSEUDOCOUNT_PP,
        "draws": draws,
        "seed": seed,
        "bootstrap_method": "Patient resampling with replacement within R and NR, holding group sizes fixed",
        "interval_method": "2.5th and 97.5th percentiles with linear interpolation; pointwise",
        "leave_one_patient_out_method": "Min/max contrast after omitting each patient once; not an interval estimate",
        "sensitivity": sensitivity,
    }


def synthetic_count_samples() -> tuple[CountSample, ...]:
    """Fourteen invented biopsies from twelve invented patients."""
    return (
        CountSample("SYNTHETIC_S01", "SYNTHETIC_P01", "R", 36, 18, 200),
        CountSample("SYNTHETIC_S02", "SYNTHETIC_P01", "R", 0, 100, 1_000),
        CountSample("SYNTHETIC_S03", "SYNTHETIC_P02", "R", 35, 10, 250),
        CountSample("SYNTHETIC_S04", "SYNTHETIC_P03", "R", 12, 0, 300),
        CountSample("SYNTHETIC_S05", "SYNTHETIC_P04", "R", 72, 24, 600),
        CountSample("SYNTHETIC_S06", "SYNTHETIC_P05", "R", 0, 0, 450),
        CountSample("SYNTHETIC_S07", "SYNTHETIC_P06", "R", 44, 30, 200),
        CountSample("SYNTHETIC_S08", "SYNTHETIC_P07", "NR", 24, 120, 600),
        CountSample("SYNTHETIC_S09", "SYNTHETIC_P08", "NR", 39, 18, 300),
        CountSample("SYNTHETIC_S10", "SYNTHETIC_P09", "NR", 6, 30, 200),
        CountSample("SYNTHETIC_S11", "SYNTHETIC_P09", "NR", 49, 77, 700),
        CountSample("SYNTHETIC_S12", "SYNTHETIC_P10", "NR", 0, 48, 400),
        CountSample("SYNTHETIC_S13", "SYNTHETIC_P11", "NR", 35, 50, 500),
        CountSample("SYNTHETIC_S14", "SYNTHETIC_P12", "NR", 33, 30, 300),
    )


def run(*, draws: int = DEFAULT_DRAWS, seed: int = DEFAULT_SEED) -> dict[str, object]:
    """Produce the standalone, entirely invented teaching report."""
    return {
        "scope": "SYNTHETIC TEACHING EXAMPLE ONLY; not study results or reproduction",
        "endpoint": "Mean within patient of log2((T% + p)/(macrophage% + p)), p in percentage points",
        "results": analyze(synthetic_count_samples(), draws=draws, seed=seed),
        "limitations": [
            "All counts, IDs and response assignments are invented; baseline selection is assumed.",
            "Intervals condition on the invented patient scores and do not cover annotation or endpoint-selection uncertainty.",
            "The pseudocount settings use the same patients and resampled indices; they are not independent replications.",
            "The demo does not run integration, annotation, clinical adjustment, hypothesis tests or external validation.",
        ],
    }
