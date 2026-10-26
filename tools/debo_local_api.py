"""Local-only DEBO command API; no Neon, cloud secrets, or public listener.

Single-owner development gateway. Not a production identity system.
"""
import hmac
import io
import json
import os
from wsgiref.simple_server import make_server

from tools.debo_command_core import CommandCore


def application(core, token, allowed_projects):
    if not token or len(token) < 32:
        raise ValueError("DEBO_LOCAL_TOKEN must be at least 32 characters")
    allowed_projects = frozenset(allowed_projects)

    def respond(start_response, status, payload):
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        start_response(status, [("Content-Type", "application/json"),
                                ("Content-Length", str(len(body))),
                                ("Cache-Control", "no-store")])
        return [body]

    def app(environ, start_response):
        supplied = environ.get("HTTP_AUTHORIZATION", "")
        expected = "Bearer " + token
        if not hmac.compare_digest(supplied, expected):
            return respond(start_response, "401 Unauthorized", {"error": "Unauthorized"})
        method, path = environ.get("REQUEST_METHOD", "GET"), environ.get("PATH_INFO", "")
        try:
            if method == "POST" and path == "/tasks":
                size = int(environ.get("CONTENT_LENGTH", "0"))
                if size < 1 or size > 16384:
                    return respond(start_response, "413 Content Too Large", {"error": "Invalid payload size"})
                payload = json.loads(environ["wsgi.input"].read(size))
                task = core.submit(payload["command"], payload["project_id"], allowed_projects,
                                   payload["idempotency_key"])
                return respond(start_response, "200 OK", {"task": task})
            bits = path.strip("/").split("/")
            if len(bits) >= 2 and bits[0] == "tasks":
                task_id = bits[1]
                if len(bits) == 2 and method == "GET":
                    return respond(start_response, "200 OK", {"task": core.get(task_id, allowed_projects)})
                if len(bits) == 3 and bits[2] == "events" and method == "GET":
                    return respond(start_response, "200 OK", {"events": core.events(task_id, allowed_projects)})
                if len(bits) == 3 and bits[2] == "execute" and method == "POST":
                    return respond(start_response, "200 OK", {"task": core.execute_note(task_id, allowed_projects)})
            return respond(start_response, "404 Not Found", {"error": "Not found"})
        except (KeyError, ValueError, TypeError, json.JSONDecodeError):
            return respond(start_response, "400 Bad Request", {"error": "Invalid request"})
        except PermissionError:
            return respond(start_response, "403 Forbidden", {"error": "Operation forbidden"})

    return app


def main():
    token = os.environ.get("DEBO_LOCAL_TOKEN", "")
    db_path = os.environ.get("DEBO_LOCAL_DB", "./debo-local.sqlite")
    projects = set(filter(None, os.environ.get("DEBO_LOCAL_PROJECTS", "").split(",")))
    if not projects:
        raise SystemExit("Set DEBO_LOCAL_PROJECTS to explicitly authorized project IDs")
    core = CommandCore(db_path, projects)
    try:
        app = application(core, token, projects)
        with make_server("127.0.0.1", 8765, app) as server:
            print("DEBO local API listening on 127.0.0.1:8765", flush=True)
            server.serve_forever()
    finally:
        core.close()


if __name__ == "__main__":
    main()
