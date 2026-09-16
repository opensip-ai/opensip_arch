import sys; sys.path.insert(0, "/tmp/opensip-implementation/m1-report-projection-review-02/work/probes")
from common import *
R = {}
fit = copy.deepcopy(B["fit-run"]); rid = fit["envelope"]["run"]["runId"]
detail = {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT", "remedy": "re-run the fit report", "subject": rid}
term = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required", "runId": rid, "domainDetail": detail}
# Q2a kind=run, no advisoryReport, post-commit candidate failure (contract 3.5 row 3)
e = copy.deepcopy(fit["envelope"]); e.pop("advisoryReport"); e["termination"] = dict(term); e["exitCode"] = 4
R["Q2a-fit-post-commit-failure-kind-run"] = admit_env(e, "fit")
# Q2b kind=failure with runId
f = copy.deepcopy(B["review-brief-failure"]["envelope"]); f["termination"] = dict(term); f["exitCode"] = 4
f["errors"] = [{"code": "DELIVERY.REQUIRED_FAILED", "detail": detail}] if False else f["errors"]
R["Q2b-fit-post-commit-failure-kind-failure"] = admit_env(f, "fit")
print("failure errors sample:", json.dumps(B["review-brief-failure"]["envelope"]["errors"])[:400])
# Q2c fit kind=run policy-failed with advisoryReport (existing accepted case) vs analysis indeterminate
e = copy.deepcopy(fit["envelope"]); e["termination"] = {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"], "runId": rid}; e["exitCode"] = 3
R["Q2c-fit-indeterminate-with-carrier"] = admit_env(e, "fit")
# Q13 path row internal consistency: hopCount/nodes/edges mismatch
d = copy.deepcopy(B["audit-full"]); done = False
for s in d["panels"]["graph"]["data"]["slots"]:
    if s["response"]["operation"] == "graph.path" and s["response"]["items"]:
        row = s["response"]["items"][0]
        print("path row", json.dumps(row)[:500], "params", json.dumps(s["request"]["params"])[:300])
        extra = {"universe": row["start"]["universe"], "kind": "file", "nativeSubjectId": "src/injected.ts"}
        row["nodes"] = row["nodes"] + [extra]
        d["panels"]["graph"]["data"]["subjectIndex"] = ctx.builder.subject_index(d["panels"]["graph"]["data"]["slots"])
        R["Q13-path-row-node-not-on-any-edge"] = admit_doc(d); done = True
        break
R["Q13-ran"] = done
g = documents["urn:opensip:product-v1:workflows:evaluator3:graph-query:3"]["$defs"]
R["GraphPathRow"] = json.dumps(g["GraphPathRow"])[:900]
print(json.dumps(R, indent=1)); json.dump(R, open("g_probes.json", "w"), indent=1)
