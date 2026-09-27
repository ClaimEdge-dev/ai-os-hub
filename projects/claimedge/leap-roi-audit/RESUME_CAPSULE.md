# Resume Capsule — Leap ROI / Neon
Updated: 2026-09-27
State: BLOCKED / READY TO RESUME

## Foreground objective
Validate and prepare the Leap ROI audit system against the real `claimedge-prod` Neon project without modifying production.

## Last verified completion
- Canonical v1 + v2 migrations execute on clean PostgreSQL 16.
- Validation pack passes.
- Synthetic fixture passes.
- Fixture rollback is proven.
- Canonical views exist.
- Fresh-head GitHub Actions validation passed.

## Current blocker
Neon connector authorization fails for project `snowy-block-04251510` before DB access.

Opera fallback is also unavailable because Browser Connector is not connected.

## Exact resume action
Immediately retry:
1. Neon describe project
2. Neon list branches
3. Neon get `neondb` tables

If those succeed:
4. inspect existing schemas/tables/views read-only;
5. identify overlap/conflicts;
6. prepare a temporary migration branch;
7. run v1 + v2 there;
8. run validation + rollback fixture;
9. compare temp schema to parent;
10. stop at explicit production-apply approval.

## Do not redo
- do not redesign schema from scratch;
- do not recreate PR;
- do not create another project brain;
- do not recreate validation pack;
- do not recreate test fixture;
- do not rerun public Leap research unless a current fact needs re-verification.

## Waiting after Neon
- Leap API token/configuration
- first live reconciliation
- first verified field baseline
- first measured time baseline
- first owner snapshot
