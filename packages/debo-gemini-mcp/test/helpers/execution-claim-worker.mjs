import { parentPort, workerData } from 'node:worker_threads';
import { D1ExecutionGate } from '../../src/durable_execution_gate.mjs';
import { executionD1, executionContext, executionInput, executionResult } from './execution-fixtures.mjs';
const local = executionD1(workerData.path, false);
try {
  const gate = new D1ExecutionGate(local.binding, executionContext);
  const answer = await gate.claim(executionInput);
  if (answer.status === 'CLAIMED') await gate.complete(answer.claim, executionResult);
  parentPort.postMessage({ won: answer.status === 'CLAIMED' });
} finally { local.close(); }
