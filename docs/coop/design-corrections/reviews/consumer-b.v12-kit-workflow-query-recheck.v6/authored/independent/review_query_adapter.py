#!/usr/bin/env python3
"""Independent kit-derived recheck of S-origin v5 query wrapper.

Rechecks prior v5 findings AND remaining public request/result law.
Does not treat author 45-case self-report as oracle. Adapter-control is
not a B12 Run. Frozen stores are not admitted.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
from pathlib import Path

ISO = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v6/output/isolated-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v6/output")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v6/consumer-snapshot")
sys.path.insert(0, str(ISO))

from helper.canonical import C  # noqa: E402
from helper.query_projection import (  # noqa: E402
    close_retained_run,
    execute_graph_query,
)
from helper.store import Store  # noqa: E402

HEX_U = hashlib.sha256(b"opensip.reviewer.v6.universe").hexdigest()
PRJ = "prj1-" + hashlib.sha256(b"opensip.reviewer.v6.project").hexdigest()
HOST_RID = "req1_" + "11" * 16
SNAP_ID = "snapshot2:" + hashlib.sha256(b"opensip.reviewer.v6.snapshot").hexdigest()
PLAN_ID = "plan2:" + hashlib.sha256(b"opensip.reviewer.v6.plan").hexdigest()
CLOS = "closure2:" + hashlib.sha256(b"opensip.reviewer.v6.closure").hexdigest()
SCHEMA_D = hashlib.sha256(b"opensip.reviewer.v6.payload-schema").hexdigest()
EP_ID = "exec-plan2:" + hashlib.sha256(b"opensip.reviewer.v6.exec-plan").hexdigest()


def ep(name, kind="symbol", pmp=None):
    d = {"universe": HEX_U, "kind": kind, "nativeSubjectId": name}
    if pmp is not None:
        d["packageManifestPath"] = pmp
    return d


def mint(*, extra_eval_domains=None, isolated_omega=False, incomplete_cov=True, incoming=True, lawful_ei_only=False):
    """Reviewer scoped control with retained evidence+proof. Not a B12 Run."""
    store = Store()
    seal = "seal3:" + hashlib.sha256(b"rev-v6-seal").hexdigest()
    cap = hashlib.sha256(b"rev-v6-cap").hexdigest()

    def put_call(caller, callee, n):
        pd = store.put_canonical({"caller": caller, "resolvedCallee": callee}, label=f"pl-{n}")
        fact = {
            "schemaVersion": 2, "snapshotId": SNAP_ID, "relation": "calls", "resolution": "resolved-callee",
            "sourceUniverse": HEX_U, "targetUniverse": HEX_U, "producerClosure": CLOS,
            "payloadSchemaDigest": SCHEMA_D, "payloadDigest": pd, "anchors": [], "confidenceMillionths": 1000000,
        }
        return store.put_h("fact", fact, label=f"f-{n}")["typedId"]

    f_ab = put_call("Unit.alpha", "Unit.beta", 0)
    f_ag = put_call("Unit.alpha", "Unit.gamma", 1)
    scope = store.put_h("subject-scope", {
        "schemaVersion": 2, "snapshotId": SNAP_ID, "sourceUniverse": HEX_U, "targetUniverse": HEX_U,
        "relation": "calls", "resolution": "resolved-callee", "enumeratorClosure": CLOS,
        "subjects": ["Unit.alpha", "Unit.beta", "Unit.gamma"] + (["Unit.omega"] if isolated_omega else []),
    }, label="scope")["typedId"]
    cov_pl = store.put_canonical({
        "schemaVersion": 3,
        "key": {"relation": "calls", "resolution": "resolved-callee"},
        "entry": {
            "coverage": "unknown" if incomplete_cov else "complete",
            "deficiency": "resolution-incomplete" if incomplete_cov else None,
            "resolutionCompleteness": {
                "state": "incomplete" if incomplete_cov else "complete",
                "attempted": True,
                "examinedExhaustive": not incomplete_cov,
                "unresolvedEdgeCount": 2 if incomplete_cov else 0,
            },
        },
    }, label="cov-pl")
    cov_id = store.put_h("coverage", {"schemaVersion": 2, "scopeId": scope, "payloadSchemaDigest": SCHEMA_D, "payloadDigest": cov_pl}, label="cov")["typedId"]
    view_id = store.put_h("view", {
        "schemaVersion": 2, "planId": PLAN_ID, "scopeIds": [scope],
        "facts": sorted([f_ab, f_ag]), "coverageIds": [cov_id],
        "producerClosure": CLOS, "schemaDigests": [SCHEMA_D],
    }, label="view-calls")["typedId"]

    rows = [
        {"nativeSubjectId": "Unit.alpha", "kind": "symbol", "path": "a.rs", "qualifiedName": "Unit.alpha", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
        {"nativeSubjectId": "Unit.beta", "kind": "symbol", "path": "b.rs", "qualifiedName": "Unit.beta", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
        {"nativeSubjectId": "Unit.gamma", "kind": "symbol", "path": "c.rs", "qualifiedName": "Unit.gamma", "subjectLanguage": "rust", "signatureTokens": [], "projections": []},
    ]
    if isolated_omega:
        rows.append({"nativeSubjectId": "Unit.omega", "kind": "symbol", "path": "o.rs", "qualifiedName": "Unit.omega", "subjectLanguage": "rust", "signatureTokens": [], "projections": []})
    inv = {
        "schemaVersion": 1, "planId": PLAN_ID, "parameterDigest": "aa" * 32,
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "symbol", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [], "rows": rows,
    }
    inv_d = store.put_canonical(inv, label="inv")
    enum_plan = {
        "schemaVersion": 1, "snapshotId": SNAP_ID, "scopeDigest": "aa" * 32, "membershipDigest": "bb" * 32,
        "cells": [{
            "capabilityId": "syntax", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True,
            "kinds": ["symbol"],
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": CLOS},
                "nativeContextDigest": "cc" * 32, "universe": HEX_U, "programEntry": None, "extents": [],
            }],
        }],
    }
    enum_d = store.put_canonical(enum_plan, label="enum")
    inc_d = None
    if incoming:
        incoming_rec = {
            "schemaVersion": 1, "planId": PLAN_ID, "providerClosure": CLOS,
            "sourceUniverse": HEX_U, "targetUniverse": HEX_U,
            "relation": "calls", "minResolution": "resolved-callee",
            "completeSearch": False, "coverage": "unknown",
        }
        inc_d = store.put_canonical(incoming_rec, label="inc")

    eval_refs = [
        {"domain": "view", "digest": view_id.split(":")[-1]},
        {"domain": "coverage", "digest": cov_id.split(":")[-1]},
        {"domain": "subject-inventory", "digest": inv_d},
    ]
    if incoming and inc_d:
        eval_refs.append({"domain": "incoming-search", "digest": inc_d})
    if extra_eval_domains:
        eval_refs.extend(extra_eval_domains)
    if not lawful_ei_only:
        eval_refs.append({"domain": "enumeration-plan", "digest": enum_d})

    selected_refs = [r for r in eval_refs if r["domain"] != "enumeration-plan"]
    ei = {
        "schemaVersion": 1, "planId": PLAN_ID, "executionPlanId": EP_ID, "evaluatorClosure": CLOS,
        "enumerationPlanDigest": enum_d, "analysisSpecDigest": "dd" * 32,
        "hostCapture": {"schemaVersion": 1},
        "selectedRefs": selected_refs,
        "cellOutcomes": [{"ordinal": 0, "kinds": ["symbol"], "inventoryDigests": [inv_d]}],
        "nativeCoverageAccounts": [], "candidateResultRefs": [],
    }
    ei_d = store.put_canonical(ei, label="ei")
    if not lawful_ei_only:
        # author's adapter-control also lists execution-inputs via digest field, not selectedRefs
        pass
    eval_refs_proof = list(eval_refs)
    if lawful_ei_only:
        eval_refs_proof = list(selected_refs) + [{"domain": "execution-inputs", "digest": ei_d}]
    proof = {
        "schemaVersion": 3, "planId": PLAN_ID, "executionPlanId": EP_ID, "evaluatorClosure": CLOS,
        "ruleProgramDigest": "ee" * 32, "evaluationInputRefs": eval_refs_proof,
        "predicateProofs": [], "findingIds": [], "verdict": "pass", "evaluationState": "evaluated",
        "ruleResults": [], "waivedFindingIds": [], "executionDeficiencies": [],
        "executionInputsDigest": ei_d,
    }
    proof_id = store.put_h("proof-bundle", proof, label="proof")["typedId"]
    evidence = {
        "schemaVersion": 3, "planId": PLAN_ID, "viewIds": [view_id], "coverageIds": [cov_id],
        "importIds": [], "findingIds": [], "proofBundleId": proof_id,
    }
    ev_id = store.put_h("semantic-evidence", evidence, label="evidence")["typedId"]
    run_id = store.put_h("run", {
        "schemaVersion": 3, "projectId": PRJ, "snapshotId": SNAP_ID, "planId": PLAN_ID,
        "evidenceId": ev_id, "evaluationSealId": seal, "capabilityManifestId": cap,
    }, label="run")["typedId"]
    return {
        "store": store, "locator": {"runId": run_id, "snapshotId": SNAP_ID, "projectId": PRJ},
        "runId": run_id, "viewId": view_id, "covId": cov_id, "invD": inv_d, "enumD": enum_d,
        "facts": {"ab": f_ab, "ag": f_ag},
    }


G = mint()
STORE, LOC, RUN = G["store"], G["locator"], G["runId"]
nb = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("Unit.alpha")}


def req(op, params, page=None, view=None, completeness="best-effort"):
    return {
        "schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": PRJ,
        "view": view or {"runId": RUN}, "operation": op, "params": params,
        "completeness": completeness, "page": page or {"size": 100},
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


rows = []


def add(id_, ok, **extra):
    rec = {"id": id_, "ok": bool(ok), **extra}
    rows.append(rec)
    print(("PASS" if rec["ok"] else "FAIL"), id_, json.dumps({k: extra[k] for k in extra if k in {"detail", "actual", "actualTargets", "code"}}, default=str)[:200])


# --- prior findings recheck ---
r0 = go(req("graph.neighbors", nb))
add("baseline-neighbors-two-edges", r0["ok"] and len(r0["response"]["items"]) == 2, n=len(r0["response"]["items"]) if r0.get("ok") else None)

ghost = Store()
ghost.object_table = dict(STORE.object_table)
ghost.blobs = dict(STORE.blobs)
gpl = ghost.put_canonical({"caller": "Unit.alpha", "resolvedCallee": "Unit.ghost"}, label="g-pl")
gf = ghost.put_h("fact", {
    "schemaVersion": 2, "snapshotId": SNAP_ID, "relation": "calls", "resolution": "resolved-callee",
    "sourceUniverse": HEX_U, "targetUniverse": HEX_U, "producerClosure": CLOS,
    "payloadSchemaDigest": SCHEMA_D, "payloadDigest": gpl, "anchors": [], "confidenceMillionths": 1000000,
}, label="g-fact")["typedId"]
gview = ghost.put_h("view", {
    "schemaVersion": 2, "planId": PLAN_ID, "scopeIds": [], "facts": [gf], "coverageIds": [],
    "producerClosure": CLOS, "schemaDigests": [SCHEMA_D],
}, label="g-view")["typedId"]
rg = go(req("graph.neighbors", nb), store=ghost)
tgts = [e["target"]["nativeSubjectId"] for e in (rg.get("response") or {}).get("items") or []]
add("prior-extra-view2-must-not-become-admitted-fact-view", rg["ok"] and "Unit.ghost" not in tgts and set(tgts) == {"Unit.beta", "Unit.gamma"}, actualTargets=tgts, extraView=gview)

r_fv = go(req("graph.neighbors", {**nb, "factViewDigests": [gview]}), store=ghost)
add("explicit-unadmitted-view-unavailable", (not r_fv["ok"]) and r_fv["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.FACT_VIEW_UNAVAILABLE")

delta = Store()
delta.object_table = dict(STORE.object_table)
delta.blobs = dict(STORE.blobs)
delta.put_canonical({
    "schemaVersion": 1, "planId": PLAN_ID, "parameterDigest": "bb" * 32, "cellOrdinal": 9, "programOrdinal": 0,
    "kind": "symbol", "state": "complete", "deficiency": None, "nativeCause": None, "examinedPaths": [],
    "rows": [{"nativeSubjectId": "Unit.delta", "kind": "symbol", "path": "d.rs", "qualifiedName": "Unit.delta", "subjectLanguage": "rust", "signatureTokens": [], "projections": []}],
}, label="inv-delta")
rd = go(req("graph.neighbors", {**nb, "endpoint": ep("Unit.delta")}), store=delta)
dcode = None if rd.get("ok") else rd["envelope"]["termination"]["domainDetail"]["code"]
add("prior-unselected-inventory-must-not-admit-endpoint", dcode == "QUERY.ENDPOINT_UNKNOWN", actual=("ok" if rd.get("ok") else dcode))

lim = ((r0.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
add(
    "prior-coverage-entry-resolutionCompleteness-disclosed",
    any(x.get("kind") == "resolution-incomplete" and x.get("resolutionState") == "incomplete" for x in lim),
    limitations=[x for x in lim if "resolution" in x.get("kind", "") or x.get("kind") == "incoming-search-incomplete"],
)

add("incoming-search-incomplete-cited", any(x.get("kind") == "incoming-search-incomplete" for x in lim), limitations=lim)

# boolean closer without records
def synth_ok(run, objects=None, blobs=None):
    return {"ok": True}

rs = execute_graph_query(req("graph.neighbors", nb), LOC, STORE.object_table, STORE.blobs, host_base(), close_run=synth_ok)
add("boolean-close-run-without-records-view-unknown", (not rs["ok"]) and rs["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN")

# --- remaining law: EnumerationPlan from execution-inputs.enumerationPlanDigest (lawful refs only) ---
G2 = mint(isolated_omega=True, lawful_ei_only=True, incomplete_cov=False, incoming=False)
nb2 = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("Unit.omega")}

def go2(request, **more):
    kw = dict(run=G2["locator"], objects=G2["store"].object_table, blobs=G2["store"].blobs, host={
        "requestId": HOST_RID, "availability": "retained", "latestRunId": G2["runId"], "runsForSnapshot": {SNAP_ID: [G2["runId"]]},
    }, close_run=close_retained_run)
    kw.update(more)
    return execute_graph_query(request, kw["run"], kw["objects"], kw["blobs"], kw["host"], close_run=kw["close_run"])

req2 = {
    "schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": PRJ,
    "view": {"runId": G2["runId"]}, "operation": "graph.neighbors",
    "params": nb2, "completeness": "best-effort", "page": {"size": 100},
}
rw = go2(req2)
wcode = None if rw.get("ok") else rw["envelope"]["termination"]["domainDetail"]["code"]
# Isolated inventory vertex is lawful empty neighbors when universe comes from EnumerationPlan program binding.
# execution-inputs.enumerationPlanDigest is the owner; selectedRefs/evaluationInputRefs must not name domain=enumeration-plan.
add(
    "isolated-inventory-universe-from-execution-inputs-enumerationPlanDigest",
    rw.get("ok") is True and rw["response"]["items"] == [] and not any(
        x.get("kind") == "native-evidence-unavailable" for x in rw["response"]["context"]["evidence"]["resolutionLimitations"]
    ),
    actual=("ok-empty" if rw.get("ok") and rw["response"]["items"] == [] else wcode or "ok-nonempty"),
    law="query-projection-contract.v3.md §2 universe from EnumerationPlan program binding; execution-inputs.enumerationPlanDigest is the retained locator, not evaluationInputRefs domain=enumeration-plan",
)

# extra TA in store not in evaluationInputRefs must not project the unattributed import
# (imports not on this graph; skip if no import view)

# remaining public request/result law
add("file-enumerated-unsupported", (not go(req("graph.neighbors", {"relation": "file", "minResolution": "enumerated", "direction": "outgoing", "endpoint": ep("a.rs", "file")}))["ok"]))
r_pkg = go(req("graph.neighbors", {**nb, "endpoint": ep("demo", "package")}))
add("package-without-PMP-ambiguous", (not r_pkg["ok"]) and r_pkg["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.ENDPOINT_AMBIGUOUS")
rcache = go(req("graph.neighbors", nb), host=host_base(cache={"edges": "poison"}))
add("cache-ignored", rcache["ok"] and rcache.get("ignoredHost", {}).get("cache") is True and len(rcache["response"]["items"]) == 2)
rnc = execute_graph_query(req("graph.neighbors", nb), LOC, STORE.object_table, STORE.blobs, host_base(), close_run=None)
add("without-close-run-view-unknown", (not rnc["ok"]) and rnc["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN")
rempty = go(req("graph.neighbors", {**nb, "endpoint": ep("Unit.gamma")}))
add("empty-neighbors-not-native-unavailable", rempty["ok"] and rempty["response"]["items"] == [] and not any(x.get("kind") == "native-evidence-unavailable" for x in rempty["response"]["context"]["evidence"]["resolutionLimitations"]))
qr = r0["envelope"]["query"]
ctx = r0["response"]["context"]
add("compact-QueryResult-joins", qr["items"] == ctx["producedItems"] == 2 and qr["truncated"] is False and qr["completenessMet"] is True and qr["advisory"] is False)
par = r0["parity"]
six = all(par[f]["resolved-view"] == ctx["resolvedView"] and par[f]["query-response"] == r0["response"] and par[f]["truncated"] == ctx["truncated"] and par[f]["total-items"] == ctx["totalItems"] for f in ("human", "json", "agent"))
add("six-field-parity", six)

rpath = go(req("graph.path", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Unit.alpha"), "target": ep("Unit.gamma"), "maxDepth": 8}))
add("path-shortest-hop", rpath["ok"] and rpath["response"]["items"][0]["hopCount"] == 1)
rreach = go(req("graph.reach", {"relation": "calls", "minResolution": "resolved-callee", "start": ep("Unit.alpha"), "maxDepth": 8}))
starts = [row.get("endpoint", {}).get("nativeSubjectId") for row in rreach["response"]["items"]]
add("includeStart-default-false", rreach["ok"] and "Unit.alpha" not in starts, actual=starts)

rpage = go(req("graph.neighbors", nb, page={"size": 1}))
add("truncated-page-not-operation-truncation", rpage["ok"] and rpage["response"]["context"]["traversalCoverage"] == "truncated-page" and rpage["response"]["context"]["truncated"] is False and rpage["envelope"]["query"]["completenessMet"] is True)
rbound = go(req("graph.path", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Unit.alpha"), "target": ep("Unit.gamma"), "maxDepth": 8}), host=host_base(testBounds={"maxVisitedNodes": 1}))
add("operation-bound-truncated", rbound["ok"] and rbound["response"]["context"]["traversalCoverage"] == "truncated-bound" and rbound["envelope"]["query"]["completenessMet"] is False)

rhost = go(req("graph.neighbors", nb), host=host_base(targetAttributions={"poison": True}, standing={"x": 1}, evaluationDeficiencies=[{"x": 1}]))
add("host-standing-ta-deficiencies-ignored", rhost["ok"] and rhost["ignoredHost"]["targetAttributions"] and rhost["ignoredHost"]["standing"] and rhost["ignoredHost"]["evaluationDeficiencies"])

# frozen stores
frozen_expected = {
    "syntax-code.store.json": "2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7",
    "ts.store.json": "885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d",
    "rust.store.json": "67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315",
    "syntax-data.store.json": "1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092",
    "rust-partial-clones.store.json": "b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246",
}
probes = []
for name, exp in frozen_expected.items():
    p = SNAP / "runs" / name
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    doc = json.loads(p.read_bytes())
    table = doc["objectTable"]
    blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    measured = execute_graph_query(
        {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": PRJ, "view": {"runId": run_ids[0]},
         "operation": "graph.neighbors", "params": nb, "completeness": "best-effort", "page": {"size": 100}},
        {"runId": run_ids[0]}, table, blobs, host_base(), close_run=None,
    )
    probes.append({"store": name, "sha256": h, "match": h == exp, "code": None if measured["ok"] else measured["envelope"]["termination"]["domainDetail"]["code"]})
add("frozen-stores-byte-identical-view-unknown-without-close-run", all(x["match"] and x["code"] == "QUERY.VIEW_UNKNOWN" for x in probes), probes=probes)

man = json.loads((SNAP.parent / "consumer-snapshot" / "snapshot-manifest.json").read_text()) if False else json.loads((SNAP / "snapshot-manifest.json").read_text())
snap_ok = all(hashlib.sha256((SNAP / rec["path"]).read_bytes()).hexdigest() == rec["sha256"] for rec in man["files"])
add("input-snapshot-unmodified", snap_ok)

failed = [r["id"] for r in rows if not r["ok"]]
doc = {"standing": "Independent kit-derived recheck of prior v5 findings and remaining public wrapper law.", "n": len(rows), "nFail": len(failed), "failed": failed, "passed": [r["id"] for r in rows if r["ok"]], "firstFailure": failed[0] if failed else None, "cases": rows}
(OUT / "independent" / "review-query-measurements.json").write_text(json.dumps(doc, indent=2) + "\n")
print("INDEPENDENT n", len(rows), "fail", failed)
raise SystemExit(1 if failed else 0)
