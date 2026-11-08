"""CI-only smoke test: all actions are local and allowlisted."""
import json, tempfile
from pathlib import Path
from engine import run
with tempfile.TemporaryDirectory() as d:
    tasks=[{'id':'R20-CI-SMOKE-001','action':'noop'},{'id':'R20-CI-SMOKE-002','action':'noop','depends_on':['R20-CI-SMOKE-001']},{'id':'WORK-RENTALS-001','owner_hold':True}]
    p=Path(d)/'receipt.json'
    first=run(tasks,p); second=run(tasks,p)
    assert first['completed']==['R20-CI-SMOKE-001','R20-CI-SMOKE-002']
    assert second['completed']==[]
    assert first['held']==['WORK-RENTALS-001']
    assert len(json.loads(p.read_text())['events'])==2
    print('R20 CI smoke passed: dependency, hold, receipt, resume')
