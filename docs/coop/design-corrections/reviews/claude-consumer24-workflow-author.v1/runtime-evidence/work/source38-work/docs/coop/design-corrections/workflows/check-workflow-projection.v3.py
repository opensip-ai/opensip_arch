"""Bounded evaluator3 workflow schema + projection checks.

Most sections consume admitted proof-shaped finding objects only. Two sections do more and
say so: the candidate-graph section and the repair closed-world selection section both build
a graph, run evaluator_replay_model.v3.derive and close it through identity-model.v3.close_run,
which runs the complete evaluator3 semantic replay. The native records those sections read are
synthetic producer observations minted by the native owner's own helpers; no section qualifies
a native producer, a compiler, a provider or a repository read.

Run: /tmp/opensip-architecture-review-env/bin/python -I -B check-workflow-projection.v3.py
     [--output PATH]

Reports: stdout, or --output under grok-workflow-projection.v12/ only.
Does not write historical v1–v11 receipts.
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


def rule_cov(gating=True, required="satisfied", rule_id="r", knowledge="complete-hit-set"):
    return {
        "ruleId": rule_id,
        "requiredCoverage": required,
        "enabled": True,
        "gating": gating,
        "evidenceUse": [],
        "absenceKnowledge": knowledge,
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
    knowledge=True,
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
        # Synthetic admitted proof projection: complete roots for the (empty) selected subjects and a covering
        # extent. knowledge=False models a projection without admitted root proofs (no absence knowledge).
        **({"predicateProofs": [], "absenceExtent": {"examinedPaths": [], "scopeDocument": SCOPE, "foundationScope": {"pathPrefixes": ["."], "excludedPathPrefixes": []}, "extractionComplete": True}} if knowledge else {}),
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
check("schema-count", len(list(E3.glob("*.schema.json"))) == 11)
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
check("query-major-3-preserves-findingId-and-closes-graph-semantics", SCHEMAS[U + "graph-query:3"]["$defs"]["GraphQueryRequestV1"]["properties"]["schemaMajor"]["const"] == 3)
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
check("graph-query-findingId-param", "findingId" in SCHEMAS[U + "graph-query:3"]["$defs"]["Params"]["properties"])
check("graph-query-fingerprint-param", "fingerprint" in SCHEMAS[U + "graph-query:3"]["$defs"]["Params"]["properties"])

pairs = re.findall(r'Refusal\(\s*"([^"]+)"\s*,\s*"([^"]+)"', (HERE / "workflow_projection_model.v3.py").read_text())
check("config-invalid-not-used-as-detail", all(detail != "CONFIG.INVALID" for _, detail in pairs) and pairs)
check("request-schema-major-not-used-as-detail", all(detail != "REQUEST.SCHEMA_MAJOR_UNSUPPORTED" for _, detail in pairs))
check(
    "checker-default-is-stdout-not-historical-receipt",
    "--output" in (HERE / "check-workflow-projection.v3.py").read_text()
    and "stdout" in (HERE / "check-workflow-projection.v3.py").read_text()
    and "v5" in (HERE / "check-workflow-projection.v3.py").read_text(),
)

# ----------------------------------------------------------------------------- admitted-run adapter over identity-model.v3.close_run
FOUNDATION = HERE.parent / "foundation"
_rc_spec = importlib.util.spec_from_file_location("replay_check3", FOUNDATION / "check-replay.v3.py")
RC = importlib.util.module_from_spec(_rc_spec)
_rc_spec.loader.exec_module(RC)

CONTROL_COUNT = len(CHECKS)
check("v4-control-coverage-preserved", CONTROL_COUNT == 141)


def project_graph(**options):
    return P.project_admitted_run_v3(*RC.positive(**options))


two = project_graph(multiple_universes=True)
occ = two["occurrences"]
cands = two["candidates"]
sarif_results = two["sarif"]["runs"][0]["results"]
matched_cands = [c for c in cands if c["fingerprint"] is not None]
all_ids = [fid for c in cands for fid in c["findingIds"]]
check("admitted-twoU-close-run-run3", two["runId"].startswith("run3:"))
check("admitted-twoU-six-findings", len(occ) == 6)
check("admitted-twoU-six-subjectIds", len({o["finding"]["subjectId"] for o in occ}) == 6)
check("admitted-twoU-three-fingerprints", len({o["finding"]["fingerprint"] for o in occ}) == 3)
check("admitted-twoU-three-baseline-entries", len(two["baselineEntries"]) == 3 and two["unmatchedOccurrences"] == [])
check("admitted-twoU-three-logical-candidates", len(matched_cands) == 3)
check("admitted-twoU-all-six-findingIds-retained", len(all_ids) == 6 and set(all_ids) == {o["findingId"] for o in occ})
check(
    "admitted-twoU-group-keeps-both-configs",
    all(len(c["findingIds"]) == 2 and len(c["occurrences"]) == 2 for c in matched_cands),
)
check("admitted-twoU-six-sarif-results", two["sarif"]["version"] == "2.1.0" and len(sarif_results) == 6)
check("admitted-twoU-sarif-findingIds", {r["properties"]["findingId"] for r in sarif_results} == {o["findingId"] for o in occ})
check("admitted-twoU-sarif-message-params", all("matchingFactCount" in r["message"]["properties"] for r in sarif_results))
check("admitted-twoU-sarif-citations", all(isinstance(r["properties"]["citations"], list) for r in sarif_results))
check("admitted-twoU-verdict-fail-from-policy-and-proof", two["derivedVerdict"] == "fail" and two["proofVerdict"] == "fail")
check("admitted-twoU-no-unmatched", all(o["finding"]["correspondence"]["state"] == "matched" for o in occ))
check("admitted-twoU-adoption-not-performed-without-scope", two["scopeDocumentParameter"] == "absent")
check("admitted-twoU-adoption-scope-detail", "baselineAdoption" not in two)
must_valid("admitted-twoU-sarif-schema", U + "sarif-adapter:2", two["sarif"])
must_valid("admitted-twoU-candidate-schema", U + "review:2#/$defs/Candidate", matched_cands[0])

file_pos = project_graph()
check("admitted-file-three-findings", len(file_pos["occurrences"]) == 3)
check("admitted-file-three-fingerprints", len({o["finding"]["fingerprint"] for o in file_pos["occurrences"]}) == 3)
check("admitted-file-three-baseline-entries", len(file_pos["baselineEntries"]) == 3)
check("admitted-file-three-candidates", len(file_pos["candidates"]) == 3)
check("admitted-file-three-sarif", len(file_pos["sarif"]["runs"][0]["results"]) == 3)
check("admitted-file-verdict-fail", file_pos["derivedVerdict"] == "fail" and file_pos["proofVerdict"] == "fail")
check("admitted-file-adoption-not-performed", file_pos["scopeDocumentParameter"] == "absent")

nongate = project_graph(gate=False)
check("admitted-nongating-three-findings", len(nongate["occurrences"]) == 3)
check("admitted-nongating-verdict-pass", nongate["derivedVerdict"] == "pass" and nongate["proofVerdict"] == "pass")
check("admitted-nongating-live-does-not-fail", any(nongate["ruleResults"][0]["findingIds"]) and nongate["derivedVerdict"] == "pass")
check("admitted-nongating-adoption-not-performed", nongate["scopeDocumentParameter"] == "absent")

reject(
    "admitted-run-adopt-without-scope-document",
    lambda: P.adopt_baseline_v3(
        {"authority": "authoritative", "availability": "retained", "runId": two["runId"], "snapshotId": two["snapshotId"]},
        two["planId"],
        two["projectId"],
        two["policy"],
        SCOPE,
        WAIVERS,
        [rule_cov(gating=True, rule_id="file-observed")],
        {"entries": two["baselineEntries"], "unmatchedOccurrences": two["unmatchedOccurrences"]},
        detector_closure_entries(),
        pivot_entries(),
        ctx(two["policy"]),
        two["analysisSpec"],
        CUSTODY,
    ),
    "REQUEST.PRECONDITION_FAILED",
    "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
)
check("open_run_closure-not-called-from-adapter", "open_run_closure(" not in (HERE / "workflow_projection_model.v3.py").read_text())
check("adapter-invokes-close_run", "close_run(" in (HERE / "workflow_projection_model.v3.py").read_text())

V5_CONTROL = len(CHECKS)
check("v5-control-coverage-preserved", V5_CONTROL == 174)

# ----------------------------------------------------------------------------- v6: blocking law, execution comparison, admitted adoption, admitted compare, SARIF
nb = [{"source": "native", "cause": "cross-family-edge-not-owed", "subjectId": None, "predicateId": None, "inputRefs": [], "evidenceKind": None, "nativeCause": None, "universe": "native.semantic-universe.rust.v2"}]
check(
    "nonblocking-cross-family-does-not-make-unknown",
    verdict(occurrences=[], rule_results=[rr(outcome="pass", deficiencies=nb)]) == "pass",
)
check(
    "waived-live-plus-incomplete-stays-indeterminate",
    verdict(occurrences=[u], rule_results=[rr(outcome="indeterminate", findings=[u["findingId"]], enum=incomplete_enum())], waived=[u["findingId"]]) == "indeterminate",
)
check(
    "optional-unknown-nonblocking-pass",
    verdict(occurrences=[], rule_results=[rr(outcome="pass", deficiencies=nb)], policy=POLICY_ADVISORY) == "pass",
)

exec_d = [{"source": "execution", "cause": "work-budget-exhausted", "subjectId": None, "predicateId": None, "inputRefs": [], "evidenceKind": None, "nativeCause": None, "universe": None}]
cmp_ex = P.compare_v3(
    baseline_artifact=art_empty,
    current=make_current(occurrences=[], rule_results=[rr(outcome="indeterminate", enum=incomplete_enum())], execution=exec_d, state="budget-exhausted"),
    host=host(),
    profile_name="code-regression",
    current_detectors=detectors(),
)
check("compare-carries-execution-deficiencies", any(d["cause"] == "work-budget-exhausted" for d in cmp_ex["descriptor"]["currentExecutionDeficiencies"]))
check("compare-budget-exhausted-not-pass", cmp_ex["descriptor"]["verdict"] == "indeterminate" and cmp_ex["descriptor"]["currentEvaluationState"] == "budget-exhausted")
must_valid("compare-execution-schema", U + "comparison:2", cmp_obj(cmp_ex))

disabled_pol = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [dict(RULE, enabled=False)]}
cmp_dis = P.compare_v3(
    baseline_artifact=art_empty,
    current=make_current(
        occurrences=[],
        rule_results=[rr(outcome="disabled", enum={"state": "disabled", "inventoryRefs": [], "selectedSubjectIds": [], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []})],
        policy=disabled_pol,
        execution=exec_d,
        state="budget-exhausted",
    ),
    host=host(),
    profile_name="code-regression",
    current_detectors=detectors(),
)
check("compare-disabled-rules-execution-still-unknown", cmp_dis["descriptor"]["verdict"] == "indeterminate")

SCOPE_DOC = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["src/**"], "exclude": []}
scope_graph = RC.positive(scope_document=SCOPE_DOC)
scope_view = P.project_admitted_run_v3(*scope_graph)
check("scope-document-selected", scope_view["scopeDocumentParameter"] == "selected" and len(scope_view["occurrences"]) == 1)
check("scope-document-verdict-fail", scope_view["derivedVerdict"] == "fail" and scope_view["proofVerdict"] == "fail")
art_scope = P.adopt_admitted_baseline_v3(*scope_graph, CUSTODY)
P.verify_baseline_artifact_v3(art_scope)
must_valid("admitted-baseline-artifact-schema", U + "baseline:2", art_scope)
check("admitted-baseline-one-entry", len(art_scope["descriptor"]["entries"]) == 1)
pins = art_scope["custody"]["retentionPins"]
expect_pins = sorted({art_scope["descriptor"]["runId"]} | {p["closureId"] for p in art_scope["descriptor"]["pivotClosure"]})
check("admitted-baseline-exact-pins", pins == expect_pins)

wrong_entries = copy.deepcopy(art_scope)
wrong_entries["descriptor"]["entries"] = []
reject("reminted-wrong-entries-refused", lambda: P.verify_baseline_artifact_v3(wrong_entries), "CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT")
wrong_pins = copy.deepcopy(art_scope)
wrong_pins["custody"]["retentionPins"] = [art_scope["descriptor"]["runId"]]
reject("reminted-wrong-pins-refused", lambda: P.verify_baseline_artifact_v3(wrong_pins), "CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT")
wrong_scope = copy.deepcopy(art_scope)
wrong_scope["descriptor"]["contextDocuments"]["scope"] = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}
wrong_scope["baselineId"] = P.wid("baseline2", "workflow.baseline", wrong_scope["descriptor"])
reject("reminted-wrong-scope-digest-refused", lambda: P.verify_baseline_artifact_v3(wrong_scope), "REQUEST.PRECONDITION_FAILED", "BASELINE.CONTEXT_DOCUMENT_MISSING")
reject(
    "ordinary-graph-adopt-admitted-refuses-without-scope",
    lambda: P.adopt_admitted_baseline_v3(*RC.positive(), CUSTODY),
    "REQUEST.PRECONDITION_FAILED",
    "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
)


def host_from_graph(run, objects):
    closures = {}
    majors = set()
    platform = None
    for key, (dom, val) in objects.items():
        if dom != "closure":
            continue
        closures[key] = {"bytes": "ok", "trust": "admitted", "protocolMajor": val["protocolMajor"], "platform": val["platform"]}
        majors.add(val["protocolMajor"])
        if val["kind"] == "evaluator":
            platform = val["platform"]
        elif platform is None and val["kind"] == "detector" and val["platform"] != "any":
            platform = val["platform"]
    return {
        "closures": closures,
        "protocolMajors": sorted(majors),
        "platform": platform or "linux",
        "pivotRunId": run["runId"] if str(run.get("runId", "")).startswith("run3:") else objects,
        "recipeMajors": [2],
    }


srun, sobj, sblobs = scope_graph
# close_run identity is view runId; overlay run dict has no runId field
srun_host = dict(srun)
# identifier from view
host_s = host_from_graph({"runId": scope_view["runId"]}, sobj)
host_s["pivotRunId"] = scope_view["runId"]
dets_s = {row["contributionId"]: {"closureId": row["detectorClosure"], "semanticsMajor": row["semanticsMajor"], "compatibleWith": []} for row in scope_view["emission"]["rules"]}
cmp_same = P.compare_admitted_v3(
    baseline_artifact=art_scope,
    current_run=srun,
    current_objects=sobj,
    current_blobs=sblobs,
    host=host_s,
    profile_name="code-regression",
    current_detectors=dets_s,
)
check("admitted-compare-same-context-performed", cmp_same["descriptor"]["comparisonPerformed"] is True)
check("admitted-compare-same-context-pass", cmp_same["descriptor"]["verdict"] in ("pass", "fail") and cmp_same["descriptor"]["projectCorrespondence"] == "same-project")
check("admitted-compare-same-context-no-invented-maps", all(e["classification"] in ("UNCHANGED", "CODE-NET-NEW", "INDETERMINATE") for e in cmp_same["descriptor"]["entries"]))
must_valid("admitted-compare-same-context-schema", U + "comparison:2", cmp_obj(cmp_same))

gate_off = RC.positive(gate=False, scope_document=SCOPE_DOC)
cmp_piv = P.compare_admitted_v3(
    baseline_artifact=art_scope,
    current_run=gate_off[0],
    current_objects=gate_off[1],
    current_blobs=gate_off[2],
    host=host_s,
    profile_name="code-regression",
    current_detectors=dets_s,
)
check("admitted-compare-policy-change-pivot-unavailable", cmp_piv["descriptor"]["pivotsAvailable"]["E1"] == "unavailable" or cmp_piv["descriptor"]["comparisonPerformed"] is False or cmp_piv["descriptor"]["verdict"] == "indeterminate")
must_valid("admitted-compare-pivot-unavailable-schema", U + "comparison:2", cmp_obj(cmp_piv))

waived_sarif = P.project_sarif([u], [u["findingId"]], verdict="pass")
check("sarif-waived-has-suppression", any(r.get("suppressions") == [{"kind": "external", "status": "accepted"}] for r in waived_sarif["runs"][0]["results"]))
check("sarif-rule-messageStrings", any(row["messageCode"] in rule.get("messageStrings", {}) for rule in waived_sarif["runs"][0]["tool"]["driver"]["rules"] for row in [{"messageCode": "r"}]))
must_valid("sarif-waived-schema", U + "sarif-adapter:2", waived_sarif)
must_valid("step-termination-output-bound", U + "common:3#/$defs/StepTermination", P.serialization_overflow_termination())

# Exercise the shared termination vectors at the CURRENT output profile too.
# These are typed-carrier controls, not retained-Run admission: $RUN1 is the
# fixture's symbolic identifier, bound here to this checker's Run3-shaped RUN.
_termination_vectors = json.loads((HERE / "workflow-cases.v1.json").read_text())["terminationVectors"]
for _standing in ("accept", "reject"):
    for _index, _raw_termination in enumerate(_termination_vectors[_standing]):
        _termination = copy.deepcopy(_raw_termination)
        if _termination.get("runId") == "$RUN1":
            _termination["runId"] = RUN
        assert not any(isinstance(_value, str) and _value.startswith("$")
                       for _value in _termination.values()), "Unresolved termination fixture symbol"
        _assertion = must_valid if _standing == "accept" else must_invalid
        _assertion(f"current-termination-{_standing}-{_index}",
                   U + "common:3#/$defs/StepTermination", _termination)
_current_operational = next(
    branch["then"] for branch in SCHEMAS[U + "common:3"]["$defs"]["StepTermination"]["allOf"]
    if branch["if"].get("properties", {}).get("class", {}).get("const") == "operational-failed"
)
check("current-termination-fault-pairs-equal-host-map",
      {branch["properties"]["faultCause"]["const"]: branch["properties"]["errorCode"]["const"]
       for branch in _current_operational.get("anyOf", [])} == P.W.FAULT_TO_ERROR)


qreq = {
    "schemaFamily": "opensip.product.query",
    "schemaMajor": 3,
    "projectId": PRJ,
    "view": {"runId": RUN},
    "operation": "finding.show",
    "params": {"findingId": u["findingId"]},
    "completeness": "required",
    "page": {"size": 1},
}
must_valid("graph-query-request-schema", U + "graph-query:3#/$defs/GraphQueryRequestV1", qreq)
must_valid("candidate-from-admitted", U + "review:2#/$defs/Candidate", scope_view["candidates"][0])

def replay_positive_cases():
    """Same positive option tuples as check-replay.v3 main (not reminted mutants)."""
    yield "complete-file-positive", {}, "fail"
    for name, options, want, _count in [
        ("two-universes-six-full-findings", {"multiple_universes": True}, "fail", 6),
        ("file-none", {"atom_override": {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}}, "pass", 0),
        ("file-count-at-most-zero", {"atom_override": {"op": "count-at-most", "relation": "file", "minResolution": "enumerated", "filters": [], "n": 0}}, "pass", 0),
        ("file-all-covered", {"atom_override": {"op": "all-covered", "relation": "file", "minResolution": "enumerated", "filters": []}}, "fail", 3),
        ("nongating-live-findings", {"gate": False}, "pass", 3),
        ("disabled-rule", {"enabled": False}, "pass", 0),
        ("budget-exhausted", {"budget_limit": 1}, "indeterminate", 0),
        ("selected-scope-document", {"scope_document": SCOPE_DOC}, "fail", 1),
        ("complete-empty-path-selection", {"enumeration_filter": {"include": ["absent/**"]}}, "pass", 0),
        ("filter-whole-segment-glob", {"atom_override": {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "glob", "value": "src/**"}]}}, "fail", 1),
    ]:
        yield name, options, want
    window = {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"}
    runtime = {
        "kind": "runtime",
        "payload": {
            "payloadDomain": "workflow.import-payload.runtime.v1",
            "format": "v8-json",
            "observationWindow": window,
            "observedPopulation": "synthetic",
            "mappingGaps": [],
            "subjects": [{"path": "src/index.ts", "observability": "observed-hit", "hits": 2}],
        },
        "observation": {"window": window, "population": "synthetic"},
    }
    for name, op, partial, required, want, _count in [
        ("runtime-known-hit", "exists", False, True, "fail", 1),
        ("runtime-missing-subject-negative", "none", False, True, "indeterminate", 0),
        ("runtime-partial-known-hit", "exists", True, True, "fail", 1),
        ("runtime-partial-all-covered", "all-covered", True, True, "indeterminate", 0),
        ("runtime-optional-unknown", "none", False, False, "pass", 0),
    ]:
        item = copy.deepcopy(runtime)
        if partial:
            item["observation"].update(completeness="partial", omissions=["fixture omitted observations"])
        atom = {"op": op, "relation": "runtime-observation", "minResolution": "observed", "filters": [], "evidence": "runtime"}
        yield name, {"atom_override": atom, "import_specs": [item], "evidence_use": [{"kind": "runtime", "requirement": "required" if required else "optional"}]}, want
    history = {
        "kind": "history",
        "payload": {
            "payloadDomain": "workflow.import-payload.history.v1",
            "vcsSystem": "git",
            "revisionRange": {"from": None, "to": "a" * 40, "commitCount": 0, "truncated": False},
            "collectionScope": "all-paths",
            "subjects": [],
        },
        "observation": {"revisionRange": {"from": None, "to": "a" * 40}},
    }
    for name, scope, partial, want, _count in [
        ("history-complete-zero", "all-paths", False, "fail", 3),
        ("history-listed-zero", "listed-paths", False, "indeterminate", 0),
        ("history-partial-zero", "all-paths", True, "indeterminate", 0),
    ]:
        item = copy.deepcopy(history)
        item["payload"]["collectionScope"] = scope
        if partial:
            item["observation"].update(completeness="partial", omissions=["fixture truncated history"])
            item["payload"]["revisionRange"]["truncated"] = True
        atom = {"op": "none", "relation": "history-change", "minResolution": "observed", "filters": [], "evidence": "history"}
        yield name, {"atom_override": atom, "import_specs": [item], "evidence_use": [{"kind": "history", "requirement": "required"}]}, want
    partial_history = copy.deepcopy(history)
    partial_history["observation"].update(completeness="partial", omissions=["fixture partial history"])
    partial_history["payload"]["revisionRange"]["truncated"] = True
    for name, op, file_filter, want in [
        ("boolean-false-keeps-required-partial-diagnostics", "and", [{"field": "subject", "cmp": "glob", "value": "absent/**"}], "pass"),
        ("boolean-true-dominates-required-partial-diagnostics", "or", [], "fail"),
    ]:
        atom = {
            "op": op,
            "operands": [
                {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": file_filter},
                {"op": "none", "relation": "history-change", "minResolution": "observed", "filters": [], "evidence": "history"},
            ],
        }
        yield name, {"atom_override": atom, "import_specs": [partial_history], "evidence_use": [{"kind": "history", "requirement": "required"}]}, want
    argv = canonical.canonical(["fixture-test"])
    empty = b""
    selection = {"mode": "full", "completenessEstablished": True}
    test = {
        "kind": "test",
        "payload": {
            "payloadDomain": "workflow.import-payload.test.v1",
            "producer": "independent-prepared",
            "argvDigest": hashlib.sha256(argv).hexdigest(),
            "toolClosureId": None,
            "exitStatus": 0,
            "signal": None,
            "timedOut": False,
            "stdoutDigest": hashlib.sha256(empty).hexdigest(),
            "stderrDigest": hashlib.sha256(empty).hexdigest(),
            "stdoutBytes": 0,
            "stderrBytes": 0,
            "outputTruncated": False,
            "tests": [{"testId": "fixture-test-1", "subjectPath": "src/index.ts", "outcome": "pass"}],
            "selection": selection,
        },
        "observation": {"selection": selection},
        "extra_blobs": [argv, empty],
    }
    for name, rel, op, filters, partial, want, _count in [
        ("test-row-exact-location", "test-result", "exists", [], False, "fail", 1),
        ("test-process-coarse-scope", "test-execution", "exists", [{"field": "testResult", "cmp": "eq", "value": "passed"}], False, "fail", 3),
        ("test-partial-no-false-all-covered", "test-execution", "all-covered", [], True, "indeterminate", 0),
    ]:
        item = copy.deepcopy(test)
        if partial:
            item["observation"].update(completeness="partial", omissions=["fixture incomplete test selection"])
        atom = {"op": op, "relation": rel, "minResolution": "observed", "filters": filters, "evidence": "test"}
        yield name, {"atom_override": atom, "import_specs": [item], "evidence_use": [{"kind": "test", "requirement": "required"}]}, want
    for name, options, want, _count, _unmatched in [
        ("symbol-with-detector-projection", {"symbol_rows": [{"nativeSubjectId": "symbol:x"}]}, "fail", 1, 0),
        ("symbol-without-detector-projection", {"symbol_rows": [{"nativeSubjectId": "symbol:x", "projectionAvailable": False}]}, "fail", 1, 1),
        ("symbol-signature-collision", {"symbol_rows": [{"nativeSubjectId": "symbol:x1"}, {"nativeSubjectId": "symbol:x2"}]}, "fail", 2, 2),
        ("symbol-distinct-overload-signatures", {"symbol_rows": [{"nativeSubjectId": "symbol:x1"}, {"nativeSubjectId": "symbol:x2", "signatureTokens": ["function", "x", "(", "number", ")"]}]}, "fail", 2, 0),
        ("export-membership-unknown", {"symbol_rows": [{"nativeSubjectId": "symbol:x", "exported": "unknown"}], "select_exports": True}, "indeterminate", 0, 0),
        ("partial-symbol-known-finding", {"symbol_rows": [{"nativeSubjectId": "symbol:x"}], "symbol_state": "partial"}, "fail", 1, 1),
        ("disabled-required-symbol-partial", {"symbol_rows": [{"nativeSubjectId": "symbol:x"}], "symbol_state": "partial", "enabled": False}, "indeterminate", 0, 0),
    ]:
        yield name, options, want


mismatch = []
replay_names = []
for name, options, want in replay_positive_cases():
    replay_names.append(name)
    projected = P.project_admitted_run_v3(*RC.positive(**options))
    if projected["derivedVerdict"] != want or projected["proofVerdict"] != want:
        mismatch.append((name, projected["derivedVerdict"], projected["proofVerdict"], want))
    check("replay-verdict-" + name, projected["derivedVerdict"] == want and projected["proofVerdict"] == want, str((projected["derivedVerdict"], want)))
check("replay-case-verdicts-aligned", mismatch == [])
check("replay-loop-covers-file-runtime-history-test-symbol", set(replay_names) >= {"complete-file-positive", "runtime-known-hit", "history-complete-zero", "test-row-exact-location", "symbol-with-detector-projection"})

V6_CONTROL = len(CHECKS)
check("v6-control-coverage-preserved", V6_CONTROL >= 224)

# v7: mixed-boolean, required evidence coverage, bound E1 pivot, SARIF colon, detector override
mixed_atom = {
    "op": "and",
    "operands": [
        {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
    ],
}
try:
    mixed = P.project_admitted_run_v3(*RC.positive(atom_override=mixed_atom))
    check("mixed-boolean-and-supported", True)
    check("mixed-boolean-determinate-false-can-pass", mixed["derivedVerdict"] == mixed["proofVerdict"])
except Exception as exc:
    check("mixed-boolean-and-supported", False, type(exc).__name__ + ": " + str(exc).splitlines()[0][:200])
    check("mixed-boolean-determinate-false-can-pass", False, "fixture/atom_override and-operands not admitted")

none_scope = RC.positive(
    atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
    scope_document=SCOPE_DOC,
)
_rt_partial = {
    "kind": "runtime",
    "payload": {
        "payloadDomain": "workflow.import-payload.runtime.v1",
        "format": "v8-json",
        "observationWindow": {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"},
        "observedPopulation": "synthetic",
        "mappingGaps": [],
        "subjects": [{"path": "src/index.ts", "observability": "observed-hit", "hits": 2}],
    },
    "observation": {
        "window": {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"},
        "population": "synthetic",
        "completeness": "partial",
        "omissions": ["fixture omitted observations"],
    },
}
rt_unknown = RC.positive(
    atom_override={"op": "all-covered", "relation": "runtime-observation", "minResolution": "observed", "filters": [], "evidence": "runtime"},
    import_specs=[_rt_partial],
    evidence_use=[{"kind": "runtime", "requirement": "required"}],
    scope_document=SCOPE_DOC,
)
art_none = P.adopt_admitted_baseline_v3(*none_scope, CUSTODY)
nv = P.project_admitted_run_v3(*none_scope)
uv = P.project_admitted_run_v3(*rt_unknown)
check(
    "required-import-unknown-not-inventory-satisfied",
    uv["ruleResults"][0]["enumeration"]["state"] == "complete"
    and P.required_coverage_from_rule_result(uv["policy"]["rules"][0], uv["ruleResults"][0]) == "unknown",
)
host_n = host_from_graph({"runId": nv["runId"]}, none_scope[1])
host_n["pivotRunId"] = nv["runId"]
cmp_req = P.compare_admitted_v3(
    baseline_artifact=art_none,
    current_run=rt_unknown[0],
    current_objects=rt_unknown[1],
    current_blobs=rt_unknown[2],
    host=host_n,
    profile_name="code-regression",
)
check("complete-inventory-required-import-unknown-comparison-indeterminate", cmp_req["descriptor"]["verdict"] == "indeterminate")
check(
    "execution-deficiency-keeps-inputRefs-nativeCause",
    all("inputRefs" in d and "nativeCause" in d and "predicateId" in d for d in cmp_ex["descriptor"]["currentExecutionDeficiencies"]),
)

colon_occ = occurrence("colon", path="src/foo:bar.ts", name="src/foo:bar.ts")
space_occ = occurrence("space", path="src/a b.ts", name="src/a b.ts")
sarif_enc = P.project_sarif([colon_occ, space_occ], [], verdict="fail")
uris = [r["locations"][0]["physicalLocation"]["artifactLocation"]["uri"] for r in sarif_enc["runs"][0]["results"]]
check("sarif-colon-not-scheme", all(":" not in u.split("/")[0] or "%3A" in u or "%3a" in u for u in uris) and any("%3A" in u or "%3a" in u for u in uris))
check("sarif-space-percent-encoded", any("%20" in u for u in uris))
must_valid("sarif-encoded-uri-schema", U + "sarif-adapter:2", sarif_enc)
check("detail-input-refused-retained", "EVALUATION.INPUT_REFUSED" in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])
check("detail-selection-limit-retained", "EVALUATION.SELECTION_LIMIT" in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])
check("detail-preimage-mismatch-retained", "REPAIR.TARGET_PREIMAGE_MISMATCH" in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])

reject(
    "current-detectors-compatibleWith-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_scope,
        current_run=srun,
        current_objects=sobj,
        current_blobs=sblobs,
        host=host_s,
        profile_name="code-regression",
        current_detectors={k: dict(v, compatibleWith=["closure2:" + "a" * 64]) for k, v in dets_s.items()},
    ),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
_noscope = RC.positive()
reject(
    "compare-admitted-without-scope-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_scope,
        current_run=_noscope[0],
        current_objects=_noscope[1],
        current_blobs=_noscope[2],
        host=host_s,
        profile_name="code-regression",
    ),
    "REQUEST.PRECONDITION_FAILED",
    "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
)

base_e1 = RC.positive(scope_document=SCOPE_DOC, gate=True)
cur_e1 = RC.positive(scope_document=SCOPE_DOC, gate=False)
art_e1 = P.adopt_admitted_baseline_v3(*base_e1, CUSTODY)
host_e = host_from_graph({"runId": art_e1["descriptor"]["runId"]}, base_e1[1])
host_e["pivotRunId"] = art_e1["descriptor"]["runId"]
cmp_e1 = P.compare_admitted_v3(
    baseline_artifact=art_e1,
    current_run=cur_e1[0],
    current_objects=cur_e1[1],
    current_blobs=cur_e1[2],
    host=host_e,
    profile_name="code-regression",
    pivot_runs={"E1": base_e1},
)
check("bound-e1-same-snapshot-available", cmp_e1["descriptor"]["pivotsAvailable"]["E1"] == "available" and cmp_e1["descriptor"]["comparisonPerformed"] is True)
must_valid("bound-e1-schema", U + "comparison:2", cmp_obj(cmp_e1))
reject(
    "wrong-context-e1-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_e1,
        current_run=cur_e1[0],
        current_objects=cur_e1[1],
        current_blobs=cur_e1[2],
        host=host_e,
        profile_name="code-regression",
        pivot_runs={"E1": cur_e1},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)

check("portable-any-rewritten-in-host-adapter", "def _host_portable_platforms" in (HERE / "workflow_projection_model.v3.py").read_text() and "provider" in P.PIVOT_KINDS)

V7_CONTROL = len(CHECKS)
check("v7-control-coverage-preserved", V7_CONTROL >= 252)

# ----------------------------------------------------------------------------- v8: exact detector map, presence law, E2/E3, envelope, Boolean coverage
check("detail-required-output-omitted-retained", "EVALUATION.REQUIRED_OUTPUT_OMITTED" in SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])
iso_detail_desc = SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["description"]
check(
    "isolated-additions-prose-shared-input-refused-selection-limit-omitted",
    "EVALUATION.INPUT_REFUSED" in iso_detail_desc
    and "EVALUATION.SELECTION_LIMIT" in iso_detail_desc
    and "EVALUATION.REQUIRED_OUTPUT_OMITTED" in iso_detail_desc
    and "Do not fork a second registration" in iso_detail_desc,
)

extra_map = {"fixture": {"closureId": DET, "semanticsMajor": 2}, "extra-detector": {"closureId": "closure2:" + "b" * 64, "semanticsMajor": 2}}
missing_map = {}
major_map = {"fixture": {"closureId": DET, "semanticsMajor": 3}}
base_map = detector_closure_entries()
reject("e0-extra-detector-id-refused", lambda: P.require_exact_detector_map(extra_map, base_map, "E0"), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
reject("e0-missing-detector-id-refused", lambda: P.require_exact_detector_map(missing_map, base_map, "E0"), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
reject("e0-semantics-major-mismatch-refused", lambda: P.require_exact_detector_map(major_map, base_map, "E0"), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
P.require_exact_detector_map({"fixture": {"closureId": DET, "semanticsMajor": 2}}, base_map, "E0")
check("e0-exact-identity-major-map-admitted", True)

none_e0, none_e1, none_e2, none_e3 = P._presence_from_equalities(
    True,
    {"detectorChanged": True, "policyChanged": True, "scopeChanged": True, "waiversChanged": True},
    {},
)
check("missing-pivot-presence-is-null-not-false", none_e0 is None and none_e1 is None and none_e2 is None and none_e3 is None)

dets_major = {"fixture": {"closureId": DET, "semanticsMajor": 3, "compatibleWith": []}}
fp_m = m["finding"]["fingerprint"]
cur_det = make_current(
    occurrences=[m],
    rule_results=[rr(outcome="fail", findings=[m["findingId"]])],
    pivots={fp_m: {"E0": False, "E1": True, "E2": True, "E3": True}},
)
cmp_det = P.compare_v3(
    baseline_artifact=art_empty,
    current=cur_det,
    host=host(),
    profile_name="code-regression",
    current_detectors=dets_major,
)
check("detector-identity-major-map-marks-detectorChanged", cmp_det["descriptor"]["contextDelta"]["detectorChanged"] is True)
check(
    "detector-change-does-not-copy-E1-to-E0",
    any(e["presence"]["E0"] is False and e["presence"]["E1"] is True for e in cmp_det["descriptor"]["entries"]),
)
check(
    "detector-change-is-detection-delta-not-code-net-new",
    any(e["classification"] == "DETECTION-DELTA" for e in cmp_det["descriptor"]["entries"])
    and not any(e["classification"] == "CODE-NET-NEW" for e in cmp_det["descriptor"]["entries"]),
)
must_valid("detector-change-comparison-schema", U + "comparison:2", cmp_obj(cmp_det))

# extra detector on a reminted baseline must not join E0 as a subset
art_extra = copy.deepcopy(art_scope)
art_extra["descriptor"]["detectorClosure"] = list(art_extra["descriptor"]["detectorClosure"]) + [
    {
        "detectorId": "extra-detector",
        "closureId": "closure2:" + "b" * 64,
        "semanticsMajor": 2,
        "semanticVersion": "1.0.0",
        "contributionId": "extra-detector",
        "manifestDigest": "b" * 64,
    }
]
art_extra["baselineId"] = P.wid("baseline2", "workflow.baseline", art_extra["descriptor"])
try:
    P.verify_baseline_artifact_v3(art_extra)
    check("m4-extra-noncontributing-detector-refused-at-baseline-admission", False, "admitted")
except P.Refusal as _extra_exc:
    check(
        "m4-extra-noncontributing-detector-refused-at-baseline-admission",
        _extra_exc.error_code == "CONFIG.INVALID" and _extra_exc.detail == "EVALUATION.FINDING_JOIN_REFUSED"
        and "embedded policy rule contributions" in str(_extra_exc.remedy),
        repr((_extra_exc.error_code, _extra_exc.detail, _extra_exc.remedy)),
    )
reject(
    "bound-e0-extra-detector-on-baseline-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_extra,
        current_run=srun,
        current_objects=sobj,
        current_blobs=sblobs,
        host=host_s,
        profile_name="code-regression",
        pivot_runs={"E0": scope_graph},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)

SCOPE_WIDE = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}
base_e2 = RC.positive(scope_document=SCOPE_DOC)
cur_e2 = RC.positive(scope_document=SCOPE_WIDE)
check("e2-graphs-share-snapshot", base_e2[0]["snapshotId"] == cur_e2[0]["snapshotId"])
check("e2-graphs-share-policy", base_e2[1][base_e2[0]["planId"]][1]["policyDigest"] == cur_e2[1][cur_e2[0]["planId"]][1]["policyDigest"])
art_e2 = P.adopt_admitted_baseline_v3(*base_e2, CUSTODY)
host_e2 = host_from_graph({"runId": art_e2["descriptor"]["runId"]}, base_e2[1])
host_e2["pivotRunId"] = art_e2["descriptor"]["runId"]
cmp_e2 = P.compare_admitted_v3(
    baseline_artifact=art_e2,
    current_run=cur_e2[0],
    current_objects=cur_e2[1],
    current_blobs=cur_e2[2],
    host=host_e2,
    profile_name="code-regression",
    pivot_runs={"E2": base_e2},
)
check(
    "bound-e2-scope-axis-available",
    cmp_e2["descriptor"]["pivotsAvailable"]["E2"] == "available"
    and cmp_e2["descriptor"]["contextDelta"]["scopeChanged"] is True
    and cmp_e2["descriptor"]["contextDelta"]["policyChanged"] is False
    and cmp_e2["descriptor"]["comparisonPerformed"] is True,
)
must_valid("bound-e2-schema", U + "comparison:2", cmp_obj(cmp_e2))
reject(
    "wrong-current-as-e2-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_e2,
        current_run=cur_e2[0],
        current_objects=cur_e2[1],
        current_blobs=cur_e2[2],
        host=host_e2,
        profile_name="code-regression",
        pivot_runs={"E2": cur_e2},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)
reject(
    "wrong-e1-policy-graph-as-e2-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_e2,
        current_run=cur_e2[0],
        current_objects=cur_e2[1],
        current_blobs=cur_e2[2],
        host=host_e2,
        profile_name="code-regression",
        pivot_runs={"E2": cur_e1},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)

WAIVER_ROWS = [
    {
        "waiverId": "fixture-waiver-src-index",
        "target": {"ruleId": "file-observed", "subjectPath": "src/index.ts"},
        "reason": "v8 waiver pivot control",
        "expires": None,
    }
]
base_e3 = RC.positive(scope_document=SCOPE_DOC)
cur_e3 = RC.positive(scope_document=SCOPE_DOC, waiver_rows=WAIVER_ROWS)
check("e3-graphs-share-snapshot", base_e3[0]["snapshotId"] == cur_e3[0]["snapshotId"])
check("e3-current-has-waived-findings", len(P.project_admitted_run_v3(*cur_e3)["waivedFindingIds"]) > 0)
art_e3 = P.adopt_admitted_baseline_v3(*base_e3, CUSTODY)
host_e3 = host_from_graph({"runId": art_e3["descriptor"]["runId"]}, base_e3[1])
host_e3["pivotRunId"] = art_e3["descriptor"]["runId"]
cmp_e3 = P.compare_admitted_v3(
    baseline_artifact=art_e3,
    current_run=cur_e3[0],
    current_objects=cur_e3[1],
    current_blobs=cur_e3[2],
    host=host_e3,
    profile_name="code-regression",
    pivot_runs={"E3": base_e3},
)
check(
    "bound-e3-waiver-axis-available",
    cmp_e3["descriptor"]["pivotsAvailable"]["E3"] == "available"
    and cmp_e3["descriptor"]["contextDelta"]["waiversChanged"] is True
    and cmp_e3["descriptor"]["contextDelta"]["scopeChanged"] is False
    and cmp_e3["descriptor"]["comparisonPerformed"] is True,
)
check(
    "waiver-pivot-keeps-matched-presence",
    any(e["presence"]["E4"] is True and e["presence"]["waivedC"] is True for e in cmp_e3["descriptor"]["entries"]),
)
must_valid("bound-e3-schema", U + "comparison:2", cmp_obj(cmp_e3))
reject(
    "wrong-current-as-e3-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_e3,
        current_run=cur_e3[0],
        current_objects=cur_e3[1],
        current_blobs=cur_e3[2],
        host=host_e3,
        profile_name="code-regression",
        pivot_runs={"E3": cur_e3},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)
reject(
    "wrong-e2-scope-graph-as-e3-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_e3,
        current_run=cur_e3[0],
        current_objects=cur_e3[1],
        current_blobs=cur_e3[2],
        host=host_e3,
        profile_name="code-regression",
        pivot_runs={"E3": cur_e2},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)

# selected-view context: ambient unselected facts must not alter relations
scope_view_ctx = P.project_admitted_run_v3(*scope_graph)
ambient_objects = copy.deepcopy(scope_view_ctx["objects"])
ambient_objects["fact2:" + "c" * 64] = (
    "fact",
    {"relation": "ambient-unselected-relation", "schemaVersion": 2},
)
dets_ctx, _ = P._pivot_and_detector_from_plan(scope_view_ctx["plan"], scope_view_ctx["objects"], scope_view_ctx["emission"])
ctx_sel = P._context_from_admitted(
    scope_view_ctx["plan"],
    ambient_objects,
    scope_view_ctx["blobs"],
    scope_view_ctx["policy"],
    scope_view_ctx["scopeDocument"],
    scope_view_ctx["waivers"],
    dets_ctx,
    scope_view_ctx["evaluationInputRefs"],
)
check("context-relations-ignore-unselected-objects", "ambient-unselected-relation" not in ctx_sel["evidenceAvailability"]["relations"])
check("context-relations-from-selected-views", "file" in ctx_sel["evidenceAvailability"]["relations"])

HISTORY_PARTIAL = {
    "kind": "history",
    "payload": {
        "payloadDomain": "workflow.import-payload.history.v1",
        "vcsSystem": "git",
        "revisionRange": {"from": None, "to": "a" * 40, "commitCount": 0, "truncated": True},
        "collectionScope": "all-paths",
        "subjects": [],
    },
    "observation": {"revisionRange": {"from": None, "to": "a" * 40}, "completeness": "partial", "omissions": ["fixture partial history"]},
}
bool_false_graph = RC.positive(
    atom_override={
        "op": "and",
        "operands": [
            {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "glob", "value": "absent/**"}]},
            {"op": "none", "relation": "history-change", "minResolution": "observed", "filters": [], "evidence": "history"},
        ],
    },
    import_specs=[copy.deepcopy(HISTORY_PARTIAL)],
    evidence_use=[{"kind": "history", "requirement": "required"}],
    scope_document=SCOPE_DOC,
)
bool_true_graph = RC.positive(
    atom_override={
        "op": "or",
        "operands": [
            {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"op": "none", "relation": "history-change", "minResolution": "observed", "filters": [], "evidence": "history"},
        ],
    },
    import_specs=[copy.deepcopy(HISTORY_PARTIAL)],
    evidence_use=[{"kind": "history", "requirement": "required"}],
    scope_document=SCOPE_DOC,
)
bool_false = P.project_admitted_run_v3(*bool_false_graph)
bool_true = P.project_admitted_run_v3(*bool_true_graph)
check(
    "boolean-and-false-retains-deficiencies-but-passes",
    bool_false["derivedVerdict"] == "pass"
    and bool_false["proofVerdict"] == "pass"
    and bool_false["ruleResults"][0]["deficiencies"],
)
check(
    "boolean-or-true-retains-deficiencies-but-fails",
    bool_true["derivedVerdict"] == "fail"
    and bool_true["proofVerdict"] == "fail"
    and bool_true["ruleResults"][0]["deficiencies"],
)
check(
    "boolean-and-false-required-coverage-satisfied",
    P.required_coverage_from_rule_result(bool_false["policy"]["rules"][0], bool_false["ruleResults"][0]) == "satisfied",
)
check(
    "boolean-or-true-required-coverage-satisfied",
    P.required_coverage_from_rule_result(bool_true["policy"]["rules"][0], bool_true["ruleResults"][0]) == "satisfied",
)
art_bool = P.adopt_admitted_baseline_v3(*bool_false_graph, CUSTODY)
host_bool = host_from_graph({"runId": art_bool["descriptor"]["runId"]}, bool_false_graph[1])
host_bool["pivotRunId"] = art_bool["descriptor"]["runId"]
cmp_bool = P.compare_admitted_v3(
    baseline_artifact=art_bool,
    current_run=bool_false_graph[0],
    current_objects=bool_false_graph[1],
    current_blobs=bool_false_graph[2],
    host=host_bool,
    profile_name="code-regression",
)
check(
    "boolean-and-false-comparison-not-coverage-indeterminate",
    cmp_bool["descriptor"]["verdict"] != "indeterminate"
    and not any(d["cause"] == "required-coverage-unknown" for d in cmp_bool["descriptor"]["ruleDeficiencies"]),
)

fail_term = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}
fail_env = {
    "schemaFamily": "opensip.product.envelope",
    "schemaMajor": 3,
    "kind": "failure",
    "requestId": "req1_" + "a" * 32,
    "termination": fail_term,
    "exitCode": 2,
    "errors": [{"code": "EVALUATION.INPUT_REFUSED", "remedy": "failure envelopes carry errors and never a Run"}],
}
must_valid("failure-envelope-without-run", U + "command-envelope:3", fail_env)
valid_run = {
    "kind": "analysis",
    "authority": "authoritative",
    "runId": RUN,
    "planId": PLAN,
    "verdict": "fail",
    "requiredCoverage": "satisfied",
    "durability": "committed",
    "deficiency": "none",
    "secondaryDeficiencies": [],
}
fail_with_run = dict(fail_env, run=valid_run)
must_invalid("failure-envelope-valid-run-refused", U + "command-envelope:3", fail_with_run)
must_valid("valid-run-body-is-analysis-result", U + "invocation:3#/$defs/AnalysisResult", valid_run)

# host any-platform rewrite is comparison metadata only
det_key = next(k for k, (dom, val) in sobj.items() if dom == "closure" and val.get("kind") == "detector")
plat_before = sobj[det_key][1]["platform"]
_ = P.compare_admitted_v3(
    baseline_artifact=art_scope,
    current_run=srun,
    current_objects=sobj,
    current_blobs=sblobs,
    host=host_s,
    profile_name="code-regression",
)
check("host-any-does-not-mutate-closure-descriptor", sobj[det_key][1]["platform"] == plat_before == "any")
src_model = (HERE / "workflow_projection_model.v3.py").read_text()
check(
    "host-any-adapter-is-host-deepcopy-only",
    "Rewrite host comparison metadata only" in src_model and "manifestDigest" in src_model and "compatibleWith" in src_model,
)

V8_CONTROL = len(CHECKS)
check("v8-control-coverage-preserved", V8_CONTROL >= 292)

# ----------------------------------------------------------------------------- v9: per-fp absence knowledge, pivot-only fps, declared-compatible standing
clar = Path("/tmp/opensip-design-corrections/grok-workflow-projection.v8/root-clarification.txt")
check(
    "root-clarification-waived-matched-presence-is-honest-law",
    clar.is_file()
    and "Do NOT delete waived findings" in clar.read_text()
    and "E4 / waivedC / entryRules from admitted occurrences only" in (HERE / "workflow_projection_model.v3.py").read_text()
    and "ANY matched occurrence is present, including waived" in (HERE / "workflow_projection_model.v3.py").read_text(),
)

none_view = P.project_admitted_run_v3(
    *RC.positive(atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}, scope_document=SCOPE_DOC)
)
check("file-none-gating-pass-can-prove-absence", P.rule_can_prove_absence(none_view, none_view["policy"]["rules"][0]["ruleId"]) is True)

_rt_partial_opt = {
    "kind": "runtime",
    "payload": {
        "payloadDomain": "workflow.import-payload.runtime.v1",
        "format": "v8-json",
        "observationWindow": {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"},
        "observedPopulation": "synthetic",
        "mappingGaps": [],
        "subjects": [],
    },
    "observation": {
        "window": {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"},
        "population": "synthetic",
        "completeness": "partial",
        "omissions": ["fixture omitted observations"],
    },
}
opt_unknown = P.project_admitted_run_v3(
    *RC.positive(
        atom_override={"op": "none", "relation": "runtime-observation", "minResolution": "observed", "filters": [], "evidence": "runtime"},
        import_specs=[_rt_partial_opt],
        evidence_use=[{"kind": "runtime", "requirement": "optional"}],
        scope_document=SCOPE_DOC,
    )
)
check(
    "optional-unknown-pass-does-not-prove-absence",
    opt_unknown["derivedVerdict"] == "pass"
    and P.rule_can_prove_absence(opt_unknown, opt_unknown["policy"]["rules"][0]["ruleId"]) is False
    and set(P.admitted_root_predicate_values(opt_unknown, opt_unknown["policy"]["rules"][0]["ruleId"]).values()) == {"indeterminate"},
)

adv_none = P.project_admitted_run_v3(
    *RC.positive(
        atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        gate=False,
        scope_document=SCOPE_DOC,
    )
)
check(
    "advisory-all-roots-false-can-prove-absence",
    adv_none["derivedVerdict"] == "pass"
    and (not P.rule_gates(adv_none["policy"], adv_none["policy"]["rules"][0]["ruleId"]))
    and P.rule_can_prove_absence(adv_none, adv_none["policy"]["rules"][0]["ruleId"]) is True,
)

budget_view = P.project_admitted_run_v3(*RC.positive(budget_limit=1, scope_document=SCOPE_DOC))
check(
    "budget-exhausted-does-not-prove-absence",
    budget_view["evaluationState"] == "budget-exhausted" and P.rule_can_prove_absence(budget_view, budget_view["policy"]["rules"][0]["ruleId"]) is False,
)

def _runtime_spec(subjects, partial=False):
    item = {
        "kind": "runtime",
        "payload": {
            "payloadDomain": "workflow.import-payload.runtime.v1",
            "format": "v8-json",
            "observationWindow": {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"},
            "observedPopulation": "synthetic",
            "mappingGaps": [],
            "subjects": subjects,
        },
        "observation": {
            "window": {"startUtc": "2026-08-01T00:00:00Z", "endUtc": "2026-08-02T00:00:00Z"},
            "population": "synthetic",
        },
    }
    if partial:
        item["observation"].update(completeness="partial", omissions=["fixture omitted observations"])
    return item


_RT_ATOM = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed", "filters": [], "evidence": "runtime"}
_RT_EU = [{"kind": "runtime", "requirement": "required"}]
_RT_TWO = [{"path": "src/index.ts", "observability": "observed-hit", "hits": 2}, {"path": "README.md", "observability": "observed-hit", "hits": 1}]
_RT_ONE = [{"path": "src/index.ts", "observability": "observed-hit", "hits": 2}]
SCOPE_ALL = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}
base_over = RC.positive(atom_override=_RT_ATOM, import_specs=[_runtime_spec(_RT_TWO)], evidence_use=_RT_EU, scope_document=SCOPE_ALL)
cur_over = RC.positive(atom_override=_RT_ATOM, import_specs=[_runtime_spec(_RT_TWO)], evidence_use=_RT_EU, gate=False, scope_document=SCOPE_ALL)
e1_partial = RC.positive(atom_override=_RT_ATOM, import_specs=[_runtime_spec(_RT_ONE, partial=True)], evidence_use=_RT_EU, scope_document=SCOPE_ALL)
check("partial-pivot-shares-snapshot-with-two-subject-baseline", base_over[0]["snapshotId"] == e1_partial[0]["snapshotId"] == cur_over[0]["snapshotId"])
check("partial-pivot-shares-policy-with-two-subject-baseline", base_over[1][base_over[0]["planId"]][1]["policyDigest"] == e1_partial[1][e1_partial[0]["planId"]][1]["policyDigest"])
art_over = P.adopt_admitted_baseline_v3(*base_over, CUSTODY)
host_over = host_from_graph({"runId": art_over["descriptor"]["runId"]}, base_over[1])
host_over["pivotRunId"] = art_over["descriptor"]["runId"]
e1_view = P.project_admitted_run_v3(*e1_partial)
e1_hits = {o["finding"]["fingerprint"] for o in e1_view["occurrences"] if o["finding"]["fingerprint"]}
check("partial-import-view-cannot-prove-absence", P.rule_can_prove_absence(e1_view, e1_view["policy"]["rules"][0]["ruleId"]) is False)
check("partial-import-view-keeps-known-hit", bool(e1_hits))
reject(
    "e1-different-import-same-snapshot-refused",
    lambda: P.compare_admitted_v3(
        baseline_artifact=art_over,
        current_run=cur_over[0],
        current_objects=cur_over[1],
        current_blobs=cur_over[2],
        host=host_over,
        profile_name="code-regression",
        pivot_runs={"E1": e1_partial},
    ),
    "CONFIG.INVALID",
    "EVALUATION.FINDING_JOIN_REFUSED",
)
cmp_partial = P.compare_admitted_v3(
    baseline_artifact=art_over,
    current_run=cur_over[0],
    current_objects=cur_over[1],
    current_blobs=cur_over[2],
    host=host_over,
    profile_name="code-regression",
    pivot_runs={"E1": base_over},
)
base_fps = {e["fingerprint"] for e in art_over["descriptor"]["entries"]}
check("same-import-policy-remint-e1-available", cmp_partial["descriptor"]["pivotsAvailable"]["E1"] == "available")
check(
    "same-import-policy-remint-keeps-known-match",
    bool(base_fps)
    and all(next(e for e in cmp_partial["descriptor"]["entries"] if e["fingerprint"] == fp)["presence"]["E1"] is True for fp in base_fps),
)
must_valid("same-import-e1-comparison-schema", U + "comparison:2", cmp_obj(cmp_partial))

base_unmatched = RC.positive(symbol_rows=[{"nativeSubjectId": "symbol:x", "projectionAvailable": False}], scope_document=SCOPE_DOC)
cur_disabled = RC.positive(symbol_rows=[{"nativeSubjectId": "symbol:x"}], enabled=False, scope_document=SCOPE_DOC)
e1_enabled = RC.positive(symbol_rows=[{"nativeSubjectId": "symbol:x"}], enabled=True, scope_document=SCOPE_DOC)
check("disabled-e1-share-snapshot", base_unmatched[0]["snapshotId"] == cur_disabled[0]["snapshotId"] == e1_enabled[0]["snapshotId"])
check("disabled-e1-baseline-policy-matches-enabled-pivot", base_unmatched[1][base_unmatched[0]["planId"]][1]["policyDigest"] == e1_enabled[1][e1_enabled[0]["planId"]][1]["policyDigest"])
art_un = P.adopt_admitted_baseline_v3(*base_unmatched, CUSTODY)
check("disabled-e1-baseline-has-no-matched-entries", art_un["descriptor"]["entries"] == [])
host_un = host_from_graph({"runId": art_un["descriptor"]["runId"]}, base_unmatched[1])
host_un["pivotRunId"] = art_un["descriptor"]["runId"]
cmp_dis = P.compare_admitted_v3(
    baseline_artifact=art_un,
    current_run=cur_disabled[0],
    current_objects=cur_disabled[1],
    current_blobs=cur_disabled[2],
    host=host_un,
    profile_name="code-regression",
    pivot_runs={"E1": e1_enabled},
)
e1_en_view = P.project_admitted_run_v3(*e1_enabled)
e1_fps = [o["finding"]["fingerprint"] for o in e1_en_view["occurrences"] if o["finding"]["fingerprint"]]
dis_view = P.project_admitted_run_v3(*cur_disabled)
check("disabled-current-has-no-matched-occurrences", all(o["finding"]["correspondence"]["state"] != "matched" for o in dis_view["occurrences"]))
check("enabled-e1-has-matched-fingerprint", bool(e1_fps))
net = [e for e in cmp_dis["descriptor"]["entries"] if e["fingerprint"] in e1_fps]
check(
    "pivot-only-fp-is-code-net-new-with-subsequent-policy",
    any(e["classification"] == "CODE-NET-NEW" and e.get("gates") and "policy" in e.get("subsequentDeltas", []) for e in net),
)
check("disabled-current-does-not-drop-pivot-only-fingerprint", bool(net))
check(
    "disabled-current-does-not-erase-baseline-unmatched-gating",
    any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_dis["descriptor"]["ruleDeficiencies"])
    or cmp_dis["descriptor"]["verdict"] == "fail",
)
must_valid("disabled-e1-comparison-schema", U + "comparison:2", cmp_obj(cmp_dis))

_chapter_s2 = Path("/tmp/opensip-design-corrections/evaluator-successor.v1/docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text()
check(
    "declared-compatible-already-in-workflows-and-surfaces-section-2",
    "authenticated compatibility listing names the baseline" in _chapter_s2
    and ".opensip/detector-compatibility.json" in _chapter_s2
    and "closure.manifestDigest` continues to identify the component manifest body" in _chapter_s2,
)
check(
    "declared-compatible-not-claimed-implemented-from-caller-maps",
    "if a later owner requires" not in (HERE / "workflow_projection_model.v3.py").read_text()
    and "caller compatibleWith is not a current-trust signed-manifest join" in (HERE / "workflow_projection_model.v3.py").read_text(),
)
inv_v1 = json.loads((HERE / "command-inventory.v1.json").read_text())
inv3_schema = SCHEMAS[U + "command-inventory:3"]
json_renderer_v1 = next(r for r in inv_v1["renderers"] if r["format"] == "json")
env_golden = next(g for g in inv_v1["goldens"] if g["id"] == "envelope-major-unsupported")
check("historical-command-inventory-instance-remains-major-1", inv_v1["schemaMajor"] == 1)
check("isolated-command-inventory-schema-is-major-3", inv3_schema["properties"]["schemaMajor"]["const"] == 3)
check("v1-json-renderer-is-envelope-major-2", json_renderer_v1["version"] == 2 and "major 2" in json_renderer_v1["parityRule"])
check("v1-envelope-golden-still-pins-major-2", "schemaMajor 2" in env_golden["remedy"])
check("v1-inventory-not-validated-as-evaluator3-inventory-3", inv_v1["schemaMajor"] != inv3_schema["properties"]["schemaMajor"]["const"])

V9_CONTROL = len(CHECKS)
check("v9-control-coverage-preserved", V9_CONTROL >= 320)

# ----------------------------------------------------------------------------- v10: E1-E3 source-input join, wider scope, admitted manifest compatibility, inventory v3
inv_v3 = json.loads((HERE / "command-inventory.v3.json").read_text())
must_valid("command-inventory-v3-instance-matches-schema-3", U + "command-inventory:3", inv_v3)
json_renderer_v3 = next(r for r in inv_v3["renderers"] if r["format"] == "json")
env_golden_v3 = next(g for g in inv_v3["goldens"] if g["id"] == "envelope-major-unsupported")
check("command-inventory-v3-instance-is-major-3", inv_v3["schemaMajor"] == 3)
check("v3-json-renderer-is-envelope-major-3", json_renderer_v3["version"] == 3 and "major 3" in json_renderer_v3["parityRule"])
check("v3-envelope-golden-pins-major-3", "schemaMajor 3" in env_golden_v3["remedy"])
check("v1-inventory-instance-left-historical", inv_v1["schemaMajor"] == 1 and inv_v3["schemaMajor"] == 3)

must_valid(
    "detector-manifest-schema-admits-listing",
    U + "detector-manifest:1",
    {
        "schemaFamily": "opensip.product.detector-manifest",
        "schemaMajor": 1,
        "compatibleClosures": [{"closureId": "closure2:" + "a" * 64, "semanticsMajor": 2}],
    },
)
COMPONENT_MANIFEST_BYTES = b'{"kind":"component","manifestSchemaVersion":1,"name":"fixture-detector"}'
COMPONENT_MANIFEST_DIGEST = hashlib.sha256(COMPONENT_MANIFEST_BYTES).hexdigest()
LISTING_PATH = P.DETECTOR_COMPATIBILITY_TREE_PATH
body = {
    "schemaFamily": "opensip.product.detector-manifest",
    "schemaMajor": 1,
    "compatibleClosures": [{"closureId": DET, "semanticsMajor": 2}],
}
raw_body = canonical.canonical(body)
listing_digest = hashlib.sha256(raw_body).hexdigest()
listing_row = {"path": LISTING_PATH, "sha256": listing_digest, "bytes": len(raw_body)}
cid_m = "closure2:" + hashlib.sha256(b"manifest-compat-detector").hexdigest()
obj_m = {
    cid_m: (
        "closure",
        {
            "kind": "detector",
            "manifestDigest": COMPONENT_MANIFEST_DIGEST,
            "schemaVersion": 2,
            "tree": [listing_row],
            "semanticVersion": "1.0.0",
            "protocolMajor": 1,
            "platform": "any",
        },
    )
}
blobs_m = {COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES, listing_digest: raw_body}
host_ok = {"closures": {cid_m: {"bytes": "ok", "trust": "admitted", "trustOrigin": "retained-generation", "protocolMajor": 1, "platform": "linux"}}}
host_untrusted = {"closures": {cid_m: {"bytes": "ok", "trust": "revoked", "trustOrigin": "retained-generation", "protocolMajor": 1, "platform": "linux"}}}
check(
    "admitted-manifest-lists-compatible-closure",
    P.admitted_manifest_compatible_with(cid_m, 2, obj_m, blobs_m, host_ok) == [DET],
)
check(
    "untrusted-host-closure-yields-no-compatibleWith",
    P.admitted_manifest_compatible_with(cid_m, 2, obj_m, blobs_m, host_untrusted) == [],
)
check("raw-fixture-bytes-are-not-detector-manifest", P.parse_detector_manifest_body({"x": b"not-json"}, "x") is None)
check("listing-is-not-component-manifest-digest", listing_digest != COMPONENT_MANIFEST_DIGEST)
check(
    "listing-not-read-from-component-manifest-digest",
    P.parse_detector_manifest_body(blobs_m, COMPONENT_MANIFEST_DIGEST) is None,
)

# wider-scope counterfactual: baseline ** vs current src/** ; E2 is ** + current policy
wide_base = RC.positive(scope_document=SCOPE_WIDE)
narrow_cur = RC.positive(scope_document=SCOPE_DOC)
art_wide = P.adopt_admitted_baseline_v3(*wide_base, CUSTODY)
host_w = host_from_graph({"runId": art_wide["descriptor"]["runId"]}, wide_base[1])
host_w["pivotRunId"] = art_wide["descriptor"]["runId"]
check("wider-scope-same-snapshot", wide_base[0]["snapshotId"] == narrow_cur[0]["snapshotId"])
check("wider-scope-same-policy", wide_base[1][wide_base[0]["planId"]][1]["policyDigest"] == narrow_cur[1][narrow_cur[0]["planId"]][1]["policyDigest"])
e2_wide = RC.positive(scope_document=SCOPE_WIDE)
cmp_wide = P.compare_admitted_v3(
    baseline_artifact=art_wide,
    current_run=narrow_cur[0],
    current_objects=narrow_cur[1],
    current_blobs=narrow_cur[2],
    host=host_w,
    profile_name="code-regression",
    pivot_runs={"E2": e2_wide},
)
wide_view = P.project_admitted_run_v3(*wide_base)
narrow_view = P.project_admitted_run_v3(*narrow_cur)
wide_fps = {o["finding"]["fingerprint"] for o in wide_view["occurrences"] if o["finding"]["fingerprint"]}
narrow_fps = {o["finding"]["fingerprint"] for o in narrow_view["occurrences"] if o["finding"]["fingerprint"]}
outside = wide_fps - narrow_fps
check("wider-scope-e2-available", cmp_wide["descriptor"]["pivotsAvailable"]["E2"] == "available")
check("narrow-current-omits-wider-selected-paths", bool(outside))
check(
    "wider-scope-does-not-false-absent-unselected-current-paths",
    all(next(e for e in cmp_wide["descriptor"]["entries"] if e["fingerprint"] == fp)["presence"]["E4"] is False for fp in outside)
    and all(next(e for e in cmp_wide["descriptor"]["entries"] if e["fingerprint"] == fp)["presence"]["E2"] is True for fp in outside),
)
must_valid("wider-scope-comparison-schema", U + "comparison:2", cmp_obj(cmp_wide))
check("path-src-in-src-glob", P.path_in_scope_document(SCOPE_DOC, "src/index.ts") is True)
check("path-readme-not-in-src-glob", P.path_in_scope_document(SCOPE_DOC, "README.md") is False)
check("path-readme-in-wide-glob", P.path_in_scope_document(SCOPE_WIDE, "README.md") is True)
check("path-double-star-ts-matches-root-file", P.path_in_scope_document({"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**/*.ts"], "exclude": []}, "a.ts") is True)
check("path-uses-owner-glob-match", P.W.glob_match("**/*.ts", "a.ts") is True and P.path_in_scope_document({"include": ["**/*.ts"], "exclude": []}, "a.ts") is True)

check("detector-manifest-schema-registered", U + "detector-manifest:1" in SCHEMAS)

V10_CONTROL = len(CHECKS)
check("v10-control-coverage-preserved", V10_CONTROL >= 342)

# ----------------------------------------------------------------------------- v11: sidecar locators, proof-root Kleene, required manifest, TCB body, E0/extent
check(
    "boolean-and-false-dominated-unknown-proves-absence",
    bool_false["derivedVerdict"] == "pass"
    and bool_false["ruleResults"][0]["deficiencies"]
    and P.rule_can_prove_absence(bool_false, bool_false["policy"]["rules"][0]["ruleId"]) is True,
)
check(
    "boolean-or-true-does-not-prove-absence",
    P.rule_can_prove_absence(bool_true, bool_true["policy"]["rules"][0]["ruleId"]) is False,
)
check(
    "boolean-or-true-keeps-known-hit-while-other-roots-unknown",
    any(o["finding"]["fingerprint"] for o in bool_true["occurrences"]),
)
check(
    "admitted-view-exposes-proof-root-p",
    any(p.get("predicateId") == "p" and p.get("ruleId") == none_view["policy"]["rules"][0]["ruleId"] for p in none_view["proof"]["predicateProofs"]),
)
check(
    "optional-unknown-roots-are-not-all-false",
    P.rule_can_prove_absence(opt_unknown, opt_unknown["policy"]["rules"][0]["ruleId"]) is False
    and "indeterminate" in P.admitted_root_predicate_values(opt_unknown, opt_unknown["policy"]["rules"][0]["ruleId"]).values(),
)
src_model = (HERE / "workflow_projection_model.v3.py").read_text()
check(
    "e0-does-not-require-current-native-input-equality",
    'if axis == "E0":\n        return' in src_model and "E0_EXCLUDED_CLOSURE_KINDS" in src_model,
)
e0_inputs = P.semantic_source_inputs(file_pos, "E0")
e1_inputs = P.semantic_source_inputs(file_pos, "E1")
check("e0-source-map-omits-native-context", "nativeContextDigests" not in e0_inputs and "nativeContextDigests" in e1_inputs)
check("e1-source-map-requires-execution-inputs", e1_inputs.get("executionInputs") is not None)
extracted = P.extracted_source_paths(file_pos)
snap_rows = file_pos["objects"][file_pos["snapshotId"]][1].get("sourceInventory") or []
snap_paths = {r.get("path") for r in snap_rows if r.get("path")}
ext_fn = src_model.split("def extracted_source_paths", 1)[1].split("\ndef ", 1)[0]
check(
    "extracted-extent-is-inventory-examined-not-snapshot-membership",
    ".get(\"sourceInventory\")" not in ext_fn and "sourceInventory]" not in ext_fn and extracted <= snap_paths and bool(extracted),
)
check("path-outside-extracted-extent-is-missing-extent-basis", "docs/out.ts" not in extracted)
thin_missing_exec = dict(file_pos, evaluationInputRefs=[r for r in file_pos["evaluationInputRefs"] if r.get("domain") != "execution-inputs"])
reject(
    "missing-execution-inputs-refused",
    lambda: P._execution_inputs_evidence(thin_missing_exec, "E1"),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)

compat = P.project_admitted_detector_compatibility(cid_m, obj_m, blobs_m, host_ok)
check(
    "admitted-compatibility-receipt-is-host-only",
    compat is not None
    and compat["closureId"] == cid_m
    and compat["componentManifestDigest"] == COMPONENT_MANIFEST_DIGEST
    and compat["listing"] == listing_row
    and compat["trustOrigin"] == "retained-generation"
    and compat.get("platform") == "any"
    and compat.get("protocolMajor") == 1
    and "trust" not in compat
    and "manifestDigest" not in compat
    and compat["compatibleClosures"][0]["closureId"] == DET,
)
check(
    "untrusted-host-yields-no-compatibility-receipt",
    P.project_admitted_detector_compatibility(cid_m, obj_m, blobs_m, host_untrusted) is None,
)
malformed_major = {"schemaFamily": "opensip.product.detector-manifest", "schemaMajor": 2, "compatibleClosures": []}
malformed_raw = canonical.canonical(malformed_major)
malformed_digest = hashlib.sha256(malformed_raw).hexdigest()
reject(
    "malformed-recognized-manifest-major-refused",
    lambda: P.parse_detector_manifest_body({malformed_digest: malformed_raw}, malformed_digest),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
wrong_key = "0" * 64
reject(
    "malformed-recognized-manifest-hash-mismatch-refused",
    lambda: P.parse_detector_manifest_body({wrong_key: raw_body}, wrong_key),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
unsorted_body = {
    "schemaFamily": "opensip.product.detector-manifest",
    "schemaMajor": 1,
    "compatibleClosures": [
        {"closureId": "closure2:" + "f" * 64, "semanticsMajor": 2},
        {"closureId": "closure2:" + "a" * 64, "semanticsMajor": 2},
    ],
}
unsorted_raw = canonical.canonical(unsorted_body)
unsorted_digest = hashlib.sha256(unsorted_raw).hexdigest()
reject(
    "malformed-recognized-manifest-order-refused",
    lambda: P.parse_detector_manifest_body({unsorted_digest: unsorted_raw}, unsorted_digest),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
other_fam = {"schemaFamily": "opensip.product.other", "schemaMajor": 1, "compatibleClosures": []}
other_raw = canonical.canonical(other_fam)
other_digest = hashlib.sha256(other_raw).hexdigest()
check("unsupported-manifest-family-is-no-declaration", P.parse_detector_manifest_body({other_digest: other_raw}, other_digest) is None)

_sr_spec = importlib.util.spec_from_file_location("semantic_replay_check3", FOUNDATION / "check-semantic-replay.v3.py")
SR = importlib.util.module_from_spec(_sr_spec)
_sr_spec.loader.exec_module(SR)


def _put_blob(blobs, value):
    raw = value if type(value) is bytes else canonical.canonical(value)
    digest = hashlib.sha256(raw).hexdigest()
    blobs[digest] = raw
    return digest


def _mint_obj(objects, domain, fields):
    rec = {"schemaVersion": 2, **fields}
    key = RC.M.identifier(domain, rec)
    objects[key] = (domain, rec)
    return key


def attach_scope_document(graph, scope_doc):
    """Remint analysis-spec + Plan locators so a semantic graph selects ScopeDocumentV1."""
    graph = copy.deepcopy(graph)
    objects, blobs = graph["objects"], graph["blobs"]
    old_plan_id = graph["inputs"]["planId"]
    old_exec_id = graph["inputs"]["executionPlanId"]
    old_plan = objects[old_plan_id][1]
    old_exec = objects[old_exec_id][1]
    spec = canonical.parse(blobs[old_plan["analysisSpecDigest"]])
    schema_d = _put_blob(blobs, (WF / "policy-document.schema.json").read_bytes())
    payload_d = _put_blob(blobs, scope_doc)
    spec = dict(spec, parameters=RC.E.cset(list(spec["parameters"]) + [{"schemaDigest": schema_d, "payloadDigest": payload_d}]))
    spec_d = _put_blob(blobs, spec)
    plan_fields = {k: v for k, v in old_plan.items() if k != "schemaVersion"}
    plan_fields["analysisSpecDigest"] = spec_d
    new_plan_id = _mint_obj(objects, "plan", plan_fields)
    inv_map = {}
    new_inventory = []
    for digest, inv in graph["inventoryResults"]:
        rec = dict(inv, planId=new_plan_id)
        nd = _put_blob(blobs, rec)
        inv_map[digest] = nd
        new_inventory.append((nd, rec))
    old_to_new_view = {}
    new_view_ids = []
    for vid in graph["viewIds"]:
        view = copy.deepcopy(objects[vid][1])
        view["planId"] = new_plan_id
        nid = _mint_obj(objects, "view", {k: v for k, v in view.items() if k != "schemaVersion"})
        old_to_new_view[vid] = nid
        new_view_ids.append(nid)
    old_stage_d = old_exec["stages"][0]["stageSpecDigest"]
    stage = dict(canonical.parse(blobs[old_stage_d]), planId=new_plan_id, parameters=spec["parameters"])
    new_stage_d = _put_blob(blobs, stage)
    new_exec_id = _mint_obj(
        objects,
        "execution-plan",
        {
            "planId": new_plan_id,
            "stages": [
                {
                    "ordinal": 0,
                    "stageSpecDigest": new_stage_d,
                    "requires": [],
                    "outputDomains": list(old_exec["stages"][0].get("outputDomains") or ["view"]),
                }
            ],
        },
    )

    def rewrite_ref(ref):
        domain, digest = ref.get("domain"), ref.get("digest")
        if domain == "view":
            new_vid = old_to_new_view.get("view2:" + digest)
            if new_vid:
                return {"domain": "view", "digest": new_vid.split(":", 1)[1]}
        if domain == "subject-inventory" and digest in inv_map:
            return {"domain": "subject-inventory", "digest": inv_map[digest]}
        if domain in ("target-attribution", "incoming-search", "candidate-producer-result") and digest in blobs:
            rec = dict(canonical.parse(blobs[digest]), planId=new_plan_id)
            if domain == "incoming-search":
                rec["expectedInventoryRefs"] = RC.E.cset(inv_map.get(x, x) for x in rec.get("expectedInventoryRefs") or [])
            if domain == "candidate-producer-result":
                rec["executionPlanId"] = new_exec_id
            return {"domain": domain, "digest": _put_blob(blobs, rec)}
        return dict(ref)

    inputs = dict(graph["inputs"])
    inputs.update(
        {
            "plan": objects[new_plan_id][1],
            "planId": new_plan_id,
            "executionPlanId": new_exec_id,
            "evaluationInputRefs": RC.E.cset(rewrite_ref(r) for r in graph["inputs"]["evaluationInputRefs"]),
            "inventoryLocatorCount": len(new_inventory),
            "inventoryRowCount": sum(len(inv["rows"]) for _d, inv in new_inventory),
        }
    )
    inputs.pop("executionInputsDigest", None)
    graph.update(
        {
            "objects": objects,
            "blobs": blobs,
            "inputs": inputs,
            "planId": new_plan_id,
            "inventoryResults": new_inventory,
            "viewIds": RC.E.cset(new_view_ids),
        }
    )
    if graph.get("viewId") in old_to_new_view:
        graph["viewId"] = old_to_new_view[graph["viewId"]]
    graph.pop("executionInputs", None)
    graph.pop("executionInputsDigest", None)
    return graph


def close_semantic_sidecar(atom, scope_doc):
    g = SR.S.build_ts_semantic_graph(
        atom=atom,
        has_declares=False,
        has_references_fact=True,
        second_partition=True,
        references_resolved=True,
        incoming_search=True,
        incoming_complete=True,
        target_sidecar=True,
    )
    g = attach_scope_document(g, scope_doc)
    run, objects, blobs, _actual = SR.close_positive(g)
    return run, objects, blobs


SIDECAR_SCOPE = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}
sidecar_exists = close_semantic_sidecar(SR.REFS_EXISTS_TGT, SIDECAR_SCOPE)
sidecar_none = close_semantic_sidecar(SR.REFS_NONE_TGT, SIDECAR_SCOPE)
sidecar_exists_view = P.project_admitted_run_v3(*sidecar_exists)
sidecar_none_view = P.project_admitted_run_v3(*sidecar_none)


def _domain_digests(view, domain):
    return sorted(r["digest"] for r in view["evaluationInputRefs"] if r.get("domain") == domain)


check("sidecar-bearing-runs-share-snapshot", sidecar_exists[0]["snapshotId"] == sidecar_none[0]["snapshotId"])
check(
    "sidecar-plan-locator-remints-raw-attribution-digest",
    bool(_domain_digests(sidecar_exists_view, "target-attribution"))
    and _domain_digests(sidecar_exists_view, "target-attribution") != _domain_digests(sidecar_none_view, "target-attribution"),
)
check(
    "sidecar-plan-locator-remints-raw-incoming-digest",
    bool(_domain_digests(sidecar_exists_view, "incoming-search"))
    and _domain_digests(sidecar_exists_view, "incoming-search") != _domain_digests(sidecar_none_view, "incoming-search"),
)
check(
    "sidecar-policy-remint-joins-stripped-source-inputs",
    canonical.canonical(P.semantic_source_inputs(sidecar_exists_view, "E1"))
    == canonical.canonical(P.semantic_source_inputs(sidecar_none_view, "E1")),
)
art_sidecar = P.adopt_admitted_baseline_v3(*sidecar_exists, CUSTODY)
host_sc = host_from_graph({"runId": art_sidecar["descriptor"]["runId"]}, sidecar_exists[1])
host_sc["pivotRunId"] = art_sidecar["descriptor"]["runId"]
cmp_sidecar = P.compare_admitted_v3(
    baseline_artifact=art_sidecar,
    current_run=sidecar_none[0],
    current_objects=sidecar_none[1],
    current_blobs=sidecar_none[2],
    host=host_sc,
    profile_name="code-regression",
    pivot_runs={"E1": sidecar_exists},
)
check("sidecar-bearing-e1-policy-remint-available", cmp_sidecar["descriptor"]["pivotsAvailable"]["E1"] == "available")
must_valid("sidecar-bearing-e1-comparison-schema", U + "comparison:2", cmp_obj(cmp_sidecar))

# ----------------------------------------------------------------------------- v12: listing tree-path, covering-scope deletion, candidate locators
empty_listing = {"schemaFamily": "opensip.product.detector-manifest", "schemaMajor": 1, "compatibleClosures": []}
empty_raw = canonical.canonical(empty_listing)
empty_digest = hashlib.sha256(empty_raw).hexdigest()
empty_row = {"path": LISTING_PATH, "sha256": empty_digest, "bytes": len(empty_raw)}
cid_empty = "closure2:" + hashlib.sha256(b"empty-listing-detector").hexdigest()
obj_empty = {
    cid_empty: (
        "closure",
        {
            "kind": "detector",
            "manifestDigest": COMPONENT_MANIFEST_DIGEST,
            "schemaVersion": 2,
            "tree": [empty_row],
            "semanticVersion": "1.0.0",
            "protocolMajor": 1,
            "platform": "any",
        },
    )
}
blobs_empty = {COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES, empty_digest: empty_raw}
host_empty = {"closures": {cid_empty: {"bytes": "ok", "trust": "admitted", "trustOrigin": "installed-signed-release", "protocolMajor": 1, "platform": "linux"}}}
proj_empty = P.project_admitted_detector_compatibility(cid_empty, obj_empty, blobs_empty, host_empty)
check("present-empty-listing-is-complete-declaration", proj_empty is not None and proj_empty["compatibleClosures"] == [])
cid_absent = "closure2:" + hashlib.sha256(b"absent-listing-detector").hexdigest()
obj_absent = {
    cid_absent: (
        "closure",
        {
            "kind": "detector",
            "manifestDigest": COMPONENT_MANIFEST_DIGEST,
            "schemaVersion": 2,
            "tree": [],
            "semanticVersion": "1.0.0",
            "protocolMajor": 1,
            "platform": "any",
        },
    )
}
host_absent = {"closures": {cid_absent: {"bytes": "ok", "trust": "admitted", "trustOrigin": "signed-closure-bundle", "protocolMajor": 1, "platform": "linux"}}}
check(
    "absent-listing-path-is-no-declaration",
    P.project_admitted_detector_compatibility(cid_absent, obj_absent, {COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES}, host_absent) is None
    and P.admitted_manifest_compatible_with(cid_absent, 2, obj_absent, {COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES}, host_absent) == [],
)
check("empty-listing-distinct-from-absent-path", proj_empty is not None and P.project_admitted_detector_compatibility(cid_absent, obj_absent, {COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES}, host_absent) is None)

def _present_listing_closure(raw, row, token, blobs_extra=None, origin="retained-generation", trust="admitted"):
    cid = "closure2:" + hashlib.sha256(token.encode()).hexdigest()
    obj = {
        cid: (
            "closure",
            {
                "kind": "detector",
                "manifestDigest": COMPONENT_MANIFEST_DIGEST,
                "schemaVersion": 2,
                "tree": [row],
                "semanticVersion": "1.0.0",
                "protocolMajor": 1,
                "platform": "any",
            },
        )
    }
    blobs = {COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES}
    if blobs_extra:
        blobs.update(blobs_extra)
    elif raw is not None:
        blobs[row["sha256"]] = raw
    host = {"closures": {cid: {"bytes": "ok", "trust": trust, "protocolMajor": 1, "platform": "linux"}}}
    if origin:
        host["closures"][cid]["trustOrigin"] = origin
    return cid, obj, blobs, host

mal_row = {"path": LISTING_PATH, "sha256": malformed_digest, "bytes": len(malformed_raw)}
cid_mal, obj_mal, blobs_mal, host_mal = _present_listing_closure(malformed_raw, mal_row, "malformed-present")
reject(
    "present-malformed-listing-refused",
    lambda: P.project_admitted_detector_compatibility(cid_mal, obj_mal, blobs_mal, host_mal),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
unrec_row = {"path": LISTING_PATH, "sha256": other_digest, "bytes": len(other_raw)}
cid_un, obj_un, blobs_un, host_un = _present_listing_closure(other_raw, unrec_row, "unrecognized-present")
reject(
    "present-unrecognized-listing-refused",
    lambda: P.project_admitted_detector_compatibility(cid_un, obj_un, blobs_un, host_un),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
miss_row = {"path": LISTING_PATH, "sha256": listing_digest, "bytes": len(raw_body)}
cid_miss, obj_miss, blobs_miss, host_miss = _present_listing_closure(None, miss_row, "missing-blob", blobs_extra={COMPONENT_MANIFEST_DIGEST: COMPONENT_MANIFEST_BYTES})
reject(
    "present-listing-missing-blob-refused",
    lambda: P.project_admitted_detector_compatibility(cid_miss, obj_miss, blobs_miss, host_miss),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
len_row = {"path": LISTING_PATH, "sha256": listing_digest, "bytes": len(raw_body) + 1}
cid_len, obj_len, blobs_len, host_len = _present_listing_closure(raw_body, len_row, "length-mismatch")
reject(
    "present-listing-hash-length-mismatch-refused",
    lambda: P.project_admitted_detector_compatibility(cid_len, obj_len, blobs_len, host_len),
    "REQUEST.PRECONDITION_FAILED",
    "EVALUATION.PROJECTION_INPUT_INCOMPLETE",
)
cid_norigin, obj_norigin, blobs_norigin, host_norigin = _present_listing_closure(raw_body, listing_row, "no-origin", origin=None)
check(
    "unsigned-listing-without-trio-origin-is-no-declaration",
    P.project_admitted_detector_compatibility(cid_norigin, obj_norigin, blobs_norigin, host_norigin) is None,
)
cid_swap, obj_swap, blobs_swap, host_swap = _present_listing_closure(raw_body, listing_row, "swapped-tree", trust="revoked", origin="retained-generation")
check(
    "swapped-tree-without-same-closure-trust-is-no-declaration",
    P.project_admitted_detector_compatibility(cid_swap, obj_swap, blobs_swap, host_swap) is None
    and P.admitted_manifest_compatible_with(cid_swap, 2, obj_swap, blobs_swap, host_swap) == [],
)
narrow_foundation = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["src"], "excludedPathPrefixes": []}
nf_raw = canonical.canonical(narrow_foundation)
nf_digest = hashlib.sha256(nf_raw).hexdigest()
check("narrow-foundation-covers-src", P.foundation_scope_covers_path(narrow_foundation, "src/index.ts") is True)
check("narrow-foundation-does-not-cover-readme", P.foundation_scope_covers_path(narrow_foundation, "README.md") is False)
check(
    "scope-wider-than-extraction-is-missing-extent",
    P.path_absence_claim_allowed(
        "README.md",
        examined={"src/index.ts"},
        scope_doc=SCOPE_WIDE,
        foundation_scope=narrow_foundation,
        extraction_complete=True,
    )
    is False,
)
check(
    "deleted-path-under-complete-covering-scope-may-be-absent",
    P.path_absence_claim_allowed(
        "README.md",
        examined={"src/index.ts"},
        scope_doc=SCOPE_WIDE,
        foundation_scope={"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["."], "excludedPathPrefixes": []},
        extraction_complete=True,
    )
    is True,
)
file_foundation = P.foundation_scope_record(file_pos)
check(
    "file-fixture-foundation-covers-readme",
    P.foundation_scope_covers_path(file_foundation, "README.md") is True and P.inventories_are_complete(file_pos) is True,
)
check("extracted-paths-are-not-a-snapshot-union-claim", "docs/out.ts" not in extracted and P.path_absence_claim_allowed("docs/out.ts", examined=extracted, scope_doc=SCOPE_WIDE, foundation_scope=narrow_foundation, extraction_complete=True) is False)

_cand_spec = importlib.util.spec_from_file_location("cand_fix_v3", FOUNDATION / "evaluator_candidate_fixture.v3.py")
Cand = importlib.util.module_from_spec(_cand_spec)
_cand_spec.loader.exec_module(Cand)


def close_candidate(mode, scope_doc):
    g = Cand.build_candidate_graph(mode=mode)
    g = attach_scope_document(g, scope_doc)
    seed, objects, blobs, _ = Cand.F.seal_fixture(g)
    _, owner = RC.M.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    result = RC.R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = SR.S.seal_derived(g, result, objects, blobs)
    RC.R.replay(run, objects, blobs)
    RC.M.close_run(run, objects, blobs)
    return run, objects, blobs


cand_wide = close_candidate("group-bearing", SCOPE_WIDE)
cand_doc = close_candidate("group-bearing", SCOPE_DOC)
cand_wide_view = P.project_admitted_run_v3(*cand_wide)
cand_doc_view = P.project_admitted_run_v3(*cand_doc)
check("candidate-graphs-share-snapshot", cand_wide[0]["snapshotId"] == cand_doc[0]["snapshotId"])
check(
    "candidate-plan-locator-remints-raw-digest",
    bool(_domain_digests(cand_wide_view, "candidate-producer-result"))
    and _domain_digests(cand_wide_view, "candidate-producer-result") != _domain_digests(cand_doc_view, "candidate-producer-result"),
)
check(
    "candidate-policy-scope-remint-joins-stripped-source-inputs",
    canonical.canonical(P.semantic_source_inputs(cand_wide_view, "E1"))
    == canonical.canonical(P.semantic_source_inputs(cand_doc_view, "E1")),
)
check(
    "candidate-execution-inputs-expand-stripped-bodies",
    bool(P.semantic_source_inputs(cand_wide_view, "E1")["executionInputs"]["candidateResultEvidence"]),
)

# ------------------------------------------------------- repair closed-world selection law
# AUTHOR_PENDING_REVIEW. Focused controls for the selection law introduced in
# repair_closed_world_selection.v1.py and workflows-and-surfaces.md section 6.
#
# SCOPE, stated exactly. The POSITIVE, the CONFLICTING NEGATIVE and the ASYMMETRIC
# selected-program control below derive from FULL ADMITTED Runs: each is built by the foundation
# graph fixture, admitted at the native producer boundary (admit_coverage_result_v3, inside the
# fixture), then closed by identity-model.v3.close_run, which runs the complete evaluator3
# semantic replay. A schema fragment or a pre-selected adapter input would not establish that
# native selection join. The _cw_preview helper separately uses the historical synthetic
# host adapter and major-1 descriptor constructor; it does not establish an admitted current
# descriptor or a joined real-Run snapshot/trust/requirements projection. Controls marked UNIT
# exercise one published rule on a
# constructed view or plan and are NOT full-Run controls; they are labelled so in their ids.
#
# The asymmetric control uses the authorized default-off fixture option
# `symbol_only_second_program`; with it unset every existing caller is byte-identical.
#
# NOT CLAIMED: native producer qualification, real extraction, or a full product repair. The
# ClosedWorldV2 values are synthetic producer observations minted by the native owner's own
# closed_world_v2 helper.
_sel_spec = importlib.util.spec_from_file_location("repair_cw_selection", HERE / "repair_closed_world_selection.v1.py")
SEL = importlib.util.module_from_spec(_sel_spec)
_sel_spec.loader.exec_module(SEL)

_wf3_spec = importlib.util.spec_from_file_location("workflows_profile3", HERE / "workflows_model.v3.py")
WF3 = importlib.util.module_from_spec(_wf3_spec)
_wf3_spec.loader.exec_module(WF3)

_nat_spec = importlib.util.spec_from_file_location("native_owner2", HERE.parent / "native" / "native_evidence_model.v2.py")
NAT = importlib.util.module_from_spec(_nat_spec)
_nat_spec.loader.exec_module(NAT)

CW_CLOSED = NAT.closed_world_v2(package_json={"private": True},
                                entry_points={"state": "all", "source": "explicit"},
                                unresolved=[], external_consumers="none-declared")
CW_OPEN = NAT.closed_world_v2(package_json={"private": True},
                              entry_points={"state": "partial", "source": "recognized"},
                              unresolved=[], external_consumers="unknown")
check("repair-cw-owner-minted-records-differ-on-the-gated-flag",
      CW_CLOSED["deadCodeRepairEligible"] is True and CW_OPEN["deadCodeRepairEligible"] is False)


def _obeys_section_4_5(record):
    """Native section 4.5: deadCodeRepairEligible is true ONLY with exportsClosed=closed,
    entryPointsRecognized=all and no nonliteral loading. Every ClosedWorldV2 value this
    section uses is minted by the native owner's own helper, so none of them is a
    schema-valid-but-non-conforming combination, and no conclusion here rests on one."""
    if not record["deadCodeRepairEligible"]:
        return True
    return (record["exportsClosed"] == "closed" and record["entryPointsRecognized"] == "all"
            and record["nonliteralLoading"] == "none")


def _close_run_with_closed_worlds(assign, **kwargs):
    """Build and FULLY ADMIT a Run whose per-entry closedWorld is chosen by `assign(key, i)`."""
    seen = []
    original = RC.F.fixture_helpers

    def helpers():
        H = original()
        base = H.coverage_result

        def coverage_result(scope_descriptor, universe, resolved, blobs=None, inventory_paths=None, unresolved=()):
            payload = base(scope_descriptor, universe, resolved, blobs, inventory_paths, unresolved)
            if universe not in seen:
                seen.append(universe)
            payload["entry"]["closedWorld"] = copy.deepcopy(assign(payload["key"], seen.index(universe)))
            return payload

        H.coverage_result = coverage_result
        return H

    RC.F.fixture_helpers = helpers
    try:
        g = RC.F.build_file_inputs(**kwargs)
        seed, objects, blobs, _ = RC.F.seal_fixture(g)
        _, owner = RC.M.open_run_closure(seed, objects, blobs)
        i = g["inputs"]
        result = RC.R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
        run, objects, blobs = RC.seal(g, result, objects, blobs)
        run_id = RC.M.close_run(run, objects, blobs)
        return run_id, run, objects, blobs
    finally:
        RC.F.fixture_helpers = original


CW_TREE = {"README.md": b"# Synthetic fixture\n", "src/index.ts": b"export const x = 1;\n", "extensionless": b"fixture\n"}
CW_PROJECT = "prj1-" + "4" * 64
CW_RECIPE = {"contributionId": "core.repair", "recipeId": "remove-unused-export", "recipeVersion": "1.0.0", "closureId": "closure2:" + "c" * 64}
CW_TRUST = {CW_RECIPE["closureId"]: "admitted"}
# The plan's ONLY evidence requirement names `imports`. Nothing here names `package`, which is
# the relation the conflicting negative dissents on.
CW_REQS = [{"relation": "imports", "minResolution": "resolved-target", "completeness": "complete", "satisfied": True}]
CW_DELETE = [{"path": "src/index.ts", "action": "delete"}]


def _cw_preview(run_id, run, objects, blobs, targets, edits, requirements=None):
    """Synthetic host projection using the current selection hook over real retained evidence.

    The tree/project/snapshot/trust/requirements adapter is historical fixture data, not derived
    from the Run. The inherited constructor emits a major-1 descriptor; this helper therefore
    demonstrates gate integration only, not current descriptor admission or snapshot joins.
    """
    view = SEL.RetainedRunView(run, objects, blobs)
    adapter = {"authority": "authoritative", "availability": "retained", "sealedAssurance": "replayable",
               "runId": run_id, "planId": run["planId"],
               "snapshotId": WF3.tree_snapshot_id(CW_PROJECT, CW_TREE),
               "findings": targets, "retained": view, "evidenceOrigin": "native-analysis"}
    return WF3.repair_preview(CW_PROJECT, CW_TREE, adapter, CW_RECIPE, targets, edits,
                              CW_REQS if requirements is None else requirements, ["**"], CW_TRUST)


# --- FULL ADMITTED RUN 1: every retained entry agrees that repair is eligible.
cw_pos_id, cw_pos_run, cw_pos_obj, cw_pos_blob = _close_run_with_closed_worlds(lambda key, idx: CW_CLOSED, multiple_universes=True)
cw_view = SEL.RetainedRunView(cw_pos_run, cw_pos_obj, cw_pos_blob)
CW_FPS = sorted({f["fingerprint"] for _, f in cw_view.matched_findings() if f.get("fingerprint")})
check("repair-cw-positive-derives-from-a-fully-admitted-run", cw_pos_id.startswith("run3:"), cw_pos_id)
cw_pos_plan = _cw_preview(cw_pos_id, cw_pos_run, cw_pos_obj, cw_pos_blob, CW_FPS[:1], CW_DELETE)
check("repair-cw-all-agreeing-entries-admit-the-unsafe-plan",
      cw_pos_plan["descriptor"]["applicable"] is True and cw_pos_plan["descriptor"]["unmetPreconditions"] == [],
      str(cw_pos_plan["descriptor"]["unmetPreconditions"]))
check("repair-cw-positive-summary-is-the-agreed-value",
      cw_pos_plan["descriptor"]["closedWorld"] == {"deadCodeRepairEligible": True, "exportsClosed": "closed",
                                                   "entryPointsRecognized": "all", "nonliteralLoading": "none",
                                                   "externalConsumers": "none-declared"},
      str(cw_pos_plan["descriptor"]["closedWorld"]))
# MULTI-UNIVERSE SAME FINGERPRINT and MULTI-OWNER PATH, both read off this admitted Run: the
# one target fingerprint is matched in BOTH universes, and src/index.ts is owned by BOTH.
cw_pos_derived = SEL.derive(cw_view, CW_FPS[:1], CW_DELETE)
check("repair-cw-one-fingerprint-matched-in-two-universes-contributes-both",
      len({s["via"] for rows in cw_pos_derived["universeSources"].values() for s in rows if s["via"] == "target"}) == 1
      and len([u for u, rows in cw_pos_derived["universeSources"].items() if any(s["via"] == "target" for s in rows)]) == 2)
check("repair-cw-multi-owner-path-keeps-every-owning-universe",
      len([u for u, rows in cw_pos_derived["universeSources"].items() if any(s["via"] == "unsafe-edit-path" for s in rows)]) == 2)
check("repair-cw-path-owners-come-from-the-retained-selected-program-census",
      all(set(s) >= {"capabilityId", "cellOrdinal", "programOrdinal", "extentKinds", "provenance"}
          for rows in cw_pos_derived["universeSources"].values() for s in rows
          if s["via"] == "unsafe-edit-path"))
check("repair-cw-census-reports-which-extent-kind-witnessed-ownership",
      {k for rows in cw_pos_derived["universeSources"].values() for s in rows
       if s["via"] == "unsafe-edit-path" for k in s["extentKinds"]} <= {"file", "package", "symbol", "candidateSourcePaths"})
check("repair-cw-source-path-relations-are-all-same-only-universes",
      set(SEL.SOURCE_PATH_UNIVERSE_RULES.values()) == {"same-only"}
      and set(SEL.SOURCE_PATH_RELATIONS) == {"file", "clones", "vcs-change"},
      str(SEL.SOURCE_PATH_UNIVERSE_RULES))
check("repair-cw-source-path-scopes-are-an-additional-witness-not-the-census",
      "censusUniverses" in cw_pos_derived["ownership"]
      and "witnessUniverses" in cw_pos_derived["ownership"]
      and "witnessOnlyUniverses" in cw_pos_derived["ownership"])
# In THIS symmetric Run every witness is already in the census. Measured, not assumed.
check("repair-cw-witnesses-are-redundant-in-a-symmetric-run",
      cw_pos_derived["ownership"]["witnessOnlyUniverses"] == []
      and set(cw_pos_derived["ownership"]["witnessUniverses"]) <= set(cw_pos_derived["ownership"]["censusUniverses"]),
      str(cw_pos_derived["ownership"]))
check("repair-cw-enumeration-plan-is-reached-through-retained-joins-only",
      set(cw_view.enumeration_plan()) >= {"cells", "snapshotId", "scopeDigest", "membershipDigest"})

# --- FULL ADMITTED RUN 2: one `package` entry in ONE universe dissents. No evidence
# requirement names `package`, so this is also the omission-does-not-bypass control.
cw_neg_id, cw_neg_run, cw_neg_obj, cw_neg_blob = _close_run_with_closed_worlds(
    lambda key, idx: CW_OPEN if (idx == 1 and key["relation"] == "package") else CW_CLOSED,
    multiple_universes=True)
check("repair-cw-conflicting-negative-derives-from-a-fully-admitted-run", cw_neg_id.startswith("run3:"), cw_neg_id)
cw_neg_plan = _cw_preview(cw_neg_id, cw_neg_run, cw_neg_obj, cw_neg_blob, CW_FPS[:1], CW_DELETE)
cw_neg_derived_pre = SEL.derive(SEL.RetainedRunView(cw_neg_run, cw_neg_obj, cw_neg_blob), CW_FPS[:1], CW_DELETE)
check("repair-cw-one-dissenting-entry-defeats-the-unsafe-plan",
      cw_neg_plan["descriptor"]["applicable"] is False
      and [u["code"] for u in cw_neg_plan["descriptor"]["unmetPreconditions"]] == ["REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"],
      str(cw_neg_plan["descriptor"]["unmetPreconditions"]))
_cw_neg_remedy = cw_neg_plan["descriptor"]["unmetPreconditions"][0]["remedy"]
check("repair-cw-remedy-names-every-coordinate-and-the-coverage-identity",
      all(member + "=" in _cw_neg_remedy for member in SEL.SELECTION_ORDER_KEY)
      and "coverage2:" in _cw_neg_remedy and "entry-points:partial" in _cw_neg_remedy,
      _cw_neg_remedy[:200])
check("repair-cw-remedy-abbreviates-no-identifier",
      all(str(row[m]) in _cw_neg_remedy for m in SEL.SELECTION_ORDER_KEY
          for row in [r for r in cw_neg_derived_pre["selectedCoverage"]
                      if not r["closedWorld"]["deadCodeRepairEligible"]][:1]))
check("repair-cw-requirement-omission-does-not-bypass-the-dissent",
      all(r["relation"] != "package" for r in CW_REQS) and cw_neg_plan["descriptor"]["applicable"] is False)
# The recipe cannot narrow the evidence: a DIFFERENT requirement list selects the same records.
cw_neg_alt = _cw_preview(cw_neg_id, cw_neg_run, cw_neg_obj, cw_neg_blob, CW_FPS[:1], CW_DELETE,
                         requirements=[{"relation": "file", "minResolution": "enumerated", "completeness": "complete", "satisfied": True}])
check("repair-cw-selection-is-independent-of-evidence-requirements",
      cw_neg_alt["descriptor"]["closedWorld"] == cw_neg_plan["descriptor"]["closedWorld"]
      and cw_neg_alt["descriptor"]["applicable"] is False)

# --- CREATE-ONLY on the SAME dissenting admitted Run: no unsafe edit, so no unsafe failure,
# but the summary and therefore the identity stay deterministic.
cw_create = _cw_preview(cw_neg_id, cw_neg_run, cw_neg_obj, cw_neg_blob, CW_FPS[:1],
                        [{"path": "src/new.ts", "action": "create", "postimage": b"export const n = 1;\n"}])
check("repair-cw-create-only-is-not-failed-by-ineligibility-alone",
      cw_create["descriptor"]["applicable"] is True and cw_create["descriptor"]["unmetPreconditions"] == [],
      str(cw_create["descriptor"]["unmetPreconditions"]))
check("repair-cw-create-only-still-builds-a-deterministic-summary",
      set(cw_create["descriptor"]["closedWorld"]) == set(SEL.DISPLAY_FIELDS)
      and cw_create["repairPlanId"] == _cw_preview(cw_neg_id, cw_neg_run, cw_neg_obj, cw_neg_blob, CW_FPS[:1],
                                                   [{"path": "src/new.ts", "action": "create", "postimage": b"export const n = 1;\n"}])["repairPlanId"])
cw_create_derived = SEL.derive(cw_view, CW_FPS[:1], [{"path": "src/new.ts", "action": "create"}])
check("repair-cw-create-only-activates-no-gate",
      cw_create_derived["gateActivated"] is False and cw_create_derived["eligible"] is None)
# create + one unsafe edit: the gate is activated by the unsafe edit alone.
cw_mixed = SEL.derive(cw_view, CW_FPS[:1], [{"path": "src/new.ts", "action": "create"}, {"path": "src/index.ts", "action": "replace"}])
check("repair-cw-create-plus-unsafe-activates-the-gate", cw_mixed["gateActivated"] is True)
check("repair-cw-unsafe-set-is-exactly-delete-and-replace", set(SEL.UNSAFE_ACTIONS) == {"delete", "replace"})

# --- zero native coverage at all: the summary is still fixed and total.
cw_zero = SEL.derive(cw_view, [], [{"path": "src/new.ts", "action": "create"}])
check("repair-cw-zero-coverage-summary-is-the-published-fixed-record",
      cw_zero["selectedCoverage"] == [] and cw_zero["closedWorld"] == SEL.EMPTY_DISPLAY_SUMMARY)
check("repair-cw-empty-summary-uses-each-enum-least-closed-pole",
      all(SEL.EMPTY_DISPLAY_SUMMARY[f] == SEL.DISPLAY_ORDER[f][-1] for f in SEL.DISPLAY_ORDER)
      and SEL.EMPTY_DISPLAY_SUMMARY["deadCodeRepairEligible"] is False)

# --- unsafe path with no retained owner: typed, not vacuous.
cw_unowned = SEL.derive(cw_view, CW_FPS[:1], [{"path": "not/enumerated.ts", "action": "delete"}])
check("repair-cw-unowned-unsafe-path-is-a-typed-refusal-not-vacuous-truth",
      cw_unowned["eligible"] is False
      and cw_unowned["unownedUnsafePaths"] == ["not/enumerated.ts"]
      and any(u["code"] == SEL.CLOSED_WORLD_NOT_ESTABLISHED and "not guessed" in u["remedy"] for u in cw_unowned["unmetPreconditions"]))

# --- determinism under input enumeration order.
cw_shuffled = SEL.derive(
    SEL.RetainedRunView(cw_pos_run, dict(reversed(list(cw_pos_obj.items()))), cw_pos_blob),
    list(reversed(CW_FPS[:1])),
    [{"path": "src/index.ts", "action": "delete"}])
check("repair-cw-derivation-is-order-independent",
      canonical.canonical(cw_shuffled["selectedCoverage"]) == canonical.canonical(cw_pos_derived["selectedCoverage"])
      and cw_shuffled["closedWorld"] == cw_pos_derived["closedWorld"])
cw_order = [(r["relation"], r["resolution"], r["sourceUniverse"], r["targetUniverse"], r["subjectScopeCommitment"], r["coverageId"]) for r in cw_pos_derived["selectedCoverage"]]
check("repair-cw-selection-order-is-the-full-partition-key-then-identity", cw_order == sorted(cw_order))
check("repair-cw-dedupe-is-by-retained-identity-not-relation",
      len({r["coverageId"] for r in cw_pos_derived["selectedCoverage"]}) == len(cw_pos_derived["selectedCoverage"])
      and len({r["relation"] for r in cw_pos_derived["selectedCoverage"]}) < len(cw_pos_derived["selectedCoverage"]))

# --- display is not the gate, and the gate reads full native records.
check("repair-cw-display-summary-carries-no-dynamicdispatch-or-reasons",
      set(cw_neg_plan["descriptor"]["closedWorld"]) == set(SEL.DISPLAY_FIELDS)
      and "dynamicDispatch" not in cw_neg_plan["descriptor"]["closedWorld"]
      and "reasons" not in cw_neg_plan["descriptor"]["closedWorld"])
cw_neg_derived = SEL.derive(SEL.RetainedRunView(cw_neg_run, cw_neg_obj, cw_neg_blob), CW_FPS[:1], CW_DELETE)
check("repair-cw-gate-reads-full-seven-member-native-records",
      bool(cw_neg_derived["selectedCoverage"])
      and all(set(r["closedWorld"]) == {"deadCodeRepairEligible", "dynamicDispatch", "entryPointsRecognized",
                                        "exportsClosed", "externalConsumers", "nonliteralLoading", "reasons"}
              for r in cw_neg_derived["selectedCoverage"]))
# dynamicDispatch is never a global eligibility veto: flipping EVERY retained entry's
# dynamicDispatch to `present` on an otherwise all-eligible admitted Run changes neither the
# gate nor the display summary. Target-relative affected_targets and per-requirement
# sufficiency stay where native section 4.5/4.6 put them and are not merged into this boolean.
# MINTED by the native owner from a real dynamic-dispatch edge, never hand-edited: a
# trait-object dispatch edge is not one of the four nonliteral-loading kinds, so the owner's
# own ingredient rule still yields exportsClosed=closed and deadCodeRepairEligible=true.
CW_CLOSED_DYNAMIC = NAT.closed_world_v2(
    package_json={"private": True}, entry_points={"state": "all", "source": "explicit"},
    unresolved=[{"edgeKind": "trait-object-dynamic-dispatch", "targetScope": "module"}],
    external_consumers="none-declared")
check("repair-cw-dynamic-record-is-owner-minted-and-still-eligible",
      CW_CLOSED_DYNAMIC["dynamicDispatch"] == "present"
      and CW_CLOSED_DYNAMIC["deadCodeRepairEligible"] is True
      and CW_CLOSED_DYNAMIC["exportsClosed"] == "closed", str(CW_CLOSED_DYNAMIC))
cw_dyn_id, cw_dyn_run, cw_dyn_obj, cw_dyn_blob = _close_run_with_closed_worlds(
    lambda key, idx: CW_CLOSED_DYNAMIC, multiple_universes=True)
cw_dyn_plan = _cw_preview(cw_dyn_id, cw_dyn_run, cw_dyn_obj, cw_dyn_blob, CW_FPS[:1], CW_DELETE)
check("repair-cw-dynamicdispatch-present-is-not-a-global-eligibility-veto",
      cw_dyn_plan["descriptor"]["applicable"] is True
      and cw_dyn_plan["descriptor"]["closedWorld"] == cw_pos_plan["descriptor"]["closedWorld"],
      str(cw_dyn_plan["descriptor"]["unmetPreconditions"]))
check("repair-cw-dynamicdispatch-is-retained-on-the-native-record-it-came-from",
      all(r["closedWorld"]["dynamicDispatch"] == "present"
          for r in SEL.derive(SEL.RetainedRunView(cw_dyn_run, cw_dyn_obj, cw_dyn_blob), CW_FPS[:1], CW_DELETE)["selectedCoverage"]))

# --- a pre-selected caller record is refused by the evaluator3 profile.
try:
    WF3.repair_preview(CW_PROJECT, CW_TREE,
                       {"authority": "authoritative", "availability": "retained", "sealedAssurance": "replayable",
                        "runId": cw_neg_id, "planId": cw_neg_run["planId"],
                        "snapshotId": WF3.tree_snapshot_id(CW_PROJECT, CW_TREE),
                        "findings": CW_FPS[:1], "closedWorld": copy.deepcopy(CW_CLOSED),
                        "evidenceOrigin": "native-analysis"},
                       CW_RECIPE, CW_FPS[:1], CW_DELETE, CW_REQS, ["**"], CW_TRUST)
    check("repair-cw-evaluator3-refuses-a-caller-selected-record", False, "not refused")
except WF3.Refusal as _exc:
    check("repair-cw-evaluator3-refuses-a-caller-selected-record", _exc.detail == "REPAIR.EVIDENCE_RUN_UNAVAILABLE", _exc.detail)

# --- UNIT: unavailable retained evidence at its ACTUAL admission site. Dropping the
# evaluation-subject records makes the identity owner's close_run refuse; this control shows
# the SELECTION layer also refuses typed rather than guessing a universe.
try:
    SEL.derive(SEL.RetainedRunView(cw_pos_run, {k: v for k, v in cw_pos_obj.items() if v[0] != "evaluation-subject"}, cw_pos_blob),
               CW_FPS[:1], CW_DELETE)
    check("repair-cw-unit-missing-subject-record-refuses-typed", False, "not refused")
except SEL.RetainedEvidenceUnavailable as _exc:
    check("repair-cw-unit-missing-subject-record-refuses-typed", str(_exc).startswith("evaluation-subject:"), str(_exc))
try:
    RC.M.close_run(copy.deepcopy(cw_pos_run), {k: v for k, v in cw_pos_obj.items() if v[0] != "evaluation-subject"}, copy.deepcopy(cw_pos_blob))
    check("repair-cw-subject-join-is-guaranteed-by-run-closure", False, "close_run admitted without subject3")
except Exception as _exc:
    check("repair-cw-subject-join-is-guaranteed-by-run-closure", "EVIDENCE_UNAVAILABLE" in str(_exc), str(_exc)[:120])

# --- UNIT: a relevant universe with NO native Coverage refuses non-vacuously, and a truly
# unrelated dissenting universe does not veto. The frozen fixture builds a Coverage for every
# scope and gives both universes identical extents, so these two rules are exercised on a
# CONSTRUCTED view over the real record shapes, not on a full admitted Run. Stated, not hidden.
class _CwStubView:
    def __init__(self, snapshot_id, findings, scopes, coverage, plan=None):
        self.snapshot_id = snapshot_id
        self._f, self._s, self._c = findings, scopes, coverage
        self._plan = plan or {"cells": []}

    def enumeration_plan(self):
        return self._plan

    def matched_findings(self):
        return list(self._f)

    def subject(self, subject_id):
        return {"universe": subject_id}

    def subject_scopes(self):
        return dict(self._s)

    def coverage_records(self):
        return list(self._c)


_U_A, _U_B = "a" * 64, "b" * 64
_stub_scope = {"scope2:a": {"relation": "file", "resolution": "enumerated", "snapshotId": "snapshot2:s",
                            "sourceUniverse": _U_A, "targetUniverse": _U_A, "subjects": ["src/a.ts"]}}
_stub_cov_b = [("coverage2:b", {}, {"snapshotId": "snapshot2:s", "sourceUniverse": _U_B},
                {"key": {"relation": "file", "resolution": "enumerated", "sourceUniverse": _U_B,
                         "targetUniverse": _U_B, "subjectScopeCommitment": "sha256:" + "0" * 64},
                 "entry": {"closedWorld": dict(CW_OPEN)}})]
_stub_no_cov = _CwStubView("snapshot2:s", [], _stub_scope, _stub_cov_b)
_stub_out = SEL.derive(_stub_no_cov, [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-relevant-universe-without-coverage-refuses-non-vacuously",
      _stub_out["eligible"] is False and _stub_out["universesWithoutCoverage"] == [_U_A]
      and any("empty evidence subset is not true" in u["remedy"] for u in _stub_out["unmetPreconditions"]))
check("repair-cw-unit-unrelated-dissenting-universe-does-not-join",
      _stub_out["selectedCoverage"] == [] and _U_B not in _stub_out["relevantUniverses"])
_stub_cov_a = [("coverage2:a", {}, {"snapshotId": "snapshot2:s", "sourceUniverse": _U_A},
                {"key": {"relation": "file", "resolution": "enumerated", "sourceUniverse": _U_A,
                         "targetUniverse": _U_A, "subjectScopeCommitment": "sha256:" + "1" * 64},
                 "entry": {"closedWorld": dict(CW_CLOSED)}})]
_stub_ok = SEL.derive(_CwStubView("snapshot2:s", [], _stub_scope, _stub_cov_a + _stub_cov_b),
                      [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-unrelated-open-universe-does-not-veto-a-covered-relevant-one",
      _stub_ok["eligible"] is True and [r["coverageId"] for r in _stub_ok["selectedCoverage"]] == ["coverage2:a"])
# cross-universe: an entry MADE IN an unrelated universe ABOUT a relevant one is not joined.
_stub_cross = [("coverage2:x", {}, {"snapshotId": "snapshot2:s", "sourceUniverse": _U_B},
                {"key": {"relation": "imports", "resolution": "resolved-target", "sourceUniverse": _U_B,
                         "targetUniverse": _U_A, "subjectScopeCommitment": "sha256:" + "2" * 64},
                 "entry": {"closedWorld": dict(CW_OPEN)}})]
_stub_cross_out = SEL.derive(_CwStubView("snapshot2:s", [], _stub_scope, _stub_cov_a + _stub_cross),
                             [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-relevance-is-decided-on-sourceuniverse-only",
      _stub_cross_out["eligible"] is True and [r["coverageId"] for r in _stub_cross_out["selectedCoverage"]] == ["coverage2:a"])

# --- identity: shape and recipe unchanged; VALUES and Run identity are what move.
for _cw_schema, _cw_major in ((WF / "repair.schema.json", 1), (E3 / "repair.schema.json", 2)):
    _cw_doc = canonical.parse(_cw_schema.read_bytes())["$defs"]["RepairPlanDescriptor"]
    check("repair-cw-descriptor-shape-unchanged-major" + str(_cw_major),
          _cw_doc["properties"]["schemaMajor"]["const"] == _cw_major
          and _cw_doc["properties"]["closedWorld"]["required"] == list(SEL.DISPLAY_FIELDS)
          and _cw_doc["properties"]["closedWorld"]["additionalProperties"] is False
          and "closedWorld" in _cw_doc["required"])
check("repair-cw-identity-recipe-unchanged-values-may-move",
      cw_pos_plan["repairPlanId"].startswith("repairplan2:")
      and cw_neg_plan["repairPlanId"].startswith("repairplan2:")
      and cw_pos_plan["repairPlanId"] != cw_neg_plan["repairPlanId"]
      and cw_pos_plan["descriptor"]["evidenceRunId"] != cw_neg_plan["descriptor"]["evidenceRunId"])
check("repair-cw-no-equal-id-claim-across-different-runs",
      cw_pos_plan["descriptor"]["evidenceRunId"] == cw_pos_id and cw_neg_plan["descriptor"]["evidenceRunId"] == cw_neg_id)
# Identical descriptor inputs over the SAME Run mint the same id; that is the only equality claimed.
check("repair-cw-same-inputs-same-run-mint-the-same-id",
      _cw_preview(cw_neg_id, cw_neg_run, cw_neg_obj, cw_neg_blob, CW_FPS[:1], CW_DELETE)["repairPlanId"] == cw_neg_plan["repairPlanId"])
# Preview is not authorization.
check("repair-cw-preview-is-not-authorization",
      "applicable" in cw_pos_plan["descriptor"] and "authorization" not in cw_pos_plan
      and "securityAuthorizationRef" not in cw_pos_plan["descriptor"])

check("repair-cw-every-record-used-here-obeys-native-4-5-true-only",
      all(_obeys_section_4_5(r) for r in (CW_CLOSED, CW_OPEN, CW_CLOSED_DYNAMIC))
      and all(_obeys_section_4_5(r["closedWorld"]) for r in cw_pos_derived["selectedCoverage"])
      and all(_obeys_section_4_5(r["closedWorld"]) for r in cw_neg_derived["selectedCoverage"]))

# ---------------------------------------------------------------- RRS-A1: the omitted census
# FULL ADMITTED ASYMMETRIC RUN. The first universe binds only on the `inventory` cell and owns
# the unsafe path through its FILE extent; the second binds only on the symbol-kind `syntax`
# cell and owns the same path through its retained SYMBOL extent, with NO source-path subject
# scope of any kind. The second universe's Coverage dissents. A source-path-scope-only owner law
# misses that owner. The empty-target derivation below isolates path ownership only; it is
# not a lawful repair request (targets requires minItems=1). The sole matched finding belongs
# to the symbol universe, so using it as a target already reaches that universe under the
# earlier target-occurrence join. This control does not prove a lawful old-preview bypass.
CW_SYMBOL_ROWS = [{"nativeSubjectId": "ts-symbol:src/index.ts#x", "qualifiedName": "x"}]
cw_asym_id, cw_asym_run, cw_asym_obj, cw_asym_blob = _close_run_with_closed_worlds(
    lambda key, idx: CW_OPEN if key["relation"] == "declares" else CW_CLOSED,
    multiple_universes=True, symbol_rows=CW_SYMBOL_ROWS, symbol_only_second_program=True)
check("repair-cw-asymmetric-control-is-a-fully-admitted-run", cw_asym_id.startswith("run3:"), cw_asym_id)
cw_asym_view = SEL.RetainedRunView(cw_asym_run, cw_asym_obj, cw_asym_blob)
cw_asym_plan = cw_asym_view.enumeration_plan()
check("repair-cw-asymmetric-plan-binds-each-universe-to-one-cell-only",
      [(c["capabilityId"], [b["universe"] for b in c["programBindings"]]) for c in cw_asym_plan["cells"]]
      == [("inventory", [cw_asym_plan["cells"][0]["programBindings"][0]["universe"]]),
          ("syntax", [cw_asym_plan["cells"][1]["programBindings"][0]["universe"]])]
      and cw_asym_plan["cells"][0]["programBindings"][0]["universe"] != cw_asym_plan["cells"][1]["programBindings"][0]["universe"])
CW_SYMBOL_UNIVERSE = cw_asym_plan["cells"][1]["programBindings"][0]["universe"]
check("repair-cw-symbol-owner-has-no-source-path-scope-at-all",
      all(sc["relation"] not in SEL.SOURCE_PATH_RELATIONS
          for sc in cw_asym_view.subject_scopes().values()
          if sc["sourceUniverse"] == CW_SYMBOL_UNIVERSE),
      str(sorted({sc["relation"] for sc in cw_asym_view.subject_scopes().values()
                  if sc["sourceUniverse"] == CW_SYMBOL_UNIVERSE})))
cw_asym_witness = SEL.source_path_scope_witnesses(cw_asym_view, ["src/index.ts"])
cw_asym_derived = SEL.derive(cw_asym_view, [], CW_DELETE)
check("repair-cw-source-path-only-law-omits-the-symbol-owner",
      CW_SYMBOL_UNIVERSE not in cw_asym_witness
      and CW_SYMBOL_UNIVERSE in cw_asym_derived["ownership"]["censusUniverses"],
      str(sorted(cw_asym_witness)))
check("repair-cw-census-recovers-the-symbol-owner-and-defeats-the-plan",
      cw_asym_derived["eligible"] is False
      and CW_SYMBOL_UNIVERSE in cw_asym_derived["relevantUniverses"]
      and any("relation=declares" in u["remedy"] for u in cw_asym_derived["unmetPreconditions"]),
      str(cw_asym_derived["unmetPreconditions"])[:220])
check("repair-cw-symbol-owner-is-witnessed-by-its-symbol-extent",
      any(s["via"] == "unsafe-edit-path" and s["extentKinds"] == ["symbol"]
          for s in cw_asym_derived["universeSources"][CW_SYMBOL_UNIVERSE]),
      str(cw_asym_derived["universeSources"][CW_SYMBOL_UNIVERSE]))
# Selection-hook integration through the synthetic host projection, with actual nonempty targets.
CW_ASYM_FPS = sorted({f["fingerprint"] for _, f in cw_asym_view.matched_findings()})
check("repair-cw-asymmetric-projection-uses-actual-nonempty-targets", bool(CW_ASYM_FPS))
cw_asym_plan_out = _cw_preview(cw_asym_id, cw_asym_run, cw_asym_obj, cw_asym_blob, CW_ASYM_FPS, CW_DELETE)
check("repair-cw-asymmetric-selection-refuses-through-synthetic-host-projection",
      cw_asym_plan_out["descriptor"]["applicable"] is False
      and [u["code"] for u in cw_asym_plan_out["descriptor"]["unmetPreconditions"]] == ["REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"],
      str(cw_asym_plan_out["descriptor"]["unmetPreconditions"])[:200])
# UNRELATED PATH on that same Run: no selected program's census contains it, so it is typed
# unresolved rather than silently owned by the file-extent universe.
cw_asym_unrelated = SEL.derive(cw_asym_view, [], [{"path": "not/enumerated.ts", "action": "delete"}])
check("repair-cw-asymmetric-unrelated-path-is-typed-not-vacuous",
      cw_asym_unrelated["unownedUnsafePaths"] == ["not/enumerated.ts"]
      and cw_asym_unrelated["eligible"] is False)
# A path in the FILE extent but NOT in the symbol program's extent keeps that program unrelated.
cw_asym_fileonly = SEL.derive(cw_asym_view, [], [{"path": "README.md", "action": "delete"}])
check("repair-cw-selected-program-without-the-path-in-its-census-stays-unrelated",
      CW_SYMBOL_UNIVERSE not in cw_asym_fileonly["ownership"]["censusUniverses"]
      and cw_asym_fileonly["ownership"]["censusUniverses"] != [],
      str(cw_asym_fileonly["ownership"]["censusUniverses"]))
check("repair-cw-file-extent-is-not-treated-as-the-symbol-program-extent",
      cw_asym_fileonly["eligible"] is True and cw_asym_derived["eligible"] is False)

# --- UNIT: unavailable and candidate-only bindings, and unselected exclusion. The frozen graph
# fixture builds no unavailable or candidate-only binding, so these exercise the published rule
# on a constructed plan over the real record shapes. Their admissibility was separately
# confirmed against the enumeration owner's own admit_enumeration and is reported in the author
# handoff; it is NOT claimed here as a full Run.
_CW_UA, _CW_UB = "a" * 64, "b" * 64


def _cw_plan(bindings, capability="inventory", kinds=("file",)):
    return {"cells": [{"capabilityId": capability, "kinds": list(kinds),
                       "programBindings": list(bindings)}]}


def _cw_binding(ordinal, universe, paths, kind="file", status="selected", **extra):
    row = {"ordinal": ordinal, "provenance": "explicit-plan-selection",
           "enumerator": {"status": status, "closureId": "closure2:" + "e" * 64},
           "universe": universe, "programEntry": None,
           "extents": [{"kind": kind, "paths": list(paths)}]}
    row.update(extra)
    return row


_cw_cov_a = [("coverage2:" + "1" * 64, {}, {"snapshotId": "snapshot2:s", "sourceUniverse": _CW_UA},
              {"key": {"relation": "file", "resolution": "enumerated", "sourceUniverse": _CW_UA,
                       "targetUniverse": _CW_UA, "subjectScopeCommitment": "sha256:" + "1" * 64},
               "entry": {"closedWorld": dict(CW_CLOSED)}})]
# UNAVAILABLE selected binding overlapping an otherwise eligible owner.
_cw_unavail = SEL.derive(_CwStubView(
    "snapshot2:s", [], {}, _cw_cov_a,
    plan=_cw_plan([_cw_binding(0, _CW_UA, ["src/a.ts"]),
                   _cw_binding(1, None, ["src/a.ts"], deficiency="provider-unavailable",
                               nativeCause=None)])),
    [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-unavailable-binding-does-not-vanish-behind-a-closed-owner",
      _cw_unavail["eligible"] is False
      and len(_cw_unavail["unresolvedOwnership"]) == 1
      and _cw_unavail["relevantUniverses"] == [_CW_UA]
      and any("UNAVAILABLE" in u["remedy"] and "does not discharge it" in u["remedy"]
              for u in _cw_unavail["unmetPreconditions"]),
      str(_cw_unavail["unmetPreconditions"])[:220])
# UNSELECTED binding is not a selected program and is never inferred.
_cw_unselected = SEL.derive(_CwStubView(
    "snapshot2:s", [], {}, _cw_cov_a,
    plan=_cw_plan([_cw_binding(0, _CW_UA, ["src/a.ts"]),
                   _cw_binding(1, None, ["src/a.ts"], status="unselected",
                               deficiency="provider-unavailable", nativeCause=None)])),
    [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-unselected-binding-is-never-inferred-as-an-owner",
      _cw_unselected["eligible"] is True and _cw_unselected["unresolvedOwnership"] == []
      and _cw_unselected["relevantUniverses"] == [_CW_UA])
# CANDIDATE-ONLY selected binding: candidateSourcePaths is a real census.
_cw_cand_plan = {"cells": [{"capabilityId": "clones-near", "kinds": [], "programBindings": [
    dict(_cw_binding(0, _CW_UB, [], kind="symbol"), extents=[],
         candidateSourcePaths=["src/a.ts"])]},
    {"capabilityId": "inventory", "kinds": ["file"], "programBindings": [
        _cw_binding(0, _CW_UA, ["src/a.ts"])]}]}
_cw_cand = SEL.derive(_CwStubView("snapshot2:s", [], {}, _cw_cov_a, plan=_cw_cand_plan),
                      [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-candidate-source-paths-are-an-owner-census",
      _CW_UB in _cw_cand["ownership"]["censusUniverses"]
      and any(s["extentKinds"] == ["candidateSourcePaths"]
              for s in _cw_cand["universeSources"][_CW_UB])
      and _cw_cand["eligible"] is False
      and _CW_UB in _cw_cand["universesWithoutCoverage"])
# MULTIPLE owners of one path, both available: both must be eligible.
_cw_cov_b = [("coverage2:" + "2" * 64, {}, {"snapshotId": "snapshot2:s", "sourceUniverse": _CW_UB},
              {"key": {"relation": "file", "resolution": "enumerated", "sourceUniverse": _CW_UB,
                       "targetUniverse": _CW_UB, "subjectScopeCommitment": "sha256:" + "2" * 64},
               "entry": {"closedWorld": dict(CW_OPEN)}})]
_cw_multi = SEL.derive(_CwStubView(
    "snapshot2:s", [], {}, _cw_cov_a + _cw_cov_b,
    plan=_cw_plan([_cw_binding(0, _CW_UA, ["src/a.ts"]), _cw_binding(1, _CW_UB, ["src/a.ts"])])),
    [], [{"path": "src/a.ts", "action": "delete"}])
check("repair-cw-unit-multiple-owners-all-must-be-eligible",
      _cw_multi["relevantUniverses"] == sorted([_CW_UA, _CW_UB])
      and _cw_multi["eligible"] is False)

# --- RRS-A2: display sentinel, absence, ordering and remedy discrimination.
check("repair-cw-sentinel-is-the-least-closed-five-field-record-not-all-unknown",
      SEL.EMPTY_DISPLAY_SUMMARY == {"deadCodeRepairEligible": False, "exportsClosed": "unknown",
                                    "entryPointsRecognized": "none", "nonliteralLoading": "present",
                                    "externalConsumers": "unknown"}
      and sorted(k for k, v in SEL.EMPTY_DISPLAY_SUMMARY.items() if v == "unknown")
      == ["exportsClosed", "externalConsumers"]
      and len([v for v in SEL.EMPTY_DISPLAY_SUMMARY.values() if v != "unknown"]) == 3)
_cw_module_text = (HERE / "repair_closed_world_selection.v1.py").read_text()
check("repair-cw-no-display-member-is-labelled-authoritative",
      "authoritative part" not in _cw_module_text
      and "NO MEMBER OF THIS RECORD IS AUTHORITATIVE" in _cw_module_text)
# A relevant universe with no Coverage now shows in the DISPLAY as well as in eligibility.
check("repair-cw-missing-relevant-universe-is-folded-into-the-display",
      _cw_cand["closedWorld"]["deadCodeRepairEligible"] is False
      and _cw_cand["closedWorld"]["entryPointsRecognized"] == "none"
      and _cw_cand["closedWorld"]["nonliteralLoading"] == "present")
check("repair-cw-display-absence-does-not-make-it-a-native-record",
      set(_cw_cand["closedWorld"]) == set(SEL.DISPLAY_FIELDS))
check("repair-cw-published-order-is-six-members-utf8",
      SEL.SELECTION_ORDER_KEY == ("relation", "resolution", "sourceUniverse", "targetUniverse",
                                  "subjectScopeCommitment", "coverageId")
      and "UTF-8" in _cw_module_text)
# CONFORMING remedy discrimination. `file` is universeRule same-only, so two lawful file records
# keep source==target and differ on the subject-scope commitment and the coverage identity. A
# cross-universe key is exercised on `imports`, which the registry permits (admitted-target).
_cw_same = [
    {"coverageId": "coverage2:" + "3" * 64, "relation": "file", "resolution": "enumerated",
     "sourceUniverse": _CW_UA, "targetUniverse": _CW_UA,
     "subjectScopeCommitment": "sha256:" + "3" * 64, "closedWorld": dict(CW_OPEN)},
    {"coverageId": "coverage2:" + "4" * 64, "relation": "file", "resolution": "enumerated",
     "sourceUniverse": _CW_UA, "targetUniverse": _CW_UA,
     "subjectScopeCommitment": "sha256:" + "4" * 64, "closedWorld": dict(CW_OPEN)},
]
check("repair-cw-remedy-distinguishes-two-same-only-file-records",
      SEL.record_coordinates(_cw_same[0]) != SEL.record_coordinates(_cw_same[1])
      and all(r["sourceUniverse"] == r["targetUniverse"] for r in _cw_same))
_cw_cross = dict(_cw_same[0], relation="imports", resolution="resolved-target",
                 targetUniverse=_CW_UB, coverageId="coverage2:" + "5" * 64)
check("repair-cw-cross-universe-example-uses-a-relation-that-permits-it",
      SEL._REGISTRY["relations"]["imports"]["universeRule"] == "admitted-target"
      and SEL._REGISTRY["relations"]["file"]["universeRule"] == "same-only"
      and SEL.record_coordinates(_cw_cross) != SEL.record_coordinates(_cw_same[0]))

REPAIR_CLOSED_WORLD_STANDING = {
    "standing": "AUTHOR_PENDING_REVIEW. Focused controls for the repair closed-world SELECTION law only.",
    "controlsUsingFullyAdmittedRunEvidence": [
        "repair-cw-all-agreeing-entries-admit-the-unsafe-plan (positive)",
        "repair-cw-one-dissenting-entry-defeats-the-unsafe-plan (conflicting negative)",
        "repair-cw-asymmetric-control-is-a-fully-admitted-run",
        "repair-cw-source-path-only-law-omits-the-symbol-owner",
        "repair-cw-census-recovers-the-symbol-owner-and-defeats-the-plan",
        "repair-cw-asymmetric-selection-refuses-through-synthetic-host-projection",
        "repair-cw-selected-program-without-the-path-in-its-census-stays-unrelated",
        "repair-cw-file-extent-is-not-treated-as-the-symbol-program-extent",
        "repair-cw-requirement-omission-does-not-bypass-the-dissent",
        "repair-cw-create-only-is-not-failed-by-ineligibility-alone",
        "repair-cw-one-fingerprint-matched-in-two-universes-contributes-both",
        "repair-cw-multi-owner-path-keeps-every-owning-universe",
        "repair-cw-dynamicdispatch-present-is-not-a-global-eligibility-veto",
        "repair-cw-evaluator3-refuses-a-caller-selected-record",
        "repair-cw-witnesses-are-redundant-in-a-symmetric-run",
    ],
    "projectionScope": "The listed controls read native evidence from fully admitted Runs. _cw_preview uses a separate synthetic host adapter and inherited major-1 descriptor constructor; its outputs are not admitted current RepairPlanDescriptors. Pure derive(..., targets=[], ...) calls isolate path ownership only and are not lawful repair requests.",
    "unitControls": [
        "repair-cw-unit-relevant-universe-without-coverage-refuses-non-vacuously",
        "repair-cw-unit-unrelated-dissenting-universe-does-not-join",
        "repair-cw-unit-unrelated-open-universe-does-not-veto-a-covered-relevant-one",
        "repair-cw-unit-relevance-is-decided-on-sourceuniverse-only",
        "repair-cw-unit-missing-subject-record-refuses-typed",
        "repair-cw-unit-unavailable-binding-does-not-vanish-behind-a-closed-owner",
        "repair-cw-unit-unselected-binding-is-never-inferred-as-an-owner",
        "repair-cw-unit-candidate-source-paths-are-an-owner-census",
        "repair-cw-unit-multiple-owners-all-must-be-eligible",
    ],
    "ownershipLaw": {
        "census": "retained EnumerationPlanV1 selected bindings: each binding's own extents[] per kind plus candidateSourcePaths",
        "availableBinding": "non-null universe becomes a relevant universe",
        "unavailableSelectedBinding": "universe=null with a retained extent containing an unsafe path is a TYPED unresolved-ownership refusal; another owner being closed does not discharge it",
        "unselectedBinding": "never inferred as an owner",
        "sourcePathScopes": "an ADDITIONAL retained witness, measured for redundancy, never an owner-completeness certificate",
        "reachabilityOfTheOmission": "confirmed at the enumeration owner's own admit_enumeration for the symbol-only, unavailable-binding and candidate-only shapes, and separately as a FULL ADMITTED Run for the symbol-only shape (repair-cw-asymmetric-control-is-a-fully-admitted-run)",
    },
    "notClaimed": [
        "a lawful old-preview bypass from the asymmetric empty-target control; its valid target already reaches the dissenting symbol universe",
        "current RepairPlanDescriptor admission, real-Run snapshot/project/preimage joins, or sufficiency derivation from the synthetic host projection",
        "native producer qualification: every ClosedWorldV2 here is a synthetic producer observation minted by the native owner's own closed_world_v2 helper",
        "a full product repair, an apply, or any authorization: preview is a Query-class step",
        "real extraction, compiler, provider or repository observation",
        "that the historical major-1 profile is corrected; it is preserved and labelled",
        "any repairPlanId equality across different evidenceRunIds",
    ],
    "disclosedLimits": [
        "the unavailable-binding, unselected-binding and candidate-only shapes are UNIT controls over constructed plans; their admissibility was confirmed against the enumeration owner's own admit_enumeration but they are not full Runs here",
        "only the fixture's two syntax universes are exercised; no Rust or TypeScript universe interaction is, so Rust sourceUnitOwnership multi-target ownership is covered by rule and not by execution",
        "ClosedWorldV2 has no unknown member for entryPointsRecognized or nonliteralLoading, so the empty display value is the least-closed pole of each enum and is labelled a display SENTINEL; root resolved that the enum stays as it is",
        "the asymmetric full-Run control uses the authorized default-off fixture option symbol_only_second_program; with it unset every existing caller is byte-identical",
    ],
}

POLICY_CLARIFICATION = {
    "standing": "Clarification of the v8 policy-derivation peer review. Historical grok-workflow-projection.v8/policy-derivation-peer-review.v8.md is retained and not overwritten.",
    "identifierDomain": "policy-derivation3",
    "corrections": [
        "derive_policy_result first calls replay, which invokes owner closure admission, reconstructs Plan policy/waiver/import blobs, and compares the complete proof. PolicyDigest/waiverDigest/waivedFindingIds joins are inherited transitively; they are not a new gap.",
        "Descriptor planId and proofBundleId transitively bind snapshot, detector/emission, scope, and results. Redundant copies of those fields are not required on policy-derivation3.",
        "The API explicitly projects an admitted Run. It is not a substitute-policy operation and must not be tested as one.",
        "Root will add a second real Plan control. Broadening remint-field mirror tests is not necessary without a demonstrated failure.",
        "Remaining standing: this projector does not mint policy-derivation3; root remains the owner. The API is not an E1/E3 pivot.",
    ],
}
DECLARED_COMPATIBLE = {
    "normative": "workflows-and-surfaces.md §2: current detector signed manifest lists baseline closure2 as exactly semantically compatible at the same major; fresh host resolves pivot closures from retained generation, installed signed release with the same closure2, or signed closureBundle, all under current trust.",
    "implemented": "DetectorManifestV1 is the unsigned listing at reserved closure.tree path .opensip/detector-compatibility.json. It is not closure.manifestDigest (DR-103 component-manifest body). compare_admitted fills compatibleWith only from that tree listing when host.closures[id].trust==admitted and trustOrigin is a trust-trio member. Parse hashes exact retained listing bytes against the tree Blob sha256/bytes. Path absent is no declaration; empty compatibleClosures is a complete listing; present malformed/unrecognized/missing/hash-mismatch refuses. Caller compatibleWith maps are refused. This helper does not verify signatures (host TCB already admitted the same closure2).",
    "securityOwnedRemainder": "Signature envelope, release catalog, DR-103 platforms[]/RJ-3, and closureBundle verification remain security/identity. Workflows consume the admitted same-closure2 tree commitment plus host trust-trio receipt.",
    "hostReceipt": "Host-only projection after TCB admission: closureId, componentManifestDigest, listing {path, sha256, bytes}, trustOrigin (retained-generation | installed-signed-release | signed-closure-bundle), compatibleClosures, tree, platform, protocolMajor. Request maps never assert trust.",
    "standing": "Typed owner schema under workflows/evaluator3; listing is a reserved tree file on the admitted same closure2. Not a cryptographic verifier.",
}
INVENTORY_JOINS = {
    "historicalInstance": "workflows/command-inventory.v1.json schemaMajor 1, json renderer version 2 / envelope major 2, golden pin schemaMajor 2",
    "currentInstance": "workflows/command-inventory.v3.json schemaMajor 3, json renderer version 3 / CommandEnvelope major 3, golden pin schemaMajor 3, validated against evaluator3 command-inventory:3",
    "remainingJoins": [
        "v1 historical instance remains schemaMajor 1 and is not the evaluator3 inventory:3 instance",
        "v1 and v3 share command names; v3 renderer/envelope majors are the selected profile",
        "parityFields token 'findings' vs FindingSurface / sarif-adapter:2 still names the same analysis projection",
        "execution-inputs manifest is required on a public admitted Run; missing capture is EVALUATION.PROJECTION_INPUT_INCOMPLETE",
        "physical store pointer inventories are excluded from semantic execution-inputs identity (main Grok v6); this projector does not join retainedObjectKeys/retainedBlobDigests",
        "sidecar/candidate parent locators are stripped; incoming-search expectedInventoryRefs expand to stripped inventory bodies",
    ],
}

# ----------------------------------------------------------------------------- consumer24 corrections (root-selected M4/S7/S5/S6/A13/A11/A12/A8/A14)
def _remint_baseline(artifact, mutate):
    out = copy.deepcopy(artifact)
    mutate(out["descriptor"])
    out["baselineId"] = P.wid("baseline2", "workflow.baseline", out["descriptor"])
    return out


def _m4_rename(desc):
    for row in desc["detectorClosure"]:
        row["detectorId"] = "renamed-detector"
    for e in desc["entries"]:
        e["detectorId"] = "renamed-detector"


def _m4_entry_outside(desc):
    for e in desc["entries"]:
        e["detectorId"] = "not-in-closure"


def _m4_duplicate_row(desc):
    row = copy.deepcopy(desc["detectorClosure"][0])
    row["semanticsMajor"] += 1
    desc["detectorClosure"].append(row)


def _m4_major(desc):
    for row in desc["detectorClosure"]:
        row["semanticsMajor"] += 1


_m4_art = P.adopt_admitted_baseline_v3(*scope_graph, CUSTODY)
_m4_desc = _m4_art["descriptor"]
check(
    "m4-admitted-detector-rows-are-emission-contributions",
    all(r["detectorId"] == r["contributionId"] for r in _m4_desc["detectorClosure"])
    and {e["detectorId"] for e in _m4_desc["entries"]} <= {r["detectorId"] for r in _m4_desc["detectorClosure"]}
    and {r["detectorId"] for r in _m4_desc["detectorClosure"]} == {row["contributionId"] for row in scope_view["emission"]["rules"]},
)
check("m4-admitted-baseline-admits", P.verify_baseline_artifact_v3(_m4_art) is True)
_m4_renamed = _remint_baseline(_m4_art, _m4_rename)
must_valid("m4-reminted-rename-is-schema-valid-so-schema-alone-cannot-decide", U + "baseline:2", _m4_renamed)
check("m4-reminted-rename-has-self-consistent-new-baselineId", _m4_renamed["baselineId"] != _m4_art["baselineId"])
reject("m4-reminted-rename-refused-at-baseline-admission", lambda: P.verify_baseline_artifact_v3(_m4_renamed), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
_m4_stale = copy.deepcopy(_m4_art)
_m4_rename(_m4_stale["descriptor"])
reject("m4-stale-hash-rename-is-artifact-corruption", lambda: P.verify_baseline_artifact_v3(_m4_stale), "CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT")
reject("m4-reminted-entry-detector-outside-closure-refused", lambda: P.verify_baseline_artifact_v3(_remint_baseline(_m4_art, _m4_entry_outside)), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
_m4_dup = _remint_baseline(_m4_art, _m4_duplicate_row)
must_valid("m4-reminted-conflicting-contribution-row-is-schema-valid", U + "baseline:2", _m4_dup)
reject("m4-reminted-conflicting-contribution-row-refused", lambda: P.verify_baseline_artifact_v3(_m4_dup), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
reject("m4-reminted-detector-major-disagreeing-with-rule-refused", lambda: P.verify_baseline_artifact_v3(_remint_baseline(_m4_art, _m4_major)), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")

# S7: presence knowledge over full owner-admitted comparisons (retained graphs replayed through close_run).
_S7_X1 = {"nativeSubjectId": "symbol:x1"}
_S7_X2 = {"nativeSubjectId": "symbol:x2", "signatureTokens": ["function", "x", "(", "number", ")"]}


def _s7_host(art, graph):
    h = host_from_graph({"runId": art["descriptor"]["runId"]}, graph[1])
    h["pivotRunId"] = art["descriptor"]["runId"]
    return h


def _s7_compare(art, graph, host_):
    return P.compare_admitted_v3(baseline_artifact=art, current_run=graph[0], current_objects=graph[1], current_blobs=graph[2], host=host_, profile_name="code-regression")


def _s7_entry(res, fp):
    return next(e for e in res["descriptor"]["entries"] if e["fingerprint"] == fp)


for _gate in (True, False):
    _tag = "gating" if _gate else "nongating"
    _b = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, gate=_gate)
    _art = P.adopt_admitted_baseline_v3(*_b, CUSTODY)
    _h = _s7_host(_art, _b)
    _fps = [e["fingerprint"] for e in _art["descriptor"]["entries"]]
    check("s7-%s-baseline-records-complete-absence-knowledge" % _tag, len(_fps) == 2 and all(r["absenceKnowledge"] == "complete-hit-set" for r in _art["descriptor"]["ruleCoverage"] if r["enabled"]))
    _complete = RC.positive(symbol_rows=[_S7_X2], scope_document=SCOPE_ALL, gate=_gate)
    _kept = {o["finding"]["fingerprint"] for o in P.project_admitted_run_v3(*_complete)["occurrences"]}
    _removed = [fp for fp in _fps if fp not in _kept]
    _res = _s7_compare(_art, _complete, _h)
    must_valid("s7-%s-complete-removal-comparison-schema" % _tag, U + "comparison:2", cmp_obj(_res))
    check(
        "s7-%s-complete-enumeration-row-removal-is-lawful-code-fixed" % _tag,
        len(_removed) == 1 and _s7_entry(_res, _removed[0])["classification"] == "CODE-FIXED" and _s7_entry(_res, _removed[0])["presence"]["E4"] is False,
        [(_s7_entry(_res, fp)["classification"], _s7_entry(_res, fp)["presence"]["E4"]) for fp in _fps],
    )
    for _name, _opts in (("partial-inventory", dict(symbol_rows=[_S7_X2], symbol_state="partial")), ("budget-exhausted", dict(symbol_rows=[_S7_X1, _S7_X2], budget_limit=1))):
        _cur = RC.positive(scope_document=SCOPE_ALL, gate=_gate, **_opts)
        _curv = P.project_admitted_run_v3(*_cur)
        _rid = _curv["policy"]["rules"][0]["ruleId"]
        _res = _s7_compare(_art, _cur, _h)
        must_valid("s7-%s-%s-comparison-schema" % (_tag, _name), U + "comparison:2", cmp_obj(_res))
        _ents = [_s7_entry(_res, fp) for fp in _fps]
        check(
            "s7-%s-%s-unknown-current-absence-is-indeterminate-not-code-fixed" % (_tag, _name),
            all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "current-absence-unknown" and e["presence"]["E4"] is None and e["gates"] is False for e in _ents),
            [(e["classification"], e.get("indeterminateReason"), e["presence"]["E4"]) for e in _ents],
        )
        check(
            "s7-%s-%s-current-law-equals-pivot-law" % (_tag, _name),
            P.axis_presence_knowledge(_curv)["prove_absence"][_rid] is False
            and P.fingerprint_absence_known(_curv, P.presence_absence_extent(_curv), _rid, None) is False,
        )
        if _gate:
            check(
                "s7-gating-%s-verdict-indeterminate-with-independent-deficiencies" % _name,
                _res["descriptor"]["verdict"] == "indeterminate" and bool(_res["descriptor"]["ruleDeficiencies"] or _res["descriptor"]["currentExecutionDeficiencies"]),
                _res["descriptor"]["verdict"],
            )
        else:
            check("s7-nongating-%s-never-fails" % _name, _res["descriptor"]["verdict"] in ("pass", "indeterminate"), _res["descriptor"]["verdict"])
    try:
        _ub = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, gate=_gate, budget_limit=1)
        _uart = P.adopt_admitted_baseline_v3(*_ub, CUSTODY)
        check("s7-%s-budget-exhausted-baseline-records-unknown-absence" % _tag, _uart["descriptor"]["entries"] == [] and all(r["absenceKnowledge"] == "unknown" for r in _uart["descriptor"]["ruleCoverage"]))
        _ures = _s7_compare(_uart, _b, _s7_host(_uart, _ub))
        must_valid("s7-%s-unknown-baseline-comparison-schema" % _tag, U + "comparison:2", cmp_obj(_ures))
        check(
            "s7-%s-hit-over-unknown-baseline-is-not-code-net-new" % _tag,
            bool(_ures["descriptor"]["entries"])
            and all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "baseline-absence-unknown" and e["presence"]["B"] is None for e in _ures["descriptor"]["entries"])
            and _ures["descriptor"]["verdict"] != "fail",
            [(e["classification"], e.get("indeterminateReason")) for e in _ures["descriptor"]["entries"]],
        )
    except Exception as _exc:
        check("s7-%s-unknown-baseline-control-executed" % _tag, False, type(_exc).__name__ + ": " + str(_exc)[:200])

_kf_new = occurrence("s7-known-new", path="src/new.ts")
_kf_old = occurrence("s7-known-old", path="src/old.ts")
_kf_art = adopt(P.project_baseline_entries([_kf_old], {"r": BINDING}, []))


def _kf_compare(cur):
    res = P.compare_v3(baseline_artifact=_kf_art, current=cur, host=host(), profile_name="code-regression", current_detectors=detectors())
    return res, {e["fingerprint"]: e for e in res["descriptor"]["entries"]}


_kf_res, _kf_e = _kf_compare(make_current(occurrences=[_kf_new], rule_results=[rr(outcome="fail", enum=incomplete_enum(), findings=[_kf_new["findingId"]])]))
check(
    "s7-known-code-net-new-failure-dominates-unknown-current-absence",
    _kf_res["descriptor"]["verdict"] == "fail"
    and _kf_e[_kf_new["finding"]["fingerprint"]]["classification"] == "CODE-NET-NEW"
    and _kf_e[_kf_old["finding"]["fingerprint"]].get("indeterminateReason") == "current-absence-unknown",
    [(e["classification"], e.get("indeterminateReason")) for e in _kf_e.values()],
)
_kc_res, _kc_e = _kf_compare(make_current(occurrences=[_kf_new], rule_results=[rr(outcome="fail", findings=[_kf_new["findingId"]])]))
check("s7-complete-current-root-proofs-prove-code-fixed", _kc_e[_kf_old["finding"]["fingerprint"]]["classification"] == "CODE-FIXED" and _kc_e[_kf_old["finding"]["fingerprint"]]["presence"]["E4"] is False)
_kn_res, _kn_e = _kf_compare(make_current(occurrences=[_kf_new], rule_results=[rr(outcome="fail", findings=[_kf_new["findingId"]])], knowledge=False))
check("s7-current-without-admitted-root-proofs-has-no-absence-knowledge", _kn_e[_kf_old["finding"]["fingerprint"]].get("indeterminateReason") == "current-absence-unknown")
_kn_unknown = _kn_e[_kf_old["finding"]["fingerprint"]]
must_valid("s7-entry-with-null-e4-and-absence-reason-admitted", U + "comparison:2#/$defs/Entry", _kn_unknown)
must_invalid("s7-indeterminate-entry-without-reason-refused", U + "comparison:2#/$defs/Entry", {k: v for k, v in _kn_unknown.items() if k != "indeterminateReason"})
must_invalid("s7-unknown-reason-outside-closed-enum-refused", U + "comparison:2#/$defs/Entry", dict(_kn_unknown, indeterminateReason="absence-unknown"))

# S7 non-selection: a side that does not select the fingerprint cannot emit it; attributed to policy/scope, never CODE-FIXED.
_ns_base = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL)
_ns_art = P.adopt_admitted_baseline_v3(*_ns_base, CUSTODY)
_ns_host = _s7_host(_ns_art, _ns_base)
_ns_disabled = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, enabled=False)
try:
    _ns_with_e1 = P.compare_admitted_v3(baseline_artifact=_ns_art, current_run=_ns_disabled[0], current_objects=_ns_disabled[1], current_blobs=_ns_disabled[2], host=_ns_host, profile_name="code-regression", pivot_runs={"E1": _ns_base})
    must_valid("s7-disabled-current-with-bound-e1-comparison-schema", U + "comparison:2", cmp_obj(_ns_with_e1))
    check(
        "s7-disabled-current-rule-with-bound-e1-is-policy-delta-not-code-fixed",
        bool(_ns_with_e1["descriptor"]["entries"])
        and all(e["classification"] == "POLICY-DELTA" and e["direction"] == "vanished" and e["presence"]["E4"] is False and e["presence"]["E1"] is True for e in _ns_with_e1["descriptor"]["entries"]),
        [(e["classification"], e.get("indeterminateReason"), e["presence"]) for e in _ns_with_e1["descriptor"]["entries"]],
    )
except Exception as _ns_exc:
    check("s7-disabled-current-rule-with-bound-e1-is-policy-delta-not-code-fixed", False, type(_ns_exc).__name__ + ": " + str(_ns_exc)[:200])
_ns_without = P.compare_admitted_v3(baseline_artifact=_ns_art, current_run=_ns_disabled[0], current_objects=_ns_disabled[1], current_blobs=_ns_disabled[2], host=_ns_host, profile_name="code-regression")
check(
    "s7-disabled-current-rule-without-e1-is-pivot-unavailable-not-code-fixed",
    bool(_ns_without["descriptor"]["entries"]) and all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "pivot-reevaluation-unavailable" for e in _ns_without["descriptor"]["entries"]),
    [(e["classification"], e.get("indeterminateReason")) for e in _ns_without["descriptor"]["entries"]],
)
_ns_policy = _ns_art["descriptor"]["contextDocuments"]["policy"]
_ns_rule = _ns_art["descriptor"]["entries"][0]["ruleId"]
check(
    "s7-non-selection-is-structural-scope-and-policy",
    P.selection_excludes(_ns_policy, SCOPE_DOC, _ns_rule, "README.md") is True
    and P.selection_excludes(_ns_policy, SCOPE_ALL, _ns_rule, "README.md") is False
    and P.selection_excludes(P.project_admitted_run_v3(*_ns_disabled)["policy"], SCOPE_ALL, _ns_rule, "README.md") is True,
)

# S5: argvDigest is raw SHA-256 of C(exact ordered argv); no shell-joined surrogate.
_te = json.loads((HERE / "workflow-cases.v1.json").read_text())["testExecution"]
_te_sub = {"$PRJ": PRJ, "$SNAP1": SNAP, "$GRANT": "security.repo-execution-grant.v2:" + token("grant"), "$TOOL0": DET}


def _te_resolve(value):
    if isinstance(value, dict):
        return {_te_sub.get(k, k): _te_resolve(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_te_resolve(v) for v in value]
    return _te_sub.get(value, value) if isinstance(value, str) else value


_te_params = _te_resolve(_te["params"])
_te_ctx = _te_resolve(_te["ctx"])


def _te_admit(argv, digest):
    ctx_ = copy.deepcopy(_te_ctx)
    ctx_["grant"]["argvDigest"] = digest
    return P.W.admit_test_execution(dict(_te_params, argv=argv), ctx_)


def _argv_digest(v):
    return hashlib.sha256(canonical.canonical(v)).hexdigest()


_te_argv = list(_te_params["argv"])
check("s5-exact-ordered-argv-canonical-digest-admits", _te_admit(_te_argv, _argv_digest(_te_argv))["admitted"] is True)
reject("s5-shell-joined-argv-surrogate-refused", lambda: _te_admit(_te_argv, hashlib.sha256(" ".join(_te_argv).encode()).hexdigest()), "REQUEST.PRECONDITION_FAILED", "TEST.PRINCIPAL_NOT_ADMITTED")
reject("s5-repeated-argument-is-a-different-argv", lambda: _te_admit(_te_argv + [_te_argv[-1]], _argv_digest(_te_argv)), "REQUEST.PRECONDITION_FAILED", "TEST.PRINCIPAL_NOT_ADMITTED")
check("s5-repeated-argument-admits-under-its-own-digest", _te_admit(_te_argv + [_te_argv[-1]], _argv_digest(_te_argv + [_te_argv[-1]]))["admitted"] is True)
reject("s5-reordered-arguments-refused", lambda: _te_admit(list(reversed(_te_argv)), _argv_digest(_te_argv)), "REQUEST.PRECONDITION_FAILED")
check(
    "s5-member-boundaries-and-empty-strings-change-the-digest-where-a-join-collides",
    _argv_digest(["run", "a b"]) != _argv_digest(["run", "a", "b"])
    and " ".join(["run", "a b"]) == " ".join(["run", "a", "b"])
    and _argv_digest(["run", "x", ""]) != _argv_digest(["run", "x"]),
)
check("s5-test-payload-uses-the-same-recipe", P.W.test_payload(_te_params, 0, b"", b"")["argvDigest"] == _argv_digest(_te_argv))

# S6 / A13: failure goldens carry actual detail; required-delivery detail binds the committed-Run reference.
_inv3 = json.loads((HERE / "command-inventory.v3.json").read_text())
_fault_for = {v: k for k, v in P.W.FAULT_TO_ERROR.items()}
_golden_envelopes = []
for _g in _inv3["goldens"]:
    if _g["class"] not in ("request-rejected", "operational-failed"):
        continue
    _d = {"code": _g["domainDetail"], "remedy": _g["remedy"]}
    _t = {"class": _g["class"], "errorCode": _g["errorCode"], "domainDetail": _d}
    if _g["class"] == "operational-failed":
        _t["faultCause"] = _fault_for[_g["errorCode"]]
        if _g["domainDetail"] == "DELIVERY.RENDERER_FAILED_AFTER_COMMIT":
            _t["runId"] = RUN
    _ok, _why = valid(U + "command-envelope:3", {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": "req1_" + "c" * 32, "termination": _t, "exitCode": _g["exitCode"], "errors": [_d]})
    _golden_envelopes.append((_g["id"], _ok, _why))
check("s6-every-v3-failure-golden-forms-a-lawful-failure-envelope", len(_golden_envelopes) >= 20 and all(ok for _, ok, _ in _golden_envelopes), [x for x in _golden_envelopes if not x[1]])
check(
    "s6-formerly-unconstructible-goldens-carry-owner-detail",
    {g["id"]: g.get("domainDetail") for g in _inv3["goldens"] if g["id"] in ("doctor-report-not-producible", "query-latest-empty", "envelope-major-unsupported")}
    == {"doctor-report-not-producible": "DOCTOR.REPORT_NOT_PRODUCIBLE", "query-latest-empty": "QUERY.VIEW_UNKNOWN", "envelope-major-unsupported": "OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED"},
)
_qle = next(g for g in _inv3["goldens"] if g["id"] == "query-latest-empty")
check(
    "s6-query-latest-empty-detail-is-the-query-owner-row",
    "| empty, missing, stale, or mismatched latest/snapshot/run selector | request-rejected | `IDENTITY.UNKNOWN` | `QUERY.VIEW_UNKNOWN` |" in (HERE / "query-projection-contract.v3.md").read_text()
    and _qle["errorCode"] == "IDENTITY.UNKNOWN",
)
_qle_no_detail = {k: v for k, v in _qle.items() if k != "domainDetail"}
must_invalid("s6-failure-golden-without-detail-refused", U + "command-inventory:3#/$defs/Golden", _qle_no_detail)
must_valid("s6-failure-golden-with-named-composition-admitted", U + "command-inventory:3#/$defs/Golden", dict(_qle_no_detail, detailSuppliedBy="native-route-composition"))
must_invalid("s6-named-composition-and-detail-together-refused", U + "command-inventory:3#/$defs/Golden", dict(_qle, detailSuppliedBy="native-route-composition"))
for _label, _gid in (("doctor", "doctor-report-not-producible"), ("query-empty", "query-latest-empty"), ("envelope-major", "envelope-major-unsupported")):
    _g = next(g for g in _inv3["goldens"] if g["id"] == _gid)
    _t = {"class": _g["class"], "errorCode": _g["errorCode"]}
    if _g["class"] == "operational-failed":
        _t["faultCause"] = _fault_for[_g["errorCode"]]
    _env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": "req1_" + "c" * 32, "termination": _t, "exitCode": _g["exitCode"]}
    must_invalid("s6-%s-failure-envelope-without-errors-refused" % _label, U + "command-envelope:3", _env)
    _d = {"code": _g["domainDetail"], "remedy": _g["remedy"]}
    must_valid("s6-%s-failure-envelope-with-golden-detail-admitted" % _label, U + "command-envelope:3", dict(_env, termination=dict(_t, domainDetail=_d), errors=[_d]))
_new_details = {"DOCTOR.REPORT_NOT_PRODUCIBLE", "OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED", "DELIVERY.REQUIRED_PROJECTION_FAILED"}
_registry_codes = {r["code"] for r in json.loads((HERE.parent / "public-detail-registry.v1.json").read_text())["records"]}
check(
    "s6-a13-new-details-registered-and-in-both-common-mirrors",
    _new_details <= _registry_codes
    and _new_details <= set(SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])
    and _new_details <= set(SCHEMAS["urn:opensip:product-v1:workflows:common"]["$defs"]["DomainDetailCode"]["enum"])
    and _registry_codes == set(SCHEMAS["urn:opensip:product-v1:workflows:common"]["$defs"]["DomainDetailCode"]["enum"]),
)
_post = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required", "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT", "remedy": "r"}}
_pre = dict(_post, domainDetail={"code": "DELIVERY.REQUIRED_PROJECTION_FAILED", "remedy": "r"})
for _label, _ref, _run in (("current", U + "common:3#/$defs/StepTermination", RUN), ("retained", "urn:opensip:product-v1:workflows:common#/$defs/StepTermination", "run2:" + token("run"))):
    must_valid("a13-%s-postcommit-detail-with-committed-run-admitted" % _label, _ref, dict(_post, runId=_run))
    must_invalid("a13-%s-postcommit-detail-without-run-refused" % _label, _ref, _post)
    must_valid("a13-%s-precommit-detail-without-run-admitted" % _label, _ref, _pre)
    must_invalid("a13-%s-precommit-detail-with-run-refused" % _label, _ref, dict(_pre, runId=_run))
    must_invalid("a13-%s-precommit-detail-on-another-class-refused" % _label, _ref, {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "DELIVERY.REQUIRED_PROJECTION_FAILED", "remedy": "r"}})
    must_valid("a13-%s-other-operational-failure-keeps-optional-run" % _label, _ref, {"class": "operational-failed", "errorCode": "DURABILITY.COMMIT_FAILED", "faultCause": "durability-commit", "runId": _run})
    must_invalid("a13-%s-termination-exclusivity-retained" % _label, _ref, dict(_pre, reasonCodes=["VERDICT.INDETERMINATE"]))

# A11: current test execution admits only the selected truth-table profile values.
_te_enum = SCHEMAS["urn:opensip:product-v1:workflows:test-execution"]["$defs"]["EnforcementValue"]
check("a11-selected-truth-table-profile-has-no-platform-primitive-row", "ENFORCED-PLATFORM" not in (HERE.parent.parent / "artifacts" / "permission-truth-tables.v9.json").read_text())
must_invalid(
    "a11-enforced-platform-effect-not-admissible-in-current-profile",
    "urn:opensip:product-v1:workflows:test-execution#/$defs/TestExecutionStepParams",
    dict(_te_params, effects=dict(_te_params["effects"], network="ENFORCED-PLATFORM:seatbelt")),
)
check("a11-enforcement-description-states-profile-law", "cannot be claimed" in _te_enum["description"] and "admitted only when" not in _te_enum["description"])
reject(
    "a11-schema-member-still-must-equal-truth-table-row",
    lambda: P.W.admit_test_execution(dict(_te_params, effects=dict(_te_params["effects"], network="ENFORCED-AT-HOST-BROKER")), copy.deepcopy(dict(_te_ctx, grant=dict(_te_ctx["grant"], argvDigest=_argv_digest(_te_argv))))),
    "REQUEST.PRECONDITION_FAILED",
    "TEST.CONFINEMENT_CLAIM_REFUSED",
)

# A12: the existing hidden reason covers any later axis; A8/A14 published selections.
_a12_rule = {"enabled": True, "gating": True, "evidenceUse": []}
_a12_entry, _a12_sig = P.W.classify(
    hid("finding-key2", "a12"), "r",
    {"B": False, "E0": True, "E1": False, "E2": False, "E3": False, "E4": False, "waivedB": False, "waivedC": False},
    _a12_rule, _a12_rule, empty_evidence(), empty_evidence(), {"detectorId": "fixture", "method": "identical-closure"}, P.AUDIT_PROFILES["code-regression"],
)
check("a12-detector-hidden-code-net-new-gates-with-hidden-reason", _a12_entry["gates"] and _a12_entry["gateReason"] == "code-net-new-policy-hidden" and _a12_entry["subsequentDeltas"] == ["detection"] and _a12_sig == "fail")
_chapter_ws = (HERE.parents[3] / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text()
check("a12-hidden-reason-defined-over-any-later-axis", "hidden by a later detector, policy or scope change" in " ".join(_chapter_ws.split()) and "detector" in SCHEMAS[U + "comparison:2"]["$defs"]["Entry"]["properties"]["gateReason"]["description"])
check("a8-workflows-publishes-present-listing-refusal-route", "`REQUEST.PRECONDITION_FAILED` / `EVALUATION.PROJECTION_INPUT_INCOMPLETE`" in _chapter_ws)
reject("a8-present-listing-missing-blob-route", lambda: P.parse_detector_manifest_body({}, "f" * 64, present=True), "REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE")
check("a14-conservative-evidence-attribution-preserved", "Evidence-change attribution is deliberately conservative" in _chapter_ws and "A future evidence-pivot recipe requires its own reviewed successor." in _chapter_ws)


def _sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

OWNED = [
    HERE / "workflow_projection_model.v3.py",
    HERE / "check-workflow-projection.v3.py",
    HERE / "workflow-projection-contract.v3.md",
    HERE / "command-inventory.v3.json",
    HERE / "command-inventory.v1.json",
    HERE / "repair_closed_world_selection.v1.py",
    HERE / "workflows_model.v3.py",
]
OWNED += sorted((HERE / "schemas" / "evaluator3").glob("*.schema.json"))
source_hashes = {str(p.relative_to(HERE)): _sha256_file(p) for p in OWNED}

passed = all(c["ok"] for c in CHECKS)
report = {
    "standing": "BOUNDED WORKFLOW PROJECTION ONLY. Isolated evaluator3 schemas + close_run adapter over synthetic owner-admitted graphs. Not real extraction qualification, not full SARIF-schema qualification, not full profile acceptance. Passing these checks does not establish complete admission. Root reminted mutants PASS open_run_closure and REFUSE complete semantic close; they are not claimed as owner-admission failures. Execution-inputs is required on an admitted Run. Main Grok v6 removes ambient physical store pointer inventories from semantic identity.",
    "passed": passed,
    "count": len(CHECKS),
    "failed": [c for c in CHECKS if not c["ok"]],
    "results": CHECKS,
    "repairClosedWorldStanding": REPAIR_CLOSED_WORLD_STANDING,
    "declaredCompatibleStanding": DECLARED_COMPATIBLE,
    "commandInventoryJoins": INVENTORY_JOINS,
    "sourceHashes": source_hashes,
}
V12_ROOT = Path("/tmp/opensip-design-corrections/grok-workflow-projection.v12")
parser = argparse.ArgumentParser(description="Bounded evaluator3 workflow projection checks")
parser.add_argument("--output", help="Write JSON report under grok-workflow-projection.v12/ only. Default: stdout.")
args = parser.parse_args()
payload = json.dumps(report, indent=2) + "\n"
if args.output:
    out = Path(args.output).resolve()
    v12 = V12_ROOT.resolve()
    blocked = {
        "grok-workflow-projection.v1",
        "grok-workflow-projection.v2",
        "grok-workflow-projection.v3",
        "grok-workflow-projection.v4",
        "grok-workflow-projection.v5",
        "grok-workflow-projection.v6",
        "grok-workflow-projection.v7",
        "grok-workflow-projection.v8",
        "grok-workflow-projection.v9",
        "grok-workflow-projection.v10",
        "grok-workflow-projection.v11",
    }
    if any(part in blocked for part in out.parts) or out.name in {
        "workflow-projection-report.v1.json",
        "workflow-projection-report.v2.json",
        "workflow-projection-report.v3.json",
        "workflow-projection-report.v4.json",
    }:
        print("refusing historical receipt path: " + str(out), file=sys.stderr)
        sys.exit(2)
    try:
        out.relative_to(v12)
    except ValueError:
        print("reports must be under " + str(v12) + " or stdout", file=sys.stderr)
        sys.exit(2)
    v12.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload)
    (out.parent / "declared-compatible-standing.v12.md").write_text(
        "# declared-compatible standing (v12)\n\n"
        + "- Normative: "
        + DECLARED_COMPATIBLE["normative"]
        + "\n- Implemented: "
        + DECLARED_COMPATIBLE["implemented"]
        + "\n- Security-owned remainder: "
        + DECLARED_COMPATIBLE["securityOwnedRemainder"]
        + "\n- Host receipt: "
        + DECLARED_COMPATIBLE["hostReceipt"]
        + "\n- Standing: "
        + DECLARED_COMPATIBLE["standing"]
        + "\n"
    )
    (out.parent / "command-inventory-joins.v12.md").write_text(
        "# Command-inventory joins (v12)\n\n"
        + "- Historical: "
        + INVENTORY_JOINS["historicalInstance"]
        + "\n- Current: "
        + INVENTORY_JOINS["currentInstance"]
        + "\n\nRemaining joins:\n"
        + "\n".join("- " + g for g in INVENTORY_JOINS["remainingJoins"])
        + "\n"
    )
    (out.parent / "source-hashes.v12.md").write_text(
        "# Owned source hashes (v12)\n\n"
        + "\n".join(f"- `{k}` `{v}`" for k, v in sorted(source_hashes.items()))
        + "\n"
    )
    print(json.dumps({"passed": passed, "count": len(CHECKS), "failed": report["failed"], "output": str(out)}, indent=2))
else:
    sys.stdout.write(payload)
sys.exit(0 if passed else 1)
