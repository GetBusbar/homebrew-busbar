"""Targeted regression tests for release metadata/formula updates."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(os.environ.get("SET_SHAS_SCRIPT", Path(__file__).resolve().parents[1] / "scripts/ci/set_shas.py"))
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

    def test_malformed_checksums_rejected(self):
        for sha in ["A" * 64, "a" * 63, "a" * 65, "a" * 64 + "\n", "g" * 64]:
            with self.subTest(sha=sha):
                result = self.run_script(sha)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("64 lowercase hexadecimal", result.stderr)
                self.assertEqual(self.formula.read_text(), SOURCE)

    def test_update_keeps_permissions_and_leaves_no_temporary_file(self):
        self.formula.chmod(0o644)
        result = self.run_script("b" * 64, "--version", "1.5.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.formula.stat().st_mode & 0o777, 0o644)
        self.assertEqual([p.name for p in self.formula.parent.iterdir()], ["example.rb"])

    def test_failed_replace_leaves_formula_byte_identical(self):
        # Run update() in-process with os.replace failing: the formula must be untouched and
        # no temporary file may remain (never a truncated, half-written formula).
        import importlib.util
        from unittest import mock
        spec = importlib.util.spec_from_file_location("set_shas", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with mock.patch.object(module.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                module.update(self.formula, ["b" * 64], "1.5.5")
        self.assertEqual(self.formula.read_text(), SOURCE)
        self.assertEqual([p.name for p in self.formula.parent.iterdir()], ["example.rb"])

    def test_options_may_precede_checksums(self):
        result = self.run_script("--version", "1.5.5", "b" * 64)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.formula.read_text(), SOURCE.replace("1.4.1", "1.5.5").replace("a" * 64, "b" * 64))

    def test_trailing_whitespace_and_commented_lines(self):
        source = ('class Example < Formula\n  version "1.4.1"  \n  # sha256 "' + "c" * 64 + '"\n'
                  '  sha256 "' + "a" * 64 + '"\t\nend\n')
        self.formula.write_text(source)
        result = self.run_script("b" * 64, "--version", "1.5.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.formula.read_text(),
                         source.replace("1.4.1", "1.5.5").replace("a" * 64, "b" * 64))

    def test_malformed_formula_version_is_blamed_on_the_formula(self):
        self.formula.write_text(SOURCE.replace("1.4.1", "1.4.1-rc1"))
        result = self.run_script("b" * 64, "--version", "1.5.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("formula version", result.stderr)

    def test_malformed_formula_checksum_line_is_reported(self):
        for bad in ["A" * 64, "a" * 63]:
            with self.subTest(bad=bad):
                self.formula.write_text(SOURCE.replace("a" * 64, bad))
                result = self.run_script("b" * 64, "--version", "1.5.5")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("malformed sha256 line", result.stderr)

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

    def test_check_version_rejects_non_release_versions(self):
        for version in ["1.6.0-rc.1", "1.6", "v1.6.0", ""]:
            with self.subTest(version=version):
                result = self.run_script("--check-version", version)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")

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


NESTED = """class Example < Formula
  version "1.4.1"
  on_macos do
    on_arm do
      sha256 "%s"
    end
    on_intel do
      sha256 "%s"
    end
  end
  on_linux do
    on_intel do
      sha256 "%s"
    end
  end
end
""" % ("a" * 64, "b" * 64, "c" * 64)


class NestedFormulaTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.formula = Path(self.directory.name) / "example.rb"

    def run_script(self, source, *args):
        self.formula.write_text(source)
        return subprocess.run([sys.executable, str(SCRIPT), str(self.formula), *args], capture_output=True, text=True)

    def test_checksums_are_assigned_in_formula_order(self):
        new = ["1" * 64, "2" * 64, "3" * 64]
        result = self.run_script(NESTED, *new, "--version", "1.5.0")
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = NESTED.replace("1.4.1", "1.5.0")
        for old, sha in zip(["a" * 64, "b" * 64, "c" * 64], new):
            expected = expected.replace(old, sha)
        self.assertEqual(self.formula.read_text(), expected)

    def test_duplicate_checksums_rejected(self):
        result = self.run_script(NESTED, "1" * 64, "1" * 64, "3" * 64, "--version", "1.5.0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate", result.stderr)
        self.assertEqual(self.formula.read_text(), NESTED)

    def test_version_bump_with_previous_release_checksums_rejected(self):
        for shas in (["a" * 64, "2" * 64, "3" * 64], ["2" * 64, "3" * 64, "a" * 64]):
            with self.subTest(shas=shas):
                result = self.run_script(NESTED, *shas, "--version", "1.5.0")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("previous release", result.stderr)
                self.assertEqual(self.formula.read_text(), NESTED)

    def test_formula_without_exactly_one_version_is_refused(self):
        for source in [NESTED.replace('  version "1.4.1"\n', ""),
                       NESTED.replace('  version "1.4.1"\n', '  version "1.4.1"\n  version "1.4.2"\n')]:
            with self.subTest(versions=source.count("version")):
                result = self.run_script(source, "1" * 64, "2" * 64, "3" * 64, "--version", "1.5.0")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("exactly one explicit formula version", result.stderr)
                self.assertEqual(self.formula.read_text(), source)

    def test_check_version_never_updates(self):
        for extra in (["1" * 64], ["--version", "1.5.0"]):
            with self.subTest(extra=extra):
                result = self.run_script(NESTED, *extra, "--check-version", "1.5.0")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("--check-version cannot update the formula", result.stderr)
                self.assertEqual(self.formula.read_text(), NESTED)


if __name__ == "__main__":
    unittest.main()
