"""Source39 run-termination owner (foundation/run-termination-contract.v1.md) over actually closed Runs.

For every claimed complete positive (runs/from-scratch.summary.json) and the admitted work-budget mutation, the Run is closed by
ref/closure.close_run (complete replay) and the analysis projection is derived by ref/run_termination.py. Then:
  * D9 golden analysis-budget-exhausted is compared with the work-budget Run's derived termination (s4);
  * s6 candidate refusals (wrong order, omitted carrier, wrong runId, faultCause, blessing member, unvalidated delegated member);
  * s7 host composition admitted/refused cases with synthetic trusted attempts and receipts bound to each Run's execution plan;
  * discovery-order independence (the population fed in reversed order derives one projection).
Host observations are explicit inputs, never read from the Run. Writes vectors/run-termination.json.
Usage: python3 tools/seq.py <label> tools/run_termination_vectors.py
"""
import copy
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import closure as CL  # noqa: E402
import run_termination as RT  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
import phase7_vectors as P7  # noqa: E402

KIT = schemas.kit()
failures = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def closed(name):
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    rep = CL.close_run(store, exported["runId"])
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    published = ([row["id"] for row in exported["objectTable"]], list(exported["blobs"]))
    return {"name": name, "runId": exported["runId"], "store": store, "g": g, "closure": rep["result"], "published": published}


def observation(r, n, **patch):
    stages = r["store"].get_object(r["g"]["seal"]["executionPlanId"])["stages"]
    attempt = {"executionId": P7.exec_id(n), "outcome": "completed",
               "derivation": {"planId": r["g"]["plan_id"], "executionPlanId": r["g"]["seal"]["executionPlanId"], "stageCount": len(stages),
                              "stagesCompleted": len(stages)}}
    receipt = {"schemaVersion": 2, "runId": r["runId"], "executionId": attempt["executionId"], "namespaceId": "cb24-synthetic-namespace",
               "commitSequence": 1, "inventoryDigest": RT.commit_inventory(r["runId"], *r["published"])[1], "sealedAssurance": "replayable",
               "signerKeyId": "cb24-synthetic-signer"}
    obs = {"attempts": [attempt], "durability": "authoritative", "receipt": receipt, "requiredClosureNotInstalled": False}
    for k, v in patch.items():
        obs[k] = v
    return obs


def main():
    summary = json.load(open(f"{OUT}/runs/from-scratch.summary.json"))
    names = [row["run"] for row in summary["runs"] if row["role"] == "claimed-positive"] + ["syntax-code~budget-exhausted"]
    runs, projections = {}, []
    for name in names:
        r = closed(name)
        must(f"closed:{name}", r["closure"] == "ADMIT", r["closure"])
        runs[name] = r
        try:
            d = RT.derive(r["g"], r["store"], r["runId"])
            row = {"run": name, "verdict": r["g"]["proof"]["verdict"], "projection": d["projection"], "deficiency": d["deficiency"],
                   "secondaryDeficiencies": d["secondaryDeficiencies"], "populationCauses": sorted({x["cause"] for x in d["population"]}),
                   "conditions": [{k: c[k] for k in ("kind", "cause", "rank", "d9", "declared", "stage")} for c in d["conditions"]],
                   "projectionSchemaValid": RT.step_termination_shape_ok(d["projection"])}
            must(f"projection-schema:{name}", row["projectionSchemaValid"], d["projection"])
            reordered = RT.derive(r["g"], r["store"], r["runId"], records=list(reversed(d["population"]))) if d["population"] else d
            row["discoveryOrderIndependent"] = reordered["projection"] == d["projection"]
            must(f"order-independent:{name}", row["discoveryOrderIndependent"])
            r["derived"] = d
        except RT.TerminationRefusal as exc:
            row = {"run": name, "verdict": r["g"]["proof"]["verdict"], "refusal": exc.key, "detail": exc.detail}
            must(f"derivable:{name}", False, exc.key)
        projections.append(row)

    # ---- D9 golden: the work budget is the only cause
    goldens = {x["id"]: x for x in KIT.doc("coop/artifacts/d9-exit-contract.v1.14.json")["goldenCases"] if isinstance(x, dict) and "id" in x}
    gold = goldens["analysis-budget-exhausted"]
    budget = runs["syntax-code~budget-exhausted"]
    expected = json.loads(json.dumps(gold["expectedTermination"]).replace("$RUN_ID", budget["runId"]))
    golden_row = {"golden": "analysis-budget-exhausted", "expected": expected, "derived": budget["derived"]["projection"],
                  "secondaryDeficiencies": budget["derived"]["secondaryDeficiencies"], "deficiency": budget["derived"]["deficiency"],
                  "equal": budget["derived"]["projection"] == expected and budget["derived"]["deficiency"] == gold["scenarioAxes"]["deficiency"]
                  and budget["derived"]["secondaryDeficiencies"] == gold["scenarioAxes"]["secondaryDeficiencies"]}
    must("d9-golden-analysis-budget-exhausted", golden_row["equal"], golden_row)

    # ---- s6 candidate check on an indeterminate Run whose primary has a Coverage carrier
    carrier = next((runs[p["run"]] for p in projections if "projection" in p and "coverageId" in p["projection"]), None)
    candidates = []

    def cand(label, run, candidate, expect, validate=RT.step_termination_shape_ok):
        res = RT.check_projection(candidate, run["derived"], validate)
        got = res.get("refusal")
        ok = (expect is None and res["admitted"]) or got == expect
        must(f"s6:{label}", ok, res)
        candidates.append({"vector": label, "run": run["name"], "classification": "valid" if expect is None else "invalid", "candidate": candidate,
                           "firstRefusal": got, "expected": expect, "schemaValidCandidate": isinstance(candidate, dict) and RT.step_termination_shape_ok(candidate),
                           "result": res, "pass": ok})
    if must("carrier-run-available", carrier is not None):
        proj = carrier["derived"]["projection"]
        cand("exact-projection", carrier, dict(proj), None)
        if len(proj["reasonCodes"]) > 1:
            cand("reason-order-reversed", carrier, dict(proj, reasonCodes=list(reversed(proj["reasonCodes"]))), "RUN_TERMINATION_NOT_DERIVED")
        cand("carrier-omitted", carrier, {k: v for k, v in proj.items() if k != "coverageId"}, "RUN_TERMINATION_NOT_DERIVED")
        cand("other-run-id", carrier, dict(proj, runId=runs["ts-pass"]["runId"]), "RUN_TERMINATION_NOT_DERIVED")
        cand("fault-cause-present", carrier, dict(proj, faultCause="host-io"), "RUN_TERMINATION_NOT_DERIVED")
        cand("blessing-member", carrier, dict(proj, valid=True), "RUN_TERMINATION_UNKNOWN_FIELD")
        cand("delegated-detail-unvalidated", carrier, dict(proj, domainDetail={"code": "resolution-incomplete", "remedy": "resolve"}),
             "RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED", validate=None)
        cand("delegated-detail-shape-invalid", carrier, dict(proj, domainDetail={"code": "NOT.A_REGISTERED_CODE", "remedy": "x"}), "RUN_TERMINATION_DELEGATED_SHAPE")
        cand("non-object", carrier, ["indeterminate"], "cb24.RUN_TERMINATION_NOT_AN_OBJECT")

    # ---- s7 host composition
    compositions = []
    n = [700]

    def comp(label, run, candidate, expect, obs=None, **patch):
        n[0] += 1
        o = obs if obs is not None else observation(run, n[0], **patch)
        res = RT.admit_step_termination(candidate, run["g"], run["store"], run["runId"], run["published"], o)
        got = res.get("refusal")
        if isinstance(expect, tuple):
            ok = got in expect
        else:
            ok = (expect is None and res.get("admitted") is True) or (expect == "owner" and res.get("admitted") is None) or got == expect
        must(f"s7:{label}", ok, res)
        compositions.append({"vector": label, "run": run["name"], "classification": "valid" if expect in (None, "owner") else "invalid",
                             "candidate": candidate, "observation": o, "firstRefusal": got, "expected": list(expect) if isinstance(expect, tuple) else expect,
                             "result": {k: v for k, v in res.items() if k != "derived"}, "pass": ok})
    if carrier is not None:
        proj = carrier["derived"]["projection"]
        comp("committed-exact-lawful-omission", carrier, dict(proj), None)
        base_obs = observation(carrier, 800)
        comp("execution-id-of-terminating-attempt", carrier, dict(proj, executionId=base_obs["attempts"][0]["executionId"]), None, obs=base_obs)
        retry = copy.deepcopy(base_obs)
        retry["attempts"].insert(0, {"executionId": P7.exec_id(801), "outcome": "failed", "faultCause": "host-io", "retried": True})
        comp("retried-attempt-terminating-last", carrier, dict(proj), None, obs=retry)
        comp("earlier-retried-execution-id", carrier, dict(proj, executionId=P7.exec_id(801)), "RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT", obs=retry)
        comp("unrelated-registered-detail", carrier, dict(proj, domainDetail={"code": "HOST.INVARIANT_VIOLATED", "remedy": "x"}), "RUN_TERMINATION_DETAIL_NOT_ADMITTED")
        comp("authority-beside-committed-run", carrier, dict(proj, authority="ephemeral"),
             ("RUN_TERMINATION_AUTHORITY_NOT_COMPOSED", "RUN_TERMINATION_DELEGATED_SHAPE"))
        other = runs["ts-pass"]
        wrong = copy.deepcopy(base_obs)
        wrong["receipt"]["runId"] = other["runId"]
        comp("receipt-of-another-run", carrier, dict(proj), "RUN_TERMINATION_RECEIPT_RUN_MISMATCH", obs=wrong)
        wrong = copy.deepcopy(base_obs)
        wrong["receipt"]["executionId"] = P7.exec_id(899)
        comp("receipt-of-another-attempt", carrier, dict(proj), "RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH", obs=wrong)
        wrong = copy.deepcopy(base_obs)
        wrong["receipt"]["inventoryDigest"] = RT.commit_inventory(carrier["runId"], carrier["published"][0], carrier["published"][1] + ["0" * 64])[1]
        comp("receipt-inventory-of-a-wider-store", carrier, dict(proj), "RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH", obs=wrong)
        for label, field, value, key in (("attempt-plan-of-another-run", "planId", other["g"]["plan_id"], "RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH"),
                                         ("attempt-execution-plan-of-another-run", "executionPlanId", other["g"]["seal"]["executionPlanId"],
                                          "RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH"),
                                         ("attempt-stage-count-not-the-plan", "stageCount", 2, "RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH"),
                                         ("attempt-progress-beyond-plan", "stagesCompleted", 2, "RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH"),
                                         ("attempt-first-failed-stage-outside-plan", "firstFailedStage", 5, "RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH")):
            wrong = copy.deepcopy(base_obs)
            wrong["attempts"][-1]["derivation"][field] = value
            comp(label, carrier, dict(proj), key, obs=wrong)
        partial = copy.deepcopy(base_obs)
        partial["attempts"][-1]["derivation"]["stagesCompleted"] = 0
        comp("partial-stage-progress-admitted", carrier, dict(proj), None, obs=partial)
        wrong = copy.deepcopy(base_obs)
        wrong["attempts"].append(dict(wrong["attempts"][0]))
        comp("attempt-id-reused", carrier, dict(proj), "RUN_TERMINATION_ATTEMPT_ID_REUSED", obs=wrong)
        wrong = copy.deepcopy(base_obs)
        wrong["attempts"][-1]["outcome"] = "failed"
        comp("last-attempt-not-completed", carrier, dict(proj), "RUN_TERMINATION_ATTEMPT_NOT_TERMINATING", obs=wrong)
        wrong = copy.deepcopy(base_obs)
        del wrong["durability"]
        comp("observation-shape", carrier, dict(proj), "RUN_TERMINATION_OBSERVATION_SHAPE", obs=wrong)
        comp("projection-refusal-not-rescued-by-delegated", carrier, dict({k: v for k, v in proj.items() if k != "coverageId"},
                                                                          executionId=base_obs["attempts"][0]["executionId"]),
             "RUN_TERMINATION_NOT_DERIVED", obs=base_obs)
        eph = copy.deepcopy(base_obs)
        eph["durability"], eph["receipt"] = "ephemeral", None
        ephemeral = {"class": "indeterminate", "reasonCodes": proj["reasonCodes"], "authority": "ephemeral"}
        comp("ephemeral-admitted", carrier, ephemeral, None, obs=eph)
        comp("ephemeral-with-run-id", carrier, dict(ephemeral, runId=carrier["runId"]), "RUN_TERMINATION_EPHEMERAL_NOT_COMMITTED_RUN", obs=eph)
        comp("ephemeral-without-authority", carrier, {k: v for k, v in ephemeral.items() if k != "authority"},
             "RUN_TERMINATION_EPHEMERAL_AUTHORITY_REQUIRED", obs=eph)
        comp("ephemeral-with-detail", carrier, dict(ephemeral, domainDetail={"code": "resolution-incomplete", "remedy": "x"}),
             "RUN_TERMINATION_DETAIL_NOT_ADMITTED", obs=eph)
        comp("operational-class-returns-owner", carrier, {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io"}, "owner")
    bproj = budget["derived"]["projection"]
    work_detail = {"code": "EVALUATION.WORK_BUDGET_EXHAUSTED", "remedy": "raise or narrow the admitted analysis work budget"}
    comp("work-budget-detail-selected", budget, dict(bproj, domainDetail=work_detail), None)
    comp("work-budget-detail-omitted", budget, dict(bproj), "RUN_TERMINATION_DETAIL_REQUIRED")
    comp("work-budget-detail-with-subject", budget, dict(bproj, domainDetail=dict(work_detail, subject="budget")), "RUN_TERMINATION_DETAIL_MEMBER_NOT_ADMITTED")
    passing = runs["ts-pass"]
    comp("success-committed", passing, dict(passing["derived"]["projection"]), None)
    comp("success-with-detail", passing, dict(passing["derived"]["projection"], domainDetail=work_detail), "RUN_TERMINATION_DETAIL_NOT_ADMITTED")
    failing = runs["ts-fail"]
    comp("policy-failed-committed", failing, dict(failing["derived"]["projection"]), None)

    bridge_table = []
    for cause in sorted(RT.REGISTERED):
        rank, d9 = RT.bridge(cause)
        bridge_table.append({"cause": cause, "rank": rank, "d9Deficiency": d9, "reasonCode": RT.TO_REASON[d9]})
    try:
        RT.bridge("made-up-cause")
        unregistered = None
    except RT.TerminationRefusal as exc:
        unregistered = exc.key
    must("unregistered-cause-refuses", unregistered == "RUN_TERMINATION_CAUSE_UNREGISTERED", unregistered)
    out = {"owner": "docs/coop/design-corrections/foundation/run-termination-contract.v1.md", "classification": "valid",
           "projections": projections, "d9Golden": golden_row, "candidateChecks": candidates, "hostComposition": compositions,
           "causeBridge": {"classification": "explanatory", "rows": bridge_table, "unregisteredCauseRefusal": unregistered},
           "notConstructedFromBuiltRuns": ["s7.5 row 2 COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED needs reasonCodes[0] COVERAGE.PROVIDER_UNAVAILABLE; no built Run has a provider-unavailable primary",
                                           "s5 stage-terminal carriers: no built Run retains a budget-exhausted or unavailable stageTerminal"],
           "readings": RT.__doc__.split("Reconstruction readings recorded for phase 10 (not contradictions of the text):")[1].strip(),
           "assertionFailures": failures}
    with open(f"{OUT}/vectors/run-termination.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("runs", len(projections), "candidates", len(candidates), "compositions", len(compositions), "failures", len(failures))
    print(json.dumps(failures, default=str)[:5000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
