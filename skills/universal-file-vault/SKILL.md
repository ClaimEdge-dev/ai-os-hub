---
name: universal-file-vault
description: Universal file sync, archive, and deployment system v2.0 — the ONE vault for all domains. Auto-discovers all files created during Kimi sessions and routes them to the right home — Notion (documents, pages, databases, claim/tournament hubs), GitHub (code, skills, templates, versioned artifacts), Neon/Supabase (structured data as SQL/CSV). Handles ClaimEdge deliverable deployment, claim archiving with shareable links, deployment status tracking, and cross-session memory sync. Triggers when user says "upload everything", "save to Notion", "push to GitHub", "vault my files", "sync files", "archive session files", "deploy", "archive this claim", "backup my work", "save everything", or at the end of ANY session with created files. Also triggers when user wants to organize, catalog, persist outputs across sessions, or recover previous work after a reset.
---

# Universal File Vault v2.0

Domain-agnostic file sync system. Every file created in a session gets routed to its canonical home — with duplicate detection, tracking, and a sync log.

> **v2.0 consolidation:** Absorbs claimedge-vault-system (ClaimEdge archiving + quick-rebuild templates), claimedge-auto-deploy (per-claim deployment + shareable links + status tracking), claimedge-session-memory (session state persistence). Canonical memory home: OS | Memory Core page in Notion.

## Core Workflow: Scan → Classify → Route → Upload → Log

```
1. SCAN — discover files in /mnt/agents/output/ and session workspace
2. CLASSIFY — by type AND domain (CE / WR / BBS / OS / REF)
3. ROUTE — map to destination per the routing table
4. UPLOAD — via live connectors; mark BLOCKED ones with fallback (never fabricate)
5. LOG — append to the vault log in Memory Core (file → destination → link → timestamp)
```

## Routing Table

| File type | Canonical home | Fallback if blocked |
|---|---|---|
| Documents, reports, claim packets | Notion (domain hub page) | Markdown files + import index |
| Skills (.skill source), code, templates | GitHub `ai-os-hub` (or domain repo) | .skill/zip in `/mnt/agents/output` |
| Structured data (claims, wrestling records) | Neon (data-only) / Supabase (needs auth/storage) | SQL schema + CSV seed files |
| Brand/design assets | Canva | HTML/markdown with brand spec |
| Session state, decisions, changelog | OS | Memory Core (Notion) | `/mnt/agents/output/memory/` markdown |

## ClaimEdge Deploy Mode (from auto-deploy)

When a ClaimEdge deliverable is created: organize by claim (`CE_[Client]_[Claim#]`), upload documents to the claim's Notion hub, push templates/code to GitHub, generate shareable links, and report deployment status per item (✅ synced / ⏸ blocked + fallback).

## Session Memory Mode (from session-memory)

At session end (or on "save context"): update TASK_STATE (active tasks, blockers, next step) and DECISION_LOG in Memory Core. At session start with existing work: read TASK_STATE first and recap before doing anything.

## Duplicate Detection

Before uploading, check the vault log: if the same filename+domain synced in the last 7 days, ask once — update-in-place or new version. Never create `final_v2_FINAL` duplicates in Notion/GitHub.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| claimedge-vault-system | Quick-rebuild templates, cross-session recovery for ClaimEdge builds |
| claimedge-auto-deploy | Per-claim organization, shareable links, deployment status tracking |
| claimedge-session-memory | Running state document, session start recovery, post-action updates |
