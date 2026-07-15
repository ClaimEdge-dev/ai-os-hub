<!-- CONTINUED FROM PART 2 -->
<!-- prompts — PART 3 of 4 -->

## By Domain

| Domain | Primary AI | Secondary AI | Escalation |
|--------|-----------|--------------|------------|
| ClaimEdge (claims work) | Perplexity (research) | Kimi (skills) | Human review for carrier-facing docs |
| Wrestling | Perplexity (schedules) | Comet (web lookups) | Kimi for complex tracking logic |
| Buddy Boy Sports | Perplexity (research) | Kimi (organization) | Comet for registration sites |
| Credit Repair | Perplexity (legal research) | Kimi (letter writing) | Human for dispute submissions |
| Personal AI Ops | Kimi (architecture) | Comet (connector mgmt) | Perplexity for best practices research |

## By Task Type

| Task Type | AI | Why |
|-----------|-----|-----|
| Write a skill | Kimi | Code generation is Kimi's strength |
| Research case law | Perplexity | Deep research with sources |
| Log into a website | Comet | Browser automation |
| Analyze skill gaps | Perplexity | Connector-powered database queries |
| Build automation script | Kimi | Code writing and architecture |
| Take a screenshot | Comet | Visual capture |
| Audit skill inventory | Perplexity | Read from Notion/GitHub |
| Design system architecture | Kimi | Planning and design |
| Scrape competitor data | Comet + Perplexity | Comet extracts, Perplexity analyzes |
| Write demand letter | Kimi | Document generation with templates |
| Check building codes | Perplexity | Legal/code research |
| Schedule inspection | Comet | Web form automation |

## PERPLEXITY PHASE 2+ SUB-TASK

When Perplexity's connectors are active, Kimi should delegate the following audit work to Perplexity using Prompt 1:

**Trigger:** Connectors are green and Robert is ready for ecosystem audit
**Delegation method:**
1. Kimi confirms connector status with Comet
2. Kimi instructs Robert to paste Prompt 1 into Perplexity
3. Perplexity executes Tasks A-H autonomously
4. Perplexity returns: skill audit, consolidation recommendations, QA rubric, risk matrix, new skill briefs, migration tracker
5. Kimi reviews Perplexity's output for quality and consistency
6. Kimi incorporates findings into the master migration plan

**Kimi's review checklist for Perplexity output:**
- [ ] All 67 skills mapped to one of 12 pillars
- [ ] No orphan skills without pillar mapping
- [ ] Naming convention applied consistently
- [ ] Security rules not violated (no PII in output)
- [ ] Risk matrix includes all skills
- [ ] QA rubric has sample evaluations
- [ ] Migration tracker schema is complete

## CLAIMEDGE GOLDEN PATH: AI HANDLING PER CLAIMS STAGE

### Stage 1: INTAKE
**Trigger:** New claim notification
**AI:** Perplexity (research) → Kimi (skill execution)
**Actions:**
- Perplexity: Research property, carrier, policy type
- Kimi: Run claim-intake-triage skill, create claim file
**Human gate:** NONE — intake is automated

### Stage 2: POLICY REVIEW
**Trigger:** Claim file created
**AI:** Perplexity (connector query)
**Actions:**
- Perplexity: Query Notion for similar claims, coverage patterns
- Kimi: Run policy-coverage-review skill
**Human gate:** HIGH — policy interpretation needs spot-check

### Stage 3: INSPECTION
**Trigger:** Coverage confirmed
**AI:** Comet (scheduling) → Kimi (preparation)
**Actions:**
- Comet: Schedule inspection via carrier portal or website
- Kimi: Generate inspection checklist, prepare document package
**Human gate:** MEDIUM — confirm inspection date/time

### Stage 4: DAMAGE ASSESSMENT
**Trigger:** Inspection complete, photos uploaded
**AI:** Kimi (analysis) → Perplexity (research)
**Actions:**
- Kimi: Run exterior-damage-assessment skill, analyze photos
- Perplexity: Research code requirements for identified damage
**Human gate:** HIGH — damage valuation spot-check

### Stage 5: ESTIMATE & SUPPLEMENT
**Trigger:** Damage assessment complete
**AI:** Kimi (document generation)
**Actions:**
- Kimi: Run estimate-supplement-support skill
- Kimi: Generate Xactimate line items, write supplement letter
**Human gate:** CRITICAL — all supplements need human approval before submission

### Stage 6: CARRIER COMMUNICATION
**Trigger:** Supplement ready
**AI:** Kimi (draft) → Human (approval) → Comet (submission)
**Actions:**
- Kimi: Draft carrier communication package
- Human: Review and approve
- Comet: Submit via carrier portal or email
**Human gate:** CRITICAL — carrier-facing docs ALWAYS need approval

### Stage 7: DOCUMENT ASSEMBLY
**Trigger:** Supplement approved
**AI:** Kimi (assembly)
**Actions:**
- Kimi: Run document-assembly skill
- Kimi: Compile final demand package with all supporting docs
**Human gate:** CRITICAL — final package needs approval

### Stage 8: JURISDICTION RESEARCH
**Trigger:** Dispute or complex claim
**AI:** Perplexity (deep research)
**Actions:**
- Perplexity: Research state laws, case law, carrier-specific precedents
- Perplexity: Query Notion for jurisdiction-specific templates
**Human gate:** HIGH — legal research always reviewed

## SAFETY RULES (ALL AIS MUST FOLLOW)

### Rule 1: No Destructive Actions Without Confirmation
**NEVER do any of these without explicit human approval:**
- Delete a skill, document, or database entry
- Send a communication to a carrier or client
- Submit a claim, supplement, or demand letter
- Modify an existing estimate or financial document
- Change connector permissions or access levels
- Delete a repository or Notion page

### Rule 2: Human Review Gates

| Risk Level | Human Review Required | Examples |
|------------|----------------------|----------|
| CRITICAL | ALWAYS before sending/using | Demand letters, supplements, carrier communications |
| HIGH | Spot-check (1 in 3) | Client emails, estimate drafts, inspection reports |
| MEDIUM | Weekly batch review | Internal notes, research summaries, process docs |
| LOW | Monthly audit | Drafts, templates, internal automation logs |

### Rule 3: PII Protection
**NEVER include in any prompt or output:**
- Client full names (use "Insured" or initials)
- Client addresses (use "Property Address")
- Claim numbers (use "Claim #[REDACTED]")
- Policy numbers (use "Policy #[REDACTED]")
- Phone numbers, emails, SSNs

### Rule 4: Data Minimization
Only access data needed for the specific task.

### Rule 5: Audit Trail
Log all actions with timestamp, AI system, action, data accessed, human approval, purpose.

## CURRENT ECOSYSTEM STATE

| Domain | Skill Count | Migration Status |
|--------|------------|-------------------|
| ClaimEdge (insurance) | ~35 | In progress |
| Wrestling (Chase Krapil) | ~16 | In progress |
| Buddy Boy Sports | ~3 | In progress |
| Credit Repair | ~3 | In progress |
| Personal AI Ops | ~12 | In progress |
| **TOTAL** | **67** | **Phase 2 active** |

## OUTPUT FORMAT

Provide everything in structured markdown with clear headers, tables, bullet points, code blocks, bold text, and separators.

## NEXT STEPS FOR ROBERT

After you process this prompt, provide:
1. A numbered list of the next 5 actions Robert should take
2. Which AI handles each action
3. Approximate time for each action
4. Expected outcome for each action

---

# QUICK REFERENCE: NAMING CONVENTIONS

```
claimedge__<pillar>__<function>__<variant>
```

| Segment | Rules | Examples |
|---------|-------|----------|
| `claimedge` | Always starts with domain | claimedge, wrestling, buddyboy, credit, aios |
| `<pillar>` | 2-4 letter pillar code | CIT, PCR, ESS, CCOMM, AIOS |
| `<function>` | Descriptive, 1-3 words | intake-form, supplement-letter, skill-qa-checker |
| `<variant>` | Version, carrier, or use | v2, carrier-a, standard, auto |

## Pillar Code Reference

| Code | Full Name | Skill Count (est.) |
|------|-----------|-------------------|
| CIT | claim-intake-triage | ~4 |
| PCR | policy-coverage-review | ~3 |
| IFE | inspections-field-evidence | ~4 |
| EDA | exterior-damage-assessment | ~5 |
| CC | code-compliance | ~3 |
| ESS | estimate-supplement-support | ~6 |
| CCOMM | carrier-communications | ~4 |
| DA | document-assembly | ~3 |
| JRL | jurisdiction-research-library | ~2 |
| AIOS | ai-os-infrastructure | ~8 |
| SV | sports-ventures | ~22 |
| PRD | productization-rd | ~3 |

---

# QUICK REFERENCE: SECURITY RULES

| # | Principle | Applies To | Check |
|---|-----------|-----------|-------|
| 1 | **READ-ONLY** | All AI systems | No write/delete/modify without approval |
| 2 | **NO SECRETS** | All prompts | No API keys, tokens, passwords in prompts |
| 3 | **OAUTH ONLY** | All connectors | OAuth flows, never credential strings |
| 4 | **PII PROTECTION** | All outputs | No client names, addresses, claim numbers |
| 5 | **DATA MINIMIZATION** | All queries | Only access data needed for task |
| 6 | **AUDIT TRAIL** | All actions | Log what was accessed, when, why |

## Risk Levels & Review Gates

| Level | Trigger | Review Frequency | Examples |
|-------|---------|-----------------|----------|
| CRITICAL | >$10K impact, legal, carrier-facing | Every single output | Demand letters, supplements, dispute docs |
| HIGH | $1K-$10K, client-facing | 1 in 3 spot-check | Client emails, estimate drafts |
| MEDIUM | Internal processes | Weekly batch | Research notes, inspection reports |
| LOW | Drafts, internal | Monthly audit | Templates, automation logs |

---

# QUICK REFERENCE: COMET BROWSER SHORTCUTS & SETTINGS

## ClaimEdge Custom Shortcuts — CREATE THESE

| Trigger | What It Does |
|---------|-------------|
| `/sum` | Summarize this page in 3 bullets with key takeaways |
| `/inv` | Inventory all files in this Google Drive folder — list filename, type, last modified, size in table |
| `/sec` | Scan this page for exposed credentials, API keys, passwords, or sensitive data |
| `/cat` | Categorize all items on this page by domain: ClaimEdge, Wrestling, Buddy Boy Sports, Credit Repair, or Personal AI Ops |
| `/report` | Generate a structured report from all data collected in this session |
| `/inspect` | Generate inspection notes template for [damage type] with code compliance checklist and photo documentation guide |
| `/supplement` | Create a supplement letter outline for [carrier] covering [damage items] with line item justification and code references |
| `/carrier` | Research [carrier name] claims handling procedures, supplement policies, and negotiation tactics |
| `/code` | Look up [state] building code requirements for [trade/material] including ordinance & law references |

## Power User Techniques

1. **Break complex tasks**: Don't say "Buy me a laptop under $1000 with good reviews" — say "Step 1: Search Amazon for laptops under $1000" → "Step 2: Filter by 4+ stars" → "Step 3: Compare top 3 in a table"
2. **Use Chrome for quick lookups**: Comet has AI latency. For "what's the weather" — use Chrome. For research, analysis, automation — use Comet.
3. **Start with one connector**: Don't connect Gmail + Calendar + Drive + Notion all at once. Start with one. Test it. Add another.
4. **Verify critical actions**: Comet is beta. Always verify financial transactions, legal citations, sent emails, deleted files.

## Recommended Settings

| Setting | Recommendation | Why |
|---------|---------------|-----|
| Default search | Perplexity | Better for research tasks |
| AI model | GPT-5 (complex), Claude (writing) | Match model to task |
| Privacy → Ad blocking | ON | Cleaner pages |
| Privacy → Tracker prevention | ON | Better privacy |
| Sidebar position | Right | Keeps content visible |
| Data sharing | OFF | Privacy protection |

## Known Limitations

| Issue | Workaround |
|-------|-----------|
| Only imports ONE Chrome profile | Manually set up additional profiles |
| Constant "make default browser" prompts | Ignore or dismiss |
| Shopping automation often fails | Break into smaller steps |

---

*Continue to PART 4 for Kimi prompt, skill counts, and final checklist.*

<!-- END PART 3 -->
