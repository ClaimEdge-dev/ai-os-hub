# DEBO R129 | GitHub Security and Execution Upgrade

**Scope:** Read-only synthetic security/evaluation pilots; only the canonical GitHub source and CI workflows are modified.

## Why this package exists
R128 installed the existing R31 deterministic router but R31 was still labeled `source_candidate_not_installed` in the elite contract. R122 stronger batch verification existed only as draft PR #40. R129 first merged reviewed PR #40 into main (commit `fb3ed09dadcade2f89ae637c2f9a5b23dd746784`), then fixed the contract to reflect R31 source-installed/offline-tested and R127 editor NOT LIVE.

## Three isolated, pinned executable pilots
- **Gitleaks v8.30.1** via pinned, public Linux/amd64 GHCR digest in `.github/workflows/debo-r129-security-execution-pilot.yml`. Scans the public repository working tree, with matches redacted in CI logs. This is a **third-party CLI scan**, not the Gitleaks Action, no app install or API key. Genuine findings must block until reviewed; no broad allowlist or false clean result.
- **Promptfoo 0.125.1** via ephemeral pinned npm CLI in CI using only `security/r129_promptfoo/provider.py`. Eight synthetic policy-abuse cases exercise the real R31 router through a deterministic Python adapter. Telemetry/sharing/update/remote-generation switches are disabled. **This does not test an LLM's resistance to prompt injection**; it is a contractual guardrail test.
- **OpenAI Agents SDK 0.24.0** pinned to a separate ephemeral Python CI job. `ScriptedModel` performs an actual SDK-runner Mack → Forge → Proof handoff with tracing disabled, no API key, no external model calls, and no remote agents. This verifies SDK routing mechanics, not provider intelligence or persistent workers.

## Recovery and no-repeat
`tools/debo_r129_interrupt_recovery.py` reuses the existing R128 planner and R31 router. It writes **only synthetic fixture data** to a supplied preexisting local directory using atomic replace; it can resume after a simulated interruption and skip previously persisted steps. It fails closed on cross-project/stale journals and on supposed owner approvals. The R128 receipt validator was corrected to support multiple source revisions while preserving per-revision uniqueness.

## Source reuse from existing private repositories (NOT copied to public)
- `ClaimEdge-dev/claimedge-command-center` contains versioned `schemas/event-log.schema.json`, `schemas/approval-ledger.schema.json`, `schemas/dead-letter-queue.schema.json`, `schemas/validation-report.schema.json`, and related handoff shapes. Consider adapting ONLY after tenant/security/field-by-field owner review.
- `ClaimEdge-dev/claimedge-vault` contains existing `manifest.json` and template/archive conventions. Do not publish private schemas or claim active cross-service synchronization.

## Other evaluated GitHub projects (not installed)
- GitHub Spec Kit: optional structured feature contracts; a small DEBO-native template is included at `docs/DEBO_R129_EXISTING_CORE_FEATURE_CONTRACT.md`, **without** installing its CLI.
- MCP Inspector: use isolated authorized development MCP server only, no production credential probing. Current license repository is transitioning between MIT and Apache-2.0/CC-BY for subsets, recheck before redistribution.
- DBOS: Postgres-backed durable workflow candidate, but source-first R19/R31 synthetic resume baseline comes first; no new DB, scheduler or dependency.
- Phoenix / GitHub Dependency Review: revisit after real agent traces or dependency-changing PRs; availability/licensing and repo settings to be assessed before CI activation.
- Temporal, Trigger.dev, CrewAI, LangGraph, OpenHands, n8n: no evidence warrants redundant orchestrators yet.

## Current business boundaries
R126 private DEBO-05 authenticated dashboard/feed passed; R127 Neon isolated DB write function passed rollback tests while the actual editor UI and writer LOGIN are **not installed or live** (draft PR #44). Existing JCT John fixture, ClaimEdge Susan review, R119 imported Work Stack approval, housing hold, youth and financial privacy remain. No production database writes or public site promotion in this PR.

## Security and honest reporting
- Pinned ephemeral CI tools are not account-wide plugin installations.
- CI runners may have outbound package fetch for installation. Promptfoo's ordinary eval provider makes no LLM calls and does not process private data.
- No numeric speed savings or token pricing are claimed without real-run evidence.
- Human owners retain spending, sending, access, public deployment and business-bound approvals.

## Next proof after source CI
Inspect exact SHA GitHub CI; retain source-only state on failure; merge reviewed changes only after full check and readback. Then run a **fresh ChatGPT project conversation** to prove actual cross-thread canonical loader behavior and a real owner-approved operational handoff. Separately finish existing DEBO-05 editor's authenticated preview without broadening the read-only user role.

External primary references:
- https://github.com/gitleaks/gitleaks
- https://github.com/promptfoo/promptfoo
- https://github.com/openai/openai-agents-python
- https://github.com/github/spec-kit
- https://github.com/modelcontextprotocol/inspector
- https://github.com/dbos-inc/dbos-transact-py
