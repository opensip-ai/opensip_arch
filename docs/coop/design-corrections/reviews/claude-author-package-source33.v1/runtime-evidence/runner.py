#!/usr/bin/env python3
"""Receipt runner for the source33 author-package runtime.

Records exact argv, stdout, stderr and exit code under probes/receipts/<label>/.
Nothing outside this runtime (and the owned package10) is written by this tool.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"

for sub in ("probes", "probes/receipts", "reports", "before", "tmp"):
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
        "label": label, "exit": proc.returncode,
        "stdoutBytes": len(proc.stdout), "stderrBytes": len(proc.stderr),
        "stdoutPath": str(out / "stdout.txt"), "stderrPath": str(out / "stderr.txt"),
        "stderrTail": proc.stderr.decode("utf-8", "replace")[-3000:],
    }


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"bootstrapped": str(HERE)}, indent=2))
        raise SystemExit(0)
    cwd = None
    args = sys.argv[1:]
    if args[0] == "--cwd":
        cwd = args[1]
        args = args[2:]
    print(json.dumps(run(args[0], args[1:], cwd=cwd), indent=2))
