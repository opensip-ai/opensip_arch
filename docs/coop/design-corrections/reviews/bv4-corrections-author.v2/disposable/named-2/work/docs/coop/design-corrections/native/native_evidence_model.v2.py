"""Native evidence reference model v2 (design evidence only).

Standing: PROPOSED design reference for docs/v2/contracts/product-v1/native-evidence.md.
It is not a product implementation, not an OS/native qualification, and executes no
compiler, provider or repository code. Every function consumes explicitly marked
TRUSTED OBSERVATION INPUTS (the fixtures say what a provider or adapter would have
observed); the model decides what the host must then do. Canonical encoding, exact
integer admission and product envelope identities are imported from the foundation
unit (foundation/canonical.py, foundation/identity-model.py); this file authors no
second serializer.
"""
from __future__ import annotations

import copy
import hashlib
import unicodedata
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
FOUNDATION = HERE.parent / "foundation"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("identity_canonical", FOUNDATION / "canonical.py")          # exact parse/canonical/identity/validate
IM = _load("identity_model", FOUNDATION / "identity-model.py")         # identifier('import', wrapper) -> import2:<hex>
DD = _load("discovery_defaults", HERE.parent / "discovery-defaults.py")   # ONE shared discovery rule (security + native), MUST-3
SCHEMAS = json.loads((HERE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))
# The CLOSED per-language grammar capability mapping, read from the published registry rather than
# restated here, so syntaxClass is a registered property of a language and not a caller choice.
GRAMMAR_CAPABILITY_REGISTRY = SCHEMAS["x-opensip-grammar-capability-registry"]
# The CLOSED per-deficiency cause-carrier mapping, likewise read from the published registry: which
# retained field carries a deficiency's cause and what that field must say. Section 10's Cause column
# names unresolved-edge classes, export states and derivation kinds for three of its rows, none of
# which the closed NativeCause enum can express, so the pair had to be either mis-typed or null.
DEFICIENCY_CAUSE_REGISTRY = SCHEMAS["x-opensip-deficiency-cause-registry"]
# THE capability vocabulary authority: the closed capability x languageMode matrix, whose
# capabilityIdLaw names it as the vocabulary for analysis-spec requestedCapabilities[].capabilityId,
# for product-configuration analysis.capabilities and for the authenticated release declaration
# registry. Read here rather than restated so a capability cannot be registered in one place only.
CAPABILITY_MATRIX = json.loads((HERE / "native-capability-matrix.v2.json").read_text(encoding="utf-8"))
AdmissionError = C.AdmissionError


# ---------------------------------------------------------------------------
# Identity helpers (all product hashing delegated to foundation/canonical.py)
# ---------------------------------------------------------------------------

def raw_sha256(data: bytes) -> str:
    """Raw SHA256 over exact bytes: blob digests, payloadDigest, payloadSchemaDigest."""
    return hashlib.sha256(data).hexdigest()


def validate_native(def_name: str, value: Any) -> Any:
    schema = copy.deepcopy(SCHEMAS)
    schema["$ref"] = "#/$defs/" + def_name
    return C.validate(schema, value)


_FOUNDATION_SCHEMAS = json.loads((FOUNDATION / "identity-schemas.v2.json").read_text(encoding="utf-8"))
# The clone body-identity language domain, READ from the foundation record rather than restated.
# native-evidence section 6.3 closes it to the languages that have body spans and a published
# L1-L3 normalisation table; a bundled data/document grammar is deliberately not a member.
BODY_LANGUAGE_IDS = frozenset(
    _FOUNDATION_SCHEMAS["$defs"]["body-language-version"]["properties"]["languageId"]["enum"])


def validate_foundation(def_name: str, value: Any) -> Any:
    schema = copy.deepcopy(_FOUNDATION_SCHEMAS); schema["$ref"] = "#/$defs/" + def_name
    return C.validate(schema, value)


def subject_discriminator_projection(signature_tokens: list[str], collision_class: list[list[str]]) -> str:
    """Compiler-owned declaration signature, in grammar order; no body/location tokens.
    The actual parser projection is qualified separately for each detector closure.
    """
    if not signature_tokens or any(type(t) is not str for t in signature_tokens):
        raise AdmissionError('SUBJECT_SIGNATURE_TOKENS_REQUIRED')
    return IM.subject_discriminator(signature_tokens, collision_class)


def native_context_closure_projection(stdlib: dict, rust_dev_llvm: dict) -> dict:
    """Exact native-context v2 successor fields; descriptors/trees stay in the closure."""
    if stdlib.get('kind') != 'stdlib' or rust_dev_llvm.get('kind') != 'rust-dev-llvm':
        raise AdmissionError('NATIVE_CONTEXT_CLOSURE_KIND_MISMATCH')
    return {'typescriptStdlibMerkleRoot': IM.identifier('closure', stdlib).removeprefix('closure2:'),
            'rustcDevLlvmDigest': IM.identifier('closure', rust_dev_llvm).removeprefix('closure2:')}


def native_identity(domain: str, def_name: str, descriptor: Any) -> str:
    """H(domain, typed semantic record) under the joint recipe; distinct from raw_sha256."""
    validate_native(def_name, descriptor)
    return "sha256:" + C.identity(domain, descriptor)




# ---------------------------------------------------------------------------
# import2: one common wrapper; ONE canonical payload schema document per kind (review v2 item 3)
# ---------------------------------------------------------------------------
# Joint decision: runtime/test/history payloads are the workflow owner's RuntimePayloadV1 /
# TestPayloadV1 / HistoryPayloadV1 (single canonical schema documents and domains). Native owns
# DependencySourcePayloadV1 / PreparedOutputPayloadV1. The native runtime-coverage / test-results /
# history structures are INPUT ADAPTER SHAPES ONLY: they are normalized to the canonical workflow
# payload BEFORE import2_wrap, and import2_wrap refuses them.

REPO = HERE.parents[3]
WORKFLOW_SCHEMAS_DIR = HERE.parent / "workflows" / "schemas"
# Schema document paths are spelled exactly as the workflow PayloadRegistryV1 spells them (relative to
# docs/coop/design-corrections/).
NATIVE_SCHEMA_DOC = "native/native-evidence.schemas.v2.json"
WORKFLOW_IMPORTED_DOC = "workflows/schemas/imported-evidence.schema.json"
WORKFLOW_TEST_DOC = "workflows/schemas/test-execution.schema.json"
WORKFLOW_COMMON_DOC = "workflows/schemas/common.schema.json"
CORRECTIONS_DIR = HERE.parent


def schema_document_digest(registry_relative: str) -> str:
    """payloadSchemaDigest = raw SHA-256 of the EXACT FULL schema document file bytes (joint decision),
    never the canonicalization of a selected $def."""
    return raw_sha256((CORRECTIONS_DIR / registry_relative).read_bytes())


def _workflow_doc(registry_relative: str) -> dict:
    return json.loads((CORRECTIONS_DIR / registry_relative).read_text(encoding="utf-8"))


_WORKFLOW_DOCS = {name: _workflow_doc(name) for name in (WORKFLOW_IMPORTED_DOC, WORKFLOW_TEST_DOC, WORKFLOW_COMMON_DOC)}


def _workflow_registry():
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    return Registry().with_resources([(d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in _WORKFLOW_DOCS.values()])


def validate_workflow(doc: str, selector: str, value: Any) -> Any:
    """Validate against the workflow owner's pinned schema document (cross-document refs resolved through the
    pinned registry closure, no network) under the foundation exact-typed validator."""
    C.typed(value)
    sid = _WORKFLOW_DOCS[doc]["$id"]
    C.ExactValidator({"$ref": sid + selector}, registry=_workflow_registry()).validate(value)
    return value


IMPORT_REGISTRY: dict[str, dict] = {
    # kind -> exactly one (schema document, selector, payload domain, owner)
    "runtime": {"schemaDocument": WORKFLOW_IMPORTED_DOC, "selector": "#/$defs/RuntimePayloadV1", "payloadDomain": "workflow.import-payload.runtime.v1", "owner": "workflow"},
    "test": {"schemaDocument": WORKFLOW_TEST_DOC, "selector": "#/$defs/TestPayloadV1", "payloadDomain": "workflow.import-payload.test.v1", "owner": "workflow"},
    "history": {"schemaDocument": WORKFLOW_IMPORTED_DOC, "selector": "#/$defs/HistoryPayloadV1", "payloadDomain": "workflow.import-payload.history.v1", "owner": "workflow"},
    "dependency": {"schemaDocument": NATIVE_SCHEMA_DOC, "selector": "#/$defs/DependencySourcePayloadV1", "payloadDomain": "native.import-payload.dependency-source.v1", "owner": "native"},
    "prepared": {"schemaDocument": NATIVE_SCHEMA_DOC, "selector": "#/$defs/PreparedOutputPayloadV1", "payloadDomain": "native.import-payload.prepared-output.v1", "owner": "native"},
}
ADAPTER_INPUT_SHAPES = {"RuntimeCoverageAdapterInputV1", "TestResultsAdapterInputV1", "HistoryAdapterInputV1"}


def import_registry_rows() -> list[dict]:
    rows = []
    for kind, r in IMPORT_REGISTRY.items():
        row = {"kind": kind, **r, "schemaDocumentSha256": schema_document_digest(r["schemaDocument"])}
        validate_native("ImportRegistryRowV1", row); rows.append(row)
    return rows


def validate_import_payload(kind: str, payload: Any) -> None:
    r = IMPORT_REGISTRY[kind]
    if r["owner"] == "native":
        validate_native(r["selector"].rsplit("/", 1)[-1], payload)
    else:
        validate_workflow(r["schemaDocument"], r["selector"], payload)


def validate_source_correspondence(correspondence: dict) -> dict:
    """Workflow shared SourceCorrespondence (common.schema.json): exact-snapshot | vcs-revision. There is no
    declared-build kind: a build string alone never maps."""
    return validate_workflow(WORKFLOW_COMMON_DOC, "#/$defs/SourceCorrespondence", correspondence)


def _looks_like_adapter_shape(payload: Any) -> str | None:
    if not isinstance(payload, dict) or "payloadDomain" in payload:
        return None
    for def_name in sorted(ADAPTER_INPUT_SHAPES):
        try:
            validate_native(def_name, payload); return def_name
        except Exception:  # noqa: BLE001
            continue
    return None


def import2_wrap(kind: str, payload: dict, correspondence: dict, producer_closure: str,
                 adapter_closure: str, blobs: list[dict], scope: dict, observation: dict,
                 completeness: str, omissions: list[str]) -> dict:
    """Build the foundation import2 wrapper around the ONE canonical payload for `kind`.
    Auxiliary digest recipes JOIN the workflow owner's CURRENT schema (imported-evidence.schema.json
    #ImportWrapperV2), which agrees with identity-and-evidence §2: every auxiliary digest is the raw SHA-256 of
    the canonical bytes of an exact closed record retained as a blob; importId is the only H-domain identity.
      payloadSchemaDigest        = raw SHA-256(schema DOCUMENT bytes)              (PayloadRegistryV1 row)
      payloadDigest              = raw SHA-256(canonical payload)
      sourceCorrespondenceDigest = raw SHA-256(canonical common#SourceCorrespondence)
      buildDigest                = raw SHA-256(canonical BuildIdentityV1{schemaVersion:1, buildIdentity})
      scopeDigest                = raw SHA-256(canonical ImportScopeDescriptor == foundation scope-descriptor)
      observationDigest          = raw SHA-256(canonical ImportObservationV1)
    Both native and workflow wrappers use these same preimages; the integration checker compares their bytes."""
    if kind not in IMPORT_REGISTRY:
        raise AdmissionError("UNKNOWN_IMPORT_KIND")
    shape = _looks_like_adapter_shape(payload)
    if shape is not None:
        raise AdmissionError(f"UNNORMALIZED_ADAPTER_SHAPE:{shape}: normalize to the canonical workflow payload before import2")
    reg = IMPORT_REGISTRY[kind]
    if payload.get("payloadDomain") != reg["payloadDomain"]:
        raise AdmissionError("IMPORT.KIND_PAYLOAD_MISMATCH")
    validate_import_payload(kind, payload)
    validate_source_correspondence(correspondence)
    validate_foundation("scope-descriptor", scope)
    obs = {"schemaVersion": 1, "kind": kind, "window": None, "population": None, "selection": None, "revisionRange": None, **observation}
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/ImportObservationV1", obs)
    build = {"schemaVersion": 1, "buildIdentity": correspondence.get("buildIdentity")}
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/BuildIdentityV1", build)
    if completeness != "complete" and not omissions:
        raise AdmissionError("INCOMPLETE_IMPORT_MUST_LIST_OMISSIONS")
    wrapper = {
        "schemaVersion": 2, "kind": kind,
        "payloadSchemaDigest": schema_document_digest(reg["schemaDocument"]),
        "payloadDigest": raw_sha256(C.canonical(payload)),
        "sourceCorrespondenceDigest": raw_sha256(C.canonical(correspondence)),
        "buildDigest": raw_sha256(C.canonical(build)),
        "producerClosure": producer_closure, "adapterClosure": adapter_closure,
        "blobs": sorted(blobs, key=lambda b: b["path"].encode("utf-8")),
        "scopeDigest": raw_sha256(C.canonical(scope)),
        "observationDigest": raw_sha256(C.canonical(obs)),
        "completeness": completeness, "omissions": sorted(set(omissions)),
    }
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/ImportWrapperV2", wrapper)
    import_id = IM.identifier("import", wrapper)
    return {"importId": import_id, "wrapper": wrapper, "payloadDigest": wrapper["payloadDigest"],
            "payloadSchemaDigest": wrapper["payloadSchemaDigest"], "payloadDomain": reg["payloadDomain"],
            "schemaDocument": reg["schemaDocument"], "selector": reg["selector"], "owner": reg["owner"],
            "retainedBlobs": {"correspondence": correspondence, "build": build, "scope": scope, "observation": obs},
            "hDomainIdentitiesInWrapper": []}


# --- native input adapter shapes -> canonical workflow payloads -------------------------------

def normalize_runtime_coverage(adapter_input: dict) -> dict:
    """RuntimeCoverageAdapterInputV1 -> workflow RuntimePayloadV1. Subject states map 1:1 onto the workflow
    observability enum; hits are carried only for observed-hit / observable-unhit."""
    validate_native("RuntimeCoverageAdapterInputV1", adapter_input)
    subjects = []
    for s in adapter_input["subjects"]:
        row = {"path": s["path"], "observability": s["state"]}
        if s["state"] in ("observed-hit", "observable-unhit"):
            row["hits"] = s["hits"]
        if s.get("symbol"):
            row["symbol"] = s["symbol"]
        subjects.append(row)
    subjects.sort(key=lambda r: (r["path"].encode("utf-8"), r.get("symbol", "").encode("utf-8")))
    payload = {"payloadDomain": "workflow.import-payload.runtime.v1", "format": adapter_input["format"],
               "observationWindow": {"startUtc": adapter_input["window"]["startUtc"], "endUtc": adapter_input["window"]["endUtc"]},
               "observedPopulation": adapter_input["population"]["kind"], "subjects": subjects,
               "mappingGaps": list(adapter_input["mappingGaps"])}
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/RuntimePayloadV1", payload)
    return {"payload": payload, "requiredOmissions": []}


def normalize_test_results(adapter_input: dict) -> dict:
    """TestResultsAdapterInputV1 -> workflow TestPayloadV1 (producer independent-prepared). Output that the
    external run did not capture is an OMISSION the wrapper must list, never an invented empty capture."""
    validate_native("TestResultsAdapterInputV1", adapter_input)
    empty = raw_sha256(b"")
    omissions = []
    stdout = adapter_input["stdoutSha256"]; stderr = adapter_input["stderrSha256"]
    if stdout is None:
        omissions.append("stdout-not-captured"); stdout = empty
    if stderr is None:
        omissions.append("stderr-not-captured"); stderr = empty
    if not adapter_input["argv"]:
        omissions.append("argv-not-recorded")
    tests = []
    for t in adapter_input["tests"]:
        row = {"testId": t["testId"], "outcome": t["outcome"]}
        if t["subjectPath"] is not None:
            row["subjectPath"] = t["subjectPath"]
        if t["durationMillis"] is not None:
            row["durationMillis"] = t["durationMillis"]
        tests.append(row)
    payload = {"payloadDomain": "workflow.import-payload.test.v1", "producer": "independent-prepared",
               "argvDigest": raw_sha256(C.canonical(adapter_input["argv"])), "toolClosureId": None,
               "exitStatus": None, "signal": None, "timedOut": False, "stdoutDigest": stdout, "stderrDigest": stderr,
               "stdoutBytes": 0, "stderrBytes": 0, "outputTruncated": False, "tests": tests,
               "selection": dict(adapter_input["selection"])}
    validate_workflow(WORKFLOW_TEST_DOC, "#/$defs/TestPayloadV1", payload)
    return {"payload": payload, "requiredOmissions": sorted(omissions),
            "selectionCompletenessEstablished": adapter_input["selection"]["completenessEstablished"]}


def normalize_history(adapter_input: dict) -> dict:
    """HistoryAdapterInputV1 (commits oldest->newest) -> workflow HistoryPayloadV1 (per-path change counts)."""
    validate_native("HistoryAdapterInputV1", adapter_input)
    counts: dict[str, int] = {}; last: dict[str, str] = {}
    for c in adapter_input["commits"]:
        for p in c["changedPaths"]:
            counts[p] = counts.get(p, 0) + 1; last[p] = c["id"]
    subjects = [{"path": p, "changeCount": counts[p], "lastChangedCommit": last[p]} for p in sorted(counts, key=lambda x: x.encode("utf-8"))]
    payload = {"payloadDomain": "workflow.import-payload.history.v1", "vcsSystem": "git",
               "revisionRange": {"from": adapter_input["range"]["fromCommitId"], "to": adapter_input["range"]["toCommitId"],
                                 "commitCount": len(adapter_input["commits"]), "truncated": adapter_input["bounded"]["truncated"]},
               "collectionScope": "all-paths", "subjects": subjects}
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/HistoryPayloadV1", payload)
    return {"payload": payload, "requiredOmissions": ["history-truncated"] if adapter_input["bounded"]["truncated"] else []}


def import_correspondence(correspondence: dict, admitted_snapshots: dict[str, dict[str, str]],
                          source_mapping: dict | None = None) -> dict:
    """Mapping law (review v2 item 3), joined to the workflow's SourceMappingV1. admitted_snapshots (TRUSTED
    INPUT): {snapshot2 id: {path: inventory sha256}}. exact-snapshot: mapped iff the snapshot2 is admitted.
    vcs-revision: mapped only through an admitted SourceMappingV1 whose raw digest equals the correspondence's
    sourceMappingDigest, whose snapshot2 is admitted, and whose EVERY entry's sourceSha256 equals the admitted
    snapshot's inventory digest at sourcePath. A clean commit name alone, or a declared build string alone, is
    a statement and never maps (IMPORT.SOURCE_MAPPING_REQUIRED, unmapped-only)."""
    validate_source_correspondence(correspondence)
    if correspondence["kind"] == "exact-snapshot":
        sid = correspondence["snapshotId"]
        return {"state": "mapped" if sid in admitted_snapshots else "unmapped", "snapshotId": sid if sid in admitted_snapshots else None,
                "basis": "exact-snapshot" if sid in admitted_snapshots else "snapshot-not-admitted"}
    rev = correspondence["vcsRevision"]
    if correspondence["sourceMappingDigest"] is None or source_mapping is None:
        return {"state": "unmapped", "snapshotId": None, "basis": "commit-name-alone-never-maps", "detail": "IMPORT.SOURCE_MAPPING_REQUIRED"}
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/SourceMappingV1", source_mapping)
    if raw_sha256(C.canonical(source_mapping)) != correspondence["sourceMappingDigest"]:
        return {"state": "unmapped", "snapshotId": None, "basis": "source-mapping-digest-mismatch"}
    if rev["dirty"]:
        return {"state": "unmapped", "snapshotId": None, "basis": "commit-dirty"}
    snap = admitted_snapshots.get(source_mapping["snapshotId"])
    if snap is None:
        return {"state": "unmapped", "snapshotId": None, "basis": "snapshot-not-admitted"}
    mismatched = sorted(e["generatedPath"] for e in source_mapping["entries"] if snap.get(e["sourcePath"]) != e["sourceSha256"])
    if mismatched:
        return {"state": "unmapped", "snapshotId": None, "basis": "per-file-mapping-incomplete", "mismatched": mismatched}
    return {"state": "mapped", "snapshotId": source_mapping["snapshotId"], "basis": "verified-per-file-source-mapping",
            "consumableGeneratedPaths": sorted(e["generatedPath"] for e in source_mapping["entries"])}


def runtime_coverage_semantics(payload: dict, correspondence_state: str) -> dict:
    """Over the canonical workflow RuntimePayloadV1. observable-unhit != unused; unobservable/unmapped != unhit;
    one window != universal non-use."""
    validate_workflow(WORKFLOW_IMPORTED_DOC, "#/$defs/RuntimePayloadV1", payload)
    counts = {"observed-hit": 0, "observable-unhit": 0, "unobservable": 0, "unmapped": 0}
    if correspondence_state != "mapped":
        counts["unmapped"] = len(payload["subjects"])
    else:
        for s in payload["subjects"]:
            counts[s["observability"]] += 1
    return {"counts": counts, "universalNonUseClaimPermitted": False,
            "consumableAsUnhit": counts["observable-unhit"] if correspondence_state == "mapped" else 0}


# ---------------------------------------------------------------------------
# Negotiation: identity versions before disclosure (feedback 1)
# ---------------------------------------------------------------------------

IDENTITY_TOKENS = ["source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3"]
RUST3_TOKENS = IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "rust-semantic-facts-v1",
                                  "resolution-completeness-v2", "unresolved-edge-v1", "dependency-source-v1",
                                  "prepared-output-v3", "native-context-v2"]
TS2_TOKENS = IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "typescript-semantic-facts-v1",
                                "resolution-completeness-v2", "unresolved-edge-v1", "native-context-v2"]


def negotiate(plan_required: list[str], signed_row: list[str], hello_ack: list[str] | None) -> dict:
    """Plan-time (no spawn) then Hello/HelloAck (no source bytes). snapshot2/plan2/fact2/coverage-v3
    are mandatory for every major-3/major-2 worker: a row lacking them is never spawned."""
    required = sorted(set(plan_required) | set(IDENTITY_TOKENS))
    missing = sorted(set(required) - set(signed_row))
    if missing:
        return {"stage": "plan-time", "spawned": False, "sourceBytesSent": False, "outcome": "coverage-unknown",
                "deficiency": "provider-unavailable", "nativeCause": "capability-missing", "missingTokens": missing,
                "d9": {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.PROVIDER_UNAVAILABLE"}}
    expected = sorted(set(signed_row))
    if hello_ack is None:
        return {"stage": "hello", "spawned": True, "sourceBytesSent": False, "outcome": "awaiting-hello-ack",
                "expectedCapabilities": expected}
    if sorted(set(hello_ack)) != expected or len(hello_ack) != len(set(hello_ack)):
        return {"stage": "hello-ack", "spawned": True, "sourceBytesSent": False, "outcome": "FAULT",
                "d9": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION"}}
    return {"stage": "hello-ack", "spawned": True, "sourceBytesSent": False, "outcome": "accepted",
            "identityNegotiated": all(t in hello_ack for t in IDENTITY_TOKENS), "next": "OpenUniverse"}


PROTOCOL3_PHASES = [
    "START", "WAIT_HELLO_ACK", "READY_OPEN_UNIVERSE", "WAIT_UNIVERSE_ACCEPTED", "READY_SNAPSHOT_MANIFEST",
    "RECEIVING_SNAPSHOT", "WAIT_SNAPSHOT_ACCEPTED", "READY_DEPENDENCY_MANIFEST", "RECEIVING_DEPENDENCY",
    "WAIT_DEPENDENCY_ACCEPTED", "READY_PREPARED_MANIFEST", "RECEIVING_PREPARED", "WAIT_PREPARED_ACCEPTED",
    "WAIT_NATIVE_CONTEXT_VERIFIED", "READY_ANALYZE", "ANALYZING", "READY_COMPLETE", "WAIT_CANCELLED",
    "WAIT_ZERO_EXIT", "WAIT_EOF", "DONE", "FAULT",
]
PROTOCOL3_RULES: list[dict] = [
    {"id": "P3-01", "phase": "START", "frame": "Hello", "next": "WAIT_HELLO_ACK"},
    {"id": "P3-02", "phase": "WAIT_HELLO_ACK", "frame": "HelloAck", "next": "READY_OPEN_UNIVERSE"},
    {"id": "P3-03", "phase": "READY_OPEN_UNIVERSE", "frame": "OpenUniverse", "guard": {"identityNegotiated": True}, "next": "WAIT_UNIVERSE_ACCEPTED"},
    {"id": "P3-04", "phase": "WAIT_UNIVERSE_ACCEPTED", "frame": "UniverseAccepted", "next": "READY_SNAPSHOT_MANIFEST"},
    {"id": "P3-05", "phase": "READY_SNAPSHOT_MANIFEST", "frame": "SnapshotManifest", "next": "RECEIVING_SNAPSHOT"},
    {"id": "P3-06", "phase": "RECEIVING_SNAPSHOT", "frame": "SnapshotFileChunk", "next": "RECEIVING_SNAPSHOT"},
    {"id": "P3-07", "phase": "RECEIVING_SNAPSHOT", "frame": "SnapshotSeal", "next": "WAIT_SNAPSHOT_ACCEPTED"},
    {"id": "P3-08", "phase": "WAIT_SNAPSHOT_ACCEPTED", "frame": "SnapshotAccepted", "guard": {"dependencyMode": True}, "next": "READY_DEPENDENCY_MANIFEST"},
    {"id": "P3-09", "phase": "WAIT_SNAPSHOT_ACCEPTED", "frame": "SnapshotAccepted", "guard": {"dependencyMode": False, "preparedMode": True}, "next": "READY_PREPARED_MANIFEST"},
    {"id": "P3-10", "phase": "WAIT_SNAPSHOT_ACCEPTED", "frame": "SnapshotAccepted", "guard": {"dependencyMode": False, "preparedMode": False}, "next": "WAIT_NATIVE_CONTEXT_VERIFIED"},
    {"id": "P3-11", "phase": "READY_DEPENDENCY_MANIFEST", "frame": "DependencySourceManifest", "next": "RECEIVING_DEPENDENCY"},
    {"id": "P3-12", "phase": "RECEIVING_DEPENDENCY", "frame": "DependencySourceChunk", "next": "RECEIVING_DEPENDENCY"},
    {"id": "P3-13", "phase": "RECEIVING_DEPENDENCY", "frame": "DependencySourceSeal", "next": "WAIT_DEPENDENCY_ACCEPTED"},
    {"id": "P3-14", "phase": "WAIT_DEPENDENCY_ACCEPTED", "frame": "DependencySourceAccepted", "guard": {"preparedMode": True}, "next": "READY_PREPARED_MANIFEST"},
    {"id": "P3-15", "phase": "WAIT_DEPENDENCY_ACCEPTED", "frame": "DependencySourceAccepted", "guard": {"preparedMode": False}, "next": "WAIT_NATIVE_CONTEXT_VERIFIED"},
    {"id": "P3-16", "phase": "READY_PREPARED_MANIFEST", "frame": "PreparedOutputManifest", "next": "RECEIVING_PREPARED"},
    {"id": "P3-17", "phase": "RECEIVING_PREPARED", "frame": "PreparedOutputChunk", "next": "RECEIVING_PREPARED"},
    {"id": "P3-18", "phase": "RECEIVING_PREPARED", "frame": "PreparedOutputSeal", "next": "WAIT_PREPARED_ACCEPTED"},
    {"id": "P3-19", "phase": "WAIT_PREPARED_ACCEPTED", "frame": "PreparedOutputAccepted", "next": "WAIT_NATIVE_CONTEXT_VERIFIED"},
    {"id": "P3-20", "phase": "WAIT_NATIVE_CONTEXT_VERIFIED", "frame": "NativeContextVerified", "next": "READY_ANALYZE"},
    {"id": "P3-21", "phase": "WAIT_NATIVE_CONTEXT_VERIFIED", "frame": "Unavailable", "next": "WAIT_ZERO_EXIT", "terminal": "unavailable"},
    {"id": "P3-22", "phase": "READY_ANALYZE", "frame": "Analyze", "next": "ANALYZING"},
    {"id": "P3-23", "phase": "ANALYZING", "frame": "FactBatch", "next": "ANALYZING"},
    {"id": "P3-24", "phase": "ANALYZING", "frame": "CoverageV3", "next": "ANALYZING_OR_READY_COMPLETE"},
    {"id": "P3-25", "phase": "ANALYZING", "frame": "Unavailable", "next": "WAIT_ZERO_EXIT", "terminal": "unavailable"},
    {"id": "P3-26", "phase": "ANALYZING", "frame": "BudgetExhausted", "next": "WAIT_ZERO_EXIT", "terminal": "budget-exhausted"},
    {"id": "P3-27", "phase": "READY_COMPLETE", "frame": "Complete", "next": "WAIT_ZERO_EXIT", "terminal": "complete"},
    {"id": "P3-28", "phase": "*PRE_COMPLETE", "frame": "ProviderFault", "next": "WAIT_ZERO_EXIT", "terminal": "provider-fault"},
    {"id": "P3-29", "phase": "*PRE_COMPLETE", "frame": "Cancel", "next": "WAIT_CANCELLED"},
    {"id": "P3-30", "phase": "WAIT_CANCELLED", "frame": "Cancelled", "next": "WAIT_ZERO_EXIT", "terminal": "cancelled"},
    {"id": "P3-31", "phase": "WAIT_ZERO_EXIT", "frame": "zero-exit", "next": "WAIT_EOF"},
    {"id": "P3-32", "phase": "WAIT_EOF", "frame": "eof", "next": "DONE"},
    {"id": "P3-33", "phase": "*ANY", "frame": "*PROCESS_FAULT", "next": "FAULT"},
    {"id": "P3-34", "phase": "*ANY", "frame": "*", "next": "FAULT"},
]
_PRE_COMPLETE = PROTOCOL3_PHASES[1:17]
_PROCESS_FAULTS = {"nonzero-exit", "signal-death", "deadline", "stdout-byte"}
_SOURCE_FRAMES = {"OpenUniverse", "SnapshotManifest", "SnapshotFileChunk", "DependencySourceManifest",
                  "DependencySourceChunk", "PreparedOutputManifest", "PreparedOutputChunk"}


def protocol3_run(events: list[dict], stage_count: int = 1) -> dict:
    """Host-side transition system. OpenUniverse (which carries snapshot2 and plan2) is admitted only
    after HelloAck negotiated every identity token; otherwise the run FAULTs with no disclosure."""
    state = {"phase": "START", "dependencyMode": False, "preparedMode": False, "identityNegotiated": False,
             "stageIndex": 0, "stageCount": 0, "terminalKind": None, "sourceBytesSent": False,
             "stagesCompleted": 0}
    trace: list[str] = []
    for ev in events:
        phase, frame = state["phase"], ev["frame"]
        if phase == "FAULT":
            trace.append("FAULT-absorb"); continue
        if phase in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in ("zero-exit", "eof") and frame not in _PROCESS_FAULTS:
            state["phase"] = "FAULT"; trace.append("post-terminal-frame"); continue
        if frame in _PROCESS_FAULTS:
            state["phase"] = "FAULT"; trace.append("P3-33"); continue
        matched = None
        for rule in PROTOCOL3_RULES:
            rp = rule["phase"]
            if rp == "*ANY":
                continue
            if rp == "*PRE_COMPLETE":
                if phase not in _PRE_COMPLETE:
                    continue
            elif rp != phase:
                continue
            if rule["frame"] != frame:
                continue
            if any(state.get(k) != v for k, v in rule.get("guard", {}).items()):
                continue
            matched = rule; break
        if matched is None:
            state["phase"] = "FAULT"; trace.append("P3-34"); continue
        if frame == "HelloAck":
            state["identityNegotiated"] = all(t in ev.get("capabilities", []) for t in IDENTITY_TOKENS)
        if frame == "OpenUniverse":
            state["dependencyMode"] = bool(ev.get("dependencyMode", False))
            state["preparedMode"] = bool(ev.get("preparedMode", False))
        if frame == "Analyze":
            state["stageCount"] = stage_count; state["stageIndex"] = 0
        if frame in _SOURCE_FRAMES:
            state["sourceBytesSent"] = True
        nxt = matched["next"]
        if nxt == "ANALYZING_OR_READY_COMPLETE":
            state["stageIndex"] += 1; state["stagesCompleted"] += 1
            nxt = "READY_COMPLETE" if state["stageIndex"] == state["stageCount"] else "ANALYZING"
        if "terminal" in matched:
            state["terminalKind"] = matched["terminal"]
        state["phase"] = nxt; trace.append(matched["id"])
    return {"finalPhase": state["phase"], "terminalKind": state["terminalKind"], "sourceBytesSent": state["sourceBytesSent"],
            "stagesCompleted": state["stagesCompleted"], "identityNegotiated": state["identityNegotiated"], "trace": trace}


# ---------------------------------------------------------------------------
# Relation registry, resolution completeness, sufficiency (feedback 6, 7, 12)
# ---------------------------------------------------------------------------

_RELATION_REGISTRY = json.loads(
    (FOUNDATION / "relation-payload-schemas.v2.json").read_text(encoding="utf-8")
)["x-opensip-relation-registry"]

# Read from the single authority rather than restated here. This module previously carried its own
# copy; that made four independent ladder sources (inherited fact-plane, this dict, the capability
# domain registry, and the foundation registry that the identity contract actually names), and they
# had already drifted -- the capability registry's arrays were alphabetised, reversing calls,
# imports and references. Order is load-bearing here: _rung_index compares ladder positions.
LADDERS: dict[str, list[str]] = {
    name: list(row["ladder"]) for name, row in _RELATION_REGISTRY["relations"].items()
}
DEPENDS_ON = {"reachability": [{"relation": "calls", "minResolution": "resolved-callee"}],
              "clones": [{"relation": "declares", "minResolution": "syntactic"}]}
RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"}
PRECEDENCE_V1 = ["language-tier-unsupported", "provider-unavailable", "budget-exhausted", "confidence-floor-unmet", "required-relation-missing"]
PRECEDENCE_V2 = ["language-tier-unsupported", "provider-unavailable", "input-closure-incomplete", "budget-exhausted",
                 "confidence-floor-unmet", "derivation-policy-unmet", "resolution-incomplete", "external-consumers-unknown", "required-relation-missing"]
RUNG_CAUSE = {"language-tier": "language-tier-unsupported", "provider-not-installed": "provider-unavailable",
              "budget": "budget-exhausted", "input-closure": "input-closure-incomplete"}
UNRESOLVED_EDGE_KINDS = SCHEMAS["$defs"]["UnresolvedEdgeKindV1"]["enum"]
RC_STATES = ["complete", "incomplete", "partial", "not-attempted", "not-applicable"]


def _rung_index(relation: str, rung: str) -> int | None:
    ladder = LADDERS.get(relation)
    return None if ladder is None or rung not in ladder else ladder.index(rung)


def sufficiency_v1(req: dict, view: dict, depth: int = 0) -> dict:
    """Mirror of the accepted fact-plane v1 rule (counterexample oracle, AR-12). Reads one scalar
    coverage value per relation and knows nothing about resolution completeness."""
    rel = req["relation"]; entry = view.get(rel)
    if entry is None:
        return {"satisfied": False, "deficiency": "required-relation-missing"}
    have_i, need_i = _rung_index(rel, entry["resolution"]), _rung_index(rel, req["minResolution"])
    if have_i is None or need_i is None:
        return {"satisfied": False, "deficiency": "required-relation-missing"}
    causes: list[str] = []
    if have_i < need_i:
        causes.append(RUNG_CAUSE.get(entry.get("rungUnavailableBecause", ""), "required-relation-missing"))
    if entry.get("confidenceMillionths", 1000000) < req.get("minConfidenceMillionths", 0):
        causes.append("confidence-floor-unmet")
    if req["completeness"] == "complete" and entry.get("coverage") != "complete":
        causes.append(RUNG_CAUSE.get(entry.get("rungUnavailableBecause", ""), "required-relation-missing"))
    if depth < 4:
        for dep in DEPENDS_ON.get(rel, []):
            sub = sufficiency_v1({**dep, "completeness": "partial-ok"}, view, depth + 1)
            if not sub["satisfied"]:
                causes.append(sub["deficiency"])
    if not causes:
        return {"satisfied": True}
    return {"satisfied": False, "deficiency": min(causes, key=lambda c: PRECEDENCE_V1.index(c) if c in PRECEDENCE_V1 else 99)}


def validate_requirement_v2(req: dict, control: bool) -> list[str]:
    errors: list[str] = []
    try:
        validate_native("RequirementV2", req)
    except Exception as exc:  # jsonschema ValidationError or AdmissionError
        return [f"schema: {getattr(exc, 'message', str(exc))}"]
    if req["minResolution"] not in LADDERS[req["relation"]]:
        errors.append("minResolution is not a rung of this relation's ladder")
    if req["quantifier"] == "universal-negative" and req["completeness"] != "complete":
        errors.append("universal-negative requires completeness=complete")
    if control and req["quantifier"] == "universal-negative":
        if req["unresolvedEdgePolicy"] != "forbid":
            errors.append("Control universal-negative requires unresolvedEdgePolicy=forbid")
        if req["externalConsumerPolicy"] != "forbid":
            errors.append("Control universal-negative requires externalConsumerPolicy=forbid")
    if req.get("derivationPolicy", "any") != "any" and req["relation"] != "types":
        errors.append("derivationPolicy applies to relation types only")
    return errors


# --------------------------------------------------------------------------- clone ownership disclosure
# The three refusable states of the languageVersionBinding selection law, paired with the typed
# Coverage disclosure each one owes. Adding the NativeCause members was necessary and NOT sufficient:
# a vocabulary nothing derives and nothing enforces leaves the disclosure optional in practice, which
# is exactly what the retained-Run counterexamples showed (an unrelated `budget-exhausted` with a null
# cause satisfied the old prerequisite). This table is the single place the pair is decided.
CLONE_OWNERSHIP_DISCLOSURE = {
    "ownership-missing": {"refusal": "BODY_LANGUAGE_OWNERSHIP_REQUIRED",
                          "deficiency": "input-closure-incomplete",
                          "nativeCause": "body-language-ownership-missing"},
    "owner-unenumerated": {"refusal": "BODY_LANGUAGE_OWNER_UNENUMERATED",
                           "deficiency": "input-closure-incomplete",
                           "nativeCause": "body-language-owner-unenumerated"},
    "owner-ambiguous": {"refusal": "BODY_LANGUAGE_OWNER_AMBIGUOUS",
                        "deficiency": "input-closure-incomplete",
                        "nativeCause": "body-language-owner-ambiguous"},
}


# --------------------------------------------------------------- syntax-universe capability support
# The closed capability registry above is the authority for WHICH relation@rung a bundled grammar can
# bear. An earlier revision consulted it only when validating a grammar descriptor's declared
# syntaxClass, so it constrained what a bundle could SAY ABOUT ITSELF and not what a Run could CLAIM:
# a Markdown-anchored declares fact admitted, an empty declares/clones scope over a data-only
# repository claimed COMPLETE, and a syntax universe minted references@resolved-binding while its own
# record declared resolutionAttempted=false. The two functions below are the capability law at the
# actual Run boundary. Neither trusts a claimed coverage value, a caller-declared class, or the
# presence or absence of facts.
INVENTORY_CAPABILITIES = frozenset({"file@enumerated", "package@manifest-declared", "vcs-change@vcs-reported"})
# The published disclosure for a well-formed request the universe cannot serve. Both members already
# exist: the capability matrix uses `language-tier-unsupported` for exactly these cells, and
# `capability-missing` is an existing NativeCause. No new vocabulary is introduced.
UNAVAILABLE_CAPABILITY_DISCLOSURE = {"deficiency": "language-tier-unsupported",
                                     "nativeCause": "capability-missing"}


def grammar_of_path(path: str, selected_rows) -> dict | None:
    """The SELECTED grammar ROW that reads this path, by longest suffix over the rows' OWN
    `suffixes`.

    Row suffix ownership, not a language set: the descriptor lets a row claim a SUBSET of its
    language's bundled suffixes, and two rows of one language may own disjoint suffixes. Admission
    only requires that a claimed suffix belong to that language and that no suffix be claimed twice;
    it does NOT require a row to claim its language's whole global set. Reducing the selection to
    languageIds therefore loses exactly the information that decides whether a path was read - a
    selected TypeScript row owning `.ts` says nothing about `.tsx` if no selected row owns `.tsx`.

    Longest match wins over the union of selected rows' suffixes, so `.d.ts` still resolves through
    a row owning `.ts`. A path no selected row owns returns None: an unselected, missing or foreign
    grammar never masquerades as a supported one."""
    best, best_row = None, None
    for row in selected_rows:
        for suffix in row.get("suffixes", ()):
            if path.endswith(suffix) and (best is None or len(suffix) > len(best)):
                best, best_row = suffix, row
    return best_row


def syntax_capability_support(selected_rows, relation: str, rung: str,
                              paths: list[str], require_all: bool) -> dict | None:
    """Is `relation@rung` supported by this syntax universe? None means supported.

    `selected_languages` are the languages of the grammars the UNIVERSE COMMITTED to select, so an
    unselected grammar cannot lend its capability to another. Support is read from the closed
    per-language registry, never from the request.

    Two modes, because two different things are decidable from a retained Run:

    * `require_all=True` (a nonempty FACT): EVERY named path - the fact's own anchors - must be read
      by a selected grammar whose registry capability set contains this capability. This is what
      stops a Markdown-anchored `declares` fact, in a pure or a mixed repository alike.
    * `require_all=False` (a requested SCOPE, including an empty view): at least one path in the
      committed examined extent must be readable by such a grammar. It never inspects whether facts
      exist, so an empty view is judged on the same evidence as a populated one.

    INVENTORY capabilities are always supported and are deliberately NOT grammar-gated: a snapshot
    inventories every file it contains, including ones no bundled grammar reads, and requiring a
    grammar per inventory row would silently narrow that promise.

    Returns the published unavailable disclosure when unsupported."""
    capability = relation + "@" + rung
    if capability in INVENTORY_CAPABILITIES:
        return None
    registry = GRAMMAR_CAPABILITY_REGISTRY["languages"]
    # Only the SELECTED rows whose own language bears this capability can read a path for it.
    supporting = [row for row in selected_rows
                  if capability in registry.get(row["languageId"], {}).get("capabilities", ())]
    if not supporting:
        # No selected grammar bears this capability at all. Every semantic rung
        # (references/imports/calls/types/reachability) and unresolved-edge lands here under a
        # syntax universe, which is what the matrix already says: a grammar-only universe attempts
        # no resolution, so it can carry no resolved rung.
        return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
    readable = [grammar_of_path(p, supporting) is not None for p in paths]
    if require_all:
        # An EMPTY path list is unsupported, never vacuously true: an unanchored code fact names no
        # file that could have been read, so `all([])` must not admit it.
        if not paths or not all(readable):
            return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
        return None
    if not any(readable):
        return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
    return None


def deficiency_cause_faults(entry: dict) -> list[str]:
    """Is this entry's DECLARED (deficiency, nativeCause) pair supported by the entry's OWN committed
    evidence? Returns the refusals; empty means supported.

    The direction matters and is deliberately one-way. What is decidable from an entry alone is
    whether a declared deficiency is CONTRADICTED by the record that carries it. What is NOT
    decidable is whether an exhibited condition OBLIGES a deficiency: several conditions are
    requirement-relative (the confidence floor lives in RequirementV2, and external-consumer state
    matters only for a universal negative about an exported target), and RC-3 makes `coverage:
    complete` with `state: incomplete` and no deficiency a valid honest entry. Deriving an
    obligation from the entry would therefore refuse lawful Runs, so this asks the answerable
    question and the registry states the limit rather than papering over it.

    Every carrier is read from the published registry, never restated here, and every one of them
    already existed and is already closed - no enum anywhere changes. Three of section 10's rows
    name causes the closed NativeCause cannot express, and for those the registry names the
    structured field that does carry them: `resolutionCompleteness` (whose unresolvedEdgeClasses
    array holds ALL applicable classes at once, which is why enum members would have been the wrong
    fix), `closedWorld.exportsClosed`, and `derivationKinds`. Their nativeCause is null BY DESIGN and
    that null is no longer an escape: the named field must actually carry the cause."""
    deficiency, cause = entry["deficiency"], entry["nativeCause"]
    if deficiency is None:
        # A cause without a deficiency names why nothing went wrong.
        return [] if cause is None else ["native.coverage-cause-without-deficiency:" + str(cause)]
    row = DEFICIENCY_CAUSE_REGISTRY["deficiencies"].get(deficiency)
    if row is None:
        return ["native.coverage-cause-registry-row-missing:" + deficiency]
    faults: list[str] = []
    # Some deficiencies exist only for one relation because their OWNING law does. Section 4.7 and
    # sufficiency_v2 apply derivationPolicy only where `rel == "types"`, so no other relation's entry
    # can be short of a derivation policy. Checking the carrier alone let a `references` entry that
    # merely carried the same array value declare it, and a complete Run admitted exactly that.
    # This is declaration SUPPORT: it does not decide whether a requirement demands the deficiency.
    if "relations" in row and entry["relation"] not in row["relations"]:
        faults.append("native.coverage-cause-relation-not-in-scope:" + deficiency + ":"
                      + entry["relation"] + ":owned-by=" + ",".join(row["relations"]))
    rule = row["nativeCause"]
    if rule == "must-be-null":
        if cause is not None:
            faults.append("native.coverage-cause-must-be-null:" + deficiency + ":" + cause
                          + ":carrier=" + row["carrier"])
    else:
        if cause is None and rule == "required":
            faults.append("native.coverage-cause-required:" + deficiency)
        if cause is not None and cause not in row["allowedCauses"]:
            faults.append("native.coverage-cause-not-for-deficiency:" + deficiency + ":" + cause)
    def at(path: list[str]):
        node = entry
        for step in path:
            if not isinstance(node, dict) or step not in node:
                return None
            node = node[step]
        return node
    if "requires" in row and at(row["requires"]["path"]) != row["requires"]["equals"]:
        faults.append("native.coverage-cause-carrier-unsupported:" + deficiency + ":"
                      + row["carrier"] + ":declared=" + json.dumps(at(row["requires"]["path"])))
    if "oneOf" in row and at(row["oneOf"]["path"]) not in row["oneOf"]["members"]:
        faults.append("native.coverage-cause-carrier-unsupported:" + deficiency + ":"
                      + row["carrier"] + ":declared=" + json.dumps(at(row["oneOf"]["path"])))
    if "contains" in row and row["contains"]["member"] not in (at(row["contains"]["path"]) or []):
        faults.append("native.coverage-cause-carrier-unsupported:" + deficiency + ":"
                      + row["carrier"] + ":declared=" + json.dumps(at(row["contains"]["path"])))
    return faults


def clone_ownership_disclosure(ownership: dict | None, subjects: list[str], edition_map: dict) -> dict | None:
    """The typed Coverage disclosure a clones scope owes, derived from COMMITTED ownership and the
    SELECTED scope. Returns None when nothing is owed.

    Decision order is the selection law's own, and each step is a different claim:

    1. no committed ownership at all -> nothing in the universe has an admissible dialect;
    2. enumeration `partial` -> an owner inside the selected scope may exist that was never listed
       and could contradict a listed one. This is a gap in KNOWLEDGE and is checked before any row
       is read, so incomplete discovery can never act as an implicit edition selection;
    3. a subject OF THIS SCOPE whose SELECTED owners disagree on effective edition -> one body
       identity cannot represent two dialects.

    What is deliberately NOT disclosed here, because native-evidence section 11 states these are
    compatible with `coverage: complete`: a path compiled by no selected target (`not-compiled`) and
    a path compiled only by targets outside the selection (`not-selected`). Those are per-body
    refusals over subjects the host DID examine and correctly produced no fact for. A deliberate
    exclusion is a committed selection, visible in the universe identity; unfinished enumeration is
    not. Collapsing the two would either hide a real gap or slander a lawful selection.

    Pure: it reads the retained ownership record, the scope's own subjects and the universe edition
    map, and touches no Run state."""
    if ownership is None:
        return CLONE_OWNERSHIP_DISCLOSURE["ownership-missing"]
    if ownership.get("enumeration") != "complete":
        return CLONE_OWNERSHIP_DISCLOSURE["owner-unenumerated"]
    units = {u["unitId"]: u for u in ownership["units"]}
    selected = set(ownership["selectedUnitIds"])
    for path in subjects:
        owners = [r for r in ownership["ownership"] if r["path"] == path and r["unitId"] in selected]
        if not owners:
            continue                      # not-compiled / not-selected: a lawful per-body refusal
        effective = set()
        for row in owners:
            unit = units.get(row["unitId"])
            if unit is None:
                return CLONE_OWNERSHIP_DISCLOSURE["owner-ambiguous"]
            if unit.get("targetEdition") is not None:
                effective.add(unit["targetEdition"])
            elif unit.get("crateName") not in edition_map:
                return CLONE_OWNERSHIP_DISCLOSURE["owner-ambiguous"]
            else:
                effective.add(edition_map[unit["crateName"]])
        if len(effective) > 1:
            return CLONE_OWNERSHIP_DISCLOSURE["owner-ambiguous"]
    return None


def completeness_from_stage(relation: str, rung: str, examined: list[str], unresolved: list[dict],
                            stage_terminal: str | None, attempted: bool, examined_exhaustive: bool) -> dict:
    """RC-2 v2. `complete` needs: resolved rung, resolution attempted, examined partition exhaustive,
    stage terminal `complete`, and zero admitted unresolved-edge facts. A zero count with a skipped,
    unavailable, budget-exhausted, crashed or partial stage is never `complete`."""
    if rung not in RESOLVED_RUNGS:
        return {"state": "not-applicable", "attempted": False, "examinedExhaustive": examined_exhaustive,
                "stageTerminal": stage_terminal, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    if not attempted or stage_terminal is None:
        return {"state": "not-attempted", "attempted": False, "examinedExhaustive": examined_exhaustive,
                "stageTerminal": stage_terminal, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    ex = set(examined)
    rels = ("calls", "reachability") if relation == "reachability" else (relation,)  # RC-4 inheritance
    mine = [u for u in unresolved if u["relation"] in rels and u["referrer"] in ex]
    base = {"attempted": True, "examinedExhaustive": examined_exhaustive, "stageTerminal": stage_terminal,
            "unresolvedEdgeCount": len(mine), "unresolvedEdgeClasses": sorted({u["edgeKind"] for u in mine})}
    if stage_terminal != "complete" or not examined_exhaustive:
        return {"state": "partial", **base}
    return {"state": "complete" if not mine else "incomplete", **base}


def coverage_bijection(entries: list[dict], unresolved_facts: list[dict]) -> list[dict]:
    """Host recheck after admission. Returns faults (empty = consistent)."""
    faults: list[dict] = []
    for entry in entries:
        rel, rung, rc = entry["relation"], entry["resolution"], entry["resolutionCompleteness"]
        name = rel + "@" + rung
        if rc["state"] not in RC_STATES:
            faults.append({"entry": name, "fault": "RC-0: state outside closed enum"}); continue
        if rung not in RESOLVED_RUNGS:
            if rc["state"] != "not-applicable" or rc["unresolvedEdgeCount"] != 0:
                faults.append({"entry": name, "fault": "RC-1: not-applicable rung carries a completeness claim"})
            continue
        if rc["state"] == "not-applicable":
            faults.append({"entry": name, "fault": "RC-1: resolved rung must not claim not-applicable"}); continue
        examined = set(entry.get("examinedSubjects", []))
        rels = ("calls", "reachability") if rel == "reachability" else (rel,)
        observed = [f for f in unresolved_facts if f["relation"] in rels and f["referrer"] in examined]
        count, classes = len(observed), sorted({f["edgeKind"] for f in observed})
        if rc["state"] == "complete":
            if not rc.get("attempted") or not rc.get("examinedExhaustive") or rc.get("stageTerminal") != "complete":
                faults.append({"entry": name, "fault": "RC-2: complete requires attempted, exhaustive examination and a complete stage"})
            elif count != 0 or rc["unresolvedEdgeCount"] != 0:
                faults.append({"entry": name, "fault": f"RC-2: complete claimed but {count} unresolved-edge facts admitted"})
        elif rc["state"] == "not-attempted":
            if rc.get("attempted") or rc["unresolvedEdgeCount"] != 0:
                faults.append({"entry": name, "fault": "RC-2: not-attempted cannot carry counts or attempted=true"})
        elif rc["state"] in ("incomplete", "partial"):
            if rc["unresolvedEdgeCount"] != count or sorted(rc["unresolvedEdgeClasses"]) != classes:
                faults.append({"entry": name, "fault": f"RC-2: {rc['state']} claims {rc['unresolvedEdgeCount']} but {count} facts admitted"})
            if rc["state"] == "incomplete" and (count == 0 or rc.get("stageTerminal") != "complete" or not rc.get("examinedExhaustive")):
                faults.append({"entry": name, "fault": "RC-2: incomplete needs >=1 edge, complete stage and exhaustive examination; else partial"})
    return faults


# ---------------------------------------------------------------------------
# subjectScopeCommitment: the producing recipe for the retained C-2 coverage key field
# (blind consumer M-1). The commitment is NOT a new preimage and NOT a native H domain:
# it is the foundation subject-scope identity (scope2) re-spelled in the native Sha256Text
# text form, over the HOST's own exhaustive subject enumeration. The provider commits to a
# value it cannot choose, and the host recomputes it before admitting the payload.
# ---------------------------------------------------------------------------

SUBJECT_SCOPE_DOMAIN = "subject-scope"      # foundation identity domain; typed prefix scope2:


def subject_scope_descriptor(snapshot_id: str, relation: str, rung: str, source_universe: str,
                             target_universe: str, enumerator_closure: str, subjects: list[str]) -> dict:
    """Closed foundation subject-scope record over the complete examined partition.

    `subjects` is what the Plan-bound enumerator closure enumerated over the admitted snapshot; it is
    never a provider-chosen subset and carries no provider-supplied digest. Duplicate subjects refuse
    rather than silently dedupe, and the array is put in canonical-set order for the foundation encoder.
    """
    if type(subjects) is not list or any(type(s) is not str for s in subjects):
        raise AdmissionError("SUBJECT_SCOPE_SUBJECTS")
    ordered_subjects = sorted(subjects, key=C.canonical)
    if len(set(subjects)) != len(subjects):
        raise AdmissionError("SUBJECT_SCOPE_DUPLICATE_SUBJECT")
    descriptor = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": source_universe,
                  "targetUniverse": target_universe, "relation": relation, "resolution": rung,
                  "enumeratorClosure": enumerator_closure, "subjects": ordered_subjects}
    validate_foundation("subject-scope", descriptor)
    return descriptor


def subject_scope_identity(descriptor: dict) -> str:
    """`scope2:<64 hex>` = H('subject-scope', descriptor) under the foundation recipe (no native domain)."""
    return IM.identifier(SUBJECT_SCOPE_DOMAIN, descriptor)


def subject_scope_commitment(descriptor: dict) -> dict:
    """SubjectScopeCommitmentV1: the same 64 hex as the scope2 identity, in the native `sha256:` text form.

    Encoding note (blind consumer A-2): the foundation spelling of this identity is the TYPED PREFIX form
    `scope2:<hex>`; native records that require a `Sha256Text` carry `sha256:<hex>`. One preimage, one digest,
    two textual forms, and neither is a second recipe.
    """
    scope_id = subject_scope_identity(descriptor)
    out = {"scopeId": scope_id,
           "subjectScopeCommitment": "sha256:" + scope_id.removeprefix("scope2:"),
           "subjectCount": len(descriptor["subjects"])}
    validate_native("SubjectScopeCommitmentV1", out)
    return out


def admit_coverage_result_v3(payload: dict, scope_descriptor: dict, unresolved_facts: list[dict],
                             payload_schema_digest: str | None = None) -> dict:
    """The admitted native producer boundary for one CoverageResultV3.

    TRUSTED OBSERVATION INPUT: `payload` is what a provider sent. Everything the host compares it against is
    recomputed here from the host's own subject-scope descriptor, so a provider can neither invent the
    commitment nor pick the partition it is judged against. Refusals are `PROVIDER.PROTOCOL_VIOLATION`
    (operational-failed 4, section 10 fault law): a faulting or lying worker mints no coverage2 and no Run.
    """
    refusals: list[str] = []
    validate_native("CoverageResultV3", payload)
    commitment = subject_scope_commitment(scope_descriptor)
    key, entry = payload["key"], payload["entry"]
    for field, want in (("relation", scope_descriptor["relation"]), ("resolution", scope_descriptor["resolution"]),
                        ("sourceUniverse", scope_descriptor["sourceUniverse"]),
                        ("targetUniverse", scope_descriptor["targetUniverse"])):
        if key[field] != want:
            refusals.append("native.coverage-key-scope-mismatch:" + field)
    if key["subjectScopeCommitment"] != commitment["subjectScopeCommitment"]:
        refusals.append("native.subject-scope-commitment-mismatch")
    if entry["relation"] != key["relation"] or entry["resolution"] != key["resolution"]:
        refusals.append("native.coverage-entry-key-mismatch")
    examined = entry["examinedUniverse"]
    if examined["subjectScopeCommitment"] != commitment["subjectScopeCommitment"]:
        refusals.append("native.examined-universe-commitment-mismatch")
    if examined["subjectCount"] != commitment["subjectCount"]:
        refusals.append("native.examined-universe-subject-count-mismatch")
    faults = coverage_bijection([dict(entry, examinedSubjects=scope_descriptor["subjects"])], unresolved_facts)
    # The declared (deficiency, nativeCause) pair against the entry's own committed carriers. Schema
    # validity is not enough: an unrelated but schema-valid cause, a relabelled one, and a deficiency
    # whose carrier says the opposite all validated and closed a Run before this join existed.
    refusals.extend(deficiency_cause_faults(entry))
    # `payloadSchemaDigest` is the raw SHA-256 of the EXACT registered schema DOCUMENT bytes (section 7.2).
    # A caller may restate it, but never choose it: a value that is not the registered document's digest is
    # refused rather than carried into coverage2.
    registered_digest = schema_document_digest(NATIVE_SCHEMA_DOC)
    schema_digest = payload_schema_digest if payload_schema_digest is not None else registered_digest
    if schema_digest != registered_digest:
        refusals.append("native.coverage-payload-schema-not-registered")
    out = {"result": "REFUSE" if (refusals or faults) else "ADMIT", "scopeId": None, "coverageId": None,
           "subjectScopeCommitment": None, "subjectCount": None,
           "refusals": sorted(set(refusals)), "faults": faults}
    if out["result"] == "ADMIT":
        out.update(scopeId=commitment["scopeId"],
                   subjectScopeCommitment=commitment["subjectScopeCommitment"],
                   subjectCount=commitment["subjectCount"],
                   coverageId=IM.identifier("coverage", {
                       "schemaVersion": 2, "scopeId": commitment["scopeId"],
                       "payloadSchemaDigest": schema_digest,
                       "payloadDigest": raw_sha256(C.canonical(payload))}))
    validate_native("CoverageAdmissionV1", out)
    return out


def coverage_view_use(view: dict, admissions: list[dict]) -> dict:
    """Coverage use: every coverage2 a view names was admitted at the boundary above, and the scope2 the
    commitment resolves to is one of the view's own scopeIds. A hash-valid coverage2 whose subject scope is
    outside the evaluated view is refused exactly as a hidden fact is (identity-and-evidence section 3)."""
    validate_foundation("view", view)
    by_id = {a["coverageId"]: a for a in admissions if a["result"] == "ADMIT"}
    refusals = []
    for coverage_id in view["coverageIds"]:
        admitted = by_id.get(coverage_id)
        if admitted is None:
            refusals.append("native.coverage-not-admitted-at-producer-boundary:" + coverage_id)
        elif admitted["scopeId"] not in view["scopeIds"]:
            refusals.append("native.coverage-subject-scope-outside-view:" + coverage_id)
    return {"result": "REFUSE" if refusals else "ADMIT", "refusals": sorted(set(refusals)),
            "scopeIds": sorted(view["scopeIds"])}


def closed_world_v2(package_json: dict | None, entry_points: dict, unresolved: list[dict],
                    external_consumers: str, cargo_targets: dict | None = None) -> dict:
    """Feedback 7. `closed` requires every ingredient; private:true alone is `unknown`."""
    validate_native("EntryPointRecognitionV1", entry_points)
    nonliteral = sorted({u["edgeKind"] for u in unresolved if u["edgeKind"] in
                         ("dynamic-import-nonliteral", "require-nonliteral", "reflective-access", "indirect-eval")})
    dyn = sorted({u["edgeKind"] for u in unresolved if u["edgeKind"] in
                  ("trait-object-dynamic-dispatch", "generic-bound-dispatch", "structural-dispatch")})
    reasons: list[str] = []
    if package_json is not None:
        published = sorted(k for k in ("exports", "main", "module", "types", "bin", "browser", "files") if k in package_json)
        if published:
            exports = "open"; reasons.append("published-entry:" + ",".join(published))
        elif package_json.get("private") is True:
            exports = "closed-candidate"
        else:
            exports = "unknown"; reasons.append("package.json-without-private-true")
        if "workspaces" in package_json:
            exports = "open"; reasons.append("workspace-root-consumed-by-members")
    elif cargo_targets is not None:
        if cargo_targets.get("lib") or cargo_targets.get("procMacro"):
            exports = "open"; reasons.append("cargo-lib-target")
        elif cargo_targets.get("bin"):
            exports = "closed-candidate"
        else:
            exports = "unknown"; reasons.append("cargo-targets-unknown")
    else:
        exports = "unknown"; reasons.append("no-manifest")
    if exports == "closed-candidate":
        if entry_points["state"] != "all":
            reasons.append("entry-points:" + entry_points["state"])
        if nonliteral:
            reasons.append("nonliteral-loading:" + ",".join(nonliteral))
        if external_consumers != "none-declared":
            reasons.append("external-consumers:" + external_consumers)
        exports = "closed" if not reasons else "unknown"
    return {"exportsClosed": exports, "entryPointsRecognized": entry_points["state"],
            "nonliteralLoading": "present" if nonliteral else "none",
            "externalConsumers": external_consumers, "dynamicDispatch": "present" if dyn else ("not-applicable" if not unresolved else "resolved"),
            "reasons": sorted(reasons), "deadCodeRepairEligible": exports == "closed" and entry_points["state"] == "all" and not nonliteral}


def affected_targets(unresolved: list[dict], exports_by_module: dict[str, list[str]], universe_subjects: list[str]) -> dict:
    """Dynamic edges propagate to every target subject they could reach. A universal negative about
    any subject in the returned set is `resolution-incomplete`."""
    affected: dict[str, list[str]] = {}
    all_exports = sorted({s for subs in exports_by_module.values() for s in subs})
    for u in unresolved:
        scope, kind = u["targetScope"], u["edgeKind"]
        if scope == "module":
            targets = exports_by_module.get(u.get("targetModule", ""), [])
        elif scope == "universe":
            targets = universe_subjects
        else:  # external / unknown: anything exported may be reached
            targets = all_exports
        for t in targets:
            affected.setdefault(t, []).append(kind)
    return {t: sorted(set(k)) for t, k in sorted(affected.items())}


def sufficiency_v2(req: dict, view: dict, target_exported: bool = False, target_affected: bool = False, depth: int = 0) -> dict:
    """Contract §4.6. Returns {satisfied, deficiency?, disclosures, causes}. Steps 1-8 run in the stated order for
    EVERY requirement; there is no early `satisfied` return for a one-rung relation under existential/partial-ok (the
    former shortcut ran before the confidence floor and let confidence 100000 pass floor 900000; removed by Codex,
    regression case `sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut`)."""
    rel = req["relation"]; quantifier = req.get("quantifier", "existential")
    disclosures: list[dict] = []; causes: list[str] = []
    entry = view.get(rel)
    if entry is None:
        return {"satisfied": False, "deficiency": "required-relation-missing", "disclosures": [], "causes": ["required-relation-missing"]}
    have_i, need_i = _rung_index(rel, entry["resolution"]), _rung_index(rel, req["minResolution"])
    if have_i is None or need_i is None:
        return {"satisfied": False, "deficiency": "required-relation-missing", "disclosures": [], "causes": ["required-relation-missing"]}
    if have_i < need_i:
        causes.append(RUNG_CAUSE.get(entry.get("rungUnavailableBecause", ""), "required-relation-missing"))
    if entry.get("confidenceMillionths", 1000000) < req.get("minConfidenceMillionths", 0):   # step 3, never skipped
        causes.append("confidence-floor-unmet")
    if rel == "types" and req.get("derivationPolicy", "any") == "declared-only":
        kinds = set(entry.get("derivationKinds", []))
        if "compiler-inferred" in kinds:
            causes.append("derivation-policy-unmet")
    if req["completeness"] == "complete" and entry.get("coverage") != "complete":
        causes.append(entry.get("deficiency") or RUNG_CAUSE.get(entry.get("rungUnavailableBecause", ""), "required-relation-missing"))
    rc = entry.get("resolutionCompleteness", {"state": "not-applicable", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []})
    if quantifier == "universal-negative":
        if rc["state"] in ("partial", "not-attempted"):
            causes.append("resolution-incomplete")
        elif rc["state"] == "incomplete" or target_affected:
            if req.get("unresolvedEdgePolicy", "forbid") == "forbid":
                causes.append("resolution-incomplete")
            else:
                disclosures.append({"kind": "unresolved-edges", "count": rc.get("unresolvedEdgeCount", 0), "classes": list(rc.get("unresolvedEdgeClasses", []))})
        cw = entry.get("closedWorld", {"exportsClosed": "unknown"})
        if target_exported and cw.get("exportsClosed") != "closed":
            if req.get("externalConsumerPolicy", "forbid") == "forbid":
                causes.append("external-consumers-unknown")
            else:
                disclosures.append({"kind": "external-consumers-assumed-closed", "exportsClosed": cw.get("exportsClosed")})
    if depth < 4:
        for dep in DEPENDS_ON.get(rel, []):
            sub_req = {**dep, "completeness": "partial-ok" if quantifier == "existential" else "complete", "quantifier": quantifier,
                       "unresolvedEdgePolicy": req.get("unresolvedEdgePolicy", "forbid"), "externalConsumerPolicy": req.get("externalConsumerPolicy", "forbid")}
            sub = sufficiency_v2(sub_req, view, target_exported, target_affected, depth + 1)
            causes.extend(sub["causes"]); disclosures.extend(sub["disclosures"])
    if not causes:
        return {"satisfied": True, "disclosures": disclosures, "causes": []}
    return {"satisfied": False, "deficiency": min(causes, key=PRECEDENCE_V2.index), "disclosures": disclosures, "causes": causes}


def types_fact_derivation(subject_language: str, has_annotation: bool, has_jsdoc: bool, check_js: bool) -> dict:
    """Feedback 12: declared derivation provenance instead of an invented probability. Every checked
    type fact is exact under the admitted universe; confidenceMillionths is 1000000 with method
    native.confidence.v1 (declared-exact). Rule authors filter on derivation, not on a fake percentage."""
    if has_annotation and subject_language == "typescript":
        kind = "annotated"
    elif has_jsdoc:
        kind = "jsdoc-declared"
    else:
        kind = "compiler-inferred"
    return {"derivationKind": kind, "confidenceMillionths": 1000000, "confidenceMethod": "native.confidence.v1",
            "checkJs": check_js, "limitations": ["L-JS3"] if kind == "compiler-inferred" and subject_language == "javascript" else []}


# ---------------------------------------------------------------------------
# Dependency sources (feedback 3) — Cargo.lock parse and DS rules with provenance
# ---------------------------------------------------------------------------

_LOCK_KV = re.compile(r'^([a-z_]+)\s*=\s*"([^"]*)"\s*$')


def parse_cargo_lock(text: str) -> dict:
    packages: list[dict] = []; current: dict | None = None; version = None
    for raw in text.splitlines():
        line = raw.strip()
        if line == "[[package]]":
            current = {"name": None, "version": None, "source": "", "checksum": None}; packages.append(current); continue
        m = _LOCK_KV.match(line)
        if not m:
            if line.startswith("version = ") and current is None:
                version = int(line.split("=", 1)[1].strip())
            continue
        k, v = m.groups()
        if current is None:
            if k == "version":
                version = int(v)
            continue
        if k in current:
            current[k] = v
    if version not in (3, 4):
        raise AdmissionError("LOCKFILE_VERSION")
    for p in packages:
        if p["name"] is None or p["version"] is None:
            raise AdmissionError("LOCK_PACKAGE_INCOMPLETE")
    return {"version": version, "packages": packages}


def _source_kind(source: str) -> str:
    if source == "":
        return "path"
    if source.startswith("registry+"):
        return "registry"
    if source.startswith("git+"):
        return "git"
    raise AdmissionError("UNKNOWN_SOURCE_KIND")


def file_manifest_identity(files: dict[str, dict]) -> str:
    rows = sorted(({"path": p, "contentSha256": f["sha256"], "byteLength": f["byteLength"]} for p, f in files.items()),
                  key=lambda r: r["path"].encode("utf-8"))
    return native_identity("native.dependency-file-manifest.v1", "DependencyFileManifestV1", rows)[len("sha256:"):]


ACQUISITION_MODES = {"in-snapshot-path", "in-snapshot-vendored", "imported-descriptor"}


def dependency_source_set_admit(lock_text: str, provided: list[dict], activated: list[str]) -> dict:
    """DS-1..DS-6 with the feedback-3 correction. provided rows (TRUSTED OBSERVATION INPUT):
    {name, version, sourceId, acquisition{mode,...}, files{path:{sha256,byteLength}},
     cargoChecksumJson{package,files}|None, crateTarballSha256|None}."""
    lock = parse_cargo_lock(lock_text)
    by_key = {f'{p["name"]} {p["version"]} {p["source"]}': p for p in lock["packages"]}
    refusals: list[dict] = []; packages: list[dict] = []; missing: list[dict] = []; provided_by_key: dict = {}
    for row in provided:
        key = f'{row["name"]} {row["version"]} {row["sourceId"]}'
        if key in provided_by_key:
            refusals.append({"rule": "DS-0", "key": key, "reason": "duplicate provided package"})
        provided_by_key[key] = row
    for key in sorted(activated):
        lock_pkg = by_key.get(key)
        if lock_pkg is None:
            refusals.append({"rule": "DS-6", "key": key, "reason": "activated package absent from Cargo.lock; no implicit lock update"}); continue
        kind = _source_kind(lock_pkg["source"])
        if kind == "path":
            continue
        row = provided_by_key.get(key)
        if row is None:
            missing.append({"name": lock_pkg["name"], "version": lock_pkg["version"], "sourceId": lock_pkg["source"]}); continue
        mode = row["acquisition"].get("mode")
        if mode not in ACQUISITION_MODES or "fetch" in row or "fetchUrl" in row.get("acquisition", {}):
            refusals.append({"rule": "DS-5", "key": key, "reason": f"ambient or fetching acquisition refused: {mode}"}); continue
        verification, provenance = "not-applicable", "declared"
        if kind == "registry":
            if lock_pkg["checksum"] is None:
                refusals.append({"rule": "DS-1", "key": key, "reason": "registry package without lock checksum"}); continue
            ccj, tarball = row.get("cargoChecksumJson"), row.get("crateTarballSha256")
            if tarball is not None:
                # DS-2: only the locked tarball digest authenticates against the registry.
                if tarball != lock_pkg["checksum"]:
                    verification = "mismatch"
                else:
                    verification, provenance = "tarball-matched", "registry-authenticated"
            elif ccj is not None:
                # DS-1: a self-consistent vendored tree is DECLARED provenance; `package` is self-asserted.
                if ccj.get("package") != lock_pkg["checksum"]:
                    verification = "mismatch"
                else:
                    files_ok = set(ccj.get("files", {}).keys()) == set(row["files"].keys()) and all(
                        ccj["files"][p] == row["files"][p]["sha256"] for p in row["files"])
                    verification = "self-consistent" if files_ok else "mismatch"
                    provenance = "declared"
            else:
                refusals.append({"rule": "DS-2", "key": key, "reason": "imported registry package needs a .crate digest or .cargo-checksum.json"}); continue
            if verification == "mismatch":
                refusals.append({"rule": "DS-1/DS-2", "key": key, "reason": "checksum mismatch refuses the whole set"})
        packages.append({
            "name": lock_pkg["name"], "version": lock_pkg["version"],
            "sourceKind": "vendored" if mode == "in-snapshot-vendored" else kind,
            "sourceId": lock_pkg["source"], "lockChecksum": lock_pkg["checksum"],
            "fileManifestSha256": file_manifest_identity(row["files"]),
            "fileCount": len(row["files"]), "totalBytes": sum(f["byteLength"] for f in row["files"].values()),
            "acquisition": {"mode": mode, "descriptorId": row["acquisition"].get("descriptorId"), "vendorPath": row["acquisition"].get("vendorPath")},
            "checksumVerification": verification, "provenanceAssurance": provenance,
        })
    packages.sort(key=lambda p: (p["name"].encode(), p["version"].encode(), p["sourceId"].encode()))
    descriptor = {"schemaVersion": 1, "language": "rust",
                  "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": raw_sha256(lock_text.encode("utf-8")), "lockfileVersion": lock["version"]},
                  "packages": packages, "completeness": {"state": "complete" if not missing else "incomplete", "missing": missing}}
    admitted = not any(r["rule"] in ("DS-0", "DS-1", "DS-2", "DS-1/DS-2", "DS-5") for r in refusals)
    return {"admitted": admitted, "refusals": refusals, "completeness": descriptor["completeness"], "descriptor": descriptor,
            "provenanceSummary": sorted({p["provenanceAssurance"] for p in packages}),
            "identity": dependency_source_set_identity(descriptor) if admitted else None}


def mutate_vendored_tree(row: dict, path: str, new_sha256: str) -> dict:
    """Adversary: rewrite one file and its .cargo-checksum.json entry while preserving `package`."""
    out = copy.deepcopy(row)
    out["files"][path]["sha256"] = new_sha256
    out["cargoChecksumJson"]["files"][path] = new_sha256
    return out


def missing_crate_coverage(crates: dict[str, list[str]], missing: list[str]) -> dict:
    affected: set[str] = set(); deps_of = {c: set(d) for c, d in crates.items()}; missing_set = set(missing); changed = True
    while changed:
        changed = False
        for crate, deps in deps_of.items():
            if crate not in affected and (deps & missing_set or deps & affected):
                affected.add(crate); changed = True
    out = {}
    for crate in crates:
        if crate in affected:
            out[crate] = {"syntax": "complete", "semanticRungs": "unknown/input-closure-incomplete/missing-dependency-source",
                          "remedy": "vendor or import the sealed source for " + ", ".join(sorted(missing_set))}
        else:
            out[crate] = {"syntax": "complete", "semanticRungs": "complete", "remedy": None}
    return out


# ---------------------------------------------------------------------------
# Cargo configuration and rustflags (feedback 5, 10)
# ---------------------------------------------------------------------------

STRIPPED_CONFIG_KEYS = ["alias", "build.rustc", "build.rustc-wrapper", "build.rustc-workspace-wrapper", "build.rustdoc",
                        "build.target-dir", "build.incremental", "build.dep-info-basedir", "build.build-dir", "cargo-new", "credential-alias",
                        "doc.browser", "env", "future-incompat-report", "http", "install", "net", "patch", "profile",
                        "registries", "registry", "target.*.linker", "target.*.runner", "target.*.<links>", "term", "unstable"]
HONORED_CONFIG_KEYS = ["build.rustflags", "build.target", "resolver", "source.<name>.directory (inside snapshot)",
                       "source.<name>.replace-with", "target.<triple>.rustflags"]
_CFG_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*(="[^"\\]*")?$')
_LINT_RE = re.compile(r'^[a-z0-9_:]+$')
_ALLOWED_C = {"target-feature", "target-cpu", "opt-level", "debuginfo", "panic", "overflow-checks", "debug-assertions", "strip"}
_ALLOWED_C_VALUES = re.compile(r'^[A-Za-z0-9_+,\-.=]+$')


def rustflags_projection(flags: list[str], snapshot_paths: set[str], closure_paths: set[str]) -> dict:
    """Exact allowlist. Anything selecting a tool, a path, a link argument, a sysroot, a response
    file or a codegen backend is stripped and disclosed. --remap-path-prefix is honored only when
    its FROM component is a verified in-snapshot or in-closure path."""
    honored: list[str] = []; stripped: list[dict] = []
    i = 0
    while i < len(flags):
        f = flags[i]; nxt = flags[i + 1] if i + 1 < len(flags) else None
        def take2(reason_ok: bool, why: str) -> None:
            nonlocal i
            if nxt is None:
                stripped.append({"flag": f, "reason": "dangling"}); i += 1; return
            if reason_ok:
                honored.extend([f, nxt])
            else:
                stripped.append({"flag": f + " " + nxt, "reason": why})
            i += 2
        if f.startswith("@"):
            stripped.append({"flag": f, "reason": "response-file"}); i += 1
        elif f == "--cfg":
            take2(nxt is not None and bool(_CFG_RE.match(nxt)), "cfg-syntax")
        elif f.startswith("--cfg="):
            v = f[len("--cfg="):]
            (honored.append(f) if _CFG_RE.match(v) else stripped.append({"flag": f, "reason": "cfg-syntax"})); i += 1
        elif f in ("-A", "-W", "-D", "-F", "--allow", "--warn", "--deny", "--forbid"):
            take2(nxt is not None and bool(_LINT_RE.match(nxt)), "lint-syntax")
        elif f.startswith("--cap-lints=") or f.startswith(("-A", "-W", "-D", "-F")) and len(f) > 2 and _LINT_RE.match(f[2:]):
            honored.append(f); i += 1
        elif f == "--cap-lints":
            take2(nxt in ("allow", "warn", "deny", "forbid"), "cap-lints-value")
        elif f in ("-C", "--codegen"):
            ok = nxt is not None and "=" in nxt and nxt.split("=", 1)[0] in _ALLOWED_C and bool(_ALLOWED_C_VALUES.match(nxt.split("=", 1)[1]))
            take2(ok, "codegen-option-not-allowlisted")
        elif f.startswith("-C"):
            body = f[2:]
            ok = "=" in body and body.split("=", 1)[0] in _ALLOWED_C and bool(_ALLOWED_C_VALUES.match(body.split("=", 1)[1]))
            (honored.append(f) if ok else stripped.append({"flag": f, "reason": "codegen-option-not-allowlisted"})); i += 1
        elif f == "--remap-path-prefix" or f.startswith("--remap-path-prefix="):
            val = nxt if f == "--remap-path-prefix" else f[len("--remap-path-prefix="):]
            src = val.split("=", 1)[0] if val and "=" in val else None
            ok = src is not None and (src in snapshot_paths or src in closure_paths)
            if f == "--remap-path-prefix":
                take2(ok, "remap-from-outside-snapshot-or-closure")
            else:
                (honored.append(f) if ok else stripped.append({"flag": f, "reason": "remap-from-outside-snapshot-or-closure"})); i += 1
        else:
            stripped.append({"flag": f, "reason": "not-allowlisted"}); i += 1
    return {"honored": honored, "stripped": stripped, "executableSelected": False}


def cargo_config_admission(ancestor_configs: list[str], snapshot_configs: list[str], env: dict[str, str],
                           tool_closure: dict[str, str], selected_tools: dict[str, str]) -> dict:
    """Feedback 10. Cargo discovers config in every ancestor of CWD and in CARGO_HOME. The first-party
    adapter does not claim a Cargo switch disables that; it verifies the carrier:
      * every ancestor directory of the private scratch root is free of .cargo/config.toml and .cargo/config
        (refusal, not fallback, if any exists);
      * CARGO_HOME is a fresh private empty directory (its config.toml is absent);
      * every .cargo/config(.toml) inside the snapshot is replaced by the projected file (data only);
      * all CARGO_*, RUSTFLAGS, RUSTC*, RUSTDOC*, CARGO_TARGET_*, PATH, CC/LD/AR variables are absent;
      * every selected tool (rustc, cargo, linker, ar, proc-macro server) is in the sealed tool closure."""
    refusals: list[dict] = []
    for p in ancestor_configs:
        refusals.append({"rule": "CC-1", "detail": f"ambient Cargo config present at {p}"})
    bad_env = sorted(k for k in env if k == "PATH" or k.startswith(("CARGO", "RUSTFLAGS", "RUSTC", "RUSTDOC", "RUSTUP", "CC", "CXX", "LD", "AR", "TARGET_")))
    bad_env = [k for k in bad_env if not (k == "CARGO_HOME" and env[k] == "<private-empty>")]
    for k in bad_env:
        refusals.append({"rule": "CC-3", "detail": f"environment override {k} must be absent"})
    if env.get("CARGO_HOME") != "<private-empty>":
        refusals.append({"rule": "CC-2", "detail": "CARGO_HOME must be a fresh private empty directory"})
    for tool, digest in selected_tools.items():
        if tool_closure.get(tool) != digest:
            refusals.append({"rule": "CC-4", "detail": f"selected tool {tool} is not in the sealed tool closure"})
    return {"admitted": not refusals, "refusals": refusals, "replacedSnapshotConfigs": sorted(snapshot_configs),
            "strategy": "verified-ancestor-carrier+private-cargo-home+projected-config",
            "claimsCargoSwitch": False, "d9": None if not refusals else
            {"class": "operational-failed", "exitCode": 4, "code": "HOST.IO_FAILURE", "detail": "native.ambient-cargo-config"}}


# ---------------------------------------------------------------------------
# Prepared outputs (feedback 4): inert expansions only; no dylib admitted from an import
# ---------------------------------------------------------------------------

INERT_ROW_KINDS = {"build-script-directives", "macro-expansion", "generated-file"}
EXECUTABLE_ROW_KINDS = {"proc-macro-dylib", "build-script-binary"}
ROW_MEDIA = {"build-script-directives": {"text/x-cargo-directives"}, "macro-expansion": {"text/x-rust-expansion"},
             "generated-file": {"text/x-rust-source", "text/plain", "application/octet-stream"}}
GENERATED_BOUNDS = {"maxGeneratedFilesPerOwner": 4096, "maxGeneratedFileBytes": 67108864, "maxGeneratedTotalBytes": 1073741824, "maxLogicalPathBytes": 1024}
VIRTUAL_OUT_DIR = ".opensip/out/v1/"
_LOGICAL_RE = re.compile(r"^(?!/)(?!.*(^|/)\.\.?(/|$))[^\x00\\]+$")


def generated_file_row_check(row: dict, per_owner_count: dict[str, int], total_bytes: list[int]) -> str | None:
    """Strict bounds for generated-file rows (review v2 item 2). Returns a refusal reason or None."""
    g = row.get("generated")
    if g is None:
        return "generated-file row without generated binding"
    lp = g["logicalPath"]
    if not _LOGICAL_RE.match(lp) or len(lp.encode("utf-8")) > GENERATED_BOUNDS["maxLogicalPathBytes"] or lp.startswith(VIRTUAL_OUT_DIR):
        return "generated logicalPath escapes or exceeds the virtual OUT_DIR bounds: " + lp
    if g["blob"]["byteLength"] > GENERATED_BOUNDS["maxGeneratedFileBytes"]:
        return "generated file exceeds maxGeneratedFileBytes"
    per_owner_count[row["ownerKey"]] = per_owner_count.get(row["ownerKey"], 0) + 1
    if per_owner_count[row["ownerKey"]] > GENERATED_BOUNDS["maxGeneratedFilesPerOwner"]:
        return "owner exceeds maxGeneratedFilesPerOwner"
    total_bytes[0] += g["blob"]["byteLength"]
    if total_bytes[0] > GENERATED_BOUNDS["maxGeneratedTotalBytes"]:
        return "set exceeds maxGeneratedTotalBytes"
    return None


def prepared_output_set_admit(prepared: dict, context: dict, explicit_prepared_mode: bool) -> dict:
    """PO-0 inert-only (by KIND and consumption channel; a media type is a label, never a trust proof),
    PO-1 staleness, PO-2 failed rows, PO-3 declared provenance, PO-4 generated-file bounds. context:
    {ownerManifests:{ownerKey:sha}, dependencySourceSetId, toolchainDigest, cfgSetId}."""
    validate_native("PreparedOutputSetV3", prepared)
    stale: list[dict] = []; usable: list[str] = []; failed: list[str] = []; refused: list[dict] = []
    per_owner: dict[str, int] = {}; total = [0]; generated_rows = 0
    for row in prepared["rows"]:
        if row["kind"] in EXECUTABLE_ROW_KINDS or row["kind"] not in INERT_ROW_KINDS:
            # kind decides: a dylib labelled text/x-rust-expansion is still a dylib row.
            refused.append({"ownerKey": row["ownerKey"], "reason": "executable product row kind refused regardless of media type: " + row["kind"]}); continue
        if row["blob"]["mediaType"] not in ROW_MEDIA[row["kind"]]:
            refused.append({"ownerKey": row["ownerKey"], "reason": f"media type {row['blob']['mediaType']} not admissible for row kind {row['kind']}"}); continue
        if row["kind"] == "generated-file":
            why = generated_file_row_check(row, per_owner, total)
            if why is not None:
                refused.append({"ownerKey": row["ownerKey"], "reason": why}); continue
            generated_rows += 1
        elif row.get("generated") is not None:
            refused.append({"ownerKey": row["ownerKey"], "reason": "generated binding on a non generated-file row"}); continue
        b = row["inputBinding"]; differing = []
        if b["ownerFileManifestSha256"] != context["ownerManifests"].get(row["ownerKey"]):
            differing.append("ownerFileManifestSha256")
        for k in ("dependencySourceSetId", "toolchainDigest", "cfgSetId"):
            if b[k] != context[k]:
                differing.append(k)
        if differing:
            stale.append({"ownerKey": row["ownerKey"], "differing": differing})
        elif row["status"] == "failed":
            failed.append(row["ownerKey"])
        else:
            usable.append(row["ownerKey"])
    if refused:
        return {"outcome": "rejected", "refused": refused, "staleRows": stale, "usableRows": [], "failedRows": failed,
                "d9": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "detail": "native.prepared-output-not-inert"}}
    if stale and explicit_prepared_mode:
        return {"outcome": "rejected", "refused": [], "staleRows": stale, "usableRows": [], "failedRows": failed,
                "d9": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "detail": "native.stale-prepared-output"}}
    if stale:
        return {"outcome": "fallback-non-prepared", "refused": [], "staleRows": stale, "usableRows": usable, "failedRows": failed,
                "disclosure": "stale prepared rows ignored; affected owners analyzed non-prepared", "d9": None}
    imported = prepared["preparation"]["kind"] == "imported-descriptor"
    return {"outcome": "admitted", "refused": [], "staleRows": [], "usableRows": usable, "failedRows": failed,
            "generatedFileRows": generated_rows, "workerExecutesRepositoryCode": False,
            "preparedResolution": "imported-inert" if imported else "host-prepared",
            "executionCapableResolution": True, "hostExecutionGrantImplied": False,
            "semanticGrantOperations": ["read-import"] if imported else ["prepare-code"],
            "provenanceAssurance": "declared" if imported else "host-prepared", "d9": None}


def generated_include_lookup(rows: list[dict], owner_key: str, include_kind: str, out_dir_relative_path: str,
                             context: dict) -> dict:
    """Worker-side consumption of build-script generated files (review v2 item 2). `env!("OUT_DIR")` resolves to
    the READ-ONLY virtual OUT_DIR `.opensip/out/v1/<ownerKey>/`; include!/include_str!/include_bytes! read the
    generated-file row bound to (ownerKey, logicalPath) whose inputBinding equals the current context. The bytes
    are consumed as source text or literal data only; nothing is loaded, linked or executed. A miss is a typed
    unknown (build-script-generated-unavailable edge, cause generated-file-missing), never a hard failure."""
    if include_kind not in ("include", "include_str", "include_bytes"):
        raise AdmissionError("unknown include macro")
    if not _LOGICAL_RE.match(out_dir_relative_path):
        return {"matched": False, "executed": False, "refused": "path escapes virtual OUT_DIR",
                "unresolvedEdge": {"relation": "references", "edgeKind": "build-script-generated-unavailable", "targetScope": "universe", "detail": out_dir_relative_path},
                "nativeCause": "generated-file-out-of-bounds"}
    for r in rows:
        if r["kind"] != "generated-file" or r["ownerKey"] != owner_key or r["status"] != "ok":
            continue
        b = r["inputBinding"]
        if b["ownerFileManifestSha256"] != context["ownerManifests"].get(owner_key) or any(b[k] != context[k] for k in ("dependencySourceSetId", "toolchainDigest", "cfgSetId")):
            continue
        if r["generated"]["logicalPath"] == out_dir_relative_path:
            return {"matched": True, "executed": False, "virtualPath": VIRTUAL_OUT_DIR + owner_key + "/" + out_dir_relative_path,
                    "blobSha256": r["generated"]["blob"]["sha256"], "consumedAs": {"include": "rust-source-text", "include_str": "string-literal", "include_bytes": "byte-literal"}[include_kind],
                    "readOnly": True}
    return {"matched": False, "executed": False,
            "unresolvedEdge": {"relation": "references", "edgeKind": "build-script-generated-unavailable", "targetScope": "universe", "detail": out_dir_relative_path},
            "nativeCause": "generated-file-missing"}


def preparation_capture(owner_key: str, out_dir_listing: list[dict], directive_lines: list[str], referenced_paths: list[str] | None,
                        binding: dict) -> dict:
    """Authorized preparation step, step 4 (review v2 item 2): after the owner's build script has run, capture the
    generated DATA the analysis needs and discard executable products. out_dir_listing (TRUSTED OBSERVATION INPUT):
    [{path, sha256, byteLength, mediaType, executableProduct: bool}]. referenced_paths = the OUT_DIR-relative paths
    named by include!/include_str!/include_bytes!(concat!(env!("OUT_DIR"), ...)) sites when statically determinable,
    else None (capture every regular data file within bounds)."""
    rows: list[dict] = []; discarded: list[str] = []; refused: list[dict] = []
    per_owner: dict[str, int] = {}; total = [0]
    rows.append({"kind": "build-script-directives", "ownerKey": owner_key, "configuration": [], "site": None, "generated": None,
                 "inputBinding": binding, "blob": {"sha256": raw_sha256("\n".join(directive_lines).encode("utf-8")), "byteLength": len("\n".join(directive_lines).encode("utf-8")), "mediaType": "text/x-cargo-directives"},
                 "status": "ok", "failureDetail": None})
    for f in sorted(out_dir_listing, key=lambda x: x["path"].encode("utf-8")):
        if f["executableProduct"]:
            discarded.append(f["path"]); continue
        if referenced_paths is not None and f["path"] not in referenced_paths:
            discarded.append(f["path"]); continue
        row = {"kind": "generated-file", "ownerKey": owner_key, "configuration": [], "site": None,
               "generated": {"logicalPath": f["path"], "blob": {"sha256": f["sha256"], "byteLength": f["byteLength"], "mediaType": f["mediaType"]}},
               "inputBinding": binding, "blob": {"sha256": f["sha256"], "byteLength": f["byteLength"], "mediaType": f["mediaType"]},
               "status": "ok", "failureDetail": None}
        why = generated_file_row_check(row, per_owner, total)
        if why is not None:
            refused.append({"path": f["path"], "reason": why}); continue
        rows.append(row)
    missing_refs = sorted(set(referenced_paths or []) - {r["generated"]["logicalPath"] for r in rows if r["kind"] == "generated-file"})
    return {"rows": rows, "discardedExecutableProducts": sorted(discarded), "refused": refused, "missingReferencedPaths": missing_refs,
            "dylibRetained": False, "outDirRetained": False}


def expansion_lookup(rows: list[dict], site: dict) -> dict:
    """Worker-side: an invocation site matches an expansion row only by exact (path, span, input token
    digest, macro crate manifest). Otherwise the site is a macro-expansion-unavailable unresolved edge."""
    for r in rows:
        if r["kind"] != "macro-expansion":
            continue
        s = r["site"]
        if (s["path"], s["startByte"], s["endByte"], s["inputTokenDigest"], r["inputBinding"]["ownerFileManifestSha256"]) == \
           (site["path"], site["startByte"], site["endByte"], site["inputTokenDigest"], site["macroCrateManifestSha256"]):
            return {"matched": True, "expansionBlob": r["blob"]["sha256"], "executed": False}
    return {"matched": False, "unresolvedEdge": {"relation": "references", "edgeKind": "macro-expansion-unavailable",
                                                 "targetScope": "universe", "detail": site["path"]}, "executed": False}


PLATFORM_ENFORCEMENT_V7 = {"subprocess": "DISCLOSURE-ONLY", "network": "DISCLOSURE-ONLY",
                           "filesystemWrite": "DISCLOSURE-ONLY", "environment": "ENFORCED-BY-CONSTRUCTION"}


def authorized_execution_admit(auth: dict, policy_records: set[str], linker_in_closure: bool,
                               truth_table: dict = PLATFORM_ENFORCEMENT_V7) -> dict:
    """AuthorizedExecutionV2 preflight over trusted observations. This function executes nothing and does not admit security grants; the host composition must admit every owner grant before any spawn."""
    validate_native("AuthorizedExecutionV2", auth)
    refusals: list[str] = []
    for effect, rec in auth["effects"].items():
        if rec["enforcement"] != truth_table[effect]:
            refusals.append(f"effect {effect} claims {rec['enforcement']} but the pinned truth table says {truth_table[effect]}")
    if auth["authorization"]["ci"]:
        if auth["authorization"]["mode"] != "policy-record" or auth["authorization"]["policyRecordId"] not in policy_records:
            refusals.append("CI requires a pre-existing policy record for this dependency set and toolchain")
    if not linker_in_closure:
        refusals.append("no bundled linker in the sealed tool closure on this platform: prepare unsupported, no system cc fallback")
    lb = auth["liveBoundaries"]
    if lb["revocationCheck"] != "before-each-owner" or lb["cancellation"] != "process-group-kill" or not lb["trustClockRequired"]:
        refusals.append("live revocation/cancellation boundaries missing")
    disclosure = (f"Build scripts and procedural macros from {len(auth['owners'])} packages will run with your user's authority. "
                  "OpenSIP does not prevent network access or other effects on this platform.")
    declared = sorted(o["ownerKey"] for o in auth["owners"] if o["provenanceAssurance"] == "declared")
    if declared:
        disclosure += " Packages with declared (unauthenticated) provenance: " + ", ".join(declared) + "."
    if refusals:
        return {"admitted": False, "refusals": refusals, "disclosure": disclosure,
                "d9": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "detail": "native.execution-not-authorized"}}
    # Principal join (review v2 item 4): security principal class `repository-code` == foundation semantic-grant
    # principal kind `trusted-repository-code` == workflow spelling `P-TRUSTED-REPO`. The semantic projection
    # (Plan-bound) carries kind/closure/owner-source and operation `prepare-code`; the authority grant is the
    # operational authorizationRef and never enters Plan.
    projection = [{"kind": "trusted-repository-code", "closureId": auth["toolClosure"]["closureId"], "ownerSourceDigest": raw_sha256(C.canonical([{k: o[k] for k in ("ownerKey", "source", "ownerFileManifestSha256")}]))}
                  for o in sorted(auth["owners"], key=lambda o: o["ownerKey"].encode("utf-8"))]
    for p in projection:
        validate_native("SemanticGrantPrincipalProjectionV1", p)
    plan_descriptor = {k: v for k, v in auth.items() if k != "authorizationRef"}
    return {"admitted": True, "refusals": [], "disclosure": disclosure, "principalClass": "repository-code",
            "semanticGrantPrincipalKind": auth["semanticGrantPrincipalKind"], "workflowPrincipalSpelling": auth["workflowPrincipalSpelling"],
            "semanticGrantProjection": {"principals": projection, "analysisOperations": ["prepare-code"]},
            "authorizationRefInPlan": "authorizationRef" in plan_descriptor,
            "identity": native_identity("native.authorized-execution.v2", "AuthorizedExecutionV2", auth), "d9": None}


# ---------------------------------------------------------------------------
# TypeScript / JavaScript modes and edge classification (feedback 11)
# ---------------------------------------------------------------------------

JS_EXT = (".js", ".mjs", ".cjs", ".jsx")
TS_EXT = (".ts", ".tsx", ".mts", ".cts")
def _under_unit(path: str, root: str) -> bool:
    return root == "" or path == root or path.startswith(root.rstrip("/") + "/")


def _rel(path: str, root: str) -> str:
    return path if root == "" else path[len(root.rstrip("/")) + 1:]


def typescript_mode(listing: list[str], unit_root: str, package_json: dict | None, tsconfig: dict | None,
                    jsconfig: dict | None, lockfiles: list[str], node_modules_in_read_set: bool) -> dict:
    # program roots exclude pruned trees by the shared segment rule (node_modules / VCS trees anywhere under the unit;
    # a tsjs unit has no Cargo root), never by substring
    files = sorted(p for p in listing if _under_unit(p, unit_root) and DD.classify_path(_rel(p, unit_root), ()) is None)
    roots_all = [p for p in files if p.endswith(JS_EXT + TS_EXT)]
    js_roots = [p for p in roots_all if p.endswith(JS_EXT)]
    module_type = package_json.get("type") if package_json and package_json.get("type") in ("module", "commonjs") else "absent"
    if tsconfig is not None or jsconfig is not None:
        cfg = tsconfig if tsconfig is not None else jsconfig
        origin = "tsconfig" if tsconfig is not None else "jsconfig"
        opts = dict(cfg.get("compilerOptions", {}))
        allow_js = bool(opts.get("allowJs", origin == "jsconfig")); check_js = bool(opts.get("checkJs", False))
        mode = "js-allowjs" if allow_js else "ts-tsconfig"; synthesized = None; synth_version = None
        program_roots = roots_all if allow_js else [p for p in roots_all if p.endswith(TS_EXT)]
        js_roots = js_roots if allow_js else []
    else:
        origin, synth_version, allow_js, check_js, mode = "synthesized", 1, True, False, "js-synthesized"
        synthesized = {"allowJs": True, "checkJs": False, "module": "node16", "moduleResolution": "node16", "target": "es2022",
                       "strict": False, "skipLibCheck": True, "types": [], "noEmit": True}
        if any(p.endswith((".jsx", ".tsx")) for p in roots_all):
            synthesized["jsx"] = "preserve"
        opts = dict(synthesized); program_roots = roots_all
    lock_kind = "none"
    for name, kind in (("package-lock.json", "package-lock"), ("pnpm-lock.yaml", "pnpm-lock"), ("yarn.lock", "yarn-lock"), ("bun.lock", "bun-lock"), ("bun.lockb", "bun-lock")):
        if name in lockfiles:
            lock_kind = kind; break
    return {"languageMode": mode, "configOrigin": origin, "synthesizerVersion": synth_version, "synthesizedOptions": synthesized,
            "packageModuleType": module_type, "allowJs": allow_js, "checkJs": check_js,
            # feedback 11: allowJs admits JS roots into the program; checkJs turns on JS diagnostics. Neither is a
            # resolution-completeness claim: that comes only from CoverageV3 after resolution is attempted.
            "jsAdmittedToProgram": allow_js and bool(js_roots), "jsDiagnosticsEnabled": check_js,
            "resolutionCompletenessImplied": False,
            "compilerOptionsSubset": {k: v for k, v in opts.items() if k in ("module", "moduleResolution", "paths", "baseUrl", "rootDirs", "types", "typeRoots", "lib", "target", "jsx", "strict", "exactOptionalPropertyTypes", "skipLibCheck", "allowJs", "checkJs")},
            "programRootFiles": program_roots, "jsRootFiles": js_roots, "lockfileKind": lock_kind,
            "nodeModulesInReadSet": node_modules_in_read_set, "executionCapableResolution": False}


# ---------------------------------------------------------------------------
# Native contexts: one closed record and one H domain per language (blind consumer M-2).
# NativeContextV2 is the RUST context. TypeScriptNativeContextV2 is the TypeScript context and is
# the record that holds `typescriptStdlibMerkleRoot`, whose producing recipe identity-and-evidence
# section 3 already states. No TypeScript universe may bind a Rust descriptor.
# ---------------------------------------------------------------------------

NATIVE_CONTEXT_DOMAINS = {"rust": "native.context.rust.v2", "typescript": "native.context.typescript.v2",
                          "syntax": "native.context.syntax.v2"}
NATIVE_CONTEXT_DEFS = {"rust": "NativeContextV2", "typescript": "TypeScriptNativeContextV2",
                       "syntax": "SyntaxNativeContextV2"}
# closure kind -> the native-context field that must carry its 64-hex closure2 suffix, with the exact
# nesting the citation needs (blind consumer A-1: rustcDevLlvmDigest is inside ToolchainIdentityV1).
CONTEXT_CLOSURE_SUFFIX_FIELDS = {
    "rust": {"rust-dev-llvm": ("toolchain", "rustcDevLlvmDigest")},
    "typescript": {"stdlib": ("toolchain", "typescriptStdlibMerkleRoot")},
    # syntax-only has no suffix-named closure: its one closure is named directly by
    # grammarBundle.closureId and is joined below like any other closure2 identity.
    "syntax": {},
}


def typescript_native_context(toolchain: dict, tool_closure: dict, config_projection: dict,
                              language_mode: str, module_resolution_mode: str, package_module_type: str,
                              node_modules_layout_digest: str | None,
                              lockfile_identity: dict | None) -> dict:
    """Build the closed TypeScript native-context descriptor.

    Field locations, all recomputed by the host before PlanId and never read from a worker claim:
      toolchain.compilerVersion            the semanticVersion of the ADMITTED signed compiler closure manifest
      toolchain.compilerPackageDigest      a member digest of that retained closure tree
      toolchain.typescriptStdlibMerkleRoot the 64-hex suffix of the kind=stdlib closure2 identity (identity section 3)
      toolchain.standardLibraryComponentDigests  every declaration file of that retained stdlib tree
      toolchain.libSelection               the effective `lib` names, each covered by a retained component
      toolClosure.{compiler,runtime}       member digests of the signed kind=toolchain closure named by closureId
      configProjection                     the effective compilerOptions projection (honored / stripped)
    It carries no platform FIELD, because TypeScript resolution semantics — which specifiers resolve, which
    subjects are examined, what is checked — are platform-invariant by design (section 1.1). That is not a
    claim that the identity is platform-invariant: `toolClosure.closureId` names a signed closure whose
    foundation descriptor includes `platform`, so the same source analysed with the platform-specific
    executables of two families mints two nativeContextIds, as it must, because different bytes ran.
    """
    descriptor = {"schemaVersion": 2, "languageMode": language_mode,
                  "toolchain": toolchain, "toolClosure": tool_closure, "configProjection": config_projection,
                  "moduleResolutionMode": module_resolution_mode, "packageModuleType": package_module_type,
                  "nodeModulesLayoutDigest": node_modules_layout_digest, "lockfileIdentity": lockfile_identity}
    validate_native("TypeScriptNativeContextV2", descriptor)
    return descriptor


def admit_native_context(language: str, descriptor: dict, closure_trees: dict[str, dict]) -> dict:
    """Admit one native context against the RETAINED closure descriptors and trees.

    `closure_trees` maps a `closure2:` identity to the complete admitted foundation `closure` record whose tree
    is retained whole. The stdlib / rust-dev-llvm closure identity is not a separate field: it is recovered as
    `closure2:` + the descriptor's suffix field, and admission requires that a retained closure of the right
    kind recomputes to exactly that identity. Refusals are typed strings, never exceptions, so a fixture can
    assert the exact cause.
    """
    if language not in NATIVE_CONTEXT_DOMAINS:
        raise AdmissionError("NATIVE_CONTEXT_LANGUAGE")
    refusals: list[str] = []
    try:
        validate_native(NATIVE_CONTEXT_DEFS[language], descriptor)
    except Exception as exc:                                # a foreign language/shape remains a typed refusal
        refusal = "native.native-context-language-mismatch:not-" + NATIVE_CONTEXT_DEFS[language]
        if getattr(exc, "validator", None) == "x-opensip-order":
            path = list(exc.absolute_path)
            subject = {("toolchain", "libSelection"): "lib-selection-order",
                       ("toolchain", "standardLibraryComponentDigests"): "stdlib-component-order"}.get(tuple(path), "array-order:" + "/".join(map(str, path)))
            refusal = "native.native-context-field-mismatch:" + subject
        return {"language": language, "domain": NATIVE_CONTEXT_DOMAINS[language],
                "nativeContextId": "sha256:" + "0" * 64, "planNativeContextDigest": "0" * 64,
                "refusals": [refusal]}

    def retained(closure_id: str, want_kind: str, where: str) -> dict | None:
        record = closure_trees.get(closure_id)
        if record is None:
            refusals.append("native.native-context-closure-unretained:" + where); return None
        try:
            recomputed = IM.identifier("closure", record)
        except Exception:
            refusals.append("native.native-context-closure-malformed:" + where); return None
        if recomputed != closure_id:
            refusals.append("native.native-context-closure-identity-mismatch:" + where); return None
        if record["kind"] != want_kind:
            refusals.append("native.native-context-closure-kind-mismatch:" + where); return None
        return record

    suffix_closures: dict[str, dict | None] = {}
    for kind, (parent, field) in CONTEXT_CLOSURE_SUFFIX_FIELDS[language].items():
        suffix_closures[kind] = retained("closure2:" + descriptor[parent][field], kind, parent + "." + field)

    if language == "typescript":
        toolchain, tools = descriptor["toolchain"], descriptor["toolClosure"]
        options = descriptor["configProjection"]["honoredOptions"]
        if descriptor["moduleResolutionMode"] != options["moduleResolution"]:
            refusals.append("native.native-context-field-mismatch:moduleResolutionMode")
        # Effective lib names are case-insensitive in the compiler. Each record retains its
        # specified order for hashing; their selected name sets must describe the same input.
        selected = [x.lower() for x in toolchain["libSelection"]]
        if len(set(selected)) != len(selected):
            refusals.append("native.native-context-field-mismatch:duplicate-lib-selection")
        if toolchain["libSelection"] != sorted(toolchain["libSelection"], key=lambda x: x.encode("utf-8")):
            refusals.append("native.native-context-field-mismatch:lib-selection-order")
        if options["lib"] is not None and set(selected) != {x.lower() for x in options["lib"]}:
            refusals.append("native.native-context-field-mismatch:libSelection")
        components = [x["component"] for x in toolchain["standardLibraryComponentDigests"]]
        if components != sorted(components, key=lambda x: x.encode("utf-8")) or len(set(components)) != len(components):
            refusals.append("native.native-context-field-mismatch:stdlib-component-order")
        stdlib = suffix_closures["stdlib"]
        if stdlib is not None:
            declarations = [b for b in stdlib["tree"] if b["path"].endswith(".d.ts")]
            by_component: dict[str, str] = {}
            for blob in declarations:
                name = blob["path"].rpartition("/")[2]
                if name in by_component:              # two tree paths, one component name: the join is ambiguous
                    refusals.append("native.native-context-stdlib-tree-ambiguous-basename:" + name)
                by_component[name] = blob["sha256"]
            declared = {c["component"] for c in toolchain["standardLibraryComponentDigests"]}
            for component in toolchain["standardLibraryComponentDigests"]:
                if by_component.get(component["component"]) != component["sha256"]:
                    refusals.append("native.native-context-stdlib-tree-mismatch:" + component["component"])
            # the row set is the COMPLETE declaration inventory of the retained tree, selected or not:
            # dropping an unselected row would admit an alternate partial inventory for the same retained library
            for name in sorted(set(by_component) - declared):
                refusals.append("native.native-context-stdlib-inventory-incomplete:" + name)
            for lib in toolchain["libSelection"]:
                if "lib.%s.d.ts" % lib.lower() not in declared:
                    refusals.append("native.native-context-lib-not-retained:" + lib)
        compiler_closure = retained(tools["closureId"], "toolchain", "toolClosure.closureId")
        digests = {b["sha256"] for b in compiler_closure["tree"]} if compiler_closure else set()
        if compiler_closure is not None:
            if compiler_closure["semanticVersion"] != toolchain["compilerVersion"]:
                refusals.append("native.native-context-compiler-version-not-from-manifest")
            for role in ("compiler", "runtime"):
                if tools[role] not in digests:
                    refusals.append("native.native-context-tool-not-in-closure:" + role)
            if toolchain["compilerPackageDigest"] not in digests:
                refusals.append("native.native-context-tool-not-in-closure:compilerPackageDigest")

    if language == "rust":
        toolchain, tools = descriptor["toolchain"], descriptor["toolClosure"]
        # CC-4: every selected tool digest equals its entry in the sealed ToolClosureV1. The exact
        # counterpart of the TypeScript compiler/runtime membership check; a claimant cannot name a
        # rustc, cargo or proc-macro server that is not a member of the retained signed closure.
        tool_closure = retained(tools["closureId"], "toolchain", "toolClosure.closureId")
        digests = {b["sha256"] for b in tool_closure["tree"]} if tool_closure else set()
        if tool_closure is not None:
            for role in ("rustc", "cargo", "procMacroServer"):
                if tools[role] not in digests:
                    refusals.append("native.native-context-tool-not-in-closure:" + role)
            for role in ("linker", "ar"):                 # optional selections; absent stays absent
                if tools[role] is not None and tools[role] not in digests:
                    refusals.append("native.native-context-tool-not-in-closure:" + role)
            if tool_closure["semanticVersion"] != toolchain["rustcVersion"]:
                refusals.append("native.native-context-compiler-version-not-from-manifest")
        if toolchain["targetTriple"] != descriptor["targetTriple"]:
            refusals.append("native.native-context-field-mismatch:targetTriple")
        components = [x["component"] for x in toolchain["standardLibraryComponentDigests"]]
        if components != sorted(components, key=lambda x: x.encode("utf-8")) or len(set(components)) != len(components):
            refusals.append("native.native-context-field-mismatch:stdlib-component-order")
        if descriptor["configProjection"]["rustflags"]["executableSelected"]:
            refusals.append("native.native-context-field-mismatch:executableSelected")

    if language == "syntax":
        # The grammar bundle is pinned exactly the way a toolchain is: an admitted kind=grammar
        # closure, a version that comes FROM its manifest rather than being asserted beside it, and
        # every grammar definition present in the retained tree. Nothing here reads a compiler.
        bundle = descriptor["grammarBundle"]
        grammar_closure = retained(bundle["closureId"], "grammar", "grammarBundle.closureId")
        digests = {b["sha256"] for b in grammar_closure["tree"]} if grammar_closure else set()
        if grammar_closure is not None:
            if grammar_closure["semanticVersion"] != bundle["parserVersion"]:
                refusals.append("native.syntax-grammar-version-not-from-manifest")
            if bundle["bundleDigest"] not in digests:
                refusals.append("native.syntax-grammar-bundle-not-in-closure")
            for grammar in bundle["grammars"]:
                if grammar["grammarDigest"] not in digests:
                    refusals.append("native.syntax-grammar-not-in-closure:" + grammar["grammarId"])
            if bundle["normalizer"]["specificationDigest"] not in digests:
                refusals.append("native.syntax-normalizer-spec-not-in-closure")
        # One suffix must select one grammar, or 'the grammar its extension maps to' is ambiguous
        # and a body could be parsed two ways under one universe.
        owners: dict[str, list[str]] = {}
        for grammar in bundle["grammars"]:
            for suffix in grammar["suffixes"]:
                owners.setdefault(suffix, []).append(grammar["grammarId"])
        for suffix in sorted(s for s, g in owners.items() if len(g) > 1):
            refusals.append("native.syntax-grammar-suffix-ambiguous:" + suffix)
        # The syntaxClass law. `code` grammars are exactly the languages that can appear in a clone
        # body preimage; `data-document` grammars are bundled, accounted and inventory-bearing but
        # mint no body identity. Enforcing both directions here is what stops a data grammar from
        # being quietly promoted into the clone identity domain, and stops a code grammar from being
        # demoted so that its clone capability silently disappears.
        for grammar in bundle["grammars"]:
            # syntaxClass is NOT caller-selected: it is read from the CLOSED published registry, so
            # a bundle cannot promote a data grammar into the clone identity domain or demote a code
            # grammar out of it. The body-language enum agreement is asserted alongside, so the
            # registry and the foundation record cannot drift apart silently.
            row = GRAMMAR_CAPABILITY_REGISTRY["languages"].get(grammar["languageId"])
            if row is None:
                refusals.append("native.syntax-grammar-language-not-in-capability-registry:" + grammar["languageId"])
                continue
            if grammar["syntaxClass"] != row["syntaxClass"]:
                refusals.append("native.syntax-grammar-class-not-the-registered-one:" + grammar["languageId"]
                                + ":declared=" + grammar["syntaxClass"] + ":registered=" + row["syntaxClass"])
            in_body_enum = grammar["languageId"] in BODY_LANGUAGE_IDS
            if row["syntaxClass"] == "code" and not in_body_enum:
                refusals.append("native.syntax-grammar-code-language-not-body-identifiable:" + grammar["languageId"])
            if row["syntaxClass"] == "data-document" and in_body_enum:
                refusals.append("native.syntax-grammar-data-language-claims-body-identity:" + grammar["languageId"])
            # The declared suffixes must be the ones the host actually bundles for that language:
            # a bundle row cannot claim a suffix the discovery table routes elsewhere.
            for suffix in grammar["suffixes"]:
                if BUNDLED_GRAMMARS.get(suffix) != grammar["languageId"]:
                    refusals.append("native.syntax-grammar-suffix-not-bundled-for-language:"
                                    + suffix + ":" + grammar["languageId"])

    identity = native_identity(NATIVE_CONTEXT_DOMAINS[language], NATIVE_CONTEXT_DEFS[language], descriptor)
    out = {"language": language, "domain": NATIVE_CONTEXT_DOMAINS[language], "nativeContextId": identity,
           "planNativeContextDigest": identity.removeprefix("sha256:"), "refusals": sorted(set(refusals))}
    validate_native("NativeContextAdmissionV1", out)
    return out


def universe_context_field_faults(universe: dict, context: dict) -> list[str]:
    """The universe and its native context describe one resolution; where they overlap they must agree.

    `nativeContextId` equality alone cannot authenticate a contradictory universe field: the id commits to
    the context bytes, not to the universe's copy of them. Each row below is a field the two records both
    carry, or a universe flag that is a function of context bytes.
    """
    options = context["configProjection"]["honoredOptions"]
    lockfile = context["lockfileIdentity"]
    expected = {
        "languageMode": context["languageMode"],
        "packageModuleType": context["packageModuleType"],
        "allowJs": options["allowJs"],
        "checkJs": options["checkJs"],
        "lockfileKind": lockfile["kind"] if lockfile is not None else "none",
        "nodeModulesInReadSet": context["nodeModulesLayoutDigest"] is not None,
        "jsDiagnosticsEnabled": options["checkJs"],
        "jsAdmittedToProgram": options["allowJs"] and bool(universe["jsRootFiles"]),
    }
    faults = ["native.universe-context-field-mismatch:" + field
              for field, want in expected.items() if universe[field] != want]
    synthesized = universe["configOrigin"] == "synthesized"
    if synthesized != (universe["languageMode"] == "js-synthesized"):
        faults.append("native.universe-context-field-mismatch:configOrigin")
    if synthesized != bool(context["configProjection"]["configGraphPaths"] == []):
        faults.append("native.universe-context-field-mismatch:configGraphPaths")
    # The exact tsconfig/jsconfig spelling is not derivable here; it is derived from the retained
    # TypeScriptConfigGraphV1 in typescript_universe_retained_input_faults, which is why that record
    # is a required binding input rather than an optional one.
    if synthesized != (universe["synthesizerVersion"] is not None) or \
            synthesized != (universe["synthesizedOptions"] is not None):
        faults.append("native.universe-context-field-mismatch:synthesizedOptions")
    if synthesized and universe["synthesizedOptions"] is not None:
        for field, value in universe["synthesizedOptions"].items():
            if not C.equal_typed(options[field], value):
                faults.append("native.universe-context-field-mismatch:synthesizedOptions." + field)
        if "jsx" not in universe["synthesizedOptions"] and options["jsx"] is not None:
            faults.append("native.universe-context-field-mismatch:synthesizedOptions.jsx")
    if universe["allowJs"] is False and universe["jsRootFiles"]:
        faults.append("native.universe-context-field-mismatch:jsRootFiles")
    return sorted(set(faults))


CONFIG_GRAPH_DOMAIN_NOTE = ("tsconfigGraphHash and nodeModulesLayoutDigest are RAW SHA-256 of C(record), "
                            "not H identities: they name retained records, not typed objects.")


# ---------------------------------------------------------------------------
# CAP-MANIFEST-ID-V1 successor admission (blind consumer Bv2 G6). CVE1 is the CAPABILITY MANIFEST
# encoding, provenance docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding;
# it is unrelated to the relation PAYLOAD codec. Bounded, pure, no network and no execution.
# ---------------------------------------------------------------------------

CAPABILITY_DOMAINS = json.loads((HERE / "capability-manifest-domains.v2.json").read_text(encoding="utf-8"))
CAPABILITY_MANIFEST_DOMAIN = b"opensip.capability-manifest.v1"
_CVE1_MAX_ITEMS = 1 << 20
_CVE1_MAX_DEPTH = 64


def cve1_encode(value: Any) -> bytes:
    """CVE1: eight closed types, NFC strings, maps sorted by unsigned lexicographic key bytes."""
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if isinstance(value, int):
        if 0 <= value <= 2 ** 64 - 1:
            return b"\x03" + value.to_bytes(8, "big")
        if -(2 ** 63) <= value < 0:
            return b"\x07" + (value + (1 << 64)).to_bytes(8, "big")
        raise AdmissionError("CVE1_INTEGER_RANGE")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise AdmissionError("CVE1_NOT_NFC")
        raw = value.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if isinstance(value, list):
        return b"\x05" + len(value).to_bytes(4, "big") + b"".join(cve1_encode(v) for v in value)
    if isinstance(value, dict):
        keys = list(value)
        if any(not isinstance(k, str) for k in keys):
            raise AdmissionError("CVE1_MAP_KEY")
        if len(set(keys)) != len(keys):
            raise AdmissionError("CVE1_DUPLICATE_KEY")
        rows = sorted(((k.encode("utf-8"), k) for k in keys))
        return b"\x06" + len(rows).to_bytes(4, "big") + b"".join(
            cve1_encode(k) + cve1_encode(value[k]) for _, k in rows)
    raise AdmissionError("CVE1_TYPE")


def cve1_decode(raw: bytes) -> Any:
    """Bounded decoder. Trailing bytes, unknown tags, non-NFC strings, unsorted or duplicate map keys,
    out-of-range counts and excessive nesting all refuse; nothing is repaired."""
    value, offset = _cve1_read(raw, 0, 0)
    if offset != len(raw):
        raise AdmissionError("CVE1_TRAILING_BYTES")
    return value


def _cve1_read(raw: bytes, offset: int, depth: int = 0):
    if depth > _CVE1_MAX_DEPTH:
        raise AdmissionError("CVE1_DEPTH_BOUND")
    if offset >= len(raw):
        raise AdmissionError("CVE1_TRUNCATED")
    tag = raw[offset]; offset += 1
    if tag == 0x00:
        return None, offset
    if tag == 0x01:
        return False, offset
    if tag == 0x02:
        return True, offset
    if tag in (0x03, 0x07):
        if offset + 8 > len(raw):
            raise AdmissionError("CVE1_TRUNCATED")
        chunk = int.from_bytes(raw[offset:offset + 8], "big"); offset += 8
        if tag == 0x03:
            return chunk, offset
        if chunk < (1 << 63):
            raise AdmissionError("CVE1_NEGATIVE_RANGE")
        return chunk - (1 << 64), offset
    if tag == 0x04:
        if offset + 4 > len(raw):
            raise AdmissionError("CVE1_TRUNCATED")
        length = int.from_bytes(raw[offset:offset + 4], "big"); offset += 4
        if offset + length > len(raw):
            raise AdmissionError("CVE1_TRUNCATED")
        try:
            text = raw[offset:offset + length].decode("utf-8", "strict")
        except UnicodeError as exc:
            raise AdmissionError("CVE1_UTF8") from exc
        if unicodedata.normalize("NFC", text) != text:
            raise AdmissionError("CVE1_NOT_NFC")
        return text, offset + length
    if tag in (0x05, 0x06):
        if offset + 4 > len(raw):
            raise AdmissionError("CVE1_TRUNCATED")
        count = int.from_bytes(raw[offset:offset + 4], "big"); offset += 4
        if count > _CVE1_MAX_ITEMS:
            raise AdmissionError("CVE1_COUNT_BOUND")
        if tag == 0x05:
            items = []
            for _ in range(count):
                item, offset = _cve1_read(raw, offset, depth + 1); items.append(item)
            return items, offset
        out: dict = {}; previous = None
        for _ in range(count):
            key, offset = _cve1_read(raw, offset, depth + 1)
            if not isinstance(key, str):
                raise AdmissionError("CVE1_MAP_KEY")
            encoded = key.encode("utf-8")
            if previous is not None and encoded <= previous:
                raise AdmissionError("CVE1_MAP_ORDER")
            previous = encoded
            item, offset = _cve1_read(raw, offset, depth + 1); out[key] = item
        return out, offset
    raise AdmissionError("CVE1_TAG")


def capability_manifest_identity(committed_bytes: bytes) -> str:
    """The inherited applied recipe, unchanged: 64 lowercase hex, no prefix."""
    return raw_sha256(CAPABILITY_MANIFEST_DOMAIN + b"\x00" + committed_bytes)


def admit_capability_manifest(committed_bytes: bytes) -> dict:
    """Admit a committed CapabilityManifestV1 under the CURRENT ADM-DOMAIN successor registry.

    Verifying the raw hash is not admission: the manifest is a PlanId input, so an unknown relation
    or a rung from another relation ladder must be REFUSED here, not carried into a Plan. Gate order
    is the inherited one: ADM-CLOSED, then ADM-DOMAIN, then ADM-ORDER.
    """
    refusals: list[str] = []
    try:
        value = cve1_decode(committed_bytes)
    except AdmissionError as exc:
        return {"result": "REFUSE", "refusals": ["capability.cve1-decode:" + str(exc)],
                "capabilityManifestId": None, "relations": []}
    registries = CAPABILITY_DOMAINS["registries"]
    shapes = CAPABILITY_DOMAINS["recordShape"]
    # ADM-TYPE: exact JSON type, before any content comparison. `type(x) is int` and never isinstance,
    # because CVE1 is total on booleans and would otherwise mint a wrong id rather than failing.
    STRING_POSITIONS = {
        "ProviderCapability": ("providerId", "language", "providerVersionSource", "toolchainIdentitySource"),
        "AbsentCapability": ("providerId", "language", "deficiency", "coverageState"),
    }

    def typed(record, name):
        ok = True
        for field in STRING_POSITIONS.get(name, ()):
            if type(record.get(field)) is not str:
                refusals.append("capability.adm-type:" + name + "." + field); ok = False
        for field in ("platformIds", "relationIds"):
            if field in record and type(record[field]) is not list:
                refusals.append("capability.adm-type:" + name + "." + field); ok = False
        if name == "ProviderCapability" and type(record.get("relations")) is not dict:
            refusals.append("capability.adm-type:ProviderCapability.relations"); ok = False
        return ok

    def closed(record, name):
        want = set(shapes[name]["requiredKeys"])
        if not isinstance(record, dict) or set(record) != want:
            refusals.append("capability.adm-closed:" + name)
            return False
        return typed(record, name)

    def strict_unique(values, where):
        if values != sorted(values) or len(set(values)) != len(values):
            refusals.append("capability.adm-order:" + where)

    if type(value.get("schemaVersion")) is not int:      # a boolean is not an integer
        refusals.append("capability.adm-type:CapabilityManifestV1.schemaVersion")
    if type(value.get("profile")) is not str:
        refusals.append("capability.adm-type:CapabilityManifestV1.profile")
    for collection in ("providers", "coverageForAbsent"):
        if type(value.get(collection)) is not list:
            refusals.append("capability.adm-type:CapabilityManifestV1." + collection)
    if not closed(value, "CapabilityManifestV1") or refusals:
        return {"result": "REFUSE", "refusals": sorted(set(refusals)), "capabilityManifestId": None, "relations": []}
    relations: set[str] = set()
    ladders = registries["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    members = set(registries["RELATION-DOMAIN-V2"]["members"])
    # Declared traversal order: providers[i].platformIds, coverageForAbsent[i].relationIds,
    # providers, coverageForAbsent.
    for provider in value["providers"]:
        if not closed(provider, "ProviderCapability"):
            continue
        for relation, rung in provider["relations"].items():
            relations.add(relation)
            if relation not in members:
                refusals.append("capability.adm-domain:relation:" + relation); continue
            if type(rung) is not str:
                refusals.append("capability.adm-type:ProviderCapability.relations.value"); continue
            if rung not in ladders[relation]:
                # A rung that is a member of ANOTHER relation ladder is still not this one's.
                refusals.append("capability.adm-domain:rung:" + relation + "@" + str(rung))
        for platform in provider["platformIds"]:
            if type(platform) is not str:
                refusals.append("capability.adm-type:ProviderCapability.platformIds[]"); continue
            if platform not in registries["PLATFORM-ID-DOMAIN-V1"]["members"]:
                refusals.append("capability.adm-domain:platformId:" + str(platform))
        strict_unique(provider["platformIds"], "platformIds")
    for absent in value["coverageForAbsent"]:
        if not closed(absent, "AbsentCapability"):
            continue
        for relation in absent["relationIds"]:
            relations.add(relation)
            if relation not in members:
                refusals.append("capability.adm-domain:relation:" + str(relation))
        strict_unique(absent["relationIds"], "relationIds")
        if absent["deficiency"] not in registries["DEFICIENCY-DOMAIN-V1"]["members"]:
            refusals.append("capability.adm-domain:deficiency:" + str(absent["deficiency"]))
        if absent["coverageState"] not in registries["COVERAGE-STATE-DOMAIN-V1"]["members"]:
            refusals.append("capability.adm-domain:coverageState:" + str(absent["coverageState"]))
    # providers and coverageForAbsent are themselves declared-sorted collections; a duplicated row is
    # an ordering violation, and providerId is the declared sort key.
    strict_unique([p["providerId"] for p in value["providers"] if isinstance(p, dict) and type(p.get("providerId")) is str], "providers")
    strict_unique([cve1_encode(a).hex() for a in value["coverageForAbsent"] if isinstance(a, dict)], "coverageForAbsent")
    if cve1_encode(value) != committed_bytes:
        refusals.append("capability.adm-order:not-canonical-cve1")
    return {"result": "REFUSE" if refusals else "ADMIT", "refusals": sorted(set(refusals)),
            "capabilityManifestId": None if refusals else capability_manifest_identity(committed_bytes),
            "relations": sorted(relations)}


def capability_manifest_gate_vectors() -> dict:
    """The four inherited gates, exercised on the live inherited golden and three bad values."""
    delivery = json.loads((HERE.parent.parent / "artifacts/delivery.v4.json").read_text(encoding="utf-8"))
    recipe = next(o for o in delivery["derivedFrom"]["operations"] if o["path"] == "capabilityManifestIdentity")["value"]
    golden = bytes.fromhex(recipe["vectors"]["byId"]["DCM-1-core"]["committedBytesHex"])
    value = cve1_decode(golden)

    def refusals(mutate):
        candidate = copy.deepcopy(value); mutate(candidate)
        return admit_capability_manifest(cve1_encode(candidate))["refusals"]
    deep = None
    for _ in range(_CVE1_MAX_DEPTH + 2):
        deep = [deep]
    try:
        cve1_decode(cve1_encode(deep)); bounded = False
    except AdmissionError:
        bounded = True
    return {
        "inheritedGoldenAdmits": admit_capability_manifest(golden)["result"] == "ADMIT",
        "booleanSchemaVersion": refusals(lambda v: v.update(schemaVersion=True)),
        "duplicatePlatformId": refusals(lambda v: v["providers"][0]["platformIds"].append(v["providers"][0]["platformIds"][0])),
        "duplicateProvider": refusals(lambda v: v["providers"].append(copy.deepcopy(v["providers"][0]))),
        "gateOrder": CAPABILITY_DOMAINS["gateOrder"],
        "declaredOpenPositions": len(CAPABILITY_DOMAINS["declaredOPEN"]),
        "decoderDepthBounded": bounded,
    }


def native_digest_annotation_coverage() -> dict:
    """The closing digest law extended to this bundle: every 64-hex or sha256: field must declare an
    x-opensip-digest representation, retention and authority. A new field without one is inadmissible."""
    hexish = ("^[0-9a-f]{64}(?![\\s\\S])", "^sha256:[0-9a-f]{64}(?![\\s\\S])")
    refs = ("#/$defs/DigestHex", "#/$defs/Sha256Text")
    seen: dict[str, bool] = {}

    def walk(node, path):
        if isinstance(node, dict):
            if node.get("pattern") in hexish or node.get("$ref") in refs:
                seen[path] = "x-opensip-digest" in node
                return
            for key, value in node.items():
                walk(value, path if key in ("properties", "items", "$defs", "oneOf", "anyOf",
                                            "additionalProperties") else path + "." + key)
        elif isinstance(node, list):
            for value in node:
                walk(value, path)
    for name, node in SCHEMAS["$defs"].items():
        if name not in ("DigestHex", "Sha256Text"):
            walk(node, name)
    return {"total": len(seen), "annotated": sum(1 for v in seen.values() if v),
            "unannotated": sorted(p for p, v in seen.items() if not v)}


def typescript_config_graph_digest(graph: dict) -> str:
    """`tsconfigGraphHash` = raw SHA-256 of C(TypeScriptConfigGraphV1). Section 2.2."""
    validate_native("TypeScriptConfigGraphV1", graph)
    return raw_sha256(C.canonical(graph))


def resolved_node_modules_layout_digest(layout: dict) -> str:
    """`nodeModulesLayoutDigest` = raw SHA-256 of C(ResolvedNodeModulesLayoutV1). Section 2.4."""
    validate_native("ResolvedNodeModulesLayoutV1", layout)
    return raw_sha256(C.canonical(layout))


def typescript_config_origin(graph: dict) -> str:
    """`configOrigin` DERIVED from the retained config graph, never asserted by a caller: it is the
    kind of the SELECTED ENTRY config, and `synthesized` exactly when there is no entry. Deriving it
    from the whole node set would call a jsconfig.json that extends a shared base.json a tsconfig
    program, which it is not."""
    entry = graph["entryConfigPath"]
    if entry is None:
        return "synthesized"
    node = next((n for n in graph["nodes"] if n["path"] == entry), None)
    if node is None:
        raise AdmissionError("CONFIG_GRAPH_ENTRY_NOT_A_NODE")
    return "jsconfig" if node["kind"] == "jsconfig" else "tsconfig"


def typescript_config_graph_faults(graph: dict) -> list[str]:
    """Membership, reachability and acyclicity of the retained extends graph, plus a `kind` that
    cannot contradict its own basename, so the entry cannot be relabelled."""
    faults: list[str] = []
    by_path = {n["path"]: n for n in graph["nodes"]}
    for node in graph["nodes"]:
        basename = node["path"].rpartition("/")[2]
        expected = basename.removesuffix(".json") if basename in ("tsconfig.json", "jsconfig.json") else "other"
        if node["kind"] != expected:
            faults.append("native.config-graph-kind-contradicts-path:" + node["path"])
        for edge in node["extendsResolved"]:
            if edge not in by_path:
                faults.append("native.config-graph-edge-not-a-node:" + edge)
    entry = graph["entryConfigPath"]
    if entry is None:
        if graph["nodes"]:
            faults.append("native.config-graph-synthesized-with-nodes")
        return sorted(set(faults))
    if entry not in by_path:
        faults.append("native.config-graph-entry-not-a-node:" + entry)
        return sorted(set(faults))
    reached, frontier = {entry}, [entry]
    while frontier:
        current = frontier.pop()
        for edge in by_path[current]["extendsResolved"]:
            if edge not in reached and edge in by_path:
                reached.add(edge); frontier.append(edge)
    for node in graph["nodes"]:
        if node["path"] not in reached:
            faults.append("native.config-graph-node-unreachable-from-entry:" + node["path"])
    state: dict[str, int] = {}

    def visit(path: str) -> None:
        if state.get(path) == 2:
            return
        if state.get(path) == 1:
            faults.append("native.config-graph-cycle:" + path); return
        state[path] = 1
        for edge in by_path.get(path, {"extendsResolved": []})["extendsResolved"]:
            visit(edge)
        state[path] = 2
    visit(entry)
    return sorted(set(faults))



def typescript_universe_retained_input_faults(universe: dict, context: dict, retained: dict,
                                              snapshot_inventory: list[dict]) -> list[str]:
    """The TypeScript universe's two retained records, and their joins to the context and snapshot.
    Neither `tsconfigGraphHash` nor `nodeModulesLayoutDigest` is an opaque string here."""
    faults: list[str] = []
    inventory = {row["path"]: row for row in snapshot_inventory}

    graph = retained.get("configGraph")
    if graph is None:
        faults.append("native.universe-retained-input-missing:configGraph")
    else:
        validate_native("TypeScriptConfigGraphV1", graph)
        if typescript_config_graph_digest(graph) != universe["tsconfigGraphHash"]:
            faults.append("native.universe-retained-input-identity-mismatch:tsconfigGraphHash")
        # The universe key and the context must describe ONE config graph.
        if sorted(n["path"] for n in graph["nodes"]) != sorted(context["configProjection"]["configGraphPaths"]):
            faults.append("native.universe-retained-input-mismatch:configGraphPaths")
        for node in graph["nodes"]:
            row = inventory.get(node["path"])
            if row is None or row["sha256"] != node["contentSha256"]:
                faults.append("native.universe-source-mismatch:" + node["path"])
        faults.extend(typescript_config_graph_faults(graph))
        # Section 2.4's configOrigin agreement, now with an input it can actually be checked
        # against: the spelling is derived from the ENTRY of the retained graph, not asserted.
        try:
            derived = typescript_config_origin(graph)
        except AdmissionError as exc:
            faults.append("native.universe-context-field-mismatch:configOrigin:" + str(exc)); derived = None
        if derived is not None and universe["configOrigin"] != derived:
            faults.append("native.universe-context-field-mismatch:configOrigin")

    layout = retained.get("nodeModulesLayout")
    if context["nodeModulesLayoutDigest"] is None:
        if universe["nodeModulesInReadSet"]:
            faults.append("native.universe-context-field-mismatch:nodeModulesInReadSet")
        if layout is not None:
            faults.append("native.universe-retained-input-unselected:nodeModulesLayout")
    elif layout is None:
        faults.append("native.universe-retained-input-missing:nodeModulesLayout")
    else:
        validate_native("ResolvedNodeModulesLayoutV1", layout)
        if resolved_node_modules_layout_digest(layout) != context["nodeModulesLayoutDigest"]:
            faults.append("native.universe-retained-input-identity-mismatch:nodeModulesLayoutDigest")
        if not universe["nodeModulesInReadSet"]:
            faults.append("native.universe-context-field-mismatch:nodeModulesInReadSet")
        # A resolved bare specifier must land on a package this layout actually carries.
        installed = {row["installPath"] for row in layout["entries"]}
        for row in layout["entries"]:
            if row["realPath"] != row["installPath"] and row["realPath"] not in installed:
                faults.append("native.universe-retained-input-mismatch:nodeModulesLayout.realPath:" + row["realPath"])

    for path in universe["programRootFiles"] + universe["jsRootFiles"]:
        if path not in inventory:
            faults.append("native.universe-path-not-inventoried:" + path)
    return sorted(set(faults))


def bind_typescript_universe(universe: dict, admission: dict, context: dict,
                             retained: dict | None = None, snapshot_inventory: list[dict] | None = None) -> dict:
    """Bind a typescript-v2 universe to its admitted context, before PlanId.

    `context`, `retained` and `snapshot_inventory` are all REQUIRED, exactly as for
    `bind_rust_universe`: there is no context-free or input-free admit path, because an optional
    field-agreement check is not a rule — a caller that omitted it would get the very bypass this
    join exists to close. Omission is the typed refusal `native.universe-context-not-supplied` /
    `native.universe-retained-inputs-not-supplied`, never an ADMIT. `retained` is
    `{configGraph: TypeScriptConfigGraphV1, nodeModulesLayout: ResolvedNodeModulesLayoutV1|absent}`.
    Nothing here executes a compiler, a resolver or a filesystem read.
    """
    validate_native("TypeScriptUniverseV2ResolvedInputs", universe)
    refusals = list(admission["refusals"])
    if admission["language"] != "typescript" or admission["domain"] != NATIVE_CONTEXT_DOMAINS["typescript"]:
        refusals.append("native.native-context-language-mismatch:typescript-universe-bound-to-" + admission["domain"])
    if universe["nativeContextId"] != admission["nativeContextId"]:
        refusals.append("native.universe-context-binding-mismatch")
    if context is None:
        refusals.append("native.universe-context-not-supplied")
    elif native_identity(NATIVE_CONTEXT_DOMAINS["typescript"], "TypeScriptNativeContextV2", context) \
            != admission["nativeContextId"]:
        refusals.append("native.universe-context-binding-mismatch:context-bytes-are-not-the-admitted-ones")
    else:
        refusals.extend(universe_context_field_faults(universe, context))
        if retained is None or snapshot_inventory is None:
            refusals.append("native.universe-retained-inputs-not-supplied")
        else:
            refusals.extend(typescript_universe_retained_input_faults(universe, context, retained, snapshot_inventory))
    universe_id = native_identity("native.semantic-universe.typescript.v2", "TypeScriptUniverseV2ResolvedInputs", universe)
    return {"result": "REFUSE" if refusals else "ADMIT", "refusals": sorted(set(refusals)),
            "universeId": universe_id, "sourceUniverse": universe_id.removeprefix("sha256:"),
            "nativeContextId": universe["nativeContextId"]}


# ---------------------------------------------------------------------------
# Rust semantic universe (section 2.1, 3.3, 3.4, 3.6, 11). One binding per language; the Rust
# binding is the exact counterpart of bind_typescript_universe, over the SAME already-registered
# Rust input records. No second compiler protocol or language is introduced here.
# ---------------------------------------------------------------------------

NATIVE_UNIVERSE_DOMAINS = {"rust": "native.semantic-universe.rust.v2",
                           "typescript": "native.semantic-universe.typescript.v2",
                           "syntax": "native.semantic-universe.syntax.v2"}
NATIVE_UNIVERSE_DEFS = {"rust": "RustUniverseV2ResolvedInputs",
                        "typescript": "TypeScriptUniverseV2ResolvedInputs",
                        "syntax": "SyntaxUniverseV2ResolvedInputs"}


def bind_syntax_universe(universe: dict, admission: dict, context: dict,
                         retained: dict | None = None, snapshot_inventory: list[dict] | None = None) -> dict:
    """Bind a syntax-v2 universe to its admitted grammar context, before PlanId.

    The exact counterpart of the two compiler bindings, with the same no-optional-join rule: the
    context is REQUIRED and must be the admitted BYTES, not merely a matching identity, because an
    optional agreement check is a bypass rather than a rule.

    It is deliberately shorter than the compiler bindings because a grammar-only universe has fewer
    inputs to agree with, not because its join is weaker: there is no config graph, no lockfile, no
    node_modules layout and no dependency set to reconcile. `retained` and `snapshot_inventory` are
    accepted for signature parity and are not consulted -- the universe names no retained nested
    record and no snapshot path, so requiring them would be theatre.

    Nothing here executes a parser, a compiler or a filesystem read.
    """
    validate_native("SyntaxUniverseV2ResolvedInputs", universe)
    refusals = list(admission["refusals"])
    if admission["language"] != "syntax" or admission["domain"] != NATIVE_CONTEXT_DOMAINS["syntax"]:
        refusals.append("native.native-context-language-mismatch:syntax-universe-bound-to-" + admission["domain"])
    if universe["nativeContextId"] != admission["nativeContextId"]:
        refusals.append("native.universe-context-binding-mismatch")
    if context is None:
        refusals.append("native.universe-context-not-supplied")
    elif native_identity(NATIVE_CONTEXT_DOMAINS["syntax"], "SyntaxNativeContextV2", context) \
            != admission["nativeContextId"]:
        refusals.append("native.universe-context-binding-mismatch:context-bytes-are-not-the-admitted-ones")
    else:
        # The selection must name grammars the admitted bundle actually contains. A selection that
        # named an absent grammar would commit a universe identity to a parse that could not have
        # happened, and the selection is part of the identity precisely so it is not an invisible
        # default: a different selected set is a DIFFERENT universe, visible to every consumer.
        available = {g["grammarId"] for g in context["grammarBundle"]["grammars"]}
        for grammar_id in sorted(set(universe["selectedGrammarIds"]) - available):
            refusals.append("native.syntax-grammar-not-in-bundle:" + grammar_id)
    universe_id = native_identity(NATIVE_UNIVERSE_DOMAINS["syntax"], "SyntaxUniverseV2ResolvedInputs", universe)
    return {"result": "REFUSE" if refusals else "ADMIT", "refusals": sorted(set(refusals)),
            "universeId": universe_id, "sourceUniverse": universe_id.removeprefix("sha256:"),
            "nativeContextId": universe["nativeContextId"]}
# Nested Rust semantic inputs. Each one is an H identity over a record this bundle already defines;
# section 11 named every domain, and the cargo config projection domain is named there now too.
CARGO_CONFIG_PROJECTION_DOMAIN = "native.cargo-config-projection.v2"
UNIFIED_FEATURES_DOMAIN = "native.unified-features.rust.v1"
PREPARED_OUTPUT_SET_DOMAIN = "native.prepared-output-set.v3"
DEPENDENCY_SOURCE_SET_DOMAIN = "native.dependency-source-set.v1"
DEPENDENCY_FILE_MANIFEST_DOMAIN = "native.dependency-file-manifest.v1"
SOURCE_UNIT_OWNERSHIP_DOMAIN = "native.source-unit-ownership.v1"


COMPILATION_UNIT_DOMAIN = "native.compilation-unit.v1"


def unit_identity_projection(unit: dict) -> dict:
    """The closed, PUBLISHED preimage of a compilation unit identity."""
    return {"schemaVersion": 1, "markerPath": unit["markerPath"],
            "targetKind": unit["targetKind"], "targetName": unit["targetName"]}


def source_unit_id(unit: dict) -> str:
    """H(native.compilation-unit.v1, UnitIdentityV1) over the unit's own four closed fields.

    DERIVED, not opaque: the preimage record, its domain, its codec and its selector are all
    published, so any consumer rebuilds it from the row that carries it. An earlier draft joined the
    fields with delimiters, which was injective only by excluding `#` from markerPath - and a `#` in
    a repository directory is admissible under the canonical repository-path contract, so that
    recipe narrowed admitted paths to make a delimiter work. H needs no such restriction and is fixed
    width for every admitted path and name length."""
    return native_identity(COMPILATION_UNIT_DOMAIN, "UnitIdentityV1", unit_identity_projection(unit))


def source_unit_ownership_faults(ownership: dict, universe: dict, inventory: dict) -> list[str]:
    """Internal coherence of one SourceUnitOwnershipV1, against the universe and the snapshot.

    Every unitId is re-derived from its own metadata, every marker and owned path is a source of THIS
    snapshot, every selection and every ownership row names a unit this record declares, and every
    deferring unit names a crate the universe committed an edition for. A record that passes this
    still proves nothing about the real repository: it is a trusted producer observation."""
    faults: list[str] = []
    declared = {unit["unitId"] for unit in ownership["units"]}
    for unit in ownership["units"]:
        if unit["unitId"] != source_unit_id(unit):
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership.unitId")
        if unit["markerPath"] not in inventory:
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership.markerPath")
        if unit["targetEdition"] is None and unit["crateName"] not in universe["edition"]:
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership.crateName")
    for unit_id in ownership["selectedUnitIds"]:
        if unit_id not in declared:
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership.selectedUnitIds")
    for row in ownership["ownership"]:
        if row["path"] not in inventory:
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership.path")
        if row["unitId"] not in declared:
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership.unitId")
    return faults


def source_unit_ownership_identity(ownership: dict) -> str:
    """H(native.source-unit-ownership.v1, SourceUnitOwnershipV1). The committed relation from a
    snapshot source path to the compilation unit that reads it, which is what decides a body span's
    source dialect. A crate-name-to-root map cannot do this: #[path], files shared by several targets
    and several compilation contexts of one crate all defeat a directory inference, so the relation is
    stated rather than guessed. This admits no compiler and qualifies no enumerator; it says only what
    the producer claims it enumerated."""
    return native_identity(SOURCE_UNIT_OWNERSHIP_DOMAIN, "SourceUnitOwnershipV1", ownership)


def cargo_config_projection_identity(projection: dict) -> str:
    """H(native.cargo-config-projection.v2, CargoConfigProjectionV2). Section 2.1 requires
    `rust-v2.configProjectionSha256` to be H over this record; this names the domain the older prose
    left unstated. It is NOT `projectionSha256`, which is the raw digest of the single projected
    `.cargo/config.toml` FILE the adapter materializes under CC-5."""
    return native_identity(CARGO_CONFIG_PROJECTION_DOMAIN, "CargoConfigProjectionV2", projection)


def unified_features_identity(features: dict) -> str:
    return native_identity(UNIFIED_FEATURES_DOMAIN, "UnifiedFeaturesV1", features)


def prepared_output_set_identity(prepared: dict) -> str:
    return native_identity(PREPARED_OUTPUT_SET_DOMAIN, "PreparedOutputSetV3", prepared)


def dependency_source_set_identity(descriptor: dict) -> str:
    return native_identity(DEPENDENCY_SOURCE_SET_DOMAIN, "DependencySourceSetV1", descriptor)


def rust_universe_context_field_faults(universe: dict, context: dict) -> list[str]:
    """The rust-v2 universe and NativeContextV2 describe one resolution; where they overlap they
    must agree. Every row is a field section 2.1 or 2.3 states both records determine. Equality of
    `nativeContextId` alone cannot authenticate a contradictory universe: the id commits to the
    context bytes, not to the universe's copy of them."""
    faults: list[str] = []
    for field in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
        if not C.equal_typed(universe[field], context[field]):
            faults.append("native.universe-context-field-mismatch:" + field)
    if not C.equal_typed(universe["rustflags"], context["configProjection"]["rustflags"]):
        faults.append("native.universe-context-field-mismatch:rustflags")
    if universe["configProjectionSha256"] != cargo_config_projection_identity(context["configProjection"]).removeprefix("sha256:"):
        faults.append("native.universe-context-field-mismatch:configProjectionSha256")
    # 2.1: executionCapableResolution names the MEANING of the universe and is exactly
    # `preparedResolution != none`; the prepared set id is null exactly when there is none.
    # Retained inert prepared bytes never imply an execution grant, in either direction.
    prepared = universe["preparedResolution"] != "none"
    if universe["executionCapableResolution"] != prepared:
        faults.append("native.universe-context-field-mismatch:executionCapableResolution")
    if (universe["preparedOutputSetId"] is None) is prepared:
        faults.append("native.universe-context-field-mismatch:preparedOutputSetId")
    # 2.1: cfg sets differ from the context's base cfg only by ADDITIONS (default primary,
    # primary+test); a set that drops a base cfg would analyse a configuration nothing selected.
    base = set(context["baseCfg"])
    for row in universe["cfgSets"]:
        if not base <= set(row["cfg"]):
            faults.append("native.universe-context-field-mismatch:cfgSets." + row["cfgSetId"])
    keys = [row["cfgSetId"] for row in universe["cfgSets"]]
    if len(set(keys)) != len(keys):
        faults.append("native.universe-context-field-mismatch:duplicate-cfg-set-id")
    return sorted(set(faults))


def rust_universe_retained_input_faults(universe: dict, context: dict, retained: dict,
                                        snapshot_inventory: list[dict]) -> list[str]:
    """The nested Rust semantic identities are not opaque strings. Each must be the exact H identity
    of a RETAINED record of its registered domain, and the records must join the universe, the
    context and the snapshot. `retained` is {dependencySourceSet, unifiedFeatures, preparedOutputSet}
    of already-parsed records; a missing required one is a fault, never a silent skip."""
    faults: list[str] = []
    inventory = {row["path"]: row for row in snapshot_inventory}

    dependency = retained.get("dependencySourceSet")
    if dependency is None:
        faults.append("native.universe-retained-input-missing:dependencySourceSet")
    else:
        validate_native("DependencySourceSetV1", dependency)
        if dependency_source_set_identity(dependency) != universe["dependencySourceSetId"]:
            faults.append("native.universe-retained-input-identity-mismatch:dependencySourceSetId")
        if not C.equal_typed(dependency["lockfileIdentity"], universe["lockfileIdentity"]):
            faults.append("native.universe-retained-input-mismatch:lockfileIdentity")

    ownership = retained.get("sourceUnitOwnership")
    if universe["sourceUnitOwnershipId"] is None:
        if ownership is not None:
            faults.append("native.universe-retained-input-mismatch:sourceUnitOwnership-unreferenced")
    elif ownership is None:
        faults.append("native.universe-retained-input-missing:sourceUnitOwnership")
    else:
        validate_native("SourceUnitOwnershipV1", ownership)
        if source_unit_ownership_identity(ownership) != universe["sourceUnitOwnershipId"]:
            faults.append("native.universe-retained-input-identity-mismatch:sourceUnitOwnershipId")
        faults.extend(source_unit_ownership_faults(ownership, universe, inventory))

    features = retained.get("unifiedFeatures")
    if features is None:
        faults.append("native.universe-retained-input-missing:unifiedFeatures")
    else:
        validate_native("UnifiedFeaturesV1", features)
        if unified_features_identity(features) != universe["unifiedFeaturesId"]:
            faults.append("native.universe-retained-input-identity-mismatch:unifiedFeaturesId")
        # 3.4: computed with --filter-platform <target> by the selected resolver.
        if features["targetTriple"] != context["targetTriple"]:
            faults.append("native.universe-retained-input-mismatch:unifiedFeatures.targetTriple")
        if features["resolverVersion"] != context["resolverVersion"]:
            faults.append("native.universe-retained-input-mismatch:unifiedFeatures.resolverVersion")

    prepared = retained.get("preparedOutputSet")
    if universe["preparedOutputSetId"] is None:
        # Optional absent preparation stays absent: a retained prepared set that no universe selected
        # must not enter the resolution by being in custody.
        if prepared is not None:
            faults.append("native.universe-retained-input-unselected:preparedOutputSet")
    elif prepared is None:
        faults.append("native.universe-retained-input-missing:preparedOutputSet")
    else:
        validate_native("PreparedOutputSetV3", prepared)
        if prepared_output_set_identity(prepared) != universe["preparedOutputSetId"]:
            faults.append("native.universe-retained-input-identity-mismatch:preparedOutputSetId")
        preparation = prepared["preparation"]
        if preparation["dependencySourceSetId"] != universe["dependencySourceSetId"]:
            faults.append("native.universe-retained-input-mismatch:preparedOutputSet.dependencySourceSetId")
        if not C.equal_typed(preparation["toolchain"], context["toolchain"]):
            faults.append("native.universe-retained-input-mismatch:preparedOutputSet.toolchain")
        if preparation["cfgSetId"] not in {row["cfgSetId"] for row in universe["cfgSets"]}:
            faults.append("native.universe-retained-input-mismatch:preparedOutputSet.cfgSetId")
        expected = "imported-inert" if preparation["kind"] == "imported-descriptor" else "host-prepared"
        if universe["preparedResolution"] != expected:
            faults.append("native.universe-retained-input-mismatch:preparedResolution")

    # Source correspondence: the analysed snapshot must actually contain what the universe names.
    lock = universe["lockfileIdentity"]
    row = inventory.get(lock["path"])
    if row is None or row["sha256"] != lock["contentSha256"]:
        faults.append("native.universe-source-mismatch:" + lock["path"])
    for path in universe["crateRootPaths"]:
        if path not in inventory:
            faults.append("native.universe-path-not-inventoried:" + path)
    for path in context["configProjection"]["replacedSnapshotConfigs"]:
        if path not in inventory:
            faults.append("native.native-context-path-not-inventoried:" + path)
    return sorted(set(faults))


def bind_rust_universe(universe: dict, admission: dict, context: dict,
                       retained: dict | None = None, snapshot_inventory: list[dict] | None = None) -> dict:
    """Bind a rust-v2 universe to its admitted context, before PlanId. The exact counterpart of
    bind_typescript_universe, and required by the same reasoning.

    `context`, `retained` and `snapshot_inventory` are all REQUIRED: there is no context-free or
    input-free admit path, because an optional join is not a rule. Omission is a typed refusal, never
    an ADMIT. Nothing here executes cargo, rustc, a build script, a proc macro or a filesystem read:
    every input is a retained descriptor or an explicitly trusted observation.
    """
    validate_native("RustUniverseV2ResolvedInputs", universe)
    refusals = list(admission["refusals"])
    if admission["language"] != "rust" or admission["domain"] != NATIVE_CONTEXT_DOMAINS["rust"]:
        refusals.append("native.native-context-language-mismatch:rust-universe-bound-to-" + admission["domain"])
    if universe["nativeContextId"] != admission["nativeContextId"]:
        refusals.append("native.universe-context-binding-mismatch")
    if context is None:
        refusals.append("native.universe-context-not-supplied")
    elif native_identity(NATIVE_CONTEXT_DOMAINS["rust"], "NativeContextV2", context) != admission["nativeContextId"]:
        refusals.append("native.universe-context-binding-mismatch:context-bytes-are-not-the-admitted-ones")
    else:
        refusals.extend(rust_universe_context_field_faults(universe, context))
        if retained is None or snapshot_inventory is None:
            refusals.append("native.universe-retained-inputs-not-supplied")
        else:
            refusals.extend(rust_universe_retained_input_faults(universe, context, retained, snapshot_inventory))
    universe_id = native_identity(NATIVE_UNIVERSE_DOMAINS["rust"], "RustUniverseV2ResolvedInputs", universe)
    return {"result": "REFUSE" if refusals else "ADMIT", "refusals": sorted(set(refusals)),
            "universeId": universe_id, "sourceUniverse": universe_id.removeprefix("sha256:"),
            "nativeContextId": universe["nativeContextId"]}


def verify_native_context(language: str, host_admission: dict, worker_descriptor: dict,
                          closure_trees: dict[str, dict]) -> dict:
    """Section 9.5: the worker recomputes the context after the sealed inputs arrive. Any differing byte is
    `Unavailable(native-context-mismatch)` BEFORE Analyze, for TypeScript exactly as for Rust."""
    worker = admit_native_context(language, worker_descriptor, closure_trees)
    equal = (not worker["refusals"] and not host_admission["refusals"]
             and worker["nativeContextId"] == host_admission["nativeContextId"])
    return {"nativeContextId": host_admission["nativeContextId"],
            "recomputedNativeContextId": worker["nativeContextId"], "equal": equal,
            "frame": "NativeContextVerified" if equal else "Unavailable",
            "unavailableReason": None if equal else "native-context-mismatch"}


def plan_native_context_digests(admissions: list[dict]) -> list[str]:
    """foundation `plan.nativeContextDigests` carries the BARE 64 hex of every selected universe's context
    (blind consumer A-2: the `sha256:` prefix is the native record spelling, not the Plan spelling).

    The Plan field is a canonical SET, and several units of one language legitimately share one context
    (same compiler closure, same stdlib, same effective options), so identical admitted contexts collapse
    to one member. That is deduplication of an identical descriptor, never of two different ones.
    """
    for a in admissions:
        if a["refusals"]:
            raise AdmissionError("NATIVE_CONTEXT_NOT_ADMITTED:" + a["refusals"][0])
    return sorted({a["planNativeContextDigest"] for a in admissions})


def classify_edges(observations: list[dict], resolvable_targets: set[str], node_modules_in_read_set: bool = True) -> dict:
    """TRUSTED OBSERVATION INPUT: closed syntactic observation forms -> resolved edge or unresolved-edge fact."""
    resolved: list[dict] = []; unresolved: list[dict] = []
    for ob in observations:
        form, referrer = ob["form"], ob["referrer"]

        def unres(relation: str, kind: str, scope: str, detail: str, module: str | None = None) -> None:
            row = {"referrer": referrer, "relation": relation, "edgeKind": kind, "targetScope": scope, "detail": detail[:512]}
            if module is not None:
                row["targetModule"] = module
            unresolved.append(row)

        if form in ("import-static", "export-from", "require-literal", "dynamic-import-literal"):
            spec = ob["specifier"]
            if ob.get("resolvedPath") in resolvable_targets and (spec.startswith(".") or node_modules_in_read_set):
                resolved.append({"referrer": referrer, "relation": "imports", "resolvedTarget": ob["resolvedPath"]})
            else:
                unres("imports", "unresolved-module-specifier", "module" if spec.startswith(".") else ("external" if not node_modules_in_read_set else "unknown"), spec)
        elif form == "require-nonliteral":
            unres("imports", "require-nonliteral", "unknown", ob.get("detail", "require(<expr>)"))
        elif form == "dynamic-import-nonliteral":
            unres("imports", "dynamic-import-nonliteral", "unknown", ob.get("detail", "import(<expr>)"))
        elif form == "member-access":
            if ob.get("computed"):
                unres("references", "computed-member-access", "module" if ob.get("baseIsNamespaceImport") else "unknown", ob.get("detail", "m[k]"), ob.get("namespaceModule"))
            else:
                resolved.append({"referrer": referrer, "relation": "references", "resolvedBinding": ob["binding"]})
        elif form == "identifier-reference":
            resolved.append({"referrer": referrer, "relation": "references", "resolvedBinding": ob["binding"]})
        elif form == "call":
            d = ob.get("dispatch")
            if ob.get("calleeType") == "any":
                unres("calls", "untyped-any-call", "unknown", ob.get("detail", "any()"))
            elif d == "structural":
                unres("calls", "structural-dispatch", "universe", ob.get("detail", "iface.method()"))
            elif d == "dyn-trait":
                unres("calls", "trait-object-dynamic-dispatch", "universe", ob.get("detail", "dyn Trait::method()"))
            elif d == "generic-bound":
                unres("calls", "generic-bound-dispatch", "universe", ob.get("detail", "T::method()"))
            else:
                resolved.append({"referrer": referrer, "relation": "calls", "resolvedCallee": ob["callee"]})
        elif form == "indirect-eval":
            unres("references", "indirect-eval", "unknown", ob.get("detail", "eval"))
        elif form == "reflective-access":
            unres("references", "reflective-access", "unknown", ob.get("detail", "Reflect"))
        elif form == "proc-macro-invocation":
            unres("references", "macro-expansion-unavailable", "universe", ob.get("detail", "#[derive(..)]"))
        elif form == "build-script-owner":
            unres("types", "build-script-generated-unavailable", "universe", ob.get("detail", "build.rs"))
        elif form == "cfg-excluded-item":
            unres("references", "cfg-excluded-region", "module", ob.get("detail", "#[cfg(...)]"))
        elif form == "ffi-extern":
            unres("calls", "ffi-extern", "external", ob.get("detail", "extern \"C\""))
        elif form == "cross-unit-import":
            unres("imports", "external-module-boundary", "external", ob.get("detail", "cross-unit"))
        else:
            raise AdmissionError(f"unknown observation form {form}")
    for u in unresolved:
        if u["edgeKind"] not in UNRESOLVED_EDGE_KINDS:
            raise AdmissionError("edge kind outside closed enum")
    return {"resolved": resolved, "unresolved": unresolved}


# ---------------------------------------------------------------------------
# Clone modes (feedback 9): same-language facts; cross-TS/JS candidate under a named projection
# ---------------------------------------------------------------------------

CLONE_PARAMS = {"minOccurrences": 2, "minBodyBytes": 64, "minTokens": 20, "nearMinTokens": 50,
                "nearThresholdMillionths": 800000, "maxCandidatesPerGroup": 4096, "maxGroupsPerUniverse": 1000000}
TS_DIRECTIVE_RE = re.compile(r"^(['\"](use strict|use client|use server)['\"]|///\s*<reference|//\s*@ts-)")
# tsjs-erasure-v1: type-only token kinds removed by the projection; runtime-significant TS tokens exclude a body.
TSJS_ERASED_KINDS = {"type-annotation", "type-declaration", "type-params", "as-assertion", "satisfies", "non-null",
                     "declare-modifier", "access-modifier", "implements-clause", "readonly-modifier", "abstract-modifier",
                     "definite-assignment", "import-type", "export-type"}
TSJS_RUNTIME_SIGNIFICANT = {"enum", "parameter-property", "namespace-value", "decorator", "const-enum", "import-equals"}


def _is_directive(language: str, value: str) -> bool:
    if language in ("typescript", "javascript"):
        return bool(TS_DIRECTIVE_RE.match(value))
    return language == "rust" and (value.startswith("///") or value.startswith("//!"))


def normalize_tokens(language: str, tokens: list[dict], level: str) -> tuple:
    out: list[tuple] = []; renames: dict[str, str] = {}
    for tok in tokens:
        kind, value = tok["kind"], tok["value"]
        if kind == "comment":
            if level in ("L2-comment-insensitive", "L3-identifier-insensitive") and not _is_directive(language, value):
                continue
            out.append(("comment", value)); continue
        if kind == "ident-local" and level == "L3-identifier-insensitive":
            renames.setdefault(value, f"$L{len(renames)}"); out.append(("ident-local", renames[value])); continue
        out.append((kind, value))
    return tuple(out)


def tsjs_projection(language: str, tokens: list[dict]) -> dict:
    """tsjs-erasure-v1: deterministic syntax projection. Removes type-only tokens; refuses (excludes the
    body) when a runtime-significant TypeScript token is present. Never a semantic-equivalence claim."""
    if language not in ("typescript", "javascript"):
        raise AdmissionError("tsjs projection is TypeScript/JavaScript only")
    significant = sorted({t["kind"] for t in tokens if t["kind"] in TSJS_RUNTIME_SIGNIFICANT})
    if significant:
        return {"projected": None, "excluded": True, "reason": "runtime-significant-ts-tokens", "tokens": significant, "projectionId": "tsjs-erasure-v1"}
    projected = [t for t in tokens if t["kind"] not in TSJS_ERASED_KINDS]
    return {"projected": projected, "excluded": False, "reason": None, "tokens": [], "projectionId": "tsjs-erasure-v1"}


def clone_groups(mode: str, bodies: list[dict], level: str | None = None, params: dict = CLONE_PARAMS) -> list[dict]:
    """bodies (TRUSTED OBSERVATION INPUT): [{id, language, bytes?, tokens?}]. Returns CloneCandidateGroupV2 rows."""
    groups: list[dict] = []
    if mode == "exact":
        # §6.3 (review v2 item 5): an IMPORT-ONLY body (a declaration span consisting solely of import/use/
        # extern-crate/top-level require statements, module headers, shebang, license header, inner attributes,
        # declare-only declarations) is excluded as a CANDIDATE. A body that is kept is hashed over its exact
        # verbatim bytes: internal use/import/directive bytes are never stripped or rewritten.
        buckets: dict = {}
        for b in bodies:
            if b.get("importOnly"):
                continue
            raw = b["bytes"].encode("utf-8")
            if len(raw) >= params["minBodyBytes"]:
                buckets.setdefault((b["language"], raw), []).append(b["id"])
        for (lang, raw), members in buckets.items():
            if len(members) >= params["minOccurrences"]:
                groups.append({"mode": "exact", "evidenceLevel": "byte-identical", "language": lang, "members": sorted(members), "authority": "fact",
                               "bodyBytesSha256": raw_sha256(raw)})
    elif mode in ("normalized", "structural"):
        lvl = level or ("L1-lexical" if mode == "normalized" else "L3-identifier-insensitive")
        if mode == "normalized" and lvl not in ("L1-lexical", "L2-comment-insensitive"):
            raise AdmissionError("normalized mode is L1 or L2")
        if mode == "structural" and lvl != "L3-identifier-insensitive":
            raise AdmissionError("structural mode is L3")
        evidence = {"L1-lexical": "lexically-identical", "L2-comment-insensitive": "comment-insensitive-identical", "L3-identifier-insensitive": "identifier-insensitive-identical"}[lvl]
        buckets = {}
        for b in bodies:
            if b.get("importOnly"):
                continue
            stream = normalize_tokens(b["language"], b["tokens"], lvl)
            if len([t for t in stream if t[0] != "comment"]) >= params["minTokens"]:
                buckets.setdefault((b["language"], stream), []).append(b["id"])
        for (lang, _), members in buckets.items():
            if len(members) >= params["minOccurrences"]:
                groups.append({"mode": mode, "evidenceLevel": evidence, "language": lang, "members": sorted(members), "authority": "fact"})
    elif mode == "cross-tsjs":
        buckets = {}; excluded: list[dict] = []
        for b in bodies:
            if b["language"] not in ("typescript", "javascript"):
                continue
            proj = tsjs_projection(b["language"], b["tokens"])
            if proj["excluded"]:
                excluded.append({"id": b["id"], "reason": proj["reason"], "tokens": proj["tokens"]}); continue
            stream = normalize_tokens(b["language"], proj["projected"], "L3-identifier-insensitive")
            if len([t for t in stream if t[0] != "comment"]) >= params["minTokens"]:
                buckets.setdefault(stream, []).append((b["id"], b["language"]))
        for _, members in buckets.items():
            langs = sorted({m[1] for m in members})
            if len(members) >= params["minOccurrences"] and len(langs) == 2:
                groups.append({"mode": "cross-tsjs", "evidenceLevel": "cross-language-syntax-candidate", "language": "typescript+javascript",
                               "projectionId": "tsjs-erasure-v1", "members": sorted(m[0] for m in members), "authority": "candidate-only",
                               "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False})
        for e in sorted(excluded, key=lambda e: e["id"]):
            groups.append({"mode": "cross-tsjs", "evidenceLevel": "excluded", "language": "typescript", "projectionId": "tsjs-erasure-v1",
                           "members": [e["id"]], "authority": "candidate-only", "excludedReason": e["reason"], "excludedTokens": e["tokens"],
                           "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False})
    elif mode == "near":
        shingled = []
        for b in bodies:
            if b.get('importOnly'):
                continue
            stream = [t for t in normalize_tokens(b["language"], b["tokens"], "L3-identifier-insensitive") if t[0] != "comment"]
            if len(stream) >= params["nearMinTokens"]:
                shingled.append((b["id"], b["language"], {tuple(stream[i:i + 5]) for i in range(len(stream) - 4)}))
        parent = {s[0]: s[0] for s in shingled}; sims: dict[str, int] = {}; edges = []

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for i in range(len(shingled)):
            for j in range(i + 1, len(shingled)):
                a, b_ = shingled[i], shingled[j]
                if a[1] != b_[1]:
                    continue
                inter, union = len(a[2] & b_[2]), len(a[2] | b_[2])
                jac = (inter * 1000000) // union if union else 0
                if jac >= params["nearThresholdMillionths"]:
                    left, right = sorted((a[0], b_[0]))
                    edges.append({'left': left, 'right': right, 'similarityMillionths': jac})
                    parent[find(a[0])] = find(b_[0]); sims[a[0]] = max(sims.get(a[0], 0), jac); sims[b_[0]] = max(sims.get(b_[0], 0), jac)
        comps: dict[str, list[str]] = {}
        for ident, _, _ in shingled:
            comps.setdefault(find(ident), []).append(ident)
        for root, members in comps.items():
            if len(members) >= params["minOccurrences"]:
                lang = next(s[1] for s in shingled if s[0] == root)
                groups.append({"mode": "near", "evidenceLevel": "similar-candidate", "language": lang, "members": sorted(members),
                               "authority": "candidate-only", "similarityMillionths": min(sims[m] for m in members),
                               "matchedEdges": sorted([e for e in edges if e['left'] in members and e['right'] in members], key=lambda e: (e['left'], e['right'])),
                               "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor"})
    else:
        raise AdmissionError(f"unknown clone mode {mode}")
    groups.sort(key=lambda g: (g["language"], g["members"]))
    return groups


# ---------------------------------------------------------------------------
# Framework recognition (§8) — literal manifests only
# ---------------------------------------------------------------------------

FRAMEWORK_HINTS = ["angular", "@angular/core", "svelte", "nuxt", "@remix-run/react", "astro", "solid-js", "vue", "ember-source", "gatsby", "@nestjs/core"]


def recognize_frameworks(files: dict[str, str]) -> dict:
    recognized: list[dict] = []; hints: list[dict] = []

    def ev(path: str, field: str) -> dict:
        return {"path": path, "contentSha256": raw_sha256(files[path].encode("utf-8")), "field": field}

    def effects(entry=None, tests=None, ignore=None) -> dict:
        return {"entryPoints": entry or [], "testGlobs": tests or [], "ignoreConventions": ignore or []}

    pkg = None
    if "package.json" in files:
        try:
            pkg = C.parse(files["package.json"].encode("utf-8"))
        except AdmissionError:
            recognized.append({"recognizerId": "node-package", "recognizerVersion": 1, "evidence": [ev("package.json", "<unparseable>")], "assurance": "inferred",
                               "effects": effects(ignore=["node_modules/"]), "unresolvedChoices": ["package.json-not-strict-json"]})
    if isinstance(pkg, dict):
        recognized.append({"recognizerId": "node-package", "recognizerVersion": 1, "evidence": [ev("package.json", "type/private/exports/main")], "assurance": "declared",
                           "effects": effects(ignore=["node_modules/"]), "unresolvedChoices": []})
        if isinstance(pkg.get("workspaces"), (list, dict)):
            recognized.append({"recognizerId": "npm-workspaces", "recognizerVersion": 1, "evidence": [ev("package.json", "workspaces")], "assurance": "declared", "effects": effects(), "unresolvedChoices": []})
        cfgs = [p for p in ("jest.config.ts", "jest.config.js", "vitest.config.ts", "vitest.config.js") if p in files]
        if "jest" in pkg or cfgs:
            path = cfgs[0] if cfgs else "package.json"
            recognized.append({"recognizerId": "vitest-jest", "recognizerVersion": 1, "evidence": [ev(path, "jest|vitest")], "assurance": "declared",
                               "effects": effects(tests=["**/*.test.*", "**/*.spec.*", "**/__tests__/**"]), "unresolvedChoices": [] if path == "package.json" else ["config-requires-evaluation"]})
        deps: dict = {}
        for k in ("dependencies", "devDependencies", "peerDependencies"):
            if isinstance(pkg.get(k), dict):
                deps.update(pkg[k])
        hints = [{"dependencyName": n} for n in sorted(deps) if n in FRAMEWORK_HINTS]
    for cfg in ("tsconfig.json", "jsconfig.json"):
        if cfg in files:
            recognized.append({"recognizerId": "typescript-config", "recognizerVersion": 1, "evidence": [ev(cfg, "compilerOptions/extends/references")], "assurance": "declared", "effects": effects(), "unresolvedChoices": []}); break
    if "pnpm-workspace.yaml" in files:
        recognized.append({"recognizerId": "pnpm-workspace", "recognizerVersion": 1, "evidence": [ev("pnpm-workspace.yaml", "packages")], "assurance": "declared", "effects": effects(), "unresolvedChoices": []})
    if "Cargo.toml" in files:
        text = files["Cargo.toml"]
        if re.search(r"^\[workspace\]", text, re.M):
            recognized.append({"recognizerId": "cargo-workspace", "recognizerVersion": 1, "evidence": [ev("Cargo.toml", "workspace.members")], "assurance": "declared", "effects": effects(ignore=["target/"]), "unresolvedChoices": []})
        if re.search(r"^\[package\]", text, re.M):
            entry = [p for p in ("src/main.rs", "src/lib.rs") if p in files]
            recognized.append({"recognizerId": "cargo-package", "recognizerVersion": 1, "evidence": [ev("Cargo.toml", "package/lib/bin")], "assurance": "declared", "effects": effects(entry=entry, ignore=["target/"]), "unresolvedChoices": []})
    next_cfg = next((p for p in ("next.config.js", "next.config.mjs", "next.config.ts") if p in files), None)
    if next_cfg:
        routes = sorted(p for p in files if (p.startswith("app/") and p.endswith(("page.tsx", "page.jsx", "page.ts", "page.js", "route.ts", "route.js"))) or (p.startswith("pages/") and p.endswith((".tsx", ".jsx", ".ts", ".js"))))
        recognized.append({"recognizerId": "nextjs", "recognizerVersion": 1, "evidence": [ev(next_cfg, "presence")], "assurance": "inferred", "effects": effects(entry=routes, ignore=[".next/"]), "unresolvedChoices": ["config-requires-evaluation"]})
    vite_cfg = next((p for p in ("vite.config.ts", "vite.config.js", "vite.config.mjs") if p in files), None)
    if vite_cfg:
        recognized.append({"recognizerId": "vite", "recognizerVersion": 1, "evidence": [ev(vite_cfg, "presence")], "assurance": "inferred", "effects": effects(entry=["index.html"] if "index.html" in files else [], ignore=["dist/"]), "unresolvedChoices": ["config-requires-evaluation"]})
    recognized.sort(key=lambda r: r["recognizerId"])
    if len(recognized) > 32:
        raise AdmissionError("maxRecognizersPerUnit exceeded")
    entry_state = "all" if any(r["effects"]["entryPoints"] for r in recognized) and not any(r["unresolvedChoices"] for r in recognized) else ("partial" if any(r["effects"]["entryPoints"] for r in recognized) else "none")
    return {"schemaVersion": 1, "recognized": recognized, "observedHints": hints, "entryPoints": {"state": entry_state, "source": "recognized" if entry_state != "none" else "none"}}


# ---------------------------------------------------------------------------
# D9 mapping and workspace units
# ---------------------------------------------------------------------------

# Review v2 item 7: EXISTING D9 codes only. The native deficiency and nativeCause travel as typed detail inside the
# coverage2 record that the termination names by coverageId (CoverageResultV3.entry.deficiency / nativeCause).
# No successor codes, no competing codes, no enum change anywhere.
_TYPED_DETAIL = "coverage2 record (CoverageResultV3.entry.deficiency + nativeCause) named by the termination's coverageId"
D9_MAP: dict[str, dict] = {
    "input-closure-incomplete": {"class": "indeterminate", "exitCode": 3, "code": "VERDICT.INDETERMINATE", "successorCode": None, "interim": False, "typedDetailCarrier": _TYPED_DETAIL},
    "resolution-incomplete": {"class": "indeterminate", "exitCode": 3, "code": "VERDICT.INDETERMINATE", "successorCode": None, "interim": False, "typedDetailCarrier": _TYPED_DETAIL},
    "external-consumers-unknown": {"class": "indeterminate", "exitCode": 3, "code": "VERDICT.INDETERMINATE", "successorCode": None, "interim": False, "typedDetailCarrier": _TYPED_DETAIL},
    "derivation-policy-unmet": {"class": "indeterminate", "exitCode": 3, "code": "VERDICT.INDETERMINATE", "successorCode": None, "interim": False, "typedDetailCarrier": _TYPED_DETAIL},
    "provider-unavailable/capability-missing": {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.PROVIDER_UNAVAILABLE", "successorCode": None, "interim": False, "typedDetailCarrier": _TYPED_DETAIL},
    "budget-exhausted": {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.BUDGET_EXHAUSTED", "successorCode": None, "interim": False, "typedDetailCarrier": _TYPED_DETAIL},
    "native.stale-prepared-output": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.prepared-output-not-inert": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.stale-import": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.execution-not-authorized": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.capability-mismatch-hello-ack": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION", "successorCode": None, "interim": False, "typedDetailCarrier": "operational record"},
    "native.coverage-bijection-mismatch": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION", "successorCode": None, "interim": False, "typedDetailCarrier": "operational record"},
    "native.identity-not-negotiated": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION", "successorCode": None, "interim": False, "typedDetailCarrier": "operational record"},
    "native.worker-fault": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION", "successorCode": None, "interim": False, "typedDetailCarrier": "operational record"},
    "native.prepare-bound-exceeded": {"class": "operational-failed", "exitCode": 4, "code": "HOST.IO_FAILURE", "successorCode": None, "interim": False, "typedDetailCarrier": "operational record"},
    "native.ambient-cargo-config": {"class": "operational-failed", "exitCode": 4, "code": "HOST.IO_FAILURE", "successorCode": None, "interim": False, "typedDetailCarrier": "operational record"},
    "PROJECT.SCOPE_LIMIT": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.UNSATISFIABLE", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.too-many-units": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.UNSATISFIABLE", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.explicit-root-without-marker": {"class": "request-rejected", "exitCode": 2, "code": "CONFIG.INVALID", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.explicit-root-grammar": {"class": "request-rejected", "exitCode": 2, "code": "CONFIG.INVALID", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    # P3: an explicit root at or below an admitted nested repository / nested project / custody-excluded directory names
    # another project's source (security refuses the same join as JOIN_CROSSES_NESTED_*); the boundary inventory a host
    # passes must have been produced by the security instrument over the same marker inventory (pruned trees agree).
    "native.explicit-root-crosses-boundary": {"class": "request-rejected", "exitCode": 2, "code": "CONFIG.INVALID", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.boundary-inventory-mismatch": {"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED", "successorCode": None, "interim": False, "typedDetailCarrier": "request rejection detail"},
    "native.framework-unrecognized": {"class": "none", "exitCode": None, "code": None, "successorCode": None, "interim": False, "typedDetailCarrier": "disclosure"},
}
EXISTING_D9_CODES = {"COVERAGE.PROVIDER_UNAVAILABLE", "COVERAGE.LANGUAGE_TIER_UNSUPPORTED", "COVERAGE.REQUIRED_RELATION_MISSING",
                     "COVERAGE.BUDGET_EXHAUSTED", "VERDICT.INDETERMINATE", "COVERAGE.CONFIDENCE_FLOOR_UNMET", "HOST.IO_FAILURE",
                     "PROVIDER.PROTOCOL_VIOLATION", "REQUEST.PRECONDITION_FAILED", "REQUEST.UNSATISFIABLE", "CONFIG.INVALID"}
CLASS_TO_EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}


def d9_map(detail: str) -> dict:
    row = D9_MAP.get(detail)
    if row is None:
        raise AdmissionError(f"no D9 mapping for {detail}; silent exit 0 is forbidden")
    if row["code"] is not None and row["code"] not in EXISTING_D9_CODES:
        raise AdmissionError("code must be an existing D9 code")
    if row["successorCode"] is not None or row["interim"]:
        raise AdmissionError("no successor or interim codes exist in this contract")
    return {"detail": detail, **row}


def d9_successor_codes() -> list[str]:
    return sorted(r["successorCode"] for r in D9_MAP.values() if r["successorCode"] is not None)


# ---------------------------------------------------------------------------
# Fault law (review v2 item 7): worker diagnostics never mint facts or a Run
# ---------------------------------------------------------------------------

def stage_authority(terminal_kind: str, inputs_admitted: bool = True) -> dict:
    """Inherited D9 fault law applied to a native stage. A worker that faults (process fault, protocol violation,
    ProviderFault frame, crash) contributes NO facts, NO Coverage entries and NO Run: its diagnostics are an
    operational record only, D9 operational-failed 4 PROVIDER.PROTOCOL_VIOLATION. A stage that terminates
    cleanly over successfully admitted but INCOMPLETE inputs (missing crate, generated file unavailable, unresolved
    edges) yields admitted facts and typed Coverage, seals an authoritative Run, and terminates indeterminate 3
    (VERDICT.INDETERMINATE with the deficiency as typed detail in the coverage2 record)."""
    if not inputs_admitted:
        raise AdmissionError("stage cannot start on inputs that were not admitted")
    if terminal_kind in ("provider-fault", "crash", "fault"):
        out = {"terminalKind": terminal_kind, "factsAdmitted": "none", "coverageEntriesAdmitted": False, "runMayBeSealed": False,
               "authority": "none", "diagnosticsCarrier": "operational-record-only",
               "d9": {"class": "operational-failed", "exitCode": 4, "code": "PROVIDER.PROTOCOL_VIOLATION"}}
    elif terminal_kind == "cancelled":
        out = {"terminalKind": terminal_kind, "factsAdmitted": "none", "coverageEntriesAdmitted": False, "runMayBeSealed": False,
               "authority": "none", "diagnosticsCarrier": "operational-record-only",
               "d9": {"class": "interrupted", "exitCode": 130, "code": None}}
    elif terminal_kind == "budget-exhausted":
        out = {"terminalKind": terminal_kind, "factsAdmitted": "before-terminal", "coverageEntriesAdmitted": True, "runMayBeSealed": True,
               "authority": "authoritative", "diagnosticsCarrier": "operational-record-only",
               "d9": {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.BUDGET_EXHAUSTED"}}
    elif terminal_kind == "unavailable":
        out = {"terminalKind": terminal_kind, "factsAdmitted": "before-terminal", "coverageEntriesAdmitted": True, "runMayBeSealed": True,
               "authority": "authoritative", "diagnosticsCarrier": "operational-record-only",
               "d9": {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.PROVIDER_UNAVAILABLE"}}
    elif terminal_kind == "complete":
        out = {"terminalKind": terminal_kind, "factsAdmitted": "all", "coverageEntriesAdmitted": True, "runMayBeSealed": True,
               "authority": "authoritative", "diagnosticsCarrier": "operational-record-only",
               "d9": {"class": "success", "exitCode": 0, "code": None}}
    else:
        raise AdmissionError("unknown terminal kind")
    validate_native("StageAuthorityV1", out)
    return out


def run_termination(stage: dict, coverage_entries: list[dict]) -> dict:
    """Combine stage authority with typed Coverage: any admitted entry carrying a deficiency makes an authoritative
    Run terminate indeterminate 3 (deficiency carried in the coverage2 record), never a fault and never exit 0."""
    if stage["authority"] == "none":
        return {"authority": "none", "runSealed": False, "factsMinted": 0, "d9": stage["d9"], "typedDetail": None}
    deficient = [e for e in coverage_entries if e.get("deficiency")]
    if stage["d9"]["class"] == "success" and deficient:
        worst = min((e["deficiency"] for e in deficient), key=PRECEDENCE_V2.index)
        d9 = {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.PROVIDER_UNAVAILABLE" if worst == "provider-unavailable" else "VERDICT.INDETERMINATE"}
        return {"authority": "authoritative", "runSealed": True, "factsMinted": len(coverage_entries), "d9": d9,
                "typedDetail": {"carrier": _TYPED_DETAIL, "deficiency": worst, "nativeCauses": sorted({e.get("nativeCause") for e in deficient if e.get("nativeCause")})}}
    return {"authority": "authoritative", "runSealed": True, "factsMinted": len(coverage_entries), "d9": stage["d9"],
            "typedDetail": None if not deficient else {"carrier": _TYPED_DETAIL, "deficiency": min((e["deficiency"] for e in deficient), key=PRECEDENCE_V2.index), "nativeCauses": []}}


# ---------------------------------------------------------------------------
# Workspace units v2 (review v2 item 1): per-language program-membership units, co-located roots
# ---------------------------------------------------------------------------

RUST_EXT = (".rs",)
FAMILY_MARKERS = {"rust": ["Cargo.toml"], "tsjs": ["tsconfig.json", "jsconfig.json", "package.json"]}
# Host ignore conventions are the shared discovery rule's pruned trees (../discovery-defaults.py): dependency trees
# (node_modules), VCS trees (.git/.hg/.svn/.jj) and Cargo build output (`target` directly under a Cargo.toml directory),
# matched by exact path segment. `packages/target/index.ts` and `src/target/x.ts` are ordinary program members.
HOST_IGNORE_SEGMENTS = DD.DEPENDENCY_TREE_SEGMENTS + DD.VCS_TREE_SEGMENTS
MAX_WORKSPACE_UNITS = DD.MAX_WORKSPACE_UNITS
BUNDLED_GRAMMARS = {".rs": "rust", ".ts": "typescript", ".tsx": "typescript", ".mts": "typescript", ".cts": "typescript",
                    ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript", ".jsx": "javascript",
                    ".json": "json", ".toml": "toml", ".md": "markdown", ".yaml": "yaml", ".yml": "yaml"}


def _family_of(path: str) -> str:
    if path.endswith(RUST_EXT):
        return "rust"
    if path.endswith(JS_EXT + TS_EXT):
        return "tsjs"
    return "none"


def _ext(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    return name[name.rfind("."):] if "." in name else ""


NO_BOUNDARY_DISCLOSURE = ("no admitted boundary inventory: standalone pure instrument over a marker inventory; nested "
                          "repositories, nested projects and custody exclusions are NOT decided here and this output is "
                          "not an operational host composition (native section 1.4 U-8)")
BOUNDARY_DISCLOSURE = ("boundaries admitted by the security discovery instrument (S3) over the same marker inventory; "
                       "units and memberships at or below a boundary are outside this project")


def _boundaries_out(boundaries: dict | None, excluded_units: list[dict]) -> dict:
    if boundaries is None:
        return {"source": "none", "nestedRepositories": [], "nestedProjects": [], "custodyExcludedUnits": [],
                "excludedUnits": [], "disclosure": NO_BOUNDARY_DISCLOSURE}
    return {"source": boundaries["source"], "nestedRepositories": list(boundaries["nestedRepositories"]),
            "nestedProjects": list(boundaries["nestedProjects"]), "custodyExcludedUnits": [dict(r) for r in boundaries["custodyExcludedUnits"]],
            "excludedUnits": excluded_units, "disclosure": BOUNDARY_DISCLOSURE}


def _boundary_hit(path: str, boundaries: dict | None, marker_name: str | None = None):
    """(anchor, reason) when `path` is outside the project under the admitted boundary inventory, else None."""
    if boundaries is None:
        return None
    hit = DD.classify_boundary(path, boundaries["nestedRepositories"], boundaries["nestedProjects"])
    if hit is not None:
        return hit
    return DD.classify_custody_exclusion(path, marker_name, boundaries["custodyExcludedUnits"])


def discover_units(markers: dict[str, dict], explicit_workspace_roots: list[str] | None = None,
                   boundaries: dict | None = None) -> dict:
    """markers (TRUSTED OBSERVATION INPUT): {markerPath: {sha256, isCargoWorkspace?, allowJs?}} — every marker file the
    snapshot inventory holds, installed dependencies included; the SHARED rule decides which ones are units.
    boundaries (TRUSTED ADMITTED INPUT, P3): the closed `AdmittedBoundaryInventoryV1` the host obtained from the
    security discovery instrument (`DD.boundary_inventory_from_provenance(S.discovery(...)['provenance'])`) over the
    SAME marker inventory: nested repositories, nested projects and custody-excluded unit directories, as relative
    scope paths. Units and marker directories at or below a boundary are excluded (`boundaries.excludedUnits`, one
    row per marker directory, reason nested-repository | nested-project | custody-excluded) and never folded into a
    Cargo workspace; an explicit root at or below one refuses `native.explicit-root-crosses-boundary` (CONFIG.INVALID),
    as security refuses JOIN_CROSSES_NESTED_REPOSITORY / JOIN_CROSSES_NESTED_PROJECT. The inventory's `prunedTrees`
    must equal the ones this instrument derives from the marker inventory (`native.boundary-inventory-mismatch`
    otherwise): a caller-supplied ignore list is never accepted as proof of boundary completeness. `boundaries=None`
    is the STANDALONE pure instrument (retained for fixtures and for callers that have no project): the output says
    so (`boundaries.source = "none"` with the disclosure) and an operational host composition must not use it.
    One unit per (directory, language family): a directory holding both Cargo.toml and package.json yields TWO
    co-located units (rust + tsjs) with the same rootPath. Within tsjs, marker precedence tsconfig > jsconfig >
    package.json selects the mode of the ONE tsjs unit at that directory; it never removes the rust unit.
    A Cargo.toml package inside a Cargo workspace root's tree is folded into the workspace unit as a member
    package (Cargo resolves the workspace as one program).
    Shared discovery rule (../discovery-defaults.py, MUST-3): markers inside dependency trees (node_modules), VCS trees
    and Cargo build output (`target` directly under a Cargo.toml directory) are pruned by exact path segment and
    reported once per tree in `prunedTrees`; they are never units and never count toward the cap. More than 4096
    first-party unit directories is the typed refusal `native.too-many-units` (REQUEST.UNSATISFIABLE), never truncation.
    Config2 discovery.workspaceRoots / CLI --workspace-root (explicit) are EXACT roots normalized by the shared
    `normalize_explicit_root` (`.` -> the project root ``; trailing `/` removed; grammar refusal is CONFIG.INVALID
    `native.explicit-root-grammar`); discovery is restricted to those roots with provenance EXPLICIT; an explicit root
    with no language marker is CONFIG.INVALID (native.explicit-root-without-marker), never silently dropped.
    Explicit roots are UNIT SELECTION, never loss of Cargo workspace semantics (P22): naming a Cargo workspace root
    explicitly keeps its member packages folded (`memberPackageRoots`) so their `target` output stays pruned; naming a
    member package alone selects that package as its own `cargo-package` unit."""
    if boundaries is not None:
        validate_native("AdmittedBoundaryInventoryV1", boundaries)
    enum = DD.enumerate_units(markers)
    pruned_trees = enum["prunedTrees"]

    def refused(detail: str, roots: list[str], **extra) -> dict:
        return {"units": [], "prunedTrees": pruned_trees, "boundaries": _boundaries_out(boundaries, []),
                "refused": {"detail": detail, "roots": roots, **extra, "d9": d9_map(detail)}}

    if boundaries is not None and boundaries["prunedTrees"] != pruned_trees:
        return refused("native.boundary-inventory-mismatch", [], expectedPrunedTrees=pruned_trees, inventoryPrunedTrees=boundaries["prunedTrees"])
    if enum["refusal"] is not None:
        return refused("native.too-many-units", [], unitCount=enum["refusal"]["unitCount"], limit=enum["refusal"]["limit"])
    cargo_roots = DD.cargo_roots_from_markers(markers)
    by_dir: dict[str, dict[str, dict]] = {}
    excluded_units: list[dict] = []
    for mp, info in sorted(markers.items(), key=lambda kv: kv[0].encode("utf-8")):
        if DD.classify_path(mp, cargo_roots) is not None:
            continue
        d, _, name = mp.rpartition("/")
        hit = _boundary_hit(d, boundaries, name)
        if hit is not None:
            excluded_units.append({"path": d, "marker": name, "reason": hit[1], "anchor": hit[0]})
            continue
        by_dir.setdefault(d, {})[name] = {**info, "markerPath": mp}
    excluded_units.sort(key=lambda r: (r["path"].encode("utf-8"), r["marker"]))
    if explicit_workspace_roots is not None:
        roots = []
        for spec in explicit_workspace_roots:
            try:
                roots.append(DD.normalize_explicit_root(spec))
            except DD.RootGrammarError:
                return refused("native.explicit-root-grammar", [spec if isinstance(spec, str) else repr(spec)])
        for r in roots:
            hit = _boundary_hit(r, boundaries)
            if hit is not None:
                return refused("native.explicit-root-crosses-boundary", [DD.spell_root(r)], anchor=hit[0], reason=hit[1])
        missing = sorted(r for r in roots if not by_dir.get(r))
        if missing:
            return refused("native.explicit-root-without-marker", [DD.spell_root(r) for r in missing])
        selected = set(roots)
        selected_workspaces = {d for d in selected if "Cargo.toml" in by_dir[d] and by_dir[d]["Cargo.toml"].get("isCargoWorkspace")}
        kept: dict[str, dict[str, dict]] = {}
        for d, m in by_dir.items():
            if d in selected:
                kept[d] = m
            elif "Cargo.toml" in m and any(w != d and _under_unit(d, w) for w in selected_workspaces):
                kept[d] = {"Cargo.toml": m["Cargo.toml"]}   # semantic member of a selected workspace: folded, never dropped (P22)
        by_dir = kept
    provenance = "EXPLICIT" if explicit_workspace_roots is not None else "DISCOVERED"
    cargo_ws_roots = sorted(d for d, m in by_dir.items() if "Cargo.toml" in m and m["Cargo.toml"].get("isCargoWorkspace"))
    units: list[dict] = []
    for d in sorted(by_dir, key=lambda x: (x.count("/") if x else -1, x)):
        m = by_dir[d]
        if "Cargo.toml" in m:
            enclosing = [w for w in cargo_ws_roots if w != d and _under_unit(d, w)]
            if enclosing:
                pass  # folded into the enclosing workspace unit below
            else:
                units.append({"rootPath": d, "languageFamily": "rust", "languageMode": "rust-cargo",
                              "unitKind": "cargo-workspace" if m["Cargo.toml"].get("isCargoWorkspace") else "cargo-package",
                              "markerPath": m["Cargo.toml"]["markerPath"], "markerSha256": m["Cargo.toml"]["sha256"],
                              "recognizerId": "cargo-workspace" if m["Cargo.toml"].get("isCargoWorkspace") else "cargo-package", "recognizerVersion": 1,
                              "provenance": provenance, "memberPackageRoots": []})
        for marker in FAMILY_MARKERS["tsjs"]:
            if marker in m:
                if marker == "tsconfig.json":
                    mode = "js-allowjs" if m[marker].get("allowJs") else "ts-tsconfig"
                elif marker == "jsconfig.json":
                    mode = "js-allowjs"
                else:
                    mode = "js-synthesized"
                units.append({"rootPath": d, "languageFamily": "tsjs", "languageMode": mode,
                              "unitKind": "ts-program" if mode == "ts-tsconfig" else "js-program",
                              "markerPath": m[marker]["markerPath"], "markerSha256": m[marker]["sha256"],
                              "recognizerId": "typescript-config" if marker != "package.json" else "node-package", "recognizerVersion": 1,
                              "provenance": provenance, "memberPackageRoots": []})
                break
    for d, m in by_dir.items():
        if "Cargo.toml" in m:
            enclosing = sorted((w for w in cargo_ws_roots if w != d and _under_unit(d, w)), key=len)
            if enclosing:
                ws = next(u for u in units if u["languageFamily"] == "rust" and u["rootPath"] == enclosing[-1])
                ws["memberPackageRoots"] = sorted(set(ws["memberPackageRoots"]) | {d})
    units.sort(key=lambda u: (u["rootPath"].encode("utf-8"), u["languageFamily"]))
    for i, u in enumerate(units):
        u["unitOrdinal"] = i
        validate_native("WorkspaceUnitV2", u)
    if len({u["rootPath"] for u in units}) > MAX_WORKSPACE_UNITS:   # unreachable after enumerate_units; kept as the stated bound
        return refused("native.too-many-units", [])
    out = {"units": units, "prunedTrees": pruned_trees, "boundaries": _boundaries_out(boundaries, excluded_units), "refused": None}
    validate_native("UnitDiscoveryV1", out)
    return out


def synthetic_marker_set(first_party: int, installed: int, root_marker: bool = True) -> dict:
    """FIXTURE GENERATOR (not a product function): a marker map with `first_party` directories `pkgNNNN/package.json`,
    `installed` manifests `node_modules/depNNNN/package.json` and optionally a root package.json. Lets the case file
    state the 4200-manifest cases (PR-MUST-3) without 25 000 literal lines; digests are constant placeholders."""
    markers = {"package.json": {"sha256": "b" * 64}} if root_marker else {}
    markers.update({"pkg%04d/package.json" % i: {"sha256": "1" * 64} for i in range(first_party)})
    markers.update({"node_modules/dep%04d/package.json" % i: {"sha256": "1" * 64} for i in range(installed)})
    return markers


def _cargo_roots_of_units(units: list[dict]) -> set[str]:
    """Cargo roots known to the membership step: every rust unit root and every folded member package root."""
    roots: set[str] = set()
    for u in units:
        if u["languageFamily"] == "rust":
            roots.add(u["rootPath"]); roots.update(u.get("memberPackageRoots", []))
    return roots


def assign_membership(units: list[dict], files: list[str], boundaries: dict | None = None) -> dict:
    """Deterministic file membership: a file belongs to the DEEPEST unit OF ITS OWN LANGUAGE FAMILY whose root
    prefixes it. Units of another family never claim or erase it. A source file of a family with no enclosing
    unit is syntax-only (cause no-program-unit). A file with no bundled grammar is listed as unsupported-file.
    Host ignore conventions are the SHARED pruned-tree rule applied by exact path segment (node_modules and VCS trees
    anywhere; Cargo `target` only directly under a Cargo root known from the units), never a substring match.
    Admitted boundaries (P3): a file at or below a nested repository / nested project / custody-excluded directory is
    `outside-project-boundary` (reason nested-repository | nested-project | custody-excluded) and listed in
    `outsideBoundaryFiles`: it is another project's source or uncustodied source, never scanned here and never a member
    of any unit of this project; the boundary test precedes the pruned-tree test.
    Every inventory file appears in exactly one row; erasedFiles is always empty (checked by schema maxItems 0)."""
    if boundaries is not None:
        validate_native("AdmittedBoundaryInventoryV1", boundaries)
    rows: list[dict] = []; unsupported: list[str] = []; outside: list[str] = []
    cargo_roots = _cargo_roots_of_units(units)
    for f in sorted(files, key=lambda x: x.encode("utf-8")):
        hit = _boundary_hit(f, boundaries)
        if hit is not None:
            rows.append({"path": f, "languageFamily": _family_of(f), "unitOrdinal": None, "membership": "outside-project-boundary", "reason": hit[1]}); outside.append(f); continue
        if DD.classify_path(f, cargo_roots) is not None:
            rows.append({"path": f, "languageFamily": _family_of(f), "unitOrdinal": None, "membership": "syntax-only", "reason": "host-ignore-convention"}); continue
        fam = _family_of(f)
        if fam == "none":
            if _ext(f) in BUNDLED_GRAMMARS:
                rows.append({"path": f, "languageFamily": "none", "unitOrdinal": None, "membership": "syntax-only", "reason": "grammar-only"})
            else:
                rows.append({"path": f, "languageFamily": "none", "unitOrdinal": None, "membership": "unsupported-file", "reason": "no-bundled-grammar"}); unsupported.append(f)
            continue
        candidates = [u for u in units if u["languageFamily"] == fam and _under_unit(f, u["rootPath"])]
        if not candidates:
            rows.append({"path": f, "languageFamily": fam, "unitOrdinal": None, "membership": "syntax-only", "reason": "no-program-unit-for-language"}); continue
        deepest = max(candidates, key=lambda u: (len(u["rootPath"]), -u["unitOrdinal"]))
        rows.append({"path": f, "languageFamily": fam, "unitOrdinal": deepest["unitOrdinal"], "membership": "program-member", "reason": "deepest-unit-in-language"})
    out = {"schemaVersion": 1, "units": units, "rows": rows, "unsupportedFiles": unsupported, "outsideBoundaryFiles": outside, "erasedFiles": []}
    validate_native("UnitMembershipV1", out)
    if sorted(r["path"] for r in rows) != sorted(files):
        raise AdmissionError("membership must cover every inventory file exactly once")
    return out


class ScopeRefusal(AdmissionError):
    """An admitted discovery population cannot fit the shared scope record; never truncate."""
    def __init__(self, field, count, limit):
        self.detail = 'PROJECT.SCOPE_LIMIT'
        self.subject = {'field': field, 'count': count, 'limit': limit}
        self.d9 = d9_map(self.detail)
        super().__init__(f'{self.detail}:{field}:{count}>{limit}')


def unit_scope_descriptor(units: list[dict], ignore_paths: list[str], explicit_path_prefixes: list[str] | None = None,
                          pruned_trees: list[dict] | None = None, boundaries: dict | None = None) -> dict:
    """Unit scopes feed the SHARED foundation scope-descriptor (identity-schemas.v2#/$defs/scope-descriptor):
    workspaceRoots = the unit roots (co-located units contribute one root), pathPrefixes = explicit prefixes or
    the roots, excludedPathPrefixes = Config2 ignorePaths, the anchors of the pruned trees discovery actually observed
    (`prunedTrees` from discover_units), the conventional anchors of the shared rule (`.git`/`node_modules` under
    every unit root; `target` under every Cargo root only) and, under an admitted boundary inventory (P3), every nested
    repository, nested project and directory-custody exclusion anchor (`DD.boundary_excluded_prefixes`). The segment
    rule itself applies in addition to these prefixes; the prefixes make the observed exclusions Plan-visible. The
    foundation record is closed, so the boundary provenance travels beside it (`boundaries`), not inside it."""
    if boundaries is not None:
        validate_native("AdmittedBoundaryInventoryV1", boundaries)
    roots = sorted({u["rootPath"] for u in units}, key=lambda x: x.encode("utf-8"))
    spelled = [DD.spell_root(r) for r in roots]  # the project root is spelled "." in the foundation record (Text minLength 1)
    conventional = DD.conventional_excluded_prefixes(roots, _cargo_roots_of_units(units))
    observed = [t["path"] for t in (pruned_trees or [])]
    boundary = DD.boundary_excluded_prefixes(boundaries) if boundaries is not None else []
    excluded = sorted({*(p.rstrip("/") for p in ignore_paths), *conventional, *observed, *boundary}, key=lambda x: x.encode("utf-8"))
    desc = {"schemaVersion": 2, "workspaceRoots": spelled, "pathPrefixes": sorted(set(explicit_path_prefixes or spelled), key=lambda x: x.encode("utf-8")),
            "excludedPathPrefixes": excluded}
    for field in ('workspaceRoots', 'pathPrefixes', 'excludedPathPrefixes'):
        limit = IM.SCHEMA['$defs']['scope-descriptor']['properties'][field]['maxItems']
        if len(desc[field]) > limit:
            raise ScopeRefusal(field, len(desc[field]), limit)
    validate_foundation("scope-descriptor", desc)
    disclosure = _boundaries_out(boundaries, [])
    return {"scopeDescriptor": desc, "scopeDigest": raw_sha256(C.canonical(desc)),
            "boundaries": {"source": disclosure["source"], "nestedRepositories": disclosure["nestedRepositories"],
                           "nestedProjects": disclosure["nestedProjects"], "custodyExcludedUnits": disclosure["custodyExcludedUnits"],
                           "excludedPathPrefixesFromBoundaries": boundary, "disclosure": disclosure["disclosure"]}}


def admit_release_capability_registry(registry: list[dict]) -> list[dict]:
    """The authenticated release declaration registry, admitted against its published authority.

    Its CONTENT is release-specific and stays an authenticated input - which rows a release ships is not a
    contract constant - but its schema, its membership authority, its canonical spelling and its binding to the
    Plan are normative, and this is where they bind. A row may declare a SUBSET of the matrix; it may never
    declare a member the matrix does not register, or a mode whose cell carries no promise."""
    validate_native("ReleaseCapabilityRegistryV1", registry)
    known = {c["id"] for c in CAPABILITY_MATRIX["capabilities"]}
    modes = set(CAPABILITY_MATRIX["languageModes"])
    not_selected = {(c["capability"], c["mode"]) for c in CAPABILITY_MATRIX["cells"]
                    if c["state"] == "NOT-SELECTED"}
    seen: set[str] = set()
    for row in registry:
        capability = row["capabilityId"]
        if capability.startswith("preview-"):
            raise AdmissionError("preview capability constants are not product registry rows")
        if capability not in known:
            raise AdmissionError("native.release-capability-unregistered:" + capability)
        if capability in seen:
            # Two rows for one capability would leave the applicable mode set ambiguous.
            raise AdmissionError("native.release-capability-duplicate:" + capability)
        seen.add(capability)
        for mode in row["languageModes"]:
            if mode not in modes:
                raise AdmissionError("native.release-capability-mode-unregistered:" + capability + ":" + mode)
            if (capability, mode) in not_selected:
                raise AdmissionError("native.release-capability-mode-not-selected:" + capability + ":" + mode)
    return registry


def admit_requested_capabilities(requested: list[dict]) -> list[dict]:
    """analysis-spec requestedCapabilities, against the SAME closed vocabulary the registry is held to.

    The field is `$ref: #/$defs/Text` and enters PlanId through analysisSpecDigest, and no document named the
    vocabulary it is drawn from - so three spellings were in live use in one release (relation@rung, a bare
    relation name, and the matrix ids) and two conforming hosts requesting the same analysis minted different
    PlanIds. Its languageMode sibling was already closed against a registered map at Run closure; this closes
    the asymmetry.

    A capability id and a relation@rung are not equated: one is a requestable unit of work that may cover
    several relations or none, the other is a fact/Coverage coordinate. The matrix publishes the bridge both
    ways, so nothing has to be guessed. This runs at the analysis-spec boundary AND again at retained Run
    closure, so an explicitly configured spec is judged exactly as a defaulted one."""
    known = {c["id"] for c in CAPABILITY_MATRIX["capabilities"]}
    modes = set(CAPABILITY_MATRIX["languageModes"])
    not_selected = {(c["capability"], c["mode"]) for c in CAPABILITY_MATRIX["cells"]
                    if c["state"] == "NOT-SELECTED"}
    for row in requested:
        capability, mode = row["capabilityId"], row["languageMode"]
        if capability not in known:
            raise AdmissionError("native.requested-capability-unregistered:" + capability)
        if mode not in modes:
            raise AdmissionError("native.requested-capability-mode-unregistered:" + capability + ":" + mode)
        if (capability, mode) in not_selected:
            # NOT-SELECTED means `outside D-371; no promise`, so there is nothing to disclose and nothing to
            # narrow. An UNSUPPORTED-TYPED cell is a different thing entirely: it IS requestable and is
            # answered with `unknown` plus its own named deficiency and cause.
            raise AdmissionError("native.requested-capability-mode-not-selected:" + capability + ":" + mode)
    return requested


def default_capability_selection(units: list[dict], registry: list[dict]) -> dict:
    """Native default discovery (review v2 item 6): the FULL registered TS/JS/Rust capability set from the
    authenticated release declaration registry (TRUSTED INPUT rows {capabilityId, languageModes[]}) is selected
    for every unit whose mode the capability applies to. There is no preview-typescript constant and no
    TypeScript-only default. Output validates against the foundation analysis-spec record.

    The registry is admitted against the published capability vocabulary before any row is read, so the
    DEFAULT and EXPLICIT paths agree on one spelling by construction rather than by convention."""
    admit_release_capability_registry(registry)
    requested = []
    for u in units:
        for r in registry:
            if u["languageMode"] in r["languageModes"]:
                requested.append({"capabilityId": r["capabilityId"], "languageMode": u["languageMode"], "workspaceRoot": u["rootPath"] or ".", "required": True})
    # `analysis-spec.requestedCapabilities` is x-opensip-order: canonical-set, so the emitted array is in
    # canonical-byte order, not discovery order; a duplicate row refuses rather than silently deduping.
    requested = sorted(requested, key=C.canonical)
    if len({C.canonical(r) for r in requested}) != len(requested):
        raise AdmissionError("DUPLICATE_REQUESTED_CAPABILITY")
    spec = {"schemaVersion": 2, "requestedCapabilities": requested, "policyPackIds": [], "parameters": []}
    validate_foundation("analysis-spec", spec)
    families = sorted({u["languageFamily"] for u in units})
    return {"analysisSpec": spec, "familiesSelected": families, "previewDefaultsUsed": False, "provenance": "DEFAULTED"}


def join_unit_coverage(per_unit: list[dict]) -> dict:
    deficiencies = [u["deficiency"] for u in per_unit if u["coverage"] != "complete"]
    if not deficiencies:
        return {"coverage": "complete", "deficiency": None, "narrowed": False}
    return {"coverage": "unknown", "deficiency": min(deficiencies, key=PRECEDENCE_V2.index), "narrowed": False,
            "units": [u["unit"] for u in per_unit if u["coverage"] != "complete"]}


__all__ = [name for name in dir() if not name.startswith("_")]
