#!/usr/bin/env python3
"""Evidence v6 identity and same-store atomic-finalization checker.

Evidence v6 preserves every Evidence v5 content identity.  Its only semantic
change is operational authority: commit_run requires the exact EP7
ProjectStoreAuthorityV1 instance that minted the admitted EAS handle, rereads
the immutable authority index/CAS immediately before publication, and commits
Terminal/RunIndex/AttemptLink/CustodyRoot/RunAuthorityIndex/outbox together.

The ledger below is a guarded in-memory executable specification.  It is not a
production store/transaction or atomicity demonstration.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import pickle
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evidence.v6.json"
PINS = {
    "evidence.v5.json": "833d2dd69276363d2951f69eb1665e12a8e87d7e433a24aaf085753013903351",
    "check-evidence-v5.py": "fc2017ffbe70f46b18c19a41688b1e7fd037dd9b174308ae63ae53d7b703abf3",
    "evaluation-proof.v7.json": "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
    "check-evaluation-proof-v7.py": "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4",
    "retention-tiers.v12.json": "1a034746512de51605b7a4bcc4fb0936bdc167db057a3018be74a2a047376dab",
    "check-retention-custody-v12.py": "104a8f9bd01e92226c11c41c234358b5a9d991b42cf12ec9318582ed12b57851",
    "versioning-policy.v7.json": "0c0f2d7396c32854c3cd5a6aff794c6a0e1be2ffe833816f9ff66f0089b49985",
    "check-versioning-v7.py": "27cc2e22dd909de2ee3050387f87129477ee050e5b25c541dcf305902fbb9d76",
}
INDEX_FIELDS = [
    "schemaVersion", "projectId", "runId", "runSealRef",
    "planAuthorityReceiptRef", "evaluationAuthorityAdmissionRef", "planId",
    "planIntentCommitment", "executionPlanCommitment", "activationManifestRef",
    "evaluationAuthoritySealRef",
]
FINAL_WRITES = [
    "TerminalRunV1", "RunIndexV1", "AttemptRunLinkV1", "CustodyRootV1",
    "RunAuthorityIndexV1", "outbox",
]
OPERATIONAL_TOKEN_KEYS = {
    "storeInstanceToken", "transactionToken", "continuityToken",
    "indexGeneration", "ProjectStoreAuthorityV1",
}


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
    return json.loads(path.read_text())


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


def _has_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(set(value) & OPERATIONAL_TOKEN_KEYS) or any(
            _has_forbidden_key(child) for child in value.values())
    if isinstance(value, list):
        return any(_has_forbidden_key(child) for child in value)
    return False


_E5: Any = None
_EP7: Any = None
_RT12: Any = None
_V7: Any = None


def _deps() -> tuple[Any, Any, Any, Any]:
    global _E5, _EP7, _RT12, _V7
    for filename, expected in PINS.items():
        actual = sha_file(filename)
        if actual != expected:
            raise ValueError(f"pinned input drift: {filename} {actual} != {expected}")
    if _E5 is None:
        _E5 = module("check-evidence-v5.py", "evidence_v5_pinned_for_v6")
    if _EP7 is None:
        _EP7 = module("check-evaluation-proof-v7.py", "ep7_pinned_for_evidence_v6")
    if _RT12 is None:
        _RT12 = module("check-retention-custody-v12.py", "rt12_pinned_for_evidence_v6")
    if _V7 is None:
        _V7 = module("check-versioning-v7.py", "versioning_v7_pinned_for_evidence_v6")
    return _E5, _EP7, _RT12, _V7


_FINALIZED_TOKEN = object()
_CUSTODY_TOKEN = object()
_COMMITTED_TOKEN = object()


class _FinalizedSemanticEvidenceV1:
    __slots__ = ("_token", "_store_token", "_project", "_eas_ref", "_admission_ref", "_accepted")

    def __init__(self, token: object, *, store_token: object, project: str,
                 eas_ref: str, admission_ref: str, accepted: dict[str, Any]) -> None:
        if token is not _FINALIZED_TOKEN:
            raise TypeError("FinalizedSemanticEvidenceV1 has no public constructor")
        self._token = token
        self._store_token = store_token
        self._project = project
        self._eas_ref = eas_ref
        self._admission_ref = admission_ref
        self._accepted = copy.deepcopy(accepted)

    def __reduce__(self):
        raise TypeError("FinalizedSemanticEvidenceV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque FinalizedSemanticEvidenceV1>"


class _PreparedCustodyV1:
    __slots__ = ("_token", "_store_token", "_project", "_eas_ref", "_execution_id", "_unit_ids")

    def __init__(self, token: object, *, store_token: object, project: str,
                 eas_ref: str, execution_id: str, unit_ids: list[str]) -> None:
        if token is not _CUSTODY_TOKEN:
            raise TypeError("PreparedCustodyV1 has no public constructor")
        self._token = token
        self._store_token = store_token
        self._project = project
        self._eas_ref = eas_ref
        self._execution_id = execution_id
        self._unit_ids = list(unit_ids)

    def __reduce__(self):
        raise TypeError("PreparedCustodyV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque PreparedCustodyV1>"


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

    def __repr__(self) -> str:
        return "<opaque CommittedRunV1>"


FinalizedSemanticEvidenceV1 = _FinalizedSemanticEvidenceV1
PreparedCustodyV1 = _PreparedCustodyV1
CommittedRunV1 = _CommittedRunV1


class _RunLedger:
    __slots__ = ("records",)

    def __init__(self) -> None:
        self.records: dict[str, dict[tuple[Any, ...], dict[str, Any]]] = {
            name: {} for name in FINAL_WRITES
        }


_LEDGERS: dict[object, _RunLedger] = {}
_TEST_BEFORE_PUBLISH_HOOK: Any = None


def _ledger_for(store: Any) -> _RunLedger:
    _, ep7, _, _ = _deps()
    port = ep7._require_store(store)
    return _LEDGERS.setdefault(port._instance_token, _RunLedger())


def _ledger_snapshot(store: Any) -> dict[str, Any]:
    return copy.deepcopy(_ledger_for(store).records)


def _accepted_vector(ep: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in ep["positiveVectors"]
                if row.get("id") == "EP7-POS-NOMATCH-PASS")


def _prepare_accepted_run(contract: dict[str, Any], rt: dict[str, Any], store: Any,
                          authority: Any, *, execution_id: str = "exec1-evidence-v6-test") -> \
        tuple[_FinalizedSemanticEvidenceV1, _PreparedCustodyV1]:
    """Fixture-only constructor for already validated/finalized E5-identical data."""
    _, ep7, _, _ = _deps()
    port = ep7._require_store(store)
    handle = ep7._require_handle(authority)
    ep7.assert_store_continuity(port, handle)
    accepted = contract.get("acceptedGolden")
    if not isinstance(accepted, dict):
        raise ValueError("accepted golden absent")
    values = accepted.get("values") or {}
    if values.get("projectId") != handle._project or \
            values.get("evaluationAuthoritySealRef") != handle._eas_ref:
        raise ValueError("finalized evidence differs from admitted authority")
    if not isinstance(execution_id, str) or not execution_id.startswith("exec1-"):
        raise ValueError("fixture execution id invalid")
    units = (rt.get("capabilityClosure") or {}).get("semanticClosure", {}).get("units") or []
    unit_ids = [row.get("unitId") for row in units]
    if len(unit_ids) != 2 or any(not isinstance(item, str) for item in unit_ids):
        raise ValueError("prepared custody lacks exact RT12 units")
    finalized = _FinalizedSemanticEvidenceV1(
        _FINALIZED_TOKEN, store_token=port._instance_token, project=handle._project,
        eas_ref=handle._eas_ref, admission_ref=handle._admission_ref,
        accepted=accepted)
    custody = _PreparedCustodyV1(
        _CUSTODY_TOKEN, store_token=port._instance_token, project=handle._project,
        eas_ref=handle._eas_ref, execution_id=execution_id, unit_ids=unit_ids)
    return finalized, custody


def _require_finalized(value: Any) -> _FinalizedSemanticEvidenceV1:
    if not isinstance(value, _FinalizedSemanticEvidenceV1) or value._token is not _FINALIZED_TOKEN:
        raise TypeError("module-finalized FinalizedSemanticEvidenceV1 required")
    return value


def _require_custody(value: Any) -> _PreparedCustodyV1:
    if not isinstance(value, _PreparedCustodyV1) or value._token is not _CUSTODY_TOKEN:
        raise TypeError("store-prepared PreparedCustodyV1 required")
    return value


def _rehash_finalized(finalized: _FinalizedSemanticEvidenceV1, authority: Any) -> dict[str, Any]:
    _, ep7, _, _ = _deps()
    accepted = finalized._accepted
    values = accepted.get("values") or {}
    checks = (
        ("rawProofInventoryHex", "rawProofInventoryLength"),
        ("semanticEvidenceHex", "semanticEvidenceLength"),
        ("evidenceDigestPreimageHex", "evidenceDigestPreimageLength"),
        ("runIdentityRecordHex", "runIdentityRecordLength"),
        ("runDomainPreimageHex", "runDomainPreimageLength"),
        ("terminalRunEncodedHex", "terminalRunLength"),
    )
    decoded: dict[str, bytes] = {}
    for hex_key, length_key in checks:
        raw_hex = accepted.get(hex_key)
        if not isinstance(raw_hex, str):
            raise ValueError(f"{hex_key} missing")
        try:
            raw = bytes.fromhex(raw_hex)
        except ValueError as exc:
            raise ValueError(f"{hex_key} invalid") from exc
        if len(raw) != accepted.get(length_key):
            raise ValueError(f"{hex_key} length mismatch")
        decoded[hex_key] = raw
    sha_ref = lambda raw: "sha256:" + hashlib.sha256(raw).hexdigest()
    if sha_ref(decoded["semanticEvidenceHex"]) != accepted.get("semanticEvidenceCasRef") or \
            sha_ref(decoded["evidenceDigestPreimageHex"]) != accepted.get("evidenceDigest") or \
            "run1:" + hashlib.sha256(decoded["runDomainPreimageHex"]).hexdigest() != accepted.get("runId") or \
            sha_ref(decoded["terminalRunEncodedHex"]) != accepted.get("runSealRef"):
        raise ValueError("SemanticEvidence/EvidenceDigest/RunId/Terminal raw identity rehash mismatch")

    handle = ep7._require_handle(authority)
    candidate = handle._candidate
    receipt = candidate["planAuthorityReceipt"]
    admission = candidate["evaluationAuthorityAdmission"]
    expected_index = {
        "schemaVersion": 1, "projectId": handle._project,
        "runId": accepted["runId"], "runSealRef": accepted["runSealRef"],
        "planAuthorityReceiptRef": ep7._ep6().raw_record_ref(
            "PlanAuthorityReceiptV1", receipt),
        "evaluationAuthorityAdmissionRef": handle._admission_ref,
        "planId": receipt["planId"],
        "planIntentCommitment": receipt["planIntentCommitment"],
        "executionPlanCommitment": candidate["evaluationAuthoritySeal"]["executionPlanCommitment"],
        "activationManifestRef": admission["activationManifestRef"],
        "evaluationAuthoritySealRef": handle._eas_ref,
    }
    if accepted.get("runAuthorityIndex") != expected_index or list(expected_index) != INDEX_FIELDS:
        raise ValueError("RunAuthorityIndex does not exactly rejoin admitted store authority")
    raw_golden = accepted.get("runAuthorityIndexRaw") or {}
    encoded = b"opensip.run-authority-index.v1\0" + canonical(expected_index)
    if raw_golden.get("value") != expected_index or \
            raw_golden.get("encodedHex") != encoded.hex() or \
            raw_golden.get("byteLength") != len(encoded) or \
            raw_golden.get("rawCasRef") != sha_ref(encoded):
        raise ValueError("RunAuthorityIndex raw identity mismatch")
    if values.get("projectId") != handle._project or \
            values.get("planId") != receipt["planId"] or \
            values.get("planIntentCommitment") != receipt["planIntentCommitment"] or \
            values.get("executionPlanCommitment") != expected_index["executionPlanCommitment"] or \
            values.get("activationManifestRef") != admission["activationManifestRef"] or \
            values.get("evaluationAuthoritySealRef") != handle._eas_ref:
        raise ValueError("finalized values differ from admitted authority")
    if _has_forbidden_key(accepted):
        raise ValueError("operational store token leaked into content identity")
    return expected_index


def _records_for_commit(finalized: _FinalizedSemanticEvidenceV1,
                        custody: _PreparedCustodyV1,
                        index: dict[str, Any]) -> dict[str, tuple[tuple[Any, ...], dict[str, Any]]]:
    accepted = finalized._accepted
    project = finalized._project
    run_id = accepted["runId"]
    run_seal = accepted["runSealRef"]
    values = {
        "TerminalRunV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": run_seal,
            "recordBytesHex": accepted["terminalRunEncodedHex"]},
        "RunIndexV1": {
            "schemaVersion": 1, "projectId": project,
            "runId": run_id, "runSealRef": run_seal},
        "AttemptRunLinkV1": {
            "schemaVersion": 1, "projectId": project,
            "executionId": custody._execution_id, "disposition": "run-committed",
            "runId": run_id, "runSealRef": run_seal},
        "CustodyRootV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": run_seal,
            "semanticEvidenceCasRef": accepted["semanticEvidenceCasRef"],
            "unitIds": list(custody._unit_ids)},
        "RunAuthorityIndexV1": copy.deepcopy(index),
        "outbox": {
            "schemaVersion": 1, "projectId": project,
            "executionId": custody._execution_id, "event": "run-committed",
            "runId": run_id, "runSealRef": run_seal},
    }
    if _has_forbidden_key(values):
        raise ValueError("operational store token leaked into final records")
    keys = {
        "TerminalRunV1": (project, run_seal),
        "RunIndexV1": (project, run_id),
        "AttemptRunLinkV1": (project, custody._execution_id),
        "CustodyRootV1": (project, run_id),
        "RunAuthorityIndexV1": (project, run_id),
        "outbox": (project, custody._execution_id, "run-committed"),
    }
    return {name: (keys[name], values[name]) for name in FINAL_WRITES}


def commit_run(store: Any, authority: Any, finalized_evidence: Any,
               prepared_custody: Any) -> _CommittedRunV1:
    """Same-store continuity check plus atomic six-record insert-or-verify."""
    _, ep7, _, _ = _deps()
    port = ep7._require_store(store)
    handle = ep7._require_handle(authority)
    finalized = _require_finalized(finalized_evidence)
    custody = _require_custody(prepared_custody)
    ep7.assert_store_continuity(port, handle)
    tokens = {port._instance_token, handle._store_token,
              finalized._store_token, custody._store_token}
    if len(tokens) != 1:
        raise ValueError("different store instance supplied to finalizer")
    if len({port._project, handle._project, finalized._project, custody._project}) != 1 or \
            finalized._eas_ref != handle._eas_ref or custody._eas_ref != handle._eas_ref or \
            finalized._admission_ref != handle._admission_ref:
        raise ValueError("project/EAS/admission continuity mismatch")
    index = _rehash_finalized(finalized, handle)
    expected_units = [
        "unit3:sha256:5c6c613a74f68e39a5052a06274fa612888a63c327f0a1c8ae03c86ede1b9adc",
        "unit3:sha256:22311dbe7dd9fd958d1946e6795a2add39298a41fa6eb82f918ee61c312054ed",
    ]
    if custody._unit_ids != expected_units:
        raise ValueError("PreparedCustodyV1 unit identity mismatch")
    writes = _records_for_commit(finalized, custody, index)

    transaction_token = object()
    if transaction_token is None:  # pragma: no cover
        raise AssertionError("unreachable")
    ledger = _ledger_for(port)
    work = copy.deepcopy(ledger.records)
    for name in FINAL_WRITES:
        key, record = writes[name]
        existing = work[name].get(key)
        if existing is not None and existing != record:
            raise ValueError(f"{name} append-only collision")
        work[name][key] = copy.deepcopy(record)

    # Test-only hook permits a deterministic mutation in the otherwise tiny
    # validation/publication window.  The second trusted reread must catch it.
    if _TEST_BEFORE_PUBLISH_HOOK is not None:
        _TEST_BEFORE_PUBLISH_HOOK()
    ep7.assert_store_continuity(port, handle)
    ledger.records = work
    return _CommittedRunV1(_COMMITTED_TOKEN, finalized._accepted["runId"],
                           finalized._accepted["runSealRef"])


def committed_run_id(value: Any) -> str:
    if not isinstance(value, _CommittedRunV1) or value._token is not _COMMITTED_TOKEN:
        raise TypeError("CommittedRunV1 required")
    return value._run_id


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        e5mod, epmod, rtmod, vmod = _deps()
        predecessor = load("evidence.v5.json")
        ep = load("evaluation-proof.v7.json")
        rt = load("retention-tiers.v12.json")
        versioning = load("versioning-policy.v7.json")
    except Exception as exc:
        return [f"dependency import failed: {type(exc).__name__}: {exc}"]
    if verify_files:
        old_errors = e5mod.check(predecessor)
        if old_errors:
            errors.append(f"Evidence v5 predecessor red: {old_errors[0]}")
        for label, checker, artifact in (
                ("EP7", epmod, ep), ("RT12", rtmod, rt),
                ("VERSIONING-v7", vmod, versioning)):
            child_errors = checker.check(artifact)
            if child_errors:
                errors.append(f"{label} dependency red: {child_errors[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.evidence", 6):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal status drift")
    if value.get("supersedes") != {
            "artifact": "evidence.v5.json", "sha256": PINS["evidence.v5.json"],
            "checker": "check-evidence-v5.py",
            "checkerSha256": PINS["check-evidence-v5.py"]}:
        errors.append("Evidence v5 protected predecessor pin drift")
    changed_top = {
        "version", "role", "supersedes", "reviewFindingTransfers",
        "dependencies", "importedAuthorityContract", "adversarialControls",
        "retainedResiduals", "storeCapabilityContinuityContract",
        "identityStabilityFromEvidenceV5", "recursiveRequestIdExclusion",
        "correlationDifferential", "availabilityDifferential", "semanticJoins",
        "persistedVsProjection", "apiContract", "storeContract",
        "admissionAndSealOrdering", "sealedCapabilityContract", "invariants",
    }
    for key in set(predecessor) - changed_top:
        if value.get(key) != predecessor[key]:
            errors.append(f"Evidence v5 protected identity/mechanism changed: {key}")
    stability = value.get("identityStabilityFromEvidenceV5") or {}
    if stability.get("predecessorSha256") != PINS["evidence.v5.json"] or \
            stability.get("predecessorCheckerSha256") != PINS["check-evidence-v5.py"]:
        errors.append("Evidence v5 protected hash window drift")
    if value.get("acceptedGolden") != predecessor.get("acceptedGolden") or \
            value.get("runSubstitutionGoldens") != predecessor.get("runSubstitutionGoldens"):
        errors.append("Evidence v5 accepted/substitution goldens changed")
    api = value.get("apiContract") or {}
    expected_opaque = [
        "ProjectStoreAuthorityV1", "AdmittedEvaluationAuthorityV1",
        "ValidatedEP7BundleV5", "ValidatedRunFreeClosureV3", "PreparedCustodyV1",
        "FinalizedSemanticEvidenceV1", "CommittedRunV1", "VerifiedStoredRunV1",
    ]
    calls = api.get("calls") or []
    calls_text = json.dumps(calls)
    if api.get("opaqueTypes") != expected_opaque or len(calls) != 9 or \
            "ProjectStoreAuthorityV1.authorize_evaluation(EvaluationAuthorityCandidateV1)" not in calls_text or \
            "commit_run_v1(ProjectStoreAuthorityV1, AdmittedEvaluationAuthorityV1" not in calls_text or \
            any(stale in calls_text for stale in (
                "admit_evaluation_authority_seal", "bind_evaluation_authority",
                "commit_prepared_run", "VerifiedPlanAuthorityV1")) or \
            "one authority path" not in api.get("constructionRule", "") or \
            "no split/decorative bind API" not in api.get("constructionRule", ""):
        errors.append("E6 public API still has a split/decorative or non-continuous authority path")
    joins = value.get("semanticJoins") or {}
    if not all(term in joins.get("preCoreAuthority", "") for term in (
            "EP7", "ProjectStoreAuthorityV1.authorize_evaluation", "trusted CAS/index")) or \
            "RT12" not in joins.get("retention", "") or \
            not all(term in joins.get("versioning", "") for term in (
                "VERSIONING v7", "RT12", "store tokens are excluded")):
        errors.append("E6 semantic join owner/store provenance drift")
    recursive_text = json.dumps(value.get("recursiveRequestIdExclusion") or {})
    if not all(term in recursive_text for term in ("EP7", "RT12")) or \
            any(term in recursive_text for term in ("EP6", "RT11")):
        errors.append("E6 recursive identity owner labels retain superseded authority path")
    correlation = copy.deepcopy(predecessor["correlationDifferential"])
    correlation["semanticInputs"] = \
        "byte-identical EP7 bundle, RT12 closure, admitted authority and canonical Evidence records"
    availability = copy.deepcopy(predecessor["availabilityDifferential"])
    availability["mutation"] = "remove one replay-only raw object from current RT12 availability"
    if value.get("correlationDifferential") != correlation or \
            value.get("availabilityDifferential") != availability:
        errors.append("E5 correlation/availability identities changed beyond owner labels")
    ordering = value.get("admissionAndSealOrdering") or []
    if len(ordering) != 6 or not all(term in json.dumps(ordering) for term in (
            "index-free candidate", "ProjectStoreAuthorityV1", "RT12",
            "identical ProjectStoreAuthorityV1/admitted handle", "atomic six-record")):
        errors.append("E6 sole authority/finalization ordering incomplete")
    store_contract = value.get("storeContract") or {}
    transaction_text = json.dumps(store_contract.get("transaction") or [])
    final_precondition = (store_contract.get("finalTransaction") or {}).get("precondition", "")
    if not all(term in transaction_text for term in (
            "same ProjectStoreAuthorityV1", "EP7 store-bound handle", "RT12 closure")) or \
            not all(term in final_precondition for term in (
                "identical ProjectStoreAuthorityV1/AdmittedEvaluationAuthorityV1",
                "authority-index/CAS reread")):
        errors.append("E6 store transaction does not unify authorize/finalize port")
    golden = value.get("acceptedGolden") or {}
    if golden.get("semanticEvidenceCasRef") != \
            "sha256:858ccc7c508c49c44ae85df6f880b4e26cecb0b2ec182abbf890a6c1ea8a0d82" or \
            golden.get("evidenceDigest") != \
            "sha256:6edbf46f919565e5a10426e4ff9f1dcf56588d18d1b75ad1c32cd848b19f47b9" or \
            golden.get("runId") != \
            "run1:3f319950f6a00565611029f3accc38a2afd38b3f4ab6539b2d6c8304ef0a9208" or \
            golden.get("runSealRef") != \
            "sha256:d34fc5e0d80f2af919c3ab572f03793b7893dddb2f816587b76bce40af497734" or \
            (golden.get("runAuthorityIndexRaw") or {}).get("byteLength") != 996 or \
            (golden.get("runAuthorityIndexRaw") or {}).get("rawCasRef") != \
            "sha256:bf50d2d6b01dcdc09ef13f830a1b8ed208547c549e53816ba282c99e53185dad":
        errors.append("explicit E5 identity stability constants drift")

    expected_deps = {
        "evaluationProof": ("evaluation-proof.v7.json", "check-evaluation-proof-v7.py"),
        "retentionCustody": ("retention-tiers.v12.json", "check-retention-custody-v12.py"),
        "versioning": ("versioning-policy.v7.json", "check-versioning-v7.py"),
    }
    dependencies = value.get("dependencies") or {}
    for key, (artifact, checker) in expected_deps.items():
        row = dependencies.get(key) or {}
        if row.get("artifact") != artifact or row.get("checker") != checker or \
                row.get("sha256") != PINS[artifact] or \
                row.get("checkerSha256") != PINS[checker]:
            errors.append(f"dependency pin drift: {key}")
    direction = dependencies.get("dependencyDirection", "")
    if not all(term in direction for term in (
            "EP7", "RT12", "VERSIONING v7", "Evidence v6", "same-store")):
        errors.append("dependency direction/continuity statement incomplete")
    if "evidence" in json.dumps((versioning.get("successorRevision") or {}).get("inputs") or {}).lower():
        errors.append("VERSIONING v7 has forbidden Evidence back-edge")

    imported = value.get("importedAuthorityContract") or {}
    if imported.get("owner") != "evaluation-proof.v7.json" or \
            imported.get("candidateType") != \
            "EvaluationAuthorityCandidateV1 (untrusted, no store/index fields)" or \
            not str(imported.get("storePortType", "")).startswith("ProjectStoreAuthorityV1") or \
            not str(imported.get("capabilityType", "")).startswith("AdmittedEvaluationAuthorityV1") or \
            imported.get("finalizeApi") != \
            "commit_run(ProjectStoreAuthorityV1, AdmittedEvaluationAuthorityV1, FinalizedSemanticEvidenceV1, PreparedCustodyV1)":
        errors.append("EP7 store/handle/finalizer import contract drift")
    continuity = value.get("storeCapabilityContinuityContract") or {}
    if continuity.get("api") != \
            "commit_run(ProjectStoreAuthorityV1, AdmittedEvaluationAuthorityV1, FinalizedSemanticEvidenceV1, PreparedCustodyV1) -> CommittedRunV1" or \
            continuity.get("atomicWrites") != FINAL_WRITES or \
            len(continuity.get("preconditions") or []) != 6 or \
            "immediately before atomic writes" not in continuity.get("toctouRule", ""):
        errors.append("same-store atomic finalization contract drift")
    token_rule = continuity.get("tokenExclusion", "")
    if not all(term in token_rule for term in (
            "nonserializable", "SemanticEvidence", "EvidenceDigest", "RunId",
            "TerminalRunV1", "RunAuthorityIndexV1", "RT closure")):
        errors.append("store token identity exclusion incomplete")
    if _has_forbidden_key(golden) or _has_forbidden_key(
            rt["capabilityClosure"]["semanticClosure"]):
        errors.append("operational store token leaked into stable identity")

    transfer = value.get("reviewFindingTransfers") or []
    if transfer[:-1] != predecessor.get("reviewFindingTransfers") or \
            (transfer[-1] if transfer else {}).get("id") != "STORE-PROVENANCE-CONTINUITY":
        errors.append("review-finding transfer is not strictly additive")
    authority = value.get("authority") or {}
    if authority != predecessor.get("authority"):
        errors.append("Evidence candidate/non-authority boundary changed")
    residuals = json.dumps(value.get("retainedResiduals") or [])
    if not all(term in residuals for term in (
            "no production store/transaction/atomicity", "V10", "CD-RT-5",
            "G19", "no seal")):
        errors.append("Evidence residual/non-claim matrix incomplete")

    # Exercise the actual store-authorize/finalize path once during conformance.
    try:
        vector = _accepted_vector(ep)
        store = epmod._open_test_project_store(vector["trustedStoreFixture"])
        handle = epmod.authorize_evaluation(store, vector["evaluationAuthorityCandidate"])
        finalized, custody = _prepare_accepted_run(value, rt, store, handle,
                                                    execution_id="exec1-conformance")
        before = _ledger_snapshot(store)
        committed = commit_run(store, handle, finalized, custody)
        after = _ledger_snapshot(store)
        if committed_run_id(committed) != golden.get("runId") or \
                before == after or any(len(after[name]) != 1 for name in FINAL_WRITES):
            errors.append("same-store six-record finalization control failed")
    except Exception as exc:
        errors.append(f"same-store finalization failed: {type(exc).__name__}: {exc}")
    return errors


def _must_reject(label: str, fn: Any, failures: list[str]) -> None:
    try:
        fn()
        failures.append(f"{label}: escaped")
    except (KeyError, TypeError, UnicodeError, ValueError):
        pass


def selftest(contract: dict[str, Any]) -> list[str]:
    global _TEST_BEFORE_PUBLISH_HOOK
    failures: list[str] = []
    _, ep7, _, _ = _deps()
    ep = load("evaluation-proof.v7.json")
    rt = load("retention-tiers.v12.json")
    vector = _accepted_vector(ep)

    store = ep7._open_test_project_store(vector["trustedStoreFixture"])
    handle = ep7.authorize_evaluation(store, vector["evaluationAuthorityCandidate"])
    finalized, custody = _prepare_accepted_run(contract, rt, store, handle,
                                                execution_id="exec1-positive")
    committed = commit_run(store, handle, finalized, custody)
    snapshot = _ledger_snapshot(store)
    if committed_run_id(committed) != contract["acceptedGolden"]["runId"] or \
            any(len(snapshot[name]) != 1 for name in FINAL_WRITES):
        failures.append("positive atomic commit failed")
    # Exact retry is idempotent.
    commit_run(store, handle, finalized, custody)
    if _ledger_snapshot(store) != snapshot:
        failures.append("idempotent retry changed ledger")

    other = ep7._open_test_project_store(vector["trustedStoreFixture"])
    _must_reject("different-store finalizer",
                 lambda: commit_run(other, handle, finalized, custody), failures)
    if any(_ledger_snapshot(other)[name] for name in FINAL_WRITES):
        failures.append("different-store failure published records")
    _must_reject("plain-dict store",
                 lambda: commit_run({}, handle, finalized, custody), failures)
    _must_reject("plain-dict handle",
                 lambda: commit_run(store, {}, finalized, custody), failures)
    _must_reject("plain-dict finalized evidence",
                 lambda: commit_run(store, handle, {}, custody), failures)

    forged_custody = _PreparedCustodyV1(
        _CUSTODY_TOKEN, store_token=object(), project=handle._project,
        eas_ref=handle._eas_ref, execution_id="exec1-forged", unit_ids=custody._unit_ids)
    _must_reject("different-store prepared custody",
                 lambda: commit_run(store, handle, finalized, forged_custody), failures)
    forged_final = _FinalizedSemanticEvidenceV1(
        _FINALIZED_TOKEN, store_token=store._instance_token,
        project="prj1-" + "b" * 64, eas_ref=handle._eas_ref,
        admission_ref=handle._admission_ref, accepted=finalized._accepted)
    _must_reject("wrong-project finalized evidence",
                 lambda: commit_run(store, handle, forged_final, custody), failures)

    missing_store = ep7._open_test_project_store(vector["trustedStoreFixture"])
    missing_handle = ep7.authorize_evaluation(missing_store, vector["evaluationAuthorityCandidate"])
    missing_final, missing_custody = _prepare_accepted_run(
        contract, rt, missing_store, missing_handle, execution_id="exec1-missing-cas")
    del missing_store._state._cas[missing_handle._required_rows[0]["recordCasRef"]]
    _must_reject("missing authority CAS",
                 lambda: commit_run(missing_store, missing_handle,
                                    missing_final, missing_custody), failures)
    if any(_ledger_snapshot(missing_store)[name] for name in FINAL_WRITES):
        failures.append("missing-CAS failure published records")

    collision_store = ep7._open_test_project_store(vector["trustedStoreFixture"])
    collision_handle = ep7.authorize_evaluation(
        collision_store, vector["evaluationAuthorityCandidate"])
    collision_final, collision_custody = _prepare_accepted_run(
        contract, rt, collision_store, collision_handle,
        execution_id="exec1-collision")
    collision_ledger = _ledger_for(collision_store)
    collision_key = (collision_handle._project, contract["acceptedGolden"]["runId"])
    collision_ledger.records["RunAuthorityIndexV1"][collision_key] = {"forged": True}
    collision_before = _ledger_snapshot(collision_store)
    _must_reject("RunAuthorityIndex collision",
                 lambda: commit_run(collision_store, collision_handle,
                                    collision_final, collision_custody), failures)
    if _ledger_snapshot(collision_store) != collision_before:
        failures.append("collision failure was not atomic")

    toctou_store = ep7._open_test_project_store(vector["trustedStoreFixture"])
    toctou_handle = ep7.authorize_evaluation(
        toctou_store, vector["evaluationAuthorityCandidate"])
    toctou_final, toctou_custody = _prepare_accepted_run(
        contract, rt, toctou_store, toctou_handle, execution_id="exec1-toctou")
    toctou_key = (toctou_handle._project, toctou_handle._eas_ref)

    def replace_index() -> None:
        row = copy.deepcopy(toctou_store._state._index[0])
        row["evaluationAuthorityAdmissionRef"] = "sha256:" + "d" * 64
        toctou_store._state._index = [row]
        toctou_store._state._index_versions[toctou_key] += 1

    _TEST_BEFORE_PUBLISH_HOOK = replace_index
    try:
        _must_reject("TOCTOU authority-index replacement",
                     lambda: commit_run(toctou_store, toctou_handle,
                                        toctou_final, toctou_custody), failures)
    finally:
        _TEST_BEFORE_PUBLISH_HOOK = None
    if any(_ledger_snapshot(toctou_store)[name] for name in FINAL_WRITES):
        failures.append("TOCTOU failure published records")

    injected = copy.deepcopy(finalized._accepted)
    injected["storeInstanceToken"] = "forged"
    injected_final = _FinalizedSemanticEvidenceV1(
        _FINALIZED_TOKEN, store_token=store._instance_token,
        project=handle._project, eas_ref=handle._eas_ref,
        admission_ref=handle._admission_ref, accepted=injected)
    _must_reject("store token identity injection",
                 lambda: commit_run(store, handle, injected_final, custody), failures)
    for label, item in (("store", store), ("handle", handle),
                        ("finalized", finalized), ("custody", custody)):
        _must_reject(f"JSON serialization {label}", lambda value=item: json.dumps(value), failures)
        _must_reject(f"pickle serialization {label}", lambda value=item: pickle.dumps(value), failures)

    mutations = []

    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        mutations.append((label, candidate))

    add("Evidence digest", lambda c: c["acceptedGolden"].__setitem__(
        "evidenceDigest", "sha256:" + "1" * 64))
    add("RunId", lambda c: c["acceptedGolden"].__setitem__(
        "runId", "run1:" + "2" * 64))
    add("run seal", lambda c: c["acceptedGolden"].__setitem__(
        "runSealRef", "sha256:" + "3" * 64))
    add("RunAuthority raw", lambda c: c["acceptedGolden"]["runAuthorityIndexRaw"].__setitem__(
        "encodedHex", "00"))
    add("atomic write omission", lambda c: c["storeCapabilityContinuityContract"]["atomicWrites"].pop())
    add("EP7 pin", lambda c: c["dependencies"]["evaluationProof"].__setitem__(
        "checkerSha256", "0" * 64))
    add("predecessor pin", lambda c: c["identityStabilityFromEvidenceV5"].__setitem__(
        "predecessorSha256", "0" * 64))
    for label, candidate in mutations:
        if not check(candidate, verify_files=False):
            failures.append(f"{label} escaped")
    return failures


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
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
        print("PASS: evidence.v6.json; same-store six-record atomic finalization; "
              "store/CAS/index/TOCTOU/collision controls rejected")
    else:
        golden = value["acceptedGolden"]
        print(f"PASS: evidence.v6.json; EvidenceDigest {golden['evidenceDigest']}; "
              f"RunId {golden['runId']}; same-store RunAuthorityIndexV1 clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
