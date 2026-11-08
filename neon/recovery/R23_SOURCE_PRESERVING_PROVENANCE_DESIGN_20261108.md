# DEBO R23 | Source-preserving task mapping and provenance design

Mission DEBO-MASTER-026. Status: PROPOSED, NOT INSTALLED. 2026-11-08.

## Design principle
Drive Portfolio Work Stack is canonical for the 15 recovered work IDs and original state strings. Neon `claimedge_os.tasks` is a target projection, never the sole source of truth. Source state must remain verbatim and retrievable. Preserve owner-parked Rentals without scheduling or importing.

## Proposed companion ledger (not executed)
```sql
CREATE TABLE IF NOT EXISTS claimedge_os.task_source_provenance (
  source_system text NOT NULL,
  work_id text NOT NULL,
  source_document_id text NOT NULL,
  source_tab text NOT NULL,
  raw_source_state text NOT NULL,
  source_row_sha256 char(64) NOT NULL,
  source_read_at timestamptz NOT NULL,
  source_priority text NOT NULL,
  source_owner text NOT NULL,
  source_project_id text NOT NULL,
  source_objective text NOT NULL,
  mapping_rule_version text,
  mapped_status text,
  mapping_reviewed_by text,
  mapping_reviewed_at timestamptz,
  import_state text NOT NULL CHECK (import_state IN ('QUARANTINED','HELD','APPROVED','IMPORTED')),
  imported_at timestamptz,
  PRIMARY KEY (source_system, work_id),
  CHECK (mapped_status IS NULL OR mapped_status IN ('Backlog','In Progress','Blocked','Review','Done')),
  CHECK (import_state NOT IN ('APPROVED','IMPORTED') OR (mapped_status IS NOT NULL AND mapping_reviewed_by IS NOT NULL AND mapping_reviewed_at IS NOT NULL))
);
```
**Caution:** This is a schema proposal only. The ledger must not be created without explicit approval. For audit history, add append-only change events and restrictive role permissions in a separately reviewed migration; the single-row ledger above is not an audit log by itself.

## Candidate field mapping, not approved
- `task_id` <- exact `work_id` (identity only).
- `title` <- source `objective` (candidate; may be long), alternatively `project_name` (ambiguous).
- `assignee_role` <- source `owner` (candidate; some owners are organizations rather than roles).
- `pillar` <- source `project_id` (candidate; validate allowed semantics).
- `priority` <- source `priority` (source P0/P1/P2 within DB constraint).
- `status` <- **explicitly reviewed per-ID mapping only**. Never keyword infer from READY, WAITING, BLOCKED, DEPLOYED, VERIFIED, or mixed compound states.
- `due_date` <- NULL only when source explicitly lacks due date and owner approves nullable handling.
- `parent_task` <- NULL unless verified link.

## Deterministic ingestion gate
1. Read exact canonical sheet range and metadata; compute stable SHA-256 from canonicalized row values with an explicit versioned encoding, preserve raw string and source read timestamp.
2. Reject duplicate work_id, missing required source fields, invalid priority, malformed dates, source-version regressions, and mismatched hashes.
3. Quarantine 14 statuses. `WORK-RENTALS-001` remains HELD. Nothing is accepted for import until per-ID owner review.
4. Generate preview diff with accepted/quarantined/held/rejected counts, source hash, mapping rule version and target branch.
5. After explicit authorization, create provenance schema on isolated branch only; test a synthetic transaction and rollback; verify no residue independently.
6. Import one explicitly approved non-Rentals real row only after separate approval. Read back target, provenance, dashboard and source; check idempotency, conflict detection, zero duplicates, rollback plan, and no unrelated writes.
7. Promotion to production and public dashboard requires independent owner release gate and mobile accessibility acceptance.

## Current verified evidence
- Canonical Drive sheet: https://docs.google.com/spreadsheets/d/1T1udeSNxYEOU5HrS79V4hX6BTEw8XIfXB06-wUf8Gm8/edit, tab Portfolio Work Stack; 15 rows.
- GitHub R21 offline acceptance run #7 success: https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/42472030602
- R22 isolated Neon synthetic fixture rollback and independent post-check: 0 fixture residue, 0 total tasks.

## Approval still needed
Explicit approval for persistent isolated provenance schema creation and review of each per-ID status/field mapping. This design does not confer that approval. No production changes.
