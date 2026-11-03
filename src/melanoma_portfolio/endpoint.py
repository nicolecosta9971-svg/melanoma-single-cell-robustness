"""Endpoint arithmetic for sample percentages and patient-level summaries.

The locked sample score is log2((T_percent + .5)/(M_percent + .5)).
Patient scores are unweighted means of sample scores, not ratios of means.
The public demonstration uses invented examples only.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from math import fsum, isfinite, log2
from numbers import Real
from statistics import median


@dataclass(frozen=True)
class Sample:
    sample_id: str
    patient_id: str
    response: str
    t_percent: float
    macrophage_percent: float


@dataclass(frozen=True)
class Patient:
    patient_id: str
    response: str
    score: float
    n_samples: int


def _percentage(value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("Percentage must be a real number, not text or bool")
    if not isfinite(value) or not 0 <= value <= 100:
        raise ValueError("Percentage must be finite and between 0 and 100")
    return float(value)


def sample_balance(t_percent: Real, macrophage_percent: Real) -> float:
    """Compute the locked sample log-ratio; .5 means percentage points.

    Both types use the same recovered-immune-cell denominator and are disjoint.
    A 1e-10 percentage-point tolerance allows ordinary floating-point rounding.
    An observed (0,0) returns zero, not evidence of biological balance/absence.
    """
    t, m = _percentage(t_percent), _percentage(macrophage_percent)
    if t + m > 100 + 1e-10:
        raise ValueError("Disjoint cell-type percentages cannot sum above 100")
    return log2((t + 0.5) / (m + 0.5))


def aggregate_patients(samples: Iterable[Sample]) -> tuple[Patient, ...]:
    """One patient outcome per person; no sample or cell-yield weighting."""
    groups, seen_samples = {}, set()
    for sample in samples:
        if not isinstance(sample, Sample):
            raise ValueError("Expected Sample records")
        for identifier in (sample.sample_id, sample.patient_id):
            if not isinstance(identifier, str) or not identifier.strip():
                raise ValueError("Sample and patient identifiers must be nonempty text")
        if sample.sample_id in seen_samples:
            raise ValueError("Duplicate sample identifier")
        seen_samples.add(sample.sample_id)
        if sample.response not in ("R", "NR"):
            raise ValueError("Response must be R or NR")
        score = sample_balance(sample.t_percent, sample.macrophage_percent)
        if sample.patient_id not in groups:
            groups[sample.patient_id] = (sample.response, [])
        response, scores = groups[sample.patient_id]
        if response != sample.response:
            raise ValueError("Conflicting responses within a patient")
        scores.append(score)
    if not groups:
        raise ValueError("At least one sample is required")
    return tuple(
        Patient(pid, response, fsum(sorted(scores)) / len(scores), len(scores))
        for pid, (response, scores) in sorted(groups.items())
    )


def _finite_scores(values: Iterable[Real]) -> tuple[Real, ...]:
    values = tuple(values)
    if not values:
        raise ValueError("Both response groups must contain patient scores")
    if any(
        isinstance(x, bool) or not isinstance(x, Real) or not isfinite(x)
        for x in values
    ):
        raise ValueError("Patient scores must be finite real numbers")
    return values


def pairwise_auc(
    responders: Iterable[Real], nonresponders: Iterable[Real]
) -> float:
    """Return within-cohort ordering probability, with half credit for ties."""
    r, nr = _finite_scores(responders), _finite_scores(nonresponders)
    wins = sum((x > y) + 0.5 * (x == y) for x in r for y in nr)
    return wins / (len(r) * len(nr))


def descriptive_summary(samples: Iterable[Sample]) -> dict[str, object]:
    """Aggregate output only. No patient identifiers/scores are returned."""
    patients = aggregate_patients(samples)
    r = [p.score for p in patients if p.response == "R"]
    nr = [p.score for p in patients if p.response == "NR"]
    auc = pairwise_auc(r, nr)  # Also refuses an empty clinical group.
    return {
        "analysis_unit": "patient mean of sample log-ratios",
        "n_patients": len(patients),
        "n_samples": sum(p.n_samples for p in patients),
        "n_R": len(r),
        "n_NR": len(nr),
        "median_difference_R_minus_NR": median(r) - median(nr),
        "auc_R_higher": auc,
        "p_value": None,
        "p_value_status": "not calculated by dependency-free arithmetic module",
    }
