-- TEMPORARY BRANCH ONLY
-- Self-checking Leap ROI fixture. Runs inside one transaction and ROLLS BACK.
-- Expected result: no exception, followed by ROLLBACK.
-- Requires migration_v1.sql and migration_v2_event_history.sql first.

BEGIN;

DO $$
DECLARE
  v_claim_id BIGINT;
  v_audit_run_id BIGINT;
  v_sync_run_id BIGINT;
  v_count INTEGER;
  v_state TEXT;
  v_verified NUMERIC;
  v_modeled NUMERIC;
  v_closed_duration NUMERIC;
  v_open_exit TIMESTAMPTZ;
BEGIN
  INSERT INTO leap_roi.audit_runs
    (run_key, scope, operator, status)
  VALUES
    ('TEST-FIXTURE-AUDIT-001', 'SYNTHETIC', 'DEBO_TEST', 'IN_PROGRESS')
  RETURNING audit_run_id INTO v_audit_run_id;

  INSERT INTO leap_roi.sync_runs
    (run_key, run_type, provider, status, source_as_of)
  VALUES
    ('TEST-FIXTURE-SYNC-001', 'VALIDATION', 'LEAP', 'IN_PROGRESS', now())
  RETURNING sync_run_id INTO v_sync_run_id;

  INSERT INTO leap_roi.claims
    (external_job_id, job_name, insured_name, pipeline_stage,
     baseline_rcv, current_rcv, financial_status)
  VALUES
    ('TEST-LEAP-JOB-001', 'Synthetic Validation Claim', 'Synthetic Insured',
     'Appointment', 10000.00, 11250.00, 'VERIFIED')
  RETURNING claim_id INTO v_claim_id;

  -- Same field audited three times. Latest view must count it once and use VERIFIED.
  INSERT INTO leap_roi.field_audits
    (audit_run_id, claim_id, field_key, current_state, event_key, audited_at)
  VALUES
    (v_audit_run_id, v_claim_id, 'policy_number', 'MISSING',
     'TEST:FIELD:POLICY:1', now() - interval '3 minutes'),
    (v_audit_run_id, v_claim_id, 'policy_number', 'USER-REPORTED',
     'TEST:FIELD:POLICY:2', now() - interval '2 minutes'),
    (v_audit_run_id, v_claim_id, 'policy_number', 'VERIFIED',
     'TEST:FIELD:POLICY:3', now() - interval '1 minute');

  SELECT count(*), max(current_state)
  INTO v_count, v_state
  FROM leap_roi.v_latest_field_audit
  WHERE claim_id=v_claim_id AND field_key='policy_number';

  IF v_count <> 1 OR v_state <> 'VERIFIED' THEN
    RAISE EXCEPTION 'Latest-field audit failed: count=%, state=%', v_count, v_state;
  END IF;

  -- Duplicate work event replay. ON CONFLICT DO NOTHING must leave one row.
  INSERT INTO leap_roi.work_events
    (claim_id, audit_run_id, event_type, description, automation_level,
     manual_baseline_minutes, actual_minutes, baseline_basis,
     verification_status, event_key)
  VALUES
    (v_claim_id, v_audit_run_id, 'CLAIM_AUDIT', 'Synthetic audit',
     'ASSISTED', 30, 10, 'synthetic timed baseline', 'VERIFIED',
     'TEST:WORK:001');

  INSERT INTO leap_roi.work_events
    (claim_id, audit_run_id, event_type, description, automation_level,
     manual_baseline_minutes, actual_minutes, baseline_basis,
     verification_status, event_key)
  VALUES
    (v_claim_id, v_audit_run_id, 'CLAIM_AUDIT', 'Synthetic duplicate replay',
     'ASSISTED', 30, 10, 'synthetic timed baseline', 'VERIFIED',
     'TEST:WORK:001')
  ON CONFLICT DO NOTHING;

  SELECT count(*) INTO v_count
  FROM leap_roi.work_events
  WHERE event_key='TEST:WORK:001';

  IF v_count <> 1 THEN
    RAISE EXCEPTION 'Work-event idempotency failed: count=%', v_count;
  END IF;

  -- Duplicate webhook delivery. Must remain one normalized event.
  INSERT INTO leap_roi.webhook_events
    (sync_run_id, claim_id, provider, event_key, action, operation,
     entity_type, external_job_id, stage_from, stage_to,
     event_occurred_at, processing_status, payload_hash)
  VALUES
    (v_sync_run_id, v_claim_id, 'LEAP', 'TEST:WEBHOOK:001',
     'jobs', 'stage_change', 'job', 'TEST-LEAP-JOB-001',
     'Lead', 'Appointment', now() - interval '60 minutes',
     'PROCESSED', 'synthetic-hash');

  INSERT INTO leap_roi.webhook_events
    (sync_run_id, claim_id, provider, event_key, action, operation,
     entity_type, external_job_id, stage_from, stage_to,
     event_occurred_at, processing_status, payload_hash)
  VALUES
    (v_sync_run_id, v_claim_id, 'LEAP', 'TEST:WEBHOOK:001',
     'jobs', 'stage_change', 'job', 'TEST-LEAP-JOB-001',
     'Lead', 'Appointment', now() - interval '60 minutes',
     'PROCESSED', 'synthetic-hash')
  ON CONFLICT DO NOTHING;

  SELECT count(*) INTO v_count
  FROM leap_roi.webhook_events
  WHERE event_key='TEST:WEBHOOK:001';

  IF v_count <> 1 THEN
    RAISE EXCEPTION 'Webhook idempotency failed: count=%', v_count;
  END IF;

  -- Two stage entries. First must have a duration; second is current/open.
  INSERT INTO leap_roi.stage_events
    (event_key, claim_id, external_job_id, from_stage, to_stage, event_at,
     verification_status)
  VALUES
    ('TEST:STAGE:001', v_claim_id, 'TEST-LEAP-JOB-001',
     'Lead', 'Appointment', now() - interval '60 minutes', 'SOURCE-CONFIRMED'),
    ('TEST:STAGE:002', v_claim_id, 'TEST-LEAP-JOB-001',
     'Appointment', 'Adjustment Estimate', now() - interval '30 minutes', 'SOURCE-CONFIRMED');

  SELECT minutes_in_stage
  INTO v_closed_duration
  FROM leap_roi.v_stage_durations
  WHERE claim_id=v_claim_id AND stage='Appointment';

  IF v_closed_duration IS NULL OR v_closed_duration < 29 OR v_closed_duration > 31 THEN
    RAISE EXCEPTION 'Closed stage duration failed: %', v_closed_duration;
  END IF;

  SELECT exited_at
  INTO v_open_exit
  FROM leap_roi.v_stage_durations
  WHERE claim_id=v_claim_id AND stage='Adjustment Estimate';

  IF v_open_exit IS NOT NULL THEN
    RAISE EXCEPTION 'Open stage should have NULL exited_at, got %', v_open_exit;
  END IF;

  -- Keep verified and modeled dollars separate.
  INSERT INTO leap_roi.financial_events
    (claim_id, audit_run_id, impact_type, amount, realization_state,
     calculation_basis, attribution, attribution_notes,
     verification_status, event_key)
  VALUES
    (v_claim_id, v_audit_run_id, 'DOCUMENTED_SCOPE_RECOVERY', 500.00,
     'VERIFIED_REALIZED', 'synthetic carrier-supported delta',
     'SHARED', 'synthetic shared attribution', 'VERIFIED',
     'TEST:FIN:VERIFIED'),
    (v_claim_id, v_audit_run_id, 'MISSED_FIELD_RISK', 900.00,
     'MODELED_OPPORTUNITY', 'synthetic modeled risk only',
     'NOT-ATTRIBUTED', 'synthetic model', 'MODELED',
     'TEST:FIN:MODELED');

  SELECT
    COALESCE(verified_realized,0),
    COALESCE(modeled_opportunity,0)
  INTO v_verified, v_modeled
  FROM leap_roi.v_financial_summary
  WHERE claim_id=v_claim_id;

  IF v_verified <> 500.00 OR v_modeled <> 900.00 THEN
    RAISE EXCEPTION 'Financial separation failed: verified=%, modeled=%',
      v_verified, v_modeled;
  END IF;

  -- Completeness must not count the three policy audits as three verified fields.
  SELECT verified_fields INTO v_count
  FROM leap_roi.v_claim_completeness
  WHERE claim_id=v_claim_id;

  IF v_count <> 1 THEN
    RAISE EXCEPTION 'Completeness overcount detected: verified_fields=%', v_count;
  END IF;

  UPDATE leap_roi.audit_runs
  SET status='COMPLETE', completed_at=now()
  WHERE audit_run_id=v_audit_run_id;

  UPDATE leap_roi.sync_runs
  SET status='COMPLETE', completed_at=now(), records_seen=1, records_inserted=1
  WHERE sync_run_id=v_sync_run_id;

  RAISE NOTICE 'Leap ROI temporary fixture passed all assertions.';
END $$;

ROLLBACK;
