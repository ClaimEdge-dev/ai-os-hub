# DEBO Gemini MCP Bridge | Governance addendum and engineering acceptance
Date: 2026-11-14
Status: REVIEW CANDIDATE — NOT INSTALLED, NOT DEPLOYED, NOT LIVE
Scope: DEBO Core / Multi-AI Router / R19. This is a governed component addendum, NOT a new DEBO Bible, memory engine, dashboard, or registry.

## Mission and source hierarchy
Keep ChatGPT as the owner-facing headquarters and direct native plugins as first choice. Reuse \`DEBO_BOOTSTRAP.md\`, \`governance/runtime-briefs/\`, \`skills/multi-ai-router/\`, existing R19 capsule/validators and the owning private task checkpoint before building an external service. Gemini is an optional task specialist, not a substitute owner or autonomous standing agent. Maintain RECOVER → DEFINE → ROUTE → EXECUTE → VERIFY → FILE → CHECKPOINT, one active objective and up to two safe independent lanes. Keep Kimi, Perplexity and Claude optional and unactivated until the first Gemini milestone passes.

## Verified source state at review
- GitHub PR #75 ("DEBO three-AI command protocol and Gemini Forge adapter") is **OPEN DRAFT**, head \`b53190358a96bfdfcdbd02781bca1cb41aa7529d\`. It changes skill/routing descriptions, not a verified external MCP runtime.
- GitHub PR #76 ("R19 Focus Recovery: Read-only resume and repeated-blocked checkpoint audit") is **MERGED**. It adds read-only resume and blocked-snapshot analysis to the existing R19 helper. This is **not** evidence of a Site-hosted receipt store or cross-ChatGPT-thread live readback.
- GitHub PR #74 browser adapter is **OPEN DRAFT / SECURITY HOLD**. Do not remove that hold to finish the bridge.
- The supplied Gemini handoff describes \`packages/debo-gemini-mcp/\` with seven proposed source/test files and calls it "BUILT & TESTED-OFFLINE"; the package is **NOT PRESENT on GitHub main at this review**. Its contents were pasted in a ChatGPT conversation, not independently compiled or verified from a repository checkout here.
- A pasted DRY_RUN receipt with typed hashes, timestamp and validation text is **unverified provenance**, not an authenticated new R19 checkpoint. Do not promote or append as LIVE.
- User-reported Google Drive Trace Run Ledger v0.2, scanner v6.2.2 pilot (6 tabs/27 entries), dashboard baseline (14 unique tasks), ChatGPT export and Colorado AAOS CI failures are separate leads; refresh source evidence before asserting their present status.

## Target architecture and scope
One owner-facing instruction → ChatGPT DEBO Core → installed private Site-hosted MCP plugin → minimal Gemini adapter → structured response → *existing authorized private* R19 receipt destination → readback in ChatGPT. Expose only \`debo_gemini_execute\` and \`debo_get_receipt\` initially. Prefer direct ChatGPT Drive/Gmail/GitHub tools for their supported tasks instead of paying for redundant AI forwarding. Keep permissions and per-entity data isolation explicit. No customer, legal, health, finance, youth, credential or private cross-project evidence leaves its owning boundary without specific approval.

## Mandatory engineering repair gate (BLOCKED until tested)
1. **Transport/runtime:** Supplied \`server.ts\` uses \`StdioServerTransport\`; verify and implement the actual Site-hosted, remotely invocable MCP transport and runtime contract. Do not assume \`Node 20 + stdio\` is deployable as-is.
2. **Persistence:** The supplied \`R19ReceiptStore\` uses process-local JSONL and lock files; do not assume durable, cross-instance, cross-chat storage or atomicity across the Site's deployed instances. Use a verified existing authorized private store and a readback path; reconcile R19's actual \`debo.r19.capsule.v1\` and handoff schemas rather than invent a competing canonical receipt.
3. **Authentication:** Do not trust \`extra.authToken\` supplied as a tool argument or the server-side \`DEBO_CALLER_TOKEN\` fallback as proof of caller identity. Authenticate at the supported transport/session boundary, authorize caller + project + operation, and compare credentials safely.
4. **Idempotency/races:** Obtain durable project-scoped idempotency ownership **before** any provider call; the pasted pre-call lookup followed by post-call locked append can execute parallel duplicate paid requests. Test concurrency across workers/restarts; define safe reconciliation for failed attempts.
5. **Spend:** A four-characters-per-token estimate and fixed rates do not enforce true billing. Check current provider model/rate/quota and free-vs-paid project, cap input/output and retries, record actual usage when returned, and fail closed against unapproved paid calls. Do not turn on \`DEBO_ENABLE_LIVE_GEMINI\` merely to run a mock fixture.
6. **Validation/data:** Actually validate \`expected_output_schema\` rather than only parsing an object. Do not rely on XML delimiters alone as prompt-injection protection: restrict tools/egress, treat provider output as untrusted, enforce output schema and authorization.
7. **Build and test proof:** Add a pinned lockfile, tsconfig, runnable build command that emits/validates artifacts, exact dependency versions, mocked integration tests, and actual command receipts. The pasted test file defines **one top-level \`node:test\` test** with several assertions, not 22 individually demonstrated cases. In particular, timeout, 429, malformed output, maximum-context and single-provider fan-out need their own executed tests, as do concurrent duplicate calls and durable restart. Mark all unexecuted cases NOT RUN.
8. **Receipt fidelity:** Avoid unverifiable pasted SHA-256 values and claims that failure receipts cost $0 after an upstream request. Recompute actual input/output byte hashes, persist evidence in approved private storage, retain source and status lineage, and verify checksum with exact saved bytes after restart.
9. **Site/plugin approval:** Sites can host an MCP-backed plugin (per official OpenAI Help Center). Site owner publishing creates a plugin, and plugin install/connection requires a separate user flow. Confirm runtime networking, secret injection, data handling and privacy before deployment. Do not claim private Site *publication* or plugin installation is authorized by this document. Do not publicly publish/share.

## First milestone, acceptance and status words
- BRANCH PREPARED: code stored on isolated branch with source readback, no mainline changes.
- BUILT: executable implementation exists in checkout; package was not just pasted into conversation.
- TESTED-OFFLINE: \`npm ci && npm run build && npm test\` run against exact branch, actual test count/output recorded, with required negative and concurrency tests.
- READY_FOR_PRIVATE_SITE_REVIEW: transport, durable receipt storage, auth, privacy, budget and rollback gates reviewed; owner can inspect private preview without public release.
- INSTALLED/CONNECTED: Site owner published private Site for plugin creation with required approval; plugin installed, connected and independently read back.
- LIVE: one **authenticated** ChatGPT → Gemini provider request with approved synthetic fixture, single execution on duplicate idempotency replay, stored receipt, checksum, and later fresh-chat readback all pass against the same authorized private destination. A local process restart or a pasted JSON receipt is not this test.
- External provider subscriptions and API keys are independent of a Gemini consumer app subscription. Keep paid API execution DISABLED until explicit owner-approved budget/credentials. Check free-tier data-use/privacy implications before transmitting real records.

## Next safe actions and holds
1. Recover PR #75, PR #76 + existing R19 schema; stage and repair provided package in an isolated branch, run comprehensive offline QA. No merge, public publish, production write, billing or secret transmission.
2. Only after genuine private plugin capability and approval gates pass, test one real Gemini synthetic round trip and independently verify R19 readback in a separate ChatGPT session; record trustworthy evidence in existing Trace Run Ledger and project capsule.
3. Resume DEBO-05 authentic upstream task refresh and scanner/export read-only reconciliation once higher-priority acceptance permits; preserve DEBO-05 HOLD, browser PR #74 security HOLD and isolated business/youth project boundaries.

## Sources for reviewer
- \`DEBO_BOOTSTRAP.md\`; \`docs/DEBO_R19_CONTINUITY_ADAPTER.md\`; \`skills/multi-ai-router/\`; GitHub PRs #75, #76, #74.
- Canonical Google Drive "CURRENT — DEBO Operating Rules", v3.2 master prompt and Trace Run Ledger.
- Gemini-to-ChatGPT engineering handoff pasted by owner on 2026-11-14 (unverified code/test claims).
- https://help.openai.com/en/articles/20001547-hosting-a-plugin-with-chatgpt-sites
- https://ai.google.dev/gemini-api/docs/billing

This addendum is a reviewable candidate. It neither modifies a private canonical checkpoint nor overrides approved DEBO Golden Rules or security/owner gates.
