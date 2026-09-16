"""Run one command with a receipt and prove the fixed source is byte-unchanged across it.

Writes receipts/<label>/{command.json, stdout.txt, stderr.txt, exit.txt, digests.json}. Before and after the command the
fixed source is re-hashed against root's capture.json; digests.json records both verifications.
Usage: run_with_receipt.py LABEL -- ARGV...
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAPTURE = Path("/tmp/opensip-design-corrections/root-repair-owner-probe.v2/capture.json")
SOURCE = CAPTURE.parent / "source"


def verify():
    cap = json.loads(CAPTURE.read_text())
    mism = [f["path"] for f in cap["files"] if hashlib.sha256((SOURCE / f["path"]).read_bytes()).hexdigest() != f["sha256"]]
    listed = {f["path"] for f in cap["files"]}
    extra = [(Path(d) / n).relative_to(SOURCE).as_posix() for d, _, fs in os.walk(SOURCE) for n in fs
             if (Path(d) / n).relative_to(SOURCE).as_posix() not in listed]
    return {"files": len(cap["files"]), "mismatch": mism, "unlisted": extra}


label, argv = sys.argv[1], sys.argv[sys.argv.index("--") + 1:]
out = HERE / "receipts" / label
out.mkdir(parents=True, exist_ok=False)
before = verify()
(out / "command.json").write_text(json.dumps({"label": label, "argv": argv, "cwd": str(HERE)}, indent=1) + "\n")
t = time.time()
proc = subprocess.run(argv, cwd=HERE, capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
seconds = round(time.time() - t, 1)
(out / "stdout.txt").write_bytes(proc.stdout)
(out / "stderr.txt").write_bytes(proc.stderr)
(out / "exit.txt").write_text(str(proc.returncode) + "\n")
after = verify()
(out / "digests.json").write_text(json.dumps({"seconds": seconds, "stdoutSha256": hashlib.sha256(proc.stdout).hexdigest(),
                                              "stderrSha256": hashlib.sha256(proc.stderr).hexdigest(),
                                              "sourceBefore": before, "sourceAfter": after}, indent=1) + "\n")
print(json.dumps({"label": label, "exit": proc.returncode, "seconds": seconds,
                  "sourceUnchanged": not (before["mismatch"] or before["unlisted"] or after["mismatch"] or after["unlisted"])}))
