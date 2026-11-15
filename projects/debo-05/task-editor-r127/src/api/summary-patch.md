# Existing DEBO-05 summary.js patch

Current deployed SQL:

```js
SELECT task_id,title,status,priority,assignee_role,pillar,blocked_reason FROM claimedge_os.tasks ORDER BY task_id LIMIT 501
```

After adding editor_revision and archived_at in the APPROVED isolated branch:

```js
SELECT task_id,title,status,priority,assignee_role,pillar,blocked_reason,editor_revision FROM claimedge_os.tasks WHERE archived_at IS NULL ORDER BY task_id LIMIT 501
```

Each returned task must also include revision:Number(r.editor_revision). Existing security headers, status whitelist, 500-row cap, duplicate ID check, and held Rentals check must remain unchanged. Do not apply this before migration; do not deploy the editor before original UI source recovery and integration acceptance.
