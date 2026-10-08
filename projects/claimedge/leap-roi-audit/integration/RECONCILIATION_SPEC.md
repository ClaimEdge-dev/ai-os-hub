# Leap Sync / Reconciliation Specification

## Purpose

Webhooks tell us what changed. Reconciliation proves nothing was missed.

## Recommended cadence

- webhook-driven for near-real-time events
- daily read-only reconciliation of active jobs
- on-demand reconciliation before an owner report

## Reconciliation loop

1. Fetch active Leap jobs in pages.
2. Include customer/address resources where supported.
3. Match to Neon by:
   - Leap job ID first
   - job number second
   - claim number / address only as review candidates
4. Never auto-merge ambiguous jobs.
5. Compare critical field set.
6. Add field-audit rows for differences.
7. Preserve prior values.
8. Apply source precedence.
9. Flag conflicts.
10. Recompute owner-summary views.

## Source precedence examples

Policy number:
1. policy/declarations
2. carrier correspondence
3. Leap populated value
4. user report

Carrier financials:
1. newest carrier estimate/settlement
2. approved supplement documentation
3. Leap populated value
4. user report

Operational stage:
1. current Leap state
2. historical webhook event log

## Idempotency

Every API import must be rerunnable without duplicating:
- work events
- field-audit events
- financial events
- webhook events

Use provider IDs or deterministic hashes where available.

## Failure handling

- 401/403: stop sync and flag AUTH_BLOCKED
- 429: exponential backoff
- 5xx: retry with bounded attempts
- ambiguous identity: REVIEW_REQUIRED
- conflicting financial values: CONFLICTED, never silent overwrite
