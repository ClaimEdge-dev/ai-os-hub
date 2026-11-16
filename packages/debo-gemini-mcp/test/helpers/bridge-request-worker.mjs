import { parentPort, workerData } from 'node:worker_threads';
import worker from '../../src/mcp_worker.mjs';
import { sqliteD1, testEnvironment, callTool } from './sqlite-d1.mjs';

const local = sqliteD1(workerData.path, false);
try {
  const result = await callTool(worker, testEnvironment(local.binding), workerData.tool, workerData.args);
  parentPort.postMessage({ status: result.response.status, rpc: result.rpc, value: result.value });
} finally { local.close(); }
