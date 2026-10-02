---
name: jct-revenue-leakage-auditor
description: Audit completed JC's Towing jobs for legitimate performed work that was omitted, under-documented, bundled incorrectly, or left unsupported before billing.
---

# JCT Revenue Leakage Auditor

## Trigger
Use before invoice finalization, after a major recovery, or during retrospective billing audits.

## Checks
Mileage; wait/standby; additional operators; cleanup; absorbent; winching/rigging; second unit; trailer work; cargo/load shift; scene management; storage; tolls; permits; vendors; adjuster/admin time; specialized equipment.

## Rules
- Potentially billable is not the same as billable.
- A line can be recommended only when actual performance evidence exists.
- Rate authority must be separate from performance evidence.
- No duplicate charges for the same truck/time/service.

## Output
PERFORMED / EVIDENCE / POTENTIALLY BILLABLE / RATE AUTHORITY / MISSING PROOF / ACTION.
