# DEBO local operator scopes — Phase 2 pilot

Status: isolated local development, **not** production authentication. No hosted service or paid resource is required.

The local API supports separately configured bearer tokens and explicit project allowlists. Tokens must be at least 32 characters, cannot be reused by two operators, and must never be committed. Operator identity is derived from the authenticated token, not an incoming request field. A token only lists, reads, and operates on tasks belonging to its configured projects.

Start with `DEBO_LOCAL_DB` and `DEBO_LOCAL_PROJECTS` set to the approved local SQLite path and the complete registered project ID list. For one operator, set `DEBO_LOCAL_TOKEN` to a unique long secret. For multiple local operators, set `DEBO_LOCAL_OPERATORS_JSON` in the launching environment, for example using **placeholders only**:

```json
{"operator-ce":{"token":"REPLACE_WITH_UNIQUE_SECRET_AT_LEAST_32_CHARS","projects":["CE"]},"operator-bbs":{"token":"REPLACE_WITH_ANOTHER_UNIQUE_SECRET_AT_LEAST_32_CHARS","projects":["BBS"]}}
```

Never place actual tokens in shell history, checked-in `.env` files, screenshots, logs, or issue comments. Use trusted local secret injection where available. Only bind to loopback (`127.0.0.1`). Do not expose port 8765 to a public network.

The API also rejects browser requests with a non-loopback `Host` header or a foreign `Origin` header (local dashboard origins `http://127.0.0.1:8765` and `http://localhost:8765` are accepted). This is a basic defense against browser-based DNS rebinding and cross-origin misuse; it does not replace a production reverse proxy, TLS, authentication service, or rate limiting.

Security events in the local SQLite `security_events` table record a configured actor ID for forbidden operations, `UNKNOWN` for rejected credentials, and an outcome code. They intentionally omit raw bearer tokens, request payloads, IP addresses, and task content. Failed authentication and authorization are independently testable. Audit storage is **not tamper-proof**; protect the SQLite file and backups.

External actions remain in `WAITING_APPROVAL` because no production approval identity service is present. The only executable action is a deterministic local `note:` checkpoint. Before any production release, replace this pilot gateway with audited authenticated identity, rate limiting, secure token lifecycle, encrypted storage/backup, transport protections, and independent approval gates.
