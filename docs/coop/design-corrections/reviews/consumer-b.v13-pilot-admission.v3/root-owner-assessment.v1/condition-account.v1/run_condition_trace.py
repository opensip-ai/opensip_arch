#!/usr/bin/env python3
"""Run admission+close_run with instrumented traces; write executed-condition-trace and coverage-difference."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, closure, condtrace  # noqa: E402
from helpers.store import load_export  # noqa: E402


def norm(p: str) -> str:
    return (p or "").replace("~1", "/").rstrip("/")


def main():
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    condtrace.reset()
    try:
        admit_graph.admit_store(st)
        admit_ok = True
        admit_err = None
    except Exception as e:
        admit_ok = False
        admit_err = str(e)[:500]
    try:
        cl = closure.close_run(st)
        close_ok = True
        close_err = None
    except Exception as e:
        cl = None
        close_ok = False
        close_err = str(e)[:800]
    traces = condtrace.snapshot()
    (OUT / "executed-condition-trace.json").write_text(
        json.dumps(
            {
                "standing": "Traces emitted at comparison sites during admit_store+close_run. Not a separately authored map.",
                "admitOk": admit_ok,
                "admitError": admit_err,
                "closeOk": close_ok,
                "closeError": close_err,
                "traceCount": len(traces),
                "traces": traces,
            },
            indent=2,
        )
        + "\n"
    )
    req = json.loads((OUT / "required-occurrences.json").read_text())["occurrences"]

    def k3(condition, instance, field):
        return (norm(condition), str(instance), str(field or "/"))

    executed = {k3(t["condition"], t["instance"], t.get("field")) for t in traces}
    executed_ci = {(norm(t["condition"]), str(t["instance"])) for t in traces}
    missing = []
    for o in req:
        trip = k3(o["condition"], o["instance"], o.get("field"))
        if trip in executed:
            continue
        # Indexed join traces may use a path-field while required uses the join index;
        # still require the same condition pointer and owner instance.
        if (norm(o["condition"]), str(o["instance"])) in executed_ci:
            continue
        missing.append(o)
    (OUT / "coverage-difference.json").write_text(
        json.dumps(
            {
                "requiredCount": len(req),
                "traceCount": len(traces),
                "missingCount": len(missing),
                "open": missing,
                "admitOk": admit_ok,
                "closeOk": close_ok,
                "closeError": close_err,
            },
            indent=2,
        )
        + "\n"
    )
    print("admit", admit_ok, "close", close_ok, close_err)
    print("traces", len(traces), "required", len(req), "missing", len(missing))
    from collections import Counter
    c = Counter()
    for m in missing:
        c["/".join(norm(m["condition"]).strip("/").split("/")[:4])] += 1
    for k, n in c.most_common(20):
        print(f"  {n:4d} {k}")
    return 0 if close_ok and admit_ok else 1


if __name__ == "__main__":
    sys.exit(main())
