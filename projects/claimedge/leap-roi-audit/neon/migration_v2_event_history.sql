-- Leap ROI + Claim Completeness Audit
-- Migration v2: event history, reconciliation health, idempotency, and corrected completeness math.
-- Additive / corrective migration proposal only.
-- Target: claimedge-prod / snowy-block-04251510 / neondb
-- DO NOT APPLY TO PRODUCTION until read-only schema audit + temporary-branch test + human approval.

CREATE SCHEMA IF NOT EXISTS leap_roi;

-- ---------------------------------------------------------------------------
-- 1) Idempotency keys for rerunnable imports
-- ---------------------------------------------------------------------------

ALTER TABLE leap_roi.field_audits
  ADD COLUMN IF NOT EXISTS event_key TEXT;

ALTER TABLE leap_roi.work_events
  ADD COLUMN IF NOT EXISTS event_key TEXT;

ALTER TABLE leap_roi.financial_events
  ADD COLUMN IF NOT EXISTS event_key TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_field_audits_event_key
  ON leap_roi.field_audits(event_key)
  WHERE event_key IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_work_events_event_key
  ON leap_roi.work_events(event_key)
  WHERE event_key IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_financial_events_event_key
  ON leap_roi.financial_events(event_key)
  WHERE event_key IS NOT NULL;

-- ---------------------------------------------------------------------------
-- 2) Sync / reconciliation run ledger
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.sync_runs (
  sync_run_id BIGSERIAL PRIMARY KEY,
  run_key TEXT UNIQUE NOT NULL,
  run_type TEXT NOT NULL
    CHECK (run_type IN ('WEBHOOK','DAILY_RECONCILIATION','ON_DEMAND','BACKFILL','VALIDATION')),
  provider TEXT NOT NULL DEFAULT 'LEAP',
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'IN_PROGRESS'
    CHECK (status IN ('IN_PROGRESS','COMPLETE','PARTIAL','AUTH_BLOCKED','RATE_LIMITED','FAILED','REVIEW_REQUIRED')),
  records_seen INTEGER NOT NULL DEFAULT 0,
  records_inserted INTEGER NOT NULL DEFAULT 0,
  records_updated INTEGER NOT NULL DEFAULT 0,
  records_unchanged INTEGER NOT NULL DEFAULT 0,
  records_conflicted INTEGER NOT NULL DEFAULT 0,
  records_errored INTEGER NOT NULL DEFAULT 0,
  source_cursor TEXT,
  source_as_of TIMESTAMPTZ,
  error_summary TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sync_runs_started_at
  ON leap_roi.sync_runs(started_at DESC);

CREATE INDEX IF NOT EXISTS idx_sync_runs_status
  ON leap_roi.sync_runs(status);

-- ---------------------------------------------------------------------------
-- 3) Normalized webhook inbox
-- Webhook payloads are triggers, not authoritative full job records.
-- Store only the normalized fields needed for audit/replay plus a hash.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.webhook_events (
  webhook_event_id BIGSERIAL PRIMARY KEY,
  sync_run_id BIGINT REFERENCES leap_roi.sync_runs(sync_run_id),
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  provider TEXT NOT NULL DEFAULT 'LEAP',
  provider_event_id TEXT,
  event_key TEXT UNIQUE NOT NULL,
  event_type TEXT NOT NULL,
  operation TEXT,
  entity_type TEXT,
  external_job_id TEXT,
  job_number TEXT,
  customer_id TEXT,
  task_id TEXT,
  stage_from TEXT,
  stage_to TEXT,
  event_occurred_at TIMESTAMPTZ,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  processed_at TIMESTAMPTZ,
  processing_status TEXT NOT NULL DEFAULT 'RECEIVED'
    CHECK (processing_status IN ('RECEIVED','PROCESSED','IGNORED','RETRY','FAILED','REVIEW_REQUIRED')),
  retry_count INTEGER NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
  payload_hash TEXT,
  normalized_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  source_locator TEXT,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_webhook_events_job
  ON leap_roi.webhook_events(external_job_id);

CREATE INDEX IF NOT EXISTS idx_webhook_events_claim
  ON leap_roi.webhook_events(claim_id);

CREATE INDEX IF NOT EXISTS idx_webhook_events_received
  ON leap_roi.webhook_events(received_at DESC);

CREATE INDEX IF NOT EXISTS idx_webhook_events_status
  ON leap_roi.webhook_events(processing_status);

-- ---------------------------------------------------------------------------
-- 4) Stage-transition history for cycle-time analysis
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.stage_events (
  stage_event_id BIGSERIAL PRIMARY KEY,
  event_key TEXT UNIQUE NOT NULL,
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  external_job_id TEXT,
  from_stage TEXT,
  to_stage TEXT NOT NULL,
  event_at TIMESTAMPTZ NOT NULL,
  source TEXT NOT NULL DEFAULT 'LEAP',
  source_webhook_event_id BIGINT REFERENCES leap_roi.webhook_events(webhook_event_id),
  verification_status TEXT NOT NULL DEFAULT 'SOURCE-CONFIRMED'
    CHECK (verification_status IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','ESTIMATED','MODELED','INFERRED','CONFLICTED')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (claim_id IS NOT NULL OR external_job_id IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS idx_stage_events_claim_time
  ON leap_roi.stage_events(claim_id, event_at);

CREATE INDEX IF NOT EXISTS idx_stage_events_job_time
  ON leap_roi.stage_events(external_job_id, event_at);

-- ---------------------------------------------------------------------------
-- 5) Owner snapshots preserve historical KPI state instead of recomputing
-- yesterday's story from today's data.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.owner_snapshots (
  owner_snapshot_id BIGSERIAL PRIMARY KEY,
  snapshot_key TEXT UNIQUE NOT NULL,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  scope TEXT NOT NULL DEFAULT 'ALL_ACTIVE',
  source_sync_run_id BIGINT REFERENCES leap_roi.sync_runs(sync_run_id),
  source_as_of TIMESTAMPTZ,
  claims_audited INTEGER NOT NULL DEFAULT 0,
  missing_fields INTEGER NOT NULL DEFAULT 0,
  conflicted_fields INTEGER NOT NULL DEFAULT 0,
  verified_fields INTEGER NOT NULL DEFAULT 0,
  minutes_saved NUMERIC(14,2) NOT NULL DEFAULT 0,
  verified_realized NUMERIC(14,2) NOT NULL DEFAULT 0,
  verified_identified NUMERIC(14,2) NOT NULL DEFAULT 0,
  modeled_opportunity NUMERIC(14,2) NOT NULL DEFAULT 0,
  directly_attributed_verified_value NUMERIC(14,2) NOT NULL DEFAULT 0,
  shared_verified_value NUMERIC(14,2) NOT NULL DEFAULT 0,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_owner_snapshots_generated_at
  ON leap_roi.owner_snapshots(generated_at DESC);

-- ---------------------------------------------------------------------------
-- 6) Correct historical-audit overcounting.
-- v1 joined every field audit ever recorded, which can overcount a field after
-- repeated audits. v2 uses only the newest audit per claim + field.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW leap_roi.v_latest_field_audit AS
SELECT DISTINCT ON (claim_id, field_key)
  field_audit_id,
  audit_run_id,
  claim_id,
  field_key,
  prior_value,
  current_value,
  prior_state,
  current_state,
  source_artifact_id,
  discovered_by,
  discovery_method,
  confidence,
  downstream_updates,
  minutes_manual_baseline,
  minutes_actual,
  notes,
  audited_at,
  event_key
FROM leap_roi.field_audits
ORDER BY claim_id, field_key, audited_at DESC, field_audit_id DESC;

CREATE OR REPLACE VIEW leap_roi.v_claim_completeness AS
SELECT
  c.claim_id,
  c.external_job_id,
  c.job_name,
  count(fr.field_key) FILTER (WHERE fr.active) AS required_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fa.current_state IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS verified_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND (fa.field_audit_id IS NULL OR fa.current_state='MISSING')
  ) AS missing_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fa.current_state='CONFLICTED'
  ) AS conflicted_fields
FROM leap_roi.claims c
CROSS JOIN leap_roi.field_requirements fr
LEFT JOIN leap_roi.v_latest_field_audit fa
  ON fa.claim_id=c.claim_id
 AND fa.field_key=fr.field_key
GROUP BY c.claim_id, c.external_job_id, c.job_name;

-- ---------------------------------------------------------------------------
-- 7) Cycle-time view.
-- Each transition's destination stage is treated as entered at event_at.
-- The next transition marks exit. Open/current stages have NULL exited_at.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW leap_roi.v_stage_durations AS
WITH ordered AS (
  SELECT
    stage_event_id,
    claim_id,
    external_job_id,
    to_stage AS stage,
    event_at AS entered_at,
    lead(event_at) OVER (
      PARTITION BY COALESCE(claim_id::text, external_job_id)
      ORDER BY event_at, stage_event_id
    ) AS exited_at,
    verification_status
  FROM leap_roi.stage_events
)
SELECT
  stage_event_id,
  claim_id,
  external_job_id,
  stage,
  entered_at,
  exited_at,
  CASE
    WHEN exited_at IS NOT NULL
    THEN EXTRACT(EPOCH FROM (exited_at-entered_at))/60.0
  END AS minutes_in_stage,
  verification_status
FROM ordered;

CREATE OR REPLACE VIEW leap_roi.v_sync_health AS
SELECT
  provider,
  max(source_as_of) FILTER (WHERE status IN ('COMPLETE','PARTIAL')) AS latest_source_as_of,
  max(completed_at) FILTER (WHERE status='COMPLETE') AS latest_complete_sync_at,
  count(*) FILTER (WHERE status='AUTH_BLOCKED') AS auth_blocked_runs,
  count(*) FILTER (WHERE status='FAILED') AS failed_runs,
  count(*) FILTER (WHERE status='REVIEW_REQUIRED') AS review_required_runs
FROM leap_roi.sync_runs
GROUP BY provider;

-- v_owner_summary from v1 continues to consume corrected v_claim_completeness.
