# Automation Backlog — Leap ROI / ClaimEdge
Status: CONTROLLED BACKLOG

| Automation | State | Trigger | Action | Approval |
|---|---|---|---|---|
| GitHub schema CI | ACTIVE | PR changes under Neon schema | PostgreSQL migration + fixture test | no |
| Neon connector health check | BLOCKED | resume / access change | read-only project/branch/table check | no |
| Live schema overlap audit | WAITING | Neon access restored | compare live objects to proposed schema | no |
| Leap read-only reconciliation | WAITING | Leap token + Neon temp validation | fetch active jobs, reconcile IDs/fields | no for read-only |
| Missing-field detector | WAITING | reconciliation import | score current required fields | no |
| Stage/cycle-time tracker | WAITING | webhook/API event | append stage event + duration | production write approval |
| Webhook dedupe receiver | READY_FOR_BUILD | credentials + deploy target | durable receipt, normalize, dedupe | deploy approval |
| Daily reconciliation | PARKED | production integration stable | detect missed webhook/state drift | enable approval |
| Weekly owner snapshot | PARKED | live baseline established | generate verified KPI snapshot | delivery/publish approval if external |
| Source freshness checker | PARKED | live sources mapped | flag stale carrier/CRM fields | no if internal/read-only |
| Process-defect miner | PARKED | enough audit history | detect recurring missing fields/rework | no |
| Global rule harvester | ACTIVE MANUAL/DEBO | reusable pattern discovered | add promotion candidate | no; global promotion reviewed |
| Thread/project checkpoint compiler | ACTIVE | meaningful checkpoint | update resume/task/control docs | no |
| Invoice/billable check | ACTIVE RULE | inspection/claim service work | flag potential billable event | no; sending invoice approval-gated |

## Priority
1. restore Neon read access;
2. live overlap + temp validation;
3. Leap read-only integration;
4. baseline capture;
5. webhook production deployment;
6. recurring reconciliation/reporting.

## Anti-bloat rule
Do not activate an automation just because it is technically possible.
Activate only when:
- dependency exists;
- measurable value exists;
- no duplicate native integration already solves it;
- failure mode is understood;
- owner and rollback path are defined.
