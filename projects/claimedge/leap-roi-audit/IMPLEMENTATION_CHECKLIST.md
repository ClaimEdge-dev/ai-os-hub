# Implementation Checklist

## Already built

- [x] GitHub feature branch
- [x] Draft PR
- [x] Master audit prompt
- [x] Initial Leap gap register
- [x] Owner presentation specification
- [x] Neon v1 schema proposal
- [x] Leap integration architecture
- [x] Reconciliation specification
- [x] Webhook normalization reference
- [x] Neon v2 event/sync/history schema
- [x] Read-only validation pack
- [x] Temporary-branch test plan
- [x] Deterministic webhook dedupe
- [x] Latest-field completeness correction
- [x] OPTIONAL / NOT-APPLICABLE denominator controls
- [x] Verified / estimated / modeled time separation
- [x] Strong-evidence gate for verified financial totals
- [x] Stage timing-basis disclosure
- [x] Rollback-safe self-checking synthetic fixture
- [x] GitHub PostgreSQL 16 CI validation
- [x] Canonical migrations execute successfully on clean PostgreSQL 16
- [x] Validation pack executes successfully in CI
- [x] Synthetic fixture passes and proves full rollback in CI
- [x] Cross-thread DEBO recovery/reconciliation
- [x] DEBO v3.2 inheritance contract
- [x] Task Delta register
- [x] Resume Capsule / exact return point
- [x] Branch decision: stay in existing Leap/Neon ROI lane
- [x] No-DEBO-v4 / no-duplicate-master guard

## Blocked by access

- [ ] Neon read-only project inspection
- [ ] Existing-schema overlap check
- [ ] Temporary migration branch
- [ ] Temporary-branch migration test
- [ ] Schema comparison against parent

Current blocker: Neon connector returns authorization/internal HTTP 404 before database access.

GitHub Actions checkpoint: `Leap ROI schema validation` run #1 passed on PostgreSQL 16, including both migrations, validation queries, rollback-safe fixture, rollback proof, and canonical-view existence checks.

## Requires Leap credential/configuration

- [ ] Obtain Leap API access token through the authorized account/admin path
- [ ] Store token as a secret/environment variable, never in GitHub
- [ ] Verify actual API resources and pagination for this account
- [ ] Register webhook endpoint
- [ ] Verify delivered event payload shapes
- [ ] Run first read-only reconciliation

## Production approval gate

These remain intentionally undone until explicit approval:

- [ ] Apply Neon migration to production
- [ ] Deploy production webhook receiver
- [ ] Turn on recurring reconciliation
- [ ] Merge PR to `main`
- [ ] Publish owner-facing KPI report

## First live baseline

After the connectors are working:

1. ingest active Leap jobs read-only;
2. build missing-field baseline;
3. record source freshness;
4. recover authoritative values from claim evidence;
5. capture manual-time baselines before automation changes them;
6. separate verified dollars from modeled opportunity;
7. separate measured time savings from estimated/modeled time;
8. generate the first owner snapshot;
9. preserve it for before/after comparison.
