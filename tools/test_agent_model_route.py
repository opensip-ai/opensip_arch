#!/usr/bin/env python3
"""Regression tests for the OpenSIP agent model router."""

from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("agent_model_route.py")
SPEC = importlib.util.spec_from_file_location("agent_model_route", MODULE_PATH)
assert SPEC and SPEC.loader
ROUTER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ROUTER
SPEC.loader.exec_module(ROUTER)


def plan(route: str = "R1-BALANCED", long_horizon: str = "false") -> str:
    claude = "claude-opus-5-5 / medium" if long_horizon == "true" else "claude-sonnet-5-5 / high"
    return f"""# Unit plan

Capability route: {route}
Codex: gpt-6.1-sol / medium
Claude: claude-sonnet-5-5 / high
Claude long-horizon lead: claude-opus-5-5 / medium
longHorizonLead: {long_horizon}; test reason
Escalate when: a named control fails
Escalation route: R2-DEEP
Independent review: different vendor; R1-BALANCED
De-escalate when: the control passes
"""


class RouterTests(unittest.TestCase):
    def write_plan(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "PLAN.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_balanced_codex(self) -> None:
        route, spec = ROUTER.spec_from_plan(self.write_plan(plan()), "codex")
        self.assertEqual(route, "R1-BALANCED")
        self.assertEqual(spec, ROUTER.AgentSpec("gpt-6.1-sol", "medium"))

    def test_long_horizon_claude(self) -> None:
        route, spec = ROUTER.spec_from_plan(self.write_plan(plan(long_horizon="true")), "claude")
        self.assertEqual(route, "R1-BALANCED")
        self.assertEqual(spec, ROUTER.AgentSpec("claude-opus-5-5", "medium"))

    def test_documented_claude_fallback_is_allowed(self) -> None:
        text = plan(route="R1-BALANCED").replace(
            "Capability route: R1-BALANCED", "Capability route: R3-FRONTIER"
        ).replace("Claude: claude-sonnet-5-5 / high", "Claude: claude-fable-5-1 / high")
        route, spec = ROUTER.spec_from_plan(self.write_plan(text), "claude")
        self.assertEqual(route, "R3-FRONTIER")
        self.assertEqual(spec, ROUTER.AgentSpec("claude-fable-5-1", "high"))

    def test_max_requires_owner_authorization(self) -> None:
        text = plan().replace("Capability route: R1-BALANCED", "Capability route: R4-EXCEPTIONAL")
        text = text.replace("Codex: gpt-6.1-sol / medium", "Codex: gpt-6-astra / max")
        path = self.write_plan(text)
        with self.assertRaisesRegex(ROUTER.RouteError, "Exceptional authorization"):
            ROUTER.spec_from_plan(path, "codex")
        path.write_text(text + "Exceptional authorization: owner decision D-999\n", encoding="utf-8")
        route, spec = ROUTER.spec_from_plan(path, "codex")
        self.assertEqual(route, "R4-EXCEPTIONAL")
        self.assertEqual(spec, ROUTER.AgentSpec("gpt-6-astra", "max"))

    def test_route_inconsistency_is_rejected(self) -> None:
        path = self.write_plan(plan().replace("gpt-6.1-sol / medium", "gpt-6-astra / high", 1))
        with self.assertRaisesRegex(ROUTER.RouteError, "allows"):
            ROUTER.spec_from_plan(path, "codex")

    def test_missing_route_is_rejected(self) -> None:
        path = self.write_plan("Codex: gpt-6.1-sol / medium\n")
        with self.assertRaisesRegex(ROUTER.RouteError, "Capability route"):
            ROUTER.spec_from_plan(path, "codex")

    def test_duplicate_route_is_rejected(self) -> None:
        path = self.write_plan(plan() + "\nCapability route: R2-DEEP\n")
        with self.assertRaisesRegex(ROUTER.RouteError, "duplicate route field"):
            ROUTER.spec_from_plan(path, "codex")

    def test_check_accepts_exact_session(self) -> None:
        args = ROUTER.build_parser().parse_args([
            "check", "--provider", "codex", "--plan", str(self.write_plan(plan())),
            "--session-route", "R1-BALANCED", "--session-provider", "codex",
            "--session-model", "gpt-6.1-sol", "--session-effort", "medium",
        ])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(ROUTER.run_check(args), 0)
        self.assertIn("ROUTE-OK", output.getvalue())

    def test_check_fails_closed_without_session_metadata(self) -> None:
        args = ROUTER.build_parser().parse_args([
            "check", "--provider", "claude", "--plan", str(self.write_plan(plan())),
        ])
        error = io.StringIO()
        with contextlib.redirect_stderr(error), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ROUTER.run_check(args), 2)
        self.assertIn("ROUTE-MISMATCH", error.getvalue())
        self.assertIn("agent_model_route.py launch", error.getvalue())

    def test_dry_run_launch_pins_codex_model_and_effort(self) -> None:
        args = ROUTER.build_parser().parse_args([
            "launch", "--provider", "codex", "--route", "R2-DEEP", "--dry-run",
        ])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(ROUTER.run_launch(args), 0)
        command = output.getvalue()
        self.assertIn("OPENSIP_AGENT_ROUTE=R2-DEEP", command)
        self.assertIn("--model gpt-6.1-sol", command)
        self.assertIn("model_reasoning_effort=high", command)

    def test_dry_run_spawn_pins_claude_model_and_effort(self) -> None:
        args = ROUTER.build_parser().parse_args([
            "spawn", "--provider", "claude", "--route", "R3-FRONTIER",
            "--pane", "w1:p9", "--name", "deep_reviewer", "--dry-run",
        ])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(ROUTER.run_spawn(args), 0)
        commands = output.getvalue()
        self.assertIn("herdr pane run w1:p9", commands)
        self.assertIn("--model claude-opus-5-5 --effort high", commands)


if __name__ == "__main__":
    unittest.main()
