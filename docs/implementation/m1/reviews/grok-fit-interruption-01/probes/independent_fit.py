"""Independent Q-FIT-1 fit-interruption01 probes. Not a restatement of check.py."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-grok-fit-interruption-review-01/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-fit-interruption-review-01/review/results")


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def load(name, path, raw=None):
    path = Path(path)
    raw = path.read_bytes() if raw is None else raw
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), m.__dict__)
    return m


def main():
    rows = []
    pins = json.loads((COPY / "input-pins.json").read_bytes())["files"]
    sources = {}
    for row in pins:
        raw = Path(row["path"]).read_bytes()
        assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"]
        sources[row["role"]] = (row["path"], raw)

    F = load("fit_proposal", COPY / "fit_output.py")
    M = load("report08", sources["report-model"][0], sources["report-model"][1])
    C = load("canonical", sources["canonical"][0], sources["canonical"][1])
    query_tree = ast.parse(sources["query-projection"][1])
    names = {"QuerySurfaceProjectionError", "_equal", "_join", "_summary", "command_surface_summary"}
    query_nodes = [n for n in query_tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    Q = {"canonical": C}
    exec(compile(ast.Module(body=query_nodes, type_ignores=[]), sources["query-projection"][0], "exec"), Q)
    fixture = json.loads(sources["report-fixtures"][1])
    golden = next(r for r in fixture["interruptionGoldens"]["scenarios"] if r["id"] == "fit/primary/signal-before-required-render")
    COMMAND = next(r for r in json.loads(sources["inventory"][1])["commands"] if r["name"] == "fit")
    PAGE = fixture["bases"]["fit-sealed"]["envelope"]["advisoryReport"]
    PARAM_SCHEMA = json.loads((COPY / "fit-query-from-analysis.schema.json").read_bytes())
    ABSENT_SCHEMA = json.loads((COPY / "fit-query-unavailable.schema.json").read_bytes())
    from jsonschema import Draft202012Validator, ValidationError

    rec(
        rows,
        "original-golden-static-parity-keyerror-advisoryReport",
        True,
    )
    try:
        M.static_parity_text(golden["envelope"], COMMAND, M.document_disclosures({}))
        rows[-1]["passed"] = False
        print("FAIL original-golden-static-parity-keyerror-advisoryReport")
    except KeyError as exc:
        rec(rows, "original-golden-static-parity-keyerror-advisoryReport", "advisoryReport" in str(exc), observed=str(exc))
        # replace the placeholder True row
        rows.pop(-2)

    request = golden["invocationRecord"]["orderedSteps"][1]["params"]["request"]
    rec(
        rows,
        "original-placeholder-run-and-project-do-not-equal-committed",
        request["view"]["runId"] != golden["envelope"]["run"]["runId"]
        and request["projectId"] != golden["envelope"]["projectId"]
        and "advisoryReport" not in golden["envelope"],
        observed={
            "plannedRun": request["view"]["runId"][:20],
            "committedRun": golden["envelope"]["run"]["runId"][:20],
        },
    )

    qstep = golden["invocationRecord"]["orderedSteps"][1]
    rec(
        rows,
        "golden-already-has-completed-source-dependency",
        qstep["dependsOn"] == [0]
        and qstep["dependencyGate"] == "completed"
        and golden["invocationRecord"]["orderedSteps"][0]["kind"] == "analysis"
        and qstep["kind"] == "query",
        observed={"dependsOn": qstep["dependsOn"], "gate": qstep["dependencyGate"]},
    )

    record = copy.deepcopy(golden["invocationRecord"])
    record["orderedSteps"][1]["params"] = {"kind": "query", "operation": "candidate.list", "sourceStep": 0}
    env = copy.deepcopy(golden["envelope"])
    before = copy.deepcopy(record)
    resolved = F.resolved_request(record)
    rec(
        rows,
        "sourceStep-binds-committed-run-project-without-plan-mutation",
        resolved == PAGE["request"]
        and resolved["view"]["runId"] == env["run"]["runId"]
        and resolved["projectId"] == env["projectId"]
        and record == before
        and "request" not in record["orderedSteps"][1]["params"],
    )

    def admit_page(report, project_id, run_id):
        if set(report) != {"state", "request", "candidateList", "parity"}:
            raise F.BindingRefusal("page-fields")
        page = report["candidateList"]
        ctx = page["context"]
        if ctx["resolvedView"] != {"runId": run_id}:
            raise F.BindingRefusal("page-run")
        summary = Q["command_surface_summary"]("candidate-list", page, {"projectId": project_id})
        listed = len(page["candidates"])
        if listed > 100 or ctx["truncated"] != (ctx["totalItems"] > listed):
            raise F.BindingRefusal("page-size")
        if ctx["truncated"]:
            if listed != 100 or ctx.get("nextCursor") != M.fit_cursor(project_id, run_id, 100):
                raise F.BindingRefusal("page-cursor")
        elif "nextCursor" in ctx:
            raise F.BindingRefusal("unexpected-cursor")
        parity = {
            "runId": run_id,
            "candidates": page["candidates"],
            "evidenceLevels": page["evidenceLevels"],
            "candidatesTruncated": ctx["truncated"],
            "candidatesTotalItems": ctx["totalItems"],
            "candidatesNextCursor": ctx.get("nextCursor"),
            "candidatesAvailability": "sealed-run-first-page",
        }
        if not C.equal_typed(parity, report["parity"]):
            raise F.BindingRefusal("page-parity")
        return summary

    handle = F.capture_completed(record, PAGE, admit_page, C.equal_typed)
    rec(
        rows,
        "private-handle-is-dictionary-stand-in-with-exact-joins",
        set(handle) == {"requestId", "stepId", "executionId", "report"}
        and handle["requestId"] == record["requestId"]
        and handle["stepId"] == qstep["stepId"]
        and handle["executionId"] == record["stepResults"][1]["attempts"][-1]["executionId"]
        and handle["report"] == PAGE,
        observed={"keys": sorted(handle)},
    )

    out = F.project_interrupted(record, env, handle, admit_page, C.equal_typed)
    text = M.static_parity_text(out, COMMAND, M.document_disclosures({}))
    rec(
        rows,
        "completed-page-copied-into-interrupted-envelope-and-renders",
        out["advisoryReport"] == PAGE
        and out["run"] == env["run"]
        and out["termination"]["class"] == "interrupted"
        and 'candidates-availability: "sealed-run-first-page"\n' in text
        and "advisoryReport" not in env,
    )

    try:
        F.project_interrupted(record, env, None, admit_page, C.equal_typed)
        rec(rows, "lost-completed-response-is-projection-fault-not-cancelled", False)
    except F.RequiredProjectionFailure as exc:
        rec(
            rows,
            "lost-completed-response-is-projection-fault-not-cancelled",
            "not-retained" in str(exc)
            and record["stepResults"][1]["outcome"] == "completed"
            and env["termination"]["class"] == "interrupted",
            observed=str(exc),
        )

    cancelled = copy.deepcopy(record)
    leftover = cancelled["stepResults"][1]["result"]
    cancelled["stepResults"][1]["outcome"] = "cancelled"
    # Independent: leftover completed summary must not become a sealed page.
    cancelled["stepResults"][1]["result"] = leftover
    absent = F.project_interrupted(cancelled, env, None, admit_page, C.equal_typed)["advisoryReport"]
    rec(
        rows,
        "cancelled-with-leftover-summary-is-unavailable-not-sealed-page",
        absent["state"] == "unavailable-query-result"
        and absent["queryOutcome"] == "cancelled"
        and absent["parity"]["candidates"] is None
        and absent["parity"]["runId"] == env["run"]["runId"],
        observed=absent["state"],
    )

    failed = copy.deepcopy(record)
    failed["stepResults"][1]["outcome"] = "failed"
    failed["stepResults"][1].pop("result")
    fail_rep = F.project_interrupted(failed, env, None, admit_page, C.equal_typed)["advisoryReport"]
    rec(
        rows,
        "failed-query-outcome-not-relabeled-cancelled",
        fail_rep["queryOutcome"] == "failed" and fail_rep["state"] == "unavailable-query-result",
        observed=fail_rep["queryOutcome"],
    )
    Draft202012Validator(ABSENT_SCHEMA).validate(fail_rep)
    empty = copy.deepcopy(fail_rep)
    empty["parity"]["candidates"] = []
    try:
        Draft202012Validator(ABSENT_SCHEMA).validate(empty)
        rec(rows, "empty-list-is-not-unavailable-absence", False)
    except ValidationError:
        rec(rows, "empty-list-is-not-unavailable-absence", True)

    eph = copy.deepcopy(record)
    eph["stepResults"][0]["result"] = {"kind": "analysis", "authority": "ephemeral"}
    rec(rows, "ephemeral-analysis-has-no-public-query-request", F.resolved_request(eph) is None)
    try:
        F.project_interrupted(eph, env, None, admit_page, C.equal_typed)
        rec(rows, "ephemeral-cannot-fill-authoritative-run-envelope", False)
    except F.BindingRefusal as exc:
        rec(rows, "ephemeral-cannot-fill-authoritative-run-envelope", "same-producing-run" in str(exc), observed=str(exc))

    float_ok_schema = True
    try:
        Draft202012Validator(PARAM_SCHEMA).validate(
            {"kind": "query", "operation": "candidate.list", "sourceStep": 0.0}
        )
    except ValidationError:
        float_ok_schema = False
    float_refused_binding = False
    bad = copy.deepcopy(record)
    bad["orderedSteps"][1]["params"]["sourceStep"] = 0.0
    try:
        F.resolved_request(bad)
    except F.BindingRefusal:
        float_refused_binding = True
    rec(
        rows,
        "s1-schema-accepts-float-sourceStep-binding-refuses",
        float_ok_schema and float_refused_binding,
        note="jsonschema default integer accepts 0.0; query_parts requires type is int",
        observed={"schemaAcceptsFloat": float_ok_schema, "bindingRefuses": float_refused_binding},
    )

    goldens = fixture["interruptionGoldens"]["scenarios"]
    fit_rows = [g for g in goldens if g["command"] == "fit"]
    rec(
        rows,
        "thirty-six-interruption-goldens-and-fit-failure-carriers-unchanged",
        len(goldens) == 36
        and any(g["id"] == "fit/primary/signal-before-required-render" for g in fit_rows)
        and all(g["envelope"]["kind"] == "failure" or g["id"] == "fit/primary/signal-before-required-render" for g in fit_rows),
        observed={"n": len(goldens), "fit": [g["id"] + ":" + g["envelope"]["kind"] for g in fit_rows]},
    )

    prior = json.loads((COPY / "prior/mutants01/mutant-results.json").read_bytes())
    rec(
        rows,
        "prior-broad-mutants-classified-consequent-errors-not-kills",
        prior["caught"] == 9
        and prior["total"] == 11
        and {r["id"] for r in prior["rows"] if not r["caught"]} == {"resolved-project-is-placeholder", "completed-report-dropped"}
        and "ERROR:" in next(r["stderr"] for r in prior["rows"] if r["id"] == "resolved-project-is-placeholder"),
        observed={"caught": prior["caught"], "missed": [r["id"] for r in prior["rows"] if not r["caught"]]},
    )

    report08 = sources["report-model"][1].decode() if False else Path(sources["report-model"][0]).read_text()
    # Q-FIT-1 remains open in pinned report08 contract, not this freeze
    r08_contract = Path("/tmp/opensip-implementation/m1-report-projection-subject-08/contract.md").read_text()
    rec(
        rows,
        "q-fit-1-still-open-in-parent-report08",
        "open joint-review question Q-FIT-1" in r08_contract
        and "This is not a completed Q-FIT-1 correction" in (COPY / "contract.md").read_text(),
    )

    joint = json.loads(Path("/tmp/opensip-implementation/m1-grok-joint-review-10/review/copy/joint-obligations.json").read_bytes())
    qfit = next(x for x in joint["jointAdditionalFindings"] if x["id"] == "Q-FIT-1")
    rec(
        rows,
        "joint10-does-not-close-q-fit-1",
        qfit["status"] == "reference-composed-review-pending",
        observed=qfit["status"],
    )

    l02 = Path("/tmp/opensip-implementation/m1-report-joint-candidate-12/L02-policy-selection.md").read_text()
    rec(
        rows,
        "l02-selection-does-not-excuse-missing-advisory-member",
        "complete-output-or-explicit-operational-failure" in l02
        and "Do not catch KeyError" in (COPY / "contract.md").read_text()
        and "L02" in Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/audits/fit-interruption-parity-01/issue.md").read_text(),
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok fit-interruption01 probes; dictionary custody; not full invocation/native/browser",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "adequacy": {
            "narrowBindingProjectionLawsAdequateToIntegrate": True,
            "qFit1Closed": False,
            "reason": "sourceStep planning, completed-source dispatch, private handle joins, lost-handle projection fault, and unavailable-query-result with actual outcome are sufficient proposed laws. Parent schema/builder/fixture/renderer succession and real host custody remain. Do not mark Q-FIT-1 closed.",
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-fit.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
