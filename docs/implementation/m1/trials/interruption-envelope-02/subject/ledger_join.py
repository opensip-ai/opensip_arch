"""J-INTERRUPTION-LEDGER reference join, after existing owner admission.

This does not replace invocation schema, DAG, step-result, D9, Run admission or
host custody. It takes the admitted host record and an independently shape-
admitted envelope. It mutates neither. Local labels are not public detail codes.
"""


class JoinRefusal(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise JoinRefusal(code)


def validate_interruption_join(record, envelope):
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
    if requested and not settled:
        signal = cancellation["signal"]
        require(signal in ("SIGINT", "SIGTERM", "SIGHUP"), "J-INTERRUPTION-SIGNAL")
        expected = {"class": "interrupted", "signal": signal}
        # Exactly the pinned owner model's required/completed result order.
        # Existing result admission guarantees that only analysis/verify can
        # carry an authoritative AnalysisResult with runId.
        committed = [r["result"]["runId"] for _, r in required
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
                actual = next(r["result"] for _, r in reversed(required)
                              if r["outcome"] == "completed" and r.get("result", {}).get("runId"))
                require(envelope["run"] == actual, "J-INTERRUPTION-RUN-CARRIER")
            else:
                require(envelope["invocation"] == record, "J-INTERRUPTION-INVOCATION-CARRIER")
        else:
            # This unit owns only the added failure alternative; an existing
            # invocation/doctor result carrier stays with its existing owner.
            # Existing nonempty-error forms may retain real earlier details;
            # their detail-to-observation join stays with the existing owner.
            require("runId" not in envelope["termination"] and "run" not in envelope,
                    "J-INTERRUPTION-RUN-CARRIER")
    else:
        # Existing aggregate admission supplies the settled non-interrupted
        # termination. This join prevents the emitter reclassifying it.
        require(record.get("termination", {}).get("class") != "interrupted"
                and envelope["termination"] == record["termination"], "J-INTERRUPTION-SETTLED")
    return True
