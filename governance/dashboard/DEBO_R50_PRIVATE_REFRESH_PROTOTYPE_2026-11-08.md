# DEBO R50 | Private summary service prototype
2026-11-08 America/Chicago. Mission DEBO-MASTER-031.
Created tools/debo_private_snapshot_server.py on nonproduction branch: localhost-only HTTP GET /api/private/tasks/summary; server-side bearer token compare_digest, reject unauthorized before DB, SQL read-only transaction, aggregate-only output via existing adapter, no-store, no CORS, no task names in response, fail closed on errors. Requires DEBO_PRIVATE_API_TOKEN (>=32 chars), DEBO_NEON_READONLY_DSN and DEBO_NEON_BRANCH; never hardcode secrets. DB role must be read-only and scoped to isolated Neon branch. Prototype does not support internet exposure.
Created tools/test_debo_private_snapshot_server.py with eight security-focused unittest cases: missing/bad token, successful aggregate, unknown path, query string, POST, bad config, held Rentals fail closed.
STATUS BUILT/COMMITTED; TESTS WRITTEN NOT EXECUTED IN THIS RUN. No verified database credentials or private hosting, so service not installed or live. Dashboard R49 remains static snapshot, unchanged. No production mutation.
Next: execute tests in CI or local environment, inspect readback, configure isolated read-only Neon role and secure private hosting with explicit owner authorization, test end-to-end before any live sync claim.
Checkpoint R50-PRIVATE-SERVER-PROTOTYPE-COMMITTED-TESTS-PENDING.
