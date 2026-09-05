#!/usr/bin/env python3
"""Retained checker for the R1 Rust pure-core realization candidate v1.5.

Run only as:
  python3 -I -B docs/coop/artifacts/check-r1-v1.5.py [--selftest]

The checker is author-side, bounded evidence.  It cannot accept, apply, seal,
freeze, demonstrate, or product-qualify the candidate it checks.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CONTRACT_PATH = HERE / "r1-lifetime-neutrality.conformance.v1.5.json"

EXPECTED_FROZEN_PINS = [
    (
        "R1-V1_4",
        "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.4.json",
        "7351b3d205097151fde08bd6c2014bcd2e7fac372049e4fd78213c3cda5cf69a",
    ),
    (
        "R1-V1_4-REVIEW",
        "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.4.review-reviewer2.json",
        "73b3d408f12de6d2babd66b28f7aa8077814818b34e62e4d8ae2b047c94ba118",
    ),
    (
        "R1-FREEZE-COORDINATOR",
        "docs/coop/artifacts/r1-lifetime-neutrality.freeze-closure-coordinator.v1.json",
        "6bf90f21178007a2df2313a18d230cf0d3b8f309dd2937c5668603b27a11569d",
    ),
    (
        "R1-V1_4-CHECKER",
        "docs/coop/artifacts/check-r1.py",
        "6d994743b5d56e8abcae44cc49573c7673d1aafbd51fc4f81297f8e6f5210cb2",
    ),
    (
        "PHASE3-V4-MARKDOWN",
        "/private/tmp/phase3-implementer-delta/PHASE3-IMPLEMENTER-DELTA-v4.md",
        "fb67cb04712a556c0d70705122a299714f2885e7ea9741c902365539d663a26c",
    ),
    (
        "PHASE3-V4-MANIFEST",
        "/private/tmp/phase3-implementer-delta/direct-dependencies.v4.json",
        "018e3ef7c7598f38707b59ab0866aa82ffe3370059e98b200c7a76fa201fff75",
    ),
    (
        "PHASE3-V4-INDEPENDENT-REVIEW",
        "/private/tmp/phase3-implementer-delta/PRELIMINARY-BLIND-LITMUS-v4-REREVIEW.md",
        "7a74575ff59a05f2857b6f9162912bf9146b93e8e173809d3d710d12c3de6046",
    ),
]

EXPECTED_D9_PATH = "docs/coop/artifacts/d9-exit-contract.v1.13.json"
EXPECTED_D9_SHA = "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae"
EXPECTED_FACT_PATH = "docs/coop/artifacts/fact-plane.v1.json"
EXPECTED_FACT_SHA = "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d"

SIGNATURE = (
    "evaluate(stageInput: &SealedStageInput, deps: &CoreDeps, "
    "attempt: &AttemptMetadata) -> CoreCompletion"
)
ATTEMPT_FIELDS = ["executionId"]
CORE_DEPS_FIELDS = ["rules", "policy", "budgetLimits"]
COMPLETION_FIELDS = {
    "completed": [
        "variant",
        "findings",
        "exactCoverage",
        "policyOutcome",
        "diagnostics",
        "budgetUsage",
    ],
    "incomplete": [
        "variant",
        "partialFindings",
        "exactCoverage",
        "deficiency",
        "policyOutcome",
        "diagnostics",
        "budgetUsage",
    ],
    "cancelled": ["variant", "exactCoverage", "diagnostics", "budgetUsage"],
    "faulted": ["variant", "faultCause", "diagnostics", "budgetUsage"],
}
FACT_DEFICIENCIES = [
    "required-relation-missing",
    "provider-unavailable",
    "language-tier-unsupported",
    "budget-exhausted",
    "confidence-floor-unmet",
]
D9_CAUSES_WITH_NONE = [
    "none",
    "host-io",
    "ledger-busy",
    "ledger-corrupt",
    "cas-link",
    "provider-protocol",
    "durability-commit",
    "delivery-required",
    "output-serialization",
    "extension-install-io",
    "serve-protocol",
]
ALLOWED_DEPS = [
    "opensip-types",
    "opensip-plan",
    "opensip-facts",
    "opensip-rules",
    "opensip-policy",
    "opensip-d9-values",
]
DEPENDENCY_CLASSES = [
    "normal",
    "build",
    "devOnly",
    "targetSpecific",
    "optional",
    "featureEnabled",
]

TOP_LEVEL_KEYS = [
    "artifact",
    "version",
    "status",
    "reviewStatus",
    "evidenceGrade",
    "purpose",
    "supersedesIfAccepted",
    "authorityBoundary",
    "frozenInputs",
    "externalValueBindings",
    "architectureInheritance",
    "rustApi",
    "schemaLanguage",
    "closedTypes",
    "localEvaluationState",
    "evidenceIdentity",
    "d9Boundary",
    "staticAndRuntimeClosure",
    "conformanceModel",
    "positiveVectors",
    "adversarialControls",
    "staticClosureFixtures",
    "requiredCheckerProperties",
    "assurance",
    "reviewRequests",
    "residuals",
]

RECORD_FIELDS = {
    "CanonicalValueRef": ["kind", "digest"],
    "SealedStageInput": [
        "observationSet",
        "targetUniverseId",
        "coverageContext",
        "planStageIds",
    ],
    "AttemptMetadata": ["executionId"],
    "RuleValue": ["ruleId", "artifactDigest"],
    "RuleSet": ["entries"],
    "PolicyValue": ["policyId", "artifactDigest"],
    "BudgetLimits": ["ruleUnits", "policyUnits", "diagnosticRecords"],
    "CoreDeps": ["rules", "policy", "budgetLimits"],
    "FindingValue": ["ruleId", "findingId", "valueDigest"],
    "CoverageEntry": ["coverageKey", "state"],
    "ExactCoverage": ["entries"],
    "PolicyOutcome": ["policyId", "verdict", "derivationDigest"],
    "DiagnosticRecord": ["ordinal", "code", "message"],
    "DiagnosticsData": ["records", "droppedCount"],
    "BudgetUsage": [
        "ruleUnits",
        "policyUnits",
        "diagnosticRecordsAccepted",
        "diagnosticRecordsDropped",
    ],
}


class StrictJsonError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise StrictJsonError("R1V15-JSON-DUPLICATE", f"duplicate key {key!r}")
        out[key] = value
    return out


def _reject_float(token: str) -> Any:
    raise StrictJsonError("R1V15-JSON-FLOAT", f"float forbidden: {token}")


def _reject_constant(token: str) -> Any:
    raise StrictJsonError("R1V15-JSON-NONFINITE", f"non-finite forbidden: {token}")


def strict_loads(raw: str) -> Any:
    try:
        return json.loads(
            raw,
            object_pairs_hook=_pairs,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except StrictJsonError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise StrictJsonError("R1V15-JSON-SYNTAX", str(exc)) from exc


def strict_load(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise StrictJsonError("R1V15-SOURCE-READ", f"{path}: {exc}") from exc
    return strict_loads(raw)


def pinned_json_load(path: Path) -> Any:
    """Load a hash-authenticated external contract without imposing R1's no-float wire.

    Some predecessor contracts legitimately contain confidence decimals.  Their exact
    bytes are authenticated first; duplicate names and non-finite values still reject.
    The R1 v1.5 candidate and every value in its own corpus always use strict_loads.
    """
    try:
        raw = path.read_text(encoding="utf-8")
        return json.loads(
            raw,
            object_pairs_hook=_pairs,
            parse_constant=_reject_constant,
        )
    except StrictJsonError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StrictJsonError("R1V15-SOURCE-READ", f"{path}: {exc}") from exc


def _path(path: str) -> Path:
    p = Path(path)
    return p if p.is_absolute() else REPO / p


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _finding(code: str, where: str, detail: str) -> dict[str, str]:
    return {"code": code, "where": where, "detail": detail}


def _add(findings: list[dict[str, str]], code: str, where: str, detail: str) -> None:
    findings.append(_finding(code, where, detail))


def _eq(
    findings: list[dict[str, str]],
    actual: Any,
    expected: Any,
    code: str,
    where: str,
) -> None:
    if actual != expected:
        _add(findings, code, where, f"expected {expected!r}; got {actual!r}")


def _get(obj: Any, keys: list[str], default: Any = None) -> Any:
    cur = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def _pointer(obj: Any, pointer: str) -> Any:
    cur = obj
    if not pointer.startswith("/"):
        raise KeyError(pointer)
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(token)]
        else:
            cur = cur[token]
    return cur


def _validate_value(
    value: Any,
    spec: Any,
    types: dict[str, Any],
    where: str,
    findings: list[dict[str, str]],
) -> None:
    """Total recursive validator for the contract's closed value language."""
    if not isinstance(spec, dict):
        _add(findings, "R1V15-SCHEMA-SPEC", where, "schema node is not an object")
        return
    if "$ref" in spec:
        ref = spec.get("$ref")
        if not isinstance(ref, str) or ref not in types:
            _add(findings, "R1V15-SCHEMA-REF", where, f"unknown ref {ref!r}")
            return
        _validate_value(value, types[ref], types, where, findings)
        required_kind = spec.get("requiredKind")
        if required_kind is not None:
            if not isinstance(value, dict) or value.get("kind") != required_kind:
                _add(
                    findings,
                    "R1V15-SCHEMA-CONSTRAINT",
                    where,
                    f"required kind {required_kind!r}",
                )
        return

    kind = spec.get("kind")
    if kind == "record":
        if not isinstance(value, dict):
            _add(findings, "R1V15-SCHEMA-TYPE", where, "expected object")
            return
        order = spec.get("fieldOrder")
        fields = spec.get("fields")
        if not isinstance(order, list) or not all(isinstance(x, str) for x in order):
            _add(findings, "R1V15-SCHEMA-SPEC", where, "invalid fieldOrder")
            return
        if not isinstance(fields, dict):
            _add(findings, "R1V15-SCHEMA-SPEC", where, "invalid fields")
            return
        expected = set(order)
        actual = set(value)
        for missing in sorted(expected - actual):
            _add(findings, "R1V15-SCHEMA-MISSING", f"{where}.{missing}", "required field missing")
        for extra in sorted(actual - expected):
            _add(findings, "R1V15-SCHEMA-UNKNOWN", f"{where}.{extra}", "unknown field")
        for key in order:
            if key in value and key in fields:
                _validate_value(value[key], fields[key], types, f"{where}.{key}", findings)
        return

    if kind == "array":
        if not isinstance(value, list):
            _add(findings, "R1V15-SCHEMA-TYPE", where, "expected array")
            return
        minimum = spec.get("minimumItems", 0)
        maximum = spec.get("maximumItems")
        if isinstance(minimum, int) and len(value) < minimum:
            _add(findings, "R1V15-SCHEMA-RANGE", where, "too few items")
        if isinstance(maximum, int) and len(value) > maximum:
            _add(findings, "R1V15-SCHEMA-RANGE", where, "too many items")
        item_spec = spec.get("items")
        for index, item in enumerate(value):
            _validate_value(item, item_spec, types, f"{where}[{index}]", findings)
        order_rule = spec.get("orderRule", "")
        uniqueness = spec.get("uniquenessRule", "")
        try:
            keys: list[Any] | None = None
            if order_rule.startswith("strict ascending UTF-8 byte order by ruleId"):
                keys = [x.get("ruleId") if isinstance(x, dict) else None for x in value]
            elif order_rule.startswith("strict ascending tuple"):
                keys = [
                    (x.get("ruleId"), x.get("findingId"), x.get("valueDigest"))
                    if isinstance(x, dict)
                    else None
                    for x in value
                ]
            elif order_rule.startswith("strict ascending UTF-8 byte order by coverageKey"):
                keys = [x.get("coverageKey") if isinstance(x, dict) else None for x in value]
            elif order_rule.startswith("strict emission order"):
                keys = [x.get("ordinal") if isinstance(x, dict) else None for x in value]
                if keys != list(range(len(value))):
                    _add(findings, "R1V15-SCHEMA-ORDER", where, "diagnostic ordinals not contiguous emission order")
                keys = None
            elif order_rule.startswith("caller-declared Plan stage order"):
                keys = None
            if keys is not None and all(k is not None for k in keys):
                if keys != sorted(keys) or any(a == b for a, b in zip(keys, keys[1:])):
                    _add(findings, "R1V15-SCHEMA-ORDER", where, "strict order violated")
            unique_keys: list[Any] | None = None
            if uniqueness == "exact string uniqueness":
                unique_keys = list(value)
            elif uniqueness == "ruleId":
                unique_keys = [x.get("ruleId") if isinstance(x, dict) else None for x in value]
            elif uniqueness == "tuple(ruleId,findingId,valueDigest)":
                unique_keys = [
                    (x.get("ruleId"), x.get("findingId"), x.get("valueDigest"))
                    if isinstance(x, dict)
                    else None
                    for x in value
                ]
            elif uniqueness == "coverageKey":
                unique_keys = [x.get("coverageKey") if isinstance(x, dict) else None for x in value]
            elif uniqueness == "ordinal":
                unique_keys = [x.get("ordinal") if isinstance(x, dict) else None for x in value]
            if unique_keys is not None:
                encoded = [repr(x) for x in unique_keys]
                if len(encoded) != len(set(encoded)):
                    _add(findings, "R1V15-SCHEMA-UNIQUE", where, "uniqueness violated")
        except Exception as exc:  # total malformed handling
            _add(findings, "R1V15-SCHEMA-TOTALITY", where, f"order oracle: {exc}")
        return

    if kind == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            _add(findings, "R1V15-SCHEMA-TYPE", where, "expected exact integer")
            return
        minimum = spec.get("minimum")
        maximum = spec.get("maximum")
        if not isinstance(minimum, int) or not isinstance(maximum, int):
            _add(findings, "R1V15-SCHEMA-SPEC", where, "integer bounds invalid")
        elif value < minimum or value > maximum:
            _add(findings, "R1V15-SCHEMA-RANGE", where, "integer outside bounds")
        return

    if kind == "string":
        if not isinstance(value, str):
            _add(findings, "R1V15-SCHEMA-TYPE", where, "expected string")
            return
        pattern = spec.get("pattern")
        if pattern is not None:
            try:
                if re.fullmatch(pattern, value) is None:
                    _add(findings, "R1V15-SCHEMA-PATTERN", where, "string does not match")
            except re.error as exc:
                _add(findings, "R1V15-SCHEMA-SPEC", where, f"bad pattern: {exc}")
        minimum = spec.get("minimumLength")
        if isinstance(minimum, int) and len(value) < minimum:
            _add(findings, "R1V15-SCHEMA-RANGE", where, "string too short")
        max_bytes = spec.get("maximumUtf8Bytes")
        if isinstance(max_bytes, int) and len(value.encode("utf-8")) > max_bytes:
            _add(findings, "R1V15-SCHEMA-RANGE", where, "UTF-8 string too long")
        return

    if kind == "enum":
        values = spec.get("values")
        if not isinstance(values, list) or value not in values:
            _add(findings, "R1V15-SCHEMA-ENUM", where, f"not in enum {values!r}")
        return

    if kind == "const":
        if value != spec.get("value"):
            _add(findings, "R1V15-SCHEMA-CONST", where, "constant mismatch")
        return

    if kind == "union":
        if not isinstance(value, dict):
            _add(findings, "R1V15-SCHEMA-TYPE", where, "expected tagged object")
            return
        tag = spec.get("tag")
        variants = spec.get("variants")
        if not isinstance(tag, str) or not isinstance(variants, dict):
            _add(findings, "R1V15-SCHEMA-SPEC", where, "invalid union schema")
            return
        selected = value.get(tag)
        if selected not in variants:
            _add(findings, "R1V15-SCHEMA-UNION", where, f"unknown variant {selected!r}")
            return
        _validate_value(value, variants[selected], types, where, findings)
        return

    _add(findings, "R1V15-SCHEMA-SPEC", where, f"unknown kind {kind!r}")


def _set_dotted(obj: dict[str, Any], dotted: str, value: Any) -> bool:
    parts = dotted.split(".")
    cur: Any = obj
    for part in parts[:-1]:
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    if not isinstance(cur, dict) or parts[-1] not in cur:
        return False
    cur[parts[-1]] = copy.deepcopy(value)
    return True


def _materialize_vectors(
    vectors: Any, findings: list[dict[str, str]]
) -> dict[str, dict[str, Any]]:
    if not isinstance(vectors, list):
        _add(findings, "R1V15-VECTORS", "positiveVectors", "must be array")
        return {}
    raw: dict[str, dict[str, Any]] = {}
    for index, vector in enumerate(vectors):
        if not isinstance(vector, dict) or not isinstance(vector.get("id"), str):
            _add(findings, "R1V15-VECTORS", f"positiveVectors[{index}]", "missing id")
            continue
        if vector["id"] in raw:
            _add(findings, "R1V15-VECTORS", vector["id"], "duplicate id")
        raw[vector["id"]] = vector

    cache: dict[str, dict[str, Any]] = {}
    active: set[str] = set()

    def build(vector_id: str) -> dict[str, Any]:
        if vector_id in cache:
            return copy.deepcopy(cache[vector_id])
        if vector_id in active:
            _add(findings, "R1V15-VECTORS", vector_id, "clone cycle")
            return {}
        active.add(vector_id)
        source = raw.get(vector_id)
        if source is None:
            _add(findings, "R1V15-VECTORS", vector_id, "unknown clone target")
            active.discard(vector_id)
            return {}
        parent_id = source.get("cloneOf")
        if parent_id is None:
            out = copy.deepcopy(source)
        elif not isinstance(parent_id, str):
            _add(findings, "R1V15-VECTORS", vector_id, "cloneOf must be string")
            out = {}
        else:
            parent = build(parent_id)
            out = {
                key: copy.deepcopy(parent[key])
                for key in (
                    "stageInput",
                    "deps",
                    "attempt",
                    "completionTemplate",
                    "exhaustionCompletion",
                )
                if key in parent
            }
            overrides = source.get("overrides", {})
            if not isinstance(overrides, dict):
                _add(findings, "R1V15-VECTORS", vector_id, "overrides must be object")
            else:
                for dotted, value in overrides.items():
                    if not isinstance(dotted, str) or not _set_dotted(out, dotted, value):
                        _add(findings, "R1V15-VECTORS", vector_id, f"override failed: {dotted!r}")
            for key, value in source.items():
                if key not in {"cloneOf", "overrides"}:
                    out[key] = copy.deepcopy(value)
        out["id"] = vector_id
        active.discard(vector_id)
        cache[vector_id] = copy.deepcopy(out)
        return out

    for vector_id in raw:
        build(vector_id)
    return cache


def _completion_projection(contract: dict[str, Any], completion: dict[str, Any]) -> dict[str, Any]:
    fields = contract["evidenceIdentity"]["projectionByVariant"][completion["variant"]]
    return {field: copy.deepcopy(completion[field]) for field in fields}


def _projection_commitment(contract: dict[str, Any], completion: dict[str, Any]) -> str:
    projection = _completion_projection(contract, completion)
    payload = json.dumps(
        projection,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(b"opensip:r1-v1.5:projection\x00" + payload).hexdigest()


def _run_vector(
    contract: dict[str, Any],
    vector: dict[str, Any],
    findings: list[dict[str, str]],
) -> tuple[dict[str, Any] | None, str | None]:
    where = vector.get("id", "<vector>")
    types = contract.get("closedTypes", {})
    for field, type_name in (
        ("stageInput", "SealedStageInput"),
        ("deps", "CoreDeps"),
        ("attempt", "AttemptMetadata"),
    ):
        if field not in vector:
            _add(findings, "R1V15-VECTOR-MISSING", where, f"missing {field}")
        elif isinstance(types, dict) and type_name in types:
            _validate_value(vector[field], types[type_name], types, f"{where}.{field}", findings)

    deps = vector.get("deps")
    if not isinstance(deps, dict):
        return None, None
    limits = _get(deps, ["budgetLimits"])
    if not isinstance(limits, dict):
        return None, None
    remaining = {"ruleUnits": limits.get("ruleUnits"), "policyUnits": limits.get("policyUnits")}
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in remaining.values()):
        return None, None
    capacity = limits.get("diagnosticRecords")
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
        return None, None
    usage: dict[str, int] = {
        "ruleUnits": 0,
        "policyUnits": 0,
        "diagnosticRecordsAccepted": 0,
        "diagnosticRecordsDropped": 0,
    }
    records: list[dict[str, Any]] = []
    next_ordinal = 0
    events = vector.get("events")
    if not isinstance(events, list):
        _add(findings, "R1V15-EVENT", where, "events must be array")
        return None, None
    completion: dict[str, Any] | None = None
    exhausted = False
    returned = False
    diagnostic_allowed = False
    diagnostic_used = False

    for index, event in enumerate(events):
        ewhere = f"{where}.events[{index}]"
        if not isinstance(event, dict):
            _add(findings, "R1V15-EVENT", ewhere, "event must be object")
            continue
        kind = event.get("kind")
        if kind == "charge":
            _eq(
                findings,
                set(event),
                {"kind", "counter", "coverageKey"},
                "R1V15-EVENT",
                ewhere,
            )
            counter = event.get("counter")
            coverage_key = event.get("coverageKey")
            if counter not in {"ruleUnits", "policyUnits"}:
                _add(findings, "R1V15-EVENT", ewhere, "unknown counter")
                continue
            if not isinstance(coverage_key, str):
                _add(findings, "R1V15-EVENT", ewhere, "coverageKey must be string")
                continue
            diagnostic_allowed = False
            diagnostic_used = False
            if remaining[counter] == 0:
                exhausted = True
                template = vector.get("exhaustionCompletion")
                if not isinstance(template, dict):
                    _add(findings, "R1V15-BUDGET-ORACLE", where, "missing exhaustionCompletion")
                    return None, None
                completion = copy.deepcopy(template)
                entries = _get(completion, ["exactCoverage", "entries"])
                matched = 0
                if isinstance(entries, list):
                    for entry in entries:
                        if isinstance(entry, dict) and entry.get("coverageKey") == coverage_key:
                            entry["state"] = "budget-exhausted"
                            matched += 1
                if matched != 1:
                    _add(
                        findings,
                        "R1V15-BUDGET-ORACLE",
                        where,
                        f"exhaustion coverageKey matched {matched} entries",
                    )
                break
            remaining[counter] -= 1
            usage[counter] += 1
            if remaining[counter] < 0 or usage[counter] > limits[counter]:
                _add(findings, "R1V15-BUDGET-ORACLE", where, "underflow or overflow")
            diagnostic_allowed = True
        elif kind == "diagnostic":
            _eq(
                findings,
                set(event),
                {"kind", "code", "message"},
                "R1V15-EVENT",
                ewhere,
            )
            if not diagnostic_allowed or diagnostic_used:
                _add(
                    findings,
                    "R1V15-DIAGNOSTICS-ORACLE",
                    ewhere,
                    "diagnostic not immediately paired with one successful charge",
                )
            code = event.get("code")
            message = event.get("message")
            candidate = {"ordinal": next_ordinal, "code": code, "message": message}
            if len(records) < capacity:
                records.append(candidate)
                usage["diagnosticRecordsAccepted"] += 1
            else:
                usage["diagnosticRecordsDropped"] += 1
            next_ordinal += 1
            diagnostic_used = True
            diagnostic_allowed = False
        elif kind == "return":
            _eq(findings, set(event), {"kind"}, "R1V15-EVENT", ewhere)
            if index != len(events) - 1:
                _add(findings, "R1V15-EVENT", ewhere, "return must be last")
            if returned:
                _add(findings, "R1V15-EVENT", ewhere, "duplicate return")
            returned = True
            template = vector.get("completionTemplate")
            if not isinstance(template, dict):
                _add(findings, "R1V15-VECTOR-MISSING", where, "missing completionTemplate")
                return None, None
            completion = copy.deepcopy(template)
        else:
            _add(findings, "R1V15-EVENT", ewhere, f"unknown kind {kind!r}")

    if not exhausted and not returned:
        _add(findings, "R1V15-EVENT", where, "no terminal return")
    if completion is None:
        return None, None
    completion["diagnostics"] = {"records": records, "droppedCount": usage["diagnosticRecordsDropped"]}
    completion["budgetUsage"] = usage
    if isinstance(types, dict) and "CoreCompletion" in types:
        _validate_value(completion, types["CoreCompletion"], types, f"{where}.completion", findings)

    variant = completion.get("variant")
    if variant == "incomplete":
        if _get(completion, ["policyOutcome", "verdict"]) != "indeterminate":
            _add(findings, "R1V15-COMPLETION", where, "incomplete policy must be indeterminate")
    if variant == "completed":
        entries = _get(completion, ["exactCoverage", "entries"], [])
        if isinstance(entries, list) and any(
            not isinstance(entry, dict) or entry.get("state") != "satisfied" for entry in entries
        ):
            _add(findings, "R1V15-COMPLETION", where, "completed Coverage not satisfied")

    expected = vector.get("expectedCompletion")
    if expected is not None and completion != expected:
        _add(findings, "R1V15-VECTOR-EXPECTED", where, "full completion mismatch")
    expected_diag = vector.get("expectedDiagnostics")
    if expected_diag is not None and completion.get("diagnostics") != expected_diag:
        _add(findings, "R1V15-DIAGNOSTICS-ORACLE", where, "diagnostics mismatch")
    expected_usage = vector.get("expectedUsage")
    if expected_usage is not None and completion.get("budgetUsage") != expected_usage:
        _add(findings, "R1V15-BUDGET-ORACLE", where, "budget usage mismatch")
    expected_variant = vector.get("expectedVariant")
    if expected_variant is not None and variant != expected_variant:
        _add(findings, "R1V15-VECTOR-EXPECTED", where, "variant mismatch")
    must_own = vector.get("mustOwn", [])
    if isinstance(must_own, list):
        for field in must_own:
            if field not in completion:
                _add(findings, "R1V15-OWNERSHIP", where, f"missing owned {field}")
    try:
        commitment = _projection_commitment(contract, completion)
    except Exception as exc:
        _add(findings, "R1V15-IDENTITY", where, f"projection failed: {exc}")
        commitment = None
    return completion, commitment


def _check_schema_definitions(contract: dict[str, Any], findings: list[dict[str, str]]) -> None:
    types = contract.get("closedTypes")
    if not isinstance(types, dict):
        _add(findings, "R1V15-SCHEMA-SPEC", "closedTypes", "must be object")
        return
    for name, fields in RECORD_FIELDS.items():
        spec = types.get(name)
        if not isinstance(spec, dict):
            _add(findings, "R1V15-SCHEMA-SPEC", f"closedTypes.{name}", "missing record")
            continue
        _eq(findings, spec.get("kind"), "record", "R1V15-SCHEMA-SPEC", name)
        _eq(findings, spec.get("fieldOrder"), fields, "R1V15-SCHEMA-SPEC", name)
        _eq(findings, spec.get("optionalFields"), [], "R1V15-SCHEMA-SPEC", name)
        _eq(findings, spec.get("additionalProperties"), False, "R1V15-SCHEMA-SPEC", name)
        field_specs = spec.get("fields")
        if not isinstance(field_specs, dict) or list(field_specs) != fields:
            _add(findings, "R1V15-SCHEMA-SPEC", name, "fields do not equal ordered closure")
    for name in ("Digest", "OpaqueId", "U64", "U128", "ExecutionId"):
        if not isinstance(types.get(name), dict):
            _add(findings, "R1V15-SCHEMA-SPEC", name, "missing primitive")
    _eq(
        findings,
        _get(types, ["U64", "maximum"]),
        18446744073709551615,
        "R1V15-SCHEMA-SPEC",
        "U64.maximum",
    )
    _eq(
        findings,
        _get(types, ["U128", "maximum"]),
        340282366920938463463374607431768211455,
        "R1V15-SCHEMA-SPEC",
        "U128.maximum",
    )
    _eq(
        findings,
        _get(types, ["FactDeficiency", "values"]),
        FACT_DEFICIENCIES,
        "R1V15-SCHEMA-SPEC",
        "FactDeficiency",
    )
    _eq(
        findings,
        _get(types, ["D9NormalizedFaultCause", "values"]),
        D9_CAUSES_WITH_NONE[1:],
        "R1V15-SCHEMA-SPEC",
        "D9NormalizedFaultCause",
    )
    union = types.get("CoreCompletion")
    if not isinstance(union, dict):
        _add(findings, "R1V15-SCHEMA-SPEC", "CoreCompletion", "missing union")
        return
    _eq(findings, union.get("kind"), "union", "R1V15-SCHEMA-SPEC", "CoreCompletion")
    _eq(findings, union.get("tag"), "variant", "R1V15-SCHEMA-SPEC", "CoreCompletion")
    _eq(
        findings,
        union.get("variantsInOrder"),
        list(COMPLETION_FIELDS),
        "R1V15-SCHEMA-SPEC",
        "CoreCompletion",
    )
    variants = union.get("variants")
    if not isinstance(variants, dict) or list(variants) != list(COMPLETION_FIELDS):
        _add(findings, "R1V15-SCHEMA-SPEC", "CoreCompletion", "variant set/order mismatch")
        return
    for variant, fields in COMPLETION_FIELDS.items():
        spec = variants.get(variant)
        if not isinstance(spec, dict):
            _add(findings, "R1V15-SCHEMA-SPEC", variant, "missing variant")
            continue
        _eq(findings, spec.get("fieldOrder"), fields, "R1V15-SCHEMA-SPEC", variant)
        _eq(findings, spec.get("optionalFields"), [], "R1V15-SCHEMA-SPEC", variant)
        _eq(findings, spec.get("additionalProperties"), False, "R1V15-SCHEMA-SPEC", variant)
        if not isinstance(spec.get("fields"), dict) or list(spec["fields"]) != fields:
            _add(findings, "R1V15-SCHEMA-SPEC", variant, "field specs not closed/ordered")


def _check_pin_declarations(contract: dict[str, Any], findings: list[dict[str, str]]) -> None:
    pins = contract.get("frozenInputs")
    if not isinstance(pins, list):
        _add(findings, "R1V15-PIN", "frozenInputs", "must be array")
        return
    actual_tuples = []
    for pin in pins:
        if not isinstance(pin, dict):
            _add(findings, "R1V15-PIN", "frozenInputs", "pin must be object")
            continue
        actual_tuples.append((pin.get("id"), pin.get("path"), pin.get("sha256")))
    _eq(findings, actual_tuples, EXPECTED_FROZEN_PINS, "R1V15-PIN", "frozenInputs")

    ext = contract.get("externalValueBindings")
    if not isinstance(ext, dict):
        _add(findings, "R1V15-PIN", "externalValueBindings", "must be object")
        return
    for label, binding, path_text, expected in (
        ("D9", ext.get("d9NormalizedCauses"), EXPECTED_D9_PATH, EXPECTED_D9_SHA),
        ("FACT", ext.get("factDeficiencies"), EXPECTED_FACT_PATH, EXPECTED_FACT_SHA),
    ):
        if not isinstance(binding, dict):
            _add(findings, "R1V15-PIN", label, "binding missing")
            continue
        _eq(findings, binding.get("sourcePath"), path_text, "R1V15-PIN", label)
        _eq(findings, binding.get("sourceSha256"), expected, "R1V15-PIN", label)


def _check_source_integrity(
    contract: dict[str, Any], findings: list[dict[str, str]]
) -> dict[str, Any]:
    sources: dict[str, Any] = {}
    _check_pin_declarations(contract, findings)

    for pin_id, path_text, expected in EXPECTED_FROZEN_PINS:
        path = _path(path_text)
        try:
            actual = _sha(path)
        except OSError as exc:
            _add(findings, "R1V15-PIN", pin_id, f"read failed: {exc}")
            continue
        if actual != expected:
            _add(findings, "R1V15-PIN", pin_id, f"sha256 {actual} != {expected}")
            continue
        try:
            if path.suffix == ".json":
                sources[pin_id] = strict_load(path)
            else:
                sources[pin_id] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError, StrictJsonError) as exc:
            _add(findings, "R1V15-PIN", pin_id, f"parse/read failed: {exc}")

    ext = contract.get("externalValueBindings")
    if not isinstance(ext, dict):
        return sources
    d9 = ext.get("d9NormalizedCauses")
    fp = ext.get("factDeficiencies")
    for label, binding, path_text, expected in (
        ("D9", d9, EXPECTED_D9_PATH, EXPECTED_D9_SHA),
        ("FACT", fp, EXPECTED_FACT_PATH, EXPECTED_FACT_SHA),
    ):
        if not isinstance(binding, dict):
            _add(findings, "R1V15-PIN", label, "binding missing")
            continue
        path = _path(path_text)
        try:
            actual = _sha(path)
            if actual != expected:
                _add(findings, "R1V15-PIN", label, f"sha256 {actual} != {expected}")
                continue
            sources[label] = pinned_json_load(path)
        except (OSError, StrictJsonError) as exc:
            _add(findings, "R1V15-PIN", label, f"read failed: {exc}")
    return sources


def _check_joins(
    contract: dict[str, Any], sources: dict[str, Any], findings: list[dict[str, str]]
) -> None:
    predecessor = sources.get("R1-V1_4")
    coordinator = sources.get("R1-FREEZE-COORDINATOR")
    phase3 = sources.get("PHASE3-V4-MANIFEST")
    phase3_review = sources.get("PHASE3-V4-INDEPENDENT-REVIEW")
    d9 = sources.get("D9")
    fact = sources.get("FACT")

    if isinstance(predecessor, dict):
        _eq(
            findings,
            _get(predecessor, ["initialTopology", "normativeFloor"]),
            "one-shot orchestration host + pure evaluation core",
            "R1V15-PREDECESSOR",
            "v1.4.initialTopology",
        )
        old_variants = _get(predecessor, ["coreCompletionSchema", "variants"])
        if isinstance(old_variants, list):
            old = {
                x.get("variant"): x.get("carries")
                for x in old_variants
                if isinstance(x, dict)
            }
            expected_old = {
                "completed": ["findings", "exactCoverage", "policyOutcome", "diagnosticsRef"],
                "incomplete": [
                    "partialFindings",
                    "exactCoverage",
                    "deficiency",
                    "policyOutcome",
                    "diagnosticsRef",
                ],
                "cancelled": ["exactCoverage", "diagnosticsRef"],
                "faulted": ["faultCause", "diagnosticsRef"],
            }
            _eq(findings, old, expected_old, "R1V15-PREDECESSOR", "v1.4 variants")
        else:
            _add(findings, "R1V15-PREDECESSOR", "v1.4 variants", "missing")
    if isinstance(coordinator, dict):
        _eq(
            findings,
            _get(coordinator, ["v1Architecture", "initialTopology"]),
            "one-shot Rust orchestration host + pure data-only evaluation core",
            "R1V15-PREDECESSOR",
            "coordinator.initialTopology",
        )
        if _get(coordinator, ["binding", "parks", "runtimeConfinement", "status"]) == "DISCHARGED":
            _add(findings, "R1V15-RUNTIME-HONESTY", "coordinator", "unexpected runtime discharge")

    if isinstance(phase3, dict):
        mapping = phase3.get("rustR1ApplicationMapping")
        if not isinstance(mapping, dict):
            _add(findings, "R1V15-PHASE3", "rustR1ApplicationMapping", "missing")
        else:
            _eq(findings, mapping.get("signature"), SIGNATURE, "R1V15-PHASE3", "signature")
            _eq(
                findings,
                _get(mapping, ["attemptMetadata", "requiredFields"]),
                ATTEMPT_FIELDS,
                "R1V15-PHASE3",
                "AttemptMetadata",
            )
            _eq(
                findings,
                _get(mapping, ["coreDeps", "requiredFields"]),
                CORE_DEPS_FIELDS,
                "R1V15-PHASE3",
                "CoreDeps",
            )
            _eq(
                findings,
                _get(mapping, ["coreCompletion", "returnsOnEveryVariant"]),
                ["bounded diagnostics data", "exact budget usage data"],
                "R1V15-PHASE3",
                "completion extras",
            )
            _eq(
                findings,
                _get(mapping, ["coreCompletion", "d9CauseValueOwner"]),
                "opensip-d9-values",
                "R1V15-PHASE3",
                "D9 owner",
            )
            _eq(
                findings,
                _get(mapping, ["coreCompletion", "mayDeriveHostTermination"]),
                False,
                "R1V15-PHASE3",
                "HostTermination",
            )
        packages = phase3.get("packages")
        core = None
        if isinstance(packages, list):
            core = next((p for p in packages if isinstance(p, dict) and p.get("id") == "opensip-core"), None)
        if not isinstance(core, dict):
            _add(findings, "R1V15-PHASE3", "opensip-core", "package missing")
        else:
            _eq(
                findings,
                _get(core, ["dependencies", "normal"]),
                ALLOWED_DEPS,
                "R1V15-PHASE3",
                "opensip-core.normal",
            )
            for cls in DEPENDENCY_CLASSES[1:]:
                _eq(
                    findings,
                    _get(core, ["dependencies", cls]),
                    [],
                    "R1V15-PHASE3",
                    f"opensip-core.{cls}",
                )
        ports = phase3.get("ports")
        r1_port = None
        if isinstance(ports, list):
            r1_port = next(
                (p for p in ports if isinstance(p, dict) and p.get("id") == "r1-rust-application-successor"),
                None,
            )
        if not isinstance(r1_port, dict):
            _add(findings, "R1V15-PHASE3", "R1 port", "missing")
        else:
            _eq(findings, r1_port.get("sourceManifest"), None, "R1V15-PHASE3", "port source")
            if "different-author independently reviewed R1 Rust application successor" not in str(
                r1_port.get("requiredSourceSelection")
            ):
                _add(findings, "R1V15-PHASE3", "port selection", "review gate missing")
    if not isinstance(phase3_review, str) or not phase3_review.startswith(
        "# Phase 3 implementer delta v4 — preliminary repair rereview\n\nStatus: **PASS"
    ):
        _add(findings, "R1V15-PHASE3", "v4 review", "frozen preliminary PASS not established")

    if isinstance(d9, dict):
        try:
            live = _pointer(d9, "/scenarioAxesSchema/properties/faultCause/enum")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            _add(findings, "R1V15-D9-OWNER", "D9 pointer", str(exc))
        else:
            _eq(findings, live, D9_CAUSES_WITH_NONE, "R1V15-D9-OWNER", "D9 cause enum")
            _eq(
                findings,
                _get(contract, ["externalValueBindings", "d9NormalizedCauses", "values"]),
                live,
                "R1V15-D9-OWNER",
                "candidate D9 values",
            )
    if isinstance(fact, dict):
        live = _get(fact, ["deficiencyVocabulary", "values"])
        _eq(findings, live, FACT_DEFICIENCIES, "R1V15-FACT-VOCAB", "fact-plane values")
        _eq(
            findings,
            _get(contract, ["externalValueBindings", "factDeficiencies", "values"]),
            live,
            "R1V15-FACT-VOCAB",
            "candidate fact values",
        )


def _check_core_contract(contract: dict[str, Any], findings: list[dict[str, str]]) -> None:
    _eq(findings, list(contract), TOP_LEVEL_KEYS, "R1V15-TOPLEVEL", "top-level order/closure")
    _eq(findings, contract.get("artifact"), "opensip.r1-lifetime-neutrality.conformance", "R1V15-TOPLEVEL", "artifact")
    _eq(findings, contract.get("version"), "v1.5", "R1V15-TOPLEVEL", "version")
    _eq(findings, contract.get("status"), "CANDIDATE-NOT-APPLIED", "R1V15-STATUS", "status")
    _eq(
        findings,
        contract.get("reviewStatus"),
        "AWAITING-INDEPENDENT-REVIEW",
        "R1V15-STATUS",
        "reviewStatus",
    )
    _eq(
        findings,
        contract.get("evidenceGrade"),
        "IMPLEMENTABLE_UNEXECUTED",
        "R1V15-STATUS",
        "evidenceGrade",
    )
    _eq(findings, _get(contract, ["rustApi", "signature"]), SIGNATURE, "R1V15-RUST-API", "signature")
    _eq(
        findings,
        _get(contract, ["rustApi", "signatureTokens", "argumentsInOrder"]),
        [
            "stageInput: &SealedStageInput",
            "deps: &CoreDeps",
            "attempt: &AttemptMetadata",
        ],
        "R1V15-RUST-API",
        "arguments",
    )
    output_ownership = _get(contract, ["rustApi", "outputOwnership"])
    if not isinstance(output_ownership, str) or "owns every transitive byte" not in output_ownership or "contains no borrow" not in output_ownership:
        _add(findings, "R1V15-OWNERSHIP", "rustApi.outputOwnership", "deep ownership not bound")
    _eq(
        findings,
        _get(contract, ["architectureInheritance", "residentHost", "permittedInV1"]),
        False,
        "R1V15-TOPOLOGY",
        "residentHost",
    )
    _eq(
        findings,
        _get(contract, ["architectureInheritance", "initialTopology"]),
        "one-shot Rust orchestration host + pure data-only evaluation core",
        "R1V15-TOPOLOGY",
        "initialTopology",
    )
    _eq(
        findings,
        _get(contract, ["staticAndRuntimeClosure", "runtimeDenial", "status"]),
        "NOT DISCHARGED",
        "R1V15-RUNTIME-HONESTY",
        "runtimeDenial",
    )
    _eq(
        findings,
        _get(contract, ["staticAndRuntimeClosure", "untrustedImperativeRules"]),
        "EXCLUDED until a restricted runtime and negative escape suite exist",
        "R1V15-RUNTIME-HONESTY",
        "untrusted rules",
    )
    _eq(
        findings,
        _get(contract, ["d9Boundary", "derivationOwner"]),
        "opensip-d9 in the host finalization boundary",
        "R1V15-D9-OWNER",
        "derivation owner",
    )
    _eq(
        findings,
        _get(contract, ["d9Boundary", "valueOwner"]),
        "opensip-d9-values",
        "R1V15-D9-OWNER",
        "value owner",
    )
    _eq(
        findings,
        _get(contract, ["staticAndRuntimeClosure", "allowedDirectDependencies"]),
        ALLOWED_DEPS,
        "R1V15-DEPENDENCY",
        "allowedDirectDependencies",
    )
    expected_classes = {cls: (ALLOWED_DEPS if cls == "normal" else []) for cls in DEPENDENCY_CLASSES}
    _eq(
        findings,
        _get(contract, ["staticAndRuntimeClosure", "allowedDependencyClasses"]),
        expected_classes,
        "R1V15-DEPENDENCY",
        "dependency classes",
    )
    projections = _get(contract, ["evidenceIdentity", "projectionByVariant"])
    expected_projection = {
        "completed": ["variant", "findings", "exactCoverage", "policyOutcome"],
        "incomplete": [
            "variant",
            "partialFindings",
            "exactCoverage",
            "deficiency",
            "policyOutcome",
        ],
        "cancelled": ["variant", "exactCoverage"],
        "faulted": ["variant", "faultCause"],
    }
    _eq(findings, projections, expected_projection, "R1V15-IDENTITY", "projectionByVariant")
    excluded = _get(contract, ["evidenceIdentity", "excluded"])
    _eq(
        findings,
        excluded,
        [
            "AttemptMetadata",
            "executionId",
            "diagnostics",
            "budgetUsage",
            "local remaining counters",
            "local diagnostics capacity",
        ],
        "R1V15-IDENTITY",
        "excluded fields",
    )
    _check_schema_definitions(contract, findings)


def _check_vectors(contract: dict[str, Any], findings: list[dict[str, str]]) -> None:
    vectors = _materialize_vectors(contract.get("positiveVectors"), findings)
    _eq(findings, len(vectors), 10, "R1V15-VECTORS", "positive count")
    commitments: dict[str, str] = {}
    completions: dict[str, dict[str, Any]] = {}
    for vector_id, vector in vectors.items():
        completion, commitment = _run_vector(contract, vector, findings)
        if completion is not None:
            completions[vector_id] = completion
        if commitment is not None:
            commitments[vector_id] = commitment
    for vector_id, vector in vectors.items():
        other = vector.get("expectProjectionEqualTo")
        if other is not None:
            if not isinstance(other, str) or other not in commitments or vector_id not in commitments:
                _add(findings, "R1V15-IDENTITY", vector_id, "equality target unavailable")
            elif commitments[vector_id] != commitments[other]:
                _add(findings, "R1V15-IDENTITY", vector_id, f"projection differs from {other}")
    variants = {completion.get("variant") for completion in completions.values()}
    _eq(findings, variants, set(COMPLETION_FIELDS), "R1V15-VECTORS", "variant coverage")


def _static_fixture_result(fixture: dict[str, Any], base: dict[str, Any]) -> str:
    if fixture.get("valid") is True:
        if fixture.get("dependencyClasses") == base.get("dependencyClasses"):
            return "ACCEPT-STATIC-ONLY"
        return "R1V15-DEPENDENCY"
    if fixture.get("addDependency") is not None:
        return "R1V15-DEPENDENCY"
    text = " ".join(str(v) for v in fixture.values()).lower()
    if any(token in text for token in ("std::fs", "std::net", "std::process")):
        return "R1V15-STATIC-AMBIENT"
    if any(token in text for token in ("refcell", "unsafecell", "mutex", "atomic")):
        return "R1V15-STATIC-MUTABILITY"
    if "dyn fn" in text or "callback" in text:
        return "R1V15-STATIC-COLLABORATOR"
    if "dlopen" in text or "ffi" in text:
        return "R1V15-BINARY-AMBIENT"
    return "R1V15-STATIC-UNCLASSIFIED"


def _check_static_fixtures(contract: dict[str, Any], findings: list[dict[str, str]]) -> None:
    fixtures = contract.get("staticClosureFixtures")
    if not isinstance(fixtures, list):
        _add(findings, "R1V15-STATIC", "staticClosureFixtures", "must be array")
        return
    _eq(findings, len(fixtures), 9, "R1V15-STATIC", "fixture count")
    ids = [f.get("id") for f in fixtures if isinstance(f, dict)]
    if len(ids) != len(set(ids)):
        _add(findings, "R1V15-STATIC", "staticClosureFixtures", "duplicate id")
    base = fixtures[0] if fixtures and isinstance(fixtures[0], dict) else {}
    expected_base = {cls: (ALLOWED_DEPS if cls == "normal" else []) for cls in DEPENDENCY_CLASSES}
    _eq(
        findings,
        base.get("dependencyClasses"),
        expected_base,
        "R1V15-DEPENDENCY",
        "static base dependency graph",
    )
    for index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            _add(findings, "R1V15-STATIC", f"fixture[{index}]", "not object")
            continue
        actual = _static_fixture_result(fixture, base)
        if actual != fixture.get("expected"):
            _add(
                findings,
                "R1V15-STATIC",
                str(fixture.get("id")),
                f"expected {fixture.get('expected')!r}, recomputed {actual!r}",
            )


def _codes(findings: list[dict[str, str]]) -> set[str]:
    return {f.get("code", "") for f in findings}


def _adversarial_probe(
    control_id: str,
    contract: dict[str, Any],
    vectors: dict[str, dict[str, Any]],
) -> set[str]:
    local: list[dict[str, str]] = []
    types = contract["closedTypes"]
    base = vectors["R1V15-POS-01-COMPLETED-NO-DIAGNOSTICS"]

    if control_id in {
        "R1V15-ADV-01-ATTEMPT-REQUEST-ID",
        "R1V15-ADV-02-ATTEMPT-UNKNOWN",
    }:
        value = copy.deepcopy(base["attempt"])
        value["requestId" if control_id.endswith("REQUEST-ID") else "futureAuthority"] = "x"
        _validate_value(value, types["AttemptMetadata"], types, control_id, local)
    elif control_id in {
        "R1V15-ADV-03-COREDEPS-RESOURCE-METER",
        "R1V15-ADV-04-COREDEPS-DIAGNOSTICS-SINK",
        "R1V15-ADV-05-COREDEPS-EFFECT-PORT",
        "R1V15-ADV-06-COREDEPS-TRAIT-OBJECT",
        "R1V15-ADV-07-COREDEPS-INTERIOR-MUTABILITY",
    }:
        field = {
            "R1V15-ADV-03-COREDEPS-RESOURCE-METER": "resourceMeter",
            "R1V15-ADV-04-COREDEPS-DIAGNOSTICS-SINK": "diagnosticsSink",
            "R1V15-ADV-05-COREDEPS-EFFECT-PORT": "effectPort",
            "R1V15-ADV-06-COREDEPS-TRAIT-OBJECT": "traitObject",
            "R1V15-ADV-07-COREDEPS-INTERIOR-MUTABILITY": "refCell",
        }[control_id]
        value = copy.deepcopy(base["deps"])
        value[field] = "forbidden"
        _validate_value(value, types["CoreDeps"], types, control_id, local)
    elif control_id == "R1V15-ADV-08-STAGE-UNKNOWN":
        value = copy.deepcopy(base["stageInput"])
        value["snapshotHandle"] = "forbidden"
        _validate_value(value, types["SealedStageInput"], types, control_id, local)
    elif control_id in {
        "R1V15-ADV-09-U64-OVERFLOW",
        "R1V15-ADV-10-U64-NEGATIVE",
        "R1V15-ADV-12-U64-BOOLEAN",
    }:
        value = copy.deepcopy(base["deps"]["budgetLimits"])
        if control_id.endswith("OVERFLOW"):
            value["ruleUnits"] = 18446744073709551616
        elif control_id.endswith("NEGATIVE"):
            value["policyUnits"] = -1
        else:
            value["ruleUnits"] = True
        _validate_value(value, types["BudgetLimits"], types, control_id, local)
    elif control_id == "R1V15-ADV-11-U64-FLOAT":
        try:
            strict_loads('{"diagnosticRecords":1.0}')
        except StrictJsonError as exc:
            _add(local, exc.code, control_id, str(exc))
    elif control_id in {"R1V15-ADV-13-UNSORTED-RULES", "R1V15-ADV-14-DUPLICATE-RULE"}:
        rule_a = {
            "ruleId": "rule:a",
            "artifactDigest": "sha256:" + "a" * 64,
        }
        rule_b = {
            "ruleId": "rule:b",
            "artifactDigest": "sha256:" + "b" * 64,
        }
        entries = [rule_b, rule_a] if control_id.endswith("UNSORTED-RULES") else [rule_a, copy.deepcopy(rule_a)]
        _validate_value({"entries": entries}, types["RuleSet"], types, control_id, local)
    elif control_id == "R1V15-ADV-15-UNKNOWN-COMPLETION-VARIANT":
        value = {"variant": "probably-fine"}
        _validate_value(value, types["CoreCompletion"], types, control_id, local)
    elif control_id in {
        "R1V15-ADV-16-CANCELLED-MISSING-DIAGNOSTICS",
        "R1V15-ADV-17-FAULTED-MISSING-BUDGET-USAGE",
        "R1V15-ADV-18-FAULTED-HOST-TERMINATION",
        "R1V15-ADV-19-DIAGNOSTIC-REORDER",
        "R1V15-ADV-20-DROPPED-COUNT-FALSE",
        "R1V15-ADV-21-BUDGET-USAGE-FALSE",
        "R1V15-ADV-22-BUDGET-WRAPS",
    }:
        source_id = {
            "R1V15-ADV-16-CANCELLED-MISSING-DIAGNOSTICS": "R1V15-POS-07-CANCELLED-OWNS-EXTRAS",
            "R1V15-ADV-17-FAULTED-MISSING-BUDGET-USAGE": "R1V15-POS-08-FAULTED-D9-VALUE-OWNS-EXTRAS",
            "R1V15-ADV-18-FAULTED-HOST-TERMINATION": "R1V15-POS-08-FAULTED-D9-VALUE-OWNS-EXTRAS",
            "R1V15-ADV-19-DIAGNOSTIC-REORDER": "R1V15-POS-02-COMPLETED-DIAGNOSTIC-BOUNDARY",
            "R1V15-ADV-20-DROPPED-COUNT-FALSE": "R1V15-POS-03-DIAGNOSTIC-TRUNCATION",
            "R1V15-ADV-21-BUDGET-USAGE-FALSE": "R1V15-POS-01-COMPLETED-NO-DIAGNOSTICS",
            "R1V15-ADV-22-BUDGET-WRAPS": "R1V15-POS-01-COMPLETED-NO-DIAGNOSTICS",
        }[control_id]
        clean_findings: list[dict[str, str]] = []
        completion, _ = _run_vector(contract, vectors[source_id], clean_findings)
        if completion is None or clean_findings:
            _add(local, "R1V15-ADVERSARIAL", control_id, "source vector not clean")
        else:
            mutated = copy.deepcopy(completion)
            expected_code = None
            if control_id.endswith("MISSING-DIAGNOSTICS"):
                del mutated["diagnostics"]
            elif control_id.endswith("MISSING-BUDGET-USAGE"):
                del mutated["budgetUsage"]
            elif control_id.endswith("HOST-TERMINATION"):
                mutated["HostTermination"] = "success"
            elif control_id.endswith("DIAGNOSTIC-REORDER"):
                mutated["diagnostics"]["records"].reverse()
                expected_code = "R1V15-DIAGNOSTICS-ORACLE"
            elif control_id.endswith("DROPPED-COUNT-FALSE"):
                mutated["diagnostics"]["droppedCount"] = 0
                expected_code = "R1V15-DIAGNOSTICS-ORACLE"
            elif control_id.endswith("BUDGET-USAGE-FALSE"):
                mutated["budgetUsage"]["ruleUnits"] = 0
                expected_code = "R1V15-BUDGET-ORACLE"
            else:
                mutated["budgetUsage"]["ruleUnits"] = 18446744073709551615
                expected_code = "R1V15-BUDGET-ORACLE"
            _validate_value(mutated, types["CoreCompletion"], types, control_id, local)
            if expected_code is not None and mutated != completion:
                _add(local, expected_code, control_id, "recomputed value differs from oracle")
    elif control_id in {
        "R1V15-ADV-23-EXECUTION-ID-IN-PROJECTION",
        "R1V15-ADV-24-DIAGNOSTICS-IN-PROJECTION",
        "R1V15-ADV-25-BY-VALUE-SIGNATURE",
        "R1V15-ADV-26-BORROWED-OUTPUT",
        "R1V15-ADV-27-RESIDENT-MODE",
        "R1V15-ADV-28-RUNTIME-DENIAL-PAPER-SEAL",
        "R1V15-ADV-29-D9-DERIVATION-IN-CORE",
        "R1V15-ADV-30-OUTPUT-ESCAPES",
    }:
        mutated = copy.deepcopy(contract)
        if control_id.endswith("EXECUTION-ID-IN-PROJECTION"):
            mutated["evidenceIdentity"]["projectionByVariant"]["completed"].append("executionId")
        elif control_id.endswith("DIAGNOSTICS-IN-PROJECTION"):
            mutated["evidenceIdentity"]["projectionByVariant"]["completed"].append("diagnostics")
        elif control_id.endswith("BY-VALUE-SIGNATURE"):
            mutated["rustApi"]["signature"] = SIGNATURE.replace("&", "")
        elif control_id.endswith("BORROWED-OUTPUT"):
            mutated["rustApi"]["signature"] = SIGNATURE.replace("CoreCompletion", "CoreCompletion<'a>")
        elif control_id.endswith("RESIDENT-MODE"):
            mutated["architectureInheritance"]["residentHost"]["permittedInV1"] = True
        elif control_id.endswith("PAPER-SEAL"):
            mutated["staticAndRuntimeClosure"]["runtimeDenial"]["status"] = "DISCHARGED"
        elif control_id.endswith("D9-DERIVATION-IN-CORE"):
            mutated["d9Boundary"]["derivationOwner"] = "opensip-core"
        else:
            mutated["rustApi"]["outputOwnership"] = "allow borrowed diagnostics handle"
        _check_core_contract(mutated, local)
    return _codes(local)


def _check_adversarial_controls(contract: dict[str, Any], findings: list[dict[str, str]]) -> None:
    controls = contract.get("adversarialControls")
    if not isinstance(controls, list):
        _add(findings, "R1V15-ADVERSARIAL", "adversarialControls", "must be array")
        return
    _eq(findings, len(controls), 30, "R1V15-ADVERSARIAL", "control count")
    ids = [x.get("id") for x in controls if isinstance(x, dict)]
    if len(ids) != len(set(ids)):
        _add(findings, "R1V15-ADVERSARIAL", "adversarialControls", "duplicate id")
    vectors = _materialize_vectors(contract.get("positiveVectors"), findings)
    for index, control in enumerate(controls):
        if not isinstance(control, dict):
            _add(findings, "R1V15-ADVERSARIAL", f"control[{index}]", "not object")
            continue
        control_id = control.get("id")
        expected = control.get("expectedFinding")
        if not isinstance(control_id, str) or not isinstance(expected, str):
            _add(findings, "R1V15-ADVERSARIAL", f"control[{index}]", "bad id/expected")
            continue
        try:
            codes = _adversarial_probe(control_id, contract, vectors)
        except Exception as exc:  # an exception is an escape, never a rejection
            _add(findings, "R1V15-ADVERSARIAL-ESCAPE", control_id, f"probe raised: {exc}")
            continue
        if expected not in codes:
            _add(
                findings,
                "R1V15-ADVERSARIAL-ESCAPE",
                control_id,
                f"expected {expected}; got {sorted(codes)}",
            )


def check_contract(contract: Any, *, verify_sources: bool = True) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    try:
        if not isinstance(contract, dict):
            _add(findings, "R1V15-TOPLEVEL-TYPE", "$", "contract must be object")
            return findings
        _check_core_contract(contract, findings)
        sources: dict[str, Any] = {}
        if verify_sources:
            sources = _check_source_integrity(contract, findings)
            _check_joins(contract, sources, findings)
        else:
            _check_pin_declarations(contract, findings)
        _check_vectors(contract, findings)
        _check_static_fixtures(contract, findings)
        _check_adversarial_controls(contract, findings)
    except Exception as exc:  # total checker boundary
        _add(findings, "R1V15-TOTALITY-EXCEPTION", "$", f"{type(exc).__name__}: {exc}")
    return findings


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _mutations() -> list[tuple[str, str, Callable[[dict[str, Any]], None]]]:
    def set_path(parts: list[Any], value: Any) -> Callable[[dict[str, Any]], None]:
        def apply(obj: dict[str, Any]) -> None:
            cur: Any = obj
            for part in parts[:-1]:
                cur = cur[part]
            cur[parts[-1]] = value
        return apply

    def delete_path(parts: list[Any]) -> Callable[[dict[str, Any]], None]:
        def apply(obj: dict[str, Any]) -> None:
            cur: Any = obj
            for part in parts[:-1]:
                cur = cur[part]
            del cur[parts[-1]]
        return apply

    def append_path(parts: list[Any], value: Any) -> Callable[[dict[str, Any]], None]:
        def apply(obj: dict[str, Any]) -> None:
            cur: Any = obj
            for part in parts:
                cur = cur[part]
            cur.append(value)
        return apply

    return [
        ("M01-status-applied", "R1V15-STATUS", set_path(["status"], "APPLIED")),
        ("M02-review-pass", "R1V15-STATUS", set_path(["reviewStatus"], "PASS")),
        ("M03-grade-demonstrated", "R1V15-STATUS", set_path(["evidenceGrade"], "DEMONSTRATED")),
        ("M04-pin-drift", "R1V15-PIN", set_path(["frozenInputs", 0, "sha256"], "0" * 64)),
        ("M05-pin-path", "R1V15-PIN", set_path(["frozenInputs", 3, "path"], "check-r1.pyc")),
        ("M06-signature-by-value", "R1V15-RUST-API", set_path(["rustApi", "signature"], SIGNATURE.replace("&", ""))),
        ("M07-argument-mut", "R1V15-RUST-API", set_path(["rustApi", "signatureTokens", "argumentsInOrder", 0], "stageInput: &mut SealedStageInput")),
        ("M08-output-borrow", "R1V15-OWNERSHIP", set_path(["rustApi", "outputOwnership"], "borrowed output")),
        ("M09-resident", "R1V15-TOPOLOGY", set_path(["architectureInheritance", "residentHost", "permittedInV1"], True)),
        ("M10-topology-daemon", "R1V15-TOPOLOGY", set_path(["architectureInheritance", "initialTopology"], "resident daemon")),
        ("M11-runtime-paper-seal", "R1V15-RUNTIME-HONESTY", set_path(["staticAndRuntimeClosure", "runtimeDenial", "status"], "DISCHARGED")),
        ("M12-untrusted-rules", "R1V15-RUNTIME-HONESTY", set_path(["staticAndRuntimeClosure", "untrustedImperativeRules"], "INCLUDED")),
        ("M13-attempt-requestid", "R1V15-SCHEMA-SPEC", append_path(["closedTypes", "AttemptMetadata", "fieldOrder"], "requestId")),
        ("M14-attempt-optional", "R1V15-SCHEMA-SPEC", append_path(["closedTypes", "AttemptMetadata", "optionalFields"], "requestId")),
        ("M15-coredeps-meter", "R1V15-SCHEMA-SPEC", append_path(["closedTypes", "CoreDeps", "fieldOrder"], "resourceMeter")),
        ("M16-coredeps-open", "R1V15-SCHEMA-SPEC", set_path(["closedTypes", "CoreDeps", "additionalProperties"], True)),
        ("M17-u64-over", "R1V15-SCHEMA-SPEC", set_path(["closedTypes", "U64", "maximum"], 18446744073709551616)),
        ("M18-u128-under", "R1V15-SCHEMA-SPEC", set_path(["closedTypes", "U128", "maximum"], 18446744073709551615)),
        ("M19-drop-completed-budget", "R1V15-SCHEMA-SPEC", delete_path(["closedTypes", "CoreCompletion", "variants", "completed", "fields", "budgetUsage"])),
        ("M20-drop-cancelled-diagnostics", "R1V15-SCHEMA-SPEC", delete_path(["closedTypes", "CoreCompletion", "variants", "cancelled", "fields", "diagnostics"])),
        ("M21-new-variant", "R1V15-SCHEMA-SPEC", append_path(["closedTypes", "CoreCompletion", "variantsInOrder"], "partial")),
        ("M22-fact-vocab", "R1V15-SCHEMA-SPEC", append_path(["closedTypes", "FactDeficiency", "values"], "unknown")),
        ("M23-d9-vocab", "R1V15-SCHEMA-SPEC", append_path(["closedTypes", "D9NormalizedFaultCause", "values"], "panic")),
        ("M24-d9-owner", "R1V15-D9-OWNER", set_path(["d9Boundary", "derivationOwner"], "opensip-core")),
        ("M25-d9-value-owner", "R1V15-D9-OWNER", set_path(["d9Boundary", "valueOwner"], "opensip-d9")),
        ("M26-identity-execution", "R1V15-IDENTITY", append_path(["evidenceIdentity", "projectionByVariant", "completed"], "executionId")),
        ("M27-identity-diagnostics", "R1V15-IDENTITY", append_path(["evidenceIdentity", "projectionByVariant", "completed"], "diagnostics")),
        ("M28-identity-unexclude", "R1V15-IDENTITY", set_path(["evidenceIdentity", "excluded", 1], "requestId")),
        ("M29-dependency-extra", "R1V15-DEPENDENCY", append_path(["staticAndRuntimeClosure", "allowedDirectDependencies"], "tokio")),
        ("M30-dependency-build", "R1V15-DEPENDENCY", append_path(["staticAndRuntimeClosure", "allowedDependencyClasses", "build"], "cc")),
        ("M31-positive-count", "R1V15-VECTORS", delete_path(["positiveVectors", 9])),
        ("M32-vector-usage", "R1V15-VECTOR-EXPECTED", set_path(["positiveVectors", 0, "expectedCompletion", "budgetUsage", "ruleUnits"], 0)),
        ("M33-vector-dropped", "R1V15-DIAGNOSTICS-ORACLE", set_path(["positiveVectors", 2, "expectedDiagnostics", "droppedCount"], 0)),
        ("M34-vector-execution-leak", "R1V15-IDENTITY", set_path(["positiveVectors", 8, "expectProjectionEqualTo"], "R1V15-POS-06-INCOMPLETE-FACT-DEFICIENCY")),
        ("M35-vector-bad-counter", "R1V15-EVENT", set_path(["positiveVectors", 0, "events", 0, "counter"], "wallClock")),
        ("M36-adversarial-count", "R1V15-ADVERSARIAL", delete_path(["adversarialControls", 29])),
        ("M37-adversarial-expect", "R1V15-ADVERSARIAL-ESCAPE", set_path(["adversarialControls", 0, "expectedFinding"], "NOPE")),
        ("M38-static-count", "R1V15-STATIC", delete_path(["staticClosureFixtures", 8])),
        ("M39-static-graph", "R1V15-DEPENDENCY", append_path(["staticClosureFixtures", 0, "dependencyClasses", "normal"], "std")),
        ("M40-top-level-extra", "R1V15-TOPLEVEL", set_path([], None)),
    ]


def _apply_special_mutation(
    mutation_id: str, fn: Callable[[dict[str, Any]], None], value: dict[str, Any]
) -> None:
    if mutation_id == "M40-top-level-extra":
        value["producerSaysValid"] = True
    else:
        fn(value)


def run_selftest(contract: dict[str, Any], original_bytes: bytes) -> tuple[bool, list[str]]:
    messages: list[str] = []
    base_findings = check_contract(contract)
    if base_findings:
        return False, ["BASE-DIRTY: normal check has findings; refusing mutation suite"]
    mutations = _mutations()
    ids = [item[0] for item in mutations]
    if len(ids) != len(set(ids)):
        return False, ["SELFTEST-ESCAPE: duplicate mutation id"]
    applied: list[str] = []
    for mutation_id, expected_code, fn in mutations:
        candidate = copy.deepcopy(contract)
        before = _canonical(candidate)
        try:
            _apply_special_mutation(mutation_id, fn, candidate)
        except Exception as exc:
            messages.append(f"SELFTEST-ESCAPE {mutation_id}: failed to apply: {exc}")
            continue
        after = _canonical(candidate)
        if before == after:
            messages.append(f"SELFTEST-ESCAPE {mutation_id}: no-op")
            continue
        applied.append(mutation_id)
        result = check_contract(candidate, verify_sources=False)
        result_codes = _codes(result)
        if not result:
            messages.append(f"SELFTEST-ESCAPE {mutation_id}: mutation passed")
        elif expected_code not in result_codes:
            messages.append(
                f"SELFTEST-ESCAPE {mutation_id}: expected {expected_code}; got {sorted(result_codes)}"
            )
    if applied != ids:
        messages.append("SELFTEST-ESCAPE: skipped or out-of-order mutation")

    parser_cases = [
        ("duplicate-top", '{"a":1,"a":2}', "R1V15-JSON-DUPLICATE"),
        ("duplicate-nested", '{"a":{"b":1,"b":2}}', "R1V15-JSON-DUPLICATE"),
        ("nan", '{"a":NaN}', "R1V15-JSON-NONFINITE"),
        ("infinity", '{"a":Infinity}', "R1V15-JSON-NONFINITE"),
        ("negative-infinity", '{"a":-Infinity}', "R1V15-JSON-NONFINITE"),
        ("decimal", '{"a":1.0}', "R1V15-JSON-FLOAT"),
        ("exponent", '{"a":1e0}', "R1V15-JSON-FLOAT"),
    ]
    for case_id, raw, expected in parser_cases:
        try:
            strict_loads(raw)
        except StrictJsonError as exc:
            if exc.code != expected:
                messages.append(f"SELFTEST-ESCAPE parser {case_id}: {exc.code} != {expected}")
        else:
            messages.append(f"SELFTEST-ESCAPE parser {case_id}: accepted")

    hostile = [
        None,
        True,
        0,
        "contract",
        [],
        {"artifact": None},
        {"closedTypes": []},
        {"positiveVectors": [None]},
        {"staticClosureFixtures": "x"},
        {"adversarialControls": [1]},
    ]
    for index, value in enumerate(hostile):
        try:
            result = check_contract(value, verify_sources=False)
        except Exception as exc:
            messages.append(f"SELFTEST-ESCAPE totality[{index}]: raised {exc}")
            continue
        if not result:
            messages.append(f"SELFTEST-ESCAPE totality[{index}]: no finding")

    try:
        final_bytes = CONTRACT_PATH.read_bytes()
    except OSError as exc:
        messages.append(f"SELFTEST-ESCAPE: cannot reread live contract: {exc}")
    else:
        if final_bytes != original_bytes:
            messages.append("SELFTEST-ESCAPE: live contract changed during selftest")
    return not messages, messages


def _print_findings(findings: list[dict[str, str]]) -> None:
    for item in findings:
        print(f"{item['code']} {item['where']}: {item['detail']}")


def main(argv: list[str]) -> int:
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        print("R1V15-INVOKE: refuse; run with python3 -I -B")
        return 2
    if argv not in ([], ["--selftest"]):
        print("usage: python3 -I -B docs/coop/artifacts/check-r1-v1.5.py [--selftest]")
        return 2
    try:
        original_bytes = CONTRACT_PATH.read_bytes()
        contract = strict_loads(original_bytes.decode("utf-8"))
    except (OSError, UnicodeError, StrictJsonError) as exc:
        print(f"R1V15-JSON: {exc}")
        return 1
    findings = check_contract(contract)
    if findings:
        _print_findings(findings)
        print(f"R1 v1.5 contract: FAIL ({len(findings)} findings)")
        return 1
    if argv == ["--selftest"]:
        ok, messages = run_selftest(contract, original_bytes)
        if not ok:
            for message in messages:
                print(message)
            print(f"R1 v1.5 selftest: FAIL ({len(messages)} escapes)")
            return 1
        print("R1 v1.5 selftest: PASS (40 mutations, 7 raw parser probes, 10 hostile totality shapes)")
        return 0
    print(
        "R1 v1.5 contract: PASS "
        "(10 positive vectors, 30 adversarial controls, 9 static-closure fixtures, "
        "4 completion variants; IMPLEMENTABLE_UNEXECUTED)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
