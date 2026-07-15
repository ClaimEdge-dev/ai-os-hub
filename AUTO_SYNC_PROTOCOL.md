# AUTO-SYNC PROTOCOL — Keep Notion + GitHub Updated Automatically

**Version:** 1.0  
**Date:** 2026-07-16  
**Applies to:** Kimi, Perplexity, Comet, Claude, Manus — ALL threads

---

## THE PROBLEM

Robert said: *"You need to always update these plugins as we go automatically no matter what threads we are in."*

**Solution:** Every AI checks Notion + GitHub first before doing anything. Every AI saves back to Notion + GitHub when done. No exceptions.

---

## PROTOCOL RULES (All AIs Must Follow)

### Rule 1: CHECK BEFORE BUILDING
**Before starting ANY new work, check these sources:**

1. **GitHub `ClaimEdge-dev/ai-os-hub`** — Is there already a skill for this?
2. **Notion "AI OS Hub" page** — What's the latest status?
3. **Skill directory** — Is there a built-in or user skill already?

**If a skill exists → Use it. Don't rebuild.**  
**If a skill is outdated → Update it. Don't create new.**  
**If no skill exists → Build it, then save to Notion + GitHub.**

### Rule 2: SAVE AFTER BUILDING
**After completing ANY work, save to these locations:**

1. **GitHub** — Push .skill files to `ClaimEdge-dev/ai-os-hub`
2. **Notion** — Update the "AI OS Hub" page with changes
3. **Local backup** — Keep copy in `/mnt/agents/output/` as fallback

**If you can't save to one location, save to the others and note the failure.**

### Rule 3: VERSION EVERYTHING
**Every save must include:**

- Version number (increment: v1.0 → v1.1 → v2.0)
- Date (YYYY-MM-DD format)
- Change summary (1-2 sentences)
- Status tag: `[ACTIVE]`, `[DEPRECATED]`, `[DRAFT]`, `[ARCHIVED]`

### Rule 4: NOTIFY ON CONFLICT
**If you detect a conflict:**

- STOP and report it
- Don't guess — ask Robert which version is correct
- Use the Skill Conflict Resolver (5-tier priority system)
- Log the conflict in Notion "AI OS Hub > Conflict Log"

### Rule 5: PERPLEXITY READS, KIMI BUILDS
**Role separation:**

| AI | Primary Role | Writes To | Reads From |
|---|---|---|---|
| **Kimi** | Build skills, write code, deploy | GitHub, Notion, local | GitHub, Notion, skills |
| **Perplexity** | Research, verify, connectors | Notion (notes only) | Notion, GitHub, web |
| **Comet** | Browse, audit, inventory | Notion (reports only) | Notion, GitHub, Drive |
| **Claude** | Analyze, strategy, writing | Notion (docs only) | Notion, GitHub |
| **Manus** | Execute tasks, automation | GitHub (code only) | GitHub, Notion |

### Rule 6: EVERY THREAD STARTS WITH SYNC
**Every new thread must:**

1. Check `ClaimEdge-dev/ai-os-hub/AUTO_SYNC_PROTOCOL.md` for latest rules
2. Check Notion "AI OS Hub" for recent changes
3. Report what's new since last session
4. Only THEN start the requested work

### Rule 7: PERPLEXITY CONNECTOR PRIORITY
**When Perplexity needs info, check in this order:**

1. Notion (via Notion connector) — fastest, always current
2. GitHub (via GitHub connector) — .skill files and docs
3. Google Drive (via Drive connector) — shared files, templates
4. Web search (via Web connector) — external verification
5. File upload (last resort) — only when connectors can't access

### Rule 8: SECURITY FIRST
**Never sync sensitive data:**

- NO API keys, passwords, tokens in any synced file
- NO client personal information in public repos
- NO claim details with identifying information
- Use `.env.example` instead of `.env`
- Use `[REDACTED]` for sensitive values in documentation
- Private repos for anything with business logic
- Public repos for documentation and templates only

### Rule 9: FALLBACK CHAIN
**If the primary sync method fails:**

```
Primary:    Notion ←→ GitHub ←→ Kimi
Fallback 1: GitHub ←→ Kimi (skip Notion)
Fallback 2: Local files ←→ Kimi (skip cloud)
Fallback 3: Robert manual update (last resort)
```

### Rule 10: WEEKLY AUDIT
**Every Sunday, run this checklist:**

- [ ] All .skill files pushed to GitHub
- [ ] Notion "AI OS Hub" reflects current state
- [ ] No skills exist only in local storage
- [ ] No duplicate skills across domains
- [ ] All deprecated skills marked [DEPRECATED]
- [ ] GitHub README links are working
- [ ] Notion page links are working
- [ ] No sensitive data in public repos

---

## FILE NAMING CONVENTION

All synced files must follow this pattern:

```
[Domain]__[Function]__[Name]__[YYYY-MM-DD]__[v#]__[Status]

Examples:
  ClaimEdge__Supplement__WindHailScope__2026-07-16__v2__ACTIVE
  Wrestling__Scout__OpponentBrief__2026-07-16__v1__DRAFT
  AI-Meta__Prompt__PerplexityStarter__2026-07-16__v1__ACTIVE
```

---

## NOTION STRUCTURE (AI OS Hub)

```
AI OS Hub (master page)
├── Skill Registry (database)
│   ├── Name
│   ├── Domain
│   ├── Description
│   ├── Trigger
│   ├── GitHub Link
│   ├── Version
│   ├── Status
│   └── Last Updated
├── Recent Changes (changelog)
├── Conflict Log (issues)
├── Cross-AI Protocol (how AIs hand off)
├── Security Audit Log
└── Weekly Status (auto-generated)
```

---

## GITHUB STRUCTURE

```
ClaimEdge-dev/ai-os-hub/
├── README.md                    # This hub
├── AUTO_SYNC_PROTOCOL.md        # This file
├── SKILL_REGISTRY.md            # All 67 skills
├── PERPLEXITY_STARTER_PROMPT.md # Send to Perplexity
├── COMET_MASTER_PROMPT.md       # Send to Comet
├── META_FEEDBACK_PROMPT.md      # Append to all sessions
├── ROBERT_AI_OS_ROADMAP_v1.0.md # Strategic plan
├── MASTER_HANDOFF_COMPLETE.md   # Full skill list
├── PERPLEXITY_HANDOFF_BRIEF.md  # Perplexity brief
├── COMET_QUICK_REFERENCE.md     # Comet shortcuts
├── releases/                    # .skill files
│   ├── robert-master-os.skill
│   ├── skill-lifecycle-manager.skill
│   └── perplexity-connector-advisor.skill
└── archives/                    # Old versions
```

---

## QUICK REFERENCE: WHAT TO SYNC WHEN

| When This Happens | Sync What | To Where |
|---|---|---|
| New skill built | .skill file + docs | GitHub + Notion |
| Skill updated | Updated .skill + changelog | GitHub + Notion |
| New prompt written | .md file | GitHub + Notion |
| Prompt updated | Updated .md | GitHub + Notion |
| New domain added | New section in registry | Notion + GitHub |
| Skill deprecated | Status → [DEPRECATED] | Notion + GitHub |
| Security issue found | Fix + audit log | GitHub (private) + Notion |
| Weekly audit | Full status report | Notion |
| Roadmap updated | Updated roadmap | GitHub + Notion |

---

## PERPLEXITY-SPECIFIC INSTRUCTIONS

When Perplexity reads this protocol:

1. **Enable these connectors:** Notion, GitHub, Google Drive
2. **Read this file first** on every new thread
3. **Check Notion "AI OS Hub"** for latest skill registry
4. **Check GitHub `ai-os-hub`** for .skill files and docs
5. **If info is missing** from Notion/GitHub, search the web
6. **If still missing**, ask Robert — don't guess
7. **Never upload files** if the data is already in Notion/GitHub
8. **Report sync status** at end of every session

---

## KIMI-SPECIFIC INSTRUCTIONS

When Kimi reads this protocol:

1. **Push .skill files to GitHub** immediately after building
2. **Update Notion "AI OS Hub"** with new/changed skills
3. **Check for existing skills** before building new ones
4. **Report sync status** — "Pushed to GitHub: [filename]" or "Failed: [reason]"
5. **Use this protocol file** as the first reference on every session start

---

## EMERGENCY: FULL REBUILD SCENARIO

If everything is lost (Notion corrupted, GitHub down, local files gone):

1. Kimi has all skills in `/app/.user/skills/` (read-only backup)
2. Re-clone `ClaimEdge-dev/ai-os-hub` from GitHub
3. Re-create Notion pages from GitHub markdown
4. Re-install .skill files from GitHub releases
5. Run weekly audit to verify completeness

**Recovery time: 15-30 minutes.**

---

## LAST UPDATED

2026-07-16 — Protocol created and deployed.
