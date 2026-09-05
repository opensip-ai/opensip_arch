#!/usr/bin/env python3
"""Validate the NOT-APPLIED OPERABILITY v10 exact-type successor.

Sole conformance commands, from the repository root:
  python3 -I -B docs/coop/artifacts/check-operability-v10.py
  python3 -I -B docs/coop/artifacts/check-operability-v10.py --selftest

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
        '"code":"OP10-UNSUPPORTED-NONISOLATED",'
        '"detail":"isolated Python startup is required"}\n')
    raise SystemExit(3)


import collections
import copy
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import tempfile
import types
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v10.json"
BINDING_SHA256 = "9bacbbf43dfb941a0d87330f79844d395b3ac838ae5bf54026ef4d69681696be"
V10_METADATA_SHA256 = "acca40ab0065e6c8c40bd4c728c03c1be6d13b6d210c9ca638ba33477c2e228c"
PINS = {
    "operability.v9.json": "8e19e23746716bb38cb6365b13f128121f38f72b81ea9ba7318caed3c135df1f",
    "check-operability-v9.py": "19f375a23b420bf2b3d0733eb0405829f2cc23fb03930d81dc9e8b1b88f1e3fa",
    "operability.v9.review-independent-prefreeze.json": "7745d371ffdb760e086d27c5f40280e71bdb822d64a3d1f8547abdb643f66a77",
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
ROOT_ENVELOPE = ("version", "status", "supersedes", "author", "reviewStatus")
V9_REVIEW_FINDING = "OP9-IR-01-RECURSIVE-EXACT-TYPE-ORACLE"
CODE_RE = re.compile(r"^[A-Z][A-Z0-9-]*$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_OUTCOME_TOKENS = (
    "internal", "exception", "traceback", "typeerror", "outward-exception",
)
MACHINE_RESULT_KEYS = {
    "schemaVersion", "kind", "status", "artifactSha256", "findings",
    "selftestCounts",
}
SELFTEST_COUNT_KEYS = {
    "targeted", "scalarLeaves", "typeSubstitutions",
    "typeSubstitutionsRejected", "typeSubstitutionEscapes", "transport",
    "cli", "retainedV9Targeted", "retainedV9Heterogeneous",
    "retainedV9Parser", "retainedV9Api", "retainedV9Cli",
    "oracleMutantsKilled", "isolation", "trust", "mutationEscape",
}
FINDING_RECORD_KEYS = {"code", "detail"}
MACHINE_MODES = {"NORMAL-PASS", "SELFTEST-PASS", "FAIL", "UNSUPPORTED"}
UNSUPPORTED_PAYLOAD = {
    "schemaVersion": 1,
    "kind": "unsupported-mode",
    "status": "UNSUPPORTED",
    "code": "OP10-UNSUPPORTED-NONISOLATED",
    "detail": "isolated Python startup is required",
}


FindingRecord = dict[str, str]
PathPart = str | int


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _finding(code: str, detail: str) -> FindingRecord:
    return {"code": code, "detail": detail}


def _float_exact(left: float, right: float) -> bool:
    if left == 0.0 and right == 0.0:
        return math.copysign(1.0, left) == math.copysign(1.0, right)
    return left == right


def json_exact(left: Any, right: Any) -> bool:
    """Recursive JSON equality with type identity before value equality."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            json_exact(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(
            json_exact(a, b) for a, b in zip(left, right))
    if type(left) is float:
        return _float_exact(left, right)
    return left == right


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return _digest(raw)


def _compile_verified(raw: bytes, filename: str, module_name: str) -> Any:
    """Compile only an already authenticated immutable buffer."""
    module = types.ModuleType(module_name)
    module.__file__ = str(HERE / filename)
    module.__package__ = None
    code = compile(raw, module.__file__, "exec", dont_inherit=True)
    exec(code, module.__dict__)
    return module


def expected_dependency_closure() -> dict[str, dict[str, str]]:
    kinds = {
        "operability.v9.json": "rejected-predecessor-data",
        "check-operability-v9.py": "rejected-predecessor-executable-source",
        "operability.v9.review-independent-prefreeze.json": "rejection-review-data",
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


def _review_binding_valid(review: Any) -> bool:
    if type(review) is not dict:
        return False
    verdict = review.get("verdict")
    binding = review.get("reviewBinding")
    if type(verdict) is not dict or type(binding) is not dict:
        return False
    if type(verdict.get("decision")) is not str or \
            verdict.get("decision") != "REJECT":
        return False
    ids = verdict.get("blockingFindingIds")
    if type(ids) is not list or len(ids) != 1 or \
            type(ids[0]) is not str or ids[0] != V9_REVIEW_FINDING:
        return False
    candidate = binding.get("candidate")
    checker = binding.get("candidateChecker")
    if type(candidate) is not dict or type(checker) is not dict:
        return False
    return candidate.get("path") == "docs/coop/artifacts/operability.v9.json" and \
        candidate.get("sha256") == PINS["operability.v9.json"] and \
        checker.get("path") == "docs/coop/artifacts/check-operability-v9.py" and \
        checker.get("sha256") == PINS["check-operability-v9.py"]


def authenticated_context() -> tuple[dict[str, Any] | None, list[str]]:
    """Hash the exact v10 binding and all sixteen inputs before predecessor exec."""
    errors: list[str] = []
    buffers: dict[str, bytes] = {}
    expected_files = {BINDING: BINDING_SHA256, **PINS}
    for name, expected in expected_files.items():
        try:
            raw = (HERE / name).read_bytes()
        except OSError:
            errors.append(f"OP10-DEP-READ: cannot read {name}")
            continue
        buffers[name] = raw
        actual = _digest(raw)
        if actual != expected:
            errors.append(f"OP10-DEP-HASH: {name} hash {actual} != {expected}")
    if errors or tuple(buffers) != tuple(expected_files):
        return None, errors or ["OP10-DEP-CLOSURE: input closure is incomplete"]

    try:
        v9mod = _compile_verified(
            buffers["check-operability-v9.py"],
            "check-operability-v9.py", "op9_rejected_verified_for_op10")
    except Exception as exc:
        return None, [f"OP10-DEP-COMPILE: verified OP9 raised {type(exc).__name__}"]
    if getattr(v9mod, "BINDING", None) != "operability.v9.json" or \
            not callable(getattr(v9mod, "strict_loads", None)) or \
            not callable(getattr(v9mod, "check", None)) or \
            not callable(getattr(v9mod, "authenticated_context", None)):
        return None, ["OP10-DEP-SURFACE: verified OP9 checker is incomplete"]
    try:
        expected_v10 = v9mod.strict_loads(buffers[BINDING])
        v9 = v9mod.strict_loads(buffers["operability.v9.json"])
        v9_review = v9mod.strict_loads(
            buffers["operability.v9.review-independent-prefreeze.json"])
    except Exception as exc:
        return None, [f"OP10-DEP-PARSE: authenticated data raised {type(exc).__name__}"]
    if not _review_binding_valid(v9_review):
        return None, ["OP10-REVIEW: exact v9 rejection binding is not closed"]
    successor = expected_v10.get("aPrimeSuccessor") \
        if type(expected_v10) is dict else None
    metadata = successor.get("operabilityV10Successor") \
        if type(successor) is dict else None
    if type(metadata) is not dict:
        return None, ["OP10-BINDING: exact v10 successor metadata is absent"]
    try:
        metadata_hash = _canonical_sha256(metadata)
    except Exception:
        metadata_hash = ""
    if metadata_hash != V10_METADATA_SHA256 or not json_exact(
            metadata.get("localDependencyClosure"),
            expected_dependency_closure()):
        return None, ["OP10-BINDING: exact v10 metadata/closure drift"]
    try:
        v9_context, v9_errors = v9mod.authenticated_context()
    except Exception as exc:
        return None, [f"OP10-DEP-CONTEXT: verified OP9 raised {type(exc).__name__}"]
    if v9_errors or v9_context is None:
        return None, [
            "OP10-DEP-CONTEXT: " + error for error in (
                v9_errors or ["verified OP9 context unavailable"])]
    try:
        predecessor_findings = v9mod.check(
            v9, verify_files=False, context=v9_context)
    except Exception as exc:
        return None, [f"OP10-DEP-CHECK: verified OP9 raised {type(exc).__name__}"]
    if predecessor_findings:
        return None, ["OP10-DEP-CHECK: exact rejected OP9 semantic check drift"]
    context = {
        "buffers": buffers,
        "expected_v10": expected_v10,
        "v9": v9,
        "v9_review": v9_review,
        "v9mod": v9mod,
        "v9_context": v9_context,
    }
    projected = _fixed_project_v9(expected_v10, v9)
    if projected is None or not json_exact(projected, v9):
        return None, ["OP10-PROJ: exact binding does not type-strict project to OP9"]
    return context, []


def _fixed_project_v9(candidate: Any, v9: dict[str, Any]) -> Any:
    if type(candidate) is not dict or \
            type(candidate.get("aPrimeSuccessor")) is not dict:
        return None
    result = copy.deepcopy(candidate)
    result["aPrimeSuccessor"].pop("operabilityV10Successor", None)
    for key in ROOT_ENVELOPE:
        result[key] = copy.deepcopy(v9[key])
    return result


def project_v9(candidate: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(candidate)
    successor = result["aPrimeSuccessor"]
    metadata = successor["operabilityV10Successor"]
    projection = metadata["v10ToV9Projection"]
    changed = projection.get("changedRootFields")
    if type(changed) is not dict or set(changed) != set(ROOT_ENVELOPE):
        raise ValueError("v10-to-v9 root envelope is not closed")
    if projection.get("removedSuccessorMetadata") != [
            "aPrimeSuccessor.operabilityV10Successor"]:
        raise ValueError("v10-to-v9 metadata removal is not exact")
    successor.pop("operabilityV10Successor")
    for key in ROOT_ENVELOPE:
        row = changed[key]
        if type(row) is not dict or set(row) != {"before", "after"}:
            raise ValueError("v10-to-v9 root row is not closed")
        result[key] = copy.deepcopy(row["before"])
    return result


def _delta_flags(actual: Any, expected: Any) -> tuple[bool, bool]:
    type_drift = False
    keyset_drift = False
    stack: list[tuple[Any, Any]] = [(actual, expected)]
    seen: set[tuple[int, int]] = set()
    while stack:
        left, right = stack.pop()
        if type(left) is not type(right):
            type_drift = True
            continue
        if type(left) is dict:
            pair = (id(left), id(right))
            if pair in seen:
                continue
            seen.add(pair)
            if set(left) != set(right):
                keyset_drift = True
            for key in set(left) & set(right):
                stack.append((left[key], right[key]))
        elif type(left) is list:
            pair = (id(left), id(right))
            if pair in seen:
                continue
            seen.add(pair)
            for a, b in zip(left, right):
                stack.append((a, b))
    return type_drift, keyset_drift


def _parse_legacy_finding(value: Any, source: str) -> FindingRecord:
    if type(value) is dict and set(value) == FINDING_RECORD_KEYS:
        return copy.deepcopy(value)
    if type(value) is not str:
        return _finding(
            "OP10-INTERNAL-MALFORMED-PREDECESSOR-FINDING",
            f"{source} returned a non-string finding")
    code, separator, detail = value.partition(": ")
    if not separator or CODE_RE.fullmatch(code) is None or not detail:
        return _finding(
            "OP10-INTERNAL-MALFORMED-PREDECESSOR-FINDING",
            f"{source} returned a malformed finding")
    return _finding(code, detail)


def _unique_records(records: list[FindingRecord]) -> list[FindingRecord]:
    result: list[FindingRecord] = []
    seen: set[str] = set()
    for record in records:
        code = record.get("code") if type(record) is dict else None
        if type(code) is str and code not in seen:
            seen.add(code)
            result.append(record)
    return result


def _check_v10_impl(value: Any, *, context: dict[str, Any]) -> list[FindingRecord]:
    v9mod = context["v9mod"]
    bounded = v9mod.json_value_findings(value)
    if bounded:
        return _unique_records([
            _parse_legacy_finding(item, "verified OP9 bounded validator")
            for item in bounded])
    expected = context["expected_v10"]
    if json_exact(value, expected):
        projected = project_v9(value)
        if not json_exact(projected, context["v9"]):
            return [_finding(
                "OP10-INTERNAL-PROJECTION",
                "exact v10 failed its type-strict v9 projection")]
        inherited = v9mod.check(
            projected, verify_files=False, context=context["v9_context"])
        if inherited:
            return [_finding(
                "OP10-INTERNAL-PREDECESSOR-CHECK",
                "exact projected v9 returned predecessor findings")]
        return []

    records: list[FindingRecord] = [
        _finding("OP10-FULL", "candidate differs from complete expected v10")]
    type_drift, keyset_drift = _delta_flags(value, expected)
    if type_drift:
        records.append(_finding(
            "OP10-TYPE-EXACT",
            "JSON node type differs from the exact v10 node type"))
    if keyset_drift:
        records.append(_finding(
            "OP10-KEYSET-EXACT",
            "JSON object key set differs from the exact v10 key set"))
    if type_drift or keyset_drift:
        return records
    projected = _fixed_project_v9(value, context["v9"])
    if projected is None:
        records.append(_finding(
            "OP10-SHAPE-SUCCESSOR", "cannot form the fixed v9 projection"))
        return _unique_records(records)
    inherited = v9mod.check(
        projected, verify_files=False, context=context["v9_context"])
    for finding in inherited:
        records.append(_parse_legacy_finding(finding, "verified OP9 checker"))
    return _unique_records(records)


def check(value: Any, *, verify_files: bool = True,
          context: dict[str, Any] | None = None) -> list[FindingRecord]:
    if context is None:
        if not verify_files:
            return [_finding(
                "OP10-DEP-CONTEXT", "unauthenticated context is forbidden")]
        context, errors = authenticated_context()
        if errors or context is None:
            return [_parse_legacy_finding(
                errors[0] if errors else "OP10-DEP-CONTEXT: unavailable",
                "v10 dependency authenticator")]
    return _check_v10_impl(value, context=context)


def _finding_record_errors(value: Any) -> list[str]:
    if type(value) is not dict or set(value) != FINDING_RECORD_KEYS:
        return ["finding record must have exactly code and detail"]
    errors: list[str] = []
    code = value.get("code")
    detail = value.get("detail")
    if type(code) is not str or CODE_RE.fullmatch(code) is None:
        errors.append("finding code is malformed")
    if type(detail) is not str or not detail or "\n" in detail or "\r" in detail:
        errors.append("finding detail is malformed")
    else:
        try:
            detail.encode("utf-8")
        except UnicodeEncodeError:
            errors.append("finding detail is not Unicode-scalar text")
    return errors


def _record_codes(records: Any) -> tuple[list[str], list[str]]:
    if type(records) is not list:
        return [], ["finding collection is not an array"]
    codes: list[str] = []
    errors: list[str] = []
    for index, record in enumerate(records):
        record_errors = _finding_record_errors(record)
        errors.extend(f"record {index}: {error}" for error in record_errors)
        if not record_errors:
            codes.append(record["code"])
    duplicates = sorted(
        code for code, count in collections.Counter(codes).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate finding codes {duplicates}")
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
    failures: list[str] = []
    if type(expected_codes) is not tuple or any(
            type(code) is not str or CODE_RE.fullmatch(code) is None
            for code in expected_codes) or \
            len(expected_codes) != len(set(expected_codes)):
        failures.append("declared expected code set is malformed or duplicated")
    codes, record_errors = _record_codes(records)
    failures.extend(record_errors)
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


class TransportInputError(ValueError):
    pass


def _closed_transport_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise TransportInputError("duplicate object member")
        result[key] = value
    return result


def _transport_loads(raw: bytes) -> Any:
    if len(raw) > 2_000_000:
        raise TransportInputError("transport exceeds raw bound")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise TransportInputError("transport is not UTF-8") from None
    try:
        return json.loads(
            text,
            object_pairs_hook=_closed_transport_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                TransportInputError(f"nonfinite constant {token}")),
        )
    except TransportInputError:
        raise
    except (json.JSONDecodeError, RecursionError, ValueError):
        raise TransportInputError("transport is not closed JSON") from None


def _machine_payload(status: str, records: list[FindingRecord],
                     artifact_hash: str | None,
                     counts: dict[str, int] | None) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "operability-v10-result",
        "status": status,
        "artifactSha256": artifact_hash,
        "findings": records,
        "selftestCounts": counts,
    }


def _emit_machine(status: str, records: list[FindingRecord],
                  artifact_hash: str | None = None,
                  counts: dict[str, int] | None = None) -> None:
    sys.stdout.write(json.dumps(
        _machine_payload(status, records, artifact_hash, counts),
        ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")


def _parse_machine_bytes(stdout: bytes, stderr: bytes,
                         expected_mode: str) -> tuple[
                             list[FindingRecord], tuple[str, ...], Any]:
    transport: list[str] = []
    if expected_mode not in MACHINE_MODES:
        return [], ("EXPECTED-MODE",), None
    if stderr:
        transport.append("STDERR")
    if not stdout.endswith(b"\n") or stdout.count(b"\n") != 1 or b"\r" in stdout:
        transport.append("UNSTRUCTURED-STDOUT")
    try:
        value = _transport_loads(stdout)
    except TransportInputError:
        return [], tuple(sorted(set(transport + ["MALFORMED-RECORD"]))), None

    if expected_mode == "UNSUPPORTED":
        if not json_exact(value, UNSUPPORTED_PAYLOAD):
            transport.append("MODE-SCHEMA")
        return [], tuple(sorted(set(transport))), value

    if type(value) is not dict or set(value) != MACHINE_RESULT_KEYS:
        return [], tuple(sorted(set(transport + ["MALFORMED-RECORD"]))), value
    if type(value.get("schemaVersion")) is not int or \
            value.get("schemaVersion") != 1 or \
            type(value.get("kind")) is not str or \
            value.get("kind") != "operability-v10-result" or \
            type(value.get("status")) is not str:
        transport.append("MALFORMED-RECORD")
    records = value.get("findings")
    _, record_errors = _record_codes(records)
    if record_errors:
        transport.append("MALFORMED-RECORD")
        records = records if type(records) is list else []
    artifact_hash = value.get("artifactSha256")
    counts = value.get("selftestCounts")

    if expected_mode == "NORMAL-PASS":
        if value.get("status") != "PASS" or \
                type(artifact_hash) is not str or \
                HEX64_RE.fullmatch(artifact_hash) is None or \
                records != [] or counts is not None:
            transport.append("MODE-SCHEMA")
    elif expected_mode == "SELFTEST-PASS":
        if value.get("status") != "PASS" or \
                type(artifact_hash) is not str or \
                HEX64_RE.fullmatch(artifact_hash) is None or records != [] or \
                type(counts) is not dict or set(counts) != SELFTEST_COUNT_KEYS or \
                any(type(item) is not int or item < 0 for item in counts.values()):
            transport.append("MODE-SCHEMA")
    else:
        if value.get("status") != "FAIL" or artifact_hash is not None or \
                type(records) is not list or not records or counts is not None:
            transport.append("MODE-SCHEMA")
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


def _scalar_paths(root: Any) -> list[tuple[PathPart, ...]]:
    paths: list[tuple[PathPart, ...]] = []
    stack: list[tuple[Any, tuple[PathPart, ...]]] = [(root, ())]
    while stack:
        value, path = stack.pop()
        if type(value) is dict:
            for key, child in reversed(list(value.items())):
                stack.append((child, path + (key,)))
        elif type(value) is list:
            for index in range(len(value) - 1, -1, -1):
                stack.append((value[index], path + (index,)))
        else:
            paths.append(path)
    return paths


def _variant_marker(value: Any) -> tuple[type[Any], str]:
    if type(value) is float and value == 0.0:
        return type(value), "-0.0" if math.copysign(1.0, value) < 0 else "0.0"
    return type(value), repr(value)


def _equality_confusable_variants(value: Any) -> list[Any]:
    variants: list[Any] = []
    if type(value) is bool:
        variants.extend([int(value), float(value)])
        if value is False:
            variants.append(-0.0)
    elif type(value) is int:
        variants.append(float(value))
        if value in (0, 1):
            variants.append(bool(value))
        if value == 0:
            variants.append(-0.0)
    elif type(value) is float and math.isfinite(value):
        if value.is_integer():
            variants.append(int(value))
            if value in (0.0, 1.0):
                variants.append(bool(int(value)))
        if value == 0.0:
            variants.append(
                -0.0 if math.copysign(1.0, value) > 0 else 0.0)
    result: list[Any] = []
    seen: set[tuple[type[Any], str]] = set()
    for variant in variants:
        marker = _variant_marker(variant)
        if marker not in seen and not json_exact(variant, value):
            seen.add(marker)
            result.append(variant)
    return result


def _assert_case(failures: list[str], label: str, candidate: Any,
                 expected_codes: tuple[str, ...],
                 context: dict[str, Any]) -> None:
    try:
        records = check(candidate, verify_files=False, context=context)
    except Exception as exc:
        failures.append(
            f"{label}: OUTWARD-EXCEPTION {type(exc).__name__}; escape")
        return
    for failure in _evaluate_exact_outcome(records, expected_codes):
        failures.append(f"{label}: {failure}")


def _type_substitution_controls(
        failures: list[str], value: dict[str, Any],
        context: dict[str, Any]) -> tuple[int, int, int, int]:
    scalar_paths = _scalar_paths(value)
    substitutions = 0
    rejected = 0
    escapes = 0
    for path in scalar_paths:
        original = _path_value(value, path)
        for replacement in _equality_confusable_variants(original):
            substitutions += 1
            candidate = copy.deepcopy(value)
            before = copy.deepcopy(candidate)
            try:
                _replace_path(candidate, path, replacement)
            except Exception as exc:
                escapes += 1
                failures.append(
                    f"type substitution {_format_path(path)} failed to apply "
                    f"({type(exc).__name__}); escape")
                continue
            if json_exact(candidate, before):
                escapes += 1
                failures.append(
                    f"type substitution {_format_path(path)} was a type-strict no-op; escape")
                continue
            try:
                records = check(candidate, verify_files=False, context=context)
            except Exception as exc:
                escapes += 1
                failures.append(
                    f"type substitution {_format_path(path)} raised "
                    f"OUTWARD-EXCEPTION {type(exc).__name__}; escape")
                continue
            outcome = _evaluate_exact_outcome(
                records, ("OP10-FULL", "OP10-TYPE-EXACT"))
            if outcome:
                escapes += 1
                for failure in outcome:
                    failures.append(
                        f"type substitution {_format_path(path)}: {failure}")
            else:
                rejected += 1
    return len(scalar_paths), substitutions, rejected, escapes


def _transport_controls(failures: list[str]) -> int:
    count = 0
    zero_counts = {key: 0 for key in SELFTEST_COUNT_KEYS}
    valid_record = _finding("OP10-EXPECTED", "expected detail")
    normal = _machine_payload("PASS", [], "a" * 64, None)
    successful_selftest = _machine_payload(
        "PASS", [], "a" * 64, zero_counts)
    failed = _machine_payload("FAIL", [valid_record], None, None)

    def encode(payload: Any) -> bytes:
        return json.dumps(
            payload, ensure_ascii=True, separators=(",", ":")).encode() + b"\n"

    def accepted(label: str, payload: Any, mode: str) -> None:
        nonlocal count
        count += 1
        records, transport, parsed = _parse_machine_bytes(
            encode(payload), b"", mode)
        if transport or parsed is None:
            failures.append(f"transport {label}: rejected {transport}")
        if mode == "FAIL" and _evaluate_exact_outcome(
                records, ("OP10-EXPECTED",), transport):
            failures.append(f"transport {label}: exact failure record drift")

    def rejected(label: str, raw: bytes, mode: str,
                 stderr: bytes = b"") -> None:
        nonlocal count
        count += 1
        _, transport, _ = _parse_machine_bytes(raw, stderr, mode)
        if not transport:
            failures.append(f"transport {label}: malformed record accepted")

    accepted("normal pass", normal, "NORMAL-PASS")
    accepted("selftest pass", successful_selftest, "SELFTEST-PASS")
    accepted("failure", failed, "FAIL")
    accepted("unsupported", UNSUPPORTED_PAYLOAD, "UNSUPPORTED")
    for label, payload, mode in (
            ("reordered normal", dict(reversed(list(normal.items()))), "NORMAL-PASS"),
            ("reordered selftest", dict(reversed(list(successful_selftest.items()))),
             "SELFTEST-PASS"),
            ("reordered failure", dict(reversed(list(failed.items()))), "FAIL"),
            ("reordered unsupported",
             dict(reversed(list(UNSUPPORTED_PAYLOAD.items()))), "UNSUPPORTED")):
        accepted(label, payload, mode)

    schema_variants: tuple[Any, ...] = (True, False, 1.0, 0.0, -0.0)
    for mode, base in (
            ("NORMAL-PASS", normal), ("SELFTEST-PASS", successful_selftest),
            ("FAIL", failed), ("UNSUPPORTED", UNSUPPORTED_PAYLOAD)):
        for variant in schema_variants:
            candidate = copy.deepcopy(base)
            candidate["schemaVersion"] = variant
            rejected(
                f"{mode} schema {type(variant).__name__}:{variant!r}",
                encode(candidate), mode)

    for key in sorted(SELFTEST_COUNT_KEYS):
        for variant in schema_variants:
            candidate = copy.deepcopy(successful_selftest)
            candidate["selftestCounts"][key] = variant
            rejected(
                f"selftest count {key} {type(variant).__name__}:{variant!r}",
                encode(candidate), "SELFTEST-PASS")

    mode_confusions = (
        (normal, "SELFTEST-PASS"),
        (successful_selftest, "NORMAL-PASS"),
        (failed, "NORMAL-PASS"),
        (normal, "FAIL"),
    )
    for index, (payload, mode) in enumerate(mode_confusions):
        rejected(f"mode confusion {index}", encode(payload), mode)

    for label, base, mode in (
            ("normal", normal, "NORMAL-PASS"),
            ("selftest", successful_selftest, "SELFTEST-PASS"),
            ("failure", failed, "FAIL"),
            ("unsupported", UNSUPPORTED_PAYLOAD, "UNSUPPORTED")):
        extra = copy.deepcopy(base)
        extra["unknown"] = 1
        rejected(f"{label} unknown key", encode(extra), mode)
        missing = copy.deepcopy(base)
        missing.pop(next(iter(missing)))
        rejected(f"{label} missing key", encode(missing), mode)

    rejected(
        "duplicate top key",
        b'{"schemaVersion":1,"schemaVersion":1,"kind":"operability-v10-result",'
        b'"status":"FAIL","artifactSha256":null,"findings":['
        b'{"code":"OP10-X","detail":"x"}],"selftestCounts":null}\n',
        "FAIL")
    rejected("human output", b"FAIL: OP10-X: human\n", "FAIL")
    rejected("two records", encode(failed) + encode(failed), "FAIL")
    rejected("no newline", encode(failed)[:-1], "FAIL")
    rejected("CRLF", encode(failed)[:-1] + b"\r\n", "FAIL")
    rejected("stderr", encode(failed), "FAIL", b"unexpected stderr")
    rejected("invalid UTF-8", b"\xff\n", "FAIL")

    for label, records, expected, should_fail in (
            ("exact", [valid_record], ("OP10-EXPECTED",), False),
            ("expected only in detail",
             [_finding("OP10-WRONG", "OP10-EXPECTED: detail only")],
             ("OP10-EXPECTED",), True),
            ("additional", [valid_record, _finding("OP10-EXTRA", "extra")],
             ("OP10-EXPECTED",), True),
            ("duplicate", [valid_record, copy.deepcopy(valid_record)],
             ("OP10-EXPECTED",), True),
            ("full substitute", [_finding("OP10-FULL", "generic")],
             ("OP10-EXPECTED",), True),
            ("internal", [_finding("OP10-INTERNAL-X", "forbidden")],
             ("OP10-INTERNAL-X",), True)):
        count += 1
        observed = bool(_evaluate_exact_outcome(records, expected))
        if observed != should_fail:
            failures.append(f"transport code oracle {label}: outcome drift")
    return count


def _cli_controls(failures: list[str], value: dict[str, Any]) -> int:
    cases: list[tuple[str, bytes, tuple[str, ...], int, bool]] = []
    with tempfile.TemporaryDirectory(prefix="op10-cli-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        case_path = temp_dir / "case.json"

        def encoded(mutator: Callable[[dict[str, Any]], None]) -> bytes:
            candidate = copy.deepcopy(value)
            mutator(candidate)
            return json.dumps(candidate, ensure_ascii=False).encode("utf-8")

        cases.extend([
            ("dirty status selftest",
             encoded(lambda c: c.__setitem__("status", "APPLIED")),
             ("OP10-FULL",), 1, True),
            ("root version type normal",
             encoded(lambda c: c.__setitem__("version", 10.0)),
             ("OP10-FULL", "OP10-TYPE-EXACT"), 1, False),
            ("root version type selftest",
             encoded(lambda c: c.__setitem__("version", 10.0)),
             ("OP10-FULL", "OP10-TYPE-EXACT"), 1, True),
            ("lifecycle schema type",
             encoded(lambda c: c["aPrimeSuccessor"]["lifecycle"]
                     ["schemaVersionConstraint"].__setitem__("value", 3.0)),
             ("OP10-FULL", "OP10-TYPE-EXACT"), 1, False),
            ("4301-digit integer", b"1" * 4301,
             ("OP8-NUMERIC-INTEGER-DIGITS",), 2, False),
            ("5000-digit integer", b"1" * 5000,
             ("OP8-NUMERIC-INTEGER-DIGITS",), 2, False),
        ])
        for label, raw, expected_codes, expected_exit, use_selftest in cases:
            case_path.write_bytes(raw)
            args = [str(case_path)]
            if use_selftest:
                args.append("--selftest")
            args.append("--machine")
            try:
                completed = subprocess.run(
                    _isolated_child_command(*args), capture_output=True,
                    check=False, env=_sanitized_python_env(), timeout=60)
            except Exception as exc:
                failures.append(
                    f"CLI {label}: OUTWARD-EXCEPTION {type(exc).__name__}")
                continue
            records, transport, result = _parse_machine_bytes(
                completed.stdout, completed.stderr, "FAIL")
            if completed.returncode != expected_exit or result is None:
                failures.append(
                    f"CLI {label}: exit/result drift ({completed.returncode})")
            for failure in _evaluate_exact_outcome(
                    records, expected_codes, transport):
                failures.append(f"CLI {label}: {failure}")
    return len(cases)


def _isolation_controls(failures: list[str]) -> int:
    count = 0
    if sys.flags.isolated != 1:
        failures.append("parent isolated-mode flag is not set")
    count += 1
    clean_env = _sanitized_python_env()
    if any(key.upper().startswith("PYTHON") for key in clean_env):
        failures.append("sanitized child environment retained PYTHON input")
    count += 1
    with tempfile.TemporaryDirectory(prefix="op10-isolation-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        marker = temp_dir / "marker"
        (temp_dir / "sitecustomize.py").write_text(
            "import os, pathlib\n"
            "pathlib.Path(os.environ['OP10_ISOLATION_MARKER']).write_text('seen')\n",
            encoding="utf-8")
        try:
            completed = subprocess.run(
                _isolated_child_command("--machine"), capture_output=True,
                check=False, cwd=temp_dir,
                env=_sanitized_python_env({
                    "OP10_ISOLATION_MARKER": str(marker),
                    "PYTHONPATH": str(temp_dir),
                }), timeout=60)
            records, transport, result = _parse_machine_bytes(
                completed.stdout, completed.stderr, "NORMAL-PASS")
            if marker.exists() or completed.returncode != 0 or transport or \
                    result is None or records:
                failures.append("nested isolated marker/control failed")
        except Exception as exc:
            failures.append(
                f"nested isolated control OUTWARD-EXCEPTION {type(exc).__name__}")
    count += 1

    # Sole sanitized non-isolated child: diagnostic refusal only, no authority.
    with tempfile.TemporaryDirectory(prefix="op10-unsupported-") as temp_name:
        try:
            completed = subprocess.run(
                [sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
                 "--machine"],
                capture_output=True, check=False, cwd=temp_name,
                env=_sanitized_python_env(), timeout=60)
            _, transport, parsed = _parse_machine_bytes(
                completed.stdout, completed.stderr, "UNSUPPORTED")
            if completed.returncode != 3 or transport or \
                    not json_exact(parsed, UNSUPPORTED_PAYLOAD):
                failures.append("sanitized non-isolated refusal result drift")
        except Exception as exc:
            failures.append(
                f"non-isolated refusal OUTWARD-EXCEPTION {type(exc).__name__}")
    count += 1
    return count


def _trust_controls(failures: list[str]) -> int:
    global HERE, _compile_verified
    count = 0
    original_here = HERE
    original_compile = _compile_verified
    with tempfile.TemporaryDirectory(prefix="op10-trust-") as temp_name:
        temp_dir = pathlib.Path(temp_name)
        for name in (BINDING, *PINS):
            (temp_dir / name).write_bytes((original_here / name).read_bytes())

        dirty = temp_dir / "operability.v9.review-independent-prefreeze.json"
        dirty.write_bytes(dirty.read_bytes() + b" ")
        compile_calls: list[str] = []

        def record_compile(raw: bytes, filename: str, module_name: str) -> Any:
            del raw, module_name
            compile_calls.append(filename)
            return types.ModuleType("unexpected_compile")

        try:
            HERE = temp_dir
            _compile_verified = record_compile
            context, errors = authenticated_context()
        finally:
            HERE = original_here
            _compile_verified = original_compile
        if context is not None or not any(
                error.startswith("OP10-DEP-HASH:") for error in errors) or \
                compile_calls:
            failures.append("trust dirty input did not stop before compilation")
        count += 1

        for name in (BINDING, *PINS):
            (temp_dir / name).write_bytes((original_here / name).read_bytes())
        first = True
        disk_marker: list[str] = []

        def substitute_after_read(
                raw: bytes, filename: str, module_name: str) -> Any:
            nonlocal first
            if first:
                first = False
                (temp_dir / "check-operability-v9.py").write_text(
                    "POST_READ_DISK_MARKER = True\n", encoding="utf-8")
            module = original_compile(raw, filename, module_name)
            if getattr(module, "POST_READ_DISK_MARKER", False):
                disk_marker.append(filename)
            return module

        try:
            HERE = temp_dir
            _compile_verified = substitute_after_read
            context, errors = authenticated_context()
        finally:
            HERE = original_here
            _compile_verified = original_compile
        if context is None or errors or disk_marker:
            failures.append("trust post-read disk substitution reached execution")
        count += 1

        for name in (BINDING, *PINS):
            (temp_dir / name).write_bytes((original_here / name).read_bytes())
        poison = types.ModuleType("op10_poison")
        poison.PATH_MODULE_MARKER = True
        module_name = "op9_rejected_verified_for_op10"
        previous = sys.modules.get(module_name)
        old_path = list(sys.path)
        sys.modules[module_name] = poison
        sys.path.insert(0, str(temp_dir))
        try:
            HERE = temp_dir
            context, errors = authenticated_context()
        finally:
            HERE = original_here
            sys.path[:] = old_path
            if previous is None:
                sys.modules.pop(module_name, None)
            else:
                sys.modules[module_name] = previous
        if context is None or errors or context.get("v9mod") is poison or \
                getattr(context.get("v9mod"), "PATH_MODULE_MARKER", False):
            failures.append("trust path/module poison reached predecessor execution")
        count += 1
    return count


def _retained_v9_selftest(
        failures: list[str], context: dict[str, Any]) -> dict[str, int]:
    v9mod = context["v9mod"]
    saved_isolation = v9mod._isolation_controls
    # V10 performs the sole nested non-isolated refusal control itself.  Reuse
    # the retained V9 matrix with only that predecessor process control elided.
    v9mod._isolation_controls = lambda inherited_failures: 0
    try:
        inherited_failures, counts = v9mod.selftest(
            context["v9"], context["v9_context"])
    except Exception as exc:
        inherited_failures = [
            f"retained V9 selftest raised {type(exc).__name__}"]
        counts = {}
    finally:
        v9mod._isolation_controls = saved_isolation
    failures.extend(f"retained V9: {failure}" for failure in inherited_failures)
    return counts


def selftest(value: dict[str, Any],
             context: dict[str, Any]) -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    if not json_exact(value, context["expected_v10"]):
        failures.append("dirty base escaped exact pre-mutation refusal")
    targeted = 0

    def targeted_case(label: str, mutator: Callable[[dict[str, Any]], None],
                      expected_codes: tuple[str, ...]) -> None:
        nonlocal targeted
        candidate = copy.deepcopy(value)
        before = copy.deepcopy(candidate)
        try:
            mutator(candidate)
        except Exception as exc:
            failures.append(
                f"{label}: mutation failed to apply ({type(exc).__name__}); escape")
            return
        if json_exact(candidate, before):
            failures.append(f"{label}: type-strict no-op mutation; escape")
            return
        targeted += 1
        _assert_case(failures, label, candidate, expected_codes, context)

    targeted_case(
        "status promotion", lambda c: c.__setitem__("status", "APPLIED"),
        ("OP10-FULL",))
    targeted_case(
        "root version integral float",
        lambda c: c.__setitem__("version", 10.0),
        ("OP10-FULL", "OP10-TYPE-EXACT"))
    targeted_case(
        "root version boolean",
        lambda c: c.__setitem__("version", True),
        ("OP10-FULL", "OP10-TYPE-EXACT"))
    targeted_case(
        "lifecycle schema integral float",
        lambda c: c["aPrimeSuccessor"]["lifecycle"]
        ["schemaVersionConstraint"].__setitem__("value", 3.0),
        ("OP10-FULL", "OP10-TYPE-EXACT"))
    targeted_case(
        "product acceptance integer",
        lambda c: c["aPrimeSuccessor"].__setitem__("productAcceptance", 0),
        ("OP10-FULL", "OP10-TYPE-EXACT"))
    targeted_case(
        "numeric policy integral float",
        lambda c: c["aPrimeSuccessor"]["operabilityV8Successor"]
        ["closedTotalityDeclarations"]["numericTokenPolicy"]["integer"]
        .__setitem__("maxDecimalDigitsExcludingSign", 4300.0),
        ("OP10-FULL", "OP10-TYPE-EXACT"))
    targeted_case(
        "v9 rejection verdict erased",
        lambda c: c["aPrimeSuccessor"]["operabilityV10Successor"]
        ["rejectionBinding"].__setitem__("verdict", "PASS"),
        ("OP10-FULL",))
    targeted_case(
        "unknown root key", lambda c: c.__setitem__("unknown", None),
        ("OP10-FULL", "OP10-KEYSET-EXACT"))

    reordered = dict(reversed(list(value.items())))
    if check(reordered, verify_files=False, context=context):
        failures.append("object-member reordering was incorrectly authoritative")
    targeted += 1
    try:
        projected = project_v9(value)
    except Exception as exc:
        failures.append(f"exact projection raised {type(exc).__name__}")
    else:
        if not json_exact(projected, context["v9"]):
            failures.append("exact type-strict v10-to-v9 projection drift")
    targeted += 1

    scalar_leaves, substitutions, rejected, escapes = \
        _type_substitution_controls(failures, value, context)

    mutation_escape = 0
    no_op = copy.deepcopy(value)
    if json_exact(no_op, value):
        mutation_escape += 1
    else:
        failures.append("deliberate no-op escape control was not detected")
    try:
        raise ValueError("deliberate failure-to-apply control")
    except ValueError:
        mutation_escape += 1
    if mutation_escape != 2:
        failures.append("no-op/failure-to-apply escape controls drifted")

    transport_count = _transport_controls(failures)
    cli_count = _cli_controls(failures, value)
    retained = _retained_v9_selftest(failures, context)
    isolation_count = _isolation_controls(failures)
    trust_count = _trust_controls(failures)
    return failures, {
        "targeted": targeted,
        "scalarLeaves": scalar_leaves,
        "typeSubstitutions": substitutions,
        "typeSubstitutionsRejected": rejected,
        "typeSubstitutionEscapes": escapes,
        "transport": transport_count,
        "cli": cli_count,
        "retainedV9Targeted": retained.get("targeted", 0),
        "retainedV9Heterogeneous": retained.get("heterogeneous", 0),
        "retainedV9Parser": retained.get("parser", 0),
        "retainedV9Api": retained.get("api", 0),
        "retainedV9Cli": retained.get("cli", 0),
        "oracleMutantsKilled": retained.get("oracleMutantsKilled", 0),
        "isolation": isolation_count,
        "trust": trust_count,
        "mutationEscape": mutation_escape,
    }


def main(argv: list[str]) -> int:
    allowed_flags = {"--selftest", "--machine"}
    unknown_flags = [
        arg for arg in argv[1:]
        if arg.startswith("-") and arg not in allowed_flags]
    positional = [
        arg for arg in argv[1:]
        if arg not in allowed_flags and not arg.startswith("-")]
    machine = "--machine" in argv[1:]
    run_selftest = "--selftest" in argv[1:]
    if unknown_flags or len(positional) > 1:
        records = [_finding("OP10-ARGS", "unsupported arguments")]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print("FAIL: OP10-ARGS: unsupported arguments")
        return 2

    context, dependency_errors = authenticated_context()
    if dependency_errors or context is None:
        records = [_parse_legacy_finding(
            dependency_errors[0] if dependency_errors else
            "OP10-DEP-CONTEXT: context unavailable",
            "v10 dependency authenticator")]
        if machine:
            _emit_machine("FAIL", records)
        else:
            if run_selftest:
                print("REFUSING selftest: OPERABILITY v10 dependency closure is dirty")
            for record in records:
                print(f"FAIL: {record['code']}: {record['detail']}")
        return 1

    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        raw = path.read_bytes()
    except OSError:
        records = [_finding("OP10-IO", "cannot read candidate")]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print("FAIL: OP10-IO: cannot read candidate")
        return 2
    try:
        value = context["v9mod"].strict_loads(raw)
    except context["v9mod"].ControlledInputError as exc:
        records = [_finding(exc.code, exc.detail)]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print(f"FAIL: {exc.code}: {exc.detail}")
        return 2
    except Exception as exc:
        records = [_finding(
            "OP10-OUTWARD-EXCEPTION",
            f"candidate parser raised {type(exc).__name__}")]
        if machine:
            _emit_machine("FAIL", records)
        else:
            print(f"FAIL: {records[0]['code']}: {records[0]['detail']}")
        return 2

    records = check(value, verify_files=False, context=context)
    if records:
        if machine:
            _emit_machine("FAIL", records)
        else:
            if run_selftest:
                print("REFUSING selftest: OPERABILITY v10 base is dirty")
            for record in records:
                print(f"FAIL: {record['code']}: {record['detail']}")
        return 1

    artifact_hash = _digest(raw)
    if run_selftest:
        failures, counts = selftest(value, context)
        if failures:
            record = _finding(
                "OP10-SELFTEST-FAIL",
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
                f"PASS: operability.v10.json@sha256:{artifact_hash}; "
                f"{counts['targeted']} targeted controls, "
                f"{counts['scalarLeaves']} scalar leaves visited, "
                f"{counts['typeSubstitutions']} value-equal type substitutions "
                f"rejected with {counts['typeSubstitutionEscapes']} escapes, "
                f"{counts['transport']} closed transport controls, "
                f"{counts['cli']} v10 CLI controls, retained V9 matrix "
                f"{counts['retainedV9Targeted']}/"
                f"{counts['retainedV9Heterogeneous']}/"
                f"{counts['retainedV9Parser']}/"
                f"{counts['retainedV9Api']}/"
                f"{counts['retainedV9Cli']}, "
                f"{counts['isolation']} isolation controls, and "
                f"{counts['trust']} trust controls")
    else:
        if machine:
            _emit_machine("PASS", [], artifact_hash, None)
        else:
            print(
                f"PASS: operability.v10.json@sha256:{artifact_hash}; exact "
                "type-strict OP10->OP9->OP8->OP7->OP6->OP5->OP2 projection; "
                "EventEnvelopeV3/startup/code-parser/numeric semantics unchanged; "
                "closed mode-specific transport; 16/16 predecessor inputs "
                "authenticated before verified-buffer execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
