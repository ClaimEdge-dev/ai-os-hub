# DEBO Reconciliation — Leap / Neon / ROI Audit
Date: 2026-09-27
Status: ACTIVE / RECOVERED / NOT PRODUCTION

## 1. Branch decision

**STAY IN CURRENT PROJECT LANE.**

This work belongs inside the existing ClaimEdge Leap/Neon ROI lane. Do not create another master DEBO brain, another Leap project, or another ROI ledger.

Current durable code branch:
`feature/leap-roi-audit-v1`

Current PR:
`#6 — Draft: Leap ROI + Claim Completeness Audit v1`

Future deployment work may branch technically inside GitHub, but project truth must merge back here.

## 2. Canonical DEBO inheritance

This project inherits the current DEBO stack:

1. Bobby = final human authority.
2. DEBO Constitution / Master Control v1.0 = architectural parent.
3. DEBO Orchestrator OS + v3.2 = current runtime/control layer.
4. `skills/robert-master-os/SKILL.md` = session/portfolio orchestrator implementation.
5. `docs/DEBO_FERRARI_BRAIN_EXECUTION_LAYER.md` = interruption, resume, NOW-3, Definition-of-Done, propagation, research, and self-audit behavior.
6. ClaimEdge = domain brain.
7. Leap ROI Audit = child project brain.
8. GitHub feature branch / PR = active implementation lane.

**Do not create DEBO v4.** New behavior patches v3.2 unless Bobby explicitly approves a new major architecture.

## 3. Recovered from this thread

### Built and verified
- GitHub feature branch created.
- Draft PR #6 created and maintained.
- Leap missing-field register created.
- DEBO Leap ROI master prompt created.
- Owner KPI / presentation specification created.
- Base Neon schema migration created.
- Canonical hardening migration created.
- Competing hardening migration detected, archived, and superseded.
- Webhook event ledger added.
- Sync/reconciliation run ledger added.
- Reconciliation findings added.
- Stage/cycle-time history added.
- Owner snapshots added.
- Event idempotency added.
- Latest-field completeness logic added.
- Optional / NOT-APPLICABLE denominator controls added.
- Verified / estimated / modeled time savings separated.
- Verified financial totals gated by strong evidence.
- Deterministic webhook normalization reference added.
- Reconciliation specification added.
- Rollback-safe synthetic fixture added.
- PostgreSQL 16 GitHub Actions validation added.
- CI run #1 passed.
- Fresh-head CI run #2 passed.
- Production writes remain intentionally untouched.

### Access blockers discovered
- Neon connector is installed but authorization for project `snowy-block-04251510` fails before database access with HTTP 404.
- Opera Browser Connector fallback is not connected.
- Leap API credential is not yet configured in the integration runtime.

## 4. Started but not finished

### P0 — blocked
1. Read-only inspect live Neon `claimedge-prod / neondb`.
2. Inspect existing `claimedge_os` and any overlapping ROI/audit objects.
3. Create temporary Neon branch.
4. Run canonical v1 + v2 migrations on that temporary branch.
5. Run validation pack and rollback fixture there.
6. Compare temp schema against parent.
7. Human approval before production migration.

### P1 — Leap live integration
1. Obtain authorized Leap API token through account/admin flow.
2. Verify live endpoints, pagination, field names, and webhook payloads against the actual account.
3. Deploy webhook receiver only after credentials and production destination are approved.
4. Run first read-only reconciliation.
5. Build first verified missing-field baseline.
6. Capture real manual-time baseline before automation changes workflow.
7. Produce first owner snapshot.

### P1 — reporting
1. Generate owner-facing baseline report from live data.
2. Separate VERIFIED_REALIZED / VERIFIED_IDENTIFIED / MODELED_OPPORTUNITY.
3. Separate DIRECT / SHARED / ENABLED attribution.
4. Preserve baseline snapshot for future before/after comparisons.

## 5. DEBO runtime gaps discovered

The project-specific master prompt was missing explicit inheritance for several current DEBO controls. These are now required:

- recover before create
- similarity / duplicate scan
- automatic branch check
- Definition-of-Done compiler
- one foreground objective + at most two safe background lanes
- Task Delta tracking
- lifecycle state on durable artifacts/tasks
- evidence promotion path
- autonomic event observer
- initiative governor
- change-propagation scan
- workspace/thread steward
- resume stack / checkpoint
- self-audit
- research-before-canonizing for substantial architecture work
- safe internal autonomy + approval firewall
- no major-version rebuild merely because a new idea appears

## 6. Lifecycle state

| Object | State |
|---|---|
| Leap ROI project | ACTIVE |
| GitHub implementation | ACTIVE |
| PR #6 | READY_FOR_REVIEW / DRAFT |
| PostgreSQL CI | VERIFIED |
| Neon live validation | BLOCKED |
| Leap live API connection | BLOCKED |
| Production migration | APPROVAL_REQUIRED |
| Webhook deployment | APPROVAL_REQUIRED |
| Owner baseline | WAITING_ON_LIVE_DATA |
| Superseded hardening migration | ARCHIVED / SUPERSEDED |

## 7. Promotion path

Project facts remain local.

Promote to DEBO Global only:
- reusable connector behavior;
- reusable database-migration safety patterns;
- reusable project/thread recovery rules;
- reusable approval/supersession/CI rules.

Do not promote:
- Leap job facts;
- claim-specific financials;
- carrier values;
- customer/insured data;
- project-specific field mappings.

## 8. Hands-free execution policy

When Bobby says `go`, `do it`, `keep going`, or `finish`:

1. recover latest checkpoint;
2. preserve foreground return point;
3. execute safe reversible internal work;
4. do not re-ask known facts;
5. do not rebuild existing structures;
6. stop only at a real blocker or approval boundary;
7. update durable state before reporting back.

External send/publish/spend/production database change/destructive action remains approval-gated.

## 9. Current NOW-3

1. **WAITING:** restore live Neon authorization.
2. **READY:** perform live read-only schema overlap audit immediately when Neon becomes available.
3. **READY:** proceed to temporary Neon validation branch, then stop at production-apply approval.

Everything else stays queued and must not hijack those three.
