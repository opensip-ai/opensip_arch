"""Bounded evaluator3 workflow schema + projection checks. Not full Run replay.

Run: /tmp/opensip-architecture-review-env/bin/python -I -B check-workflow-projection.v3.py
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
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

spec = importlib.util.spec_from_file_location("proj", HERE / "workflow_projection_model.v3.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

E3 = HERE / "schemas" / "evaluator3"
WF = HERE / "schemas"
CHECKS = []


def check(cid, ok, detail=""):
    CHECKS.append({"id": cid, "ok": bool(ok), "detail": "" if ok else str(detail)[:240]})
    return bool(ok)


def token(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def hid(prefix: str, s: str) -> str:
    return prefix + ":" + token(s)


SCHEMAS = {}
for p in sorted(E3.glob("*.schema.json")):
    doc = canonical.parse(p.read_bytes())
    Draft202012Validator.check_schema(doc)
    SCHEMAS[doc["$id"]] = doc
for name in (
    "common.schema.json",
    "imported-evidence.schema.json",
    "policy-document.schema.json",
    "policy-document.v2.schema.json",
    "test-execution.schema.json",
):
    path = WF / name
    if path.exists():
        doc = canonical.parse(path.read_bytes())
        Draft202012Validator.check_schema(doc)
        SCHEMAS[doc["$id"]] = doc

REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
)
U = "urn:opensip:product-v1:workflows:evaluator3:"


def validator(ref: str):
    return canonical.ExactValidator({"$ref": ref}, registry=REG)


def valid(ref, value):
    try:
        canonical.typed(value)
        validator(ref).validate(value)
        return True, ""
    except (ValidationError, canonical.AdmissionError, Exception) as exc:
        return False, str(exc).splitlines()[0][:200]


def must_valid(cid, ref, value):
    ok, why = valid(ref, value)
    return check(cid, ok, why)


def must_invalid(cid, ref, value):
    ok, _ = valid(ref, value)
    return check(cid, not ok, "unexpectedly valid")


def reject(cid, fn, error=None, detail=None):
    try:
        fn()
    except P.Refusal as exc:
        ok = True
        if error is not None:
            ok = ok and exc.error_code == error
        if detail is not None:
            ok = ok and exc.detail == detail
        return check(cid, ok, f"{exc.error_code}/{exc.detail}")
    return check(cid, False, "expected refusal")


RUN = "run3:" + token("run")
PLAN = "plan2:" + token("plan")
SNAP = "snapshot2:" + token("snap")
PRJ = "prj1-" + token("proj")
DET = "closure2:" + token("detector")
SCOPE = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}
WAIVERS = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
ATOM = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}
RULE = {
    "ruleId": "r",
    "ruleProgramRef": {
        "contributionId": "fixture",
        "ruleStableId": "r",
        "semanticsMajor": 2,
        "programDigest": token("prog"),
    },
    "enabled": True,
    "severity": "error",
    "gate": True,
    "subjectEnumeration": {"universe": "typescript", "subjectKind": "file"},
    "emitWhen": ATOM,
    "evidenceUse": [],
}
POLICY = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 2,
    "gateSeverityAtLeast": "error",
    "rules": [RULE],
}
POLICY_ADVISORY = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 2,
    "gateSeverityAtLeast": "error",
    "rules": [dict(RULE, gate=False)],
}
BINDING = {
    "ruleId": "r",
    "contributionId": "fixture",
    "ruleStableId": "r",
    "semanticsMajor": 2,
    "detectorClosure": DET,
    "stabilityClass": "path-stable",
    "emissionProfile": "declarative-subject-v1",
}
CUSTODY = {"exportedAtUtc": "2026-09-08T00:00:00Z", "exportedByHostRelease": "1.0.0"}


def fp_desc(path="src/a.ts", name="src/a.ts", kind="file", disc=None):
    if disc is None:
        disc = hashlib.sha256(canonical.canonical([])).hexdigest()
    return {
        "schemaVersion": 2,
        "ruleStableId": "r",
        "detectorSemanticsMajor": 2,
        "subjectKey": {
            "language": "typescript",
            "kind": kind,
            "logicalPath": path,
            "qualifiedName": name,
            "discriminator": disc,
        },
        "relatedSubjectKeys": [],
    }


def params(path="src/a.ts", name="src/a.ts", kind="file", facts=0, imports=0, language="typescript"):
    return {
        "schemaVersion": 2,
        "messageCode": "r",
        "parameters": {
            "ruleId": "r",
            "subjectPath": path,
            "qualifiedName": name,
            "subjectKind": kind,
            "subjectLanguage": language,
            "matchingFactCount": facts,
            "matchingImportCount": imports,
        },
    }


def occurrence(tag, *, unmatched=False, reason=None, universe="one", path="src/a.ts", facts=0, legacy=None, kind=None, name=None, subject_id=None):
    if kind is None:
        kind = "symbol" if unmatched and reason == "projection-unavailable" else "file"
    if name is None:
        name = "f" if kind == "symbol" else ("pkg" if kind == "package" else path)
    desc = None if unmatched else fp_desc(path, name, kind)
    fp = None if unmatched else P.fingerprint_id(desc)
    par = params(path, name, kind, facts=facts)
    if subject_id is None:
        subject_id = hid("subject3", universe + "|" + path + "|" + kind + "|" + name)
    finding = {
        "schemaVersion": 3,
        "fingerprint": fp,
        "ruleClosure": DET,
        "subjectId": subject_id,
        "messageCode": "r",
        "parameterDigest": P.sha(par),
        "severity": "error",
        "evidenceRefs": [],
        "ruleId": "r",
        "subject": {"language": "typescript", "kind": kind, "logicalPath": path, "qualifiedName": name},
        "correspondence": {
            "state": "unmatched" if unmatched else "matched",
            "reason": reason if unmatched else None,
        },
    }
    occ = {"findingId": hid("finding3", tag), "finding": finding, "parameterRecord": par}
    if desc is not None:
        occ["fingerprintDescriptor"] = desc
    if legacy is not None:
        occ["legacyFingerprint"] = legacy
    return occ


def empty_evidence():
    return {"importKinds": [], "relations": [], "imports": []}


def rule_cov(gating=True, required="satisfied"):
    return {
        "ruleId": "r",
        "requiredCoverage": required,
        "enabled": True,
        "gating": gating,
        "evidenceUse": [],
    }


def ctx():
    return {
        "policyDigest": P.doc_digest(POLICY),
        "scopeDigest": P.doc_digest(SCOPE),
        "waiverSetDigest": P.doc_digest(WAIVERS),
        "detectorClosureIds": [DET],
        "evidenceAvailability": empty_evidence(),
    }


def host():
    return {
        "closures": {DET: {"bytes": "ok", "trust": "admitted", "protocolMajor": 1, "platform": "linux"}},
        "protocolMajors": [1],
        "platform": "linux",
        "pivotRunId": RUN,
        "recipeMajors": [2],
    }


def detectors():
    return {"fixture": {"closureId": DET, "semanticsMajor": 2, "compatibleWith": []}}


def complete_enum():
    return {
        "state": "complete",
        "inventoryRefs": [],
        "selectedSubjectIds": [],
        "unresolvedSubjectIds": [],
        "incompleteInventoryRefs": [],
    }


def incomplete_enum():
    e = complete_enum()
    e["state"] = "incomplete"
    return e


def rr(*, outcome, enum=None, findings=None, deficiencies=None):
    return {
        "ruleId": "r",
        "enumeration": enum if enum is not None else complete_enum(),
        "outcome": outcome,
        "findingIds": findings or [],
        "deficiencies": deficiencies or [],
    }


def detector_closure_entries():
    return [
        {
            "detectorId": "fixture",
            "closureId": DET,
            "semanticsMajor": 2,
            "semanticVersion": "1.0.0",
            "contributionId": "fixture",
            "manifestDigest": token("man"),
        }
    ]


def pivot_entries():
    return [
        {
            "closureId": DET,
            "kind": "detector",
            "manifestDigest": token("man"),
            "protocolMajor": 1,
            "platform": "linux",
        }
    ]


def scope_spec():
    digest = hashlib.sha256((WF / "policy-document.schema.json").read_bytes()).hexdigest()
    return {"parameters": [{"schemaDigest": digest, "payloadDigest": P.doc_digest(SCOPE)}]}


def adopt(projected, run_id=RUN):
    run = {"authority": "authoritative", "availability": "retained", "runId": run_id, "snapshotId": SNAP}
    return P.adopt_baseline_v3(
        run,
        PLAN,
        PRJ,
        POLICY,
        SCOPE,
        WAIVERS,
        [rule_cov()],
        projected,
        detector_closure_entries(),
        pivot_entries(),
        ctx(),
        scope_spec(),
        CUSTODY,
    )


def pivot_true(fps):
    return {fp: {"E0": False, "E1": True, "E2": True, "E3": True} for fp in fps}


def make_current(*, occurrences, rule_results, policy=None, waived=None, required=None, run_id=None, snapshot=None, project=None, execution=None, state="evaluated", pivots=None, bound=None):
    occs = occurrences
    fps = [o["finding"]["fingerprint"] for o in occs if o["finding"]["fingerprint"]]
    return {
        "runId": run_id or hid("run3", "cur"),
        "snapshotId": snapshot or hid("snapshot2", "cur"),
        "projectId": project if project is not None else PRJ,
        "policy": policy or POLICY,
        "occurrences": occs,
        "ruleResults": rule_results,
        "waivedFindingIds": waived or [],
        "executionDeficiencies": execution or [],
        "evaluationState": state,
        "emissionBindings": {"r": BINDING},
        "context": ctx(),
        "requiredCoverage": required or {"r": "satisfied"},
        "boundPivots": bound if bound is not None else [],
        "pivotPresence": pivots if pivots is not None else pivot_true(fps),
        "proofVerdict": None,
    }


def verdict(**kwargs):
    cur = make_current(**kwargs)
    return P.current_run_verdict(
        policy=cur["policy"],
        occurrences=cur["occurrences"],
        waived_ids=cur["waivedFindingIds"],
        rule_results=cur["ruleResults"],
        execution_deficiencies=cur["executionDeficiencies"],
        evaluation_state=cur["evaluationState"],
        proof_verdict=kwargs.get("proof_verdict"),
    )


# ----------------------------------------------------------------------------- schema shape vs v1
check("schema-count", len(list(E3.glob("*.schema.json"))) == 10)
check("common-run3-not-mixed", SCHEMAS[U + "common:3"]["$defs"]["RunId"]["pattern"].startswith("^run3:"))
check("common-no-run2-alternation", "run[23]" not in json.dumps(SCHEMAS[U + "common:3"]["$defs"]["RunId"]))
check("fingerprint-retained-key2", SCHEMAS[U + "common:3"]["$defs"]["Fingerprint"]["pattern"].startswith("^finding-key2:"))
v1_base = json.loads((WF / "baseline-artifact.schema.json").read_text())
v1_cmp = json.loads((WF / "comparison-result.schema.json").read_text())
v1_env = json.loads((WF / "command-envelope.schema.json").read_text())
v1_inv = json.loads((WF / "invocation-record.schema.json").read_text())
v1_q = json.loads((WF / "graph-query.schema.json").read_text())
v1_rep = json.loads((WF / "repair.schema.json").read_text())
check("v1-baseline-identity-major-was-1", v1_base["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-comparison-identity-major-was-1", v1_cmp["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-envelope-major-was-2", v1_env["properties"]["schemaMajor"]["const"] == 2)
check("v1-invocation-major-was-1", v1_inv["properties"]["schemaMajor"]["const"] == 1)
check("v1-query-major-was-1", v1_q["$defs"]["GraphQueryRequestV1"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-repair-plan-major-was-1", v1_rep["$defs"]["RepairPlanDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("unmatched-requires-side", "side" in SCHEMAS[U + "common:3"]["$defs"]["UnmatchedOccurrence"]["required"])
must_invalid("run2-prefix-refused", U + "common:3#/$defs/RunId", "run2:" + "a" * 64)
must_valid("run3-prefix-admitted", U + "common:3#/$defs/RunId", "run3:" + "a" * 64)

surf_matched = {
    "findingId": hid("finding3", "s1"),
    "ruleId": "r",
    "subjectId": hid("subject3", "s1"),
    "subjectPath": "src/a.ts",
    "severity": "error",
    "messageCode": "r",
    "correspondence": {"state": "matched", "reason": None},
    "fingerprint": "finding-key2:" + "a" * 64,
    "waived": False,
    "partialFingerprints": {"opensip/finding-key2": "finding-key2:" + "a" * 64},
}
must_valid("finding-surface-matched", U + "common:3#/$defs/FindingSurface", surf_matched)
surf_unmatched = copy.deepcopy(surf_matched)
surf_unmatched["correspondence"] = {"state": "unmatched", "reason": "signature-ambiguous"}
surf_unmatched["fingerprint"] = None
del surf_unmatched["partialFingerprints"]
must_valid("finding-surface-unmatched-null-fp", U + "common:3#/$defs/FindingSurface", surf_unmatched)

# ----------------------------------------------------------------------------- two-config / package / baseline
a = occurrence("cfg-a", universe="one", facts=0)
b = occurrence("cfg-b", universe="two", facts=3)
check("two-config-same-logical-fingerprint", a["finding"]["fingerprint"] == b["finding"]["fingerprint"])
proj = P.project_baseline_entries([a, b], {"r": BINDING}, [])
check("two-config-one-baseline-entry", len(proj["entries"]) == 1 and len(proj["unmatchedOccurrences"]) == 0)
pkg_a = occurrence("pkg-a", kind="package", name="dup", path="crates/a/Cargo.toml", universe="u", subject_id=hid("subject3", "pkg-a-opaque"))
pkg_b = occurrence("pkg-b", kind="package", name="dup", path="crates/b/Cargo.toml", universe="u", subject_id=hid("subject3", "pkg-b-opaque"))
check("package-manifest-path-owns-fingerprint", pkg_a["finding"]["fingerprint"] != pkg_b["finding"]["fingerprint"])
art = adopt(proj)
check("adopt-schema-major-2", art["descriptor"]["schemaMajor"] == 2)
check("adopt-uses-trusted-custody-timestamp", art["custody"]["exportedAtUtc"] == CUSTODY["exportedAtUtc"])
must_valid("baseline-artifact-schema", U + "baseline:2", art)
P.verify_baseline_artifact_v3(art)

c = occurrence("leg-a", universe="one")
d = occurrence("leg-b", universe="two", legacy="old-key")
reject("legacy-optional-presence-conflict", lambda: P.project_baseline_entries([c, d], {"r": BINDING}, []), "CONFIG.INVALID", "BASELINE.ENTRY_PROJECTION_CONFLICT")
reject(
    "adopt-requires-scope-parameter",
    lambda: P.adopt_baseline_v3(
        {"authority": "authoritative", "availability": "retained", "runId": RUN, "snapshotId": SNAP},
        PLAN, PRJ, POLICY, SCOPE, WAIVERS, [rule_cov()], proj,
        detector_closure_entries(), pivot_entries(), ctx(), None, CUSTODY,
    ),
    "REQUEST.PRECONDITION_FAILED",
    "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
)

# ----------------------------------------------------------------------------- gating from policy, not ruleResults
u = occurrence("un-1", unmatched=True, reason="signature-ambiguous")
check(
    "nongating-live-finding-does-not-fail",
    verdict(occurrences=[u], rule_results=[rr(outcome="pass")], policy=POLICY_ADVISORY) == "pass",
)
check(
    "gating-live-unmatched-fails",
    verdict(occurrences=[u], rule_results=[rr(outcome="fail", findings=[u["findingId"]])], policy=POLICY) == "fail",
)
check(
    "path-waiver-current-pass",
    verdict(occurrences=[u], rule_results=[rr(outcome="pass", findings=[u["findingId"]])], waived=[u["findingId"]], policy=POLICY) == "pass",
)
check(
    "execution-deficiency-independent-indeterminate",
    verdict(
        occurrences=[],
        rule_results=[rr(outcome="disabled", enum={"state": "disabled", "inventoryRefs": [], "selectedSubjectIds": [], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []})],
        execution=[{"source": "execution", "cause": "required-cell-unsatisfied", "subjectId": None, "predicateId": None, "inputRefs": [], "evidenceKind": None, "nativeCause": None, "universe": None}],
        policy={"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [dict(RULE, enabled=False)]},
    )
    == "indeterminate",
)
check(
    "budget-exhausted-independent",
    verdict(occurrences=[], rule_results=[rr(outcome="indeterminate", enum=incomplete_enum())], state="budget-exhausted") == "indeterminate",
)

# ----------------------------------------------------------------------------- comparison: derive E4, baseline unmatched, profiles
proj_u = P.project_baseline_entries([u], {"r": BINDING}, [])
art_u = adopt(proj_u)
base_u = art_u
current_u = make_current(occurrences=[u], rule_results=[rr(outcome="fail", findings=[u["findingId"]])])
cmp_u = P.compare_v3(baseline_artifact=base_u, current=current_u, host=host(), profile_name="code-regression", current_detectors=detectors())
check("unmatched-not-classified-as-net-new", all(e.get("classification") != "CODE-NET-NEW" for e in cmp_u["descriptor"]["entries"]))
check(
    "unmatched-audit-correspondence-incomplete",
    cmp_u["descriptor"]["verdict"] == "indeterminate"
    and any(d["cause"] == "correspondence-incomplete" for d in cmp_u["descriptor"]["ruleDeficiencies"]),
)
must_valid("comparison-artifact-schema", U + "comparison:2", {"comparisonResultId": cmp_u["comparisonResultId"], "descriptor": cmp_u["descriptor"]})

current_w = make_current(occurrences=[u], rule_results=[rr(outcome="pass", findings=[u["findingId"]])], waived=[u["findingId"]])
cmp_w = P.compare_v3(baseline_artifact=base_u, current=current_w, host=host(), profile_name="code-regression", current_detectors=detectors())
check("path-waiver-audit-still-unknown", cmp_w["descriptor"]["verdict"] == "indeterminate" and any(x["waived"] for x in cmp_w["descriptor"]["unmatchedOccurrences"] if x["side"] == "current"))

# missing occurrences heals not allowed
bad_cur = dict(current_u)
del bad_cur["occurrences"]
reject(
    "compare-requires-occurrences",
    lambda: P.compare_v3(baseline_artifact=base_u, current=bad_cur, host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
reject(
    "compare-rejects-supplied-presence",
    lambda: P.compare_v3(baseline_artifact=base_u, current=dict(current_u, presence={}), host=host(), profile_name="code-regression", current_detectors=detectors()),
    "CONFIG.INVALID",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)

# baseline unmatched survives current empty under baseline-or-current
empty_current = make_current(occurrences=[], rule_results=[rr(outcome="pass")], snapshot=SNAP)
# same snapshot so code axis unchanged; no current findings
cmp_b = P.compare_v3(baseline_artifact=base_u, current=empty_current, host=host(), profile_name="code-regression", current_detectors=detectors())
check(
    "baseline-unmatched-survives-current-empty-baseline-or-current",
    any(d["cause"] == "correspondence-incomplete" and d["gating"] for d in cmp_b["descriptor"]["ruleDeficiencies"])
    and any(x["side"] == "baseline" for x in cmp_b["descriptor"]["unmatchedOccurrences"]),
)
# current-only: rule removed
POLICY_REMOVED = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [dict(RULE, ruleId="other")]}
# need ruleResult for other
other_rr = dict(rr(outcome="pass"), ruleId="other")
empty_removed = make_current(
    occurrences=[],
    rule_results=[other_rr],
    policy=POLICY_REMOVED,
    required={"other": "satisfied"},
    snapshot=SNAP,
)
empty_removed["emissionBindings"] = {"other": dict(BINDING, ruleId="other")}
cmp_co = P.compare_v3(baseline_artifact=base_u, current=empty_removed, host=host(), profile_name="full-current", current_detectors=detectors())
check(
    "current-only-removed-rule-does-not-inherit-baseline-unmatched-gate",
    not any(d["cause"] == "correspondence-incomplete" and d["ruleId"] == "r" for d in cmp_co["descriptor"]["ruleDeficiencies"]),
)

# matched regression dominates unknown
m = occurrence("reg-new", universe="cur-only")
proj_empty = P.project_baseline_entries([], {"r": BINDING}, [])
art_empty = adopt(proj_empty)
current_reg = make_current(
    occurrences=[m, u],
    rule_results=[rr(outcome="fail", findings=[m["findingId"], u["findingId"]])],
)
cmp_reg = P.compare_v3(baseline_artifact=art_empty, current=current_reg, host=host(), profile_name="code-regression", current_detectors=detectors())
check(
    "matched-regression-dominates-unknown",
    cmp_reg["descriptor"]["verdict"] == "fail"
    and any(e["classification"] == "CODE-NET-NEW" and e["gates"] for e in cmp_reg["descriptor"]["entries"]),
)

# unmapped project: required contextDelta present
unmapped = make_current(occurrences=[m], rule_results=[rr(outcome="fail", findings=[m["findingId"]])], project="prj1-" + token("other"))
cmp_un = P.compare_v3(baseline_artifact=art_empty, current=unmapped, host=host(), profile_name="code-regression", current_detectors=detectors())
check("unmapped-has-contextDelta", "contextDelta" in cmp_un["descriptor"] and cmp_un["descriptor"]["comparisonPerformed"] is False)
check("unmapped-error-is-precondition", cmp_un.get("errorCode") == "REQUEST.PRECONDITION_FAILED")
must_valid("unmapped-comparison-schema", U + "comparison:2", {"comparisonResultId": cmp_un["comparisonResultId"], "descriptor": cmp_un["descriptor"]})

old = copy.deepcopy(art)
old["descriptor"]["schemaMajor"] = 1
del old["descriptor"]["unmatchedOccurrences"]
reject("old-baseline-major-refused-not-empty-coercion", lambda: P.verify_baseline_artifact_v3(old), "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "BASELINE.SCHEMA_MAJOR_UNSUPPORTED")

# ----------------------------------------------------------------------------- optional unknown non-gating
check(
    "optional-unknown-non-gating-current-pass",
    verdict(occurrences=[], rule_results=[rr(outcome="pass")], policy=POLICY_ADVISORY) == "pass",
)
cmp_opt = P.compare_v3(
    baseline_artifact=art_empty,
    current=make_current(occurrences=[], rule_results=[rr(outcome="pass")], policy=POLICY_ADVISORY),
    host=host(),
    profile_name="code-regression",
    current_detectors=detectors(),
)
check(
    "optional-unknown-no-gating-correspondence-deficiency",
    not any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_opt["descriptor"]["ruleDeficiencies"]),
)

zero_rules = [rr(outcome="indeterminate", enum=incomplete_enum())]
check("zero-finding-population-unknown-not-pass", verdict(occurrences=[], rule_results=zero_rules) == "indeterminate")
cmp_z = P.compare_v3(
    baseline_artifact=art_empty,
    current=make_current(occurrences=[], rule_results=zero_rules),
    host=host(),
    profile_name="code-regression",
    current_detectors=detectors(),
)
check("zero-result-population-unknown-preserved", cmp_z["descriptor"]["correspondenceCoverage"][0]["populationUnknown"] is True)

# ----------------------------------------------------------------------------- SARIF actual + intermediate surfaces
surfaces = P.project_finding_surfaces([a, b, u], [])
check("intermediate-surface-one-per-findingId", len(surfaces) == 3)
sarif = P.project_sarif([a, b, u], [], verdict="fail", parameter_records=None)
check("sarif-version-2-1-0", sarif["version"] == "2.1.0" and len(sarif["runs"][0]["results"]) == 3)
check("sarif-one-result-per-findingId", len({r["properties"]["findingId"] for r in sarif["runs"][0]["results"]}) == 3)
check(
    "sarif-partialFingerprints-only-matched",
    all(("partialFingerprints" in r) == (r["properties"]["correspondence"]["state"] == "matched") for r in sarif["runs"][0]["results"]),
)
check("sarif-keeps-message-params", any(r["message"]["properties"]["matchingFactCount"] == 3 for r in sarif["runs"][0]["results"]))
must_valid("sarif-log-schema", U + "sarif-adapter:2", sarif)

# ----------------------------------------------------------------------------- candidates grouped
cands = P.project_candidates(RUN, PRJ, [a, b, u], POLICY, [], {}, "2026-09-08", {"r": BINDING})
matched_c = [c for c in cands if c["fingerprint"] == a["finding"]["fingerprint"]]
un_c = [c for c in cands if c["fingerprint"] is None]
check("matched-two-configs-one-candidateId", len(matched_c) == 1 and len(matched_c[0]["findingIds"]) == 2)
check("matched-candidate-preserves-both-params", len({o["parameterDigest"] for o in matched_c[0]["occurrences"]}) == 2)
check("unmatched-candidate-by-findingId", len(un_c) == 1 and un_c[0]["findingIds"] == [u["findingId"]])
must_valid("candidate-matched-schema", U + "review:2#/$defs/Candidate", matched_c[0])
must_valid("candidate-unmatched-schema", U + "review:2#/$defs/Candidate", un_c[0])
disp = {matched_c[0]["candidateId"]: {"disposition": "reject", "suppressUntil": "2026-12-01", "receiptId": hid("receipt2", "r1")}}
cands2 = P.project_candidates(RUN, PRJ, [a, b, u], POLICY, [], disp, "2026-09-08", {"r": BINDING})
check("suppression-targets-logical-fingerprint-candidate", next(c for c in cands2 if c["fingerprint"] == a["finding"]["fingerprint"])["suppressed"] is True)
check("suppression-does-not-hide-unmatched", next(c for c in cands2 if c["fingerprint"] is None)["suppressed"] is False)

reject(
    "repair-unmatched-refuses",
    lambda: P.project_repair_targets(["finding-key2:" + "f" * 64], [u]),
    "REQUEST.PRECONDITION_FAILED",
    "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE",
)
ok_repair = P.project_repair_targets([a["finding"]["fingerprint"]], [a, b])
check("repair-multi-config-compatible-keeps-both-ids", len(ok_repair[a["finding"]["fingerprint"]]["findingIds"]) == 2)

term = P.serialization_overflow_termination()
check(
    "output-bound-existing-error",
    term["errorCode"] == "OUTPUT.SERIALIZATION_FAILED"
    and term["faultCause"] == "output-serialization"
    and term["domainDetail"]["code"] == "EVALUATION.OUTPUT_BOUND_EXCEEDED",
)
check("output-bound-detail-is-registered", "EVALUATION.OUTPUT_BOUND_EXCEEDED" in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])
check("schema-major-error-is-d9-errorcode", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED" in SCHEMAS[U + "common:3"]["$defs"]["D9ErrorCode"]["enum"])
check("schema-major-error-not-used-as-detail-member", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED" not in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])

passed = all(c["ok"] for c in CHECKS)
report = {
    "standing": "BOUNDED WORKFLOW PROJECTION ONLY. Isolated evaluator3 schemas + pure projection over admitted finding objects. Not native admission, not complete retained-Run replay, not public-registry integration. Passing these checks does not establish complete admission.",
    "passed": passed,
    "count": len(CHECKS),
    "failed": [c for c in CHECKS if not c["ok"]],
    "results": CHECKS,
}
Path("/tmp/opensip-design-corrections/grok-workflow-projection.v1/workflow-projection-report.v3.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": passed, "count": len(CHECKS), "failed": report["failed"]}, indent=2))
sys.exit(0 if passed else 1)
