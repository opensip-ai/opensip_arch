"""Reference-model corrections (M4 baseline detector identity, S7 presence knowledge, M5/A13 query carrier). Exact-once edits."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/tools')
from textedit import apply  # noqa: E402

WPM = 'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py'
QSP = 'docs/coop/design-corrections/workflows/query_surface_projection.v3.py'
rows = []

rows.append(apply('M4+S7 model', WPM, [
    # M4: baseline admission enforces the detector identity joins, including a self-consistently reminted rename.
    ('''    if not any(p["kind"] == "detector" for p in d["pivotClosure"]):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "pivotClosure must include the origin detector")
    return True
''', '''    if not any(p["kind"] == "detector" for p in d["pivotClosure"]):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "pivotClosure must include the origin detector")
    # Detector identity (workflows-and-surfaces §2): one detectorClosure row per emission contribution,
    # detectorId = contributionId, rule semanticsMajor, and entry detectorId = its rule's contribution.
    # Checked after baselineId recomputation, so a reminted rename is refused, not only a stale hash.
    detector_rows = d["detectorClosure"]
    detector_ids = [row["detectorId"] for row in detector_rows]
    for row in detector_rows:
        if row["detectorId"] != row["contributionId"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "detectorClosure detectorId must equal its emission contributionId", row["detectorId"])
    if len(set(detector_ids)) != len(detector_ids):
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "detectorClosure has exactly one row per contributionId", ",".join(sorted(detector_ids)))
    by_detector = {row["detectorId"]: row for row in detector_rows}
    rule_refs = {rule["ruleId"]: rule["ruleProgramRef"] for rule in docs["policy"]["rules"]}
    if {ref["contributionId"] for ref in rule_refs.values()} != set(detector_ids):
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "detectorClosure must be exactly the embedded policy rule contributions")
    for rule_id, ref in rule_refs.items():
        if by_detector[ref["contributionId"]]["semanticsMajor"] != ref["semanticsMajor"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "detectorClosure semanticsMajor disagrees with the rule contribution", rule_id)
    for entry in d["entries"]:
        ref = rule_refs.get(entry["ruleId"])
        if ref is None or entry["detectorId"] != ref["contributionId"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "BaselineEntry detectorId must be its rule contribution in detectorClosure", entry["fingerprint"])
    return True
'''),
    # S7: E4 knowledge in the unit/public comparison presence derivation.
    ('''def _derive_or_admit_presence(fps, b_entries, derived_e4, pivot, delta):
    """Unchanged policy/scope/waiver/detector axes copy E4. Do not invent measured absence.
''', '''def _derive_or_admit_presence(fps, b_entries, derived_e4, pivot, delta, absence_known=None):
    """Unchanged policy/scope/waiver/detector axes copy E4 knowledge, including null. Do not invent measured absence.

    E4 is True for a matched current occurrence, False only when absence_known(fp) proves absence under the
    pivot law, otherwise None: a missing matched hit is not by itself known absence.
'''),
    ('''        e4 = bool(derived_e4.get(fp, {}).get("E4"))
        waived_c = bool(derived_e4.get(fp, {}).get("waivedC", False))''', '''        if derived_e4.get(fp, {}).get("E4"):
            e4 = True
        elif absence_known is not None and absence_known(fp):
            e4 = False
        else:
            e4 = None
        waived_c = bool(derived_e4.get(fp, {}).get("waivedC", False))'''),
    ('''    fps = set(b_entries) | set(derived_e4) | set(pivot or {}) | set(extra_rules)
    presence = _derive_or_admit_presence(fps, b_entries, derived_e4, pivot, delta)''', '''    fps = set(b_entries) | set(derived_e4) | set(pivot or {}) | set(extra_rules)
    absence_known = current_absence_knowledge(current, b_entries, extra_rules)
    presence = _derive_or_admit_presence(fps, b_entries, derived_e4, pivot, delta, absence_known)'''),
    ('''        pres = dict(current["presence"][fp])
        pres["B"] = fp in b_entries''', '''        pres = dict(current["presence"][fp])
        pres["B"] = baseline_presence_knowledge(fp, rule_id, b_entries, b_rules)'''),
    ('''            profile,
            entry_unavail,
        )
        desc["entries"].append(entry)''', '''            profile,
            entry_unavail,
        )
        entry["liveInCurrent"] = bool(pres["E4"] is True and not pres.get("waivedC"))
        unknown_reason = first_attribution_unknown(pres)
        if unknown_reason and entry["classification"] != "INDETERMINATE":
            entry.pop("direction", None)
            entry.pop("gateReason", None)
            entry.update(classification="INDETERMINATE", indeterminateReason=unknown_reason, gates=False, subsequentDeltas=[])
            sig = "indeterminate" if comparison_rule_gating(b_rules.get(rule_id), c_rules.get(rule_id), profile) else None
        desc["entries"].append(entry)'''),
    ('''        elif gating_def:
            desc["remedy"] = {
                "code": "COMPARISON.REQUIRED_COVERAGE_UNSATISFIED",
                "remedy": "restore required coverage/evidence for " + ",".join(d["ruleId"] for d in gating_def),
            }
''', '''        elif gating_def:
            desc["remedy"] = {
                "code": "COMPARISON.REQUIRED_COVERAGE_UNSATISFIED",
                "remedy": "restore required coverage/evidence for " + ",".join(d["ruleId"] for d in gating_def),
            }
        elif any(e.get("indeterminateReason") in ("current-absence-unknown", "baseline-absence-unknown") for e in desc["entries"]):
            unknown_rules = sorted({e["ruleId"] for e in desc["entries"] if e.get("indeterminateReason") in ("current-absence-unknown", "baseline-absence-unknown")})
            desc["remedy"] = {
                "code": "COMPARISON.REQUIRED_COVERAGE_UNSATISFIED",
                "remedy": "absence is not established for " + ",".join(unknown_rules) + "; complete enumeration and determinate evaluation on the unknown side",
            }
'''),
    ('''def _rule_coverage_from_admitted(policy, rule_results):''', '''def _rule_coverage_from_admitted(policy, rule_results, view=None):'''),
    ('''                "gating": rule_gates(policy, rule["ruleId"]),
                "evidenceUse": copy.deepcopy(rule["evidenceUse"]),
            }''', '''                "gating": rule_gates(policy, rule["ruleId"]),
                "evidenceUse": copy.deepcopy(rule["evidenceUse"]),
                "absenceKnowledge": rule_absence_knowledge(view, rule["ruleId"]) if view is not None else "unknown",
            }'''),
    ('''    coverage = _rule_coverage_from_admitted(view["policy"], view["ruleResults"])''', '''    coverage = _rule_coverage_from_admitted(view["policy"], view["ruleResults"], view)'''),
    ('''        "boundPivots": [] if bound is None else bound,
        **({"pivotPresence": pivots} if pivots is not None else {}),''', '''        "predicateProofs": copy.deepcopy((view.get("proof") or {}).get("predicateProofs")),
        "absenceExtent": presence_absence_extent(view),
        "boundPivots": [] if bound is None else bound,
        **({"pivotPresence": pivots} if pivots is not None else {}),'''),
    ('''    prove = {rule["ruleId"]: rule_has_complete_hit_set(view, rule["ruleId"]) for rule in view["policy"]["rules"]}
    return {"hits": hits, "prove_absence": prove, "entry_rules": entry_rules}
''', '''    prove = {rule["ruleId"]: rule_has_complete_hit_set(view, rule["ruleId"]) for rule in view["policy"]["rules"]}
    return {"hits": hits, "prove_absence": prove, "entry_rules": entry_rules}


def rule_absence_knowledge(view, rule_id) -> str:
    """RuleCoverage.absenceKnowledge recorded at baseline adoption: the same complete-hit-set law as pivots."""
    return "complete-hit-set" if rule_has_complete_hit_set(view, rule_id) else "unknown"


def presence_absence_extent(view) -> dict:
    """Attested extent one admitted view contributes to the path absence law (pivot and current alike)."""
    return {
        "examinedPaths": sorted(extracted_source_paths(view)),
        "scopeDocument": copy.deepcopy(view.get("scopeDocument")),
        "foundationScope": foundation_scope_record(view),
        "extractionComplete": inventories_are_complete(view),
    }


def fingerprint_absence_known(knowledge_view, extent, rule_id, path) -> bool:
    """Known absence of one non-emitted fingerprint: the law _bind_pivot_runs/compare_admitted_v3 apply to pivots.

    Requires the owning rule's complete hit set (enabled, evaluated, complete enumeration, every selected root
    determinate, not budget-exhausted) and the path absence law over the attested extent. Missing admitted
    root predicate proofs or extent is unknown, never false.
    """
    if not rule_id or extent is None:
        return False
    try:
        complete = rule_has_complete_hit_set(knowledge_view, rule_id)
    except Refusal:
        return False
    if not complete:
        return False
    return path_absence_claim_allowed(
        path,
        examined=set(extent.get("examinedPaths") or []),
        scope_doc=extent.get("scopeDocument"),
        foundation_scope=extent.get("foundationScope"),
        extraction_complete=bool(extent.get("extractionComplete")),
    )


def current_absence_knowledge(current, b_entries, extra_rules):
    """E4 absence knowledge for compare_v3 from the admitted current projection only.

    Uses the admitted proof predicateProofs and absenceExtent the admitted-run adapter carries. A unit
    projection without them has no absence knowledge. Caller presence maps remain refused.
    """
    knowledge_view = {
        "policy": current["policy"],
        "evaluationState": current["evaluationState"],
        "ruleResults": current["ruleResults"],
        "proof": {"predicateProofs": current.get("predicateProofs")},
    }
    extent = current.get("absenceExtent")
    rules, paths = {}, {}
    for fp, entry in b_entries.items():
        rules[fp] = entry["ruleId"]
        paths[fp] = entry.get("subjectPath")
    for fp, pair in (extra_rules or {}).items():
        rules.setdefault(fp, pair[0])
    for occ in current["occurrences"]:
        finding = occ["finding"]
        if finding["fingerprint"]:
            rules[finding["fingerprint"]] = finding["ruleId"]
            paths[finding["fingerprint"]] = finding["subject"]["logicalPath"]
    return lambda fp: fingerprint_absence_known(knowledge_view, extent, rules.get(fp), paths.get(fp))


def baseline_presence_knowledge(fp, rule_id, b_entries, b_rules):
    """B: True for a baseline entry; False only under recorded complete-hit-set absence knowledge; else None."""
    if fp in b_entries:
        return True
    rule = b_rules.get(rule_id)
    return False if rule is not None and rule.get("absenceKnowledge") == "complete-hit-set" else None


def first_attribution_unknown(pres):
    """Reason when the first attributable change along B..E4 would rest on an unknown presence value."""
    chain = [pres["B"], pres["E0"] if pres["E0"] is not None else pres["E1"], pres["E1"], pres["E2"], pres["E3"], pres["E4"]]
    for i in range(5):
        if chain[i] is None or chain[i + 1] is None:
            return "baseline-absence-unknown" if pres["B"] is None else "current-absence-unknown"
        if chain[i] != chain[i + 1]:
            return None
    return None


def comparison_rule_gating(rule_b, rule_c, profile) -> bool:
    """classify()'s gating selection, reused for an entry reclassified as unknown."""
    gating_b = bool(rule_b and rule_b["enabled"] and rule_b["gating"])
    gating_c = bool(rule_c and rule_c["enabled"] and rule_c["gating"])
    return (gating_b or gating_c) if profile["gateRuleUnder"] == "baseline-or-current" else gating_c
'''),
    ('''    for fp in fps_union:
        measured = {}
        rule_id = None''', '''    current_extent = presence_absence_extent(view)
    for fp in fps_union:
        measured = {}
        rule_id = None'''),
    ('''        e4 = bool(e4_map.get(fp, {}).get("E4"))
        e0, e1, e2, e3 = _presence_from_equalities(e4, delta, measured)''', '''        if e4_map.get(fp, {}).get("E4"):
            e4 = True
        elif fingerprint_absence_known(view, current_extent, rule_id, path):
            e4 = False
        else:
            e4 = None
        e0, e1, e2, e3 = _presence_from_equalities(e4, delta, measured)'''),
]))

rows.append(apply('M5+A13 query surface', QSP, [
    ('''Pure helper: no semantic authority, no Run admission, no graph walk, no envelope
schema change. Callers must supply an already owner-admitted GraphQueryResponseV1
and the enclosing actual StepTermination / CommandEnvelope.''', '''Pure helper: no semantic authority, no Run admission, no graph walk. The public
carrier is CommandEnvelope major 3 kind=query with querySurface=graph-query-response
and the complete owner-admitted GraphQueryResponseV1 in queryResponse. Callers supply
that response and the enclosing actual StepTermination / CommandEnvelope.'''),
    ('''QUERY_RESULT_REF = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/QueryResult"
''', '''QUERY_RESULT_REF = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/QueryResult"
QUERY_SURFACE_GRAPH = "graph-query-response"
QUERY_SURFACE_OTHER = "command-owned-summary"
'''),
    ('''def delivery_required_termination(enclosing=None):
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
    return t''', '''def delivery_required_termination(enclosing=None, *, committed=None):
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
    return t'''),
    ('''        expected_exit = Wlegacy.EXIT[termination["class"]]
        if envelope.get("exitCode") != expected_exit:
            raise QuerySurfaceProjectionError(
                "QUERY_SURFACE_EXIT_JOIN",
                str(envelope.get("exitCode")) + "!=" + str(expected_exit),
            )''', '''        expected_exit = Wlegacy.EXIT[termination["class"]]
        if envelope.get("exitCode") != expected_exit:
            raise QuerySurfaceProjectionError(
                "QUERY_SURFACE_EXIT_JOIN",
                str(envelope.get("exitCode")) + "!=" + str(expected_exit),
            )
        if envelope.get("querySurface") != QUERY_SURFACE_GRAPH:
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_SELECTOR", str(envelope.get("querySurface")))
        if not _equal(envelope.get("queryResponse"), response):
            raise QuerySurfaceProjectionError("QUERY_SURFACE_ENVELOPE_RESPONSE_MISMATCH")'''),
    ('''def render_query_formats(parity, envelope, command, hints=None):
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
    }''', '''def _parity_from_rendering(rendering, command):
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
            body = "".join(k + ": " + canonical.canonical(parity[k]).decode() + "\\n" for k in fields)
        renderings.append({"format": fmt, "body": body})
    recovered = [_parity_from_rendering(r, command) for r in renderings]
    holds = all(_equal({k: p.get(k) for k in fields}, {k: owner[k] for k in fields}) for p in recovered)
    return {"ok": True, "deliveryTermination": None, "renderings": renderings, "parityHolds": holds}'''),
    ('''    def envelope_for(summary, term, extra_query=None):
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
        return env''', '''    def envelope_for(summary, term, response, extra_query=None):
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
        return env'''),
    ('''    env_page = envelope_for(summary_page, success_term)''', '''    env_page = envelope_for(summary_page, success_term, resp_page)'''),
    ('''        env_lb = envelope_for(summary_lb, success_term)''', '''        env_lb = envelope_for(summary_lb, success_term, resp_lb)'''),
    ('''        env_empty = envelope_for(summary_empty, success_term)''', '''        env_empty = envelope_for(summary_empty, success_term, resp_empty)'''),
    ('''    env17 = envelope_for(other17_summary, success_term)''', '''    env17 = envelope_for(other17_summary, success_term, resp17)'''),
    ('''        env_mut = envelope_for(graph_query_result_summary(mutated), success_term)''', '''        env_mut = envelope_for(graph_query_result_summary(mutated), success_term, mutated)'''),
    ('''        {"kind": "query", "items": 2, "truncated": False, "completenessMet": True, "advisory": False, "nextCursor": cursor},
        other_failed_term,
    )''', '''        {"kind": "query", "items": 2, "truncated": False, "completenessMet": True, "advisory": False, "nextCursor": cursor},
        other_failed_term,
        resp_term,
    )'''),
    ('''        env_agree = envelope_for(graph_query_result_summary(resp_agree), success_term)''', '''        env_agree = envelope_for(graph_query_result_summary(resp_agree), success_term, resp_agree)'''),
    ('''    return {
        "standing": "projection controls over schema-admitted owned-response shapes; not Run admission; not traversal evidence",''', '''    # --- public carrier: CommandEnvelope major 3 queryResponse selected by querySurface ---
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
    other_with_response["querySurface"] = QUERY_SURFACE_OTHER
    record("command-owned-summary-with-query-response-refused-by-schema", not schema_ok(ENVELOPE_REF, other_with_response))
    other_summary = copy.deepcopy(other_with_response)
    del other_summary["queryResponse"]
    record("command-owned-summary-without-query-response-admitted", schema_ok(ENVELOPE_REF, other_summary))
    try:
        project_query_surface(resp_page, success_term, envelope=other_summary, command=live)
        record("query-command-cannot-select-command-owned-summary", False)
    except QuerySurfaceProjectionError as exc:
        record("query-command-cannot-select-command-owned-summary", exc.code == "QUERY_SURFACE_ENVELOPE_SELECTOR", code=exc.code)
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
    surfaces = {c["name"]: (QUERY_SURFACE_GRAPH if "query-response" in c["parityFields"] else QUERY_SURFACE_OTHER) for c in inventory["commands"] if c["requestClass"] == "query"}
    record(
        "query-class-selector-join-only-query-command-carries-response",
        [n for n, s in surfaces.items() if s == QUERY_SURFACE_GRAPH] == ["query"] and len(surfaces) > 1,
        surfaces=surfaces,
    )

    return {
        "standing": "projection controls over schema-admitted owned-response shapes; not Run admission; not traversal evidence",'''),
]))
print(json.dumps(rows, indent=1))
