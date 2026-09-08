# Morgan’s Perplexity Skills Registry v1.0

Audit Perplexity built-ins first; create only missing project adapters.

- `morgans-master-research-router`
- `morgans-local-market-intelligence`
- `morgans-competitor-intelligence`
- `morgans-hospitality-benchmarks`
- `morgans-menu-engineering-research`
- `morgans-billiards-intelligence`
- `morgans-event-intelligence`
- `morgans-hospitality-tech-scout`
- `morgans-local-seo-research`
- `morgans-reputation-intelligence`
- `morgans-sponsorship-intelligence`
- `morgans-regulatory-research`
- `morgans-source-verification`
- `morgans-handoff-to-debo`

## Skill standard
Every skill should define: YAML frontmatter, purpose, triggers, inputs, source requirements, process, sub-agent strategy, output schema, validation, failure handling, approval gates, and DEBO handoff.

## No-result rule
Never silently fail. Mark `NOT FOUND` or `BLOCKED-BY-ACCESS`, list what was searched, and generate the next DEBO continuation prompt.

## Handoff rule
Substantial missions end with `# COPY THIS BACK TO DEBO` plus `DEBO_IMPORT_MANIFEST.json`.
