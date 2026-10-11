# DEC-016 — Durable-Save Gate runtime receipt
Date: 2026-10-10
Status: RUNTIME VERIFIED (user-provided Kimi report); INSTALL PENDING
Public-safe evidence summary; do not put private artifact contents in this repository.

## Source
- Repository: ClaimEdge-dev/ai-os-hub
- Utility: tools/debo_durable_save_gate.py (1767 bytes; Git blob 07bf9b955508b8a82b04eaf0861197d4e15cf06e)
- README: tools/DEBO_DURABLE_SAVE_GATE_README.md (1129 bytes; Git blob fb9710d28f992c2efc760d896656a0d143b5b4e3)
- User-supplied Kimi report states Python 3.12.12, GitHub API/codeload retrieval, and matching source checksums. Only abbreviated SHA-256 values were supplied: utility 44255f49…a926649d; README c885eac9…f1b461f5.

## User-supplied runtime evidence
1. Matching ZIPs: exit 0, VERIFIED.
2. Wrong expected SHA-256: exit 1, FAILED_VERIFICATION.
3. Mutated readback: exit 1, matching=false.
Kimi reported "DEBO gate: 3 checks passed." Full stdout/stderr and complete hashes were not provided in this handoff. Do not label the archived log independently verified.

## Boundaries
- This is evidence of a successful one-session execution, not persistent Kimi skill installation.
- No .skill file was installed or changed in the reported session.
- No automatic invocation is established for DEBO sister brains.
- GitHub Actions workflow: .github/workflows/debo-durable-save-gate.yml; commit 7faa20f3077a644db7b2558cff32bbe0fb7bb736. Workflow run success not independently confirmed.
- No user-private records, credentials, or claim evidence may be committed to this public repo.

## Promotion gate
To promote to INSTALLED/ACTIVE: prove a supported persistent runtime hook, run on a fresh real artifact and independent durable readback, retain full SHA-256 and exit code, and verify the saved receipt at its destination. Until then: RUNTIME VERIFIED / INSTALL PENDING.

## Cross-AI handoff
Kimi: archive complete raw execution logs privately (e.g. /mnt/agents/output/ if available), then save durably and read back. DeboGPT26: independently repeat tests and reconcile receipts. Sister brains: reuse one utility; do not duplicate or claim automatic execution without a real hook.


## Independent DeboGPT26 verification — 2026-10-10

Fetched GitHub source and reproduced its exact Python scripts in the execution container. Script SHA-256:
- `tools/debo_durable_save_gate.py`: `44255f491f9b6ea10eedcb5ba0289381c8ccbced3e0cf9d7b5161c26a926649d`
- `tools/debo_verify_all.py`: `49a586ee52d68fd16d8d095d6cfdc7aac89a1d6016ca81f142381a9964fdffa1`

Real artifact: DEBO source-difference ZIP, SHA-256 `2243db349548e2bf44aca83c47be4e5d263552b80c917834c0c1eba95e8be714`. Independently fetched Google Drive copy at file ID `1juEp1lpwMru3u_K_83JZxIRREPhvg7sa` matched the local original byte-for-byte by SHA-256. The exact batch runner invoked the exact gate: `VERIFIED`, exit `0`.

Negative test matrix (batch runner calling exact gate): matching artifact exit 0; wrong expected hash exit 1; mutated readback exit 1; empty manifest exit 1. **4/4 expected outcomes passed.** Local detailed JSON receipt and test logs generated. These tests prove execution in the current ChatGPT environment, not persistent deployment in other AI runtimes.

Persistent Kimi/sister-brain automatic hooks remain unverified; GitHub Actions server-side run remains unverified. No sensitive artifact content included in this public record.
