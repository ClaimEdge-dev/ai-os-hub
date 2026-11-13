#!/usr/bin/env python3
"""DEBO skill delta audit; stdlib, offline, read-only inputs, no external actions."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

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


def audit_notion_identities(rows, source_paths):
    """Report incomplete source pointers without resolving names or writing rows.

    An explicit, unique skill_id may look up an already scanned local path.
    Neither that lookup nor a matching URL verifies linked bytes or installation.
    """
    declared_ids = Counter(str(row.get('skill_id') or '').strip() for row in rows)
    duplicates = {sid for sid, count in declared_ids.items() if sid and count > 1}
    entries = []
    for number, row in enumerate(rows, 1):
        name = str(row.get('Name') or row.get('name') or row.get('Skill') or '').strip()
        skill_id = str(row.get('skill_id') or '').strip()
        link = str(row.get('GitHub Link') or '').strip()
        issues = []
        if not name:
            issues.append('NAME_MISSING')
        if not skill_id:
            issues.append('SKILL_ID_MISSING')
        elif skill_id in duplicates:
            issues.append('DUPLICATE_SKILL_ID')
        if not link:
            issues.append('SOURCE_LINK_MISSING')
        source_path = source_paths.get(skill_id) if skill_id not in duplicates else None
        if skill_id and skill_id not in duplicates and source_path is None:
            issues.append('LOCAL_SOURCE_NOT_IN_SCAN')
        if link:
            try:
                parsed = urlsplit(link)
                parts = parsed.path.strip('/').split('/')
                local_link = (parsed.scheme == 'https' and parsed.hostname == 'github.com'
                              and not parsed.username and not parsed.password
                              and len(parts) >= 5 and parts[0].casefold() == 'claimedge-dev'
                              and parts[1].casefold() == 'ai-os-hub' and parts[2] == 'blob')
            except ValueError:
                local_link = False
            if not local_link:
                issues.append('SOURCE_LINK_OUTSIDE_LOCAL_REPOSITORY')
            elif source_path and '/'.join(parts[4:]) != source_path:
                # A suffix can hide archived copies or an unresolved slash ref.
                # Never guess the ref boundary and silently accept either one.
                ambiguous_ref = (parts[3] not in ('main', 'master', 'HEAD')
                                 and not re.fullmatch(r'[0-9a-fA-F]{40}', parts[3])
                                 and '/'.join(parts[4:]).endswith('/' + source_path))
                issues.append('SOURCE_LINK_REF_OR_PATH_UNVERIFIED' if ambiguous_ref
                              else 'SOURCE_LINK_ID_MISMATCH')
        entries.append({'row_number': number, 'notion_url': row.get('url'),
                        'name': name or None, 'skill_id': skill_id or None,
                        'version': row.get('Version') or row.get('version'),
                        'source_link': link or None, 'source_path': source_path,
                        'issues': issues, 'runtime_installed': 'UNVERIFIED'})
    return {'mode': 'SOURCE_POINTER_REVIEW_ONLY',
            'summary': {'rows': len(entries),
                        'missing_names': sum(not e['name'] for e in entries),
                        'missing_skill_ids': sum(not e['skill_id'] for e in entries),
                        'missing_source_links': sum(not e['source_link'] for e in entries),
                        'duplicate_skill_ids': sorted(duplicates),
                        'rows_needing_review': sum(bool(e['issues']) for e in entries)},
            'entries': entries,
            'limitations': ['No title-to-ID inference, row edits or status promotion',
                            'Local source scope excludes unscanned packages and repositories',
                            'URL/path checks do not fetch or verify linked bytes or versions',
                            'No runtime installation evidence']}



# R149-002: optional constrained metadata preflight, not a general YAML parser.
def validate_skill_contract(markdown, directory_name):
    """Inspect basic Agent Skills metadata without installing or modifying skills.

    Complex YAML is marked REVIEW rather than falsely passing validation.
    """
    lines = markdown.splitlines()
    issues = []
    if not lines or lines[0].strip() != '---':
        return {'status': 'REVIEW', 'issues': ['FRONTMATTER_MISSING'],
                'name': None, 'runtime_installed': 'UNVERIFIED'}
    try:
        end = lines.index('---', 1)
    except ValueError:
        return {'status': 'REVIEW', 'issues': ['FRONTMATTER_UNCLOSED'],
                'name': None, 'runtime_installed': 'UNVERIFIED'}
    fields = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith('#'):
            index += 1
            continue
        match = re.fullmatch(r'([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)', line)
        if not match:
            issues.append('COMPLEX_YAML_REQUIRES_REFERENCE_VALIDATOR'
                          if line.startswith((' ', '\t')) else 'YAML_SYNTAX_UNVERIFIED')
            index += 1
            continue
        field, value = match.groups()
        if field in fields:
            issues.append('DUPLICATE_FIELD')
        if value in ('>', '>-', '|', '|-'):
            body = []
            next_index = index + 1
            while next_index < end and (not lines[next_index].strip()
                                         or lines[next_index][0].isspace()):
                body.append(lines[next_index].strip())
                next_index += 1
            fields[field] = (' '.join(part for part in body if part)
                             if value.startswith('>') else '\n'.join(body).strip())
            index = next_index
        else:
            if value.startswith(('"', "'")):
                if len(value) < 2 or value[-1] != value[0]:
                    issues.append('SCALAR_YAML_UNVERIFIED')
                else:
                    value = value[1:-1]
            fields[field] = value.strip()
            index += 1
    name = fields.get('name', '')
    if len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        issues.append('NAME_INVALID')
    if directory_name and name != directory_name:
        issues.append('NAME_DIRECTORY_MISMATCH')
    description = fields.get('description', '')
    if not (1 <= len(description) <= 1024):
        issues.append('DESCRIPTION_LENGTH_INVALID')
    if 'compatibility' in fields and not (1 <= len(fields['compatibility']) <= 500):
        issues.append('COMPATIBILITY_LENGTH_INVALID')
    if not any(x.strip() for x in lines[end + 1:]):
        issues.append('SKILL_BODY_MISSING')
    return {'status': 'PASS' if not issues else 'REVIEW',
            'issues': sorted(set(issues)), 'name': name or None,
            'runtime_installed': 'UNVERIFIED'}


def build_report(markdown, notion_rows=None, skills_root=None, previous=None, automations=None, projects_root=None):
    base = audit(markdown)
    gh = github_statuses(markdown)
    rows = notion_rows or []
    ncounts = Counter(key(r.get('Name') or r.get('name') or r.get('Skill')) for r in rows)
    # Never let the last row win when multiple Notion names normalize to one ID.
    # Until a stable source identity is verified, quarantine the alias instead.
    ambiguous_aliases = {name for name, count in ncounts.items() if name and count > 1}
    notion = {}
    for row in rows:
        name = key(row.get('Name') or row.get('name') or row.get('Skill'))
        if name and name not in ambiguous_aliases:
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
    for name in sorted(set(gh) | set(notion) | set(sources) | ambiguous_aliases):
        gs = gh.get(name, 'NOT_CATALOGUED')
        is_ambiguous = name in ambiguous_aliases
        ns = ('AMBIGUOUS_NOTION_ALIAS' if is_ambiguous else
              notion.get(name, {}).get('status', 'NOT_IN_SNAPSHOT'))
        conflict = not is_ambiguous and name in gh and name in notion and gs != ns
        evidence = {'github': gs, 'notion': ns,
                    'notion_version': notion.get(name, {}).get('version', ''),
                    'sha256': sources.get(name)}
        fingerprint = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()
        records.append({'id': name, 'priority': PRIORITY.get(name, 50),
                        'github_status': gs, 'notion_status': ns,
                        'source_sha256': sources.get(name),
                        'source_path': source_paths.get(name),
                        'catalog_conflict': conflict,
                        'notion_alias_ambiguous': is_ambiguous, 'fingerprint': fingerprint,
                        'delta': ('NEW' if name not in old else
                                  'CHANGED' if fingerprint != old[name] else 'UNCHANGED'),
                        'runtime_installed': 'UNVERIFIED'})
    seen_auto = Counter(key(a.get('title') or a.get('Title')) for a in (automations or []))
    return {'schema': 'DEBO-SKILL-DELTA-v1', 'mode': 'READ_ONLY_LOCAL',
            'scope': ('GitHub registry and optional exported snapshots; root plus scoped project sources'
                      if projects_root else 'GitHub registry and optional exported snapshots; root skills only'),
            'summary': {'github_catalog_rows': base['row_count'],
                        'github_duplicate_numbers': base['duplicate_numbers'],
                        'notion_rows': len(rows), 'notion_unique': sum(bool(k) for k in ncounts),
                        'notion_duplicate_names': sorted(ambiguous_aliases),
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
    parser.add_argument('--validate-contracts', action='store_true',
                        help='Opt-in source-only SKILL.md metadata preflight')
    parser.add_argument('--audit-identities', action='store_true',
                        help='Opt-in review of exported Notion IDs and source links; no matching or writes')
    args = parser.parse_args()
    if args.audit_identities and args.notion is None:
        parser.error('--audit-identities requires an authorized --notion export')
    previous = json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
    notion_rows = load_rows(args.notion)
    report = build_report((args.repo / 'SKILL_REGISTRY.md').read_text(encoding='utf-8'),
                          notion_rows, args.repo / 'skills', previous, load_rows(args.automations),
                          projects_root=(args.repo / 'projects' if args.include_projects else None))
    if args.audit_identities:
        report['identity_audit'] = audit_notion_identities(
            notion_rows, {s['id']: s['source_path'] for s in report['skills'] if s['source_path']})
    if args.validate_contracts:
        entries = []
        for item in report['skills']:
            source_path = item.get('source_path')
            if not source_path:
                continue
            skill_file = args.repo / source_path
            if not skill_file.is_file():
                continue
            check = validate_skill_contract(skill_file.read_text(encoding='utf-8'),
                                            skill_file.parent.name)
            entries.append({'id': item['id'], 'source_path': source_path, **check})
        report['contract_audit'] = {
            'mode': 'SOURCE_ONLY_OPT_IN_REVIEW',
            'checked': len(entries),
            'pass': sum(v['status'] == 'PASS' for v in entries),
            'needs_review': sum(v['status'] != 'PASS' for v in entries),
            'entries': entries,
            'limitation': 'Partial YAML preflight; use official skills-ref in an authorized sandbox; no runtime installation evidence.'
        }
    content = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding='utf-8')
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
