# Limitations and future work

These are scientific constraints, not problems resolved by a polished repository, passing tests or a DOI.

| Limitation | Consequence |
| --- | --- |
| Retrospective endpoint selection | The primary reporting endpoint was locked after an earlier result existed. Full earlier search history is unavailable; its p-value does not correct for endpoint selection. |
| Small, selected released cohort | Independent clinical N is 22 patients, not thousands of cells. The supplied immune subset does not establish representativeness of all treated patients or whole-tumour abundance. |
| Mixed clinical response definitions | The primary field mixes best-overall and pathological response. The more uniform BOR-only subset is inconclusive. Labels were not changed after inspecting results. |
| Sparse regimen overlap | Joint and regimen-adjusted estimates are imprecise; favourable one-field models do not establish clinical independence. Exact small treatment-stratum counts are not reproduced in this summary. |
| Recovery dependence | The endpoint is strongly associated with recovered-cell yield. Fractions conditional on recovery are not absolute infiltration. Yield adjustment/restriction neither proves artefact nor identifies a causal effect. |
| Sample relationships | One patient has two baseline records from different sites; technical replication is not established. Mean sample log-ratio aggregation does not remove sampling uncertainty. |
| Annotation uncertainty | The fixed Tem/Trm label spans multiple author states rather than purified cytotoxic CD8 cells. Myeloid overlap is asymmetric. Literal cycling/doublet-labelled records remain unresolved, not removed after inspecting agreement. |
| Processing scope | Integration used baseline plus on-treatment cells. Patient scores varied across seeds despite a consistent group direction. No comprehensive formal integration-quality benchmark establishes optimal processing. |
| Compositional warnings | Selection differed across all four retained scCODA chains: seeds 19/21 selected macrophages, whereas 18/20 selected no type. Every chain had divergence flags. Conditional 94% HDIs alone are not definitive corroboration, and are not conventional p-values. |
| Exploratory eligibility | Family-specific pseudobulk eligibility is uneven. Fixed signature associations are unadjusted for clinical confounding and do not establish cellular function or mechanism. |
| External non-equivalence | Platforms, annotations, denominators and clinical definitions differ. Findings were inconclusive or opposing; there is no equivalent independent endpoint confirmation. |
| Uncertainty scope | Bootstrap intervals condition on observed patients and saved processing. They do not capture all recruitment, assay, annotation or selection uncertainty. Setting ranges are not population confidence intervals. |
| Upstream and numerical provenance | FASTQ processing, the published/exported cell bridge and full upstream cell lineage were not reconstructed. Historical and controlled primary summaries disagree; the historical vector/intervals are unavailable. |
| Reproduction scope | The qualified verified-core profile reused a primary vector and native R/base OS. Matching declared CSV outputs is not full changed-machine, isolated raw-to-results reproduction. Public synthetic code is not the private pipeline. |

No untreated or alternative-treatment comparator establishes a treatment-specific predictive effect. Same-cohort AUC is rank separation, not independently evaluated clinical prediction. No result supports removing macrophages, assigning treatment, or claiming causality or clinical utility.

## Most valuable scientific extension

Qualify an independent pretreatment tumour cohort with a documented chain from patient to physical biopsy, expression library and course-aligned patient-overall response. Establish eligibility using authorised/public metadata **before** expression acquisition or endpoint testing. Then freeze an outcome-blind harmonisation and analysis plan, preserving this project's locked primary result.

Current candidate-cohort HOLD decisions represent unresolved eligibility, not negative association results. No new expression testing, author contact or restricted-record access is part of this candidate.

## Useful improvements that do not change the conclusion

- Genuine human biological/statistical appraisal and accurate personal-contribution documentation.
- Resource-specific permissions/privacy decisions and a reviewed redistribution scope.
- A source-export cell bridge and broader integration/annotation appraisal, if separately authorised.
- A later changed-machine reproduction with explicitly scoped portable environments.

More complex models or more significant p-values are not prerequisites for an honest retrospective portfolio. Stronger biomarker language requires stronger independent evidence.

## Release and testing are separate boundaries

Public availability, successful synthetic checks and matching a package manifest do not certify the research contents, redistribution rights or biological interpretation. The [reproduction record](../REPRODUCIBILITY.md), [data availability](DATA_AVAILABILITY.md) and [source terms](THIRD_PARTY_TERMS.md) separate these decisions from the scientific limitations above. Not reproducing clinical rows or small-stratum tables is not a guarantee against reconstructing subgroup information from linked public sources.
