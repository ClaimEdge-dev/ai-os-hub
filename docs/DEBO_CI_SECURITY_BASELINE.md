# DEBO CI Security Baseline v0.1

Status: **PILOT / draft PR**

This workflow is intended to be the reusable minimum CI/security guard for DEBO-managed repositories.

## What it checks

The baseline job:

1. parses every tracked JSON file;
2. fails on unresolved merge-conflict marker sets;
3. blocks tracked sensitive-file types such as private keys and non-template .env files;
4. scans tracked text for a short list of high-confidence secret patterns;
5. never prints a detected secret value.

An optional CodeQL job uses GitHub CodeQL Action v4 when a caller supplies a language.

## Reuse after this baseline is merged

A repository can call the workflow with no CodeQL language:

```yaml
jobs:
  debo-baseline:
    uses: ClaimEdge-dev/ai-os-hub/.github/workflows/debo-ci-security.yml@main
```

Or request CodeQL for a supported language:

```yaml
jobs:
  debo-baseline:
    uses: ClaimEdge-dev/ai-os-hub/.github/workflows/debo-ci-security.yml@main
    with:
      codeql_language: javascript-typescript
```

## Boundaries

- This is a **minimum baseline**, not proof that a repository is secure.
- It does not read GitHub secrets.
- It does not print matched secret values.
- CodeQL is optional because the repository estate spans docs/data/code projects and languages.
- Artifact attestations belong in build/release workflows that actually create artifacts; they are not faked in a generic baseline.
- Repositories with package-specific tests should add their own test/build jobs in addition to this baseline.
- No automatic merge is performed by DEBO. Promotion to an organization-wide standard requires a passing pilot and review.

## Promotion gate

PILOT passes when:

- this workflow runs successfully on its own PR;
- a deliberate safe negative fixture or regression test proves one guard fails when expected, without committing a real secret;
- at least one second repository successfully calls the reusable workflow.

Only after those gates should DEBO treat it as a verified cross-repo baseline.
