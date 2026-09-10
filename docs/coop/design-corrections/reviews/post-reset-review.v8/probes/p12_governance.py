#!/usr/bin/env python3
"""P12: NEW-SHOULD-2 -- the crosswalk's three-part standing, and the
AR/FW/residual/DR row inventories. Every referenced review file is re-hashed
against its declared digest; a stale or self-referential binding is a finding.
"""
import hashlib, json, re, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
DC = SUBJ / "docs/coop/design-corrections"
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/"
                "reviews/candidate-subject.v8.json")

R = {"checks": [], "observations": {}}


def rec(n, ok, d=None):
    R["checks"].append({"id": n, "passed": bool(ok), "detail": d})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    man = json.loads(MANIFEST.read_bytes())
    cw = json.loads((DC / "correction-crosswalk.proposed.json").read_bytes())
    items = cw["items"]
    ids = [i["id"] for i in items]
    ar = [i for i in ids if i.startswith("AR-")]
    fw = [i for i in ids if i.startswith("FW-")]
    other = [i for i in ids if not i.startswith(("AR-", "FW-"))]
    R["observations"]["crosswalkIds"] = {"AR": ar, "FW": fw, "other": other}
    rec("CW-01-all-16-AR-rows-present", len(ar) == 16, {"count": len(ar), "ar": ar})
    rec("CW-02-all-15-FW-rows-present", len(fw) == 15, {"count": len(fw), "fw": fw})
    rec("CW-03-no-duplicate-row-ids", len(ids) == len(set(ids)))

    # --- three-part standing on every row --------------------------------
    missing_hist, missing_latest, missing_binding, stale = [], [], [], []
    self_hash = []
    for it in items:
        if not it.get("historicalReviews"):
            missing_hist.append(it["id"])
        lc = it.get("latestCompletedReview")
        if not lc:
            missing_latest.append(it["id"])
        else:
            p = SUBJ / lc["path"]
            if p.exists() and "sha256" in lc and sha(p) != lc["sha256"]:
                stale.append({"id": it["id"], "path": lc["path"],
                              "declared": lc["sha256"], "actual": sha(p)})
            # the latest completed review must pin the PREDECESSOR manifest
            if lc.get("subjectManifestSha256") != man["predecessorManifestSha256"]:
                stale.append({"id": it["id"], "reason": "not-the-predecessor-manifest",
                              "declared": lc.get("subjectManifestSha256")})
        b = it.get("currentReviewBinding")
        if not b:
            missing_binding.append(it["id"])
        else:
            # a future review must NOT be hash-embedded in its own subject
            if any(k for k in b if "sha256" in k.lower()):
                self_hash.append({"id": it["id"], "binding": b})
            if b.get("standing") != "PENDING-INDEPENDENT-REVIEW":
                self_hash.append({"id": it["id"], "standing": b.get("standing")})
    rec("CW-04-every-row-carries-immutable-historical-reviews",
        not missing_hist, {"missing": missing_hist})
    rec("CW-05-every-row-carries-the-latest-completed-predecessor-review",
        not missing_latest, {"missing": missing_latest})
    rec("CW-06-every-row-carries-a-pending-current-binding",
        not missing_binding, {"missing": missing_binding})
    rec("CW-07-no-stale-or-mis-pinned-predecessor-review", not stale,
        {"stale": stale[:6]})
    rec("CW-08-no-self-hash-cycle-demanded", not self_hash,
        {"offenders": self_hash[:6]})

    # --- the predecessor pin is the ACTUAL v7 subject ---------------------
    v7 = DC / "reviews/post-reset-review.v7/review.json"
    R["observations"]["predecessorManifestSha256"] = man["predecessorManifestSha256"]
    if v7.exists():
        v7j = json.loads(v7.read_bytes())
        R["observations"]["v7Verdict"] = v7j.get("verdict")
        R["observations"]["v7SubjectManifest"] = (
            v7j.get("subject", {}).get("manifestSha256"))
        rec("CW-09-v7-review-pins-the-declared-predecessor-manifest",
            v7j.get("subject", {}).get("manifestSha256")
            == man["predecessorManifestSha256"],
            {"v7": v7j.get("subject", {}).get("manifestSha256"),
             "manifest": man["predecessorManifestSha256"]})
        rec("CW-10-v7-verdict-is-ACCEPT-and-limited-to-its-bytes",
            v7j.get("verdict") == "ACCEPT")
        # every row's latestCompletedReview digest equals the real file
        rec("CW-11-latest-completed-review-file-hash-matches",
            all(i["latestCompletedReview"]["sha256"] == sha(v7)
                for i in items if i.get("latestCompletedReview")),
            {"actual": sha(v7)})

    # --- the later blind review must still be carried ---------------------
    blind = DC / "reviews/consumer-b.v2/output/blind-review.json"
    clar = DC / "reviews/consumer-b.v2-clarification/clarification.json"
    carried = [i["id"] for i in items if i.get("latestCompletedBlindReview")]
    R["observations"]["rowsCarryingBlind"] = len(carried)
    rec("CW-12-blind-Bv2-CHANGES_REQUIRED-carried-on-every-row",
        len(carried) == len(items), {"carried": len(carried), "rows": len(items)})
    bad_blind = []
    for i in items:
        b = i.get("latestCompletedBlindReview")
        if not b:
            continue
        if blind.exists() and b.get("sha256") != sha(blind):
            bad_blind.append({"id": i["id"], "declared": b.get("sha256")})
        if b.get("overallVerdict") != "CHANGES_REQUIRED":
            bad_blind.append({"id": i["id"], "verdict": b.get("overallVerdict")})
        c = b.get("clarification") or {}
        if clar.exists() and c.get("sha256") and c["sha256"] != sha(clar):
            bad_blind.append({"id": i["id"], "clarificationDigest": c.get("sha256")})
    rec("CW-13-blind-review-and-clarification-digests-are-exact",
        not bad_blind, {"bad": bad_blind[:6], "blindActual": sha(blind) if blind.exists() else None,
                        "clarActual": sha(clar) if clar.exists() else None})
    rec("CW-14-v7-ACCEPT-is-not-extended-over-later-blind-findings",
        all("not acceptance of successor" in
            (i.get("latestCompletedReview", {}).get("standing") or "")
            for i in items if i.get("latestCompletedReview")))

    # --- scoped DR-201..205 ----------------------------------------------
    disp = json.loads((DC / "post-reset-dispositions.v8.proposed.json").read_bytes())
    R["observations"]["dispositionKeys"] = list(disp.keys())
    scoped = disp.get("scopedReviewOwnerDispositions") or disp.get("scopedRows") or {}
    if not scoped:
        # search anywhere for DR-201..205
        found = {}
        def walk(n, p=""):
            if isinstance(n, dict):
                for k, v in n.items():
                    if re.fullmatch(r"DR-20[1-5]", str(k)):
                        found[k] = v
                    walk(v, p + "/" + str(k))
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    walk(v, p + "/" + str(i))
        walk(disp)
        scoped = found
    R["observations"]["scopedDR"] = scoped
    rec("CW-15-DR-201-to-205-present",
        sorted(scoped) == ["DR-201", "DR-202", "DR-203", "DR-204", "DR-205"],
        {"keys": sorted(scoped)})

    # --- qualification gates ---------------------------------------------
    qg = json.loads((DC / "qualification-gates.proposed.json").read_bytes())
    R["observations"]["qualificationGatesKeys"] = list(qg.keys())
    gates = qg.get("gates") or qg.get("items") or []
    if isinstance(gates, dict):
        gates = list(gates.values())
    R["observations"]["gateCount"] = len(gates)
    quals = [g for g in gates if isinstance(g, dict)
             and str(g.get("status", "")).upper().startswith("QUALIF")]
    R["observations"]["gateStatuses"] = sorted({
        str(g.get("status")) for g in gates if isinstance(g, dict)})
    rec("CW-16-all32-gates-enumerated", len(gates) == 32, {"count": len(gates)})
    rec("CW-17-no-gate-is-claimed-qualified", not quals,
        {"claimedQualified": [g.get("id") for g in quals]})

    # --- inherited residuals / row sources --------------------------------
    ires = (DC / "inherited-residuals.proposed.md").read_text()
    rows = re.findall(r"^\|\s*(RES-[A-Za-z0-9\-]+)", ires, re.M)
    R["observations"]["inheritedResidualIds"] = sorted(set(rows))
    rec("CW-18-inherited-residuals-enumerated", bool(rows), {"count": len(set(rows))})

    evd = json.loads((DC / "evaluation-residual-dispositions.proposed.json").read_bytes())
    R["observations"]["evaluationResidualKeys"] = list(evd.keys())
    irs = json.loads((DC / "inherited-row-sources.proposed.json").read_bytes())
    R["observations"]["inheritedRowSourceKeys"] = list(irs.keys())

    # --- readiness must remain unapplied ---------------------------------
    vs = json.loads((DC / "validation-summary.v1.json").read_bytes())
    rec("CW-19-readiness-not-changed", vs.get("readinessChanged") is False)
    rec("CW-20-application-still-pending",
        man.get("applicationPending") is True and man.get("reviewPending") is True)
    applied = list(DC.glob("correction-crosswalk.applied*.json")) + \
        list(DC.glob("application.v1.json"))
    rec("CW-21-no-applied-wrapper-committed-yet", not applied,
        {"found": [str(p.relative_to(DC)) for p in applied]})

    R["summary"] = {"total": len(R["checks"]),
                    "passed": sum(c["passed"] for c in R["checks"]),
                    "failed": [c for c in R["checks"] if not c["passed"]]}
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
