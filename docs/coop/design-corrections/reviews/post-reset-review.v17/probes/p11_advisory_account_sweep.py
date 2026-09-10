#!/usr/bin/env python
"""Sweep every item of advisory-application-account.v17.proposed.json.

For each item that pins a SOURCE file, decide whether the pin resolves against
the frozen v17 bytes and, if not, whether the item carries an explicit
historical/as-of label plus a current-source binding - the repair pattern
V16-ADV-1 asked for and that item 43 now implements.

An unresolved pin WITHOUT that labelling is the V16-ADV-1 defect recurring.
"""
import hashlib
import json
import os
import sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v17"
ACC = os.path.join(
    ROOT, "docs/coop/design-corrections/reviews/codex-post-reset.v1/"
          "advisory-application-account.v17.proposed.json")
OUT = sys.argv[1]

CONTEXT_KEYS = ("sourceCorrectionContext", "currentSource",
                "historicalSourceSubject", "historicalCurrentSourceReferences")


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


doc = json.load(open(ACC))
items = doc["items"]
rows = []
for i, it in enumerate(items):
    sc = it.get("sourceCorrection")
    if not isinstance(sc, dict) or "path" not in sc or "sha256" not in sc:
        continue
    p = os.path.join(ROOT, sc["path"])
    exists = os.path.isfile(p)
    actual = sha_file(p) if exists else None
    resolves = actual == sc["sha256"]
    ctx = {k: (k in it) for k in CONTEXT_KEYS}
    has_ctx = any(ctx.values())
    # a current binding that actually matches the frozen bytes
    cur = it.get("currentSource") or (
        it.get("sourceCorrectionContext", {}) or {}).get("currentSource")
    cur_ok = None
    if isinstance(cur, dict) and "path" in cur:
        cp = os.path.join(ROOT, cur["path"])
        cur_ok = os.path.isfile(cp) and sha_file(cp) == cur.get("sha256")
    rows.append({
        "index": i,
        "id": it.get("id"),
        "severity": it.get("originalSeverity") or it.get("severity"),
        "sourceCorrectionPath": sc["path"],
        "pinnedSha256": sc["sha256"],
        "frozenSha256": actual,
        "pinResolvesAgainstFrozen": resolves,
        "contextKeysPresent": ctx,
        "hasHistoricalContext": has_ctx,
        "currentBindingPresent": cur is not None,
        "currentBindingMatchesFrozen": cur_ok,
        "isTheV16Adv1DefectPattern": (not resolves) and not has_ctx,
    })

rep = {
    "accountPath": os.path.relpath(ACC, ROOT),
    "accountSha256": sha_file(ACC),
    "itemCount": len(items),
    "itemsWithASourceCorrectionPin": len(rows),
    "rows": rows,
    "pinsResolving": [r for r in rows if r["pinResolvesAgainstFrozen"]],
    "pinsNotResolvingButLabelledHistorical":
        [r for r in rows if not r["pinResolvesAgainstFrozen"]
         and r["hasHistoricalContext"]],
    "pinsNotResolvingAndNotLabelled":
        [r for r in rows if r["isTheV16Adv1DefectPattern"]],
}
rep["resolvingCount"] = len(rep["pinsResolving"])
rep["labelledHistoricalCount"] = len(rep["pinsNotResolvingButLabelledHistorical"])
rep["unlabelledStaleCount"] = len(rep["pinsNotResolvingAndNotLabelled"])

# severity account: original severities must be unchanged / none promoted
sev = {}
for it in items:
    s = it.get("originalSeverity") or it.get("severity")
    sev[str(s)] = sev.get(str(s), 0) + 1
rep["severityHistogram"] = sev
rep["itemsWithCurrentAssentStanding"] = sum(
    1 for it in items if "currentAssentStanding" in it)
rep["standing"] = doc.get("standing")

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("account items:", rep["itemCount"],
      "| items with a sourceCorrection pin:", rep["itemsWithASourceCorrectionPin"])
print("pins resolving against frozen bytes :", rep["resolvingCount"])
print("stale but LABELLED historical       :", rep["labelledHistoricalCount"])
print("stale and NOT labelled (V16-ADV-1)  :", rep["unlabelledStaleCount"])
print()
for r in rep["pinsNotResolvingButLabelledHistorical"]:
    print("  LABELLED  item %d %s -> %s" % (r["index"], r["id"],
                                            r["sourceCorrectionPath"]))
    print("            currentBindingMatchesFrozen:",
          r["currentBindingMatchesFrozen"])
for r in rep["pinsNotResolvingAndNotLabelled"]:
    print("  UNLABELLED item %d %s -> %s" % (r["index"], r["id"],
                                             r["sourceCorrectionPath"]))
    print("            pinned %s" % r["pinnedSha256"][:16])
    print("            frozen %s" % (r["frozenSha256"] or "")[:16])
    print("            contextKeys:", r["contextKeysPresent"])
print()
print("severity histogram:", rep["severityHistogram"])
print("items carrying currentAssentStanding:", rep["itemsWithCurrentAssentStanding"])
print("standing:", str(rep["standing"])[:300])
