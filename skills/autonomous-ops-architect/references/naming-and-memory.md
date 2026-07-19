# Naming Standard & Memory Objects

Read during Phase 3 (Naming Recommendations) and Phase 12 (Memory & Context Engineering).

## Contents
- Unified Naming Standard
- Long-Term Memory Objects
- Retrieval Priority & Token Discipline

## Unified Naming Standard

Pattern: `[DOMAIN]_[Subject]_[Descriptor]_[YYYY-MM or version]`

| Domain | Prefix | Examples |
|---|---|---|
| ClaimEdge Core | `CE` | `CE_Coffey-061609752_MasterPacket_2026-07`, `CE_Skill_SupplementWriter_v3` |
| Wrestling App Core | `WR` | `WR_ChaseKrapil_OpponentDB_2026`, `WR_App_MasterBuild_v2` |
| Buddy Boy Sports | `BBS` | `BBS_ResearchHub_2026`, `BBS_Tournament_11U_Summer2026` |
| AI OS / Automation | `OS` | `OS_Skill_OpsArchitect_v1`, `OS_Prompt_MasterConstitution_2026-07` |
| Reference Library | `REF` | `REF_Xactimate-Chicago-Pricing_2026`, `REF_IL-Statutes_215ILCS5-155` |
| Archive | `ARC` | `ARC_Legacy-Exteriors_BrandSuite_2025`, `ARC_Prompt_OldMaster_v1` |
| Trash Pending Review | `TPR` | `TPR_Untitled-thread-dup_2026-07` |

Notion pages use the human-readable form: `CE | Coffey Claim — Final Packet`, `OS | Memory Core`.

Rules:
- No spaces in file/repo names; hyphens within segments, underscores between segments.
- Threads/pages get human-readable titles but must start with the domain prefix.
- Version bumps: `v1 → v2` for content changes; date suffix for point-in-time artifacts.
- Never keep names like `Untitled`, `Copy of`, `final_FINAL2`. Rename on sight during audits — but only after the Phase 5 plan is approved.
- Ambiguous items: keep current name, tag `NEEDS REVIEW`, ask user once in a batch list (never one-by-one).

## Long-Term Memory Objects

Maintain these 10 objects. Canonical home: **OS | Memory Core** page in Notion (under OS | AI OS Hub). Fallback: markdown files in `/mnt/agents/output/memory/` or a GitHub `memory/` folder.

| Object | Holds | Update trigger |
|---|---|---|
| PROJECT_CHARTER | Mission, domains, constitution version | Constitution change |
| DOMAIN_MEMORY (ClaimEdge / Wrestling / BBS / AI OS) | Standing facts per domain | Any domain decision |
| TASK_STATE | Active tasks, owners, blockers | Every session end |
| DECISION_LOG | Decisions + rationale + date | Any non-obvious decision |
| CHANGE_LOG | Every rename/move/archive executed | Phase 5 execution |
| CONNECTOR_REGISTRY | Plugins live, scopes, last audit date | Phase 0 and Phase 6 |
| NAMING_STANDARD | This document's table, versioned | Naming rule change |
| WEEKLY_COMPACT_SUMMARY | 1-page rollup of the week | Weekly or session 5+ |
| RISK_REGISTER | Security/governance risks with severity | Phase 15 or any P0 find |
| RELEASE_NOTES | Version bumps of apps/skills/prompts | Any merge/deploy |

## Retrieval Priority & Token Discipline

1. Current instruction
2. PROJECT_CHARTER
3. Relevant DOMAIN_MEMORY
4. TASK_STATE
5. Relevant DECISION_LOG / CHANGE_LOG
6. Current session evidence
7. Older chats — only if nothing above answers it

Keep 30–50% token headroom for tool outputs and revisions. Prefer fetching one memory object over pasting all ten. When a memory update and a token budget conflict, update TASK_STATE and DECISION_LOG first — they prevent the most rework.
