import assert from 'node:assert/strict';
import { planSync } from '../tools/debo_r19_sync.mjs';
const base={schema:'debo.r19.event.v1', event_type:'TASK_VERIFIED',event_id:'DEBO-EVENT-abc',project_id:'DEBO',task_id:'DEBO-TASK-abc',checkpoint:'R19',source_revision:'rev-1',status:'TESTED',scope:'private',evidence:[{type:'test_receipt',ref:'local:test-1'}]};
let checks=0;
function test(fn){fn();checks++}
test(()=>assert.equal(planSync(base).result,'DRY_RUN'));
test(()=>assert.equal(planSync(base).writes,0));
test(()=>assert.deepEqual(planSync(base).destinations,['OWNING_PROJECT_CHECKPOINT','DEBO_CORE_INDEX']));
test(()=>assert.equal(planSync({...base,scope:'public_metadata'}).destinations.length,3));
test(()=>assert.equal(planSync(base,new Set(['DEBO-EVENT-abc'])).result,'SKIP_DUPLICATE'));
test(()=>assert.throws(()=>planSync({...base,status:'LIVE'}),/runtime_probe/));
test(()=>assert.throws(()=>planSync({...base,status:'UNKNOWN'}),/no verified completion/));
test(()=>assert.throws(()=>planSync({...base,scope:'invalid'}),/scope/));
test(()=>assert.throws(()=>planSync({...base,project_id:' '}),/project_id/));
test(()=>assert.throws(()=>planSync({...base, event_type:'SNEAKY'}),/invalid event/));
console.log('PASS: ' + checks + ' JavaScript dry-run assertions');
