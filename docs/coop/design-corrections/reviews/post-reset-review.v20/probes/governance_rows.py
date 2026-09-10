"""Count the governance row families exactly, and check their routing-only standing.

Carry-forward/routing is not a fresh readiness grade, so this records for each family
whether any row claims application/qualification by this review.
"""
import json
import os
import re
import sys

ROOT = sys.argv[1]
DC = os.path.join(ROOT, "docs/coop/design-corrections")
out = {}

cw = json.load(open(os.path.join(DC, "correction-crosswalk.proposed.json")))
out["arRows"] = {
    "count": len(cw["items"]),
    "ids": [i.get("id") for i in cw["items"]],
    "standing": cw.get("standing"),
}

ev = json.load(open(os.path.join(DC,
                                 "evaluation-residual-dispositions.proposed.json")))
out["evaluationResidualRows"] = {
    "count": len(ev["items"]),
    "ids": [i.get("id") for i in ev["items"]][:40],
    "standing": ev.get("standing"),
}

md = open(os.path.join(DC, "inherited-residuals.proposed.md")).read()
rows = [l for l in md.splitlines()
        if l.startswith("|") and not re.match(r"^\|[\s\-|]+\|$", l)]
body = [l for l in rows if not l.startswith("| Residual")]
out["inheritedResidualRows"] = {
    "tablePipeLines": len(rows),
    "bodyRows": len(body),
    "firstIds": [l.split("|")[1].strip().split()[0] for l in body][:40],
}

gates = json.load(open(os.path.join(DC, "qualification-gates.proposed.json")))
out["qualificationGates"] = {
    "count": len(gates["items"]),
    "standing": gates.get("standing"),
    "platformFamilies": gates.get("platformFamilies"),
    "anyPerformed": any(
        str(i.get("status", "")).lower() not in ("", "unperformed", "not-performed")
        for i in gates["items"]),
    "statuses": sorted({str(i.get("status")) for i in gates["items"]}),
}

src = json.load(open(os.path.join(DC, "inherited-row-sources.proposed.json")))
out["inheritedRowSources"] = {
    "count": len(src["records"]),
    "ids": [r.get("id") or r.get("row") for r in src["records"]],
}

# FW rows: locate wherever they live
fw = {}
for dirpath, _d, files in os.walk(ROOT):
    if "/reviews/" in dirpath:
        continue
    for fn in files:
        if not fn.endswith((".json", ".md")):
            continue
        p = os.path.join(dirpath, fn)
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        ids = set(re.findall(r"\bFW-\d+\b", t))
        if len(ids) >= 5:
            fw[os.path.relpath(p, ROOT)] = sorted(ids, key=lambda s: int(
                s.split("-")[1]))
out["fwRowSources"] = {k: {"count": len(v), "ids": v} for k, v in fw.items()}

# scoped review owners
so = {}
for dirpath, _d, files in os.walk(DC):
    if "/reviews/" in dirpath:
        continue
    for fn in files:
        p = os.path.join(dirpath, fn)
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if "scopedReviewOwner" in t or "scoped review owner" in t.lower():
            so[os.path.relpath(p, ROOT)] = t.lower().count("scoped review owner") \
                + t.count("scopedReviewOwner")
out["scopedReviewOwnerMentions"] = so

print(json.dumps(out, indent=2)[:6000])
