"""Why does the reference cite a coverage partition the consumer omits?

Pulls the exact coverage payloads behind the coverageIds difference and the atom node, so the
selection law can be checked against the published contract rather than guessed.

READ-ONLY; no remint.
"""
import importlib.util
import json
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
S = B / "candidate-subject.v33"
F = S / "docs/coop/design-corrections/foundation"
IN = B / "root-blind20-final33-replay.v1"


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


T = load("t3", B / "check-blind-successor33-export.v1.py")
R = load("r3", F / "evaluator_replay_model.v3.py")
M = R.M
I = load("i3", F / "evaluator_input_model.v3.py")
A = load("a3", F / "atom_model.v1.py")

out = {"standing": "READ-ONLY coverage-selection comparison on exact consumer inputs."}

for n in ["syntax-data", "syntax-code", "rust"]:
    raw = (IN / "captured" / (n + ".store.json")).read_bytes()
    o, b, _ = T.decode(raw, M)
    rid = T.parse(raw)["claim"]["runId"]
    run = o[rid][1]
    _, owner = M.open_run_closure(run, o, b)
    seal = o[run["evaluationSealId"]][1]
    cproof = o[seal["proofBundleId"]][1]
    normalized, atom_inputs = I.reconstruct(run["planId"], seal["executionPlanId"],
                                            seal["evaluatorClosure"],
                                            cproof["evaluationInputRefs"], o, b, owner, M)
    r = R.derive(run["planId"], seal["executionPlanId"], seal["evaluatorClosure"],
                 cproof["evaluationInputRefs"], o, b, owner)
    ref_blobs = r["blobs"]
    rproof = r["proof"]

    policy = normalized["policy"]
    rules = {x["ruleId"]: x for x in policy["rules"]}

    cases = []
    for i, (cp, rp) in enumerate(zip(cproof["predicateProofs"], rproof["predicateProofs"])):
        if cp.get("witnessDigest") == rp.get("witnessDigest"):
            continue
        cw = json.loads(b[cp["witnessDigest"]])
        rw = json.loads(ref_blobs[rp["witnessDigest"]])
        c_cov, r_cov = set(cw["coverageIds"]), set(rw["coverageIds"])
        only_ref, only_cons = sorted(r_cov - c_cov), sorted(c_cov - r_cov)
        detail = []
        for cid in only_ref + only_cons:
            rec = atom_inputs["coverages"].get(cid)
            if rec is None:
                detail.append({"coverageId": cid, "inAtomInputs": False})
                continue
            entry = rec.get("entry") or {}
            key = rec.get("key") or {}
            detail.append({
                "coverageId": cid,
                "side": "reference-only" if cid in only_ref else "consumer-only",
                "key": key,
                "coverage": entry.get("coverage"), "deficiency": entry.get("deficiency"),
                "nativeCause": entry.get("nativeCause"),
                "resolutionCompleteness": entry.get("resolutionCompleteness"),
            })
        cases.append({
            "index": i, "ruleId": cp.get("ruleId"), "predicateId": cp.get("predicateId"),
            "subjectId": cp.get("subjectId"),
            "value": [cp.get("value"), rp.get("value")],
            "atomNode": rules.get(cp.get("ruleId"), {}).get("emitWhen"),
            "consumerCoverageIds": sorted(c_cov), "referenceCoverageIds": sorted(r_cov),
            "referenceOnly": only_ref, "consumerOnly": only_cons,
            "coverageDetail": detail,
            "consumerDeficiencyCauses": sorted({d["cause"] for d in cw["deficiencies"]}),
            "referenceDeficiencyCauses": sorted({d["cause"] for d in rw["deficiencies"]}),
        })
    # Which coverages exist at all, and their keys.
    inventory = []
    for cid, rec in sorted(atom_inputs["coverages"].items()):
        entry = rec.get("entry") or {}
        inventory.append({"coverageId": cid, "key": rec.get("key"),
                          "coverage": entry.get("coverage"),
                          "deficiency": entry.get("deficiency"),
                          "nativeCause": entry.get("nativeCause")})
    out[n] = {"runId": rid, "differingPredicates": cases,
              "atomInputCoverages": inventory,
              "atomInputCoverageCount": len(inventory)}

print(json.dumps(out, indent=2, default=str))
