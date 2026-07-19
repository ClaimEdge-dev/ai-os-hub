# Governance Constitution (Full Detail)

Read this for extended-phase work (Phases 6–17), governance disputes, or when SKILL.md rules need their full context.

## Contents
- Business & Sports Context Rules
- Model / Mode Selection
- WebBridge / Browser Safety
- Self-Correction Loops
- Version Control Governance
- Extended Phases 6–17

## Business & Sports Context Rules

- Business-side organization is **ClaimEdge-only**. All reports, skills, templates, and communications use ClaimEdge branding exclusively.
- The legacy exteriors brand (retired 2026-07-19) is not an active business operating domain — archive only. Do not reference it except for explicitly preserved historical context.
- **Kevin and Tim** are excluded from active business context unless the user explicitly reintroduces them.
- **Wrestling is the core sports build.** Consolidate all sports-related artifacts into one integrated wrestling master build. Exclude football. Buddy Boy Sports baseball is a separate BBS domain, not part of the wrestling build.

## Model / Mode Selection

| Work type | Route |
|---|---|
| Architecture, classification, audits, governance, memory, versioning, long-context analysis | Kimi Thinking mode |
| Code generation, schema generation, HTML app implementation, automation specs, database builders | Kimi Code mode |
| Direct, necessary, safe browser actions | Agent mode + browser tools only |
| Auditable parallel decomposition | Swarm, only with clear sub-tasks |
| Post-hoc synthesis/editing | Claude |
| Final factual/link verification | Perplexity |

## WebBridge / Browser Safety

1. Confirm browser bridge is active before acting.
2. Identify the exact browser/tab.
3. Describe the intended action before executing.
4. Confirm reversibility.
5. Log success/failure.
6. Stop and ask if the UI is ambiguous.
7. Require explicit approval for destructive actions unless the item is in a pre-approved safe bucket.

## Self-Correction Loops

- `max_attempts` default = 3. Never loop indefinitely.
- Validation order: deterministic checks > evidence checks > domain checklist > critic review > human review.
- Log `attempt_number`, `failure_reason`, `critique_history`, `validation_method` for every retry.
- At the attempt limit, escalate with the best partial result and a precise next-action path.

## Version Control Governance

- Branch before major changes: `feature/`, `fix/`, `audit/`, `refactor/`.
- Test before merge; review before deploy.
- Preserve rollback paths and release notes.
- One canonical mainline — no competing "master" prompts. This constitution is the single source of governance truth; older master prompts get archived, not duplicated.

## Extended Phases 6–17

**6. Connector / Plugin / Skill Audit** — inventory every connector, plugin, and skill; rate usefulness, overlap, risk, gaps. Overlapping skills: recommend merge/retire, never silently delete. Output: registry table with A/B/C/D tags.

**7. Skill Architecture** — design reusable skills, templates, SOPs, schemas for ongoing hands-free operations. New skills follow the skill-creator standard (lean SKILL.md, progressive-disclosure references). Check both skill directories for name clashes before creating.

**8. Wrestling Master Build Consolidation** — merge all wrestling artifacts (brackets, opponent intel, rankings, Chase Krapil profile, ICDWA, Level Up app, tournament prep) into one master structure. Preserve verified data with source URLs; mark UNVERIFIED / NOT FOUND honestly.

**9. Wrestling HTML App Roadmap** — single-file HTML/PWA roadmap: features, data model, offline behavior, version milestones.

**10. ClaimEdge Operating System Roadmap** — intake → inspection → supplement → negotiation → settlement pipeline; CRM schema; template library; training/SOP layer.

**11. Auto-Generated Fields / Status Pills / Stage Logic** — define status taxonomies and stage transitions for Notion databases (claims, wrestling, threads). Every status pill needs: name, color, entry criteria, exit criteria.

**12. Long-Term Memory & Context Engineering** — maintain the 10 memory objects (see `naming-and-memory.md`). Keep 30–50% token headroom. Retrieval priority: current instruction > PROJECT_CHARTER > DOMAIN_MEMORY > TASK_STATE > DECISION_LOG/CHANGE_LOG > current evidence > older chats only if needed.

**13. Autonomous Self-Correction Loops** — implement the loop rules above as standing behavior; produce checkpoint summaries at every phase boundary.

**14. Version Control / Branching / Merge Governance** — apply the rules above to GitHub repos and any versioned artifact.

**15. Security / Access / Governance Review** — never ask for or store passwords/secrets in skills, prompts, or repos. Flag any credential found in plaintext as a P0 risk. Review connector scopes: recommend least-privilege.

**16. Execution Roadmap** — sequenced, dated action plan: this week / this month / this quarter. Every item has owner (user vs. agent), effort estimate, and dependency list.

**17. Action Log & Output Format** — see `action-log.md`.
