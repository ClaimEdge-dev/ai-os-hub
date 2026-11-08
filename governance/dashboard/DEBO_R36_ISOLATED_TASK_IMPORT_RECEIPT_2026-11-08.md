# DEBO R36 | Isolated Task Import and Acceptance Receipt
Mission DEBO-MASTER-031. Date 2026-11-08 America/Chicago.
Branch: Neon project snowy-block-04251510 / isolated slice-day1 br-sparkling-forest-a6n5v8rd.
Source: Google Drive Portfolio Work Stack spreadsheet 1T1udeSNxYEOU5HrS79V4hX6BTEw8XIfXB06-wUf8Gm8, 15 rows.

## Actual execution
- Read live source rows and exact 14 owner-approved isolated mapping rules from neon/recovery/debo_r18_mapping_approvals.json.
- Verified each source state exactly matches the approved mapping, else fail closed.
- Staged 15 rows into claimedge_os.task_source_provenance using SHA-256 of complete row JSON as supplied by the source connector, with 14 APPROVED and 1 historical Rentals HELD. 15 unique IDs and 15 valid 64-character hashes confirmed.
- Imported 14 approved rows into isolated claimedge_os.tasks, preserving source objective as title, priority, owner as assignee_role, project_id as pillar, mapped status; parent_task NULL because no verified parent relation. Imported no Rentals task.
- Created 14 IMPORTED receipts in claimedge_os.task_sync_receipts; 14 provenance records updated to IMPORTED. No external communications or production changes.
- Double readback returned identical counts twice: tasks=14, provenance=15, imported_provenance=14, held_provenance=1, import_receipts=14, rentals_task=0, exact_field_matches=14.
- Idempotency test reran task insert with ON CONFLICT DO NOTHING: duplicate inserts=0.
- This is isolated database integration, not dashboard/live release or account-wide automation.

## Owner authorizations and remaining boundaries
User authorized internal continuation across project lanes and specifically prohibited emails, contacting anyone, and public publishing without separate approval. Other independent owner/coach rights remain relevant. Rentals private research/planning may resume; historical source HOLD kept intact pending an explicit canonical source update.

## Remaining work
- Verify GitHub current-commit CI, dashboard live data feed and iPhone/VoiceOver 5-task test.
- Reconcile five historically reported but absent source tasks without inventing them.
- Resolve current per-project authenticated owner/source access and independent owner release approvals.
- Any production promotion, customer intake or public posting remains separate.

## Thread Index
DEBO-00 > R20 Turbo > R31 router > R32 bridge > R33 local QA > R34 migration > R35 mapping approval > R36 isolated 14-task import.
Checkpoint: R36-ISOLATED-14-IMPORTED-DOUBLE-READBACK-PASS.
Next action: verify exact current-commit CI and private dashboard acceptance; prepare Rentals private research plan while preserving canonical source history.
