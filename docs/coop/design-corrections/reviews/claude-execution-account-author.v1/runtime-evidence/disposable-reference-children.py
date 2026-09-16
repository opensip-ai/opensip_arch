#!/usr/bin/env python3
"""DISPOSABLE TEST-ONLY runner for the five children of run-reference-checks.py.

That launcher's own pin sweep over `source-pins.v1.json` is stale by construction after any
edit, so the children are invoked directly here and the stale-pin fact is reported separately.
Every report is written under THIS runtime via --report-dir; nothing in the source is written.
The authoritative ledgers are read only.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"
OUT = HERE / "suite2"
PY = "/tmp/opensip-architecture-review-env/bin/python"

CHILDREN = [
    ("check-foundation.py", "foundation-report.json"),
    ("check-identity.py", "identity-report.json"),
    ("check-product-quality.py", "product-quality-report.json"),
    ("check-product-configuration.py", "product-configuration-report.json"),
    ("check-array-orders.py", "array-order-report.json"),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = json.loads((FOUNDATION / "source-pins.v1.json").read_text())
    stale = []
    for row in ledger["files"]:
        target = SRC / row["path"]
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != row["sha256"]:
            stale.append(row["path"])

    rows = []
    for script, report in CHILDREN:
        command = [PY, "-I", "-B", str(FOUNDATION / script), "--report", str(OUT / report)]
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=900)
            code, out, err, timed = proc.returncode, proc.stdout, proc.stderr, False
        except subprocess.TimeoutExpired as exc:
            dec = lambda v: "" if v is None else (v if isinstance(v, str) else v.decode("utf-8", "replace"))
            code, out, err, timed = None, dec(exc.stdout), dec(exc.stderr), True
        (OUT / (script + ".stdout")).write_text(out)
        (OUT / (script + ".stderr")).write_text(err)
        rows.append({"script": script, "exitCode": code, "timedOut": timed,
                     "stdoutTail": out[-600:], "stderrTail": err[-1200:]})
        print(script, code, "TIMEOUT" if timed else "", flush=True)

    result = {
        "standing": "DISPOSABLE TEST-ONLY direct invocation of run-reference-checks.py's five "
                    "children over EDITED successor source. Authoritative source-pins.v1.json is "
                    "unchanged and its staleness is reported, not repaired. Not acceptance.",
        "authoritativeSourcePinsStale": sorted(stale),
        "stalePinCount": len(stale),
        "checks": rows,
        "passed": all(r["exitCode"] == 0 and not r["timedOut"] for r in rows),
        "productQualification": False,
    }
    (HERE / "suite2-report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
