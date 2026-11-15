import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Worker } from 'node:worker_threads';
import { D1ExecutionGate } from '../src/durable_execution_gate.mjs';
import { buildSyntheticTransportRequest } from '../src/interactions_transport.mjs';
import { createReceipt, sha256 } from '../src/synthetic_contract.mjs';
import { executionD1, executionContext as context, executionInput as input, executionResult as result } from './helpers/execution-fixtures.mjs';

test('claim is durable before a caller may attempt execution', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const first = await gate.claim(input);
  assert.equal(first.status, 'CLAIMED');
  const row = local.database.prepare('SELECT * FROM bridge_execution_claims').get();
  assert.equal(row.state, 'CLAIMED');
  assert.equal(row.owner_token, first.claim.owner_token);
  assert.equal(row.request_sha256, first.claim.request_sha256);
  assert.equal(Object.isFrozen(first.claim.request.body.generation_config), true);
  assert.equal(first.claim.request.body.store, false);
  assert.equal(first.claim.request.body.background, false);
});
test('completed duplicate returns the same verified immutable receipt', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const { claim } = await gate.claim(input);
  const saved = await gate.complete(claim, result);
  const duplicate = await gate.claim(input);
  assert.equal(duplicate.status, 'COMPLETED');
  assert.deepEqual(duplicate.receipt, saved);
  assert.equal(Object.hasOwn(duplicate, 'claim'), false);
  assert.equal(Object.hasOwn(saved, 'actual_cost_usd'), false);
  assert.equal(saved.result.billing_verified, false);
  assert.equal(local.database.prepare('SELECT count(*) AS n FROM bridge_execution_claims').get().n, 1);
});
test('same-process concurrent claims grant one ownership token', async t => {
  const local = executionD1(); t.after(local.close);
  const gates = Array.from({ length: 6 }, () => new D1ExecutionGate(local.binding, context));
  const answers = await Promise.all(gates.map(g => g.claim(input)));
  assert.equal(answers.filter(x => x.status === 'CLAIMED').length, 1);
  assert.equal(answers.filter(x => x.status === 'UNCERTAIN').length, 5);
});
test('changed payload or output schema conflicts under the existing key', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context); await gate.claim(input);
  for (const patch of [{ payload: 'SYNTHETIC:different' }, { expected_output_keys: ['changed'] }, { task_description: 'A different synthetic fixture instruction' }]) {
    await assert.rejects(gate.claim({ ...input, ...patch }), e => e.code === 'IDEMPOTENCY_CONFLICT');
  }
});
test('request fingerprint binds endpoint and actual normalized wire settings', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const { claim } = await gate.claim(input);
  const request = buildSyntheticTransportRequest(input);
  assert.equal(claim.request_sha256, await sha256({ project_id: input.project_id, provider_scope: context.providerScope, request }));
  await assert.rejects(gate.claim(input, { endpoint: 'https://generativelanguage.googleapis.com/v1beta/interactions' }), e => e.code === 'IDEMPOTENCY_CONFLICT');
});
test('caller and provider-project changes cannot reuse another operation', async t => {
  const local = executionD1(); t.after(local.close);
  await new D1ExecutionGate(local.binding, context).claim(input);
  for (const patch of [{ principal: 'synthetic-other-owner' }, { providerScope: 'synthetic-other-project' }]) {
    await assert.rejects(new D1ExecutionGate(local.binding, { ...context, ...patch }).claim(input), e => e.code === 'IDEMPOTENCY_CONFLICT');
  }
});
test('project authorization and malformed input fail before any database write', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  await assert.rejects(gate.claim({ ...input, project_id: 'JCT' }), e => e.code === 'SCOPE_DENIED');
  await assert.rejects(gate.claim({ ...input, idempotency_key: 'x' }), e => e.code === 'BAD_REQUEST');
  await assert.rejects(gate.claim({ ...input, payload: 'private' }), e => e.code === 'NOT_SYNTHETIC');
  assert.equal(local.database.prepare('SELECT count(*) AS n FROM bridge_execution_claims').get().n, 0);
});
test('wildcard and unbound server contexts are rejected', () => {
  for (const patch of [{ principal: '' }, { projects: ['*'] }, { providerScope: '' }]) {
    assert.throws(() => new D1ExecutionGate({}, { ...context, ...patch }), e => e.code === 'CONFIGURATION_REQUIRED');
  }
});
test('same key in separately authorized projects remains isolated', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, { ...context, projects: ['DEBO-CORE', 'JCT'] });
  assert.equal((await gate.claim(input)).status, 'CLAIMED');
  assert.equal((await gate.claim({ ...input, project_id: 'JCT' })).status, 'CLAIMED');
});
test('uncertain ownership can never be reclaimed or completed automatically', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const { claim } = await gate.claim(input);
  await gate.markUncertain(claim);
  assert.equal((await gate.claim(input)).status, 'UNCERTAIN');
  await assert.rejects(gate.complete(claim, result), e => e.code === 'CLAIM_NOT_ACTIVE');
});
test('old claimed rows remain blocked without lease takeover', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context); await gate.claim(input);
  local.database.exec("UPDATE bridge_execution_claims SET created_at = '2000-01-01T00:00:00.000Z'");
  assert.equal((await new D1ExecutionGate(local.binding, context).claim(input)).status, 'UNCERTAIN');
});
test('wrong token cannot complete or mutate another claim', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const { claim } = await gate.claim(input);
  const forged = { ...claim, owner_token: crypto.randomUUID() };
  await assert.rejects(gate.complete(forged, result), e => e.code === 'CLAIM_NOT_ACTIVE');
  await assert.rejects(gate.markUncertain(forged), e => e.code === 'CLAIM_NOT_ACTIVE');
  assert.equal(local.database.prepare('SELECT state FROM bridge_execution_claims').get().state, 'CLAIMED');
});
test('completion and uncertain markers cannot overwrite a completed receipt', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const { claim } = await gate.claim(input); const saved = await gate.complete(claim, result);
  assert.deepEqual(await gate.complete(claim, result), saved);
  await assert.rejects(gate.complete(claim, { ...result, output: { finding: 'CHANGED' } }), e => e.code === 'RECEIPT_CONFLICT');
  await assert.rejects(gate.markUncertain(claim), e => e.code === 'CLAIM_NOT_ACTIVE');
  assert.deepEqual((await gate.claim(input)).receipt, saved);
});
test('replay rejects corrupted receipts and recomputed invalid scope or usage', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context);
  const { claim } = await gate.claim(input); const saved = await gate.complete(claim, result);
  for (const mutate of [r => { r.project_id = 'JCT'; }, r => { r.result.usage.total_tokens = -1; }, r => { r.result.output.extra = 'injection'; }, r => { r.result.output.finding = 'changed output'; }, r => { r.result_sha256 = '0'.repeat(64); }]) {
    const changed = structuredClone(saved); mutate(changed);
    const { receipt_sha256, ...unsigned } = changed;
    changed.receipt_sha256 = await sha256(unsigned);
    local.database.prepare('UPDATE bridge_execution_claims SET receipt_json = ?').run(JSON.stringify(changed));
    await assert.rejects(gate.claim(input), e => e.code === 'RECEIPT_INTEGRITY');
  }
  local.database.prepare('UPDATE bridge_execution_claims SET receipt_json = ?').run('{broken');
  await assert.rejects(gate.claim(input), e => e.code === 'RECEIPT_INTEGRITY');
});
test('invalid result and invented zero billing claims cannot be completed', async t => {
  const local = executionD1(); t.after(local.close);
  const gate = new D1ExecutionGate(local.binding, context); const { claim } = await gate.claim(input);
  for (const patch of [{ model: 'different' }, { provider_requests: 2 }, { billing_verified: true }, { actual_cost_usd: 0 }, { usage: {} }]) {
    await assert.rejects(gate.complete(claim, { ...result, ...patch }), e => e.code === 'INVALID_EXECUTION_RESULT');
  }
});
test('storage errors are generic and failed post-result persistence stays blocked', async t => {
  const local = executionD1(); t.after(local.close);
  const good = new D1ExecutionGate(local.binding, context); const { claim } = await good.claim(input);
  const session = local.binding.withSession('first-primary');
  const binding = { withSession: () => ({ prepare(sql) { if (sql.includes("SET state = 'COMPLETED'")) throw Error('SENSITIVE_STORAGE_DETAIL'); return session.prepare(sql); } }) };
  const gate = new D1ExecutionGate(binding, context);
  await assert.rejects(gate.complete(claim, result), e => e.code === 'EXECUTION_UNCERTAIN' && !e.message.includes('SENSITIVE'));
  assert.equal((await good.claim(input)).status, 'UNCERTAIN');
});
test('uncertain update failure leaves a permanent claimed barrier', async t => {
  const local = executionD1(); t.after(local.close);
  const good = new D1ExecutionGate(local.binding, context); const { claim } = await good.claim(input);
  const session = local.binding.withSession('first-primary');
  const binding = { withSession: () => ({ prepare(sql) { if (sql.startsWith('UPDATE')) throw Error('PRIVATE'); return session.prepare(sql); } }) };
  await assert.rejects(new D1ExecutionGate(binding, context).complete(claim, result), e => e.code === 'EXECUTION_UNCERTAIN');
  assert.equal(local.database.prepare('SELECT state FROM bridge_execution_claims').get().state, 'CLAIMED');
  assert.equal((await good.claim(input)).status, 'UNCERTAIN');
});
test('lost completion acknowledgement preserves the committed receipt for replay', async t => {
  const local = executionD1(); t.after(local.close);
  const good = new D1ExecutionGate(local.binding, context); const { claim } = await good.claim(input);
  const session = local.binding.withSession('first-primary');
  const binding = { withSession: () => ({ prepare(sql) {
    const statement = session.prepare(sql);
    if (!sql.includes("SET state = 'COMPLETED'")) return statement;
    return { bind: (...values) => ({ first: async () => { await statement.bind(...values).first(); throw Error('ACKNOWLEDGEMENT_LOST'); } }) };
  } }) };
  await assert.rejects(new D1ExecutionGate(binding, context).complete(claim, result), e => e.code === 'EXECUTION_UNCERTAIN');
  const replay = await good.claim(input);
  assert.equal(replay.status, 'COMPLETED');
  assert.deepEqual(replay.receipt.result, result);
  assert.equal(local.database.prepare('SELECT state FROM bridge_execution_claims').get().state, 'COMPLETED');
});
test('stalled claim storage is bounded and does not grant ownership', async () => {
  const binding = { withSession: () => ({ prepare: () => ({ bind: () => ({ first: async () => new Promise(() => {}) }) }) }) };
  const gate = new D1ExecutionGate(binding, context, { deadlineMs: 20 });
  await assert.rejects(gate.claim(input), e => e.code === 'STORE_UNAVAILABLE');
});
test('fixture table is untouched by candidate execution storage', async t => {
  const local = executionD1(); t.after(local.close);
  const existing = await createReceipt({ project_id: 'DEBO-CORE', idempotency_key: 'untouched-fixture-key', fixture_id: 'bridge-health-v1' }, 'owner');
  const bytes = JSON.stringify(existing);
  local.database.prepare('INSERT INTO bridge_fixture_receipts VALUES (?, ?, ?, ?, ?)').run('DEBO-CORE', 'untouched-fixture-key', 'owner', existing.input_sha256, bytes);
  const gate = new D1ExecutionGate(local.binding, context); const { claim } = await gate.claim(input); await gate.complete(claim, result);
  assert.equal(local.database.prepare('SELECT receipt_json FROM bridge_fixture_receipts').get().receipt_json, bytes);
});
test('separate worker isolates and restart recover one completed receipt', async t => {
  const directory = mkdtempSync(join(tmpdir(), 'debo-execution-')); t.after(() => rmSync(directory, { recursive: true, force: true }));
  const path = join(directory, 'claims.sqlite'); const local = executionD1(path); local.close();
  const run = () => new Promise((resolve, reject) => {
    const w = new Worker(new URL('./helpers/execution-claim-worker.mjs', import.meta.url), { workerData: { path } });
    w.once('message', resolve); w.once('error', reject); w.once('exit', code => { if (code) reject(Error(`Worker failed: ${code}`)); });
  });
  const answers = await Promise.all(Array.from({ length: 6 }, run));
  assert.equal(answers.filter(x => x.won).length, 1);
  const restarted = executionD1(path, false); t.after(restarted.close);
  const replay = await new D1ExecutionGate(restarted.binding, context).claim(input);
  assert.equal(replay.status, 'COMPLETED');
  assert.equal(restarted.database.prepare('SELECT count(*) AS n FROM bridge_execution_claims').get().n, 1);
});
