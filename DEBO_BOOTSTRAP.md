# DEBO Runtime Bootstrap
Before executing work in any DEBO master or sister-brain project:
1. Load the current generated brief for the resolved project under `governance/runtime-briefs/`, with `DEBO.md` for the master. Follow the [single canonical runtime bootstrap](governance/DEBO_RUNTIME_BOOTSTRAP_v2.md) for freshness, fallback and compact golden rules. With a checkout, `python tools/debo_bootstrap_check.py --brief --project DEBO` generates a view on demand. The [JARVIS policy](debo/policies/DEBO_JARVIS_AUTONOMOUS_V2.md) remains authoritative; load detailed policies for their relevant triggers.
2. For skill inventory or registry conflict work, use `tools/debo_skill_delta.py` (canonical) or `tools/debo_skill_delta_audit.py` (stable shortcut), guided by `docs/DEBO_SKILL_DELTA_README.md`. Compare `SKILL_REGISTRY.md` with the Notion **Skill Registry database** under the AI OS Hub; older summary counts are historical. These tools are read-only and not an automatic connector.
3. Load only the selected project profile and latest verified private checkpoint; a static profile is not live project state. Do not assume repository policy auto-injects into every chat.
4. Apply inherited defaults and project adapter; preserve approval boundaries.
5. Record evidence, decisions, version, tests, and next action.
6. For future projects, add a project adapter without duplicating master rules.
This bootstrap is persistent in GitHub, not proof of activation in external applications.
