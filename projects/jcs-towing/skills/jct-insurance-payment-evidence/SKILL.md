---
name: jct-insurance-payment-evidence
description: Build evidence of what insurers and claim payers actually allow and pay JC's Towing by extracting paid invoices, remittances, reductions, denials, adjuster communications, and payment timing.
---

# JCT Insurance Payment Evidence

## Trigger
Use when analyzing carrier payment behavior, historical reimbursements, allowed amounts, payment delays, invoice reductions, or insurer-specific rate evidence.

## Record
Carrier; claim; date of loss; job; invoice total; submitted date; line item; billed amount; allowed amount; paid amount; reduced/denied amount; denial reason; adjuster; documents requested; payment date; days to pay; source evidence.

## Rules
- Policy roadside-benefit limits are not vendor reimbursement rates.
- One paid claim does not establish a universal carrier rate.
- Preserve the original remittance/invoice evidence.
- Never generalize beyond the available claim population without labeling the limitation.

## Output
Carrier payment evidence table, repeat-payment patterns, disputed-line patterns, and evidence-backed rate references.
