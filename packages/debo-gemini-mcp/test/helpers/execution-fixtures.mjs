import { readFileSync } from 'node:fs';
import { sqliteD1 } from './sqlite-d1.mjs';

export const executionInput = { project_id: 'DEBO-CORE', task_type: 'test_fixture_analysis', task_description: 'Check a deliberately synthetic execution fixture', approved_sources: ['fixtures/health.json'], payload: 'SYNTHETIC:{"case":"health"}', idempotency_key: 'execution-fixture-v1', privacy_classification: 'PUBLIC', mode: 'read_only', cost_ceiling_usd: 0, expected_output_keys: ['finding'] };
export const executionContext = { principal: 'synthetic-execution-owner', projects: ['DEBO-CORE'], providerScope: 'synthetic-provider-project' };
export const executionResult = { interaction_id: 'synthetic-interaction-1', model: 'gemini-3.8-flash', output: { finding: 'PASS' }, usage: { total_input_tokens: 20, total_output_tokens: 5, total_tokens: 25 }, provider_requests: 1, billing_verified: false };
export function executionD1(path = ':memory:', migrate = true) {
  const local = sqliteD1(path, migrate);
  if (migrate) local.database.exec(readFileSync(new URL('../../migrations/0002_execution_claims.sql', import.meta.url), 'utf8'));
  return local;
}
