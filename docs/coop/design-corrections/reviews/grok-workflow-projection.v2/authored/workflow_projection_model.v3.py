"""Pure evaluator3 workflow projection. Not full Run replay.

Consumes ADMITTED evaluator3 findings, fingerprint preimages, emission bindings,
waivedFindingIds and ruleResults. Does not read producer expected entries, expected
classifications, or any verified flag. Reuses workflows_model.v1 classify/audit
profiles unchanged, then adds typed unmatched/population deficiencies.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "foundation"))
import canonical  # noqa: E402

_spec = importlib.util.spec_from_file_location("workflows_legacy_profile", HERE / "workflows_model.v1.py")
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)

Refusal = W.Refusal
wid = W.wid
doc_digest = W.doc_digest
AUDIT_PROFILES = W.AUDIT_PROFILES
COUNT_KEYS = W.COUNT_KEYS
classify = W.classify
resolve_detectors = W.resolve_detectors
verify_scope_parameter_binding = W.verify_scope_parameter_binding

GENERIC7 = (
    "ruleId",
    "subjectPath",
    "qualifiedName",
    "subjectKind",
    "subjectLanguage",
    "matchingFactCount",
    "matchingImportCount",
)
STORED_KINDS = {"file", "symbol", "package"}
UNMATCHED_REASONS = {
    "projection-unavailable",
    "signature-ambiguous",
    "anonymous-subject",
    "population-incomplete",
}
COMPAT_META = ("ruleId", "subjectPath", "kind", "qualifiedName", "ruleClosure")


def sha(value) -> str:
    return hashlib.sha256(canonical.canonical(value)).hexdigest()


def fingerprint_id(descriptor: dict) -> str:
    return wid("finding-key2", "finding-fingerprint", descriptor)


def findings_map(occurrences: list) -> dict:
    """Per-run map keyed by findingId. NEVER by fingerprint (duplicates are normal)."""
    out = {}
    for occ in occurrences:
        fid = occ["findingId"]
        if fid in out:
            raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "duplicate findingId", fid)
        if not str(fid).startswith("finding3:"):
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "finding3 required", fid)
        sid = occ["finding"]["subjectId"]
        if not str(sid).startswith("subject3:"):
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "opaque subject3 required", sid)
        out[fid] = occ
    return out


def admit_occurrence(occ: dict, binding: dict) -> dict:
    finding = occ["finding"]
    if finding.get("schemaVersion") != 3:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "finding schemaVersion 3")
    corr = finding["correspondence"]
    fp = finding["fingerprint"]
    params = occ["parameterRecord"]
    if sha(params) != finding["parameterDigest"]:
        raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "parameterDigest mismatch", occ["findingId"])
    if params.get("schemaVersion") != 2 or set(params["parameters"]) != set(GENERIC7):
        raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "declarative-subject-v1 requires exactly the generic 7 parameters")
    if params["parameters"]["subjectKind"] not in STORED_KINDS:
        raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "subjectKind is stored kind, never export")
    if corr["state"] == "matched":
        if fp is None or corr.get("reason") is not None:
            raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "matched requires nonnull fingerprint and null reason")
        desc = occ.get("fingerprintDescriptor")
        if desc is None:
            raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "matched finding missing fingerprint preimage")
        if fingerprint_id(desc) != fp:
            raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "fingerprint identity does not match preimage")
        if desc.get("schemaVersion") != 2:
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "finding-key2 retained")
    elif corr["state"] == "unmatched":
        if fp is not None or corr.get("reason") not in UNMATCHED_REASONS:
            raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "unmatched requires null fingerprint and closed reason")
        if occ.get("fingerprintDescriptor") is not None:
            raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "unmatched must not carry a fingerprint preimage")
    else:
        raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "correspondence.state")
    if binding["emissionProfile"] != "declarative-subject-v1" or binding["stabilityClass"] != "path-stable":
        raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "declarative-subject-v1/path-stable required")
    return occ


def _entry_fields(occ: dict, binding: dict, waived: bool) -> dict:
    finding = occ["finding"]
    # Path is finding.subject.logicalPath, not a reconstructed subject3 triple.
    # Package names may repeat; distinct manifest paths yield distinct fingerprints.
    entry = {
        "fingerprint": finding["fingerprint"],
        "ruleId": finding["ruleId"],
        "detectorId": binding["contributionId"],
        "stabilityClass": binding["stabilityClass"],
        "subjectPath": finding["subject"]["logicalPath"],
        "waived": waived,
    }
    if "legacyFingerprint" in occ:
        entry["legacyFingerprint"] = occ["legacyFingerprint"]
    return entry


def project_baseline_entries(occurrences: list, bindings: dict, waived_ids) -> dict:
    """Compute baseline entries and unmatched array. No producer expected entries."""
    waived = set(waived_ids)
    by_id = findings_map(occurrences)
    groups = {}
    unmatched = []
    for fid, occ in by_id.items():
        finding = occ["finding"]
        binding = bindings[finding["ruleId"]]
        admit_occurrence(occ, binding)
        is_waived = fid in waived
        if finding["correspondence"]["state"] == "unmatched":
            row = {
                "findingId": fid,
                "ruleId": finding["ruleId"],
                "subjectId": finding["subjectId"],
                "subjectPath": finding["subject"]["logicalPath"],
                "severity": finding["severity"],
                "waived": is_waived,
                "correspondenceReason": finding["correspondence"]["reason"],
            }
            unmatched.append(row)
            continue
        desc = occ["fingerprintDescriptor"]
        fp = finding["fingerprint"]
        g = groups.setdefault(fp, {"descriptor": desc, "fields": None, "findingIds": []})
        if canonical.canonical(g["descriptor"]) != canonical.canonical(desc):
            raise Refusal(
                "CONFIG.INVALID",
                "CONFIG.INVALID",
                "fingerprint preimage conflict is input refusal, not incomplete",
                fp,
            )
        fields = _entry_fields(occ, binding, is_waived)
        if g["fields"] is None:
            g["fields"] = fields
        elif canonical.canonical(g["fields"]) != canonical.canonical(fields):
            raise Refusal(
                "CONFIG.INVALID",
                "BASELINE.ENTRY_PROJECTION_CONFLICT",
                "BaselineEntry fields including optional legacyFingerprint presence/value must agree",
                fp,
            )
        g["findingIds"].append(fid)
    entries = sorted((g["fields"] for g in groups.values()), key=lambda e: e["fingerprint"].encode())
    unmatched.sort(key=lambda r: r["findingId"].encode())
    return {"entries": entries, "unmatchedOccurrences": unmatched, "groups": groups}


def adopt_baseline_v3(run, plan, project_id, policy, scope, waivers, rule_coverage, projected, detector_closure, pivot_closure, context, host_release, analysis_spec=None):
    """Adapter over v1 adopt_baseline: schemaMajor 2, run3, unmatched array. Scope join reused."""
    if run.get("authority") != "authoritative":
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.SOURCE_EPHEMERAL", "run an authoritative analysis first")
    if run.get("availability", "retained") != "retained":
        raise Refusal("REQUEST.PRECONDITION_FAILED", "REPAIR.EVIDENCE_RUN_UNAVAILABLE", "the Run evidence is " + run.get("availability"))
    if not str(run["runId"]).startswith("run3:"):
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "baseline origin Run must be run3")
    if policy.get("schemaMajor") != 2:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "PolicyDocumentV2 required")
    if analysis_spec is not None:
        verify_scope_parameter_binding(analysis_spec, scope)
    ctx = dict(context)
    ctx["policyDigest"] = doc_digest(policy)
    ctx["scopeDigest"] = doc_digest(scope)
    ctx["waiverSetDigest"] = doc_digest(waivers)
    ents = projected["entries"]
    unmatched = projected["unmatchedOccurrences"]
    if len({x["fingerprint"] for x in ents}) != len(ents):
        raise Refusal("CONFIG.INVALID", None, "duplicate fingerprint in baseline entries")
    desc = {
        "schemaFamily": "opensip.product.baseline",
        "schemaMajor": 2,
        "originProjectId": project_id,
        "source": {"snapshotId": run["snapshotId"]},
        "runId": run["runId"],
        "planId": plan,
        "fingerprintRecipe": {"domain": "finding-fingerprint", "recipeMajor": 2},
        "detectorClosure": detector_closure,
        "pivotClosure": sorted(pivot_closure, key=lambda p: p["closureId"]),
        "context": ctx,
        "contextDocuments": {"policy": policy, "scope": scope, "waivers": waivers},
        "ruleCoverage": rule_coverage,
        "entries": ents,
        "unmatchedOccurrences": unmatched,
    }
    bid = wid("baseline2", "workflow.baseline", desc)
    pins = sorted({run["runId"]} | {p["closureId"] for p in pivot_closure})
    return {
        "baselineId": bid,
        "descriptor": desc,
        "custody": {
            "exportedByHostRelease": host_release,
            "exportedAtUtc": "2026-09-08T00:00:00Z",
            "runRetainedAtExport": True,
            "retentionPins": pins,
        },
    }


def verify_baseline_artifact_v3(art) -> bool:
    d = art["descriptor"]
    if d.get("schemaMajor") != 2:
        raise Refusal(
            "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
            "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
            "historical schemaMajor 1 is refused; missing unmatched is not []",
        )
    if wid("baseline2", "workflow.baseline", d) != art["baselineId"]:
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "baselineId does not match descriptor")
    if not d["runId"].startswith("run3:"):
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "a baseline names an authoritative run3")
    fps = [x["fingerprint"] for x in d["entries"]]
    if fps != sorted(fps, key=lambda s: s.encode()) or len(set(fps)) != len(fps):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "entries must be sorted and unique")
    uids = [x["findingId"] for x in d.get("unmatchedOccurrences", [])]
    if uids != sorted(uids, key=lambda s: s.encode()) or len(set(uids)) != len(uids):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "unmatchedOccurrences must be sorted unique findingId")
    if "unmatchedOccurrences" not in d:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "BASELINE.SCHEMA_MAJOR_UNSUPPORTED", "schemaMajor 2 requires unmatchedOccurrences")
    return True


def correspondence_coverage(rule_results, occurrences, waived_ids) -> list:
    by_rule = {r["ruleId"]: r for r in rule_results}
    counts = {rid: {"matched": 0, "unmatched": 0} for rid in by_rule}
    for occ in occurrences:
        rid = occ["finding"]["ruleId"]
        state = occ["finding"]["correspondence"]["state"]
        counts.setdefault(rid, {"matched": 0, "unmatched": 0})
        counts[rid][state] += 1
    out = []
    for rid in sorted(by_rule, key=lambda s: s.encode()):
        r = by_rule[rid]
        enum = r["enumeration"]
        pop_unknown = enum["state"] == "incomplete"
        matched_n = counts.get(rid, {}).get("matched", 0)
        unmatched_n = counts.get(rid, {}).get("unmatched", 0)
        zero = (matched_n + unmatched_n) == 0
        out.append(
            {
                "ruleId": rid,
                "gating": bool(r.get("gating", r["outcome"] != "pass" and enum["state"] != "disabled")),
                "matchedCount": matched_n,
                "unmatchedCount": unmatched_n,
                "populationUnknown": pop_unknown,
                "zeroFindings": zero,
            }
        )
    return out


def _unmatched_rows(occurrences, waived_ids) -> list:
    waived = set(waived_ids)
    rows = []
    for occ in occurrences:
        f = occ["finding"]
        if f["correspondence"]["state"] != "unmatched":
            continue
        rows.append(
            {
                "findingId": occ["findingId"],
                "ruleId": f["ruleId"],
                "subjectId": f["subjectId"],
                "subjectPath": f["subject"]["logicalPath"],
                "severity": f["severity"],
                "waived": occ["findingId"] in waived,
                "correspondenceReason": f["correspondence"]["reason"],
            }
        )
    rows.sort(key=lambda r: r["findingId"].encode())
    return rows


def current_run_verdict(rule_results, occurrences, waived_ids) -> str:
    """Current sealed-run verdict from admitted ruleResults plus live unwaived findings.

    Path-waived unmatched findings are not live. Population unknown without a live
    gating finding is indeterminate, not a vacuous pass.
    """
    waived = set(waived_ids)
    live_by_rule = {}
    for occ in occurrences:
        rid = occ["finding"]["ruleId"]
        if occ["findingId"] not in waived:
            live_by_rule.setdefault(rid, []).append(occ)
    fail = False
    indeterminate = False
    for r in rule_results:
        if r["outcome"] == "disabled":
            continue
        gating = bool(r.get("gating", True))
        if not gating:
            continue
        if live_by_rule.get(r["ruleId"]):
            fail = True
            continue
        if r["enumeration"]["state"] == "incomplete" or r["outcome"] == "indeterminate":
            indeterminate = True
    if fail:
        return "fail"
    if indeterminate or any(r["outcome"] == "indeterminate" for r in rule_results):
        return "indeterminate"
    return "pass"


def compare_v3(baseline, current, host, profile_name, current_detectors, accept_origins=()):
    """Matched classification via v1.classify; unmatched are not guessed into entries."""
    profile = AUDIT_PROFILES[profile_name]
    bdesc = baseline if "schemaFamily" in baseline else baseline["descriptor"]
    if bdesc.get("schemaMajor") != 2:
        desc = {
            "schemaFamily": "opensip.product.comparison",
            "schemaMajor": 2,
            "baselineId": baseline.get("_baselineId") or baseline.get("baselineId"),
            "currentRunId": current["runId"],
            "currentSnapshotId": current["snapshotId"],
            "auditProfile": profile,
            "projectCorrespondence": "unmapped",
            "comparisonPerformed": False,
            "wholeIndeterminateReason": "baseline-schema-major-unsupported",
            "remedy": {
                "code": "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
                "remedy": "re-adopt under evaluator3 schemaMajor 2; do not treat missing unmatched as []",
            },
            "baselineContext": bdesc.get("context", {}),
            "currentContext": current["context"],
            "contextDelta": {
                "codeChanged": False,
                "detectorChanged": False,
                "policyChanged": False,
                "scopeChanged": False,
                "waiversChanged": False,
                "evidenceAvailabilityChanged": False,
            },
            "pivotsAvailable": {k: "unavailable" for k in ("E0", "E1", "E2", "E3")},
            "detectors": [],
            "ruleDeficiencies": [],
            "entries": [],
            "unmatchedOccurrences": [],
            "correspondenceCoverage": [],
            "counts": {k: 0 for k in COUNT_KEYS},
            "verdict": "indeterminate",
            "d9Deficiency": "baseline-recipe-unsupported",
        }
        if bdesc.get("originProjectId") == current["projectId"]:
            desc["projectCorrespondence"] = "same-project"
        return {
            "comparisonResultId": wid("comparison2", "workflow.comparison", desc),
            "descriptor": desc,
            "errorCode": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
        }
    # Delegate matched classification through a v1-shaped current, then attach unmatched.
    current_v1 = {
        "runId": current["runId"],
        "snapshotId": current["snapshotId"],
        "projectId": current["projectId"],
        "context": current["context"],
        "ruleCoverage": current["ruleCoverage"],
        "presence": current["presence"],
        "entryRules": current["entryRules"],
        "boundPivots": current.get("boundPivots", []),
    }
    baseline_v1 = copy.deepcopy(bdesc)
    baseline_v1["schemaMajor"] = 1  # v1.compare gates on ==1; we already checked ==2
    baseline_v1["_baselineId"] = baseline.get("_baselineId") or baseline.get("baselineId")
    # v1 refuses schemaMajor != 1. Call classify loop locally instead of W.compare.
    res = _compare_matched(baseline_v1, current_v1, host, profile_name, current_detectors, accept_origins)
    desc = res["descriptor"]
    desc["schemaMajor"] = 2
    occ = current.get("occurrences", [])
    waived = current.get("waivedFindingIds", [])
    rules = current.get("ruleResults", [])
    desc["unmatchedOccurrences"] = _unmatched_rows(occ, waived)
    cov = correspondence_coverage(rules, occ, waived)
    # Prefer explicit gating from current ruleCoverage when present.
    rc = current["ruleCoverage"]
    for row in cov:
        if row["ruleId"] in rc:
            row["gating"] = bool(rc[row["ruleId"]]["enabled"] and rc[row["ruleId"]]["gating"])
    desc["correspondenceCoverage"] = cov
    extra = []
    for row in cov:
        if row["gating"] and (row["unmatchedCount"] > 0 or row["populationUnknown"]):
            extra.append({"ruleId": row["ruleId"], "gating": True, "cause": "correspondence-incomplete"})
    existing = {(d["ruleId"], d["cause"]) for d in desc["ruleDeficiencies"]}
    for dfc in extra:
        if (dfc["ruleId"], dfc["cause"]) not in existing:
            desc["ruleDeficiencies"].append(dfc)
    desc["ruleDeficiencies"] = sorted(desc["ruleDeficiencies"], key=lambda d: (d["ruleId"].encode(), d["cause"].encode()))
    if desc["verdict"] != "fail" and any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in desc["ruleDeficiencies"]):
        desc["verdict"] = "indeterminate"
        desc["d9Deficiency"] = desc.get("d9Deficiency") or "verdict-indeterminate"
        desc["remedy"] = {
            "code": "COMPARISON.CORRESPONDENCE_INCOMPLETE",
            "remedy": "complete inventories/projections; unmatched cannot be classified as net-new or resolved",
        }
    # Matched fail already set by classify; keep fail over indeterminate.
    res["comparisonResultId"] = wid("comparison2", "workflow.comparison", desc)
    res["descriptor"] = desc
    return res


def _compare_matched(baseline, current, host, profile_name, current_detectors, accept_origins):
    """Copy of v1.compare matched loop with schemaMajor 1 after the v3 gate already ran."""
    profile = AUDIT_PROFILES[profile_name]
    desc = {
        "schemaFamily": "opensip.product.comparison",
        "schemaMajor": 1,
        "baselineId": baseline["_baselineId"],
        "currentRunId": current["runId"],
        "currentSnapshotId": current["snapshotId"],
        "auditProfile": profile,
        "baselineContext": baseline["context"],
        "currentContext": current["context"],
        "detectors": [],
        "ruleDeficiencies": [],
        "entries": [],
    }
    if baseline["originProjectId"] == current["projectId"]:
        desc["projectCorrespondence"] = "same-project"
    elif baseline["originProjectId"] in accept_origins:
        desc["projectCorrespondence"] = "declared"
    else:
        desc["projectCorrespondence"] = "unmapped"

    def whole(reason, code, remedy):
        desc.update(
            comparisonPerformed=False,
            wholeIndeterminateReason=reason,
            remedy={"code": code, "remedy": remedy},
            pivotsAvailable={k: "unavailable" for k in ("E0", "E1", "E2", "E3")},
            counts={k: 0 for k in COUNT_KEYS},
            verdict="indeterminate",
            d9Deficiency="baseline-recipe-unsupported",
            unmatchedOccurrences=[],
            correspondenceCoverage=[],
        )
        return {"comparisonResultId": wid("comparison2", "workflow.comparison", desc), "descriptor": desc}

    if desc["projectCorrespondence"] == "unmapped":
        return whole("baseline-project-unmapped", "BASELINE.PROJECT_UNMAPPED", "pass --accept-origin " + baseline["originProjectId"])
    bc, cc = baseline["context"], current["context"]
    desc["contextDelta"] = {
        "codeChanged": baseline["source"]["snapshotId"] != current["snapshotId"],
        "detectorChanged": sorted(bc["detectorClosureIds"]) != sorted(cc["detectorClosureIds"]),
        "policyChanged": bc["policyDigest"] != cc["policyDigest"],
        "scopeChanged": bc["scopeDigest"] != cc["scopeDigest"],
        "waiversChanged": bc["waiverSetDigest"] != cc["waiverSetDigest"],
        "evidenceAvailabilityChanged": sorted(i["importId"] for i in bc["evidenceAvailability"].get("imports", []))
        != sorted(i["importId"] for i in cc["evidenceAvailability"].get("imports", [])),
    }
    dets = resolve_detectors(baseline, current_detectors, host)
    desc["detectors"] = [dets[k] for k in sorted(dets, key=lambda s: s.encode())]
    e0_state = (
        "not-needed"
        if not desc["contextDelta"]["detectorChanged"]
        else ("available" if all(d["method"] != "indeterminate" for d in dets.values()) else "unavailable")
    )
    bound = set(current.get("boundPivots", []))
    piv = {"E0": e0_state}
    unavailable = []
    for axis, key in (("policy", "policyChanged"), ("scope", "scopeChanged"), ("waiver", "waiversChanged")):
        pv = W.AXIS_PIVOT[axis]
        if not desc["contextDelta"][key]:
            piv[pv] = "not-needed"
        elif pv in bound:
            piv[pv] = "available"
        else:
            piv[pv] = "unavailable"
            unavailable.append(pv)
    desc["pivotsAvailable"] = piv
    desc["comparisonPerformed"] = True
    b_rules = {r["ruleId"]: r for r in baseline["ruleCoverage"]}
    c_rules = current["ruleCoverage"]
    desc["ruleDeficiencies"] = W.rule_deficiencies(c_rules)
    b_entries = {x["fingerprint"]: x for x in baseline["entries"]}
    fps = sorted(set(b_entries) | set(current["presence"]), key=lambda s: s.encode())
    counts = {k: 0 for k in COUNT_KEYS}
    verdict_signals = set()
    for fp in fps:
        rule_id, det_id = current["entryRules"].get(fp) or (b_entries[fp]["ruleId"], b_entries[fp]["detectorId"])
        pres = current["presence"].get(fp) or {
            "B": True,
            "E0": False if e0_state == "available" else None,
            "E1": False,
            "E2": False,
            "E3": False,
            "E4": False,
            "waivedB": b_entries[fp]["waived"],
            "waivedC": False,
        }
        pres = dict(pres)
        pres["B"] = fp in b_entries
        if pres["B"]:
            pres["waivedB"] = b_entries[fp]["waived"]
        m = dets[det_id]["method"]
        if m in ("identical-closure", "declared-compatible") and e0_state != "available":
            pres["E0"] = pres["E1"]
        elif m == "detector-added":
            pres["E0"] = False
        elif m == "detector-removed":
            pres["E1"] = pres["E2"] = pres["E3"] = pres["E4"] = False
        elif m == "indeterminate":
            pres["E0"] = None
        entry, sig = classify(
            fp,
            rule_id,
            pres,
            b_rules.get(rule_id),
            c_rules.get(rule_id),
            bc["evidenceAvailability"],
            cc["evidenceAvailability"],
            dets[det_id],
            profile,
            unavailable,
        )
        desc["entries"].append(entry)
        counts[entry["classification"]] += 1
        if entry["gates"]:
            counts["gating"] += 1
        if sig:
            verdict_signals.add(sig)
    for dfc in desc["ruleDeficiencies"]:
        if dfc["gating"]:
            verdict_signals.add("indeterminate")
    gating_rules = list(c_rules.values())
    if profile["gateRuleUnder"] == "baseline-or-current":
        gating_rules += list(b_rules.values())
    if (unavailable or e0_state == "unavailable") and any(r["enabled"] and r["gating"] for r in gating_rules):
        verdict_signals.add("indeterminate")
    desc["counts"] = counts
    desc["verdict"] = "fail" if "fail" in verdict_signals else ("indeterminate" if "indeterminate" in verdict_signals else "pass")
    if desc["verdict"] == "indeterminate":
        desc["d9Deficiency"] = "baseline-recipe-unsupported" if e0_state == "unavailable" else "verdict-indeterminate"
        gating_def = [d for d in desc["ruleDeficiencies"] if d["gating"]]
        if e0_state == "unavailable":
            desc["remedy"] = {
                "code": "BASELINE.PIVOT_DETECTOR_UNAVAILABLE",
                "remedy": "install or bundle the baseline pivot closure under current trust, or adopt a new baseline explicitly",
            }
        elif unavailable:
            desc["remedy"] = {
                "code": "COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE",
                "remedy": "bind the re-evaluation results for " + ",".join(unavailable),
            }
        elif gating_def:
            desc["remedy"] = {
                "code": "COMPARISON.REQUIRED_COVERAGE_UNSATISFIED",
                "remedy": "restore required coverage/evidence for " + ",".join(d["ruleId"] for d in gating_def),
            }
        else:
            desc["remedy"] = {
                "code": "COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE",
                "remedy": "re-import the required evidence against the current snapshot",
            }
    return {"comparisonResultId": wid("comparison2", "workflow.comparison", desc), "descriptor": desc}


def project_finding_surface(occ: dict, waived: bool) -> dict:
    f = occ["finding"]
    row = {
        "findingId": occ["findingId"],
        "ruleId": f["ruleId"],
        "subjectId": f["subjectId"],
        "subjectPath": f["subject"]["logicalPath"],
        "subjectKind": f["subject"]["kind"],
        "qualifiedName": f["subject"]["qualifiedName"],
        "severity": f["severity"],
        "messageCode": f["messageCode"],
        "correspondence": copy.deepcopy(f["correspondence"]),
        "fingerprint": f["fingerprint"],
        "waived": waived,
        "parameterDigest": f["parameterDigest"],
    }
    if f["correspondence"]["state"] == "matched":
        row["partialFingerprints"] = {"opensip/finding-key2": f["fingerprint"]}
    return row


def project_sarif(occurrences, waived_ids) -> list:
    waived = set(waived_ids)
    rows = [project_finding_surface(occ, occ["findingId"] in waived) for occ in occurrences]
    rows.sort(key=lambda r: r["findingId"].encode())
    return rows


def project_candidates(run_id, project_id, occurrences, rule_gating, waived_ids, dispositions, today):
    """Matched candidates key by fingerprint; unmatched key by findingId. No fake fingerprint."""
    waived = set(waived_ids)
    out = []
    for occ in occurrences:
        f = occ["finding"]
        matched = f["correspondence"]["state"] == "matched"
        key = f["fingerprint"] if matched else occ["findingId"]
        cid = wid("candidate2", "workflow.candidate", {"projectId": project_id, "kind": "finding", "key": key})
        gating = bool(rule_gating.get(f["ruleId"]))
        live = occ["findingId"] not in waived
        c = {
            "candidateId": cid,
            "runId": run_id,
            "kind": "finding",
            "findingId": occ["findingId"],
            "fingerprint": f["fingerprint"],
            "ruleId": f["ruleId"],
            "correspondence": copy.deepcopy(f["correspondence"]),
            "evidenceLevel": "proof-backed",
            "subjectPath": f["subject"]["logicalPath"],
            "controlBearing": gating and live,
            "suppressed": False,
        }
        d = dispositions.get(cid)
        if matched and d and d["disposition"] in ("reject", "defer"):
            if d["suppressUntil"] is None or d["suppressUntil"] >= today:
                c["suppressed"] = True
                c["suppressedBy"] = d["receiptId"]
            else:
                c["previouslyReviewed"] = True
        # Unmatched: fingerprint suppression of a different candidateId cannot hide this row.
        out.append(c)
    return sorted(out, key=lambda c: c["candidateId"])


def query_finding(occurrences, *, finding_id=None, fingerprint=None) -> list:
    if finding_id is not None:
        return [occ for occ in occurrences if occ["findingId"] == finding_id]
    if fingerprint is not None:
        return [
            occ
            for occ in occurrences
            if occ["finding"]["fingerprint"] == fingerprint and occ["finding"]["correspondence"]["state"] == "matched"
        ]
    raise Refusal("CONFIG.INVALID", "CONFIG.INVALID", "finding.show requires findingId or fingerprint")


def _meta(occ: dict) -> dict:
    f = occ["finding"]
    return {
        "ruleId": f["ruleId"],
        "subjectPath": f["subject"]["logicalPath"],
        "kind": f["subject"]["kind"],
        "qualifiedName": f["subject"]["qualifiedName"],
        "ruleClosure": f["ruleClosure"],
    }


def project_repair_targets(target_fingerprints, occurrences) -> dict:
    """Fingerprint-targeted repair. Unmatched refuse. Multi-config must be metadata-compatible."""
    by_fp = {}
    for occ in occurrences:
        f = occ["finding"]
        if f["correspondence"]["state"] != "matched":
            continue
        by_fp.setdefault(f["fingerprint"], []).append(occ)
    out = {}
    for fp in target_fingerprints:
        occs = by_fp.get(fp, [])
        if not occs:
            raise Refusal(
                "REQUEST.PRECONDITION_FAILED",
                "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE",
                "fingerprint-targeted repair requires a matched finding-key2; unmatched inspect by findingId",
                fp,
            )
        metas = [_meta(o) for o in occs]
        first = metas[0]
        if any(canonical.canonical(m) != canonical.canonical(first) for m in metas[1:]):
            raise Refusal(
                "REQUEST.PRECONDITION_FAILED",
                "REPAIR.TARGET_METADATA_AMBIGUOUS",
                "multiple configurations share this fingerprint with incompatible path/kind/rule metadata",
                fp,
            )
        out[fp] = {
            "fingerprint": fp,
            "findingIds": sorted(o["findingId"] for o in occs),
            "parameterDigests": sorted({o["finding"]["parameterDigest"] for o in occs}),
            "metadata": first,
        }
    return out


def serialization_overflow_termination():
    """Existing D9 error. Detail EVALUATION.OUTPUT_BOUND_EXCEEDED is not HOST.IO_FAILURE."""
    return {
        "class": "operational-failed",
        "errorCode": "OUTPUT.SERIALIZATION_FAILED",
        "faultCause": "output-serialization",
        "domainDetail": {
            "code": "EVALUATION.OUTPUT_BOUND_EXCEEDED",
            "remedy": "narrow the admitted output or raise the array/C-byte bound; never truncate to an empty Run",
        },
    }
