"""Replay export per claimed complete positive (R-REPLAY-EXPORT, R-REPLAY-ENUM-AND-IDS, R-REPLAY-PREDICATE-WITNESS-VERDICT, R-REPLAY-COMPARE-BUNDLE).

Single Run:  /tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py runs/<name>.store.json runs/<name>.replay-export.json
All positives (spawns one fresh reference-interpreter process per Run):  python3 tools/replay_export.py

Order is admission first, replay after: close_run must ADMIT (complete graph admission + semantic replay) before anything is exported.
The export then recomputes the proof again from the admitted retained inputs only (no caller truth), and writes:
  inputs   - the exact selected refs, views, scopes, Coverage, facts, imports, subject inventories, policy/program/emission digests;
  derived  - per-rule enumeration (selected subject ids, state, unresolved ids), every predicate proof with its witness record
             (matchingFactIds, coverageIds, childPredicateIds, import rows, uncertain ids, deficiencies, value), finding ids/fingerprints;
  proof    - the complete recomputed proof bundle;
  comparison - byte equality of C(recomputed proof) vs the retained proof frame, and proof/evidence/seal/run identity equality.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/preserved/pre-s42"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]


def export_one(src, dst):
    sys.path.insert(0, OUT + "/ref")
    import canonical as K
    import closure as CL
    import evaluator as EV
    from store import Store
    raw = open(src, "rb").read()
    exported = json.loads(raw)
    store = Store.load(exported)
    admission = CL.close_run(store, exported["runId"])
    doc = {"run": os.path.basename(src)[:-len(".store.json")], "runId": exported["runId"], "storeFileSha256": hashlib.sha256(raw).hexdigest(),
           "pid": os.getpid(), "admission": {"result": admission["result"], "firstRefusal": admission.get("firstRefusal"),
                                             "graphFaults": admission["graphAdmission"]["faults"],
                                             "retainedClosure": {k: admission.get("retainedClosure", {}).get(k) for k in
                                                                 ("result", "firstRefusal", "requiredPreimages", "retainedPreimages", "referenceClassesWalked")},
                                             "replayFaults": admission["semanticReplay"].get("faults"),
                                             "reachableOutputSet": admission["semanticReplay"].get("reachableOutputSet")}}
    if admission["result"] != "ADMIT":
        doc["exported"] = False
        json.dump(doc, open(dst, "w"), indent=1, sort_keys=True)
        return 1
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    im = g["imports"]
    inp = EV.Inputs(plan=g["plan"], plan_id=g["plan_id"], exec_plan_id=g["exec_plan_id"], evaluator_closure=g["xi"]["evaluatorClosure"],
                    policy=g["policy"], waivers=g["waivers"], emission=g["emission"], enum_plan=g["enum"], inventories=g["index"]["inventories"],
                    views=g["views"], scopes=g["scopes"], coverages=g["coverages"], facts=g["facts"], fact_payloads=g["payloads"], bound=g["bound"],
                    imports={i: r["wrapper"] for i, r in im.items()}, import_payloads={i: r["payload"] for i, r in im.items()},
                    import_observations={i: r["observation"] for i, r in im.items()}, import_scopes={i: r["scope"] for i, r in im.items()},
                    import_flags={i: r["flags"] for i, r in im.items()}, exec_inputs=g["xi"], exec_inputs_digest=g["proof"]["executionInputsDigest"],
                    required_rows=g["derived"]["requiredRows"], scope_document=g["scope_document"], project_id=g["snapshot"]["projectId"])
    out = EV.evaluate(inp)
    proof = out["proof"]
    retained_hex = g["seal"]["proofBundleId"].split(":", 1)[1]
    retained_frame = store.blobs[retained_hex]
    witnesses = []
    for p in proof["predicateProofs"]:
        w = json.loads(out["blobs"][p["witnessDigest"]])
        witnesses.append({"ruleId": p["ruleId"], "subjectId": p["subjectId"], "predicateId": p["predicateId"], "operation": p["operation"], "value": p["value"],
                          "witnessDigest": p["witnessDigest"], "witnessRetainedByteEqual": store.blobs.get(p["witnessDigest"]) == out["blobs"][p["witnessDigest"]],
                          "witness": w})
    doc.update(exported=True, inputs={
        "planId": g["plan_id"], "executionPlanId": g["exec_plan_id"], "executionInputsDigest": g["proof"]["executionInputsDigest"],
        "evaluationInputRefs": proof["evaluationInputRefs"], "viewIds": sorted(g["views"]), "scopeIds": sorted(g["scopes"]), "coverageIds": sorted(g["coverages"]),
        "factIds": sorted(g["facts"]), "importIds": sorted(g["plan"]["importIds"]),
        "subjectInventoryDigests": sorted({d for (d, _) in g["index"]["inventories"].values()}),
        "policyDigest": g["plan"]["policyDigest"], "waiverDigest": g["plan"]["waiverDigest"], "ruleProgramDigest": proof["ruleProgramDigest"],
        "emissionRules": [r["ruleId"] for r in g["emission"]["rules"]], "scopeDocumentSelected": g["scope_document"] is not None},
        derived={"ruleEnumerations": [{"ruleId": r["ruleId"], "outcome": r["outcome"], "enumeration": r["enumeration"], "findingIds": r["findingIds"],
                                       "deficiencies": r["deficiencies"]} for r in proof["ruleResults"]],
                 "predicates": witnesses,
                 "findings": [{"findingId": f["findingId"], "ruleId": f["finding"]["ruleId"], "fingerprint": f["finding"]["fingerprint"],
                               "subjectPath": f["subjectPath"], "evidenceRefs": f["finding"]["evidenceRefs"]} for f in out["findings"]],
                 "waivedFindingIds": proof["waivedFindingIds"], "executionDeficiencies": proof["executionDeficiencies"],
                 "evaluationState": proof["evaluationState"], "verdict": proof["verdict"]},
        proof=proof,
        comparison={"proofBytesEqual": K.frame("proof-bundle", proof) == retained_frame, "proofId": [out["proofId"], g["seal"]["proofBundleId"]],
                    "evidenceIdEqual": out["evidenceId"] == g["run"]["evidenceId"], "sealIdEqual": out["sealId"] == g["run"]["evaluationSealId"],
                    "runIdEqual": out["runId"] == exported["runId"], "allWitnessesRetainedByteEqual": all(w["witnessRetainedByteEqual"] for w in witnesses),
                    "outputObjectsRecomputed": len(out["objects"])})
    json.dump(doc, open(dst, "w"), indent=1, sort_keys=True)
    c = doc["comparison"]
    return 0 if c["proofBytesEqual"] and c["evidenceIdEqual"] and c["sealIdEqual"] and c["runIdEqual"] and c["allWitnessesRetainedByteEqual"] else 1


def main_all():
    rows = []
    for rp in sorted(glob.glob(f"{OUT}/runs/*.replay.json")):
        name = os.path.basename(rp)[:-len(".replay.json")]
        if "~" in name or "." in name or json.load(open(rp))["result"] != "ADMIT":
            continue
        dst = f"{OUT}/runs/{name}.replay-export.json"
        p = subprocess.run(REF + [os.path.abspath(__file__), f"{OUT}/runs/{name}.store.json", dst], capture_output=True, text=True)
        d = json.load(open(dst)) if os.path.exists(dst) else {}
        rows.append({"run": name, "exit": p.returncode, "stderr": p.stderr[-800:], "exported": d.get("exported"), "comparison": d.get("comparison"),
                     "predicates": len(d.get("derived", {}).get("predicates", [])), "pid": d.get("pid")})
        print(name, p.returncode, d.get("exported"), (d.get("comparison") or {}).get("proofBytesEqual"))
    json.dump({"runs": rows, "allExportedAndEqual": all(r["exit"] == 0 and r["exported"] for r in rows)},
              open(f"{OUT}/runs/replay-export.summary.json", "w"), indent=1, sort_keys=True)
    return 0 if all(r["exit"] == 0 for r in rows) else 1


if __name__ == "__main__":
    sys.exit(export_one(sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else main_all())
