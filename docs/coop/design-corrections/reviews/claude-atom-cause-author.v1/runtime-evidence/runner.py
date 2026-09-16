#!/usr/bin/env python3
"""Receipt runner for the atom-cause successor authoring runtime.

Records exact argv, stdout, stderr, exit under probes/receipts/<label>/. Failed attempts are
retained, never overwritten: a repeated label gets a numeric suffix.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"
for sub in ("probes", "probes/receipts", "reports", "before", "after"):
    (HERE / sub).mkdir(parents=True, exist_ok=True)


def slot(label: str) -> Path:
    out = RECEIPTS / label
    if not out.exists():
        return out
    n = 2
    while (RECEIPTS / f"{label}.{n}").exists():
        n += 1
    return RECEIPTS / f"{label}.{n}"


def run(label, argv):
    out = slot(label)
    out.mkdir(parents=True)
    p = subprocess.run(argv, cwd=str(HERE), capture_output=True)
    (out / "command.json").write_text(json.dumps(
        {"label": out.name, "argv": argv}, indent=2) + "\n")
    (out / "stdout.txt").write_bytes(p.stdout)
    (out / "stderr.txt").write_bytes(p.stderr)
    (out / "exit.txt").write_text(str(p.returncode) + "\n")
    return {"label": out.name, "exit": p.returncode, "stdoutBytes": len(p.stdout),
            "stdoutPath": str(out / "stdout.txt"),
            "stderrTail": p.stderr.decode("utf-8", "replace")[-3000:]}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"bootstrapped": str(HERE)}, indent=2))
        raise SystemExit(0)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
