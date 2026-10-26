# DEBO Neon-free local command API — 2026-10-26

Status: **TESTED LOCALLY / NOT DEPLOYED / NOT PRODUCTION AUTHENTICATION**.

The Neon `damp-math-10052614` project remains unavailable to the current connection, so DEBO Phase 2 can make safe development progress with the local SQLite backend. This is a **temporary independent runtime**, not a competing canonical brain or replacement for the established Neon Live Bridge.

## Components

- `tools/debo_command_core.py`: durable task state, project-scope checks, idempotency and safe local execution.
- `tools/debo_local_api.py`: token-protected loopback WSGI API.
- `tests/test_debo_local_api.py`: auth failure, scoped access, duplicate request, full local task execution and error tests.

## Start locally

Run from the repository root in a trusted development environment:

```bash
export DEBO_LOCAL_TOKEN='SET_A_RANDOM_SECRET_OF_AT_LEAST_32_CHARACTERS'
export DEBO_LOCAL_PROJECTS='CE,BBS'
export DEBO_LOCAL_DB='./debo-local.sqlite'
python3 -m tools.debo_local_api
```

Replace the example token with a privately generated random value. Never commit it or paste it in chat. The service listens only on `127.0.0.1:8765`, **not** on a public network interface. Use `Authorization: Bearer <token>` for API requests.

Routes:

| Method | Path | Purpose |
|---|---|---|
| POST | `/tasks` | JSON `{command, project_id, idempotency_key}` |
| GET | `/tasks/{id}` | Read scoped task |
| GET | `/tasks/{id}/events` | Read evidence events |
| POST | `/tasks/{id}/execute` | Execute allowlisted `note:` action only |
| GET | `/tasks` | List recent tasks within the configured project scope |
| GET | `/` | Mobile-friendly local command dashboard (no private data embedded) |

The dashboard is served on the same local endpoint and asks for the bearer token after loading. It retains the token only in page memory. The interface supports task creation, scoped task listing, local-note execution and evidence inspection. It is not publicly hosted or visually QA-certified on an iPhone.

There is intentionally **no API route to approve or send** sensitive external actions. Unsupported commands stay `WAITING_APPROVAL`.

## Verification

`python3 -m unittest discover -s tests -p 'test_debo*.py' -v` → 28 tests passed locally on 2026-10-26.

## Security limitations

This is single-owner local development authentication using one bearer token. It is not a multi-user login, identity provider, session manager, TLS endpoint, or production RBAC implementation. Project access scopes come from operator configuration, and data is not encrypted at rest. Do not put claim records, credit reports, customer information, youth athlete data, or secrets in this test database. Before network/public hosting, implement authenticated identities, per-project authorization, CSRF/CORS policy as applicable, rate limiting, monitoring, backups, deployment security and a real approval service.

## Integration policy

When the historical Neon connection becomes available, inspect its schema and authorization model first; add an adapter and migration tests without overwriting existing tables. Do not silently copy local demo data into production.
