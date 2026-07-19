# Connector Registry & Fallback Playbooks

Read during Phase 0 (Environment Check) and Phase 6 (Connector/Plugin Audit).

## Contents
- Phase 0 Environment Check Procedure
- Capability Map
- Overlap Resolution Rules
- Blocked-Fallback Playbooks

## Phase 0 Environment Check Procedure

1. List which plugin MCP servers are actually live in the current session (check the session's tool list — never assume from past sessions).
2. For each live connector, run one cheap read-only probe before relying on it:
   - Notion: search for a known page
   - GitHub: `get_me` or list repos
   - Neon: `list_projects`
   - Supabase: `list_projects`
   - Canva: `search-designs` with a broad term
3. Record results in CONNECTOR_REGISTRY format: connector, status (LIVE/DEGRADED/BLOCKED), scope observed, probe timestamp.
4. For every BLOCKED connector, state the fallback from the playbooks below and continue — never stall the whole run on one missing connector.

## Capability Map

| Connector | Best at | Avoid for |
|---|---|---|
| **Notion** | Pages, wikis, databases, project boards, memory objects, claim/tournament hubs, audit logs | Large binary files, code versioning |
| **GitHub** | Skills (`.skill` source), templates, code, HTML apps, version control, release notes | Frequently-edited documents, relational data |
| **Neon** | Structured relational data: wrestling DB, claims records, rankings. Branching for safe schema migrations | Auth, file storage, serverless functions |
| **Supabase** | Full-stack needs: Postgres + auth + storage + edge functions (app backends, e.g. Level Up Wrestling) | Simple data tables Neon already holds |
| **Canva** | Brand kits, presentations, social graphics, client-facing design from templates | Precise data reports, code artifacts |
| **interactive-research-report-en** (skill) | Editorial-grade interactive report websites from deep reports | Quick internal notes, raw data dumps |

## Overlap Resolution Rules

- **Neon vs Supabase**: if the need is data-only (tables, SQL, rankings), use Neon. If the need includes auth, file storage, or edge functions, use Supabase. Never maintain the same table in both — pick one canonical home per dataset and record it in CONNECTOR_REGISTRY.
- **Notion vs GitHub for skills**: GitHub is canonical for skill source; Notion holds the human-readable catalog/index of what exists.
- **Notion vs local files for memory objects**: Notion is canonical; local markdown under `/mnt/agents/output/memory/` is the session fallback and gets synced when Notion is live.
- **GitHub repo settings (rename/archive/description)** are NOT available via the current toolset — give the user the exact click path (repo → Settings → Rename / Archive) instead of fabricating completion.

## Blocked-Fallback Playbooks

- **Notion blocked** → deliver markdown files with a `NOTION_IMPORT.md` index the user can paste/import; queue a sync task for when the connector is live.
- **GitHub blocked** → package deliverables (`.skill`, zips) to `/mnt/agents/output/`; include a `git-push-commands.sh` script the user can run later.
- **Neon/Supabase blocked** → deliver SQL schema files + CSV seed data + a `run-order.md`; never fabricate that rows were inserted.
- **Canva blocked** → deliver HTML/markdown with an explicit brand spec block (colors, fonts, logo notes) the user can hand to Canva manually.
- **Browser actions blocked** → write the exact click-path instructions as a numbered manual runbook.

Always label fallback output with: `FALLBACK DELIVERY — connector X was BLOCKED at [timestamp]; sync pending`.
