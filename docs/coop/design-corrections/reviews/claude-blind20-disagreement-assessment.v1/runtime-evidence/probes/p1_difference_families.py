"""Group every measured proof difference into families, with exact values.

READ-ONLY over root's captured derivation. Writes only into this runtime.
"""
import collections
import hashlib
import json
from pathlib import Path

D = Path("/tmp/opensip-design-corrections/root-blind20-proof-differences33.v1")
RUNS = ["syntax-code", "typescript", "rust", "rust-partial", "syntax-data"]

out = {"standing": "READ-ONLY family grouping of root's exact consumer-vs-reference proof diffs."}
families = collections.Counter()
rows = {}
for n in RUNS:
    diffs = json.loads((D / n / "differences.json").read_text())
    cons = json.loads((D / n / "consumer-proof.json").read_text())
    ref = json.loads((D / n / "reference-proof.json").read_text())
    per = []
    for d in diffs:
        p = d["path"]
        seg = p.strip("/").split("/")
        top = seg[0]
        leaf = seg[-1] if len(seg) > 1 else top
        fam = {
            ("predicateProofs", "witnessDigest"): "witnessDigest",
            ("predicateProofs", "scopeIds"): "predicateScopeIds",
            ("predicateProofs", "value"): "predicateValue",
        }.get((top, leaf))
        if fam is None:
            if top == "findingIds":
                fam = "findingIds"
            elif top == "ruleResults" and "deficiencies" in seg:
                fam = "ruleResultDeficiencies:" + (leaf if leaf != "deficiencies" else "whole-list")
            elif top == "ruleResults" and "findingIds" in seg:
                fam = "ruleResultFindingIds"
            else:
                fam = "other:" + p
        families[fam] += 1
        per.append({"path": p, "family": fam,
                    "consumer": d.get("consumer"), "reference": d.get("reference"),
                    "lengths": d.get("lengths"), "missingFrom": d.get("missingFrom")})
    rows[n] = {
        "differenceCount": len(diffs),
        "familyCounts": dict(collections.Counter(x["family"] for x in per)),
        "differences": per,
        "consumerVerdict": cons.get("verdict"), "referenceVerdict": ref.get("verdict"),
        "consumerEvaluationState": cons.get("evaluationState"),
        "referenceEvaluationState": ref.get("evaluationState"),
        "consumerFindingCount": len(cons.get("findingIds") or []),
        "referenceFindingCount": len(ref.get("findingIds") or []),
        "executionDeficienciesEqual":
            cons.get("executionDeficiencies") == ref.get("executionDeficiencies"),
        "evaluationInputRefsEqual":
            cons.get("evaluationInputRefs") == ref.get("evaluationInputRefs"),
        "executionInputsDigestEqual":
            cons.get("executionInputsDigest") == ref.get("executionInputsDigest"),
        "predicateProofCount": [len(cons.get("predicateProofs") or []),
                                len(ref.get("predicateProofs") or [])],
        "consumerProofSha256": hashlib.sha256(
            (D / n / "consumer-proof.json").read_bytes()).hexdigest(),
        "referenceProofSha256": hashlib.sha256(
            (D / n / "reference-proof.json").read_bytes()).hexdigest(),
    }
out["familyTotals"] = dict(families)
out["runs"] = rows
print(json.dumps(out, indent=2, default=str))
