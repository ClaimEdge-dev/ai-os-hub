-- Leap ROI + Claim Completeness Audit
-- Canonical hardening migration v2.
-- Target: claimedge-prod / snowy-block-04251510 / neondb
--
-- CANONICAL ORDER:
--   1) migration_v1.sql
--   2) migration_v2_event_history.sql
--   3) validation_v1.sql
--   4) temporary_test_fixture.sql (temporary branch only)
--
-- DO NOT APPLY TO PRODUCTION until read-only schema audit + temporary-branch
-- test + human approval.

CREATE SCHEMA IF NOT EXISTS leap_roi;

-- ---------------------------------------------------------------------------
-- 1) Claim identity additions
-- ---------------------------------------------------------------------------

ALTER TABLE leap_roi.claims
  ADD COLUMN IF NOT EXISTS job_number TEXT;

CREATE INDEX IF NOT EXISTS idx_leap_roi_claims_job_number
  ON leap_roi.claims(job_number)
  WHERE job_number IS NOT NULL;

-- Do NOT add a production UNIQUE constraint on external_job_id until the
-- duplicate preflight has run. Ambiguous/duplicate identities must be reviewed,
-- not hidden by a failed migration.

-- ---------------------------------------------------------------------------
-- 2) Idempotency keys for rerunnable imports
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
-- 3) Sync / reconciliation run ledger
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.sync_runs (
  sync_run_id BIGSERIAL PRIMARY KEY,
  run_key TEXT UNIQUE NOT NULL,
  run_type TEXT NOT NULL
    CHECK (run_type IN (
      'WEBHOOK',
      'DAILY_RECONCILIATION',
      'ON_DEMAND',
      'BACKFILL',
      'VALIDATION'
    )),
  provider TEXT NOT NULL DEFAULT 'LEAP',
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'IN_PROGRESS'
    CHECK (status IN (
      'IN_PROGRESS',
      'COMPLETE',
      'PARTIAL',
      'AUTH_BLOCKED',
      'RATE_LIMITED',
      'FAILED',
      'REVIEW_REQUIRED',
      'SUPERSEDED'
    )),
  records_seen INTEGER NOT NULL DEFAULT 0 CHECK (records_seen >= 0),
  records_inserted INTEGER NOT NULL DEFAULT 0 CHECK (records_inserted >= 0),
  records_updated INTEGER NOT NULL DEFAULT 0 CHECK (records_updated >= 0),
  records_unchanged INTEGER NOT NULL DEFAULT 0 CHECK (records_unchanged >= 0),
  records_conflicted INTEGER NOT NULL DEFAULT 0 CHECK (records_conflicted >= 0),
  records_review_required INTEGER NOT NULL DEFAULT 0 CHECK (records_review_required >= 0),
  records_errored INTEGER NOT NULL DEFAULT 0 CHECK (records_errored >= 0),
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
-- 4) Normalized webhook inbox
-- Webhooks are durable triggers, not complete claim or financial truth.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.webhook_events (
  webhook_event_id BIGSERIAL PRIMARY KEY,
  sync_run_id BIGINT REFERENCES leap_roi.sync_runs(sync_run_id),
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  provider TEXT NOT NULL DEFAULT 'LEAP',
  provider_event_id TEXT,
  event_key TEXT UNIQUE NOT NULL,
  action TEXT,
  operation TEXT,
  entity_type TEXT,
  external_id TEXT,
  external_job_id TEXT,
  job_number TEXT,
  customer_id TEXT,
  task_id TEXT,
  stage_from TEXT,
  stage_to TEXT,
  source_event_at TIMESTAMPTZ,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  processed_at TIMESTAMPTZ,
  processing_status TEXT NOT NULL DEFAULT 'RECEIVED'
    CHECK (processing_status IN (
      'RECEIVED',
      'PROCESSED',
      'IGNORED',
      'RETRY',
      'FAILED',
      'REVIEW_REQUIRED'
    )),
  retry_count INTEGER NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
  payload_hash TEXT NOT NULL,
  normalized_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  source_locator TEXT,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_webhook_events_job
  ON leap_roi.webhook_events(external_job_id, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_webhook_events_claim
  ON leap_roi.webhook_events(claim_id, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_webhook_events_status
  ON leap_roi.webhook_events(processing_status, received_at DESC);

-- ---------------------------------------------------------------------------
-- 5) Stage transitions for cycle-time analysis
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS leap_roi.stage_events (
  stage_event_id BIGSERIAL PRIMARY KEY,
  event_key TEXT UNIQUE NOT NULL,
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  external_job_id TEXT,
  job_number TEXT,
  from_stage TEXT,
  to_stage TEXT NOT NULL,
  event_at TIMESTAMPTZ NOT NULL,
  source TEXT NOT NULL DEFAULT 'LEAP',
  source_webhook_event_id BIGINT REFERENCES leap_roi.webhook_events(webhook_event_id),
  verification_status TEXT NOT NULL DEFAULT 'SOURCE-CONFIRMED'
    CHECK (verification_status IN (
      'VERIFIED',
      'SOURCE-CONFIRMED',
      'USER-REPORTED',
      'ESTIMATED',
      'MODELED',
      'INFERRED',
      'CONFLICTED'
    )),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (claim_id IS NOT NULL OR external_job_id IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS idx_stage_events_claim_time
  ON leap_roi.stage_events(claim_id, event_at);

CREATE INDEX IF NOT EXISTS idx_stage_events_job_time
  ON leap_roi.stage_events(external_job_id, event_at);

-- ---------------------------------------------------------------------------
-- 6) Reconciliation findings
-- Keeps ambiguous identity and source conflicts visible instead of overwriting.
-- ---------------------------------------------------------------------------

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
    CHECK (resolution_status IN (
      'OPEN',
      'REVIEW_REQUIRED',
      'RESOLVED',
      'ACCEPTED_DIFFERENCE',
      'SUPERSEDED'
    )),
  evidence_basis TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  resolved_at TIMESTAMPTZ,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_reconciliation_findings_status
  ON leap_roi.reconciliation_findings(resolution_status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_reconciliation_findings_job
  ON leap_roi.reconciliation_findings(external_job_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- 7) Owner snapshots preserve historical KPI state.
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
  unverified_fields INTEGER NOT NULL DEFAULT 0,
  verified_fields INTEGER NOT NULL DEFAULT 0,
  not_applicable_fields INTEGER NOT NULL DEFAULT 0,
  minutes_saved NUMERIC(14,2) NOT NULL DEFAULT 0,
  verified_minutes_saved NUMERIC(14,2) NOT NULL DEFAULT 0,
  estimated_minutes_saved NUMERIC(14,2) NOT NULL DEFAULT 0,
  modeled_minutes_saved NUMERIC(14,2) NOT NULL DEFAULT 0,
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
-- 8) Latest-field view fixes historical overcounting.
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

-- ---------------------------------------------------------------------------
-- 9) Time savings with verified / estimated / modeled separation.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW leap_roi.v_time_savings AS
SELECT
  claim_id,
  count(*) AS work_event_count,
  sum(COALESCE(manual_baseline_minutes,0)) AS baseline_minutes,
  sum(COALESCE(actual_minutes,0)) AS actual_minutes,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) AS minutes_saved,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) FILTER (
    WHERE verification_status IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS verified_minutes_saved,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) FILTER (
    WHERE verification_status IN ('USER-REPORTED','ESTIMATED','INFERRED')
  ) AS estimated_minutes_saved,
  sum(
    GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)
  ) FILTER (
    WHERE verification_status='MODELED'
  ) AS modeled_minutes_saved
FROM leap_roi.work_events
GROUP BY claim_id;

-- ---------------------------------------------------------------------------
-- 10) Financial summary.
-- VERIFIED_* buckets require strong verification status.
-- ---------------------------------------------------------------------------

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

-- ---------------------------------------------------------------------------
-- 11) Completeness uses only latest audit per field.
-- Optional and NOT-APPLICABLE fields do not inflate the denominator.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW leap_roi.v_claim_completeness AS
SELECT
  c.claim_id,
  c.external_job_id,
  c.job_number,
  c.job_name,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND COALESCE(fa.current_state,'MISSING') <> 'NOT-APPLICABLE'
  ) AS required_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND fa.current_state IN ('VERIFIED','SOURCE-CONFIRMED')
  ) AS verified_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND COALESCE(fa.current_state,'MISSING')='MISSING'
  ) AS missing_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND fa.current_state='CONFLICTED'
  ) AS conflicted_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND fa.current_state IN (
        'USER-REPORTED',
        'CARRIER-ASSERTED',
        'ESTIMATED',
        'MODELED',
        'INFERRED'
      )
  ) AS unverified_fields,
  count(fr.field_key) FILTER (
    WHERE fr.active
      AND fr.importance <> 'OPTIONAL'
      AND fa.current_state='NOT-APPLICABLE'
  ) AS not_applicable_fields
FROM leap_roi.claims c
CROSS JOIN leap_roi.field_requirements fr
LEFT JOIN leap_roi.v_latest_field_audit fa
  ON fa.claim_id=c.claim_id
 AND fa.field_key=fr.field_key
GROUP BY c.claim_id, c.external_job_id, c.job_number, c.job_name;

-- ---------------------------------------------------------------------------
-- 12) Cycle-time view.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW leap_roi.v_stage_durations AS
WITH ordered AS (
  SELECT
    stage_event_id,
    claim_id,
    external_job_id,
    job_number,
    to_stage AS stage,
    event_at AS entered_at,
    lead(event_at) OVER (
      PARTITION BY CASE
        WHEN claim_id IS NOT NULL THEN 'claim:' || claim_id::text
        ELSE 'job:' || external_job_id
      END
      ORDER BY event_at, stage_event_id
    ) AS exited_at,
    verification_status
  FROM leap_roi.stage_events
)
SELECT
  stage_event_id,
  claim_id,
  external_job_id,
  job_number,
  stage,
  entered_at,
  exited_at,
  CASE
    WHEN exited_at IS NOT NULL
    THEN EXTRACT(EPOCH FROM (exited_at-entered_at))/60.0
  END AS minutes_in_stage,
  verification_status
FROM ordered;

-- ---------------------------------------------------------------------------
-- 13) Sync health.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW leap_roi.v_sync_health AS
SELECT
  provider,
  max(source_as_of) FILTER (
    WHERE status IN ('COMPLETE','PARTIAL')
  ) AS latest_source_as_of,
  max(completed_at) FILTER (
    WHERE status='COMPLETE'
  ) AS latest_complete_sync_at,
  count(*) FILTER (WHERE status='AUTH_BLOCKED') AS auth_blocked_runs,
  count(*) FILTER (WHERE status='RATE_LIMITED') AS rate_limited_runs,
  count(*) FILTER (WHERE status='FAILED') AS failed_runs,
  count(*) FILTER (WHERE status='REVIEW_REQUIRED') AS review_required_runs
FROM leap_roi.sync_runs
GROUP BY provider;

-- ---------------------------------------------------------------------------
-- 14) Owner summary.
-- ---------------------------------------------------------------------------

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
  cc.unverified_fields,
  cc.not_applicable_fields,
  ts.minutes_saved,
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
