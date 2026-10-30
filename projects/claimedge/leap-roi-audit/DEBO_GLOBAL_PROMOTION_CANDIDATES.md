# DEBO Global Promotion Candidates
Date: 2026-09-27
State: READY_FOR_REVIEW
Source project: ClaimEdge / Leap ROI Audit

These are reusable lessons discovered here that may belong in DEBO Core. They are **not automatically promoted to main/global governance from this project branch**.

## Candidate 1 — Database migration safety ladder
For durable database changes:
RECOVER SCHEMA → READ-ONLY OVERLAP AUDIT → CLEAN POSTGRES CI → TEMPORARY PROVIDER BRANCH → FIXTURE/ROLLBACK TEST → SCHEMA COMPARE → HUMAN APPROVAL → PRODUCTION APPLY → POST-APPLY VERIFY.

Why reusable:
This pattern applies beyond Neon/Leap.

## Candidate 2 — Parallel migration collision detector
If two branches/artifacts create the same table/view with different definitions:
- stop;
- preserve both originals;
- designate one canonical lineage;
- archive/supersede the other;
- write explicit migration order;
- validate the canonical chain in CI.

## Candidate 3 — Access blocker exhaustion rule
When a connector fails:
1. retry distinct read-only paths;
2. try an authorized alternate connector/browser path;
3. record exact error + searched scope;
4. continue safe offline/internal work;
5. create exact resume action;
6. do not repeatedly hammer the same failed route.

## Candidate 4 — CI before provider access
When live provider access is blocked but schema/code can be tested independently:
build a local/CI equivalent test lane instead of idling.

## Candidate 5 — Project inheritance over prompt duplication
Child project prompts should declare parent DEBO inheritance and specialize only local behavior. This reduces governance drift when DEBO Core changes.

## Candidate 6 — Fresh-head validation
A passing CI check is only authoritative for the commit it tested. After material branch changes, validate the new head before calling the branch verified.

## Promotion gate
Before global promotion:
- dedupe against `robert-master-os`, Ferrari layer, autonomous-ops-architect, and skill-lifecycle-manager;
- patch existing sections rather than create another orchestration skill;
- preserve supersession/version history;
- keep project-specific Neon/Leap facts out of DEBO Core.
