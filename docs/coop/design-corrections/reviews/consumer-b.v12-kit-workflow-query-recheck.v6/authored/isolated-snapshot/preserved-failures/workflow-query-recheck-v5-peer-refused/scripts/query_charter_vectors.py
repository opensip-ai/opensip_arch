#!/usr/bin/env python3
"""Charter query reconstruction vectors (adapter-control retained graph).

Public execute_graph_query projects from admitted retained bytes after
close_retained_run (H-frame rehash + run identity join). That closer is
query-scoped identity admission, not identity-and-evidence §3 complete
B12 close_run. Frozen five Run stores are not rewritten and not claimed
admitted. traverse_projected_graph remains labeled algorithmic.

Independently chosen endpoints: Unit.alpha / Unit.beta / Unit.gamma.
Expected values derived from query-projection-contract.v3.md §§1–8,
graph-query.schema.json major 3, and workflows-and-surfaces §8.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v4")
OUT = ROOT
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.identity import H, parse_h_frame  # noqa: E402
from helper.query_projection import (  # noqa: E402
    close_retained_run,
    execute_graph_query,
    traverse_projected_graph,
)
from helper.schema_admit import validate_against  # noqa: E402
from helper.store import Store  # noqa: E402
from helper.workflow_laws import project_edges  # noqa: E402

HEX_U = hashlib.sha256(b"opensip.author.adapter-control.universe.v4").hexdigest()
PRJ = "prj1-" + hashlib.sha256(b"opensip.author.adapter-control.project.v4").hexdigest()
HOST_RID = "req1_" + "cd" * 16
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
SNAP_ID = "snapshot2:" + hashlib.sha256(b"opensip.author.adapter-control.snapshot.v4").hexdigest()
PLAN_ID = "plan2:" + hashlib.sha256(b"opensip.author.adapter-control.plan.v4").hexdigest()
CLOS = "closure2:" + hashlib.sha256(b"opensip.author.adapter-control.closure.v4").hexdigest()
SCHEMA_D = hashlib.sha256(b"opensip.author.adapter-control.payload-schema.v4").hexdigest()


def dump(rel, obj):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return p


def ep(name, kind="symbol", pmp=None):
    d = {"universe": HEX_U, "kind": kind, "nativeSubjectId": name}
    if pmp is not None:
        d["packageManifestPath"] = pmp
    return d


def mint_control_graph():
    """Independently constructed retained bytes for adapter-control. Not a B12 complete Run."""
    store = Store()
    ev = "evidence3:" + hashlib.sha256(b"adapter-control-evidence").hexdigest()
    seal = "seal3:" + hashlib.sha256(b"adapter-control-seal").hexdigest()
    cap = hashlib.sha256(b"adapter-control-cap").hexdigest()
    run_body = {
        "schemaVersion": 3,
        "projectId": PRJ,
        "snapshotId": SNAP_ID,
        "planId": PLAN_ID,
        "evidenceId": ev,
        "evaluationSealId": seal,
        "capabilityManifestId": cap,
    }
    run_rec = store.put_h("run", run_body, label="adapter-control-run")
    run_id = run_rec["typedId"]

    def put_call(caller, callee, ordinal):
        payload = {"caller": caller, "resolvedCallee": callee}
        pd = store.put_canonical(payload, label=f"calls-payload-{ordinal}")
        fact = {
            "schemaVersion": 2,
            "snapshotId": SNAP_ID,
            "relation": "calls",
            "resolution": "resolved-callee",
            "sourceUniverse": HEX_U,
            "targetUniverse": HEX_U,
            "producerClosure": CLOS,
            "payloadSchemaDigest": SCHEMA_D,
            "payloadDigest": pd,
            "anchors": [],
            "confidenceMillionths": 1000000,
        }
        rec = store.put_h("fact", fact, label=f"call-{ordinal}")
        return rec["typedId"]

    f_ab = put_call("Unit.alpha", "Unit.beta", 0)
    f_ag = put_call("Unit.alpha", "Unit.gamma", 1)
    f_bg = put_call("Unit.beta", "Unit.gamma", 2)

    # weaker-rung fact in the same view: omitted, not a request refusal
    weak_pl = store.put_canonical({"caller": "Unit.alpha", "calleeName": "ghost"}, label="weak-payload")
    weak_fact = {
        "schemaVersion": 2,
        "snapshotId": SNAP_ID,
        "relation": "calls",
        "resolution": "syntactic-callee-name",
        "sourceUniverse": HEX_U,
        "targetUniverse": HEX_U,
        "producerClosure": CLOS,
        "payloadSchemaDigest": SCHEMA_D,
        "payloadDigest": weak_pl,
        "anchors": [],
        "confidenceMillionths": 1000000,
    }
    weak_id = store.put_h("fact", weak_fact, label="weak-call")["typedId"]

    # imports without TargetAttributionV1 → unprojectable
    imp_pl = store.put_canonical({"importer": "Unit.alpha", "resolvedTarget": "pkg.other"}, label="imp-payload")
    imp_fact = {
        "schemaVersion": 2,
        "snapshotId": SNAP_ID,
        "relation": "imports",
        "resolution": "resolved-target",
        "sourceUniverse": HEX_U,
        "targetUniverse": HEX_U,
        "producerClosure": CLOS,
        "payloadSchemaDigest": SCHEMA_D,
        "payloadDigest": imp_pl,
        "anchors": [],
        "confidenceMillionths": 1000000,
    }
    imp_id = store.put_h("fact", imp_fact, label="imp-no-ta")["typedId"]

    # imports WITH TargetAttributionV1 package
    imp2_pl = store.put_canonical({"importer": "Unit.beta", "resolvedTarget": "demo"}, label="imp2-payload")
    imp2_fact = {
        "schemaVersion": 2,
        "snapshotId": SNAP_ID,
        "relation": "imports",
        "resolution": "resolved-target",
        "sourceUniverse": HEX_U,
        "targetUniverse": HEX_U,
        "producerClosure": CLOS,
        "payloadSchemaDigest": SCHEMA_D,
        "payloadDigest": imp2_pl,
        "anchors": [],
        "confidenceMillionths": 1000000,
    }
    imp2_id = store.put_h("fact", imp2_fact, label="imp-with-ta")["typedId"]
    ta = {
        "schemaVersion": 1,
        "planId": PLAN_ID,
        "sourceFactId": imp2_id,
        "producerClosure": CLOS,
        "targetUniverse": HEX_U,
        "targetNativeId": "demo",
        "kind": "package",
        "occupancy": "first-party",
        "exported": False,
        "logicalPath": "Cargo.toml",
        "packageManifestPath": "Cargo.toml",
    }
    store.put_canonical(ta, label="target-attribution")

    scope_calls = store.put_h(
        "subject-scope",
        {
            "schemaVersion": 2,
            "snapshotId": SNAP_ID,
            "sourceUniverse": HEX_U,
            "targetUniverse": HEX_U,
            "relation": "calls",
            "resolution": "resolved-callee",
            "enumeratorClosure": CLOS,
            "subjects": ["Unit.alpha", "Unit.beta", "Unit.gamma"],
        },
        label="scope-calls",
    )["typedId"]
    cov_pl = store.put_canonical(
        {"key": {"relation": "calls", "resolution": "resolved-callee"}, "entry": {"coverage": "complete"}},
        label="cov-calls-payload",
    )
    cov_calls = store.put_h(
        "coverage",
        {"schemaVersion": 2, "scopeId": scope_calls, "payloadSchemaDigest": SCHEMA_D, "payloadDigest": cov_pl},
        label="cov-calls",
    )["typedId"]

    view_calls = store.put_h(
        "view",
        {
            "schemaVersion": 2,
            "planId": PLAN_ID,
            "scopeIds": [scope_calls],
            "facts": sorted([f_ab, f_ag, f_bg, weak_id]),
            "coverageIds": [cov_calls],
            "producerClosure": CLOS,
            "schemaDigests": [SCHEMA_D],
        },
        label="view-calls",
    )["typedId"]

    # file@enumerated view: explicit selection against calls discloses native-evidence-unavailable
    file_pl = store.put_canonical({"path": "src/lib.rs", "contentSha256": "aa" * 32, "byteLength": 1}, label="file-payload")
    file_fact = {
        "schemaVersion": 2,
        "snapshotId": SNAP_ID,
        "relation": "file",
        "resolution": "enumerated",
        "sourceUniverse": HEX_U,
        "targetUniverse": HEX_U,
        "producerClosure": CLOS,
        "payloadSchemaDigest": SCHEMA_D,
        "payloadDigest": file_pl,
        "anchors": [],
        "confidenceMillionths": 1000000,
    }
    file_id = store.put_h("fact", file_fact, label="file-fact")["typedId"]
    scope_file = store.put_h(
        "subject-scope",
        {
            "schemaVersion": 2,
            "snapshotId": SNAP_ID,
            "sourceUniverse": HEX_U,
            "targetUniverse": HEX_U,
            "relation": "file",
            "resolution": "enumerated",
            "enumeratorClosure": CLOS,
            "subjects": ["src/lib.rs"],
        },
        label="scope-file",
    )["typedId"]
    cov_file_pl = store.put_canonical(
        {"key": {"relation": "file", "resolution": "enumerated"}, "entry": {"coverage": "complete"}},
        label="cov-file-payload",
    )
    cov_file = store.put_h(
        "coverage",
        {"schemaVersion": 2, "scopeId": scope_file, "payloadSchemaDigest": SCHEMA_D, "payloadDigest": cov_file_pl},
        label="cov-file",
    )["typedId"]
    view_file = store.put_h(
        "view",
        {
            "schemaVersion": 2,
            "planId": PLAN_ID,
            "scopeIds": [scope_file],
            "facts": [file_id],
            "coverageIds": [cov_file],
            "producerClosure": CLOS,
            "schemaDigests": [SCHEMA_D],
        },
        label="view-file",
    )["typedId"]

    view_imports = store.put_h(
        "view",
        {
            "schemaVersion": 2,
            "planId": PLAN_ID,
            "scopeIds": [scope_calls],
            "facts": sorted([imp_id, imp2_id]),
            "coverageIds": [],
            "producerClosure": CLOS,
            "schemaDigests": [SCHEMA_D],
        },
        label="view-imports",
    )["typedId"]

    inv_sym = {
        "schemaVersion": 1,
        "planId": PLAN_ID,
        "parameterDigest": "aa" * 32,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "symbol",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": ["src/lib.rs"],
        "rows": [
            {"nativeSubjectId": "Unit.alpha", "kind": "symbol", "path": "src/a.rs", "qualifiedName": "Unit.alpha", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
            {"nativeSubjectId": "Unit.beta", "kind": "symbol", "path": "src/b.rs", "qualifiedName": "Unit.beta", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
            {"nativeSubjectId": "Unit.gamma", "kind": "symbol", "path": "src/c.rs", "qualifiedName": "Unit.gamma", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
        ],
    }
    store.put_canonical(inv_sym, label="inventory-symbol")
    inv_pkg = {
        "schemaVersion": 1,
        "planId": PLAN_ID,
        "parameterDigest": "aa" * 32,
        "cellOrdinal": 1,
        "programOrdinal": 0,
        "kind": "package",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": ["Cargo.toml"],
        "rows": [
            {"nativeSubjectId": "demo", "kind": "package", "path": "Cargo.toml", "qualifiedName": "demo", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
        ],
    }
    store.put_canonical(inv_pkg, label="inventory-package")

    locator = {"runId": run_id, "snapshotId": SNAP_ID, "projectId": PRJ}
    return {
        "store": store,
        "locator": locator,
        "runId": run_id,
        "viewCalls": view_calls,
        "viewFile": view_file,
        "viewImports": view_imports,
        "facts": {"ab": f_ab, "ag": f_ag, "bg": f_bg, "weak": weak_id, "imp": imp_id, "imp2": imp2_id},
        "label": "adapter-control-retained-graph-not-b12-complete-run",
    }


G = mint_control_graph()
STORE = G["store"]
LOC = G["locator"]
RUN = G["runId"]


def req(op, params, page=None, view=None, completeness="best-effort"):
    return {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "projectId": PRJ,
        "view": view or {"runId": RUN},
        "operation": op,
        "params": params,
        "completeness": completeness,
        "page": page or {"size": 100},
    }


def host_base(**more):
    h = {
        "requestId": HOST_RID,
        "availability": "retained",
        "latestRunId": RUN,
        "runsForSnapshot": {SNAP_ID: [RUN]},
    }
    h.update(more)
    return h


def go(request, **more):
    kw = dict(run=LOC, objects=STORE.object_table, blobs=STORE.blobs, host=host_base(), close_run=close_retained_run)
    kw.update(more)
    return execute_graph_query(request, kw["run"], kw["objects"], kw["blobs"], kw["host"], close_run=kw["close_run"])


nb_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("Unit.alpha")}
path_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Unit.alpha"), "target": ep("Unit.gamma"), "maxDepth": 8}
reach_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Unit.alpha"), "maxDepth": 8, "includeStart": True}

cases = []

r_nb = go(req("graph.neighbors", nb_params))
r_path = go(req("graph.path", path_params))
r_reach = go(req("graph.reach", reach_params))
cases.append({
    "id": "all-three-operations",
    "ok": r_nb["ok"] and r_path["ok"] and r_reach["ok"]
    and len(r_nb["response"]["items"]) == 2
    and (r_path["response"]["items"] or [{}])[0].get("hopCount") == 1
    and len(r_reach["response"]["items"]) >= 2,
    "neighborsN": len(r_nb["response"]["items"]) if r_nb["ok"] else None,
    "pathHops": (r_path["response"]["items"] or [{}])[0].get("hopCount") if r_path["ok"] else None,
    "reachN": len(r_reach["response"]["items"]) if r_reach["ok"] else None,
})

nb_items = r_nb["response"]["items"] if r_nb["ok"] else []
ordered = sorted(nb_items, key=lambda e: (
    e["source"]["universe"], e["source"]["kind"], e["source"]["nativeSubjectId"], "",
    e["target"]["universe"], e["target"]["kind"], e["target"]["nativeSubjectId"], "",
    e["factId"],
))
cases.append({"id": "canonical-units-order", "ok": nb_items == ordered, "factIds": [e["factId"] for e in nb_items]})

# compact QueryResult joins on actual produced output
env = r_nb["envelope"]
qr = env["query"]
ctx = r_nb["response"]["context"]
cases.append({
    "id": "compact-QueryResult-joins",
    "ok": (
        env["kind"] == "query"
        and qr["kind"] == "query"
        and qr["items"] == ctx["producedItems"] == 2
        and qr["truncated"] is False
        and qr["truncated"] == ctx["truncated"]
        and qr["completenessMet"] is True
        and qr["completenessMet"] == (ctx["countBasis"] == "exact")
        and qr["advisory"] is False
        and "nextCursor" not in qr
        and env["termination"]["class"] == "success"
        and env["projectId"] == PRJ
        and "run" not in env
    ),
    "queryResult": qr,
})

# six-field exact projections
par = r_nb["parity"]
six_ok = all(
    par[f]["resolved-view"] == ctx["resolvedView"]
    and par[f]["availability"] == ctx["availability"]
    and par[f]["truncated"] == ctx["truncated"]
    and par[f]["total-items"] == ctx["totalItems"]
    and par[f]["termination-class"] == "success"
    and par[f]["query-response"] == r_nb["response"]
    for f in ("human", "json", "agent")
)
cases.append({"id": "six-field-parity-exact", "ok": six_ok})

# file@enumerated request refused
r_file = go(req("graph.neighbors", {
    "relation": "file", "minResolution": "enumerated", "direction": "outgoing",
    "endpoint": ep("src/lib.rs", "file"),
}))
cases.append({"id": "file-enumerated-unsupported", "ok": (not r_file["ok"]) and r_file["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED" and "run" not in r_file["envelope"]})

r_syn = go(req("graph.neighbors", {**nb_params, "minResolution": "syntactic-callee-name"}))
cases.append({"id": "weaker-rung-request-refused", "ok": (not r_syn["ok"]) and r_syn["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED"})

r_unk = go(req("graph.neighbors", {**nb_params, "endpoint": ep("Unit.missing")}))
r_mal = go(req("graph.neighbors", {**nb_params, "endpoint": {"logicalPath": "src/a.rs"}}))
r_extra = go(req("graph.neighbors", {**nb_params, "subject": "x"}))
r_maj = go({**req("graph.neighbors", nb_params), "schemaMajor": 2})
cases.append({"id": "endpoint-unknown", "ok": (not r_unk["ok"]) and r_unk["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.ENDPOINT_UNKNOWN"})
cases.append({"id": "malformed-logicalpath", "ok": (not r_mal["ok"]) and r_mal["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.PARAMS_MALFORMED" and "run" not in r_mal["envelope"]})
cases.append({"id": "extra-params", "ok": (not r_extra["ok"]) and r_extra["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.PARAMS_MALFORMED"})
cases.append({"id": "schema-major", "ok": (not r_maj["ok"]) and r_maj["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.SCHEMA_MAJOR_UNSUPPORTED" and r_maj["envelope"]["termination"]["errorCode"] == "REQUEST.SCHEMA_MAJOR_UNSUPPORTED"})

# package without PMP is always ambiguous
r_pkg = go(req("graph.neighbors", {
    "relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing",
    "endpoint": ep("demo", "package"),
}))
cases.append({"id": "package-without-PMP-ambiguous", "ok": (not r_pkg["ok"]) and r_pkg["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.ENDPOINT_AMBIGUOUS"})

# page vs bound
r_page = go(req("graph.neighbors", nb_params, page={"size": 1}))
ctxp = (r_page.get("response") or {}).get("context") or {}
page2_cur = ctxp.get("nextCursor")
r_page2 = go(req("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur})) if page2_cur else {"ok": False}
qr_page = (r_page.get("envelope") or {}).get("query") or {}
cases.append({
    "id": "truncated-page-not-truncated",
    "ok": r_page["ok"] and ctxp.get("traversalCoverage") == "truncated-page" and ctxp.get("truncated") is False
    and qr_page.get("truncated") is False and qr_page.get("completenessMet") is True
    and qr_page.get("nextCursor") == page2_cur and qr_page.get("items") == 1
    and r_page2.get("ok"),
})

r_bound = go(req("graph.path", path_params, completeness="best-effort"), host=host_base(testBounds={"maxVisitedNodes": 1}))
ctxb = (r_bound.get("response") or {}).get("context") or {}
qrb = (r_bound.get("envelope") or {}).get("query") or {}
cases.append({
    "id": "operation-bound",
    "ok": r_bound["ok"] and ctxb.get("traversalCoverage") == "truncated-bound" and ctxb.get("truncated") is True
    and qrb.get("completenessMet") is False and qrb.get("truncated") is True
    and r_bound["response"]["items"] == [],
})
r_reqb = go(req("graph.path", path_params, completeness="required"), host=host_base(testBounds={"maxVisitedNodes": 1}))
term = (r_reqb.get("response") or {}).get("termination") or {}
cases.append({
    "id": "operation-bound-required",
    "ok": r_reqb["ok"] and term.get("reasonCodes") == ["QUERY.COMPLETENESS_UNMET"]
    and term.get("class") == "indeterminate"
    and r_reqb["envelope"]["termination"] == term
    and r_reqb["envelope"]["kind"] == "query"
    and r_reqb["envelope"]["exitCode"] == 3
    and r_reqb["parity"]["json"]["termination-class"] == "indeterminate",
})

zero_params = {**path_params, "start": ep("Unit.alpha"), "target": ep("Unit.alpha")}
r_zero = go(req("graph.path", zero_params), host=host_base(testBounds={"maxVisitedNodes": 1}))
cases.append({"id": "zero-hop-at-cap-complete", "ok": r_zero["ok"] and r_zero["response"]["items"][0]["hopCount"] == 0 and r_zero["response"]["context"]["traversalCoverage"] == "complete"})

# historical pagination
newer = "run3:" + hashlib.sha256(b"opensip.author.newer-run").hexdigest()
r_hist = go(req("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur}, view={"runId": RUN}), host=host_base(latestRunId=newer)) if page2_cur else {"ok": False}
cases.append({"id": "historical-pagination-after-newer-latest", "ok": r_hist.get("ok") and r_hist["response"]["context"]["resolvedView"]["runId"] == RUN})
r_lat = go(req("graph.neighbors", nb_params, view={"latest": True}), host=host_base(latestRunId=newer))
cases.append({"id": "latest-mismatch-unknown", "ok": (not r_lat["ok"]) and r_lat["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN"})
r_latcur = go(req("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur}, view={"latest": True})) if page2_cur else {"ok": True}
cases.append({"id": "continuation-requires-view-runId", "ok": (not r_latcur.get("ok")) and (r_latcur.get("envelope") or {}).get("termination", {}).get("domainDetail", {}).get("code") == "QUERY.CURSOR_MISMATCH"})

r_cache = go(req("graph.neighbors", nb_params), host=host_base(cache={"edges": "poison"}))
cases.append({"id": "cache-ignored", "ok": r_cache["ok"] and r_cache["response"]["items"] == nb_items and r_cache["ignoredHost"]["cache"] is True})

r_amb = go(req("graph.neighbors", nb_params, view={"snapshotId": SNAP_ID}), host=host_base(runsForSnapshot={SNAP_ID: [RUN, "run3:" + "dd" * 32]}))
cases.append({"id": "view-ambiguous", "ok": (not r_amb["ok"]) and r_amb["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_AMBIGUOUS"})
r_snone = go(req("graph.neighbors", nb_params, view={"snapshotId": SNAP_ID}), host=host_base(runsForSnapshot={}))
cases.append({"id": "snapshot-missing-unknown", "ok": (not r_snone["ok"]) and r_snone["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN"})

r_purge = go(req("graph.neighbors", nb_params), host=host_base(availability="purged"))
cases.append({"id": "availability-purged", "ok": (not r_purge["ok"]) and r_purge["envelope"]["kind"] == "failure" and "run" not in r_purge["envelope"]})

r_noclose = execute_graph_query(req("graph.neighbors", nb_params), LOC, STORE.object_table, STORE.blobs, host_base(), close_run=None)
cases.append({"id": "execute-requires-close-run", "ok": (not r_noclose["ok"]) and r_noclose["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN"})

# no-op synthetic close_run cannot supply caller edges; missing parse still needs retained bytes
def synthetic_ok(run, objects=None, blobs=None):
    return {"ok": True, "synthetic": True}

# A synthetic flag still proceeds to project from objects/blobs — if objects exist, it would
# produce edges. That is why public evidence is the retained bytes, not the flag.
# Demonstrate: empty objects with synthetic close_run → missing/unknown, not invented edges.
r_synflag = execute_graph_query(req("graph.neighbors", nb_params), LOC, {}, {}, host_base(), close_run=synthetic_ok)
cases.append({
    "id": "synthetic-flag-without-bytes-not-evidence",
    "ok": (not r_synflag["ok"]) and r_synflag["envelope"]["kind"] == "failure",
})

# explicit file view selected for calls → native-evidence-unavailable, empty neighbors, not no-callers
r_wrongview = go(req("graph.neighbors", {**nb_params, "factViewDigests": [G["viewFile"]]}))
lim_w = ((r_wrongview.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
cases.append({
    "id": "native-unavailable-when-selected-view-mismatches",
    "ok": r_wrongview["ok"] and r_wrongview["response"]["items"] == []
    and any(x.get("kind") == "native-evidence-unavailable" and x.get("relation") == "calls" for x in lim_w),
    "limitations": lim_w,
})

# matching view + empty stored edges is lawful empty neighbors WITHOUT native-unavailable
# (this graph has edges). Isolated vertex: Unit that is inventory-only — use gamma incoming none? gamma has incoming.
# Isolated: request neighbors of a vertex that exists via inventory but wait all have edges.
# Empty neighbors at gamma outgoing: gamma has no outgoing calls.
r_empty_nb = go(req("graph.neighbors", {**nb_params, "endpoint": ep("Unit.gamma"), "direction": "outgoing"}))
lim_e = r_empty_nb["response"]["context"]["evidence"]["resolutionLimitations"] if r_empty_nb["ok"] else []
cases.append({
    "id": "empty-neighbors-not-native-unavailable-when-view-matches",
    "ok": r_empty_nb["ok"] and r_empty_nb["response"]["items"] == []
    and not any(x.get("kind") == "native-evidence-unavailable" for x in lim_e)
    and any(x.get("kind") == "unsupported-rung-omitted" for x in lim_e),
    "limitations": lim_e,
})

# unknown view digest
r_fv = go(req("graph.neighbors", {**nb_params, "factViewDigests": ["view2:" + "ab" * 32]}))
cases.append({"id": "fact-view-unavailable", "ok": (not r_fv["ok"]) and r_fv["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.FACT_VIEW_UNAVAILABLE"})

# imports projection
r_imp = go(req("graph.neighbors", {
    "relation": "imports", "minResolution": "resolved-target", "direction": "outgoing",
    "endpoint": ep("Unit.beta"),
}))
imp_items = r_imp["response"]["items"] if r_imp["ok"] else []
lim_i = ((r_imp.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
cases.append({
    "id": "imports-with-TA-projected-without-TA-omitted",
    "ok": r_imp["ok"] and len(imp_items) == 1 and imp_items[0]["target"]["kind"] == "package"
    and imp_items[0]["target"].get("packageManifestPath") == "Cargo.toml"
    and any(x.get("kind") == "unprojectable-fact" for x in lim_i),
    "items": imp_items,
    "limitations": lim_i,
})

cases.append({"id": "advisory-false", "ok": r_nb["ok"] and r_nb["response"]["context"]["advisory"] is False})
cases.append({"id": "resolvedView-runId-only", "ok": list(r_nb["response"]["context"]["resolvedView"].keys()) == ["runId"]})
cases.append({"id": "did-not-seal", "ok": r_nb.get("didNotSealRun") is True and r_file.get("didNotSealRun") is True})

bad_cur = "q3." + RUN.split(":")[-1] + "." + ("ee" * 32) + ".0"
r_cur = go(req("graph.neighbors", nb_params, page={"size": 1, "cursor": bad_cur}))
cases.append({"id": "cursor-bind-mismatch", "ok": (not r_cur["ok"]) and r_cur["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.CURSOR_MISMATCH"})

noreq_ok = False
try:
    execute_graph_query(req("graph.neighbors", nb_params), LOC, STORE.object_table, STORE.blobs, {"availability": "retained"}, close_run=close_retained_run)
except Exception as e:
    noreq_ok = getattr(e, "code", "") == "REFERENCE_CALL_PRECONDITION"
cases.append({"id": "host-requestId-precondition", "ok": noreq_ok})

# includeStart default false
r_rdef = go(req("graph.reach", {"relation": "calls", "minResolution": "resolved-callee", "start": ep("Unit.alpha"), "maxDepth": 8}))
starts = [row.get("endpoint", {}).get("nativeSubjectId") for row in (r_rdef.get("response") or {}).get("items") or []]
cases.append({"id": "includeStart-default-false", "ok": r_rdef["ok"] and "Unit.alpha" not in starts, "actual": starts})

# algorithmic traverse labeled
alg_edges = project_edges(
    [
        {"factId": G["facts"]["ab"], "relation": "calls", "resolution": "resolved-callee",
         "sourceUniverse": HEX_U, "targetUniverse": HEX_U,
         "payload": {"caller": "Unit.alpha", "resolvedCallee": "Unit.beta"}},
        {"factId": G["facts"]["ag"], "relation": "calls", "resolution": "resolved-callee",
         "sourceUniverse": HEX_U, "targetUniverse": HEX_U,
         "payload": {"caller": "Unit.alpha", "resolvedCallee": "Unit.gamma"}},
        {"factId": G["facts"]["bg"], "relation": "calls", "resolution": "resolved-callee",
         "sourceUniverse": HEX_U, "targetUniverse": HEX_U,
         "payload": {"caller": "Unit.beta", "resolvedCallee": "Unit.gamma"}},
    ],
    relation="calls", min_resolution="resolved-callee",
)
alg = traverse_projected_graph(edges=alg_edges, operation="graph.neighbors", params=nb_params)
cases.append({"id": "traverse-labeled-algorithmic", "ok": alg.get("label") == "algorithmic" and len(alg["items"]) == 2})

# schema inhabitance
schema_rows = []
for label, inst, doc, sel in [
    ("nb-req", req("graph.neighbors", nb_params), GQ, "#/$defs/GraphQueryRequestV1"),
    ("nb-resp", r_nb["response"], GQ, "#/$defs/GraphQueryResponseV1"),
    ("nb-env", r_nb["envelope"], CE, "#"),
    ("fail-file", r_file["envelope"], CE, "#"),
    ("qr", r_nb["envelope"]["query"], "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json", "#/$defs/QueryResult"),
]:
    r = validate_against(inst, doc, selector=sel, label=label)
    schema_rows.append({"label": label, "stockOk": r.get("stockOk"), "errors": (r.get("errors") or [])[:3]})
    cases.append({"id": f"schema-{label}", "ok": bool(r.get("stockOk")), "errors": (r.get("errors") or [])[:3]})

# frozen-store probe: no close_run, no fabricated edges, no claim of admission
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
        frame = blobs.get(rec.get("digest"))
        if not frame:
            continue
        try:
            parsed = parse_h_frame(frame)
            val = parsed["value"]
            relations.append((val.get("relation"), val.get("resolution")))
        except Exception:
            continue
    probe_req = req("graph.neighbors", nb_params, view={"runId": run_ids[0]} if run_ids else {"runId": RUN})
    measured = execute_graph_query(
        probe_req,
        {"runId": run_ids[0], "snapshotId": "unknown", "projectId": PRJ} if run_ids else LOC,
        table, blobs, host_base(), close_run=None,
    )
    store_probes.append({
        "store": name,
        "sha256": got,
        "matchesFrozen": got == exp["sha256"],
        "runIds": run_ids,
        "callsResolvedCalleePresent": ("calls", "resolved-callee") in relations,
        "importsResolvedTargetPresent": ("imports", "resolved-target") in relations,
        "executeWithoutCloseRun": {
            "ok": measured["ok"],
            "code": None if measured["ok"] else measured["envelope"]["termination"]["domainDetail"]["code"],
        },
        "didNotFabricateEdges": True,
        "closeRun": "not-executed",
        "completeGraphAdmission": "not-claimed",
    })

dump("query/charter-algorithmic-cases.json", {
    "label": "adapter-control-retained-graph + labeled-algorithmic-traverse",
    "notB12CompleteRun": True,
    "notFrozenStoreAdmission": True,
    "closeRun": "helper.query_projection.close_retained_run (H-frame rehash + run identity; not identity-and-evidence §3 complete graph)",
    "endpoints": ["Unit.alpha", "Unit.beta", "Unit.gamma"],
    "cases": cases,
    "neighborsResponse": r_nb["response"],
    "neighborsEnvelope": r_nb["envelope"],
    "pathResponse": r_path["response"],
    "reachResponse": r_reach["response"],
    "page1": r_page.get("response"),
    "page1QueryResult": (r_page.get("envelope") or {}).get("query"),
    "operationBound": r_bound,
    "failures": {
        "endpointUnknown": r_unk["envelope"],
        "malformed": r_mal["envelope"],
        "schemaMajor": r_maj["envelope"],
        "unsupported": r_file["envelope"],
        "packagePMP": r_pkg["envelope"],
        "latestMismatch": r_lat["envelope"],
        "viewAmbiguous": r_amb["envelope"],
        "purged": r_purge["envelope"],
        "noCloseRun": r_noclose["envelope"],
    },
    "rendererParity": r_nb["parity"],
    "didNotSealRun": True,
})
dump("query/frozen-store-probe.json", {
    "label": "frozen-store-bytes-without-close_run",
    "closeRun": "not-executed-out-of-scope",
    "didNotFabricateGraphEvidence": True,
    "completeGraphAdmission": "not-claimed",
    "probes": store_probes,
})
dump("query/parity.json", {
    "formats": ["human", "json", "agent"],
    "parityFields": ["resolved-view", "availability", "truncated", "total-items", "termination-class", "query-response"],
    "rendered": r_nb["parity"],
    "queryResult": r_nb["envelope"]["query"],
    "source": "adapter-control public wrapper; query-response is complete GraphQueryResponseV1; QueryResult compact summary joined",
})
dump("query/graph-query-bundle.json", {
    "underlyingRunAdmissionUnverified": True,
    "didNotClaimCloseRun": True,
    "completeGraphClose": False,
    "adapterControlRunId": RUN,
    "adapterControlLabel": G["label"],
    "frozenStoresNotRewritten": True,
    "publicWrapper": "execute_graph_query(request, run, objects, blobs, host) projects from admitted closure",
    "algorithmic": "traverse_projected_graph labeled algorithmic",
    "projectableRelation": ["calls", "resolved-callee"],
    "coverageId": (r_nb["response"]["context"]["evidence"]["coverageIds"] or [None])[0],
    "runId": RUN,
    "viewId": G["viewCalls"],
    "requests": {
        "neighbors": req("graph.neighbors", nb_params),
        "path": req("graph.path", path_params),
        "reach": req("graph.reach", reach_params),
    },
    "responses": {
        "neighbors": r_nb["response"],
        "path": r_path["response"],
        "reach": r_reach["response"],
        "neighborsPaged": r_page.get("response"),
        "neighborsPage2": r_page2.get("response") if isinstance(r_page2, dict) else None,
    },
    "failureEnvelope": r_file["envelope"],
    "unsupportedRelationRefusal": r_file["envelope"]["termination"]["domainDetail"]["code"],
    "cursor": {
        "nextCursor": page2_cur,
        "remainingNeighborFactId": ((r_page2.get("response") or {}).get("items") or [{}])[0].get("factId"),
    },
    "rendererParity": {"formats": ["human", "json", "agent"], "parityFields": sorted(["resolved-view", "availability", "truncated", "total-items", "termination-class", "query-response"]), "rendered": r_nb["parity"]},
    "queryResult": r_nb["envelope"]["query"],
    "casesOk": [c["id"] for c in cases if c["ok"]],
    "casesFail": [c["id"] for c in cases if not c["ok"]],
})

failed = [c["id"] for c in cases if not c["ok"]]
print("CHARTER_QUERY cases", len(cases), "fail", failed)
print("FROZEN", [(p["store"], p["callsResolvedCalleePresent"], p["executeWithoutCloseRun"]["code"]) for p in store_probes])
if failed:
    raise SystemExit(1)
print("OK")
