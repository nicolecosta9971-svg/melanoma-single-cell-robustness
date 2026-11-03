"""Small, dependency-free teaching implementation of the fixed endpoint.

This package is not the original expression-processing or model-training workflow.
"""

from .endpoint import Sample, aggregate_patients, descriptive_summary, sample_balance

__all__ = ["Sample", "aggregate_patients", "descriptive_summary", "sample_balance"]
