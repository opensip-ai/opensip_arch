"""The non-witness families: predicateValue, predicateScopeIds, findingIds, ruleResult deficiencies.

READ-ONLY over root's captured derivation plus exact consumer inputs; no remint.
"""
import collections
import json
from pathlib import Path

D = Path("/tmp/opensip-design-corrections/root-blind20-proof-differences33.v1")
out = {"standing": "READ-ONLY analysis of the non-witnessDigest difference families."}

# --- rust: predicate value disagreements and the finding-count gap -------------------------
n = "rust"
diffs = json.loads((D / n / "differences.json").read_text())
cons = json.loads((D / n / "consumer-proof.json").read_text())
ref = json.loads((D / n / "reference-proof.json").read_text())
vals = []
for d in diffs:
    if d["path"].endswith("/value"):
        idx = int(d["path"].strip("/").split("/")[1])
        cp, rp = cons["predicateProofs"][idx], ref["predicateProofs"][idx]
        vals.append({"index": idx, "consumerValue": d["consumer"], "referenceValue": d["reference"],
                     "ruleId": cp.get("ruleId"), "predicateId": cp.get("predicateId"),
                     "subjectId": cp.get("subjectId"), "operation": cp.get("operation"),
                     "consumerScopeIds": cp.get("scopeIds"), "referenceScopeIds": rp.get("scopeIds")})
out["rust"] = {
    "predicateValueDifferences": vals,
    "consumerFindingIds": cons["findingIds"], "referenceFindingIds": ref["findingIds"],
    "consumerFindingCount": len(cons["findingIds"]), "referenceFindingCount": len(ref["findingIds"]),
    "findingsOnlyInReference": sorted(set(ref["findingIds"]) - set(cons["findingIds"])),
    "findingsOnlyInConsumer": sorted(set(cons["findingIds"]) - set(ref["findingIds"])),
    "consumerVerdict": cons["verdict"], "referenceVerdict": ref["verdict"],
    "perPredicateValueTally": {
        "consumer": dict(collections.Counter(p["value"] for p in cons["predicateProofs"])),
        "reference": dict(collections.Counter(p["value"] for p in ref["predicateProofs"])),
    },
    "ruleResultOutcomes": {
        "consumer": [(r["ruleId"], r["outcome"], len(r["findingIds"]), len(r["deficiencies"]))
                     for r in cons["ruleResults"]],
        "reference": [(r["ruleId"], r["outcome"], len(r["findingIds"]), len(r["deficiencies"]))
                      for r in ref["ruleResults"]],
    },
}

# --- typescript: predicateProofs[*].scopeIds -----------------------------------------------
n = "typescript"
diffs = json.loads((D / n / "differences.json").read_text())
cons = json.loads((D / n / "consumer-proof.json").read_text())
ref = json.loads((D / n / "reference-proof.json").read_text())
scopes = []
for d in diffs:
    if d["path"].endswith("/scopeIds"):
        idx = int(d["path"].strip("/").split("/")[1])
        cp = cons["predicateProofs"][idx]
        c, r = set(d["consumer"] or []), set(d["reference"] or [])
        scopes.append({"index": idx, "ruleId": cp.get("ruleId"),
                       "predicateId": cp.get("predicateId"), "operation": cp.get("operation"),
                       "subjectId": cp.get("subjectId"),
                       "consumerCount": len(c), "referenceCount": len(r),
                       "referenceOnly": sorted(r - c), "consumerOnly": sorted(c - r)})
out["typescript"] = {
    "scopeIdDifferences": scopes,
    "findingIdDifferences": [d for d in diffs if d["path"].startswith("/findingIds")],
    "ruleResultFindingIdDifferences": [d for d in diffs if "/findingIds/" in d["path"]
                                       and d["path"].startswith("/ruleResults")],
    "consumerFindingCount": len(cons["findingIds"]),
    "referenceFindingCount": len(ref["findingIds"]),
    "findingsOnlyInReference": sorted(set(ref["findingIds"]) - set(cons["findingIds"])),
    "findingsOnlyInConsumer": sorted(set(cons["findingIds"]) - set(ref["findingIds"])),
}

# --- rust-partial: the per-field deficiency families ---------------------------------------
n = "rust-partial"
diffs = json.loads((D / n / "differences.json").read_text())
cons = json.loads((D / n / "consumer-proof.json").read_text())
ref = json.loads((D / n / "reference-proof.json").read_text())
cd = cons["ruleResults"][0]["deficiencies"]
rd = ref["ruleResults"][0]["deficiencies"]
pairs = []
for i, (c, r) in enumerate(zip(cd, rd)):
    delta = {k: {"consumer": c.get(k), "reference": r.get(k)}
             for k in sorted(set(c) | set(r)) if c.get(k) != r.get(k)}
    pairs.append({"index": i, "differingFields": sorted(delta),
                  "consumerCause": c.get("cause"), "referenceCause": r.get("cause"),
                  "consumerNativeCause": c.get("nativeCause"),
                  "referenceNativeCause": r.get("nativeCause"),
                  "consumerUniverse": c.get("universe"), "referenceUniverse": r.get("universe"),
                  "consumerSource": c.get("source"), "referenceSource": r.get("source"),
                  "consumerInputRefDomains": sorted({x["domain"] for x in (c.get("inputRefs") or [])}),
                  "referenceInputRefDomains": sorted({x["domain"] for x in (r.get("inputRefs") or [])}),
                  "consumerInputRefCount": len(c.get("inputRefs") or []),
                  "referenceInputRefCount": len(r.get("inputRefs") or [])})
out["rust-partial"] = {
    "deficiencyCount": [len(cd), len(rd)],
    "perDeficiency": pairs,
    "causeTally": {
        "consumer": dict(collections.Counter(x.get("cause") for x in cd)),
        "reference": dict(collections.Counter(x.get("cause") for x in rd)),
    },
    "nativeCauseTally": {
        "consumer": dict(collections.Counter(str(x.get("nativeCause")) for x in cd)),
        "reference": dict(collections.Counter(str(x.get("nativeCause")) for x in rd)),
    },
}

# --- syntax-code: the two whole-list ruleResult deficiency differences ----------------------
n = "syntax-code"
diffs = json.loads((D / n / "differences.json").read_text())
cons = json.loads((D / n / "consumer-proof.json").read_text())
ref = json.loads((D / n / "reference-proof.json").read_text())
rows = []
for d in diffs:
    if d["path"].endswith("/deficiencies"):
        idx = int(d["path"].strip("/").split("/")[1])
        c, r = d["consumer"] or [], d["reference"] or []
        rows.append({"ruleIndex": idx, "ruleId": cons["ruleResults"][idx]["ruleId"],
                     "counts": [len(c), len(r)],
                     "consumerCauses": dict(collections.Counter(x.get("cause") for x in c)),
                     "referenceCauses": dict(collections.Counter(x.get("cause") for x in r))})
out["syntax-code"] = {"ruleResultDeficiencyDifferences": rows}

n = "syntax-data"
cons = json.loads((D / n / "consumer-proof.json").read_text())
ref = json.loads((D / n / "reference-proof.json").read_text())
c = cons["ruleResults"][0]["deficiencies"]
r = ref["ruleResults"][0]["deficiencies"]
out["syntax-data"] = {
    "counts": [len(c), len(r)],
    "consumerCauses": dict(collections.Counter(x.get("cause") for x in c)),
    "referenceCauses": dict(collections.Counter(x.get("cause") for x in r)),
}

print(json.dumps(out, indent=2, default=str))
