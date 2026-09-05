#!/usr/bin/env python3
"""Validate the narrow OPERABILITY v6 EventEnvelopeV3 binding successor.

The checker authenticates its complete local OP5/OP2 data and executable-source
closure before compiling either predecessor checker.  It executes checker source
only from the already verified in-memory bytes, constructs the complete expected
v6 object from exact OP5, and proves OP6 -> OP5 -> protected OP2 projections.

Usage: python3 -B check-operability-v6.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
import types
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v6.json"
PINS = {
    "operability.v5.json": "89a18ffde1df3255b6a766aa74d1ad496ee3c7ed09cf5d69aa0ef34451699d8f",
    "check-operability-v5.py": "047afb978bc02b62402e4036bb42659a7ac14d427408ef06d59d8a8d7438ef70",
    "operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
}
EXECUTABLE_DEPENDENCIES = {
    "check-operability-v5.py": "op5_verified_for_op6",
    "check-operability.py": "op2_verified_for_op6",
}
ROOT_ENVELOPE = ("version", "status", "supersedes", "author", "reviewStatus")
LIFECYCLE_DELTA_FIELDS = (
    "schemaVersionConstraint", "phasePlaneBindings", "bindingFixtures")
REQ_RE = re.compile(r"^req1_[0-9a-f]{32}$")

V6_ROOT = {
    "version": 6,
    "status": "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-COMBINED-REVIEW (EventEnvelopeV3 version/phase-plane binding successor over unaccepted v5)",
    "supersedes": {
        "artifact": "operability.v5.json",
        "sha256": PINS["operability.v5.json"],
        "checker": "check-operability-v5.py",
        "checkerSha256": PINS["check-operability-v5.py"],
    },
    "author": "agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane; EventEnvelopeV3 binding successor by operability-v6 lane",
    "reviewStatus": "OPERABILITY v6 is a NOT-APPLIED exact successor over v5. OPERABILITY v5 was not independently accepted. The required independent combined review MUST cover the inherited v5 lifecycle/store-provenance overlay and the v6 EventEnvelopeV3 schema-version/phase-plane binding delta. Green checkers are design-integrity evidence only; no product, integration, application, seal, or release authority is claimed.",
}
SCHEMA_VERSION_CONSTRAINT = {
    "field": "schemaVersion",
    "operator": "==",
    "value": 3,
    "scope": "every public EventEnvelopeV3 in every closed phase",
    "presenceRule": "Listing schemaVersion as required is insufficient; its JSON value MUST be the integer 3.",
    "runCommittedRule": "Every run-committed public envelope MUST use schemaVersion 3 and plane progress.",
}
PHASE_PLANE_BINDINGS = {
    "request-validation": None,
    "attempt-admitted": None,
    "run-committed": "progress",
    "stored-run-read": None,
}
RUN_ID = "run1:3f319950f6a00565611029f3accc38a2afd38b3f4ab6539b2d6c8304ef0a9208"


class DuplicateKeyError(ValueError):
    """Raised when JSON contains a duplicate object member."""


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_loads(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_closed_object)


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _compile_verified(raw: bytes, filename: str, module_name: str) -> Any:
    """Compile only an already authenticated source buffer."""
    module = types.ModuleType(module_name)
    module.__file__ = str(HERE / filename)
    module.__package__ = None
    code = compile(raw, module.__file__, "exec", dont_inherit=True)
    exec(code, module.__dict__)
    return module


def authenticated_context() -> tuple[dict[str, Any] | None, list[str]]:
    """Read and authenticate the complete closure before any source execution."""
    errors: list[str] = []
    buffers: dict[str, bytes] = {}
    for name, expected in PINS.items():
        try:
            raw = (HERE / name).read_bytes()
        except OSError as exc:
            errors.append(f"OP6-DEP: cannot read {name}: {type(exc).__name__}: {exc}")
            continue
        buffers[name] = raw
        actual = _digest(raw)
        if actual != expected:
            errors.append(f"OP6-DEP: {name} hash {actual} != {expected}")
    if errors or set(buffers) != set(PINS):
        return None, errors or ["OP6-DEP: dependency closure is incomplete"]

    # Parsing data is non-executable; source compilation occurs only after all
    # four local dependency bytes have authenticated above.
    try:
        op5 = strict_loads(buffers["operability.v5.json"])
        op2 = strict_loads(buffers["operability.v2.json"])
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        return None, [f"OP6-DEP: authenticated data parse failed: {type(exc).__name__}: {exc}"]
    modules: dict[str, Any] = {}
    try:
        for filename, module_name in EXECUTABLE_DEPENDENCIES.items():
            modules[filename] = _compile_verified(
                buffers[filename], filename, module_name)
    except Exception as exc:
        return None, [f"OP6-DEP: verified source compile failed: {type(exc).__name__}: {exc}"]

    op5mod = modules["check-operability-v5.py"]
    op2mod = modules["check-operability.py"]
    if getattr(op5mod, "BINDING", None) != "operability.v5.json" or \
            not callable(getattr(op5mod, "project_op2", None)) or \
            not callable(getattr(op5mod, "check", None)):
        errors.append("OP6-DEP: verified OP5 checker surface is incomplete")
    if getattr(op2mod, "BINDING", None) != "operability.v2.json" or \
            not callable(getattr(op2mod, "check", None)):
        errors.append("OP6-DEP: verified OP2 checker surface is incomplete")
    op5_pins = getattr(op5mod, "PINS", {})
    if not isinstance(op5_pins, dict) or \
            op5_pins.get("operability.v2.json") != PINS["operability.v2.json"] or \
            op5_pins.get("check-operability.py") != PINS["check-operability.py"]:
        errors.append("OP6-DEP: OP5 checker does not bind the protected OP2 bytes")
    try:
        if op5mod.project_op2(op5) != op2:
            errors.append("OP6-DEP: exact OP5 bytes do not project to protected OP2")
    except Exception as exc:
        errors.append(f"OP6-DEP: OP5-to-OP2 projection failed: {type(exc).__name__}: {exc}")
    if errors:
        return None, errors
    return {
        "buffers": buffers,
        "op5": op5,
        "op2": op2,
        "op5mod": op5mod,
        "op2mod": op2mod,
    }, []


def expected_dependency_closure() -> dict[str, dict[str, str]]:
    return {
        "operability.v5.json": {
            "kind": "data", "sha256": PINS["operability.v5.json"]},
        "check-operability-v5.py": {
            "kind": "executable-source", "sha256": PINS["check-operability-v5.py"]},
        "operability.v2.json": {
            "kind": "protected-data", "sha256": PINS["operability.v2.json"]},
        "check-operability.py": {
            "kind": "protected-executable-source", "sha256": PINS["check-operability.py"]},
    }


def expected_binding_fixtures() -> list[dict[str, Any]]:
    common = {
        "schemaVersion": 3,
        "plane": "progress",
        "phase": "run-committed",
        "budgetOwner": "ExecutionId",
        "payloadType": "RunCommittedV1",
        "payloadBytes": 128,
        "runId": RUN_ID,
    }

    def envelope_fixture(fixture_id: str, suffix: str, *, valid: bool,
                         expected: list[str], **changes: Any) -> dict[str, Any]:
        envelope = copy.deepcopy(common)
        envelope["requestId"] = f"req1_{suffix}"
        envelope["executionId"] = f"exec:{fixture_id.removeprefix('op6-')}"
        for key, value in changes.items():
            if value is _MISSING:
                envelope.pop(key, None)
            else:
                envelope[key] = value
        # Preserve the exact human-readable execution identifiers in the JSON.
        exact_exec = {
            "op6-valid-run-committed-v3-progress": "exec:op6-run-committed",
            "op6-reject-missing-schema-version": "exec:op6-missing-version",
            "op6-reject-wrong-schema-version": "exec:op6-wrong-version",
            "op6-reject-missing-plane": "exec:op6-missing-plane",
            "op6-reject-wrong-run-committed-plane": "exec:op6-wrong-plane",
            "op6-reject-evidence-plane": "exec:op6-evidence-plane",
            "op6-reject-legacy-attempt-sealed": "exec:op6-legacy-phase",
        }
        envelope["executionId"] = exact_exec[fixture_id]
        return {
            "id": fixture_id,
            "kind": "event-envelope",
            "valid": valid,
            "expectedErrors": expected,
            "envelope": envelope,
        }

    return [
        envelope_fixture("op6-valid-run-committed-v3-progress", "0" * 30 + "61",
                         valid=True, expected=[]),
        envelope_fixture("op6-reject-missing-schema-version", "0" * 30 + "62",
                         valid=False, expected=["SCHEMA_VERSION_MISSING"],
                         schemaVersion=_MISSING),
        envelope_fixture("op6-reject-wrong-schema-version", "0" * 30 + "63",
                         valid=False, expected=["SCHEMA_VERSION_NOT_3"],
                         schemaVersion=2),
        envelope_fixture("op6-reject-missing-plane", "0" * 30 + "64",
                         valid=False, expected=["PLANE_MISSING"], plane=_MISSING),
        envelope_fixture("op6-reject-wrong-run-committed-plane", "0" * 30 + "65",
                         valid=False, expected=["RUN_COMMITTED_PLANE_NOT_PROGRESS"],
                         plane="diagnostics"),
        envelope_fixture("op6-reject-evidence-plane", "0" * 30 + "66",
                         valid=False, expected=["PLANE_NOT_CLOSED"], plane="evidence"),
        envelope_fixture("op6-reject-legacy-attempt-sealed", "0" * 30 + "67",
                         valid=False, expected=["PHASE_NOT_CLOSED"],
                         phase="attempt-sealed"),
        {
            "id": "op6-reject-unknown-phase-plane-binding-key",
            "kind": "phase-plane-bindings",
            "valid": False,
            "expectedErrors": ["PHASE_PLANE_BINDING_KEYS_NOT_CLOSED"],
            "bindings": {
                **PHASE_PLANE_BINDINGS,
                "attempt-sealed": None,
            },
        },
    ]


_MISSING = object()


def expected_v6_metadata(op5: dict[str, Any]) -> dict[str, Any]:
    changed = {
        key: {"before": copy.deepcopy(op5[key]),
              "after": copy.deepcopy(V6_ROOT[key])}
        for key in ROOT_ENVELOPE
    }
    return {
        "id": "OPERABILITY-V6-EVENT-ENVELOPE-V3-BINDING-SUCCESSOR",
        "applicationState": "NOT-APPLIED",
        "authorityClaim": "NONE",
        "predecessorIndependentAcceptance": "NOT-GRANTED",
        "requiredIndependentCombinedReview": {
            "state": "REQUIRED",
            "scope": [
                "the inherited OPERABILITY v5 lifecycle and store-provenance overlay",
                "the v6 schemaVersion == 3 constraint, closed phasePlaneBindings map, normative run-committed binding, and derived fixtures",
            ],
            "rule": "The v5 authored checker and this v6 checker are design-integrity evidence only. Review may not accept the v6 delta while assuming the inherited, not-independently-accepted v5 lifecycle overlay.",
        },
        "localDependencyClosure": expected_dependency_closure(),
        "v6ToV5Projection": {
            "id": "OP6-TO-OP5-EXACT-PROJECTION",
            "predecessor": copy.deepcopy(V6_ROOT["supersedes"]),
            "algorithm": "Delete aPrimeSuccessor.operabilityV6Successor; delete aPrimeSuccessor.lifecycle.schemaVersionConstraint, phasePlaneBindings, and bindingFixtures; restore the five root successor envelope fields from changedRootFields.before; canonical deep-compare the complete result to exact operability.v5.json bytes.",
            "changedRootFields": changed,
            "removedSuccessorMetadata": ["aPrimeSuccessor.operabilityV6Successor"],
            "removedLifecycleFields": list(LIFECYCLE_DELTA_FIELDS),
            "deepEqualityRule": "The projection may remove only the enumerated v6 successor metadata and three lifecycle fields and may restore only the five enumerated root successor envelope fields. Every remaining v5 key, list item, scalar, lifecycle/store-provenance semantic, and OP5-to-OP2 projection byte is exact deep-equal.",
            "inheritedProjectionRule": "After exact OP6-to-OP5 projection, the unchanged OP5-TO-OP2-EXACT-PROJECTION must produce the protected operability.v2.json object.",
        },
    }


def construct_expected_v6(op5: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(op5)
    for key, value in V6_ROOT.items():
        result[key] = copy.deepcopy(value)
    successor = result["aPrimeSuccessor"]
    successor["operabilityV6Successor"] = expected_v6_metadata(op5)
    lifecycle = successor["lifecycle"]
    lifecycle["schemaVersionConstraint"] = copy.deepcopy(SCHEMA_VERSION_CONSTRAINT)
    lifecycle["phasePlaneBindings"] = copy.deepcopy(PHASE_PLANE_BINDINGS)
    lifecycle["bindingFixtures"] = expected_binding_fixtures()
    return result


def project_v5(candidate: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(candidate)
    successor = result["aPrimeSuccessor"]
    metadata = successor["operabilityV6Successor"]
    projection = metadata["v6ToV5Projection"]
    if set(projection["changedRootFields"]) != set(ROOT_ENVELOPE):
        raise ValueError("v6-to-v5 root envelope is not closed")
    if projection["removedSuccessorMetadata"] != [
            "aPrimeSuccessor.operabilityV6Successor"]:
        raise ValueError("v6-to-v5 successor metadata removal is not exact")
    if projection["removedLifecycleFields"] != list(LIFECYCLE_DELTA_FIELDS):
        raise ValueError("v6-to-v5 lifecycle removal is not exact")
    lifecycle = successor["lifecycle"]
    for key in LIFECYCLE_DELTA_FIELDS:
        lifecycle.pop(key)
    successor.pop("operabilityV6Successor")
    for key in ROOT_ENVELOPE:
        result[key] = copy.deepcopy(projection["changedRootFields"][key]["before"])
    return result


def _unique_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(row, str) for row in value) \
        and len(value) == len(set(value))


def _binding_map_errors(bindings: Any, closed_phases: Any) -> list[str]:
    if not isinstance(bindings, dict) or not _unique_strings(closed_phases):
        return ["PHASE_PLANE_BINDING_KEYS_NOT_CLOSED"]
    if set(bindings) != set(closed_phases) or len(bindings) != len(closed_phases):
        return ["PHASE_PLANE_BINDING_KEYS_NOT_CLOSED"]
    errors: list[str] = []
    if bindings.get("run-committed") != "progress":
        errors.append("RUN_COMMITTED_PLANE_BINDING_NOT_PROGRESS")
    for phase in closed_phases:
        if phase != "run-committed" and bindings.get(phase) is not None:
            errors.append(f"PHASE_PLANE_BINDING_NOT_UNBOUND:{phase}")
    return errors


def _event_errors(envelope: Any, schema: Any, bindings: Any) -> list[str]:
    if not isinstance(envelope, dict) or not isinstance(schema, dict) or \
            not isinstance(bindings, dict):
        return ["ENVELOPE_OR_SCHEMA_NOT_OBJECT"]
    errors: list[str] = []
    required = schema.get("required")
    optional = schema.get("optional")
    closed_planes = schema.get("closedPlanes")
    closed_phases = schema.get("closedPhases")
    phase_requirements = schema.get("phaseRequirements")
    if not all(_unique_strings(rows) for rows in (
            required, optional, closed_planes, closed_phases)) or \
            not isinstance(phase_requirements, dict):
        return ["INHERITED_EVENT_SCHEMA_MALFORMED"]
    allowed = set(required) | set(optional)
    if not set(envelope).issubset(allowed):
        errors.append("ENVELOPE_UNKNOWN_FIELDS")
    for field in required:
        if field not in {"schemaVersion", "plane"} and field not in envelope:
            errors.append(f"REQUIRED_FIELD_MISSING:{field}")

    if "schemaVersion" not in envelope:
        errors.append("SCHEMA_VERSION_MISSING")
    elif type(envelope.get("schemaVersion")) is not int or \
            envelope.get("schemaVersion") != 3:
        errors.append("SCHEMA_VERSION_NOT_3")

    plane = envelope.get("plane")
    plane_is_closed = False
    if "plane" not in envelope:
        errors.append("PLANE_MISSING")
    elif not isinstance(plane, str) or plane not in closed_planes:
        errors.append("PLANE_NOT_CLOSED")
    else:
        plane_is_closed = True

    phase = envelope.get("phase")
    phase_is_closed = isinstance(phase, str) and phase in closed_phases
    if not phase_is_closed:
        errors.append("PHASE_NOT_CLOSED")
    request_id = envelope.get("requestId")
    if not isinstance(request_id, str) or REQ_RE.fullmatch(request_id) is None:
        errors.append("REQUEST_ID_NOT_CANONICAL")

    if phase_is_closed:
        requirement = phase_requirements.get(phase)
        if not isinstance(requirement, dict):
            errors.append("PHASE_REQUIREMENT_MISSING")
        else:
            for field in ("executionId", "runId"):
                present = isinstance(envelope.get(field), str) and bool(envelope.get(field))
                mode = requirement.get(field)
                if isinstance(mode, str) and mode.startswith("required") and not present:
                    errors.append(f"PHASE_FIELD_REQUIRED:{field}")
                if mode == "forbidden" and present:
                    errors.append(f"PHASE_FIELD_FORBIDDEN:{field}")
            if envelope.get("budgetOwner") != requirement.get("budgetOwner"):
                errors.append("BUDGET_OWNER_MISMATCH")
        if plane_is_closed:
            bound_plane = bindings.get(phase)
            if bound_plane is not None and plane != bound_plane:
                errors.append("RUN_COMMITTED_PLANE_NOT_PROGRESS")
    return errors


def _fixture_errors(row: Any, schema: Any, closed_phases: Any,
                    bindings: Any) -> list[str]:
    if not isinstance(row, dict):
        return ["FIXTURE_NOT_OBJECT"]
    kind = row.get("kind")
    if kind == "event-envelope":
        return _event_errors(row.get("envelope"), schema, bindings)
    if kind == "phase-plane-bindings":
        return _binding_map_errors(row.get("bindings"), closed_phases)
    return ["FIXTURE_KIND_UNKNOWN"]


def _gate(root: Any, gate_id: str) -> dict[str, Any] | None:
    if not isinstance(root, dict) or not isinstance(root.get("validationGates"), list):
        return None
    rows = [row for row in root["validationGates"]
            if isinstance(row, dict) and row.get("id") == gate_id]
    return rows[0] if len(rows) == 1 else None


def check(value: Any, *, verify_files: bool = True,
          context: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["OP6-TOTALITY: root is not an object"]
    if context is None:
        if not verify_files:
            return ["OP6-DEP: unauthenticated context is forbidden"]
        context, dependency_errors = authenticated_context()
        if dependency_errors or context is None:
            return dependency_errors or ["OP6-DEP: no authenticated context"]
    op5 = context.get("op5")
    op2 = context.get("op2")
    op5mod = context.get("op5mod")
    if not isinstance(op5, dict) or not isinstance(op2, dict) or op5mod is None:
        return ["OP6-DEP: malformed authenticated context"]

    expected = construct_expected_v6(op5)
    if value != expected:
        errors.append("OP6-FULL: candidate differs from the complete expected v6 construction")
    if value.get("artifact") != "opensip.operability" or value.get("version") != 6:
        errors.append("OP6-ID: artifact/version mismatch")
    if any(value.get(key) != V6_ROOT[key] for key in ROOT_ENVELOPE):
        errors.append("OP6-META: closed root successor metadata drift")

    successor = value.get("aPrimeSuccessor")
    if not isinstance(successor, dict):
        return errors + ["OP6-TOTALITY: aPrimeSuccessor is not an object"]
    metadata = successor.get("operabilityV6Successor")
    lifecycle = successor.get("lifecycle")
    if not isinstance(metadata, dict) or not isinstance(lifecycle, dict):
        return errors + ["OP6-TOTALITY: v6 metadata/lifecycle is not an object"]
    if metadata != expected_v6_metadata(op5):
        errors.append("OP6-META: successor metadata/dependency/projection closure drift")
    if metadata.get("localDependencyClosure") != expected_dependency_closure():
        errors.append("OP6-DEP: declared local dependency closure is not exact four-file OP5/OP2 closure")
    review = metadata.get("requiredIndependentCombinedReview")
    if not isinstance(review, dict) or review.get("state") != "REQUIRED" or \
            metadata.get("predecessorIndependentAcceptance") != "NOT-GRANTED" or \
            not all(token in " ".join(review.get("scope") or []) for token in (
                "inherited OPERABILITY v5 lifecycle", "schemaVersion == 3",
                "phasePlaneBindings")):
        errors.append("OP6-REVIEW: v5 non-acceptance/combined-review scope drift")

    try:
        projected_v5 = project_v5(value)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        errors.append(f"OP6-PROJ: controlled v6-to-v5 projection failure: {type(exc).__name__}: {exc}")
        projected_v5 = None
    if projected_v5 is not None and projected_v5 != op5:
        errors.append("OP6-PROJ: v6 does not project exact-deep-equal to OP5")
    if projected_v5 is not None:
        try:
            if op5mod.project_op2(projected_v5) != op2:
                errors.append("OP6-PROJ: projected OP5 does not project exact-deep-equal to protected OP2")
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            errors.append(f"OP6-PROJ: controlled OP5-to-OP2 projection failure: {type(exc).__name__}: {exc}")
    if successor.get("compatibilityProjection") != \
            op5.get("aPrimeSuccessor", {}).get("compatibilityProjection"):
        errors.append("OP6-PROJ: inherited OP5-to-OP2 projection changed")
    if _gate(value, "G19") != _gate(op5, "G19") or \
            (_gate(value, "G19") or {}).get("status") != "BLOCKED-NO-MECHANISM":
        errors.append("OP6-G19: inherited live gate changed or was promoted")

    schema = lifecycle.get("eventSchemaV3")
    constraint = lifecycle.get("schemaVersionConstraint")
    bindings = lifecycle.get("phasePlaneBindings")
    fixtures = lifecycle.get("bindingFixtures")
    if constraint != SCHEMA_VERSION_CONSTRAINT:
        errors.append("OP6-VERSION: schemaVersion == 3 binding drift")
    if not isinstance(schema, dict):
        return errors + ["OP6-TOTALITY: eventSchemaV3 is not an object"]
    for key in ("required", "optional", "closedPlanes", "closedPhases"):
        if not _unique_strings(schema.get(key)):
            errors.append(f"OP6-CLOSED: {key} is malformed or duplicated")
    closed_phases = schema.get("closedPhases")
    if bindings != PHASE_PLANE_BINDINGS:
        errors.append("OP6-PLANE: full expected phasePlaneBindings map drift")
    for finding in _binding_map_errors(bindings, closed_phases):
        errors.append(f"OP6-PLANE: {finding}")

    expected_fixtures = expected_binding_fixtures()
    if fixtures != expected_fixtures:
        errors.append("OP6-FIXTURE: full expected binding-fixture construction drift")
    if not isinstance(fixtures, list):
        return errors + ["OP6-TOTALITY: bindingFixtures is not a list"]
    ids = [row.get("id") if isinstance(row, dict) else None for row in fixtures]
    if len(fixtures) != 8 or len(ids) != len(set(ids)) or any(
            not isinstance(fixture_id, str) for fixture_id in ids):
        errors.append("OP6-FIXTURE: fixture denominator/identity is malformed or duplicated")
    positive_count = 0
    negative_count = 0
    for row in fixtures:
        derived = _fixture_errors(row, schema, closed_phases, bindings)
        authored_valid = row.get("valid") if isinstance(row, dict) else None
        expected_errors = row.get("expectedErrors") if isinstance(row, dict) else None
        derived_valid = not derived
        if authored_valid is not derived_valid:
            errors.append(f"OP6-FIXTURE: authored valid boolean disagrees with derivation: {row.get('id') if isinstance(row, dict) else None}")
        if expected_errors != derived:
            errors.append(f"OP6-FIXTURE: expected errors disagree with derivation: {row.get('id') if isinstance(row, dict) else None}")
        positive_count += int(derived_valid)
        negative_count += int(not derived_valid)
    if (positive_count, negative_count) != (1, 7):
        errors.append(f"OP6-FIXTURE: derived positive/negative count {(positive_count, negative_count)} != (1, 7)")
    return errors


def selftest(value: dict[str, Any], context: dict[str, Any]) -> tuple[list[str], int, int]:
    failures: list[str] = []
    cases: list[tuple[str, Any]] = []

    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(value)
        before = copy.deepcopy(candidate)
        try:
            mutate(candidate)
        except Exception as exc:
            failures.append(f"{label}: mutation setup raised {type(exc).__name__}: {exc}")
            return
        if candidate == before:
            failures.append(f"{label}: no-op mutation escaped")
            return
        cases.append((label, candidate))

    life = lambda c: c["aPrimeSuccessor"]["lifecycle"]
    meta = lambda c: c["aPrimeSuccessor"]["operabilityV6Successor"]
    valid = lambda c: life(c)["bindingFixtures"][0]["envelope"]
    add("remove schema-version binding", lambda c: life(c).pop("schemaVersionConstraint"))
    add("change schema-version binding", lambda c: life(c)["schemaVersionConstraint"].__setitem__("value", 4))
    add("remove phase-plane binding", lambda c: life(c)["phasePlaneBindings"].pop("request-validation"))
    add("change run-committed plane binding", lambda c: life(c)["phasePlaneBindings"].__setitem__("run-committed", "diagnostics"))
    add("bind otherwise-unbound phase", lambda c: life(c)["phasePlaneBindings"].__setitem__("attempt-admitted", "progress"))
    add("valid fixture missing schemaVersion", lambda c: valid(c).pop("schemaVersion"))
    add("valid fixture wrong schemaVersion", lambda c: valid(c).__setitem__("schemaVersion", 2))
    add("valid fixture boolean schemaVersion", lambda c: valid(c).__setitem__("schemaVersion", True))
    add("valid fixture missing plane", lambda c: valid(c).pop("plane"))
    add("valid fixture wrong closed plane", lambda c: valid(c).__setitem__("plane", "diagnostics"))
    add("valid fixture evidence plane", lambda c: valid(c).__setitem__("plane", "evidence"))
    add("valid fixture legacy attempt-sealed", lambda c: valid(c).__setitem__("phase", "attempt-sealed"))
    add("unknown phase-plane binding key", lambda c: life(c)["phasePlaneBindings"].__setitem__("attempt-sealed", None))
    add("weaken projection removals", lambda c: meta(c)["v6ToV5Projection"]["removedLifecycleFields"].pop())
    add("weaken projection deep equality", lambda c: meta(c)["v6ToV5Projection"].__setitem__("deepEqualityRule", "field presence only"))
    add("status promotion", lambda c: c.__setitem__("status", "APPLIED/INDEPENDENTLY-ACCEPTED"))
    add("incomplete dependency closure", lambda c: meta(c)["localDependencyClosure"].pop("check-operability.py"))
    add("authored valid-boolean shortcut", lambda c: life(c)["bindingFixtures"][0].__setitem__("valid", False))
    add("authored expected-errors shortcut", lambda c: life(c)["bindingFixtures"][1].__setitem__("expectedErrors", []))
    add("duplicate fixture id", lambda c: life(c)["bindingFixtures"][1].__setitem__("id", life(c)["bindingFixtures"][0]["id"]))
    add("duplicate closed phase", lambda c: life(c)["eventSchemaV3"]["closedPhases"].append("run-committed"))
    add("malformed lifecycle", lambda c: c["aPrimeSuccessor"].__setitem__("lifecycle", "not-an-object"))
    add("unknown event field", lambda c: valid(c).__setitem__("eventId", "evt:forbidden"))
    add("payload media-type field", lambda c: valid(c).__setitem__("payloadMediaType", "application/json"))
    add("forbidden extra dependency pin", lambda c: meta(c)["localDependencyClosure"].__setitem__("d9.json", {"kind": "data", "sha256": "0" * 64}))

    for label, candidate in cases:
        try:
            findings = check(candidate, verify_files=False, context=context)
        except Exception as exc:
            failures.append(f"{label}: uncontrolled {type(exc).__name__}: {exc}")
            continue
        if not findings:
            failures.append(f"{label}: escaped")

    totality_cases: list[tuple[str, Any]] = [
        ("string root", "hostile-root"),
        ("null root", None),
        ("list root", []),
        ("empty object", {}),
        ("malformed successor", {"artifact": "opensip.operability", "aPrimeSuccessor": []}),
    ]
    for label, candidate in totality_cases:
        try:
            findings = check(candidate, verify_files=False, context=context)
        except Exception as exc:
            failures.append(f"{label}: uncontrolled {type(exc).__name__}: {exc}")
            continue
        if not findings:
            failures.append(f"{label}: malformed input escaped")

    try:
        strict_loads(b'{"root": {"duplicate": 1, "duplicate": 2}}')
    except DuplicateKeyError:
        pass
    except Exception as exc:
        failures.append(f"duplicate-key parser: uncontrolled {type(exc).__name__}: {exc}")
    else:
        failures.append("duplicate-key parser: duplicate member escaped")
    return failures, len(cases), len(totality_cases) + 1


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        raw = path.read_bytes()
        value = strict_loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    context, dependency_errors = authenticated_context()
    if dependency_errors or context is None:
        if "--selftest" in argv[1:]:
            print("REFUSING selftest: OPERABILITY v6 base/dependency closure is dirty")
        for error in dependency_errors or ["OP6-DEP: no authenticated context"]:
            print(f"FAIL: {error}")
        return 1
    errors = check(value, verify_files=False, context=context)
    if errors:
        if "--selftest" in argv[1:]:
            print("REFUSING selftest: OPERABILITY v6 base/dependency closure is dirty")
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    artifact_hash = _digest(raw)
    if "--selftest" in argv[1:]:
        failures, mutation_count, totality_count = selftest(value, context)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(
            f"PASS: operability.v6.json@sha256:{artifact_hash}; "
            f"{mutation_count} successor mutations rejected; "
            f"{totality_count} malformed/duplicate controls rejected; "
            "8 binding fixtures derived (1 positive, 7 negative)"
        )
    else:
        print(
            f"PASS: operability.v6.json@sha256:{artifact_hash}; "
            "exact OP6->OP5->OP2 projection; 4/4 local dependencies authenticated "
            "before verified-buffer compilation; 8 binding fixtures derived "
            "(1 positive, 7 negative)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
