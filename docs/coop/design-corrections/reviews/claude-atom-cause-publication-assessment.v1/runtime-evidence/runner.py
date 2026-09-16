#!/usr/bin/env python3
"""Receipt runner for the bounded normative-publication check. Writes only in this runtime."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"
for sub in ("probes", "probes/receipts", "reports"):
    (HERE / sub).mkdir(parents=True, exist_ok=True)


def run(label, argv):
    out = RECEIPTS / label
    out.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(argv, cwd=str(HERE), capture_output=True)
    (out / "command.json").write_text(json.dumps({"label": label, "argv": argv}, indent=2) + "\n")
    (out / "stdout.txt").write_bytes(p.stdout)
    (out / "stderr.txt").write_bytes(p.stderr)
    (out / "exit.txt").write_text(str(p.returncode) + "\n")
    return {"label": label, "exit": p.returncode, "stdoutBytes": len(p.stdout),
            "stderrTail": p.stderr.decode("utf-8", "replace")[-2000:]}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"bootstrapped": str(HERE)}, indent=2))
        raise SystemExit(0)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
