"""Source-only regression checks for the DEBO plugin selection governor.

These tests guard policy wiring. They do not prove any plugin or background task runs.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "governance" / "DEBO_TOOL_SELECTION_REGISTER_v1.md"
BOOTSTRAP = ROOT / "governance" / "DEBO_RUNTIME_BOOTSTRAP_v2.md"


class TestDEBOPluginGovernor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = REGISTER.read_text(encoding="utf-8")
        cls.bootstrap = BOOTSTRAP.read_text(encoding="utf-8")

    def test_extend_existing_canonical_register(self):
        self.assertIn("# DEBO Tool Selection & Plugin Discovery Register v1.0", self.register)
        self.assertEqual(self.register.count("## Plugin selection governor v1.1"), 1)

    def test_bootstrap_routes_to_existing_policy(self):
        self.assertIn(
            "DEBO_TOOL_SELECTION_REGISTER_v1.md#plugin-selection-governor",
            self.bootstrap,
        )
        self.assertIn("Choosing, automatically invoking, suggesting, updating", self.bootstrap)

    def test_explicit_tool_lifecycle_and_verification(self):
        for status in ("AVAILABLE", "EXPOSED", "INSTALLED", "CONNECTED",
                       "AUTHENTICATED", "AUTHORIZED", "WORKFLOW-TESTED"):
            with self.subTest(status=status):
                self.assertIn(status, self.register)
        for action in ("USE", "UPDATE", "MERGE", "SUGGEST", "PILOT", "HOLD", "RETIRE"):
            with self.subTest(action=action):
                self.assertIn(action, self.register)

    def test_approval_and_privacy_controls(self):
        for phrase in ("Never silently install", "explicit required approval first",
                       "business-A", "business-B", "seven days",
                       "credential material", "no new app, second master"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.register)

    def test_reuses_existing_automation_and_tools(self):
        for phrase in ("DEBO System Scout", "no second Plugin Scout",
                       "Firecrawl", "TinyFish", "ChatGPT Search",
                       "GitHub", "Notion"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.register)

    def test_does_not_claim_runtime_activation(self):
        self.assertIn("documentation until exercised", self.register)
        self.assertIn("future-chat auto boot unverified", self.register)


if __name__ == "__main__":
    unittest.main()
