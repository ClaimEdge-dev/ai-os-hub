# DEBO Gemini MCP policy / idempotency pilot

**Status:** ISOLATED LOCAL FIXTURE PILOT ONLY. This does NOT install MCP, call Gemini, consume API credits, deploy a Site, or connect ChatGPT to an external AI. All input data must be synthetic.

This is a narrow, dependency-free Node 20+ test pilot validating the reusable gates needed for the existing DEBO Multi-AI Router PR #75 and R19 helper PR #76. It intentionally does not replace the current R19 `debo.r19.capsule.v1` validator and does not claim its fixture receipts as canonical project evidence.

## Execute offline

`cd packages/debo-gemini-mcp && npm test`

No npm install is needed. No network calls occur. Test command reports exact number of individually executed `node:test` tests.

## Current proofs

- Project allowlist, token checks, read-only and zero-spend defaults, privacy restrictions, output key checking, endpoint host restrictions, per-project lookup isolation, idempotency-key payload conflict detection, single-machine lock serialization and checksum readback.
- Receipt schema `debo.gemini.fixture_receipt.v1` is for test evidence only, **not** R19 canonical `debo.r19.capsule.v1`.

## Missing for a production remote MCP plugin (HOLD)

1. Verify ChatGPT Sites runtime supports a deployed remote MCP transport; implement authenticated HTTP MCP tooling using supported SDK.
2. Replace file locks/fixture disk storage with an approved private **durable transactional** per-project datastore that prevents parallel duplicate paid calls across instances, retries and restarts.
3. Authenticate the caller at the remote transport/session layer and bind allowed project IDs to the caller. Do not place bearer secrets in tool arguments.
4. Reconcile result with existing R19 `debo.r19.capsule.v1` and verified private project store. A typed hash is not evidence of a live result.
5. Verify Gemini API model availability, billing status and real provider-side usage; keep paid calls disabled pending explicit approval.
6. Validate full structured JSON Schema and response limits; use strict egress/tool restrictions and never trust model output as executable instructions.
7. Run isolated integration, concurrency, cancellation, timeout, rate-limit, provider 401/403, error redaction and runtime-restart tests.
8. Only after private Site approval and installation, run one real synthetic end-to-end request and a separate fresh ChatGPT thread receipt readback.

Do not merge, publicly deploy or activate paid provider calls based only on this pilot.
