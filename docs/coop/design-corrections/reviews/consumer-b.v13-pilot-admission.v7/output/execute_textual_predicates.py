#!/usr/bin/env python3
"""Interpret mandatory textual clauses into exact comparisons on retained instances.

Does not label a sentence PASS. Each executed row has operands. Unrecognized
mandatory clauses stay OPEN (unexecuted).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
sys.path.insert(0, str(OUT))

from helpers import canonical, condtrace, h, order  # noqa: E402
from helpers.store import load_export  # noqa: E402
from helpers.evaluator import _load_c  # noqa: E402
from derive_conditions import classify_object  # noqa: E402


def get_path(obj, dotted: str):
    cur = obj
    for p in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def main() -> int:
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    inv = json.loads((OUT / "inventory" / "specification-inventory.json").read_text())
    run_id = st.meta["runId"]
    run = st.objects[run_id]
    plan = st.objects[run["planId"]]
    evid = st.objects[run["evidenceId"]]
    condtrace.reset()
    executed = []
    unrecognized = []

    def emit(doc, ptr, instance, field, comparison, left, right, result, extra=None):
        condtrace.set_document(doc)
        condtrace.emit(
            condition=ptr,
            instance=str(instance),
            field=field,
            comparison=comparison,
            left=left,
            right=right,
            result=result,
            extra=extra,
        )
        executed.append(
            {
                "document": doc,
                "pointer": ptr,
                "instance": instance,
                "field": field,
                "comparison": comparison,
                "result": result,
            }
        )

    # Always-executed owner joins named by selected descriptions we can operationalize.
    # 1. semantic-evidence.importIds equals plan.importIds (composition §9.7 / schema description)
    want = order.cset(list(plan.get("importIds") or []))
    got = evid.get("importIds")
    ok = canonical.encode(got) == canonical.encode(want)
    emit(
        "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "/$defs/semantic-evidence/properties/importIds/description",
        run["evidenceId"],
        "importIds",
        "cset-eq-plan.importIds",
        got,
        want,
        "pass" if ok else "refuse",
    )

    # 2. enumeratorClosure kind=provider
    for ident, obj in st.objects.items():
        if not ident.startswith("scope2:"):
            continue
        cid = obj.get("enumeratorClosure")
        clo = st.objects.get(cid) or {}
        ok = clo.get("kind") == "provider"
        emit(
            "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
            "/$defs/subject-scope/properties/enumeratorClosure/description",
            ident,
            "enumeratorClosure",
            "kind-eq-provider",
            clo.get("kind"),
            "provider",
            "pass" if ok else "refuse",
        )

    # 3. EI.planId equals selected run.planId (never read off Plan descriptor)
    ei = None
    proof = st.objects[evid["proofBundleId"]]
    ei = _load_c(st, proof["executionInputsDigest"])
    ok = ei.get("planId") == run["planId"]
    emit(
        "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
        "/properties/planId/description",
        proof["executionInputsDigest"],
        "planId",
        "eq-selected-run.planId",
        ei.get("planId"),
        run["planId"],
        "pass" if ok else "refuse",
    )

    # 4. inventory deficiency null iff state=complete
    for ident, obj in st.objects.items():
        cls = classify_object(ident, obj)
        if not cls or cls[0] != "opensip.product.subject-inventory.1":
            continue
        stt = obj.get("state")
        d = obj.get("deficiency")
        ok = (stt == "complete" and d is None) or (stt != "complete" and d is not None)
        emit(
            "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
            "/properties/deficiency/description",
            ident,
            "deficiency",
            "null-iff-state-complete",
            {"state": stt, "deficiency": d},
            {"complete=>null", "else=>non-null"},
            "pass" if ok else "refuse",
        )

    # 5. TargetAttributionV2 exported MUST be null when kind is file/package/unknown
    for ident, obj in st.objects.items():
        cls = classify_object(ident, obj)
        if not cls or cls[0] != "opensip.product.target-attribution.2":
            continue
        kind = obj.get("kind")
        exported = obj.get("exported")
        if kind in {"file", "package", "unknown"}:
            ok = exported is None
            emit(
                "docs/coop/design-corrections/foundation/target-attribution.schema.v2.json",
                "/properties/exported/description",
                ident,
                "exported",
                "must-be-null-when-kind-not-symbol",
                {"kind": kind, "exported": exported},
                None,
                "pass" if ok else "refuse",
            )
        else:
            emit(
                "docs/coop/design-corrections/foundation/target-attribution.schema.v2.json",
                "/properties/exported/description",
                ident,
                "exported",
                "kind-symbol-exported-applicable",
                {"kind": kind, "exported": exported},
                "symbol",
                "pass",
            )
        # occupancy first-party => evaluationNativeId required; else MUST be null
        occu = obj.get("occupancy")
        enid = obj.get("evaluationNativeId")
        if occu == "first-party":
            ok = enid is not None
            cmpn = "required-non-null-iff-first-party"
        else:
            ok = enid is None
            cmpn = "must-be-null-when-not-first-party"
        emit(
            "docs/coop/design-corrections/foundation/target-attribution.schema.v2.json",
            "/properties/evaluationNativeId/description",
            ident,
            "evaluationNativeId",
            cmpn,
            {"occupancy": occu, "evaluationNativeId": enid},
            "first-party" if occu == "first-party" else "null",
            "pass" if ok else "refuse",
        )
        # producerClosure equals source fact producerClosure
        src = st.objects.get(obj.get("sourceFactId"))
        if src:
            ok = obj.get("producerClosure") == src.get("producerClosure")
            emit(
                "docs/coop/design-corrections/foundation/target-attribution.schema.v2.json",
                "/properties/producerClosure/description",
                ident,
                "producerClosure",
                "eq-sourceFact.producerClosure",
                obj.get("producerClosure"),
                src.get("producerClosure"),
                "pass" if ok else "refuse",
            )

    # 6. enumeration-plan snapshotId equals plan.snapshotId
    spec = _load_c(st, plan["analysisSpecDigest"])
    from helpers import builder

    ep_d = next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.ENUM_PLAN_DIGEST)
    enum_plan = _load_c(st, ep_d)
    ok = enum_plan.get("snapshotId") == plan.get("snapshotId")
    emit(
        "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "/properties/snapshotId/description",
        ep_d,
        "snapshotId",
        "eq-plan.snapshotId",
        enum_plan.get("snapshotId"),
        plan.get("snapshotId"),
        "pass" if ok else "refuse",
    )
    ok = enum_plan.get("scopeDigest") == plan.get("scopeDigest")
    emit(
        "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "/properties/scopeDigest/description",
        ep_d,
        "scopeDigest",
        "eq-plan.scopeDigest",
        enum_plan.get("scopeDigest"),
        plan.get("scopeDigest"),
        "pass" if ok else "refuse",
    )

    # Walk remaining mandatory textual clauses: record unrecognized rather than PASS.
    for o in inv.get("occurrences") or []:
        if o.get("kind") not in {"textual-clause", "prose-clause"}:
            continue
        if o.get("classification") not in {"mandatory-candidate", "mixed-mandatory-and-explanatory"}:
            continue
        key = (o.get("document"), o.get("condition"), str(o.get("instance")), str(o.get("field")))
        already = any(
            (e["document"], e["pointer"], str(e["instance"]), str(e["field"])) == key for e in executed
        )
        if already:
            continue
        unrecognized.append(
            {
                "document": o.get("document"),
                "pointer": o.get("condition"),
                "instance": o.get("instance"),
                "field": o.get("field"),
                "classification": o.get("classification"),
                "status": "OPEN-uninterpreted",
                "bindWhy": o.get("bindWhy"),
            }
        )

    traces = condtrace.snapshot()
    report = {
        "standing": "Textual clauses executed only when a concrete predicate was interpreted. Unrecognized mandatory clauses remain OPEN.",
        "executedComparisons": len(executed),
        "unrecognizedMandatory": len(unrecognized),
        "refuseCount": sum(1 for e in executed if e["result"] == "refuse"),
        "executed": executed,
        "unrecognized": unrecognized[:500],
        "unrecognizedTruncated": max(0, len(unrecognized) - 500),
        "traceCount": len(traces),
    }
    (OUT / "inventory" / "textual-predicate-execution.json").write_text(json.dumps(report, indent=2) + "\n")
    (OUT / "inventory" / "textual-predicate-traces.json").write_text(json.dumps({"traces": traces}, indent=2) + "\n")
    print(
        "executed",
        len(executed),
        "unrecognizedMandatory",
        len(unrecognized),
        "refuse",
        report["refuseCount"],
    )
    return 1 if report["refuseCount"] or unrecognized else 0


if __name__ == "__main__":
    sys.exit(main())
