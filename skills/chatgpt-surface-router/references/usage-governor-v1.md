# DEBO ChatGPT Usage Governor v1.1 — routing examples and acceptance

**Parent skill:** `skills/chatgpt-surface-router/SKILL.md`. This is a reference for the **existing** surface router, not a new standalone skill or installed ChatGPT setting.
**Authority:** DEBO bootstrap, project-specific instructions, account permissions, privacy and owner approval always take precedence.

## Quick routing examples

| Case | Default route | Avoid |
|---|---|---|
| One simple question or brief explanation | Chat / Instant, concise answer | Work, Deep Research, agent swarm |
| Multi-step comparison using known source files | Chat + targeted files; Medium if needed | Full library rescan or repeated giant context |
| Conflicting public-source investigation | Search first; Deep Research for truly extended evidence | Unnecessary long research on one fact |
| Authenticated multi-app records and completed artifact | Work + supported permissioned connectors | Pretending ordinary chat has browser session access |
| Repository refactor with tests | Codex or GitHub-approved development workflow; QA/checkpoint | Calling browser agents for every edit |
| Hard risk/architecture decision | High reasoning if available and justified | Defaulting to costly/slowest mode for routine work |
| API workflow with observed usage metrics | Approved telemetry, per-project scope, model-aware costs | Treating API tokens as ChatGPT Plus consumption |
| User asks remaining account usage but no authorized meter | Label USAGE UNKNOWN; describe exact Settings inspection step | Inventing credits, token balance or reset time |
| Observed quota low | Finish one high-impact task; concise checkpoint; retain quality gates | Unauthorized billing, fallback to unapproved tenant |

## Acceptance cases (manual or static QA)

- **R1 — No duplicate owner.** The only new governance language extends `chatgpt-surface-router`; `chatgpt-mode-router` and `multi-ai-router` remain supporting, and neither is replaced.
- **R2 — Plan separation.** Consumer ChatGPT allowance is distinct from separately metered API usage; no automatic token-account mapping.
- **R3 — Unknown is unknown.** Missing signed-in usage view never yields an estimated remaining percentage, reset time or claim that quota was inspected.
- **R4 — Routine cheap path.** A short factual request does not trigger Work or Deep Research without an execution/research reason.
- **R5 — Actual execution path.** Browser, connected app and repo-change requests select tools capable of doing the work; not merely the lowest-cost model.
- **R6 — Approval firewall.** No credit purchase, API key capture, expanded access, public release, or sensitive transfers.
- **R7 — No false savings.** Do not claim a percentage reduction without comparable observed before/after usage data.
- **R8 — Preserve evidence.** Compact checkpoints keep source refs, approvals, real statuses and rollback; compression must not erase contradictions.
- **R9 — Accessibility.** Concision must preserve legibility and plain-English clarity; never optimize by producing a cryptic output.
- **R10 — Promotion.** Static checks and GitHub CI do not establish live availability in fresh ChatGPT/Work sessions. Require actual task tests after reviewed plugin promotion.

## Measurement for a bounded pilot

Use three **non-sensitive** representative tasks: a routine answer, source-backed research, and a safe code/tool task. Before/after compare: correctly completed outcomes, repeated retrieval attempts, unnecessary mode transitions, observed model/tool calls, and usage/cost only where an authorized source exposes it. Keep the current project checkpoint as the one ledger; don't add a new tracker. Mark token savings **NOT MEASURED** until observed. Reserve QA capacity when a specific finite budget is known.

## Trusted public references

- OpenAI ChatGPT Projects: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- ChatGPT Work and Codex: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- OpenAI API usage: https://platform.openai.com/usage
- OpenAI API prompt caching: https://platform.openai.com/docs/guides/prompt-caching

**Change control:** Draft PR, verify GitHub readback, run available CI and independent source review, then update only the existing private DEBO plugin if appropriate; no account-level activation inferred from GitHub.
