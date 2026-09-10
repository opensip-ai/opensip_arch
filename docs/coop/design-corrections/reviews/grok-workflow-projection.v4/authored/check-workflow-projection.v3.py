"""Bounded evaluator3 workflow schema + projection checks. Not full Run replay.

Consumes admitted proof-shaped finding objects. Does not run native admission
or evaluator_replay_model.v3.derive/replay.

Run: /tmp/opensip-architecture-review-env/bin/python -I -B check-workflow-projection.v3.py
     [--output PATH]

Does not write historical workflow-projection-report.v1/v2/v3.json receipts.
Without --output, the JSON report is printed to stdout only.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
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
    except Exception as exc:
        return check(cid, False, type(exc).__name__ + ": " + str(exc).splitlines()[0][:200])
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


def rule_cov(gating=True, required="satisfied", rule_id="r"):
    return {
        "ruleId": rule_id,
        "requiredCoverage": required,
        "enabled": True,
        "gating": gating,
        "evidenceUse": [],
    }


def ctx(policy=None):
    pol = policy if policy is not None else POLICY
    return {
        "policyDigest": P.doc_digest(pol),
        "scopeDigest": P.doc_digest(SCOPE),
        "waiverSetDigest": P.doc_digest(WAIVERS),
        "detectorClosureIds": [DET],
        "evidenceAvailability": empty_evidence(),
    }


def host(**overrides):
    h = {
        "closures": {DET: {"bytes": "ok", "trust": "admitted", "protocolMajor": 1, "platform": "linux"}},
        "protocolMajors": [1],
        "platform": "linux",
        "pivotRunId": RUN,
        "recipeMajors": [2],
    }
    h.update(overrides)
    return h


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


def rr(*, outcome, enum=None, findings=None, deficiencies=None, rule_id="r"):
    return {
        "ruleId": rule_id,
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


def adopt(projected, run_id=RUN, policy=None, coverage=None, custody=None, analysis_spec=None):
    pol = policy if policy is not None else POLICY
    run = {"authority": "authoritative", "availability": "retained", "runId": run_id, "snapshotId": SNAP}
    return P.adopt_baseline_v3(
        run,
        PLAN,
        PRJ,
        pol,
        SCOPE,
        WAIVERS,
        coverage if coverage is not None else [rule_cov(gating=P.rule_gates(pol, "r"))],
        projected,
        detector_closure_entries(),
        pivot_entries(),
        ctx(pol),
        scope_spec() if analysis_spec is None else analysis_spec,
        custody if custody is not None else CUSTODY,
    )


def pivot_true(fps):
    return {fp: {"E0": False, "E1": True, "E2": True, "E3": True} for fp in fps}


def make_current(
    *,
    occurrences,
    rule_results,
    policy=None,
    waived=None,
    required=None,
    run_id=None,
    snapshot=None,
    project=None,
    execution=None,
    state="evaluated",
    pivots=None,
    bound=None,
    bindings=None,
):
    pol = policy if policy is not None else POLICY
    occs = occurrences
    fps = [o["finding"]["fingerprint"] for o in occs if o["finding"]["fingerprint"]]
    return {
        "runId": run_id or hid("run3", "cur"),
        "snapshotId": snapshot or hid("snapshot2", "cur"),
        "projectId": project if project is not None else PRJ,
        "policy": pol,
        "occurrences": occs,
        "ruleResults": rule_results,
        "waivedFindingIds": [] if waived is None else waived,
        "executionDeficiencies": [] if execution is None else execution,
        "evaluationState": state,
        "emissionBindings": bindings if bindings is not None else {"r": BINDING},
        "context": ctx(pol),
        "requiredCoverage": required if required is not None else {r["ruleId"]: "satisfied" for r in pol["rules"]},
        "boundPivots": [] if bound is None else bound,
        "pivotPresence": pivots if pivots is not None else pivot_true(fps),
    }


def verdict(**kwargs):
    pv = kwargs.pop("proof_verdict", None)
    cur = make_current(**kwargs)
    return P.current_run_verdict(
        policy=cur["policy"],
        occurrences=cur["occurrences"],
        waived_ids=cur["waivedFindingIds"],
        rule_results=cur["ruleResults"],
        execution_deficiencies=cur["executionDeficiencies"],
        evaluation_state=cur["evaluationState"],
        proof_verdict=pv,
    )


def cmp_obj(res):
    return {"comparisonResultId": res["comparisonResultId"], "descriptor": res["descriptor"]}


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
v1_invt = json.loads((WF / "command-inventory.schema.json").read_text())
check("v1-baseline-identity-major-was-1", v1_base["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-comparison-identity-major-was-1", v1_cmp["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-envelope-major-was-2", v1_env["properties"]["schemaMajor"]["const"] == 2)
check("v1-invocation-major-was-1", v1_inv["properties"]["schemaMajor"]["const"] == 1)
check("v1-query-major-was-1", v1_q["$defs"]["GraphQueryRequestV1"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-repair-plan-major-was-1", v1_rep["$defs"]["RepairPlanDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-inventory-major-was-1", v1_invt["properties"]["schemaMajor"]["const"] == 1)
check("baseline-schema-major-2", SCHEMAS[U + "baseline:2"]["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check("baseline-requires-unmatched", "unmatchedOccurrences" in SCHEMAS[U + "baseline:2"]["$defs"]["BaselineDescriptor"]["required"])
check("comparison-schema-major-2", SCHEMAS[U + "comparison:2"]["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check(
    "comparison-cause-correspondence",
    "correspondence-incomplete" in SCHEMAS[U + "comparison:2"]["$defs"]["RuleDeficiency"]["properties"]["cause"]["enum"],
)
check("envelope-major-3", SCHEMAS[U + "command-envelope:3"]["properties"]["schemaMajor"]["const"] == 3)
check("invocation-major-3", SCHEMAS[U + "invocation:3"]["properties"]["schemaMajor"]["const"] == 3)
check("new-baseline-major-bumped-for-unmatched-preimage", SCHEMAS[U + "baseline:2"]["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] != 1)
check("new-comparison-major-bumped-for-unmatched-preimage", SCHEMAS[U + "comparison:2"]["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] != 1)
check("new-repair-plan-major-bumped-for-run3", SCHEMAS[U + "repair:2"]["$defs"]["RepairPlanDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check("new-query-major-bumped-for-findingId", SCHEMAS[U + "graph-query:2"]["$defs"]["GraphQueryRequestV1"]["properties"]["schemaMajor"]["const"] == 2)
pins = SCHEMAS[U + "baseline:2"]["$defs"]["Custody"]["properties"]["retentionPins"]["items"]["pattern"]
check("retention-pins-run3-not-mixed-regex", pins.startswith("^(run3|closure2):") and "run[23]" not in pins)
check("unmatched-requires-side", "side" in SCHEMAS[U + "common:3"]["$defs"]["UnmatchedOccurrence"]["required"])
check("finding-surface-is-not-sarif", "not a SARIF" in SCHEMAS[U + "common:3"]["$defs"]["FindingSurface"]["description"])
check("sarif-adapter-major-2", SCHEMAS[U + "sarif-adapter:2"]["properties"]["version"]["const"] == "2.1.0")
must_invalid("run2-prefix-refused", U + "common:3#/$defs/RunId", "run2:" + "a" * 64)
must_valid("run3-prefix-admitted", U + "common:3#/$defs/RunId", "run3:" + "a" * 64)
must_invalid("finding2-prefix-refused", U + "common:3#/$defs/FindingId", "finding2:" + "a" * 64)

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
surf_bad = copy.deepcopy(surf_unmatched)
surf_bad["partialFingerprints"] = {"opensip/finding-key2": "finding-key2:" + "a" * 64}
must_invalid("unmatched-cannot-carry-partialFingerprints", U + "common:3#/$defs/FindingSurface", surf_bad)

# ----------------------------------------------------------------------------- two-config / package / baseline
a = occurrence("cfg-a", universe="one", facts=0)
b = occurrence("cfg-b", universe="two", facts=3)
check("two-config-same-logical-fingerprint", a["finding"]["fingerprint"] == b["finding"]["fingerprint"])
check("two-config-different-params", a["finding"]["parameterDigest"] != b["finding"]["parameterDigest"])
proj = P.project_baseline_entries([a, b], {"r": BINDING}, [])
check("two-config-one-baseline-entry", len(proj["entries"]) == 1 and len(proj["unmatchedOccurrences"]) == 0)
check("two-config-params-not-collapsed", len({a["finding"]["parameterDigest"], b["finding"]["parameterDigest"]}) == 2)
check("subjectId-opaque-not-three-coords", a["finding"]["subjectId"].startswith("subject3:") and "universe" not in a["finding"]["subjectId"])
pkg_a = occurrence("pkg-a", kind="package", name="dup", path="crates/a/Cargo.toml", universe="u", subject_id=hid("subject3", "pkg-a-opaque"))
pkg_b = occurrence("pkg-b", kind="package", name="dup", path="crates/b/Cargo.toml", universe="u", subject_id=hid("subject3", "pkg-b-opaque"))
check("package-same-name-different-manifest-paths", pkg_a["finding"]["subject"]["qualifiedName"] == "dup" and pkg_b["finding"]["subject"]["qualifiedName"] == "dup")
check("package-manifest-path-owns-fingerprint", pkg_a["finding"]["fingerprint"] != pkg_b["finding"]["fingerprint"])
proj_pkg = P.project_baseline_entries([pkg_a, pkg_b], {"r": BINDING}, [])
check("package-two-baseline-entries-by-path", len(proj_pkg["entries"]) == 2)
art = adopt(proj)
check("adopt-schema-major-2", art["descriptor"]["schemaMajor"] == 2)
check("adopt-run3", art["descriptor"]["runId"].startswith("run3:"))
check("adopt-uses-trusted-custody-timestamp", art["custody"]["exportedAtUtc"] == CUSTODY["exportedAtUtc"])
must_valid("baseline-artifact-schema", U + "baseline:2", art)
P.verify_baseline_artifact_v3(art)

c = occurrence("leg-a", universe="one")
d = occurrence("leg-b", universe="two", legacy="old-key")
reject("legacy-optional-presence-conflict", lambda: P.project_baseline_entries([c, d], {"r": BINDING}, []), "CONFIG.INVALID", "BASELINE.ENTRY_PROJECTION_CONFLICT")
lv1 = occurrence("lv1", universe="one", legacy="x")
lv2 = occurrence("lv2", universe="two", legacy="y")
reject("legacy-value-conflict", lambda: P.project_baseline_entries([lv1, lv2], {"r": BINDING}, []), "CONFIG.INVALID", "BASELINE.ENTRY_PROJECTION_CONFLICT")
lg1 = occurrence("lg1", universe="one", legacy="same")
lg2 = occurrence("lg2", universe="two", legacy="same")
proj_lg = P.project_baseline_entries([lg1, lg2], {"r": BINDING}, [])
check("legacy-agree-groups", len(proj_lg["entries"]) == 1 and proj_lg["entries"][0]["legacyFingerprint"] == "same")
pre = copy.deepcopy(a)
pre["findingId"] = hid("finding3", "pre")
pre["fingerprintDescriptor"] = fp_desc("src/other.ts", "src/other.ts", "file")
reject("preimage-conflict-input-refusal", lambda: P.project_baseline_entries([a, pre], {"r": BINDING}, []), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
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
reject(
    "adopt-requires-trusted-custody",
    lambda: P.adopt_baseline_v3(
        {"authority": "authoritative", "availability": "retained", "runId": RUN, "snapshotId": SNAP},
        PLAN, PRJ, POLICY, SCOPE, WAIVERS, [rule_cov()], proj,
        detector_closure_entries(), pivot_entries(), ctx(), scope_spec(), {},
    ),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)

# ----------------------------------------------------------------------------- gating from policy, not ruleResults
u = occurrence("un-1", unmatched=True, reason="signature-ambiguous")
proj_u = P.project_baseline_entries([u], {"r": BINDING}, [])
check("unmatched-not-in-entries", proj_u["entries"] == [] and len(proj_u["unmatchedOccurrences"]) == 1)
check("unmatched-fingerprint-is-null", u["finding"]["fingerprint"] is None)
check(
    "nongating-live-finding-does-not-fail",
    verdict(occurrences=[u], rule_results=[rr(outcome="pass")], policy=POLICY_ADVISORY) == "pass",
)
check(
    "advisory-outcome-fail-does-not-gate",
    verdict(occurrences=[u], rule_results=[rr(outcome="fail", findings=[u["findingId"]])], policy=POLICY_ADVISORY) == "pass",
)
check(
    "gating-live-unmatched-fails",
    verdict(occurrences=[u], rule_results=[rr(outcome="fail", findings=[u["findingId"]])], policy=POLICY) == "fail",
)
check(
    "gating-live-ignores-outcome-pass",
    verdict(occurrences=[u], rule_results=[rr(outcome="pass", findings=[u["findingId"]])], policy=POLICY) == "fail",
)
check("unmatched-current-fail", verdict(occurrences=[u], rule_results=[rr(outcome="fail", findings=[u["findingId"]])]) == "fail")
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
reject(
    "proof-verdict-inconsistent",
    lambda: P.current_run_verdict(
        policy=POLICY,
        occurrences=[u],
        waived_ids=[],
        rule_results=[rr(outcome="pass", findings=[u["findingId"]])],
        execution_deficiencies=[],
        evaluation_state="evaluated",
        proof_verdict="pass",
    ),
    "CONFIG.INVALID",
    "EVALUATION.PROOF_VERDICT_INCONSISTENT",
)
cov_adv = P.correspondence_coverage(POLICY_ADVISORY, [rr(outcome="fail", findings=[u["findingId"]])], [u])
check("correspondence-gating-not-from-outcome", cov_adv[0]["gating"] is False and cov_adv[0]["unmatchedCount"] == 1)

# ----------------------------------------------------------------------------- comparison: derive E4, baseline unmatched, profiles
art_u = adopt(proj_u)
current_u = make_current(occurrences=[u], rule_results=[rr(outcome="fail", findings=[u["findingId"]])])
cmp_u = P.compare_v3(baseline_artifact=art_u, current=current_u, host=host(), profile_name="code-regression", current_detectors=detectors())
check("unmatched-not-classified-as-net-new", all(e.get("classification") != "CODE-NET-NEW" for e in cmp_u["descriptor"]["entries"]))
check(
    "unmatched-audit-correspondence-incomplete",
    cmp_u["descriptor"]["verdict"] == "indeterminate"
    and any(d["cause"] == "correspondence-incomplete" for d in cmp_u["descriptor"]["ruleDeficiencies"]),
)
must_valid("comparison-artifact-schema", U + "comparison:2", cmp_obj(cmp_u))

current_w = make_current(occurrences=[u], rule_results=[rr(outcome="pass", findings=[u["findingId"]])], waived=[u["findingId"]])
cmp_w = P.compare_v3(baseline_artifact=art_u, current=current_w, host=host(), profile_name="code-regression", current_detectors=detectors())
check("path-waiver-audit-still-unknown", cmp_w["descriptor"]["verdict"] == "indeterminate" and any(x["waived"] for x in cmp_w["descriptor"]["unmatchedOccurrences"] if x["side"] == "current"))

bad_cur = dict(current_u)
del bad_cur["occurrences"]
reject(
    "compare-requires-occurrences",
    lambda: P.compare_v3(baseline_artifact=art_u, current=bad_cur, host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
bad_rr = dict(current_u)
del bad_rr["ruleResults"]
reject(
    "compare-requires-ruleResults",
    lambda: P.compare_v3(baseline_artifact=art_u, current=bad_rr, host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
heal = dict(current_u)
heal["ruleResults"] = []
reject(
    "empty-ruleResults-does-not-heal",
    lambda: P.compare_v3(baseline_artifact=art_u, current=heal, host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
reject(
    "compare-rejects-supplied-presence",
    lambda: P.compare_v3(baseline_artifact=art_u, current=dict(current_u, presence={}), host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
reject(
    "compare-rejects-supplied-entryRules",
    lambda: P.compare_v3(baseline_artifact=art_u, current=dict(current_u, entryRules={}), host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)

empty_current = make_current(occurrences=[], rule_results=[rr(outcome="pass")], snapshot=SNAP)
cmp_b = P.compare_v3(baseline_artifact=art_u, current=empty_current, host=host(), profile_name="code-regression", current_detectors=detectors())
check(
    "baseline-unmatched-survives-current-empty-baseline-or-current",
    any(d["cause"] == "correspondence-incomplete" and d["gating"] for d in cmp_b["descriptor"]["ruleDeficiencies"])
    and any(x["side"] == "baseline" for x in cmp_b["descriptor"]["unmatchedOccurrences"]),
)

POLICY_REMOVED = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [dict(RULE, ruleId="other")]}
empty_removed = make_current(
    occurrences=[],
    rule_results=[rr(outcome="pass", rule_id="other")],
    policy=POLICY_REMOVED,
    required={"other": "satisfied"},
    snapshot=SNAP,
    bindings={"other": dict(BINDING, ruleId="other")},
    bound=["E1"],
)
cmp_co = P.compare_v3(baseline_artifact=art_u, current=empty_removed, host=host(), profile_name="full-current", current_detectors=detectors())
check(
    "current-only-removed-rule-does-not-inherit-baseline-unmatched-gate",
    not any(d["cause"] == "correspondence-incomplete" and d["ruleId"] == "r" for d in cmp_co["descriptor"]["ruleDeficiencies"]),
)

art_adv = adopt(proj_u, policy=POLICY_ADVISORY, coverage=[rule_cov(gating=False)])
empty_adv = make_current(occurrences=[], rule_results=[rr(outcome="pass")], policy=POLICY_ADVISORY, snapshot=SNAP)
cmp_adv_b = P.compare_v3(baseline_artifact=art_adv, current=empty_adv, host=host(), profile_name="code-regression", current_detectors=detectors())
check(
    "nongating-baseline-unmatched-does-not-block",
    not any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_adv_b["descriptor"]["ruleDeficiencies"]),
)

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

mw = occurrence("waiver-new", universe="cur-w")
current_hidden = make_current(
    occurrences=[mw],
    rule_results=[rr(outcome="pass", findings=[mw["findingId"]])],
    waived=[mw["findingId"]],
)
cmp_hide = P.compare_v3(baseline_artifact=art_empty, current=current_hidden, host=host(), profile_name="code-regression", current_detectors=detectors())
check(
    "code-regression-new-waiver-does-not-suppress",
    any(e["classification"] == "CODE-NET-NEW" and e["gates"] for e in cmp_hide["descriptor"]["entries"]),
)
cmp_full_w = P.compare_v3(baseline_artifact=art_empty, current=current_hidden, host=host(), profile_name="full-current", current_detectors=detectors())
check(
    "full-current-new-waiver-suppresses-hidden-net-new",
    any(e["classification"] == "CODE-NET-NEW" and not e["gates"] for e in cmp_full_w["descriptor"]["entries"]),
)

other_prj = "prj1-" + token("other")
unmapped = make_current(occurrences=[m], rule_results=[rr(outcome="fail", findings=[m["findingId"]])], project=other_prj)
cmp_un = P.compare_v3(baseline_artifact=art_empty, current=unmapped, host=host(), profile_name="code-regression", current_detectors=detectors())
check("unmapped-has-contextDelta", "contextDelta" in cmp_un["descriptor"] and set(cmp_un["descriptor"]["contextDelta"]) == {"codeChanged", "detectorChanged", "policyChanged", "scopeChanged", "waiversChanged", "evidenceAvailabilityChanged"})
check("unmapped-comparison-not-performed", cmp_un["descriptor"]["comparisonPerformed"] is False and cmp_un["descriptor"]["verdict"] == "indeterminate")
check("unmapped-error-is-precondition", cmp_un.get("errorCode") == "REQUEST.PRECONDITION_FAILED")
check("unmapped-reason-project-unmapped", cmp_un["descriptor"]["wholeIndeterminateReason"] == "baseline-project-unmapped")
check("unmapped-empty-unmatched", cmp_un["descriptor"]["unmatchedOccurrences"] == [] and cmp_un["descriptor"]["correspondenceCoverage"] == [])
must_valid("unmapped-comparison-schema", U + "comparison:2", cmp_obj(cmp_un))

cmp_decl = P.compare_v3(baseline_artifact=art_empty, current=unmapped, host=host(), profile_name="code-regression", current_detectors=detectors(), accept_origins=(PRJ,))
check("declared-origin-performs-comparison", cmp_decl["descriptor"]["projectCorrespondence"] == "declared" and cmp_decl["descriptor"]["comparisonPerformed"] is True)
must_valid("declared-origin-schema", U + "comparison:2", cmp_obj(cmp_decl))

cmp_recipe = P.compare_v3(
    baseline_artifact=art_empty,
    current=make_current(occurrences=[], rule_results=[rr(outcome="pass")], snapshot=SNAP),
    host=host(recipeMajors=[99]),
    profile_name="code-regression",
    current_detectors=detectors(),
)
check("recipe-unsupported-whole-shape", cmp_recipe["descriptor"]["comparisonPerformed"] is False and "contextDelta" in cmp_recipe["descriptor"])
check("recipe-unsupported-reason", cmp_recipe["descriptor"]["wholeIndeterminateReason"] == "baseline-recipe-unsupported")
check("recipe-unsupported-error", cmp_recipe.get("errorCode") == "REQUEST.SCHEMA_MAJOR_UNSUPPORTED")
must_valid("recipe-unsupported-schema", U + "comparison:2", cmp_obj(cmp_recipe))

old = copy.deepcopy(art)
old["descriptor"]["schemaMajor"] = 1
del old["descriptor"]["unmatchedOccurrences"]
reject("old-baseline-major-refused-not-empty-coercion", lambda: P.verify_baseline_artifact_v3(old), "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "BASELINE.SCHEMA_MAJOR_UNSUPPORTED")
reject(
    "old-baseline-compare-refused-not-v1-semantics",
    lambda: P.compare_v3(baseline_artifact=old, current=empty_current, host=host(), profile_name="code-regression", current_detectors=detectors()),
    "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
    "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
)
old_cmp = copy.deepcopy(cmp_obj(cmp_u))
old_cmp["descriptor"]["schemaMajor"] = 1
must_invalid("old-comparison-major-unsupported", U + "comparison:2", old_cmp)

tamper = copy.deepcopy(art)
tamper["descriptor"]["contextDocuments"]["policy"] = POLICY_ADVISORY
tamper["baselineId"] = P.wid("baseline2", "workflow.baseline", tamper["descriptor"])
reject("verify-context-digest-binding", lambda: P.verify_baseline_artifact_v3(tamper), "REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING")

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
check("zero-unknown-gating-deficiency", any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_z["descriptor"]["ruleDeficiencies"]))
check("source-syntax-invalid-is-enumeration-unknown-not-native", verdict(occurrences=[], rule_results=zero_rules) == "indeterminate")
check("source-syntax-invalid-preserves-zero-population-unknown", cmp_z["descriptor"]["correspondenceCoverage"][0]["zeroFindings"] is True and cmp_z["descriptor"]["correspondenceCoverage"][0]["populationUnknown"] is True)

# ----------------------------------------------------------------------------- SARIF actual + intermediate surfaces
surfaces = P.project_finding_surfaces([a, b, u], [])
check("intermediate-surface-one-per-findingId", len(surfaces) == 3)
check("intermediate-surface-is-not-sarif-log", all("version" not in row and "runs" not in row for row in surfaces))
cited = occurrence("cited", universe="cite", facts=4)
cited["finding"]["evidenceRefs"] = [{"domain": "fact", "digest": token("factblob")}]
sarif = P.project_sarif([a, b, u, cited], [], verdict="fail")
check("sarif-version-2-1-0", sarif["version"] == "2.1.0" and len(sarif["runs"][0]["results"]) == 4)
check("sarif-one-result-per-findingId", len({r["properties"]["findingId"] for r in sarif["runs"][0]["results"]}) == 4)
check(
    "sarif-partialFingerprints-only-matched",
    all(("partialFingerprints" in r) == (r["properties"]["correspondence"]["state"] == "matched") for r in sarif["runs"][0]["results"]),
)
check("sarif-keeps-message-params", any(r["message"]["properties"]["matchingFactCount"] == 3 for r in sarif["runs"][0]["results"]))
check("sarif-keeps-citations", any(r["properties"]["citations"] == cited["finding"]["evidenceRefs"] for r in sarif["runs"][0]["results"]))
check("sarif-one-per-findingId", {r["properties"]["findingId"] for r in sarif["runs"][0]["results"]} == {a["findingId"], b["findingId"], u["findingId"], cited["findingId"]})
check("sarif-matched-have-partialFingerprints", all("partialFingerprints" in r for r in sarif["runs"][0]["results"] if r["properties"]["findingId"] in {a["findingId"], b["findingId"]}))
must_valid("sarif-log-schema", U + "sarif-adapter:2", sarif)
ids = {a["findingId"], b["findingId"], u["findingId"]}
surf_ids = {row["findingId"] for row in surfaces}
check("sarif-surface-cfg-a", a["findingId"] in surf_ids)
check("sarif-surface-cfg-b", b["findingId"] in surf_ids)
check("sarif-surface-unmatched", u["findingId"] in surf_ids)

# ----------------------------------------------------------------------------- candidates grouped
cands = P.project_candidates(RUN, PRJ, [a, b, u], POLICY, [], {}, "2026-09-08", {"r": BINDING})
matched_c = [c for c in cands if c["fingerprint"] == a["finding"]["fingerprint"]]
un_c = [c for c in cands if c["fingerprint"] is None]
check("matched-two-configs-one-candidateId", len(matched_c) == 1 and len(matched_c[0]["findingIds"]) == 2)
check("matched-candidate-preserves-both-params", len({o["parameterDigest"] for o in matched_c[0]["occurrences"]}) == 2)
check("unmatched-candidate-by-findingId", len(un_c) == 1 and un_c[0]["findingIds"] == [u["findingId"]])
check("unmatched-candidate-key-is-findingId", un_c[0]["candidateId"] == P.wid("candidate2", "workflow.candidate", {"projectId": PRJ, "kind": "finding", "key": u["findingId"]}))
check("matched-candidate-has-fingerprint", matched_c[0]["fingerprint"] == a["finding"]["fingerprint"])
must_valid("candidate-matched-schema", U + "review:2#/$defs/Candidate", matched_c[0])
must_valid("candidate-unmatched-schema", U + "review:2#/$defs/Candidate", un_c[0])
disp = {matched_c[0]["candidateId"]: {"disposition": "reject", "suppressUntil": "2026-12-01", "receiptId": hid("receipt2", "r1")}}
cands2 = P.project_candidates(RUN, PRJ, [a, b, u], POLICY, [], disp, "2026-09-08", {"r": BINDING})
check("suppression-targets-logical-fingerprint-candidate", next(c for c in cands2 if c["fingerprint"] == a["finding"]["fingerprint"])["suppressed"] is True)
check("fingerprint-suppression-does-not-hide-unmatched", next(c for c in cands2 if c["fingerprint"] is None)["suppressed"] is False)
check("suppression-does-not-hide-unmatched", next(c for c in cands2 if c["fingerprint"] is None)["suppressed"] is False)
disp_u = {un_c[0]["candidateId"]: {"disposition": "defer", "suppressUntil": "2026-12-01", "receiptId": hid("receipt2", "r2")}}
cands3 = P.project_candidates(RUN, PRJ, [a, b, u], POLICY, [], disp_u, "2026-09-08", {"r": BINDING})
check("unmatched-suppression-by-findingId-candidate", next(c for c in cands3 if c["fingerprint"] is None)["suppressed"] is True)
check("unmatched-suppression-does-not-hide-matched", next(c for c in cands3 if c["fingerprint"] == a["finding"]["fingerprint"])["suppressed"] is False)

q_u = P.query_finding([a, b, u], finding_id=u["findingId"])
q_fp = P.query_finding([a, b, u], fingerprint=a["finding"]["fingerprint"])
check("query-unmatched-by-findingId", [o["findingId"] for o in q_u] == [u["findingId"]])
check("query-fingerprint-matched-only-all-configs", {o["findingId"] for o in q_fp} == {a["findingId"], b["findingId"]})
check("findings-map-by-findingId", set(P.findings_map([a, b]).keys()) == {a["findingId"], b["findingId"]})
dup = copy.deepcopy(a)
reject("findings-map-duplicate-refused", lambda: P.findings_map([a, dup]), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")

reject(
    "repair-unmatched-refuses",
    lambda: P.project_repair_targets(["finding-key2:" + "f" * 64], [u]),
    "REQUEST.PRECONDITION_FAILED",
    "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE",
)
ok_repair = P.project_repair_targets([a["finding"]["fingerprint"]], [a, b])
check("repair-multi-config-compatible-keeps-both-ids", len(ok_repair[a["finding"]["fingerprint"]]["findingIds"]) == 2)
check("repair-does-not-collapse-params", len(ok_repair[a["finding"]["fingerprint"]]["parameterDigests"]) == 2)
amb = copy.deepcopy(a)
amb["findingId"] = hid("finding3", "amb")
amb["finding"] = dict(a["finding"], subject=dict(a["finding"]["subject"], logicalPath="src/b.ts"))
reject(
    "repair-multi-config-path-ambiguity",
    lambda: P.project_repair_targets([a["finding"]["fingerprint"]], [a, amb]),
    "REQUEST.PRECONDITION_FAILED",
    "REPAIR.TARGET_METADATA_AMBIGUOUS",
)

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
check("graph-query-findingId-param", "findingId" in SCHEMAS[U + "graph-query:2"]["$defs"]["Params"]["properties"])
check("graph-query-fingerprint-param", "fingerprint" in SCHEMAS[U + "graph-query:2"]["$defs"]["Params"]["properties"])

pairs = re.findall(r'Refusal\(\s*"([^"]+)"\s*,\s*"([^"]+)"', (HERE / "workflow_projection_model.v3.py").read_text())
check("config-invalid-not-used-as-detail", all(detail != "CONFIG.INVALID" for _, detail in pairs) and pairs)
check("request-schema-major-not-used-as-detail", all(detail != "REQUEST.SCHEMA_MAJOR_UNSUPPORTED" for _, detail in pairs))
check(
    "checker-default-is-stdout-not-historical-receipt",
    "--output" in (HERE / "check-workflow-projection.v3.py").read_text()
    and "stdout only" in (HERE / "check-workflow-projection.v3.py").read_text(),
)

passed = all(c["ok"] for c in CHECKS)
report = {
    "standing": "BOUNDED WORKFLOW PROJECTION ONLY. Isolated evaluator3 schemas + pure projection over admitted finding objects. Not native admission, not complete retained-Run replay, not public-registry integration. Passing these checks does not establish complete admission.",
    "passed": passed,
    "count": len(CHECKS),
    "failed": [c for c in CHECKS if not c["ok"]],
    "results": CHECKS,
}
parser = argparse.ArgumentParser(description="Bounded evaluator3 workflow projection checks")
parser.add_argument("--output", help="Write JSON report to PATH. Default: stdout only. Never writes historical v1/v2/v3 receipts.")
args = parser.parse_args()
payload = json.dumps(report, indent=2) + "\n"
if args.output:
    out = Path(args.output)
    if out.name in {"workflow-projection-report.v1.json", "workflow-projection-report.v2.json", "workflow-projection-report.v3.json"}:
        print("refusing historical receipt path: " + out.name, file=sys.stderr)
        sys.exit(2)
    out.write_text(payload)
    print(json.dumps({"passed": passed, "count": len(CHECKS), "failed": report["failed"], "output": str(out)}, indent=2))
else:
    sys.stdout.write(payload)
sys.exit(0 if passed else 1)
