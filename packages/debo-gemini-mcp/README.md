# DEBO Gemini bridge — private MCP and free web workflow

**R8 checkpoint: PRIVATE MCP READBACK PASS / FREE WEB ROUND TRIP PASS / DRAFT.**

The owner-private synthetic Worker and saved receipt are hosted and its existing
ChatGPT plugin has successfully returned the original receipt through an actual
authenticated `debo_get_receipt` call. R7 package verification passed **87/87**
tests locally and in GitHub CI. The existing receipt survived private
redeployments unchanged. The MCP tools remain fixed synthetic fixtures, with no
outbound Gemini API implementation.

R9 adds an **unwired, offline-tested provider transport primitive**, not a live
API connection; see the staged-client section below. It is excluded from the
deployed Worker entry points and their build output.

The existing private plugin also carries the browser-assisted workflow at
`plugin/skills/debo-gemini-free-web/SKILL.md`. A real coding handoff through the
free Gemini website completed; the returned URL validator passed **20/20** local
cases and matched the canonical endpoint policy on all 20. This is a website
route operated by ChatGPT's browser controls, distinct from the synthetic MCP
executor. No sign-in, purchase or API key was used for that observed task.

Gemini API activation, mainline merge and protected release remain **HOLD**.
Free website availability and quotas are provider-controlled; existing
ChatGPT/Work usage still applies. The historical R4-R7 sections below describe
their original source milestones; current operational evidence is recorded in
the existing PR #81 checkpoint rather than private receipt data in this repository.

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

## Current acceptance boundary

| Requirement | Verified evidence | Still required |
|---|---|---|
| Transport | Worker build, MCP2 wire tests and an actual authenticated ChatGPT `debo_get_receipt` call | Revalidate materially changed transport or host behavior |
| Authentication | Owner-private Site, actual Site-scoped caller receipt, project ACL tests and owner-supplied six-check browser PASS | Independent release/security approval remains separate |
| Persistence | SQLite concurrency/restart tests plus one hosted D1 receipt row recovered unchanged after private redeployments and through ChatGPT | Canonical task/R19 storage remains separate from fixture storage |
| Validation | Closed tool input contracts; exact bounded server fixture outputs; tampering rejected even after output hashes are recomputed | Full future live-task/provider JSON Schema validation |
| Provider | Offline Interactions mapper; no provider SDK in Worker; separate free website coding task completed and locally checked | Gemini API credentials/free-tier/billing, model/version and bounded provider error/usage handling before API activation |
| Continuity | Existing synthetic receipt recovered through the current ChatGPT plugin connection | Existing authorized R19 integration for real tasks; browser answers are not stored in the fixture table |
| Release | Existing draft PR; generic source and synthetic tests only | Required independent review, current-head CI and owner release gates |

The identity boundary flag is a configuration guard, **not** authentication by
itself. Trust `oai-authenticated-user-id` only behind a verified Sites dispatch
that authenticates the caller and protects identity headers. Do not expose this
Worker directly or infer security from locally supplied headers. The configured
owner-private Site and private runtime owner allowlist remain the trusted
boundary; do not replace them with a public route or a client identity claim.

`migrations/0001_synthetic_receipts.sql` supplies the local test schema. Request
handlers do not create tables. The hosted Site's migration metadata, DB binding
and manifest were prepared through the supported deployment workflow for the
approved private destination. No canonical R19 data belongs in this fixture table.

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

## Historical R4 verification and resume

- Original R3 baseline reproduced: **39/39 individual tests pass**.
- RED: new transport suite fails because `src/mcp_worker.mjs` does not exist.
- GREEN: offline install, four-module build, and **68/68 individual tests pass**.
- Covers ACL/auth failures, scope isolation, malformed/oversized requests,
  unknown tools, argument injection, nonzero-spend rejection, missing/stalled
  datastore, corrupted/recomputed-hash outputs, concurrency and worker restart.
- Existing security workflow gains a Node 24 job to build/test this package;
  its Python checks and permissions are preserved. Verify the final head's CI.

**R4 next action (historical):** review this exact source and resolve actual trusted caller
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

## Historical owner-private verification adapter (R5)

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

## Historical mobile verification route repair (R6)

The private test page now posts to its authenticated `/api/fixture` route. That
route invokes the existing MCP handler internally with the same owner identity,
project ACL, limits and receipt checks. `/mcp` remains the plugin endpoint.
The browser reports HTTP context for non-JSON responses instead of exposing a
browser-specific JSON parser error.

Evidence: hosted owner identity checks return HTTP 200, but the failing browser
verification calls do not appear in Worker request logs. The pre-Worker MCP
transport mismatch is the working diagnosis; the precise rejected response was
not captured on the user's phone. An executable page regression models that
boundary with a non-JSON transport rejection and fails before the repair.
After the repair, the actual shipped page script plus Worker and SQLite save
and replay one receipt. The full local suite passes **79/79** tests. Live iPhone
button acceptance was subsequently confirmed by the owner's R6_PRIVATE_C
six-check PASS result; the same receipt was later recovered through the plugin.

## MCP client handshake repair (R7)

The previous handler rejected the standard per-request `_meta` in discovery,
tool listing and tool calls, and omitted MCP 2026-07-28 result/cache fields.
Browser verification did not expose this because its internal requests omit
protocol metadata. R7 accepts and validates protocol metadata without using it
as caller identity or project authority; response envelopes include
`resultType: complete`, server information, and private/zero-TTL discovery and
tool-list cache hints. Unsupported versions and header/body mismatches fail.
Metadata-free authenticated browser/internal requests remain compatible.

Seven new wire-contract cases fail against the prior handler. After repair the
full suite passes **87/87** individual tests. Missing transport identity still
fails closed, metadata cannot widen project ACLs, and native receipt reads do
not create another record. Republishing refreshes the existing Site-owned App;
do not replace its identity, connection or sharing to repair registration.
Hosted ChatGPT tool invocation was subsequently accepted: the actual read tool
returned the existing receipt, with every field matching the owner's R7 result.

Primary wire reference:
https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.ts

## Free browser workflow (R8)

The private plugin's added workflow reuses the existing App connection and MCP
tools. It routes only public or deliberately synthetic tasks to the visible
Gemini website, reads the completed answer, inspects generated code and verifies
the work locally before acceptance. It does not add a new API connection or
change Site access, provider flags, schemas or the existing fixture receipt.

Acceptance evidence: the public synthetic task `gemini-free-web-code-v1` asked
Gemini's observed Flash-Lite guest interface to implement a pure JavaScript
Interactions endpoint validator. The completed code was returned to ChatGPT,
inspected and run against 20 bounded local cases, including normalized host and
default port, approved v1/v1beta paths, legacy paths, lookalike hosts, URL-carried
synthetic credentials, queries, fragments and malformed input. All 20 matched
the existing canonical contract. The check performed no network calls; no
Gemini API call, purchase or key setup occurred.

The workflow also passed offline routing exercises for a public coding task,
sensitive insurance records and an exhausted free quota. Sensitive material
stays local without specific destination/data authorization; quota exhaustion
does not authorize payment, account rotation or safeguard evasion.

A saved workflow is reusable guidance, not an unattended server worker. It needs
a ChatGPT host with browser controls and an available free website session.
Do not claim automatic activation in every conversation, unlimited free usage,
an API-backed service or a durable browser-result MCP receipt. Keep the fixture
and browser result labels separate. Use the existing PR checkpoint for sanitized
public completion evidence; do not create another record system.

## Staged Interactions transport (R9 — NOT LIVE)

`src/interactions_transport.mjs` adds a bounded single-request HTTP primitive for
the existing explicitly synthetic mapper. Its caller must supply the HTTP
implementation and credential explicitly; there is no implicit global fetch.
The existing Worker entry points do not import it, and the deployment build
does not include it. No new tool, secret, database migration, runtime setting
or deployment is introduced by this source change.

The candidate enforces approved HTTPS Interactions endpoints, header-only
credentials, redirect rejection, stateless foreground requests, a 1024-output
token cap, deadlines through response-body reading, response byte limits,
strict completion/output checks, token-usage bounds and generic errors.
Dispatched failures carry `outcome: unknown`; it never automatically retries.
It returns `billing_verified: false` and never guesses a dollar cost from a
successful HTTP response. The current example model remains account/quota
unverified. `store: false` does not establish free-tier data-use restrictions.

This primitive is **not a billing or authorization boundary**. Before a future
caller may supply a real transport/key, the integration must verify the actual
owner/project, free-tier eligibility and unlinked billing; acquire durable
pre-call ownership; persist/reconcile uncertain outcomes; complete current-model
live contract checks; and pass the existing release/security gates. Those
controls are not supplied by a label, a caller boolean or this HTTP helper.
Do not expose it through MCP or enable it just because these offline tests pass.

R9 setup attempt: AI Studio redirected to Google account selection. The secure
sign-in request returned `declined`; no signed-in project/free-tier readback,
credential creation, terms acceptance, paid setup or provider request occurred.
The existing free browser-assisted route remains available under its own usage
limits. Automatic API integration remains BLOCKED, not complete.

Transport references checked for this source:
- https://ai.google.dev/api/interactions-api-v1
- https://ai.google.dev/gemini-api/docs/api-key
- https://ai.google.dev/gemini-api/docs/billing
