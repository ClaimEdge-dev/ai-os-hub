#!/usr/bin/env python3
"""Read-only bridge for DEBO R4 local recovery reports + canonical skill delta reports.

Companion report only. Does not modify canonical tool or infer installation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

CANONICAL_SCHEMA = 'DEBO-SKILL-DELTA-v1'

def key(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', str(name or '').casefold()).strip('-')

def validate_sha(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[a-fA-F0-9]{64}', value))

def source_id(relpath):
    if not isinstance(relpath, str) or '\\' in relpath or relpath.startswith('/'):
        return None
    p = PurePosixPath(relpath)
    if '..' in p.parts or p.name != 'SKILL.md' or any(x.startswith('.') for x in p.parts):
        return None
    parts = p.parts
    if len(parts) == 3 and parts[0] == 'skills':
        return key(parts[1])
    if len(parts) == 5 and parts[0] == 'projects' and parts[2] == 'skills':
        return 'project/' + key(parts[1]) + '/' + key(parts[3])
    return None

def validate_recovery(data):
    if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('files'), list):
        raise ValueError('Expected DEBO R4 recovery schema_version=1 with files list')
    seen = set()
    for rec in data['files']:
        if not isinstance(rec, dict) or not isinstance(rec.get('path'), str) or not validate_sha(rec.get('sha256')):
            raise ValueError('Invalid recovery file path or sha256')
        p = rec['path']
        if p in seen or p.startswith('/') or '\\' in p or '..' in PurePosixPath(p).parts:
            raise ValueError('Duplicate or unsafe recovery path')
        seen.add(p)
    return data

def validate_canonical(data):
    if not isinstance(data, dict) or data.get('schema') != CANONICAL_SCHEMA or not isinstance(data.get('skills'), list):
        raise ValueError('Expected canonical DEBO-SKILL-DELTA-v1 report with skills array')
    ids = set()
    for rec in data['skills']:
        if not isinstance(rec, dict) or not isinstance(rec.get('id'), str):
            raise ValueError('Invalid canonical record')
        if rec['id'] in ids:
            raise ValueError('Ambiguous duplicate canonical ID')
        ids.add(rec['id'])
    return data

def build_bridge(recovery, canonical=None):
    validate_recovery(recovery)
    if canonical is not None:
        validate_canonical(canonical)
    indexed = []
    for f in recovery['files']:
        identifier = source_id(f['path'])
        if identifier:
            indexed.append({'id': identifier, 'relative_path': f['path'], 'sha256': f['sha256'].lower(),
                            'evidence': 'R4_LOCAL_HASH_ONLY', 'runtime_installed': 'UNVERIFIED'})
    by_id = defaultdict(list)
    for item in indexed:
        by_id[item['id']].append(item)
    canon = {r['id']: r for r in (canonical or {}).get('skills', [])}
    matches, mismatches, unknown, ambiguous = [], [], [], []
    for identifier, variants in sorted(by_id.items()):
        if len(variants) != 1:
            ambiguous.append({'id': identifier, 'candidates': variants, 'decision': 'HOLD_AMBIGUOUS_SOURCE'})
            continue
        file = variants[0]
        ref = canon.get(identifier)
        if not ref:
            unknown.append({**file, 'decision': 'SOURCE_PRESENT_NOT_IN_CANONICAL_REPORT'})
            continue
        if ref.get('source_path') != file['relative_path']:
            unknown.append({**file, 'canonical_source_path': ref.get('source_path'),
                            'decision': 'PATH_SCOPE_MISMATCH_REVIEW'})
            continue
        gh = ref.get('source_sha256')
        if not validate_sha(gh):
            unknown.append({**file, 'decision': 'CANONICAL_HASH_MISSING'})
        elif gh.lower() == file['sha256']:
            matches.append({**file, 'decision': 'SOURCE_HASH_MATCH',
                            'canonical_runtime_installed': 'UNVERIFIED'})
        else:
            mismatches.append({**file, 'canonical_sha256': gh.lower(), 'decision': 'SOURCE_HASH_MISMATCH_REVIEW'})
    non_skill_files = len(recovery['files']) - len(indexed)
    return {'schema': 'DEBO-RECOVERY-DELTA-BRIDGE-v1', 'mission': 'DEBO-SKILLS-001-R5',
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'mode': 'READ_ONLY_LOCAL_NO_EXTERNAL_WRITES',
            'canonical_report_provided': canonical is not None,
            'canonical_report_schema': canonical.get('schema') if canonical else None,
            'summary': {'recovery_files': len(recovery['files']), 'skill_sources': len(indexed),
                        'non_skill_files': non_skill_files, 'hash_matches': len(matches),
                        'hash_mismatches': len(mismatches), 'not_matched_or_unverifiable': len(unknown),
                        'ambiguous_names': len(ambiguous)},
            'hash_matches': matches, 'hash_mismatches': mismatches,
            'unmatched_sources': unknown, 'ambiguous_sources': ambiguous,
            'unsupported_comparisons': ['Notion row status cannot be inferred from a local source file',
                'Native ChatGPT installation cannot be inferred from GitHub or local files',
                'A canonical baseline must be generated by the existing tools/debo_skill_delta.py before real GitHub-vs-local hash comparisons'],
            'next_action': 'Run canonical audit on an authorized checkout, then feed its JSON via --canonical-report; inspect mismatches without writing back.'}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--recovery-report', required=True, type=Path)
    p.add_argument('--canonical-report', type=Path, default=None)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args(argv)
    if args.output.exists(): p.error('output exists; no overwrite allowed')
    if args.output.resolve(strict=False) in [args.recovery_report.resolve(), args.canonical_report.resolve() if args.canonical_report else None]:
        p.error('output must not overwrite an input')
    recovery = json.loads(args.recovery_report.read_text(encoding='utf-8'))
    canonical = json.loads(args.canonical_report.read_text(encoding='utf-8')) if args.canonical_report else None
    result = build_bridge(recovery, canonical)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['summary'], sort_keys=True))

if __name__ == '__main__':
    main()
