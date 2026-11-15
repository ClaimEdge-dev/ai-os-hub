-- DEBO-05 R127 candidate. REVIEW ONLY; DO NOT run against production without
-- approved ownership, original backup and exact branch/tenant acceptance.
-- Designed for existing isolated claimedge_os.tasks, not a second task DB.
-- DELETE means reversible archive. Imported Work Stack rows are owner-held.
BEGIN;
ALTER TABLE claimedge_os.tasks ADD COLUMN IF NOT EXISTS editor_revision integer NOT NULL DEFAULT 0;
ALTER TABLE claimedge_os.tasks ADD COLUMN IF NOT EXISTS archived_at timestamptz;

CREATE TABLE IF NOT EXISTS claimedge_os.task_editor_authorizations (
  task_id text PRIMARY KEY REFERENCES claimedge_os.tasks(task_id),
  approved_by text NOT NULL,
  approval_reference text NOT NULL,
  approved_at timestamptz NOT NULL DEFAULT now(),
  revoked_at timestamptz
);
-- The editor role has NO direct grants on authorizations.
CREATE TABLE IF NOT EXISTS claimedge_os.task_editor_audit (
  idempotency_key text PRIMARY KEY,
  task_id text NOT NULL,
  action text NOT NULL CHECK(action IN ('create','update','archive')),
  actor_label text NOT NULL,
  request_fingerprint text NOT NULL,
  old_record jsonb,
  new_record jsonb NOT NULL,
  result_json jsonb NOT NULL,
  occurred_at timestamptz NOT NULL DEFAULT now()
);
CREATE OR REPLACE FUNCTION claimedge_os.debo_edit_task(
  p_action text, p_task_id text, p_fields jsonb,
  p_expected_revision integer, p_actor text, p_idempotency text
) RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER
SET search_path = pg_catalog, claimedge_os
AS $fn$
DECLARE
  old_rec jsonb;
  new_rec jsonb;
  already_rec record;
  reply jsonb;
  invalid_count integer;
  fingerprint text;
BEGIN
  IF p_action NOT IN ('create','update','archive') OR p_action IS NULL THEN
    RAISE EXCEPTION 'invalid action' USING ERRCODE='P0001';
  END IF;
  IF p_task_id IS NULL OR p_task_id !~ '^(DEBO-LOCAL|WORK)-[A-Z0-9-]{3,80}$'
     OR p_task_id = 'WORK-RENTALS-001' THEN
    RAISE EXCEPTION 'invalid or held task ID' USING ERRCODE='P0001';
  END IF;
  IF p_actor IS NULL OR p_actor !~ '^[A-Za-z0-9_-]{3,50}$' THEN
    RAISE EXCEPTION 'invalid actor' USING ERRCODE='P0001';
  END IF;
  IF p_idempotency IS NULL OR p_idempotency !~ '^[A-Za-z0-9-]{16,100}$' THEN
    RAISE EXCEPTION 'invalid idempotency key' USING ERRCODE='P0001';
  END IF;
  IF p_fields IS NULL OR jsonb_typeof(p_fields) <> 'object' THEN
    RAISE EXCEPTION 'invalid fields' USING ERRCODE='P0001';
  END IF;
  SELECT COUNT(*) INTO invalid_count FROM jsonb_object_keys(p_fields) AS field(key)
    WHERE key NOT IN ('title','status','priority','assignee_role','pillar','blocked_reason');
  IF invalid_count <> 0 THEN
    RAISE EXCEPTION 'unknown fields' USING ERRCODE='P0001';
  END IF;
  IF (p_fields ? 'title' AND (jsonb_typeof(p_fields->'title') <> 'string' OR
       length(trim(p_fields->>'title')) = 0 OR length(p_fields->>'title') > 200)) OR
     (p_fields ? 'status' AND (p_fields->>'status') NOT IN ('Backlog','Blocked','In Progress','Review','Done')) OR
     (p_fields ? 'priority' AND (p_fields->>'priority') NOT IN ('P0','P1','P2','P3')) OR
     (p_fields ? 'assignee_role' AND (jsonb_typeof(p_fields->'assignee_role') <> 'string' OR
       length(trim(p_fields->>'assignee_role'))=0 OR length(p_fields->>'assignee_role')>100)) OR
     (p_fields ? 'pillar' AND (jsonb_typeof(p_fields->'pillar') <> 'string' OR
       length(trim(p_fields->>'pillar'))=0 OR length(p_fields->>'pillar')>100)) OR
     (p_fields ? 'blocked_reason' AND p_fields->'blocked_reason' <> 'null'::jsonb AND
       (jsonb_typeof(p_fields->'blocked_reason') <> 'string' OR length(p_fields->>'blocked_reason')>1000))
  THEN
    RAISE EXCEPTION 'invalid field value' USING ERRCODE='P0001';
  END IF;

  fingerprint=md5(p_action || '|' || p_task_id || '|' || p_fields::text || '|' ||
                  COALESCE(p_expected_revision::text,'null') || '|' || p_actor);
  -- Retries with the same key and exactly same operation return prior result.
  -- Concurrent duplicate keys are rejected atomically by the primary key.
  SELECT action, task_id, request_fingerprint, result_json INTO already_rec
    FROM claimedge_os.task_editor_audit WHERE idempotency_key=p_idempotency;
  IF FOUND THEN
    IF already_rec.action <> p_action OR already_rec.task_id <> p_task_id OR
       already_rec.request_fingerprint <> fingerprint THEN
      RAISE EXCEPTION 'idempotency key reused for another request' USING ERRCODE='P0001';
    END IF;
    RETURN already_rec.result_json;
  END IF;

  IF p_action='create' THEN
    IF p_task_id !~ '^DEBO-LOCAL-[A-Z0-9-]{4,60}$' OR
       NOT(p_fields ?& ARRAY['title','status','priority','assignee_role','pillar']) OR
       p_expected_revision IS NOT NULL THEN
      RAISE EXCEPTION 'create requires approved local task fields' USING ERRCODE='P0001';
    END IF;
    INSERT INTO claimedge_os.tasks
      (task_id,title,status,priority,assignee_role,pillar,blocked_reason,editor_revision)
    VALUES
      (p_task_id, p_fields->>'title', p_fields->>'status', p_fields->>'priority',
       p_fields->>'assignee_role',p_fields->>'pillar',p_fields->>'blocked_reason',0);
    SELECT to_jsonb(t) INTO new_rec FROM claimedge_os.tasks t WHERE task_id=p_task_id;
  ELSE
    IF p_expected_revision IS NULL OR p_expected_revision < 0 THEN
      RAISE EXCEPTION 'revision required' USING ERRCODE='P0001';
    END IF;
    IF p_task_id LIKE 'WORK-%' AND NOT EXISTS (
      SELECT 1 FROM claimedge_os.task_editor_authorizations a
      WHERE a.task_id=p_task_id AND a.revoked_at IS NULL
        AND length(trim(a.approved_by))>0 AND length(trim(a.approval_reference))>0
    ) THEN
      RAISE EXCEPTION 'source-owned Work Stack approval hold' USING ERRCODE='P0001';
    END IF;
    SELECT to_jsonb(t) INTO old_rec FROM claimedge_os.tasks t
      WHERE t.task_id=p_task_id FOR UPDATE;
    IF old_rec IS NULL OR (old_rec->>'editor_revision')::integer <> p_expected_revision OR
       old_rec->>'archived_at' IS NOT NULL THEN
      RAISE EXCEPTION 'missing/archived task or stale revision' USING ERRCODE='P0001';
    END IF;
    IF p_action='update' THEN
      IF p_fields='{}'::jsonb THEN
        RAISE EXCEPTION 'empty update' USING ERRCODE='P0001';
      END IF;
      UPDATE claimedge_os.tasks SET
        title=COALESCE(p_fields->>'title',title),
        status=COALESCE(p_fields->>'status',status),
        priority=COALESCE(p_fields->>'priority',priority),
        assignee_role=COALESCE(p_fields->>'assignee_role',assignee_role),
        pillar=COALESCE(p_fields->>'pillar',pillar),
        blocked_reason=CASE WHEN p_fields ? 'blocked_reason' THEN p_fields->>'blocked_reason' ELSE blocked_reason END,
        editor_revision=editor_revision+1,
        updated_at=now()
      WHERE task_id=p_task_id;
    ELSE
      IF p_fields <> '{}'::jsonb THEN
        RAISE EXCEPTION 'archive does not take fields' USING ERRCODE='P0001';
      END IF;
      UPDATE claimedge_os.tasks SET
        archived_at=now(),editor_revision=editor_revision+1,updated_at=now()
      WHERE task_id=p_task_id;
    END IF;
    SELECT to_jsonb(t) INTO new_rec FROM claimedge_os.tasks t WHERE task_id=p_task_id;
  END IF;
  reply=jsonb_build_object('task_id',p_task_id,'revision',(new_rec->>'editor_revision')::integer,
                           'archived',new_rec->>'archived_at' IS NOT NULL,'action',p_action);
  INSERT INTO claimedge_os.task_editor_audit
    (idempotency_key,task_id,action,actor_label,request_fingerprint,old_record,new_record,result_json)
  VALUES (p_idempotency,p_task_id,p_action,p_actor,fingerprint,old_rec,new_rec,reply);
  RETURN reply;
END;
$fn$;

-- NOLOGIN role is a scoped function permission, not an application credential.
DO $role$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='debo_task_editor_api_r127') THEN
    CREATE ROLE debo_task_editor_api_r127 NOLOGIN;
  END IF;
END;
$role$;
GRANT USAGE ON SCHEMA claimedge_os TO debo_task_editor_api_r127;
REVOKE ALL ON FUNCTION claimedge_os.debo_edit_task(text,text,jsonb,integer,text,text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION claimedge_os.debo_edit_task(text,text,jsonb,integer,text,text)
  TO debo_task_editor_api_r127;
-- There are deliberately NO direct GRANT INSERT, UPDATE or DELETE on tasks.
-- Create a separate limited LOGIN and attach role membership only via an
-- owner-reviewed, secret-managed operation after isolated E2E acceptance.
COMMIT;
