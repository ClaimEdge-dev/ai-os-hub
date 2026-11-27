// Test adapter: real local SQLite, NOT the deployed Cloudflare D1 runtime.
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';

export function sqliteD1(path = ':memory:', migrate = true) {
  const database = new DatabaseSync(path);
  database.exec('PRAGMA busy_timeout = 5000');
  if (migrate) database.exec(readFileSync(new URL('../../migrations/0001_synthetic_receipts.sql', import.meta.url), 'utf8'));
  const binding = {
    withSession(constraint) {
      if (constraint !== 'first-primary') throw new Error('Primary-consistent session required');
      return {
        prepare(sql) {
          return { bind: (...values) => ({ first: async () => database.prepare(sql).get(...values) ?? null }) };
        }
      };
    }
  };
  return { database, binding, close: () => database.close() };
}

export function testEnvironment(binding, caller = 'synthetic-owner') {
  return {
    DB: binding,
    DEBO_BRIDGE_MODE: 'synthetic_only',
    DEBO_IDENTITY_BOUNDARY: 'sites_dispatch',
    DEBO_ENABLE_LIVE_GEMINI: 'false',
    DEBO_CALLER_PROJECT_ACL: JSON.stringify({ [caller]: ['DEBO-CORE'] })
  };
}

export const executeArguments = { project_id: 'DEBO-CORE', idempotency_key: 'synthetic-bridge-0001', fixture_id: 'bridge-health-v1' };

export function rpcRequest(method, params = {}, options = {}) {
  return new Request(options.url ?? 'https://synthetic.invalid/mcp', {
    method: options.method ?? 'POST',
    headers: { 'content-type': 'application/json', 'oai-authenticated-user-id': 'synthetic-owner', ...options.headers },
    body: options.method === 'GET' ? undefined : options.body ?? JSON.stringify({ jsonrpc: '2.0', id: 1, method, params })
  });
}

export async function callTool(worker, env, name = 'debo_gemini_execute', args = executeArguments, options = {}) {
  const response = await worker.fetch(rpcRequest('tools/call', { name, arguments: args }, options), env);
  const rpc = await response.json();
  const value = rpc.result?.content?.[0]?.text;
  return { response, rpc, value: value ? JSON.parse(value) : undefined };
}
