# DEBO change detection v0.1 — review-only

Status: **SOURCE AVAILABLE**. This is an offline preview, NOT an active sync service.

**Reuse rather than replace** the existing `AUTO_SYNC_PROTOCOL.md`, `tools/debo_durable_save_gate.py`, and the DEBO Live Bridge Neon ledger described in the 2026-10-30 read-only sweep. Do **not** create duplicate `sync_*` database tables, access live business data, or activate a schedule.

Run from the repository root:

~~~bash
python tools/debo_sync_detect.py --dry-run=true
python -m unittest discover -s tests -p 'test_debo*.py' -v
~~~

Only three already-public policy/registry files are permitted by `sync/debo-change-manifest.json`. The detector reads them from the checkout and prints proposed JSON to stdout. It does not write, call an API, or store receipts. Symlink, traversal, duplicate source, invalid state and non-dry-run attempts fail closed.

A later **read-only exported ledger snapshot** may be placed in the git-ignored `sync/.private/` directory and passed as `--state=sync/.private/ledger_state.json`, formatted like `{"sources":{"debo-sync-protocol":{"fingerprint":"<64-hex-sha256>","version":1}}}`. Do **not** commit private data or ledger exports to the public repository. Without verified prior ledger history, proposed version 1 is a preview baseline, not a confirmed version. Private snapshots are never committed or emitted in full by the tool. Never copy customer records into a public checkout.

## Neon integration gates

- Existing `public.debo_core_change_events`: eventual destination for change events. A unique key on `(entity_type, entity_id, version)` does **not** by itself prevent repeated fingerprints; a future writer needs a serialized latest-fingerprint comparison.
- Existing `debo_evolution.execution_receipts`: outcome receipts, subject to checking actual column constraints.
- Existing `debo_evolution.diagnostics` and `connector_health`: failure recording, pending actual schema.
- Existing `tools/debo_durable_save_gate.py`: SHA-256 readback verifier; reuse it.

The Neon connector returned an authorization error on 2026-10-30, so actual columns, permissions, row counts and connectivity are **UNRESOLVED**. This preview does not demonstrate real persistence, transaction-safe deduplication, or interrupted-run recovery.

**Review-only QA:** A pull-request workflow runs the existing full DEBO unittest suite and this detector with `--dry-run=true`. GitHub CI status must be read from the exact current head commit. The pipeline does not prove persistence, Drive/Sheets access or cross-AI synchronization.

**Approval gate:** no live database writes, no secrets, no new platform, no customer-flow tests, no deployment, no merge. Owner-approved staging and authenticated access are required before any JC's Towing end-to-end test.
