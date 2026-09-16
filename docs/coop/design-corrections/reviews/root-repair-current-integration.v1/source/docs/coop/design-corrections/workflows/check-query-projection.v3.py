"""Bounded graph-query schema + projection controls. Not product qualification.

Run:
  /tmp/opensip-architecture-review-env/bin/python -I -B check-query-projection.v3.py --report PATH
  /tmp/opensip-architecture-review-env/bin/python -I -B check-query-projection.v3.py --out PATH

Requires --report or --out. Fails on any required control. Reports limits.
traverse_projected_graph goldens test algorithm only. Owner-admitted controls
use identity close_run. execute_graph_query cannot be bypassed by host.standing.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import inspect
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
    "traverse_projected_graph goldens test algorithm and cannot be the only evidence",
    "owner-admitted controls replay the semantic fixture through close_run; seed seal is discarded",
    "host.testBounds may only lower public visited/produced caps; schema Bounds constants unchanged",
    "historical workflows/schemas/graph-query.schema.json is not this owner and is not edited",
    "root owns workflows-and-surfaces.md §8, launchers, source pins, and shared inventory count guards",
    "no all-suite pin rerun; no independent ACCEPT claimed by this checker",
    "imports@resolved-target uses the same reconciled occupancy as atom matching; owner-admitted execute_graph_query covers mapped file, exact-id symbol without sidecar, unknown sidecar plus unique inventory, and genuine unmapped limitation",
    "native incomplete resolutionState is mapped from completeness_from_stage; the semantic fixture unresolved path remains not-attempted",
    "host-defect controls monkeypatch close_run or the loaded replay comparison in this process only and always restore; they model an untyped host failure, not a product fault injector",
    "host_adapter_refusal and observe_retained_availability are reference adapter laws; no product host adapter or evidence store is implemented",
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
    "policy-test.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        SCHEMAS[doc["$id"]] = doc
_native_schema = canonical.parse((HERE.parent / "native" / "native-evidence.schemas.v2.json").read_bytes())
SCHEMAS[_native_schema["$id"]] = _native_schema
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


def host_obs(**kw):
    body = {"requestId": "req1_" + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    body.update(kw)
    return body


def refuse(cid, fn, error=None, detail=None, envelope=True):
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
        env_ok, env_why = True, ""
        if envelope:
            try:
                env = exc.envelope()
                env_ok, env_why = valid(U + "command-envelope:3", env)
                env_ok = env_ok and env.get("kind") == "failure" and "run" not in env and env.get("errors")
            except Exception as env_exc:
                env_ok, env_why = False, type(env_exc).__name__ + ": " + str(env_exc).splitlines()[0][:160]
        return check(cid, ok and tok and env_ok, "%s/%s %s %s" % (exc.error_code, exc.detail, why, env_why))
    except Q.ReferenceCallPrecondition as exc:
        return check(cid, False, "reference-call precondition: " + str(exc))
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
    snap_req["view"] = {"snapshotId": hid("snapshot2", "s")}
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
    ng_ctx = {
        "advisory": False, "availability": "retained", "coverage": "complete",
        "projectId": project_id(), "resolvedView": {"snapshotId": hid("snapshot2", "s")},
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
    avail_rsp = {
        "schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "availability.show",
        "context": ng_ctx, "termination": {"class": "success"},
    }
    must_valid("rsp-availability-snapshot-view", rsp_ref, avail_rsp)
    # Admission must enforce the exact advisory-operation set in both directions.
    # These carrier controls do not claim an independently replayed graph.
    for operation in ("run.show", "finding.list", "availability.show"):
        response = copy.deepcopy(avail_rsp)
        response["operation"] = operation
        must_valid("rsp-nonadvisory-false-" + operation, rsp_ref, response)
        response["context"]["advisory"] = True
        must_invalid("rsp-nonadvisory-true-" + operation, rsp_ref, response)
    for operation in ("comparison.diff", "candidate.list", "inspection.show", "review.brief"):
        response = copy.deepcopy(avail_rsp)
        response["operation"] = operation
        response["context"]["advisory"] = True
        must_valid("rsp-advisory-true-" + operation, rsp_ref, response)
        response["context"]["advisory"] = False
        must_invalid("rsp-advisory-false-" + operation, rsp_ref, response)
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
        "QUERY.CURSOR_MISMATCH", "QUERY.ENDPOINT_AMBIGUOUS", "QUERY.ENDPOINT_UNKNOWN",
        "QUERY.FACT_VIEW_UNAVAILABLE", "QUERY.PARAMS_MALFORMED", "QUERY.RELATION_UNSUPPORTED",
        "QUERY.SCHEMA_MAJOR_UNSUPPORTED", "QUERY.VIEW_AMBIGUOUS", "QUERY.VIEW_UNKNOWN",
    }
    check("registry-query-details", needed <= have, str(sorted(needed - have)))
    common = json.loads((E3 / "common.schema.json").read_text())["$defs"]["DomainDetailCode"]["enum"]
    hist = json.loads((WF / "common.schema.json").read_text())["$defs"]["DomainDetailCode"]["enum"]
    check("common-enums-mirror-query-details", needed <= set(common) and needed <= set(hist), "common=%s hist=%s" % (sorted(needed - set(common)), sorted(needed - set(hist))))
    inv = json.loads((HERE / "command-inventory.v3.json").read_text())
    query_cli = next(c["cli"] for c in inv["commands"] if c["name"] == "query")
    check("inventory-query-run3", "run3:" in query_cli and "run2:" not in query_cli, query_cli)


def algorithm_controls():
    u1, u2 = token("universe:u1"), token("universe:u2")
    a = ep(u1, "symbol", "symbol:a")
    b = ep(u1, "symbol", "symbol:b")
    c = ep(u1, "symbol", "symbol:c")
    a2 = ep(u2, "symbol", "symbol:a")
    prj, rid = project_id("alg"), run_id("A")
    f1, f2 = edge("p1", a, b), edge("p2", a, b)
    neigh = {
        "direction": "outgoing", "endpoint": a, "minResolution": "resolved-binding", "relation": "references",
    }
    result = Q.traverse_projected_graph("graph.neighbors", neigh, [f1, f2], project_id=prj, run_id=rid)
    check("dual-provenance-two-rows", len(result["items"]) == 2 and result["context"]["totalItems"] == 2 and result["context"]["countBasis"] == "exact", result["context"])
    check("dual-provenance-distinct-facts", {row["factId"] for row in result["items"]} == {f1["factId"], f2["factId"]})
    check("dual-provenance-order-fact2", result["items"][0]["factId"] < result["items"][1]["factId"], [r["factId"] for r in result["items"]])
    check("advisory-false", result["context"]["advisory"] is False)

    cycle = [edge("ab", a, b), edge("ba", b, a)]
    path_params = {
        "direction": "outgoing", "maxDepth": 8, "minResolution": "resolved-binding",
        "relation": "references", "start": a, "target": a,
    }
    zero = Q.traverse_projected_graph("graph.path", path_params, cycle, project_id=prj, run_id=rid)
    check("path-start-eq-target-zero-hop", len(zero["items"]) == 1 and zero["items"][0]["hopCount"] == 0 and zero["items"][0]["edges"] == [], zero["items"])
    path_ab = dict(path_params, target=b)
    ab = Q.traverse_projected_graph("graph.path", path_ab, cycle, project_id=prj, run_id=rid)
    check("path-shortest-not-cycle", len(ab["items"]) == 1 and ab["items"][0]["hopCount"] == 1, ab["items"])
    reach_p = {
        "direction": "outgoing", "includeStart": False, "maxDepth": 8,
        "minResolution": "resolved-binding", "relation": "references", "start": a,
    }
    reach = Q.traverse_projected_graph("graph.reach", reach_p, cycle, project_id=prj, run_id=rid)
    ids = [row["endpoint"]["nativeSubjectId"] for row in reach["items"]]
    check("reach-default-excludes-start", ids == ["symbol:b"], ids)
    reach_s = Q.traverse_projected_graph("graph.reach", dict(reach_p, includeStart=True), cycle, project_id=prj, run_id=rid)
    ids_s = [row["endpoint"]["nativeSubjectId"] for row in reach_s["items"]]
    check("reach-include-start-true", ids_s == ["symbol:a", "symbol:b"], ids_s)

    cross = [edge("u1ab", a, b), edge("u2aa", a2, a2)]
    n1 = Q.traverse_projected_graph("graph.neighbors", neigh, cross, project_id=prj, run_id=rid)
    check("two-universes-not-union", len(n1["items"]) == 1 and n1["items"][0]["target"]["universe"] == u1, n1["items"])
    n2 = Q.traverse_projected_graph("graph.neighbors", dict(neigh, endpoint=a2), cross, project_id=prj, run_id=rid)
    check("two-universes-second-endpoint", len(n2["items"]) == 1 and n2["items"][0]["source"]["universe"] == u2, n2["items"])

    e_direct, e_long1, e_long2 = edge("d1", a, b), edge("d2", a, c), edge("d3", c, b)
    sp = Q.traverse_projected_graph("graph.path", path_ab, [e_direct, e_long1, e_long2], project_id=prj, run_id=rid)
    check("path-shortest-hop", sp["items"][0]["hopCount"] == 1 and sp["items"][0]["edges"][0]["factId"] == e_direct["factId"], sp["items"])

    many = [edge("n%d" % i, a, ep(u1, "symbol", "symbol:t%d" % i)) for i in range(5)]
    p1 = Q.traverse_projected_graph("graph.neighbors", neigh, many, page={"size": 2}, project_id=prj, run_id=rid)
    check("page-full-not-truncation", p1["context"]["traversalCoverage"] == "truncated-page" and p1["context"]["truncated"] is False and p1["context"]["countBasis"] == "exact" and p1["context"]["totalItems"] == 5, p1["context"])
    p2 = Q.traverse_projected_graph("graph.neighbors", neigh, many, page={"size": 2, "cursor": p1["context"]["nextCursor"]}, project_id=prj, run_id=rid)
    p3 = Q.traverse_projected_graph("graph.neighbors", neigh, many, page={"size": 2, "cursor": p2["context"]["nextCursor"]}, project_id=prj, run_id=rid)
    check("page-complete-last", p3["context"]["traversalCoverage"] == "complete" and p3["context"].get("nextCursor") is None and p3["context"]["countBasis"] == "exact", p3["context"])

    refuse("cursor-params-changed", lambda: Q.traverse_projected_graph(
        "graph.neighbors", dict(neigh, direction="incoming"), many,
        page={"size": 2, "cursor": p1["context"]["nextCursor"]}, project_id=prj, run_id=rid,
    ), "REQUEST.PRECONDITION_FAILED", "QUERY.CURSOR_MISMATCH", envelope=False)

    cap = dict(Q.PUBLIC_BOUNDS, maxItemsPerOperation=3)
    c1 = Q.traverse_projected_graph("graph.neighbors", neigh, many, bounds=cap, completeness="best-effort", page={"size": 2}, project_id=prj, run_id=rid)
    check("produced-cap-page1", c1["context"]["traversalCoverage"] == "truncated-page" and c1["context"]["countBasis"] == "lower-bound" and c1["context"]["totalItems"] == 3, c1["context"])
    c2 = Q.traverse_projected_graph("graph.neighbors", neigh, many, bounds=cap, completeness="best-effort", page={"size": 2, "cursor": c1["context"]["nextCursor"]}, project_id=prj, run_id=rid)
    check("produced-cap-last-truncated-bound-no-cursor", c2["context"]["traversalCoverage"] == "truncated-bound" and c2["context"].get("nextCursor") is None, c2["context"])
    req_cap = Q.traverse_projected_graph("graph.neighbors", neigh, many, bounds=cap, completeness="required", project_id=prj, run_id=rid)
    check("required-completeness-unmet-at-produced-cap", req_cap["termination"]["class"] == "indeterminate" and req_cap["termination"]["reasonCodes"] == ["QUERY.COMPLETENESS_UNMET"], req_cap["termination"])

    chain = []
    nodes = [ep(u1, "symbol", "symbol:n%d" % i) for i in range(4)]
    for i in range(3):
        chain.append(edge("c%d" % i, nodes[i], nodes[i + 1]))
    reach_start = dict(reach_p, start=nodes[0], includeStart=True)
    exact_r = Q.traverse_projected_graph("graph.reach", reach_start, chain, bounds=dict(Q.PUBLIC_BOUNDS, maxVisitedNodes=4), project_id=prj, run_id=rid)
    check("exact-at-visited-cap-complete", exact_r["context"]["traversalCoverage"] == "complete" and exact_r["context"]["countBasis"] == "exact" and exact_r["context"]["visitedNodes"] == 4, exact_r["context"])
    over_r = Q.traverse_projected_graph("graph.reach", reach_start, chain, bounds=dict(Q.PUBLIC_BOUNDS, maxVisitedNodes=2), completeness="required", project_id=prj, run_id=rid)
    check("over-visited-cap-unmet", over_r["context"]["traversalCoverage"] == "truncated-bound" and over_r["termination"]["class"] == "indeterminate" and over_r["context"]["visitedNodes"] == 2, over_r["context"])
    check("cursor-not-issued-past-visited-cap", over_r["context"].get("nextCursor") is None)
    one = Q.traverse_projected_graph("graph.path", path_ab, [e_direct], bounds=dict(Q.PUBLIC_BOUNDS, maxVisitedNodes=1), completeness="required", project_id=prj, run_id=rid)
    check("path-visited-cap-one-does-not-enter-target", one["context"]["visitedNodes"] == 1 and one["context"]["traversalCoverage"] == "truncated-bound" and one["items"] == [], one["context"])
    # First BFS reach is the canonical shortest/tie witness; extra branches must not truncate it.
    long1, long2 = edge("z9", a, c), edge("z8", c, b)
    short = edge("a0", a, b)
    short["factId"] = "fact2:" + ("0" * 64)
    long1["factId"] = "fact2:" + ("f" * 64)
    proven = Q.traverse_projected_graph("graph.path", path_ab, [long1, long2, short], bounds=dict(Q.PUBLIC_BOUNDS, maxVisitedNodes=2), completeness="required", project_id=prj, run_id=rid)
    check("path-stops-at-first-canonical-bfs-target", len(proven["items"]) == 1 and proven["items"][0]["hopCount"] == 1 and proven["items"][0]["edges"][0]["factId"] == short["factId"] and proven["context"]["traversalCoverage"] == "complete" and proven["context"]["visitedNodes"] == 2, proven["context"])
    fa, fb = edge("aa", a, b), edge("ab", a, b)
    tie = Q.traverse_projected_graph("graph.path", path_ab, [fb, fa], project_id=prj, run_id=rid)
    check("path-tie-least-fact2", tie["items"][0]["edges"][0]["factId"] == min(fa["factId"], fb["factId"]), tie["items"])
    cyc = [edge("ab1", a, b), edge("ba1", b, a)]
    cyc_path = Q.traverse_projected_graph("graph.path", path_ab, cyc, project_id=prj, run_id=rid)
    check("path-cycle-simple-one-hop", cyc_path["items"][0]["hopCount"] == 1, cyc_path["items"])

    refuse("relation-unsupported-types", lambda: Q.traverse_projected_graph("graph.neighbors", {
        "direction": "outgoing", "endpoint": a, "minResolution": "checked", "relation": "types",
    }, [f1], project_id=prj, run_id=rid), "REQUEST.PRECONDITION_FAILED", "QUERY.RELATION_UNSUPPORTED", envelope=False)


def surface_carrier_controls(response, project):
    """Retained-Run owner graph response through the public CommandEnvelope major 3 carrier and every renderer."""
    QS = load("query_surface_projection3_checker", HERE / "query_surface_projection.v3.py")
    inv = json.loads((HERE / "command-inventory.v3.json").read_text())
    command = next(c for c in inv["commands"] if c["name"] == "query")
    term = copy.deepcopy(response.get("termination") or {"class": "success"})
    env = {
        "schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "query", "requestId": host_obs()["requestId"],
        "projectId": project, "termination": term, "exitCode": QS.Wlegacy.EXIT[term["class"]],
        "query": QS.graph_query_result_summary(response), "querySurface": "graph-query-response", "queryResponse": copy.deepcopy(response),
    }
    must_valid("m5-retained-run-graph-response-in-public-envelope", U + "command-envelope:3", env)
    try:
        proj = QS.project_query_surface(response, term, envelope=env, command=command)
        rnd = QS.render_query_formats(proj["parity"], env, command, hints=["hint"])
        bodies = {r["format"]: r["body"] for r in rnd["renderings"]}
        check("m5-retained-run-all-advertised-renderers-hold-parity", rnd["ok"] and rnd["parityHolds"] and sorted(bodies) == ["agent", "human", "json"], rnd.get("ok"))
        check("m5-retained-run-json-rendering-is-the-schema-valid-envelope", bodies["json"] == env and valid(U + "command-envelope:3", bodies["agent"])[0] and "agentHints" not in bodies["json"])
        check("m5-retained-run-query-response-is-the-owner-response", proj["parity"]["query-response"] == response and proj["parity"]["total-items"] == response["context"]["totalItems"])
        pointer = QS.project_command_surface(env, command)
        check("r2-query-command-parity-paths-equal-owner-projection", pointer["parity"] == proj["parity"] and pointer["surface"] == "graph-query-response")
        generic = QS.render_command_formats(env, command, hints=["hint"])
        check("r2-query-command-generic-renderer-recovers-parity", generic["ok"] and generic["parityHolds"])
        partial = {k: v for k, v in proj["parity"].items() if k != "query-response"}
        failed = QS.render_query_formats(partial, env, command)
        dt = failed["deliveryTermination"] or {}
        check(
            "m5-a13-retained-run-missing-query-response-is-precommit-delivery-fault",
            failed["ok"] is False and "runId" not in dt and dt.get("domainDetail", {}).get("code") == "DELIVERY.REQUIRED_PROJECTION_FAILED" and valid(U + "common:3#/$defs/StepTermination", dt)[0],
            dt,
        )
    except Exception as exc:
        check("m5-retained-run-all-advertised-renderers-hold-parity", False, type(exc).__name__ + ": " + str(exc)[:200])
    missing = copy.deepcopy(env)
    del missing["queryResponse"]
    must_invalid("m5-retained-run-graph-envelope-cannot-omit-query-response", U + "command-envelope:3", missing)
    other_project = copy.deepcopy(env)
    other_project["projectId"] = project_id("elsewhere")
    try:
        QS.project_query_surface(response, term, envelope=other_project, command=command)
        check("m5-retained-run-envelope-project-join", False, "admitted")
    except QS.QuerySurfaceProjectionError as exc:
        check("m5-retained-run-envelope-project-join", exc.code == "QUERY_SURFACE_PROJECT_JOIN", exc.code)


def owner_controls():
    foundation = HERE.parent / "foundation"
    S = load("query_semantic_fixture3", foundation / "evaluator_semantic_fixture.v3.py")
    replay = load("query_semantic_replay_check3", foundation / "check-semantic-replay.v3.py")
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding", "endpoint": "target", "filters": []}
    g = S.build_ts_semantic_graph(
        atom=atom, has_declares=False, has_references_fact=True, second_partition=True,
        references_resolved=False, incoming_search=True, incoming_complete=False,
        target_sidecar=True, second_universe=True,
    )
    run, objects, blobs, actual = replay.close_positive(g)
    run_key = actual["runId"]
    project = run["projectId"]
    foo_ep = ep(g["u1"], "symbol", g["foo"])
    bar_ep = ep(g["u1"], "symbol", g["bar"])
    baz_ep = ep(g["u2"], "symbol", g["baz"])
    host = host_obs(latestRunId=run_key)

    def ex(req, h=None, r=None, o=None, b=None):
        used = h if h is not None else host
        if "requestId" not in used:
            used = dict(host_obs(), **used)
        return Q.execute_graph_query(req, run if r is None else r, objects if o is None else o, blobs if b is None else b, host=used)

    out_req = request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    })
    neigh = ex(out_req)
    check("owner-neighbors-foo-bar", len(neigh["items"]) == 1 and neigh["items"][0]["target"]["nativeSubjectId"] == g["bar"], neigh["items"])
    check("matching-selected-views-are-not-native-evidence-unavailable", "native-evidence-unavailable" not in {x.get("kind") for x in neigh["context"]["evidence"]["resolutionLimitations"]}, neigh["context"]["evidence"]["resolutionLimitations"])
    check("owner-resolved-run-only", neigh["context"]["resolvedView"] == {"runId": run_key})
    check("owner-evidence-coverage", len(neigh["context"]["evidence"]["coverageIds"]) >= 1, neigh["context"]["evidence"])
    states = {x.get("resolutionState") for x in neigh["context"]["evidence"]["resolutionLimitations"]}
    kinds = {x.get("kind") for x in neigh["context"]["evidence"]["resolutionLimitations"]}
    check("owner-partial-or-not-attempted-disclosed", bool(states & {"not-attempted", "partial", "incomplete"}) or bool(kinds & {"resolution-not-attempted", "resolution-partial", "resolution-incomplete", "incoming-search-incomplete"}), str(states | kinds))
    check("owner-unresolvedEdgeCount-field", any("unresolvedEdgeCount" in x or x.get("kind") == "incoming-search-incomplete" for x in neigh["context"]["evidence"]["resolutionLimitations"]), neigh["context"]["evidence"]["resolutionLimitations"][:3])

    cites = neigh["context"]["evidence"]["deficiencyCitations"]
    check("owner-deficiency-keeps-inputRefs", bool(cites) and all("inputRefs" in c and c["source"] in Q.DEFICIENCY_SOURCES for c in cites), cites[:2])
    surface_carrier_controls(neigh, project)
    refuse("a8-request-project-differs-from-admitted-run", lambda: ex(request("graph.neighbors", project_id("elsewhere"), {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    check("a8-query-contract-publishes-project-mismatch-route", "| request `projectId` differs from the admitted Run's project | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.PARAMS_MALFORMED` |" in (HERE / "query-projection-contract.v3.md").read_text())

    in_req = request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "incoming", "endpoint": foo_ep,
    })
    incoming = ex(in_req)
    check("owner-incoming-zero-not-absence", incoming["items"] == [] and incoming["context"]["countBasis"] == "exact", incoming["context"])
    in_kinds = {x.get("kind") for x in incoming["context"]["evidence"]["resolutionLimitations"]}
    check("owner-incoming-unknown-disclosed", bool(in_kinds & {"resolution-not-attempted", "resolution-partial", "resolution-incomplete", "coverage-unknown", "incoming-search-incomplete"}), str(in_kinds))

    path_same = ex(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": foo_ep, "maxDepth": 4,
    }))
    check("owner-path-start-eq-target", path_same["items"][0]["hopCount"] == 0, path_same["items"])
    path_fb = ex(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": bar_ep, "maxDepth": 4,
    }))
    check("owner-path-foo-bar", len(path_fb["items"]) == 1 and path_fb["items"][0]["hopCount"] == 1, path_fb["items"])
    path_cap = ex(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": bar_ep, "maxDepth": 1,
    }), {"latestRunId": run_key, "testBounds": {"maxVisitedNodes": 1}})
    check("owner-path-visited-cap-one", path_cap["context"]["visitedNodes"] == 1 and path_cap["context"]["traversalCoverage"] == "truncated-bound" and path_cap["items"] == [], path_cap["context"])

    isolated = ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": bar_ep,
    }))
    check("owner-known-empty-incidence", isolated["items"] == [] and isolated["context"]["traversalCoverage"] == "complete", isolated["context"])

    refuse("unknown-endpoint-zero-hop", lambda: ex(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": {"universe": "e" * 64, "kind": "symbol", "nativeSubjectId": "missing"},
        "target": {"universe": "e" * 64, "kind": "symbol", "nativeSubjectId": "missing"},
        "maxDepth": 1,
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_UNKNOWN")
    refuse("absent-subject-known-universe", lambda: ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "endpoint": ep(g["u1"], "symbol", "symbol:missing"),
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_UNKNOWN")

    refuse("strong-wrapper-with-no-retained-run", lambda: Q.execute_graph_query(out_req, host=host_obs(standing="synthetic-admitted-fact-graph", admittedFactGraph={"edges": [], "projectId": project, "runId": run_key, "viewIds": []})), "IDENTITY.UNKNOWN", "QUERY.VIEW_UNKNOWN")
    refuse("malformed-request-no-retained-run", lambda: Q.execute_graph_query({"schemaMajor": 3, "bad": True}, host=host_obs()), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    refuse("non-object-request", lambda: Q.execute_graph_query("not-an-object", host=host_obs()), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")

    poisoned = {"cache": {("x",): {"edges": []}}, "latestRunId": run_key}
    poisoned_result = ex(out_req, poisoned)
    check("cache-omission-does-not-drop-edge", len(poisoned_result["items"]) == 1 and poisoned_result["context"]["totalItems"] == neigh["context"]["totalItems"], poisoned_result["context"])
    added = copy.deepcopy(poisoned)
    added["cache"][("x",)] = {"edges": [edge("fake", foo_ep, baz_ep)]}
    added_result = ex(out_req, added)
    check("cache-added-edge-ignored", [x["factId"] for x in added_result["items"]] == [x["factId"] for x in neigh["items"]])
    changed = copy.deepcopy(poisoned)
    if neigh["items"]:
        row = copy.deepcopy(neigh["items"][0])
        row["factId"] = hid("fact2", "changed-provenance")
        changed["cache"][("x",)] = {"edges": [row]}
    changed_result = ex(out_req, changed)
    check("cache-changed-provenance-ignored", [x["factId"] for x in changed_result["items"]] == [x["factId"] for x in neigh["items"]])
    deleted = ex(out_req, {"cache": {}, "latestRunId": run_key})
    check("cache-deletion-same-result", [x["factId"] for x in deleted["items"]] == [x["factId"] for x in neigh["items"]])

    fake = "snapshot2:" + ("e" * 64)
    snap_req = request("graph.neighbors", project, {"snapshotId": run["snapshotId"]}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    })
    refuse("wrong-snapshot-index-result", lambda: ex(request("graph.neighbors", project, {"snapshotId": fake}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    }), host_obs(latestRunId=run_key, runsForSnapshot={fake: [run_key]})), "IDENTITY.UNKNOWN", "QUERY.VIEW_UNKNOWN")
    refuse("snapshot-missing-uniqueness-observation", lambda: ex(snap_req, host_obs(latestRunId=run_key)), "IDENTITY.UNKNOWN", "QUERY.VIEW_UNKNOWN")
    refuse("snapshot-empty-uniqueness-observation", lambda: ex(snap_req, host_obs(latestRunId=run_key, runsForSnapshot={run["snapshotId"]: []})), "IDENTITY.UNKNOWN", "QUERY.VIEW_UNKNOWN")
    refuse("snapshot-multi-uniqueness-observation", lambda: ex(snap_req, host_obs(latestRunId=run_key, runsForSnapshot={run["snapshotId"]: [run_key, run_id("other")]})), "REQUEST.PRECONDITION_FAILED", "QUERY.VIEW_AMBIGUOUS")
    refuse("snapshot-unique-names-other-run", lambda: ex(snap_req, host_obs(latestRunId=run_key, runsForSnapshot={run["snapshotId"]: [run_id("other")]})), "IDENTITY.UNKNOWN", "QUERY.VIEW_UNKNOWN")
    snap_ok = ex(snap_req, host_obs(latestRunId=run_key, runsForSnapshot={run["snapshotId"]: [run_key]}))
    check("snapshot-join-admitted-run", snap_ok["context"]["resolvedView"]["runId"] == run_key and len(snap_ok["items"]) == 1)

    refuse("schema-major-2-model", lambda: ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    }, major=2)), "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "QUERY.SCHEMA_MAJOR_UNSUPPORTED")
    refuse("relation-unsupported-syntactic-calls", lambda: ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "calls", "minResolution": "syntactic-callee-name", "direction": "outgoing", "endpoint": foo_ep,
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.RELATION_UNSUPPORTED")

    host_def = {"latestRunId": run_key, "evaluationDeficiencies": [{"source": "execution", "cause": "invented"}], "targetAttributions": {neigh["items"][0]["factId"] if neigh["items"] else "x": {"kind": "package"}}}
    ignored = ex(out_req, host_def)
    check("host-deficiencies-do-not-replace-retained", ignored["context"]["evidence"]["deficiencyCitations"] == neigh["context"]["evidence"]["deficiencyCitations"], ignored["context"]["evidence"]["deficiencyCitations"][:2])

    refuse("owner-mismatched-view", lambda: ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
        "factViewDigests": [hid("view2", "not-on-run")],
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.FACT_VIEW_UNAVAILABLE")

    c_objects, c_blobs = copy.deepcopy(objects), copy.deepcopy(blobs)
    evidence = c_objects[run["evidenceId"]][1]
    victim = None
    for vid in evidence["viewIds"]:
        view = c_objects[vid][1]
        if view.get("facts"):
            victim = view["facts"][0]
            break
    check("owner-has-fact-to-corrupt", victim is not None, "no fact in views")
    if victim is not None:
        digest = c_objects[victim][1]["payloadDigest"]
        c_blobs[digest] = b"not-the-retained-payload"
        refuse("owner-corrupt-payload", lambda: ex(out_req, host, run, c_objects, c_blobs), "HOST.IO_FAILURE", "evidence.corrupt")
        refuse("host-retained-flag-cannot-admit-corrupt-payload", lambda: ex(out_req, host_obs(availability="retained"), run, c_objects, c_blobs), "HOST.IO_FAILURE", "evidence.corrupt")
        del c_blobs[digest]
        refuse("owner-missing-payload", lambda: ex(out_req, host, run, c_objects, c_blobs), "HOST.IO_FAILURE", "evidence.missing")

    path_cross = ex(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": baz_ep, "maxDepth": 8,
    }))
    check("owner-two-universes-same-native-not-union", path_cross["items"] == [] and path_cross["context"]["countBasis"] == "exact", path_cross["context"])
    check("owner-subjects-foo-bar-baz", g["foo"] and g["bar"] and g["baz"])

    refuse("runid-mismatch-view-unknown", lambda: ex(request("graph.neighbors", project, {"runId": run_id("other")}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    })), "IDENTITY.UNKNOWN", "QUERY.VIEW_UNKNOWN")
    refuse("fully-specified-unknown-not-ambiguous", lambda: ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "endpoint": ep("e" * 64, "symbol", g["foo"]),
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_UNKNOWN")

    nonev = ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": foo_ep,
    }))
    nonev_kinds = {x.get("kind") for x in nonev["context"]["evidence"]["resolutionLimitations"]}
    check("native-evidence-unavailable-no-selected-views", nonev["items"] == [] and "native-evidence-unavailable" in nonev_kinds and any(x.get("relation") == "calls" and x.get("minResolution") == "resolved-callee" for x in nonev["context"]["evidence"]["resolutionLimitations"]), nonev["context"]["evidence"]["resolutionLimitations"])
    unrelated = ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": foo_ep,
        "factViewDigests": neigh["context"]["factViewDigests"],
    }))
    unrelated_lim = unrelated["context"]["evidence"]["resolutionLimitations"]
    check(
        "native-evidence-unavailable-explicit-unrelated-views",
        unrelated["items"] == []
        and unrelated["context"]["factViewDigests"] == sorted(neigh["context"]["factViewDigests"])
        and any(
            x.get("kind") == "native-evidence-unavailable"
            and x.get("relation") == "calls"
            and x.get("minResolution") == "resolved-callee"
            for x in unrelated_lim
        ),
        unrelated_lim,
    )

    refuse("host-availability-purged-refuses", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="purged")), "HOST.IO_FAILURE", "evidence.purged")
    refuse("host-availability-expired-refuses", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="expired")), "HOST.IO_FAILURE", "evidence.expired")
    retained_anyway = ex(out_req, host_obs(latestRunId=run_key, availability="retained"))
    check("host-availability-retained-does-not-skip-close-run", len(retained_anyway["items"]) == 1)

    # Contract section 7: every identity availability refusal state has one registered detail, and each is
    # operational-failed / HOST.IO_FAILURE / exit 4 at the public wrapper. `unavailable` reuses evidence.missing.
    refuse("host-availability-corrupt-refuses", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="corrupt")), "HOST.IO_FAILURE", "evidence.corrupt")
    refuse("host-availability-unavailable-refuses-evidence-missing", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="unavailable")), "HOST.IO_FAILURE", "evidence.missing")
    for state, detail in (("purged", "evidence.purged"), ("expired", "evidence.expired"),
                          ("corrupt", "evidence.corrupt"), ("unavailable", "evidence.missing")):
        cid = "host-availability-%s-envelope-operational-failed-exit-4" % state
        try:
            ex(out_req, host_obs(latestRunId=run_key, availability=state))
            check(cid, False, "expected QueryRefusal")
        except Q.QueryRefusal as exc:
            env = exc.envelope()
            check(cid, env["exitCode"] == 4 and env["termination"]["class"] == "operational-failed"
                  and [e["code"] for e in env["errors"]] == [detail], env)
    refuse("host-availability-direct-missing", lambda: ex(out_req, host_obs(availability="missing")), "HOST.IO_FAILURE", "evidence.missing")
    for label, observation in (("unknown", "not-a-state"), ("null", None), ("boolean", False),
                               ("number", 1), ("list", []), ("object", {})):
        try:
            ex(out_req, host_obs(availability=observation))
        except Q.ReferenceCallPrecondition as exc:
            check("host-availability-precondition-" + label, exc.missing == "host.availability")
        else:
            check("host-availability-precondition-" + label, False, "invalid trusted observation was ignored")
    # Contract section 7: the precondition is reference-harness law. A product host adapter's own out-of-vocabulary
    # observation is the existing host-internal invariant route when a valid RequestId exists; without one it stays
    # a precondition. A retained availability record failing identity admission is corrupt evidence instead.
    try:
        ex(out_req, host_obs(availability="not-a-state"))
        precondition = None
    except Q.ReferenceCallPrecondition as exc:
        precondition = exc
    check("host-adapter-invalid-observation-is-typed-precondition", precondition is not None and precondition.missing == "host.availability")
    if precondition is not None:
        refuse("host-adapter-invalid-availability-host-invariant",
               lambda: raise_(Q.host_adapter_refusal(precondition, out_req, host_obs())),
               "SYSTEM.OUTCOME.ILLEGAL_STATE", "HOST.INVARIANT_VIOLATED")
        adapter_env = Q.host_adapter_refusal(precondition, out_req, host_obs()).envelope()
        check("host-adapter-invalid-availability-envelope-exit-4",
              adapter_env["exitCode"] == 4 and adapter_env["termination"]["faultCause"] == "host-invariant"
              and adapter_env["termination"]["domainDetail"]["subject"] == "host.availability" and "run" not in adapter_env, adapter_env)
        try:
            Q.host_adapter_refusal(precondition, out_req, {})
            check("host-adapter-without-request-id-stays-precondition", False, "adapter fault projected without a RequestId")
        except Q.ReferenceCallPrecondition as exc:
            check("host-adapter-without-request-id-stays-precondition", exc.missing == "host.requestId", exc.missing)
    try:
        Q.host_adapter_refusal(Q.ReferenceCallPrecondition("host.requestId"), out_req, host_obs())
        check("host-adapter-request-id-precondition-not-projected", False, "RequestId precondition was projected")
    except Q.ReferenceCallPrecondition as exc:
        check("host-adapter-request-id-precondition-not-projected", exc.missing == "host.requestId", exc.missing)
    record = {"schemaVersion": 2, "runId": run_key, "generation": 0, "state": "purged", "missingRefs": [], "reason": "operator purge"}
    observed = Q.observe_retained_availability(canonical.canonical(record), run_key)
    check("retained-availability-record-admitted-supplies-state", observed == "purged", observed)
    refuse("retained-availability-record-state-routes-as-observation", lambda: ex(out_req, host_obs(latestRunId=run_key, availability=observed)), "HOST.IO_FAILURE", "evidence.purged")
    for label, raw in (("unparseable-bytes", b"{not-json"),
                       ("unknown-state", canonical.canonical(dict(record, state="not-a-state"))),
                       ("other-run", canonical.canonical(dict(record, runId=run_id("other"))))):
        refuse("retained-availability-record-%s-is-corrupt" % label,
               lambda raw=raw: Q.observe_retained_availability(raw, run_key), "HOST.IO_FAILURE", "evidence.corrupt", envelope=False)
    partial_ok = ex(out_req, host_obs(latestRunId=run_key, availability="partial"))
    check("host-availability-partial-neither-refuses-nor-grants", len(partial_ok["items"]) == 1, partial_ok["items"])
    if victim is not None:
        refuse("host-availability-partial-cannot-admit-missing-bytes", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="partial"), run, c_objects, c_blobs), "HOST.IO_FAILURE", "evidence.missing")

    # Contract section 2, schema-first: a package endpoint without its coordinate is malformed at the public
    # wrapper and at the endpoint helper alike, and still precedes Run/view joins; ENDPOINT_AMBIGUOUS is reserved
    # for a complete tuple resolving to several admitted vertices.
    pkg_no_path = ep(g["u1"], "package", "demo-package")
    for label, endpoint in (("missing", pkg_no_path), ("empty", dict(pkg_no_path, packageManifestPath=""))):
        refuse("package-endpoint-%s-manifest-path-is-malformed" % label, lambda e=endpoint: ex(request("graph.neighbors", project, {"runId": run_key}, {
            "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": e,
        })), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    refuse("package-path-target-without-manifest-path-is-malformed", lambda: ex(request("graph.path", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "start": foo_ep, "target": pkg_no_path, "maxDepth": 2,
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    refuse("package-without-manifest-path-malformed-before-run-and-view", lambda: Q.execute_graph_query(request("graph.neighbors", project, {"runId": run_id("other")}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": pkg_no_path,
    }), host=host_obs(availability="purged")), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    refuse("endpoint-helper-agrees-package-without-manifest-path-is-malformed", lambda: Q.parse_endpoint_syntax(pkg_no_path, "endpoint"), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED", envelope=False)
    refuse("well-formed-package-tuple-outside-domain-is-unknown", lambda: ex(request("graph.neighbors", project, {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
        "endpoint": ep(g["u1"], "package", "demo-package", "package.json"),
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_UNKNOWN")
    refuse("endpoint-ambiguous-only-for-a-complete-tuple-marked-ambiguous-helper-unit", lambda: Q.admit_vertices(
        [("endpoint", foo_ep)], {Q.endpoint_tuple(foo_ep): foo_ep}, {Q.endpoint_tuple(foo_ep)}),
        "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_AMBIGUOUS", envelope=False)

    try:
        Q.execute_graph_query(dict(out_req, page={"size": 1.25}), run, objects, blobs, host=host_obs())
        check("malformed-float-failure-carrier", False, "expected QueryRefusal")
    except Q.QueryRefusal as exc:
        env = exc.envelope()
        check("malformed-float-failure-carrier", env["kind"] == "failure" and env["requestId"] == host_obs()["requestId"] and "run" not in env, env)
    try:
        Q.execute_graph_query(dict(out_req, projectId="not-a-project"), run, objects, blobs, host=host_obs())
        check("malformed-project-omitted-from-envelope", False, "expected QueryRefusal")
    except Q.QueryRefusal as exc:
        env = exc.envelope()
        check("malformed-project-omitted-from-envelope", "projectId" not in env and env["requestId"] == host_obs()["requestId"], env)
    same_bad = {"schemaMajor": 3, "bad": True}
    h1, h2 = host_obs(), host_obs()
    h1["requestId"], h2["requestId"] = "req1_" + "b" * 32, "req1_" + "c" * 32
    try:
        Q.execute_graph_query(same_bad, host=h1)
        e1 = None
    except Q.QueryRefusal as exc:
        e1 = exc.envelope()
    try:
        Q.execute_graph_query(same_bad, host=h2)
        e2 = None
    except Q.QueryRefusal as exc:
        e2 = exc.envelope()
    check("duplicate-request-distinct-host-request-ids", e1 and e2 and e1["requestId"] == h1["requestId"] and e2["requestId"] == h2["requestId"] and e1["requestId"] != e2["requestId"], (e1 or {}, e2 or {}))
    try:
        Q.execute_graph_query(same_bad, host={})
        check("missing-host-request-id-is-reference-precondition", False, "expected ReferenceCallPrecondition or QueryRefusal without envelope")
    except Q.QueryRefusal as exc:
        try:
            exc.envelope()
            check("missing-host-request-id-is-reference-precondition", False, "envelope succeeded without requestId")
        except Q.ReferenceCallPrecondition:
            check("missing-host-request-id-is-reference-precondition", True)
    except Q.ReferenceCallPrecondition:
        check("missing-host-request-id-is-reference-precondition", True)

    ig = S.build_ts_semantic_graph(
        atom={"op": "exists", "relation": "imports", "minResolution": "resolved-target",
              "endpoint": "target", "filters": []},
        subject_kind="file", has_declares=False, has_references_fact=False, second_partition=False,
    )
    irun, iobjects, iblobs, iactual = replay.close_positive(ig)
    irun_key = iactual["runId"]
    iproject = irun["projectId"]
    ihost = host_obs(latestRunId=irun_key)
    file_ep = ep(ig["u1"], "file", "a.ts")
    namespaced_ep = ep(ig["u1"], "file", "file:a.ts")

    def iex(req, h=None):
        used = h if h is not None else ihost
        if "requestId" not in used:
            used = dict(host_obs(), **used)
        return Q.execute_graph_query(req, irun, iobjects, iblobs, host=used)

    in_imp = iex(request("graph.neighbors", iproject, {"runId": irun_key}, {
        "relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": file_ep,
    }))
    check("owner-imports-file-occupies-inventory-vertex",
          len(in_imp["items"]) == 1 and in_imp["items"][0]["target"]["nativeSubjectId"] == "a.ts",
          in_imp["items"])
    refuse("owner-imports-namespaced-id-not-inventory-vertex", lambda: iex(request("graph.neighbors", iproject, {"runId": irun_key}, {
        "relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": namespaced_ep,
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_UNKNOWN")
    isolated_pkg = None
    for item in ig["inputs"]["population"].values():
        if item["kind"] == "package":
            isolated_pkg = ep(item["universe"], "package", item["row"]["nativeSubjectId"], item["row"]["path"])
            break
    if isolated_pkg:
        pkg_n = iex(request("graph.neighbors", iproject, {"runId": irun_key}, {
            "relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": isolated_pkg,
        }))
        check("owner-imports-isolated-package-inventory-empty-not-absence",
              pkg_n["items"] == [] and pkg_n["termination"]["class"] == "success", pkg_n)
    path_imp = iex(request("graph.path", iproject, {"runId": irun_key}, {
        "relation": "imports", "minResolution": "resolved-target", "direction": "outgoing",
        "start": ep(ig["u1"], "symbol", ig["foo"]), "target": file_ep, "maxDepth": 8,
    }))
    check("owner-imports-path-source-to-file-occupancy",
          len(path_imp["items"]) == 1 and path_imp["items"][0]["hopCount"] == 1, path_imp["items"])
    reach_imp = iex(request("graph.reach", iproject, {"runId": irun_key}, {
        "relation": "imports", "minResolution": "resolved-target", "direction": "outgoing",
        "start": ep(ig["u1"], "symbol", ig["foo"]), "maxDepth": 8,
    }))
    reach_ids = [row["endpoint"]["nativeSubjectId"] for row in reach_imp["items"]]
    check("owner-imports-reach-includes-file-occupancy", "a.ts" in reach_ids and "file:a.ts" not in reach_ids, reach_ids)

    IMPORTS_EXISTS = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                      "endpoint": "target", "filters": []}

    sg = S.build_ts_semantic_graph(
        atom=IMPORTS_EXISTS, subject_kind="symbol", has_declares=False, has_references_fact=False,
        second_partition=False, imports_occupancy="exact-id-symbol",
    )
    srun, sobjects, sblobs, sactual = replay.close_positive(sg)
    shost = host_obs(latestRunId=sactual["runId"])

    def sex(req, run_=None, objects_=None, blobs_=None, h=None):
        used = h if h is not None else shost
        if "requestId" not in used:
            used = dict(host_obs(), **used)
        return Q.execute_graph_query(
            req,
            srun if run_ is None else run_,
            sobjects if objects_ is None else objects_,
            sblobs if blobs_ is None else blobs_,
            host=used,
        )

    foo_ep = ep(sg["u1"], "symbol", sg["foo"])
    bar_ep = ep(sg["u1"], "symbol", sg["bar"])
    sym_in = sex(request("graph.neighbors", srun["projectId"], {"runId": sactual["runId"]}, {
        "relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": foo_ep,
    }))
    check("owner-imports-symbol-exact-id-no-sidecar-query",
          len(sym_in["items"]) == 1 and sym_in["items"][0]["source"]["nativeSubjectId"] == sg["bar"]
          and sym_in["items"][0]["target"]["nativeSubjectId"] == sg["foo"],
          sym_in["items"])
    check("owner-imports-symbol-exact-id-atom-run-agrees",
          sactual["verdict"] == "fail" and sactual["findingCount"] >= 1,
          sactual)

    ug = S.build_ts_semantic_graph(
        atom=IMPORTS_EXISTS, subject_kind="symbol", has_declares=False, has_references_fact=False,
        second_partition=False, imports_occupancy="unknown-sidecar-symbol",
    )
    urun, uobjects, ublobs, uactual = replay.close_positive(ug)
    uhost = host_obs(latestRunId=uactual["runId"])
    ufoo = ep(ug["u1"], "symbol", ug["foo"])
    uin = Q.execute_graph_query(
        request("graph.neighbors", urun["projectId"], {"runId": uactual["runId"]}, {
            "relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": ufoo,
        }),
        urun, uobjects, ublobs, host=dict(uhost, targetAttributions={"forged": True}),
    )
    check("owner-imports-unknown-sidecar-unique-inventory-query",
          len(uin["items"]) == 1 and uin["items"][0]["target"]["nativeSubjectId"] == ug["foo"],
          uin["items"])
    check("owner-imports-unknown-sidecar-atom-run-agrees",
          uactual["verdict"] == "fail" and uactual["findingCount"] >= 1,
          uactual)
    check("owner-imports-host-targetAttributions-do-not-grant-occupancy",
          len(uin["items"]) == 1, uin["items"])

    mg = S.build_ts_semantic_graph(
        atom=IMPORTS_EXISTS, subject_kind="file", has_declares=False, has_references_fact=False,
        second_partition=False, imports_occupancy="unmapped-file",
    )
    mrun, mobjects, mblobs, mactual = replay.close_positive(mg)
    mhost = host_obs(latestRunId=mactual["runId"])
    mout = Q.execute_graph_query(
        request("graph.neighbors", mrun["projectId"], {"runId": mactual["runId"]}, {
            "relation": "imports", "minResolution": "resolved-target", "direction": "outgoing",
            "endpoint": ep(mg["u1"], "symbol", mg["foo"]),
        }),
        mrun, mobjects, mblobs, host=mhost,
    )
    lims = mout["context"]["evidence"]["resolutionLimitations"]
    check("owner-imports-unmapped-no-exact-id-unprojectable",
          mout["items"] == [] and any(x.get("kind") == "unprojectable-fact" for x in lims),
          {"items": mout["items"], "limitations": lims})
    minc = Q.execute_graph_query(
        request("graph.neighbors", mrun["projectId"], {"runId": mactual["runId"]}, {
            "relation": "imports", "minResolution": "resolved-target", "direction": "incoming",
            "endpoint": ep(mg["u1"], "file", "a.ts"),
        }),
        mrun, mobjects, mblobs, host=mhost,
    )
    check("owner-imports-unmapped-file-inventory-vertex-empty-not-hit",
          minc["items"] == [] and minc["termination"]["class"] == "success", minc)
    check("owner-imports-unmapped-atom-run-not-known-hit",
          mactual.get("findingCount", 0) == 0,
          mactual)

    check("owner-imports-mapped-file-atom-run-agrees",
          iactual["verdict"] == "fail" and iactual["findingCount"] >= 1,
          iactual)

    plan_digest = hashlib.sha256((foundation / "enumeration-plan.schema.v1.json").read_bytes()).hexdigest()
    check("enumeration-plan-row-is-registered-digest", Q.identity3().parameter_row_of(plan_digest) == Q.ENUM_PLAN_ROW, Q.identity3().parameter_row_of(plan_digest))
    duck_payload = {"cells": [{"programBindings": [{"ordinal": 0, "universe": "a" * 64}]}]}
    duck_raw = canonical.canonical(duck_payload)
    duck_digest = hashlib.sha256(duck_raw).hexdigest()
    real_payload = {"cells": [{"programBindings": [{"ordinal": 1, "universe": "b" * 64}]}]}
    real_raw = canonical.canonical(real_payload)
    real_digest = hashlib.sha256(real_raw).hexdigest()
    spec = {
        "parameters": [
            {"schemaDigest": "0" * 64, "payloadDigest": duck_digest},
            {"schemaDigest": plan_digest, "payloadDigest": real_digest},
        ]
    }
    spec_raw = canonical.canonical(spec)
    spec_digest = hashlib.sha256(spec_raw).hexdigest()
    blobs_sel = {spec_digest: spec_raw, duck_digest: duck_raw, real_digest: real_raw}
    selected_plan = Q.load_enumeration_plan({"analysisSpecDigest": spec_digest}, blobs_sel)
    check("enumeration-plan-skips-duck-typed-cells", selected_plan == real_payload, selected_plan)
    spec_duck = {"parameters": [{"schemaDigest": "0" * 64, "payloadDigest": duck_digest}]}
    spec_duck_raw = canonical.canonical(spec_duck)
    spec_duck_digest = hashlib.sha256(spec_duck_raw).hexdigest()
    skipped = Q.load_enumeration_plan({"analysisSpecDigest": spec_duck_digest}, {spec_duck_digest: spec_duck_raw, duck_digest: duck_raw})
    check("enumeration-plan-absent-registered-digest-is-none", skipped is None, skipped)
    owner_plan = Q.load_enumeration_plan(objects[run["planId"]][1], blobs)
    check("owner-enumeration-plan-selected-by-schemaDigest", type(owner_plan) is dict and type(owner_plan.get("cells")) is list and len(owner_plan["cells"]) >= 1, owner_plan and list(owner_plan)[:6])

    Nmod = load("query_native_evidence", HERE.parent / "native" / "native_evidence_model.v2.py")
    rc = Nmod.completeness_from_stage("references", "resolved-binding", [g["foo"]], [{"relation": "references", "referrer": g["foo"], "edgeKind": "dynamic"}], "complete", True, True)
    check("native-incomplete-state-token", rc.get("state") == "incomplete", rc)
    fake_cov = "coverage2:" + token("incomplete-cov")
    entry = {"coverage": "unknown", "deficiency": "resolution-incomplete", "relation": "references", "resolution": "resolved-binding", "resolutionCompleteness": rc}
    payload = {"entry": entry, "key": {"relation": "references", "resolution": "resolved-binding"}}
    raw = canonical.canonical(payload)
    digest = hashlib.sha256(raw).hexdigest()
    mapped, _, _ = Q.relevant_resolution_limitations(
        {"coverageIds": [fake_cov], "viewIds": []},
        {fake_cov: ("coverage", {"payloadDigest": digest})},
        {digest: raw},
        "references",
        [],
        [],
    )
    check("incomplete-state-projected-as-kind-resolution-incomplete", any(x.get("resolutionState") == "incomplete" and x.get("kind") == "resolution-incomplete" for x in mapped), mapped)


def hook_control():
    P = load("workflow_projection_hook3", HERE / "workflow_projection_model.v3.py")
    owner = P.query_projection_owner()
    check("w-hook-loads-query-owner", owner.SCHEMA_ID == GQ, getattr(owner, "SCHEMA_ID", None))
    check("w-query-finding-unchanged", callable(P.query_finding))
    check("strong-entry-has-no-standing-bypass", not hasattr(owner, "SYNTHETIC_STANDING") or "standing" not in (owner.execute_graph_query.__doc__ or ""))


def raise_(exc):
    raise exc


def remint_false_result(M, packed, flip):
    """Fully remint a structurally valid but semantically false result: flipped predicate values with emptied
    witnesses, no findings or execution deficiencies, verdict pass; proof, evidence, seal and Run re-identified."""
    run, objects, blobs = copy.deepcopy(packed)
    seal = copy.deepcopy(objects[run["evaluationSealId"]][1])
    proof = copy.deepcopy(objects[seal["proofBundleId"]][1])
    evidence = copy.deepcopy(objects[run["evidenceId"]][1])
    for predicate in proof["predicateProofs"]:
        value = flip(predicate)
        if value is None or value == predicate["value"]:
            continue
        witness = canonical.parse(blobs[predicate["witnessDigest"]])
        witness.update(matchingFactIds=[], uncertainFactIds=[], deficiencies=[])
        raw = canonical.canonical(witness)
        digest = hashlib.sha256(raw).hexdigest()
        blobs[digest] = raw
        predicate.update(witnessDigest=digest, value=value)
    proof.update(findingIds=[], waivedFindingIds=[], executionDeficiencies=[], verdict="pass")
    for rule in proof["ruleResults"]:
        rule.update(findingIds=[], deficiencies=[])
        if rule["outcome"] in ("fail", "indeterminate"):
            rule["outcome"] = "pass"
    proof_id = M.identifier("proof-bundle", proof)
    objects[proof_id] = ("proof-bundle", proof)
    evidence.update(findingIds=[], proofBundleId=proof_id)
    evidence_id = M.identifier("semantic-evidence", evidence)
    objects[evidence_id] = ("semantic-evidence", evidence)
    seal.update(proofBundleId=proof_id, evidenceId=evidence_id, verdict="pass")
    seal_id = M.identifier("evaluation-seal", seal)
    objects[seal_id] = ("evaluation-seal", seal)
    run.update(evidenceId=evidence_id, evaluationSealId=seal_id)
    return run, objects, blobs


def semantic_refusal_controls():
    # Contract section 7: close_run outcomes route by the exact typed classes of the query's identity copy, never by
    # message text. Fully reminted false results are structurally admitted, then refused by complete replay through
    # the evaluator fault registry's retained-regeneration route; structural corruption, missing bytes and host
    # defects keep their own routes. Reuses the maintained semantic fixtures and finding mutation constructor.
    foundation = HERE.parent / "foundation"
    semantic = load("query_refusal_semantic3", foundation / "check-semantic-replay.v3.py")
    mutants = load("query_refusal_mutants3", foundation / "check-replay.v3.py")
    faults = load("query_refusal_faults3", foundation / "evaluator_fault_model.v3.py")
    M3 = Q.identity3()
    declares_graph, declares, declares_actual = semantic.case_declares_exists()
    incoming_graph, incoming, incoming_actual = semantic.case_incoming_incomplete_unknown()
    inventory_graph, inventory, inventory_actual = semantic.case_missing_inventory_execution()
    lawful = {declares_actual["runId"], incoming_actual["runId"], inventory_actual["runId"]}
    regeneration = faults.ROUTES["complete-replay-mismatch:retained-regeneration"]
    host_internal = faults.ROUTES["input-schema-invalid:host-internal"]
    routes = {}

    def query(graph, packed, run_key=None):
        run, objects, blobs = packed
        symbol = next(row for row in graph["inputs"]["population"].values() if row["kind"] == "symbol")
        req = request("graph.neighbors", run["projectId"], {"runId": run_key or M3.identifier("run", run)}, {
            "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing",
            "endpoint": ep(symbol["universe"], "symbol", symbol["row"]["nativeSubjectId"]),
        })
        return Q.execute_graph_query(req, run, objects, blobs, host=host_obs())

    def refusal(fn):
        try:
            fn()
        except Q.QueryRefusal as exc:
            return exc
        except Exception:
            return None
        return None

    def summary(exc):
        return None if exc is None else (exc.termination(), type(exc.__cause__).__name__)

    for name, graph, packed in (
        ("finding-severity", declares_graph, mutants.remint_finding(*declares, lambda finding, _blobs: finding.update(severity="warning"))),
        ("fail-to-pass", declares_graph, remint_false_result(semantic.M, declares, lambda p: "false" if p["value"] == "true" else None)),
        ("indeterminate-laundered", incoming_graph, remint_false_result(semantic.M, incoming, lambda p: "false" if p["value"] == "indeterminate" else None)),
        ("execution-deficiency-erased", inventory_graph, remint_false_result(semantic.M, inventory, lambda p: None)),
    ):
        cid = "semantic-mutant-" + name
        run_key, _ = M3.open_run_closure(*packed)
        check(cid + "-structurally-admitted-new-run", run_key not in lawful, run_key)
        exc = refusal(lambda: query(graph, packed, run_key))
        if exc is None or exc.diagnostic is None:
            check(cid + "-retained-regeneration-route", False, summary(exc))
            continue
        term = exc.termination()
        env = exc.envelope()
        carrier = M3.RegenerationMismatch(run_key)
        diagnostic = exc.diagnostic.encode()
        observation = faults.owner_observation(carrier, diagnostic)
        routed = faults.route(observation, diagnostic)["termination"]
        check(cid + "-retained-regeneration-route",
              term == carrier.termination == routed
              and (observation["condition"], observation["origin"]) == ("complete-replay-mismatch", "retained-regeneration")
              and term["errorCode"] == regeneration["termination"]["errorCode"] and term["domainDetail"]["code"] == regeneration["detail"]
              and env["exitCode"] == 4 and env["errors"] == [term["domainDetail"]] and "run" not in env, term)
        check(cid + "-typed-cause-retains-exact-diagnostic",
              type(exc.__cause__) is M3.CompleteReplayMismatch and exc.diagnostic == exc.__cause__.diagnostic == str(exc.__cause__)
              and exc.diagnostic.startswith("EVALUATOR_"), (type(exc.__cause__).__name__, exc.diagnostic))
        routes["semantic-replay"] = (term["errorCode"], term["faultCause"], term["domainDetail"]["code"])

    stack = M3.complete_replay()
    check("replay-stack-is-a-separate-identity-load",
          stack.M is not M3 and stack.M.CompleteReplayMismatch is not M3.CompleteReplayMismatch
          and stack.M.C.AdmissionError is not M3.C.AdmissionError and canonical.AdmissionError is not M3.C.AdmissionError)

    run, objects, blobs = copy.deepcopy(declares)
    domain, value = objects[run["evidenceId"]]
    objects[run["evidenceId"]] = (domain, dict(value, findingIds=list(value["findingIds"])[:-1]))
    try:
        M3.open_run_closure(run, objects, blobs)
        structural = "ADMIT"
    except M3.EvidenceUnavailable:
        structural = "MISSING"
    except M3.C.AdmissionError:
        structural = "REFUSE"
    check("structural-retained-graph-refused-by-owner-closure", structural == "REFUSE", structural)
    exc = refusal(lambda: query(declares_graph, (run, objects, blobs)))
    check("structural-retained-graph-evidence-corrupt",
          exc is not None and (exc.error_code, exc.fault_cause, exc.detail) == ("HOST.IO_FAILURE", "host-io", "evidence.corrupt")
          and type(exc.__cause__) is M3.C.AdmissionError and exc.envelope()["exitCode"] == 4, summary(exc))
    if exc is not None:
        routes["structural"] = (exc.error_code, exc.fault_cause, exc.detail)

    run, objects, blobs = copy.deepcopy(declares)
    proof_id = objects[run["evaluationSealId"]][1]["proofBundleId"]
    del objects[proof_id]
    exc = refusal(lambda: query(declares_graph, (run, objects, blobs)))
    check("missing-promised-bytes-evidence-missing",
          exc is not None and (exc.error_code, exc.fault_cause, exc.detail, exc.subject) == ("HOST.IO_FAILURE", "host-io", "evidence.missing", proof_id)
          and type(exc.__cause__) is M3.EvidenceUnavailable and exc.envelope()["exitCode"] == 4, summary(exc))
    if exc is not None:
        routes["missing"] = (exc.error_code, exc.fault_cause, exc.detail)

    def host_defect(cid, raised):
        original = M3.close_run
        M3.close_run = lambda *args, **kwargs: raise_(raised)
        try:
            exc = refusal(lambda: query(declares_graph, declares, declares_actual["runId"]))
        finally:
            M3.close_run = original
        term = exc.termination() if exc is not None else {}
        detail = term.get("domainDetail") or {}
        check(cid,
              term.get("class") == "operational-failed"
              and (term.get("errorCode"), term.get("faultCause")) == (host_internal["termination"]["errorCode"], host_internal["termination"]["faultCause"])
              and (detail.get("code"), detail.get("remedy")) == (host_internal["detail"], host_internal["remedy"])
              and exc.__cause__ is raised and exc.envelope()["exitCode"] == 4, summary(exc))
        if exc is not None:
            routes["host-defect"] = (exc.error_code, exc.fault_cause, exc.detail)

    host_defect("host-defect-with-replay-key-text-is-host-invariant", RuntimeError("EVALUATOR_COMPLETE_PROOF_REPLAY"))
    host_defect("host-defect-with-missing-key-text-is-host-invariant", RuntimeError("EVIDENCE_UNAVAILABLE:" + proof_id))
    host_defect("foreign-identity-copy-mismatch-is-host-invariant", semantic.M.CompleteReplayMismatch("EVALUATOR_COMPLETE_PROOF_REPLAY"))
    original_compare = stack.E.compare_complete_replay
    stack.E.compare_complete_replay = lambda *args, **kwargs: raise_(TypeError("simulated evaluator comparison defect"))
    try:
        exc = refusal(lambda: query(declares_graph, declares, declares_actual["runId"]))
    finally:
        stack.E.compare_complete_replay = original_compare
    check("host-defect-inside-replay-stack-is-host-invariant",
          exc is not None and (exc.error_code, exc.fault_cause, exc.detail) == ("SYSTEM.OUTCOME.ILLEGAL_STATE", "host-invariant", "HOST.INVARIANT_VIOLATED")
          and type(exc.__cause__) is TypeError, summary(exc))

    try:
        lawful_result = query(declares_graph, declares, declares_actual["runId"])
        lawful_ok = M3.close_run(*declares) == declares_actual["runId"] and lawful_result["termination"]["class"] == "success"
        lawful_why = lawful_result["termination"]
    except Exception as exc:
        lawful_ok, lawful_why = False, type(exc).__name__ + ": " + str(exc)[:200]
    check("lawful-replay-and-query-unchanged-after-restore", lawful_ok, lawful_why)
    check("structural-missing-semantic-host-defect-routes-distinct",
          len(routes) == 4 and len(set(routes.values())) == 4
          and not {r[0] for r in routes.values()} & {"PROVIDER.PROTOCOL_VIOLATION", "CONFIG.INVALID"}, routes)
    check("evaluator-fault-origin-law-unchanged",
          faults.ROUTES["complete-replay-mismatch:host-internal"]["termination"] == {"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE", "faultCause": "host-invariant"}
          and faults.ROUTES["complete-replay-mismatch:host-internal"]["detail"] == "HOST.INVARIANT_VIOLATED"
          and faults.ROUTES["input-schema-invalid:provider-return"]["termination"]["errorCode"] == "PROVIDER.PROTOCOL_VIOLATION"
          and faults.ROUTES["input-schema-invalid:external-configuration"]["termination"]["errorCode"] == "CONFIG.INVALID"
          and regeneration["termination"]["faultCause"] == "host-io")
    source = inspect.getsource(Q.close_retained_run)
    check("close-retained-run-routes-without-message-parsing", "startswith" not in source and ".split(" not in source)


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
    semantic_refusal_controls()
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
            "QUERY.CURSOR_MISMATCH", "QUERY.ENDPOINT_AMBIGUOUS", "QUERY.ENDPOINT_UNKNOWN",
            "QUERY.FACT_VIEW_UNAVAILABLE", "QUERY.PARAMS_MALFORMED", "QUERY.RELATION_UNSUPPORTED",
            "QUERY.SCHEMA_MAJOR_UNSUPPORTED", "QUERY.VIEW_AMBIGUOUS", "QUERY.VIEW_UNKNOWN",
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
