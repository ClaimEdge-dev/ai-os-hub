---
name: jct-dispatch-pricing-guardrail
description: Give dispatchers safe pricing guidance from approved JC rate sources and account contracts while preventing unsupported quoting.
---
# JCT Dispatch Pricing Guardrail
Identify towing lane, vehicle/equipment class, account/payer, jurisdiction, service and approved rate authority before quoting. If authority is missing/conflicting, return HOLD / JOHN APPROVAL instead of guessing. Never convert municipal, relocation, insurer, retail or contract rates across lanes. Record quote source/version and exceptions.
