# Action Log, Session Templates & Output Format

Read during Phase 5 execution and at every session start/end.

## Contents
- Action Log Format
- Session Start Template
- Session End Template
- Final Output Format

## Action Log Format

One row per action, appended to CHANGE_LOG (Notion canonical; markdown fallback):

```
| timestamp | phase | action_type | target | old_value | new_value | verification | reversible | result |
```

- `action_type`: RENAME / ARCHIVE / MOVE / CREATE / CONNECTOR_CHANGE / DELETE(approved-only)
- `verification`: A / B / C / D per the constitution standard
- `reversible`: YES + rollback path, or NO + why it was approved
- `result`: SUCCESS / FAILED(reason) / SKIPPED(reason)
- Failed actions get a self-correction entry: `attempt_number`, `failure_reason`, `critique_history`, `validation_method`.

## Session Start Template

```
SESSION START — [date]
Active goal:
Domain(s): CE / WR / BBS / OS / REF / ARC
Canonical memory sources loaded: PROJECT_CHARTER, TASK_STATE, ...
Branch/version:
Blockers (with D-tag fallbacks):
Approved actions this session:
Prohibited actions:
Next best step:
```

## Session End Template

```
SESSION END — [date]
Completed (with verification tags):
Memory objects updated: TASK_STATE / DECISION_LOG / CHANGE_LOG / ...
Version changes:
Open items (owner: user / agent):
Approvals needed next session:
Next session's first step:
```

## Final Output Format

Every governance run ends with these sections, in this order:

1. **Verification Summary** — counts of A/B/C/D findings; every D has a fallback stated.
2. **Inventory & Classification Table** — item → domain → action bucket (Safe Rename / Safe Archive / Trash Pending Review / Needs Manual Review).
3. **Dry-Run Action Plan** — exact proposed actions with reversibility; nothing executed yet unless pre-approved.
4. **Connector Registry Delta** — what changed in plugin status since last audit.
5. **Memory Updates Made** — which of the 10 objects changed and why.
6. **Action Log Rows** — the CHANGE_LOG entries from this run.
7. **Next Steps** — sequenced, with owner (user/agent) and the single next best step first.

Formatting: short sections, tables over prose, no walls of text. The user processes best with visual progress markers (✅ done / 🔄 in progress / ⏸ blocked) on multi-phase runs.
