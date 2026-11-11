# DEBO R146 | Action-First Plugin Intelligence (review module)

**Status:** REVIEW BRANCH ONLY. Source candidate committed for inspection; NOT installed in the existing protected Vercel dashboard. No standalone public launch, extra database, replacement prompt compiler or credential change.

## Verified recovery
- DEBO Core: \`ClaimEdge-dev/ai-os-hub\`, current main base \`74b980b\` at development checkout.
- R143 owner editor: draft [PR #44](https://github.com/ClaimEdge-dev/ai-os-hub/pull/44), current head \`645eb648f8f1251ca163235a1732193d07f87d3f\` at review. Its source lives under \`projects/debo-05/task-editor-r127/\`, **not** in repository-root \`src/index.html\`.
- R146 earlier packaged installer assumes \`src/index.html\`. Do not run that installer against this repo until the complete original Vercel app source is recovered and inspected. We stage only an additive module here, no auto-injection.

## What this module provides
1. Three action cards above plugin search, one-tap existing Make a Prompt entry.
2. 147 **source-labelled** capability records, representing the R144 count of 115 observed tool families and 32 spoken/private/native aliases. Snapshot reconstructed from accessible source, **not byte-for-byte identity with Notion's earlier CSV**. This does not prove 147 installed or permitted apps.
3. Read-only responsive search, categories, initially six matches, Show More.
4. Browser-rendered prompt instruction. Does not execute an external task or connect any account.
5. Strict self-origin CSP, textContent-only DOM display, no API, token or private record.

## Integration and release
This lives under \`projects/debo-05/plugin-intelligence-r146/src/\` solely as reviewable code. When the full, original Vercel frontend files are available, link these assets inside the EXISTING protected dashboard without replacing its original CSS, navigation, auth, editor or task feed. Check current PR #44 HEAD, verify branch exact revision, and use a private preview. Do not silently merge or deploy this review PR.

### Test checkpoints
The original local R146 archive had 52/52 synthetic tests PASS. These **newly adapted** GitHub sources require separate CI and code readback. The root CI regression suite discovers \`tests/test_debo*.py\`, including \`tests/test_debo_r146_plugin_intelligence.py\`. Run full review CI and verify its exact commit SHA.

Unfinished real acceptance: authenticated owner create/update/archive with fixture IDs; reader and invalid-key denial; isolated Neon readbacks; physical iPhone Safari + VoiceOver. The R143 protected preview READY state is not proof of any of these.

## Authoritative records
- [R144 Notion capability matrix](https://app.notion.com/p/3e4b37124b6781c4821ef4d9c8e78972)
- [R143/R146 Thread Index](https://app.notion.com/p/3c6b37124b6781f8b6daf738609e7120)
- [Figma R145 design review](https://www.figma.com/design/8HdtU303ueNWGUg0s6ie2T)

**Rollback:** revert this isolated review PR or delete its unmerged branch after owner approval. No production data is involved.