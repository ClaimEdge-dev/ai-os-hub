#!/usr/bin/env python3
"""DEBO skill delta audit; stdlib, offline, read-only inputs, no external actions."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

try:
    from .debo_registry_audit import audit
except ImportError:
    from debo_registry_audit import audit

PRIORITY = {
    'thread-ops': 100, 'skill-lifecycle-manager': 98,
    'multi-ai-router': 96, 'universal-file-vault': 94,
    'robert-master-os': 92, 'proactive-build-ahead': 85,
}


def key(name):
    return re.sub(r'[^a-z0-9]+', '-', str(name or '').casefold()).strip('-')


def load_rows(path):
    if path is None:
        return []
    p = Path(path)
    if p.suffix.lower() == '.csv':
        with p.open(encoding='utf-8-sig', newline='') as stream:
            return list(csv.DictReader(stream))
    value = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for field in ('results', 'rows', 'skills', 'automations'):
            if isinstance(value.get(field), list):
                return value[field]
    raise ValueError('Expected CSV or JSON array/object containing rows')


def github_statuses(markdown):
    items = {}
    for line in markdown.splitlines():
        if not re.match(r'^\|\s*\d+\s*\|', line):
            continue
        fields = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(fields) >= 5:
            name = fields[1].strip('`')
            items[key(name)] = fields[-1].upper()
    return items


def build_report(markdown, notion_rows=None, skills_root=None, previous=None, automations=None, projects_root=None):
    base = audit(markdown)
    gh = github_statuses(markdown)
    rows = notion_rows or []
    ncounts = Counter(key(r.get('Name') or r.get('name') or r.get('Skill')) for r in rows)
    notion = {}
    for row in rows:
        name = key(row.get('Name') or row.get('name') or row.get('Skill'))
        if name:
            notion[name] = {'status': str(row.get('Status') or row.get('status') or 'UNSPECIFIED').upper(),
                            'version': str(row.get('Version') or row.get('version') or '')}
    root = Path(skills_root) if skills_root else None
    sources = {}
    source_paths = {}
    if root and root.is_dir():
        for folder in root.iterdir():
            if folder.is_dir() and (folder / 'SKILL.md').is_file():
                skill_id = key(folder.name)
                sources[skill_id] = hashlib.sha256((folder / 'SKILL.md').read_bytes()).hexdigest()
                source_paths[skill_id] = f'skills/{folder.name}/SKILL.md'

    # Opt-in project adapters use a scoped ID. Never shadow a DEBO Core skill.
    project_count = 0
    if projects_root and Path(projects_root).is_dir():
        for skill_file in sorted(Path(projects_root).glob('*/skills/*/SKILL.md')):
            project_name = skill_file.parents[2].name
            skill_name = skill_file.parent.name
            project_id, adapter_id = key(project_name), key(skill_name)
            if not project_id or not adapter_id:
                continue
            skill_id = f'project/{project_id}/{adapter_id}'
            sources[skill_id] = hashlib.sha256(skill_file.read_bytes()).hexdigest()
            source_paths[skill_id] = f'projects/{project_name}/skills/{skill_name}/SKILL.md'
            project_count += 1

    old = {row['id']: row.get('fingerprint') for row in (previous or {}).get('skills', [])}
    records = []
    for name in sorted(set(gh) | set(notion) | set(sources)):
        gs = gh.get(name, 'NOT_CATALOGUED')
        ns = notion.get(name, {}).get('status', 'NOT_IN_SNAPSHOT')
        conflict = name in gh and name in notion and gs != ns
        evidence = {'github': gs, 'notion': ns,
                    'notion_version': notion.get(name, {}).get('version', ''),
                    'sha256': sources.get(name)}
        fingerprint = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()
        records.append({'id': name, 'priority': PRIORITY.get(name, 50),
                        'github_status': gs, 'notion_status': ns,
                        'source_sha256': sources.get(name),
                        'source_path': source_paths.get(name),
                        'catalog_conflict': conflict, 'fingerprint': fingerprint,
                        'delta': ('NEW' if name not in old else
                                  'CHANGED' if fingerprint != old[name] else 'UNCHANGED'),
                        'runtime_installed': 'UNVERIFIED'})
    seen_auto = Counter(key(a.get('title') or a.get('Title')) for a in (automations or []))
    return {'schema': 'DEBO-SKILL-DELTA-v1', 'mode': 'READ_ONLY_LOCAL',
            'scope': ('GitHub registry and optional exported snapshots; root plus scoped project sources'
                      if projects_root else 'GitHub registry and optional exported snapshots; root skills only'),
            'summary': {'github_catalog_rows': base['row_count'],
                        'github_duplicate_numbers': base['duplicate_numbers'],
                        'notion_rows': len(rows), 'notion_unique': len(notion),
                        'notion_duplicate_names': sorted(k for k, v in ncounts.items() if k and v > 1),
                        'catalog_conflicts': sum(r['catalog_conflict'] for r in records),
                        'project_skill_sources': project_count,
                        'new_skills': sum(r['delta'] == 'NEW' for r in records),
                        'changed_skills': sum(r['delta'] == 'CHANGED' for r in records),
                        'removed_skills': sorted(set(old) - {r['id'] for r in records}),
                        'automation_rows': len(automations or []),
                        'automation_duplicate_titles': sorted(k for k, v in seen_auto.items() if k and v > 1)},
            'skills': sorted(records, key=lambda r: (-r['priority'], r['id'])),
            'limitations': ['ACTIVE is not an installation receipt',
                            'No automatic Notion or Kimi access',
                            ('Project-local sources are an inventory, not runtime installation proof'
                             if projects_root else 'Project-local inventory requires --include-projects'),
                            'No installs, scheduling changes, external writes or deployment']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--notion', type=Path)
    parser.add_argument('--automations', type=Path)
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--include-projects', action='store_true',
                        help='Include scoped projects/*/skills/*/SKILL.md sources (read-only)')
    args = parser.parse_args()
    previous = json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
    report = build_report((args.repo / 'SKILL_REGISTRY.md').read_text(encoding='utf-8'),
                          load_rows(args.notion), args.repo / 'skills', previous, load_rows(args.automations),
                          projects_root=(args.repo / 'projects' if args.include_projects else None))
    content = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding='utf-8')
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
