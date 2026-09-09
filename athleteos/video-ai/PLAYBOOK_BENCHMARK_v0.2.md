# AthleteOS — Bulldogs Video AI Playbook Benchmark v0.2

Source of truth: `TPBD LW Playbook 2026`.

## Mandatory call order
Formation → Motion → Fake → Play

## Controlled vocabulary
- 28 formations (playbook pages 6–20)
- 4 motions: 3 MO, 4 MO, 3 ARC, 4 ARC (page 21)
- 43 named plays across Run, Pass, Counter, and Trick sections (pages 22–45)

## AI rules
1. Use only Bulldogs labels supported by the playbook or explicit coach-approved corrections.
2. Never invent formations, motions, fakes, plays, assignments, routes, reads, blocking rules, cadence, audibles, or wristband calls.
3. Every film classification must include candidate label, source page, confidence, Team Truth status, and evidence.
4. If evidence is insufficient, return UNKNOWN / NOT_VISIBLE.
5. If the playbook does not state a written assignment, return NOT_SPECIFIED_IN_PLAYBOOK.
6. Page 38 Flood exact fake numbers are BLOCKED pending coach review because the title and QB assignment text conflict.
7. Preserve source spelling. Goaline/Goalline normalization may be metadata only until approved.
8. COACH_VERIFIED may only be assigned after explicit coach confirmation.
9. QB grading is allowed only when the relevant assignment is explicitly supported by the playbook or coach correction.

## Confidence gates
- >= 0.90: strong AI candidate; still not coach-verified
- 0.70–0.89: candidate requiring review
- < 0.70: unknown/review required
- Any source conflict: blocked regardless of confidence

## Known review locks
- Page 38 `DW X-Wide Fake 24 Flood R`: title says Fake 24; QB text says Fake 23.
- Page 38 `DW Y-Wide Fake 23 Flood L`: title says Fake 23; QB text says Fake 24.
- Source uses Goaline/Goalline variants.
- Page 45 `ACE tight Hook & Ladder` has no written player assignment text; do not grade written assignments from it.

## Cross-plugin mapping
- Google Drive / Sheets: canonical Week 3 film vault + play ledger
- Airtable: structured Playbook Truth + Coach Review registry
- Figma: Film Intelligence UI + Team Truth benchmark panel
- GitHub AI OS Hub: schemas, prompts, cross-AI handoff and source control
- Descript: downstream teaching clips and coach/player cutups, not Team Truth classification
- VEED: downstream narrated/creative video production, not Team Truth classification

Status: active benchmark, coach-review gated where noted.
