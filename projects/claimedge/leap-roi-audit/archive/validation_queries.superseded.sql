-- Temporary-branch validation checks for Leap ROI schema.
-- Run only after migration_v1.sql + migration_v1_1_hardening.sql on a Neon temporary branch.

-- 1) Required objects exist.
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'leap_roi'
ORDER BY table_name;

SELECT table_schema, table_name
FROM information_schema.views
WHERE table_schema = 'leap_roi'
ORDER BY table_name;

-- 2) Unique/idempotency indexes exist.
SELECT schemaname, tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'leap_roi'
  AND indexname IN (
    'uq_leap_roi_claims_external_job_id',
    'uq_leap_roi_field_audits_event_key',
    'uq_leap_roi_work_events_event_key',
    'uq_leap_roi_financial_events_event_key'
  )
ORDER BY indexname;

-- 3) The completeness view uses only the latest audit row per claim/field.
SELECT *
FROM leap_roi.v_latest_field_audits
LIMIT 25;

-- 4) Owner summary keeps verified, estimated, modeled, and attribution buckets separate.
SELECT *
FROM leap_roi.v_owner_summary
LIMIT 25;

-- 5) Constraint inventory.
SELECT
  tc.table_name,
  tc.constraint_name,
  tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.table_schema = 'leap_roi'
ORDER BY tc.table_name, tc.constraint_name;

-- 6) Orphan check: should return zero rows.
SELECT fa.field_audit_id
FROM leap_roi.field_audits fa
LEFT JOIN leap_roi.claims c ON c.claim_id = fa.claim_id
WHERE c.claim_id IS NULL;

-- 7) Financial realization integrity review.
-- Any rows returned here need review because they are labeled VERIFIED_* while the
-- underlying verification status is not VERIFIED or SOURCE-CONFIRMED.
SELECT financial_event_id, claim_id, realization_state, verification_status, amount
FROM leap_roi.financial_events
WHERE realization_state IN ('VERIFIED_REALIZED','VERIFIED_IDENTIFIED')
  AND verification_status NOT IN ('VERIFIED','SOURCE-CONFIRMED');

-- 8) Dedupe review. All counts should equal 1.
SELECT event_key, count(*)
FROM leap_roi.webhook_events
GROUP BY event_key
HAVING count(*) > 1;
