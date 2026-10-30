# DEBO Phase 2 command-core pilot — 2026-10-26

Status: **LOCALLY TESTED / NOT LIVE**. Owner: DEBO Core. Branch: `feat/debo-phase2-command-core-20261026`.

This pilot does not replace `robert-master-os`, `multi-ai-router`, the established project registry, Neon Live Bridge, or approval/security owners. It is an isolated, standard-library command-state adapter in `tools/debo_command_core.py` plus tests in `tests/test_debo_command_core.py`.

## Preflight evidence

- Canonical repository: `ClaimEdge-dev/ai-os-hub`, public, default branch `main`, commit `b712c8c3be3e79fcfba6b71c4f9f1dc90b03f9ee` on clone.
- `python3 tools/debo_bootstrap_check.py` returned PASS for 20 required files and 13 profiles.
- Initial `python3 -m unittest discover -s tests -p 'test_debo*.py' -v` reported 17 tests with two failures in the anti-repeat missing-control test. The cause was a test method calling a second method that used `unittest.subTest`, which captures assertion failures rather than raising to the caller.
- Fixed the negative test without altering canonical governance content.
- With the pilot's five additional tests, the same unittest command returned 22 tests, all PASS.
- Current Neon connector `list_projects` returned an empty array, despite historical GitHub records documenting Neon Live Bridge. Current DB project/schema access and live health are **NOT VERIFIED**. No DB write was attempted.
- CI workflow YAML was retrieved, but no current server-side green run was established. Local tests are not proof of GitHub Actions success.

## Pilot behavior

The module accepts explicit registered project IDs and actor scopes provided by the caller; it uses SQLite for local durable tasks and append-only events. Only `note:` is executable and has no external side effect. All other operations enter `WAITING_APPROVAL` and fail closed (there is no approval service yet). It validates state transitions and requires an evidence string to mark a manually routed task `VERIFIED`.

**Security limitation:** `actor_projects` is caller-supplied test input, not authenticated identity. Do not expose this module as a public service or store sensitive records in it. The transition evidence check confirms only presence, not independent validity; the production verification engine remains unimplemented.

## Acceptance evidence

1. Duplicate prevention: PASS (same key resumes; conflicting key fails).
2. Restart recovery: PASS (SQLite reopened and completed once).
3. Cross-project permission denial: PASS in synthetic caller-scope tests.
4. Unauthorized external action blocked: PASS (no external adapter exists).
5. Invalid transition and absent evidence rejected: PASS.
6. Existing repository regression tests: PASS locally (22 total).
7. Real user authentication: NOT IMPLEMENTED.
8. Neon integration: BLOCKED (current connector no projects visible).
9. CI server run: UNKNOWN.
10. Deployment: NOT STARTED.

## Next action

Recover Neon Live Bridge connection/project authority and actual CI status. Then adapt command schemas to the existing database on a non-production branch, wire authenticated actor scopes, and verify an end-to-end task with durable readback before claiming broader DEBO activation.
