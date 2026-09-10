#!/usr/bin/env python3
import json
from pathlib import Path

root = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/run")
adm = json.loads((root / "admission-results.json").read_text())
inv = json.loads((root / "producing-law-inventory.json").read_text())
print("=== graphs ===")
for g in adm:
    pl = g.get("producingLaw") or {}
    rp = g.get("replay") if isinstance(g.get("replay"), dict) else {}
    print(g["graph"], "overall", g["verdict"], "struct", g.get("structuralVerdict"), "replay", rp.get("status"))
    print("  first", (g.get("firstRefusal") or {}).get("code"))
    print(
        "  producing",
        {k: pl.get(k) for k in ("assertionCount", "executedPass", "executedFail", "notReached", "applicableCount", "inapplicableCount")},
    )
    print("  mismatches", rp.get("mismatches"))
    cmp = rp.get("comparison") or {}
    print("  proof", cmp.get("derivedProofSha256"), "claimed", cmp.get("claimedProofSha256"), "equal", cmp.get("proofCEqual"))
    print("  verdict", cmp.get("derivedVerdict"), "vs", cmp.get("claimedVerdict"))
    print("  subjects", rp.get("derivedSubjects"))
    print("  enclosing", rp.get("derivedEnclosing"))
for name, asserts in inv.get("assertionsByGraph", {}).items():
    print("\n==", name, "assertions", len(asserts))
    by_doc = {}
    by_status = {}
    for a in asserts:
        by_doc.setdefault(a["document"], [0, 0, 0])
        if a["status"] == "executed-pass":
            by_doc[a["document"]][0] += 1
        elif a["status"] == "executed-fail":
            by_doc[a["document"]][1] += 1
        else:
            by_doc[a["document"]][2] += 1
        by_status[a["status"]] = by_status.get(a["status"], 0) + 1
        if not a.get("applicable"):
            by_status["inapplicable"] = by_status.get("inapplicable", 0) + 1
    print("  by status", by_status)
    print("  by doc pass/fail/nr", by_doc)
    for a in asserts:
        flag = "" if a.get("applicable") else " [N/A]"
        print("   ", a["id"], a["status"] + flag, "field=" + str(a.get("field")))
