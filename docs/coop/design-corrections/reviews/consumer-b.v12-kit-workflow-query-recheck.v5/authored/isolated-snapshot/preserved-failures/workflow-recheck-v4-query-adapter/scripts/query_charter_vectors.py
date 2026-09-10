#!/usr/bin/env python3
"""Charter query reconstruction vectors.

Algorithmic cases use independently chosen projected edges (labeled).
execute_graph_query against frozen stores without close_run is measured as
VIEW_UNKNOWN — not fabricated admission. Frozen stores are never rewritten.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v3")
OUT = ROOT
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.identity import H, parse_h_frame  # noqa: E402
from helper.query_projection import (  # noqa: E402
    execute_graph_query,
    operational_bind,
    project_edges,
    render_parity,
    traverse_projected_graph,
    vertex_domain,
)
from helper.schema_admit import validate_against  # noqa: E402
from helper.workflow_laws import GRAPH_PROJECTABLE, cursor_token  # noqa: E402

HEX_A = "a" * 64
HEX_B = "b" * 64
UNI = HEX_A
PRJ = "prj1-" + HEX_A
RUN = "run3:" + HEX_B
SNAP = "snapshot2:" + HEX_A
HOST_RID = "req1_" + "ab" * 16
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"


def dump(rel, obj):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return p


def ep(name, kind="symbol"):
    return {"universe": UNI, "kind": kind, "nativeSubjectId": name}


def mint_fact(i, caller, callee):
    rec = {
        "schemaVersion": 1, "relation": "calls", "resolution": "resolved-callee",
        "sourceUniverse": UNI, "targetUniverse": UNI,
        "payload": {"caller": caller, "resolvedCallee": callee}, "ordinal": i,
    }
    fid = "fact2:" + H("fact", rec)
    return {
        "factId": fid, "relation": "calls", "resolution": "resolved-callee",
        "sourceUniverse": UNI, "targetUniverse": UNI, "payload": rec["payload"],
    }


facts = [mint_fact(0, "mod.a", "mod.b"), mint_fact(1, "mod.a", "mod.c"), mint_fact(2, "mod.b", "mod.c")]
facts.sort(key=lambda f: f["factId"])
edges = project_edges(facts, relation="calls", min_resolution="resolved-callee")
view_id = "view2:" + H("view", {"schemaVersion": 1, "facts": [f["factId"] for f in facts]})
cov_id = "coverage2:" + H("coverage", {"schemaVersion": 1, "relation": "calls", "resolution": "resolved-callee"})
scope_id = "scope2:" + H("subject-scope", {"schemaVersion": 1, "include": ["**/*"]})
inv = {"kind": "symbol", "universe": UNI, "rows": [
    {"nativeSubjectId": "mod.a", "path": "a.ts"},
    {"nativeSubjectId": "mod.b", "path": "b.ts"},
    {"nativeSubjectId": "mod.c", "path": "c.ts"},
]}
admitted_run = {"runId": RUN, "snapshotId": SNAP, "projectId": PRJ}


def close_run_ok(run, objects=None, blobs=None):
    if run.get("runId") != RUN:
        raise AdmissionError("CLOSE_RUN", "unexpected run")
    return {"ok": True, "synthetic": True}


def req(op, params, page=None, view=None, completeness="best-effort"):
    return {
        "schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": PRJ,
        "view": view or {"runId": RUN}, "operation": op, "params": params,
        "completeness": completeness, "page": page or {"size": 100},
    }


def host_base(**more):
    h = {"requestId": HOST_RID, "availability": "retained", "latestRunId": RUN, "runsForSnapshot": {SNAP: [RUN]}}
    h.update(more)
    return h


kw = dict(
    run=admitted_run, objects={}, blobs={}, host=host_base(), close_run=close_run_ok,
    projected_edges=edges, inventories=[inv], coverage_ids=[cov_id], scope_ids=[scope_id],
    fact_view_digests=[view_id],
)

cases = []

nb_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("mod.a")}
path_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("mod.a"), "target": ep("mod.c"), "maxDepth": 8}
reach_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("mod.a"), "maxDepth": 8, "includeStart": True}

r_nb = execute_graph_query(req("graph.neighbors", nb_params), **kw)
r_path = execute_graph_query(req("graph.path", path_params, page={"size": 1}), **kw)
r_reach = execute_graph_query(req("graph.reach", reach_params), **kw)
cases.append({"id": "all-three-operations", "label": "algorithmic-with-synthetic-close_run", "ok": r_nb["ok"] and r_path["ok"] and r_reach["ok"],
              "neighborsN": len(r_nb["response"]["items"]), "pathHops": (r_path["response"]["items"] or [{}])[0].get("hopCount"), "reachN": len(r_reach["response"]["items"])})

# canonical order
nb_items = r_nb["response"]["items"]
order_ok = nb_items == sorted(nb_items, key=lambda e: (e["source"]["universe"], e["source"]["kind"], e["source"]["nativeSubjectId"], "", e["target"]["universe"], e["target"]["kind"], e["target"]["nativeSubjectId"], "", e["factId"]))
cases.append({"id": "canonical-units-order", "label": "algorithmic", "ok": order_ok, "factIds": [e["factId"] for e in nb_items]})

# endpoint unknown / malformed
r_unk = execute_graph_query(req("graph.neighbors", {**nb_params, "endpoint": ep("mod.missing")}), **kw)
r_mal = execute_graph_query(req("graph.neighbors", {**nb_params, "endpoint": {"logicalPath": "src/a.ts"}}), **kw)
r_maj = execute_graph_query({**req("graph.neighbors", nb_params), "schemaMajor": 2}, **kw)
r_unsup = execute_graph_query(req("graph.neighbors", {"relation": "file", "minResolution": "enumerated", "direction": "outgoing", "endpoint": ep("src/index.ts", "file")}), **kw)
cases.append({"id": "endpoint-unknown", "ok": (not r_unk["ok"]) and r_unk["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.ENDPOINT_UNKNOWN"})
cases.append({"id": "malformed-logicalpath", "ok": (not r_mal["ok"]) and r_mal["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.PARAMS_MALFORMED" and "run" not in r_mal["envelope"]})
cases.append({"id": "schema-major", "ok": (not r_maj["ok"]) and r_maj["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.SCHEMA_MAJOR_UNSUPPORTED"})
cases.append({"id": "relation-unsupported", "ok": (not r_unsup["ok"]) and r_unsup["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED"})

# page vs operation bound
r_page = execute_graph_query(req("graph.neighbors", nb_params, page={"size": 1}), **kw)
ctxp = r_page["response"]["context"]
page2_cur = ctxp.get("nextCursor")
r_page2 = execute_graph_query(req("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur}), **kw)
cases.append({"id": "page-boundary", "ok": ctxp["traversalCoverage"] == "truncated-page" and ctxp["truncated"] is False and bool(page2_cur) and r_page2["ok"] and bool(r_page2["response"]["items"])})

kw_bound = dict(kw)
kw_bound["host"] = host_base(testBounds={"maxVisitedNodes": 1})
r_bound = execute_graph_query(req("graph.path", path_params, completeness="best-effort"), **kw_bound)
ctxb = (r_bound.get("response") or {}).get("context") or {}
cases.append({"id": "operation-bound", "ok": r_bound["ok"] and ctxb.get("traversalCoverage") == "truncated-bound" and ctxb.get("truncated") is True,
              "items": (r_bound.get("response") or {}).get("items")})
r_req_bound = execute_graph_query(req("graph.path", path_params, completeness="required"), **kw_bound)
cases.append({"id": "operation-bound-required", "ok": r_req_bound["ok"] and (r_req_bound["response"] or {}).get("termination", {}).get("reasonCodes") == ["QUERY.COMPLETENESS_UNMET"]})

# historical bind after newer latest
newer = "run3:" + ("c" * 64)
cur = r_page["response"]["context"]["nextCursor"]
kw_latest = dict(kw)
kw_latest["host"] = host_base(latestRunId=newer)
# continuation must use view.runId of bound historical run, not latest
r_hist = execute_graph_query(req("graph.neighbors", nb_params, page={"size": 1, "cursor": cur}, view={"runId": RUN}), **kw_latest)
cases.append({"id": "historical-pagination-after-newer-latest", "ok": r_hist["ok"] and r_hist["response"]["context"]["resolvedView"]["runId"] == RUN,
              "hostLatest": newer, "resolved": r_hist.get("response", {}).get("context", {}).get("resolvedView")})
r_latest_mismatch = execute_graph_query(req("graph.neighbors", nb_params, view={"latest": True}), **kw_latest)
cases.append({"id": "latest-mismatch-refuses", "ok": (not r_latest_mismatch["ok"]) and r_latest_mismatch["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN"})

# cache loss: same result with and without host.cache
kw_cache = dict(kw)
kw_cache["host"] = host_base(cache={"edges": "must-be-ignored"})
r_cache = execute_graph_query(req("graph.neighbors", nb_params), **kw_cache)
cases.append({"id": "cache-loss-rebuild", "ok": r_cache["ok"] and r_cache["response"]["items"] == r_nb["response"]["items"] and r_cache["ignoredHostCache"] is True})

# evidence limitations vs stored-edge completion
kw_empty = dict(kw)
kw_empty["projected_edges"] = []
kw_empty["limitations"] = [{"kind": "resolution-incomplete", "state": "incomplete"}]
r_empty = execute_graph_query(req("graph.neighbors", nb_params), **kw_empty)
lim = r_empty["response"]["context"]["evidence"]["resolutionLimitations"]
cases.append({"id": "evidence-limits-vs-stored-completion", "ok": r_empty["ok"] and r_empty["response"]["items"] == [] and any(x.get("kind") == "native-evidence-unavailable" or x.get("kind") == "resolution-incomplete" for x in lim),
              "limitations": lim, "note": "zero neighbor rows is not no-callers; disclosure retained"})

# view ambiguous
kw_amb = dict(kw)
kw_amb["host"] = host_base(runsForSnapshot={SNAP: [RUN, "run3:" + ("d" * 64)]})
r_amb = execute_graph_query(req("graph.neighbors", nb_params, view={"snapshotId": SNAP}), **kw_amb)
cases.append({"id": "view-ambiguous", "ok": (not r_amb["ok"]) and r_amb["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_AMBIGUOUS"})

# availability refuse
kw_purge = dict(kw)
kw_purge["host"] = host_base(availability="purged")
r_purge = execute_graph_query(req("graph.neighbors", nb_params), **kw_purge)
cases.append({"id": "availability-purged", "ok": (not r_purge["ok"]) and r_purge["envelope"]["kind"] == "failure" and "run" not in r_purge["envelope"]})

# execute without close_run
r_noclose = execute_graph_query(req("graph.neighbors", nb_params), run=admitted_run, objects={}, blobs={}, host=host_base(), close_run=None, projected_edges=edges)
cases.append({"id": "execute-requires-close-run", "ok": (not r_noclose["ok"]) and r_noclose["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN",
              "message": (r_noclose.get("refusal") or {}).get("message")})

# parity
parity = render_parity(r_nb["response"], ["human", "json", "agent"])
six = {"resolved-view", "availability", "truncated", "total-items", "termination-class", "query-response"}
parity_ok = all(isinstance(parity[f], dict) and set(parity[f]) >= six and "context" in parity[f]["query-response"] for f in ("human", "json", "agent"))
cases.append({"id": "human-json-agent-parity", "ok": parity_ok})

# traverse_projected_graph labeled algorithmic
alg = traverse_projected_graph(edges=edges, operation="graph.neighbors", params=nb_params)
cases.append({"id": "standalone-walk-labeled-not-admission", "ok": alg["label"] == "algorithmic" and len(alg["items"]) == len(nb_items)})

# missing host requestId
r_noreq = None
try:
    r_noreq = execute_graph_query(req("graph.neighbors", nb_params), run=admitted_run, objects={}, blobs={}, host={"availability": "retained"}, close_run=close_run_ok, projected_edges=edges)
    noreq_ok = False
except Exception as e:
    noreq_ok = getattr(e, "code", "") == "REFERENCE_CALL_PRECONDITION"
cases.append({"id": "synthetic-host-requestId-required", "ok": noreq_ok})

# schema inhabitance
schema_ok = True
schema_errs = []
for label, inst, doc, sel in [
    ("nb-req", req("graph.neighbors", nb_params), GQ, "#/$defs/GraphQueryRequestV1"),
    ("nb-resp", r_nb["response"], GQ, "#/$defs/GraphQueryResponseV1"),
    ("fail-unsup", r_unsup["envelope"], CE, "#"),
]:
    r = validate_against(inst, doc, selector=sel, label=label)
    if not r["stockOk"]:
        schema_ok = False
        schema_errs.append({label: r["errors"][:2]})
cases.append({"id": "schema-inhabitance", "ok": schema_ok, "errors": schema_errs})

# --- frozen store probe (no close_run, no fabricated edges) ---
import base64

frozen = json.loads((OUT / "frozen-run-hashes.json").read_text())["runs"]
store_probes = []
for name, exp in frozen.items():
    raw = (OUT / "runs" / name).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    doc = json.loads(raw)
    table = doc["objectTable"]
    blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    relations = []
    for k, rec in table.items():
        if not (isinstance(k, str) and k.startswith("fact2:")):
            continue
        frame = blobs.get(rec["digest"])
        if not frame:
            continue
        parsed = parse_h_frame(frame)
        val = parsed["value"]
        relations.append({"factId": k, "relation": val.get("relation"), "resolution": val.get("resolution")})
    projectable = [r for r in relations if (r["relation"], r["resolution"]) in GRAPH_PROJECTABLE]
    # execute_graph_query without close_run
    probe_req = req("graph.neighbors", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("mod.a")})
    if run_ids:
        probe_req["view"] = {"runId": run_ids[0]}
    measured = execute_graph_query(
        probe_req, run={"runId": run_ids[0], "snapshotId": "unknown", "projectId": PRJ} if run_ids else None,
        objects=table, blobs=blobs, host=host_base(), close_run=None, projected_edges=None,
    )
    store_probes.append({
        "store": name,
        "sha256": got,
        "matchesFrozen": got == exp["sha256"],
        "runIds": run_ids,
        "observedFactRelations": relations,
        "graphProjectableFacts": projectable,
        "callsResolvedCalleePresent": any(r["relation"] == "calls" and r["resolution"] == "resolved-callee" for r in relations),
        "importsResolvedTargetPresent": any(r["relation"] == "imports" and r["resolution"] == "resolved-target" for r in relations),
        "targetAttributionObserved": False,
        "executeWithoutCloseRun": {
            "ok": measured["ok"],
            "code": None if measured["ok"] else measured["envelope"]["termination"]["domainDetail"]["code"],
        },
        "didNotFabricateEdges": True,
        "closeRun": "not-executed",
    })

dump("query/charter-algorithmic-cases.json", {
    "label": "algorithmic-or-synthetic-close_run",
    "notRetainedRunAdmission": True,
    "edges": edges,
    "cases": cases,
    "neighborsResponse": r_nb["response"],
    "pathResponse": r_path["response"],
    "reachResponse": r_reach["response"],
    "page1": r_page["response"],
    "page2": r_page2["response"],
    "operationBound": r_bound,
    "historicalAfterLatest": r_hist["response"] if r_hist["ok"] else r_hist,
    "cacheRebuild": r_cache["response"],
    "emptyWithDisclosure": r_empty["response"],
    "failures": {
        "endpointUnknown": r_unk["envelope"],
        "malformed": r_mal["envelope"],
        "schemaMajor": r_maj["envelope"],
        "unsupported": r_unsup["envelope"],
        "latestMismatch": r_latest_mismatch["envelope"],
        "viewAmbiguous": r_amb["envelope"],
        "purged": r_purge["envelope"],
        "noCloseRun": r_noclose["envelope"],
    },
    "rendererParity": {"formats": ["human", "json", "agent"], "parityFields": sorted(six), "rendered": parity},
    "didNotSealRun": True,
})
dump("query/frozen-store-probe.json", {
    "label": "frozen-store-bytes-without-close_run",
    "closeRun": "not-executed-out-of-scope",
    "didNotFabricateGraphEvidence": True,
    "probes": store_probes,
})
dump("query/parity.json", {"formats": ["human", "json", "agent"], "parityFields": sorted(six), "rendered": parity, "source": "charter query reconstruction; query-response is complete GraphQueryResponseV1"})

print("CHARTER_QUERY cases", len(cases), "fail", [c["id"] for c in cases if not c["ok"]])
print("FROZEN", [(p["store"], p["callsResolvedCalleePresent"], p["executeWithoutCloseRun"]["code"]) for p in store_probes])
if any(not c["ok"] for c in cases):
    raise SystemExit(1)
print("OK")
