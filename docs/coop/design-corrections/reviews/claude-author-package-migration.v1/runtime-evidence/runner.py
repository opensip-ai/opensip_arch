"""Receipt runner for the author-package migration runtime.

Records exact argv, cwd, stdout, stderr, exit and SHA-256 digests under receipts/<label>/. A repeated label gets a
numeric suffix, so failed attempts are never overwritten. Writes only under this runtime.
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
PY = "/tmp/opensip-architecture-review-env/bin/python"


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
    (out / "command.json").write_text(json.dumps({"label": out.name, "argv": [str(a) for a in argv], "cwd": workdir}, indent=2) + "\n")
    started = time.time()
    try:
        p = subprocess.run([str(a) for a in argv], cwd=workdir, capture_output=True, timeout=timeout)
        stdout, stderr, code = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, code = exc.stdout or b"", (exc.stderr or b"") + b"\nTIMEOUT", 124
    (out / "stdout.txt").write_bytes(stdout)
    (out / "stderr.txt").write_bytes(stderr)
    (out / "exit.txt").write_text(str(code) + "\n")
    digests = {"stdoutSha256": hashlib.sha256(stdout).hexdigest(), "stderrSha256": hashlib.sha256(stderr).hexdigest(),
               "seconds": round(time.time() - started, 1)}
    (out / "digests.json").write_text(json.dumps(digests, indent=2) + "\n")
    return {"label": out.name, "exit": code, **digests,
            "stdoutTail": stdout.decode("utf-8", "replace")[-2000:], "stderrTail": stderr.decode("utf-8", "replace")[-2000:]}


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit("usage: runner.py LABEL ARGV...")
    print(json.dumps(run(args[0], args[1:]), indent=2))
