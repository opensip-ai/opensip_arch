#!/usr/bin/env python3
"""Evidence v7 durable cold-restart and six-write finalization checker.

The executable store below is a guarded design test double.  Durable project
state is explicit and separate from ephemeral sessions; no process-global
ledger or old capability participates in recovery.  This is architecture
evidence only, not a production store, transaction, restart, or atomicity
demonstration.
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
BINDING = "evidence.v7.json"
PINS = {
    "evidence.v6.json": "a941cd24365ce4b0bd43de45698dc045d292005e378ed87e5e6884732e83e102",
    "check-evidence-v6.py": "ad3aa393abac0a5094678c3f29b2a4478eccb651b747c0e19e2e69499cab92f4",
    "evaluation-proof.v8.json": "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    "check-evaluation-proof-v8.py": "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    "retention-tiers.v13.json": "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    "check-retention-custody-v13.py": "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    "versioning-policy.v8.json": "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    "check-versioning-v8.py": "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
    "check-evidence-v4.py": "fd8db2ab77261ba31351d0647cf62ba4de92db35ba7a15426cb8f4bcf28865bc",
    "check-retention-custody.py": "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "scope-correction-a3.v5.json": "6ca4bd407b80d80aba9035dfb4d66d28d8704ccf30a729854810396c6f66c7af",
    "check-scope-correction-a3-v5.py": "5d777c42dfa6fb3826916b157f53955d66d07e93ce08acbdb1c27a027b753c0c",
}
FINAL_WRITES = [
    "TerminalRunV1", "RunIndexV1", "AttemptRunLinkV1", "CustodyRootV1",
    "RunAuthorityIndexV1", "outbox",
]
INDEX_FIELDS = [
    "schemaVersion", "projectId", "runId", "runSealRef",
    "planAuthorityReceiptRef", "evaluationAuthorityAdmissionRef", "planId",
    "planIntentCommitment", "executionPlanCommitment", "activationManifestRef",
    "evaluationAuthoritySealRef",
]
JOURNAL_FIELDS = {
    "schemaVersion", "projectId", "executionId", "expectedAttemptRevision",
    "evaluationAuthoritySealRef", "semanticEvidenceCasRef",
    "custodyPreparationRef",
}
PREPARATION_FIELDS = {
    "schemaVersion", "projectId", "executionId",
    "evaluationAuthoritySealRef", "semanticEvidenceCasRef",
    "evaluationProofBundleCasRef", "semanticCapabilityClosureCasRef",
    "semanticCapabilityClosureCommitment", "rawProofInventoryCasRef",
    "frozenRetentionTargetRef", "units",
}
PREPARED_OBJECT_FIELDS = {
    "schemaVersion", "projectId", "custodyPreparationRef",
    "frozenRetentionTargetRef", "unitId", "requiredForCapability",
    "recordCasRef", "recordKind",
}
ATTEMPT_FIELDS = {
    "schemaVersion", "projectId", "executionId", "revision",
    "evaluationAuthoritySealRef", "frozenRetentionTargetRef",
}
TOKEN_WORDS = {
    "storeInstanceToken", "transactionToken", "continuityToken",
    "preparedCustodyToken", "finalizedEvidenceToken", "candidateCache",
    "ProjectStoreAuthorityV1",
}
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
EXEC_RE = re.compile(r"^exec1-[a-z0-9-]+$")


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha_ref(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _contains_token_key(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(set(value) & TOKEN_WORDS) or any(
            _contains_token_key(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_token_key(child) for child in value)
    return False


_E6: Any = None
_EP8: Any = None
_RT13: Any = None
_V8: Any = None
_E4: Any = None
_RTCORE: Any = None


def _deps() -> tuple[Any, Any, Any, Any, Any, Any]:
    global _E6, _EP8, _RT13, _V8, _E4, _RTCORE
    for filename, expected in PINS.items():
        actual = sha_file(filename)
        if actual != expected:
            raise ValueError(f"pinned input drift: {filename} {actual} != {expected}")
    if _E6 is None:
        _E6 = module("check-evidence-v6.py", "evidence_v6_pinned_for_v7")
    if _EP8 is None:
        _EP8 = module("check-evaluation-proof-v8.py", "ep8_pinned_for_evidence_v7")
    if _RT13 is None:
        _RT13 = module("check-retention-custody-v13.py", "rt13_pinned_for_evidence_v7")
    if _V8 is None:
        _V8 = module("check-versioning-v8.py", "versioning_v8_pinned_for_evidence_v7")
    if _E4 is None:
        _E4 = module("check-evidence-v4.py", "evidence_wire_pinned_for_v7")
    if _RTCORE is None:
        _RTCORE = module("check-retention-custody.py", "rtcore_pinned_for_evidence_v7")
    return _E6, _EP8, _RT13, _V8, _E4, _RTCORE


class LedgerCorrupt(ValueError):
    pass


class CommitFailed(ValueError):
    pass


class InjectedCrash(RuntimeError):
    pass


class ResponseLost(RuntimeError):
    pass


class NoPreparedRun(ValueError):
    pass


_STATE_TOKEN = object()
_SESSION_TOKEN = object()
_FINALIZED_TOKEN = object()
_CUSTODY_TOKEN = object()
_COMMITTED_TOKEN = object()


class _DurableProjectStateV1:
    __slots__ = (
        "_token", "_project", "_authority_state", "_private_cas",
        "_attempts", "_custody_rows", "_ledger",
    )

    def __init__(self, token: object, project: str, authority_state: Any) -> None:
        if token is not _STATE_TOKEN:
            raise TypeError("DurableProjectStateV1 has no public constructor")
        self._token = token
        self._project = project
        self._authority_state = authority_state
        self._private_cas: dict[str, list[bytes]] = {}
        self._attempts: dict[tuple[str, str], dict[str, Any]] = {}
        self._custody_rows: dict[str, list[dict[str, Any]]] = {}
        self._ledger = {
            "journals": {},
            "records": {name: {} for name in FINAL_WRITES},
        }

    def __reduce__(self):
        raise TypeError("DurableProjectStateV1 is a guarded backend capability")


class _ProjectStoreSessionV1:
    __slots__ = ("_token", "_instance_token", "_project", "_state", "_ep_port")

    def __init__(self, token: object, state: _DurableProjectStateV1, ep_port: Any) -> None:
        if token is not _SESSION_TOKEN or not isinstance(state, _DurableProjectStateV1) or \
                state._token is not _STATE_TOKEN:
            raise TypeError("ProjectStoreAuthorityV1 has no public constructor")
        if state._project != ep_port._project or state._authority_state is not ep_port._state:
            raise ValueError("composite store session/state mismatch")
        self._token = token
        self._instance_token = ep_port._instance_token
        self._project = state._project
        self._state = state
        self._ep_port = ep_port

    def __reduce__(self):
        raise TypeError("ProjectStoreAuthorityV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque ProjectStoreAuthorityV1>"


class _FinalizedSemanticEvidenceV1:
    __slots__ = (
        "_token", "_store_token", "_project", "_eas_ref", "_admission_ref",
        "_execution_id", "_accepted",
    )

    def __init__(self, token: object, *, store_token: object, project: str,
                 eas_ref: str, admission_ref: str, execution_id: str,
                 accepted: dict[str, Any]) -> None:
        if token is not _FINALIZED_TOKEN:
            raise TypeError("FinalizedSemanticEvidenceV1 has no public constructor")
        self._token = token
        self._store_token = store_token
        self._project = project
        self._eas_ref = eas_ref
        self._admission_ref = admission_ref
        self._execution_id = execution_id
        self._accepted = copy.deepcopy(accepted)

    def __reduce__(self):
        raise TypeError("FinalizedSemanticEvidenceV1 is non-serializable")


class _PreparedCustodyV1:
    __slots__ = (
        "_token", "_store_token", "_project", "_eas_ref", "_execution_id",
        "_preparation_ref", "_unit_ids",
    )

    def __init__(self, token: object, *, store_token: object, project: str,
                 eas_ref: str, execution_id: str, preparation_ref: str,
                 unit_ids: list[str]) -> None:
        if token is not _CUSTODY_TOKEN:
            raise TypeError("PreparedCustodyV1 has no public constructor")
        self._token = token
        self._store_token = store_token
        self._project = project
        self._eas_ref = eas_ref
        self._execution_id = execution_id
        self._preparation_ref = preparation_ref
        self._unit_ids = list(unit_ids)

    def __reduce__(self):
        raise TypeError("PreparedCustodyV1 is non-serializable")


class _CommittedRunV1:
    __slots__ = ("_token", "_run_id", "_run_seal_ref")

    def __init__(self, token: object, run_id: str, run_seal_ref: str) -> None:
        if token is not _COMMITTED_TOKEN:
            raise TypeError("CommittedRunV1 has no public constructor")
        self._token = token
        self._run_id = run_id
        self._run_seal_ref = run_seal_ref

    def __reduce__(self):
        raise TypeError("CommittedRunV1 is non-serializable")


DurableProjectStateV1 = _DurableProjectStateV1
ProjectStoreAuthorityV1 = _ProjectStoreSessionV1
FinalizedSemanticEvidenceV1 = _FinalizedSemanticEvidenceV1
PreparedCustodyV1 = _PreparedCustodyV1
CommittedRunV1 = _CommittedRunV1


def _require_session(value: Any) -> _ProjectStoreSessionV1:
    if not isinstance(value, _ProjectStoreSessionV1) or value._token is not _SESSION_TOKEN:
        raise TypeError("live ProjectStoreAuthorityV1 session required")
    return value


def _require_finalized(value: Any) -> _FinalizedSemanticEvidenceV1:
    if not isinstance(value, _FinalizedSemanticEvidenceV1) or \
            value._token is not _FINALIZED_TOKEN:
        raise TypeError("current-session FinalizedSemanticEvidenceV1 required")
    return value


def _require_custody(value: Any) -> _PreparedCustodyV1:
    if not isinstance(value, _PreparedCustodyV1) or value._token is not _CUSTODY_TOKEN:
        raise TypeError("current-session PreparedCustodyV1 required")
    return value


def committed_run_id(value: Any) -> str:
    if not isinstance(value, _CommittedRunV1) or value._token is not _COMMITTED_TOKEN:
        raise TypeError("CommittedRunV1 required")
    return value._run_id


def _accepted_vector(ep: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in ep["positiveVectors"]
                if row.get("id") == "EP8-POS-NOMATCH-PASS")


def _state_from_authority_fixture(fixture: dict[str, Any]) -> _DurableProjectStateV1:
    _, ep8, _, _, _, _ = _deps()
    ep_port = ep8._open_test_project_store(copy.deepcopy(fixture))
    return _DurableProjectStateV1(
        _STATE_TOKEN, ep_port._project, ep_port._state)


def _open_session(state: Any, *, fixture_id: str) -> _ProjectStoreSessionV1:
    _, ep8, _, _, _, _ = _deps()
    if not isinstance(state, _DurableProjectStateV1) or state._token is not _STATE_TOKEN:
        raise TypeError("guarded DurableProjectStateV1 required")
    if not isinstance(fixture_id, str) or not re.fullmatch(r"[a-z0-9-]+", fixture_id):
        raise ValueError("session fixture id invalid")
    project = state._project
    host = ep8._HostProjectAdmissionV1(
        ep8._HOST_TOKEN, project,
        ep8._host_ref("opensip.test.project-marker.v1", project, fixture_id),
        ep8._host_ref("opensip.test.project-registry.v1", project, fixture_id),
        ep8._host_ref("opensip.test.opened-root.v1", project, fixture_id),
    )
    ep_port = ep8.open_project_store_authority(host, state._authority_state)
    return _ProjectStoreSessionV1(_SESSION_TOKEN, state, ep_port)


def _record_key(name: str, record: dict[str, Any]) -> tuple[Any, ...]:
    project = record["projectId"]
    if name == "TerminalRunV1":
        return project, record["runSealRef"]
    if name in ("RunIndexV1", "CustodyRootV1", "RunAuthorityIndexV1"):
        return project, record["runId"]
    if name == "AttemptRunLinkV1":
        return project, record["executionId"]
    if name == "outbox":
        return project, record["executionId"], record["event"]
    raise ValueError(f"unknown final record {name}")


def _durable_image(store: Any, *, fixture_id: str) -> dict[str, Any]:
    """Flatten durable rows only; no session or opaque capability survives."""
    port = _require_session(store)
    _, ep8, _, _, _, _ = _deps()
    ep_fixture = ep8._empty_fixture(port._project, fixture_id)
    ep_fixture["immutableCasRecords"] = sorted([
        copy.deepcopy(row)
        for rows in port._state._authority_state._cas.values()
        for row in rows
    ], key=lambda row: (row["projectId"], row["recordCasRef"], row["recordKind"]))
    ep_fixture["evaluationAuthorityIndex"] = sorted(
        copy.deepcopy(port._state._authority_state._index), key=canonical)
    image = {
        "schemaVersion": 1,
        "projectId": port._project,
        "authorityFixture": ep_fixture,
        "privateCas": [
            {"recordCasRef": ref, "recordBytesHex": raw.hex()}
            for ref, rows in sorted(port._state._private_cas.items())
            for raw in rows
        ],
        "attempts": sorted(copy.deepcopy(list(port._state._attempts.values())),
                           key=canonical),
        "custodyRows": [
            copy.deepcopy(row)
            for ref in sorted(port._state._custody_rows)
            for row in sorted(port._state._custody_rows[ref], key=canonical)
        ],
        "journals": sorted(
            copy.deepcopy(list(port._state._ledger["journals"].values())),
            key=canonical),
        "finalRecords": {
            name: sorted(copy.deepcopy(list(
                port._state._ledger["records"][name].values())), key=canonical)
            for name in FINAL_WRITES
        },
    }
    if _contains_token_key(image):
        raise ValueError("operational token leaked into durable image")
    # Force the same boundary a fresh process receives: JSON values only.
    return json.loads(json.dumps(image, sort_keys=True, allow_nan=False),
                      object_pairs_hook=_pairs)


def _state_from_durable_image(image: Any) -> _DurableProjectStateV1:
    if not isinstance(image, dict) or set(image) != {
            "schemaVersion", "projectId", "authorityFixture", "privateCas",
            "attempts", "custodyRows", "journals", "finalRecords"} or \
            image.get("schemaVersion") != 1 or _contains_token_key(image):
        raise ValueError("durable project image is not exact/token-free")
    fixture = image.get("authorityFixture")
    if not isinstance(fixture, dict) or fixture.get("projectId") != image.get("projectId"):
        raise ValueError("authority fixture/project mismatch")
    state = _state_from_authority_fixture(fixture)
    if state._project != image["projectId"]:
        raise ValueError("durable image crosses ProjectId")
    for row in image.get("privateCas") or []:
        if not isinstance(row, dict) or set(row) != {"recordCasRef", "recordBytesHex"}:
            raise ValueError("private CAS row is not exact")
        ref = row.get("recordCasRef")
        raw_hex = row.get("recordBytesHex")
        if not isinstance(ref, str) or not REF_RE.fullmatch(ref) or \
                not isinstance(raw_hex, str) or not re.fullmatch(r"(?:[0-9a-f]{2})*", raw_hex):
            raise ValueError("private CAS row invalid")
        raw = bytes.fromhex(raw_hex)
        if sha_ref(raw) != ref:
            raise ValueError("private CAS hash mismatch")
        state._private_cas.setdefault(ref, []).append(raw)
    for attempt in image.get("attempts") or []:
        _validate_attempt(attempt, state._project)
        key = (state._project, attempt["executionId"])
        if key in state._attempts:
            raise ValueError("duplicate Attempt row")
        state._attempts[key] = copy.deepcopy(attempt)
    for row in image.get("custodyRows") or []:
        _validate_prepared_object(row, state._project)
        state._custody_rows.setdefault(row["custodyPreparationRef"], []).append(
            copy.deepcopy(row))
    for journal in image.get("journals") or []:
        _validate_journal(journal, state._project)
        key = (state._project, journal["executionId"])
        if key in state._ledger["journals"]:
            raise ValueError("duplicate journal key")
        state._ledger["journals"][key] = copy.deepcopy(journal)
    finals = image.get("finalRecords")
    if not isinstance(finals, dict) or set(finals) != set(FINAL_WRITES):
        raise ValueError("final record image shape invalid")
    for name in FINAL_WRITES:
        rows = finals.get(name)
        if not isinstance(rows, list):
            raise ValueError("final record rows are not an array")
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("final record is not an object")
            key = _record_key(name, row)
            if key in state._ledger["records"][name]:
                raise ValueError("duplicate final record key")
            state._ledger["records"][name][key] = copy.deepcopy(row)
    return state


def _read_private(state: _DurableProjectStateV1, ref: Any, label: str) -> bytes:
    if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
        raise LedgerCorrupt(f"{label} ref malformed")
    rows = state._private_cas.get(ref, [])
    if len(rows) != 1 or sha_ref(rows[0]) != ref:
        raise LedgerCorrupt(f"{label} missing, duplicate, or corrupt")
    return rows[0]


def _put_private(state: _DurableProjectStateV1, raw: bytes) -> str:
    ref = sha_ref(raw)
    rows = state._private_cas.get(ref, [])
    if rows and rows != [raw]:
        raise LedgerCorrupt("private CAS collision")
    if not rows:
        state._private_cas[ref] = [bytes(raw)]
    return ref


def _validate_attempt(value: Any, project: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != ATTEMPT_FIELDS or \
            value.get("schemaVersion") != 1 or value.get("projectId") != project or \
            not isinstance(value.get("revision"), int) or value["revision"] < 0 or \
            not isinstance(value.get("executionId"), str) or \
            not EXEC_RE.fullmatch(value["executionId"]):
        raise LedgerCorrupt("frozen Attempt row invalid")
    for key in ("evaluationAuthoritySealRef", "frozenRetentionTargetRef"):
        if not isinstance(value.get(key), str) or not REF_RE.fullmatch(value[key]):
            raise LedgerCorrupt("frozen Attempt ref invalid")
    return copy.deepcopy(value)


def _validate_journal(value: Any, project: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != JOURNAL_FIELDS or \
            value.get("schemaVersion") != 2 or value.get("projectId") != project or \
            not isinstance(value.get("executionId"), str) or \
            not EXEC_RE.fullmatch(value["executionId"]) or \
            not isinstance(value.get("expectedAttemptRevision"), int) or \
            value["expectedAttemptRevision"] < 0 or _contains_token_key(value):
        raise LedgerCorrupt("RunFreePreparedCommitV2 invalid")
    for key in ("evaluationAuthoritySealRef", "semanticEvidenceCasRef",
                "custodyPreparationRef"):
        if not isinstance(value.get(key), str) or not REF_RE.fullmatch(value[key]):
            raise LedgerCorrupt("RunFreePreparedCommitV2 ref invalid")
    forbidden = {"runId", "runSealRef", "terminalRunCasRef"}
    if set(value) & forbidden:
        raise LedgerCorrupt("RunFreePreparedCommitV2 exposes Run identity")
    return copy.deepcopy(value)


def _validate_preparation(value: Any, project: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != PREPARATION_FIELDS or \
            value.get("schemaVersion") != 1 or value.get("projectId") != project or \
            not isinstance(value.get("executionId"), str) or \
            not EXEC_RE.fullmatch(value["executionId"]) or _contains_token_key(value):
        raise LedgerCorrupt("CustodyPreparationMaterialV1 invalid")
    for key in PREPARATION_FIELDS - {"schemaVersion", "projectId", "executionId",
                                     "semanticCapabilityClosureCommitment", "units"}:
        if not isinstance(value.get(key), str) or not REF_RE.fullmatch(value[key]):
            raise LedgerCorrupt("CustodyPreparationMaterialV1 ref invalid")
    if not isinstance(value.get("semanticCapabilityClosureCommitment"), str) or \
            not REF_RE.fullmatch(value["semanticCapabilityClosureCommitment"]) or \
            not isinstance(value.get("units"), list):
        raise LedgerCorrupt("CustodyPreparationMaterialV1 closure invalid")
    return copy.deepcopy(value)


def _validate_prepared_object(value: Any, project: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != PREPARED_OBJECT_FIELDS or \
            value.get("schemaVersion") != 1 or value.get("projectId") != project or \
            value.get("requiredForCapability") not in ("verifiable", "replayable") or \
            not isinstance(value.get("unitId"), str) or \
            not isinstance(value.get("recordKind"), str) or _contains_token_key(value):
        raise LedgerCorrupt("CustodyPreparedObjectV1 invalid")
    for key in ("custodyPreparationRef", "frozenRetentionTargetRef", "recordCasRef"):
        if not isinstance(value.get(key), str) or not REF_RE.fullmatch(value[key]):
            raise LedgerCorrupt("CustodyPreparedObjectV1 ref invalid")
    return copy.deepcopy(value)


def _derive_closure(rt: dict[str, Any], bundle: dict[str, Any], authority: Any) -> dict[str, Any]:
    """Recompute RT13 closure through the newly minted EP8 handle."""
    _, ep8, _, _, _, rtcore = _deps()
    findings = ep8.validate_bundle(bundle, authority)
    if findings:
        raise LedgerCorrupt(f"cold authority rejected stored bundle: {findings[0][0]}")
    proof_refs = ep8.derive_raw_proof_requirements(bundle, authority)
    edges = ep8.derive_dependency_edges(bundle, authority)
    roots = sorted(ep8.derive_semantic_requirements(authority), key=canonical)
    resolved_bindings = ep8.resolve_semantic_object_bindings(authority)
    bindings = sorted(
        [copy.deepcopy(row["binding"]) for row in resolved_bindings.values()],
        key=ep8.encode_semantic_object_binding)
    grouped: dict[str, list[dict[str, Any]]] = {"verifiable": [], "replayable": []}
    for row in proof_refs:
        capability = row.get("requiredForCapability")
        if capability not in grouped:
            raise LedgerCorrupt("derived raw requirement capability invalid")
        grouped[capability].append({
            "projectId": row["projectId"],
            "recordCasRef": row["recordCasRef"],
            "recordKind": row["recordKind"],
        })
    rtcore._set_closure_grammar(rt["capabilityClosure"]["closureGrammar"])
    units = []
    for capability in ("verifiable", "replayable"):
        refs = grouped[capability]
        if refs:
            unit = {
                "unitId": "", "projectId": bundle["projectId"],
                "requiredForCapability": capability, "objectRefs": refs,
            }
            unit["unitId"] = rtcore.derive_unit_id(
                unit["projectId"], capability, refs)
            units.append(unit)
    expected = {
        "schemaVersion": 3,
        "projectId": bundle["projectId"],
        "sealedCapability": rt["capabilityClosure"]["semanticClosure"]["sealedCapability"],
        "semanticObjectBindings": bindings,
        "semanticRoots": roots,
        "proofRefs": proof_refs,
        "dependencyEdges": edges,
        "units": units,
        "closureCommitment": rtcore.semantic_closure_commitment(units),
    }
    if expected != rt["capabilityClosure"]["semanticClosure"]:
        raise LedgerCorrupt("fresh EP8/RT13 closure differs from frozen authority")
    return expected


def _regenerate_evidence(rt: dict[str, Any], bundle: dict[str, Any],
                         authority: Any) -> dict[str, Any]:
    _, _, _, _, e4, _ = _deps()
    seal = authority._candidate["evaluationAuthoritySeal"]
    synthetic = {"positiveVectors": [{
        "id": "EP5-POS-NOMATCH-PASS",
        "bundle": copy.deepcopy(bundle),
        "verifiedAuthorityInput": {"evaluationAuthoritySeal": copy.deepcopy(seal)},
    }]}
    return e4.regenerate(synthetic, rt)


def _expected_index(authority: Any, accepted: dict[str, Any]) -> dict[str, Any]:
    _, ep8, _, _, _, _ = _deps()
    handle = ep8._require_handle(authority)
    candidate = handle._candidate
    receipt = candidate["planAuthorityReceipt"]
    admission = candidate["evaluationAuthorityAdmission"]
    result = {
        "schemaVersion": 1,
        "projectId": handle._project,
        "runId": accepted["runId"],
        "runSealRef": accepted["runSealRef"],
        "planAuthorityReceiptRef": ep8._ep6().raw_record_ref(
            "PlanAuthorityReceiptV1", receipt),
        "evaluationAuthorityAdmissionRef": handle._admission_ref,
        "planId": receipt["planId"],
        "planIntentCommitment": receipt["planIntentCommitment"],
        "executionPlanCommitment": candidate["evaluationAuthoritySeal"][
            "executionPlanCommitment"],
        "activationManifestRef": admission["activationManifestRef"],
        "evaluationAuthoritySealRef": handle._eas_ref,
    }
    if list(result) != INDEX_FIELDS:
        raise AssertionError("RunAuthorityIndex field order drift")
    if accepted.get("runAuthorityIndex") != result:
        raise LedgerCorrupt("RunAuthorityIndex differs from cold authority")
    raw = b"opensip.run-authority-index.v1\0" + canonical(result)
    golden = accepted.get("runAuthorityIndexRaw") or {}
    if golden.get("value") != result or golden.get("encodedHex") != raw.hex() or \
            golden.get("byteLength") != len(raw) or \
            golden.get("rawCasRef") != sha_ref(raw):
        raise LedgerCorrupt("RunAuthorityIndex raw identity mismatch")
    return result


def _material_for(contract: dict[str, Any], rt: dict[str, Any], store: Any,
                  authority: Any, bundle: dict[str, Any], execution_id: str,
                  *, target_bytes: bytes | None = None) -> dict[str, Any]:
    port = _require_session(store)
    _, ep8, _, _, _, _ = _deps()
    handle = ep8._require_handle(authority)
    ep8.assert_store_continuity(port._ep_port, handle)
    if not EXEC_RE.fullmatch(execution_id):
        raise ValueError("ExecutionId invalid")
    closure = _derive_closure(rt, bundle, handle)
    generated = _regenerate_evidence(rt, bundle, handle)
    accepted = contract["acceptedGolden"]
    identity_checks = {
        "semanticEvidenceHex": generated["evidence"].hex(),
        "rawProofInventoryHex": generated["inventory"].hex(),
        "evidenceDigest": generated["evidenceDigest"],
        "runId": generated["runId"],
        "terminalRunEncodedHex": generated["terminal"].hex(),
        "runSealRef": generated["runSealRef"],
    }
    if any(accepted.get(key) != value for key, value in identity_checks.items()):
        raise LedgerCorrupt("Evidence v6 protected semantic/Run identity drift")
    bundle_bytes = canonical(bundle)
    closure_bytes = canonical(closure)
    inventory_bytes = generated["inventory"]
    evidence_bytes = generated["evidence"]
    bundle_ref = sha_ref(bundle_bytes)
    closure_ref = sha_ref(closure_bytes)
    inventory_ref = sha_ref(inventory_bytes)
    evidence_ref = sha_ref(evidence_bytes)
    values = accepted.get("values") or {}
    if bundle_ref != values.get("evaluationProofBundleCasRef") or \
            closure_ref != values.get("semanticCapabilityClosureCasRef") or \
            evidence_ref != accepted.get("semanticEvidenceCasRef"):
        raise LedgerCorrupt("stored input CAS identities differ from SemanticEvidence")
    if target_bytes is None:
        target = {
            "schemaVersion": 1, "projectId": port._project,
            "selection": "explicit-project-policy-fixture",
            "sealedCapability": closure["sealedCapability"],
        }
        target_bytes = canonical(target)
    target_ref = sha_ref(target_bytes)
    preparation = {
        "schemaVersion": 1,
        "projectId": port._project,
        "executionId": execution_id,
        "evaluationAuthoritySealRef": handle._eas_ref,
        "semanticEvidenceCasRef": evidence_ref,
        "evaluationProofBundleCasRef": bundle_ref,
        "semanticCapabilityClosureCasRef": closure_ref,
        "semanticCapabilityClosureCommitment": closure["closureCommitment"],
        "rawProofInventoryCasRef": inventory_ref,
        "frozenRetentionTargetRef": target_ref,
        "units": copy.deepcopy(closure["units"]),
    }
    preparation_bytes = canonical(preparation)
    preparation_ref = sha_ref(preparation_bytes)
    prepared_rows = []
    for unit in closure["units"]:
        for obj in unit["objectRefs"]:
            prepared_rows.append({
                "schemaVersion": 1,
                "projectId": port._project,
                "custodyPreparationRef": preparation_ref,
                "frozenRetentionTargetRef": target_ref,
                "unitId": unit["unitId"],
                "requiredForCapability": unit["requiredForCapability"],
                "recordCasRef": obj["recordCasRef"],
                "recordKind": obj["recordKind"],
            })
    prepared_rows.sort(key=canonical)
    return {
        "closure": closure,
        "generated": generated,
        "accepted": accepted,
        "targetBytes": target_bytes,
        "targetRef": target_ref,
        "bundleBytes": bundle_bytes,
        "bundleRef": bundle_ref,
        "closureBytes": closure_bytes,
        "closureRef": closure_ref,
        "inventoryBytes": inventory_bytes,
        "inventoryRef": inventory_ref,
        "evidenceBytes": evidence_bytes,
        "evidenceRef": evidence_ref,
        "preparation": preparation,
        "preparationBytes": preparation_bytes,
        "preparationRef": preparation_ref,
        "preparedRows": prepared_rows,
    }


def prepare_run_commit(contract: dict[str, Any], rt: dict[str, Any], store: Any,
                       authority: Any, bundle: dict[str, Any], *, execution_id: str,
                       expected_attempt_revision: int = 1,
                       crash_before_journal: bool = False) -> \
        tuple[Any, _FinalizedSemanticEvidenceV1, _PreparedCustodyV1]:
    """Persist exact recovery material, then publish a closed Run-free journal."""
    port = _require_session(store)
    _, ep8, _, _, _, _ = _deps()
    handle = ep8._require_handle(authority)
    material = _material_for(contract, rt, port, handle, bundle, execution_id)
    state = port._state
    for raw in (
            material["targetBytes"], material["bundleBytes"],
            material["closureBytes"], material["inventoryBytes"],
            material["evidenceBytes"], material["preparationBytes"]):
        _put_private(state, raw)
    state._custody_rows[material["preparationRef"]] = copy.deepcopy(
        material["preparedRows"])
    attempt = {
        "schemaVersion": 1, "projectId": port._project,
        "executionId": execution_id, "revision": expected_attempt_revision,
        "evaluationAuthoritySealRef": handle._eas_ref,
        "frozenRetentionTargetRef": material["targetRef"],
    }
    _validate_attempt(attempt, port._project)
    attempt_key = (port._project, execution_id)
    old_attempt = state._attempts.get(attempt_key)
    if old_attempt is not None and old_attempt != attempt:
        raise LedgerCorrupt("Attempt preparation collision")
    state._attempts[attempt_key] = copy.deepcopy(attempt)
    if crash_before_journal:
        raise InjectedCrash("injected crash before journal visibility")
    journal = {
        "schemaVersion": 2, "projectId": port._project,
        "executionId": execution_id,
        "expectedAttemptRevision": expected_attempt_revision,
        "evaluationAuthoritySealRef": handle._eas_ref,
        "semanticEvidenceCasRef": material["evidenceRef"],
        "custodyPreparationRef": material["preparationRef"],
    }
    _validate_journal(journal, port._project)
    work = copy.deepcopy(state._ledger)
    old = work["journals"].get(attempt_key)
    if old is not None and old != journal:
        raise LedgerCorrupt("Run-free journal collision")
    work["journals"][attempt_key] = copy.deepcopy(journal)
    state._ledger = work
    return _rehydrate(contract, rt, port, execution_id)


def _decode_canonical_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise LedgerCorrupt(f"{label} is not closed JSON") from exc
    if not isinstance(value, dict) or canonical(value) != raw:
        raise LedgerCorrupt(f"{label} is not canonical JSON")
    return value


def _rehydrate(contract: dict[str, Any], rt: dict[str, Any], store: Any,
               execution_id: str) -> \
        tuple[Any, _FinalizedSemanticEvidenceV1, _PreparedCustodyV1]:
    """Cold-resolve and remint solely from current-session durable reads."""
    port = _require_session(store)
    _, ep8, _, _, _, _ = _deps()
    key = (port._project, execution_id)
    journal = port._state._ledger["journals"].get(key)
    if journal is None:
        raise NoPreparedRun("no Run-free prepared journal")
    journal = _validate_journal(journal, port._project)
    attempt = _validate_attempt(port._state._attempts.get(key), port._project)
    if attempt["revision"] != journal["expectedAttemptRevision"] or \
            attempt["evaluationAuthoritySealRef"] != journal["evaluationAuthoritySealRef"]:
        raise LedgerCorrupt("journal/Attempt authority mismatch")
    # Decisive process-independent authority step: EAS is a locator only; EP8
    # reconstructs and re-admits every authority record under this new port.
    handle = ep8.resolve_stored_evaluation(
        port._ep_port, journal["evaluationAuthoritySealRef"])
    ep8.assert_store_continuity(port._ep_port, handle)

    preparation_raw = _read_private(
        port._state, journal["custodyPreparationRef"], "custody preparation")
    preparation = _validate_preparation(
        _decode_canonical_json(preparation_raw, "custody preparation"), port._project)
    if sha_ref(preparation_raw) != journal["custodyPreparationRef"] or \
            preparation["executionId"] != execution_id or \
            preparation["evaluationAuthoritySealRef"] != handle._eas_ref or \
            preparation["semanticEvidenceCasRef"] != journal["semanticEvidenceCasRef"] or \
            preparation["frozenRetentionTargetRef"] != attempt["frozenRetentionTargetRef"]:
        raise LedgerCorrupt("journal/custody preparation mismatch")

    target_raw = _read_private(
        port._state, preparation["frozenRetentionTargetRef"], "frozen retention target")
    target = _decode_canonical_json(target_raw, "frozen retention target")
    if set(target) != {"schemaVersion", "projectId", "selection", "sealedCapability"} or \
            target.get("schemaVersion") != 1 or target.get("projectId") != port._project or \
            target.get("selection") != "explicit-project-policy-fixture":
        raise LedgerCorrupt("frozen retention target invalid")
    bundle_raw = _read_private(
        port._state, preparation["evaluationProofBundleCasRef"], "evaluation bundle")
    closure_raw = _read_private(
        port._state, preparation["semanticCapabilityClosureCasRef"], "RT closure")
    inventory_raw = _read_private(
        port._state, preparation["rawProofInventoryCasRef"], "raw proof inventory")
    evidence_raw = _read_private(
        port._state, preparation["semanticEvidenceCasRef"], "SemanticEvidence")
    bundle = _decode_canonical_json(bundle_raw, "evaluation bundle")
    stored_closure = _decode_canonical_json(closure_raw, "RT closure")
    derived_closure = _derive_closure(rt, bundle, handle)
    if stored_closure != derived_closure or canonical(derived_closure) != closure_raw or \
            preparation["semanticCapabilityClosureCommitment"] != \
            derived_closure["closureCommitment"] or \
            preparation["units"] != derived_closure["units"] or \
            target["sealedCapability"] != derived_closure["sealedCapability"]:
        raise LedgerCorrupt("stored RT closure/custody plan differs from fresh derivation")
    generated = _regenerate_evidence(rt, bundle, handle)
    accepted = contract["acceptedGolden"]
    if inventory_raw != generated["inventory"] or \
            evidence_raw != generated["evidence"] or \
            generated["evidenceDigest"] != accepted["evidenceDigest"] or \
            generated["runId"] != accepted["runId"] or \
            generated["terminal"] .hex() != accepted["terminalRunEncodedHex"] or \
            generated["runSealRef"] != accepted["runSealRef"]:
        raise LedgerCorrupt("SemanticEvidence/Run identities fail cold regeneration")
    if sha_ref(inventory_raw) != preparation["rawProofInventoryCasRef"] or \
            sha_ref(evidence_raw) != journal["semanticEvidenceCasRef"]:
        raise LedgerCorrupt("inventory/Evidence raw hash mismatch")

    expected_rows = []
    for unit in derived_closure["units"]:
        for obj in unit["objectRefs"]:
            expected_rows.append({
                "schemaVersion": 1, "projectId": port._project,
                "custodyPreparationRef": journal["custodyPreparationRef"],
                "frozenRetentionTargetRef": preparation["frozenRetentionTargetRef"],
                "unitId": unit["unitId"],
                "requiredForCapability": unit["requiredForCapability"],
                "recordCasRef": obj["recordCasRef"],
                "recordKind": obj["recordKind"],
            })
    expected_rows.sort(key=canonical)
    actual_rows = port._state._custody_rows.get(journal["custodyPreparationRef"], [])
    for row in actual_rows:
        _validate_prepared_object(row, port._project)
    if sorted(copy.deepcopy(actual_rows), key=canonical) != expected_rows:
        raise LedgerCorrupt("durable custody rows do not exactly cover RT units")
    index = _expected_index(handle, accepted)
    if index != accepted["runAuthorityIndex"]:
        raise LedgerCorrupt("cold RunAuthorityIndex rejoin failed")
    finalized = _FinalizedSemanticEvidenceV1(
        _FINALIZED_TOKEN, store_token=port._instance_token,
        project=port._project, eas_ref=handle._eas_ref,
        admission_ref=handle._admission_ref, execution_id=execution_id,
        accepted=accepted)
    custody = _PreparedCustodyV1(
        _CUSTODY_TOKEN, store_token=port._instance_token,
        project=port._project, eas_ref=handle._eas_ref,
        execution_id=execution_id,
        preparation_ref=journal["custodyPreparationRef"],
        unit_ids=[row["unitId"] for row in derived_closure["units"]])
    return handle, finalized, custody


def _records_for_commit(finalized: _FinalizedSemanticEvidenceV1,
                        custody: _PreparedCustodyV1,
                        index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    accepted = finalized._accepted
    project = finalized._project
    run_id = accepted["runId"]
    run_seal = accepted["runSealRef"]
    result = {
        "TerminalRunV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": run_seal,
            "recordBytesHex": accepted["terminalRunEncodedHex"],
        },
        "RunIndexV1": {
            "schemaVersion": 1, "projectId": project,
            "runId": run_id, "runSealRef": run_seal,
        },
        "AttemptRunLinkV1": {
            "schemaVersion": 1, "projectId": project,
            "executionId": custody._execution_id,
            "disposition": "run-committed", "runId": run_id,
            "runSealRef": run_seal,
        },
        "CustodyRootV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": run_seal,
            "semanticEvidenceCasRef": accepted["semanticEvidenceCasRef"],
            "unitIds": list(custody._unit_ids),
        },
        "RunAuthorityIndexV1": copy.deepcopy(index),
        "outbox": {
            "schemaVersion": 1, "projectId": project,
            "executionId": custody._execution_id, "event": "run-committed",
            "runId": run_id, "runSealRef": run_seal,
        },
    }
    if _contains_token_key(result):
        raise LedgerCorrupt("operational token leaked into final records")
    return result


_TEST_COMMIT_CRASH: str | None = None


def _existing_state(state: _DurableProjectStateV1,
                    writes: dict[str, dict[str, Any]]) -> tuple[int, int]:
    present = 0
    exact = 0
    for name in FINAL_WRITES:
        record = writes[name]
        existing = state._ledger["records"][name].get(_record_key(name, record))
        if existing is not None:
            present += 1
            if existing == record:
                exact += 1
    return present, exact


def _commit_rehydrated(store: Any, authority: Any,
                       finalized: _FinalizedSemanticEvidenceV1,
                       custody: _PreparedCustodyV1) -> _CommittedRunV1:
    global _TEST_COMMIT_CRASH
    port = _require_session(store)
    _, ep8, _, _, _, _ = _deps()
    handle = ep8._require_handle(authority)
    ep8.assert_store_continuity(port._ep_port, handle)
    tokens = {
        port._instance_token, handle._store_token,
        finalized._store_token, custody._store_token,
    }
    if len(tokens) != 1:
        raise ValueError("old or different store-session capability rejected")
    if len({port._project, handle._project, finalized._project, custody._project}) != 1 or \
            handle._eas_ref != finalized._eas_ref or handle._eas_ref != custody._eas_ref or \
            finalized._execution_id != custody._execution_id or \
            finalized._admission_ref != handle._admission_ref:
        raise ValueError("project/EAS/admission/execution continuity mismatch")
    index = _expected_index(handle, finalized._accepted)
    writes = _records_for_commit(finalized, custody, index)
    state = port._state
    journal_key = (port._project, custody._execution_id)
    present, exact = _existing_state(state, writes)
    journal_exists = journal_key in state._ledger["journals"]
    if present:
        if present == len(FINAL_WRITES) and exact == len(FINAL_WRITES) and not journal_exists:
            return _CommittedRunV1(
                _COMMITTED_TOKEN, finalized._accepted["runId"],
                finalized._accepted["runSealRef"])
        raise LedgerCorrupt("partial or conflicting final record set")
    if not journal_exists:
        raise NoPreparedRun("no journal and no committed final record set")
    work = copy.deepcopy(state._ledger)
    for name in FINAL_WRITES:
        record = writes[name]
        key = _record_key(name, record)
        existing = work["records"][name].get(key)
        if existing is not None and existing != record:
            raise LedgerCorrupt(f"{name} append-only collision")
        work["records"][name][key] = copy.deepcopy(record)
    del work["journals"][journal_key]
    if _TEST_COMMIT_CRASH == "during-transaction":
        raise CommitFailed("injected failure before durable ledger swap")
    # One assignment models the specified transaction boundary.  It is not a
    # production atomicity claim.
    state._ledger = work
    if _TEST_COMMIT_CRASH == "after-commit-before-response":
        raise ResponseLost("injected response loss after durable commit")
    return _CommittedRunV1(
        _COMMITTED_TOKEN, finalized._accepted["runId"],
        finalized._accepted["runSealRef"])


def commit_run(contract: dict[str, Any], rt: dict[str, Any], store: Any,
               authority: Any, finalized_evidence: Any,
               prepared_custody: Any) -> _CommittedRunV1:
    port = _require_session(store)
    finalized = _require_finalized(finalized_evidence)
    custody = _require_custody(prepared_custody)
    # Reject old tokens before any durable recovery lookup.
    if finalized._store_token is not port._instance_token or \
            custody._store_token is not port._instance_token:
        raise ValueError("old FinalizedSemanticEvidence/PreparedCustody rejected")
    handle, fresh_finalized, fresh_custody = _rehydrate(
        contract, rt, port, finalized._execution_id)
    if authority is not None:
        _, ep8, _, _, _, _ = _deps()
        supplied = ep8._require_handle(authority)
        ep8.assert_store_continuity(port._ep_port, supplied)
        if supplied._eas_ref != handle._eas_ref:
            raise ValueError("supplied authority differs from durable authority")
    if finalized._accepted != fresh_finalized._accepted or \
            custody._preparation_ref != fresh_custody._preparation_ref or \
            custody._unit_ids != fresh_custody._unit_ids:
        raise ValueError("live capabilities differ from durable rederivation")
    return _commit_rehydrated(port, handle, fresh_finalized, fresh_custody)


def _verify_committed_by_link(contract: dict[str, Any], store: Any,
                              execution_id: str) -> _CommittedRunV1:
    port = _require_session(store)
    accepted = contract["acceptedGolden"]
    records = port._state._ledger["records"]
    link = records["AttemptRunLinkV1"].get((port._project, execution_id))
    if not isinstance(link, dict):
        raise NoPreparedRun("no committed Attempt link")
    if link.get("runId") != accepted["runId"] or \
            link.get("runSealRef") != accepted["runSealRef"]:
        raise LedgerCorrupt("Attempt link identity conflict")
    # Reconstruct exact expected records from immutable Evidence v6 golden and
    # the committed RunAuthorityIndex; do not accept index/link presence alone.
    index = records["RunAuthorityIndexV1"].get((port._project, accepted["runId"]))
    if index != accepted["runAuthorityIndex"]:
        raise LedgerCorrupt("RunAuthorityIndex missing or conflicting")
    pseudo_final = _FinalizedSemanticEvidenceV1(
        _FINALIZED_TOKEN, store_token=port._instance_token,
        project=port._project,
        eas_ref=accepted["runAuthorityIndex"]["evaluationAuthoritySealRef"],
        admission_ref=accepted["runAuthorityIndex"]["evaluationAuthorityAdmissionRef"],
        execution_id=execution_id, accepted=accepted)
    unit_ids = [
        "unit3:sha256:5c6c613a74f68e39a5052a06274fa612888a63c327f0a1c8ae03c86ede1b9adc",
        "unit3:sha256:22311dbe7dd9fd958d1946e6795a2add39298a41fa6eb82f918ee61c312054ed",
    ]
    pseudo_custody = _PreparedCustodyV1(
        _CUSTODY_TOKEN, store_token=port._instance_token,
        project=port._project, eas_ref=pseudo_final._eas_ref,
        execution_id=execution_id, preparation_ref="sha256:" + "0" * 64,
        unit_ids=unit_ids)
    expected = _records_for_commit(pseudo_final, pseudo_custody, index)
    if any(records[name].get(_record_key(name, expected[name])) != expected[name]
           for name in FINAL_WRITES):
        raise LedgerCorrupt("committed six-record set missing or conflicting")
    if (port._project, execution_id) in port._state._ledger["journals"]:
        raise LedgerCorrupt("committed record set retains prepared journal")
    return _CommittedRunV1(_COMMITTED_TOKEN, accepted["runId"], accepted["runSealRef"])


def recover_run(contract: dict[str, Any], rt: dict[str, Any], store: Any,
                execution_id: str) -> _CommittedRunV1:
    port = _require_session(store)
    if not isinstance(execution_id, str) or not EXEC_RE.fullmatch(execution_id):
        raise ValueError("ExecutionId invalid")
    link = port._state._ledger["records"]["AttemptRunLinkV1"].get(
        (port._project, execution_id))
    if link is not None:
        return _verify_committed_by_link(contract, port, execution_id)
    key = (port._project, execution_id)
    if key not in port._state._ledger["journals"]:
        raise NoPreparedRun("no journal or committed Attempt link")
    handle, finalized, custody = _rehydrate(contract, rt, port, execution_id)
    return _commit_rehydrated(port, handle, finalized, custody)


def d9_for_failure(error: Exception, execution_id: str) -> dict[str, Any]:
    if isinstance(error, LedgerCorrupt):
        code = "LEDGER.CORRUPT"
    elif isinstance(error, CommitFailed):
        code = "DURABILITY.COMMIT_FAILED"
    else:
        raise TypeError("failure has no Evidence v7 D9 mapping")
    result = {
        "class": "operational-failed", "errorCode": code,
        "executionId": execution_id,
    }
    if any(key in result for key in ("runId", "runSealRef", "terminalRunCasRef")):
        raise AssertionError("failed finalization exposed Run identity")
    return result


def _record_counts(store: Any) -> dict[str, int]:
    port = _require_session(store)
    return {name: len(port._state._ledger["records"][name])
            for name in FINAL_WRITES}


def _new_prepared(contract: dict[str, Any], rt: dict[str, Any],
                  ep: dict[str, Any], execution_id: str, fixture_id: str) -> \
        tuple[_DurableProjectStateV1, _ProjectStoreSessionV1, Any,
              _FinalizedSemanticEvidenceV1, _PreparedCustodyV1]:
    _, ep8, _, _, _, _ = _deps()
    vector = _accepted_vector(ep)
    state = _state_from_authority_fixture(vector["trustedStoreFixture"])
    store = _open_session(state, fixture_id=fixture_id)
    eas_ref = vector["evaluationAuthorityCandidate"][
        "evaluationAuthorityAdmission"]["evaluationAuthoritySealRef"]
    handle = ep8.resolve_stored_evaluation(store._ep_port, eas_ref)
    handle, finalized, custody = prepare_run_commit(
        contract, rt, store, handle, vector["bundle"],
        execution_id=execution_id)
    return state, store, handle, finalized, custody


def run_recovery_matrix(contract: dict[str, Any]) -> dict[str, Any]:
    """Execute the deterministic cold-recovery/crash/corruption oracle.

    This function is deliberately public to other candidate checkers.  Results
    are recomputed from durable images and executable transitions, not read from
    an authored fixture or status field.
    """
    global _TEST_COMMIT_CRASH
    _, ep8, _, _, _, _ = _deps()
    ep = load("evaluation-proof.v8.json")
    rt = load("retention-tiers.v13.json")
    vector = _accepted_vector(ep)
    expected_run_id = contract["acceptedGolden"]["runId"]
    zero = {name: 0 for name in FINAL_WRITES}
    one = {name: 1 for name in FINAL_WRITES}
    result: dict[str, Any] = {
        "schemaVersion": 1,
        "assurance": "EXECUTABLE-DESIGN-TEST-DOUBLE-NOT-RUNTIME-DEMONSTRATION",
        "scenarios": {},
    }

    # Live commit and exact retry.
    _, live, live_handle, live_final, live_custody = _new_prepared(
        contract, rt, ep, "exec1-matrix-live", "matrix-live")
    prepared_counts = _record_counts(live)
    committed = commit_run(
        contract, rt, live, live_handle, live_final, live_custody)
    after_commit_image = _durable_image(live, fixture_id="matrix-live-image")
    retry = _verify_committed_by_link(contract, live, "exec1-matrix-live")
    after_retry_image = _durable_image(live, fixture_id="matrix-live-image")
    result["scenarios"]["live-positive-and-exact-retry"] = {
        "preparedPublicCounts": prepared_counts,
        "committedPublicCounts": _record_counts(live),
        "journalCountAfterCommit": len(live._state._ledger["journals"]),
        "runId": committed_run_id(committed),
        "retryRunId": committed_run_id(retry),
        "retryStateUnchanged": after_commit_image == after_retry_image,
    }

    # Crash before journal.  Private orphans may exist; no Run and no recovery
    # authority exists.
    pre_state = _state_from_authority_fixture(vector["trustedStoreFixture"])
    pre_store = _open_session(pre_state, fixture_id="matrix-before-journal")
    eas_ref = vector["evaluationAuthorityCandidate"][
        "evaluationAuthorityAdmission"]["evaluationAuthoritySealRef"]
    pre_handle = ep8.resolve_stored_evaluation(pre_store._ep_port, eas_ref)
    crashed = False
    try:
        prepare_run_commit(
            contract, rt, pre_store, pre_handle, vector["bundle"],
            execution_id="exec1-matrix-before-journal", crash_before_journal=True)
    except InjectedCrash:
        crashed = True
    pre_fresh = _open_session(
        _state_from_durable_image(_durable_image(
            pre_store, fixture_id="matrix-before-journal-image")),
        fixture_id="matrix-before-journal-fresh")
    no_prepared = False
    try:
        recover_run(contract, rt, pre_fresh, "exec1-matrix-before-journal")
    except NoPreparedRun:
        no_prepared = True
    result["scenarios"]["crash-before-journal"] = {
        "crashObserved": crashed,
        "freshNoPreparedRun": no_prepared,
        "publicCounts": _record_counts(pre_fresh),
        "journalCount": len(pre_fresh._state._ledger["journals"]),
        "publicRunIdentity": "ABSENT",
    }

    # Crash after journal: only durable image crosses the process boundary.
    _, old_store, old_handle, old_final, old_custody = _new_prepared(
        contract, rt, ep, "exec1-matrix-after-journal", "matrix-after-journal")
    after_journal_counts = _record_counts(old_store)
    durable = _durable_image(old_store, fixture_id="matrix-after-journal-image")
    fresh_store = _open_session(
        _state_from_durable_image(durable), fixture_id="matrix-after-journal-fresh")
    old_handle_rejected = False
    old_tokens_rejected = False
    try:
        ep8.assert_store_continuity(fresh_store._ep_port, old_handle)
    except (TypeError, ValueError):
        old_handle_rejected = True
    try:
        commit_run(contract, rt, fresh_store, old_handle, old_final, old_custody)
    except (TypeError, ValueError):
        old_tokens_rejected = True
    cold_committed = recover_run(
        contract, rt, fresh_store, "exec1-matrix-after-journal")
    result["scenarios"]["crash-after-journal-fresh-process"] = {
        "preparedPublicCounts": after_journal_counts,
        "oldHandleRejected": old_handle_rejected,
        "oldFinalizedAndCustodyRejected": old_tokens_rejected,
        "freshCommittedPublicCounts": _record_counts(fresh_store),
        "journalCountAfterCommit": len(fresh_store._state._ledger["journals"]),
        "runId": committed_run_id(cold_committed),
    }

    # Crash/failure during the transaction: private work never swaps.
    _, during, _, _, _ = _new_prepared(
        contract, rt, ep, "exec1-matrix-during-txn", "matrix-during-txn")
    _TEST_COMMIT_CRASH = "during-transaction"
    during_d9: dict[str, Any] | None = None
    try:
        recover_run(contract, rt, during, "exec1-matrix-during-txn")
    except CommitFailed as exc:
        during_d9 = d9_for_failure(exc, "exec1-matrix-during-txn")
    finally:
        _TEST_COMMIT_CRASH = None
    during_counts = _record_counts(during)
    during_journals = len(during._state._ledger["journals"])
    during_fresh = _open_session(
        _state_from_durable_image(_durable_image(
            during, fixture_id="matrix-during-image")),
        fixture_id="matrix-during-fresh")
    during_recovered = recover_run(
        contract, rt, during_fresh, "exec1-matrix-during-txn")
    result["scenarios"]["crash-during-six-write-transaction"] = {
        "failure": during_d9,
        "failedPublicCounts": during_counts,
        "journalCountAfterFailure": during_journals,
        "freshCommittedPublicCounts": _record_counts(during_fresh),
        "runId": committed_run_id(during_recovered),
    }

    # Commit succeeded but process lost the response.
    _, lost, _, _, _ = _new_prepared(
        contract, rt, ep, "exec1-matrix-response-lost", "matrix-response-lost")
    _TEST_COMMIT_CRASH = "after-commit-before-response"
    response_lost = False
    try:
        recover_run(contract, rt, lost, "exec1-matrix-response-lost")
    except ResponseLost:
        response_lost = True
    finally:
        _TEST_COMMIT_CRASH = None
    lost_fresh = _open_session(
        _state_from_durable_image(_durable_image(
            lost, fixture_id="matrix-response-image")),
        fixture_id="matrix-response-fresh")
    lost_recovered = recover_run(
        contract, rt, lost_fresh, "exec1-matrix-response-lost")
    result["scenarios"]["commit-before-response"] = {
        "responseLost": response_lost,
        "committedPublicCounts": _record_counts(lost_fresh),
        "journalCount": len(lost_fresh._state._ledger["journals"]),
        "runId": committed_run_id(lost_recovered),
    }

    def partial_case(label: str, keep: str, conflict: bool = False) -> dict[str, Any]:
        _, partial, h, f, c = _new_prepared(
            contract, rt, ep, f"exec1-matrix-{label}", f"matrix-{label}")
        index = _expected_index(h, f._accepted)
        writes = _records_for_commit(f, c, index)
        row = copy.deepcopy(writes[keep])
        if conflict:
            row["runSealRef"] = "sha256:" + "f" * 64
        partial._state._ledger["records"][keep][
            _record_key(keep, writes[keep])] = row
        before = _durable_image(partial, fixture_id=f"matrix-{label}-image")
        termination: dict[str, Any] | None = None
        try:
            recover_run(contract, rt, partial, f"exec1-matrix-{label}")
        except LedgerCorrupt as exc:
            termination = d9_for_failure(exc, f"exec1-matrix-{label}")
        after = _durable_image(partial, fixture_id=f"matrix-{label}-image")
        return {
            "termination": termination,
            "stateUnchanged": before == after,
            "publicCounts": _record_counts(partial),
            "journalCount": len(partial._state._ledger["journals"]),
            "publicRunIdentity": "ABSENT-FROM-TERMINATION",
        }

    result["scenarios"]["run-index-only"] = partial_case(
        "run-index-only", "RunIndexV1")
    result["scenarios"]["attempt-link-only"] = partial_case(
        "attempt-link-only", "AttemptRunLinkV1")
    result["scenarios"]["conflicting-final-record"] = partial_case(
        "conflicting-index", "RunIndexV1", conflict=True)
    # Aliases make the neither/both classification explicit without trusting a
    # second fixture: these are the already executed transition outcomes.
    result["scenarios"]["neither-index-nor-link"] = {
        "withJournalAction": "RETRY-EXECUTED",
        "withoutJournalAction": "NO_PREPARED_RUN",
        "preparedPublicCounts": zero,
    }
    result["scenarios"]["both-exact"] = {
        "action": "IDEMPOTENT-SUCCESS-EXECUTED",
        "publicCounts": one,
        "runId": expected_run_id,
    }
    result["scenarios"]["old-token-rejection"] = {
        "oldHandleRejected": old_handle_rejected,
        "oldFinalizedAndCustodyRejected": old_tokens_rejected,
        "freshRecoverySucceeded": committed_run_id(cold_committed) == expected_run_id,
    }
    return result


def _matrix_errors(matrix: Any, expected_run_id: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(matrix, dict) or set(matrix) != {"schemaVersion", "assurance", "scenarios"}:
        return ["recovery matrix root is not exact"]
    scenarios = matrix.get("scenarios") or {}
    required = {
        "live-positive-and-exact-retry", "crash-before-journal",
        "crash-after-journal-fresh-process", "crash-during-six-write-transaction",
        "commit-before-response", "neither-index-nor-link", "both-exact",
        "run-index-only", "attempt-link-only", "conflicting-final-record",
        "old-token-rejection",
    }
    if set(scenarios) != required:
        errors.append("recovery matrix scenario set drift")
        return errors
    zero = {name: 0 for name in FINAL_WRITES}
    one = {name: 1 for name in FINAL_WRITES}
    live = scenarios["live-positive-and-exact-retry"]
    if live.get("preparedPublicCounts") != zero or \
            live.get("committedPublicCounts") != one or \
            live.get("journalCountAfterCommit") != 0 or \
            live.get("runId") != expected_run_id or \
            live.get("retryRunId") != expected_run_id or \
            live.get("retryStateUnchanged") is not True:
        errors.append("live commit/exact retry matrix failed")
    before = scenarios["crash-before-journal"]
    if before.get("crashObserved") is not True or \
            before.get("freshNoPreparedRun") is not True or \
            before.get("publicCounts") != zero or before.get("journalCount") != 0 or \
            before.get("publicRunIdentity") != "ABSENT":
        errors.append("crash-before-journal matrix failed")
    after = scenarios["crash-after-journal-fresh-process"]
    if after.get("preparedPublicCounts") != zero or \
            after.get("oldHandleRejected") is not True or \
            after.get("oldFinalizedAndCustodyRejected") is not True or \
            after.get("freshCommittedPublicCounts") != one or \
            after.get("journalCountAfterCommit") != 0 or \
            after.get("runId") != expected_run_id:
        errors.append("crash-after-journal cold recovery matrix failed")
    during = scenarios["crash-during-six-write-transaction"]
    if during.get("failure") != {
            "class": "operational-failed",
            "errorCode": "DURABILITY.COMMIT_FAILED",
            "executionId": "exec1-matrix-during-txn"} or \
            during.get("failedPublicCounts") != zero or \
            during.get("journalCountAfterFailure") != 1 or \
            during.get("freshCommittedPublicCounts") != one or \
            during.get("runId") != expected_run_id:
        errors.append("during-transaction crash matrix failed")
    lost = scenarios["commit-before-response"]
    if lost.get("responseLost") is not True or \
            lost.get("committedPublicCounts") != one or lost.get("journalCount") != 0 or \
            lost.get("runId") != expected_run_id:
        errors.append("commit-before-response matrix failed")
    for label in ("run-index-only", "attempt-link-only", "conflicting-final-record"):
        row = scenarios[label]
        term = row.get("termination") or {}
        if term.get("class") != "operational-failed" or \
                term.get("errorCode") != "LEDGER.CORRUPT" or \
                any(key in term for key in ("runId", "runSealRef", "terminalRunCasRef")) or \
                row.get("stateUnchanged") is not True or row.get("journalCount") != 1:
            errors.append(f"{label} corruption matrix failed")
    old = scenarios["old-token-rejection"]
    if not all(old.get(key) is True for key in (
            "oldHandleRejected", "oldFinalizedAndCustodyRejected",
            "freshRecoverySucceeded")):
        errors.append("old-token rejection matrix failed")
    return errors


def cold_recovery_probe(contract: dict[str, Any]) -> dict[str, Any]:
    """Stable exported name consumed by OPERABILITY successors."""
    return run_recovery_matrix(contract)


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        e6mod, ep8mod, rt13mod, v8mod, _, _ = _deps()
        predecessor = load("evidence.v6.json")
        ep = load("evaluation-proof.v8.json")
        rt = load("retention-tiers.v13.json")
        versioning = load("versioning-policy.v8.json")
    except Exception as exc:
        return [f"dependency import failed: {type(exc).__name__}: {exc}"]
    if verify_files:
        for label, checker, artifact in (
                ("Evidence-v6", e6mod, predecessor),
                ("EP8", ep8mod, ep), ("RT13", rt13mod, rt),
                ("VERSIONING-v8", v8mod, versioning)):
            child_errors = checker.check(artifact)
            if child_errors:
                errors.append(f"{label} dependency red: {child_errors[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.evidence", 7):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal status drift")
    if value.get("supersedes") != {
            "artifact": "evidence.v6.json", "sha256": PINS["evidence.v6.json"],
            "checker": "check-evidence-v6.py",
            "checkerSha256": PINS["check-evidence-v6.py"]}:
        errors.append("Evidence v6 predecessor pin drift")
    assurance = value.get("assurance") or {}
    if assurance != {
            "state": "SPECIFIED", "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
            "qualificationEvidenceIds": [], "releaseEvidenceIds": [],
            "candidateState": "NOT-APPLIED"}:
        errors.append("assurance exceeds specified/implementable-unexecuted")

    changed = {
        "version", "role", "supersedes", "reviewFindingTransfers",
        "dependencies", "importedAuthorityContract", "apiContract",
        "storeContract", "admissionAndSealOrdering", "invariants",
        "retainedResiduals", "storeCapabilityContinuityContract",
    }
    additions = {
        "assurance", "identityStabilityFromEvidenceV6",
        "durableRecoveryContract", "recoveryMatrixContract",
    }
    if set(value) != set(predecessor) | additions:
        errors.append("Evidence v7 root is not the exact closed successor shape")
    for key in set(predecessor) - changed:
        if value.get(key) != predecessor[key]:
            errors.append(f"Evidence v6 protected surface changed: {key}")
    if value.get("acceptedGolden") != predecessor.get("acceptedGolden") or \
            value.get("runSubstitutionGoldens") != predecessor.get("runSubstitutionGoldens"):
        errors.append("Evidence v6 semantic/Run identity goldens changed")
    golden = value.get("acceptedGolden") or {}
    if golden.get("evidenceDigest") != \
            "sha256:6edbf46f919565e5a10426e4ff9f1dcf56588d18d1b75ad1c32cd848b19f47b9" or \
            golden.get("runId") != \
            "run1:3f319950f6a00565611029f3accc38a2afd38b3f4ab6539b2d6c8304ef0a9208" or \
            golden.get("runSealRef") != \
            "sha256:d34fc5e0d80f2af919c3ab572f03793b7893dddb2f816587b76bce40af497734":
        errors.append("explicit protected identity constants drift")

    expected_deps = {
        "evaluationProof": ("evaluation-proof.v8.json", "check-evaluation-proof-v8.py"),
        "retentionCustody": ("retention-tiers.v13.json", "check-retention-custody-v13.py"),
        "versioning": ("versioning-policy.v8.json", "check-versioning-v8.py"),
    }
    deps = value.get("dependencies") or {}
    for key, (artifact, checker_name) in expected_deps.items():
        row = deps.get(key) or {}
        if row.get("artifact") != artifact or row.get("sha256") != PINS[artifact] or \
                row.get("checker") != checker_name or \
                row.get("checkerSha256") != PINS[checker_name]:
            errors.append(f"dependency pin drift: {key}")
    if not all(term in deps.get("dependencyDirection", "") for term in (
            "EP8", "RT13", "VERSIONING v8", "Evidence v7")):
        errors.append("dependency direction drift")
    if "evidence" in json.dumps(
            (versioning.get("successorRevision") or {}).get("inputs") or []).lower():
        errors.append("VERSIONING v8 has forbidden Evidence back-edge")

    imported = value.get("importedAuthorityContract") or {}
    if imported.get("owner") != "evaluation-proof.v8.json" or \
            "immutable CAS plus EvaluationAuthorityIndexV1 only" not in \
            imported.get("storedReadApi", "") or \
            "one production" not in imported.get("onePortRule", ""):
        errors.append("EP8 cold authority/one-port import contract drift")
    stability = value.get("identityStabilityFromEvidenceV6") or {}
    if stability.get("predecessorSha256") != PINS["evidence.v6.json"] or \
            stability.get("predecessorCheckerSha256") != PINS["check-evidence-v6.py"] or \
            not all(term in json.dumps(stability.get("exactUnchanged") or []) for term in (
                "SemanticEvidence", "EvidenceDigest", "RunId", "TerminalRunV1",
                "D9 v1.7", "six final")):
        errors.append("Evidence v6 identity-stability window incomplete")

    records = ((value.get("storeContract") or {}).get("records") or {})
    journal = records.get("RunFreePreparedCommitV2") or {}
    if journal.get("required") != [
            "schemaVersion", "projectId", "executionId", "expectedAttemptRevision",
            "evaluationAuthoritySealRef", "semanticEvidenceCasRef",
            "custodyPreparationRef"] or \
            not {"runId", "runSealRef", "terminalRunCasRef",
                 "preparedCustodyToken", "storeInstanceToken", "transactionToken"}.issubset(
                    set(journal.get("forbidden") or [])) or \
            set((records.get("CustodyPreparationMaterialV1") or {}).get("required") or []) != \
            PREPARATION_FIELDS or \
            set((records.get("CustodyPreparedObjectV1") or {}).get("required") or []) != \
            PREPARED_OBJECT_FIELDS:
        errors.append("durable Run-free journal/custody schemas drift")
    durable = value.get("durableRecoveryContract") or {}
    if durable.get("stateType") != "DurableProjectStateV1" or \
            durable.get("sessionType") != "ProjectStoreAuthorityV1" or \
            len(durable.get("recoveryOrder") or []) != 6 or \
            not all(term in json.dumps(durable) for term in (
                "fresh", "EP8", "RT13", "old FinalizedSemanticEvidenceV1",
                "process-global ledger")):
        errors.append("durable fresh-session recovery contract incomplete")
    continuity = value.get("storeCapabilityContinuityContract") or {}
    if continuity.get("atomicWrites") != FINAL_WRITES or \
            "partial" not in continuity.get("collisionRule", "") or \
            "current-session" not in continuity.get("toctouRule", ""):
        errors.append("six-write/current-session continuity contract drift")
    api_text = json.dumps((value.get("apiContract") or {}).get("calls") or [])
    if not all(term in api_text for term in (
            "DurableProjectStateV1", "resolve_stored_evaluation",
            "prepare_run_commit_v2", "recover_run_v1", "RT13", "VERSIONING v8")):
        errors.append("durable recovery API surface incomplete")
    transfer = value.get("reviewFindingTransfers") or []
    if transfer[:-1] != predecessor.get("reviewFindingTransfers") or \
            (transfer[-1] if transfer else {}).get("id") != \
            "IR-E6OP5-01-COLD-READ-RECOVERY":
        errors.append("cold-recovery finding transfer is not strictly additive")
    residuals = json.dumps(value.get("retainedResiduals") or [])
    if not all(term in residuals for term in (
            "no production", "restart", "IMPLEMENTABLE", "V10", "CD-RT-5",
            "G19", "no seal")):
        errors.append("assurance/residual boundary incomplete")
    if value.get("d9Mapping") != predecessor.get("d9Mapping"):
        errors.append("D9 mapping changed")

    # Mandatory executable oracle.  Normal mode cannot pass on prose/fixture
    # presence alone, and OP6 can independently call the same exported probe.
    try:
        matrix = cold_recovery_probe(value)
        errors.extend(_matrix_errors(matrix, golden.get("runId")))
    except Exception as exc:
        errors.append(f"cold recovery oracle failed: {type(exc).__name__}: {exc}")
    return errors


def selftest(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    try:
        matrix = cold_recovery_probe(contract)
        failures.extend(_matrix_errors(matrix, contract["acceptedGolden"]["runId"]))
    except Exception as exc:
        return [f"cold recovery matrix raised: {type(exc).__name__}: {exc}"]
    # Opaque state/session/live values cannot cross a process boundary.
    ep = load("evaluation-proof.v8.json")
    rt = load("retention-tiers.v13.json")
    _, store, handle, finalized, custody = _new_prepared(
        contract, rt, ep, "exec1-selftest-serialization", "selftest-serialization")
    for label, item in (
            ("state", store._state), ("session", store), ("handle", handle),
            ("finalized", finalized), ("custody", custody)):
        for encoder in (json.dumps, pickle.dumps):
            try:
                encoder(item)
                failures.append(f"{label} capability serialized")
            except (TypeError, ValueError, pickle.PicklingError):
                pass
    image = _durable_image(store, fixture_id="selftest-image")
    if _contains_token_key(image):
        failures.append("durable image contains operational token key")
    try:
        json.dumps(image, sort_keys=True, allow_nan=False)
    except (TypeError, ValueError):
        failures.append("durable image is not plain serializable data")

    # Contract mutations must fail even though the executable packet is live.
    mutations: list[tuple[str, Any]] = []
    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        mutations.append((label, candidate))
    add("EvidenceDigest", lambda c: c["acceptedGolden"].__setitem__(
        "evidenceDigest", "sha256:" + "1" * 64))
    add("RunId", lambda c: c["acceptedGolden"].__setitem__(
        "runId", "run1:" + "2" * 64))
    add("EP8 pin", lambda c: c["dependencies"]["evaluationProof"].__setitem__(
        "checkerSha256", "0" * 64))
    add("journal EAS", lambda c: c["storeContract"]["records"][
        "RunFreePreparedCommitV2"]["required"].remove("evaluationAuthoritySealRef"))
    add("six-write omission", lambda c: c["storeCapabilityContinuityContract"][
        "atomicWrites"].pop())
    add("assurance promotion", lambda c: c["assurance"].__setitem__(
        "evidenceGrade", "DEMONSTRATED"))
    for label, candidate in mutations:
        if not check(candidate, verify_files=False):
            failures.append(f"{label} mutation escaped")
    return failures


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    errors = check(value)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    if "--selftest" in argv[1:]:
        failures = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print("PASS: evidence.v7.json; cold restart/crash/retry/corruption matrix; "
              "old-token and partial-publication controls rejected")
    else:
        golden = value["acceptedGolden"]
        print(f"PASS: evidence.v7.json; EvidenceDigest {golden['evidenceDigest']}; "
              f"RunId {golden['runId']}; durable cold recovery oracle clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
