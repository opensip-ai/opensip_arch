#!/usr/bin/env python3
"""Write outcome.json: the machine-readable review-ready outcome of AUTHOR candidate 05.

Reads only subject files: successor.json (reviewResolutions: review-04 RF/A rows and retained review-03 R3- and review-02 R2- rows),
check-result.json, selftest-result.json and isolation-result.json. It opens nothing under the review directories. It
records author readiness for independent review; it is not approval.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    j = lambda n: json.loads((ROOT / n).read_text())
    check, selftest, isolation, succ = j("check-result.json"), j("selftest-result.json"), j("isolation-result.json"), j("successor.json")
    status = {r["id"]: r["ok"] for r in check["results"]}

    def resolve(cid):
        if cid == "isolation":
            return {"id": cid, "ok": bool(isolation["pass"])}
        hits = [ok for rid, ok in status.items() if rid == cid or rid.startswith(cid + ":")]
        return {"id": cid, "ok": bool(hits) and all(hits), "matched": len(hits)}

    rows = [{"id": r["id"], "review": r.get("review"), "resolution": r["resolution"], "checks": [resolve(c) for c in r["checks"]]} for r in succ["reviewResolutions"]]
    for r in rows:
        r["resolved"] = all(c["ok"] for c in r["checks"])
    required = [r for r in rows if r["id"].startswith("RF-")]
    advisories = [r for r in rows if r["id"].startswith("A-")]
    prior = [{"id": r["id"], "resolved": r["resolved"]} for r in rows if r["id"].startswith(("R2-", "R3-"))]
    controls = {c["control"]: c["caught"] for c in selftest["controls"]}
    ready = check["failed"] == 0 and selftest["allCaught"] and isolation["pass"] and all(r["resolved"] for r in rows)
    doc = {
        "standing": "AUTHOR candidate 05 review-ready outcome; not approval, not acceptance, not production codec, admission, sender or generator.",
        "subject": str(ROOT),
        "supersedesCandidate": succ["supersedesCandidate"],
        "authorStatus": "ready-for-independent-review" if ready else "not-ready",
        "requiredFindings": required,
        "advisories": advisories,
        "retainedPriorResolutions": prior,
        "check": {"checks": check["checks"], "failed": check["failed"]},
        "selftest": {"caught": selftest["caught"], "total": selftest["total"], "reviewer01MutantsAdapted": selftest["reviewer01MutantsAdapted"],
                     "reviewer02MutantsAdapted": selftest["reviewer02MutantsAdapted"], "reviewer03MutantsAdapted": selftest["reviewer03MutantsAdapted"], "reviewer04MutantsAdapted": selftest["reviewer04MutantsAdapted"],
                     "allCaught": selftest["allCaught"], "reviewer03Mutants": {k: v for k, v in controls.items() if k.startswith("r3_")},
                     "reviewer04Mutants": {k: v for k, v in controls.items() if k.startswith("r4_")}},
        "isolation": {"pass": isolation["pass"], "copiedInputs": isolation["copiedInputs"], "subjectFilesJsonCopied": isolation["subjectFilesJsonCopied"]},
        "remainingContradictions": succ["remainingContradictions"],
        "futureQualification": succ["futureQualification"],
        "notClaimed": ["approval", "production wire decoder", "production admission", "production (M3) sender", "generator run", "platform or M2/M3 qualification",
                       "commit or push", "clean git state of the architecture snapshot", "general filesystem confinement (open/exec audit only)",
                       "pinned Node system libraries (trusted, unselected boundary)"],
    }
    (ROOT / "outcome.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({"authorStatus": doc["authorStatus"], "required": {r["id"]: r["resolved"] for r in required},
                      "advisories": {a["id"]: a["resolved"] for a in advisories}}, indent=1))
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
