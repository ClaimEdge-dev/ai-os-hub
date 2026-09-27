# Task Delta Register — Leap ROI Audit

| ID | Task | State | Priority | Dependency | Next action |
|---|---|---|---|---|---|
| LRA-001 | Recover current thread/build | COMPLETE | P0 | none | preserve checkpoint |
| LRA-002 | Reconcile newest DEBO governance | COMPLETE | P0 | recovery | inherit DEBO Core |
| LRA-003 | Canonicalize Neon migrations | COMPLETE | P0 | schema design | keep v1 + v2 |
| LRA-004 | PostgreSQL CI validation | COMPLETE / VERIFIED | P0 | migrations | continue enforcing CI |
| LRA-005 | Live Neon read-only inspection | PARTIAL / BLOCKED | P0 | Neon auth or stable Opera connector | target URL reached; inspect live schema when connector stabilizes |
| LRA-006 | Live schema overlap audit | WAITING | P0 | LRA-005 | inspect claimedge_os + leap_roi |
| LRA-007 | Temporary Neon branch validation | WAITING | P0 | LRA-006 | prepare migration branch |
| LRA-008 | Production Neon apply | APPROVAL_REQUIRED | P0 | LRA-007 | explicit human approval |
| LRA-009 | Leap API credential/config | BLOCKED | P1 | authorized admin/account | configure secret |
| LRA-010 | First read-only Leap reconciliation | WAITING | P1 | LRA-009 + LRA-007 | ingest active jobs |
| LRA-011 | Baseline missing-field audit | WAITING | P1 | LRA-010 | generate verified baseline |
| LRA-012 | Manual-time baseline sample | WAITING | P1 | live workflow | measure before automation |
| LRA-013 | First owner snapshot | WAITING | P1 | live data | preserve before state |
| LRA-014 | Production webhook receiver | APPROVAL_REQUIRED | P1 | credentials + Neon prod | deploy only after approval |
| LRA-015 | Recurring reconciliation | APPROVAL_REQUIRED | P2 | production integration | activate after live QA |
| LRA-016 | Promote reusable DEBO lessons | READY_FOR_REVIEW | P2 | project reconciliation | patch DEBO Core separately |
