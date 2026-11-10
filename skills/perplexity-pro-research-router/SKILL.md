---
name: perplexity-pro-research-router
description: Select the appropriate Perplexity Pro search mode and available AI model for DEBO research, source verification, technical reasoning and document synthesis. Trigger on "research with Perplexity", model choice, Perplexity research handoffs, or a Perplexity Pro account inventory.
---

# Perplexity Pro Research Router v1.0

Owner: DEBO / Scout. Source candidate only. Canon: \`DEBO_BOOTSTRAP.md\`, \`skills/multi-ai-router/SKILL.md\`, and the latest project checkpoint. This is an adapter, **not** a second AI router.

## Account facts for this mission
The owner reports **Perplexity Pro**, **without access to Perplexity Computer**. Treat Computer as UNAVAILABLE for this workflow regardless of marketing, until the owner reports a change and the actual session independently verifies it. Do not route to Computer, its Light/Standard/High/Ultra controls, or Max-exclusive options. Do not buy or upgrade plans.

## Select the task first, model second
Use \`tools/debo_perplexity_pro_route.py\` to obtain a source-only decision card. Confirm available models in the user's current model dropdown before choosing any named model; if not seen, use Best/automatic and mark unverified. Choose one primary model and an independent verification pass only for material conclusions. Never claim one model is universally "best".

| Job | Pro mode | Suggested model when present | Why and QA |
| --- | --- | --- | --- |
| Fast fact, URL, release notes, one official source | Best | Automatic | Fastest. Open primary link if decision-critical. |
| Quick source comparison, local/current external research | Pro Search | Sonar | Search-first citations; verify dates and source quality. |
| Technical specs, APIs, structured requirements, code explanations | Pro Search | Available GPT-series model | Structured reasoning; validate code/source version independently. |
| Long document interpretation, contracts, strategy, nuanced argument | Pro Search / Reasoning if shown | Claude Sonnet / Thinking variant | Careful textual analysis; never substitute for legal/owner approval. |
| Long multimodal material, cross-document comparison, images | Pro Search | Gemini Pro family if shown | Multimodal candidate; verify extracted details. |
| Broad complex landscape, many sources, disputed findings | Research | Automatic combined model selection | Deep synthesis; verify decisive sources separately. |
| Private Perplexity account inventory, saved threads, files, skills | Existing account history / authorized export, not Pro web search | N/A | Pro Search cannot read private history without explicit first-party access. |

Specific model names and access can change; verify official current docs and in-account menu. Family preferences are operational hypotheses, not benchmark results.

## Research execution contract
1. Recover DEBO master bootstrap and relevant adapter, then check previous research packet, source fingerprint, Notion checkpoint, settled decisions, and project scope. Do not relaunch identical research.
2. Define question, date range, geography, target projects, output format and 3–5 most important evidence gaps.
3. Choose search mode above, confirm availability/quota when exposed, keep prompts focused, separate primary sources from Reddit/forum opinions and identify stale evidence.
4. For decisive facts capture claim, source URL, publication/effective date, retrieved date, quote under applicable limits, contradiction, and verification status. A citation link does not prove a claim.
5. Return a small research packet to DEBO. Use existing Notion/Drive project vault only if Perplexity has verified write access; otherwise provide one pasteable packet. A Pro subscription alone does not authorize API calls or access to other apps.
6. Require DEBO review before classifying recommendations as approved, installing skills, changing an account, publishing, or merging code.

## Perplexity account inventory
Use the separate \`cross-ai-artifact-inventory\` skill. With a real authenticated account session, enumerate only visible search threads, Projects (or legacy Spaces), user-uploaded files, generated artifacts, settings, preferences, memories, model list, quota and enabled integrations. Where supported, the owner can request a first-party data export from https://www.perplexity.ai/account/details; classify data as PRIVATE, collect only needed fields, and redact before cross-system handoff. Without such access, mark scope NOT READ rather than "empty". Do not create connectors, move data or change memory/settings without scope approval.

## Negative tests
- User reports Pro but no Computer: never recommend Computer as the execution mode.
- No Perplexity account connector: do not claim private account inventory.
- Model missing from user menu: use Best/automatic rather than insist on a named model.
- One trivial question: do not burn a Research run.
- Protected customer/child/private source: never publish to public GitHub or share between business tenants.
- No writable Notion from Perplexity: return packet with UNSAVED tag, do not claim auto-sync.

## Evidence
Official documentation: https://www.perplexity.ai/help-center/en/articles/10352901-what-is-perplexity-pro ; https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search ; https://www.perplexity.ai/en-GB/hub/legal/self-serve-data-options . Last source check: 2026-11-10. Refresh if mode/model menu changes.
