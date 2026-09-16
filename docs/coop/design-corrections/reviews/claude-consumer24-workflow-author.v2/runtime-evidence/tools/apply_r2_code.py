"""R2 reference code: owner projections for non-graph command surfaces, generic typed carrier admission/parity/render,
closed query-step params admission, schema loaders, and updated v1 carrier controls. Exact-once edits."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import apply  # noqa: E402

WPM = 'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py'
QSP = 'docs/coop/design-corrections/workflows/query_surface_projection.v3.py'
CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
CQP = 'docs/coop/design-corrections/workflows/check-query-projection.v3.py'
rows = []

MODEL_PROJECTIONS = r'''NON_GRAPH_EVIDENCE_LEVELS = ("proof-backed", "partial-coverage", "advisory-only")
INSPECTION_FACT_LIMIT = 4096
INSPECTION_REF_LIMIT = 64


def non_graph_query_context(view, total_items, advisory, truncated=False):
    """GraphQueryResponseContext of a Run-backed non-graph command surface (candidates, inspect, review brief).

    coverage is complete exactly when the admitted proof was evaluated with no execution deficiency and every enabled
    rule's enumeration is complete; otherwise partial. availability is retained because the Run was admitted."""
    enabled = {r["ruleId"] for r in view["policy"]["rules"] if r["enabled"]}
    complete = (
        view["evaluationState"] == "evaluated"
        and not view["executionDeficiencies"]
        and all(rr["enumeration"]["state"] == "complete" for rr in view["ruleResults"] if rr["ruleId"] in enabled)
    )
    return {"projectId": view["projectId"], "resolvedView": {"runId": view["runId"]}, "coverage": "complete" if complete else "partial",
            "availability": "retained", "truncated": truncated, "totalItems": total_items, "advisory": advisory}


def candidate_evidence_level_counts(candidates) -> dict:
    return {level: sum(1 for c in candidates if c["evidenceLevel"] == level) for level in NON_GRAPH_EVIDENCE_LEVELS}


def project_candidate_list(view, include_suppressed):
    """candidates: every Run candidate; suppressed candidates are listed only on request and always counted."""
    everything = list(view["candidates"])
    suppressed = [c for c in everything if c["suppressed"]]
    listed = everything if include_suppressed else [c for c in everything if not c["suppressed"]]
    return {"candidates": copy.deepcopy(listed), "suppressedCount": len(suppressed), "evidenceLevels": candidate_evidence_level_counts(listed)}


def project_inspection_bundle(view, candidate_id):
    """inspect: review:2 InspectionBundle of one candidate of an admitted Run (workflows-and-surfaces §5 inspection law).

    facts/coverageIds/importIds are the fact2/coverage2/import2 evidenceRefs of the candidate's findings, unique and
    sorted by UTF-8 bytes; limitations name every unmatched correspondence reason, an incomplete enumeration of the
    candidate's rule, and any bound truncation. An unknown candidate refuses IDENTITY.UNKNOWN / REVIEW.CANDIDATE_UNKNOWN."""
    cand = next((c for c in view["candidates"] if c["candidateId"] == candidate_id), None)
    if cand is None:
        raise Refusal("IDENTITY.UNKNOWN", "REVIEW.CANDIDATE_UNKNOWN", "candidateId is not a candidate of the admitted Run", candidate_id)
    by_id = {o["findingId"]: o for o in view["occurrences"]}
    facts, coverage, imports, limits = set(), set(), set(), []
    for fid in cand.get("findingIds", []):
        finding = by_id[fid]["finding"]
        for ref in finding["evidenceRefs"]:
            if ref["domain"] == "fact":
                facts.add("fact2:" + ref["digest"])
            elif ref["domain"] == "coverage":
                coverage.add("coverage2:" + ref["digest"])
            elif ref["domain"] == "import":
                imports.add("import2:" + ref["digest"])
        if finding["correspondence"]["state"] == "unmatched":
            limits.append("correspondence " + finding["correspondence"]["reason"] + ": " + fid)
    rr = next((r for r in view["ruleResults"] if r["ruleId"] == cand.get("ruleId")), None)
    if rr is not None and rr["enumeration"]["state"] != "complete":
        limits.append("enumeration incomplete for rule " + rr["ruleId"])

    def bounded(values, limit, label):
        ordered = sorted(values, key=lambda s: s.encode())
        if len(ordered) > limit:
            limits.append(label + " truncated at " + str(limit) + " of " + str(len(ordered)))
        return ordered[:limit]

    fact_list = bounded(facts, INSPECTION_FACT_LIMIT, "facts")
    coverage_list = bounded(coverage, INSPECTION_REF_LIMIT, "coverageIds")
    import_list = bounded(imports, INSPECTION_REF_LIMIT, "importIds")
    if len(limits) > INSPECTION_REF_LIMIT:
        limits = limits[: INSPECTION_REF_LIMIT - 1] + ["limitations truncated at " + str(INSPECTION_REF_LIMIT)]
    return {"candidateId": candidate_id, "runId": view["runId"], "facts": fact_list, "coverageIds": coverage_list,
            "importIds": import_list, "limitations": limits, "advisory": True}


def pivot_closure_availability(artifact, host):
    """baseline show: current-trust resolution of every pivot closure of an admitted baseline, in descriptor order.

    The same law as resolve_detectors' pivot state: missing record or bytes -> missing; trust not admitted -> revoked;
    protocol major not supported or platform neither the host platform nor any -> incompatible; otherwise available with
    its trust origin, which must be one of the three current-trust origins."""
    verify_baseline_artifact_v3(artifact)
    rows = []
    for pc in artifact["descriptor"]["pivotClosure"]:
        c = (host.get("closures") or {}).get(pc["closureId"])
        row = {"closureId": pc["closureId"], "kind": pc["kind"]}
        if c is None or c.get("bytes") == "missing":
            row["state"] = "missing"
        elif c.get("trust") != "admitted":
            row["state"] = "revoked"
        elif c.get("protocolMajor") not in (host.get("protocolMajors") or []) or c.get("platform") not in (host.get("platform"), "any"):
            row["state"] = "incompatible"
        else:
            if c.get("trustOrigin") not in TRUST_ORIGINS:
                raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "an available pivot closure requires a current-trust origin", pc["closureId"])
            row.update(state="available", trustOrigin=c["trustOrigin"])
        rows.append(row)
    return rows


def serialization_overflow_termination():'''

QS_GENERIC = r'''QUERY_STEP_PARAMS_REF = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/QueryParams"
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


def run_projection_controls(inventory):'''

rows.append(apply('R2 model projections and registry', WPM, [
    ('''        "policy-document.v2.schema.json",
        "test-execution.schema.json",
    ):
        path = HERE / "schemas" / name
        doc = json.loads(path.read_text())
        Draft202012Validator.check_schema(doc)
        docs[doc["$id"]] = doc
    _PROFILE_REG = Registry()''', '''        "policy-document.v2.schema.json",
        "test-execution.schema.json",
        "policy-test.schema.json",
    ):
        path = HERE / "schemas" / name
        doc = json.loads(path.read_text())
        Draft202012Validator.check_schema(doc)
        docs[doc["$id"]] = doc
    # recommend carries the native-owned UnitDiscoveryV2 by $ref; the native schema is loaded, never copied.
    native = json.loads((HERE.parent / "native" / "native-evidence.schemas.v2.json").read_text())
    Draft202012Validator.check_schema(native)
    docs[native["$id"]] = native
    _PROFILE_REG = Registry()'''),
    ('''def serialization_overflow_termination():''', MODEL_PROJECTIONS),
]))

rows.append(apply('R2 query surface generic carriers', QSP, [
    ('''QUERY_SURFACE_OTHER = "command-owned-summary"
''', '''QUERY_SURFACE_NON_GRAPH = ("discovery-recommendation", "baseline-inspection", "effective-policy", "policy-test-result",
                           "candidate-list", "candidate-inspection", "review-brief", "repair-preview")
'''),
    ('''def run_projection_controls(inventory):''', QS_GENERIC),
    ('''    other_with_response = copy.deepcopy(env_page)
    other_with_response["querySurface"] = QUERY_SURFACE_OTHER
    record("command-owned-summary-with-query-response-refused-by-schema", not schema_ok(ENVELOPE_REF, other_with_response))
    other_summary = copy.deepcopy(other_with_response)
    del other_summary["queryResponse"]
    record("command-owned-summary-without-query-response-admitted", schema_ok(ENVELOPE_REF, other_summary))
    try:
        project_query_surface(resp_page, success_term, envelope=other_summary, command=live)
        record("query-command-cannot-select-command-owned-summary", False)
    except QuerySurfaceProjectionError as exc:
        record("query-command-cannot-select-command-owned-summary", exc.code == "QUERY_SURFACE_ENVELOPE_SELECTOR", code=exc.code)''',
     '''    other_with_response = copy.deepcopy(env_page)
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
        record("query-command-cannot-select-a-non-graph-surface", exc.code == "QUERY_SURFACE_ENVELOPE_SELECTOR", code=exc.code)'''),
    ('''    surfaces = {c["name"]: (QUERY_SURFACE_GRAPH if "query-response" in c["parityFields"] else QUERY_SURFACE_OTHER) for c in inventory["commands"] if c["requestClass"] == "query"}
    record(
        "query-class-selector-join-only-query-command-carries-response",
        [n for n, s in surfaces.items() if s == QUERY_SURFACE_GRAPH] == ["query"] and len(surfaces) > 1,
        surfaces=surfaces,
    )''', '''    surfaces = {c["name"]: c.get("queryDispatch", {}).get("surface") for c in inventory["commands"] if c["requestClass"] == "query"}
    record(
        "query-class-selector-join-only-query-command-carries-response",
        [n for n, s in surfaces.items() if s == QUERY_SURFACE_GRAPH] == ["query"]
        and None not in surfaces.values() and len(set(surfaces.values())) == len(surfaces) == 9
        and set(surfaces.values()) == {QUERY_SURFACE_GRAPH, *QUERY_SURFACE_NON_GRAPH},
        surfaces=surfaces,
    )'''),
]))

rows.append(apply('R2 workflow checker schema loaders', CWP, [
    ('''    "test-execution.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        Draft202012Validator.check_schema(doc)
        SCHEMAS[doc["$id"]] = doc
''', '''    "test-execution.schema.json",
    "policy-test.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        Draft202012Validator.check_schema(doc)
        SCHEMAS[doc["$id"]] = doc
_native_schema = canonical.parse((HERE.parent / "native" / "native-evidence.schemas.v2.json").read_bytes())
Draft202012Validator.check_schema(_native_schema)
SCHEMAS[_native_schema["$id"]] = _native_schema
'''),
]))

rows.append(apply('R2 query checker loaders and generic graph parity', CQP, [
    ('''    "test-execution.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        SCHEMAS[doc["$id"]] = doc
''', '''    "test-execution.schema.json",
    "policy-test.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        SCHEMAS[doc["$id"]] = doc
_native_schema = canonical.parse((HERE.parent / "native" / "native-evidence.schemas.v2.json").read_bytes())
SCHEMAS[_native_schema["$id"]] = _native_schema
'''),
    ('''        check("m5-retained-run-query-response-is-the-owner-response", proj["parity"]["query-response"] == response and proj["parity"]["total-items"] == response["context"]["totalItems"])
''', '''        check("m5-retained-run-query-response-is-the-owner-response", proj["parity"]["query-response"] == response and proj["parity"]["total-items"] == response["context"]["totalItems"])
        pointer = QS.project_command_surface(env, command)
        check("r2-query-command-parity-paths-equal-owner-projection", pointer["parity"] == proj["parity"] and pointer["surface"] == "graph-query-response")
        generic = QS.render_command_formats(env, command, hints=["hint"])
        check("r2-query-command-generic-renderer-recovers-parity", generic["ok"] and generic["parityHolds"])
'''),
]))
print(json.dumps(rows, indent=1))
