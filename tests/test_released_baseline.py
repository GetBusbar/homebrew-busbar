"""Keep development formula selections at or above the published tap baseline."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
# Published tap commit 6c97aa59c6c845ffb682e004c6b9d16cbac63006.
RELEASED = {"busbar": (1, 5, 5), "busbar-admin": (0, 2, 3)}


class ReleasedBaselineTests(unittest.TestCase):
    def test_formula_versions_do_not_regress_below_published_baseline(self):
        for name, baseline in RELEASED.items():
            with self.subTest(formula=name):
                source = (ROOT / "Formula" / f"{name}.rb").read_text()
                versions = re.findall(r'^  version "([0-9]+\.[0-9]+\.[0-9]+)"$', source, re.MULTILINE)
                self.assertEqual(len(versions), 1)
                self.assertGreaterEqual(tuple(map(int, versions[0].split("."))), baseline)


if __name__ == "__main__":
    unittest.main()
