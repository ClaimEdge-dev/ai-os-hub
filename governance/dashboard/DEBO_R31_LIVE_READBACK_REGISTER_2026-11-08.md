# DEBO R31 | Live Readback & Installation Register
Mission: DEBO-MASTER-031
Date: 2026-11-08 America/Chicago
Branch: debo-r18-source-preserving-sync-20261108
Status: READ-ONLY ACCEPTANCE RECONCILIATION; NOT A PRODUCTION RELEASE

## Verified source readback
Canonical Drive sheet: CURRENT — DEBO Live Project Index — v1.0, Portfolio Work Stack.
15 rows, 15 distinct stable IDs. Source states are descriptive, not automatically normalized.
WORK-RENTALS-001: PARKED BY OWNER / RECORDS PRESERVED. Immutable owner hold.
14 other records: QUARANTINE pending reviewed exact-state mappings and target fields.
Canonical GitHub mapping manifest: NOT_APPROVED, empty mappings (blob 33bef730b6d05ef105f9dc4c6c4bff8d55693719).
Five historically reported additional tasks remain unverified.

## Isolated Neon readback
Project snowy-block-04251510, branch br-sparkling-forest-a6n5v8rd.
Core tasks: 0.
claimedge_os.task_source_provenance: installed (previously verified).
claimedge_os.task_sync_receipts: absent.
claimedge_os.debo_resume_capsules: installed, 0 rows.
claimedge_os.debo_thread_index: installed, 0 rows.
No write, migration, import, release or permission change performed.

## GitHub automation
R20-R29 offline CI run 42474433838: success (previous verified workflow job readback).
R30 workflow file includes the R30 readiness test step and path trigger (current branch blob 6a4f28eff61d52a4eeec7ec5f6477b46c1061104).
R30 current-commit workflow conclusion: UNKNOWN until a matching run and its steps are read.
Offline CI success does not establish a real Neon import or live dashboard.

## Installation register
| Component | Installed | Connected | Live | Next gate |
| --- | --- | --- | --- | --- |
| GitHub DEBO bootstrap | YES (repo) | YES (connector readback) | Repo source only | None for source |
| GitHub R20-R29 offline CI | YES | YES | YES for nonproduction tests | Verify R30 latest run |
| GitHub R30 safety gate | YES (dev branch) | Workflow configured | NOT VERIFIED on CI | Current-commit CI readback |
| Drive Work Stack | YES (source) | YES | Source readable | Approve 14 mappings |
| Neon isolated Core | YES (database) | YES | NO TASK SYNC | Owner-reviewed mappings and fields |
| Task provenance table | YES (isolated) | UNKNOWN data adapter | NO IMPORTS | Authenticated readback |
| Sync receipts table | NO | NO | NO | Scoped schema/rollback approval |
| R19 capsule table | YES (isolated) | Offline adapter tested | EMPTY | Authorized persistence and readback |
| R19 thread index table | YES (isolated) | Offline adapter tested | EMPTY | Authorized persistence and readback |
| Official dashboard | Candidate and source-health feed | Offline contract tested | Real task feed unverified | Live read model, stale/security QA, mobile |
| Sister project adapters | Mixed private candidates | UNKNOWN per project | UNKNOWN per project | Per-project evidence and owner gates |

## Critical path
1. Verify latest R30 CI workflow result against matching commit.
2. Recover and review authoritative status mappings for 14 records and required fields.
3. Recover five purported missing records or correct historical count.
4. Obtain explicit isolated schema/cost/rollback approval.
5. Install sync receipts and verify readback, then authenticated idempotent sync.
6. Verify Core records twice, dashboard real feed and fallback, iPhone/VoiceOver, security, and owner release.
7. File signed-off live acceptance. Do not promote based on offline fixtures.

## Thread Index
DEBO-00 → R18 Core → R20 Turbo → R29 Neon Adapter → R30 Safety Gate → R31 Acceptance → DEBO-05 Dashboard → R19 Continuity.

Checkpoint is source-readback evidence only; never treat this document as installed live functionality.
