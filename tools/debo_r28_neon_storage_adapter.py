"""R28 Neon/Postgres checkpoint adapter. Requires an explicitly supplied scoped DB connection.
No credentials embedded. Caller owns auth, network and branch isolation.
"""
from debo_r26_capsule_validator import fingerprint,validate

UPSERT_CAPSULE = """INSERT INTO claimedge_os.debo_resume_capsules(project_id,mission_id,capsule,content_sha256)
VALUES (%s,%s,%s::jsonb,%s)
ON CONFLICT (project_id) DO UPDATE SET mission_id=EXCLUDED.mission_id,
capsule=EXCLUDED.capsule,content_sha256=EXCLUDED.content_sha256,
revision=claimedge_os.debo_resume_capsules.revision+1,updated_at=now()
WHERE claimedge_os.debo_resume_capsules.mission_id=EXCLUDED.mission_id
RETURNING content_sha256,revision"""
UPSERT_THREAD = """INSERT INTO claimedge_os.debo_thread_index(thread_ref,project_id,mission_id,suggested_title,checkpoint_sha256,next_action)
VALUES (%s,%s,%s,%s,%s,%s)
ON CONFLICT (thread_ref) DO UPDATE SET project_id=EXCLUDED.project_id,
mission_id=EXCLUDED.mission_id,suggested_title=EXCLUDED.suggested_title,
checkpoint_sha256=EXCLUDED.checkpoint_sha256,next_action=EXCLUDED.next_action,updated_at=now()"""

def save_and_verify(conn,capsule,thread_ref,title):
    """Transactionally save and read back. Caller must provide isolated, authorized DB connection."""
    import json
    validate(capsule)
    if capsule['save_readback_status']=='VERIFIED':
        raise ValueError('preclaimed verification is forbidden')
    if not thread_ref or not title:raise ValueError('thread ref and title required')
    payload=dict(capsule,save_readback_status='UNVERIFIED')
    digest=fingerprint(payload)
    try:
        with conn.cursor() as cur:
            cur.execute(UPSERT_CAPSULE,(payload['project_id'],payload['mission_id'],json.dumps(payload,sort_keys=True),digest))
            if not cur.fetchone():raise ValueError('conflicting mission; no overwrite')
            cur.execute(UPSERT_THREAD,(thread_ref,payload['project_id'],payload['mission_id'],title,digest,payload['next_action']))
            cur.execute('SELECT capsule,content_sha256 FROM claimedge_os.debo_resume_capsules WHERE project_id=%s',(payload['project_id'],))
            row=cur.fetchone()
            if not row or row[1].strip()!=digest or fingerprint(row[0] if isinstance(row[0],dict) else json.loads(row[0]))!=digest:
                raise RuntimeError('database readback mismatch')
            cur.execute('SELECT checkpoint_sha256 FROM claimedge_os.debo_thread_index WHERE thread_ref=%s',(thread_ref,))
            idx=cur.fetchone()
            if not idx or idx[0].strip()!=digest:raise RuntimeError('thread index readback mismatch')
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return {'readback_verified':True,'project_id':payload['project_id'],'sha256':digest,'storage':'postgres','chatgpt_auto_sync':'NOT_CONNECTED'}
