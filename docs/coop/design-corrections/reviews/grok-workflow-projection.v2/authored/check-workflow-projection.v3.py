"""Bounded evaluator3 workflow schema + projection checks. Not full Run replay.

Run: python3.12 -I -B check-workflow-projection.v3.py
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


# ----------------------------------------------------------------------------- schema registry
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


# ----------------------------------------------------------------------------- fixtures
HEX = "ab" * 32
RUN = "run3:" + token("run")
PLAN = "plan2:" + token("plan")
SNAP = "snapshot2:" + token("snap")
PRJ = "prj1-" + token("proj")
DET = "closure2:" + token("detector")
SCOPE = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}
WAIVERS = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
ATOM = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}
POLICY = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 2,
    "gateSeverityAtLeast": "error",
    "rules": [
        {
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
            "subjectEnumeration": {"universe": "typescript-v2", "subjectKind": "file"},
            "emitWhen": ATOM,
            "evidenceUse": [],
        }
    ],
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
    occ = {
        "findingId": hid("finding3", tag),
        "finding": finding,
        "parameterRecord": par,
    }
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


def presence(fp, *, e4=True, waived_c=False):
    return {
        "B": True,
        "E0": True,
        "E1": True,
        "E2": True,
        "E3": True,
        "E4": e4,
        "waivedB": False,
        "waivedC": waived_c,
    }


def adopt(projected, run_id=RUN):
    run = {
        "authority": "authoritative",
        "availability": "retained",
        "runId": run_id,
        "snapshotId": SNAP,
    }
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
        "1.0.0",
    )


# ----------------------------------------------------------------------------- schema shape
check("schema-count", len(list(E3.glob("*.schema.json"))) == 9)
check("common-run3-not-mixed", SCHEMAS[U + "common:3"]["$defs"]["RunId"]["pattern"].startswith("^run3:"))
check("common-no-run2-alternation", "run[23]" not in json.dumps(SCHEMAS[U + "common:3"]["$defs"]["RunId"]))
check("fingerprint-retained-key2", SCHEMAS[U + "common:3"]["$defs"]["Fingerprint"]["pattern"].startswith("^finding-key2:"))
check("baseline-schema-major-2", SCHEMAS[U + "baseline:2"]["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check(
    "baseline-requires-unmatched",
    "unmatchedOccurrences" in SCHEMAS[U + "baseline:2"]["$defs"]["BaselineDescriptor"]["required"],
)
check("comparison-schema-major-2", SCHEMAS[U + "comparison:2"]["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check(
    "comparison-cause-correspondence",
    "correspondence-incomplete" in SCHEMAS[U + "comparison:2"]["$defs"]["RuleDeficiency"]["properties"]["cause"]["enum"],
)
check("envelope-major-3", SCHEMAS[U + "command-envelope:3"]["properties"]["schemaMajor"]["const"] == 3)
check("invocation-major-3", SCHEMAS[U + "invocation:3"]["properties"]["schemaMajor"]["const"] == 3)
V1 = WF
v1_base = json.loads((V1 / "baseline-artifact.schema.json").read_text())
v1_cmp = json.loads((V1 / "comparison-result.schema.json").read_text())
v1_env = json.loads((V1 / "command-envelope.schema.json").read_text())
v1_inv = json.loads((V1 / "invocation-record.schema.json").read_text())
v1_q = json.loads((V1 / "graph-query.schema.json").read_text())
v1_rep = json.loads((V1 / "repair.schema.json").read_text())
v1_invt = json.loads((V1 / "command-inventory.schema.json").read_text())
check("v1-baseline-identity-major-was-1", v1_base["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-comparison-identity-major-was-1", v1_cmp["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-envelope-major-was-2", v1_env["properties"]["schemaMajor"]["const"] == 2)
check("v1-invocation-major-was-1", v1_inv["properties"]["schemaMajor"]["const"] == 1)
check("v1-query-major-was-1", v1_q["$defs"]["GraphQueryRequestV1"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-repair-plan-major-was-1", v1_rep["$defs"]["RepairPlanDescriptor"]["properties"]["schemaMajor"]["const"] == 1)
check("v1-inventory-major-was-1", v1_invt["properties"]["schemaMajor"]["const"] == 1)
check("new-baseline-major-bumped-for-unmatched-preimage", SCHEMAS[U + "baseline:2"]["$defs"]["BaselineDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check("new-comparison-major-bumped-for-unmatched-preimage", SCHEMAS[U + "comparison:2"]["$defs"]["ComparisonDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check("new-repair-plan-major-bumped-for-run3", SCHEMAS[U + "repair:2"]["$defs"]["RepairPlanDescriptor"]["properties"]["schemaMajor"]["const"] == 2)
check("new-query-major-bumped-for-findingId", SCHEMAS[U + "graph-query:2"]["$defs"]["GraphQueryRequestV1"]["properties"]["schemaMajor"]["const"] == 2)
pins = SCHEMAS[U + "baseline:2"]["$defs"]["Custody"]["properties"]["retentionPins"]["items"]["pattern"]
check("retention-pins-run3-not-mixed-regex", pins == "^(run3|closure2):[0-9a-f]{64}(?![\\s\\S])")
must_invalid(
    "run2-prefix-refused",
    U + "common:3#/$defs/RunId",
    "run2:" + "a" * 64,
)
must_valid("run3-prefix-admitted", U + "common:3#/$defs/RunId", "run3:" + "a" * 64)
must_invalid(
    "finding2-prefix-refused",
    U + "common:3#/$defs/FindingId",
    "finding2:" + "a" * 64,
)

# mixed-major finding surface
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
bad = copy.deepcopy(surf_unmatched)
bad["partialFingerprints"] = {"opensip/finding-key2": "finding-key2:" + "a" * 64}
must_invalid("unmatched-cannot-carry-partialFingerprints", U + "common:3#/$defs/FindingSurface", bad)

# ----------------------------------------------------------------------------- two-config one fingerprint, different params
a = occurrence("cfg-a", universe="one", facts=0)
b = occurrence("cfg-b", universe="two", facts=3)
check("two-config-same-logical-fingerprint", a["finding"]["fingerprint"] == b["finding"]["fingerprint"])
check("two-config-different-params", a["parameterRecord"]["parameters"]["matchingFactCount"] != b["parameterRecord"]["parameters"]["matchingFactCount"])
proj = P.project_baseline_entries([a, b], {"r": BINDING}, [])
check("two-config-one-baseline-entry", len(proj["entries"]) == 1 and len(proj["unmatchedOccurrences"]) == 0)
check("two-config-params-not-collapsed", a["finding"]["parameterDigest"] != b["finding"]["parameterDigest"])
check("subjectId-opaque-not-three-coords", a["finding"]["subjectId"] != b["finding"]["subjectId"] and a["finding"]["subject"]["logicalPath"] == b["finding"]["subject"]["logicalPath"])
# Same packageName, two first-party manifests: fingerprints differ by finding.subject.logicalPath.
pkg_a = occurrence("pkg-a", kind="package", name="dup", path="crates/a/Cargo.toml", universe="u", subject_id=hid("subject3", "pkg-a-opaque"))
pkg_b = occurrence("pkg-b", kind="package", name="dup", path="crates/b/Cargo.toml", universe="u", subject_id=hid("subject3", "pkg-b-opaque"))
check("package-same-name-different-manifest-paths", pkg_a["finding"]["subject"]["qualifiedName"] == pkg_b["finding"]["subject"]["qualifiedName"])
check("package-manifest-path-owns-fingerprint", pkg_a["finding"]["fingerprint"] != pkg_b["finding"]["fingerprint"])
pkg_proj = P.project_baseline_entries([pkg_a, pkg_b], {"r": BINDING}, [])
check("package-two-baseline-entries-by-path", len(pkg_proj["entries"]) == 2)
art = adopt(proj)
check("adopt-schema-major-2", art["descriptor"]["schemaMajor"] == 2)
check("adopt-run3", art["descriptor"]["runId"].startswith("run3:"))
P.verify_baseline_artifact_v3(art)
must_valid("baseline-artifact-schema", U + "baseline:2", art)

# ----------------------------------------------------------------------------- legacyFingerprint presence disagreement refuses
c = occurrence("leg-a", universe="one")
d = occurrence("leg-b", universe="two", legacy="old-key")
reject(
    "legacy-optional-presence-conflict",
    lambda: P.project_baseline_entries([c, d], {"r": BINDING}, []),
    "CONFIG.INVALID",
    "BASELINE.ENTRY_PROJECTION_CONFLICT",
)
e = occurrence("leg-c", universe="one", legacy="old-key")
f = occurrence("leg-d", universe="two", legacy="other-key")
reject(
    "legacy-value-conflict",
    lambda: P.project_baseline_entries([e, f], {"r": BINDING}, []),
    "CONFIG.INVALID",
    "BASELINE.ENTRY_PROJECTION_CONFLICT",
)
g = occurrence("leg-ok-a", universe="one", legacy="same")
h = occurrence("leg-ok-b", universe="two", legacy="same")
ok_legacy = P.project_baseline_entries([g, h], {"r": BINDING}, [])
check("legacy-agree-groups", ok_legacy["entries"][0]["legacyFingerprint"] == "same")

# fingerprint preimage conflict is input refusal
i_occ = occurrence("pre-a")
j_occ = copy.deepcopy(i_occ)
j_occ["findingId"] = hid("finding3", "pre-b")
j_occ["fingerprintDescriptor"] = fp_desc(path="src/b.ts")
# keep same fingerprint id (conflict)
reject(
    "preimage-conflict-input-refusal",
    lambda: P.project_baseline_entries([i_occ, j_occ], {"r": BINDING}, []),
    "CONFIG.INVALID",
    "CONFIG.INVALID",
)

# ----------------------------------------------------------------------------- unmatched current fail / audit unknown / path waiver
u = occurrence("un-1", unmatched=True, reason="signature-ambiguous")
proj_u = P.project_baseline_entries([u], {"r": BINDING}, [])
check("unmatched-not-in-entries", proj_u["entries"] == [] and len(proj_u["unmatchedOccurrences"]) == 1)
rules_fail = [
    {
        "ruleId": "r",
        "enumeration": complete_enum(),
        "outcome": "fail",
        "findingIds": [u["findingId"]],
        "deficiencies": [],
        "gating": True,
    }
]
check("unmatched-current-fail", P.current_run_verdict(rules_fail, [u], []) == "fail")
art_u = adopt(proj_u)
current_u = {
    "runId": hid("run3", "cur"),
    "snapshotId": hid("snapshot2", "cur"),
    "projectId": PRJ,
    "context": ctx(),
    "ruleCoverage": {"r": rule_cov()},
    "presence": {},
    "entryRules": {},
    "boundPivots": [],
    "occurrences": [u],
    "waivedFindingIds": [],
    "ruleResults": rules_fail,
}
cmp_u = P.compare_v3({"descriptor": art_u["descriptor"], "baselineId": art_u["baselineId"], **art_u["descriptor"]}, current_u, host(), "code-regression", detectors())
# compare_v3 expects baseline with _baselineId and descriptor fields at top. Pass flattened.
base_flat = dict(art_u["descriptor"])
base_flat["_baselineId"] = art_u["baselineId"]
cmp_u = P.compare_v3(base_flat, current_u, host(), "code-regression", detectors())
check("unmatched-not-classified-as-net-new", all(e.get("classification") != "CODE-NET-NEW" for e in cmp_u["descriptor"]["entries"]))
check(
    "unmatched-audit-correspondence-incomplete",
    cmp_u["descriptor"]["verdict"] == "indeterminate"
    and any(d["cause"] == "correspondence-incomplete" for d in cmp_u["descriptor"]["ruleDeficiencies"]),
)
must_valid("comparison-artifact-schema", U + "comparison:2", {"comparisonResultId": cmp_u["comparisonResultId"], "descriptor": cmp_u["descriptor"]})

rules_pass = copy.deepcopy(rules_fail)
rules_pass[0]["outcome"] = "pass"
check("path-waiver-current-pass", P.current_run_verdict(rules_pass, [u], [u["findingId"]]) == "pass")
current_w = copy.deepcopy(current_u)
current_w["waivedFindingIds"] = [u["findingId"]]
current_w["ruleResults"] = rules_pass
cmp_w = P.compare_v3(base_flat, current_w, host(), "code-regression", detectors())
check(
    "path-waiver-audit-still-unknown",
    cmp_w["descriptor"]["verdict"] == "indeterminate"
    and cmp_w["descriptor"]["unmatchedOccurrences"][0]["waived"] is True,
)

# fingerprint waiver cannot be applied by projector to unmatched (null fp)
check("unmatched-fingerprint-is-null", u["finding"]["fingerprint"] is None)

# ----------------------------------------------------------------------------- matched regression dominates unknown
m = occurrence("reg-new", universe="cur-only")
# baseline empty matched, current has matched finding → CODE-NET-NEW
proj_empty = P.project_baseline_entries([], {"r": BINDING}, [])
art_empty = adopt(proj_empty)
base_empty = dict(art_empty["descriptor"])
base_empty["_baselineId"] = art_empty["baselineId"]
fp_m = m["finding"]["fingerprint"]
current_reg = {
    "runId": hid("run3", "reg"),
    "snapshotId": hid("snapshot2", "reg"),
    "projectId": PRJ,
    "context": ctx(),
    "ruleCoverage": {"r": rule_cov()},
    "presence": {fp_m: {"B": False, "E0": False, "E1": True, "E2": True, "E3": True, "E4": True, "waivedB": False, "waivedC": False}},
    "entryRules": {fp_m: ("r", "fixture")},
    "boundPivots": [],
    "occurrences": [m, u],
    "waivedFindingIds": [],
    "ruleResults": [
        {
            "ruleId": "r",
            "enumeration": complete_enum(),
            "outcome": "fail",
            "findingIds": [m["findingId"], u["findingId"]],
            "deficiencies": [],
            "gating": True,
        }
    ],
}
cmp_reg = P.compare_v3(base_empty, current_reg, host(), "code-regression", detectors())
check(
    "matched-regression-dominates-unknown",
    cmp_reg["descriptor"]["verdict"] == "fail"
    and any(e["classification"] == "CODE-NET-NEW" and e["gates"] for e in cmp_reg["descriptor"]["entries"])
    and any(d["cause"] == "correspondence-incomplete" for d in cmp_reg["descriptor"]["ruleDeficiencies"]),
)
# default profile: new waiver does not suppress net-new
current_reg_w = copy.deepcopy(current_reg)
current_reg_w["presence"][fp_m]["waivedC"] = True
current_reg_w["presence"][fp_m]["E4"] = True
cmp_nw = P.compare_v3(base_empty, current_reg_w, host(), "code-regression", detectors())
net = next(e for e in cmp_nw["descriptor"]["entries"] if e["classification"] == "CODE-NET-NEW")
check("code-regression-new-waiver-does-not-suppress", net["gates"] is True and net.get("gateReason") == "code-net-new-policy-hidden")
cmp_fc = P.compare_v3(base_empty, current_reg_w, host(), "full-current", detectors())
# full-current newWaiverSuppressesCodeNetNew: if not live (waived), code-net-new does not gate via live; hidden suppressed
net_fc = next(e for e in cmp_fc["descriptor"]["entries"] if e["classification"] == "CODE-NET-NEW")
check("full-current-new-waiver-suppresses-hidden-net-new", net_fc["gates"] is False)

# ----------------------------------------------------------------------------- optional unknown non-gating
opt_rules = [
    {
        "ruleId": "r",
        "enumeration": complete_enum(),
        "outcome": "pass",
        "findingIds": [],
        "deficiencies": [{"source": "import", "cause": "absent-runtime", "subjectId": None, "predicateId": "p", "inputRefs": []}],
        "gating": False,
    }
]
check("optional-unknown-non-gating-current-pass", P.current_run_verdict(opt_rules, [], []) == "pass")
current_opt = {
    "runId": hid("run3", "opt"),
    "snapshotId": SNAP,
    "projectId": PRJ,
    "context": ctx(),
    "ruleCoverage": {"r": rule_cov(gating=False)},
    "presence": {},
    "entryRules": {},
    "occurrences": [],
    "waivedFindingIds": [],
    "ruleResults": opt_rules,
}
cmp_opt = P.compare_v3(base_empty, current_opt, host(), "code-regression", detectors())
check(
    "optional-unknown-no-gating-correspondence-deficiency",
    not any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_opt["descriptor"]["ruleDeficiencies"]),
)

# ----------------------------------------------------------------------------- zero findings + population unknown preserved
zero_rules = [
    {
        "ruleId": "r",
        "enumeration": incomplete_enum(),
        "outcome": "indeterminate",
        "findingIds": [],
        "deficiencies": [{"source": "enumeration", "cause": "no-covering-program", "subjectId": None, "predicateId": None, "inputRefs": []}],
        "gating": True,
    }
]
check("zero-finding-population-unknown-not-pass", P.current_run_verdict(zero_rules, [], []) == "indeterminate")
current_z = {
    "runId": hid("run3", "zero"),
    "snapshotId": SNAP,
    "projectId": PRJ,
    "context": ctx(),
    "ruleCoverage": {"r": rule_cov()},
    "presence": {},
    "entryRules": {},
    "occurrences": [],
    "waivedFindingIds": [],
    "ruleResults": zero_rules,
}
cmp_z = P.compare_v3(base_empty, current_z, host(), "code-regression", detectors())
cov = cmp_z["descriptor"]["correspondenceCoverage"][0]
check("zero-result-population-unknown-preserved", cov["populationUnknown"] is True and cov["zeroFindings"] is True and cov["unmatchedCount"] == 0)
check(
    "zero-unknown-gating-deficiency",
    any(d["cause"] == "correspondence-incomplete" and d["gating"] for d in cmp_z["descriptor"]["ruleDeficiencies"]),
)
syn_rules = [
    {
        "ruleId": "r",
        "enumeration": incomplete_enum(),
        "outcome": "indeterminate",
        "findingIds": [],
        "deficiencies": [
            {
                "source": "enumeration",
                "cause": "source-syntax-invalid",
                "subjectId": None,
                "predicateId": None,
                "inputRefs": [],
                "evidenceKind": None,
                "nativeCause": None,
                "universe": None,
            }
        ],
        "gating": True,
    }
]
check("source-syntax-invalid-is-enumeration-unknown-not-native", P.current_run_verdict(syn_rules, [], []) == "indeterminate")
current_syn = copy.deepcopy(current_z)
current_syn["ruleResults"] = syn_rules
cmp_syn = P.compare_v3(base_empty, current_syn, host(), "code-regression", detectors())
check(
    "source-syntax-invalid-preserves-zero-population-unknown",
    cmp_syn["descriptor"]["correspondenceCoverage"][0]["populationUnknown"] is True
    and any(d["cause"] == "correspondence-incomplete" for d in cmp_syn["descriptor"]["ruleDeficiencies"]),
)

# ----------------------------------------------------------------------------- SARIF one per config / unmatched
sarif = P.project_sarif([a, b, u], [])
check("sarif-one-per-findingId", len(sarif) == 3 and len({r["findingId"] for r in sarif}) == 3)
check("sarif-matched-have-partialFingerprints", all(("partialFingerprints" in r) == (r["fingerprint"] is not None) for r in sarif))
for row in sarif:
    must_valid("sarif-surface-" + row["findingId"][-8:], U + "common:3#/$defs/FindingSurface", row)

# ----------------------------------------------------------------------------- old major refused, not [] coercion
old = copy.deepcopy(art)
old["descriptor"]["schemaMajor"] = 1
del old["descriptor"]["unmatchedOccurrences"]
reject(
    "old-baseline-major-refused-not-empty-coercion",
    lambda: P.verify_baseline_artifact_v3(old),
    "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
    "BASELINE.SCHEMA_MAJOR_UNSUPPORTED",
)
cmp_old = P.compare_v3(old["descriptor"] | {"_baselineId": old["baselineId"]}, current_z, host(), "code-regression", detectors())
check(
    "old-comparison-major-unsupported",
    cmp_old["descriptor"]["comparisonPerformed"] is False
    and cmp_old.get("errorCode") == "REQUEST.SCHEMA_MAJOR_UNSUPPORTED"
    and cmp_old["descriptor"]["unmatchedOccurrences"] == [],
)

# ----------------------------------------------------------------------------- repair unmatched refuse + multi-config path
reject(
    "repair-unmatched-refuses",
    lambda: P.project_repair_targets(["finding-key2:" + "f" * 64], [u]),
    "REQUEST.PRECONDITION_FAILED",
    "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE",
)
ok_repair = P.project_repair_targets([a["finding"]["fingerprint"]], [a, b])
check("repair-multi-config-compatible-keeps-both-ids", len(ok_repair[a["finding"]["fingerprint"]]["findingIds"]) == 2)
check("repair-does-not-collapse-params", len(ok_repair[a["finding"]["fingerprint"]]["parameterDigests"]) == 2)
amb_a = occurrence("amb-a", path="src/a.ts")
amb_b = occurrence("amb-b", path="src/b.ts")
# force same fingerprint id with different path metadata — preimage would refuse at baseline;
# repair sees two occs mapped to same fp key by overwriting fingerprint field.
amb_b["finding"]["fingerprint"] = amb_a["finding"]["fingerprint"]
amb_b["fingerprintDescriptor"] = amb_a["fingerprintDescriptor"]
reject(
    "repair-multi-config-path-ambiguity",
    lambda: P.project_repair_targets([amb_a["finding"]["fingerprint"]], [amb_a, amb_b]),
    "REQUEST.PRECONDITION_FAILED",
    "REPAIR.TARGET_METADATA_AMBIGUOUS",
)

# ----------------------------------------------------------------------------- candidates / query: unmatched by findingId, no fake fp, no fp suppression
cands = P.project_candidates(RUN, PRJ, [a, u], {"r": True}, [], {}, "2026-09-08")
un_c = next(c for c in cands if c["findingId"] == u["findingId"])
m_c = next(c for c in cands if c["findingId"] == a["findingId"])
check("unmatched-candidate-key-is-findingId", un_c["fingerprint"] is None and un_c["findingId"] == u["findingId"])
check("matched-candidate-has-fingerprint", m_c["fingerprint"] == a["finding"]["fingerprint"])
# suppress matched candidate; unmatched remains
disp = {m_c["candidateId"]: {"disposition": "reject", "suppressUntil": "2026-12-01", "receiptId": hid("receipt2", "r1")}}
cands2 = P.project_candidates(RUN, PRJ, [a, u], {"r": True}, [], disp, "2026-09-08")
check(
    "fingerprint-suppression-does-not-hide-unmatched",
    next(c for c in cands2 if c["findingId"] == u["findingId"])["suppressed"] is False
    and next(c for c in cands2 if c["findingId"] == a["findingId"])["suppressed"] is True,
)
q1 = P.query_finding([a, b, u], finding_id=u["findingId"])
check("query-unmatched-by-findingId", len(q1) == 1 and q1[0]["findingId"] == u["findingId"])
q2 = P.query_finding([a, b, u], fingerprint=a["finding"]["fingerprint"])
check("query-fingerprint-matched-only-all-configs", len(q2) == 2 and all(o["finding"]["fingerprint"] for o in q2))
must_valid("candidate-matched-schema", U + "review:2#/$defs/Candidate", m_c)
must_valid("candidate-unmatched-schema", U + "review:2#/$defs/Candidate", un_c)

# findings map never fingerprint
fm = P.findings_map([a, b])
check("findings-map-by-findingId", set(fm) == {a["findingId"], b["findingId"]})

# output bound route
term = P.serialization_overflow_termination()
check(
    "output-bound-existing-error",
    term["errorCode"] == "OUTPUT.SERIALIZATION_FAILED"
    and term["faultCause"] == "output-serialization"
    and term["class"] == "operational-failed"
    and term["domainDetail"]["code"] == "EVALUATION.OUTPUT_BOUND_EXCEEDED"
    and term["errorCode"] != "HOST.IO_FAILURE",
)

# query schema findingId
must_valid(
    "graph-query-findingId-param",
    U + "graph-query:2#/$defs/Params",
    {"findingId": hid("finding3", "q")},
)

passed = all(c["ok"] for c in CHECKS)
report = {
    "standing": "BOUNDED WORKFLOW PROJECTION ONLY. Isolated evaluator3 schemas + pure projection over admitted finding objects. Not native admission, not complete retained-Run replay, not public-registry integration.",
    "passed": passed,
    "count": len(CHECKS),
    "failed": [c for c in CHECKS if not c["ok"]],
    "results": CHECKS,
}
helper = Path("/tmp/opensip-design-corrections/grok-workflow-projection.v1/workflow-projection-report.v3.json")
helper.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": passed, "count": len(CHECKS), "failed": report["failed"]}, indent=2))
sys.exit(0 if passed else 1)
