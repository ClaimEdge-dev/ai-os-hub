# DEBO R19 Continuity Adapter | Candidate v1

Mission: DEBO-MASTER-025. Parent: DEBO-MASTER-024.
Status: CANDIDATE / OFFLINE TESTED, not merged, not scheduled, not installed in ChatGPT, and not live.

## Reuse, do not replace

The authoritative DEBO Core remains DEBO_BOOTSTRAP.md, governance/runtime-briefs/DEBO.md and the owning project's verified private checkpoint. The existing skills/thread-ops/SKILL.md and governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md own thread lifecycle and anti-repeat policy. This is an optional adapter for stable task signatures, capsule validation, private local checkpoint writing, and read-only event planning. It creates no master registry or database.

## Scope and boundaries

- Python: offline, 3.10+, standard library. A checkpoint command writes only a user-selected local file, refuses changed overwrites and symlinks, and reads back exact bytes. Keep private files in the existing authorized project store.
- Evidence references: schema-checked, NOT independently authenticated. A typed reference is not proof of a passing test or actual approval.
- Task fingerprints: deterministic on normalized objective, or existing stable source-key. They do not recognize paraphrases; use the existing task ledger and manual/source-backed alias reconciliation.
- JavaScript: Node 18+ read-only DRY_RUN. It does not write an owning project checkpoint, DEBO Core index, dashboard, or any webhook. In-memory duplicate checks do not persist between runs.
- Public GitHub: only generic source and metadata. Never commit customer records, private capsules, youth/financial data, secrets, evidence URLs, or actual source-backed private event payloads.
- No ChatGPT conversation/Memory, Notion, Google Drive, Neon, schedule, or external AI is automatically changed. No runner is connected.

## Offline usage

    python tools/debo_r19_continuity.py fingerprint DEBO "Verify thread continuity" --source-key existing-task-15
    python tools/debo_r19_continuity.py validate --input private_capsule.json
    python tools/debo_r19_continuity.py checkpoint --input private_capsule.json --output /approved/private/location/R19-001.json
    python tools/debo_r19_continuity.py event --input private_capsule.json --type TASK_VERIFIED --revision source-rev-1 > private_event.json
    node tools/debo_r19_sync.mjs private_event.json

Input is a project-scoped private file provided by the owning project. The checkpoint command does not migrate other registries.

## Candidate acceptance matrix

| Gate | Result | Meaning |
| --- | --- | --- |
| Stable task signatures and project isolation | LOCAL TESTED | Not semantic deduplication |
| Status-dependent typed evidence checks | LOCAL TESTED | Not evidence authenticity |
| Local readback, no changed overwrite or symlink | LOCAL TESTED | No external persistence |
| Duplicate event skip in read-only plan | LOCAL TESTED | Supplied seen-event set only |
| GitHub candidate source readback | PENDING | Read branch files after commit |
| Private canonical checkpoint updated | PENDING | Source-specific write/readback required |
| Fresh separate ChatGPT thread recovery | NOT RUN | Must be shown in another thread |
| Existing schedule real execution | NOT RUN | Requires recorded run receipt |
| Cross-project event writeback | NOT IMPLEMENTED | Requires approvals and a real runner |
| Continuous production release | NOT AUTHORIZED | No production mutation |

## Promotion and rollback

Review diffs against current ThreadOps and anti-repeat policies, run isolated tests, open a draft PR, verify branch files, and add one R19 entry to the existing DEBO-00 index. Only then consider a real private project checkpoint connector and a fresh-thread acceptance test. Project owner gates remain intact.

Rollback: Leave the draft unmerged, or revert the adapter commits if ever merged later. The candidate creates no schedule, webhook, production endpoint, or database migration.

## R131 Source Merge and Separate-Process Acceptance (2026-11-09)

This section supersedes the old *candidate/not merged* heading above **only for GitHub source status**. [R19 PR #39](https://github.com/ClaimEdge-dev/ai-os-hub/pull/39) is MERGED into main at commit `456f5240ac8892ead8cd14c0eb48b8ef314140b0`. Original exact PR-head source security review ran 102 Python tests OK; postmerge main Bootstrap Integrity [run 42690638285](https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/42690638285) and Runtime Brief [run 42690638152](https://github.com/ClaimEdge-dev/ai-os-hub/actions/runs/42690638152) passed, with source contract and CLI file read back directly from main.

R131 adds eight source-verified tests in `tests/test_debo_r131_process_recovery.py` to test **independent local Python subprocesses**, identical checkpoint readbacks, unchanged-write deduplication, cross-project fingerprint isolation, fail-closed missing evidence/task IDs/schema and optional Node read-only event duplicate suppression. The first test run exposed a missing-task-id event failure; R131 hardened the existing adapter to reject malformed capsule identity before any checkpoint or event is processed. The test receives ONLY synthetic fixture contents; the local file is isolated within the CI runner. **A process restart is NOT a fresh ChatGPT thread**. Actual ChatGPT cold-start connector recovery, authenticated external store writeback, persisted events, real owners and a live scheduler remain unverified and need separate supported tool evidence.

Neither the merge nor the test overrides the private project source policy, JCT John acceptance, Claims Susan review, DEBO-05 editor live-login gate, or user authorization for any sensitive action. Rollback remains a Git revert; user/production data never entered the test.
