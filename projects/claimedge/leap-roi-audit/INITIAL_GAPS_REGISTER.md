# Initial Leap Gap Register

Status: USER-REPORTED / NEEDS VERIFICATION
Created: 2026-09-27

This register captures gaps surfaced while building the current Leap workflow. It is not proof that a field is absent from every job.

| Section | Field | Initial status | Verification target | Business effect if missing |
|---|---|---|---|---|
| Insurance | Policy number | USER-REPORTED MISSING | policy/declarations/carrier docs | weak claim linkage, slower retrieval |
| Contact | Insured/customer email | USER-REPORTED MISSING | intake/CRM/email | follow-up friction |
| Carrier | Carrier fax | USER-REPORTED MISSING | carrier letter/contact sheet | slower document transmission |
| Adjuster | Adjuster phone | USER-REPORTED MISSING | carrier correspondence | slower follow-up |
| Financial | ACV | USER-REPORTED MISSING | carrier estimate/settlement | financial state incomplete |
| Financial | Deductible | USER-REPORTED MISSING | declarations/estimate | net-claim math incomplete |
| Financial | Net claim | USER-REPORTED MISSING | settlement/estimate | collection planning incomplete |
| Financial | Depreciation | USER-REPORTED MISSING | estimate | recoverable/nonrecoverable tracking incomplete |
| Financial | RCV | USER-REPORTED MISSING | estimate | total claim-value baseline incomplete |
| Financial | Upgrade totals | USER-REPORTED MISSING | estimate/supplements | upgrade revenue/scope not visible |
| Financial | Supplement totals | USER-REPORTED MISSING | supplement history | claim uplift not measurable |
| Operations | Work type | NEEDS AUDIT | Leap | reporting/routing weakness |
| Operations | Category | NEEDS AUDIT | Leap | segmentation weakness |
| Operations | Job duration | NEEDS AUDIT | Leap/timestamps | cycle-time not measurable |
| Operations | Job ID | NEEDS AUDIT | Leap | cross-system joining risk |
| Operations | Job name | NEEDS AUDIT | Leap | lookup quality |
| Operations | Lead name | NEEDS AUDIT | Leap | ownership ambiguity |
| Operations | Job title | NEEDS AUDIT | Leap | role/reporting ambiguity |
| Operations | Division | NEEDS AUDIT | Leap | profitability segmentation missing |
| Operations | Tasks | NEEDS AUDIT | Leap | next-action leakage |
| Evidence | Photos/files | NEEDS AUDIT | Leap/Drive/evidence store | proof fragmentation |
| Notes | Claim notes | NEEDS AUDIT | Leap/threads/Drive | context loss |
| Pipeline | Lead | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |
| Pipeline | Adjustment estimate | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |
| Pipeline | Appointment | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |
| Pipeline | Adjustment complete | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |
| Pipeline | Follow-up | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |
| Pipeline | Contract scheduled | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |
| Pipeline | Build | PRESENT-STAGE-TO-VERIFY | Leap | stage consistency |

## Audit rule

For every row, capture:
- claim/job
- prior field state
- corrected field state
- source document
- verification status
- who/what found it
- minutes to find manually
- minutes with current process
- rework prevented
- downstream systems updated
- financial relevance
- confidence
