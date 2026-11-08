"""R20 dry-run planner. No external writes."""
import hashlib, json

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def plan(tasks, receipts):
    ids = [t['id'] for t in tasks]
    if len(ids) != len(set(ids)): raise ValueError('duplicate task IDs')
    known = set(ids)
    for t in tasks:
        if not set(t.get('depends_on', [])).issubset(known): raise ValueError('unknown dependency: '+t['id'])
    done = {t['id'] for t in tasks if receipts.get(t['id']) == digest(t)}
    ready = [t for t in tasks if t['id'] not in done and not t.get('owner_hold') and not t.get('approval_required') and set(t.get('depends_on', [])).issubset(done)]
    return ready, done
