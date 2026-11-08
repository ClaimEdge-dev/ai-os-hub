"""R27 local atomic checkpoint and thread index store. No network or automatic activation."""
import json,os,tempfile
from pathlib import Path
from debo_r26_capsule_validator import fingerprint,validate

def _write_atomic(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.debo-',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(data,f,sort_keys=True,ensure_ascii=False,indent=2)
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def save_capsule(root,capsule,thread_ref,title):
    validate(capsule)
    if capsule['save_readback_status']=='VERIFIED':
        raise ValueError('cannot preclaim readback verification')
    root=Path(root)
    project=capsule['project_id']
    if not project.replace('-','').replace('_','').isalnum():raise ValueError('unsafe project id')
    if not isinstance(thread_ref,str) or not thread_ref.strip():raise ValueError('missing thread reference')
    path=root/'capsules'/(project+'.json')
    if path.exists():
        existing=json.loads(path.read_text(encoding='utf-8'))
        if existing['mission_id']!=capsule['mission_id']:
            raise ValueError('different mission; explicit reconciliation required')
    data=dict(capsule,save_readback_status='UNVERIFIED')
    _write_atomic(path,data)
    observed=json.loads(path.read_text(encoding='utf-8'))
    if fingerprint(observed)!=fingerprint(data):raise RuntimeError('capsule readback mismatch')
    index_path=root/'thread_index.json'
    index=json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else {'schema_version':'1.0','threads':[]}
    threads=[r for r in index['threads'] if r['thread_ref']!=thread_ref]
    threads.append({'thread_ref':thread_ref,'project_id':project,'mission_id':data['mission_id'],'suggested_title':title,'checkpoint_path':str(path.relative_to(root)),'checkpoint_sha256':fingerprint(observed),'next_action':data['next_action'],'status':'CHECKPOINT_READBACK_VERIFIED'})
    index={'schema_version':'1.0','threads':sorted(threads,key=lambda r:r['thread_ref'])}
    _write_atomic(index_path,index)
    actual=json.loads(index_path.read_text(encoding='utf-8'))
    if actual!=index:raise RuntimeError('thread index readback mismatch')
    return {'capsule':str(path),'capsule_sha256':fingerprint(observed),'thread_index':str(index_path),'readback_verified':True,'external_sync':'NOT_CONNECTED'}
