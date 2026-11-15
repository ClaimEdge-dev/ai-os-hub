# DEBO Skill Foundry v0.1

Status: PROPOSED / NOT INSTALLED
Owner: DEBO orchestration layer
Scope: reusable skill lifecycle across JCT, RRR, ClaimEdge, sports, and other projects.

## Governing principles
- Recover before rebuild. Search existing skills before authoring new ones.
- Separate shared capabilities from project-specific policies.
- Never claim installation based on a folder, README, ZIP, or skill manifest alone.
- Require explicit approval for external sends, public deployment, destructive operations, financial commitments, and changes to sensitive access.
- Never store credentials, customer data, or confidential rates in this public repository.
- Use reviewable pull requests, not direct edits to main.

## Skill lifecycle
1. DISCOVER: enumerate candidate skills and their source/version.
2. REUSE: prefer a verified compatible existing skill.
3. SPECIFY: define input/output contract, project scope, permissions and acceptance tests.
4. BUILD: draft a reusable skill or versioned patch.
5. TEST: lint metadata, check secrets, validate permissions and test sample inputs.
6. REVIEW: request approval for elevated privileges or sensitive behavior.
7. PACKAGE: generate target-specific artifact if the runtime supports it.
8. INSTALL: install only through a supported authorized adapter.
9. VERIFY: record a real runtime invocation and result.
10. REGISTER: record status, version, evidence, owner and rollback plan.
11. MONITOR: detect drift and retire superseded versions.

## Registry schema
skill_id, display_name, description, source_repository, source_path, version, sha, category, project_scope, runtime_target, required_permissions, dependencies, test_status, install_status, installed_version, last_verified_at, evidence_url, owner, approval_state, supersedes, rollback_reference.

Statuses: DISCOVERED, DRAFT, TESTED, APPROVED, PACKAGED, INSTALLED, VERIFIED, BLOCKED, RETIRED.
Do not infer one status from another.

## Shared modules (proposed)
- debo-skill-lifecycle-manager
- debo-skill-registry
- debo-skill-test-runner
- debo-runtime-adapter
- debo-evidence-recorder
- debo-approval-gatekeeper

## Pilot: JCT
1. Inventory existing JCT skill folders and inspect each manifest.
2. Deduplicate overlapping JCT skills; preserve originals until reviewed.
3. Test one read-only skill end-to-end before attempting bulk installation.
4. Keep private JCT business details outside the public repository.
5. Record runtime-specific receipts; never report 51 installed without 51 verified receipts.

## Next implementation gates
- Confirm skill formats and runtime support in each destination.
- Implement manifest validation and secret scanning in CI.
- Build a registry export and test report.
- Install only on authorized targets, verifying each.
- Merge this proposal only after review.
