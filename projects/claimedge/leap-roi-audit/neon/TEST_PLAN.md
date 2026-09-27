# Temporary-Branch Test Plan

Status: REQUIRED BEFORE PRODUCTION APPLY

## Purpose

Prove the Leap ROI audit schema is additive, rerunnable, mathematically sane, and incapable of silently inflating completeness or financial value.

## Gate sequence

1. Read-only inspect `claimedge-prod / neondb`.
2. Confirm whether `leap_roi` or overlapping tables already exist.
3. Prepare a temporary Neon migration branch.
4. Apply `migration_v1.sql` then `migration_v2_event_history.sql` on the temporary branch only.
5. Run `validation_v1.sql`.
6. Insert synthetic test records on the temporary branch.
7. Re-run the same synthetic import using identical event keys.
8. Confirm no duplicate field, work, financial, webhook, or stage events are created.
9. Confirm a second field audit for the same claim + field replaces the first one in `v_latest_field_audit` without inflating completeness counts.
10. Confirm `VERIFIED_REALIZED`, `VERIFIED_IDENTIFIED`, and `MODELED_OPPORTUNITY` remain separate in `v_financial_summary`.
11. Confirm `v_stage_durations` calculates a closed stage duration and leaves the current/open stage with a null exit time.
12. Confirm an ambiguous claim/job match is routed to review rather than merged.
13. Confirm a failed/auth-blocked sync is visible in `v_sync_health`.
14. Produce one synthetic owner snapshot.
15. Compare temporary-branch schema against its parent.
16. Human review.
17. Only after explicit approval, complete the migration into production.

## Required synthetic cases

### Case A — clean claim
One Leap job, all critical fields present, two stage transitions, one verified time-saving event, one verified financial event.

Expected:
- no duplicates
- completeness math correct
- stage duration calculable
- financial value appears in the correct realization bucket

### Case B — repeated audit
Audit the same field three times:
1. MISSING
2. USER-REPORTED
3. VERIFIED

Expected:
- raw audit history contains all three events
- `v_latest_field_audit` returns only VERIFIED
- `v_claim_completeness` counts the field once

### Case C — duplicate webhook delivery
Submit the same `event_key` twice.

Expected:
- second insert conflicts/no-ops at the integration layer
- one `webhook_events` row remains

### Case D — modeled opportunity
Create a modeled financial opportunity.

Expected:
- it never appears inside verified-realized or verified-identified totals

### Case E — ambiguous identity
Two claims share a weak matching signal such as address text but have different Leap job IDs.

Expected:
- no automatic merge
- reconciliation status becomes REVIEW_REQUIRED

## Release blockers

Do not approve production migration if any of these remain:
- Neon connector authorization is unresolved
- overlapping canonical tables are discovered without reconciliation
- duplicate external job IDs are unexplained
- validation query returns an unreviewed issue
- idempotency test fails
- completeness view overcounts
- modeled dollars appear in verified totals
- migration cannot be discarded cleanly from the temporary branch
