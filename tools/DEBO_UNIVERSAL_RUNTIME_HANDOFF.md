# DEBO v3.2 — Universal verification handoff
Scope: ClaimEdge, JCT, PLG, RRR, Bulldogs, WrestlingOS, Chase Athletics, Buddy Boy Sports, CreditRepairOS, SettleSure, Morgan's, Rental OS and future sister brains.

1. Retrieve the shared gate from `tools/debo_durable_save_gate.py`.
2. Save artifacts to approved durable storage, then independently download each to a different path.
3. Run `python tools/debo_verify_all.py manifest.json --receipt receipt.json`.
4. Mark DONE only if all checks return exit 0, full SHA-256 matches, destination ID is known and approvals are satisfied. Otherwise mark BLOCKED/PARTIAL.
5. Keep private receipts in approved private storage. Never put sensitive data in this public repository.

Example:
```json
{"artifacts":[{"id":"example","original":"/path/original.zip","readback":"/path/independent-download.zip","destination":"approved-private-location","expected_sha256":"64-character-sha256"}]}
```

This is a shared source and a tested workflow, NOT evidence of a persistent Kimi hook or installation in any sister brain. Kimi reported 3/3 tests; complete original logs remain unavailable in this session. See [DEC-016](../records/DEC-016_DURABLE_SAVE_GATE_RUNTIME_RECEIPT_2026-10-10.md).
