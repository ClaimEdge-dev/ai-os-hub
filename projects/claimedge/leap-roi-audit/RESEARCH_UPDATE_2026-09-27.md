# Research Update — 2026-09-27
State: VERIFIED / PROJECT REFERENCE

## Scope searched
- Neon official branching/schema-diff guidance
- GitHub Actions official PostgreSQL service-container guidance
- Leap / JobProgress official API documentation
- GitHub/community implementation discussion
- Reddit database-branching discussions
- video/social discovery searches

## Verified findings

### Neon
Official Neon guidance supports:
- isolated database branches for testing;
- branches carrying parent schema/data state at creation;
- migration testing on child branches;
- schema comparison between child and parent;
- API/automation support for schema diff;
- short-lived branch workflows around PRs/tests.

Project impact:
**No architecture change needed.**
Current plan already uses temporary branch → migration → validation → schema compare → approval → production.

### GitHub Actions
Official GitHub documentation supports PostgreSQL service containers on Linux runners with health checks and runner-to-service connectivity.

Project impact:
Current PostgreSQL 16 CI lane is aligned with official guidance.

### Leap / JobProgress API
Official API docs currently confirm:
- API throttling at 60 requests/minute;
- HTTP 429 when rate limit is exceeded;
- exponential backoff recommended;
- normal auth/not-found/server error classes documented.

Project impact:
Keep bounded retries, exponential backoff, and AUTH_BLOCKED / RATE_LIMITED / FAILED sync states.

## Community signals — not canonical by themselves
Recent developer discussions commonly favor:
- short-lived branch-per-feature / branch-per-test;
- treating migrations as code;
- fresh disposable databases for CI;
- avoiding long-lived divergent database branches;
- preserving production as the boring/canonical branch.

These support the current design but are not promoted without primary-source backing.

## Video / social result
No higher-authority finding surfaced that changes the verified architecture. Social/video material remains discovery-only.

## Rejected / not adopted
- no automatic production migration directly from GitHub CI;
- no long-lived test branch as canonical truth;
- no reliance on community claims for security/production behavior;
- no replacing Neon with another database merely because auth is temporarily blocked.

## Current conclusion
The project architecture remains:
clean PostgreSQL CI
→ live Neon read-only overlap audit
→ short-lived Neon temporary branch
→ migrate/test
→ schema diff
→ approval
→ production apply
→ verify.
