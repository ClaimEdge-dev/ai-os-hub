---
name: rc-case-inventory
description: Safely index Illinois court cases from authorized source records, flag identity gaps and duplicate candidates. Use when recovering docket screenshots, cases or dispositions.
---
# Illinois Case Inventory
Reuse `skills/skill-lifecycle-manager` and existing `AGENT_SYSTEM.md`. One case per record, one charge per charge record. Verify identity beyond name-only results. Prefer official court records to screenshots; unknowns remain null. Store source URL/ID and retrieval date. Detect possible duplicates, but never merge disputed identities automatically. Never bypass court portals or scrape behind access controls. No client records in a public repo. No eligibility conclusions or filings.