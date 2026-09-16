"""Independent report-projection08 probes. Q-FIT-1 is a required original-freeze defect."""
from __future__ import annotations

import copy
import hashlib
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-report-projection08-reproduction/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-root-report-projection08-reproduction/results")
FROZEN = Path("/tmp/opensip-implementation/m1-report-projection-subject-08")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
FIT01 = Path("/tmp/opensip-implementation/m1-fit-interruption-subject-01")
L02SEL = Path("/tmp/opensip-implementation/m1-report-joint-candidate-12/L02-policy-selection.json")
ENV5_ID = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:5"
ENV6_ID = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:6"


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(name, path):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(Path(path).read_bytes(), str(path), "exec"), m.__dict__)
    return m


def main():
    rows = []
    M = load("report08", COPY / "report_model.py")
    fixtures = json.loads((COPY / "fixtures.json").read_bytes())
    inventory = json.loads((COPY / "owner/command-inventory.v5.json").read_bytes())
    command = next(r for r in inventory["commands"] if r["name"] == "fit")
    golden = next(g for g in fixtures["interruptionGoldens"]["scenarios"] if g["id"] == "fit/primary/signal-before-required-render")

    try:
        M.static_parity_text(golden["envelope"], command, M.document_disclosures({}))
        rec(rows, "rf1-interrupted-fit-completed-query-static-parity-keyerror", False)
    except KeyError as exc:
        rec(
            rows,
            "rf1-interrupted-fit-completed-query-static-parity-keyerror",
            exc.args[0] == "advisoryReport"
            and golden["envelope"]["kind"] == "run"
            and "advisoryReport" not in golden["envelope"]
            and [r["outcome"] for s, r in zip(golden["invocationRecord"]["orderedSteps"], golden["invocationRecord"]["stepResults"]) if s["kind"] == "query"]
            == ["completed"],
            observed=str(exc.args[0]),
        )

    req = golden["invocationRecord"]["orderedSteps"][1]["params"]["request"]
    rec(
        rows,
        "rf1-placeholder-request-not-committed-run",
        req["view"]["runId"] != golden["envelope"]["run"]["runId"] and req["projectId"] != golden["envelope"]["projectId"],
        observed={"planned": req["view"]["runId"][:18], "committed": golden["envelope"]["run"]["runId"][:18]},
    )

    scenarios = fixtures["interruptionGoldens"]["scenarios"]
    rec(
        rows,
        "declared-144-renderer-rows-are-format-counts",
        len(scenarios) == 36
        and all(g["formats"] == ["human", "json", "agent", "html"] for g in scenarios)
        and sum(len(g["formats"]) for g in scenarios) == 144
        and "static_parity_text" not in Path(COPY / "check.py").read_text().split("def interruption_controls")[1].split("def capacity_regression")[0],
        observed={"scenarios": len(scenarios), "formatRows": 144},
    )

    fit_rows = []
    for g in scenarios:
        if g["command"] != "fit":
            continue
        try:
            raw = M.static_parity_text(g["envelope"], command, M.document_disclosures({})).encode()
            fit_rows.append({"id": g["id"], "kind": g["envelope"]["kind"], "state": "rendered", "bytes": len(raw)})
        except KeyError as exc:
            fit_rows.append({"id": g["id"], "kind": g["envelope"]["kind"], "state": "KeyError", "missing": exc.args[0]})
    rec(
        rows,
        "only-completed-query-fit-run-crashes-static-parity",
        fit_rows
        == [
            {"id": "fit/primary/signal-before-first-step", "kind": "failure", "state": "rendered", "bytes": 527},
            {"id": "fit/primary/signal-before-required-render", "kind": "run", "state": "KeyError", "missing": "advisoryReport"},
            {"id": "fit/primary/first-step-rejected-signal-before-required-render", "kind": "failure", "state": "rendered", "bytes": 804},
        ],
        observed=fit_rows,
    )

    env5 = json.loads((COPY / "owner/command-envelope.v5.schema.json").read_bytes())
    env6 = json.loads(
        (ARCH / "docs/implementation/m1/trials/interruption-envelope-07/subject/command-envelope.v6.schema.json").read_bytes()
    )
    suc6 = json.loads((ARCH / "docs/implementation/m1/trials/interruption-envelope-07/subject/successor.json").read_bytes())
    delta6 = suc6["delta"][0]
    index6 = int(delta6["selector"].split("/")[2])
    restored = copy.deepcopy(env6)
    for key in ("$id", "title", "description"):
        restored[key] = env5[key]
    restored["properties"]["schemaMajor"]["const"] = 5
    restored["allOf"][index6]["then"] = delta6["before"]
    rec(
        rows,
        "envelope6-restores-exactly-to-unaccepted-envelope5",
        restored == env5
        and env5["$id"] == ENV5_ID
        and env6["$id"] == ENV6_ID
        and sha(COPY / "owner/command-envelope.v5.schema.json") == "45de2b0a12fc2f1f41f3a4f50b22b5e177fad58b19e5cc5072ff808c737e789d",
        observed={"deltaSelector": delta6["selector"]},
    )

    skipped = {"kind": "verify", "requirement": "optional", "recorded": True, "outcome": "skipped",
               "termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
                               "domainDetail": {"code": "skip.fabricated", "remedy": "x"}}}
    cancelled = {"kind": "render", "requirement": "required", "recorded": True, "outcome": "cancelled",
                 "termination": {"class": "interrupted", "signal": "SIGINT",
                                 "domainDetail": {"code": "cancel.fabricated", "remedy": "x"}}}
    real = {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "failed",
            "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
                            "domainDetail": {"code": "evidence.missing", "remedy": "restore"}}}
    rec(
        rows,
        "recorded-failure-details-exclude-skipped-and-cancelled",
        M.recorded_failure_details([skipped, cancelled, real]) == [real["termination"]["domainDetail"]],
    )

    binding = json.loads((COPY / "owner/interruption-binding.v1.json").read_bytes())
    rec(
        rows,
        "interruption07-conditional-does-not-accept-envelope5-parent",
        binding["unit"]["status"] == "ACCEPTED-DESIGN-CORRECTION-CONDITIONAL-PARENT"
        and binding["unit"]["integrationApproved"] is False
        and json.loads((COPY / "successor.json").read_bytes())["envelopeParentDependency"]["envelope5"]["bytesUnchangedFromSubject04"] is True,
    )

    rec(
        rows,
        "later-fit-interruption01-correction-not-in-this-freeze",
        not (COPY / "fit_output.py").exists()
        and not (COPY / "fit-query-unavailable.schema.json").exists()
        and FIT01.is_dir()
        and "unavailable-query-result" not in (COPY / "report_model.py").read_text()
        and "FitQueryFromAnalysisParams" not in (COPY / "report-projection.schema.json").read_text(),
    )

    sel = json.loads(L02SEL.read_bytes())
    obl = json.loads((COPY / "owner/design-obligations.v1.json").read_bytes())
    l02 = next(x for x in obl["integrationObligations"] if x["id"] == "RP-OBL-L02")
    rec(
        rows,
        "this-freeze-l02-still-open-later-selection-is-not-this-unit",
        l02["status"] == "open-owner-decision"
        and l02["blocksM1FinalIntegration"] is True
        and sel["oldCriterionSuperseded"] is True
        and sel["sourcePromoted"] is False
        and "OUTPUT.SERIALIZATION_FAILED" not in (COPY / "report_model.py").read_text(),
        observed={"freeze": l02["status"], "later": sel["status"]},
    )

    k01 = next(x for x in obl["integrationObligations"] if x["id"] == "RP-OBL-K01")
    rec(
        rows,
        "k01-closed-by-accepted-coverage-prerequisite-unit",
        k01["status"] == "closed-by-accepted-unit"
        and k01["acceptedUnit"]["subjectManifestSha256"] == "480350895e0943c26db10eb6fd5277709733a169510a7c6f7cfdd2a421bf7ff9",
    )

    later_history = Path("/tmp/opensip-implementation/m1-history-selection-subject-02/history.py")
    later_catalog = Path("/tmp/opensip-implementation/m1-presentation-catalog-subject-02")
    rec(
        rows,
        "later-feature-owners-not-adopted-in-this-freeze",
        later_history.is_file()
        and later_catalog.is_dir()
        and "explicit-run-ids.1" not in (COPY / "report_model.py").read_text()
        and "presentation-catalog" not in (COPY / "report-projection.schema.json").read_text()
        and json.loads((COPY / "successor.json").read_bytes())["ownerSuccessorProposals"]["otherReportFeatureOwners"].startswith("unchanged"),
    )

    blockers = json.loads((COPY / "owner/design-obligations.v1.json").read_bytes())["readiness"]["blockers"]
    rec(rows, "eleven-feature-blockers-remain-open", blockers == ["RP-DO-01", "RP-DO-03", "RP-DO-04", "RP-DO-05", "RP-DO-06", "RP-DO-07", "RP-DO-08", "RP-DO-09", "RP-DO-10", "RP-DO-11", "RP-DO-12"])

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok report-projection08 original-unit probes; later successors distinguished; not product",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "requiredDefect": {
            "id": "Q-FIT-1",
            "inThisFreeze": True,
            "laterCorrectionUnit": "m1-fit-interruption-subject-01",
            "laterCorrectionAdoptedHere": False,
            "waived": False,
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-report08.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
