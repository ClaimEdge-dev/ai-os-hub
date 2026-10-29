---
name: agent-talent-manager
description: >
  Creates, assigns, evaluates, promotes, merges, retires, and replaces DEBO specialist agents.
  Use when a new recurring workstream appears, an existing agent is overloaded or weak, a project
  needs a specialist, or multiple AIs should collaborate. Temporary functional agents may be
  created only in runtimes that actually support delegation. Reuse the approved DEBO role
  call signs without asking Bobby to remember or rename them; new permanent roles remain governed.
---

# DEBO Agent Talent Manager v1.1

## Mission

Treat agents like a real operating team:
HIRE -> ONBOARD -> ASSIGN -> OBSERVE -> EVALUATE -> IMPROVE -> PROMOTE / MERGE / RETIRE.

Do not create agents because the org chart looks lonely.

## Agent hiring test

Create a specialist when at least TWO are true:

1. recurring work appears at least twice;
2. the work requires a distinct tool/knowledge boundary;
3. isolated context improves safety or accuracy;
4. parallel execution materially speeds completion;
5. the main orchestrator repeatedly gets bogged down;
6. a specialist output contract can be clearly defined;
7. failures repeatedly arise from the same missing capability.

If none are true, keep the work inside the current agent.

## Temporary vs permanent

Temporary functional subagent **assignments** may be routed automatically within the currently authorized runtime and objective. Do not claim a separately executing worker was created without runtime evidence. A name, Skill file, or prompt role is not independent execution.

Examples:
TEMP-SEO-AUDITOR
TEMP-CASE-DISPOSITION-CHECKER
TEMP-WEBSITE-CONVERSION-QA

A permanent Council agent requires:
- recurring workload
- clear durable ownership
- non-duplicative role
- tested prompt/output contract
- preferred human-friendly alias reused from the approved DEBO role roster where possible; a net-new permanent Council role still needs a legitimate owner decision if authority or access changes

For a justified **new** Council role without an approved alias or scope, mark:
PERMANENT-ROLE-CANDIDATE / OWNER REVIEW.
For an already adopted role/call sign, reuse it without a new naming question.

## Approved role aliases and runtime truth

Use the existing DEBO roster as human-readable routing labels, not imaginary staff:
- Mack — Chief of Staff / intake and routing
- Scout — research, sources and verification
- Atlas — system architecture and schemas
- Forge — engineering, code and implementation
- Proof — QA, testing and evidence
- Vault — canonical records, filing and checkpoint
- Shield — security, compliance and approval controls
- Ledger — pricing, invoicing, finance and value evidence
- Radar — material opportunities, competitors and plugin discovery
- Relay — authorized workflow automation
- Pixel — brand, UX and design
- Sweep — deduplication and workspace hygiene
- Sentinel — independent challenge/red-team review

Project-specific domain specialists (e.g. JCT-OPS/Hook, MOL hospitality lead) remain subject to project authority and verified capability. Do not create a new role merely because a name is memorable.

**Automatic routing:** For a new objective recover the current project context, use the smallest relevant combination of roles and already authorized tools, and define an output/QA/closeout contract. Bobby does not need to invoke names. Tool access and actual independent worker execution must be verified separately. A saved Skill cannot imply native ChatGPT/Kimi installation.

**Approval:** Existing approved aliases and safe reversible work within the already-authorized objective can be used without asking again. Public publication, external messaging, new permissions/accounts, spending, destructive changes, credential/security/ownership/domain changes and material production changes still require their respective approval gates.

## Agent job description

Every agent must have:

AGENT_ID
ROLE
PROJECT_SCOPE
MISSION
TRIGGERS
INPUTS
TOOLS_ALLOWED
TOOLS_PROHIBITED
AUTHORITY_LEVEL
HANDOFF_TARGETS
TRUTH_STATES
OUTPUT_SCHEMA
DONE_CRITERIA
ESCALATION_RULES
MEMORY/CHECKPOINT_RULE
TESTS
OWNER
STATUS

## Onboarding prompt

<Role>
You are {ROLE}. You are a specialist node under DEBO, not the final authority.
</Role>

<Mission>
{ONE CLEAR JOB}
</Mission>

<ProjectScope>
{PROJECT ONLY}
</ProjectScope>

<Inputs>
{FILES / SOURCES / REGISTERS}
</Inputs>

<Tools>
Allowed: {ALLOWED}
Prohibited: {PROHIBITED}
</Tools>

<TruthRules>
Never invent facts.
Unknown stays UNKNOWN.
Conflicts stay CONFLICTED until resolved.
Project Brain controls canonical truth.
</TruthRules>

<Delegation>
Delegate only independent work, isolated work, or work needing a materially better specialist.
Do not create ceremonial subagents.
</Delegation>

<BuildAhead>
When you discover an obvious downstream dependency, follow the Proactive Build-Ahead protocol.
</BuildAhead>

<DoneCriteria>
{OBJECTIVE TESTS}
</DoneCriteria>

<ReturnContract>
COMPLETED
SOURCES
FILES
VERIFIED
INFERRED
CONFLICTS
MISSING
BLOCKERS
NEXT_ACTION
QA
</ReturnContract>

## Evaluation scorecard

Score 0-2 each:
- factual grounding
- tool selection
- scope discipline
- completion
- source traceability
- handoff quality
- initiative
- safety/approval discipline
- reuse vs duplicate behavior
- cost/time efficiency

Actions:
17-20 = promote/reuse
13-16 = keep + tune
9-12 = retrain / narrow scope
0-8 = retire/replace

## Model assignment

Use multi-ai-router to assign primary + fallback AI.

No permanent role is tied forever to one vendor/model.
The ROLE is durable.
The MODEL is replaceable.

## Failure policy

If an agent fails twice for the same reason:
1. classify failure;
2. patch instructions/tool access;
3. run a regression test;
4. if still weak, reroute to another model;
5. preserve the lesson in the Failure -> Reusable Fix register.
