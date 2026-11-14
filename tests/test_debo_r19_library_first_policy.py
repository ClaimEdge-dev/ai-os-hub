"""Regression checks for DEBO Library-first R19 policy wiring.

These tests validate source contracts only, not live ChatGPT/AI connector behavior.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "DEBO_BOOTSTRAP.md"
STEWARD = ROOT / "skills" / "chatgpt-workspace-steward" / "SKILL.md"
R19 = ROOT / "docs" / "DEBO_R19_CONTINUITY_ADAPTER.md"


class LibraryFirstR19PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.boot = BOOT.read_text(encoding="utf-8")
        cls.steward = STEWARD.read_text(encoding="utf-8")
        cls.r19 = R19.read_text(encoding="utf-8")

    def test_bootstrap_routes_to_existing_components(self):
        self.assertIn("skills/chatgpt-workspace-steward/SKILL.md", self.boot)
        self.assertIn("docs/DEBO_R19_CONTINUITY_ADAPTER.md", self.boot)
        self.assertIn("Library-first cleanup and R19 cross-AI handoff", self.boot)

    def test_cleanup_order_is_explicit(self):
        ordered = ["ChatGPT Library", "ChatGPT export", "Gmail", "Google Drive", "Other connected storage"]
        section = self.steward.split("## Library-first cleanup mission (2026-11-14)", 1)[1]
        positions = [section.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))

    def test_exact_duplicates_require_real_bytes(self):
        self.assertIn("actual bytes/hashes", self.steward)
        self.assertIn("same-name and same-size are candidates", self.r19)

    def test_no_unapproved_destructive_cleanup(self):
        self.assertIn("Default to read-only", self.steward)
        self.assertIn("without its required explicit approval", self.steward)
        self.assertIn("Preserve originals", self.r19)

    def test_no_sensitive_cross_provider_transfer(self):
        self.assertIn("sanitized packets", self.r19)
        self.assertIn("Never transmit private files", self.r19)
        self.assertIn("out of public GitHub", self.steward)

    def test_preserves_legacy_capsule_schema(self):
        self.assertIn("debo.r19.handoff.v1", self.r19)
        self.assertIn("debo.r19.capsule.v1", self.r19)
        self.assertIn("create a second memory or registry", self.r19)

    def test_cannot_claim_live_activation(self):
        self.assertIn("not an external runtime activation", self.r19)
        self.assertIn("not a ChatGPT Library audit", self.boot)
        self.assertIn("no-false-LIVE", self.r19)

    def test_scope_and_evidence_are_required(self):
        for field in ("mission_id", "project_id", "task_id", "provider", "source_scope",
                      "coverage", "sources", "proposed_changes", "tests", "conflicts",
                      "blockers", "next_action"):
            self.assertIn('"' + field + '"', self.r19)
        self.assertIn("VERIFIED_PARTIAL|VERIFIED_COMPLETE|UNKNOWN", self.r19)

    def test_preserve_dashboard_separate_gate(self):
        self.assertIn("DEBO-05", self.boot)
        self.assertIn("DEBO-05", self.steward)


if __name__ == "__main__":
    unittest.main()
