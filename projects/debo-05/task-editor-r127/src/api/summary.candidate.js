/* R127 targeted replacement for EXISTING private DEBO-05 src/api/summary.js.
 * Deploy with schema migration only. Read-only DB role must stay read-only.
 */
import { neon } from '@neondatabase/serverless';
const statuses = ['Backlog','Blocked','In Progress','Review','Done'];
export default async function handler(req,res) {
  res.setHeader('Cache-Control','private, no-store, max-age=0');
  res.setHeader('X-Content-Type-Options','nosniff');
  res.setHeader('Content-Security-Policy',"default-src 'none'");
  if (req.method !== 'GET') return res.status(405).json({error:'method_not_allowed'});
  if (!process.env.DEBO_NEON_READONLY_DSN) return res.status(503).json({error:'not_configured'});
  try {
    const sql = neon(process.env.DEBO_NEON_READONLY_DSN);
    const rows = await sql`SELECT task_id,title,status,priority,assignee_role,pillar,blocked_reason,editor_revision FROM claimedge_os.tasks WHERE archived_at IS NULL ORDER BY task_id LIMIT 501`;
    if (rows.length > 500) throw Error('limit');
    const ids=new Set(),counts={};
    const tasks=rows.map(r=>{
      if(!r.task_id||ids.has(r.task_id)||r.task_id==='WORK-RENTALS-001'||!statuses.includes(r.status)) throw Error('invalid_row');
      if (!Number.isSafeInteger(Number(r.editor_revision)) || Number(r.editor_revision)<0) throw Error('invalid_revision');
      ids.add(r.task_id);counts[r.status]=(counts[r.status]||0)+1;
      return {id:String(r.task_id),title:String(r.title||''),status:r.status,
        priority:String(r.priority||''),owner:String(r.assignee_role||''),project:String(r.pillar||''),
        blocker:r.status==='Blocked'?String(r.blocked_reason||'Not recorded'):null,
        revision:Number(r.editor_revision)};
    });
    return res.status(200).json({schema_version:'debo.private.tasks.r60',source:'isolated_neon',checked_at:new Date().toISOString(),task_count:tasks.length,status_counts:counts,tasks});
  } catch {return res.status(503).json({error:'private_source_unavailable'});}
}
