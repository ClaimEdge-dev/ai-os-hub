import { test } from 'node:test';
import assert from 'node:assert/strict';
import { postSyntheticInteraction } from '../src/interactions_transport.mjs';

const input = { project_id: 'DEBO-CORE', task_type: 'test_fixture_analysis', task_description: 'Check synthetic bridge fixture and return finding', approved_sources: ['fixtures/health.json'], payload: 'SYNTHETIC:{"case":"health"}', idempotency_key: 'transport-fixture-v1', privacy_classification: 'PUBLIC', mode: 'read_only', cost_ceiling_usd: 0, expected_output_keys: ['finding'] };
const key = 'SYNTHETIC_TEST_CREDENTIAL_NOT_REAL';
const interaction = () => ({ id: 'synthetic-interaction-1', status: 'completed', model: 'gemini-3.8-flash', steps: [{ type: 'model_output', content: [{ type: 'text', text: '{"finding":"PASS"}' }] }], usage: { total_input_tokens: 20, total_output_tokens: 5, total_tokens: 25, total_tool_use_tokens: 0 } });
const response = value => new Response(JSON.stringify(value), { headers: { 'content-type': 'application/json' } });
const options = overrides => ({ apiKey: key, fetchImpl: async () => response(interaction()), ...overrides });
// One occupied local JS turn exposes a due timer being overtaken by promise
// continuations. This does not model deployed Worker CPU-time accounting.
const blockTurn = ms => { const end = performance.now() + ms; while (performance.now() < end) {} };

test('candidate transport requires an explicitly supplied HTTP implementation', async () => {
  await assert.rejects(postSyntheticInteraction(input, { apiKey: key }), e => e.code === 'TRANSPORT_UNCONFIGURED' && e.outcome === 'not_started');
});
test('invalid routes, models, input and keys fail before dispatch', async () => {
  let calls = 0;
  const fetchImpl = async () => { calls++; return response(interaction()); };
  for (const extra of [{ endpoint: 'https://example.com/v1/interactions' }, { endpoint: 'https://generativelanguage.googleapis.com/v1/interactions?key=test' }, { model: 'unapproved' }, { apiKey: '' }, { apiKey: 'invalid\ncredential' }, { timeoutMs: 0 }, { maxResponseBytes: 10000000 }]) {
    await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl, ...extra })), e => e.outcome === 'not_started');
  }
  await assert.rejects(postSyntheticInteraction({ ...input, payload: 'private input' }, options({ fetchImpl })), e => e.code === 'NOT_SYNTHETIC');
  assert.equal(calls, 0);
});
test('uses one bounded stateless POST with credentials in the header only', async () => {
  let calls = 0;
  const result = await postSyntheticInteraction(input, options({ fetchImpl: async (url, init) => {
    calls++;
    assert.equal(url, 'https://generativelanguage.googleapis.com/v1/interactions');
    assert.equal(init.method, 'POST');
    assert.equal(init.redirect, 'error');
    assert.equal(init.credentials, 'omit');
    assert.equal(init.headers['x-goog-api-key'], key);
    assert.equal(init.headers['Api-Revision'], '2026-05-20');
    assert.equal(init.body.includes(key), false);
    const body = JSON.parse(init.body);
    assert.equal(body.store, false);
    assert.equal(body.background, false);
    assert.equal(body.stream, false);
    assert.equal(body.service_tier, 'standard');
    assert.equal(body.generation_config.max_output_tokens, 1024);
    assert.equal(body.generation_config.tool_choice, 'none');
    assert.equal(Object.hasOwn(body, 'tools'), false);
    return response(interaction());
  } }));
  assert.equal(calls, 1);
  assert.deepEqual(result.output, { finding: 'PASS' });
  assert.equal(result.provider_requests, 1);
  assert.equal(result.billing_verified, false);
  assert.equal(Object.hasOwn(result, 'actual_cost_usd'), false);
  assert.equal(JSON.stringify(result).includes(key), false);
});
test('allows the existing v1beta route without enabling redirects', async () => {
  await postSyntheticInteraction(input, options({ endpoint: 'https://generativelanguage.googleapis.com/v1beta/interactions', fetchImpl: async (url, init) => {
    assert.equal(new URL(url).pathname, '/v1beta/interactions'); assert.equal(init.redirect, 'error'); return response(interaction());
  } }));
});
for (const status of [401, 403, 429, 500]) test(`HTTP ${status} is redacted and never automatically retried`, async () => {
  let calls = 0;
  await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => { calls++; return new Response(key, { status }); } })), e => e.code === `PROVIDER_HTTP_${status}` && e.outcome === 'unknown' && !e.message.includes(key));
  assert.equal(calls, 1);
});
test('network and redirect failures do not expose exception text or retry', async () => {
  let calls = 0;
  await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => { calls++; throw Error(key); } })), e => e.code === 'PROVIDER_NETWORK_ERROR' && e.outcome === 'unknown' && !e.message.includes(key));
  assert.equal(calls, 1);
});
test('rejects non-JSON and malformed response bodies', async () => {
  for (const r of [new Response(key, { headers: { 'content-type': 'text/html' } }), new Response('{broken', { headers: { 'content-type': 'application/json' } })]) {
    await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => r })), e => e.code === 'PROVIDER_INVALID_RESPONSE' && !e.message.includes(key));
  }
});
test('cancels an unread non-JSON response stream', async () => {
  let cancelled = false;
  const body = new ReadableStream({ start() {}, cancel() { cancelled = true; } });
  await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => new Response(body, { headers: { 'content-type': 'text/html' } }) })), e => e.code === 'PROVIDER_INVALID_RESPONSE');
  assert.equal(cancelled, true);
});
test('captures the output contract before asynchronous dispatch', async () => {
  const localInput = { ...input, expected_output_keys: ['finding'] };
  const result = await postSyntheticInteraction(localInput, options({ fetchImpl: async () => {
    localInput.expected_output_keys[0] = 'changed_after_dispatch';
    return response(interaction());
  } }));
  assert.deepEqual(result.output, { finding: 'PASS' });
});
test('enforces response bytes while streaming', async () => {
  let cancelled = false;
  const body = new ReadableStream({ pull(c) { c.enqueue(new Uint8Array(1100)); }, cancel() { cancelled = true; } });
  await assert.rejects(postSyntheticInteraction(input, options({ maxResponseBytes: 1024, fetchImpl: async () => new Response(body, { headers: { 'content-type': 'application/json' } }) })), e => e.code === 'PROVIDER_RESPONSE_LIMIT');
  assert.equal(cancelled, true);
});
test('deadline bounds a fetch that ignores AbortSignal', async () => {
  await assert.rejects(postSyntheticInteraction(input, options({ timeoutMs: 20, fetchImpl: async () => new Promise(() => {}) })), e => e.code === 'PROVIDER_TIMEOUT' && e.outcome === 'unknown');
});
test('deadline includes a stalled response body', async () => {
  let cancelled = false;
  const body = new ReadableStream({ start() {}, cancel() { cancelled = true; } });
  await assert.rejects(postSyntheticInteraction(input, options({ timeoutMs: 20, fetchImpl: async () => new Response(body, { headers: { 'content-type': 'application/json' } }) })), e => e.code === 'PROVIDER_TIMEOUT');
  assert.equal(cancelled, true);
});
test('already-cancelled requests do not dispatch', async () => {
  const controller = new AbortController(); controller.abort();
  let calls = 0;
  await assert.rejects(postSyntheticInteraction(input, options({ signal: controller.signal, fetchImpl: async () => { calls++; return response(interaction()); } })), e => e.code === 'REQUEST_CANCELLED' && e.outcome === 'not_started');
  assert.equal(calls, 0);
});
test('cancellation after dispatch records an uncertain outcome', async () => {
  const controller = new AbortController();
  await assert.rejects(postSyntheticInteraction(input, options({ signal: controller.signal, fetchImpl: async () => { controller.abort(); return new Promise(() => {}); } })), e => e.code === 'REQUEST_CANCELLED' && e.outcome === 'unknown');
});
test('requires explicit completion, interaction identity and the requested model', async () => {
  for (const patch of [{ status: undefined }, { status: 'incomplete' }, { id: '' }, { model: 'different-model' }, { errors: [{ message: key }] }]) {
    await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => response({ ...interaction(), ...patch }) })), e => e.code === 'PROVIDER_INVALID_RESPONSE' && !e.message.includes(key));
  }
});
test('rejects tool steps and invalid structured output', async () => {
  for (const patch of [{ steps: [{ type: 'function_call' }] }, { output_text: '{"finding":42}' }, { output_text: '{"finding":"PASS","extra":"x"}' }]) {
    await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => response({ ...interaction(), ...patch }) })), e => e.outcome === 'unknown');
  }
});
test('requires bounded reported token usage without guessing dollar cost', async () => {
  for (const usage of [undefined, { total_input_tokens: -1, total_output_tokens: 1, total_tokens: 0 }, { total_input_tokens: 1, total_output_tokens: 1025, total_tokens: 1026 }, { total_input_tokens: 1, total_output_tokens: 1, total_tokens: '2' }, { total_input_tokens: 1, total_output_tokens: 1, total_tokens: 2, total_tool_use_tokens: 1 }]) {
    await assert.rejects(postSyntheticInteraction(input, options({ fetchImpl: async () => response({ ...interaction(), usage }) })), e => e.code === 'PROVIDER_INVALID_USAGE');
  }
});

test('synchronously slow fetch cannot clear an already-due transport deadline', async () => {
  let calls = 0;
  await assert.rejects(postSyntheticInteraction(input, options({ timeoutMs: 15, fetchImpl: async () => {
    calls++; blockTurn(40); return response(interaction());
  } })), e => e.code === 'PROVIDER_TIMEOUT' && e.outcome === 'unknown');
  assert.equal(calls, 1);
});
test('synchronously slow response reading cannot clear an already-due transport deadline', async () => {
  let calls = 0;
  await assert.rejects(postSyntheticInteraction(input, options({ timeoutMs: 15, fetchImpl: async () => {
    calls++;
    const body = new ReadableStream({ pull(controller) {
      blockTurn(40);
      controller.enqueue(new TextEncoder().encode(JSON.stringify(interaction())));
      controller.close();
    } });
    return new Response(body, { headers: { 'content-type': 'application/json' } });
  } })), e => e.code === 'PROVIDER_TIMEOUT' && e.outcome === 'unknown');
  assert.equal(calls, 1);
});
test('queued cancellation after a blocking fetch is honored before transport success', async () => {
  const controller = new AbortController(); let calls = 0;
  await assert.rejects(postSyntheticInteraction(input, options({ signal: controller.signal, fetchImpl: async () => {
    calls++; setTimeout(() => controller.abort(), 0); blockTurn(20); return response(interaction());
  } })), e => e.code === 'REQUEST_CANCELLED' && e.outcome === 'unknown');
  assert.equal(calls, 1);
});
