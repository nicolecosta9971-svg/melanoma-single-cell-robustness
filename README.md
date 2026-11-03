# Immune balance and melanoma immunotherapy response

A retrospective single-cell association and robustness case study, with selected aggregate figures and a runnable synthetic Python example.

**Maintainer:** N. N. Costa. This is a prepared local portfolio summary; preparation is not public-release, privacy or source-use clearance. See [data availability](docs/DATA_AVAILABILITY.md) and [source terms](docs/THIRD_PARTY_TERMS.md).

## Research question and conclusion

Was baseline balance between fixed CellTypist-defined T-cell and macrophage populations associated with response in the released Poźniak melanoma cohort?

A positive association was observed under the fixed definition, but **clinical independence, equivalent external confirmation and clinical utility remain unestablished**. This is not a clinically validated biomarker, prospective prediction study or causal experiment. The original investigators generated the biological data.

## Primary result, with its limits

The retrospective locked primary analysis uses baseline **patients**, not independent cells: **22 patients, 10 responders/12 nonresponders**, represented by 23 sample records and 14,801 retained cells.

For each baseline sample, calculate:

`log2((Tem/Trm cytotoxic T-cell % + 0.5)/(macrophage % + 0.5))`

Then average the **sample scores** within each patient. The pseudocount is 0.5 percentage points; the denominator is the recovered QC-retained immune subset, not whole-tumour tissue. Fixed CellTypist `Immune_All_Low` cluster-majority labels are retained. The T-cell label is not a purified CD8 state.

The controlled responder-minus-nonresponder median difference was **4.5988 log₂ units** (95% patient-bootstrap interval **1.0392–6.5159**; two-sided patient Mann–Whitney **p=0.0134105**). Descriptive within-cohort rank AUC was **0.8167** (95% interval **0.6083–0.9750**), not independently evaluated predictive accuracy.

The endpoint was locked after an earlier association existed; the p-value does not account for incomplete historical endpoint selection. Historical p=0.00919942/AUC=0.833333 differs from the controlled result, without a recovered historical vector or intervals. This disagreement is not labelled exact reproduction.

## Evidence that constrains the conclusion

- Five predeclared same-patient processing sensitivities retained positive direction, but individual scores changed. They are not five independent replications.
- In a secondary joint sex/regimen model of the same 22 patients, the adjusted **mean** difference was 3.2542 log₂ units (HC3 95% interval −0.2171–6.7255; nominal p=0.0661514; Holm-seven p=0.187682). Sparse treatment overlap limits adjustment. This mean effect is not the primary median estimand.
- Recovery adjustment and the best-overall-response-only subset were inconclusive. External comparisons were inconclusive or opposing and non-equivalent to the primary endpoint.
- Annotation definitions differed; compositional selection varied across all four chains with warnings in every chain. Exploratory pseudobulk eligibility was uneven and findings are not mechanistic evidence.

![Association estimates shown alongside uncertainty](figures/association_summary.svg)

## Explore the research

| Item | Purpose |
| --- | --- |
| [Case study](docs/CASE_STUDY.md) | Selected findings, uncertainty and balanced conclusion |
| [Methods](docs/METHODS.md) and [limitations](docs/LIMITATIONS.md) | Design choices, fixed endpoint and interpretation boundaries |
| [Participant flow](figures/participant_flow.svg) | Released cells → baseline records → patient endpoints |
| [All five processing fits](figures/processing_stability.svg) | Directional stability, intervals and individual-score instability |
| [All nine annotation overlaps](figures/annotation_overlap.svg) | Definition disagreement, not classification accuracy |
| [Figure captions](docs/FIGURE_CAPTIONS.md) | Analysis class, cohort, patient N, effects, uncertainty and limitations |

These are selected summaries, not a complete results register or a count of independent confirmations. Full results and private research evidence remain unchanged outside this package. No patient-level tables, clinical extracts, expression matrices or full aggregate exports are bundled. [Disclosure and source-use limits](docs/DATA_AVAILABILITY.md) still apply to aggregate figures.

## Run the Python example

Use Python 3.11 or 3.12. Only the standard library is required. From this folder:

```sh
python3 -B scripts/run_synthetic_demo.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_release.py
```

The example contains **five invented records from four invented patients**, two per group. It calculates sample log-ratios, patient means, descriptive group medians and tie-aware AUC. It deliberately calculates **no p-value or confidence interval**. Its output is not the real cohort result.

The included code does not run scVI, annotation, clinical models or the full research pipeline. [Reproducibility](REPRODUCIBILITY.md) distinguishes the synthetic checks, retained research output comparisons and unfinished raw-to-results boundaries. The earlier public starter's successful hosted checks do not certify this expanded package.

## Attribution and scope

See [references](docs/REFERENCES.md), [contributions](docs/CONTRIBUTIONS.md), [sources](SOURCES.md), [data availability](docs/DATA_AVAILABILITY.md) and [licensing scope](LICENSING.md). The existing [MIT licence](LICENSE) covers original software only, not all research content or source assets.

The most valuable scientific extension is an independently qualified pretreatment cohort with a documented expression-to-course-aligned patient-overall-response link and an outcome-blind harmonisation plan. This portfolio does not support treatment decisions.
