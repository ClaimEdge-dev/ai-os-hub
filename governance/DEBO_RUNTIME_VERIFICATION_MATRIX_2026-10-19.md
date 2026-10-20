# DEBO Runtime Verification Matrix — 2026-10-19

## Evidence policy
PROFILE_VERIFIED = repository profile read successfully; it does not mean application runtime is active. The Neon Live Bridge registry contains 13 projects, 13 sister brains, and 13 tasks whose statuses were read back as PROFILE_VERIFIED. Housing remains HOLD at project level. Never promote a project or sister brain to VERIFIED without its own runtime test and evidence.

## Verified foundation
- Repository: ClaimEdge-dev/ai-os-hub
- Bootstrap validator: tools/debo_bootstrap_check.py (20 required files)
- Regression tests: tests/test_debo_bootstrap.py and other test_debo*.py
- GitHub Actions: .github/workflows/debo-bootstrap-check.yml; push, pull_request, daily schedule and manual dispatch configured
- Neon: DEBO Live Bridge project damp-math-10052614, schema debo_evolution; actual read and task write verified
- All 13 profile files fetched individually; correct project keys confirmed for twelve standard profiles and DWE file nonempty

## Runtime verification backlog
| Project | Profile | Actual runtime | Required test |
|---|---|---|---|
| DWE | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| JCT | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| RRR | PROFILE_VERIFIED | DATABASE VERIFIED; APPLICATION NOT VERIFIED | Supabase project ACTIVE_HEALTHY, 13 RLS tables, 9 migrations, zero security advisories; smoke receipt ffaa047e-a0cd-4ab7-a461-559ae1ee2f76. Staff auth, workbook-to-staging, dispatcher workflow and resume remain pending |
| MOR | PROFILE_VERIFIED | PRIVATE DEPLOYMENT PARTIALLY VERIFIED | Vercel project exists; latest preview BLOCKED, previous READY; SSO protection enabled. Protected preview and actual application workflow not tested |
| CE | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| PLG | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| BULLDOGS | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| CWA | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| BBS | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| CREDIT | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| SCHOOL | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| HOUSING | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| SETTLESURE | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |

## Completion gate
Each project needs (1) source access (2) profile load (3) authorized safe operation (4) verified result (5) durable execution receipt (6) successful resume test. External communications, production launches, finance and destructive operations remain approval gated.

## Known limits
GitHub profile retrieval and Neon metadata writes do not activate ChatGPT-wide instructions or install cross-platform runtimes. Workflow YAML configuration alone does not prove GitHub Actions has passed; inspect actual job logs/checks.

## Additional checks — 2026-10-19
- RRR original Google workbook ID `1hRtE0y98SvgG5Fv7oni1ZG_GvDn2BBRKrepElTeP7eE` identified and 38 tabs inspected. Owner granted editor access to `claimedgeinspections@gmail.com`; original remained read-only to Sheets batchUpdate (HTTP 403).
- RRR recovery copy `1BgbO2U9V31ljxMy2dbaZKJScPYygakJBTZNppXLrGF8` created with all 38 tabs. Its integration status and Sync Control updated and read back successfully. This copy is NOT yet connected to the deployed endpoint.
- RRR `rrr-sheets-stage` Edge Function is ACTIVE, version 2, and accepts the ORIGINAL spreadsheet ID only. It uses a separate sync secret and stages records for review. Secret configuration, authenticated sync and schedule are unverified; do not infer a successful transfer.
- RRR active staff query returned 0; staff authorization cannot pass until a real authorized account exists.
- RRR Vercel preview `rrr-rapid-roadside-preview` latest deployment READY; public production is not established.
- Morgan's Vercel `morgans-lockport-private-preview` latest deployment BLOCKED, SSO enabled; do not disable protection or promote to production as a workaround.
- Supabase SQL inspection queries were subsequently blocked by safety checks; do not treat those as test failures or retry to bypass.

## October 20, 2026 — independent reconciliation and connector identity check
Audit scope: evidence retrieved from GitHub default branch; portable October 19 skill/install receipts in ChatGPT Library; selected Google Drive indexes; exposed connector actions; official CompanyCam/Leap documentation. A full August 20–October 20 conversation-by-conversation audit is **not** established by this update.

### Corrected evidence and status
- GitHub repository ClaimEdge-dev/ai-os-hub was reachable through authenticated connected GitHub search and file fetch. The October 19 portable installation receipt recording an unavailable GitHub write remains historically true for that earlier execution **but does not describe all subsequent sessions**; repository commits on October 19 and 20 establish later successful writes. No cross-platform permanent DEBO installation is inferred.
- Both exposed connector namespaces `CompanyCam` and `Company_cam` returned the same current OAuth company ID `1520702` from `get_current_user` on October 20. These are duplicate connector surfaces, not evidence of two separately authenticated companies. Earlier records associate `1520702` with ClaimEdge. Do not touch D-Wing production jobs via this session; verify D-Wing target tenant and authorization first.
- CompanyCam's official Leap integration exists: https://companycam.com/integrations/leap . Investigate existing native job-photo sync and enabled account configuration **before** designing custom LEAP↔CompanyCam↔DEBO synchronization.
- CompanyCam's new REST API and Beta MCP exist (https://help.companycam.com/en/articles/15949273-building-custom-integrations-with-companycam-s-api; https://help.companycam.com/en/articles/15928195-connecting-the-companycam-mcp-server-beta). API availability or accessible tool methods are not proof of tenant authorization, real job access, or successful delivery.
- RRR91 lead/revenue spec was fetched at `projects/rapid-roadside-repair/RRR91_LEAD_REVENUE_OS.md`. It marks attribution changes pushed but **not deployed**, backend migrations **not applied**, and compensation agreement **not executed**. Its Higgsfield URL and zero-count baseline are prior-file evidence, not a fresh live smoke test here.
- Google Drive discovery identified `CURRENT — DEBO Operating Rules`, `CURRENT — DEBO Skill Registry`, `DEBO — Trace Run Ledger`, and existing RRR/D-Wing indices. These were located, **not all read end-to-end**. Do not replace their authority with this note.
- GitHub combined status request for commit `6034228a9bd20ac6291160f5f4bc4da879154e15` returned **zero individual statuses**. Therefore GitHub Actions PASS is **NOT ESTABLISHED** by that query; inspect actual workflow logs before asserting it.
- Source-of-truth rule: personal pay, legal, claim/client and minor records belong in access-controlled systems, not in this public GitHub repository.

### Required next deterministic smoke test
DEBO-01: Fetch this matrix from GitHub; identify source/date/status; confirm connector tenant; execute one authorized private, non-destructive improvement; read back exact persisted data; create receipt; in a later session recover the exact receipt with no conversational handholding. Mark PASS only after complete.
Next action: verify actual CI workflow run and a real, permitted end-to-end project-specific operation. Tool choices live in `governance/DEBO_TOOL_SELECTION_REGISTER_v1.md`.
