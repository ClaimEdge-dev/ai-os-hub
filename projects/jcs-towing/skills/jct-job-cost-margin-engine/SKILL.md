---
name: jct-job-cost-margin-engine
description: Model the actual economics of JC's Towing jobs and services using verified operating costs, billing, collections, and write-downs. Never invent JC operating costs.
---

# JCT Job Cost & Margin Engine

## Trigger
Use for profitability, minimum acceptable rates, job margin, truck-hour economics, pricing decisions, commercial-account pricing, or heavy-recovery economics.

## Inputs
Truck/unit operating cost; fuel; operator labor burden; insurance allocation; equipment/maintenance; dispatch/admin; deadhead; storage; subcontractors; payment fees; collection delay; denials/write-downs.

## Rules
- Recover actual JC costs first.
- Missing cost inputs remain TBD/UNRESOLVED; do not infer them.
- Separate billed revenue from collected revenue.
- Separate direct cost from allocated overhead.
- Never treat a proposed list rate as collected revenue.

## Output
JC LIST RATE / TARGET COLLECTED RATE / CONTRACT RATE / MINIMUM ACCEPTABLE RATE / DIRECT COST / CONTRIBUTION MARGIN / COLLECTION RISK, with assumptions clearly labeled.
