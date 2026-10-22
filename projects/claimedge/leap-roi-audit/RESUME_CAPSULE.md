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

**Confirmed ChatGPT plugin-state inconsistency**
- Plugin directory says Neon is installed/enabled.
- Permission service says the same Neon app ID is not installed.
- Neon API calls fail authorization with HTTP 404.

Treat Neon as CONNECTION_BROKEN until re-authorized in ChatGPT.


Neon connector authorization still fails for project `snowy-block-04251510` before DB access.

Opera fallback partially recovered:
- browser connector briefly connected;
- signed-in Neon account label observed as `bobby.huuso`;
- target project URL `snowy-block-04251510` opened successfully;
- connector disconnected again before schema content could be inspected.

Therefore live schema inspection remains incomplete.

## Exact resume action
Immediately retry BOTH lanes:

Neon connector:
1. describe project
2. list branches
3. get `neondb` tables

Opera fallback:
1. reconnect Browser Connector;
2. reopen/read target Neon tab for `snowy-block-04251510`;
3. confirm project identity + branch/database/schema content.

When either lane confirms live read access:
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
