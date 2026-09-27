-- Leap ROI read-only validation pack
-- Run on a TEMPORARY Neon branch after migration_v1.sql + migration_v2_event_history.sql.
-- Every statement is read-only. Any non-empty result set should be reviewed.

-- 1) Duplicate Leap job IDs. Do not auto-merge these.
SELECT external_job_id, count(*) AS record_count
FROM leap_roi.claims
WHERE external_job_id IS NOT NULL
GROUP BY external_job_id
HAVING count(*) > 1
ORDER BY record_count DESC, external_job_id;

-- 2) Claims with impossible or suspicious negative financial values.
SELECT claim_id, external_job_id, job_name,
       baseline_rcv, baseline_acv, baseline_depreciation, baseline_deductible, baseline_net_claim,
       current_rcv, current_acv, current_depreciation, current_net_claim,
       approved_supplement_total, pending_supplement_total, upgrade_total
FROM leap_roi.claims
WHERE COALESCE(baseline_rcv,0) < 0
   OR COALESCE(baseline_acv,0) < 0
   OR COALESCE(baseline_depreciation,0) < 0
   OR COALESCE(baseline_deductible,0) < 0
   OR COALESCE(current_rcv,0) < 0
   OR COALESCE(current_acv,0) < 0
   OR COALESCE(current_depreciation,0) < 0
   OR COALESCE(approved_supplement_total,0) < 0
   OR COALESCE(pending_supplement_total,0) < 0
   OR COALESCE(upgrade_total,0) < 0;

-- 3) Work events where actual time is negative or baseline is negative.
SELECT *
FROM leap_roi.work_events
WHERE COALESCE(manual_baseline_minutes,0) < 0
   OR COALESCE(actual_minutes,0) < 0;

-- 4) Financial events with modeled realization but stronger-than-modeled verification.
-- Not automatically wrong, but review the calculation basis.
SELECT *
FROM leap_roi.financial_events
WHERE realization_state='MODELED_OPPORTUNITY'
  AND verification_status IN ('VERIFIED','SOURCE-CONFIRMED');

-- 5) Direct attribution with no attribution notes.
SELECT *
FROM leap_roi.financial_events
WHERE attribution='DIRECT'
  AND NULLIF(btrim(attribution_notes),'') IS NULL;

-- 6) Webhooks that failed, need retry, or require human review.
SELECT webhook_event_id, event_key, event_type, external_job_id,
       processing_status, retry_count, last_error, received_at
FROM leap_roi.webhook_events
WHERE processing_status IN ('FAILED','RETRY','REVIEW_REQUIRED')
ORDER BY received_at DESC;

-- 7) Stage events that move backward in time for the same claim/job.
WITH x AS (
  SELECT
    stage_event_id,
    claim_id,
    external_job_id,
    event_at,
    lag(event_at) OVER (
      PARTITION BY CASE
        WHEN claim_id IS NOT NULL THEN 'claim:' || claim_id::text
        ELSE 'job:' || external_job_id
      END
      ORDER BY stage_event_id
    ) AS prior_event_at
  FROM leap_roi.stage_events
)
SELECT *
FROM x
WHERE prior_event_at IS NOT NULL
  AND event_at < prior_event_at;

-- 8) Completeness sanity check: verified + missing + conflicted must not exceed required.
SELECT *
FROM leap_roi.v_claim_completeness
WHERE verified_fields + missing_fields + conflicted_fields > required_fields;

-- 9) Owner summary should never mix modeled opportunity into verified columns.
SELECT *
FROM leap_roi.v_owner_summary
WHERE COALESCE(verified_realized,0) < 0
   OR COALESCE(verified_identified,0) < 0
   OR COALESCE(modeled_opportunity,0) < 0;

-- 10) Freshness check.
SELECT * FROM leap_roi.v_sync_health;
