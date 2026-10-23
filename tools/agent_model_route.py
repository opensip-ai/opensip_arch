#!/usr/bin/env python3
"""Validate and launch OpenSIP agents against a plan's capability route."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class AgentSpec:
    model: str
    effort: str


ROUTES: dict[str, dict[str, AgentSpec]] = {
    "R0-MECHANICAL": {
        "codex": AgentSpec("gpt-6-luna", "low"),
        "claude": AgentSpec("claude-haiku-5-5", "medium"),
    },
    "R1-BALANCED": {
        "codex": AgentSpec("gpt-6.1-sol", "medium"),
        "claude": AgentSpec("claude-sonnet-5-5", "high"),
    },
    "R2-DEEP": {
        "codex": AgentSpec("gpt-6.1-sol", "high"),
        "claude": AgentSpec("claude-opus-5-5", "medium"),
    },
    "R3-FRONTIER": {
        "codex": AgentSpec("gpt-6-astra", "high"),
        "claude": AgentSpec("claude-opus-5-5", "high"),
    },
    "R4-EXCEPTIONAL": {
        "codex": AgentSpec("gpt-6-astra", "xhigh"),
        "claude": AgentSpec("claude-fable-5-1", "high"),
    },
}

EFFORTS = {"low", "medium", "high", "xhigh", "max"}
FIELD_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?([^:*]+?)(?:\*\*)?\s*:\s*(.*?)\s*$"
)


class RouteError(ValueError):
    """The plan does not contain a usable or consistent route declaration."""


def _clean(value: str) -> str:
    return value.strip().strip("`").strip()


def _fields(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if match:
            key = match.group(1).strip().lower()
            if key in result and key in {
                "capability route", "codex", "claude", "claude long-horizon lead",
                "longhorizonlead", "exceptional authorization",
            }:
                raise RouteError(f"duplicate route field: {match.group(1).strip()}")
            result[key] = _clean(match.group(2))
    return result


def _parse_spec(value: str, label: str) -> AgentSpec:
    parts = [_clean(part) for part in value.split("/")]
    if len(parts) != 2 or not all(parts):
        raise RouteError(f"{label} must be '<exact-model> / <effort>'")
    if parts[1] not in EFFORTS:
        raise RouteError(f"{label} has unsupported effort {parts[1]!r}")
    return AgentSpec(*parts)


def _validate_declared(
    route: str,
    provider: str,
    spec: AgentSpec,
    long_horizon: bool,
    exceptional_authorization: str,
) -> None:
    expected = ROUTES[route][provider]
    allowed = {expected}
    if route == "R0-MECHANICAL" and provider == "codex":
        allowed.add(AgentSpec("gpt-6-luna", "medium"))
    if route == "R1-BALANCED" and provider == "claude" and long_horizon:
        allowed.add(AgentSpec("claude-opus-5-5", "medium"))
    if route == "R2-DEEP" and provider == "claude":
        allowed.add(AgentSpec("claude-opus-5-5", "high"))
    if route == "R3-FRONTIER" and provider == "claude":
        allowed.add(AgentSpec("claude-fable-5-1", "high"))
    if route == "R4-EXCEPTIONAL":
        allowed.add(AgentSpec(expected.model, "max"))
    if spec.effort == "max" and (
        not exceptional_authorization
        or exceptional_authorization.startswith("<")
    ):
        raise RouteError("max effort requires an Exceptional authorization owner-decision reference")
    if spec not in allowed:
        choices = ", ".join(f"{item.model}/{item.effort}" for item in sorted(allowed, key=lambda x: (x.model, x.effort)))
        raise RouteError(
            f"plan declares {provider} {spec.model}/{spec.effort}, but {route} allows {choices}"
        )


def spec_from_plan(path: Path, provider: str) -> tuple[str, AgentSpec]:
    fields = _fields(path.read_text(encoding="utf-8"))
    route = _clean(fields.get("capability route", ""))
    if route not in ROUTES:
        raise RouteError(f"missing or unknown Capability route in {path}: {route!r}")

    raw_long_horizon = fields.get("longhorizonlead", "false").split(";", 1)[0].strip().lower()
    if raw_long_horizon not in {"true", "false"}:
        raise RouteError("longHorizonLead must begin with true or false")
    long_horizon = raw_long_horizon == "true"
    exceptional_authorization = fields.get("exceptional authorization", "")

    label = provider
    if provider == "claude" and long_horizon:
        label = "claude long-horizon lead"
    if label not in fields:
        raise RouteError(f"missing {label.title()} route in {path}")
    spec = _parse_spec(fields[label], label.title())
    _validate_declared(
        route, provider, spec, long_horizon, exceptional_authorization
    )
    return route, spec


def resolve(args: argparse.Namespace) -> tuple[str, AgentSpec]:
    if bool(args.plan) == bool(args.route):
        raise RouteError("select exactly one of --plan or --route")
    if args.plan:
        return spec_from_plan(Path(args.plan).expanduser().resolve(), args.provider)
    if args.route not in ROUTES:
        raise RouteError(f"unknown route: {args.route!r}")
    return args.route, ROUTES[args.route][args.provider]


def session_values(args: argparse.Namespace) -> tuple[str | None, str | None, str | None, str | None]:
    return (
        args.session_route or os.environ.get("OPENSIP_AGENT_ROUTE"),
        args.session_provider or os.environ.get("OPENSIP_AGENT_PROVIDER"),
        args.session_model or os.environ.get("OPENSIP_AGENT_MODEL"),
        args.session_effort or os.environ.get("OPENSIP_AGENT_EFFORT"),
    )


def agent_argv(provider: str, spec: AgentSpec, cwd: Path, extra: Sequence[str]) -> list[str]:
    if provider == "codex":
        return [
            "codex", "--model", spec.model,
            "--config", f"model_reasoning_effort={spec.effort}",
            "--cd", str(cwd), *extra,
        ]
    return ["claude", "--model", spec.model, "--effort", spec.effort, *extra]


def route_env(route: str, provider: str, spec: AgentSpec) -> dict[str, str]:
    return {
        "OPENSIP_AGENT_ROUTE": route,
        "OPENSIP_AGENT_PROVIDER": provider,
        "OPENSIP_AGENT_MODEL": spec.model,
        "OPENSIP_AGENT_EFFORT": spec.effort,
    }


def print_direct_command(route: str, provider: str, spec: AgentSpec, cwd: Path, extra: Sequence[str]) -> None:
    assignments = [f"{key}={shlex.quote(value)}" for key, value in route_env(route, provider, spec).items()]
    command = [*assignments, *[shlex.quote(item) for item in agent_argv(provider, spec, cwd, extra)]]
    print(" ".join(command))


def router_launch_argv(args: argparse.Namespace) -> list[str]:
    source = ["--plan", str(Path(args.plan).expanduser().resolve())] if args.plan else ["--route", args.route]
    return [
        "python3", "-I", "-B", str(Path(__file__).resolve()), "launch",
        "--provider", args.provider, *source, "--cwd", str(Path(args.cwd).resolve()),
    ]


def run_check(args: argparse.Namespace) -> int:
    route, spec = resolve(args)
    actual_route, actual_provider, actual_model, actual_effort = session_values(args)
    expected = (route, args.provider, spec.model, spec.effort)
    actual = (actual_route, actual_provider, actual_model, actual_effort)
    if actual == expected:
        print(f"ROUTE-OK {route} {args.provider} {spec.model}/{spec.effort}")
        return 0

    labels = ("route", "provider", "model", "effort")
    differences = [
        f"{label}: expected {wanted!r}, got {found!r}"
        for label, wanted, found in zip(labels, expected, actual)
        if wanted != found
    ]
    print("ROUTE-MISMATCH " + "; ".join(differences), file=sys.stderr)
    print("After writing the required handoff and ending this agent, run:", file=sys.stderr)
    print(shlex.join(router_launch_argv(args)), file=sys.stderr)
    return 2


def run_launch(args: argparse.Namespace) -> int:
    route, spec = resolve(args)
    cwd = Path(args.cwd).expanduser().resolve()
    argv = agent_argv(args.provider, spec, cwd, args.agent_args)
    if args.dry_run:
        print_direct_command(route, args.provider, spec, cwd, args.agent_args)
        return 0
    env = os.environ.copy()
    env.update(route_env(route, args.provider, spec))
    os.chdir(cwd)
    os.execvpe(argv[0], argv, env)
    return 127


def run_spawn(args: argparse.Namespace) -> int:
    route, spec = resolve(args)
    cwd = Path(args.cwd).expanduser().resolve()
    env = route_env(route, args.provider, spec)
    setup = "cd " + shlex.quote(str(cwd)) + " && export " + " ".join(
        f"{key}={shlex.quote(value)}" for key, value in env.items()
    )
    native_args = agent_argv(args.provider, spec, cwd, args.agent_args)[1:]
    setup_cmd = ["herdr", "pane", "run", args.pane, setup]
    start_cmd = [
        "herdr", "agent", "start", args.name,
        "--kind", args.provider, "--pane", args.pane, "--", *native_args,
    ]
    if args.dry_run:
        print(shlex.join(setup_cmd))
        print(shlex.join(start_cmd))
        return 0
    if os.environ.get("HERDR_ENV") != "1":
        raise RouteError("spawn requires HERDR_ENV=1; use launch from an ordinary shell")
    subprocess.run(setup_cmd, check=True)
    subprocess.run(start_cmd, check=True)
    return 0


def add_route_source(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--provider", required=True, choices=("codex", "claude"))
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--plan", help="plan containing the exact route block")
    source.add_argument("--route", choices=tuple(ROUTES), help="explicit route for a frozen plan")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="compare the plan route with this session")
    add_route_source(check)
    check.add_argument("--cwd", default=os.getcwd())
    check.add_argument("--session-route")
    check.add_argument("--session-provider", choices=("codex", "claude"))
    check.add_argument("--session-model")
    check.add_argument("--session-effort", choices=tuple(sorted(EFFORTS)))
    check.set_defaults(func=run_check)

    launch = subparsers.add_parser("launch", help="replace this shell with a routed agent")
    add_route_source(launch)
    launch.add_argument("--cwd", default=os.getcwd())
    launch.add_argument("--dry-run", action="store_true")
    launch.add_argument("agent_args", nargs=argparse.REMAINDER)
    launch.set_defaults(func=run_launch)

    spawn = subparsers.add_parser("spawn", help="start a routed agent in an available Herdr pane")
    add_route_source(spawn)
    spawn.add_argument("--pane", required=True)
    spawn.add_argument("--name", required=True)
    spawn.add_argument("--cwd", default=os.getcwd())
    spawn.add_argument("--dry-run", action="store_true")
    spawn.add_argument("agent_args", nargs=argparse.REMAINDER)
    spawn.set_defaults(func=run_spawn)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "agent_args", None) and args.agent_args[0] == "--":
        args.agent_args = args.agent_args[1:]
    try:
        return args.func(args)
    except (OSError, RouteError, subprocess.CalledProcessError) as error:
        print(f"route error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
