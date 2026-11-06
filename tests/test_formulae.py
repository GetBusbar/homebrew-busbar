"""Static checks on the formulae and README that Homebrew users depend on."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


FORMULAE = ["Formula/busbar.rb", "Formula/busbar-admin.rb"]


class FormulaTests(unittest.TestCase):
    def test_formulae_keep_the_shape_set_shas_relies_on(self):
        for name in FORMULAE:
            with self.subTest(formula=name):
                source = (ROOT / name).read_text()
                self.assertEqual(len(re.findall(r'^  version "\d+\.\d+\.\d+"$', source, re.MULTILINE)), 1)
                # every url is followed by its own sha256, a distinct lowercase digest
                pairs = re.findall(r'^(\s*)url "([^"]+)"\n\1sha256 "([^"]*)"$', source, re.MULTILINE)
                self.assertEqual(len(pairs), len(re.findall(r"^\s*url ", source, re.MULTILINE)))
                self.assertEqual(len(pairs), len(re.findall(r"^\s*sha256 ", source, re.MULTILINE)))
                shas = [sha for _, _, sha in pairs]
                for sha in shas:
                    self.assertRegex(sha, r"^[0-9a-f]{64}$")
                self.assertEqual(len(set(shas)), len(shas))

    def test_urls_follow_the_version_line(self):
        # set_shas.py only rewrites the version and sha256 lines, so every url must take its
        # release from #{version} (directly or via BASE); a hard-coded release survives a bump.
        for name in FORMULAE:
            with self.subTest(formula=name):
                code = [l for l in (ROOT / name).read_text().splitlines() if not l.lstrip().startswith("#")]
                base = [l for l in code if re.match(r"\s*BASE\s*=", l)]
                self.assertEqual(len(base), 1)
                self.assertIn('/download/v#{version}"', base[0])
                urls = [l for l in code if re.match(r'\s*url "', l)]
                self.assertTrue(urls)
                for line in urls:
                    self.assertRegex(line, r'url "#\{BASE\}/')
                    self.assertNotRegex(line, r"\d+\.\d+\.\d+")

    def test_formula_comments_do_not_promise_a_bump_workflow(self):
        for name in FORMULAE:
            with self.subTest(formula=name):
                self.assertNotIn("bump.yml", (ROOT / name).read_text())

    def test_core_submission_test_block_accepts_head_builds(self):
        source = (ROOT / "core-submission/busbar.rb").read_text()
        block = re.search(r"^  test do\n((?:    .*\n|\n)*)  end$", source, re.MULTILINE)
        self.assertIsNotNone(block)
        code = "\n".join(l for l in block.group(1).splitlines() if not l.lstrip().startswith("#"))
        self.assertIn("version.head?", code)
        self.assertRegex(code, r"assert_match expected,")

    def test_readme_upgrade_commands_name_one_formula_each(self):
        lines = re.findall(r"brew upgrade[^\n]*", (ROOT / "README.md").read_text())
        self.assertTrue(lines)
        for line in lines:
            self.assertEqual(len(line.split("brew upgrade", 1)[1].split("#", 1)[0].split()), 1, line)

    def test_admin_refuses_linux_arm_cleanly(self):
        source = (ROOT / "Formula/busbar-admin.rb").read_text()
        linux = re.search(r"^  on_linux do\n((?:    .*\n|\n)*?)  end$", source, re.MULTILINE)
        self.assertIsNotNone(linux)
        # The url must sit directly under on_linux (not inside on_intel): a stable spec with no
        # url on Linux arm64 fails to load, before any `depends_on arch:` is evaluated.
        self.assertIn("depends_on arch: :x86_64", linux.group(1))
        self.assertNotRegex(linux.group(1), r"on_(?:intel|arm)\b")
        self.assertRegex(linux.group(1), r'(?m)^    url "')



if __name__ == "__main__":
    unittest.main()
