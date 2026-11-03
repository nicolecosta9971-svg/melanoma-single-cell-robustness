"""Synthetic code and bounded presentation contracts, not study reproduction."""

import ast
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from melanoma_portfolio.demo import run, synthetic_samples

spec = importlib.util.spec_from_file_location("starter_checks", ROOT / "scripts/check_release.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class PackageTests(unittest.TestCase):
    def sandbox(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "portfolio"
        for rel in checks.ALLOWED_FILES:
            destination = root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, destination)
        return root

    def test_exact_portfolio_contract(self):
        self.assertEqual(len(checks.ALLOWED_FILES), 27)
        self.assertEqual(checks.validate(), [])

    def test_unlisted_file_refused(self):
        root = self.sandbox()
        (root / "unlisted.txt").write_text("synthetic extra", encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_missing_file_refused(self):
        root = self.sandbox()
        (root / "README.md").unlink()
        self.assertTrue(checks.validate(root))

    def test_filename_privacy_pattern_refused(self):
        root = self.sandbox()
        (root / ("patient" + "_987654.txt")).write_text("invented negative fixture", encoding="utf-8")
        errors = checks.validate(root)
        self.assertTrue(any("Filename pattern requiring review" in error for error in errors))

    def test_changed_code_refused(self):
        root = self.sandbox()
        path = root / "src/melanoma_portfolio/endpoint.py"
        path.write_text(path.read_text(encoding="utf-8") + "\n# synthetic mutation\n", encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_missing_manifest_entry_refused(self):
        root = self.sandbox()
        path = root / "RELEASE_MANIFEST.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["files"].pop("LICENSE")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_manifest_cannot_hash_itself(self):
        root = self.sandbox()
        path = root / "RELEASE_MANIFEST.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["files"]["RELEASE_MANIFEST.json"] = {"bytes": 0, "sha256": "synthetic"}
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_malformed_manifest_refused(self):
        root = self.sandbox()
        (root / "RELEASE_MANIFEST.json").write_text("{", encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_nonobject_manifest_refused(self):
        root = self.sandbox()
        (root / "RELEASE_MANIFEST.json").write_text("[]", encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_malformed_manifest_pin_refused(self):
        root = self.sandbox()
        path = root / "RELEASE_MANIFEST.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["files"]["LICENSE"] = {"bytes": True, "sha256": "not a digest"}
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(checks.validate(root))

    def test_symlink_refused(self):
        root = self.sandbox()
        (root / "extra-link").symlink_to(root / "README.md")
        self.assertTrue(checks.validate(root))

    def test_only_invented_fixture_records(self):
        samples = synthetic_samples()
        self.assertEqual(len(samples), 5)
        for sample in samples:
            self.assertTrue(sample.sample_id.startswith("SYNTHETIC_"))
            self.assertTrue(sample.patient_id.startswith("SYNTHETIC_"))
        result = run()
        self.assertEqual(result["results"]["n_patients"], 4)
        self.assertIsNone(result["results"]["p_value"])
        self.assertNotIn("aggregate export", json.dumps(result))

    def test_no_research_tables_or_renderer_entrypoints(self):
        self.assertFalse(any(path.startswith("results/") for path in checks.ALLOWED_FILES))
        self.assertNotIn("scripts/render_report.py", checks.ALLOWED_FILES)
        self.assertNotIn("tests/test_release_contract.py", checks.ALLOWED_FILES)
        self.assertNotIn("tests/test_render_report.py", checks.ALLOWED_FILES)

    def test_standalone_copy_runs_outside_repository(self):
        root = self.sandbox()
        process = subprocess.run(
            [sys.executable, "-I", "-S", "-B", str(root / "scripts/run_synthetic_demo.py")],
            cwd=root.parent, capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout), run())

    def test_code_imports_are_standard_library_or_own_modules(self):
        for rel in checks.ALLOWED_FILES:
            if not rel.endswith(".py"):
                continue
            tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    names = [node.module.split(".")[0]]
                else:
                    continue
                for name in names:
                    self.assertTrue(name in sys.stdlib_module_names or name == "melanoma_portfolio", (rel, name))

    def test_mit_and_explicit_code_scope(self):
        licence = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(licence.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Nike Nicole Costa", licence)
        scope = (ROOT / "LICENSING.md").read_text(encoding="utf-8")
        for name in ("src/melanoma_portfolio/*.py", "scripts/*.py", "tests/*.py", ".github/workflows/synthetic-checks.yml", ".gitignore"):
            self.assertIn(f"`{name}`", scope)
        self.assertIn("figures/", scope)
        self.assertIn("scientific", scope.lower())

    def test_workflow_is_limited_to_synthetic_and_file_checks(self):
        text = (ROOT / ".github/workflows/synthetic-checks.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("scripts/check_release.py", text)
        self.assertNotIn("render_report.py", text)
        self.assertNotIn("upload-artifact", text)
        self.assertNotIn("pip install", text)

    def test_all_four_figures_are_passive_and_accessible(self):
        figures = sorted(path for path in checks.ALLOWED_FILES if path.endswith(".svg"))
        self.assertEqual(len(figures), 4)
        for relative in figures:
            self.assertEqual(checks.validate_svg((ROOT / relative).read_text(encoding="utf-8")), [], relative)

    def test_svg_external_resources_and_scripts_refused(self):
        for content in ("<script>bad</script>", '<image href="https://example.invalid/x"/>', '<rect onclick="bad"/>', '<rect fill="url(https://example.invalid/x)"/>'):
            svg = '<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="t d"><title id="t">Test</title><desc id="d">Test</desc>' + content + '</svg>'
            self.assertTrue(checks.validate_svg(svg))

    def test_svg_broken_accessible_reference_refused(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="missing"><title id="t">Test</title><desc id="d">Test</desc></svg>'
        self.assertTrue(checks.validate_svg(svg))

    def test_fake_identifier_patterns_are_only_heuristics(self):
        self.assertTrue(checks.PATTERNS["patient reference"].search("patient" + "_987654"))
        self.assertFalse(checks.PATTERNS["patient reference"].search("SYNTHETIC_P01"))


if __name__ == "__main__":
    unittest.main()
