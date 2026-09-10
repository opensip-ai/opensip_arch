#!/usr/bin/env python
"""CB3-MUST-2 / CX-BV3-EVIDENCE-USE-1 at the RETAINED RUN boundary.

p3 established the policy-admission boundary but its close_run cases were
inconclusive: replacing the whole policy tripped FOREIGN_RECORD (my synthetic
rule was not a valid PolicyDocumentV1) and stripping evidenceUse from the
fixture policy was a semantic no-op, because that policy's only atom is a NATIVE
`references` atom with no `evidence` field at all. Neither outcome says anything
about the rule-level obligation.

This probe makes the atom an EVIDENCE atom and varies ONLY the declaration, so
the two cases differ in exactly one field. That isolates the join:

  undeclared -> must refuse with POLICY_RULE_NOT_ADMISSIBLE (the rule-level
                obligation, reached at close_run)
  declared   -> must NOT refuse for that reason (any later join failure is a
                different, named cause)

A same-cause result in both arms would mean the obligation is not what is
firing, so I compare causes rather than just admit/refuse.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("fx", HERE / "integration-fixtures.py")
M, C = F.M, F.C

results = []


def close_with_policy(case, mutate, expect_cause_prefix, expect_not=False):
    try:
        run, objects, blobs = F.build(resolved=True, has_match=True)
        plan_id = run["planId"]
        plan = dict(objects[plan_id][1])
        policy = mutate(copy.deepcopy(C.parse(blobs[plan["policyDigest"]])))
        new_policy_digest = F.put_blob(blobs, policy)
        plan["policyDigest"] = new_policy_digest
        F.rekey(objects, plan_id, plan, run)
        # Attempt 3 correction: the evaluation seal records policyDigest too,
        # and VERDICT_JOIN (which compares plan.policyDigest to
        # seal.policyDigest) runs BEFORE the policy-rule admission block. A
        # stale seal made all three arms refuse at VERDICT_JOIN, upstream of
        # the guard under test.
        seal_key = run["evaluationSealId"]
        seal = dict(objects[seal_key][1])
        seal["policyDigest"] = new_policy_digest
        F.rekey(objects, seal_key, seal, run)
        # Attempt 4 correction: the compiled RuleProgramV1 records policyDigest
        # and is joined twice (RULE_PROGRAM_POLICY_JOIN and
        # RULE_PROGRAM_COMPILATION_JOIN), both upstream of policy-rule
        # admission. I recompile the program from the mutated policy using the
        # SAME recipe the workflow unit publishes, so the program is the exact
        # projection of the policy rather than a stale one.
        import hashlib as _h
        program = F.compiled_program(policy)
        program_digest = _h.sha256(C.canonical(program)).hexdigest()
        F.put_blob(blobs, program)
        seal_key = run["evaluationSealId"]
        proof_key = objects[seal_key][1]["proofBundleId"]
        proof = dict(objects[proof_key][1])
        proof["ruleProgramDigest"] = program_digest
        F.rekey(objects, proof_key, proof, run)
        # Attempt 2 correction: rekey() rewrites typed OBJECTS only. Moving
        # plan2 leaves the stage-spec PAYLOAD BLOB naming the old Plan, and the
        # graph then refuses with EVIDENCE_UNAVAILABLE on the stale plan id --
        # which is not evidence about the mutation under test. All three arms
        # previously shared that one stale cause.
        F.resync_stage_spec(objects, blobs, run)
        F.resync_witness(objects, blobs, run)
        F.resync_proof_refs(objects, blobs, run)
    except Exception as exc:
        results.append({"case": case, "phase": "fixture",
                        "observed": "fixture-error",
                        "cause": f"{type(exc).__name__}: {str(exc)[:180]}",
                        "agrees": False})
        return
    try:
        M.close_run(run, objects, blobs)
        obs, cause = "admits", None
    except Exception as exc:
        obs, cause = "refuses", str(exc)[:220]
    if expect_cause_prefix == "":
        # Control arm: the assertion is simply that the graph admits.
        agrees = (obs == "admits")
    elif expect_not:
        agrees = not (cause or "").startswith(expect_cause_prefix)
    else:
        agrees = bool(cause and cause.startswith(expect_cause_prefix))
    results.append({"case": case, "observed": obs, "cause": cause,
                    "expectedCausePrefix": expect_cause_prefix,
                    "expectedNot": expect_not, "agrees": agrees})
    return cause


def make_evidence_atom(evidence_use):
    """Turn the fixture's single rule into an EVIDENCE atom and set the
    rule-level declaration to `evidence_use`. Only that array differs between
    the two arms."""
    def go(policy):
        rule = policy["rules"][0]
        rule["emitWhen"] = {
            "op": "exists",
            "relation": "runtime-observation",
            "minResolution": "observed",
            "filters": [],
            "evidence": "runtime",
        }
        rule["subjectEnumeration"] = {"subjectKind": "symbol",
                                      "universe": "typescript"}
        rule["evidenceUse"] = evidence_use
        return policy
    return go


def main():
    # Baseline: the untouched graph closes, so any refusal below is caused by
    # my mutation and not by the fixture.
    close_with_policy("control/untouched-policy", lambda p: p,
                      "", expect_not=True)

    undeclared = close_with_policy(
        "evidence-atom/UNDECLARED-evidenceUse",
        make_evidence_atom([]),
        "POLICY_RULE_NOT_ADMISSIBLE")

    declared = close_with_policy(
        "evidence-atom/DECLARED-matching-evidenceUse",
        make_evidence_atom([{"kind": "runtime", "requirement": "required"}]),
        "POLICY_RULE_NOT_ADMISSIBLE", expect_not=True)

    mismatched = close_with_policy(
        "evidence-atom/MISMATCHED-kind-evidenceUse",
        make_evidence_atom([{"kind": "test", "requirement": "required"}]),
        "POLICY_RULE_NOT_ADMISSIBLE")

    # The differential is the actual finding: the two arms must not share a
    # cause, otherwise the declaration is not what is being enforced.
    results.append({
        "case": "DIFFERENTIAL/undeclared-vs-declared",
        "observed": "distinct-causes" if undeclared != declared else "same-cause",
        "cause": json.dumps({"undeclared": (undeclared or "")[:150],
                             "declared": (declared or "")[:150]}),
        "agrees": undeclared != declared,
    })
    results.append({
        "case": "DIFFERENTIAL/mismatched-vs-declared",
        "observed": "distinct-causes" if mismatched != declared else "same-cause",
        "cause": json.dumps({"mismatched": (mismatched or "")[:150],
                             "declared": (declared or "")[:150]}),
        "agrees": mismatched != declared,
    })

    bad = [r for r in results if not r["agrees"]]
    print(json.dumps({"total": len(results), "disagreeing": bad,
                      "results": results}, indent=2))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
