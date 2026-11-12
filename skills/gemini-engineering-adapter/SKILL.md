---
name: gemini-engineering-adapter
description: Route an approved DEBO coding, Google Apps Script, Workspace automation or integration task to Gemini as first-pass Forge implementation worker and return exact source/test evidence to the existing DEBO orchestrator. Trigger when the task is scoped for Gemini, a Gemini build result arrives, or a Google ecosystem build requires a governed handoff.
---

# Gemini Engineering Adapter v0.1 | REVIEW CANDIDATE

**Owner:** DEBO Core / Mack routes; Atlas architecture; Forge implements; Proof + Shield review. This adapter does not replace `multi-ai-router`, `agent-talent-manager`, or the canonical skills registry. It does not mean Gemini is connected, authorized or executing.

## When to use
Use if a real authorized Gemini runtime has a material coding/Google tool advantage, the project boundary and cost are known, and the task can be handed off without leaking private tenant/customer/youth information. Otherwise use the existing ChatGPT/GitHub builder or a separately authorized tool; mark external delivery NOT_EXECUTED.

## Inputs
MISSION_ID, PROJECT_ID, CURRENT_CHECKPOINT, EXACT_SOURCE_REF_SHA, GOAL, ACCEPTANCE_TESTS, TOOL_SCOPE, DATA_CLASS, ALLOWED_ACTIONS, PROHIBITED_ACTIONS, OWNER_APPROVALS, TIME_OR_COST_LIMIT, OUTPUT_LOCATION, RETURN_TO_DEBO.

## Procedure
1. Recover `DEBO_BOOTSTRAP.md`, current versioned source, project instructions, relevant tests and approved technical architecture.
2. Verify that this Gemini session *actually* has the named GitHub/Google tools, authentication, permissions, credits, and allowed data. No invented integrations.
3. Implement smallest reversible change on authorized feature branch. Avoid public/private source boundary violations and duplicate registries.
4. Use risk-based red/green testing for executable behavior; use structural/readback validation for documentation-only changes. Test tenant isolation, retries, rollback, failures and security negatives as appropriate.
5. Run or clearly label not-run tests. Commit only with authorized branch access; never self-merge protected PRs or deploy. Do not claim a successful CI run without exact head and receipt.
6. Return to DEBO using the common packet in `skills/multi-ai-router/references/three-ai-command-protocol-v1.md`. If no verified delivery route, supply a copy/paste packet and an authorized GitHub reference; do not claim direct delivery.

## Must not
- No exposed tokens, secret reuse, account linking, private cross-project uploads, unapproved cost, production changes, public release, external messaging or protected merge.
- No auto-reroute of Browser Use writes after credit exhaustion.
- No false claims that Google Workspace, GitHub, Gemini, ChatGPT and Perplexity share memory.
- Preserve DEBO-05 live sync gate and PR #74 security HOLD.

## Acceptance
- Explicit scoped authority and correct project owner.
- Exact file paths and real commit SHA, or explicit UNSAVED/UNEXECUTED.
- Command + exit status/test receipt for each claimed test.
- Independent DEBO review before APPROVED/MERGED/DEPLOYED/LIVE.
- One concise handoff (<=400-token cover + links/attachments) containing EVIDENCE, RISK, BLOCKER, NEXT_ACTION and RETURN_TO_DEBO.

## Negative tests (manual/CI)
- Missing GitHub write permission -> DO NOT CLAIM COMMIT.
- Missing code runtime -> patch only; TEST_NOT_RUN.
- Research without source dates -> request/source check; do not manufacture citations.
- Credit exhaustion + interactive write -> BLOCK; no alternate write provider.
- Cross-entity sensitive data -> reject transfer; redact/keep local.
- PR CI on wrong SHA or skipped tests -> HOLD.
- Unverified Gemini -> DEBO makes copyable instruction only, no claim of independent worker.
