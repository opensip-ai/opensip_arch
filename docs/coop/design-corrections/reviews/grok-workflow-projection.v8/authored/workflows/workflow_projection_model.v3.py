"""Pure evaluator3 workflow projection. Not a substitute for owner Run admission.

Consumes ADMITTED evaluator3 findings, fingerprint preimages, emission bindings,
waivedFindingIds, ruleResults, policy, and executionDeficiencies. Does not read
producer expected entries, expected classifications, or verified flags.
ruleResults have no gating field; gating is derived from admitted policy.
Matched classification reuses workflows_model.v1.classify (audit-profile law).
Emitted descriptors are ComparisonDescriptor/BaselineDescriptor schemaMajor 2.

project_admitted_run_v3 is the public adapter: identity-model.v3.close_run (full
replay), then occurrence maps from the admitted Plan/policy/emission/proof.
open_run_closure is owner-internal and is not called here.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import urllib.parse
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
)
PIN_PREFIX = ("run3:", "closure2:")
EMISSION_PARAMETER_ROW = "foundation/evaluator-emission-plan.schema.v1.json"
SCOPE_PARAMETER_ROW = "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"
PIVOT_KINDS = {"detector", "evaluator", "provider", "toolchain", "stdlib", "schema-set"}
PIVOT_AXES = ("E0", "E1", "E2", "E3")
_ID3 = None
_DEF_REG = None


def evaluator_deficiency_registry():
    global _DEF_REG
    if _DEF_REG is None:
        doc = json.loads((HERE.parent / "foundation" / "identity-schemas.v3.json").read_text())
        _DEF_REG = doc["x-opensip-evaluator-deficiency-registry"]
    return _DEF_REG


def deficiency_blocks(rule, d) -> bool:
    """Root composer blocks() law. nonBlockingDisclosures never make a rule unknown."""
    if d.get("cause") in evaluator_deficiency_registry()["nonBlockingDisclosures"]:
        return False
    src = d.get("source")
    if src != "import":
        return src in ("native", "enumeration", "execution")
    required = {v["kind"] for v in rule.get("evidenceUse", []) if v.get("requirement") == "required"}
    return d.get("evidenceKind") in required


def project_execution_deficiencies(records) -> list:
    """Copy the admitted evaluation-deficiency record in full. No field drop."""
    out = []
    required = ("source", "cause", "subjectId", "predicateId", "inputRefs", "evidenceKind", "nativeCause", "universe")
    for d in records:
        missing = [k for k in required if k not in d]
        if missing:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "execution deficiency missing " + ",".join(missing))
        out.append(copy.deepcopy({k: d[k] for k in required}))
    return out
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
    """INTERNAL helper. Documents and projected entries must already be the admitted origin Run's.

    Public adoption is adopt_admitted_baseline_v3 (close_run + source Plan/scope/waiver/policy join).
    Caller authority/availability flags do not substitute for that join.
    """
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
    expected_pins = sorted({d["runId"]} | {p["closureId"] for p in d["pivotClosure"]})
    pins = list(custody["retentionPins"])
    if pins != expected_pins or len(set(pins)) != len(pins):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "retentionPins must be the unique sorted run3 plus pivotClosure set")
    for pin in pins:
        if not pin.startswith(PIN_PREFIX):
            raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "retentionPins are run3|closure2", pin)
    if not any(p["kind"] == "detector" for p in d["pivotClosure"]):
        raise Refusal("CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT", "pivotClosure must include the origin detector")
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
        live = bool(live_by_rule.get(rid))
        if gating and live:
            fail = True
            continue
        if rr["outcome"] == "indeterminate":
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


def detector_identity_map(spec) -> dict:
    """Exact selected detector identity: detectorId → {closureId, semanticsMajor}.

    Not a subset of common IDs and not a closure-id list. Extra or missing detector
    identities and disagreeing majors are map inequality. compatibleWith is not part
    of identity and is never inferred.
    """
    out = {}
    if isinstance(spec, dict):
        rows = []
        for did, rec in spec.items():
            rows.append({"detectorId": did, "closureId": rec["closureId"], "semanticsMajor": rec["semanticsMajor"]})
        spec = rows
    for row in spec:
        did = row["detectorId"]
        rec = {"closureId": row["closureId"], "semanticsMajor": row["semanticsMajor"]}
        if did in out and canonical.canonical(out[did]) != canonical.canonical(rec):
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "conflicting detector identity", did)
        out[did] = rec
    return {k: out[k] for k in sorted(out, key=lambda s: s.encode())}


def detector_map_changed(baseline_spec, current_spec) -> bool:
    return canonical.canonical(detector_identity_map(baseline_spec)) != canonical.canonical(detector_identity_map(current_spec))


def require_exact_detector_map(actual, expected, axis) -> None:
    """E0 (and any explicit exact-selection axis) requires the full identity/major map."""
    if canonical.canonical(detector_identity_map(actual)) != canonical.canonical(detector_identity_map(expected)):
        raise Refusal(
            "CONFIG.INVALID",
            "EVALUATION.FINDING_JOIN_REFUSED",
            "pivot detector identity/major map is not an exact baseline/current selection",
            axis,
        )


def require_current(current: dict) -> None:
    if not isinstance(current, dict):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "current projection input required")
    missing = [k for k in REQUIRED_CURRENT if k not in current]
    if missing:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "missing required current fields: " + ",".join(missing))
    if "presence" in current or "entryRules" in current:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "current.presence/entryRules are derived from occurrences; do not supply them")
    if current["evaluationState"] not in ("evaluated", "budget-exhausted"):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "evaluationState must be evaluated or budget-exhausted")
    if not isinstance(current["executionDeficiencies"], list):
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "executionDeficiencies required")
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


def _whole_comparison_without_maps(baseline, current, host, accept_origins):
    if baseline["originProjectId"] != current["projectId"] and baseline["originProjectId"] not in accept_origins:
        return True
    if baseline.get("schemaMajor") != 2:
        return True
    if "recipeMajors" in host and baseline["fingerprintRecipe"]["recipeMajor"] not in host["recipeMajors"]:
        return True
    return False


def _derive_or_admit_presence(fps, b_entries, derived_e4, pivot, delta):
    """Unchanged policy/scope/waiver/detector axes copy E4. Do not invent measured absence.

    Independently admitted pivotPresence supplies E0-E3 when present. Mock maps are not
    full comparison evidence; compare_admitted_v3 is the retained-run adapter.
    """
    unchanged = (
        not delta["detectorChanged"]
        and not delta["policyChanged"]
        and not delta["scopeChanged"]
        and not delta["waiversChanged"]
    )
    presence = {}
    for fp in fps:
        e4 = bool(derived_e4.get(fp, {}).get("E4"))
        waived_c = bool(derived_e4.get(fp, {}).get("waivedC", False))
        measured = {}
        if pivot and fp in pivot:
            pvt = dict(pivot[fp])
            pvt.pop("E4", None)
            pvt.pop("waivedC", None)
            for axis in ("E0", "E1", "E2", "E3"):
                if axis not in pvt:
                    continue
                val = pvt[axis]
                if val is None:
                    continue
                if not isinstance(val, bool):
                    raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "pivotPresence axis must be bool or null", fp)
                measured[axis] = val
        e0, e1, e2, e3 = _presence_from_equalities(e4, delta, measured)
        presence[fp] = {
            "B": fp in b_entries,
            "E0": e0,
            "E1": e1,
            "E2": e2,
            "E3": e3,
            "E4": e4,
            "waivedB": b_entries[fp]["waived"] if fp in b_entries else False,
            "waivedC": waived_c,
        }
    return presence


def _presence_from_equalities(e4, delta, measured):
    """Only copy along axes whose context substitutions are identical.

    E3=E4 iff waivers unchanged; E2=E3 iff scope unchanged; E1=E2 iff policy
    unchanged; E0=E1 iff detector identity/major map unchanged. A later changed
    axis does not authorize copying E4 onto an earlier one.

    Unbound changed axes stay None. None is not false-absence; callers must not
    feed these placeholders into measured availability.
    """
    e3 = measured.get("E3")
    if "E3" not in measured and e3 is None and not delta["waiversChanged"]:
        e3 = e4
    e2 = measured.get("E2")
    if "E2" not in measured and e2 is None and not delta["scopeChanged"] and e3 is not None:
        e2 = e3
    e1 = measured.get("E1")
    if "E1" not in measured and e1 is None and not delta["policyChanged"] and e2 is not None:
        e1 = e2
    e0 = measured.get("E0")
    if "E0" not in measured and e0 is None and not delta["detectorChanged"] and e1 is not None:
        e0 = e1
    if "E0" in measured:
        e0 = measured["E0"]
    if "E1" in measured:
        e1 = measured["E1"]
    if "E2" in measured:
        e2 = measured["E2"]
    if "E3" in measured:
        e3 = measured["E3"]
    return e0, e1, e2, e3


def compare_v3(*, baseline_artifact, current, host, profile_name, current_detectors, accept_origins=()):
    """Matched classify() reuse; unmatched from both sides; E4 derived from occurrences.

    Unmapped/schema/recipe whole refusal does not require E0-E3 maps.
    pivotPresence is optional independently admitted E0-E3; it is not full comparison evidence.
    """
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
    exec_rows = project_execution_deficiencies(current["executionDeficiencies"])
    stub = {
        "runId": current["runId"],
        "snapshotId": current["snapshotId"],
        "projectId": current["projectId"],
        "context": current["context"],
        "ruleCoverage": c_rules,
        "presence": {},
        "entryRules": {},
        "boundPivots": current["boundPivots"],
        "evaluationState": current["evaluationState"],
        "executionDeficiencies": exec_rows,
    }
    if _whole_comparison_without_maps(bdesc, stub, host, accept_origins):
        res = _compare_matched(bdesc, stub, host, profile_name, current_detectors, accept_origins, baseline_id=baseline_artifact["baselineId"])
        return _finish_comparison(res, current, occurrences, waived, profile, bdesc, None)
    bc, cc = bdesc["context"], current["context"]
    delta = {
        "codeChanged": bdesc["source"]["snapshotId"] != current["snapshotId"],
        "detectorChanged": detector_map_changed(bdesc["detectorClosure"], current_detectors),
        "policyChanged": bc["policyDigest"] != cc["policyDigest"],
        "scopeChanged": bc["scopeDigest"] != cc["scopeDigest"],
        "waiversChanged": bc["waiverSetDigest"] != cc["waiverSetDigest"],
        "evidenceAvailabilityChanged": sorted(i["importId"] for i in bc["evidenceAvailability"]["imports"])
        != sorted(i["importId"] for i in cc["evidenceAvailability"]["imports"]),
    }
    pivot = current.get("pivotPresence")
    b_entries = {x["fingerprint"]: x for x in bdesc["entries"]}
    fps = set(b_entries) | set(derived_e4)
    presence = _derive_or_admit_presence(fps, b_entries, derived_e4, pivot, delta)
    current_v1 = dict(stub, presence=presence, entryRules=entry_rules)
    res = _compare_matched(bdesc, current_v1, host, profile_name, current_detectors, accept_origins, baseline_id=baseline_artifact["baselineId"])
    return _finish_comparison(res, current, occurrences, waived, profile, bdesc, None)


def _apply_execution_to_comparison(desc, current):
    desc["currentEvaluationState"] = current["evaluationState"]
    desc["currentExecutionDeficiencies"] = project_execution_deficiencies(current["executionDeficiencies"])
    exec_unknown = bool(current["executionDeficiencies"]) or current["evaluationState"] == "budget-exhausted"
    if exec_unknown and desc.get("verdict") != "fail":
        desc["verdict"] = "indeterminate"
        if current["evaluationState"] == "budget-exhausted":
            desc["d9Deficiency"] = "budget-exhausted"
        else:
            desc["d9Deficiency"] = desc.get("d9Deficiency") or "verdict-indeterminate"
        causes = sorted({d["cause"] for d in desc["currentExecutionDeficiencies"]})
        desc["remedy"] = {
            "code": "EVALUATION.WORK_BUDGET_EXHAUSTED" if current["evaluationState"] == "budget-exhausted" else "COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE",
            "remedy": "current execution deficiencies remain: " + (",".join(causes) if causes else current["evaluationState"]),
        }


def _finish_comparison(res, current, occurrences, waived, profile, bdesc, extra_desc):
    desc = res["descriptor"]
    desc["schemaMajor"] = 2
    _apply_execution_to_comparison(desc, current)
    if extra_desc:
        desc.update(extra_desc)
    current_unmatched = [_unmatched_row(occ, occ["findingId"] in set(waived), "current") for occ in occurrences if occ["finding"]["correspondence"]["state"] == "unmatched"]
    baseline_unmatched = list(bdesc["unmatchedOccurrences"])
    combined = sorted(baseline_unmatched + current_unmatched, key=lambda r: (r["side"].encode(), r["findingId"].encode()))
    if not desc.get("comparisonPerformed"):
        desc["unmatchedOccurrences"] = []
        desc["correspondenceCoverage"] = []
        res["comparisonResultId"] = wid("comparison2", "workflow.comparison", desc)
        res["descriptor"] = desc
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
    _apply_execution_to_comparison(desc, current)
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
    detector_changed = detector_map_changed(baseline["detectorClosure"], current_detectors)
    context_delta = {
        "codeChanged": baseline["source"]["snapshotId"] != current["snapshotId"],
        "detectorChanged": detector_changed,
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
    bound = set(current["boundPivots"])
    methods_ok = all(d["method"] != "indeterminate" for d in dets.values())
    e0_state = (
        "not-needed"
        if not desc["contextDelta"]["detectorChanged"]
        else ("available" if methods_ok else "unavailable")
    )
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
        # Copy E1→E0 only when the selected detector identity/major map is unchanged.
        # Do not copy for a changed detector, including identical-closure with a
        # disagreeing semantics major.
        if m in ("identical-closure", "declared-compatible") and not desc["contextDelta"]["detectorChanged"]:
            pres["E0"] = pres["E1"]
        elif m == "detector-added":
            pres["E0"] = False
        elif m == "detector-removed":
            pres["E1"] = pres["E2"] = pres["E3"] = pres["E4"] = False
        elif m == "indeterminate":
            pres["E0"] = None
        entry_unavail = list(unavailable)
        if desc["contextDelta"]["detectorChanged"] and pres.get("E0") is None and "E0" not in entry_unavail:
            entry_unavail.append("E0")
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
            entry_unavail,
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


def _sarif_uri(path: str) -> str:
    return urllib.parse.quote(path, safe="/")


def project_sarif(occurrences, waived_ids, *, verdict, deficiency=None) -> dict:
    """SARIF 2.1.0 adapter subset: one result per finding3.

    Waived findings emit SARIF suppressions (kind=external, status=accepted) in addition
    to properties.waived. message.id is defined on the rule messageStrings.
    This adapter schema is not a claim of full OASIS SARIF-schema qualification.
    """
    waived = set(waived_ids)
    surfaces = project_finding_surfaces(occurrences, waived_ids)
    by_id = {occ["findingId"]: occ for occ in occurrences}
    rules = []
    seen = set()
    results = []
    for row in surfaces:
        occ = by_id[row["findingId"]]
        if row["ruleId"] not in seen:
            rules.append(
                {
                    "id": row["ruleId"],
                    "shortDescription": {"text": row["messageCode"]},
                    "messageStrings": {row["messageCode"]: {"text": row["messageCode"]}},
                }
            )
            seen.add(row["ruleId"])
        params = occ["parameterRecord"]["parameters"]
        result = {
            "ruleId": row["ruleId"],
            "level": row["severity"],
            "message": {"id": row["messageCode"], "text": row["messageCode"], "properties": dict(params)},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": _sarif_uri(row["subjectPath"])}}}],
            "properties": {
                "findingId": row["findingId"],
                "subjectId": row["subjectId"],
                "correspondence": copy.deepcopy(row["correspondence"]),
                "waived": occ["findingId"] in waived,
                "citations": copy.deepcopy(occ["finding"]["evidenceRefs"]),
            },
        }
        if occ["findingId"] in waived:
            result["suppressions"] = [{"kind": "external", "status": "accepted"}]
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
    """Public envelope StepTermination for output-bound overflow. Root registers the detail key."""
    term = {
        "class": "operational-failed",
        "errorCode": "OUTPUT.SERIALIZATION_FAILED",
        "faultCause": "output-serialization",
        "domainDetail": {
            "code": "EVALUATION.OUTPUT_BOUND_EXCEEDED",
            "remedy": "narrow the admitted output or raise the array/C-byte bound; never truncate to an empty Run",
        },
    }
    validate_profile("urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/StepTermination", term)
    return term


def identity3():
    """Lazy load of root identity-model.v3. Not a copy; not edited."""
    global _ID3
    if _ID3 is None:
        spec = importlib.util.spec_from_file_location(
            "workflow_identity3", HERE.parent / "foundation" / "identity-model.v3.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _ID3 = mod
    return _ID3


def _object(objects, key, domain):
    if key not in objects:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "missing admitted object", key)
    actual, value = objects[key]
    if actual != domain:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "object domain mismatch", key)
    return value


def _blob(blobs, digest, what):
    if digest not in blobs:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "missing admitted blob: " + what, digest)
    return canonical.parse(blobs[digest])


def _analysis_spec_parameters(plan, blobs):
    spec = _blob(blobs, plan["analysisSpecDigest"], "analysisSpec")
    if "parameters" not in spec:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "analysis spec parameters required")
    return spec, spec["parameters"]


def _selected_parameter(M, parameters, blobs, row_key):
    hits = [p for p in parameters if M.parameter_row_of(p["schemaDigest"]) == row_key]
    if len(hits) > 1:
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "at most one selected parameter per registry row", row_key)
    if not hits:
        return None
    return _blob(blobs, hits[0]["payloadDigest"], row_key)


def project_admitted_run_v3(run, objects, blobs, *, dispositions=None, suppression_today=None):
    """Public adapter: close_run full replay, then occurrence maps from admitted proof.

    Reads Plan policy, emission-plan parameter, proof findings, fingerprint
    preimages and parameter records. Does not read producer verified flags or
    expected finding lists. Gating is derived from the admitted policy document.
    Baseline *entry* projection does not require ScopeDocumentV1. Baseline
    *artifact adoption* does, and is not performed when the spec selects none
    (ordinary analysis). open_run_closure is not called.
    """
    M = identity3()
    run_id = M.close_run(run, objects, blobs)
    plan = _object(objects, run["planId"], "plan")
    seal = _object(objects, run["evaluationSealId"], "evaluation-seal")
    proof = _object(objects, seal["proofBundleId"], "proof-bundle")
    policy = _blob(blobs, plan["policyDigest"], "policy")
    if policy.get("schemaMajor") != 2:
        raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "PolicyDocumentV2 required")
    spec, parameters = _analysis_spec_parameters(plan, blobs)
    emission = _selected_parameter(M, parameters, blobs, EMISSION_PARAMETER_ROW)
    if emission is None:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "evaluator-emission-plan parameter is required")
    bindings = {}
    for row in emission["rules"]:
        rid = row["ruleId"]
        if rid in bindings:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "duplicate emission rule", rid)
        bindings[rid] = {
            "ruleId": rid,
            "contributionId": row["contributionId"],
            "ruleStableId": row["ruleStableId"],
            "semanticsMajor": row["semanticsMajor"],
            "detectorClosure": row["detectorClosure"],
            "stabilityClass": row["stabilityClass"],
            "emissionProfile": row["emissionProfile"],
        }
    waived = list(proof["waivedFindingIds"])
    occurrences = []
    for fid in proof["findingIds"]:
        finding = copy.deepcopy(_object(objects, fid, "finding"))
        params = _blob(blobs, finding["parameterDigest"], "finding-parameters")
        occ = {"findingId": fid, "finding": finding, "parameterRecord": params}
        fp = finding["fingerprint"]
        if fp is not None:
            desc = copy.deepcopy(_object(objects, fp, "finding-fingerprint"))
            occ["fingerprintDescriptor"] = desc
        occurrences.append(occ)
        admit_occurrence(occ, bindings[finding["ruleId"]])
    findings_map(occurrences)
    derived = current_run_verdict(
        policy=policy,
        occurrences=occurrences,
        waived_ids=waived,
        rule_results=proof["ruleResults"],
        execution_deficiencies=proof["executionDeficiencies"],
        evaluation_state=proof["evaluationState"],
        proof_verdict=proof["verdict"],
    )
    baseline = project_baseline_entries(occurrences, bindings, waived)
    disp = {} if dispositions is None else dispositions
    if disp and suppression_today is None:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "suppression_today required when dispositions are supplied")
    candidates = project_candidates(
        run_id,
        run["projectId"],
        occurrences,
        policy,
        waived,
        disp,
        suppression_today if suppression_today is not None else "1970-01-01",
        bindings,
    )
    sarif = project_sarif(occurrences, waived, verdict=derived)
    scope_payload = _selected_parameter(M, parameters, blobs, SCOPE_PARAMETER_ROW)
    waivers = _blob(blobs, plan["waiverDigest"], "waivers")
    return {
        "runId": run_id,
        "projectId": run["projectId"],
        "snapshotId": run["snapshotId"],
        "planId": run["planId"],
        "plan": plan,
        "objects": objects,
        "blobs": blobs,
        "proofVerdict": proof["verdict"],
        "derivedVerdict": derived,
        "evaluationState": proof["evaluationState"],
        "policy": policy,
        "waivers": waivers,
        "emissionBindings": bindings,
        "emission": emission,
        "occurrences": occurrences,
        "ruleResults": proof["ruleResults"],
        "waivedFindingIds": waived,
        "executionDeficiencies": proof["executionDeficiencies"],
        "baselineEntries": baseline["entries"],
        "unmatchedOccurrences": baseline["unmatchedOccurrences"],
        "candidates": candidates,
        "sarif": sarif,
        "scopeDocumentParameter": "selected" if scope_payload is not None else "absent",
        "scopeDocument": scope_payload,
        "analysisSpec": spec,
        "evaluationInputRefs": copy.deepcopy(proof.get("evaluationInputRefs") or []),
    }


def _pivot_and_detector_from_plan(plan, objects, emission):
    """One detector row per contributionId. Shared closures are allowed; conflicting semantics refuse.

    Pivot pins include every selected semantic closure whose kind is in the successor PivotClosure set
    (detector, evaluator, provider, toolchain, stdlib, schema-set). Provider closures are retained
    because the origin Run selected them.
    """
    by_id = {}
    for row in emission["rules"]:
        did = row["contributionId"]
        clo = _object(objects, row["detectorClosure"], "closure")
        rec = {
            "detectorId": did,
            "closureId": row["detectorClosure"],
            "semanticsMajor": row["semanticsMajor"],
            "semanticVersion": clo.get("semanticVersion", "0.0.0"),
            "contributionId": did,
            "manifestDigest": clo["manifestDigest"],
        }
        if did in by_id and canonical.canonical(by_id[did]) != canonical.canonical(rec):
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "conflicting emission rows for detector identity", did)
        by_id[did] = rec
    detectors = [by_id[k] for k in sorted(by_id, key=lambda s: s.encode())]
    pivots = []
    for cid in plan["semanticClosures"]:
        clo = _object(objects, cid, "closure")
        kind = clo["kind"]
        if kind not in PIVOT_KINDS:
            raise Refusal(
                "REQUEST.PRECONDITION_FAILED",
                "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
                "selected semantic closure kind is not a typed pivot kind: " + kind,
                cid,
            )
        pivots.append(
            {
                "closureId": cid,
                "kind": kind,
                "manifestDigest": clo["manifestDigest"],
                "protocolMajor": clo["protocolMajor"],
                "platform": clo["platform"],
            }
        )
    pivots.sort(key=lambda p: p["closureId"])
    return detectors, pivots


def _selected_view_fact_relations(objects, input_refs):
    """Relations from admitted selected views/input refs only. No ambient object-map scan."""
    relations = set()
    for ref in input_refs or []:
        domain = ref.get("domain")
        digest = ref.get("digest")
        if not digest:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "evaluationInputRef missing digest")
        if domain == "view":
            key = "view2:" + digest
            val = _object(objects, key, "view")
            for fid in val.get("facts", []):
                if fid not in objects:
                    raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "selected view fact missing", fid)
                if objects[fid][0] != "fact":
                    raise Refusal("REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR", "selected view fact domain", fid)
                rel = objects[fid][1].get("relation")
                if rel:
                    relations.add(rel)
        elif domain == "fact":
            key = "fact2:" + digest
            val = _object(objects, key, "fact")
            rel = val.get("relation")
            if rel:
                relations.add(rel)
    return sorted(relations, key=lambda s: s.encode())


def _context_from_admitted(plan, objects, blobs, policy, scope, waivers, detectors, input_refs):
    """Context from Plan-selected imports and admitted selected views/input refs.

    Unrelated objects in the closure map are not an authority for relations.
    """
    imports = []
    selected_imports = list(plan.get("importIds", []))
    for ref in input_refs or []:
        if ref.get("domain") == "import":
            iid = "import2:" + ref["digest"]
            if iid not in selected_imports:
                selected_imports.append(iid)
    for iid in selected_imports:
        wrap = _object(objects, iid, "import")
        imports.append(
            {
                "kind": wrap["kind"],
                "importId": iid,
                "payloadDigest": wrap["payloadDigest"],
                "sourceCorrespondenceDigest": wrap["sourceCorrespondenceDigest"],
                "scopeDigest": wrap["scopeDigest"],
                "observationDigest": wrap["observationDigest"],
            }
        )
    imports.sort(key=lambda i: i["importId"].encode())
    kinds = sorted({i["kind"] for i in imports})
    relations = _selected_view_fact_relations(objects, input_refs)
    if scope is None:
        raise Refusal(
            "REQUEST.PRECONDITION_FAILED",
            "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
            "baseline/comparison require a selected ScopeDocumentV1; foundation plan.scopeDigest is a different owner",
        )
    return {
        "policyDigest": plan["policyDigest"],
        "scopeDigest": doc_digest(scope),
        "waiverSetDigest": plan["waiverDigest"],
        "detectorClosureIds": sorted({d["closureId"] for d in detectors}),
        "evidenceAvailability": {
            "importKinds": kinds,
            "relations": relations,
            "imports": imports,
        },
    }


def required_coverage_from_rule_result(rule, rr) -> str:
    """Complete inventory is not complete required evidence.

    Provenance is admitted rule truth: a determinate pass/fail outcome keeps
    coverage satisfied even when Boolean roots retain nonblocking required-partial
    diagnostics. Indeterminate outcomes use required-evidence causes. Inventory
    completeness alone never upgrades an unknown required plane.
    """
    if not rule["enabled"] or rr["outcome"] == "disabled":
        return "satisfied"
    if rr["outcome"] in ("pass", "fail"):
        return "satisfied"
    required_kinds = {v["kind"] for v in rule.get("evidenceUse", []) if v.get("requirement") == "required"}
    required_unknown = False
    required_unsatisfied = False
    for d in rr["deficiencies"]:
        if d.get("source") == "import" and d.get("evidenceKind") in required_kinds:
            required_unknown = True
        if d.get("source") in ("native", "execution") and deficiency_blocks(rule, d):
            required_unknown = True
        if d.get("cause") in ("required-relation-missing", "required-cell-unsatisfied", "import-absent-for-requirement"):
            required_unsatisfied = True
    if required_unsatisfied:
        return "unsatisfied"
    if required_unknown or rr["enumeration"]["state"] == "incomplete" or rr["outcome"] == "indeterminate":
        return "unknown"
    return "satisfied"


def _rule_coverage_from_admitted(policy, rule_results):
    by = {r["ruleId"]: r for r in rule_results}
    out = []
    for rule in policy["rules"]:
        rr = by[rule["ruleId"]]
        out.append(
            {
                "ruleId": rule["ruleId"],
                "requiredCoverage": required_coverage_from_rule_result(rule, rr),
                "enabled": bool(rule["enabled"]),
                "gating": rule_gates(policy, rule["ruleId"]),
                "evidenceUse": copy.deepcopy(rule["evidenceUse"]),
            }
        )
    return out


def adopt_admitted_baseline_v3(run, objects, blobs, custody):
    """Public baseline adoption: close_run, then join Plan policy/scope/waivers/snapshot.

    ScopeDocumentV1 must be a selected analysis-spec parameter. custody.exportedAtUtc is
    trusted caller input. Does not accept authority/availability flags in place of the Run.
    """
    view = project_admitted_run_v3(run, objects, blobs)
    if view["scopeDocumentParameter"] != "selected" or view["scopeDocument"] is None:
        raise Refusal(
            "REQUEST.PRECONDITION_FAILED",
            "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
            "ordinary analysis may select zero ScopeDocumentV1; baseline adoption requires one",
        )
    plan = view["plan"]
    if doc_digest(view["policy"]) != plan["policyDigest"]:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING", "policy is not the Plan-selected document")
    if doc_digest(view["waivers"]) != plan["waiverDigest"]:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING", "waivers are not the Plan-selected document")
    detectors, pivots = _pivot_and_detector_from_plan(plan, objects, view["emission"])
    if not detectors or not pivots:
        raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "origin detector and pivot closures required")
    ctx = _context_from_admitted(
        plan,
        objects,
        blobs,
        view["policy"],
        view["scopeDocument"],
        view["waivers"],
        detectors,
        view["evaluationInputRefs"],
    )
    coverage = _rule_coverage_from_admitted(view["policy"], view["ruleResults"])
    overlay = {
        "authority": "authoritative",
        "availability": "retained",
        "runId": view["runId"],
        "snapshotId": view["snapshotId"],
    }
    return adopt_baseline_v3(
        overlay,
        view["planId"],
        view["projectId"],
        view["policy"],
        view["scopeDocument"],
        view["waivers"],
        coverage,
        {"entries": view["baselineEntries"], "unmatchedOccurrences": view["unmatchedOccurrences"]},
        detectors,
        pivots,
        ctx,
        view["analysisSpec"],
        custody,
    )


def _current_from_admitted_view(view, bound=None, pivots=None):
    if view["scopeDocumentParameter"] != "selected" or view["scopeDocument"] is None:
        raise Refusal(
            "REQUEST.PRECONDITION_FAILED",
            "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
            "comparison requires selected ScopeDocumentV1 on the current Run",
        )
    req = {r["ruleId"]: required_coverage_from_rule_result(next(x for x in view["policy"]["rules"] if x["ruleId"] == r["ruleId"]), r) for r in view["ruleResults"]}
    detectors, _ = _pivot_and_detector_from_plan(view["plan"], view["objects"], view["emission"])
    ctx = _context_from_admitted(
        view["plan"],
        view["objects"],
        view["blobs"],
        view["policy"],
        view["scopeDocument"],
        view["waivers"],
        detectors,
        view["evaluationInputRefs"],
    )
    return {
        "runId": view["runId"],
        "snapshotId": view["snapshotId"],
        "projectId": view["projectId"],
        "policy": view["policy"],
        "occurrences": view["occurrences"],
        "ruleResults": view["ruleResults"],
        "waivedFindingIds": view["waivedFindingIds"],
        "executionDeficiencies": view["executionDeficiencies"],
        "evaluationState": view["evaluationState"],
        "emissionBindings": view["emissionBindings"],
        "context": ctx,
        "requiredCoverage": req,
        "boundPivots": [] if bound is None else bound,
        **({"pivotPresence": pivots} if pivots is not None else {}),
    }


def _host_portable_platforms(host):
    """Rewrite host comparison metadata only.

    Closure platform `any` is rewritten on the deepcopy of host.closures records used
    for resolve_detectors comparison. This never mutates admitted closure descriptors,
    manifestDigest, object-map identity, or any closure hash. It does not accept
    untrusted compatibleWith; authentic manifest join remains an explicit product
    contract if a later owner requires declared compatibility.
    """
    h = copy.deepcopy(host)
    plat = h["platform"]
    for rec in h.get("closures", {}).values():
        if rec.get("platform") == "any":
            rec["platform"] = plat
    return h


def _emission_detectors(view):
    dets = {}
    for row in view["emission"]["rules"]:
        did = row["contributionId"]
        rec = {"closureId": row["detectorClosure"], "semanticsMajor": row["semanticsMajor"], "compatibleWith": []}
        if did in dets and canonical.canonical(dets[did]) != canonical.canonical(rec):
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "conflicting detector identity", did)
        dets[did] = rec
    return dets


def _assert_detector_override(actual, override):
    if not override:
        return actual
    for did, rec in override.items():
        if did not in actual:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "current_detectors names a detector not in admitted emission", did)
        if rec.get("closureId") != actual[did]["closureId"] or rec.get("semanticsMajor") != actual[did]["semanticsMajor"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "current_detectors does not match admitted emission closure/semanticsMajor", did)
        if rec.get("compatibleWith"):
            raise Refusal(
                "REQUEST.PRECONDITION_FAILED",
                "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
                "compatibleWith requires authenticated detector-manifest provenance, not an arbitrary map",
                did,
            )
    extra = set(actual) - set(override)
    if extra:
        raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "current_detectors is not total over admitted emission")
    return actual


def _effective_matched_presence(view):
    """Same effective presence law as derive_current_matched E4, including waived matched findings."""
    incomplete = any(rr["enumeration"]["state"] == "incomplete" for rr in view["ruleResults"])
    presence, _ = derive_current_matched(view["occurrences"], view["waivedFindingIds"], view["emissionBindings"])
    return {fp: bool(rec.get("E4")) for fp, rec in presence.items()}, incomplete


def _bind_pivot_runs(pivot_runs, baseline, current_view):
    """Verify each supplied pivot Run against section-3 substitutions and measure matched fingerprints."""
    if not pivot_runs:
        return {}, []
    bctx = baseline["descriptor"]["context"]
    bdocs = baseline["descriptor"]["contextDocuments"]
    measured = {axis: {} for axis in PIVOT_AXES}
    bound = []
    want = {
        "E0": {
            "snapshotId": current_view["snapshotId"],
            "policyDigest": bctx["policyDigest"],
            "scopeDigest": bctx["scopeDigest"],
            "waiverSetDigest": bctx["waiverSetDigest"],
            "detector": "baseline",
        },
        "E1": {
            "snapshotId": current_view["snapshotId"],
            "policyDigest": bctx["policyDigest"],
            "scopeDigest": bctx["scopeDigest"],
            "waiverSetDigest": bctx["waiverSetDigest"],
            "detector": "current",
        },
        "E2": {
            "snapshotId": current_view["snapshotId"],
            "policyDigest": current_view["plan"]["policyDigest"],
            "scopeDigest": bctx["scopeDigest"],
            "waiverSetDigest": bctx["waiverSetDigest"],
            "detector": "current",
        },
        "E3": {
            "snapshotId": current_view["snapshotId"],
            "policyDigest": current_view["plan"]["policyDigest"],
            "scopeDigest": doc_digest(current_view["scopeDocument"]),
            "waiverSetDigest": bctx["waiverSetDigest"],
            "detector": "current",
        },
    }
    for axis, graph in pivot_runs.items():
        if axis not in want:
            raise Refusal("REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE", "unknown pivot axis", axis)
        run, objects, blobs = graph
        pview = project_admitted_run_v3(run, objects, blobs)
        if pview["scopeDocumentParameter"] != "selected":
            raise Refusal("REQUEST.PRECONDITION_FAILED", "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER", "pivot Run must select ScopeDocumentV1", axis)
        got_scope = doc_digest(pview["scopeDocument"])
        spec = want[axis]
        if pview["snapshotId"] != spec["snapshotId"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "pivot snapshot is not current source", axis)
        if pview["plan"]["policyDigest"] != spec["policyDigest"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "pivot policyDigest does not match axis substitution", axis)
        if got_scope != spec["scopeDigest"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "pivot ScopeDocument does not match axis substitution", axis)
        if pview["plan"]["waiverDigest"] != spec["waiverSetDigest"]:
            raise Refusal("CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED", "pivot waiverDigest does not match axis substitution", axis)
        if spec["detector"] == "current":
            require_exact_detector_map(_emission_detectors(pview), _emission_detectors(current_view), axis)
        elif spec["detector"] == "baseline":
            require_exact_detector_map(_emission_detectors(pview), baseline["descriptor"]["detectorClosure"], axis)
        fps, incomplete = _effective_matched_presence(pview)
        if incomplete:
            continue
        measured[axis] = {fp: True for fp, present in fps.items() if present}
        bound.append(axis)
    return measured, bound


def compare_admitted_v3(
    *,
    baseline_artifact,
    current_run,
    current_objects,
    current_blobs,
    host,
    profile_name,
    current_detectors=None,
    accept_origins=(),
    pivot_runs=None,
):
    """Compare a verified baseline artifact to an admitted current Run.

    pivot_runs: optional {E0|E1|E2|E3: (run, objects, blobs)} each close_run'd and
    bound to section-3 substitutions. Incomplete pivot population is not false absence.
    current_detectors may only repeat admitted emission identity; compatibleWith is refused.
    detectorChanged is the exact selected detector identity/major map, never a subset of IDs.
    Unbound pivot axes stay None; they are not false-absence.
    """
    verify_baseline_artifact_v3(baseline_artifact)
    view = project_admitted_run_v3(current_run, current_objects, current_blobs)
    dets = _assert_detector_override(_emission_detectors(view), current_detectors)
    axis_measured, bound = _bind_pivot_runs(pivot_runs or {}, baseline_artifact, view)
    fps_union = {e["fingerprint"] for e in baseline_artifact["descriptor"]["entries"]} | {
        o["finding"]["fingerprint"] for o in view["occurrences"] if o["finding"]["fingerprint"]
    }
    pivot_presence = {}
    e4_map, _ = derive_current_matched(view["occurrences"], view["waivedFindingIds"], view["emissionBindings"])
    delta = {
        "detectorChanged": detector_map_changed(baseline_artifact["descriptor"]["detectorClosure"], dets),
        "policyChanged": baseline_artifact["descriptor"]["context"]["policyDigest"] != view["plan"]["policyDigest"],
        "scopeChanged": baseline_artifact["descriptor"]["context"]["scopeDigest"] != doc_digest(view["scopeDocument"]),
        "waiversChanged": baseline_artifact["descriptor"]["context"]["waiverSetDigest"] != view["plan"]["waiverDigest"],
    }
    bound_set = set(bound)
    for fp in fps_union:
        measured = {}
        for axis in PIVOT_AXES:
            if axis not in bound_set:
                continue
            hits = axis_measured[axis]
            measured[axis] = bool(hits.get(fp))
        e4 = bool(e4_map.get(fp, {}).get("E4"))
        e0, e1, e2, e3 = _presence_from_equalities(e4, delta, measured)
        pivot_presence[fp] = {"E0": e0, "E1": e1, "E2": e2, "E3": e3}
    current = _current_from_admitted_view(view, bound=bound, pivots=pivot_presence)
    return compare_v3(
        baseline_artifact=baseline_artifact,
        current=current,
        host=_host_portable_platforms(host),
        profile_name=profile_name,
        current_detectors=dets,
        accept_origins=accept_origins,
    )
