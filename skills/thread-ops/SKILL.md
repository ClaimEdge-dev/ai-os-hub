---
name: thread-ops
description: Thread operations system v2.0 (formerly thread-handoff-manager) — the single skill for thread audits, sidebar organization, context preservation, and cross-session handoffs. Scans current and recent threads, classifies each (continue / save & close / archive / merge), auto-generates descriptive names for unnamed threads, builds a priority dashboard with next-step recommendations, creates master project files and new-thread starter packs, monitors context limits, and prevents error propagation and data loss between sessions. Triggers when user says "audit my threads", "organize threads", "rename threads", "what should I do with this thread", "clean up threads", "thread status", "sidebar is messy", "save context", "handoff", "where were we", "continue later", "start a new thread", "where did we leave off", "catch me up", or references previous work without specific context. Also triggers at session end with unfinished work and when context preservation between AI sessions is needed.
---

# Thread Ops v2.0

One skill for the whole thread lifecycle: audit → decide → name → hand off → recover.

> **v2.0 consolidation:** Absorbs thread-audit-manager (audit + naming dashboard) and session-context-preserver (save/recover state). Renamed from thread-handoff-manager.

## Mode 1: Thread Audit ("audit my threads")

1. Scan current/recent threads (titles, message counts, last activity, domain).
2. Classify each: **CONTINUE** (active work) / **SAVE & CLOSE** (deliverables done) / **ARCHIVE** (reference only) / **MERGE** (duplicate of another thread).
3. Auto-name anything titled "Untitled", "New chat", or gibberish — pattern: `[DOMAIN] | [Subject] — [Status]` per the naming standard.
4. Output a dashboard: table of threads, priority rank, next step for each. Batch questions — never ask one thread at a time.

## Mode 2: Handoff ("save context" / ending a session)

1. Snapshot: goal, decisions made, deliverables produced, open items, next step.
2. Update TASK_STATE + DECISION_LOG in OS | Memory Core (Notion).
3. Generate a **starter pack** for the next thread: 5-line brief + links to Memory Core, relevant registry rows, and deliverable files.
4. Flag any unverified claims that must not propagate to the next session.

## Mode 3: Recovery ("where were we" / new session with prior work)

1. Read TASK_STATE and DECISION_LOG from Memory Core FIRST.
2. Recap in ≤8 lines: where we were, what's done, what's next.
3. Confirm before resuming — memory may be stale.

## Mode 4: Context Guard (during long sessions)

- Watch for context bloat: warn at ~70% with a handoff offer.
- Watch for rebuild loops: if the user starts redoing finished work, show the existing deliverable.
- Error quarantine: mark disputed/unverified data UNVERIFIED so it never silently becomes "fact" in a later thread.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| thread-audit-manager | Thread scanning, continue/close/archive/merge classification, auto-naming, priority dashboard |
| session-context-preserver | State auto-save, handoff briefs, rebuild-loop prevention, session-start recovery |
