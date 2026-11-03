# DEBO skill delta audit (review-only upgrade)

## Where to find the auditor

- **Stable shortcut:** `python tools/debo_skill_delta_audit.py` (compatibility entrypoint; safe for old references).
- **Canonical implementation:** `tools/debo_skill_delta.py` (source of truth; do not rename it or duplicate its logic).
- **Instructions:** `docs/DEBO_SKILL_DELTA_README.md`.
- **Notion comparison source:** AI OS Hub Master Skill Registry → **Skill Registry** database (not the historical summary count).
- `ACTIVE` in either catalog is a *source label*, not proof a skill is installed or operational.

## Purpose
Run the existing DEBO Markdown skill-registry parser and compare against optional **authorized offline exports** from Notion and scheduled-task metadata. Flags cross-registry status conflicts, duplicate names, root skill-source SHA-256 changes, and new/changed/removed skill IDs. No credentials, internet calls, ChatGPT installation, Notion updates, or schedule mutations.

## Use
From the root of an authorized ai-os-hub checkout:

```bash
python tools/debo_skill_delta.py --output /tmp/debo-skill-audit.json
python tools/debo_skill_delta.py --notion /path/to/notion-skills-export.json --automations /path/to/automations-export.json --previous /tmp/previous.json --output /tmp/current.json
python -m unittest discover -s tests -p 'test_debo*.py' -v
```

- The first run is a baseline. The optional prior JSON gives a meaningful incremental comparison.
- Notion export: JSON array or object containing results/rows/skills, each with Name, Status, Version; CSV with those columns is also accepted.
- Automation export: JSON array or object containing automations, each with title and is_enabled. The script checks duplicate titles only; it does **not** enable anything.
- Source SHA-256 discovery covers root `skills/*/SKILL.md` only; project-local source validation remains with the existing project auditors.
- GitHub `ACTIVE` / Notion `ACTIVE` describes **documentation state**, never an installed/runtime agent.
- A missing Notion export makes cross-catalog conflicts unknown, not zero in reality. This project does not expose a live Notion connector to GitHub Actions.
- The script writes output only when `--output` is passed, to the caller-chosen local file. No permanent data changes.

## Promotion gates
Use a GitHub review branch, run the repo's existing CI and synthetic tests, inspect real-source conflicts, then approve promotion. Keep 403 Google Sheets and 404 event-trigger capability separate. Do not create another ChatGPT scheduler or merge the unreviewed R9/PR #17 as a side effect.

Related: `tools/debo_registry_audit.py`, `tools/debo_bootstrap_check.py`, `governance/runtime-briefs/DEBO.md`, and the existing Notion 07 ThreadOps checkpoint.
