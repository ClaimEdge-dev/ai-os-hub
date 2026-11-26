"""Source-only safety regression for public Track data and iPhone Prompt Upgrade."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class PublicSourceAndPromptBridgeTests(unittest.TestCase):
    def test_existing_extraction_skill_extended_not_replaced(self):
        path=ROOT/"skills/wrestling-extraction-suite/SKILL.md"
        s=path.read_text(encoding="utf-8")
        self.assertIn("One skill, two modes",s)
        self.assertIn("references/public-track-evidence-v1.md",s)
    def test_provider_and_privacy_review(self):
        a=(ROOT/"skills/wrestling-extraction-suite/references/public-track-evidence-v1.md").read_text(encoding="utf-8").lower()
        for required in ("robots","paywall","source","duplicate","bye","permission","no"):
            self.assertIn(required,a)
        self.assertNotIn("twSessionId=secret",a)
    def test_mobile_is_user_initiated_no_global_keyboard_capturing(self):
        b=(ROOT/"skills/skill-lifecycle-manager/references/iphone-prompt-upgrade-2026-11-22.md").read_text(encoding="utf-8").lower()
        for required in ("share sheet","use model","writing tools","no keylogging","copy to clipboard","not installed"):
            self.assertIn(required,b)
    def test_existing_work_launcher_mentions_existing_skill_paths(self):
        c=(ROOT/"prompts/DEBO_WRESTLING_AI_RESEARCH_WORK_LAUNCH_20261121.md").read_text(encoding="utf-8")
        self.assertIn("2026-11-22 Public Results + iPhone Prompt Upgrade",c)
        self.assertIn("skills/wrestling-extraction-suite/SKILL.md",c)

if __name__=="__main__":unittest.main()
