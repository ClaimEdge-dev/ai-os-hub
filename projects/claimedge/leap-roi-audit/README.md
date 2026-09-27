# Leap ROI + Claim Completeness Audit

Status: DRAFT / BRANCH-ONLY
Branch: `feature/leap-roi-audit-v1`
Canonical Neon target: `claimedge-prod`
Neon project ID: `snowy-block-04251510`
Database: `neondb`
Planned schema: `leap_roi`

## Mission

Create a defensible, continuously updated audit trail showing:

1. what information was missing or incomplete in Leap before cleanup;
2. what source supplied each corrected field;
3. how much manual time the improved workflow avoids;
4. how much documented financial value the workflow protects, recovers, accelerates, or prevents from leaking;
5. what claim-scope or supplement value was supported by newly organized evidence;
6. what portion of the result is VERIFIED versus ESTIMATED or MODELED;
7. which improvements are attributable to Bobby's process, automation, research, field documentation, or QA;
8. what remains unresolved.

This is an owner-facing value system, not a vanity counter.

## Core rule

Never equate a larger claim with a better claim. The financial objective is complete, accurate, well-supported scope and faster, cleaner operations. Do not inflate, duplicate, invent, or count unsupported claim value.

## Current known Leap gaps to verify

User-reported current missing/underbuilt insurance fields include:

- policy number
- insured/customer email
- carrier fax
- adjuster phone
- ACV
- deductible
- net claim
- depreciation
- RCV
- upgrade totals
- supplement totals

Operational fields being built/reviewed include:

- lead/stage
- adjustment estimate
- appointment
- adjustment complete
- follow-up
- contract scheduled
- build
- work type
- category
- job duration
- job ID
- job name
- lead name
- job title
- division
- tasks
- photos/files
- claim notes

All of the above start as USER-REPORTED until verified against Leap, carrier documents, policy, estimate, notes, Drive, CompanyCam-equivalent evidence, or another authoritative source.

## Architecture

### GitHub
Stores the system definition, prompt, migration SQL, KPI formulas, data dictionary, and change history.

### Neon
Stores live structured audit events, missing fields, sources, work events, time-savings events, financial-impact events, recommendations, and presentation snapshots.

### Leap
Operational CRM/source of job and claim-state fields. Do not treat a Leap field as verified merely because it is populated.

### Drive / claim files
Primary evidence source for carrier estimates, policy/declarations, correspondence, field notes, reports, invoices, photos, videos, and other claim documents.

## Truth states

Use these statuses everywhere:

- VERIFIED
- SOURCE-CONFIRMED
- USER-REPORTED
- CARRIER-ASSERTED
- ESTIMATED
- MODELED
- INFERRED
- CONFLICTED
- MISSING
- NOT-APPLICABLE

Never silently promote ESTIMATED, MODELED, or INFERRED to VERIFIED.

## ROI classes

Time:
- MANUAL_BASELINE
- ACTUAL_CURRENT
- AUTOMATED
- REWORK_AVOIDED
- SEARCH_TIME_AVOIDED
- FOLLOWUP_TIME_AVOIDED

Financial:
- DOCUMENTED_SCOPE_RECOVERY
- SUPPLEMENT_VALUE
- DEPRECIATION_RECOVERY
- REWORK_COST_AVOIDANCE
- ERROR_COST_AVOIDANCE
- DELAY_COST_AVOIDANCE
- COLLECTION_ACCELERATION
- ADMIN_LABOR_SAVINGS
- MISSED_FIELD_RISK
- OTHER_VERIFIED_VALUE

Every financial event must include its calculation basis and evidence status.

## Attribution

Bobby's contribution is tracked separately from total company outcome.

Allowed attribution bases include:
- direct data recovery
- field/evidence collection
- claim audit
- missing-field correction
- estimate/scope QA
- supplement support
- workflow automation
- CRM cleanup
- document organization
- owner/reporting system
- prevented rework
- prevented omission

Do not assign 100% credit simply because Bobby touched the claim. Record shared attribution where appropriate.

## Current blocker

The Neon connector can identify the project from GitHub recovery, but the current connection returned an authorization error for `snowy-block-04251510`. No production database write has been attempted. Apply the migration only after Neon access is authorized and the existing schema is read-only audited.

## Files

- `MASTER_PROMPT.md` — autonomous DEBO audit/orchestration prompt
- `INITIAL_GAPS_REGISTER.md` — first known missing/underbuilt fields
- `OWNER_PRESENTATION_SPEC.md` — owner-facing KPI and presentation design
- `neon/migration_v1.sql` — additive schema proposal for Neon

## Release gate

Before merging to main or applying to Neon:

1. read-only inspect `claimedge-prod`;
2. confirm no overlapping canonical tables already exist;
3. run migration on a temporary Neon branch;
4. test views and formulas;
5. verify duplicate/double-count controls;
6. human approval;
7. apply to production;
8. create first owner baseline snapshot.
