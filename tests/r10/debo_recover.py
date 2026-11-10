#!/usr/bin/env python3
"""DEBO Phase 1 source inventory: local/read-only, stdlib-only, no text export.

Input is a directory the operator owns and explicitly chooses. The utility never
follows symlinks and never opens binary/archive interiors; it inventories metadata
and content digests, and records possible *name* duplicates for human review.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

ALLOWED = {'.md', '.txt', '.json', '.jsonl', '.csv', '.yaml', '.yml', '.py', '.js', '.ts', '.html', '.pdf', '.docx', '.xlsx', '.pptx', '.zip'}
DEFAULT_MAX_MB = 50

def normalize_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', Path(name).stem.casefold()).strip()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def collect(root: Path, max_file_bytes: int = DEFAULT_MAX_MB * 1024 * 1024):
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('root must be a directory')
    records, skipped = [], []
    # rglob enumerates symlinks but won't recursively traverse directory symlinks;
    # explicitly reject symlinks at every level and refuse path escapes.
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            skipped.append({'path': str(path.relative_to(root)), 'reason': 'symlink'})
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(part.startswith('.') for part in path.relative_to(root).parts):
            skipped.append({'path': rel, 'reason': 'hidden_path'})
            continue
        if path.suffix.lower() not in ALLOWED:
            skipped.append({'path': rel, 'reason': 'extension_not_allowlisted'})
            continue
        size = path.stat().st_size
        if size > max_file_bytes:
            skipped.append({'path': rel, 'reason': 'size_limit'})
            continue
        records.append({'path': rel, 'filename': path.name, 'size_bytes': size,
                        'sha256': sha256_file(path), 'normalized_name': normalize_name(path.name),
                        'source_status': 'LOCAL_FILE_READ'})
    return records, skipped

def analyze(records, similarity_threshold: float = 0.83):
    byhash = defaultdict(list)
    for rec in records:
        byhash[rec['sha256']].append(rec['path'])
    exact = [{'sha256': digest, 'paths': sorted(paths), 'decision': 'REVIEW_ONLY_NO_DELETE'}
             for digest, paths in byhash.items() if len(paths) > 1]
    possible = []
    # Avoid treating same-content pairs as fuzzy duplicates.
    for i, a in enumerate(records):
        for b in records[i+1:]:
            if a['sha256'] == b['sha256']:
                continue
            an, bn = a['normalized_name'], b['normalized_name']
            if not an or not bn:
                continue
            score = SequenceMatcher(None, an, bn).ratio()
            if score >= similarity_threshold:
                possible.append({'a': a['path'], 'b': b['path'],
                                 'filename_similarity': round(score, 4),
                                 'decision': 'MANUAL_CONTENT_REVIEW'})
    return exact, possible

def build(root: Path, max_mb: int = DEFAULT_MAX_MB, threshold: float = 0.83):
    records, skipped = collect(root, max_mb * 1024 * 1024)
    exact, possible = analyze(records, threshold)
    return {'schema_version': 1, 'mission': 'DEBO-SKILLS-001-R4',
            'generated_utc': datetime.now(timezone.utc).isoformat(),
            'input_root': str(root.resolve()), 'read_only': True,
            'external_calls': 0, 'installed_or_integrated': False,
            'notes': ['Inventory and checksums only; no extracted content or secrets in report',
                      'Filename similarity is a candidate, not proof of identical meaning',
                      'No automatic merge, deletion, archive, or network operation'],
            'summary': {'files': len(records), 'skipped': len(skipped),
                        'exact_duplicate_groups': len(exact),
                        'possible_name_duplicate_pairs': len(possible)},
            'files': records, 'skipped_files': skipped,
            'exact_duplicates': exact, 'potential_name_duplicates': possible}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True, type=Path, help='Explicit authorized local directory')
    p.add_argument('--output', type=Path, required=True, help='New report JSON outside input directory')
    p.add_argument('--max-mb', type=int, default=DEFAULT_MAX_MB)
    p.add_argument('--threshold', type=float, default=.83)
    args = p.parse_args(argv)
    if args.max_mb < 1 or not 0 <= args.threshold <= 1:
        p.error('invalid limit or threshold')
    root = args.root.resolve(strict=True)
    output = args.output.resolve(strict=False)
    if output == root or root in output.parents:
        p.error('report must be outside scanned tree; avoids self-inventory and mutation of sources')
    if output.exists():
        p.error('output exists: choose a new file to avoid overwriting any prior report')
    report = build(root, args.max_mb, args.threshold)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(output), **report['summary']}))

if __name__ == '__main__':
    main()
