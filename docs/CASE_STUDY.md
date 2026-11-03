# Case study: testing an association and its limits

## The question

Could a simple balance between fixed annotated T-cell and macrophage populations distinguish response groups in existing melanoma immunotherapy data? More importantly, which aspects of that observation survived scrutiny, and which did not?

The work is a retrospective reanalysis of investigator-generated public data. It is not a new clinical experiment, original data collection or the first analysis of immune-response relationships in this cohort. The endpoint was locked for subsequent checks after a historical association existed, rather than selected prospectively before outcomes were known.

## The measurement

For each baseline sample:

`log2((Tem/Trm cytotoxic T-cell percentage + 0.5) / (macrophage percentage + 0.5))`

Percentages use the recovered, QC-retained immune subset as denominator. The pseudocount is 0.5 percentage points. Sample log-ratios are then averaged within each patient. A ratio of mean percentages or pooled cell counts would answer a different question.

The fixed CellTypist label is not a purified CD8 state. Different-site records from one patient are not established technical replicates and do not create independent patient outcomes.

## What the evidence supports

The retrospective primary analysis included 22 baseline Poźniak patients, 10 R/12 NR, represented by 23 records and 14,801 cells. The median difference was 4.5988 log₂ units (95% patient-bootstrap interval 1.0392–6.5159; two-sided patient Mann–Whitney p=0.0134105). Within-cohort rank AUC was 0.8167 (0.6083–0.9750), a description of separation in these same patients—not validated clinical accuracy.

The historical p=0.00919942/AUC=0.833333 differs from the controlled result. Its full vector and uncertainty were not recovered. The discrepancy remains visible instead of being labelled exact reproduction.

Five predeclared same-cohort patient-level processing sensitivities, each using the same 10 R/12 NR, retained the positive group direction, but individual scores varied. Median differences ranged 4.3018–4.5677 log₂ units, AUC 0.8167–0.8500 and nominal p 0.006211–0.013411; each fit's patient-bootstrap intervals appear in the [processing figure](../figures/processing_stability.svg). These are setting ranges, not confidence intervals or five independent studies. Agreement of majority labels across 24,361 baseline/on-treatment integrated cells ranged 0.860515–0.957555; the maximum patient-score shift against the controlled vector reached 3.4576 log₂ units. Seed 0's median difference of 4.5236 differs from the controlled primary's 4.5988 despite their matching displayed p-value and AUC.

## What narrowed the interpretation

| Analysis class; patient unit; cohort and N | Effect and uncertainty | Statistical result and limitation |
| --- | --- | --- |
| Post-primary recovery adjustment; Poźniak, 10 R/12 NR | Adjusted mean difference 1.2820 log₂ units; HC3 95% interval −1.0699–3.6338 | p=0.2854; recovery independence not established; adjustment is not causal identification |
| Secondary joint sex/regimen adjustment; same 22 patients | Adjusted mean difference 3.2542; HC3 95% interval −0.2171–6.7255 | Nominal p=0.0661514; Holm-seven p=0.187682; sparse treatment overlap |
| Post-primary best-overall-response-only sensitivity; Poźniak, 6 R/11 NR | Median difference 2.6335; 95% interval −0.5279–6.2210 | p=0.121526; small same-cohort subset, not independent evidence |
| External direct-label sensitivity; GSE120575, 9 R/10 NR | Median difference 2.3882; 95% interval −0.8251–3.7171 | p=0.0550138; platform, annotation and response-definition differences |
| Fresh external mapped effector-memory sensitivity; same 19 GSE120575 patients | Median difference 2.2813; 95% interval −1.1981–3.3303 | p=0.130911; not equivalent to the primary or the older favourable preparation |
| External broad author-label sensitivity; Schlenker, 12 R+TF/10 PD | Median difference −0.9404; 95% interval −2.5371–1.0220 | p=0.222520; opposing but inconclusive, with different response coding and denominator |

Adjusted mean effects and primary median effects are different estimands; their magnitudes do not directly quantify attenuation. The cohorts were not pooled. The complete register remains preserved outside this selected portfolio package; this page is not a comprehensive per-setting report. See [figure captions](FIGURE_CAPTIONS.md) and [data availability](DATA_AVAILABILITY.md).

The author-annotation audit also constrained the biological label. In the same 22 baseline patients, only 4.94% of the patient-balanced fixed Tem/Trm mass overlapped the narrow author cytotoxic-CD8 state (pointwise 95% patient-bootstrap interval 3.06–7.02%). A broader, fixed four-author-CD8-state union overlapped 80.71% (76.70–84.51%). These are measurement overlaps, not accuracy or response tests; p-values are not applicable.

The four **patient-level Poźniak compositional sensitivities**, each using the same 10 R/12 NR, did not provide stable selection: macrophages were selected in two chains, with divergence flags in every chain. These are diagnostic summaries, not displayed posterior effect estimates or conventional p-value tests. Per-chain posterior quantities and conditional 94% HDIs remain in the complete retained record, not bundled here. Neither a favourable signature nor a significant primary test overrides these limitations.

## Exploratory biological follow-up

The retained exploratory analysis summed raw counts within baseline patient and fixed cell family, then compared six fixed signature scores with multiple-testing correction. Family eligibility required at least 20 recovered cells and was uneven between response groups, particularly for cytotoxic T cells. No cell-level or genome-wide differential-expression inference was substituted for patient-level analysis.

This compact summary does not reproduce any of the signature estimates or full pathway tables. The complete exploratory results, including both normalisations, remain preserved outside this package rather than selecting one favourable pathway for display. They are unadjusted for clinical confounding and cannot establish function or mechanism.

## Reproducibility is a separate question

A protected 40-stage verified-core profile completed all five processing fits and six computational audits. All 94 emitted CSVs matched a prior completed run under declared namespace normalisation; 55 were byte-identical. This is evidence about those outputs, not proof that every file or biological inference is correct.

That profile reused a primary vector. A separate earlier count-object reconstruction matched the controlled primary, not the historical summary. Neither is a FASTQ reconstruction or fully isolated reproduction on another machine; native R/base operating-system components remained reused. The public code in this candidate demonstrates the endpoint using synthetic observations only; it does not claim to package the private full pipeline. [Reproducibility](../REPRODUCIBILITY.md) distinguishes these observations from checks on the new public candidate.

## Research value and conclusion

The value is an inspectable example of patient-level design, uncertainty reporting and critical reanalysis: distinguishing bounded computational reproducibility from a clinically useful biomarker. The selected figures keep positive, inconclusive and opposing estimates together; the complete retained evidence also preserves all refusals and other settings.

A positive baseline association exists under the fixed definition in this retained cohort. Clinical independence, external confirmation and clinical utility remain unestablished. The most valuable scientific extension is not a more favourable model: it is an independently qualified pretreatment cohort and a frozen, equivalent-endpoint analysis plan.

See [methods](METHODS.md), [limitations](LIMITATIONS.md), [original-source references](REFERENCES.md), [contributions](CONTRIBUTIONS.md) and [source/disclosure boundaries](DATA_AVAILABILITY.md). Preparing this summary does not constitute a new statistical run or public-release clearance.
