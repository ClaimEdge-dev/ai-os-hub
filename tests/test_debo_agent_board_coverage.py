import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json").read_text())

class DEBOAgentBoardCoverage(unittest.TestCase):
    def test_unique_roles(self):
        ids=[x["id"] for x in DATA["roles"]]
        self.assertEqual(len(ids), len(set(ids)))
    def test_required_core(self):
        ids={x["id"] for x in DATA["roles"]}
        self.assertTrue({"DEBO-MACK","DEBO-ATLAS","DEBO-FORGE","DEBO-PROOF","DEBO-SHIELD"} <= ids)
    def test_skill_count_and_unique_routing(self):
        rows=DATA["jct"]["skills"]
        self.assertEqual(len(rows),50)
        self.assertEqual(len({x["skill"] for x in rows}),50)
        self.assertEqual(len({x["source_path"] for x in rows}),50)
    def test_no_claim_of_live_workers(self):
        for role in DATA["roles"]:
            self.assertNotEqual(role["worker_status"],"VERIFIED_RUNNING")
        for skill in DATA["jct"]["skills"]:
            self.assertEqual(skill["runtime_tested"],"NOT_VERIFIED")
    def test_sister_scope(self):
        self.assertEqual(len({p["project_id"] for p in DATA["project_adapters"]}),13)
if __name__ == "__main__":
    unittest.main()
