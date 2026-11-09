/** DEBO-05 R127 task editor route (existing app integration candidate).
 * Fail closed unless SSO-protected app has a second, separate editor credential.
 * This module never uses the read-only DSN for writes or stores the editor token.
 */
import { createHash, timingSafeEqual } from 'node:crypto';

const STATUSES = new Set(['Backlog', 'Blocked', 'In Progress', 'Review', 'Done']);
const PRIORITIES = new Set(['P0', 'P1', 'P2', 'P3']);
const FIELDS = new Set(['title', 'status', 'priority', 'assignee_role', 'pillar', 'blocked_reason']);
const ID = /^(?:DEBO-LOCAL|WORK)-[A-Z0-9-]{3,80}$/;
const LOCAL_ID = /^DEBO-LOCAL-[A-Z0-9-]{4,60}$/;
const IDEMPOTENCY = /^[A-Za-z0-9-]{16,100}$/;

function fail(code, error) { return { code, error }; }
function secureMatch(supplied, expectedHex) {
  if (typeof supplied !== 'string' || supplied.length < 32 || supplied.length > 256 ||
      typeof expectedHex !== 'string' || !/^[0-9a-f]{64}$/i.test(expectedHex)) return false;
  const actual = createHash('sha256').update(supplied, 'utf8').digest();
  const expected = Buffer.from(expectedHex, 'hex');
  return timingSafeEqual(actual, expected);
}
function parseBody(req) {
  const b = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  if (!b || typeof b !== 'object' || Array.isArray(b)) throw new Error('invalid_payload');
  if (Buffer.byteLength(JSON.stringify(b), 'utf8') > 8192) throw new Error('oversize');
  return b;
}
function validate(action, b) {
  if (!ID.test(b.task_id || '') || b.task_id === 'WORK-RENTALS-001') return 'invalid_task_id';
  if (action === 'create' && !LOCAL_ID.test(b.task_id)) return 'create_requires_local_task_id';
  if (action !== 'create' && (!Number.isSafeInteger(b.expected_revision) || b.expected_revision < 0)) return 'revision_required';
  if (action === 'archive' && (b.fields === undefined || (b.fields && Object.keys(b.fields).length === 0))) return null;
  const o = b.fields;
  if (!o || typeof o !== 'object' || Array.isArray(o)) return 'fields_required';
  if (Object.keys(o).some(k => !FIELDS.has(k))) return 'unknown_field';
  if (action === 'create' && ['title','status','priority','assignee_role','pillar'].some(k => !(k in o))) return 'missing_required_field';
  for (const [k,v] of Object.entries(o)) {
    if (k === 'blocked_reason' && v === null) continue;
    if (typeof v !== 'string' || v.length > (k === 'title' ? 200 : k === 'blocked_reason' ? 1000 : 100) || !v.trim()) return 'invalid_field';
    if (k === 'status' && !STATUSES.has(v)) return 'invalid_status';
    if (k === 'priority' && !PRIORITIES.has(v)) return 'invalid_priority';
  }
  return null;
}

export async function handleEditor(req, res, { env, sql }) {
  res.setHeader('Cache-Control', 'private, no-store, max-age=0');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy', "default-src 'none'");
  const send = (status, obj) => res.status(status).json(obj);
  if (env.DEBO_TASK_EDITOR_ENABLED !== 'true') return send(503, fail(503,'editor_not_enabled'));
  if (!['POST','PATCH','DELETE'].includes(req.method)) return send(405, fail(405,'method_not_allowed'));
  if (typeof env.DEBO_EDITOR_ALLOWED_ORIGIN !== 'string' || !env.DEBO_EDITOR_ALLOWED_ORIGIN.startsWith('https://') ||
      req.headers.origin !== env.DEBO_EDITOR_ALLOWED_ORIGIN || req.headers['sec-fetch-site'] === 'cross-site')
    return send(403, fail(403,'origin_denied'));
  if (!secureMatch(req.headers['x-debo-editor-key'], env.DEBO_EDITOR_KEY_SHA256))
    return send(403, fail(403,'editor_auth_required'));
  if (!env.DEBO_NEON_EDITOR_DSN || !env.DEBO_EDITOR_ACTOR || !/^[A-Za-z0-9_-]{3,50}$/.test(env.DEBO_EDITOR_ACTOR))
    return send(503, fail(503,'editor_not_configured'));
  if (!req.headers['content-type']?.toLowerCase().startsWith('application/json'))
    return send(415, fail(415,'json_required'));
  if (Number(req.headers['content-length'] || 0) > 8192) return send(413, fail(413,'body_too_large'));
  const key = req.headers['idempotency-key'];
  if (typeof key !== 'string' || !IDEMPOTENCY.test(key)) return send(400, fail(400,'idempotency_key_required'));
  let data;
  try { data = parseBody(req); } catch (e) { return send(e.message === 'oversize' ? 413 : 400, fail(400,'invalid_json')); }
  const action = { POST:'create', PATCH:'update', DELETE:'archive' }[req.method];
  const error = validate(action,data);
  if (error) return send(400,fail(400,error));
  try {
    // All three actions are implemented in ONE audited, transactional DB function.
    // The editor DB login should have EXECUTE on this function, no direct DML grants.
    const records = await sql`SELECT claimedge_os.debo_edit_task(
      ${action}::text, ${data.task_id}::text,
      ${JSON.stringify(data.fields || {})}::jsonb,
      ${action === 'create' ? null : data.expected_revision}::integer,
      ${env.DEBO_EDITOR_ACTOR}::text, ${key}::text
    ) AS result`;
    return send(action === 'create' ? 201 : 200, {ok: true, record: records[0]?.result});
  } catch (e) {
    // Do not disclose SQL, credentials or user data to the caller.
    const code = e?.code;
    if (code === '23505') return send(409,fail(409,'duplicate_task_or_operation'));
    if (code === 'P0001') return send(409,fail(409,'edit_conflict_or_owner_hold'));
    return send(503,fail(503,'editor_source_unavailable'));
  }
}
export default async function handler(req,res) {
  if (process.env.DEBO_TASK_EDITOR_ENABLED !== 'true') {
    return handleEditor(req,res,{env:process.env,sql:null});
  }
  const { neon } = await import('@neondatabase/serverless');
  const sql = process.env.DEBO_NEON_EDITOR_DSN ? neon(process.env.DEBO_NEON_EDITOR_DSN) : null;
  return handleEditor(req,res,{env:process.env,sql});
}
