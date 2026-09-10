"""Assemble a complete Run graph from admitted parts, then replay + close it."""
from __future__ import annotations

import hashlib

import build as B
import canon as K
import closure as CL
import kit
from evaluator import EvalView, replay
from store import split_id


def semantic_grant(store, scope_digest, operations=("read-source", "native-analysis"),
                   principals=None):
    g = {"schemaVersion": 2, "projectId": B.PROJECT_ID,
         "principals": principals or [
             {"kind": "first-party", "closureId": "closure2:" + "0" * 64,
              "ownerSourceDigest": None}],
         "analysisOperations": sorted(set(operations), key=lambda s: s.encode()),
         "scopeDigest": scope_digest}
    return store.put_record(g), g


def compile_program(policy, policy_digest):
    return {"schemaVersion": 1, "policyDigest": policy_digest,
            "rules": [{"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"],
                       "emitWhen": r["emitWhen"]} for r in policy["rules"]]}


def finish_run(store, *, plan_id, plan, snapshot_id, views, view_ids, scopes,
               facts, coverages, policy, policy_digest, waivers, rule_program,
               evaluator_closure_id, detector_closure_id, exec_plan_id,
               universe_language, capability_manifest_id, tamper=None):
    """Replay the evaluator, then mint proof/findings/evidence/seal/run."""
    rp_digest = store.put_record(rule_program)
    view = EvalView(facts=facts, scopes=scopes, coverages=coverages,
                    universe_language=universe_language)
    result = replay(policy, rule_program, rp_digest, view, waivers)

    # retain the witness and program-predicate preimages
    for w in result["witnesses"].values():
        store.put_record(w)
    for pp in result["programPredicates"].values():
        store.put_record(pp)

    eval_inputs = []
    for vid in view_ids:
        eval_inputs.append({"domain": "view", "digest": split_id(vid, "view2")})
    for cid in coverages:
        eval_inputs.append({"domain": "coverage", "digest": split_id(cid, "coverage2")})
    eval_inputs.append({"domain": "rule-program", "digest": rp_digest})
    eval_inputs.append({"domain": "policy", "digest": policy_digest})
    eval_inputs.sort(key=K.C)

    # findings
    finding_ids = []
    findings_out = []
    for f in result["findings"]:
        rule = next(r for r in policy["rules"] if r["ruleId"] == f["ruleId"])
        tokens = [f"path:{f['subject']}", f"rule:{f['ruleId']}"]
        discriminator = hashlib.sha256(K.C(tokens)).hexdigest()
        store.put_blob(K.C(tokens))
        fp = {"schemaVersion": 2,
              "ruleStableId": rule["ruleProgramRef"]["ruleStableId"],
              "detectorSemanticsMajor": rule["ruleProgramRef"]["semanticsMajor"],
              "subjectKey": {"language": "typescript", "kind": "file",
                             "logicalPath": f["subject"],
                             "qualifiedName": f["subject"],
                             "discriminator": discriminator},
              "relatedSubjectKeys": []}
        fp_id = store.put_identity("finding-fingerprint", fp)
        params = {"schemaVersion": 2, "messageCode": rule.get("messageCode", "cb9.finding"),
                  "parameters": {"subject": f["subject"]}}
        pdigest = store.put_record(params)
        witness_refs = sorted(
            [{"domain": "predicate-witness", "digest": p["witnessDigest"]}
             for p in result["predicateProofs"]
             if p["ruleId"] == f["ruleId"] and p["subjectId"] == f["subject"]
             and p["predicateId"] == "p"], key=K.C)
        fin = {"schemaVersion": 2, "fingerprint": fp_id,
               "ruleClosure": detector_closure_id, "subjectId": f["subject"],
               "messageCode": params["messageCode"], "parameterDigest": pdigest,
               "severity": rule["severity"], "evidenceRefs": witness_refs}
        fid = store.put_identity("finding", fin)
        finding_ids.append(fid)
        findings_out.append(fin)

    verdict = result["verdict"]
    if tamper == "verdict":
        verdict = {"fail": "pass", "pass": "fail",
                   "indeterminate": "pass"}[result["verdict"]]

    proof = {"schemaVersion": 2, "planId": plan_id, "executionPlanId": exec_plan_id,
             "evaluatorClosure": evaluator_closure_id,
             "ruleProgramDigest": rp_digest,
             "evaluationInputRefs": eval_inputs,
             "predicateProofs": result["predicateProofs"],
             "findingIds": sorted(finding_ids, key=K.C),
             "verdict": verdict}
    if tamper == "predicate-value":
        pp = [dict(p) for p in proof["predicateProofs"]]
        pp[0]["value"] = {"true": "false", "false": "true",
                          "indeterminate": "true"}[pp[0]["value"]]
        proof["predicateProofs"] = pp
    proof_id = store.put_identity("proof-bundle", proof)

    evidence = {"schemaVersion": 2, "planId": plan_id,
                "viewIds": sorted(view_ids, key=K.C),
                "coverageIds": sorted(coverages, key=K.C),
                "importIds": list(plan["importIds"]),
                "findingIds": sorted(finding_ids, key=K.C),
                "proofBundleId": proof_id}
    evidence_id = store.put_identity("semantic-evidence", evidence)

    seal = {"schemaVersion": 2, "planId": plan_id, "executionPlanId": exec_plan_id,
            "evidenceId": evidence_id, "evaluatorClosure": evaluator_closure_id,
            "policyDigest": policy_digest, "proofBundleId": proof_id,
            "verdict": verdict}
    seal_id = store.put_identity("evaluation-seal", seal)

    run = {"schemaVersion": 2, "projectId": B.PROJECT_ID, "snapshotId": snapshot_id,
           "planId": plan_id, "evidenceId": evidence_id,
           "evaluationSealId": seal_id,
           "capabilityManifestId": capability_manifest_id}
    run_id = store.put_identity("run", run)
    return {"runId": run_id, "run": run, "seal": seal, "evidence": evidence,
            "proof": proof, "replay": result, "ruleProgramDigest": rp_digest,
            "findings": findings_out}


def verify_replay(store, closed, expected):
    """Semantic proof replay: recompute the complete bundle from the RETAINED
    inputs and compare it to the retained claim.  A mismatch REFUSES."""
    facts = {fid: closed["facts"][fid] for fid in closed["facts"]}
    scopes = closed["scopes"]
    coverages = {cid: {"scopeId": c["scopeId"], "payload": c["payload"]}
                 for cid, c in closed["coverages"].items()}
    ulang = {}
    for uhex, (dom, u) in closed["universes"].items():
        ulang[uhex] = kit.DOMAIN_SETS["native-semantic-universe"][dom]["language"]
    view = EvalView(facts=facts, scopes=scopes, coverages=coverages,
                    universe_language=ulang)
    recomputed = replay(closed["policy"], closed["ruleProgram"],
                        closed["proof"]["ruleProgramDigest"], view,
                        closed["waivers"])
    diffs = []
    retained = closed["proof"]
    if recomputed["verdict"] != retained["verdict"]:
        diffs.append(f"verdict: recomputed {recomputed['verdict']} != retained "
                     f"{retained['verdict']}")
    rk = {(p["ruleId"], p["subjectId"], p["predicateId"]): p
          for p in recomputed["predicateProofs"]}
    tk = {(p["ruleId"], p["subjectId"], p["predicateId"]): p
          for p in retained["predicateProofs"]}
    if set(rk) != set(tk):
        diffs.append(f"predicate address set differs: {sorted(set(rk) ^ set(tk))}")
    for key in sorted(set(rk) & set(tk)):
        a, b = rk[key], tk[key]
        for field in ("operation", "value", "witnessDigest", "scopeIds"):
            if a[field] != b[field]:
                diffs.append(f"{key} {field}: recomputed {a[field]} != retained {b[field]}")
    rf = sorted((f["ruleId"], f["subject"]) for f in recomputed["findings"])
    tf = sorted((closed["findings"][fid]["finding"]["subjectId"],)
                for fid in closed["findings"])
    if len(rf) != len(tf):
        diffs.append(f"finding count: recomputed {len(rf)} != retained {len(tf)}")
    return {"ok": not diffs, "diffs": diffs, "recomputed": recomputed}
