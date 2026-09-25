---
name: chatgpt-surface-router
description: >
  Mandatory DEBO router for deciding whether Bobby should use Chat, Voice, Dictation, Work,
  Search, Deep Research, Projects, Library, plugins/apps, or a higher reasoning level.
  Triggers at the start of substantial tasks and whenever the current ChatGPT surface is
  inefficient for the requested outcome. Optimizes usage, context, and duplication.
---

# ChatGPT Surface Router v1.0

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

## Usage governor

1. Reuse existing project/thread before creating another.
2. Retrieve only the smallest relevant context.
3. Ask specialist agents for DELTAS, not repeated full project history.
4. Use Instant/Medium for ordinary work.
5. Use High for difficult reasoning, architecture, reconciliation, legal/technical analysis, or high-stakes QA.
6. Use Pro only for the hardest tasks when available and materially useful.
7. Use Search before Deep Research for quick current facts.
8. Use Work only when execution depth justifies it.
9. Use Kimi Swarm only for genuinely independent parallel branches.
10. Preserve results so the same analysis is not paid for twice in time/context.

Consumer ChatGPT usage is governed by plan limits rather than a per-message token bill. Optimize scarce usage and context, not imaginary token accounting.

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
