"""R50 private HTTP service security tests, no network or database."""
import http.client
import threading
import unittest
from http.server import ThreadingHTTPServer
from debo_private_snapshot_server import make_handler

TOKEN = "t" * 40
ROW = dict(task_id="WORK-TEST-1",title="Test",status="Review",priority="P1",assignee_role="Proof",pillar="Systems")

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        def fetch(dsn):
            self.calls.append(dsn)
            return [ROW]
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(TOKEN, "fake-readonly-dsn", "slice-day1", fetch))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
    def request(self, path="/api/private/tasks/summary", headers=None, method="GET"):
        c = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        c.request(method, path, headers=headers or {})
        r = c.getresponse()
        body = r.read()
        result = (r.status, dict(r.getheaders()), body)
        c.close()
        return result
    def test_no_token_denied_before_db(self):
        self.assertEqual(self.request()[0], 401)
        self.assertEqual(self.calls, [])
    def test_bad_token_denied(self):
        self.assertEqual(self.request(headers={"Authorization":"Bearer bad"})[0],401)
        self.assertEqual(self.calls, [])
    def test_valid_token_returns_aggregate_only(self):
        status, headers, body = self.request(headers={"Authorization":"Bearer "+TOKEN})
        self.assertEqual(status,200)
        self.assertEqual(headers["Cache-Control"],"no-store")
        self.assertEqual(__import__("json").loads(body)["task_count"],1)
        self.assertNotIn(b"Test",body)
        self.assertNotIn(b"WORK-TEST-1",body)
    def test_unknown_path_no_db(self):
        self.assertEqual(self.request(path="/private")[0],404)
        self.assertEqual(self.calls,[])
    def test_query_string_not_allowed(self):
        self.assertEqual(self.request(path="/api/private/tasks/summary?x=1")[0],404)
    def test_post_denied(self):
        self.assertEqual(self.request(method="POST")[0],405)
    def test_bad_config_denied(self):
        with self.assertRaises(ValueError):
            make_handler("short","dsn","slice-day1")
        with self.assertRaises(ValueError):
            make_handler(TOKEN,"dsn","main")
    def test_held_record_fails_closed(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        def held(dsn):
            return [{**ROW,"task_id":"WORK-RENTALS-001"}]
        self.server=ThreadingHTTPServer(("127.0.0.1",0),make_handler(TOKEN,"dsn","slice-day1",held))
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.assertEqual(self.request(headers={"Authorization":"Bearer "+TOKEN})[0],503)

if __name__=="__main__":
    unittest.main()
