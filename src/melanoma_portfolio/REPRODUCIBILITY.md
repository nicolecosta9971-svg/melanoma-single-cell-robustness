# Reproducing the synthetic example

This starter checks a small arithmetic implementation, not the biological research. It contains no study vector, expression data, clinical records, annotation models or full raw-to-results workflow.

## Requirements and commands

Python 3.11 or 3.12; standard library only. No installation, account, network call, data download or additional package is required to run the example locally.

From this repository's root:

```sh
python3 -B scripts/run_synthetic_demo.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_release.py
```

The output describes five invented sample records from four invented patients, two in each group. The first invented patient has two samples; their two sample log-ratios are averaged before the between-group summary. Identifiers and individual scores are not printed in the summary. Descriptive AUC uses half credit for ties. The `p_value` is `null`; no significance test, confidence interval, model training or clinical prediction is implemented.

## Local verification and isolation

The starter was checked locally on 2 November 2026 using Python 3.11.16 and Python 3.12.14. Tests and demonstration were also run from a temporary standalone copy containing only the allowlisted starter files, without copying the research directory or adding it to the module search path. The isolated interpreter options `-I -S -B` ignore Python environment paths and site-package loading and prevent bytecode writes. These checks show that the tested standard-library example does not require the retained research files or installed scientific packages. The original filesystem was not access-blocked: this is not an operating-system sandbox, container or new-machine reproduction.

Checks cover:

- sample scores, percentage-point pseudocount, patient aggregation, group summaries and tie handling;
- invalid inputs, repeated records and inconsistent response labels;
- the exact allowlisted files, content fingerprints, local documentation links and bounded sensitive-content patterns;
- the synthetic-only fixture, code imports, licensing scope and standalone execution.

The [manifest](RELEASE_MANIFEST.json) records file sizes and SHA-256 fingerprints, excluding its own bytes. It is an integrity aid, not a digital signature or proof of ownership, authorship, legal clearance or scientific validity. The checker ignores an eventual `.git` directory; it does not inspect repository history. Do not regenerate a manifest merely to conceal an unexplained mismatch.

## What is not established

Passing these tests does not verify source biological labels, baseline eligibility, response definitions, cohort independence, causal effects, biomarker validity or the numerical results of the separate retrospective melanoma study. No claim of full study reproduction is made.

The proposed GitHub Actions configuration runs only these local synthetic/package checks with read-only repository permissions. GitHub-hosted CI has not run. Its checkout and Python-setup steps need network access on a hosted runner; the example itself does not download data or models.
