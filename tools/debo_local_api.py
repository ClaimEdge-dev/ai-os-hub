"""Local-only DEBO command API; no Neon, cloud secrets, or public listener.

Local development gateway with scoped operators. Not production identity.
"""
import hmac
import json
import os
from pathlib import Path
from wsgiref.simple_server import make_server

from tools.debo_command_core import CommandCore


def application(core, token=None, allowed_projects=(), *, operators=None):
    if operators is None:
        operators = {"local-owner": {"token": token, "projects": allowed_projects}}
    validated = []
    seen = set()
    for actor_id, operator in operators.items():
        secret = operator.get("token")
        projects = frozenset(operator.get("projects", ()))
        if (not isinstance(actor_id, str) or not actor_id or not isinstance(secret, str)
                or len(secret) < 32 or secret in seen or not projects
                or not projects.issubset(core.project_ids)):
            raise ValueError("Invalid operator configuration, credential, or project scope")
        seen.add(secret)
        validated.append((actor_id, "Bearer " + secret, projects))
    if not validated:
        raise ValueError("At least one operator is required")
    dashboard = (Path(__file__).resolve().parents[1] / "web" / "debo-local.html").read_bytes()

    def respond(start_response, status, payload):
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        start_response(status, [("Content-Type", "application/json"),
                                ("Content-Length", str(len(body))),
                                ("Cache-Control", "no-store")])
        return [body]

    def app(environ, start_response):
        method, path = environ.get("REQUEST_METHOD", "GET"), environ.get("PATH_INFO", "")
        # Loopback listener alone does not prevent DNS-rebinding browser requests.
        host = environ.get("HTTP_HOST", "")
        valid_hosts = {"127.0.0.1:8765", "localhost:8765"}
        if host and host not in valid_hosts:
            return respond(start_response, "403 Forbidden", {"error": "Invalid local host"})
        origin = environ.get("HTTP_ORIGIN")
        if origin and origin not in {"http://" + h for h in valid_hosts}:
            return respond(start_response, "403 Forbidden", {"error": "Invalid local origin"})
        if method == "GET" and path == "/":
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"),
                       ("Content-Length", str(len(dashboard))),
                       ("Cache-Control", "no-store"),
                       ("X-Content-Type-Options", "nosniff"),
                       ("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")])
            return [dashboard]
        supplied = environ.get("HTTP_AUTHORIZATION", "")
        authenticated = None
        for actor_id, expected, scope in validated:
            if hmac.compare_digest(supplied, expected):
                authenticated = (actor_id, scope)
        if authenticated is None:
            core.audit_security("UNKNOWN", "API_REQUEST", "AUTH_DENIED")
            return respond(start_response, "401 Unauthorized", {"error": "Unauthorized"})
        actor_id, allowed_projects = authenticated
        try:
            if method == "GET" and path == "/tasks":
                return respond(start_response, "200 OK", {"tasks": core.list_tasks(allowed_projects)})
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
            core.audit_security(actor_id, "API_REQUEST", "ACCESS_DENIED")
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
        operators_json = os.environ.get("DEBO_LOCAL_OPERATORS_JSON")
        operators = json.loads(operators_json) if operators_json else None
        app = application(core, token, projects, operators=operators)
        with make_server("127.0.0.1", 8765, app) as server:
            print("DEBO local API listening on 127.0.0.1:8765", flush=True)
            server.serve_forever()
    finally:
        core.close()


if __name__ == "__main__":
    main()
