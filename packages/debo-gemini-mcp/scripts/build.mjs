import { mkdir, copyFile, readFile, writeFile, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';

const root = fileURLToPath(new URL('../', import.meta.url));
const target = new URL('../dist/server/', import.meta.url);
await rm(new URL('../dist/', import.meta.url), { recursive: true, force: true });
await mkdir(target, { recursive: true });
const files = [
  ['src/mcp_worker.mjs', 'index.js'],
  ['src/contracts.mjs', 'contracts.mjs'],
  ['src/synthetic_contract.mjs', 'synthetic_contract.mjs'],
  ['src/d1_store.mjs', 'd1_store.mjs']
];
const hashes = {};
for (const [source, destination] of files) {
  const bytes = await readFile(new URL(`../${source}`, import.meta.url));
  // The Worker module graph must stay independent of Node and provider SDKs.
  const imports = [...bytes.toString('utf8').matchAll(/\b(?:import|export)\s+(?:[^'";]*?\s+from\s+)?['"]([^'"]+)['"]/g)].map(m => m[1]);
  if (imports.some(specifier => !['./contracts.mjs', './synthetic_contract.mjs', './d1_store.mjs'].includes(specifier))) throw new Error(`Unapproved Worker import in ${source}`);
  if (/\b(?:fetch\s*\(|XMLHttpRequest\b|WebSocket\b|import\s*\()/.test(bytes.toString('utf8').replace('async fetch(request, env)', 'async handler(request, env)'))) throw new Error(`Unexpected outbound API or dynamic import in ${source}`);
  const output = new URL(destination, target);
  await copyFile(new URL(`../${source}`, import.meta.url), output);
  const check = spawnSync(process.execPath, ['--check', fileURLToPath(output)], { cwd: root, encoding: 'utf8' });
  if (check.status !== 0) throw new Error(check.stderr);
  hashes[`server/${destination}`] = createHash('sha256').update(bytes).digest('hex');
}
await writeFile(new URL('../dist/build-manifest.json', import.meta.url), JSON.stringify({ status: 'BUILT_LOCAL_ONLY', entrypoint: 'server/index.js', files: hashes }, null, 2) + '\n');
console.log(`Validated ${files.length} Worker modules; local artifact: dist/server/index.js`);
