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
| RRR | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
| MOR | PROFILE_VERIFIED | NOT VERIFIED | Load bootstrap in actual project environment, perform one authorized safe operation, inspect result and write an evidence receipt |
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
