"""Read-only summary of vectors/graph-query.json#/source43ReAudit for the review (prints; writes nothing).
Usage: python3 tools/summarize_s43_query.py
"""
import json

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/"
gq = json.load(open(OUT + "vectors/graph-query.json"))
ra = gq["source43ReAudit"]
print("counts", gq["counts"], "failures", gq["assertionFailures"])
print("contract", ra["contract"])
for row in ra["lawAudit"]:
    print("LAW", row["selector"], "|", row["unchangedHelper"])
for p in ra["prePost"]:
    print("PRE/POST", p["vector"], p["expected"], "| before:", json.dumps(p["unchangedSource42v3Helper"])[:260], "| after:", json.dumps(p["correctedHelper"])[:200])
for pc in ra["preconditionVectors"]:
    print("PRECONDITION", pc["vector"], pc["firstRefusal"], pc["pass"])
for t in ra["typedOutcomeControls"]:
    print("TYPED", t["report"]["firstRefusal"], t["expected"], t["observed"])
print("tampered close_run", ra["tamperedStoreCloseRun"])
print("endpoint", ra["endpointControls"])
