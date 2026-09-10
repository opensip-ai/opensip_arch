#!/usr/bin/env python3
"""Reproduce root's M2 follow-up counterexample: the rule-level evidenceUse declaration obligation.

Root reported that on released v1, a policy whose evidence atom carried NO matching rule-level
`evidenceUse` was refused by `resolve_policy` (IMPORT.ABSENT_FOR_PREDICATE) while `close_run`
ADMITTED the full Run - one document, two answers. The atom is changed in place before graph
construction, so policy, compiled program and addressed witness all carry the same predicate.

Both cases are empty/indeterminate with absent runtime evidence; this is a declaration-admission
law, not a claim about findings.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

work = Path(sys.argv[1])
dc = work / "docs/coop/design-corrections"
spec = importlib.util.spec_from_file_location("m2_fixture", dc / "integration-fixtures.py")
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)
M, C = f.M, f.C
W = M.workflow_admission()

ATOM = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
        "filters": [], "evidence": "runtime"}
DECLARED = [{"kind": "runtime", "requirement": "required"}]


def policy_answer(evidence_use):
    rule = dict(f.rule_for("typescript", copy.deepcopy(ATOM), "symbol"),
                evidenceUse=copy.deepcopy(evidence_use))
    doc = {"schemaFamily": "opensip.product.policy", "schemaMajor": 1,
           "gateSeverityAtLeast": "error", "rules": [rule]}
    try:
        W.resolve_policy(doc)
        return None
    except W.Refusal as exc:
        return str(exc.detail)


def closure_answer(evidence_use):
    """Full Run closure over a graph whose policy, compiled program and addressed witness all carry
    the same atom and the same declaration."""
    run, objects, blobs = f.build(resolved=True, has_match=True)
    put = lambda v: f.put_blob(blobs, v)
    plan = copy.deepcopy(objects[run["planId"]][1])
    policy = C.parse(blobs[plan["policyDigest"]])
    policy["rules"][0]["emitWhen"] = copy.deepcopy(ATOM)
    policy["rules"][0]["evidenceUse"] = copy.deepcopy(evidence_use)
    program = f.compiled_program(policy)
    plan["policyDigest"] = put(policy)
    program_digest = put(program)
    pk = objects[run["evaluationSealId"]][1]["proofBundleId"]
    proof = copy.deepcopy(objects[pk][1])
    proof["ruleProgramDigest"] = program_digest
    for pred in proof["predicateProofs"]:
        witness = C.parse(blobs[pred["witnessDigest"]])
        record = C.parse(blobs[witness["programPredicateDigest"]])
        node = M.predicate_node_at(
            next(r for r in program["rules"] if r["ruleId"] == record["ruleId"])["emitWhen"],
            record["predicateId"])
        import hashlib
        record.update(ruleProgramDigest=program_digest, operation=node["op"],
                      nodeDigest=hashlib.sha256(C.canonical(node)).hexdigest())
        witness["programPredicateDigest"] = put(record)
        pred["witnessDigest"] = put(witness)
        pred["operation"] = node["op"]
    f.rekey(objects, pk, proof, run)
    seal_key = run["evaluationSealId"]
    seal = copy.deepcopy(objects[seal_key][1])
    seal["policyDigest"] = plan["policyDigest"]
    f.rekey(objects, seal_key, seal, run)
    f.rekey_plan(objects, blobs, run, plan)
    try:
        return None, M.close_run(run, objects, blobs)
    except Exception as exc:
        return str(exc)[:150], None


rows = []
for label, use in [("declared", DECLARED), ("undeclared", []),
                   ("wrong-kind", [{"kind": "history", "requirement": "required"}])]:
    p = policy_answer(use)
    c, run_id = closure_answer(use)
    rows.append({"case": label, "resolvePolicy": p, "closeRun": c, "runId": run_id,
                 "boundariesAgree": (p is None) == (c is None)})
report = {"standing": "Coauthor reproduction of root's M2 follow-up counterexample. The two policy "
                      "admission boundaries must give ONE answer for one document.",
          "sourceRoot": str(work), "cases": rows,
          "allBoundariesAgree": all(r["boundariesAgree"] for r in rows)}
print(json.dumps(report, indent=2))
sys.exit(0 if report["allBoundariesAgree"] else 1)
