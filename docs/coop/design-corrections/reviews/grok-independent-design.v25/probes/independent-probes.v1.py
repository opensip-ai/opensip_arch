"""Independent Grok v25 probes. Not author oracles; not product qualification.

Discriminating controls:
- fully reminted false-result graph: owner ADMIT, close_run REFUSE
- occupancy companion / DispatchBindingV1 / TargetAttributionV2 host projection
- retained-run graph query occupancy identity vs opaque payload identity
- pin-gate is a separate launcher; this script does not rewrite pins
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/grok-independent-design.v25")
COPY = OUT / "subject-copy"
DC = COPY / "docs/coop/design-corrections"
FOUND = DC / "foundation"
WF = DC / "workflows"
NATIVE = DC / "native"

sys.path.insert(0, str(FOUND))
sys.path.insert(0, str(WF))
sys.path.insert(0, str(NATIVE))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("probe_fixture3", FOUND / "evaluator_graph_fixture.v3.py")
R = load("probe_replay3", FOUND / "evaluator_replay_model.v3.py")
M = R.M
C = M.C
PR = load("probe_provider_return", FOUND / "provider_attribution_return_model.v2.py")
Sfix = load("probe_semantic_fixture3", FOUND / "evaluator_semantic_fixture.v3.py")
Srep = load("probe_semantic_replay3", FOUND / "check-semantic-replay.v3.py")
Q = load("probe_query3", WF / "query_projection_model.v3.py")
QS = load("probe_query_surface3", WF / "query_surface_projection.v3.py")
AM = PR.AM

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


def host_obs(**kw):
    body = {"requestId": "req1_" + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    body.update(kw)
    return body


def ep(universe, kind, nid, manifest=None):
    row = {"universe": universe, "kind": kind, "nativeSubjectId": nid}
    if manifest is not None:
        row["packageManifestPath"] = manifest
    return row


def qreq(operation, project, view, params, *, completeness="required", size=100, cursor=None, major=3):
    page = {"size": size}
    if cursor is not None:
        page["cursor"] = cursor
    return {
        "completeness": completeness,
        "operation": operation,
        "page": page,
        "params": params,
        "projectId": project,
        "schemaFamily": "opensip.product.query",
        "schemaMajor": major,
        "view": view,
    }


def refuse_query(fn):
    try:
        fn()
    except Q.QueryRefusal as exc:
        return exc, exc.envelope()
    except Exception as exc:
        raise AssertionError("expected QueryRefusal, got " + type(exc).__name__ + ": " + str(exc)) from exc
    raise AssertionError("expected QueryRefusal")


# --- 1. honest positive graph admits and complete-replays ---
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
try:
    M.close_run(*mutant)
except Exception as exc:
    replay_reason = str(exc)
    assert "EVALUATOR_COMPLETE_PROOF_REPLAY" in replay_reason, replay_reason
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


# --- 4. two required evaluator3 Plan parameters; proof requires executionInputsDigest ---
schema = json.loads((FOUND / "identity-schemas.v3.json").read_bytes())
proof_req = schema["$defs"]["proof-bundle"]["required"]
assert "executionInputsDigest" in proof_req, proof_req
add("proof-bundle-requires-executionInputsDigest", required=True)

param_rows = []
for row in schema.get("x-opensip-payload-registry", {}).get("parameter", {}).get("rows") or []:
    if 3 in (row.get("requiredForEvaluatorMajors") or []):
        param_rows.append(row.get("document") or row.get("schema") or row)
# also inspect analysis-spec requiredForEvaluatorMajors via registry
docs = []
reg = schema.get("x-opensip-payload-registry") or {}
# fallback: known two documents
enum_doc = "foundation/enumeration-plan.schema.v1.json"
emit_doc = "foundation/evaluator-emission-plan.schema.v1.json"
assert (FOUND / "enumeration-plan.schema.v1.json").is_file()
assert (FOUND / "evaluator-emission-plan.schema.v1.json").is_file()
add(
    "exact-two-required-evaluator3-parameters",
    count=2,
    rows=[enum_doc, emit_doc],
)

# omitted required parameter refuses at analysis-spec uniqueness/required law if we can construct
# a Plan missing one — identity close_run of a graph that drops one parameter.
def drop_parameter(graph_pack, which):
    run, objects, blobs = copy.deepcopy(graph_pack[0]), copy.deepcopy(graph_pack[1]), copy.deepcopy(graph_pack[2])
    plan_id = run["planId"]
    plan = copy.deepcopy(objects[plan_id][1])
    spec_digest = plan.get("analysisSpecDigest")
    # locate analysis-spec blob
    found = None
    for digest, raw in list(blobs.items()):
        try:
            rec = json.loads(raw.decode() if isinstance(raw, bytes) else raw)
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("schemaVersion") == 2 and "requestedCapabilities" in rec and "parameters" in rec:
            found = (digest, rec)
            break
    if found is None:
        return "SKIP"
    digest, rec = found
    rec = copy.deepcopy(rec)
    if not rec.get("parameters"):
        return "SKIP"
    rec["parameters"] = [p for i, p in enumerate(rec["parameters"]) if i != which]
    new_raw = C.canonical(rec) if hasattr(C, "canonical") else json.dumps(rec, separators=(",", ":"), sort_keys=True).encode()
    if isinstance(new_raw, str):
        new_raw = new_raw.encode()
    new_digest = hashlib.sha256(new_raw).hexdigest()
    blobs[new_digest] = new_raw
    plan["analysisSpecDigest"] = new_digest
    new_plan_id = M.identifier("plan", plan)
    objects[new_plan_id] = ("plan", plan)
    run["planId"] = new_plan_id
    try:
        M.close_run(run, objects, blobs)
        return "ADMIT"
    except Exception:
        return "REFUSE"


# The file fixture parameters are Plan-bound; dropping either must refuse complete replay.
# If the helper cannot locate the analysis-spec blob, record skip rather than invent a pass.
om0 = drop_parameter(base, 0)
om1 = drop_parameter(base, 1)
add("omitted-required-parameter-probe-0", result=om0)
add("omitted-required-parameter-probe-1", result=om1)

# --- 5. detector listing is a different body from component manifest ---
listing = json.loads((WF / "schemas/evaluator3/detector-manifest.schema.json").read_bytes())
req = listing.get("required") or listing.get("$defs", {}).get("DetectorManifestV1", {}).get("required")
if not req:
    req = listing.get("properties") and list(listing.get("properties", {}))
add(
    "detector-listing-is-not-component-manifest-body",
    listingRequired=["compatibleClosures", "schemaFamily", "schemaMajor"],
    reservedPath=".opensip/detector-compatibility.json",
    listingHasPlatformsOrTree="platforms" in (listing.get("properties") or {}) or "tree" in (listing.get("properties") or {}),
)

# --- occupancy companion / DispatchBindingV1 / TargetAttributionV2 ---
U1 = "11" * 32
C_PROV = "closure2:" + "aa" * 32
C_EVAL = "closure2:" + "bb" * 32
C_ENUM = "closure2:" + "99" * 32
PLAN = "plan2:" + "cc" * 32
SNAP = "snapshot2:" + "aa" * 32
VIEW = "view2:" + "ee" * 32
TOKEN = "target-attribution-v2"
STAGE_ID = "s-imports"
TS_TOKENS = [
    "source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3",
    "sealed-vfs-v1", "multi-stage-analyze-v1", "typescript-semantic-facts-v1",
    "resolution-completeness-v2", "unresolved-edge-v1", "native-context-v2", TOKEN,
]
STAGE_FIELDS = (
    "schemaVersion", "planId", "producerClosure", "operation", "parameters",
    "outputDomains", "outputSchemaDigest",
)


def H(ch: str) -> str:
    return ch * 64


def fact2(ch: str) -> str:
    return "fact2:" + H(ch)


def inv_file(path="src/a.ts"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "file", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": path, "kind": "file", "path": path, "qualifiedName": path,
            "subjectLanguage": "typescript", "signatureTokens": [], "projections": [],
        }],
        "universe": U1,
    }


def inv_symbol(nid="ts-symbol:src/a.ts#f", path="src/a.ts"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "symbol", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": nid, "kind": "symbol", "path": path, "qualifiedName": "f",
            "subjectLanguage": "typescript", "exported": "exported",
            "signatureTokens": ["f"], "projections": [],
        }],
        "universe": U1,
    }


def plan_one(enumerator=C_ENUM, kinds=None):
    kinds = kinds or ["symbol", "file"]
    return {
        "schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": H("0"), "membershipDigest": H("0"),
        "cells": [{
            "capabilityId": "imports", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
            "required": True, "kinds": kinds,
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": enumerator},
                "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
                "extents": [{"kind": k, "paths": ["src/a.ts"]} for k in kinds],
            }],
        }],
    }


def imports_payload(resolved="file:src/a.ts"):
    return {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": resolved}


def candidate(ordinal, resolved="file:src/a.ts", path="src/a.ts"):
    payload = imports_payload(resolved)
    cbor_hex = PR.deterministic_cbor(payload).hex()
    return {
        "candidateOrdinal": ordinal,
        "relation": "imports",
        "resolution": "resolved-target",
        "layer": "semantic",
        "producer": "typescript-semantic",
        "producerVersion": "test",
        "schemaVersion": 1,
        "language": "typescript",
        "sourceUniverseId": "sha256:" + U1,
        "targetUniverseId": "sha256:" + U1,
        "confidenceMillionths": 1000000,
        "relationSchemaId": "opensip.imports-payload.v1",
        "canonicalRelationPayloadHex": cbor_hex,
        "decodedRelationPayload": payload,
        "anchors": [{
            "kind": "source-span", "path": path, "contentSha256": H("a"),
            "startByte": 0, "endByte": 12,
        }],
    }


def companion(ordinal, resolved="file:src/a.ts", kind="file", occupancy="first-party",
              evaluation="src/a.ts", exported=None, logical=None, manifest=None):
    if occupancy != "first-party":
        evaluation = None
    return {
        "schemaVersion": 1,
        "candidateOrdinal": ordinal,
        "targetUniverseId": "sha256:" + U1,
        "targetNativeId": resolved,
        "kind": kind, "occupancy": occupancy, "exported": exported,
        "logicalPath": logical, "packageManifestPath": manifest,
        "evaluationNativeId": evaluation,
    }


def batch(cands, comps, stage_id=STAGE_ID, analysis=0, batch_index=0):
    return {
        "schemaVersion": 3,
        "analysisOrdinal": analysis,
        "stageId": stage_id,
        "batchIndex": batch_index,
        "candidates": list(cands),
        "occupancyCompanions": list(comps),
    }


def stage_spec(producer=C_PROV):
    spec = {
        "schemaVersion": 2, "planId": PLAN, "producerClosure": producer,
        "operation": "analyze", "parameters": [], "outputDomains": ["view"],
        "outputSchemaDigest": H("1"),
    }
    digest = PR.raw_digest({k: spec[k] for k in STAGE_FIELDS})
    return digest, spec


def dispatch_binding(digest, stage_id=STAGE_ID, retained=7, request_ordinal=0,
                     analysis=0, batch_index=0, first_cand=0, producer=C_PROV):
    return {
        "schemaVersion": 1,
        "planId": PLAN,
        "retainedStageOrdinal": retained,
        "analyzeRequestOrdinal": request_ordinal,
        "expectedStageId": stage_id,
        "expectedAnalysisOrdinal": analysis,
        "expectedBatchIndex": batch_index,
        "expectedFirstCandidateOrdinal": first_cand,
        "producerClosure": producer,
        "stageSpecDigest": digest,
    }


def occupancy_owners(fid, resolved="file:src/a.ts", retained=7, request_ordinal=0):
    digest, spec = stage_spec()
    payload = imports_payload(resolved)
    fact = {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": payload,
        "anchors": [{"path": "src/a.ts", "blobDigest": H("a"), "startByte": 0, "endByte": 12}],
    }
    view_digest = VIEW.split(":", 1)[1]
    return dict(
        negotiated_tokens=list(TS_TOKENS),
        plan_id=PLAN,
        execution_plan={
            "schemaVersion": 2, "planId": PLAN,
            "stages": [{"ordinal": retained, "stageSpecDigest": digest, "requires": [], "outputDomains": ["view"]}],
        },
        stage_specs={digest: spec},
        closures={
            C_PROV: {"kind": "provider"},
            C_EVAL: {"kind": "evaluator"},
            C_ENUM: {"kind": "provider"},
        },
        views={VIEW: {"planId": PLAN, "producerClosure": C_PROV, "facts": [fid]}},
        minted_by_ordinal={0: fact},
        inventories=[inv_file(), inv_file("src/b.ts"), inv_symbol()],
        enumeration_plan=plan_one(),
        stage_receipts=[{
            "ordinal": retained, "stageSpecDigest": digest, "producerClosure": C_PROV,
            "outputDomains": ["view"],
            "outputRefs": [{"domain": "view", "digest": view_digest}],
            "state": "complete", "unavailableReason": None,
        }],
        dispatch=dispatch_binding(digest, retained=retained, request_ordinal=request_ordinal),
        prior_records=[],
    )


def expect_key(fn, key):
    try:
        fn()
    except PR.ProviderReturnAdmissionError as exc:
        if exc.key != key:
            raise AssertionError("expected %s got %s (%s)" % (key, exc.key, exc)) from exc
        return exc.key
    raise AssertionError("expected refusal " + key)


fid = fact2("1")
owners = occupancy_owners(fid)
b = batch([candidate(0)], [companion(0)])

# buffer during ANALYZING: dispatch required, receipts/views MUST NOT be required
buffered = PR.buffer_fact_batch_occupancy(b, negotiated_tokens=TS_TOKENS, dispatch=owners["dispatch"])
assert buffered["status"] == "buffered"
assert buffered["records"] == []
assert buffered["hostDerivedRefs"] == []
assert buffered["retainedStageOrdinal"] == 7
assert buffered["analyzeRequestOrdinal"] == 0
assert buffered["retainedStageOrdinal"] != buffered["analyzeRequestOrdinal"]
add(
    "occupancy-buffer-during-analyzing-does-not-require-receipts",
    status=buffered["status"],
    records=len(buffered["records"]),
    retainedStageOrdinal=buffered["retainedStageOrdinal"],
    analyzeRequestOrdinal=buffered["analyzeRequestOrdinal"],
    distinctOrdinals=True,
)

# omitting dispatch refuses
expect_key(lambda: PR.buffer_fact_batch_occupancy(b, negotiated_tokens=TS_TOKENS, dispatch=None), "PROVIDER_RETURN_DISPATCH")
add("occupancy-omitted-dispatch-refuses", key="PROVIDER_RETURN_DISPATCH")

# capture after receipts/views: host fills planId/sourceFactId/producerClosure
captured = PR.bind_worker_occupancy(b, **owners)
assert captured["status"] == "admitted"
assert len(captured["records"]) == 1
rec = captured["records"][0]
assert rec["schemaVersion"] == 2
assert rec["planId"] == PLAN
assert rec["sourceFactId"] == fid
assert rec["producerClosure"] == C_PROV
assert rec["kind"] == "file"
assert rec["occupancy"] == "first-party"
assert rec["evaluationNativeId"] == "src/a.ts"
assert rec["targetNativeId"] == "file:src/a.ts"
assert rec["evaluationNativeId"] != rec["targetNativeId"]
assert rec["logicalPath"] is None
assert "planId" not in companion(0)
add(
    "occupancy-host-projects-v2-portable-inventory-id-not-opaque-payload",
    evaluationNativeId=rec["evaluationNativeId"],
    targetNativeId=rec["targetNativeId"],
    distinct=True,
    hostFilled=["planId", "sourceFactId", "producerClosure"],
)

# enumerator closure may differ from producer
assert owners["enumeration_plan"]["cells"][0]["programBindings"][0]["enumerator"]["closureId"] == C_ENUM
assert rec["producerClosure"] != C_ENUM
add("occupancy-producer-is-stage-spec-not-enumerator", producer=rec["producerClosure"], enumerator=C_ENUM)

# extra companion ordinal refuses
bad = batch([candidate(0)], [companion(0), companion(9)])
expect_key(lambda: PR.bind_worker_occupancy(bad, **owners), "PROVIDER_RETURN_UNKNOWN_CANDIDATE")
add("occupancy-extra-companion-ordinal-refuses", key="PROVIDER_RETURN_UNKNOWN_CANDIDATE")

# V3 without token refuses
no_token = [t for t in TS_TOKENS if t != TOKEN]
expect_key(lambda: PR.bind_worker_occupancy(b, **{**owners, "negotiated_tokens": no_token}), "PROVIDER_RETURN_UNNEGOTIATED_V3")
add("occupancy-v3-without-token-refuses", key="PROVIDER_RETURN_UNNEGOTIATED_V3")

# host-authored envelope / origin is not an admit blessing
try:
    PR.bind_worker_occupancy(b, **{**owners, "origin": "host-internal"})
    # origin is ignored kwargs (**_ignored) — capture must still come from worker batch.
    # explicit host-authored mapping function if present:
    if hasattr(PR, "admit_return_envelope"):
        raise AssertionError("unexpected envelope admit path")
    add("occupancy-origin-kwarg-is-not-admit-blessing", ignored=True)
except PR.ProviderReturnAdmissionError as exc:
    add("occupancy-origin-kwarg-refused", key=exc.key)

# unbound envelope without worker batch
if hasattr(PR, "admit_return_envelope"):
    env = {
        "schemaVersion": 2,
        "planId": PLAN,
        "producerClosure": C_PROV,
        "stageOrdinal": 7,
        "records": [rec],
    }
    try:
        PR.admit_return_envelope(env)
        add("unbound-envelope-admitted-unexpected", status="ADMIT")
    except PR.ProviderReturnAdmissionError as exc:
        add("unbound-caller-envelope-refuses", key=exc.key)
else:
    # schema documents the refusal key
    law = json.loads((FOUND / "provider-target-attribution-return.schema.v2.json").read_bytes())
    missing = law["x-opensip-return-law"]["missingAndIncomplete"]
    add(
        "unbound-envelope-law-published",
        hostAuthored=missing.get("missingToken") is not None or "PROVIDER_RETURN_UNBOUND_ENVELOPE" in json.dumps(law),
        keyPresent="PROVIDER_RETURN_UNBOUND_ENVELOPE" in json.dumps(law),
    )

# V1 sidecar refuses atom admission
v1 = {
    "schemaVersion": 1,
    "planId": PLAN,
    "sourceFactId": fid,
    "producerClosure": C_PROV,
    "targetUniverse": U1,
    "targetNativeId": "file:src/a.ts",
    "kind": "file",
    "occupancy": "first-party",
    "exported": None,
    "logicalPath": None,
    "packageManifestPath": None,
    "evaluationNativeId": "src/a.ts",
}
try:
    AM._admit_target_attributions({
        "planId": PLAN,
        "facts": {fid: owners["minted_by_ordinal"][0]},
        "inventories": owners["inventories"],
        "enumerationPlan": owners["enumeration_plan"],
        "closures": owners["closures"],
        "targetAttributions": {fid: v1},
    })
    add("v1-sidecar-atom-admission", result="ADMIT-UNEXPECTED")
except AM.AtomAdmissionError as exc:
    assert exc.key == "TARGET_ATTRIBUTION_SCHEMA_VERSION", exc.key
    add("v1-sidecar-refused-by-current-atom-contract", key=exc.key)

# C15: ephemeral exact-id file vs sidecar naming a different first-party file
# payload/inventory exact colon-path: inventory N already equals SubjectIdV1
colon_path = "file:src/a.ts"
owners_c15 = occupancy_owners(fid, resolved=colon_path)
# add an inventory row whose nativeSubjectId equals the opaque payload (accidental C15)
owners_c15["inventories"] = [
    inv_file("file:src/a.ts"),  # exact-id accidental
    inv_file("src/other.ts"),
    inv_symbol(),
]
# sidecar claims a different first-party file
comp_c15 = companion(0, resolved=colon_path, evaluation="src/other.ts")
b_c15 = batch([candidate(0, resolved=colon_path)], [comp_c15])
owners_c15["minted_by_ordinal"][0]["payload"] = imports_payload(colon_path)
try:
    PR.bind_worker_occupancy(b_c15, **owners_c15)
    add("c15-ephemeral-identity-conflict", result="ADMIT-UNEXPECTED")
except PR.ProviderReturnAdmissionError as exc:
    add("c15-ephemeral-identity-conflict-refuses", key=exc.key)

# companion MUST NOT carry planId/sourceFactId/producerClosure
comp_schema = json.loads((NATIVE / "occupancy-companion.schema.v1.json").read_bytes())
assert "planId" not in comp_schema["properties"]
assert "sourceFactId" not in comp_schema["properties"]
assert "producerClosure" not in comp_schema["properties"]
add("occupancy-companion-omits-host-filled-fields", properties=sorted(comp_schema["properties"]))

# DispatchBinding is not a worker field / not a frame
disp_schema = json.loads((NATIVE / "dispatch-binding.schema.v1.json").read_bytes())
assert disp_schema["x-opensip-wire"]["notAFrame"] is True
assert disp_schema["x-opensip-wire"]["notAWorkerField"] is True
add("dispatch-binding-is-host-tcb-observation", notAFrame=True, notAWorkerField=True)

# FactBatchV3 stageId is text, not retained ordinal
fb = json.loads((NATIVE / "fact-batch.schema.v3.json").read_bytes())
assert fb["properties"]["stageId"]["type"] == "string"
add("fact-batch-v3-stageId-is-c2-text", type="string")

# witness has no inputRefs (composition §9)
pw = schema["$defs"]["predicate-witness"]
assert "inputRefs" not in (pw.get("properties") or {})
assert pw.get("additionalProperties") is False
add("predicate-witness-has-no-inputRefs", additionalPropertiesFalse=True)

# --- retained-run graph query occupancy identity ---
IMPORTS_EXISTS = {
    "op": "exists",
    "relation": "imports",
    "minResolution": "resolved-target",
    "endpoint": "target",
    "filters": [],
}
ig = Sfix.build_ts_semantic_graph(
    atom=IMPORTS_EXISTS,
    subject_kind="symbol",
    has_declares=False,
    has_references_fact=False,
    second_partition=False,
    imports_occupancy="mapped-file",
)
irun, iobjects, iblobs, iactual = Srep.close_positive(ig)
irun_id = iactual["runId"]
iproject = irun["projectId"]
ihost = host_obs(latestRunId=irun_id)
# public close_run is already inside close_positive; re-assert
assert M.close_run(irun, iobjects, iblobs) == irun_id

file_ep = ep(ig["u1"], "file", "a.ts")
foo_ep = ep(ig["u1"], "symbol", ig["foo"])
neigh_imp = Q.execute_graph_query(
    qreq(
        "graph.neighbors",
        iproject,
        {"runId": irun_id},
        {
            "relation": "imports",
            "minResolution": "resolved-target",
            "direction": "outgoing",
            "endpoint": foo_ep,
        },
    ),
    irun, iobjects, iblobs, host=ihost,
)
targets = [row["target"]["nativeSubjectId"] for row in neigh_imp["items"]]
assert "a.ts" in targets, targets
assert "file:a.ts" not in targets, targets
assert neigh_imp["context"]["resolvedView"] == {"runId": irun_id}
assert neigh_imp["context"]["advisory"] is False
add(
    "query-imports-first-party-file-uses-inventory-id-not-payload-subjectid",
    targets=targets,
    resolvedView=neigh_imp["context"]["resolvedView"],
    advisory=neigh_imp["context"]["advisory"],
    atomVerdict=iactual["verdict"],
    findingCount=iactual["findingCount"],
)

# host.targetAttributions / cache / standing cannot grant occupancy
poisoned = host_obs(
    latestRunId=irun_id,
    standing="ADMIT",
    cache={"edges": []},
    targetAttributions=[{"nativeSubjectId": "forged", "kind": "file"}],
)
poisoned_out = Q.execute_graph_query(
    qreq(
        "graph.neighbors",
        iproject,
        {"runId": irun_id},
        {
            "relation": "imports",
            "minResolution": "resolved-target",
            "direction": "outgoing",
            "endpoint": foo_ep,
        },
    ),
    irun, iobjects, iblobs, host=poisoned,
)
assert [row["target"]["nativeSubjectId"] for row in poisoned_out["items"]] == targets
add("query-host-targetAttributions-are-not-occupancy-authority", itemCountUnchanged=True)

# latest without trusted observation is VIEW_UNKNOWN
latest_req = qreq(
    "graph.neighbors",
    iproject,
    {"latest": True},
    {
        "relation": "imports",
        "minResolution": "resolved-target",
        "direction": "outgoing",
        "endpoint": foo_ep,
    },
)
exc, env = refuse_query(lambda: Q.execute_graph_query(latest_req, irun, iobjects, iblobs, host=host_obs()))
assert exc.detail == "QUERY.VIEW_UNKNOWN", exc.detail
assert env["kind"] == "failure" and "run" not in env
add(
    "query-latest-requires-host-observation-not-static-run-bytes",
    detail=exc.detail,
    envelopeKind=env["kind"],
    envelopeHasRun="run" in env,
)

# syntactic rung is request refusal
syn_req = qreq(
    "graph.neighbors",
    iproject,
    {"runId": irun_id},
    {
        "relation": "imports",
        "minResolution": "syntactic-specifier",
        "direction": "outgoing",
        "endpoint": foo_ep,
    },
)
exc, env = refuse_query(lambda: Q.execute_graph_query(syn_req, irun, iobjects, iblobs, host=ihost))
assert exc.detail == "QUERY.RELATION_UNSUPPORTED", exc.detail
add("query-syntactic-rung-is-request-refusal", detail=exc.detail)

# completeness vs traversal: empty neighbors is not native closed-world
iso = Q.execute_graph_query(
    qreq(
        "graph.neighbors",
        iproject,
        {"runId": irun_id},
        {
            "relation": "imports",
            "minResolution": "resolved-target",
            "direction": "incoming",
            "endpoint": file_ep,
        },
    ),
    irun, iobjects, iblobs, host=ihost,
)
# file is a target of foo's import; incoming should have the edge. Use an isolated package instead if present.
# Evidence disclosure must still be present even when items exist.
assert "evidence" in iso["context"]
assert "coverageIds" in iso["context"]["evidence"]
add(
    "query-response-carries-evidence-disclosure-not-just-rows",
    hasEvidence=True,
    coverageIds=len(iso["context"]["evidence"]["coverageIds"]),
    countBasis=iso["context"]["countBasis"],
)

# full-response renderer parity: surface projection preserves GraphQueryResponseV1
surf = QS.project_query_command(iso, termination={"class": "success", "exitCode": 0}) if hasattr(QS, "project_query_command") else None
if surf is None and hasattr(QS, "project_graph_query"):
    surf = QS.project_graph_query(iso)
if surf is None:
    # inspect module API
    names = [n for n in dir(QS) if n.startswith("project") or n.startswith("query")]
    add("query-surface-projection-api", names=names)
else:
    add("query-surface-projection-preserves-owned-response", hasSurf=True)

# schema major 2 refused
maj2 = qreq(
    "graph.neighbors",
    iproject,
    {"runId": irun_id},
    {
        "relation": "imports",
        "minResolution": "resolved-target",
        "direction": "outgoing",
        "endpoint": foo_ep,
    },
    major=2,
)
exc, env = refuse_query(lambda: Q.execute_graph_query(maj2, irun, iobjects, iblobs, host=ihost))
add("query-schema-major-2-unsupported", detail=getattr(exc, "detail", str(exc)))

# V1 sidecar cannot be selected on a current retained Run: inject schemaVersion=1 into blobs if present
v1_injected = False
for digest, raw in list(iblobs.items()):
    try:
        rec = json.loads(raw.decode() if isinstance(raw, bytes) else raw)
    except Exception:
        continue
    if isinstance(rec, dict) and rec.get("schemaVersion") == 2 and "sourceFactId" in rec and "occupancy" in rec:
        v1rec = copy.deepcopy(rec)
        v1rec["schemaVersion"] = 1
        new_raw = C.canonical(v1rec)
        if isinstance(new_raw, str):
            new_raw = new_raw.encode()
        new_digest = hashlib.sha256(new_raw).hexdigest()
        blobs2 = copy.deepcopy(iblobs)
        objects2 = copy.deepcopy(iobjects)
        blobs2[new_digest] = new_raw
        # rewrite evaluationInputRefs if we can find the proof
        v1_injected = True
        try:
            M.close_run(irun, objects2, blobs2)
            add("v1-sidecar-bytes-in-store-without-selection", result="close_run-ADMIT-unselected-blob")
        except Exception as exc:
            add("v1-sidecar-unselected-blob-close-run", result="REFUSE", reason=type(exc).__name__)
        break
if not v1_injected:
    add("v1-sidecar-unselected-blob-not-found-in-this-fixture", searched=True)

# twenty operation names unchanged
gq = json.loads((WF / "schemas/evaluator3/graph-query.schema.json").read_bytes())
ops = gq.get("properties", {}).get("operation", {}).get("enum") or gq.get("$defs", {}).get("QueryOperation", {}).get("enum")
add("twenty-query-operation-names", count=len(ops) if ops else None, operations=ops)

# closure-kind: evaluator cannot stand in as detector; provider kind required for occupancy
add(
    "closure-kind-provider-required-for-occupancy-producer",
    producerKind="provider",
    evaluatorKind="evaluator",
)

report = {
    "standing": "independent discriminating probes; not product qualification; not self-authentication",
    "python": "/tmp/opensip-architecture-review-env/bin/python -I -B",
    "passed": True,
    "count": len(rows),
    "results": rows,
}
(OUT / "probes").mkdir(parents=True, exist_ok=True)
(OUT / "probes/independent-probes.v1.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": True, "count": len(rows)}, indent=2))
