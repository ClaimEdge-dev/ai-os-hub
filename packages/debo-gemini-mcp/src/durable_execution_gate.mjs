// Staged storage component: NO provider call, implicit executor, billing verifier
// or MCP route. Its future server caller must authenticate the actual Sites
// principal, authorize the project and independently verify billing eligibility.
// Context/ownership handles are server-internal, never tool arguments/results.
import { PolicyError } from './contracts.mjs';
import { KEY_PATTERN, PROJECT_PATTERN, canonicalJson, sha256 } from './synthetic_contract.mjs';
import { buildSyntheticTransportRequest, validateSyntheticTransportResult } from './interactions_transport.mjs';
import { parseUnambiguousJson } from './strict_output_json.mjs';

const fail = (code, message = 'Candidate execution request rejected') => { throw new PolicyError(code, message); };
const uuid = /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/;
const iso = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value) && Number.isFinite(Date.parse(value));
const freeze = value => { if (value && typeof value === 'object') { Object.values(value).forEach(freeze); Object.freeze(value); } return value; };
// SQLite length(text) counts characters, not UTF-8 bytes. Bound serialized
// storage envelopes explicitly before writing and again when reading.
const utf8Bytes = text => new TextEncoder().encode(text).byteLength;

export class D1ExecutionGate {
  #session;
  #context;
  #deadlineMs;
  constructor(binding, context, { deadlineMs = 1500 } = {}) {
    if (!context || typeof context.principal !== 'string' || !context.principal.length || context.principal.length > 256 || /[\x00-\x1f\x7f]/.test(context.principal) || !Array.isArray(context.projects) || !context.projects.length || context.projects.length > 14 || context.projects.some(p => typeof p !== 'string' || !new RegExp(PROJECT_PATTERN).test(p)) || typeof context.providerScope !== 'string' || !/^[A-Za-z0-9._:-]{8,128}$/.test(context.providerScope) || !Number.isSafeInteger(deadlineMs) || deadlineMs < 10 || deadlineMs > 30_000) fail('CONFIGURATION_REQUIRED');
    this.#context = freeze(structuredClone(context));
    this.#deadlineMs = deadlineMs;
    try { this.#session = binding.withSession('first-primary'); }
    catch { fail('STORE_UNAVAILABLE', 'Candidate execution storage is unavailable'); }
  }
  async #query(sql, values) {
    let timer;
    try {
      return await Promise.race([
        this.#session.prepare(sql).bind(...values).first(),
        new Promise((_, reject) => { timer = setTimeout(() => reject(Error('deadline')), this.#deadlineMs); })
      ]);
    } catch { fail('STORE_UNAVAILABLE', 'Candidate storage request failed; do not dispatch or retry a provider'); }
    finally { clearTimeout(timer); }
  }
  #scope(project, key) {
    if (typeof project !== 'string' || !new RegExp(PROJECT_PATTERN).test(project) || typeof key !== 'string' || !new RegExp(KEY_PATTERN).test(key)) fail('BAD_REQUEST');
    if (!this.#context.projects.includes(project)) fail('SCOPE_DENIED');
  }
  async #operation(project, key, request) {
    this.#scope(project, key);
    const copied = structuredClone(request);
    if (utf8Bytes(canonicalJson(copied)) > 48_000) fail('BAD_REQUEST');
    return { project_id: project, idempotency_key: key, request: freeze(copied), request_sha256: await sha256({ project_id: project, provider_scope: this.#context.providerScope, request: copied }) };
  }
  #read(op) {
    return this.#query('SELECT * FROM bridge_execution_claims WHERE project_id = ?1 AND idempotency_key = ?2', [op.project_id, op.idempotency_key]);
  }
  #checkRow(row, op) {
    if (!row) fail('STORE_UNAVAILABLE', 'Candidate claim could not be read back');
    if (row.owner_id !== this.#context.principal || row.provider_scope !== this.#context.providerScope || row.request_sha256 !== op.request_sha256) fail('IDEMPOTENCY_CONFLICT');
    let request;
    try { if (typeof row.request_json !== 'string' || utf8Bytes(row.request_json) > 48_000) throw Error(); request = parseUnambiguousJson(row.request_json, { maxChars: 48_000 }); }
    catch { fail('RECEIPT_INTEGRITY'); }
    if (row.project_id !== op.project_id || row.idempotency_key !== op.idempotency_key || canonicalJson(request) !== canonicalJson(op.request) || !uuid.test(row.owner_token) || !['CLAIMED', 'COMPLETED', 'UNCERTAIN'].includes(row.state) || !iso(row.created_at) || !iso(row.updated_at) || (row.state === 'COMPLETED' ? typeof row.receipt_json !== 'string' : row.receipt_json !== null)) fail('RECEIPT_INTEGRITY');
    return row;
  }
  async #receipt(row, op) {
    try {
      if (utf8Bytes(row.receipt_json) > 48_000) throw Error();
      const receipt = parseUnambiguousJson(row.receipt_json, { maxChars: 48_000 });
      const fields = ['schema', 'receipt_id', 'project_id', 'idempotency_key', 'caller_sha256', 'provider_scope', 'request_sha256', 'result', 'result_sha256', 'completed_at', 'receipt_sha256'];
      if (!receipt || Array.isArray(receipt) || Object.keys(receipt).length !== fields.length || fields.some(k => !Object.hasOwn(receipt, k)) || receipt.schema !== 'debo.gemini.transport_receipt.v1' || typeof receipt.receipt_id !== 'string' || !receipt.receipt_id.startsWith('TRANSPORT-') || !uuid.test(receipt.receipt_id.slice(10)) || receipt.project_id !== op.project_id || receipt.idempotency_key !== op.idempotency_key || receipt.caller_sha256 !== await sha256(this.#context.principal) || receipt.provider_scope !== this.#context.providerScope || receipt.request_sha256 !== op.request_sha256 || !iso(receipt.completed_at) || receipt.completed_at !== row.updated_at) throw Error();
      const result = validateSyntheticTransportResult(receipt.result, op.request);
      const { receipt_sha256, ...unsigned } = receipt;
      if (canonicalJson(result) !== canonicalJson(receipt.result) || receipt.result_sha256 !== await sha256(result) || receipt_sha256 !== await sha256(unsigned)) throw Error();
      return receipt;
    } catch { fail('RECEIPT_INTEGRITY', 'Stored candidate receipt failed validation'); }
  }
  async #handle(claim) {
    if (!claim || Object.keys(claim).length !== 5 || !uuid.test(claim.owner_token ?? '')) fail('CLAIM_NOT_ACTIVE');
    const op = await this.#operation(claim.project_id, claim.idempotency_key, claim.request);
    if (claim.request_sha256 !== op.request_sha256) fail('CLAIM_NOT_ACTIVE');
    const row = this.#checkRow(await this.#read(op), op);
    if (row.owner_token !== claim.owner_token) fail('CLAIM_NOT_ACTIVE');
    return { op, row };
  }
  async claim(rawInput, transportOptions = {}) {
    this.#scope(rawInput?.project_id, rawInput?.idempotency_key);
    const op = await this.#operation(rawInput.project_id, rawInput.idempotency_key, buildSyntheticTransportRequest(rawInput, transportOptions));
    const token = crypto.randomUUID();
    const now = new Date().toISOString();
    const inserted = await this.#query(
      "INSERT INTO bridge_execution_claims (project_id, idempotency_key, owner_id, provider_scope, request_sha256, request_json, owner_token, state, receipt_json, created_at, updated_at) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, 'CLAIMED', NULL, ?8, ?8) ON CONFLICT(project_id, idempotency_key) DO NOTHING RETURNING owner_token",
      [op.project_id, op.idempotency_key, this.#context.principal, this.#context.providerScope, op.request_sha256, canonicalJson(op.request), token, now]
    );
    const row = this.#checkRow(await this.#read(op), op);
    if (inserted !== null) {
      if (inserted?.owner_token !== token || row.owner_token !== token || row.state !== 'CLAIMED') fail('STORE_UNAVAILABLE');
      return { status: 'CLAIMED', replayed: false, claim: freeze({ ...op, owner_token: token }) };
    }
    if (row.state === 'COMPLETED') return { status: 'COMPLETED', replayed: true, receipt: await this.#receipt(row, op) };
    // A crash, elapsed time or an uncertain write never grants a new token.
    // There is intentionally no automatic lease-expiry/reclaim path.
    return { status: 'UNCERTAIN', replayed: false };
  }
  async complete(claim, rawResult) {
    try {
      const { op, row } = await this.#handle(claim);
      const result = validateSyntheticTransportResult(rawResult, op.request);
      if (row.state === 'COMPLETED') {
        const saved = await this.#receipt(row, op);
        if (canonicalJson(saved.result) !== canonicalJson(result)) fail('RECEIPT_CONFLICT');
        return saved;
      }
      if (row.state !== 'CLAIMED') fail('CLAIM_NOT_ACTIVE');
      const completed_at = new Date().toISOString();
      const unsigned = { schema: 'debo.gemini.transport_receipt.v1', receipt_id: `TRANSPORT-${crypto.randomUUID()}`, project_id: op.project_id, idempotency_key: op.idempotency_key, caller_sha256: await sha256(this.#context.principal), provider_scope: this.#context.providerScope, request_sha256: op.request_sha256, result, result_sha256: await sha256(result), completed_at };
      const receipt = { ...unsigned, receipt_sha256: await sha256(unsigned) };
      const serializedReceipt = JSON.stringify(receipt);
      if (utf8Bytes(serializedReceipt) > 48_000) fail('RECEIPT_LIMIT', 'Candidate receipt exceeds its UTF-8 byte limit');
      const updated = await this.#query(
        "UPDATE bridge_execution_claims SET state = 'COMPLETED', receipt_json = ?1, updated_at = ?2 WHERE project_id = ?3 AND idempotency_key = ?4 AND owner_id = ?5 AND request_sha256 = ?6 AND owner_token = ?7 AND state = 'CLAIMED' RETURNING owner_token",
        [serializedReceipt, completed_at, op.project_id, op.idempotency_key, this.#context.principal, op.request_sha256, claim.owner_token]
      );
      if (updated?.owner_token !== claim.owner_token) fail('CLAIM_NOT_ACTIVE');
      return await this.#receipt(this.#checkRow(await this.#read(op), op), op);
    } catch (error) {
      if (error?.code === 'STORE_UNAVAILABLE') {
        try { await this.markUncertain(claim); } catch { /* Durable CLAIMED still blocks retry. */ }
        fail('EXECUTION_UNCERTAIN', 'Result persistence is uncertain; do not repeat provider execution');
      }
      throw error;
    }
  }
  async markUncertain(claim) {
    const { op, row } = await this.#handle(claim);
    if (row.state === 'COMPLETED') fail('CLAIM_NOT_ACTIVE');
    if (row.state === 'UNCERTAIN') return { status: 'UNCERTAIN' };
    const updated = await this.#query(
      "UPDATE bridge_execution_claims SET state = 'UNCERTAIN', updated_at = ?1 WHERE project_id = ?2 AND idempotency_key = ?3 AND owner_id = ?4 AND request_sha256 = ?5 AND owner_token = ?6 AND state = 'CLAIMED' RETURNING owner_token",
      [new Date().toISOString(), op.project_id, op.idempotency_key, this.#context.principal, op.request_sha256, claim.owner_token]
    );
    if (updated?.owner_token !== claim.owner_token) fail('CLAIM_NOT_ACTIVE');
    return { status: 'UNCERTAIN' };
  }
}
