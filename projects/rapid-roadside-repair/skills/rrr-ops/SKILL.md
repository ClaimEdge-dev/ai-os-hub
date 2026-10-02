---
name: rrr-ops
description: Root router for Rapid Roadside Repair under DEBO Core.
---
# RRR-OPS

Route RRR work through verified business truth and approval gates.

## Routes
- TRUTH → rrr-business-truth-auditor
- SERVICES → rrr-service-capability-register
- DISPATCH → rrr-dispatch-intake
- EVIDENCE → rrr-job-evidence-narrative
- RATE / QUOTE → rrr-rate-authority-manager
- CRM / LEAD → rrr-crm-lead-account
- WEB / PUBLIC CLAIM → rrr-website-public-claim-qa

## Invariants
Never invent services, rates, equipment, territory, credentials, ETA, availability, contracts, or public claims.
Unknown required facts remain TBD/HOLD.
External sends, publishing, spending, account changes, and destructive actions require approval.
