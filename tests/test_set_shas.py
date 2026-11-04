"""Targeted regression tests for release metadata/formula updates."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(os.environ.get("SET_SHAS_SCRIPT", Path(__file__).resolve().parents[1] / ".github/scripts/set_shas.py"))
SOURCE = 'class Example < Formula\n  version "1.4.1"\n  sha256 "' + "a" * 64 + '"\nend\n'


class FormulaUpdateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.formula = Path(self.directory.name) / "example.rb"
        self.formula.write_text(SOURCE)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.formula), *args], capture_output=True, text=True)

    def test_invalid_checksum_leaves_formula_intact(self):
        result = self.run_script('"; system("unexpected"); #')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.formula.read_text(), SOURCE)

    def test_count_mismatch_leaves_formula_intact(self):
        result = self.run_script("b" * 64, "c" * 64)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.formula.read_text(), SOURCE)

    def test_checksums_and_version_update_together(self):
        result = self.run_script("b" * 64, "--version", "1.5.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.formula.read_text(), SOURCE.replace("1.4.1", "1.5.5").replace("a" * 64, "b" * 64))

    def test_invalid_version_does_not_modify_formula(self):
        for version in ['1.5.5"; system("unexpected")', "1.5.5-rc.1", "01.5.5", "1.5", "1.5.5\n"]:
            with self.subTest(version=version):
                result = self.run_script("b" * 64, "--version", version)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.formula.read_text(), SOURCE)

    def test_version_check_uses_numeric_order_and_never_downgrades(self):
        for version, expected in [("1.4.1", "current"), ("1.3.9", "current"), ("1.10.0", "newer"), ("2.0.0", "newer")]:
            with self.subTest(version=version):
                result = self.run_script("--check-version", version)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), expected)
                self.assertEqual(self.formula.read_text(), SOURCE)

    def test_downgrade_update_rejected(self):
        result = self.run_script("b" * 64, "--version", "1.3.0")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.formula.read_text(), SOURCE)

    def test_bad_checksum_count_does_not_partially_bump_version(self):
        result = self.run_script("b" * 64, "c" * 64, "--version", "1.5.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.formula.read_text(), SOURCE)

    def test_checksum_only_compatibility(self):
        result = self.run_script("b" * 64)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.formula.read_text(), SOURCE.replace("a" * 64, "b" * 64))


if __name__ == "__main__":
    unittest.main()
