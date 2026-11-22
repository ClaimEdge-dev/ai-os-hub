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
## 2026-11-14 R19 Library-First and Cross-AI Evidence Handoff

**Scope:** Source-policy extension to the existing R19 offline/private-first adapter. This section does not change the adapter's capsule schema, create a second memory or registry, connect another AI, authorize destructive cleanup, or establish real ChatGPT fresh-thread recovery.

**Task order:** ChatGPT Library read-only inventory and proposed cleanup manifest first; then an accessible ChatGPT export/conversation audit; then Gmail; then Google Drive; then other authorized stores. Independent read-only checks may run in separate safe lanes without displacing Library-first. Preserve originals, protected records, restore paths and the DEBO-05 HOLD. Historical Library audit figures and scanner staging reports are leads requiring fresh readback, never present-tense truth.

**Use existing specialist routing, not new agents:**
- **ChatGPT / DEBO Core:** own the project objective, tool/tenant authorization, dedupe, conflict adjudication, review gates, current canonical source readback, and R19 checkpoint preparation.
- **Gemini:** when independently connected/authorized, recover Google Workspace metadata/ledger/scanner and prepare reviewable engineering deltas. Supply original IDs, precise source versions, timestamps and actual test receipts. Do not assume it sees ChatGPT Library or private threads.
- **Perplexity:** when available, perform public external research and independent source/date checks using **sanitized packets**. Never transmit private files, customer/youth/financial/claims details, credentials, or account metadata without specific approval.

**Handoff packet contract (inside the owning private project, not committed to this public repository):**

```json
{
  "schema": "debo.r19.handoff.v1",
  "mission_id": "SOURCE-VERIFIED-MISSION",
  "project_id": "DEBO",
  "task_id": "SOURCE-VERIFIED-TASK",
  "provider": "ChatGPT|Gemini|Perplexity",
  "source_scope": "ChatGPT Library|ChatGPT export|Gmail|Drive|public research|other",
  "coverage": "VERIFIED_PARTIAL|VERIFIED_COMPLETE|UNKNOWN",
  "sources": [{"source_id": "VERIFIED-PRIVATE-ID", "version_or_hash": "OBSERVED-OR-UNKNOWN", "observed_at": "ISO8601"}],
  "findings": [],
  "proposed_changes": [],
  "tests": [{"name": "ACTUAL-CHECK", "result": "PASS|FAIL|NOT_RUN", "receipt": "PRIVATE-REFERENCE-OR-NONE"}],
  "conflicts": [],
  "blockers": [],
  "next_action": "CONCRETE-SAFE-ACTION"
}
```

**Ingestion and status gate:** Resolve exact owning tenant/project and authentic source identity. Keep evidence links in their approved private location. Deduplicate only stable IDs/hashes in the same ownership scope; same-name and same-size are candidates, not exact copies. On source conflict, preserve both, prefer the latest verified authorized source, and hold irreconcilable material changes. Convert a verified accepted handoff into the **existing** `debo.r19.capsule.v1` only through its validator and existing approved private destination; follow duplicate-safe readback and evidence/status requirements. A typed citation alone is not authenticated proof. No automatic writeback, cross-platform sync, schedule, memory installation or LIVE assertion without separate connector and runtime receipts.

**Acceptance:** Existing R19 regression tests continue passing; Library-first order, no-destructive-cleanup default, tenant isolation, unverified-coverage behavior, conflict hold, and no-false-LIVE status are tested; exact-head CI and any existing independent security review pass before promotion. A GitHub merge is **SOURCE MERGED**, not an external runtime activation.


## 2026-11-22 | Continuity Engine 1.0 — R19 extension (review candidate)

**Implementation:** Existing R19 Python capsule validator/writer remains the only writer. New read-only tool tools/debo_r19_continuity_guard.py is a planning guard, NOT another memory store or task engine. Its synthetic tests are in tests/test_debo_r19_continuity_guard.py; existing Bootstrap Integrity runs test_debo*.py. The guard is offline: no API keys, new database, network calls or API charges.

Example for project-owned private files (never commit real capsules):

    python tools/debo_r19_continuity_guard.py --input /approved/private/path/capsule-v1.json
    # Multiple --input values must be from one task lineage in oldest-first order.
    python tools/debo_r19_continuity.py checkpoint --input /approved/private/path/capsule-v1.json --output /approved/private/path/next-version.json

| Upgrade | Existing component | Deliverable | Limit |
| --- | --- | --- | --- |
| 1. Continuity recovery | R19 + existing Resume Capsule | Source-first read-only plan | Not a live ChatGPT cold-start |
| 2. Cross-AI bridge | Cortex plugin v0.3.3 + PR #85 | Same-account two-way acceptance contract | Second client not connected/tested |
| 3. Checkpoint capture | Existing R19 checkpoint + ThreadOps | Explicit approved private write/readback | No unattended event runner |
| 4. Memory conflicts | R19 guard | Same-revision conflict HOLD | Structural, not semantic contradiction |
| 5. Project awareness | Existing profiles + R19 fingerprints | Mixed-project/task comparison rejected | No real private data imported |
| 6. Execution dashboard | Existing DEBO-05 UI + Core source feed | NOW/MONEY/BLOCKED/DONE metadata contract | No live editor claim |
| 7. Agent routing | Existing multi-ai-router | Canonical-first, optional Cortex read | External AI access unverified |
| 8. Self-diagnostic QA | Existing Bootstrap Integrity + tests | Privacy, stale state, duplicate and conflict checks | Synthetic/offline only |
| 9. Cost governor | Existing work-credit-governor | Zero additional spend planner and no API calls | No quota/balance inferred |

**Privacy:** No objective, checkpoint text, source evidence references, customer details, private financials, credentials, government IDs or youth/guardian data appear in planner output. Cortex metadata is a candidate only; the offline guard sets external_write_permitted=false. Private file data must not enter the public GitHub repository or dashboard feed.

**Conflict/freshness:** Identical capsule bytes are deduplicated. Same source_revision or identical observation timestamp with conflicting states triggers HOLD_CONFLICT for review; not proof that one historical state is false. Missing/future timestamps are UNKNOWN; evidence reports older than seven days are REVERIFY. Typed proof references remain unauthenticated. Exactly one project and one task lineage per call.

**Execution and rollback:** During an authorized active session, ThreadOps can use this read-only guard before creating a new approved private checkpoint with the existing R19 command. No bulk sync, hidden scheduling, cross-provider authentication or production deployment is created. Use the existing public dashboard only for source health, not private status. Cross-AI continuity stays HOLD until an independently authenticated second client completes both-direction reads. Roll back by leaving the review branch unmerged; the guard changes no account or storage.
