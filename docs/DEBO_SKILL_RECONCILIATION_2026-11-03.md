# DEBO Skill Batch Reconciliation — 2026-11-03

**Mission:** DEBO-START-20261103-01 / DEBO-01
**Scope:** Existing GitHub `SKILL_REGISTRY.md` versus the already-accessible Notion Skill Registry, plus the current GitHub source tree and targeted canonical skill files. Generated from a real same-day connector comparison and manually verified source files; NOT a direct Kimi-runtime audit or live installation.

## Counts, not installations

| Evidence | Verified count |
|---|---:|
| Numbered GitHub historical catalog rows | 72 |
| Notion database rows / unique normalized names | 94 / 93 |
| GitHub/Notion matching numbered names | 54 |
| GitHub ACTIVE vs Notion DEPRECATED conflicts at baseline | 17 |
| GitHub retired labels reconciled in this PR | 17 |
| Direct root `skills/*/SKILL.md` sources | 19 |
| Nested root `skills/**/SKILL.md` sources beyond direct root | 5 |
| Project-local JCT `SKILL.md` files | 51 |
| Project-local RRR `SKILL.md` files | 8 |
| Plugin-local `SKILL.md` files | 1 |
| Total source files (not distinct installed skills) | 84 |

### Exact status reconciliations

The 17 below were all `ACTIVE` in an older GitHub catalog and `DEPRECATED` in the current queried Notion database. Status is aligned to DEPRECATED in the existing GitHub catalog, with original rows retained. No source code, linked Notion skill pages, or installed software was deleted.

- `claimedge-session-memory` → DEPRECATED
- `claimedge-vault-system` → DEPRECATED
- `claimedge-skill-forge` → DEPRECATED
- `claimedge-auto-deploy` → DEPRECATED
- `claim-command-center` → DEPRECATED
- `claims-evidence-orchestrator` → DEPRECATED
- `bobby-ai-command-center` → DEPRECATED
- `bobby-autopilot-system` → DEPRECATED
- `bobby-skill-activator` → DEPRECATED
- `ai-workflow-decoder` → DEPRECATED
- `session-boot-loader` → DEPRECATED
- `session-context-preserver` → DEPRECATED
- `thread-audit-manager` → DEPRECATED
- `perplexity-connector-advisor` → DEPRECATED
- `pi-case-analyzer` → DEPRECATED
- `claimed-master-workflow` → DEPRECATED
- `credit-repair-orchestrator` → DEPRECATED

### Canonical source-based successors

Evidence from the current GitHub SKILL.md files explicitly documents these consolidations:

- `claimedge-session-memory`, `claimedge-vault-system`, `claimedge-auto-deploy` → `universal-file-vault` v2.0.
- `claimedge-skill-forge` → `skill-lifecycle-manager` v2.1.
- `session-context-preserver`, `thread-audit-manager` → `thread-ops` v2.1.
- `credit-repair-orchestrator` → `credit-repair-master-orchestrator` v2.0 (documented historical control lineage).

The remaining ten deprecated entries **do not gain a claimed replacement** without source and behavioral QA.

### Highest-value current source skills

| Priority | Canonical source | Version | What it unlocks |
|---|---|---|---|
| P0 | `skills/thread-ops/SKILL.md` | v2.1 | Resume Capsules, thread hygiene, no repeats |
| P0 | `skills/skill-lifecycle-manager/SKILL.md` | v2.1 | Use/update/merge governance, prevents duplicate skill builds |
| P0 | `skills/multi-ai-router/SKILL.md` | v3.2 | Smallest effective AI team, project-safe handoffs |
| P0 | `skills/robert-master-os/SKILL.md` | v3.0 | Parent/child orchestration and verified continuation |
| P1 | `skills/universal-file-vault/SKILL.md` | v2.0 | Durable artifacts and evidence receipts |
| P1 | `skills/autonomous-ops-architect/SKILL.md` | v3.0 | Workspace dedupe, lifecycle hygiene |
| P1 | `skills/chatgpt-workspace-steward/SKILL.md` | v1.0 | ChatGPT project organization |
| P2 | `skills/proactive-build-ahead/SKILL.md` | v1.0 | Safely scaffold predictable nonproduction components |

All are **GITHUB_SOURCE_PRESENT / RUNTIME_UNVERIFIED** until independently tested in each target system. None of these source versions is promoted into Notion as a completed runtime install by this PR.

### Remaining gaps and automatic handling

- A single duplicate **non-DEBO** Notion entry was detected: two records for a YouTube Help article with the same title and URL. Preserve both for now; do not delete unrelated records without review.
- Three Notion records have no status, and some have no version, GitHub source link or skill ID. Flag for metadata enrichment rather than assigning fabricated versions.
- The historical GitHub catalog contains legacy `huuso-` names. Treat as legacy provenance; do not auto-promote them or rewrite their semantics solely from a name.
- GitHub source folder counts and the 72-row historical catalog differ in scope; merge by provenance and role, not by summing counts.
- The 404 event-source API and 403 Drive spreadsheet update are independent integration gates. Neither blocks this GitHub metadata correction.
- Existing five enabled ChatGPT schedules remain untouched. The existing GitHub DEBO Bootstrap Integrity workflow gains only a bounded source-only audit step; no new cron, provider permissions or cross-app sync.
- Notion Query Data Source reached a workspace hourly usage allowance after the comparison was completed. No retry was attempted. This PR uses the earlier verified snapshot, not a subsequent unavailable query.

### Release/verification contract

1. Run regression tests on the PR using the **existing** GitHub Actions `DEBO Bootstrap Integrity` workflow.
2. Confirm exactly 17 lifecycle labels differ from the old blob, 72 numbered records remain, and all eight canonical source paths exist.
3. Promote/merge only on passing CI and safe diff; read back the file on main and the post-merge Actions result.
4. Append the exact confirmed outcomes in the **existing** Notion 07 ThreadOps checkpoint; no second registry or new skill installation.
5. Later, obtain a new Notion snapshot after query allowance resets or through authorized view mode, and use the existing `tools/debo_skill_delta.py` incremental report. Do not present absent Notion data as zero actual conflicts.

**Checkpoint:** GitHub lifecycle metadata and core source index review. Runtime installation or Kimi→ChatGPT live transmission remains UNVERIFIED.
