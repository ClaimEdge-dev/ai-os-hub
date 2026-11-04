# DEBO-MASTER-020 | Recovery execution checkpoint
Date: 2026-11-04 (America/Chicago)
Status: PARTIAL / READ-ONLY SOURCE VERIFICATION; NO RELEASE

## Confirmed readbacks
- DEBO_BOOTSTRAP.md: dashboard is read-only; public Core feed is governance metadata, never live business status. v0.2.2 is the rollback.
- docs/DEBO_DASHBOARD_V0_3_INTEGRATION_HANDOFF.md: v0.3 is an integration REVIEW CANDIDATE, not deployed; original private v0.2.2 bytes must be recovered before selecting or editing a newer canonical candidate.
- governance/dashboard/README.md: source feed contract and source-health limitation.
- governance/dashboard/DEBO_G3_SOURCE_ROUTE_MAP_v1.json: SCHOOL and CWA mapping recorded; Sheets writeback 403; education folder sharing review remains open.
- Google Drive metadata: original CURRENT — DEBO Live Project Index — v1.0 exists, private, last modified 2026-10-30; Trace Run Ledger v0.2 exists. No replacement copy verified.
## Decisions
1. Canonical source-control policy: existing GitHub Core; canonical dashboard implementation NOT YET SELECTED until private latest candidate and v0.2.2 original are inspected.
2. Do not promote v0.3 or later candidates based on historical tests alone.
3. 20-task queue reported in prior session, but individual 20 rows not independently recovered here: reconciliation PENDING, not completed.
4. Drive storageQuotaExceeded and Sheets 403 are prior observed blockers, not newly retested in this checkpoint. Preserve original. Alternate-account copy not authorized for a specified destination; no copy attempted.
5. JCT owner authentication deferred by user.
## Next executable steps
- Recover private dashboard candidate and original v0.2.2 bytes; compare hashes, features, tests; select one candidate without deploying.
- Retrieve actual 20-task source and classify each DONE/BLOCKED/NEXT/DUPLICATE with evidence.
- Diagnose quota and write authorization separately. If alternate account is approved and destination chosen, make private copy and verify all 17 tabs plus harmless write/readback before promotion.
- Run one task -> evidence -> review -> checkpoint -> dashboard refresh synthetic workflow, then authorized private real-source QA.
## Guardrails
No spending, deletion, production deployment, customer contact, credential exposure, permission changes, or unsupported claims of live sync.
Thread Index: DEBO-00 -> DEBO-MASTER-020 -> Dashboard Candidate Audit -> Queue Reconciliation -> Storage Recovery -> End-to-End QA.
