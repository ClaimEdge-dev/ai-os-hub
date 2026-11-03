"""Regression guard: legacy status cleanup must not resurrect retired skills."""
import unittest
from pathlib import Path

from tools.debo_registry_audit import audit
from tools.debo_skill_delta import github_statuses, build_report

ROOT = Path(__file__).resolve().parents[1]
RETIRED = [
  'claimedge-session-memory',
  'claimedge-vault-system',
  'claimedge-skill-forge',
  'claimedge-auto-deploy',
  'claim-command-center',
  'claims-evidence-orchestrator',
  'bobby-ai-command-center',
  'bobby-autopilot-system',
  'bobby-skill-activator',
  'ai-workflow-decoder',
  'session-boot-loader',
  'session-context-preserver',
  'thread-audit-manager',
  'perplexity-connector-advisor',
  'pi-case-analyzer',
  'claimed-master-workflow',
  'credit-repair-orchestrator'
]

CANONICAL = [
    "thread-ops", "skill-lifecycle-manager", "multi-ai-router",
    "robert-master-os", "universal-file-vault", "autonomous-ops-architect",
    "chatgpt-workspace-steward", "proactive-build-ahead",
]

class TestDeboSkillRegistryConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = (ROOT / "SKILL_REGISTRY.md").read_text(encoding="utf-8")

    def test_72_historical_rows_preserved(self):
        result = audit(self.registry)
        self.assertEqual(result["row_count"], 72)
        self.assertEqual(len(result["duplicate_skill_names"]), 0)
        self.assertFalse(result["runtime_installation_verified"])

    def test_17_retired_statuses_are_not_reactivated(self):
        statuses = github_statuses(self.registry)
        self.assertEqual(len(RETIRED), 17)
        for name in RETIRED:
            with self.subTest(name=name):
                self.assertEqual(statuses.get(name), "DEPRECATED")

    def test_canonical_source_files_exist_without_install_claim(self):
        for name in CANONICAL:
            with self.subTest(name=name):
                self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())
        report = build_report(self.registry, [{"Name": name, "Status": "DEPRECATED"} for name in RETIRED])
        self.assertEqual(report["summary"]["catalog_conflicts"], 0)
        self.assertTrue(all(row["runtime_installed"] == "UNVERIFIED" for row in report["skills"]))

if __name__ == "__main__":
    unittest.main()
