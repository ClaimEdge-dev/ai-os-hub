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

    def call(self, method, path, payload=None, token=None):
        body = json.dumps(payload).encode() if payload is not None else b""
        env = {"REQUEST_METHOD": method, "PATH_INFO": path,
               "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body)}
        if token is not None:
            env["HTTP_AUTHORIZATION"] = "Bearer " + token
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


if __name__ == "__main__":
    unittest.main()
