'use strict';
const assert = require('node:assert/strict');
const {preview,simulateRollback} = require('./debo_r18_stage_preview');
const SRC = {document_id:'synthetic-fixture-source',tab:'Portfolio Work Stack'};
const R = {work_id:'WORK-SYN-001',project_id:'SIM',project_name:'Synthetic',
  objective:'Test only',state:'REVIEW WITH OWNER',priority:'P2',owner:'Test',
  assignee_role:'Proof',pillar:'SYSTEMS'};
const A = {mappings:{[R.state]:{raw_state:R.state,status:'Review',approved_by:'owner',approved_at:'2026-11-08T03:00:00-06:00'}}};
let n = 0;
function test(fn) {fn(); n++;}
test(() => assert.equal(preview([R],A,SRC).steps[0].action,'STAGE_CANDIDATE'));
test(() => assert.equal(preview([R],{},SRC).steps[0].reason,'QUARANTINE'));
test(() => assert.equal(preview([{...R,state:'PARKED BY OWNER'}],A,SRC).steps[0].reason,'HOLD_OWNER'));
test(() => assert.throws(() => preview([R,R],A,SRC), /Duplicate work_id/));
test(() => assert.throws(() => preview([R],A,{...SRC,document_id:''}), /source document ID/));
test(() => assert.throws(() => preview([R],A,{...SRC,tab:'Other'}), /Unexpected source tab/));
test(() => assert.equal(preview([R],A,SRC).write_eligible,false));
const first = preview([R],A,SRC).steps[0].next;
test(() => assert.equal(preview([R],A,SRC,[first]).steps[0].action,'NOOP'));
test(() => assert.equal(preview([{...R,objective:'Changed'}],A,SRC,[first]).steps[0].action,'CONFLICT_REVIEW'));
test(() => assert.equal(preview([R],A,SRC,[{...first,mapped_status:'Done'}]).steps[0].action,'CONFLICT_REVIEW'));
test(() => assert.equal(preview([R],A,SRC,[{...first,raw_source_state:'CHANGED'}]).steps[0].action,'CONFLICT_REVIEW'));
test(() => assert.throws(() => preview([R],A,SRC,[first,first]),/Duplicate prior receipt/));
test(() => assert.throws(() => preview([R],A,SRC,[{...first,source_row_hash:'BAD'}]), /Invalid prior receipt/));
test(() => assert.equal(simulateRollback([R],A,SRC).rolled_back,true));
test(() => assert.equal(simulateRollback([R],A,SRC).staged_before_rollback,1));
test(() => assert.equal(simulateRollback([R],A,SRC).applied,0));
test(() => assert.equal(simulateRollback([R],A,SRC,[first]).staged_before_rollback,0));
test(() => assert.equal(simulateRollback([{...R,objective:'Changed'}],A,SRC,[first]).blocked,'CONFLICT_REVIEW'));
const history = [first];
test(() => assert.equal(simulateRollback([R],A,SRC,history).original_unchanged,true));
test(() => assert.equal(history.length,1));
console.log('PASS ' + n + ' offline staging/rollback assertions');
