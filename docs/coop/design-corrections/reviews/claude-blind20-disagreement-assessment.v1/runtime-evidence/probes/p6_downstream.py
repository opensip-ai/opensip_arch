"""Is the rust count-at-most value gap downstream of the atom-completeness gap, and what field
makes the two typescript findings differ? READ-ONLY."""
import json
from pathlib import Path

D = Path("/tmp/opensip-design-corrections/root-blind20-proof-differences33.v1")
B = Path("/tmp/opensip-design-corrections")
IN = B / "root-blind20-final33-replay.v1"
out = {"standing": "READ-ONLY downstream-linkage check."}

# --- rust: tie the four indeterminate count-at-most predicates to their witness deficiencies
cons = json.loads((D / "rust" / "consumer-proof.json").read_text())
ref = json.loads((D / "rust" / "reference-proof.json").read_text())
rows = []
ref_by = {(p["ruleId"], p["subjectId"], p["predicateId"]): p for p in ref["predicateProofs"]}
for cp in cons["predicateProofs"]:
    if cp["operation"] != "count-at-most":
        continue
    rp = ref_by[(cp["ruleId"], cp["subjectId"], cp["predicateId"])]
    rows.append({"subjectId": cp["subjectId"],
                 "consumerValue": cp["value"], "referenceValue": rp["value"],
                 "valuesDiffer": cp["value"] != rp["value"],
                 "witnessDiffers": cp["witnessDigest"] != rp["witnessDigest"],
                 "consumerScopeIds": len(cp["scopeIds"]), "referenceScopeIds": len(rp["scopeIds"])})
out["rustCountAtMost"] = {
    "predicates": rows,
    "everyValueDifferenceAlsoHasAWitnessDifference":
        all(r["witnessDiffers"] for r in rows if r["valuesDiffer"]),
    "valueDifferences": sum(1 for r in rows if r["valuesDiffer"]),
    "witnessDifferences": sum(1 for r in rows if r["witnessDiffers"]),
}

# --- typescript: which field distinguishes the two differing findings?
import importlib.util


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


S = B / "candidate-subject.v33"
F = S / "docs/coop/design-corrections/foundation"
T = load("t6", B / "check-blind-successor33-export.v1.py")
R = load("r6", F / "evaluator_replay_model.v3.py")
M = R.M

raw = (IN / "captured" / "typescript.store.json").read_bytes()
o, b, _ = T.decode(raw, M)
rid = T.parse(raw)["claim"]["runId"]
run = o[rid][1]
_, owner = M.open_run_closure(run, o, b)
seal = o[run["evaluationSealId"]][1]
cproof = o[seal["proofBundleId"]][1]
r = R.derive(run["planId"], seal["executionPlanId"], seal["evaluatorClosure"],
             cproof["evaluationInputRefs"], o, b, owner)
rproof, ref_objects = r["proof"], r["objects"]

c_only = sorted(set(cproof["findingIds"]) - set(rproof["findingIds"]))
r_only = sorted(set(rproof["findingIds"]) - set(cproof["findingIds"]))
pairs = []
for cf in c_only:
    crec = o.get(cf)
    crec = crec[1] if crec else None
    best = None
    for rf in r_only:
        rrec = ref_objects.get(rf)
        rrec = rrec[1] if isinstance(rrec, tuple) else rrec
        if not isinstance(crec, dict) or not isinstance(rrec, dict):
            continue
        same_subject = crec.get("subjectId") == rrec.get("subjectId")
        if same_subject:
            delta = {k: {"consumer": crec.get(k), "reference": rrec.get(k)}
                     for k in sorted(set(crec) | set(rrec)) if crec.get(k) != rrec.get(k)}
            best = {"consumerFindingId": cf, "referenceFindingId": rf,
                    "subjectId": crec.get("subjectId"),
                    "differingFieldNames": sorted(delta),
                    "differingFields": {k: v for k, v in delta.items() if k != "citations"},
                    "citationCounts": [len(crec.get("citations") or []),
                                       len(rrec.get("citations") or [])],
                    "citationDomainsConsumer": sorted({x["domain"] for x in (crec.get("citations") or [])}),
                    "citationDomainsReference": sorted({x["domain"] for x in (rrec.get("citations") or [])}),
                    "citationsOnlyConsumer": [x for x in (crec.get("citations") or [])
                                              if x not in (rrec.get("citations") or [])],
                    "citationsOnlyReference": [x for x in (rrec.get("citations") or [])
                                               if x not in (crec.get("citations") or [])]}
            break
    pairs.append(best or {"consumerFindingId": cf, "matched": False})
out["typescriptFindingIdentity"] = {
    "consumerOnly": c_only, "referenceOnly": r_only, "pairs": pairs,
}
print(json.dumps(out, indent=2, default=str))
