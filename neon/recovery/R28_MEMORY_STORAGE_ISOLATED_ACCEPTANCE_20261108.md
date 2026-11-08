# R28 Memory storage isolated acceptance — 2026-11-08
Mission DEBO-MASTER-026. Environment: Neon project snowy-block-04251510, isolated branch br-sparkling-forest-a6n5v8rd only; NOT production.

VERIFIED: created claimedge_os.debo_resume_capsules and claimedge_os.debo_thread_index using CREATE TABLE IF NOT EXISTS; information_schema readback confirmed 6 and 7 columns respectively. Synthetic capsule+thread insertion, in-transaction readback, forced exception rollback completed. Independent readback confirmed 0 capsules and 0 threads after test. Existing task/provenance data untouched.

BUILT: tools/debo_r28_neon_storage_adapter.py, explicit injected Postgres connection, parameterized SQL, transactional upsert and readback, rollback on mismatch, no embedded secrets. Adapter not yet executed with a live Python DB driver, no CI test coverage yet, no production install. Shared hosted database schema is present on isolated branch, but no application service or automatic ChatGPT session sync is connected. Do not claim globally LIVE.

Safety: owner holds remain in validated capsule; no actual project/task data imported; no ChatGPT settings or production branch modified. Access control, role isolation, retention and API service still need independent acceptance before live activation.

NEXT ACTION: add R28 adapter unit/integration tests and CI wiring, test scoped DB credentials and project isolation in nonproduction, verify run, then design supported ChatGPT/Work retrieval path with explicit permission boundaries.
