# DEBO Reusable Delegation Compiler Rule v1.0

**Scope:** GLOBAL / all DEBO sister brains  
**Authority:** DEBO  
**Date:** 2026-10-06  
**Status:** ACTIVE CONTROL RULE  
**Canonical owners:** `multi-ai-router` + `skill-lifecycle-manager`

## Purpose

When Kimi, K3, Claude, Perplexity, Manus, Codex, Gemini, Comet, or another approved worker can materially accelerate a task, DEBO should not automatically fall back to a giant one-off copy/paste prompt.

DEBO first decides whether the delegation should become a reusable governed worker skill or adapter.

## Operating sequence

RECOVER
→ ROUTE
→ REUSABILITY GATE
→ USE / UPDATE / MERGE / BUILD
→ STRUCTURE WORKER PROMPT
→ TEST
→ EXECUTE MISSION
→ RETURN RECEIPTS
→ DEBO VERIFY
→ MERGE CANON

## Prime rule

RECOVER BEFORE REBUILD.

Search:
1. project truth and latest checkpoint;
2. existing DEBO skills;
3. sister-brain skills;
4. worker/platform skills;
5. prior handoffs/prompts;
6. current source code/schemas/tests;
7. durable GitHub/Drive/Notion artifacts when relevant.

Do not make Bobby repeat recoverable context.

## Delegation modes

### NATIVE
DEBO/ChatGPT can do the work better or with lower handoff cost.

### ONE-OFF
External worker is useful, but the task is unique or too small to justify a reusable adapter.

### UPDATE-SKILL
A current skill already covers most of the need. Extend it instead of creating another skill.

### NEW-WORKER-SKILL
A recurring, stable, high-value workflow has a true reusable gap. Build the narrow adapter first, test it, then execute the mission through it.

## Structured worker-skill prompt template

Use this skeleton and fill only mission-relevant sections:

```text
DEBO — REUSABLE WORKER SKILL BUILD

PROJECT:
MISSION:
PARENT AUTHORITY: DEBO

PURPOSE:
Convert this recurring external-AI workflow into a reusable governed skill/adapter.

RECOVER FIRST:
- Search current project truth.
- Search existing DEBO/sister-brain skills.
- Search prior worker outputs.
- Search current code/schemas/tests where relevant.
- Reuse or update before building.

SKILL ACTION:
USE / UPDATE / MERGE / BUILD

ROLE:
Keep this skill narrow. It coordinates only its defined job and delegates specialist work to existing skills.

WORKFLOW:
RECOVER → REUSE → EXECUTE GAP → TEST → RECEIPT → HANDOFF

TOOLS ALLOWED:
[mission-specific]

TOOLS PROHIBITED:
[mission-specific]

APPROVAL FIREWALL:
No publishing, sending, spending, deployment, destructive changes, ownership/recovery changes, unsupported public claims, or real-data creation without explicit authorization.

TRUTH RULE:
Unknown stays UNKNOWN / TBD / OWNER CONFIRMATION REQUIRED as appropriate.
Do not convert possibilities into performed facts.

AGENT MODE:
Use controlled native swarm only when actually available and useful.
Otherwise use sequential/K3 fallback.
Never fake parallel execution.

EFFICIENCY:
- reuse stable context;
- send deltas;
- avoid repeated giant searches;
- avoid unnecessary agents;
- preserve reusable outputs;
- optimize token/credit use without sacrificing verification.

TESTS:
- recovery before build;
- duplicate prevention;
- approval-gate behavior;
- security/privacy boundaries;
- test truth;
- fallback behavior;
- return contract.

RETURN:
STATUS
RECOVERED
REUSED
BUILT/UPDATED
TESTED
NOT TESTED
SKILLS USED
CONFLICTS
SECURITY
OPEN GAPS
APPROVALS
FILES/ARTIFACTS
INSTALL STATE
NEXT ACTION
```

## Runtime rule

A source file or package is not proof of native installation.

Track:
SOURCE CREATED
→ PACKAGE CREATED
→ REGISTERED
→ INSTALLED
→ TESTED
→ VERIFIED

## Approval boundary

Internal read-only recovery, analysis, drafting, code preparation, safe local tests, and packaging may proceed automatically.

External/destructive actions remain approval-gated.

## Inheritance

This rule applies DEBO-wide and should be inherited by project/sister-brain routers unless a narrower project rule explicitly overrides it.
