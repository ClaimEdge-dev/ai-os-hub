"""Source-only acceptance checks for the existing DEBO skill lifecycle manager.

These do NOT test ChatGPT/Codex runtime activation, MCP auth, or plugin installation.
"""
import unittest
from pathlib import Path

from tools.debo_skill_delta import validate_skill_contract

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "skill-lifecycle-manager" / "SKILL.md"
REFERENCE = ROOT / "skills" / "skill-lifecycle-manager" / "references" / "openai-skill-authoring.md"


class TestOpenAISkillAuthoringSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_valid_portable_frontmatter(self):
        result = validate_skill_contract(self.skill, "skill-lifecycle-manager")
        self.assertEqual(result["status"], "PASS", result)

    def test_existing_factory_extended_not_replaced(self):
        self.assertIn("Lifecycle Manager v2.4", self.skill)
        self.assertIn("REGISTRY CHECK", self.skill)
        self.assertIn("UPDATE existing", self.skill)
        self.assertIn("references/openai-skill-authoring.md", self.skill)
        self.assertIn("not another Skill Factory", self.skill)

    def test_workflow_boundary(self):
        self.assertIn("MCP servers supply live data", self.skill)
        self.assertIn("AGENTS.md", self.skill)
        self.assertIn("Agents API/SDK/Responses", self.skill)
        self.assertIn("agents/openai.yaml", self.reference)
        self.assertIn("verified", self.reference.lower())

    def test_five_activation_and_nonactivation_cases(self):
        for case in ("direct", "indirect", "incomplete", "nonactivation", "edge"):
            with self.subTest(case=case):
                self.assertIn(f"**{case}**", self.reference)
        self.assertIn("target-runtime evaluation", self.reference)

    def test_governance_and_no_fictitious_install(self):
        for term in ("owner approvals", "Notion Skill Registry", "INSTALL", "LIVE"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), (self.skill + self.reference).lower())
        self.assertIn("Do not invent an MCP endpoint", self.skill)
        self.assertIn("no customer/claim", self.reference)


if __name__ == "__main__":
    unittest.main()
