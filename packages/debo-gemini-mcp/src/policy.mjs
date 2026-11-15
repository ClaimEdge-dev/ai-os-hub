import { timingSafeEqual, createHash } from 'node:crypto';

const PROJECTS = new Set(['DEBO-CORE', 'DEBO-05', 'CLAIMEDGE', 'DWING', 'ALL-ROOFS', 'SETTLESURE', 'JCT', 'P-LOGISTICS', 'RRR', 'MORGANS', 'WRESTLING-OS', 'BASEBALL-OS', 'RENTAL-OS', 'DEBO-CAREER']);
const TASK_TYPES = new Set(['code_review', 'code_generation', 'workspace_audit', 'schema_validation', 'test_fixture_analysis']);
const CLASSIFICATIONS = new Set(['PUBLIC', 'INTERNAL_DEV', 'CONFIDENTIAL_BUSINESS', 'RESTRICTED_PII']);
export class PolicyError extends Error { constructor(code, message) { super(message); this.name='PolicyError'; this.code=code; } }
const fail=(code, text)=>{throw new PolicyError(code,text);};
export function hashJson(object) { return createHash('sha256').update(JSON.stringify(object)).digest('hex'); }
export function assertCaller(provided, expected) {
  if (typeof expected !== 'string' || expected.length < 16) fail('AUTH_UNCONFIGURED', 'Server caller credential not configured');
  if (typeof provided !== 'string') fail('AUTH_INVALID','Caller token missing');
  const a = createHash('sha256').update(provided).digest();
  const b = createHash('sha256').update(expected).digest();
  if (!timingSafeEqual(a,b)) fail('AUTH_INVALID','Caller token invalid');
}
export function validateEndpoint(candidate) {
  let u;
  try { u=new URL(candidate); } catch { fail('ENDPOINT_DENIED','Invalid URL'); }
  if (u.protocol!=='https:' || u.hostname!=='generativelanguage.googleapis.com' || u.port || u.username || u.password || u.search || u.hash || !/^\/v1beta\/models\/[A-Za-z0-9._-]+:generateContent$/.test(u.pathname)) fail('ENDPOINT_DENIED','Non-allowlisted Gemini endpoint');
  return u;
}
export function validateInput(raw) {
  if (!raw || typeof raw!=='object' || Array.isArray(raw)) fail('BAD_REQUEST','Input must be an object');
  const { project_id, task_type, task_description, approved_sources, payload, idempotency_key, privacy_classification='INTERNAL_DEV', mode='read_only', cost_ceiling_usd=0, expected_output_keys=[] }=raw;
  if (!PROJECTS.has(project_id)) fail('SCOPE_VIOLATION','Unknown project');
  if (!TASK_TYPES.has(task_type)) fail('BAD_REQUEST','Unknown task type');
  if (typeof task_description!=='string' || task_description.length<10 || task_description.length>4000) fail('BAD_REQUEST','Invalid task description');
  if (typeof payload!=='string' || !payload.length || payload.length>32000) fail('PAYLOAD_LIMIT','Invalid payload size');
  if (!Array.isArray(approved_sources) || approved_sources.length<1 || approved_sources.length>10 || approved_sources.some(x=>typeof x!=='string'||x.length<1||x.length>256)) fail('BAD_REQUEST','Missing approved source references');
  if (typeof idempotency_key!=='string' || !/^[a-zA-Z0-9._:-]{8,128}$/.test(idempotency_key)) fail('BAD_REQUEST','Invalid idempotency key');
  if (!CLASSIFICATIONS.has(privacy_classification)) fail('BAD_REQUEST','Invalid privacy label');
  if (privacy_classification==='RESTRICTED_PII' || privacy_classification==='CONFIDENTIAL_BUSINESS') fail('PRIVACY_BLOCKED','Sensitive material requires separate authorization and approved routing');
  if (mode!=='read_only') fail('WRITE_DENIED','Offline pilot prohibits all writes to outside systems');
  if (typeof cost_ceiling_usd!=='number'|| !Number.isFinite(cost_ceiling_usd)||cost_ceiling_usd!==0) fail('SPEND_DENIED','Pilot requires zero external spend');
  if (!Array.isArray(expected_output_keys) || expected_output_keys.length>20 || expected_output_keys.some(k=>typeof k!=='string'||!/^[A-Za-z0-9_]{1,64}$/.test(k))) fail('BAD_REQUEST','Invalid output key contract');
  return {project_id,task_type,task_description,approved_sources:[...approved_sources],payload,idempotency_key,privacy_classification,mode,cost_ceiling_usd,expected_output_keys:[...expected_output_keys]};
}
export function validateOutput(out, keys) {
  if(!out || typeof out!=='object'||Array.isArray(out)) fail('INVALID_OUTPUT','Provider output must be JSON object');
  for (const k of keys) if(!Object.hasOwn(out,k)) fail('INVALID_OUTPUT',`Missing expected output key: ${k}`);
  const serialized=JSON.stringify(out);
  if(serialized.length>32000) fail('INVALID_OUTPUT','Provider output exceeds max size');
  return structuredClone(out);
}
