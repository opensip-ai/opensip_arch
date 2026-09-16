#!/usr/bin/env python3
"""Receipt runner for the v2 source-author runtime.

Runs a command, records exact argv, stdout, stderr and exit code under
probes/receipts/<label>/. Nothing outside this runtime is written.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"

for sub in ("before", "after", "probes", "suite", "probes/receipts"):
    (HERE / sub).mkdir(parents=True, exist_ok=True)


def run(label: str, argv: list[str], cwd: str | None = None) -> dict:
    out = RECEIPTS / label
    out.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(argv, cwd=cwd or str(HERE), capture_output=True)
    (out / "command.json").write_text(json.dumps(
        {"label": label, "argv": argv, "cwd": cwd or str(HERE)}, indent=2) + "\n")
    (out / "stdout.txt").write_bytes(proc.stdout)
    (out / "stderr.txt").write_bytes(proc.stderr)
    (out / "exit.txt").write_text(str(proc.returncode) + "\n")
    return {
        "label": label,
        "exit": proc.returncode,
        "stdoutBytes": len(proc.stdout),
        "stderrBytes": len(proc.stderr),
        "stdoutPath": str(out / "stdout.txt"),
        "stderrPath": str(out / "stderr.txt"),
        "stderrTail": proc.stderr.decode("utf-8", "replace")[-2000:],
    }


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"bootstrapped": str(HERE)}, indent=2))
        raise SystemExit(0)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
