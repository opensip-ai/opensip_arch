"""J-INTERRUPTION-LEDGER reference join, after existing owner admission.

This does not replace invocation schema, DAG, step-result, D9, Run admission or
host custody. It takes the admitted host record and an independently shape-
admitted envelope. It mutates neither. Local labels are not public detail codes.
"""
import re


class JoinRefusal(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise JoinRefusal(code)


def validate_interruption_join(record, envelope):
    try:
        return _validate_interruption_join(record, envelope)
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise JoinRefusal("J-INTERRUPTION-INPUT") from error


def _validate_interruption_join(record, envelope):
    require(isinstance(record, dict) and isinstance(envelope, dict)
            and {"requestId", "orderedSteps", "stepResults", "termination"} <= set(record)
            and {"requestId", "termination", "kind", "exitCode"} <= set(envelope), "J-INTERRUPTION-INPUT")
    for field in ("requestId", "clientCorrelationId", "projectId"):
        require((field in record) == (field in envelope)
                and record.get(field) == envelope.get(field), "J-INTERRUPTION-CORRELATION")
    steps = record["orderedSteps"]
    results = record.get("stepResults", [])
    # The caller has already admitted the immutable step/result binding. Check
    # it again here rather than allowing zip() to silently drop missing rows.
    require([s["stepId"] for s in steps] == list(range(len(steps))), "J-INTERRUPTION-STEPS")
    require([r["stepId"] for r in results] == list(range(len(steps))), "J-INTERRUPTION-STEPS")
    required = [(s, r) for s, r in zip(steps, results) if s["requirement"] == "required"]
    settled = all(r["outcome"] in ("completed", "rejected", "failed", "skipped", "abandoned")
                  for _, r in required)
    cancellation = record.get("cancellation", {})
    requested = cancellation.get("requested") is True
    phase = cancellation.get("phase", "none")
    require(phase == ("after-settle" if settled else "before-settle") if requested
            else phase == "none", "J-INTERRUPTION-PHASE")
    cancelled_seen = False
    kinds = {"analysis", "verify", "comparison", "query", "render", "import", "repair-preview",
             "repair-apply", "test-execution", "mutation", "export-delivery", "doctor", "native-preparation"}
    for spec, result in zip(steps, results):
        require(spec["kind"] in kinds, "J-INTERRUPTION-RESULT-KIND")
        if "result" in result:
            expected_kind = spec["kind"]
            require(result["result"]["kind"] == expected_kind, "J-INTERRUPTION-RESULT-KIND")
        require(result["outcome"] != "completed" or "result" in result, "J-INTERRUPTION-RESULT-KIND")
        if result["outcome"] == "cancelled":
            cancelled_seen = True
            require(requested and result["termination"] == {"class": "interrupted", "signal": cancellation["signal"]}
                    and "result" not in result, "J-INTERRUPTION-CANCELLED-STEP")
        else:
            require(not cancelled_seen, "J-INTERRUPTION-CANCELLED-PREFIX")
            require(result["termination"]["class"] != "interrupted", "J-INTERRUPTION-CANCELLED-STEP")
    if requested and not settled:
        result_fields = {"run", "invocation", "query", "querySurface", "queryResponse", "queryRecord", "mutation", "doctor", "meta"}
        expected_fields = {envelope["kind"]} if envelope["kind"] in ("run", "invocation") else set()
        require(set(envelope) & result_fields == expected_fields, "J-INTERRUPTION-RESULT-CARRIERS")
        # One deterministic error projection for every interrupted carrier.
        # Include optional-step failures, exclude skipped/cancelled steps. The
        # host records a composed detail when each failed/rejected step is
        # recorded, not only later when interruption happens.
        earlier_details = [r["termination"]["domainDetail"] for r in results
                           if r["outcome"] not in ("cancelled", "skipped")
                           and r["termination"]["class"] in ("request-rejected", "operational-failed")
                           and "domainDetail" in r["termination"]]
        if earlier_details or envelope["kind"] == "failure":
            require("errors" in envelope and envelope["errors"] == earlier_details,
                    "J-INTERRUPTION-INVENTED-DETAIL")
        else:
            # The existing schema admits empty errors only on the selected
            # failure branches. Keep run/invocation absence deterministic.
            require("errors" not in envelope, "J-INTERRUPTION-INVENTED-DETAIL")
        signal = cancellation["signal"]
        require(signal in ("SIGINT", "SIGTERM", "SIGHUP"), "J-INTERRUPTION-SIGNAL")
        expected = {"class": "interrupted", "signal": signal}
        # Explicit successor of the owner's cancellation-only required filter:
        # preserve every earlier committed analysis/verify Run, including an
        # optional step. Requirement still controls settled D9 aggregation.
        committed = [r["result"]["runId"] for r in results
                     if r["outcome"] == "completed" and r.get("result", {}).get("runId")]
        if committed:
            expected["runId"] = committed[-1]
        require(record.get("termination") == expected, "J-INTERRUPTION-AGGREGATE")
        require(envelope["termination"] == expected and envelope["exitCode"] == 130,
                "J-INTERRUPTION-AGGREGATE")
        if committed:
            require(envelope["kind"] in ("run", "invocation"), "J-INTERRUPTION-RUN-CARRIER")
            if envelope["kind"] == "run":
                require(envelope["run"].get("runId") == committed[-1], "J-INTERRUPTION-RUN-CARRIER")
                actual = next(r["result"] for r in reversed(results)
                              if r["outcome"] == "completed" and r.get("result", {}).get("runId"))
                require(envelope["run"] == actual, "J-INTERRUPTION-RUN-CARRIER")
            else:
                require(envelope["invocation"] == record, "J-INTERRUPTION-INVOCATION-CARRIER")
        else:
            # The current aggregate is interruption, which has no detail code.
            # Earlier real failures remain in stepResults. This successor
            # selects a failure with exactly its recorded earlier error
            # details (empty only when none exist), or an exact invocation;
            # no cancelled query/doctor completion is manufactured.
            require(envelope["kind"] in ("failure", "invocation"), "J-INTERRUPTION-NO-RUN-CARRIER")
            if envelope["kind"] == "failure":
                require("errors" in envelope, "J-INTERRUPTION-INVENTED-DETAIL")
            else:
                require(envelope["invocation"] == record, "J-INTERRUPTION-INVOCATION-CARRIER")
            require(not ({"findings", "advisoryReport", "availability"} & set(envelope)),
                    "J-INTERRUPTION-RESULT-CARRIERS")
            require("runId" not in envelope["termination"] and "run" not in envelope,
                    "J-INTERRUPTION-RUN-CARRIER")
    else:
        # Existing aggregate admission supplies the settled non-interrupted
        # termination. This join prevents the emitter reclassifying it.
        require(record.get("termination", {}).get("class") != "interrupted"
                and envelope["termination"] == record["termination"], "J-INTERRUPTION-SETTLED")
    return True


def validate_preplanning_interruption(context, envelope):
    """Trusted host request observation before an invocation is admitted.

    This context is private host state, not a request or serialized authority.
    Actual RequestContext custody and lifecycle implementation remain required.
    """
    try:
        required = {"stage", "requestId", "signal"}
        optional = {"projectId", "clientCorrelationId"}
        require(isinstance(context, dict) and required <= set(context) <= required | optional,
                "J-INTERRUPTION-CONTEXT")
        require(context["stage"] == "before-planning", "J-INTERRUPTION-CONTEXT")
        require(isinstance(context["requestId"], str)
                and re.fullmatch(r"req1_[0-9a-f]{32}", context["requestId"]) is not None,
                "J-INTERRUPTION-CONTEXT")
        require(context["signal"] in ("SIGINT", "SIGTERM", "SIGHUP"), "J-INTERRUPTION-SIGNAL")
        for field in ("requestId", "projectId", "clientCorrelationId"):
            require((field in context) == (field in envelope)
                    and context.get(field) == envelope.get(field), "J-INTERRUPTION-CORRELATION")
        require(envelope["kind"] == "failure" and envelope.get("errors") == []
                and envelope["exitCode"] == 130
                and envelope["termination"] == {"class": "interrupted", "signal": context["signal"]},
                "J-INTERRUPTION-PREPLANNING-CARRIER")
        return True
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise JoinRefusal("J-INTERRUPTION-INPUT") from error
