"""Full-shape fixture probes for the narrow host ledger join, not host custody."""
import copy


def run(ref, registry, schema, inputs, join_module):
    fixtures = inputs["reportFixtures"]
    inventory = inputs["inventory"]
    golden = fixtures["deliveryGoldens"][24]
    analysis = copy.deepcopy(golden["envelope"]["run"])
    run_id = analysis["runId"]
    request_id = golden["envelope"]["requestId"]
    project_id = golden["envelope"]["projectId"]
    invocation_id = "urn:opensip:product-v1:workflows:evaluator3:invocation:3"
    rows = []

    def validate(value, schema_id):
        ref.validate({"$ref": schema_id}, value, registry)

    def spec(step_id, kind):
        params = {"kind": kind}
        if kind == "analysis":
            params.update(profile="default", role="primary", durability="authoritative", snapshotSource="live-worktree")
        elif kind == "render":
            params.update(format="json", destination="stdout", sourceSteps=list(range(step_id)), required=True)
        elif kind == "query":
            request = copy.deepcopy(golden["envelope"]["advisoryReport"]["request"])
            params.update(operation=request["operation"], completeness=request["completeness"],
                          page=request["page"], request=request)
        return {"stepId": step_id, "kind": kind, "requirement": "required", "dependsOn": list(range(step_id)),
                "dependencyGate": "terminal" if kind == "render" else "completed", "retryPolicy": "none", "params": params}

    def record(kinds, committed_count=0):
        steps = [spec(i, k) for i, k in enumerate(kinds)]
        results = []
        for i, kind in enumerate(kinds):
            completed = i < committed_count
            result = {"stepId": i, "outcome": "completed" if completed else "cancelled",
                      "attempts": [{"executionId": "exec1_" + format(i + 1, "032x"),
                                    "outcome": "completed" if completed else "cancelled"}],
                      "termination": {"class": "success"} if completed else {"class": "interrupted", "signal": "SIGINT"}}
            if completed:
                result["result"] = copy.deepcopy(analysis)
                if i:
                    result["result"]["runId"] = "run3:" + "b" * 64
            results.append(result)
        term = {"class": "interrupted", "signal": "SIGINT"}
        if committed_count:
            term["runId"] = results[committed_count - 1]["result"]["runId"]
        return {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3,
                "requestId": request_id, "projectId": project_id,
                "workflow": {"kind": "builtin", "name": "analyze"},
                "mode": {"interactive": False, "ci": True, "ephemeral": False},
                "orderedSteps": steps, "stepResults": results, "termination": term,
                "terminationEmitted": True,
                "cancellation": {"requested": True, "signal": "SIGINT", "phase": "before-settle"}}

    def envelope(rec):
        e = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "failure",
             "requestId": rec["requestId"], "projectId": rec["projectId"],
             "termination": copy.deepcopy(rec["termination"]), "exitCode": 130, "errors": []}
        if "runId" in rec["termination"]:
            del e["errors"]
            e["kind"] = "run"
            e["run"] = copy.deepcopy(next(r["result"] for r in reversed(rec["stepResults"])
                                         if r.get("result", {}).get("runId")))
        return e

    def probe(name, rec, env, expected=None, shapes=True):
        if shapes:
            validate(rec, invocation_id)
            validate(env, schema["$id"])
        got = None
        try:
            join_module.validate_interruption_join(rec, env)
        except join_module.JoinRefusal as error:
            got = str(error)
        assert got == expected, (name, got, expected)
        rows.append({"case": name, "result": got or "accepted", "bothShapesAdmitted": shapes})

    before = record(["analysis", "render"])
    after = record(["analysis", "render"], 1)
    for name, rec in [("pre-run", before), ("post-commit", after)]:
        for signal in ("SIGINT", "SIGTERM", "SIGHUP"):
            r = copy.deepcopy(rec)
            r["cancellation"]["signal"] = r["termination"]["signal"] = signal
            for step in r["stepResults"]:
                if step["outcome"] == "cancelled":
                    step["termination"]["signal"] = signal
            probe(name + "-" + signal, r, envelope(r))
    erased = envelope(before)
    probe("committed-run-erasure-valid-shapes", after, erased, "J-INTERRUPTION-AGGREGATE")
    invented = envelope(after)
    probe("invented-run-valid-shapes", before, invented, "J-INTERRUPTION-AGGREGATE")
    multiple = record(["analysis", "analysis", "render"], 2)
    # Multiple analysis steps belong to a profile, not the analyze builtin.
    multiple["workflow"] = {"kind": "profile", "contributionId": "org.example.workflow", "activationId": "review", "profileVersion": "1.0.0"}
    probe("last-committed-run", multiple, envelope(multiple))
    wrong = envelope(multiple)
    wrong["termination"]["runId"] = wrong["run"]["runId"] = run_id
    probe("earlier-run-instead-of-last", multiple, wrong, "J-INTERRUPTION-AGGREGATE")
    inv_env = envelope(multiple)
    inv_env.pop("run")
    inv_env["kind"] = "invocation"
    inv_env["invocation"] = copy.deepcopy(multiple)
    probe("profile-invocation-carrier-keeps-ledger", multiple, inv_env)
    inv_env["invocation"]["clientCorrelationId"] = "different"
    probe("invocation-carrier-ledger-mismatch", multiple, inv_env, "J-INTERRUPTION-INVOCATION-CARRIER")
    for key in ("requestId", "projectId", "clientCorrelationId"):
        changed = envelope(before)
        changed[key] = {"requestId": "req1_" + "b" * 32, "projectId": "prj1-" + "b" * 64,
                        "clientCorrelationId": "different"}[key]
        probe("mismatched-" + key, before, changed, "J-INTERRUPTION-CORRELATION")
    r = copy.deepcopy(before)
    r["clientCorrelationId"] = "same"
    e = envelope(r)
    e["clientCorrelationId"] = "same"
    probe("correlation-preserved", r, e)
    for field, val in [("phase", "after-settle"), ("requested", False)]:
        r = copy.deepcopy(before)
        r["cancellation"][field] = val
        probe("wrong-cancellation-" + field, r, envelope(r), "J-INTERRUPTION-PHASE")
    e = envelope(before)
    e["termination"]["signal"] = "SIGHUP"
    probe("signal-mismatch", before, e, "J-INTERRUPTION-AGGREGATE")
    e = envelope(after)
    e["run"]["planId"] = "plan2:" + "b" * 64
    probe("same-run-id-different-result", after, e, "J-INTERRUPTION-RUN-CARRIER")
    optional = copy.deepcopy(after)
    optional["workflow"] = {"kind": "profile", "contributionId": "org.example.workflow", "activationId": "review", "profileVersion": "1.0.0"}
    optional["orderedSteps"][0]["requirement"] = "optional"
    optional["orderedSteps"][1]["dependsOn"] = []
    optional["orderedSteps"][1]["params"]["sourceSteps"] = []
    probe("optional-committed-run-preserved", optional, envelope(optional))
    optional_erased = copy.deepcopy(optional)
    del optional_erased["termination"]["runId"]
    probe("optional-committed-run-erased-in-both-record-and-envelope", optional_erased,
          envelope(before), "J-INTERRUPTION-AGGREGATE")
    wrong_signal = copy.deepcopy(before)
    wrong_signal["stepResults"][0]["termination"]["signal"] = "SIGHUP"
    probe("cancelled-step-signal-disagrees", wrong_signal, envelope(wrong_signal), "J-INTERRUPTION-CANCELLED-STEP")
    wrong_kind = copy.deepcopy(after)
    wrong_kind["orderedSteps"][0] = spec(0, "query")
    probe("query-result-cannot-be-analysis", wrong_kind, envelope(wrong_kind), "J-INTERRUPTION-RESULT-KIND")
    fabricated = copy.deepcopy(fixtures["bases"]["candidates-run"]["envelope"])
    fabricated["schemaMajor"] = 6
    fabricated["requestId"] = before["requestId"]
    fabricated["termination"] = copy.deepcopy(before["termination"])
    fabricated["exitCode"] = 130
    probe("cancelled-query-cannot-have-completed-query-carrier", before, fabricated, "J-INTERRUPTION-RESULT-CARRIERS")
    invented_error = envelope(before)
    invented_error["errors"] = [{"code": "QUERY.VIEW_UNKNOWN", "remedy": "Invented: select a different Run."}]
    probe("unrelated-interruption-error-refused", before, invented_error, "J-INTERRUPTION-INVENTED-DETAIL")
    no_run_invocation = envelope(before)
    no_run_invocation.pop("errors")
    no_run_invocation["kind"] = "invocation"
    no_run_invocation["invocation"] = copy.deepcopy(before)
    probe("no-run-exact-invocation", before, no_run_invocation)
    no_run_invocation["invocation"]["clientCorrelationId"] = "different"
    probe("no-run-wrong-invocation", before, no_run_invocation, "J-INTERRUPTION-INVOCATION-CARRIER")
    mixed = envelope(after)
    mixed["query"] = copy.deepcopy(fixtures["bases"]["candidates-run"]["envelope"]["query"])
    probe("run-carrier-cannot-invent-query-summary", after, mixed, "J-INTERRUPTION-RESULT-CARRIERS")
    mixed = envelope(after)
    mixed["errors"] = copy.deepcopy(invented_error["errors"])
    probe("run-carrier-cannot-invent-interruption-detail", after, mixed, "J-INTERRUPTION-INVENTED-DETAIL")
    previous_failure = copy.deepcopy(before)
    previous_failure["stepResults"][0] = {"stepId": 0, "outcome": "rejected", "attempts": [],
        "termination": {"class": "request-rejected", "errorCode": "CONFIG.INVALID",
                        "domainDetail": {"code": "CONFIG.INVALID", "remedy": "Correct the invalid configuration."}}}
    genuine = envelope(previous_failure)
    genuine["errors"] = [copy.deepcopy(previous_failure["stepResults"][0]["termination"]["domainDetail"])]
    probe("recorded-earlier-error-retained", previous_failure, genuine)
    probe("earlier-error-cannot-be-emptied", previous_failure, envelope(previous_failure), "J-INTERRUPTION-INVENTED-DETAIL")
    changed_detail = copy.deepcopy(genuine)
    changed_detail["errors"][0]["remedy"] = "A different invented explanation."
    probe("earlier-error-remedy-cannot-change", previous_failure, changed_detail, "J-INTERRUPTION-INVENTED-DETAIL")
    repeated_detail = copy.deepcopy(genuine)
    repeated_detail["errors"] *= 2
    probe("earlier-error-cannot-duplicate", previous_failure, repeated_detail, "J-INTERRUPTION-INVENTED-DETAIL")
    omitted = copy.deepcopy(genuine)
    del omitted["errors"]
    probe("earlier-error-array-cannot-be-omitted", previous_failure, omitted,
          "J-INTERRUPTION-INVENTED-DETAIL", shapes=False)
    polluted = copy.deepcopy(genuine)
    polluted["findings"] = copy.deepcopy(fixtures["bases"]["default-run"]["envelope"].get("findings", []))
    probe("no-commit-failure-cannot-carry-findings", previous_failure, polluted,
          "J-INTERRUPTION-RESULT-CARRIERS")
    inv_error = copy.deepcopy(genuine)
    inv_error["kind"] = "invocation"
    inv_error["invocation"] = copy.deepcopy(previous_failure)
    probe("invocation-errors-exactly-recorded", previous_failure, inv_error)
    del inv_error["errors"]
    probe("invocation-errors-cannot-be-omitted", previous_failure, inv_error,
          "J-INTERRUPTION-INVENTED-DETAIL")
    no_error_run = envelope(after)
    no_error_run["errors"] = []
    probe("run-empty-error-array-forbidden", after, no_error_run,
          "J-INTERRUPTION-INVENTED-DETAIL", shapes=False)
    # Optional failures are still real ledger details even though they do not
    # gate the settled aggregate. Their provenance survives a later commit.
    run_with_error = copy.deepcopy(multiple)
    run_with_error["stepResults"][0] = copy.deepcopy(previous_failure["stepResults"][0])
    run_with_error["orderedSteps"][0]["requirement"] = "optional"
    run_with_error["orderedSteps"][1]["dependsOn"] = []
    run_with_error["orderedSteps"][2]["dependsOn"] = [1]
    run_with_error["orderedSteps"][2]["params"]["sourceSteps"] = [1]
    run_error_env = envelope(run_with_error)
    run_error_env["errors"] = copy.deepcopy(genuine["errors"])
    probe("run-retains-optional-step-error", run_with_error, run_error_env)
    del run_error_env["errors"]
    probe("run-cannot-omit-optional-step-error", run_with_error, run_error_env,
          "J-INTERRUPTION-INVENTED-DETAIL")
    # Query builtins consume existing Run views. Their exact inventory has no
    # analysis/verify step, so no Run was committed in this invocation.
    for name in ("candidates", "inspect", "review-brief"):
        command = next(c for c in inventory["commands"] if c["name"] == name)
        assert command["steps"] == ["query", "render"]
        r = record(command["steps"])
        r["workflow"]["name"] = name
        params = r["orderedSteps"][0]["params"]
        if name == "inspect":
            params["operation"] = params["request"]["operation"] = "inspection.show"
            params["request"]["params"] = {"candidateId": fixtures["bases"]["inspect-run"]["envelope"]["queryRecord"]["inspection"]["candidateId"]}
        elif name == "review-brief":
            r["orderedSteps"][0]["params"] = {"kind": "query", "operation": "review.produce-brief", "request": {
                "operation": "review.produce-brief", "view": {"runId": run_id},
                "producer": {"kind": "policy-rule", "id": "opensip.review.heuristic"}}}
        probe(name + "-selected-history-is-not-commit", r, envelope(r))
    # A completed query and required renderer settle to success. Cancelling
    # afterward cannot replace that settled record by the interruption form.
    r = record(["query", "render"])
    r["workflow"]["name"] = "candidates"
    r["cancellation"]["phase"] = "after-settle"
    r["termination"] = {"class": "success"}
    for i, result in enumerate(r["stepResults"]):
        result["outcome"] = "completed"
        result["attempts"][0]["outcome"] = "completed"
        result["termination"] = {"class": "success"}
        result["result"] = ({"kind": "query", "items": 1, "truncated": False, "completenessMet": True, "advisory": True}
                            if i == 0 else {"kind": "render", "format": "json", "rendererVersion": 1,
                                             "bytes": 100, "truncation": False, "written": True})
    e = copy.deepcopy(fixtures["bases"]["candidates-run"]["envelope"])
    e["schemaMajor"] = 6
    e["requestId"] = r["requestId"]
    probe("after-settle-keeps-query-success", r, e)
    probe("after-settle-cannot-reclassify", r, envelope(before), "J-INTERRUPTION-SETTLED")
    impossible = copy.deepcopy(before)
    impossible["stepResults"][1] = copy.deepcopy(r["stepResults"][1])
    probe("completion-after-cancelled-step", impossible, envelope(impossible), "J-INTERRUPTION-CANCELLED-PREFIX")
    for bad in [{}, None, [], {"requestId": request_id, "projectId": project_id}]:
        probe("malformed-reference-record-" + repr(bad), bad, envelope(before),
              "J-INTERRUPTION-INPUT", shapes=False)
    for signal in ("SIGINT", "SIGTERM", "SIGHUP"):
        context = {"stage": "before-planning", "requestId": request_id, "signal": signal}
        env = envelope(before)
        del env["projectId"]
        env["termination"]["signal"] = signal
        validate(env, schema["$id"])
        assert join_module.validate_preplanning_interruption(context, env)
        rows.append({"case": "preplanning-" + signal, "result": "accepted", "envelopeShapeAdmitted": True})
        changed = copy.deepcopy(env)
        changed["termination"]["signal"] = "SIGHUP" if signal != "SIGHUP" else "SIGINT"
        try:
            join_module.validate_preplanning_interruption(context, changed)
        except join_module.JoinRefusal as error:
            assert str(error) == "J-INTERRUPTION-PREPLANNING-CARRIER"
        else:
            raise AssertionError("preplanning signal mismatch")
        rows.append({"case": "preplanning-signal-mismatch-" + signal, "result": "J-INTERRUPTION-PREPLANNING-CARRIER"})
    # The added form forbids even otherwise valid extension payloads. Check
    # the payload independently before checking the combined negative.
    for field, value in [
        ("agentHints", ["inspect a retained Run"]),
        ("retentionDisclosure", {"policy": "durable-unbounded", "provenance": "DEFAULTED", "firstUse": True, "storageRoot": ".opensip"})
    ]:
        prop = schema["properties"][field]
        ref.validate(prop, value, registry)
        e = envelope(before)
        e[field] = value
        try:
            validate(e, schema["$id"])
        except Exception as error:
            if type(error).__name__ not in ("ValidationError", "AdmissionError"):
                raise
        else:
            raise AssertionError("new empty form admits " + field)
        rows.append({"case": "valid-payload-forbidden-" + field, "result": "shape-refused", "payloadShapeAdmitted": True})
    return rows
