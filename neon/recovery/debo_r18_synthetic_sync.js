'use strict';
/**
 * R18 synthetic, in-memory acceptance harness ONLY. No network, Neon, or Drive calls.
 * This file is NOT a persistent integration or permission to import real tasks.
 * For actual sync, the reviewed mapping + authorized branch + private provenance
 * storage and source/version guards must be implemented and independently tested.
 */
const VALID = new Set(['Backlog', 'In Progress', 'Blocked', 'Review', 'Done']);
const ID_PATTERN = /^[A-Z0-9][A-Z0-9_-]{2,127}$/;
const HASH_PATTERN = /^[a-f0-9]{64}$/;
function makeStore() { return { tasks: new Map(), provenance: new Map(), receipts: [] }; }
function snapshot(store) { return { tasks: new Map(store.tasks), provenance: new Map(store.provenance), receipts: store.receipts.slice() }; }
function restore(store, old) { store.tasks = old.tasks; store.provenance = old.provenance; store.receipts = old.receipts; }
function fail(reason) { const error = new Error(reason); error.code = reason; throw error; }
function validateEntry(entry) {
  if (!entry || !ID_PATTERN.test(entry.task_id || '')) fail('INVALID_TASK_ID');
  if (entry.decision !== 'ACCEPT') return;
  if (entry.reason !== 'REVIEWED_EXACT_MAPPING' || !VALID.has(entry.status)) fail('UNREVIEWED_MAPPING');
  const p = entry.provenance;
  if (!p || p.source_system !== 'google_drive' || !p.source_document_id ||
      !p.source_tab || p.work_id !== entry.task_id ||
      typeof p.raw_source_state !== 'string' || !p.raw_source_state ||
      !HASH_PATTERN.test(p.source_row_hash || '') || !p.mapping_rule_version) fail('INVALID_PROVENANCE');
  if (p.raw_source_state.toUpperCase().includes('PARKED BY OWNER') || entry.task_id === 'WORK-RENTALS-001') fail('OWNER_HOLD_VIOLATION');
}
/** Atomic simulation, not a DB or network adapter. Reject ambiguous changes. */
function simulateBatch(batch, store, {mode = '', injectFailureAfter = 0} = {}) {
  if (mode !== 'synthetic-in-memory') fail('REAL_WRITES_DISABLED');
  if (!store || !(store.tasks instanceof Map) || !(store.provenance instanceof Map) || !Array.isArray(store.receipts)) fail('INVALID_STORE');
  if (!batch || !Array.isArray(batch.entries) || batch.write_eligible !== false) fail('NOT_DRY_RUN_PLAN');
  const ids = new Set(), actions = [];
  const counts = {staged:0, noop:0, quarantined:0, owner_held:0, rejected:0, conflicts:0};
  // Plan every change before touching the in-memory store.
  for (const entry of batch.entries) {
    validateEntry(entry);
    if (ids.has(entry.task_id)) fail('DUPLICATE_SOURCE_ID');
    ids.add(entry.task_id);
    if (entry.decision === 'HOLD_OWNER') { counts.owner_held++; continue; }
    if (entry.decision === 'QUARANTINE' || entry.decision === 'REVIEW_FIELD_MAPPING') { counts.quarantined++; continue; }
    if (entry.decision !== 'ACCEPT') { counts.rejected++; continue; }
    const p = entry.provenance, existing = store.tasks.get(entry.task_id), old = store.provenance.get(entry.task_id);
    if (existing || old) {
      if (!existing || !old || existing.status !== entry.status ||
          old.source_row_hash !== p.source_row_hash || old.source_document_id !== p.source_document_id ||
          old.raw_source_state !== p.raw_source_state) { counts.conflicts++; continue; }
      counts.noop++; continue;
    }
    actions.push({task_id:entry.task_id,status:entry.status,provenance:{...p}});
  }
  if (counts.conflicts) return {state:'CONFLICT_REVIEW',counts,changed:false};
  const before = snapshot(store);
  try {
    for (const action of actions) {
      store.tasks.set(action.task_id, {task_id:action.task_id,status:action.status});
      store.provenance.set(action.task_id, action.provenance);
      store.receipts.push({task_id:action.task_id,outcome:'SYNTHETIC_STAGED'});
      counts.staged++;
      if (injectFailureAfter > 0 && counts.staged >= injectFailureAfter) fail('INJECTED_FAILURE');
    }
    return {state:'SIMULATED',counts,changed:actions.length>0};
  } catch (err) { restore(store, before); throw err; }
}
module.exports = { makeStore, simulateBatch };
