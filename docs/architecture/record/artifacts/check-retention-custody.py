#!/usr/bin/env python3
"""Total retained checker for Phase-1A retention/custody v10.

This checker consumes a concrete accepted evaluation-proof v5 bundle. It derives
the complete typed raw-CAS/minimum graph, validates its exact custody
closure, executes a typed lease reducer, derives ProjectId-scoped purge results,
and compares complete D9 input/output records against the live D9 contract.

Public pure helpers (the cross-lane API) are:

  derive_transitive_requirements(seed_requirements, dependency_edges)
  derive_unit_id(project_id, capability, object_refs)
  encode_semantic_custody_unit(unit)
  semantic_closure_commitment(units)
  validate_capability_closure(proof_bundle, authority, closure)
  derive_effective_capability(sealed_capability, units, availability_records)
  reduce_lease(state, event)
  derive_purge(fixture)

Every checker entry point is total over successfully parsed JSON values.

Usage: python3 artifacts/check-retention-custody.py [contract] [--selftest]
Exit: 0 clean; 1 findings; 2 I/O or JSON syntax error.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys
import unicodedata
from typing import Any, Callable

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "retention-tiers.v10.json"
PROOF = "evaluation-proof.v5.json"
D9 = "d9-exit-contract.v1.6.json"
D9_CHECKER = "check-d9.py"
PRODUCT = "product-dispositions.v1.json"
RI = "resolved-inputs.v2.json"
C2 = "c2-plan-stage-schema.v3.json"
TM = "threat-model.v3.json"
STORAGE = "storage-namespace.adjudication-admission-storage-lane.v1.json"
EXPECTED_VERSION = 10
EXPECTED_CLOSURE_GRAMMAR_SHA256 = "abd8c541da028f2a273cc509bb8a2bc1c19eb78618ea56676ac301a83dd82ef8"

PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
RUN_RE = re.compile(r"^run1:[0-9a-f]{64}$")
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
UNIT_RE = re.compile(r"^unit1:[a-z][a-z0-9-]{0,63}$")
SEMANTIC_UNIT_RE = re.compile(r"^unit3:sha256:[0-9a-f]{64}$")
LEASE_RE = re.compile(r"^lease1:[0-9a-f]{32}$")
OWNER_RE = re.compile(r"^owner1:[0-9a-f]{32}$")
LIVENESS_RE = re.compile(r"^live1:[0-9a-f]{32}$")
PURGE_RE = re.compile(r"^purge1:[0-9a-f]{32}$")

CAPABILITY_RANK = {"recorded": 0, "verifiable": 1, "replayable": 2}
CAPABILITIES = set(CAPABILITY_RANK)
UNIT_STATES = {"AVAILABLE", "OUTAGE", "PURGED", "EXPIRED", "CORRUPT", "MISSING-DEPENDENCY"}
LEASE_STATES = {"HELD", "RELEASED", "RECLAIMED_STALE"}
TX_BOUNDARY = "ONE_PROJECT_LEDGER_TRANSACTION"

TOP_KEYS = {
    "artifact", "version", "status", "claimId", "supersedesAsArchitectureCandidate",
    "capabilityClosure", "leaseProtocol", "storageAndLineage",
    "d9Derivation", "custodyPolicy", "authority", "integrationState", "invariants",
    "assurance", "retainedResiduals", "sealRecommendation",
    "rawPhysicalIdentityContract",
}

DEPENDENCY_ROLES = {
    "coverage-fact-partition", "coverage-predicate-semantics", "partition-fact",
    "predicate-verifier", "policy-verifier", "verifier-signature", "fact-anchor",
    "replay-input", "historical-semantics", "historical-manifest",
    "historical-executable", "historical-signature", "historical-trust-root",
    "historical-public-key", "evaluation-authority-seal-record",
    "activation-manifest-record",
}


class DuplicateKeyError(ValueError):
    pass


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_EVAL_MODULE: Any = None


def _load_eval_module():
    global _EVAL_MODULE
    if _EVAL_MODULE is None:
        _EVAL_MODULE = _load_module(HERE / "check-evaluation-proof.py", "check_evaluation_proof_v5")
    return _EVAL_MODULE


def _load_d9_module():
    return _load_module(HERE / D9_CHECKER, "check_d9_v16")


def _sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs_no_duplicates)


def _load_context() -> dict[str, Any]:
    ctx: dict[str, Any] = {"errors": []}
    files = {
        "proof": PROOF, "d9contract": D9, "product": PRODUCT, "ri": RI,
        "c2": C2, "tm": TM, "storage": STORAGE,
    }
    for key, filename in files.items():
        path = HERE / filename
        try:
            ctx[key] = _load_json(path)
            ctx[key + "Sha256"] = _sha256_file(path)
        except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
            ctx["errors"].append(f"{filename}: {type(exc).__name__}: {exc}")
    try:
        ctx["epmod"] = _load_eval_module()
    except Exception as exc:
        ctx["errors"].append(f"check-evaluation-proof.py: {type(exc).__name__}: {exc}")
    try:
        ctx["d9mod"] = _load_d9_module()
    except Exception as exc:
        ctx["errors"].append(f"{D9_CHECKER}: {type(exc).__name__}: {exc}")
    if isinstance(ctx.get("proof"), dict) and ctx.get("epmod") is not None:
        try:
            ctx["proofFindings"] = ctx["epmod"].check(ctx["proof"])
        except Exception as exc:
            ctx["proofFindings"] = [f"EP-TOTALITY: {type(exc).__name__}: {exc}"]
    return ctx


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _exact(value: Any, required: set[str], optional: set[str], path: str,
           out: list[tuple[str, str]], invariant: str) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        out.append((invariant, f"{path}: expected object, got {type(value).__name__}"))
        return None
    keys = set(value)
    for key in sorted(required - keys):
        out.append((invariant, f"{path}: missing required field {key!r}"))
    for key in sorted(keys - required - optional):
        out.append((invariant, f"{path}: unknown field {key!r}"))
    return value


def _array(value: Any, path: str, out: list[tuple[str, str]], invariant: str) -> list[Any] | None:
    if not isinstance(value, list):
        out.append((invariant, f"{path}: expected array, got {type(value).__name__}"))
        return None
    return value


def _string(value: Any, path: str, out: list[tuple[str, str]], invariant: str,
            pattern: re.Pattern[str] | None = None, max_bytes: int = 4096) -> bool:
    if not isinstance(value, str):
        out.append((invariant, f"{path}: expected string, got {type(value).__name__}"))
        return False
    if not value or unicodedata.normalize("NFC", value) != value or len(value.encode("utf-8")) > max_bytes:
        out.append((invariant, f"{path}: empty, non-NFC, or over {max_bytes} UTF-8 bytes"))
        return False
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        out.append((invariant, f"{path}: control character forbidden"))
        return False
    if pattern is not None and not pattern.fullmatch(value):
        out.append((invariant, f"{path}: value {value!r} violates exact grammar"))
        return False
    return True


def _project(value: Any, path: str, out: list[tuple[str, str]], invariant: str = "RC-13") -> bool:
    return _string(value, path, out, invariant, PROJECT_RE)


def _run(value: Any, path: str, out: list[tuple[str, str]], invariant: str = "RC-13") -> bool:
    return _string(value, path, out, invariant, RUN_RE)


def _ref(value: Any, path: str, out: list[tuple[str, str]], invariant: str = "RC-11") -> bool:
    return _string(value, path, out, invariant, REF_RE)


def _frame_blob(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + len(value).to_bytes(4, "big") + value


_ACTIVE_CLOSURE_GRAMMAR: Any = None
UNIT_ID_DOMAIN = b"opensip.semantic-custody-unit-id.v3"


def _set_closure_grammar(value: Any) -> None:
    global _ACTIVE_CLOSURE_GRAMMAR
    _ACTIVE_CLOSURE_GRAMMAR = value


def _closure_grammar() -> dict[str, Any]:
    global _ACTIVE_CLOSURE_GRAMMAR
    if _ACTIVE_CLOSURE_GRAMMAR is None:
        _ACTIVE_CLOSURE_GRAMMAR = _load_json(HERE / BINDING)["capabilityClosure"]["closureGrammar"]
    if not isinstance(_ACTIVE_CLOSURE_GRAMMAR, dict):
        raise ValueError("closureGrammar must be an object")
    return _ACTIVE_CLOSURE_GRAMMAR


def _closure_tag(role: str) -> int:
    rows = _closure_grammar().get("tagRegistry")
    if not isinstance(rows, list):
        raise ValueError("closureGrammar.tagRegistry must be an array")
    matches = [row for row in rows if isinstance(row, dict) and row.get("role") == role]
    if len(matches) != 1 or not isinstance(matches[0].get("tag"), str) or not re.fullmatch(r"0x[0-9a-f]{2}", matches[0]["tag"]):
        raise ValueError(f"closure grammar must declare exactly one tag for {role}")
    return int(matches[0]["tag"], 16)


def derive_transitive_requirements(seed_requirements: dict[str, str],
                                   dependency_edges: list[dict[str, Any]]) -> dict[str, str]:
    """Canonical v10 wrapper: Evidence/Retention never copy lattice ranks."""
    return _load_eval_module().derive_transitive_requirements(seed_requirements, dependency_edges)


def _encoded_object_ref(item: dict[str, Any]) -> bytes:
    ep = _load_eval_module()
    return _frame_blob(_closure_tag("objectRefs item blob"),
                       ep.frame_component(_closure_tag("recordCasRef component inside item"), item["recordCasRef"])
                       + ep.frame_component(_closure_tag("object ProjectId component inside item"), item["projectId"])
                       + ep.frame_component(_closure_tag("recordKind component inside item"), item["recordKind"]))


def _object_refs_blob(object_refs: list[dict[str, Any]]) -> bytes:
    rows = sorted(_encoded_object_ref(item) for item in object_refs)
    if len(rows) != len(set(rows)):
        raise ValueError("duplicate semantic custody raw-object key")
    return _frame_blob(_closure_tag("sorted objectRefs list blob"), b"".join(rows))


def unit_id_preimage(project_id: str, capability: str,
                     object_refs: list[dict[str, Any]]) -> bytes:
    ep = _load_eval_module()
    domain = _closure_grammar().get("unitIdContract", {}).get("domainUtf8")
    if domain != UNIT_ID_DOMAIN.decode("ascii"):
        raise ValueError("UNIT-ID-V3 domain drift")
    return (UNIT_ID_DOMAIN + b"\x00" + bytes([_closure_tag("SemanticCustodyUnitV3 record")])
            + ep.frame_component(_closure_tag("projectId component"), project_id)
            + ep.frame_component(_closure_tag("requiredForCapability component"), capability)
            + _object_refs_blob(object_refs))


def derive_unit_id(project_id: str, capability: str,
                   object_refs: list[dict[str, Any]]) -> str:
    return "unit3:sha256:" + hashlib.sha256(unit_id_preimage(project_id, capability, object_refs)).hexdigest()


def encode_semantic_custody_unit(unit: dict[str, Any]) -> bytes:
    ep = _load_eval_module()
    return (bytes([_closure_tag("SemanticCustodyUnitV3 record")])
            + ep.frame_component(_closure_tag("unitId component"), unit["unitId"])
            + ep.frame_component(_closure_tag("projectId component"), unit["projectId"])
            + ep.frame_component(_closure_tag("requiredForCapability component"), unit["requiredForCapability"])
            + _object_refs_blob(unit["objectRefs"]))


def semantic_closure_commitment(units: list[dict[str, Any]]) -> str:
    domain = _closure_grammar().get("commitmentDomain")
    if domain != "semantic-capability-closure-v3":
        raise ValueError("semantic closure commitment domain drift")
    return _load_eval_module().commit(domain, [encode_semantic_custody_unit(unit) for unit in units])


def _raw_key(value: dict[str, Any]) -> tuple[str, str, str]:
    return value["projectId"], value["recordCasRef"], value["recordKind"]


def _availability_map(records: list[dict[str, Any]]) -> dict[str, dict[tuple[str, str, str], str]]:
    return {record["unitId"]: {_raw_key(state): state["state"] for state in record["objectStates"]}
            for record in records}


def derive_effective_capability(sealed_capability: str, units: list[dict[str, Any]],
                                availability_records: list[dict[str, Any]]) -> str:
    if sealed_capability not in CAPABILITY_RANK:
        raise ValueError("unknown sealed capability")
    availability = _availability_map(availability_records)
    result = "recorded"
    for candidate in sorted(CAPABILITY_RANK, key=CAPABILITY_RANK.get):
        if CAPABILITY_RANK[candidate] > CAPABILITY_RANK[sealed_capability]:
            continue
        required_units = [unit for unit in units
                          if CAPABILITY_RANK[unit["requiredForCapability"]] <= CAPABILITY_RANK[candidate]]
        if all(unit["objectRefs"] and set(availability.get(unit["unitId"], {})) == {_raw_key(x) for x in unit["objectRefs"]}
               and all(state == "AVAILABLE" for state in availability[unit["unitId"]].values())
               for unit in required_units):
            result = candidate
    return result


def _flatten_proof_edges(bundle: dict[str, Any], authority: dict[str, Any]) -> list[dict[str, Any]]:
    requirements = _load_eval_module().derive_raw_proof_requirements(bundle, authority)
    kinds = {row["recordCasRef"]: row["recordKind"] for row in requirements}
    edges: list[dict[str, Any]] = []
    for record in bundle["objectStore"]:
        for dependency in record["dependencies"]:
            edges.append({
                "fromRecordCasRef": record["ref"], "fromRecordKind": kinds[record["ref"]],
                "toRecordCasRef": dependency["ref"], "toRecordKind": kinds[dependency["ref"]],
                "projectId": dependency["projectId"], "role": dependency["role"],
            })
    return sorted(edges, key=lambda edge: (
        edge["fromRecordCasRef"], edge["fromRecordKind"], edge["toRecordCasRef"],
        edge["toRecordKind"], edge["role"], edge["projectId"]))


def _validate_ref_scope(value: Any, path: str, project_id: Any,
                        out: list[tuple[str, str]], invariant: str = "RC-11") -> tuple[str, str, str] | None:
    obj = _exact(value, {"recordCasRef", "projectId", "recordKind"}, set(), path, out, invariant)
    if obj is None:
        return None
    ok_ref = _ref(obj.get("recordCasRef"), path + ".recordCasRef", out, invariant)
    ok_pid = _project(obj.get("projectId"), path + ".projectId", out, invariant)
    ok_kind = _string(obj.get("recordKind"), path + ".recordKind", out, invariant)
    if ok_pid and obj["projectId"] != project_id:
        out.append((invariant, f"{path}: ProjectId mismatch"))
    return (obj["projectId"], obj["recordCasRef"], obj["recordKind"]) if ok_ref and ok_pid and ok_kind else None


def _validate_unit(value: Any, path: str, project_id: Any,
                   out: list[tuple[str, str]]) -> dict[str, Any] | None:
    unit = _exact(value, {"unitId", "projectId", "requiredForCapability", "objectRefs"}, set(), path, out, "RC-11")
    if unit is None:
        return None
    _string(unit.get("unitId"), path + ".unitId", out, "RC-11", SEMANTIC_UNIT_RE)
    if not _project(unit.get("projectId"), path + ".projectId", out, "RC-11") or unit.get("projectId") != project_id:
        out.append(("RC-11", f"{path}: unit ProjectId does not equal proof bundle"))
    if unit.get("requiredForCapability") not in CAPABILITIES:
        out.append(("RC-11", f"{path}.requiredForCapability: unknown capability"))
    refs_raw = _array(unit.get("objectRefs"), path + ".objectRefs", out, "RC-11")
    refs: list[tuple[str, str, str]] = []
    if refs_raw is not None:
        if not refs_raw:
            out.append(("RC-11", f"{path}.objectRefs: unit cannot be empty"))
        for i, record in enumerate(refs_raw):
            parsed = _validate_ref_scope(record, f"{path}.objectRefs[{i}]", project_id, out)
            if parsed is not None:
                refs.append(parsed)
        if len(refs) != len(set(refs)):
            out.append(("RC-11", f"{path}.objectRefs: duplicate physical key"))
    try:
        if unit.get("unitId") != derive_unit_id(unit.get("projectId"), unit.get("requiredForCapability"), unit.get("objectRefs")):
            out.append(("RC-11", f"{path}.unitId: does not derive by UNIT-ID-V3 from exact typed raw fields"))
        if unit.get("objectRefs") != sorted(unit.get("objectRefs"), key=_encoded_object_ref):
            out.append(("RC-11", f"{path}.objectRefs: must be strict encoded-byte order"))
    except (KeyError, TypeError, ValueError) as exc:
        out.append(("RC-11", f"{path}: UNIT-ID-V3/byte encoding failed ({exc})"))
    return unit


def _validate_availability_records(value: Any, units: list[dict[str, Any]], project_id: Any,
                                   out: list[tuple[str, str]]) -> list[dict[str, Any]]:
    records_raw = _array(value, "$availability", out, "RC-12")
    records: list[dict[str, Any]] = []
    seen_units: set[str] = set()
    if records_raw is None:
        return records
    expected = {unit["unitId"]: {_raw_key(x) for x in unit["objectRefs"]} for unit in units}
    run_ids: set[str] = set()
    for i, raw in enumerate(records_raw):
        path = f"$availability[{i}]"
        record = _exact(raw, {"schemaVersion", "projectId", "runId", "unitId", "objectStates"}, set(), path, out, "RC-12")
        if record is None:
            continue
        if record.get("schemaVersion") != 2:
            out.append(("RC-12", f"{path}.schemaVersion: expected 2"))
        if not _project(record.get("projectId"), path + ".projectId", out, "RC-12") or record.get("projectId") != project_id:
            out.append(("RC-12", f"{path}: ProjectId mismatch"))
        if _run(record.get("runId"), path + ".runId", out, "RC-12"):
            run_ids.add(record["runId"])
        _string(record.get("unitId"), path + ".unitId", out, "RC-12", SEMANTIC_UNIT_RE)
        if record.get("unitId") in seen_units:
            out.append(("RC-12", f"{path}.unitId: duplicate availability record"))
        elif isinstance(record.get("unitId"), str):
            seen_units.add(record["unitId"])
        states_raw = _array(record.get("objectStates"), path + ".objectStates", out, "RC-12")
        refs: list[tuple[str, str, str]] = []
        if states_raw is not None:
            for j, raw_state in enumerate(states_raw):
                spath = f"{path}.objectStates[{j}]"
                state = _exact(raw_state, {"recordCasRef", "projectId", "recordKind", "state"}, set(), spath, out, "RC-12")
                if state is None:
                    continue
                _ref(state.get("recordCasRef"), spath + ".recordCasRef", out, "RC-12")
                _string(state.get("recordKind"), spath + ".recordKind", out, "RC-12")
                if not _project(state.get("projectId"), spath + ".projectId", out, "RC-12") or state.get("projectId") != project_id:
                    out.append(("RC-12", f"{spath}: ProjectId mismatch"))
                if state.get("state") not in UNIT_STATES:
                    out.append(("RC-12", f"{spath}.state: unknown state"))
                if (isinstance(state.get("recordCasRef"), str)
                        and isinstance(state.get("recordKind"), str)
                        and isinstance(state.get("projectId"), str)):
                    refs.append(_raw_key(state))
        if len(refs) != len(set(refs)) or set(refs) != expected.get(record.get("unitId"), set()):
            out.append(("RC-12", f"{path}.objectStates: must exactly cover semantic unit refs"))
        records.append(record)
    if seen_units != set(expected):
        out.append(("RC-12", "$availability: must contain exactly one record per semantic unit"))
    if len(run_ids) > 1:
        out.append(("RC-12", "$availability: records must share one derived downstream RunId"))
    return records


def validate_capability_closure(proof_bundle: Any, authority: Any, value: Any,
                                availability_records: Any | None = None) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    try:
        closure = _exact(value, {
            "schemaVersion", "projectId", "sealedCapability", "semanticObjectBindings",
            "semanticRoots", "proofRefs", "dependencyEdges", "units", "closureCommitment",
        }, set(), "$closure", out, "RC-11")
        if closure is None:
            return out
        if not isinstance(proof_bundle, dict):
            out.append(("RC-11", "$proof: accepted proof bundle is not an object"))
            return out
        if closure.get("schemaVersion") != 3:
            out.append(("RC-11", "$closure.schemaVersion: expected integer constant 3"))
        project_id = proof_bundle.get("projectId")
        if not _project(closure.get("projectId"), "$closure.projectId", out, "RC-11") or closure.get("projectId") != project_id:
            out.append(("RC-11", "$closure.projectId: must equal concrete proof bundle"))
        if closure.get("sealedCapability") not in CAPABILITIES:
            out.append(("RC-11", "$closure.sealedCapability: unknown capability"))

        ep = _load_eval_module()
        try:
            authority_hits = ep.validate_activation_authority(authority, proof_bundle)
            out.extend(("RC-11", f"fixed proof authority is invalid: {msg}") for _, msg in authority_hits)
            resolved = ep.resolve_semantic_object_bindings(authority)
            semantic_roots = ep.derive_semantic_requirements(authority)
            raw_requirements = ep.derive_raw_proof_requirements(proof_bundle, authority)
        except (KeyError, TypeError, ValueError) as exc:
            out.append(("RC-11", f"$proof: cannot derive complete requirements ({exc})"))
            resolved, semantic_roots, raw_requirements = {}, [], []
        if closure.get("semanticObjectBindings") != authority.get("semanticObjectBindings"):
            out.append(("RC-11", "$closure.semanticObjectBindings: must exactly equal the two verified derived witnesses"))
        if closure.get("semanticRoots") != semantic_roots:
            out.append(("RC-11", "$closure.semanticRoots: must exactly equal the two typed semantic commitments"))
        if len(resolved) != 2:
            out.append(("RC-11", "$closure: exactly two resolvable typed semantic roots are required"))
        if not raw_requirements:
            out.append(("RC-11", "$closure: empty proof dependency closure cannot support verifiable/replayable authority"))
        if not any(row.get("requiredForCapability") == "verifiable" for row in raw_requirements):
            out.append(("RC-11", "$closure: no verifiable proof dependency"))
        if closure.get("sealedCapability") == "replayable" and not any(
                row.get("requiredForCapability") == "replayable" for row in raw_requirements):
            out.append(("RC-11", "$closure: replayable seal has no replayable dependency"))

        proof_refs_raw = _array(closure.get("proofRefs"), "$closure.proofRefs", out, "RC-11")
        proof_refs: list[dict[str, Any]] = []
        seen_physical: set[tuple[str, str, str]] = set()
        if proof_refs_raw is not None:
            for i, record in enumerate(proof_refs_raw):
                path = f"$closure.proofRefs[{i}]"
                obj = _exact(record, {"identityKind", "projectId", "recordCasRef", "recordKind", "requiredForCapability"}, set(), path, out, "RC-11")
                if obj is None:
                    continue
                _ref(obj.get("recordCasRef"), path + ".recordCasRef", out)
                if not _project(obj.get("projectId"), path + ".projectId", out, "RC-11") or obj.get("projectId") != project_id:
                    out.append(("RC-11", f"{path}: ProjectId mismatch"))
                _string(obj.get("recordKind"), path + ".recordKind", out, "RC-11")
                if obj.get("identityKind") != "raw-cas":
                    out.append(("RC-11", f"{path}.identityKind: only raw-cas may enter physical custody"))
                if obj.get("requiredForCapability") not in CAPABILITIES:
                    out.append(("RC-11", f"{path}.requiredForCapability: unknown capability"))
                if all(isinstance(obj.get(key), str) for key in ("projectId", "recordCasRef", "recordKind")):
                    key = _raw_key(obj)
                    if key in seen_physical:
                        out.append(("RC-11", f"{path}: duplicate physical proof key"))
                    seen_physical.add(key)
                proof_refs.append(obj)
        if proof_refs != raw_requirements:
            out.append(("RC-11", "$closure.proofRefs: must exactly equal every typed raw direct/transitive reference, kind, and minimum"))
        derived = {_raw_key(row): row["requiredForCapability"] for row in raw_requirements}

        edges_raw = _array(closure.get("dependencyEdges"), "$closure.dependencyEdges", out, "RC-11")
        edges: list[dict[str, Any]] = []
        if edges_raw is not None:
            for i, edge in enumerate(edges_raw):
                path = f"$closure.dependencyEdges[{i}]"
                obj = _exact(edge, {"fromRecordCasRef", "fromRecordKind", "toRecordCasRef", "toRecordKind", "projectId", "role"}, set(), path, out, "RC-11")
                if obj is None:
                    continue
                _ref(obj.get("fromRecordCasRef"), path + ".fromRecordCasRef", out)
                _ref(obj.get("toRecordCasRef"), path + ".toRecordCasRef", out)
                _string(obj.get("fromRecordKind"), path + ".fromRecordKind", out, "RC-11")
                _string(obj.get("toRecordKind"), path + ".toRecordKind", out, "RC-11")
                if not _project(obj.get("projectId"), path + ".projectId", out, "RC-11") or obj.get("projectId") != project_id:
                    out.append(("RC-11", f"{path}: ProjectId mismatch"))
                if obj.get("role") not in DEPENDENCY_ROLES:
                    out.append(("RC-11", f"{path}.role: unknown dependency role"))
                edges.append(obj)
        if edges != _flatten_proof_edges(proof_bundle, authority):
            out.append(("RC-11", "$closure.dependencyEdges: must exactly equal the typed raw concrete accepted proof graph"))

        units_raw = _array(closure.get("units"), "$closure.units", out, "RC-11")
        units: list[dict[str, Any]] = []
        if units_raw is not None:
            unit_ids: set[str] = set()
            for i, value_unit in enumerate(units_raw):
                unit = _validate_unit(value_unit, f"$closure.units[{i}]", project_id, out)
                if unit is None:
                    continue
                if unit.get("unitId") in unit_ids:
                    out.append(("RC-11", f"$closure.units[{i}].unitId: duplicate"))
                elif isinstance(unit.get("unitId"), str):
                    unit_ids.add(unit["unitId"])
                units.append(unit)
            try:
                if units != sorted(units, key=encode_semantic_custody_unit):
                    out.append(("RC-11", "$closure.units: must be strict encoded-byte order"))
            except (KeyError, TypeError, ValueError) as exc:
                out.append(("RC-11", f"$closure.units: cannot encode ({exc})"))

        owners: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
        for unit in units:
            for record in unit.get("objectRefs", []) if isinstance(unit.get("objectRefs"), list) else []:
                if (isinstance(record, dict)
                        and all(isinstance(record.get(key), str)
                                for key in ("projectId", "recordCasRef", "recordKind"))):
                    owners.setdefault(_raw_key(record), []).append(unit)
        for raw_key, minimum in derived.items():
            holders = owners.get(raw_key, [])
            if len(holders) != 1:
                out.append(("RC-11", f"$closure.units: physical key {raw_key} has {len(holders)} owners; exactly one required"))
            elif holders[0].get("requiredForCapability") != minimum:
                out.append(("RC-11", f"$closure.units: physical key {raw_key} minimum is {minimum}, unit declares {holders[0].get('requiredForCapability')}"))
        for raw_key in sorted(set(owners) - set(derived)):
            out.append(("RC-11", f"$closure.units: injected non-proof physical key {raw_key}"))
        for unit in units:
            minima = {derived.get(_raw_key(record)) for record in unit.get("objectRefs", []) if isinstance(record, dict)
                      and all(isinstance(record.get(key), str) for key in ("projectId", "recordCasRef", "recordKind"))}
            if None in minima or len(minima) != 1 or unit.get("requiredForCapability") not in minima:
                out.append(("RC-11", f"$closure.units: {unit.get('unitId')} mixes or misstates exact minima"))

        semantic_refs = {row.get("semanticRef") for row in semantic_roots if isinstance(row, dict)}
        if semantic_refs & {key[1] for key in owners}:
            out.append(("RC-11", "$closure.units: SemanticCommitmentRef appears as a physical RawCasRef key"))

        try:
            if closure.get("closureCommitment") != semantic_closure_commitment(units):
                out.append(("RC-11", "$closure.closureCommitment: does not recompute from exact units"))
        except (KeyError, TypeError, ValueError) as exc:
            out.append(("RC-11", f"$closure: cannot derive semantic commitment ({exc})"))
        if availability_records is not None:
            _validate_availability_records(availability_records, units, project_id, out)
        return out
    except Exception as exc:
        out.append(("RC-TOTALITY", f"$closure: controlled validation failure {type(exc).__name__}: {exc}"))
        return out


def _object_state_map(state: dict[str, Any]) -> dict[tuple[str, str, str], dict[str, Any]]:
    return {_raw_key(record): record for record in state["objects"]}


def _pin_set(records: list[dict[str, Any]]) -> set[tuple[str, str, str]]:
    return {_raw_key(record) for record in records}


def _d9_result(cls: str, **codes: Any) -> dict[str, Any]:
    return {"kind": "D9", "termination": {"class": cls, **codes}}


def reduce_lease(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    """Pure normative LeaseStateV2 x LeaseEventV2 -> LeaseOutputV2 reducer."""
    current = copy.deepcopy(state)
    if event["projectId"] != current["projectId"]:
        raise ValueError("cross-project lease event")
    if event["transactionBoundary"] != TX_BOUNDARY:
        raise ValueError("lease event is not one project-ledger transaction")
    if event["atSequence"] != current["ledgerSequence"] + 1:
        raise ValueError("lease event sequence is not the next ledger sequence")
    objects = _object_state_map(current)
    lease = current["lease"]
    kind = event["kind"]

    if kind == "resolve-and-pin":
        requested = _pin_set(event["pinRefs"])
        if lease is not None and lease["state"] == "HELD":
            same = (lease["leaseId"] == event["leaseId"]
                    and lease["ownerId"] == event["ownerId"]
                    and lease["ownerLivenessToken"] == event["ownerLivenessToken"]
                    and lease["previousFencingToken"] == event["expectedPreviousFencingToken"]
                    and lease["expiresAtSequence"] == event["expiresAtSequence"]
                    and _pin_set(lease["pinnedRefs"]) == requested)
            if same:
                return {"state": current, "result": {
                    "kind": "LEASE_GRANTED", "leaseId": lease["leaseId"],
                    "fencingToken": lease["fencingToken"], "idempotent": True,
                }}
            return {"state": current, "result": _d9_result("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED")}
        if event["expectedPreviousFencingToken"] != current["lastIssuedFencingToken"]:
            return {"state": current, "result": _d9_result("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED")}
        if event["expiresAtSequence"] <= event["atSequence"]:
            return {"state": current, "result": _d9_result("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED")}
        if any(ref not in objects or objects[ref]["state"] != "AVAILABLE" for ref in requested):
            return {"state": current, "result": _d9_result("request-rejected", errorCode="REQUEST.UNSATISFIABLE")}
        next_fence = current["lastIssuedFencingToken"] + 1
        current["ledgerSequence"] = event["atSequence"]
        current["lastIssuedFencingToken"] = next_fence
        current["lease"] = {
            "leaseId": event["leaseId"], "projectId": event["projectId"],
            "ownerId": event["ownerId"], "ownerLivenessToken": event["ownerLivenessToken"],
            "ownerAlive": True, "previousFencingToken": event["expectedPreviousFencingToken"],
            "fencingToken": next_fence, "state": "HELD",
            "acquiredAtSequence": event["atSequence"], "expiresAtSequence": event["expiresAtSequence"],
            "pinnedRefs": copy.deepcopy(event["pinRefs"]), "pendingExpiryRefs": [],
        }
        return {"state": current, "result": {
            "kind": "LEASE_GRANTED", "leaseId": event["leaseId"],
            "fencingToken": next_fence, "idempotent": False,
        }}

    if kind == "purge":
        targets = _pin_set(event["targetRefs"])
        if lease is not None and lease["state"] == "HELD" and targets & _pin_set(lease["pinnedRefs"]):
            return {"state": current, "result": _d9_result("operational-failed", errorCode="LEDGER.BUSY_TIMEOUT")}
        for ref in targets:
            if ref in objects:
                objects[ref]["state"] = "PURGED"
        current["ledgerSequence"] = event["atSequence"]
        return {"state": current, "result": {"kind": "PURGE_COMMITTED", "removedRefs": copy.deepcopy(event["targetRefs"])}}

    if kind == "expiry":
        targets = _pin_set(event["targetRefs"])
        current["ledgerSequence"] = event["atSequence"]
        if lease is not None and lease["state"] == "HELD" and targets & _pin_set(lease["pinnedRefs"]):
            existing = _pin_set(lease["pendingExpiryRefs"])
            lease["pendingExpiryRefs"] += [copy.deepcopy(record) for record in event["targetRefs"] if _raw_key(record) not in existing]
            return {"state": current, "result": {"kind": "READ_CONTINUES", "termination": {"class": "success"}}}
        for ref in targets:
            if ref in objects:
                objects[ref]["state"] = "EXPIRED"
        return {"state": current, "result": {"kind": "EXPIRY_COMMITTED", "expiredRefs": copy.deepcopy(event["targetRefs"])}}

    if kind == "release":
        if (lease is None or lease["state"] != "HELD" or lease["leaseId"] != event["leaseId"]
                or lease["ownerId"] != event["ownerId"] or lease["fencingToken"] != event["fencingToken"]):
            return {"state": current, "result": _d9_result("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED")}
        applied = copy.deepcopy(lease["pendingExpiryRefs"])
        for record in applied:
            if _raw_key(record) in objects:
                objects[_raw_key(record)]["state"] = "EXPIRED"
        lease["state"] = "RELEASED"
        lease["pendingExpiryRefs"] = []
        current["ledgerSequence"] = event["atSequence"]
        return {"state": current, "result": {"kind": "LEASE_RELEASED", "leaseState": "RELEASED", "expiryAppliedRefs": applied}}

    if kind == "crash-reclaim":
        scope = _pin_set(event["scopeRefs"])
        if (lease is None or lease["state"] != "HELD"
                or event["leaseId"] != lease["leaseId"]
                or event["expectedOwnerId"] != lease["ownerId"]
                or event["expectedOwnerLivenessToken"] != lease["ownerLivenessToken"]
                or event["expectedFencingToken"] != lease["fencingToken"]
                or scope != _pin_set(lease["pinnedRefs"])
                or event["observedOwnerAlive"] is not False
                or event["atSequence"] < lease["expiresAtSequence"]):
            return {"state": current, "result": _d9_result("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED")}
        applied = copy.deepcopy(lease["pendingExpiryRefs"])
        for record in applied:
            if _raw_key(record) in objects:
                objects[_raw_key(record)]["state"] = "EXPIRED"
        reclaimed_id = lease["leaseId"]
        current["lease"] = None
        current["ledgerSequence"] = event["atSequence"]
        return {"state": current, "result": {
            "kind": "LEASE_RECLAIMED", "leaseId": reclaimed_id,
            "leaseState": "RECLAIMED_STALE", "expiryAppliedRefs": applied,
        }}
    raise ValueError(f"unknown lease event kind {kind!r}")


def _validate_scoped_refs(value: Any, path: str, project_id: Any,
                          out: list[tuple[str, str]], invariant: str) -> list[dict[str, Any]]:
    raw = _array(value, path, out, invariant)
    records: list[dict[str, Any]] = []
    if raw is None:
        return records
    seen: set[tuple[str, str, str]] = set()
    for i, record in enumerate(raw):
        parsed = _validate_ref_scope(record, f"{path}[{i}]", project_id, out, invariant)
        if parsed is not None:
            if parsed in seen:
                out.append((invariant, f"{path}[{i}]: duplicate raw physical key"))
            seen.add(parsed)
            records.append(record)
    return records


def _validate_lease_record(value: Any, path: str, project_id: Any,
                           out: list[tuple[str, str]]) -> dict[str, Any] | None:
    lease = _exact(value, {
        "leaseId", "projectId", "ownerId", "ownerLivenessToken", "ownerAlive",
        "previousFencingToken", "fencingToken", "state", "acquiredAtSequence", "expiresAtSequence",
        "pinnedRefs", "pendingExpiryRefs",
    }, set(), path, out, "RC-5")
    if lease is None:
        return None
    _string(lease.get("leaseId"), path + ".leaseId", out, "RC-5", LEASE_RE)
    if not _project(lease.get("projectId"), path + ".projectId", out, "RC-5") or lease.get("projectId") != project_id:
        out.append(("RC-5", f"{path}: ProjectId mismatch"))
    _string(lease.get("ownerId"), path + ".ownerId", out, "RC-5", OWNER_RE)
    _string(lease.get("ownerLivenessToken"), path + ".ownerLivenessToken", out, "RC-5", LIVENESS_RE)
    if type(lease.get("ownerAlive")) is not bool:
        out.append(("RC-5", f"{path}.ownerAlive: expected boolean"))
    if not _is_int(lease.get("previousFencingToken")) or lease["previousFencingToken"] < 0:
        out.append(("RC-5", f"{path}.previousFencingToken: expected non-negative integer"))
    if not _is_int(lease.get("fencingToken")) or lease["fencingToken"] < 1:
        out.append(("RC-5", f"{path}.fencingToken: expected positive integer"))
    if (_is_int(lease.get("previousFencingToken")) and _is_int(lease.get("fencingToken"))
            and lease["fencingToken"] != lease["previousFencingToken"] + 1):
        out.append(("RC-5", f"{path}: fencingToken must be exactly previousFencingToken + 1"))
    if lease.get("state") not in LEASE_STATES:
        out.append(("RC-5", f"{path}.state: unknown lease state"))
    for key in ("acquiredAtSequence", "expiresAtSequence"):
        if not _is_int(lease.get(key)) or lease[key] < 0:
            out.append(("RC-5", f"{path}.{key}: expected non-negative integer"))
    _validate_scoped_refs(lease.get("pinnedRefs"), path + ".pinnedRefs", project_id, out, "RC-5")
    _validate_scoped_refs(lease.get("pendingExpiryRefs"), path + ".pendingExpiryRefs", project_id, out, "RC-5")
    return lease


def _validate_lease_state(value: Any, path: str, out: list[tuple[str, str]]) -> dict[str, Any] | None:
    state = _exact(value, {"schemaVersion", "projectId", "ledgerSequence", "lastIssuedFencingToken", "objects", "lease"}, set(), path, out, "RC-5")
    if state is None:
        return None
    if state.get("schemaVersion") != 2:
        out.append(("RC-5", f"{path}.schemaVersion: expected 2"))
    _project(state.get("projectId"), path + ".projectId", out, "RC-5")
    if not _is_int(state.get("ledgerSequence")) or state["ledgerSequence"] < 0:
        out.append(("RC-5", f"{path}.ledgerSequence: expected non-negative integer"))
    if not _is_int(state.get("lastIssuedFencingToken")) or state["lastIssuedFencingToken"] < 0:
        out.append(("RC-5", f"{path}.lastIssuedFencingToken: expected non-negative integer"))
    objects_raw = _array(state.get("objects"), path + ".objects", out, "RC-5")
    seen: set[tuple[str, str, str]] = set()
    if objects_raw is not None:
        for i, record in enumerate(objects_raw):
            opath = f"{path}.objects[{i}]"
            obj = _exact(record, {"recordCasRef", "projectId", "recordKind", "state"}, set(), opath, out, "RC-5")
            if obj is None:
                continue
            _ref(obj.get("recordCasRef"), opath + ".recordCasRef", out, "RC-5")
            _string(obj.get("recordKind"), opath + ".recordKind", out, "RC-5")
            if not _project(obj.get("projectId"), opath + ".projectId", out, "RC-5") or obj.get("projectId") != state.get("projectId"):
                out.append(("RC-5", f"{opath}: ProjectId mismatch"))
            if obj.get("state") not in UNIT_STATES:
                out.append(("RC-5", f"{opath}.state: unknown state"))
            if all(isinstance(obj.get(key), str) for key in ("projectId", "recordCasRef", "recordKind")):
                key = _raw_key(obj)
                if key in seen:
                    out.append(("RC-5", f"{opath}: duplicate raw physical key"))
                seen.add(key)
    if state.get("lease") is not None:
        lease = _validate_lease_record(state["lease"], path + ".lease", state.get("projectId"), out)
        if (lease is not None and _is_int(lease.get("fencingToken"))
                and _is_int(state.get("lastIssuedFencingToken"))):
            if lease["fencingToken"] > state["lastIssuedFencingToken"]:
                out.append(("RC-5", f"{path}: lease fence exceeds durable lastIssuedFencingToken"))
            if lease.get("state") == "HELD" and lease["fencingToken"] != state["lastIssuedFencingToken"]:
                out.append(("RC-5", f"{path}: HELD lease must own the durable latest fence"))
    return state


def _validate_lease_event(value: Any, path: str, project_id: Any,
                          out: list[tuple[str, str]]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        out.append(("RC-5", f"{path}: expected tagged event object, got {type(value).__name__}"))
        return None
    kind = value.get("kind")
    common = {"kind", "projectId", "transactionBoundary", "atSequence"}
    by_kind = {
        "resolve-and-pin": {"leaseId", "ownerId", "ownerLivenessToken", "expectedPreviousFencingToken", "expiresAtSequence", "pinRefs"},
        "purge": {"targetRefs"}, "expiry": {"targetRefs"},
        "release": {"leaseId", "ownerId", "fencingToken"},
        "crash-reclaim": {"leaseId", "expectedOwnerId", "expectedOwnerLivenessToken", "expectedFencingToken", "scopeRefs", "observedOwnerAlive"},
    }
    if kind not in by_kind:
        _exact(value, common, set(), path, out, "RC-5")
        out.append(("RC-5", f"{path}.kind: unknown lease event {kind!r}"))
        return value
    event = _exact(value, common | by_kind[kind], set(), path, out, "RC-5")
    if event is None:
        return None
    if not _project(event.get("projectId"), path + ".projectId", out, "RC-5") or event.get("projectId") != project_id:
        out.append(("RC-5", f"{path}: event ProjectId mismatch"))
    if event.get("transactionBoundary") != TX_BOUNDARY:
        out.append(("RC-5", f"{path}.transactionBoundary: split/non-project transaction forbidden"))
    if not _is_int(event.get("atSequence")) or event["atSequence"] < 1:
        out.append(("RC-5", f"{path}.atSequence: expected positive integer"))
    if kind == "resolve-and-pin":
        _string(event.get("leaseId"), path + ".leaseId", out, "RC-5", LEASE_RE)
        _string(event.get("ownerId"), path + ".ownerId", out, "RC-5", OWNER_RE)
        _string(event.get("ownerLivenessToken"), path + ".ownerLivenessToken", out, "RC-5", LIVENESS_RE)
        if not _is_int(event.get("expectedPreviousFencingToken")) or event["expectedPreviousFencingToken"] < 0:
            out.append(("RC-5", f"{path}.expectedPreviousFencingToken: expected non-negative integer"))
        if not _is_int(event.get("expiresAtSequence")) or event["expiresAtSequence"] < 1:
            out.append(("RC-5", f"{path}.expiresAtSequence: expected positive integer"))
        pins = _validate_scoped_refs(event.get("pinRefs"), path + ".pinRefs", project_id, out, "RC-5")
        if not pins:
            out.append(("RC-5", f"{path}.pinRefs: resolve-and-pin must pin concrete refs"))
    elif kind in {"purge", "expiry"}:
        targets = _validate_scoped_refs(event.get("targetRefs"), path + ".targetRefs", project_id, out, "RC-5")
        if not targets:
            out.append(("RC-5", f"{path}.targetRefs: event must target concrete refs"))
    elif kind == "release":
        _string(event.get("leaseId"), path + ".leaseId", out, "RC-5", LEASE_RE)
        _string(event.get("ownerId"), path + ".ownerId", out, "RC-5", OWNER_RE)
        if not _is_int(event.get("fencingToken")) or event["fencingToken"] < 1:
            out.append(("RC-5", f"{path}.fencingToken: expected positive integer"))
    elif kind == "crash-reclaim":
        _string(event.get("leaseId"), path + ".leaseId", out, "RC-5", LEASE_RE)
        _string(event.get("expectedOwnerId"), path + ".expectedOwnerId", out, "RC-5", OWNER_RE)
        _string(event.get("expectedOwnerLivenessToken"), path + ".expectedOwnerLivenessToken", out, "RC-5", LIVENESS_RE)
        if not _is_int(event.get("expectedFencingToken")) or event["expectedFencingToken"] < 1:
            out.append(("RC-5", f"{path}.expectedFencingToken: expected positive integer"))
        scope = _validate_scoped_refs(event.get("scopeRefs"), path + ".scopeRefs", project_id, out, "RC-5")
        if not scope:
            out.append(("RC-5", f"{path}.scopeRefs: exact non-empty lease scope required"))
        if type(event.get("observedOwnerAlive")) is not bool:
            out.append(("RC-5", f"{path}.observedOwnerAlive: expected boolean"))
    return event


def _validate_lease_output(value: Any, path: str, out: list[tuple[str, str]]) -> None:
    obj = _exact(value, {"state", "result"}, set(), path, out, "RC-5")
    if obj is None:
        return
    state = _validate_lease_state(obj.get("state"), path + ".state", out)
    result = obj.get("result")
    if not isinstance(result, dict):
        out.append(("RC-5", f"{path}.result: expected tagged object"))
        return
    kind = result.get("kind")
    schemas = {
        "LEASE_GRANTED": ({"kind", "leaseId", "fencingToken", "idempotent"}, set()),
        "D9": ({"kind", "termination"}, set()),
        "PURGE_COMMITTED": ({"kind", "removedRefs"}, set()),
        "READ_CONTINUES": ({"kind", "termination"}, set()),
        "EXPIRY_COMMITTED": ({"kind", "expiredRefs"}, set()),
        "LEASE_RELEASED": ({"kind", "leaseState", "expiryAppliedRefs"}, set()),
        "LEASE_RECLAIMED": ({"kind", "leaseId", "leaseState", "expiryAppliedRefs"}, set()),
    }
    if kind not in schemas:
        out.append(("RC-5", f"{path}.result.kind: unknown result {kind!r}"))
        return
    _exact(result, *schemas[kind], path + ".result", out, "RC-5")
    project_id = state.get("projectId") if isinstance(state, dict) else None
    if kind == "LEASE_GRANTED":
        _string(result.get("leaseId"), path + ".result.leaseId", out, "RC-5", LEASE_RE)
        if not _is_int(result.get("fencingToken")) or type(result.get("idempotent")) is not bool:
            out.append(("RC-5", f"{path}.result: invalid grant scalar types"))
    elif kind in {"PURGE_COMMITTED", "EXPIRY_COMMITTED", "LEASE_RELEASED"}:
        field = {"PURGE_COMMITTED": "removedRefs", "EXPIRY_COMMITTED": "expiredRefs", "LEASE_RELEASED": "expiryAppliedRefs"}[kind]
        _validate_scoped_refs(result.get(field), path + ".result." + field, project_id, out, "RC-5")
    if kind in {"LEASE_RELEASED", "LEASE_RECLAIMED"}:
        expected = "RELEASED" if kind == "LEASE_RELEASED" else "RECLAIMED_STALE"
        if result.get("leaseState") != expected:
            out.append(("RC-5", f"{path}.result.leaseState: expected {expected}"))
    if kind == "LEASE_RECLAIMED":
        _string(result.get("leaseId"), path + ".result.leaseId", out, "RC-5", LEASE_RE)
        _validate_scoped_refs(result.get("expiryAppliedRefs"), path + ".result.expiryAppliedRefs", project_id, out, "RC-5")
    if kind in {"D9", "READ_CONTINUES"}:
        termination = result.get("termination")
        if not isinstance(termination, dict) or not isinstance(termination.get("class"), str):
            out.append(("RC-5", f"{path}.result.termination: malformed"))


LEASE_TYPE_REGISTRY = {
    "LeaseRecordV2": {"closed": True, "required": ["leaseId", "projectId", "ownerId", "ownerLivenessToken", "ownerAlive", "previousFencingToken", "fencingToken", "state", "acquiredAtSequence", "expiresAtSequence", "pinnedRefs", "pendingExpiryRefs"]},
    "LeaseStateV2": {"closed": True, "required": ["schemaVersion", "projectId", "ledgerSequence", "lastIssuedFencingToken", "objects", "lease"]},
    "RawObjectKeyV1": {"closed": True, "required": ["projectId", "recordCasRef", "recordKind"]},
    "RawObjectStateV1": {"closed": True, "required": ["projectId", "recordCasRef", "recordKind", "state"]},
    "ResolveAndPinEventV2": {"closed": True, "required": ["kind", "projectId", "transactionBoundary", "atSequence", "leaseId", "ownerId", "ownerLivenessToken", "expectedPreviousFencingToken", "expiresAtSequence", "pinRefs"]},
    "PurgeEventV1": {"closed": True, "required": ["kind", "projectId", "transactionBoundary", "atSequence", "targetRefs"]},
    "ReleaseEventV1": {"closed": True, "required": ["kind", "projectId", "transactionBoundary", "atSequence", "leaseId", "ownerId", "fencingToken"]},
    "CrashReclaimEventV2": {"closed": True, "required": ["kind", "projectId", "transactionBoundary", "atSequence", "leaseId", "expectedOwnerId", "expectedOwnerLivenessToken", "expectedFencingToken", "scopeRefs", "observedOwnerAlive"]},
    "ExpiryEventV1": {"closed": True, "required": ["kind", "projectId", "transactionBoundary", "atSequence", "targetRefs"]},
}

LEASE_REDUCER_DECLARATION = {
    "algorithmId": "opensip.lease-reducer.v2",
    "transactionBoundary": TX_BOUNDARY,
    "rules": {
        "resolveAndPin": "atomically validate availability; require expectedPreviousFencingToken == durable lastIssuedFencingToken; allocate exactly last+1; persist one HELD lease with scoped pins",
        "purgeOrdering": "HELD intersecting pins reject purge with LEDGER.BUSY_TIMEOUT",
        "release": "matching owner/fence releases and atomically applies pending expiry",
        "crashReclaim": "exact lease/owner/liveness/fence/ProjectId/scope plus dead owner and expired sequence atomically applies pending expiry, removes expired authority, then clears the lease",
        "expiryDuringUse": "HELD live read continues; expiry becomes pending and applies at release",
        "idempotentRetry": "same lease/owner/liveness/previous-fence/pins/expiry returns unchanged grant and never extends expiry",
        "fenceMonotonicity": "durable lastIssuedFencingToken never decreases or resets; no later grant may reuse an issued fence",
        "composition": "release or reclaim is reduced before any repin; expired objects remain ineligible while an available object receives only the next fence",
    },
}


def _validate_lease_scenario(value: Any, path: str, out: list[tuple[str, str]]) -> str | None:
    scenario = _exact(value, {"id", "initial", "events", "expectedOutputs", "expectedFinalState"}, set(), path, out, "RC-5")
    if scenario is None:
        return None
    scenario_id = scenario.get("id")
    if not isinstance(scenario_id, str) or not scenario_id:
        out.append(("RC-5", f"{path}.id: required string"))
        scenario_id = None
    initial = _validate_lease_state(scenario.get("initial"), path + ".initial", out)
    events = _array(scenario.get("events"), path + ".events", out, "RC-5")
    outputs = _array(scenario.get("expectedOutputs"), path + ".expectedOutputs", out, "RC-5")
    final = _validate_lease_state(scenario.get("expectedFinalState"), path + ".expectedFinalState", out)
    if events is None or outputs is None:
        return scenario_id
    if not events or len(events) != len(outputs):
        out.append(("RC-5", f"{path}: non-empty events and one expected output per event required"))
        return scenario_id
    current = copy.deepcopy(initial) if isinstance(initial, dict) else None
    for i, (raw_event, expected) in enumerate(zip(events, outputs)):
        event = _validate_lease_event(raw_event, f"{path}.events[{i}]", current.get("projectId") if isinstance(current, dict) else None, out)
        _validate_lease_output(expected, f"{path}.expectedOutputs[{i}]", out)
        if current is None or event is None:
            continue
        try:
            derived = reduce_lease(current, event)
            if expected != derived:
                out.append(("RC-5", f"{path}.expectedOutputs[{i}]: composed reducer derives a different full output"))
            current = derived["state"]
        except (KeyError, TypeError, ValueError) as exc:
            out.append(("RC-5", f"{path}.events[{i}]: composed reducer rejected typed event ({exc})"))
    if current is not None and final is not None and current != final:
        out.append(("RC-5", f"{path}.expectedFinalState: differs from sequential reducer state"))
    return scenario_id


def _validate_lease_protocol(value: Any, run_mutations: bool = True) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    protocol = _exact(value, {"typeRegistry", "normativeReducer", "fixtures", "scenarios", "mutationCases", "doesNotClaim"}, set(), "$leaseProtocol", out, "RC-5")
    if protocol is None:
        return out
    if protocol.get("typeRegistry") != LEASE_TYPE_REGISTRY:
        out.append(("RC-5", "$leaseProtocol.typeRegistry: must exactly bind all closed typed lease records"))
    if protocol.get("normativeReducer") != LEASE_REDUCER_DECLARATION:
        out.append(("RC-5", "$leaseProtocol.normativeReducer: must exactly bind opensip.lease-reducer.v2"))
    if protocol.get("doesNotClaim") != "No wall-clock implementation, distributed lock service, crash harness, durable ledger implementation, or runtime measurement is demonstrated here.":
        out.append(("RC-5", "$leaseProtocol.doesNotClaim: exact implementation boundary required"))
    fixtures = _array(protocol.get("fixtures"), "$leaseProtocol.fixtures", out, "RC-5")
    if fixtures is not None:
        seen: set[str] = set()
        for i, fixture in enumerate(fixtures):
            path = f"$leaseProtocol.fixtures[{i}]"
            obj = _exact(fixture, {"id", "initial", "event", "expected"}, set(), path, out, "RC-5")
            if obj is None:
                continue
            if not isinstance(obj.get("id"), str) or obj["id"] in seen:
                out.append(("RC-5", f"{path}.id: missing/duplicate"))
            else:
                seen.add(obj["id"])
            initial = _validate_lease_state(obj.get("initial"), path + ".initial", out)
            project_id = initial.get("projectId") if isinstance(initial, dict) else None
            event = _validate_lease_event(obj.get("event"), path + ".event", project_id, out)
            _validate_lease_output(obj.get("expected"), path + ".expected", out)
            if initial is not None and event is not None:
                try:
                    derived = reduce_lease(initial, event)
                    if obj.get("expected") != derived:
                        out.append(("RC-5", f"{path}.expected: fixture label not trusted; reducer derives a different full output"))
                except (KeyError, TypeError, ValueError) as exc:
                    out.append(("RC-5", f"{path}: reducer rejected typed input ({exc})"))
    scenarios = _array(protocol.get("scenarios"), "$leaseProtocol.scenarios", out, "RC-5")
    scenario_ids: set[str] = set()
    if scenarios is not None:
        for i, scenario in enumerate(scenarios):
            scenario_id = _validate_lease_scenario(scenario, f"$leaseProtocol.scenarios[{i}]", out)
            if scenario_id is not None:
                if scenario_id in scenario_ids:
                    out.append(("RC-5", f"$leaseProtocol.scenarios[{i}].id: duplicate"))
                scenario_ids.add(scenario_id)
    if scenario_ids != {"LS-01-RECLAIM-EXPIRY-THEN-REPIN", "LS-02-RELEASE-THEN-REPIN", "LS-03-STALE-RECLAIM-AFTER-REPIN"}:
        out.append(("RC-5", "$leaseProtocol.scenarios: exact reclaim/release/repin composition controls required"))
    if run_mutations:
        cases = _array(protocol.get("mutationCases"), "$leaseProtocol.mutationCases", out, "RC-5")
        expected_kinds = {"split-transaction-coordinated", "boolean-lease-record", "crash-held-forever-coordinated", "expiry-preempts-live-coordinated", "retry-extends-expiry", "stale-reclaim-accepted", "wrong-reclaim-owner-accepted", "wrong-reclaim-liveness-accepted", "wrong-reclaim-fence-accepted", "reclaim-drops-pending-expiry", "fence-reuse-accepted", "repin-expired-accepted"}
        seen_kinds: set[str] = set()
        if cases is not None:
            for i, case in enumerate(cases):
                obj = _exact(case, {"id", "kind", "expectedInvariant"}, set(), f"$leaseProtocol.mutationCases[{i}]", out, "RC-5")
                if obj is None:
                    continue
                if obj.get("expectedInvariant") != "RC-5":
                    out.append(("RC-5", f"$leaseProtocol.mutationCases[{i}]: must name RC-5"))
                kind = obj.get("kind")
                if kind in seen_kinds or kind not in expected_kinds:
                    out.append(("RC-5", f"$leaseProtocol.mutationCases[{i}].kind: duplicate/unknown"))
                elif isinstance(kind, str):
                    seen_kinds.add(kind)
                    mutated = copy.deepcopy(protocol)
                    _apply_lease_mutation(mutated, kind)
                    hits = {inv for inv, _ in _validate_lease_protocol(mutated, False)}
                    if "RC-5" not in hits:
                        out.append(("RC-5", f"$leaseProtocol.mutationCases[{i}]: mutation escaped"))
        if seen_kinds != expected_kinds:
            out.append(("RC-5", f"$leaseProtocol.mutationCases: exact P08..P11 plus RR-03 identity/expiry/fence/composition controls required"))
    return out


def _apply_lease_mutation(protocol: dict[str, Any], kind: str) -> None:
    fixtures = protocol["fixtures"]
    if kind == "split-transaction-coordinated":
        fixture = next(f for f in fixtures if f["id"] == "LF-01-RESOLVE-AND-PIN")
        fixture["event"]["transactionBoundary"] = "SPLIT_RESOLVE_THEN_PIN"
        fixture["expected"]["result"] = {"kind": "LEASE_GRANTED", "leaseId": fixture["event"]["leaseId"], "fencingToken": fixture["initial"]["lastIssuedFencingToken"] + 1, "idempotent": False}
    elif kind == "boolean-lease-record":
        protocol["typeRegistry"]["LeaseRecordV2"] = {"closed": True, "required": ["isPinned"]}
    elif kind == "crash-held-forever-coordinated":
        protocol["normativeReducer"]["rules"]["crashReclaim"] = "crashed lease remains HELD forever"
        fixture = next(f for f in fixtures if f["id"] == "LF-05-CRASH-RECLAIM")
        fixture["expected"]["state"] = copy.deepcopy(fixture["initial"])
        fixture["expected"]["result"] = {"kind": "LEASE_GRANTED", "leaseId": fixture["initial"]["lease"]["leaseId"], "fencingToken": fixture["initial"]["lease"]["fencingToken"], "idempotent": True}
    elif kind == "expiry-preempts-live-coordinated":
        protocol["normativeReducer"]["rules"]["expiryDuringUse"] = "expiry preempts and deletes a live reader's pin"
        fixture = next(f for f in fixtures if f["id"] == "LF-06-EXPIRY-DURING-USE")
        fixture["expected"]["state"]["objects"][0]["state"] = "EXPIRED"
        fixture["expected"]["result"] = _d9_result("request-rejected", errorCode="REQUEST.UNSATISFIABLE")
    elif kind == "retry-extends-expiry":
        fixture = next(f for f in fixtures if f["id"] == "LF-08-IDEMPOTENT-RETRY")
        fixture["event"]["expiresAtSequence"] += 100
        fixture["expected"]["state"]["lease"]["expiresAtSequence"] += 100
    elif kind in {"stale-reclaim-accepted", "wrong-reclaim-owner-accepted", "wrong-reclaim-liveness-accepted", "wrong-reclaim-fence-accepted"}:
        fixture_id = {
            "stale-reclaim-accepted": "LF-09-STALE-RECLAIM",
            "wrong-reclaim-owner-accepted": "LF-10-WRONG-RECLAIM-OWNER",
            "wrong-reclaim-liveness-accepted": "LF-11-WRONG-RECLAIM-LIVENESS",
            "wrong-reclaim-fence-accepted": "LF-12-WRONG-RECLAIM-FENCE",
        }[kind]
        fixture = next(f for f in fixtures if f["id"] == fixture_id)
        bad_state = copy.deepcopy(fixture["initial"])
        bad_state["ledgerSequence"] = fixture["event"]["atSequence"]
        bad_state["lease"] = None
        fixture["expected"] = {"state": bad_state, "result": {
            "kind": "LEASE_RECLAIMED", "leaseId": fixture["event"]["leaseId"],
            "leaseState": "RECLAIMED_STALE", "expiryAppliedRefs": [],
        }}
    elif kind == "reclaim-drops-pending-expiry":
        fixture = next(f for f in fixtures if f["id"] == "LF-13-RECLAIM-PENDING-EXPIRY")
        fixture["expected"]["state"]["objects"][0]["state"] = "AVAILABLE"
        fixture["expected"]["result"]["expiryAppliedRefs"] = []
    elif kind == "fence-reuse-accepted":
        fixture = next(f for f in fixtures if f["id"] == "LF-14-FENCE-REUSE")
        event, initial = fixture["event"], fixture["initial"]
        reused = event["expectedPreviousFencingToken"] + 1
        bad_state = copy.deepcopy(initial)
        bad_state["ledgerSequence"] = event["atSequence"]
        bad_state["lease"] = {
            "leaseId": event["leaseId"], "projectId": event["projectId"],
            "ownerId": event["ownerId"], "ownerLivenessToken": event["ownerLivenessToken"],
            "ownerAlive": True, "previousFencingToken": event["expectedPreviousFencingToken"],
            "fencingToken": reused, "state": "HELD", "acquiredAtSequence": event["atSequence"],
            "expiresAtSequence": event["expiresAtSequence"], "pinnedRefs": copy.deepcopy(event["pinRefs"]),
            "pendingExpiryRefs": [],
        }
        fixture["expected"] = {"state": bad_state, "result": {"kind": "LEASE_GRANTED", "leaseId": event["leaseId"], "fencingToken": reused, "idempotent": False}}
    elif kind == "repin-expired-accepted":
        fixture = next(f for f in fixtures if f["id"] == "LF-15-REPIN-EXPIRED")
        event, initial = fixture["event"], fixture["initial"]
        fence = initial["lastIssuedFencingToken"] + 1
        bad_state = copy.deepcopy(initial)
        bad_state["ledgerSequence"] = event["atSequence"]
        bad_state["lastIssuedFencingToken"] = fence
        bad_state["lease"] = {
            "leaseId": event["leaseId"], "projectId": event["projectId"], "ownerId": event["ownerId"],
            "ownerLivenessToken": event["ownerLivenessToken"], "ownerAlive": True,
            "previousFencingToken": event["expectedPreviousFencingToken"], "fencingToken": fence,
            "state": "HELD", "acquiredAtSequence": event["atSequence"], "expiresAtSequence": event["expiresAtSequence"],
            "pinnedRefs": copy.deepcopy(event["pinRefs"]), "pendingExpiryRefs": [],
        }
        fixture["expected"] = {"state": bad_state, "result": {"kind": "LEASE_GRANTED", "leaseId": event["leaseId"], "fencingToken": fence, "idempotent": False}}


def _object_key(project_id: str, record_cas_ref: str, record_kind: str) -> dict[str, str]:
    return {"projectId": project_id, "recordCasRef": record_cas_ref, "recordKind": record_kind}


def derive_purge(fixture: dict[str, Any]) -> dict[str, Any]:
    request = fixture["request"]
    project_id = request["projectId"]
    scope = set(request["scopeRunIds"])
    edges = fixture["lineageEdges"]
    run_to_units: dict[str, set[str]] = {}
    unit_to_objects: dict[str, set[tuple[str, str]]] = {}
    for edge in edges:
        if edge["projectId"] != project_id:
            continue
        source, target = edge["from"], edge["to"]
        if source["kind"] == "run" and target["kind"] == "unit":
            run_to_units.setdefault(source["id"], set()).add(target["id"])
        if source["kind"] == "unit" and target["kind"] == "object":
            unit_to_objects.setdefault(source["id"], set()).add((target["id"], target["recordKind"]))
    object_runs: dict[tuple[str, str], set[str]] = {}
    for run_id, unit_ids in run_to_units.items():
        for unit_id in unit_ids:
            for object_key in unit_to_objects.get(unit_id, set()):
                object_runs.setdefault(object_key, set()).add(run_id)
    pin_blockers: dict[tuple[str, str], list[str]] = {}
    for pin in fixture["pins"]:
        if pin["projectId"] == project_id and pin["state"] == "HELD":
            pin_blockers.setdefault((pin["objectRef"]["recordCasRef"], pin["objectRef"]["recordKind"]), []).append(pin["leaseId"])

    removed: list[dict[str, str]] = []
    blocked: list[dict[str, Any]] = []
    untouched: list[dict[str, str]] = []
    for obj in fixture["objects"]:
        key = _object_key(obj["projectId"], obj["recordCasRef"], obj["recordKind"])
        if obj["projectId"] != project_id or not obj["containsSubject"]:
            untouched.append(key)
            continue
        physical = (obj["recordCasRef"], obj["recordKind"])
        outside = sorted(object_runs.get(physical, set()) - scope)
        leases = sorted(pin_blockers.get(physical, []))
        if outside or leases:
            blocked.append({"object": key, "blockingRunIds": outside, "blockingLeaseIds": leases})
        else:
            removed.append(key)
    key_sort = lambda key: (key["projectId"], key["recordCasRef"], key["recordKind"])
    return {
        "removed": sorted(removed, key=key_sort),
        "retainedBlocked": sorted(blocked, key=lambda row: key_sort(row["object"])),
        "untouched": sorted(untouched, key=key_sort),
        "demotedOutsideScope": False,
    }


def _endpoint(value: Any, path: str, out: list[tuple[str, str]]) -> tuple[str, str, str | None] | None:
    if not isinstance(value, dict):
        out.append(("RC-13", f"{path}: expected lineage endpoint object"))
        return None
    kind = value.get("kind")
    required = {"kind", "id", "recordKind"} if kind == "object" else {"kind", "id"}
    obj = _exact(value, required, set(), path, out, "RC-13")
    if obj is None:
        return None
    kind = obj.get("kind")
    if kind not in {"run", "unit", "object", "pin"}:
        out.append(("RC-13", f"{path}.kind: unknown lineage node kind"))
        return None
    patterns = {"run": RUN_RE, "unit": UNIT_RE, "object": REF_RE, "pin": LEASE_RE}
    _string(obj.get("id"), path + ".id", out, "RC-13", patterns[kind])
    if kind == "object":
        _string(obj.get("recordKind"), path + ".recordKind", out, "RC-13")
    return (kind, obj.get("id"), obj.get("recordKind")) if isinstance(obj.get("id"), str) else None


def _validate_object_key(value: Any, path: str, out: list[tuple[str, str]]) -> tuple[str, str, str] | None:
    obj = _exact(value, {"projectId", "recordCasRef", "recordKind"}, set(), path, out, "RC-13")
    if obj is None:
        return None
    ok1 = _project(obj.get("projectId"), path + ".projectId", out)
    ok2 = _ref(obj.get("recordCasRef"), path + ".recordCasRef", out, "RC-13")
    ok3 = _string(obj.get("recordKind"), path + ".recordKind", out, "RC-13")
    return (obj["projectId"], obj["recordCasRef"], obj["recordKind"]) if ok1 and ok2 and ok3 else None


def _validate_purge_fixture(value: Any, path: str = "$purge") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    try:
        fixture = _exact(value, {"id", "request", "runs", "units", "objects", "pins", "lineageEdges", "expected"}, set(), path, out, "RC-13")
        if fixture is None:
            return out
        _string(fixture.get("id"), path + ".id", out, "RC-13")
        request = _exact(fixture.get("request"), {"purgeId", "projectId", "targetSubject", "scopeRunIds"}, set(), path + ".request", out, "RC-13")
        project_id = request.get("projectId") if request else None
        if request is not None:
            _string(request.get("purgeId"), path + ".request.purgeId", out, "RC-13", PURGE_RE)
            _project(project_id, path + ".request.projectId", out)
            _string(request.get("targetSubject"), path + ".request.targetSubject", out, "RC-13")
            scope_raw = _array(request.get("scopeRunIds"), path + ".request.scopeRunIds", out, "RC-13")
            scope: list[str] = []
            if scope_raw is not None:
                for i, run_id in enumerate(scope_raw):
                    if _run(run_id, f"{path}.request.scopeRunIds[{i}]", out):
                        scope.append(run_id)
                if not scope or len(scope) != len(set(scope)):
                    out.append(("RC-13", f"{path}.request.scopeRunIds: non-empty unique list required"))
        runs_raw = _array(fixture.get("runs"), path + ".runs", out, "RC-13")
        runs: dict[tuple[str, str], dict[str, Any]] = {}
        if runs_raw is not None:
            for i, run_record in enumerate(runs_raw):
                rpath = f"{path}.runs[{i}]"
                obj = _exact(run_record, {"runId", "projectId"}, set(), rpath, out, "RC-13")
                if obj is None:
                    continue
                if _run(obj.get("runId"), rpath + ".runId", out) and _project(obj.get("projectId"), rpath + ".projectId", out):
                    key = (obj["projectId"], obj["runId"])
                    if key in runs: out.append(("RC-13", f"{rpath}: duplicate Run"))
                    runs[key] = obj
        if request is not None and isinstance(request.get("scopeRunIds"), list):
            for run_id in request["scopeRunIds"]:
                if (project_id, run_id) not in runs:
                    out.append(("RC-13", f"{path}.request.scopeRunIds: {run_id!r} not owned by request ProjectId"))

        objects_raw = _array(fixture.get("objects"), path + ".objects", out, "RC-13")
        objects: dict[tuple[str, str, str], dict[str, Any]] = {}
        if objects_raw is not None:
            for i, record in enumerate(objects_raw):
                opath = f"{path}.objects[{i}]"
                obj = _exact(record, {"recordCasRef", "recordKind", "projectId", "containsSubject"}, set(), opath, out, "RC-13")
                if obj is None:
                    continue
                if (_ref(obj.get("recordCasRef"), opath + ".recordCasRef", out, "RC-13")
                        and _string(obj.get("recordKind"), opath + ".recordKind", out, "RC-13")
                        and _project(obj.get("projectId"), opath + ".projectId", out)):
                    key = (obj["projectId"], obj["recordCasRef"], obj["recordKind"])
                    if key in objects: out.append(("RC-13", f"{opath}: duplicate object key"))
                    objects[key] = obj
                if type(obj.get("containsSubject")) is not bool:
                    out.append(("RC-13", f"{opath}.containsSubject: expected boolean"))

        units_raw = _array(fixture.get("units"), path + ".units", out, "RC-13")
        units: dict[tuple[str, str], dict[str, Any]] = {}
        expected_edges: set[tuple[str, str, str, str | None, str, str, str | None]] = set()
        if units_raw is not None:
            for i, record in enumerate(units_raw):
                upath = f"{path}.units[{i}]"
                unit = _exact(record, {"unitId", "projectId", "runId", "objectRefs"}, set(), upath, out, "RC-13")
                if unit is None:
                    continue
                uid_ok = _string(unit.get("unitId"), upath + ".unitId", out, "RC-13", UNIT_RE)
                pid_ok = _project(unit.get("projectId"), upath + ".projectId", out)
                rid_ok = _run(unit.get("runId"), upath + ".runId", out)
                if pid_ok and rid_ok and (unit["projectId"], unit["runId"]) not in runs:
                    out.append(("RC-13", f"{upath}: unit Run does not exist in same ProjectId"))
                refs = _validate_scoped_refs(unit.get("objectRefs"), upath + ".objectRefs", unit.get("projectId"), out, "RC-13")
                if not refs:
                    out.append(("RC-13", f"{upath}.objectRefs: non-empty required"))
                if uid_ok and pid_ok:
                    key = (unit["projectId"], unit["unitId"])
                    if key in units: out.append(("RC-13", f"{upath}: duplicate unit"))
                    units[key] = unit
                    if rid_ok:
                        expected_edges.add((unit["projectId"], "run", unit["runId"], None, "unit", unit["unitId"], None))
                    for ref_record in refs:
                        raw_key = _raw_key(ref_record)
                        if raw_key not in objects:
                            out.append(("RC-13", f"{upath}: object ref not present in same ProjectId"))
                        expected_edges.add((unit["projectId"], "unit", unit["unitId"], None,
                                            "object", ref_record["recordCasRef"], ref_record["recordKind"]))

        pins_raw = _array(fixture.get("pins"), path + ".pins", out, "RC-13")
        pins: dict[tuple[str, str], dict[str, Any]] = {}
        if pins_raw is not None:
            for i, record in enumerate(pins_raw):
                ppath = f"{path}.pins[{i}]"
                pin = _exact(record, {"leaseId", "projectId", "runId", "state", "objectRef"}, set(), ppath, out, "RC-13")
                if pin is None:
                    continue
                lid_ok = _string(pin.get("leaseId"), ppath + ".leaseId", out, "RC-13", LEASE_RE)
                pid_ok = _project(pin.get("projectId"), ppath + ".projectId", out)
                rid_ok = _run(pin.get("runId"), ppath + ".runId", out)
                if pin.get("state") not in LEASE_STATES:
                    out.append(("RC-13", f"{ppath}.state: unknown pin state"))
                ref_parsed = _validate_ref_scope(pin.get("objectRef"), ppath + ".objectRef", pin.get("projectId"), out, "RC-13")
                if pid_ok and rid_ok and (pin["projectId"], pin["runId"]) not in runs:
                    out.append(("RC-13", f"{ppath}: pin Run not present in same ProjectId"))
                if ref_parsed is not None and ref_parsed not in objects:
                    out.append(("RC-13", f"{ppath}: pin object not present in same ProjectId"))
                if lid_ok and pid_ok:
                    key = (pin["projectId"], pin["leaseId"])
                    if key in pins: out.append(("RC-13", f"{ppath}: duplicate pin"))
                    pins[key] = pin
                    if rid_ok:
                        expected_edges.add((pin["projectId"], "run", pin["runId"], None, "pin", pin["leaseId"], None))
                    if ref_parsed is not None:
                        expected_edges.add((pin["projectId"], "pin", pin["leaseId"], None,
                                            "object", ref_parsed[1], ref_parsed[2]))

        edges_raw = _array(fixture.get("lineageEdges"), path + ".lineageEdges", out, "RC-13")
        actual_edges: set[tuple[str, str, str, str | None, str, str, str | None]] = set()
        if edges_raw is not None:
            for i, record in enumerate(edges_raw):
                epath = f"{path}.lineageEdges[{i}]"
                edge = _exact(record, {"projectId", "from", "to"}, set(), epath, out, "RC-13")
                if edge is None:
                    continue
                pid_ok = _project(edge.get("projectId"), epath + ".projectId", out)
                source = _endpoint(edge.get("from"), epath + ".from", out)
                target = _endpoint(edge.get("to"), epath + ".to", out)
                if pid_ok and source and target:
                    row = (edge["projectId"], source[0], source[1], source[2], target[0], target[1], target[2])
                    if row in actual_edges: out.append(("RC-13", f"{epath}: duplicate lineage edge"))
                    actual_edges.add(row)
                    nodes = {"run": runs, "unit": units, "object": objects, "pin": pins}
                    source_key = ((edge["projectId"], source[1], source[2]) if source[0] == "object"
                                  else (edge["projectId"], source[1]))
                    target_key = ((edge["projectId"], target[1], target[2]) if target[0] == "object"
                                  else (edge["projectId"], target[1]))
                    if source_key not in nodes[source[0]] or target_key not in nodes[target[0]]:
                        out.append(("RC-13", f"{epath}: malicious/cross-project endpoint"))
        if actual_edges != expected_edges:
            out.append(("RC-13", f"{path}.lineageEdges: must exactly encode all and only same-project Run/unit/object/pin relations"))

        expected = _exact(fixture.get("expected"), {"removed", "retainedBlocked", "untouched", "demotedOutsideScope"}, set(), path + ".expected", out, "RC-13")
        if expected is not None:
            for field in ("removed", "untouched"):
                rows = _array(expected.get(field), path + ".expected." + field, out, "RC-13")
                if rows is not None:
                    for i, key in enumerate(rows): _validate_object_key(key, f"{path}.expected.{field}[{i}]", out)
            blocked = _array(expected.get("retainedBlocked"), path + ".expected.retainedBlocked", out, "RC-13")
            if blocked is not None:
                for i, row in enumerate(blocked):
                    bpath = f"{path}.expected.retainedBlocked[{i}]"
                    obj = _exact(row, {"object", "blockingRunIds", "blockingLeaseIds"}, set(), bpath, out, "RC-13")
                    if obj is None: continue
                    _validate_object_key(obj.get("object"), bpath + ".object", out)
                    for field, pattern in (("blockingRunIds", RUN_RE), ("blockingLeaseIds", LEASE_RE)):
                        values = _array(obj.get(field), bpath + "." + field, out, "RC-13")
                        if values is not None:
                            for j, item in enumerate(values): _string(item, f"{bpath}.{field}[{j}]", out, "RC-13", pattern)
            if expected.get("demotedOutsideScope") is not False:
                out.append(("RC-13", f"{path}.expected.demotedOutsideScope: cross-scope demotion forbidden"))
        if not out:
            derived = derive_purge(fixture)
            if fixture.get("expected") != derived:
                out.append(("RC-13", f"{path}.expected: reachability/project reducer derives a different full partition"))
        return out
    except Exception as exc:
        out.append(("RC-TOTALITY", f"{path}: controlled purge validation failure {type(exc).__name__}: {exc}"))
        return out


def _apply_purge_mutation(fixtures: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    result = copy.deepcopy(fixtures)
    if kind == "cross-project-removal" or kind == "equal-digest-cross-project-alias":
        fixture = next(f for f in result if f["id"] == "PF-03-EQUAL-DIGEST-CROSS-PROJECT")
        foreign = next(obj for obj in fixture["objects"] if obj["projectId"] != fixture["request"]["projectId"])
        key = _object_key(foreign["projectId"], foreign["recordCasRef"], foreign["recordKind"])
        fixture["expected"]["untouched"].remove(key)
        fixture["expected"]["removed"].append(key)
    elif kind == "malicious-cross-project-lineage":
        fixture = next(f for f in result if f["id"] == "PF-03-EQUAL-DIGEST-CROSS-PROJECT")
        foreign_unit = next(unit for unit in fixture["units"] if unit["projectId"] != fixture["request"]["projectId"])
        fixture["lineageEdges"].append({"projectId": fixture["request"]["projectId"], "from": {"kind": "run", "id": fixture["request"]["scopeRunIds"][0]}, "to": {"kind": "unit", "id": foreign_unit["unitId"]}})
    elif kind == "remove-blocked-shared-object":
        fixture = next(f for f in result if f["id"] == "PF-02-BLOCKED-SHARED-WITHIN-PROJECT")
        row = fixture["expected"]["retainedBlocked"].pop()
        fixture["expected"]["removed"].append(row["object"])
    return result


def _validate_d9_axes(axes: Any, schema: Any, path: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if not isinstance(schema, dict) or not isinstance(schema.get("properties"), dict) or schema.get("additionalProperties") is not False:
        out.append(("RC-10", "$d9.scenarioAxesSchema: live schema is not a closed object"))
        return out
    props = schema["properties"]
    required = {key for key, rule in props.items() if isinstance(rule, dict) and rule.get("required") is True}
    obj = _exact(axes, required, set(props) - required, path, out, "RC-10")
    if obj is None:
        return out
    for key, value in obj.items():
        rule = props.get(key)
        if not isinstance(rule, dict):
            out.append(("RC-10", f"{path}.{key}: live schema rule malformed"))
            continue
        if rule.get("type") == "array":
            if not isinstance(value, list):
                out.append(("RC-10", f"{path}.{key}: expected array, got {type(value).__name__}"))
                continue
            allowed = rule.get("items", {}).get("enum") if isinstance(rule.get("items"), dict) else None
            if not isinstance(allowed, list):
                out.append(("RC-10", f"{path}.{key}: live item enum malformed"))
                continue
            if any(type(item) is not str or item not in allowed for item in value):
                out.append(("RC-10", f"{path}.{key}: item outside exact closed enum"))
            if len(value) != len(set(value)):
                out.append(("RC-10", f"{path}.{key}: duplicates forbidden"))
        else:
            allowed = rule.get("enum")
            if type(value) is not str:
                out.append(("RC-10", f"{path}.{key}: expected string enum, got {type(value).__name__}"))
            elif not isinstance(allowed, list) or value not in allowed:
                out.append(("RC-10", f"{path}.{key}: outside exact closed enum"))
    secondary = obj.get("secondaryDeficiencies")
    if isinstance(secondary, list):
        if secondary and obj.get("deficiency") == "none":
            out.append(("RC-10", f"{path}.secondaryDeficiencies: non-empty without primary"))
        if obj.get("deficiency") in secondary:
            out.append(("RC-10", f"{path}.secondaryDeficiencies: repeats primary"))
    return out


def _validate_d9_section(value: Any, d9c: Any, d9mod: Any, run_negatives: bool = True) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    section = _exact(value, {"source", "rule", "requiredDistinctions", "rows", "negativeFixtures"}, set(), "$d9Derivation", out, "RC-10")
    if section is None:
        return out
    if not isinstance(d9c, dict) or d9mod is None:
        out.append(("RC-10", "$d9Derivation: live D9 contract/checker unavailable"))
        return out
    if section.get("source") != "d9-exit-contract.v1.6.json#scenarioAxesSchema+referenceDerivation+classToExitCode":
        out.append(("RC-10", "$d9Derivation.source: must bind live closed D9 input/output contract"))
    if section.get("rule") != "Validate the complete closed axes object, derive class and all ordered codes with the live checker, then map that class to the live exit code.":
        out.append(("RC-10", "$d9Derivation.rule: exact closed derivation statement required"))
    rows = _array(section.get("rows"), "$d9Derivation.rows", out, "RC-10")
    row_map: dict[str, dict[str, Any]] = {}
    if rows is not None:
        for i, row_value in enumerate(rows):
            path = f"$d9Derivation.rows[{i}]"
            row = _exact(row_value, {"id", "situation", "axes", "expectedTermination", "expectedExitCode"}, set(), path, out, "RC-10")
            if row is None:
                continue
            rid = row.get("id")
            if not isinstance(rid, str) or rid in row_map:
                out.append(("RC-10", f"{path}.id: missing/duplicate"))
            elif isinstance(rid, str):
                row_map[rid] = row
            if not isinstance(row.get("situation"), str) or not row["situation"]:
                out.append(("RC-10", f"{path}.situation: required"))
            axis_hits = _validate_d9_axes(row.get("axes"), d9c.get("scenarioAxesSchema"), path + ".axes")
            out.extend(axis_hits)
            if axis_hits:
                continue
            try:
                cls = d9mod.derive_class(row["axes"])
                codes = d9mod.derive_codes(row["axes"], d9c["codeMaps"])
                expected = {"class": cls, **codes}
                if row.get("expectedTermination") != expected:
                    out.append(("RC-10", f"{path}.expectedTermination: asserted projection differs from complete derived payload {expected!r}"))
                exit_code = d9c["classToExitCode"].get(cls)
                if row.get("expectedExitCode") != exit_code or not _is_int(row.get("expectedExitCode")):
                    out.append(("RC-10", f"{path}.expectedExitCode: expected exact class mapping {exit_code!r}"))
            except (KeyError, TypeError, ValueError) as exc:
                out.append(("RC-10", f"{path}: D9 derivation failed ({exc})"))
    distinctions = section.get("requiredDistinctions")
    if not isinstance(distinctions, list) or any(type(item) is not str for item in distinctions):
        out.append(("RC-10", "$d9Derivation.requiredDistinctions: expected string array"))
    else:
        derived_codes: set[str] = set()
        for row in row_map.values():
            termination = row.get("expectedTermination")
            if isinstance(termination, dict):
                if isinstance(termination.get("errorCode"), str): derived_codes.add(termination["errorCode"])
                if isinstance(termination.get("reasonCodes"), list): derived_codes.update(x for x in termination["reasonCodes"] if isinstance(x, str))
        if not set(distinctions) <= derived_codes:
            out.append(("RC-10", "$d9Derivation.requiredDistinctions: at least one full remedy class has no row"))
        multi = row_map.get("RD-09-MULTI-DEFICIENCY", {}).get("expectedTermination", {})
        if not isinstance(multi, dict) or len(multi.get("reasonCodes", [])) < 2:
            out.append(("RC-10", "$d9Derivation.rows: ordered multi-deficiency full payload is required"))
    if run_negatives:
        negative = _array(section.get("negativeFixtures"), "$d9Derivation.negativeFixtures", out, "RC-10")
        kinds_expected = {"drop-secondary-reason", "undeclared-axis", "missing-axis", "type-confused-axis"}
        seen: set[str] = set()
        if negative is not None:
            for i, case in enumerate(negative):
                obj = _exact(case, {"id", "kind", "baseRowId", "expectedInvariant"}, set(), f"$d9Derivation.negativeFixtures[{i}]", out, "RC-10")
                if obj is None: continue
                kind = obj.get("kind")
                if kind not in kinds_expected or kind in seen:
                    out.append(("RC-10", f"$d9Derivation.negativeFixtures[{i}].kind: duplicate/unknown"))
                    continue
                seen.add(kind)
                mutated = copy.deepcopy(section)
                _apply_d9_mutation(mutated, kind, obj.get("baseRowId"))
                hits = {inv for inv, _ in _validate_d9_section(mutated, d9c, d9mod, False)}
                if obj.get("expectedInvariant") != "RC-10" or "RC-10" not in hits:
                    out.append(("RC-10", f"$d9Derivation.negativeFixtures[{i}]: mutation escaped"))
        if seen != kinds_expected:
            out.append(("RC-10", "$d9Derivation.negativeFixtures: exact P13/P14 and missing/type controls required"))
    return out


def _apply_d9_mutation(section: dict[str, Any], kind: str, row_id: Any) -> None:
    row = next(row for row in section["rows"] if row["id"] == row_id)
    if kind == "drop-secondary-reason":
        row["expectedTermination"]["reasonCodes"] = row["expectedTermination"]["reasonCodes"][:1]
    elif kind == "undeclared-axis":
        row["axes"]["futureAxis"] = "accepted"
    elif kind == "missing-axis":
        del row["axes"]["durability"]
    elif kind == "type-confused-axis":
        row["axes"]["admission"] = True


EXPECTED_CUSTODY_POLICY = {
    "selectionOwner": "orchestration host applies an explicit project policy; producers never select custody",
    "perObligation": "frozen evidence or exact deterministic regeneration closure is selected per proof obligation",
    "recommendedDefaultPosture": {
        "recommendation": "no managed durable user-derived write without an explicit project storage and retention policy",
        "whenPolicyMissing": "advisory/ephemeral only, or reject durable/authoritative evidence request",
        "status": "AWAITING-PRODUCT-DISPOSITION",
        "authority": "product-dispositions.v1.json#pendingDecisions.CD-RT-5",
        "currentProductState": "BLOCKED_ON_PHASE_1A",
        "durableDefault": "UNSELECTED",
    },
}

EXPECTED_AUTHORITY = {
    "candidateRole": "architecture authoring candidate; may specify but cannot accept, sign, seal, or apply product/integration state",
    "mayRecordProductAcceptance": False,
    "productAuthority": {"artifact": "product-dispositions.v1.json", "decisionId": "CD-RT-5", "requiredLiveState": "BLOCKED_ON_PHASE_1A"},
    "independentReview": {"state": "AWAITING-INDEPENDENT-COMBINED-REREVIEW", "reviewerMustNotHaveAuthored": ["evaluation-proof.v5.json", "retention-tiers.v10.json", "check-evaluation-proof.py", "check-retention-custody.py"]},
    "candidateState": "NOT-APPLIED",
}

EXPECTED_INTEGRATION = {
    "candidateState": "NOT-APPLIED",
    "externalClosureClaim": "NONE",
    "pending": [
        {"target": "threat-model.v3.json#V10", "currentState": "UNRESOLVED", "applicationState": "NOT-APPLIED"},
        {"target": "product-dispositions.v1.json#CD-RT-5", "currentState": "BLOCKED_ON_PHASE_1A", "applicationState": "NOT-APPLIED"},
        {"target": "operability.v2.json#G19", "currentState": "BLOCKED-NO-MECHANISM", "applicationState": "NOT-APPLIED"},
        {"target": "claim-register.v1.json#ARCH.RETENTION-TIERS", "currentState": "STALE-CONTRADICTORY", "applicationState": "NOT-APPLIED"},
        {"target": "architecture/06-evidence-and-persistence.md", "currentState": "STALE-CONTRADICTORY", "applicationState": "NOT-APPLIED"},
        {"target": "architecture/09-open-decisions.md", "currentState": "STALE-CONTRADICTORY", "applicationState": "NOT-APPLIED"},
    ],
    "nextTransitionAuthority": "independent combined Evidence/EP/RT/OP/store reviewer first; product owner separately decides CD-RT-5; coordinator alone may serialize later integration",
}

EXPECTED_ASSURANCE = {
    "state": "SPECIFIED",
    "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
    "independentRereview": "REQUIRED-COMBINED-PACKET",
    "runtimeDemonstrated": False,
    "productDisposition": "BLOCKED_ON_PHASE_1A",
    "why": "Pure authority-seal, semantic closure, availability, lease, purge, and D9 derivations are executable specification evidence only; coordinated Evidence/OP/store admission and identity timing, production runtime, durable ledger, physical storage, and independent acceptance are not demonstrated.",
}

EXPECTED_RETAINED_RESIDUALS = [
    {"id": "A1-RTV4-02", "class": "MEASUREMENT", "statement": "Runtime overhead, scale, and operational behavior remain unmeasured."},
    {"id": "RC-R-01", "class": "STORAGE-ARCHITECTURE", "statement": "Lexical ProjectId paths do not demonstrate physical containment or backend isolation."},
    {"id": "RC-R-02", "class": "PROCESS", "statement": "An independent reviewer who authored none of the v5/v10 artifacts or owned checkers must rereview the combined packet."},
    {"id": "A-PRIME-IDENTITY-TIMING", "class": "COORDINATED-CONTRACT", "statement": "Narrow D9 v1.6, OP, and scope-correction EC-3 identity-timing repair remains required; no D9 code/class vocabulary change is authorized here."},
    {"id": "CD-RT-5", "class": "PRODUCT", "statement": "The recommended default posture remains BLOCKED_ON_PHASE_1A under product authority."},
]

EXPECTED_RAW_PHYSICAL_IDENTITY_CONTRACT = {
    "type": "RawObjectKeyV1",
    "key": ["projectId", "recordCasRef", "recordKind"],
    "fields": ["projectId", "recordCasRef", "recordKind"],
    "rawCasPattern": r"^sha256:[0-9a-f]{64}$",
    "semanticRefsForbiddenIn": ["unit.objectRefs", "availability.objectStates", "lease.objects", "lease.pins", "inventory", "objectPath", "purge.targets", "purge.lineage"],
    "bindingAuthority": "A semantic binding is derived witness only; AVAILABLE requires the exact raw target key and never the binding alone.",
    "pathTemplate": "projects/<ProjectId>/objects/<recordKind>/sha256/<digestHex>",
    "negativeControls": ["semantic-ref-as-path-key", "semantic-ref-as-purge-key"],
}


def _authority_guard(value: Any, product: Any) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if not isinstance(value, dict):
        return [("RC-14", "$contract: candidate must be an object")]
    if value.get("custodyPolicy") != EXPECTED_CUSTODY_POLICY:
        out.append(("RC-14", "$contract.custodyPolicy: recursively closed pending policy shape drifted"))
    if value.get("authority") != EXPECTED_AUTHORITY:
        out.append(("RC-14", "$contract.authority: recursively closed authoring authority shape drifted"))
    if value.get("integrationState") != EXPECTED_INTEGRATION:
        out.append(("RC-14", "$contract.integrationState: recursively closed non-applying pending shape drifted"))
    live = None
    if isinstance(product, dict):
        pending = product.get("pendingDecisions")
        if isinstance(pending, dict):
            decision = pending.get("CD-RT-5")
            if isinstance(decision, dict):
                live = decision.get("status")
    if live != "BLOCKED_ON_PHASE_1A":
        out.append(("RC-14", f"$product.CD-RT-5: exact live state must be BLOCKED_ON_PHASE_1A, got {live!r}"))
    if value.get("custodyPolicy") == EXPECTED_CUSTODY_POLICY:
        if value["custodyPolicy"]["recommendedDefaultPosture"]["currentProductState"] != live:
            out.append(("RC-14", "$contract.custodyPolicy: does not match live product authority"))

    forbidden_keys = {"resolves", "productdecision", "productacceptance", "signoff", "signedoff", "approval", "acceptedby"}
    forbidden_values = {"RESOLVED", "COMPLETE", "COMPLETED", "ACCEPTED", "SIGNED", "SIGNEDOFF", "PRODUCTSIGNEDOFF", "APPROVED", "SEALED"}
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                normalized_key = re.sub(r"[^a-z]", "", str(key).lower())
                if normalized_key in forbidden_keys:
                    out.append(("RC-14", f"{path}.{key}: forbidden authority/closure declaration"))
                if isinstance(child, str) and normalized_key in {"status", "state", "currentstate", "disposition", "verdict", "outcome"}:
                    normalized_value = re.sub(r"[^A-Z]", "", child.upper())
                    if normalized_value in forbidden_values:
                        out.append(("RC-14", f"{path}.{key}: forbidden positive authority state {child!r}"))
                walk(child, path + "." + str(key))
        elif isinstance(node, list):
            for i, child in enumerate(node): walk(child, f"{path}[{i}]")
    walk(value, "$contract")
    return out


def _cross_contract_project_join(ctx: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    try:
        ri_pattern = ctx["ri"]["projectIdContract"]["representation"]["regex"]
        c2_project = ctx["c2"]["planIntent"]["wireTypes"]["projectId"]["pattern"]
        c2_run = ctx["c2"]["planIntent"]["wireTypes"]["runId"]["pattern"]
        tm_project = ctx["tm"]["storageNamespace"]["projectId"]["canonicalTextPattern"]
        tm_object = ctx["tm"]["storageNamespace"]["objectId"]["wirePattern"]
        tm_path = ctx["tm"]["storageNamespace"]["layout"]["casObject"]
        join = ctx["storage"]["identityJoin"]
    except (KeyError, TypeError) as exc:
        return [("RC-13", f"live RI/C2/TM/storage namespace contract malformed ({exc})")]
    if {ri_pattern, c2_project, tm_project} != {r"^prj1-[0-9a-f]{64}$"}:
        out.append(("RC-13", "PROJECT-ID-V1 grammar disagrees across RI/C2/TM"))
    if c2_run != r"^run1:[0-9a-f]{64}$" or tm_object != r"^sha256:[0-9a-f]{64}$":
        out.append(("RC-13", "C2 RunId or TM object wire grammar drift"))
    if tm_path != "<admittedStorageRoot>/projects/<ProjectId>/objects/sha256/<digestHex>":
        out.append(("RC-13", "live TM object path is not the canonical per-project namespace"))
    expected_join = {
        "contractId": "PROJECT-ID-V1", "source": "resolved-inputs.v2.json#projectIdContract",
        "consumer": "threat-model.v3.json#storageNamespace.projectId",
        "c2Wire": "c2-plan-stage-schema.v3.json#planIntent.wireTypes.projectId",
    }
    if join != expected_join:
        out.append(("RC-13", "storage adjudication identityJoin drifted from live PROJECT-ID-V1 owner"))
    return out


def _find_proof_vector(proof_contract: Any, vector_id: Any) -> dict[str, Any] | None:
    if not isinstance(proof_contract, dict) or not isinstance(proof_contract.get("positiveVectors"), list):
        return None
    for vector in proof_contract["positiveVectors"]:
        if (isinstance(vector, dict) and vector.get("id") == vector_id
                and isinstance(vector.get("bundle"), dict)
                and isinstance(vector.get("verifiedAuthorityInput"), dict)):
            return vector
    return None


def _semantic_physical_key_findings(value: Any, semantic_refs: set[str]) -> list[tuple[str, str]]:
    """Reject semantic commitments and legacy untyped refs in every RT10 physical API."""
    out: list[tuple[str, str]] = []

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            if "ref" in node:
                out.append(("RC-11", f"{path}.ref: legacy untyped physical reference is forbidden"))
            if node.get("recordCasRef") in semantic_refs:
                out.append(("RC-11", f"{path}.recordCasRef: SemanticCommitmentRef used as RawCasRef"))
            if node.get("kind") == "object" and node.get("id") in semantic_refs:
                out.append(("RC-13", f"{path}.id: SemanticCommitmentRef used as a lineage/path object key"))
            for key, child in node.items():
                walk(child, f"{path}.{key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")

    walk(value, "$contract")
    return out


def _apply_closure_overrides(records: list[dict[str, Any]], overrides: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = copy.deepcopy(records)
    by_ref = {_raw_key(state): state for record in result for state in record["objectStates"]}
    for override in overrides:
        by_ref[_raw_key(override)]["state"] = override["state"]
    return result


def _apply_closure_mutation(closure: dict[str, Any], availability: list[dict[str, Any]], kind: str) -> None:
    if kind == "empty-closure":
        closure["proofRefs"] = []
        closure["dependencyEdges"] = []
        closure["units"] = []
        closure["closureCommitment"] = semantic_closure_commitment([])
    elif kind == "proof-ref-removed":
        closure["proofRefs"].pop()
    elif kind == "unit-ref-removed":
        unit = closure["units"][0]
        unit["objectRefs"].pop()
        closure["closureCommitment"] = semantic_closure_commitment(closure["units"])
    elif kind == "reference-alias":
        source = closure["units"][0]
        alias = copy.deepcopy(source)
        closure["units"].append(alias)
        closure["closureCommitment"] = semantic_closure_commitment(closure["units"])
    elif kind == "weaken-minimum":
        unit = next(unit for unit in closure["units"] if unit["requiredForCapability"] == "verifiable")
        unit["requiredForCapability"] = "recorded"
        closure["closureCommitment"] = semantic_closure_commitment(closure["units"])
    elif kind == "strengthen-minimum":
        unit = next(unit for unit in closure["units"] if unit["requiredForCapability"] == "verifiable")
        unit["requiredForCapability"] = "replayable"
        closure["closureCommitment"] = semantic_closure_commitment(closure["units"])
    elif kind == "target-purge-retains-authority":
        record = next(record for record in availability if len(record["objectStates"]) > 1)
        record["objectStates"][0]["state"] = "PURGED"
        record["expectedEffectiveCapability"] = closure["sealedCapability"]
    elif kind == "dependency-edge-removed":
        closure["dependencyEdges"].pop()
    elif kind == "closure-root-run-id":
        closure["runId"] = "run1:" + "0" * 64
    elif kind == "unit-run-id":
        closure["units"][0]["runId"] = "run1:" + "0" * 64
    elif kind == "runid-derived-unit-id":
        unit = closure["units"][0]
        unit["unitId"] = "unit3:sha256:" + hashlib.sha256((unit["unitId"] + "run1:" + "0" * 64).encode()).hexdigest()
    elif kind == "semantic-object-states":
        closure["units"][0]["objectStates"] = copy.deepcopy(availability[0]["objectStates"])
    elif kind == "semantic-effective-capability":
        closure["effectiveCapability"] = closure["sealedCapability"]
    elif kind == "terminal-run-seal-child":
        closure["proofRefs"].append({
            "identityKind": "raw-cas", "projectId": closure["projectId"],
            "recordCasRef": "sha256:" + "61" * 32, "recordKind": "terminal-run-seal",
            "requiredForCapability": "verifiable",
        })
    elif kind == "old-v2-tag-substitution":
        ep = _load_eval_module()
        legacy = [encode_semantic_custody_unit(unit) + ep.frame_component(0x63, "run1:" + "0" * 64)
                  for unit in closure["units"]]
        closure["closureCommitment"] = "sha256:" + hashlib.sha256(b"".join(legacy)).hexdigest()
    elif kind == "old-v2-domain-substitution":
        closure["closureCommitment"] = _load_eval_module().commit(
            "capability-closure", [encode_semantic_custody_unit(unit) for unit in closure["units"]])
    elif kind == "semantic-ref-as-cas":
        closure["proofRefs"][0]["recordCasRef"] = closure["semanticRoots"][0]["semanticRef"]
    elif kind == "binding-only-available":
        binding = closure["semanticObjectBindings"][0]
        availability[0]["objectStates"].append({
            "projectId": binding["projectId"], "recordCasRef": binding["semanticRef"],
            "recordKind": binding["recordKind"], "state": "AVAILABLE",
        })
    elif kind == "semantic-binding-missing":
        closure["semanticObjectBindings"].pop()
    elif kind == "semantic-binding-duplicate":
        closure["semanticObjectBindings"].append(copy.deepcopy(closure["semanticObjectBindings"][0]))
    elif kind == "semantic-binding-cross-project":
        closure["semanticObjectBindings"][0]["projectId"] = "prj1-" + "b" * 64
    elif kind == "hidden-unreachable-binding":
        closure["semanticObjectBindings"].append({
            "projectId": closure["projectId"], "semanticDomain": "activation-manifest-v1",
            "semanticRef": "sha256:" + "7" * 64, "recordCasRef": "sha256:" + "8" * 64,
            "recordKind": "ActivationManifestV1",
        })
    elif kind == "authority-edge-role-downgrade":
        edge = next(row for row in closure["dependencyEdges"]
                    if row["role"] == "evaluation-authority-seal-record")
        edge["role"] = "policy-verifier"
    elif kind == "minimum-downgrade":
        row = next(row for row in closure["proofRefs"] if row["requiredForCapability"] == "verifiable")
        row["requiredForCapability"] = "recorded"
    elif kind == "versioning-raw-retyped-semantic":
        row = next(row for row in closure["proofRefs"] if row["recordKind"] == "historical-manifest")
        row["identityKind"] = "semantic-commitment"
    elif kind == "downstream-field-in-binding":
        closure["semanticObjectBindings"][0]["runId"] = "run1:" + "0" * 64


def _canonical_json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _check_closure_grammar(section: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    grammar = section.get("closureGrammar")
    _set_closure_grammar(grammar)
    try:
        digest = _canonical_json_sha256(grammar)
        if section.get("closureGrammarSha256") != digest:
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammarSha256: does not recompute"))
        if digest != EXPECTED_CLOSURE_GRAMMAR_SHA256:
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammar: differs from pinned v3 grammar"))
        rows = grammar.get("tagRegistry")
        expected_tags = [f"0x{x:02x}" for x in range(0x70, 0x7A)]
        if not isinstance(rows, list) or [row.get("tag") for row in rows if isinstance(row, dict)] != expected_tags:
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammar.tagRegistry: must declare 0x70..0x79 exactly once in order"))
        if not isinstance(rows, list) or len(rows) != 10 or "RESERVED-FORBIDDEN" not in str(rows[3].get("role", "")):
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammar: legacy RunId tag 0x73 must remain reserved and forbidden"))
        for role in ("SemanticCustodyUnitV3 record", "unitId component", "projectId component",
                     "requiredForCapability component", "objectRefs item blob",
                     "recordCasRef component inside item", "object ProjectId component inside item",
                     "recordKind component inside item",
                     "sorted objectRefs list blob"):
            _closure_tag(role)
        if grammar.get("emissionOrder") != ["0x70", "0x71", "0x72", "0x74", "0x79", "0x75", "0x76", "0x77", "0x78"]:
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammar.emissionOrder: nesting/order drift"))
        uid = grammar.get("unitIdContract")
        if not isinstance(uid, dict) or uid.get("id") != "UNIT-ID-V3" or uid.get("textPattern") != r"^unit3:sha256:[0-9a-f]{64}$" or uid.get("domainUtf8") != UNIT_ID_DOMAIN.decode():
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammar.unitIdContract: UNIT-ID-V3 drift"))
        forbidden_unit = ["runId", "runSealRef", "semanticRef", "objectStates", "effectiveCapability", "expectedEffectiveCapability", "lease", "fence", "ledger", "clocks", "physicalLocators"]
        forbidden_closure = ["runId", "runSealRef", "expectedEffectiveCapability", "effectiveCapability", "objectStates", "unitAvailabilityRecords", "lease", "fence", "ledger", "clocks", "physicalLocators"]
        if grammar.get("semanticUnitSchema", {}).get("forbidden") != forbidden_unit or grammar.get("semanticClosureSchema", {}).get("forbidden") != forbidden_closure:
            out.append(("RC-11", "$contract.capabilityClosure.closureGrammar: semantic forbidden-field boundary drift"))

        goldens = section.get("closureGoldens")
        if not isinstance(goldens, dict) or set(goldens) != {"unit", "closure"}:
            out.append(("RC-11", "$contract.capabilityClosure.closureGoldens: must be exact unit+closure object"))
        else:
            unit_g = goldens["unit"]
            if not isinstance(unit_g, dict) or set(unit_g) != {"id", "value", "unitIdPreimageHex", "derivedUnitId", "encodedHex", "encodedSha256"}:
                out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.unit: shape drift"))
            else:
                unit = unit_g["value"]
                preimage = unit_id_preimage(unit["projectId"], unit["requiredForCapability"], unit["objectRefs"])
                encoded = encode_semantic_custody_unit(unit)
                if unit_g.get("unitIdPreimageHex") != preimage.hex() or unit_g.get("derivedUnitId") != derive_unit_id(unit["projectId"], unit["requiredForCapability"], unit["objectRefs"]):
                    out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.unit: UNIT-ID-V3 golden disagrees"))
                if unit_g.get("encodedHex") != encoded.hex() or unit_g.get("encodedSha256") != "sha256:" + hashlib.sha256(encoded).hexdigest():
                    out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.unit: encoded bytes/hash disagree"))
            closure_g = goldens["closure"]
            required = {"id", "inputUnitEncodedHex", "sortedUniqueUnitEncodedHex", "leafHashHex", "merkleRootHex", "outerPreimageHex", "commitment"}
            if not isinstance(closure_g, dict) or set(closure_g) != required:
                out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.closure: shape drift"))
            else:
                units = section.get("semanticClosure", {}).get("units", [])
                encoded_units = [encode_semantic_custody_unit(unit) for unit in units]
                ordered = sorted(set(encoded_units))
                leaves = [hashlib.sha256(b"\x00" + len(item).to_bytes(8, "big") + item).digest() for item in ordered]
                level = leaves[:]
                while len(level) > 1:
                    level = [hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest()
                             if i + 1 < len(level) else level[i]
                             for i in range(0, len(level), 2)]
                root = level[0]
                ep = _load_eval_module()
                outer = ep.commitment_preimage("semantic-capability-closure-v3", encoded_units)
                if closure_g.get("inputUnitEncodedHex") != [x.hex() for x in encoded_units] or closure_g.get("sortedUniqueUnitEncodedHex") != [x.hex() for x in ordered]:
                    out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.closure: input/sort bytes disagree"))
                if closure_g.get("leafHashHex") != [x.hex() for x in leaves] or closure_g.get("merkleRootHex") != root.hex():
                    out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.closure: Merkle bytes disagree"))
                if closure_g.get("outerPreimageHex") != outer.hex() or closure_g.get("commitment") != "sha256:" + hashlib.sha256(outer).hexdigest():
                    out.append(("RC-11", "$contract.capabilityClosure.closureGoldens.closure: outer preimage/commitment disagree"))
    except Exception as exc:
        out.append(("RC-11", f"$contract.capabilityClosure.closureGrammar: cannot drive encoders ({type(exc).__name__}: {exc})"))
    return out


def _check_impl(value: Any, ctx: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    if ctx.get("errors"):
        findings.extend(f"context: {error}" for error in ctx["errors"])
    root_out: list[tuple[str, str]] = []
    contract = _exact(value, TOP_KEYS, set(), "$contract", root_out, "RC-15")
    findings.extend(f"{inv}: {msg}" for inv, msg in root_out)
    if contract is None:
        return findings
    if contract.get("artifact") != "opensip.retention-custody" or contract.get("version") != EXPECTED_VERSION:
        findings.append("RC-15: artifact/version must be opensip.retention-custody integer 10")
    if contract.get("status") != "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW-AND-PRODUCT-DISPOSITION":
        findings.append("RC-14: v10 must remain an unapplied candidate awaiting combined review and product gates")
    if contract.get("claimId") != "ARCH.RETENTION-TIERS":
        findings.append("RC-15: claimId must be exact")
    if contract.get("supersedesAsArchitectureCandidate") != "artifacts/retention-tiers.v9.json (preserved byte-identical; rejected intermediate successor only)":
        findings.append("RC-15: v10 must name the byte-preserved rejected v9 predecessor")
    if contract.get("sealRecommendation") != "DO NOT SEAL OR APPLY. EP4/RT9 are rejected intermediates; await coordinated Evidence/OP/store and narrow D9/scope identity-timing successors, independent combined-packet rereview, separate CD-RT-5 product disposition, and coordinator-owned integration. V10 remains UNRESOLVED.":
        findings.append("RC-14: sealRecommendation must preserve the exact no-self-accept boundary")
    if contract.get("rawPhysicalIdentityContract") != EXPECTED_RAW_PHYSICAL_IDENTITY_CONTRACT:
        findings.append("RC-11: rawPhysicalIdentityContract must exactly bind every physical API to (ProjectId,RawCasRef,recordKind)")

    epmod, proof_contract = ctx.get("epmod"), ctx.get("proof")
    closure_out: list[tuple[str, str]] = []
    section = _exact(contract.get("capabilityClosure"), {
        "source", "closureGrammarSha256", "closureGrammar", "closureGoldens",
        "semanticClosure", "unitAvailabilityRecords", "availabilityFixtures",
        "negativeFixtures", "grammarNegativeControls", "historicalNegativeControls",
    }, set(), "$contract.capabilityClosure", closure_out, "RC-11")
    proof_bundle = None
    proof_authority = None
    if section is not None:
        closure_out.extend(_check_closure_grammar(section))
        source = _exact(section.get("source"), {
            "artifact", "sha256", "acceptedVectorId", "requiredCheckerApi",
        }, set(), "$contract.capabilityClosure.source", closure_out, "RC-11")
        expected_api = [
            "resolve_semantic_object_bindings", "derive_semantic_requirements",
            "derive_raw_proof_requirements", "derive_transitive_requirements",
            "encode_semantic_object_binding", "derive_unit_id", "encode_semantic_custody_unit",
            "semantic_closure_commitment", "derive_effective_capability",
        ]
        if source is not None:
            if source.get("artifact") != PROOF or source.get("sha256") != ctx.get("proofSha256"):
                closure_out.append(("RC-11", "capability closure source must hash-bind the concrete live evaluation-proof.v5.json"))
            if source.get("requiredCheckerApi") != expected_api:
                closure_out.append(("RC-11", "$contract.capabilityClosure.source.requiredCheckerApi: exact EP5/RT10 typed derivation seam required"))
            proof_vector = _find_proof_vector(proof_contract, source.get("acceptedVectorId"))
            if proof_vector is None:
                closure_out.append(("RC-11", "acceptedVectorId does not resolve to a concrete EP5 positive bundle and verified authority input"))
            else:
                proof_bundle = proof_vector["bundle"]
                proof_authority = proof_vector["verifiedAuthorityInput"]
        if epmod is None or not isinstance(proof_contract, dict):
            closure_out.append(("RC-11", "evaluation-proof v5 contract/checker unavailable"))
        else:
            for name in expected_api[:5]:
                if not callable(getattr(epmod, name, None)):
                    closure_out.append(("RC-11", f"evaluation-proof v5 checker lacks required callable {name}"))
            for name in expected_api[5:]:
                if not callable(globals().get(name)):
                    closure_out.append(("RC-11", f"retention v10 checker lacks required callable {name}"))
            proof_findings = ctx.get("proofFindings")
            if not isinstance(proof_findings, list):
                proof_findings = epmod.check(proof_contract)
            if proof_findings:
                closure_out.append(("RC-11", f"live evaluation-proof v5 contract is not accepted ({proof_findings[0]})"))

        if proof_authority is not None and epmod is not None:
            try:
                semantic_refs = {
                    row["semanticRef"] for row in epmod.derive_semantic_requirements(proof_authority)
                }
                closure_out.extend(_semantic_physical_key_findings(contract, semantic_refs))
            except (KeyError, TypeError, ValueError) as exc:
                closure_out.append(("RC-11", f"semantic/raw physical-key audit failed closed ({exc})"))

        base_closure = section.get("semanticClosure")
        base_availability = section.get("unitAvailabilityRecords")
        if not isinstance(base_availability, list):
            closure_out.append(("RC-12", "$contract.capabilityClosure.unitAvailabilityRecords: required array outside semantic closure"))
        if proof_bundle is not None and proof_authority is not None:
            closure_out.extend(validate_capability_closure(
                proof_bundle, proof_authority, base_closure, base_availability))
            if isinstance(base_closure, dict) and isinstance(base_availability, list):
                try:
                    semantic = epmod.derive_semantic_requirements(proof_authority)
                    raw = epmod.derive_raw_proof_requirements(proof_bundle, proof_authority)
                    if len(semantic) != 2 or {row.get("identityKind") for row in semantic} != {"semantic-commitment"}:
                        closure_out.append(("RC-11", "$closure: exact two typed semantic roots are required"))
                    if len(raw) != 22 or {row.get("identityKind") for row in raw} != {"raw-cas"}:
                        closure_out.append(("RC-11", "$closure: exact typed raw physical closure is required"))
                    if {row["semanticRef"] for row in semantic} & {row["recordCasRef"] for row in raw}:
                        closure_out.append(("RC-11", "$closure: semantic commitments and raw CAS identities alias"))
                    if "runId" in proof_bundle or "runSealRef" in proof_bundle:
                        closure_out.append(("RC-11", "$proof: pre-evaluation semantic bundle cannot be a terminal Run/run-seal child"))
                except (KeyError, TypeError, ValueError) as exc:
                    closure_out.append(("RC-11", f"$proof: authority-seal dependency derivation failed ({exc})"))

                fixtures = _array(section.get("availabilityFixtures"), "$contract.capabilityClosure.availabilityFixtures", closure_out, "RC-12")
                if fixtures is not None:
                    seen: set[str] = set()
                    expected_fixture_ids = {"AF-01-ALL-AVAILABLE", "AF-02-REPLAY-MISSING", "AF-03-VERIFY-PURGED", "AF-04-VERIFY-OUTAGE"}
                    base_refs = {
                        _raw_key(record) for unit in base_closure.get("units", [])
                        if isinstance(unit, dict) for record in unit.get("objectRefs", [])
                        if isinstance(record, dict) and all(isinstance(record.get(key), str)
                                                           for key in ("projectId", "recordCasRef", "recordKind"))
                    }
                    base_run_ids = {
                        record.get("runId") for record in base_availability
                        if isinstance(record, dict) and isinstance(record.get("runId"), str)
                    }
                    for i, fixture in enumerate(fixtures):
                        path = f"$contract.capabilityClosure.availabilityFixtures[{i}]"
                        obj = _exact(fixture, {"id", "runId", "stateOverrides", "expectedEffectiveCapability"}, set(), path, closure_out, "RC-12")
                        if obj is None:
                            continue
                        if not isinstance(obj.get("id"), str) or obj["id"] in seen:
                            closure_out.append(("RC-12", f"{path}.id: missing/duplicate"))
                        else:
                            seen.add(obj["id"])
                        if not _run(obj.get("runId"), path + ".runId", closure_out, "RC-12") or obj.get("runId") not in base_run_ids:
                            closure_out.append(("RC-12", f"{path}.runId: must join the mutable availability records"))
                        overrides_raw = _array(obj.get("stateOverrides"), path + ".stateOverrides", closure_out, "RC-12")
                        overrides: list[dict[str, Any]] = []
                        seen_refs: set[tuple[str, str, str]] = set()
                        if overrides_raw is not None:
                            for j, override in enumerate(overrides_raw):
                                opath = f"{path}.stateOverrides[{j}]"
                                row = _exact(override, {"recordCasRef", "projectId", "recordKind", "state"}, set(), opath, closure_out, "RC-12")
                                if row is None:
                                    continue
                                _ref(row.get("recordCasRef"), opath + ".recordCasRef", closure_out, "RC-12")
                                _string(row.get("recordKind"), opath + ".recordKind", closure_out, "RC-12")
                                if (not _project(row.get("projectId"), opath + ".projectId", closure_out, "RC-12")
                                        or row.get("projectId") != base_closure.get("projectId")):
                                    closure_out.append(("RC-12", f"{opath}: ProjectId mismatch"))
                                if row.get("state") not in UNIT_STATES:
                                    closure_out.append(("RC-12", f"{opath}.state: unknown"))
                                if all(isinstance(row.get(key), str) for key in ("projectId", "recordCasRef", "recordKind")):
                                    raw_key = _raw_key(row)
                                    if raw_key not in base_refs or raw_key in seen_refs:
                                        closure_out.append(("RC-12", f"{opath}: unknown/duplicate raw physical key"))
                                    else:
                                        seen_refs.add(raw_key)
                                overrides.append(row)
                        try:
                            records = _apply_closure_overrides(base_availability, overrides)
                            fixture_out: list[tuple[str, str]] = []
                            _validate_availability_records(records, base_closure["units"], base_closure["projectId"], fixture_out)
                            closure_out.extend(fixture_out)
                            effective = derive_effective_capability(
                                base_closure["sealedCapability"], base_closure["units"], records)
                            if obj.get("expectedEffectiveCapability") != effective:
                                closure_out.append(("RC-12", f"{path}: independently derived {effective}, asserted {obj.get('expectedEffectiveCapability')!r}"))
                        except (KeyError, TypeError, ValueError) as exc:
                            closure_out.append(("RC-12", f"{path}: cannot derive fixture ({exc})"))
                    if seen != expected_fixture_ids:
                        closure_out.append(("RC-12", "$contract.capabilityClosure.availabilityFixtures: exact four availability cases required"))

                negative = _array(section.get("negativeFixtures"), "$contract.capabilityClosure.negativeFixtures", closure_out, "RC-11")
                required_kinds = {
                    "empty-closure", "proof-ref-removed", "unit-ref-removed", "reference-alias",
                    "weaken-minimum", "strengthen-minimum", "target-purge-retains-authority",
                    "dependency-edge-removed", "closure-root-run-id", "unit-run-id",
                    "runid-derived-unit-id", "semantic-object-states", "semantic-effective-capability",
                    "terminal-run-seal-child", "old-v2-tag-substitution", "old-v2-domain-substitution",
                    "semantic-ref-as-cas", "binding-only-available", "semantic-binding-missing",
                    "semantic-binding-duplicate", "semantic-binding-cross-project",
                    "hidden-unreachable-binding", "authority-edge-role-downgrade",
                    "minimum-downgrade", "versioning-raw-retyped-semantic",
                    "downstream-field-in-binding",
                }
                seen_kinds: set[str] = set()
                if negative is not None:
                    for i, case in enumerate(negative):
                        obj = _exact(case, {"id", "kind", "expectedInvariant"}, set(), f"$contract.capabilityClosure.negativeFixtures[{i}]", closure_out, "RC-11")
                        if obj is None:
                            continue
                        kind = obj.get("kind")
                        if kind not in required_kinds or kind in seen_kinds:
                            closure_out.append(("RC-11", f"negativeFixtures[{i}].kind duplicate/unknown"))
                            continue
                        seen_kinds.add(kind)
                        mutated_closure = copy.deepcopy(base_closure)
                        mutated_availability = copy.deepcopy(base_availability)
                        try:
                            _apply_closure_mutation(mutated_closure, mutated_availability, kind)
                            hits = {inv for inv, _ in validate_capability_closure(
                                proof_bundle, proof_authority, mutated_closure, mutated_availability)}
                        except (KeyError, TypeError, ValueError) as exc:
                            hits = {"RC-11"}
                            closure_out.append(("RC-11", f"negativeFixtures[{i}] mutation execution failed ({exc})"))
                        if obj.get("expectedInvariant") not in hits:
                            closure_out.append(("RC-11", f"negativeFixtures[{i}] mutation escaped named invariant"))
                if seen_kinds != required_kinds:
                    closure_out.append(("RC-11", "$contract.capabilityClosure.negativeFixtures: exact 26 typed closure/lifecycle controls required"))

                tags = [f"0x{x:02x}" for x in range(0x70, 0x7A)]
                expected_grammar_controls = ([
                    {"id": f"RT10-GRAMMAR-TAG-{tag[2:].upper()}", "kind": "tag-substitution", "tag": tag, "expectedInvariant": "RC-11"}
                    for tag in tags
                ] + [
                    {"id": f"RT10-GRAMMAR-OMIT-{tag[2:].upper()}", "kind": "tag-omission", "tag": tag, "expectedInvariant": "RC-11"}
                    for tag in tags
                ] + [
                    {"id": "RT10-GRAMMAR-ORDER", "kind": "order-substitution", "tag": None, "expectedInvariant": "RC-11"},
                    {"id": "RT10-GRAMMAR-GOLDEN", "kind": "golden-substitution", "tag": None, "expectedInvariant": "RC-11"},
                ])
                if section.get("grammarNegativeControls") != expected_grammar_controls:
                    closure_out.append(("RC-11", "$contract.capabilityClosure.grammarNegativeControls: exact 10 tag substitutions, 10 omissions, order, and golden controls required"))

                historical_roles = list(getattr(epmod, "HISTORICAL_DEPENDENCIES", {}))
                expected_historical_controls = ([
                    {"id": f"RT10-HIST-OMIT-{role.upper()}", "kind": "historical-ref-omitted", "role": role, "expectedInvariant": "RC-11"}
                    for role in historical_roles
                ] + [
                    {"id": f"RT10-HIST-MISLABEL-{role.upper()}", "kind": "historical-role-mislabeled", "role": role, "expectedInvariant": "RC-11"}
                    for role in historical_roles
                ])
                controls = section.get("historicalNegativeControls")
                if controls != expected_historical_controls:
                    closure_out.append(("RC-11", "$contract.capabilityClosure.historicalNegativeControls: exact omit/mislabel control for all six VERSIONING v4 roles required"))
                elif isinstance(controls, list):
                    for i, control in enumerate(controls):
                        mutated_bundle = copy.deepcopy(proof_bundle)
                        role = control["role"]
                        target = epmod.HISTORICAL_DEPENDENCIES[role]
                        matches = [
                            dependency for record in mutated_bundle["objectStore"]
                            for dependency in record["dependencies"]
                            if dependency.get("role") == role and dependency.get("ref") == target
                        ]
                        if len(matches) != 1:
                            closure_out.append(("RC-11", f"historicalNegativeControls[{i}]: base proof graph has no unique {role} edge"))
                            continue
                        if control["kind"] == "historical-ref-omitted":
                            for record in mutated_bundle["objectStore"]:
                                record["dependencies"] = [
                                    dependency for dependency in record["dependencies"]
                                    if not (dependency.get("role") == role and dependency.get("ref") == target)
                                ]
                        else:
                            matches[0]["role"] = "policy-verifier"
                        hits = {inv for inv, _ in validate_capability_closure(
                            mutated_bundle, proof_authority, base_closure, base_availability)}
                        if control["expectedInvariant"] not in hits:
                            closure_out.append(("RC-11", f"historicalNegativeControls[{i}]: mutation escaped RC-11"))
    findings.extend(f"{inv}: {msg}" for inv, msg in closure_out)

    findings.extend(f"{inv}: {msg}" for inv, msg in _validate_lease_protocol(contract.get("leaseProtocol")))

    lineage_out: list[tuple[str, str]] = []
    lineage = _exact(contract.get("storageAndLineage"), {"source", "projectContract", "objectPath", "physicalClaimBoundary", "fixtures", "negativeFixtures", "residual"}, set(), "$contract.storageAndLineage", lineage_out, "RC-13")
    if lineage is not None:
        expected_storage_source = "storage-namespace.adjudication-admission-storage-lane.v1.json+resolved-inputs.v2.json#projectIdContract+threat-model.v3.json#storageNamespace"
        expected_storage_residual = "RC-R-01 retains physical path-containment, symlink, hardlink, mount, and backend-isolation implementation evidence."
        if lineage.get("projectContract") != "PROJECT-ID-V1" or lineage.get("objectPath") != "projects/<ProjectId>/objects/<recordKind>/sha256/<digestHex>" or lineage.get("physicalClaimBoundary") != "LEXICAL_ONLY; physical isolation remains IMPLEMENTABLE_UNEXECUTED":
            lineage_out.append(("RC-13", "$contract.storageAndLineage: namespace binding/claim boundary drift"))
        if lineage.get("source") != expected_storage_source or lineage.get("residual") != expected_storage_residual:
            lineage_out.append(("RC-13", "$contract.storageAndLineage: source/residual metadata must be exact closed scalars"))
        lineage_out.extend(_cross_contract_project_join(ctx))
        fixtures = _array(lineage.get("fixtures"), "$contract.storageAndLineage.fixtures", lineage_out, "RC-13")
        fixture_list = fixtures or []
        if fixtures is not None:
            seen_ids: set[str] = set()
            for i, fixture in enumerate(fixtures):
                hits = _validate_purge_fixture(fixture, f"$contract.storageAndLineage.fixtures[{i}]")
                lineage_out.extend(hits)
                if isinstance(fixture, dict) and isinstance(fixture.get("id"), str):
                    if fixture["id"] in seen_ids: lineage_out.append(("RC-13", f"purge fixture id {fixture['id']} duplicate"))
                    seen_ids.add(fixture["id"])
        negatives = _array(lineage.get("negativeFixtures"), "$contract.storageAndLineage.negativeFixtures", lineage_out, "RC-13")
        required_kinds = {"cross-project-removal", "equal-digest-cross-project-alias", "malicious-cross-project-lineage", "remove-blocked-shared-object"}
        seen_kinds: set[str] = set()
        if negatives is not None:
            for i, case in enumerate(negatives):
                obj = _exact(case, {"id", "kind", "expectedInvariant"}, set(), f"$contract.storageAndLineage.negativeFixtures[{i}]", lineage_out, "RC-13")
                if obj is None: continue
                kind = obj.get("kind")
                if kind not in required_kinds or kind in seen_kinds: lineage_out.append(("RC-13", f"lineage negative kind {kind!r} duplicate/unknown")); continue
                seen_kinds.add(kind)
                mutated_list = _apply_purge_mutation(fixture_list, kind)
                hits = {inv for index, fixture in enumerate(mutated_list) for inv, _ in _validate_purge_fixture(fixture, f"$mutated[{index}]")}
                if obj.get("expectedInvariant") != "RC-13" or "RC-13" not in hits: lineage_out.append(("RC-13", f"lineage negative {kind} escaped"))
        if seen_kinds != required_kinds: lineage_out.append(("RC-13", "lineage negatives must cover cross-project/equal-digest/malicious/shared blocking"))
    findings.extend(f"{inv}: {msg}" for inv, msg in lineage_out)

    findings.extend(f"{inv}: {msg}" for inv, msg in _validate_d9_section(contract.get("d9Derivation"), ctx.get("d9contract"), ctx.get("d9mod")))
    findings.extend(f"{inv}: {msg}" for inv, msg in _authority_guard(contract, ctx.get("product")))

    invariants = contract.get("invariants")
    expected_ids = {f"RC-{i}" for i in range(1, 16)}
    if not isinstance(invariants, list):
        findings.append("RC-15: invariants must be an array")
    else:
        ids: set[str] = set()
        for i, invariant in enumerate(invariants):
            if not isinstance(invariant, dict) or set(invariant) != {"id", "assert"} or not isinstance(invariant.get("id"), str) or not isinstance(invariant.get("assert"), str):
                findings.append(f"RC-15: invariants[{i}] must be closed id/assert strings")
                continue
            ids.add(invariant["id"])
        if ids != expected_ids or len(ids) != len(invariants):
            findings.append("RC-15: invariant registry must be exactly RC-1..RC-15 without duplicates")

    assurance = contract.get("assurance")
    if not isinstance(assurance, dict) or set(assurance) != set(EXPECTED_ASSURANCE):
        findings.append("assurance: recursively closed assurance record required")
    elif assurance != EXPECTED_ASSURANCE:
        findings.append("assurance: exact SPECIFIED / IMPLEMENTABLE_UNEXECUTED / blocked boundary drifted")
    residuals = contract.get("retainedResiduals")
    if not isinstance(residuals, list) or any(not isinstance(row, dict) or set(row) != {"id", "class", "statement"} for row in residuals):
        findings.append("assurance: retainedResiduals must be recursively closed records")
    elif residuals != EXPECTED_RETAINED_RESIDUALS:
        findings.append("assurance: retainedResiduals must equal the exact closed v8 residual registry")
    else:
        by_id = {row.get("id"): row for row in residuals}
        if by_id.get("A1-RTV4-02", {}).get("class") != "MEASUREMENT": findings.append("assurance: A1-RTV4-02 measurement residual must remain")
        if by_id.get("RC-R-01", {}).get("class") != "STORAGE-ARCHITECTURE": findings.append("assurance: RC-R-01 storage limitation must remain")
        if not any(row.get("class") == "PROCESS" and "independent" in row.get("statement", "").lower() for row in residuals): findings.append("assurance: explicit independent rereview process residual required")
    return findings


def check(value: Any, ctx: dict[str, Any] | None = None) -> list[str]:
    try:
        return _check_impl(value, ctx if ctx is not None else _load_context())
    except Exception as exc:
        return [f"RC-TOTALITY: controlled contract validation failure {type(exc).__name__}: {exc}"]


def _semantic_mutations() -> list[tuple[str, Callable[[dict[str, Any]], bool]]]:
    def closure(kind: str):
        def mutate(contract):
            section = contract["capabilityClosure"]
            _apply_closure_mutation(
                section["semanticClosure"], section["unitAvailabilityRecords"], kind)
            return True
        return mutate
    def lease(kind: str):
        def mutate(contract): _apply_lease_mutation(contract["leaseProtocol"], kind); return True
        return mutate
    def d9(kind: str, row: str):
        def mutate(contract): _apply_d9_mutation(contract["d9Derivation"], kind, row); return True
        return mutate
    def purge(kind: str):
        def mutate(contract): contract["storageAndLineage"]["fixtures"] = _apply_purge_mutation(contract["storageAndLineage"]["fixtures"], kind); return True
        return mutate
    def current_state(contract): contract["integrationState"]["pending"][0]["currentState"] = "RESOLVED"; return True
    def nested_resolves(contract): contract["integrationState"]["resolves"] = {"V10": "RESOLVED", "Phase1A": "COMPLETE"}; return True
    def product_acceptance(contract): contract["custodyPolicy"]["productAcceptance"] = {"status": "ACCEPTED", "decisionId": "CD-RT-5"}; return True
    def hidden_product_decision(contract): contract["repairs"] = [{"productDecision": {"decisionId": "CD-RT-5", "outcome": "APPROVED", "by": "architecture-candidate"}}]; return True
    def top_current(contract): contract["currentState"] = "RESOLVED"; return True
    def assurance(contract): contract["assurance"]["state"] = "QUALIFIED"; return True
    def proof_hash(contract): contract["capabilityClosure"]["source"]["sha256"] = "0" * 64; return True
    def grammar_tag(tag: str, omit: bool):
        def mutate(contract):
            rows = contract["capabilityClosure"]["closureGrammar"]["tagRegistry"]
            index = next(i for i, row in enumerate(rows) if row["tag"] == tag)
            if omit:
                rows.pop(index)
            else:
                rows[index]["tag"] = "0xff"
            return True
        return mutate
    def grammar_order(contract):
        order = contract["capabilityClosure"]["closureGrammar"]["emissionOrder"]
        order[1], order[2] = order[2], order[1]
        return True
    def grammar_golden(contract):
        golden = contract["capabilityClosure"]["closureGoldens"]["unit"]
        golden["encodedHex"] = "00" + golden["encodedHex"]
        return True
    def historical_declaration(contract):
        contract["capabilityClosure"]["historicalNegativeControls"][0]["role"] = "policy-verifier"
        return True
    def semantic_path_key(contract):
        semantic_ref = contract["capabilityClosure"]["semanticClosure"]["semanticRoots"][0]["semanticRef"]
        contract["storageAndLineage"]["objectPath"] = semantic_ref
        return True
    def semantic_purge_key(contract):
        semantic_ref = contract["capabilityClosure"]["semanticClosure"]["semanticRoots"][0]["semanticRef"]
        fixture = next(row for row in contract["leaseProtocol"]["fixtures"]
                       if row["event"]["kind"] == "purge")
        fixture["event"]["targetRefs"][0]["recordCasRef"] = semantic_ref
        return True

    mutations: list[tuple[str, Callable[[dict[str, Any]], bool]]] = [
        ("RT10 empty closure", closure("empty-closure")),
        ("RT10 proofRefs removed", closure("proof-ref-removed")),
        ("RT10 semantic unit ref removed", closure("unit-ref-removed")),
        ("RT10 semantic unit alias", closure("reference-alias")),
        ("RT10 weakened exact minimum", closure("weaken-minimum")),
        ("RT10 strengthened exact minimum", closure("strengthen-minimum")),
        ("RT10 target purge retains authority", closure("target-purge-retains-authority")),
        ("RT10 dependency edge removed", closure("dependency-edge-removed")),
        ("RT10 closure-root RunId", closure("closure-root-run-id")),
        ("RT10 unit RunId", closure("unit-run-id")),
        ("RT10 RunId-derived UNIT-ID", closure("runid-derived-unit-id")),
        ("RT10 semantic objectStates", closure("semantic-object-states")),
        ("RT10 semantic effectiveCapability", closure("semantic-effective-capability")),
        ("RT10 terminal run-seal child", closure("terminal-run-seal-child")),
        ("RT10 old v2 tag", closure("old-v2-tag-substitution")),
        ("RT10 old v2 domain", closure("old-v2-domain-substitution")),
        ("RT10 semantic ref as CAS", closure("semantic-ref-as-cas")),
        ("RT10 binding only AVAILABLE", closure("binding-only-available")),
        ("RT10 missing semantic binding", closure("semantic-binding-missing")),
        ("RT10 duplicate semantic binding", closure("semantic-binding-duplicate")),
        ("RT10 cross-project semantic binding", closure("semantic-binding-cross-project")),
        ("RT10 hidden unreachable binding", closure("hidden-unreachable-binding")),
        ("RT10 authority edge role downgrade", closure("authority-edge-role-downgrade")),
        ("RT10 minimum downgrade", closure("minimum-downgrade")),
        ("RT10 VERSIONING raw retyped semantic", closure("versioning-raw-retyped-semantic")),
        ("RT10 downstream binding field", closure("downstream-field-in-binding")),
        ("R8-P1A-P08 split transaction coordinated", lease("split-transaction-coordinated")),
        ("R8-P1A-P09 boolean lease record", lease("boolean-lease-record")),
        ("R8-P1A-P10 crashed lease held forever coordinated", lease("crash-held-forever-coordinated")),
        ("R8-P1A-P11 expiry preempts live use coordinated", lease("expiry-preempts-live-coordinated")),
        ("R8-P1A-RR-03 stale reclaim accepted", lease("stale-reclaim-accepted")),
        ("R8-P1A-RR-03 wrong reclaim owner accepted", lease("wrong-reclaim-owner-accepted")),
        ("R8-P1A-RR-03 wrong reclaim liveness accepted", lease("wrong-reclaim-liveness-accepted")),
        ("R8-P1A-RR-03 wrong reclaim fence accepted", lease("wrong-reclaim-fence-accepted")),
        ("R8-P1A-RR-03 reclaim drops pending expiry", lease("reclaim-drops-pending-expiry")),
        ("R8-P1A-RR-03 fence reuse accepted", lease("fence-reuse-accepted")),
        ("R8-P1A-RR-03 repin expired object accepted", lease("repin-expired-accepted")),
        ("R8-P1A-P12 cross-project removal", purge("cross-project-removal")),
        ("equal digest cross-project alias", purge("equal-digest-cross-project-alias")),
        ("malicious cross-project lineage", purge("malicious-cross-project-lineage")),
        ("R8-P1A-P13 secondary reason dropped", d9("drop-secondary-reason", "RD-09-MULTI-DEFICIENCY")),
        ("R8-P1A-P14 undeclared D9 axis", d9("undeclared-axis", "RD-09-MULTI-DEFICIENCY")),
        ("R8-P1A-P15 currentState RESOLVED", current_state),
        ("R8-P1A-P16 nested resolves declaration", nested_resolves),
        ("R8-P1A-P17 nested productAcceptance ACCEPTED", product_acceptance),
        ("R8-P1A-RR-04 hidden repairs productDecision APPROVED", hidden_product_decision),
        ("top-level currentState RESOLVED", top_current),
        ("assurance overclaim", assurance),
        ("proof artifact hash is not load-bearing", proof_hash),
        ("historical negative declaration mislabeled", historical_declaration),
        ("RT10 semantic ref as physical path key", semantic_path_key),
        ("RT10 semantic ref as purge key", semantic_purge_key),
    ]
    for tag in (f"0x{x:02x}" for x in range(0x70, 0x7A)):
        mutations.append((f"RT10 grammar {tag} substituted", grammar_tag(tag, False)))
        mutations.append((f"RT10 grammar {tag} omitted", grammar_tag(tag, True)))
    mutations.extend([
        ("RT10 grammar emission order", grammar_order),
        ("RT10 grammar golden", grammar_golden),
    ])
    return mutations


HOSTILE_VALUES = [None, True, 7, "scalar", [None], {}]


def _hostile_cases(contract: dict[str, Any]) -> list[tuple[str, Any]]:
    setters: list[tuple[str, Callable[[dict[str, Any], Any], None]]] = [
        ("root", lambda c, v: None),
        ("capabilityClosure", lambda c, v: c.__setitem__("capabilityClosure", v)),
        ("closureGrammar", lambda c, v: c["capabilityClosure"].__setitem__("closureGrammar", v)),
        ("closureGrammarTag", lambda c, v: c["capabilityClosure"]["closureGrammar"]["tagRegistry"].__setitem__(0, v)),
        ("closureGolden", lambda c, v: c["capabilityClosure"]["closureGoldens"].__setitem__("unit", v)),
        ("semanticClosure", lambda c, v: c["capabilityClosure"].__setitem__("semanticClosure", v)),
        ("proofRefs", lambda c, v: c["capabilityClosure"]["semanticClosure"].__setitem__("proofRefs", v)),
        ("proofRef", lambda c, v: c["capabilityClosure"]["semanticClosure"]["proofRefs"].__setitem__(0, v)),
        ("unit", lambda c, v: c["capabilityClosure"]["semanticClosure"]["units"].__setitem__(0, v)),
        ("objectRef", lambda c, v: c["capabilityClosure"]["semanticClosure"]["units"][0]["objectRefs"].__setitem__(0, v)),
        ("unitAvailabilityRecords", lambda c, v: c["capabilityClosure"].__setitem__("unitAvailabilityRecords", v)),
        ("unitAvailabilityRecord", lambda c, v: c["capabilityClosure"]["unitAvailabilityRecords"].__setitem__(0, v)),
        ("availabilityObjectState", lambda c, v: c["capabilityClosure"]["unitAvailabilityRecords"][0]["objectStates"].__setitem__(0, v)),
        ("leaseProtocol", lambda c, v: c.__setitem__("leaseProtocol", v)),
        ("leaseFixture", lambda c, v: c["leaseProtocol"]["fixtures"].__setitem__(0, v)),
        ("leaseInitial", lambda c, v: c["leaseProtocol"]["fixtures"][0].__setitem__("initial", v)),
        ("leaseEvent", lambda c, v: c["leaseProtocol"]["fixtures"][0].__setitem__("event", v)),
        ("leaseExpected", lambda c, v: c["leaseProtocol"]["fixtures"][0].__setitem__("expected", v)),
        ("leaseScenario", lambda c, v: c["leaseProtocol"]["scenarios"].__setitem__(0, v)),
        ("leaseScenarioEvent", lambda c, v: c["leaseProtocol"]["scenarios"][0]["events"].__setitem__(0, v)),
        ("leaseScenarioOutput", lambda c, v: c["leaseProtocol"]["scenarios"][0]["expectedOutputs"].__setitem__(0, v)),
        ("storageAndLineage", lambda c, v: c.__setitem__("storageAndLineage", v)),
        ("purgeFixture", lambda c, v: c["storageAndLineage"]["fixtures"].__setitem__(0, v)),
        ("purgeRequest", lambda c, v: c["storageAndLineage"]["fixtures"][0].__setitem__("request", v)),
        ("lineageEdge", lambda c, v: c["storageAndLineage"]["fixtures"][0]["lineageEdges"].__setitem__(0, v)),
        ("d9Derivation", lambda c, v: c.__setitem__("d9Derivation", v)),
        ("d9Row", lambda c, v: c["d9Derivation"]["rows"].__setitem__(0, v)),
        ("d9Axes", lambda c, v: c["d9Derivation"]["rows"][0].__setitem__("axes", v)),
        ("d9Output", lambda c, v: c["d9Derivation"]["rows"][0].__setitem__("expectedTermination", v)),
        ("custodyPolicy", lambda c, v: c.__setitem__("custodyPolicy", v)),
        ("authority", lambda c, v: c.__setitem__("authority", v)),
        ("integrationState", lambda c, v: c.__setitem__("integrationState", v)),
        ("assurance", lambda c, v: c.__setitem__("assurance", v)),
    ]
    result: list[tuple[str, Any]] = []
    for name, setter in setters:
        for hostile in HOSTILE_VALUES:
            if name == "root":
                result.append((f"{name}={type(hostile).__name__}", copy.deepcopy(hostile)))
                continue
            mutated = copy.deepcopy(contract)
            try:
                setter(mutated, copy.deepcopy(hostile))
            except (KeyError, IndexError, TypeError):
                continue
            result.append((f"{name}={type(hostile).__name__}", mutated))
    return result


def selftest(contract: Any, ctx: dict[str, Any]) -> int:
    base = check(contract, ctx)
    if base:
        print(f"REFUSING to self-test: base contract has {len(base)} finding(s); mutations would be masked.")
        for finding in base[:16]: print("  -", finding)
        return 1
    assert isinstance(contract, dict)
    failures: list[str] = []
    total = 0
    for name, mutate in _semantic_mutations():
        total += 1
        mutated = copy.deepcopy(contract)
        before = copy.deepcopy(mutated)
        try:
            applied = mutate(mutated)
        except Exception as exc:
            failures.append(f"{name}: mutation raised {type(exc).__name__}: {exc}")
            continue
        if not applied or mutated == before:
            failures.append(f"{name}: mutation did not apply (escape)")
        elif not check(mutated, ctx):
            failures.append(f"{name}: mutation survived")
    for name, hostile in _hostile_cases(contract):
        total += 1
        try:
            result = check(hostile, ctx)
        except Exception as exc:
            failures.append(f"{name}: traceback escape {type(exc).__name__}: {exc}")
            continue
        if not result:
            failures.append(f"{name}: hostile parsed value accepted")
    if failures:
        print(f"{len(failures)}/{total} retention self-test cases escaped")
        for failure in failures: print("  -", failure)
        return 1
    print(f"PASS: {total} retention mutations/hostile parsed-value cases rejected; base-dirty and non-applying-mutation guards active")
    return 0


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    try:
        contract = _load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"cannot load {path}: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    ctx = _load_context()
    if "--selftest" in sys.argv:
        return selftest(contract, ctx)
    findings = check(contract, ctx)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings: print("  -", finding)
        return 1
    assert isinstance(contract, dict)
    closure = contract["capabilityClosure"]["semanticClosure"]
    print(f"PASS: {path.name}; {len(closure['proofRefs'])} transitive proof refs / {len(closure['dependencyEdges'])} dependency edges / {len(closure['units'])} semantic custody units; {len(contract['leaseProtocol']['fixtures'])} lease reducer fixtures + {len(contract['leaseProtocol']['scenarios'])} composed scenarios; {len(contract['storageAndLineage']['fixtures'])} ProjectId purge fixtures; {len(contract['d9Derivation']['rows'])} full D9 rows; RC-1..RC-15 clean")
    print("  typed semantic-to-raw bindings and UNIT-ID-V3 raw-custody closure clean; RunId/effective availability remain outside semantic digest")
    print("  CD-RT-5 BLOCKED_ON_PHASE_1A; V10 UNRESOLVED; candidate NOT-APPLIED; no dependency/register/narrative closure claimed")
    print("  assurance SPECIFIED / IMPLEMENTABLE_UNEXECUTED; independent combined-packet rereview REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
