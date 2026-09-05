#!/usr/bin/env python3
"""Validate OPERABILITY v8, a deterministic-totality successor over rejected v7.

The checker authenticates every lineage byte before compiling executable source,
parses JSON numbers through explicit pre-conversion callbacks, validates nested
types before aggregate/hash/index operations, and proves the exact
OP8 -> OP7 -> OP6 -> OP5 -> protected OP2 projection.  Candidate validation has
no catch-all exception oracle: a checker defect is a test failure, never evidence
that malformed input was rejected.

Usage: python3 -B check-operability-v8.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import pathlib
import py_compile
import re
import subprocess
import sys
import tempfile
import types
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v8.json"
PINS = {
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
    "check-operability-v7.py": "op7_rejected_verified_for_op8",
    "check-operability-v6.py": "op6_rejected_verified_for_op8",
    "check-operability-v5.py": "op5_verified_for_op8",
    "check-operability.py": "op2_verified_for_op8",
}
ROOT_ENVELOPE = ("version", "status", "supersedes", "author", "reviewStatus")
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
FORBIDDEN_SELFTEST_TOKENS = (
    "OP7-TOTALITY-INTERNAL", "OP8-INTERNAL", "INTERNAL", "EXCEPTION",
    "TRACEBACK", "TypeError",
)

V8_ROOT = {
    "version": 8,
    "status": "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REREVIEW (numeric-parser and validation-order totality-only successor over frozen/rejected v7; EventEnvelopeV3 semantics unchanged)",
    "supersedes": {
        "artifact": "operability.v7.json",
        "sha256": PINS["operability.v7.json"],
        "checker": "check-operability-v7.py",
        "checkerSha256": PINS["check-operability-v7.py"],
    },
    "author": "agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane; EventEnvelopeV3 binding successor by operability-v6 lane; totality-only successor by operability-v7 lane; deterministic numeric-totality successor by operability-v8 lane",
    "reviewStatus": "OPERABILITY v7 exact bytes were independently REJECTED for OP7-IR-01-NUMERIC-PARSER-TOTALITY and OP7-IR-02-VALIDATION-ORDER. OPERABILITY v8 preserves the complete v7 artifact, inherited EventEnvelopeV3 lifecycle, store-provenance content, and predecessor metadata exactly, and adds only closed numeric-token/validation-order declarations, exact rejection binding, successor metadata, and checker mechanics/tests. v8 is NOT-APPLIED and awaits independent rereview; no product, integration, application, acceptance, seal, or release authority is claimed.",
}

# Filled from the authored v8 artifact and held as immutable source text.  It is
# parsed by this checker's own closed parser, never read from the candidate.
EXPECTED_V8_METADATA_JSON = r'''{"id":"OPERABILITY-V8-DETERMINISTIC-TOTALITY-ONLY-SUCCESSOR","applicationState":"NOT-APPLIED","authorityClaim":"NONE","predecessorDisposition":"REJECT-EXACT-BYTES","rejectionBinding":{"artifact":"operability.v7.review-independent-prefreeze.json","sha256":"194e92128886fc8f11a1b513f597b79a91647732bb5a04772503379c228d10a4","reviewedCandidate":{"artifact":"operability.v7.json","sha256":"30d038363e94dc84766c43d3c28bf9a4e9fa7701fcb76a3ead942a210533eebd","checker":"check-operability-v7.py","checkerSha256":"6e7163871087be56e2d89e1911992870097f966fd2a7d728ab3d84ca06bf1832"},"verdict":"REJECT","blockingFindingIds":["OP7-IR-01-NUMERIC-PARSER-TOTALITY","OP7-IR-02-VALIDATION-ORDER"]},"requiredIndependentRereview":{"state":"REQUIRED","scope":["the complete frozen OPERABILITY v7 object, including the inherited object-identical EventEnvelopeV3 lifecycle and v7-to-v6-to-v5-to-v2 chain","the v8 deterministic numeric parser, validation-before-membership repair, exact-code selftest oracle, rejection binding, and exact v8-to-v7 projection"],"rule":"The rejected v7 checker and this authored v8 checker are design-integrity evidence only. Independent rereview must cover the complete semantic slice and every totality adversary on the exact replacement bytes before any application, acceptance, promotion, or seal."},"localDependencyClosure":{"operability.v7.json":{"kind":"rejected-predecessor-data","sha256":"30d038363e94dc84766c43d3c28bf9a4e9fa7701fcb76a3ead942a210533eebd"},"check-operability-v7.py":{"kind":"rejected-predecessor-executable-source","sha256":"6e7163871087be56e2d89e1911992870097f966fd2a7d728ab3d84ca06bf1832"},"operability.v7.review-independent-prefreeze.json":{"kind":"rejection-review-data","sha256":"194e92128886fc8f11a1b513f597b79a91647732bb5a04772503379c228d10a4"},"operability.v6.json":{"kind":"protected-lineage-data","sha256":"12d9f072c25a3efb789a05a1c513dfbc2aaf6612a234b23a8cf82ae027d9acb3"},"check-operability-v6.py":{"kind":"protected-lineage-executable-source","sha256":"2bd5e41d128388f50bb3d1518eb8e460d6987518dd71dcc350a7bc202b7407bd"},"operability.v6.review-independent-prefreeze.json":{"kind":"protected-lineage-rejection-review-data","sha256":"c34d304245a0dc932aae24d8b4283da6e7691bff45b4eb5e3b8ede9ab2c24ad7"},"operability.v5.json":{"kind":"protected-lineage-data","sha256":"89a18ffde1df3255b6a766aa74d1ad496ee3c7ed09cf5d69aa0ef34451699d8f"},"check-operability-v5.py":{"kind":"protected-lineage-executable-source","sha256":"047afb978bc02b62402e4036bb42659a7ac14d427408ef06d59d8a8d7438ef70"},"operability.v2.json":{"kind":"protected-base-data","sha256":"43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04"},"check-operability.py":{"kind":"protected-base-executable-source","sha256":"925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2"}},"closedTotalityDeclarations":{"jsonInputBounds":{"maxRawBytes":2000000,"maxDepth":64,"maxNodes":100000,"maxArrayItems":10000,"maxObjectMembers":10000,"maxStringUtf8Bytes":1048576},"numericTokenPolicy":{"grammar":"Only the RFC 8259 JSON number grammar is accepted. Integer, float/exponent, and nonstandard-constant tokens are inspected by parser callbacks before numeric conversion.","integer":{"maxDecimalDigitsExcludingSign":4300,"negativeValues":"PERMITTED; an optional leading minus is not a decimal digit","conversion":"After grammar and digit-count validation, accumulate base 10 from chunks of at most 9 digits; never call int on the complete token and never depend on ambient int_max_str_digits.","overBoundFinding":"OP8-NUMERIC-INTEGER-DIGITS"},"floatOrExponent":{"maxSignificandDecimalDigits":4300,"maxExponentDecimalDigits":4,"maxAbsoluteExponent":4300,"negativeValues":"PERMITTED for the significand and exponent within the same closed bounds","finiteBinary64Result":"REQUIRED","conversion":"Validate grammar, significand digits, exponent digits, and exponent magnitude before float conversion; reject every nonfinite conversion result.","overBoundSignificandFinding":"OP8-NUMERIC-FLOAT-DIGITS","overBoundExponentFinding":"OP8-NUMERIC-EXPONENT","nonfiniteFinding":"OP8-NUMERIC-NONFINITE"},"nonstandardConstants":{"acceptedTokens":[],"rejectedTokens":["NaN","Infinity","-Infinity"],"finding":"OP8-NUMERIC-CONSTANT"},"invalidJsonNumberFinding":"OP8-JSON-SYNTAX","runtimeIndependenceRule":"Every token is accepted or rejected by these declared bounds before an ambient runtime conversion limit can act. Parser refusal always produces the declared named CLI finding with no traceback."},"fixtureKind":{"path":"aPrimeSuccessor.lifecycle.bindingFixtures[*].kind","exactFixtureCount":8,"type":"string","closedValues":["event-envelope","phase-plane-bindings"],"validationOrder":"Validate string type before closed-value membership, dictionary lookup, set construction, hashing, or branch dispatch.","nonStringFinding":"OP8-SHAPE-FIXTURE-KIND-TYPE","unknownStringFinding":"OP8-SHAPE-FIXTURE-KIND-VALUE"},"nestedConsumerRule":"For every consumed nested value, validate its container and member type before joins, set construction, hash lookup, membership, indexing, or predecessor checker invocation. A non-exact candidate returns named shape/full findings before projection or inherited execution.","selftestOracle":{"required":"Every adversarial vector declares and receives its exact expected named invariant/code.","forbiddenOutcomes":["OP7-TOTALITY-INTERNAL","OP8-INTERNAL","INTERNAL","EXCEPTION","TRACEBACK","caught TypeError"],"nonemptyArbitraryFindingSufficient":false,"noOpOrFailureToApplyMutation":"SELFTEST-FAIL/ESCAPE","unexpectedFindingOnly":"SELFTEST-FAIL/ESCAPE"}},"v8ToV7Projection":{"id":"OP8-TO-OP7-EXACT-PROJECTION","predecessor":{"artifact":"operability.v7.json","sha256":"30d038363e94dc84766c43d3c28bf9a4e9fa7701fcb76a3ead942a210533eebd","checker":"check-operability-v7.py","checkerSha256":"6e7163871087be56e2d89e1911992870097f966fd2a7d728ab3d84ca06bf1832"},"algorithm":"Delete aPrimeSuccessor.operabilityV8Successor; restore the five root successor envelope fields from changedRootFields.before; canonical deep-compare the complete result to exact operability.v7.json bytes.","changedRootFields":{"version":{"before":7,"after":8},"status":{"before":"CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REREVIEW (totality-only successor over rejected v6; EventEnvelopeV3 semantics unchanged)","after":"CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REREVIEW (numeric-parser and validation-order totality-only successor over frozen/rejected v7; EventEnvelopeV3 semantics unchanged)"},"supersedes":{"before":{"artifact":"operability.v6.json","sha256":"12d9f072c25a3efb789a05a1c513dfbc2aaf6612a234b23a8cf82ae027d9acb3","checker":"check-operability-v6.py","checkerSha256":"2bd5e41d128388f50bb3d1518eb8e460d6987518dd71dcc350a7bc202b7407bd"},"after":{"artifact":"operability.v7.json","sha256":"30d038363e94dc84766c43d3c28bf9a4e9fa7701fcb76a3ead942a210533eebd","checker":"check-operability-v7.py","checkerSha256":"6e7163871087be56e2d89e1911992870097f966fd2a7d728ab3d84ca06bf1832"}},"author":{"before":"agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane; EventEnvelopeV3 binding successor by operability-v6 lane; totality-only successor by operability-v7 lane","after":"agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane; EventEnvelopeV3 binding successor by operability-v6 lane; totality-only successor by operability-v7 lane; deterministic numeric-totality successor by operability-v8 lane"},"reviewStatus":{"before":"OPERABILITY v6 exact bytes were independently REJECTED for OP6-IR-01-MALFORMED-TOTALITY. OPERABILITY v7 preserves the complete v6 EventEnvelopeV3 semantic object and all inherited lifecycle/store-provenance content exactly, and adds only closed totality shape declarations, rejection binding, successor metadata, and checker tests. v7 is NOT-APPLIED and awaits independent rereview; no product, integration, application, seal, or release authority is claimed.","after":"OPERABILITY v7 exact bytes were independently REJECTED for OP7-IR-01-NUMERIC-PARSER-TOTALITY and OP7-IR-02-VALIDATION-ORDER. OPERABILITY v8 preserves the complete v7 artifact, inherited EventEnvelopeV3 lifecycle, store-provenance content, and predecessor metadata exactly, and adds only closed numeric-token/validation-order declarations, exact rejection binding, successor metadata, and checker mechanics/tests. v8 is NOT-APPLIED and awaits independent rereview; no product, integration, application, acceptance, seal, or release authority is claimed."}},"removedSuccessorMetadata":["aPrimeSuccessor.operabilityV8Successor"],"deepEqualityRule":"The projection removes only the v8 successor metadata and restores only the five root successor fields. The complete frozen v7 object, inherited v6 EventEnvelopeV3 lifecycle/bindings/fixtures, store-provenance semantics, G19/CD-RT-5 state, and v7-to-v6-to-v5-to-v2 projections remain object-identical.","inheritedProjectionRule":"Exact OP8-to-OP7 projection must chain through unchanged OP7-to-OP6, OP6-to-OP5, and OP5-to-OP2 projections."}}'''
_EXPECTED_V8_METADATA_CACHE: dict[str, Any] | None = None


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


def authenticated_context() -> tuple[dict[str, Any] | None, list[str]]:
    """Authenticate the complete ten-file closure before any source execution."""
    errors: list[str] = []
    buffers: dict[str, bytes] = {}
    for name, expected in PINS.items():
        try:
            raw = (HERE / name).read_bytes()
        except OSError:
            errors.append(f"OP8-DEP-READ: cannot read {name}")
            continue
        buffers[name] = raw
        actual = _digest(raw)
        if actual != expected:
            errors.append(f"OP8-DEP-HASH: {name} hash {actual} != {expected}")
    if errors or tuple(buffers) != tuple(PINS):
        return None, errors or ["OP8-DEP-CLOSURE: dependency closure is incomplete"]

    data_names = (
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
            errors.append(f"OP8-DEP-PARSE: {name}: {exc.code}")
    if errors:
        return None, errors

    v7_review = parsed["operability.v7.review-independent-prefreeze.json"]
    v6_review = parsed["operability.v6.review-independent-prefreeze.json"]
    if not _review_bindings_valid(v7_review, v6_review):
        return None, ["OP8-REVIEW: exact v7/v6 rejection binding is not closed"]

    modules: dict[str, Any] = {}
    for filename, module_name in EXECUTABLE_DEPENDENCIES.items():
        modules[filename] = _compile_verified(
            buffers[filename], filename, module_name)

    v7mod = modules["check-operability-v7.py"]
    v6mod = modules["check-operability-v6.py"]
    v5mod = modules["check-operability-v5.py"]
    v2mod = modules["check-operability.py"]
    for label, module, binding in (
            ("OP7", v7mod, "operability.v7.json"),
            ("OP6", v6mod, "operability.v6.json"),
            ("OP5", v5mod, "operability.v5.json"),
            ("OP2", v2mod, "operability.v2.json")):
        if getattr(module, "BINDING", None) != binding or \
                not callable(getattr(module, "check", None)):
            errors.append(f"OP8-DEP-SURFACE: verified {label} checker is incomplete")
    if not callable(getattr(v7mod, "project_v6", None)) or \
            not callable(getattr(v6mod, "project_v5", None)) or \
            not callable(getattr(v5mod, "project_op2", None)):
        errors.append("OP8-DEP-SURFACE: predecessor projection chain is incomplete")
    if errors:
        return None, errors

    v7 = parsed["operability.v7.json"]
    v6 = parsed["operability.v6.json"]
    v5 = parsed["operability.v5.json"]
    v2 = parsed["operability.v2.json"]
    if v7mod.project_v6(v7) != v6:
        errors.append("OP8-DEP-PROJECTION: exact OP7 does not project to exact OP6")
    if v6mod.project_v5(v6) != v5:
        errors.append("OP8-DEP-PROJECTION: exact OP6 does not project to exact OP5")
    if v5mod.project_op2(v5) != v2:
        errors.append("OP8-DEP-PROJECTION: exact OP5 does not project to protected OP2")
    if errors:
        return None, errors
    context = {
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
    }
    context["expected_v8"] = construct_expected_v8(v7)
    return context, []


def expected_dependency_closure() -> dict[str, dict[str, str]]:
    kinds = {
        "operability.v7.json": "rejected-predecessor-data",
        "check-operability-v7.py": "rejected-predecessor-executable-source",
        "operability.v7.review-independent-prefreeze.json": "rejection-review-data",
        "operability.v6.json": "protected-lineage-data",
        "check-operability-v6.py": "protected-lineage-executable-source",
        "operability.v6.review-independent-prefreeze.json": "protected-lineage-rejection-review-data",
        "operability.v5.json": "protected-lineage-data",
        "check-operability-v5.py": "protected-lineage-executable-source",
        "operability.v2.json": "protected-base-data",
        "check-operability.py": "protected-base-executable-source",
    }
    return {
        name: {"kind": kinds[name], "sha256": digest}
        for name, digest in PINS.items()
    }


def expected_v8_metadata() -> dict[str, Any]:
    global _EXPECTED_V8_METADATA_CACHE
    if _EXPECTED_V8_METADATA_CACHE is None:
        parsed = strict_loads(EXPECTED_V8_METADATA_JSON.encode("utf-8"))
        if type(parsed) is not dict:
            raise AssertionError("authored v8 metadata literal is not an object")
        _EXPECTED_V8_METADATA_CACHE = parsed
    return copy.deepcopy(_EXPECTED_V8_METADATA_CACHE)


def construct_expected_v8(v7: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(v7)
    for key, value in V8_ROOT.items():
        result[key] = copy.deepcopy(value)
    result["aPrimeSuccessor"]["operabilityV8Successor"] = expected_v8_metadata()
    return result


def project_v7(candidate: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(candidate)
    successor = result["aPrimeSuccessor"]
    metadata = successor["operabilityV8Successor"]
    projection = metadata["v8ToV7Projection"]
    if set(projection["changedRootFields"]) != set(ROOT_ENVELOPE):
        raise ValueError("v8-to-v7 root envelope is not closed")
    if projection["removedSuccessorMetadata"] != [
            "aPrimeSuccessor.operabilityV8Successor"]:
        raise ValueError("v8-to-v7 metadata removal is not exact")
    successor.pop("operabilityV8Successor")
    for key in ROOT_ENVELOPE:
        result[key] = copy.deepcopy(projection["changedRootFields"][key]["before"])
    return result


def _string_array_findings(value: Any, path: str, *, exact_count: int | None = None,
                           allow_empty_items: bool = False) -> list[str]:
    if type(value) is not list:
        return [f"OP8-SHAPE-STRING-ARRAY: {path} must be an array"]
    findings: list[str] = []
    if exact_count is not None and len(value) != exact_count:
        findings.append(
            f"OP8-SHAPE-STRING-ARRAY: {path} count must equal {exact_count}")
    validated: list[str] = []
    for index, item in enumerate(value):
        if type(item) is not str or (not allow_empty_items and not item.strip()):
            findings.append(
                f"OP8-SHAPE-STRING-ARRAY: {path}[{index}] must be a nonempty string")
        else:
            validated.append(item)
    if len(validated) == len(value):
        if len(validated) != len(set(validated)):
            findings.append(f"OP8-SHAPE-STRING-ARRAY: {path} contains duplicates")
    return findings


def _projection_shape_findings(meta: dict[str, Any], name: str,
                               label: str) -> list[str]:
    findings: list[str] = []
    projection = meta.get(name)
    if type(projection) is not dict:
        return [f"OP8-SHAPE-PROJECTION: {label} must be an object"]
    changed = projection.get("changedRootFields")
    if type(changed) is not dict:
        findings.append(
            f"OP8-SHAPE-PROJECTION: {label}.changedRootFields must be an object")
    else:
        keys_valid = all(type(key) is str for key in changed)
        if not keys_valid or set(changed) != set(ROOT_ENVELOPE):
            findings.append(
                f"OP8-SHAPE-PROJECTION: {label}.changedRootFields keys are not closed")
        for key in ROOT_ENVELOPE:
            row = changed.get(key)
            if type(row) is not dict or "before" not in row or "after" not in row:
                findings.append(
                    f"OP8-SHAPE-PROJECTION: {label}.changedRootFields.{key} is malformed")
    findings.extend(_string_array_findings(
        projection.get("removedSuccessorMetadata"),
        f"{label}.removedSuccessorMetadata", exact_count=1))
    if name == "v6ToV5Projection":
        findings.extend(_string_array_findings(
            projection.get("removedLifecycleFields"),
            f"{label}.removedLifecycleFields", exact_count=3))
    return findings


def _closure_shape_findings(meta: dict[str, Any], label: str,
                            expected_count: int) -> list[str]:
    closure = meta.get("localDependencyClosure")
    if type(closure) is not dict or len(closure) != expected_count:
        return [
            f"OP8-SHAPE-CLOSURE: {label} must be a {expected_count}-member object"]
    findings: list[str] = []
    for name, row in closure.items():
        if type(name) is not str or not name:
            findings.append(f"OP8-SHAPE-CLOSURE: {label} key must be a string")
        if type(row) is not dict:
            findings.append(f"OP8-SHAPE-CLOSURE: {label}.{name} must be an object")
            continue
        if type(row.get("kind")) is not str or type(row.get("sha256")) is not str:
            findings.append(
                f"OP8-SHAPE-CLOSURE: {label}.{name} kind/sha256 must be strings")
    return findings


def _review_shape_findings(meta: dict[str, Any], field: str,
                           label: str) -> list[str]:
    review = meta.get(field)
    if type(review) is not dict:
        return [f"OP8-SHAPE-REVIEW: {label} must be an object"]
    findings: list[str] = []
    if review.get("state") != "REQUIRED":
        findings.append(f"OP8-SHAPE-REVIEW: {label}.state must equal REQUIRED")
    findings.extend(_string_array_findings(
        review.get("scope"), f"{label}.scope", exact_count=2))
    if type(review.get("rule")) is not str or not review.get("rule").strip():
        findings.append(f"OP8-SHAPE-REVIEW: {label}.rule must be a nonempty string")
    return findings


def _v8_totality_metadata_shape_findings(meta: dict[str, Any]) -> list[str]:
    rejection = meta.get("rejectionBinding")
    findings: list[str] = []
    if type(rejection) is not dict:
        findings.append("OP8-SHAPE-REJECTION: rejectionBinding must be an object")
    else:
        findings.extend(_string_array_findings(
            rejection.get("blockingFindingIds"),
            "rejectionBinding.blockingFindingIds", exact_count=2))
        reviewed = rejection.get("reviewedCandidate")
        if type(reviewed) is not dict:
            findings.append(
                "OP8-SHAPE-REJECTION: reviewedCandidate must be an object")
        else:
            for key in ("artifact", "sha256", "checker", "checkerSha256"):
                if type(reviewed.get(key)) is not str or not reviewed.get(key).strip():
                    findings.append(
                        f"OP8-SHAPE-REJECTION: reviewedCandidate.{key} must be a string")
    declarations = meta.get("closedTotalityDeclarations")
    if type(declarations) is not dict:
        findings.append(
            "OP8-SHAPE-TOTALITY-META: closedTotalityDeclarations must be an object")
        return findings
    bounds = declarations.get("jsonInputBounds")
    if type(bounds) is not dict:
        findings.append("OP8-SHAPE-TOTALITY-META: jsonInputBounds must be an object")
    else:
        for key in (
                "maxRawBytes", "maxDepth", "maxNodes", "maxArrayItems",
                "maxObjectMembers", "maxStringUtf8Bytes"):
            if type(bounds.get(key)) is not int or bounds.get(key) <= 0:
                findings.append(f"OP8-SHAPE-TOTALITY-META: {key} must be positive integer")
    numeric = declarations.get("numericTokenPolicy")
    if type(numeric) is not dict:
        findings.append("OP8-SHAPE-TOTALITY-META: numericTokenPolicy must be an object")
    else:
        integer = numeric.get("integer")
        floating = numeric.get("floatOrExponent")
        constants = numeric.get("nonstandardConstants")
        if type(integer) is not dict or type(integer.get(
                "maxDecimalDigitsExcludingSign")) is not int:
            findings.append("OP8-SHAPE-TOTALITY-META: integer policy is malformed")
        if type(floating) is not dict or any(type(floating.get(key)) is not int for key in (
                "maxSignificandDecimalDigits", "maxExponentDecimalDigits",
                "maxAbsoluteExponent")):
            findings.append("OP8-SHAPE-TOTALITY-META: float policy is malformed")
        if type(constants) is not dict:
            findings.append("OP8-SHAPE-TOTALITY-META: constant policy is malformed")
        else:
            findings.extend(_string_array_findings(
                constants.get("acceptedTokens"), "numeric.acceptedTokens",
                exact_count=0))
            findings.extend(_string_array_findings(
                constants.get("rejectedTokens"), "numeric.rejectedTokens",
                exact_count=3))
    fixture_kind = declarations.get("fixtureKind")
    if type(fixture_kind) is not dict:
        findings.append("OP8-SHAPE-TOTALITY-META: fixtureKind must be an object")
    else:
        findings.extend(_string_array_findings(
            fixture_kind.get("closedValues"), "fixtureKind.closedValues",
            exact_count=2))
    oracle = declarations.get("selftestOracle")
    if type(oracle) is not dict:
        findings.append("OP8-SHAPE-TOTALITY-META: selftestOracle must be an object")
    else:
        findings.extend(_string_array_findings(
            oracle.get("forbiddenOutcomes"), "selftestOracle.forbiddenOutcomes",
            exact_count=6))
        if type(oracle.get("nonemptyArbitraryFindingSufficient")) is not bool:
            findings.append(
                "OP8-SHAPE-TOTALITY-META: arbitrary-finding oracle must be boolean")
    return findings


def _lifecycle_shape_findings(lifecycle: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    schema = lifecycle.get("eventSchemaV3")
    if type(schema) is not dict:
        return ["OP8-SHAPE-EVENT-SCHEMA: eventSchemaV3 must be an object"]
    for key in ("required", "optional", "closedPlanes", "closedPhases"):
        findings.extend(_string_array_findings(
            schema.get(key), f"eventSchemaV3.{key}"))
    closed_phases = schema.get("closedPhases")
    closed_phase_strings = type(closed_phases) is list and all(
        type(item) is str and bool(item.strip()) for item in closed_phases)
    phase_requirements = schema.get("phaseRequirements")
    if type(phase_requirements) is not dict:
        findings.append(
            "OP8-SHAPE-EVENT-SCHEMA: phaseRequirements must be an object")
    else:
        if closed_phase_strings and set(phase_requirements) != set(closed_phases):
            findings.append(
                "OP8-SHAPE-EVENT-SCHEMA: phaseRequirements keys are not closed")
        for phase, row in phase_requirements.items():
            if type(phase) is not str or type(row) is not dict:
                findings.append(
                    f"OP8-SHAPE-EVENT-SCHEMA: phase requirement {phase} is malformed")
                continue
            for field in ("executionId", "runId", "budgetOwner"):
                if field in row and type(row.get(field)) is not str:
                    findings.append(
                        f"OP8-SHAPE-EVENT-SCHEMA: phaseRequirements.{phase}.{field} must be a string")
    if type(lifecycle.get("schemaVersionConstraint")) is not dict:
        findings.append(
            "OP8-SHAPE-EVENT-SCHEMA: schemaVersionConstraint must be an object")
    bindings = lifecycle.get("phasePlaneBindings")
    if type(bindings) is not dict:
        findings.append("OP8-SHAPE-BINDINGS: phasePlaneBindings must be an object")
    else:
        if closed_phase_strings and set(bindings) != set(closed_phases):
            findings.append("OP8-SHAPE-BINDINGS: phasePlaneBindings keys are not closed")
        for phase, plane in bindings.items():
            if type(phase) is not str or (plane is not None and type(plane) is not str):
                findings.append(
                    f"OP8-SHAPE-BINDINGS: phasePlaneBindings.{phase} value is malformed")

    fixtures = lifecycle.get("bindingFixtures")
    if type(fixtures) is not list:
        return findings + ["OP8-SHAPE-FIXTURE: bindingFixtures must be an array"]
    if len(fixtures) != 8:
        findings.append("OP8-SHAPE-FIXTURE: bindingFixtures count must equal 8")
    valid_ids: list[str] = []
    for index, row in enumerate(fixtures):
        prefix = f"bindingFixtures[{index}]"
        if type(row) is not dict:
            findings.append(f"OP8-SHAPE-FIXTURE: {prefix} must be an object")
            continue
        fixture_id = row.get("id")
        if type(fixture_id) is not str or not fixture_id.strip():
            findings.append(f"OP8-SHAPE-FIXTURE-ID: {prefix}.id must be a nonempty string")
        else:
            valid_ids.append(fixture_id)
        kind = row.get("kind")
        if type(kind) is not str:
            findings.append(
                f"OP8-SHAPE-FIXTURE-KIND-TYPE: {prefix}.kind must be a string")
            kind_is_event = False
            kind_is_bindings = False
        else:
            kind_is_event = kind == "event-envelope"
            kind_is_bindings = kind == "phase-plane-bindings"
            if not kind_is_event and not kind_is_bindings:
                findings.append(
                    f"OP8-SHAPE-FIXTURE-KIND-VALUE: {prefix}.kind is not closed")
        if type(row.get("valid")) is not bool:
            findings.append(f"OP8-SHAPE-FIXTURE-VALID: {prefix}.valid must be boolean")
        findings.extend(_string_array_findings(
            row.get("expectedErrors"), f"{prefix}.expectedErrors"))
        if kind_is_event:
            envelope = row.get("envelope")
            if type(envelope) is not dict:
                findings.append(
                    f"OP8-SHAPE-FIXTURE-ENVELOPE: {prefix}.envelope must be an object")
            else:
                for field in (
                        "plane", "phase", "requestId", "budgetOwner", "payloadType",
                        "executionId", "runId", "parentEventId"):
                    if field in envelope and type(envelope.get(field)) is not str:
                        findings.append(
                            f"OP8-SHAPE-FIXTURE-ENVELOPE: {prefix}.envelope.{field} must be a string")
                if "schemaVersion" in envelope and type(
                        envelope.get("schemaVersion")) is not int:
                    findings.append(
                        f"OP8-SHAPE-FIXTURE-ENVELOPE: {prefix}.envelope.schemaVersion must be integer")
                if "payloadBytes" in envelope and type(
                        envelope.get("payloadBytes")) is not int:
                    findings.append(
                        f"OP8-SHAPE-FIXTURE-ENVELOPE: {prefix}.envelope.payloadBytes must be integer")
        if kind_is_bindings:
            fixture_bindings = row.get("bindings")
            if type(fixture_bindings) is not dict:
                findings.append(
                    f"OP8-SHAPE-FIXTURE-BINDINGS: {prefix}.bindings must be an object")
            else:
                for phase, plane in fixture_bindings.items():
                    if type(phase) is not str or (plane is not None and type(plane) is not str):
                        findings.append(
                            f"OP8-SHAPE-FIXTURE-BINDINGS: {prefix}.bindings.{phase} is malformed")
    if len(valid_ids) == len(fixtures):
        if len(valid_ids) != len(set(valid_ids)):
            findings.append("OP8-SHAPE-FIXTURE-ID-DUPLICATE: fixture ids are duplicated")
    return findings


def shape_findings(value: Any) -> list[str]:
    """Validate every nested consumer before any type-sensitive operation."""
    if type(value) is not dict:
        return ["OP8-SHAPE-ROOT: root must be an object"]
    successor = value.get("aPrimeSuccessor")
    if type(successor) is not dict:
        return ["OP8-SHAPE-SUCCESSOR: aPrimeSuccessor must be an object"]
    lifecycle = successor.get("lifecycle")
    v6meta = successor.get("operabilityV6Successor")
    v7meta = successor.get("operabilityV7Successor")
    v8meta = successor.get("operabilityV8Successor")
    findings: list[str] = []
    for label, meta in (("v6", v6meta), ("v7", v7meta), ("v8", v8meta)):
        if type(meta) is not dict:
            findings.append(f"OP8-SHAPE-METADATA: {label} metadata must be an object")
    if type(lifecycle) is not dict:
        findings.append("OP8-SHAPE-LIFECYCLE: lifecycle must be an object")
    if findings:
        return findings

    findings.extend(_review_shape_findings(
        v6meta, "requiredIndependentCombinedReview", "v6 combined review"))
    findings.extend(_review_shape_findings(
        v7meta, "requiredIndependentRereview", "v7 independent rereview"))
    findings.extend(_review_shape_findings(
        v8meta, "requiredIndependentRereview", "v8 independent rereview"))
    findings.extend(_projection_shape_findings(
        v6meta, "v6ToV5Projection", "v6ToV5Projection"))
    findings.extend(_projection_shape_findings(
        v7meta, "v7ToV6Projection", "v7ToV6Projection"))
    findings.extend(_projection_shape_findings(
        v8meta, "v8ToV7Projection", "v8ToV7Projection"))
    findings.extend(_closure_shape_findings(v6meta, "v6 closure", 4))
    findings.extend(_closure_shape_findings(v7meta, "v7 closure", 7))
    findings.extend(_closure_shape_findings(v8meta, "v8 closure", 10))
    findings.extend(_v8_totality_metadata_shape_findings(v8meta))
    findings.extend(_lifecycle_shape_findings(lifecycle))
    return findings


def structural_delta_findings(value: Any, expected: Any) -> list[str]:
    """Name structural deviations without indexing through unvalidated shapes."""
    findings: list[str] = []
    stack: list[tuple[Any, Any, str]] = [(value, expected, "$")]
    while stack:
        actual, wanted, path = stack.pop()
        if type(actual) is not type(wanted):
            findings.append(
                f"OP8-SHAPE-TYPE: {path} expected {type(wanted).__name__}, "
                f"got {type(actual).__name__}")
            continue
        if type(actual) is dict:
            actual_keys = set(actual)
            wanted_keys = set(wanted)
            if actual_keys != wanted_keys:
                findings.append(f"OP8-SHAPE-KEYSET: {path} key set differs")
            for key in actual_keys & wanted_keys:
                stack.append((actual[key], wanted[key], _short_path(path, key)))
        elif type(actual) is list:
            if len(actual) != len(wanted):
                findings.append(f"OP8-SHAPE-COUNT: {path} item count differs")
            for index in range(min(len(actual), len(wanted))):
                stack.append((
                    actual[index], wanted[index], _short_path(path, index)))
    return findings


def _gate(root: Any, gate_id: str) -> dict[str, Any] | None:
    if type(root) is not dict or type(root.get("validationGates")) is not list:
        return None
    rows: list[dict[str, Any]] = []
    for row in root["validationGates"]:
        if type(row) is dict and row.get("id") == gate_id:
            rows.append(row)
    return rows[0] if len(rows) == 1 else None


def _check_impl(value: Any, *, verify_files: bool,
                context: dict[str, Any] | None) -> list[str]:
    bounded = json_value_findings(value)
    if bounded:
        return bounded
    if type(value) is not dict:
        return ["OP8-TOTALITY-ROOT: root must be an object"]
    if context is None:
        if not verify_files:
            return ["OP8-DEP-CONTEXT: unauthenticated context is forbidden"]
        context, dependency_errors = authenticated_context()
        if dependency_errors or context is None:
            return dependency_errors or ["OP8-DEP-CONTEXT: context unavailable"]
    if type(context) is not dict:
        return ["OP8-DEP-CONTEXT: authenticated context must be an object"]
    expected = context.get("expected_v8")
    v7 = context.get("v7")
    v6 = context.get("v6")
    v5 = context.get("v5")
    v2 = context.get("v2")
    v7mod = context.get("v7mod")
    v6mod = context.get("v6mod")
    v5mod = context.get("v5mod")
    if any(type(row) is not dict for row in (expected, v7, v6, v5, v2)) or \
            v7mod is None or v6mod is None or v5mod is None:
        return ["OP8-DEP-CONTEXT: authenticated context is malformed"]

    exact = value == expected
    findings: list[str] = []
    if not exact:
        findings.append("OP8-FULL: candidate differs from complete expected v8")
        findings.extend(structural_delta_findings(value, expected))
    findings.extend(shape_findings(value))
    # Candidate-derived projection, inherited checker calls, and deep indexing
    # are reserved for the exact fully-shaped object.
    if not exact or findings:
        return findings

    successor = value["aPrimeSuccessor"]
    v8meta = successor["operabilityV8Successor"]
    if any(value[key] != V8_ROOT[key] for key in ROOT_ENVELOPE):
        findings.append("OP8-META: closed root successor metadata drift")
    if v8meta != expected_v8_metadata():
        findings.append("OP8-META: complete v8 successor metadata drift")
    if v8meta["localDependencyClosure"] != expected_dependency_closure():
        findings.append("OP8-DEP-CLOSURE: declared ten-file closure drift")
    review = context["v7_review"]
    if v8meta["rejectionBinding"]["sha256"] != PINS[
            "operability.v7.review-independent-prefreeze.json"] or \
            v8meta["rejectionBinding"]["verdict"] != "REJECT" or \
            tuple(v8meta["rejectionBinding"]["blockingFindingIds"]) != \
            V7_REVIEW_FINDINGS or review["verdict"]["decision"] != "REJECT":
        findings.append("OP8-REVIEW: exact v7 rejection/verdict/findings binding drift")
    if successor["lifecycle"] != v7["aPrimeSuccessor"]["lifecycle"] or \
            successor["lifecycle"] != v6["aPrimeSuccessor"]["lifecycle"]:
        findings.append("OP8-SEMANTIC: EventEnvelopeV3 lifecycle object changed")
    if successor["operabilityV7Successor"] != \
            v7["aPrimeSuccessor"]["operabilityV7Successor"] or \
            successor["operabilityV6Successor"] != \
            v7["aPrimeSuccessor"]["operabilityV6Successor"]:
        findings.append("OP8-SEMANTIC: inherited successor metadata changed")

    projected_v7 = project_v7(value)
    if projected_v7 != v7:
        findings.append("OP8-PROJ: v8 does not project exact-deep-equal to v7")
    projected_v6 = v7mod.project_v6(projected_v7)
    if projected_v6 != v6:
        findings.append("OP8-PROJ: projected v7 does not project exact-deep-equal to v6")
    projected_v5 = v6mod.project_v5(projected_v6)
    if projected_v5 != v5:
        findings.append("OP8-PROJ: projected v6 does not project exact-deep-equal to v5")
    if v5mod.project_op2(projected_v5) != v2:
        findings.append("OP8-PROJ: projected v5 does not project exact-deep-equal to OP2")
    v6_context = {
        "op5": v5,
        "op2": v2,
        "op5mod": v5mod,
        "op2mod": context["v2mod"],
    }
    inherited_findings = v6mod.check(
        projected_v6, verify_files=False, context=v6_context)
    if inherited_findings:
        findings.append(
            f"OP8-INHERITED: exact v6 semantic checker red: {inherited_findings[0]}")
    if _gate(value, "G19") != _gate(v7, "G19") or \
            (_gate(value, "G19") or {}).get("status") != "BLOCKED-NO-MECHANISM":
        findings.append("OP8-G19: inherited gate changed or was promoted")
    return findings


def check(value: Any, *, verify_files: bool = True,
          context: dict[str, Any] | None = None) -> list[str]:
    """Total for built-in bounded JSON values; checker defects propagate."""
    return _check_impl(value, verify_files=verify_files, context=context)


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


def _codes(findings: list[str]) -> set[str]:
    return {finding.split(":", 1)[0] for finding in findings}


def _forbidden_findings(findings: list[str]) -> list[str]:
    return [
        finding for finding in findings
        if any(token.lower() in finding.lower() for token in FORBIDDEN_SELFTEST_TOKENS)
    ]


def _assert_check_case(failures: list[str], label: str, candidate: Any,
                       expected_codes: tuple[str, ...],
                       context: dict[str, Any]) -> None:
    try:
        findings = check(candidate, verify_files=False, context=context)
    except Exception as exc:
        failures.append(
            f"{label}: checker raised {type(exc).__name__}; exception is a failure")
        return
    forbidden = _forbidden_findings(findings)
    if forbidden:
        failures.append(f"{label}: forbidden internal/exception finding {forbidden[0]}")
    actual_codes = _codes(findings)
    for expected in expected_codes:
        if expected not in actual_codes:
            failures.append(
                f"{label}: expected {expected}, got {sorted(actual_codes)}")


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


def _cli_controls(failures: list[str], clean_value: dict[str, Any]) -> int:
    node_inner = b"[" + b",".join([b"0"] * MAX_ARRAY_ITEMS) + b"]"
    node_bound_raw = b"[" + b",".join([node_inner] * 10) + b"]"
    controls: list[tuple[str, bytes, str, int, dict[str, str]]] = [
        ("4300-digit integer", b"1" * 4300, "OP8-TOTALITY-ROOT", 1, {}),
        ("4300-digit integer/ambient-low", b"1" * 4300,
         "OP8-TOTALITY-ROOT", 1, {"PYTHONINTMAXSTRDIGITS": "640"}),
        ("4301-digit integer", b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {}),
        ("4301-digit integer/ambient-disabled", b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {"PYTHONINTMAXSTRDIGITS": "0"}),
        ("5000-digit integer/default", b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {}),
        ("5000-digit integer/ambient-disabled", b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {"PYTHONINTMAXSTRDIGITS": "0"}),
        ("5000-digit integer/ambient-low", b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {"PYTHONINTMAXSTRDIGITS": "640"}),
        ("negative 4301-digit integer", b"-" + b"1" * 4301,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {}),
        ("negative 5000-digit integer", b"-" + b"1" * 5000,
         "OP8-NUMERIC-INTEGER-DIGITS", 2, {}),
        ("float significand over bound", b"0." + b"1" * 4300,
         "OP8-NUMERIC-FLOAT-DIGITS", 2, {}),
        ("positive exponent nonfinite", b"1e4300",
         "OP8-NUMERIC-NONFINITE", 2, {}),
        ("positive exponent over bound", b"1e4301",
         "OP8-NUMERIC-EXPONENT", 2, {}),
        ("negative exponent over bound", b"-1e-4301",
         "OP8-NUMERIC-EXPONENT", 2, {}),
        ("NaN constant", b"NaN", "OP8-NUMERIC-CONSTANT", 2, {}),
        ("Infinity constant", b"Infinity", "OP8-NUMERIC-CONSTANT", 2, {}),
        ("negative Infinity constant", b"-Infinity", "OP8-NUMERIC-CONSTANT", 2, {}),
        ("invalid leading-zero number", b"01", "OP8-JSON-SYNTAX", 2, {}),
        ("duplicate object member", b'{"x":1,"x":2}',
         "OP8-JSON-DUPLICATE", 2, {}),
        ("malformed UTF-8", b'"\xff"', "OP8-JSON-UTF8", 2, {}),
        ("depth over bound", b"[" * 66 + b"0" + b"]" * 66,
         "OP8-LIMIT-DEPTH", 2, {}),
        ("array over bound", b"[" + b",".join([b"0"] * 10001) + b"]",
         "OP8-LIMIT-ARRAY", 2, {}),
        ("object over bound", b"{" + b",".join(
            f'"k{i}":0'.encode("ascii") for i in range(10001)) + b"}",
         "OP8-LIMIT-OBJECT", 2, {}),
        ("node count over bound", node_bound_raw,
         "OP8-LIMIT-NODES", 2, {}),
        ("string over bound",
         b'"' + b"x" * (MAX_STRING_UTF8_BYTES + 1) + b'"',
         "OP8-LIMIT-STRING", 2, {}),
        ("raw over bound", b" " * (MAX_RAW_BYTES + 1),
         "OP8-LIMIT-RAW", 2, {}),
    ]
    with tempfile.TemporaryDirectory(prefix="op8-cli-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        case_path = temp_dir / "case.json"
        for label, raw, expected_code, expected_exit, overrides in controls:
            case_path.write_bytes(raw)
            environment = os.environ.copy()
            environment.update(overrides)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            completed = subprocess.run(
                [sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
                 str(case_path)],
                capture_output=True,
                check=False,
                env=environment,
                timeout=30,
            )
            output = (completed.stdout + completed.stderr).decode(
                "utf-8", errors="replace")
            if completed.returncode != expected_exit:
                failures.append(
                    f"CLI {label}: exit {completed.returncode} != {expected_exit}")
            if f"{expected_code}:" not in output:
                failures.append(f"CLI {label}: missing exact code {expected_code}")
            if any(token.lower() in output.lower() for token in (
                    "traceback", "totality-internal", "typeerror", "exception")):
                failures.append(f"CLI {label}: forbidden traceback/internal outcome")

        dirty = copy.deepcopy(clean_value)
        dirty["status"] = "APPLIED"
        case_path.write_text(
            json.dumps(dirty, ensure_ascii=False), encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
             str(case_path), "--selftest"],
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            timeout=30,
        )
        output = (completed.stdout + completed.stderr).decode(
            "utf-8", errors="replace")
        if completed.returncode != 1 or \
                "REFUSING selftest: OPERABILITY v8 base/dependency closure is dirty" \
                not in output or "PASS:" in output:
            failures.append("CLI dirty base did not refuse selftest before mutation oracle")
    return len(controls) + 1


def _trust_controls(failures: list[str]) -> int:
    global HERE, _compile_verified
    count = 0
    poison_names = tuple(EXECUTABLE_DEPENDENCIES.values())
    saved_modules = {name: sys.modules.get(name) for name in poison_names}
    poison = types.ModuleType("op8_poison")
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
            context[key] is poison for key in ("v7mod", "v6mod", "v5mod", "v2mod")):
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
                error.startswith("OP8-DEP-HASH:") for error in dirty_errors) or \
                compile_calls:
            failures.append("trust dirty dependency did not fail before all compilation")
    count += 1
    return count


def selftest(value: dict[str, Any], context: dict[str, Any]) -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    targeted: list[tuple[str, Any, tuple[str, ...]]] = []
    heterogeneous: list[tuple[str, Any, tuple[str, ...]]] = []

    def add(target: list[tuple[str, Any, tuple[str, ...]]], label: str,
            mutate: Callable[[dict[str, Any]], None],
            expected_codes: tuple[str, ...]) -> None:
        candidate = copy.deepcopy(value)
        before = copy.deepcopy(candidate)
        try:
            mutate(candidate)
        except Exception as exc:
            failures.append(
                f"{label}: mutation failed to apply ({type(exc).__name__}); escape")
            return
        if candidate == before:
            failures.append(f"{label}: no-op mutation; escape")
            return
        target.append((label, candidate, expected_codes))

    v8meta = lambda c: c["aPrimeSuccessor"]["operabilityV8Successor"]
    lifecycle = lambda c: c["aPrimeSuccessor"]["lifecycle"]
    add(targeted, "status promotion", lambda c: c.__setitem__("status", "APPLIED"),
        ("OP8-FULL",))
    add(targeted, "rejection verdict erased",
        lambda c: v8meta(c)["rejectionBinding"].__setitem__("verdict", "PASS"),
        ("OP8-FULL",))
    add(targeted, "rejection finding erased",
        lambda c: v8meta(c)["rejectionBinding"]["blockingFindingIds"].pop(),
        ("OP8-FULL", "OP8-SHAPE-STRING-ARRAY"))
    add(targeted, "incomplete dependency closure",
        lambda c: v8meta(c)["localDependencyClosure"].pop(
            "operability.v7.review-independent-prefreeze.json"),
        ("OP8-FULL", "OP8-SHAPE-CLOSURE"))
    add(targeted, "weaken exact projection",
        lambda c: v8meta(c)["v8ToV7Projection"].__setitem__(
            "deepEqualityRule", "field presence"), ("OP8-FULL",))
    add(targeted, "numeric bound drift",
        lambda c: v8meta(c)["closedTotalityDeclarations"]["numericTokenPolicy"][
            "integer"].__setitem__("maxDecimalDigitsExcludingSign", 5000),
        ("OP8-FULL",))
    add(targeted, "false arbitrary-finding oracle",
        lambda c: v8meta(c)["closedTotalityDeclarations"]["selftestOracle"].__setitem__(
            "nonemptyArbitraryFindingSufficient", True), ("OP8-FULL",))
    add(targeted, "semantic schema version change",
        lambda c: lifecycle(c)["schemaVersionConstraint"].__setitem__("value", 4),
        ("OP8-FULL",))
    add(targeted, "semantic run-committed plane change",
        lambda c: lifecycle(c)["phasePlaneBindings"].__setitem__(
            "run-committed", "diagnostics"), ("OP8-FULL",))
    add(targeted, "review scope object counterexample",
        lambda c: c["aPrimeSuccessor"]["operabilityV6Successor"][
            "requiredIndependentCombinedReview"].__setitem__("scope", [{}]),
        ("OP8-FULL", "OP8-SHAPE-STRING-ARRAY"))
    add(targeted, "fixture id list counterexample",
        lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("id", []),
        ("OP8-FULL", "OP8-SHAPE-FIXTURE-ID"))
    add(targeted, "fixture id object counterexample",
        lambda c: lifecycle(c)["bindingFixtures"][0].__setitem__("id", {}),
        ("OP8-FULL", "OP8-SHAPE-FIXTURE-ID"))
    add(targeted, "duplicate fixture id",
        lambda c: lifecycle(c)["bindingFixtures"][1].__setitem__(
            "id", lifecycle(c)["bindingFixtures"][0]["id"]),
        ("OP8-FULL", "OP8-SHAPE-FIXTURE-ID-DUPLICATE"))

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
                ("OP8-FULL", expected),
            )

    variants: list[tuple[str, Any]] = [
        ("null", None), ("boolean", True), ("integer", 7), ("float", 7.5),
        ("string", "heterogeneous"), ("array", []),
        ("object", {"heterogeneous": True}),
    ]
    kind_suffix = ("aPrimeSuccessor", "lifecycle", "bindingFixtures")
    for path in heterogeneous_targets(value):
        original = _path_value(value, path)
        for variant_name, replacement in variants:
            if type(original) is type(replacement) and original == replacement:
                continue
            expected_codes = ("OP8-FULL",)
            if type(original) is not type(replacement):
                expected_codes += ("OP8-SHAPE-TYPE",)
            elif type(original) is dict:
                expected_codes += ("OP8-SHAPE-KEYSET",)
            elif type(original) is list:
                expected_codes += ("OP8-SHAPE-COUNT",)
            if len(path) >= 2 and path[-1] == "kind" and \
                    path[:3] == kind_suffix:
                expected_codes += (
                    "OP8-SHAPE-FIXTURE-KIND-VALUE" if type(replacement) is str
                    else "OP8-SHAPE-FIXTURE-KIND-TYPE",
                )
            add(
                heterogeneous,
                f"heterogeneous {variant_name} at {_format_path(path)}",
                lambda c, p=path, r=copy.deepcopy(replacement):
                    _replace_path(c, p, r),
                expected_codes,
            )

    for label, candidate, expected_codes in targeted + heterogeneous:
        _assert_check_case(failures, label, candidate, expected_codes, context)

    parser_count = 0
    integer_4300 = b"1" * 4300
    integer_value_4300 = _decimal_digits_to_int("1" * 4300)
    _assert_parser_value(
        failures, "integer 4300-digit boundary", integer_4300,
        integer_value_4300, int)
    parser_count += 1
    _assert_parser_error(
        failures, "integer 4301-digit attack", b"1" * 4301,
        "OP8-NUMERIC-INTEGER-DIGITS")
    parser_count += 1
    _assert_parser_error(
        failures, "integer 5000-digit attack", b"1" * 5000,
        "OP8-NUMERIC-INTEGER-DIGITS")
    parser_count += 1
    _assert_parser_value(
        failures, "negative integer 4300-digit boundary", b"-" + integer_4300,
        -integer_value_4300, int)
    parser_count += 1
    _assert_parser_error(
        failures, "negative integer 4301-digit attack", b"-" + b"1" * 4301,
        "OP8-NUMERIC-INTEGER-DIGITS")
    parser_count += 1
    _assert_parser_error(
        failures, "negative integer 5000-digit attack", b"-" + b"1" * 5000,
        "OP8-NUMERIC-INTEGER-DIGITS")
    parser_count += 1
    node_inner = b"[" + b",".join([b"0"] * MAX_ARRAY_ITEMS) + b"]"
    node_bound_raw = b"[" + b",".join([node_inner] * 10) + b"]"
    parser_errors = [
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
        ("depth bound", b"[" * 66 + b"0" + b"]" * 66,
         "OP8-LIMIT-DEPTH"),
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
    _assert_parser_value(failures, "finite negative float/exponent", b"-1.5e-2",
                         -0.015, float)
    parser_count += 1
    float_4300 = b"0." + b"1" * 4299
    _assert_parser_value(
        failures, "float significand 4300-digit boundary", float_4300,
        float(float_4300.decode("ascii")), float)
    parser_count += 1
    _assert_parser_value(failures, "negative exponent lower boundary", b"-1e-4300",
                         -0.0, float)
    parser_count += 1

    api_cases: list[tuple[str, Any, tuple[str, ...]]] = [
        ("API null root", None, ("OP8-TOTALITY-ROOT",)),
        ("API boolean root", True, ("OP8-TOTALITY-ROOT",)),
        ("API integer root", 7, ("OP8-TOTALITY-ROOT",)),
        ("API float root", 7.5, ("OP8-TOTALITY-ROOT",)),
        ("API string root", "hostile", ("OP8-TOTALITY-ROOT",)),
        ("API array root", [], ("OP8-TOTALITY-ROOT",)),
        ("API empty object", {}, ("OP8-FULL",)),
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
        _assert_check_case(failures, label, candidate, expected_codes, context)

    cli_count = _cli_controls(failures, value)
    trust_count = _trust_controls(failures)
    return failures, {
        "targeted": len(targeted),
        "heterogeneous": len(heterogeneous),
        "parser": parser_count,
        "api": len(api_cases),
        "cli": cli_count,
        "trust": trust_count,
    }


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        raw = path.read_bytes()
    except OSError:
        print("FAIL: OP8-IO: cannot read candidate", file=sys.stderr)
        return 2
    try:
        value = strict_loads(raw)
    except ControlledInputError as exc:
        print(f"FAIL: {exc.code}: {exc.detail}", file=sys.stderr)
        return 2
    context, dependency_errors = authenticated_context()
    if dependency_errors or context is None:
        if "--selftest" in argv[1:]:
            print("REFUSING selftest: OPERABILITY v8 base/dependency closure is dirty")
        for error in dependency_errors or ["OP8-DEP-CONTEXT: context unavailable"]:
            print(f"FAIL: {error}")
        return 1
    findings = check(value, verify_files=False, context=context)
    if findings:
        if "--selftest" in argv[1:]:
            print("REFUSING selftest: OPERABILITY v8 base/dependency closure is dirty")
        for finding in findings:
            print(f"FAIL: {finding}")
        return 1
    artifact_hash = _digest(raw)
    if "--selftest" in argv[1:]:
        failures, counts = selftest(value, context)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(
            f"PASS: operability.v8.json@sha256:{artifact_hash}; "
            f"{counts['targeted']} targeted mutations, "
            f"{counts['heterogeneous']} systematic heterogeneous replacements, "
            f"{counts['parser']} parser/API-token controls, "
            f"{counts['api']} bounded API controls, {counts['cli']} CLI controls, "
            f"and {counts['trust']} trust-order/cache/path controls rejected"
        )
    else:
        print(
            f"PASS: operability.v8.json@sha256:{artifact_hash}; "
            "exact OP8->OP7->OP6->OP5->OP2 projection; complete EventEnvelopeV3 "
            "lifecycle object-identical; 10/10 dependencies authenticated before "
            "verified-buffer compilation; OP7-IR-01/02 controlled"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
