import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Worker } from 'node:worker_threads';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import worker from '../src/mcp_worker.mjs';
import { sha256 } from '../src/synthetic_contract.mjs';
import { sqliteD1, testEnvironment, rpcRequest, callTool, executeArguments } from './helpers/sqlite-d1.mjs';

async function withDatabase(fn) {
  const local = sqliteD1();
  try { return await fn(local, testEnvironment(local.binding)); } finally { local.close(); }
}
const errorCode = result => result.value?.error?.code;
const execute = (env, args = executeArguments, options) => callTool(worker, env, 'debo_gemini_execute', args, options);
const read = (env, args = executeArguments, options) => callTool(worker, env, 'debo_get_receipt', { project_id: args.project_id, idempotency_key: args.idempotency_key }, options);
function isolatedRequest(path, tool, args) {
  return new Promise((resolve, reject) => {
    const thread = new Worker(new URL('./helpers/bridge-request-worker.mjs', import.meta.url), { workerData: { path, tool, args } });
    let value;
    thread.on('message', result => { value = result; });
    thread.on('error', reject);
    thread.on('exit', code => code === 0 && value ? resolve(value) : reject(new Error(`Worker exited ${code}`)));
  });
}

test('MCP discovery advertises the supported Sites protocol', () => withDatabase(async (_, env) => {
  const response = await worker.fetch(rpcRequest('server/discover'), env);
  assert.equal(response.status, 200);
  const result = (await response.json()).result;
  assert.deepEqual(result.supportedVersions, ['2026-07-28']);
  assert.deepEqual(result.capabilities, { tools: {} });
  assert.equal(result.resultType, 'complete');
  assert.equal(result.cacheScope, 'private');
  assert.equal(result.ttlMs, 0);
}));
test('MCP lists only execute and receipt tools with closed argument schemas', () => withDatabase(async (_, env) => {
  const response = await worker.fetch(rpcRequest('tools/list'), env);
  const tools = (await response.json()).result.tools;
  assert.deepEqual(tools.map(t => t.name), ['debo_gemini_execute', 'debo_get_receipt']);
  for (const tool of tools) { assert.equal(tool.inputSchema.additionalProperties, false); assert.ok(!JSON.stringify(tool.inputSchema).includes('token')); }
}));
test('MCP rejects missing transport identity before executing or storing', () => withDatabase(async (local, env) => {
  const r = await execute(env, executeArguments, { headers: { 'oai-authenticated-user-id': '' } });
  assert.equal(r.response.status, 401);
  assert.equal(local.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 0);
}));
test('MCP rejects identity absent from the server project ACL', () => withDatabase(async (_, env) => {
  assert.equal((await execute(env, executeArguments, { headers: { 'oai-authenticated-user-id': 'other-user' } })).response.status, 403);
}));
test('MCP fails closed without an explicitly configured trusted identity boundary', () => withDatabase(async (_, env) => {
  delete env.DEBO_IDENTITY_BOUNDARY;
  assert.equal((await execute(env)).response.status, 503);
}));
test('MCP fails closed on missing or malformed project ACL', () => withDatabase(async (_, env) => {
  for (const value of [undefined, '{bad', '[]', '{"synthetic-owner":"DEBO-CORE"}']) {
    env.DEBO_CALLER_PROJECT_ACL = value;
    assert.equal((await execute(env)).response.status, 503);
  }
}));
test('MCP rejects live mode even when a live flag is configured', () => withDatabase(async (_, env) => {
  env.DEBO_ENABLE_LIVE_GEMINI = 'true';
  assert.equal((await execute(env)).response.status, 503);
  delete env.DEBO_ENABLE_LIVE_GEMINI;
  env.DEBO_BRIDGE_MODE = 'live';
  assert.equal((await execute(env)).response.status, 503);
}));
test('MCP forbids GET tool calls and unexpected routes or query credentials', () => withDatabase(async (_, env) => {
  assert.equal((await worker.fetch(rpcRequest('tools/list', {}, { method: 'GET' }), env)).status, 405);
  assert.equal((await worker.fetch(rpcRequest('tools/list', {}, { url: 'https://synthetic.invalid/other' }), env)).status, 404);
  assert.equal((await worker.fetch(rpcRequest('tools/list', {}, { url: 'https://synthetic.invalid/mcp?key=unused' }), env)).status, 400);
}));
test('MCP rejects cross-origin browser calls and unsupported content types', () => withDatabase(async (_, env) => {
  assert.equal((await execute(env, executeArguments, { headers: { origin: 'https://other.invalid' } })).response.status, 403);
  assert.equal((await execute(env, executeArguments, { headers: { 'content-type': 'text/plain' } })).response.status, 415);
}));
test('MCP bounds actual streamed request bytes without trusting Content-Length', () => withDatabase(async (_, env) => {
  const r = await execute(env, executeArguments, { body: 'x'.repeat(8193), headers: { 'content-length': '1' } });
  assert.equal(r.response.status, 413);
}));
test('MCP rejects malformed JSON and JSON-RPC batches', () => withDatabase(async (_, env) => {
  for (const body of ['{bad', '[]']) assert.equal((await execute(env, executeArguments, { body })).response.status, 400);
}));
test('MCP returns protocol errors for unsupported methods and invalid envelopes', () => withDatabase(async (_, env) => {
  let r = await worker.fetch(rpcRequest('unknown/method'), env);
  assert.equal((await r.json()).error.code, -32601);
  r = await worker.fetch(rpcRequest('tools/list', {}, { body: '{"jsonrpc":"2.0","id":1,"method":"tools/list","extra":true}' }), env);
  assert.equal((await r.json()).error.code, -32600);
}));
test('MCP rejects unknown tools and bearer credentials in arguments', () => withDatabase(async (_, env) => {
  assert.equal(errorCode(await callTool(worker, env, 'arbitrary_tool')), 'TOOL_NOT_ALLOWED');
  assert.equal(errorCode(await execute(env, { ...executeArguments, token: 'do-not-accept' })), 'BAD_REQUEST');
}));
test('MCP denies caller-selected prompts, fixtures, schema and nonzero spend', () => withDatabase(async (_, env) => {
  for (const args of [
    { ...executeArguments, payload: 'SYNTHETIC:private-content' },
    { ...executeArguments, fixture_id: 'unknown' },
    { ...executeArguments, expected_output_schema: {} },
    { ...executeArguments, cost_ceiling_usd: 1 }
  ]) assert.equal(errorCode(await execute(env, args)), 'BAD_REQUEST');
}));
test('MCP enforces project authorization separately for execution and readback', () => withDatabase(async (_, env) => {
  const args = { ...executeArguments, project_id: 'JCT' };
  assert.equal(errorCode(await execute(env, args)), 'SCOPE_DENIED');
  assert.equal(errorCode(await read(env, args)), 'SCOPE_DENIED');
}));
test('MCP saves a bounded, checksum-verified synthetic receipt with zero provider calls', () => withDatabase(async (local, env) => {
  const r = await execute(env);
  assert.equal(r.rpc.result.isError, false);
  assert.equal(r.value.receipt.status, 'TESTED_OFFLINE');
  assert.equal(r.value.receipt.provider, 'synthetic_fixture_only');
  assert.equal(r.value.receipt.network_calls, 0);
  assert.equal(r.value.receipt.actual_cost_usd, 0);
  assert.equal(r.value.deduplicated, false);
  assert.equal(local.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 1);
  assert.deepEqual((await read(env)).value.receipt, r.value.receipt);
}));
test('MCP replay returns the original immutable receipt', () => withDatabase(async (_, env) => {
  const first = await execute(env), second = await execute(env);
  assert.equal(second.value.deduplicated, true);
  assert.deepEqual(second.value.receipt, first.value.receipt);
}));
test('MCP detects conflicting fixture under an existing idempotency key', () => withDatabase(async (_, env) => {
  const first = await execute(env);
  assert.equal(errorCode(await execute(env, { ...executeArguments, fixture_id: 'bridge-replay-v1' })), 'IDEMPOTENCY_CONFLICT');
  assert.deepEqual((await read(env)).value.receipt, first.value.receipt);
}));
test('MCP hides receipts owned by another caller with access to the same project', () => withDatabase(async (_, env) => {
  await execute(env);
  env.DEBO_CALLER_PROJECT_ACL = JSON.stringify({ 'synthetic-owner': ['DEBO-CORE'], 'second-owner': ['DEBO-CORE'] });
  const options = { headers: { 'oai-authenticated-user-id': 'second-owner' } };
  assert.equal((await read(env, executeArguments, options)).value.receipt, null);
  assert.equal(errorCode(await execute(env, executeArguments, options)), 'IDEMPOTENCY_CONFLICT');
}));
test('MCP detects stored output tampering on readback and duplicate replay', () => withDatabase(async (local, env) => {
  await execute(env);
  const row = local.database.prepare('SELECT receipt_json FROM bridge_fixture_receipts').get();
  const receipt = JSON.parse(row.receipt_json);
  receipt.output.finding = 'forged';
  local.database.prepare('UPDATE bridge_fixture_receipts SET receipt_json = ?').run(JSON.stringify(receipt));
  assert.equal(errorCode(await read(env)), 'RECEIPT_INTEGRITY');
  assert.equal(errorCode(await execute(env)), 'RECEIPT_INTEGRITY');
}));
test('MCP rejects corrupted receipt metadata and private datastore errors without echoing them', () => withDatabase(async (local, env) => {
  await execute(env);
  local.database.prepare('UPDATE bridge_fixture_receipts SET input_sha256 = ?').run('0'.repeat(64));
  assert.equal(errorCode(await read(env)), 'RECEIPT_INTEGRITY');
  env.DB = { withSession() { throw new Error('private-sql-and-secret-must-not-leak'); } };
  const result = await read(env);
  assert.equal(errorCode(result), 'STORE_UNAVAILABLE');
  assert.ok(!JSON.stringify(result.rpc).includes('private-sql-and-secret'));
}));
test('MCP fails closed when durable database binding is absent', () => withDatabase(async (_, env) => {
  delete env.DB;
  assert.equal(errorCode(await execute(env)), 'STORE_UNAVAILABLE');
}));
test('MCP receipt lookup validates keys and returns null for an unknown receipt', () => withDatabase(async (_, env) => {
  assert.equal((await read(env)).value.receipt, null);
  assert.equal(errorCode(await read(env, { ...executeArguments, idempotency_key: '../secret' })), 'BAD_REQUEST');
}));
test('MCP responses prevent caching and omit internal error details', () => withDatabase(async (_, env) => {
  const r = await execute(env);
  assert.equal(r.response.headers.get('cache-control'), 'no-store');
  assert.equal(r.response.headers.get('x-content-type-options'), 'nosniff');
}));
test('MCP execution and receipt replay succeed with outbound fetch disabled', () => withDatabase(async (_, env) => {
  const originalFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => { calls++; throw new Error('Outbound requests forbidden'); };
  try {
    assert.equal((await execute(env)).rpc.result.isError, false);
    assert.equal((await read(env)).rpc.result.isError, false);
    assert.equal(calls, 0);
  } finally { globalThis.fetch = originalFetch; }
}));
test('MCP receipt schema rejects forged field types even if checksums are recomputed', () => withDatabase(async (local, env) => {
  await execute(env);
  const row = local.database.prepare('SELECT receipt_json FROM bridge_fixture_receipts').get();
  const receipt = JSON.parse(row.receipt_json);
  receipt.output.finding = { injected: 'not a string' };
  receipt.output_sha256 = await sha256(receipt.output);
  const { receipt_sha256, ...unsigned } = receipt;
  receipt.receipt_sha256 = await sha256(unsigned);
  local.database.prepare('UPDATE bridge_fixture_receipts SET receipt_json = ?').run(JSON.stringify(receipt));
  assert.equal(errorCode(await read(env)), 'RECEIPT_INTEGRITY');
}));
test('MCP same receipt key in two authorized projects remains isolated', () => withDatabase(async (local, env) => {
  env.DEBO_CALLER_PROJECT_ACL = JSON.stringify({ 'synthetic-owner': ['DEBO-CORE', 'JCT'] });
  const core = await execute(env);
  const jctArgs = { ...executeArguments, project_id: 'JCT' };
  const jct = await execute(env, jctArgs);
  assert.notEqual(core.value.receipt.receipt_id, jct.value.receipt.receipt_id);
  assert.equal((await read(env, jctArgs)).value.receipt.project_id, 'JCT');
  assert.equal((await read(env)).value.receipt.project_id, 'DEBO-CORE');
  assert.equal(local.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 2);
}));
test('MCP bounds a stalled datastore request without revealing underlying details', () => withDatabase(async (_, env) => {
  env.DB = { withSession: () => ({ prepare: () => ({ bind: () => ({ first: () => new Promise(() => {}) }) }) }) };
  const result = await execute(env);
  assert.equal(errorCode(result), 'STORE_UNAVAILABLE');
}));
test('MCP concurrent independent worker isolates persist one receipt and replay after restart', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'debo-mcp-isolates-'));
  const path = join(directory, 'receipts.sqlite');
  const local = sqliteD1(path);
  local.close();
  try {
    const results = await Promise.all(Array.from({ length: 6 }, () => isolatedRequest(path, 'debo_gemini_execute', executeArguments)));
    assert.equal(results.filter(r => r.value?.deduplicated === false).length, 1);
    const receipt = results[0].value.receipt;
    for (const r of results) assert.deepEqual(r.value.receipt, receipt);
    const restarted = await isolatedRequest(path, 'debo_get_receipt', { project_id: executeArguments.project_id, idempotency_key: executeArguments.idempotency_key });
    assert.deepEqual(restarted.value.receipt, receipt);
    const replay = await isolatedRequest(path, 'debo_gemini_execute', executeArguments);
    assert.equal(replay.value.deduplicated, true);
    assert.deepEqual(replay.value.receipt, receipt);
  } finally { await rm(directory, { recursive: true, force: true }); }
});
