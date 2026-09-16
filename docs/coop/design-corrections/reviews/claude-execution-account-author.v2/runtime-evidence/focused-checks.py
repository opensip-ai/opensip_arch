#!/usr/bin/env python3
"""Focused current reference checks for the v2 follow-up.

Scope rationale: the v2 edits touch `execution_inputs_model.v1.py` (derive_outcome /
_outcome_from_items / candidate carrier), `evaluator_graph_fixture.v3.py` (one default-OFF option)
and `check-execution-inputs.v1.py`. The checks below are the ones that exercise those paths.
Root performs the authoritative pin/planning rebind and the full integrated suites on final bytes,
so this deliberately does NOT repeat the broad v1 sweep.

Reports are written under THIS runtime only. Authoritative pin ledgers are read but never written;
their staleness is reported, not repaired.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")
DC = SRC / "docs/coop/design-corrections"
OUT = HERE / "suite"
PY = "/tmp/opensip-architecture-review-env/bin/python"

JOBS = [
    ("execution-inputs", "foundation/check-execution-inputs.v1.py", [],
     "the edited checker itself"),
    ("execution-replay", "foundation/check-execution-replay.v3.py", [],
     "full retained Runs over derive_outcome through M.close_run"),
    ("candidate-replay", "foundation/check-candidate-replay.v3.py", [],
     "the candidate carrier path this revision changed"),
    ("composition", "foundation/check-composition.v3.py", [],
     "the §9.6 proof bridge the row carrier feeds"),
    ("full-replay", "foundation/check-replay.v3.py", [],
     "graph-fixture consumers at large"),
    ("native-replay", "foundation/check-semantic-replay.v3.py", [],
     "semantic fixture consumers of the graph fixture"),
    ("enumeration", "foundation/check-enumeration.v1.py", ["--stdout"],
     "binding/inventory guards the carrier law leans on"),
    ("policy-derivation", "foundation/check-policy-derivation.v3.py", [],
     "cheap downstream of a closed Run"),
    ("faults", "foundation/check-evaluator-faults.v3.py", [],
     "cheap downstream fault vocabulary"),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    stale = {}
    for ledger in ("evaluator3-source-pins.v1.json", "source-pins.v1.json"):
        rows = json.loads((DC / "foundation" / ledger).read_text())["files"]
        bad = []
        for row in rows:
            target = SRC / row["path"]
            if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != row["sha256"]:
                bad.append(row["path"])
        stale[ledger] = sorted(bad)

    rows = []
    for name, script, args, why in JOBS:
        command = [PY, "-I", "-B", str(DC / script)] + args
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=900)
            code, out, err, timed = proc.returncode, proc.stdout, proc.stderr, False
        except subprocess.TimeoutExpired as exc:
            dec = lambda v: "" if v is None else (v if isinstance(v, str) else v.decode("utf-8", "replace"))
            code, out, err, timed = None, dec(exc.stdout), dec(exc.stderr), True
        (OUT / (name + ".stdout")).write_text(out)
        (OUT / (name + ".stderr")).write_text(err)
        rows.append({"name": name, "why": why, "command": command, "exitCode": code,
                     "timedOut": timed, "stderrTail": err[-800:]})
        print(name, code, "TIMEOUT" if timed else "", flush=True)

    report = {
        "standing": "FOCUSED current reference checks over the v2-edited source. Not acceptance, "
                    "not product qualification, not a pin/planning update, and deliberately NOT "
                    "the full integrated suite - root runs that on final bytes.",
        "notRun": ["current-profile", "atoms", "provider-attribution-return", "workflow-projection",
                   "query-projection", "comparison-knowledge", "analysis-seal",
                   "check-identity.py", "check-foundation.py", "check-product-quality.py",
                   "check-product-configuration.py", "check-array-orders.py"],
        "notRunReason": "untouched by the v2 edits and all green on the v1 bytes; re-running them "
                        "would repeat an unchanged broad sweep root asked to avoid.",
        "authoritativePinsStale": stale,
        "checks": rows,
        "allChecksPassed": bool(rows) and all(r["exitCode"] == 0 and not r["timedOut"] for r in rows),
        "productQualification": False,
    }
    (HERE / "focused-checks-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "checks"}, indent=2))
    return 0 if report["allChecksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
