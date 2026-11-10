# Reproducibility: what is and is not supplied

This portfolio contains two runnable synthetic Python examples, selected aggregate research figures and methods. It does not include the full research workflow, full aggregate register, expression data, patient vectors, clinical tables, scientific environments, model weights or reference assets.

## Check this package

Python 3.11 or 3.12 and the standard library are sufficient:

```sh
python3 -I -S -B scripts/run_bootstrap_demo.py --draws 5000 --seed 18
python3 -I -S -B scripts/run_synthetic_demo.py
python3 -I -S -B -m unittest discover -s tests -v
python3 -I -S -B scripts/check_release.py
```

### How to read the new demo

- **Input and unit:** Hard-coded invented baseline sample counts include unequal cell yields, repeat samples and zero counts. Each sample's T-cell and macrophage counts are divided by its own recovered immune-cell count. Add the pseudocount in **percentage points**, take the log₂ ratio, then average sample scores within each patient. Larger biopsies do not get more weight.
- **Bootstrap:** Resample the patient scores with replacement within each response group, keeping both group sizes fixed. Compute the responder-minus-nonresponder median difference for each draw. The 2.5th and 97.5th percentiles form a pointwise interval. The demo uses a seeded Python random generator; it does not reproduce the retained research's NumPy draw sequence.
- **Sensitivity:** Repeat at 0.05, 0.1, 0.25, **0.5** (the reference), 1, 2 and 5 percentage points. Reuse the same patient draw indices across settings so changes are not driven by different random resamples. Separately, omit each patient once and report the minimum and maximum estimates. This omission range is not a confidence interval; the settings and omissions do not add independent patients or replications.
- **Scope:** This is an illustration of uncertainty and influence, conditional on the invented counts, fixed labels and recorded response groups. It does not measure annotation or processing uncertainty, calculate a p-value, or run integration, annotation or clinical adjustment. The older arithmetic demo still reports a descriptive AUC and no bootstrap interval.

The tests cover endpoint arithmetic, patient aggregation, synthetic resampling and sensitivity, invalid inputs, AUC ties/orientation and package contracts. The checker binds exactly 30 files, checks local links, passive accessible SVGs and bounded sensitive-content patterns. The manifest excludes its own bytes. A manifest does not authenticate itself, inspect Git history or certify rights, privacy, scientific validity or personal proficiency.

The `-I -S -B` flags disable environment import paths and site packages and avoid writing bytecode. This is not OS isolation; the rest of the filesystem is not access-blocked.

## Previous hosted checks versus this revision

The previous public version at [commit 6cf5ca2](https://github.com/nicolecosta9971-svg/melanoma-single-cell-robustness/tree/6cf5ca203fb32692647b5d15bc12f77a9468116e) passed [workflow run 41566831668](https://github.com/nicolecosta9971-svg/melanoma-single-cell-robustness/actions/runs/41566831668) on Python 3.11 and 3.12. That run did not include the new bootstrap demo. The workflow in this revision runs both synthetic examples and the package checks; it does not run the research models.

## Retained research reproduction

The retained private evidence records a completed 40-stage verified-core profile, five fixed integration fits and six computational audits. All 94 emitted CSVs matched a prior completed sensitivity run after declared path/run-ID normalisation: 55 byte-identical and 39 namespace-only differences. Another 144 non-CSV outputs were integrity-only checks; 52 source CSVs were outside the emitted comparison.

The profile **reused the designated primary vector**. A separate earlier reconstruction from a processed count object matched the controlled primary, not the historical summary. Historical p/AUC disagreement remains documented; unavailable historical effects and intervals were not replaced with controlled uncertainty.

Native R/base/macOS were reused and not every compiled binary was byte-hashed. No complete FASTQ reconstruction, upstream export/cell-lineage bridge, changed-machine reproduction or fully isolated raw-to-results build is claimed. An earlier storage-stopped attempt and genuine stochastic-output disagreement remain preserved. Clinical and author-annotation audits were separate from the 40 stages.

These facts describe retained computational evidence, not an independent human scientific review or a complete public reproduction package. Readers cannot regenerate the research results from this package.

## Scientific content in this summary

The selected SVGs display saved estimates, intervals and diagnostics; no model was refit and no scientific number changed to prepare this folder. Two copied figure footers were adapted to refer to the included captions rather than a non-bundled complete results register. The source figures, full results and all earlier research evidence remain unchanged.

Historical and controlled results remain separate. The public summary preserves clinical, recovery and external uncertainty, all four compositional chains' warning/selection context, annotation disagreement and uneven exploratory eligibility. It is not comprehensive per-setting reporting; full data and operational receipts are deliberately not redistributed.

See [methods](docs/METHODS.md), [captions](docs/FIGURE_CAPTIONS.md), [limitations](docs/LIMITATIONS.md), [data availability](docs/DATA_AVAILABILITY.md) and [source-specific terms](docs/THIRD_PARTY_TERMS.md). Software success does not supply biological validation or redistribution clearance.
