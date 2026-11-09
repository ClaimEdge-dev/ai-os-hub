# DEBO Tool Selection & Plugin Discovery Register v1.0
Last verified: 2026-10-20 America/Chicago. Maintainer: DEBO core. **This register is an index, not proof that every listed app is installed, authenticated, authorized, or affordable.**
Canonical runtime truth: [DEBO Runtime Verification Matrix](DEBO_RUNTIME_VERIFICATION_MATRIX_2026-10-19.md). Re-evaluate a tool when functionality, permissions, pricing, or task scope changes.

## Status vocabulary
AVAILABLE = described/offered; EXPOSED = actions in this conversation; INSTALLED = installation independently known; CONNECTED = connector session returns data; AUTHENTICATED = linked identity confirmed; AUTHORIZED = exact operation permitted; WORKFLOW-TESTED = representative task completed with output inspected. Never compress these labels into "working".

## Preferred task routes (verify permissions at runtime)
| Task | Preferred tool | Why | Fallback | Known limit / recheck trigger |
| --- | --- | --- | --- | --- |
| Retrieve DEBO code, version history, tests | GitHub connector | Canonical committed evidence | Local audited copy | Connected and read/write proven Oct 20, CI PASS not established |
| Find/edit current project documents | Google Drive connector | Existing master indexes, Docs and Sheets | ChatGPT Library for local files | Multiple Google accounts; select correct business owner before writes |
| Recover previous ChatGPT project/files | Personal context + Files | Find existing decisions before recreation | User-supplied source | Retrieval coverage incomplete; not omniscient |
| Generate private working report | Local artifact tools (Python, DOCX/PDF/Sheets skills) | Readable controlled artifact with tests | Drive-native file | User must choose authorized sharing destination |
| Long, multi-app browser work | ChatGPT Work when present | Navigate and verify real workflow | Focused connector calls | Work mode availability and quotas require account check |
| Project code/change/test | GitHub + appropriate coding runtime | Reviewable diff and reproducible tests | Local test sandbox | Merge/production release gate |
| CompanyCam photo/job evidence | CompanyCam connector | Native field media and context | Authorized read-only export | Both CompanyCam spellings currently same ClaimEdge tenant 1520702; not D-Wing |
| D-Wing job-photo link | Leap CRM native CompanyCam integration | Documented official connection; avoids duplicate sync | Scoped API/webhook bridge | Target Leap account and D-Wing CompanyCam permission NOT VERIFIED |
| Custom CompanyCam integration | Current API / beta MCP | Supported projects/photos/webhooks | Native integration first | Plan and admin authorization; legacy API sunset risk |
| Website UI components/brand kit | Figma connected tools | Reusable editable components/Code Connect | Existing Canva/Adobe asset | Full seat / rate limits may apply; don't rebuild approved artwork |
| Marketing one-offs | Canva or Adobe, if connected | Fast production templates | Existing files/Figma | Permissions and asset rights |
| Website implementation | Existing source project + Vercel/Lovable/Higgsfield connector | Preserve working app and deployment trail | Local preview | Preview READY ≠ working production; launch gated |
| Structured registry / DB | Existing Neon/Supabase project | Durable data with querying, audit | Google Sheet | Avoid duplicate truth, verify schema and authorization |
| Business task board | Existing Linear/ClickUp/Airtable where in use | Assignable work and clear handoffs | GitHub issues / Drive ledger | Don't add third task manager |
| Time and usage measurement | Connector execution events + recorded timestamps | Measured event ledger | Manual once per milestone | Exact labor hours/billing unknown until source records checked |
| Scheduled watch/reminder | ChatGPT Tasks / Work | Events or cadence with host-managed delivery | Calendar reminder | Create only when requested, inspect existing tasks first |
| Research latest official docs | Native web research | Source links and recency | Exa/Firecrawl specialized if needed | Costs / quota unknown |
| Kimi large context / code | Existing Kimi subscription if verified | External coding/research alternative | ChatGPT/Codex | Different app, no invisible shared memory; current credits unknown |
| Gemini/Workspace | Google Workspace/Gemini when authorized | Docs/Gmail/calendar-native work | Google Drive connector | Feature/plan access not established by this register |
| Perplexity research | Perplexity if directly accessible | Parallel cited research | Native web | Import findings with sources; no assumed cross-AI sync |
| Grok | Only unique, tested capability | Optional parallel exploration | Native research | No demonstrated necessity |
| Long-tail plugins | Inventory, park until use case arises | Reduce maintenance & distraction | Existing preferred app | Exposed does not mean installed or connected |

## Confirmed evidence checks on Oct 20
1. GitHub repo `ClaimEdge-dev/ai-os-hub` accessible, modification of verification matrix committed and read back.
2. Google Drive file search returned existing DEBO documents (operating rules, skills registry, trace ledger) from a linked account.
3. `CompanyCam.get_current_user` and `Company_cam.get_current_user` returned **the same company_id: 1520702**. Route them as duplicate connector surfaces; do not treat as two company accounts or duplicate-install blindly.
4. Official Leap CRM ↔ CompanyCam integration: https://companycam.com/integrations/leap
5. Official CompanyCam API: https://help.companycam.com/en/articles/15949273-building-custom-integrations-with-companycam-s-api
6. Official CompanyCam MCP beta: https://help.companycam.com/en/articles/15928195-connecting-the-companycam-mcp-server-beta
7. OpenAI plugin/permission docs: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
8. Figma MCP tool docs: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
9. Kimi capabilities documentation: https://www.kimi.ai/help/agent/agent-overview
10. All pricing, seat, account quotas, OAuth permissions and billing must be checked per target app before purchase/use.

## Exposed app-tool families (discovery only)
Discovery is a snapshot of names and tool counts exposed to this assistant, **not an installed-plugin list**. Actions from different families may overlap, and availability/permissions are variable.

| Tool family | Exposed action count | Current evaluation |
| --- | ---: | --- |
| Ace Quiz Maker | 7 | EXPOSED / NOT YET EVALUATED |
| Adobe | 83 | EXPOSED / NOT YET EVALUATED |
| Adobe Acrobat | 19 | EXPOSED / NOT YET EVALUATED |
| Adobe Express | 7 | EXPOSED / NOT YET EVALUATED |
| Airtable | 47 | EXPOSED / NOT YET EVALUATED |
| Alpaca | 24 | EXPOSED / NOT YET EVALUATED |
| AnyPDF | 7 | EXPOSED / NOT YET EVALUATED |
| Apollo io | 72 | EXPOSED / NOT YET EVALUATED |
| AppDeploy | 24 | EXPOSED / NOT YET EVALUATED |
| Auto | 17 | EXPOSED / NOT YET EVALUATED |
| B A | 8 | EXPOSED / NOT YET EVALUATED |
| Base44 | 22 | EXPOSED / NOT YET EVALUATED |
| Canva | 40 | EXPOSED / NOT YET EVALUATED |
| ClickUp | 61 | EXPOSED / NOT YET EVALUATED |
| Code Tytor | 11 | EXPOSED / NOT YET EVALUATED |
| Codex Tasks | 5 | EXPOSED / NOT YET EVALUATED |
| Company cam | 98 | EXPOSED / NOT YET EVALUATED |
| CompanyCam | 96 | EXPOSED / NOT YET EVALUATED |
| Coursera Learning | 9 | EXPOSED / NOT YET EVALUATED |
| Courtroom5 | 3 | EXPOSED / NOT YET EVALUATED |
| DataCamp | 101 | EXPOSED / NOT YET EVALUATED |
| Descript | 16 | EXPOSED / NOT YET EVALUATED |
| Dispatcher City | 3 | EXPOSED / NOT YET EVALUATED |
| Dropbox | 24 | EXPOSED / NOT YET EVALUATED |
| Exa | 2 | EXPOSED / NOT YET EVALUATED |
| Figma | 48 | EXPOSED / NOT YET EVALUATED |
| Finances | 14 | EXPOSED / NOT YET EVALUATED |
| Firecrawl | 28 | EXPOSED / NOT YET EVALUATED |
| Floot | 44 | EXPOSED / NOT YET EVALUATED |
| Found | 6 | EXPOSED / NOT YET EVALUATED |
| Gamma | 21 | EXPOSED / NOT YET EVALUATED |
| getMindmap | 2 | EXPOSED / NOT YET EVALUATED |
| GitBook | 11 | EXPOSED / NOT YET EVALUATED |
| GitHub | 89 | EXPOSED / NOT YET EVALUATED |
| GitLab | 128 | EXPOSED / NOT YET EVALUATED |
| Gmail | 21 | EXPOSED / NOT YET EVALUATED |
| Google Calendar | 15 | EXPOSED / NOT YET EVALUATED |
| Google Contacts | 3 | EXPOSED / NOT YET EVALUATED |
| Google Drive | 45 | EXPOSED / NOT YET EVALUATED |
| Grow My Website | 3 | EXPOSED / NOT YET EVALUATED |
| GSC Wizard | 131 | EXPOSED / NOT YET EVALUATED |
| Health | 11 | EXPOSED / NOT YET EVALUATED |
| Higgsfield | 143 | EXPOSED / NOT YET EVALUATED |
| HoneyBook | 7 | EXPOSED / NOT YET EVALUATED |
| HubSpot | 33 | EXPOSED / NOT YET EVALUATED |
| Indeed Job Search | 3 | EXPOSED / NOT YET EVALUATED |
| Intuit Credit Karma | 4 | EXPOSED / NOT YET EVALUATED |
| Intuit QuickBooks | 91 | EXPOSED / NOT YET EVALUATED |
| Jotform | 9 | EXPOSED / NOT YET EVALUATED |
| Jotform Apps | 6 | EXPOSED / NOT YET EVALUATED |
| Legal Data Hunter | 7 | EXPOSED / NOT YET EVALUATED |
| Linear | 74 | EXPOSED / NOT YET EVALUATED |
| Lovable | 41 | EXPOSED / NOT YET EVALUATED |
| Lusha | 50 | EXPOSED / NOT YET EVALUATED |
| Magnific | 222 | EXPOSED / NOT YET EVALUATED |
| Mailopoly Inbox | 103 | EXPOSED / NOT YET EVALUATED |
| Manus | 5 | EXPOSED / NOT YET EVALUATED |
| MarcoPolo | 5 | EXPOSED / NOT YET EVALUATED |
| Mermaid Chart | 2 | EXPOSED / NOT YET EVALUATED |
| Metricool | 9 | EXPOSED / NOT YET EVALUATED |
| Microsoft Outlook Calendar | 27 | EXPOSED / NOT YET EVALUATED |
| Microsoft Outlook Email | 38 | EXPOSED / NOT YET EVALUATED |
| Microsoft SharePoint | 20 | EXPOSED / NOT YET EVALUATED |
| Midpage Legal Research | 6 | EXPOSED / NOT YET EVALUATED |
| monday com | 110 | EXPOSED / NOT YET EVALUATED |
| Neon | 119 | EXPOSED / NOT YET EVALUATED |
| Notion | 26 | EXPOSED / NOT YET EVALUATED |
| Opera Browser Connector | 8 | EXPOSED / NOT YET EVALUATED |
| Parallel Search | 2 | EXPOSED / NOT YET EVALUATED |
| Perchli Property Search | 5 | EXPOSED / NOT YET EVALUATED |
| Plugin Management | 6 | EXPOSED / NOT YET EVALUATED |
| Realtor com | 13 | EXPOSED / NOT YET EVALUATED |
| Redfin | 2 | EXPOSED / NOT YET EVALUATED |
| Remote Desktop Commander | 31 | EXPOSED / NOT YET EVALUATED |
| Replit | 8 | EXPOSED / NOT YET EVALUATED |
| Semrush | 14 | EXPOSED / NOT YET EVALUATED |
| Sider Scholar | 18 | EXPOSED / NOT YET EVALUATED |
| Slack | 38 | EXPOSED / NOT YET EVALUATED |
| Soluvery | 11 | EXPOSED / NOT YET EVALUATED |
| Soul Family AI | 6 | EXPOSED / NOT YET EVALUATED |
| Stack Overflow For Agents | 25 | EXPOSED / NOT YET EVALUATED |
| Supabase | 29 | EXPOSED / NOT YET EVALUATED |
| Tarot | 1 | EXPOSED / NOT YET EVALUATED |
| The Astro Scope Tarot Reading | 3 | EXPOSED / NOT YET EVALUATED |
| TinyFish | 20 | EXPOSED / NOT YET EVALUATED |
| Todoist | 47 | EXPOSED / NOT YET EVALUATED |
| Tripsy | 54 | EXPOSED / NOT YET EVALUATED |
| Ubersuggest | 59 | EXPOSED / NOT YET EVALUATED |
| VEED Video Generator | 7 | EXPOSED / NOT YET EVALUATED |
| Vercel | 235 | EXPOSED / NOT YET EVALUATED |
| vidIQ | 70 | EXPOSED / NOT YET EVALUATED |
| Webflow | 37 | EXPOSED / NOT YET EVALUATED |
| Windsor ai Facebook Ads | 18 | EXPOSED / NOT YET EVALUATED |
| Wolfram | 3 | EXPOSED / NOT YET EVALUATED |
| Writing Style | 2 | EXPOSED / NOT YET EVALUATED |
| Zillow | 9 | EXPOSED / NOT YET EVALUATED |
| ZoomInfo | 20 | EXPOSED / NOT YET EVALUATED |

## Anti-repeat decision
Before each new integration: check existing native connection -> check target company identity/permissions -> check whether desired data is already present -> propose smallest missing adapter -> dry-run with synthetic records -> verify access, logging, dedupe, retries, source references -> only then request production release. Log negative tests, not merely happy-path demos.


## Sports workflow tool routing — Oct 20 evidence delta
Sports source files read from GitHub: `governance/sister-brains/BULLDOGS_PROFILE_v1.md`, `athleteos/video-ai/PLAYBOOK_BENCHMARK_v0.2.md`, `skills/wrestling-extraction-suite/SKILL.md` and `skills/wrestling-intelligence-master/SKILL.md`. Source availability is not installation or workflow-test evidence.

| Task type | First-choice existing tool/source | Reason | Fallback | Runtime evidence / blocker |
| --- | --- | --- | --- | --- |
| Bulldogs roster and playbook truth | Existing coach-approved team register and original playbook in Drive, versioned GitHub benchmark | Native team source, allows coach review | Human reviewed private upload | Exact Drive document contents, team permissions and film rights need current check |
| Bulldogs game film analysis | Existing AthleteOS benchmark with source film and reviewed tags | Reuse call vocabulary; one film-to-play acceptance | Manual clip tags | NO live model accuracy/production pipeline demonstrated |
| Wrestling tournament and achievement histories | Official public event/bracket sources + existing wrestling extraction skill source | Direct evidence, source/version provenance | Restricted read-only authorized export | Skill source fetched; trigger/extraction not tested |
| Hitters baseball scores, roster, tournaments | Authorized originals in existing Hitters Drive folders and provider accounts (GameChanger etc. only if authorized) | Avoid duplicate app/database and unlicensed scraping | Coach-approved scorecard import | Third-party live connectors and reuse rights unverified |
| Sports schedule and team events | Existing authorized team calendar and Google Calendar connector | Avoid duplicate events | Manual source-backed calendar import | Account ownership and write authorization not tested |
| Shared athlete identity/permissions | Existing project registry and secure access-controlled data store | Link one athlete to many team-season records without publishing minors | Private, pseudonymized spreadsheet pilot | DB schema proposal only; no migrations tested |
| Social highlights and athlete marketing | Existing media/brand apps + explicit guardian/coach/media rights | Preserve ownership and consent | Private draft review | No child/public post without approval |
| Official honors, league rules, eligibility | League/team/school primary sources with season/version | Prevent mistaken awards and allegations | Authorized registrar review | No automatic classification or public allegations |
| Registration and operational sports management | Existing authorized Hudl/GameChanger/TeamSnap/SportsEngine/LeagueApps/etc. only where already in use | Prefer native software over custom rebuilds | Existing Drive roster | Plan, account connection, licensing and data-export access still unknown |

Privacy gate: Do not use public repo as a youth identity store. Availability of search or linked media is not consent to republish. Research records should track source, date, identity match basis, guardian/media permissions, season and authority level. New app/plugin installations require demonstrated work fit, free-tier suitability and reversible authorization.


## Plugin selection governor v1.1 — 2026-11-03 (DEBO-wide, inherited through an actual loader)

**Intent:** DEBO must automatically **select and use** the least-complex *existing, authorized* capability for each meaningful task; automatically **discover and recommend** a useful missing app only when necessary; and automatically **detect/report a candidate update** to an installed app or skill. A suggestion, saved rule, enabled tool, connector connection, or scheduled Scout run does not independently prove invocation or delivery. This is the canonical tool-governance rule, not a new app, second master, plugin, or scheduler. The governing runtime bootstrap and actual project approval boundaries always take precedence.

**Execution trigger:** substantial new objective, source/permission/cost change, stale/failed tool, new requested integration, recurring manual action, or existing weekly DEBO System Scout. Do not turn an ordinary one-line chat reply into a tool hunt. Recover current project canon, approved apps, recent Scout findings, and the exact intended output before discovery.

### Choose → evaluate → act

1. **DEFINE:** state the task's concrete outcome, business/project ID and account, data sensitivity, output, desired freshness, needed read/write scope, and owner/human approval gate. Use user instructions and evidence already known; avoid needless intake questions.
2. **RECOVER:** check the installed eight DEBO Core skills, this register, relevant project adapter, **current** app catalog state, canonical artifacts and prior trial receipts. Do not confuse an exposed action with an installed/connected app or an old tool list with live status.
3. **ROUTE (default):** private project files → Files/Library or authorized Google Drive/Notion; public quick evidence → native ChatGPT Search; multi-source investigated report → Deep Research; reproducible code and tests → existing Python/Codex/GitHub; multi-page public structured retrieval → existing Firecrawl; explicitly permitted interactive browser workflow → Work/TinyFish; project business records → *their own* authorized CompanyCam/CRM/finance/operations app; scheduled monitoring → existing task first. Keep private records and minors out of unrelated providers. Do not use browser automation to evade authentication or bypass an unavailable native connector.
4. **STATUS CHECK:** record AVAILABLE, EXPOSED, INSTALLED, CONNECTED, AUTHENTICATED, AUTHORIZED, WORKFLOW-TESTED separately for each shortlisted app, with actual workspace/account and source of evidence. Installed globally != authenticated for the requested company. Unknown means UNKNOWN, not "not installed".
5. **DECIDE:** **USE** a fit, currently authorized existing app; **UPDATE** an existing adapter when features/versions are stale; **MERGE** overlapping skills to one canonical route; **DISCOVER/SUGGEST** a new app only for a demonstrated missing capability or evidence-backed superiority; **PILOT** unfamiliar behavior with synthetic/non-sensitive data; **HOLD** anything with missing authority, cost approval, permissions or runtime proof; **RETIRE** only after dependency/rollback review and explicit authorization. Prefer the smallest complete stack.
6. **AUTOMATIC USE (bounded):** choose and invoke existing tool(s) automatically for ordinary read-only and task-scoped actions within the user's expressed objective and connector permissions; perform safe reversible internal edits only when authorization and expected downstream impact are clear. For external messages, payments, public deployment, irreversible deletion, broad access, sensitive customer/minor records, confidential cross-tenant transfer, or legal/regulatory submission, **obtain explicit required approval first**. Never silently install, connect, purchase, change permission modes, enable automation or deploy. Tool selection is not authority to perform every tool action.
7. **AUTO-DISCOVERY / SUGGESTION:** if a real capability gap remains, search current plugin catalog for relevant provider/category; rank up to **two** candidates using specific use case, overlapping installed alternatives, source coverage, maintenance/security posture, permissions, expected benefit, marginal cost, provider quota, support, export/exit plan. Recommend only when the benefit materially advances the ongoing task. No duplicate suggestions within seven days unless the user explicitly re-requests installation. Let the user authorize any connection; a recommendation alone does not create a link.
8. **AUTO-UPDATE ADVISOR:** weekly existing DEBO System Scout and task-time checks inspect official changelog, removed functionality, connector/tool/schema drift, pricing/quota/terms, and recurring failures. Prefer provider-managed automatic updates where supported; **do not** arbitrarily upgrade a dependency or source skill because the version number is larger. For a real needed change, create a small source diff/version, run existing regression tests and negative permission cases, compare behavior and cost, present risk/rollback, and promote only after required approvals and readback.
9. **NO DUPLICATE AUTOMATION:** inspect saved scheduled tasks before offering a monitor. Extend the existing weekly DEBO System Scout for plugin discovery, not a second Plugin Scout, cron job, CRM, skill registry, or dashboard. A scheduled prompt is not proof of a continuously running agent. Conditional monitoring must use a supported provider trigger; otherwise retain an explicit scheduled/manual fallback.
10. **FAILURE AND RECOVERY:** read exact provider/tool error, account, scope, quota and time. Attempt at most one *different authorized* diagnostic or fallback, record the blocker and retry condition, and complete unblocked work. Never bypass auth, MFA, safety checks, rate limits, paywalls or service restrictions.
11. **MEASURE AND REUSE:** store task-to-tool choice, source links and dates, cost/rate-limit signals, measured time/rework **only when observed**, permissions, test receipts, remaining risks and one next action in the existing DEBO Scorecard Keeper / ThreadOps checkpoint. No separate Plugin OS, hidden user-data collection or uncontrolled cross-app memory. If another tool gives no demonstrated improvement, keep the current default.

### Plugin decision score (reviewed judgment, not invented numerical ROI)

Assess each candidate on task effectiveness, evidence/source accuracy, time saved from measured work, integration/maintenance burden, security and tenant isolation, owner authority, cost/quota, availability, reversibility and data portability. Use **BLOCKED** for failed permission/cost/safety gates regardless of total score. If two candidates meet requirements, prefer an already connected one with no new permissions. A trial should have a real acceptance question, inspected output and a rollback plan. Do not infer payback time or assign fake financial savings.

### Current prioritization snapshot (2026-11-03; re-check before task-specific action)

| Priority | Capability | Status checked in ChatGPT | Use / next step |
| --- | --- | --- | --- |
| P0 | Native Search, Files/Library, GitHub, Notion, Google Drive, Python, existing CI | Native/built-in or installed, but exact operation permissions vary | Source retrieval, evidence, versions, actual QA and durable checkpoint. Use first. |
| P0 | DEBO Core v0.1.0 eight private skill adapters | Prior runtime readback reported eight accessible and a successful DEBO START read; future-chat auto boot unverified | Reuse; version existing adapter after tests, do not duplicate brain. |
| P0 | Existing DEBO System Scout and Morning Brief | Saved enabled task records; successful prior runs do not prove every current feature works | Use existing weekly and daily task schedule. |
| P1 | Firecrawl and TinyFish | Installed; business/account-specific workflow authorization unverified | Multi-page public extraction and permitted browser interactions, only when Search is insufficient. |
| P1 | HubSpot, Airtable, Linear, Todoist, Supabase, Neon and existing business tools | Installed by catalog when indicated; workspace-specific authority/connected identity not proven by catalog | Use ONLY the business's canonical CRM/task/DB; avoid a second source of truth. |
| P1 | Figma, Canva, MagicPath and existing design tools | Installed per catalog; actual project seat/tool action must be verified | Reuse brand and design assets; do not rebuild approved websites or create competing design systems. |
| P1 | Similarweb | User connected via surfaced plugin suggestion on 2026-11-03; specific analytics call and credits **NOT TESTED** | Candidate market/domain benchmark; use after a business-specific research objective and consent, verify sampling/limits. |
| P2 | G2 MCP | Suggested, connection pending as of this snapshot | Compare software alternatives using user reviews before switching tools; optional, no core dependency. |
| P2 | Windsor.ai, Ahrefs, Otter.ai or other specialist analytics/meeting sources | Catalog candidates, NOT installed unless independently rechecked | Only if existing marketing/meeting evidence cannot answer the actual question; verify pricing and data permissions first. |
| HOLD | More dashboards, general CRM/project manager, all JCT/RRR source skills, more master brains | Existing approved alternatives already present | Do not bulk install or migrate production for speculative benefits. |

### Evidence / promotion receipt schema (reuse existing ledgers)

\`mission_id\`, \`project_id\`, \`task_outcome\`, \`decision\` (USE/UPDATE/MERGE/SUGGEST/PILOT/HOLD/RETIRE), \`provider\`, \`app_id\`, \`capability\`, \`installed_state\`, \`connected_account_scope\`, \`operation_authority\`, \`requested_permissions\`, \`source_revision\`, \`quota_or_price_verified_at\`, \`privacy_risk\`, \`alternatives_compared\`, \`test_type\`, \`test_result\`, \`artifact_url_or_id\`, \`readback_receipt\`, \`rollback\`, \`checkpoint\`, \`next_action\`, \`checked_at\`. Redact credential material and private identifiers in public GitHub files; store private receipts only in an authorized private project source. Any missing evidence is explicitly UNKNOWN.

**Quality gates / acceptance cases:** (a) already connected tool selected without new install; (b) unsupported app suggestion rejected when existing tool fully meets task; (c) new app suggested at most once per 7 days without explicit re-request; (d) protected customer/public/write operation stops for exact owner approval; (e) failure shows a real fallback rather than claiming task completion; (f) business-A data never routes into business-B; (g) installed/connected/authorized/tested are never collapsed; (h) plugin update waits for regression/rollback checks. This policy is documentation until exercised in the actual ChatGPT Core/Scout runtime.

**Ownership:** Multi-AI Router + ChatGPT Surface Router choose tool; Skill Lifecycle Manager governs adapter changes; Universal File Vault records verified artifacts; DEBO System Scout discovers candidates; Robert Master OS prioritizes; existing project approval policies control effects. No separate agent roles or independent always-on plugin manager are implied.

## R136 verified Figma, Supabase and Airtable routing (2026-11-09)

**Mission:** DEBO-MASTER-R136 / per-project adapter routing. **Scope:** verified account discovery and governance only; not production migration, automatic ChatGPT plugin deployment, connector permission change, app publication or background runtime activation.

| Capability | Verified connected state | Appropriate existing route | Guardrail / next acceptance |
| --- | --- | --- | --- |
| Figma | Installed and authenticated account returned a Starter **View seat**; no file-level edit or export tested | Design references, components and private mobile UX review for DEBO-05, JCT and other approved projects | Do not assert editable design access, upgrade a seat, create paid usage, or replace source designs; check the exact Figma file and user seat before a write |
| Supabase | Installed and project listing authenticated. Two entries visible: **RRR — Rapid Roadside Repair** is **INACTIVE**; one generic personal project is ACTIVE_HEALTHY but has **no established DEBO project assignment** | Reuse a project's existing Supabase only where separately mapped and authorized (e.g., RRR recovery and known sister-system adapters); leave DEBO-05's established Neon source unchanged | No new Supabase project, migration, branch, resume, auth policy or cross-project data sync without project identity and scope check. Check fees first; maintain RLS and rollback |
| Airtable | Installed and connector returned **zero accessible bases** | Optional structured inventory/projection only when an existing approved base becomes available; current DEBO task, idea and source canon stays in Notion/Drive/GitHub | No Airtable base created or records migrated; verify workspace, ownership and duplicate-prevention first |

**Tool-role install for all upgrades:** Use the existing plugin selection governor as the per-task router. For each DEBO project and upgrade: discover relevant installed connector, verify exact business account and operating rights, use the canonical source, make bounded changes, run affected tests, read back the result, and checkpoint. Do **not** connect a plugin to every project indiscriminately, replicate all business data into Airtable or Supabase, create a competing source of truth, or treat plugin installation as code/runtime installation. DEBO-05 remains GitHub + Vercel + Neon with protected sign-in; Figma is optional read-only design review; Notion is knowledge registry and Drive original evidence. JCT/RRR and each sister project retain their own verified business adapters. Owner-authorized public deployment must still pass security, private information and role access gates.

**Read-only discovery evidence:** Figma `whoami`, Supabase `list_projects`, Airtable `list_bases`, and current installed-plugin directory check on 2026-11-09. No secrets, private workspace email, or raw customer records recorded in this public register. **Status:** routing rule saved in source when committed; individual plugin work inside each project remains untested until actual task-specific execution.

## R137 continuous plugin inventory and owner learning contract (2026-11-09)

**Owner instruction:** Always know which DEBO-relevant apps/plugins and features are available when supported by live discovery; explain and recommend their uses at the relevant moment. The owner orally named a broad set of plugins; many names are ambiguous voice transcription and must be resolved via the current plugin directory before marking INSTALLED. Preserve exact unknown names as UNRESOLVED aliases rather than creating fake plugin records. This updates the **existing** governor and Scout, not a second source of truth.

**Discovery triggers:** a new task needing external data/software, an owner-reported install/connection/disconnection, a tool failure/capability change, a major feature release, and the existing weekly DEBO System Scout. On each trigger, use the current directory and the actual connector session/tenant where material; inspect changed features against vendor docs or relevant live tools. Verify installed separately from connected, authenticated, action-authorized, workflow-tested and deployed. Historical installed lists are not live proof; a directory search may be partial.

**Automatic maintenance within available authorization:** refresh the existing DEBO tool register/Skill Registry/Notion checkpoint with a minimal changed-field delta only when authenticated write access and evidence exist, read back the saved result, and record source/time. Do not duplicate a whole catalog or assert unperformed cross-chat synchronization. Weekly Scout may report diffs and suggest changes; it cannot magically detect a plug-in install between runs or update a ChatGPT account setting without a supported authorization path. If no write tool or permission, leave a NOT_SAVED checkpoint.

**Teach in context:** for each proposed plugin, give five concise fields: `What it is`; `What it does` (2-4 concrete features); `When DEBO would use it` (one actual project/task); `What it produces` (example output); and `Requirements` (account/permissions/limits/possible cost). When recommending action, make one best recommendation and a short beginner-friendly example. Define unfamiliar jargon once. Prefer current existing tools and explicitly say if the user already has the right plugin. Never sell new subscriptions by default; mention not-connected/not-tested truthfully.

**Ownership and boundaries:** GitHub = source and code; Notion = durable knowledge and capabilities; Drive = original evidence; DEBO dashboard = protected command interface; canonical project apps keep their own business records. No blind mirroring of all plugins to all projects, duplicate CRM/databases, permission broadening, unsafe health/finance/youth data crossover, unattended purchases, or unapproved publishing. Owners may authorize release per project; production still requires security and privacy acceptance.

**Current task receipt:** R136 Figma account authenticated with Starter View seat; Supabase only two visible projects with inactive RRR and unassigned personal project; Airtable connector returned zero accessible bases. R135 GitHub/Vercel tools worked; TinyFish default browser profile had no proven Vercel login. These are dated snapshots requiring refresh, not permanent states. Existing enabled `DEBO System Scout` weekly Monday task found in Automations; extend its current task instructions without creating another automation.
