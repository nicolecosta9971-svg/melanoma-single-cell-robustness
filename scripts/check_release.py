"""Read-only file, link and SVG checks for the exact local portfolio package.

Not a privacy/legal/authorship certificate or an inspection of Git history.
"""

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 100_000
ALLOWED_FILES = frozenset({
    ".github/workflows/synthetic-checks.yml", ".gitignore", "LICENSE",
    "LICENSING.md", "README.md", "REPRODUCIBILITY.md", "SOURCES.md",
    "RELEASE_MANIFEST.json", "scripts/check_release.py",
    "scripts/run_synthetic_demo.py", "src/melanoma_portfolio/__init__.py",
    "src/melanoma_portfolio/demo.py", "src/melanoma_portfolio/endpoint.py",
    "tests/test_endpoint.py", "tests/test_package.py",
    "docs/CASE_STUDY.md", "docs/CONTRIBUTIONS.md",
    "docs/DATA_AVAILABILITY.md", "docs/FIGURE_CAPTIONS.md",
    "docs/LIMITATIONS.md", "docs/METHODS.md", "docs/REFERENCES.md",
    "docs/THIRD_PARTY_TERMS.md", "figures/participant_flow.svg",
    "figures/association_summary.svg", "figures/processing_stability.svg",
    "figures/annotation_overlap.svg",
})
PATTERNS = {
    "personal path": re.compile(r"/(?:Users|Volumes)/"),
    "patient reference": re.compile(r"\bpatient[_ -]?\d+\b", re.I),
    "source patient key": re.compile(r'"(?:patient_ID|sample_ID|left_out_patient_ID)"'),
    "private key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "known token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})"),
    "credential URL": re.compile(r"https?://[^\s/@:]+:[^\s/@]+@"),
}


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def validate_svg(text):
    """Check passive accessible presentation, not biological correctness."""
    if "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
        return ["Unexpected XML declaration"]
    try:
        tree = ET.fromstring(text)
    except ET.ParseError:
        return ["Malformed SVG"]
    namespace = "{http://www.w3.org/2000/svg}"
    if tree.tag != namespace + "svg":
        return ["Unexpected SVG root namespace"]
    errors = []
    labels = tree.attrib.get("aria-labelledby", "").split()
    if tree.attrib.get("role") != "img" or not labels:
        errors.append("SVG missing accessible role/labels")
    ids = {element.attrib["id"] for element in tree.iter() if "id" in element.attrib}
    if any(label not in ids for label in labels):
        errors.append("SVG has unresolved accessible label reference")
    for name in ("title", "desc"):
        element = tree.find(namespace + name)
        if element is None or not (element.text or "").strip() or element.attrib.get("id") not in labels:
            errors.append("SVG missing referenced title/description")
    for element in tree.iter():
        if element.tag.split("}")[-1].lower() in ("script", "foreignobject", "image", "a", "style"):
            errors.append("Unexpected active or external SVG element")
        for key, value in element.attrib.items():
            if key.lower().startswith("on") or "href" in key.lower() or "url(" in value.lower():
                errors.append("SVG event handler or linked resource")
    return errors


def _read_text(path):
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Unexpected large artifact")
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError("Artifact grew beyond size limit")
    return data.decode("utf-8"), data


def validate(root=ROOT):
    root = Path(root).resolve()
    errors, actual = [], set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[0] == ".git":
            continue
        rel = relative.as_posix()
        for label, pattern in PATTERNS.items():
            if pattern.search(rel):
                errors.append(f"Filename pattern requiring review ({label}): {rel}")
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
        errors.append("Portfolio file set differs from the explicit allowlist")
    manifest_path = root / "RELEASE_MANIFEST.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        return errors + ["Missing regular manifest"]
    try:
        manifest_text, _ = _read_text(manifest_path)
        manifest = json.loads(manifest_text)
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
    for pin in pins.values():
        if not isinstance(pin, dict) or set(pin) != {"bytes", "sha256"} or isinstance(pin.get("bytes"), bool) or not isinstance(pin.get("bytes"), int) or pin["bytes"] < 0 or not isinstance(pin.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]):
            errors.append("Malformed manifest fingerprint entry")
    for rel in sorted(actual & ALLOWED_FILES):
        path = root / rel
        try:
            text, data = _read_text(path)
        except (OSError, UnicodeError, ValueError):
            errors.append(f"Unreadable, oversized or non-UTF-8 file: {rel}")
            continue
        if rel != "RELEASE_MANIFEST.json" and pins.get(rel) != {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}:
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
        if path.suffix == ".svg":
            errors.extend(f"{rel}: {error}" for error in validate_svg(text))
    return errors


def main():
    errors = validate()
    print(json.dumps({
        "status": "passed" if not errors else "failed",
        "files_expected": len(ALLOWED_FILES), "errors": errors,
        "scope": "Exact local portfolio files; synthetic code and bounded file/link/SVG checks, not research reproduction, rights/privacy clearance or Git-history inspection",
    }, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
