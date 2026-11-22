#!/usr/bin/env python3
"""R19 continuity planning guard: offline, no new registry, memory writes or network.

Imports the already-merged R19 capsule validator; emits only safe metadata.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

from debo_r19_continuity import validate_capsule, canonical_bytes, resume_summary

SCHEMA = "debo.r19.continuity_plan.v1"


def _observed_utc(value):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if not dt.tzinfo:
            return None
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def build_plan(capsules, now=None):
    """Read-only plan. Input is ONE project's ONE task lineage, oldest first."""
    if not isinstance(capsules, list) or not capsules:
        raise ValueError('capsules must be a nonempty ordered list')
    for c in capsules:
        validate_capsule(c)
    project, task = capsules[0]['project_id'].casefold(), capsules[0]['task_id']
    if any(c['project_id'].casefold() != project or c['task_id'] != task for c in capsules):
        raise ValueError('cross-project or cross-task comparison refused')

    # Preserve first occurrence; repeated byte-identical saves are not new events.
    deduped, hashes = [], set()
    for c in capsules:
        digest = hashlib.sha256(canonical_bytes(c)).hexdigest()
        if digest not in hashes:
            hashes.add(digest)
            deduped.append(c)
    resume = resume_summary(deduped)

    # Repeated revisions with mutually incompatible reported states need review.
    seen_revisions = {}
    conflict = False
    for c in deduped:
        revision = c.get('source_revision')
        observed = c.get('as_of_utc')
        key = ('revision', revision) if isinstance(revision, str) and revision.strip() else (
            ('observed', observed) if _observed_utc(observed) else None)
        if key is None:
            continue
        state = (c['status'], c['checkpoint'])
        if key in seen_revisions and seen_revisions[key] != state:
            conflict = True
        seen_revisions[key] = state

    clock = now or datetime.now(timezone.utc)
    if clock.tzinfo is None:
        raise ValueError('now must have timezone')
    observed = _observed_utc(deduped[-1].get('as_of_utc'))
    freshness = 'UNKNOWN' if not observed or observed > clock else ('REVERIFY' if (clock - observed).days >= 7 else 'RECENT_REPORT_ONLY')
    decision = 'HOLD_CONFLICT' if conflict else 'REVERIFY_SOURCE' if freshness != 'RECENT_REPORT_ONLY' else 'RECOVER_FROM_CANON'

    # Never surface raw objectives, checkpoint text, source refs, or private data.
    # A memory record candidate is abstract metadata, NOT permission to write.
    safe = {'project_id': deduped[-1]['project_id'], 'task_id': task,
            'reported_status': deduped[-1]['status'], 'conflict': conflict,
            'freshness': freshness}
    return {
        'schema': SCHEMA, 'mode': 'DRY_RUN', 'writes': 0,
        'project_id': safe['project_id'], 'task_id': task,
        'resume': {'decision': decision, 'reported_status': safe['reported_status'],
                   'source_verification': 'REQUIRED', 'evidence_assurance': resume['evidence_assurance'],
                   'repeated_stall': resume['repeated_stall'], 'freshness': freshness},
        'dedupe': {'input_count': len(capsules), 'unique_count': len(deduped),
                   'exact_duplicates': len(capsules)-len(deduped)},
        'conflicts': {'detected': conflict, 'disposition': 'REVIEW_BOTH_CLAIMS' if conflict else 'NONE_DETECTED_NOT_PROOF_OF_AGREEMENT'},
        'checkpoint': {'adapter': 'tools/debo_r19_continuity.py', 'capture': 'OWNER_PRIVATE_SOURCE_ONLY',
                       'automatic_runtime_runner': 'NOT_CONFIGURED', 'recovery': 'CANONICAL_SOURCE_FIRST'},
        'cortex': {'role': 'OPTIONAL_READ_OR_APPROVED_ABSTRACT_METADATA',
                   'candidate_metadata': safe, 'external_write_permitted': False,
                   'second_client_continuity': 'NOT_VERIFIED', 'bulk_sync': False},
        'dashboard': {'existing_feed': 'governance/dashboard/DEBO_CORE_FEED_v1.json',
                      'private_task_data': False, 'editor_live': 'NOT_VERIFIED',
                      'view': 'NOW / MONEY / BLOCKED / DONE', 'project_status': 'UNKNOWN_UNTIL_PRIVATE_READBACK'},
        'router': {'primary': 'EXISTING_CANONICAL_SOURCE_AND_R19_OFFLINE',
                   'fallback': 'AUTHORIZED_CORTEX_READ_IF_RELEVANT',
                   'external_ai_connector': 'NOT_ASSUMED_CONNECTED'},
        'cost': {'policy': 'ZERO_ADDITIONAL_SPEND', 'paid_calls_allowed': False,
                 'paid_calls_executed': 0, 'work_reserve': 'UNCHANGED'},
        'diagnostics': {'status': 'HOLD' if conflict else 'SOURCE_RECHECK_REQUIRED',
                        'cross_tenant_events': 'REJECTED', 'data_export': 'SAFE_METADATA_ONLY',
                        'independent_ai_test': 'NOT_RUN'},
    }


def main():
    parser = argparse.ArgumentParser(description='DEBO R19 optional read-only continuity plan')
    parser.add_argument('--input', type=Path, action='append', required=True,
                        help='Repeat in chronological order; one project and task only')
    args = parser.parse_args()
    capsules = [json.loads(path.read_text(encoding='utf-8')) for path in args.input]
    print(json.dumps(build_plan(capsules), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
