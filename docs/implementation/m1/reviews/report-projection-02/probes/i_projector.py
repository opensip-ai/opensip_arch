import sys; sys.path.insert(0, "/tmp/opensip-implementation/m1-report-projection-review-02/work/probes")
from common import *
R = {}
m = ctx.builder.material()
audit = B["audit-full"]
# S1: evidence byte-prefix path of the law (cap lowered on a context copy to exercise the law, not the constant)
src = ctx.builder.budget_sources(B, m)
src["history"]["findings"] = []
src["graph"]["planned"] = [copy.deepcopy(audit["panels"]["graph"]["data"]["slots"][0])]
entry_bytes = len(chk.canonical(src["evidence"]["entries"][0]))
small = chk.Context(); small.__dict__.update(ctx.__dict__); small.budget = dict(ctx.budget, explorationMaxCanonicalBytes=600000)
p1 = chk.project_exploration(small, src, ctx.builder.subject_index)
p1b = chk.project_exploration(small, src, ctx.builder.subject_index)
ev = p1["evidence"]
R["S1-entryBytes"] = entry_bytes
R["S1-deterministic"] = chk.canonical(p1) == chk.canonical(p1b)
R["S1-evidence"] = ev["data"]["entriesProjection"] if ev["state"] == "present" else ev
R["S1-graph-state"] = p1["graph"]["state"]; R["S1-history-state"] = p1["history"]["state"]
if ev["state"] == "present":
    n = len(ev["data"]["entries"]); bigger = copy.deepcopy(p1); bigger["evidence"]["data"]["entries"] = src["evidence"]["entries"][:n + 1]
    R["S1-maximal"] = len(chk.canonical(bigger)) > 600000
doc = copy.deepcopy(audit); doc["panels"] = p1
R["S1-admit-under-real-cap"] = admit_doc(doc)
R["S1-order-note"] = "graph/history present after evidence byte-budget prefix" if p1["graph"]["state"] == "present" or p1["history"]["state"] == "present" else "later panels omitted"
# S2: graph page-size reduction under the real cap with a worst-case neighbor slot of 100 rows
worst_doc = json.loads(chk.apply_ops(ctx, audit, [{"op": "x-worst-neighbor-slot", "rows": 100}]))
wslot = worst_doc["panels"]["graph"]["data"]["slots"][1]
src2 = ctx.builder.budget_sources(B, m)
src2["evidence"]["entries"] = src2["evidence"]["entries"][:10]
src2["history"]["findings"] = src2["history"]["findings"][:10]
src2["graph"]["planned"] = [wslot, copy.deepcopy(audit["panels"]["graph"]["data"]["slots"][0])]
p2 = chk.project_exploration(ctx, src2, ctx.builder.subject_index)
g = p2["graph"]
R["S2-graph"] = {"state": g["state"], "slots": [(s["request"]["page"]["size"], s["hostProjection"]["pageSizeCause"], len(s["response"]["items"])) for s in g["data"]["slots"]] if g["state"] == "present" else None,
                 "slotsProjection": g["data"]["slotsProjection"] if g["state"] == "present" else None}
R["S2-panelsBytes"] = len(chk.canonical(p2))
doc2 = copy.deepcopy(audit); doc2["panels"] = p2
R["S2-admit"] = admit_doc(doc2)
print(json.dumps(R, indent=1)); json.dump(R, open("i_projector.json", "w"), indent=1)
