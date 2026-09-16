import sys; sys.path.insert(0, "/tmp/opensip-implementation/m1-report-projection-review-02/work/probes")
from common import *
R = {}
fit = copy.deepcopy(B["fit-run"])
R["base-fit-run"] = admit_doc(fit)
print(json.dumps(fit["envelope"]["termination"]), json.dumps(fit["envelope"]["advisoryReport"]["candidateList"]["context"])[:600])
# Q1 fit parity: truncated candidate page (nextCursor, totalItems > listed)
d = copy.deepcopy(fit); c = d["envelope"]["advisoryReport"]["candidateList"]["context"]
c["truncated"] = True; c["totalItems"] = len(d["envelope"]["advisoryReport"]["candidateList"]["candidates"]) + 500; c["nextCursor"] = "q3." + "a"*64 + "." + "b"*64 + ".1"
R["Q1-fit-truncated-candidate-page-envelope"] = admit_env(d["envelope"], "fit")
R["Q1-fit-truncated-candidate-page-report"] = admit_doc(d)
# Q2 fit candidate step failure after commit, per contract 3.5 (operational-failed, DELIVERY.REQUIRED_FAILED, runId, no advisoryReport)
d = copy.deepcopy(fit); e = d["envelope"]; rid = e["run"]["runId"]
e.pop("advisoryReport")
e["termination"] = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required", "runId": rid, "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT"}}
e["exitCode"] = 4
R["Q2a-fit-post-commit-candidate-failure-kind-run"] = admit_env(e, "fit")
print("failure base termination:", json.dumps(B["review-brief-failure"]["envelope"]["termination"]), sorted(B["review-brief-failure"]["envelope"]))
# Q2b same as kind=failure
e2 = copy.deepcopy(B["review-brief-failure"]["envelope"]); e2["termination"] = dict(e["termination"]); e2["exitCode"] = 4
R["Q2b-fit-post-commit-candidate-failure-kind-failure"] = admit_env(e2, "fit")
# Q3 evidence: byte-budget omission claimed on a tiny document (maximality not verifiable, not disclosed as host assertion)
d = copy.deepcopy(B["audit-full"]); ev = d["panels"]["evidence"]["data"]; n = len(ev["entries"])
ev["entriesProjection"] = {"total": n + 3000, "omitted": 3000, "omissionCause": "byte-budget"}
R["Q3-evidence-byte-budget-on-small-document"] = admit_doc(d)
R["Q3-document-bytes"] = len(chk.canonical(d))
# Q4 graph slot: byte-budget-reduced page size on a small document
d = copy.deepcopy(B["audit-full"]); s = d["panels"]["graph"]["data"]["slots"][0]
s["request"]["page"]["size"] = 50; s["hostProjection"]["pageSizeCause"] = "byte-budget-reduced"
R["Q4-graph-byte-budget-reduced-on-small-document"] = admit_doc(d)
# Q5 rows-match-request-parameters: neighbor row resolution vs minResolution
d = copy.deepcopy(B["audit-full"])
for i, s in enumerate(d["panels"]["graph"]["data"]["slots"]):
    if s["response"]["operation"] == "graph.neighbors" and s["response"]["items"]:
        print("neighbors params", json.dumps(s["request"]["params"])[:400], "row resolution", s["response"]["items"][0]["resolution"])
        s["response"]["items"][0]["resolution"] = "unresolved"
        s["request"]["params"]["minResolution"] = "resolved"
        R["Q5-neighbor-row-below-minResolution"] = admit_doc(d)
        break
# Q6 command relabel: audit envelope embedded as analyze
d = copy.deepcopy(B["audit-full"]); d["command"] = "analyze"
d["supportedReportViews"] = ["overview", "findings", "evidence", "comparison", "catalog", "graph", "symbol-detail"]
d["featureStates"] = next(b for b in ctx.schema["allOf"] if b.get("if", {}).get("properties", {}).get("command", {}).get("const") == "analyze")["then"]["properties"]["featureStates"]["const"]
d["panels"].pop("history")
R["Q6-audit-envelope-labelled-analyze"] = admit_doc(d)
# Q7 deep nesting code determinism
base = chk.canonical(B["audit-full"])
deep39 = base[:-1] + b',"x":' + b"[" * 39 + b"]" * 39 + b"}"
R["Q7a-nesting-39"] = admit_doc(deep39)
deep = base[:-1] + b',"x":' + b"[" * 200000 + b"]" * 200000 + b"}"
R["Q7b-nesting-200000"] = admit_doc(deep)
# Q8 subject index row bound arithmetic
ep = {"universe": "a"*64, "kind": "file", "nativeSubjectId": "a"}
R["Q8-min-endpoint-bytes"] = len(chk.canonical(ep))
R["Q8-min-index-row-bytes"] = len(chk.canonical({"subjectId": chk.subject_id(ctx, ep), "endpoint": ep}))
R["Q8-schema-subjectIndex-maxItems"] = ctx.schema["$defs"]["GraphPanelV1"]["properties"]["subjectIndex"].get("maxItems")
g = documents["urn:opensip:product-v1:workflows:evaluator3:graph-query:3"]["$defs"]
R["Q8-GraphPathRow-nodes-maxItems"] = g["GraphPathRow"]["properties"]["nodes"].get("maxItems")
# Q9 root allowance
d = B["audit-full"]
R["Q9-root-overhead-bytes"] = len(chk.canonical(d)) - len(chk.canonical(d["envelope"])) - len(chk.canonical(d["panels"]))
R["Q9-featureStates-bytes"] = len(chk.canonical(d["featureStates"]))
print(json.dumps(R, indent=1)); json.dump(R, open("f_probes.json", "w"), indent=1)
