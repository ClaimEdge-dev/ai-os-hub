"""R130 evidence state regressions: CI-tested source ≠ live agent runtime."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"governance"/"DEBO_ELITE_EXECUTION_DEFAULT_v1.json"
REPORT=ROOT/"governance"/"dashboard"/"DEBO_R129_GITHUB_EXECUTION_UPGRADE_2026-11-09.md"
PLUGINS=ROOT/"governance"/"dashboard"/"DEBO_R129_PLUGIN_OPTIMIZATION_REGISTER_2026-11-09.md"

class R130EvidenceStateTests(unittest.TestCase):
    def setUp(self):
        self.g=json.loads(GOV.read_text(encoding="utf-8"))

    def test_ci_receipt_updates_stale_label_without_claiming_live(self):
        r=self.g["verified_r129"]
        self.assertEqual(r["external_security_tools"],"EPHEMERAL_CI_TESTED_ONLY")
        self.assertEqual(r["evidence"]["security_regression_tests_passed"],164)
        self.assertEqual(r["evidence"]["promptfoo_synthetic_cases_passed"],8)
        self.assertEqual(r["evidence"]["agents_sdk_scripted_tests_passed"],2)
        self.assertEqual(r["evidence"]["gitleaks_other_secrets_exempted"],0)
        self.assertEqual(r["evidence"]["pilot_ci_status"],"PASS")
        self.assertFalse(r["actual_live_independent_agents"])
        self.assertFalse(r["cross_thread_cold_start_proved"])
        self.assertEqual(r["external_plugin_installations_this_batch"],0)
        self.assertEqual(r["db_task_editor"],"ISOLATED_BACKEND_TESTED_UI_NOT_LIVE")

    def test_router_still_offline_tested_with_no_autoload_claim(self):
        r=self.g["existing_router_candidate"]
        self.assertEqual(r["status"],"SOURCE_INSTALLED_TESTED")
        self.assertEqual(r["execution_scope"],"DETERMINISTIC_OFFLINE_ONLY")
        self.assertFalse(r["new_chat_autoload_verified"])
        self.assertFalse(r["external_agent_runtime_verified"])

    def test_merge_evidence_is_referenced_in_source_report(self):
        r=REPORT.read_text(encoding="utf-8")
        for needle in (
            "6eba4c636bf6ee7457ba7eab166a52db0faf262c",
            "42684260985", "42684260441", "42684584885", "42684584744",
            "164 Python tests", "2/2 scripted", "8/8 offline",
            "0 private keys exempted", "NOT LIVE",
        ):
            self.assertIn(needle,r)

    def test_plugin_report_preserves_posthog_no_data_and_scope(self):
        p=PLUGINS.read_text(encoding="utf-8")
        self.assertIn("no ingested events",p.lower())
        self.assertIn("no evidence that this project belongs to DEBO-05",p)
        self.assertIn("No new ChatGPT plugins were installed",p)
        self.assertIn("No new plugin connection",p) if "No new plugin connection" in p else self.assertIn("No new ChatGPT plugins",p)

    def test_security_scanner_is_still_fail_closed(self):
        workflow=(ROOT/".github"/"workflows"/"debo-r129-security-execution-pilot.yml").read_text(encoding="utf-8")
        classifier=(ROOT/"security"/"r129_gitleaks"/"classify_findings.py").read_text(encoding="utf-8")
        self.assertIn("classify_findings.py",workflow)
        self.assertIn("MAX_FINDS = 2",classifier)
        self.assertIn("PASS_PUBLIC_PUBLISHABLE_KEY_ONLY",classifier)
        self.assertIn("scanner_failed",classifier)
        self.assertNotIn("--exit-code 0",workflow)

if __name__=="__main__":
    unittest.main()
