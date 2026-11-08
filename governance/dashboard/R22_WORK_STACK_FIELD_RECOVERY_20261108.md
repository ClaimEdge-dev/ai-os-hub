# DEBO R22 | Authoritative Work Stack field recovery (read-only)

Mission: DEBO-MASTER-026. Status: SOURCE FIELDS RECOVERED; MAPPINGS NOT APPROVED; NO IMPORTS.

## Canonical source
Google Drive **CURRENT — DEBO Live Project Index — v1.0**, spreadsheet ID `1T1udeSNxYEOU5HrS79V4hX6BTEw8XIfXB06-wUf8Gm8`, tab **Portfolio Work Stack**, read-only range A1:X24 on 2026-11-08. URL: https://docs.google.com/spreadsheets/d/1T1udeSNxYEOU5HrS79V4hX6BTEw8XIfXB06-wUf8Gm8/edit

## Verified fields
15 rows, unique work_id; headers: work_id, project_id, project_name, objective, state, priority, owner, started_at, last_touched_at, resume_point, next_action, dependency_ids, parallel_safe, approval_needed, blocker, return_to, source_refs, checkpoint_ref, notes.

The sheet provides objective, priority, owner, and project_id, **but not canonical Neon title, assignee_role, or pillar fields**. Proposed semantic correspondence is title <- objective or project_name, assignee_role <- owner, pillar <- project_id. These are **candidates, not approved mappings**, and must not be imported without review. Priority P0/P1/P2 is source-backed and within Neon enum; all 15 raw state strings remain unmapped. Source last_touched_at is a date, not a unique source revision token; use a stable row hash and revision/read timestamp for provenance before any import.

| work_id | source project_id | source priority | source owner | source state (verbatim) | mapping decision |
|---|---|---|---|---|---|
| WORK-DEBO-001 | DEBO | P0 | DEBO | CHECKPOINT / EXECUTION CONTINUES IN PROJECT LANES | QUARANTINE |
| WORK-JCT-001 | JCT | P0 | JCT-OPS | NATIVE BACKEND DEPLOYED PRIVATE / DATA SCHEMA VERIFIED / E2E HELD | QUARANTINE |
| WORK-CE-001 | CE-OS | P0 | ClaimEdge | SOURCE RECOVERED / GOVERNANCE & LIVE E2E OPEN | QUARANTINE |
| WORK-DWING-001 | DWING | P0 | D-Wing | PRIVATE V13 TESTED / V12 INTEGRATION BLOCKED | QUARANTINE |
| WORK-SETTLE-001 | SETTLE | P0 | Records Recovery | EXISTING EVIDENCE LEDGER / PRIMARY PROOF & DEDUPE OPEN | QUARANTINE |
| WORK-PLOG-001 | PLOG | P0 | PLG-OPS | SOURCE RECONCILED / PRIMARY LEGAL AUTHORITY UNVERIFIED | QUARANTINE |
| WORK-RRR-001 | RRR | P1 | RRR-OPS | EXISTING BUILD VERIFIED / LIVE PUBLIC INTAKE UNVERIFIED | QUARANTINE |
| WORK-MOL-001 | MORGANS | P1 | MOL | PRIVATE SOURCE DEMO / CANONICAL SITE-CRM UNVERIFIED | QUARANTINE |
| WORK-BBS-001 | BBS | P1 | BBS | READY | QUARANTINE |
| WORK-WRESTLE-001 | WRESTLE | P1 | WrestlingOS | STAGED RECOVERY / LIVE DB ACCESS BLOCKED | QUARANTINE |
| WORK-ATHLETE-001 | ATHLETE | P1 | AthleteOS | PRIVATE PREVIEW SOURCE / PRODUCTION AUTH UNVERIFIED | QUARANTINE |
| WORK-BASEBALL-001 | BASEBALL | P2 | BaseballOS | WAITING | QUARANTINE |
| WORK-RENTALS-001 | RENTALS | P1 | Rental OS | PARKED BY OWNER / RECORDS PRESERVED | HOLD_OWNER |
| WORK-NEON-001 | NEON | P0 | DEBO Systems | BLOCKED — CONNECTED NEON HAS ZERO VISIBLE PROJECTS | QUARANTINE; SOURCE STALE: isolated Neon read-only access since restored |
| WORK-TPB-001 | DEBO-TPB-OS | P1 | DEBO-TPB-OS | RECOVERY + MEDIA QA OPEN | QUARANTINE |

## Reconciliation
- Original source currently shows **15**, not 20, Work Stack records in this tab. Five claimed additional tasks have not been located or substantiated; do not fabricate.
- Neon task status CHECK allows Backlog, In Progress, Blocked, Review, Done. Compound source states cannot be safely coerced.
- Owner-held Rentals remains excluded from search, sync, or automation.
- R21 GitHub Actions run #7 passed offline end-to-end test: https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/42472030602
- No source edits, database writes, imports, or production changes performed.

## Next decision gate
Review mapping for title, assignee_role, pillar and each status. Preserve verbatim source state in approved provenance ledger. Then test isolated branch fixture with explicit approval and rollback before any real task refresh. Live dashboard transport is not yet connected.
