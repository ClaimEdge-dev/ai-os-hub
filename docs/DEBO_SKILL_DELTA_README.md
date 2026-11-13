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

## Opt-in project-adapter source inventory (R144)

Run `python tools/debo_skill_delta.py --include-projects --output /tmp/debo-all-skill-sources.json` to include existing `projects/*/skills/*/SKILL.md` adapters alongside root skills. The default remains root-only for backward compatibility. The read-only scanner emits stable scoped IDs such as `project/jcs-towing/jct-dispatch-intake`, source paths and SHA-256 fingerprints. Identically named skills in two projects stay separate; they cannot shadow a root DEBO Core skill. Synthetic regression tests cover opt-in behavior, scope separation and changed-source detection.

This is a source file inventory only. It does not activate skills in ChatGPT, Kimi, Notion or other systems, and does not prove tenant authorization, production installation or workflow testing. The source glob intentionally does not include standalone `plugins/` packages or nested legacy ClaimEdge skills; keep those separate until the canonical auditor explicitly adopts their scope. Reconcile new evidence with the *existing* Notion Skill Registry and R141 crosswalk; do not create another register or fill blank source links by guessing.


## R149-002 | Optional SKILL.md metadata preflight

Run: python tools/debo_skill_delta.py --include-projects --validate-contracts --output /tmp/debo-skill-contracts.json

The existing canonical auditor's optional contract_audit block checks basic Agent Skills SKILL.md metadata and reports PASS/REVIEW; the default report is unchanged. Required fields are name and description; license is optional. A lightweight stdlib reader cannot fully parse complex YAML, so those cases are explicitly marked REVIEW and should use the official skills-ref validator in an isolated authorized environment. Legacy missing headers remain review candidates, not an installed-skill failure. This command reads files and writes only the specified local report; no Notion or GitHub mutations, deployments or account permissions.
Source: https://agentskills.io/specification .

## Optional Notion identity completeness review

Add `--audit-identities` alongside an authorized `--notion` export to include an
`identity_audit` block. It retains every exported row, including blank names and
duplicate titles, and reports missing IDs/links, duplicate declared IDs, local
source scope gaps and mismatched source-link paths. The default report remains
unchanged when this flag is absent.

Only an explicitly supplied, unique `skill_id` can look up a scanned local path;
the review never invents IDs from titles or URLs. A matching source pointer is
not verification of the linked bytes, version, tenant permission or installed
runtime. Out-of-scope repositories and unscanned packages require separate source
recovery; they are not declared nonexistent. Keep exports and reports in the
owning private project, outside public GitHub commits. This mode does not update
Notion, resolve aliases, promote statuses or install anything.
