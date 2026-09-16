"""Consolidate the families into root causes, using SET comparison (not index alignment).

Index-aligned diffs over canonical SETS overstate the difference: a member present on both sides
at a different position reads as several field differences. This compares membership.

READ-ONLY; no remint.
"""
import collections
import json
from pathlib import Path

D = Path("/tmp/opensip-design-corrections/root-blind20-proof-differences33.v1")
RUNS = ["syntax-code", "typescript", "rust", "rust-partial", "syntax-data"]
out = {"standing": "READ-ONLY set-level root-cause consolidation."}


def key(d):
    return json.dumps(d, sort_keys=True)


runs = {}
for n in RUNS:
    cons = json.loads((D / n / "consumer-proof.json").read_text())
    ref = json.loads((D / n / "reference-proof.json").read_text())
    rules = {}
    for cr, rr in zip(cons["ruleResults"], ref["ruleResults"]):
        c = {key(x) for x in cr["deficiencies"]}
        r = {key(x) for x in rr["deficiencies"]}
        only_c = [json.loads(x) for x in sorted(c - r)]
        only_r = [json.loads(x) for x in sorted(r - c)]
        if not only_c and not only_r and cr["findingIds"] == rr["findingIds"]:
            continue
        rules[cr["ruleId"]] = {
            "outcome": [cr["outcome"], rr["outcome"]],
            "deficiencyCounts": [len(cr["deficiencies"]), len(rr["deficiencies"])],
            "sharedMembers": len(c & r),
            "consumerOnlyCauses": dict(collections.Counter(
                str(x.get("cause")) + "/" + str(x.get("nativeCause")) for x in only_c)),
            "referenceOnlyCauses": dict(collections.Counter(
                str(x.get("cause")) + "/" + str(x.get("nativeCause")) for x in only_r)),
            "consumerOnlyCount": len(only_c), "referenceOnlyCount": len(only_r),
            "findingIdsEqual": cr["findingIds"] == rr["findingIds"],
            "findingCounts": [len(cr["findingIds"]), len(rr["findingIds"])],
        }
    # Composite-node scopeIds law check: composition unions children scopeIds.
    by_pid = {}
    for p in ref["predicateProofs"]:
        by_pid[(p["ruleId"], p["subjectId"], p["predicateId"])] = p
    composite = []
    for cp in cons["predicateProofs"]:
        if cp["operation"] not in ("and", "or", "not"):
            continue
        rp = by_pid.get((cp["ruleId"], cp["subjectId"], cp["predicateId"]))
        if rp is None:
            continue
        # children are predicateIds extending this one by one component
        kids = [q for q in cons["predicateProofs"]
                if q["ruleId"] == cp["ruleId"] and q["subjectId"] == cp["subjectId"]
                and q["predicateId"] != cp["predicateId"]
                and q["predicateId"].startswith(cp["predicateId"])]
        union = sorted({s for k in kids for s in k["scopeIds"]})
        composite.append({
            "predicateId": cp["predicateId"], "operation": cp["operation"],
            "consumerScopeIds": cp["scopeIds"], "referenceScopeIds": rp["scopeIds"],
            "unionOfConsumerChildren": union,
            "consumerEqualsUnionOfItsOwnChildren": sorted(cp["scopeIds"]) == union,
            "referenceEqualsUnionOfConsumerChildren": sorted(rp["scopeIds"]) == union,
            "childCount": len(kids),
        })
    # Finding identity: same count but different ids?
    c_f, r_f = cons["findingIds"], ref["findingIds"]
    runs[n] = {
        "ruleLevel": rules,
        "compositeNodes": composite,
        "compositeNodesWithEmptyConsumerScopeIds":
            sum(1 for x in composite if not x["consumerScopeIds"]),
        "compositeNodesWhereReferenceIsChildUnion":
            sum(1 for x in composite if x["referenceEqualsUnionOfConsumerChildren"]),
        "compositeNodesWhereConsumerIsChildUnion":
            sum(1 for x in composite if x["consumerEqualsUnionOfItsOwnChildren"]),
        "findingCounts": [len(c_f), len(r_f)],
        "findingIdsEqual": c_f == r_f,
        "findingsOnlyConsumer": sorted(set(c_f) - set(r_f)),
        "findingsOnlyReference": sorted(set(r_f) - set(c_f)),
    }
out["runs"] = runs

# Cross-run cause substitution tally.
subs = collections.Counter()
for n, r in runs.items():
    for rid, row in r["ruleLevel"].items():
        for k, v in row["consumerOnlyCauses"].items():
            subs["consumer-only:" + k.split("/")[0]] += v
        for k, v in row["referenceOnlyCauses"].items():
            subs["reference-only:" + k.split("/")[0]] += v
out["causeSubstitutionTally"] = dict(sorted(subs.items()))
print(json.dumps(out, indent=2, default=str))
