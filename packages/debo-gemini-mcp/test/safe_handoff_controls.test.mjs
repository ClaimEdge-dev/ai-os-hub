import { test } from 'node:test';
import assert from 'node:assert/strict';
import { runIndependentReads, createSerializedSourceWriter, prepareDraftReplacement } from '../src/safe_handoff_controls.mjs';
const deferred=()=>{let resolve;const promise=new Promise(r=>{resolve=r;});return{resolve,promise};};
const read=(id,fn)=>({source_id:id,independent:true,read:fn});
const editor=(current_text,checkpointed_previous_text,mission_id='DEBO-HANDOFF-008')=>({
  mission_id,current_text,checkpointed_previous_text,
  next_text:'DEBO-HANDOFF '+mission_id+'\nSYNTHETIC PUBLIC CODE TASK'
});
test('GB-118 batch independent reads with a strict 3-call concurrency ceiling',async()=>{
  let active=0,max=0;const gate=deferred();const entered=deferred();let started=0;
  const jobs=Array.from({length:7},(_,i)=>read('source-'+i,async()=>{
    active++;started++;max=Math.max(max,active);
    if(started===3)entered.resolve();
    await gate.promise;active--;return 'ok-'+i;
  }));
  const pending=runIndependentReads(jobs,{maxConcurrent:3});
  await entered.promise;assert.equal(started,3);gate.resolve();
  const result=await pending;assert.equal(result.length,7);assert.equal(max,3);
  assert.deepEqual(result.map(r=>r.value),Array.from({length:7},(_,i)=>'ok-'+i));
});
test('GB-118 sequential fallback processes reads in source order',async()=>{
  let max=0,active=0;const order=[];
  const r=await runIndependentReads(Array.from({length:5},(_,i)=>read('source-'+i,async()=>{
    active++;max=Math.max(max,active);order.push(i);
    await Promise.resolve();active--;return i;
  })),{maxConcurrent:1});
  assert.equal(max,1);assert.deepEqual(order,[0,1,2,3,4]);
  assert.deepEqual(r.map(x=>x.value),order);
});
test('GB-118 failed read never leaks exception text or triggers an implicit retry',async()=>{
  let calls=0;
  const results=await runIndependentReads([read('source-1',async()=>{calls++;throw Error('private:credential');}),
    read('source-2',async()=>42)]);
  assert.equal(calls,1);
  assert.deepEqual(results[0],{source_id:'source-1',status:'FAILED',code:'READ_FAILED'});
  assert.equal(JSON.stringify(results).includes('private:'),false);
  assert.equal(results[1].value,42);
});
test('GB-118 malformed or not independently approved read tasks fail before any call',async()=>{
  let calls=0;
  for(const list of [[read('source-1',async()=>{calls++;}),{source_id:'other',independent:false,read:async()=>{calls++;}}],
    [{source_id:'source-1',independent:true,read:async()=>{},secret:true}]]) {
    await assert.rejects(runIndependentReads(list),TypeError);
  }
  for(const maxConcurrent of [0,5,1.5,Infinity]) {
    await assert.rejects(runIndependentReads([read('source-1',async()=>{calls++;})],{maxConcurrent}),TypeError);
  }
  assert.equal(calls,0);
});
test('GB-118 one source writer serializes the mutations, without swapping source order',async()=>{
  const writer=createSerializedSourceWriter(),gate=deferred(),events=[];
  const a=writer.write({source_id:'source-1',mutation_id:'write-1',run:async()=>{events.push('first-start');await gate.promise;events.push('first-end');return 1;}});
  const b=writer.write({source_id:'source-1',mutation_id:'write-2',run:async()=>{events.push('second');return 2;}});
  await Promise.resolve();assert.deepEqual(events,['first-start']);
  gate.resolve();assert.deepEqual(await Promise.all([a,b]),[1,2]);
  assert.deepEqual(events,['first-start','first-end','second']);
});
test('GB-118 same in-flight mutation is rejected; separate sources may run concurrently',async()=>{
  const writer=createSerializedSourceWriter(),gate=deferred(),started=deferred();let count=0;
  const a=writer.write({source_id:'source-1',mutation_id:'write-1',run:async()=>{count++;started.resolve();await gate.promise;return'ok';}});
  await started.promise;
  await assert.rejects(writer.write({source_id:'source-1',mutation_id:'write-1',run:async()=>{count++;}}),/DUPLICATE_IN_FLIGHT_WRITE/);
  const b=await writer.write({source_id:'source-2',mutation_id:'write-1',run:async()=>42});
  assert.equal(b,42);assert.equal(count,1);gate.resolve();await a;
});
test('GB-118 failed first write does not automatically retry or prevent next queued write',async()=>{
  const writer=createSerializedSourceWriter();let count=0;
  const a=writer.write({source_id:'source-1',mutation_id:'write-1',run:async()=>{count++;throw Error('failed');}});
  const b=writer.write({source_id:'source-1',mutation_id:'write-2',run:async()=>{count++;return'next';}});
  await assert.rejects(a,/failed/);assert.equal(await b,'next');assert.equal(count,2);
});
test('GB-082 empty composer permits only a prepared, never sent, handoff',()=>{
  const r=prepareDraftReplacement(editor(''));
  assert.equal(r.status,'PREPARED_EMPTY_EDITOR');assert.equal(r.allowed,true);
  assert.ok(r.proposed_text.startsWith('DEBO-HANDOFF DEBO-HANDOFF-008\n'));
});
test('GB-082 unrelated user draft is preserved even when next handoff looks legitimate',()=>{
  const r=prepareDraftReplacement(editor('An unrelated personal unsent message','An unrelated personal unsent message'));
  assert.deepEqual(r,{status:'BLOCKED',code:'UNVERIFIED_DRAFT_PRESERVED'});
  assert.equal(JSON.stringify(r).includes('unrelated personal'),false);
});
test('GB-082 same-mission draft also blocks if not recorded exactly',()=>{
  const current='DEBO-HANDOFF DEBO-HANDOFF-008\nEdited text';
  const r=prepareDraftReplacement(editor(current,'DEBO-HANDOFF DEBO-HANDOFF-008\nOld version'));
  assert.equal(r.status,'BLOCKED');
});
test('GB-082 only exact same-mission previously checkpointed draft can be replaced',()=>{
  const current='DEBO-HANDOFF DEBO-HANDOFF-008\nSYNTHETIC PREVIOUS TASK';
  const r=prepareDraftReplacement(editor(current,current));
  assert.equal(r.status,'PREPARED_VERIFIED_REPLACEMENT');assert.equal(r.allowed,true);
});
test('GB-082 malformed new draft or mission fails closed',()=>{
  assert.throws(()=>prepareDraftReplacement({...editor(''),next_text:'wrong task'}),TypeError);
  assert.throws(()=>prepareDraftReplacement(editor('','','bad mission')),TypeError);
});
