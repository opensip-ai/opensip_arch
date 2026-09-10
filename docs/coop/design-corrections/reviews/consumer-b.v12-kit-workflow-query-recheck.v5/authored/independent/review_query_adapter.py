#!/usr/bin/env python3
"""Independent kit-derived discriminating measurements of S-origin query wrapper.

Does not treat author 40-case self-report as oracle. Does not admit frozen
stores. Does not invent a sixth B12 Run. Adapter-control graph is a scoped
control only.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ISO = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v5/output/isolated-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v5/output")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v5/consumer-snapshot")
sys.path.insert(0, str(ISO))

from helper.identity import typed_id  # noqa: E402
from helper.query_projection import (  # noqa: E402
    close_retained_run,
    execute_graph_query,
    load_closure_records,
)
from helper.store import Store  # noqa: E402

HEX_U = hashlib.sha256(b"opensip.reviewer.disc.universe").hexdigest()
PRJ = "prj1-" + hashlib.sha256(b"opensip.reviewer.disc.project").hexdigest()
HOST_RID = "req1_" + "ab" * 16
SNAP_ID = "snapshot2:" + hashlib.sha256(b"opensip.reviewer.disc.snapshot").hexdigest()
PLAN_ID = "plan2:" + hashlib.sha256(b"opensip.reviewer.disc.plan").hexdigest()
CLOS = "closure2:" + hashlib.sha256(b"opensip.reviewer.disc.closure").hexdigest()
SCHEMA_D = hashlib.sha256(b"opensip.reviewer.disc.payload-schema").hexdigest()


def ep(name, kind="symbol", pmp=None):
    d = {"universe": HEX_U, "kind": kind, "nativeSubjectId": name}
    if pmp is not None:
        d["packageManifestPath"] = pmp
    return d


def mint_scoped():
    """Reviewer-minted scoped control graph. Not a B12 complete Run."""
    store = Store()
    ev = "evidence3:" + hashlib.sha256(b"reviewer-disc-evidence").hexdigest()
    seal = "seal3:" + hashlib.sha256(b"reviewer-disc-seal").hexdigest()
    cap = hashlib.sha256(b"reviewer-disc-cap").hexdigest()
    run_body = {
        "schemaVersion": 3,
        "projectId": PRJ,
        "snapshotId": SNAP_ID,
        "planId": PLAN_ID,
        "evidenceId": ev,
        "evaluationSealId": seal,
        "capabilityManifestId": cap,
    }
    run_id = store.put_h("run", run_body, label="disc-run")["typedId"]

    def put_call(caller, callee, ordinal):
        payload = {"caller": caller, "resolvedCallee": callee}
        pd = store.put_canonical(payload, label=f"c-{ordinal}")
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
        return store.put_h("fact", fact, label=f"call-{ordinal}")["typedId"]

    f_ab = put_call("Unit.alpha", "Unit.beta", 0)
    f_ag = put_call("Unit.alpha", "Unit.gamma", 1)
    scope = store.put_h(
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
    # CoverageResultV3-shaped: resolutionCompleteness lives on entry, not payload top-level
    cov_pl = store.put_canonical(
        {
            "schemaVersion": 3,
            "key": {"relation": "calls", "resolution": "resolved-callee"},
            "entry": {
                "coverage": "complete",
                "resolutionCompleteness": {
                    "state": "incomplete",
                    "attempted": True,
                    "examinedExhaustive": False,
                    "unresolvedEdgeCount": 2,
                },
                "deficiency": "resolution-incomplete",
            },
        },
        label="cov-payload",
    )
    cov_id = store.put_h(
        "coverage",
        {"schemaVersion": 2, "scopeId": scope, "payloadSchemaDigest": SCHEMA_D, "payloadDigest": cov_pl},
        label="cov-calls",
    )["typedId"]
    view_id = store.put_h(
        "view",
        {
            "schemaVersion": 2,
            "planId": PLAN_ID,
            "scopeIds": [scope],
            "facts": sorted([f_ab, f_ag]),
            "coverageIds": [cov_id],
            "producerClosure": CLOS,
            "schemaDigests": [SCHEMA_D],
        },
        label="view-calls",
    )["typedId"]
    inv = {
        "schemaVersion": 1,
        "planId": PLAN_ID,
        "parameterDigest": "aa" * 32,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "symbol",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": [],
        "rows": [
            {"nativeSubjectId": "Unit.alpha", "kind": "symbol", "path": "a.rs", "qualifiedName": "Unit.alpha", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
            {"nativeSubjectId": "Unit.beta", "kind": "symbol", "path": "b.rs", "qualifiedName": "Unit.beta", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
            {"nativeSubjectId": "Unit.gamma", "kind": "symbol", "path": "c.rs", "qualifiedName": "Unit.gamma", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
        ],
    }
    store.put_canonical(inv, label="inv-symbol")
    locator = {"runId": run_id, "snapshotId": SNAP_ID, "projectId": PRJ}
    return {
        "store": store,
        "locator": locator,
        "runId": run_id,
        "viewId": view_id,
        "facts": {"ab": f_ab, "ag": f_ag},
        "covId": cov_id,
        "evidenceId": ev,
        "label": "reviewer-scoped-control-not-b12-run",
    }


G = mint_scoped()
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
    h = {"requestId": HOST_RID, "availability": "retained", "latestRunId": RUN, "runsForSnapshot": {SNAP_ID: [RUN]}}
    h.update(more)
    return h


def go(request, store=None, locator=None, **more):
    st = store or STORE
    loc = locator or LOC
    kw = dict(run=loc, objects=st.object_table, blobs=st.blobs, host=host_base(), close_run=close_retained_run)
    kw.update(more)
    return execute_graph_query(request, kw["run"], kw["objects"], kw["blobs"], kw["host"], close_run=kw["close_run"])


nb = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("Unit.alpha")}
rows = []


def add(id_, ok, **extra):
    rec = {"id": id_, "ok": bool(ok), **extra}
    rows.append(rec)
    print(("PASS" if rec["ok"] else "FAIL"), id_, extra.get("detail", ""))


# --- independently derived expected behavior from contract ---
r0 = go(req("graph.neighbors", nb))
add(
    "baseline-neighbors-two-edges",
    r0["ok"] and len(r0["response"]["items"]) == 2,
    n=len(r0["response"]["items"]) if r0.get("ok") else None,
)
add("close-retained-run-not-complete-graph", close_retained_run(LOC, STORE.object_table, STORE.blobs).get("completeGraphClose") is False)
add("run-evidenceId-not-retained", G["evidenceId"] not in STORE.object_table, evidenceId=G["evidenceId"])
add("wrapper-does-not-require-evidence-record", r0["ok"] is True, note="queries succeed while Run.evidenceId is an unreained locator; authority is object-table scan")

# extra view2 with ghost calls fact: NOT on any evidence.viewIds (none exist)
ghost_store = Store()
ghost_store.object_table = dict(STORE.object_table)
ghost_store.blobs = dict(STORE.blobs)
ghost_pl = ghost_store.put_canonical({"caller": "Unit.alpha", "resolvedCallee": "Unit.ghost"}, label="ghost-pl")
ghost_fact = {
    "schemaVersion": 2,
    "snapshotId": SNAP_ID,
    "relation": "calls",
    "resolution": "resolved-callee",
    "sourceUniverse": HEX_U,
    "targetUniverse": HEX_U,
    "producerClosure": CLOS,
    "payloadSchemaDigest": SCHEMA_D,
    "payloadDigest": ghost_pl,
    "anchors": [],
    "confidenceMillionths": 1000000,
}
ghost_fid = ghost_store.put_h("fact", ghost_fact, label="ghost-fact")["typedId"]
ghost_view = ghost_store.put_h(
    "view",
    {
        "schemaVersion": 2,
        "planId": PLAN_ID,
        "scopeIds": [],
        "facts": [ghost_fid],
        "coverageIds": [],
        "producerClosure": CLOS,
        "schemaDigests": [SCHEMA_D],
    },
    label="ghost-view",
)["typedId"]
r_ghost = go(req("graph.neighbors", nb), store=ghost_store)
ghost_targets = [e["target"]["nativeSubjectId"] for e in (r_ghost.get("response") or {}).get("items") or []]
# Contract §1: admitted views of THIS Run. Extra view2 is unrelated stored data.
# Expected: neighbors remain {beta, gamma}. Actual leak would include ghost.
add(
    "extra-view2-must-not-become-admitted-fact-view",
    r_ghost["ok"] and "Unit.ghost" not in ghost_targets and set(ghost_targets) == {"Unit.beta", "Unit.gamma"},
    actualTargets=ghost_targets,
    extraView=ghost_view,
    law="query-projection-contract.v3.md §1 fact-view set is admitted views of this Run, not every view2 blob",
)

# extra inventory row Unit.delta not on evaluationInputRefs (no proof exists)
delta_store = Store()
delta_store.object_table = dict(STORE.object_table)
delta_store.blobs = dict(STORE.blobs)
inv_delta = {
    "schemaVersion": 1,
    "planId": PLAN_ID,
    "parameterDigest": "bb" * 32,
    "cellOrdinal": 9,
    "programOrdinal": 0,
    "kind": "symbol",
    "state": "complete",
    "deficiency": None,
    "nativeCause": None,
    "examinedPaths": [],
    "rows": [
        {"nativeSubjectId": "Unit.delta", "kind": "symbol", "path": "d.rs", "qualifiedName": "Unit.delta", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
    ],
}
delta_store.put_canonical(inv_delta, label="inv-unselected")
r_delta = go(req("graph.neighbors", {**nb, "endpoint": ep("Unit.delta")}), store=delta_store)
delta_code = None if r_delta.get("ok") else r_delta["envelope"]["termination"]["domainDetail"]["code"]
# Contract §2: vertex domain from inventories selected by proof evaluationInputRefs.
# Unselected inventory is unrelated stored data → ENDPOINT_UNKNOWN.
add(
    "unselected-inventory-must-not-admit-endpoint",
    delta_code == "QUERY.ENDPOINT_UNKNOWN",
    actual=("ok" if r_delta.get("ok") else delta_code),
    law="query-projection-contract.v3.md §2 inventory rows selected by admitted proof evaluationInputRefs",
)

# CoverageResultV3 entry.resolutionCompleteness.state=incomplete must be disclosed
lim = ((r0.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
add(
    "coverage-entry-resolutionCompleteness-disclosed",
    any(x.get("kind") == "resolution-incomplete" or x.get("resolutionState") == "incomplete" for x in lim),
    limitations=lim,
    law="query-projection-contract.v3.md §6 copies native resolutionCompleteness.state from CoverageResultV3 entry",
)

# file@enumerated refused
r_file = go(req("graph.neighbors", {"relation": "file", "minResolution": "enumerated", "direction": "outgoing", "endpoint": ep("a.rs", "file")}))
add(
    "file-enumerated-unsupported",
    (not r_file["ok"]) and r_file["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED",
)

# package without PMP
r_pkg = go(req("graph.neighbors", {**nb, "endpoint": ep("demo", "package")}))
add(
    "package-without-PMP-ambiguous",
    (not r_pkg["ok"]) and r_pkg["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.ENDPOINT_AMBIGUOUS",
)

# cache ignored
r_cache = go(req("graph.neighbors", nb), host=host_base(cache={"edges": "poison"}))
add("cache-ignored", r_cache["ok"] and r_cache.get("ignoredHost", {}).get("cache") is True and len(r_cache["response"]["items"]) == 2)

# close_run None
r_nc = execute_graph_query(req("graph.neighbors", nb), LOC, STORE.object_table, STORE.blobs, host_base(), close_run=None)
add("without-close-run-view-unknown", (not r_nc["ok"]) and r_nc["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN")

# empty neighbors at gamma not native-unavailable
r_empty = go(req("graph.neighbors", {**nb, "endpoint": ep("Unit.gamma")}))
lim_e = ((r_empty.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
add(
    "empty-neighbors-not-native-unavailable",
    r_empty["ok"] and r_empty["response"]["items"] == [] and not any(x.get("kind") == "native-evidence-unavailable" for x in lim_e),
    limitations=lim_e,
)

# QueryResult joins
qr = r0["envelope"]["query"]
ctx = r0["response"]["context"]
add(
    "compact-QueryResult-joins",
    qr["items"] == ctx["producedItems"] == 2 and qr["truncated"] is False and qr["completenessMet"] is True and qr["advisory"] is False,
    queryResult=qr,
)

# six-field
par = r0["parity"]
six = all(
    par[f]["resolved-view"] == ctx["resolvedView"]
    and par[f]["availability"] == ctx["availability"]
    and par[f]["truncated"] == ctx["truncated"]
    and par[f]["total-items"] == ctx["totalItems"]
    and par[f]["query-response"] == r0["response"]
    for f in ("human", "json", "agent")
)
add("six-field-parity", six)

# load_closure_records scans all view2
recs = load_closure_records(ghost_store, run_id=RUN, run_body={"snapshotId": SNAP_ID, "projectId": PRJ, "planId": PLAN_ID})
add(
    "load_closure_records-includes-unselected-view2",
    ghost_view in recs["views"],
    nViews=len(recs["views"]),
    note="call-graph: load_closure_records iterates object_table view2: keys, not evidence.viewIds",
)

# frozen stores: hashes + without close_run
frozen_expected = {
    "syntax-code.store.json": "2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7",
    "ts.store.json": "885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d",
    "rust.store.json": "67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315",
    "syntax-data.store.json": "1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092",
    "rust-partial-clones.store.json": "b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246",
}
frozen_rows = []
for name, exp in frozen_expected.items():
    p = SNAP / "runs" / name
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    doc = json.loads(p.read_bytes())
    table = doc["objectTable"]
    blobs = {k: __import__("base64").b64decode(v) for k, v in doc["blobs"].items()}
    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    measured = execute_graph_query(
        {
            "schemaFamily": "opensip.product.query",
            "schemaMajor": 3,
            "projectId": PRJ,
            "view": {"runId": run_ids[0]},
            "operation": "graph.neighbors",
            "params": nb,
            "completeness": "best-effort",
            "page": {"size": 100},
        },
        {"runId": run_ids[0]},
        table,
        blobs,
        host_base(),
        close_run=None,
    )
    frozen_rows.append({
        "store": name,
        "sha256": h,
        "matchesExpectedFrozen": h == exp,
        "executeWithoutCloseRun": None if measured["ok"] else measured["envelope"]["termination"]["domainDetail"]["code"],
        "didNotClaimAdmission": True,
    })
add("frozen-stores-byte-identical-and-view-unknown-without-close-run", all(x["matchesExpectedFrozen"] and x["executeWithoutCloseRun"] == "QUERY.VIEW_UNKNOWN" for x in frozen_rows), probes=frozen_rows)

# snapshot unmodified
man = json.loads(Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v5/snapshot-manifest.json").read_text())
snap_ok = True
for rec in man["files"]:
    hp = hashlib.sha256((SNAP / rec["path"]).read_bytes()).hexdigest()
    if hp != rec["sha256"]:
        snap_ok = False
        break
add("input-snapshot-unmodified", snap_ok)

failed = [r["id"] for r in rows if not r["ok"]]
passed = [r["id"] for r in rows if r["ok"]]
doc = {
    "standing": "Independent kit-derived discriminating measurements. Adapter-control is not B12 Run admission.",
    "n": len(rows),
    "nFail": len(failed),
    "failed": failed,
    "passed": passed,
    "cases": rows,
    "firstFailure": failed[0] if failed else None,
}
(OUT / "independent" / "review-query-measurements.json").write_text(json.dumps(doc, indent=2) + "\n")
print("INDEPENDENT n", len(rows), "fail", failed)
raise SystemExit(1 if failed else 0)
