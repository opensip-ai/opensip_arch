#!/usr/bin/env python3
"""Retained executable checker for the C-2 plan/stage contract, v4.

WHY v4 EXISTS
-------------
c2-plan-stage-schema.v3.json was independently reviewed AT ITS LIVE BYTES
(3c488ff6..., checker 4f31d57c...) on 2026-08-02 and the verdict was REJECT with
two blocking findings.  This checker is the retained instrument for the repair
candidate.  It creates NOTHING and edits NOTHING: v3 and check-c2.py stay
byte-identical as historical input and stay pinned by their existing consumers.

  LB-C2-01  BLOCKING.  v3 guarded both commitment-bearing schemaVersion fields
            with a bare inequality against the integer 1.  In the host language
            True == 1 and 1.0 == 1, so a wire PlanIntent spelling schemaVersion
            as JSON true was ADMITTED and committed to a SECOND digest, and one
            spelling it as JSON 1.0 was ADMITTED and then raised an unguarded
            ValueError inside the canonical encoder.  20 cases across seven
            fixtures, both intentKind branches, both positions.  Repaired here
            by exact-type guards AND by a scan of this checker's own syntax tree
            that refuses any bare numeric comparison against a wire-sourced value
            anywhere in the reachable validator closure, so a fifth site cannot
            be added silently.  The sweep found two sites the finding did not
            name by location: planIdentityInputs.planSchemaMajor and
            planIntentTotalityMatrix.caseCount.

  LB-C2-02  BLOCKING.  validate_coverage raised on seven hostile roots and
            silently conformed six FALSY relation values, because it wrote
            `if factplane and relation:` and therefore skipped the declared C2X
            registry lookup whenever relation was null, 0, false, "", [] or {}.
            58 of 81 mutations produced no finding.  Repaired here by a
            non-object-root guard, a named-finding boundary, an isinstance-driven
            registry lookup, closed entry shape and per-field type validation.

  LB-C2-03  subjectScopeCommitment bound by presence only; the shipped value
            "sha256:..." violated C-2's own sha256Id grammar.
  LB-C2-04  validate_plan raised TypeError on container-valued kind/operator.
  LB-C2-05  planId / snapshotId / executionId named but ungrammared.
  LB-C2-06  an unattributed byte state between an independent PASS and the live
            file; recorded in the candidate's `lineage` rather than lost.

THE STANDING REQUIREMENT
------------------------
Five surfaces in this corpus have shipped a totality claim quantified over a
region their own instrument could not observe.  v3's 4x4 hostile matrix was
PINNED never to reach a scalar leaf, and LB-C2-01 lived at a scalar leaf.  This
checker therefore enumerates EVERY position of every retained fixture and of the
candidate document - the root, every object key and every array index at
unlimited depth, CONTAINER AND SCALAR LEAF alike - and publishes the live
measured counts.  Understating the space is a finding, not an omission.

Usage: python3 -I -B artifacts/check-c2-v4.py [contract]  ·  --selftest
Exit:  0 clean or green selftest · 1 findings · 2 unsupported invocation or a
       pinned input that does not hash to its declared digest · 3 --selftest
       REFUSED over a dirty base, which can never be absorbed into a pass.

Scope: checker-scope evidence only.  SPECIFIED / IMPLEMENTABLE_UNEXECUTED.
CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW.  A green run is authored by
the same lane that authored the contract and is not review, qualification,
demonstration, seal, freeze, integration or product acceptance.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import sys
import types
import unicodedata
from contextlib import redirect_stdout

BINDING = "c2-plan-stage-schema.v4.json"
DECLARED_FLAGS = ("--selftest",)
HERE = pathlib.Path(__file__).resolve().parent

D9 = "d9-exit-contract.v1.6.json"
FP = "fact-plane.v1.json"
TM = "threat-model.v3.json"
OP = "operability.v2.json"
DELIVERY = "delivery.v2.json"
RESOLVED_INPUTS = "resolved-inputs.v2.json"
V3_CONTRACT = "c2-plan-stage-schema.v3.json"
V3_CHECKER = "check-c2.py"
V3_REVIEW = "c2-plan-stage-schema.v3.review-independent-livebytes.json"

# Hash-before-execution.  Every pinned transitive input is read once, verified
# against the digest below, and then parsed or EXECUTED from that verified byte
# string rather than re-read from disk.  check-c2.py is pinned at exactly the
# bytes the live-bytes review bound, and is executed as an INDEPENDENT ENCODER:
# the seven planIntentCommitment vectors must reproduce under it as well as
# under this checker, so a repair that moved a commitment cannot pass quietly.
PINS: dict[str, str] = {
    D9: "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    FP: "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    TM: "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    OP: "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    DELIVERY: "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    RESOLVED_INPUTS: "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    V3_CONTRACT: "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    V3_CHECKER: "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3",
    V3_REVIEW: "0f297bed7d8c83e6bd96e54fe40bcda14281b3e4bcedf96e1173d14fbe60a3a3",
}

# The verdict the pinned review must actually carry.  A repair lane that quietly
# points at a different review, or at a review whose verdict has been softened,
# is refused at load rather than reported as a finding.
REVIEW_BINDING = {"verdict": "REJECT", "blockingFindingCount": 2,
                  "blockingFindings": ["LB-C2-01", "LB-C2-02"]}

MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
    ZeroDivisionError, OverflowError, RecursionError,
)


class AuthorityLoadError(RuntimeError):
    """A pinned input could not be admitted as authority."""


class PinMismatch(AuthorityLoadError):
    """A pinned byte string does not hash to its declared digest."""


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this checker does not accept."""


class _VerifiedSourceLoader:
    """Execute exactly the bytes that were hash-verified, never a re-read."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec):
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_snapshot(name: str, filename: str, source: bytes) -> types.ModuleType:
    path = (HERE / filename).resolve()
    loader = _VerifiedSourceLoader(path, source)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    if spec is None or spec.loader is None:
        raise AuthorityLoadError(f"cannot construct verified spec for {filename}")
    module = importlib.util.module_from_spec(spec)
    prior = sys.modules.get(name)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if prior is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = prior
    return module


class Authority:
    """Everything admitted after hash verification, and nothing else."""

    def __init__(self, snapshots, parsed, modules):
        self.snapshots = snapshots
        self.parsed = parsed
        self.modules = modules
        self.census = None
        self.contract_census = None
        # The leaf-inclusive census layer is itself the instrument.  It runs in
        # full on every ordinary invocation.  While the contract-root hostile
        # matrix is driving check() over ~20k mutated copies of the whole
        # document, re-running the instrument inside every case would multiply
        # the cost by two orders of magnitude, so it is disabled for exactly
        # that window and the candidate declares this in contractRoot.
        self.census_enabled = True

    def json(self, name):
        return self.parsed.get(name)

    def module(self, name):
        return self.modules.get(name)


def load_authority(directory: pathlib.Path = HERE) -> Authority:
    """Hash-before-execution over the pinned transitive inputs."""
    snapshots: dict[str, bytes] = {}
    errors: list[str] = []
    for name, expected in PINS.items():
        try:
            source = (directory / name).read_bytes()
        except OSError as exc:
            errors.append(f"{name}: read {type(exc).__name__}: {exc}")
            continue
        actual = hashlib.sha256(source).hexdigest()
        if actual != expected:
            errors.append(f"{name}: {actual} != {expected}")
            continue
        snapshots[name] = source
    if errors:
        raise PinMismatch("; ".join(sorted(errors)))
    parsed: dict[str, object] = {}
    for name in PINS:
        if name.endswith(".json"):
            try:
                parsed[name] = json.loads(snapshots[name].decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise AuthorityLoadError(
                    f"cannot parse pinned data {name}: {type(exc).__name__}") from exc
    review = parsed.get(V3_REVIEW)
    if not isinstance(review, dict):
        raise AuthorityLoadError(f"pinned review {V3_REVIEW} is not an object")
    statement = review.get("verdictStatement")
    statement = statement if isinstance(statement, dict) else {}
    if review.get("verdict") != REVIEW_BINDING["verdict"] or \
            statement.get("verdict") != REVIEW_BINDING["verdict"]:
        raise AuthorityLoadError(
            f"pinned review {V3_REVIEW} does not carry verdict "
            f"{REVIEW_BINDING['verdict']!r}")
    if review.get("blockingFindingCount") != REVIEW_BINDING["blockingFindingCount"] or \
            statement.get("blockingFindings") != REVIEW_BINDING["blockingFindings"]:
        raise AuthorityLoadError(
            f"pinned review {V3_REVIEW} does not carry the two blocking findings "
            f"{REVIEW_BINDING['blockingFindings']} this candidate repairs")
    modules: dict[str, types.ModuleType] = {}
    sink = io.StringIO()
    with redirect_stdout(sink):
        modules[V3_CHECKER] = _execute_snapshot(
            "opensip_c2v4_pinned_v3_checker", V3_CHECKER, snapshots[V3_CHECKER])
    return Authority(snapshots, parsed, modules)


# ---------------------------------------------------------------------------
# Section 1.  The LB-C2-01 guard helpers.
#
# Every integer-constant and integer-range test in this checker routes through
# these three functions.  Nothing else in the reachable validator closure may
# compare a wire-sourced value to a numeric literal, and _integer_guard_scan
# enforces that over this file's own abstract syntax tree on every run.
# ---------------------------------------------------------------------------

INT64_MIN, INT64_MAX = -(2 ** 63), 2 ** 63 - 1


def is_wire_int(value) -> bool:
    """True only for a JSON integer.  A JSON boolean is NOT a JSON integer."""
    return isinstance(value, int) and not isinstance(value, bool)


def exact_int(value, constant) -> bool:
    """Exact-type integer constant guard.  Rejects true, false, 1.0 and "1"."""
    return is_wire_int(value) and value == constant


def int_in_range(value, low, high) -> bool:
    """Exact-type integer range guard."""
    return is_wire_int(value) and low <= value <= high


def _schema_version_ok(value) -> bool:
    """PlanIntent.schemaVersion.  LB-C2-01 site 1."""
    return exact_int(value, 1)


def _descriptor_schema_version_ok(value) -> bool:
    """AdmissionDescriptorV1.schemaVersion.  LB-C2-01 site 2."""
    return exact_int(value, 1)


def _plan_schema_major_ok(value) -> bool:
    """planIdentityInputs.planSchemaMajor.  LB-C2-01 site 3, found by the sweep."""
    return exact_int(value, 1)


def _coverage_schema_version_ok(value) -> bool:
    """Coverage.schemaVersion.  LB-C2-01 class at the LB-C2-02 surface."""
    return exact_int(value, 1)


def _coverage_root_ok(value) -> bool:
    """LB-C2-02: v3 raised on seven hostile Coverage roots."""
    return isinstance(value, dict) and bool(value)


def _coverage_relation_is_checkable(value) -> bool:
    """LB-C2-02: the registry lookup is driven by TYPE, never by truthiness."""
    return isinstance(value, str)


def _subject_scope_shape_ok(value) -> bool:
    """LB-C2-03: sha256Id, not merely present."""
    return isinstance(value, str) and SHA256_ID_RE.fullmatch(value) is not None


def _stage_kind_ok(value) -> bool:
    """LB-C2-04: a container kind must not reach a set-membership test."""
    return isinstance(value, str)


def _stage_operator_ok(value) -> bool:
    """LB-C2-04: a container operator must not reach a set-membership test."""
    return isinstance(value, str)


def json_type_name(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number-with-fraction"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


# ---------------------------------------------------------------------------
# Section 2.  Canonical commitment.
#
# Carried unchanged in its encoding rules from v3, so the seven declared vectors
# must reproduce byte-exactly.  What is NEW is the boundary: plan_intent_commit-
# ment_total returns a named finding instead of raising, and the property "no
# value the validator admits can raise at the encoder" is MEASURED over the
# leaf-inclusive hostile enumeration rather than asserted.
# ---------------------------------------------------------------------------


def _normalise_json(value):
    """The restricted opensip-canonical-json-v1 data model."""
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        raise ValueError("floating-point values are forbidden")
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [_normalise_json(x) for x in value]
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("object key is not a string")
            canonical_key = unicodedata.normalize("NFC", key)
            if canonical_key in out:
                raise ValueError("keys collide after NFC normalisation")
            out[canonical_key] = _normalise_json(item)
        return out
    raise ValueError(f"unsupported JSON value {type(value).__name__}")


def canonical_plan_intent(intent, c) -> bytes:
    spec = c["planIntent"]["canonicalCommitment"]
    if spec.get("domainTagUtf8") != "opensip.plan-intent.v1":
        raise ValueError("unknown PlanIntent commitment domain")
    if spec.get("digest") != "SHA-256" or \
            spec.get("encoding", {}).get("name") != "opensip-canonical-json-v1":
        raise ValueError("unknown PlanIntent commitment algorithm/encoding")
    normal = _normalise_json(intent)
    body = json.dumps(normal, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return spec["domainTagUtf8"].encode("utf-8") + b"\0" + body


def plan_intent_commitment(intent, c) -> str:
    return "sha256:" + hashlib.sha256(canonical_plan_intent(intent, c)).hexdigest()


def plan_intent_commitment_total(intent, c):
    """LB-C2-01, admit-then-raise half.

    validate_plan_intent has carried a totality boundary since v3; the encoder
    did not, so a float schemaVersion that the validator ADMITTED then raised an
    unguarded ValueError inside the evaluation-proof authority join.  Returns
    (commitment, findings): never raises for parsed JSON.
    """
    try:
        return plan_intent_commitment(intent, c), []
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return None, [("C2I-04", "PlanIntent admitted by validation cannot be "
                                 f"canonically encoded: {type(exc).__name__}: {exc}")]


def _pointer_mutate(value, operation):
    """The tiny set/remove fixture mutation language, returning a copy."""
    out = copy.deepcopy(value)
    parts = [p.replace("~1", "/").replace("~0", "~")
             for p in operation["path"].split("/")[1:]]
    parent = out
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    leaf = parts[-1]
    if operation["op"] == "set":
        if isinstance(parent, list):
            parent[int(leaf)] = copy.deepcopy(operation["value"])
        else:
            parent[leaf] = copy.deepcopy(operation["value"])
    elif operation["op"] == "remove":
        if isinstance(parent, list):
            del parent[int(leaf)]
        else:
            parent.pop(leaf, None)
    else:
        raise ValueError(f"unknown fixture mutation op {operation['op']}")
    return out


# ---------------------------------------------------------------------------
# Section 3.  Wire types.
# ---------------------------------------------------------------------------

IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PROJECT_ID_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
RUN_ID_RE = re.compile(r"^run1:[0-9a-f]{64}$")
ARTIFACT_ID_RE = re.compile(
    r"^artifact1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*:sha256:[0-9a-f]{64}$"
)
FACT_VIEW_ID_RE = re.compile(r"^factview1:sha256:[0-9a-f]{64}$")
REQUEST_ID_RE = re.compile(r"^req1_[0-9a-f]{32}$")
BUDGET_KEY_RE = re.compile(
    r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*\."
    r"(?:work-units|milliseconds|bytes|items)$"
)
# LB-C2-05.  planId and snapshotId are joined BYTE-EXACTLY to the live
# resolved-inputs.v2.json patterns; _check fails on any drift, exactly as
# C2I-OP does for REQUEST-ID-V1.  executionId has no cross-contract owner in
# this corpus, so C-2 declares it and says so (RES-C2V4-01).
PLAN_ID_RE = re.compile(r"^plan1:sha256:[0-9a-f]{64}$")
SNAPSHOT_ID_RE = re.compile(r"^snap1:sha256:[0-9a-f]{64}$")
EXECUTION_ID_RE = re.compile(r"^exec1_[0-9a-f]{32}$")


def _exact_object(value, fields) -> bool:
    return isinstance(value, dict) and set(value) == fields


def _is_identifier(value, max_bytes=128) -> bool:
    return isinstance(value, str) and len(value.encode("utf-8")) <= max_bytes and \
        IDENTIFIER_RE.fullmatch(value) is not None


def _is_semver(value) -> bool:
    return isinstance(value, str) and len(value.encode("utf-8")) <= 96 and \
        SEMVER_RE.fullmatch(value) is not None


def _is_sorted_unique_strings(value, *, nonempty=False, max_items=None,
                              validator=_is_identifier) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and \
        (max_items is None or len(value) <= max_items) and \
        all(validator(x) for x in value) and value == sorted(value) and \
        len(value) == len(set(value))


def _is_relative_path(value) -> bool:
    if not isinstance(value, str) or value != unicodedata.normalize("NFC", value):
        return False
    if not int_in_range(len(value.encode("utf-8")), 1, 4096) or \
            value.startswith("/") or "\\" in value or "\0" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def _bounded_parameter(value, *, depth=0) -> bool:
    if not int_in_range(depth, 0, 8):
        return False
    if value is None or isinstance(value, bool):
        return True
    if is_wire_int(value):
        return int_in_range(value, INT64_MIN, INT64_MAX)
    if isinstance(value, float):
        return False
    if isinstance(value, str):
        return value == unicodedata.normalize("NFC", value) and \
            int_in_range(len(value.encode("utf-8")), 0, 4096)
    if isinstance(value, list):
        return int_in_range(len(value), 0, 256) and \
            all(_bounded_parameter(item, depth=depth + 1) for item in value)
    if isinstance(value, dict):
        if not int_in_range(len(value), 0, 64) or \
                not all(isinstance(key, str) for key in value):
            return False
        return list(value) == sorted(value) and \
            all(_is_identifier(key) and _bounded_parameter(item, depth=depth + 1)
                for key, item in value.items())
    return False


def _bounded_parameter_root(value, *, require_map=False) -> bool:
    if require_map and not isinstance(value, dict):
        return False
    if not _bounded_parameter(value):
        return False
    try:
        size = len(json.dumps(_normalise_json(value), ensure_ascii=False,
                              sort_keys=True, separators=(",", ":")).encode("utf-8"))
    except ValueError:
        return False
    return int_in_range(size, 0, 65536)


def _validate_budget(value, sid):
    if not _exact_object(value, {"unit", "limit"}):
        return [("PS-01", f"stage '{sid}': budget is not the exact StageBudgetV1 shape")]
    if value["unit"] not in ("work-units", "milliseconds", "bytes", "items"):
        return [("PS-01", f"stage '{sid}': budget unit is unknown")]
    if not int_in_range(value["limit"], 1, INT64_MAX):
        return [("PS-01", f"stage '{sid}': budget limit is outside 1..INT64_MAX")]
    return []


# ---------------------------------------------------------------------------
# Section 4.  Stage-plan validation.
#
# LB-C2-04: v3 tested `kind not in kinds` against a Python set and
# `operator in {...}` against a set literal with no type guard, so a container
# raised TypeError('unhashable type').  Both membership tests are now preceded
# by an explicit type guard that emits the SAME PS-01 finding, and the public
# entrypoint carries a named-finding boundary.
# ---------------------------------------------------------------------------


def _validate_plan(plan, c, relations, grant_ids=None):
    errs = []
    ss = c["stageSchemas"]
    kinds = set(c["executionPlan"]["stageKinds"])
    private = set(ss["privateOperators"]["names"])
    common = ss["common"]
    stages = plan.get("stages") if isinstance(plan, dict) else None
    if not isinstance(stages, list) or not stages:
        return [("PS-01", "stages must be a non-empty array")]

    stage_ids = [st.get("stageId") if isinstance(st, dict) else None for st in stages]
    if any(not _is_identifier(sid) for sid in stage_ids):
        errs.append(("PS-01", "stageId values must be non-null canonical identifiers"))
    if stage_ids != sorted(stage_ids, key=lambda x: x if isinstance(x, str) else "") or \
            len(stage_ids) != len(set(map(str, stage_ids))):
        errs.append(("PS-01", "stages must be uniquely sorted by stageId"))

    prior = set()
    for st in stages:
        if not isinstance(st, dict):
            errs.append(("PS-01", "stage is not an object"))
            continue
        sid = st.get("stageId", "?")
        kind = st.get("kind")
        if not _stage_kind_ok(kind):
            errs.append(("PS-01", f"stage '{sid}': kind must be a JSON string, not "
                                  f"{json_type_name(kind)} — the kind set is closed"))
            continue
        if kind not in kinds:
            vid = "PS-11" if kind == "snapshot" else "PS-01"
            errs.append((vid, f"stage '{sid}': unknown kind '{kind}' — the kind set is closed"))
            continue
        spec = ss["kinds"][kind]
        for fld in common["required"] + spec["required"]:
            if fld not in st:
                vid = ("PS-10" if fld == "requiredness"
                       else "PS-12b" if kind == "probe" and fld == "capabilityGrants"
                       else "PS-01")
                errs.append((vid, f"stage '{sid}': missing required field '{fld}'"))
        allowed = set(common["required"]) | set(common["optional"]) | \
            set(spec["required"]) | set(spec.get("optional", []))
        for fld in st:
            if fld in private:
                errs.append(("PS-02", f"stage '{sid}': private operator '{fld}' in a serialised plan"))
            elif fld in spec.get("forbidden", []):
                errs.append(("PS-12a", f"stage '{sid}': field '{fld}' is forbidden on kind '{kind}'"))
            elif fld not in allowed:
                errs.append(("PS-01", f"stage '{sid}': field '{fld}' not permitted on kind '{kind}'"))

        depends = st.get("dependsOn", [])
        if "dependsOn" in st and not _is_sorted_unique_strings(depends, nonempty=True):
            errs.append(("PS-01", f"stage '{sid}': dependsOn is not a non-empty sorted identifier set"))
        elif any(dep not in prior for dep in depends):
            errs.append(("PS-01", f"stage '{sid}': dependsOn names self, forward or unknown stage"))
        if "budget" in st:
            errs.extend(_validate_budget(st["budget"], str(sid)))

        if kind == "fact-derivation":
            rels = st.get("relations")
            if not _is_sorted_unique_strings(rels, nonempty=True):
                errs.append(("PS-01", f"stage '{sid}': relations is not a non-empty sorted identifier set"))
            else:
                for rel in rels:
                    if rel not in relations:
                        errs.append(("C2X", f"stage '{sid}': relation '{rel}' is not in the fact-plane registry"))
            operator = st.get("operator")
            if not _stage_operator_ok(operator):
                # LB-C2-04: v3 sent this straight into a set-membership test and
                # raised TypeError('unhashable type') for a list or a dict.
                errs.append(("PS-01", f"stage '{sid}': operator must be a JSON string, not "
                                      f"{json_type_name(operator)}"))
            else:
                if operator not in spec["operatorAuthority"]:
                    errs.append(("PS-01", f"stage '{sid}': operator '{operator}' is not a declared authority"))
                if operator in ("semantic-provider", "external-scanner") and \
                        not _is_identifier(st.get("providerId")):
                    errs.append(("PS-01", f"stage '{sid}': {operator} requires canonical providerId"))
                if operator == "builtin-extractor" and "providerId" in st:
                    errs.append(("PS-01", f"stage '{sid}': builtin-extractor forbids providerId"))
        elif kind == "rule-evaluation":
            if not _is_sorted_unique_strings(st.get("ruleIds"), nonempty=True):
                errs.append(("PS-10", f"stage '{sid}': ruleIds is not a non-empty sorted identifier set"))
            if st.get("requiredness") not in ("required", "optional"):
                errs.append(("PS-10", f"stage '{sid}': requiredness must be required or optional"))
        elif kind == "policy-evaluation":
            if not _is_identifier(st.get("policyId")):
                errs.append(("PS-01", f"stage '{sid}': policyId is not a canonical identifier"))
        elif kind == "probe" and not _is_identifier(st.get("probeId")):
            errs.append(("PS-01", f"stage '{sid}': probeId is not a canonical identifier"))

        if "capabilityGrants" in st:
            refs = st["capabilityGrants"]
            if not _is_sorted_unique_strings(refs, nonempty=True):
                errs.append(("PS-12b" if kind == "probe" else "PS-01",
                             f"stage '{sid}': capabilityGrants is not a non-empty sorted identifier set"))
            elif grant_ids is not None and any(ref not in grant_ids for ref in refs):
                errs.append(("PS-01", f"stage '{sid}': capabilityGrants names an unadmitted grantId"))
        if isinstance(sid, str):
            prior.add(sid)
    return errs


def validate_plan(plan, c, relations, grant_ids=None):
    """Total stage-plan validator: malformed input is data, never an exception."""
    try:
        return _validate_plan(plan, c, relations, grant_ids)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [("PS-01", "malformed parsed JSON rejected at the stage-plan "
                          f"validation boundary: {type(exc).__name__}")]


# ---------------------------------------------------------------------------
# Section 5.  AdmissionDescriptorV1, StoredViewIntentV1, PlanIntent.
# ---------------------------------------------------------------------------


def _validate_admission_descriptor(value, c, relations):
    errs = []
    spec = c["planIntent"]["admissionDescriptorV1"]
    required = set(spec["required"])
    if not _exact_object(value, required):
        return [("C2I-01", "admissionDescriptor is not the exact closed AdmissionDescriptorV1 shape")]
    if not _descriptor_schema_version_ok(value["schemaVersion"]):
        errs.append(("C2I-02", "AdmissionDescriptor schemaVersion must be the JSON integer 1; "
                               f"got {json_type_name(value['schemaVersion'])} "
                               f"{value['schemaVersion']!r}"))

    release = value["release"]
    if not _exact_object(release, {"manifestId", "capabilityManifestId", "profileId"}):
        errs.append(("C2I-01", "release is not the exact closed shape"))
    elif not SHA256_HEX_RE.fullmatch(str(release["manifestId"])) or \
            not SHA256_HEX_RE.fullmatch(str(release["capabilityManifestId"])) or \
            not _is_identifier(release["profileId"]):
        errs.append(("C2I-02", "release contains a malformed manifest/profile identifier"))
    if value["invocationProfile"] not in spec["invocationProfile"]:
        errs.append(("C2I-02", "invocationProfile is not declared"))

    config = value["resolvedConfiguration"]
    config_paths = []
    if not isinstance(config, list):
        errs.append(("C2I-01", "resolvedConfiguration is not an array"))
        config = []
    for index, entry in enumerate(config):
        fields = {"path", "value", "decidingLayer", "analysisAffecting"}
        if not _exact_object(entry, fields):
            errs.append(("C2I-01", f"resolvedConfiguration[{index}] is not the exact closed shape"))
            continue
        path = entry["path"]
        if not _is_identifier(path, 256):
            errs.append(("C2I-02", f"resolvedConfiguration[{index}].path is malformed"))
        if isinstance(path, str):
            config_paths.append(path)
        if not int_in_range(entry["decidingLayer"], 1, 6):
            errs.append(("C2I-02", f"resolvedConfiguration[{index}].decidingLayer is not a "
                                   "JSON integer inside 1..6"))
        if entry["analysisAffecting"] is not True or not _bounded_parameter_root(entry["value"]):
            errs.append(("C2I-02", f"resolvedConfiguration[{index}] value/analysisAffecting is invalid"))
    if config_paths != sorted(config_paths) or len(config_paths) != len(set(config_paths)):
        errs.append(("C2I-02", "resolvedConfiguration is not uniquely sorted by path"))

    scope = value["scope"]
    if not _exact_object(scope, {"projectId", "workspaceUnitIds", "requestedPaths", "impactExpansion"}):
        errs.append(("C2I-01", "scope is not the exact closed shape"))
        project_id = None
    else:
        project_id = scope["projectId"]
        if not isinstance(project_id, str) or not PROJECT_ID_RE.fullmatch(project_id):
            errs.append(("C2I-02", "scope.projectId is not PROJECT-ID-V1 text"))
        if not _is_sorted_unique_strings(scope["workspaceUnitIds"], nonempty=True, max_items=4096):
            errs.append(("C2I-02", "workspaceUnitIds is not a non-empty sorted identifier set"))
        if not _is_sorted_unique_strings(scope["requestedPaths"], max_items=100000,
                                         validator=_is_relative_path):
            errs.append(("C2I-02", "requestedPaths is not a sorted canonical-relative-path set"))
        if scope["impactExpansion"] not in spec["scope"]["impactExpansion"]:
            errs.append(("C2I-02", "scope.impactExpansion is not declared"))

    change = value["changeSpec"]
    change_fields = {"mode", "baseCommitId", "dirtyOverlayPolicy", "untrackedPolicy", "vcsAdapterId"}
    if not _exact_object(change, change_fields):
        errs.append(("C2I-01", "changeSpec is not the exact closed shape"))
    else:
        if change["mode"] not in spec["changeSpec"]["mode"] or \
                change["dirtyOverlayPolicy"] not in spec["changeSpec"]["dirtyOverlayPolicy"] or \
                change["untrackedPolicy"] not in spec["changeSpec"]["untrackedPolicy"]:
            errs.append(("C2I-02", "changeSpec contains an undeclared enum value"))
        base = change["baseCommitId"]
        if base is not None and (not isinstance(base, str) or not SHA256_HEX_RE.fullmatch(base)):
            errs.append(("C2I-02", "changeSpec.baseCommitId is neither null nor sha256Hex"))
        if not _is_identifier(change["vcsAdapterId"]):
            errs.append(("C2I-02", "changeSpec.vcsAdapterId is malformed"))

    contributions = value["contributions"]
    activation_ids, contribution_authorities = [], set()
    contribution_fields = set(spec["contribution"]["required"])
    if not isinstance(contributions, list):
        errs.append(("C2I-01", "contributions is not an array"))
        contributions = []
    for index, item in enumerate(contributions):
        if not _exact_object(item, contribution_fields):
            errs.append(("C2I-01", f"contribution {index} is not the exact closed shape"))
            continue
        if isinstance(item["activationId"], str):
            activation_ids.append(item["activationId"])
        for field in ("activationId", "contributionId", "bundleId"):
            if not _is_identifier(item[field]):
                errs.append(("C2I-02", f"contribution {index}.{field} is malformed"))
        if not _is_semver(item["contributionVersion"]) or \
                not SHA256_HEX_RE.fullmatch(str(item["artifactDigest"])):
            errs.append(("C2I-02", f"contribution {index} version/digest is malformed"))
        if item["admissionGrant"] not in spec["contribution"]["admissionGrant"] or \
                item["role"] not in spec["contribution"]["role"] or \
                item["verificationState"] not in spec["contribution"]["verificationState"] or \
                item["origin"] not in spec["contribution"]["origin"] or \
                item["authority"] not in spec["contribution"]["authority"]:
            errs.append(("C2I-02", f"contribution {index} contains an undeclared enum value"))
        evidence = item["verificationEvidenceId"]
        if item["verificationState"] == "VERIFIED":
            if not _is_identifier(evidence):
                errs.append(("C2I-02", f"contribution {index} VERIFIED requires verificationEvidenceId"))
        elif evidence is not None:
            errs.append(("C2I-02", f"contribution {index} non-VERIFIED forbids verificationEvidenceId"))
        if not _bounded_parameter_root(item["parameters"], require_map=True):
            errs.append(("C2I-02", f"contribution {index}.parameters violates boundedParameterValue"))
        if isinstance(item["contributionId"], str) and isinstance(item["authority"], str):
            contribution_authorities.add((item["contributionId"], item["authority"]))
    if activation_ids != sorted(activation_ids) or len(activation_ids) != len(set(activation_ids)):
        errs.append(("C2I-02", "contributions are not uniquely sorted by activationId"))

    grants = value["capabilityGrants"]
    grant_fields = set(spec["capabilityGrant"]["required"])
    grant_tuples, grant_ids = [], set()
    if not isinstance(grants, list):
        errs.append(("C2I-01", "capabilityGrants is not an array"))
        grants = []
    for index, item in enumerate(grants):
        if not _exact_object(item, grant_fields):
            errs.append(("C2I-01", f"capabilityGrant {index} is not the exact closed shape"))
            continue
        if not _is_identifier(item["grantId"]) or not _is_semver(item["grantVersion"]) or \
                not isinstance(item["projectId"], str) or not PROJECT_ID_RE.fullmatch(item["projectId"]):
            errs.append(("C2I-02", f"capabilityGrant {index} identifier/version/project is malformed"))
        if item["projectId"] != project_id:
            errs.append(("C2I-02", f"capabilityGrant {index} crosses descriptor projectId"))
        if item["capability"] not in spec["capabilityGrant"]["capability"] or \
                not _bounded_parameter_root(item["parameters"], require_map=True):
            errs.append(("C2I-02", f"capabilityGrant {index} capability/parameters is invalid"))
        if all(isinstance(item[field], str)
               for field in ("grantId", "grantVersion", "projectId")):
            grant_tuples.append((item["grantId"], item["grantVersion"], item["projectId"]))
        if isinstance(item["grantId"], str):
            grant_ids.add(item["grantId"])
    if grant_tuples != sorted(grant_tuples) or len(grant_tuples) != len(set(grant_tuples)) or \
            len(grant_ids) != len(grant_tuples):
        errs.append(("C2I-02", "capabilityGrants are not uniquely sorted by grant tuple/id"))

    workflow = value["workflow"]
    if not _exact_object(workflow, {"stages"}):
        errs.append(("C2I-01", "workflow is not the exact closed shape"))
    else:
        for _, message in validate_plan(workflow, c, relations, grant_ids):
            errs.append(("C2I-03", message))
        stages = workflow.get("stages")
        for stage in stages if isinstance(stages, list) else []:
            if not isinstance(stage, dict):
                continue
            operator = stage.get("operator")
            provider = stage.get("providerId")
            # LB-C2-04: the same unhashable-container failure lived here too.
            if _stage_operator_ok(operator) and \
                    operator in ("semantic-provider", "external-scanner") and \
                    (not isinstance(provider, str) or
                     (provider, operator) not in contribution_authorities):
                errs.append(("C2I-03", f"stage {stage.get('stageId')} has no matching admitted contribution"))

    budgets = value["budgets"]
    if not isinstance(budgets, dict) or not int_in_range(len(budgets), 0, 64):
        errs.append(("C2I-01", "budgets is not a closed map with at most 64 entries"))
    else:
        for key, limit in budgets.items():
            if not isinstance(key, str) or not BUDGET_KEY_RE.fullmatch(key) or \
                    not int_in_range(limit, 1, INT64_MAX):
                errs.append(("C2I-02", f"budget {key!r} has malformed unit-bearing key or limit"))
    return errs


def _validate_stored_view(value, c):
    errs = []
    spec = c["planIntent"]["storedViewIntentV1"]
    if not _exact_object(value, set(spec["required"])):
        return [("C2I-07", "storedView is not the exact closed StoredViewIntentV1 shape")]
    if not isinstance(value["projectId"], str) or not PROJECT_ID_RE.fullmatch(value["projectId"]):
        errs.append(("C2I-07", "storedView.projectId is not PROJECT-ID-V1 text"))
    target = value["target"]
    if not _exact_object(target, {"kind", "runId", "sealedManifestDigest"}):
        errs.append(("C2I-07", "storedView.target is not the exact closed shape"))
    elif target["kind"] != "sealed-run" or \
            not isinstance(target["runId"], str) or not RUN_ID_RE.fullmatch(target["runId"]) or \
            not isinstance(target["sealedManifestDigest"], str) or \
            not SHA256_ID_RE.fullmatch(target["sealedManifestDigest"]):
        errs.append(("C2I-07", "storedView.target contains a malformed kind/RunId/manifest digest"))
    query = value["query"]
    union = spec["query"]["closedTaggedUnion"]
    operation = query.get("operation") if isinstance(query, dict) else None
    # A container operation must not reach a dict lookup (unhashable type).
    branch = union.get(operation) if isinstance(operation, str) else None
    if branch is None or not _exact_object(query, set(branch["exactFields"])):
        errs.append(("C2I-07", "storedView.query is not one exact declared tagged-union branch"))
    elif operation == "read-artifact" and \
            (not isinstance(query["artifactId"], str) or not ARTIFACT_ID_RE.fullmatch(query["artifactId"])):
        errs.append(("C2I-07", "storedView.query artifactId is malformed"))
    elif operation == "read-fact-view" and \
            (not isinstance(query["factViewId"], str) or not FACT_VIEW_ID_RE.fullmatch(query["factViewId"])):
        errs.append(("C2I-07", "storedView.query factViewId is malformed"))
    allowed_results = spec["resultSelectorByOperation"].get(operation, []) \
        if isinstance(operation, str) else []
    if value["resultSelector"] not in allowed_results:
        errs.append(("C2I-07", "storedView.resultSelector is incompatible with query.operation"))
    retention = value["retentionSelector"]
    if not _exact_object(retention, {"requiredState", "onUnavailable"}) or \
            retention.get("requiredState") not in spec["retentionSelector"]["requiredState"] or \
            retention.get("onUnavailable") != spec["retentionSelector"]["onUnavailable"]:
        errs.append(("C2I-07", "storedView.retentionSelector is not the exact declared selector"))
    return errs


def _validate_plan_intent(intent, c, relations):
    errs = []
    intent_spec = c.get("planIntent", {})
    schema = intent_spec.get("schema", {})
    if schema.get("closed") is not True or schema.get("required") != ["schemaVersion", "intentKind"] or \
            set(schema.get("taggedUnion", {})) != {"analysis", "stored-view"}:
        errs.append(("C2I-01", "PlanIntent binding is not the declared closed tagged union"))
    if not isinstance(intent, dict):
        return errs + [("C2I-01", "PlanIntent is not an object")]
    kind = intent.get("intentKind")
    if not isinstance(kind, str):
        return errs + [("C2I-02", "PlanIntent intentKind must be a JSON string, not "
                                  f"{json_type_name(kind)}")]
    branch = schema.get("taggedUnion", {}).get(kind)
    if branch is None:
        return errs + [("C2I-02", "PlanIntent intentKind is not declared")]
    expected = set(branch["exactTopLevelFields"])
    if set(intent) != expected:
        errs.append(("C2I-01", f"PlanIntent {kind} branch is not exact; fields={sorted(intent)}"))
    if not _schema_version_ok(intent.get("schemaVersion")):
        errs.append(("C2I-02", "PlanIntent schemaVersion must be the JSON integer 1; got "
                               f"{json_type_name(intent.get('schemaVersion'))} "
                               f"{intent.get('schemaVersion')!r}"))
    if kind == "stored-view":
        return errs + _validate_stored_view(intent.get("storedView"), c)

    analysis = intent.get("analysis")
    analysis_spec = intent_spec["analysisIntentV1"]
    if not _exact_object(analysis, set(analysis_spec["required"])):
        return errs + [("C2I-01", "analysis is not the exact closed AnalysisIntentV1 shape")]
    for field in ("executionTopology", "workflowIntent", "networkIntent", "remoteComputation"):
        if analysis[field] not in analysis_spec[field]:
            errs.append(("C2I-02", f"analysis.{field} has undeclared value {analysis[field]!r}"))
    repo = analysis["repositoryExecution"]
    repo_spec = analysis_spec["repositoryExecution"]
    if not _exact_object(repo, set(repo_spec["required"])):
        errs.append(("C2I-01", "repositoryExecution is not the exact closed shape"))
    else:
        for field in repo_spec["required"]:
            if repo[field] not in repo_spec["values"]:
                errs.append(("C2I-02", f"repositoryExecution.{field} has undeclared value"))
    errs.extend(_validate_admission_descriptor(analysis["admissionDescriptor"], c, relations))
    return errs


def validate_plan_intent(intent, c, relations):
    """Total parsed-JSON validator: malformed input is data, never an exception."""
    try:
        return _validate_plan_intent(intent, c, relations)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [("C2I-02", f"malformed parsed JSON rejected at validation boundary: "
                           f"{type(exc).__name__}")]


# ---------------------------------------------------------------------------
# Section 6.  Coverage.  LB-C2-02 and LB-C2-03.
# ---------------------------------------------------------------------------


def _validate_coverage(entry, c, fp):
    """Pure Coverage entry -> violations, checked against the live fact-plane."""
    errs = []
    if not _coverage_root_ok(entry):
        return [f"C2X-ROOT: Coverage entry must be a non-empty JSON object, not "
                f"{json_type_name(entry)}"]
    schema = c["coverageKey"].get("entrySchema", {})
    key_fields = {f["field"]: f for f in c["coverageKey"]["key"]}
    if schema.get("closed") is not True:
        errs.append("C2X: the Coverage entry schema is not declared closed")
    for fld in schema.get("required", []):
        if fld not in entry:
            errs.append(f"C2X: Coverage entry missing '{fld}'")
    for fld in entry:
        if fld not in key_fields:
            errs.append(f"C2X: Coverage entry carries unknown field '{fld}' — "
                        "the entry schema is closed")
    for fld, meta in key_fields.items():
        # `relation` is owned end to end by _coverage_relation_findings, so no
        # second overlapping check can mask a regression there.  Every guard in
        # this validator is the SOLE owner of its property; that is what makes
        # each retained source mutation a genuine falsifier rather than one of
        # two redundant tests.
        if fld not in entry or fld == "relation":
            continue
        value = entry[fld]
        wire = meta.get("wireType")
        if wire == "sha256Id":
            if not _subject_scope_shape_ok(value):
                errs.append(f"C2X: Coverage field '{fld}' is not sha256Id text; the field "
                            "exists to make membership and NON-membership checkable, so a "
                            "value that is not a digest defeats it")
            continue
        if wire == "schemaVersionInteger":
            if not _coverage_schema_version_ok(value):
                errs.append(f"C2X: Coverage field '{fld}' must be the JSON integer 1, not "
                            f"{json_type_name(value)} {value!r}")
            continue
        want = meta.get("jsonType")
        if want == "string" and not isinstance(value, str):
            errs.append(f"C2X: Coverage field '{fld}' must be a JSON string, not "
                        f"{json_type_name(value)}")
        elif want == "integer" and not is_wire_int(value):
            errs.append(f"C2X: Coverage field '{fld}' must be a JSON integer, not "
                        f"{json_type_name(value)}")
    errs.extend(_coverage_relation_findings(entry, c, fp))
    return errs


def _coverage_relation_findings(entry, c, fp):
    """LB-C2-02, sole owner of the relation field.

    v3 wrote `rel = entry.get("relation")` then `if fp and rel:`, so the declared
    C2X registry lookup was SKIPPED for all six falsy JSON values - null, 0,
    false, the empty string, the empty array and the empty object - and an entry
    naming no relation at all was C-2-conformant.  The lookup is now driven by
    TYPE.  Truthiness never gates it.
    """
    errs = []
    rel = entry.get("relation")
    if fp is None:
        return [f"C2X: could not load {FP} — relation constraints unverified"]
    if not _coverage_relation_is_checkable(rel):
        return [f"C2X: relation must be a JSON string checked against the fact-plane "
                f"registry, not {json_type_name(rel)}; truthiness never gates the "
                f"registry lookup"]
    rels = fp["relationRegistry"]["relations"]
    if rel not in rels:
        errs.append(f"C2X: relation '{rel}' is not in the fact-plane registry")
    else:
        resolution = entry.get("resolution")
        if not isinstance(resolution, str) or resolution not in rels[rel]["ladder"]:
            errs.append(f"C2X: resolution {resolution!r} is not a rung of "
                        f"'{rel}' — ladders are per-relation")
    if rel in c["coverageKey"]["crossUniverseRelations"] and "targetUniverseId" not in entry:
        errs.append(f"C2X: cross-universe relation '{rel}' has no targetUniverseId — "
                    f"source-complete would masquerade as target-complete")
    return errs


def validate_coverage(entry, c, fp):
    """Total Coverage validator.  LB-C2-02: v3 raised on seven hostile roots."""
    try:
        return _validate_coverage(entry, c, fp)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"C2X: malformed parsed JSON rejected at the Coverage validation "
                f"boundary: {type(exc).__name__}"]


# ---------------------------------------------------------------------------
# Section 7.  Fixture expansion and the immutable intent bindings.
#
# LB-C2-05: v3 named planId, snapshotId and executionId, declared no wire type
# for any of them, shipped the placeholders plan-1 / snap-1 / exec-1 in both the
# contract and the checker, and accepted every JSON type at
# executionPlan.planId and attemptRecord.executionId.  The default envelopes
# below are DERIVED from the pinned resolved-inputs.v2.json golden vectors, so
# the positive vector exercises the grammar it declares.
# ---------------------------------------------------------------------------


def canonical_identifiers(ri):
    """The three envelope identifiers, taken from the owning artifact."""
    if not isinstance(ri, dict):
        return {}
    try:
        return {
            "planId": ri["planIdContract"]["goldenVectors"]["positive"][0]["expectedPlanId"],
            "snapshotId": ri["snapshotIdContract"]["goldenVectors"]["positive"][0]["expectedSnapshotId"],
            "executionId": ri["planIdContract"]["goldenVectors"]["negative"][2]["addTopLevel"]["executionId"],
            "planIdPattern": ri["planIdContract"]["identityRepresentation"]["regex"],
            "snapshotIdPattern": ri["snapshotIdContract"]["identityRepresentation"]["regex"],
        }
    except MALFORMED_SHAPE_EXCEPTIONS:
        return {}


def _intent_fixture_values(c):
    """Expand concrete/base+mutation PlanIntent fixtures."""
    values = {}
    findings = []
    for fx in c.get("planIntentFixtures", []):
        if "intent" in fx:
            values[fx["id"]] = copy.deepcopy(fx["intent"])
            continue
        base_id = fx.get("baseFixtureId")
        if base_id not in values:
            findings.append(f"I1 {fx.get('id')}: base fixture {base_id!r} is unavailable "
                            "or forward-referenced")
            continue
        try:
            values[fx["id"]] = _pointer_mutate(values[base_id], fx["mutation"])
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append(f"I1 {fx.get('id')}: fixture mutation failed: {exc}")
    return values, findings


def _analysis_descriptor(intent):
    return intent["analysis"]["admissionDescriptor"]


def _stored_payload(intent):
    return intent["storedView"]


def _replace_binding_sentinels(value, intent, commitment):
    descriptor = _analysis_descriptor(intent) if intent.get("intentKind") == "analysis" else None
    stored = _stored_payload(intent) if intent.get("intentKind") == "stored-view" else None
    sentinels = {
        "$BASE_COMMITMENT": commitment,
        "$BASE_INTENT": intent,
        "$BASE_ADMISSION_DESCRIPTOR": descriptor,
        "$BASE_PROJECT_ID": descriptor["scope"]["projectId"] if descriptor else stored["projectId"],
        "$BASE_RELEASE": descriptor["release"] if descriptor else None,
        "$BASE_INVOCATION_PROFILE": descriptor["invocationProfile"] if descriptor else None,
        "$BASE_RESOLVED_CONFIGURATION": descriptor["resolvedConfiguration"] if descriptor else None,
        "$BASE_SCOPE": descriptor["scope"] if descriptor else None,
        "$BASE_CHANGE_SPEC": descriptor["changeSpec"] if descriptor else None,
        "$BASE_CONTRIBUTIONS": descriptor["contributions"] if descriptor else None,
        "$BASE_CAPABILITY_GRANTS": descriptor["capabilityGrants"] if descriptor else None,
        "$BASE_WORKFLOW": descriptor["workflow"] if descriptor else None,
        "$BASE_BUDGETS": descriptor["budgets"] if descriptor else None,
        "$BASE_STAGE_INTENTS": descriptor["workflow"]["stages"] if descriptor else None,
        "$BASE_STORED_TARGET": stored["target"] if stored else None,
        "$BASE_STORED_QUERY": stored["query"] if stored else None,
        "$BASE_RESULT_SELECTOR": stored["resultSelector"] if stored else None,
        "$BASE_RETENTION_SELECTOR": stored["retentionSelector"] if stored else None,
    }
    if isinstance(value, str) and value in sentinels:
        return copy.deepcopy(sentinels[value])
    if isinstance(value, list):
        return [_replace_binding_sentinels(x, intent, commitment) for x in value]
    if isinstance(value, dict):
        return {k: _replace_binding_sentinels(v, intent, commitment)
                for k, v in value.items()}
    return value


def _default_attempt(intent, commitment, ids):
    descriptor = _analysis_descriptor(intent)
    return {
        "executionId": ids.get("executionId"),
        "admittedPlanIntent": copy.deepcopy(intent),
        "admissionDescriptor": copy.deepcopy(descriptor),
        "planIntentCommitment": commitment,
    }


def _default_execution_plan(intent, commitment, ids):
    descriptor = _analysis_descriptor(intent)
    inputs = {
        "snapshotId": ids.get("snapshotId"),
        "planSchemaMajor": 1,
        "release": copy.deepcopy(descriptor["release"]),
        "invocationProfile": descriptor["invocationProfile"],
        "resolvedConfiguration": copy.deepcopy(descriptor["resolvedConfiguration"]),
        "scope": copy.deepcopy(descriptor["scope"]),
        "changeSpec": copy.deepcopy(descriptor["changeSpec"]),
        "contributions": copy.deepcopy(descriptor["contributions"]),
        "semanticUniverses": [],
        "capabilityGrants": copy.deepcopy(descriptor["capabilityGrants"]),
        "workflow": copy.deepcopy(descriptor["workflow"]),
        "budgets": copy.deepcopy(descriptor["budgets"]),
        "planIntentCommitment": commitment,
    }
    return {
        "snapshotId": ids.get("snapshotId"),
        "planId": ids.get("planId"),
        "projectId": descriptor["scope"]["projectId"],
        "planIntentCommitment": commitment,
        "planIdentityInputs": inputs,
        "stages": copy.deepcopy(descriptor["workflow"]["stages"]),
    }


def _validate_intent_binding(fx, base_intent, c, relations, ids):
    if base_intent.get("intentKind") != "analysis":
        return [("C2I-06", "analysis binding fixture does not use an analysis PlanIntent")]
    commitment, encode_errs = plan_intent_commitment_total(base_intent, c)
    if encode_errs:
        return encode_errs
    attempt = _replace_binding_sentinels(
        copy.deepcopy(fx.get("attemptRecord", _default_attempt(base_intent, commitment, ids))),
        base_intent, commitment)
    plan = _replace_binding_sentinels(
        copy.deepcopy(fx.get("executionPlan",
                             _default_execution_plan(base_intent, commitment, ids))),
        base_intent, commitment)
    candidate_intent = copy.deepcopy(base_intent)
    try:
        if fx.get("candidateIntentMutation"):
            candidate_intent = _pointer_mutate(candidate_intent, fx["candidateIntentMutation"])
        if fx.get("attemptRecordMutation"):
            attempt = _pointer_mutate(attempt, fx["attemptRecordMutation"])
        if fx.get("executionPlanMutation"):
            plan = _pointer_mutate(plan, fx["executionPlanMutation"])
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [("C2I-06", f"binding fixture mutation failed: {exc}")]

    errs = []
    attempt_required = set(c["planIntent"]["attemptAndExecutionJoin"]["attemptRecordRequired"])
    if not isinstance(attempt, dict) or set(attempt) != attempt_required:
        if not isinstance(attempt, dict) or "planIntentCommitment" not in attempt:
            errs.append(("C2I-05", "AttemptRecord lacks planIntentCommitment"))
        errs.append(("C2I-06", "AttemptRecord is not the exact closed intent-bound envelope"))
    # LB-C2-05: the ExecutionId value itself, not merely the field's presence.
    execution_id = attempt.get("executionId") if isinstance(attempt, dict) else None
    if not isinstance(execution_id, str) or not EXECUTION_ID_RE.fullmatch(execution_id):
        errs.append(("C2I-06", "AttemptRecord.executionId is not EXECUTION-ID-V1 text "
                               f"(got {json_type_name(execution_id)} {execution_id!r})"))
    required_plan = set(c["executionPlan"].get("requiredFields", []))
    if not isinstance(plan, dict) or c["executionPlan"].get("closedTopLevel") is not True or \
            set(plan) != required_plan:
        return errs + [("C2I-06", "ExecutionPlan is not the exact closed intent-bound envelope")]

    plan_id = plan.get("planId")
    if not isinstance(plan_id, str) or not PLAN_ID_RE.fullmatch(plan_id):
        errs.append(("C2I-06", "ExecutionPlan.planId is not PLAN-ID-V1 text "
                               f"(got {json_type_name(plan_id)} {plan_id!r})"))
    snapshot_id = plan.get("snapshotId")
    if not isinstance(snapshot_id, str) or not SNAPSHOT_ID_RE.fullmatch(snapshot_id):
        errs.append(("C2I-06", "ExecutionPlan.snapshotId is not SNAPSHOT-ID-V1 text "
                               f"(got {json_type_name(snapshot_id)} {snapshot_id!r})"))

    descriptor = _analysis_descriptor(base_intent)
    candidate_commitment, candidate_errs = plan_intent_commitment_total(candidate_intent, c)
    errs.extend(candidate_errs)
    inputs = plan.get("planIdentityInputs")
    inputs_required = set(c["planIntent"]["attemptAndExecutionJoin"]["planIdentityInputsRequired"])
    if not isinstance(inputs, dict) or set(inputs) != inputs_required:
        errs.append(("C2I-06", "planIdentityInputs is not the exact 13-field PlanDescriptor"))
        inputs = {}

    commitment_values = [
        attempt.get("planIntentCommitment") if isinstance(attempt, dict) else None,
        plan.get("planIntentCommitment"),
        inputs.get("planIntentCommitment"),
    ]
    if any(value != commitment for value in commitment_values) or candidate_commitment != commitment:
        errs.append(("C2I-06", "PlanIntent commitment differs across candidate, AttemptRecord, "
                               "ExecutionPlan or PlanId input"))
    if not isinstance(attempt, dict) or attempt.get("admittedPlanIntent") != base_intent:
        errs.append(("C2I-06", "AttemptRecord.admittedPlanIntent differs from frozen admitted PlanIntent"))
    if not isinstance(attempt, dict) or attempt.get("admissionDescriptor") != descriptor:
        errs.append(("C2I-06", "AttemptRecord.admissionDescriptor differs from admitted subobject"))

    mapping = ("release", "invocationProfile", "resolvedConfiguration", "scope",
               "changeSpec", "contributions", "capabilityGrants", "workflow", "budgets")
    for field in mapping:
        if inputs.get(field) != descriptor[field]:
            errs.append(("C2I-06", f"planIdentityInputs.{field} differs from admitted descriptor"))
    # LB-C2-01, third site: v3 guarded planSchemaMajor with a bare inequality too.
    if inputs.get("snapshotId") != plan.get("snapshotId") or \
            not _plan_schema_major_ok(inputs.get("planSchemaMajor")) or \
            not isinstance(inputs.get("semanticUniverses"), list):
        errs.append(("C2I-06", "post-admission PlanDescriptor fields are malformed or "
                               "inconsistent (planSchemaMajor must be the JSON integer 1)"))
    if plan.get("projectId") != descriptor["scope"]["projectId"]:
        errs.append(("C2I-06", "ExecutionPlan.projectId differs from admitted scope.projectId"))
    if plan.get("stages") != descriptor["workflow"]["stages"]:
        errs.append(("C2I-06", "ExecutionPlan.stages differs from admitted workflow.stages"))
    grant_ids = {grant["grantId"] for grant in descriptor["capabilityGrants"]}
    for _, message in validate_plan({"stages": plan.get("stages")}, c, relations, grant_ids):
        errs.append(("C2I-03", message))
    return errs


def validate_intent_binding(fx, base_intent, c, relations, ids):
    """Total analysis-binding validator."""
    try:
        return _validate_intent_binding(fx, base_intent, c, relations, ids)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [("C2I-06", "malformed parsed JSON rejected at the intent-binding "
                           f"validation boundary: {type(exc).__name__}")]


def _default_stored_binding(intent, commitment):
    stored = _stored_payload(intent)
    request_id = "req1_00000000000000000000000000000001"
    request = {
        "requestId": request_id,
        "admittedPlanIntent": copy.deepcopy(intent),
        "planIntentCommitment": commitment,
    }
    prepared = {
        "requestId": request_id,
        "planIntentCommitment": commitment,
        "projectId": stored["projectId"],
        "target": copy.deepcopy(stored["target"]),
        "query": copy.deepcopy(stored["query"]),
        "resultSelector": stored["resultSelector"],
        "retentionSelector": copy.deepcopy(stored["retentionSelector"]),
    }
    return request, prepared


def _validate_stored_view_binding(fx, base_intent, c):
    if base_intent.get("intentKind") != "stored-view":
        return [("C2I-08", "stored binding fixture does not use a stored-view PlanIntent")]
    commitment, encode_errs = plan_intent_commitment_total(base_intent, c)
    if encode_errs:
        return encode_errs
    default_request, default_prepared = _default_stored_binding(base_intent, commitment)
    request = _replace_binding_sentinels(
        copy.deepcopy(fx.get("requestContext", default_request)), base_intent, commitment)
    prepared = _replace_binding_sentinels(
        copy.deepcopy(fx.get("preparedStoredRead", default_prepared)), base_intent, commitment)
    try:
        if fx.get("requestContextMutation"):
            request = _pointer_mutate(request, fx["requestContextMutation"])
        if fx.get("preparedStoredReadMutation"):
            prepared = _pointer_mutate(prepared, fx["preparedStoredReadMutation"])
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [("C2I-08", f"stored binding fixture mutation failed: {exc}")]

    errs = []
    request_fields = set(c["planIntent"]["storedViewJoin"]["requestContextRequired"])
    prepared_fields = set(c["planIntent"]["storedViewJoin"]["preparedStoredReadRequired"])
    if not _exact_object(request, request_fields):
        errs.append(("C2I-08", "RequestContext is not the exact closed stored-read envelope"))
    if not _exact_object(prepared, prepared_fields):
        errs.append(("C2I-08", "PreparedStoredRead is not the exact closed stored-read envelope"))
    request_id = request.get("requestId") if isinstance(request, dict) else None
    prepared_request_id = prepared.get("requestId") if isinstance(prepared, dict) else None
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id) or \
            not isinstance(prepared_request_id, str) or \
            not REQUEST_ID_RE.fullmatch(prepared_request_id):
        errs.append(("C2I-09", "stored-read envelopes require canonical REQUEST-ID-V1 text"))
    if fx.get("requestIdAuthority", "host-minted-reserved") != "host-minted-reserved":
        errs.append(("C2I-09", "stored-read RequestId was not host-minted and reserved at ingress"))
    stored = _stored_payload(base_intent)
    if not isinstance(request, dict) or request.get("admittedPlanIntent") != base_intent or \
            request.get("planIntentCommitment") != commitment:
        errs.append(("C2I-08", "RequestContext differs from frozen stored-view intent/commitment"))
    if not isinstance(prepared, dict) or prepared_request_id != request_id or \
            prepared.get("planIntentCommitment") != commitment:
        errs.append(("C2I-08", "PreparedStoredRead request/commitment differs from RequestContext"))
    for field in ("projectId", "target", "query", "resultSelector", "retentionSelector"):
        if not isinstance(prepared, dict) or prepared.get(field) != stored[field]:
            errs.append(("C2I-08", f"PreparedStoredRead.{field} differs from admitted "
                                   "stored-view request"))
    return errs


def validate_stored_view_binding(fx, base_intent, c):
    """Total stored-view-binding validator."""
    try:
        return _validate_stored_view_binding(fx, base_intent, c)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [("C2I-08", "malformed parsed JSON rejected at the stored-view-binding "
                           f"validation boundary: {type(exc).__name__}")]


# ---------------------------------------------------------------------------
# Section 8.  Self-scans over this checker's own abstract syntax tree.
#
# LB-C2-01 was not one typo, it was a CLASS.  Repairing the two sites the review
# named would have left the class open: sweeping the tree found two more.  These
# scans run on every invocation, so a fifth site is REPORTED rather than missed,
# and the selftest proves each scan is load-bearing by breaking the property in
# a copy of this file's own tree and requiring the scan to say so.
# ---------------------------------------------------------------------------

GUARD_HELPERS = (
    "is_wire_int", "exact_int", "int_in_range", "_schema_version_ok",
    "_descriptor_schema_version_ok", "_plan_schema_major_ok",
    "_coverage_schema_version_ok",
)
INTEGER_SCAN_ENTRYPOINTS = (
    "check", "_check", "validate_plan_intent", "_validate_plan_intent",
    "_validate_admission_descriptor", "_validate_stored_view", "validate_plan",
    "_validate_plan", "validate_coverage", "_validate_coverage",
    "validate_intent_binding", "_validate_intent_binding",
    "validate_stored_view_binding", "_validate_stored_view_binding",
    "canonical_plan_intent", "plan_intent_commitment",
    "plan_intent_commitment_total", "_intent_fixture_values",
)
TOTAL_BOUNDARIES = {
    "validate_plan": "_validate_plan",
    "validate_plan_intent": "_validate_plan_intent",
    "validate_coverage": "_validate_coverage",
    "validate_intent_binding": "_validate_intent_binding",
    "validate_stored_view_binding": "_validate_stored_view_binding",
    "plan_intent_commitment_total": "plan_intent_commitment",
    "check": "_check",
}
_OWN_TREE_CACHE = None
# A scan of this file's own tree is a pure function of that tree, and the tree
# does not change during a run.  The contract-root hostile matrix drives check()
# tens of thousands of times, so the unmutated results are memoised; a scan of a
# SUPPLIED tree (the source-mutation battery) is never cached.
_SCAN_CACHE: dict[str, object] = {}


def _own_tree():
    global _OWN_TREE_CACHE
    if _OWN_TREE_CACHE is None:
        _OWN_TREE_CACHE = ast.parse(pathlib.Path(__file__).resolve().read_bytes())
    return _OWN_TREE_CACHE


def _module_functions(tree):
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


def _reachable(functions, entrypoints):
    reached, frontier = set(), [n for n in entrypoints if n in functions]
    while frontier:
        name = frontier.pop()
        if name in reached:
            continue
        reached.add(name)
        for child in ast.walk(functions[name]):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and \
                    child.func.id in functions and child.func.id not in reached:
                frontier.append(child.func.id)
    return reached


def _is_wire_expression(node, tainted):
    """A value that came off the wire: a subscript, a .get(), or a name bound to one."""
    if isinstance(node, ast.Subscript):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and \
            node.func.attr == "get":
        return True
    return isinstance(node, ast.Name) and node.id in tainted


def _tainted_names(function):
    tainted = {arg.arg for arg in function.args.args}
    tainted |= {arg.arg for arg in function.args.kwonlyargs}
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                isinstance(node.targets[0], ast.Name) and \
                _is_wire_expression(node.value, tainted):
            tainted.add(node.targets[0].id)
    return tainted


def _numeric_literal(node):
    return isinstance(node, ast.Constant) and \
        isinstance(node.value, (int, float)) and not isinstance(node.value, bool)


def integer_guard_scan(tree=None):
    """Every wire-sourced numeric test must route through a declared guard.

    This is the systemic half of the LB-C2-01 repair.  A bare `!= 1` against a
    parsed-JSON value silently admits JSON true and JSON 1.0; the fix is a type
    guard, and the fix STAYS fixed only if the pattern itself is refused.
    """
    if tree is None and 'integer_guard_scan' in _SCAN_CACHE:
        return _SCAN_CACHE['integer_guard_scan']
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    reached = _reachable(functions, INTEGER_SCAN_ENTRYPOINTS) - set(GUARD_HELPERS)
    missing = [name for name in INTEGER_SCAN_ENTRYPOINTS if name not in functions]
    unguarded, helper_sites = [], 0
    for name in sorted(reached):
        function = functions[name]
        tainted = _tainted_names(function)
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                    node.func.id in GUARD_HELPERS:
                helper_sites += 1
            if not isinstance(node, ast.Compare):
                continue
            operands = [node.left] + list(node.comparators)
            for index, op in enumerate(node.ops):
                if isinstance(op, (ast.Is, ast.IsNot, ast.In, ast.NotIn)):
                    continue
                left, right = operands[index], operands[index + 1]
                for a, b in ((left, right), (right, left)):
                    if _numeric_literal(b) and _is_wire_expression(a, tainted):
                        unguarded.append(f"{name} line {getattr(node, 'lineno', 0)}: "
                                         f"{ast.unparse(node)}")
    result = {
        "scannedFunctions": len(reached),
        "guardHelperCallSites": helper_sites,
        "unguardedNumericComparisons": len(unguarded),
        "unguarded": sorted(set(unguarded)),
        "missingEntrypoints": missing,
    }
    if tree is None:
        _SCAN_CACHE['integer_guard_scan'] = result
    return result


def _handles_malformed(handler):
    declared = handler.type
    if declared is None:
        return True
    nodes = declared.elts if isinstance(declared, ast.Tuple) else [declared]
    return any(isinstance(n, ast.Name) and
               n.id in ("MALFORMED_SHAPE_EXCEPTIONS", "Exception", "BaseException")
               for n in nodes)


def _calls_inside_guard(node, target, protected, sites):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
            node.func.id == target:
        sites.append(protected)
    if isinstance(node, ast.Try):
        guarded = protected or any(_handles_malformed(h) for h in node.handlers)
        for child in node.body:
            _calls_inside_guard(child, target, guarded, sites)
        for handler in node.handlers:
            for child in handler.body:
                _calls_inside_guard(child, target, protected, sites)
        for child in list(node.orelse) + list(node.finalbody):
            _calls_inside_guard(child, target, protected, sites)
        return
    for child in ast.iter_child_nodes(node):
        _calls_inside_guard(child, target, protected, sites)


def total_boundary_scan(tree=None):
    """Every public validator must convert a missed traversal into a finding.

    LB-C2-02 and LB-C2-04: v3's validate_coverage and validate_plan carried no
    boundary at all, so hostile parsed JSON reached the caller as a traceback.
    """
    if tree is None and 'total_boundary_scan' in _SCAN_CACHE:
        return _SCAN_CACHE['total_boundary_scan']
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    guarded, unguarded, missing = 0, [], []
    for public, inner in sorted(TOTAL_BOUNDARIES.items()):
        if public not in functions or inner not in functions:
            missing.append(public)
            continue
        sites = []
        for child in ast.iter_child_nodes(functions[public]):
            _calls_inside_guard(child, inner, False, sites)
        if not sites:
            missing.append(public)
            continue
        for protected in sites:
            if protected:
                guarded += 1
            else:
                unguarded.append(f"{public} -> {inner}")
    result = {
        "declaredBoundaries": len(TOTAL_BOUNDARIES),
        "guardedDispatches": guarded,
        "unguardedDispatches": len(unguarded),
        "unguarded": sorted(set(unguarded)),
        "missing": sorted(set(missing)),
    }
    if tree is None:
        _SCAN_CACHE['total_boundary_scan'] = result
    return result


def selftest_reachability_scan(tree=None):
    """The --selftest path must be live, singular and flag-guarded."""
    if tree is None and 'selftest_reachability_scan' in _SCAN_CACHE:
        return _SCAN_CACHE['selftest_reachability_scan']
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    flags = set()
    for node in ast.walk(subject):
        if isinstance(node, ast.Compare):
            for child in ast.walk(node):
                if isinstance(child, ast.Constant) and isinstance(child.value, str) \
                        and child.value.startswith("--"):
                    flags.add(child.value)
    for node in subject.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "DECLARED_FLAGS" for t in node.targets):
            flags.update(child.value for child in ast.walk(node.value)
                         if isinstance(child, ast.Constant) and isinstance(child.value, str))
    dispatches, guarded_dispatches = 0, 0

    def visit(node, inside, guard):
        nonlocal dispatches, guarded_dispatches
        if isinstance(node, ast.FunctionDef) and node.name == "selftest":
            inside = True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                node.func.id == "selftest" and not inside:
            dispatches += 1
            if guard is not None:
                guarded_dispatches += 1
        if isinstance(node, ast.If):
            literals = {child.value for child in ast.walk(node.test)
                        if isinstance(child, ast.Constant) and isinstance(child.value, str)}
            declared = literals & set(DECLARED_FLAGS)
            for child in node.body:
                visit(child, inside, sorted(declared)[0] if declared else guard)
            for child in node.orelse:
                visit(child, inside, guard)
            return
        for child in ast.iter_child_nodes(node):
            visit(child, inside, guard)

    visit(subject, False, None)
    main_fn = functions.get("main")
    dispatch_index = findings_index = None
    if main_fn is not None:
        for index, statement in enumerate(main_fn.body):
            text = ast.dump(statement)
            if dispatch_index is None and "Name(id='selftest'" in text:
                dispatch_index = index
            if findings_index is None and "Name(id='findings'" in text and "Return(" in text:
                findings_index = index
    result = {
        "hasSingleMain": main_fn is not None and
                         sum(1 for n in subject.body
                             if isinstance(n, ast.FunctionDef) and n.name == "main") == 1,
        "flags": sorted(flags),
        "dispatchCount": dispatches,
        "guardedDispatchCount": guarded_dispatches,
        "dispatchBeforeFindingsReturn": dispatch_index is not None and
                                        (findings_index is None or dispatch_index < findings_index),
    }
    if tree is None:
        _SCAN_CACHE['selftest_reachability_scan'] = result
    return result


def _scan_findings():
    findings = []
    integers = integer_guard_scan()
    for site in integers["unguarded"]:
        findings.append("LB-C2-01 CLASS: a wire-sourced value is compared to a numeric "
                        f"literal outside the declared guard helpers: {site}")
    if integers["missingEntrypoints"]:
        findings.append("the integer-guard scan cannot find validator entrypoint "
                        f"{integers['missingEntrypoints'][0]}")
    if not int_in_range(integers["guardHelperCallSites"], 8, 10 ** 6):
        findings.append(f"the integer-guard scan found only "
                        f"{integers['guardHelperCallSites']} guard-helper call site(s), so "
                        "it cannot be distinguished from a vacuous scan")
    boundaries = total_boundary_scan()
    for site in boundaries["unguarded"]:
        findings.append("a public validator dispatches to its implementation outside a "
                        f"named-finding boundary: {site}")
    for name in boundaries["missing"]:
        findings.append(f"public validator {name} has no named-finding boundary at all")
    reach = selftest_reachability_scan()
    if not reach["hasSingleMain"]:
        findings.append("this checker does not define exactly one main()")
    if reach["flags"] != sorted(DECLARED_FLAGS):
        findings.append(f"this checker carries command flag literals {reach['flags']}, "
                        f"which is not the declared entrypoint set {sorted(DECLARED_FLAGS)}")
    if not exact_int(reach["dispatchCount"], 1) or \
            reach["guardedDispatchCount"] != reach["dispatchCount"]:
        findings.append(f"main() dispatches to selftest() {reach['dispatchCount']} time(s), "
                        f"{reach['guardedDispatchCount']} of them flag-guarded; exactly one "
                        "flag-guarded dispatch is permitted")
    if not reach["dispatchBeforeFindingsReturn"]:
        findings.append("main() can return on findings before reaching the selftest suite")
    return findings


# ---------------------------------------------------------------------------
# Section 9.  Leaf-inclusive hostile enumeration.
#
# The enumeration is the whole value: the root, every object key and every array
# index at unlimited depth, CONTAINER AND SCALAR LEAF alike.  v3's retained
# corpus reached four collection-adjacent scalars and was GUARDED to stay that
# size, so the instrument could not observe the region its claim quantified
# over.  Every count below is measured live and compared to the candidate's
# published measurement.
# ---------------------------------------------------------------------------

CONTRACT_HOSTILE_VALUES = (
    ("null", None), ("integer", 0), ("float", 1.0), ("boolean", True),
    ("string", "hostile"), ("array", []), ("object", {}),
)


def enumerate_positions(base, leaves=True):
    positions = [("", base)]

    def walk(value, prefix):
        if isinstance(value, dict):
            children = [(f"{prefix}.{key}" if prefix else str(key), value[key])
                        for key in value]
        elif isinstance(value, list):
            children = [(f"{prefix}[{index}]", item) for index, item in enumerate(value)]
        else:
            return
        for child_path, child in children:
            container = isinstance(child, (dict, list))
            if container or leaves:
                positions.append((child_path, child))
            if container:
                walk(child, child_path)

    walk(base, "")
    return positions


_STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")


def _path_steps(path):
    steps = []
    for index, name in _STEP_RE.findall(path):
        steps.append(int(index) if index else name)
    return steps


def _resolve(root, path):
    node = root
    for step in _path_steps(path):
        node = node[step]
    return node


def _assign(root, path, value):
    steps = _path_steps(path)
    node = root
    for step in steps[:-1]:
        node = node[step]
    node[steps[-1]] = value


def _round_trips(base, path, value):
    if path == "":
        return True
    try:
        return _resolve(base, path) is value
    except MALFORMED_SHAPE_EXCEPTIONS:
        return False


def _same_leaf(left, right):
    return type(left) is type(right) and left == right


def node_census(base, values, leaves=True):
    containers = scalars = dicts = not_round_tripping = no_ops = 0
    counted = set()
    for path, value in enumerate_positions(base, leaves):
        if path in counted:
            continue
        if not _round_trips(base, path, value):
            not_round_tripping += 1
            continue
        counted.add(path)
        if isinstance(value, dict):
            dicts += 1
            containers += 1
        elif isinstance(value, list):
            containers += 1
        else:
            scalars += 1
        for _label, injected in values:
            if path != "" and _same_leaf(value, injected):
                no_ops += 1
    paths = len(counted)
    enumerated = paths * len(values) + dicts
    return {
        "enumeratedPaths": paths,
        "containerPaths": containers,
        "scalarLeafPaths": scalars,
        "dictPaths": dicts,
        "pathsNotRoundTripping": not_round_tripping,
        "injectionValues": len(values),
        "enumeratedCases": enumerated,
        "noOpInjections": no_ops,
        "executedCases": enumerated - no_ops,
    }


def merge_census(left, right):
    return {key: left.get(key, 0) + right.get(key, 0) for key in
            ("enumeratedPaths", "containerPaths", "scalarLeafPaths", "dictPaths",
             "pathsNotRoundTripping", "enumeratedCases", "noOpInjections",
             "executedCases")}


def hostile_cases(base, values, leaves=True):
    """Yield (path, label, mutated-copy) for every non-no-op injection."""
    counted = set()
    for path, value in enumerate_positions(base, leaves):
        if path in counted or not _round_trips(base, path, value):
            continue
        counted.add(path)
        injections = list(values)
        if isinstance(value, dict):
            injections.append(("unknown-key", "<insert>"))
        for label, injected in injections:
            if label != "unknown-key" and path != "" and _same_leaf(value, injected):
                continue
            if path == "":
                if label == "unknown-key":
                    candidate = copy.deepcopy(base)
                    if isinstance(candidate, dict):
                        candidate["c2v4UnknownRootKey"] = 1
                else:
                    candidate = copy.deepcopy(injected)
            else:
                candidate = copy.deepcopy(base)
                try:
                    if label == "unknown-key":
                        node = _resolve(candidate, path)
                        if not isinstance(node, dict):
                            continue
                        node["c2v4UnknownNestedKey"] = 1
                    else:
                        _assign(candidate, path, copy.deepcopy(injected))
                except MALFORMED_SHAPE_EXCEPTIONS:
                    continue
            yield path, label, candidate


def drive_surface(bases, values, unguarded, guarded, extra=None, leaves=True):
    """Run one leaf-inclusive hostile matrix and return (census, statistics)."""
    census = {}
    stats = {"executedCases": 0, "unguardedEscapes": 0, "guardedEscapes": 0,
             "silentAccepts": 0, "admitThenRaise": 0,
             "typeDistinctConstantAdmissions": 0}
    for base in bases:
        census = merge_census(census, node_census(base, values, leaves))
        for path, label, candidate in hostile_cases(base, values, leaves):
            stats["executedCases"] += 1
            try:
                unguarded(candidate)
            except BaseException:                       # noqa: BLE001 - measured
                stats["unguardedEscapes"] += 1
            try:
                findings = guarded(candidate)
            except BaseException:                       # noqa: BLE001 - measured
                stats["guardedEscapes"] += 1
                findings = ["guarded boundary raised"]
            if not findings:
                stats["silentAccepts"] += 1
            if extra is not None:
                extra(stats, path, label, candidate, findings)
    return census, stats


CONSTANT_LEAF_PATHS = ("schemaVersion", "analysis.admissionDescriptor.schemaVersion")


def measure_surfaces(c, relations, fp, values, intent_values):
    """Every fixture-backed surface, enumerated at scalar leaves and executed."""
    surfaces = {}
    valid_intents = [intent_values[fx["id"]] for fx in c.get("planIntentFixtures", [])
                     if fx.get("valid") and fx.get("id") in intent_values]

    def intent_extra(stats, path, _label, candidate, findings):
        if findings:
            return
        _commitment, encode_errs = plan_intent_commitment_total(candidate, c)
        if encode_errs:
            stats["admitThenRaise"] += 1
        if path in CONSTANT_LEAF_PATHS:
            stats["typeDistinctConstantAdmissions"] += 1

    census, stats = drive_surface(
        valid_intents, values,
        lambda x: _validate_plan_intent(x, c, relations),
        lambda x: validate_plan_intent(x, c, relations),
        intent_extra)
    surfaces["plan-intent"] = {"census": census, "stats": stats}

    valid_coverage = [fx["entry"] for fx in c.get("coverageFixtures", []) if fx.get("valid")]
    census, stats = drive_surface(
        valid_coverage, values,
        lambda x: _validate_coverage(x, c, fp),
        lambda x: validate_coverage(x, c, fp))
    surfaces["coverage"] = {"census": census, "stats": stats}

    valid_plans = [fx["plan"] for fx in c.get("planFixtures", []) if fx.get("valid")]
    census, stats = drive_surface(
        valid_plans, values,
        lambda x: _validate_plan(x, c, relations),
        lambda x: validate_plan(x, c, relations))
    surfaces["stage-plan"] = {"census": census, "stats": stats}
    return surfaces


def measure_contract_root(c, authority, execute):
    """The candidate document itself, driven through the total check() boundary."""
    census = node_census(c, CONTRACT_HOSTILE_VALUES)
    stats = {"executedCases": 0, "unguardedEscapes": 0, "guardedEscapes": 0,
             "guardedExercised": 0, "executed": execute}
    if not execute:
        return census, stats
    saved = authority.census_enabled
    authority.census_enabled = False
    try:
        seen_paths = set()
        for path, _label, candidate in hostile_cases(c, CONTRACT_HOSTILE_VALUES):
            stats["executedCases"] += 1
            raised = False
            try:
                _check(candidate, authority)
            except BaseException:                       # noqa: BLE001 - measured
                stats["unguardedEscapes"] += 1
                raised = True
            # The guarded entrypoint is exercised on every case where the
            # unguarded layer raised - the only cases where it can matter - and
            # additionally once per enumerated path as a live control.
            if raised or path not in seen_paths:
                seen_paths.add(path)
                stats["guardedExercised"] += 1
                try:
                    check(candidate, authority)
                except BaseException:                   # noqa: BLE001 - measured
                    stats["guardedEscapes"] += 1
    finally:
        authority.census_enabled = saved
    return census, stats


# ---------------------------------------------------------------------------
# Section 10.  The contract check.
# ---------------------------------------------------------------------------

DECLARED_LEAF_KEY_IDS = frozenset({
    "plan-intent-schema-version", "plan-intent-intent-kind",
    "admission-descriptor-schema-version", "full-profile-schema-version",
    "full-profile-descriptor-schema-version", "stored-view-schema-version",
    "stored-view-intent-kind", "resolved-configuration-deciding-layer",
    "resolved-configuration-analysis-affecting",
})
DECLARED_COLLECTION_KEY_IDS = frozenset({
    "resolved-configuration-path", "contribution-activation-id",
    "contribution-id", "capability-grant-id",
})
DECLARED_HOSTILE_TYPES = frozenset({
    "object", "array", "boolean-true", "boolean-false", "null",
    "float-equal-to-one", "integer-zero", "integer-negative", "empty-string",
    "numeric-string",
})
DECLARED_INTEGER_CONSTANT_IDS = frozenset({
    "plan-intent-schema-version", "admission-descriptor-schema-version",
    "plan-descriptor-schema-major", "coverage-schema-version",
    "resolved-configuration-deciding-layer", "stage-budget-limit",
    "descriptor-budget-limit", "totality-matrix-case-count",
})
DECLARED_TOTALITY_CLASSES = frozenset({
    "object-in-scalar-collection-key", "array-in-scalar-collection-key",
    "boolean-in-scalar-collection-key", "null-in-scalar-collection-key",
    "boolean-in-declared-integer-constant", "float-in-declared-integer-constant",
    "string-in-declared-integer-constant",
})
DECLARED_EXIT_CODES = frozenset({"0", "1", "2", "3"})


def _matrix_values(matrix):
    return [(item.get("jsonType"), item.get("value"))
            for item in matrix.get("hostileValues", [])]


def _check(c, authority):
    f = []
    d9 = authority.json(D9)
    fp = authority.json(FP)
    tm = authority.json(TM)
    operability = authority.json(OP)
    delivery = authority.json(DELIVERY)
    ri = authority.json(RESOLVED_INPUTS)
    v3 = authority.json(V3_CONTRACT)
    v3_module = authority.module(V3_CHECKER)
    relations = set(fp["relationRegistry"]["relations"]) if fp else set()
    ids = canonical_identifiers(ri)

    f.extend(_scan_findings())

    # ---- candidate identity ------------------------------------------------
    if c.get("artifact") != "opensip.c2-plan-stage-schema":
        f.append("C2V4: candidate is not the C-2 plan/stage schema artifact")
    if not exact_int(c.get("version"), 4) or not exact_int(c.get("supersedes"), 3):
        f.append("C2V4: candidate must declare version 4 superseding 3 as JSON integers")
    if "CANDIDATE-NOT-APPLIED" not in str(c.get("status")) or \
            "AWAITING-INDEPENDENT-REVIEW" not in str(c.get("status")):
        f.append("C2V4: candidate status must remain CANDIDATE-NOT-APPLIED / "
                 "AWAITING-INDEPENDENT-REVIEW")

    # ---- LB-C2-06: the lineage must record the unattributed byte state ------
    lineage = c.get("lineage", {})
    states = lineage.get("byteStates", []) if isinstance(lineage, dict) else []
    by_state = {s.get("state"): s for s in states if isinstance(s, dict)}
    if set(by_state) != {"REVIEWED-BY-THE-STALE-PASS", "UNATTRIBUTED-INTERMEDIATE",
                         "LIVE-V3-AND-THE-REJECTED-BYTES", "V4-CANDIDATE"}:
        f.append("LB-C2-06: the lineage does not record all four C-2 byte states")
    else:
        if by_state["REVIEWED-BY-THE-STALE-PASS"].get("schemaSha256") != \
                "fbba5d0afe46405c79bd8980dfbd4a6a7a34a48c1fe3be0a5bfd3c12388ce511" or \
                by_state["UNATTRIBUTED-INTERMEDIATE"].get("schemaSha256") != \
                "84e0bda2f9226874c0a1121d63f71945c7ac180ae33d66121fd28d2fdea5e11d" or \
                by_state["LIVE-V3-AND-THE-REJECTED-BYTES"].get("schemaSha256") != \
                PINS[V3_CONTRACT]:
            f.append("LB-C2-06: a recorded lineage digest does not match the byte state "
                     "it names")
        intermediate = by_state["UNATTRIBUTED-INTERMEDIATE"]
        if not str(intermediate.get("recordedBy", "")).startswith("NOTHING"):
            f.append("LB-C2-06: the intermediate byte state is not recorded as "
                     "unattributed — it had no witness and must not be relabelled")
        if not str(intermediate.get("attributionStatus", "")).startswith(
                "RECONSTRUCTED, NOT WITNESSED"):
            f.append("LB-C2-06: the intermediate byte state's content is reconstruction, "
                     "not observation, and must say so")
    if not exact_int(lineage.get("commitmentContinuity", {}).get(
            "expectedUnchangedVectors"), 7):
        f.append("LB-C2-06: the lineage does not bind seven unchanged commitment vectors")

    # ---- the pinned review this candidate repairs --------------------------
    repairs = c.get("repairs", {})
    if repairs.get("reviewedBytes") != PINS[V3_CONTRACT] or \
            repairs.get("reviewedCheckerBytes") != PINS[V3_CHECKER] or \
            repairs.get("review") != V3_REVIEW or \
            repairs.get("reviewVerdict") != "REJECT" or \
            not exact_int(repairs.get("reviewBlockingFindingCount"), 2):
        f.append("C2V4: the repairs section does not bind the exact reviewed bytes and "
                 "the exact REJECT verdict with two blocking findings")
    declared_ids = [item.get("id") for item in repairs.get("items", [])]
    if declared_ids != ["LB-C2-01", "LB-C2-02", "LB-C2-03", "LB-C2-04", "LB-C2-05",
                        "LB-C2-06"]:
        f.append("C2V4: the repairs section does not address exactly the six review "
                 "findings in order")
    known_mutations = {name for name, _ in CONTRACT_MUTATIONS} | \
                      {name for name, _ in SOURCE_MUTATIONS} | \
                      {row[0] for row in SCAN_MUTATIONS}
    for item in repairs.get("items", []):
        declared = item.get("mutations", [])
        if not declared and item.get("id") != "LB-C2-06":
            f.append(f"C2V4: repair {item.get('id')} declares no falsifier — a repair "
                     "with no retained mutation is a claim, not a repair")
        for label in declared:
            if label not in known_mutations:
                f.append(f"C2V4: repair {item.get('id')} declares mutation {label!r}, "
                         "which this checker does not retain or execute")

    # ---- C1X: the admission model must agree with the LIVE D9 axes ---------
    if fp is None:
        f.append(f"C2X: could not load {FP} — relation constraints unverified")
    if d9 is None:
        f.append(f"C1X: could not load {D9} — the admission boundary is unverified")
    if d9:
        goldens = d9["goldenCases"]
        levels = {lv["level"]: lv for lv in c["theAdmissionBoundary"]["levels"]}
        for name, lv in levels.items():
            corr = lv.get("d9Correspondence", "")
            pairs = [p.strip() for p in corr.split(",") if "=" in p]
            want = dict(p.split("=", 1) for p in pairs)
            if want and not any(all(g["scenarioAxes"].get(k) == v for k, v in want.items())
                                for g in goldens):
                f.append(f"C1X: level '{name}' declares D9 correspondence '{corr}' but no "
                         f"D9 golden matches it")
        snap = [g for g in goldens
                if g["scenarioAxes"].get("deficiency") == "convergence-exhausted"]
        if not snap:
            f.append("C1X: D9 has no convergence-exhausted golden — the snapshot boundary "
                     "claim cannot be cross-checked")
        for g in snap:
            ax = g["scenarioAxes"]
            if ax["admission"] != "admitted":
                f.append(f"C1X: D9 golden '{g['id']}' treats snapshot exhaustion as "
                         f"admission={ax['admission']}, but C-2 places snapshot-binding "
                         f"AFTER admission (B-C2V2-01)")
            if ax["lifecycle"] != "coherent-terminal-run":
                f.append(f"C1X: D9 golden '{g['id']}' has lifecycle={ax['lifecycle']}; C-2 "
                         f"claims snapshot exhaustion seals a coherent terminal Run")
        sb = levels.get("snapshot-binding", {})
        if "POST-ADMISSION" not in sb.get("onFailure", "").upper():
            f.append("C1X: snapshot-binding does not declare post-admission failure semantics")
        if "ExecutionId" not in levels.get("attempt-admission", {}).get("allocates", []):
            f.append("C1X: ExecutionId is not allocated at attempt-admission — a crash "
                     "before snapshot work could not name the orphan (EC-6)")

    # ---- I1..I4 joins ------------------------------------------------------
    intent_spec = c.get("planIntent", {})
    lifecycle = intent_spec.get("lifecycle", {})
    wire_types = intent_spec.get("wireTypes", {})
    if "No ExecutionId" not in lifecycle.get("onInvalidOrExcluded", "") or \
            "AttemptRecord" not in lifecycle.get("onInvalidOrExcluded", ""):
        f.append("I1: invalid/excluded PlanIntent does not bind zero attempt allocation")
    if tm is None:
        f.append(f"C2I-TM: could not load {TM} — ProjectId path encoding join unverified")
    elif wire_types.get("projectId", {}).get("pattern") != \
            tm.get("storageNamespace", {}).get("projectId", {}).get("canonicalTextPattern"):
        f.append("C2I-TM: PlanIntent and storage namespace disagree on ProjectId encoding")
    request_join = intent_spec.get("storedViewJoin", {}).get("requestIdContract", {})
    if operability is None:
        f.append(f"C2I-OP: could not load {OP} — stored-read REQUEST-ID-V1 join unverified")
    else:
        live_request = operability.get("requestIdContract", {})
        live_pattern = live_request.get("representation", {}).get("regex")
        if request_join.get("id") != "REQUEST-ID-V1" or \
                request_join.get("source") != "operability.v2.json#requestIdContract" or \
                request_join.get("pattern") != live_pattern or \
                live_pattern != r"^req1_[0-9a-f]{32}$":
            f.append("C2I-OP: stored-view envelopes drift from live REQUEST-ID-V1")
        owner_blob = json.dumps(request_join)
        live_owner_blob = json.dumps(live_request.get("authority", {}))
        if "host-minted-reserved" not in owner_blob or \
                "MUST NOT supply requestId" not in live_owner_blob:
            f.append("C2I-OP: stored-view RequestId ownership/caller exclusion is incomplete")

    # ---- C2I-RI: LB-C2-05, the byte-exact PLAN-ID / SNAPSHOT-ID join -------
    if ri is None or not ids:
        f.append(f"C2I-RI: could not load {RESOLVED_INPUTS} — PLAN-ID-V1 and "
                 "SNAPSHOT-ID-V1 joins unverified")
    else:
        if wire_types.get("planId", {}).get("pattern") != ids["planIdPattern"] or \
                ids["planIdPattern"] != PLAN_ID_RE.pattern:
            f.append("C2I-RI: PlanIntent.wireTypes.planId drifts from the live "
                     "resolved-inputs PLAN-ID-V1 identity representation")
        if wire_types.get("snapshotId", {}).get("pattern") != ids["snapshotIdPattern"] or \
                ids["snapshotIdPattern"] != SNAPSHOT_ID_RE.pattern:
            f.append("C2I-RI: PlanIntent.wireTypes.snapshotId drifts from the live "
                     "resolved-inputs SNAPSHOT-ID-V1 identity representation")
        if wire_types.get("executionId", {}).get("pattern") != EXECUTION_ID_RE.pattern or \
                wire_types.get("executionId", {}).get("owner") != "C-2" or \
                "NO cross-contract EXECUTION-ID-V1 owner exists" not in \
                str(wire_types.get("executionId", {}).get("ownershipHonesty")):
            f.append("C2I-RI: the executionId wire type must declare C-2 ownership and "
                     "state plainly that no cross-contract owner exists")
        if not EXECUTION_ID_RE.fullmatch(str(ids["executionId"])):
            f.append("C2I-RI: the corpus ExecutionId spelling does not satisfy the "
                     "declared EXECUTION-ID-V1 grammar")
        binding_zero = next((x for x in c.get("intentBindingFixtures", [])
                             if x.get("id") == "valid-frozen-intent-execution-plan"), None)
        if binding_zero is None or \
                binding_zero.get("executionPlan", {}).get("planId") != ids["planId"] or \
                binding_zero.get("executionPlan", {}).get("snapshotId") != ids["snapshotId"] or \
                binding_zero.get("attemptRecord", {}).get("executionId") != ids["executionId"]:
            f.append("C2I-RI: the positive binding vector does not carry the owning "
                     "artifact's PlanId/SnapshotId/ExecutionId values (LB-C2-05)")

    # ---- LB-C2-01: the declared integer-constant register ------------------
    constants = intent_spec.get("integerConstantFields", {})
    if {item.get("id") for item in constants.get("fields", [])} != \
            DECLARED_INTEGER_CONSTANT_IDS:
        f.append("LB-C2-01: the declared integer-constant register is not the exact "
                 "swept set; a site added or removed here is a silent reopening")
    if wire_types.get("schemaVersionInteger", {}).get("jsonType") != "integer" or \
            not exact_int(wire_types.get("schemaVersionInteger", {}).get("constant"), 1) or \
            "A JSON boolean is NOT an integer" not in \
            str(wire_types.get("schemaVersionInteger", {}).get("rule")):
        f.append("LB-C2-01: the schemaVersionInteger wire type does not declare that a "
                 "JSON boolean is not a JSON integer")
    if wire_types.get("subjectScopeCommitment", {}).get("wireType") != "sha256Id" or \
            wire_types.get("subjectScopeCommitment", {}).get("pattern") != \
            SHA256_ID_RE.pattern:
        f.append("LB-C2-03: subjectScopeCommitment does not declare the sha256Id wire type")
    return f + _check_fixtures(c, authority, relations, fp, delivery, ids, v3, v3_module)


def _check_fixtures(c, authority, relations, fp, delivery, ids, v3, v3_module):
    f = []
    intent_spec = c.get("planIntent", {})
    lifecycle = intent_spec.get("lifecycle", {})
    intent_values, fixture_findings = _intent_fixture_values(c)
    f.extend(fixture_findings)

    # ---- C2DL: the named v1 full-profile provider oracle -------------------
    full_profile = next((fx for fx in c.get("planIntentFixtures", [])
                         if fx.get("id") == "valid-full-profile-semantic-providers"), None)
    canonical_provider_ids = {"rust-semantic", "typescript-semantic"}
    if full_profile is None or full_profile.get("productScope") != "V1 FULL PROFILE" or \
            full_profile.get("id") not in intent_values:
        f.append("C2DL: named V1 FULL PROFILE PlanIntent oracle is absent")
    elif delivery is None:
        f.append(f"C2DL: could not load {DELIVERY} — v1 provider namespace join unverified")
    else:
        descriptor = _analysis_descriptor(intent_values[full_profile["id"]])
        contribution_ids = {
            item.get("contributionId") for item in descriptor.get("contributions", [])
            if isinstance(item, dict) and item.get("authority") == "semantic-provider"}
        provider_ids = {
            stage.get("providerId") for stage in descriptor.get("workflow", {}).get("stages", [])
            if isinstance(stage, dict) and stage.get("operator") == "semantic-provider"}
        conditions = delivery.get("initialProductScope", {}).get(
            "v1PlanIntentOverlay", {}).get("conditions", {})
        canonical_list = ["rust-semantic", "typescript-semantic"]
        if contribution_ids != canonical_provider_ids or \
                provider_ids != canonical_provider_ids or \
                conditions.get("bundled-semantic-provider", {}).get(
                    "allowedContributionIds") != canonical_list or \
                conditions.get("bundled-semantic-provider-stage", {}).get(
                    "allowedProviderIds") != canonical_list:
            f.append("C2DL: v1 full-profile contributionId/providerId surfaces drift "
                     "from DELIVERY's exact rust-semantic/typescript-semantic namespace")

    # ---- I1: the leaf-inclusive totality matrix ----------------------------
    matrix = c.get("planIntentTotalityMatrix", {})
    matrix_keys = list(matrix.get("scalarCollectionKeys", [])) + \
        list(matrix.get("scalarLeafKeys", []))
    matrix_values = _matrix_values(matrix)
    if {item.get("id") for item in matrix.get("scalarCollectionKeys", [])} != \
            DECLARED_COLLECTION_KEY_IDS or \
            {item.get("id") for item in matrix.get("scalarLeafKeys", [])} != \
            DECLARED_LEAF_KEY_IDS or \
            {label for label, _ in matrix_values} != DECLARED_HOSTILE_TYPES or \
            matrix.get("expectedViolation") != "C2I-02" or \
            matrix.get("expectedCreatesAttempt") is not False:
        f.append("I1: the hostile parsed-JSON totality matrix is not the exact declared "
                 "corpus over BOTH collection-adjacent scalars and declared-constant "
                 "scalar leaves — v3's corpus was pinned never to reach a scalar leaf, "
                 "which is exactly where LB-C2-01 lived")
    else:
        enumerated = no_ops = 0
        for key_case in matrix_keys:
            base = intent_values.get(key_case.get("baseFixtureId"))
            if base is None:
                f.append(f"I1 totality {key_case.get('id')}: base fixture missing")
                continue
            try:
                current = _pointer_resolve(base, key_case["path"])
            except MALFORMED_SHAPE_EXCEPTIONS:
                f.append(f"I1 totality {key_case.get('id')}: declared path does not exist")
                continue
            for label, value in matrix_values:
                enumerated += 1
                if _same_leaf(current, value):
                    no_ops += 1
                    continue
                candidate = _pointer_mutate(base, {"op": "set",
                                                   "path": key_case["path"], "value": value})
                errors = validate_plan_intent(candidate, c, relations)
                codes = {code for code, _ in errors}
                if "C2I-02" not in codes:
                    f.append(f"I1 totality {key_case['id']}/{label}: expected typed C2I-02 "
                             f"rejection, got {sorted(codes)}")
                _commitment, encode_errs = plan_intent_commitment_total(candidate, c)
                if not errors and encode_errs:
                    f.append(f"I1 totality {key_case['id']}/{label}: ADMITTED and then "
                             "failed to encode — the LB-C2-01 admit-then-raise path")
        declared_cases = matrix.get("caseCount")
        declared_no_ops = matrix.get("noOpInjections")
        declared_executed = matrix.get("executedCases")
        if not is_wire_int(declared_cases) or declared_cases != enumerated or \
                not is_wire_int(declared_no_ops) or declared_no_ops != no_ops or \
                not is_wire_int(declared_executed) or \
                declared_executed != enumerated - no_ops:
            f.append(f"I1: the totality matrix publishes caseCount={declared_cases!r}, "
                     f"noOpInjections={declared_no_ops!r}, "
                     f"executedCases={declared_executed!r}; this run enumerated "
                     f"{enumerated}, skipped {no_ops} and executed {enumerated - no_ops}")

    # ---- I1/I2: PlanIntent fixtures and the seven commitment vectors -------
    seen_intent_codes, valid_operations = set(), set()
    reproduced, moved = 0, []
    for fx in c.get("planIntentFixtures", []):
        intent = intent_values.get(fx.get("id"))
        if intent is None:
            continue
        errs = validate_plan_intent(intent, c, relations)
        codes = {code for code, _ in errs}
        seen_intent_codes.update(codes)
        commitment, encode_errs = plan_intent_commitment_total(intent, c)
        errs = errs + encode_errs
        codes.update(code for code, _ in encode_errs)
        if fx.get("valid"):
            expected = fx.get("expectedCommitment")
            if errs:
                f.append(f"I1 {fx['id']}: expected valid but got — {errs[0][1]}")
            if expected != commitment:
                f.append(f"I2 {fx['id']}: commitment vector is {expected!r}; recomputed "
                         f"{commitment!r}")
            # The seven vectors must also reproduce under the PINNED v3 encoder,
            # executed from its verified snapshot.  A repair that moved a
            # commitment is a major finding, never something to absorb.
            if v3_module is not None:
                try:
                    independent = v3_module.plan_intent_commitment(intent, c)
                except Exception as exc:               # noqa: BLE001 - reported
                    independent = f"pinned v3 encoder raised {type(exc).__name__}: {exc}"
                if independent == expected:
                    reproduced += 1
                else:
                    moved.append(f"{fx['id']}: declared {expected!r}, pinned v3 encoder "
                                 f"produced {independent!r}")
            if intent.get("intentKind") == "stored-view":
                valid_operations.add(intent["storedView"]["query"]["operation"])
                if fx.get("expectedCreatesAttempt") is not False or \
                        fx.get("expectedCreatesExecutionPlan") is not False:
                    f.append(f"I1 {fx['id']}: stored-view fixture does not assert zero "
                             "attempt/ExecutionPlan")
                stored_rule = lifecycle.get("onValidatedStoredRead", "")
                if "No ExecutionId" not in stored_rule or "AttemptRecord" not in stored_rule or \
                        "ExecutionPlan" not in stored_rule:
                    f.append("I1: stored-view lifecycle does not preserve the zero-attempt "
                             "boundary")
        else:
            want = fx.get("violates")
            if not errs:
                f.append(f"I1 {fx['id']}: expected pre-attempt rejection by {want} but "
                         "intent validated")
            elif want not in list(codes):
                f.append(f"I1 {fx['id']}: expected {want}, got {sorted(codes)}")
    for message in moved:
        f.append(f"C2V4-COMMITMENT-MOVED: a v4 repair changed a planIntentCommitment. "
                 f"This is a MAJOR finding and must not be absorbed — {message}")
    v3_vectors = {fx["id"]: fx.get("expectedCommitment")
                  for fx in (v3 or {}).get("planIntentFixtures", []) if fx.get("valid")}
    v4_vectors = {fx["id"]: fx.get("expectedCommitment")
                  for fx in c.get("planIntentFixtures", []) if fx.get("valid")}
    if v3_vectors and v3_vectors != v4_vectors:
        f.append("C2V4-COMMITMENT-MOVED: the seven declared v3 vectors are not the seven "
                 f"declared v4 vectors — v3 {sorted(v3_vectors.items())} vs v4 "
                 f"{sorted(v4_vectors.items())}")
    if v3_module is not None and not exact_int(reproduced, len(v4_vectors)):
        f.append(f"I2: only {reproduced} of {len(v4_vectors)} commitment vectors "
                 "reproduced under the pinned v3 encoder")
    for required_code in {"C2I-01", "C2I-02", "C2I-03", "C2I-07"} - seen_intent_codes:
        f.append(f"I1: no negative PlanIntent fixture proves {required_code}")
    totality = intent_spec.get("validationTotality", {})
    totality_classes = {fx.get("totalityClass") for fx in c.get("planIntentFixtures", [])
                        if fx.get("totalityClass")}
    if totality_classes != DECLARED_TOTALITY_CLASSES or \
            set(totality.get("retainedClasses", [])) != DECLARED_TOTALITY_CLASSES or \
            "CONTAINER AND SCALAR LEAF alike" not in totality.get("domain", "") or \
            "never raises" not in totality.get("result", "") or \
            "admitThenCommitClosure" not in totality:
        f.append("I1: the PlanIntent parsed-JSON totality contract/corpus does not reach "
                 "scalar leaves or does not bind the admit-then-commit closure")
    expected_operations = set(intent_spec.get("storedViewIntentV1", {})
                              .get("query", {}).get("closedTaggedUnion", {}))
    if valid_operations != expected_operations:
        f.append(f"I1: stored-view positive vectors cover {sorted(valid_operations)}, "
                 f"expected every query branch {sorted(expected_operations)}")

    valid_intents = [intent_values[fx["id"]] for fx in c.get("planIntentFixtures", [])
                     if fx.get("valid") and fx.get("id") in intent_values]
    external_scanner_visible = any(
        intent.get("intentKind") == "analysis" and
        any(stage.get("kind") == "fact-derivation" and
            stage.get("operator") == "external-scanner" and stage.get("providerId")
            for stage in intent["analysis"]["admissionDescriptor"]["workflow"]["stages"]) and
        any(item.get("authority") == "external-scanner"
            for item in intent["analysis"]["admissionDescriptor"]["contributions"])
        for intent in valid_intents)
    if not external_scanner_visible:
        f.append("I1: no valid general-schema PlanIntent exposes external-scanner at both "
                 "stage and contribution surfaces")

    # ---- I3 / I4 bindings --------------------------------------------------
    seen_binding_codes = set()
    for fx in c.get("intentBindingFixtures", []):
        base = intent_values.get(fx.get("baseFixtureId"))
        if base is None:
            f.append(f"I3 {fx.get('id')}: unknown base PlanIntent fixture")
            continue
        errs = validate_intent_binding(fx, base, c, relations, ids)
        codes = {code for code, _ in errs}
        seen_binding_codes.update(codes)
        if fx.get("valid") and errs:
            f.append(f"I3 {fx['id']}: expected valid but got — {errs[0][1]}")
        elif not fx.get("valid"):
            want = fx.get("violates")
            if not errs:
                f.append(f"I3 {fx['id']}: expected binding rejection by {want} but it validated")
            elif want not in list(codes):
                f.append(f"I3 {fx['id']}: expected {want}, got {sorted(codes)}")
    for required_code in {"C2I-05", "C2I-06"} - seen_binding_codes:
        f.append(f"I3: no negative analysis intent-binding fixture proves {required_code}")

    seen_stored_binding_codes = set()
    for fx in c.get("storedViewBindingFixtures", []):
        base = intent_values.get(fx.get("baseFixtureId"))
        if base is None:
            f.append(f"I4 {fx.get('id')}: unknown base stored-view fixture")
            continue
        errs = validate_stored_view_binding(fx, base, c)
        codes = {code for code, _ in errs}
        seen_stored_binding_codes.update(codes)
        if fx.get("valid") and errs:
            f.append(f"I4 {fx['id']}: expected valid but got — {errs[0][1]}")
        elif fx.get("valid") and fx.get("requestIdAuthority") != "host-minted-reserved":
            f.append(f"I4 {fx['id']}: positive stored read does not declare "
                     "host-minted-reserved REQUEST-ID-V1")
        elif not fx.get("valid"):
            want = fx.get("violates")
            if not errs:
                f.append(f"I4 {fx['id']}: expected stored-read rejection by {want} but it "
                         "validated")
            elif want not in list(codes):
                f.append(f"I4 {fx['id']}: expected {want}, got {sorted(codes)}")
        if fx.get("valid") and (fx.get("expectedCreatesAttempt") is not False or
                                fx.get("expectedCreatesExecutionPlan") is not False):
            f.append(f"I4 {fx['id']}: stored binding does not assert zero attempt/ExecutionPlan")
    for required_code in {"C2I-08", "C2I-09"} - seen_stored_binding_codes:
        f.append(f"I4: no negative stored-view binding fixture proves {required_code}")

    # ---- C3X: no paper seals ----------------------------------------------
    impl = {t["id"]: t.get("implementable", False) for t in c["conformanceTests"]}
    for prop in c["dischargeStatus"]["properties"]:
        for tid in prop["dischargedBy"]:
            if tid not in impl:
                f.append(f"C3X: '{prop['property']}' names unknown test '{tid}'")
            elif not impl[tid]:
                f.append(f"C3X: '{prop['property']}' is discharged by '{tid}', which is "
                         f"not implementable — that is a paper seal")
        if prop["status"] == "SPECIFIED" and prop["dischargedBy"] and \
                prop.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
            f.append(f"C3X: '{prop['property']}' is SPECIFIED by unexecuted tests but "
                     "does not say IMPLEMENTABLE_UNEXECUTED")
        if prop["status"] in {"DISCHARGED", "DEMONSTRATED"}:
            if not prop["dischargedBy"]:
                f.append(f"C3X: '{prop['property']}' claims {prop['status']} with no tests")
            if prop.get("evidenceGrade") != "DEMONSTRATED" or not \
                    prop.get("demonstrationEvidenceIds"):
                f.append(f"C3X: '{prop['property']}' claims {prop['status']} without "
                         "evidenceGrade DEMONSTRATED and retained demonstrationEvidenceIds "
                         "— implementable:true is not execution evidence")

    # ---- P1..P5 plan fixtures ---------------------------------------------
    provider_fixture = next((fx for fx in c.get("planFixtures", [])
                             if isinstance(fx, dict) and
                             fx.get("id") == "valid-provider-plan"), None)
    provider_stages = ((provider_fixture or {}).get("plan") or {}).get("stages")
    semantic_stages = [stage for stage in provider_stages
                       if isinstance(stage, dict) and
                       stage.get("operator") == "semantic-provider"] \
        if isinstance(provider_stages, list) else []
    if provider_fixture is None or provider_fixture.get("valid") is not True or \
            not exact_int(len(semantic_stages), 1) or \
            semantic_stages[0].get("providerId") != "typescript-semantic":
        f.append("C2PV: valid-provider-plan must use the exact shipping providerId "
                 "'typescript-semantic'")
    for fx in c["planFixtures"]:
        errs = validate_plan(fx["plan"], c, relations)
        codes = {code for code, _ in errs}
        if fx["valid"] and errs:
            f.append(f"P1 {fx['id']}: expected valid but got — {errs[0][1]}")
        elif not fx["valid"]:
            want = fx.get("violates")
            if not errs:
                f.append(f"P1 {fx['id']}: expected REJECTION (violates {want}) but the "
                         f"plan validated")
            elif want not in list(codes):
                f.append(f"P1 {fx['id']}: expected rejection by {want} but was rejected "
                         f"by {sorted(codes)} — the fixture proves a different property "
                         f"than it claims")

    # ---- C4 coverage fixtures, LB-C2-02 and LB-C2-03 -----------------------
    entry_schema = c["coverageKey"].get("entrySchema", {})
    if entry_schema.get("closed") is not True or \
            "REJECTED with the named finding C2X-ROOT" not in str(entry_schema.get("rootRule")):
        f.append("LB-C2-02: the Coverage entry schema is not closed, or does not bind the "
                 "named non-object-root rejection")
    for case in c["coverageKey"].get("rootTotalityCases", []):
        errs = validate_coverage(case.get("value"), c, fp)
        if not errs or not str(errs[0]).startswith("C2X-ROOT:"):
            f.append(f"LB-C2-02 root {case.get('id')}: a hostile Coverage root must return "
                     f"a named C2X-ROOT finding, got {errs!r}")
    for fx in c["coverageFixtures"]:
        errs = validate_coverage(fx["entry"], c, fp)
        codes = {str(e).split(":", 1)[0] for e in errs}
        if fx["valid"] and errs:
            f.append(f"C4 {fx['id']}: expected valid but got — {errs[0]}")
        elif not fx["valid"] and not errs:
            f.append(f"C4 {fx['id']}: expected REJECTION (violates {fx.get('violates')}) "
                     f"but the entry validated")
        elif not fx["valid"] and fx.get("violates") not in list(codes):
            f.append(f"C4 {fx['id']}: expected rejection by {fx.get('violates')} but was "
                     f"rejected by {sorted(codes)}")
        preimage = fx.get("subjectScopeCommitmentPreimageUtf8")
        if fx["valid"]:
            if not isinstance(preimage, str):
                f.append(f"C4 {fx['id']}: a valid coverage fixture must declare the exact "
                         "preimage of its subjectScopeCommitment, so the shape binding is "
                         "not satisfied by an opaque constant (LB-C2-03)")
            else:
                digest = "sha256:" + hashlib.sha256(preimage.encode("utf-8")).hexdigest()
                if fx["entry"].get("subjectScopeCommitment") != digest:
                    f.append(f"C4 {fx['id']}: subjectScopeCommitment is not SHA-256 over "
                             "its declared preimage")

    kinds = set(c["executionPlan"]["stageKinds"])
    seen = {st.get("kind") for fx in c["planFixtures"] if fx["valid"]
            for st in fx["plan"]["stages"]}
    for k in kinds - seen:
        f.append(f"P2: stage kind '{k}' has no positive fixture — unexercised schema")

    # ---- the published leaf-inclusive measurement --------------------------
    f.extend(_census_findings(c, authority, relations, fp, intent_values))

    # ---- the checker mode contract ----------------------------------------
    mode = c.get("checkerModeContract", {})
    if mode.get("checker") != "check-c2-v4.py" or \
            set(mode.get("exitCodes", {})) != DECLARED_EXIT_CODES or \
            "REFUSED" not in str(mode.get("exitCodes", {}).get("3")):
        f.append("C2V4: the checker mode contract does not declare exactly exit codes "
                 "0/1/2/3 with 3 reserved for the dirty-base selftest refusal")
    return f


def _pointer_resolve(value, pointer):
    node = value
    for part in [p.replace("~1", "/").replace("~0", "~")
                 for p in pointer.split("/")[1:]]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def _census_findings(c, authority, relations, fp, intent_values):
    f = []
    if not authority.census_enabled:
        return f
    published = c.get("hostileScalarLeafTotality", {})
    matrix = c.get("planIntentTotalityMatrix", {})
    values = _matrix_values(matrix)
    if not values:
        return ["I1: no hostile injection values are declared, so the leaf-inclusive "
                "measurement cannot be reproduced"]
    surfaces = measure_surfaces(c, relations, fp, values, intent_values)
    root_census, root_stats = measure_contract_root(c, authority, execute=False)
    authority.census = surfaces
    authority.contract_census = root_census
    declared = {row.get("id"): row for row in published.get("surfaces", [])}
    for name in sorted(surfaces):
        measured = surfaces[name]
        row = declared.get(name)
        if row is None:
            f.append(f"C2V4-CENSUS: the candidate publishes no measurement for the "
                     f"{name} surface, which this run enumerated over "
                     f"{measured['census']['enumeratedPaths']} paths of which "
                     f"{measured['census']['scalarLeafPaths']} are scalar leaves")
            continue
        for key, value in measured["census"].items():
            if row.get(key) != value:
                f.append(f"C2V4-CENSUS: {name}.{key} is published as {row.get(key)!r} but "
                         f"this run measured {value}")
        for key in ("executedCases", "unguardedEscapes", "guardedEscapes",
                    "silentAccepts", "admitThenRaise",
                    "typeDistinctConstantAdmissions"):
            if row.get(key) != measured["stats"][key]:
                f.append(f"C2V4-CENSUS: {name}.{key} is published as {row.get(key)!r} but "
                         f"this run measured {measured['stats'][key]}")
        if measured["stats"]["guardedEscapes"]:
            f.append(f"C2V4-TOTALITY: {measured['stats']['guardedEscapes']} hostile case(s) "
                     f"escaped the guarded {name} boundary as a traceback")
        if measured["stats"]["unguardedEscapes"]:
            # LB-C2-04.  The named-finding boundary is the backstop, not the
            # repair: an explicit type guard must reject the container before it
            # reaches a membership test, so the finding names the field.
            f.append(f"LB-C2-04: {measured['stats']['unguardedEscapes']} hostile case(s) "
                     f"raised inside the unguarded {name} validator; the boundary caught "
                     "them but the explicit type guard that names the field is missing")
        if measured["stats"]["admitThenRaise"]:
            f.append(f"LB-C2-01: {measured['stats']['admitThenRaise']} hostile case(s) were "
                     "ADMITTED by validation and then failed to encode")
        if measured["stats"]["typeDistinctConstantAdmissions"]:
            f.append(f"LB-C2-01: {measured['stats']['typeDistinctConstantAdmissions']} "
                     "type-distinct spelling(s) of a declared integer constant were ADMITTED")
        if not int_in_range(measured["census"]["scalarLeafPaths"], 1, 10 ** 9):
            f.append(f"C2V4-CENSUS: the {name} enumeration reaches no scalar leaf position, "
                     "which is the exact blindness that produced LB-C2-01")
    root_row = published.get("contractRoot", {})
    for key, value in root_census.items():
        if root_row.get(key) != value:
            f.append(f"C2V4-CENSUS: contractRoot.{key} is published as "
                     f"{root_row.get(key)!r} but this run measured {value}")
    if "MUST be zero" not in str(root_row.get("guardedEscapesRule")) or \
            "Reported, NOT required to be zero" not in \
            str(root_row.get("unguardedEscapesRule")):
        f.append("C2V4-CENSUS: the contract-root block must state plainly which of its "
                 "two escape counts is required to be zero and which is only reported; "
                 "a single number covering both would be a claim over an unobserved "
                 "region")
    if root_row.get("executedIn") != "--selftest" or \
            "except the leaf-inclusive census layer" not in \
            str(root_row.get("executedLayers")):
        f.append("C2V4-CENSUS: the contract-root execution matrix must declare plainly "
                 "that it executes in --selftest, not in normal mode, and exactly which "
                 "layers it drives")
    if not int_in_range(root_census["scalarLeafPaths"], 1, 10 ** 9):
        f.append("C2V4-CENSUS: the contract-root enumeration reaches no scalar leaf")
    return f


def check(c, authority):
    """Total contract boundary: malformed parsed JSON becomes a named finding."""
    if not isinstance(c, dict) or not c:
        return ["C2-TOTALITY-ROOT: contract root must be a non-empty object"]
    admission = c.get("theAdmissionBoundary")
    if not isinstance(admission, dict) or not isinstance(admission.get("levels"), list):
        return ["C2-TOTALITY-SHAPE: theAdmissionBoundary.levels must be an array"]
    try:
        return _check(c, authority)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"C2-TOTALITY-EXCEPTION: malformed contract shape ({type(exc).__name__})"]


# ---------------------------------------------------------------------------
# Section 11.  Retained mutations.  Every repair carries at least one falsifier.
#
# The contract's `repairs` section names each mutation by label, and _check
# refuses any declared label this table does not retain, so a repair cannot
# claim a falsifier that is not executed.
# ---------------------------------------------------------------------------


def _fixture(c, section, fixture_id):
    return next(x for x in c[section] if x["id"] == fixture_id)


def _m_snapshot_preadmission(c):
    for lv in c["theAdmissionBoundary"]["levels"]:
        if lv["level"] == "snapshot-binding":
            lv["onFailure"] = "pre-admission: request-rejected, never a Run verdict"


def _m_execid_after_snapshot(c):
    for lv in c["theAdmissionBoundary"]["levels"]:
        if lv["level"] == "attempt-admission":
            lv["allocates"] = []


def _m_paper_seal(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "effectful work is unrepresentable as a Rule":
            p["dischargedBy"] = ["PS-09", "PS-12c"]
            p["status"] = "DISCHARGED"


def _m_ps07_discharges_privacy(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "physical storage schema stays private":
            p["dischargedBy"] = ["PS-02", "PS-07"]


def _m_implementable_boolean_discharges(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "fact sufficiency is predicate-relative":
            p["status"] = "DISCHARGED"
            p.pop("evidenceGrade", None)


def _m_allow_private_operator(c):
    c["stageSchemas"]["privateOperators"]["names"].remove("shardAssignment")


def _m_rule_may_have_grants(c):
    c["stageSchemas"]["kinds"]["rule-evaluation"]["forbidden"] = []
    c["stageSchemas"]["kinds"]["rule-evaluation"]["optional"] = ["capabilityGrants", "operator"]


def _m_open_stage_kinds(c):
    c["executionPlan"]["stageKinds"].append("snapshot")
    c["stageSchemas"]["kinds"]["snapshot"] = {"required": [], "optional": [],
                                              "effectClass": "no-effect"}


def _m_drop_target_universe(c):
    c["coverageKey"]["crossUniverseRelations"] = []


def _m_unknown_relation_ok(c):
    _fixture(c, "planFixtures", "reject-unknown-relation")["valid"] = True


def _m_probe_without_grants_ok(c):
    c["stageSchemas"]["kinds"]["probe"]["required"] = ["probeId"]


def _m_open_plan_intent(c):
    c["planIntent"]["schema"]["closed"] = False


def _m_change_intent_domain(c):
    c["planIntent"]["canonicalCommitment"]["domainTagUtf8"] = "opensip.plan-intent.v2"


def _m_drop_attempt_intent_commitment(c):
    _fixture(c, "intentBindingFixtures",
             "valid-frozen-intent-execution-plan")["attemptRecord"].pop("planIntentCommitment")


def _m_accept_stage_substitution(c):
    _fixture(c, "intentBindingFixtures",
             "reject-post-admission-stage-substitution")["valid"] = True


def _m_hide_external_scanner_intent(c):
    fixture = _fixture(c, "planIntentFixtures", "valid-explicit-general-authority-forms")
    stage = fixture["intent"]["analysis"]["admissionDescriptor"]["workflow"]["stages"][0]
    stage["operator"] = "builtin-extractor"
    stage.pop("providerId")


def _m_accept_null_contribution_id(c):
    _fixture(c, "planIntentFixtures",
             "reject-null-contribution-id-before-attempt")["valid"] = True


def _m_accept_stored_target_substitution(c):
    _fixture(c, "storedViewBindingFixtures",
             "reject-stored-read-target-substitution")["valid"] = True


def _m_shrink_plan_descriptor_join(c):
    c["planIntent"]["attemptAndExecutionJoin"]["planIdentityInputsRequired"].remove("contributions")


def _m_accept_object_config_path(c):
    _fixture(c, "planIntentFixtures",
             "reject-object-resolved-configuration-path-before-attempt")["valid"] = True


def _m_accept_array_activation_id(c):
    _fixture(c, "planIntentFixtures",
             "reject-array-contribution-activation-id-before-attempt")["valid"] = True


def _m_accept_boolean_contribution_id(c):
    _fixture(c, "planIntentFixtures",
             "reject-boolean-contribution-id-before-attempt")["valid"] = True


def _m_accept_null_grant_id(c):
    _fixture(c, "planIntentFixtures",
             "reject-null-capability-grant-id-before-attempt")["valid"] = True


def _m_accept_malformed_stored_request_id(c):
    _fixture(c, "storedViewBindingFixtures",
             "reject-stored-read-malformed-request-id")["valid"] = True


def _m_accept_caller_stored_request_id(c):
    _fixture(c, "storedViewBindingFixtures",
             "reject-stored-read-caller-supplied-request-id")["valid"] = True


def _m_drift_request_id_join(c):
    c["planIntent"]["storedViewJoin"]["requestIdContract"]["pattern"] = "^request-[0-9]+$"


def _m_drop_totality_collection_key(c):
    c["planIntentTotalityMatrix"]["scalarCollectionKeys"].pop()


def _m_drop_totality_hostile_type(c):
    c["planIntentTotalityMatrix"]["hostileValues"].pop()


def _m_prefix_full_profile_provider_ids(c):
    fixture = _fixture(c, "planIntentFixtures", "valid-full-profile-semantic-providers")
    descriptor = fixture["intent"]["analysis"]["admissionDescriptor"]
    prefixed = {"rust-semantic": "provider.rust-semantic",
                "typescript-semantic": "provider.typescript-semantic"}
    for item in descriptor["contributions"]:
        if item.get("contributionId") in prefixed:
            item["contributionId"] = prefixed[item["contributionId"]]
    for stage in descriptor["workflow"]["stages"]:
        if stage.get("providerId") in prefixed:
            stage["providerId"] = prefixed[stage["providerId"]]
    fixture["expectedCommitment"] = plan_intent_commitment(fixture["intent"], c)


def _set_valid_provider_plan_id(c, provider_id):
    _fixture(c, "planFixtures", "valid-provider-plan")["plan"]["stages"][0]["providerId"] = provider_id


def _m_alias_valid_provider_plan(c):
    _set_valid_provider_plan_id(c, "provider.typescript-semantic")


def _m_legacy_valid_provider_plan(c):
    _set_valid_provider_plan_id(c, "typescript")


def _m_arbitrary_valid_provider_plan(c):
    _set_valid_provider_plan_id(c, "arbitrary-semantic-provider")


# ---- v4 repairs -----------------------------------------------------------

def _m_narrow_totality_matrix(c):
    c["planIntentTotalityMatrix"]["scalarLeafKeys"] = []


def _m_drop_integer_constant_field(c):
    c["planIntent"]["integerConstantFields"]["fields"].pop()


def _m_reopen_coverage_schema(c):
    c["coverageKey"]["entrySchema"]["closed"] = False


def _m_restore_scope_placeholder(c):
    _fixture(c, "coverageFixtures",
             "intra-universe-complete")["entry"]["subjectScopeCommitment"] = "sha256:..."


def _m_drift_plan_id_join(c):
    c["planIntent"]["wireTypes"]["planId"]["pattern"] = "^plan-[0-9]+$"


def _m_drift_snapshot_id_join(c):
    c["planIntent"]["wireTypes"]["snapshotId"]["pattern"] = "^snap-[0-9]+$"


def _m_accept_placeholder_plan_id(c):
    _fixture(c, "intentBindingFixtures", "reject-noncanonical-plan-id")["valid"] = True


def _m_drop_lineage_state(c):
    c["lineage"]["byteStates"] = [s for s in c["lineage"]["byteStates"]
                                  if s.get("state") != "UNATTRIBUTED-INTERMEDIATE"]


def _m_relabel_reconstruction_as_witnessed(c):
    for state in c["lineage"]["byteStates"]:
        if state.get("state") == "UNATTRIBUTED-INTERMEDIATE":
            state["recordedBy"] = "witnessed by the DELIVERY reviewer5 adjudication response"
            state["attributionStatus"] = "WITNESSED"


def _m_soften_schema_version_declaration(c):
    c["planIntent"]["wireTypes"]["schemaVersionInteger"]["rule"] = \
        "The value must equal 1."


def _m_understate_leaf_census(c):
    for row in c["hostileScalarLeafTotality"]["surfaces"]:
        if row.get("id") == "plan-intent":
            row["scalarLeafPaths"] = 0


CONTRACT_MUTATIONS = [
    ("make snapshot failure pre-admission again (B-C2V2-01)", _m_snapshot_preadmission),
    ("allocate ExecutionId after snapshot work (EC-6)", _m_execid_after_snapshot),
    ("discharge a sealed property with an unbuilt test (B-C2V2-02)", _m_paper_seal),
    ("treat implementable:true as retained discharge evidence (R2-FINAL-02)",
     _m_implementable_boolean_discharges),
    ("let PS-07 discharge private-operator privacy (A1-C2V2-05)", _m_ps07_discharges_privacy),
    ("permit a private operator in a plan (PS-02)", _m_allow_private_operator),
    ("let a rule stage hold capability grants (PS-12a)", _m_rule_may_have_grants),
    ("reopen the stage-kind set (PS-01/PS-11)", _m_open_stage_kinds),
    ("stop requiring targetUniverseId (B-C2V2-05)", _m_drop_target_universe),
    ("accept a relation outside the fact-plane registry (P5)", _m_unknown_relation_ok),
    ("let a probe run without capability grants (PS-12b)", _m_probe_without_grants_ok),
    ("make the pre-admission PlanIntent schema open (IP-R4-04)", _m_open_plan_intent),
    ("change the PlanIntent commitment domain without new vectors", _m_change_intent_domain),
    ("allocate an attempt without its admitted-intent commitment",
     _m_drop_attempt_intent_commitment),
    ("accept post-admission stage substitution", _m_accept_stage_substitution),
    ("hide external-scanner from the pre-admission operator surface",
     _m_hide_external_scanner_intent),
    ("accept null contribution identity in admitted input", _m_accept_null_contribution_id),
    ("accept stored-read target substitution", _m_accept_stored_target_substitution),
    ("shrink the exact PlanDescriptor equality join", _m_shrink_plan_descriptor_join),
    ("accept object-valued resolved-configuration path", _m_accept_object_config_path),
    ("accept array-valued contribution activationId", _m_accept_array_activation_id),
    ("accept boolean-valued contributionId", _m_accept_boolean_contribution_id),
    ("accept null capability grantId", _m_accept_null_grant_id),
    ("accept malformed matching stored-read RequestId", _m_accept_malformed_stored_request_id),
    ("accept caller-supplied stored-read RequestId", _m_accept_caller_stored_request_id),
    ("drift stored-read RequestId from live REQUEST-ID-V1", _m_drift_request_id_join),
    ("drop one exception-prone scalar key from totality matrix", _m_drop_totality_collection_key),
    ("drop one hostile JSON type from totality matrix", _m_drop_totality_hostile_type),
    ("drift the joined v1 full-profile provider namespace to provider.*",
     _m_prefix_full_profile_provider_ids),
    ("alias valid-provider-plan as provider.typescript-semantic (R9-PROVIDER-VECTOR-01)",
     _m_alias_valid_provider_plan),
    ("alias valid-provider-plan as legacy typescript (R9-PROVIDER-VECTOR-01)",
     _m_legacy_valid_provider_plan),
    ("replace valid-provider-plan with an arbitrary canonical identifier "
     "(R9-PROVIDER-VECTOR-01)", _m_arbitrary_valid_provider_plan),
    # v4 repairs
    ("narrow the totality matrix back to container-adjacent keys only",
     _m_narrow_totality_matrix),
    ("delete a declared integer-constant field from the contract",
     _m_drop_integer_constant_field),
    ("soften the schemaVersionInteger type declaration",
     _m_soften_schema_version_declaration),
    ("reopen the Coverage entry schema", _m_reopen_coverage_schema),
    ("restore the 'sha256:...' placeholder into a valid fixture",
     _m_restore_scope_placeholder),
    ("drift the joined PLAN-ID-V1 pattern", _m_drift_plan_id_join),
    ("drift the joined SNAPSHOT-ID-V1 pattern", _m_drift_snapshot_id_join),
    ("accept the noncanonical plan-1 placeholder", _m_accept_placeholder_plan_id),
    ("drop the unattributed intermediate byte state from the lineage", _m_drop_lineage_state),
    ("relabel the reconstructed state as witnessed", _m_relabel_reconstruction_as_witnessed),
    ("understate the published scalar-leaf census", _m_understate_leaf_census),
]


# ---------------------------------------------------------------------------
# Section 12.  Source self-mutations.
#
# A guard is load-bearing only if breaking it is detected.  Each entry below
# rewrites this checker's own syntax tree, executes the mutated module, and
# requires it to report findings against the CLEAN candidate.
# ---------------------------------------------------------------------------


def _replace_body(tree, name, source):
    subject = copy.deepcopy(tree)
    replacement = ast.parse(source).body
    for node in subject.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            node.body = replacement
            return ast.fix_missing_locations(subject)
    raise AuthorityLoadError(f"cannot find {name} to mutate")


def _s_bare_schema_version(tree):
    return _replace_body(tree, "_schema_version_ok", "return value == 1")


def _s_bare_descriptor_schema_version(tree):
    return _replace_body(tree, "_descriptor_schema_version_ok", "return value == 1")


def _s_bare_plan_schema_major(tree):
    return _replace_body(tree, "_plan_schema_major_ok", "return value == 1")


def _s_truthy_relation(tree):
    """Restore v3's exact relation handling, truthiness short-circuit and all."""
    return _replace_body(tree, "_coverage_relation_findings", """
errs = []
rel = entry.get("relation")
if fp and rel:
    rels = fp["relationRegistry"]["relations"]
    if rel not in rels:
        errs.append(f"C2X: relation '{rel}' is not in the fact-plane registry")
    elif entry.get("resolution") not in rels[rel]["ladder"]:
        errs.append(f"C2X: resolution is not a rung of '{rel}'")
if rel in c["coverageKey"]["crossUniverseRelations"] and "targetUniverseId" not in entry:
    errs.append(f"C2X: cross-universe relation '{rel}' has no targetUniverseId")
return errs
""")


def _s_drop_coverage_root_guard(tree):
    return _replace_body(tree, "_coverage_root_ok", "return True")


def _s_drop_subject_scope_shape(tree):
    return _replace_body(tree, "_subject_scope_shape_ok", "return True")


def _s_drop_stage_kind_guard(tree):
    return _replace_body(tree, "_stage_kind_ok", "return True")


class _TupleToSet(ast.NodeTransformer):
    """Restore v3's set literals, where an unhashable container RAISED."""

    def visit_Tuple(self, node):
        self.generic_visit(node)
        literals = [e.value for e in node.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        if set(literals) == {"semantic-provider", "external-scanner"}:
            return ast.Set(elts=node.elts)
        return node


def _s_drop_stage_operator_guard(tree):
    """LB-C2-04 at the operator site.

    Removing the type guard alone is not a faithful falsifier while the
    membership tests use tuples, so this mutation also restores v3's set
    literals.  The break is then detected by the measured unguardedEscapes
    count on the stage-plan surface: a container operator RAISES again.
    """
    return ast.fix_missing_locations(
        _TupleToSet().visit(_replace_body(tree, "_stage_operator_ok", "return True")))


def _s_bare_coverage_schema_version(tree):
    return _replace_body(tree, "_coverage_schema_version_ok", "return value == 1")


SOURCE_MUTATIONS = [
    ("restore the bare schemaVersion equality at the PlanIntent position",
     _s_bare_schema_version),
    ("restore the bare schemaVersion equality at the descriptor position",
     _s_bare_descriptor_schema_version),
    ("restore the bare planSchemaMajor equality", _s_bare_plan_schema_major),
    ("restore the bare Coverage schemaVersion equality", _s_bare_coverage_schema_version),
    ("restore the truthiness short-circuit on relation", _s_truthy_relation),
    ("remove the Coverage root-shape guard", _s_drop_coverage_root_guard),
    ("drop the subjectScopeCommitment shape check", _s_drop_subject_scope_shape),
    ("remove the stage kind type guard", _s_drop_stage_kind_guard),
    ("remove the stage operator type guard", _s_drop_stage_operator_guard),
]


def _execute_tree(tree):
    module = types.ModuleType("opensip_c2v4_mutated")
    module.__file__ = str(pathlib.Path(__file__).resolve())
    exec(compile(tree, module.__file__, "exec"), module.__dict__)
    return module


def _s_inject_bare_comparison(tree):
    """The scan itself must report a newly introduced bare numeric comparison."""
    subject = copy.deepcopy(tree)
    injected = ast.parse('if intent.get("schemaVersion") == 1:\n    pass\n').body
    for node in subject.body:
        if isinstance(node, ast.FunctionDef) and node.name == "_validate_plan_intent":
            node.body = injected + node.body
            return ast.fix_missing_locations(subject)
    raise AuthorityLoadError("cannot find _validate_plan_intent to mutate")


def _s_drop_coverage_boundary(tree):
    """The total-boundary scan must report a validator that lost its boundary."""
    return _replace_body(tree, "validate_coverage", "return _validate_coverage(entry, c, fp)")


SCAN_MUTATIONS = [
    ("inject a bare numeric comparison into the checker's own syntax tree",
     _s_inject_bare_comparison, integer_guard_scan, "unguardedNumericComparisons"),
    ("remove a public validator's named-finding boundary",
     _s_drop_coverage_boundary, total_boundary_scan, "unguardedDispatches"),
]


def run_contract_mutations(base, authority, report):
    escaped = []
    for name, mutate in CONTRACT_MUTATIONS:
        candidate = copy.deepcopy(base)
        try:
            mutate(candidate)
        except Exception as exc:                        # noqa: BLE001 - reported
            escaped.append(f"{name}: mutation could not be applied ({type(exc).__name__})")
            continue
        findings = check(candidate, authority)
        if not findings:
            escaped.append(f"{name}: NO FINDING — the mutation survived")
        report(bool(findings), name,
               findings[0] if findings else "NO FINDING — mutation survived")
    return escaped


def run_source_mutations(base, authority, tree, report):
    escaped = []
    for name, mutate in SOURCE_MUTATIONS:
        try:
            module = _execute_tree(mutate(tree))
            findings = module.check(copy.deepcopy(base), authority)
        except Exception as exc:                        # noqa: BLE001 - reported
            findings = [f"mutated checker raised {type(exc).__name__}: {exc}"]
        if not findings:
            escaped.append(f"{name}: NO FINDING — the broken guard was not detected")
        report(bool(findings), name,
               findings[0] if findings else "NO FINDING — broken guard undetected")
    for name, mutate, scan, key in SCAN_MUTATIONS:
        try:
            broken = scan(mutate(tree))[key]
            clean = scan(tree)[key]
        except Exception as exc:                        # noqa: BLE001 - reported
            broken, clean = 0, f"scan raised {type(exc).__name__}: {exc}"
        detected = is_wire_int(broken) and broken > 0 and clean == 0
        if not detected:
            escaped.append(f"{name}: the scan reported {broken!r} on the broken tree and "
                           f"{clean!r} on the clean tree")
        report(detected, name,
               f"scan reports {broken} broken site(s) and {clean} on the unmutated tree")
    return escaped


def run_generator_narrowing(base, authority, relations, fp, values, intent_values):
    """Prove the leaf-inclusive enumeration is load-bearing, not decorative.

    Narrowing the generator back to container-only positions - exactly the shape
    v3's instrument had - must lose every scalar leaf and make the published
    counts detectably wrong.
    """
    escapes = []
    valid_intents = [intent_values[fx["id"]] for fx in base.get("planIntentFixtures", [])
                     if fx.get("valid") and fx.get("id") in intent_values]
    wide, _ = drive_surface(valid_intents, values,
                            lambda x: _validate_plan_intent(x, base, relations),
                            lambda x: validate_plan_intent(x, base, relations))
    narrow, _ = drive_surface(valid_intents, values,
                              lambda x: _validate_plan_intent(x, base, relations),
                              lambda x: validate_plan_intent(x, base, relations),
                              leaves=False)
    if narrow["scalarLeafPaths"]:
        escapes.append("the container-only enumeration still reports scalar leaf positions")
    if not wide["scalarLeafPaths"]:
        escapes.append("the leaf-inclusive enumeration reports no scalar leaf position")
    if narrow["enumeratedPaths"] >= wide["enumeratedPaths"]:
        escapes.append("narrowing the generator did not shrink the enumerated space")
    return {"widePaths": wide["enumeratedPaths"], "wideLeaves": wide["scalarLeafPaths"],
            "narrowPaths": narrow["enumeratedPaths"], "escapes": escapes}


TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"), ("null", None), ("list", []), ("empty-object", {}),
)


def selftest(candidate, authority, path):
    """Always reaches the suite; refuses a dirty base with a distinct code."""
    base_findings = check(candidate, authority)
    if base_findings:
        print("SELFTEST-REFUSED: the base candidate is not clean, so the mutation suite "
              "is not an oracle over it — every row would echo the pre-existing failure "
              "and report 'all rejected'.")
        print(f"  dirty base: {len(base_findings)} finding(s) in {path.name}")
        for finding in base_findings[:10]:
            print("  base-finding:", finding)
        if len(base_findings) > 10:
            print(f"  ... {len(base_findings) - 10} further base finding(s)")
        print(f"SELFTEST-NOT-RUN: 0 of {len(CONTRACT_MUTATIONS) + len(SOURCE_MUTATIONS) + len(SCAN_MUTATIONS)} "
              "mutations executed. Exit 3 distinguishes this refusal from a green "
              "selftest (0), from ordinary findings (1) and from a bad invocation (2), "
              "and can never be absorbed into a pass.")
        return 3
    # Captured from the CLEAN base before any mutation runs: every later
    # check() call overwrites the live measurement with a mutated one.
    clean_surfaces = authority.census or {}
    print(f"C-2 v4 mutation self-test over {path.name} — each row must be REJECTED\n")
    escaped = []
    rows = 0

    def report(rejected, name, detail):
        nonlocal rows
        rows += 1
        print(f"  {'reject' if rejected else 'ESCAPE':>6}  {name}")
        print(f"          {detail}")

    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), authority)
        if not findings:
            escaped.append(f"parsed-JSON root {name}: NO FINDING")
        report(bool(findings), f"parsed-JSON contract root {name}",
               findings[0] if findings else "NO FINDING — root survived")
    for case in candidate["coverageKey"].get("rootTotalityCases", []):
        findings = validate_coverage(case.get("value"), c=candidate,
                                     fp=authority.json(FP))
        named = bool(findings) and str(findings[0]).startswith("C2X-ROOT:")
        if not named:
            escaped.append(f"Coverage root {case.get('id')}: no named C2X-ROOT finding")
        report(named, f"hostile Coverage root {case.get('id')} (LB-C2-02)",
               findings[0] if findings else "NO FINDING — hostile root survived")
    escaped.extend(run_contract_mutations(candidate, authority, report))
    tree = _own_tree()
    escaped.extend(run_source_mutations(candidate, authority, tree, report))

    relations = set(authority.json(FP)["relationRegistry"]["relations"])
    intent_values, _ = _intent_fixture_values(candidate)
    values = _matrix_values(candidate["planIntentTotalityMatrix"])
    narrowing = run_generator_narrowing(candidate, authority, relations,
                                        authority.json(FP), values, intent_values)
    escaped.extend(narrowing["escapes"])
    report(not narrowing["escapes"], "narrow the leaf-inclusive generator back to "
           "container positions (v3's instrument)",
           f"leaf-inclusive reaches {narrowing['widePaths']} paths including "
           f"{narrowing['wideLeaves']} scalar leaves; container-only reaches "
           f"{narrowing['narrowPaths']} paths and 0 scalar leaves")

    root_census, root_stats = measure_contract_root(candidate, authority, execute=True)
    # Only the GUARDED count is the declared property at this surface, and the
    # candidate says so in contractRoot.unguardedEscapesRule.  The unguarded
    # number is published because refusing to state it is exactly the coverage
    # claim over an unobserved region this corpus keeps shipping.
    contract_ok = not root_stats["guardedEscapes"]
    if not contract_ok:
        escaped.append(f"contract-root matrix: {root_stats['guardedEscapes']} case(s) "
                       "escaped the guarded CLI boundary as a traceback")
    report(contract_ok, "hostile parsed JSON at every contract-root position "
           "including scalar leaves",
           f"{root_stats['executedCases']} cases over {root_census['enumeratedPaths']} "
           f"paths ({root_census['scalarLeafPaths']} scalar leaves); "
           f"{root_stats['guardedEscapes']} guarded escapes over "
           f"{root_stats['guardedExercised']} guarded exercises "
           f"(REQUIRED zero); {root_stats['unguardedEscapes']} unguarded inner-reader "
           "raises (REPORTED, not required zero — see contractRoot.unguardedEscapesRule)")

    print()
    if escaped:
        for item in escaped:
            print("SELFTEST-FAIL:", item)
        print(f"{len(escaped)}/{rows} retained cases ESCAPED — the proof path is optional")
        return 1
    surfaces = clean_surfaces
    print(f"SELFTEST-PASS: all {rows} retained cases rejected — the proof path is "
          "load-bearing")
    for name in sorted(surfaces):
        census = surfaces[name]["census"]
        stats = surfaces[name]["stats"]
        print(f"  {name}: {census['enumeratedPaths']} paths "
              f"({census['scalarLeafPaths']} scalar leaves, "
              f"{census['containerPaths']} containers), {stats['executedCases']} executed "
              f"cases, {stats['guardedEscapes']} guarded escapes, "
              f"{stats['unguardedEscapes']} unguarded escapes, "
              f"{stats['silentAccepts']} silent accepts")
    print(f"  contract-root: {root_census['enumeratedPaths']} paths "
          f"({root_census['scalarLeafPaths']} scalar leaves), "
          f"{root_stats['executedCases']} executed cases, "
          f"{root_stats['guardedEscapes']} guarded escapes over "
          f"{root_stats['guardedExercised']} guarded exercises, "
          f"{root_stats['unguardedEscapes']} unguarded inner-reader raises "
          "(reported, not required zero: a contract document is an authoring "
          "artifact, not caller-controlled input — the three wire-request "
          "surfaces above are total UNGUARDED as well)")
    print("  scope: checker-scope evidence only; SPECIFIED / IMPLEMENTABLE_UNEXECUTED; "
          "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW; independent re-review "
          "REQUIRED; no seal, freeze, integration or product acceptance")
    return 0


def _parse_argv(argv):
    flags, positional = set(), []
    for arg in argv[1:]:
        if arg in DECLARED_FLAGS:
            flags.add(arg)
        elif isinstance(arg, str) and arg.startswith("-"):
            raise UnsupportedInvocation(f"unknown flag {arg!r}; declared flags are "
                                        f"{list(DECLARED_FLAGS)}")
        else:
            positional.append(arg)
    if len(positional) > 1:
        raise UnsupportedInvocation("at most one contract path may be supplied")
    return flags, (positional[0] if positional else None)


def main(argv):
    try:
        flags, requested = _parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"C2V4-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    try:
        authority = load_authority()
    except AuthorityLoadError as exc:
        print(f"C2V4-PINNED-INPUT-REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        candidate = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"cannot load C-2 v4 candidate {path}: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in flags:
        return selftest(candidate, authority, path)
    findings = check(candidate, authority)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for item in findings:
            print("  -", item)
        return 1
    surfaces = authority.census or {}
    root = authority.contract_census or {}
    paths = sum(s["census"]["enumeratedPaths"] for s in surfaces.values())
    leaves = sum(s["census"]["scalarLeafPaths"] for s in surfaces.values())
    cases = sum(s["stats"]["executedCases"] for s in surfaces.values())
    print(f"C-2 v4 contract OK — {path.name}, "
          f"{len(candidate['planIntentFixtures'])} PlanIntent + "
          f"{len(candidate['intentBindingFixtures'])} analysis binding + "
          f"{len(candidate['storedViewBindingFixtures'])} stored binding + "
          f"{len(candidate['planFixtures'])} stage-plan + "
          f"{len(candidate['coverageFixtures'])} coverage fixtures; "
          f"I1..I4/C1X/C2X/C2DL/C2PV/C2I-TM/C2I-OP/C2I-RI/C3X/P1..P5 clean")
    print(f"  {len(PINS)} inputs hash-verified before execution; the pinned v3 checker "
          f"{V3_CHECKER} was executed from its verified snapshot and independently "
          "reproduced all 7 planIntentCommitment vectors unchanged")
    print(f"  hostile parsed JSON driven at EVERY position including scalar leaves: "
          f"{cases} executed cases over {paths} enumerated fixture paths of which "
          f"{leaves} are scalar leaves; 0 guarded escapes, 0 admit-then-raise, "
          "0 type-distinct constant admissions")
    print(f"  contract-root space measured at {root.get('enumeratedPaths')} paths of which "
          f"{root.get('scalarLeafPaths')} are scalar leaves; its execution matrix runs "
          "under --selftest (RES-C2V4-05)")
    print("  scope: checker-scope evidence only; SPECIFIED / IMPLEMENTABLE_UNEXECUTED; "
          "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW; no seal, freeze, "
          "integration or product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
