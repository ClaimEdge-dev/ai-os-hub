import { test } from 'node:test';
import assert from 'node:assert/strict';
import { runInNewContext } from 'node:vm';
import worker from '../src/site_worker.mjs';
import { sqliteD1, testEnvironment } from './helpers/sqlite-d1.mjs';

// Exercise the shipped inline page script against the actual Worker and SQLite.
// Only the external Sites routing/identity boundary and DOM controls are modeled.
async function pageHarness(fn, { invalidResponse = false } = {}) {
  const db = sqliteD1();
  const env = { ...testEnvironment(db.binding), DEBO_OWNER_EMAIL: 'owner@example.invalid', DEBO_ENABLE_LIVE_GEMINI: 'false', DEBO_VERIFICATION_REVISION: 'PAGE_TEST' };
  const injectedIdentity = { 'oai-authenticated-user-id': 'page-owner', 'oai-authenticated-user-email': 'owner@example.invalid' };
  const controls = new Map();
  for (const id of ['result', 'runtime', 'run', 'read']) {
    controls.set('#' + id, { textContent: '', disabled: false, listeners: {}, addEventListener(name, action) { this.listeners[name] = action; } });
  }
  const html = await (await worker.fetch(new Request('https://synthetic.invalid/', { headers: injectedIdentity }), env)).text();
  const script = html.match(/<script nonce="[^"]+">([\s\S]*?)<\/script>/)?.[1];
  assert.ok(script, 'Served page includes its executable client script');
  const fetchThroughSites = async (path, init = {}) => {
    // /mcp is a plugin transport boundary, not a browser JSON API. This models
    // the inferred pre-Worker rejection behind the reported parsing failure.
    if (path === '/mcp') return new Response('Plugin transport authorization required', { status: 401, headers: { 'content-type': 'text/plain' } });
    if (invalidResponse && path !== '/api/identity') return new Response('<html>upstream response</html>', { status: 502, headers: { 'content-type': 'text/html' } });
    const headers = new Headers(init.headers);
    for (const [key, value] of Object.entries(injectedIdentity)) headers.set(key, value);
    return worker.fetch(new Request('https://synthetic.invalid' + path, { ...init, headers }), env);
  };
  runInNewContext(script, { document: { querySelector: selector => controls.get(selector) }, fetch: fetchThroughSites });
  try { await fn({ db, controls }); } finally { db.close(); }
}

test('verification button saves and replays one receipt behind the Sites browser boundary', () => pageHarness(async ({ db, controls }) => {
  await controls.get('#run').listeners.click();
  const result = JSON.parse(controls.get('#result').textContent);
  assert.equal(result.status, 'PASS', JSON.stringify(result));
  assert.equal(result.checks.authenticated_owner, true);
  assert.equal(result.checks.cross_project_denied, true);
  assert.equal(result.checks.replay_identical, true);
  assert.equal(result.receipt.network_calls, 0);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 1);
}));

test('saved receipt button uses the authenticated browser path without another write', () => pageHarness(async ({ db, controls }) => {
  await controls.get('#run').listeners.click();
  const first = JSON.parse(controls.get('#result').textContent);
  await controls.get('#read').listeners.click();
  const readback = JSON.parse(controls.get('#result').textContent);
  assert.equal(readback.receipt?.receipt_id, first.receipt?.receipt_id);
  assert.ok(readback.receipt);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 1);
}));

test('verification button reports HTTP context for a non-JSON response', () => pageHarness(async ({ controls }) => {
  await controls.get('#run').listeners.click();
  const result = JSON.parse(controls.get('#result').textContent);
  assert.equal(result.status, 'ERROR');
  assert.match(result.message, /HTTP 502/);
  assert.ok(!result.message.includes('<html>'));
  assert.equal(controls.get('#run').disabled, false);
  assert.equal(controls.get('#read').disabled, false);
}, { invalidResponse: true }));
