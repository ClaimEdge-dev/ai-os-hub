-- Leap ROI + Claim Completeness Audit
-- Additive migration proposal only.
-- Target: claimedge-prod / snowy-block-04251510 / neondb
-- DO NOT APPLY until read-only schema audit + temporary-branch test + human approval.

CREATE SCHEMA IF NOT EXISTS leap_roi;

CREATE TABLE IF NOT EXISTS leap_roi.audit_runs (
  audit_run_id BIGSERIAL PRIMARY KEY,
  run_key TEXT UNIQUE NOT NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  scope TEXT NOT NULL,
  operator TEXT,
  toolchain TEXT[],
  status TEXT NOT NULL DEFAULT 'IN_PROGRESS'
    CHECK (status IN ('IN_PROGRESS','READY_FOR_REVIEW','APPROVED','COMPLETE','BLOCKED','SUPERSEDED')),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS leap_roi.claims (
  claim_id BIGSERIAL PRIMARY KEY,
  external_job_id TEXT,
  job_name TEXT,
  insured_name TEXT,
  property_address TEXT,
  carrier TEXT,
  claim_number TEXT,
  policy_number TEXT,
  pipeline_stage TEXT,
  division TEXT,
  work_type TEXT,
  category TEXT,
  baseline_rcv NUMERIC(14,2),
  baseline_acv NUMERIC(14,2),
  baseline_depreciation NUMERIC(14,2),
  baseline_deductible NUMERIC(14,2),
  baseline_net_claim NUMERIC(14,2),
  current_rcv NUMERIC(14,2),
  current_acv NUMERIC(14,2),
  current_depreciation NUMERIC(14,2),
  current_net_claim NUMERIC(14,2),
  approved_supplement_total NUMERIC(14,2),
  pending_supplement_total NUMERIC(14,2),
  upgrade_total NUMERIC(14,2),
  financial_status TEXT NOT NULL DEFAULT 'MISSING'
    CHECK (financial_status IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','CARRIER-ASSERTED','ESTIMATED','MODELED','INFERRED','CONFLICTED','MISSING','NOT-APPLICABLE')),
  source_last_verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_leap_roi_claims_job ON leap_roi.claims(external_job_id);
CREATE INDEX IF NOT EXISTS idx_leap_roi_claims_claim_number ON leap_roi.claims(claim_number);
CREATE INDEX IF NOT EXISTS idx_leap_roi_claims_stage ON leap_roi.claims(pipeline_stage);

CREATE TABLE IF NOT EXISTS leap_roi.source_artifacts (
  artifact_id BIGSERIAL PRIMARY KEY,
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  artifact_type TEXT NOT NULL,
  title TEXT NOT NULL,
  source_system TEXT,
  source_locator TEXT,
  document_date DATE,
  content_hash TEXT,
  verification_status TEXT NOT NULL
    CHECK (verification_status IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','CARRIER-ASSERTED','ESTIMATED','MODELED','INFERRED','CONFLICTED','MISSING','NOT-APPLICABLE')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS leap_roi.field_requirements (
  field_key TEXT PRIMARY KEY,
  section TEXT NOT NULL,
  field_label TEXT NOT NULL,
  importance TEXT NOT NULL DEFAULT 'STANDARD'
    CHECK (importance IN ('CRITICAL','HIGH','STANDARD','OPTIONAL')),
  required_when TEXT,
  authoritative_sources TEXT[],
  financial_relevance BOOLEAN NOT NULL DEFAULT false,
  time_relevance BOOLEAN NOT NULL DEFAULT false,
  active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS leap_roi.field_audits (
  field_audit_id BIGSERIAL PRIMARY KEY,
  audit_run_id BIGINT REFERENCES leap_roi.audit_runs(audit_run_id),
  claim_id BIGINT NOT NULL REFERENCES leap_roi.claims(claim_id),
  field_key TEXT NOT NULL REFERENCES leap_roi.field_requirements(field_key),
  prior_value TEXT,
  current_value TEXT,
  prior_state TEXT,
  current_state TEXT NOT NULL
    CHECK (current_state IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','CARRIER-ASSERTED','ESTIMATED','MODELED','INFERRED','CONFLICTED','MISSING','NOT-APPLICABLE')),
  source_artifact_id BIGINT REFERENCES leap_roi.source_artifacts(artifact_id),
  discovered_by TEXT,
  discovery_method TEXT,
  confidence NUMERIC(5,2) CHECK (confidence BETWEEN 0 AND 100),
  downstream_updates TEXT[],
  minutes_manual_baseline NUMERIC(10,2),
  minutes_actual NUMERIC(10,2),
  notes TEXT,
  audited_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_field_audits_claim ON leap_roi.field_audits(claim_id);
CREATE INDEX IF NOT EXISTS idx_field_audits_key ON leap_roi.field_audits(field_key);
CREATE INDEX IF NOT EXISTS idx_field_audits_state ON leap_roi.field_audits(current_state);

CREATE TABLE IF NOT EXISTS leap_roi.work_events (
  work_event_id BIGSERIAL PRIMARY KEY,
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  audit_run_id BIGINT REFERENCES leap_roi.audit_runs(audit_run_id),
  event_type TEXT NOT NULL,
  description TEXT NOT NULL,
  actor TEXT,
  automation_level TEXT NOT NULL DEFAULT 'MANUAL'
    CHECK (automation_level IN ('MANUAL','ASSISTED','MOSTLY_AUTOMATED','AUTOMATED')),
  manual_baseline_minutes NUMERIC(10,2),
  actual_minutes NUMERIC(10,2),
  baseline_basis TEXT,
  verification_status TEXT NOT NULL DEFAULT 'ESTIMATED'
    CHECK (verification_status IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','ESTIMATED','MODELED','INFERRED','CONFLICTED')),
  event_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS leap_roi.financial_events (
  financial_event_id BIGSERIAL PRIMARY KEY,
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  audit_run_id BIGINT REFERENCES leap_roi.audit_runs(audit_run_id),
  impact_type TEXT NOT NULL
    CHECK (impact_type IN (
      'DOCUMENTED_SCOPE_RECOVERY',
      'SUPPLEMENT_VALUE',
      'DEPRECIATION_RECOVERY',
      'REWORK_COST_AVOIDANCE',
      'ERROR_COST_AVOIDANCE',
      'DELAY_COST_AVOIDANCE',
      'COLLECTION_ACCELERATION',
      'ADMIN_LABOR_SAVINGS',
      'MISSED_FIELD_RISK',
      'OTHER_VERIFIED_VALUE'
    )),
  amount NUMERIC(14,2) NOT NULL,
  realization_state TEXT NOT NULL
    CHECK (realization_state IN ('VERIFIED_REALIZED','VERIFIED_IDENTIFIED','MODELED_OPPORTUNITY')),
  calculation_basis TEXT NOT NULL,
  source_artifact_id BIGINT REFERENCES leap_roi.source_artifacts(artifact_id),
  attribution TEXT NOT NULL DEFAULT 'NOT-ATTRIBUTED'
    CHECK (attribution IN ('DIRECT','SHARED','ENABLED','NOT-ATTRIBUTED')),
  attribution_notes TEXT,
  verification_status TEXT NOT NULL
    CHECK (verification_status IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','ESTIMATED','MODELED','INFERRED','CONFLICTED')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_financial_events_claim ON leap_roi.financial_events(claim_id);
CREATE INDEX IF NOT EXISTS idx_financial_events_type ON leap_roi.financial_events(impact_type);
CREATE INDEX IF NOT EXISTS idx_financial_events_realization ON leap_roi.financial_events(realization_state);

CREATE TABLE IF NOT EXISTS leap_roi.recommendations (
  recommendation_id BIGSERIAL PRIMARY KEY,
  audit_run_id BIGINT REFERENCES leap_roi.audit_runs(audit_run_id),
  claim_id BIGINT REFERENCES leap_roi.claims(claim_id),
  category TEXT NOT NULL,
  recommendation TEXT NOT NULL,
  expected_effect TEXT,
  priority TEXT NOT NULL DEFAULT 'P2'
    CHECK (priority IN ('P0','P1','P2','P3')),
  status TEXT NOT NULL DEFAULT 'OPEN'
    CHECK (status IN ('OPEN','APPROVED','IN_PROGRESS','DONE','REJECTED','BLOCKED','SUPERSEDED')),
  owner TEXT,
  evidence_basis TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS leap_roi.assumptions (
  assumption_key TEXT PRIMARY KEY,
  value_numeric NUMERIC,
  value_text TEXT,
  unit TEXT,
  source TEXT,
  status TEXT NOT NULL DEFAULT 'ESTIMATED'
    CHECK (status IN ('VERIFIED','SOURCE-CONFIRMED','USER-REPORTED','ESTIMATED','MODELED','CONFLICTED')),
  effective_date DATE,
  notes TEXT
);

INSERT INTO leap_roi.field_requirements
(field_key, section, field_label, importance, authoritative_sources, financial_relevance, time_relevance)
VALUES
('policy_number','insurance','Policy number','CRITICAL',ARRAY['policy declarations','carrier correspondence'],false,true),
('insured_email','contact','Insured/customer email','HIGH',ARRAY['intake','email','CRM'],false,true),
('carrier_fax','carrier','Carrier fax','STANDARD',ARRAY['carrier letter','contact sheet'],false,true),
('adjuster_phone','adjuster','Adjuster phone','HIGH',ARRAY['carrier letter','email signature','estimate'],false,true),
('acv','financial','Actual Cash Value','CRITICAL',ARRAY['carrier estimate','settlement letter'],true,true),
('deductible','financial','Deductible','CRITICAL',ARRAY['policy declarations','carrier estimate'],true,true),
('net_claim','financial','Net claim','CRITICAL',ARRAY['carrier estimate','settlement letter'],true,true),
('depreciation','financial','Depreciation','CRITICAL',ARRAY['carrier estimate'],true,true),
('rcv','financial','Replacement Cost Value','CRITICAL',ARRAY['carrier estimate'],true,true),
('upgrade_total','financial','Upgrade total','HIGH',ARRAY['estimate','supplement'],true,true),
('supplement_total','financial','Supplement total','HIGH',ARRAY['supplement','carrier approval'],true,true),
('work_type','operations','Work type','STANDARD',ARRAY['Leap'],false,true),
('category','operations','Category','STANDARD',ARRAY['Leap'],false,true),
('job_duration','operations','Job duration','HIGH',ARRAY['Leap timestamps'],false,true),
('job_id','operations','Job ID','CRITICAL',ARRAY['Leap'],false,true),
('job_name','operations','Job name','HIGH',ARRAY['Leap'],false,true),
('lead_name','operations','Lead name','STANDARD',ARRAY['Leap'],false,true),
('job_title','operations','Job title','STANDARD',ARRAY['Leap'],false,true),
('division','operations','Division','HIGH',ARRAY['Leap'],true,true),
('tasks','operations','Tasks / next actions','HIGH',ARRAY['Leap'],false,true),
('photos_files','evidence','Photos and files linked','CRITICAL',ARRAY['Leap','Drive','evidence store'],true,true),
('claim_notes','notes','Claim notes','CRITICAL',ARRAY['Leap','thread notes','Drive'],true,true)
ON CONFLICT (field_key) DO NOTHING;

CREATE OR REPLACE VIEW leap_roi.v_time_savings AS
SELECT
  claim_id,
  count(*) AS work_event_count,
  sum(COALESCE(manual_baseline_minutes,0)) AS baseline_minutes,
  sum(COALESCE(actual_minutes,0)) AS actual_minutes,
  sum(GREATEST(COALESCE(manual_baseline_minutes,0)-COALESCE(actual_minutes,0),0)) AS minutes_saved
FROM leap_roi.work_events
GROUP BY claim_id;

CREATE OR REPLACE VIEW leap_roi.v_financial_summary AS
SELECT
  claim_id,
  sum(amount) FILTER (WHERE realization_state='VERIFIED_REALIZED') AS verified_realized,
  sum(amount) FILTER (WHERE realization_state='VERIFIED_IDENTIFIED') AS verified_identified,
  sum(amount) FILTER (WHERE realization_state='MODELED_OPPORTUNITY') AS modeled_opportunity,
  sum(amount) FILTER (WHERE attribution='DIRECT' AND realization_state<>'MODELED_OPPORTUNITY') AS directly_attributed_verified_value,
  sum(amount) FILTER (WHERE attribution='SHARED' AND realization_state<>'MODELED_OPPORTUNITY') AS shared_verified_value
FROM leap_roi.financial_events
GROUP BY claim_id;

CREATE OR REPLACE VIEW leap_roi.v_claim_completeness AS
SELECT
  c.claim_id,
  c.external_job_id,
  c.job_name,
  count(fr.field_key) FILTER (WHERE fr.active) AS required_fields,
  count(fa.field_audit_id) FILTER (WHERE fa.current_state IN ('VERIFIED','SOURCE-CONFIRMED')) AS verified_fields,
  count(fa.field_audit_id) FILTER (WHERE fa.current_state='MISSING') AS missing_fields,
  count(fa.field_audit_id) FILTER (WHERE fa.current_state='CONFLICTED') AS conflicted_fields
FROM leap_roi.claims c
CROSS JOIN leap_roi.field_requirements fr
LEFT JOIN leap_roi.field_audits fa
  ON fa.claim_id=c.claim_id AND fa.field_key=fr.field_key
GROUP BY c.claim_id, c.external_job_id, c.job_name;

CREATE OR REPLACE VIEW leap_roi.v_owner_summary AS
SELECT
  c.claim_id,
  c.external_job_id,
  c.job_name,
  cc.required_fields,
  cc.verified_fields,
  cc.missing_fields,
  cc.conflicted_fields,
  ts.minutes_saved,
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
