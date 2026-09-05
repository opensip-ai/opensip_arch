#!/usr/bin/env python3
"""Validate OPERABILITY v7, a totality-only successor over rejected v6.

All local data and executable-source dependencies authenticate before source
compilation.  Malformed candidate values are bounded and shape-checked before
any predecessor join, set construction, hash lookup, or list index.  The exact
clean candidate then proves OP7 -> OP6 -> OP5 -> protected OP2 and reuses the
authenticated v6 checker only after the candidate has projected byte-semantically
to the exact known v6 object.

Usage: python3 -B check-operability-v7.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import pathlib
import sys
import types
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v7.json"
PINS = {
    "operability.v6.json": "12d9f072c25a3efb789a05a1c513dfbc2aaf6612a234b23a8cf82ae027d9acb3",
    "check-operability-v6.py": "2bd5e41d128388f50bb3d1518eb8e460d6987518dd71dcc350a7bc202b7407bd",
    "operability.v6.review-independent-prefreeze.json": "c34d304245a0dc932aae24d8b4283da6e7691bff45b4eb5e3b8ede9ab2c24ad7",
    "operability.v5.json": "89a18ffde1df3255b6a766aa74d1ad496ee3c7ed09cf5d69aa0ef34451699d8f",
    "check-operability-v5.py": "047afb978bc02b62402e4036bb42659a7ac14d427408ef06d59d8a8d7438ef70",
    "operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
}
EXECUTABLE_DEPENDENCIES = {
    "check-operability-v6.py": "op6_rejected_verified_for_op7",
    "check-operability-v5.py": "op5_verified_for_op7",
    "check-operability.py": "op2_verified_for_op7",
}
ROOT_ENVELOPE = ("version", "status", "supersedes", "author", "reviewStatus")
REVIEW_FINDING = "OP6-IR-01-MALFORMED-TOTALITY"

MAX_RAW_BYTES = 2_000_000
MAX_DEPTH = 64
MAX_NODES = 100_000
MAX_ARRAY_ITEMS = 10_000
MAX_OBJECT_MEMBERS = 10_000
MAX_STRING_UTF8_BYTES = 1_048_576

V7_ROOT = {
    "version": 7,
    "status": "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REREVIEW (totality-only successor over rejected v6; EventEnvelopeV3 semantics unchanged)",
    "supersedes": {
        "artifact": "operability.v6.json",
        "sha256": PINS["operability.v6.json"],
        "checker": "check-operability-v6.py",
        "checkerSha256": PINS["check-operability-v6.py"],
    },
    "author": "agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane; EventEnvelopeV3 binding successor by operability-v6 lane; totality-only successor by operability-v7 lane",
    "reviewStatus": "OPERABILITY v6 exact bytes were independently REJECTED for OP6-IR-01-MALFORMED-TOTALITY. OPERABILITY v7 preserves the complete v6 EventEnvelopeV3 semantic object and all inherited lifecycle/store-provenance content exactly, and adds only closed totality shape declarations, rejection binding, successor metadata, and checker tests. v7 is NOT-APPLIED and awaits independent rereview; no product, integration, application, seal, or release authority is claimed.",
}


class DuplicateKeyError(ValueError):
    """A JSON object repeated one member name."""


class InputLimitError(ValueError):
    """Raw or parsed JSON exceeded a declared v7 resource bound."""


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _short_path(parent: str, child: str | int) -> str:
    if isinstance(child, int):
        return f"{parent}[{child}]"
    safe = child if len(child) <= 48 else child[:45] + "..."
    return f"{parent}.{safe}"


def json_value_findings(value: Any) -> list[str]:
    """Iteratively prove a bounded, finite JSON tree before recursive work."""
    findings: list[str] = []
    stack: list[tuple[Any, int, str]] = [(value, 0, "$")]
    seen_containers: set[int] = set()
    nodes = 0
    while stack:
        current, depth, path = stack.pop()
        nodes += 1
        if nodes > MAX_NODES:
            return [f"OP7-LIMIT: node count exceeds {MAX_NODES}"]
        if depth > MAX_DEPTH:
            findings.append(f"OP7-LIMIT: depth exceeds {MAX_DEPTH} at {path}")
            continue
        if isinstance(current, dict):
            identity = id(current)
            if identity in seen_containers:
                findings.append(f"OP7-TOTALITY: non-tree/cyclic object at {path}")
                continue
            seen_containers.add(identity)
            if len(current) > MAX_OBJECT_MEMBERS:
                findings.append(
                    f"OP7-LIMIT: object member count exceeds {MAX_OBJECT_MEMBERS} at {path}")
                continue
            for key, child in current.items():
                if not isinstance(key, str):
                    findings.append(f"OP7-TOTALITY: non-string object key at {path}")
                    child_path = f"{path}.<non-string-key>"
                else:
                    if len(key) > MAX_STRING_UTF8_BYTES or \
                            len(key.encode("utf-8")) > MAX_STRING_UTF8_BYTES:
                        findings.append(f"OP7-LIMIT: object key too large at {path}")
                    child_path = _short_path(path, key)
                stack.append((child, depth + 1, child_path))
        elif isinstance(current, list):
            identity = id(current)
            if identity in seen_containers:
                findings.append(f"OP7-TOTALITY: non-tree/cyclic array at {path}")
                continue
            seen_containers.add(identity)
            if len(current) > MAX_ARRAY_ITEMS:
                findings.append(
                    f"OP7-LIMIT: array item count exceeds {MAX_ARRAY_ITEMS} at {path}")
                continue
            for index, child in enumerate(current):
                stack.append((child, depth + 1, _short_path(path, index)))
        elif isinstance(current, str):
            if len(current) > MAX_STRING_UTF8_BYTES or \
                    len(current.encode("utf-8")) > MAX_STRING_UTF8_BYTES:
                findings.append(f"OP7-LIMIT: string too large at {path}")
        elif current is None or isinstance(current, (bool, int)):
            pass
        elif isinstance(current, float):
            if not math.isfinite(current):
                findings.append(f"OP7-TOTALITY: non-finite JSON number at {path}")
        else:
            findings.append(
                f"OP7-TOTALITY: non-JSON {type(current).__name__} at {path}")
    return findings


def strict_loads(raw: bytes) -> Any:
    if len(raw) > MAX_RAW_BYTES:
        raise InputLimitError(f"raw JSON exceeds {MAX_RAW_BYTES} bytes")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_closed_object)
    limits = json_value_findings(value)
    if limits:
        raise InputLimitError(limits[0])
    return value


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _compile_verified(raw: bytes, filename: str, module_name: str) -> Any:
    module = types.ModuleType(module_name)
    module.__file__ = str(HERE / filename)
    module.__package__ = None
    code = compile(raw, module.__file__, "exec", dont_inherit=True)
    exec(code, module.__dict__)
    return module


def _nonempty_string_array(value: Any, *, exact_count: int | None = None) -> bool:
    if not isinstance(value, list) or \
            (exact_count is not None and len(value) != exact_count):
        return False
    validated: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            return False
        validated.append(item)
    return len(validated) == len(set(validated))


def authenticated_context() -> tuple[dict[str, Any] | None, list[str]]:
    """Authenticate all seven local dependencies before compiling any source."""
    errors: list[str] = []
    buffers: dict[str, bytes] = {}
    for name, expected in PINS.items():
        try:
            raw = (HERE / name).read_bytes()
        except OSError as exc:
            errors.append(f"OP7-DEP: cannot read {name}: {type(exc).__name__}: {exc}")
            continue
        buffers[name] = raw
        actual = _digest(raw)
        if actual != expected:
            errors.append(f"OP7-DEP: {name} hash {actual} != {expected}")
    if errors or set(buffers) != set(PINS):
        return None, errors or ["OP7-DEP: dependency closure is incomplete"]

    try:
        v6 = strict_loads(buffers["operability.v6.json"])
        v6_review = strict_loads(
            buffers["operability.v6.review-independent-prefreeze.json"])
        v5 = strict_loads(buffers["operability.v5.json"])
        v2 = strict_loads(buffers["operability.v2.json"])
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError,
            InputLimitError, RecursionError) as exc:
        return None, [f"OP7-DEP: authenticated data parse failed: {type(exc).__name__}: {exc}"]

    modules: dict[str, Any] = {}
    try:
        for filename, module_name in EXECUTABLE_DEPENDENCIES.items():
            modules[filename] = _compile_verified(
                buffers[filename], filename, module_name)
    except Exception as exc:
        return None, [
            f"OP7-DEP: verified source compile failed: {type(exc).__name__}: {exc}"]
    v6mod = modules["check-operability-v6.py"]
    v5mod = modules["check-operability-v5.py"]
    v2mod = modules["check-operability.py"]
    for label, module, binding in (
            ("OP6", v6mod, "operability.v6.json"),
            ("OP5", v5mod, "operability.v5.json"),
            ("OP2", v2mod, "operability.v2.json")):
        if getattr(module, "BINDING", None) != binding or \
                not callable(getattr(module, "check", None)):
            errors.append(f"OP7-DEP: verified {label} checker surface is incomplete")
    if not callable(getattr(v6mod, "project_v5", None)) or \
            not callable(getattr(v5mod, "project_op2", None)):
        errors.append("OP7-DEP: verified predecessor projection surface is incomplete")

    verdict = v6_review.get("verdict") if isinstance(v6_review, dict) else None
    blocking_ids = verdict.get("blockingFindingIds") if isinstance(verdict, dict) else None
    if not isinstance(verdict, dict) or verdict.get("decision") != "REJECT" or \
            not _nonempty_string_array(blocking_ids) or REVIEW_FINDING not in blocking_ids:
        errors.append("OP7-DEP: bound v6 review does not carry the exact rejection finding")
    try:
        if v6mod.project_v5(v6) != v5:
            errors.append("OP7-DEP: exact OP6 does not project to exact OP5")
        if v5mod.project_op2(v5) != v2:
            errors.append("OP7-DEP: exact OP5 does not project to protected OP2")
    except Exception as exc:
        errors.append(
            f"OP7-DEP: authenticated projection failed: {type(exc).__name__}: {exc}")
    if errors:
        return None, errors
    return {
        "buffers": buffers,
        "v6": v6,
        "v6_review": v6_review,
        "v5": v5,
        "v2": v2,
        "v6mod": v6mod,
        "v5mod": v5mod,
        "v2mod": v2mod,
    }, []


def expected_dependency_closure() -> dict[str, dict[str, str]]:
    return {
        "operability.v6.json": {
            "kind": "data", "sha256": PINS["operability.v6.json"]},
        "check-operability-v6.py": {
            "kind": "executable-source", "sha256": PINS["check-operability-v6.py"]},
        "operability.v6.review-independent-prefreeze.json": {
            "kind": "rejection-review-data",
            "sha256": PINS["operability.v6.review-independent-prefreeze.json"]},
        "operability.v5.json": {
            "kind": "protected-data", "sha256": PINS["operability.v5.json"]},
        "check-operability-v5.py": {
            "kind": "protected-executable-source",
            "sha256": PINS["check-operability-v5.py"]},
        "operability.v2.json": {
            "kind": "protected-data", "sha256": PINS["operability.v2.json"]},
        "check-operability.py": {
            "kind": "protected-executable-source",
            "sha256": PINS["check-operability.py"]},
    }


def expected_shape_declarations() -> dict[str, Any]:
    return {
        "reviewScopes": {
            "v6RequiredIndependentCombinedReview": {
                "path": "aPrimeSuccessor.operabilityV6Successor.requiredIndependentCombinedReview.scope",
                "containerType": "array",
                "itemType": "nonempty-string",
                "exactItemCount": 2,
                "duplicateItems": "FORBIDDEN",
            },
            "v7RequiredIndependentRereview": {
                "path": "aPrimeSuccessor.operabilityV7Successor.requiredIndependentRereview.scope",
                "containerType": "array",
                "itemType": "nonempty-string",
                "exactItemCount": 2,
                "duplicateItems": "FORBIDDEN",
            },
        },
        "eventSchemaStringArrays": {
            "required": "array-of-unique-nonempty-strings",
            "optional": "array-of-unique-nonempty-strings",
            "closedPlanes": "array-of-unique-nonempty-strings",
            "closedPhases": "array-of-unique-nonempty-strings",
        },
        "bindingFixtures": {
            "containerType": "array",
            "exactItemCount": 8,
            "elementType": "closed-object",
            "idType": "nonempty-string",
            "duplicateIds": "FORBIDDEN",
            "validType": "boolean-derived-not-trusted",
            "expectedErrorsType": "array-of-unique-nonempty-strings",
            "eventEnvelopeKeys": "inherited-required-plus-optional-only",
            "bindingMapKeys": "exactly-every-v3-closed-phase",
        },
        "phasePlaneBindings": {
            "containerType": "closed-object",
            "keySet": "exactly-every-v3-closed-phase",
            "run-committed": "progress",
            "allOtherValues": None,
        },
        "jsonInputBounds": {
            "maxRawBytes": MAX_RAW_BYTES,
            "maxDepth": MAX_DEPTH,
            "maxNodes": MAX_NODES,
            "maxArrayItems": MAX_ARRAY_ITEMS,
            "maxObjectMembers": MAX_OBJECT_MEMBERS,
            "maxStringUtf8Bytes": MAX_STRING_UTF8_BYTES,
        },
        "totalityRule": "Before any join, set construction, hash lookup, or list index, validate the container and every consumed member. Every bounded JSON list, object, null, boolean, number, or string shape returns named findings and never an exception.",
    }


def expected_v7_metadata(v6: dict[str, Any]) -> dict[str, Any]:
    changed = {
        key: {"before": copy.deepcopy(v6[key]),
              "after": copy.deepcopy(V7_ROOT[key])}
        for key in ROOT_ENVELOPE
    }
    return {
        "id": "OPERABILITY-V7-TOTALITY-ONLY-SUCCESSOR",
        "applicationState": "NOT-APPLIED",
        "authorityClaim": "NONE",
        "predecessorDisposition": "REJECT-EXACT-BYTES",
        "rejectionBinding": {
            "artifact": "operability.v6.review-independent-prefreeze.json",
            "sha256": PINS["operability.v6.review-independent-prefreeze.json"],
            "verdict": "REJECT",
            "blockingFindingId": REVIEW_FINDING,
        },
        "requiredIndependentRereview": {
            "state": "REQUIRED",
            "scope": [
                "the inherited, object-identical OPERABILITY v6 EventEnvelopeV3 lifecycle and store-provenance content",
                "the v7 totality-only shape declarations, checker implementation, rejection binding, and exact projection",
            ],
            "rule": "The rejected v6 checker is not an acceptance oracle. Independent rereview must cover the inherited v6 semantic slice and the v7 totality repair on the exact replacement bytes.",
        },
        "localDependencyClosure": expected_dependency_closure(),
        "closedShapeDeclarations": expected_shape_declarations(),
        "v7ToV6Projection": {
            "id": "OP7-TO-OP6-EXACT-PROJECTION",
            "predecessor": copy.deepcopy(V7_ROOT["supersedes"]),
            "algorithm": "Delete aPrimeSuccessor.operabilityV7Successor; restore the five root successor envelope fields from changedRootFields.before; canonical deep-compare the complete result to exact operability.v6.json bytes.",
            "changedRootFields": changed,
            "removedSuccessorMetadata": ["aPrimeSuccessor.operabilityV7Successor"],
            "deepEqualityRule": "The projection may remove only the enumerated v7 successor metadata and restore only the five enumerated root successor fields. The complete v6 EventEnvelopeV3 lifecycle object, bindings, fixtures, store-provenance semantics, G19/CD-RT-5 state, and OP6-to-OP5 projection remain object-identical.",
            "inheritedProjectionRule": "Exact OP7-to-OP6 projection must chain through unchanged OP6-to-OP5 and OP5-to-OP2 projections.",
        },
    }


def construct_expected_v7(v6: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(v6)
    for key, value in V7_ROOT.items():
        result[key] = copy.deepcopy(value)
    result["aPrimeSuccessor"]["operabilityV7Successor"] = expected_v7_metadata(v6)
    return result


def project_v6(candidate: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(candidate)
    successor = result["aPrimeSuccessor"]
    metadata = successor["operabilityV7Successor"]
    projection = metadata["v7ToV6Projection"]
    if set(projection["changedRootFields"]) != set(ROOT_ENVELOPE):
        raise ValueError("v7-to-v6 root envelope is not closed")
    if projection["removedSuccessorMetadata"] != [
            "aPrimeSuccessor.operabilityV7Successor"]:
        raise ValueError("v7-to-v6 metadata removal is not exact")
    successor.pop("operabilityV7Successor")
    for key in ROOT_ENVELOPE:
        result[key] = copy.deepcopy(projection["changedRootFields"][key]["before"])
    return result


_MISSING = object()


def _at(root: Any, path: tuple[str, ...]) -> Any:
    current = root
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return _MISSING
        current = current[key]
    return current


def _array_shape_findings(value: Any, path: str, *, exact_count: int | None = None,
                          allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        return [f"OP7-SHAPE: {path} must be an array"]
    findings: list[str] = []
    if exact_count is not None and len(value) != exact_count:
        findings.append(f"OP7-SHAPE: {path} item count must equal {exact_count}")
    validated: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or (not allow_empty and not item.strip()):
            findings.append(
                f"OP7-SHAPE: {path}[{index}] must be a nonempty string")
        else:
            validated.append(item)
    if len(validated) == len(value) and len(validated) != len(set(validated)):
        findings.append(f"OP7-SHAPE: {path} contains duplicate strings")
    return findings


def shape_findings(value: Any) -> list[str]:
    """Name all type-sensitive v6/v7 surfaces without unsafe aggregation."""
    findings: list[str] = []
    if not isinstance(value, dict):
        return ["OP7-SHAPE: root must be an object"]
    successor = value.get("aPrimeSuccessor")
    if not isinstance(successor, dict):
        return ["OP7-SHAPE: aPrimeSuccessor must be an object"]
    v6meta = successor.get("operabilityV6Successor")
    v7meta = successor.get("operabilityV7Successor")
    lifecycle = successor.get("lifecycle")
    if not isinstance(v6meta, dict):
        findings.append("OP7-SHAPE: operabilityV6Successor must be an object")
    if not isinstance(v7meta, dict):
        findings.append("OP7-SHAPE: operabilityV7Successor must be an object")
    if not isinstance(lifecycle, dict):
        findings.append("OP7-SHAPE: lifecycle must be an object")
    if findings:
        return findings

    for meta, field, label in (
            (v6meta, "requiredIndependentCombinedReview", "v6 combined review"),
            (v7meta, "requiredIndependentRereview", "v7 independent rereview")):
        review = meta.get(field)
        if not isinstance(review, dict):
            findings.append(f"OP7-SHAPE: {label} must be an object")
            continue
        if review.get("state") != "REQUIRED":
            findings.append(f"OP7-SHAPE: {label}.state must equal REQUIRED")
        findings.extend(_array_shape_findings(
            review.get("scope"), f"{label}.scope", exact_count=2))
        if not isinstance(review.get("rule"), str) or not review["rule"].strip():
            findings.append(f"OP7-SHAPE: {label}.rule must be a nonempty string")

    for meta, projection_name, label in (
            (v6meta, "v6ToV5Projection", "v6ToV5Projection"),
            (v7meta, "v7ToV6Projection", "v7ToV6Projection")):
        projection = meta.get(projection_name)
        if not isinstance(projection, dict):
            findings.append(f"OP7-SHAPE: {label} must be an object")
            continue
        changed = projection.get("changedRootFields")
        if not isinstance(changed, dict):
            findings.append(f"OP7-SHAPE: {label}.changedRootFields must be an object")
        else:
            if set(changed) != set(ROOT_ENVELOPE):
                findings.append(f"OP7-SHAPE: {label}.changedRootFields key set is not closed")
            for key in ROOT_ENVELOPE:
                row = changed.get(key)
                if not isinstance(row, dict) or "before" not in row or "after" not in row:
                    findings.append(
                        f"OP7-SHAPE: {label}.changedRootFields.{key} must be a before/after object")
        findings.extend(_array_shape_findings(
            projection.get("removedSuccessorMetadata"),
            f"{label}.removedSuccessorMetadata", exact_count=1))
        if projection_name == "v6ToV5Projection":
            findings.extend(_array_shape_findings(
                projection.get("removedLifecycleFields"),
                f"{label}.removedLifecycleFields", exact_count=3))

    for meta, label, expected_count in (
            (v6meta, "v6 localDependencyClosure", 4),
            (v7meta, "v7 localDependencyClosure", 7)):
        closure = meta.get("localDependencyClosure")
        if not isinstance(closure, dict) or len(closure) != expected_count:
            findings.append(
                f"OP7-SHAPE: {label} must be a closed {expected_count}-member object")
            continue
        for name, row in closure.items():
            if not isinstance(name, str) or not name:
                findings.append(f"OP7-SHAPE: {label} key must be a nonempty string")
            if not isinstance(row, dict) or not isinstance(row.get("kind"), str) or \
                    not isinstance(row.get("sha256"), str):
                findings.append(f"OP7-SHAPE: {label}.{name} row must contain string kind/sha256")

    schema = lifecycle.get("eventSchemaV3")
    if not isinstance(schema, dict):
        findings.append("OP7-SHAPE: eventSchemaV3 must be an object")
        return findings
    for key in ("required", "optional", "closedPlanes", "closedPhases"):
        findings.extend(_array_shape_findings(
            schema.get(key), f"eventSchemaV3.{key}"))
    phase_requirements = schema.get("phaseRequirements")
    if not isinstance(phase_requirements, dict):
        findings.append("OP7-SHAPE: eventSchemaV3.phaseRequirements must be an object")
    else:
        closed_phases = schema.get("closedPhases")
        if isinstance(closed_phases, list) and all(
                isinstance(item, str) for item in closed_phases):
            if set(phase_requirements) != set(closed_phases):
                findings.append("OP7-SHAPE: phaseRequirements key set is not closed")
        for phase, row in phase_requirements.items():
            if not isinstance(row, dict):
                findings.append(f"OP7-SHAPE: phaseRequirements.{phase} must be an object")

    constraint = lifecycle.get("schemaVersionConstraint")
    if not isinstance(constraint, dict):
        findings.append("OP7-SHAPE: schemaVersionConstraint must be an object")
    bindings = lifecycle.get("phasePlaneBindings")
    if not isinstance(bindings, dict):
        findings.append("OP7-SHAPE: phasePlaneBindings must be an object")
    else:
        closed_phases = schema.get("closedPhases")
        if isinstance(closed_phases, list) and all(
                isinstance(item, str) for item in closed_phases):
            if set(bindings) != set(closed_phases):
                findings.append("OP7-SHAPE: phasePlaneBindings key set is not closed")

    fixtures = lifecycle.get("bindingFixtures")
    if not isinstance(fixtures, list):
        findings.append("OP7-SHAPE: bindingFixtures must be an array")
        return findings
    if len(fixtures) != 8:
        findings.append("OP7-SHAPE: bindingFixtures item count must equal 8")
    valid_ids: list[str] = []
    for index, row in enumerate(fixtures):
        prefix = f"bindingFixtures[{index}]"
        if not isinstance(row, dict):
            findings.append(f"OP7-SHAPE: {prefix} must be an object")
            continue
        fixture_id = row.get("id")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            findings.append(f"OP7-SHAPE: {prefix}.id must be a nonempty string")
        else:
            valid_ids.append(fixture_id)
        kind = row.get("kind")
        if kind not in {"event-envelope", "phase-plane-bindings"}:
            findings.append(f"OP7-SHAPE: {prefix}.kind is not closed")
        if type(row.get("valid")) is not bool:
            findings.append(f"OP7-SHAPE: {prefix}.valid must be boolean")
        findings.extend(_array_shape_findings(
            row.get("expectedErrors"), f"{prefix}.expectedErrors", allow_empty=False))
        if kind == "event-envelope" and not isinstance(row.get("envelope"), dict):
            findings.append(f"OP7-SHAPE: {prefix}.envelope must be an object")
        if kind == "phase-plane-bindings" and not isinstance(row.get("bindings"), dict):
            findings.append(f"OP7-SHAPE: {prefix}.bindings must be an object")
    if len(valid_ids) == len(fixtures) and len(valid_ids) != len(set(valid_ids)):
        findings.append("OP7-SHAPE: bindingFixtures contains duplicate ids")
    return findings


def _gate(root: Any, gate_id: str) -> dict[str, Any] | None:
    if not isinstance(root, dict) or not isinstance(root.get("validationGates"), list):
        return None
    rows: list[dict[str, Any]] = []
    for row in root["validationGates"]:
        if isinstance(row, dict) and row.get("id") == gate_id:
            rows.append(row)
    return rows[0] if len(rows) == 1 else None


def _check_impl(value: Any, *, verify_files: bool,
                context: dict[str, Any] | None) -> list[str]:
    limits = json_value_findings(value)
    if limits:
        return limits
    if not isinstance(value, dict):
        return ["OP7-TOTALITY: root is not an object"]
    if context is None:
        if not verify_files:
            return ["OP7-DEP: unauthenticated context is forbidden"]
        context, dependency_errors = authenticated_context()
        if dependency_errors or context is None:
            return dependency_errors or ["OP7-DEP: no authenticated context"]
    v6 = context.get("v6")
    v5 = context.get("v5")
    v2 = context.get("v2")
    v6mod = context.get("v6mod")
    v5mod = context.get("v5mod")
    if not isinstance(v6, dict) or not isinstance(v5, dict) or \
            not isinstance(v2, dict) or v6mod is None or v5mod is None:
        return ["OP7-DEP: malformed authenticated context"]

    expected = construct_expected_v7(v6)
    exact = value == expected
    findings: list[str] = []
    if not exact:
        findings.append("OP7-FULL: candidate differs from complete expected v7 construction")
    findings.extend(shape_findings(value))
    # No projection, rejected-v6 checker call, set aggregation beyond validated
    # strings, or nested candidate indexing occurs on a non-exact candidate.
    if not exact:
        return findings
    if findings:
        return findings

    successor = value["aPrimeSuccessor"]
    v7meta = successor["operabilityV7Successor"]
    if any(value[key] != V7_ROOT[key] for key in ROOT_ENVELOPE):
        findings.append("OP7-META: closed root successor metadata drift")
    if v7meta != expected_v7_metadata(v6):
        findings.append("OP7-META: complete v7 successor metadata drift")
    if v7meta["localDependencyClosure"] != expected_dependency_closure():
        findings.append("OP7-DEP: declared seven-file dependency closure drift")
    if v7meta["closedShapeDeclarations"] != expected_shape_declarations():
        findings.append("OP7-SHAPE: closed shape declaration drift")
    review = context["v6_review"]
    if v7meta["rejectionBinding"] != {
            "artifact": "operability.v6.review-independent-prefreeze.json",
            "sha256": PINS["operability.v6.review-independent-prefreeze.json"],
            "verdict": "REJECT",
            "blockingFindingId": REVIEW_FINDING} or \
            review["verdict"]["decision"] != "REJECT":
        findings.append("OP7-REVIEW: exact v6 rejection binding drift")
    if successor["lifecycle"] != v6["aPrimeSuccessor"]["lifecycle"]:
        findings.append("OP7-SEMANTIC: EventEnvelopeV3 lifecycle object differs from v6")
    if successor["operabilityV6Successor"] != \
            v6["aPrimeSuccessor"]["operabilityV6Successor"]:
        findings.append("OP7-SEMANTIC: inherited v6 successor/binding object changed")

    try:
        projected_v6 = project_v6(value)
        if projected_v6 != v6:
            findings.append("OP7-PROJ: v7 does not project exact-deep-equal to v6")
        projected_v5 = v6mod.project_v5(projected_v6)
        if projected_v5 != v5:
            findings.append("OP7-PROJ: projected v6 does not project exact-deep-equal to v5")
        if v5mod.project_op2(projected_v5) != v2:
            findings.append("OP7-PROJ: projected v5 does not project exact-deep-equal to OP2")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(
            f"OP7-PROJ: controlled clean projection failure: {type(exc).__name__}: {exc}")
        projected_v6 = None

    if projected_v6 is not None:
        v6_context = {
            "op5": v5,
            "op2": v2,
            "op5mod": v5mod,
            "op2mod": context["v2mod"],
        }
        try:
            inherited_findings = v6mod.check(
                projected_v6, verify_files=False, context=v6_context)
        except Exception as exc:
            findings.append(
                f"OP7-INHERITED: controlled exact-v6 validation failure: {type(exc).__name__}: {exc}")
        else:
            if inherited_findings:
                findings.append(
                    f"OP7-INHERITED: exact v6 semantic checker red: {inherited_findings[0]}")
    if _gate(value, "G19") != _gate(v6, "G19") or \
            (_gate(value, "G19") or {}).get("status") != "BLOCKED-NO-MECHANISM":
        findings.append("OP7-G19: inherited gate changed or was promoted")
    return findings


def check(value: Any, *, verify_files: bool = True,
          context: dict[str, Any] | None = None) -> list[str]:
    """Total over bounded JSON values; unexpected shape errors become findings."""
    try:
        return _check_impl(value, verify_files=verify_files, context=context)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError,
            OverflowError, RecursionError) as exc:
        return [
            f"OP7-TOTALITY-INTERNAL: controlled {type(exc).__name__}: {exc}"]


PathPart = str | int


def _path_value(root: Any, path: tuple[PathPart, ...]) -> Any:
    current = root
    for part in path:
        current = current[part]
    return current


def _replace_path(root: Any, path: tuple[PathPart, ...], replacement: Any) -> None:
    current = root
    for part in path[:-1]:
        current = current[part]
    current[path[-1]] = replacement


def _format_path(path: tuple[PathPart, ...]) -> str:
    rendered = "$"
    for part in path:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


SENSITIVE_KEYS = {
    "id", "kind", "valid", "expectedErrors", "scope", "state", "rule",
    "field", "operator", "value", "schemaVersion", "plane", "phase",
    "requestId", "budgetOwner", "payloadType", "payloadBytes", "executionId",
    "runId", "bindings", "envelope", "removedSuccessorMetadata",
    "removedLifecycleFields", "changedRootFields", "localDependencyClosure",
    "sha256", "verdict", "blockingFindingId", "exactItemCount",
}


def heterogeneous_targets(value: dict[str, Any]) -> list[tuple[PathPart, ...]]:
    """Enumerate every list element and shape-sensitive field in the v6/v7 slice."""
    roots = [
        ("aPrimeSuccessor", "operabilityV6Successor", "requiredIndependentCombinedReview"),
        ("aPrimeSuccessor", "operabilityV6Successor", "v6ToV5Projection"),
        ("aPrimeSuccessor", "operabilityV7Successor"),
        ("aPrimeSuccessor", "lifecycle", "eventSchemaV3"),
        ("aPrimeSuccessor", "lifecycle", "schemaVersionConstraint"),
        ("aPrimeSuccessor", "lifecycle", "phasePlaneBindings"),
        ("aPrimeSuccessor", "lifecycle", "bindingFixtures"),
    ]
    targets: dict[tuple[PathPart, ...], None] = {}

    def walk(node: Any, path: tuple[PathPart, ...]) -> None:
        if isinstance(node, list):
            for index, child in enumerate(node):
                child_path = path + (index,)
                targets[child_path] = None
                walk(child, child_path)
        elif isinstance(node, dict):
            for key, child in node.items():
                child_path = path + (key,)
                if key in SENSITIVE_KEYS:
                    targets[child_path] = None
                walk(child, child_path)

    for root_path in roots:
        walk(_path_value(value, root_path), root_path)
    return list(targets)


def selftest(value: dict[str, Any], context: dict[str, Any]) -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    targeted: list[tuple[str, dict[str, Any]]] = []
    heterogeneous: list[tuple[str, dict[str, Any]]] = []

    def add(target: list[tuple[str, dict[str, Any]]], label: str,
            mutate: Any) -> None:
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
        target.append((label, candidate))

    v7meta = lambda c: c["aPrimeSuccessor"]["operabilityV7Successor"]
    lifecycle = lambda c: c["aPrimeSuccessor"]["lifecycle"]
    add(targeted, "status promotion", lambda c: c.__setitem__("status", "APPLIED"))
    add(targeted, "rejection binding erased", lambda c: v7meta(c)["rejectionBinding"].__setitem__("verdict", "PASS"))
    add(targeted, "incomplete dependency closure", lambda c: v7meta(c)["localDependencyClosure"].pop("operability.v6.review-independent-prefreeze.json"))
    add(targeted, "weaken exact projection", lambda c: v7meta(c)["v7ToV6Projection"].__setitem__("deepEqualityRule", "field presence"))
    add(targeted, "semantic schema version change", lambda c: lifecycle(c)["schemaVersionConstraint"].__setitem__("value", 4))
    add(targeted, "semantic run-committed plane change", lambda c: lifecycle(c)["phasePlaneBindings"].__setitem__("run-committed", "diagnostics"))
    add(targeted, "exact review scope object counterexample", lambda c: c["aPrimeSuccessor"]["operabilityV6Successor"]["requiredIndependentCombinedReview"].__setitem__("scope", [{}]))
    add(targeted, "exact fixture id list counterexample", lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("id", []))
    add(targeted, "exact fixture id object counterexample", lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("id", {}))
    add(targeted, "duplicate fixture id", lambda c: lifecycle(c)["bindingFixtures"][1].__setitem__("id", lifecycle(c)["bindingFixtures"][0]["id"]))
    add(targeted, "authored valid boolean shortcut", lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("valid", False))

    variants: list[tuple[str, Any]] = [
        ("list", ["heterogeneous"]),
        ("object", {"heterogeneous": True}),
        ("null", None),
        ("scalar", 7),
    ]
    for path in heterogeneous_targets(value):
        original = _path_value(value, path)
        for variant_name, replacement in variants:
            if original == replacement and type(original) is type(replacement):
                continue
            add(
                heterogeneous,
                f"heterogeneous {variant_name} at {_format_path(path)}",
                lambda candidate, p=path, r=copy.deepcopy(replacement):
                    _replace_path(candidate, p, r),
            )

    for label, candidate in targeted + heterogeneous:
        try:
            findings = check(candidate, verify_files=False, context=context)
        except Exception as exc:
            failures.append(f"{label}: uncontrolled {type(exc).__name__}: {exc}")
            continue
        if not findings:
            failures.append(f"{label}: escaped")

    totality_values: list[tuple[str, Any]] = [
        ("null root", None),
        ("boolean root", True),
        ("integer root", 7),
        ("float root", 7.5),
        ("string root", "hostile-root"),
        ("array root", []),
        ("empty object", {}),
        ("nonfinite number", float("nan")),
        ("non-JSON tuple", ("tuple",)),
    ]
    deep: Any = "leaf"
    for _ in range(MAX_DEPTH + 2):
        deep = [deep]
    totality_values.extend([
        ("depth bound", deep),
        ("array-size bound", [None] * (MAX_ARRAY_ITEMS + 1)),
        ("object-size bound", {f"k{i}": None for i in range(MAX_OBJECT_MEMBERS + 1)}),
        ("string-size bound", "x" * (MAX_STRING_UTF8_BYTES + 1)),
    ])
    for label, candidate in totality_values:
        try:
            findings = check(candidate, verify_files=False, context=context)
        except Exception as exc:
            failures.append(f"{label}: uncontrolled {type(exc).__name__}: {exc}")
            continue
        if not findings:
            failures.append(f"{label}: malformed/bounded input escaped")

    parser_controls = 0
    try:
        strict_loads(b'{"root": {"duplicate": 1, "duplicate": 2}}')
    except DuplicateKeyError:
        parser_controls += 1
    except Exception as exc:
        failures.append(f"duplicate JSON: uncontrolled {type(exc).__name__}: {exc}")
    else:
        failures.append("duplicate JSON escaped")
    try:
        strict_loads(b" " * (MAX_RAW_BYTES + 1))
    except InputLimitError:
        parser_controls += 1
    except Exception as exc:
        failures.append(f"raw-size bound: uncontrolled {type(exc).__name__}: {exc}")
    else:
        failures.append("raw-size bound escaped")

    return failures, {
        "targeted": len(targeted),
        "heterogeneous": len(heterogeneous),
        "jsonTotality": len(totality_values),
        "parser": parser_controls,
    }


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        raw = path.read_bytes()
        value = strict_loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError,
            InputLimitError, RecursionError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    context, dependency_errors = authenticated_context()
    if dependency_errors or context is None:
        if "--selftest" in argv[1:]:
            print("REFUSING selftest: OPERABILITY v7 base/dependency closure is dirty")
        for error in dependency_errors or ["OP7-DEP: no authenticated context"]:
            print(f"FAIL: {error}")
        return 1
    errors = check(value, verify_files=False, context=context)
    if errors:
        if "--selftest" in argv[1:]:
            print("REFUSING selftest: OPERABILITY v7 base/dependency closure is dirty")
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    artifact_hash = _digest(raw)
    if "--selftest" in argv[1:]:
        failures, counts = selftest(value, context)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(
            f"PASS: operability.v7.json@sha256:{artifact_hash}; "
            f"{counts['targeted']} targeted mutations, "
            f"{counts['heterogeneous']} systematic heterogeneous replacements, "
            f"{counts['jsonTotality']} JSON/API totality controls, and "
            f"{counts['parser']} duplicate/raw-bound parser controls rejected"
        )
    else:
        print(
            f"PASS: operability.v7.json@sha256:{artifact_hash}; "
            "exact OP7->OP6->OP5->OP2 projection; v6 lifecycle object-identical; "
            "7/7 dependencies authenticated before verified-buffer compilation; "
            "OP6-IR-01 counterexamples controlled"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
