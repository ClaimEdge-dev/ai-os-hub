// Staged transport primitive, deliberately NOT imported by either deployed
// Worker entry point. This does not establish authentication, project billing,
// durable pre-call ownership or permission to activate a provider. Its future
// caller must supply those separately reviewed server-side controls.
// No implicit global fetch: the caller must explicitly provide its transport.
import { PolicyError, validateEndpoint, parseUnambiguousJson } from './contracts.mjs';
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
    // Check the entire envelope before duplicate keys can discard status,
    // tool steps or usage evidence. Retain the stream byte bound and the
    // shared parser's 48,000-character, Unicode and nesting restrictions.
    try { return parseUnambiguousJson(new TextDecoder('utf-8', { fatal: true }).decode(bytes), { maxChars: 48000 }); }
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

// The ledger and transport must fingerprint/dispatch the same normalized wire
// settings, including the output schema and controls, not just the input text.
export function buildSyntheticTransportRequest(rawInput, options = {}) {
  const endpoint = validateEndpoint(options.endpoint ?? 'https://generativelanguage.googleapis.com/v1/interactions').href;
  const body = buildSyntheticInteractionRequest(rawInput, options.model);
  body.stream = false;
  body.service_tier = 'standard';
  body.generation_config = { max_output_tokens: 1024, tool_choice: 'none' };
  return { endpoint, api_revision: '2026-05-20', body };
}

export function validateSyntheticTransportResult(value, request) {
  const fields = ['interaction_id', 'model', 'output', 'usage', 'provider_requests', 'billing_verified'];
  try {
    if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).length !== fields.length || fields.some(k => !Object.hasOwn(value, k)) || typeof value.interaction_id !== 'string' || !/^[A-Za-z0-9_.:-]{1,256}$/.test(value.interaction_id) || value.model !== request.body.model || value.provider_requests !== 1 || value.billing_verified !== false) fail('INVALID_EXECUTION_RESULT');
    if (!value.usage || Object.keys(value.usage).some(k => !['total_input_tokens', 'total_output_tokens', 'total_tokens', 'total_thought_tokens'].includes(k))) fail('INVALID_EXECUTION_RESULT');
    const output = parseSyntheticInteractionResult({ status: 'completed', output_text: JSON.stringify(value.output) }, request.body.response_format.schema.required);
    return { interaction_id: value.interaction_id, model: value.model, output, usage: reportedUsage(value.usage), provider_requests: 1, billing_verified: false };
  } catch { fail('INVALID_EXECUTION_RESULT'); }
}

export async function postSyntheticInteraction(rawInput, options = {}) {
  let request, endpoint, body, expectedKeys, fetchImpl, apiKey, timeoutMs, maxResponseBytes, signal;
  try {
    if (!options || typeof options !== 'object' || Array.isArray(options)) fail('TRANSPORT_UNCONFIGURED');
    ({ fetchImpl, apiKey, timeoutMs = 15_000, maxResponseBytes = 65_536, signal } = options);
    if (typeof fetchImpl !== 'function') fail('TRANSPORT_UNCONFIGURED');
    if (typeof apiKey !== 'string' || !/^[!-~]{16,512}$/.test(apiKey)) fail('CREDENTIAL_REQUIRED');
    if (!boundedInteger(timeoutMs, 10, 30_000) || !boundedInteger(maxResponseBytes, 1024, 131_072)) fail('TRANSPORT_LIMITS_INVALID');
    if (signal !== undefined && !(signal instanceof AbortSignal)) fail('TRANSPORT_LIMITS_INVALID');
    if (signal?.aborted) fail('REQUEST_CANCELLED');
    request = buildSyntheticTransportRequest(rawInput, options);
    ({ endpoint, body } = request);
    expectedKeys = [...body.response_format.schema.required];
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
        headers: { 'content-type': 'application/json', 'x-goog-api-key': apiKey, 'Api-Revision': request.api_revision },
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
      return validateSyntheticTransportResult({ interaction_id: interaction.id, model: body.model, output, usage: reportedUsage(interaction.usage), provider_requests: 1, billing_verified: false }, request);
    })();
    const result = await Promise.race([operation, deadline]);
    // A fulfilled fetch/body promise can outrun a due timer after synchronous
    // work. Keep the deadline/cancellation listeners armed through a timer
    // turn before accepting success. This is not Worker CPU-time accounting.
    await new Promise(resolve => setTimeout(resolve, 0));
    if (controller.signal.aborted) fail(timedOut ? 'PROVIDER_TIMEOUT' : 'REQUEST_CANCELLED');
    return result;
  } catch (error) {
    const code = error instanceof PolicyError ? error.code : 'PROVIDER_NETWORK_ERROR';
    throw new ProviderAttemptError(code, attempted ? 'unknown' : 'not_started');
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener('abort', cancel);
    controller.abort();
  }
}
