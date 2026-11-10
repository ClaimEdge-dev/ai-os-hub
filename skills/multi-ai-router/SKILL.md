---
name: multi-ai-router
description: >
  Routes any DEBO task to the best AI/model/mode/tool stack, then assigns a fallback model
  to cover known weaknesses. Use at complex workflow kickoff, before cross-AI handoffs, when
  a task needs research + build + browser execution, or when an agent stalls, overreaches,
  lacks citations, lacks execution access, produces weak output, or when a reusable external-AI workflow could eliminate repeated prompting and handoff work.
---

# Multi-AI Router v3.2

## Mission

Choose the smallest effective AI team, not the largest possible AI parade.

For every material task, decide:

1. PRIMARY AI
2. PRIMARY MODE
3. REQUIRED TOOLS / CONNECTORS
4. FALLBACK / REVIEW AI
5. HANDOFF CONTRACT
6. APPROVAL BOUNDARY
7. DONE CRITERIA

DEBO / ChatGPT remains the canonical orchestrator unless a project explicitly defines another authority.

## Core routing matrix

| Work type | Primary | Secondary / weakness coverage |
|---|---|---|
| Canonical project orchestration, connected apps/files, finished cross-system work | ChatGPT / DEBO; use Work for long execution | Claude for independent critique; Kimi for large parallel branch work |
| New API-based managed agent systems | OpenAI Agents API | Google ADK when A2A / Google Cloud topology is the better fit |
| Long-horizon reasoning, difficult synthesis, code review, dense document work | Claude Opus/Sonnet | ChatGPT for connector execution; Perplexity for current-source verification |
| Massive independent research/batch branches | Kimi K3 Swarm | ChatGPT merges canon; Perplexity independently verifies important public facts |
| Reusable Kimi workflow | Kimi Skill | Keep each Skill narrow; use Swarm only for independent parallel work |
| Current public-source research and citations | Perplexity Research / Pro Search | ChatGPT or Claude evaluates conclusions and applies them to project truth |
| Formal multi-agent app architecture, A2A, parallel/loop workflows, Google ecosystem | Gemini + Google ADK | ChatGPT/Claude for prompt/spec review |
| Authenticated browser work across tabs/sites | Comet or Manus Browser Operator | DEBO verifies results and records source state |
| Local-computer / file / CLI execution | Manus My Computer or Kimi Work/Code when authorized | GitHub + DEBO for durable version/control |
| Full-stack prototype or autonomous build | Manus / Kimi Agent / ChatGPT Work depending project | Independent Red Team before release |

## Prompting standards by model family

### OpenAI / ChatGPT / Agents
Agent definition should explicitly include:
- name
- mission/instructions
- tools
- guardrails
- MCP/connectors
- handoff targets
- structured output schema
- human approval points

For new API agent applications, prefer the Agents API. Keep one specialist clean before scaling into multi-agent workflows.

Official references:
- https://developers.openai.com/api/docs/guides/agents/define-agents
- https://openai.com/index/introducing-the-agents-api/

### Claude
Prompt Claude like a highly capable new employee:
- be explicit and direct
- give a role
- provide context and 3-5 good examples when useful
- use XML tags for complex prompts
- state whether to IMPLEMENT vs merely SUGGEST
- use subagents for independent/parallel/isolated work
- do direct work for simple sequential or single-file tasks
- require investigation before conclusions

Official reference:
https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables

### Kimi
Use:
- K3 Agent for autonomous execution
- K3 Swarm for large independent parallel branches
- Kimi Code for code/schemas/tests
- Skills for repeatable SOPs
- Claw/Work for persistent/scheduled/local workflows when available

Skill rule:
ONE SKILL = ONE COHERENT JOB.
Skill description must clearly state core function, scenarios and trigger phrases.

Official references:
- https://www.kimi.com/en/help/agent/agent-swarm
- https://www.kimi.com/en/help/plugins-and-skills/use-skills-in-agent
- https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html

### Gemini / Google ADK
Use ADK when the workflow benefits from explicit multi-agent topology:
- LlmAgent
- ParallelAgent
- LoopAgent
- A2A
- agent evaluation
- deployable agent services

Agent instructions should say:
- what this agent does
- when it should defer to another agent/tool
- how it should respond

Official references:
- https://google.github.io/adk-docs/tutorials/coding-with-ai/
- https://google.github.io/agents-cli/guide/use-cases/

### Perplexity Pro-only inventory and model selector (R144)

The owner reports **Perplexity Pro on iPhone**. Cloud Computer can be available to Pro, but no authenticated Computer action or Notion/GitHub permission is established in this ChatGPT session; do not infer access from marketing or a saved browser profile. Invoke the source-only \`perplexity-pro-research-router\` when choosing between Best, Pro Search, Reasoning (if shown), and Research. Its \`tools/debo_perplexity_pro_route.py\` helper picks only models from an observed menu, never from an assumed plan. Use \`cross-ai-artifact-inventory\` for account data rather than attempting to search private Perplexity history using public web search. Source skill: \`skills/perplexity-pro-research-router/SKILL.md\`; compare against current Perplexity official docs. The owner has not connected a Perplexity account-inventory API to this conversation.

### Manus project and account inventory (R144)

Use \`manus-debo-research-adapter\` plus \`cross-ai-artifact-inventory\` for Manus Projects, Task outputs, Skills and Connectors when actually accessible. The exposed Manus research-initiation tool is *not* evidence of account-wide task listing or finished research. Reuse the existing R148 dashboard task, not a duplicate new task. New tasks need correct owner, cost/credit and readback gates. Source skill: \`skills/manus-debo-research-adapter/SKILL.md\`.

### Perplexity
Use for:
- current-source discovery
- broad web reconnaissance
- independent source verification
- research reports with direct citations

Do NOT make Perplexity the canonical project database simply because it found the source.

Official references:
- https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search
- https://www.perplexity.ai/help-center/en/articles/10352901-what-is-perplexity-pro

### Manus
Use for:
- browser/cloud execution
- connected-app workflows
- local file/CLI execution through My Computer
- autonomous full-stack/web builds
- long operational workflows

Keep destructive/account-changing actions approval-gated.

Official references:
- https://www.manus.im/download
- https://manus.im/blog/manus-browser-operator

### Comet
Use when the job depends on the user's authenticated browser session, open tabs, or direct web interaction.
Keep visibility and user-control requirements intact.

Official references:
- https://www.perplexity.ai/en-GB/hub/blog/the-new-comet-assistant
- https://www.perplexity.ai/enterprise/comet

## Research Return Bridge (2026-11-02)

**Default choice:** Keep DEBO in regular ChatGPT, use its available connected sources and current web research first, and save evidence into the existing project checkpoint. Delegate to Perplexity only when it provides material independent source verification, larger research coverage, or a measurable advantage. Do not route every trivial search through an extra AI or burn Work quota to copy prompts.

**Optional automation architecture:** Authorized trigger (manual/scheduled/supported connected-app event) → existing project queue/checkpoint → native sources or Perplexity Agent API / Search API → standardized research packet → source/claim QA → project-specific private evidence store → DEBO resume/notification through a **verified supported** scheduled or event-driven task. A GitHub Action may produce a packet or PR; that alone does not wake a generic ChatGPT conversation. Never claim automatic end-to-end execution before a real triggered run and readback.

**Perplexity API selection:** Prefer current Agent API for web-grounded synthesized answers or Search API for web results that DEBO independently evaluates. Do not implement a new integration against retired legacy Sonar chat-completions endpoints. Use official current API docs to select endpoints and models at build time. API access and charges require verified credentials, a scoped budget, and prior authorization; no key or client/child/credit-case information in the public repository. GitHub Actions secrets must be configured through the approved secret manager, never committed.

**Minimum research handoff fields:** mission_id, project_id, objective, source_urls, retrieval_dates, factual_claims, direct_quotes_if_needed, uncertainty, conflicts, proposed_actions, priority, cost_estimate_if_known, approval_needed, output_artifact_pointer, verification_status, next_safe_action. Clearly label citations collected versus claims independently verified. Reuse the existing ledger, work queue and project memory; do not create a competing master.

**Release test before claiming hands-free:** One harmless scheduled or manually triggered test creates a private or non-sensitive research packet; confirm correct project/account isolation, source traceability, deduplication, bounded retries, protected credentials, checkpoint readback, supported ChatGPT task pickup, and no unauthorized messages/public launches/payments. Mark untested connections PROPOSED / NOT CONFIGURED.

**Reference sources checked 2026-11-02:** https://docs.perplexity.ai/docs/getting-started/overview ; https://github.com/perplexityai/modelcontextprotocol ; https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows ; https://learn.chatgpt.com/docs/automations?surface=app

## Weakness Compensation Rule

Never ask one model to be great at everything.

When PRIMARY has a known weakness, automatically assign a SECONDARY:

- research without enough citations -> Perplexity verifier
- strong analysis but no authenticated app access -> ChatGPT connector / Comet / Manus executor
- giant batch task becoming sequential -> Kimi Swarm
- large build without independent QA -> Claude or DEBO Red Team
- Google/A2A agent topology needed -> Gemini ADK
- polished conclusion but weak canonical state -> DEBO merges into Project Brain/registers
- browser execution produced facts -> source/evidence verifier before canonization

## Quota / Credit Guard

Before external delegation, use any visible worker quota, plan, rate-limit, or credit state as a routing constraint.

- Low remaining quota -> prefer delta prompts, existing skills, targeted branches, or an alternate capable worker.
- Do not spend scarce worker quota rediscovering project context that DEBO can recover itself.
- Build/update a reusable worker skill when doing so is expected to reduce repeated future prompt cost.
- Never claim a quota value unless it was actually observed in the current worker/runtime state.
- Do not buy credits or upgrade plans without explicit approval.

## Cross-AI handoff schema

MISSION_ID:
PROJECT_ID:
CHECKPOINT:
PRIMARY_AI:
SECONDARY_AI:
OBJECTIVE:
CURRENT_TRUTH:
SOURCES:
FILES:
UNKNOWN:
CONFLICTS:
TOOLS_ALLOWED:
TOOLS_PROHIBITED:
APPROVALS_REQUIRED:
DONE_CRITERIA:
OUTPUT_SCHEMA:
RETURN_TO_DEBO:

## Delegation test

Use another agent only if at least one is true:
- work can run independently in parallel
- isolated context reduces contamination
- specialist tools are materially better
- independent verification is valuable
- primary model lacks the needed connector/execution environment

Do NOT spawn an agent for:
- one simple fact
- one small file edit
- sequential steps that share tight state
- ceremonial role-playing


## Reusable Delegation Compiler Rule — DEBO-Wide

DEBO must automatically apply this rule when another AI/tool has a material advantage.

Do not make Bobby ask for a reusable setup after the fact.

Before issuing a cross-AI prompt:

1. RECOVER the current project truth, prior worker outputs, relevant skills, code, schemas, tests, and durable handoffs.
2. CHECK the skill registry and worker/platform adapters.
3. CLASSIFY the delegation:
   - NATIVE — DEBO/ChatGPT should do it directly.
   - ONE-OFF — bounded external task; use a structured one-time handoff.
   - UPDATE-SKILL — an existing skill covers most of the need; extend it.
   - NEW-WORKER-SKILL — a genuine reusable gap exists; build the narrow worker skill first, then execute the mission through it.
4. USE skill-lifecycle-manager for USE / UPDATE / MERGE / BUILD decisions.
5. Prefer delta prompts, patches, references, and durable source links over repeatedly pasting giant context blocks.
6. Add platform-native agent/swarm instructions only when that runtime actually supports controlled execution.
7. If native swarm is unavailable, use a governed sequential/K3-style fallback rather than pretending parallel agents ran.
8. Require a structured return contract, receipts, test truth, known gaps, integration target, rollback, and approvals.
9. Route returned work back to DEBO for verification before canonization.

### Reusability gate

Prefer UPDATE-SKILL or NEW-WORKER-SKILL when one or more are materially true:
- the workflow is likely to recur;
- the task has multiple stable steps;
- the same specialist roles will be reused;
- the handoff prompt is large or expensive to reconstruct;
- a worker-specific capability meaningfully reduces future time/credit use;
- the result should be portable across sister brains.

Prefer ONE-OFF when:
- the task is genuinely unique;
- the workflow is tiny;
- the rules are too unstable to encode;
- creating a skill would cost more than the expected reuse.

### Automatic worker-skill pattern

When the reusability gate is met:

RECOVER → REUSE → SPECIFY → BUILD/UPDATE WORKER SKILL → TEST SKILL → RUN MISSION → RETURN ARTIFACTS → DEBO VERIFY/MERGE

The worker-skill creation prompt must include:
- project / mission authority;
- parent DEBO authority;
- exact purpose and trigger;
- recover-before-rebuild rule;
- existing skills to inspect first;
- specialist routing;
- tool/connector boundaries;
- approval firewall;
- truth/provenance requirements;
- agent/swarm rules with fallback;
- token/credit efficiency rules;
- required artifacts;
- test scenarios;
- exact return schema;
- installation/package instructions when supported.

### Structured compiler receipt

Every compiled delegation records:

DEBO_DELEGATION_MODE:
PROJECT_ID:
MISSION_ID:
PRIMARY_WORKER:
WHY_THIS_WORKER:
EXISTING_SKILLS_RECOVERED:
SKILL_ACTION: USE / UPDATE / MERGE / BUILD / NONE
REUSABILITY_REASON:
CONTEXT_REFERENCES:
TOOLS_ALLOWED:
TOOLS_PROHIBITED:
APPROVAL_GATES:
TEST_REQUIREMENTS:
RETURN_ARTIFACTS:
RETURN_SCHEMA:
ROLLBACK:
KNOWN_GAPS:
DEBO_REVIEW_TARGET:

No external worker output becomes project truth until DEBO verifies it.

## Final rule

AI output is a proposal to project truth until DEBO verifies and merges it.


## Zero-Hand-Off-Burden Rule

When another AI/model is better suited to a bounded branch, DEBO must minimize Bobby's manual transfer work.

Order of preference:
1. use a connected plugin/app/MCP/API to pass or retrieve the needed context directly;
2. write/read the handoff through the project's durable GitHub/Drive/Notion location;
3. use browser/computer execution when authorized to move the work;
4. only then give Bobby a copy-paste prompt.

Every outgoing handoff includes a return destination and structured return contract.

If safe automated back-and-forth is possible:
DEBO → specialist AI → durable return location → DEBO verification/merge.

Do not make Bobby shuttle files, repeat facts, or relay intermediate messages unless authentication, authorization, a provider limitation, or genuine ambiguity makes that unavoidable.

## ChatGPT Surface Handoff

Before sending work to another AI, check whether the job is actually better solved natively by:
- ChatGPT Work
- Work + Voice
- Codex
- a connected plugin/app
- Cloud Browser
- a scheduled/event-triggered Work task

Use the external AI only when its material advantage exceeds the handoff cost.

## R149-001 | Verified permission, tenant and cost preflight

**Checkpoint:** \`DEBO-R149-001-PREFLIGHT\`. Update this existing router rather than creating a second plugin router. Before an account-bound, paid, write, browser, or external-AI action, use the **pure, fail-closed** decision helper \`tools/debo_connector_preflight.py\` or follow its equivalent checklist in runtimes where Python cannot execute. This helper neither connects nor authorizes tools.

1. Verify the action exists in this **current runtime**, not merely in the catalog. Record actual supported operation and whether it is metered; static plugin names, MCP annotations and prior installation status are not authorization.
2. Require proof of **current account/identity and exact tool permission**, required OAuth/API scope where applicable, and matching verified tenant before private reads, writes, or external effects. Unknown tenant or unknown scope means BLOCK.
3. Require observed cost bounds and task-specific spending approval before any metered or nonzero-cost action. Missing cost estimate means hold. Auto-reload, vendor billing and new subscriptions always require independent permission.
4. For sends, deployments, deletions and access changes, require separate owner approval **and** any standing restrictions on customer contact, production, sharing, data privacy and minor records. The helper is not authorization to take those actions.
5. Never transmit secrets, customer, minor, personal health or financial information in external-AI/browser handoffs without a distinct, authorized data-release gate and verified destination. Never serialize credentials, account IDs or private record content in preflight logs.
6. If a preferred route fails, try a truly verified, independent **read-only** fallback; do not silently downgrade a write into an unrelated read or treat a read test as a write test.
7. Preserve a concise receipt: \`tool, operation, allowed, reason_codes, source/checkpoint, test_status, next_safe_action\`. Keep \`AUTHORIZED\`, \`TESTED\`, \`INSTALLED\` and \`LIVE\` distinct. If source data may be stale, recheck before any action.

**Test contract:** \`tests/test_debo_connector_preflight.py\` covers public reads, private identity/tenant/scope failures, no-cost versus metered browser runs, unapproved external contact, sensitive data transfers, and permission escalation. Test fixtures are synthetic. Runtime acceptance still requires actual authorized connector readback. This router's output must never be called a real credential or OAuth token validation.
