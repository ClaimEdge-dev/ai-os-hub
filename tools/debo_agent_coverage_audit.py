#!/usr/bin/env python3
"""Read-only DEBO agent registry and on-disk skill-source validation.

Standard-library only. A documented skill is NOT a running or installed agent.
"""
import argparse
import collections
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'governance' / 'DEBO_AGENT_COVERAGE_REGISTER_v1.json'
CORE = {f'DEBO-{name}' for name in (
    'MACK', 'ATLAS', 'FORGE', 'SCOUT', 'PROOF', 'VAULT', 'SHIELD',
    'LEDGER', 'RADAR', 'RELAY', 'PIXEL', 'SWEEP', 'SENTINEL')}
GATES = {'external_message', 'public_release', 'spend', 'production_mutation',
         'delete', 'access_grant', 'credential_change'}


def audit(data, root=ROOT, check_files=True):
    """Return explicit errors and warnings; no writes or external requests."""
    errors, warnings = [], []
    roles = data.get('roles', [])
    role_ids = [r.get('id') for r in roles]
    duplicate_roles = sorted(k for k, n in collections.Counter(role_ids).items() if n > 1)
    if duplicate_roles:
        errors.append(f'duplicate roles: {duplicate_roles}')
    if missing := sorted(CORE - set(role_ids)):
        errors.append(f'missing DEBO board roles: {missing}')
    jct_roles = {r['id'] for r in roles if r.get('project_id') == 'JCT' and r.get('id')}
    for role in roles:
        if role.get('worker_status') in {'RUNNING', 'VERIFIED_RUNNING'}:
            errors.append(f'unsupported running-agent claim: {role.get("id")}')
    projects = [p.get('project_id') for p in data.get('project_adapters', [])]
    if len(projects) != 13 or len(set(projects)) != 13:
        errors.append('expected 13 unique sister projects')
    if data.get('jct', {}).get('root') != 'jct-ops':
        errors.append('JCT root must remain jct-ops')
    skills = data.get('jct', {}).get('skills', [])
    if len(skills) != 50 or data.get('jct', {}).get('documented_specialist_count') != 50:
        errors.append('expected exactly 50 documented JCT specialist skills')
    names = [s.get('skill') for s in skills]
    if len(set(names)) != len(names):
        errors.append('duplicate JCT skill names')
    seen_paths = set()
    safe_root = root.resolve()
    for item in skills:
        name = item.get('skill', '')
        source = item.get('source_path', '')
        expected = f'projects/jcs-towing/skills/{name}/SKILL.md'
        if not re.fullmatch(r'jct-[a-z0-9]+(?:-[a-z0-9]+)*', name):
            errors.append(f'invalid JCT skill name: {name!r}')
        if source != expected:
            errors.append(f'skill source mismatch for {name}: {source!r}')
            continue
        if source in seen_paths:
            errors.append(f'duplicate skill source: {source}')
        seen_paths.add(source)
        if item.get('lead_role') not in jct_roles:
            errors.append(f'missing/cross-tenant JCT lead for {name}')
        if item.get('installed_in_chatgpt') != 'NOT_VERIFIED' or item.get('runtime_tested') != 'NOT_VERIFIED':
            errors.append(f'unsubstantiated runtime claim for {name}')
        if check_files:
            target = root / source
            try:
                target.resolve(strict=True).relative_to(safe_root)
                if not target.is_file() or not target.read_text(encoding='utf8').strip():
                    errors.append(f'missing/empty source file: {source}')
            except (OSError, ValueError, UnicodeError):
                errors.append(f'missing, unreadable or escaped source file: {source}')
    if not GATES.issubset(set(data.get('approval_gates', []))):
        errors.append('missing critical approval gates')
    if data.get('truth_rule', '').lower().find('does not establish') == -1:
        warnings.append('registry must distinguish documented roles from live execution')
    return {
        'status': 'PASS' if not errors else 'FAIL', 'roles': len(roles),
        'jct_skills': len(skills), 'sister_projects': len(projects),
        'source_files_checked': len(seen_paths) if check_files else 0,
        'errors': errors, 'warnings': warnings,
        'note': 'Repository source validation only. Not runtime installation, authentication or hosted workflow verification.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', type=Path, default=REGISTRY)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    report = audit(json.loads(args.registry.read_text(encoding='utf8')), args.root)
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
