"""Invented teaching fixture; never a surrogate patient vector for the study."""

from .endpoint import Sample, descriptive_summary


def synthetic_samples():
    return (
        Sample("SYNTHETIC_S01", "SYNTHETIC_P01", "R", 0, 10),
        Sample("SYNTHETIC_S02", "SYNTHETIC_P01", "R", 30, 10),
        Sample("SYNTHETIC_S03", "SYNTHETIC_P02", "R", 25, 15),
        Sample("SYNTHETIC_S04", "SYNTHETIC_P03", "NR", 10, 20),
        Sample("SYNTHETIC_S05", "SYNTHETIC_P04", "NR", 15, 15),
    )


def run():
    return {
        "scope": "SYNTHETIC TEACHING EXAMPLE ONLY; not study results or reproduction",
        "endpoint": "mean within patient of log2((T% + 0.5)/(macrophage% + 0.5))",
        "results": descriptive_summary(synthetic_samples()),
        "limitations": [
            "Four invented patients do not represent the original cohort.",
            "No scientific hypothesis test or bootstrap interval is calculated here.",
            "No real study results or patient records are included in this standalone example.",
            "No expression processing, annotation, integration or model fitting is performed.",
        ],
    }
