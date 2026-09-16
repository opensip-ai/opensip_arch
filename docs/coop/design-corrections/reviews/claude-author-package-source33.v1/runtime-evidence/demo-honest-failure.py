#!/usr/bin/env python3
"""DISPOSABLE demonstration that the corrected verifier RECORDS a query failure.

Root's evidence showed no verification.json at all, because the old verifier asserted mid-flight.
This builds a THROWAWAY copy of package10 inside this runtime, makes its query assessment step
exit non-zero, rebuilds only that copy's manifest, and runs the verifier. package10 itself and v9
are never written. The throwaway is labelled and is not part of any deliverable.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
DEMO = HERE / "tmp" / "DISPOSABLE-failure-demo-package"
OUT = HERE / "verification" / "failure-demo"
SRC = "/tmp/opensip-design-corrections/candidate-subject.v33"
PY = "/tmp/opensip-architecture-review-env/bin/python"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if DEMO.exists():
        shutil.rmtree(DEMO)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(V10, DEMO)
    (DEMO / "DISPOSABLE-README.txt").write_text(
        "THROWAWAY copy of package10 used only to demonstrate honest failure recording.\n"
        "Its query assessment step is deliberately broken. Never a deliverable.\n")
    # Break only the query assessment step.
    target = DEMO / "assess-author-query.py"
    target.write_text('import sys\nsys.stderr.write("DISPOSABLE deliberate failure\\n")\n'
                      'raise SystemExit(3)\n')
    files = []
    for p in sorted(DEMO.rglob("*")):
        if p.is_file() and not p.is_symlink():
            rel = str(p.relative_to(DEMO))
            if rel == "artifact-manifest.json":
                continue
            files.append({"path": rel, "sha256": sha(p), "bytes": p.stat().st_size})
    (DEMO / "artifact-manifest.json").write_text(json.dumps(
        {"standing": "DISPOSABLE demo manifest", "sourceManifestSha256":
         "1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299",
         "files": files}, indent=2) + "\n")

    cmd = [PY, "-I", "-B", str(DEMO / "verify-package.py"), "--source", SRC, "--out", str(OUT)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    verification = OUT / "verification.json"
    out = {
        "standing": "DISPOSABLE demonstration that the corrected verifier records a query failure "
                    "instead of aborting without a report. package10 and v9 are untouched.",
        "command": cmd, "exitCode": proc.returncode,
        "stdout": proc.stdout, "stderrTail": proc.stderr[-1500:],
        "verificationJsonWritten": verification.is_file(),
    }
    if verification.is_file():
        v = json.loads(verification.read_text())
        out["verificationPassed"] = v["passed"]
        out["groups"] = [{"group": g["group"], "passed": g["passed"],
                          "failure": g.get("failure")} for g in v["groups"]]
    (HERE / "reports" / "honest-failure-demo.json").write_text(json.dumps(out, indent=2) + "\n")
    shutil.rmtree(DEMO)
    out["throwawayRemoved"] = True
    print(json.dumps({k: v for k, v in out.items() if k != "stdout"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
