# DEBO-00 to DEBO-05 | Dashboard v0.3 Integration Handoff

Mission: DEBO-DASH-005 | Date: November 3, 2026 | Status: REVIEW CANDIDATE.
This is an integration contract, not a deployed dashboard, second database, new plugin, or running sync.

## Ownership and baseline
- DEBO-00: priorities, permissions, selection of plugins/skills, task and project status, release approval and verified checkpoint.
- DEBO-05: incremental edits to the CURRENT dashboard HTML, test suite, accessibility and mobile QA, versioned artifact and rollback.
- Exact existing Library source: DEBO_Progress_Command_Center_v0.2.2_Guided_iPhone.html (141267 bytes, Nov 3, offline HTML). Obtain authorized original bytes in the dashboard build thread or Work before editing. Preserve it and publish a different v0.3-CANDIDATE filename. A Files text-index is not an editable original.
- The already existing Notion Scorecard Keeper is the control layer; GitHub holds source policy/code; actual claim, financial, customer and youth data remain in their own access-controlled stores.
- Reuse the user-reported new DEBO-00 (command) → DEBO-05 (dashboard build) chat. No separate dashboard, master brain, task manager, automation or skill registry.

## What is being built outside the dashboard
- schemas/debo_dashboard_snapshot_v0_3.schema.json is the versioned SOURCE-SCOPED display contract, not a live database.
- tools/debo_dashboard_snapshot_validate.py checks timezone-aware source receipts, four NOW/MONEY/BLOCKED/DONE cards, status honesty, source IDs, duplicate ideas and the distinction between synthetic versus authenticated and approved production.
- tests/test_debo_dashboard_snapshot.py adds synthetic positive and negative cases to existing GitHub Actions test discovery.
- This handoff tells DEBO-05 exactly how to consume the contract without duplicating dashboard implementation.

## Screen mapping
1. "Start here": NOW (one next action), MONEY (only verified receipts), BLOCKED (real approval or access gate), DONE (proof links). Always display checked-at and snapshot state.
2. Sister brains: project/readiness/owner gate with exact source links and verified task completion. JCT source tests passing are SYNTHETIC_TESTED, not LIVE_VERIFIED.
3. Skills and plugins: DEBO Core v0.2.0 eight skills, installed-vs-connected-vs-workflow-tested, tool routing, source/last-checked, approval needs. A public SKILL.md does not prove installation.
4. Thread Index: DEBO-00 main command and DEBO-05 dashboard build; branch to DEBO-01/02/04 and each sister-brain only as needed. No invisible sidebar renaming or archiving.
5. Ideas: USE_NOW / RESEARCH_LATER / WAIT / NOT_RELEVANT with project, source and trigger; reuse the existing task/idea workflow, not another app.
6. Automations and export: list only current observed tasks/runs. The Nov 3 previous check showed 25 saved, five enabled; this number may change. Preserve local-only private ChatGPT export workflow. An enabled task is not proof of fresh results.
7. Learning and accessibility: keep existing glossary, Mermaid brain diagram, large tap targets, dyslexia-friendly options, iPhone typography and VoiceOver support. Keep historical views, versions and evidence tabs.

## Current capability choices
ALREADY AVAILABLE/INSTALLED (task-specific permissions may vary): ChatGPT Search; Files/Library; GitHub; Notion; Google Drive; DEBO Core private plugin v0.2.0 with eight skill adapters; Python and current GitHub Actions; Firecrawl; TinyFish; existing design/coding apps; current weekly DEBO System Scout.
OPTIONAL: Similarweb was connected by the user but its analytics/credits have not been tested; G2 MCP was suggested previously and awaits user connection.
NOT NECESSARY: another dashboard, project manager, plugin watcher, "master brain" or bulk import of GitHub skills. No new plugin is a prerequisite to v0.3.

Only use another service when it measurably solves a missing task; explain why, what it changes, overlap, price/limits, customer privacy, authorization and rollback. Connecting apps and high-impact business operations require the appropriate user's explicit action/approval.

## Snapshot contract and release checks
Run:
  python tools/debo_dashboard_snapshot_validate.py /path/to/snapshot.json
  python -m unittest discover -s tests -p 'test_debo*.py' -v

A valid JSON snapshot proves only consistency of fields and evidence references. It does not confirm source reality. The offline dashboard must say NOT LIVE-SYNCED. The VERIFIED_REFRESH state requires actual independent refresh/source receipts; never infer continuous sync or permission from a code path. The MONEY card is UNKNOWN without source-backed amounts. The DONE card must have checked evidence. A project cannot be LIVE_VERIFIED on synthetic tests alone. Keep actual records private.

Source checks from the Nov 3 DEBO-00 conversation: private Core 0.2.0 skill content read in current chat; merged PR #26 tool governance and postmerge CI passed; JCT latest Higgsfield checkout d583979 passed 125/125 synthetic tests and 35/35 source release checks; hosted site reported deployed but owner secret names were absent, so authenticated website→CRM E2E is NOT VERIFIED. John's approval gate still governs JCT public/financial/dispatch actions. A fresh chat's auto skill activation is still untested.

## DEBO-05 completion definition
1. Obtain original editable v0.2.2 bytes, record hash/size and retain as rollback.
2. Make targeted UI enhancements; do NOT overwrite previous work or re-import all project data.
3. Render synthetic contract first and test missing/blocked/verified states.
4. Use only permitted fresh source readbacks; no protected customer/child data in public HTML.
5. Regression test iPhone small screen, 44px touch targets, accessible contrast, VoiceOver, missing-source states, deduplication and existing old navigation.
6. Produce v0.3 CANDIDATE with new verified artifact path, screenshots if appropriate, diff and QA receipt.
7. Send result/checkpoint to DEBO-00 and existing Notion Control & Index. Only approved release mechanisms may publish it.

Do not assume this handoff has access to the other new thread's current state. DEBO-05 should compare its own actual latest source before implementing anything.

Next: validate this source PR in GitHub CI; once on main, DEBO-05 can consume the schema, validator and instructions without needing a new install.

## DEBO-MASTER-026 capability control adapter R0.2 (2026-11-10, REVIEW ONLY)

This additive design handoff preserves the existing canonical dashboard, data model and release gates. The user-facing standalone R0.2 HTML is a **private local review artifact**, not stored in this public repository, not a new DEBO master, not a deployed site, and not a permissioned connector adapter.

### Existing contracts to reuse
- `schemas/debo_dashboard_snapshot_v0_3.schema.json` and `tools/debo_dashboard_snapshot_validate.py` remain the snapshot/display gate. Do not create a parallel live operational status model.
- `governance/dashboard/DEBO_CORE_FEED_v1.json` is public governance/source-health metadata only. Read it to verify source reachability; never infer a live task feed, customer/project status, permission, approval or delivery.
- `governance/DEBO_TOOL_SELECTION_REGISTER_v1.md` and `tools/debo_connector_preflight.py` govern plugin selection and external transfer preflight.
- Existing DEBO-05 private HTML plus preserved v0.2.2 rollback remain the only eligible integration target after original source bytes and hashes are read back.

### R0.2 local review behavior
- iPhone-first Overview, capability scope/permissions/readback/limits, a **dated** scheduled-task split visual, route-this-task recommendations, approvals, blockers, setup checklist, local history, JSON checkpoint export, and resume view.
- Distinguish **screenshot listed**, **action exposed**, **installed**, **connected**, **authenticated**, **authorized**, **read verified**, **workflow tested**, and **deployed**. Screenshots and available tool descriptions are not live connection proof.
- Support documented source truth labels VERIFIED, INFERRED, UNRESOLVED, PROPOSED, DEPLOYED and ESTIMATE independently of each capability's workflow-readiness state.
- Local notes are device-only. No hidden API polling, auto-save to GitHub/Notion/Drive, credential storage, new schedule, external notification, production write or public launch.
- Protective holds cover sign-in/credentials, spending, third-party messages/forms, production edits, destructive changes, permission changes and public hosting.

### Verified source check versus unverified private refresh
A read of the **public** canonical Core feed on 2026-11-10 returned schema `debo.core.public_feed.v1`, ten golden rules, 14 distinct project IDs with zero duplicates, public-only classification and `writes_enabled=false`; all 14 project runtime statuses remained UNKNOWN. This is **not** a signed-in private task-feed refresh, not a private dashboard acceptance test and not a deployment receipt. Do not fold source-health success into the private task-feed `VERIFIED_REFRESH` field.

### QA and next safe step
Local Chromium checks for the R0.2 review artifact passed 33/33, including five viewport widths, routing holds and screenshot-only UNKNOWN entries. The HTML, screenshots, machine receipt, and local test script remain private conversation artifacts. Browser testing via an in-memory loaded HTML page does not verify actual localhost hosting, Safari or VoiceOver. Figma editable design was attempted, but the Starter tool quota blocked native layer work; a blank review file alone is not a design deliverable.

**Integration gate:** recover original private v0.2.2 HTML plus selected latest candidate and hashes; run one authenticated private task-feed read with duplicate check, source timestamps, permissions and a private receipt; apply the R0.2 UI *incrementally* to the selected private candidate; run original navigation/data/accessibility regressions; obtain separate owner-governed release approval. Keep this addendum in review until independently checked.

### Private database reader acceptance (R0.3) — review-only update, 2026-11-10
A dedicated existing DEBO-05 database reader role completed a bounded read-only task count and duplicate check on the existing isolated database branch. Results, source timestamps, database role/privilege evidence, and the private local adapter receipt were filed and read back in the existing **Notion DEBO-00 Control & Index** under `DEBO-05-R03-NEON-READER-20261110-175943Z`. **No private task rows, project data, database secrets, identifiers or task counts are published in this public governance document.**

This is **not** an authenticated read of the protected Vercel R55 web UI or its private `/api/summary` endpoint; it does not prove continuous sync, delivered Work automation or writer authorization. The Vercel connector read the R55 project/deployment/file tree but returned truncated original frontend file bodies, so source-faithful UI integration remains held. The R0.3 companion UI passed local in-memory Chromium checks, but is not the deployed dashboard. Preserve existing SSO, reader grants, PR #44 owner-editor gate, protected originals and rollback. No new dashboard, migration, deployment or release is authorized.
