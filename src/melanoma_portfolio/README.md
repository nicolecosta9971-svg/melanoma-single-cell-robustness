# Patient-level immune-balance calculation

A small, dependency-free Python example showing how to calculate sample immune-cell balances, aggregate repeated samples within patients, and summarise two invented groups.

**Maintainer:** N. N. Costa.

## Scope

The example contains **five invented sample records from four invented patients**, with two patients labelled `R` and two labelled `NR`. These labels are teaching placeholders—not clinical observations.

No research data, real patient records, clinical metadata, study findings, models or reference assets are included. This is an educational calculation, not the complete melanoma single-cell workflow or a clinically validated prediction model.

## Calculation

For each sample:

```text
sample score = log2((T-cell percentage + 0.5) /
                    (macrophage percentage + 0.5))
```

The percentages share the same denominator and represent disjoint cell categories. The pseudocount is **0.5 percentage points**, not 0.5 cells.

Each patient receives the arithmetic mean of their **sample scores**. This is not a ratio of mean percentages. Multiple samples from one person do not become independent patient outcomes.

The summary reports patient/group counts, the difference between group medians and a descriptive pairwise AUC. AUC gives half credit to tied pairs; it describes ordering in these invented observations, not predictive accuracy. **No p-value or confidence interval is calculated.**

## Run

Use Python 3.11 or 3.12. Only the Python standard library is required.

From the repository root:

```sh
python3 -B scripts/run_synthetic_demo.py
```

The program prints a JSON summary. Its `p_value` is deliberately `null`.

Run the tests from the same folder:

```sh
python3 -B -m unittest discover -s tests -v
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the verified local checks and their limits. A proposed [GitHub Actions workflow](.github/workflows/synthetic-checks.yml) checks tests, demonstration output and the package manifest; hosted CI has not been run.

## Code and tests

- `src/melanoma_portfolio/endpoint.py`: input validation, sample scores, patient aggregation and descriptive summaries.
- `src/melanoma_portfolio/demo.py`: invented observations and demonstration output.
- `src/melanoma_portfolio/__init__.py`: package entry.
- `scripts/run_synthetic_demo.py`: command-line entry point.
- `tests/test_endpoint.py`: 22 synthetic endpoint tests; additional package-contract tests check the starter's release boundaries.

The endpoint tests cover score symmetry and pseudocount units, aggregation order, repeated samples, input-order invariance, duplicate/conflicting records, invalid percentages and identifiers, missing response groups, AUC ties and orientation, and omission of patient identifiers and inferential p-values from the aggregate output.

These tests check the implemented example. They do not establish biological validity or reproduce a research cohort. The [release manifest](RELEASE_MANIFEST.json) describes the packaged files; it is not a scientific validation certificate.

## Background, attribution and licensing

The broader research context is melanoma immunotherapy and immune-cell composition. Original biological studies and their data deposit are credited in [SOURCES.md](SOURCES.md). Their investigators generated the experimental data; this example does not claim that work.

See [LICENSE](LICENSE) and the scope explained in [LICENSING.md](LICENSING.md). Referenced research resources retain their own terms; their citation does not grant redistribution rights.
