# DEBO R34 | One-Batch Source Mapping Approval Package
Date 2026-11-08. Owner requested review-batch, NOT mapping approval. 14 proposed exact-state mappings; NO import or task status changes.

Mapping rules: source state preserved verbatim; target status is a proposal, not proof of readiness. Target title from source objective/project_name requires owner confirmation; assignee_role from source owner; pillar from source project_id; parent_task NULL only after FK and hierarchy review. Do not overwrite historical source. Current Neon branch tasks count 0.

| Work ID | Source state (verbatim) | Proposed target | Proposed role | Proposed pillar |
|---|---|---|---|---|
| WORK-DEBO-001 | CHECKPOINT / EXECUTION CONTINUES IN PROJECT LANES | In Progress | DEBO | DEBO |
| WORK-JCT-001 | NATIVE BACKEND DEPLOYED PRIVATE / DATA SCHEMA VERIFIED / E2E HELD | Blocked | JCT-OPS | JCT |
| WORK-CE-001 | SOURCE RECOVERED / GOVERNANCE & LIVE E2E OPEN | In Progress | ClaimEdge | CE-OS |
| WORK-DWING-001 | PRIVATE V13 TESTED / V12 INTEGRATION BLOCKED | Blocked | D-Wing | DWING |
| WORK-SETTLE-001 | EXISTING EVIDENCE LEDGER / PRIMARY PROOF & DEDUPE OPEN | In Progress | Records Recovery | SETTLE |
| WORK-PLOG-001 | SOURCE RECONCILED / PRIMARY LEGAL AUTHORITY UNVERIFIED | Blocked | PLG-OPS | PLOG |
| WORK-RRR-001 | EXISTING BUILD VERIFIED / LIVE PUBLIC INTAKE UNVERIFIED | Review | RRR-OPS | RRR |
| WORK-MOL-001 | PRIVATE SOURCE DEMO / CANONICAL SITE-CRM UNVERIFIED | Review | MOL | MORGANS |
| WORK-BBS-001 | READY | Review | BBS | BBS |
| WORK-WRESTLE-001 | STAGED RECOVERY / LIVE DB ACCESS BLOCKED | Blocked | WrestlingOS | WRESTLE |
| WORK-ATHLETE-001 | PRIVATE PREVIEW SOURCE / PRODUCTION AUTH UNVERIFIED | Review | AthleteOS | ATHLETE |
| WORK-BASEBALL-001 | WAITING | Backlog | BaseballOS | BASEBALL |
| WORK-NEON-001 | BLOCKED — CONNECTED NEON HAS ZERO VISIBLE PROJECTS | Review | DEBO Systems | NEON |
| WORK-TPB-001 | RECOVERY + MEDIA QA OPEN | In Progress | DEBO-TPB-OS | DEBO-TPB-OS |

**Explicit exclusions:** WORK-RENTALS-001 owner authorized resume of PRIVATE research/planning in this chat; historical PARKED state remains unchanged until an authorized canonical source update. No housing outreach, applications or tours. Five historically claimed tasks not found in the source sheet remain unresolved. No mapping approval implied by this package.

**Owner approval requested later:** approve or edit each target status, role, pillar, title and parent relation after checking evidence. Status mapping review is separate from public launch approval. The R31 approvals JSON remains NOT_APPROVED and must not be altered until actual review.

**Database migration:** Approved isolated `slice-day1` non-default Neon branch br-sparkling-forest-a6n5v8rd project snowy-block-04251510. Created claimedge_os.task_sync_receipts plus task_sync_receipts_work_idx; readback table exists, index count 1, 0 receipts, 0 tasks. Default main branch br-lucky-smoke-a6qm5vgg readback receipts table absent. No task sync executed. Rollback: drop only after confirming no dependent consumers or accepted receipts; currently zero.

Checkpoint R34-ISOLATED-RECEIPTS-INSTALLED-MAPPINGS-REVIEW-READY. Next: review batch, run source reconciliation, then authenticated idempotent sync only after approval. No email or public publishing.
