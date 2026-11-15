import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createStagedSyntheticExecutor } from '../src/guarded_interaction.mjs';
import { executionD1, executionInput as input, executionContext as context } from './helpers/execution-fixtures.mjs';

const credential = 'SYNTHETIC_TEST_CREDENTIAL_NOT_REAL';
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r; }); return { promise, resolve }; };
const interaction = () => ({ id: 'synthetic-interaction-1', status: 'completed', model: 'gemini-3.8-flash', steps: [{ type: 'model_output', content: [{ type: 'text', text: '{"finding":"PASS"}' }] }], usage: { total_input_tokens: 20, total_output_tokens: 5, total_tokens: 25 } });
const response = value => new Response(JSON.stringify(value), { headers: { 'content-type': 'application/json' } });
function config(local, overrides = {}) {
  return { enabled: true, binding: local.binding, context, authorizeRequest: async () => true, transportOptions: { apiKey: credential, fetchImpl: async () => response(interaction()) }, ...overrides };
}
const count = local => local.database.prepare('SELECT count(*) AS n FROM bridge_execution_claims').get().n;
const state = local => local.database.prepare('SELECT state FROM bridge_execution_claims').get()?.state;
// Deliberately occupy one short JS turn: a fulfilled promise can otherwise
// outrun an already-due timer. This is a regression reproduction, not a delay
// model for the deployed Workers clock or a performance benchmark.
const blockTurn = ms => { const end = performance.now() + ms; while (performance.now() < end) {} };

test('staged executor is disabled by default without accessing storage or transport', async () => {
  let touched = 0;
  const executor = createStagedSyntheticExecutor({ binding: { withSession() { touched++; throw Error(); } }, transportOptions: { fetchImpl() { touched++; } } });
  assert.deepEqual(await executor.execute(input), { status: 'BLOCKED', code: 'PROVIDER_DISABLED' });
  assert.equal(touched, 0);
});
test('enabled configuration requires internal authorization and explicit transport dependencies', t => {
  const local = executionD1(); t.after(local.close);
  for (const patch of [{ authorizeRequest: undefined }, { authorizeRequest: true }, { transportOptions: { apiKey: credential } }, { transportOptions: { fetchImpl: async () => response(interaction()) } }, { authorizationDeadlineMs: 0 }]) {
    assert.throws(() => createStagedSyntheticExecutor(config(local, patch)), e => e.code === 'CONFIGURATION_REQUIRED');
  }
  assert.equal(count(local), 0);
});
test('rejected, self-asserted and failing authorization never claim or disclose raw errors', async t => {
  const local = executionD1(); t.after(local.close);
  let calls = 0;
  for (const authorizeRequest of [async () => false, async () => ({ authenticated: true, billing_tier: 'FREE_TIER_UNLINKED' }), async () => { throw Error(credential); }]) {
    const executor = createStagedSyntheticExecutor(config(local, { authorizeRequest, transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
    const denied = await executor.execute(input);
    assert.deepEqual(denied, { status: 'BLOCKED', code: 'AUTHORIZATION_DENIED' });
    assert.equal(JSON.stringify(denied).includes(credential), false);
  }
  assert.equal(count(local), 0); assert.equal(calls, 0);
});
test('invalid inputs, client authorization fields and out-of-scope projects fail before authorization or storage', async t => {
  const local = executionD1(); t.after(local.close);
  let authorizations = 0;
  const executor = createStagedSyntheticExecutor(config(local, { authorizeRequest: async () => { authorizations++; return true; } }));
  for (const patch of [{ authenticated: true }, { enabled: true }, { endpoint: 'https://example.com' }, { payload: 'private data' }, { privacy_classification: 'RESTRICTED_PII' }, { project_id: 'JCT' }, { cost_ceiling_usd: 1 }]) {
    assert.deepEqual(await executor.execute({ ...input, ...patch }), { status: 'BLOCKED', code: 'REQUEST_REJECTED' });
  }
  assert.equal(authorizations, 0); assert.equal(count(local), 0);
});
test('a cancelled request cannot authorize or create a claim', async t => {
  const local = executionD1(); t.after(local.close);
  const controller = new AbortController(); controller.abort();
  const executor = createStagedSyntheticExecutor(config(local, { transportOptions: { apiKey: credential, fetchImpl: async () => { throw Error('must not dispatch'); }, signal: controller.signal } }));
  assert.deepEqual(await executor.execute(input), { status: 'BLOCKED', code: 'REQUEST_REJECTED' });
  assert.equal(count(local), 0);
});
test('dispatch sees a durable claim and exactly the stored normalized wire request', async t => {
  const local = executionD1(); t.after(local.close);
  const phases = []; let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, {
    authorizeRequest: async details => { phases.push(details.phase); assert.equal(Object.isFrozen(details.request.body), true); assert.equal(Object.hasOwn(details, 'owner_token'), false); return true; },
    transportOptions: { apiKey: credential, endpoint: 'https://generativelanguage.googleapis.com/v1beta/interactions', fetchImpl: async (url, init) => {
      calls++; const row = local.database.prepare('SELECT * FROM bridge_execution_claims').get();
      assert.equal(row.state, 'CLAIMED');
      const stored = JSON.parse(row.request_json);
      assert.equal(url, stored.endpoint); assert.deepEqual(JSON.parse(init.body), stored.body);
      assert.equal(init.headers['Api-Revision'], stored.api_revision);
      assert.equal(init.method, 'POST'); assert.equal(init.redirect, 'error');
      return response(interaction());
    } }
  }));
  const result = await executor.execute(input);
  assert.equal(result.status, 'COMPLETED'); assert.equal(result.replayed, false);
  assert.deepEqual(phases, ['before_claim', 'before_dispatch']);
  assert.equal(calls, 1); assert.equal(state(local), 'COMPLETED');
  assert.deepEqual(result.receipt.result.output, { finding: 'PASS' });
  assert.equal(result.receipt.result.billing_verified, false);
  assert.equal(JSON.stringify(result).includes(credential), false);
  assert.equal(JSON.stringify(result).includes('owner_token'), false);
});
test('concurrent duplicates dispatch once and replay the same checked receipt', async t => {
  const local = executionD1(); t.after(local.close);
  const entered = deferred(); const finish = deferred(); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; entered.resolve(); await finish.promise; return response(interaction()); } } }));
  const pending = executor.execute(input); await entered.promise;
  assert.deepEqual(await executor.execute(input), { status: 'UNCERTAIN', code: 'EXECUTION_UNCERTAIN' });
  finish.resolve(); const first = await pending; const replay = await executor.execute(input);
  assert.equal(first.status, 'COMPLETED'); assert.equal(replay.replayed, true);
  assert.deepEqual(replay.receipt, first.receipt); assert.equal(calls, 1); assert.equal(count(local), 1);
});
test('restart replay uses durable state without another provider request', async t => {
  const directory = mkdtempSync(join(tmpdir(), 'debo-guarded-')); t.after(() => rmSync(directory, { recursive: true, force: true }));
  const file = join(directory, 'claims.sqlite'); const first = executionD1(file);
  const original = await createStagedSyntheticExecutor(config(first)).execute(input); first.close();
  const restarted = executionD1(file, false); t.after(restarted.close); let calls = 0;
  const replay = await createStagedSyntheticExecutor(config(restarted, { transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; throw Error(); } } })).execute(input);
  assert.equal(replay.replayed, true); assert.deepEqual(replay.receipt, original.receipt); assert.equal(calls, 0);
});
test('conflicting requests, owners and provider scopes cannot reuse a completed key', async t => {
  const local = executionD1(); t.after(local.close); let calls = 0;
  const transportOptions = { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } };
  const executor = createStagedSyntheticExecutor(config(local, { transportOptions })); await executor.execute(input);
  for (const patch of [{ payload: 'SYNTHETIC:changed' }, { expected_output_keys: ['different'] }]) {
    assert.deepEqual(await executor.execute({ ...input, ...patch }), { status: 'BLOCKED', code: 'IDEMPOTENCY_CONFLICT' });
  }
  for (const patch of [{ principal: 'other-synthetic-owner' }, { providerScope: 'other-synthetic-project' }]) {
    assert.deepEqual(await createStagedSyntheticExecutor(config(local, { context: { ...context, ...patch }, transportOptions })).execute(input), { status: 'BLOCKED', code: 'IDEMPOTENCY_CONFLICT' });
  }
  assert.equal(calls, 1);
});
test('caller mutations during authorization cannot alter the claimed dispatch', async t => {
  const local = executionD1(); t.after(local.close); const entered = deferred(); const allow = deferred();
  const changingInput = structuredClone(input); const changingContext = structuredClone(context);
  const transportOptions = { apiKey: credential, fetchImpl: async (url, init) => {
    assert.equal(url, 'https://generativelanguage.googleapis.com/v1/interactions');
    assert.equal(JSON.parse(init.body).model, 'gemini-3.8-flash'); return response(interaction());
  } };
  const executor = createStagedSyntheticExecutor(config(local, { context: changingContext, transportOptions, authorizeRequest: async details => { if (details.phase === 'before_claim') { entered.resolve(); await allow.promise; } return true; } }));
  const pending = executor.execute(changingInput); await entered.promise;
  changingInput.payload = 'private'; changingInput.expected_output_keys[0] = 'changed';
  changingContext.principal = 'changed'; changingContext.projects.length = 0;
  transportOptions.endpoint = 'https://example.com'; transportOptions.model = 'different'; transportOptions.apiKey = '';
  allow.resolve(); const result = await pending;
  assert.equal(result.status, 'COMPLETED'); assert.deepEqual(result.receipt.result.output, { finding: 'PASS' });
});
test('authorization revoked at dispatch blocks the key without making a provider call', async t => {
  const local = executionD1(); t.after(local.close); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { authorizeRequest: async details => details.phase === 'before_claim', transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.deepEqual(await executor.execute(input), { status: 'UNCERTAIN', code: 'EXECUTION_UNCERTAIN' });
  assert.equal(state(local), 'UNCERTAIN');
  assert.equal((await executor.execute(input)).status, 'UNCERTAIN'); assert.equal(calls, 0);
});
for (const kind of ['network', 'quota', 'gateway', 'bad_json', 'bad_usage']) test(`${kind} failure persists an uncertain barrier and never retries`, async t => {
  const local = executionD1(); t.after(local.close); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { transportOptions: { apiKey: credential, fetchImpl: async () => {
    calls++;
    if (kind === 'network') throw Error(credential);
    if (kind === 'quota' || kind === 'gateway') return new Response(credential, { status: kind === 'quota' ? 429 : 503 });
    if (kind === 'bad_json') return new Response('{broken', { headers: { 'content-type': 'application/json' } });
    return response({ ...interaction(), usage: {} });
  } } }));
  const result = await executor.execute(input);
  assert.deepEqual(result, { status: 'UNCERTAIN', code: 'EXECUTION_UNCERTAIN' });
  assert.equal(state(local), 'UNCERTAIN'); assert.equal(JSON.stringify(result).includes(credential), false);
  assert.deepEqual(await executor.execute(input), result); assert.equal(calls, 1);
});
test('post-dispatch persistence failure never permits another provider attempt', async t => {
  const local = executionD1(); t.after(local.close); const session = local.binding.withSession('first-primary'); let calls = 0;
  const binding = { withSession: () => ({ prepare(sql) { if (sql.includes("SET state = 'COMPLETED'")) throw Error(credential); return session.prepare(sql); } }) };
  const executor = createStagedSyntheticExecutor(config(local, { binding, transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.equal((await executor.execute(input)).status, 'UNCERTAIN');
  assert.equal((await executor.execute(input)).status, 'UNCERTAIN'); assert.equal(calls, 1);
});
test('lost completion acknowledgement is recovered by replay, not redispatch', async t => {
  const local = executionD1(); t.after(local.close); const session = local.binding.withSession('first-primary'); let calls = 0;
  const binding = { withSession: () => ({ prepare(sql) {
    const statement = session.prepare(sql);
    if (!sql.includes("SET state = 'COMPLETED'")) return statement;
    return { bind: (...values) => ({ first: async () => { await statement.bind(...values).first(); throw Error('lost acknowledgement'); } }) };
  } }) };
  const executor = createStagedSyntheticExecutor(config(local, { binding, transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.equal((await executor.execute(input)).status, 'UNCERTAIN');
  const replay = await executor.execute(input); assert.equal(replay.status, 'COMPLETED'); assert.equal(replay.replayed, true); assert.equal(calls, 1);
});
test('storage deadlines fail closed before dispatch', async () => {
  let calls = 0;
  const binding = { withSession: () => ({ prepare: () => ({ bind: () => ({ first: async () => new Promise(() => {}) }) }) }) };
  const executor = createStagedSyntheticExecutor({ enabled: true, binding, context, authorizeRequest: async () => true, storageOptions: { deadlineMs: 15 }, transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } });
  assert.equal((await executor.execute(input)).status, 'UNCERTAIN'); assert.equal(calls, 0);
});
test('a late pre-claim authorization cannot create a row after its deadline', async t => {
  const local = executionD1(); t.after(local.close); const allow = deferred();
  const executor = createStagedSyntheticExecutor(config(local, { authorizationDeadlineMs: 15, authorizeRequest: async () => allow.promise }));
  assert.deepEqual(await executor.execute(input), { status: 'BLOCKED', code: 'AUTHORIZATION_DENIED' });
  allow.resolve(true); await new Promise(setImmediate); assert.equal(count(local), 0);
});
test('a late dispatch authorization cannot start fetch after the transport timeout', async t => {
  const local = executionD1(); t.after(local.close); const allow = deferred(); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { authorizationDeadlineMs: 200, authorizeRequest: async details => details.phase === 'before_claim' ? true : allow.promise, transportOptions: { apiKey: credential, timeoutMs: 15, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.equal((await executor.execute(input)).status, 'UNCERTAIN');
  allow.resolve(true); await new Promise(setImmediate);
  assert.equal(calls, 0); assert.equal(state(local), 'UNCERTAIN');
});
test('a provider response arriving after cancellation cannot complete or repeat the claim', async t => {
  const local = executionD1(); t.after(local.close); const entered = deferred(); const finish = deferred();
  const controller = new AbortController(); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { transportOptions: { apiKey: credential, signal: controller.signal, fetchImpl: async () => { calls++; entered.resolve(); await finish.promise; return response(interaction()); } } }));
  const pending = executor.execute(input); await entered.promise; controller.abort();
  assert.equal((await pending).status, 'UNCERTAIN');
  finish.resolve(); await new Promise(setImmediate); assert.equal(state(local), 'UNCERTAIN');
  const fresh = createStagedSyntheticExecutor(config(local, { transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.equal((await fresh.execute(input)).status, 'UNCERTAIN'); assert.equal(calls, 1);
});
test('a lost claim acknowledgement never dispatches or grants a replacement claim', async t => {
  const local = executionD1(); t.after(local.close); const session = local.binding.withSession('first-primary'); let calls = 0;
  const binding = { withSession: () => ({ prepare(sql) {
    const statement = session.prepare(sql);
    if (!sql.startsWith('INSERT')) return statement;
    return { bind: (...values) => ({ first: async () => { await statement.bind(...values).first(); throw Error('claim acknowledgement lost'); } }) };
  } }) };
  const transportOptions = { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } };
  assert.equal((await createStagedSyntheticExecutor(config(local, { binding, transportOptions })).execute(input)).status, 'UNCERTAIN');
  assert.equal(state(local), 'CLAIMED');
  assert.equal((await createStagedSyntheticExecutor(config(local, { transportOptions })).execute(input)).status, 'UNCERTAIN');
  assert.equal(calls, 0); assert.equal(count(local), 1);
});
test('corrupted completed receipts cannot replay or trigger a replacement dispatch', async t => {
  const local = executionD1(); t.after(local.close); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.equal((await executor.execute(input)).status, 'COMPLETED');
  local.database.prepare('UPDATE bridge_execution_claims SET receipt_json = ?').run('{broken');
  assert.deepEqual(await executor.execute(input), { status: 'BLOCKED', code: 'RECEIPT_INTEGRITY' });
  assert.equal(calls, 1); assert.equal(state(local), 'COMPLETED');
});
test('synchronously slow pre-claim authorization cannot cancel an already-due deadline', async t => {
  const local = executionD1(); t.after(local.close); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { authorizationDeadlineMs: 15, authorizeRequest: () => { blockTurn(40); return true; }, transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.deepEqual(await executor.execute(input), { status: 'BLOCKED', code: 'AUTHORIZATION_DENIED' });
  assert.equal(count(local), 0); assert.equal(calls, 0);
});
test('synchronously slow dispatch authorization cannot outrun a queued transport timeout', async t => {
  const local = executionD1(); t.after(local.close); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { authorizationDeadlineMs: 1000, authorizeRequest: details => { if (details.phase === 'before_dispatch') blockTurn(40); return true; }, transportOptions: { apiKey: credential, timeoutMs: 15, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.deepEqual(await executor.execute(input), { status: 'UNCERTAIN', code: 'EXECUTION_UNCERTAIN' });
  assert.equal(state(local), 'UNCERTAIN'); assert.equal(calls, 0);
});
test('queued cancellation runs before dispatch after synchronous authorization work', async t => {
  const local = executionD1(); t.after(local.close); const controller = new AbortController(); let calls = 0;
  const executor = createStagedSyntheticExecutor(config(local, { authorizeRequest: details => { if (details.phase === 'before_dispatch') { setTimeout(() => controller.abort(), 0); blockTurn(20); } return true; }, transportOptions: { apiKey: credential, signal: controller.signal, fetchImpl: async () => { calls++; return response(interaction()); } } }));
  assert.deepEqual(await executor.execute(input), { status: 'UNCERTAIN', code: 'EXECUTION_UNCERTAIN' });
  assert.equal(state(local), 'UNCERTAIN'); assert.equal(calls, 0);
});
