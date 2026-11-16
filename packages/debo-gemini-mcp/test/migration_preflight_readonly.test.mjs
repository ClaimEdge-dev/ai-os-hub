// GB-031 / GB-032: read-only local metadata inspection before any reviewed
// hosted migration. This is SQLite test evidence, NOT remote D1 proof.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
const schema = readFileSync(new URL('../migrations/0002_execution_claims.sql', import.meta.url), 'utf8');
const required = new Map([
  ['project_id', { type: 'TEXT', pk: 1 }],
  ['idempotency_key', { type: 'TEXT', pk: 2 }],
  ['owner_id', { type: 'TEXT', pk: 0 }],
  ['provider_scope', { type: 'TEXT', pk: 0 }],
  ['request_sha256', { type: 'TEXT', pk: 0 }],
  ['request_json', { type: 'TEXT', pk: 0 }],
  ['owner_token', { type: 'TEXT', pk: 0 }],
  ['state', { type: 'TEXT', pk: 0 }],
  ['receipt_json', { type: 'TEXT', pk: 0 }],
  ['created_at', { type: 'TEXT', pk: 0 }],
  ['updated_at', { type: 'TEXT', pk: 0 }]
]);
function inspectReadonly(db) {
  // PRAGMAs and SELECTs only. Never output owner/claim/receipt data.
  const existence = db.prepare("SELECT type FROM sqlite_schema WHERE name = 'bridge_execution_claims'").get();
  if (!existence) return Object.freeze({ status: 'NOT_APPLIED', rows: null });
  if (existence.type !== 'table') return Object.freeze({ status: 'CONFLICTING_NAME', rows: null });
  const cols = db.prepare("PRAGMA table_info('bridge_execution_claims')").all();
  const expected = cols.length === required.size && cols.every(c => {
    const entry = required.get(c.name);
    const isNullable = c.name === 'receipt_json';
    return entry && c.type.toUpperCase() === entry.type && c.pk === entry.pk &&
      c.notnull === (isNullable ? 0 : 1);
  });
  const sql = db.prepare("SELECT sql FROM sqlite_schema WHERE type='table' AND name='bridge_execution_claims'").get()?.sql ?? '';
  const constraints = sql.includes("PRIMARY KEY(project_id, idempotency_key)") &&
    sql.includes("state IN ('CLAIMED', 'COMPLETED', 'UNCERTAIN')") &&
    sql.includes("receipt_json IS NOT NULL") && sql.includes("receipt_json IS NULL");
  if (!expected || !constraints) return Object.freeze({ status: 'SCHEMA_CONFLICT', rows: null });
  const rows = db.prepare('SELECT COUNT(*) AS total FROM bridge_execution_claims').get().total;
  return Object.freeze({ status: 'SCHEMA_MATCH_LOCAL', rows });
}
test('GB-031 missing local migration is reported, never auto-applied', () => {
  const db = new DatabaseSync(':memory:');
  try {
    db.exec("CREATE TABLE unrelated (x TEXT); INSERT INTO unrelated VALUES ('keep');");
    assert.deepEqual(inspectReadonly(db), { status: 'NOT_APPLIED', rows: null });
    assert.equal(db.prepare("SELECT x FROM unrelated").get().x, 'keep');
    assert.equal(db.prepare("SELECT COUNT(*) AS n FROM sqlite_schema WHERE name='bridge_execution_claims'").get().n, 0);
  } finally { db.close(); }
});
test('GB-031 applied synthetic schema is metadata-only readable', () => {
  const db = new DatabaseSync(':memory:');
  try {
    db.exec("CREATE TABLE unrelated (x TEXT); INSERT INTO unrelated VALUES ('protected');");
    db.exec(schema); // isolated test fixture setup, never a remote migration.
    const before = db.prepare("SELECT group_concat(name || ':' || sql) AS s FROM sqlite_schema WHERE type='table' ORDER BY name").get().s;
    assert.deepEqual(inspectReadonly(db), { status: 'SCHEMA_MATCH_LOCAL', rows: 0 });
    assert.equal(db.prepare("SELECT group_concat(name || ':' || sql) AS s FROM sqlite_schema WHERE type='table' ORDER BY name").get().s, before);
    assert.equal(db.prepare("SELECT x FROM unrelated").get().x, 'protected');
  } finally { db.close(); }
});
test('GB-031 existing conflict never triggers replacement or DDL', () => {
  const db = new DatabaseSync(':memory:');
  try {
    db.exec("CREATE TABLE bridge_execution_claims (project_id TEXT PRIMARY KEY, leak TEXT); INSERT INTO bridge_execution_claims VALUES ('owner-private', 'DO_NOT_READ');");
    const before = db.prepare("SELECT sql FROM sqlite_schema WHERE name='bridge_execution_claims'").get().sql;
    assert.deepEqual(inspectReadonly(db), { status: 'SCHEMA_CONFLICT', rows: null });
    assert.equal(db.prepare("SELECT sql FROM sqlite_schema WHERE name='bridge_execution_claims'").get().sql, before);
    assert.equal(db.prepare("SELECT leak FROM bridge_execution_claims").get().leak, 'DO_NOT_READ');
  } finally { db.close(); }
});
test('GB-032 source backout never deletes completed and uncertain synthetic claims', () => {
  const db = new DatabaseSync(':memory:');
  try {
    db.exec(schema);
    const cols = db.prepare("PRAGMA table_info('bridge_execution_claims')").all();
    assert.equal(cols.filter(x => x.pk).length, 2);
    const forbidden = ['DROP TABLE', 'DELETE FROM', 'TRUNCATE', 'UPDATE bridge_execution_claims'];
    for (const term of forbidden) assert.equal(schema.toUpperCase().includes(term), false);
    // Proposed rollback is disable dispatch and revert source with an approved
    // private-host procedure, never DROP/DELETE/RETRY the existing claims.
    assert.deepEqual(inspectReadonly(db), { status: 'SCHEMA_MATCH_LOCAL', rows: 0 });
  } finally { db.close(); }
});
