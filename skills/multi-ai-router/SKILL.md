---
name: multi-ai-router
description: Answers which AI, which Kimi mode, and which connector stack for any task. Routes between Kimi, Perplexity, Claude, Manus, Comet; picks Kimi Instant/Thinking/Agent/Agent Swarm; maps connectors (Notion, Neon, Supabase, GitHub, Canva) to Robert's 6 domains; explains Kimi features (Claw, Scheduled Tasks, Code, Deep Research, Deploy); generates handoff master prompts. Triggers on 'which AI should I use', 'which connectors', 'send this to Perplexity', 'decode this', 'explain this feature', or at complex workflow kickoff.
---

# Multi-AI Router v2.0

One skill answers three questions: **which AI**, **which mode**, **which connectors**.

> **v2.0 consolidation:** Absorbs perplexity-connector-advisor (connector toggle mapping) and ai-workflow-decoder (Kimi version/feature decode + prompt generation).

## The Routing Table

| Task type | Best tool | Why |
|---|---|---|
| Builds, code, HTML apps, browser actions | **Kimi Agent/Code** | Executes, not just advises |
| Architecture, audits, governance, long docs | **Kimi Thinking** | Long-context reasoning |
| Massive parallel research | **Kimi Agent Swarm** | Auditable sub-agents |
| Final fact/link verification, current events | **Perplexity** | Live citations |
| Letter/email/report polishing | **Claude** | Best prose synthesis |
| Hands-free multi-page browser extraction | **Comet / Manus** | Persistent browser agents |

## Connector Stack by Domain (Perplexity + Kimi)

| Domain | Connectors ON | Connectors OFF |
|---|---|---|
| Claims (ClaimEdge) | Notion, GitHub, Neon | Wrestling DBs, Canva |
| Wrestling/Sports | Notion, Neon (wrestling DB), GitHub | Claims repos |
| AI/Automation | GitHub, Notion | Domain DBs |
| Research | Scholar, web, Notion | Production DBs |
| Productization | GitHub, Notion, Canva | — |

Rule: enable only the connectors the task needs — every unnecessary connector wastes context and risks cross-domain data leaks.

## Kimi Feature Quick Decode

- **Thinking vs Agent vs Swarm**: reasoning / doing / parallel-doing. When unsure: Thinking for decisions, Agent for builds, Swarm only with clear sub-tasks.
- **Claw**: browser control for repetitive web tasks. **Scheduled Tasks**: recurring presets (see OS | Scheduled Task Presets). **Deep Research**: long-form cited reports. **Deploy**: publish HTML/webapps.

## Handoff Prompt Generation

When routing to another AI, generate a copy-paste master prompt containing: goal, context (≤15 lines), exact deliverable, constraints, and "report back in this format". Never send Robert to another AI empty-handed.

## Session Start Integration

At complex-workflow kickoff, output one routing card: `Goal → AI sequence → Mode per step → Connectors on/off → Expected deliverable`. Then execute step 1.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| perplexity-connector-advisor | Domain→connector toggle map, availability rules, wasted-connector prevention |
| ai-workflow-decoder | Kimi version/mode selection, feature explanations, master prompt generation |
