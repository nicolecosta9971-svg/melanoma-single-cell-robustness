# Credits and contributions

## Nike Nicole Costa — project lead and portfolio maintainer

- **Research question and analysis unit:** I asked whether baseline T-cell/macrophage balance differed by immunotherapy response. I defined the score using cell-type percentages from each immune sample and averaged repeat-sample scores within each patient so that an extra biopsy did not count as an extra clinical outcome.
- **Implementation and analysis:** I built, ran and debugged the retrospective computational workflow using existing software, including Scanpy for preprocessing, scVI for integration and CellTypist for annotation. I implemented the patient-level comparisons and uncertainty checks described in the [methods](METHODS.md).
- **Robustness and interpretation:** I evaluated changes in processing and annotation, tested how alternative clinical and recovery definitions affected the comparison, and examined non-equivalent external cohorts separately. I documented where the group direction persisted, where individual scores shifted and why these results did not validate a biomarker. See the [case study](CASE_STUDY.md).

## Credits and boundaries

- **Original study:** The cited investigators recruited participants, collected biopsies, performed laboratory assays and sequencing, and supplied the clinical information and source annotations. I did not generate those biological data. [Source references](REFERENCES.md)
- **Existing methods:** I used established software, reference models and statistical methods. This project does not claim to have developed those tools or invented a new statistical method.
- **Teaching example:** The [synthetic bootstrap example](../scripts/run_bootstrap_demo.py) was prepared for this portfolio revision with AI coding assistance. It illustrates a bounded part of the analysis on invented counts; it is separate from the retained study workflow. [Reproducibility and scope](../REPRODUCIBILITY.md)

