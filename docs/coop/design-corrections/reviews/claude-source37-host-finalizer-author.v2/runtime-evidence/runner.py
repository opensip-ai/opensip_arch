#!/usr/bin/env python3
"""Receipt runner for the source37 host-finalizer author v2 runtime.

Records exact argv, cwd, stdout, stderr, exit and SHA-256 digests under receipts/<label>/.
Failed attempts are retained: a repeated label gets a numeric suffix. Writes only under this runtime.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "receipts"
RECEIPTS.mkdir(parents=True, exist_ok=True)


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
    started = time.time()
    p = subprocess.run(argv, cwd=workdir, capture_output=True, timeout=timeout)
    (out / "stdout.txt").write_bytes(p.stdout)
    (out / "stderr.txt").write_bytes(p.stderr)
    (out / "exit.txt").write_text(str(p.returncode) + "\n")
    digests = {"stdoutSha256": hashlib.sha256(p.stdout).hexdigest(), "stderrSha256": hashlib.sha256(p.stderr).hexdigest(),
               "seconds": round(time.time() - started, 1)}
    (out / "digests.json").write_text(json.dumps(digests, indent=2) + "\n")
    return {"label": out.name, "exit": p.returncode, "stdoutBytes": len(p.stdout), **digests,
            "stdoutTail": p.stdout.decode("utf-8", "replace")[-2500:],
            "stderrTail": p.stderr.decode("utf-8", "replace")[-2500:]}


if __name__ == "__main__":
    args = sys.argv[1:]
    cwd = None
    if args[:1] == ["--cwd"]:
        cwd, args = args[1], args[2:]
    if len(args) < 2:
        raise SystemExit("usage: runner.py [--cwd DIR] LABEL ARGV...")
    print(json.dumps(run(args[0], args[1:], cwd=cwd), indent=2))
