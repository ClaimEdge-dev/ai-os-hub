# DEBO Durable-Save Gate (working integration)

Reusable standard-library verification utility for DEBO, ClaimEdge, JCT, PLG, RRR, Bulldogs, and other sister brains.

## Usage

1. Produce an artifact and record its SHA-256.
2. Save the artifact to the approved durable destination.
3. Independently download the saved object into a separate file.
4. Run:

```bash
python tools/debo_durable_save_gate.py ./artifact.zip ./downloaded-artifact.zip
```

An optional `--expected-sha256 HASH` checks the original against a known hash. Exit code 0 means the two files match. Exit code 1 means blocked or failed verification.

**Important:** This utility does not upload, install skills, fetch private data, configure accounts, or approve a release. A matching checksum is only one part of DEBO's seven-step durable-save policy. Use governed storage, live readback, recorded source IDs, and owner approval where required.

## Deployment state

Working GitHub integration only. Do not call this installed in Kimi, ChatGPT, or all sister brains without runtime evidence. No secrets or private project data belong in this public repository.
