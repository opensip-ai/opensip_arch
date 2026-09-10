#!/usr/bin/env python3
"""Assertions over charter query vectors. Nonzero exit on failure."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v3")
OUT = ROOT / "output"
sys.path.insert(0, str(OUT))

FAILED = []


def fail(msg: str) -> None:
    FAILED.append(msg)
    print("FAIL", msg)


def must(cond, msg):
    if not cond:
        fail(msg)


def load(rel):
    return json.loads((OUT / rel).read_text())


cases = {c["id"]: c for c in load("query/charter-algorithmic-cases.json")["cases"]}
for cid in [
    "all-three-operations", "canonical-units-order", "endpoint-unknown", "malformed-logicalpath",
    "schema-major", "relation-unsupported", "page-boundary", "operation-bound", "operation-bound-required",
    "historical-pagination-after-newer-latest", "latest-mismatch-refuses", "cache-loss-rebuild",
    "evidence-limits-vs-stored-completion", "view-ambiguous", "availability-purged",
    "execute-requires-close-run", "human-json-agent-parity", "standalone-walk-labeled-not-admission",
    "synthetic-host-requestId-required", "schema-inhabitance",
]:
    must(cid in cases and cases[cid]["ok"] is True, f"case {cid}")

alg = load("query/charter-algorithmic-cases.json")
must(alg["notRetainedRunAdmission"] is True and alg["didNotSealRun"] is True, "not admission")
must(alg["pathResponse"]["items"][0]["hopCount"] >= 1, "nontrivial path")
must(alg["page1"]["context"]["traversalCoverage"] == "truncated-page" and alg["page1"]["context"]["truncated"] is False, "page law")
must(alg["operationBound"]["response"]["context"]["truncated"] is True, "op bound truncated true")
fail_env = alg["failures"]["unsupported"]
must(fail_env["kind"] == "failure" and "run" not in fail_env, "failure has no run")

probe = load("query/frozen-store-probe.json")
must(probe["closeRun"] == "not-executed-out-of-scope", "frozen close_run")
must(all(p["matchesFrozen"] and p["didNotFabricateEdges"] for p in probe["probes"]), "frozen hashes")
must(all(not p["callsResolvedCalleePresent"] for p in probe["probes"]), "no calls@resolved-callee in frozen stores")
must(all(p["executeWithoutCloseRun"]["code"] == "QUERY.VIEW_UNKNOWN" for p in probe["probes"]), "no close_run => VIEW_UNKNOWN")
ts = next(p for p in probe["probes"] if p["store"] == "ts.store.json")
must(ts["importsResolvedTargetPresent"] is True and ts["targetAttributionObserved"] is False, "imports unprojectable without TargetAttribution")

print("assertions", "FAIL" if FAILED else "PASS", "nfail", len(FAILED))
if FAILED:
    for m in FAILED:
        print(" -", m)
    raise SystemExit(1)
print("OK")
