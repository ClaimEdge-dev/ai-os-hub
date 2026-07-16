# ClaimEdge Plugins

This directory contains the ClaimEdge AI OS skill plugins in source form.

## Structure

Each subdirectory contains the source files for a skill plugin:
- `SKILL.md` — The skill trigger file with YAML frontmatter
- `references/` — Reference documentation and templates
- `scripts/` — Optional automation scripts

## Building .skill Packages

To create distributable `.skill` files (ZIP archives):

### Option 1: Use the build script
```bash
./build-skills.sh
```

### Option 2: Manual packaging
```bash
cd /path/to/skill-source/
zip -r ../skill-name.skill SKILL.md references/ scripts/
```

### Option 3: Use the skill-creator skill
```
Run package_skill.py from the skill-creator skill
```

## Available Skills

| # | Skill | Pillar | Status | Source Path |
|---|-------|--------|--------|-------------|
| 2 | Policy Coverage Analyzer | Policy & Coverage | Complete | `claimedge-policy-review-coverage-analyzer/` |
| 3 | Policy Endorsement Tracker | Policy & Coverage | Complete | `claimedge-policy-review-endorsement-tracker/` |

## Pre-built .skill Files

Pre-built `.skill` packages are available as build artifacts.
Build from source using the script above.
