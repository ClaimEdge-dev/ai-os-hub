"""DEBO v0.3 dashboard source contract: deterministic, no customer data or network."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/debo_dashboard_snapshot_v0_3.schema.json"
SCRIPT = ROOT / "tools/debo_dashboard_snapshot_validate.py"
spec = importlib.util.spec_from_file_location("debo_dashboard_snapshot_validate", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def demo():
    unknown = lambda label: {
        "label": label, "detail": "No authenticated evidence", "truth_state": "UNKNOWN",
        "source_ids": [], "next_action": "Recover an authorized primary source."
    }
    return {
        "schema_version": "0.3", "generated_at": "2026-11-03T09:00:00-06:00",
        "snapshot_kind": "OFFLINE_SNAPSHOT", "mission_id": "DEBO-DASH-005",
        "sources": [{"id": "synthetic-source", "uri": "https://example.org/test",
                     "truth_state": "SOURCE_ONLY", "checked_at": "2026-11-03T09:00:00-06:00"}],
        "cards": {key: unknown(key.upper()) for key in ("now", "money", "blocked", "done")},
        "projects": [{"project_id": "JCT", "label": "Synthetic JCT fixture",
                      "readiness": "SYNTHETIC_TESTED", "source_ids": ["synthetic-source"],
                      "next_action": "Authenticated E2E after owner consent", "owner_gate": "REQUIRED",
                      "owner_approval": "UNVERIFIED", "authenticated_test": "UNVERIFIED"}],
        "capabilities": [{"name": "GitHub", "kind": "PLUGIN", "state": "INSTALLED",
                          "source_ids": ["synthetic-source"]}],
        "automations": [],
        "ideas": [{"idea_id": "demo-01", "project_id": "DEBO", "title": "Demo idea",
                   "disposition": "RESEARCH_LATER", "source_ids": [], "trigger": "On next review"}],
        "thread_index": [{"thread_id": "DEBO-00", "label": "Master command",
                          "purpose": "Priorities and approvals", "status": "ACTIVE"},
                         {"thread_id": "DEBO-05", "label": "Dashboard build",
                          "purpose": "HTML and QA", "status": "BUILD"}]
    }


class DashboardContractTests(unittest.TestCase):
    def test_valid_synthetic_offline_snapshot(self):
        self.assertEqual(module.validate(demo()), [])

    def test_schema_describes_existing_home_cards_and_unknowns(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "0.3")
        self.assertEqual(set(schema["properties"]["cards"]["required"]),
                         {"now", "money", "blocked", "done"})
        self.assertIn("UNKNOWN", schema["$defs"]["truth"]["enum"])
        self.assertIn("LIVE_VERIFIED", schema["$defs"]["project"]["properties"]["readiness"]["enum"])

    def test_cannot_invent_verified_done(self):
        x = demo()
        x["cards"]["done"]["truth_state"] = "VERIFIED"
        self.assertTrue(any("verified source" in e or "proof" in e
                            for e in module.validate(x)))

    def test_money_needs_real_evidence(self):
        x = demo()
        x["cards"]["money"]["truth_state"] = "VERIFIED"
        x["cards"]["money"]["source_ids"] = ["synthetic-source"]
        self.assertTrue(any("money" in e for e in module.validate(x)))

    def test_unsupported_live_jct_cannot_be_promoted(self):
        x = demo()
        x["projects"][0]["readiness"] = "LIVE_VERIFIED"
        errors = module.validate(x)
        self.assertTrue(any("real authenticated test" in e for e in errors))
        self.assertTrue(any("owner approval" in e for e in errors))
        self.assertTrue(any("verified source" in e for e in errors))

    def test_offline_snapshot_cannot_be_mislabeled_verified_refresh(self):
        x = demo()
        x["snapshot_kind"] = "VERIFIED_REFRESH"
        errors = module.validate(x)
        self.assertTrue(any("refresh_receipt" in e for e in errors))
        self.assertTrue(any("verified source" in e for e in errors))

    def test_source_ref_and_idea_dedup(self):
        x = demo()
        x["ideas"][0]["source_ids"] = ["missing-private-record"]
        x["ideas"].append(dict(x["ideas"][0]))
        errors = module.validate(x)
        self.assertTrue(any("dangling source" in e for e in errors))
        self.assertTrue(any("duplicate idea_id" in e for e in errors))

    def test_timezone_and_automation_truth(self):
        x = demo()
        x["generated_at"] = "2026-11-03T09:00:00"
        x["automations"] = [{"title": "Demo task", "enabled": "yes",
                             "truth_state": "VERIFIED", "source_ids": [],
                             "last_run_at": "2026-11-03"}]
        errors = module.validate(x)
        self.assertTrue(any("generated_at" in e for e in errors))
        self.assertTrue(any("true/false" in e for e in errors))
        self.assertTrue(any("last_run_at" in e for e in errors))

    def test_workflow_tested_plugin_needs_evidence(self):
        x = demo()
        x["capabilities"][0]["state"] = "WORKFLOW_TESTED"
        self.assertTrue(any("verified source" in e for e in module.validate(x)))

    def test_verified_source_permits_verified_done(self):
        x = demo()
        x["sources"][0]["truth_state"] = "VERIFIED"
        x["cards"]["done"]["truth_state"] = "VERIFIED"
        x["cards"]["done"]["source_ids"] = ["synthetic-source"]
        self.assertEqual(module.validate(x), [])


if __name__ == "__main__":
    unittest.main()
