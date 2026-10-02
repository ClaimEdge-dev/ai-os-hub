---
name: jct-dispatch-intake
description: Create or reconstruct a JC's Towing dispatch/job record from calls, texts, screenshots, notes, photos, or partial job information without inventing ETA, price, capability, or authorization.
---
# JCT Dispatch Intake

## Global JCT invariants
- Recover existing JC's Towing work before rebuilding.
- Truth states: VERIFIED, PROVISIONAL, CONFLICT, TBD.
- Never invent rates, service capabilities, licenses, authority, fleet capacity, ETAs, contracts, or public claims.
- Preserve source evidence and keep transformations traceable.
- Default to private, reversible work.
- Sending, publishing, spending, account/identity changes, and destructive actions require approval.
- File durable artifacts in the existing JC'S TOWING — DEBO BUSINESS OS structure.
- Return material state changes to JCT-OPS.

## Capture
Caller/customer, callback, dispatch/referral source, exact location, safe-access notes, vehicle/unit type, tractor/trailer/load state when relevant, condition/reason, pickup, destination, urgency/safety, required equipment, assigned operator/unit, timestamps, authorization/payment/account type, evidence, status.
## Workflow
Normalize supplied facts; distinguish supplied versus inferred; flag missing dispatch-critical fields; route completed jobs to narrative/billing.
## Output
Dispatch record + missing-field list + next operational/billing route.
