// Staged transport primitive, deliberately NOT imported by either deployed
// Worker entry point. This does not establish authentication, project billing,
// durable pre-call ownership or permission to activate a provider. Its future
// caller must supply those separately reviewed server-side controls.
// No implicit global fetch: the caller must explicitly provide its transport.
import { PolicyError, validateEndpoint } from './contracts.mjs';
import { buildSyntheticInteractionRequest, parseSyntheticInteractionResult } from './interactions_mapper.mjs';

export class ProviderAttemptError extends Error {
  constructor(code, outcome) {
    super(`Synthetic provider transport failed (${code}); automatic retry is disabled`);
    this.name = 'ProviderAttemptError';
    this.code = code;
    this.outcome = outcome;
  }
}
const fail = code => { throw new PolicyError(code, 'Synthetic transport request rejected'); };
const boundedInteger = (n, min, max) => Number.isSafeInteger(n) && n >= min && n <= max;

async function boundedResponseJson(response, signal, maxBytes) {
  if (!/^application\/json(?:\s*;|$)/i.test(response.headers.get('content-type') ?? '') || !response.body) {
    void response.body?.cancel().catch(() => {});
    fail('PROVIDER_INVALID_RESPONSE');
  }
  const reader = response.body.getReader();
  const cancel = () => { void reader.cancel().catch(() => {}); };
  signal.addEventListener('abort', cancel, { once: true });
  const chunks = [];
  let length = 0;
  try {
    for (;;) {
      if (signal.aborted) fail('REQUEST_CANCELLED');
      const { value, done } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > maxBytes) fail('PROVIDER_RESPONSE_LIMIT');
      chunks.push(value);
    }
    const bytes = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
    catch { fail('PROVIDER_INVALID_RESPONSE'); }
  } finally {
    signal.removeEventListener('abort', cancel);
    cancel();
  }
}

function reportedUsage(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail('PROVIDER_INVALID_USAGE');
  const result = {};
  for (const k of ['total_input_tokens', 'total_output_tokens', 'total_tokens']) {
    if (!boundedInteger(value[k], 0, 1_000_000)) fail('PROVIDER_INVALID_USAGE');
    result[k] = value[k];
  }
  if (result.total_output_tokens > 1024 || result.total_tokens < result.total_input_tokens + result.total_output_tokens || (value.total_tool_use_tokens ?? 0) !== 0) fail('PROVIDER_INVALID_USAGE');
  if (value.total_thought_tokens !== undefined) {
    if (!boundedInteger(value.total_thought_tokens, 0, result.total_tokens)) fail('PROVIDER_INVALID_USAGE');
    result.total_thought_tokens = value.total_thought_tokens;
  }
  return result;
}

export async function postSyntheticInteraction(rawInput, options = {}) {
  let endpoint, body, expectedKeys, fetchImpl, apiKey, timeoutMs, maxResponseBytes, signal;
  try {
    if (!options || typeof options !== 'object' || Array.isArray(options)) fail('TRANSPORT_UNCONFIGURED');
    ({ fetchImpl, apiKey, timeoutMs = 15_000, maxResponseBytes = 65_536, signal } = options);
    if (typeof fetchImpl !== 'function') fail('TRANSPORT_UNCONFIGURED');
    endpoint = validateEndpoint(options.endpoint ?? 'https://generativelanguage.googleapis.com/v1/interactions').href;
    if (typeof apiKey !== 'string' || !/^[!-~]{16,512}$/.test(apiKey)) fail('CREDENTIAL_REQUIRED');
    if (!boundedInteger(timeoutMs, 10, 30_000) || !boundedInteger(maxResponseBytes, 1024, 131_072)) fail('TRANSPORT_LIMITS_INVALID');
    if (signal !== undefined && !(signal instanceof AbortSignal)) fail('TRANSPORT_LIMITS_INVALID');
    if (signal?.aborted) fail('REQUEST_CANCELLED');
    body = buildSyntheticInteractionRequest(rawInput, options.model);
    expectedKeys = [...body.response_format.schema.required];
    body.stream = false;
    body.service_tier = 'standard';
    body.generation_config = { max_output_tokens: 1024, tool_choice: 'none' };
  } catch (error) {
    throw new ProviderAttemptError(error instanceof PolicyError ? error.code : 'TRANSPORT_UNCONFIGURED', 'not_started');
  }

  const controller = new AbortController();
  const cancel = () => controller.abort();
  signal?.addEventListener('abort', cancel, { once: true });
  let timer, timedOut = false, attempted = false;
  const deadline = new Promise((_, reject) => {
    controller.signal.addEventListener('abort', () => reject(new PolicyError(timedOut ? 'PROVIDER_TIMEOUT' : 'REQUEST_CANCELLED', 'Request stopped')), { once: true });
    timer = setTimeout(() => { timedOut = true; controller.abort(); }, timeoutMs);
  });
  try {
    const operation = (async () => {
      if (signal?.aborted) { controller.abort(); fail('REQUEST_CANCELLED'); }
      attempted = true;
      const response = await fetchImpl(endpoint, {
        method: 'POST', redirect: 'error', credentials: 'omit', cache: 'no-store',
        signal: controller.signal,
        headers: { 'content-type': 'application/json', 'x-goog-api-key': apiKey, 'Api-Revision': '2026-05-20' },
        body: JSON.stringify(body)
      });
      if (!(response instanceof Response)) fail('PROVIDER_INVALID_RESPONSE');
      if (!response.ok) {
        void response.body?.cancel().catch(() => {});
        fail(`PROVIDER_HTTP_${response.status}`);
      }
      if (response.redirected || (response.url && response.url !== endpoint)) {
        void response.body?.cancel().catch(() => {});
        fail('PROVIDER_INVALID_RESPONSE');
      }
      const interaction = await boundedResponseJson(response, controller.signal, maxResponseBytes);
      if (!interaction || typeof interaction !== 'object' || Array.isArray(interaction) || interaction.status !== 'completed' || typeof interaction.id !== 'string' || !/^[A-Za-z0-9_.:-]{1,256}$/.test(interaction.id) || (interaction.model !== undefined && interaction.model !== body.model) || (interaction.errors !== undefined && (!Array.isArray(interaction.errors) || interaction.errors.length))) fail('PROVIDER_INVALID_RESPONSE');
      if (!Array.isArray(interaction.steps) || interaction.steps.some(step => !step || !['user_input', 'model_output'].includes(step.type))) fail('PROVIDER_INVALID_RESPONSE');
      const output = parseSyntheticInteractionResult(interaction, expectedKeys);
      return { interaction_id: interaction.id, model: body.model, output, usage: reportedUsage(interaction.usage), provider_requests: 1, billing_verified: false };
    })();
    return await Promise.race([operation, deadline]);
  } catch (error) {
    const code = error instanceof PolicyError ? error.code : 'PROVIDER_NETWORK_ERROR';
    throw new ProviderAttemptError(code, attempted ? 'unknown' : 'not_started');
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener('abort', cancel);
    controller.abort();
  }
}
