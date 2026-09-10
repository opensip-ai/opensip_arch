"""Independent Grok probes of frozen source23. Not author oracles; not qualification."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/grok-independent-design.v23")
ORIG = Path("/tmp/opensip-design-corrections/candidate-subject.v23")
COPY = OUT / "subject-copy"
DC = COPY / "docs/coop/design-corrections"
FOUND = DC / "foundation"
PY = "/tmp/opensip-architecture-review-env/bin/python"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("probe_fixture3", FOUND / "evaluator_graph_fixture.v3.py")
R = load("probe_replay3", FOUND / "evaluator_replay_model.v3.py")
M = R.M
C = M.C
W = load("probe_projection3", DC / "workflows/workflow_projection_model.v3.py")
rows = []


def add(name, **kwargs):
    rec = {"case": name, **kwargs}
    rows.append(rec)
    return rec


def canonical_sets(value):
    if type(value) is dict:
        for k, v in value.items():
            canonical_sets(v)
            if k in (
                "findingIds",
                "waivedFindingIds",
                "evidenceRefs",
                "inputRefs",
                "evaluationInputRefs",
                "scopeIds",
                "coverageIds",
                "matchingFactIds",
                "uncertainFactIds",
                "matchingImportRows",
                "uncertainImportRows",
                "deficiencies",
            ):
                value[k] = R.E.cset(v)
            if k == "predicateProofs":
                value[k] = sorted(
                    v, key=lambda x: tuple(x[t].encode() for t in ("ruleId", "subjectId", "predicateId"))
                )
        return value
    if type(value) is list:
        for x in value:
            canonical_sets(x)
    return value


def seal(graph, result, objects, blobs):
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    objects.update(result["objects"])
    blobs.update(result["blobs"])
    i = graph["inputs"]

    def add_obj(domain, fields):
        value = {"schemaVersion": 3, **fields}
        key = M.identifier(domain, value)
        objects[key] = (domain, value)
        return key

    evidence = add_obj(
        "semantic-evidence",
        {
            "planId": i["planId"],
            "viewIds": graph["viewIds"],
            "coverageIds": graph["coverageIds"],
            "importIds": i["plan"]["importIds"],
            "findingIds": result["proof"]["findingIds"],
            "proofBundleId": result["proofBundleId"],
        },
    )
    sid = add_obj(
        "evaluation-seal",
        {
            "planId": i["planId"],
            "executionPlanId": i["executionPlanId"],
            "evidenceId": evidence,
            "evaluatorClosure": i["evaluatorClosure"],
            "policyDigest": i["plan"]["policyDigest"],
            "proofBundleId": result["proofBundleId"],
            "verdict": result["proof"]["verdict"],
        },
    )
    run = {
        "schemaVersion": 3,
        "projectId": graph["snapshot"]["projectId"],
        "snapshotId": i["plan"]["snapshotId"],
        "planId": i["planId"],
        "evidenceId": evidence,
        "evaluationSealId": sid,
        "capabilityManifestId": i["plan"]["capabilityManifestId"],
    }
    return run, objects, blobs


def positive_graph(**options):
    g = F.build_file_inputs(**options)
    seed, objects, blobs, _ = F.seal_fixture(g)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    result = R.derive(
        i["planId"],
        i["executionPlanId"],
        i["evaluatorClosure"],
        i["evaluationInputRefs"],
        objects,
        blobs,
        owner,
    )
    return seal(g, result, objects, blobs)


def remint_enclosing(run, objects, blobs, mutate_finding=None, mutate_proof=None):
    """Reviewer-owned remint: rewrite claimed outputs then re-hash enclosing identities."""
    run = copy.deepcopy(run)
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    evidence = copy.deepcopy(objects[run["evidenceId"]][1])
    seal_rec = copy.deepcopy(objects[run["evaluationSealId"]][1])
    proof = copy.deepcopy(objects[seal_rec["proofBundleId"]][1])
    old_fid = proof["findingIds"][0] if proof.get("findingIds") else None
    if mutate_finding is not None and old_fid:
        finding = copy.deepcopy(objects[old_fid][1])
        mutate_finding(finding, blobs)
        new_fid = M.identifier("finding", finding)
        objects[new_fid] = ("finding", finding)

        def replace(value):
            if value == old_fid:
                return new_fid
            if type(value) is list:
                return [replace(x) for x in value]
            if type(value) is dict:
                return {k: replace(v) for k, v in value.items()}
            return value

        proof = replace(proof)
        evidence = replace(evidence)
    if mutate_proof is not None:
        mutate_proof(proof, objects, blobs)
    canonical_sets(proof)
    pid = M.identifier("proof-bundle", proof)
    objects[pid] = ("proof-bundle", proof)
    evidence["proofBundleId"] = pid
    canonical_sets(evidence)
    eid = M.identifier("semantic-evidence", evidence)
    objects[eid] = ("semantic-evidence", evidence)
    seal_rec.update(proofBundleId=pid, evidenceId=eid, verdict=proof["verdict"])
    sid = M.identifier("evaluation-seal", seal_rec)
    objects[sid] = ("evaluation-seal", seal_rec)
    run.update(evidenceId=eid, evaluationSealId=sid)
    return run, objects, blobs


# --- 1. honest positive graph admits and replays ---
base = positive_graph()
honest_close = M.close_run(*base)
honest_open = M.open_run_closure(*base)[0]
assert honest_close == honest_open
add(
    "honest-positive-close-run-equals-open-run-id",
    ownerAdmission="ADMIT",
    closeRunId=honest_close,
    openRunId=honest_open,
    equal=True,
)

# --- 2. fully reminted false finding: owner ADMIT, complete replay REFUSE ---
def bump_severity(finding, blobs):
    finding["severity"] = "warning"


mutant = remint_enclosing(*base, mutate_finding=bump_severity)
owner_id = M.open_run_closure(*mutant)[0]
replay_refused = False
replay_reason = None
try:
    M.close_run(*mutant)
except Exception as exc:
    replay_reason = str(exc)
    replay_refused = "EVALUATOR_COMPLETE_PROOF_REPLAY" in replay_reason
    if not replay_refused:
        raise
else:
    raise AssertionError("reminted false finding accepted by close_run")
add(
    "reminted-severity-false-result-owner-admits-replay-refuses",
    ownerAdmission="ADMIT",
    ownerRunId=owner_id,
    closeRun="REFUSE",
    replayReasonClass="EVALUATOR_COMPLETE_PROOF_REPLAY",
    structuralApiIsNotSemanticAuthority=True,
)

# --- 3. reminted false verdict with same finding count ---
def force_pass(proof, objects, blobs):
    proof["verdict"] = "pass"


verdict_mutant = remint_enclosing(*base, mutate_proof=force_pass)
owner_id2 = M.open_run_closure(*verdict_mutant)[0]
try:
    M.close_run(*verdict_mutant)
except Exception as exc:
    assert "EVALUATOR_COMPLETE_PROOF_REPLAY" in str(exc), str(exc)
    add(
        "reminted-false-pass-verdict-owner-admits-replay-refuses",
        ownerAdmission="ADMIT",
        ownerRunId=owner_id2,
        closeRun="REFUSE",
        findingCountUnchanged=True,
    )
else:
    raise AssertionError("false pass verdict accepted by close_run")

# --- 4. required evaluator3 Plan parameters ---
payloads = M.PAYLOADS["classes"]["parameter"]["rows"]
required_rows = [k for k, rec in payloads.items() if 3 in rec.get("requiredForEvaluatorMajors", [])]
assert set(required_rows) == {
    "foundation/enumeration-plan.schema.v1.json",
    "foundation/evaluator-emission-plan.schema.v1.json",
}, required_rows
required = [
    {"schemaDigest": hashlib.sha256((DC / path).read_bytes()).hexdigest(), "payloadDigest": "a" * 64}
    for path in required_rows
]
M.admit_parameter_selection(required)
add("exact-two-required-evaluator3-parameters", count=len(required), rows=sorted(required_rows))
for i, _ in enumerate(required):
    selection = [r for j, r in enumerate(required) if j != i]
    try:
        M.admit_parameter_selection(selection)
    except Exception as exc:
        assert "EVALUATOR_REQUIRED_PARAMETER_MISSING" in str(exc), str(exc)
        add("omitted-required-parameter-" + str(i), result="REFUSE", missing=required_rows[i])
    else:
        raise AssertionError("missing required parameter accepted")

# --- 5. DetectorManifestV1 is not the component-manifest body ---
listing_schema = json.loads(
    (DC / "workflows/schemas/evaluator3/detector-manifest.schema.json").read_text()
)
comp_schema = json.loads((COPY / "docs/coop/artifacts/component-manifest-schemas.v11.json").read_bytes())
listing_required = set(listing_schema["required"])
assert listing_required == {"schemaFamily", "schemaMajor", "compatibleClosures"}
assert "platforms" not in listing_schema.get("properties", {})
assert "tree" not in listing_schema.get("properties", {})
# DR-103 component manifest has platforms/tree; listing cannot occupy manifestDigest
manifest_schema = comp_schema.get("manifestSchema") or comp_schema.get("schemas") or comp_schema
text = json.dumps(comp_schema)
assert "platforms" in text and "TreeCommitment" in text or "tree" in text.lower()
add(
    "detector-listing-is-not-component-manifest-body",
    listingRequired=sorted(listing_required),
    listingFieldCount=len(listing_schema["properties"]),
    reservedPath=".opensip/detector-compatibility.json",
    componentManifestHasPlatformsOrTree=True,
)

# --- 6. Independent mixed-root comparison (not the author checker) ---
scope = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}


def build_filtered(pattern):
    return positive_graph(
        scope_document=scope,
        atom_override={
            "op": "exists",
            "relation": "file",
            "minResolution": "enumerated",
            "filters": [{"field": "subject", "cmp": "glob", "value": pattern}],
        },
    )


baseline = build_filtered("README.md")
current = build_filtered("src/**")
M.close_run(*baseline)
M.close_run(*current)
bv = W.project_admitted_run_v3(*baseline)
cv = W.project_admitted_run_v3(*current)
assert bv["snapshotId"] == cv["snapshotId"]
for view in (bv, cv):
    roots = W.admitted_root_predicate_values(view, view["policy"]["rules"][0]["ruleId"])
    assert set(roots.values()) <= {"true", "false"}
    assert not view["executionDeficiencies"]
art = W.adopt_admitted_baseline_v3(
    *baseline, {"exportedAtUtc": "2026-09-08T00:00:00Z", "exportedByHostRelease": "1.0.0"}
)
closures = {
    k: {
        "bytes": "ok",
        "trust": "admitted",
        "trustOrigin": "retained-generation",
        "protocolMajor": v["protocolMajor"],
        "platform": v["platform"],
    }
    for k, (d, v) in baseline[1].items()
    if d == "closure"
}
host = {
    "closures": closures,
    "protocolMajors": sorted({v["protocolMajor"] for v in closures.values()}),
    "platform": "macos-aarch64",
    "pivotRunId": bv["runId"],
    "recipeMajors": [2],
}
comparison = W.compare_admitted_v3(
    baseline_artifact=art,
    current_run=current[0],
    current_objects=current[1],
    current_blobs=current[2],
    host=host,
    profile_name="code-regression",
    pivot_runs={"E1": baseline},
)
entries = comparison["descriptor"]["entries"]
assert len(entries) == 2, entries
assert all(e["classification"] == "POLICY-DELTA" for e in entries), entries
appeared = next(e for e in entries if e["direction"] == "appeared")
assert appeared["presence"]["E1"] is False and appeared["presence"]["E4"] is True
add(
    "independent-mixed-root-absence-is-policy-delta-not-indeterminate",
    classifications=sorted({e["classification"] for e in entries}),
    directions=sorted({e["direction"] for e in entries}),
    appearedE1=appeared["presence"]["E1"],
    appearedE4=appeared["presence"]["E4"],
    verdict=comparison["descriptor"]["verdict"],
)

# --- 7. Independent counts vs author-prose claims ---
native_cases = json.loads((DC / "native/native-cases.v2.json").read_bytes())
# fixtures may be under several keys
if isinstance(native_cases, dict) and "fixtures" in native_cases:
    n_count = len(native_cases["fixtures"])
elif isinstance(native_cases, dict) and "cases" in native_cases:
    n_count = len(native_cases["cases"])
else:
    n_count = None
# report independently
n_report = json.loads((OUT / "pinned-runs/native-evidence-report.v2.json").read_bytes())
n_pass = None
if "counts" in n_report:
    n_pass = n_report["counts"]
elif "result" in n_report:
    n_pass = n_report.get("result")
add(
    "independent-native-case-count",
    nativeCasesFileKeys=sorted(native_cases.keys())[:20] if isinstance(native_cases, dict) else type(native_cases).__name__,
    nativeReportResult=n_report.get("result"),
    nativeReportPassed=n_report.get("passed") if "passed" in n_report else n_report.get("counts"),
)

# executionInputsDigest required on proof schema
schema = json.loads((FOUND / "identity-schemas.v3.json").read_bytes())
proof_req = schema["$defs"]["proof-bundle"]["required"]
assert "executionInputsDigest" in proof_req, proof_req
add("proof-bundle-requires-executionInputsDigest", required=True)

# --- 8. Pin-gate refusal: tamper one pinned file in the disposable copy, run launcher ---
ledger = json.loads((FOUND / "evaluator3-source-pins.v1.json").read_bytes())
target_rel = next(
    item["path"]
    for item in ledger["files"]
    if item["path"].endswith("admission-and-qualification.md")
)
target = COPY / target_rel
orig_bytes = (ORIG / target_rel).read_bytes()
assert hashlib.sha256(target.read_bytes()).hexdigest() == hashlib.sha256(orig_bytes).hexdigest()
target.write_bytes(orig_bytes + b"\n# pin-gate-probe\n")
pin_out = OUT / "pinned-runs" / "pin-gate-refusal"
if pin_out.exists():
    shutil.rmtree(pin_out)
proc = subprocess.run(
    [PY, "-I", "-B", str(FOUND / "run-evaluator3-checks.py"), "--out", str(pin_out)],
    capture_output=True,
    text=True,
    timeout=120,
)
# restore immediately
target.write_bytes(orig_bytes)
assert hashlib.sha256(target.read_bytes()).hexdigest() == hashlib.sha256(orig_bytes).hexdigest()
report = json.loads((pin_out / "report.json").read_text())
assert report["sourcePinsValid"] is False, report
assert report["passed"] is False
assert report.get("checks") in ([], None) or report["checks"] == []
assert target_rel in report["changedOrMissing"]
add(
    "pin-gate-refusal-on-tampered-admission-contract",
    sourcePinsValid=False,
    passed=False,
    launcherExit=proc.returncode,
    changedNamed=target_rel in report["changedOrMissing"],
    childrenNotExecuted=not report["checks"],
    restored=True,
)

# --- 9. Original snapshot still matches after restore ---
assert hashlib.sha256((ORIG / target_rel).read_bytes()).hexdigest() == hashlib.sha256(orig_bytes).hexdigest()
add("original-snapshot-unaltered-after-pin-gate-probe", path=target_rel)

report = {
    "standing": "Independent Grok probes of frozen candidate-subject.v23; synthetic TCB; not product qualification",
    "passed": all(
        r.get("closeRun") != "ACCEPT_FALSE" for r in rows
    )
    and all("error" not in r for r in rows),
    "count": len(rows),
    "results": rows,
    "productQualification": False,
}
print(json.dumps(report, indent=2))
(OUT / "probes" / "independent-probes.v1.json").write_text(json.dumps(report, indent=2) + "\n")
raise SystemExit(0 if report["passed"] else 1)
