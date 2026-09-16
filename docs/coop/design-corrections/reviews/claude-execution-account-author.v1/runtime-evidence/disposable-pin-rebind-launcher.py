#!/usr/bin/env python3
"""DISPOSABLE TEST-ONLY pin rebinding + current reference suite runner.

STANDING: this is a THROWAWAY copy that exists only so the current suites can execute over
edited source. It is NOT an authority and it is NOT a pin update.

* The authoritative ledger `foundation/evaluator3-source-pins.v1.json` in the successor source
  is READ ONLY here and is left byte-identical. Root owns the real pin/planning rebinding at
  final integration.
* The rebound ledger written under this runtime is labelled `DISPOSABLE-...` and is never
  copied back.
* It reports, separately and honestly: (a) which authoritative pins are now stale, and (b) the
  exit code of every current check run against the edited source.

Job list is copied verbatim from foundation/run-evaluator3-checks.py.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")
DC = SRC / "docs/coop/design-corrections"
FOUNDATION = DC / "foundation"
OUT = HERE / "suite"
PY = "/tmp/opensip-architecture-review-env/bin/python"

JOBS = [
    ("current-profile", "foundation/check-current-profile.v3.py", []),
    ("enumeration", "foundation/check-enumeration.v1.py", ["--stdout"]),
    ("atoms", "foundation/check-atoms.v1.py", []),
    ("execution-inputs", "foundation/check-execution-inputs.v1.py", []),
    ("composition", "foundation/check-composition.v3.py", []),
    ("full-replay", "foundation/check-replay.v3.py", []),
    ("native-replay", "foundation/check-semantic-replay.v3.py", []),
    ("execution-replay", "foundation/check-execution-replay.v3.py", []),
    ("candidate-replay", "foundation/check-candidate-replay.v3.py", []),
    ("policy-derivation", "foundation/check-policy-derivation.v3.py", []),
    ("faults", "foundation/check-evaluator-faults.v3.py", []),
    ("provider-attribution-return", "foundation/check-provider-attribution-return.v2.py", []),
    ("workflow-projection", "workflows/check-workflow-projection.v3.py", []),
    ("query-projection", "workflows/check-query-projection.v3.py",
     ["--report", str(OUT / "query-projection.receipt.json")]),
    ("comparison-knowledge", "workflows/check-comparison-knowledge.v3.py", []),
    ("analysis-seal", "security/check-analysis-seal-adapter.v1.py", []),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = json.loads((FOUNDATION / "evaluator3-source-pins.v1.json").read_text())
    stale, missing, rebound = [], [], []
    for row in ledger["files"]:
        target = SRC / row["path"]
        if not target.is_file():
            missing.append(row["path"])
            continue
        now = hashlib.sha256(target.read_bytes()).hexdigest()
        if now != row["sha256"]:
            stale.append({"path": row["path"], "pinned": row["sha256"], "now": now})
        rebound.append({"path": row["path"], "sha256": now})

    (HERE / "DISPOSABLE-rebound-source-pins.json").write_text(json.dumps({
        "standing": "DISPOSABLE TEST-ONLY REBINDING. Not an authority, not a pin update, never "
                    "copied back into the source. The authoritative "
                    "foundation/evaluator3-source-pins.v1.json is unchanged; root owns the real "
                    "rebinding at final integration.",
        "rebuiltFrom": str(FOUNDATION / "evaluator3-source-pins.v1.json"),
        "stalePinsAgainstAuthoritativeLedger": stale,
        "missingFromSource": missing,
        "files": rebound,
    }, indent=2) + "\n")

    rows = []
    for name, script, args in JOBS:
        command = [PY, "-I", "-B", str(DC / script)] + args
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=900)
            code, stdout, stderr, timed = proc.returncode, proc.stdout, proc.stderr, False
        except subprocess.TimeoutExpired as exc:
            dec = lambda v: v.decode("utf-8", "replace") if isinstance(v, bytes) else (v or "")
            code, stdout, stderr, timed = None, dec(exc.stdout), dec(exc.stderr), True
        (OUT / (name + ".stdout")).write_text(stdout)
        (OUT / (name + ".stderr")).write_text(stderr)
        rows.append({
            "name": name, "command": command, "exitCode": code, "timedOut": timed,
            "stdoutSha256": hashlib.sha256(stdout.encode()).hexdigest(),
            "stderrSha256": hashlib.sha256(stderr.encode()).hexdigest(),
            "stderrTail": stderr[-800:],
        })
        print(name, code, "TIMEOUT" if timed else "", flush=True)

    report = {
        "standing": "current reference checks over EDITED successor source, run through a "
                    "DISPOSABLE test-only pin rebinding. Not acceptance, not product "
                    "qualification, not a pin/planning update.",
        "authoritativePinsStale": bool(stale),
        "stalePinCount": len(stale),
        "stalePins": stale,
        "checks": rows,
        "allChecksPassed": bool(rows) and all(r["exitCode"] == 0 and not r["timedOut"] for r in rows),
        "productQualification": False,
    }
    (HERE / "suite-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "checks"}, indent=2))
    return 0 if report["allChecksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
