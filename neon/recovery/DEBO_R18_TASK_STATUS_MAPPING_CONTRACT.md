# DEBO R18 | Task synchronization mapping contract (candidate)

Mission DEBO-MASTER-024. Status: PROPOSED, NOT DEPLOYED. Date 2026-11-08.

## Authority and safeguards
Google Drive Portfolio Work Stack is the source for the 15 verified work IDs and original detailed state strings. Neon original project snowy-block-04251510 / secondary slice-day1 is test-only for this work. Production main is not a test target. Keep rentals WORK-RENTALS-001 PARKED BY OWNER; do not trigger search or automation.

## Exact schema evidence
Neon claimedge_os.tasks has primary key task_id, NOT NULL title/status/priority/assignee_role/pillar, status CHECK Backlog/In Progress/Blocked/Review/Done, priority CHECK P0/P1/P2/P3, and updated_at trigger. It has no source_state, source_version, or provenance columns. Do not silently replace the Drive source state with a normalized status.

## Proposed deterministic transformation
1. Canonical identity: task_id = exact work_id (no regeneration). Preserve raw source state verbatim in separate provenance ledger before any import.
2. Normalized status: only explicit owner-reviewed mappings. The generic words READY, WAITING, BLOCKED, PRIVATE, VERIFIED, DEPLOYED in compound states are **not sufficient** to infer a lifecycle state. Unmapped -> quarantine, not Backlog by default.
3. Owner-parked work: quarantine/hold until owner resumes, never silently turn into Backlog or In Progress.
4. Priority, title, assignee_role, pillar must be sourced from authoritative fields and validated. No invented defaults; due_date and parent_task must validate.
5. Provenance ledger proposal: source_system, source_document_id, source_tab, work_id, raw_source_state, source_row_hash, source_version_or_read_timestamp, mapped_status, mapping_rule_version, review_decision, imported_at. Keep exact original text and stable identity; upsert by (source_system, work_id) with source-row version check and audit history.
6. Sync only approved rows with valid required fields; dry-run produces accepted/quarantined/rejected counts. Idempotency via task_id primary key and guarded upsert. Repeated same source version must not change rows. On conflicting updates, halt and log evidence.
7. Test in secondary branch only after separate provenance storage is approved; verify fixture insert, exact state readback, duplicate handling, rollback, zero residue, and no primary branch changes. Dashboard acceptance requires a real authorized end-to-end refresh and mobile tests.

## Verified tests to date
15 source IDs unique, 0 duplicates, 15 raw states unmapped under exact-only matching, 0 target tasks. Isolated synthetic transaction script completed and independent post-check returned 0 persisted synthetic records. Intermediate SQL assertions not separately surfaced. No actual Drive task import or dashboard acceptance.

## Decision gate
Owner authorization to execute safe reversible work does not authorize altering production schema, incurring costs, or promoting a deployment. Proposed provenance table and mapping choices remain unapproved. Next: implement a nonproduction offline mapper with unit tests and a reviewed mapping matrix; only then consider isolated integration fixture writes.