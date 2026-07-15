# COMET MASTER PROMPT — Hands-Free AI OS Audit

> Send this to Comet (Perplexity's browser agent) as a new thread. Attach `COMET_QUICK_REFERENCE.md`.

---

## YOUR MISSION

Perform a complete hands-free audit and organization of my AI Operating System. Do not stop until every phase is complete. Research the most efficient Comet browser techniques as you go. Verify everything. Suggest improvements.

---

## PHASE 0 — SECURITY AUDIT (First Priority)

Before touching anything, scan for exposed credentials:

1. **Google Drive** — Search shared folders for API keys, tokens, passwords in plain text
2. **Notion** — Check any shared Notion pages for embedded credentials
3. **GitHub repos** — Scan all public repos for `.env`, `config.json`, or hardcoded secrets
4. **Gmail** — Search for emails containing passwords or API keys

**For each finding:**
- Document the exact location
- Rate severity (Critical / High / Medium / Low)
- Provide remediation steps

---

## PHASE 1 — GLOBAL DISCOVERY (Inventory Everything)

### 1A — Google Drive Inventory
Navigate through all folders. For each folder, record:
- Folder name and path
- Number of files
- File types
- Last modified date
- Whether contents are readable

Build a complete folder tree.

### 1B — Notion Inventory
Navigate through all Notion pages. For each page/database:
- Page name
- Type (page / database / calendar / board)
- Child pages/databases
- Last edited date
- Content summary (brief)

### 1C — GitHub Inventory
List all repos under `ClaimEdge-dev`. For each:
- Repo name
- Description
- Public/Private
- Last updated
- Primary language
- Key files

### 1D — Gmail Inventory (if accessible)
Search for emails related to: AI, skills, automation, Perplexity, Kimi, Comet, Claude, Manus, wrestling, claims, Huuso, Buddy Boy Sports

---

## PHASE 1E — COMET OPTIMIZATION (Research While Working)

While running the above phases, simultaneously research:

1. **Custom shortcuts** — Can Comet create keyboard shortcuts? Set up 5:
   - `Ctrl+Shift+1` = Screenshot current page
   - `Ctrl+Shift+2` = Copy page content to clipboard
   - `Ctrl+Shift+3` = Save to designated Drive folder
   - `Ctrl+Shift+4` = Toggle browser tools panel
   - `Ctrl+Shift+5` = Quick search my Notion

2. **Browser settings** — Research optimal Chromium settings for Comet:
   - Disable unnecessary extensions
   - Enable hardware acceleration
   - Set default download location to Drive/Comet-Downloads/
   - Configure print-to-PDF settings

3. **Widget configuration** — What widgets are available? Configure:
   - Quick access to Notion
   - Quick access to GitHub
   - Current task tracker
   - Time tracker

4. **Power user techniques** from forums/reddit:
   - Search Reddit r/perplexity_ai for Comet tips
   - Search for "Comet browser automation tips"
   - Find any undocumented features

---

## PHASE 2 — RECOMMENDED ACTIONS

Based on Phase 1 findings, recommend:

### 2A — Folder Structure Optimization
Suggest a reorganized folder structure with these top-level folders:
- `01-ClaimEdge-Claims/` — All claims-related files
- `02-Huuso-Exteriors/` — Inspection reports, photos, estimates
- `03-Wrestling-ICDWA/` — Tournament data, opponent scouting
- `04-Buddy-Boy-Sports/` — Team management, tournaments
- `05-AI-Engineering/` — Skills, prompts, automation scripts
- `06-Research/` — Market research, product development
- `07-Personal/` — Personal documents
- `08-Archive/` — Completed/deprecated items

### 2B — Notion Structure Optimization
Suggest improvements to Notion organization:
- Consolidate scattered pages
- Create consistent database templates
- Set up relations between databases
- Add status tracking

### 2C — GitHub Repo Consolidation
- Identify repos that could be merged
- Suggest naming conventions
- Flag repos missing README files
- Recommend which should be public vs private

---

## EXECUTION RULES

1. **Do NOT ask for permission** — execute each phase autonomously
2. **Document everything** — create a running log of actions taken
3. **Screenshot key findings** — save to Drive/Comet-Audit-2026-07-16/
4. **If blocked** — skip and note the blocker, continue with next item
5. **If unsure** — make a reasonable assumption and note it
6. **Verify** — double-check every inventory count
7. **Suggest** — at every step, suggest better ways to do things
8. **Flag risks** — immediately flag anything that looks like a security risk
9. **Track time** — note how long each phase takes
10. **Final report** — produce a structured summary with all findings

---

## OUTPUT FORMAT

Produce a final report with these sections:

```
## Security Audit Results
[Critical/High/Medium/Low findings with locations]

## Complete Inventory
### Google Drive
[Folder tree with counts]
### Notion
[Page tree with counts]
### GitHub
[Repo list with details]

## Comet Optimization Applied
[What was configured]

## Recommended Actions
### Immediate (This Week)
[Top 5]
### Short Term (Next 2 Weeks)
[Top 5]
### Long Term (Next Month)
[Top 5]

## Time Tracking
[Phase | Duration | Notes]

## Issues / Blockers
[What couldn't be accessed and why]

## Suggestions for Improvement
[Think outside the box — what am I missing?]
```

---

## CONSTRAINTS
- Never delete anything without explicit confirmation
- Never move files that might break existing links
- Never expose credentials in the final report
- Always prioritize security over convenience
- If a page/file is too large to inventory, note the size and skip
- Respect rate limits — add delays between rapid actions

---

## POST-COMPLETION TASK

After the audit is complete, run the Meta Feedback Protocol:

```
Run this self-assessment:
1. What worked well in this session?
2. What was inefficient?
3. What features did I (Comet) use most?
4. What features did I not use that I should have?
5. How can Robert get 2x more value from Comet next time?
6. What other AI tools should Robert be using with Comet?
7. Suggest 3 specific workflow improvements
8. Rate overall session efficiency 1-10 with justification
```

Report all findings back to the chat when complete.
