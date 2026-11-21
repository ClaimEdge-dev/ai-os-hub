# DEBO Universal Website Factory + Project Rescue | v0.1 review packet

**State:** Review-branch source candidate. No production deployment, live website change, installed ChatGPT skill, cloud-file mutation, or public release is implied.

## Recovered canon and overlap decision

- Core authority: DEBO_BOOTSTRAP.md, governance/runtime-briefs/DEBO.md, skills/skill-lifecycle-manager/SKILL.md, and existing project adapters.
- Skill registry: existing Notion AI OS Hub / Skill Registry, with GitHub SKILL_REGISTRY.md as historical source catalog. Do not create a new registry.
- Cleanup/recovery: autonomous-ops-architect, chatgpt-workspace-steward, universal-file-vault, cross-ai-artifact-inventory, ThreadOps, and R19 continuity.
- Existing draft PR #64 provides *private ChatGPT export* ZIP salvage and conversation inventory. Reuse it for that specific job; this packet does not copy or merge its tools.
- Existing draft PR #68 provides *ChatGPT Library* duplicate review. Reuse it for that specific job.
- JCT project adapters already provide website conversion, CRM synchronization, and release QA. They remain business-specific and must not be overwritten by a generic skill.
- New gap: generic local directory/normal-ZIP inventory, and one cross-brand website build/review orchestrator.

## Read-only Project Rescue: exact usage

Run only in an authorized local Python 3.11+ checkout of ai-os-hub.

Directory:

    python tools/debo_project_inventory.py /private/project-folder --project-id CELTIC --private-report /private/reports/celtic-manifest.json

ZIP:

    python tools/debo_project_inventory.py /private/export.zip --project-id CELTIC --private-report /private/reports/celtic-zip-manifest.json

Tests:

    python -m unittest tests.test_debo_project_inventory -v
    python tools/debo_skill_delta.py --include-projects --validate-contracts
    python -m unittest discover -s tests -p 'test_debo*.py' -v

The utility reads accessible local files, hashes regular bytes with SHA-256, identifies exact duplicate groups and potential case/Unicode name collisions, and emits a deterministic private JSON manifest. It does not extract archives, run recovered code, follow symlinks, upload anything, rename/move/delete files, contact providers, or decide the canonical version.

Safety limits: at most 5,000 recorded entries, 128 MiB per hashed file, 512 MiB total hashed local-directory bytes or declared ZIP uncompressed bytes, and 200:1 ZIP member compression ratio. Local directory read failures are reported as UNREADABLE_DIRECTORY and force PARTIAL coverage; the entry limit fails closed before recording additional entries. Encrypted, unsafe-path, unsupported-compression, over-limit, duplicate-name, symlink, and unreadable members are skipped or flagged. Generated directories (.git, .next, .venv, node_modules, __pycache__) are excluded by default and counted as skipped; use --include-generated only for an authorized, bounded investigation. Coverage becomes PARTIAL when anything is skipped. Broken or truncated ZIPs should be handled separately through reviewed private-export recovery, not silently salvaged here.

The detailed manifest contains filenames and content hashes. Keep it in a private project location, outside the scanned directory, never in public GitHub or CI logs. The CLI prints counts only. An existing report is not overwritten unless --replace-report is explicitly supplied. No private report is created in this public repository.

### Manifest contract

Schema: debo.project-inventory.v1.

- project_id: caller-supplied scoped ID, not a cross-company account key.
- source: directory or ZIP, local label and read-only scope.
- entries: relative path, status, size, SHA-256 where actually hashed.
- exact_duplicates: same size + SHA-256, grouped within one scan only.
- potential_name_collisions: Unicode NFC/casefold path collisions for human review.
- summary: total, hashed, skipped, duplicate groups, collisions, and coverage.

A hash match proves identical bytes, not permission to delete either copy. A similar name proves neither duplicate content nor authority. Never infer supersession from modified time alone.

## Cloud evidence and filing boundary

GitHub, Drive, Notion, GitBook and design/hosting providers are read through their actual connected, authorized actions. This Python utility does not grant access to them. For each cloud artifact record the stable provider ID, owning tenant, source revision, observed timestamp, read scope, sensitivity, canonical pointer, and verification state in the existing project checkpoint.

Prepare rename/move/archive plans as a dry run with original ID, proposed destination, dependencies, link impact, owner gate and rollback. Do not execute bulk moves or private cross-tenant transfers without approval. Preserve existing Notion database and Drive folder structures; do not scaffold duplicates.

## Universal website invocation

- DEBO RECOVER SITE: <project> — recover canonical source, tests, design, business truth, preview and blockers.
- DEBO BUILD SITE: <project> — build smallest approved compatible delta; reuse existing stack.
- DEBO POLISH SITE: <project> — improve approved brand, mobile UX, accessibility and conversion.
- DEBO TEST SITE: <project> — execute static, browser and security checks where tools actually permit.
- DEBO HANDOFF SITE: <project> — save source-backed checkpoint and review packet.

The shared workflow is in skills/universal-website-factory/SKILL.md. Each business retains its own project adapter and approval gates. A generated starter or synthetic test is not a verified deployed website.

## Minimal new-project setup contract

Before scaffolding: search the existing Project Registry, GitHub, Drive and Notion for an owning project. For a genuinely new project, prepare only a project adapter, canonical repo/source pointer, existing-or-approved Drive root, existing Notion command center, private secrets template, stack decision, acceptance checks and rollback/handoff. Do not provision a paid service or a public deployment without approval.

## Pilot and release gates

1. First controlled pilot: Celtic Wrestling Academy. Recover its current authorized repository/branch, design, privacy restrictions and latest checkpoint before making a website change. Use synthetic youth/tournament fixtures.
2. Second controlled pilot: JC's Towing. Inherit JCT website QA, conversion and CRM adapters. Keep John Clemens' review gate and real business truth.
3. For each pilot: exact commit, inventory/coverage, changed features, tests, private preview if supported, owner approval, rollback and one next action.
4. No pilot site was modified by this review packet. The Python utility must pass exact-head CI and independent source/security review before promotion. Runtime installation and production use require separate evidence.

## Proposed capability dispositions

| Capability | Decision | Reason |
| --- | --- | --- |
| Skill management/registry | REUSE | Existing Skill Lifecycle Manager and Notion registry |
| AI workspace artifact inventory | REUSE | Existing cross-ai-artifact-inventory |
| General project organization | UPGRADE | Existing autonomous-ops-architect + new local inventory helper |
| ChatGPT export ZIP salvage | REUSE/HOLD | Existing PR #64 remains separately review-gated |
| ChatGPT Library hash review | REUSE/HOLD | Existing PR #68 remains separately review-gated |
| Website build/review orchestration | BUILD CANDIDATE | Cross-brand capability absent from verified root skills |
| JCT website QA/CRM/conversion | REUSE | Existing project-local skills |
| Automated cloud renames/moves | HOLD | Require verified source IDs, approval, and rollback |
| Public plugin packaging/GitBook site | HOLD | First prove a reusable workflow; avoid premature publication |

## Checkpoint contract

MISSION | CANONICAL SOURCE/REF | INVENTORY COVERAGE | REUSE/BUILD DECISIONS | CHANGED FILES | TEST RECEIPTS | INSTALL/LIVE TRUTH | APPROVALS | BLOCKERS | NEXT ACTION.

This document is a review packet, not a new registry, master dashboard, or durable private evidence vault.
