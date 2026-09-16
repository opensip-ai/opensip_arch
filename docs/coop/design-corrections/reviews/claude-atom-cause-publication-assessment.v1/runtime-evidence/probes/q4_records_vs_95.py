"""Are the disputed consumer/reference records §9.5-SHAPE-legal, differing only in cause CONTENT?

Uses the preserved root derivation from the prior diagnosis. No re-derivation, no reference Python
loaded, no consumer contact. READ-ONLY.
"""
import json
from pathlib import Path

D = Path("/tmp/opensip-design-corrections/root-blind20-proof-differences33.v1")
out = {"standing": "READ-ONLY. Preserved root-derived proofs; shape-tested against composition "
                   "section 9.5 items 1-3 as published."}

FIELDS = {"source", "cause", "subjectId", "predicateId", "inputRefs", "evidenceKind",
          "nativeCause", "universe"}


def shape_ok(rec):
    """Section 9.5 line 151: the record is exactly these eight fields."""
    return set(rec) == FIELDS


def channel(rec, atom_ei_domains):
    """Which published channel could have produced this record's inputRefs?"""
    doms = sorted({r["domain"] for r in rec.get("inputRefs") or []})
    n = len(rec.get("inputRefs") or [])
    if n == 1 and doms == ["coverage"]:
        return "9.5-item-3 (per-Coverage entry.deficiency)"
    if doms == atom_ei_domains:
        return "9.5-item-1 or -2 (atomEI)"
    return "other/unclassified"


for run in ("syntax-code", "rust-partial"):
    cons = json.loads((D / run / "consumer-proof.json").read_text())
    ref = json.loads((D / run / "reference-proof.json").read_text())
    rows = []
    for cr, rr in zip(cons["ruleResults"], ref["ruleResults"]):
        ck = {json.dumps(x, sort_keys=True) for x in cr["deficiencies"]}
        rk = {json.dumps(x, sort_keys=True) for x in rr["deficiencies"]}
        only_c = [json.loads(x) for x in sorted(ck - rk)]
        only_r = [json.loads(x) for x in sorted(rk - ck)]
        if not only_c and not only_r:
            continue
        # atomEI domain signature = the widest inputRefs domain set seen on shared members
        shared = [json.loads(x) for x in sorted(ck & rk)]
        ei = []
        for s in shared + only_c + only_r:
            doms = sorted({r["domain"] for r in s.get("inputRefs") or []})
            if len(doms) > len(ei):
                ei = doms
        rows.append({
            "ruleId": cr["ruleId"],
            "atomEIDomainSignature": ei,
            "consumerOnly": [{
                "cause": x["cause"], "source": x["source"], "nativeCause": x["nativeCause"],
                "universe": (x["universe"] or "")[:10] or None,
                "inputRefCount": len(x["inputRefs"]),
                "shapeIsSection95Legal": shape_ok(x),
                "publishedChannel": channel(x, ei),
            } for x in only_c],
            "referenceOnly": [{
                "cause": x["cause"], "source": x["source"], "nativeCause": x["nativeCause"],
                "universe": (x["universe"] or "")[:10] or None,
                "inputRefCount": len(x["inputRefs"]),
                "shapeIsSection95Legal": shape_ok(x),
                "publishedChannel": channel(x, ei),
            } for x in only_r],
        })
    out[run] = rows

flat = [r for run in ("syntax-code", "rust-partial") for row in out[run]
        for r in row["consumerOnly"] + row["referenceOnly"]]
out["everyDisputedRecordIsSection95ShapeLegal"] = all(r["shapeIsSection95Legal"] for r in flat)
out["disputedRecordCount"] = len(flat)
out["channelsUsed"] = sorted({r["publishedChannel"] for r in flat})
print(json.dumps(out, indent=2, default=str))
