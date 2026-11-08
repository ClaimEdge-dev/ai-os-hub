# DEBO R26 | Memory and Thread Continuity Adapter v1

Mission DEBO-MASTER-026 / R26. 2026-11-08. Status: COMMITTED SPECIFICATION; NOT GLOBAL CHATGPT MEMORY ACTIVATION.

## Scope
Extends existing DEBO Runtime Bootstrap v2, communication/recovery standard, and existing checkpoints; does not replace Golden Rules or create a second master brain. GitHub stores nonsecret code/policies and redacted references; permissioned project systems retain sensitive records. A chat is a workspace, not a reliable database.

## Continuity contract
Every mission's Resume Capsule must include: schema_version, mission_id, project_id, canonical_sources (URLs and version identifiers), thread_index_refs, objective, completed (each with evidence and verification state), active_tasks, decisions (scope/approver/time), owner_holds, blockers (cause/attempted route/retry condition), next_action, last_verified_at, source_fingerprint, checkpoint_location, save_readback_status. Never claim a saved checkpoint without readback. Never infer global ChatGPT memory installation from repository writes.

## State machine
PROPOSED -> BUILT -> TESTED -> VERIFIED -> INSTALLED -> LIVE. Independent booleans for each scope and environment; never use LIVE for a proposed integration. Owner holds override task routing. A thread's completion is not a project's completion.

## Safe merge algorithm
1. Recover bootstrap and owning project brief, then newest verified capsule; search only accessible prior threads and connected sources.
2. Verify source versions and project identity; preserve conflicts instead of overwriting or assuming freshness.
3. Deduplicate by (project_id, mission_id, source_record_id) and content fingerprint; retain event history rather than silently mutating a verified decision.
4. Apply explicit owner holds and approval gates before proposing action; do not promote old permissions to unrelated projects or environments.
5. Route actionable tasks to existing project adapters; choose smallest authorized reversible next step.
6. Test changes, write capsule to authorized canonical store, read back exact revision/hash; update Thread Index pointer and checkpoint receipt.
7. If inaccessible, mark NOT_SAVED or UNVERIFIED, retain next retry instruction; never invent cross-thread sync.

## Thread Index format
One row per thread: thread_ref, project_id, mission_id, suggested_title, last_verified_checkpoint_ref, active_next_action, current_status, last_verified_at, source_version. Thread titles are suggestions until the actual ChatGPT UI rename is verified. Maintain pointer to one canonical project capsule, not a duplicate copy in every thread.

## Automation proposals (NOT INSTALLED)
- On mission start: bootstrap -> resolve project -> read capsule -> reconcile delta -> work.
- On material state change: write append-only delta, verify readback, update project capsule and Thread Index.
- On recurring maintenance: detect stale checkpoints, missing evidence, duplicates, owner holds, CI failures; report rather than auto-promote.
- Cross-project propagation: publish only a nonsecret, versioned routing summary; do not replicate customer data, youth information or private documents.
- Retry budget: one distinct authorized alternate route per blocker, then checkpoint without looping.

## Tests required before installation
Fresh-session recovery; two-thread merge with conflicting source revisions; duplicate idempotency; owner hold; no unauthorized approval inheritance; failed write readback; stale pointer; sensitive-data exclusion; false-LIVE prevention; interrupted-session resume; CI receipt link verification.

## Next action
Implement deterministic capsule validator and test suite on dev branch, connect it to existing CI, and verify actual CI result. Separately assess approved canonical storage and UI/Work connector capability before any claimed cross-thread activation.
