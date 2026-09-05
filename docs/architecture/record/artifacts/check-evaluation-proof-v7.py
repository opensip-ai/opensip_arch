#!/usr/bin/env python3
"""Executable design-integrity checker for Evaluation Proof v7.

EP7 preserves EP6's exact C2/RI/raw/semantic proof core while moving the
EvaluationAuthorityIndex out of caller-controlled JSON.  An untrusted closed
EvaluationAuthorityCandidateV1 can be admitted only by a guarded, host-created
ProjectStoreAuthorityV1.  The store port publishes/verifies immutable CAS,
inserts-or-verifies the unique ProjectId/EAS index, rereads trusted state, and
only then mints a store-instance-bound capability.

The in-memory port below is an executable specification/test double.  It is not
evidence of a production store, transaction implementation, or atomicity.

Public successor APIs consumed by RT12/Evidence v6:

  authorize_evaluation(store, candidate) -> AdmittedEvaluationAuthorityV1
  resolve_stored_evaluation(store, eas_ref) -> AdmittedEvaluationAuthorityV1
  assert_store_continuity(store, admitted_handle)
  validate_bundle(bundle, admitted_handle)
  resolve_semantic_object_bindings(admitted_handle)
  derive_semantic_requirements(admitted_handle)
  derive_dependency_edges(bundle, admitted_handle)
  derive_raw_proof_requirements(bundle, admitted_handle)
  derive_transitive_requirements(seed_requirements, dependency_edges)
  encode_semantic_object_binding(binding)

Usage: python3 -B check-evaluation-proof-v7.py [artifact] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import pickle
import re
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evaluation-proof.v7.json"
EXPECTED_VERSION = 7
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

PINNED = {
    "evaluation-proof.v6.json": "74f35668afae2efb57070ff9a2897d373a91b42cc1cbbc87f3c673f872ca4bce",
    "check-evaluation-proof-v6.py": "0a7ac122a598bb7b9454b1b3c46c586f6fd551a2a1ebcf5584665f875457c5f0",
}

CANDIDATE_FIELDS = {
    "schemaVersion", "interfaceId", "admittedResolvedInputs",
    "planAuthorityReceipt", "evaluationAuthorityAdmission",
    "authorityObjectRecords", "authorityDependencyEdges",
    "evaluationAuthoritySeal", "activationManifest",
    "semanticObjectBindings", "semanticObjectRecords",
}
FIXTURE_FIELDS = {
    "schemaVersion", "fixtureOnly", "fixtureId", "projectId",
    "hostAdmissionEvidence", "immutableCasRecords",
    "evaluationAuthorityIndex",
}
HOST_EVIDENCE_FIELDS = {
    "projectMarkerRef", "projectRegistryRef", "openedRootRef",
}
RAW_ROW_FIELDS = {"projectId", "recordCasRef", "recordKind", "recordBytesHex"}
INDEX_FIELDS = {
    "schemaVersion", "projectId", "evaluationAuthoritySealRef",
    "evaluationAuthorityAdmissionRef",
}
FORBIDDEN_CANDIDATE_KEYS = {
    "evaluationAuthorityStoreIndex", "EvaluationAuthorityIndexV1",
    "projectStoreAuthority", "ProjectStoreAuthorityV1", "storeInstanceToken",
    "transactionToken", "indexGeneration", "verificationOwner", "suppliedBy",
    "verified", "pinned",
}


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def sha_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _load_module(filename: str, name: str) -> Any:
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_EP6: Any = None


def _ep6() -> Any:
    global _EP6
    for filename, expected in PINNED.items():
        actual = sha_file(HERE / filename)
        if actual != expected:
            raise ValueError(f"pinned input drift: {filename} {actual} != {expected}")
    if _EP6 is None:
        _EP6 = _load_module("check-evaluation-proof-v6.py", "ep6_pinned_for_ep7")
    return _EP6


def _exact_project(value: Any, label: str) -> str:
    if not isinstance(value, str) or not PROJECT_RE.fullmatch(value):
        raise ValueError(f"{label} is not PROJECT-ID-V1")
    return value


def _exact_ref(value: Any, label: str) -> str:
    if not isinstance(value, str) or not REF_RE.fullmatch(value):
        raise ValueError(f"{label} is not sha256 ref")
    return value


def _walk_candidate(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        bad = set(value) & FORBIDDEN_CANDIDATE_KEYS
        if bad:
            raise ValueError(f"{path} contains forbidden store/attestation keys {sorted(bad)}")
        for key, child in value.items():
            _walk_candidate(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_candidate(child, f"{path}[{index}]")


def _host_ref(domain: str, project: str, fixture_id: str) -> str:
    raw = domain.encode("ascii") + b"\0" + project.encode("ascii") + b"\0" + fixture_id.encode("ascii")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _validate_physical_row(row: Any, project: str) -> dict[str, Any]:
    if not isinstance(row, dict) or set(row) != RAW_ROW_FIELDS:
        raise ValueError("trusted CAS row is not exact/closed")
    if row.get("projectId") != project:
        raise ValueError("trusted CAS row crosses ProjectId")
    ref = _exact_ref(row.get("recordCasRef"), "CAS row ref")
    kind = row.get("recordKind")
    raw_hex = row.get("recordBytesHex")
    if not isinstance(kind, str) or not kind or not isinstance(raw_hex, str) or \
            not re.fullmatch(r"(?:[0-9a-f]{2})+", raw_hex):
        raise ValueError("trusted CAS row kind/bytes invalid")
    if "sha256:" + hashlib.sha256(bytes.fromhex(raw_hex)).hexdigest() != ref:
        raise ValueError("trusted CAS row raw hash mismatch")
    return copy.deepcopy(row)


def _validate_index_row(row: Any, project: str) -> dict[str, Any]:
    if not isinstance(row, dict) or set(row) != INDEX_FIELDS or row.get("schemaVersion") != 1:
        raise ValueError("EvaluationAuthorityIndexV1 row is not exact/closed")
    if row.get("projectId") != project:
        raise ValueError("EvaluationAuthorityIndexV1 crosses ProjectId")
    _exact_ref(row.get("evaluationAuthoritySealRef"), "index EAS ref")
    _exact_ref(row.get("evaluationAuthorityAdmissionRef"), "index admission ref")
    return copy.deepcopy(row)


_HOST_TOKEN = object()
_STATE_TOKEN = object()
_STORE_TOKEN = object()
_HANDLE_TOKEN = object()


class _HostProjectAdmissionV1:
    __slots__ = ("_token", "_project", "_marker", "_registry", "_root")

    def __init__(self, token: object, project: str, marker: str,
                 registry: str, root: str) -> None:
        if token is not _HOST_TOKEN:
            raise TypeError("HostProjectAdmissionV1 has no public constructor")
        self._token = token
        self._project = project
        self._marker = marker
        self._registry = registry
        self._root = root

    def __reduce__(self):
        raise TypeError("HostProjectAdmissionV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque HostProjectAdmissionV1>"


class _TrustedStoreState:
    __slots__ = ("_token", "_project", "_cas", "_index", "_candidates", "_index_versions")

    def __init__(self, token: object, project: str, cas_rows: list[dict[str, Any]],
                 index_rows: list[dict[str, Any]]) -> None:
        if token is not _STATE_TOKEN:
            raise TypeError("TrustedStoreState has no public constructor")
        self._token = token
        self._project = project
        self._cas: dict[str, list[dict[str, Any]]] = {}
        for row in cas_rows:
            self._cas.setdefault(row["recordCasRef"], []).append(copy.deepcopy(row))
        self._index = copy.deepcopy(index_rows)
        self._candidates: dict[tuple[str, str], dict[str, Any]] = {}
        self._index_versions: dict[tuple[str, str], int] = {}
        for row in index_rows:
            key = (row["projectId"], row["evaluationAuthoritySealRef"])
            self._index_versions[key] = 1

    def __reduce__(self):
        raise TypeError("TrustedStoreState is non-serializable")


class _AdmittedEvaluationAuthorityV1:
    __slots__ = (
        "_token", "_store_token", "_project", "_eas_ref", "_admission_ref",
        "_index_fingerprint", "_index_version", "_candidate", "_legacy",
        "_required_rows",
    )

    def __init__(self, token: object, *, store_token: object, project: str,
                 eas_ref: str, admission_ref: str, index_fingerprint: str,
                 index_version: int, candidate: dict[str, Any], legacy: Any,
                 required_rows: list[dict[str, Any]]) -> None:
        if token is not _HANDLE_TOKEN:
            raise TypeError("AdmittedEvaluationAuthorityV1 has no public constructor")
        self._token = token
        self._store_token = store_token
        self._project = project
        self._eas_ref = eas_ref
        self._admission_ref = admission_ref
        self._index_fingerprint = index_fingerprint
        self._index_version = index_version
        self._candidate = copy.deepcopy(candidate)
        self._legacy = legacy
        self._required_rows = copy.deepcopy(required_rows)

    def __reduce__(self):
        raise TypeError("AdmittedEvaluationAuthorityV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque AdmittedEvaluationAuthorityV1>"


class _ProjectStoreAuthorityV1:
    __slots__ = (
        "_token", "_instance_token", "_project", "_marker", "_registry",
        "_root", "_state",
    )

    def __init__(self, token: object, host: _HostProjectAdmissionV1,
                 state: _TrustedStoreState) -> None:
        if token is not _STORE_TOKEN or not isinstance(host, _HostProjectAdmissionV1) or \
                host._token is not _HOST_TOKEN or not isinstance(state, _TrustedStoreState) or \
                state._token is not _STATE_TOKEN:
            raise TypeError("ProjectStoreAuthorityV1 has no public constructor")
        if host._project != state._project:
            raise ValueError("host admission/store state ProjectId mismatch")
        self._token = token
        self._instance_token = object()
        self._project = host._project
        self._marker = host._marker
        self._registry = host._registry
        self._root = host._root
        self._state = state

    def __reduce__(self):
        raise TypeError("ProjectStoreAuthorityV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque ProjectStoreAuthorityV1>"

    def authorize_evaluation(self, candidate: Any) -> _AdmittedEvaluationAuthorityV1:
        """Atomically validate, publish/verify, index, reread, then mint."""
        if not isinstance(candidate, dict) or set(candidate) != CANDIDATE_FIELDS:
            raise ValueError("EvaluationAuthorityCandidateV1 is not exact/closed")
        if candidate.get("schemaVersion") != 1 or candidate.get("interfaceId") != \
                "opensip-evidence.evaluation-authority-candidate.v1":
            raise ValueError("EvaluationAuthorityCandidateV1 interface/version mismatch")
        _walk_candidate(candidate)
        try:
            candidate_project = candidate["evaluationAuthorityAdmission"]["projectId"]
            resolved_project = candidate["admittedResolvedInputs"]["projectId"]
        except (KeyError, TypeError) as exc:
            raise ValueError("candidate lacks closed project authority") from exc
        _exact_project(candidate_project, "candidate project")
        if candidate_project != resolved_project or candidate_project != self._project:
            raise ValueError("candidate/store ProjectId mismatch before CAS mutation")

        ep6 = _ep6()
        admission = candidate["evaluationAuthorityAdmission"]
        admission_ref = ep6.raw_record_ref("EvaluationAuthorityAdmissionV1", admission)
        eas_ref = _exact_ref(admission.get("evaluationAuthoritySealRef"), "candidate EAS ref")
        index_row = {
            "schemaVersion": 1,
            "projectId": self._project,
            "evaluationAuthoritySealRef": eas_ref,
            "evaluationAuthorityAdmissionRef": admission_ref,
        }
        # EP6 remains the pinned pure recomputation oracle.  The only index it
        # sees is module-derived; no caller/store row participates in this step.
        ep6_input = copy.deepcopy(candidate)
        ep6_input["interfaceId"] = "opensip-evidence.evaluation-authority-admission.v1"
        ep6_input["evaluationAuthorityStoreIndex"] = [copy.deepcopy(index_row)]
        legacy = ep6.admit_evaluation_authority(ep6_input)

        required_rows = copy.deepcopy(
            candidate["authorityObjectRecords"] + candidate["semanticObjectRecords"])
        required_rows.sort(key=lambda row: (
            row.get("projectId"), row.get("recordCasRef"), row.get("recordKind")))
        # Work on private copies and publish all changes only after every reread
        # succeeds.  The transaction token is deliberately local/nonserializable.
        transaction_token = object()
        if transaction_token is None:  # pragma: no cover - documents liveness only
            raise AssertionError("unreachable")
        work_cas = copy.deepcopy(self._state._cas)
        work_index = copy.deepcopy(self._state._index)
        work_versions = copy.deepcopy(self._state._index_versions)
        for supplied in required_rows:
            row = _validate_physical_row(supplied, self._project)
            existing = work_cas.get(row["recordCasRef"], [])
            if len(existing) > 1:
                raise ValueError("duplicate immutable CAS key")
            if existing and existing[0] != row:
                raise ValueError("conflicting immutable CAS key")
            if not existing:
                work_cas[row["recordCasRef"]] = [copy.deepcopy(row)]

        key = (self._project, eas_ref)
        matches = [row for row in work_index
                   if (row.get("projectId"), row.get("evaluationAuthoritySealRef")) == key]
        if len(matches) > 1:
            raise ValueError("duplicate EvaluationAuthorityIndexV1 key")
        if matches and matches[0] != index_row:
            raise ValueError("conflicting EvaluationAuthorityIndexV1 key")
        if not matches:
            work_index.append(copy.deepcopy(index_row))
            work_index.sort(key=canonical_json)
            work_versions[key] = work_versions.get(key, 0) + 1
        elif key not in work_versions:
            work_versions[key] = 1

        # Trusted reread inside the same transaction snapshot.
        reread = [row for row in work_index
                  if (row.get("projectId"), row.get("evaluationAuthoritySealRef")) == key]
        if reread != [index_row]:
            raise ValueError("authority index reread differs")
        for row in required_rows:
            stored = work_cas.get(row["recordCasRef"], [])
            if stored != [row]:
                raise ValueError("authority CAS reread missing/duplicate/conflicting")
            _validate_physical_row(stored[0], self._project)

        self._state._cas = work_cas
        self._state._index = work_index
        self._state._index_versions = work_versions
        self._state._candidates[key] = copy.deepcopy(candidate)
        fingerprint = ep6.raw_record_ref("EvaluationAuthorityIndexV1", index_row)
        return _AdmittedEvaluationAuthorityV1(
            _HANDLE_TOKEN, store_token=self._instance_token, project=self._project,
            eas_ref=eas_ref, admission_ref=admission_ref,
            index_fingerprint=fingerprint, index_version=work_versions[key],
            candidate=candidate, legacy=legacy, required_rows=required_rows)

    def resolve_stored_evaluation(self, eas_ref: Any) -> _AdmittedEvaluationAuthorityV1:
        ref = _exact_ref(eas_ref, "stored-read EAS ref")
        key = (self._project, ref)
        matches = [row for row in self._state._index
                   if (row.get("projectId"), row.get("evaluationAuthoritySealRef")) == key]
        if len(matches) != 1:
            raise ValueError("stored-read index missing or duplicate")
        _validate_index_row(matches[0], self._project)
        candidate = self._state._candidates.get(key)
        if candidate is None:
            raise ValueError("stored-read has no store-admitted candidate reconstruction")
        required_rows = copy.deepcopy(
            candidate["authorityObjectRecords"] + candidate["semanticObjectRecords"])
        for expected in required_rows:
            rows = self._state._cas.get(expected["recordCasRef"], [])
            if rows != [expected]:
                raise ValueError("stored-read authority CAS missing/duplicate/conflicting")
            _validate_physical_row(rows[0], self._project)
        # authorize_evaluation repeats raw/C2/RI/semantic validation and performs
        # the same exact trusted CAS/index reread before returning a fresh handle.
        return self.authorize_evaluation(copy.deepcopy(candidate))


# Public nominal aliases expose type names, not usable constructors.
ProjectStoreAuthorityV1 = _ProjectStoreAuthorityV1
AdmittedEvaluationAuthorityV1 = _AdmittedEvaluationAuthorityV1


def open_project_store_authority(host_admission: Any, state: Any) -> _ProjectStoreAuthorityV1:
    """Production-shaped constructor: only two guarded host objects are accepted."""
    if not isinstance(host_admission, _HostProjectAdmissionV1) or \
            host_admission._token is not _HOST_TOKEN:
        raise TypeError("host-admitted project capability required")
    if not isinstance(state, _TrustedStoreState) or state._token is not _STATE_TOKEN:
        raise TypeError("trusted store state capability required")
    return _ProjectStoreAuthorityV1(_STORE_TOKEN, host_admission, state)


def _open_test_project_store(fixture: Any) -> _ProjectStoreAuthorityV1:
    """Fixture-only bridge; ordinary JSON never reaches the production constructor."""
    if not isinstance(fixture, dict) or set(fixture) != FIXTURE_FIELDS or \
            fixture.get("schemaVersion") != 1 or fixture.get("fixtureOnly") is not True:
        raise ValueError("trusted test-store fixture is not exact/closed")
    fixture_id = fixture.get("fixtureId")
    project = _exact_project(fixture.get("projectId"), "fixture project")
    if not isinstance(fixture_id, str) or not re.fullmatch(r"[a-z0-9-]+", fixture_id):
        raise ValueError("fixture id invalid")
    host = fixture.get("hostAdmissionEvidence")
    if not isinstance(host, dict) or set(host) != HOST_EVIDENCE_FIELDS:
        raise ValueError("host admission evidence is not exact/closed")
    expected_host = {
        "projectMarkerRef": _host_ref("opensip.test.project-marker.v1", project, fixture_id),
        "projectRegistryRef": _host_ref("opensip.test.project-registry.v1", project, fixture_id),
        "openedRootRef": _host_ref("opensip.test.opened-root.v1", project, fixture_id),
    }
    if host != expected_host:
        raise ValueError("test host marker/registry/open-root admission differs")
    cas = fixture.get("immutableCasRecords")
    index = fixture.get("evaluationAuthorityIndex")
    if not isinstance(cas, list) or not isinstance(index, list):
        raise ValueError("fixture CAS/index must be arrays")
    cas_rows = [_validate_physical_row(row, project) for row in cas]
    index_rows = [_validate_index_row(row, project) for row in index]
    host_capability = _HostProjectAdmissionV1(
        _HOST_TOKEN, project, host["projectMarkerRef"],
        host["projectRegistryRef"], host["openedRootRef"])
    state = _TrustedStoreState(_STATE_TOKEN, project, cas_rows, index_rows)
    return open_project_store_authority(host_capability, state)


def _require_store(value: Any) -> _ProjectStoreAuthorityV1:
    if not isinstance(value, _ProjectStoreAuthorityV1) or value._token is not _STORE_TOKEN:
        raise TypeError("live ProjectStoreAuthorityV1 capability required")
    return value


def _require_handle(value: Any) -> _AdmittedEvaluationAuthorityV1:
    if not isinstance(value, _AdmittedEvaluationAuthorityV1) or value._token is not _HANDLE_TOKEN:
        raise TypeError("module-minted AdmittedEvaluationAuthorityV1 required")
    return value


def authorize_evaluation(store: Any, candidate: Any) -> _AdmittedEvaluationAuthorityV1:
    return _require_store(store).authorize_evaluation(candidate)


def resolve_stored_evaluation(store: Any, eas_ref: Any) -> _AdmittedEvaluationAuthorityV1:
    return _require_store(store).resolve_stored_evaluation(eas_ref)


def assert_store_continuity(store: Any, authority: Any) -> bool:
    port = _require_store(store)
    handle = _require_handle(authority)
    if handle._store_token is not port._instance_token or handle._project != port._project:
        raise ValueError("store-instance/project capability continuity mismatch")
    key = (port._project, handle._eas_ref)
    matches = [row for row in port._state._index
               if (row.get("projectId"), row.get("evaluationAuthoritySealRef")) == key]
    if len(matches) != 1:
        raise ValueError("current authority index missing or duplicate")
    row = _validate_index_row(matches[0], port._project)
    if row["evaluationAuthorityAdmissionRef"] != handle._admission_ref or \
            _ep6().raw_record_ref("EvaluationAuthorityIndexV1", row) != handle._index_fingerprint or \
            port._state._index_versions.get(key) != handle._index_version:
        raise ValueError("authority index changed after admission")
    for expected in handle._required_rows:
        rows = port._state._cas.get(expected["recordCasRef"], [])
        if rows != [expected]:
            raise ValueError("authority CAS changed/missing after admission")
        _validate_physical_row(rows[0], port._project)
    return True


def encode_semantic_object_binding(binding: dict[str, Any]) -> bytes:
    return _ep6().encode_semantic_object_binding(binding)


def resolve_semantic_object_bindings(authority: Any) -> dict[str, dict[str, Any]]:
    return _ep6().resolve_semantic_object_bindings(_require_handle(authority)._legacy)


def derive_semantic_requirements(authority: Any) -> list[dict[str, str]]:
    return _ep6().derive_semantic_requirements(_require_handle(authority)._legacy)


def derive_dependency_edges(bundle: Any, authority: Any) -> list[dict[str, Any]]:
    return _ep6().derive_dependency_edges(bundle, _require_handle(authority)._legacy)


def derive_transitive_requirements(seed_requirements: dict[str, str],
                                   dependency_edges: list[dict[str, Any]]) -> dict[str, str]:
    return _ep6().derive_transitive_requirements(seed_requirements, dependency_edges)


def derive_raw_proof_requirements(bundle: Any, authority: Any) -> list[dict[str, str]]:
    return _ep6().derive_raw_proof_requirements(bundle, _require_handle(authority)._legacy)


def validate_bundle(bundle: Any, authority: Any) -> list[tuple[str, str]]:
    try:
        handle = _require_handle(authority)
    except (TypeError, ValueError) as exc:
        return [("EP7-AUTHORITY", str(exc))]
    findings = _ep6().validate_bundle(bundle, handle._legacy)
    return [(code.replace("EP6-", "EP7-"), detail) for code, detail in findings]


def _project_vector(vector: dict[str, Any]) -> dict[str, Any]:
    value = {key: copy.deepcopy(item) for key, item in vector.items()
             if key not in {"evaluationAuthorityCandidate", "trustedStoreFixture"}}
    value["id"] = value["id"].replace("EP7-", "EP6-", 1)
    candidate = copy.deepcopy(vector["evaluationAuthorityCandidate"])
    candidate["interfaceId"] = "opensip-evidence.evaluation-authority-admission.v1"
    candidate["evaluationAuthorityStoreIndex"] = copy.deepcopy(
        vector["trustedStoreFixture"]["evaluationAuthorityIndex"])
    value["authorityAdmissionInput"] = candidate
    return value


def _fixture_errors(vector: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        fixture = vector["trustedStoreFixture"]
        candidate = vector["evaluationAuthorityCandidate"]
        store = _open_test_project_store(fixture)
        handle = authorize_evaluation(store, candidate)
        assert_store_continuity(store, handle)
        reread = resolve_stored_evaluation(
            store, candidate["evaluationAuthorityAdmission"]["evaluationAuthoritySealRef"])
        assert_store_continuity(store, reread)
        rows = copy.deepcopy(candidate["authorityObjectRecords"] + candidate["semanticObjectRecords"])
        rows.sort(key=lambda row: (row["projectId"], row["recordCasRef"], row["recordKind"]))
        if fixture["immutableCasRecords"] != rows:
            errors.append("fixture CAS is not exact candidate custody")
        if validate_bundle(vector["bundle"], handle):
            errors.append("EP6 pure core rejected store-admitted handle")
    except Exception as exc:
        errors.append(f"store authorization failed: {type(exc).__name__}: {exc}")
    return errors


def check(contract: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["root is not an object"]
    try:
        ep6 = _ep6()
        predecessor = load_json(HERE / "evaluation-proof.v6.json")
    except Exception as exc:
        return [f"pinned predecessor import failed: {type(exc).__name__}: {exc}"]
    if ep6.check(predecessor):
        errors.append("pinned EP6 predecessor no longer validates")
    if (contract.get("artifact"), contract.get("version")) != \
            ("opensip.evaluation-proof", EXPECTED_VERSION):
        errors.append("artifact/version mismatch")
    if contract.get("status") != "CANDIDATE-NOT-APPLIED" or \
            contract.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal status drift")
    assurance = contract.get("assurance") or {}
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("candidateState") != "NOT-APPLIED" or \
            assurance.get("qualificationEvidenceIds") != [] or \
            assurance.get("releaseEvidenceIds") != []:
        errors.append("assurance exceeds specified/implementable-unexecuted")
    residuals = json.dumps(contract.get("knownLimitations") or [])
    if not all(term in residuals for term in ("V10", "CD-RT-5", "G19", "not applied")):
        errors.append("required unresolved/blocked/not-applied residuals absent")

    admission = contract.get("authorityAdmissionContract") or {}
    store_contract = contract.get("projectStoreAuthorityContract") or {}
    if admission.get("untrustedInputType") != "EvaluationAuthorityCandidateV1" or \
            admission.get("storePortType") != "ProjectStoreAuthorityV1" or \
            admission.get("atomicApi") != \
            "ProjectStoreAuthorityV1.authorize_evaluation(EvaluationAuthorityCandidateV1) -> AdmittedEvaluationAuthorityV1" or \
            admission.get("nonSerializable") is not True or \
            admission.get("noPublicConstructor") is not True:
        errors.append("candidate/store/capability admission contract drift")
    order = admission.get("authorizeOrder") or []
    if len(order) != 5 or not all(term in json.dumps(order) for term in (
            "rehash", "C2/RI", "publish-or-verify", "insert-or-verify", "read", "mint")):
        errors.append("atomic authorize order incomplete")
    if set(store_contract.get("operationalOnly") or []) != {
            "storeInstanceToken", "transactionToken", "indexGeneration"}:
        errors.append("operational store token registry drift")
    index_contract = contract.get("evaluationAuthorityStoreIndex") or {}
    if "forbidden in EvaluationAuthorityCandidateV1" not in index_contract.get("ownership", "") or \
            "append-only" not in index_contract.get("mutationRule", ""):
        errors.append("trusted index ownership/mutation rule drift")

    changed_top = {
        "version", "role", "supersedesProofObligationsOf", "repairs",
        "positiveVectors", "assurance", "knownLimitations", "authoritySeam",
        "authorityAdmissionContract", "evaluationAuthorityStoreIndex",
        "acceptedAuthorityVectorId", "projectStoreAuthorityContract",
        "identityStabilityFromEP6", "adversarialControlsV7", "invariants",
        "activationAuthority",
    }
    for key in set(predecessor) - changed_top:
        if contract.get(key) != predecessor[key]:
            errors.append(f"EP6 protected surface changed: {key}")
    stability = contract.get("identityStabilityFromEP6") or {}
    if stability.get("predecessorSha256") != PINNED["evaluation-proof.v6.json"] or \
            stability.get("predecessorCheckerSha256") != PINNED["check-evaluation-proof-v6.py"]:
        errors.append("EP6 protected hash window drift")
    expected_invariants = copy.deepcopy(predecessor["invariants"])
    ep12 = next((row for row in expected_invariants if row.get("id") == "EP-12"), None)
    if ep12 is not None:
        ep12["assert"] = "Only ProjectStoreAuthorityV1.authorize_evaluation over a recursively closed EvaluationAuthorityCandidateV1 may mint AdmittedEvaluationAuthorityV1. The candidate carries no store/index state; trusted CAS/index reread and store-instance continuity are mandatory before core invocation."
    if contract.get("invariants") != expected_invariants:
        errors.append("EP7 active authority invariant drift")
    activation = contract.get("activationAuthority") or {}
    if activation.get("inputType") != \
            "EvaluationAuthorityCandidateV1 + ProjectStoreAuthorityV1" or \
            "contains no store/index fields" not in activation.get("trustedInputRule", "") or \
            "insert-or-verify and reread" not in activation.get("trustedInputRule", "") or \
            not activation.get("producerAuthority", "").startswith("ProjectStoreAuthorityV1 only"):
        errors.append("EP7 active authority type/producer rule drift")

    vectors = contract.get("positiveVectors")
    predecessor_vectors = predecessor.get("positiveVectors")
    if not isinstance(vectors, list) or len(vectors) != 7:
        errors.append("expected seven EP7 vectors")
        return errors
    if [_project_vector(row) for row in vectors] != predecessor_vectors:
        errors.append("EP7 -> EP6 vector projection is not byte-value exact")
    seen: set[str] = set()
    for index, vector in enumerate(vectors):
        ident = vector.get("id") if isinstance(vector, dict) else None
        if not isinstance(ident, str) or not ident.startswith("EP7-POS-") or ident in seen:
            errors.append(f"vector[{index}] id invalid/duplicate")
            continue
        seen.add(ident)
        candidate = vector.get("evaluationAuthorityCandidate")
        if not isinstance(candidate, dict) or set(candidate) != CANDIDATE_FIELDS:
            errors.append(f"{ident}: candidate is not exact/closed")
        else:
            try:
                _walk_candidate(candidate)
            except ValueError as exc:
                errors.append(f"{ident}: {exc}")
        errors.extend(f"{ident}: {item}" for item in _fixture_errors(vector))
    if contract.get("acceptedAuthorityVectorId") != "EP7-POS-NOMATCH-PASS":
        errors.append("accepted vector id drift")
    required_negatives = {
        "EP7-NEG-FORGED-CANDIDATE-INDEX-FIELD", "EP7-NEG-PLAIN-DICT-STORE",
        "EP7-NEG-OWNER-STRING-BOOLEAN-REF-STORE", "EP7-NEG-WRONG-PROJECT-STORE",
        "EP7-NEG-ABSENT-STORED-INDEX", "EP7-NEG-DUPLICATE-INDEX",
        "EP7-NEG-CONFLICTING-INDEX", "EP7-NEG-MISSING-CAS",
        "EP7-NEG-CALLER-CONSTRUCTED-STORE", "EP7-NEG-CALLER-CONSTRUCTED-HANDLE",
        "EP7-NEG-SERIALIZED-STORE-OR-HANDLE", "EP7-NEG-TOCTOU-INDEX-REPLACEMENT",
        "EP7-NEG-DIFFERENT-STORE-FINALIZER",
    }
    negatives = contract.get("adversarialControlsV7") or []
    if {row.get("id") for row in negatives if isinstance(row, dict)} != required_negatives:
        errors.append("EP7 adversarial matrix incomplete")
    return errors


def _must_reject(label: str, fn: Any, failures: list[str]) -> None:
    try:
        fn()
        failures.append(f"{label}: escaped")
    except (KeyError, TypeError, UnicodeError, ValueError, DuplicateKeyError):
        pass


def _empty_fixture(project: str, fixture_id: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1, "fixtureOnly": True, "fixtureId": fixture_id,
        "projectId": project,
        "hostAdmissionEvidence": {
            "projectMarkerRef": _host_ref("opensip.test.project-marker.v1", project, fixture_id),
            "projectRegistryRef": _host_ref("opensip.test.project-registry.v1", project, fixture_id),
            "openedRootRef": _host_ref("opensip.test.opened-root.v1", project, fixture_id),
        },
        "immutableCasRecords": [], "evaluationAuthorityIndex": [],
    }


def selftest(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    vector = next(row for row in contract["positiveVectors"]
                  if row["id"] == "EP7-POS-NOMATCH-PASS")
    candidate = vector["evaluationAuthorityCandidate"]
    fixture = vector["trustedStoreFixture"]
    store = _open_test_project_store(fixture)
    handle = authorize_evaluation(store, candidate)
    if validate_bundle(vector["bundle"], handle) or not assert_store_continuity(store, handle):
        failures.append("positive store-authorized control failed")
    reread = resolve_stored_evaluation(
        store, candidate["evaluationAuthorityAdmission"]["evaluationAuthoritySealRef"])
    if validate_bundle(vector["bundle"], reread):
        failures.append("positive stored-read control failed")

    forged = copy.deepcopy(candidate)
    forged["evaluationAuthorityStoreIndex"] = copy.deepcopy(fixture["evaluationAuthorityIndex"])
    _must_reject("forged candidate index", lambda: authorize_evaluation(store, forged), failures)
    forged = copy.deepcopy(candidate)
    forged["activationManifest"]["projectStoreAuthority"] = "sha256:" + "1" * 64
    _must_reject("nested forged store authority", lambda: authorize_evaluation(store, forged), failures)
    for false_store in ({}, "opensip-store", True, "sha256:" + "2" * 64):
        _must_reject("plain/owner/boolean/ref store",
                     lambda value=false_store: authorize_evaluation(value, candidate), failures)

    wrong_project = "prj1-" + "b" * 64
    wrong_store = _open_test_project_store(_empty_fixture(wrong_project, "wrong-project"))
    _must_reject("wrong-project store",
                 lambda: authorize_evaluation(wrong_store, candidate), failures)
    if wrong_store._state._cas or wrong_store._state._index:
        failures.append("wrong-project rejection mutated store")

    # Empty trusted state is a valid authorization target: CAS and index are
    # inserted atomically.  Absence remains fatal to stored-read resolution.
    empty = _open_test_project_store(_empty_fixture(fixture["projectId"], "empty-authorize"))
    empty_handle = authorize_evaluation(empty, candidate)
    if not assert_store_continuity(empty, empty_handle):
        failures.append("insert-if-absent positive control failed")
    key = (empty._project, empty_handle._eas_ref)
    empty._state._index = []
    empty._state._index_versions[key] += 1
    _must_reject("absent stored index",
                 lambda: resolve_stored_evaluation(empty, empty_handle._eas_ref), failures)

    duplicate_fixture = copy.deepcopy(fixture)
    duplicate_fixture["fixtureId"] = "duplicate-index"
    duplicate_fixture["hostAdmissionEvidence"] = _empty_fixture(
        fixture["projectId"], "duplicate-index")["hostAdmissionEvidence"]
    duplicate_fixture["evaluationAuthorityIndex"].append(
        copy.deepcopy(duplicate_fixture["evaluationAuthorityIndex"][0]))
    duplicate_store = _open_test_project_store(duplicate_fixture)
    _must_reject("duplicate index",
                 lambda: authorize_evaluation(duplicate_store, candidate), failures)

    conflict_fixture = copy.deepcopy(fixture)
    conflict_fixture["fixtureId"] = "conflicting-index"
    conflict_fixture["hostAdmissionEvidence"] = _empty_fixture(
        fixture["projectId"], "conflicting-index")["hostAdmissionEvidence"]
    conflict_fixture["evaluationAuthorityIndex"][0]["evaluationAuthorityAdmissionRef"] = \
        "sha256:" + "c" * 64
    conflict_store = _open_test_project_store(conflict_fixture)
    _must_reject("conflicting index",
                 lambda: authorize_evaluation(conflict_store, candidate), failures)

    missing_store = _open_test_project_store(fixture)
    missing_handle = authorize_evaluation(missing_store, candidate)
    missing_ref = missing_handle._required_rows[0]["recordCasRef"]
    del missing_store._state._cas[missing_ref]
    _must_reject("missing CAS stored read",
                 lambda: resolve_stored_evaluation(missing_store, missing_handle._eas_ref), failures)
    _must_reject("missing CAS continuity",
                 lambda: assert_store_continuity(missing_store, missing_handle), failures)

    _must_reject("caller-constructed store",
                 lambda: _ProjectStoreAuthorityV1(object(), None, None), failures)
    _must_reject("dict production constructor",
                 lambda: open_project_store_authority({}, {}), failures)
    _must_reject("caller-constructed handle", lambda: _AdmittedEvaluationAuthorityV1(
        object(), store_token=object(), project=fixture["projectId"],
        eas_ref="sha256:" + "1" * 64, admission_ref="sha256:" + "2" * 64,
        index_fingerprint="sha256:" + "3" * 64, index_version=1,
        candidate=candidate, legacy=None, required_rows=[]), failures)
    for label, value in (("store", store), ("handle", handle)):
        _must_reject(f"JSON serialized {label}", lambda item=value: json.dumps(item), failures)
        _must_reject(f"pickle serialized {label}", lambda item=value: pickle.dumps(item), failures)

    toctou_store = _open_test_project_store(fixture)
    toctou_handle = authorize_evaluation(toctou_store, candidate)
    toctou_key = (toctou_store._project, toctou_handle._eas_ref)
    replacement = copy.deepcopy(toctou_store._state._index[0])
    replacement["evaluationAuthorityAdmissionRef"] = "sha256:" + "d" * 64
    toctou_store._state._index = [replacement]
    toctou_store._state._index_versions[toctou_key] += 1
    _must_reject("TOCTOU index replacement",
                 lambda: assert_store_continuity(toctou_store, toctou_handle), failures)

    other_store = _open_test_project_store(fixture)
    _must_reject("different-store finalizer seam",
                 lambda: assert_store_continuity(other_store, handle), failures)

    changed = copy.deepcopy(contract)
    changed["positiveVectors"][0]["evaluationAuthorityCandidate"][
        "evaluationAuthorityStoreIndex"] = []
    if not check(changed, verify_files=False):
        failures.append("artifact candidate-index mutation escaped")
    changed = copy.deepcopy(contract)
    changed["identityStabilityFromEP6"]["predecessorSha256"] = "0" * 64
    if not check(changed, verify_files=False):
        failures.append("EP6 protected hash mutation escaped")
    return failures


def main(argv: list[str]) -> int:
    path = HERE / BINDING
    selftest_mode = "--selftest" in argv[1:]
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    if positional:
        path = pathlib.Path(positional[0])
    try:
        contract = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    findings = check(contract)
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        return 1
    if selftest_mode:
        failures = selftest(contract)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print("PASS: evaluation-proof.v7.json; 7 store-authorized vectors; "
              "13 named store-provenance adversarial controls")
    else:
        vector = next(row for row in contract["positiveVectors"]
                      if row["id"] == "EP7-POS-NOMATCH-PASS")
        store = _open_test_project_store(vector["trustedStoreFixture"])
        handle = authorize_evaluation(store, vector["evaluationAuthorityCandidate"])
        rows = derive_raw_proof_requirements(vector["bundle"], handle)
        counts = {cap: sum(row["requiredForCapability"] == cap for row in rows)
                  for cap in ("verifiable", "replayable")}
        print(f"PASS: evaluation-proof.v7.json; {len(rows)} unchanged raw refs "
              f"({counts['verifiable']} verifiable/{counts['replayable']} replayable); "
              "store provenance specified/implementable-unexecuted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
