# DEBO Runtime and Integrity Test Receipt
Date: 2026-10-19

## PASS: repository integrity
Method: GitHub connector read-only fetch, 20 expected canonical files.
Result: 20/20 readable and nonempty. Master bootstrap contains references to communication, preventive, and self-improvement standards. Zero missing links.

## UNVERIFIED: GitHub Actions execution
Workflow file exists at .github/workflows/debo-bootstrap-check.yml. The available commit-workflow-run lookup returned an empty list, but this endpoint only reports PR-triggered runs, so it does not establish whether push-triggered runs occurred. No successful Actions job log observed.

## BLOCKED: local full checkout
A local git clone attempt failed because the execution container could not resolve github.com. This is a network limitation, not evidence of a broken repository.

## UNVERIFIED: actual cross-app activation
ChatGPT account-wide/project/thread autoload, Notion-triggered actions, Kimi, Perplexity, Neon, and plugins have not passed an end-to-end execution test. Persisted docs do not equal installed autonomous runtime.

## Next operational acceptance tests
1. Confirm GitHub Actions workflow is enabled and inspect its first job logs at the repository Actions page.
2. Introduce a harmless test edit to a governed file; verify workflow triggers, validator returns PASS and logs a receipt.
3. Intentionally test a missing required file in a temporary branch, verify FAIL, then discard the branch. Never break main.
4. Test each sister-brain startup in its actual host, with a safe read-only task and evidence of correct profile loading.
5. For integration sync, verify least-privilege auth, retry queue, duplicate protection, failure alerts and rollback.
6. For continuous monitoring, set a supported schedule explicitly; never claim idle-time autonomous operation without a running service.

## Truth boundary
This receipt records a verified repository read check, not a successful production or cross-platform installation.


## Superseding live verification — 2026-10-19 21:38 UTC
The earlier UNVERIFIED Actions and BLOCKED checkout observations above are historical, superseded by this run.

- Authenticated repository metadata and a full local git clone succeeded.
- Root cause of earlier uncertainty: the commit-workflow lookup is restricted to pull_request events. Querying the repository Actions runs endpoint recovered successful push runs and job logs; no workflow activation fault was found.
- Positive baseline: https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/39328103149 — validator PASS, 20 required files, 13 profiles; actual job log inspected.
- Controlled negative test reused the existing PR #10 branch, emptied only its JCT profile, and observed exit 1 with `Empty: governance/sister-brains/JCT_PROFILE_v1.md`: https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/39328765450 . Main was not broken.
- Restored the original profile blob, then verified successful recovery: https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/39328849623 . PRs #10 and #11 closed without merge; branches retained as evidence.
- Installed isolated regression tests in tests/test_debo_bootstrap.py. Missing-file tests cover every required path, plus empty profile, broken inheritance and successful startup.
- Local test suite: 13 tests PASS. GitHub-hosted suite: 13 tests PASS (job log inspected): https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/39328885549 .
- Existing workflow now runs these regressions on governed changes and includes daily cron `17 12 * * *` (12:17 UTC). Push execution VERIFIED; first scheduled invocation still PENDING. Failure is detected by nonzero exit and failed GitHub check; external alert delivery not tested.
- These tests verify repository integrity and failure detection only. They do not certify business apps, customer intake, isolation enforcement, or global ChatGPT installation.
