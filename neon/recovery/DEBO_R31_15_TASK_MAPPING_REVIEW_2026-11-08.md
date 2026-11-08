# DEBO R31 | Exact Source Mapping Review and Owner Gate
Date: 2026-11-08 America/Chicago
Mission: DEBO-MASTER-031
Source: CURRENT — DEBO Live Project Index — v1.0, Portfolio Work Stack, A1:S25.
Status: PREPARED FOR REVIEW, NOT APPROVED. NO IMPORT AUTHORIZED.

## Canonical source states (verbatim)
| Work ID | Source state | Source approval needed | Gate |
| --- | --- | --- | --- |
| WORK-DEBO-001 | CHECKPOINT / EXECUTION CONTINUES IN PROJECT LANES | NO | QUARANTINE |
| WORK-JCT-001 | NATIVE BACKEND DEPLOYED PRIVATE / DATA SCHEMA VERIFIED / E2E HELD | YES — consequential owner/public/production only | QUARANTINE |
| WORK-CE-001 | SOURCE RECOVERED / GOVERNANCE & LIVE E2E OPEN | NO | QUARANTINE |
| WORK-DWING-001 | PRIVATE V13 TESTED / V12 INTEGRATION BLOCKED | YES | QUARANTINE |
| WORK-SETTLE-001 | EXISTING EVIDENCE LEDGER / PRIMARY PROOF & DEDUPE OPEN | NO | QUARANTINE |
| WORK-PLOG-001 | SOURCE RECONCILED / PRIMARY LEGAL AUTHORITY UNVERIFIED | YES | QUARANTINE |
| WORK-RRR-001 | EXISTING BUILD VERIFIED / LIVE PUBLIC INTAKE UNVERIFIED | YES | QUARANTINE |
| WORK-MOL-001 | PRIVATE SOURCE DEMO / CANONICAL SITE-CRM UNVERIFIED | YES — owner facts/public/site changes only | QUARANTINE |
| WORK-BBS-001 | READY | NO | QUARANTINE |
| WORK-WRESTLE-001 | STAGED RECOVERY / LIVE DB ACCESS BLOCKED | NO | QUARANTINE |
| WORK-ATHLETE-001 | PRIVATE PREVIEW SOURCE / PRODUCTION AUTH UNVERIFIED | NO | QUARANTINE |
| WORK-BASEBALL-001 | WAITING | NO | QUARANTINE |
| WORK-RENTALS-001 | PARKED BY OWNER / RECORDS PRESERVED | YES | HOLD_OWNER (immutable) |
| WORK-NEON-001 | BLOCKED — CONNECTED NEON HAS ZERO VISIBLE PROJECTS | YES | QUARANTINE; historical source status, not a current Neon connection verdict |
| WORK-TPB-001 | RECOVERY + MEDIA QA OPEN | NO — owner/coach gate for promotion | QUARANTINE |

## Required mapping and field decisions
- For each non-held ID: explicit exact-source-state -> target-state mapping with approver, timestamp and evidence; no blanket normalization.
- Required target fields: assignee_role, pillar, title, parent_task_id; identify canonical origin and allowed nullability.
- Verify current task schema and constraints on the isolated Neon branch before proposing an insert.
- Recover five historically reported tasks from authoritative source or record discrepancy; never synthesize records.
- For any task whose source says NO approval needed, that applies to the source task's own operational work, NOT to schema migration, mapping normalization, public release or production writes.

## Minimal owner approvals (separate)
A. Review and approve the exact 14 status mappings and field provenance.
B. Approve scoped nonproduction isolated schema/compute/rollback operation after inspecting migration SQL.
C. Approve live release only after authenticated sync, double readback, dashboard/mobile/security QA.

All other safe read-only inventory, code tests and documentation can continue independently.
