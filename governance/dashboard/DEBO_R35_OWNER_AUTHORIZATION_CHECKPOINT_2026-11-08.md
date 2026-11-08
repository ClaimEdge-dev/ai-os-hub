# DEBO R35 | Owner Authorization and Isolated Mapping Checkpoint
Mission DEBO-MASTER-031; date 2026-11-08 America/Chicago.

## Owner decision
Owner explicitly authorized continuation across Rentals, JCT, D-Wing, P Logistics, RRR, Morgan's, DEBO Core/Neon, youth sports; specifically prohibits contacting or sending anything to anyone and public publication without separate approval. Independent John/coach/other owner authority remains mandatory where applicable. No spend, destructive action, access change or production release inferred.

## Verified execution
- Existing R34 mapping batch recovered; owner authorized internal continuation.
- 14 exact source-state mappings approved for **isolated internal development only** in `neon/recovery/debo_r18_mapping_approvals.json`, SHA 2736f8ef26aa7e82be0a97e2d484858bd1e5f55a, independently read back. Status values are internal normalization, not claims of public readiness.
- WORK-RENTALS-001 excluded from 14 task import mappings; its historical PARKED record preserved, but owner has lifted the hold for **private research and planning**. Do not contact landlords, tour, apply or publish.
- Neon receipts table installed in isolated slice-day1 branch; prior readback 0 tasks/0 receipts, default branch unaffected.
- Fresh schema inspection confirms tasks fields `parent_task` nullable, `assignee_role`, `pillar`, `title`, `status`, `priority` required; provenance has `source_row_sha256`, `mapped_status`, `mapping_reviewed_by`, `mapping_reviewed_at`, `import_state`. No task import yet.

## Remaining verification before data import
- Fresh source row hashes, titles, owner, priority, parent and blocker provenance; preserve exact state and 15th Rentals hold. No invented historical 5 tasks.
- Idempotent staging/import plan with authenticated connector, conflict handling and double readback.
- Current commit CI and dashboard/mobile acceptance unverified. No live service or cross-project auto-sync claimed.

## Thread Index
DEBO-00 > R20 runner > R31 router > R32 bridge > R33 local test > R34 isolated migration > R35 owner mapping approval.

Checkpoint R35-MAPPINGS-APPROVED-ISOLATED-IMPORT-PREFLIGHT. Next action: verify source row hashes, produce exact provenance records, then perform scoped nonproduction staging and readback.
