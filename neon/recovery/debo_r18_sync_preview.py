"""DEBO R18 safe, offline source-preserving preview. No database/network writes."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

VALID_STATUSES = {'Backlog', 'In Progress', 'Blocked', 'Review', 'Done'}
VALID_PRIORITIES = {'P0', 'P1', 'P2', 'P3'}
REQUIRED = ('work_id', 'project_id', 'project_name', 'objective', 'state', 'priority', 'owner')


def row_hash(row):
    payload = json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def plan(rows, approvals=None):
    """Never normalize an unapproved status, and never perform a write."""
    mappings = (approvals or {}).get('mappings', {})
    seen, results = set(), []
    for row in rows:
        task_id = str(row.get('work_id') or '').strip()
        if not task_id:
            raise ValueError('Missing work_id')
        if task_id in seen:
            raise ValueError(f'Duplicate work_id: {task_id}')
        seen.add(task_id)
        raw = str(row.get('state') or '')
        rule = mappings.get(raw) or {}
        reviewed = (rule.get('raw_state') == raw and rule.get('status') in VALID_STATUSES
                    and bool(rule.get('approved_by')) and bool(rule.get('approved_at')))
        if 'PARKED BY OWNER' in raw.upper():
            decision = 'HOLD_OWNER'
        elif any(not str(row.get(k) or '').strip() for k in REQUIRED) or row.get('priority') not in VALID_PRIORITIES:
            decision = 'REJECT_REQUIRED_FIELDS'
        elif not reviewed:
            decision = 'QUARANTINE'
        elif not row.get('assignee_role') or not row.get('pillar'):
            decision = 'REVIEW_FIELD_MAPPING'
        else:
            decision = 'ACCEPT'
        results.append({'work_id': task_id, 'decision': decision,
                        'source_row_hash': row_hash(row), 'raw_source_state': raw,
                        'mapped_status': rule.get('status') if reviewed else None})
    counts = dict(Counter(r['decision'] for r in results))
    return {'count': len(results), 'decisions': counts, 'write_eligible': False, 'rows': results}


def run(csv_file, approvals_file):
    with open(csv_file, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            raise ValueError('Required CSV columns missing')
        rows = list(reader)
    with open(approvals_file, encoding='utf-8') as f:
        approvals = json.load(f)
    result = plan(rows, approvals)
    # Do not print raw source states into public console logs.
    return {k: result[k] for k in ('count', 'decisions', 'write_eligible')}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--csv', type=Path, required=True, help='Private local CSV export')
    p.add_argument('--approvals', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(run(args.csv, args.approvals), indent=2))
