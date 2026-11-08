# DEBO-MASTER-024 | R18 continued acceptance and next-15 checkpoint
Date: 2026-11-08, America/Chicago. Thread: DEBO-00 | Neon Connection Recovery & Core Acceptance.
Checkpoint: **R18-NEXT15-SAFETY-GATES-TESTED**. Status: NONPRODUCTION CODE TESTED; CORE INTEGRATION NOT LIVE.

## Evidence and guardrails
- Canonical DEBO_BOOTSTRAP.md and generated DEBO runtime brief recovered. Existing feature branch reused: `debo-r18-source-preserving-sync-20261108`, unmerged.
- Two fresh private Drive Work Stack reads agree on 15 nonempty, distinct source IDs, zero duplicate IDs. The previously reported 20-task inventory remains unverified; do not fabricate the missing five.
- Original Neon project `snowy-block-04251510` recovered through the authorized connected ClaimEdge account. The `main` and `slice-day1` branches remain distinct. Explicit read-only SQL: primary tasks=0; two independent secondary reads tasks=0 and duplicate IDs=0.
- PostgreSQL live constraint review: task_id primary key; 5 allowed task statuses; P0-P3 priorities; parent-task foreign key. `task_source_provenance` and `task_sync_receipts` do not exist on secondary.
- Existing source mapping dry run classifies 14 QUARANTINE, 1 HOLD_OWNER, 0 ACCEPT. The owner-parked Rentals task remains held. Original Drive source has no verified `assignee_role` or `pillar` column.
- Source-preserving mapper, candidate nonproduction SQL and approvals JSON remain in existing R18 branch. Approvals manifest has `approval_state: NOT_APPROVED` and zero mapping rules.
- Strengthened `debo_r18_dashboard_source_contract.js` on the existing R18 branch: release eligibility now additionally requires explicit source freshness, security QA and owner approval, on top of source/Core/import verification and mobile QA. Expanded regression script passes **20 tests** locally on Node.js 22; the Git blob hashes of tested guard and test files match independent GitHub readback. GitHub commits: `af9d6d242e93eaf51720c982d2a046044b6184ef`, `5ff57e9609c215db9f5e3e594c237846f705154e`.
- Combined GitHub status and PR-triggered workflow lookup did not provide a current-commit CI run. **CI is UNVERIFIED**, not passing. No new task import, persistent DB migration, merge or public deployment in this execution.

## Ten carried-forward integration gates (1-10)
| # | Gate | Result |
|---|---|---|
| 1 | Owner-reviewed exact mappings for 14 source statuses | PENDING: no approvals; no guessing |
| 2 | Verified title, priority, assignee_role, pillar, dates and parents | PENDING: target-field mapping missing |
| 3 | Authorized isolated provenance schema and cost/isolation review | PENDING: candidate exists, approval not established |
| 4 | Install permanent provenance schema with rollback proof | NOT EXECUTED |
| 5 | Privately stage source records and source hashes | NOT EXECUTED |
| 6 | Authenticated idempotent task sync, conflict/update tests | NOT EXECUTED |
| 7 | Recover authoritative evidence for five purported extra tasks | UNRESOLVED |
| 8 | Two independent post-import Core list/provenance readbacks | NOT EXECUTED |
| 9 | Actual dashboard v0.3.3 source/hash, private E2E + fallback | NOT EXECUTED |
| 10 | Physical iPhone Safari/VoiceOver + security + owner release acceptance | NOT EXECUTED |

## Fifteen follow-on actions (11-25)
| # | Action in this batch | Observed result |
|---|---|---|
| 11 | Re-read canonical bootstrap and runtime rules | PASS: recovered; owner gates confirmed |
| 12 | Locate and reuse existing unmerged implementation branch | PASS: branch and receipt read |
| 13 | Recheck source Work Stack twice | PASS: same 15 rows/IDs |
| 14 | Compare stable source identities and duplicates | PASS: 15 unique, 0 duplicates |
| 15 | Check 20-task claim against authoritative source | UNRESOLVED: 5 missing records not invented |
| 16 | Inspect required target-field coverage | GAP CONFIRMED: role/pillar not in source |
| 17 | Inspect exact-state mapping approvals | GAP CONFIRMED: 0 approved |
| 18 | Check explicit owner hold | PASS: Rentals HOLD preserved |
| 19 | Resolve Neon project through connected owner scope | PASS: original 4-project account found |
| 20 | Inspect primary/secondary branch identities | PASS: separate branch IDs, no new branch |
| 21 | Compare read-only Core counts | PASS: primary 0, secondary 0 twice |
| 22 | Verify task schema and constraints live | PASS: primary key, status, priority, parent |
| 23 | Verify provenance storage installation state | PASS: both permanent provenance tables absent |
| 24 | Add security/owner/freshness release guards and regression tests | PASS: 20 local tests, GitHub source hash match |
| 25 | Read back code and inspect current-commit CI | PARTIAL: code readback PASS; CI UNVERIFIED |

## Honest finish state
**Built and tested:** strengthened nonproduction dashboard acceptance contract, 20 local Node tests, read-only database/source refresh, this scoped checkpoint.
**Not built or installed:** persistent provenance schema, authenticated sync adapter, live imported tasks, dashboard E2E, physical iPhone QA.
**Not authorized by shorthand:** source-status guessing, production modification, paid compute, public release, security/access changes.
**Next executable dependency:** an authority-backed per-task status and required-field mapping, plus approved nonproduction storage and cost/isolation scope. Then run migration readback, import receipts and authenticated dashboard acceptance, keeping the owner-parked task excluded.

Thread Index: DEBO-00 -> DEBO-MASTER-011 (Core sync acceptance) -> DEBO-05 (dashboard QA) -> R19 (continuity automation). One Core; no duplicate master.


## R18 lookup retry and offline staging acceptance — 2026-11-08

**RETRY RECOVERED:** Explicit read-only SQL succeeded on the original `slice-day1` branch (`br-sparkling-forest-a6n5v8rd`), returning `task_count=0` and `distinct_ids=0`. A direct public raw-file download failed due to container DNS resolution; the existing authenticated GitHub `fetch_file` source was already recovered, and its canonical blob SHA `e0a363c81b55b45aaa3b1b1d7369c79a8a0b634e` independently matched the exact dependency tested locally. No retry loop or access bypass.

**NEW BRANCH-LOCAL CODE AND QA:**
- Added `neon/recovery/debo_r18_stage_preview.js` (Git blob `c2c4aba0365f6f85a850bff36f000a9289b712cf`), pure JS, no SQL driver, network action or write eligibility. It rejects wrong/missing source provenance, rejects duplicate IDs/receipts, skips owner-held/unapproved rows, stages only reviewed valid rows, makes identical receipts NOOP, and routes changed source or mapping to CONFLICT_REVIEW.
- Added `neon/recovery/debo_r18_stage_preview.test.js` (Git blob `a0520a78cc95652e348e6409006826a964bcb2d5`). **20 of 20 synthetic Node.js assertions PASS**, including missing approvals, hold override, duplicate rejection, repeated import, source mutation, mapping mutation, receipt corruption, and in-memory rollback simulation. `node --test` also passed. Both file Git hashes matched independently fetched GitHub files after commits `13e6a8044ec4f5c6c37f5323ed6bc1b62ce71120` and `fe331e689ea5fbceabc6f9c0da81505565043773`.
- A passing **in-memory** rollback test is not a database transaction/rollback acceptance receipt. Historical isolated SQL rollback evidence remains separately documented. This addition does not implement a live authenticated sync adapter or approve the pending database migration.

**UNCHANGED GATES:** 14 source tasks need owner-reviewed status and target-field mapping; 1 Rentals task remains on owner HOLD; five purported extra tasks are unresolved. Source data were not exported into public GitHub. There are still zero imported Core tasks and no persistent provenance tables. Production `main`, customer data, pricing, access, and public dashboard deployment remain untouched. Current branch is a **TESTED NONPRODUCTION CANDIDATE**, not approved, merged, installed or live. The owner/field/isolated-storage acceptance gates remain prerequisites for actual sync.

**Checkpoint addendum:** `R18-OFFLINE-STAGING-RETRY-PASS`. Resume from existing gate 1/2 owner-reviewed status and target-field mappings, then authorized isolated migration and authenticated end-to-end readback. Reuse DEBO-00 -> Core acceptance -> DEBO-05 dashboard QA -> R19, no duplicate master.

## R18 | Rentals status-drift regression correction — 2026-11-08
**Checkpoint:** `R18-RENTALS-DRIFT-CODE-AND-JS-TEST-VERIFIED`
**Issue:** An earlier progress message said the Rental drift tests were complete before the updated test files were actually present. This is the corrected code and evidence record.
- R18 JavaScript planner `debo_r18_sync_plan.js` blob `efcaaa0464822924e635fc9ef78f3f8ebb84d7b8` holds task ID `WORK-RENTALS-001` independent of mutable source state.
- R18 Python planner `debo_r18_sync_preview.py` blob `2e67950335523bf6a72e563711e29dfc7d64f0d5` applies the equivalent task-ID hold.
- Newly updated JavaScript regression `debo_r18_sync_plan.test.js` blob `d6605084248528a9c3ddbeee48093dfd14b0cc7c`: four new tests, including READY/IN PROGRESS status drift and approved READY mapping bypass attempt. Execution in V8 with a deterministic crypto compatibility shim: 24/24 assertions PASS. This run does **not** independently prove Node's native crypto implementation.
- Newly updated Python regression `test_debo_r18_sync_preview.py` blob `2e602b4be7eba35f2f4705783e59d7ef0ab754aa`: four task-ID drift tests present, for 16 total test methods. GitHub source readback verified. Its browser executor only returned a prepared script, not an execution receipt; do not count that tool result as a fresh PASS.
- The public GitHub repository feature branch remains **unmerged and nonproduction**. No real Drive task import; no persistent provenance schema; no Core/database production modification or dashboard release.
**Next:** Obtain a verified Python runtime test receipt, then complete owner-reviewed mapping and required target-field provenance before any isolated real synchronization.
