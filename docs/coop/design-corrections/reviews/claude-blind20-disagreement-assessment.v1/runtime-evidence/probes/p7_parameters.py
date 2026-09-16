"""Name the typescript finding parameterDigest difference. READ-ONLY."""
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


T = load("t7", B / "check-blind-successor33-export.v1.py")
R = load("r7", F / "evaluator_replay_model.v3.py")
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
rproof, ref_objects, ref_blobs = r["proof"], r["objects"], r["blobs"]

c_only = sorted(set(cproof["findingIds"]) - set(rproof["findingIds"]))
r_only = sorted(set(rproof["findingIds"]) - set(cproof["findingIds"]))
out = {"standing": "READ-ONLY finding parameter comparison.",
       "consumerOnlyFindingIds": c_only, "referenceOnlyFindingIds": r_only}
rows = []
for cf in c_only:
    crec = o[cf][1]
    for rf in r_only:
        rr = ref_objects.get(rf)
        rrec = rr[1] if isinstance(rr, tuple) else rr
        if not isinstance(rrec, dict) or rrec.get("subjectId") != crec.get("subjectId"):
            continue
        cpar = json.loads(b[crec["parameterDigest"]]) if crec["parameterDigest"] in b else None
        rpar = (json.loads(ref_blobs[rrec["parameterDigest"]])
                if rrec["parameterDigest"] in ref_blobs else None)
        delta = {}
        if isinstance(cpar, dict) and isinstance(rpar, dict):
            for k in sorted(set(cpar) | set(rpar)):
                if cpar.get(k) != rpar.get(k):
                    delta[k] = {"consumer": cpar.get(k), "reference": rpar.get(k)}
        rows.append({"subjectId": crec.get("subjectId"),
                     "consumerParameters": cpar, "referenceParameters": rpar,
                     "differingKeys": sorted(delta), "delta": delta,
                     "otherFindingFieldsEqual": {
                         k: crec.get(k) == rrec.get(k)
                         for k in sorted(set(crec) | set(rrec)) if k != "parameterDigest"}})
        break
out["pairs"] = rows
print(json.dumps(out, indent=2, default=str))
