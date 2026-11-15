-- Leap ROI + Claim Completeness Audit
-- Hardening migration layered on top of migration_v1.sql.
-- Purpose: idempotency, webhook durability, reconciliation history, and accurate latest-state views.
-- Target: claimedge-prod / snowy-block-04251510 / neondb
-- DO NOT APPLY TO PRODUCTION until read-only audit + temporary-branch validation + human approval.

ALTER TABLE leap_roi.claims
  ADD COLUMN IF NOT EXISTS job_number TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_leap_roi_claims_external_job_id
  ON leap_roi.claims(external_job_id)
  WHERE external_job_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_leap_roi_claims_job_number
  ON leap_roi.claims(job_number)
  WHERE job_number IS NOT NULL;

CREATE TABLE IF NOT EXISTS leap_roi.webhook_events (
  webhook_event_id BIGSERIAL PRIMARY KEY,
  event_key TEXT NOT NULL UNIQUE,
  action TEXT,
  operation TEXT,
  external_id TEXT,
  external_job_id TEXT,
  job_number TEXT,
  customer_id TEXT,
  stage_from TEXT,
  stage_to TEXT,
  payload_hash TEXT NOT NULL,
  payload JSONB,
  source_event_at TIMESTAMPTZ,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  processed_at TIMESTAMPTZ,
  processing_status TEXT NOT NULL DEFAULT 'RECEIVED'
    CHECK (processing_status IN ('RECEIVED','PROCESSED','IGNORED','REVIEW_REQUIRED','FAILED')),
  retry_count INTEGER NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
  error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_leap_roi_webhook_job
  ON leap_roi.webhook_events(external_job_id, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_leap_roi_webhook_status
  ON leap_roi.webhook_events(processing_status, received_at DESC);

CREATE TABLE IF NOT EXISTS leap_roi.stage_history (
  stage_event_id BIGSERIAL PRIMARY KEY,
  event_key TEXT UNIQUE,
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  webhook_event_id BIGINT REFERENCES leap_roi.webhook_events(webhook_event_id),
  external_job_id TEXT,
  job_number TEXT,
  stage_from TEXT,
  stage_to TEXT NOT NULL,
  source_system TEXT NOT NULL DEFAULT 'Leap',
  source_event_at TIMESTAMPTZ,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_leap_roi_stage_history_claim
  ON leap_roi.stage_history(claim_id, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_leap_roi_stage_history_job
  ON leap_roi.stage_history(external_job_id, received_at DESC);

CREATE TABLE IF NOT EXISTS leap_roi.sync_runs (
  sync_run_id BIGSERIAL PRIMARY KEY,
  run_key TEXT NOT NULL UNIQUE,
  sync_type TEXT NOT NULL
    CHECK (sync_type IN ('WEBHOOK','DAILY_RECONCILIATION','ON_DEMAND_RECONCILIATION','BACKFILL')),
  source_system TEXT NOT NULL DEFAULT 'Leap',
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'IN_PROGRESS'
    CHECK (status IN ('IN_PROGRESS','COMPLETE','PARTIAL','AUTH_BLOCKED','FAILED','SUPERSEDED')),
  records_seen INTEGER NOT NULL DEFAULT 0 CHECK (records_seen >= 0),
  records_created INTEGER NOT NULL DEFAULT 0 CHECK (records_created >= 0),
  records_updated INTEGER NOT NULL DEFAULT 0 CHECK (records_updated >= 0),
  records_conflicted INTEGER NOT NULL DEFAULT 0 CHECK (records_conflicted >= 0),
  records_review_required INTEGER NOT NULL DEFAULT 0 CHECK (records_review_required >= 0),
  cursor_or_page TEXT,
  error_summary TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS leap_roi.reconciliation_findings (
  finding_id BIGSERIAL PRIMARY KEY,
  sync_run_id BIGINT NOT NULL REFERENCES leap_roi.sync_runs(sync_run_id),
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  external_job_id TEXT,
  job_number TEXT,
  finding_type TEXT NOT NULL
    CHECK (finding_type IN (
      'MISSING_IN_NEON',
      'MISSING_IN_LEAP',
      'FIELD_MISMATCH',
      'AMBIGUOUS_IDENTITY',
      'CONFLICTED_FINANCIAL',
      'STALE_SNAPSHOT',
      'DUPLICATE_CANDIDATE',
      'OTHER'
    )),
  field_key TEXT,
  leap_value TEXT,
  neon_value TEXT,
  resolution_status TEXT NOT NULL DEFAULT 'OPEN'
    CHECK (resolution_status IN ('OPEN','REVIEW_REQUIRED','RESOLVED','ACCEPTED_DIFFERENCE','SUPERSEDED')),
  evidence_basis TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  resolved_at TIMESTAMPTZ,
  notes TEXT
);

ALTER TABLE leap_roi.field_audits
  ADD COLUMN IF NOT EXISTS event_key TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_leap_roi_field_audits_event_key
  ON leap_roi.field_audits(event_key)
  WHERE event_key IS NOT NULL;

ALTER TABLE leap_roi.work_events
  ADD COLUMN IF NOT EXISTS event_key TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_leap_roi_work_events_event_key
  ON leap_roi.work_events(event_key)
  WHERE event_key IS NOT NULL;

ALTER TABLE leap_roi.financial_events
  ADD COLUMN IF NOT EXISTS event_key TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_leap_roi_financial_events_event_key
  ON leap_roi.financial_events(event_key)
  WHERE event_key IS NOT NULL;

CREATE OR REPLACE VIEW leap_roi.v_latest_field_audits AS
WITH ranked AS (
  SELECT
    fa.*,
    row_number() OVER (
      PARTITION BY fa.claim_id, fa.field_key
      ORDER BY fa.audited_at DESC, fa.field_audit_id DESC
    ) AS rn
  FROM leap_roi.field_audits fa
)
SELECT *
FROM ranked
WHERE rn = 1;

CREATE OR REPLACE VIEW leap_roi.v_time_savings AS
SELECT
  claim_id,
  count(*) AS work_event_count,
  sum(COALESCE(manual_baseline_minutes,0)) AS baseline_minutes,
  sum(COALESCE(actual_minutes,0)) AS actual_minutes,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) AS total_minutes_saved,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) FILTER (WHERE verification_status IN ('VERIFIED','SOURCE-CONFIRMED')) AS verified_minutes_saved,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) FILTER (WHERE verification_status IN ('USER-REPORTED','ESTIMATED','INFERRED')) AS estimated_minutes_saved,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) FILTER (WHERE verification_status = 'MODELED') AS modeled_minutes_saved
FROM leap_roi.work_events
GROUP BY claim_id;

CREATE OR REPLACE VIEW leap_roi.v_financial_summary AS
SELECT
  claim_id,
  sum(amount) FILTER (
    WHERE realization_state='VERIFIED_REALIZED'
      AND verification_status IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS verified_realized,
  sum(amount) FILTER (
    WHERE realization_state='VERIFIED_IDENTIFIED'
      AND verification_status IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS verified_identified,
  sum(amount) FILTER (
    WHERE realization_state='MODELED_OPPORTUNITY'
  ) AS modeled_opportunity,
  sum(amount) FILTER (
    WHERE attribution='DIRECT'
      AND realization_state IN ('VERIFIED_REALIZED','VERIFIED_IDENTIFIED')
      AND verification_status IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS directly_attributed_verified_value,
  sum(amount) FILTER (
    WHERE attribution='SHARED'
      AND realization_state IN ('VERIFIED_REALIZED','VERIFIED_IDENTIFIED')
      AND verification_status IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS shared_verified_value
FROM leap_roi.financial_events
GROUP BY claim_id;

CREATE OR REPLACE VIEW leap_roi.v_claim_completeness AS
SELECT
  c.claim_id,
  c.external_job_id,
  c.job_number,
  c.job_name,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND COALESCE(lfa.current_state,'MISSING') <> 'NOT-APPLICABLE'
  ) AS required_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND lfa.current_state IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS verified_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND COALESCE(lfa.current_state,'MISSING') = 'MISSING'
  ) AS missing_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND lfa.current_state = 'CONFLICTED'
  ) AS conflicted_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND lfa.current_state = 'NOT-APPLICABLE'
  ) AS not_applicable_fields
FROM leap_roi.claims c
CROSS JOIN leap_roi.field_requirements fr
LEFT JOIN leap_roi.v_latest_field_audits lfa
  ON lfa.claim_id = c.claim_id
 AND lfa.field_key = fr.field_key
GROUP BY c.claim_id, c.external_job_id, c.job_number, c.job_name;

CREATE OR REPLACE VIEW leap_roi.v_owner_summary AS
SELECT
  c.claim_id,
  c.external_job_id,
  c.job_number,
  c.job_name,
  cc.required_fields,
  cc.verified_fields,
  cc.missing_fields,
  cc.conflicted_fields,
  cc.not_applicable_fields,
  ts.total_minutes_saved,
  ts.verified_minutes_saved,
  ts.estimated_minutes_saved,
  ts.modeled_minutes_saved,
  fs.verified_realized,
  fs.verified_identified,
  fs.modeled_opportunity,
  fs.directly_attributed_verified_value,
  fs.shared_verified_value,
  CASE
    WHEN c.baseline_rcv IS NOT NULL AND c.current_rcv IS NOT NULL
    THEN c.current_rcv - c.baseline_rcv
  END AS documented_rcv_delta
FROM leap_roi.claims c
LEFT JOIN leap_roi.v_claim_completeness cc USING (claim_id)
LEFT JOIN leap_roi.v_time_savings ts USING (claim_id)
LEFT JOIN leap_roi.v_financial_summary fs USING (claim_id);
