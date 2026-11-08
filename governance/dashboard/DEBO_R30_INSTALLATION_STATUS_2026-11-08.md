# DEBO R30 | Current execution and installation checkpoint
Date: 2026-11-08 America/Chicago
Mission: DEBO-MASTER-026. Existing unmerged branch: `debo-r18-source-preserving-sync-20261108`.
Status: R30 SAFETY GATE INSTALLED IN DEV; PRODUCTION NOT LIVE.

## Verified this execution
- GitHub Actions run 42474433838 (commit c9ba3ebd) concluded SUCCESS. R20/R21/R25/R26/R27/R29 offline test steps succeeded. This proves nonproduction CI execution, not live task or dashboard integration.
- Connected Drive Work Stack readback: 15 source rows, 15 distinct IDs; Rentals owner-parked.
- Isolated Neon branch `slice-day1` read-only query: 0 tasks. Tables: task_source_provenance present; task_sync_receipts absent; debo_resume_capsules present; debo_thread_index present. Existing installed tables are empty based on prior readback.
- Exact-state mapping approval manifest is NOT_APPROVED and contains no approved rules.
- Added `tools/debo_r30_gate.py` and `tools/test_debo_r30_gate.py`, verified GitHub readback.
- Local R30 tests: 10/10 passed. Nonproduction workflow now includes R30 tests and path triggers. Workflow source readback verified.
- Current-commit GitHub Actions run outcome after the R30 workflow change: NOT YET VERIFIED. Do not claim CI pass on R30 until a fresh run result is read.
- No real imports, DB writes, migrations, releases, production changes, access changes, or paid compute authorized/performed.

## Required gates before live
1. Owner-reviewed mapping and target-field provenance for 14 non-held source records.
2. Verify the five previously reported additional records or correct the historical count.
3. Approve isolated schema/compute/rollback boundaries.
4. Install and read back sync receipts on authorized isolated branch.
5. Authenticated real sync with idempotency and rollback, followed by two readbacks.
6. Connect dashboard to real read model and prove freshness/fallback/security.
7. Physical iPhone Safari/VoiceOver QA and explicit release approval.

Do not bypass any gate by assuming shorthand execution authorization is owner approval. Keep Rentals held.
Thread Index: DEBO-00 -> R20 Turbo -> R29 Neon Adapter -> R30 Readiness Gate -> DEBO-05 Dashboard -> R19 Continuity.
