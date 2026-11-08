-- DEBO R31 | isolated branch ONLY | PROPOSED, NOT EXECUTED
-- Requires explicit approval of schema mutation, branch identity, cost and rollback.
-- Do not rerun the R18 CREATE TABLE task_source_provenance migration: that table exists
-- with a different deployed schema. This migration creates ONLY the missing receipts table.
BEGIN;
CREATE TABLE IF NOT EXISTS claimedge_os.task_sync_receipts (
  receipt_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_system text NOT NULL,
  work_id text NOT NULL,
  source_row_sha256 char(64) NOT NULL CHECK (source_row_sha256 ~ '^[a-f0-9]{64}$'),
  outcome text NOT NULL CHECK (outcome IN
    ('STAGED','NOOP','CONFLICT','QUARANTINED','OWNER_HELD','REJECTED','IMPORTED','ROLLBACK')),
  occurred_at timestamptz NOT NULL DEFAULT now(),
  note text
);
CREATE INDEX IF NOT EXISTS task_sync_receipts_work_idx
 ON claimedge_os.task_sync_receipts (source_system,work_id,occurred_at DESC);
COMMIT;
-- Rollback ONLY after confirming no dependent consumers or accepted receipts:
-- BEGIN;
-- DROP TABLE claimedge_os.task_sync_receipts;
-- COMMIT;
