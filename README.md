# Robert Krapil's AI Operating System (AI OS Hub)

**Single source of truth for all AI skills, prompts, and cross-AI sync protocols.**

This repository stores the shared source that connected AI tools can load through their supported startup paths. Repository updates alone do not establish automatic sync or runtime activation.

---

## Quick Navigation

| What You Need | File |
|---|---|
| **Start DEBO or a sister brain: compact golden rules** | [`DEBO runtime bootstrap`](governance/DEBO_RUNTIME_BOOTSTRAP_v2.md) |
| **Skill descriptions and recorded source status** | [`SKILL_REGISTRY.md`](SKILL_REGISTRY.md) |
| **Perplexity starter prompt** | [`PERPLEXITY_STARTER_PROMPT.md`](PERPLEXITY_STARTER_PROMPT.md) |
| **Comet hands-free execution** | [`COMET_MASTER_PROMPT.md`](COMET_MASTER_PROMPT.md) |
| **Meta feedback self-report** | [`META_FEEDBACK_PROMPT.md`](META_FEEDBACK_PROMPT.md) |
| **Strategic roadmap (P0-P6)** | [`ROBERT_AI_OS_ROADMAP_v1.0.md`](ROBERT_AI_OS_ROADMAP_v1.0.md) |
| **Master handoff (all skills)** | [`MASTER_HANDOFF_COMPLETE.md`](MASTER_HANDOFF_COMPLETE.md) |
| **Perplexity handoff instructions** | [`docs/PERPLEXITY_HANDOFF_PROMPT.md`](docs/PERPLEXITY_HANDOFF_PROMPT.md) |
| **Comet quick reference** | [`COMET_QUICK_REFERENCE.md`](COMET_QUICK_REFERENCE.md) |
| **Auto-sync protocol** | [`AUTO_SYNC_PROTOCOL.md`](AUTO_SYNC_PROTOCOL.md) |

---

## 6 Domains

1. **ClaimEdge** — Insurance claims investigation, supplements, carrier negotiation
2. **ClaimEdge — Exteriors** — Roofing/siding inspection, Xactimate, code compliance (legacy "Huuso" brand retired 2026-07-19 — everything is ClaimEdge now)
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

## How This Works (Source and Runtime Loading)

1. Save approved source updates in this repository.
2. Start supported sessions from the [canonical compact bootstrap](governance/DEBO_RUNTIME_BOOTSTRAP_v2.md), selected project profile and latest authorized checkpoint.
3. Use the Notion "AI OS Hub" and [`AUTO_SYNC_PROTOCOL.md`](AUTO_SYNC_PROTOCOL.md) as linked references; refresh material stale or conflicting evidence.
4. Verify loading and execution in each runtime before claiming installation or automatic sync.

---

## Last Updated
2026-11-02 — Compact golden-rule startup, automatic master/project brief regeneration and explicit runtime-loading limits.
2026-07-19 — Huuso→ClaimEdge rebrand scrubbed workspace-wide; legacy brand retired. 17 Notion pages renamed to domain prefixes; autonomous-ops-architect skill added.
2026-07-16 — Session continuation with Notion/GitHub sync built.


## DEBO v2 canonical activation

For every DEBO and sister-brain task, begin with the compact golden rules in the [DEBO runtime bootstrap](governance/DEBO_RUNTIME_BOOTSTRAP_v2.md), selected project profile and current authorized checkpoint. Load the full [execution standard](governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md) and other policy detail for their relevant triggers. Use the [profile template](governance/SISTER_BRAIN_PROFILE_TEMPLATE_v2.md) when creating an authorized new project, not on every startup. The [activation checklist](governance/DEBO_INSTALLATION_CHECKLIST_2026-10-19.md) documents runtime verification.

Treat these as canonical repository instructions, not proof of automatic loading into ChatGPT or other AI runtimes. Only mark an integration installed after its own startup and execution tests succeed. Recover before rebuild, complete safe reversible steps without redundant approval, maintain project isolation, and record verified outcomes.

Source changes on `main` trigger the [runtime-brief auto-update workflow](.github/workflows/debo-runtime-briefs.yml), which regenerates the master and thirteen project-specific derived views in `governance/runtime-briefs/`. This is automatic repository maintenance. Each external AI runtime still needs a supported loader and its own activation evidence.
