import sys; sys.path.insert(0, "/tmp/opensip-implementation/m1-report-projection-review-02/work/probes")
from common import *
R = {}
m = ctx.builder.material(); audit = B["audit-full"]
worst_doc = json.loads(chk.apply_ops(ctx, audit, [{"op": "x-worst-neighbor-slot", "rows": 100}]))
wslot = worst_doc["panels"]["graph"]["data"]["slots"][1]
src = ctx.builder.budget_sources(B, m)
src["evidence"]["entries"] = src["evidence"]["entries"][:10]; src["history"]["findings"] = src["history"]["findings"][:10]
src["graph"]["planned"] = [wslot, copy.deepcopy(audit["panels"]["graph"]["data"]["slots"][0])]
p = chk.project_exploration(ctx, src, ctx.builder.subject_index)
s = p["graph"]["data"]["slots"][0]
c = s["response"]["context"]
R["planned-response-items"] = len(wslot["response"]["items"])
R["planned-context"] = {k: wslot["response"]["context"].get(k) for k in ("truncated", "totalItems", "nextCursor", "produced")}
R["projected-page-size"] = s["request"]["page"]["size"]
R["projected-items"] = len(s["response"]["items"])
R["projected-context"] = {k: c.get(k) for k in ("truncated", "totalItems", "nextCursor", "produced")}
R["projected-context-keys"] = sorted(c)
R["projected-hostProjection"] = s["hostProjection"]
# Standalone mutation: cut a complete audit slot's items without changing context -> admission result
d = copy.deepcopy(audit)
for sl in d["panels"]["graph"]["data"]["slots"]:
    if len(sl["response"]["items"]) >= 2 and "nextCursor" not in sl["response"]["context"]:
        before = len(sl["response"]["items"]); sl["response"]["items"] = sl["response"]["items"][:1]
        d["panels"]["graph"]["data"]["subjectIndex"] = ctx.builder.subject_index(d["panels"]["graph"]["data"]["slots"])
        R["mutation-cut-items"] = {"before": before, "after": 1, "context": {k: sl["response"]["context"].get(k) for k in ("truncated", "totalItems")}, "hostProjection": sl["hostProjection"], "admission": admit_doc(d)}
        break
print(json.dumps(R, indent=1)); json.dump(R, open("j_reduced_slot.json", "w"), indent=1)
