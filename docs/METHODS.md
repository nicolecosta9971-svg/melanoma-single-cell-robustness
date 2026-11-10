# Methods and interpretation

## Design and source

Retrospective secondary analysis of the Poźniak/SPECIAL investigators' publicly deposited processed immune-cell RNA count object, KU Leuven dataset version 7. Original recruitment, biopsies, sequencing and source annotations were performed by the original investigators. Their Cell study and same-cohort immune-focused companion both require attribution; see [references](REFERENCES.md).

The input export contained 25,178 cells and 22,897 RNA features. This is a selected immune subset, not all enrolled patients, whole-tumour composition or FASTQ data. The published-versus-exported cell-count bridge and upstream lineage remain incomplete.

## Processing represented by the retained analysis

- Cells required at least 200 detected genes and mitochondrial-count percentage below 20; genes required detection in at least three cells.
- QC retained 24,361 cells from 45 baseline and on-treatment samples. Integration/annotation used both timepoints; endpoint inference used baseline only.
- Counts were retained separately. Expression was total-normalised to 10,000, log1p-transformed and used to select 3,000 highly variable genes with the Scanpy `seurat` flavour, without an HVG batch key.
- scVI used HVG counts, sample ID as batch covariate, a negative-binomial likelihood, 30 latent dimensions and up to 100 epochs with early stopping. Response and timepoint were not supplied as model covariates.
- A 15-neighbour latent-space graph and Leiden resolution 0.8 supplied the fixed clustering. UMAP was visualisation, not clinical inference. An outcome-blind historical rationale for selecting resolution 0.8 is not established.
- CellTypist classified broader retained log-normalised expression rather than scaled HVGs. The locked labels were `Immune_All_Low` cluster-majority assignments. The exact numerator label was `Tem/Trm cytotoxic T cells`; it was not newly restricted to CD8.

These describe the retained scientific workflow, not procedures rerun for this package. Selected figures display saved aggregate estimates; the complete register and scientific inputs are not bundled. The runnable examples illustrate the patient endpoint, bootstrap and sensitivity checks with **invented data**, not a complete implementation of the scientific workflow. See [reproducibility](../REPRODUCIBILITY.md).

## Locked primary measurement and test

Include available baseline (`BT`) records with the original R/NR response field. Compute the two fixed family percentages using all QC-retained cells in each baseline immune sample:

`sample_score = log2((Tem/Trm cytotoxic T-cell % + 0.5) / (macrophage % + 0.5))`

Then take the arithmetic mean of available baseline sample scores within each patient. The 0.5 addition is in **percentage points**. Do not substitute a ratio of patient-mean percentages, pooled counts or independently tested repeated records. Different-site samples are not established technical replicates.

The primary comparison is a two-sided patient-level Mann–Whitney U test in 10 responders and 12 nonresponders. Pinned SciPy `method='auto'` uses the asymptotic procedure at these group sizes with default continuity/tie handling. R-minus-NR median difference and rank AUC receive within-response patient-percentile bootstrap intervals: 5,000 resamples, NumPy `default_rng` seed 18. AUC is U/(10×12), oriented toward higher scores in responders; it is not a held-out accuracy estimate. The median-difference interval and rank-test p-value target different summaries.

“Primary” denotes the fixed retrospective reporting endpoint. It was locked after an earlier association existed; incomplete earlier selection history and uncorrected selection uncertainty remain limitations.

## Sensitivity and secondary analyses

| Component | Fixed approach and interpretation boundary |
| --- | --- |
| Processing | Five seeds 0–4, fixed scientific parameters, no preferred seed. Fits are dependent checks, not independent patient cohorts. |
| Pseudocounts | 0.05, 0.1, 0.25, 0.5, 1, 2 and 5 percentage points; primary remains 0.5. |
| Alternative annotation | Direct CellTypist, fixed marker gates and reference-mapped definitions kept separate. Agreement does not establish truth. |
| Author-label measurement audit | Sample joint fractions averaged within patient, then equal patient weights. Nine prespecified overlap ratios, whole-patient percentile bootstrap, 5,000 resamples, seed 20261016; pointwise intervals, no hypothesis or response tests. No relabelling/removal. |
| Recovery | Yield associations, thresholds, influence and resampling checks, followed by explicitly post-primary yield adjustment/common-support restriction. Not causal adjustment or proof of artefact. |
| scCODA | Baseline patient-summed counts over 13 types; automatically selected regulatory-T reference, expected FDR 0.05, four seeds 18–21 and 5,000 retained draws per chain. Different estimand/aggregation from the primary. All four chains, conditional package 94% HDIs and diagnostics retained; every chain had divergence flags and final selection differed. Conventional p-values are not applicable. |
| Clinical models | Seven secondary models fixed after seeing primary/metadata distributions; OLS score outcome, response coefficient as adjusted mean difference, HC3 normal-approximation intervals/tests. Six estimable models, age-band complexity refusal, no imputation. Holm family retains all seven, internally assigning p=1 to refusal without reporting a fictitious estimated effect. |
| Response definitions | Original labels unchanged; best-overall-response-only sensitivity separate. Pathological-only subset descriptive, not inferential. |

Public clinical Table S1 matched all 45 immune samples on audited fields. Age bands, recorded sex flag, stage, regimen, tissue and protocol were available; exact age and true sequencing batch were not. Protocol was not relabelled as batch. Source response coding mixed best-overall and pathological response. Sparse regimen overlap limits adjustment.

## Exploratory biological follow-up

Raw counts were summed within baseline patient and fixed cell family. At least 20 recovered family cells were required. Fixed signatures used mean log₂(CPM+1), with library totals across all 22,897 exported RNA features. These are patient signature-score comparisons, not cell-level or genome-wide differential-expression inference. All six full-RNA contrasts received BH correction; a separate 12-dependent-test comparison across normalisations remains distinct. Eligibility differed by family and was particularly uneven for cytotoxic T cells. Clinical score adjustment was not applied to these signatures.

## External evidence

GSE120575 used 19 designated baseline patients, Smart-seq2 log₂(TPM+1) expression and distinct label/mapping preparations. Retained response metadata do not resolve uniform patient-overall best response, lesion-level coding or assessment timing. Schlenker used author annotations, different immune denominators and R+TF/PD coding including adjuvant treatment-failure cases. These were separate sensitivities, not equivalent-endpoint confirmation. No cohort pooling was performed.

Selected results, uncertainty, patient N, analysis class and limitations are in the [case study](CASE_STUDY.md), [figures and captions](FIGURE_CAPTIONS.md). Complete per-setting, compositional and exploratory tables remain outside this smaller package. Conventional sensitivities are not one retrospectively corrected confirmation family; explicit Holm/BH families are distinguished. Annotation intervals are pointwise, not simultaneous; the measurement audit adds no independent patients or clinical-response tests. [Source terms](THIRD_PARTY_TERMS.md) and [data availability](DATA_AVAILABILITY.md) remain distinct from statistical methods.
