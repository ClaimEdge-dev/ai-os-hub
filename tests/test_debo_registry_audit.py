import unittest
from pathlib import Path
from tools.debo_registry_audit import audit

class RegistryAuditTests(unittest.TestCase):
    def test_duplicates_and_missing_numbers(self):
        report = audit("## Domain 1: Test\n| 1 | `alpha` | x |\n| 3 | `beta` | x |\n| 3 | `gamma` | x |")
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["duplicate_numbers"], [3])
        self.assertEqual(report["missing_numbers"], [2])
        self.assertFalse(report["runtime_installation_verified"])

    def test_canonical_registry_integrity(self):
        report = audit((Path(__file__).resolve().parents[1] / "SKILL_REGISTRY.md").read_text())
        self.assertGreater(report["row_count"], 0)
        for field in ("duplicate_numbers", "missing_numbers", "duplicate_skill_names"):
            self.assertEqual(report[field], [], field)

    def test_historical_statuses_are_accurate(self):
        report = audit((Path(__file__).resolve().parents[1] / "SKILL_REGISTRY.md").read_text())
        self.assertEqual(report["row_count"], 72)
        self.assertEqual(report["source_status_counts"]["ACTIVE"], 55)
        self.assertEqual(report["source_status_counts"]["DEPRECATED"], 17)
        self.assertEqual(report["stats_conflicts"], {})
        self.assertTrue(report["stats_match"])
        self.assertFalse(report["runtime_installation_verified"])

    def test_stale_summary_is_detected_without_modifying_sources(self):
        text = ("## Domain 1: Test\n"
                "| 1 | `active-skill` | x | y | ACTIVE |\n"
                "| 2 | `old-skill` | x | y | DEPRECATED |\n"
                "## Stats\n"
                "| Total Skills | 2 |\n"
                "| Source-labelled Active | 2 |\n"
                "| Deprecated | 0 |\n")
        report = audit(text)
        self.assertFalse(report["stats_match"])
        self.assertEqual(report["stats_conflicts"]["Source-labelled Active"],
                         {"declared": 2, "actual": 1})
        self.assertEqual(report["stats_conflicts"]["Deprecated"],
                         {"declared": 0, "actual": 1})

    def test_empty_registry(self):
        self.assertEqual(audit("")["row_count"], 0)

if __name__ == "__main__":
    unittest.main()
