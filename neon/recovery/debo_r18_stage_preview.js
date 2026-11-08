'use strict';
// NONPRODUCTION ONLY. No database clients, no SQL execution, no writes.
const {plan, STATUSES} = require('./debo_r18_sync_plan');
const HEX64 = /^[0-9a-f]{64}$/;

function preview(rows, approvals, source, prior = []) {
  if (!source || typeof source.document_id !== 'string' || !source.document_id.trim())
    throw Error('Verified source document ID required');
  if (!source.tab || source.tab !== 'Portfolio Work Stack')
    throw Error('Unexpected source tab');
  if (!Array.isArray(prior)) throw Error('Prior receipts must be an array');
  const old = new Map();
  for (const entry of prior) {
    if (!entry || !entry.work_id || !HEX64.test(String(entry.source_row_hash)))
      throw Error('Invalid prior receipt');
    if (old.has(entry.work_id)) throw Error('Duplicate prior receipt');
    old.set(entry.work_id, entry);
  }
  const planned = plan(rows, approvals, source);
  const steps = planned.entries.map(e => {
    if (e.decision !== 'ACCEPT') return {
      work_id: e.task_id, action: 'SKIP', reason: e.decision
    };
    if (!STATUSES.has(e.status)) throw Error('Unapproved task status');
    const before = old.get(e.task_id);
    const next = {
      work_id: e.task_id,
      source_row_hash: e.provenance.source_row_hash,
      raw_source_state: e.provenance.raw_source_state,
      mapped_status: e.status
    };
    if (!before) return {work_id: e.task_id, action: 'STAGE_CANDIDATE', next};
    const equal = before.source_row_hash === next.source_row_hash
      && before.raw_source_state === next.raw_source_state
      && before.mapped_status === next.mapped_status;
    return {work_id: e.task_id, action: equal ? 'NOOP' : 'CONFLICT_REVIEW',
      ...(equal ? {} : {reason:'CHANGED_SOURCE_OR_MAPPING'})};
  });
  const counts = steps.reduce((acc, step) => {
    acc[step.action] = (acc[step.action] || 0) + 1;
    return acc;
  }, {});
  return {mode:'OFFLINE_PREVIEW', write_eligible:false, counts, steps};
}

function simulateRollback(rows, approvals, source, prior = []) {
  // Clone a fixture ledger, stage candidate rows into the clone, then discard it.
  // This is NOT a database rollback receipt.
  const result = preview(rows, approvals, source, prior);
  const before = JSON.stringify(prior);
  const proposed = new Map(prior.map(x => [x.work_id, {...x}]));
  for (const step of result.steps) {
    if (step.action === 'CONFLICT_REVIEW')
      return {mode:'IN_MEMORY_SIMULATION', rolled_back:true, applied:0,
        blocked:'CONFLICT_REVIEW', original_unchanged:JSON.stringify(prior) === before};
    if (step.action === 'STAGE_CANDIDATE') proposed.set(step.work_id, step.next);
  }
  const staged = proposed.size - prior.length;
  return {mode:'IN_MEMORY_SIMULATION', rolled_back:true, applied:0,
    staged_before_rollback:staged,
    original_unchanged:JSON.stringify(prior) === before,
    original_count:prior.length};
}
module.exports = {preview, simulateRollback};
