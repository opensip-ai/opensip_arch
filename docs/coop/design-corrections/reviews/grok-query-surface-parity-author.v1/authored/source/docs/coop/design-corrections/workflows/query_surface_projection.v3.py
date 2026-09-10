"""Query renderer-parity projection. Design/reference only.

Pure helper: no semantic authority, no Run admission, no graph walk, no envelope
schema change. Callers must supply an already owner-admitted GraphQueryResponseV1
and the enclosing actual StepTermination / CommandEnvelope.

query-response is the complete owned response. Leftover scalars are projections
of that record. Graph QueryResult summary is derived for graph.* only; other 17
keep their owned summary. Does not invent a graph coverage scalar.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

canonical = _load("query_surface_canonical", HERE.parent / "foundation" / "canonical.py")
Wprof = _load("query_surface_profile", HERE / "workflow_projection_model.v3.py")
Wlegacy = _load("query_surface_legacy", HERE / "workflows_model.v1.py")

GRAPH_OPERATIONS = frozenset({"graph.neighbors", "graph.path", "graph.reach"})
ADVERTISED_QUERY_FORMATS = ("human", "json", "agent")
PROSPECTIVE_QUERY_PARITY_FIELDS = (
    "resolved-view",
    "availability",
    "truncated",
    "total-items",
    "termination-class",
    "query-response",
)
QUERY_RESPONSE_REF = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/GraphQueryResponseV1"
TERMINATION_REF = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/StepTermination"
ENVELOPE_REF = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:3"
QUERY_RESULT_REF = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/QueryResult"
CONTEXT_SCALARS = ("resolvedView", "availability", "truncated", "totalItems")
LEFTOVER_FROM_CONTEXT = {
    "resolved-view": "resolvedView",
    "availability": "availability",
    "truncated": "truncated",
    "total-items": "totalItems",
}


class QuerySurfaceProjectionError(Exception):
    def __init__(self, code, detail=None):
        super().__init__(code if detail is None else code + ":" + detail)
        self.code = code
        self.detail = detail


def prospective_query_command(live_command):
    """Local command row with the post-handoff six parity keys. Does not mutate inventory."""
    cmd = copy.deepcopy(live_command)
    cmd["parityFields"] = list(PROSPECTIVE_QUERY_PARITY_FIELDS)
    return cmd


def _admit(ref, value, code):
    try:
        Wprof.validate_profile(ref, value)
    except Exception as exc:
        raise QuerySurfaceProjectionError(code, str(exc)) from exc


def _equal(a, b):
    return canonical.equal_typed(a, b)


def delivery_required_termination(enclosing=None):
    """Existing required-delivery law. Copy runId only when the enclosing termination already has one.
    A historical query read does not mint a committed Run.
    """
    t = {
        "class": "operational-failed",
        "errorCode": "DELIVERY.REQUIRED_FAILED",
        "faultCause": "delivery-required",
    }
    if isinstance(enclosing, dict) and "runId" in enclosing:
        t["runId"] = enclosing["runId"]
    return t


def graph_query_result_summary(response):
    """Graph.* only. QueryResult.items is the page row count, never the items array
    and never context.totalItems. completenessMet is countBasis==exact: completion of
    the declared bounded stored-edge operation, not native closed-world and not
    'every page delivered'. maxDepth is scope, not incompleteness.
    """
    if response.get("operation") not in GRAPH_OPERATIONS:
        raise QuerySurfaceProjectionError("QUERY_SURFACE_NOT_GRAPH", response.get("operation"))
    ctx = response["context"]
    items = response.get("items")
    if type(items) is not list:
        raise QuerySurfaceProjectionError("QUERY_SURFACE_GRAPH_ITEMS_NOT_ARRAY", type(items).__name__)
    summary = {
        "kind": "query",
        "items": len(items),
        "truncated": ctx["truncated"],
        "completenessMet": ctx["countBasis"] == "exact",
        "advisory": False,
    }
    if "nextCursor" in ctx:
        summary["nextCursor"] = ctx["nextCursor"]
    elif "nextCursor" in summary:
        raise QuerySurfaceProjectionError("QUERY_SURFACE_CURSOR_PRESENT_WITHOUT_CONTEXT")
    _admit(QUERY_RESULT_REF, summary, "QUERY_SURFACE_QUERYRESULT_NOT_ADMITTED")
    return summary


def project_query_surface(response, termination, envelope=None, command=None):
    """Project renderer parity from an owner-admitted query response.

    Returns dict with parity, graphSummary (graph.* only), command used, and
    standing that this is not Run admission or native completeness.
    """
    _admit(QUERY_RESPONSE_REF, response, "QUERY_SURFACE_RESPONSE_NOT_ADMITTED")
    _admit(TERMINATION_REF, termination, "QUERY_SURFACE_TERMINATION_NOT_ADMITTED")
    op = response["operation"]
    ctx = response["context"]
    graph = op in GRAPH_OPERATIONS
    if graph:
        if "coverage" in ctx:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_GRAPH_COVERAGE_INVENTED")
        for key in ("evidence", "countBasis", "traversalCoverage", "factViewDigests", "visitedNodes", "producedItems"):
            if key not in ctx:
                raise QuerySurfaceProjectionError("QUERY_SURFACE_GRAPH_DISCLOSURE_MISSING", key)
        evidence = ctx["evidence"]
        for key in ("coverageIds", "scopeIds", "deficiencyCitations", "resolutionLimitations"):
            if key not in evidence:
                raise QuerySurfaceProjectionError("QUERY_SURFACE_GRAPH_DISCLOSURE_MISSING", "evidence." + key)
        expected_truncated = ctx["traversalCoverage"] == "truncated-bound"
        if ctx["truncated"] is not expected_truncated:
            raise QuerySurfaceProjectionError(
                "QUERY_SURFACE_TRUNCATED_JOIN",
                "truncated=" + str(ctx["truncated"]) + " traversalCoverage=" + ctx["traversalCoverage"],
            )
        if type(response.get("items")) is not list:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_GRAPH_ITEMS_NOT_ARRAY")
    else:
        if "coverage" not in ctx:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_OTHER17_COVERAGE_MISSING")
    for field in CONTEXT_SCALARS:
        if field not in ctx:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_CONTEXT_SCALAR_MISSING", field)
    if "termination" in response and not _equal(response["termination"], termination):
        raise QuerySurfaceProjectionError("QUERY_SURFACE_RESPONSE_TERMINATION_MISMATCH")
    if envelope is not None:
        _admit(ENVELOPE_REF, envelope, "QUERY_SURFACE_ENVELOPE_NOT_ADMITTED")
        if envelope.get("kind") != "query":
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_NOT_QUERY", str(envelope.get("kind")))
        if not _equal(envelope.get("termination"), termination):
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_TERMINATION_MISMATCH")
        expected_exit = Wlegacy.EXIT[termination["class"]]
        if envelope.get("exitCode") != expected_exit:
            raise QuerySurfaceProjectionError(
                "QUERY_SURFACE_EXIT_JOIN",
                str(envelope.get("exitCode")) + "!=" + str(expected_exit),
            )
    parity = {
        "resolved-view": copy.deepcopy(ctx["resolvedView"]),
        "availability": ctx["availability"],
        "truncated": ctx["truncated"],
        "total-items": ctx["totalItems"],
        "termination-class": termination["class"],
        "query-response": copy.deepcopy(response),
    }
    if "coverage" in parity:
        raise QuerySurfaceProjectionError("QUERY_SURFACE_GRAPH_COVERAGE_INVENTED")
    graph_summary = graph_query_result_summary(response) if graph else None
    if graph and envelope is not None:
        if not _equal(envelope.get("query"), graph_summary):
            raise QuerySurfaceProjectionError("QUERY_SURFACE_QUERYRESULT_JOIN")
    cmd = command
    out = {
        "standing": "projection over schema-admitted owned-response shapes; not Run admission; not native closed-world",
        "parity": parity,
        "graphSummary": graph_summary,
        "command": cmd,
        "graph": graph,
    }
    if cmd is not None:
        missing = [k for k in cmd["parityFields"] if k not in parity]
        if missing:
            out["deliveryTermination"] = delivery_required_termination(termination)
            out["missingParityFields"] = missing
            raise QuerySurfaceProjectionError("QUERY_SURFACE_DELIVERY_REQUIRED", ",".join(missing))
    return out


def render_query_formats(parity, envelope, command, hints=None):
    """Inherited strict render across advertised query formats."""
    env = {"parity": parity, "envelope": envelope}
    if hints is not None:
        env["hints"] = hints
    try:
        renderings = [Wlegacy.render(env, fmt, command) for fmt in ADVERTISED_QUERY_FORMATS]
    except KeyError:
        return {
            "ok": False,
            "deliveryTermination": delivery_required_termination(envelope.get("termination") if isinstance(envelope, dict) else None),
            "renderings": [],
        }
    except Wlegacy.Refusal as exc:
        raise QuerySurfaceProjectionError("QUERY_SURFACE_RENDER_REFUSED", exc.error_code) from exc
    return {
        "ok": True,
        "deliveryTermination": None,
        "renderings": renderings,
        "parityHolds": Wlegacy.parity_holds(renderings),
    }


def run_projection_controls(inventory):
    """Measured projection controls. Labelled not-Run-admission. No fake boolean PASS."""
    live = next(c for c in inventory["commands"] if c["name"] == "query")
    prospective = prospective_query_command(live)
    rows = []
    failed = []

    def record(case, ok, **extra):
        row = {"case": case, "result": "PASS" if ok else "FAIL", "kind": "projection-control-not-run-admission"}
        row.update(extra)
        rows.append(row)
        if not ok:
            failed.append(case)

    H64 = "ab" * 32
    H64b = "cd" * 32
    H32 = "ef" * 16
    run_id = "run3:" + H64
    project_id = "prj1-" + H64
    view_id = "view2:" + H64
    cov_id = "coverage2:" + H64
    fact_id = "fact2:" + H64
    fact_id2 = "fact2:" + H64b
    scope_id = "scope2:" + H64
    request_id = "req1_" + H32
    universe = H64
    cursor = "q3." + H64 + "." + H64b + ".0"
    endpoint = {"universe": universe, "kind": "symbol", "nativeSubjectId": "mod.fn"}
    evidence_ok = {
        "coverageIds": [cov_id],
        "scopeIds": [scope_id],
        "deficiencyCitations": [],
        "resolutionLimitations": [],
    }
    neighbor = {
        "factId": fact_id,
        "relation": "calls",
        "resolution": "resolved-callee",
        "source": copy.deepcopy(endpoint),
        "target": {"universe": universe, "kind": "symbol", "nativeSubjectId": "mod.other"},
    }
    neighbor2 = copy.deepcopy(neighbor)
    neighbor2["factId"] = fact_id2
    neighbor2["target"] = {"universe": universe, "kind": "symbol", "nativeSubjectId": "mod.third"}

    def graph_ctx(**over):
        ctx = {
            "projectId": project_id,
            "resolvedView": {"runId": run_id},
            "factViewDigests": [view_id],
            "availability": "retained",
            "truncated": False,
            "totalItems": 2,
            "countBasis": "exact",
            "traversalCoverage": "truncated-page",
            "visitedNodes": 4,
            "producedItems": 5,
            "advisory": False,
            "evidence": copy.deepcopy(evidence_ok),
            "nextCursor": cursor,
        }
        ctx.update(over)
        if "nextCursor" in over and over["nextCursor"] is None:
            del ctx["nextCursor"]
        return ctx

    def graph_response(items, ctx, termination=None, operation="graph.neighbors"):
        body = {
            "schemaFamily": "opensip.product.query",
            "schemaMajor": 3,
            "operation": operation,
            "context": ctx,
            "items": items,
        }
        if termination is not None:
            body["termination"] = copy.deepcopy(termination)
        return body

    success_term = {"class": "success"}
    success_term_with_reason = {
        "class": "operational-failed",
        "errorCode": "HOST.IO_FAILURE",
        "faultCause": "host-io",
    }
    other_failed_term = {
        "class": "operational-failed",
        "errorCode": "DELIVERY.REQUIRED_FAILED",
        "faultCause": "delivery-required",
    }

    def envelope_for(summary, term, extra_query=None):
        q = extra_query if extra_query is not None else summary
        env = {
            "schemaFamily": "opensip.product.envelope",
            "schemaMajor": 3,
            "kind": "query",
            "requestId": request_id,
            "projectId": project_id,
            "termination": copy.deepcopy(term),
            "exitCode": Wlegacy.EXIT[term["class"]],
            "query": copy.deepcopy(q),
        }
        return env

    def other17_response():
        return {
            "schemaFamily": "opensip.product.query",
            "schemaMajor": 3,
            "operation": "coverage.show",
            "context": {
                "projectId": project_id,
                "resolvedView": {"runId": run_id},
                "coverage": "complete",
                "availability": "retained",
                "truncated": False,
                "totalItems": 3,
                "advisory": False,
            },
        }

    other17_summary = {
        "kind": "query",
        "items": 3,
        "truncated": False,
        "completenessMet": True,
        "advisory": False,
    }

    # --- graph exact count with next page ---
    ctx_page = graph_ctx(totalItems=5, producedItems=5, countBasis="exact", traversalCoverage="truncated-page", truncated=False)
    resp_page = graph_response([neighbor, neighbor2], ctx_page)
    summary_page = graph_query_result_summary(resp_page)
    env_page = envelope_for(summary_page, success_term)
    try:
        proj = project_query_surface(resp_page, success_term, envelope=env_page, command=prospective)
        rnd = render_query_formats(proj["parity"], env_page, prospective)
        formats = [r["format"] for r in rnd["renderings"]]
        record(
            "graph-exact-next-page-all-advertised-formats",
            rnd["ok"]
            and rnd["parityHolds"]
            and formats == list(ADVERTISED_QUERY_FORMATS)
            and proj["parity"]["truncated"] is False
            and proj["parity"]["total-items"] == 5
            and type(proj["parity"]["query-response"]["items"]) is list
            and len(proj["parity"]["query-response"]["items"]) == 2
            and summary_page["items"] == 2
            and summary_page["items"] != proj["parity"]["total-items"]
            and summary_page["completenessMet"] is True
            and "nextCursor" in summary_page
            and summary_page["nextCursor"] == cursor
            and "coverage" not in proj["parity"]
            and "evidence" in proj["parity"]["query-response"]["context"],
            queryResultItems=summary_page["items"],
            totalItems=proj["parity"]["total-items"],
            completenessMet=summary_page["completenessMet"],
            formats=formats,
        )
    except Exception as exc:
        record("graph-exact-next-page-all-advertised-formats", False, error=str(exc))

    # --- graph lower-bound prefix, intermediate page truncated=false ---
    ctx_lb = graph_ctx(
        totalItems=2,
        producedItems=2,
        countBasis="lower-bound",
        traversalCoverage="truncated-page",
        truncated=False,
    )
    resp_lb = graph_response([neighbor, neighbor2], ctx_lb)
    try:
        summary_lb = graph_query_result_summary(resp_lb)
        env_lb = envelope_for(summary_lb, success_term)
        proj_lb = project_query_surface(resp_lb, success_term, envelope=env_lb, command=prospective)
        rnd_lb = render_query_formats(proj_lb["parity"], env_lb, prospective)
        record(
            "graph-lower-bound-prefix-intermediate-page",
            rnd_lb["ok"]
            and rnd_lb["parityHolds"]
            and summary_lb["completenessMet"] is False
            and proj_lb["parity"]["truncated"] is False
            and summary_lb["truncated"] is False
            and "coverage" not in proj_lb["parity"],
            completenessMet=summary_lb["completenessMet"],
            truncated=proj_lb["parity"]["truncated"],
            countBasis=ctx_lb["countBasis"],
        )
    except Exception as exc:
        record("graph-lower-bound-prefix-intermediate-page", False, error=str(exc))

    # --- empty graph results with limitations: not native closed-world ---
    empty_ev = copy.deepcopy(evidence_ok)
    empty_ev["resolutionLimitations"] = [{"kind": "unprojectable-fact", "note": "no projected edge"}]
    ctx_empty = graph_ctx(
        totalItems=0,
        producedItems=0,
        visitedNodes=1,
        countBasis="exact",
        traversalCoverage="complete",
        truncated=False,
        nextCursor=None,
        evidence=empty_ev,
    )
    resp_empty = graph_response([], ctx_empty)
    try:
        summary_empty = graph_query_result_summary(resp_empty)
        env_empty = envelope_for(summary_empty, success_term)
        proj_empty = project_query_surface(resp_empty, success_term, envelope=env_empty, command=prospective)
        rnd_empty = render_query_formats(proj_empty["parity"], env_empty, prospective)
        native_inferred = (
            "coverage" in proj_empty["parity"]
            or proj_empty["parity"]["query-response"]["context"].get("coverage") == "complete"
        )
        record(
            "graph-empty-with-limitations-not-native-completeness",
            rnd_empty["ok"]
            and rnd_empty["parityHolds"]
            and summary_empty["items"] == 0
            and summary_empty["completenessMet"] is True
            and len(proj_empty["parity"]["query-response"]["context"]["evidence"]["resolutionLimitations"]) == 1
            and native_inferred is False,
            completenessMet=summary_empty["completenessMet"],
            nativeCompletenessInferred=native_inferred,
            limitationCount=len(proj_empty["parity"]["query-response"]["context"]["evidence"]["resolutionLimitations"]),
        )
    except Exception as exc:
        record("graph-empty-with-limitations-not-native-completeness", False, error=str(exc))

    # --- other17: coverage preserved inside query-response, not as standalone parity key ---
    resp17 = other17_response()
    env17 = envelope_for(other17_summary, success_term)
    try:
        proj17 = project_query_surface(resp17, success_term, envelope=env17, command=prospective)
        rnd17 = render_query_formats(proj17["parity"], env17, prospective)
        record(
            "other17-coverage-show-inside-query-response",
            rnd17["ok"]
            and rnd17["parityHolds"]
            and proj17["graph"] is False
            and proj17["graphSummary"] is None
            and "coverage" not in proj17["parity"]
            and proj17["parity"]["query-response"]["context"]["coverage"] == "complete"
            and proj17["parity"]["total-items"] == 3
            and env17["query"]["items"] == 3
            and type(proj17["parity"]["query-response"].get("items", [])) is not int,
            formats=[r["format"] for r in rnd17["renderings"]],
        )
    except Exception as exc:
        record("other17-coverage-show-inside-query-response", False, error=str(exc))

    # --- missing query-response via live inventory field selection ---
    live_fields = list(live["parityFields"])
    try:
        proj_live_attempt = project_query_surface(resp_page, success_term, envelope=env_page, command=live)
        record("live-inventory-still-requires-coverage-key", False, unexpected="projected against live command", liveFields=live_fields)
    except QuerySurfaceProjectionError as exc:
        record(
            "live-inventory-still-requires-coverage-key",
            exc.code == "QUERY_SURFACE_DELIVERY_REQUIRED" and "coverage" in (exc.detail or ""),
            code=exc.code,
            detail=exc.detail,
            liveFields=live_fields,
            prospectiveFields=list(PROSPECTIVE_QUERY_PARITY_FIELDS),
            selection="UNMET-until-root-applies-inventory" if live_fields != list(PROSPECTIVE_QUERY_PARITY_FIELDS) else "matched",
        )

    # --- inherited render KeyError on missing query-response, no invented runId ---
    try:
        incomplete = {
            "resolved-view": {"runId": run_id},
            "availability": "retained",
            "truncated": False,
            "total-items": 2,
            "termination-class": "success",
        }
        rnd_miss = render_query_formats(incomplete, env_page, prospective)
        no_run = "runId" not in (rnd_miss["deliveryTermination"] or {})
        record(
            "missing-query-response-delivery-required-no-invented-run",
            rnd_miss["ok"] is False
            and rnd_miss["deliveryTermination"]["errorCode"] == "DELIVERY.REQUIRED_FAILED"
            and rnd_miss["deliveryTermination"]["faultCause"] == "delivery-required"
            and rnd_miss["deliveryTermination"]["class"] == "operational-failed"
            and no_run,
            delivery=rnd_miss["deliveryTermination"],
        )
    except Exception as exc:
        record("missing-query-response-delivery-required-no-invented-run", False, error=str(exc))

    # preserve already-present runId, do not replace it
    term_with_run = {"class": "success", "runId": run_id}
    preserved = delivery_required_termination(term_with_run)
    invented = delivery_required_termination({"class": "success"})
    record(
        "delivery-required-preserves-only-existing-runId",
        preserved.get("runId") == run_id and "runId" not in invented,
        preserved=preserved,
        inventedHasRunId="runId" in invented,
    )

    # --- missing required nested graph disclosure (not schema-admitted) ---
    bad_ctx = graph_ctx()
    del bad_ctx["evidence"]
    bad_resp = graph_response([neighbor], bad_ctx)
    try:
        project_query_surface(bad_resp, success_term, command=prospective)
        record("missing-graph-evidence-refused", False, unexpected="admitted")
    except QuerySurfaceProjectionError as exc:
        record(
            "missing-graph-evidence-refused",
            exc.code in ("QUERY_SURFACE_RESPONSE_NOT_ADMITTED", "QUERY_SURFACE_GRAPH_DISCLOSURE_MISSING"),
            code=exc.code,
        )

    # --- conflicting leftover scalar vs context (claimed override) ---
    try:
        proj_ok = project_query_surface(resp_page, success_term, envelope=env_page, command=prospective)
        claimed = copy.deepcopy(proj_ok["parity"])
        claimed["total-items"] = 99
        mismatch = claimed["total-items"] != resp_page["context"]["totalItems"]
        record(
            "conflicting-scalar-vs-context-detected",
            mismatch and proj_ok["parity"]["total-items"] == resp_page["context"]["totalItems"] == 5,
            derived=proj_ok["parity"]["total-items"],
            claimedOverride=claimed["total-items"],
        )
    except Exception as exc:
        record("conflicting-scalar-vs-context-detected", False, error=str(exc))

    # helper refuses if we could pass a mutated leftover through a second check
    try:
        proj_ok = project_query_surface(resp_page, success_term, envelope=env_page, command=prospective)
        mutated = copy.deepcopy(resp_page)
        mutated["context"]["totalItems"] = 99
        # truncated-page + truncated false still; schema admits 99
        env_mut = envelope_for(graph_query_result_summary(mutated), success_term)
        proj_mut = project_query_surface(mutated, success_term, envelope=env_mut, command=prospective)
        record(
            "derived-scalars-follow-context-not-caller-memory",
            proj_mut["parity"]["total-items"] == 99 and proj_ok["parity"]["total-items"] == 5,
            first=proj_ok["parity"]["total-items"],
            second=proj_mut["parity"]["total-items"],
        )
    except Exception as exc:
        record("derived-scalars-follow-context-not-caller-memory", False, error=str(exc))

    # --- response termination vs envelope termination: full object, not class-only ---
    resp_term = graph_response([neighbor, neighbor2], ctx_page, termination=success_term_with_reason)
    env_conflict = envelope_for(
        # summary still from a success-shaped graph page would fail query join; use matching summary after admit
        {"kind": "query", "items": 2, "truncated": False, "completenessMet": True, "advisory": False, "nextCursor": cursor},
        other_failed_term,
    )
    try:
        project_query_surface(resp_term, other_failed_term, envelope=env_conflict, command=prospective)
        record("response-envelope-termination-full-mismatch-refused", False, unexpected="admitted")
    except QuerySurfaceProjectionError as exc:
        record(
            "response-envelope-termination-full-mismatch-refused",
            exc.code == "QUERY_SURFACE_RESPONSE_TERMINATION_MISMATCH"
            and success_term_with_reason["class"] == other_failed_term["class"]
            and success_term_with_reason["errorCode"] != other_failed_term["errorCode"],
            code=exc.code,
            sameClass=success_term_with_reason["class"] == other_failed_term["class"],
        )

    # agreeing full termination on both sides
    try:
        resp_agree = graph_response([neighbor, neighbor2], ctx_page, termination=success_term)
        env_agree = envelope_for(graph_query_result_summary(resp_agree), success_term)
        proj_agree = project_query_surface(resp_agree, success_term, envelope=env_agree, command=prospective)
        record(
            "response-envelope-termination-full-agree",
            proj_agree["parity"]["termination-class"] == "success"
            and _equal(resp_agree["termination"], env_agree["termination"]),
        )
    except Exception as exc:
        record("response-envelope-termination-full-agree", False, error=str(exc))

    # --- QueryResult.items is count; query-response.items is array ---
    try:
        kinds_ok = type(summary_page["items"]) is int and type(resp_page["items"]) is list
        record(
            "queryresult-items-count-not-graph-items-array",
            kinds_ok and summary_page["items"] == len(resp_page["items"]) != resp_page["context"]["totalItems"],
            queryResultItemsType=type(summary_page["items"]).__name__,
            responseItemsType=type(resp_page["items"]).__name__,
        )
    except Exception as exc:
        record("queryresult-items-count-not-graph-items-array", False, error=str(exc))

    # --- complete query-response not field-selected: evidence survives ---
    try:
        proj_full = project_query_surface(resp_page, success_term, envelope=env_page, command=prospective)
        qr = proj_full["parity"]["query-response"]
        record(
            "query-response-is-complete-owned-object",
            _equal(qr, resp_page)
            and "evidence" in qr["context"]
            and "countBasis" in qr["context"]
            and "traversalCoverage" in qr["context"]
            and "factViewDigests" in qr["context"]
            and "nextCursor" in qr["context"],
        )
    except Exception as exc:
        record("query-response-is-complete-owned-object", False, error=str(exc))

    selected = list(live["parityFields"])
    rows.append(
        {
            "case": "selected-inventory-query-parity-keys",
            "result": "PASS" if selected == list(PROSPECTIVE_QUERY_PARITY_FIELDS) else "UNMET",
            "kind": "inventory-selection-honest-until-root-handoff",
            "selected": selected,
            "prospective": list(PROSPECTIVE_QUERY_PARITY_FIELDS),
            "note": "Do not mutate W-owned inventory. Final launcher must require selected==prospective after root applies the keys.",
        }
    )

    return {
        "standing": "projection controls over schema-admitted owned-response shapes; not Run admission; not traversal evidence",
        "passed": not failed,
        "failed": failed,
        "rows": rows,
        "prospectiveParityFields": list(PROSPECTIVE_QUERY_PARITY_FIELDS),
        "advertisedFormats": list(ADVERTISED_QUERY_FORMATS),
    }
