# DEBO CI Security Baseline v0.1

Status: **PILOT / draft PR**

This design intentionally separates a **read-only reusable baseline** from a **privileged CodeQL workflow**. That prevents callers from granting security-write permissions merely to run repository hygiene checks.

## Read-only baseline

`.github/workflows/debo-ci-security.yml`:

1. parses every tracked JSON file;
2. detects actual unresolved merge-conflict blocks;
3. blocks tracked sensitive-file types such as private keys and non-template .env files;
4. scans tracked text for a short list of high-confidence secret patterns;
5. never prints a detected secret value;
6. includes safe synthetic regression self-tests for the conflict and token detectors.

### Reuse after merge

```yaml
jobs:
  debo-baseline:
    uses: ClaimEdge-dev/ai-os-hub/.github/workflows/debo-ci-security.yml@main
```

The caller only needs:

```yaml
permissions:
  contents: read
```

## Separate CodeQL workflow

`.github/workflows/debo-codeql.yml` is deliberately separate because GitHub Code Scanning requires elevated token permissions.

A caller that actually needs CodeQL can opt in:

```yaml
permissions:
  contents: read
  security-events: write
  packages: read

jobs:
  codeql:
    uses: ClaimEdge-dev/ai-os-hub/.github/workflows/debo-codeql.yml@main
    with:
      language: javascript-typescript
```

## Pilot findings

The first baseline run caught a false-positive design bug: the conflict detector matched the marker strings inside its own source code. The detector was rewritten to recognize full conflict-marker lines in order and now carries regression self-tests.

The first cross-repo reusable call then hit a startup failure. The likely least-privilege cause was the combined workflow requesting CodeQL write permissions while the caller granted only read access. v0.1 was redesigned to separate those permission domains instead of broadening every caller.

## Boundaries

- These workflows are a minimum guard, not proof a repository is secure.
- They do not read repository secret values.
- Matched secret values are never printed.
- Artifact attestations belong in build/release workflows that actually produce artifacts.
- Package-specific tests/builds remain repository-specific additions.
- No DEBO automatic merge to main.

## Promotion gate

PILOT passes when:

1. the source baseline workflow passes on its own PR;
2. safe detector regression self-tests pass;
3. a second repository successfully invokes the read-only reusable workflow.

Only after those gates should DEBO consider the baseline verified for cross-repo use.
