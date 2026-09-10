#!/usr/bin/env python3
"""Assert query adapter laws from produced outputs, not key-presence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5")
OUT = ROOT / "output"

FAILED = []


def fail(msg: str) -> None:
    FAILED.append(msg)
    print("FAIL", msg)


def must(cond, msg):
    if not cond:
        fail(msg)


cases = json.loads((OUT / "query/charter-algorithmic-cases.json").read_text())["cases"]
by = {c["id"]: c for c in cases}
must(all(c["ok"] for c in cases), f"failed cases {[c['id'] for c in cases if not c['ok']]}")
must(len(cases) >= 40, f"preserve useful controls n={len(cases)}")
for pid in (
    "extra-view2-must-not-become-admitted-fact-view",
    "unselected-inventory-must-not-admit-endpoint",
    "coverage-entry-resolutionCompleteness-disclosed",
    "incoming-search-incomplete-cited",
    "close-run-returns-selected-records-not-flag",
):
    must(by.get(pid, {}).get("ok") is True, pid)

qr = json.loads((OUT / "query/parity.json").read_text())["queryResult"]
must(qr.get("kind") == "query", "QueryResult.kind")
must(isinstance(qr.get("items"), int) and qr["items"] == 2, f"QueryResult.items actual={qr.get('items')}")
must(qr.get("truncated") is False, "QueryResult.truncated")
must(qr.get("completenessMet") is True, "QueryResult.completenessMet")
must(qr.get("advisory") is False, "QueryResult.advisory")

par = json.loads((OUT / "query/parity.json").read_text())["rendered"]
resp = json.loads((OUT / "query/charter-algorithmic-cases.json").read_text())["neighborsResponse"]
ctx = resp["context"]
for fmt in ("human", "json", "agent"):
    must(par[fmt]["resolved-view"] == ctx["resolvedView"], f"{fmt} resolved-view")
    must(par[fmt]["availability"] == ctx["availability"], f"{fmt} availability")
    must(par[fmt]["truncated"] == ctx["truncated"], f"{fmt} truncated")
    must(par[fmt]["total-items"] == ctx["totalItems"], f"{fmt} total-items")
    must(par[fmt]["query-response"] == resp, f"{fmt} query-response identity")

page_qr = json.loads((OUT / "query/charter-algorithmic-cases.json").read_text())["page1QueryResult"]
must(page_qr["completenessMet"] is True and page_qr["truncated"] is False and page_qr.get("nextCursor"), "page QueryResult joins")

env_fail = json.loads((OUT / "query/charter-algorithmic-cases.json").read_text())["failures"]["unsupported"]
must(env_fail["kind"] == "failure" and "run" not in env_fail and env_fail.get("errors"), "failure envelope")

probe = json.loads((OUT / "query/frozen-store-probe.json").read_text())
must(all(p["executeWithoutCloseRun"]["code"] == "QUERY.VIEW_UNKNOWN" for p in probe["probes"]), "frozen without close_run")
must(all(p["matchesFrozen"] for p in probe["probes"]), "frozen hashes")
must(not any(p["callsResolvedCalleePresent"] for p in probe["probes"]), "no fabricated calls")

if FAILED:
    print("assertions FAIL nfail", len(FAILED))
    raise SystemExit(1)
print("assertions PASS nfail 0")
print("OK")
