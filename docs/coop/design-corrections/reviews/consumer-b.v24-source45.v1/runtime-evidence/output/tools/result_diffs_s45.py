"""Explain every retained result file whose bytes differ from the source44.v1 copy (preserved/s44-final/results-manifest.json, 546 files).

Classes, tested in this order:
  helper-source-edited-in-source45  a *.py in the manifest whose status in selfcheck/s45-provenance.json is edited or new in source45;
  runtime-path-only                 mapping consumer-b.v24-source45.v1 back to consumer-b.v24-source44.v1 reproduces the source44 sha256;
  process-id-bearing                the JSON carries a "pid" member (replay subprocess id). My source44 determinism probe measured these files differing
                                    between two identical executions (selfcheck/s44-determinism-after.json);
  expected-content                  phase-3 traces (HC-60), the kit census and its consumer, custody reports, and the source44/source45 selfcheck records
                                    rewritten here;
  unexpected                        anything else.
Result equality of the re-executed closures, independent of bytes: the run id of every claimed positive against the preserved source44 review, and
from-scratch agreement with each Run's retained replay result. Writes selfcheck/s45-result-diffs.json and exits 1 on an unexpected difference, a
run-id difference or a from-scratch disagreement. It reports counts only from the file set it compares.
"""
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
NEW, OLD = b"consumer-b.v24-source45.v1", b"consumer-b.v24-source44.v1"
EXPECTED_REASON = {"traces/": "phase 3 re-executed under the source45 owners (HC-60)",
                   "vectors/reference-census.json": "the census walks every kit JSON document; two JSON documents changed",
                   "vectors/retention-negatives.json": "consumes the census",
                   "vectors/phase0-custody.json": "source45 custody rows", "runs/final-custody.json": "source45 custody"}


def has_pid(node):
    if isinstance(node, dict):
        return "pid" in node or any(has_pid(v) for v in node.values())
    if isinstance(node, list):
        return any(has_pid(v) for v in node)
    return False


manifest = json.load(open(OUT + "preserved/s44-final/results-manifest.json"))["files"]
helper_status = {r["file"]: r["status"] for r in json.load(open(OUT + "selfcheck/s45-provenance.json"))["helperBytes"]}
rows, unexpected = [], []
for r in manifest:
    p = OUT + r["path"]
    if not os.path.exists(p):
        rows.append({"path": r["path"], "class": "missing"})
        unexpected.append(r["path"])
        continue
    b = open(p, "rb").read()
    if hashlib.sha256(b).hexdigest() == r["sha256"]:
        continue
    row = {"path": r["path"]}
    # Own tool error in the first run (logs/s45-cp.7.result_diffs_s45.log): helper sources were tested against the edited/new census status before the
    # root mapping. The source44 results manifest holds pre-rebind bytes, so the rebound-only vectors/*.py files were reported as unexpected.
    if hashlib.sha256(b.replace(NEW, OLD)).hexdigest() == r["sha256"]:
        row["class"] = "runtime-path-only"
    elif r["path"].endswith(".py"):
        status = helper_status.get(r["path"], "not in the helper census")
        row["class"], row["helperStatus"] = ("helper-source-edited-in-source45" if status.startswith(("edited in source45", "new in source45")) else "unexpected"), status
        if row["class"] == "unexpected":
            unexpected.append(r["path"])
    else:
        try:
            doc = json.loads(b)
        except ValueError:
            doc = None
        reason = next((v for k, v in EXPECTED_REASON.items() if r["path"].startswith(k)), None)
        if doc is not None and has_pid(doc):
            row["class"] = "process-id-bearing"
        elif reason:
            row["class"], row["reason"] = "expected-content", reason
        else:
            row["class"] = "unexpected"
            unexpected.append(r["path"])
    rows.append(row)
review44 = json.load(open(OUT + "preserved/s44-final/blind-review.json"))
old_ids = {c["run"]: c["runId"] for c in review44["claimedCompletePositives"]}
new_ids = {run: json.load(open(OUT + f"runs/{run}.replay.fromscratch.json"))["runId"] for run in old_ids}
id_diffs = {k: [old_ids[k], new_ids[k]] for k in old_ids if old_ids[k] != new_ids[k]}
fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
counts = {}
for x in rows:
    counts[x["class"]] = counts.get(x["class"], 0) + 1
out = {"base": "preserved/s44-final/results-manifest.json", "comparedFiles": len(manifest), "identicalFiles": len(manifest) - len(rows),
       "differingFiles": len(rows), "classCounts": counts, "rows": rows, "unexpected": unexpected,
       "claimedPositiveRunIdsCompared": len(old_ids), "runIdDifferences": id_diffs,
       "fromScratchEveryResultMatchesRetainedReplay": fs.get("everyResultMatchesOriginal"),
       "processIdNondeterminismEvidence": "selfcheck/s44-determinism-after.json (source44 measurement, reused)"}
out["result"] = "PASS" if not unexpected and not id_diffs and fs.get("everyResultMatchesOriginal") is True else "FAIL"
json.dump(out, open(OUT + "selfcheck/s45-result-diffs.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
sys.exit(0 if out["result"] == "PASS" else 1)
