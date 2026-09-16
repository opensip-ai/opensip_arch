"""F1 identity source bridge (author-02): executes the PINNED identity/evaluator/native owner code against the proposed successor documents.

It never edits architecture bytes. `build_overlay` writes, into a fresh scratch directory, exact byte copies of the pinned owner files the Run
closure reads, plus exactly three published successor changes:
  1. foundation/identity-schemas.v3.json with ONE optional parameter row added (no requiredForEvaluatorMajors);
  2. foundation/identity-model.v3.py with the parameter document appended to its closed registered-record document list (exact once-only replace);
  3. the new foundation/framework-recognition-plan.schema.v1.json document.
A fourth, fixture-only transformation lets the pinned evaluator3 graph fixture select the optional parameter; it is not an owner change.
`demonstrate` then builds and closes real retained evaluator3 Runs through `close_run`.
"""
import copy
import hashlib
import json

PARAMETER_DOCUMENT = "foundation/framework-recognition-plan.schema.v1.json"
DC = "docs/coop/design-corrections/"
# exact closure of files the fixture build, open_run_closure, evaluator replay and close_run read (traced; bytecode never read)
OVERLAY_FILES = [
    "docs/coop/artifacts/check-fact-plane.py", "docs/coop/artifacts/delivery.v2.json", "docs/coop/artifacts/delivery.v4.json",
    "docs/coop/artifacts/fact-identity-policy.v2.json", "docs/coop/artifacts/rust-provider-protocol.v2.json", DC + "discovery-defaults.py",
    DC + "foundation/atom_model.v1.py", DC + "foundation/canonical.py", DC + "foundation/check-identity.py", DC + "foundation/enumeration-plan.schema.v1.json",
    DC + "foundation/enumeration_model.v1.py", DC + "foundation/evaluator-emission-plan.schema.v1.json", DC + "foundation/evaluator-projection-registry.v1.json",
    DC + "foundation/evaluator_composition_model.v3.py", DC + "foundation/evaluator_graph_fixture.v3.py", DC + "foundation/evaluator_input_model.v3.py",
    DC + "foundation/evaluator_replay_model.v3.py", DC + "foundation/execution-inputs.schema.v1.json", DC + "foundation/execution_inputs_fixture.v3.py",
    DC + "foundation/execution_inputs_model.v1.py", DC + "foundation/identity-model.py", DC + "foundation/identity-model.v3.py", DC + "foundation/identity-schemas.v2.json",
    DC + "foundation/identity-schemas.v3.json", DC + "foundation/import-source-context.schema.json", DC + "foundation/incoming-search.schema.v1.json",
    DC + "foundation/relation-payload-schemas.v2.json", DC + "foundation/subject-inventory.schema.v1.json", DC + "foundation/target-attribution.schema.v1.json",
    DC + "foundation/target-attribution.schema.v2.json", DC + "native/capability-manifest-domains.v2.json", DC + "native/fact-batch.schema.v3.json",
    DC + "native/native-capability-matrix.v2.json", DC + "native/native-cases.v2.json", DC + "native/native-evidence.schemas.v2.json", DC + "native/native_evidence_model.v2.py",
    DC + "native/occupancy-companion.schema.v1.json", DC + "native/protocol3-transitions.v1.json", DC + "native/provider-handshake.schemas.v1.json",
    DC + "native/provider-startup.schemas.v1.json", DC + "native/provider_startup_model.v1.py", DC + "native/provider_wire_model.v1.py",
    DC + "native/typescript-protocol2-order.v1.json", DC + "workflows/schemas/baseline-artifact.schema.json", DC + "workflows/schemas/command-envelope.schema.json",
    DC + "workflows/schemas/command-inventory.schema.json", DC + "workflows/schemas/common.schema.json", DC + "workflows/schemas/comparison-result.schema.json",
    DC + "workflows/schemas/graph-query.schema.json", DC + "workflows/schemas/imported-evidence.schema.json", DC + "workflows/schemas/invocation-record.schema.json",
    DC + "workflows/schemas/policy-document.schema.json", DC + "workflows/schemas/policy-document.v2.schema.json", DC + "workflows/schemas/policy-test.schema.json",
    DC + "workflows/schemas/repair.schema.json", DC + "workflows/schemas/review.schema.json", DC + "workflows/schemas/test-execution.schema.json",
    DC + "workflows/workflows_model.v1.py", DC + "workflows/workflows_model.v3.py",
]
REGISTRY_ROW = {"document": PARAMETER_DOCUMENT, "selector": "#", "owner": "foundation",
                "note": "OPTIONAL FrameworkRecognitionPlanV1 (at most one per spec). Absence is the historical evaluator3 shape and reads as not-plan-bound; new Plans with a compiler language mode carry it under the pre-Plan duty NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED."}
OWNER_TRANSFORMS = [
    {"id": "T1-identity-model-registered-record-document", "owner": "identity", "file": DC + "foundation/identity-model.v3.py",
     "old": "'incoming-search.schema.v1.json','execution-inputs.schema.v1.json']]",
     "new": "'incoming-search.schema.v1.json','execution-inputs.schema.v1.json','framework-recognition-plan.schema.v1.json']]",
     "why": "validate_registered_record admits a foundation parameter payload only through its closed document list (UNREGISTERED_DOCUMENT otherwise)"},
]
FIXTURE_TRANSFORMS = [
    {"id": "F1-fixture-signature", "file": DC + "foundation/evaluator_graph_fixture.v3.py", "old": "clones_fact_subjects=None, clone_body_fact=None):",
     "new": "clones_fact_subjects=None, clone_body_fact=None, recognition_plan=None):"},
    {"id": "F2-fixture-parameter", "file": DC + "foundation/evaluator_graph_fixture.v3.py", "old": "    spec_record={'schemaVersion':2,'requestedCapabilities':",
     "new": "    if recognition_plan is not None:\n        parameters=E.cset(parameters+[{'schemaDigest':blob((HERE/'framework-recognition-plan.schema.v1.json').read_bytes()),'payloadDigest':blob(recognition_plan(enum))}])\n    spec_record={'schemaVersion':2,'requestedCapabilities':"},
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pointer_token(key):
    return key.replace("~", "~0").replace("/", "~1")


def successor_identity_schemas(raw):
    doc = json.loads(raw)
    rows = doc["x-opensip-payload-registry"]["classes"]["parameter"]["rows"]
    assert PARAMETER_DOCUMENT not in rows
    rows[PARAMETER_DOCUMENT] = copy.deepcopy(REGISTRY_ROW)
    return (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def transform(text, rows):
    for row in rows:
        assert text.count(row["old"]) == 1, "transform precondition " + row["id"]
        text = text.replace(row["old"], row["new"])
    return text


def build_overlay(arch, root, parameter_document_raw):
    """-> {relative path: sha256 of the bytes written}. Reads only pinned architecture files."""
    written = {}
    for rel in OVERLAY_FILES:
        raw = (arch / rel).read_bytes()
        if rel == DC + "foundation/identity-schemas.v3.json":
            raw = successor_identity_schemas(raw)
        elif rel == DC + "foundation/identity-model.v3.py":
            raw = transform(raw.decode("utf-8"), OWNER_TRANSFORMS).encode("utf-8")
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        written[rel] = sha(raw)
    target = root / DC / PARAMETER_DOCUMENT
    target.write_bytes(parameter_document_raw)
    written[DC + PARAMETER_DOCUMENT] = sha(parameter_document_raw)
    return written


def positive_run(F, R, **options):
    """evaluator3 reference: build inputs, seal, admit, derive the complete proof, reseal (foundation check-replay.v3 positive())."""
    M = R.M
    graph = F.build_file_inputs(**options)
    seed, objects, blobs, _ = F.seal_fixture(graph)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = graph["inputs"]
    result = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    objects.update(result["objects"])
    blobs.update(result["blobs"])

    def add(domain, fields):
        value = {"schemaVersion": 3, **fields}
        key = M.identifier(domain, value)
        objects[key] = (domain, value)
        return key
    evidence = add("semantic-evidence", {"planId": i["planId"], "viewIds": graph["viewIds"], "coverageIds": graph["coverageIds"], "importIds": i["plan"]["importIds"],
                                         "findingIds": result["proof"]["findingIds"], "proofBundleId": result["proofBundleId"]})
    seal = add("evaluation-seal", {"planId": i["planId"], "executionPlanId": i["executionPlanId"], "evidenceId": evidence, "evaluatorClosure": i["evaluatorClosure"],
                                   "policyDigest": i["plan"]["policyDigest"], "proofBundleId": result["proofBundleId"], "verdict": result["proof"]["verdict"]})
    run = {"schemaVersion": 3, "projectId": graph["snapshot"]["projectId"], "snapshotId": i["plan"]["snapshotId"], "planId": i["planId"], "evidenceId": evidence,
           "evaluationSealId": seal, "capabilityManifestId": i["plan"]["capabilityManifestId"]}
    return run, objects, blobs, graph


def outcome(fn):
    try:
        value = fn()
        return {"result": "admitted", "value": value}
    except Exception as exc:  # the owner models raise their own AdmissionError/EvidenceUnavailable classes
        return {"result": "refused", "code": type(exc).__name__ + ":" + str(exc).split("\n")[0][:160]}


def demonstrate(pred, succ, M, parameter_document_sha256):
    """pred/succ: namespaces with fixture F, replay R, loaded from the pinned tree and from the successor overlay. M: reference model."""
    out = {}
    run, objects, blobs, graph = positive_run(pred.F, pred.R)
    out["predecessorRunClosedByPinnedModel"] = outcome(lambda: str(pred.R.M.close_run(run, objects, blobs))[:80])
    closed = outcome(lambda: str(succ.R.M.close_run(run, objects, blobs))[:80])
    out["predecessorRunClosedBySuccessorModel"] = closed
    _, owner = succ.R.M.open_run_closure(run, objects, blobs)
    parameters = owner["analysisSpec"]["parameters"]
    out["predecessorRunParameters"] = len(parameters)
    out["predecessorRunCustody"] = M.custody_from_parameters(parameters, parameter_document_sha256, {"state": "retained", "missingDigests": []}, {})

    record_holder = {}

    def recognition_plan(enum):
        record = {"schemaVersion": 1, "snapshotId": enum["snapshotId"], "membershipDigest": enum["membershipDigest"], "explicitEntryPoints": [], "units": []}
        record_holder["record"] = record
        return record
    new_run, new_objects, new_blobs, new_graph = positive_run(succ.Fx, succ.R, recognition_plan=recognition_plan)
    out["newPlanRunClosedBySuccessorModel"] = outcome(lambda: str(succ.R.M.close_run(new_run, new_objects, new_blobs))[:80])
    _, new_owner = succ.R.M.open_run_closure(new_run, new_objects, new_blobs)
    new_parameters = new_owner["analysisSpec"]["parameters"]
    record = record_holder["record"]
    payload = M.raw_sha(record)
    out["newPlanRunCustody"] = M.custody_from_parameters(new_parameters, parameter_document_sha256, {"state": "retained", "missingDigests": []}, {payload: record})
    out["newPlanRunCustodyWhenParameterPurged"] = M.custody_from_parameters(new_parameters, parameter_document_sha256, {"state": "purged", "missingDigests": [payload]}, {})
    out["newPlanRunCustodyPartialMissing"] = M.custody_from_parameters(new_parameters, parameter_document_sha256, {"state": "partial", "missingDigests": [payload]}, {})
    out["newPlanRunClosedByPinnedPredecessorModel"] = outcome(lambda: str(pred.R.M.close_run(new_run, new_objects, new_blobs))[:80])
    stripped = {k: v for k, v in new_blobs.items() if k != payload}
    out["newPlanRunWithParameterBytesLost"] = outcome(lambda: str(succ.R.M.close_run(new_run, new_objects, stripped))[:80])
    out["planIdsDiffer"] = run["planId"] != new_run["planId"]

    IM = succ.R.M
    row_key = PARAMETER_DOCUMENT
    lang = IM.SCHEMA["x-opensip-digest-domains"]["languageModes"]["map"]
    spec = copy.deepcopy(owner["analysisSpec"])
    new_spec = copy.deepcopy(new_owner["analysisSpec"])
    compiler_request = [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True}]

    def duty(parameters_, requested):
        IM.admit_parameter_selection(parameters_)
        return M.admit_new_plan_recognition_parameter(parameters_, requested, IM.parameter_row_of, lang, row_key)
    out["duty"] = {
        "syntaxOnlySpecWithoutParameter": outcome(lambda: duty(spec["parameters"], spec["requestedCapabilities"])),
        "compilerSpecWithoutParameter": outcome(lambda: duty(spec["parameters"], compiler_request)),
        "compilerSpecWithParameter": outcome(lambda: duty(new_spec["parameters"], compiler_request)),
        "compilerSpecWithTwoParameters": outcome(lambda: duty(new_spec["parameters"] + [{"schemaDigest": parameter_document_sha256, "payloadDigest": "0" * 64}], compiler_request)),
    }
    out["successorRegistryRowOptional"] = "requiredForEvaluatorMajors" not in IM.PAYLOADS["classes"]["parameter"]["rows"][row_key]
    return out
