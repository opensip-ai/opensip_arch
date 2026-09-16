"""Query renderer-parity projection. Design/reference only.

Pure helper: no semantic authority, no Run admission, no graph walk. The public
carrier is CommandEnvelope major 3 kind=query with querySurface=graph-query-response
and the complete owner-admitted GraphQueryResponseV1 in queryResponse. Callers supply
that response and the enclosing actual StepTermination / CommandEnvelope.

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
QUERY_PARITY_FIELDS = (
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
QUERY_SURFACE_GRAPH = "graph-query-response"
QUERY_SURFACE_NON_GRAPH = ("discovery-recommendation", "baseline-inspection", "effective-policy", "policy-test-result",
                           "candidate-list", "candidate-inspection", "review-brief", "repair-preview")
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
    """Local command row with the six required parity keys. Does not mutate inventory."""
    cmd = copy.deepcopy(live_command)
    cmd["parityFields"] = list(QUERY_PARITY_FIELDS)
    return cmd


def _admit(ref, value, code):
    try:
        Wprof.validate_profile(ref, value)
    except Exception as exc:
        raise QuerySurfaceProjectionError(code, str(exc)) from exc


def _equal(a, b):
    return canonical.equal_typed(a, b)


def delivery_required_termination(enclosing=None, *, committed=None):
    """Existing required-delivery law with its registered detail.

    committed=None infers a committed Run from the enclosing termination's runId (analysis commands). Query
    renderings pass committed=False: a historical query read never commits a Run. After commit the runId is
    retained with DELIVERY.RENDERER_FAILED_AFTER_COMMIT; otherwise no runId is invented and the detail is
    DELIVERY.REQUIRED_PROJECTION_FAILED.
    """
    t = {
        "class": "operational-failed",
        "errorCode": "DELIVERY.REQUIRED_FAILED",
        "faultCause": "delivery-required",
    }
    run_id = enclosing.get("runId") if isinstance(enclosing, dict) else None
    if committed is None:
        committed = run_id is not None
    if committed and run_id is not None:
        t["runId"] = run_id
        t["domainDetail"] = {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT", "remedy": "the Run is committed; rerun the renderer with this runId"}
    else:
        t["domainDetail"] = {"code": "DELIVERY.REQUIRED_PROJECTION_FAILED", "remedy": "no Run was committed; retry when the required projection can be delivered"}
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
        if envelope.get("projectId") != ctx["projectId"]:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_PROJECT_JOIN")
        if not _equal(envelope.get("termination"), termination):
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_TERMINATION_MISMATCH")
        expected_exit = Wlegacy.EXIT[termination["class"]]
        if envelope.get("exitCode") != expected_exit:
            raise QuerySurfaceProjectionError(
                "QUERY_SURFACE_EXIT_JOIN",
                str(envelope.get("exitCode")) + "!=" + str(expected_exit),
            )
        if envelope.get("querySurface") != QUERY_SURFACE_GRAPH:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_SELECTOR", str(envelope.get("querySurface")))
        if not _equal(envelope.get("queryResponse"), response):
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_RESPONSE_MISMATCH")
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


def _parity_from_rendering(rendering, command):
    """Recover parity from one rendering alone (no caller memory)."""
    body = rendering["body"]
    if rendering["format"] in ("json", "agent"):
        if rendering["format"] == "json" and "agentHints" in body:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_JSON_CARRIES_AGENT_HINTS")
        _admit(ENVELOPE_REF, body, "QUERY_SURFACE_ENVELOPE_NOT_ADMITTED")
        return project_query_surface(body["queryResponse"], body["termination"], envelope=body, command=command)["parity"]
    out = {}
    for line in body.splitlines():
        label, _, value = line.partition(": ")
        out[label] = canonical.parse(value.encode())
    return out


def render_query_formats(parity, envelope, command, hints=None):
    """Render every advertised query format from the public CommandEnvelope major 3 carrier.

    json is the envelope itself; agent is the same envelope plus agentHints; human prints every parity field
    by its fixed label with the canonical JSON value. Parity is recovered from each rendering alone and must
    equal the owner projection. A carrier or parity field that cannot be delivered is the required-delivery
    fault; a query never commits a Run, so no runId is invented.
    """
    def failed():
        return {"ok": False, "deliveryTermination": delivery_required_termination(committed=False), "renderings": []}

    for fmt in ADVERTISED_QUERY_FORMATS:
        if fmt not in command["formats"]:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_RENDER_REFUSED", "OUTPUT.FORMAT_NOT_APPLICABLE")
    if not isinstance(envelope, dict) or not isinstance(parity, dict) or any(k not in parity for k in command["parityFields"]):
        return failed()
    try:
        _admit(ENVELOPE_REF, envelope, "QUERY_SURFACE_ENVELOPE_NOT_ADMITTED")
        owner = project_query_surface(envelope["queryResponse"], envelope["termination"], envelope=envelope, command=command)["parity"]
    except (QuerySurfaceProjectionError, KeyError):
        return failed()
    fields = list(command["parityFields"])
    if not _equal({k: parity[k] for k in fields}, {k: owner[k] for k in fields}):
        raise QuerySurfaceProjectionError("QUERY_SURFACE_PARITY_NOT_OWNER_PROJECTION")
    renderings = []
    for fmt in ADVERTISED_QUERY_FORMATS:
        if fmt == "json":
            body = copy.deepcopy(envelope)
            body.pop("agentHints", None)
        elif fmt == "agent":
            body = copy.deepcopy(envelope)
            body["agentHints"] = list(hints or [])
        else:
            body = "".join(k + ": " + canonical.canonical(parity[k]).decode() + "\n" for k in fields)
        renderings.append({"format": fmt, "body": body})
    recovered = [_parity_from_rendering(r, command) for r in renderings]
    holds = all(_equal({k: p.get(k) for k in fields}, {k: owner[k] for k in fields}) for p in recovered)
    return {"ok": True, "deliveryTermination": None, "renderings": renderings, "parityHolds": holds}


QUERY_STEP_PARAMS_REF = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/QueryParams"
DD = _load("query_surface_discovery_defaults", HERE.parent / "discovery-defaults.py")
COMMAND_RENDER_FORMATS = ("human", "json", "agent")


def json_pointer(document, pointer):
    """Resolve one published queryDispatch.parityPaths pointer inside an envelope (tokens are never escaped)."""
    node = document
    for token in pointer.split("/")[1:]:
        if not isinstance(node, dict) or token not in node:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_PARITY_PATH_MISSING", pointer)
        node = node[token]
    return node


def _join(ok, code, detail=None):
    if not ok:
        raise QuerySurfaceProjectionError(code, detail)


def admit_query_step_params(params):
    """Closed query-step params, plus the public request join: request operation, completeness and page equal the step's."""
    _admit(QUERY_STEP_PARAMS_REF, params, "QUERY_SURFACE_STEP_PARAMS_NOT_ADMITTED")
    if "completeness" in params:
        request = params["request"]
        _join(request["operation"] == params["operation"] and request["completeness"] == params["completeness"]
              and _equal(request["page"], params["page"]), "QUERY_SURFACE_STEP_REQUEST_JOIN")
    return params


def _summary(items, truncated, complete, advisory, cursor=None):
    out = {"kind": "query", "items": items, "truncated": truncated, "completenessMet": complete, "advisory": advisory}
    if cursor is not None:
        out["nextCursor"] = cursor
    return out


def command_surface_summary(surface, record, envelope):
    """Cross-record joins of one typed non-graph carrier and its compact QueryResult (workflows-and-surfaces §8)."""
    if surface == "discovery-recommendation":
        units = record["discovery"]["units"]
        roots_known = {u["rootPath"] for u in units}
        for proposal in record["config2Proposals"]:
            try:
                roots = [DD.normalize_explicit_root(r) for r in proposal["workspaceRoots"]]
            except Exception as exc:
                raise QuerySurfaceProjectionError("QUERY_SURFACE_CONFIG2_ROOT_GRAMMAR", str(exc)) from exc
            _join(len(set(roots)) == len(roots) and set(roots) <= roots_known, "QUERY_SURFACE_CONFIG2_ROOT_NOT_DISCOVERED")
            _join(sorted(proposal["unitOrdinals"]) == sorted(u["unitOrdinal"] for u in units if u["rootPath"] in set(roots)), "QUERY_SURFACE_CONFIG2_UNIT_JOIN")
        return _summary(len(record["recommendations"]), False, True, True)
    if surface == "baseline-inspection":
        artifact = record["baseline"]
        try:
            Wprof.verify_baseline_artifact_v3(artifact)
        except Wprof.Refusal as exc:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_BASELINE_NOT_ADMITTED", str(exc.detail)) from exc
        rows = record["pivotClosureAvailability"]
        _join([(r["closureId"], r["kind"]) for r in rows] == [(p["closureId"], p["kind"]) for p in artifact["descriptor"]["pivotClosure"]],
              "QUERY_SURFACE_PIVOT_AVAILABILITY_JOIN")
        return _summary(len(rows), False, all(r["state"] == "available" for r in rows), False)
    if surface == "effective-policy":
        _join(record["policyDigest"] == Wprof.doc_digest(record["policy"]), "QUERY_SURFACE_POLICY_DIGEST_JOIN")
        _join(record["waiverSetDigest"] == Wprof.doc_digest(record["effectiveWaivers"]), "QUERY_SURFACE_WAIVER_DIGEST_JOIN")
        effective = {w["waiverId"] for w in record["effectiveWaivers"]["waivers"]}
        res = record["waiverResolution"]
        _join(res["effectiveCount"] == len(effective) and not ((set(res["expired"]) | set(res["duplicatesRejected"])) & effective),
              "QUERY_SURFACE_WAIVER_RESOLUTION_JOIN")
        return _summary(len(record["policy"]["rules"]), False, True, False)
    if surface == "policy-test-result":
        result = record["result"]
        preimage = {k: v for k, v in result.items() if k != "policyTestResultId"}
        _join(result["policyTestResultId"] == Wlegacy.wid("policytest2", "workflow.policy-test-result", preimage), "QUERY_SURFACE_POLICY_TEST_ID_JOIN")
        counts = {"passed": 0, "failed": 0, "indeterminate": 0, "notExecutable": 0}
        for case in result["results"]:
            counts["notExecutable" if case["outcome"] == "not-executable" else case["outcome"]] += 1
        _join(_equal(counts, result["summary"]), "QUERY_SURFACE_POLICY_TEST_SUMMARY_JOIN")
        complete = result["resolverAccepted"] and counts["indeterminate"] == 0 and counts["notExecutable"] == 0
        return _summary(len(result["results"]), False, complete, False)
    if surface in ("candidate-list", "candidate-inspection", "review-brief"):
        ctx = record["context"]
        _join(ctx["projectId"] == envelope.get("projectId"), "QUERY_SURFACE_PROJECT_JOIN")
        _join(ctx["advisory"] is True, "QUERY_SURFACE_ADVISORY_JOIN")
        run_id = ctx["resolvedView"].get("runId")
        _join(run_id is not None, "QUERY_SURFACE_CONCRETE_RUN_REQUIRED")
        cursor = ctx.get("nextCursor")
        if surface == "candidate-list":
            cands = record["candidates"]
            _join(all(c["runId"] == run_id for c in cands), "QUERY_SURFACE_CANDIDATE_RUN_JOIN")
            levels = {lvl: sum(1 for c in cands if c["evidenceLevel"] == lvl) for lvl in ("proof-backed", "partial-coverage", "advisory-only")}
            _join(_equal(levels, record["evidenceLevels"]), "QUERY_SURFACE_EVIDENCE_LEVEL_JOIN")
            if record["includeSuppressed"]:
                _join(record["suppressedCount"] == sum(1 for c in cands if c["suppressed"]), "QUERY_SURFACE_SUPPRESSED_COUNT_JOIN")
            else:
                _join(not any(c["suppressed"] for c in cands), "QUERY_SURFACE_SUPPRESSED_LISTED")
            _join(ctx["truncated"] or ctx["totalItems"] == len(cands), "QUERY_SURFACE_TOTAL_ITEMS_JOIN")
            return _summary(len(cands), ctx["truncated"], ctx["coverage"] == "complete", True, cursor)
        if surface == "candidate-inspection":
            insp = record["inspection"]
            _join(insp["runId"] == run_id, "QUERY_SURFACE_CANDIDATE_RUN_JOIN")
            _join(insp["facts"] == sorted(set(insp["facts"]), key=lambda s: s.encode()), "QUERY_SURFACE_INSPECTION_ORDER")
            _join(ctx["totalItems"] == len(insp["facts"]), "QUERY_SURFACE_TOTAL_ITEMS_JOIN")
            return _summary(len(insp["facts"]), ctx["truncated"], ctx["coverage"] == "complete", True, cursor)
        brief = record["brief"]
        _join(brief["runId"] == run_id, "QUERY_SURFACE_CANDIDATE_RUN_JOIN")
        _join(brief["truncated"] == ctx["truncated"], "QUERY_SURFACE_TRUNCATED_JOIN")
        _join(ctx["totalItems"] >= len(brief["candidates"]) and brief["truncated"] == (ctx["totalItems"] > len(brief["candidates"])), "QUERY_SURFACE_TOTAL_ITEMS_JOIN")
        return _summary(len(brief["candidates"]), brief["truncated"], not brief["truncated"], True, cursor)
    if surface == "repair-preview":
        plan, preview = record["plan"], record["preview"]
        desc = plan["descriptor"]
        _join(plan["repairPlanId"] == Wlegacy.wid("repairplan2", "workflow.repair-plan", desc), "QUERY_SURFACE_REPAIR_PLAN_ID_JOIN")
        _join(preview["repairPlanId"] == plan["repairPlanId"] and preview["snapshotId"] == desc["snapshotId"] and preview["applicable"] == desc["applicable"]
              and _equal(preview["unmetPreconditions"], desc["unmetPreconditions"]), "QUERY_SURFACE_REPAIR_PREVIEW_JOIN")
        _join(desc["projectId"] == envelope.get("projectId"), "QUERY_SURFACE_PROJECT_JOIN")
        return _summary(len(desc["edits"]), False, preview["applicable"], False)
    raise QuerySurfaceProjectionError("QUERY_SURFACE_UNKNOWN_SURFACE", surface)


def project_command_surface(envelope, command):
    """Admit the public carrier of one query-class command, run its joins, then read every parity field at its pointer.

    Closed record/response admission and joins precede any rendering. The query command delegates to
    project_query_surface for its graph joins."""
    dispatch = command.get("queryDispatch")
    if not dispatch:
        raise QuerySurfaceProjectionError("QUERY_SURFACE_COMMAND_NOT_QUERY_CLASS", str(command.get("name")))
    _admit(ENVELOPE_REF, envelope, "QUERY_SURFACE_ENVELOPE_NOT_ADMITTED")
    _join(envelope.get("kind") == "query", "QUERY_SURFACE_ENVELOPE_NOT_QUERY", str(envelope.get("kind")))
    _join(envelope.get("querySurface") == dispatch["surface"], "QUERY_SURFACE_ENVELOPE_SELECTOR", str(envelope.get("querySurface")))
    _join(envelope.get("exitCode") == Wlegacy.EXIT[envelope["termination"]["class"]], "QUERY_SURFACE_EXIT_JOIN")
    _join(set(dispatch["parityPaths"]) == set(command["parityFields"]), "QUERY_SURFACE_PARITY_PATHS_DRIFT")
    if dispatch["surface"] == QUERY_SURFACE_GRAPH:
        project_query_surface(envelope["queryResponse"], envelope["termination"], envelope=envelope, command=command)
        summary = copy.deepcopy(envelope["query"])
    else:
        summary = command_surface_summary(dispatch["surface"], envelope["queryRecord"], envelope)
        _join(_equal(envelope["query"], summary), "QUERY_SURFACE_QUERYRESULT_JOIN")
    parity = {field: copy.deepcopy(json_pointer(envelope, dispatch["parityPaths"][field])) for field in command["parityFields"]}
    return {"surface": dispatch["surface"], "parity": parity, "summary": summary}


def parity_from_human(body):
    """Recover parity from the human rendering's labelled canonical-JSON lines alone."""
    out = {}
    for line in body.splitlines():
        label, _, value = line.partition(": ")
        out[label] = canonical.parse(value.encode())
    return out


def render_command_formats(envelope, command, hints=None):
    """Render json (the envelope), agent (the envelope plus agentHints) and human (labelled parity) for any query-class
    command. The carrier is admitted and joined first; parity recovered from every rendering must equal the owner
    projection. An undeliverable carrier is the pre-commit required-delivery fault (a query never commits a Run).
    HTML renderings are not modelled by this reference."""
    try:
        owner = project_command_surface(envelope, command)["parity"]
    except (QuerySurfaceProjectionError, KeyError, TypeError):
        return {"ok": False, "deliveryTermination": delivery_required_termination(committed=False), "renderings": []}
    fields = list(command["parityFields"])
    renderings = []
    for fmt in COMMAND_RENDER_FORMATS:
        if fmt not in command["formats"]:
            continue
        if fmt == "json":
            body = copy.deepcopy(envelope)
            body.pop("agentHints", None)
        elif fmt == "agent":
            body = copy.deepcopy(envelope)
            body["agentHints"] = list(hints or [])
        else:
            body = "".join(k + ": " + canonical.canonical(owner[k]).decode() + "\n" for k in fields)
        renderings.append({"format": fmt, "body": body})
    recovered = []
    for r in renderings:
        if r["format"] == "human":
            recovered.append(parity_from_human(r["body"]))
        else:
            _join(r["format"] != "json" or "agentHints" not in r["body"], "QUERY_SURFACE_JSON_CARRIES_AGENT_HINTS")
            recovered.append(project_command_surface(r["body"], command)["parity"])
    holds = all(_equal({k: p.get(k) for k in fields}, {k: owner[k] for k in fields}) for p in recovered)
    return {"ok": True, "deliveryTermination": None, "renderings": renderings, "parityHolds": holds, "parity": owner}


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

    def envelope_for(summary, term, response, extra_query=None):
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
            "querySurface": QUERY_SURFACE_GRAPH,
            "queryResponse": copy.deepcopy(response),
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
    env_page = envelope_for(summary_page, success_term, resp_page)
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
        env_lb = envelope_for(summary_lb, success_term, resp_lb)
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
        env_empty = envelope_for(summary_empty, success_term, resp_empty)
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
    env17 = envelope_for(other17_summary, success_term, resp17)
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

    # The selected inventory must actually carry the complete typed response.
    selected = list(live["parityFields"])
    record("selected-inventory-query-parity-keys", selected == list(QUERY_PARITY_FIELDS),
           selected=selected, required=list(QUERY_PARITY_FIELDS))
    try:
        selected_projection = project_query_surface(resp_page, success_term, envelope=env_page, command=live)
        selected_render = render_query_formats(selected_projection["parity"], env_page, live)
        record("selected-inventory-query-rendering", selected_render["ok"] and selected_render["parityHolds"])
    except Exception as exc:
        record("selected-inventory-query-rendering", False, error=str(exc))

    # A shape-valid response cannot be attached to another project's envelope.
    wrong_project = copy.deepcopy(env_page)
    wrong_project["projectId"] = "prj1-" + H64b
    try:
        project_query_surface(resp_page, success_term, envelope=wrong_project, command=live)
        record("response-envelope-project-mismatch-refused", False)
    except QuerySurfaceProjectionError as exc:
        record("response-envelope-project-mismatch-refused", exc.code == "QUERY_SURFACE_PROJECT_JOIN", code=exc.code)

    # The compact envelope summary must agree with the owner's page, not its total.
    wrong_summary = copy.deepcopy(env_page)
    wrong_summary["query"]["items"] = resp_page["context"]["totalItems"]
    try:
        project_query_surface(resp_page, success_term, envelope=wrong_summary, command=live)
        record("response-envelope-page-count-mismatch-refused", False)
    except QuerySurfaceProjectionError as exc:
        record("response-envelope-page-count-mismatch-refused", exc.code == "QUERY_SURFACE_QUERYRESULT_JOIN", code=exc.code)

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
        env_mut = envelope_for(graph_query_result_summary(mutated), success_term, mutated)
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
        resp_term,
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
        env_agree = envelope_for(graph_query_result_summary(resp_agree), success_term, resp_agree)
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

    # --- public carrier: CommandEnvelope major 3 queryResponse selected by querySurface ---
    def schema_ok(ref, value):
        try:
            Wprof.validate_profile(ref, value)
            return True
        except Exception:
            return False

    record("envelope-carries-complete-query-response", schema_ok(ENVELOPE_REF, env_page) and _equal(env_page["queryResponse"], resp_page))
    no_response = copy.deepcopy(env_page)
    del no_response["queryResponse"]
    record("graph-selector-without-query-response-refused-by-schema", not schema_ok(ENVELOPE_REF, no_response))
    no_selector = copy.deepcopy(env_page)
    del no_selector["querySurface"]
    record("query-kind-without-selector-refused-by-schema", not schema_ok(ENVELOPE_REF, no_selector))
    other_with_response = copy.deepcopy(env_page)
    other_with_response["querySurface"] = "candidate-list"
    record("non-graph-surface-with-query-response-refused-by-schema", not schema_ok(ENVELOPE_REF, other_with_response))
    other_summary = copy.deepcopy(other_with_response)
    del other_summary["queryResponse"]
    record("non-graph-surface-without-typed-record-refused-by-schema", not schema_ok(ENVELOPE_REF, other_summary))
    other_summary["queryRecord"] = {
        "surface": "candidate-list",
        "context": {"projectId": project_id, "resolvedView": {"runId": run_id}, "coverage": "complete", "availability": "retained",
                    "truncated": False, "totalItems": 0, "advisory": True},
        "includeSuppressed": False, "candidates": [], "evidenceLevels": {"proof-backed": 0, "partial-coverage": 0, "advisory-only": 0}, "suppressedCount": 0,
    }
    other_summary["query"] = {"kind": "query", "items": 0, "truncated": False, "completenessMet": True, "advisory": True}
    record("non-graph-surface-with-its-typed-record-admitted", schema_ok(ENVELOPE_REF, other_summary))
    untyped = copy.deepcopy(other_summary)
    untyped["queryRecord"]["payload"] = {"anything": True}
    record("typed-record-with-untyped-member-refused-by-schema", not schema_ok(ENVELOPE_REF, untyped))
    try:
        project_query_surface(resp_page, success_term, envelope=other_summary, command=live)
        record("query-command-cannot-select-a-non-graph-surface", False)
    except QuerySurfaceProjectionError as exc:
        record("query-command-cannot-select-a-non-graph-surface", exc.code == "QUERY_SURFACE_ENVELOPE_SELECTOR", code=exc.code)
    failure_env = {
        "schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": request_id,
        "termination": {"class": "request-rejected", "errorCode": "IDENTITY.UNKNOWN", "domainDetail": {"code": "QUERY.VIEW_UNKNOWN", "remedy": "run an analysis first"}},
        "exitCode": 2, "errors": [{"code": "QUERY.VIEW_UNKNOWN", "remedy": "run an analysis first"}], "queryResponse": copy.deepcopy(resp_page),
    }
    record("non-query-kind-cannot-carry-query-response", not schema_ok(ENVELOPE_REF, failure_env))
    del failure_env["queryResponse"]
    record("query-latest-empty-failure-envelope-with-owner-detail-admitted", schema_ok(ENVELOPE_REF, failure_env))
    swapped = copy.deepcopy(env_page)
    swapped["queryResponse"] = copy.deepcopy(resp_lb)
    try:
        project_query_surface(resp_page, success_term, envelope=swapped, command=live)
        record("envelope-response-must-equal-projected-response", False)
    except QuerySurfaceProjectionError as exc:
        record("envelope-response-must-equal-projected-response", exc.code == "QUERY_SURFACE_ENVELOPE_RESPONSE_MISMATCH", code=exc.code)
    try:
        page_parity = project_query_surface(resp_page, success_term, envelope=env_page, command=live)["parity"]
        carrier = render_query_formats(page_parity, env_page, live, hints=["advisory hint"])
        bodies = {r["format"]: r["body"] for r in carrier["renderings"]}
        record(
            "json-and-agent-renderings-are-public-envelopes",
            carrier["ok"] and carrier["parityHolds"] and schema_ok(ENVELOPE_REF, bodies["json"]) and schema_ok(ENVELOPE_REF, bodies["agent"])
            and "agentHints" not in bodies["json"] and bodies["agent"]["agentHints"] == ["advisory hint"]
            and _equal(bodies["json"]["queryResponse"], resp_page) and isinstance(bodies["human"], str),
        )
        missing_carrier = render_query_formats(page_parity, no_response, live)
        pre = missing_carrier["deliveryTermination"] or {}
        record(
            "missing-carrier-is-precommit-required-delivery",
            missing_carrier["ok"] is False and "runId" not in pre
            and pre.get("domainDetail", {}).get("code") == "DELIVERY.REQUIRED_PROJECTION_FAILED" and schema_ok(TERMINATION_REF, pre),
            delivery=pre,
        )
        post = delivery_required_termination({"class": "success", "runId": run_id})
        bad_post = {k: v for k, v in post.items() if k != "runId"}
        record(
            "after-commit-detail-requires-committed-run",
            schema_ok(TERMINATION_REF, post) and post["domainDetail"]["code"] == "DELIVERY.RENDERER_FAILED_AFTER_COMMIT" and not schema_ok(TERMINATION_REF, bad_post),
        )
        record("precommit-detail-forbids-run", not schema_ok(TERMINATION_REF, dict(pre, runId=run_id)))
    except Exception as exc:
        record("json-and-agent-renderings-are-public-envelopes", False, error=str(exc))
    surfaces = {c["name"]: c.get("queryDispatch", {}).get("surface") for c in inventory["commands"] if c["requestClass"] == "query"}
    record(
        "query-class-selector-join-only-query-command-carries-response",
        [n for n, s in surfaces.items() if s == QUERY_SURFACE_GRAPH] == ["query"]
        and None not in surfaces.values() and len(set(surfaces.values())) == len(surfaces) == 9
        and set(surfaces.values()) == {QUERY_SURFACE_GRAPH, *QUERY_SURFACE_NON_GRAPH},
        surfaces=surfaces,
    )

    return {
        "standing": "projection controls over schema-admitted owned-response shapes; not Run admission; not traversal evidence",
        "passed": not failed,
        "failed": failed,
        "rows": rows,
        "requiredParityFields": list(QUERY_PARITY_FIELDS),
        "advertisedFormats": list(ADVERTISED_QUERY_FORMATS),
    }
