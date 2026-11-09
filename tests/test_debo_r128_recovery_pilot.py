"""R128 source-only recovery pilot; no external agents or network are used."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from debo_r31_decision_router import Task, decide, batch
from debo_r128_recovery_pilot import (
    validate, plan, mack_forge_proof_pilot, classify_failure
)

FIXTURE = ROOT / "tests" / "fixtures" / "debo_r128_recovery_synthetic.json"

class RecoveryPilotTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_synthetic_fixture_routes_with_no_side_effects(self):
        p = plan(self.data)
        self.assertEqual(p["mode"], "DRY_RUN_NO_EXTERNAL_EFFECT")
        self.assertEqual(p["skipped_verified"], ["DEBO-R128-AUTH", "DEBO-R128-SOURCE"])
        self.assertEqual(p["ignored_approval_receipts"], ["DEBO-R128-OWNER"])
        self.assertEqual(p["stale_receipts_need_reverification"], ["DEBO-R128-STALE"])
        self.assertEqual(p["metrics_fixture"]["candidate_steps"], 7)
        self.assertEqual(p["metrics_fixture"]["already_verified_steps"], 2)
        self.assertEqual(p["metrics_fixture"]["routed_auto_steps"], 2)
        self.assertEqual(p["metrics_fixture"]["owner_approval_steps"], 1)
        self.assertEqual(p["metrics_fixture"]["blocked_steps"], 2)
        self.assertEqual(p["metrics_fixture"]["actual_external_tool_calls"], 0)

    def test_approval_receipt_cannot_bypass_owner_gate(self):
        p = plan(self.data)
        self.assertEqual(p["route"]["approval"][0]["action"], "approve_mapping")
        self.assertIn("DEBO-R128-OWNER",p["ignored_approval_receipts"])

    def test_completed_owner_approval_not_silently_skipped_by_r31(self):
        r = batch([Task("DEBO-R128-OWNER","approve_mapping")],
                  {"DEBO-R128-OWNER"},set())
        self.assertEqual(len(r["approval"]),1)

    def test_bad_evidence_type_does_not_mark_tests_complete(self):
        self.data["receipts"].append({
            "task_id":"DEBO-R128-NEXT", "project_id":"DEBO",
            "state":"PASS", "evidence_type":"source_readback",
            "evidence_ref":"fixture:not-a-test",
            "source_revision":"synthetic-rev-1"})
        p = plan(self.data)
        self.assertIn("DEBO-R128-NEXT",p["ignored_mismatched_proof_receipts"])
        self.assertTrue(any(x["task_id"]=="DEBO-R128-NEXT" for x in p["route"]["auto"]))

    def test_actual_test_receipt_skips_exact_version_step(self):
        self.data["receipts"].append({
            "task_id":"DEBO-R128-NEXT", "project_id":"DEBO",
            "state":"PASS", "evidence_type":"test_receipt",
            "evidence_ref":"fixture:test-pass",
            "source_revision":"synthetic-rev-1"})
        p=plan(self.data)
        self.assertIn("DEBO-R128-NEXT",p["skipped_verified"])
        self.assertEqual(p["metrics_fixture"]["already_verified_steps"],3)

    def test_stale_receipt_must_be_reverified(self):
        p=plan(self.data)
        self.assertTrue(any(x["task_id"]=="DEBO-R128-STALE" for x in p["route"]["auto"]))

    def test_failed_task_cannot_be_retried_blindly(self):
        p=plan(self.data)
        self.assertTrue(any(x["task_id"]=="DEBO-R128-FAILED" for x in p["route"]["blocked"]))

    def test_deterministic_repeated_plan(self):
        self.assertEqual(plan(self.data),plan(deepcopy(self.data)))

    def test_duplicate_task_ids_are_rejected(self):
        self.data["tasks"].append(deepcopy(self.data["tasks"][0]))
        with self.assertRaises(ValueError): validate(self.data)

    def test_duplicate_receipts_are_rejected(self):
        self.data["receipts"].append(deepcopy(self.data["receipts"][0]))
        with self.assertRaises(ValueError): validate(self.data)

    def test_cross_project_task_is_rejected(self):
        self.data["tasks"][0]["project_id"]="JCT"
        with self.assertRaises(ValueError): validate(self.data)

    def test_cross_project_receipt_is_rejected(self):
        self.data["receipts"][0]["project_id"]="JCT"
        with self.assertRaises(ValueError): validate(self.data)

    def test_foreign_dependency_is_rejected(self):
        self.data["tasks"][0]["depends_on"]=["WORK-JCT-001"]
        with self.assertRaises(ValueError): validate(self.data)

    def test_self_dependency_is_rejected(self):
        self.data["tasks"][0]["depends_on"]=["DEBO-R128-SOURCE"]
        with self.assertRaises(ValueError): validate(self.data)

    def test_unrecognized_action_is_fail_closed(self):
        self.data["tasks"].append({
            "id":"DEBO-R128-UNKNOWN","project_id":"DEBO",
            "action":"export_customer_data","depends_on":[]})
        p=plan(self.data)
        self.assertTrue(any(x["task_id"]=="DEBO-R128-UNKNOWN" for x in p["route"]["blocked"]))

    def test_r31_safe_action_auto(self):
        self.assertEqual(decide(Task("DEBO-R128-T","run_local_tests"),set(),set())[0],"AUTO")

    def test_r31_production_write_needs_approval(self):
        self.assertEqual(decide(Task("DEBO-R128-T","production_write"),set(),set())[0],"APPROVAL")

    def test_r31_duplicate_batch_raises(self):
        with self.assertRaises(ValueError):
            batch([Task("DEBO-R128-T","read_source"),Task("DEBO-R128-T","read_source")],set(),set())

    def test_mack_forge_proof_is_mock_only(self):
        r=mack_forge_proof_pilot([2,3,5])
        self.assertEqual(r["status"],"TESTED")
        self.assertEqual([t["role"] for t in r["trace"]],["Mack","Forge","Proof"])
        self.assertEqual(r["trace"][1]["output"],10)
        self.assertFalse(r["independent_agents_running"])

    def test_mock_handoff_rejects_invalid_input(self):
        self.assertEqual(mack_forge_proof_pilot([True,2])["status"],"BLOCKED")

    def test_auth_error_has_no_automatic_retries(self):
        self.assertEqual(classify_failure("AUTH_403")["max_automatic_retries"],0)
        self.assertEqual(classify_failure("AUTH_403")["route"],"OWNER_APPROVAL")

    def test_timeout_max_one_safe_retry(self):
        self.assertEqual(classify_failure("NETWORK_TIMEOUT")["max_automatic_retries"],1)

    def test_duplicate_request_is_skipped(self):
        self.assertEqual(classify_failure("DUPLICATE_REQUEST")["route"],"SKIP_DUPLICATE")

    def test_unknown_failure_is_blocked(self):
        self.assertEqual(classify_failure("COMPLETELY_UNKNOWN")["route"],"BLOCKED")


class AliasAndSkillInventoryTests(unittest.TestCase):
    def test_morgans_legacy_id_maps_to_one_core_route(self):
        source=(ROOT/"projects/morgans/AGENT_SYSTEM.md").read_text(encoding="utf-8")
        self.assertIn("Project ID: MOL (legacy local alias)",source)
        self.assertIn("Canonical DEBO routing ID: MOR",source)
        derived=(ROOT/"governance/runtime-briefs/MOR.md").read_text(encoding="utf-8")
        self.assertIn("## Selected project: MOR",derived)

    def test_credit_legacy_id_preserves_restricted_route(self):
        source=(ROOT/"projects/credit-repair/AGENT_SYSTEM.md").read_text(encoding="utf-8")
        self.assertIn("Project ID: CR (legacy local alias)",source)
        self.assertIn("Canonical DEBO routing ID: CREDIT",source)
        self.assertIn("Sensitivity: RESTRICTED",source)
        derived=(ROOT/"governance/runtime-briefs/CREDIT.md").read_text(encoding="utf-8")
        self.assertIn("## Selected project: CREDIT",derived)

    def test_source_skill_files_are_not_installations(self):
        actual=[]
        for root in ("skills","projects","plugins"):
            actual.extend((ROOT/root).rglob("SKILL.md"))
        self.assertGreaterEqual(len(actual),84)
        self.assertEqual(len(actual),len(set(actual)))
        from tools.debo_registry_audit import audit
        registry=audit((ROOT/"SKILL_REGISTRY.md").read_text(encoding="utf-8"))
        self.assertEqual(registry["row_count"],72)
        self.assertEqual(registry["source_status_counts"]["ACTIVE"],55)
        self.assertEqual(registry["source_status_counts"]["DEPRECATED"],17)
        self.assertFalse(registry["runtime_installation_verified"])

if __name__=="__main__":
    unittest.main()
