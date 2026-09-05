#!/usr/bin/env python3
"""Validate the NOT-APPLIED OPERABILITY v9 oracle/startup successor.

Sole conformance commands, from the repository root:
  python3 -I -B docs/coop/artifacts/check-operability-v9.py
  python3 -I -B docs/coop/artifacts/check-operability-v9.py --selftest

The checker itself must be authenticated externally.  The interpreter,
built-in/frozen modules, standard library, OS file/process primitives, and this
early isolated-mode diagnostic are the verifier-runtime TCB.  A non-isolated
refusal is diagnostic and cannot retroactively prevent startup activity.
"""
from __future__ import annotations

import sys


if sys.flags.isolated != 1:
    sys.stdout.write(
        '{"schemaVersion":1,"kind":"unsupported-mode","status":"UNSUPPORTED",'
        '"code":"OP9-UNSUPPORTED-NONISOLATED",'
        '"detail":"isolated Python startup is required"}\n')
    raise SystemExit(3)


import copy
import collections
import hashlib
import json
import math
import os
import pathlib
import py_compile
import re
import subprocess
import tempfile
import types
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v9.json"
PINS = {
    "operability.v8.json": "7818600b0b80df3cd4541335e570f1880ad48064644fdb1d2cc66e2707912b6e",
    "check-operability-v8.py": "dace5afdde6df4404b0ce4fd0841c3444ad93af813d79c24b64f3b38525c56b2",
    "operability.v8.review-independent-prefreeze.json": "7bca764684f50c5f486015c409c7ea91ef03a37648307dfbb156257be8dddf6a",
    "operability.v7.json": "30d038363e94dc84766c43d3c28bf9a4e9fa7701fcb76a3ead942a210533eebd",
    "check-operability-v7.py": "6e7163871087be56e2d89e1911992870097f966fd2a7d728ab3d84ca06bf1832",
    "operability.v7.review-independent-prefreeze.json": "194e92128886fc8f11a1b513f597b79a91647732bb5a04772503379c228d10a4",
    "operability.v6.json": "12d9f072c25a3efb789a05a1c513dfbc2aaf6612a234b23a8cf82ae027d9acb3",
    "check-operability-v6.py": "2bd5e41d128388f50bb3d1518eb8e460d6987518dd71dcc350a7bc202b7407bd",
    "operability.v6.review-independent-prefreeze.json": "c34d304245a0dc932aae24d8b4283da6e7691bff45b4eb5e3b8ede9ab2c24ad7",
    "operability.v5.json": "89a18ffde1df3255b6a766aa74d1ad496ee3c7ed09cf5d69aa0ef34451699d8f",
    "check-operability-v5.py": "047afb978bc02b62402e4036bb42659a7ac14d427408ef06d59d8a8d7438ef70",
    "operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
}
EXECUTABLE_DEPENDENCIES = {
    "check-operability-v8.py": "op8_rejected_verified_for_op9",
    "check-operability-v7.py": "op7_rejected_verified_for_op9",
    "check-operability-v6.py": "op6_rejected_verified_for_op9",
    "check-operability-v5.py": "op5_verified_for_op9",
    "check-operability.py": "op2_verified_for_op9",
}
ROOT_ENVELOPE = ("version", "status", "supersedes", "author", "reviewStatus")
V8_REVIEW_FINDINGS = (
    "OP8-IR-01-EXACT-CODE-ORACLE",
    "OP8-IR-02-DECLARED-STARTUP-BOUNDARY",
)
V7_REVIEW_FINDINGS = (
    "OP7-IR-01-NUMERIC-PARSER-TOTALITY",
    "OP7-IR-02-VALIDATION-ORDER",
)
V6_REVIEW_FINDING = "OP6-IR-01-MALFORMED-TOTALITY"

MAX_RAW_BYTES = 2_000_000
MAX_DEPTH = 64
MAX_NODES = 100_000
MAX_ARRAY_ITEMS = 10_000
MAX_OBJECT_MEMBERS = 10_000
MAX_STRING_UTF8_BYTES = 1_048_576
MAX_INTEGER_DIGITS = 4_300
MAX_FLOAT_SIGNIFICAND_DIGITS = 4_300
MAX_EXPONENT_DIGITS = 4
MAX_ABS_EXPONENT = 4_300
INTEGER_ABS_LIMIT = 10 ** MAX_INTEGER_DIGITS

INTEGER_TOKEN_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)$")
FLOAT_TOKEN_RE = re.compile(
    r"^(?P<sign>-)?(?P<integer>0|[1-9][0-9]*)"
    r"(?:\.(?P<fraction>[0-9]+))?"
    r"(?:[eE](?P<exponent_sign>[+-])?(?P<exponent>[0-9]+))?$"
)
FIXTURE_KINDS = ("event-envelope", "phase-plane-bindings")
CODE_RE = re.compile(r"^[A-Z][A-Z0-9-]*$")
FORBIDDEN_OUTCOME_TOKENS = (
    "internal", "exception", "traceback", "typeerror", "outward-exception",
)
MACHINE_RESULT_KEYS = {
    "schemaVersion", "kind", "status", "artifactSha256", "findings",
    "selftestCounts",
}
SELFTEST_COUNT_KEYS = {
    "targeted", "heterogeneous", "parser", "api", "cli", "oracleInjected",
    "oracleRejected", "oracleMutantsKilled", "isolation", "trust",
    "mutationEscape",
}
FINDING_RECORD_KEYS = {"code", "detail"}
V9_METADATA_SHA256 = "61b01c0bb4fbc28f4fa06e51d33735e714dbef16206672c97d63cfcd0e72be81"

V9_ROOT = {
    "version": 9,
    "status": "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REREVIEW (exact-code-oracle and isolated-startup-boundary successor over frozen/rejected v8; EventEnvelopeV3 and numeric/shape semantics unchanged)",
    "supersedes": {
        "artifact": "operability.v8.json",
        "sha256": PINS["operability.v8.json"],
        "checker": "check-operability-v8.py",
        "checkerSha256": PINS["check-operability-v8.py"],
    },
    "author": "agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane; EventEnvelopeV3 binding successor by operability-v6 lane; totality-only successor by operability-v7 lane; deterministic numeric-totality successor by operability-v8 lane; oracle/startup-boundary successor by the author of the v8 independent rejection review",
    "reviewStatus": "OPERABILITY v8 exact bytes were independently REJECTED for OP8-IR-01-EXACT-CODE-ORACLE and OP8-IR-02-DECLARED-STARTUP-BOUNDARY. OPERABILITY v9 preserves the complete v8 artifact, inherited EventEnvelopeV3 lifecycle, store-provenance content, numeric-token policy, fixture validation, predecessor metadata, and non-promotion states exactly, and adds only closed structural-oracle/startup declarations, exact rejection binding, successor metadata, and checker mechanics/tests. The v9 author also authored the v8 rejection review and has no authority to approve v9; a different independent reviewer is required. v9 is NOT-APPLIED and awaits independent rereview; no product, integration, application, acceptance, freeze, seal, or release authority is claimed.",
}

class ControlledInputError(ValueError):
    """An untrusted input deterministically violated one named parser bound."""

    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail


def _input_error(code: str, detail: str) -> ControlledInputError:
    return ControlledInputError(code, detail)


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _input_error("OP8-JSON-DUPLICATE", "duplicate object member")
        result[key] = value
    return result


def _decimal_digits_to_int(digits: str) -> int:
    """Convert already-bounded ASCII digits without ambient full-token int()."""
    value = 0
    first = len(digits) % 9
    offset = 0
    if first:
        value = int(digits[:first])
        offset = first
    while offset < len(digits):
        value = value * 1_000_000_000 + int(digits[offset:offset + 9])
        offset += 9
    return value


def _parse_int_token(token: str) -> int:
    if INTEGER_TOKEN_RE.fullmatch(token) is None:
        raise _input_error("OP8-NUMERIC-GRAMMAR", "invalid integer token")
    digits = token[1:] if token.startswith("-") else token
    if len(digits) > MAX_INTEGER_DIGITS:
        raise _input_error(
            "OP8-NUMERIC-INTEGER-DIGITS",
            f"integer token exceeds {MAX_INTEGER_DIGITS} decimal digits",
        )
    value = _decimal_digits_to_int(digits)
    return -value if token.startswith("-") else value


def _parse_float_token(token: str) -> float:
    match = FLOAT_TOKEN_RE.fullmatch(token)
    if match is None or (
            match.group("fraction") is None and match.group("exponent") is None):
        raise _input_error("OP8-NUMERIC-GRAMMAR", "invalid float/exponent token")
    significand_digits = len(match.group("integer")) + len(
        match.group("fraction") or "")
    if significand_digits > MAX_FLOAT_SIGNIFICAND_DIGITS:
        raise _input_error(
            "OP8-NUMERIC-FLOAT-DIGITS",
            "float significand exceeds 4300 decimal digits",
        )
    exponent_digits = match.group("exponent")
    if exponent_digits is not None:
        if len(exponent_digits) > MAX_EXPONENT_DIGITS:
            raise _input_error(
                "OP8-NUMERIC-EXPONENT",
                "exponent exceeds 4 decimal digits",
            )
        exponent = _decimal_digits_to_int(exponent_digits)
        if exponent > MAX_ABS_EXPONENT:
            raise _input_error(
                "OP8-NUMERIC-EXPONENT",
                "absolute exponent exceeds 4300",
            )
    try:
        value = float(token)
    except (OverflowError, ValueError):
        raise _input_error(
            "OP8-NUMERIC-NONFINITE", "float token has no finite binary64 value") from None
    if not math.isfinite(value):
        raise _input_error(
            "OP8-NUMERIC-NONFINITE", "float token has no finite binary64 value")
    return value


def _parse_constant_token(token: str) -> Any:
    del token
    raise _input_error(
        "OP8-NUMERIC-CONSTANT", "nonstandard nonfinite numeric constant is forbidden")


def _short_path(parent: str, child: str | int) -> str:
    if type(child) is int:
        return f"{parent}[{child}]"
    safe = child if len(child) <= 48 else child[:45] + "..."
    return f"{parent}.{safe}"


def _utf8_size(value: str, path: str) -> tuple[int | None, list[str]]:
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        return None, [f"OP8-TOTALITY-UNICODE: non-scalar Unicode string at {path}"]
    return len(encoded), []


def json_value_findings(value: Any) -> list[str]:
    """Iteratively prove a bounded finite built-in JSON tree before consumers."""
    stack: list[tuple[Any, int, str]] = [(value, 0, "$")]
    seen_containers: set[int] = set()
    findings: list[str] = []
    nodes = 0
    while stack:
        current, depth, path = stack.pop()
        nodes += 1
        if nodes > MAX_NODES:
            return [f"OP8-LIMIT-NODES: node count exceeds {MAX_NODES}"]
        if depth > MAX_DEPTH:
            findings.append(f"OP8-LIMIT-DEPTH: depth exceeds {MAX_DEPTH} at {path}")
            continue
        if type(current) is dict:
            identity = id(current)
            if identity in seen_containers:
                findings.append(f"OP8-TOTALITY-NONTREE: repeated/cyclic object at {path}")
                continue
            seen_containers.add(identity)
            if len(current) > MAX_OBJECT_MEMBERS:
                findings.append(
                    f"OP8-LIMIT-OBJECT: object exceeds {MAX_OBJECT_MEMBERS} members at {path}")
                continue
            for key, child in current.items():
                if type(key) is not str:
                    findings.append(f"OP8-TOTALITY-KEY: non-string object key at {path}")
                    child_path = f"{path}.<non-string-key>"
                else:
                    key_size, key_errors = _utf8_size(key, path)
                    findings.extend(key_errors)
                    if key_size is not None and key_size > MAX_STRING_UTF8_BYTES:
                        findings.append(f"OP8-LIMIT-STRING: object key too large at {path}")
                    child_path = _short_path(path, key)
                stack.append((child, depth + 1, child_path))
        elif type(current) is list:
            identity = id(current)
            if identity in seen_containers:
                findings.append(f"OP8-TOTALITY-NONTREE: repeated/cyclic array at {path}")
                continue
            seen_containers.add(identity)
            if len(current) > MAX_ARRAY_ITEMS:
                findings.append(
                    f"OP8-LIMIT-ARRAY: array exceeds {MAX_ARRAY_ITEMS} items at {path}")
                continue
            for index, child in enumerate(current):
                stack.append((child, depth + 1, _short_path(path, index)))
        elif type(current) is str:
            size, errors = _utf8_size(current, path)
            findings.extend(errors)
            if size is not None and size > MAX_STRING_UTF8_BYTES:
                findings.append(f"OP8-LIMIT-STRING: string too large at {path}")
        elif current is None or type(current) is bool:
            pass
        elif type(current) is int:
            if current >= INTEGER_ABS_LIMIT or current <= -INTEGER_ABS_LIMIT:
                findings.append(
                    f"OP8-NUMERIC-INTEGER-DIGITS: integer exceeds {MAX_INTEGER_DIGITS} decimal digits at {path}")
        elif type(current) is float:
            if not math.isfinite(current):
                findings.append(f"OP8-NUMERIC-NONFINITE: nonfinite number at {path}")
        else:
            findings.append(
                f"OP8-TOTALITY-NONJSON: {type(current).__name__} is not a JSON value at {path}")
    return findings


def strict_loads(raw: bytes) -> Any:
    if len(raw) > MAX_RAW_BYTES:
        raise _input_error(
            "OP8-LIMIT-RAW", f"raw JSON exceeds {MAX_RAW_BYTES} bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise _input_error("OP8-JSON-UTF8", "input is not valid UTF-8") from None
    try:
        value = json.loads(
            text,
            object_pairs_hook=_closed_object,
            parse_int=_parse_int_token,
            parse_float=_parse_float_token,
            parse_constant=_parse_constant_token,
        )
    except ControlledInputError:
        raise
    except json.JSONDecodeError as exc:
        raise _input_error(
            "OP8-JSON-SYNTAX",
            f"invalid JSON at line {exc.lineno} column {exc.colno}",
        ) from None
    except RecursionError:
        raise _input_error(
            "OP8-LIMIT-DEPTH", f"JSON nesting exceeds {MAX_DEPTH}") from None
    findings = json_value_findings(value)
    if findings:
        code, _, detail = findings[0].partition(": ")
        raise _input_error(code, detail)
    return value


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _compile_verified(raw: bytes, filename: str, module_name: str) -> Any:
    """Compile only the already authenticated buffer; never import disk/cache."""
    module = types.ModuleType(module_name)
    module.__file__ = str(HERE / filename)
    module.__package__ = None
    code = compile(raw, module.__file__, "exec", dont_inherit=True)
    exec(code, module.__dict__)
    return module


def _exact_string_array(value: Any, expected: tuple[str, ...]) -> bool:
    if type(value) is not list or len(value) != len(expected):
        return False
    for index, item in enumerate(value):
        if type(item) is not str or item != expected[index]:
            return False
    return True


def _review_bindings_valid(v7_review: Any, v6_review: Any) -> bool:
    if type(v7_review) is not dict or type(v6_review) is not dict:
        return False
    v7_verdict = v7_review.get("verdict")
    v7_binding = v7_review.get("reviewBinding")
    if type(v7_verdict) is not dict or type(v7_binding) is not dict:
        return False
    if v7_verdict.get("decision") != "REJECT" or not _exact_string_array(
            v7_verdict.get("blockingFindingIds"), V7_REVIEW_FINDINGS):
        return False
    candidate = v7_binding.get("candidate")
    checker = v7_binding.get("candidateChecker")
    if type(candidate) is not dict or type(checker) is not dict:
        return False
    if candidate.get("path") != "docs/coop/artifacts/operability.v7.json" or \
            candidate.get("sha256") != PINS["operability.v7.json"] or \
            checker.get("path") != "docs/coop/artifacts/check-operability-v7.py" or \
            checker.get("sha256") != PINS["check-operability-v7.py"]:
        return False
    v6_verdict = v6_review.get("verdict")
    if type(v6_verdict) is not dict or v6_verdict.get("decision") != "REJECT":
        return False
    v6_ids = v6_verdict.get("blockingFindingIds")
    return type(v6_ids) is list and len(v6_ids) == 1 and \
        type(v6_ids[0]) is str and v6_ids[0] == V6_REVIEW_FINDING


def _v9_review_bindings_valid(v8_review: Any, v7_review: Any,
                              v6_review: Any) -> bool:
    if type(v8_review) is not dict or type(v7_review) is not dict or \
            type(v6_review) is not dict:
        return False
    verdict = v8_review.get("verdict")
    binding = v8_review.get("reviewBinding")
    if type(verdict) is not dict or type(binding) is not dict:
        return False
    if verdict.get("decision") != "REJECT" or not _exact_string_array(
            verdict.get("blockingFindingIds"), V8_REVIEW_FINDINGS):
        return False
    candidate = binding.get("candidate")
    checker = binding.get("candidateChecker")
    if type(candidate) is not dict or type(checker) is not dict:
        return False
    if candidate.get("path") != "docs/coop/artifacts/operability.v8.json" or \
            candidate.get("sha256") != PINS["operability.v8.json"] or \
            checker.get("path") != "docs/coop/artifacts/check-operability-v8.py" or \
            checker.get("sha256") != PINS["check-operability-v8.py"]:
        return False
    return _review_bindings_valid(v7_review, v6_review)


def authenticated_context() -> tuple[dict[str, Any] | None, list[str]]:
    """Authenticate all thirteen lineage bytes before dependency execution."""
    errors: list[str] = []
    buffers: dict[str, bytes] = {}
    for name, expected in PINS.items():
        try:
            raw = (HERE / name).read_bytes()
        except OSError:
            errors.append(f"OP9-DEP-READ: cannot read {name}")
            continue
        buffers[name] = raw
        actual = _digest(raw)
        if actual != expected:
            errors.append(f"OP9-DEP-HASH: {name} hash {actual} != {expected}")
    if errors or tuple(buffers) != tuple(PINS):
        return None, errors or [
            "OP9-DEP-CLOSURE: dependency closure is incomplete"]

    data_names = (
        "operability.v8.json",
        "operability.v8.review-independent-prefreeze.json",
        "operability.v7.json",
        "operability.v7.review-independent-prefreeze.json",
        "operability.v6.json",
        "operability.v6.review-independent-prefreeze.json",
        "operability.v5.json",
        "operability.v2.json",
    )
    parsed: dict[str, Any] = {}
    for name in data_names:
        try:
            parsed[name] = strict_loads(buffers[name])
        except ControlledInputError as exc:
            errors.append(f"OP9-DEP-PARSE: {name}: {exc.code}")
    if errors:
        return None, errors

    v8_review = parsed["operability.v8.review-independent-prefreeze.json"]
    v7_review = parsed["operability.v7.review-independent-prefreeze.json"]
    v6_review = parsed["operability.v6.review-independent-prefreeze.json"]
    if not _v9_review_bindings_valid(v8_review, v7_review, v6_review):
        return None, [
            "OP9-REVIEW: exact v8/v7/v6 rejection binding is not closed"]

    modules: dict[str, Any] = {}
    for filename, module_name in EXECUTABLE_DEPENDENCIES.items():
        modules[filename] = _compile_verified(
            buffers[filename], filename, module_name)

    v8mod = modules["check-operability-v8.py"]
    v7mod = modules["check-operability-v7.py"]
    v6mod = modules["check-operability-v6.py"]
    v5mod = modules["check-operability-v5.py"]
    v2mod = modules["check-operability.py"]
    for label, module, binding in (
            ("OP8", v8mod, "operability.v8.json"),
            ("OP7", v7mod, "operability.v7.json"),
            ("OP6", v6mod, "operability.v6.json"),
            ("OP5", v5mod, "operability.v5.json"),
            ("OP2", v2mod, "operability.v2.json")):
        if getattr(module, "BINDING", None) != binding or \
                not callable(getattr(module, "check", None)):
            errors.append(
                f"OP9-DEP-SURFACE: verified {label} checker is incomplete")
    if not callable(getattr(v8mod, "project_v7", None)) or \
            not callable(getattr(v7mod, "project_v6", None)) or \
            not callable(getattr(v6mod, "project_v5", None)) or \
            not callable(getattr(v5mod, "project_op2", None)):
        errors.append(
            "OP9-DEP-SURFACE: predecessor projection chain is incomplete")
    if errors:
        return None, errors

    v8 = parsed["operability.v8.json"]
    v7 = parsed["operability.v7.json"]
    v6 = parsed["operability.v6.json"]
    v5 = parsed["operability.v5.json"]
    v2 = parsed["operability.v2.json"]
    if v8mod.project_v7(v8) != v7:
        errors.append("OP9-DEP-PROJECTION: exact OP8 does not project to exact OP7")
    if v7mod.project_v6(v7) != v6:
        errors.append("OP9-DEP-PROJECTION: exact OP7 does not project to exact OP6")
    if v6mod.project_v5(v6) != v5:
        errors.append("OP9-DEP-PROJECTION: exact OP6 does not project to exact OP5")
    if v5mod.project_op2(v5) != v2:
        errors.append("OP9-DEP-PROJECTION: exact OP5 does not project to protected OP2")
    if errors:
        return None, errors
    context = {
        "buffers": buffers,
        "v8": v8,
        "v8_review": v8_review,
        "v7": v7,
        "v7_review": v7_review,
        "v6": v6,
        "v6_review": v6_review,
        "v5": v5,
        "v2": v2,
        "v8mod": v8mod,
        "v7mod": v7mod,
        "v6mod": v6mod,
        "v5mod": v5mod,
        "v2mod": v2mod,
    }
    context["v8_context"] = {
        "buffers": buffers,
        "v7": v7,
        "v7_review": v7_review,
        "v6": v6,
        "v6_review": v6_review,
        "v5": v5,
        "v2": v2,
        "v7mod": v7mod,
        "v6mod": v6mod,
        "v5mod": v5mod,
        "v2mod": v2mod,
        "expected_v8": v8,
    }
    return context, []


def expected_dependency_closure() -> dict[str, dict[str, str]]:
    kinds = {
        "operability.v8.json": "rejected-predecessor-data",
        "check-operability-v8.py": "rejected-predecessor-executable-source",
        "operability.v8.review-independent-prefreeze.json": "rejection-review-data",
        "operability.v7.json": "protected-lineage-data",
        "check-operability-v7.py": "protected-lineage-executable-source",
        "operability.v7.review-independent-prefreeze.json":
            "protected-lineage-rejection-review-data",
        "operability.v6.json": "protected-lineage-data",
        "check-operability-v6.py": "protected-lineage-executable-source",
        "operability.v6.review-independent-prefreeze.json":
            "protected-lineage-rejection-review-data",
        "operability.v5.json": "protected-lineage-data",
        "check-operability-v5.py": "protected-lineage-executable-source",
        "operability.v2.json": "protected-base-data",
        "check-operability.py": "protected-base-executable-source",
    }
    return {
        name: {"kind": kinds[name], "sha256": digest}
        for name, digest in PINS.items()
    }


def project_v8(candidate: dict[str, Any]) -> dict[str, Any]:
    """Project v9 through only its closed successor delta."""
    result = copy.deepcopy(candidate)
    successor = result["aPrimeSuccessor"]
    metadata = successor["operabilityV9Successor"]
    projection = metadata["v9ToV8Projection"]
    if type(projection) is not dict or \
            type(projection.get("changedRootFields")) is not dict or \
            set(projection["changedRootFields"]) != set(ROOT_ENVELOPE):
        raise ValueError("v9-to-v8 root envelope is not closed")
    if projection.get("removedSuccessorMetadata") != [
            "aPrimeSuccessor.operabilityV9Successor"]:
        raise ValueError("v9-to-v8 metadata removal is not exact")
    successor.pop("operabilityV9Successor")
    for key in ROOT_ENVELOPE:
        result[key] = copy.deepcopy(
            projection["changedRootFields"][key]["before"])
    return result


def _fixed_project_v8(candidate: dict[str, Any], v8: dict[str, Any]) -> Any:
    """Safely remove v9 mechanics using exact frozen-v8 root values."""
    if type(candidate) is not dict or type(candidate.get("aPrimeSuccessor")) is not dict:
        return None
    result = copy.deepcopy(candidate)
    result["aPrimeSuccessor"].pop("operabilityV9Successor", None)
    for key in ROOT_ENVELOPE:
        result[key] = copy.deepcopy(v8[key])
    return result


def _gate(root: Any, gate_id: str) -> dict[str, Any] | None:
    if type(root) is not dict or type(root.get("validationGates")) is not list:
        return None
    rows: list[dict[str, Any]] = []
    for row in root["validationGates"]:
        if type(row) is dict and row.get("id") == gate_id:
            rows.append(row)
    return rows[0] if len(rows) == 1 else None


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
        rendered += f"[{part}]" if type(part) is int else f".{part}"
    return rendered


SENSITIVE_KEYS = {
    "id", "kind", "valid", "expectedErrors", "scope", "state", "rule",
    "field", "operator", "value", "schemaVersion", "plane", "phase",
    "requestId", "budgetOwner", "payloadType", "payloadBytes", "executionId",
    "runId", "bindings", "envelope", "removedSuccessorMetadata",
    "removedLifecycleFields", "changedRootFields", "localDependencyClosure",
    "sha256", "verdict", "blockingFindingId", "blockingFindingIds",
    "exactItemCount", "closedValues", "acceptedTokens", "rejectedTokens",
    "maxDecimalDigitsExcludingSign", "maxSignificandDecimalDigits",
    "maxExponentDecimalDigits", "maxAbsoluteExponent", "forbiddenOutcomes",
    "nonemptyArbitraryFindingSufficient", "closedTotalityDeclarations",
    "numericTokenPolicy", "fixtureKind", "selftestOracle",
}


def heterogeneous_targets(value: dict[str, Any]) -> list[tuple[PathPart, ...]]:
    roots = [
        ("aPrimeSuccessor", "operabilityV6Successor", "requiredIndependentCombinedReview"),
        ("aPrimeSuccessor", "operabilityV6Successor", "v6ToV5Projection"),
        ("aPrimeSuccessor", "operabilityV7Successor"),
        ("aPrimeSuccessor", "operabilityV8Successor"),
        ("aPrimeSuccessor", "lifecycle", "eventSchemaV3"),
        ("aPrimeSuccessor", "lifecycle", "schemaVersionConstraint"),
        ("aPrimeSuccessor", "lifecycle", "phasePlaneBindings"),
        ("aPrimeSuccessor", "lifecycle", "bindingFixtures"),
    ]
    targets: dict[tuple[PathPart, ...], None] = {}

    def walk(node: Any, path: tuple[PathPart, ...]) -> None:
        if type(node) is list:
            for index, child in enumerate(node):
                child_path = path + (index,)
                targets[child_path] = None
                walk(child, child_path)
        elif type(node) is dict:
            for key, child in node.items():
                child_path = path + (key,)
                if key in SENSITIVE_KEYS:
                    targets[child_path] = None
                walk(child, child_path)

    for root_path in roots:
        walk(_path_value(value, root_path), root_path)
    return list(targets)


def _assert_parser_error(failures: list[str], label: str, raw: bytes,
                         expected_code: str) -> None:
    try:
        strict_loads(raw)
    except ControlledInputError as exc:
        if exc.code != expected_code:
            failures.append(f"{label}: expected {expected_code}, got {exc.code}")
    except Exception as exc:
        failures.append(
            f"{label}: parser raised {type(exc).__name__}; exception is a failure")
    else:
        failures.append(f"{label}: expected parser finding {expected_code}, got value")


def _assert_parser_value(failures: list[str], label: str, raw: bytes,
                         expected_value: Any, expected_type: type[Any]) -> None:
    try:
        value = strict_loads(raw)
    except Exception as exc:
        failures.append(
            f"{label}: parser raised {type(exc).__name__}; exception is a failure")
        return
    if type(value) is not expected_type or value != expected_value:
        failures.append(f"{label}: accepted boundary value drift")


def _trust_controls(failures: list[str]) -> int:
    global HERE, _compile_verified
    count = 0
    poison_names = tuple(EXECUTABLE_DEPENDENCIES.values())
    saved_modules = {name: sys.modules.get(name) for name in poison_names}
    poison = types.ModuleType("op9_poison")
    poison.executed = True
    with tempfile.TemporaryDirectory(prefix="op8-path-cache-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        for name in poison_names:
            hostile_source = temp_dir / f"{name}.py"
            hostile_source.write_text(
                "raise RuntimeError('hostile PYTHONPATH/pyc executed')\n",
                encoding="utf-8",
            )
            py_compile.compile(str(hostile_source), doraise=True)
        original_path = list(sys.path)
        original_pythonpath = os.environ.get("PYTHONPATH")
        try:
            sys.path.insert(0, str(temp_dir))
            os.environ["PYTHONPATH"] = str(temp_dir)
            for name in poison_names:
                sys.modules[name] = poison
            context, errors = authenticated_context()
        finally:
            sys.path[:] = original_path
            if original_pythonpath is None:
                os.environ.pop("PYTHONPATH", None)
            else:
                os.environ["PYTHONPATH"] = original_pythonpath
            for name, previous in saved_modules.items():
                if previous is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = previous
    if errors or context is None or any(
            context[key] is poison for key in (
                "v8mod", "v7mod", "v6mod", "v5mod", "v2mod")):
        failures.append("trust sys.modules poison was used or context failed")
    count += 1

    with tempfile.TemporaryDirectory(prefix="op8-buffer-") as temp_name:
        hostile_path = pathlib.Path(temp_name) / "verified_source.py"
        hostile_path.write_text("HOSTILE_DISK_EXECUTED = True\n", encoding="utf-8")
        module = _compile_verified(
            b"AUTHENTICATED_BUFFER_EXECUTED = True\n",
            str(hostile_path), "op8_buffer_snapshot_probe")
        if not getattr(module, "AUTHENTICATED_BUFFER_EXECUTED", False) or \
                getattr(module, "HOSTILE_DISK_EXECUTED", False):
            failures.append("trust compile reread hostile disk instead of verified buffer")
    count += 1

    with tempfile.TemporaryDirectory(prefix="op8-dirty-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        for name in PINS:
            (temp_dir / name).write_bytes((HERE / name).read_bytes())
        dirty_path = temp_dir / "operability.v2.json"
        dirty_path.write_bytes(dirty_path.read_bytes() + b" ")
        compile_calls: list[str] = []
        original_here = HERE
        original_compile = _compile_verified

        def record_compile(raw: bytes, filename: str, module_name: str) -> Any:
            del raw, module_name
            compile_calls.append(filename)
            return types.ModuleType("unexpected_compile")

        try:
            HERE = temp_dir
            _compile_verified = record_compile
            dirty_context, dirty_errors = authenticated_context()
        finally:
            HERE = original_here
            _compile_verified = original_compile
        if dirty_context is not None or not any(
                error.startswith("OP9-DEP-HASH:") for error in dirty_errors) or \
                compile_calls:
            failures.append("trust dirty dependency did not fail before all compilation")
    count += 1
    return count


# V9 uses closed finding records.  The inherited string-based v8 surface is
# parsed once at its API boundary; no detail text is ever interpreted as a code.
FindingRecord = dict[str, str]


def _finding(code: str, detail: str) -> FindingRecord:
    return {"code": code, "detail": detail}


def _finding_record_errors(value: Any) -> list[str]:
    errors: list[str] = []
    if type(value) is not dict or set(value) != FINDING_RECORD_KEYS:
        return ["finding record must have exactly code and detail"]
    code = value.get("code")
    detail = value.get("detail")
    if type(code) is not str or CODE_RE.fullmatch(code) is None:
        errors.append("finding code is malformed")
    if type(detail) is not str or not detail or "\n" in detail or "\r" in detail:
        errors.append("finding detail is malformed")
    else:
        size, unicode_errors = _utf8_size(detail, "$.detail")
        if unicode_errors:
            errors.append("finding detail is not Unicode-scalar text")
        elif size is not None and size > MAX_STRING_UTF8_BYTES:
            errors.append("finding detail exceeds the UTF-8 byte bound")
    return errors


def _parse_text_finding(value: Any, source: str) -> FindingRecord:
    if type(value) is not str:
        return _finding(
            "OP9-INTERNAL-MALFORMED-API-FINDING",
            f"{source} returned a non-string finding")
    code, separator, detail = value.partition(": ")
    if not separator or CODE_RE.fullmatch(code) is None or not detail or \
            "\n" in detail or "\r" in detail:
        return _finding(
            "OP9-INTERNAL-MALFORMED-API-FINDING",
            f"{source} returned a malformed finding record")
    return _finding(code, detail)


def _records_from_text(findings: Any, source: str) -> list[FindingRecord]:
    if type(findings) is not list:
        return [_finding(
            "OP9-INTERNAL-MALFORMED-API-FINDING",
            f"{source} returned a non-array finding collection")]
    return _unique_records([
        _parse_text_finding(item, source) for item in findings])


def _unique_records(records: list[FindingRecord]) -> list[FindingRecord]:
    """Aggregate legacy same-code details before the duplicate-free v9 boundary."""
    result: list[FindingRecord] = []
    positions: dict[str, int] = {}
    for record in records:
        code = record.get("code") if type(record) is dict else None
        marker = code if type(code) is str else "OP9-INTERNAL-MALFORMED-RECORD"
        if marker not in positions:
            normalized = record if type(record) is dict else _finding(
                marker, "non-object finding reached aggregation")
            positions[marker] = len(result)
            result.append(normalized)
            continue
        existing = result[positions[marker]]
        detail = record.get("detail") if type(record) is dict else "malformed detail"
        if type(detail) is str and detail not in existing["detail"].split(" | "):
            existing["detail"] += f" | {detail}"
    return result


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return _digest(raw)


def _v9_metadata_shape_records(value: Any) -> list[FindingRecord]:
    if type(value) is not dict:
        return [_finding(
            "OP9-SHAPE-V9-METADATA", "v9 successor metadata must be an object")]
    records: list[FindingRecord] = []
    authorship = value.get("authorshipAndReviewSeparation")
    rejection = value.get("rejectionBinding")
    review = value.get("requiredIndependentRereview")
    closure = value.get("localDependencyClosure")
    declarations = value.get("closedOracleAndStartupDeclarations")
    projection = value.get("v9ToV8Projection")
    if type(authorship) is not dict:
        records.append(_finding(
            "OP9-SHAPE-AUTHORSHIP", "authorship separation must be an object"))
    if type(rejection) is not dict:
        records.append(_finding(
            "OP9-SHAPE-REJECTION", "rejection binding must be an object"))
    else:
        ids = rejection.get("blockingFindingIds")
        if not _exact_string_array(ids, V8_REVIEW_FINDINGS):
            records.append(_finding(
                "OP9-SHAPE-REJECTION", "blocking finding ids must be exact and ordered"))
        reviewed = rejection.get("reviewedCandidate")
        if type(reviewed) is not dict or any(
                type(reviewed.get(key)) is not str
                for key in ("artifact", "sha256", "checker", "checkerSha256")):
            records.append(_finding(
                "OP9-SHAPE-REJECTION", "reviewed candidate binding is malformed"))
    if type(review) is not dict or type(review.get("scope")) is not list or \
            any(type(item) is not str or not item for item in review.get("scope", [])):
        records.append(_finding(
            "OP9-SHAPE-REVIEW", "different-reviewer requirement is malformed"))
    if type(closure) is not dict or len(closure) != len(PINS):
        records.append(_finding(
            "OP9-SHAPE-CLOSURE", "v9 closure must contain thirteen entries"))
    else:
        for name, row in closure.items():
            if type(name) is not str or type(row) is not dict or \
                    type(row.get("kind")) is not str or \
                    type(row.get("sha256")) is not str:
                records.append(_finding(
                    "OP9-SHAPE-CLOSURE", "v9 closure entry is malformed"))
                break
    if type(declarations) is not dict:
        records.append(_finding(
            "OP9-SHAPE-ORACLE", "oracle/startup declarations must be an object"))
    else:
        for key in (
                "findingRecord", "legacyApiFindingAdapter", "machineResult", "exactOracle",
                "genericForbiddenOutcomeRule", "startupBoundary",
                "retainedTotality"):
            if type(declarations.get(key)) is not dict:
                records.append(_finding(
                    "OP9-SHAPE-ORACLE", f"{key} must be an object"))
        controls = declarations.get("requiredInjectedRegressionControls")
        if type(controls) is not list or any(
                type(item) is not str or not item for item in controls):
            records.append(_finding(
                "OP9-SHAPE-ORACLE", "regression controls must be strings"))
    if type(projection) is not dict:
        records.append(_finding(
            "OP9-SHAPE-PROJECTION", "v9-to-v8 projection must be an object"))
    else:
        changed = projection.get("changedRootFields")
        removed = projection.get("removedSuccessorMetadata")
        if type(changed) is not dict or set(changed) != set(ROOT_ENVELOPE):
            records.append(_finding(
                "OP9-SHAPE-PROJECTION", "changed root fields are not closed"))
        else:
            for key in ROOT_ENVELOPE:
                row = changed.get(key)
                if type(row) is not dict or set(row) != {"before", "after"}:
                    records.append(_finding(
                        "OP9-SHAPE-PROJECTION", "root projection row is malformed"))
                    break
        if removed != ["aPrimeSuccessor.operabilityV9Successor"]:
            records.append(_finding(
                "OP9-SHAPE-PROJECTION", "metadata removal is not exact"))
    return _unique_records(records)


def _v9_exact_candidate(value: dict[str, Any], context: dict[str, Any]) -> bool:
    successor = value.get("aPrimeSuccessor")
    if type(successor) is not dict:
        return False
    metadata = successor.get("operabilityV9Successor")
    if type(metadata) is not dict:
        return False
    try:
        metadata_exact = _canonical_sha256(metadata) == V9_METADATA_SHA256
    except (TypeError, ValueError, UnicodeError):
        return False
    if not metadata_exact or any(
            value.get(key) != wanted for key, wanted in V9_ROOT.items()):
        return False
    projected = _fixed_project_v8(value, context["v8"])
    return projected == context["v8"]


def _check_v9_impl(value: Any, *, verify_files: bool,
                   context: dict[str, Any] | None) -> list[FindingRecord]:
    bounded = json_value_findings(value)
    if bounded:
        return _records_from_text(bounded, "v9 bounded-value validator")
    if type(value) is not dict:
        return [_finding("OP9-TOTALITY-ROOT", "root must be an object")]
    if context is None:
        if not verify_files:
            return [_finding(
                "OP9-DEP-CONTEXT", "unauthenticated context is forbidden")]
        context, dependency_errors = authenticated_context()
        if dependency_errors or context is None:
            return _records_from_text(
                dependency_errors or ["OP9-DEP-CONTEXT: context unavailable"],
                "v9 dependency authenticator")
    if type(context) is not dict or type(context.get("v8")) is not dict or \
            context.get("v8mod") is None or type(context.get("v8_context")) is not dict:
        return [_finding(
            "OP9-DEP-CONTEXT", "authenticated context is malformed")]

    successor = value.get("aPrimeSuccessor")
    if type(successor) is not dict:
        return [
            _finding("OP9-FULL", "candidate differs from complete expected v9"),
            _finding("OP9-SHAPE-SUCCESSOR", "aPrimeSuccessor must be an object"),
        ]
    metadata = successor.get("operabilityV9Successor")
    records: list[FindingRecord] = []
    exact = _v9_exact_candidate(value, context)
    if not exact:
        records.append(_finding(
            "OP9-FULL", "candidate differs from complete expected v9"))
        records.extend(_v9_metadata_shape_records(metadata))
        projected = _fixed_project_v8(value, context["v8"])
        if projected is None:
            records.append(_finding(
                "OP9-SHAPE-SUCCESSOR", "cannot form the fixed v8 projection"))
        else:
            inherited = context["v8mod"].check(
                projected, verify_files=False, context=context["v8_context"])
            records.extend(_records_from_text(inherited, "verified OP8 checker"))
        return _unique_records(records)

    metadata_records = _v9_metadata_shape_records(metadata)
    if metadata_records:
        return metadata_records
    if metadata["localDependencyClosure"] != expected_dependency_closure():
        records.append(_finding(
            "OP9-DEP-CLOSURE", "declared thirteen-file closure drift"))
    review = context["v8_review"]
    rejection = metadata["rejectionBinding"]
    if rejection["sha256"] != PINS[
            "operability.v8.review-independent-prefreeze.json"] or \
            rejection["verdict"] != "REJECT" or \
            tuple(rejection["blockingFindingIds"]) != V8_REVIEW_FINDINGS or \
            review["verdict"]["decision"] != "REJECT":
        records.append(_finding(
            "OP9-REVIEW", "exact v8 rejection/verdict/findings binding drift"))
    authorship = metadata["authorshipAndReviewSeparation"]
    if authorship["v8IndependentReviewAuthoredByV9Author"] is not True or \
            authorship["v9ApprovalAuthorityOfThisAuthor"] != "NONE":
        records.append(_finding(
            "OP9-AUTHORSHIP", "author/reviewer separation was weakened"))

    v8 = context["v8"]
    projected_v8 = project_v8(value)
    if projected_v8 != v8:
        records.append(_finding(
            "OP9-PROJ", "v9 does not project exact-deep-equal to v8"))
    inherited = context["v8mod"].check(
        projected_v8, verify_files=False, context=context["v8_context"])
    if inherited:
        records.append(_finding(
            "OP9-INTERNAL-INHERITED-CHECK",
            "exact projected v8 semantic checker returned findings"))
    projected_v7 = context["v8mod"].project_v7(projected_v8)
    projected_v6 = context["v7mod"].project_v6(projected_v7)
    projected_v5 = context["v6mod"].project_v5(projected_v6)
    projected_v2 = context["v5mod"].project_op2(projected_v5)
    if projected_v7 != context["v7"] or projected_v6 != context["v6"] or \
            projected_v5 != context["v5"] or projected_v2 != context["v2"]:
        records.append(_finding(
            "OP9-PROJ", "ordered inherited projection chain drift"))
    if successor["lifecycle"] != v8["aPrimeSuccessor"]["lifecycle"]:
        records.append(_finding(
            "OP9-SEMANTIC", "EventEnvelopeV3 lifecycle object changed"))
    for inherited_key in ("operabilityV6Successor", "operabilityV7Successor",
                          "operabilityV8Successor"):
        if successor[inherited_key] != v8["aPrimeSuccessor"][inherited_key]:
            records.append(_finding(
                "OP9-SEMANTIC", "inherited successor metadata changed"))
            break
    if _gate(value, "G19") != _gate(v8, "G19") or \
            (_gate(value, "G19") or {}).get("status") != "BLOCKED-NO-MECHANISM":
        records.append(_finding(
            "OP9-G19", "inherited gate changed or was promoted"))
    return _unique_records(records)


def check(value: Any, *, verify_files: bool = True,
          context: dict[str, Any] | None = None) -> list[FindingRecord]:
    """Return closed findings; checker defects propagate as test failures."""
    return _check_v9_impl(value, verify_files=verify_files, context=context)


def _record_codes(records: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    codes: list[str] = []
    if type(records) is not list:
        return [], ["finding collection is not an array"]
    for index, record in enumerate(records):
        record_errors = _finding_record_errors(record)
        if record_errors:
            errors.extend(f"record {index}: {error}" for error in record_errors)
        elif type(record) is dict:
            codes.append(record["code"])
    return codes, errors


def _forbidden_outcomes(codes: list[str],
                        transport_classes: tuple[str, ...]) -> list[str]:
    prohibited: list[str] = []
    for field in [*codes, *transport_classes]:
        lowered = field.lower()
        if any(token in lowered for token in FORBIDDEN_OUTCOME_TOKENS):
            prohibited.append(field)
    return prohibited


def _evaluate_exact_outcome(records: Any, expected_codes: tuple[str, ...],
                            transport_classes: tuple[str, ...] = ()) -> list[str]:
    """Exact unordered set equality with duplicates forbidden on both sides."""
    failures: list[str] = []
    if len(expected_codes) != len(set(expected_codes)) or any(
            CODE_RE.fullmatch(code) is None for code in expected_codes):
        failures.append("declared expected code set is malformed or duplicated")
    codes, record_errors = _record_codes(records)
    failures.extend(record_errors)
    duplicate_codes = sorted(
        code for code, count in collections.Counter(codes).items() if count > 1)
    if duplicate_codes:
        failures.append(f"duplicate actual codes {duplicate_codes}")
    forbidden = _forbidden_outcomes(codes, transport_classes)
    if forbidden:
        failures.append(f"forbidden outcome classes {sorted(forbidden)}")
    if transport_classes:
        failures.append(f"transport failures {sorted(transport_classes)}")
    if collections.Counter(codes) != collections.Counter(expected_codes):
        failures.append(
            f"exact code set mismatch: expected {sorted(expected_codes)}, "
            f"got {sorted(codes)}")
    return failures


def _machine_payload(status: str, records: list[FindingRecord],
                     artifact_hash: str | None,
                     counts: dict[str, int] | None) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "operability-v9-result",
        "status": status,
        "artifactSha256": artifact_hash,
        "findings": records,
        "selftestCounts": counts,
    }


def _emit_machine(status: str, records: list[FindingRecord],
                  artifact_hash: str | None = None,
                  counts: dict[str, int] | None = None) -> None:
    payload = _machine_payload(status, records, artifact_hash, counts)
    sys.stdout.write(json.dumps(
        payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")


def _parse_machine_bytes(stdout: bytes, stderr: bytes) -> tuple[
        list[FindingRecord], tuple[str, ...], dict[str, Any] | None]:
    transport: list[str] = []
    if stderr:
        transport.append("STDERR")
    if not stdout.endswith(b"\n") or stdout.count(b"\n") != 1 or b"\r" in stdout:
        transport.append("UNSTRUCTURED-STDOUT")
    try:
        value = strict_loads(stdout)
    except ControlledInputError:
        return [], tuple(sorted(set(transport + ["MALFORMED-RECORD"]))), None
    if type(value) is not dict or set(value) != MACHINE_RESULT_KEYS:
        return [], tuple(sorted(set(transport + ["MALFORMED-RECORD"]))), None
    if value.get("schemaVersion") != 1 or \
            value.get("kind") != "operability-v9-result" or \
            value.get("status") not in ("PASS", "FAIL"):
        transport.append("MALFORMED-RECORD")
    artifact_hash = value.get("artifactSha256")
    if value.get("status") == "PASS":
        if type(artifact_hash) is not str or re.fullmatch(
                r"[0-9a-f]{64}", artifact_hash) is None:
            transport.append("MALFORMED-RECORD")
    elif artifact_hash is not None:
        transport.append("MALFORMED-RECORD")
    counts = value.get("selftestCounts")
    if counts is not None and (type(counts) is not dict or
            set(counts) != SELFTEST_COUNT_KEYS or any(
                type(item) is not int or item < 0 for item in counts.values())):
        transport.append("MALFORMED-RECORD")
    if value.get("status") == "FAIL" and counts is not None:
        transport.append("MALFORMED-RECORD")
    records = value.get("findings")
    _, record_errors = _record_codes(records)
    if record_errors:
        transport.append("MALFORMED-RECORD")
        records = records if type(records) is list else []
    if value.get("status") == "PASS" and records:
        transport.append("MALFORMED-RECORD")
    if value.get("status") == "FAIL" and not records:
        transport.append("MALFORMED-RECORD")
    return records, tuple(sorted(set(transport))), value


def _sanitized_python_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    source = os.environ.copy()
    if extra:
        source.update(extra)
    return {
        key: value for key, value in source.items()
        if not key.upper().startswith("PYTHON")
    }


def _isolated_child_command(*args: str,
                            runtime_options: tuple[str, ...] = ()) -> list[str]:
    return [
        sys.executable, "-I", "-B", *runtime_options,
        str(pathlib.Path(__file__).resolve()), *args,
    ]


def _oracle_regression_controls(failures: list[str]) -> dict[str, int]:
    expected = "OP9-EXPECTED"
    valid = _finding(expected, "expected detail")
    cases: list[tuple[str, list[Any], tuple[str, ...], tuple[str, ...], bool]] = [
        ("valid exact record", [valid], (expected,), (), False),
        ("expected text only in detail",
         [_finding("OP9-WRONG", f"detail mentions {expected}: only")],
         (expected,), (), True),
        ("wrong code", [_finding("OP9-WRONG", "wrong")], (expected,), (), True),
        ("additional code", [valid, _finding("OP9-EXTRA", "extra")],
         (expected,), (), True),
        ("duplicate code", [valid, copy.deepcopy(valid)], (expected,), (), True),
        ("near prefix", [_finding("OP9-EXPECTED-X", "near")],
         (expected,), (), True),
        ("near suffix", [_finding("X-OP9-EXPECTED", "near")],
         (expected,), (), True),
        ("internal code", [_finding("OP9-INTERNAL-X", "forbidden")],
         ("OP9-INTERNAL-X",), (), True),
        ("exception code", [_finding("OP9-EXCEPTION-X", "forbidden")],
         ("OP9-EXCEPTION-X",), (), True),
        ("traceback code", [_finding("OP9-TRACEBACK-X", "forbidden")],
         ("OP9-TRACEBACK-X",), (), True),
        ("typeerror code", [_finding("OP9-TYPEERROR-X", "forbidden")],
         ("OP9-TYPEERROR-X",), (), True),
        ("malformed finding", [{"code": expected}], (expected,), (), True),
        ("expected plus internal", [valid, _finding("OP9-INTERNAL-X", "bad")],
         (expected,), (), True),
        ("outward exception transport", [valid], (expected,),
         ("OuTwArD-ExCePtIoN",), True),
        ("detail is non-authoritative for forbidden class",
         [_finding(expected, "detail says INTERNAL and TRACEBACK")],
         (expected,), (), False),
    ]
    rejected = 0
    for label, records, expected_codes, transport, should_fail in cases:
        observed_fail = bool(_evaluate_exact_outcome(
            records, expected_codes, transport))
        if observed_fail != should_fail:
            failures.append(f"oracle regression {label}: outcome drift")
        if observed_fail:
            rejected += 1

    duplicate_key = (
        b'{"schemaVersion":1,"schemaVersion":1,"kind":"operability-v9-result",'
        b'"status":"FAIL","artifactSha256":null,"findings":[],'
        b'"selftestCounts":null}\n')
    _, malformed_transport, _ = _parse_machine_bytes(duplicate_key, b"")
    if "MALFORMED-RECORD" not in malformed_transport:
        failures.append("oracle regression duplicate machine key was accepted")
    _, stderr_transport, _ = _parse_machine_bytes(
        json.dumps(_machine_payload(
            "FAIL", [valid], None, None), separators=(",", ":")).encode() + b"\n",
        b"unexpected stderr")
    if "STDERR" not in stderr_transport:
        failures.append("oracle regression machine stderr was accepted")
    _, unstructured_transport, _ = _parse_machine_bytes(b"not-json\n", b"")
    if "MALFORMED-RECORD" not in unstructured_transport:
        failures.append("oracle regression unstructured output was accepted")

    extra_records = [valid, _finding("OP9-EXTRA", "extra")]
    subset_mutant_accepts = set([expected]).issubset(
        {record["code"] for record in extra_records})
    exact_rejects_extra = bool(_evaluate_exact_outcome(
        extra_records, (expected,)))
    detail_records = [_finding("OP9-WRONG", f"{expected}: detail only")]
    substring_mutant_accepts = any(
        expected in record["code"] or expected in record["detail"]
        for record in detail_records)
    exact_rejects_detail = bool(_evaluate_exact_outcome(
        detail_records, (expected,)))
    subset_killed = subset_mutant_accepts and exact_rejects_extra
    substring_killed = substring_mutant_accepts and exact_rejects_detail
    if not subset_killed:
        failures.append("oracle regression did not kill subset mutant")
    if not substring_killed:
        failures.append("oracle regression did not kill substring mutant")
    return {
        "injected": len(cases) + 3,
        "rejected": rejected + 3,
        "mutantsKilled": int(subset_killed) + int(substring_killed),
    }


def _declared_mutation_codes(candidate: Any,
                             context: dict[str, Any]) -> tuple[str, ...]:
    """Derive the complete expected non-exact set from separate shape surfaces."""
    bounded = json_value_findings(candidate)
    if bounded:
        records = _records_from_text(bounded, "declared bounded-value oracle")
        return tuple(record["code"] for record in _unique_records(records))
    if type(candidate) is not dict:
        return ("OP9-TOTALITY-ROOT",)
    successor = candidate.get("aPrimeSuccessor")
    if type(successor) is not dict:
        return ("OP9-FULL", "OP9-SHAPE-SUCCESSOR")
    records: list[FindingRecord] = [
        _finding("OP9-FULL", "candidate differs from complete expected v9")]
    records.extend(_v9_metadata_shape_records(
        successor.get("operabilityV9Successor")))
    projected = _fixed_project_v8(candidate, context["v8"])
    if projected is None:
        records.append(_finding(
            "OP9-SHAPE-SUCCESSOR", "cannot form the fixed v8 projection"))
    elif projected != context["v8"]:
        inherited_strings = [
            "OP8-FULL: candidate differs from complete expected v8",
            *context["v8mod"].structural_delta_findings(
                projected, context["v8"]),
            *context["v8mod"].shape_findings(projected),
        ]
        records.extend(_records_from_text(
            inherited_strings, "declared OP8 shape oracle"))
    return tuple(record["code"] for record in _unique_records(records))


def _assert_v9_case(failures: list[str], label: str, candidate: Any,
                    expected_codes: tuple[str, ...], context: dict[str, Any],
                    required_specific: tuple[str, ...] = ()) -> None:
    for code in required_specific:
        if code not in expected_codes:
            failures.append(
                f"{label}: declared exact set omits required specific code {code}")
    try:
        records = check(candidate, verify_files=False, context=context)
    except Exception as exc:
        failures.append(
            f"{label}: OUTWARD-EXCEPTION {type(exc).__name__}; escape")
        return
    outcome_failures = _evaluate_exact_outcome(records, expected_codes)
    for failure in outcome_failures:
        failures.append(f"{label}: {failure}")


def _cli_controls_v9(failures: list[str], clean_value: dict[str, Any]) -> int:
    node_inner = b"[" + b",".join([b"0"] * MAX_ARRAY_ITEMS) + b"]"
    node_bound_raw = b"[" + b",".join([node_inner] * 10) + b"]"
    controls: list[tuple[str, bytes, str, int, tuple[str, ...]]] = [
        ("4300-digit integer/default", b"1" * 4300,
         "OP9-TOTALITY-ROOT", 1, ()),
        ("4300-digit integer/runtime-low", b"1" * 4300,
         "OP9-TOTALITY-ROOT", 1, ("-X", "int_max_str_digits=640")),
        ("4300-digit integer/runtime-disabled", b"1" * 4300,
         "OP9-TOTALITY-ROOT", 1, ("-X", "int_max_str_digits=0")),
        ("4301-digit integer/default", b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, ()),
        ("4301-digit integer/runtime-low", b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2,
         ("-X", "int_max_str_digits=640")),
        ("4301-digit integer/runtime-disabled", b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2,
         ("-X", "int_max_str_digits=0")),
        ("5000-digit integer/default", b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, ()),
        ("5000-digit integer/runtime-disabled", b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2,
         ("-X", "int_max_str_digits=0")),
        ("5000-digit integer/runtime-low", b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2,
         ("-X", "int_max_str_digits=640")),
        ("negative 4301-digit integer", b"-" + b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, ()),
        ("negative 5000-digit integer", b"-" + b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, ()),
        ("float significand over bound", b"0." + b"1" * 4300,
         "OP8-NUMERIC-FLOAT-DIGITS", 2, ()),
        ("positive exponent nonfinite", b"1e4300",
         "OP8-NUMERIC-NONFINITE", 2, ()),
        ("positive exponent over bound", b"1e4301",
         "OP8-NUMERIC-EXPONENT", 2, ()),
        ("negative exponent over bound", b"-1e-4301",
         "OP8-NUMERIC-EXPONENT", 2, ()),
        ("NaN constant", b"NaN", "OP8-NUMERIC-CONSTANT", 2, ()),
        ("Infinity constant", b"Infinity", "OP8-NUMERIC-CONSTANT", 2, ()),
        ("negative Infinity constant", b"-Infinity",
         "OP8-NUMERIC-CONSTANT", 2, ()),
        ("invalid leading-zero number", b"01", "OP8-JSON-SYNTAX", 2, ()),
        ("duplicate object member", b'{"x":1,"x":2}',
         "OP8-JSON-DUPLICATE", 2, ()),
        ("malformed UTF-8", b'"\xff"', "OP8-JSON-UTF8", 2, ()),
        ("depth over bound", b"[" * 66 + b"0" + b"]" * 66,
         "OP8-LIMIT-DEPTH", 2, ()),
        ("array over bound", b"[" + b",".join([b"0"] * 10001) + b"]",
         "OP8-LIMIT-ARRAY", 2, ()),
        ("object over bound", b"{" + b",".join(
            f'"k{i}":0'.encode("ascii") for i in range(10001)) + b"}",
         "OP8-LIMIT-OBJECT", 2, ()),
        ("node count over bound", node_bound_raw, "OP8-LIMIT-NODES", 2, ()),
        ("string over bound",
         b'"' + b"x" * (MAX_STRING_UTF8_BYTES + 1) + b'"',
         "OP8-LIMIT-STRING", 2, ()),
        ("raw over bound", b" " * (MAX_RAW_BYTES + 1),
         "OP8-LIMIT-RAW", 2, ()),
    ]
    with tempfile.TemporaryDirectory(prefix="op9-cli-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        case_path = temp_dir / "case.json"
        for label, raw, expected_code, expected_exit, runtime_options in controls:
            case_path.write_bytes(raw)
            try:
                completed = subprocess.run(
                    _isolated_child_command(
                        str(case_path), "--machine",
                        runtime_options=runtime_options),
                    capture_output=True,
                    check=False,
                    env=_sanitized_python_env(),
                    timeout=30,
                )
            except Exception as exc:
                failures.append(
                    f"CLI {label}: OUTWARD-EXCEPTION {type(exc).__name__}")
                continue
            records, transport, result = _parse_machine_bytes(
                completed.stdout, completed.stderr)
            if completed.returncode != expected_exit:
                failures.append(
                    f"CLI {label}: exit {completed.returncode} != {expected_exit}")
            if result is None or result.get("status") != "FAIL":
                failures.append(f"CLI {label}: structured FAIL status missing")
            for failure in _evaluate_exact_outcome(
                    records, (expected_code,), transport):
                failures.append(f"CLI {label}: {failure}")

        dirty = copy.deepcopy(clean_value)
        dirty["status"] = "APPLIED"
        case_path.write_text(
            json.dumps(dirty, ensure_ascii=False), encoding="utf-8")
        try:
            completed = subprocess.run(
                _isolated_child_command(
                    str(case_path), "--selftest", "--machine"),
                capture_output=True,
                check=False,
                env=_sanitized_python_env(),
                timeout=30,
            )
            records, transport, result = _parse_machine_bytes(
                completed.stdout, completed.stderr)
            if completed.returncode != 1 or result is None or \
                    result.get("status") != "FAIL" or \
                    result.get("selftestCounts") is not None:
                failures.append("CLI dirty base did not refuse selftest structurally")
            for failure in _evaluate_exact_outcome(
                    records, ("OP9-FULL",), transport):
                failures.append(f"CLI dirty base: {failure}")
        except Exception as exc:
            failures.append(
                f"CLI dirty base: OUTWARD-EXCEPTION {type(exc).__name__}")
    return len(controls) + 1


def _isolation_controls(failures: list[str]) -> int:
    count = 0
    if sys.flags.isolated != 1:
        failures.append("parent isolated-mode flag is not set")
    count += 1
    clean_env = _sanitized_python_env()
    if any(key.upper().startswith("PYTHON") for key in clean_env):
        failures.append("sanitized child environment retained PYTHON input")
    count += 1
    with tempfile.TemporaryDirectory(prefix="op9-isolation-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        marker = temp_dir / "marker"
        (temp_dir / "sitecustomize.py").write_text(
            "import os, pathlib\n"
            "pathlib.Path(os.environ['OP9_ISOLATION_MARKER']).write_text('seen')\n",
            encoding="utf-8",
        )
        try:
            completed = subprocess.run(
                _isolated_child_command("--machine"),
                capture_output=True,
                check=False,
                cwd=temp_dir,
                env=_sanitized_python_env({
                    "OP9_ISOLATION_MARKER": str(marker),
                }),
                timeout=30,
            )
            records, transport, result = _parse_machine_bytes(
                completed.stdout, completed.stderr)
            if marker.exists() or completed.returncode != 0 or \
                    transport or result is None or result.get("status") != "PASS" or \
                    records:
                failures.append("nested isolated marker/control failed")
        except Exception as exc:
            failures.append(
                f"nested isolated control OUTWARD-EXCEPTION {type(exc).__name__}")
    count += 1

    # Exactly one sanitized non-isolated child is permitted, only to diagnose
    # the early refusal.  It grants no authority and proves no startup safety.
    with tempfile.TemporaryDirectory(prefix="op9-unsupported-") as temp_name:
        try:
            completed = subprocess.run(
                [sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
                 "--machine"],
                capture_output=True,
                check=False,
                cwd=temp_name,
                env=_sanitized_python_env(),
                timeout=30,
            )
            expected = {
                "schemaVersion": 1,
                "kind": "unsupported-mode",
                "status": "UNSUPPORTED",
                "code": "OP9-UNSUPPORTED-NONISOLATED",
                "detail": "isolated Python startup is required",
            }
            parsed: Any = None
            try:
                parsed = strict_loads(completed.stdout)
            except ControlledInputError:
                pass
            if completed.returncode != 3 or completed.stderr or \
                    completed.stdout.count(b"\n") != 1 or parsed != expected:
                failures.append("sanitized non-isolated refusal result drift")
        except Exception as exc:
            failures.append(
                f"non-isolated refusal control OUTWARD-EXCEPTION {type(exc).__name__}")
    count += 1
    return count


def selftest(value: dict[str, Any],
             context: dict[str, Any]) -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    targeted: list[tuple[str, Any, tuple[str, ...], tuple[str, ...]]] = []
    heterogeneous: list[tuple[str, Any, tuple[str, ...], tuple[str, ...]]] = []

    def mutate_copy(label: str, mutate: Callable[[dict[str, Any]], None],
                    sink: list[str]) -> dict[str, Any] | None:
        candidate = copy.deepcopy(value)
        before = copy.deepcopy(candidate)
        try:
            mutate(candidate)
        except Exception as exc:
            sink.append(
                f"{label}: mutation failed to apply ({type(exc).__name__}); escape")
            return None
        if candidate == before:
            sink.append(f"{label}: no-op mutation; escape")
            return None
        return candidate

    def add(target: list[tuple[str, Any, tuple[str, ...], tuple[str, ...]]],
            label: str, mutate: Callable[[dict[str, Any]], None],
            required_specific: tuple[str, ...] = ()) -> None:
        candidate = mutate_copy(label, mutate, failures)
        if candidate is None:
            return
        expected_codes = _declared_mutation_codes(candidate, context)
        target.append((label, candidate, expected_codes, required_specific))

    escape_probe: list[str] = []
    mutate_copy("no-op probe", lambda candidate: None, escape_probe)
    mutate_copy("failure-to-apply probe",
                lambda candidate: (_ for _ in ()).throw(ValueError("probe")),
                escape_probe)
    if len(escape_probe) != 2 or not any(
            "no-op mutation" in item for item in escape_probe) or not any(
            "failed to apply" in item for item in escape_probe):
        failures.append("no-op/failure-to-apply escape controls drifted")

    v9meta = lambda c: c["aPrimeSuccessor"]["operabilityV9Successor"]
    v8meta = lambda c: c["aPrimeSuccessor"]["operabilityV8Successor"]
    lifecycle = lambda c: c["aPrimeSuccessor"]["lifecycle"]
    add(targeted, "status promotion",
        lambda c: c.__setitem__("status", "APPLIED"), ("OP9-FULL",))
    add(targeted, "v9 rejection verdict erased",
        lambda c: v9meta(c)["rejectionBinding"].__setitem__("verdict", "PASS"),
        ("OP9-FULL",))
    add(targeted, "v9 rejection finding erased",
        lambda c: v9meta(c)["rejectionBinding"]["blockingFindingIds"].pop(),
        ("OP9-SHAPE-REJECTION",))
    add(targeted, "v9 dependency closure incomplete",
        lambda c: v9meta(c)["localDependencyClosure"].pop(
            "operability.v8.review-independent-prefreeze.json"),
        ("OP9-SHAPE-CLOSURE",))
    add(targeted, "author approval self-grant",
        lambda c: v9meta(c)["authorshipAndReviewSeparation"].__setitem__(
            "v9ApprovalAuthorityOfThisAuthor", "GRANTED"), ("OP9-FULL",))
    add(targeted, "subset oracle metadata regression",
        lambda c: v9meta(c)["closedOracleAndStartupDeclarations"][
            "exactOracle"].__setitem__("comparison", "EXPECTED-SUBSET"),
        ("OP9-FULL",))
    add(targeted, "substring oracle metadata regression",
        lambda c: v9meta(c)["closedOracleAndStartupDeclarations"][
            "findingRecord"].__setitem__("codeSourceRule", "search text"),
        ("OP9-FULL",))
    add(targeted, "machine stderr weakened",
        lambda c: v9meta(c)["closedOracleAndStartupDeclarations"][
            "machineResult"].__setitem__("stderr", "PERMITTED"),
        ("OP9-FULL",))
    add(targeted, "non-isolated command introduced",
        lambda c: v9meta(c)["closedOracleAndStartupDeclarations"][
            "startupBoundary"]["soleConformanceCommands"].append(
                "python3 -B check-operability-v9.py"), ("OP9-FULL",))
    add(targeted, "v9 projection weakened",
        lambda c: v9meta(c)["v9ToV8Projection"].__setitem__(
            "deepEqualityRule", "field presence"), ("OP9-FULL",))
    add(targeted, "inherited numeric bound drift",
        lambda c: v8meta(c)["closedTotalityDeclarations"]["numericTokenPolicy"][
            "integer"].__setitem__("maxDecimalDigitsExcludingSign", 5000),
        ("OP8-FULL",))
    add(targeted, "semantic schema version change",
        lambda c: lifecycle(c)["schemaVersionConstraint"].__setitem__("value", 4),
        ("OP8-FULL",))
    add(targeted, "semantic run-committed plane change",
        lambda c: lifecycle(c)["phasePlaneBindings"].__setitem__(
            "run-committed", "diagnostics"), ("OP8-FULL",))
    add(targeted, "review scope object counterexample",
        lambda c: c["aPrimeSuccessor"]["operabilityV6Successor"][
            "requiredIndependentCombinedReview"].__setitem__("scope", [{}]),
        ("OP8-SHAPE-STRING-ARRAY",))
    add(targeted, "fixture id list counterexample",
        lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("id", []),
        ("OP8-SHAPE-FIXTURE-ID",))
    add(targeted, "fixture id object counterexample",
        lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("id", {}),
        ("OP8-SHAPE-FIXTURE-ID",))
    add(targeted, "duplicate fixture id",
        lambda c: lifecycle(c)["bindingFixtures"][1].__setitem__(
            "id", lifecycle(c)["bindingFixtures"][0]["id"]),
        ("OP8-SHAPE-FIXTURE-ID-DUPLICATE",))

    for index in range(8):
        for label, replacement in (
                ("null", None), ("boolean", True), ("integer", 7),
                ("float", 7.5), ("unknown-string", "heterogeneous"),
                ("array", []), ("object", {})):
            expected = "OP8-SHAPE-FIXTURE-KIND-VALUE" if type(
                replacement) is str else "OP8-SHAPE-FIXTURE-KIND-TYPE"
            add(
                targeted,
                f"fixture kind {label} at row {index}",
                lambda c, i=index, r=copy.deepcopy(replacement):
                    lifecycle(c)["bindingFixtures"][i].__setitem__("kind", r),
                (expected,),
            )

    variants: list[tuple[str, Any]] = [
        ("null", None), ("boolean", True), ("integer", 7), ("float", 7.5),
        ("string", "heterogeneous"), ("array", []),
        ("object", {"heterogeneous": True}),
    ]
    kind_prefix = ("aPrimeSuccessor", "lifecycle", "bindingFixtures")
    for path in heterogeneous_targets(value):
        original = _path_value(value, path)
        for variant_name, replacement in variants:
            if type(original) is type(replacement) and original == replacement:
                continue
            required: tuple[str, ...] = ()
            if type(original) is not type(replacement):
                required = ("OP8-SHAPE-TYPE",)
            elif type(original) is dict:
                required = ("OP8-SHAPE-KEYSET",)
            elif type(original) is list:
                required = ("OP8-SHAPE-COUNT",)
            if len(path) >= 4 and path[-1] == "kind" and \
                    path[:3] == kind_prefix:
                required += (
                    "OP8-SHAPE-FIXTURE-KIND-VALUE"
                    if type(replacement) is str
                    else "OP8-SHAPE-FIXTURE-KIND-TYPE",
                )
            add(
                heterogeneous,
                f"heterogeneous {variant_name} at {_format_path(path)}",
                lambda c, p=path, r=copy.deepcopy(replacement):
                    _replace_path(c, p, r),
                required,
            )

    for label, candidate, expected_codes, required in targeted + heterogeneous:
        _assert_v9_case(
            failures, label, candidate, expected_codes, context, required)

    parser_count = 0
    integer_4300 = b"1" * 4300
    integer_value_4300 = _decimal_digits_to_int("1" * 4300)
    parser_values = [
        ("integer 4300-digit boundary", integer_4300, integer_value_4300, int),
        ("negative integer 4300-digit boundary", b"-" + integer_4300,
         -integer_value_4300, int),
        ("finite negative float/exponent", b"-1.5e-2", -0.015, float),
        ("float significand 4300-digit boundary", b"0." + b"1" * 4299,
         float((b"0." + b"1" * 4299).decode("ascii")), float),
        ("negative exponent lower boundary", b"-1e-4300", -0.0, float),
    ]
    for label, raw, expected_value, expected_type in parser_values:
        _assert_parser_value(
            failures, label, raw, expected_value, expected_type)
        parser_count += 1
    node_inner = b"[" + b",".join([b"0"] * MAX_ARRAY_ITEMS) + b"]"
    node_bound_raw = b"[" + b",".join([node_inner] * 10) + b"]"
    parser_errors = [
        ("integer 4301-digit", b"1" * 4301, "OP8-NUMERIC-INTEGER-DIGITS"),
        ("integer 5000-digit", b"1" * 5000, "OP8-NUMERIC-INTEGER-DIGITS"),
        ("negative integer 4301-digit", b"-" + b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS"),
        ("negative integer 5000-digit", b"-" + b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS"),
        ("float significand 4301 digits", b"0." + b"1" * 4300,
         "OP8-NUMERIC-FLOAT-DIGITS"),
        ("positive exponent finite-range overflow", b"1e4300",
         "OP8-NUMERIC-NONFINITE"),
        ("positive exponent magnitude overflow", b"1e4301",
         "OP8-NUMERIC-EXPONENT"),
        ("negative exponent magnitude overflow", b"-1e-4301",
         "OP8-NUMERIC-EXPONENT"),
        ("five-digit exponent token", b"1e00001", "OP8-NUMERIC-EXPONENT"),
        ("NaN", b"NaN", "OP8-NUMERIC-CONSTANT"),
        ("Infinity", b"Infinity", "OP8-NUMERIC-CONSTANT"),
        ("negative Infinity", b"-Infinity", "OP8-NUMERIC-CONSTANT"),
        ("invalid leading zero", b"01", "OP8-JSON-SYNTAX"),
        ("invalid trailing decimal", b"1.", "OP8-JSON-SYNTAX"),
        ("invalid leading decimal", b".1", "OP8-JSON-SYNTAX"),
        ("invalid empty exponent", b"1e", "OP8-JSON-SYNTAX"),
        ("duplicate key", b'{"x":1,"x":2}', "OP8-JSON-DUPLICATE"),
        ("malformed UTF-8", b'"\xff"', "OP8-JSON-UTF8"),
        ("depth bound", b"[" * 66 + b"0" + b"]" * 66, "OP8-LIMIT-DEPTH"),
        ("array bound", b"[" + b",".join([b"0"] * 10001) + b"]",
         "OP8-LIMIT-ARRAY"),
        ("object bound", b"{" + b",".join(
            f'"k{i}":0'.encode("ascii") for i in range(10001)) + b"}",
         "OP8-LIMIT-OBJECT"),
        ("node count bound", node_bound_raw, "OP8-LIMIT-NODES"),
        ("string bound", b'"' + b"x" * (MAX_STRING_UTF8_BYTES + 1) + b'"',
         "OP8-LIMIT-STRING"),
        ("key bound", b'{"' + b"x" * (MAX_STRING_UTF8_BYTES + 1) + b'":0}',
         "OP8-LIMIT-STRING"),
        ("raw bound", b" " * (MAX_RAW_BYTES + 1), "OP8-LIMIT-RAW"),
    ]
    for label, raw, expected_code in parser_errors:
        _assert_parser_error(failures, label, raw, expected_code)
        parser_count += 1

    api_cases: list[tuple[str, Any, tuple[str, ...]]] = [
        ("API null root", None, ("OP9-TOTALITY-ROOT",)),
        ("API boolean root", True, ("OP9-TOTALITY-ROOT",)),
        ("API integer root", 7, ("OP9-TOTALITY-ROOT",)),
        ("API float root", 7.5, ("OP9-TOTALITY-ROOT",)),
        ("API string root", "hostile", ("OP9-TOTALITY-ROOT",)),
        ("API array root", [], ("OP9-TOTALITY-ROOT",)),
        ("API empty object", {}, ("OP9-FULL", "OP9-SHAPE-SUCCESSOR")),
        ("API nonfinite", float("nan"), ("OP8-NUMERIC-NONFINITE",)),
        ("API non-JSON tuple", ("tuple",), ("OP8-TOTALITY-NONJSON",)),
        ("API over-bound integer", INTEGER_ABS_LIMIT,
         ("OP8-NUMERIC-INTEGER-DIGITS",)),
        ("API negative over-bound integer", -INTEGER_ABS_LIMIT,
         ("OP8-NUMERIC-INTEGER-DIGITS",)),
        ("API non-string object key", {7: None}, ("OP8-TOTALITY-KEY",)),
        ("API non-scalar Unicode string", "\ud800", ("OP8-TOTALITY-UNICODE",)),
    ]
    deep: Any = "leaf"
    for _ in range(MAX_DEPTH + 2):
        deep = [deep]
    cyclic: list[Any] = []
    cyclic.append(cyclic)
    api_cases.extend([
        ("API depth bound", deep, ("OP8-LIMIT-DEPTH",)),
        ("API array bound", [None] * (MAX_ARRAY_ITEMS + 1),
         ("OP8-LIMIT-ARRAY",)),
        ("API object bound", {f"k{i}": None for i in range(MAX_OBJECT_MEMBERS + 1)},
         ("OP8-LIMIT-OBJECT",)),
        ("API node bound", [[0] * MAX_ARRAY_ITEMS for _ in range(10)],
         ("OP8-LIMIT-NODES",)),
        ("API string bound", "x" * (MAX_STRING_UTF8_BYTES + 1),
         ("OP8-LIMIT-STRING",)),
        ("API key bound", {"x" * (MAX_STRING_UTF8_BYTES + 1): None},
         ("OP8-LIMIT-STRING",)),
        ("API cyclic array", cyclic, ("OP8-TOTALITY-NONTREE",)),
    ])
    for label, candidate, expected_codes in api_cases:
        _assert_v9_case(
            failures, label, candidate, expected_codes, context, expected_codes)

    cli_count = _cli_controls_v9(failures, value)
    oracle_counts = _oracle_regression_controls(failures)
    isolation_count = _isolation_controls(failures)
    trust_count = _trust_controls(failures)
    return failures, {
        "targeted": len(targeted),
        "heterogeneous": len(heterogeneous),
        "parser": parser_count,
        "api": len(api_cases),
        "cli": cli_count,
        "oracleInjected": oracle_counts["injected"],
        "oracleRejected": oracle_counts["rejected"],
        "oracleMutantsKilled": oracle_counts["mutantsKilled"],
        "isolation": isolation_count,
        "trust": trust_count,
        "mutationEscape": len(escape_probe),
    }


def main(argv: list[str]) -> int:
    allowed_flags = {"--selftest", "--machine"}
    unknown_flags = [arg for arg in argv[1:] if arg.startswith("-") and
                     arg not in allowed_flags]
    positional = [arg for arg in argv[1:] if arg not in allowed_flags and
                  not arg.startswith("-")]
    machine = "--machine" in argv[1:]
    run_selftest = "--selftest" in argv[1:]
    if unknown_flags or len(positional) > 1:
        records = [_finding("OP9-ARGS", "unsupported arguments")]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print("FAIL: OP9-ARGS: unsupported arguments")
        return 2
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        raw = path.read_bytes()
    except OSError:
        records = [_finding("OP9-IO", "cannot read candidate")]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print("FAIL: OP9-IO: cannot read candidate")
        return 2
    try:
        value = strict_loads(raw)
    except ControlledInputError as exc:
        records = [_finding(exc.code, exc.detail)]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print(f"FAIL: {exc.code}: {exc.detail}")
        return 2
    context, dependency_errors = authenticated_context()
    if dependency_errors or context is None:
        records = _records_from_text(
            dependency_errors or ["OP9-DEP-CONTEXT: context unavailable"],
            "v9 dependency authenticator")
        if machine:
            _emit_machine("FAIL", _unique_records(records))
        else:
            if run_selftest:
                print("REFUSING selftest: OPERABILITY v9 base/dependency closure is dirty")
            for record in _unique_records(records):
                print(f"FAIL: {record['code']}: {record['detail']}")
        return 1
    records = check(value, verify_files=False, context=context)
    if records:
        if machine:
            _emit_machine("FAIL", records)
        else:
            if run_selftest:
                print("REFUSING selftest: OPERABILITY v9 base/dependency closure is dirty")
            for record in records:
                print(f"FAIL: {record['code']}: {record['detail']}")
        return 1
    artifact_hash = _digest(raw)
    if run_selftest:
        failures, counts = selftest(value, context)
        if failures:
            record = _finding(
                "OP9-SELFTEST-FAIL",
                f"{len(failures)} failure(s); first: {failures[0]}")
            if machine:
                _emit_machine("FAIL", [record])
            else:
                for failure in failures:
                    print(f"SELFTEST-FAIL: {failure}")
            return 1
        if machine:
            _emit_machine("PASS", [], artifact_hash, counts)
        else:
            print(
                f"PASS: operability.v9.json@sha256:{artifact_hash}; "
                f"{counts['targeted']} targeted mutations, "
                f"{counts['heterogeneous']} systematic heterogeneous replacements, "
                f"{counts['parser']} parser/token controls, "
                f"{counts['api']} bounded API controls, "
                f"{counts['cli']} structural CLI controls, "
                f"{counts['oracleInjected']} injected oracle controls with "
                f"{counts['oracleMutantsKilled']} mutants killed, "
                f"{counts['isolation']} isolation controls, and "
                f"{counts['trust']} trust-order/cache/path controls rejected")
    else:
        if machine:
            _emit_machine("PASS", [], artifact_hash, None)
        else:
            print(
                f"PASS: operability.v9.json@sha256:{artifact_hash}; exact "
                "OP9->OP8->OP7->OP6->OP5->OP2 projection; complete "
                "EventEnvelopeV3/numeric/shape semantics object-identical; 13/13 "
                "dependencies authenticated before verified-buffer compilation; "
                "structural exact-code oracle and isolated startup required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
