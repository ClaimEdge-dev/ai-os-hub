-- DEBO R18: proposed PRIVATE/nonproduction Postgres migration. NOT APPLIED.
-- Requires explicit isolated-branch approval, cost review, and rollback plan.
-- Never run on production main. No customer data or secrets in this file.
BEGIN;
CREATE TABLE claimedge_os.task_source_provenance (
 source_system text NOT NULL,
 source_document_id text NOT NULL,
 source_tab text NOT NULL,
 work_id text NOT NULL,
 raw_source_state text NOT NULL,
 source_row_hash text NOT NULL CHECK (source_row_hash ~ '^[a-f0-9]{64}$'),
 source_read_at timestamptz NOT NULL,
 normalized_status text CHECK (normalized_status IN ('Backlog','In Progress','Blocked','Review','Done')),
 mapping_rule_version text NOT NULL,
 review_decision text NOT NULL CHECK (review_decision IN ('QUARANTINE','HOLD_OWNER','REJECT_REQUIRED_FIELDS','REVIEW_FIELD_MAPPING','ACCEPT')),
 reviewed_by text,
 reviewed_at timestamptz,
 last_seen_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY (source_system,source_document_id,source_tab,work_id),
 CHECK ((review_decision <> 'ACCEPT') OR (normalized_status IS NOT NULL AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL))
);
CREATE TABLE claimedge_os.task_sync_receipts (
 receipt_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 source_system text NOT NULL,
 work_id text NOT NULL,
 source_row_hash text NOT NULL CHECK(source_row_hash ~ '^[a-f0-9]{64}$'),
 outcome text NOT NULL CHECK (outcome IN ('STAGED','NOOP','CONFLICT','QUARANTINED','OWNER_HELD','REJECTED','IMPORTED','ROLLBACK')),
 occurred_at timestamptz NOT NULL DEFAULT now(),
 note text
);
CREATE INDEX task_sync_receipts_work_idx ON claimedge_os.task_sync_receipts (source_system,work_id,occurred_at DESC);
-- On a fresh approved branch only. Commit is deliberately explicit.
COMMIT;
