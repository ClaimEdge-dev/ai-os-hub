# DEBO Gemini bridge — synthetic MCP prototype

**R4 checkpoint: BUILT / TESTED OFFLINE / DRAFT / DEPLOYMENT HOLD.**

This package contains a stateless JSON-RPC Worker candidate and the original
policy/Interactions mapping fixtures. It has no outbound provider implementation.
It is not hosted, installed, connected to Gemini, or approved for production.

## Run locally

Use Node **22.13+** (native `node:sqlite` for tests); R4 was tested on Node 24.22.1.
There are no third-party runtime or development dependencies.

```sh
npm ci --ignore-scripts --offline --no-audit --no-fund
npm run build
npm test
```

The build validates and copies four web-standard ESM modules to
`dist/server/index.js` and its sibling modules, with a SHA-256 build manifest.
It does not register a Site, provision storage, or generate deployment identity.
The lockfile contains only this dependency-free package.

## What the prototype does

- Implements `POST /mcp`: `server/discover`, `tools/list`, and `tools/call` using
  the documented Sites MCP protocol version `2026-07-28`.
- Exposes only `debo_gemini_execute` and `debo_get_receipt`. Execution accepts
  `project_id`, `idempotency_key`, and one of two fixed `fixture_id` values.
  Prompts, API keys, arbitrary payloads, caller tokens, schema overrides, paid
  operations and provider URLs cannot be supplied through these tools.
- Reuses the existing project/input policy via web-standard `src/contracts.mjs`;
  existing Node caller/hash helpers remain in `src/policy.mjs`.
- Requires explicitly configured synthetic mode, the Sites identity boundary,
  and a server-owned caller-to-project ACL. Missing identity or scope fails closed.
- Uses D1-style primary-consistent prepared statements with a unique
  `(project_id, idempotency_key)` receipt key. Atomic insert never overwrites an
  existing receipt. Readback verifies caller, project, fixture, full fixed output
  contract and canonical-JSON hashes before returning a result.
- Bounds request bytes and body/store deadlines, rejects unexpected routes,
  cross-origin calls and extra argument fields, and redacts storage errors.

Example tool arguments (synthetic data only):

```json
{"project_id":"DEBO-CORE","idempotency_key":"synthetic-bridge-0001","fixture_id":"bridge-health-v1"}
```

The tool name describes the future bridge role; its current executor only
returns server-owned fixture data. `network_calls: 0` and `actual_cost_usd: 0`
refer to that fixed synthetic execution, not to an unimplemented provider call.

## Exact acceptance boundary

| Requirement | Verified evidence | Still required |
|---|---|---|
| Transport | In-process Request/Response tests; Worker artifact builds | Real Sites protocol/tool discovery acceptance |
| Authentication | Simulated transport headers plus server ACL tests | Verify owner-private Site policy and dispatch header provenance; bind actual Site-scoped caller ID |
| Persistence | Actual SQLite SQL; 6 independent worker isolates produce one row; later worker reads/replays identical receipt | Approve and bind the private hosted store; verify D1 semantics, migration packaging and hosted restart/readback |
| Validation | Closed tool input contracts; exact bounded server fixture outputs; tampering rejected even after output hashes are recomputed | Full future live-task/provider JSON Schema validation |
| Provider | Offline Interactions mapper; outbound fetch disabled in a transport test; no provider SDK in Worker build | Model/version, credentials, quotas, billing approval, timeout/429/401/403/cancellation/usage tests |
| Continuity | Synthetic receipt schema `debo.gemini.fixture_receipt.v1` only | Existing authorized R19 store integration and authenticated fresh-chat readback |
| Release | Existing draft PR; generic source and synthetic tests only | Required independent review, current-head CI and owner release gates |

The identity boundary flag is a configuration guard, **not** authentication by
itself. Trust `oai-authenticated-user-id` only behind a verified Sites dispatch
that authenticates the caller and protects identity headers. Do not expose this
Worker directly or infer security from locally supplied headers. No bypass token,
OAuth server, user ACL, Site permission, or production secret was created.

`migrations/0001_synthetic_receipts.sql` is a candidate schema applied only to
temporary local test databases. Request handlers do not create tables. Hosted
Sites migration metadata, DB binding and manifest must be prepared through the
supported deployment workflow after the private destination is approved. No
canonical R19 data belongs in this fixture table.

Atomic fixture persistence does **not** establish exactly-once paid execution:
there is no provider call here. A live adapter still needs durable pre-call
ownership and uncertain-outcome reconciliation before any charge. A timed-out
database request may still commit; retry only the identical request key. There
are no automatic retries. Hashes detect consistency/corruption; they are not
digital signatures or proof against a privileged database writer.

## Interactions endpoint policy

Only these HTTPS create endpoints pass the existing URL policy:

- `https://generativelanguage.googleapis.com/v1/interactions`
- `https://generativelanguage.googleapis.com/v1beta/interactions`

Legacy `generateContent`, unexpected paths, other domains, embedded credentials,
queries and fragments are denied. URL validation does not execute HTTP. The
offline mapper retains `store: false`, `background: false`, no provider tools or
previous-interaction ID; these settings are not a universal data-retention claim.
Its example model remains unverified for live availability and its response
mapping requires live API-version verification before activation.

## R4 verification and resume

- Original R3 baseline reproduced: **39/39 individual tests pass**.
- RED: new transport suite fails because `src/mcp_worker.mjs` does not exist.
- GREEN: offline install, four-module build, and **68/68 individual tests pass**.
- Covers ACL/auth failures, scope isolation, malformed/oversized requests,
  unknown tools, argument injection, nonzero-spend rejection, missing/stalled
  datastore, corrupted/recomputed-hash outputs, concurrency and worker restart.
- Existing security workflow gains a Node 24 job to build/test this package;
  its Python checks and permissions are preserved. Verify the final head's CI.

**Next action:** review this exact source and resolve actual trusted caller
binding plus the authorized hosted persistence/migration contract. Preserve
deployment/merge/live-provider HOLD until those requirements and owner gates are
satisfied. No independent review, fresh ChatGPT thread acceptance, Site/plugin
installation, real-data transfer or provider request has been performed here.
R3 source rollback: `0d0e53de3936f66f759f60c477c5b611d194234b`.

## Primary references

- [Sites-hosted MCP plugins](https://help.openai.com/en/articles/20001547-hosting-a-plugin-with-chatgpt-sites)
- [D1 database/session API](https://developers.cloudflare.com/d1/worker-api/d1-database/)
- [D1 prepared statements](https://developers.cloudflare.com/d1/worker-api/prepared-statements/)
- [Gemini Interactions v1](https://ai.google.dev/api/interactions-api-v1)
- [Gemini Interactions v1beta](https://ai.google.dev/api/interactions-api)

These are interface references, not evidence of this prototype's hosted runtime.

## Owner-private verification adapter (R5)

`src/site_worker.mjs` adds an owner-private test page and an identity readback
endpoint. The owner allowlist is a private runtime email value supplied from the
actual Site owner record. Receipt ownership still uses the Site-scoped caller ID.
The caller may access only `DEBO-CORE`; tools accept only fixed synthetic fixtures.
`DEBO_ENABLE_LIVE_GEMINI` must explicitly equal `false`.

The optional Site build uses `scripts/build-private-site.mjs` and requires the
registered Site manifest plus build-only `esbuild@0.25.12` in that private Site's
package. The core package remains dependency-free. Site schema generation uses
the supported Drizzle workflow; do not apply schema DDL from a request handler.

The expanded local suite passes **75/75** tests, including seven owner adapter
tests. The browser test can check live identity, replay, scope, extra input and
header-spoof rejection; those remote checks are not established by local tests.
Private synthetic publication was specifically authorized by the owner. This
does not authorize paid provider usage, mainline merge or live Gemini activation.
