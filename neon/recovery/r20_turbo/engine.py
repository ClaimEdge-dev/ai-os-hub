"""R20 allowlisted local engine. No network, shell, or production adapters."""
import hashlib, json, os, pathlib, tempfile, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from runner import plan, digest
SAFE_ACTIONS = {'noop', 'verify_text'}

def atomic_json(path, data):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False, encoding='utf8') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.flush(); os.fsync(f.fileno()); tmp = f.name
    os.replace(tmp, path)

def validate(tasks):
    ids = {t['id'] for t in tasks}
    if len(ids) != len(tasks): raise ValueError('duplicate IDs')
    for t in tasks:
        if not set(t.get('depends_on', [])).issubset(ids): raise ValueError('unknown dependency')
        if t.get('action', 'noop') not in SAFE_ACTIONS: raise ValueError('unapproved action')
    graph = {t['id']: t.get('depends_on', []) for t in tasks}
    visiting, visited = set(), set()
    def walk(k):
        if k in visiting: raise ValueError('dependency cycle')
        if k in visited: return
        visiting.add(k)
        for v in graph[k]: walk(v)
        visiting.remove(k); visited.add(k)
    for k in graph: walk(k)

def execute_one(task):
    action = task.get('action', 'noop')
    if action == 'noop': return {'ok': True, 'detail': 'local no-op verified'}
    if action == 'verify_text':
        path = pathlib.Path(task['path'])
        if not path.is_file(): raise FileNotFoundError(str(path))
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != task['sha256']: raise ValueError('source hash mismatch')
        return {'ok': True, 'detail': 'SHA-256 verified', 'sha256': actual}
    raise ValueError('unapproved action')

def _retry(task, attempts):
    for i in range(attempts):
        try: return execute_one(task)
        except (OSError, ValueError) as exc:
            if i == attempts-1: return {'ok': False, 'error': type(exc).__name__+': '+str(exc), 'attempts': i+1}
            time.sleep(min(.05*(2**i), .2))

def run(tasks, receipt_path, workers=3, attempts=2):
    validate(tasks)
    if not (1 <= workers <= 8 and 1 <= attempts <= 3): raise ValueError('unsafe limits')
    receipt_path = pathlib.Path(receipt_path)
    state = json.loads(receipt_path.read_text()) if receipt_path.exists() else {'verified': {}, 'events': []}
    if not isinstance(state.get('verified'), dict): raise ValueError('invalid receipts')
    completed = []
    attempted = set()
    while True:
        candidates, _ = plan(tasks, state['verified'])
        ready = [t for t in candidates if t['id'] not in attempted]
        if not ready: break
        attempted.update(t['id'] for t in ready)
        results = {}
        with ThreadPoolExecutor(max_workers=workers) as pool:
            future_map = {pool.submit(_retry, t, attempts): t for t in ready}
            for future in as_completed(future_map):
                t = future_map[future]; results[t['id']] = future.result()
        advanced = False
        for t in ready:
            result = results[t['id']]
            state['events'].append({'id': t['id'], 'result': result, 'task_hash': digest(t)})
            if result['ok']:
                state['verified'][t['id']] = digest(t)
                completed.append(t['id']); advanced = True
            atomic_json(receipt_path, state)
        if not advanced: break
    _, done = plan(tasks, state['verified'])
    return {'completed': completed, 'verified': sorted(done), 'held': [t['id'] for t in tasks if t.get('owner_hold') or t.get('approval_required')], 'pending': [t['id'] for t in tasks if t['id'] not in done and not t.get('owner_hold') and not t.get('approval_required')]}
