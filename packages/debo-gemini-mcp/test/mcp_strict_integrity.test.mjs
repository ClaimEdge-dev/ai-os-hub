// GB-035/055: strict JSON protects the existing synthetic MCP Worker and its
// durable receipts, not only the unactivated provider-output mapper.
// These tests use a local SQLite D1 emulator. No network/provider calls.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/mcp_worker.mjs';
import { sqliteD1, testEnvironment, rpcRequest, callTool, executeArguments } from './helpers/sqlite-d1.mjs';

const local = async fn => {
  const db = sqliteD1();
  try { return await fn(db, testEnvironment(db.binding)); }
  finally { db.close(); }
};
const raw = (env, body) => worker.fetch(rpcRequest('tools/list', {}, { body }), env);
const receiptErr = result => result.value?.error?.code;

test('duplicate JSON-RPC method names reject the request rather than choosing last', () => local(async (db, env) => {
  const r = await raw(env, '{"jsonrpc":"2.0","id":1,"method":"tools/call","method":"tools/list","params":{}}');
  assert.equal(r.status, 400);
  assert.equal((await r.json()).error.code, -32700);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n, 0);
}));
test('escaped-equivalent duplicate method names also reject the request', () => local(async (_, env) => {
  const r = await raw(env, String.raw`{"jsonrpc":"2.0","id":1,"method":"tools/call","\u006dethod":"tools/list","params":{}}`);
  assert.equal(r.status, 400);
  assert.equal((await r.json()).error.code, -32700);
}));
test('duplicate tool argument project_id cannot silently switch authority', () => local(async (db, env) => {
  const args = '{"project_id":"JCT","project_id":"DEBO-CORE","idempotency_key":"synthetic-bridge-0001","fixture_id":"bridge-health-v1"}';
  const r = await raw(env,'{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"debo_gemini_execute","arguments":'+args+'}}');
  assert.equal(r.status,400);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n,0);
}));
test('duplicate nested metadata property cannot be normalized through JSON.parse', () => local(async (_,env)=>{
  const r=await raw(env,'{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}');
  assert.equal(r.status,400);
}));
test('invalid Unicode lone surrogate in wire JSON is rejected',()=>local(async(_,env)=>{
  const r=await raw(env,String.raw`{"jsonrpc":"2.0","id":1,"method":"tools/li\ud800st","params":{}}`);
  assert.equal(r.status,400);
}));
test('duplicate immutable stored receipt key cannot replay despite matching decoded SHA',()=>local(async (db,env)=>{
  const initial=await callTool(worker,env,'debo_gemini_execute',executeArguments);
  assert.equal(initial.rpc.result.isError,false);
  const row=db.database.prepare('SELECT receipt_json FROM bridge_fixture_receipts').get();
  const needle='"provider":"synthetic_fixture_only"';
  assert.ok(row.receipt_json.includes(needle));
  const tampered=row.receipt_json.replace(needle,needle+','+needle);
  assert.deepEqual(JSON.parse(tampered),JSON.parse(row.receipt_json));
  db.database.prepare('UPDATE bridge_fixture_receipts SET receipt_json=?').run(tampered);
  const read=await callTool(worker,env,'debo_get_receipt',{project_id:executeArguments.project_id,idempotency_key:executeArguments.idempotency_key});
  assert.equal(receiptErr(read),'RECEIPT_INTEGRITY');
  const replay=await callTool(worker,env,'debo_gemini_execute',executeArguments);
  assert.equal(receiptErr(replay),'RECEIPT_INTEGRITY');
  assert.equal(db.database.prepare('SELECT receipt_json FROM bridge_fixture_receipts').get().receipt_json,tampered);
  assert.equal(db.database.prepare('SELECT count(*) AS n FROM bridge_fixture_receipts').get().n,1);
}));
test('valid source strings with escaped punctuation remain accepted',()=>local(async(_,env)=>{
  const r=await raw(env,'{"jsonrpc":"2.0","id":"a\\\\nb","method":"tools/list","params":{}}');
  assert.equal(r.status,200);
  assert.ok((await r.json()).result.tools.length===2);
}));
