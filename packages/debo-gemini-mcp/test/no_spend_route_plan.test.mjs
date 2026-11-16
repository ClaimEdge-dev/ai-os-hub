import { test } from 'node:test';
import assert from 'node:assert/strict';
import { proposeNoSpendRoute } from '../src/no_spend_route_plan.mjs';
const task = () => ({ project_id:'DEBO-CORE',mission_id:'DEBO-GEMINI-BRIDGE-PR81',kind:'public_research',classification:'PUBLIC' });
const cap = (kind,overrides={}) => ({kind,project_id:'DEBO-CORE',access:'AVAILABLE',pricing:'VERIFIED_ZERO_NEW_SPEND',supports:['public_research'],...overrides});
const plan = (capabilities,other={})=>proposeNoSpendRoute({task:task(),capabilities,...other});
test('GB-111 prefer existing scoped connected read over public browser',()=>{
  const p=plan([cap('public_browser'),cap('connected_read')]);
  assert.equal(p.selected_route,'connected_read'); assert.equal(p.dispatch_authorized,false);assert.equal(p.automatic_fallback,false);
});
test('GB-111 use public browser candidate only when verified no-spend connected reader absent',()=>{
  const p=plan([cap('connected_read',{access:'UNAVAILABLE'}),cap('public_browser')]);
  assert.equal(p.selected_route,'public_browser'); assert.equal(p.dispatch_authorized,false);
});
test('GB-111 unknown account allowance stays unknown, never free by assumption',()=>{
  const p=plan([cap('connected_read',{pricing:'UNKNOWN'}),cap('public_browser',{pricing:'UNKNOWN'})]);
  assert.equal(p.status,'HOLD');assert.equal(p.reason,'NO_VERIFIED_NO_SPEND_ROUTE');
});
test('GB-111 paid-only and unverified site routes are excluded',()=>{
  const p=plan([cap('connected_read',{pricing:'PAID'}),cap('public_browser',{access:'UNKNOWN'})]);
  assert.equal(p.status,'HOLD');assert.equal(p.selected_route,null);
});
test('GB-111 real Gemini API is never an enabled candidate from task metadata',()=>{
  const p=plan([cap('gemini_api')]);
  assert.equal(p.status,'HOLD'); assert.equal(p.dispatch_authorized,false);
});
test('GB-025 uncertain attempt blocks automatic route switching even when browser is eligible',()=>{
  const p=plan([cap('public_browser')],{existing_attempt:{mission_id:task().mission_id,state:'UNCERTAIN'}});
  assert.equal(p.reason,'UNCERTAIN_ATTEMPT_NO_ROUTE_SWITCH');assert.equal(p.automatic_fallback,false);
});
test('GB-025 completed or claimed same task cannot be dispatched elsewhere',()=>{
  for(const state of ['CLAIMED','COMPLETED']){
    const p=plan([cap('connected_read')],{existing_attempt:{mission_id:task().mission_id,state}});
    assert.equal(p.status,'HOLD');assert.equal(p.selected_route,null);
  }
});
test('GB-025 only known NOT_STARTED can produce another recommendation, not execution',()=>{
  const p=plan([cap('connected_read')],{existing_attempt:{mission_id:task().mission_id,state:'NOT_STARTED'}});
  assert.equal(p.status,'CANDIDATE_REQUIRES_OWN_AUTHORIZATION');assert.equal(p.dispatch_authorized,false);
});
test('GB-025 unknown or mismatched claim status fails closed',()=>{
  for(const existing_attempt of [{mission_id:'OTHER-PROJECT',state:'UNCERTAIN'}, {mission_id:task().mission_id,state:'FAILED'}, {mission_id:task().mission_id,state:'NOT_STARTED',authorized:true}]) {
    assert.equal(plan([cap('connected_read')],{existing_attempt}).reason,'EXISTING_ATTEMPT_UNVERIFIED');
  }
});
test('GB-111 source/scope/data contract rejects extra fields and cross-project records',()=>{
  for(const update of [{project_id:'JCT'},{credentials:'SENSITIVE'},{classification:'PRIVATE'},{kind:'unknown'}]) {
    const p=plan([cap('public_browser')],{task:{...task(),...update}});
    assert.equal(p.status,'HOLD');assert.equal(p.reason,'CLOSED_ROUTE_INPUT_REQUIRED');
  }
});
test('GB-111 unknown capability, cross-project capability or unapproved kind fails closed',()=>{
  for(const c of [cap('gemini_web'),cap('connected_read',{project_id:'JCT'}),cap('connected_read',{secret:'NOT_ALLOWED'}),cap('connected_read',{pricing:'FREE_ASSUMED'})]){
    assert.equal(plan([c]).reason,'CLOSED_ROUTE_INPUT_REQUIRED');
  }
});
test('GB-111 pure planning never calls browser, connector or provider',()=>{
  let calls=0;
  const c=cap('connected_read');c.execute=()=>{calls++;};
  assert.equal(plan([c]).reason,'CLOSED_ROUTE_INPUT_REQUIRED');
  assert.equal(calls,0);
});
