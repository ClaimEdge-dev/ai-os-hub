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

    def test_empty_registry(self):
        self.assertEqual(audit("")["row_count"], 0)

if __name__ == "__main__":
    unittest.main()
