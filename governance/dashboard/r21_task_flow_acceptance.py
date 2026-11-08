"""Nonproduction end-to-end DEBO source ID -> quarantine -> dashboard projection.
No Neon writes, imports, secrets, or external network calls.
"""
import json
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec

ROOT=Path(__file__).resolve().parents[2]
def load(path,name):
    spec=spec_from_file_location(name,path)
    module=module_from_spec(spec);spec.loader.exec_module(module)
    return module

def build_projection():
    tasks=load(ROOT/'neon/recovery/r21_task_dashboard_offline_test.py','r21_tasks')
    adapter=load(ROOT/'governance/dashboard/r21_receipt_adapter.py','r21_adapter')
    rows=tasks.reconcile(tasks.IDS)
    evidence=adapter.from_file(ROOT/'governance/dashboard/R21_R20_EXECUTION_RECEIPTS_v1.json')
    counts={k:sum(row['decision']==k for row in rows) for k in ('ACCEPT','QUARANTINE','HOLD_OWNER')}
    assert len(rows)==15 and counts=={'ACCEPT':0,'QUARANTINE':14,'HOLD_OWNER':1}
    assert evidence['live_task_sync']=='NOT_CONNECTED' and evidence['real_task_imports']==0
    return {'schema_version':'1.0','classification':'PUBLIC_GOVERNANCE_METADATA_ONLY',
            'mode':'SYNTHETIC_OFFLINE_PROJECTION','source_id_count':len(rows),
            'decision_counts':counts,'held_ids':['WORK-RENTALS-001'],
            'ci_evidence':evidence,'database_writes':0,'dashboard_live_connected':False,
            'warning':'Not a live Work Stack refresh or task import'}

if __name__=='__main__':
    print(json.dumps(build_projection(),indent=2,sort_keys=True))
