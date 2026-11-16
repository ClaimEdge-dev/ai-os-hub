import { PolicyError, validateInput, parseUnambiguousJson } from './contracts.mjs';

export const FIXTURES = Object.freeze({
  'bridge-health-v1': Object.freeze({ finding: 'SYNTHETIC_HEALTH_OK', source: 'server_fixture_only' }),
  'bridge-replay-v1': Object.freeze({ finding: 'SYNTHETIC_REPLAY_OK', source: 'server_fixture_only' })
});
const deny = (code, message) => { throw new PolicyError(code, message); };
export const KEY_PATTERN = '^[A-Za-z0-9._:-]{8,128}$';
export const PROJECT_PATTERN = '^[A-Z][A-Z0-9-]{1,63}$';
const propertySchemas = {
  project_id: { type: 'string', pattern: PROJECT_PATTERN, maxLength: 64 },
  idempotency_key: { type: 'string', pattern: KEY_PATTERN, minLength: 8, maxLength: 128 },
  fixture_id: { type: 'string', enum: Object.keys(FIXTURES) }
};
export function argumentSchema(execute) {
  const fields = execute ? ['project_id', 'idempotency_key', 'fixture_id'] : ['project_id', 'idempotency_key'];
  return { type: 'object', properties: Object.fromEntries(fields.map(k => [k, propertySchemas[k]])), required: fields, additionalProperties: false };
}
export function validateArguments(args, execute) {
  const fields = execute ? ['project_id', 'idempotency_key', 'fixture_id'] : ['project_id', 'idempotency_key'];
  if (!args || typeof args !== 'object' || Array.isArray(args) || Object.keys(args).length !== fields.length || fields.some(k => !Object.hasOwn(args, k))) deny('BAD_REQUEST', 'Only the documented tool arguments are permitted');
  if (typeof args.project_id !== 'string' || !new RegExp(PROJECT_PATTERN).test(args.project_id) || typeof args.idempotency_key !== 'string' || !new RegExp(KEY_PATTERN).test(args.idempotency_key)) deny('BAD_REQUEST', 'Invalid project or receipt key');
  if (execute && (typeof args.fixture_id !== 'string' || !Object.hasOwn(FIXTURES, args.fixture_id))) deny('BAD_REQUEST', 'Select a documented server-owned fixture');
  return structuredClone(args);
}
export function fixtureInput(args) {
  return validateInput({
    project_id: args.project_id,
    idempotency_key: args.idempotency_key,
    task_type: 'test_fixture_analysis',
    task_description: 'Check the fixed synthetic bridge fixture',
    approved_sources: [`fixtures/${args.fixture_id}.json`],
    payload: `SYNTHETIC:${JSON.stringify({ fixture_id: args.fixture_id })}`,
    privacy_classification: 'INTERNAL_DEV', mode: 'read_only', cost_ceiling_usd: 0,
    expected_output_keys: ['finding', 'source']
  });
}
// The supported output schema is deliberately fixed and fully checked: two
// bounded strings, no extra fields, and the exact server-owned fixture values.
function validateFixtureOutput(output, fixture) {
  if (!output || typeof output !== 'object' || Array.isArray(output) || Object.keys(output).length !== 2 || ['finding', 'source'].some(k => !Object.hasOwn(output, k) || typeof output[k] !== 'string' || output[k].length > 128 || output[k] !== fixture[k])) deny('RECEIPT_INTEGRITY', 'Stored fixture output violates its contract');
}
export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonicalJson(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
}
export async function sha256(value) {
  const bytes = new TextEncoder().encode(canonicalJson(value));
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
}
export async function createReceipt(args, principal) {
  const output = structuredClone(FIXTURES[args.fixture_id]);
  const receipt = {
    schema: 'debo.gemini.fixture_receipt.v1', receipt_id: `FIXTURE-${crypto.randomUUID()}`,
    project_id: args.project_id, idempotency_key: args.idempotency_key, fixture_id: args.fixture_id,
    caller_sha256: await sha256(principal), provider: 'synthetic_fixture_only', status: 'TESTED_OFFLINE',
    input_sha256: await sha256(fixtureInput(args)), output_sha256: await sha256(output), output,
    network_calls: 0, actual_cost_usd: 0, executed_at: new Date().toISOString()
  };
  return { ...receipt, receipt_sha256: await sha256(receipt) };
}
const receiptFields = ['schema', 'receipt_id', 'project_id', 'idempotency_key', 'fixture_id', 'caller_sha256', 'provider', 'status', 'input_sha256', 'output_sha256', 'output', 'network_calls', 'actual_cost_usd', 'executed_at', 'receipt_sha256'];
export async function verifyReceipt(row, principal, args) {
  let receipt;
  try { receipt = parseUnambiguousJson(row.receipt_json, { maxChars: 48000 }); } catch { deny('RECEIPT_INTEGRITY', 'Stored receipt is invalid'); }
  if (!receipt || typeof receipt !== 'object' || Array.isArray(receipt) || Object.keys(receipt).length !== receiptFields.length || receiptFields.some(k => !Object.hasOwn(receipt, k))) deny('RECEIPT_INTEGRITY', 'Stored receipt has invalid fields');
  if (receipt.schema !== 'debo.gemini.fixture_receipt.v1' || receipt.project_id !== args.project_id || receipt.idempotency_key !== args.idempotency_key || row.owner_id !== principal || receipt.caller_sha256 !== await sha256(principal) || typeof receipt.fixture_id !== 'string' || !Object.hasOwn(FIXTURES, receipt.fixture_id) || receipt.provider !== 'synthetic_fixture_only' || receipt.status !== 'TESTED_OFFLINE' || receipt.network_calls !== 0 || receipt.actual_cost_usd !== 0 || typeof receipt.receipt_id !== 'string' || !/^FIXTURE-[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(receipt.receipt_id) || typeof receipt.executed_at !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(receipt.executed_at) || !Number.isFinite(Date.parse(receipt.executed_at))) deny('RECEIPT_INTEGRITY', 'Stored receipt has invalid scope or provenance');
  validateFixtureOutput(receipt.output, FIXTURES[receipt.fixture_id]);
  const { receipt_sha256, ...unsigned } = receipt;
  if (receipt_sha256 !== await sha256(unsigned) || receipt.output_sha256 !== await sha256(receipt.output) || receipt.input_sha256 !== row.input_sha256 || receipt.input_sha256 !== await sha256(fixtureInput(receipt))) deny('RECEIPT_INTEGRITY', 'Stored receipt checksum mismatch');
  return receipt;
}
