---
name: rrr-approval-gate
description: Gate consequential Rapid Roadside Repair actions until required truth, evidence and explicit approval exist.
---
# RRR Approval Gate

Consequential actions include:
public publishing; customer/vendor communication; quote/rate release; live CRM mutation; deployment; account/auth changes; legal/compliance assertions; production automation.

Return:
APPROVED / HOLD / BLOCKED

Required output:
action requested; approval source; truth dependencies; evidence dependencies; rollback; unresolved blocker.

Default: if approval or required truth is ambiguous, do not execute the consequential action.
