"""R153: synthetic tests for optional Codex lifecycle hooks.

No live Codex, external connector, owner permission, or paid service required.
"""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import debo_codex_hook as hooks


class PreToolUseTests(unittest.TestCase):
    def event(self, tool="Bash", command="python -m unittest"):
        return {"hook_event_name": "PreToolUse", "tool_name": tool,
                "tool_input": {"command": command}}

    def assert_denied(self, event):
        result = hooks.pre_tool_use(event)
        self.assertEqual(
            result["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(result["hookSpecificOutput"]["hookEventName"], "PreToolUse")
        self.assertNotIn("updatedInput", result["hookSpecificOutput"])

    def test_safe_unit_test_does_not_grant_approval(self):
        self.assertEqual(hooks.pre_tool_use(self.event()), {})

    def test_safe_pull_request_create_is_not_promoted_to_merging(self):
        event = {"hook_event_name": "PreToolUse",
                 "tool_name": "mcp__GitHub__create_pull_request",
                 "tool_input": {"draft": True}}
        self.assertEqual(hooks.pre_tool_use(event), {})

    def test_protects_direct_shell_actions(self):
        for command in [
            "rm -rf /important",
            "git push origin main",
            "git push --force origin feature",
            "gh pr merge 54 --merge",
            "gh repo delete sample",
            "gh release create v1",
            "vercel --prod",
            "npm publish",
            "terraform destroy",
            "kubectl delete secret example",
            "echo ok && gh pr merge 51",
        ]:
            with self.subTest(command=command):
                self.assert_denied(self.event(command=command))

    def test_protects_connected_merge_or_send(self):
        for name in ("mcp__GitHub__merge_pull_request",
                     "mcp__Gmail__send_email",
                     "mcp__GitHub__delete_file",
                     "mcp__GitHub__enable_auto_merge"):
            with self.subTest(tool=name):
                self.assert_denied(
                    {"hook_event_name": "PreToolUse",
                     "tool_name": name, "tool_input": {"id": "synthetic"}})

    def test_bash_requires_inspectable_string(self):
        self.assert_denied(self.event(command=None))

    def test_missing_tool_identity_denied(self):
        self.assert_denied({"hook_event_name": "PreToolUse",
                            "tool_input": {}})

    def test_mismatched_event_denied(self):
        self.assert_denied({"hook_event_name": "SomethingElse",
                            "tool_name": "Bash",
                            "tool_input": {"command": "echo hi"}})


class SessionStartTests(unittest.TestCase):
    def event(self):
        return {"hook_event_name": "SessionStart", "source": "startup"}

    def test_reads_canonical_rendered_rules_and_freshness(self):
        text = "## Golden rules\n1. Resume work\n## Next\nSafe"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "governance/runtime-briefs/DEBO.md"
            path.parent.mkdir(parents=True)
            path.write_text(text, encoding="utf-8")
            with mock.patch.object(hooks, "ROOT", root), \
                 mock.patch.object(hooks, "render_brief", return_value=text), \
                 mock.patch.dict(os.environ, {"DEBO_PROJECT_ID": "DEBO"}):
                result = hooks.session_start(self.event())
        ctx = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("MATCHES_GENERATED_SOURCE", ctx)
        self.assertIn("Resume work", ctx)
        self.assertIn("private checkpoint", ctx)
        self.assertLessEqual(len(ctx), hooks.CONTEXT_LIMIT)

    def test_stale_brief_is_not_called_current(self):
        text = "## Golden rules\n1. Keep canon\n## Next\nSafe"
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(hooks, "ROOT", Path(tmp)), \
                 mock.patch.object(hooks, "render_brief", return_value=text):
                result = hooks.session_start(self.event())
        self.assertIn("STALE_OR_MISSING",
                      result["hookSpecificOutput"]["additionalContext"])

    def test_unknown_project_does_not_load_fallback(self):
        with mock.patch.dict(os.environ, {"DEBO_PROJECT_ID": "NOT_A_PROJECT"}):
            result = hooks.session_start(self.event())
        self.assertIn("unsupported project", result["systemMessage"])

    def test_missing_canon_does_not_claim_success(self):
        with mock.patch.object(hooks, "render_brief",
                               side_effect=ValueError("private diagnostic")):
            result = hooks.session_start(self.event())
        self.assertIn("unavailable", result["systemMessage"])
        self.assertNotIn("private diagnostic", json.dumps(result))

    def test_wrong_event_gives_warning(self):
        self.assertIn("mismatch",
                      hooks.session_start({"hook_event_name": "Stop"})
                      ["systemMessage"])


class PostToolUseTests(unittest.TestCase):
    def test_failure_recommends_bounded_recovery_without_leak(self):
        result = hooks.post_tool_use({
            "hook_event_name": "PostToolUse",
            "tool_response": {"exit_code": 1, "stderr": "SECRET=synthetic"}})
        text = json.dumps(result)
        self.assertIn("one distinct authorized recovery", text)
        self.assertNotIn("SECRET=", text)

    def test_success_no_extra_claim(self):
        result = hooks.post_tool_use({
            "hook_event_name": "PostToolUse",
            "tool_response": {"exit_code": 0}})
        self.assertEqual(result, {})

    def test_non_dictionary_response_is_safe(self):
        result = hooks.post_tool_use({
            "hook_event_name": "PostToolUse",
            "tool_response": "arbitrary output"})
        self.assertEqual(result, {})


class ConfigurationTests(unittest.TestCase):
    def test_hook_config_is_json_and_bounded(self):
        path = Path(__file__).resolve().parents[1] / ".codex/hooks.json"
        conf = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(conf["hooks"]),
                         {"SessionStart", "PreToolUse", "PostToolUse"})
        for groups in conf["hooks"].values():
            for group in groups:
                for item in group["hooks"]:
                    self.assertLessEqual(item["timeout"], 12)
                    self.assertIn("debo_codex_hook.py", item["command"])
                    self.assertNotIn("--dangerously-bypass-hook-trust",
                                     item["command"])

    def test_malformed_input_to_cli_fails_closed_for_pretool(self):
        with mock.patch.object(sys, "stdin", io.StringIO("{not-json")), \
             mock.patch.object(sys, "stdout", new_callable=io.StringIO) as output:
            self.assertEqual(hooks.main(["pre-tool-use"]), 0)
            result = json.loads(output.getvalue())
        self.assertEqual(
            result["hookSpecificOutput"]["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
