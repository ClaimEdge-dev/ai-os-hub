"""DEBO R26 deterministic resume-capsule validation. Stdlib only; no external writes."""
import hashlib
import json
import re

STATES = {'PROPOSED','BUILT','TESTED','VERIFIED','INSTALLED','LIVE'}
REQUIRED = ('schema_version','mission_id','project_id','canonical_sources','thread_index_refs','objective','completed','active_tasks','decisions','owner_holds','blockers','next_action','last_verified_at','source_fingerprint','checkpoint_location','save_readback_status')
SENSITIVE = re.compile(r'(?i)(sk-proj-[a-z0-9_-]+|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:password|api[_-]?key|secret)\s*[:=]\s*[^\s,}]+)')

def fingerprint(data):
    canonical=json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

def validate(capsule):
    if not isinstance(capsule,dict): raise ValueError('capsule must be object')
    missing=[k for k in REQUIRED if k not in capsule]
    if missing: raise ValueError('missing required fields: '+','.join(missing))
    if capsule['schema_version'] != '1.0': raise ValueError('unsupported schema_version')
    if not all(isinstance(capsule[k],str) and capsule[k].strip() for k in ('mission_id','project_id','objective','next_action','last_verified_at','checkpoint_location')): raise ValueError('invalid identifiers or checkpoint')
    for k in ('canonical_sources','thread_index_refs','completed','active_tasks','decisions','owner_holds','blockers'):
        if not isinstance(capsule[k],list): raise ValueError(k+' must be list')
    if capsule['save_readback_status'] not in ('VERIFIED','UNVERIFIED','NOT_SAVED'): raise ValueError('invalid save readback status')
    if not isinstance(capsule['source_fingerprint'],str) or not re.fullmatch('[a-f0-9]{64}',capsule['source_fingerprint']): raise ValueError('invalid source fingerprint')
    for item in capsule['active_tasks']:
        if not isinstance(item,dict) or not item.get('task_id'): raise ValueError('invalid task')
        if item.get('state') not in STATES: raise ValueError('invalid task state')
        if item.get('state')=='LIVE' and not item.get('live_receipt'): raise ValueError('false live claim')
        if item.get('task_id') in capsule['owner_holds'] and item.get('state') in ('INSTALLED','LIVE'): raise ValueError('owner hold violation')
    ids=[item['task_id'] for item in capsule['active_tasks']]
    if len(ids)!=len(set(ids)): raise ValueError('duplicate task identity')
    if SENSITIVE.search(json.dumps(capsule,ensure_ascii=False)): raise ValueError('possible secret in capsule')
    return {'valid':True,'project_id':capsule['project_id'],'tasks':len(ids),'holds':len(capsule['owner_holds']),'readback':capsule['save_readback_status']}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('path');args=p.parse_args()
    with open(args.path,encoding='utf-8') as f: data=json.load(f)
    print(json.dumps(validate(data),sort_keys=True))
