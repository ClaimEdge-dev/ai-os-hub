"""Static acceptance tests for DEBO reference-intelligence prompt source only.

These tests do not prove account-wide activation, external runtime tools, or money earned.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "prompts" / "DEBO_ELITE_EXECUTION_PROMPT_v2.md"
RUBRIC = ROOT / "prompts" / "DEBO_REFERENCE_INTELLIGENCE_SCORECARD_v1.md"


class TestReferenceIntelligencePrompt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompt = RUBRIC.read_text(encoding="utf-8")
        cls.master = MASTER.read_text(encoding="utf-8")

    def test_extends_one_existing_master(self):
        self.assertIn("DEBO_REFERENCE_INTELLIGENCE_SCORECARD_v1.md", self.master)
        self.assertIn("not another agent", self.prompt)
        self.assertIn("existing DEBO", self.prompt)

    def test_weights_total_100(self):
        section = self.prompt.split("## Value rubric", 1)[1].split("## Default", 1)[0]
        points = [int(n) for n in re.findall(r"^\\| [^\\n]+ \\| (\\d+) \\|", section, re.M)]
        self.assertEqual(points, [25, 20, 15, 15, 10, 10, 5])
        self.assertEqual(sum(points), 100)

    def test_activation_and_nonactivation(self):
        for token in ("**Direct:**", "**Indirect:**", "**Incomplete:**",
                      "**Nonactivation:**", "**Unsafe edge:**", "**Source attack:**"):
            with self.subTest(token=token):
                self.assertIn(token, self.prompt)

    def test_evidence_and_runtime_truth(self):
        for token in ("OFFICIAL-CONFIRMED", "RUNTIME-VERIFIED", "UNKNOWN",
                      "SOURCE_BUILT", "CI_TESTED", "INSTALLED", "LIVE", "UNSAVED"):
            with self.subTest(token=token):
                self.assertIn(token, self.prompt)

    def test_privacy_copyright_and_no_paid_execution(self):
        for token in ("private-data exports", "youth", "copyrighted",
                      "source links", "purchases", "external data transfer"):
            with self.subTest(token=token):
                self.assertIn(token.lower(), self.prompt.lower())


if __name__ == "__main__":
    unittest.main()
