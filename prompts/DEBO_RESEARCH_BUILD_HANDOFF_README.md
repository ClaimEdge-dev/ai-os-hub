# DEBO Research → Build Handoff Kit v1.0

**2026-11-02 · Review-ready, not installed in an external AI.**

This **extends**, and does not replace, the existing DEBO GitHub bootstrap, generated briefs, 72-skill source registry, weekly DEBO System Scout, Notion master and project checkpoints. Source-labelled skills and documented routes are not proof of active runtime capability. The built-in validator is a formatting and honesty gate, not a security audit.

## How to use

1. **Perplexity:** Paste `PERPLEXITY_STARTER_PROMPT.md` into an appropriately scoped Perplexity Search/Computer session. Supply only a minimal non-sensitive project brief and available verified source pointers. Confirm actual connectors/permissions. The user must create/authorize any Perplexity scheduled task separately, if appropriate; this kit does not do that.
2. **Kimi:** Give `DEBO_KIMI_SYSTEM_WIDE_ENGINEERING_COMMAND_v1.md` and the approved **read-only or private** handoff JSON. Ask Kimi to compare code, reuse assets and stage a review branch. It must not treat this file as authorization for live changes.
3. **ChatGPT/DEBO:** Existing DEBO System Scout (weekly, Mondays) can prepare these packets and reconcile findings back to the existing private checkpoint and Installation Register. No duplicate scheduled scout or new master database needed.
4. **Validate:** `python validate_handoff.py DEBO_HANDOFF_EXAMPLE.json` (stdlib checks). Optional full JSON Schema validation: `python -m pip install jsonschema` in an authorized isolated environment, then rerun. No dependencies required to read the kit; don't install packages on a production server just to validate examples.
5. **Save safely:** Research findings may go into an authorized private Notion/Drive project checkpoint and are independently read back; public GitHub is for these **public-safe templates only**. Never put real client, minor, account, health or financial data into public artifacts.

## Files

- `PERPLEXITY_STARTER_PROMPT.md`: Research/integration prompt, compact return contract, optional task instruction.
- `DEBO_KIMI_SYSTEM_WIDE_ENGINEERING_COMMAND_v1.md`: Builder prompt and authority/QA protocol.
- `DEBO_HANDOFF_SCHEMA.json`: Cross-tool handoff contract (JSON Schema Draft 2020-12).
- `DEBO_HANDOFF_EXAMPLE.json`: Fully synthetic example, explicitly not a live state report.
- `validate_handoff.py`: Local check and ranking; not an API, runtime installer or security scanner.
- `manifest.json`: File hashes, source pointers and statuses (generated after test).

## Source links

- Bootstrap: https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/DEBO_BOOTSTRAP.md
- Runtime bootstrap: https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/governance/DEBO_RUNTIME_BOOTSTRAP_v2.md
- Prior Perplexity starter: https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/PERPLEXITY_STARTER_PROMPT.md
- Prior Kimi engineering command: https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/prompts/DEBO_KIMI_SYSTEM_WIDE_ENGINEERING_COMMAND_v1.md
- Installation and verification register: https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/governance/DEBO_INSTALLATION_AND_VERIFICATION_REGISTER_v1.md
- GitHub software advisory database: https://github.com/advisories
- Perplexity Computer feature overview: https://www.perplexity.ai/products/computer

## Checkpoint

**DONE:** Prepared and locally validated source-format kit. **NOT DONE:** Sent to/installed in Perplexity or Kimi; private connector delivery; live app changes; account-memory installation. Next step: complete staged review in the existing repository and test one authorized JCT synthetic handoff in a target runtime.