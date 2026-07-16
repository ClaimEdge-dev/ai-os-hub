# ClaimEdge Artifact Classification & Routing

## Summary
- **116 total artifacts** cataloged across 3 sources
- **60 Notion pages**, **39 GitHub files**, **30+ local files**
- **103 Active**, **8 Archive**, **2 Migrate**, **3 Review**

---

## NOTION PAGES — Classification

### Hub & Registry (Keep, Update)
| ID | Title | Class | Domain | Status | Action |
|----|-------|-------|--------|--------|--------|
| N1 | AI OS Hub | Hub/Registry | Cross-Cutting | Active | Update to 12-pillar, remove Huuso refs |
| N2 | Skill Registry DB | Hub/Registry | Cross-Cutting | Active | Add GitHub links, update statuses |
| N3 | ClaimEdge Command Center | Hub/Registry | ClaimEdge-Claims | Active | Keep, ensure synced |
| N4 | ClaimEdge University | Hub/Registry | ClaimEdge-Claims | Active | Keep |

### Operational Pages (Keep)
| ID | Title | Class | Domain | Status | Action |
|----|-------|-------|--------|--------|--------|
| N5 | Workflows & SOPs | SOP | ClaimEdge-Claims | Active | Keep |
| N6 | Content Library | Marketing/Product | ClaimEdge-Claims | Active | Keep |
| N7 | Templates Library | Template | ClaimEdge-Claims | Active | Keep |
| N8 | Master System Prompt v3 | Prompt | Cross-Cutting | Active | Keep, update v# |
| N9 | Email Automation Sequences | Template | ClaimEdge-Claims | Active | Keep |
| N10 | Coffey Claim #061609752 | Claim Ops | ClaimEdge-Claims | Active | Keep (active claim) |
| N11 | ClaimEdge Presets | Workflow | ClaimEdge-Claims | Active | Keep |
| N12 | Kimi Scheduled Task Presets | Workflow | Cross-Cutting | Active | Keep |
| N13 | ClaimEdge Kimi Claw Presets | Workflow | ClaimEdge-Claims | Active | Keep |
| N14 | Kimi Feature Guide | SOP | Cross-Cutting | Active | Keep |
| N15 | BBS Research Hub | Hub/Registry | Buddy-Boy-Sports | Active | Keep |
| N16 | Wrestling Skills Inventory (11 Skills) | Hub/Registry | Wrestling | Active | Renamed from Skills Inventory |

### ClaimEdge Skills (Keep All, Group by Pillar)
| ID | Title | Pillar | Status |
|----|-------|--------|--------|
| S1 | claimedge-complete-system | Claims-Ops | Active |
| S2 | claimedge-full-claims-investigation | Claims-Ops | Active |
| S3 | claimedge-auto-deploy | AI-Infrastructure | Active |
| S4 | claimedge-training-builder | Claims-Ops | Active |
| S5 | claimedge-session-memory | AI-Infrastructure | Active |
| S6 | claimedge-vault-system | AI-Infrastructure | Active |
| S7 | claimedge-skill-forge | AI-Infrastructure | Active |
| S8 | claimedge-master-coach | AI-Infrastructure | Active |
| S9 | claimedge-material-hazards | Claims-Ops | Active |
| S10 | claimedge-roof-valley-claims | Claims-Ops | Active |
| S11 | claimedge-weather-researcher | Claims-Ops | Active |
| S12 | claimedge-claims-master | Claims-Ops | **Renamed from huuso-claimedge-master** |
| S13 | claimedge-supplement-writer | Claims-Ops | **Renamed from huuso-supplement-writer** |
| S14 | wind-hail-property-claims | Claims-Ops | Active |
| S15 | claimed-master-workflow | Claims-Ops | Active |
| S16 | premier-claims-investigation | Claims-Ops | Active |

### Cross-Cutting AI Skills (Keep, Group)
| ID | Title | Status |
|----|-------|--------|
| A1 | robert-master-os | Active |
| A2 | ai-workflow-decoder | Active |
| A3 | multi-ai-router | Active |
| A4 | bobby-focus-system | Active |
| A5 | bobbys-ai-translator | Active |
| A6 | bobby-skill-activator | Active |
| A7 | kimi-usage-optimizer | Active |
| A8 | session-context-preserver | Active |
| A9 | skill-lifecycle-manager | Active |

### Wrestling Skills (Keep, Archive to Wrestling Hub)
| ID | Title | Status |
|----|-------|--------|
| W1-W5 | All wrestling skills | Active -> Archive from main, keep in wrestling hub |

### Sports / Buddy Boy (Keep)
| ID | Title | Status |
|----|-------|--------|
| B1-B2 | content-repurposer, sports-tournament-scout | Active |

### Other (Review)
| ID | Title | Status |
|----|-------|--------|
| O1 | credit-repair-orchestrator | Review -- not core ClaimEdge |

### Security Audit Pages (Keep, Organize)
| ID | Title | Severity |
|----|-------|----------|
| SEC1-11 | All 11 security findings | Keep in Security section |

---

## GITHUB FILES -- Status

### Full Content (31 files) -- Keep
All key deliverables verified with full content.

### Placeholder Files (8) -- Cleanup
| Path | Action |
|------|--------|
| docs/migration-jul-2026/UNNECESSARY_ITEMS_AUDIT.md | Delete (21B placeholder) |
| prompts/REVISED_PROMPTS_PACKAGE_v2.md | Delete (15B artifact) |
| docs/REVISED_CLAIMEDGE_MIGRATION_PACK.md | Delete (97B, superseded by v2 in migration/) |
| Other root-level legacy files | Archive |

### Critical Fix
| Path | Action |
|------|--------|
| docs/security-check.yml | Move to .github/workflows/security-check.yml |
| .github/workflows/ | Create directory (blocked by MCP, needs Comet) |

---

## LOCAL FILES -- Routing

### .skill Packages (Keep in GitHub)
| File | Action |
|------|--------|
| robert-master-os/ | Push SKILL.md + references to GitHub |
| skill-lifecycle-manager/ | Push to GitHub |
| perplexity-connector-advisor/ | Push to GitHub |
| claimedge__intake__/ | Already in GitHub |

### V2 Documents (GitHub is canonical)
| File | Action |
|------|--------|
| REVISED_CLAIMEDGE_MIGRATION_PACK_v2.md | Already in GitHub |
| REVISED_PROMPTS_PACKAGE_v2.md | Already in GitHub |
| UBIQUITOUS_LANGUAGE.md | Already in GitHub |

### Handoff Docs (GitHub is canonical)
| File | Action |
|------|--------|
| PERPLEXITY_MASTER_HANDOFF_COMPLETE.md | Already in GitHub |

### V1/Legacy Documents (Archive)
| File | Action |
|------|--------|
| CLAIMEDGE_MIGRATION_PACK.md | Archive (superseded by v2) |
| PROMPTS_PACKAGE.md | Archive (superseded by v2) |
| GAP_ANALYSIS_COMPLETE.md | Archive |
| MASTER_HANDOFF_COMPLETE.md | Archive |
| Various v1 files | Archive |

---

## TOP 10 PRIORITY ACTIONS

| Prio | Action | Platform | Effort |
|------|--------|----------|--------|
| P0 | Move security-check.yml to .github/workflows/ | GitHub | 15 min |
| P0 | Update AI OS Hub to 12-pillar ClaimEdge-only | Notion | 45 min |
| P0 | Add GitHub links to Skill Registry DB | Notion | 30 min |
| P0 | Clean up 8 GitHub placeholder files | GitHub | 15 min |
| P1 | Organize security audit pages under Security section | Notion | 15 min |
| P1 | Push remaining .skill packages to GitHub | GitHub | 30 min |
| P1 | Archive v1 documents (keep v2 as canonical) | Local | 15 min |
| P2 | Create .github/workflows/ directory | GitHub | Needs Comet |
