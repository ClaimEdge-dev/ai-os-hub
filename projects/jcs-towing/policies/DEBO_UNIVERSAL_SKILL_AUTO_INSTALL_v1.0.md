# DEBO Universal Skill Lifecycle & Auto-Install Policy v1.0
Date: 2026-10-11
Status: PROPOSED — shared development branch; not yet merged or installed into any native AI runtime.
Parent: DEBO v3.2. Applies to all sister brains, including JCT-OPS.

## Default trigger
When the user reports, requests, creates, updates, or hands off a skill or plugin:
1. Recover current project and existing skill registry; search source, current target runtime, prior receipts, and duplicates.
2. Determine the skill's intended host(s). Do not confuse GitHub source, packaged artifact, Kimi native skill, ChatGPT native capability, or other agent runtime.
3. Check code provenance, license, security, required permissions, compatibility, dependencies and any installation charges.
4. Merge or extend an existing skill where practical. Prefer existing source of truth over a duplicate.
5. Build/repair, validate, package only when host requires, install through an authorized supported integration, activate, run representative test, and verify a host-native installation receipt.
6. Record source path, version, host, install status, evidence, test results, blockers and next action in canonical registry. Sync verified reusable improvements across applicable sister brains with separate per-host verification.
7. Continue original mission automatically; do not stop after building skill definitions.

## Approval and access
Treat user instructions as standing permission to attempt safe, supported, no-cost installation into already authorized environments, not permission to bypass platform restrictions, connect new accounts, grant elevated permissions, expose secrets, spend money, install unreviewed executables, alter production, or publish. Request explicit approval for those actions. If a host lacks native installation tools, mark BLOCKED / NOT INSTALLED and preserve source in shared repository; do not invent an installation. Never require ZIP/manual downloads when direct connected handoff is supported. Do not assume continuous autonomous execution without a real persistent workflow.

## States
DISCOVERED → BUILT → VALIDATED → INSTALLED → ACTIVE → TESTED → VERIFIED COMPLETE.
Also: BLOCKED, FAILED, SUPERSEDED.
A package or GitHub commit alone is never INSTALLED. Installation and test evidence are host-specific.

## Required handoff
project_id, skill_id, version, source_repo, branch, commit_sha, target_host, install_method, installed_at, activation_status, test_name, test_result, evidence_link, blockers, approvals_required, next_action.
Never fabricate values; use UNRESOLVED when unknown.

## Current JCT K3 six-skill case
Reported six created; five packaged; jct-k3-debo-handoff packaging needs rerun. Native installations unverified. Recover and reconcile with jct-ops + 50 specialist source definitions and jct-command-center-k3-elite; fix packaging, install/test in Kimi if supported, sync safe source via development branch, verify separately for ChatGPT. No ZIP handoff required where connected source sharing works.

## Governance
Changes to global master instructions and production runtimes require proper review and host capabilities. This file is a proposed policy until approved/merged into canonical DEBO Core. Preserve DEBO v3.2 rather than creating a duplicate parent.
