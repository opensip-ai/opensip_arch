"""Bounded graph-query schema + projection controls. Not product qualification.

Run:
  /tmp/opensip-architecture-review-env/bin/python -I -B check-query-projection.v3.py --report PATH
  /tmp/opensip-architecture-review-env/bin/python -I -B check-query-projection.v3.py --out PATH

Requires --report or --out. Fails on any required control. Reports limits.
Internal synthetic-admitted-fact-graph goldens test algorithm; they are not the
only evidence. Owner-admitted source-bound controls use identity close_run.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "foundation"))
import canonical  # noqa: E402
from jsonschema import ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

spec = importlib.util.spec_from_file_location("query_proj3", HERE / "query_projection_model.v3.py")
Q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Q)

E3 = HERE / "schemas" / "evaluator3"
WF = HERE / "schemas"
CHECKS = []
LIMITS = [
    "reference admission/projection only; not a product query engine or compiler qualification",
    "synthetic-admitted-fact-graph goldens test algorithm and cannot be the only evidence",
    "owner-admitted controls replay the semantic fixture through close_run; seed seal is discarded",
    "host.testBounds may only lower public visited/produced caps; schema Bounds constants unchanged",
    "historical workflows/schemas/graph-query.schema.json is not this owner and is not edited",
    "root still owns workflows-and-surfaces.md §8, launchers, source pins, and shared inventory count guards",
    "no all-suite pin rerun; no independent ACCEPT claimed by this checker",
]


def check(cid, ok, detail=""):
    CHECKS.append({"id": cid, "ok": bool(ok), "detail": "" if ok else str(detail)[:320], "required": True})
    return bool(ok)


def token(s):
    return hashlib.sha256(s.encode()).hexdigest()


def hid(prefix, s):
    return prefix + ":" + token(s)


SCHEMAS = {}
for p in sorted(E3.glob("*.schema.json")):
    doc = canonical.parse(p.read_bytes())
    SCHEMAS[doc["$id"]] = doc
for name in (
    "common.schema.json",
    "imported-evidence.schema.json",
    "policy-document.schema.json",
    "policy-document.v2.schema.json",
    "test-execution.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        SCHEMAS[doc["$id"]] = doc
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
)
U = "urn:opensip:product-v1:workflows:evaluator3:"
GQ = U + "graph-query:3"


def validator(ref):
    return canonical.ExactValidator({"$ref": ref}, registry=REG)


def valid(ref, value):
    try:
        canonical.typed(value)
        validator(ref).validate(value)
        return True, ""
    except (ValidationError, canonical.AdmissionError, Exception) as exc:
        return False, str(exc).splitlines()[0][:240]


def must_valid(cid, ref, value):
    ok, why = valid(ref, value)
    return check(cid, ok, why)


def must_invalid(cid, ref, value):
    ok, _ = valid(ref, value)
    return check(cid, not ok, "unexpectedly valid")


def refuse(cid, fn, error=None, detail=None):
    try:
        fn()
    except Q.QueryRefusal as exc:
        ok = True
        if error is not None:
            ok = ok and exc.error_code == error
        if detail is not None:
            ok = ok and exc.detail == detail
        term = exc.termination()
        tok, why = valid(U + "common:3#/$defs/StepTermination", term)
        return check(cid, ok and tok, "%s/%s %s" % (exc.error_code, exc.detail, why or term))
    except Exception as exc:
        return check(cid, False, type(exc).__name__ + ": " + str(exc).splitlines()[0][:240])
    return check(cid, False, "expected QueryRefusal")


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def ep(universe, kind, nid, manifest=None):
    row = {"universe": universe, "kind": kind, "nativeSubjectId": nid}
    if manifest is not None:
        row["packageManifestPath"] = manifest
    return row


def edge(label, src, dst, relation="references", resolution="resolved-binding"):
    return {
        "confidenceMillionths": 1000000,
        "factId": hid("fact2", "fact:" + label),
        "producerClosure": hid("closure2", "prod:" + label),
        "relation": relation,
        "resolution": resolution,
        "source": src,
        "target": dst,
    }


def project_id(label="proj"):
    return "prj1-" + token("project:" + label)


def run_id(label="run"):
    return hid("run3", "run:" + label)


def view_id(label="view"):
    return hid("view2", "view:" + label)


def snap_id(label="snap"):
    return hid("snapshot2", "snap:" + label)


def uni(label):
    return token("universe:" + label)


def request(operation, project, view, params, *, completeness="required", size=100, cursor=None, major=3):
    page = {"size": size}
    if cursor is not None:
        page["cursor"] = cursor
    return {
        "completeness": completeness,
        "operation": operation,
        "page": page,
        "params": params,
        "projectId": project,
        "schemaFamily": "opensip.product.query",
        "schemaMajor": major,
        "view": view,
    }


def synth_host(run, project, edges, *, views=None, **extra):
    host = {
        "admittedFactGraph": {
            "coverageIds": list(extra.get("coverageIds") or []),
            "deficiencies": list(extra.get("deficiencies") or []),
            "edges": edges,
            "factsExamined": extra.get("factsExamined", len(edges) or 1),
            "projectId": project,
            "resolutionLimitations": list(extra.get("resolutionLimitations") or []),
            "runId": run,
            "scopeIds": list(extra.get("scopeIds") or []),
            "snapshotId": extra.get("snapshotId") or snap_id(),
            "viewIds": list(views or [view_id()]),
        },
        "availability": extra.get("availability", "retained"),
        "cache": extra["cache"] if "cache" in extra else {},
        "latestRunId": extra.get("latestRunId", run),
        "standing": Q.SYNTHETIC_STANDING,
    }
    if extra.get("runsForSnapshot") is not None:
        host["runsForSnapshot"] = extra["runsForSnapshot"]
    if extra.get("testBounds") is not None:
        host["testBounds"] = extra["testBounds"]
    return host


def execute(req, host, run=None, objects=None, blobs=None):
    return Q.execute_graph_query(req, run=run, objects=objects, blobs=blobs, host=host)


def schema_controls():
    check("schema-id-major-3", SCHEMAS.get(GQ, {}).get("$id") == GQ and SCHEMAS[GQ].get("$defs", {}).get("GraphQueryRequestV1", {}).get("properties", {}).get("schemaMajor", {}).get("const") == 3, SCHEMAS.get(GQ, {}).get("$id"))
    ops = SCHEMAS[GQ]["$defs"]["Operation"]["enum"]
    check("twenty-operation-names", ops == [
        "run.show", "run.list", "finding.list", "finding.show", "fact.list", "coverage.show",
        "artifact.get", "graph.neighbors", "graph.path", "graph.reach", "baseline.show",
        "comparison.show", "comparison.diff", "candidate.list", "inspection.show", "review.brief",
        "policy.effective", "import.show", "receipt.show", "availability.show",
    ], str(ops))
    bounds = SCHEMAS[GQ]["$defs"]["Bounds"]["properties"]
    check("public-bounds-unchanged", [
        bounds["maxPageSize"]["const"], bounds["defaultPageSize"]["const"],
        bounds["maxItemsPerOperation"]["const"], bounds["maxTraversalDepth"]["const"],
        bounds["maxVisitedNodes"]["const"],
    ] == [1000, 100, 100000, 64, 1000000])
    check("advisory-ops-unchanged", SCHEMAS[GQ]["$defs"]["AdvisoryOperation"]["enum"] == [
        "comparison.diff", "candidate.list", "inspection.show", "review.brief",
    ])
    req_ref = GQ + "#/$defs/GraphQueryRequestV1"
    ctx_ref = GQ + "#/$defs/GraphOperationResponseContext"
    ng_ref = GQ + "#/$defs/GraphQueryResponseContext"
    rsp_ref = GQ + "#/$defs/GraphQueryResponseV1"
    u1 = token("u")
    endpoint = ep(u1, "symbol", "symbol:foo")
    base = request("graph.neighbors", project_id(), {"runId": run_id()}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": endpoint,
    })
    must_valid("req-neighbors-closed", req_ref, base)
    must_invalid("req-path-empty-params", req_ref, request("graph.path", project_id(), {"runId": run_id()}, {}))
    bad = copy.deepcopy(base)
    bad["params"]["baselineId"] = hid("baseline2", "b")
    must_invalid("req-neighbors-forbidden-baseline", req_ref, bad)
    path_lp = request("graph.path", project_id(), {"runId": run_id()}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "subject": "a.ts", "target": "b.ts", "maxDepth": 4,
    })
    must_invalid("req-path-logicalpath-refused", req_ref, path_lp)
    latest_req = copy.deepcopy(base)
    latest_req["view"] = {"latest": True}
    must_valid("req-latest-still-resolver", req_ref, latest_req)
    snap_req = copy.deepcopy(base)
    snap_req["view"] = {"snapshotId": snap_id()}
    must_valid("req-snapshot-still-resolver", req_ref, snap_req)
    major2 = copy.deepcopy(base)
    major2["schemaMajor"] = 2
    must_invalid("req-major-2-refused", req_ref, major2)
    finding = request("finding.show", project_id(), {"runId": run_id()}, {"findingId": hid("finding3", "f")})
    must_valid("req-finding-show-kept", req_ref, finding)
    reach = request("graph.reach", project_id(), {"runId": run_id()}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": endpoint, "maxDepth": 8, "includeStart": False,
    })
    must_valid("req-reach-include-start", req_ref, reach)
    reach_omit = copy.deepcopy(reach)
    del reach_omit["params"]["includeStart"]
    must_valid("req-reach-include-start-default-omitted", req_ref, reach_omit)
    ng_ctx = {
        "advisory": False, "availability": "retained", "coverage": "complete",
        "projectId": project_id(), "resolvedView": {"snapshotId": snap_id()},
        "totalItems": 0, "truncated": False,
    }
    must_valid("non-graph-snapshot-resolved-view", ng_ref, ng_ctx)
    must_invalid("graph-ctx-latest-forbidden", ctx_ref, {
        "advisory": False, "availability": "retained", "countBasis": "exact",
        "evidence": {"coverageIds": [], "deficiencyCitations": [], "resolutionLimitations": [], "scopeIds": []},
        "factViewDigests": [], "producedItems": 0, "projectId": project_id(),
        "resolvedView": {"latest": True}, "totalItems": 0, "traversalCoverage": "complete",
        "truncated": False, "visitedNodes": 0,
    })
    graph_ctx = {
        "advisory": False, "availability": "retained", "countBasis": "exact",
        "evidence": {"coverageIds": [], "deficiencyCitations": [], "resolutionLimitations": [], "scopeIds": []},
        "factViewDigests": [], "producedItems": 0, "projectId": project_id(),
        "resolvedView": {"runId": run_id()}, "totalItems": 0, "traversalCoverage": "complete",
        "truncated": False, "visitedNodes": 1,
    }
    must_valid("graph-ctx-run-only", ctx_ref, graph_ctx)
    adv_true = copy.deepcopy(graph_ctx)
    adv_true["advisory"] = True
    must_invalid("graph-advisory-true-refused", ctx_ref, adv_true)
    must_invalid("graph-unqualified-total-missing-countBasis", ctx_ref, {
        k: v for k, v in graph_ctx.items() if k != "countBasis"
    })
    rsp = {
        "schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "graph.neighbors",
        "context": graph_ctx, "items": [], "termination": {"class": "success"},
    }
    must_valid("rsp-neighbors-empty-complete", rsp_ref, rsp)
    rsp_latest = copy.deepcopy(rsp)
    rsp_latest["context"] = dict(graph_ctx, **{})
    # already run-only; a latest response is the ctx test above
    avail_rsp = {
        "schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "availability.show",
        "context": ng_ctx, "termination": {"class": "success"},
    }
    must_valid("rsp-availability-snapshot-view", rsp_ref, avail_rsp)
    diff_ctx = dict(ng_ctx, advisory=True, resolvedView={"runId": run_id()})
    must_valid("rsp-advisory-diff-true", rsp_ref, {
        "schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "comparison.diff",
        "context": diff_ctx,
    })


def table_controls():
    table = Q.projection_table()
    expected = {
        ("calls", "resolved-callee"),
        ("references", "resolved-binding"),
        ("imports", "resolved-target"),
        ("control-flow", "syntactic"),
        ("reachability", "from-resolved-calls"),
    }
    check("projection-table-five-binary-rungs", set(table) == expected, str(sorted(table)))
    forbidden = [
        ("calls", "syntactic-callee-name"), ("references", "syntactic-name-match"),
        ("imports", "syntactic-specifier"), ("file", "enumerated"), ("package", "manifest-declared"),
        ("declares", "syntactic"), ("types", "checked"), ("unresolved-edge", "observed"),
        ("clones", "normalized-body-hash"),
    ]
    check("projection-table-rejects-nonbinary", all(k not in table for k in forbidden), str([k for k in forbidden if k in table]))
    codes = json.loads((HERE.parent / "public-detail-registry.v1.json").read_text())["records"]
    have = {r["code"] for r in codes}
    needed = {
        "QUERY.CURSOR_MISMATCH", "QUERY.ENDPOINT_AMBIGUOUS", "QUERY.FACT_VIEW_UNAVAILABLE",
        "QUERY.PARAMS_MALFORMED", "QUERY.RELATION_UNSUPPORTED", "QUERY.VIEW_AMBIGUOUS",
    }
    check("registry-six-query-details", needed <= have, str(sorted(needed - have)))
    common = json.loads((E3 / "common.schema.json").read_text())["$defs"]["DomainDetailCode"]["enum"]
    hist = json.loads((WF / "common.schema.json").read_text())["$defs"]["DomainDetailCode"]["enum"]
    check("common-enums-mirror-query-details", needed <= set(common) and needed <= set(hist), "common=%s hist=%s" % (sorted(needed - set(common)), sorted(needed - set(hist))))
    inv = json.loads((HERE / "command-inventory.v3.json").read_text())
    query_cli = next(c["cli"] for c in inv["commands"] if c["name"] == "query")
    check("inventory-query-run3", "run3:" in query_cli and "run2:" not in query_cli, query_cli)


def algorithm_controls():
    u1, u2 = uni("u1"), uni("u2")
    a = ep(u1, "symbol", "symbol:a")
    b = ep(u1, "symbol", "symbol:b")
    c = ep(u1, "symbol", "symbol:c")
    a2 = ep(u2, "symbol", "symbol:a")
    project = project_id("alg")
    run_a = run_id("A")
    run_b = run_id("B")
    f1 = edge("p1", a, b)
    f2 = edge("p2", a, b)
    host = synth_host(run_a, project, [f1, f2])
    req = request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    })
    result = execute(req, host)
    check("dual-provenance-two-rows", len(result["items"]) == 2 and result["context"]["totalItems"] == 2 and result["context"]["countBasis"] == "exact", result["context"])
    check("dual-provenance-distinct-facts", {row["factId"] for row in result["items"]} == {f1["factId"], f2["factId"]})
    check("dual-provenance-order-fact2", result["items"][0]["factId"] < result["items"][1]["factId"], [r["factId"] for r in result["items"]])
    check("q3-evidence-required", set(result["context"]["evidence"]) == {"coverageIds", "scopeIds", "deficiencyCitations", "resolutionLimitations"})
    check("advisory-false", result["context"]["advisory"] is False)

    cycle = [edge("ab", a, b), edge("ba", b, a)]
    chost = synth_host(run_a, project, cycle)
    zero = execute(request("graph.path", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": a, "target": a, "maxDepth": 8,
    }), chost)
    check("path-start-eq-target-zero-hop", len(zero["items"]) == 1 and zero["items"][0]["hopCount"] == 0 and zero["items"][0]["edges"] == [], zero["items"])
    ab = execute(request("graph.path", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": a, "target": b, "maxDepth": 8,
    }), chost)
    check("path-shortest-not-cycle", len(ab["items"]) == 1 and ab["items"][0]["hopCount"] == 1, ab["items"])
    reach = execute(request("graph.reach", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": a, "maxDepth": 8, "includeStart": False,
    }), chost)
    ids = [row["endpoint"]["nativeSubjectId"] for row in reach["items"]]
    check("reach-default-excludes-start", ids == ["symbol:b"], ids)
    reach_s = execute(request("graph.reach", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": a, "maxDepth": 8, "includeStart": True,
    }), chost)
    ids_s = [row["endpoint"]["nativeSubjectId"] for row in reach_s["items"]]
    check("reach-include-start-true", ids_s == ["symbol:a", "symbol:b"], ids_s)

    # two universes: same native id is not a union
    cross = [edge("u1ab", a, b), edge("u2aa", a2, a2)]
    xhost = synth_host(run_a, project, cross)
    n1 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }), xhost)
    check("two-universes-not-union", len(n1["items"]) == 1 and n1["items"][0]["target"]["universe"] == u1, n1["items"])
    n2 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a2,
    }), xhost)
    check("two-universes-second-endpoint", len(n2["items"]) == 1 and n2["items"][0]["source"]["universe"] == u2, n2["items"])

    # tie-break shortest path: a-f2->c-f9->b vs a-f1->b ; wait a->b direct should win
    e_direct = edge("d1", a, b)
    e_long1 = edge("d2", a, c)
    e_long2 = edge("d3", c, b)
    thost = synth_host(run_a, project, [e_direct, e_long1, e_long2])
    sp = execute(request("graph.path", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": a, "target": b, "maxDepth": 8,
    }), thost)
    check("path-shortest-hop", sp["items"][0]["hopCount"] == 1 and sp["items"][0]["edges"][0]["factId"] == e_direct["factId"], sp["items"])

    # paging exact total; page fullness is not truncation
    many = [edge("n%d" % i, a, ep(u1, "symbol", "symbol:t%d" % i)) for i in range(5)]
    phost = synth_host(run_a, project, many)
    p1 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, size=2), phost)
    check("page-full-not-truncation", p1["context"]["traversalCoverage"] == "truncated-page" and p1["context"]["truncated"] is False and p1["context"]["countBasis"] == "exact" and p1["context"]["totalItems"] == 5, p1["context"])
    check("page-cursor-present", bool(p1["context"].get("nextCursor")))
    p2 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, size=2, cursor=p1["context"]["nextCursor"]), phost)
    p3 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, size=2, cursor=p2["context"]["nextCursor"]), phost)
    check("page-complete-last", p3["context"]["traversalCoverage"] == "complete" and p3["context"].get("nextCursor") is None and p3["context"]["countBasis"] == "exact", p3["context"])
    check("empty-cursor-not-alone-completeness", p3["context"]["traversalCoverage"] == "complete" and p3["context"]["countBasis"] == "exact")

    # latest A then B between pages
    host_latest = synth_host(run_a, project, many, latestRunId=run_a)
    first = execute(request("graph.neighbors", project, {"latest": True}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, size=2), host_latest)
    check("latest-resolves-once", first["context"]["resolvedView"]["runId"] == run_a)
    host_latest["latestRunId"] = run_b
    refuse("latest-page2-re-resolve-refused", lambda: execute(request("graph.neighbors", project, {"latest": True}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, size=2, cursor=first["context"]["nextCursor"]), host_latest), "REQUEST.PRECONDITION_FAILED", "QUERY.CURSOR_MISMATCH")
    cont = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, size=2, cursor=first["context"]["nextCursor"]), host_latest)
    check("latest-continue-bound-runA", cont["context"]["resolvedView"]["runId"] == run_a and len(cont["items"]) == 2, cont["context"])

    # cursor params changed
    refuse("cursor-params-changed", lambda: execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "incoming", "endpoint": a,
    }, size=2, cursor=first["context"]["nextCursor"]), phost), "REQUEST.PRECONDITION_FAILED", "QUERY.CURSOR_MISMATCH")

    # cache-delete exact resume
    cache = {}
    ch = synth_host(run_a, project, many, cache=cache)
    r1 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }), ch)
    check("cache-populated", len(cache) == 1, str(len(cache)))
    cache.clear()
    r2 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }), ch)
    check("cache-delete-exact-resume", [x["factId"] for x in r1["items"]] == [x["factId"] for x in r2["items"]] and r1["context"]["totalItems"] == r2["context"]["totalItems"])

    # purge unavailable
    refuse("purge-unavailable", lambda: execute(req, synth_host(run_a, project, [f1], availability="purged")), "HOST.IO_FAILURE", "evidence.purged")
    refuse("expired-unavailable", lambda: execute(req, synth_host(run_a, project, [f1], availability="expired")), "HOST.IO_FAILURE", "evidence.expired")
    refuse("corrupt-unavailable", lambda: execute(req, synth_host(run_a, project, [f1], availability="corrupt")), "HOST.IO_FAILURE", "evidence.corrupt")

    # view ambiguous
    refuse("snapshot-two-runs-ambiguous", lambda: execute(request("graph.neighbors", project, {"snapshotId": snap_id("s")}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }), synth_host(run_a, project, [f1], runsForSnapshot={snap_id("s"): [run_a, run_b]})), "REQUEST.PRECONDITION_FAILED", "QUERY.VIEW_AMBIGUOUS")
    refuse("snapshot-empty-unknown", lambda: execute(request("graph.neighbors", project, {"snapshotId": snap_id("none")}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }), synth_host(run_a, project, [f1], runsForSnapshot={})), "IDENTITY.UNKNOWN", None)

    refuse("relation-unsupported-types", lambda: execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "types", "minResolution": "checked", "direction": "outgoing", "endpoint": a,
    }), host), "REQUEST.PRECONDITION_FAILED", "QUERY.RELATION_UNSUPPORTED")
    refuse("relation-unsupported-syntactic-calls", lambda: execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "calls", "minResolution": "syntactic-callee-name", "direction": "outgoing", "endpoint": a,
    }), host), "REQUEST.PRECONDITION_FAILED", "QUERY.RELATION_UNSUPPORTED")
    refuse("schema-major-2-model", lambda: execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, major=2), host), "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", None)
    refuse("endpoint-missing-universe", lambda: execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "endpoint": {"kind": "symbol", "nativeSubjectId": "symbol:a", "universe": ""},
    }), host), "REQUEST.PRECONDITION_FAILED", None)

    # produced cap paging prefix; last page truncated-bound no cursor
    cap_host = synth_host(run_a, project, many, testBounds={"maxItemsPerOperation": 3})
    c1 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, completeness="best-effort", size=2), cap_host)
    check("produced-cap-page1-not-op-trunc-if-more-prefix", c1["context"]["traversalCoverage"] == "truncated-page" and c1["context"]["countBasis"] == "lower-bound" and c1["context"]["totalItems"] == 3, c1["context"])
    c2 = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, completeness="best-effort", size=2, cursor=c1["context"]["nextCursor"]), cap_host)
    check("produced-cap-last-truncated-bound-no-cursor", c2["context"]["traversalCoverage"] == "truncated-bound" and c2["context"].get("nextCursor") is None and c2["context"]["truncated"] is True, c2["context"])
    req_cap = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }, completeness="required", size=100), cap_host)
    check("required-completeness-unmet-at-produced-cap", req_cap["termination"]["class"] == "indeterminate" and req_cap["termination"]["reasonCodes"] == ["QUERY.COMPLETENESS_UNMET"], req_cap["termination"])

    # visited cap on reach chain; exactly-at-cap complete if queue empty
    chain = []
    nodes = [ep(u1, "symbol", "symbol:n%d" % i) for i in range(4)]
    for i in range(3):
        chain.append(edge("c%d" % i, nodes[i], nodes[i + 1]))
    exact_host = synth_host(run_a, project, chain, testBounds={"maxVisitedNodes": 4})
    exact_r = execute(request("graph.reach", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": nodes[0], "maxDepth": 8, "includeStart": True,
    }, completeness="required"), exact_host)
    check("exact-at-visited-cap-complete", exact_r["context"]["traversalCoverage"] == "complete" and exact_r["context"]["countBasis"] == "exact" and exact_r["termination"]["class"] == "success", exact_r["context"])
    over_host = synth_host(run_a, project, chain, testBounds={"maxVisitedNodes": 2})
    over_r = execute(request("graph.reach", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": nodes[0], "maxDepth": 8, "includeStart": True,
    }, completeness="required"), over_host)
    check("over-visited-cap-unmet", over_r["context"]["traversalCoverage"] == "truncated-bound" and over_r["termination"]["class"] == "indeterminate", over_r["context"])
    check("cursor-not-issued-past-visited-cap", over_r["context"].get("nextCursor") is None)

    # zero edges + resolution limitation disclosure
    empty_host = synth_host(run_a, project, [], resolutionLimitations=[{"kind": "resolution-incomplete", "note": "dynamic edge unresolved"}])
    empty = execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
    }), empty_host)
    check("zero-edges-not-absence", empty["context"]["totalItems"] == 0 and empty["context"]["countBasis"] == "exact" and empty["context"]["traversalCoverage"] == "complete", empty["context"])
    check("zero-edges-resolution-limitation", any(x.get("kind") == "resolution-incomplete" for x in empty["context"]["evidence"]["resolutionLimitations"]), empty["context"]["evidence"])

    # malformed extra property already schema-invalid
    refuse("view-digest-unknown", lambda: execute(request("graph.neighbors", project, {"runId": run_a}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a,
        "factViewDigests": [view_id("missing")],
    }), host), "REQUEST.PRECONDITION_FAILED", "QUERY.FACT_VIEW_UNAVAILABLE")


def owner_controls():
    foundation = HERE.parent / "foundation"
    S = load("query_semantic_fixture3", foundation / "evaluator_semantic_fixture.v3.py")
    replay = load("query_semantic_replay_check3", foundation / "check-semantic-replay.v3.py")
    atom = {"op": "exists", "relation": "references", "minResolution": "resolved-binding", "endpoint": "source", "filters": []}
    g = S.build_ts_semantic_graph(
        atom=atom, has_declares=False, has_references_fact=True, second_partition=True,
        references_resolved=True, second_universe=True, target_sidecar=True,
    )
    run, objects, blobs, actual = replay.close_positive(g)
    run_key = actual["runId"]
    project = run["projectId"]
    foo = replay.by_native(replay.symbol_items(g, g["u1"]), g["foo"])
    bar = replay.by_native(replay.symbol_items(g, g["u1"]), g["bar"])
    baz = replay.by_native(replay.symbol_items(g, g["u2"]), g["baz"])
    foo_ep = ep(g["u1"], "symbol", g["foo"])
    bar_ep = ep(g["u1"], "symbol", g["bar"])
    baz_ep = ep(g["u2"], "symbol", g["baz"])
    host = {"availability": "retained", "latestRunId": run_key, "cache": {}}
    neigh = execute(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    }), host, run, objects, blobs)
    check("owner-neighbors-foo-bar", len(neigh["items"]) == 1 and neigh["items"][0]["target"]["nativeSubjectId"] == g["bar"] and neigh["items"][0]["source"]["universe"] == g["u1"], neigh["items"])
    check("owner-resolved-run-only", neigh["context"]["resolvedView"] == {"runId": run_key})
    check("owner-evidence-coverage", len(neigh["context"]["evidence"]["coverageIds"]) >= 1, neigh["context"]["evidence"])
    check("owner-order-without-subject-object", neigh["items"][0]["factId"].startswith("fact2:"))
    path_same = execute(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": foo_ep, "maxDepth": 4,
    }), host, run, objects, blobs)
    check("owner-path-start-eq-target", path_same["items"][0]["hopCount"] == 0, path_same["items"])
    path_fb = execute(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": bar_ep, "maxDepth": 4,
    }), host, run, objects, blobs)
    check("owner-path-foo-bar", len(path_fb["items"]) == 1 and path_fb["items"][0]["hopCount"] == 1, path_fb["items"])
    path_cross = execute(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": baz_ep, "maxDepth": 8,
    }), host, run, objects, blobs)
    check("owner-two-universes-same-native-not-union", path_cross["items"] == [] and path_cross["context"]["countBasis"] == "exact", path_cross["context"])
    path_baz = execute(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": baz_ep, "target": foo_ep, "maxDepth": 8,
    }), host, run, objects, blobs)
    # baz -> foo is in u2; foo_ep is u1, so not the same endpoint
    check("owner-cross-universe-endpoint-distinct", path_baz["items"] == [], path_baz["items"])

    # mismatched view digest
    refuse("owner-mismatched-view", lambda: execute(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
        "factViewDigests": [view_id("not-on-run")],
    }), host, run, objects, blobs), "REQUEST.PRECONDITION_FAILED", "QUERY.FACT_VIEW_UNAVAILABLE")

    # corrupt payload: copy graph, wipe a referenced fact payload
    c_objects = copy.deepcopy(objects)
    c_blobs = copy.deepcopy(blobs)
    evidence = c_objects[run["evidenceId"]][1]
    victim = None
    for vid in evidence["viewIds"]:
        view = c_objects[vid][1]
        if view.get("facts"):
            victim = view["facts"][0]
            break
    check("owner-has-fact-to-corrupt", victim is not None, "no fact in views")
    if victim is not None:
        fact = c_objects[victim][1]
        digest = fact["payloadDigest"]
        c_blobs[digest] = b"not-the-retained-payload"
        refuse("owner-corrupt-payload", lambda: execute(request("graph.neighbors", project, {"runId": run_key}, {
            "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
        }), host, run, c_objects, c_blobs), "HOST.IO_FAILURE", "evidence.corrupt")
        del c_blobs[digest]
        refuse("owner-missing-payload", lambda: execute(request("graph.neighbors", project, {"runId": run_key}, {
            "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
        }), host, run, c_objects, c_blobs), "HOST.IO_FAILURE", "evidence.missing")

    # stale/mismatched fact listed on a view
    m_objects = copy.deepcopy(objects)
    m_blobs = copy.deepcopy(blobs)
    evidence = m_objects[run["evidenceId"]][1]
    vid0 = evidence["viewIds"][0]
    view0 = copy.deepcopy(m_objects[vid0][1])
    fake = hid("fact2", "mismatched-fact")
    view0["facts"] = sorted(set(list(view0.get("facts") or []) + [fake]))
    m_objects[vid0] = ("view", view0)
    refuse("owner-mismatched-fact", lambda: execute(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
        "factViewDigests": [vid0],
    }), host, run, m_objects, m_blobs), "HOST.IO_FAILURE", "evidence.corrupt")

    # partial resolution / zero projected edges with disclosure
    g0 = S.build_ts_semantic_graph(
        atom=atom, has_declares=False, has_references_fact=False, second_partition=True,
        references_resolved=False, second_universe=False,
    )
    run0, objects0, blobs0, actual0 = replay.close_positive(g0)
    foo0 = replay.by_native(replay.symbol_items(g0, g0["u1"]), g0["foo"])
    host0 = {"availability": "retained", "latestRunId": actual0["runId"]}
    zero = execute(request("graph.neighbors", run0["projectId"], {"runId": actual0["runId"]}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "endpoint": ep(g0["u1"], "symbol", g0["foo"]),
    }), host0, run0, objects0, blobs0)
    check("owner-partial-resolution-zero-edges", zero["items"] == [] and zero["context"]["countBasis"] == "exact", zero["context"])
    kinds = {x.get("kind") for x in zero["context"]["evidence"]["resolutionLimitations"]}
    check("owner-partial-resolution-disclosed", bool(kinds & {"resolution-incomplete", "coverage-unknown", "coverage-partial", "examined-not-exhaustive"}), str(kinds))
    check("owner-zero-not-native-absence", zero["context"]["traversalCoverage"] == "complete")
    check("owner-subjects-foo-bar-exist-for-identity", foo["row"]["nativeSubjectId"] == g["foo"] and bar["row"]["nativeSubjectId"] == g["bar"] and baz["row"]["nativeSubjectId"] == g["baz"])


def hook_control():
    P = load("workflow_projection_hook3", HERE / "workflow_projection_model.v3.py")
    owner = P.query_projection_owner()
    check("w-hook-loads-query-owner", owner.SCHEMA_ID == GQ, getattr(owner, "SCHEMA_ID", None))
    check("w-query-finding-unchanged", callable(P.query_finding))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report")
    parser.add_argument("--out")
    args = parser.parse_args()
    dest = args.report or args.out
    if not dest:
        sys.stderr.write("check-query-projection.v3.py requires --report or --out\n")
        raise SystemExit(2)
    schema_controls()
    table_controls()
    algorithm_controls()
    owner_controls()
    hook_control()
    failed = [c for c in CHECKS if not c["ok"]]
    report = {
        "checker": "check-query-projection.v3.py",
        "schemaId": GQ,
        "standing": "isolated query successor reference controls; not product qualification; not independent ACCEPT",
        "passed": not failed,
        "count": len(CHECKS),
        "failedCount": len(failed),
        "failed": failed,
        "checks": CHECKS,
        "limits": LIMITS,
        "newDomainDetails": [
            "QUERY.CURSOR_MISMATCH", "QUERY.ENDPOINT_AMBIGUOUS", "QUERY.FACT_VIEW_UNAVAILABLE",
            "QUERY.PARAMS_MALFORMED", "QUERY.RELATION_UNSUPPORTED", "QUERY.VIEW_AMBIGUOUS",
        ],
        "publicBounds": Q.PUBLIC_BOUNDS,
        "projectionTable": sorted("%s@%s" % (r, m) for r, m in Q.projection_table()),
    }
    text = json.dumps(report, indent=2) + "\n"
    out = Path(dest)
    if out.suffix == ".json":
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    else:
        out.mkdir(parents=True, exist_ok=True)
        (out / "check-query-projection.v3.json").write_text(text)
    sys.stdout.write(text)
    if failed:
        raise SystemExit(1)
    return report


if __name__ == "__main__":
    main()
