# DEBO-MASTER-024 | R18 nonproduction batch execution receipt
Date: 2026-11-08 (America/Chicago). Status: TESTED CANDIDATE, NOT INSTALLED OR LIVE.
Suggested thread: DEBO-00 | Neon Recovery & Core Acceptance.
Branch: `debo-r18-source-preserving-sync-20261108` (unmerged; production main untouched).

## Recover and verify
- Loaded canonical `DEBO_BOOTSTRAP.md`, generated `governance/runtime-briefs/DEBO.md`, previous R18 checkpoint, mapping contract, prior temporary fixture receipt and original Drive Work Stack.
- Authenticated Neon integration exposes four projects. Original historical ID `snowy-block-04251510` = `claimedge-prod`; original branches `main` = `br-lucky-smoke-a6qm5vgg` and `slice-day1` = `br-sparkling-forest-a6n5v8rd`. Do not equate production-named project or branch with an approved task store.
- Two independent reads of company Drive `Portfolio Work Stack!A1:P30`: 15 nonempty rows; 15 distinct `work_id`, zero duplicates, 15 detailed states, no conflicting read. Source had no verified Core `assignee_role` or `pillar` fields. Reported five additional tasks not located and must not be invented.
- Fresh read-only SQL on both Neon branches returned `tasks.total=0` and `distinct_ids=0`. This is missing synchronization, not an acceptance pass.
- Live-source dry-run with empty explicit status approvals: ACCEPT=0, QUARANTINE=14, HOLD_OWNER=1 (`WORK-RENTALS-001`), REJECT=0. All 15 raw states preserved. Zero import-eligible tasks.
- Original Work Stack `WORK-NEON-001` contains stale zero-visible-projects text relative to latest connector verification; authoritative source Sheet deliberately not modified.

## New safe artifacts (unmerged branch)
- `debo_r18_sync_plan.js` and `debo_r18_sync_plan.test.js`: exact-state review enforcement, stable-ID validation, source-row fingerprint, idempotency/no-op versus changed-source conflict, owner hold, private dry-run only.
- `debo_r18_sync_preview.py` and `test_debo_r18_sync_preview.py`: equivalent offline private-CSV preview, SHA-256 row hash, no DB writes.
- `debo_r18_mapping_approvals.json`: intentionally zero approved mapping rules. No approval is assumed.
- `debo_r18_provenance_MIGRATION_CANDIDATE.sql`: proposed persistent private Postgres provenance and audit schema, **NOT EXECUTED**. No production migration.
- `debo_r18_dashboard_source_contract.js` and test: health remains UNKNOWN and release held until source+Core+import readback+physical mobile QA are each verified.

## QA and rollback receipts
- Python: 12 local `unittest` assertions passed. Git blob hashes of both public Python files matched bytes tested locally.
- JavaScript: 20 planner assertions plus 5 dashboard-contract assertions passed in JavaScript validation harness using a deterministic hash shim in place of Node crypto. These are logic checks, not proof of exact runtime `node` execution; production cryptographic hashing remains the built-in Node SHA-256 implementation.
- Explicit secondary branch, SQL `DO` nested-exception rollback: created one synthetic provenance fixture table/record with schema/hash/status checks, asserted in-block count=1 and intentionally rolled back. Tool returned success but did not expose intermediate assertion values. Two independent post-check SQL reads confirmed temporary fixture table absent, permanent provenance table absent, and `claimedge_os.tasks` still 0 rows.
- GitHub readbacks of the six original JS/JSON/SQL files and two Python files succeeded.
- GitHub workflows latest successfully completed on separate R19 candidate branch and previous main commits; **no CI runs for this R18 feature branch** were found. Do not treat other branches' green checks as R18 acceptance.
- Existing read-only public Core dashboard feed continues to label operational status UNKNOWN; no dashboard application E2E performed.
- No real Drive source row was inserted into Neon. No new Neon project, no permanent schema change, no production mutation, no public deployment, no external sends or credentials accessed.

## Next ten execution gates, in order
1. **PENDING** Secure owner-reviewed exact status mappings for 14 unmapped rows; keep Rentals parked. Do not infer from descriptive English.
2. **PENDING** Verify target title, assignee_role, pillar, priority, due date and parent mapping against authoritative project adapters. No guessed defaults.
3. **CANDIDATE** Approve a private nonproduction branch and provenance migration with isolation and compute/cost review; candidate SQL exists but not installed.
4. **PENDING** Apply provenance schema in approved nonproduction target, then independent readback and rollback recovery proof.
5. **PENDING** Stage original Drive data privately, verify fingerprints and source version, and quarantine conflicted/held rows.
6. **PENDING** Implement authenticated idempotent sync adapter for approved rows only; test duplicate prevention, updates, concurrent conflicts and source history.
7. **PENDING** Reconcile 15 verified original IDs against the reported 20 using authoritative evidence; five missing source tasks remain UNKNOWN.
8. **PENDING** Complete two private Neon Core reads after a permitted import, matching task IDs and provenance to the Drive source with zero duplicates.
9. **PENDING** Validate dashboard v0.3.3 actual source/hash, authenticated source-to-dashboard refresh and fault/UNKNOWN states; preserve v0.2.2 rollback.
10. **PENDING** Perform physical iPhone Safari + VoiceOver five-task QA, security/owner release review, and only then consider merge/deploy through separate approvals.

## Safety / checkpoint
PROJECT_ID: DEBO
MISSION_ID: DEBO-MASTER-024
CHECKPOINT: R18-NONPROD-BATCH-VALIDATED
LAST_VERIFIED: 15-source read pair; 14/1 classification; 25 JS harness checks; 12 Python tests; secondary SQL rollback double-read.
NOT_COMPLETE: status approvals, source field mapping, persistent ledger, authenticated sync, five missing tasks, dashboard/mobile acceptance.
NEXT_ACTION: owner-reviewed status and target field mapping, then approved isolated persistent migration and readback. Keep production and dashboard release held.
