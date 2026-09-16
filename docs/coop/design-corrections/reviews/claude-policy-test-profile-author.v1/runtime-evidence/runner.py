"""Receipt runner: run one argv and keep command, stdout, stderr, exit and digests under receipts/<label>[.N].

Usage (as a module): runner.run(label, argv, cwd=None, timeout=None) -> (exit_code, receipt_dir)
Usage (CLI):         runner.py LABEL [--cwd DIR] -- ARGV...
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"


def run(label, argv, cwd=None, timeout=None):
    base = HERE / "receipts"
    base.mkdir(exist_ok=True)
    out, n = base / label, 1
    while out.exists():
        n += 1
        out = base / ("%s.%d" % (label, n))
    out.mkdir()
    (out / "command.json").write_text(json.dumps({"label": out.name, "argv": [str(x) for x in argv], "cwd": str(cwd or HERE)}, indent=1) + "\n")
    t = time.time()
    proc = subprocess.run([str(x) for x in argv], cwd=cwd or HERE, capture_output=True, timeout=timeout,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    (out / "stdout.txt").write_bytes(proc.stdout)
    (out / "stderr.txt").write_bytes(proc.stderr)
    (out / "exit.txt").write_text("%d\n" % proc.returncode)
    (out / "digests.json").write_text(json.dumps({"seconds": round(time.time() - t, 1), "stdoutSha256": hashlib.sha256(proc.stdout).hexdigest(),
                                                  "stderrSha256": hashlib.sha256(proc.stderr).hexdigest()}, indent=1) + "\n")
    return proc.returncode, out


if __name__ == "__main__":
    label = sys.argv[1]
    cwd = sys.argv[sys.argv.index("--cwd") + 1] if "--cwd" in sys.argv[:sys.argv.index("--")] else None
    code, where = run(label, sys.argv[sys.argv.index("--") + 1:], cwd=cwd)
    print(json.dumps({"label": where.name, "exit": code, "stdoutTail": (where / "stdout.txt").read_text(errors="replace")[-3000:],
                      "stderrTail": (where / "stderr.txt").read_text(errors="replace")[-3000:]}, indent=1))
    sys.exit(0)
