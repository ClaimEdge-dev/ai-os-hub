import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/mcp_worker.mjs';
import { sqliteD1, testEnvironment, executeArguments, callTool } from './helpers/sqlite-d1.mjs';

// Literal wire metadata from MCP 2026-07-28 RequestMetaObject. None of these
// client-reported fields may be used as authenticated caller/project evidence.
const metadata = {
  'io.modelcontextprotocol/protocolVersion': '2026-07-28',
  'io.modelcontextprotocol/clientInfo': { name: 'mcp-wire-regression', version: '1.0.0' },
  'io.modelcontextprotocol/clientCapabilities': {}
};
async function local(fn) {
  const db = sqliteD1();
  try { await fn(db, testEnvironment(db.binding)); } finally { db.close(); }
}
async function rpc(env, method, params = {}, { meta = metadata, version = '2026-07-28' } = {}) {
  const request = new Request('https://synthetic.invalid/mcp', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'accept': 'application/json, text/event-stream', 'mcp-protocol-version': version, 'oai-authenticated-user-id': 'synthetic-owner' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 'wire-1', method, params: { ...params, _meta: meta } })
  });
  const response = await worker.fetch(request, env);
  return { response, body: await response.json() };
}
const assertComplete = result => {
  assert.equal(result?.resultType, 'complete');
  assert.equal(typeof result?._meta?.['io.modelcontextprotocol/serverInfo']?.name, 'string');
  assert.equal(typeof result?._meta?.['io.modelcontextprotocol/serverInfo']?.version, 'string');
};

test('MCP 2 discovery accepts standard per-request metadata and returns required result/cache fields', () => local(async (_, env) => {
  const r = await rpc(env, 'server/discover');
  assert.equal(r.response.status, 200);
  assert.ok(r.body.result, JSON.stringify(r.body));
  assertComplete(r.body.result);
  assert.deepEqual(r.body.result.supportedVersions, ['2026-07-28']);
  assert.deepEqual(r.body.result.capabilities, { tools: {} });
  assert.equal(r.body.result.ttlMs, 0);
  assert.equal(r.body.result.cacheScope, 'private');
}));
test('MCP 2 tool discovery lists both tools with standard client metadata', () => local(async (_, env) => {
  const r = await rpc(env, 'tools/list');
  assert.ok(r.body.result, JSON.stringify(r.body));
  assertComplete(r.body.result);
  assert.deepEqual(r.body.result.tools.map(t => t.name), ['debo_gemini_execute', 'debo_get_receipt']);
  assert.equal(r.body.result.cacheScope, 'private');
  assert.equal(r.body.result.ttlMs, 0);
  for (const tool of r.body.result.tools) assert.equal(tool.inputSchema.type, 'object');
}));
test('MCP 2 caller can read its existing receipt with metadata and no extra write', () => local(async (db, env) => {
  const original = await callTool(worker, env);
  const r = await rpc(env, 'tools/call', { name: 'debo_get_receipt', arguments: { project_id: executeArguments.project_id, idempotency_key: executeArguments.idempotency_key } });
  assertComplete(r.body.result);
  assert.equal(r.body.result.isError, false);
  const value = JSON.parse(r.body.result.content[0].text);
  assert.deepEqual(value.receipt, original.value.receipt);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 1);
}));
test('MCP 2 metadata cannot widen the transport caller project ACL', () => local(async (_, env) => {
  const r = await rpc(env, 'tools/call', { name: 'debo_gemini_execute', arguments: { ...executeArguments, project_id: 'JCT' } }, { meta: { ...metadata, project_id: 'JCT', allowed_projects: ['JCT'], user_id: 'other' } });
  assertComplete(r.body.result);
  assert.equal(r.body.result.isError, true);
  assert.equal(JSON.parse(r.body.result.content[0].text).error.code, 'SCOPE_DENIED');
}));
test('MCP 2 rejects unsupported versions with the canonical version error', () => local(async (_, env) => {
  const r = await rpc(env, 'tools/list', {}, { meta: { ...metadata, 'io.modelcontextprotocol/protocolVersion': '2099-01-01' }, version: '2099-01-01' });
  assert.equal(r.body.error.code, -32022);
  assert.deepEqual(r.body.error.data, { supported: ['2026-07-28'], requested: '2099-01-01' });
  assert.equal(r.response.status, 400);
}));
test('MCP 2 rejects header/body version mismatch before tool dispatch', () => local(async (db, env) => {
  const r = await rpc(env, 'tools/call', { name: 'debo_gemini_execute', arguments: executeArguments }, { version: '2025-11-25' });
  assert.equal(r.response.status, 400);
  assert.equal(r.body.error.code, -32600);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 0);
}));
test('MCP 2 rejects malformed metadata objects', () => local(async (_, env) => {
  for (const meta of [null, [], 'invalid', { ...metadata, 'io.modelcontextprotocol/clientCapabilities': [] }]) {
    const r = await rpc(env, 'server/discover', {}, { meta });
    assert.equal(r.response.status, 400);
    assert.equal(r.body.error.code, -32602);
  }
}));
test('MCP 2 metadata never authorizes a missing transport identity', () => local(async (db, env) => {
  const request = new Request('https://synthetic.invalid/mcp', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { _meta: { ...metadata, user_id: 'synthetic-owner' }, name: 'debo_gemini_execute', arguments: executeArguments } }) });
  assert.equal((await worker.fetch(request, env)).status, 401);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 0);
}));
