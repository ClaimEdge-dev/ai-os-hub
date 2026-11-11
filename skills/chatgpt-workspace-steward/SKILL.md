---
name: chatgpt-workspace-steward
description: >
  Keeps Bobby's ChatGPT Projects, chats, files, project sources, Drive/Notion/GitHub mirrors,
  checkpoints, and archives organized. Use at session close, after major builds, during project
  creation or instruction refresh, or during ChatGPT cleanup. Never deletes valuable history without verification.
---

# ChatGPT Workspace Steward v1.1

## Mission

Make ChatGPT Projects navigable without sacrificing recoverability.

## Project instruction refresh

Recover the existing project and relevant conversation before creating either. For a genuine new project, prepare tailored instructions covering goal, canonical sources, tools, privacy, approvals, tests and handoff. On return, compare current instructions with verified evidence and revise only outdated sections. Save through a supported authorized tool and read back the change; otherwise provide one ready-to-paste replacement and mark it NOT SAVED.

Reuse the existing Thread Index and Resume Capsule. Keep the deeper queue internally and show only the top three next actions. Recommend ACTIVE, HANDOFF, MERGE-CANDIDATE or ARCHIVE-CANDIDATE as warranted; reconcile unique evidence and dependencies before proposing a merge or archive. Suggested UI changes are not completed actions.

## Canonical project pattern

PROJECT
- one clear purpose
- project-specific instructions
- icon + color
- project-only memory when isolation is valuable and available
- canonical Drive/Notion/GitHub links
- minimal uploaded files
- command-center chat
- specialist chats only when useful
- Resume Capsule
- Next-10
- archive discipline

## Recommended project visual mapping

Use the closest available ChatGPT project color.

- 🧠 DEBO Core — purple
- 🏢 ClaimEdge — blue
- 💳 Credit Repair — teal/green
- ⚖️ Illinois Record Clearing — gray/slate
- 🚨 JC's Towing — red
- 🎱 Morgan's of Lockport — amber/brown
- 🤼 WrestlingOS — green
- 🏈 Bulldogs / AthleteOS — orange
- ⚾ Buddy Boy Sports — navy/blue

Do not use color as the only identifier; keep the icon + name.

## Chat naming

00 — Command Center — ACTIVE
01 — Intake / Truth
02 — Research / Sources
03 — Build
04 — QA / Red Team
05 — Deliverables
90 — Approval Queue
99 — Archive / Reference

Add lanes only when the project needs them.

## Filing rules

At substantial completion:
1. save durable artifact;
2. store in correct system of record;
3. update Notion/Project Brain;
4. update GitHub if code/schema/Skill/config changed;
5. update Drive for evidence/finals;
6. save reusable ChatGPT response to Project sources when useful;
7. update Resume Capsule / Next-10;
8. mark predecessor SUPERSEDED instead of leaving two apparent masters;
9. classify stale chat as ARCHIVE_CANDIDATE after checkpoint and preservation checks. Only call it ARCHIVED after an authorized ChatGPT UI/API archive action actually succeeds; otherwise give the user a batch archive queue.

## Cleanup rules

Archive, do not delete, when:
- chat contains useful history
- chat is superseded but may explain lineage
- project context may still matter

Delete only when verified:
- empty
- accidental duplicate
- test junk
- contains no unique decisions/evidence
- canonical copy is preserved elsewhere

## Project file strategy

Avoid filling the project upload limit with duplicate binaries.
Prefer:
- canonical Google Drive folder/file links as project sources
- a few essential project-native files
- Library for reusable files
- Drive for large evidence sets and durable deliverables

## Shared project rule

Shared projects are collaboration surfaces, not private-memory dumping grounds.
Only include project-appropriate material.
Use project-only memory/isolation where available.
