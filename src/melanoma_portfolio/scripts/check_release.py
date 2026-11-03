"""Read-only integrity and bounded content checks for this synthetic starter.

Not a privacy/legal/authorship certificate or an inspection of Git history.
"""

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FILES = frozenset({
    ".github/workflows/synthetic-checks.yml", ".gitignore", "LICENSE",
    "LICENSING.md", "README.md", "REPRODUCIBILITY.md", "SOURCES.md",
    "RELEASE_MANIFEST.json", "scripts/check_release.py",
    "scripts/run_synthetic_demo.py", "src/melanoma_portfolio/__init__.py",
    "src/melanoma_portfolio/demo.py", "src/melanoma_portfolio/endpoint.py",
    "tests/test_endpoint.py", "tests/test_package.py",
})
PATTERNS = {
    "personal path": re.compile(r"/(?:Users|Volumes)/"),
    "private key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "known token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})"),
    "credential URL": re.compile(r"https?://[^\s/@:]+:[^\s/@]+@"),
}


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def validate(root=ROOT):
    root = Path(root).resolve()
    errors, actual = [], set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[0] == ".git":
            continue
        rel = relative.as_posix()
        if path.is_symlink():
            errors.append(f"Symlink not allowed: {rel}")
            continue
        if path.is_dir():
            continue
        if not path.is_file():
            errors.append(f"Nonregular file: {rel}")
            continue
        actual.add(rel)
    if actual != ALLOWED_FILES:
        errors.append("Starter file set differs from the explicit allowlist")
    manifest_path = root / "RELEASE_MANIFEST.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        return errors + ["Missing regular manifest"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return errors + ["Unreadable or malformed manifest"]
    keys = {"schema_version", "scope", "excludes_itself_by_design", "files"}
    if not isinstance(manifest, dict) or set(manifest) != keys:
        return errors + ["Unexpected manifest schema"]
    pins = manifest["files"]
    if manifest["schema_version"] != 1 or manifest["excludes_itself_by_design"] is not True:
        errors.append("Unexpected manifest version/self-exclusion")
    if not isinstance(pins, dict):
        return errors + ["Invalid manifest file map"]
    if set(pins) != ALLOWED_FILES - {"RELEASE_MANIFEST.json"}:
        errors.append("Manifest does not bind exactly the allowed non-manifest files")
    for rel in sorted(actual & ALLOWED_FILES):
        path = root / rel
        if path.stat().st_size > 100_000:
            errors.append(f"Unexpected large file: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"Unreadable or non-UTF-8 file: {rel}")
            continue
        if rel != "RELEASE_MANIFEST.json" and pins.get(rel) != fingerprint(path):
            errors.append(f"Fingerprint mismatch: {rel}")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                errors.append(f"Pattern requiring review ({label}): {rel}")
        if path.suffix == ".md":
            for raw in re.findall(r"\]\(([^\n)]+)\)", text):
                target = raw.split(' "', 1)[0].strip("<>")
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
                if not destination.is_relative_to(root) or not destination.is_file():
                    errors.append(f"Missing or nonportable local link: {rel}")
    return errors


def main():
    errors = validate()
    print(json.dumps({
        "status": "passed" if not errors else "failed",
        "files_expected": len(ALLOWED_FILES), "errors": errors,
        "scope": "Synthetic starter only; bounded integrity/link/content checks, not rights/privacy/scientific clearance or Git-history inspection",
    }, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
