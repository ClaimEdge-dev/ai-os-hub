---
name: rrr-dispatch-intake
description: Normalize Rapid Roadside Repair dispatch/job intake without inventing facts or availability.
---
# RRR Dispatch Intake

Capture:
caller/account; callback; location; vehicle/unit; service need; urgency/safety; symptoms; accessibility; requested destination if applicable; timestamps; source; known constraints; approval/escalation need.

Never invent ETA, availability, price, service capability, equipment, or diagnosis.
If requested work is outside verified capability, route to HOLD / OWNER DECISION.
Output: normalized dispatch record + missing facts + safe next action.
