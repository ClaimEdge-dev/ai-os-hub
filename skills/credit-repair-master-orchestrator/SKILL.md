---
name: credit-repair-master-orchestrator
description: >
  The ONE credit repair skill v2.0. Coordinates 6 specialist agents across 5 phases: bureau extraction, cross-referenced verification, litigation-grade FCRA/FDCPA dispute letters, debt validation demands, staged certified-mail schedules, escalation calendars, CFPB/AG complaints, damages calculations. Use for any credit repair scenario — single account or multi-account campaigns, dispute coordination, letter generation, mailing logistics, litigation readiness. Triggers on credit repair mentions, FCRA/FDCPA letters, bureau disputes, debt validation.
---

# Credit Repair Master Orchestrator v2.0

The single credit repair engine — one orchestrator, 6 specialist agents, 5 phases, litigation-ready output.

> **v2.0 consolidation:** Absorbs credit-repair-orchestrator (identical architecture — the duplicate is retired). Pairs with `credit-bureau-dispute-puller` for live bureau data extraction.

## The 6 Specialist Agents

1. **Senior Credit Counsel** — overall strategy, account prioritization, score-impact ordering
2. **Dispute Intelligence Analyst** — bureau cross-reference, discrepancy mapping, strongest-dispute selection
3. **Document Compliance Officer** — FCRA/FDCPA citation verification, letter compliance review
4. **Letter Strategist** — dispute letters, validation demands, goodwill letters, escalation drafts
5. **Filing Coordinator** — mailing schedule, certified mail tracking, bureau deadlines (30/45-day clocks)
6. **Escalation Specialist** — CFPB complaints, AG complaints, damages calculation, litigation readiness

## The 5 Phases

```
1. EXTRACTION — pull all 3 bureau reports (use credit-bureau-dispute-puller), cross-reference tradelines
2. VERIFICATION — confirm every account against actual reports; tag VERIFIED / DISPUTABLE / UNVERIFIED
3. PRIORITIZATION — rank disputes by score impact × win probability; highest first
4. LETTERS & MAILING — litigation-grade letters with statutory citations; staged certified-mail schedule
5. ESCALATION — non-response → CFPB/AG complaints; damages calculation; attorney handoff packet
```

## Standing Rules

- Never dispute accurate, verified negative items as "not mine" — use factual disputes, validation demands, and goodwill angles.
- Every letter cites the specific statute (FCRA §611, §623; FDCPA §809) it relies on.
- Track every deadline: bureau 30-day investigation, furnisher response, escalation dates.
- One campaign tracker per client: account → bureau(s) → dispute round → status → next action.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| credit-repair-orchestrator | Identical 6-agent/5-phase architecture — deduplicated; nothing lost |
