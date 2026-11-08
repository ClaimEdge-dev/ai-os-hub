# DEBO R99 | GitHub CI source and historical failure investigation
Date 2026-11-08 America/Chicago. Mission DEBO-MASTER-039.
Checkpoint R99-CI-SOURCE-RECOVERED-HISTORIC-FAILURE-UNRESOLVED.
Parent R98.

Recovered canonical main DEBO_BOOTSTRAP.md, governance/DEBO_RUNTIME_BOOTSTRAP_v2.md, governance/runtime-briefs/DEBO.md, tools/debo_bootstrap_check.py, and .github/workflows/debo-runtime-briefs.yml via GitHub connector. Current workflow defines PR verify-proposal and main update-derived-briefs; checks include bootstrap checker, generated runtime brief validation, dashboard feed validation, and unittest discover -s tests -p test_debo*.py. Workflow writes derived artifacts on main only when changed. R84-R98 evidence commits are on branch debo-r18-source-preserving-sync-20261108, not proof main CI executed.

Historical commit 51504f8c23d411d670bcf33549637fd056acf722 fetched successfully. It changes governance/DEBO_FACTORY_TWO_PRIVATE_PILOTS_v1.md to mark experimental pilot as reference pending dedupe against canonical 24/24 test suite; it does not itself identify the root cause of historical DEBO Bootstrap Integrity failure. fetch_commit_workflow_runs for abbreviated SHA returned empty (this connector filters PR-triggered runs); empty results do not establish no workflow ran. Expected guessed path .github/workflows/debo-bootstrap-integrity.yml and .yaml not found, but actual runtime-brief workflow exists. No CI run logs or job ID recovered, so root cause UNRESOLVED, not repaired.

Next: locate exact historical workflow run/job and logs from GitHub Actions using authorized browser/API; isolate failure, patch on private branch, run tests and verify, then propose PR; no automatic main merge or deployment.
No production, account permission, or customer data change.
Thread Index R98 QA -> R99 CI recovery.
