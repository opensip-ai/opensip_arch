"""Explain every retained result file whose bytes differ from the source43.v1 copy (preserved/s43-final/results-manifest.json).

Classes, tested in this order:
  runtime-path-only   mapping the runtime root text consumer-b.v24-source44.v1 back to consumer-b.v24-source43.v1 reproduces the source43 sha256;
  process-id-bearing  the JSON carries a "pid" member (the id of the replay subprocess), so no two executions can produce equal bytes;
                      selfcheck/s44-determinism-after.json shows whether the file also differs between two source44 executions;
  expected-content    phase-3 traces (HC-57/HC-58), the kit census and its consumers, custody reports;
  unexpected          anything else.
Result equality of the re-executed closures is checked independently of bytes: the run id of every claimed positive against the preserved source43
review, and from-scratch agreement with each Run's retained replay result (runs/from-scratch.summary.json everyResultMatchesOriginal).
Writes selfcheck/s44-result-diffs.json and exits 1 on an unexpected difference, a run-id difference or a from-scratch disagreement.
The first version of this file (never executed) treated every non-path difference as content; it was rewritten after runs/ts-pass.replay-export.json
was seen to carry "pid".
"""
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
NEW, OLD = b"consumer-b.v24-source44.v1", b"consumer-b.v24-source43.v1"
EXPECTED_REASON = {"traces/": "phase 3 corrected under the source44 owners (HC-57, HC-58)",
                   "vectors/reference-census.json": "the census walks every kit JSON document; three were added and four JSON documents changed",
                   "vectors/retention-negatives.json": "consumes the census",
                   "vectors/phase0-custody.json": "source44 custody rows", "runs/final-custody.json": "source44 custody"}


def has_pid(node):
    if isinstance(node, dict):
        return "pid" in node or any(has_pid(v) for v in node.values())
    if isinstance(node, list):
        return any(has_pid(v) for v in node)
    return False


manifest = json.load(open(OUT + "preserved/s43-final/results-manifest.json"))["files"]
# Own tool error in the first run (logs/s44-diff.0.result_diffs_s44.log): the results manifest also hashed the helper sources that live in vectors/, and
# the four I edited in source44 were reported as unexpected. They are classified by the provenance helper census instead.
helper_status = {r["file"]: r["status"] for r in json.load(open(OUT + "selfcheck/s44-provenance.json"))["helperBytes"]}
det_path = OUT + "selfcheck/s44-determinism-after.json"
det = json.load(open(det_path)) if os.path.exists(det_path) else None
unstable = set(det["differsBetweenTwoSource44Executions"]) if det else set()
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
    if r["path"].endswith(".py"):
        status = helper_status.get(r["path"], "not in the helper census")
        row["class"], row["helperStatus"] = ("helper-source-edited-in-source44" if status.startswith(("edited in source44", "new in source44")) else "unexpected"), status
        if row["class"] == "unexpected":
            unexpected.append(r["path"])
    elif hashlib.sha256(b.replace(NEW, OLD)).hexdigest() == r["sha256"]:
        row["class"] = "runtime-path-only"
    else:
        try:
            doc = json.loads(b)
        except ValueError:
            doc = None
        reason = next((v for k, v in EXPECTED_REASON.items() if r["path"].startswith(k)), None)
        if doc is not None and has_pid(doc):
            row["class"] = "process-id-bearing"
            row["differsBetweenTwoSource44Executions"] = (r["path"] in unstable) if det else "not measured"
        elif reason:
            row["class"], row["reason"] = "expected-content", reason
        else:
            row["class"] = "unexpected"
            unexpected.append(r["path"])
    rows.append(row)
review43 = json.load(open(OUT + "preserved/s43-final/blind-review.json"))
old_ids = {c["run"]: c["runId"] for c in review43["claimedCompletePositives"]}
new_ids = {run: json.load(open(OUT + f"runs/{run}.replay.fromscratch.json"))["runId"] for run in old_ids}
id_diffs = {k: [old_ids[k], new_ids[k]] for k in old_ids if old_ids[k] != new_ids[k]}
fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
counts = {}
for x in rows:
    counts[x["class"]] = counts.get(x["class"], 0) + 1
pid_rows = [x for x in rows if x["class"] == "process-id-bearing"]
out = {"comparedFiles": len(manifest), "differingFiles": len(rows), "classCounts": counts, "rows": rows, "unexpected": unexpected,
       "processIdBearingAlsoUnstableWithinSource44": (all(x["differsBetweenTwoSource44Executions"] is True for x in pid_rows) if det else "not measured"),
       "claimedPositiveRunIdsCompared": len(old_ids), "runIdDifferences": id_diffs,
       "fromScratchEveryResultMatchesRetainedReplay": fs.get("everyResultMatchesOriginal"),
       "determinismProbe": "selfcheck/s44-determinism-after.json" if det else None}
out["result"] = "PASS" if not unexpected and not id_diffs and fs.get("everyResultMatchesOriginal") is True else "FAIL"
json.dump(out, open(OUT + "selfcheck/s44-result-diffs.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
sys.exit(0 if out["result"] == "PASS" else 1)
