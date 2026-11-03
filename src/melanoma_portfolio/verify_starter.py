"""Private review of a new synthetic-only starter; never a public upload item."""

import argparse
import difflib
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
STARTER = PROJECT / "github_portfolio_starter_2026-11-02_01"
RESEARCH_PINS = PROJECT / "github_portfolio_preparation_2026-11-02_01/protected_before_01.json"
PREVIOUS_RECEIPT = PROJECT / "github_portfolio_licensing_2026-11-02_01/licensing_validation_01.json"
PREVIOUS = PROJECT / "github_portfolio_candidate_2026-11-02_03"
ALLOWLIST = {
    ".github/workflows/synthetic-checks.yml", ".gitignore", "LICENSE", "LICENSING.md", "README.md",
    "REPRODUCIBILITY.md", "SOURCES.md", "RELEASE_MANIFEST.json", "scripts/check_release.py",
    "scripts/run_synthetic_demo.py", "src/melanoma_portfolio/__init__.py", "src/melanoma_portfolio/demo.py",
    "src/melanoma_portfolio/endpoint.py", "tests/test_endpoint.py", "tests/test_package.py",
}
UNCHANGED_CODE = ("src/melanoma_portfolio/__init__.py", "src/melanoma_portfolio/endpoint.py", "tests/test_endpoint.py", "LICENSE")
RUNTIMES = (
    PROJECT / "recovery_2026-10-15/runtime/core/bin/python",
    Path("/Users/nicolecosta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"),
)


def pin(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("Expected regular non-symlink file")
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def tree(root):
    return {p.relative_to(root).as_posix(): pin(p) for p in sorted(root.rglob("*")) if p.is_file() or p.is_symlink()}


def emit_manifest_patch():
    actual = tree(STARTER)
    expected = ALLOWLIST - {"RELEASE_MANIFEST.json"}
    if set(actual) - {"RELEASE_MANIFEST.json"} != expected:
        raise ValueError("Unexpected starter file set")
    doc = {
        "schema_version": 1, "scope": "Synthetic-only local starter; not a scientific reproduction or published release",
        "excludes_itself_by_design": True,
        "files": {rel: v for rel, v in actual.items() if rel != "RELEASE_MANIFEST.json"},
    }
    path = STARTER / "RELEASE_MANIFEST.json"
    new = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    print("*** Begin Patch")
    if path.exists():
        old = path.read_text(encoding="utf-8")
        print(f"*** Update File: {path}")
        for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=1))[2:]:
            print("@@" if line.startswith("@@") else line)
    else:
        print(f"*** Add File: {path}")
        for line in new.splitlines():
            print("+" + line)
    print("*** End Patch")


def verify():
    output = HERE / "starter_validation_01.json"
    if output.exists():
        raise ValueError("Use an unused validation receipt")
    before = tree(STARTER)
    prior = json.loads(PREVIOUS_RECEIPT.read_text(encoding="utf-8"))
    if prior["status"] != "passed":
        raise ValueError("Previous candidate did not pass its recorded checks")
    previous_pins = prior["candidate_fingerprints"]
    previous_now = tree(PREVIOUS)
    previous_changes = [rel for rel in set(previous_pins) | set(previous_now) if previous_pins.get(rel) != previous_now.get(rel)]
    research_pins = json.loads(RESEARCH_PINS.read_text(encoding="utf-8"))["files"]
    research_changes = [rel for rel, v in research_pins.items() if pin(PROJECT / rel) != v]
    unchanged_code = {rel: before.get(rel) == previous_pins[rel] for rel in UNCHANGED_CODE}
    checks, demo_outputs = [], []
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for runtime in RUNTIMES:
        for args in (["--version"], ["-I", "-S", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], ["-I", "-S", "-B", "scripts/run_synthetic_demo.py"], ["-I", "-S", "-B", "scripts/check_release.py"]):
            r = subprocess.run([str(runtime), *args], cwd=STARTER, env=env, capture_output=True, text=True, timeout=60)
            checks.append({"runtime": str(runtime), "location": "starter", "arguments": args, "returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
            if "scripts/run_synthetic_demo.py" in args:
                demo_outputs.append(r.stdout)
    with tempfile.TemporaryDirectory(prefix="melanoma_synthetic_starter_") as temporary:
        sandbox = Path(temporary)
        isolated = sandbox / "starter"
        for rel in ALLOWLIST:
            destination = isolated / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((STARTER / rel).read_bytes())
        copied_before = tree(isolated)
        for runtime in RUNTIMES:
            for args in (
                ["-I", "-S", "-B", "-m", "unittest", "discover", "-s", str(isolated / "tests"), "-v"],
                ["-I", "-S", "-B", str(isolated / "scripts/run_synthetic_demo.py")],
                ["-I", "-S", "-B", str(isolated / "scripts/check_release.py")],
            ):
                r = subprocess.run([str(runtime), *args], cwd=sandbox, env=env, capture_output=True, text=True, timeout=60)
                checks.append({"runtime": str(runtime), "location": "standalone copy from unrelated working directory", "arguments": [arg.replace(str(isolated), "<standalone>") for arg in args], "returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr.replace(str(isolated), "<standalone>")})
                if any(arg.endswith("run_synthetic_demo.py") for arg in args):
                    demo_outputs.append(r.stdout)
        copied_after = tree(isolated)
        copy_same = copied_before == copied_after == before
    after = tree(STARTER)
    equal_outputs = len(demo_outputs) == 4 and len(set(demo_outputs)) == 1
    expected_demo = json.loads(demo_outputs[0])
    synthetic_counts = expected_demo["results"]["n_samples"] == 5 and expected_demo["results"]["n_patients"] == 4 and expected_demo["results"]["n_R"] == expected_demo["results"]["n_NR"] == 2 and expected_demo["results"]["p_value"] is None
    passed = set(before) == ALLOWLIST and before == after and not previous_changes and not research_changes and all(unchanged_code.values()) and copy_same and equal_outputs and synthetic_counts and all(r["returncode"] == 0 for r in checks)
    report = {
        "status": "passed" if passed else "failed", "date": "2026-11-02", "candidate": STARTER.name,
        "candidate_fingerprints": after, "exact_file_set": set(before) == ALLOWLIST,
        "candidate_unchanged_by_execution": before == after,
        "previous_candidate_files_checked": len(previous_pins), "previous_candidate_changes": sorted(previous_changes),
        "protected_research_files_checked": len(research_pins), "protected_research_changes": research_changes,
        "copied_core_files_byte_identical": unchanged_code,
        "standalone_copy_file_set_and_bytes_unchanged": copy_same,
        "demo_stdout_identical_across_four_runs": equal_outputs,
        "synthetic_counts_and_null_p_verified": synthetic_counts,
        "synthetic_demo_output": expected_demo, "checks": checks,
        "research_analysis_changed": False, "git_or_public_action": False,
        "scope": "Original synthetic implementation and local isolation/package checks only; no OS-level sandbox, hosted CI, human proficiency assessment, full scientific reproduction or privacy/legal clearance",
    }
    with output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "starter_files": len(after), "starter_bytes": sum(v["bytes"] for v in after.values()), "previous_candidate_changes": len(previous_changes), "protected_research_changes": len(research_changes), "isolated_copy_unchanged": copy_same, "demo_outputs_identical": equal_outputs, "nonzero_checks": sum(r["returncode"] != 0 for r in checks)}))
    return 0 if passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("manifest", "verify"))
    args = parser.parse_args()
    if args.action == "manifest":
        emit_manifest_patch()
    else:
        raise SystemExit(verify())
