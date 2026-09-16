"""Final20 multistep availability / indeterminate proofs: what is actually retained? READ-ONLY."""
import hashlib
import json
import re
from pathlib import Path

C20 = Path("/tmp/opensip-design-corrections/consumer-b.v20")
V = C20 / "output/vectors"
out = {"standing": "READ-ONLY inspection of final20 retained workflow/availability artifacts."}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# Which retained artifacts mention availability / multistep / indeterminate aggregation?
hits = []
for p in sorted(V.rglob("*.json")):
    txt = p.read_text()
    row = {"path": str(p.relative_to(C20)), "sha256": sha(p),
           "availability": len(re.findall(r"availability", txt)),
           "multiStep": len(re.findall(r"multi[- ]?step|multistep", txt, re.I)),
           "indeterminate": len(re.findall(r"indeterminate", txt)),
           "terminationClass": len(re.findall(r"terminationClass|termination", txt))}
    if row["availability"] or row["multiStep"]:
        hits.append(row)
out["artifactsMentioningAvailabilityOrMultistep"] = hits

# The workflow projection vector, if retained.
for name in ("phase8-all.json", "phase7-standing-rules.json"):
    p = V / name
    if not p.is_file():
        continue
    d = json.loads(p.read_text())
    txt = json.dumps(d)
    out[name] = {
        "sha256": sha(p),
        "topKeys": list(d.keys()) if isinstance(d, dict) else "list",
        "availabilityMentions": len(re.findall(r"availability", txt)),
        "stepCountMentions": sorted(set(re.findall(r"step1|single-step|singleStep", txt))),
        "hasMultistepAvailability": bool(re.search(r"multi[- ]?step[^\"]{0,60}availability", txt, re.I)),
    }

# Does any retained record carry a workflow aggregate termination with proofs?
agg = []
for p in sorted(V.rglob("*.json")):
    txt = p.read_text()
    if re.search(r"aggregateTermination|aggregate_termination", txt):
        agg.append({"path": str(p.relative_to(C20)), "sha256": sha(p),
                    "occurrences": len(re.findall(r"aggregateTermination|aggregate_termination", txt))})
out["artifactsWithAggregateTermination"] = agg

# The consumer's own verify-all and requirement status headline numbers.
va = C20 / "output/verify-all.json"
if va.is_file():
    d = json.loads(va.read_text())
    out["verifyAll"] = {"sha256": sha(va),
                        "topKeys": list(d.keys()) if isinstance(d, dict) else "list",
                        "head": json.dumps(d)[:900]}
rs = C20 / "output/requirement-status.json"
if rs.is_file():
    d = json.loads(rs.read_text())
    out["requirementStatusSha256"] = sha(rs)
    if isinstance(d, dict):
        out["requirementStatusTopKeys"] = list(d.keys())
        for k, v in d.items():
            if isinstance(v, list):
                out["requirementStatusListSizes"] = out.get("requirementStatusListSizes", {})
                out["requirementStatusListSizes"][k] = len(v)
print(json.dumps(out, indent=2, default=str))
