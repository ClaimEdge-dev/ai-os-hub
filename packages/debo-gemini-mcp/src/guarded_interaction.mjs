// Staged server-internal orchestration. NOT imported by the deployed Workers.
// The authorization dependency must verify actual identity, project, credential,
// billing eligibility and release authority. This module cannot establish those
// facts. An enable flag or a test callback is NOT proof of free API access.
import { PolicyError } from './contracts.mjs';
import { canonicalJson, sha256 } from './synthetic_contract.mjs';
import { D1ExecutionGate } from './durable_execution_gate.mjs';
import { createNoRetryAttemptObserver } from './no_retry_attempt_observer.mjs';
import { buildSyntheticTransportRequest, postSyntheticInteraction } from './interactions_transport.mjs';

const freeze = value => { if (value && typeof value === 'object') { Object.values(value).forEach(freeze); Object.freeze(value); } return value; };
const blocked = code => ({ status: 'BLOCKED', code });
const uncertain = () => ({ status: 'UNCERTAIN', code: 'EXECUTION_UNCERTAIN' });
const integer = (n, min, max) => Number.isSafeInteger(n) && n >= min && n <= max;
const rejectConfiguration = () => { throw new PolicyError('CONFIGURATION_REQUIRED', 'Staged executor requires reviewed server-side dependencies'); };
const inputFields = new Set(['project_id', 'task_type', 'task_description', 'approved_sources', 'payload', 'idempotency_key', 'privacy_classification', 'mode', 'cost_ceiling_usd', 'expected_output_keys']);
const transportFields = new Set(['endpoint', 'model', 'apiKey', 'fetchImpl', 'timeoutMs', 'maxResponseBytes', 'signal']);

export function createStagedSyntheticExecutor(configuration = {}) {
  if (configuration?.enabled !== true) return Object.freeze({ execute: async () => blocked('PROVIDER_DISABLED') });
  const { binding, authorizeRequest, authorizationDeadlineMs = 1500, recordAttemptEvidence } = configuration;
  const supplied = configuration.transportOptions;
  if (typeof authorizeRequest !== 'function' || !supplied || typeof supplied !== 'object' || Array.isArray(supplied) || Object.keys(supplied).some(k => !transportFields.has(k)) || !integer(authorizationDeadlineMs, 10, 30_000) || (recordAttemptEvidence !== undefined && typeof recordAttemptEvidence !== 'function')) rejectConfiguration();
  const options = Object.freeze({ timeoutMs: 15_000, maxResponseBytes: 65_536, ...supplied });
  if (typeof options.fetchImpl !== 'function' || typeof options.apiKey !== 'string' || !/^[!-~]{16,512}$/.test(options.apiKey) || !integer(options.timeoutMs, 10, 30_000) || !integer(options.maxResponseBytes, 1024, 131_072) || (options.signal !== undefined && !(options.signal instanceof AbortSignal))) rejectConfiguration();
  let context;
  try { context = freeze(structuredClone(configuration.context)); } catch { rejectConfiguration(); }
  // Acquires a session handle only; no statement executes before authorization.
  const gate = new D1ExecutionGate(binding, context, configuration.storageOptions);

  async function authorized(details, signal) {
    if (signal?.aborted) return false;
    let timer, cancel, expired = false;
    try {
      const stopped = new Promise(resolve => {
        timer = setTimeout(() => { expired = true; resolve(false); }, authorizationDeadlineMs);
        cancel = () => resolve(false);
        signal?.addEventListener('abort', cancel, { once: true });
      });
      const decision = await Promise.race([Promise.resolve().then(() => authorizeRequest(details)), stopped]);
      if (decision !== true) return false;
      // A synchronous callback or promise chain can finish before an already-due
      // timer gets a turn. Keep the deadline armed while yielding to timer work,
      // then honor expiry/cancellation before claiming or invoking HTTP.
      // Worker clocks do not measure CPU time; do not replace this with Date.now.
      await new Promise(resolve => setTimeout(resolve, 0));
      return !expired && !signal?.aborted;
    } catch { return false; }
    finally { clearTimeout(timer); signal?.removeEventListener('abort', cancel); }
  }

  // Diagnostics are strictly best effort. They cannot control authorization,
  // persistence, transport, replay, or result shape. The observation contains
  // no credential, raw source, owner token, project ID, or receipt.
  function recordObservation(trace) {
    if (typeof recordAttemptEvidence !== 'function') return;
    try {
      const result = recordAttemptEvidence(trace.observeFailure());
      if (result && typeof result.then === 'function') void Promise.resolve(result).catch(() => {});
    } catch { /* Diagnostic failures must not change durable barriers. */ }
  }

  return Object.freeze({
    async execute(rawInput) {
      let input, request, details;
      try {
        if (!rawInput || typeof rawInput !== 'object' || Array.isArray(rawInput) || Object.keys(rawInput).some(k => !inputFields.has(k)) || options.signal?.aborted) throw Error();
        input = freeze(structuredClone(rawInput));
        request = freeze(buildSyntheticTransportRequest(input, options));
        if (!context.projects.includes(input.project_id)) throw Error();
        details = freeze({ principal: context.principal, project_id: input.project_id, idempotency_key: input.idempotency_key, provider_scope: context.providerScope, request, request_sha256: await sha256({ project_id: input.project_id, provider_scope: context.providerScope, request }) });
      } catch { return blocked('REQUEST_REJECTED'); }

      if (!await authorized(freeze({ ...details, phase: 'before_claim' }), options.signal)) return blocked('AUTHORIZATION_DENIED');
      const trace = createNoRetryAttemptObserver();
      let acquired;
      try { acquired = await gate.claim(input, options); }
      catch (error) {
        if (error instanceof PolicyError && ['IDEMPOTENCY_CONFLICT', 'RECEIPT_INTEGRITY'].includes(error.code)) return blocked(error.code);
        // A timed-out insert might have committed. Never dispatch without proof.
        trace.observeClaimUnknown();
        recordObservation(trace);
        return uncertain();
      }
      if (acquired.status === 'COMPLETED') return { status: 'COMPLETED', replayed: true, receipt: acquired.receipt };
      if (acquired.status !== 'CLAIMED') {
        trace.observeClaimUnknown();
        recordObservation(trace);
        return uncertain();
      }
      trace.observeClaimAcknowledged();
      const { claim } = acquired;
      let invoked = false;
      try {
        const fetchClaimed = async (url, init) => {
          if (invoked) throw Error('Claim dispatch already attempted');
          invoked = true;
          const saved = claim.request;
          if (claim.request_sha256 !== details.request_sha256 || url !== saved.endpoint || init.method !== 'POST' || init.redirect !== 'error' || init.credentials !== 'omit' || init.cache !== 'no-store' || Object.keys(init.headers).length !== 3 || init.headers['content-type'] !== 'application/json' || init.headers['Api-Revision'] !== saved.api_revision || init.headers['x-goog-api-key'] !== options.apiKey || canonicalJson(JSON.parse(init.body)) !== canonicalJson(saved.body) || !(init.signal instanceof AbortSignal)) throw Error('Claim dispatch mismatch');
          if (!await authorized(freeze({ ...details, phase: 'before_dispatch' }), init.signal) || init.signal.aborted) throw Error('Dispatch authorization unavailable');
          // The deadline can fire during authorization. Recheck cancellation
          // before the only call to the explicitly injected HTTP dependency.
          trace.observeProviderEntry();
          return options.fetchImpl(url, init);
        };
        const result = await postSyntheticInteraction(input, { ...options, fetchImpl: fetchClaimed });
        const receipt = await gate.complete(claim, result);
        return { status: 'COMPLETED', replayed: false, receipt };
      } catch {
        try { await gate.markUncertain(claim); } catch { /* CLAIMED or COMPLETED still blocks redispatch. */ }
        recordObservation(trace);
        return uncertain();
      }
    }
  });
}
