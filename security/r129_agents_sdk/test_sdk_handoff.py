"""An ACTUAL Agents SDK runner/handoff test with scripted models and no API calls.

This verifies SDK agent handoff mechanics, not a model's intelligence,
production agent installation, connected tool authorization, or billing.
Run only inside the separate pinned-dependency GitHub pilot job.
"""
import os
os.environ["OPENAI_AGENTS_DISABLE_TRACING"]="1"

import unittest
from agents import Agent, RunConfig, Runner
from agents.testing import ScriptedModel, assistant_message, function_call


class AgentSDKHandoffPilot(unittest.IsolatedAsyncioTestCase):
    async def test_mack_to_forge_to_proof(self):
        mack_model=ScriptedModel([
            [function_call("transfer_to_forge", {}, call_id="handoff_mack_forge")]
        ])
        forge_model=ScriptedModel([
            [function_call("transfer_to_proof", {}, call_id="handoff_forge_proof")]
        ])
        proof_model=ScriptedModel([
            [assistant_message("SYNTHETIC_PASS: source-only handoff examined")]
        ])
        proof=Agent(name="Proof", model=proof_model)
        forge=Agent(name="Forge", model=forge_model, handoffs=[proof])
        mack=Agent(name="Mack", model=mack_model, handoffs=[forge])
        result=await Runner.run(
            mack,
            "Synthetic, no customer data, no production changes: route to Forge then Proof.",
            run_config=RunConfig(tracing_disabled=True),
        )
        self.assertEqual(result.last_agent.name,"Proof")
        self.assertEqual(result.final_output,"SYNTHETIC_PASS: source-only handoff examined")
        self.assertEqual(len(mack_model.calls),1)
        self.assertEqual(len(forge_model.calls),1)
        self.assertEqual(len(proof_model.calls),1)
        for model in (mack_model,forge_model,proof_model):
            model.assert_complete()

    async def test_model_drift_is_detected(self):
        model=ScriptedModel([[assistant_message("Synthetic pass")]])
        agent=Agent(name="Proof",model=model)
        result=await Runner.run(agent,"Run no external actions",run_config=RunConfig(tracing_disabled=True))
        self.assertEqual(result.final_output,"Synthetic pass")
        model.assert_complete()


if __name__=="__main__":
    unittest.main()
