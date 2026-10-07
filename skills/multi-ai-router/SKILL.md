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
