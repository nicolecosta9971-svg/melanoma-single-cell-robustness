# Credits and contributions

## Nike Nicole Costa — project direction and analysis-code contribution

My contribution included project direction and personally writing or substantially editing, running and debugging analysis code for this retrospective reanalysis. This confirmed role does not assign sole authorship of every historical component or establish independent mastery of every method.

The workflow used Scanpy for preprocessing, scVI for integration and CellTypist for annotation. The patient-level endpoint averages baseline sample log-ratios within each patient. Processing, annotation, clinical, recovery and non-equivalent external comparisons remain separate from the retrospective primary reporting result; see [methods](METHODS.md) and the [case study](CASE_STUDY.md).

## Assistance and verification

The retained reanalysis used AI assistance in coding/debugging, planning and interpretation support, source/output auditing, and manuscript/figure documentation. This assistance was broader than the separate synthetic teaching examples. The retained record does not allocate every historical edit to a particular person or model. The maintainer remains responsible for verifying the claims; computational checks and assistant reviews are not independent human scientific peer review.

The [Zenodo report](https://doi.org/10.5281/zenodo.24164657) records the contribution, assistance and interpretation boundaries for report version 1.0.0-rc.6. Its DOI identifies the report archive, rather than this repository's software or a complete research workflow.

## Credits and boundaries

- **Original study:** The cited investigators recruited participants, collected biopsies, performed laboratory assays and sequencing, and supplied the clinical information and source annotations. I did not generate those biological data. [Source references](REFERENCES.md)
- **Existing methods:** I used established software, reference models and statistical methods. This project does not claim to have developed those tools or invented a new statistical method.
- **Teaching example:** The [synthetic bootstrap example](../scripts/run_bootstrap_demo.py) was prepared for this portfolio revision with AI coding assistance. It illustrates a bounded part of the analysis on invented counts; it is separate from the retained study workflow. [Reproducibility and scope](../REPRODUCIBILITY.md)

