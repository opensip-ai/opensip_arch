#!/usr/bin/env python3
"""Subprocess runner for safety-38 DeTable probes. Does not touch the root probe."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-implementation/m2-grok-toml-safety-38")
PROBE = ROOT / "probe"
BIN = PROBE / "target/debug/opensip-private-toml-safety-38"
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
OUT = ROOT / "results"

CASES = [
    ("nested-array-80", None, 30),
    ("nested-array-81", None, 30),
    ("nested-inline-80", None, 30),
    ("nested-inline-81", None, 30),
    ("dotted-80", None, 30),
    ("dotted-81", None, 30),
    ("std-table-chain-80", None, 30),
    ("std-table-chain-81", None, 30),
    ("array-table-chain-80", None, 30),
    ("array-table-chain-81", None, 30),
    ("unclosed-array-80", None, 30),
    ("unclosed-array-200", None, 30),
    ("unclosed-array-10000", None, 30),
    ("sibling-tables-1000", None, 30),
    ("mixed-80-80", None, 30),
    ("invalid-duplicate-table", None, 30),
    ("invalid-unclosed-inline", None, 30),
    ("invalid-trailing-junk", None, 30),
    ("empty", None, 30),
    ("nested-array-80", 524288, 30),
    ("nested-array-81", 524288, 30),
    ("std-table-chain-80", 524288, 30),
    ("mixed-80-80", 524288, 30),
    ("four-mib-open-brackets", None, 60),
    ("four-mib-open-brackets", 524288, 60),
    ("four-mib-sibling-tables", None, 120),
    ("four-mib-sibling-tables", 524288, 120),
    ("nested-array-80", 65536, 30),
    ("mixed-80-80", 65536, 30),
]


def run(cmd, timeout, cwd=None, env=None):
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "cmd": cmd,
            "timeout_s": timeout,
            "returncode": p.returncode,
            "stdout": p.stdout[-8000:],
            "stderr": p.stderr[-8000:],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
        return {
            "cmd": cmd,
            "timeout_s": timeout,
            "returncode": None,
            "stdout": (out or "")[-8000:],
            "stderr": (err or "")[-8000:],
            "timed_out": True,
        }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["CARGO_TERM_COLOR"] = "never"
    build = run(
        [CARGO, "build", "--offline", "--locked", "-q"],
        timeout=180,
        cwd=PROBE,
        env=env,
    )
    (OUT / "build.json").write_text(json.dumps(build, indent=2) + "\n")
    if build["returncode"] != 0:
        print("BUILD FAILED", file=sys.stderr)
        print(build["stderr"], file=sys.stderr)
        return 1
    rows = []
    for case, stack, timeout in CASES:
        cmd = [str(BIN), case]
        if stack is not None:
            cmd.append(str(stack))
        r = run(cmd, timeout=timeout)
        row = {
            "case": case,
            "stack": stack,
            "timed_out": r["timed_out"],
            "returncode": r["returncode"],
            "stdout": r["stdout"].strip(),
            "stderr": r["stderr"].strip()[-2000:],
        }
        rows.append(row)
        print(row["stdout"] or f"FAIL {case} rc={r['returncode']} timeout={r['timed_out']}")
    (OUT / "cases.json").write_text(json.dumps(rows, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
