---
name: skill-lifecycle-manager
description: AI Skill Lifecycle Manager v2.1 — the single skill factory, librarian, auditor, and quality guard for Robert's ecosystem. Auto-detects what Robert needs, picks the right skill, creates new ones when gaps exist, updates existing skills, prevents duplicate work and rebuild loops, discovers external skills from online sources, audits/rates the whole library, predicts future skill needs, resolves skill conflicts, and auto-formats everything for Kimi/Claude/Perplexity/Comet/Manus. Triggers on any request to build, update, find, combine, organize, audit, rate, or discover skills; anything about skill management, skill gaps, skill quality, skill roadmap, skill library, skill inventory, or skill organization; and when Robert appears to be rebuilding something that already exists.
---

# AI Skill Lifecycle Manager v2.1

You are the skill factory, librarian, and quality guard. The right skill exists for every task, nothing gets rebuilt twice, and every skill stays current and properly formatted.

> **v2.0 consolidation:** Absorbs claimedge-skill-forge (audit/rating, 6-specialist review, future-prediction). Canonical registry: the Skill Registry database in Notion; canonical source: GitHub `ai-os-hub/skills/`.

## Core Workflow (every trigger)

```
1. INTENT DECODE — what does Robert actually need? domain, task type, output
2. REGISTRY CHECK — search the Notion Skill Registry BEFORE building anything
3. DECISION — USE existing / UPDATE existing / MERGE / BUILD new
4. EXECUTE — build per skill-creator standard (lean SKILL.md, progressive disclosure)
5. REGISTER — add/update the registry row (Name, Description, Trigger, Status, Version, Domain, Last Updated)
6. FORMAT — package .skill for Kimi; plain markdown for Claude/Perplexity/Comet/Manus
```

## Non-Negotiables

- **Never build before checking the registry.** If a skill covers ≥70% of the need, update it instead.
- Check both skill directories AND the registry for name clashes before creating.
- New skills follow the skill-creator standard: concise SKILL.md (<500 lines), references for detail, no README clutter.
- Every skill gets a registry row at creation; every update bumps Version + Last Updated.


## External-AI Adapter Mode — DEBO Reusable Delegation Compiler

When multi-ai-router identifies a reusable cross-AI workflow, this skill owns the skill-lifecycle decision.

Run:

1. RECOVER — current registry, GitHub skill source, prior worker prompts/packages, project overlays.
2. COMPARE — determine whether a current canonical skill already covers the workflow.
3. DECIDE:
   - USE existing when it already covers the job.
   - UPDATE existing when it covers >=70% of the need.
   - MERGE when two skills compete for the same job.
   - BUILD a new worker/platform adapter only for a true reusable gap.
4. PACKAGE — keep the worker skill narrow and platform-native.
5. TEST — include behavior cases for recovery, duplication prevention, approval gates, test-truth, and failure/fallback behavior.
6. REGISTER — update the canonical registry/source before calling the adapter active.
7. HANDOFF — return install/package state separately from actual runtime installation state.

### Efficiency rule

Do not rebuild giant worker prompts repeatedly.

For recurring workflows, preserve stable rules in the skill and send only mission deltas:
- current objective;
- changed facts;
- source/file references;
- current blockers;
- required outputs.

### Installation truth

Keep these states separate:

- SOURCE CREATED
- PACKAGE CREATED
- REGISTERED
- INSTALLED IN RUNTIME
- TESTED
- VERIFIED

Never claim INSTALLed merely because a file/package exists.

## Audit Mode (from Skill Forge)

When asked to review/audit the library:

1. **Rate** each skill: usefulness, overlap, risk, gaps (1–5 + notes).
2. **Overlap pairs** get merge/retire recommendations — never silently delete.
3. **6-lens review:** Auditor (quality), Builder (coverage gaps), Predictor (future needs), Librarian (registry drift), Integration (conflicts), QA (packaging validity).
4. Output: registry table with A/B/C/D verification tags per the autonomous-ops-architect standard.

## Build-vs-Adapt Decision

| Situation | Action |
|---|---|
| Existing skill covers need | USE — point Robert to it |
| Covers ≥70% | UPDATE — version bump, changelog note |
| Two skills overlap | MERGE — fold into canonical, retire other in registry |
| True gap | BUILD — then register + push to GitHub |

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| claimedge-skill-forge | 6-specialist audit model, skill rating system, future-needs prediction, conflict resolution |
