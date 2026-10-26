import io
import json
import tempfile
import unittest
from pathlib import Path
from tools.debo_command_core import CommandCore
from tools.debo_local_api import application


class LocalAPITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.core = CommandCore(Path(self.tmp.name) / "data.sqlite", {"CE", "BBS"})
        self.addCleanup(self.core.close)
        self.token = "a" * 48
        self.app = application(self.core, self.token, {"CE"})

    def call(self, method, path, payload=None, token=None, headers=None):
        body = json.dumps(payload).encode() if payload is not None else b""
        env = {"REQUEST_METHOD": method, "PATH_INFO": path,
               "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body)}
        if token is not None:
            env["HTTP_AUTHORIZATION"] = "Bearer " + token
        env.update(headers or {})
        status = []
        data = b"".join(self.app(env, lambda s, h: status.append(s)))
        return status[0], json.loads(data)

    def test_token_required_and_wrong_token_rejected(self):
        self.assertTrue(self.call("GET", "/tasks/nope")[0].startswith("401"))
        self.assertTrue(self.call("GET", "/tasks/nope", token="wrong")[0].startswith("401"))

    def test_local_end_to_end(self):
        payload = {"command": "note: safe checkpoint", "project_id": "CE", "idempotency_key": "idem-1"}
        status, data = self.call("POST", "/tasks", payload, self.token)
        self.assertEqual(status, "200 OK")
        task_id = data["task"]["id"]
        self.assertEqual(self.call("POST", "/tasks", payload, self.token)[1]["task"]["id"], task_id)
        self.assertEqual(self.call("POST", f"/tasks/{task_id}/execute", token=self.token)[1]["task"]["state"], "VERIFIED")
        self.assertEqual(len(self.call("GET", f"/tasks/{task_id}/events", token=self.token)[1]["events"]), 2)

    def test_project_denied_and_external_action_blocked(self):
        status, _ = self.call("POST", "/tasks", {"command": "note: x", "project_id": "BBS", "idempotency_key": "x"}, self.token)
        self.assertTrue(status.startswith("403"))
        status, data = self.call("POST", "/tasks", {"command": "send email", "project_id": "CE", "idempotency_key": "y"}, self.token)
        self.assertEqual(data["task"]["state"], "WAITING_APPROVAL")
        self.assertTrue(self.call("POST", "/tasks/" + data["task"]["id"] + "/execute", token=self.token)[0].startswith("403"))

    def test_payload_limit_and_bad_json(self):
        self.assertTrue(self.call("POST", "/tasks", token=self.token)[0].startswith("413"))
        self.assertTrue(self.call("POST", "/tasks", {"oops": True}, self.token)[0].startswith("400"))

    def test_dashboard_and_scoped_list(self):
        # Public local UI contains no private task data; API still requires token.
        status = []
        html = b"".join(self.app({"REQUEST_METHOD": "GET", "PATH_INFO": "/"},
                                 lambda s, h: status.append((s, h)))).decode()
        self.assertEqual(status[0][0], "200 OK")
        self.assertIn("DEBO Command Center", html)
        self.assertIn("Content-Security-Policy", dict(status[0][1]))
        self.assertTrue(self.call("GET", "/tasks")[0].startswith("401"))
        self.core.submit("note: hidden", "BBS", {"BBS"}, "hidden")
        self.core.submit("note: visible", "CE", {"CE"}, "visible")
        status, data = self.call("GET", "/tasks", token=self.token)
        self.assertEqual(status, "200 OK")
        self.assertEqual([x["project_id"] for x in data["tasks"]], ["CE"])

    def test_independent_operator_tokens_and_denial_audit(self):
        bbs_token = "b" * 48
        self.app = application(self.core, operators={
            "ce-operator": {"token": self.token, "projects": ["CE"]},
            "bbs-operator": {"token": bbs_token, "projects": ["BBS"]},
        })
        ce_task = self.call("POST", "/tasks", {"command": "note: ce", "project_id": "CE",
              "idempotency_key": "ce-only"}, self.token)[1]["task"]["id"]
        bbs_task = self.call("POST", "/tasks", {"command": "note: bbs", "project_id": "BBS",
              "idempotency_key": "bbs-only"}, bbs_token)[1]["task"]["id"]
        self.assertEqual([t["id"] for t in self.call("GET", "/tasks", token=self.token)[1]["tasks"]], [ce_task])
        self.assertEqual([t["id"] for t in self.call("GET", "/tasks", token=bbs_token)[1]["tasks"]], [bbs_task])
        for path in (f"/tasks/{bbs_task}", f"/tasks/{bbs_task}/events"):
            self.assertTrue(self.call("GET", path, token=self.token)[0].startswith("403"))
        self.assertTrue(self.call("POST", f"/tasks/{bbs_task}/execute", token=self.token)[0].startswith("403"))
        self.assertTrue(self.call("GET", "/tasks", token="invalid")[0].startswith("401"))
        rows = [dict(r) for r in self.core.db.execute("SELECT * FROM security_events ORDER BY id")]
        self.assertEqual([r["outcome"] for r in rows], ["ACCESS_DENIED"] * 3 + ["AUTH_DENIED"])
        self.assertTrue(all(r["actor_id"] in {"ce-operator", "UNKNOWN"} for r in rows))
        self.assertNotIn(self.token, str(rows))
        self.assertNotIn(bbs_token, str(rows))

    def test_operator_configuration_rejects_shared_or_short_tokens(self):
        with self.assertRaises(ValueError):
            application(self.core, operators={"a": {"token": self.token, "projects": ["CE"]},
                                              "b": {"token": self.token, "projects": ["BBS"]}})
        with self.assertRaises(ValueError):
            application(self.core, operators={"a": {"token": "short", "projects": ["CE"]}})
        with self.assertRaises(ValueError):
            application(self.core, operators={"a": {"token": self.token, "projects": ["UNKNOWN"]}})

    def test_dns_rebinding_and_cross_origin_requests_rejected(self):
        for headers in ({"HTTP_HOST": "attacker.example:8765"},
                        {"HTTP_HOST": "127.0.0.1:8765", "HTTP_ORIGIN": "https://attacker.example"},
                        {"HTTP_HOST": "localhost:8765", "HTTP_ORIGIN": "null"}):
            self.assertTrue(self.call("GET", "/tasks", token=self.token, headers=headers)[0].startswith("403"))
        self.assertEqual(self.call("GET", "/tasks", token=self.token,
            headers={"HTTP_HOST": "localhost:8765", "HTTP_ORIGIN": "http://localhost:8765"})[0], "200 OK")


if __name__ == "__main__":
    unittest.main()
