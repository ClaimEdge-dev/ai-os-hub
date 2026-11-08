from dataclasses import dataclass
from hashlib import sha256

ALLOWED = {'Backlog','In Progress','Blocked','Review','Done'}

@dataclass(frozen=True)
class SourceTask:
    work_id: str
    raw_state: str
    title: str
    priority: str
    assignee_role: str
    pillar: str

def normalize(task: SourceTask, approved: dict[str,str]) -> dict:
    assert task.work_id and task.raw_state
    status = approved.get(task.raw_state)
    if 'PARKED BY OWNER' in task.raw_state.upper():
        return {'task_id': task.work_id, 'decision':'HOLD_OWNER', 'raw_state':task.raw_state}
    if status not in ALLOWED:
        return {'task_id':task.work_id,'decision':'QUARANTINE','raw_state':task.raw_state}
    if not task.title or task.priority not in {'P0','P1','P2','P3'} or not task.assignee_role or not task.pillar:
        return {'task_id':task.work_id,'decision':'REJECT_REQUIRED_FIELDS','raw_state':task.raw_state}
    return {'task_id':task.work_id,'decision':'ACCEPT','status':status,'raw_state':task.raw_state,'source_hash':sha256(repr(task).encode()).hexdigest()}

def validate_batch(tasks: list[SourceTask], approved: dict[str,str]) -> list[dict]:
    ids=[t.work_id for t in tasks]
    if len(ids)!=len(set(ids)):
        raise ValueError('duplicate work_id')
    return [normalize(t,approved) for t in tasks]

def test():
    t=SourceTask('WORK-CE-001','SOURCE RECOVERED / GOVERNANCE & LIVE E2E OPEN','ClaimEdge','P2','Proof','CLAIMEDGE')
    assert normalize(t,{})['decision']=='QUARANTINE'
    assert normalize(t,{t.raw_state:'In Progress'})['status']=='In Progress'
    assert normalize(t,{t.raw_state:'In Progress'})['raw_state']==t.raw_state
    assert normalize(t,{t.raw_state:'In Progress'})==normalize(t,{t.raw_state:'In Progress'})
    assert normalize(SourceTask('WORK-RENTALS-001','PARKED BY OWNER / RECORDS PRESERVED','Rentals','P2','Proof','RENTALS'),{'PARKED BY OWNER / RECORDS PRESERVED':'In Progress'})['decision']=='HOLD_OWNER'
    try: validate_batch([t,t],{})
    except ValueError: pass
    else: raise AssertionError('duplicate not rejected')
    assert normalize(SourceTask('WORK-X','READY','', 'P2','Proof','SYSTEMS'),{'READY':'Backlog'})['decision']=='REJECT_REQUIRED_FIELDS'
    print('PASS: 7 assertions / no database writes')

if __name__=='__main__':test()
