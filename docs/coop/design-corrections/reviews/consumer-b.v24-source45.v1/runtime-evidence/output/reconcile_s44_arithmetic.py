"""Internal reporting-consistency reconciliation of my own source44 result-comparison arithmetic (source45.v1).

The source44 blind-review.md said "251 of 473 retained result files are byte-identical", while selfcheck/s44-result-diffs.json reports 103 differing
files of 473 (89 + 10 + 4). This script derives the numbers only from retained source44 files, as copied into this runtime:
  - preserved/s43-final/results-manifest.json          the 473 source43 hashes (the comparison base)
  - selfcheck/s44-result-diffs.json                    the full 473-file classification (written at logs/s44-fin10.0)
  - selfcheck/s44-determinism-before.json / -after.json  the determinism probe, which hashed only runs/, negatives/ and vectors/ non-store files
It also re-hashes the current copied bytes against the source43 manifest, to show the copy is the source44 final state apart from files rewritten after
s44-fin10.0. Writes output/selfcheck/s45-s44-arithmetic-reconciliation.json. Read-only on every source44 artifact.
Usage: python3 output/reconcile_s44_arithmetic.py
"""
import collections
import hashlib
import json
import os

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
manifest = json.load(open(OUT + "preserved/s43-final/results-manifest.json"))["files"]
rd = json.load(open(OUT + "selfcheck/s44-result-diffs.json"))
before = json.load(open(OUT + "selfcheck/s44-determinism-before.json"))["hashes"]
after_doc = json.load(open(OUT + "selfcheck/s44-determinism-after.json"))
after = after_doc["hashes"]
s43 = {r["path"]: r["sha256"] for r in manifest}


def prefix(p):
    if p.endswith(".store.json"):
        return "runs/*.store.json"
    return p.split("/")[0] + "/"


full_by_prefix = collections.Counter(prefix(p) for p in s43)
rd_differ = {r["path"]: r["class"] for r in rd["rows"]}
rd_class = collections.Counter(rd_differ.values())
full_identical = len(s43) - len(rd_differ)
subset = sorted(after)  # determinism-probe subset
subset_by_prefix = collections.Counter(prefix(p) for p in subset)
subset_identical = sum(1 for p in subset if after[p] == s43[p])
subset_differ = [p for p in subset if after[p] != s43[p]]
unstable = [p for p in subset if before.get(p) != after.get(p)]
stable_differ = [p for p in subset if before.get(p) == after.get(p) and after[p] != s43[p]]
outside_subset_differ = sorted(p for p in rd_differ if p not in after)
subset_differ_classes = collections.Counter(rd_differ.get(p, "not in s44-result-diffs rows") for p in subset_differ)
current = {}
for p, h in s43.items():
    fp = OUT + p
    current[p] = hashlib.sha256(open(fp, "rb").read()).hexdigest() if os.path.exists(fp) else None
current_identical = sum(1 for p in s43 if current[p] == s43[p])
current_vs_rd = sorted(p for p in s43 if (current[p] != s43[p]) != (p in rd_differ))
out = {
    "standing": "internal reporting consistency of my own source44 numbers; derived from retained source44 files; not a normative expected output",
    "fullComparison": {"base": "preserved/s43-final/results-manifest.json", "files": len(s43), "byPrefix": dict(full_by_prefix),
                       "differingPerS44ResultDiffs": len(rd_differ), "classCounts": dict(rd_class), "identical": full_identical,
                       "reportedByS44ResultDiffs": {"comparedFiles": rd["comparedFiles"], "differingFiles": rd["differingFiles"], "classCounts": rd["classCounts"]}},
    "determinismProbeSubset": {"scope": "runs/, negatives/, vectors/ entries of the manifest excluding *.store.json", "files": len(subset), "byPrefix": dict(subset_by_prefix),
                               "reportedHashed": after_doc["hashed"], "identicalToSource43": subset_identical, "reportedIdenticalToSource43": after_doc["identicalToSource43"],
                               "differingFromSource43": len(subset_differ), "differingClassesPerS44ResultDiffs": dict(subset_differ_classes),
                               "differsBetweenTwoSource44Executions": len(unstable), "stableButDifferentFromSource43": len(stable_differ),
                               "stableButDifferentPaths": stable_differ},
    "differingOutsideDeterminismSubset": {"count": len(outside_subset_differ), "paths": outside_subset_differ},
    "reconciliation": {
        "correctFullStatement": f"{full_identical} of {len(s43)} retained result files are byte-identical to the source43 copy; {len(rd_differ)} differ "
                                f"({rd_class.get('process-id-bearing', 0)} process-id-bearing, {rd_class.get('expected-content', 0)} expected content, "
                                f"{rd_class.get('helper-source-edited-in-source44', 0)} helper sources edited in source44)",
        "correctSubsetStatement": f"of the {len(subset)} runs/negatives/vectors non-store files hashed by the determinism probe, {subset_identical} are identical "
                                  f"and {len(subset_differ)} differ ({len(unstable)} differ between two source44 executions; {len(stable_differ)} are stable but "
                                  f"differ from source43)",
        "source44ProseError": "blind-review.md ('251 of 473 retained result files are byte-identical') paired the determinism-subset identical count (251 of 347) "
                              "with the full manifest size (473). notes/13-source44-provider-wire.md also said '251 files are byte-identical' under the 473 comparison.",
        "checks": {"subsetIdenticalEqualsReported": subset_identical == after_doc["identicalToSource43"],
                   "subsetSizeEqualsReported": len(subset) == after_doc["hashed"],
                   "fullDifferingEqualsReported": len(rd_differ) == rd["differingFiles"],
                   "fullArithmetic": full_identical + len(rd_differ) == len(s43),
                   "subsetArithmetic": subset_identical + len(subset_differ) == len(subset),
                   "differingPartition": len(subset_differ) + len(outside_subset_differ) == len(rd_differ)}},
    "currentCopiedBytes": {"identicalToSource43": current_identical, "differingFromSource43": len(s43) - current_identical,
                           "filesWhoseCurrentStatusDiffersFromS44ResultDiffs": current_vs_rd,
                           "note": "the copy includes files rewritten after logs/s44-fin10.0 (for example runs/final-custody.json at s44-fin11.0)"}}
out["result"] = "PASS" if all(out["reconciliation"]["checks"].values()) else "FAIL"
os.makedirs(OUT + "selfcheck", exist_ok=True)
json.dump(out, open(OUT + "selfcheck/s45-s44-arithmetic-reconciliation.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("reconciliation", "differingOutsideDeterminismSubset", "currentCopiedBytes", "result")}, indent=1))
