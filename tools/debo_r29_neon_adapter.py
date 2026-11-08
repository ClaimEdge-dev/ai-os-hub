"""R29 Neon SQL adapter: parameterized queries, caller-owned connection, isolated-branch only.
No credentials, network calls, migrations or automatic ChatGPT memory integration.
"""
import json
from debo_r26_capsule_validator import validate,fingerprint

SCHEMA='claimedge_os'

def store_capsule(connection,capsule,expected_revision=0):
    """CAS write; commit is caller-owned. Revision 0 means insert only."""
    validate(capsule)
    if capsule['save_readback_status']=='VERIFIED':raise ValueError('cannot preclaim readback')
    if not isinstance(expected_revision,int) or expected_revision<0:raise ValueError('bad revision')
    payload=json.dumps(capsule,sort_keys=True,separators=(',',':'))
    digest=fingerprint(capsule)
    with connection.cursor() as cur:
        if expected_revision==0:
            cur.execute('INSERT INTO claimedge_os.debo_resume_capsules (project_id,mission_id,capsule,content_sha256,revision) VALUES (%s,%s,%s::jsonb,%s,1) ON CONFLICT (project_id) DO NOTHING RETURNING revision', (capsule['project_id'],capsule['mission_id'],payload,digest))
        else:
            cur.execute('UPDATE claimedge_os.debo_resume_capsules SET capsule=%s::jsonb,content_sha256=%s,revision=revision+1,updated_at=now() WHERE project_id=%s AND mission_id=%s AND revision=%s RETURNING revision',(payload,digest,capsule['project_id'],capsule['mission_id'],expected_revision))
        row=cur.fetchone()
        if row is None:raise ValueError('revision conflict or project already exists')
        revision=row[0]
        cur.execute('SELECT capsule,content_sha256,revision FROM claimedge_os.debo_resume_capsules WHERE project_id=%s AND mission_id=%s',(capsule['project_id'],capsule['mission_id']))
        found=cur.fetchone()
        if found is None or fingerprint(found[0])!=digest or str(found[1]).strip()!=digest or found[2]!=revision:raise RuntimeError('checkpoint readback mismatch')
    return {'project_id':capsule['project_id'],'revision':revision,'sha256':digest,'transaction_readback_verified':True,'committed':False}

def get_capsule(connection,project_id):
    with connection.cursor() as cur:
        cur.execute('SELECT mission_id,capsule,content_sha256,revision FROM claimedge_os.debo_resume_capsules WHERE project_id=%s',(project_id,))
        row=cur.fetchone()
    if row is None:return None
    mission,capsule,sha,revision=row
    validate(capsule)
    if fingerprint(capsule)!=str(sha).strip() or capsule['mission_id']!=mission:raise RuntimeError('stored capsule mismatch')
    return {'capsule':capsule,'revision':revision,'sha256':str(sha).strip()}

def upsert_thread_index(connection,thread_ref,capsule,checkpoint_sha256,title):
    validate(capsule)
    if not isinstance(thread_ref,str) or not thread_ref.strip():raise ValueError('thread ref required')
    if checkpoint_sha256!=fingerprint(capsule):raise ValueError('fingerprint mismatch')
    with connection.cursor() as cur:
        cur.execute('INSERT INTO claimedge_os.debo_thread_index (thread_ref,project_id,mission_id,suggested_title,checkpoint_sha256,next_action) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (thread_ref) DO UPDATE SET project_id=EXCLUDED.project_id,mission_id=EXCLUDED.mission_id,suggested_title=EXCLUDED.suggested_title,checkpoint_sha256=EXCLUDED.checkpoint_sha256,next_action=EXCLUDED.next_action,updated_at=now()', (thread_ref,capsule['project_id'],capsule['mission_id'],title,checkpoint_sha256,capsule['next_action']))
        cur.execute('SELECT project_id,checkpoint_sha256 FROM claimedge_os.debo_thread_index WHERE thread_ref=%s',(thread_ref,))
        row=cur.fetchone()
    if row is None or row[0]!=capsule['project_id'] or str(row[1]).strip()!=checkpoint_sha256:raise RuntimeError('thread index readback mismatch')
    return {'thread_ref':thread_ref,'transaction_readback_verified':True,'committed':False}
