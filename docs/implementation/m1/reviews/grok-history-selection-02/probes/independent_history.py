"""Independent HIS-F1–F6 probes against copy bytes. Not a restatement of check.py."""
from __future__ import annotations

import copy
import hashlib
import json
import types
from contextlib import contextmanager
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-grok-history-selection-review-02/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-history-selection-review-02/review/results")
FROZEN = Path("/tmp/opensip-implementation/m1-history-selection-subject-02")
JOINT10 = Path("/tmp/opensip-implementation/m1-grok-joint-review-10/review/copy/composed-sources")
ARCH_QUERY = Path(
    "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
)
ARCH_COMMON = Path(
    "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"
)
PARENT_QUERY_ID = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3"
PID = "prj1-" + "2" * 64


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def load(name, rel):
    p = COPY / rel
    m = types.ModuleType(name)
    m.__file__ = str(p)
    exec(compile(p.read_bytes(), str(p), "exec"), m.__dict__)
    return m


def rid(n):
    return "run3:" + format(n, "064x")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    rows = []
    H = load("history_reference", "history.py")
    Q = H.QUERY
    flags = json.loads((COPY / "history-command-flags.json").read_bytes())
    query_schema = json.loads((COPY / "graph-query.history-candidate.schema.json").read_bytes())
    parent_query = json.loads(ARCH_QUERY.read_bytes())
    parent_common = json.loads(ARCH_COMMON.read_bytes())
    common_cand = json.loads((COPY / "common.history-candidate.schema.json").read_bytes())
    explicit = json.loads((COPY / "explicit-history.schema.json").read_bytes())
    goldens = json.loads((COPY / "history-route-goldens.json").read_bytes())
    budget = json.loads((COPY / "budget-result.json").read_bytes())
    pins = json.loads((COPY / "input-pins.json").read_bytes())["files"]
    panel = json.loads((COPY / "explicit-history-panel.schema.json").read_bytes())
    report = json.loads(Path(next(p["path"] for p in pins if p["role"] == "report-schema")).read_bytes())
    identity = json.loads(Path(next(p["path"] for p in pins if p["role"] == "identity-schema")).read_bytes())
    invocation = json.loads(Path(next(p["path"] for p in pins if p["role"] == "invocation")).read_bytes())
    canonical_path = Path(next(p["path"] for p in pins if p["role"] == "canonical"))
    C = types.ModuleType("canonical_owner")
    exec(compile(canonical_path.read_bytes(), str(canonical_path), "exec"), C.__dict__)

    from jsonschema import Draft202012Validator, ValidationError, validators
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    validator_cls = validators.extend(
        Draft202012Validator,
        type_checker=Draft202012Validator.TYPE_CHECKER.redefine("integer", lambda _, v: type(v) is int),
    )

    def registry_for(*docs):
        return Registry().with_resources(
            (d["$id"], Resource(contents={k: v for k, v in d.items() if k != "$schema"}, specification=DRAFT202012))
            for d in docs
        )

    cand_reg = registry_for(query_schema, panel, report, explicit, common_cand, identity, invocation)
    parent_reg = registry_for(parent_query, parent_common, identity, invocation)

    def validate_query(v):
        validator_cls({"$ref": query_schema["$id"] + "#/$defs/GraphQueryResponseV1"}, registry=cand_reg).validate(v)

    def validate_parent_query(v):
        validator_cls({"$ref": parent_query["$id"] + "#/$defs/GraphQueryResponseV1"}, registry=parent_reg).validate(v)

    def validate_history(v):
        validator_cls({"$ref": panel["$id"] + "#/$defs/RetainedHistorySlotV1"}, registry=cand_reg).validate(v)

    def typed_value(value):
        if type(value) is not dict or value.get("state") not in ["present", "unavailable"]:
            return value
        value = copy.deepcopy(value)
        run_id = value.get("runId")
        if value["state"] == "unavailable":
            response = Q.unavailable(PID, run_id, value["availability"])
        else:
            result = {
                "kind": "analysis",
                "authority": "authoritative",
                "runId": run_id,
                "planId": "plan2:" + "3" * 64,
                "verdict": "pass",
                "requiredCoverage": "satisfied",
                "durability": "committed",
                "deficiency": "none",
                "secondaryDeficiencies": [],
            }
            sealed = {
                "schemaVersion": 3,
                "projectId": PID,
                "snapshotId": "snapshot2:" + "4" * 64,
                "planId": result["planId"],
                "evidenceId": "evidence3:" + "5" * 64,
                "evaluationSealId": "seal3:" + "6" * 64,
                "capabilityManifestId": "7" * 64,
            }
            response = {
                "schemaFamily": "opensip.product.query",
                "schemaMajor": 3,
                "operation": "run.show",
                "context": {
                    "projectId": PID,
                    "resolvedView": {"runId": run_id},
                    "coverage": "complete",
                    "availability": "retained",
                    "truncated": False,
                    "totalItems": 1,
                    "advisory": False,
                },
                "items": [{"projectId": PID, "runId": run_id, "sealedRun": sealed, "result": result}],
            }
            value.setdefault("run", copy.deepcopy(result))
            value.setdefault("commitSequence", None)
            value.setdefault("findings", [])
            value.setdefault(
                "findingsProjection",
                {"total": len(value["findings"]), "omitted": 0, "omissionCause": "none"},
            )
        return {"query": response, "history": value}

    rec(
        rows,
        "his-f6-eight-command-flags",
        len(flags["rows"]) == 8
        and [r["command"] for r in flags["rows"]]
        == ["default", "analyze", "fit", "audit", "candidates", "inspect", "review-brief", "repair-preview"]
        and all(r["appendFlag"]["flag"] == "--history-run" for r in flags["rows"])
        and all(r["appendFlag"] == flags["rows"][0]["appendFlag"] for r in flags["rows"])
        and "Repeatable 1..4" in flags["rows"][0]["appendFlag"]["join"]
        and "Requires --format html" in flags["rows"][0]["appendFlag"]["join"],
    )

    try:
        H.admit_request(["private-invalid"], "json")
        rec(rows, "his-f1-format-precedes-malformed-token", False)
    except H.HistoryRefusal as exc:
        rec(
            rows,
            "his-f1-format-precedes-malformed-token",
            exc.route
            == {
                "class": "request-rejected",
                "code": "REQUEST.UNKNOWN_OPTION",
                "exitCode": 2,
                "detail": "OUTPUT.FORMAT_NOT_APPLICABLE",
            }
            and "private-invalid" not in str(exc)
            and "private-invalid" not in json.dumps(exc.route),
            observed=exc.route,
        )

    try:
        H.admit_request([rid(i) for i in range(5)], "json")
        rec(rows, "his-f1-format-precedes-five-valid", False)
    except H.HistoryRefusal as exc:
        rec(
            rows,
            "his-f1-format-precedes-five-valid",
            exc.route["detail"] == "OUTPUT.FORMAT_NOT_APPLICABLE"
            and exc.route["code"] == "REQUEST.UNKNOWN_OPTION",
            observed=exc.route,
        )

    try:
        H.admit_request([rid(i) for i in range(5)], "html")
        rec(rows, "his-f1-five-ids-selection-limit", False)
    except H.HistoryRefusal as exc:
        rec(
            rows,
            "his-f1-five-ids-selection-limit",
            exc.route["detail"] == "EVALUATION.SELECTION_LIMIT"
            and exc.route["code"] == "REQUEST.UNSATISFIABLE",
            observed=exc.route,
        )

    try:
        H.admit_request([rid(1), rid(1)], "html")
        rec(rows, "his-f1-duplicate-history-selection-invalid", False)
    except H.HistoryRefusal as exc:
        rec(
            rows,
            "his-f1-duplicate-history-selection-invalid",
            exc.route["detail"] == "REPORT.HISTORY_SELECTION_INVALID",
            observed=exc.route,
        )

    mixed = [rid(i) for i in range(4)] + ["private-invalid"]
    try:
        H.admit_request(mixed, "html")
        rec(rows, "his-f1-lexical-before-count", False)
    except H.HistoryRefusal as exc:
        rec(
            rows,
            "his-f1-lexical-before-count",
            exc.route["detail"] == "REPORT.HISTORY_SELECTION_INVALID"
            and "private-invalid" not in str(exc)
            and "private-invalid" not in json.dumps(exc.route),
            observed=exc.route,
        )

    rec(
        rows,
        "his-f1-goldens-three-routes",
        {r["detail"] for r in goldens["cases"]}
        == {"OUTPUT.FORMAT_NOT_APPLICABLE", "EVALUATION.SELECTION_LIMIT", "REPORT.HISTORY_SELECTION_INVALID"}
        and goldens["precedence"]
        == ["command-known-option", "format-applicability", "lexical-shape-and-uniqueness", "selection-count"],
    )

    try:
        H.plan_selection(H.admit_request([rid(1)], "html"), "latest")
        rec(rows, "his-f2-malformed-current-is-source-refusal", False)
    except Exception as exc:
        rec(
            rows,
            "his-f2-malformed-current-is-source-refusal",
            type(exc) is H.HistorySourceRefusal and not isinstance(exc, H.HistoryRefusal),
            observed=type(exc).__name__,
        )

    selection = H.plan_selection(H.admit_request([rid(1), rid(2)], "html"), rid(1))
    rec(
        rows,
        "his-f3-current-run-slot-skips-lookup-source",
        selection["slots"][0]["source"] == "current-run" and selection["slots"][1]["source"] == "exact-retained-lookup",
    )

    live = {
        rid(1): {"state": "unavailable", "runId": rid(1), "availability": "expired"},
        rid(3): {"state": "present", "runId": rid(3), "findings": []},
    }
    events = ["primary-committed", "pivot-committed"]

    @contextmanager
    def acquire():
        events.append("acquire")
        snap = copy.deepcopy(live)
        try:
            yield snap
        finally:
            events.append("release")

    def typed_lookup(snap, run_id):
        events.append("lookup:" + run_id[-2:])
        live[rid(3)] = {"state": "unavailable", "runId": rid(3), "availability": "purged"}
        return typed_value(snap[run_id])

    request = H.admit_request([rid(1), rid(2), rid(3)], "html")
    sel, out_rows = H.resolve_in_snapshot(request, rid(2), PID, acquire, typed_lookup, validate_query, validate_history)
    rec(
        rows,
        "his-f3-one-snapshot-includes-own-pivot-current-skips-lookup",
        events == ["primary-committed", "pivot-committed", "acquire", "lookup:01", "lookup:03", "release"]
        and [r["state"] for r in out_rows] == ["unavailable", "current-run", "present"]
        and out_rows[2]["state"] == "present",
        observed=events,
    )

    rec(rows, "his-f4-unavailable-and-present-order-preserved", [r["runId"] for r in out_rows] == [rid(1), rid(2), rid(3)])

    other = typed_value({"state": "present", "runId": rid(1), "findings": []})
    other["query"]["items"][0]["projectId"] = "prj1-" + "f" * 64
    try:
        H.resolve_slots(
            H.plan_selection(H.admit_request([rid(1)], "html"), None),
            PID,
            lambda _: other,
            validate_query,
            validate_history,
        )
        rec(rows, "his-f4-other-project-present-refused", False)
    except H.HistorySourceRefusal:
        rec(rows, "his-f4-other-project-present-refused", True)

    ids = [rid(i) for i in range(4)]
    selections = [H.plan_selection(H.admit_request(ids, "html"), current) for current in [None, rid(99), *ids]]
    selection_max = max(selections, key=lambda v: len(C.canonical(v)))
    text = "\0" * 1024
    choices = []
    for availability, code in [
        ("expired", "evidence.expired"),
        ("purged", "evidence.purged"),
        ("corrupt", "evidence.corrupt"),
        ("unavailable", "QUERY.VIEW_UNKNOWN"),
    ]:
        row = {
            "state": "unavailable",
            "runId": ids[0],
            "availability": availability,
            "detail": {"code": code, "remedy": text, "subject": text},
        }
        validate_history(row)
        choices.append(row)
    worst = max(choices, key=lambda v: len(C.canonical(v)))
    max_rows = [{**copy.deepcopy(worst), "runId": r} for r in ids]
    minimal = [{"state": "unavailable", "runId": r, "availability": "unavailable"} for r in ids]
    whole = {
        "selection": selection_max,
        "runs": max_rows,
        "provenance": copy.deepcopy(panel["properties"]["provenance"]["const"]),
    }
    rec(
        rows,
        "his-f4-budget-bytes-match-documented",
        len(C.canonical(selection_max)) == 896
        and len(C.canonical(minimal)) == 533
        and len(C.canonical(worst)) == 12484
        and len(C.canonical(max_rows)) == 49941
        and len(C.canonical(whole)) == 51243
        and budget["selectionMaxBytes"] == 896
        and budget["wholeExplicitUnavailablePanelMaxBytes"] == 51243,
        observed={
            "selection": len(C.canonical(selection_max)),
            "minimal": len(C.canonical(minimal)),
            "worst": len(C.canonical(worst)),
            "four": len(C.canonical(max_rows)),
            "whole": len(C.canonical(whole)),
        },
    )

    pinned = copy.deepcopy(worst)
    pinned["detail"]["code"] = "evidence.pinned"
    try:
        validate_history(pinned)
        rec(rows, "his-f4-writer-purge-detail-refused", False)
    except ValidationError:
        rec(rows, "his-f4-writer-purge-detail-refused", True)

    untyped = {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "operation": "run.show",
        "context": {
            "projectId": PID,
            "resolvedView": {"runId": rid(1)},
            "coverage": "complete",
            "availability": "retained",
            "truncated": False,
            "totalItems": 1,
            "advisory": False,
        },
        "items": [{"unowned": "arbitrary run.show item"}],
    }
    try:
        validate_query(untyped)
        rec(rows, "his-f5-candidate-refuses-untyped-run-show-item", False)
    except ValidationError as exc:
        rec(rows, "his-f5-candidate-refuses-untyped-run-show-item", True, observed=type(exc).__name__)

    try:
        validate_parent_query(untyped)
        rec(rows, "his-f5-parent-still-accepts-untyped-run-show-item", True)
    except Exception as exc:
        rec(rows, "his-f5-parent-still-accepts-untyped-run-show-item", False, observed=type(exc).__name__)

    missing_items = copy.deepcopy(untyped)
    del missing_items["items"]
    try:
        validate_query(missing_items)
        rec(
            rows,
            "s1-retained-run-show-without-items-passes-schema",
            True,
            note="then-branch minItems applies only when items is present; producer still emits items; consumer KeyError is not typed admission",
        )
        missing_items_passes = True
    except ValidationError as exc:
        rec(rows, "s1-retained-run-show-without-items-passes-schema", False, observed=type(exc).__name__)
        missing_items_passes = False

    class Spy:
        EvidenceUnavailable = type("EvidenceUnavailable", (Exception,), {})
        CompleteReplayMismatch = type("CompleteReplayMismatch", (Exception,), {})

        class C:
            class AdmissionError(Exception):
                pass

        called = []

        @staticmethod
        def close_run(run, objects, blobs):
            Spy.called.append({"projectId": run.get("projectId"), "nObjects": len(objects), "nBlobs": len(blobs)})
            return rid(1)

    seal_id = "seal3:" + "6" * 64
    plan_id = "plan2:" + "3" * 64
    spy_run = {"schemaVersion": 3, "projectId": PID, "planId": plan_id, "evaluationSealId": seal_id}
    spy_objects = {seal_id: ["evaluation-seal", {"verdict": "pass"}]}
    spy_result = {"runId": rid(1), "planId": plan_id, "verdict": "pass"}
    spy_source = {
        "state": "retained",
        "run": spy_run,
        "objects": spy_objects,
        "blobs": {"b": b"x"},
        "result": spy_result,
    }
    recorded = []

    def record_validate(v):
        recorded.append(copy.deepcopy(v))

    Spy.called.clear()
    out = Q.run_show(PID, rid(1), spy_source, Spy, record_validate)
    rec(
        rows,
        "his-f5-run-show-invokes-close_run-before-retained-item",
        len(Spy.called) == 1
        and Spy.called[0]["nObjects"] == 1
        and Spy.called[0]["nBlobs"] == 1
        and out["context"]["availability"] == "retained"
        and len(out["items"]) == 1
        and out["items"][0]["runId"] == rid(1)
        and recorded[-1]["operation"] == "run.show",
        observed=Spy.called,
    )

    class Missing:
        EvidenceUnavailable = Spy.EvidenceUnavailable
        CompleteReplayMismatch = Spy.CompleteReplayMismatch
        C = Spy.C

        @staticmethod
        def close_run(*_a, **_k):
            raise Spy.EvidenceUnavailable()

    miss = Q.run_show(PID, rid(1), spy_source, Missing, validate_query)
    rec(
        rows,
        "his-f5-declared-missing-evidence-is-unavailable",
        miss["context"]["availability"] == "unavailable" and miss["items"] == [],
        observed=miss["context"]["availability"],
    )

    class Boom:
        EvidenceUnavailable = Spy.EvidenceUnavailable
        CompleteReplayMismatch = Spy.CompleteReplayMismatch
        C = Spy.C

        @staticmethod
        def close_run(*_a, **_k):
            raise RuntimeError("sentinel-host-fault")

    try:
        Q.run_show(PID, rid(1), spy_source, Boom, validate_query)
        rec(rows, "his-f5-unexpected-exception-not-downgraded", False)
    except RuntimeError as exc:
        rec(rows, "his-f5-unexpected-exception-not-downgraded", str(exc) == "sentinel-host-fault", observed=str(exc))

    rec(
        rows,
        "query-candidate-reuses-parent-id",
        query_schema["$id"] == parent_query["$id"] == PARENT_QUERY_ID
        and common_cand["$id"] == parent_common["$id"],
        note="unselected candidate document; not an in-place product overwrite",
    )

    rec(
        rows,
        "query-successor-adds-only-run-show-response",
        set(query_schema["$defs"]) - set(parent_query["$defs"]) == {"RunShowItemV1", "RunShowResponseV1"}
        and query_schema["$defs"]["Operation"] == parent_query["$defs"]["Operation"],
    )

    rec(
        rows,
        "common-candidate-appends-only-history-selection-invalid",
        set(common_cand["$defs"]["DomainDetailCode"]["enum"]) - set(parent_common["$defs"]["DomainDetailCode"]["enum"])
        == {"REPORT.HISTORY_SELECTION_INVALID"}
        and len(common_cand["$defs"]["DomainDetailCode"]["enum"])
        == len(parent_common["$defs"]["DomainDetailCode"]["enum"]) + 1,
    )

    freeze_hist = sha(FROZEN / "explicit-history.schema.json")
    freeze_panel = sha(FROZEN / "explicit-history-panel.schema.json")
    joint_hist = sha(JOINT10 / "explicit-history.schema.json") if (JOINT10 / "explicit-history.schema.json").is_file() else None
    joint_panel = (
        sha(JOINT10 / "explicit-history-panel.schema.json") if (JOINT10 / "explicit-history-panel.schema.json").is_file() else None
    )
    rec(
        rows,
        "joint10-explicit-history-byte-identical",
        freeze_hist == joint_hist == "3fc78bc593ae104f09f4448d9f372bd2ccf5e35d97f9c97b012139d005869a94",
        observed={"freeze": freeze_hist, "joint10": joint_hist},
    )
    rec(
        rows,
        "joint10-panel-not-identical-and-not-a-waiver",
        freeze_panel == "f96cba040d4c27ef7d2e06cb1548940dbebca9e6638b427efec16452c4469ba9"
        and joint_panel == "694bc4c2b653a63824d2795936fe266051b6d21c530d919d2c0313b236bd926e"
        and freeze_panel != joint_panel
        and (FROZEN / "explicit-history-panel.schema.json").stat().st_size
        == (JOINT10 / "explicit-history-panel.schema.json").stat().st_size
        == 4171,
        observed={"freeze": freeze_panel, "joint10": joint_panel},
    )

    rec(
        rows,
        "subject-run-extracted-and-current-run-mapping",
        (COPY / "subject_run.py").is_file()
        and H.current_run_from_envelope({"kind": "run", "run": {"authority": "authoritative", "runId": rid(1)}}, "analyze")
        == rid(1)
        and H.current_run_from_envelope({"kind": "run", "run": {"authority": "ephemeral", "runId": rid(1)}}, "analyze")
        is None
        and H.current_run_from_envelope({"kind": "query", "queryRecord": {"preview": {}}}, "repair-preview") is None
        and H.current_run_from_envelope({"kind": "failure"}, "audit") is None,
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok history-selection02 probes; synthetic; not store/CLI/browser",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "queryVersioningDecision": {
            "reuseParentUriAndMajor": True,
            "silentInPlaceProductTightening": False,
            "acceptableAsUnselectedCandidateDocument": True,
            "legacyUntypedCacheMustNotBeRelabeled": True,
            "hostMayReprojectFromExactRetainedRun": True,
            "distinctCandidateIdRequiredInThisFreeze": False,
            "rationale": "Same URI/major is the selected successor identity for graph-query:3 after source selection. The candidate filename is not product. Untyped cached items fail RunShowItemV1 and must not be relabeled. A host with retained Run/objects/blobs/receipt may emit a new typed response via close_run; it must not reanalyze the current checkout or substitute latest.",
        },
        "shouldFixObservations": {
            "s1RetainedRunShowWithoutItemsPassesSchema": missing_items_passes,
            "severity": "should-fix" if missing_items_passes else "none",
            "note": "RunShowResponseV1 then-branch constrains items only when present. Producer always emits one item. Consumer KeyError is not typed admission. Not a false-accept of an untyped payload.",
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-history.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
