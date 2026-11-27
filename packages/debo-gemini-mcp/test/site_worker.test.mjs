import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/site_worker.mjs';
import { sqliteD1, testEnvironment, callTool } from './helpers/sqlite-d1.mjs';
const ownerEmail = 'synthetic-owner@example.invalid';
const options = { headers: { 'oai-authenticated-user-email': ownerEmail } };
async function local(fn) {
  const db = sqliteD1();
  const env = { ...testEnvironment(db.binding), DEBO_OWNER_EMAIL: ownerEmail, DEBO_ENABLE_LIVE_GEMINI: 'false', DEBO_VERIFICATION_REVISION: 'PRIVATE_A' };
  try { return await fn(db, env); } finally { db.close(); }
}
const identityRequest = headers => new Request('https://synthetic.invalid/api/identity', { headers: { 'oai-authenticated-user-id': 'synthetic-owner', 'oai-authenticated-user-email': ownerEmail, ...headers } });
test('private adapter binds verified owner identity to the existing project ACL', () => local(async (_, env) => {
  const result = await callTool(worker, env, undefined, undefined, options);
  assert.equal(result.rpc.result.isError, false);
  assert.equal(result.value.receipt.project_id, 'DEBO-CORE');
  assert.equal(result.value.receipt.network_calls, 0);
}));
test('private adapter rejects missing caller ID even with a matching email', () => local(async (_, env) => {
  assert.equal((await worker.fetch(identityRequest({ 'oai-authenticated-user-id': '' }), env)).status, 401);
}));
test('private adapter rejects a signed-in caller whose verified email is not the owner', () => local(async (_, env) => {
  assert.equal((await worker.fetch(identityRequest({ 'oai-authenticated-user-email': 'another@example.invalid' }), env)).status, 403);
}));
test('private adapter requires explicit disabled live mode and configured owner', () => local(async (_, env) => {
  delete env.DEBO_OWNER_EMAIL;
  assert.equal((await worker.fetch(identityRequest(), env)).status, 503);
  env.DEBO_OWNER_EMAIL = ownerEmail;
  env.DEBO_ENABLE_LIVE_GEMINI = 'true';
  assert.equal((await worker.fetch(identityRequest(), env)).status, 503);
}));
test('private identity endpoint reveals only a scoped digest and does not create receipts', () => local(async (db, env) => {
  const r = await worker.fetch(identityRequest(), env);
  const value = await r.json();
  assert.equal(value.verified_owner, true);
  assert.match(value.caller_sha256, /^[a-f0-9]{64}$/);
  assert.ok(!JSON.stringify(value).includes(ownerEmail));
  assert.ok(!JSON.stringify(value).includes('synthetic-owner'));
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 0);
}));
test('private UI uses platform session identity and contains no caller credential', () => local(async (_, env) => {
  const req = new Request('https://synthetic.invalid/', { headers: { 'oai-authenticated-user-id': 'synthetic-owner', 'oai-authenticated-user-email': ownerEmail } });
  const r = await worker.fetch(req, env);
  const html = await r.text();
  assert.equal(r.status, 200);
  assert.ok(html.includes('Run verification'));
  assert.ok(!html.includes(ownerEmail));
  assert.ok(!html.includes('synthetic-owner'));
  assert.ok(r.headers.get('content-security-policy').includes("default-src 'none'"));
}));
test('private adapter cannot widen the single-project tool scope', () => local(async (_, env) => {
  const r = await callTool(worker, env, 'debo_get_receipt', { project_id: 'JCT', idempotency_key: 'private-runtime-verification-v1' }, options);
  assert.equal(r.value.error.code, 'SCOPE_DENIED');
}));
test('browser verification API rejects missing owner identity before storing a receipt', () => local(async (db, env) => {
  const req = new Request('https://synthetic.invalid/api/fixture', { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' });
  const r = await worker.fetch(req, env);
  assert.equal(r.status, 401);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 0);
}));
