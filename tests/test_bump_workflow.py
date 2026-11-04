"""Run only the two formula bump shell steps against a fake release service."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(os.environ.get("BUMP_ROOT", Path(__file__).resolve().parents[1]))


class BumpWorkflowTests(unittest.TestCase):
    def run_bump(self, index, tag, fail=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "Formula", root / "Formula")
            shutil.copytree(ROOT / ".github/scripts", root / ".github/scripts")
            before = {path.name: path.read_bytes() for path in (root / "Formula").glob("*.rb")}
            mock = root / "mock"
            mock.mkdir()
            gh = mock / "gh"
            gh.write_text('#!/bin/bash\nif [ "$2" = view ]; then\n  [ "$FAIL_VIEW" = 0 ] || exit 42\n  printf "%s\\n" "$RELEASE_TAG"\nelse\n  echo unexpected-download >&2\n  exit 43\nfi\n')
            gh.chmod(0o755)
            blocks = re.findall(r'        run: \|\n((?:          .*\n|\n)+)', (ROOT / ".github/workflows/bump.yml").read_text())
            script = "\n".join(line[10:] for line in blocks[index].splitlines())
            env = dict(os.environ, PATH=f"{mock}:{os.environ['PATH']}", RELEASE_TAG=tag, FAIL_VIEW="1" if fail else "0")
            result = subprocess.run(["bash", "-c", script], cwd=root, env=env, text=True, capture_output=True)
            self.assertEqual(before, {path.name: path.read_bytes() for path in (root / "Formula").glob("*.rb")})
            return result

    def test_older_release_is_noop_without_download(self):
        result = self.run_bump(0, "v1.3.9")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("unexpected-download", result.stderr)

    def test_invalid_release_fails_before_download(self):
        result = self.run_bump(0, 'v1.5.5";raise')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("unexpected-download", result.stderr)

    def test_unprefixed_tag_rejected_before_download(self):
        result = self.run_bump(0, "1.5.5")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("unexpected-download", result.stderr)

    def test_admin_api_failure_is_not_success(self):
        result = self.run_bump(1, "v0.1.0", fail=True)
        self.assertNotEqual(result.returncode, 0)

    def test_current_admin_release_is_noop(self):
        result = self.run_bump(1, "v0.1.0")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
