# Robert Krapil's AI Operating System (AI OS Hub)

**Single source of truth for all AI skills, prompts, and cross-AI sync protocols.**

This repository is automatically synced from Kimi and serves as the central hub that Perplexity, Comet, Claude, and Manus can read via connectors.

---

## Quick Navigation

| What You Need | File |
|---|---|
| **All 67 skills with descriptions** | [`SKILL_REGISTRY.md`](SKILL_REGISTRY.md) |
| **Perplexity starter prompt** | [`PERPLEXITY_STARTER_PROMPT.md`](PERPLEXITY_STARTER_PROMPT.md) |
| **Comet hands-free execution** | [`COMET_MASTER_PROMPT.md`](COMET_MASTER_PROMPT.md) |
| **Meta feedback self-report** | [`META_FEEDBACK_PROMPT.md`](META_FEEDBACK_PROMPT.md) |
| **Strategic roadmap (P0-P6)** | [`ROBERT_AI_OS_ROADMAP_v1.0.md`](ROBERT_AI_OS_ROADMAP_v1.0.md) |
| **Master handoff (all skills)** | [`MASTER_HANDOFF_COMPLETE.md`](MASTER_HANDOFF_COMPLETE.md) |
| **Perplexity handoff brief** | [`PERPLEXITY_HANDOFF_BRIEF.md`](PERPLEXITY_HANDOFF_BRIEF.md) |
| **Comet quick reference** | [`COMET_QUICK_REFERENCE.md`](COMET_QUICK_REFERENCE.md) |
| **Auto-sync protocol** | [`AUTO_SYNC_PROTOCOL.md`](AUTO_SYNC_PROTOCOL.md) |

---

## 6 Domains

1. **ClaimEdge** — Insurance claims investigation, supplements, carrier negotiation
2. **Huuso Exteriors** — Roofing/siding inspection, Xactimate, code compliance
3. **Wrestling** — ICDWA, opponent scouting, tournament prep, Ascend Academy
4. **Buddy Boy Sports** — Baseball team management, tournament discovery
5. **AI Engineering** — Skill building, automation, cross-AI orchestration
6. **Research/Productization** — Market research, product development

---

## .skill Files

| Skill | File | Size |
|---|---|---|
| `robert-master-os` | [`robert-master-os.skill`](https://github.com/ClaimEdge-dev/ai-os-hub/releases) | 68 KB |
| `skill-lifecycle-manager` | [`skill-lifecycle-manager.skill`](https://github.com/ClaimEdge-dev/ai-os-hub/releases) | 17 KB |
| `perplexity-connector-advisor` | [`perplexity-connector-advisor.skill`](https://github.com/ClaimEdge-dev/ai-os-hub/releases) | 14 KB |

> Download .skill files from the [Releases](https://github.com/ClaimEdge-dev/ai-os-hub/releases) page.

---

## How This Works (Auto-Sync Protocol)

1. **Kimi builds/updates a skill** → Pushes .skill + docs to this repo
2. **Perplexity reads via GitHub connector** → Always has latest skills
3. **Notion "AI OS Hub" page** → Human-readable registry with links
4. **Every thread auto-checks** → See [`AUTO_SYNC_PROTOCOL.md`](AUTO_SYNC_PROTOCOL.md)

---

## Last Updated
2026-07-16 — Session continuation with Notion/GitHub sync built.
