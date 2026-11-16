import { timingSafeEqual, createHash } from 'node:crypto';
import { PolicyError } from './contracts.mjs';
export { PolicyError, validateEndpoint, validateInput, validateOutput } from './contracts.mjs';
const fail = (code, text) => { throw new PolicyError(code, text); };
export function hashJson(object) { return createHash('sha256').update(JSON.stringify(object)).digest('hex'); }
export function assertCaller(provided, expected) {
  if (typeof expected !== 'string' || expected.length < 16) fail('AUTH_UNCONFIGURED', 'Server caller credential not configured');
  if (typeof provided !== 'string') fail('AUTH_INVALID','Caller token missing');
  const a = createHash('sha256').update(provided).digest();
  const b = createHash('sha256').update(expected).digest();
  if (!timingSafeEqual(a,b)) fail('AUTH_INVALID','Caller token invalid');
}
