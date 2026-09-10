"""Run every vector set and emit vectors/summary.json."""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "vectors")
PY = "/tmp/opensip-architecture-review-env/bin/python"
KIT = "/tmp/opensip-design-corrections/consumer-b.v4/subject"

SETS = [("v1_admission", "v1-admission.json"), ("v2_runs", "v2-runs.json"),
        ("v3_workflows", "v3-workflows.json"), ("v4_audit", "v4-audit.json"),
        ("v5_laws", "v5-law-checks.json"), ("v6_gaps", "v6-gaps.json")]

# manifest verification
man = json.load(open(os.path.join(KIT, "consumer-input-manifest.json")))
ver = {"parentSubjectSha256": man["parentSubjectSha256"], "files": len(man["files"]),
       "verified": 0, "mismatched": [], "missing": [], "unlisted": []}
for f in man["files"]:
    p = os.path.join(KIT, f["path"])
    if not os.path.exists(p):
        ver["missing"].append(f["path"])
        continue
    b = open(p, "rb").read()
    if hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"]:
        ver["verified"] += 1
    else:
        ver["mismatched"].append(f["path"])
listed = {f["path"] for f in man["files"]} | {"consumer-input-manifest.json"}
for root, _, files in os.walk(KIT):
    for x in files:
        rp = os.path.relpath(os.path.join(root, x), KIT)
        if rp not in listed:
            ver["unlisted"].append(rp)
ver["allVerified"] = (ver["verified"] == len(man["files"]) and not ver["mismatched"]
                      and not ver["missing"] and not ver["unlisted"])

summary = {"inputVerification": ver, "sets": {}, "totals": {}}
tot = {"positive": 0, "negative": 0, "negativeRefused": 0, "verification": 0,
       "verificationHolds": 0, "advisory": 0, "gaps": 0}
for mod, fname in SETS:
    r = subprocess.run([PY, "-I", "-B", os.path.join(HERE, mod + ".py")],
                       capture_output=True)
    if r.returncode != 0:
        summary["sets"][mod] = {"error": r.stderr.decode()[-2000:]}
        continue
    open(os.path.join(OUT, fname), "wb").write(r.stdout)
    data = json.loads(r.stdout)
    s = {"file": fname, "entries": len(data)}
    if mod == "v6_gaps":
        s["bySeverity"] = {}
        for e in data:
            s["bySeverity"][e["severity"]] = s["bySeverity"].get(e["severity"], 0) + 1
        tot["gaps"] += len(data)
    else:
        for e in data:
            k = e.get("kind", "positive")
            tot[k] = tot.get(k, 0) + 1
            if k == "negative" and e.get("outcome") == "refused":
                tot["negativeRefused"] += 1
            if k == "verification" and e.get("claimHolds"):
                tot["verificationHolds"] += 1
        s["kinds"] = {}
        for e in data:
            k = e.get("kind", "positive")
            s["kinds"][k] = s["kinds"].get(k, 0) + 1
    summary["sets"][mod] = s
summary["totals"] = tot
summary["allNegativesRefused"] = tot["negative"] == tot["negativeRefused"]
print(json.dumps(summary, indent=1))
