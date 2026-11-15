# GB-003 — unactivated private wiring and rollback plan

Status: CANDIDATE CODE + OFFLINE TEST / HOSTED IMPLEMENTATION HOLD. This is an engineering review package, not authorization to modify a managed Site.

## Exact existing components to reuse

- src/trusted_sites_authorization.mjs: GB-001 server-owned Sites caller resolution, exact owner and project.
- src/financial_authorization_review.mjs: GB-002 closed financial-evidence contract, rejects missing/stale/paid/self-asserted evidence; a synthetic review result is not dispatch permission.
- src/private_wiring_plan.mjs: GB-003/011 source-only read-only preflight, projects bound to DEBO-CORE, closed credential reference and request hash, provider always blocked.
- src/guarded_interaction.mjs and src/durable_execution_gate.mjs: existing staged executor and durable claim/readback. Their test-only injectable dependencies do not constitute live financial approval.
- migrations/0002_execution_claims.sql: present in the candidate branch; NOT deployed remotely. Never apply DDL in a request handler.
- src/site_worker.mjs and src/mcp_worker.mjs: current private synthetic routes only. Do not change or import the staged modules until source, review and owner gates pass.

The source build deliberately outputs only four modules in scripts/build.mjs. Added candidates are excluded from its allowlist. This is a positive invariant to verify in exact-head CI and separately in the target host.

## Proposed minimal future host patch (NOT APPLIED)

1. Capture actual private Site source/version, manifest/bindings and current owner/tenant/permission readback. Fail if a different project or identity boundary is present.
2. Obtain approved server-only host identity resolver, scoped secret-to-project reference resolver, and independently reviewed nonbillable financial-verification implementation. Do not accept caller flags, model names, quota screenshots, credential values or test callbacks as authority.
3. Bind these to the existing preflight. Keep LIVE_GEMINI=false and executor enable=false; do not attach a provider transport or alter the public MCP tool list.
4. Review the original execution migration using a private target and exact expected schema. It is not an applied migration until authorized, executed and read back. Preserve uncertainty rows and originals.
5. Test local synthetic preflight and D1 claims; then perform exact authorized private hosted negative tests with a scoped owner, fake/synthetic input, no provider network, no billing changes, and record actual identity/host/version.
6. Independently review source and runtime observations. Obtain explicit owner release approval before changing dispatch state, publishing new MCP tools, enabling real credentials or making a live provider request.

## Rollback (plan, not rehearsal)

Stop dispatch at the server first and verify false/disabled; preserve all CLAIMED, COMPLETED and UNCERTAIN receipts. For a source regression, revert only the exact candidate commits through a new reviewed non-forced commit/PR, restoring the four-module current synthetic Worker and prior private Site revision. Preserve existing migration/receipt rows; destructive rollback and key rotation are not authorized. Source revert, private host reversion and D1 migration reversal are distinct operations and must each have a verified snapshot, approval and readback before use.

No mainline merge, force push, environment secret changes, new permissions, provider calls, account purchase, private Site update or production changes have occurred through this plan.
