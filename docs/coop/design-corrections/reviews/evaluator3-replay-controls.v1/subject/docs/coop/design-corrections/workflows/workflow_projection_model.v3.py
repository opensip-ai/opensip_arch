"""Pure evaluator3 workflow projection. Not full Run replay.

Consumes ADMITTED evaluator3 findings, fingerprint preimages, emission bindings,
waivedFindingIds, ruleResults, policy, and executionDeficiencies. Does not read
producer expected entries, expected classifications, or verified flags.
ruleResults have no gating field; gating is derived from admitted policy.
Matched classification reuses workflows_model.v1.classify (audit-profile law).
Emitted descriptors are ComparisonDescriptor/BaselineDescriptor schemaMajor 2.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "foundation"))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

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
SEVERITY = {"note": 0, "warning": 1, "error": 2}
REQUIRED_CURRENT = (
    "runId",
    "snapshotId",
    "projectId",
    "policy",
    "occurrences",
    "ruleResults",
    "waivedFindingIds",
    "executionDeficiencies",
    "evaluationState",
    "emissionBindings",
    "context",
    "requiredCoverage",
    "boundPivots",
    "pivotPresence",
)
PIN_PREFIX = ("run3:", "closure2:")
_PROFILE_REG = None


def sha(value) -> str:
    return hashlib.sha256(canonical.canonical(value)).hexdigest()


def fingerprint_id(descriptor: dict) -> str:
    return wid("finding-key2", "finding-fingerprint", descriptor)


def profile_registry():
    global _PROFILE_REG
    if _PROFILE_REG is not None:
        return _PROFILE_REG
    docs = {}
    for path in sorted((HERE / "schemas" / "evaluator3").glob("*.schema.json")):
        doc = json.loads(path.read_text())
        Draft202012Validator.check_schema(doc)
        docs[doc["$id"]] = doc
    for name in (
        "common.schema.json",
        "imported-evidence.schema.json",
        "policy-document.schema.json",
        "policy-document.v2.schema.json",
        "test-execution.schema.json",
    ):
        path = HERE / "schemas" / name
        doc = json.loads(path.read_text())
        Draft202012Validator.check_schema(doc)
        docs[doc["$id"]] = doc
    _PROFILE_REG = Registry().with_resources(
        [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in docs.items()]
    )
    return _PROFILE_REG


def validate_profile(ref: str, value) -> None:
    canonical.typed(value)
    canonical.ExactValidator({"$ref": ref}, registry=profile_registry()).validate(value)


def rule_gates(policy: dict, rule_id: str) -> bool:
    """Admitted PolicyDocumentV2 only. ruleResults do not carry gating."""
    for rule in policy["rules"]:
        if rule["ruleId"] == rule_id:
            return bool(
                rule["enabled"]
                and rule["gate"]
                and SEVERITY[rule["severity"]] >= SEVERITY[policy["gateSeverityAtLeast"]]
            )
    return False


def policy_rule(policy: dict, rule_id: str):
    for rule in policy["rules"]:
        if rule["ruleId"] == rule_id:
            return rule
    return None


def findings_map(occurrences: list) -> dict:
    """Per-run map keyed by findingId. NEVER by fingerprint (duplicates are normal)."""
    out = {}
    for occ in occurrences:
        fid = occ["findingId"]
        if fid in out:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "duplicate findingId", fid)
        if not str(fid).startswith("finding3:"):
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "finding3 required", fid)
        sid = occ["finding"]["subjectId"]
        if not str(sid).startswith("subject3:"):
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "opaque subject3 required", sid)
        out[fid] = occ
    return out


def admit_occurrence(occ: dict, binding: dict) -> dict:
    finding = occ["finding"]
    if finding.get("schemaVersion") != 3:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "finding schemaVersion 3")
    corr = finding["correspondence"]
    fp = finding["fingerprint"]
    params = occ["parameterRecord"]
    if sha(params) != finding["parameterDigest"]:
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "parameterDigest mismatch", occ["findingId"])
    if params.get("schemaVersion") != 2 or set(params["parameters"]) != set(GENERIC7):
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "declarative-subject-v1 requires exactly the generic 7 parameters")
    if params["parameters"]["subjectKind"] not in STORED_KINDS:
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "subjectKind is stored kind, never export")
    if corr["state"] == "matched":
        if fp is None or corr.get("reason") is not None:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "matched requires nonnull fingerprint and null reason")
        desc = occ.get("fingerprintDescriptor")
        if desc is None:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "matched finding missing fingerprint preimage")
        if fingerprint_id(desc) != fp:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "fingerprint identity does not match preimage")
        if desc.get("schemaVersion") != 2:
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "finding-key2 retained")
        sk = desc["subjectKey"]
        sub = finding["subject"]
        if sk["logicalPath"] != sub["logicalPath"] or sk["kind"] != sub["kind"] or sk["qualifiedName"] != sub["qualifiedName"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "finding.subject must equal fingerprint subjectKey")
        if finding["ruleClosure"] != binding["detectorClosure"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "finding.ruleClosure must equal emission detectorClosure")
    elif corr["state"] == "unmatched":
        if fp is not None or corr.get("reason") not in UNMATCHED_REASONS:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "unmatched requires null fingerprint and closed reason")
        if occ.get("fingerprintDescriptor") is not None:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "unmatched must not carry a fingerprint preimage")
    else:
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "correspondence.state")
    if binding["emissionProfile"] != "declarative-subject-v1" or binding["stabilityClass"] != "path-stable":
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "declarative-subject-v1/path-stable required")
    return occ


def _entry_fields(occ: dict, binding: dict, waived: bool) -> dict:
    finding = occ["finding"]
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


def _unmatched_row(occ: dict, waived: bool, side: str) -> dict:
    f = occ["finding"]
    return {
        "side": side,
        "findingId": occ["findingId"],
        "ruleId": f["ruleId"],
        "subjectId": f["subjectId"],
        "subjectPath": f["subject"]["logicalPath"],
        "severity": f["severity"],
        "waived": waived,
        "correspondenceReason": f["correspondence"]["reason"],
    }


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
            unmatched.append(_unmatched_row(occ, is_waived, "baseline"))
            continue
        desc = occ["fingerprintDescriptor"]
        fp = finding["fingerprint"]
        g = groups.setdefault(fp, {"descriptor": desc, "fields": None, "findingIds": [], "occs": []})
        if canonical.canonical(g["descriptor"]) != canonical.canonical(desc):
            raise Refusal(
                "CONFIG.INVALID",
                "EVALUATION.FINDING_JOIN_REFUSED",
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
        g["occs"].append(occ)
    entries = sorted((g["fields"] for g in groups.values()), key=lambda e: e["fingerprint"].encode())
    unmatched.sort(key=lambda r: (r["side"].encode(), r["findingId"].encode()))
    return {"entries": entries, "unmatchedOccurrences": unmatched, "groups": groups}


def adopt_baseline_v3(run, plan, project_id, policy, scope, waivers, rule_coverage, projected, detector_closure, pivot_closure, context, analysis_spec, custody):
    """Adapter: schemaMajor 2, run3, unmatched array. Scope join is mandatory. exportedAtUtc is trusted custody input."""
    if run.get("authority") != "authoritative":
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.SOURCE_EPHEMERAL", "run an authoritative analysis first")
    if "availability" not in run:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "origin run availability is required")
    if run["availability"] != "retained":
        raise Refusal("REQUEST.PRECONDITION_FAILED", "REPAIR.EVIDENCE_RUN_UNAVAILABLE", "the Run evidence is " + str(run["availability"]))
    if not str(run["runId"]).startswith("run3:"):
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "baseline origin Run must be run3")
    if policy.get("schemaMajor") != 2:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "PolicyDocumentV2 required")
    if analysis_spec is None:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER", "ScopeDocumentV1 parameter join is mandatory for baseline adoption")
    verify_scope_parameter_binding(analysis_spec, scope)
    if not custody or "exportedAtUtc" not in custody or "exportedByHostRelease" not in custody:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "trusted custody exportedAtUtc and exportedByHostRelease are required inputs")
    ctx = dict(context)
    ctx["policyDigest"] = doc_digest(policy)
    ctx["scopeDigest"] = doc_digest(scope)
    ctx["waiverSetDigest"] = doc_digest(waivers)
    ents = projected["entries"]
    unmatched = projected["unmatchedOccurrences"]
    if len({x["fingerprint"] for x in ents}) != len(ents):
        raise Refusal("CONFIG.INVALID", "BASELINE.ENTRY_PROJECTION_CONFLICT", "duplicate fingerprint in baseline entries")
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
    art = {
        "baselineId": bid,
        "descriptor": desc,
        "custody": {
            "exportedByHostRelease": custody["exportedByHostRelease"],
            "exportedAtUtc": custody["exportedAtUtc"],
            "runRetainedAtExport": True,
            "retentionPins": pins,
        },
    }
    verify_baseline_artifact_v3(art)
    return art


def verify_baseline_artifact_v3(art) -> bool:
    """Schema + H identity + context-document digest bindings + custody pins.

    Root source/admission is a prerequisite: this function does not call
    evaluator_replay_model.v3.derive/replay or open_run_closure. Adoption already
    required an authoritative retained run3. Historical schemaMajor 1 is refused
    before any unmatched-array coercion.
    """
    if not isinstance(art, dict) or not isinstance(art.get("descriptor"), dict):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "baseline artifact required")
    d = art["descriptor"]
    if d.get("schemaMajor") != 2:
        raise Refusal(
            "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
            "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
            "historical schemaMajor 1 is refused; missing unmatched is not []",
        )
    try:
        validate_profile("urn:opensip:product-v1:workflows:evaluator3:baseline:2", art)
    except Exception as exc:
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "baseline artifact failed schema admission: " + str(exc).splitlines()[0][:180]) from exc
    if wid("baseline2", "workflow.baseline", d) != art["baselineId"]:
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "baselineId does not match descriptor")
    if not d["runId"].startswith("run3:"):
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "a baseline names an authoritative run3")
    docs = d["contextDocuments"]
    ctx = d["context"]
    if doc_digest(docs["policy"]) != ctx["policyDigest"]:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING", "embedded policy digest mismatch")
    if doc_digest(docs["scope"]) != ctx["scopeDigest"]:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING", "embedded scope digest mismatch")
    if doc_digest(docs["waivers"]) != ctx["waiverSetDigest"]:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING", "embedded waiver digest mismatch")
    fps = [x["fingerprint"] for x in d["entries"]]
    if fps != sorted(fps, key=lambda s: s.encode()) or len(set(fps)) != len(fps):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "entries must be sorted and unique")
    unmatched = d["unmatchedOccurrences"]
    if any(x.get("side") != "baseline" for x in unmatched):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "baseline unmatchedOccurrences.side must be baseline")
    uids = [x["findingId"] for x in unmatched]
    if uids != sorted(uids, key=lambda s: s.encode()) or len(set(uids)) != len(uids):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "unmatchedOccurrences must be sorted unique findingId")
    custody = art["custody"]
    if "exportedAtUtc" not in custody or "exportedByHostRelease" not in custody:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "trusted custody exportedAtUtc and exportedByHostRelease are required")
    for pin in custody["retentionPins"]:
        if not pin.startswith(PIN_PREFIX):
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "retentionPins are run3|closure2", pin)
    return True


def require_rule_results_total(policy, rule_results) -> dict:
    """ruleResults are required and total over policy.rules. Empty default is not a heal."""
    if not isinstance(rule_results, list):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "ruleResults required")
    by_id = {}
    for rr in rule_results:
        rid = rr["ruleId"]
        if rid in by_id:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "duplicate ruleResult", rid)
        by_id[rid] = rr
    needed = [rule["ruleId"] for rule in policy["rules"]]
    missing = [rid for rid in needed if rid not in by_id]
    extra = [rid for rid in by_id if rid not in set(needed)]
    if missing or extra:
        raise Refusal(
            "REQUEST.PRECONDITION_FAILED",
            "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
            "ruleResults must be total over policy.rules",
        )
    return by_id


def current_run_verdict(*, policy, occurrences, waived_ids, rule_results, execution_deficiencies, evaluation_state, proof_verdict=None):
    """Derive current sealed-run verdict from admitted policy + findings + enumeration + execution.

    ruleResults have no gating field. Gating is policy enabled AND gate AND severity floor.
    Advisory live findings do not fail. ruleResults.outcome is not a gating switch.
    executionDeficiencies and budget-exhausted are independent of rule findings.
    If proof_verdict is supplied, it must equal the derived verdict.
    """
    by_id = require_rule_results_total(policy, rule_results)
    waived = set(waived_ids)
    live_by_rule = {}
    for occ in occurrences:
        if occ["findingId"] not in waived:
            live_by_rule.setdefault(occ["finding"]["ruleId"], []).append(occ)
    fail = False
    indeterminate = False
    for rule in policy["rules"]:
        rid = rule["ruleId"]
        rr = by_id[rid]
        if not rule["enabled"]:
            continue
        gating = rule_gates(policy, rid)
        unknown = rr["enumeration"]["state"] == "incomplete" or bool(rr["deficiencies"])
        if gating and live_by_rule.get(rid):
            fail = True
            continue
        if gating and unknown:
            indeterminate = True
    if execution_deficiencies or evaluation_state == "budget-exhausted":
        indeterminate = True
    derived = "fail" if fail else ("indeterminate" if indeterminate else "pass")
    if proof_verdict is not None and proof_verdict != derived:
        raise Refusal("CONFIG.INVALID", "EVALUATION.PROOF_VERDICT_INCONSISTENT", "admitted proof verdict disagrees with policy-derived verdict")
    return derived


def correspondence_coverage(policy, rule_results, occurrences) -> list:
    """Gating from admitted policy only, never from ruleResults.outcome."""
    require_rule_results_total(policy, rule_results)
    counts = {r["ruleId"]: {"matched": 0, "unmatched": 0} for r in rule_results}
    for occ in occurrences:
        rid = occ["finding"]["ruleId"]
        if rid not in counts:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "occurrence ruleId not in admitted ruleResults", rid)
        state = occ["finding"]["correspondence"]["state"]
        counts[rid][state] += 1
    out = []
    for r in sorted(rule_results, key=lambda x: x["ruleId"].encode()):
        rid = r["ruleId"]
        enum = r["enumeration"]
        matched_n = counts.get(rid, {}).get("matched", 0)
        unmatched_n = counts.get(rid, {}).get("unmatched", 0)
        out.append(
            {
                "ruleId": rid,
                "gating": rule_gates(policy, rid),
                "matchedCount": matched_n,
                "unmatchedCount": unmatched_n,
                "populationUnknown": enum["state"] == "incomplete",
                "zeroFindings": (matched_n + unmatched_n) == 0,
            }
        )
    return out


def derive_current_matched(occurrences, waived_ids, bindings):
    """E4 / waivedC / entryRules from admitted occurrences only."""
    waived = set(waived_ids)
    recs = {}
    for occ in occurrences:
        f = occ["finding"]
        if f["correspondence"]["state"] != "matched":
            continue
        fp = f["fingerprint"]
        rec = recs.setdefault(fp, {"waived": [], "ruleId": f["ruleId"], "detectorId": bindings[f["ruleId"]]["contributionId"]})
        rec["waived"].append(occ["findingId"] in waived)
    presence = {}
    entry_rules = {}
    for fp, rec in recs.items():
        presence[fp] = {"E4": True, "waivedC": all(rec["waived"])}
        entry_rules[fp] = (rec["ruleId"], rec["detectorId"])
    return presence, entry_rules


def require_current(current: dict) -> None:
    if not isinstance(current, dict):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "current projection input required")
    missing = [k for k in REQUIRED_CURRENT if k not in current]
    if missing:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "missing required current fields: " + ",".join(missing))
    if "presence" in current or "entryRules" in current:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "current.presence/entryRules are derived from occurrences; do not supply them")
    if not str(current["runId"]).startswith("run3:"):
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "current runId must be run3")
    if current["policy"].get("schemaMajor") != 2:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "current PolicyDocumentV2 required")
    require_rule_results_total(current["policy"], current["ruleResults"])
    if current["requiredCoverage"].keys() != {r["ruleId"] for r in current["policy"]["rules"]}:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "requiredCoverage must be total over policy.rules")


def _rule_coverage_from_policy(policy, required_coverage):
    out = {}
    for rule in policy["rules"]:
        rid = rule["ruleId"]
        if rid not in required_coverage:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "requiredCoverage missing for rule", rid)
        out[rid] = {
            "ruleId": rid,
            "requiredCoverage": required_coverage[rid],
            "enabled": bool(rule["enabled"]),
            "gating": rule_gates(policy, rid),
            "evidenceUse": copy.deepcopy(rule["evidenceUse"]),
        }
    return out


def _baseline_unmatched_deficiencies(profile, baseline, current_policy, extra_keys):
    """Under baseline-or-current, baseline unmatched gating obligations survive current empty/removed rules."""
    out = []
    b_rules = {r["ruleId"]: r for r in baseline["ruleCoverage"]}
    for u in baseline["unmatchedOccurrences"]:
        b = b_rules.get(u["ruleId"])
        b_gate = bool(b and b.get("enabled") and b.get("gating"))
        c_gate = rule_gates(current_policy, u["ruleId"])
        relevant = (b_gate or c_gate) if profile["gateRuleUnder"] == "baseline-or-current" else c_gate
        if relevant:
            key = (u["ruleId"], "correspondence-incomplete")
            if key not in extra_keys:
                out.append({"ruleId": u["ruleId"], "gating": True, "cause": "correspondence-incomplete"})
                extra_keys.add(key)
    return out


def compare_v3(*, baseline_artifact, current, host, profile_name, current_detectors, accept_origins=()):
    """Matched classify() reuse; unmatched from both sides; E4 derived from occurrences."""
    require_current(current)
    verify_baseline_artifact_v3(baseline_artifact)
    profile = AUDIT_PROFILES[profile_name]
    bdesc = baseline_artifact["descriptor"]
    occurrences = current["occurrences"]
    waived = current["waivedFindingIds"]
    bindings = current["emissionBindings"]
    findings_map(occurrences)
    for occ in occurrences:
        binding = bindings.get(occ["finding"]["ruleId"])
        if binding is None:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "missing emission binding", occ["finding"]["ruleId"])
        admit_occurrence(occ, binding)
    derived_e4, entry_rules = derive_current_matched(occurrences, waived, bindings)
    c_rules = _rule_coverage_from_policy(current["policy"], current["requiredCoverage"])
    pivot = current["pivotPresence"]
    if not isinstance(pivot, dict):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "pivotPresence is the independently admitted E0-E3 map")
    presence = {}
    b_entries = {x["fingerprint"]: x for x in bdesc["entries"]}
    fps = set(b_entries) | set(derived_e4)
    for fp in fps:
        if fp not in pivot:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "missing independently admitted pivotPresence for fingerprint", fp)
        pvt = dict(pivot[fp])
        pvt.pop("E4", None)
        pvt.pop("waivedC", None)
        pvt.pop("entryRules", None)
        for axis in ("E1", "E2", "E3"):
            if axis not in pvt or not isinstance(pvt[axis], bool):
                raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "pivotPresence must admit E1/E2/E3 booleans", fp)
        if "E0" not in pvt:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "pivotPresence must admit E0", fp)
        row = {
            "B": fp in b_entries,
            "E0": pvt["E0"],
            "E1": pvt["E1"],
            "E2": pvt["E2"],
            "E3": pvt["E3"],
            "E4": bool(derived_e4.get(fp, {}).get("E4")),
            "waivedB": b_entries[fp]["waived"] if fp in b_entries else False,
            "waivedC": bool(derived_e4.get(fp, {}).get("waivedC", False)),
        }
        presence[fp] = row
    current_v1 = {
        "runId": current["runId"],
        "snapshotId": current["snapshotId"],
        "projectId": current["projectId"],
        "context": current["context"],
        "ruleCoverage": c_rules,
        "presence": presence,
        "entryRules": entry_rules,
        "boundPivots": current["boundPivots"],
    }
    res = _compare_matched(bdesc, current_v1, host, profile_name, current_detectors, accept_origins, baseline_id=baseline_artifact["baselineId"])
    desc = res["descriptor"]
    desc["schemaMajor"] = 2
    current_unmatched = [_unmatched_row(occ, occ["findingId"] in set(waived), "current") for occ in occurrences if occ["finding"]["correspondence"]["state"] == "unmatched"]
    baseline_unmatched = list(bdesc["unmatchedOccurrences"])
    combined = sorted(baseline_unmatched + current_unmatched, key=lambda r: (r["side"].encode(), r["findingId"].encode()))
    if not desc.get("comparisonPerformed"):
        desc["unmatchedOccurrences"] = []
        desc["correspondenceCoverage"] = []
        validate_profile("urn:opensip:product-v1:workflows:evaluator3:comparison:2", {"comparisonResultId": res["comparisonResultId"], "descriptor": desc})
        return res
    desc["unmatchedOccurrences"] = combined
    cov = correspondence_coverage(current["policy"], current["ruleResults"], occurrences)
    desc["correspondenceCoverage"] = cov
    extra_keys = {(d["ruleId"], d["cause"]) for d in desc["ruleDeficiencies"]}
    for row in cov:
        if row["gating"] and (row["unmatchedCount"] > 0 or row["populationUnknown"]):
            key = (row["ruleId"], "correspondence-incomplete")
            if key not in extra_keys:
                desc["ruleDeficiencies"].append({"ruleId": row["ruleId"], "gating": True, "cause": "correspondence-incomplete"})
                extra_keys.add(key)
    for dfc in _baseline_unmatched_deficiencies(profile, bdesc, current["policy"], extra_keys):
        desc["ruleDeficiencies"].append(dfc)
    desc["ruleDeficiencies"] = sorted(desc["ruleDeficiencies"], key=lambda d: (d["ruleId"].encode(), d["cause"].encode()))
    if desc["verdict"] != "fail" and any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in desc["ruleDeficiencies"]):
        desc["verdict"] = "indeterminate"
        desc["d9Deficiency"] = desc.get("d9Deficiency") or "verdict-indeterminate"
        desc["remedy"] = {
            "code": "COMPARISON.CORRESPONDENCE_INCOMPLETE",
            "remedy": "complete inventories/projections; unmatched cannot be classified as net-new or resolved",
        }
    res["comparisonResultId"] = wid("comparison2", "workflow.comparison", desc)
    res["descriptor"] = desc
    validate_profile("urn:opensip:product-v1:workflows:evaluator3:comparison:2", {"comparisonResultId": res["comparisonResultId"], "descriptor": desc})
    return res


def _empty_context_delta():
    return {
        "codeChanged": False,
        "detectorChanged": False,
        "policyChanged": False,
        "scopeChanged": False,
        "waiversChanged": False,
        "evidenceAvailabilityChanged": False,
    }


def _compare_matched(baseline, current, host, profile_name, current_detectors, accept_origins, baseline_id):
    """Explicit adapter: v1.classify audit-profile law, ComparisonDescriptor schemaMajor 2 identity."""
    profile = AUDIT_PROFILES[profile_name]
    bc, cc = baseline["context"], current["context"]
    context_delta = {
        "codeChanged": baseline["source"]["snapshotId"] != current["snapshotId"],
        "detectorChanged": sorted(bc["detectorClosureIds"]) != sorted(cc["detectorClosureIds"]),
        "policyChanged": bc["policyDigest"] != cc["policyDigest"],
        "scopeChanged": bc["scopeDigest"] != cc["scopeDigest"],
        "waiversChanged": bc["waiverSetDigest"] != cc["waiverSetDigest"],
        "evidenceAvailabilityChanged": sorted(i["importId"] for i in bc["evidenceAvailability"]["imports"])
        != sorted(i["importId"] for i in cc["evidenceAvailability"]["imports"]),
    }
    desc = {
        "schemaFamily": "opensip.product.comparison",
        "schemaMajor": 2,
        "baselineId": baseline_id,
        "currentRunId": current["runId"],
        "currentSnapshotId": current["snapshotId"],
        "auditProfile": profile,
        "baselineContext": baseline["context"],
        "currentContext": current["context"],
        "contextDelta": context_delta,
        "detectors": [],
        "ruleDeficiencies": [],
        "entries": [],
        "unmatchedOccurrences": [],
        "correspondenceCoverage": [],
    }
    if baseline["originProjectId"] == current["projectId"]:
        desc["projectCorrespondence"] = "same-project"
    elif baseline["originProjectId"] in accept_origins:
        desc["projectCorrespondence"] = "declared"
    else:
        desc["projectCorrespondence"] = "unmapped"

    def whole(reason, code, remedy, error_code):
        d9 = "baseline-recipe-unsupported" if reason in ("baseline-recipe-unsupported", "baseline-schema-major-unsupported") else "verdict-indeterminate"
        desc.update(
            comparisonPerformed=False,
            wholeIndeterminateReason=reason,
            remedy={"code": code, "remedy": remedy},
            contextDelta=context_delta,
            pivotsAvailable={k: "unavailable" for k in ("E0", "E1", "E2", "E3")},
            counts={k: 0 for k in COUNT_KEYS},
            verdict="indeterminate",
            d9Deficiency=d9,
            unmatchedOccurrences=[],
            correspondenceCoverage=[],
            detectors=[],
            ruleDeficiencies=[],
            entries=[],
        )
        return {
            "comparisonResultId": wid("comparison2", "workflow.comparison", desc),
            "descriptor": desc,
            "errorCode": error_code,
        }

    if desc["projectCorrespondence"] == "unmapped":
        return whole(
            "baseline-project-unmapped",
            "BASELINE.PROJECT_UNMAPPED",
            "pass --accept-origin " + baseline["originProjectId"],
            "REQUEST.PRECONDITION_FAILED",
        )
    if baseline.get("schemaMajor") != 2:
        return whole(
            "baseline-schema-major-unsupported",
            "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
            "re-adopt under evaluator3 schemaMajor 2; do not treat missing unmatched as []",
            "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
        )
    if "recipeMajors" not in host:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "host.recipeMajors required")
    if baseline["fingerprintRecipe"]["recipeMajor"] not in host["recipeMajors"]:
        return whole(
            "baseline-recipe-unsupported",
            "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
            "baseline fingerprint recipe major is not in host.recipeMajors",
            "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
        )
    dets = resolve_detectors(baseline, current_detectors, host)
    desc["detectors"] = [dets[k] for k in sorted(dets, key=lambda s: s.encode())]
    e0_state = (
        "not-needed"
        if not desc["contextDelta"]["detectorChanged"]
        else ("available" if all(d["method"] != "indeterminate" for d in dets.values()) else "unavailable")
    )
    bound = set(current["boundPivots"])
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
        if fp not in current["presence"]:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "matched fingerprint missing from derived presence", fp)
        pres = dict(current["presence"][fp])
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


def project_finding_surfaces(occurrences, waived_ids) -> list:
    """Intermediate host projection. Not SARIF."""
    waived = set(waived_ids)
    rows = []
    for occ in occurrences:
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
            "waived": occ["findingId"] in waived,
            "parameterDigest": f["parameterDigest"],
        }
        if f["correspondence"]["state"] == "matched":
            row["partialFingerprints"] = {"opensip/finding-key2": f["fingerprint"]}
        rows.append(row)
    rows.sort(key=lambda r: r["findingId"].encode())
    return rows


def project_sarif(occurrences, waived_ids, *, verdict, deficiency=None) -> dict:
    """Actual SARIF 2.1.0 log: one result per finding3, citations and message parameters retained."""
    waived = set(waived_ids)
    surfaces = project_finding_surfaces(occurrences, waived_ids)
    by_id = {occ["findingId"]: occ for occ in occurrences}
    rules = []
    seen = set()
    results = []
    for row in surfaces:
        occ = by_id[row["findingId"]]
        if row["ruleId"] not in seen:
            rules.append({"id": row["ruleId"], "shortDescription": {"text": row["messageCode"]}})
            seen.add(row["ruleId"])
        params = occ["parameterRecord"]["parameters"]
        result = {
            "ruleId": row["ruleId"],
            "level": row["severity"],
            "message": {"id": row["messageCode"], "text": row["messageCode"], "properties": dict(params)},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": row["subjectPath"]}}}],
            "properties": {
                "findingId": row["findingId"],
                "subjectId": row["subjectId"],
                "correspondence": copy.deepcopy(row["correspondence"]),
                "waived": occ["findingId"] in waived,
                "citations": copy.deepcopy(occ["finding"]["evidenceRefs"]),
            },
        }
        if row["fingerprint"] is not None:
            result["partialFingerprints"] = {"opensip/finding-key2": row["fingerprint"]}
        results.append(result)
    rules.sort(key=lambda r: r["id"].encode())
    log = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "opensip", "rules": rules}},
                "results": results,
                "properties": {"verdict": verdict, **({"deficiency": deficiency} if deficiency else {})},
            }
        ],
    }
    validate_profile("urn:opensip:product-v1:workflows:evaluator3:sarif-adapter:2", log)
    return log


def project_candidates(run_id, project_id, occurrences, policy, waived_ids, dispositions, today, bindings):
    """Matched candidates group by fingerprint after BaselineEntry agreement; unmatched by findingId."""
    waived = set(waived_ids)
    projected = project_baseline_entries(occurrences, bindings, waived_ids)
    out = []
    for fp, g in projected["groups"].items():
        occs = sorted(g["occs"], key=lambda o: o["findingId"].encode())
        finding_ids = [o["findingId"] for o in occs]
        rows = []
        live_gating = False
        for o in occs:
            f = o["finding"]
            live = o["findingId"] not in waived
            if live and rule_gates(policy, f["ruleId"]):
                live_gating = True
            rows.append(
                {
                    "findingId": o["findingId"],
                    "subjectId": f["subjectId"],
                    "subjectPath": f["subject"]["logicalPath"],
                    "parameterDigest": f["parameterDigest"],
                    "correspondence": copy.deepcopy(f["correspondence"]),
                    "waived": not live,
                }
            )
        cid = wid("candidate2", "workflow.candidate", {"projectId": project_id, "kind": "finding", "key": fp})
        c = {
            "candidateId": cid,
            "runId": run_id,
            "kind": "finding",
            "fingerprint": fp,
            "ruleId": g["fields"]["ruleId"],
            "evidenceLevel": "proof-backed",
            "subjectPath": g["fields"]["subjectPath"],
            "controlBearing": live_gating,
            "suppressed": False,
            "findingIds": finding_ids,
            "occurrences": rows,
        }
        _apply_disposition(c, dispositions.get(cid), today)
        out.append(c)
    for u in projected["unmatchedOccurrences"]:
        occ = next(o for o in occurrences if o["findingId"] == u["findingId"])
        f = occ["finding"]
        live = occ["findingId"] not in waived
        cid = wid("candidate2", "workflow.candidate", {"projectId": project_id, "kind": "finding", "key": u["findingId"]})
        c = {
            "candidateId": cid,
            "runId": run_id,
            "kind": "finding",
            "fingerprint": None,
            "ruleId": f["ruleId"],
            "evidenceLevel": "proof-backed",
            "subjectPath": f["subject"]["logicalPath"],
            "controlBearing": live and rule_gates(policy, f["ruleId"]),
            "suppressed": False,
            "findingIds": [u["findingId"]],
            "occurrences": [
                {
                    "findingId": u["findingId"],
                    "subjectId": f["subjectId"],
                    "subjectPath": f["subject"]["logicalPath"],
                    "parameterDigest": f["parameterDigest"],
                    "correspondence": copy.deepcopy(f["correspondence"]),
                    "waived": not live,
                }
            ],
        }
        _apply_disposition(c, dispositions.get(cid), today)
        out.append(c)
    return sorted(out, key=lambda c: c["candidateId"])


def _apply_disposition(candidate, disposition, today) -> None:
    if not disposition or disposition["disposition"] not in ("reject", "defer"):
        return
    until = disposition["suppressUntil"]
    if until is None or until >= today:
        candidate["suppressed"] = True
        candidate["suppressedBy"] = disposition["receiptId"]
    else:
        candidate["previouslyReviewed"] = True


def query_finding(occurrences, *, finding_id=None, fingerprint=None) -> list:
    if finding_id is not None:
        return [occ for occ in occurrences if occ["findingId"] == finding_id]
    if fingerprint is not None:
        return [
            occ
            for occ in occurrences
            if occ["finding"]["fingerprint"] == fingerprint and occ["finding"]["correspondence"]["state"] == "matched"
        ]
    raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "finding.show requires findingId or fingerprint")


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
    return {
        "class": "operational-failed",
        "errorCode": "OUTPUT.SERIALIZATION_FAILED",
        "faultCause": "output-serialization",
        "domainDetail": {
            "code": "EVALUATION.OUTPUT_BOUND_EXCEEDED",
            "remedy": "narrow the admitted output or raise the array/C-byte bound; never truncate to an empty Run",
        },
    }
