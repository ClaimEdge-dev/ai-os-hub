"""DEBO plugin routing source controls, not app connection/runtime tests."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "governance/DEBO_PLUGIN_SELECTION_AND_LIFECYCLE_RULES_v1.md"
BOOT = ROOT / "governance/DEBO_RUNTIME_BOOTSTRAP_v2.md"
class PluginRoutingPolicyTests(unittest.TestCase):
    def test_bootstrap_links_policy(self):
        self.assertTrue(POLICY.is_file())
        self.assertIn(POLICY.name, BOOT.read_text(encoding="utf-8"))
    def test_required_sections(self):
        text = POLICY.read_text(encoding="utf-8")
        for label in ("Automatically choose", "Suggest a missing plugin", "Update, reuse, merge", "DEBO System Scout", "Practical route map", "Tool decision receipt"):
            with self.subTest(label=label): self.assertIn(label, text)
    def test_no_silent_install_or_unverified_live_claim(self):
        text = POLICY.read_text(encoding="utf-8")
        for rule in ("explicit action", "No new permissions", "INSTALLED, CONNECTED, AUTHORIZED, CALLABLE, TESTED, LIVE", "seven days"):
            with self.subTest(rule=rule): self.assertIn(rule, text)
if __name__ == "__main__":
    unittest.main()
