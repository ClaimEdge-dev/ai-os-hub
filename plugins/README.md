# ClaimEdge Plugins

This directory contains build artifacts and references for ClaimEdge AI OS skill plugins.

## Source of Truth

**Canonical source files are in `skills/claimedge/policy/`:**

| Skill | Source Path | Status |
|-------|------------|--------|
| Policy Coverage Analyzer | `skills/claimedge/policy/policy-review-coverage-analyzer/v1/` | Complete |
| Policy Endorsement Tracker | `skills/claimedge/policy/policy-review-endorsement-tracker/v1/` | Complete |

## Building .skill Packages

The `.skill` files are ZIP archives of the source directories. To build:

```bash
# From repo root
cd skills/claimedge/policy/policy-review-coverage-analyzer/v1
zip -r ../../../claimedge-policy-review-coverage-analyzer.skill SKILL.md references/

cd ../policy-review-endorsement-tracker/v1
zip -r ../../../claimedge-policy-review-endorsement-tracker.skill SKILL.md references/
```

Or use the packaging script from the skill-creator skill.

## Note on Binary Files

`.skill` binary packages cannot be stored directly in this repo via the MCP tools
(text-only encoding). Build them locally from the source files above.
