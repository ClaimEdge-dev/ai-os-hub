// Local-only candidate for a Sites-dispatch-protected Worker. No HTTP listener,
// provider SDK, outgoing HTTP operation, API key, or production R19 write exists.
import { PolicyError } from './contracts.mjs';
import { argumentSchema, validateArguments, createReceipt } from './synthetic_contract.mjs';
import { D1FixtureStore } from './d1_store.mjs';

const MAX_BODY_BYTES = 8192;
const MCP_VERSION = '2026-07-28';
const SERVER_INFO = { name: 'debo-gemini-private-bridge', version: '0.2.0' };
const deny = (code, message) => { throw new PolicyError(code, message); };
function json(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff', ...extraHeaders } });
}
const protocolError = (id, code, message, status = 200, data) => json({ jsonrpc: '2.0', id, error: { code, message, ...(data === undefined ? {} : { data }) } }, status);
const complete = result => ({ resultType: 'complete', _meta: { 'io.modelcontextprotocol/serverInfo': SERVER_INFO }, ...result });
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);
function protocolMetadataError(body, request) {
  const params = body.params ?? {};
  const header = request.headers.get('mcp-protocol-version');
  // Preserve the existing metadata-free authenticated browser/internal calls.
  // Native MCP 2 callers provide standard per-request metadata, never identity.
  if (!Object.hasOwn(params, '_meta')) {
    if (header && header !== MCP_VERSION) return protocolError(body.id, -32022, 'Unsupported protocol version', 400, { supported: [MCP_VERSION], requested: header });
    return null;
  }
  const meta = params._meta;
  if (!record(meta)) return protocolError(body.id, -32602, 'Invalid request metadata', 400);
  const version = meta['io.modelcontextprotocol/protocolVersion'];
  if (typeof version !== 'string' || !version.length || version.length > 64 || !record(meta['io.modelcontextprotocol/clientCapabilities'])) return protocolError(body.id, -32602, 'Protocol version and client capabilities are required', 400);
  if (header && header !== version) return protocolError(body.id, -32600, 'Protocol header and request metadata disagree', 400);
  if (version !== MCP_VERSION) return protocolError(body.id, -32022, 'Unsupported protocol version', 400, { supported: [MCP_VERSION], requested: version });
  const info = meta['io.modelcontextprotocol/clientInfo'];
  if (info !== undefined && (!record(info) || typeof info.name !== 'string' || typeof info.version !== 'string')) return protocolError(body.id, -32602, 'Invalid client metadata', 400);
  return null;
}
function authenticate(request, env) {
  // Identity headers are trustworthy ONLY behind the documented Sites dispatch.
  // These opt-in flags are configuration guards, not cryptographic attestation.
  if (env?.DEBO_BRIDGE_MODE !== 'synthetic_only' || env?.DEBO_IDENTITY_BOUNDARY !== 'sites_dispatch' || env?.DEBO_ENABLE_LIVE_GEMINI === 'true') deny('CONFIGURATION_REQUIRED', 'Only the synthetic Sites identity boundary may be configured');
  let acl;
  try { acl = JSON.parse(env.DEBO_CALLER_PROJECT_ACL); } catch { deny('CONFIGURATION_REQUIRED', 'Server caller-to-project mapping is required'); }
  if (!acl || typeof acl !== 'object' || Array.isArray(acl) || Object.keys(acl).length === 0 || Object.entries(acl).some(([id, projects]) => !id.length || id.length > 256 || !Array.isArray(projects) || projects.length === 0 || projects.length > 14 || projects.some(p => typeof p !== 'string' || !/^[A-Z][A-Z0-9-]{1,63}$/.test(p)))) deny('CONFIGURATION_REQUIRED', 'Server caller-to-project mapping is invalid');
  const principal = request.headers.get('oai-authenticated-user-id');
  if (!principal) deny('AUTH_REQUIRED', 'Authenticated Sites identity is required');
  if (!Object.hasOwn(acl, principal)) deny('ACCESS_DENIED', 'Caller is not authorized');
  return { principal, projects: acl[principal] };
}
async function boundedJson(request) {
  if (!request.body) deny('BAD_JSON', 'A JSON-RPC body is required');
  const reader = request.body.getReader();
  const chunks = [];
  let length = 0, timer;
  try {
    await Promise.race([
      (async () => {
        for (;;) {
          const { value, done } = await reader.read();
          if (done) return;
          length += value.byteLength;
          if (length > MAX_BODY_BYTES) deny('BODY_LIMIT', 'Request exceeds its byte limit');
          chunks.push(value);
        }
      })(),
      new Promise((_, reject) => { timer = setTimeout(() => reject(new PolicyError('BAD_JSON', 'Request body deadline exceeded')), 1500); })
    ]);
  } finally { clearTimeout(timer); await reader.cancel().catch(() => {}); }
  const bytes = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { deny('BAD_JSON', 'Request must contain valid JSON'); }
}
function validEnvelope(body) {
  return body && typeof body === 'object' && !Array.isArray(body) && body.jsonrpc === '2.0' && typeof body.method === 'string' && body.method.length <= 64 && (typeof body.id === 'string' && body.id.length > 0 && body.id.length <= 128 || Number.isSafeInteger(body.id)) && Object.keys(body).every(k => ['jsonrpc', 'id', 'method', 'params'].includes(k)) && (body.params === undefined || body.params && typeof body.params === 'object' && !Array.isArray(body.params));
}
const tools = [
  { name: 'debo_gemini_execute', description: 'Save or replay a fixed synthetic fixture receipt. No Gemini request, charge or private project input.', inputSchema: argumentSchema(true) },
  { name: 'debo_get_receipt', description: 'Read this caller’s project-scoped synthetic fixture receipt and verify its checksum.', inputSchema: argumentSchema(false) }
];
async function callTool(params, identity, env) {
  try {
    if (!params || !Object.hasOwn(params, 'name') || !Object.hasOwn(params, 'arguments') || Object.keys(params).some(k => !['name', 'arguments', '_meta'].includes(k))) deny('BAD_REQUEST', 'Tool name and arguments are required');
    if (!['debo_gemini_execute', 'debo_get_receipt'].includes(params.name)) deny('TOOL_NOT_ALLOWED', 'Tool is not available');
    const execute = params.name === 'debo_gemini_execute';
    const args = validateArguments(params.arguments, execute);
    if (!identity.projects.includes(args.project_id)) deny('SCOPE_DENIED', 'Caller is not authorized for this project');
    const store = new D1FixtureStore(env.DB);
    const result = execute ? await store.put(identity.principal, args, await createReceipt(args, identity.principal)) : { receipt: await store.read(identity.principal, args) };
    return { content: [{ type: 'text', text: JSON.stringify(result) }], isError: false };
  } catch (error) {
    const safe = error instanceof PolicyError ? { code: error.code, message: error.message } : { code: 'INTERNAL_ERROR', message: 'Synthetic tool request failed' };
    return { content: [{ type: 'text', text: JSON.stringify({ error: safe }) }], isError: true };
  }
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== '/mcp') return protocolError(null, -32600, 'Route not found', 404);
    if (url.search || url.hash || url.username || url.password || url.protocol !== 'https:') return protocolError(null, -32600, 'Invalid MCP URL', 400);
    if (request.method !== 'POST') return json({ error: 'POST required' }, 405, { allow: 'POST' });
    const origin = request.headers.get('origin');
    if (origin && origin !== url.origin) return protocolError(null, -32600, 'Origin is not permitted', 403);
    let identity;
    try { identity = authenticate(request, env); }
    catch (error) { return protocolError(null, -32001, error.message, error.code === 'AUTH_REQUIRED' ? 401 : error.code === 'ACCESS_DENIED' ? 403 : 503); }
    if (!/^application\/json(?:\s*;\s*charset=utf-8)?$/i.test(request.headers.get('content-type') ?? '')) return protocolError(null, -32600, 'JSON content type required', 415);
    let body;
    try { body = await boundedJson(request); }
    catch (error) { return protocolError(null, -32700, 'Invalid or oversized JSON request', error.code === 'BODY_LIMIT' ? 413 : 400); }
    if (!validEnvelope(body)) return protocolError(null, -32600, 'Invalid JSON-RPC request', 400);
    const metadataError = protocolMetadataError(body, request);
    if (metadataError) return metadataError;
    const params = body.params ?? {};
    let result;
    if (body.method === 'tools/call') result = await callTool(params, identity, env);
    else if (body.method === 'tools/list' || body.method === 'server/discover') {
      if (Object.keys(params).some(k => k !== '_meta')) return protocolError(body.id, -32602, 'Unexpected method parameters');
      result = body.method === 'tools/list' ? { tools: structuredClone(tools), ttlMs: 0, cacheScope: 'private' } : { supportedVersions: [MCP_VERSION], capabilities: { tools: {} }, ttlMs: 0, cacheScope: 'private' };
    } else return protocolError(body.id, -32601, 'Method not found');
    return json({ jsonrpc: '2.0', id: body.id, result: complete(result) });
  }
};
