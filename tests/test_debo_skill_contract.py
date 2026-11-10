"""R149-002 synthetic Agent Skills contract tests (no external I/O)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tools.debo_skill_delta import validate_skill_contract

def mk(name="sample-skill", desc="Use when processing sample source."):
    return "---\nname: " + name + "\ndescription: " + desc + "\n---\n\n# Instructions\nDo work.\n"

class SkillContractTests(unittest.TestCase):
    def test_valid_frontmatter(self):
        self.assertEqual(validate_skill_contract(mk(), "sample-skill")["status"], "PASS")

    def test_optional_license(self):
        self.assertNotIn("LICENSE", validate_skill_contract(mk(), "sample-skill")["issues"])

    def test_folded_description(self):
        content = "---\nname: sample-skill\ndescription: >\n  Work with source files.\n  Use during review.\n---\n# Work\n"
        self.assertEqual(validate_skill_contract(content, "sample-skill")["status"], "PASS")

    def test_missing_frontmatter(self):
        self.assertIn("FRONTMATTER_MISSING", validate_skill_contract("no header", "sample-skill")["issues"])

    def test_unclosed_frontmatter(self):
        self.assertIn("FRONTMATTER_UNCLOSED", validate_skill_contract("---\nname: sample-skill", "sample-skill")["issues"])

    def test_bad_uppercase_name(self):
        self.assertIn("NAME_INVALID", validate_skill_contract(mk("Sample"), "Sample")["issues"])

    def test_double_hyphen(self):
        self.assertIn("NAME_INVALID", validate_skill_contract(mk("two--words"), "two--words")["issues"])

    def test_wrong_folder(self):
        self.assertIn("NAME_DIRECTORY_MISMATCH", validate_skill_contract(mk(), "another")["issues"])

    def test_blank_description(self):
        self.assertIn("DESCRIPTION_LENGTH_INVALID", validate_skill_contract(mk(desc=""), "sample-skill")["issues"])

    def test_description_over_limit(self):
        self.assertIn("DESCRIPTION_LENGTH_INVALID", validate_skill_contract(mk(desc="x" * 1025), "sample-skill")["issues"])

    def test_compatibility_over_limit(self):
        content = mk().replace("---\n\n# Instructions", "compatibility: " + ("x" * 501) + "\n---\n\n# Instructions")
        self.assertIn("COMPATIBILITY_LENGTH_INVALID", validate_skill_contract(content, "sample-skill")["issues"])

    def test_missing_body(self):
        self.assertIn("SKILL_BODY_MISSING", validate_skill_contract("---\nname: sample-skill\ndescription: Small.\n---", "sample-skill")["issues"])

    def test_nested_yaml_needs_reference_validator(self):
        content = "---\nname: sample-skill\ndescription: Use for sample work.\nmetadata:\n  author: sample\n---\n# Body"
        self.assertIn("COMPLEX_YAML_REQUIRES_REFERENCE_VALIDATOR", validate_skill_contract(content, "sample-skill")["issues"])

    def test_cli_is_opt_in_and_default_summary_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "SKILL_REGISTRY.md").write_text("| 1 | sample-skill | x | x | ACTIVE |\n")
            folder = root / "skills" / "sample-skill"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(mk())
            script = Path(__file__).resolve().parents[1] / "tools" / "debo_skill_delta.py"
            before = json.loads(subprocess.check_output([sys.executable, str(script), "--repo", str(root)]))
            after = json.loads(subprocess.check_output([sys.executable, str(script), "--repo", str(root), "--validate-contracts"]))
            self.assertNotIn("contract_audit", before)
            self.assertEqual(after["contract_audit"]["checked"], 1)
            self.assertEqual(after["contract_audit"]["pass"], 1)
            self.assertEqual(after["summary"], before["summary"])

if __name__ == "__main__":
    unittest.main()
