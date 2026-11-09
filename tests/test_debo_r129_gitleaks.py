"""R129 Gitleaks scoped publishable-key triage, no real keys or networks."""
import importlib.util
import tempfile
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "r129_gitleaks", ROOT/"security"/"r129_gitleaks"/"classify_findings.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GitleaksTriageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.one = "projects/jcs-towing/website-v2-preview/app.js"
        self.two = "projects/jcs-towing/website-v2-preview/preview-standalone.html"
        self.key = "sb_" + "publishable_" + ("A" * 32)
        for p in (self.one, self.two):
            file = self.root / p
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text("const DATA_URL='https://example.invalid';\n"
                            + "const KEY='" + self.key + "';\n")
        self.findings = [
            {"File": "/source/" + self.one, "StartLine": 2, "RuleID": "generic-api-key"},
            {"File": "/source/" + self.two, "StartLine": 2, "RuleID": "generic-api-key"},
        ]

    def check(self, report=None, code=1):
        return MODULE.classify(self.findings if report is None else report, self.root, code)

    def test_two_scoped_public_keys_pass(self):
        self.assertEqual(self.check()["status"], "PASS_PUBLIC_PUBLISHABLE_KEY_ONLY")

    def test_empty_clean_scan_passes(self):
        self.assertEqual(self.check([], 0)["status"], "PASS_NO_FINDINGS")

    def test_unknown_path_blocks(self):
        self.findings[0]["File"] = "/source/other/app.js"
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_secret_key_prefix_blocks(self):
        (self.root/self.one).write_text("const KEY='sb_secret_" + "B"*32 + "';\n")
        self.findings[0]["StartLine"] = 1
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_other_rule_blocks(self):
        self.findings[0]["RuleID"] = "github-pat"
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_more_than_two_findings_blocks(self):
        self.findings.append(dict(self.findings[0]))
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_duplicate_finding_location_blocks(self):
        self.findings[1] = dict(self.findings[0])
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_mismatched_public_keys_blocks(self):
        (self.root/self.two).write_text("const DATA_URL='https://example.invalid';\n"
                                       + "const KEY='sb_publishable_" + "C"*32 + "';\n")
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_invalid_line_blocks(self):
        self.findings[0]["StartLine"] = 100
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_scanner_unexpected_error_blocks(self):
        self.assertEqual(self.check(code=2)["status"], "BLOCKED")

    def test_report_and_exit_inconsistent_blocks(self):
        self.assertEqual(self.check(code=0)["status"], "BLOCKED")
        self.assertEqual(self.check(report=[],code=1)["status"], "BLOCKED")

    def test_missing_source_blocks(self):
        (self.root/self.one).unlink()
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_not_full_key_assignment_blocks(self):
        (self.root/self.one).write_text("const KEY='sb_publishable_"+"D"*32+"'; doBadThing();\n")
        self.findings[0]["StartLine"] = 1
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_does_not_echo_token_value(self):
        self.assertNotIn(self.key, repr(self.check()))


if __name__ == "__main__":
    unittest.main()
