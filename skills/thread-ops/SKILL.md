---
name: thread-ops
description: Thread operations system v2.1 (formerly thread-handoff-manager) — the single skill for thread audits, sidebar organization, context preservation, and cross-session handoffs. Scans current and recent threads, classifies each (continue / save & close / archive / merge), auto-generates descriptive names for unnamed threads, builds a priority dashboard with next-step recommendations, creates master project files and new-thread starter packs, monitors context limits, and prevents error propagation and data loss between sessions. Triggers when user says "audit my threads", "organize threads", "rename threads", "what should I do with this thread", "clean up threads", "thread status", "sidebar is messy", "save context", "handoff", "where were we", "continue later", "start a new thread", "where did we leave off", "catch me up", or references previous work without specific context. Also triggers at session end with unfinished work and when context preservation between AI sessions is needed.
---

# Thread Ops v2.1

One skill for the whole thread lifecycle: audit → decide → name → hand off → recover.

> **v2.0 consolidation:** Absorbs thread-audit-manager (audit + naming dashboard) and session-context-preserver (save/recover state). Renamed from thread-handoff-manager.

## Mode 1: Thread Audit ("audit my threads")

1. Recover thread metadata only from authorized, actually accessible chat/project sources and the current registry; missing ChatGPT sidebar metadata remains UNVERIFIED. Never claim inaccessible history was scanned.
2. Classify each: **CONTINUE** (active work) / **SAVE & CLOSE** (deliverables done) / **ARCHIVE** (reference only) / **MERGE** (duplicate of another thread).
3. Recommend canonical names for unnamed/duplicated threads using `[DOMAIN] | [Subject] — [Status]`. Actually rename ChatGPT conversations only if an authorized UI/API mutation tool exists and succeeds; otherwise save an exact rename queue.
4. Output a dashboard: table of threads, priority rank, next step for each. Batch questions — never ask one thread at a time.

## Mode 2: Handoff ("save context" / ending a session)

1. Snapshot: goal, decisions made, deliverables produced, open items, next step.
2. Update the current canonical project TASK_STATE / Decision Log / Resume Capsule in its designated source of truth (Drive/Notion/GitHub as relevant); do not require Notion when it is not canonical.
3. Generate a **starter pack** for the next thread: 5-line brief + links to Memory Core, relevant registry rows, and deliverable files.
4. Flag any unverified claims that must not propagate to the next session.

## Mode 3: Recovery ("where were we" / new session with prior work)

1. Read the latest canonical project checkpoint and decision log first, from the project's actual approved source.
2. Recap in ≤8 lines: where we were, what's done, what's next.
3. Resume safe reversible work automatically when the current objective and verified checkpoint are clear. Ask only for truly missing critical facts or protected approval-gated actions; mark stale sources for re-verification.

## Mode 4: Context Guard (during long sessions)

- Watch for context bloat: warn at ~70% with a handoff offer.
- Watch for rebuild loops: if the user starts redoing finished work, show the existing deliverable.
- Error quarantine: mark disputed/unverified data UNVERIFIED so it never silently becomes "fact" in a later thread.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| thread-audit-manager | Thread scanning, continue/close/archive/merge classification, auto-naming, priority dashboard |
| session-context-preserver | State auto-save, handoff briefs, rebuild-loop prevention, session-start recovery |

## Mode 5: Prevent clutter continuously (R7)

- Before a new thread: recover existing objective and classify SAME TASK / REQUIRED DEPENDENCY / SEPARATE BRANCH / FUTURE IDEA.
- Default to one canonical active execution thread per objective and one best next action. A project-wide WIP cap is a review signal, not an absolute ban on justified parallel work.
- During scope creep, finish the current objective and park unrelated discoveries; never drop them from the backlog.
- After substantial completion: source/readback → QA → audit receipt → checkpoint → classifiy STAY / MERGE / REFERENCE / ARCHIVE_CANDIDATE.
- An ARCHIVE_CANDIDATE is not a confirmed archived chat. Require proof that unique decisions, artifacts and open items survive in canonical sources. Never auto-delete and never claim ChatGPT archive UI was mutated without a supported tool and successful response.
- Deduplicate by objective, source and content, not just title. Maintain a lightweight archive index with canonical replacement and reopen conditions.
- Staleness: preserve true last-touch only when returned by an authoritative source. Otherwise record UNKNOWN and use last verified checkpoint time as a different field.
- Time windows: default to delta sync. Use focused 48-hour changes, 14-day material reconciliation and targeted 30-day lineage only when full recovery is justified and accessible. Do not create a new historical rescan when current verified checkpoints already cover those periods.
- Reopen archived/reference threads only when unique necessary evidence was missed or canonical successor failed. Otherwise continue canonical thread.
- Prompt dedupe and rule dedupe route to existing Skill Registry and governance queues, never another master thread.
- Report execution truth: VERIFIED BY LIVE TOOL, VERIFIED DOCUMENT, HISTORICAL CLAIM, UNVERIFIED, BLOCKED. A thread label is not proof of archival action.

## Accountability
Owner: DEBO Workspace Steward; Specialist: Thread Ops; QA: Proof; Records: Vault; Approval: Bobby for destructive or security-impacting actions. 
