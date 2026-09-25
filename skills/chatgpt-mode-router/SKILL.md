---
name: chatgpt-mode-router
description: >
  Tells Bobby when to use Chat, Work, Voice, Work+Voice, Codex, Temporary Chat, or a Project chat.
  Optimizes context, usage, connected-app execution, and handoffs. Trigger on every substantial
  DEBO task, mode confusion, long build, voice idea dump, browser/app workflow, or artifact mission.
---

# ChatGPT Mode Router v1.0

## Rule

Give a mode cue when the surface materially changes the outcome.
Do not nag on trivial questions.

## Routing

### CHAT
Best for:
- fast questions
- decisions
- planning
- writing/rewrite
- small edits
- review/QA
- orchestrating other tools
- short current-info lookups

### WORK
Best for:
- multi-step execution
- connected apps/files
- cloud browser
- signed-in web workflows
- creating/editing documents, spreadsheets, presentations, reports
- long research/build missions
- tasks that may continue after Bobby leaves
- scheduled/event-triggered work where available

### VOICE
Best for:
- idea dumps
- rapid intake
- hands-free conversation
- dyslexia-friendly capture
- brainstorming / clarifying
- reading through options verbally

Use Advanced Voice only when supported screen/video sharing is actually needed.

### WORK + VOICE
Best for:
- talking through a substantial build while Work uses tools/apps/files/browser
- starting a Work mission by voice and letting it continue in text

### CODEX
Best for:
- software development
- repositories
- local folders
- terminals / code changes
Use desktop when local repo access is needed.

### PROJECT CHAT
Use whenever work belongs to a durable project.
Keep the work inside that Project Brain so files, instructions, and history stay aligned.

### TEMPORARY CHAT
Use for:
- disposable experiments
- sensitive one-off discussion that should not create new memory
- testing a prompt before promoting it
Save it only when the work becomes worth preserving.

## Usage/context efficiency

- Recover, don't repaste.
- Prefer compact project instructions + linked sources.
- Save durable responses to project sources.
- Keep large artifacts in Drive/Library/Notion/GitHub.
- Use Resume Capsules instead of dragging huge threads forever.
- Move eligible old chats into the correct Project.
- Archive stale chats after checkpointing.
- One Work mission > many tiny agent missions when the goal is one deliverable.
- Kimi Swarm only for truly independent branches.
- Do not call the same connector repeatedly without a freshness reason.

## Default cue format

MODE: CHAT / WORK / VOICE / WORK+VOICE / CODEX
WHY: one short sentence
THEN: execute or give the exact handoff
