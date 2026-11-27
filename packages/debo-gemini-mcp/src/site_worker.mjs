// Owner-private verification adapter. Sites dispatch supplies both identity
// headers. The owner email is configured as a private runtime value; actual
// receipt ownership always uses the Site-scoped user ID, never an email key.
import bridge from './mcp_worker.mjs';
import { sha256 } from './synthetic_contract.mjs';

function response(body, status = 200, type = 'application/json; charset=utf-8', extra = {}) {
  return new Response(typeof body === 'string' ? body : JSON.stringify(body), { status, headers: {
    'content-type': type, 'cache-control': 'no-store', 'x-content-type-options': 'nosniff',
    'referrer-policy': 'no-referrer', ...extra
  } });
}
function identity(request, env) {
  if (env?.DEBO_BRIDGE_MODE !== 'synthetic_only' || env?.DEBO_IDENTITY_BOUNDARY !== 'sites_dispatch' || env?.DEBO_ENABLE_LIVE_GEMINI !== 'false' || typeof env?.DEBO_OWNER_EMAIL !== 'string' || !env.DEBO_OWNER_EMAIL.includes('@')) return { status: 503 };
  const id = request.headers.get('oai-authenticated-user-id');
  const email = request.headers.get('oai-authenticated-user-email');
  if (!id || !email) return { status: 401 };
  if (id.length > 256 || email.trim().toLowerCase() !== env.DEBO_OWNER_EMAIL.trim().toLowerCase()) return { status: 403 };
  return { id };
}
function page(nonce) {
  return `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DEBO Bridge Verification</title>
<style nonce="${nonce}">:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#101722;color:#edf4ff}body{max-width:760px;margin:auto;padding:28px 18px;line-height:1.6}h1{font-size:1.6rem}p{color:#ccd8e8}button{padding:14px 18px;margin:8px 8px 8px 0;background:#b8ebce;color:#092518;border:0;border-radius:10px;font:inherit;font-weight:650;cursor:pointer}button:disabled{opacity:.5;cursor:wait}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1a2637;border-radius:12px;padding:18px;font-size:14px}small{color:#bdd0e7}.tag{color:#b8ebce}</style>
<h1>DEBO Bridge Verification</h1><p class="tag">Owner-private · Synthetic samples · Gemini disabled</p><p>Check the signed-in caller and save one fixed test receipt. Replaying the request must return the same receipt.</p><p id="runtime">Checking identity…</p><button id="run" type="button">Run verification</button><button id="read" type="button">Read saved receipt</button><pre id="result" aria-live="polite">Ready.</pre><small>This page performs no Gemini calls. It accepts no private records, prompts, API keys or paid operations.</small>
<script nonce="${nonce}">
const result=document.querySelector('#result'),runtime=document.querySelector('#runtime'),run=document.querySelector('#run'),read=document.querySelector('#read');
const args={project_id:'DEBO-CORE',idempotency_key:'private-runtime-verification-v1',fixture_id:'bridge-health-v1'};
async function who(headers){const r=await fetch('/api/identity',{credentials:'same-origin',cache:'no-store',headers:headers||{}});return {status:r.status,data:await r.json()};}
async function tool(name,input){const r=await fetch('/api/fixture',{method:'POST',credentials:'same-origin',headers:{'content-type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name,arguments:input}})});if(!(r.headers.get('content-type')||'').toLowerCase().includes('application/json'))throw Error('Verification returned a non-JSON response (HTTP '+r.status+'). Reload this page and retry.');let rpc;try{rpc=await r.json();}catch{throw Error('Verification returned invalid JSON (HTTP '+r.status+').');}if(typeof rpc?.result?.content?.[0]?.text!=='string')throw Error('Verification request failed (HTTP '+r.status+').');let value;try{value=JSON.parse(rpc.result.content[0].text);}catch{throw Error('Verification tool returned invalid JSON.');}return {isError:rpc.result.isError,value};}
async function readSaved(){const me=await who();if(me.status!==200)throw Error('Owner authentication failed');const r=await tool('debo_get_receipt',{project_id:args.project_id,idempotency_key:args.idempotency_key});if(r.isError)throw Error(JSON.stringify(r.value));return {revision:me.data.revision,caller_sha256:me.data.caller_sha256,...r.value};}
async function verify(){const me=await who();if(me.status!==200)throw Error('Owner authentication failed');const a=await tool('debo_gemini_execute',args);const b=await tool('debo_gemini_execute',args);if(a.isError||b.isError)throw Error(JSON.stringify({a,b}));const forbidden=await tool('debo_gemini_execute',{...args,project_id:'JCT'});const injection=await tool('debo_gemini_execute',{...args,payload:'not accepted'});const canary=await who({'oai-authenticated-user-id':'forged-synthetic-caller'});const checks={authenticated_owner:me.data.verified_owner===true,replay_identical:b.value.deduplicated===true&&a.value.receipt.receipt_sha256===b.value.receipt.receipt_sha256,cross_project_denied:forbidden.isError&&forbidden.value.error.code==='SCOPE_DENIED',extra_payload_denied:injection.isError&&injection.value.error.code==='BAD_REQUEST',forged_identity_header_rejected_or_overwritten:[401,403].includes(canary.status)||(canary.status===200&&canary.data.caller_sha256===me.data.caller_sha256),zero_provider_calls:a.value.receipt.network_calls===0&&a.value.receipt.actual_cost_usd===0};return {status:Object.values(checks).every(Boolean)?'PASS':'FAIL',revision:me.data.revision,checks,receipt:a.value.receipt};}
async function perform(fn){run.disabled=read.disabled=true;result.textContent='Checking…';try{result.textContent=JSON.stringify(await fn(),null,2);}catch(e){result.textContent=JSON.stringify({status:'ERROR',message:e.message},null,2);}finally{run.disabled=read.disabled=false;}}
run.addEventListener('click',()=>perform(verify));read.addEventListener('click',()=>perform(readSaved));who().then(r=>{runtime.textContent=r.status===200?'Authenticated owner · Runtime '+r.data.revision:'Owner sign-in required ('+r.status+')';}).catch(()=>{runtime.textContent='Identity check unavailable';});
</script></html>`;
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.protocol !== 'https:' || url.search || url.hash) return response({ error: 'Invalid URL' }, 400);
    const caller = identity(request, env);
    if (!caller.id) return response({ error: caller.status === 503 ? 'Runtime not configured' : 'Owner authentication required' }, caller.status);
    const revision = /^[A-Z0-9_-]{1,40}$/.test(env.DEBO_VERIFICATION_REVISION ?? '') ? env.DEBO_VERIFICATION_REVISION : 'UNSET';
    if (url.pathname === '/mcp' || url.pathname === '/api/fixture') {
      const scoped = { ...env, DEBO_CALLER_PROJECT_ACL: JSON.stringify({ [caller.id]: ['DEBO-CORE'] }) };
      // The browser uses an authenticated Site API route. Keep /mcp for the
      // platform's plugin transport, then reuse the same handler internally.
      const internalUrl = new URL(request.url);
      internalUrl.pathname = '/mcp';
      return bridge.fetch(new Request(internalUrl, request), scoped);
    }
    if (request.method !== 'GET') return response({ error: 'Method not allowed' }, 405);
    if (url.pathname === '/api/identity') return response({ verified_owner: true, caller_sha256: await sha256(caller.id), revision, project_id: 'DEBO-CORE', provider: 'disabled' });
    if (url.pathname === '/') {
      const nonce = crypto.randomUUID().replaceAll('-', '');
      return response(page(nonce), 200, 'text/html; charset=utf-8', { 'content-security-policy': `default-src 'none'; script-src 'nonce-${nonce}'; style-src 'nonce-${nonce}'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'self' https://chatgpt.com` });
    }
    return response({ error: 'Not found' }, 404);
  }
};
