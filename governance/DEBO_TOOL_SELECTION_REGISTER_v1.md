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
