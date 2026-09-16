"""Compare the WITNESS RECORD PREIMAGES, not just their digests.

A witnessDigest difference is opaque. This re-derives the reference witnesses on the exact
consumer inputs, pulls the consumer's own retained witness blobs, and diffs the records field by
field so the disagreement is named rather than hashed.

READ-ONLY. No remint: the consumer Run is never re-sealed and no consumer file is written.
"""
import collections
import importlib.util
import json
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
S = B / "candidate-subject.v33"
F = S / "docs/coop/design-corrections/foundation"
IN = B / "root-blind20-final33-replay.v1"
DIFF = B / "root-blind20-proof-differences33.v1"


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


T = load("t20", B / "check-blind-successor33-export.v1.py")
R = load("r20", F / "evaluator_replay_model.v3.py")
M = R.M
E = load("e20", F / "evaluator_composition_model.v3.py")

RUNS = ["syntax-data", "syntax-code", "typescript", "rust", "rust-partial"]
out = {"standing": "READ-ONLY witness preimage comparison on exact consumer inputs; no remint."}
summary = collections.Counter()

for n in RUNS:
    raw = (IN / "captured" / (n + ".store.json")).read_bytes()
    o, b, _ = T.decode(raw, M)
    d = T.parse(raw)
    rid = d["claim"]["runId"]
    run = o[rid][1]
    _, owner = M.open_run_closure(run, o, b)
    seal = o[run["evaluationSealId"]][1]
    cproof = o[seal["proofBundleId"]][1]
    r = R.derive(run["planId"], seal["executionPlanId"], seal["evaluatorClosure"],
                 cproof["evaluationInputRefs"], o, b, owner)
    rproof = r["proof"]
    ref_blobs = r.get("blobs") or {}

    rows = []
    for i, (cp, rp) in enumerate(zip(cproof["predicateProofs"], rproof["predicateProofs"])):
        cw, rw = cp.get("witnessDigest"), rp.get("witnessDigest")
        if cw == rw:
            continue
        c_rec = None
        raw_c = b.get(cw)
        if raw_c is not None:
            try:
                c_rec = json.loads(raw_c)
            except Exception:  # noqa: BLE001
                c_rec = {"_undecodable": True}
        raw_r = ref_blobs.get(rw)
        r_rec = json.loads(raw_r) if raw_r is not None else None
        fields = {}
        if isinstance(c_rec, dict) and isinstance(r_rec, dict):
            for k in sorted(set(c_rec) | set(r_rec)):
                if c_rec.get(k) != r_rec.get(k):
                    fields[k] = {"consumer": c_rec.get(k), "reference": r_rec.get(k)}
        rows.append({
            "index": i,
            "predicateId": cp.get("predicateId"), "subjectId": cp.get("subjectId"),
            "consumerValue": cp.get("value"), "referenceValue": rp.get("value"),
            "consumerWitnessDigest": cw, "referenceWitnessDigest": rw,
            "consumerWitnessRetained": raw_c is not None,
            "referenceWitnessAvailable": r_rec is not None,
            "differingFields": fields,
            "differingFieldNames": sorted(fields),
        })
        for k in fields:
            summary[k] += 1
    out[n] = {
        "runId": rid,
        "witnessDigestDifferences": len(rows),
        "predicateProofCount": len(cproof["predicateProofs"]),
        "rows": rows,
        "referenceBlobCount": len(ref_blobs),
    }
out["differingWitnessFieldTotals"] = dict(summary)
print(json.dumps(out, indent=2, default=str))
