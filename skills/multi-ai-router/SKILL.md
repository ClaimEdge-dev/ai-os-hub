---
name: multi-ai-router
description: >
  Routes any DEBO task to the best AI/model/mode/tool stack, then assigns a fallback model
  to cover known weaknesses. Use at complex workflow kickoff, before cross-AI handoffs, when
  a task needs research + build + browser execution, or when an agent stalls, overreaches,
  lacks citations, lacks execution access, or produces weak output.
---

# Multi-AI Router v3.1

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

## Final rule

AI output is a proposal to project truth until DEBO verifies and merges it.
