#!/usr/bin/env python3
# Retained checker for the Rust semantic-provider protocol v4 candidate.
# Supported only as:
#   python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v4.py
#   python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v4.py --selftest
from __future__ import annotations
import sys
if sys.flags.isolated != 1 or not sys.dont_write_bytecode:
    print("RPPV4-UNSUPPORTED-INVOCATION: require python3 -I -B", file=sys.stderr)
    raise SystemExit(2)

import copy
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
import pathlib
import re
import types
from decimal import Decimal
from typing import Any, Callable, Mapping

HERE = pathlib.Path(__file__).resolve().parent
PROTOCOL = "rust-provider-protocol.v4.json"
DELIVERY = "delivery-rust-provider-join.v4.json"
RI_JOIN = "resolved-inputs-rust-provider-join.v4.json"
RESPONSE = "rust-provider-protocol.v4.adjudication-v3-rejection-response.json"
CHECKER = "check-rust-provider-protocol-v4.py"
V3_PROTOCOL = "rust-provider-protocol.v3.json"
V3_DELIVERY = "delivery-rust-provider-join.v3.json"
V3_RI = "resolved-inputs-rust-provider-join.v3.json"
V3_RESPONSE = "rust-provider-protocol.v3.adjudication-v2-rejection-response.json"
V3_CHECKER = "check-rust-provider-protocol-v3.py"
V3_REVIEW = "rust-provider-protocol.v3.review-independent-prefreeze.json"
V2_PROTOCOL = "rust-provider-protocol.v2.json"
V2_DELIVERY = "delivery-rust-provider-join.v2.json"
V2_RI = "resolved-inputs-rust-provider-join.v2.json"
V2_RESPONSE = "rust-provider-protocol.v2.adjudication-v1-rejection-response.json"
V2_CHECKER = "check-rust-provider-protocol-v2.py"
D9 = "d9-exit-contract.v1.13.json"
D9_CHECKER = "check-d9-v1.13.py"
STATUS = "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REVIEW"
REVIEW_SHA = "747f47b70f13679e8f7800187ce59cf0e48d13c6d0292f11e4a94d1556b5a79e"
U64_MAX = 18446744073709551615

LOCAL_JSON_HASHES = {
    PROTOCOL: "3e34934720a78f823d3d4c7ceb73735d444f09a4a1ec964a894bd1ac5daf2909",
    DELIVERY: "02d7c925eceedceafdf70073b6d8e19dfde046b830b25d9187b776e533456146",
    RI_JOIN: "4ce77f694df56edbe60a673e6c3c24c916bffe14ec09b4457d943cdc2aa6763e",
}
PRESERVED_HASHES = {
    V3_PROTOCOL: "b79a2374786d0ed4245ba550e926d4a1aeaeebf4f7e72e74107fc78718a7ff2d",
    V3_CHECKER: "798700b58af1f0ed048bd35e17f9ff21cfe71df6af39f38565e5343d8bab51ca",
    V3_RESPONSE: "5f298ae13d9807937ad9000cda381cf3a5ff2ecb7f24f4b0c60f630bc2d6a080",
    V3_DELIVERY: "4f4b300eb74059d3bb7165754267eace42d02241618da5fd95fe9f4cb8dc1c75",
    V3_RI: "598216742f31b1b53c017eadea2b9871e3dc91a54b10ead071d3addbbd902922",
    V3_REVIEW: REVIEW_SHA,
    "rust-provider-protocol.v1.json": "8c749eb7942a80cee3da2e304328addce4dac42e20a084b4ce26bcf31da51796",
    "check-rust-provider-protocol.py": "c190ee7f62552ec342f5da1f66ba2b840cdffd5cd5cddb25e5987c315ee1502e",
    "rust-provider-protocol.v1.adjudication-gap-response.json": "6da46e9160287cecd57e4ea6e9b5ea6fb7c3fb8b65708732f40c45ada2214891",
    "delivery-rust-provider-join.v1.json": "42eb9788132aee6d436123881bbd2e82db0da4f223bd13de16c26410fb3e5558",
    "resolved-inputs-rust-provider-join.v1.json": "b85017567f2f31589b17d9cd130aeb55b58700844f431cb7baa650a4f255d707",
    "rust-provider-protocol.v1.review-independent-prefreeze.json": "566dc23e6b774a5c8141a45ab4563579d3a2e5a1d0427cb29d7cdaca16ca6a69",
    V2_PROTOCOL: "6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b",
    V2_CHECKER: "7b967b888fc172b27268fae2f59273e5cf10b58b97db7c1f19a15657826a48e4",
    V2_RESPONSE: "a20f48e3f78361c6cfc07f4a40dd5b2aaad4bdfc7f1d9cec1c131006aadeda43",
    V2_DELIVERY: "12dd96eddaf99ba9b6efafa05fe11791685065b225fd602b4b5a9692345dfa1e",
    V2_RI: "435ec9cdd45a85255df0c099238bd0a3e1c10e88960716cd84649030d6482d47",
    "rust-provider-protocol.v2.review-independent-prefreeze.json": "52cf1b32a1fda7988abd0911fd44cd7ec9282d3972ad417765ed4e2752eb6565",
}
DEPENDENCY_HASHES = {
    "delivery.v2.json": "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    "resolved-inputs.v2.json": "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "c2-plan-stage-schema.v3.json": "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    "fact-plane.v1.json": "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    D9: "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    D9_CHECKER: "a905ab0e4b932c2ef4c565e847a12cb398abf9cd7a74abd92f95cbc85ffc8717",
    "d9-exit-contract.v1.13.review-independent-prefreeze.json": "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
}
EXPECTED_V2 = {"positive": 263, "adversarial": 68, "reducer": 12288, "traces": 78, "mutations": 42}
EXPECTED_V3 = {"positive": 11, "adversarial": 12, "reducer": 12288, "traces": 78, "totality": 522, "rules": 28, "admitted": 148, "invalid": 2156, "mutations": 36, "escapes": 6}
EXPECTED_FSM_TRACES = 78
EXPECTED_FSM_TOTALITY = 522
EXPECTED_REDUCER = 12288
EXPECTED_FINALIZER = {"full": 2304, "admitted": 148, "invalid": 2156, "goldens": 7}
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

class StrictJsonError(ValueError):
    pass

class EvalFailure(RuntimeError):
    pass

class Report:
    def __init__(self) -> None:
        self.positive = 0
        self.adversarial = 0
        self.failures: list[str] = []
    def expect(self, condition: bool, label: str) -> None:
        self.positive += 1
        if not condition:
            self.failures.append(label)
    def reject(self, thunk: Callable[[], Any], label: str) -> None:
        self.adversarial += 1
        try:
            value = thunk()
        except Exception:
            return
        if value is not False:
            self.failures.append(label)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha_ref(data: bytes) -> str:
    return "sha256:" + sha(data)

def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def compact_sha(value: Any) -> str:
    return sha_ref(compact(value))

def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in rows:
        if key in out:
            raise StrictJsonError("duplicate key")
        out[key] = value
    return out

def reject_constant(value: str) -> None:
    raise StrictJsonError("nonfinite " + value)

def reject_float(value: str) -> None:
    raise StrictJsonError("float " + value)

def strict_loads(source: str, dependency: bool = False) -> Any:
    if dependency:
        return json.loads(source, object_pairs_hook=pairs, parse_constant=reject_constant, parse_float=Decimal)
    return json.loads(source, object_pairs_hook=pairs, parse_constant=reject_constant, parse_float=reject_float)

def read_hashed(name: str, expected: str, dependency: bool = False) -> tuple[Any, bytes]:
    raw = (HERE / name).read_bytes()
    if sha(raw) != expected:
        raise StrictJsonError(name + " hash mismatch")
    return strict_loads(raw.decode("utf-8"), dependency), raw

class SnapshotLoader:
    def __init__(self, path: pathlib.Path, source: bytes):
        self.path = path
        self.source = source
    def create_module(self, spec: Any) -> None:
        return None
    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.path), "exec", dont_inherit=True), module.__dict__)

def execute_verified(name: str, expected: str, module_name: str) -> types.ModuleType:
    path = (HERE / name).resolve()
    source = path.read_bytes()
    if sha(source) != expected:
        raise StrictJsonError(name + " executable hash mismatch")
    loader = SnapshotLoader(path, source)
    spec = importlib.util.spec_from_file_location(module_name, path, loader=loader)
    if spec is None or spec.loader is None:
        raise StrictJsonError(name + " spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def exact_keys(value: Any, keys: list[str]) -> bool:
    return type(value) is dict and list(value) == keys

def u64(value: Any) -> bool:
    return type(value) is int and 0 <= value <= U64_MAX

def preserved_manifest() -> tuple[list[dict[str, str]], str]:
    rows = [{"path": name, "sha256": digest} for name, digest in PRESERVED_HASHES.items()]
    return rows, sha_ref(compact(rows))

def pyc_snapshot() -> dict[str, str]:
    return {
        str(path.relative_to(HERE)): sha(path.read_bytes())
        for path in sorted(HERE.rglob("*.pyc"))
    }

def projection_selector_hashes(source: dict[str, Any], selectors: list[str]) -> list[dict[str, str]]:
    return [
        {"selector": "/" + key, "sha256": compact_sha(source[key])}
        for key in selectors
    ]

def rename_v4_to_v3(value: Any) -> Any:
    if type(value) is dict:
        return {key.replace("V4", "V3"): rename_v4_to_v3(item) for key, item in value.items()}
    if type(value) is list:
        return [rename_v4_to_v3(item) for item in value]
    if type(value) is str:
        return value.replace("V4", "V3")
    return copy.deepcopy(value)

def v3_protocol_preservation_errors(p: dict[str, Any], v3p: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        current = p["orderingAndStateMachineV4"]
        prior = v3p["orderingAndStateMachineV3"]
        exact_pairs = [
            ("model", "model"), ("nominalTypes", "nominalTypes"),
            ("allowedReferencePaths", "allowedReferencePaths"),
            ("operandUnionV4", "operandUnionV3"), ("guardUnionV4", "guardUnionV3"),
            ("actionUnionV4", "actionUnionV3"), ("eventUnionV4", "eventUnionV3"),
            ("eventSelectorUnionV4", "eventSelectorUnionV3"),
            ("transitionRuleSchemaV4", "transitionRuleSchemaV3"),
            ("stateRecordV4", "stateRecordV3"), ("initialState", "initialState"),
            ("providerFaultPermittedPhases", "providerFaultPermittedPhases"),
            ("cancelPermittedPhases", "cancelPermittedPhases"),
            ("transitionRulesV4", "transitionRulesV3"), ("fallbackRule", "fallbackRule"),
            ("phaseEventCompatibility", "phaseEventCompatibility"),
            ("semanticConformanceVectors", "semanticConformanceVectors"),
            ("generatedExplanation", "generatedExplanation"),
        ]
        for new_key, old_key in exact_pairs:
            if not exact_json_equal(rename_v4_to_v3(current[new_key]), prior[old_key]):
                errors.append("v3 protocol drift " + new_key)
        old_domain = prior["modelCheckDomain"]
        new_domain = current["modelCheckDomain"]
        for key in old_domain:
            if key == "requiredEquality":
                continue
            if key == "semanticForksRequired":
                if new_domain[key][:len(old_domain[key])] != old_domain[key]:
                    errors.append("v3 model semantic forks")
            elif not exact_json_equal(new_domain[key], old_domain[key]):
                errors.append("v3 model domain " + key)
        old_pre = prior["prechecksV3"]
        new_pre = rename_v4_to_v3(current["prechecksV4"])
        retained_pre_fields = {
            "faultAbsorption": ["when", "priority"],
            "runtimeStateAndEventClosedShape": ["priority"],
            "preInvariantCheck": ["priority", "set"],
            "terminalOutputPrecheck": ["when", "actions", "priority"],
            "framePrecheck": ["when", "accept", "onAccept", "onReject", "priority"],
            "firstMatchingRule": ["priority", "rules"],
            "postInvariantCheck": ["priority", "set"],
            "atomicCommit": ["priority", "rule"],
        }
        if new_pre["evaluationOrder"] != old_pre["evaluationOrder"]:
            errors.append("v3 precheck order drift")
        for record, fields in retained_pre_fields.items():
            if any(not exact_json_equal(new_pre[record][field], old_pre[record][field]) for field in fields):
                errors.append("v3 precheck retained drift " + record)
    except (KeyError, TypeError, ValueError) as exc:
        errors.append("v3 protocol preservation escape " + type(exc).__name__)
    return errors

def v3_delivery_preservation_errors(d: dict[str, Any], v3d: dict[str, Any]) -> list[str]:
    try:
        current = rename_v4_to_v3(d["hostFinalizerBoundaryV4"])
        prior = copy.deepcopy(v3d["hostFinalizerBoundaryV3"])
        domain = current["finiteContextDomain"]
        del domain["tupleRecordV3Schema"]
        del domain["admissionRuleMetadata"]
        domain["tupleEncoding"] = prior["finiteContextDomain"]["tupleEncoding"]
        domain["admittedTupleCommitment"] = prior["finiteContextDomain"]["admittedTupleCommitment"]
        current["hostFinalizerContextV3Schema"]["fields"]["schemaVersion"] = prior["hostFinalizerContextV3Schema"]["fields"]["schemaVersion"]
        return [] if exact_json_equal(current, prior) else ["v3 finalizer semantic drift outside tuple repair"]
    except (KeyError, TypeError, ValueError) as exc:
        return ["v3 delivery preservation escape " + type(exc).__name__]

def variant_map(union: dict[str, Any]) -> dict[str, dict[str, Any]]:
    variants = union.get("variants")
    if type(variants) is not list:
        raise ValueError("variants")
    out = {}
    for row in variants:
        tag = row.get("tagValue") if type(row) is dict else None
        if type(tag) is not str or tag in out:
            raise ValueError("variant tag")
        out[tag] = row
    return out

def exact_json_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return list(left) == list(right) and all(exact_json_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_json_equal(a, b) for a, b in zip(left, right))
    return left == right

def nominal_schema_ok(schema: Any, value: Any, check_enum: bool = True) -> bool:
    if type(schema) is not dict or "jsonType" not in schema:
        return False
    jt = schema["jsonType"]
    types = [jt] if type(jt) is str else jt
    if type(types) is not list or not types or len(types) != len(set(types)) or any(x not in {"null", "boolean", "integer", "string"} for x in types):
        return False
    if value is None:
        valid = "null" in types
    elif type(value) is bool:
        valid = "boolean" in types
    elif type(value) is int:
        minimum = schema.get("minimum", -U64_MAX - 1)
        maximum = schema.get("maximum", U64_MAX)
        valid = type(minimum) is int and type(maximum) is int and "integer" in types and minimum <= value <= maximum
    elif type(value) is str:
        valid = "string" in types
    else:
        valid = False
    if not valid:
        return False
    if check_enum and "enum" in schema and not any(exact_json_equal(value, item) for item in schema["enum"]):
        return False
    return True

def nominal_ok(machine: dict[str, Any], nominal: str, value: Any) -> bool:
    return nominal_schema_ok(machine.get("nominalTypes", {}).get(nominal), value)

def nominal_oracle(schema: dict[str, Any], value: Any) -> bool:
    jt = schema["jsonType"]
    declared = {jt} if type(jt) is str else set(jt)
    actual = "null" if value is None else "boolean" if type(value) is bool else "integer" if type(value) is int else "string" if type(value) is str else "other"
    if actual not in declared:
        return False
    if actual == "integer" and not (schema.get("minimum", -U64_MAX - 1) <= value <= schema.get("maximum", U64_MAX)):
        return False
    return "enum" not in schema or any(type(value) is type(item) and value == item for item in schema["enum"])

def nominal_probe_checks(p: dict[str, Any]) -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    try:
        machine = p["orderingAndStateMachineV4"]
        plan = machine["nominalTypeProbePlanV4"]
        for nominal, schema in machine["nominalTypes"].items():
            corpus = list(plan["baseCorpus"]) + list(schema.get("enum", []))
            for value in corpus:
                if nominal_ok(machine, nominal, value) != nominal_oracle(schema, value):
                    errors.append("nominal probe divergence " + nominal + "/" + repr(value))
                count += 1
        for row in plan["requiredNamedProbes"]:
            if nominal_ok(machine, row["nominalType"], row["value"]) is not row["accept"]:
                errors.append("named nominal probe " + row["id"])
            count += 1
        for row in plan["syntheticConsistencyProbes"]:
            if nominal_schema_ok(row["schema"], row["value"]) is not row["accept"]:
                errors.append("synthetic nominal probe " + row["id"])
            count += 1
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append("nominal probe escape " + type(exc).__name__)
    return errors, count

def allowed_reference_map(machine: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = machine.get("allowedReferencePaths")
    if type(rows) is not list:
        raise ValueError("reference rows")
    out = {}
    for row in rows:
        if not exact_keys(row, ["path", "nominalType", "availability", "readContexts"]):
            raise ValueError("reference row")
        if row["path"] in out:
            raise ValueError("duplicate reference")
        out[row["path"]] = row
    return out

def operand_error(machine: dict[str, Any], node: Any, context: str) -> str | None:
    try:
        variants = variant_map(machine["operandUnionV4"])
        if type(node) is not dict or node.get("kind") not in variants:
            return "operand variant"
        schema = variants[node["kind"]]
        if list(node) != schema["required"] or schema["optional"] != []:
            return "operand fields"
        if node["kind"] == "constant":
            if not nominal_ok(machine, node["nominalType"], node["value"]):
                return "constant nominal type"
        else:
            refs = allowed_reference_map(machine)
            row = refs.get(node["path"])
            if row is None or row["nominalType"] != node["nominalType"]:
                return "reference path/type"
            if context not in row["readContexts"]:
                return "reference context"
        return None
    except (KeyError, TypeError, ValueError):
        return "hostile operand"

def guard_error(machine: dict[str, Any], node: Any, context: str = "guard", depth: int = 1, counter: list[int] | None = None) -> str | None:
    counter = counter if counter is not None else [0]
    counter[0] += 1
    bounds = machine["grammarBounds"]
    if depth > bounds["maxGuardDepth"] or counter[0] > bounds["maxGuardNodes"]:
        return "guard bound"
    try:
        variants = variant_map(machine["guardUnionV4"])
        if type(node) is not dict or node.get("op") not in variants:
            return "guard variant"
        schema = variants[node["op"]]
        if list(node) != schema["required"] or schema["optional"] != []:
            return "guard fields"
        op = node["op"]
        if op in ("all", "any"):
            if type(node["items"]) is not list or not 1 <= len(node["items"]) <= 64:
                return "guard items"
            for item in node["items"]:
                err = guard_error(machine, item, context, depth + 1, counter)
                if err:
                    return err
        elif op == "not":
            return guard_error(machine, node["item"], context, depth + 1, counter)
        elif op in ("eq", "neq", "lt"):
            left = operand_error(machine, node["left"], context)
            right = operand_error(machine, node["right"], context)
            if left or right:
                return left or right
            if node["left"]["nominalType"] != node["right"]["nominalType"]:
                return "guard type equality"
            if op == "lt" and node["left"]["nominalType"] != "uint64":
                return "lt type"
        elif op == "between":
            for key in ("value", "minimum", "maximum"):
                err = operand_error(machine, node[key], context)
                if err or node[key]["nominalType"] != "uint64":
                    return err or "between type"
        elif op == "in":
            if operand_error(machine, node["value"], context):
                return "in value"
            if type(node["values"]) is not list or not 1 <= len(node["values"]) <= 64:
                return "in values"
            encoded = []
            for item in node["values"]:
                err = operand_error(machine, item, context)
                if err or item["nominalType"] != node["value"]["nominalType"]:
                    return err or "in type"
                encoded.append(compact(item))
            if len(encoded) != len(set(encoded)):
                return "in duplicate"
        elif op == "phaseIn":
            if type(node["values"]) is not list or not node["values"] or len(node["values"]) != len(set(node["values"])) or any(x not in machine["nominalTypes"]["phase"]["enum"] for x in node["values"]):
                return "phaseIn values"
        elif op == "eventKindIn":
            if type(node["values"]) is not list or not node["values"] or len(node["values"]) != len(set(node["values"])) or any(x not in machine["nominalTypes"]["event-kind"]["enum"] for x in node["values"]):
                return "eventKindIn values"
        elif op == "checkedAddCompare":
            for key in ("left", "addend", "right"):
                err = operand_error(machine, node[key], context)
                if err or node[key]["nominalType"] != "uint64":
                    return err or "checked compare type"
            if node["comparison"] not in ("eq", "lt"):
                return "checked comparison"
        elif op == "directionCounterLessThan":
            err = operand_error(machine, node["limit"], context)
            if err or node["limit"]["nominalType"] != "uint64":
                return err or "counter limit"
        return None
    except (KeyError, TypeError, ValueError):
        return "hostile guard"

def action_error(machine: dict[str, Any], node: Any) -> str | None:
    try:
        variants = variant_map(machine["actionUnionV4"])
        if type(node) is not dict or node.get("op") not in variants:
            return "action variant"
        schema = variants[node["op"]]
        if list(node) != schema["required"] or schema["optional"] != []:
            return "action fields"
        op = node["op"]
        refs = allowed_reference_map(machine)
        if op in ("set", "copy", "checkedAdd"):
            target = node["target"]
            if target not in machine["actionUnionV4"]["mutableStateTargets"] or target not in refs:
                return "action target"
            target_type = refs[target]["nominalType"]
            key = "value" if op == "set" else ("source" if op == "copy" else "addend")
            err = operand_error(machine, node[key], "action")
            if err or node[key]["nominalType"] != target_type:
                return err or "action type"
            if op == "checkedAdd" and target_type != "uint64":
                return "checked target type"
        elif op == "checkedIncrementDirectionCounter":
            err = operand_error(machine, node["amount"], "action")
            if err or node["amount"]["nominalType"] != "uint64":
                return err or "increment type"
        return None
    except (KeyError, TypeError, ValueError):
        return "hostile action"

def selector_error(machine: dict[str, Any], node: Any) -> str | None:
    try:
        variants = variant_map(machine["eventSelectorUnionV4"])
        if type(node) is not dict or node.get("selectorKind") not in variants:
            return "selector variant"
        schema = variants[node["selectorKind"]]
        if list(node) != schema["required"] or schema["optional"] != []:
            return "selector fields"
        if node["selectorKind"] == "frame":
            if node["frameType"] == "UNKNOWN_FRAME" or node["frameType"] not in machine["nominalTypes"]["frame-type"]["enum"]:
                return "selector frame"
        elif node["selectorKind"] == "event-kind":
            if node["kind"] == "frame" or node["kind"] not in machine["nominalTypes"]["event-kind"]["enum"]:
                return "selector kind"
        else:
            values = node["kinds"]
            if type(values) is not list or not values or len(values) != len(set(values)) or any(x not in machine["nominalTypes"]["event-kind"]["enum"] for x in values):
                return "selector set"
        return None
    except (KeyError, TypeError, ValueError):
        return "hostile selector"

def ast_event_references(node: Any) -> set[str]:
    out: set[str] = set()
    if type(node) is dict:
        if node.get("kind") == "reference" and type(node.get("path")) is str and node["path"].startswith("event."):
            out.add(node["path"][6:])
        for value in node.values():
            out |= ast_event_references(value)
    elif type(node) is list:
        for value in node:
            out |= ast_event_references(value)
    return out

def protocol_errors(p: Any, v2p: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        expected_root = [
            "artifact", "version", "status", "reviewStatus", "purpose",
            "predecessorRejection", "retainedV3RepairBoundary", "dependencyPins", "retainedV2SemanticProjection",
            "schemaLanguageV4", "orderingAndStateMachineV4", "d9JoinV4",
            "narrowJoinReferencesV4", "closureClaims", "residuals", "nonClaims",
            "authority", "supersedesOnlyIfIndependentlyAcceptedAndApplied",
        ]
        if not exact_keys(p, expected_root):
            errors.append("protocol root")
            return errors
        if p["artifact"] != "opensip.rust-provider-protocol" or p["version"] != 4 or p["status"] != STATUS or p["reviewStatus"] != "AWAITING-INDEPENDENT-REVIEW":
            errors.append("protocol identity/status")
        rejection = p["predecessorRejection"]
        if rejection.get("sha256") != REVIEW_SHA or rejection.get("decision") != "REJECT" or rejection.get("blockingFindings") != [
            "RPPV3-PF-01-NULL-NOMINAL-TYPE-CONTRADICTS-EXACT-TYPE",
            "RPPV3-PF-02-TRANSITION-FAULT-ATOMICITY-AND-PRECHECK-ORDER-DIVERGE",
            "RPPV3-PF-03-ADMITTED-TUPLE-COMMITMENT-ENCODING-UNDECLARED-FIELD",
        ]:
            errors.append("protocol rejection binding")
        boundary = p["retainedV3RepairBoundary"]
        expected_frozen = [{"path": name, "sha256": PRESERVED_HASHES[name]} for name in [V3_PROTOCOL, V3_CHECKER, V3_RESPONSE, V3_DELIVERY, V3_RI, V3_REVIEW]]
        if boundary.get("frozenSubjects") != expected_frozen or boundary.get("retainedExecutableCounts") != {
            "semanticPositive": 11, "adversarial": 12, "reducerTuples": 12288,
            "fsmTraces": 78, "fsmTotalityComparisons": 522, "transitionRules": 28,
            "finalizerFullDomain": 2304, "finalizerAdmitted": 148, "finalizerInvalid": 2156,
            "finalizerGoldens": 7, "mutations": 36, "harnessEscapes": 6,
        } or len(boundary.get("permittedRepairs", [])) != 3:
            errors.append("v3 repair boundary")
        pins = p["dependencyPins"]
        if [{"path": row.get("path"), "sha256": row.get("sha256")} for row in pins[:6]] != expected_frozen:
            errors.append("v3 dependency pins")
        excluded = {
            "artifact", "version", "status", "reviewStatus", "purpose",
            "orderingAndStateMachine", "d9Join", "narrowJoinReferences",
            "rejectionBasis", "residuals", "authority", "nonClaims",
            "supersedesOnlyIfIndependentlyAcceptedAndApplied",
        }
        inherited = [k for k in v2p if k not in excluded]
        proj = p["retainedV2SemanticProjection"]
        if proj.get("inheritedTopLevelSelectors") != inherited or proj.get("source", {}).get("sha256") != PRESERVED_HASHES[V2_PROTOCOL]:
            errors.append("protocol retained projection")
        schema_language = p["schemaLanguageV4"]
        if not exact_keys(schema_language, [
            "closedMap", "taggedUnion", "exactType", "array",
            "referencePathGrammar", "recursiveBounds", "artifactFailure",
            "runtimeFailure",
        ]):
            errors.append("schema language fields")
        if schema_language.get("recursiveBounds") != {
            "maxGuardDepth": 16,
            "maxGuardNodes": 256,
            "maxActionsPerList": 64,
            "maxRules": 64,
            "maxInvariants": 64,
            "maxArrayItems": 64,
            "maxUtf8BytesPerIdentifier": 128,
            "maxAstCanonicalJsonBytes": 262144,
        }:
            errors.append("recursive grammar bounds")
        source_machine = p["orderingAndStateMachineV4"]
        if not exact_keys(source_machine, [
            "model", "precheckResultUnionV4", "transitionResultUnionV4", "transitionTransactionV4",
            "nominalTypes", "nominalTypeProbePlanV4", "allowedReferencePaths", "operandUnionV4",
            "guardUnionV4", "actionUnionV4", "eventUnionV4",
            "eventSelectorUnionV4", "transitionRuleSchemaV4", "stateRecordV4",
            "initialState", "providerFaultPermittedPhases",
            "cancelPermittedPhases", "precheckRecordSchemasV4", "prechecksV4", "transitionRulesV4",
            "fallbackRule", "phaseEventCompatibility", "modelCheckDomain",
            "semanticConformanceVectors", "generatedExplanation",
        ]):
            errors.append("machine fields")
        m = dict(source_machine)
        m["grammarBounds"] = schema_language["recursiveBounds"]
        if "Null is admitted if and only if" not in schema_language["exactType"] or "enum" not in schema_language["exactType"] or "nullable-uint64 is exactly uint64-or-null" not in schema_language["exactType"] or "nullable-boolean is exactly boolean-or-null" not in schema_language["exactType"]:
            errors.append("exact null typing declaration")
        if m["nominalTypes"].get("nullable-uint64") != {"jsonType": ["integer", "null"], "minimum": 0, "maximum": U64_MAX, "booleanExcluded": True} or m["nominalTypes"].get("nullable-boolean") != {"jsonType": ["boolean", "null"]}:
            errors.append("exact nullable nominal types")
        for nominal, schema in m["nominalTypes"].items():
            jt = schema.get("jsonType")
            types = [jt] if type(jt) is str else jt
            if type(types) is not list or not types or len(types) != len(set(types)) or any(x not in {"null", "boolean", "integer", "string"} for x in types):
                errors.append("nominal jsonType " + nominal)
                break
            if "enum" in schema and (type(schema["enum"]) is not list or any(not nominal_schema_ok(schema, value, False) for value in schema["enum"])):
                errors.append("nominal enum/jsonType coherence " + nominal)
                break
        if [row["tagValue"] for row in m["precheckResultUnionV4"]["variants"]] != ["CONTINUE", "STOP", "STAGED_RULE", "STOP_STAGED_RESULT"] or [row["tagValue"] for row in m["transitionResultUnionV4"]["variants"]] != ["ABSORB_UNCHANGED", "COMMIT", "CONTROLLED_FAULT_COMMIT", "RUNTIME_FAULT_ROLLBACK", "REJECT_NON_OBJECT_STATE"]:
            errors.append("closed result unions")
        if m["precheckResultUnionV4"].get("closed") is not True or m["transitionResultUnionV4"].get("closed") is not True or len(m["transitionTransactionV4"].get("orderedAlgorithm", [])) != 10:
            errors.append("closed transaction declaration")
        if m["eventUnionV4"].get("runtimeUnknownFieldOrVariantFate") != "FAULT_FROM_ORIGINAL_NO_PARTIAL_COMMIT":
            errors.append("runtime unknown event fate")
        if m["stateRecordV4"].get("evaluation") != "Evaluate every invariant in listed order on valid input state before prechecks and again on the staged post-action state. A false assertion whose when is true, or any runtime evaluation failure, faults atomically. FAULT is absorbing and bypasses invariant evaluation.":
            errors.append("invariant evaluation fate")
        if m["actionUnionV4"].get("readSemantics") != "LEFT_TO_RIGHT_SEQUENTIAL_UPDATED_STATE" or "Commit once only" not in m["actionUnionV4"].get("commitSemantics", ""):
            errors.append("action read/commit semantics")
        if m["actionUnionV4"].get("overflow") != "CHECKED_UINT64_RUNTIME_FAILURE_TO_ATOMIC_FAULT":
            errors.append("action overflow semantics")
        if [x["tagValue"] for x in m["operandUnionV4"]["variants"]] != ["constant", "reference"]:
            errors.append("operand variants")
        expected_guards = ["true", "all", "any", "not", "eq", "neq", "lt", "between", "in", "phaseIn", "eventKindIn", "checkedAddCompare", "directionMatchesFrameSchema", "sequenceEqualsDirectionCounter", "directionCounterLessThan"]
        if [x["tagValue"] for x in m["guardUnionV4"]["variants"]] != expected_guards:
            errors.append("guard variants")
        if [x["tagValue"] for x in m["actionUnionV4"]["variants"]] != ["set", "copy", "checkedAdd", "checkedIncrementDirectionCounter"]:
            errors.append("action variants")
        if [x["tagValue"] for x in m["eventSelectorUnionV4"]["variants"]] != ["frame", "event-kind", "event-kind-set"]:
            errors.append("selector variants")
        if list(m["stateRecordV4"]["fieldNominalTypes"]) != m["stateRecordV4"]["required"]:
            errors.append("state fields/order")
        if list(m["initialState"]) != m["stateRecordV4"]["required"]:
            errors.append("initial order")
        if not runtime_state_valid(m, m["initialState"]):
            errors.append("initial state type")
        invariants = m["stateRecordV4"]["stateInvariantsV4"]
        if len(invariants) != 5 or len({row.get("id") for row in invariants}) != 5:
            errors.append("invariant count/id")
        for row in invariants:
            if not exact_keys(row, ["id", "when", "assert"]) or guard_error(m, row.get("when"), "invariant") or guard_error(m, row.get("assert"), "invariant"):
                errors.append("invariant AST")
                break
        rules = m["transitionRulesV4"]
        if len(rules) != 28 or [r.get("priority") for r in rules] != list(range(1, 29)) or len({r.get("id") for r in rules}) != 28:
            errors.append("rule priority/count")
        semantic_fields = {"repositoryMode", "stageCount", "batchIndex", "firstCandidateOrdinal", "candidateCount", "budgetMatchesCurrentStage", "budgetUnit"}
        frame_variant = variant_map(m["eventUnionV4"])["frame"]
        nonnull = frame_variant["constraints"]["nonNullSemanticFieldsByFrameType"]
        for row in rules:
            if not exact_keys(row, ["id", "priority", "phaseIn", "eventSelector", "guard", "actions"]):
                errors.append("rule fields")
                break
            if type(row["phaseIn"]) is not list or not row["phaseIn"] or len(row["phaseIn"]) != len(set(row["phaseIn"])) or any(x == "FAULT" or x not in m["nominalTypes"]["phase"]["enum"] for x in row["phaseIn"]):
                errors.append("rule phases")
                break
            if selector_error(m, row["eventSelector"]) or guard_error(m, row["guard"]):
                errors.append("rule selector/guard")
                break
            if type(row["actions"]) is not list or len(row["actions"]) > 64 or any(action_error(m, a) for a in row["actions"]):
                errors.append("rule actions")
                break
            refs = ast_event_references(row["guard"]) | ast_event_references(row["actions"])
            used = refs & semantic_fields
            if used:
                if row["eventSelector"]["selectorKind"] != "frame" or not used <= set(nonnull[row["eventSelector"]["frameType"]]):
                    errors.append("rule event reference availability")
                    break
        fallback = m["fallbackRule"]
        last = rules[-1]
        if last["id"] != fallback.get("id") or last["priority"] != 28 or last["guard"] != {"op": "true"} or last["actions"] != [fallback.get("onlyAction")]:
            errors.append("fallback exact")
        compatibility: dict[str, list[str]] = {}
        for row in rules[:-1]:
            key = json.dumps(row["eventSelector"], separators=(",", ":"), sort_keys=True)
            for phase in row["phaseIn"]:
                compatibility.setdefault(phase, [])
                if key not in compatibility[phase]:
                    compatibility[phase].append(key)
        expected_compat = [
            {"phase": phase, "nonFallbackSelectorCanonicalJson": compatibility.get(phase, []), "otherwise": "T028-TOTAL-FALLBACK"}
            for phase in m["nominalTypes"]["phase"]["enum"] if phase != "FAULT"
        ]
        if m["phaseEventCompatibility"] != expected_compat:
            errors.append("phase/event compatibility")
        pre = m["prechecksV4"]
        if pre.get("evaluationOrder") != ["faultAbsorption", "runtimeStateAndEventClosedShape", "preInvariantCheck", "terminalOutputPrecheck", "framePrecheck", "firstMatchingRule", "postInvariantCheck", "atomicCommit"]:
            errors.append("precheck order")
        schemas = m["precheckRecordSchemasV4"]
        if list(pre) != schemas["pipeline"]["required"] or schemas["pipeline"].get("closed") is not True or schemas["pipeline"].get("optional") != []:
            errors.append("closed precheck pipeline")
        for record_schema in schemas["records"]:
            record = pre.get(record_schema["recordName"])
            if record_schema.get("closed") is not True or record_schema.get("optional") != [] or type(record) is not dict or list(record) != record_schema["required"]:
                errors.append("closed precheck record " + record_schema.get("recordName", "?"))
                break
        result_fields = [
            pre["faultAbsorption"]["onTrue"], pre["faultAbsorption"]["onFalse"],
            pre["runtimeStateAndEventClosedShape"]["onValid"], pre["runtimeStateAndEventClosedShape"]["onInvalid"],
            pre["preInvariantCheck"]["onPass"], pre["preInvariantCheck"]["onFailure"],
            pre["terminalOutputPrecheck"]["onTrue"], pre["terminalOutputPrecheck"]["onFalse"],
            pre["framePrecheck"]["onAcceptResult"], pre["framePrecheck"]["onRejectResult"],
            pre["firstMatchingRule"]["onOrdinaryMatch"], pre["firstMatchingRule"]["onFallbackMatch"],
            pre["firstMatchingRule"]["onGuardFailure"], pre["firstMatchingRule"]["onActionFailure"], pre["firstMatchingRule"]["onNoMatch"],
            pre["postInvariantCheck"]["onPass"], pre["postInvariantCheck"]["onFailure"], pre["atomicCommit"]["onPublish"],
        ]
        if any(not precheck_result_valid(m, value) for value in result_fields):
            errors.append("precheck result encoding")
        if pre["faultAbsorption"]["priority"] != 1 or pre["terminalOutputPrecheck"].get("stopAfterTrue") is not True or pre["terminalOutputPrecheck"].get("owner") != "terminal-output-precheck" or pre["framePrecheck"].get("onRejectActionsAreDiscarded") is not True or pre["firstMatchingRule"].get("fallbackOwner") != "T028-TOTAL-FALLBACK" or pre["firstMatchingRule"].get("fallbackCommitsAcceptedFramePrecheckWrites") is not True:
            errors.append("precheck control semantics")
        exact_outcomes = [
            (pre["faultAbsorption"]["onTrue"], {"outcome": "STOP", "transitionResultKind": "ABSORB_UNCHANGED"}),
            (pre["runtimeStateAndEventClosedShape"]["onInvalid"], {"outcome": "STOP", "transitionResultKind": "RUNTIME_FAULT_ROLLBACK"}),
            (pre["terminalOutputPrecheck"]["onTrue"], {"outcome": "STOP", "transitionResultKind": "CONTROLLED_FAULT_COMMIT"}),
            (pre["framePrecheck"]["onRejectResult"], {"outcome": "STOP", "transitionResultKind": "RUNTIME_FAULT_ROLLBACK"}),
            (pre["firstMatchingRule"]["onOrdinaryMatch"], {"outcome": "STAGED_RULE", "transitionResultKind": "COMMIT"}),
            (pre["firstMatchingRule"]["onFallbackMatch"], {"outcome": "STAGED_RULE", "transitionResultKind": "CONTROLLED_FAULT_COMMIT"}),
            (pre["postInvariantCheck"]["onFailure"], {"outcome": "STOP", "transitionResultKind": "RUNTIME_FAULT_ROLLBACK"}),
            (pre["atomicCommit"]["onPublish"], {"outcome": "STOP_STAGED_RESULT"}),
        ]
        if any(not exact_json_equal(actual, expected) for actual, expected in exact_outcomes):
            errors.append("exact precheck outcomes")
        for node in [pre["faultAbsorption"]["when"], pre["terminalOutputPrecheck"]["when"], pre["framePrecheck"]["when"], pre["framePrecheck"]["accept"]]:
            if guard_error(m, node):
                errors.append("precheck guard")
        for actions in [pre["terminalOutputPrecheck"]["actions"], pre["framePrecheck"]["onAccept"], pre["framePrecheck"]["onReject"]]:
            if any(action_error(m, a) for a in actions):
                errors.append("precheck action")
        if [v.get("id") for v in m["semanticConformanceVectors"]] != [
            "SEM-ACTION-SEQUENTIAL-UPDATED-READ", "SEM-GUARD-ALL-SHORT-CIRCUIT",
            "SEM-GUARD-ANY-SHORT-CIRCUIT", "SEM-ACTION-OVERFLOW-ATOMIC",
            "SEM-POST-INVARIANT-FAILURE-FAULTS-ATOMically",
            "SEM-RUNTIME-EVENT-SHAPE-FAILURE",
        ]:
            errors.append("semantic vectors")
        model_domain = m["modelCheckDomain"]
        if model_domain.get("retainedV3TraceCount") != 78 or model_domain.get("retainedV3TotalityComparisonCount") != 522 or model_domain.get("requiredRepairWitnesses") != [
            "RV4-FAULT-ABSORB-MALFORMED", "RV4-MALFORMED-MISSING-PHASE",
            "RV4-MALFORMED-WRONG-TYPE-PRESERVED", "RV4-MALFORMED-UNKNOWN-FIELD-PRESERVED",
            "RV4-NONOBJECT-CLOSED-REJECT", "RV4-TERMINAL-OUTPUT-STOPS",
            "RV4-FALLBACK-FRAME-COMMITS-SEQUENCE", "RV4-REJECTED-FRAME-ROLLS-BACK",
            "RV4-ORDINARY-FRAME-COMMITS", "RV4-PREINVARIANT-ROLLS-BACK",
            "RV4-POSTINVARIANT-ROLLS-BACK", "RV4-FAULT-ABSORPTION-PRECEDES-EVENT-SHAPE",
        ]:
            errors.append("model repair domain")
        if p["authority"].get("selfReview") is not False or p["authority"].get("applied") is not False:
            errors.append("protocol authority")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        errors.append("hostile protocol: " + type(exc).__name__)
    return errors

def runtime_state_valid(machine: dict[str, Any], state: Any) -> bool:
    try:
        schema = machine["stateRecordV4"]
        if not exact_keys(state, schema["required"]):
            return False
        return all(nominal_ok(machine, typ, state[field]) for field, typ in schema["fieldNominalTypes"].items())
    except (KeyError, TypeError):
        return False

def runtime_event_valid(machine: dict[str, Any], event: Any) -> bool:
    try:
        variants = variant_map(machine["eventUnionV4"])
        if type(event) is not dict or event.get("kind") not in variants:
            return False
        row = variants[event["kind"]]
        if list(event) != row["required"] or row["optional"] != []:
            return False
        if not all(nominal_ok(machine, typ, event[field]) for field, typ in row["fieldNominalTypes"].items()):
            return False
        if event["kind"] == "frame":
            constraints = row["constraints"]
            ft = event["frameType"]
            if ft not in constraints["frameTypeValues"]:
                return False
            nonnull = set(constraints["nonNullSemanticFieldsByFrameType"][ft])
            semantic = {"repositoryMode", "stageCount", "batchIndex", "firstCandidateOrdinal", "candidateCount", "budgetMatchesCurrentStage", "budgetUnit"}
            if any((event[field] is None) != (field not in nonnull) for field in semantic):
                return False
        return True
    except (KeyError, TypeError, ValueError):
        return False

def resolve_operand(machine: dict[str, Any], node: dict[str, Any], state: dict[str, Any], event: dict[str, Any], limits: dict[str, int]) -> Any:
    err = operand_error(machine, node, "action")
    if err and node.get("kind") == "reference":
        # Invariants and guards use the same exact path/type rules; only path/type matters at runtime.
        refs = allowed_reference_map(machine)
        row = refs.get(node.get("path"))
        if row is None or row["nominalType"] != node.get("nominalType"):
            raise EvalFailure(err)
    elif err and node.get("kind") == "constant":
        raise EvalFailure(err)
    if node["kind"] == "constant":
        return node["value"]
    prefix, field = node["path"].split(".", 1)
    source = state if prefix == "state" else event if prefix == "event" else limits
    if field not in source:
        raise EvalFailure("missing reference")
    value = source[field]
    if not nominal_ok(machine, node["nominalType"], value):
        raise EvalFailure("runtime reference type")
    return value

def eval_guard(machine: dict[str, Any], node: dict[str, Any], state: dict[str, Any], event: dict[str, Any], limits: dict[str, int], frames: dict[str, Any]) -> bool:
    if guard_error(machine, node):
        raise EvalFailure("ill typed guard")
    schema = variant_map(machine["guardUnionV4"])[node["op"]]
    alg = schema["runtimeAlgorithm"]
    if alg == "RETURN_TRUE":
        return True
    if alg == "EVALUATE_LEFT_TO_RIGHT_STOP_ON_FIRST_FALSE":
        for item in node["items"]:
            if not eval_guard(machine, item, state, event, limits, frames):
                return False
        return True
    if alg == "EVALUATE_LEFT_TO_RIGHT_STOP_ON_FIRST_TRUE":
        for item in node["items"]:
            if eval_guard(machine, item, state, event, limits, frames):
                return True
        return False
    if alg == "EVALUATE_ITEM_THEN_BOOLEAN_NEGATE":
        return not eval_guard(machine, node["item"], state, event, limits, frames)
    if alg in ("EVALUATE_LEFT_THEN_RIGHT_EXACT_EQUAL", "EVALUATE_LEFT_THEN_RIGHT_EXACT_NOT_EQUAL", "EVALUATE_LEFT_THEN_RIGHT_UINT64_LESS_THAN"):
        left = resolve_operand(machine, node["left"], state, event, limits)
        right = resolve_operand(machine, node["right"], state, event, limits)
        return left == right if alg.endswith("EXACT_EQUAL") else left != right if alg.endswith("EXACT_NOT_EQUAL") else left < right
    if alg == "EVALUATE_VALUE_MINIMUM_MAXIMUM_THEN_INCLUSIVE_UINT64_RANGE":
        value = resolve_operand(machine, node["value"], state, event, limits)
        minimum = resolve_operand(machine, node["minimum"], state, event, limits)
        maximum = resolve_operand(machine, node["maximum"], state, event, limits)
        return minimum <= value <= maximum
    if alg == "EVALUATE_VALUE_THEN_VALUES_LEFT_TO_RIGHT_EXACT_MEMBERSHIP":
        value = resolve_operand(machine, node["value"], state, event, limits)
        for item in node["values"]:
            if value == resolve_operand(machine, item, state, event, limits):
                return True
        return False
    if alg == "READ_UPDATED_STATE_PHASE_THEN_EXACT_MEMBERSHIP":
        return state["phase"] in node["values"]
    if alg == "READ_EVENT_KIND_THEN_EXACT_MEMBERSHIP":
        return event["kind"] in node["values"]
    if alg == "EVALUATE_LEFT_ADDEND_CHECKED_ADD_RIGHT_THEN_COMPARE":
        left = resolve_operand(machine, node["left"], state, event, limits)
        add = resolve_operand(machine, node["addend"], state, event, limits)
        right = resolve_operand(machine, node["right"], state, event, limits)
        if left > U64_MAX - add:
            raise EvalFailure("checked guard overflow")
        value = left + add
        return value == right if node["comparison"] == "eq" else value < right
    if alg == "LOOK_UP_EVENT_FRAME_TYPE_IN_PINNED_FRAME_SCHEMA_AND_EXACT_COMPARE_DIRECTION":
        try:
            return event["direction"] == frames[event["frameType"]]["direction"]
        except KeyError as exc:
            raise EvalFailure("frame direction") from exc
    if alg == "SELECT_COUNTER_BY_EVENT_DIRECTION_THEN_EXACT_UINT64_EQUALITY":
        key = "nextHostSequence" if event.get("direction") == "host-to-worker" else "nextWorkerSequence" if event.get("direction") == "worker-to-host" else None
        if key is None:
            raise EvalFailure("direction")
        return event["sequence"] == state[key]
    if alg == "SELECT_COUNTER_BY_EVENT_DIRECTION_EVALUATE_LIMIT_THEN_UINT64_LESS_THAN":
        key = "nextHostSequence" if event.get("direction") == "host-to-worker" else "nextWorkerSequence" if event.get("direction") == "worker-to-host" else None
        if key is None:
            raise EvalFailure("direction")
        return state[key] < resolve_operand(machine, node["limit"], state, event, limits)
    raise EvalFailure("unknown declared guard algorithm")

def apply_actions_raise(machine: dict[str, Any], actions: list[dict[str, Any]], state: dict[str, Any], event: dict[str, Any], limits: dict[str, int]) -> dict[str, Any]:
    staged = copy.deepcopy(state)
    schemas = variant_map(machine["actionUnionV4"])
    refs = allowed_reference_map(machine)
    for node in actions:
        err = action_error(machine, node)
        if err:
            raise EvalFailure(err)
        alg = schemas[node["op"]]["runtimeAlgorithm"]
        if alg == "EVALUATE_VALUE_AGAINST_CURRENT_STAGED_STATE_THEN_ASSIGN_TARGET":
            value = resolve_operand(machine, node["value"], staged, event, limits)
            staged[node["target"][6:]] = value
        elif alg == "EVALUATE_SOURCE_AGAINST_CURRENT_STAGED_STATE_THEN_ASSIGN_TARGET":
            value = resolve_operand(machine, node["source"], staged, event, limits)
            staged[node["target"][6:]] = value
        elif alg == "READ_TARGET_AND_EVALUATE_ADDEND_FROM_CURRENT_STAGED_STATE_THEN_CHECKED_UINT64_ADD":
            field = node["target"][6:]
            add = resolve_operand(machine, node["addend"], staged, event, limits)
            if staged[field] > U64_MAX - add:
                raise EvalFailure("action overflow")
            staged[field] += add
        elif alg == "SELECT_COUNTER_BY_EVENT_DIRECTION_READ_CURRENT_STAGED_COUNTER_EVALUATE_AMOUNT_THEN_CHECKED_UINT64_ADD":
            field = "nextHostSequence" if event.get("direction") == "host-to-worker" else "nextWorkerSequence" if event.get("direction") == "worker-to-host" else None
            if field is None:
                raise EvalFailure("action direction")
            add = resolve_operand(machine, node["amount"], staged, event, limits)
            if staged[field] > U64_MAX - add:
                raise EvalFailure("counter overflow")
            staged[field] += add
        else:
            raise EvalFailure("unknown declared action algorithm")
        target_path = node.get("target")
        if target_path is None:
            target_path = "state." + field
        target_field = target_path[6:]
        if not nominal_ok(machine, refs[target_path]["nominalType"], staged[target_field]):
            raise EvalFailure("post action type")
    return staged

def fault(state: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(state)
    out["phase"] = "FAULT"
    return out

def transition_result_valid(machine: dict[str, Any], value: Any) -> bool:
    try:
        variants = variant_map(machine["transitionResultUnionV4"])
        if type(value) is not dict or value.get("resultKind") not in variants:
            return False
        row = variants[value["resultKind"]]
        if list(value) != row["required"] or row["optional"] != []:
            return False
        kind = value["resultKind"]
        if kind == "REJECT_NON_OBJECT_STATE":
            return True
        if type(value["state"]) is not dict:
            return False
        if kind == "COMMIT":
            return type(value["transitionRuleId"]) is str and value["transitionRuleId"] != "T028-TOTAL-FALLBACK" and runtime_state_valid(machine, value["state"])
        if kind == "CONTROLLED_FAULT_COMMIT":
            owner = value["owner"]
            rule_id = value["transitionRuleId"]
            return runtime_state_valid(machine, value["state"]) and value["state"]["phase"] == "FAULT" and owner in row["ownerEnum"] and ((owner == "terminal-output-precheck" and rule_id is None) or (owner == "T028-TOTAL-FALLBACK" and rule_id == "T028-TOTAL-FALLBACK"))
        if kind == "RUNTIME_FAULT_ROLLBACK":
            return value["failureStage"] in row["failureStageEnum"] and value["state"].get("phase") == "FAULT"
        return kind == "ABSORB_UNCHANGED"
    except (KeyError, TypeError, ValueError):
        return False

def precheck_result_valid(machine: dict[str, Any], value: Any) -> bool:
    try:
        variants = variant_map(machine["precheckResultUnionV4"])
        if type(value) is not dict or value.get("outcome") not in variants:
            return False
        row = variants[value["outcome"]]
        if list(value) != row["required"] or row["optional"] != []:
            return False
        return "transitionResultKind" not in value or value["transitionResultKind"] in row["transitionResultKindEnum"]
    except (KeyError, TypeError, ValueError):
        return False

def absorb_result(state: dict[str, Any]) -> dict[str, Any]:
    return {"resultKind": "ABSORB_UNCHANGED", "state": copy.deepcopy(state)}

def runtime_fault_result(state: dict[str, Any], stage: str) -> dict[str, Any]:
    return {"resultKind": "RUNTIME_FAULT_ROLLBACK", "state": fault(state), "failureStage": stage}

def controlled_result(state: dict[str, Any], owner: str, rule_id: str | None) -> dict[str, Any]:
    return {"resultKind": "CONTROLLED_FAULT_COMMIT", "state": copy.deepcopy(state), "owner": owner, "transitionRuleId": rule_id}

def commit_result(state: dict[str, Any], rule_id: str) -> dict[str, Any]:
    return {"resultKind": "COMMIT", "state": copy.deepcopy(state), "transitionRuleId": rule_id}

def invariants_ok(machine: dict[str, Any], state: dict[str, Any], event: dict[str, Any], limits: dict[str, int], frames: dict[str, Any]) -> bool:
    if state["phase"] == "FAULT":
        return True
    try:
        for row in machine["stateRecordV4"]["stateInvariantsV4"]:
            if eval_guard(machine, row["when"], state, event, limits, frames) and not eval_guard(machine, row["assert"], state, event, limits, frames):
                return False
        return True
    except (EvalFailure, KeyError, TypeError):
        return False

def selector_matches(selector: dict[str, Any], event: dict[str, Any]) -> bool:
    kind = selector["selectorKind"]
    if kind == "frame":
        return event["kind"] == "frame" and event["frameType"] == selector["frameType"]
    if kind == "event-kind":
        return event["kind"] == selector["kind"]
    return event["kind"] in selector["kinds"]

def ast_step_result(p: dict[str, Any], v2p: dict[str, Any], state: Any, event: Any, hits: set[str] | None = None) -> dict[str, Any]:
    machine = dict(p["orderingAndStateMachineV4"])
    machine["grammarBounds"] = p["schemaLanguageV4"]["recursiveBounds"]
    limits = v2p["limits"]
    frames = v2p["wireSchema"]["frameSchemas"]
    original = copy.deepcopy(state)
    if type(state) is dict and state.get("phase") == "FAULT":
        return absorb_result(state)
    if type(state) is not dict:
        return {"resultKind": "REJECT_NON_OBJECT_STATE"}
    if not runtime_state_valid(machine, state):
        return runtime_fault_result(original, "runtime-shape")
    if not runtime_event_valid(machine, event):
        return runtime_fault_result(original, "runtime-shape")
    if not invariants_ok(machine, state, event, limits, frames):
        return runtime_fault_result(original, "pre-invariant")
    pre = machine["prechecksV4"]
    try:
        if eval_guard(machine, pre["terminalOutputPrecheck"]["when"], state, event, limits, frames):
            staged = apply_actions_raise(machine, pre["terminalOutputPrecheck"]["actions"], state, event, limits)
            return controlled_result(staged, pre["terminalOutputPrecheck"]["owner"], None)
        staged = copy.deepcopy(state)
        if event["kind"] == "frame":
            if not eval_guard(machine, pre["framePrecheck"]["accept"], staged, event, limits, frames):
                return runtime_fault_result(original, pre["framePrecheck"]["rejectFailureStage"])
            staged = apply_actions_raise(machine, pre["framePrecheck"]["onAccept"], staged, event, limits)
        matched = False
        matched_id = ""
        for rule in machine["transitionRulesV4"]:
            if staged["phase"] not in rule["phaseIn"] or not selector_matches(rule["eventSelector"], event):
                continue
            try:
                guard = eval_guard(machine, rule["guard"], staged, event, limits, frames)
            except (EvalFailure, KeyError, TypeError, ValueError):
                return runtime_fault_result(original, pre["firstMatchingRule"]["guardFailureStage"])
            if not guard:
                continue
            try:
                staged = apply_actions_raise(machine, rule["actions"], staged, event, limits)
            except (EvalFailure, KeyError, TypeError, ValueError):
                return runtime_fault_result(original, pre["firstMatchingRule"]["actionFailureStage"])
            matched = True
            matched_id = rule["id"]
            if hits is not None:
                hits.add(rule["id"])
            break
        if not matched:
            return runtime_fault_result(original, pre["firstMatchingRule"]["noMatchFailureStage"])
        if not invariants_ok(machine, staged, event, limits, frames):
            return runtime_fault_result(original, pre["postInvariantCheck"]["failureStage"])
        if matched_id == "T028-TOTAL-FALLBACK":
            return controlled_result(staged, pre["firstMatchingRule"]["fallbackOwner"], matched_id)
        return commit_result(staged, matched_id)
    except (EvalFailure, KeyError, TypeError, ValueError):
        return runtime_fault_result(original, "action-evaluation")

def ast_step(p: dict[str, Any], v2p: dict[str, Any], state: Any, event: Any, hits: set[str] | None = None) -> Any:
    result = ast_step_result(p, v2p, state, event, hits)
    return copy.deepcopy(result.get("state"))

def frame_event(v2p: dict[str, Any], state: dict[str, Any], frame_type: str, **values: Any) -> dict[str, Any]:
    direction = v2p["wireSchema"]["frameSchemas"].get(frame_type, {}).get("direction", "host-to-worker")
    sequence = state["nextHostSequence"] if direction == "host-to-worker" else state["nextWorkerSequence"]
    out = {
        "kind": "frame", "direction": direction, "sequence": sequence,
        "frameType": frame_type, "payloadValid": values.get("payloadValid", True),
        "repositoryMode": None, "stageCount": None, "batchIndex": None,
        "firstCandidateOrdinal": None, "candidateCount": None,
        "budgetMatchesCurrentStage": None, "budgetUnit": None,
    }
    if frame_type == "OpenUniverse":
        out["repositoryMode"] = values.get("repositoryMode", "disabled")
    elif frame_type == "Analyze":
        out["stageCount"] = values.get("stageCount", 1)
    elif frame_type == "FactBatch":
        out["batchIndex"] = values.get("batchIndex", state["nextBatchIndex"])
        out["firstCandidateOrdinal"] = values.get("firstCandidateOrdinal", state["nextCandidateOrdinal"])
        out["candidateCount"] = values.get("candidateCount", 1)
    elif frame_type == "BudgetExhausted":
        out["budgetMatchesCurrentStage"] = values.get("budgetMatchesCurrentStage", True)
        out["budgetUnit"] = values.get("budgetUnit", "items")
    return out

def model_state_valid(v2p: dict[str, Any], state: Any) -> bool:
    if type(state) is not dict or list(state) != list(v2p["orderingAndStateMachine"]["initialState"]):
        return False
    phases = v2p["orderingAndStateMachine"]["stateRecord"]["phaseValues"]
    integers = ["stageIndex", "stageCount", "nextBatchIndex", "nextCandidateOrdinal", "nextHostSequence", "nextWorkerSequence"]
    booleans = ["outputSeen", "preparedMode", "requestClosed"]
    terminals = {None, "complete", "unavailable", "budget-exhausted", "provider-fault", "cancelled"}
    return state["phase"] in phases and all(u64(state[k]) for k in integers) and all(type(state[k]) is bool for k in booleans) and state["terminalKind"] in terminals

def model_event_valid(v2p: dict[str, Any], event: Any) -> bool:
    if type(event) is not dict or "kind" not in event:
        return False
    process = {"zero-exit", "nonzero-exit", "signal-death", "eof", "deadline", "stdout-byte"}
    if event["kind"] in process:
        return list(event) == ["kind"]
    required = ["kind", "direction", "sequence", "frameType", "payloadValid", "repositoryMode", "stageCount", "batchIndex", "firstCandidateOrdinal", "candidateCount", "budgetMatchesCurrentStage", "budgetUnit"]
    if event["kind"] != "frame" or list(event) != required:
        return False
    frames = v2p["wireSchema"]["frameSchemas"]
    ft = event["frameType"]
    if type(ft) is not str or ft not in frames or event["direction"] not in {"host-to-worker", "worker-to-host"} or not u64(event["sequence"]) or type(event["payloadValid"]) is not bool:
        return False
    if event["repositoryMode"] not in {None, "disabled", "prepared"} or any(value is not None and not u64(value) for value in [event["stageCount"], event["batchIndex"], event["firstCandidateOrdinal"], event["candidateCount"]]) or (event["budgetMatchesCurrentStage"] is not None and type(event["budgetMatchesCurrentStage"]) is not bool) or event["budgetUnit"] not in {None, "work-units", "bytes", "items", "milliseconds"}:
        return False
    semantic = {"repositoryMode", "stageCount", "batchIndex", "firstCandidateOrdinal", "candidateCount", "budgetMatchesCurrentStage", "budgetUnit"}
    nonnull = {"OpenUniverse": {"repositoryMode"}, "Analyze": {"stageCount"}, "FactBatch": {"batchIndex", "firstCandidateOrdinal", "candidateCount"}, "BudgetExhausted": {"budgetMatchesCurrentStage", "budgetUnit"}}.get(ft, set())
    return all((event[field] is None) == (field not in nonnull) for field in semantic)

def model_invariants_ok(v2p: dict[str, Any], state: dict[str, Any]) -> bool:
    phase = state["phase"]
    preanalysis = {"START", "WAIT_HELLO_ACK", "READY_OPEN_UNIVERSE", "WAIT_UNIVERSE_ACCEPTED", "READY_SNAPSHOT_MANIFEST", "RECEIVING_SNAPSHOT", "WAIT_SNAPSHOT_ACCEPTED", "READY_PREPARED_MANIFEST", "RECEIVING_PREPARED", "WAIT_PREPARED_ACCEPTED", "READY_ANALYZE"}
    if phase in preanalysis and state["stageCount"] != 0:
        return False
    if phase == "ANALYZING" and not (state["stageIndex"] < state["stageCount"] and 1 <= state["stageCount"] <= v2p["limits"]["maxAnalyzeStages"]):
        return False
    if phase == "READY_COMPLETE" and state["stageIndex"] != state["stageCount"]:
        return False
    if phase in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"} and state["terminalKind"] not in {"complete", "unavailable", "budget-exhausted", "provider-fault", "cancelled"}:
        return False
    if phase == "WAIT_CANCELLED" and state["requestClosed"] is not True:
        return False
    return True

def model_step_result(p: dict[str, Any], v2p: dict[str, Any], state: Any, event: Any) -> dict[str, Any]:
    original = copy.deepcopy(state)
    if type(state) is dict and state.get("phase") == "FAULT":
        return absorb_result(state)
    if type(state) is not dict:
        return {"resultKind": "REJECT_NON_OBJECT_STATE"}
    if not model_state_valid(v2p, state) or not model_event_valid(v2p, event):
        return runtime_fault_result(original, "runtime-shape")
    if not model_invariants_ok(v2p, state):
        return runtime_fault_result(original, "pre-invariant")
    if state["phase"] in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"} and event["kind"] in {"frame", "stdout-byte"}:
        out = fault(state)
        return controlled_result(out, "terminal-output-precheck", None)
    if event["kind"] != "frame":
        if event["kind"] == "zero-exit" and state["phase"] == "WAIT_ZERO_EXIT":
            out = copy.deepcopy(state); out["phase"] = "WAIT_EOF"; return commit_result(out, "T025-ZERO-EXIT")
        if event["kind"] == "eof" and state["phase"] == "WAIT_EOF":
            out = copy.deepcopy(state); out["phase"] = "DONE"; return commit_result(out, "T026-EOF")
        if event["kind"] in {"nonzero-exit", "signal-death", "deadline", "stdout-byte"}:
            return commit_result(fault(state), "T027-PROCESS-FAULT")
        return controlled_result(fault(state), "T028-TOTAL-FALLBACK", "T028-TOTAL-FALLBACK")
    frames = v2p["wireSchema"]["frameSchemas"]
    ft = event["frameType"]
    if event["payloadValid"] is not True or event["direction"] != frames[ft]["direction"]:
        return runtime_fault_result(original, "frame-precheck")
    field = "nextHostSequence" if event["direction"] == "host-to-worker" else "nextWorkerSequence"
    if event["sequence"] != state[field] or state[field] == U64_MAX:
        return runtime_fault_result(original, "frame-precheck")
    out = copy.deepcopy(state); out[field] += 1
    phase = state["phase"]
    direct = {
        ("START", "Hello"): ("WAIT_HELLO_ACK", "T001-HELLO"),
        ("WAIT_HELLO_ACK", "HelloAck"): ("READY_OPEN_UNIVERSE", "T002-HELLO-ACK"),
        ("WAIT_UNIVERSE_ACCEPTED", "UniverseAccepted"): ("READY_SNAPSHOT_MANIFEST", "T005-UNIVERSE-ACCEPTED"),
        ("READY_SNAPSHOT_MANIFEST", "SnapshotManifest"): ("RECEIVING_SNAPSHOT", "T006-SNAPSHOT-MANIFEST"),
        ("RECEIVING_SNAPSHOT", "SnapshotFileChunk"): ("RECEIVING_SNAPSHOT", "T007-SNAPSHOT-CHUNK"),
        ("RECEIVING_SNAPSHOT", "SnapshotSeal"): ("WAIT_SNAPSHOT_ACCEPTED", "T008-SNAPSHOT-SEAL"),
        ("READY_PREPARED_MANIFEST", "PreparedOutputManifest"): ("RECEIVING_PREPARED", "T011-PREPARED-MANIFEST"),
        ("RECEIVING_PREPARED", "PreparedOutputChunk"): ("RECEIVING_PREPARED", "T012-PREPARED-CHUNK"),
        ("RECEIVING_PREPARED", "PreparedOutputSeal"): ("WAIT_PREPARED_ACCEPTED", "T013-PREPARED-SEAL"),
        ("WAIT_PREPARED_ACCEPTED", "PreparedOutputAccepted"): ("READY_ANALYZE", "T014-PREPARED-ACCEPTED"),
    }
    if (phase, ft) in direct:
        out["phase"], rule_id = direct[(phase, ft)]
        return commit_result(out, rule_id)
    if phase == "READY_OPEN_UNIVERSE" and ft == "OpenUniverse":
        out["preparedMode"] = event["repositoryMode"] == "prepared"; out["phase"] = "WAIT_UNIVERSE_ACCEPTED"
        return commit_result(out, "T004-OPEN-PREPARED" if out["preparedMode"] else "T003-OPEN-DISABLED")
    if phase == "WAIT_SNAPSHOT_ACCEPTED" and ft == "SnapshotAccepted":
        out["phase"] = "READY_PREPARED_MANIFEST" if state["preparedMode"] else "READY_ANALYZE"
        return commit_result(out, "T010-SNAPSHOT-ACCEPTED-PREPARED" if state["preparedMode"] else "T009-SNAPSHOT-ACCEPTED-DISABLED")
    if phase == "READY_ANALYZE" and ft == "Analyze" and 1 <= event["stageCount"] <= v2p["limits"]["maxAnalyzeStages"]:
        out.update({"stageCount": event["stageCount"], "stageIndex": 0, "nextBatchIndex": 0, "nextCandidateOrdinal": 0, "outputSeen": False, "phase": "ANALYZING"})
        return commit_result(out, "T015-ANALYZE")
    if phase == "ANALYZING" and ft == "FactBatch":
        count = event["candidateCount"]
        if event["batchIndex"] == state["nextBatchIndex"] and event["firstCandidateOrdinal"] == state["nextCandidateOrdinal"] and 1 <= count <= v2p["limits"]["maxFactBatchCandidates"] and out["nextBatchIndex"] < U64_MAX and out["nextCandidateOrdinal"] <= U64_MAX - count:
            out["nextBatchIndex"] += 1; out["nextCandidateOrdinal"] += count; out["outputSeen"] = True
            return commit_result(out, "T016-FACT-BATCH")
    if phase == "ANALYZING" and ft == "Coverage":
        next_stage = out["stageIndex"] + 1
        if next_stage < out["stageCount"]:
            out.update({"stageIndex": next_stage, "nextBatchIndex": 0, "nextCandidateOrdinal": 0, "outputSeen": True})
            return commit_result(out, "T017-COVERAGE-NEXT")
        if next_stage == out["stageCount"]:
            out.update({"stageIndex": next_stage, "nextBatchIndex": 0, "nextCandidateOrdinal": 0, "outputSeen": True, "phase": "READY_COMPLETE"})
            return commit_result(out, "T018-COVERAGE-LAST")
    if phase == "ANALYZING" and ft == "Unavailable" and state["stageIndex"] == 0 and state["outputSeen"] is False:
        out["terminalKind"] = "unavailable"; out["phase"] = "WAIT_ZERO_EXIT"; return commit_result(out, "T019-UNAVAILABLE")
    if phase == "ANALYZING" and ft == "BudgetExhausted" and event["budgetMatchesCurrentStage"] is True and event["budgetUnit"] in {"work-units", "bytes", "items"}:
        out["terminalKind"] = "budget-exhausted"; out["phase"] = "WAIT_ZERO_EXIT"; return commit_result(out, "T020-BUDGET")
    if phase == "READY_COMPLETE" and ft == "Complete":
        out["terminalKind"] = "complete"; out["phase"] = "WAIT_ZERO_EXIT"; return commit_result(out, "T021-COMPLETE")
    if phase in v2p["orderingAndStateMachine"]["providerFaultPermittedPhases"] and ft == "ProviderFault":
        out["terminalKind"] = "provider-fault"; out["phase"] = "WAIT_ZERO_EXIT"; return commit_result(out, "T022-PROVIDER-FAULT")
    if phase in v2p["orderingAndStateMachine"]["cancelPermittedPhases"] and ft == "Cancel" and state["requestClosed"] is False:
        out["requestClosed"] = True; out["phase"] = "WAIT_CANCELLED"; return commit_result(out, "T023-CANCEL")
    if phase == "WAIT_CANCELLED" and ft == "Cancelled" and state["requestClosed"] is True:
        out["terminalKind"] = "cancelled"; out["phase"] = "WAIT_ZERO_EXIT"; return commit_result(out, "T024-CANCELLED")
    result = controlled_result(fault(out), "T028-TOTAL-FALLBACK", "T028-TOTAL-FALLBACK")
    return result if model_invariants_ok(v2p, result["state"]) else runtime_fault_result(original, "post-invariant")

def model_step(p: dict[str, Any], v2p: dict[str, Any], state: Any, event: Any) -> Any:
    return copy.deepcopy(model_step_result(p, v2p, state, event).get("state"))

def canonical_state(v2p: dict[str, Any], phase: str) -> dict[str, Any]:
    state = copy.deepcopy(v2p["orderingAndStateMachine"]["initialState"])
    state["phase"] = phase
    if phase == "ANALYZING":
        state["stageCount"] = 1
    elif phase == "READY_COMPLETE":
        state["stageCount"] = 1; state["stageIndex"] = 1; state["outputSeen"] = True
    elif phase in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"}:
        state["terminalKind"] = "complete"
    elif phase == "WAIT_CANCELLED":
        state["requestClosed"] = True
    return state

def fsm_checks(p: dict[str, Any], v2p: dict[str, Any]) -> tuple[list[str], int, int, int]:
    errors = protocol_errors(p, v2p)
    if errors:
        return errors, 0, 0, 0
    m = dict(p["orderingAndStateMachineV4"])
    m["grammarBounds"] = p["schemaLanguageV4"]["recursiveBounds"]
    hits: set[str] = set()
    trace_count = 0
    for prepared in (False, True):
        for stage_count in (1, 2, 3):
            for batches in itertools.product((0, 1, 2), repeat=stage_count):
                left = copy.deepcopy(m["initialState"]); right = copy.deepcopy(left)
                sequence: list[dict[str, Any]] = []
                def add(ft: str, **values: Any) -> None:
                    nonlocal left, right
                    event = frame_event(v2p, left, ft, **values)
                    model_result = model_step_result(p, v2p, left, event)
                    ast_result = ast_step_result(p, v2p, right, event, hits)
                    if not exact_json_equal(model_result, ast_result):
                        raise AssertionError("FSM divergence " + ft)
                    left = copy.deepcopy(model_result["state"])
                    right = copy.deepcopy(ast_result["state"])
                for ft, values in [
                    ("Hello", {}), ("HelloAck", {}), ("OpenUniverse", {"repositoryMode": "prepared" if prepared else "disabled"}),
                    ("UniverseAccepted", {}), ("SnapshotManifest", {}), ("SnapshotSeal", {}), ("SnapshotAccepted", {}),
                ]:
                    add(ft, **values)
                if prepared:
                    for ft in ("PreparedOutputManifest", "PreparedOutputSeal", "PreparedOutputAccepted"):
                        add(ft)
                add("Analyze", stageCount=stage_count)
                for count in batches:
                    for _ in range(count):
                        add("FactBatch")
                    add("Coverage")
                add("Complete")
                for event in ({"kind": "zero-exit"}, {"kind": "eof"}):
                    model_result = model_step_result(p, v2p, left, event)
                    ast_result = ast_step_result(p, v2p, right, event, hits)
                    if not exact_json_equal(model_result, ast_result):
                        raise AssertionError("FSM process divergence")
                    left = copy.deepcopy(model_result["state"])
                    right = copy.deepcopy(ast_result["state"])
                if left["phase"] != "DONE":
                    raise AssertionError("FSM not done")
                trace_count += 1
    totality = 0
    frame_types = list(v2p["wireSchema"]["frameSchemas"])
    process = ["zero-exit", "nonzero-exit", "signal-death", "eof", "deadline", "stdout-byte"]
    for phase in m["nominalTypes"]["phase"]["enum"]:
        for label in frame_types + process + ["UNKNOWN_FRAME", "MALFORMED_FRAME_SHAPE"]:
            left = canonical_state(v2p, phase); right = copy.deepcopy(left)
            if label == "MALFORMED_FRAME_SHAPE":
                event = {"kind": "frame"}
            else:
                event = frame_event(v2p, left, label) if label not in process else {"kind": label}
            # Unknown and malformed frames are deliberately hostile; both semantics fault.
            a = model_step_result(p, v2p, left, event)
            b = ast_step_result(p, v2p, right, event, hits)
            if not exact_json_equal(a, b):
                errors.append("FSM totality divergence " + phase + "/" + label)
                return errors, trace_count, totality, len(hits)
            totality += 1
    if hits != {row["id"] for row in m["transitionRulesV4"]}:
        errors.append("FSM rule coverage")
    try:
        vectors = {row["id"]: row for row in m["semanticConformanceVectors"]}
        seq = vectors["SEM-ACTION-SEQUENTIAL-UPDATED-READ"]
        state = apply_actions_raise(m, seq["actions"], seq["initialState"], seq["event"], v2p["limits"])
        if state["nextBatchIndex"] != 7 or state["stageIndex"] != 7:
            errors.append("sequential updated read")
        for vid, expected in [("SEM-GUARD-ALL-SHORT-CIRCUIT", False), ("SEM-GUARD-ANY-SHORT-CIRCUIT", True)]:
            row = vectors[vid]
            got = eval_guard(m, row["guard"], row["initialState"], row["event"], v2p["limits"], v2p["wireSchema"]["frameSchemas"])
            if got is not expected:
                errors.append("short circuit " + vid)
        row = vectors["SEM-ACTION-OVERFLOW-ATOMIC"]
        try:
            apply_actions_raise(m, row["actions"], row["initialState"], row["event"], v2p["limits"])
            errors.append("overflow did not fail")
        except EvalFailure:
            if fault(row["initialState"])["nextBatchIndex"] != row["initialState"]["nextBatchIndex"]:
                errors.append("partial action write")
        row = vectors["SEM-POST-INVARIANT-FAILURE-FAULTS-ATOMically"]
        staged = apply_actions_raise(m, row["actions"], row["initialState"], row["event"], v2p["limits"])
        if invariants_ok(m, staged, row["event"], v2p["limits"], v2p["wireSchema"]["frameSchemas"]):
            errors.append("post invariant vector")
        row = vectors["SEM-RUNTIME-EVENT-SHAPE-FAILURE"]
        if ast_step(p, v2p, row["initialState"], row["event"]) != fault(row["initialState"]):
            errors.append("runtime unknown field fate")
    except (KeyError, TypeError, EvalFailure) as exc:
        errors.append("semantic vector escape " + type(exc).__name__)
    return errors, trace_count, totality, len(hits)

def safe_fsm_checks(p: Any, v2p: dict[str, Any]) -> tuple[list[str], int, int, int]:
    try:
        return fsm_checks(p, v2p)
    except Exception as exc:
        return ["FSM total failure: " + type(exc).__name__], 0, 0, 0

def repair_witness_checks(p: dict[str, Any], v2p: dict[str, Any]) -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    machine = dict(p["orderingAndStateMachineV4"])
    machine["grammarBounds"] = p["schemaLanguageV4"]["recursiveBounds"]
    declared = machine["modelCheckDomain"]["requiredRepairWitnesses"]
    observed: list[str] = []

    def compare(witness_id: str, state: Any, event: Any, predicate: Callable[[dict[str, Any]], bool]) -> None:
        nonlocal count
        observed.append(witness_id)
        left = model_step_result(p, v2p, copy.deepcopy(state), copy.deepcopy(event))
        right = ast_step_result(p, v2p, copy.deepcopy(state), copy.deepcopy(event))
        if not exact_json_equal(left, right):
            errors.append(witness_id + " interpreter/model divergence")
        if not transition_result_valid(machine, right):
            errors.append(witness_id + " invalid closed result")
        if not predicate(right):
            errors.append(witness_id + " wrong result")
        count += 1

    malformed_fault = {"phase": "FAULT", "alien": [True, {"x": 1}], "stageIndex": "wrong"}
    compare("RV4-FAULT-ABSORB-MALFORMED", malformed_fault, None, lambda r: r == {"resultKind": "ABSORB_UNCHANGED", "state": malformed_fault})

    missing_phase = copy.deepcopy(machine["initialState"])
    del missing_phase["phase"]
    compare("RV4-MALFORMED-MISSING-PHASE", missing_phase, {"kind": "zero-exit"}, lambda r: r["resultKind"] == "RUNTIME_FAULT_ROLLBACK" and list(r["state"]) == list(missing_phase) + ["phase"] and all(exact_json_equal(r["state"][k], missing_phase[k]) for k in missing_phase))

    wrong_type = copy.deepcopy(machine["initialState"]); wrong_type["stageIndex"] = "wrong"
    compare("RV4-MALFORMED-WRONG-TYPE-PRESERVED", wrong_type, {"kind": "zero-exit"}, lambda r: r["resultKind"] == "RUNTIME_FAULT_ROLLBACK" and r["state"]["stageIndex"] == "wrong" and list(r["state"]) == list(wrong_type))

    unknown = copy.deepcopy(machine["initialState"]); unknown["unknownTail"] = {"nested": [1, False]}
    compare("RV4-MALFORMED-UNKNOWN-FIELD-PRESERVED", unknown, {"kind": "zero-exit"}, lambda r: r["resultKind"] == "RUNTIME_FAULT_ROLLBACK" and r["state"]["unknownTail"] == unknown["unknownTail"] and list(r["state"]) == list(unknown))

    compare("RV4-NONOBJECT-CLOSED-REJECT", ["not", "state"], {"kind": "zero-exit"}, lambda r: r == {"resultKind": "REJECT_NON_OBJECT_STATE"})

    terminal = canonical_state(v2p, "WAIT_ZERO_EXIT"); terminal["nextWorkerSequence"] = 5
    terminal_event = frame_event(v2p, terminal, "HelloAck")
    compare("RV4-TERMINAL-OUTPUT-STOPS", terminal, terminal_event, lambda r: r["resultKind"] == "CONTROLLED_FAULT_COMMIT" and r["owner"] == "terminal-output-precheck" and r["transitionRuleId"] is None and r["state"]["nextWorkerSequence"] == 5)

    fallback_state = copy.deepcopy(machine["initialState"])
    fallback_event = frame_event(v2p, fallback_state, "HelloAck")
    compare("RV4-FALLBACK-FRAME-COMMITS-SEQUENCE", fallback_state, fallback_event, lambda r: r["resultKind"] == "CONTROLLED_FAULT_COMMIT" and r["owner"] == "T028-TOTAL-FALLBACK" and r["state"]["nextWorkerSequence"] == 1)

    rejected_state = copy.deepcopy(machine["initialState"])
    rejected_event = frame_event(v2p, rejected_state, "Hello", payloadValid=False)
    compare("RV4-REJECTED-FRAME-ROLLS-BACK", rejected_state, rejected_event, lambda r: r["resultKind"] == "RUNTIME_FAULT_ROLLBACK" and r["failureStage"] == "frame-precheck" and r["state"]["nextHostSequence"] == 0)

    ordinary_state = copy.deepcopy(machine["initialState"])
    ordinary_event = frame_event(v2p, ordinary_state, "Hello")
    compare("RV4-ORDINARY-FRAME-COMMITS", ordinary_state, ordinary_event, lambda r: r["resultKind"] == "COMMIT" and r["transitionRuleId"] == "T001-HELLO" and r["state"]["nextHostSequence"] == 1)

    bad_invariant = copy.deepcopy(machine["initialState"]); bad_invariant["stageCount"] = 1
    compare("RV4-PREINVARIANT-ROLLS-BACK", bad_invariant, {"kind": "zero-exit"}, lambda r: r["resultKind"] == "RUNTIME_FAULT_ROLLBACK" and r["failureStage"] == "pre-invariant" and r["state"]["stageCount"] == 1)

    observed.append("RV4-POSTINVARIANT-ROLLS-BACK")
    vector = next(row for row in machine["semanticConformanceVectors"] if row["id"] == "SEM-POST-INVARIANT-FAILURE-FAULTS-ATOMically")
    staged = apply_actions_raise(machine, vector["actions"], vector["initialState"], vector["event"], v2p["limits"])
    ast_ok = invariants_ok(machine, staged, vector["event"], v2p["limits"], v2p["wireSchema"]["frameSchemas"])
    model_ok = model_invariants_ok(v2p, staged)
    post_result = runtime_fault_result(vector["initialState"], "post-invariant")
    if ast_ok or model_ok or not transition_result_valid(machine, post_result) or post_result["state"]["stageCount"] != 0:
        errors.append("RV4-POSTINVARIANT-ROLLS-BACK wrong result")
    count += 1

    absorbed = copy.deepcopy(machine["initialState"]); absorbed["phase"] = "FAULT"
    compare("RV4-FAULT-ABSORPTION-PRECEDES-EVENT-SHAPE", absorbed, {"kind": "frame"}, lambda r: r["resultKind"] == "ABSORB_UNCHANGED" and r["state"] == absorbed)

    if observed != declared:
        errors.append("repair witness declaration/order")
    return errors, count

def axes_valid(schema: dict[str, Any], axes: Any, ordered: list[str]) -> bool:
    try:
        if not exact_keys(axes, ordered):
            return False
        props = schema["properties"]
        for key in ordered:
            spec = props[key]
            value = axes[key]
            if key == "secondaryDeficiencies":
                if type(value) is not list or len(value) != len(set(value)) or any(x not in spec["items"]["enum"] for x in value):
                    return False
            elif value not in spec["enum"]:
                return False
        if axes["secondaryDeficiencies"] and (axes["deficiency"] == "none" or axes["deficiency"] in axes["secondaryDeficiencies"]):
            return False
        return True
    except (KeyError, TypeError):
        return False

def termination_valid(union: dict[str, Any], value: Any, policy: dict[str, list[str]]) -> bool:
    try:
        if type(value) is not dict or value.get("class") not in policy or list(value) != policy[value["class"]]:
            return False
        variant = next(row for row in union["variants"] if row["class"] == value["class"])
        fields = set(value) - {"class"}
        if not set(variant["required"]) <= fields <= set(variant["required"]) | set(variant["optional"]):
            return False
        if "exitCode" in value:
            return False
        if "reasonCodes" in value and (type(value["reasonCodes"]) is not list or not value["reasonCodes"] or any(type(x) is not str for x in value["reasonCodes"])):
            return False
        if "signal" in value and value["signal"] not in union["fieldTypes"]["signal"]["enum"]:
            return False
        return all(type(v) is str for k, v in value.items() if k not in {"class", "reasonCodes"})
    except (KeyError, StopIteration, TypeError):
        return False

def delivery_projection_errors(d: Any, v2d: dict[str, Any], d9doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        expected_root = [
            "artifact", "version", "status", "reviewStatus", "purpose",
            "predecessorRejection", "protocolReference", "retainedV3RepairBoundary", "retainedV2SemanticProjection",
            "dependencyPins", "hostFinalizerBoundaryV4", "reducerPreservation",
            "residuals", "authority", "supersedesOnlyIfIndependentlyAcceptedAndApplied",
        ]
        if not exact_keys(d, expected_root):
            return ["delivery root"]
        if d["version"] != 4 or d["status"] != STATUS or d["predecessorRejection"].get("sha256") != REVIEW_SHA or d["protocolReference"] .get("version") != 4:
            errors.append("delivery identity")
        if d["retainedV3RepairBoundary"].get("source", {}).get("sha256") != PRESERVED_HASHES[V3_DELIVERY]:
            errors.append("delivery v3 repair boundary")
        excluded = {"artifact", "version", "status", "reviewStatus", "purpose", "protocolReference", "hostFinalizerContextV2", "hostFinalizerProjection", "exhaustivenessRule", "rejectionBasis", "residuals", "authority", "supersedesOnlyIfIndependentlyAcceptedAndApplied"}
        inherited = [k for k in v2d if k not in excluded]
        proj = d["retainedV2SemanticProjection"]
        if proj.get("inheritedTopLevelSelectors") != inherited:
            errors.append("delivery inherited selectors")
        expected_hashes = projection_selector_hashes(v2d, inherited)
        actual_hashes = [{"selector": x.get("selector"), "sha256": x.get("sha256")} for x in proj.get("inheritedSelectorSha256", [])]
        if actual_hashes != expected_hashes:
            errors.append("delivery inherited hashes")
        b = d["hostFinalizerBoundaryV4"]
        d9p = b["pinnedD9Projection"]
        if d9p["scenarioAxesSchema"] != d9doc["scenarioAxesSchema"] or d9p["hostTerminationUnion"] != d9doc["hostTerminationUnion"] or d9p["codeMaps"] != d9doc["codeMaps"] or d9p["classToExitCode"] != d9doc["classToExitCode"]:
            errors.append("D9 exact projection")
        base = b["baseAxesContract"]
        ordered = list(d9doc["scenarioAxesSchema"]["properties"])
        if base["orderedFields"] != ordered or base["exactPinnedScenarioAxesSchema"] != d9doc["scenarioAxesSchema"]:
            errors.append("base axes schema")
        ids = set()
        policy = b["hostIdentityV4"]["terminationFieldPolicy"]
        for row in base["profiles"]:
            if not exact_keys(row, ["id", "axes", "checkedD9"]) or row["id"] in ids or not axes_valid(d9doc["scenarioAxesSchema"], row["axes"], ordered):
                errors.append("base axes profile")
                break
            ids.add(row["id"])
            checked = row["checkedD9"]
            if not termination_valid(d9doc["hostTerminationUnion"], checked["hostTerminationChecked"], policy):
                errors.append("base checked termination")
                break
        c1 = b["c1PredicateRelativeSufficiencyV4"]
        if c1["recordRequired"] != ["predicateId", "relation", "minimumResolution", "availableNonProviderResolution", "requiredCompleteness", "availableCompleteness", "derivedSufficiency"] or c1["recordOptional"] != []:
            errors.append("C1 schema")
        for row in c1["profiles"]:
            value = row["inputs"]
            if not exact_keys(value, c1["recordRequired"]):
                errors.append("C1 fields")
                break
            ladder = c1["relationLadders"][value["relation"]]
            derived = "sufficient" if ladder.index(value["availableNonProviderResolution"]) >= ladder.index(value["minimumResolution"]) and (value["requiredCompleteness"] != "complete" or value["availableCompleteness"] == "complete") else "insufficient"
            if value["derivedSufficiency"] != derived:
                errors.append("C1 derivation")
        domain = b["finiteContextDomain"]
        names = domain["dimensionOrder"]; dims = domain["dimensions"]
        tuple_schema = domain["tupleRecordV4Schema"]
        if names != ["normalizedFate", "baseAxesProfile", "admittedProviderRequiredness", "c1SufficiencyProfile", "interruptionTiming", "settlementMode"] or tuple_schema != {"closed": True, "required": names, "optional": [], "requiredEqualsDimensionOrder": True} or "admissionRuleId" not in domain["tupleEncoding"] or "excluded" not in domain["tupleEncoding"]:
            errors.append("six-field tuple schema/encoding")
        tuples = [dict(zip(names, values)) for values in itertools.product(*(dims[k] for k in names))]
        admitted: list[dict[str, Any]] = []; invalid: list[dict[str, Any]] = []
        for tup in tuples:
            hits = [row["id"] for row in domain["admittedRows"] if all(tup[k] in row[k] for k in names)]
            if len(hits) == 1:
                admitted.append(copy.deepcopy(tup))
            elif not hits:
                invalid.append(tup)
            else:
                errors.append("admission ambiguity")
                break
        if (len(tuples), len(admitted), len(invalid)) != (domain["fullCartesianSize"], domain["admittedCount"], domain["invalidCombinations"]["count"]) or (len(tuples), len(admitted), len(invalid)) != (2304, 148, 2156):
            errors.append("finalizer domain counts")
        if compact_sha(admitted) != "sha256:bfdecd8a02a7479082a7aab3858e261aada86e05c119174f48a7dac8f3c3489e" or compact_sha(admitted) != domain["admittedTupleCommitment"] or compact_sha(invalid) != domain["invalidCombinations"]["tupleCommitment"]:
            errors.append("finalizer domain commitments")
        rules = b["transformationV4"]["rules"]
        if [x["priority"] for x in rules] != list(range(1, 11)) or len({x["id"] for x in rules}) != 10:
            errors.append("transform rules")
        if b["transformationV4"]["causePrecedence"] != ["faultCause", "rejectionCause", "deficiency"]:
            errors.append("cause precedence")
        if b["transformationV4"]["forbiddenResults"] != ["DEFER", "DEFER-EXACT-HOST-D9-NO-PROVIDER-DEFICIENCY", "DEFER-HIGHER-PRIORITY-HOST-D9", "PRESERVE", "PRESERVE-SETTLED-FINALIZATION", "UNKNOWN"]:
            errors.append("forbidden placeholder set")
        settle = b["settlementOptionV4"]["exactSettledFixture"]
        raw = bytes.fromhex(settle["hostTerminationCanonicalBytesHex"])
        if sha_ref(raw) != settle["hostTerminationSha256"] or compact(strict_loads(raw.decode())) != raw:
            errors.append("settled termination bytes")
        auth_raw = bytes.fromhex(settle["authorityRecordCanonicalBytesHex"])
        if compact(settle["authorityRecord"]) != auth_raw or sha_ref(auth_raw) != settle["settlementAuthorityRef"]:
            errors.append("settlement authority")
        if len(b["narrowGoldens"]) != 7:
            errors.append("finalizer goldens")
        if b["hostFinalizerContextV4Schema"]["unknownFieldFate"] != "REJECT_CONTEXT":
            errors.append("context unknown fate")
        if b["hostFinalizerContextV4Schema"]["fields"].get("schemaVersion") != "uint64 exactly 4":
            errors.append("context schema version")
        if d["authority"].get("selfReview") is not False or d["authority"].get("applied") is not False:
            errors.append("delivery authority")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        errors.append("hostile delivery: " + type(exc).__name__)
    return errors

def make_context(boundary: dict[str, Any], tup: dict[str, Any]) -> dict[str, Any]:
    profiles = {x["id"]: x["axes"] for x in boundary["baseAxesContract"]["profiles"]}
    c1 = {x["id"]: x["inputs"] for x in boundary["c1PredicateRelativeSufficiencyV4"]["profiles"]}
    settlement = {"kind": "absent"} if tup["settlementMode"] == "absent" else copy.deepcopy(boundary["settlementOptionV4"]["exactSettledFixture"])
    return {
        "schemaVersion": 4,
        "normalizedFate": tup["normalizedFate"],
        "baseAxesProfile": tup["baseAxesProfile"],
        "baseAxes": copy.deepcopy(profiles[tup["baseAxesProfile"]]),
        "hostIdentity": copy.deepcopy(boundary["hostIdentityV4"]["exactFixture"]),
        "admittedProviderRequiredness": tup["admittedProviderRequiredness"],
        "c1SufficiencyProfile": tup["c1SufficiencyProfile"],
        "c1PredicateRelativeInputs": copy.deepcopy(c1[tup["c1SufficiencyProfile"]]),
        "interruptionTiming": tup["interruptionTiming"],
        "settlement": settlement,
    }

def require_admitted(boundary: dict[str, Any], tup: dict[str, Any]) -> str:
    domain = boundary["finiteContextDomain"]
    names = domain["dimensionOrder"]
    hits = [
        row["id"] for row in domain["admittedRows"]
        if all(tup[key] in row[key] for key in names)
    ]
    if len(hits) != 1:
        raise ValueError("context is not uniquely admitted")
    return hits[0]

def effective_required(context: dict[str, Any]) -> bool:
    return context["admittedProviderRequiredness"] == "required" or context["c1PredicateRelativeInputs"]["derivedSufficiency"] == "insufficient"

def base_family(axes: dict[str, Any]) -> str:
    if axes["faultCause"] != "none":
        return "faultCause"
    if axes["rejectionCause"] != "none":
        return "rejectionCause"
    if axes["deficiency"] != "none":
        return "deficiency"
    return "none"

def transform_contract(boundary: dict[str, Any], context: dict[str, Any]) -> tuple[str, dict[str, Any], str]:
    computed = {
        "effectiveProviderRequired": effective_required(context),
        "baseCauseFamily": base_family(context["baseAxes"]),
    }
    matches = []
    for row in boundary["transformationV4"]["rules"]:
        if all((context.get(k, computed.get(k)) in values) for k, values in row["when"].items()):
            matches.append(row)
            break
    if len(matches) != 1:
        raise ValueError("no transformation")
    row = matches[0]
    alg = row["axesAlgorithm"]
    if alg == "EXACT_BASE_AXES":
        axes = copy.deepcopy(context["baseAxes"])
    elif alg == "EXACT_TEMPLATE":
        axes = copy.deepcopy(boundary["transformationV4"]["axisTemplates"][row["templateId"]])
    elif alg == "PROVIDER_DEFICIENCY_PATCH":
        axes = copy.deepcopy(context["baseAxes"])
        axes["requiredCoverage"] = row["requiredCoverage"]
        axes["verdict"] = row["verdict"]
        deficiency = row["providerDeficiency"]
        if axes["deficiency"] == "none":
            axes["deficiency"] = deficiency
            axes["secondaryDeficiencies"] = []
        elif axes["deficiency"] != deficiency and deficiency not in axes["secondaryDeficiencies"]:
            axes["secondaryDeficiencies"].append(deficiency)
    else:
        raise ValueError("algorithm")
    return row["id"], axes, row["terminationAlgorithm"]

def transform_model(boundary: dict[str, Any], context: dict[str, Any]) -> tuple[str, dict[str, Any], str]:
    fate = context["normalizedFate"]; timing = context["interruptionTiming"]; base = copy.deepcopy(context["baseAxes"])
    protocol = {
        "POST_TERMINAL_OUTPUT", "MALFORMED_FRAME", "SCHEMA_OR_COMMITMENT_FAULT",
        "HANDSHAKE_MISMATCH", "DEADLINE_HANG", "NONZERO_EXIT", "EARLY_EOF",
        "UNSOLICITED_CANCELLED", "PROVIDER_DECLARED_FAULT", "INCOMPLETE_PROTOCOL",
    }
    templates = boundary["transformationV4"]["axisTemplates"]
    if timing == "signal-after-finalization" and fate == "VERIFIED_COMPLETE":
        return "FINAL-SETTLED-AFTER", base, "RETURN_AND_BYTE_COMPARE_SETTLED_HOST_TERMINATION"
    if timing == "signal-before-finalization" and fate in {"USER_INTERRUPTED", "VERIFIED_CANCELLED"}:
        return "FINAL-INTERRUPTED-BEFORE", copy.deepcopy(templates["interrupt-before"]), "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    if timing == "none" and fate == "DELIVERY_REQUIRED_FAILURE":
        return "FINAL-DELIVERY-FAULT", copy.deepcopy(templates["delivery-required-failure"]), "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    if timing == "none" and fate in protocol:
        return "FINAL-PROVIDER-PROTOCOL-FAULT", copy.deepcopy(templates["provider-protocol-failure"]), "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    if timing == "none" and fate == "VERIFIED_COMPLETE":
        return "FINAL-COMPLETE-IDENTITY", base, "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    req = effective_required(context)
    if timing == "none" and fate == "VERIFIED_UNAVAILABLE" and not req:
        return "FINAL-OPTIONAL-UNAVAILABLE-IDENTITY", base, "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    if timing == "none" and fate == "VERIFIED_BUDGET_EXHAUSTED" and not req:
        return "FINAL-OPTIONAL-BUDGET-IDENTITY", base, "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    if timing == "none" and fate in {"VERIFIED_UNAVAILABLE", "VERIFIED_BUDGET_EXHAUSTED"} and req and base_family(base) == "faultCause":
        return "FINAL-REQUIRED-PROVIDER-HOST-FAULT-PRECEDENCE", base, "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    if timing == "none" and fate in {"VERIFIED_UNAVAILABLE", "VERIFIED_BUDGET_EXHAUSTED"} and req:
        deficiency = "provider-unavailable" if fate == "VERIFIED_UNAVAILABLE" else "budget-exhausted"
        base["requiredCoverage"] = "unsatisfied" if fate == "VERIFIED_UNAVAILABLE" else "unknown"
        base["verdict"] = "indeterminate"
        if base["deficiency"] == "none":
            base["deficiency"] = deficiency; base["secondaryDeficiencies"] = []
        elif base["deficiency"] != deficiency and deficiency not in base["secondaryDeficiencies"]:
            base["secondaryDeficiencies"].append(deficiency)
        ident = "FINAL-REQUIRED-UNAVAILABLE" if fate == "VERIFIED_UNAVAILABLE" else "FINAL-REQUIRED-BUDGET"
        return ident, base, "DERIVE_MINIMAL_EXACT_HOST_TERMINATION"
    raise ValueError("invalid model context")

def construct_termination(boundary: dict[str, Any], cls: str, codes: dict[str, Any], identity: dict[str, str]) -> dict[str, Any]:
    if cls == "success":
        return {"class": cls, "runId": identity["runId"], "executionId": identity["executionId"]}
    if cls == "policy-failed":
        return {"class": cls, "runId": identity["runId"], "executionId": identity["executionId"]}
    if cls == "indeterminate":
        return {"class": cls, "reasonCodes": codes["reasonCodes"], "runId": identity["runId"], "coverageId": identity["coverageId"], "executionId": identity["executionId"]}
    if cls == "operational-failed":
        return {"class": cls, "errorCode": codes["errorCode"], "executionId": identity["executionId"], "runId": identity["runId"]}
    if cls == "interrupted":
        return {"class": cls, "signal": identity["signal"], "executionId": identity["executionId"], "runId": identity["runId"]}
    raise ValueError("D9 class")

def finalizer_checks(d: dict[str, Any], v2d: dict[str, Any], d9doc: dict[str, Any], d9mod: types.ModuleType) -> tuple[list[str], int, int]:
    errors = delivery_projection_errors(d, v2d, d9doc)
    if errors:
        return errors, 0, 0
    b = d["hostFinalizerBoundaryV4"]
    domain = b["finiteContextDomain"]; names = domain["dimensionOrder"]; dims = domain["dimensions"]
    policy = b["hostIdentityV4"]["terminationFieldPolicy"]
    admitted_count = invalid_count = 0
    results: dict[tuple[Any, ...], dict[str, Any]] = {}
    for values in itertools.product(*(dims[k] for k in names)):
        tup = dict(zip(names, values))
        hits = [row["id"] for row in domain["admittedRows"] if all(tup[k] in row[k] for k in names)]
        if not hits:
            invalid_count += 1
            try:
                require_admitted(b, tup)
                errors.append("invalid context transformed")
                break
            except ValueError:
                continue
        if len(hits) != 1:
            errors.append("admitted ambiguity")
            break
        admitted_count += 1
        require_admitted(b, tup)
        context = make_context(b, tup)
        left = transform_contract(b, context)
        right = transform_model(b, context)
        if left != right:
            errors.append("finalizer independent model divergence")
            break
        rule_id, axes, term_alg = left
        if not axes_valid(d9doc["scenarioAxesSchema"], axes, b["baseAxesContract"]["orderedFields"]):
            errors.append("final axes invalid")
            break
        cls = d9mod.derive_class(axes)
        codes = d9mod.derive_codes(axes, d9doc["codeMaps"])
        exit_code = d9doc["classToExitCode"][cls]
        termination = construct_termination(b, cls, codes, context["hostIdentity"])
        if term_alg == "RETURN_AND_BYTE_COMPARE_SETTLED_HOST_TERMINATION":
            settlement = context["settlement"]
            raw = bytes.fromhex(settlement["hostTerminationCanonicalBytesHex"])
            settled = strict_loads(raw.decode())
            if compact(settled) != raw or settled != termination or sha_ref(raw) != settlement["hostTerminationSha256"]:
                errors.append("settled byte return")
                break
            termination = settled
        if not termination_valid(d9doc["hostTerminationUnion"], termination, policy):
            errors.append("termination union")
            break
        expected_codes = {}
        if "reasonCodes" in termination:
            expected_codes["reasonCodes"] = termination["reasonCodes"]
        if "errorCode" in termination:
            expected_codes["errorCode"] = termination["errorCode"]
        if expected_codes != codes:
            errors.append("D9 code equality")
            break
        results[tuple(tup[k] for k in names)] = {
            "transformationRuleId": rule_id,
            "finalAxesChecked": axes,
            "hostTerminationChecked": termination,
            "exitCodeChecked": exit_code,
        }
    if (admitted_count, invalid_count) != (148, 2156):
        errors.append("finalizer enumeration count")
    for golden in b["narrowGoldens"]:
        selector = golden["contextSelector"]
        key = tuple(selector[k] for k in names)
        actual = results.get(key)
        expected = {
            "transformationRuleId": golden["expectedTransformationRuleId"],
            "finalAxesChecked": golden["expectedFinalAxesChecked"],
            "hostTerminationChecked": golden["expectedHostTerminationChecked"],
            "exitCodeChecked": golden["expectedExitCodeChecked"],
        }
        if actual != expected:
            errors.append("finalizer golden " + golden["id"])
    return errors, admitted_count, invalid_count

def safe_finalizer_checks(d: Any, v2d: dict[str, Any], d9doc: dict[str, Any], d9mod: types.ModuleType) -> tuple[list[str], int, int]:
    try:
        return finalizer_checks(d, v2d, d9doc, d9mod)
    except Exception as exc:
        return ["finalizer total failure: " + type(exc).__name__], 0, 0

def reduce_from_rows(rows: list[dict[str, Any]], obs: dict[str, Any]) -> str:
    for row in sorted(rows, key=lambda x: x["priority"]):
        predicate = row["predicate"]
        if predicate == "true":
            return row["normalizedFate"]
        clauses = predicate.split(" and ")
        ok = True
        for clause in clauses:
            field, expected = clause.split("=", 1)
            value: Any = True if expected == "true" else False if expected == "false" else expected
            if obs[field] != value:
                ok = False
                break
        if ok:
            return row["normalizedFate"]
    raise ValueError("reducer no fallback")

def reducer_checks(v2d: dict[str, Any], v2mod: types.ModuleType) -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    rows = v2d["orderedNormalizationReducerV2"]["rows"]
    for bits in itertools.product((False, True), repeat=len(v2mod.BOOL_OBSERVATIONS)):
        for terminal in v2mod.TERMINAL_KINDS:
            obs = dict(zip(v2mod.BOOL_OBSERVATIONS, bits)); obs["terminalKind"] = terminal
            if reduce_from_rows(rows, obs) != v2mod.reduce_observation(obs):
                errors.append("reducer divergence")
                return errors, count
            count += 1
    return errors, count

def ri_errors(r: Any, v2r: dict[str, Any], v3r: dict[str, Any] | None = None) -> list[str]:
    try:
        expected_root = [
            "artifact", "version", "status", "reviewStatus", "purpose",
            "predecessorRejection", "protocolReference", "retainedV3ExactProjection", "exactSemanticProjectionOfV2",
            "dependencyPins", "retainedPasses", "residuals", "authority",
            "supersedesOnlyIfIndependentlyAcceptedAndApplied",
        ]
        if not exact_keys(r, expected_root):
            return ["RI root"]
        if r["version"] != 4 or r["status"] != STATUS or r["predecessorRejection"].get("sha256") != REVIEW_SHA:
            return ["RI identity"]
        if r["retainedV3ExactProjection"].get("sourceSha256") != PRESERVED_HASHES[V3_RI] or r["retainedV3ExactProjection"].get("semanticSelector") != "/exactSemanticProjectionOfV2":
            return ["RI v3 binding"]
        metadata = {"artifact", "version", "status", "reviewStatus", "purpose", "protocolReference", "rejectionBasis", "residuals", "authority", "supersedesOnlyIfIndependentlyAcceptedAndApplied"}
        selectors = [k for k in v2r if k not in metadata]
        projection = r["exactSemanticProjectionOfV2"]
        expected = [{"selector": "/" + key, "compactOrderedJsonSha256": compact_sha(v2r[key])} for key in selectors]
        if projection["sourceSha256"] != PRESERVED_HASHES[V2_RI] or projection["inheritedTopLevelSelectors"] != selectors or projection["selectorCommitments"] != expected:
            return ["RI semantic projection"]
        if v3r is not None:
            old_projection = v3r["exactSemanticProjectionOfV2"]
            for key in old_projection:
                if key != "projectionAlgorithm" and not exact_json_equal(projection[key], old_projection[key]):
                    return ["RI v3 semantic drift " + key]
        if r["authority"].get("selfReview") is not False or r["authority"].get("applied") is not False:
            return ["RI authority"]
        return []
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return ["hostile RI: " + type(exc).__name__]

def response_errors(a: Any, checker_hash: str) -> list[str]:
    try:
        expected_root = [
            "artifact", "version", "status", "reviewStatus", "purpose",
            "sourceReview", "candidateSet", "exactFilesCreated",
            "findingDispositions", "retainedPasses", "checkerExecutionRecord",
            "hashRecord", "preExistingByteIdentity", "residuals", "authority",
        ]
        if not exact_keys(a, expected_root):
            return ["response root"]
        if a["artifact"] != "opensip.rust-provider-protocol.v4.adjudication-v3-rejection-response" or a["version"] != 1 or a["status"] != STATUS:
            return ["response identity"]
        if a["sourceReview"] != {"path": V3_REVIEW, "sha256": REVIEW_SHA, "decision": "REJECT", "blockingFindingCount": 3}:
            return ["response review"]
        expected_set = [PROTOCOL, CHECKER, RESPONSE, DELIVERY, RI_JOIN]
        if a["candidateSet"] != expected_set or a["exactFilesCreated"] != ["docs/coop/artifacts/" + x for x in expected_set]:
            return ["response candidate set"]
        dispositions = a["findingDispositions"]
        if [x.get("id") for x in dispositions] != ["RPPV3-PF-01-NULL-NOMINAL-TYPE-CONTRADICTS-EXACT-TYPE", "RPPV3-PF-02-TRANSITION-FAULT-ATOMICITY-AND-PRECHECK-ORDER-DIVERGE", "RPPV3-PF-03-ADMITTED-TUPLE-COMMITMENT-ENCODING-UNDECLARED-FIELD"] or any(x.get("v4Disposition") != "REPAIRED-IN-CANDIDATE-AWAITING-INDEPENDENT-REVIEW" for x in dispositions):
            return ["response dispositions"]
        hashes = a["hashRecord"]
        if not exact_keys(hashes, ["protocolSha256", "deliveryJoinSha256", "resolvedInputsJoinSha256", "checkerSha256", "selfHash", "state"]) or hashes.get("state") != "TWO-STABLE-POST-RUN-REHASHES-COMPLETE":
            return ["response hash record"]
        if hashes.get("protocolSha256") != LOCAL_JSON_HASHES[PROTOCOL] or hashes.get("deliveryJoinSha256") != LOCAL_JSON_HASHES[DELIVERY] or hashes.get("resolvedInputsJoinSha256") != LOCAL_JSON_HASHES[RI_JOIN] or hashes.get("checkerSha256") != checker_hash or hashes.get("selfHash") != "Not embedded; self-referential file hashing is not an authority mechanism.":
            return ["response hashes"]
        record = a["checkerExecutionRecord"]
        record_keys = [
            "requiredNormalCommand", "requiredSelftestCommand", "normalExit",
            "selftestExit", "normalPositiveCount", "normalAdversarialCount",
            "selftestPositiveCount", "selftestAdversarialCount",
            "v2SemanticPositive", "v2SemanticAdversarial", "v2ReducerTuples",
            "v2StateTraces", "v2Mutations", "retainedV3NormalExit", "retainedV3SelftestExit",
            "retainedV3ReducerTuples", "retainedV3FsmTraces", "retainedV3FsmTotalityComparisons",
            "retainedV3TransitionRules", "retainedV3FinalizerFullDomain", "retainedV3FinalizerAdmitted",
            "retainedV3FinalizerInvalid", "retainedV3FinalizerGoldens", "retainedV3Mutations",
            "v4ReducerTuples", "v4FsmTraces", "v4FsmTotalityComparisons", "v4TransitionRules",
            "v4NominalTypeProbes", "v4RepairWitnesses", "v4FinalizerFullDomain", "v4FinalizerAdmitted",
            "v4FinalizerInvalid", "v4FinalizerGoldens", "v4Mutations", "harnessEscapes", "state",
        ]
        if not exact_keys(record, record_keys):
            return ["response execution record fields"]
        expected_counts = {
            "normalExit": 0, "selftestExit": 0,
            "normalPositiveCount": 14, "normalAdversarialCount": 12,
            "selftestPositiveCount": 15, "selftestAdversarialCount": 12,
            "v2SemanticPositive": 263, "v2SemanticAdversarial": 68,
            "v2ReducerTuples": 12288, "v2StateTraces": 78, "v2Mutations": 42,
            "retainedV3NormalExit": 0, "retainedV3SelftestExit": 0,
            "retainedV3ReducerTuples": 12288, "retainedV3FsmTraces": 78,
            "retainedV3FsmTotalityComparisons": 522, "retainedV3TransitionRules": 28,
            "retainedV3FinalizerFullDomain": 2304, "retainedV3FinalizerAdmitted": 148,
            "retainedV3FinalizerInvalid": 2156, "retainedV3FinalizerGoldens": 7,
            "retainedV3Mutations": 36,
            "v4ReducerTuples": 12288, "v4FsmTraces": 78,
            "v4FsmTotalityComparisons": 522, "v4TransitionRules": 28,
            "v4NominalTypeProbes": 187, "v4RepairWitnesses": 12,
            "v4FinalizerFullDomain": 2304, "v4FinalizerAdmitted": 148,
            "v4FinalizerInvalid": 2156, "v4FinalizerGoldens": 7,
            "v4Mutations": 52, "harnessEscapes": 6,
        }
        if any(record.get(k) != v for k, v in expected_counts.items()):
            return ["response execution counts"]
        if record.get("requiredNormalCommand") != "python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v4.py" or record.get("requiredSelftestCommand") != "python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v4.py --selftest" or record.get("state") != "NORMAL-AND-SELFTEST-PASS":
            return ["response execution command/state"]
        manifest, digest = preserved_manifest()
        preserve = a["preExistingByteIdentity"]
        if preserve.get("subjects") != manifest or preserve.get("aggregateSha256") != digest or preserve.get("allMatchedAfter") is not True:
            return ["response preservation"]
        auth = a["authority"]
        if auth.get("selfReview") is not False or auth.get("independentReviewPerformed") is not False or auth.get("applied") is not False or any(auth.get(x) != "NONE" for x in ["integrationAuthority", "productAuthority", "freezeAuthority", "releaseAuthority"]):
            return ["response authority"]
        return []
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return ["hostile response: " + type(exc).__name__]

def v2_replay(v2mod: types.ModuleType, docs: dict[str, Any], raw: dict[str, bytes], deps: dict[str, Any], selftest: bool) -> tuple[list[str], dict[str, int]]:
    v2docs = {
        v2mod.PROTOCOL: docs[V2_PROTOCOL],
        v2mod.DELIVERY_JOIN: docs[V2_DELIVERY],
        v2mod.RI_JOIN: docs[V2_RI],
        v2mod.RESPONSE: docs[V2_RESPONSE],
    }
    v2raw = {
        v2mod.PROTOCOL: raw[V2_PROTOCOL], v2mod.DELIVERY_JOIN: raw[V2_DELIVERY],
        v2mod.RI_JOIN: raw[V2_RI], v2mod.RESPONSE: raw[V2_RESPONSE],
        v2mod.CHECKER: raw[V2_CHECKER],
    }
    v2deps = {name: deps[name] for name in v2mod.DEPENDENCY_HASHES}
    report = v2mod.CheckReport()
    reducer, traces = v2mod.run_semantic_checks(report, v2docs, v2deps, v2raw)
    errors = []
    if report.failures != ["pre-existing full bytes", "pre-existing source bytes ignoring pyc"]:
        errors.append("v2 replay failures: " + repr(report.failures))
    if (report.positive, report.adversarial, reducer, traces) != (263, 68, 12288, 78):
        errors.append("v2 replay counts")
    mutations = 0
    if selftest:
        mutation_report = v2mod.CheckReport()
        mutations = v2mod.run_selftest(mutation_report, v2docs)
        if mutations != 42 or mutation_report.failures:
            errors.append("v2 mutation replay")
    return errors, {"positive": report.positive, "adversarial": report.adversarial, "reducer": reducer, "traces": traces, "mutations": mutations}

def v3_replay_main(v3mod: types.ModuleType, selftest: bool) -> tuple[list[str], str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = v3mod.main()
    except Exception as exc:
        return ["v3 checker escape " + type(exc).__name__], ""
    output = stdout.getvalue().strip()
    diagnostic = stderr.getvalue().strip()
    mode = "selftest" if selftest else "normal"
    expected_prefix = "RPPV3-PASS mode=" + mode
    if exit_code != 0 or diagnostic or not output.startswith(expected_prefix) or "fsm_traces=78" not in output or "fsm_totality=522" not in output or "finalizer_admitted=148" not in output or "finalizer_invalid=2156" not in output or (selftest and ("mutations=36" not in output or "harness_escapes=6" not in output)):
        return ["v3 checker replay failed exit=" + str(exit_code) + " stderr=" + diagnostic[:160]], output
    return [], output

def all_document_errors(docs: Any, v2docs: Mapping[str, Any], d9doc: dict[str, Any], checker_hash: str) -> list[str]:
    if type(docs) is not dict or set(docs) != {PROTOCOL, DELIVERY, RI_JOIN, RESPONSE}:
        return ["candidate document set"]
    errors = []
    errors += protocol_errors(docs[PROTOCOL], v2docs[V2_PROTOCOL])
    if V3_PROTOCOL in v2docs:
        errors += v3_protocol_preservation_errors(docs[PROTOCOL], v2docs[V3_PROTOCOL])
    errors += delivery_projection_errors(docs[DELIVERY], v2docs[V2_DELIVERY], d9doc)
    if V3_DELIVERY in v2docs:
        errors += v3_delivery_preservation_errors(docs[DELIVERY], v2docs[V3_DELIVERY])
    errors += ri_errors(docs[RI_JOIN], v2docs[V2_RI], v2docs.get(V3_RI))
    errors += response_errors(docs[RESPONSE], checker_hash)
    return errors

DELETE = object()
def mutate(root: dict[str, Any], document: str, path: tuple[Any, ...], replacement: Any) -> dict[str, Any]:
    if document not in root:
        raise ValueError("missing document")
    out = copy.deepcopy(root)
    target: Any = out[document]
    for part in path[:-1]:
        target = target[part]
    leaf = path[-1]
    original = target[leaf]
    if replacement is DELETE:
        if type(target) is dict:
            del target[leaf]
        elif type(target) is list:
            target.pop(leaf)
        else:
            raise ValueError("delete target")
    else:
        if original == replacement:
            raise ValueError("no-op")
        target[leaf] = replacement
    return out

def mutation_specs(docs: dict[str, Any]) -> list[tuple[str, str, tuple[Any, ...], Any]]:
    p = docs[PROTOCOL]["orderingAndStateMachineV4"]
    d = docs[DELIVERY]["hostFinalizerBoundaryV4"]
    return [
        ("M01-GUARD-EXTRA", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 0, "guard"), {"op": "true", "extra": 0}),
        ("M02-GUARD-MISSING", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 2, "guard", "right"), DELETE),
        ("M03-OPERAND-TYPE", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 2, "guard", "right", "nominalType"), "boolean"),
        ("M04-REFERENCE-PATH", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 2, "guard", "left", "path"), "event.repository_mode"),
        ("M05-PRESTATE-READ", PROTOCOL, ("orderingAndStateMachineV4", "actionUnionV4", "readSemantics"), "IMMUTABLE_PRESTATE"),
        ("M06-COMMIT-PARTIAL", PROTOCOL, ("orderingAndStateMachineV4", "actionUnionV4", "commitSemantics"), "commit each action"),
        ("M07-SHORT-CIRCUIT", PROTOCOL, ("orderingAndStateMachineV4", "guardUnionV4", "variants", 1, "runtimeAlgorithm"), "EVALUATE_ALL_EAGER"),
        ("M08-OVERFLOW", PROTOCOL, ("orderingAndStateMachineV4", "actionUnionV4", "overflow"), "wrap"),
        ("M09-INVARIANT-FATE", PROTOCOL, ("orderingAndStateMachineV4", "stateRecordV4", "evaluation"), "raise implementation exception"),
        ("M10-INVARIANT-DROP", PROTOCOL, ("orderingAndStateMachineV4", "stateRecordV4", "stateInvariantsV4", 4), DELETE),
        ("M11-SELECTOR-EXTRA", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 0, "eventSelector"), {"selectorKind": "frame", "frameType": "Hello", "future": True}),
        ("M12-RULE-PRIORITY", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 2, "priority"), 99),
        ("M13-RULE-PHASE", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 2, "phaseIn"), ["START"]),
        ("M14-RULE-ACTION", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 0, "actions", 0, "target"), "state.stageIndex"),
        ("M15-FALLBACK-DROP", PROTOCOL, ("orderingAndStateMachineV4", "transitionRulesV4", 27), DELETE),
        ("M16-FALLBACK-ACTION", PROTOCOL, ("orderingAndStateMachineV4", "fallbackRule", "onlyAction", "value", "value"), "DONE"),
        ("M17-EVENT-UNKNOWN-FATE", PROTOCOL, ("orderingAndStateMachineV4", "eventUnionV4", "runtimeUnknownFieldOrVariantFate"), "ignore"),
        ("M18-AST-DEPTH", PROTOCOL, ("schemaLanguageV4", "recursiveBounds", "maxGuardDepth"), 999),
        ("M19-PROTOCOL-STATUS", PROTOCOL, ("status",), "APPLIED"),
        ("M20-BASE-AXIS-DROP", DELIVERY, ("hostFinalizerBoundaryV4", "baseAxesContract", "profiles", 0, "axes", "faultCause"), DELETE),
        ("M21-BASE-AXIS-TYPE", DELIVERY, ("hostFinalizerBoundaryV4", "baseAxesContract", "profiles", 0, "axes", "secondaryDeficiencies"), {}),
        ("M22-D9-SCHEMA", DELIVERY, ("hostFinalizerBoundaryV4", "pinnedD9Projection", "scenarioAxesSchema", "properties", "commandKind", "required"), False),
        ("M23-DOMAIN-COUNT", DELIVERY, ("hostFinalizerBoundaryV4", "finiteContextDomain", "admittedCount"), 147),
        ("M24-DOMAIN-COMMIT", DELIVERY, ("hostFinalizerBoundaryV4", "finiteContextDomain", "admittedTupleCommitment"), "sha256:" + "0" * 64),
        ("M25-CANCEL-NONE", DELIVERY, ("hostFinalizerBoundaryV4", "finiteContextDomain", "admittedRows", 1, "interruptionTiming"), ["none"]),
        ("M26-TRANSFORM-PRIORITY", DELIVERY, ("hostFinalizerBoundaryV4", "transformationV4", "rules", 0, "priority"), 99),
        ("M27-OPTIONAL-NOT-IDENTITY", DELIVERY, ("hostFinalizerBoundaryV4", "transformationV4", "rules", 5, "axesAlgorithm"), "PROVIDER_DEFICIENCY_PATCH"),
        ("M28-FAULT-PRECEDENCE", DELIVERY, ("hostFinalizerBoundaryV4", "transformationV4", "causePrecedence"), ["deficiency", "faultCause", "rejectionCause"]),
        ("M29-SETTLED-BYTES", DELIVERY, ("hostFinalizerBoundaryV4", "settlementOptionV4", "exactSettledFixture", "hostTerminationCanonicalBytesHex"), "00"),
        ("M30-FORBIDDEN-RESULT", DELIVERY, ("hostFinalizerBoundaryV4", "transformationV4", "forbiddenResults"), []),
        ("M31-GOLDEN-EXIT", DELIVERY, ("hostFinalizerBoundaryV4", "narrowGoldens", 0, "expectedExitCodeChecked"), 3),
        ("M32-RI-SELECTOR", RI_JOIN, ("exactSemanticProjectionOfV2", "inheritedTopLevelSelectors"), []),
        ("M33-RI-COMMIT", RI_JOIN, ("exactSemanticProjectionOfV2", "selectorCommitments", 0, "compactOrderedJsonSha256"), "sha256:" + "0" * 64),
        ("M34-RESPONSE-FINDINGS", RESPONSE, ("findingDispositions",), []),
        ("M35-RESPONSE-AUTHORITY", RESPONSE, ("authority", "selfReview"), True),
        ("M36-RESPONSE-STATUS", RESPONSE, ("status",), "APPLIED"),
        ("M37-NULL-TYPING-PROSE", PROTOCOL, ("schemaLanguageV4", "exactType"), "Null is always rejected."),
        ("M38-NULLABLE-U64-DROP-NULL", PROTOCOL, ("orderingAndStateMachineV4", "nominalTypes", "nullable-uint64", "jsonType"), "integer"),
        ("M39-ENUM-DROP-NULL", PROTOCOL, ("orderingAndStateMachineV4", "nominalTypes", "repository-mode", "enum"), ["disabled", "prepared"]),
        ("M40-FAULT-ABSORPTION-ORDER", PROTOCOL, ("orderingAndStateMachineV4", "prechecksV4", "evaluationOrder"), ["runtimeStateAndEventClosedShape", "faultAbsorption", "preInvariantCheck", "terminalOutputPrecheck", "framePrecheck", "firstMatchingRule", "postInvariantCheck", "atomicCommit"]),
        ("M41-ABSORPTION-RESULT", PROTOCOL, ("orderingAndStateMachineV4", "prechecksV4", "faultAbsorption", "onTrue", "transitionResultKind"), "RUNTIME_FAULT_ROLLBACK"),
        ("M42-TERMINAL-DOES-NOT-STOP", PROTOCOL, ("orderingAndStateMachineV4", "prechecksV4", "terminalOutputPrecheck", "stopAfterTrue"), False),
        ("M43-FALLBACK-DROPS-PRECHECK", PROTOCOL, ("orderingAndStateMachineV4", "prechecksV4", "firstMatchingRule", "fallbackCommitsAcceptedFramePrecheckWrites"), False),
        ("M44-CONTROLLED-RESULT-DROP", PROTOCOL, ("orderingAndStateMachineV4", "transitionResultUnionV4", "variants", 2), DELETE),
        ("M45-TRANSACTION-ALGORITHM-DROP", PROTOCOL, ("orderingAndStateMachineV4", "transitionTransactionV4", "orderedAlgorithm", 0), DELETE),
        ("M46-TUPLE-SEVENTH-FIELD", DELIVERY, ("hostFinalizerBoundaryV4", "finiteContextDomain", "tupleRecordV4Schema", "required"), d["finiteContextDomain"]["dimensionOrder"] + ["admissionRuleId"]),
        ("M47-TUPLE-ENCODING-METADATA", DELIVERY, ("hostFinalizerBoundaryV4", "finiteContextDomain", "tupleEncoding"), "UTF-8 compact JSON including admission metadata"),
        ("M48-INVALID-COMMITMENT", DELIVERY, ("hostFinalizerBoundaryV4", "finiteContextDomain", "invalidCombinations", "tupleCommitment"), "sha256:" + "0" * 64),
        ("M49-V3-FROZEN-SUBJECT", PROTOCOL, ("retainedV3RepairBoundary", "frozenSubjects", 0, "sha256"), "0" * 64),
        ("M50-REPAIR-WITNESS-DROP", PROTOCOL, ("orderingAndStateMachineV4", "modelCheckDomain", "requiredRepairWitnesses", 11), DELETE),
        ("M51-NONOBJECT-RESULT-DROP", PROTOCOL, ("orderingAndStateMachineV4", "transitionResultUnionV4", "variants", 4), DELETE),
        ("M52-PRECHECK-CLOSED-SCHEMA", PROTOCOL, ("orderingAndStateMachineV4", "precheckRecordSchemasV4", "records", 0, "required"), ["when", "priority"]),
    ]

def selftest_errors(docs: dict[str, Any], v2docs: Mapping[str, Any], d9doc: dict[str, Any], d9mod: types.ModuleType, checker_hash: str) -> tuple[list[str], int, int]:
    errors: list[str] = []
    specs = mutation_specs(docs)
    ids = [x[0] for x in specs]
    if len(ids) != len(set(ids)):
        return ["duplicate mutation id"], 0, 0
    applied = 0
    for ident, document, path, replacement in specs:
        try:
            mutated = mutate(docs, document, path, replacement)
        except Exception as exc:
            errors.append("mutation apply escape " + ident + ":" + type(exc).__name__)
            continue
        applied += 1
        static = all_document_errors(mutated, v2docs, d9doc, checker_hash)
        if not static:
            fsm, _, _, _ = safe_fsm_checks(mutated[PROTOCOL], v2docs[V2_PROTOCOL])
            final, _, _ = safe_finalizer_checks(mutated[DELIVERY], v2docs[V2_DELIVERY], d9doc, d9mod)
            nominal, _ = nominal_probe_checks(mutated[PROTOCOL])
            witnesses, _ = repair_witness_checks(mutated[PROTOCOL], v2docs[V2_PROTOCOL])
            static = fsm + final + nominal + witnesses
        if not static:
            errors.append("mutation survived " + ident)
    escapes = 0
    for label, thunk in [
        ("no-op", lambda: mutate(docs, PROTOCOL, ("version",), 4)),
        ("failed", lambda: mutate(docs, PROTOCOL, ("missing",), 1)),
        ("ambiguous", lambda: (_ for _ in ()).throw(ValueError("ambiguous path"))),
        ("duplicate", lambda: (_ for _ in ()).throw(ValueError("duplicate id"))),
        ("skip", lambda: False if applied == len(specs) else True),
        ("dirty-base", lambda: False if all_document_errors({**docs, PROTOCOL: None}, v2docs, d9doc, checker_hash) else True),
    ]:
        try:
            result = thunk()
        except Exception:
            escapes += 1
            continue
        if result is False:
            escapes += 1
        else:
            errors.append(label + " harness escape accepted")
    return errors, applied, escapes

def main() -> int:
    if sys.argv[1:] not in ([], ["--selftest"]):
        print("RPPV4-UNSUPPORTED-INVOCATION: require no arguments or --selftest", file=sys.stderr)
        return 2
    selftest = sys.argv[1:] == ["--selftest"]
    report = Report()
    before_pyc = pyc_snapshot()
    try:
        docs: dict[str, Any] = {}
        raw: dict[str, bytes] = {}
        for name, expected in LOCAL_JSON_HASHES.items():
            docs[name], raw[name] = read_hashed(name, expected)
        raw[CHECKER] = (HERE / CHECKER).read_bytes()
        checker_hash = sha(raw[CHECKER])
        docs[RESPONSE] = strict_loads((HERE / RESPONSE).read_text())
        raw[RESPONSE] = (HERE / RESPONSE).read_bytes()
        preserved: dict[str, Any] = {}
        for name, expected in PRESERVED_HASHES.items():
            if name.endswith(".py"):
                source = (HERE / name).read_bytes()
                if sha(source) != expected:
                    raise StrictJsonError(name + " hash")
                preserved[name] = None
                raw[name] = source
            else:
                value, source = read_hashed(name, expected)
                preserved[name] = value
                raw[name] = source
        deps: dict[str, Any] = {}
        for name, expected in DEPENDENCY_HASHES.items():
            if name.endswith(".py"):
                raw[name] = (HERE / name).read_bytes()
                if sha(raw[name]) != expected:
                    raise StrictJsonError(name + " hash")
            else:
                deps[name], raw[name] = read_hashed(name, expected, True)
        # Response is deliberately not self-hash pinned; its four other exact hashes are checked structurally.
        v3mod = execute_verified(V3_CHECKER, PRESERVED_HASHES[V3_CHECKER], "opensip_rppv3_verified")
        v2mod = execute_verified(V2_CHECKER, PRESERVED_HASHES[V2_CHECKER], "opensip_rppv2_verified")
        d9mod = execute_verified(D9_CHECKER, DEPENDENCY_HASHES[D9_CHECKER], "opensip_d9v113_verified")
    except Exception as exc:
        print("RPPV4-FAIL load: " + type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 1
    v2docs = {
        V3_PROTOCOL: preserved[V3_PROTOCOL], V3_DELIVERY: preserved[V3_DELIVERY], V3_RI: preserved[V3_RI], V3_RESPONSE: preserved[V3_RESPONSE],
        V2_PROTOCOL: preserved[V2_PROTOCOL], V2_DELIVERY: preserved[V2_DELIVERY], V2_RI: preserved[V2_RI], V2_RESPONSE: preserved[V2_RESPONSE],
    }
    report.expect(not all_document_errors(docs, v2docs, deps[D9], checker_hash), "document closure: " + "; ".join(all_document_errors(docs, v2docs, deps[D9], checker_hash)[:4]))
    # Strict JSON and hostile roots are total.
    for source in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":1.5}', '{"a":-Infinity}']:
        report.reject(lambda source=source: strict_loads(source), "strict JSON accepted " + source)
    for hostile in [None, True, 1, "x", [], [1], {"unexpected": {}}]:
        report.reject(lambda hostile=hostile: False if all_document_errors(hostile, v2docs, deps[D9], checker_hash) else True, "hostile root")
    manifest, manifest_hash = preserved_manifest()
    report.expect(all(sha((HERE / row["path"]).read_bytes()) == row["sha256"] for row in manifest), "v1/v2 byte preservation")
    report.expect(manifest_hash == sha_ref(compact(manifest)), "preservation aggregate")
    v2err, v2counts = v2_replay(v2mod, preserved, raw, deps, selftest)
    report.expect(not v2err, "v2 semantic replay: " + "; ".join(v2err))
    v3err, v3output = v3_replay_main(v3mod, selftest)
    report.expect(not v3err, "v3 exact checker replay: " + "; ".join(v3err))
    fsmerr, traces, totality, rules = safe_fsm_checks(docs[PROTOCOL], v2docs[V2_PROTOCOL])
    report.expect(not fsmerr, "v4 FSM: " + "; ".join(fsmerr[:4]))
    nominalerr, nominal_probes = nominal_probe_checks(docs[PROTOCOL])
    report.expect(not nominalerr, "v4 nominal probes: " + "; ".join(nominalerr[:4]))
    witnesserr, repair_witnesses = repair_witness_checks(docs[PROTOCOL], v2docs[V2_PROTOCOL])
    report.expect(not witnesserr, "v4 repair witnesses: " + "; ".join(witnesserr[:4]))
    reducer_err, reducer_count = reducer_checks(v2docs[V2_DELIVERY], v2mod)
    report.expect(not reducer_err and reducer_count == EXPECTED_REDUCER, "reducer replay")
    finalerr, admitted, invalid = safe_finalizer_checks(docs[DELIVERY], v2docs[V2_DELIVERY], deps[D9], d9mod)
    report.expect(not finalerr, "finalizer: " + "; ".join(finalerr[:4]))
    report.expect((traces, totality, rules) == (78, 522, 28), "FSM exact counts")
    report.expect((admitted, invalid) == (148, 2156), "finalizer exact counts")
    report.expect(not ri_errors(docs[RI_JOIN], v2docs[V2_RI]), "RI exact projection")
    mutations = escapes = 0
    if selftest:
        if report.failures:
            print("RPPV4-DIRTY-BASE: mutation selftest refused", file=sys.stderr)
            for failure in report.failures[:30]:
                print("  " + failure, file=sys.stderr)
            return 1
        serr, mutations, escapes = selftest_errors(docs, v2docs, deps[D9], d9mod, checker_hash)
        report.expect(not serr and mutations == 52 and escapes == 6, "mutation suite: " + "; ".join(serr[:6]))
    report.expect(pyc_snapshot() == before_pyc, "no pyc creation/change")
    if report.failures:
        print(f"RPPV4-FAIL mode={'selftest' if selftest else 'normal'} positive={report.positive} adversarial={report.adversarial} v2_positive={v2counts['positive']} v2_adversarial={v2counts['adversarial']} reducer={reducer_count} fsm_traces={traces} fsm_totality={totality} nominal_probes={nominal_probes} repair_witnesses={repair_witnesses} finalizer_admitted={admitted} finalizer_invalid={invalid} mutations={mutations} harness_escapes={escapes}", file=sys.stderr)
        for failure in report.failures[:40]:
            print("  " + failure, file=sys.stderr)
        return 1
    print(f"RPPV4-PASS mode={'selftest' if selftest else 'normal'} positive={report.positive} adversarial={report.adversarial} v2_positive={v2counts['positive']} v2_adversarial={v2counts['adversarial']} v2_mutations={v2counts['mutations']} retained_v3=true reducer={reducer_count} fsm_traces={traces} fsm_totality={totality} rules={rules} nominal_probes={nominal_probes} repair_witnesses={repair_witnesses} finalizer_full={admitted+invalid} finalizer_admitted={admitted} finalizer_invalid={invalid} finalizer_goldens=7 mutations={mutations} harness_escapes={escapes}")
    print("RPPV4-RESIDUAL independent-review-required applied=false self_review=false product=false integration=false freeze=false release=false")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
