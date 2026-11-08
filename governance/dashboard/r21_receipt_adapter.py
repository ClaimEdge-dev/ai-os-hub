"""DEBO R21: read-only governance receipt adapter. Never presents CI as live task sync."""
import json
from pathlib import Path

REQUIRED = {'schema_version','mode','source_url','ci_conclusion','run_number','production_writes','execution_receipts_connected','real_task_imports','owner_holds'}

def build_card(receipt):
    if not REQUIRED.issubset(receipt):
        raise ValueError('receipt missing required fields')
    if receipt['mode'] != 'READ_ONLY_NONPRODUCTION' or receipt['production_writes'] is not False:
        raise ValueError('unsafe receipt mode')
    if receipt['execution_receipts_connected'] is not False or receipt['real_task_imports'] != 0:
        raise ValueError('live/import claim not supported')
    if 'WORK-RENTALS-001' not in receipt['owner_holds']:
        raise ValueError('owner hold missing')
    if receipt['ci_conclusion'] not in ('success','failure','cancelled','skipped'):
        raise ValueError('invalid CI conclusion')
    return {'kind':'nonproduction_ci_evidence','run_number':receipt['run_number'],
            'ci_conclusion':receipt['ci_conclusion'],'source_url':receipt['source_url'],
            'live_task_sync':'NOT_CONNECTED','real_task_imports':0,
            'owner_holds':receipt['owner_holds'],'production_writes':False}

def from_file(path):
    return build_card(json.loads(Path(path).read_text(encoding='utf-8')))

if __name__ == '__main__':
    import sys
    print(json.dumps(from_file(sys.argv[1]),sort_keys=True))
