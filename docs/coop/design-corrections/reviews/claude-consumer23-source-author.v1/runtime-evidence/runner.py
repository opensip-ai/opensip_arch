#!/usr/bin/env python3
"""Receipt runner for the consumer23 source-clarification author runtime.

Records exact argv, cwd, stdout, stderr, exit and SHA-256 digests under probes/receipts/<label>/.
Failed attempts are retained: a repeated label gets a numeric suffix. Writes only under this runtime.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"
for sub in ("probes", "probes/receipts", "before", "after", "reports"):
    (HERE / sub).mkdir(parents=True, exist_ok=True)


def slot(label: str) -> Path:
    out = RECEIPTS / label
    if not out.exists():
        return out
    n = 2
    while (RECEIPTS / f"{label}.{n}").exists():
        n += 1
    return RECEIPTS / f"{label}.{n}"


def run(label, argv, cwd=None, timeout=3600):
    out = slot(label)
    out.mkdir(parents=True)
    workdir = str(cwd or HERE)
    (out / "command.json").write_text(json.dumps({"label": out.name, "argv": argv, "cwd": workdir}, indent=2) + "\n")
    p = subprocess.run(argv, cwd=workdir, capture_output=True, timeout=timeout)
    (out / "stdout.txt").write_bytes(p.stdout)
    (out / "stderr.txt").write_bytes(p.stderr)
    (out / "exit.txt").write_text(str(p.returncode) + "\n")
    digests = {"stdoutSha256": hashlib.sha256(p.stdout).hexdigest(), "stderrSha256": hashlib.sha256(p.stderr).hexdigest()}
    (out / "digests.json").write_text(json.dumps(digests, indent=2) + "\n")
    return {"label": out.name, "exit": p.returncode, "stdoutBytes": len(p.stdout), **digests,
            "stdoutPath": str(out / "stdout.txt"), "stderrTail": p.stderr.decode("utf-8", "replace")[-3000:]}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"bootstrapped": str(HERE)}, indent=2))
        raise SystemExit(0)
    print(json.dumps(run(sys.argv[1], sys.argv[2:]), indent=2))
