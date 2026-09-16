"""Phase 8 baseline adoption/admission and multi-axis comparison over admitted Runs.

Owners: workflows-and-surfaces.md s2 (lines 254-305), s3 (309-399), s1 audit gate ownership (213-219);
workflow-projection-contract.v3.md s2-s4, s9-s15; evaluator3 baseline-artifact / comparison-result / invocation schemas.
Every Run is re-admitted through ref/closure.py graph admission (their fresh-process replays are runs/cmp-*.replay.json).
E1..E3 are re-evaluations of the CURRENT admitted inputs with only policy/scope/waivers substituted (evaluationInputRefs must be
identical); E0 is a separately committed pivot Run over the current snapshot under the baseline detector and prior documents.

cb24 reconstruction choices (recorded in each vector, adjudicated in phase 10):
  * detectorId = emission binding contributionId (no kit derivation found);
  * a pivot whose axis is unchanged copies the NEXT pivot (E3<-E4, E2<-E3, E1<-E2, E0<-E1);
  * presence "disabled" (rule not enabled in that pivot) is absent-without-negative-knowledge: serialized null on E0..E3,
    false on B/E4; disabled<->false is no change, disabled<->true is a change at that axis;
  * RuleCoverage.requiredCoverage: unsatisfied for required evidence missing, unknown for other indeterminate, else satisfied.
Writes vectors/baseline-audit.json, comparison-missing.json, comparison-evidence-changed.json, comparison-empty-result.json,
comparison-scope-policy-only.json, baseline-e0-e3.json, pivot-only-fingerprints.json.
Usage: python3 tools/runref.py tools/phase8_compare.py
"""
import copy
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import detector_compat as DC  # noqa: E402
import evaluator as EV  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
import phase7_vectors as P7  # noqa: E402

KIT = schemas.kit()
BASE_DOC = "workflows/schemas/evaluator3/baseline-artifact.schema.json"
CMP_DOC = "workflows/schemas/evaluator3/comparison-result.schema.json"
INVOC3, COMMON3 = P7.INVOC3, P7.COMMON3
SEV = {"note": 0, "warning": 1, "error": 2}
PROFILES = {
    "code-regression": {"name": "code-regression", "gateCodeNetNew": True, "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False,
                        "newWaiverSuppressesCodeNetNew": False, "gateRuleUnder": "baseline-or-current"},
    "policy-change": {"name": "policy-change", "gateCodeNetNew": True, "gateNewlyLiveByPolicyAxes": True, "gateAllCurrentLive": False,
                      "newWaiverSuppressesCodeNetNew": False, "gateRuleUnder": "baseline-or-current"},
    "full-current": {"name": "full-current", "gateCodeNetNew": True, "gateNewlyLiveByPolicyAxes": True, "gateAllCurrentLive": True,
                     "newWaiverSuppressesCodeNetNew": True, "gateRuleUnder": "current-only"},
    "report-only": {"name": "report-only", "gateCodeNetNew": False, "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False,
                    "newWaiverSuppressesCodeNetNew": True, "gateRuleUnder": "current-only"}}
AXES = ["code", "detection", "policy", "scope", "waiver"]
CLASS = {"code": ("CODE-NET-NEW", "CODE-FIXED"), "detection": ("DETECTION-DELTA",) * 2, "policy": ("POLICY-DELTA",) * 2,
         "scope": ("SCOPE-DELTA",) * 2}
CLASSIFICATIONS = ["UNCHANGED", "CODE-NET-NEW", "CODE-FIXED", "DETECTION-DELTA", "POLICY-DELTA", "SCOPE-DELTA", "WAIVER-DELTA",
                   "EVIDENCE-DELTA", "INDETERMINATE"]
failures = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def dump(rel, obj):
    with open(f"{OUT}/{rel}", "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


def enc(s):
    return s.encode()


class Refusal(Exception):
    def __init__(self, key, detail=""):
        super().__init__(f"{key}:{detail}")
        self.key, self.detail = key, detail


RUNS = {}


def gating(rule, policy):
    return bool(rule["enabled"] and rule["gate"] and SEV[rule["severity"]] >= SEV[policy["gateSeverityAtLeast"]])


def detector_id(binding):
    return binding["contributionId"]


def project(findings, proof, policy, emission):
    waived = set(proof["waivedFindingIds"])
    bind = {r["ruleId"]: r for r in emission["rules"]}
    matched, unmatched = {}, []
    for o in findings:
        f = o["finding"]
        rid = f["ruleId"]
        if f["fingerprint"] is None:
            u = {"findingId": o["findingId"], "ruleId": rid, "subjectId": f["subjectId"], "subjectPath": f["subject"]["logicalPath"],
                 "severity": f["severity"], "waived": o["findingId"] in waived}
            if f["correspondence"]["reason"]:
                u["correspondenceReason"] = f["correspondence"]["reason"]
            unmatched.append(u)
            continue
        b = bind[rid]
        entry = {"fingerprint": f["fingerprint"], "ruleId": rid, "detectorId": detector_id(b), "stabilityClass": b["stabilityClass"],
                 "subjectPath": f["subject"]["logicalPath"], "waived": o["findingId"] in waived}
        prev = matched.get(f["fingerprint"])
        if prev is not None and prev != entry:
            raise Refusal("BASELINE.ENTRY_PROJECTION_CONFLICT", f["fingerprint"])
        matched[f["fingerprint"]] = entry
    rules = {r["ruleId"]: r for r in policy["rules"]}
    results = {r["ruleId"]: r for r in proof["ruleResults"]}
    roots = {}
    for p in proof["predicateProofs"]:
        if p["predicateId"] == "p":
            roots.setdefault(p["ruleId"], []).append(p["value"])
    # HC-26: source39 absence knowledge (evaluator3 comparison-result RuleCoverage.absenceKnowledge; workflows s3 lines 360-400): a side
    # proves absence of a non-emitted fingerprint only for an enabled, evaluated rule whose outcome is not indeterminate, with complete
    # enumeration and every selected emitWhen root determinate. A disabled rule is non-selection, a separate known false.
    negative = {}
    for rid, r in rules.items():
        rr = results.get(rid)
        if not r["enabled"]:
            negative[rid] = "not-selected"
        elif rr and rr["outcome"] != "indeterminate" and rr["enumeration"]["state"] == "complete" and not rr["enumeration"]["unresolvedSubjectIds"] and \
                proof["evaluationState"] == "evaluated" and all(v in ("true", "false") for v in roots.get(rid, [])):
            negative[rid] = "complete-hit-set"
        else:
            negative[rid] = "unknown"
    return {"matched": matched, "unmatched": unmatched, "negative": negative, "rules": rules, "results": results}


def run(name):
    if name in RUNS:
        return RUNS[name]
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    if C.faults:
        raise SystemExit(f"{name}: graph admission refused {C.faults[:3]}")
    g.update(runId=exported["runId"], name=name, store=store, exported=exported, spec=store.get_record(g["plan"]["analysisSpecDigest"]))
    g["closureDescs"] = {row["id"]: store.get_object(row["id"]) for row in exported["objectTable"] if row["domain"] == "closure"}
    findings = []
    for fid in g["proof"]["findingIds"]:
        f = store.get_object(fid)
        findings.append({"findingId": fid, "finding": f, "subjectPath": f["subject"]["logicalPath"]})
    g["occ"] = project(findings, g["proof"], g["policy"], g["emission"])
    RUNS[name] = g
    return g


def evaluation_context(g):
    imports = []
    for iid in sorted(g["plan"]["importIds"], key=enc):
        w = g["imports"][iid]["wrapper"]
        imports.append({"kind": w["kind"], "importId": iid, "payloadDigest": w["payloadDigest"], "sourceCorrespondenceDigest": w["sourceCorrespondenceDigest"],
                        "scopeDigest": w["scopeDigest"], "observationDigest": w["observationDigest"]})
    sel_views = ["view2:" + r["digest"] for r in g["proof"]["evaluationInputRefs"] if r["domain"] == "view"]
    relations = sorted({g["scopes"][sid]["relation"] for v in sel_views for sid in g["views"][v]["scopeIds"]}, key=enc)
    return {"policyDigest": g["plan"]["policyDigest"], "scopeDigest": K.raw_digest(g["scope_document"]), "waiverSetDigest": g["plan"]["waiverDigest"],
            "detectorClosureIds": sorted({b["detectorClosure"] for b in g["emission"]["rules"]}, key=enc),
            "evidenceAvailability": {"importKinds": sorted({i["kind"] for i in imports}, key=enc), "relations": relations, "imports": imports}}


def detector_map(g):
    return {detector_id(b): (b["detectorClosure"], b["semanticsMajor"]) for b in g["emission"]["rules"]}


def adopt_baseline(g, exported_at="2026-09-12T00:00:00Z"):
    if g["scope_document"] is None or K.raw_digest(g["scope_document"]) not in {p["payloadDigest"] for p in g["spec"]["parameters"]}:
        raise Refusal("BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER", g["name"])
    occ, policy = g["occ"], g["policy"]
    dm = {}
    for b in sorted(g["emission"]["rules"], key=lambda r: enc(r["ruleId"])):
        d = g["closureDescs"][b["detectorClosure"]]
        dm.setdefault(detector_id(b), {"detectorId": detector_id(b), "closureId": b["detectorClosure"], "semanticsMajor": b["semanticsMajor"],
                                       "semanticVersion": d["semanticVersion"], "contributionId": b["contributionId"], "manifestDigest": d["manifestDigest"]})
    selected = set(g["plan"]["semanticClosures"])
    pivot = [{"closureId": cid, "kind": d["kind"], "manifestDigest": d["manifestDigest"], "protocolMajor": d["protocolMajor"], "platform": d["platform"]}
             for cid, d in sorted(g["closureDescs"].items(), key=lambda kv: enc(kv[0]))
             if (cid in selected or d["kind"] in ("toolchain", "stdlib")) and d["kind"] in ("detector", "evaluator", "provider", "toolchain", "stdlib")]
    rule_cov = []
    for r in sorted(policy["rules"], key=lambda r: enc(r["ruleId"])):
        rr = occ["results"][r["ruleId"]]
        missing = any(x["source"] == "import" and x["cause"] == "evidence-kind-unavailable" for x in rr["deficiencies"])
        rc = "unsatisfied" if missing else ("unknown" if rr["outcome"] == "indeterminate" else "satisfied")
        # HC-26: RuleCoverage.absenceKnowledge is recorded at adoption by the same complete-hit-set law (workflows s3 lines 390-395)
        rule_cov.append({"ruleId": r["ruleId"], "requiredCoverage": rc, "enabled": r["enabled"], "gating": gating(r, policy), "evidenceUse": r["evidenceUse"],
                         "absenceKnowledge": "complete-hit-set" if occ["negative"][r["ruleId"]] == "complete-hit-set" else "unknown"})
    desc = {"schemaFamily": "opensip.product.baseline", "schemaMajor": 2, "originProjectId": g["snapshot"]["projectId"],
            "source": {"snapshotId": g["plan"]["snapshotId"]}, "runId": g["runId"], "planId": g["plan_id"],
            "fingerprintRecipe": {"domain": "finding-fingerprint", "recipeMajor": 2}, "detectorClosure": list(dm.values()), "pivotClosure": pivot,
            "context": evaluation_context(g), "contextDocuments": {"policy": g["policy"], "scope": g["scope_document"], "waivers": g["waivers"]},
            "ruleCoverage": rule_cov, "entries": [occ["matched"][fp] for fp in sorted(occ["matched"], key=enc)],
            "unmatchedOccurrences": sorted([dict(u, side="baseline") for u in occ["unmatched"]], key=lambda u: enc(u["findingId"]))}
    pins = sorted({g["runId"]} | {p["closureId"] for p in pivot}, key=enc)
    return {"baselineId": "baseline2:" + K.H("workflow.baseline", desc), "descriptor": desc,
            "custody": {"exportedByHostRelease": "0.0.0-cb24", "exportedAtUtc": exported_at, "runRetainedAtExport": True, "retentionPins": pins}}


def verify_baseline(art):
    d = art.get("descriptor", {})
    if d.get("schemaMajor") != 2:
        return ["BASELINE.SCHEMA_MAJOR_UNSUPPORTED"]
    ok, errs = P7.admit(art, BASE_DOC, "#")
    if not ok:
        return [f"BASELINE_SCHEMA:{errs}"]
    faults = []
    if art["baselineId"] != "baseline2:" + K.H("workflow.baseline", d):
        faults.append("cb24.BASELINE_ID_MISMATCH")
    if d["fingerprintRecipe"]["recipeMajor"] != 2:
        faults.append("BASELINE.RECIPE_UNSUPPORTED")
    for name, key in (("policy", "policyDigest"), ("scope", "scopeDigest"), ("waivers", "waiverSetDigest")):
        if K.raw_digest(d["contextDocuments"][name]) != d["context"][key]:
            faults.append(f"BASELINE.CONTEXT_DOCUMENT_MISSING:{name}")
    if any(u["side"] != "baseline" for u in d["unmatchedOccurrences"]):
        faults.append("cb24.BASELINE_UNMATCHED_SIDE")
    if art["custody"]["retentionPins"] != sorted({d["runId"]} | {p["closureId"] for p in d["pivotClosure"]}, key=enc):
        faults.append("cb24.BASELINE_RETENTION_PINS")
    return faults


def reevaluate(g, policy, scope_doc, waivers):
    bind = {r["ruleId"]: r for r in g["emission"]["rules"]}
    missing = [r["ruleId"] for r in policy["rules"] if r["ruleId"] not in bind]
    if missing:
        raise Refusal("cb24.PIVOT_RULE_WITHOUT_CURRENT_BINDING", ",".join(missing))
    emission = {"schemaVersion": 1, "policyDigest": K.raw_digest(policy),
                "rules": [bind[r["ruleId"]] for r in sorted(policy["rules"], key=lambda r: enc(r["ruleId"]))]}
    plan = dict(g["plan"], policyDigest=K.raw_digest(policy), waiverDigest=K.raw_digest(waivers))
    im = g["imports"]
    inp = EV.Inputs(plan=plan, plan_id=g["plan_id"], exec_plan_id=g["exec_plan_id"], evaluator_closure=g["xi"]["evaluatorClosure"],
                    policy=policy, waivers=waivers, emission=emission, enum_plan=g["enum"], inventories=g["index"]["inventories"],
                    views=g["views"], scopes=g["scopes"], coverages=g["coverages"], facts=g["facts"], fact_payloads=g["payloads"], bound=g["bound"],
                    imports={i: r["wrapper"] for i, r in im.items()}, import_payloads={i: r["payload"] for i, r in im.items()},
                    import_observations={i: r["observation"] for i, r in im.items()}, import_scopes={i: r["scope"] for i, r in im.items()},
                    import_flags={i: r["flags"] for i, r in im.items()}, exec_inputs=g["xi"], exec_inputs_digest=g["proof"]["executionInputsDigest"],
                    required_rows=g["derived"]["requiredRows"], scope_document=scope_doc, project_id=g["snapshot"]["projectId"])
    out = EV.evaluate(inp)
    if out["proof"]["evaluationInputRefs"] != g["proof"]["evaluationInputRefs"]:
        raise Refusal("EVALUATION.FINDING_JOIN_REFUSED", "pivot evaluation inputs differ from the current admitted inputs")
    view = project(out["findings"], out["proof"], policy, emission)
    view.update(proofId=out["proofId"], mintedRun=False, evaluationInputRefsEqualCurrent=True)
    return view


def presence(view, fp, rid, path, scope_doc):
    """HC-26: evaluator3 comparison-result $defs/PivotPresence and workflows s3 lines 376-400 for a pivot or the current side.
    true = known matched occurrence; false = non-selection (rule not enabled, or its include/exclude or that side's ScopeDocument does
    not select the path) or evaluated absence (complete-hit-set and no unmatched occurrence of the same rule on the same path, the
    barrier that applies where no stronger relation is retained); null = not known."""
    if fp in view["matched"]:
        return True
    rule = view["rules"].get(rid)
    if rule is None or not rule["enabled"]:
        return False
    se = rule["subjectEnumeration"]
    if not EV.rule_enumeration_selects(se.get("include"), se.get("exclude"), path) or \
            (scope_doc is not None and not EV.scope_document_selects(scope_doc, path)):
        return False
    if view["negative"].get(rid) != "complete-hit-set" or any(u["ruleId"] == rid and u["subjectPath"] == path for u in view["unmatched"]):
        return None
    return False


def baseline_presence(d, fp, rid, path):
    """HC-26: B presence from the artifact alone - an entry is true; non-selection under the embedded baseline policy/ScopeDocument is
    false; evaluated absence requires RuleCoverage.absenceKnowledge=complete-hit-set and no retained unmatchedOccurrences row of the
    same rule and path; otherwise null."""
    if any(e["fingerprint"] == fp for e in d["entries"]):
        return True
    rule = next((r for r in d["contextDocuments"]["policy"]["rules"] if r["ruleId"] == rid), None)
    if rule is None or not rule["enabled"]:
        return False
    se = rule["subjectEnumeration"]
    if not EV.rule_enumeration_selects(se.get("include"), se.get("exclude"), path) or \
            not EV.scope_document_selects(d["contextDocuments"]["scope"], path):
        return False
    rc = next((r for r in d["ruleCoverage"] if r["ruleId"] == rid), None)
    if rc is None or rc["absenceKnowledge"] != "complete-hit-set" or \
            any(u["ruleId"] == rid and u["subjectPath"] == path for u in d["unmatchedOccurrences"]):
        return None
    return False


def transition(a, b):
    for x in (a, b):
        if isinstance(x, tuple):
            return ("unavailable", x[1])
    if a is None or b is None:
        return ("none", None) if a is b else ("unknown", None)
    if (a is True) == (b is True):
        return ("none", None)
    return ("appeared" if b is True else "vanished", None)


def ser(v, boolean=False):
    if v is True:
        return True
    if boolean:
        return False
    return False if v is False else None


def compare(art, cur, profile_name, e0_name=None, available=("E1", "E2", "E3"), accept=()):
    prof = PROFILES[profile_name]
    d = art["descriptor"]
    g = run(cur)
    cur_ctx, base_ctx = evaluation_context(g), d["context"]
    base_dm = {x["detectorId"]: (x["closureId"], x["semanticsMajor"]) for x in d["detectorClosure"]}
    cur_dm = detector_map(g)
    delta = {"codeChanged": d["source"]["snapshotId"] != g["plan"]["snapshotId"], "detectorChanged": base_dm != cur_dm,
             "policyChanged": base_ctx["policyDigest"] != cur_ctx["policyDigest"], "scopeChanged": base_ctx["scopeDigest"] != cur_ctx["scopeDigest"],
             "waiversChanged": base_ctx["waiverSetDigest"] != cur_ctx["waiverSetDigest"],
             "evidenceAvailabilityChanged": base_ctx["evidenceAvailability"] != cur_ctx["evidenceAvailability"]}
    project_ok = d["originProjectId"] == g["snapshot"]["projectId"]
    corr = "same-project" if project_ok else ("declared" if d["originProjectId"] in accept else "unmapped")
    common = {"schemaFamily": "opensip.product.comparison", "schemaMajor": 2, "baselineId": art["baselineId"], "currentRunId": g["runId"],
              "currentSnapshotId": g["plan"]["snapshotId"], "auditProfile": prof, "projectCorrespondence": corr, "baselineContext": base_ctx,
              "currentContext": cur_ctx, "contextDelta": delta, "currentEvaluationState": g["proof"]["evaluationState"],
              "currentExecutionDeficiencies": g["proof"]["executionDeficiencies"]}
    whole = None
    if d["fingerprintRecipe"]["recipeMajor"] != 2:
        whole = ("baseline-recipe-unsupported", "BASELINE.RECIPE_UNSUPPORTED", "adopt a baseline with a supported fingerprint recipe")
    elif corr == "unmapped":
        whole = ("baseline-project-unmapped", "BASELINE.PROJECT_UNMAPPED", "adopt a baseline for this project or pass --accept-origin for its origin project")
    elif any(K.raw_digest(d["contextDocuments"][n]) != base_ctx[k] for n, k in (("policy", "policyDigest"), ("scope", "scopeDigest"), ("waivers", "waiverSetDigest"))):
        whole = ("baseline-context-document-missing", "BASELINE.CONTEXT_DOCUMENT_MISSING", "re-export the baseline with its embedded context documents")
    if whole:
        desc = dict(common, comparisonPerformed=False, wholeIndeterminateReason=whole[0],
                    remedy={"code": whole[1], "remedy": whole[2], "subject": d["originProjectId"]},
                    pivotsAvailable={k: "unavailable" for k in ("E0", "E1", "E2", "E3")}, detectors=[], ruleDeficiencies=[], entries=[],
                    counts=dict({c: 0 for c in CLASSIFICATIONS}, gating=0), verdict="indeterminate", unmatchedOccurrences=[], correspondenceCoverage=[])
        return finalize(desc, g, {})
    detectors, methods = [], {}
    for did in sorted(set(base_dm) | set(cur_dm), key=enc):
        b, c = base_dm.get(did), cur_dm.get(did)
        if b and c and b == c:
            m = "identical-closure"
        elif b is None:
            m = "detector-added"
        else:
            compat = False
            if c is not None and c[1] == b[1]:
                adm = DC.admit_listing(g["store"], c[0], g["closureDescs"][c[0]], "retained-generation")
                if adm["state"] == "refused":
                    raise Refusal(adm["firstRefusal"], c[0])
                compat = DC.declared_compatible(adm, b[0], b[1])
            m = "declared-compatible" if compat else (("three-way-pivot" if c is not None else "detector-removed") if e0_name else "indeterminate")
        methods[did] = m
        disp = {"detectorId": did, "baselineClosureId": b[0] if b else None, "currentClosureId": c[0] if c else None,
                "baselineSemanticsMajor": b[1] if b else None, "currentSemanticsMajor": c[1] if c else None, "method": m}
        if m in ("three-way-pivot", "detector-removed"):
            disp["pivotRunId"] = run(e0_name)["runId"]
        if m == "indeterminate":
            disp["indeterminateReason"] = "pivot-detector-unavailable"
        detectors.append(disp)
    need_e0 = any(m in ("three-way-pivot", "detector-removed", "indeterminate") for m in methods.values())
    e0 = None
    if need_e0 and e0_name:
        g0 = run(e0_name)
        if g0["plan"]["snapshotId"] != g["plan"]["snapshotId"]:
            raise Refusal("cb24.E0_PIVOT_NOT_OVER_CURRENT_SOURCE", e0_name)
        if detector_map(g0) != base_dm:
            raise Refusal("cb24.E0_DETECTOR_MAP_DISAGREES_WITH_BASELINE", e0_name)
        c0 = evaluation_context(g0)
        if any(c0[k] != base_ctx[k] for k in ("policyDigest", "scopeDigest", "waiverSetDigest")):
            raise Refusal("cb24.E0_CONTEXT_NOT_PRIOR", e0_name)
        e0 = g0["occ"]
    status = {"E0": "not-needed" if not need_e0 else ("available" if e0 is not None else "unavailable")}
    docs = d["contextDocuments"]
    subst = {"E1": (docs["policy"], docs["scope"], docs["waivers"]), "E2": (g["policy"], docs["scope"], docs["waivers"]),
             "E3": (g["policy"], g["scope_document"], docs["waivers"])}
    need = {"E1": delta["policyChanged"], "E2": delta["scopeChanged"], "E3": delta["waiversChanged"]}
    views = {"E4": g["occ"], "E0": e0}
    for k in ("E3", "E2", "E1"):
        if not need[k]:
            status[k] = "not-needed"
        elif k in available:
            views[k] = reevaluate(g, *subst[k])
            status[k] = "available"
        else:
            status[k] = "unavailable"
    base_entries = {e["fingerprint"]: e for e in d["entries"]}
    base_rc = {r["ruleId"]: r for r in d["ruleCoverage"]}
    meta = {}
    for src, view in (("current", views["E4"]), ("E3", views.get("E3")), ("E2", views.get("E2")), ("E1", views.get("E1")), ("E0", e0)):
        if view:
            for fp, e in view["matched"].items():
                meta.setdefault(fp, dict(e, source=src))
    for fp, e in base_entries.items():
        meta.setdefault(fp, dict(e, source="baseline"))
    entries, summary = [], []
    cur_rules = g["occ"]["rules"]
    bimp = {}
    for i in base_ctx["evidenceAvailability"]["imports"]:
        bimp.setdefault(i["kind"], []).append(i["importId"])
    cimp = {}
    for i in cur_ctx["evidenceAvailability"]["imports"]:
        cimp.setdefault(i["kind"], []).append(i["importId"])
    changed_pivots = [p for p, flag in (("E0", delta["detectorChanged"]), ("E1", delta["policyChanged"]), ("E2", delta["scopeChanged"]),
                                        ("E3", delta["waiversChanged"])) if flag]
    pivot_scope = {"E1": docs["scope"], "E2": docs["scope"], "E3": g["scope_document"]}
    for fp in sorted(meta, key=enc):
        m = meta[fp]
        rid, path = m["ruleId"], m["subjectPath"]
        # HC-26: one presence-knowledge law on every side (workflows s3 lines 376-400; evaluator3 comparison-result $defs/PivotPresence)
        vals = {"B": baseline_presence(d, fp, rid, path), "E4": presence(views["E4"], fp, rid, path, g["scope_document"])}
        for k in ("E3", "E2", "E1"):
            nxt = {"E3": "E4", "E2": "E3", "E1": "E2"}[k]
            vals[k] = vals[nxt] if status[k] == "not-needed" else (("UNAVAILABLE", k) if status[k] == "unavailable" else
                                                                   presence(views[k], fp, rid, path, pivot_scope[k]))
        vals["E0"] = vals["E1"] if status["E0"] == "not-needed" else (("UNAVAILABLE", "E0") if status["E0"] == "unavailable" else
                                                                      presence(e0, fp, rid, path, docs["scope"]))
        waived_b = bool(base_entries.get(fp, {}).get("waived", False))
        waived_c = bool(views["E4"]["matched"].get(fp, {}).get("waived", False))
        waived_3 = bool(views["E3"]["matched"].get(fp, {}).get("waived", False)) if status["E3"] == "available" else waived_c
        seq = [vals[k] for k in ("B", "E0", "E1", "E2", "E3")]
        trans = [transition(seq[i], seq[i + 1]) for i in range(4)]
        must(f"E3-E4-presence-equal:{cur}:{fp[:24]}", (vals["E3"] is True) == (vals["E4"] is True) or status["E3"] == "unavailable", vals)
        cls, direction, reason, first, subsequent = None, None, None, None, []
        for i, (t, piv) in enumerate(trans):
            if cls is None:
                if t in ("unavailable", "unknown"):
                    # workflows s3: a first attributable change resting on a null value is INDETERMINATE; an earlier known change keeps its class
                    cls = "INDETERMINATE"
                    break
                if t in ("appeared", "vanished"):
                    cls, direction, first = CLASS[AXES[i]][0 if t == "appeared" else 1], t, i
            elif t in ("appeared", "vanished"):
                subsequent.append(AXES[i])
        both_present = vals["E3"] is True and vals["E4"] is True
        if cls is None:
            if both_present and waived_3 != waived_c:
                cls, direction = "WAIVER-DELTA", "waiver-added" if waived_c else "waiver-removed"
            else:
                cls = "UNCHANGED"
        elif cls != "INDETERMINATE" and both_present and waived_3 != waived_c:
            subsequent.append("waiver")
        # HC-26: closed first-applicable IndeterminateReason order (workflows s3 lines 402-411).
        # (1) a changed axis's pivot presence is null, whether unbound or bound without presence knowledge
        if cls == "INDETERMINATE" and any(vals[p] is None or isinstance(vals[p], tuple) for p in changed_pivots):
            reason = "pivot-reevaluation-unavailable"
        gB = bool(base_rc.get(rid, {}).get("gating", False))
        gC = gating(cur_rules[rid], g["policy"]) if rid in cur_rules else False
        ev_rule = cur_rules.get(rid) or {"evidenceUse": base_rc.get(rid, {}).get("evidenceUse", [])}
        ev = {e["kind"]: e["requirement"] for e in ev_rule["evidenceUse"]}
        changed = [k for k in ev if sorted(bimp.get(k, [])) != sorted(cimp.get(k, []))] if delta["evidenceAvailabilityChanged"] else []
        if changed and reason != "pivot-reevaluation-unavailable":
            # (2) the evidence axis, per declared evidenceUse in declaration order
            first_change = next((t for t, _ in trans if t in ("appeared", "vanished")), None)
            ev_reason = None
            for k in changed:
                if ev[k] == "required" and not cimp.get(k):
                    ev_reason = "required-evidence-unavailable"
                elif gB or gC:
                    ev_reason = "evidence-availability-changed" if bool(bimp.get(k)) != bool(cimp.get(k)) else "evidence-content-changed"
                if ev_reason:
                    break
            if ev_reason:
                cls, direction, reason, subsequent = "INDETERMINATE", None, ev_reason, []
            elif first_change:
                cls, direction, reason, subsequent = "EVIDENCE-DELTA", first_change, None, []
            elif cls != "INDETERMINATE":
                cls, direction, reason, subsequent = "UNCHANGED", None, None, []
        if cls == "INDETERMINATE" and reason is None:
            disp = next((x for x in detectors if x["detectorId"] == m["detectorId"] and x["method"] == "indeterminate"), None)
            if disp is not None:
                reason = disp["indeterminateReason"]  # (3) the detector disposition's own reason
            elif vals["B"] is None:
                reason = "baseline-absence-unknown"  # (4)
            elif vals["E4"] is None:
                reason = "current-absence-unknown"  # (5)
        must(f"indeterminate-reason-derived:{cur}:{fp[:24]}", cls != "INDETERMINATE" or reason is not None, vals)
        approximated = False
        rule_gates = (gB or gC) if prof["gateRuleUnder"] == "baseline-or-current" else gC
        live = vals["E4"] is True and not waived_c
        gates, gate_reason = False, None
        if cls == "CODE-NET-NEW" and prof["gateCodeNetNew"] and rule_gates:
            if live:
                gates, gate_reason = True, "code-net-new"
            elif not (prof["newWaiverSuppressesCodeNetNew"] and vals["E4"] is True and waived_c) and prof["gateRuleUnder"] == "baseline-or-current":
                gates, gate_reason = True, "code-net-new-policy-hidden"
        if not gates and prof["gateNewlyLiveByPolicyAxes"] and cls in ("POLICY-DELTA", "SCOPE-DELTA", "WAIVER-DELTA") and \
                direction in ("appeared", "waiver-removed") and live and rule_gates:
            gates, gate_reason = True, "newly-live-policy-axis"
        if not gates and prof["gateAllCurrentLive"] and live and gC and cls != "INDETERMINATE":
            gates, gate_reason = True, "current-live"
        entry = {"fingerprint": fp, "ruleId": rid, "detectorId": m["detectorId"],
                 "presence": {"B": ser(vals["B"]), "E0": ser(vals["E0"]), "E1": ser(vals["E1"]), "E2": ser(vals["E2"]), "E3": ser(vals["E3"]),
                              "E4": ser(vals["E4"]), "waivedB": waived_b, "waivedC": waived_c},
                 "classification": cls, "subsequentDeltas": subsequent, "liveInCurrent": live, "gates": gates}
        if direction:
            entry["direction"] = direction
        if reason:
            entry["indeterminateReason"] = reason
        if gate_reason:
            entry["gateReason"] = gate_reason
        entries.append(entry)
        summary.append({"fingerprint": fp, "ruleId": rid, "subjectPath": m["subjectPath"], "source": m["source"],
                        "semanticsMajor": (base_dm if m["source"] in ("baseline", "E0") else cur_dm).get(m["detectorId"], (None, None))[1],
                        "classification": cls, "direction": direction, "indeterminateReason": reason, "subsequentDeltas": subsequent,
                        "gates": gates, "gateReason": gate_reason, "ruleGates": rule_gates, "reasonApproximated": approximated, "pivotValues": {k: (list(v) if isinstance(v, tuple) else v) for k, v in vals.items()}})
    all_rules = sorted(set(cur_rules) | set(base_rc), key=enc)
    rdefs, ccov = [], []
    base_unmatched = d["unmatchedOccurrences"]
    for rid in all_rules:
        gB = bool(base_rc.get(rid, {}).get("gating", False))
        r = cur_rules.get(rid)
        gC = gating(r, g["policy"]) if r else False
        rg = (gB or gC) if prof["gateRuleUnder"] == "baseline-or-current" else gC
        rr = g["occ"]["results"].get(rid)
        matched_n = sum(1 for e in g["occ"]["matched"].values() if e["ruleId"] == rid)
        unmatched_n = sum(1 for u in g["occ"]["unmatched"] if u["ruleId"] == rid)
        if prof["gateRuleUnder"] == "baseline-or-current":
            unmatched_n += sum(1 for u in base_unmatched if u["ruleId"] == rid and gB)
        pop_unknown = bool(r and r["enabled"] and rr and rr["enumeration"]["state"] != "complete")
        ccov.append({"ruleId": rid, "gating": rg, "matchedCount": matched_n, "unmatchedCount": unmatched_n, "populationUnknown": pop_unknown,
                     "zeroFindings": matched_n + unmatched_n == 0})
        cause = None
        if r and rr and r["enabled"]:
            req = {e["kind"] for e in r["evidenceUse"] if e["requirement"] == "required"}
            if any(x["source"] == "import" and x["cause"] == "evidence-kind-unavailable" and x["evidenceKind"] in req for x in rr["deficiencies"]):
                cause = "required-evidence-unavailable"
            elif rr["outcome"] == "indeterminate":
                cause = "required-coverage-unknown"
        if cause is None and rg and (unmatched_n > 0 or pop_unknown):
            cause = "correspondence-incomplete"
        if cause:
            rdefs.append({"ruleId": rid, "gating": rg, "cause": cause})
    rg_of = {s["fingerprint"]: s["ruleGates"] for s in summary}
    if any(e["gates"] for e in entries):
        verdict = "fail"
    elif any(e["classification"] == "INDETERMINATE" and rg_of[e["fingerprint"]] for e in entries) or any(x["gating"] for x in rdefs):
        verdict = "indeterminate"
    else:
        verdict = "pass"
    counts = {c: sum(1 for e in entries if e["classification"] == c) for c in CLASSIFICATIONS}
    counts["gating"] = sum(1 for e in entries if e["gates"])
    unmatched = sorted([dict(u) for u in base_unmatched] + [dict(u, side="current") for u in g["occ"]["unmatched"]],
                       key=lambda u: (enc(u["side"]), enc(u["findingId"])))
    desc = dict(common, comparisonPerformed=True, pivotsAvailable=status, detectors=detectors, ruleDeficiencies=rdefs, entries=entries,
                counts=counts, verdict=verdict, unmatchedOccurrences=unmatched, correspondenceCoverage=ccov)
    return finalize(desc, g, {"summary": summary, "pivotViews": {k: {"proofId": v.get("proofId"), "mintedRun": v.get("mintedRun", True),
                                                                        "evaluationInputRefsEqualCurrent": v.get("evaluationInputRefsEqualCurrent")}
                                                                    for k, v in views.items() if v and k != "E4"},
                                  "e0Run": e0_name if e0 is not None else None})


def finalize(desc, g, extra):
    res = {"comparisonResultId": "comparison2:" + K.H("workflow.comparison", desc), "descriptor": desc}
    ok, errs = P7.admit(res, CMP_DOC, "#")
    d = desc
    sr = {"kind": "comparison", "comparisonResultId": res["comparisonResultId"], "currentRunId": d["currentRunId"], "baselineId": d["baselineId"],
          "verdict": d["verdict"], "comparisonPerformed": d["comparisonPerformed"],
          "counts": {"entries": len(d["entries"]), "gating": d["counts"]["gating"], "indeterminate": d["counts"]["INDETERMINATE"]}}
    if d["verdict"] == "fail":
        term = {"class": "policy-failed", "runId": d["currentRunId"]}
    elif d["verdict"] == "pass":
        term = {"class": "success", "runId": d["currentRunId"]}
    else:
        # HC-26: under the closed per-entry order an entry whose E0 pivot is null publishes pivot-reevaluation-unavailable (reason 1), so the
        # detector's own unavailability is read from the detector dispositions rather than from entry reasons
        disp_reasons = {x.get("indeterminateReason") for x in d["detectors"] if x.get("method") == "indeterminate"}
        recipe = bool(d.get("wholeIndeterminateReason")) or bool(disp_reasons & {"pivot-detector-unavailable", "pivot-closure-revoked", "pivot-closure-incompatible"})
        sr["d9Deficiency"] = "baseline-recipe-unsupported" if recipe else "verdict-indeterminate"
        term = {"class": "indeterminate", "reasonCodes": ["BASELINE.RECIPE_UNSUPPORTED" if recipe else "VERDICT.INDETERMINATE"]}
        detail = d.get("remedy")
        if detail is None and "pivot-detector-unavailable" in disp_reasons:
            detail = {"code": "BASELINE.PIVOT_DETECTOR_UNAVAILABLE", "remedy": "install or supply the baseline detector closure so the E0 pivot can run"}
        if detail is None and any(x["cause"] == "required-evidence-unavailable" and x["gating"] for x in d["ruleDeficiencies"]):
            detail = {"code": "COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE", "remedy": "re-import the required evidence for the current snapshot"}
        if detail:
            term["domainDetail"] = detail
            sr["remedy"] = detail
    sok, serrs = P7.admit(sr, INVOC3, "#/$defs/ComparisonStepResult")
    tok, terrs = P7.admit(term, COMMON3, "#/$defs/StepTermination")
    step = {"result": sr, "termination": term, "exitCode": P7.EXIT[term["class"]], "resultAdmitted": sok, "resultErrors": serrs,
            "terminationAdmitted": tok, "terminationErrors": terrs}
    must(f"comparison-schema:{g['name']}:{d['auditProfile']['name']}", ok, errs)
    must(f"comparison-step:{g['name']}:{d['auditProfile']['name']}", sok and tok, (serrs, terrs))
    must(f"comparison-id-recomputes:{g['name']}", res["comparisonResultId"] == "comparison2:" + K.H("workflow.comparison", res["descriptor"]))
    return {"comparison": res, "schemaAdmitted": ok, "schemaErrors": errs, "step": step, **extra}


def pick(out, rule, path, major=None, source=None):
    rows = [s for s in out.get("summary", []) if s["ruleId"] == rule and s["subjectPath"] == path and
            (major is None or s["semanticsMajor"] == major) and (source is None or s["source"] == source)]
    return rows


def brief(out):
    d = out["comparison"]["descriptor"]
    return {"verdict": d["verdict"], "comparisonPerformed": d["comparisonPerformed"], "contextDelta": d["contextDelta"],
            "pivotsAvailable": d["pivotsAvailable"], "counts": d["counts"], "ruleDeficiencies": d["ruleDeficiencies"],
            "entries": [{k: s[k] for k in ("ruleId", "subjectPath", "semanticsMajor", "source", "classification", "direction", "indeterminateReason",
                                           "subsequentDeltas", "gates", "gateReason", "pivotValues")} for s in out.get("summary", [])],
            "termination": out["step"]["termination"], "exitCode": out["step"]["exitCode"]}


def audit_invocation(cur, out, profile, n):
    g = run(cur)
    step = out["step"]

    def spec(i, kind, params, deps, gate):
        return {"stepId": i, "kind": kind, "requirement": "required", "dependsOn": deps, "dependencyGate": gate, "retryPolicy": "none", "params": params}
    ordered = [spec(0, "analysis", {"kind": "analysis", "profile": "audit", "role": "primary", "verdictGate": "delegated", "durability": "authoritative",
                                    "snapshotSource": "live-worktree", "baseline": {"path": "opensip.baseline.json", "auditProfile": profile}}, [], "completed"),
               spec(1, "comparison", {"kind": "comparison", "currentStep": 0, "baseline": "opensip.baseline.json", "auditProfile": profile}, [0], "completed"),
               spec(2, "render", {"kind": "render", "format": "json", "destination": "stdout", "sourceSteps": [0, 1], "required": True}, [0, 1], "terminal")]
    ar = {"kind": "analysis", "authority": "authoritative", "runId": g["runId"], "planId": g["plan_id"], "verdict": g["proof"]["verdict"],
          "requiredCoverage": "satisfied", "durability": "committed", "deficiency": "none", "secondaryDeficiencies": []}
    results = [{"stepId": 0, "outcome": "completed", "attempts": [{"executionId": P7.exec_id(n), "outcome": "completed",
                                                                  "derivation": {"planId": g["plan_id"], "executionPlanId": g["exec_plan_id"], "stageCount": 1, "stagesCompleted": 1}}],
                "result": ar, "termination": {"class": "success", "runId": g["runId"]}},
               {"stepId": 1, "outcome": "completed", "attempts": [{"executionId": P7.exec_id(n + 1), "outcome": "completed"}],
                "result": step["result"], "termination": step["termination"]},
               {"stepId": 2, "outcome": "completed", "attempts": [{"executionId": P7.exec_id(n + 2), "outcome": "completed"}],
                "result": {"kind": "render", "format": "json", "rendererVersion": 3, "bytes": 4096, "truncation": False, "written": True},
                "termination": {"class": "success"}}]
    order = ["operational-failed", "request-rejected", "policy-failed", "indeterminate", "success"]
    agg = min((r["termination"] for r in results), key=lambda t: order.index(t["class"]))
    record = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": P7.req_id(n), "projectId": g["snapshot"]["projectId"],
              "workflow": {"kind": "builtin", "name": "audit"}, "mode": {"interactive": False, "ci": True, "ephemeral": False},
              "orderedSteps": ordered, "stepResults": results, "termination": agg, "terminationEmitted": True}
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "invocation", "requestId": record["requestId"], "projectId": record["projectId"],
           "termination": agg, "exitCode": P7.EXIT[agg["class"]], "invocation": record}
    faults = P7.check_envelope(env)
    must(f"audit-invocation:{cur}", not faults, faults)
    return {"envelope": env, "envelopeFaults": faults, "inventoryAuditSteps": P7.INVENTORY["audit"]["steps"]}


def main():
    base = run("cmp-base")
    art = adopt_baseline(base)
    vf = verify_baseline(art)
    must("baseline-admits", not vf, vf)
    negatives = []
    for label, mutate, expect in (
            ("entry-waived-flag-flipped-no-remint", lambda a: a["descriptor"]["entries"][0].update(waived=not a["descriptor"]["entries"][0]["waived"]), "cb24.BASELINE_ID_MISMATCH"),
            ("schema-major-1", lambda a: a["descriptor"].update(schemaMajor=1), "BASELINE.SCHEMA_MAJOR_UNSUPPORTED"),
            ("embedded-policy-edited-reminted", lambda a: (a["descriptor"]["contextDocuments"]["policy"].update(gateSeverityAtLeast="error"),
                                                          a.update(baselineId="baseline2:" + K.H("workflow.baseline", a["descriptor"]))), "BASELINE.CONTEXT_DOCUMENT_MISSING:policy"),
            ("entries-reversed-reminted", lambda a: (a["descriptor"].update(entries=list(reversed(a["descriptor"]["entries"]))),
                                                    a.update(baselineId="baseline2:" + K.H("workflow.baseline", a["descriptor"]))), "BASELINE_SCHEMA"),
            ("retention-pin-dropped", lambda a: a["custody"].update(retentionPins=a["custody"]["retentionPins"][:-1]), "cb24.BASELINE_RETENTION_PINS")):
        bad = copy.deepcopy(art)
        mutate(bad)
        fl = verify_baseline(bad)
        ok = bool(fl) and fl[0].startswith(expect)
        must(f"baseline-negative:{label}", ok, fl)
        negatives.append({"vector": label, "classification": "invalid", "firstRefusal": fl[0] if fl else None, "masksLater": fl[1:], "pass": ok})
    try:
        adopt_baseline(run("rust-mixed"))
        no_scope = {"vector": "adopt-run-without-scope-document-parameter", "firstRefusal": None, "note": "rust-mixed selects a ScopeDocumentV1; control not constructible"}
    except Refusal as exc:
        no_scope = {"vector": "adopt-run-without-scope-document-parameter", "classification": "invalid", "firstRefusal": exc.key, "pass": exc.key == "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER"}

    # ---- R-BASELINE-AUDIT: code regression under every profile, identity comparison, audit invocation
    code = {p: compare(art, "cmp-code", p) for p in PROFILES}
    helper = pick(code["code-regression"], "cb24.ts.external-call", "src/util.ts")
    must("code-regression-helper-code-net-new", helper and helper[0]["classification"] == "CODE-NET-NEW" and helper[0]["gateReason"] == "code-net-new", helper)
    must("code-regression-verdicts", [code[p]["comparison"]["descriptor"]["verdict"] for p in PROFILES] == ["fail", "fail", "fail", "pass"],
         [code[p]["comparison"]["descriptor"]["verdict"] for p in PROFILES])
    others = [s for s in code["code-regression"]["summary"] if s["subjectPath"] != "src/util.ts" or s["ruleId"] != "cb24.ts.external-call"]
    must("code-regression-others-unchanged", all(s["classification"] == "UNCHANGED" for s in others), [(s["ruleId"], s["classification"]) for s in others])
    ident = compare(art, "cmp-base", "code-regression")
    must("identity-comparison-pass-over-failing-run", ident["comparison"]["descriptor"]["verdict"] == "pass" and run("cmp-base")["proof"]["verdict"] == "fail"
         and ident["step"]["termination"]["class"] == "success")
    inv_fail = audit_invocation("cmp-code", code["code-regression"], "code-regression", 900)
    inv_pass = audit_invocation("cmp-base", ident, "code-regression", 910)
    must("audit-invocation-aggregate", inv_fail["envelope"]["exitCode"] == 1 and inv_pass["envelope"]["exitCode"] == 0,
         (inv_fail["envelope"]["exitCode"], inv_pass["envelope"]["exitCode"]))
    dump("vectors/baseline-audit.json", {
        "classification": "valid", "baselineRun": "cmp-base", "baselineArtifact": art, "freshHostAdmission": vf, "baselineNegatives": negatives,
        "adoptionScopeParameterControl": no_scope,
        "codeRegressionByProfile": {p: brief(o) for p, o in code.items()}, "identityComparison": brief(ident),
        "auditInvocationFail": inv_fail, "auditInvocationPass": inv_pass,
        "goldens": ["audit-inherited-run-fail-comparison-pass (success)", "audit-code-regression-under-policy-change (policy-failed; see pivot-only-fingerprints.json)"],
        "cb24Choices": ["detectorId = emission contributionId", "unchanged-axis pivots copy the next pivot", "RuleCoverage.requiredCoverage derivation",
                        "exportedAtUtc/exportedByHostRelease are synthetic trusted custody inputs", "pivotClosure keeps descriptor platform 'any' (no host rewrite)"],
        "comparisons": {p: o["comparison"] for p, o in code.items()}})

    # ---- R-SCOPE-POLICY-ONLY-COMPARISON
    scope = {p: compare(art, "cmp-scope", p) for p in ("code-regression", "policy-change")}
    sd = scope["code-regression"]["comparison"]["descriptor"]
    g_scope = run("cmp-scope")
    cold = pick(scope["code-regression"], "cb24.ts.cold-file", "src/util.ts")
    must("scope-only-delta", sd["contextDelta"] == {"codeChanged": False, "detectorChanged": False, "policyChanged": False, "scopeChanged": True,
                                                  "waiversChanged": False, "evidenceAvailabilityChanged": False}, sd["contextDelta"])
    must("scope-foundation-scope-unchanged", g_scope["plan"]["scopeDigest"] == base["plan"]["scopeDigest"] and g_scope["plan"]["snapshotId"] == base["plan"]["snapshotId"])
    must("scope-cold-file-scope-delta", cold and cold[0]["classification"] == "SCOPE-DELTA" and cold[0]["direction"] == "vanished", cold)
    must("scope-E2-reevaluated", sd["pivotsAvailable"]["E2"] == "available" and scope["code-regression"]["pivotViews"]["E2"]["evaluationInputRefsEqualCurrent"])
    must("scope-verdict-pass", sd["verdict"] == "pass", sd["verdict"])
    dump("vectors/comparison-scope-policy-only.json", {
        "classification": "valid", "baselineRun": "cmp-base", "currentRun": "cmp-scope",
        "sourceAndDiscoveryScope": {"snapshotIdEqual": g_scope["plan"]["snapshotId"] == base["plan"]["snapshotId"],
                                    "foundationScopeDescriptorDigestEqual": g_scope["plan"]["scopeDigest"] == base["plan"]["scopeDigest"],
                                    "baselineScopeDocument": base["scope_document"], "currentScopeDocument": g_scope["scope_document"],
                                    "analysisSpecDigestDiffers": g_scope["plan"]["analysisSpecDigest"] != base["plan"]["analysisSpecDigest"]},
        "byProfile": {p: brief(o) for p, o in scope.items()}, "comparison": scope["code-regression"]["comparison"],
        "selectors": ["comparison-result EvaluationContext.description (scopeDigest is ScopeDocumentV1, distinct from plan.scopeDigest)",
                      "workflow-projection-contract.v3 s10 (plan.scopeDigest is not a substitute), s13 (wider baseline ScopeDocument is a real E2 counterfactual)"]})

    # ---- R-CMP-EVIDENCE-CHANGED
    ev_ng = compare(art, "cmp-evidence", "code-regression")
    gart = adopt_baseline(run("cmp-gbase"))
    must("gbase-baseline-admits", not verify_baseline(gart), verify_baseline(gart))
    ev_g = compare(gart, "cmp-gevidence", "code-regression")
    c1 = pick(ev_ng, "cb24.ts.cold-file", "src/util.ts")
    c2 = pick(ev_g, "cb24.ts.cold-file", "src/util.ts")
    must("evidence-nongating-delta", c1 and c1[0]["classification"] == "EVIDENCE-DELTA" and c1[0]["direction"] == "vanished", c1)
    must("evidence-gating-indeterminate", c2 and c2[0]["classification"] == "INDETERMINATE" and c2[0]["indeterminateReason"] == "evidence-content-changed", c2)
    must("evidence-verdicts", ev_ng["comparison"]["descriptor"]["verdict"] == "pass" and ev_g["comparison"]["descriptor"]["verdict"] == "indeterminate",
         (ev_ng["comparison"]["descriptor"]["verdict"], ev_g["comparison"]["descriptor"]["verdict"]))
    bi = ev_ng["comparison"]["descriptor"]["baselineContext"]["evidenceAvailability"]["imports"]
    ci = ev_ng["comparison"]["descriptor"]["currentContext"]["evidenceAvailability"]["imports"]
    dump("vectors/comparison-evidence-changed.json", {
        "classification": "valid", "sameKindDifferentImport": {"baseline": bi, "current": ci,
                                                             "kindsEqual": [i["kind"] for i in bi] == [i["kind"] for i in ci],
                                                             "importIdsDiffer": [i["importId"] for i in bi] != [i["importId"] for i in ci]},
        "nonGatingRule": {"baselineRun": "cmp-base", "currentRun": "cmp-evidence", **brief(ev_ng)},
        "gatingRule": {"baselineRun": "cmp-gbase", "currentRun": "cmp-gevidence", **brief(ev_g)},
        "comparisons": {"nonGating": ev_ng["comparison"], "gating": ev_g["comparison"]},
        "selectors": ["workflows-and-surfaces.md s3 lines 371-380 (evidence axis)", "lines 1395-1405 (no evidence pivot; conservative attribution)"]})

    # ---- R-CMP-MISSING
    miss = compare(gart, "cmp-gmissing", "code-regression")
    md = miss["comparison"]["descriptor"]
    c3 = pick(miss, "cb24.ts.cold-file", "src/util.ts")
    must("missing-entry-indeterminate", c3 and c3[0]["indeterminateReason"] == "required-evidence-unavailable", c3)
    must("missing-rule-deficiency", {"ruleId": "cb24.ts.cold-file", "gating": True, "cause": "required-evidence-unavailable"} in md["ruleDeficiencies"], md["ruleDeficiencies"])
    must("missing-termination-golden", miss["step"]["termination"] == {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"],
                                                                        "domainDetail": {"code": "COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE",
                                                                                         "remedy": "re-import the required evidence for the current snapshot"}},
         miss["step"]["termination"])
    gold = next(x for x in KIT.doc("workflows/command-inventory.v3.json")["goldens"] if x["id"] == "audit-required-evidence-lost")
    dump("vectors/comparison-missing.json", {"classification": "valid", "baselineRun": "cmp-gbase", "currentRun": "cmp-gmissing", **brief(miss),
                                            "golden": gold, "comparison": miss["comparison"], "stepResult": miss["step"]})

    # ---- R-CMP-EMPTY-RESULT
    eart = adopt_baseline(run("cmp-empty"))
    empty = compare(eart, "cmp-empty", "code-regression")
    ed = empty["comparison"]["descriptor"]
    must("empty-complete", ed["comparisonPerformed"] and ed["entries"] == [] and ed["verdict"] == "pass" and
         all(c["zeroFindings"] and not c["populationUnknown"] and not c["gating"] for c in ed["correspondenceCoverage"]), brief(empty))
    tart = adopt_baseline(run("ts-pass"))
    unmapped = compare(tart, "cmp-empty", "code-regression")
    ud = unmapped["comparison"]["descriptor"]
    must("unmapped-not-performed", not ud["comparisonPerformed"] and ud["entries"] == [] and ud["wholeIndeterminateReason"] == "baseline-project-unmapped"
         and unmapped["step"]["termination"]["reasonCodes"] == ["BASELINE.RECIPE_UNSUPPORTED"], brief(unmapped))
    dump("vectors/comparison-empty-result.json", {
        "classification": "valid",
        "completeEmpty": {"baselineRun": "cmp-empty", "currentRun": "cmp-empty", **brief(empty), "correspondenceCoverage": ed["correspondenceCoverage"],
                          "note": "every rule disabled on both sides: zero entries is a performed comparison with determinate empty entries; zeroFindings never asserts complete analysis"},
        "notPerformed": {"baselineRun": "ts-pass (other project)", "currentRun": "cmp-empty", **brief(unmapped), "remedy": ud.get("remedy")},
        "distinct": {"performed": [ed["comparisonPerformed"], ud["comparisonPerformed"]], "verdict": [ed["verdict"], ud["verdict"]]},
        "comparisons": {"completeEmpty": empty["comparison"], "notPerformed": unmapped["comparison"]}})

    # ---- R-E0-VS-E1-E3
    det2 = compare(art, "cmp-code-det2", "code-regression", e0_name="cmp-code")
    main1 = pick(det2, "cb24.ts.external-call", "src/index.ts", major=1)
    help1 = pick(det2, "cb24.ts.external-call", "src/util.ts", major=1)
    help2 = pick(det2, "cb24.ts.external-call", "src/util.ts", major=2)
    must("det2-main-detection-vanished", main1 and main1[0]["classification"] == "DETECTION-DELTA" and main1[0]["direction"] == "vanished", main1)
    must("det2-helper-code-net-new-hidden-by-detection", help1 and help1[0]["classification"] == "CODE-NET-NEW" and "detection" in help1[0]["subsequentDeltas"], help1)
    must("det2-helper-major2-detection-appeared", help2 and help2[0]["classification"] == "DETECTION-DELTA" and help2[0]["direction"] == "appeared", help2)
    must("det2-E0-available", det2["comparison"]["descriptor"]["pivotsAvailable"]["E0"] == "available" and
         det2["comparison"]["descriptor"]["detectors"][0]["method"] == "three-way-pivot")
    det2_no = compare(art, "cmp-code-det2", "code-regression")
    # HC-26: closed per-entry order (workflows s3 lines 402-411) - the changed detector map's E0 presence is null, so reason (1)
    # pivot-reevaluation-unavailable is first applicable; the detector disposition itself still names pivot-detector-unavailable
    must("det2-no-e0-indeterminate", det2_no["comparison"]["descriptor"]["verdict"] == "indeterminate" and
         all(s["indeterminateReason"] == "pivot-reevaluation-unavailable" for s in det2_no["summary"]) and
         all(x.get("indeterminateReason") == "pivot-detector-unavailable" for x in det2_no["comparison"]["descriptor"]["detectors"] if x["method"] == "indeterminate") and
         det2_no["step"]["termination"]["reasonCodes"] == ["BASELINE.RECIPE_UNSUPPORTED"], brief(det2_no))
    e0_refusals = []
    for label, e0n, expect in (("e0-over-baseline-source", "cmp-base", "cb24.E0_PIVOT_NOT_OVER_CURRENT_SOURCE"),
                               ("e0-with-current-detector", "cmp-code-det2", "cb24.E0_DETECTOR_MAP_DISAGREES_WITH_BASELINE")):
        try:
            compare(art, "cmp-code-det2", "code-regression", e0_name=e0n)
            e0_refusals.append({"vector": label, "firstRefusal": None, "pass": False})
            must(f"e0-refusal:{label}", False)
        except Refusal as exc:
            e0_refusals.append({"vector": label, "classification": "invalid", "firstRefusal": exc.key, "pass": exc.key == expect})
            must(f"e0-refusal:{label}", exc.key == expect, exc.key)
    detc = compare(art, "cmp-code-detc", "code-regression")
    hc = pick(detc, "cb24.ts.external-call", "src/util.ts")
    must("detc-declared-compatible", detc["comparison"]["descriptor"]["detectors"][0]["method"] == "declared-compatible" and
         detc["comparison"]["descriptor"]["pivotsAvailable"]["E0"] == "not-needed" and hc and hc[0]["gateReason"] == "code-net-new", brief(detc))
    pol = {p: compare(art, "cmp-policy", p) for p in PROFILES}
    pdis = pick(pol["policy-change"], "cb24.ts.disabled", "src/index.ts")
    must("policy-E1-reevaluated", pol["code-regression"]["comparison"]["descriptor"]["pivotsAvailable"]["E1"] == "available" and
         pol["code-regression"]["pivotViews"]["E1"]["evaluationInputRefsEqualCurrent"] and not pol["code-regression"]["pivotViews"]["E1"]["mintedRun"])
    must("policy-delta-appeared", pdis and pdis[0]["classification"] == "POLICY-DELTA" and pdis[0]["gateReason"] == "newly-live-policy-axis", pdis)
    must("policy-verdicts", [pol[p]["comparison"]["descriptor"]["verdict"] for p in PROFILES] == ["pass", "fail", "fail", "pass"],
         [pol[p]["comparison"]["descriptor"]["verdict"] for p in PROFILES])
    pol_unavail = compare(art, "cmp-policy", "code-regression", available=())
    must("policy-E1-unavailable-indeterminate", all(s["indeterminateReason"] == "pivot-reevaluation-unavailable" for s in pol_unavail["summary"]) and
         pol_unavail["comparison"]["descriptor"]["pivotsAvailable"]["E1"] == "unavailable", brief(pol_unavail))
    wv = compare(art, "cmp-waiver", "code-regression")
    wr = pick(wv, "cb24.ts.reachable", "src/index.ts")
    must("waiver-delta-removed", wr and wr[0]["classification"] == "WAIVER-DELTA" and wr[0]["direction"] == "waiver-removed" and
         wv["comparison"]["descriptor"]["pivotsAvailable"]["E3"] == "available", wr)
    g_cur, g_e0 = run("cmp-code-det2"), run("cmp-code")
    dump("vectors/baseline-e0-e3.json", {
        "classification": "valid",
        "E0": {"what": "prior detector closure executed over CURRENT source: a separately committed, admitted pivot Run",
               "pivotRun": {"name": "cmp-code", "runId": g_e0["runId"], "planId": g_e0["plan_id"], "snapshotId": g_e0["plan"]["snapshotId"],
                            "detectorClosure": sorted(detector_map(g_e0).values())},
               "currentRun": {"name": "cmp-code-det2", "runId": g_cur["runId"], "planId": g_cur["plan_id"], "snapshotId": g_cur["plan"]["snapshotId"],
                              "detectorClosure": sorted(detector_map(g_cur).values())},
               "sameSnapshotDifferentPlanAndRun": g_e0["plan"]["snapshotId"] == g_cur["plan"]["snapshotId"] and g_e0["runId"] != g_cur["runId"],
               "withE0": brief(det2), "withoutE0": brief(det2_no), "refusals": e0_refusals, "declaredCompatible": brief(detc)},
        "E1_E3": {"what": "pure re-evaluations of the current admitted inputs (same evaluationInputRefs) with the baseline's embedded policy/scope/waivers substituted; no run3 minted",
                  "E1_policy": {"currentRun": "cmp-policy", "byProfile": {p: brief(o) for p, o in pol.items()}, "pivotView": pol["code-regression"]["pivotViews"],
                                "unavailable": brief(pol_unavail)},
                  "E2_scope": "vectors/comparison-scope-policy-only.json",
                  "E3_waiver": {"currentRun": "cmp-waiver", **brief(wv), "pivotView": wv["pivotViews"]}},
        "cb24Choices": ["semanticsMajor 2 detector is modelled by fingerprint major only (evaluation logic identical); declared-compatible listing is the reserved tree file (ref/detector_compat.py)",
                        "E0 joins (snapshot, exact detector map, prior documents) refuse with cb24 keys: the kit names the refusal but no key"],
        "comparisons": {"withE0": det2["comparison"], "withoutE0": det2_no["comparison"], "declaredCompatible": detc["comparison"],
                        "policyCodeRegression": pol["code-regression"]["comparison"], "waiver": wv["comparison"]}})

    # ---- R-PIVOT-ONLY-FINGERPRINTS
    hid = {p: compare(art, "cmp-hidden", p) for p in ("code-regression", "full-current")}
    h1 = pick(hid["code-regression"], "cb24.ts.external-call", "src/util.ts")
    m1 = pick(hid["code-regression"], "cb24.ts.external-call", "src/index.ts")
    must("hidden-pivot-only-retained", h1 and h1[0]["source"] == "E1" and h1[0]["classification"] == "CODE-NET-NEW" and h1[0]["subsequentDeltas"] == ["policy"]
         and h1[0]["gateReason"] == "code-net-new-policy-hidden", h1)
    must("hidden-main-policy-vanished", m1 and m1[0]["classification"] == "POLICY-DELTA" and m1[0]["direction"] == "vanished", m1)
    must("hidden-verdicts", hid["code-regression"]["comparison"]["descriptor"]["verdict"] == "fail" and hid["full-current"]["comparison"]["descriptor"]["verdict"] == "pass",
         [hid[p]["comparison"]["descriptor"]["verdict"] for p in hid])
    fp = h1[0]["fingerprint"] if h1 else None
    gold = next(x for x in KIT.doc("workflows/command-inventory.v3.json")["goldens"] if x["id"] == "audit-code-regression-under-policy-change")
    dump("vectors/pivot-only-fingerprints.json", {
        "classification": "valid", "baselineRun": "cmp-base", "currentRun": "cmp-hidden",
        "pivotOnlyFingerprint": {"fingerprint": fp, "inBaselineEntries": fp in {e["fingerprint"] for e in art["descriptor"]["entries"]},
                                 "inCurrentMatched": fp in run("cmp-hidden")["occ"]["matched"],
                                 "presence": next((e["presence"] for e in hid["code-regression"]["comparison"]["descriptor"]["entries"] if e["fingerprint"] == fp), None)},
        "byProfile": {p: brief(o) for p, o in hid.items()}, "golden": gold, "comparison": hid["code-regression"]["comparison"],
        "selectors": ["workflows-and-surfaces.md s3 lines 334-339", "workflow-projection-contract.v3 s12"]})

    # ---- source39 absence knowledge (workflows s3 lines 376-411; evaluator3 comparison-result RuleCoverage.absenceKnowledge / PivotPresence):
    # a null B and a null E4 publish their own closed reasons instead of the former pivot-reevaluation approximation
    budget_art = adopt_baseline(run("cmp-budget"))
    bvf = verify_baseline(budget_art)
    must("budget-baseline-admits", not bvf, bvf)
    must("budget-baseline-absence-unknown", all(r["absenceKnowledge"] == "unknown" for r in budget_art["descriptor"]["ruleCoverage"] if r["enabled"]),
         budget_art["descriptor"]["ruleCoverage"])
    must("complete-baseline-absence-known", all(r["absenceKnowledge"] == "complete-hit-set" for r in art["descriptor"]["ruleCoverage"]
                                                if r["enabled"] and r["requiredCoverage"] == "satisfied"), art["descriptor"]["ruleCoverage"])
    cur_unknown = compare(art, "cmp-budget", "code-regression")
    cu = [s for s in cur_unknown["summary"] if s["source"] == "baseline"]
    must("current-absence-unknown", bool(cu) and all(s["classification"] == "INDETERMINATE" and s["indeterminateReason"] == "current-absence-unknown"
                                                     and s["pivotValues"]["E4"] is None for s in cu), brief(cur_unknown))
    base_unknown = compare(budget_art, "cmp-code", "code-regression")
    bu = base_unknown["summary"]
    must("baseline-absence-unknown", bool(bu) and all(s["classification"] == "INDETERMINATE" and s["indeterminateReason"] == "baseline-absence-unknown"
                                                      and s["pivotValues"]["B"] is None for s in bu), brief(base_unknown))
    must("absence-unknown-verdicts", cur_unknown["comparison"]["descriptor"]["verdict"] == "indeterminate" and
         base_unknown["comparison"]["descriptor"]["verdict"] == "indeterminate",
         (cur_unknown["comparison"]["descriptor"]["verdict"], base_unknown["comparison"]["descriptor"]["verdict"]))
    known = pick(code["code-regression"], "cb24.ts.external-call", "src/util.ts")
    must("complete-hit-set-baseline-proves-code-net-new", known and known[0]["pivotValues"]["B"] is False and known[0]["classification"] == "CODE-NET-NEW", known)
    dump("vectors/comparison-absence-knowledge.json", {
        "classification": "valid", "baselineComplete": "cmp-base", "budgetRun": "cmp-budget",
        "budgetBaselineRuleCoverage": budget_art["descriptor"]["ruleCoverage"], "budgetBaselineAdmission": bvf,
        "currentAbsenceUnknown": brief(cur_unknown), "baselineAbsenceUnknown": brief(base_unknown),
        "knownAbsenceControl": {"comparison": "cmp-base -> cmp-code", "entry": known},
        "comparisons": {"currentAbsenceUnknown": cur_unknown["comparison"], "baselineAbsenceUnknown": base_unknown["comparison"]},
        "selectors": ["workflows-and-surfaces.md s3 lines 376-411", "workflows/schemas/evaluator3/comparison-result.schema.json#/$defs/RuleCoverage/properties/absenceKnowledge",
                      "workflows/schemas/evaluator3/comparison-result.schema.json#/$defs/PivotPresence", "workflow-projection-contract.v3.md s12 lines 201-204"]})
    print("failures", len(failures))
    print(json.dumps(failures, default=str)[:8000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
