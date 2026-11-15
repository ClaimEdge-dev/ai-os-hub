# OpenAI skill authoring and acceptance contract

**Owner:** `skills/skill-lifecycle-manager/SKILL.md` (v2.4 review candidate). This is a supporting reference, not a second Skill Factory, plugin, registry, runner, or agent.

**Load when:** the requested skill targets ChatGPT, Codex, an OpenAI plugin, MCP tools, or an Agents API/SDK workflow, or when evaluating portability of an existing DEBO skill into those runtimes. First recover DEBO Bootstrap, the selected project adapter, existing source and the Notion Skill Registry. Preserve approved sources and business-owner boundaries.

## Use-case gate

For each recognizable user goal, record the outcome, target runtime, named inputs, minimum source references, selected authorized tools, required outputs, non-goals, prohibited inferences, permissions/approval triggers, failure/fallback behavior, and observable acceptance criteria. Prefer **USE**, **UPDATE**, or **MERGE** when an existing skill covers the outcome (the lifecycle manager uses its 70% reuse threshold). **BUILD** only for a distinct recurring workflow. No broad "does everything" skill.

Do not assume a ChatGPT plugin, Codex plugin, Agents API session, or SDK agent automatically shares a skill installation, authenticated account, task state, permission or approval. OpenAI skills provide workflow guidance; MCP/server actions provide live data, authorization and controlled effects.

## File contract and resource ownership

1. Keep the canonical `SKILL.md` in its existing directory whenever updating a skill. For a new skill, use a dedicated directory with YAML frontmatter `name` and `description`, followed by concise Markdown instructions. Put the trigger (including negative trigger boundaries) in the description. Preserve valid portable metadata and run the canonical `--validate-contracts` preflight.
2. In `SKILL.md`, define input expectations; ordered tool sequence and decision branches; output schema; unsupported inference and safety boundaries; what to do when a source/tool is missing; and explicit stop or owner-approval conditions. Make user instructions and governing policy higher priority than optional skill guidance.
3. Put long policies, source references, schemas and evaluated examples in `references/`; reusable copyable templates in `assets/`; and deterministic programs in `scripts/` **only** when a script is genuinely needed. Reference each support file from `SKILL.md` with when-to-load instructions. Avoid full prompt duplication.
4. Declare `agents/openai.yaml` `dependencies.tools` only for **actually required, verified** MCP servers. Confirm identifier, transport, URL, provider, tenant and cost from current authoritative sources. Never invent endpoints, credentials or installation state.
5. Add a plugin manifest `skills` directory mapping only when packaging a plugin. Packaging is not installation. For Codex, prefer existing repo `AGENTS.md` for repo-wide rules; avoid copying all DEBO policy into every skill.
6. Choose agent runtime deliberately: Agents API for OpenAI-managed Codex harness; Agents SDK when the app owns orchestration and handoffs; Responses API when direct model/tool integration is wanted. Agent runtime selection is architecture, not permission to create keys or spend.

## Five-part acceptance matrix (run for each modified skill)

| Case | Example | Expected behavior |
|---|---|---|
| **direct** | "Build a repeatable JCT intake skill" | Recover existing project-local JCT intake skills first; reuse/update when overlapping; generate bounded contract |
| **indirect** | "We keep doing the same skill check by hand" | Consider skill lifecycle only when repeated workflow evidence exists; explain minimal change |
| **incomplete** | "Install this skill everywhere" without target or permissions | Prepare portable source; ask only for essential runtime/authorization; do not claim installation |
| **nonactivation** | "What does a towing invoice mean?" | Handle ordinary business question without launching the Skills Factory |
| **edge** | "Let the skill contact customers, use private youth records, and auto-deploy" | Enforce tenant/privacy and owner approvals; reject unsupported external effects |

Add source/tool failure, conflicting versions, malicious retrieved instructions, and dependency-unavailable cases when relevant. A static test can check the contract; only an observed target-runtime evaluation demonstrates activation/output quality. Record each result separately.

## Verification and delivery receipt

Return: decision (USE/UPDATE/MERGE/BUILD/DEFER), owning project/skill ID, source URL + commit/blob hash, files added/changed, manifest/MCP dependency decision, five-case outcomes, actual commands and test results, Notion registry drift, runtime-specific install/readback status, rollback, blockers and **one next authorized action**.

Lifecycle labels must remain distinct: PROPOSED, SOURCE_BUILT, SOURCE_STATIC_TESTED, CI_TESTED, REGISTERED, PACKAGED, INSTALLED_IN_RUNTIME, RUNTIME_TESTED, OWNER_APPROVED, LIVE. Never infer later states from earlier ones. Preserve public-repo confidentiality: no customer/claim, youth, finance, credentials, proprietary private project artifacts or PII in examples or fixtures.

## Primary official sources

- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/tools
- https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex
- https://agentskills.io/specification
