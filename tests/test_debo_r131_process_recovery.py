"""R131 offline process restart acceptance for the already-merged R19 adapter.

Real separate Python processes + optional Node planning, public synthetic fixture only.
Never claims a fresh ChatGPT thread loaded sources, a Notion/Neon write,
a real owner approval, authenticated evidence, or an automatic scheduler.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"debo_r19_continuity.py"
SYNC=ROOT/"tools"/"debo_r19_sync.mjs"
GOV=ROOT/"governance"/"DEBO_R19_CONTINUITY_ADAPTER_v1.json"

def python_tool(*args,expected=0):
    r=subprocess.run([sys.executable,str(TOOL),*map(str,args)],capture_output=True,text=True,check=False,timeout=12)
    if expected == 0 and r.returncode:
        raise AssertionError(f"R19 CLI exit {r.returncode}: {r.stderr[:200]}")
    return r

class R131FreshProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.capsule=self.root/"synthetic-input.json"
        self.saved=self.root/"checkpoint-v1.json"
        self.event=self.root/"event.json"
        self.seen=self.root/"seen.json"
        self.source_ref="fixture:r131-offline-test"
        self.data={
            "schema":"debo.r19.capsule.v1",
            "project_id":"DEBO",
            "mission_id":"DEBO-MASTER-043",
            "objective":"R131 isolated continuity test only",
            "checkpoint":"R131-SYNTHETIC",
            "next_action":"Run verified read-only event planner",
            "status":"TESTED",
            "scope":"private",
            "evidence":[{"type":"test_receipt","ref":self.source_ref}],
        }
        # Generate a real R19 source-scoped fingerprint in a separate process.
        self.data["task_id"]=python_tool(
            "fingerprint","DEBO",self.data["objective"],"--source-key","r131-synthetic-001"
        ).stdout.strip()
        self.capsule.write_text(json.dumps(self.data),encoding="utf-8")

    def test_process_restarts_with_byte_identical_receipt(self):
        created=json.loads(python_tool("checkpoint","--input",self.capsule,"--output",self.saved).stdout)
        self.assertEqual(created["readback"],"PASS")
        self.assertTrue(self.saved.exists())
        checked=python_tool("validate","--input",self.saved)
        self.assertIn("PASS",checked.stdout)
        repeated=json.loads(python_tool("checkpoint","--input",self.capsule,"--output",self.saved).stdout)
        self.assertEqual(repeated["sha256"],created["sha256"])
        self.assertTrue(repeated["unchanged"])
        self.assertEqual(json.loads(self.saved.read_text()),self.data)

    def test_private_event_survives_new_process_and_is_deterministic(self):
        python_tool("checkpoint","--input",self.capsule,"--output",self.saved)
        a=json.loads(python_tool("event","--input",self.saved,"--type","TASK_VERIFIED","--revision","synthetic-source-v1").stdout)
        b=json.loads(python_tool("event","--input",self.saved,"--type","TASK_VERIFIED","--revision","synthetic-source-v1").stdout)
        self.assertEqual(a["event_id"],b["event_id"])
        self.assertEqual(a["scope"],"private")
        self.assertEqual(a["project_id"],"DEBO")
        self.assertEqual(a["evidence"][0]["ref"],self.source_ref)
        self.event.write_text(json.dumps(a),encoding="utf-8")
        if not shutil.which("node"):
            self.skipTest("Node unavailable; JavaScript planner is covered by separate Node tests")
        plan=subprocess.run(["node",str(SYNC),str(self.event)],capture_output=True,text=True,check=False,timeout=12)
        self.assertEqual(plan.returncode,0,plan.stderr[:200])
        result=json.loads(plan.stdout)
        self.assertEqual(result["result"],"DRY_RUN")
        self.assertEqual(result["writes"],0)
        self.assertEqual(result["destinations"],["OWNING_PROJECT_CHECKPOINT","DEBO_CORE_INDEX"])
        self.seen.write_text(json.dumps([a["event_id"]]),encoding="utf-8")
        skipped=subprocess.run(["node",str(SYNC),str(self.event),str(self.seen)],capture_output=True,text=True,check=False,timeout=12)
        self.assertEqual(skipped.returncode,0,skipped.stderr[:200])
        self.assertEqual(json.loads(skipped.stdout)["result"],"SKIP_DUPLICATE")

    def test_revised_checkpoint_requires_new_filename(self):
        python_tool("checkpoint","--input",self.capsule,"--output",self.saved)
        before=self.saved.read_bytes()
        self.data["next_action"]="Never silently overwrite previous proof"
        self.capsule.write_text(json.dumps(self.data),encoding="utf-8")
        failed=python_tool("checkpoint","--input",self.capsule,"--output",self.saved,expected=1)
        self.assertNotEqual(failed.returncode,0)
        self.assertEqual(self.saved.read_bytes(),before)

    def test_missing_proof_blocks_checkpoints_before_write(self):
        self.data["evidence"]=[]
        self.capsule.write_text(json.dumps(self.data),encoding="utf-8")
        failed=python_tool("checkpoint","--input",self.capsule,"--output",self.saved,expected=1)
        self.assertNotEqual(failed.returncode,0)
        self.assertFalse(self.saved.exists())

    def test_project_scoped_ids_differ_across_processes(self):
        a=python_tool("fingerprint","DEBO","The same objective", "--source-key", "task-001").stdout.strip()
        b=python_tool("fingerprint","JCT","The same objective", "--source-key", "task-001").stdout.strip()
        self.assertNotEqual(a,b)
        self.assertTrue(a.startswith("DEBO-TASK-"))

    def test_missing_task_id_rejected_without_writing(self):
        del self.data["task_id"]
        self.capsule.write_text(json.dumps(self.data),encoding="utf-8")
        failed=python_tool("checkpoint","--input",self.capsule,"--output",self.saved,expected=1)
        self.assertNotEqual(failed.returncode,0)
        self.assertFalse(self.saved.exists())

    def test_wrong_capsule_schema_rejected_without_writing(self):
        self.data["schema"]="debo.r19.other.v1"
        self.capsule.write_text(json.dumps(self.data),encoding="utf-8")
        failed=python_tool("checkpoint","--input",self.capsule,"--output",self.saved,expected=1)
        self.assertNotEqual(failed.returncode,0)
        self.assertFalse(self.saved.exists())

    def test_source_status_is_not_global_activation(self):
        contract=json.loads(GOV.read_text(encoding="utf-8"))
        self.assertEqual(contract["source_installation"]["state"],"SOURCE_MERGED_CI_PASS")
        self.assertFalse(contract["source_installation"]["external_chat_loader_installed"])
        self.assertFalse(contract["source_installation"]["external_agent_runtime_installed"])
        self.assertFalse(contract["source_installation"]["authenticated_private_store_connector_installed"])
        self.assertEqual(contract["source_installation"]["actual_cross_chat_readback"],"NOT_VERIFIED")
        self.assertFalse(contract["production_writes_enabled"])
        self.assertFalse(contract["scheduled_runners_enabled"])

if __name__=="__main__":
    unittest.main()
