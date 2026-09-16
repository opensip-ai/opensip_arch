#!/usr/bin/env python3
"""Write outcome.json: the machine-readable review-ready outcome of AUTHOR candidate 02.

Reads only subject files: successor.json (reviewResolutions), check-result.json, selftest-result.json and
isolation-result.json. It opens nothing under the review directory. It records author readiness for independent review;
it is not approval.

    PYTHONDONTWRITEBYTECODE=1 python3 -B tools/outcome.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ADVISORIES = {
    "ADV-1": ["architecture-pins-verified-before-import", "architecture-pins-unchanged-after-run"],
    "ADV-2": ["vectors-cover-every-rule"],
    "ADV-3": ["field-coverage-gaps-resolved", "field-coverage-positional-rows-explicit", "field-coverage-matches-inputs"],
    "ADV-4": ["ts2-unavailable-selection-trace-difference-stated"],
    "ADV-5": ["p3-guard-successor-file", "p3-overlay-updates-match-rust2"],
    "ADV-6": ["path-members-bound-to-lexical-rules"],
    "ADV-7": ["anchor-order-languages-differ", "anchor-order-path-only-same", "anchor-order-sources"],
    "ADV-8": ["limit-literals"],
    "ADV-9": ["commit-map-value-classes-match-owner", "vectors:COMMIT-MAP"],
    "ADV-10": ["d9join-interruption-timing-source", "native-md-anchors"],
}


def main():
    j = lambda n: json.loads((ROOT / n).read_text())
    check, selftest, isolation, succ = j("check-result.json"), j("selftest-result.json"), j("isolation-result.json"), j("successor.json")
    status = {r["id"]: r["ok"] for r in check["results"]}

    def resolve(cid):
        if cid == "isolation":
            return {"id": cid, "ok": bool(isolation["pass"])}
        hits = [ok for rid, ok in status.items() if rid == cid or rid.startswith(cid + ":")]
        return {"id": cid, "ok": bool(hits) and all(hits), "matched": len(hits)}

    required = [{"id": r["id"], "resolution": r["resolution"], "checks": [resolve(c) for c in r["checks"]]} for r in succ["reviewResolutions"]]
    for r in required:
        r["resolved"] = all(c["ok"] for c in r["checks"])
    advisories = [{"id": a, "checks": [resolve(c) for c in cs]} for a, cs in ADVISORIES.items()]
    for a in advisories:
        a["addressed"] = all(c["ok"] for c in a["checks"])
    ready = (check["failed"] == 0 and selftest["allCaught"] and isolation["pass"]
             and all(r["resolved"] for r in required) and all(a["addressed"] for a in advisories))
    doc = {
        "standing": "AUTHOR candidate 02 review-ready outcome; not approval, not acceptance, not production codec or admission.",
        "subject": str(ROOT),
        "supersedesCandidate": succ["supersedesCandidate"],
        "authorStatus": "ready-for-independent-review" if ready else "not-ready",
        "requiredFindings": required,
        "advisories": advisories,
        "check": {"checks": check["checks"], "failed": check["failed"]},
        "selftest": {"caught": selftest["caught"], "total": selftest["total"], "reviewerMutantsAdapted": selftest["reviewerMutantsAdapted"], "allCaught": selftest["allCaught"]},
        "isolation": {"pass": isolation["pass"], "copiedInputs": isolation["copiedInputs"]},
        "remainingContradictions": succ["remainingContradictions"],
        "futureQualification": succ["futureQualification"],
        "notClaimed": ["approval", "production wire decoder", "production admission", "generator run", "M2/M3 qualification", "commit or push"],
    }
    (ROOT / "outcome.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({"authorStatus": doc["authorStatus"], "required": {r["id"]: r["resolved"] for r in required},
                      "advisories": {a["id"]: a["addressed"] for a in advisories}}, indent=1))
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
