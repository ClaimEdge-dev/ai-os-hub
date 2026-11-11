---
name: chatgpt-surface-router
description: >
  Mandatory DEBO router for deciding whether Bobby should use Chat, Voice, Dictation, Work,
  Search, Deep Research, Projects, Library, plugins/apps, or a higher reasoning level.
  Triggers at the start of substantial tasks and whenever the current ChatGPT surface is
  inefficient for the requested outcome. Optimizes usage, context, and duplication.
---

# ChatGPT Surface Router v1.1

## Mandatory Mode Card

At the start of every substantial task, emit a compact internal/user-facing routing card when useful:

MODE: CHAT / VOICE / DICTATION / WORK
REASONING: INSTANT / MEDIUM / HIGH / PRO IF AVAILABLE
TOOLS: SEARCH / DEEP RESEARCH / APPS / FILES / BROWSER / NONE
PROJECT: existing project / new project / no project
WHY: one sentence

Do not clutter trivial replies with a card.

## Surface decision table

| Need | Use |
|---|---|
| quick question, drafting, review, decision, small file task | Chat |
| brainstorm, talk through ideas, hands-free conversation | Voice |
| long spoken prompt that must be editable/precise before sending | Dictation |
| multi-step execution across websites, files, apps, browser, or finished artifacts | Work |
| one current fact or fast public lookup | Search |
| multi-source investigation with citations and a report | Deep Research |
| ongoing domain with repeated context | Project |
| reusable files across chats | Library |
| external account data/actions | Connected app/plugin |
| hard reasoning but not a full autonomous workflow | raise reasoning level before switching surfaces |

## Voice rule

Voice is for conversation and ideation.
Voice transcripts are not guaranteed verbatim.

For:
- exact legal language
- addresses
- dollar figures
- claim numbers
- filenames
- commands
- complicated multi-part instructions

prefer Dictation or typed text so Bobby can review the transcription before sending.

Voice + Work is useful when Bobby wants to direct a longer Work task hands-free.

## Chat vs Work

Stay in Chat when:
- answer can be completed in one/few turns;
- no persistent web navigation is needed;
- no long multi-app sequence is needed;
- user mainly needs reasoning, drafting, review or a decision.

Switch/recommend Work when:
- task needs many steps;
- browser navigation/sign-in/downloads are required;
- multiple connected apps/files must be reconciled;
- a substantial document/spreadsheet/presentation/site must be produced;
- task should continue after Bobby leaves the conversation;
- execution matters more than discussion.

## Search vs Deep Research

Search:
- current fact
- current product/feature
- one or a few sources
- urgent/fast

Deep Research:
- many sources
- source conflicts
- competitive/market/legal/technical research
- documented report
- explicit source-control needs

Do not spend a Deep Research run on a one-answer lookup.

## Project rule

A durable Project is justified when the work:
- will recur;
- has files/instructions that need shared context;
- has several related chats;
- has a stable domain boundary;
- benefits from project-only memory.

Every durable project gets:
- descriptive name
- icon
- color
- project instructions
- canonical source links
- minimal thread map
- Resume Capsule
- archive policy

Project-only memory is preferred for sensitive or contamination-prone domains when the setting is available.

## File/Library rule

Do not repeatedly upload/paste the same file.

If a file is reusable:
- keep it in canonical Drive where appropriate;
- keep/save it in ChatGPT Library when useful;
- add it to the Project only when the whole project benefits from it.

Save high-value ChatGPT responses into the Project sources when they are durable decisions, summaries, specifications, or handoffs.

## Usage governor (v1.1 — existing skill extension, 2026-11-11)

**Owner:** This `chatgpt-surface-router` skill is the canonical ChatGPT-surface and usage policy. `chatgpt-mode-router` supplies supporting mode cues; `multi-ai-router` handles cross-provider routing. Do not create an independent usage-governor skill, dashboard, registry, or scheduled poll.

### Budget and evidence boundaries

- **ChatGPT plan allowance is not an OpenAI API token balance.** Use the actual signed-in ChatGPT usage/settings view for plan-specific allowance, reset, or rate limits, if accessible. Without a direct read, mark them UNKNOWN; never invent numbers or promise extra quota.
- **OpenAI API usage is separately billed/managed.** For authorized API applications, use the matching project's real API usage/cost records and model-specific pricing before calculating dollars. Never use API usage records as proof of ChatGPT Plus consumption.
- Feature eligibility, model availability, token accounting and limits change. Check up-to-date official documentation when the choice materially depends on them; do not hardcode future plan announcements into a current routing decision.
- No API key inspection, account connection, telemetry installation, credit purchase, subscription upgrade, billing change, or export of private usage data without the appropriate authorization. Never put customer or minor information into public metrics.

### Choose the smallest capable route

1. **RECOVER** the current project checkpoint and only the relevant source slices; avoid repasting whole threads, repos, or large file batches.
2. **QUICK/ROUTINE:** Chat + Instant when sufficient. Do not invoke Work, Deep Research or a second AI for a short answer.
3. **MODERATE REASONING:** Use Medium when a better structured decision or comparison is needed. Select High or Extra High (when accessible) for genuinely difficult analysis, security-sensitive review, conflicting evidence or complicated code. Do not downgrade accuracy to save an unmeasured allowance.
4. **ACTION/TOOLS:** Select Work for substantial app/file/browser execution; Codex for repository coding/testing. Surface and tools are chosen by the *work required*, not a claimed token price.
5. **RESEARCH:** Begin with targeted connected-source reads or Search. Use Deep Research only when multiple sources, conflicts, and sustained investigation justify it.
6. **CONTEXT:** Use short source-backed Resume Capsules, file ranges, delta prompts, and cacheable shared instructions when supported. Preserve exact identifiers, approvals, relevant citations, and rollback information. Never compress away material evidence.
7. **DELEGATION:** Send a narrow structured task with a source pointer and return contract. Spawn another worker only when independence, isolation, connector access, or independent QA creates measurable value; do not perform ceremonial multi-agent loops.
8. **RETRIES:** After a repeated failed call, diagnose and change the authorized method once rather than continuing identical requests. Do not bypass approval or security controls to save time.
9. **QA RESERVE:** If Bobby states a finite usage/time budget, provisionally keep about 15–20% for verification and checkpointing unless the task's risk requires more; this is a planning heuristic, **not** an observed account balance.
10. **EVIDENCE:** Record model/surface chosen, task outcome, material tool calls, duplicative retrievals, observed usage/cost *if actually available*, source freshness, tests, and the next action in the existing checkpoint. Label any proposed savings ESTIMATE until measured.

### Routing fallback and acceptance

- If account allowance/plan meter is unavailable: continue on the smallest capable authorized route; report **USAGE UNKNOWN** rather than a fabricated remaining percentage.
- If an observed allowance is low: prioritize high-value completion, concise handoffs and reuse of existing results. Never silently switch tenants, create billable API jobs or reduce necessary safeguards.
- For API agents only, evaluate prompt caching, bounded outputs and usage telemetry with real before/after measurements, cost checks and approved secret handling; these do not alter ChatGPT's included allowance.
- Before adoption, compare three representative DEBO workflows: routine answer, multi-source research, and repo/tool execution. Require completed correct outputs, no new sensitive transfers, no duplicated master skills, and no increase in blocked actions. Measure improvements only with available comparable data.
- See `references/usage-governor-v1.md` for small examples and static contract checks. A passing document check is not proof of runtime routing or a measured decrease in usage.

## Current official references

Projects:
https://help.openai.com/en/articles/10169521-projects-in-chatgpt

Work:
https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex

Cloud browser:
https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt

Voice:
https://help.openai.com/en/articles/20001274-chatgpt-voice

Dictation:
https://help.openai.com/en/articles/12168547-voice-dictation-faq

Deep Research:
https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt

Library:
https://help.openai.com/en/articles/20001052-using-library-to-manage-files-in-chatgpt

Plugins/apps:
https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex
https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt

Memory:
https://help.openai.com/en/articles/8590148-memory-in-chatgpt

Models:
https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt
