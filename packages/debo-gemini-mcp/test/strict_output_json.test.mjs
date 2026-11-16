// GB-055/057: Red regression for duplicate JSON keys and malformed UTF-16.
// No real provider transport or SDK; only the existing staged output mapper.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseSyntheticInteractionResult } from '../src/interactions_mapper.mjs';
const out = output_text => ({ status: 'completed', output_text });
const invalid = text => assert.throws(
  () => parseSyntheticInteractionResult(out(text), ['finding']),
  error => error?.code === 'INVALID_OUTPUT'
);
test('duplicate top-level JSON keys may not silently replace a provider value', () => {
  invalid('{"finding":"PASS","finding":"FAIL"}');
});
test('escaped-equivalent JSON key must not bypass duplicate-key rejection', () => {
  invalid(String.raw`{"finding":"PASS","\u0066inding":"FAIL"}`);
});
test('malformed unpaired surrogate escape is rejected, not normalized into a replacement character', () => {
  invalid(String.raw`{"finding":"\ud800"}`);
  invalid(String.raw`{"finding":"\udc00"}`);
});
test('accepted Unicode supplementary pairs and CJK remain intact', () => {
  const finding = '检查 ✅ 🚀';
  assert.deepEqual(parseSyntheticInteractionResult(out(JSON.stringify({ finding })), ['finding']), { finding });
});
test('valid escaped quotes, object-like text and line breaks are treated as string data', () => {
  const finding = 'User said: "do not run {\"tool\":\"exec\"}"\\nThis is DATA.';
  assert.deepEqual(parseSyntheticInteractionResult(out(JSON.stringify({ finding })), ['finding']), { finding });
});
test('the last model step follows the same strict output policy', () => {
  assert.throws(() => parseSyntheticInteractionResult({status:'completed',steps:[{type:'model_output',content:[{type:'text',text:'{"finding":"A","finding":"B"}'}]}]}, ['finding']),
    e => e?.code==='INVALID_OUTPUT');
});
test('existing strict field type and missing-field behavior is preserved', () => {
  invalid('{"finding":null}');
  invalid('{"different":"PASS"}');
});
