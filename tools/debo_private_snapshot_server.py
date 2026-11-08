"""DEBO R50 private, loopback-only read-only snapshot HTTP service.

Not production deployed. Auth is enforced here, not asserted by the caller.
Requires DEBO_PRIVATE_API_TOKEN and DEBO_NEON_READONLY_DSN in server environment.
The DSN MUST belong to a read-only Neon role on an isolated branch.
"""
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from debo_private_task_snapshot import build_private_snapshot, safe_summary

SQL = """SELECT task_id,title,status,priority,assignee_role,pillar
FROM claimedge_os.tasks ORDER BY task_id LIMIT 5001"""

def query_rows(dsn):
    import psycopg  # optional runtime dependency, never shipped with dashboard
    with psycopg.connect(dsn, connect_timeout=5, autocommit=False) as conn:
        with conn.cursor() as cur:
            cur.execute("SET TRANSACTION READ ONLY")
            cur.execute("SET LOCAL statement_timeout = '5000ms'")
            cur.execute(SQL)
            if len(cur.description) != 6:
                raise ValueError("unexpected task schema")
            rows = [dict(zip(("task_id","title","status","priority","assignee_role","pillar"), r)) for r in cur.fetchall()]
            conn.rollback()
            return rows

def make_handler(token, dsn, source_branch, fetch_rows=query_rows):
    if not token or len(token) < 32 or not dsn or not source_branch or source_branch in ("main", "production"):
        raise ValueError("missing secure private configuration")
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if urlsplit(self.path).path != "/api/private/tasks/summary" or self.path != "/api/private/tasks/summary":
                return self.send_error(404)
            supplied = self.headers.get("Authorization", "")
            expected = "Bearer " + token
            if not hmac.compare_digest(supplied.encode(), expected.encode()):
                return self.send_error(401, "Unauthorized")
            try:
                rows = fetch_rows(dsn)
                if len(rows) > 5000:
                    raise ValueError("task cap exceeded")
                snapshot = build_private_snapshot(rows, authenticated=True, source_branch=source_branch)
                body = json.dumps(safe_summary(snapshot), separators=(",", ":")).encode()
            except Exception:
                return self.send_error(503, "Private data unavailable")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'")
            self.end_headers()
            self.wfile.write(body)
        def do_POST(self):
            self.send_error(405)
        def log_message(self, format, *args):
            # No authorization header or private task data in logs.
            pass
    return Handler

def main():
    token = os.environ.get("DEBO_PRIVATE_API_TOKEN", "")
    dsn = os.environ.get("DEBO_NEON_READONLY_DSN", "")
    branch = os.environ.get("DEBO_NEON_BRANCH", "")
    handler = make_handler(token, dsn, branch)
    # Loopback only; do not forward publicly or use this as internet-facing auth.
    ThreadingHTTPServer(("127.0.0.1", 8765), handler).serve_forever()

if __name__ == "__main__":
    main()
