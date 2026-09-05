#!/usr/bin/env python3
"""Evidence v9 successor checker: recomputed identity over a rejected v8.

evidence.v8 was independently REJECTED with eight blocking findings.  The
reviewer established that the v8 CONTENT is sound and that every defect is an
ENFORCEMENT gap.  This checker keeps the content and closes the enforcement:

  EV8-IR-01  the three v8 TODOs are closed on merit against artifacts that
             passed independent review after v8 was authored (D9 v1.13,
             retention-tiers v22, trusted-request-context v3).
  EV8-IR-02  the complete expected successor object is DERIVED from the pinned
             predecessor bytes plus the pinned dependency bytes and compared
             for exact equality, so every leaf is derived rather than declared.
  EV8-IR-03  SemanticEvidenceV1 is re-encoded under the tag table declared by
             the candidate's own canonicalWireGrammar, and universeCommitment,
             outcomeSetCommitment and verdictDerivationCommitment are bound by
             equality to the accepted EP8 vector's bundle.
  EV8-IR-04  RawProofInventoryV1 is projected from the pinned retention
             closure's proofRefs and required to equal both acceptedGolden and
             the inventory embedded inside SemanticEvidenceV1.
  EV8-IR-05  every d9Mapping row is produced by calling the live D9 v1.13
             reference derivation; no class, code or exit code is authored.
  EV8-IR-06  --selftest always reaches the mutation suite, and refuses to run
             against a dirty base with a distinct exit code.
  EV8-IR-07  every schema node is type-guarded; hostile parsed JSON returns
             findings and never a traceback.
  EV8-IR-08  EV7-PF-01..08 / R01..R03 and EV8-IR-01..08 / R1..R6 each carry an
             explicit disposition whose id set is read from the pinned review
             files, and no disposition may claim closure without naming an
             executed probe that actually ran in this invocation.

Trust root: caller-owned ``python3 -I -B``.  Every pinned byte string is
hash-verified BEFORE any of it is parsed or executed.

Authorship: CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW.  A green run
of this authored checker is checker-scope evidence ONLY.  It declares no seal,
no freeze, no integration and no product acceptance, and it does not sign
CD-RT-5.

Supported usage only:
  python3 -I -B artifacts/check-evidence-v9.py [candidate] [--selftest]
  python3 -I -B artifacts/check-evidence-v9.py --emit-candidate
Exit: 0 clean; 1 findings; 2 unsupported invocation/input; 3 selftest refused
      because the base candidate is not clean.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "EV9-UNSUPPORTED-INVOCATION: caller must use "
    "python3 -I -B artifacts/check-evidence-v9.py"
)
if sys.flags.isolated != 1 or not sys.flags.dont_write_bytecode:
    print(_STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import types
from contextlib import redirect_stdout
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evidence.v9.json"
CHECKER = "check-evidence-v9.py"

PREDECESSOR = "evidence.v8.json"
PREDECESSOR_CHECKER = "check-evidence-v8.py"
PREDECESSOR_REVIEW = "evidence.v8.review-independent-prefreeze.json"
V7 = "evidence.v7.json"
V7_CHECKER = "check-evidence-v7.py"
V7_REVIEW = "evidence.v7.review-adversarial-prefreeze-rejected.json"
V4_CHECKER = "check-evidence-v4.py"
EP8 = "evaluation-proof.v8.json"
EP8_CHECKER = "check-evaluation-proof-v8.py"
EP8_REVIEW = "ep8-rt13.review-independent-cold-reconstruction.json"
RT22 = "retention-tiers.v22.json"
RT22_CHECKER = "check-retention-custody-v22.py"
RT22_REVIEW = "retention-tiers.v22.review-independent-prefreeze.json"
RT13 = "retention-tiers.v13.json"
RT13_CHECKER = "check-retention-custody-v13.py"
RT_CORE = "check-retention-custody.py"
D9 = "d9-exit-contract.v1.13.json"
D9_CHECKER = "check-d9-v1.13.py"
D9_REVIEW = "d9-exit-contract.v1.13.review-independent-prefreeze.json"
TRC3 = "trusted-request-context.v3.json"
TRC3_CHECKER = "check-trusted-request-context-v3.py"
TRC3_REVIEW = "trusted-request-context.v3.review-independent-prefreeze.json"
VERSIONING = "versioning-policy.v8.json"
VERSIONING_CHECKER = "check-versioning-v8.py"

PINS: dict[str, str] = {
    PREDECESSOR:
        "4ef262d156a0c66d9cefef4c2fd5c1b80883b5573164754558a42ed139f3921c",
    PREDECESSOR_CHECKER:
        "0771f3e1079b99b8e28f6b7a7154c722d2195ba5142e91f350438a2eae7ae525",
    PREDECESSOR_REVIEW:
        "ad07b4ae3f5c5fa8886ea1b838373e0b5d134dfcc5ab5e894c1e3d7c86f9b7f0",
    V7: "157da8cf2b44fd72794ee2c7c3dedfa30745164798c45a8d21e08094a128c356",
    V7_CHECKER:
        "9fd858b1c59f064dd9693ba3c6d2d935fc462f0833078cc2eb5bc26cc4009524",
    V7_REVIEW:
        "5a98de124ffd0ab1b47e148d13b5f8e9dbab549fb8e62e02b37a8066ba09ab2d",
    V4_CHECKER:
        "fd8db2ab77261ba31351d0647cf62ba4de92db35ba7a15426cb8f4bcf28865bc",
    EP8: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    EP8_CHECKER:
        "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    EP8_REVIEW:
        "f4599b32a9f1b93049111b9e86debd19419902c9c5f4fb886f8d0dc9c330567e",
    RT22: "52aa540df75a047f0abc09b4fab4b472ab2934ad1f488146bb370ed6050743e1",
    RT22_CHECKER:
        "497909c21118b656d222346d9498b7a9cac34ef3dd3bb0f29ef59c0db90e1c5c",
    RT22_REVIEW:
        "a30e84cbc67e25a2da231d0204202755c9ee2e3baf3bd0dc48039f4a8bc38600",
    RT13: "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    RT13_CHECKER:
        "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    RT_CORE:
        "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    D9: "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    D9_CHECKER:
        "a905ab0e4b932c2ef4c565e847a12cb398abf9cd7a74abd92f95cbc85ffc8717",
    D9_REVIEW:
        "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
    TRC3: "bc53c2679a977fd2c2c8369ec9d5794f2295b0df5100b1e360a42c155d04008a",
    TRC3_CHECKER:
        "0c96564d2027a6f178a4b88d3442dda1ba2beec7790e2c05fd31da1dce9473ad",
    TRC3_REVIEW:
        "f0c58f34cfc391a35b51dcfda0003c98a5eaa53d0fc9ae7526a84c378c5ae811",
    VERSIONING:
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    VERSIONING_CHECKER:
        "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
}

ROLES: dict[str, str] = {
    PREDECESSOR: "rejected v8 candidate; carried root values and predecessor identity",
    PREDECESSOR_CHECKER: "retained executable v8 foundation suite",
    PREDECESSOR_REVIEW: "independent v8 REJECT whose eight blocking findings this successor answers",
    V7: "v7 lineage referenced by the v8 supersedes chain",
    V7_CHECKER: "retained v7 checker",
    V7_REVIEW: "independent v7 REJECT whose EV7-PF finding ids this successor disposes",
    V4_CHECKER: "retained independent wire-encoding implementation used as a cross-implementation control",
    EP8: "accepted evaluation-authority vector and proof bundle",
    EP8_CHECKER: "executable EP8 authority",
    EP8_REVIEW: "independent PASS of the EP8/RT13 cold reconstruction root",
    RT22: "independently accepted retention successor supplying the semantic capability closure",
    RT22_CHECKER: "executable RT22 authority",
    RT22_REVIEW: "independent PASS of retention-tiers.v22",
    RT13: "declared exact semantic basis of RT22; required by the retained v8 foundation",
    RT13_CHECKER: "executable RT13 authority required by the retained v8 foundation",
    RT_CORE: "retention core derivation required by the retained v8 foundation",
    D9: "independently accepted host termination contract",
    D9_CHECKER: "live D9 v1.13 reference derivation",
    D9_REVIEW: "independent PASS of d9-exit-contract.v1.13",
    TRC3: "independently accepted TrustedRequestContext construction authority",
    TRC3_CHECKER: "executable request-context authority",
    TRC3_REVIEW: "independent PASS of trusted-request-context.v3",
    VERSIONING: "versioning policy dependency",
    VERSIONING_CHECKER: "executable versioning authority",
}

# Pinned reviews and the exact verdict each one must carry.  A dependency is
# admitted only when its own independent review is the exact decision below.
REVIEW_BINDINGS: dict[str, dict[str, Any]] = {
    PREDECESSOR_REVIEW: {"decision": "REJECT", "blockingFindingCount": 8},
    V7_REVIEW: {"decision": "REJECT", "blockingFindingCount": 8},
    RT22_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
    D9_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
    TRC3_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
    EP8_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
}


class DuplicateKeyError(ValueError):
    """A JSON object repeated a key; the document is not canonical."""


class AuthorityLoadError(RuntimeError):
    """A pinned input could not be admitted as authority."""


class PinMismatch(AuthorityLoadError):
    """A pinned byte string does not hash to its declared digest."""


class Malformed(Exception):
    """A candidate-driven layer met a shape it cannot consume."""


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def _parse_json_bytes(source: bytes, name: str) -> Any:
    try:
        return json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise AuthorityLoadError(
            f"cannot parse pinned data {name}: {type(exc).__name__}: {exc}"
        ) from exc


def load_source(path: pathlib.Path) -> tuple[Any, bytes]:
    source = path.read_bytes()
    return _parse_json_bytes(source, path.name), source


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha_ref(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


class _VerifiedSourceLoader:
    """Execute exactly the bytes that were hash-verified, never a re-read."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec: Any) -> None:
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_snapshot(name: str, filename: str,
                      source: bytes) -> types.ModuleType:
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

    def __init__(self, snapshots: Mapping[str, bytes],
                 parsed: Mapping[str, Any],
                 modules: Mapping[str, types.ModuleType]):
        self.snapshots = snapshots
        self.parsed = parsed
        self.modules = modules
        self.probe_log: dict[str, bool] = {}

    def json(self, name: str) -> Any:
        return self.parsed[name]

    def module(self, name: str) -> types.ModuleType:
        return self.modules[name]

    def record_probe(self, probe_id: str, passed: bool) -> bool:
        prior = self.probe_log.get(probe_id)
        self.probe_log[probe_id] = passed if prior is None else (prior and passed)
        return passed


class DeferredAuthorityLoader:
    """Hash-before-execution: verify every pinned byte string, then execute."""

    EXECUTABLES = (
        PREDECESSOR_CHECKER, V4_CHECKER, D9_CHECKER, TRC3_CHECKER,
        RT22_CHECKER, EP8_CHECKER, VERSIONING_CHECKER,
    )

    def __init__(self, directory: pathlib.Path = HERE):
        self.directory = directory

    def snapshots(self, byte_reader: Callable[[pathlib.Path], bytes] | None = None
                  ) -> dict[str, bytes]:
        reader = byte_reader or (lambda path: path.read_bytes())
        collected: dict[str, bytes] = {}
        errors: list[str] = []
        for name, expected in PINS.items():
            try:
                source = reader(self.directory / name)
            except (OSError, TypeError, ValueError) as exc:
                errors.append(f"{name}: read {type(exc).__name__}: {exc}")
                continue
            if not isinstance(source, bytes):
                errors.append(f"{name}: reader returned {type(source).__name__}")
                continue
            actual = hashlib.sha256(source).hexdigest()
            if actual != expected:
                errors.append(f"{name}: {actual} != {expected}")
                continue
            collected[name] = source
        if errors:
            raise PinMismatch("; ".join(sorted(errors)))
        if set(collected) != set(PINS):
            raise PinMismatch("not every pinned input produced a snapshot")
        return collected

    @staticmethod
    def parse(snapshots: Mapping[str, bytes]) -> dict[str, Any]:
        parsed = {name: _parse_json_bytes(snapshots[name], name)
                  for name in PINS if name.endswith(".json")}
        for name, expected in REVIEW_BINDINGS.items():
            review = parsed.get(name)
            if not isinstance(review, dict):
                raise AuthorityLoadError(f"pinned review {name} is not an object")
            verdict = review.get("verdict")
            if not isinstance(verdict, dict):
                raise AuthorityLoadError(f"pinned review {name} has no verdict object")
            decision = verdict.get("decision", review.get("decision"))
            if decision != expected["decision"]:
                raise AuthorityLoadError(
                    f"pinned review {name} decision {decision!r} != "
                    f"{expected['decision']!r}")
            blockers = verdict.get("blockingFindings")
            count = verdict.get("blockingFindingCount")
            if count is None and isinstance(blockers, list):
                count = len(blockers)
            if count != expected["blockingFindingCount"]:
                raise AuthorityLoadError(
                    f"pinned review {name} blocking count {count!r} != "
                    f"{expected['blockingFindingCount']!r}")
        return parsed

    def load(self) -> Authority:
        snapshots = self.snapshots()
        parsed = self.parse(snapshots)
        modules: dict[str, types.ModuleType] = {}
        for filename in self.EXECUTABLES:
            module_name = "opensip_ev9_verified_" + \
                filename.replace("-", "_").replace(".", "_")
            sink = io.StringIO()
            with redirect_stdout(sink):
                modules[filename] = _execute_snapshot(
                    module_name, filename, snapshots[filename])
        return Authority(snapshots, parsed, modules)


# The eager bootstrap is reached only after the caller-owned isolated-start
# guard.  Every retained source byte is verified before it executes.
_BOOTSTRAP_AUTHORITY = DeferredAuthorityLoader().load()


# ---------------------------------------------------------------------------
# Section 1.  Grammar-driven wire codec.
#
# The tag table is read from a canonicalWireGrammar object rather than from a
# constant in this source, so the grammar is mechanically consumed.  Mutating
# any recordTag, field tag, field name or field order changes the derived bytes
# and therefore the EvidenceDigest, the RunId and the runSealRef.
# ---------------------------------------------------------------------------

GRAMMAR_RECORD_ORDER = (
    "RawProofInventoryItemV1", "RawProofInventoryV1", "SemanticEvidenceV1",
    "RunIdentityPreimageV1", "TerminalRunV1",
)
DOMAIN_SEMANTIC_EVIDENCE = "opensip.semantic-evidence.v1"
DOMAIN_RUN_ID = "opensip.run-id.v1"
ITEM_WRAPPER_TAG = 0x8B
SET_SORT_RULE = ("sort complete item record bytes unsigned; reject duplicates "
                 "instead of silently deduplicating")


def _tag(text: Any, where: str) -> int:
    if not isinstance(text, str) or not re.fullmatch(r"0x[0-9a-f]{2}", text):
        raise Malformed(f"{where}: tag {text!r} is not a canonical 0xNN literal")
    return int(text, 16)


def _frame(tag: int, value: Any) -> bytes:
    if isinstance(value, bool):
        raise Malformed("booleans have no canonical scalar encoding")
    if isinstance(value, int):
        payload = str(value).encode("ascii")
    elif isinstance(value, str):
        payload = value.encode("utf-8")
    elif isinstance(value, (bytes, bytearray)):
        payload = bytes(value)
    else:
        raise Malformed(f"no canonical encoding for {type(value).__name__}")
    return bytes([tag]) + len(payload).to_bytes(4, "big") + payload


def _record(tag: int, parts: list[bytes]) -> bytes:
    return bytes([tag]) + b"".join(parts)


class WireCodec:
    """Encoder built from a canonicalWireGrammar object."""

    def __init__(self, grammar: Any):
        if not isinstance(grammar, dict):
            raise Malformed("canonicalWireGrammar is not an object")
        records = grammar.get("records")
        if not isinstance(records, dict):
            raise Malformed("canonicalWireGrammar.records is not an object")
        if tuple(records) != GRAMMAR_RECORD_ORDER:
            raise Malformed(
                "canonicalWireGrammar.records key order/content is not the "
                f"closed set {list(GRAMMAR_RECORD_ORDER)}")
        self.record_tag: dict[str, int] = {}
        self.fields: dict[str, list[tuple[str, int]]] = {}
        for name in GRAMMAR_RECORD_ORDER:
            spec = records.get(name)
            if not isinstance(spec, dict):
                raise Malformed(f"records.{name} is not an object")
            self.record_tag[name] = _tag(spec.get("recordTag"), f"records.{name}")
            fields = spec.get("fields")
            if not isinstance(fields, list) or not fields:
                raise Malformed(f"records.{name}.fields is not a non-empty array")
            ordered: list[tuple[str, int]] = []
            for index, field in enumerate(fields):
                if not isinstance(field, dict):
                    raise Malformed(f"records.{name}.fields[{index}] is not an object")
                field_name = field.get("name")
                if not isinstance(field_name, str) or not field_name:
                    raise Malformed(f"records.{name}.fields[{index}].name is not text")
                ordered.append((field_name, _tag(
                    field.get("tag"), f"records.{name}.fields[{index}]")))
            required = spec.get("required")
            if not isinstance(required, list) or \
                    [item for item, _ in ordered] != required:
                raise Malformed(
                    f"records.{name}.required does not equal its field order")
            self.fields[name] = ordered
        envelope = grammar.get("domainEnvelope")
        if not isinstance(envelope, dict):
            raise Malformed("canonicalWireGrammar.domainEnvelope is not an object")
        self.envelope_tag = _tag(envelope.get("recordTag"), "domainEnvelope")
        envelope_fields = envelope.get("fields")
        if not isinstance(envelope_fields, list) or len(envelope_fields) != 2:
            raise Malformed("domainEnvelope.fields must declare exactly two fields")
        names = []
        tags = []
        for index, field in enumerate(envelope_fields):
            if not isinstance(field, dict):
                raise Malformed(f"domainEnvelope.fields[{index}] is not an object")
            names.append(field.get("name"))
            tags.append(_tag(field.get("tag"), f"domainEnvelope.fields[{index}]"))
        if names != ["domain", "payload"]:
            raise Malformed("domainEnvelope fields are not [domain, payload]")
        self.domain_tag, self.payload_tag = tags
        rules = grammar.get("recordRules")
        if not isinstance(rules, dict) or rules.get("sets") != SET_SORT_RULE:
            raise Malformed("recordRules.sets does not declare the exact set rule")
        registry = grammar.get("tagRegistry")
        if not isinstance(registry, list):
            raise Malformed("canonicalWireGrammar.tagRegistry is not an array")
        seen: set[int] = set()
        self.registry: dict[int, str] = {}
        for index, row in enumerate(registry):
            if not isinstance(row, dict):
                raise Malformed(f"tagRegistry[{index}] is not an object")
            value = _tag(row.get("tag"), f"tagRegistry[{index}]")
            if value in seen:
                raise Malformed(f"tagRegistry[{index}] repeats tag {row.get('tag')}")
            seen.add(value)
            role = row.get("role")
            if not isinstance(role, str) or not role:
                raise Malformed(f"tagRegistry[{index}].role is not text")
            self.registry[value] = role
        declared = {self.envelope_tag, self.domain_tag, self.payload_tag,
                    ITEM_WRAPPER_TAG}
        for name in GRAMMAR_RECORD_ORDER:
            declared.add(self.record_tag[name])
            declared.update(tag for _, tag in self.fields[name])
        missing = sorted(declared - seen)
        if missing:
            raise Malformed(
                "tagRegistry omits tags used by the record table: "
                + ", ".join(f"0x{value:02x}" for value in missing))

    def emit(self, name: str, values: Mapping[str, Any]) -> bytes:
        parts = []
        for field_name, tag in self.fields[name]:
            if field_name not in values:
                raise Malformed(f"{name}.{field_name} has no value to encode")
            parts.append(_frame(tag, values[field_name]))
        return _record(self.record_tag[name], parts)

    def envelope(self, domain: str, payload: bytes) -> bytes:
        return _record(self.envelope_tag, [
            _frame(self.domain_tag, domain), _frame(self.payload_tag, payload)])

    def inventory_items(self, proof_refs: Any,
                        sort_wrappers: bool = False) -> bytes:
        if not isinstance(proof_refs, list) or not proof_refs:
            raise Malformed("proofRefs is not a non-empty array")
        encoded: list[bytes] = []
        for index, row in enumerate(proof_refs):
            if not isinstance(row, dict):
                raise Malformed(f"proofRefs[{index}] is not an object")
            for key in ("recordCasRef", "recordKind", "requiredForCapability"):
                if not isinstance(row.get(key), str) or not row[key]:
                    raise Malformed(f"proofRefs[{index}].{key} is not text")
            encoded.append(self.emit("RawProofInventoryItemV1", row))
        if len(set(encoded)) != len(encoded):
            raise Malformed("proofRefs contains duplicate item record bytes")
        if sort_wrappers:
            return b"".join(sorted(
                _frame(ITEM_WRAPPER_TAG, item) for item in encoded))
        return b"".join(_frame(ITEM_WRAPPER_TAG, item)
                        for item in sorted(encoded))


RUN_SUBSTITUTIONS: tuple[tuple[str, dict[str, Any]], ...] = (
    ("RUN-SUB-SCHEMA-MAJOR", {"schemaMajor": 2}),
    ("RUN-SUB-PROJECT", {"projectId": "prj1-" + "b" * 64}),
    ("RUN-SUB-PLAN", {"planId": "plan1:sha256:" + "b" * 64}),
    ("RUN-SUB-AUTHORITY", {"evaluationAuthoritySealRef": "sha256:" + "c" * 64}),
    ("RUN-SUB-EVIDENCE", {"evidenceDigest": "sha256:" + "d" * 64}),
    ("RUN-SUB-CAPABILITY", {"sealedCapability": "verifiable"}),
)


def accepted_vector(ep8: Any) -> dict[str, Any]:
    if not isinstance(ep8, dict):
        raise Malformed("evaluation-proof root is not an object")
    vector_id = ep8.get("acceptedAuthorityVectorId")
    if not isinstance(vector_id, str) or not vector_id:
        raise Malformed("evaluation-proof acceptedAuthorityVectorId is not text")
    vectors = ep8.get("positiveVectors")
    if not isinstance(vectors, list):
        raise Malformed("evaluation-proof positiveVectors is not an array")
    rows = [row for row in vectors
            if isinstance(row, dict) and row.get("id") == vector_id]
    if len(rows) != 1:
        raise Malformed(
            f"evaluation-proof accepted vector {vector_id!r} is not unique")
    return rows[0]


def retention_closure(rt22: Any) -> dict[str, Any]:
    if not isinstance(rt22, dict):
        raise Malformed("retention root is not an object")
    projection = rt22.get("semanticBasisProjection")
    if not isinstance(projection, dict):
        raise Malformed("retention semanticBasisProjection is not an object")
    closure = projection.get("semanticCapabilityClosure")
    if not isinstance(closure, dict):
        raise Malformed("retention semanticCapabilityClosure is not an object")
    return closure


def derive_identity(grammar: Any, ep8: Any, rt22: Any) -> dict[str, Any]:
    """Recompute every published Evidence commitment from pinned dependencies.

    Nothing here reads acceptedGolden.  The result is what the golden must be.
    """
    codec = WireCodec(grammar)
    vector = accepted_vector(ep8)
    bundle = vector.get("bundle")
    candidate = vector.get("evaluationAuthorityCandidate")
    if not isinstance(bundle, dict) or not isinstance(candidate, dict):
        raise Malformed("accepted vector lacks bundle/evaluationAuthorityCandidate")
    seal = candidate.get("evaluationAuthoritySeal")
    universe = bundle.get("requiredUniverse")
    verdict_proof = bundle.get("verdictProof")
    if not isinstance(seal, dict) or not isinstance(universe, dict) or \
            not isinstance(verdict_proof, dict):
        raise Malformed("accepted vector authority/universe/verdictProof shape")
    closure = retention_closure(rt22)
    project = seal.get("projectId")
    if not isinstance(project, str) or \
            not re.fullmatch(r"prj1-[0-9a-f]{64}", project):
        raise Malformed("accepted authority projectId is not PROJECT-ID-V1")
    if bundle.get("projectId") != project or closure.get("projectId") != project:
        raise Malformed("bundle/closure ProjectId differs from the seal ProjectId")
    proof_refs = closure.get("proofRefs")
    if not isinstance(proof_refs, list):
        raise Malformed("retention closure proofRefs is not an array")
    for index, row in enumerate(proof_refs):
        if not isinstance(row, dict):
            raise Malformed(f"proofRefs[{index}] is not an object")
        if row.get("identityKind") != "raw-cas":
            raise Malformed(f"proofRefs[{index}] is not identityKind raw-cas")
        if row.get("projectId") != project:
            raise Malformed(f"proofRefs[{index}] crosses the Evidence project")

    inventory = codec.emit("RawProofInventoryV1", {
        "schemaVersion": 1, "projectId": project,
        "items": codec.inventory_items(proof_refs)})
    wrapper_sorted = codec.emit("RawProofInventoryV1", {
        "schemaVersion": 1, "projectId": project,
        "items": codec.inventory_items(proof_refs, sort_wrappers=True)})
    bundle_ref = sha_ref(canonical(bundle))
    closure_ref = sha_ref(canonical(closure))
    values = {
        "projectId": project,
        "planId": seal.get("planId"),
        "evaluationAuthoritySealRef": bundle.get("evaluationAuthoritySealRef"),
        "planIntentCommitment": seal.get("planIntentCommitment"),
        "executionPlanCommitment": seal.get("executionPlanCommitment"),
        "activationManifestRef": seal.get("activationManifestRef"),
        "evaluationProofBundleCasRef": bundle_ref,
        "universeCommitment": universe.get("universeCommitment"),
        "outcomeSetCommitment": verdict_proof.get("outcomeSetCommitment"),
        "verdictDerivationCommitment": verdict_proof.get("derivationCommitment"),
        "verdict": verdict_proof.get("verdict"),
        "sealedCapability": closure.get("sealedCapability"),
        "semanticCapabilityClosureCasRef": closure_ref,
        "semanticCapabilityClosureCommitment": closure.get("closureCommitment"),
    }
    for key, value in values.items():
        if not isinstance(value, str) or not value:
            raise Malformed(f"derived value {key} is not text")

    semantic = codec.emit("SemanticEvidenceV1", {
        "schemaVersion": 1,
        "projectId": project,
        "planId": values["planId"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "evaluationProofBundleCasRef": bundle_ref,
        "universeCommitment": values["universeCommitment"],
        "outcomeSetCommitment": values["outcomeSetCommitment"],
        "verdictDerivationCommitment": values["verdictDerivationCommitment"],
        "verdict": values["verdict"],
        "sealedCapability": values["sealedCapability"],
        "rawProofInventory": inventory,
        "semanticCapabilityClosureCasRef": closure_ref,
        "semanticCapabilityClosureCommitment":
            values["semanticCapabilityClosureCommitment"],
    })
    semantic_preimage = codec.envelope(DOMAIN_SEMANTIC_EVIDENCE, semantic)
    evidence_digest = sha_ref(semantic_preimage)
    run_values = {
        "schemaMajor": 1, "projectId": project, "planId": values["planId"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "evidenceDigest": evidence_digest,
        "sealedCapability": values["sealedCapability"],
    }
    run_record = codec.emit("RunIdentityPreimageV1", run_values)
    run_preimage = codec.envelope(DOMAIN_RUN_ID, run_record)
    run_id = "run1:" + hashlib.sha256(run_preimage).hexdigest()
    terminal = codec.emit("TerminalRunV1", {
        "schemaVersion": 1, "projectId": project, "runId": run_id,
        "planId": values["planId"],
        "planIntentCommitment": values["planIntentCommitment"],
        "executionPlanCommitment": values["executionPlanCommitment"],
        "activationManifestRef": values["activationManifestRef"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "semanticEvidenceCasRef": sha_ref(semantic),
        "evidenceDigest": evidence_digest,
        "verdict": values["verdict"],
        "sealedCapability": values["sealedCapability"],
        "semanticCapabilityClosureCasRef": closure_ref,
        "semanticCapabilityClosureCommitment":
            values["semanticCapabilityClosureCommitment"],
    })
    substitutions = []
    for identifier, mutation in RUN_SUBSTITUTIONS:
        mutated = dict(run_values)
        mutated.update(mutation)
        substitutions.append({
            "id": identifier,
            "mutation": copy.deepcopy(mutation),
            "expectedRunId": "run1:" + hashlib.sha256(codec.envelope(
                DOMAIN_RUN_ID,
                codec.emit("RunIdentityPreimageV1", mutated))).hexdigest(),
        })
    return {
        "codec": codec, "vector": vector, "bundle": bundle, "seal": seal,
        "closure": closure, "proofRefs": proof_refs, "values": values,
        "inventory": inventory, "inventoryWrapperSorted": wrapper_sorted,
        "semantic": semantic, "semanticPreimage": semantic_preimage,
        "evidenceDigest": evidence_digest, "runRecord": run_record,
        "runPreimage": run_preimage, "runId": run_id, "terminal": terminal,
        "runSealRef": sha_ref(terminal), "substitutions": substitutions,
    }


def golden_from_identity(previous_golden: Any,
                         derived: Mapping[str, Any]) -> dict[str, Any]:
    """Assemble acceptedGolden entirely from recomputed bytes.

    Only the two frozen historical labels (id, sourceVectorId) are carried from
    the predecessor; neither enters any encoded record or commitment.
    """
    if not isinstance(previous_golden, dict):
        raise Malformed("predecessor acceptedGolden is not an object")
    for key in ("id", "sourceVectorId", "runAuthorityIndex",
                "runAuthorityIndexRaw"):
        if key not in previous_golden:
            raise Malformed(f"predecessor acceptedGolden lacks {key}")
    return {
        "id": previous_golden["id"],
        "sourceVectorId": previous_golden["sourceVectorId"],
        "values": copy.deepcopy(dict(derived["values"])),
        "rawProofInventoryLength": len(derived["inventory"]),
        "rawProofInventoryHex": derived["inventory"].hex(),
        "semanticEvidenceLength": len(derived["semantic"]),
        "semanticEvidenceHex": derived["semantic"].hex(),
        "semanticEvidenceCasRef": sha_ref(derived["semantic"]),
        "evidenceDigestDomain": DOMAIN_SEMANTIC_EVIDENCE,
        "evidenceDigestPreimageLength": len(derived["semanticPreimage"]),
        "evidenceDigestPreimageHex": derived["semanticPreimage"].hex(),
        "evidenceDigest": derived["evidenceDigest"],
        "runIdentityRecordLength": len(derived["runRecord"]),
        "runIdentityRecordHex": derived["runRecord"].hex(),
        "runDomainPreimageLength": len(derived["runPreimage"]),
        "runDomainPreimageHex": derived["runPreimage"].hex(),
        "runId": derived["runId"],
        "terminalRunLength": len(derived["terminal"]),
        "terminalRunEncodedHex": derived["terminal"].hex(),
        "runSealRef": derived["runSealRef"],
        "runAuthorityIndex": copy.deepcopy(previous_golden["runAuthorityIndex"]),
        "runAuthorityIndexRaw": copy.deepcopy(
            previous_golden["runAuthorityIndexRaw"]),
    }


# ---------------------------------------------------------------------------
# Section 2.  Live D9 v1.13 termination derivation (EV8-IR-05, EV7-PF-04,
# EV7-PF-R02).  Every row below supplies only a situation and its exact fault
# axes.  Class, ordered code payload and exit code are produced by calling the
# pinned reference derivation.
# ---------------------------------------------------------------------------

D9_AXIS_DEFAULTS: dict[str, Any] = {
    "commandKind": "run",
    "admission": "admitted",
    "lifecycle": "pre-run",
    "requiredCoverage": "not-applicable",
    "verdict": "not-applicable",
    "durability": "not-applicable",
    "interruption": "none",
    "requiredPostconditions": "not-applicable",
    "domainCondition": "none",
    "deficiency": "none",
    "rejectionCause": "none",
    "faultCause": "none",
    "secondaryDeficiencies": [],
}


def _axes(**overrides: Any) -> dict[str, Any]:
    axes = copy.deepcopy(D9_AXIS_DEFAULTS)
    axes.update(overrides)
    return axes


_REJECTED = {"admission": "rejected", "lifecycle": "pre-run"}
_FAULTED = {"lifecycle": "cannot-seal-coherent-run",
            "domainCondition": "host-fault"}
_SETTLED = {"lifecycle": "coherent-terminal-run", "durability": "committed",
            "requiredPostconditions": "met", "requiredCoverage": "satisfied"}

D9_SITUATIONS: tuple[tuple[str, str, dict[str, Any]], ...] = (
    ("E9-D9-01-MALFORMED-BOUNDARY-INPUT",
     "A boundary request does not decode under its declared schema.",
     _axes(**_REJECTED, rejectionCause="config-invalid")),
    ("E9-D9-02-WELL-FORMED-PRECONDITION-SUBSTITUTION",
     "A well-formed request substitutes a value that fails an admission precondition.",
     _axes(**_REJECTED, rejectionCause="precondition-failed")),
    ("E9-D9-03-MISSING-RETENTION-DEFAULT-OR-UNSUPPORTED-TARGET",
     "No sealed retention target is supplied, or the supplied target is unsupported.",
     _axes(**_REJECTED, rejectionCause="unsatisfiable")),
    ("E9-D9-04-UNSUPPORTED-SCHEMA-MAJOR",
     "The request declares a schema major this host does not implement.",
     _axes(**_REJECTED, rejectionCause="schema-major-unsupported")),
    ("E9-D9-05-UNKNOWN-COMMITTED-RUN",
     "A read addresses a committed Run identity that this project has never published.",
     _axes(**_REJECTED, commandKind="query", rejectionCause="identity-unknown",
           domainCondition="addressed-identity-unresolved")),
    ("E9-D9-06-EXPIRED-COMMITTED-RUN",
     "A read addresses a committed Run identity with tombstone evidence of expiry.",
     _axes(**_REJECTED, commandKind="query", rejectionCause="identity-expired",
           domainCondition="addressed-identity-unresolved")),
    ("E9-D9-07-CAS-MATERIALIZATION-OR-LINK-FAILURE",
     "A required raw CAS object cannot be materialized or linked.",
     _axes(**_FAULTED, faultCause="cas-link")),
    ("E9-D9-08-HOST-IO-FAILURE",
     "The host durable medium fails an input/output operation.",
     _axes(**_FAULTED, faultCause="host-io")),
    ("E9-D9-09-FINAL-TRANSACTION-FAILURE",
     "The single final transaction that publishes all six Run-scoped records fails.",
     _axes(**_FAULTED, durability="failed", faultCause="durability-commit")),
    ("E9-D9-10-PERSISTED-HASH-OR-INDEX-MISMATCH",
     "A persisted record does not rehash to its stored ref, or an index disagrees with it.",
     _axes(**_FAULTED, faultCause="ledger-corrupt")),
    ("E9-D9-11-CONTENTION-TIMEOUT",
     "Serialized custody cannot be acquired inside the declared contention horizon.",
     _axes(**_FAULTED, faultCause="ledger-busy")),
    ("E9-D9-12-TRUSTED-DURABLE-STORE-RECONSTRUCTION-FAILURE",
     "Cold reconstruction of the trusted durable project state does not reproduce its own bytes.",
     _axes(**_FAULTED, faultCause="ledger-corrupt")),
    ("E9-D9-13-EVALUATION-PROOF-RECONSTRUCTION-FAILURE",
     "The stored evaluation proof bundle does not reproduce the admitted bundle CAS ref.",
     _axes(**_FAULTED, faultCause="ledger-corrupt")),
    ("E9-D9-14-RETENTION-CLOSURE-RECONSTRUCTION-FAILURE",
     "The stored semantic capability closure does not reproduce the admitted closure CAS ref.",
     _axes(**_FAULTED, faultCause="ledger-corrupt")),
    ("E9-D9-15-INDETERMINATE-VERDICT-NOT-ABSORBED",
     "The evaluation verdict is indeterminate on an otherwise coherent terminal Run.",
     _axes(**_SETTLED, verdict="indeterminate", deficiency="verdict-indeterminate")),
    ("E9-D9-16-REQUIRED-COVERAGE-UNSATISFIED",
     "A required relation is missing, so required coverage is unsatisfied.",
     _axes(**{**_SETTLED, "requiredCoverage": "unsatisfied"},
           deficiency="required-relation-missing")),
    ("E9-D9-17-SIGNAL-BEFORE-FINALIZATION",
     "An operator signal arrives while the outcome is still unsettled.",
     _axes(interruption="signal-before-finalization")),
    ("E9-D9-18-COHERENT-PASS",
     "A coherent terminal Run commits with a pass verdict and satisfied coverage.",
     _axes(**_SETTLED, verdict="pass")),
    ("E9-D9-19-CALLER-ERROR-IS-NOT-A-LEDGER-FAULT",
     "The caller supplies an unknown option; a caller error must not become a ledger fault.",
     _axes(**_REJECTED, rejectionCause="unknown-option")),
    ("E9-D9-21-POLICY-FAIL",
     "A coherent terminal Run commits with a policy fail verdict.",
     _axes(**_SETTLED, verdict="fail")),
)

D9_CONCURRENT_CONDITIONS: dict[str, Any] = {
    "faultCauses": ["ledger-corrupt"],
    "rejectionCauses": ["precondition-failed"],
    "deficiencies": ["provider-unavailable"],
}


def derive_d9_mapping(authority: Authority) -> dict[str, Any]:
    """Build d9Mapping by calling the live pinned D9 v1.13 derivation."""
    contract = authority.json(D9)
    module = authority.module(D9_CHECKER)
    if not isinstance(contract, dict):
        raise Malformed("D9 contract root is not an object")
    maps = contract.get("codeMaps")
    class_to_exit = contract.get("classToExitCode")
    cause_model = contract.get("causeModel")
    reference = contract.get("referenceDerivation")
    if not isinstance(maps, dict) or not isinstance(class_to_exit, dict) or \
            not isinstance(cause_model, dict) or not isinstance(reference, dict):
        raise Malformed("D9 contract lacks codeMaps/classToExitCode/causeModel")
    if not isinstance(reference.get("implementation"), str) or \
            reference.get("pure") is not True:
        raise Malformed("D9 referenceDerivation is not a pure declared implementation")
    precedence = cause_model.get("precedence")
    if precedence != ["faultCause", "rejectionCause", "deficiency"]:
        raise Malformed("D9 causeModel precedence is not fault>rejection>deficiency")

    def row_for(identifier: str, situation: str,
                axes: dict[str, Any]) -> dict[str, Any]:
        derived_class = module.derive_class(axes)
        derived_codes = module.derive_codes(axes, maps)
        if derived_class not in class_to_exit:
            raise Malformed(f"{identifier}: derived class is outside classToExitCode")
        return {
            "id": identifier,
            "situation": situation,
            "axes": copy.deepcopy(axes),
            "derivedClass": derived_class,
            "derivedCodes": copy.deepcopy(derived_codes),
            "derivedExitCode": class_to_exit[derived_class],
        }

    rows = [row_for(identifier, situation, axes)
            for identifier, situation, axes in D9_SITUATIONS]
    reduced = module.reduce_concurrent(
        copy.deepcopy(D9_CONCURRENT_CONDITIONS), list(precedence))
    if not isinstance(reduced, dict):
        raise Malformed("D9 reduce_concurrent did not return exclusive axes")
    concurrent_axes = _axes(**_FAULTED, **{
        key: reduced[key] for key in
        ("faultCause", "rejectionCause", "deficiency", "secondaryDeficiencies")})
    rows.append({
        **row_for("E9-D9-20-CONCURRENT-CONDITIONS-REDUCE-BY-PRECEDENCE",
                  "A fault, a rejection and a deficiency are observed together "
                  "and must reduce to one exclusive cause.",
                  concurrent_axes),
        "preReductionConditions": copy.deepcopy(D9_CONCURRENT_CONDITIONS),
        "reducedCauseAxes": copy.deepcopy(reduced),
    })
    rows.sort(key=lambda row: row["id"])

    codes: set[str] = set()
    for row in rows:
        payload = row["derivedCodes"]
        codes.update(payload.get("reasonCodes", []))
        if "errorCode" in payload:
            codes.add(payload["errorCode"])
    known: set[str] = set()
    for family in ("deficiencyToReasonCode", "rejectionCauseToErrorCode",
                   "faultCauseToErrorCode"):
        table = maps.get(family)
        if not isinstance(table, dict):
            raise Malformed(f"D9 codeMaps.{family} is not an object")
        known.update(str(value) for value in table.values())
    if not codes <= known:
        raise Malformed("d9Mapping emits a code outside the pinned D9 vocabulary")
    classes = sorted({row["derivedClass"] for row in rows})
    if set(classes) != set(class_to_exit):
        raise Malformed("d9Mapping rows do not cover every pinned D9 class")
    return {
        "schemaVersion": 1,
        "authority": D9,
        "authoritySha256": PINS[D9],
        "referenceDerivation": reference["implementation"],
        "derivationRule": (
            "Every row is produced by calling the pinned D9 v1.13 reference "
            "derivation on the row's exact axes. No termination class, ordered "
            "code payload or exit code in this artifact is authored."),
        "vocabularyRule": (
            "No new D9 class, code, axis, precedence or exit mapping is "
            "introduced. Every emitted code is a value of the pinned D9 "
            "codeMaps and every derived class is a key of the pinned "
            "classToExitCode."),
        "coveredClasses": classes,
        "concurrentReductionPrecedence": list(precedence),
        "totality": (
            "Rows 12, 13 and 14 carry cold reconstruction failure of the "
            "trusted durable store, of the evaluation proof bundle and of the "
            "semantic capability closure. Row 19 shows that a caller error "
            "stays request-rejected and never becomes an operational ledger "
            "fault. Rows 15 and 16 show that an indeterminate outcome "
            "terminates at exit 3 and can never be absorbed into a pass."),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Section 3.  TrustedRequestContext construction authority (E8-TODO-REQUEST-
# CONTEXT-LEAF).  Every field is projected from the independently accepted
# trusted-request-context.v3 authority; nothing here is authored.
# ---------------------------------------------------------------------------

TRC_REQUIRED_EXCLUSIONS = (
    "EvidenceDigest and evaluation proofs",
    "RunId derivation",
    "sealed Run semantic manifest",
    "fact identity and fingerprints",
)


def derive_request_context_binding(authority: Authority) -> dict[str, Any]:
    contract = authority.json(TRC3)
    if not isinstance(contract, dict):
        raise Malformed("trusted-request-context root is not an object")
    capability = contract.get("capabilityContract")
    boundary = contract.get("semanticBoundary")
    if not isinstance(capability, dict) or not isinstance(boundary, dict):
        raise Malformed("request-context capabilityContract/semanticBoundary shape")
    projection = capability.get("allowedProjection")
    registry = capability.get("authorityRegistry")
    if not isinstance(projection, dict) or not isinstance(registry, dict):
        raise Malformed("request-context allowedProjection/authorityRegistry shape")
    forbidden_sources = capability.get("forbiddenConstructionSources")
    forbidden_participation = boundary.get("forbiddenParticipation")
    if not isinstance(forbidden_sources, list) or not forbidden_sources:
        raise Malformed("request-context forbiddenConstructionSources is empty")
    if not isinstance(forbidden_participation, list):
        raise Malformed("request-context forbiddenParticipation is not an array")
    missing = [name for name in TRC_REQUIRED_EXCLUSIONS
               if name not in forbidden_participation]
    if missing:
        raise Malformed(
            "request-context authority does not exclude " + ", ".join(missing))
    if capability.get("publicConstructors") != []:
        raise Malformed("request-context declares a public constructor")
    if capability.get("contextExposes") != []:
        raise Malformed("request-context exposes a field")
    if capability.get("opaque") is not True or \
            capability.get("serializable") is not False or \
            capability.get("copyable") is not False:
        raise Malformed("request-context opacity/serializability drift")
    if registry.get("callerSuppliedRegistry") is not False or \
            registry.get("contextSuppliedAuthority") is not False:
        raise Malformed("request-context registry accepts caller authority")
    return {
        "schemaVersion": 1,
        "authority": TRC3,
        "authoritySha256": PINS[TRC3],
        "review": TRC3_REVIEW,
        "reviewSha256": PINS[TRC3_REVIEW],
        "capabilityType": capability.get("type"),
        "opaque": True,
        "serializable": False,
        "copyable": False,
        "publicConstructors": [],
        "contextExposes": [],
        "mintOwner": capability.get("mintOwner"),
        "mintPreconditions": copy.deepcopy(capability.get("mintPreconditions")),
        "allowedProjectionMethod": projection.get("method"),
        "allowedProjectionFields": copy.deepcopy(projection.get("fields")),
        "projectedRepresentation": projection.get("representation"),
        "forbiddenConstructionSources": copy.deepcopy(forbidden_sources),
        "forbiddenSemanticParticipation": copy.deepcopy(forbidden_participation),
        "evidenceJoin": (
            "E9 replaces the opaque E8 test-fixture capability with this "
            "independently accepted construction authority. The projected "
            "RequestId is operational-correlation-only: it may enter only a "
            "downstream closed operational record and never a semantic record, "
            "an encoded Evidence byte string, EvidenceDigest, RunId, "
            "RunIdentityPreimageV1 or TerminalRunV1."),
        "unexecutedGate": (
            "Production Rust capability ownership and durable atomic "
            "reservation remain UNEXECUTED in the pinned authority and are not "
            "claimed here."),
    }

# ---------------------------------------------------------------------------
# Section 4.  Semantic binding registry (EV8-IR-02).
#
# Each entry carries a prose claim, a closed machine-readable predicate, and
# the artifact leaf paths whose semantic content the entry underwrites.  The
# checker requires BOTH that the prose equals the deterministic rendering of
# the predicate AND that the predicate evaluates true against pinned
# dependency bytes.  Editing the prose alone fails rendering; editing the
# predicate alone fails evaluation; editing both consistently fails
# evaluation.  A prose claim can therefore not act as its own oracle.
# ---------------------------------------------------------------------------

ABSORPTION_VECTORS = ("EP8-POS-INDETERMINATE", "EP8-POS-ERROR")
OPERATIONAL_TOKENS = ("requestId", "executionId", "attemptId", "correlationId",
                      "req1_", "exec1-", "runSealRef")
NO_AUTHORITY_FACTS = (
    ("authority.authorityClaim", "NONE"),
    ("authority.independentReview", "REQUIRED"),
    ("authority.candidateState", "NOT-APPLIED"),
    ("assurance.state", "SPECIFIED"),
    ("assurance.evidenceGrade", "IMPLEMENTABLE_UNEXECUTED"),
    ("sealRecommendation", "DO-NOT-SEAL"),
)


def _dotted(root: Any, path: str) -> Any:
    current = root
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise Malformed(f"path {path} is absent")
        current = current[part]
    return current


def _render(kind: str, params: Mapping[str, Any]) -> str:
    if kind == "ep-policy-order-head":
        return (f"The accepted evaluation-proof vector {params['vectorId']} "
                f"evaluates its policy order head '{params['expected']}', so an "
                "indeterminate or error outcome dominates before any pass "
                "classification can be reached.")
    if kind == "ep-nonpass-vectors":
        pairs = ", ".join(f"{name} yields '{verdict}'"
                          for name, verdict in params["observed"])
        return (f"No evaluation-proof vector in the absorption control set "
                f"yields a pass: {pairs}. An indeterminate or error outcome "
                "cannot be recorded as an authoritative pass.")
    if kind == "ep-accepted-vector-identity":
        return ("The declared accepted evaluation-proof vector equals the "
                "pinned artifact's own acceptedAuthorityVectorId "
                f"'{params['expected']}', which occurs exactly once in its "
                "positiveVectors.")
    if kind == "rt-proof-member-set":
        return ("RawProofInventoryV1 is the exact projection of the pinned "
                f"retention closure's {params['count']} proofRefs "
                f"({params['verifiable']} verifiable / {params['replayable']} "
                f"replayable, every identityKind '{params['identityKind']}'), "
                "re-encoded under the declared grammar to bytes identical with "
                "acceptedGolden and with the inventory embedded inside "
                "SemanticEvidenceV1.")
    if kind == "rt-closure-commitment":
        return ("The declared accepted closure commitment equals the pinned "
                f"retention closure commitment {params['commitment']}, and its "
                f"canonical CAS ref {params['casRef']} recomputes from the "
                "closure bytes this artifact consumes.")
    if kind == "rt-semantic-basis":
        return ("The pinned retention successor declares "
                f"{params['artifact']}@{params['sha256']} as its exact "
                "semantic basis, so every retained reference to that "
                "generation is a declared lineage reference and not a stale "
                "generation fork.")
    if kind == "d9-live-derivation":
        return (f"All {params['rowCount']} d9Mapping rows obtain their "
                "termination class, ordered code payload and exit code from "
                f"the pinned reference derivation {params['implementation']}; "
                f"the derived classes cover {', '.join(params['classes'])}.")
    if kind == "d9-closed-vocabulary":
        return ("Every code emitted by d9Mapping is a value of the pinned D9 "
                "codeMaps and every derived class is a key of the pinned "
                "classToExitCode, so no new D9 class, code, axis, precedence "
                "or exit mapping is introduced.")
    if kind == "trc-construction-authority":
        return ("TrustedRequestContext exposes no field and no public "
                f"constructor; its only projection is {params['method']}; and "
                f"the pinned authority declares {params['forbiddenCount']} "
                "forbidden construction sources, so no producer may "
                "self-declare a weaker construction obligation.")
    if kind == "trc-semantic-exclusion":
        return ("The pinned request-context authority forbids the projected "
                "RequestId from participating in "
                f"{'; '.join(params['forbidden'])}.")
    if kind == "operational-token-exclusion":
        return ("No operational correlation token "
                f"({', '.join(params['tokens'])}) occurs in any encoded "
                "RawProofInventoryV1, SemanticEvidenceV1, "
                "RunIdentityPreimageV1 or TerminalRunV1 byte string, nor in "
                "the EvidenceDigest or RunId domain preimages.")
    if kind == "producer-declares-no-authority":
        facts = ", ".join(f"{name} '{value}'" for name, value in params["facts"])
        return (f"The producer declares no authority: {facts}. No CD-RT-5 "
                "disposition, seal, freeze, integration or product acceptance "
                "is claimed by this artifact.")
    if kind == "dependency-acyclicity":
        return ("No pinned dependency artifact references this Evidence "
                f"generation ({params['token']}), so the declared dependency "
                "direction carries no back edge.")
    if kind == "predecessor-rejection-binding":
        return ("The pinned predecessor review is the exact "
                f"{params['decision']} with {params['blockingCount']} blocking "
                f"findings and {params['residualCount']} residuals; every one "
                "of those identifiers carries a disposition in "
                "reviewFindingTransfers.")
    if kind == "grammar-derivation-closure":
        return (f"All {params['valueCount']} acceptedGolden values and "
                f"{params['byteFields']} encoded byte fields recompute from "
                "the pinned evaluation-proof vector and retention closure "
                "under the tag table declared by canonicalWireGrammar; no "
                "published commitment is carried.")
    if kind == "inventory-sort-disambiguation":
        return ("RawProofInventoryV1 sorts complete item record bytes before "
                "framing. Sorting the framed wrappers instead produces "
                f"different inventory bytes ({params['wrapperSortedLength']} "
                f"vs {params['itemSortedLength']} bytes are equal in length "
                "but differ in content) and therefore a different "
                "EvidenceDigest and RunId, so the encoding rule is "
                "disambiguated in this generation.")
    raise Malformed(f"unknown semantic predicate kind {kind!r}")


class SemanticContext:
    def __init__(self, authority: Authority, derived: Mapping[str, Any],
                 d9_mapping: Mapping[str, Any],
                 request_context: Mapping[str, Any]):
        self.authority = authority
        self.derived = derived
        self.d9_mapping = d9_mapping
        self.request_context = request_context
        self.ep8 = authority.json(EP8)
        self.rt22 = authority.json(RT22)
        self.d9 = authority.json(D9)
        self.trc3 = authority.json(TRC3)
        self.predecessor = authority.json(PREDECESSOR)
        self.review = authority.json(PREDECESSOR_REVIEW)


def semantic_entries(context: SemanticContext) -> list[dict[str, Any]]:
    derived = context.derived
    proof_refs = derived["proofRefs"]
    closure = derived["closure"]
    vector = derived["vector"]
    policy = _dotted(vector, "bundle.verdictProof.policy")
    order = policy.get("evaluationOrder") if isinstance(policy, dict) else None
    if not isinstance(order, list) or not order:
        raise Malformed("accepted vector policy evaluationOrder is not an array")
    observed = []
    for name in ABSORPTION_VECTORS:
        rows = [row for row in context.ep8.get("positiveVectors", [])
                if isinstance(row, dict) and row.get("id") == name]
        if len(rows) != 1:
            raise Malformed(f"absorption control vector {name} is not unique")
        observed.append((name, _dotted(rows[0], "bundle.verdictProof.verdict")))
    projection = _dotted(context.rt22, "semanticBasisProjection")
    blocking = context.review.get("blockingFindings")
    residual = context.review.get("residuals")
    specs: list[dict[str, Any]] = [
        {"id": "SB-01-INDETERMINATE-OR-ERROR-DOMINATES",
         "kind": "ep-policy-order-head",
         "params": {"vectorId": vector["id"], "expected": order[0]},
         "boundArtifactPaths": [
             "invariants", "d9Mapping.rows", "acceptedGolden.values.verdict"],
         "provenBy": "PR-03-EP-COMMITMENT-DERIVATION"},
        {"id": "SB-02-NO-ABSORPTION-INTO-AUTHORITATIVE-PASS",
         "kind": "ep-nonpass-vectors",
         "params": {"observed": [list(pair) for pair in observed]},
         "boundArtifactPaths": ["invariants", "adversarialControls"],
         "provenBy": "PR-03-EP-COMMITMENT-DERIVATION"},
        {"id": "SB-03-ACCEPTED-VECTOR-IS-NOT-SELF-DECLARED",
         "kind": "ep-accepted-vector-identity",
         "params": {"expected": context.ep8["acceptedAuthorityVectorId"]},
         "boundArtifactPaths": ["dependencies.evaluationProof.acceptedVectorId"],
         "provenBy": "PR-03-EP-COMMITMENT-DERIVATION"},
        {"id": "SB-04-AGGREGATE-BINDS-ITS-MEMBER-SET",
         "kind": "rt-proof-member-set",
         "params": {
             "count": len(proof_refs),
             "verifiable": sum(1 for row in proof_refs
                               if row.get("requiredForCapability") == "verifiable"),
             "replayable": sum(1 for row in proof_refs
                               if row.get("requiredForCapability") == "replayable"),
             "identityKind": "raw-cas"},
         "boundArtifactPaths": [
             "semanticJoins.retention", "acceptedGolden.rawProofInventoryHex",
             "canonicalWireGrammar.records.RawProofInventoryV1.equalityRule"],
         "provenBy": "PR-02-INVENTORY-MEMBER-BINDING"},
        {"id": "SB-05-RETENTION-CLOSURE-COMMITMENT-IS-DERIVED",
         "kind": "rt-closure-commitment",
         "params": {"commitment": closure["closureCommitment"],
                    "casRef": sha_ref(canonical(closure))},
         "boundArtifactPaths": [
             "dependencies.retentionCustody.acceptedClosureCommitment",
             "acceptedGolden.values.semanticCapabilityClosureCommitment",
             "acceptedGolden.values.semanticCapabilityClosureCasRef"],
         "provenBy": "PR-02-INVENTORY-MEMBER-BINDING"},
        {"id": "SB-06-RETENTION-SEMANTIC-BASIS-IS-DECLARED-LINEAGE",
         "kind": "rt-semantic-basis",
         "params": {"artifact": projection["sourceRetentionArtifact"],
                    "sha256": projection["sourceRetentionSha256"]},
         "boundArtifactPaths": [
             "dependencies.retentionCustody.semanticBasisArtifact",
             "semanticJoins.versioning"],
         "provenBy": "PR-09-RETENTION-CHECKER-GREEN"},
        {"id": "SB-07-TERMINATION-IS-DERIVED-NOT-AUTHORED",
         "kind": "d9-live-derivation",
         "params": {"rowCount": len(context.d9_mapping["rows"]),
                    "implementation": context.d9_mapping["referenceDerivation"],
                    "classes": list(context.d9_mapping["coveredClasses"])},
         "boundArtifactPaths": ["d9Mapping.rows", "d9Mapping.derivationRule"],
         "provenBy": "PR-05-D9-LIVE-DERIVATION"},
        {"id": "SB-08-NO-NEW-TERMINATION-VOCABULARY",
         "kind": "d9-closed-vocabulary", "params": {},
         "boundArtifactPaths": ["d9Mapping.vocabularyRule"],
         "provenBy": "PR-05-D9-LIVE-DERIVATION"},
        {"id": "SB-09-REQUEST-CONTEXT-CONSTRUCTION-AUTHORITY",
         "kind": "trc-construction-authority",
         "params": {
             "method": context.request_context["allowedProjectionMethod"],
             "forbiddenCount": len(
                 context.request_context["forbiddenConstructionSources"])},
         "boundArtifactPaths": [
             "requestContextBinding", "sealedCapabilityContract.productFork"],
         "provenBy": "PR-06-REQUEST-CONTEXT-AUTHORITY"},
        {"id": "SB-10-REQUEST-CONTEXT-SEMANTIC-EXCLUSION",
         "kind": "trc-semantic-exclusion",
         "params": {"forbidden": list(TRC_REQUIRED_EXCLUSIONS)},
         "boundArtifactPaths": [
             "recursiveRequestIdExclusion.rule",
             "requestContextBinding.forbiddenSemanticParticipation"],
         "provenBy": "PR-06-REQUEST-CONTEXT-AUTHORITY"},
        {"id": "SB-11-OPERATIONAL-TOKENS-ABSENT-FROM-ENCODED-RECORDS",
         "kind": "operational-token-exclusion",
         "params": {"tokens": list(OPERATIONAL_TOKENS)},
         "boundArtifactPaths": [
             "recursiveRequestIdExclusion.surfaces",
             "recursiveRequestIdExclusion.negativeControl"],
         "provenBy": "PR-14-OPERATIONAL-TOKEN-EXCLUSION"},
        {"id": "SB-12-PRODUCER-DECLARES-NO-AUTHORITY",
         "kind": "producer-declares-no-authority",
         "params": {"facts": [list(pair) for pair in NO_AUTHORITY_FACTS]},
         "boundArtifactPaths": [
             "authority", "assurance", "sealRecommendation",
             "sealedCapabilityContract.productFork"],
         "provenBy": "PR-15-PRODUCER-OBLIGATION"},
        {"id": "SB-13-DEPENDENCY-DIRECTION-HAS-NO-BACK-EDGE",
         "kind": "dependency-acyclicity",
         "params": {"token": "evidence.v9"},
         "boundArtifactPaths": ["dependencies.dependencyDirection"],
         "provenBy": "PR-16-DEPENDENCY-ACYCLICITY"},
        {"id": "SB-14-PREDECESSOR-REJECTION-IS-BOUND",
         "kind": "predecessor-rejection-binding",
         "params": {
             "decision": _dotted(context.review, "verdict.decision"),
             "blockingCount": len(blocking) if isinstance(blocking, list) else -1,
             "residualCount": len(residual) if isinstance(residual, list) else -1},
         "boundArtifactPaths": [
             "successorDelta.rejection", "reviewFindingTransfers"],
         "provenBy": "PR-17-FINDING-DISPOSITION-CLOSURE"},
        {"id": "SB-15-EVERY-COMMITMENT-IS-RECOMPUTED",
         "kind": "grammar-derivation-closure",
         "params": {"valueCount": len(derived["values"]), "byteFields": 6},
         "boundArtifactPaths": [
             "acceptedGolden.values", "acceptedGolden.evidenceDigest",
             "acceptedGolden.runId", "acceptedGolden.runSealRef",
             "evidenceRecomputationContract"],
         "provenBy": "PR-01-GRAMMAR-RECOMPUTATION"},
        {"id": "SB-16-INVENTORY-SORT-IS-DISAMBIGUATED",
         "kind": "inventory-sort-disambiguation",
         "params": {
             "itemSortedLength": len(derived["inventory"]),
             "wrapperSortedLength": len(derived["inventoryWrapperSorted"])},
         "boundArtifactPaths": [
             "canonicalWireGrammar.recordRules.sets",
             "canonicalWireGrammar.records.RawProofInventoryV1.fields"],
         "provenBy": "PR-01-GRAMMAR-RECOMPUTATION"},
    ]
    for spec in specs:
        spec["claim"] = _render(spec["kind"], spec["params"])
    return specs


def evaluate_semantic_entry(entry: Mapping[str, Any],
                            context: SemanticContext) -> tuple[bool, str]:
    kind = entry.get("kind")
    params = entry.get("params")
    if not isinstance(params, dict):
        return False, "params is not an object"
    derived = context.derived
    if kind == "ep-policy-order-head":
        order = _dotted(derived["vector"], "bundle.verdictProof.policy.evaluationOrder")
        ok = isinstance(order, list) and bool(order) and \
            order[0] == params.get("expected") == "indeterminate-or-error-dominates"
        return ok, f"policy order head is {order[0] if order else None!r}"
    if kind == "ep-nonpass-vectors":
        for row in params.get("observed", []):
            if not isinstance(row, list) or len(row) != 2:
                return False, "observed row shape"
            name, verdict = row
            matches = [item for item in context.ep8.get("positiveVectors", [])
                       if isinstance(item, dict) and item.get("id") == name]
            if len(matches) != 1:
                return False, f"{name} is not unique"
            live = _dotted(matches[0], "bundle.verdictProof.verdict")
            if live != verdict or live == "pass":
                return False, f"{name} yields {live!r}"
        return True, "absorption control vectors are all non-pass"
    if kind == "ep-accepted-vector-identity":
        return (context.ep8.get("acceptedAuthorityVectorId") ==
                params.get("expected") == derived["vector"]["id"],
                "accepted vector identity")
    if kind == "rt-proof-member-set":
        refs = derived["proofRefs"]
        counts = {"verifiable": 0, "replayable": 0}
        for row in refs:
            capability = row.get("requiredForCapability")
            if capability not in counts or row.get("identityKind") != "raw-cas":
                return False, "proofRef capability/identityKind outside the closed set"
            counts[capability] += 1
        ok = (params.get("count") == len(refs) and
              params.get("verifiable") == counts["verifiable"] and
              params.get("replayable") == counts["replayable"])
        return ok, f"{len(refs)} members {counts}"
    if kind == "rt-closure-commitment":
        closure = derived["closure"]
        ok = (params.get("commitment") == closure.get("closureCommitment") and
              params.get("casRef") == sha_ref(canonical(closure)) ==
              derived["values"]["semanticCapabilityClosureCasRef"])
        return ok, "closure commitment/CAS ref"
    if kind == "rt-semantic-basis":
        projection = _dotted(context.rt22, "semanticBasisProjection")
        ok = (projection.get("sourceRetentionArtifact") == params.get("artifact")
              == RT13 and
              projection.get("sourceRetentionSha256") == params.get("sha256")
              == PINS[RT13])
        return ok, "declared semantic basis"
    if kind == "d9-live-derivation":
        rows = context.d9_mapping["rows"]
        module = context.authority.module(D9_CHECKER)
        maps = context.d9["codeMaps"]
        table = context.d9["classToExitCode"]
        for row in rows:
            axes = row["axes"]
            if module.derive_class(axes) != row["derivedClass"] or \
                    module.derive_codes(axes, maps) != row["derivedCodes"] or \
                    table[row["derivedClass"]] != row["derivedExitCode"]:
                return False, f"{row['id']} does not reproduce the live derivation"
        ok = (params.get("rowCount") == len(rows) and
              params.get("implementation") ==
              _dotted(context.d9, "referenceDerivation.implementation"))
        return ok, f"{len(rows)} rows re-derived live"
    if kind == "d9-closed-vocabulary":
        maps = context.d9["codeMaps"]
        known = set()
        for family in ("deficiencyToReasonCode", "rejectionCauseToErrorCode",
                       "faultCauseToErrorCode"):
            known.update(str(value) for value in maps[family].values())
        for row in context.d9_mapping["rows"]:
            payload = row["derivedCodes"]
            emitted = set(payload.get("reasonCodes", []))
            if "errorCode" in payload:
                emitted.add(payload["errorCode"])
            if not emitted <= known:
                return False, f"{row['id']} emits an unknown code"
            if row["derivedClass"] not in context.d9["classToExitCode"]:
                return False, f"{row['id']} emits an unknown class"
        return True, "closed D9 vocabulary"
    if kind == "trc-construction-authority":
        capability = _dotted(context.trc3, "capabilityContract")
        ok = (capability.get("publicConstructors") == [] and
              capability.get("contextExposes") == [] and
              _dotted(context.trc3, "capabilityContract.allowedProjection.method")
              == params.get("method") and
              len(capability.get("forbiddenConstructionSources", [])) ==
              params.get("forbiddenCount"))
        return ok, "request-context construction authority"
    if kind == "trc-semantic-exclusion":
        forbidden = _dotted(context.trc3, "semanticBoundary.forbiddenParticipation")
        ok = all(name in forbidden for name in params.get("forbidden", [])) and \
            list(params.get("forbidden", [])) == list(TRC_REQUIRED_EXCLUSIONS)
        return ok, "request-context semantic exclusion"
    if kind == "operational-token-exclusion":
        blobs = [derived["inventory"], derived["semantic"],
                 derived["semanticPreimage"], derived["runRecord"],
                 derived["runPreimage"], derived["terminal"]]
        for token in params.get("tokens", []):
            needle = str(token).encode("utf-8")
            for blob in blobs:
                if needle in blob:
                    return False, f"token {token!r} occurs in an encoded record"
        return list(params.get("tokens", [])) == list(OPERATIONAL_TOKENS), \
            "no operational token in any encoded record"
    if kind == "producer-declares-no-authority":
        facts = params.get("facts")
        if [tuple(row) for row in facts] != list(NO_AUTHORITY_FACTS):
            return False, "declared no-authority fact set drifted"
        return True, "producer declares no authority"
    if kind == "dependency-acyclicity":
        token = str(params.get("token", "")).encode("utf-8")
        if not token:
            return False, "empty acyclicity token"
        for name in (EP8, RT22, D9, TRC3, VERSIONING):
            if token in context.authority.snapshots[name]:
                return False, f"{name} references {params['token']}"
        return True, "no dependency back edge"
    if kind == "predecessor-rejection-binding":
        review = context.review
        ok = (_dotted(review, "verdict.decision") == params.get("decision")
              == "REJECT" and
              len(review.get("blockingFindings", [])) ==
              params.get("blockingCount") == 8 and
              len(review.get("residuals", [])) == params.get("residualCount"))
        return ok, "predecessor rejection binding"
    if kind == "grammar-derivation-closure":
        return (params.get("valueCount") == len(derived["values"]) == 14 and
                params.get("byteFields") == 6), "derivation closure"
    if kind == "inventory-sort-disambiguation":
        item_sorted = derived["inventory"]
        wrapper_sorted = derived["inventoryWrapperSorted"]
        ok = (item_sorted != wrapper_sorted and
              len(item_sorted) == params.get("itemSortedLength") and
              len(wrapper_sorted) == params.get("wrapperSortedLength"))
        return ok, "inventory sort disambiguation"
    return False, f"unknown predicate kind {kind!r}"


# ---------------------------------------------------------------------------
# Section 5.  Expected successor construction.
#
# check() derives the COMPLETE expected v9 object from the pinned predecessor
# bytes plus the pinned dependency bytes and requires exact equality with the
# candidate.  Every leaf of the artifact is therefore derived rather than
# declared, which is the mechanical form of the repair EV8-IR-02 demanded.
# ---------------------------------------------------------------------------

EXPECTED_STATUS = "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW"
EXPECTED_AUTHOR = "phase1a-evidence-v9-successor-lane"
EXPECTED_DATE = "2026-08-02"
EXPECTED_ROLE = (
    "E9 recomputed-identity Evidence successor: EP8/RT22-derived Run terminal "
    "identity, live D9 v1.13 termination derivation, pinned "
    "TrustedRequestContextV3 construction authority, and derivation-complete "
    "successor binding over the independently rejected E8 foundation"
)

PROBE_IDS: tuple[str, ...] = (
    "PR-01-GRAMMAR-RECOMPUTATION",
    "PR-02-INVENTORY-MEMBER-BINDING",
    "PR-03-EP-COMMITMENT-DERIVATION",
    "PR-04-RUN-SUBSTITUTION-GOLDENS",
    "PR-05-D9-LIVE-DERIVATION",
    "PR-06-REQUEST-CONTEXT-AUTHORITY",
    "PR-07-RETAINED-PREDECESSOR-FOUNDATION",
    "PR-08-RETAINED-PREDECESSOR-MUTATION-SUITE",
    "PR-09-RETENTION-CHECKER-GREEN",
    "PR-10-TERMINATION-CHECKER-GREEN",
    "PR-11-EVALUATION-PROOF-CHECKER-GREEN",
    "PR-12-CROSS-IMPLEMENTATION-WIRE-CONTROL",
    "PR-13-HOSTILE-INPUT-TOTALITY",
    "PR-14-OPERATIONAL-TOKEN-EXCLUSION",
    "PR-15-PRODUCER-OBLIGATION",
    "PR-16-DEPENDENCY-ACYCLICITY",
    "PR-17-FINDING-DISPOSITION-CLOSURE",
    "PR-18-EXPECTED-SUCCESSOR-EQUALITY",
    "PR-19-NOMENCLATURE-CLOSURE",
    "PR-20-SEMANTIC-BINDING-REGISTRY",
    "PR-21-SELFTEST-REACHABILITY",
    "PR-22-VERSIONING-CHECKER-GREEN",
)
CLOSED_STATES = ("CLOSED-BY-EXECUTED-PROBE", "CLOSED-BY-DERIVATION")
OPEN_STATES = ("OPEN-CARRIED-RESIDUAL", "CARRIED-FROM-PREDECESSOR")
ALL_STATES = CLOSED_STATES + OPEN_STATES

DISPOSITIONS: dict[str, dict[str, Any]] = {
    "EV7-PF-01-SAME-RUN-MULTI-ATTEMPT-CONVERGENCE": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "The retained predecessor foundation executes same-Run convergence: a second distinct Attempt whose semantic inputs reproduce an already committed Run converges onto the existing four Run-scoped peers instead of being read as a forbidden partial final set.",
        "provenBy": ["PR-07-RETAINED-PREDECESSOR-FOUNDATION"]},
    "EV7-PF-02-TRANSACTION-PRECONDITION-TOCTOU": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "The retained foundation executes the Attempt/journal snapshot-CAS TOCTOU probe, so the modeled swap is conditioned on the exact Attempt revision and journal bytes that were validated.",
        "provenBy": ["PR-07-RETAINED-PREDECESSOR-FOUNDATION"]},
    "EV7-PF-03-NO-JOURNAL-PARTIAL-PUBLICATION-BLIND-SPOT": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "The project-wide integrity enumeration walks all six final containers before target lookup, so an absent link and journal no longer hide other final peers; the 128-state final/journal matrix executes the whole boundary.",
        "provenBy": ["PR-07-RETAINED-PREDECESSOR-FOUNDATION"]},
    "EV7-PF-04-D9-NOT-TOTAL-OVER-COLD-RECOVERY": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "d9Mapping rows 12, 13 and 14 carry cold reconstruction failure of the trusted durable store, of the evaluation proof bundle and of the semantic capability closure, and each derives LEDGER.CORRUPT / operational-failed / exit 4 from the live D9 v1.13 derivation. Row 19 shows a caller error stays request-rejected.",
        "provenBy": ["PR-05-D9-LIVE-DERIVATION"]},
    "EV7-PF-05-CUSTODY-PREPARATION-OVERWRITES-CORRUPTION": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "The retained foundation enforces absent-or-exact equality on custody preparation rows through the pinned retention serialized-custody reducer join rather than replacing them blindly.",
        "provenBy": ["PR-07-RETAINED-PREDECESSOR-FOUNDATION"]},
    "EV7-PF-06-COLD-IMAGE-FINAL-ROW-BOUNDARY-OPEN": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "Closed durable-record enforcement is mechanical for all six final kinds; the independent v8 review reproduced 65 of 65 unknown-field, missing-field, mistyped, out-of-enum, cross-project, null, scalar, array and wrong-container cases rejected deterministically as LedgerCorrupt.",
        "provenBy": ["PR-07-RETAINED-PREDECESSOR-FOUNDATION",
                     "PR-08-RETAINED-PREDECESSOR-MUTATION-SUITE"]},
    "EV7-PF-07-DECLARED-SUCCESSOR-CONTRACT-NOT-CHECKER-BOUND": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "The successor object is no longer validated by sampling. The complete expected artifact is derived from the pinned predecessor and dependency bytes and compared for exact equality, and the semantic binding registry additionally binds the changed-root obligations to executed predicates over pinned authority.",
        "provenBy": ["PR-18-EXPECTED-SUCCESSOR-EQUALITY",
                     "PR-20-SEMANTIC-BINDING-REGISTRY"]},
    "EV7-PF-08-BINDING-NOMENCLATURE-AND-GENERATION-FORK": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "The custody-root record alias and the stale evaluation-proof, retention and versioning generation labels are forbidden by a regular-expression scan over every string in the artifact, and the predecessor-generation labels that survived inside the identity-protected grammar are replaced by the consumed generations in this successor.",
        "provenBy": ["PR-19-NOMENCLATURE-CLOSURE"]},
    "EV7-PF-R01-CUSTODY-AUTHORITY-JOIN": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "The serialized custody contract and the pinned retention reducer join address this, but no reviewer has independently reimplemented the 23-object acquire/retry/release, pending-expiry, crash-gap repin and contention probes. Carried forward unchanged as EV8-IR-R6.",
        "provenBy": []},
    "EV7-PF-R02-D9-DERIVATION-IS-LITERAL": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "No termination class, ordered code payload or exit code is authored anywhere in this artifact. Every d9Mapping row is produced by calling the pinned D9 v1.13 reference derivation on the row's exact axes, and the concurrent-condition row additionally calls the pinned reducer.",
        "provenBy": ["PR-05-D9-LIVE-DERIVATION",
                     "PR-10-TERMINATION-CHECKER-GREEN"]},
    "EV7-PF-R03-MATRIX-ALIASES-ARE-AUTHORED-SUMMARIES": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "The recovery matrix alias rows remain author-summarised inside the retained predecessor foundation. This successor does not repair them and does not claim they are executed.",
        "provenBy": []},
    "EV8-IR-01-CANDIDATE-IS-RED-AGAINST-ITS-OWN-CHECKER": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "All three predecessor TODOs are closed on merit, not suppressed. The D9/retention successors are pinned at d9-exit-contract.v1.13 and retention-tiers.v22, both independently accepted with zero blocking findings; the request-context leaf is pinned at the independently accepted trusted-request-context.v3; and the remaining changed-root binding is closed by derivation of the whole successor object. blockingTodos is empty because every obligation is discharged, and this checker emits no unconditional finding.",
        "provenBy": ["PR-05-D9-LIVE-DERIVATION", "PR-06-REQUEST-CONTEXT-AUTHORITY",
                     "PR-09-RETENTION-CHECKER-GREEN",
                     "PR-18-EXPECTED-SUCCESSOR-EQUALITY"]},
    "EV8-IR-02-CHANGED-ROOT-SEMANTICS-ARE-DECLARATION-ONLY": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "Every leaf of this artifact is derived: carried roots from the pinned predecessor bytes, dependency roots from the pinned dependency bytes, termination rows from the live D9 derivation, the golden from the grammar-driven recomputation, and every remaining new string from the successor construction that this checker also emits under --emit-candidate. The twenty-two mutations the independent review reported as escaping are each rejected, and a mutation that fails to apply or that applies without changing bytes is counted as an escape.",
        "provenBy": ["PR-18-EXPECTED-SUCCESSOR-EQUALITY",
                     "PR-20-SEMANTIC-BINDING-REGISTRY"]},
    "EV8-IR-03-EP-PROOF-COMMITMENTS-NOT-RECOMPUTED": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "SemanticEvidenceV1 is re-encoded under the tag table declared by canonicalWireGrammar, so universeCommitment, outcomeSetCommitment and verdictDerivationCommitment are bound by equality to bundle.requiredUniverse.universeCommitment and bundle.verdictProof.{outcomeSetCommitment,derivationCommitment} of the accepted evaluation-proof vector. A valid-looking arbitrary digest, a same-cardinality swap and a same-shape substitution are each rejected, and the retained independent wire implementation reproduces the same bytes.",
        "provenBy": ["PR-01-GRAMMAR-RECOMPUTATION", "PR-03-EP-COMMITMENT-DERIVATION",
                     "PR-12-CROSS-IMPLEMENTATION-WIRE-CONTROL"]},
    "EV8-IR-04-AGGREGATE-DOES-NOT-BIND-ITS-MEMBER-SET": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "RawProofInventoryV1 is projected from the pinned retention closure's proofRefs and required to equal both acceptedGolden.rawProofInventoryHex and the inventory embedded inside SemanticEvidenceV1. Member drop, member add, member substitution and reorder are rejected, and the declared cardinality and verifiable/replayable split are asserted against the pinned closure rather than against authored bytes.",
        "provenBy": ["PR-02-INVENTORY-MEMBER-BINDING",
                     "PR-09-RETENTION-CHECKER-GREEN"]},
    "EV8-IR-05-D9-MAPPING-IS-UNRECOMPUTED-AUTHORED-LITERALS": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "The D9 authority is pinned by hash, executed from the verified bytes, and called for every row. d9Mapping is no longer an identity-protected literal block: it is derived, it covers all six pinned termination classes, and it is proved total over trusted durable-store, evaluation-proof and retention reconstruction failure without converting caller errors into ledger faults.",
        "provenBy": ["PR-05-D9-LIVE-DERIVATION",
                     "PR-10-TERMINATION-CHECKER-GREEN"]},
    "EV8-IR-06-DOCUMENTED-SELFTEST-MODE-IS-UNREACHABLE": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "There is no unconditional TODO gate and no second undocumented selftest entrypoint. --selftest always reaches the mutation suite; when the base candidate is not clean it refuses with a distinct exit code 3 and reports the dirty base rather than silently printing the same output as normal mode.",
        "provenBy": ["PR-21-SELFTEST-REACHABILITY"]},
    "EV8-IR-07-HOSTILE-PARSED-JSON-RAISES-INSTEAD-OF-REPORTING": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "Every root and nested schema node is type-guarded before member access, and the hostile-input matrix injects null, integer, negative, float, boolean, empty text, text, empty array, empty object, nested array, nested object and unknown-key values at the root, at every root key and at every nested schema node. Zero cases escape as an uncaught exception from the unguarded checking layers.",
        "provenBy": ["PR-13-HOSTILE-INPUT-TOTALITY"]},
    "EV8-IR-08-PREDECESSOR-REJECTION-FINDINGS-HAVE-NO-DISPOSITION": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "reviewFindingTransfers carries one entry per identifier read live from the pinned predecessor and lineage reviews. A missing, fabricated or renamed disposition is rejected, and no entry may declare a closed state without naming executed probes that actually ran and returned true in the same invocation.",
        "provenBy": ["PR-17-FINDING-DISPOSITION-CLOSURE"]},
    "EV8-IR-R1-PROVENANCE-NOT-RECOMPUTATION": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "This checker performs its own wire re-encoding for all five records and both domain envelopes, and additionally cross-checks the framing, record and envelope primitives against the retained independent implementation in check-evidence-v4.py, which is pinned by hash. No published commitment rests on byte equality with a predecessor.",
        "provenBy": ["PR-01-GRAMMAR-RECOMPUTATION",
                     "PR-12-CROSS-IMPLEMENTATION-WIRE-CONTROL"]},
    "EV8-IR-R2-DRIFT-CONTROL-MISREAD-AS-BINDING": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "Carried roots are still compared to the pinned predecessor, but that comparison is no longer the only protection: the semantic binding registry binds the outcome-absorption, producer-obligation, retention/termination join and attempt-metadata-exclusion obligations to predicates evaluated against pinned dependency bytes, and the registry's coverage of the escaping surfaces is itself checked.",
        "provenBy": ["PR-20-SEMANTIC-BINDING-REGISTRY"]},
    "EV8-IR-R3-TAUTOLOGICAL-CONTRACT-BINDING": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Genuinely new prose in this successor is still authored in the checker that emits it, so for that prose the comparison proves only self-consistency. The mitigation is that the prose is not the oracle: each semantic obligation is additionally evaluated against pinned dependency bytes, and the executable probes remain the semantic authority. This residual is retained, not claimed closed.",
        "provenBy": []},
    "EV8-IR-R4-GRAMMAR-SORT-AMBIGUITY": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "The RawProofInventoryV1 items encoding now states that complete item record bytes sort before framing. The checker computes both orders, requires them to differ on this data, and requires the item-sorted order to reproduce the published inventory, so an implementer reading only the per-record rule can no longer derive a different EvidenceDigest.",
        "provenBy": ["PR-01-GRAMMAR-RECOMPUTATION"]},
    "EV8-IR-R5-EP7-RT11-NOMENCLATURE-IN-PROTECTED-SURFACES": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "canonicalWireGrammar now names the consumed evaluation-proof and retention generations wherever it named their predecessors. The remaining predecessor-generation labels are exactly the frozen historical golden identifiers and retained control text, each enumerated at leaf-path granularity and checked to be non-empty and exhaustive.",
        "provenBy": ["PR-19-NOMENCLATURE-CLOSURE"]},
    "EV8-IR-R6-CUSTODY-AUTHORITY-JOIN": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward unverified. The 23-object acquire/retry/release, pending-expiry, crash-gap repin and contention probes are executed only by the retained predecessor foundation and have not been independently reimplemented by any reviewer.",
        "provenBy": []},
}

GRAMMAR_DELTA: tuple[tuple[str, str, str, str], ...] = (
    ("records.RawProofInventoryItemV1.fields[1].type",
     "RT11 closed recordKind", "RT22 closed recordKind",
     "name the consumed retention generation"),
    ("records.RawProofInventoryV1.fields[2].encoding",
     "blob(concat(sorted blob(0x8b, complete RawProofInventoryItemV1 bytes)))",
     "blob(0x8a, concat(blob(0x8b, item) for item in sort-ascending-unsigned("
     "complete RawProofInventoryItemV1 record bytes))); the sort is over the "
     "unframed item record bytes and happens BEFORE 0x8b framing",
     "remove the sort-order ambiguity recorded as EV8-IR-R4"),
    ("records.RawProofInventoryV1.equalityRule",
     "Exact projection of RT11 SemanticCapabilityClosureV3.proofRefs after "
     "requiring identityKind=raw-cas and every item ProjectId equal the outer "
     "ProjectId. Preserve recordCasRef, recordKind, and requiredForCapability "
     "exactly; zero items is permitted only when RT11 validates that capability.",
     "Exact projection of RT22 semanticBasisProjection.semanticCapabilityClosure"
     ".proofRefs after requiring identityKind=raw-cas and every item ProjectId "
     "equal the outer ProjectId. Preserve recordCasRef, recordKind, and "
     "requiredForCapability exactly; zero items is permitted only when the "
     "retention authority validates that capability.",
     "name the consumed retention generation"),
    ("records.SemanticEvidenceV1.fields[4].type",
     "RawCasRef<EP6.EvaluationProofBundleV5>",
     "RawCasRef<EP8.EvaluationProofBundleV5>",
     "name the consumed evaluation-proof generation"),
    ("records.SemanticEvidenceV1.fields[5].type",
     "EP6 universe commitment", "EP8 universe commitment",
     "name the consumed evaluation-proof generation"),
    ("records.SemanticEvidenceV1.fields[6].type",
     "EP6 outcome-set commitment", "EP8 outcome-set commitment",
     "name the consumed evaluation-proof generation"),
    ("records.SemanticEvidenceV1.fields[7].type",
     "EP6 verdict-input commitment", "EP8 verdict-input commitment",
     "name the consumed evaluation-proof generation"),
    ("records.SemanticEvidenceV1.fields[11].type",
     "RawCasRef<RT11.SemanticCapabilityClosureV3>",
     "RawCasRef<RT22.SemanticCapabilityClosureV3>",
     "name the consumed retention generation"),
    ("records.SemanticEvidenceV1.fields[12].type",
     "RT11 semantic-capability-closure-v3 commitment",
     "RT22 semantic-capability-closure-v3 commitment",
     "name the consumed retention generation"),
    ("records.TerminalRunV1.fields[12].type",
     "RawCasRef<RT11.SemanticCapabilityClosureV3>",
     "RawCasRef<RT22.SemanticCapabilityClosureV3>",
     "name the consumed retention generation"),
    ("records.TerminalRunV1.fields[13].type",
     "RT11 semantic-capability-closure-v3 commitment",
     "RT22 semantic-capability-closure-v3 commitment",
     "name the consumed retention generation"),
)
GRAMMAR_DELTA_FORBIDDEN_LEAVES = (
    "recordTag", "tag", "name", "required", "fields", "recordRules",
    "tagRegistry", "domainEnvelope", "commitments",
)

_BASE_HISTORICAL_LABEL_PATHS = (
    "acceptedGolden.id",
    "acceptedGolden.sourceVectorId",
    "positiveControls[0].assert",
    "positiveControls[2].assert",
    "adversarialControls.authority[10]",
    "reviewFindingTransfers[0].closure",
    "reviewFindingTransfers[2].closure",
    "reviewFindingTransfers[4].closure",
)
HISTORICAL_LABEL_RE = re.compile(r"(?<![A-Za-z0-9])(EP5|EP6|RT10|RT11)(?![A-Za-z0-9])")
# The quoted predecessor value of a grammar editorial delta necessarily carries
# the label the delta removes.  Those paths are derived, never hand-listed.
RETAINED_HISTORICAL_LABEL_PATHS = _BASE_HISTORICAL_LABEL_PATHS + tuple(
    f"successorDelta.grammarEditorialDelta[{index}].predecessorValue"
    for index, row in enumerate(GRAMMAR_DELTA)
    if HISTORICAL_LABEL_RE.search(row[1]))
FORBIDDEN_ALIAS_RE = re.compile(r"(?<![A-Za-z0-9])CustodyRootV1(?![A-Za-z0-9])")
STALE_GENERATION_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:EP7|RT12|RT21|VERSIONING v6|VERSIONING v7|Evidence v7|"
    r"TrustedRequestContextV2)(?![A-Za-z0-9])")

_PATH_STEP = re.compile(r"([A-Za-z0-9_]+)|\[(\d+)\]")


def _path_steps(path: str) -> list[Any]:
    steps: list[Any] = []
    position = 0
    while position < len(path):
        if path[position] == ".":
            position += 1
            continue
        match = _PATH_STEP.match(path, position)
        if match is None:
            raise Malformed(f"unparsable path {path!r}")
        steps.append(match.group(1) if match.group(1) is not None
                     else int(match.group(2)))
        position = match.end()
    if not steps:
        raise Malformed("empty path")
    return steps


def _resolve(root: Any, path: str) -> Any:
    current = root
    for step in _path_steps(path):
        if isinstance(step, int):
            if not isinstance(current, list) or not 0 <= step < len(current):
                raise Malformed(f"path {path}: index {step} is absent")
            current = current[step]
        else:
            if not isinstance(current, dict) or step not in current:
                raise Malformed(f"path {path}: key {step!r} is absent")
            current = current[step]
    return current


def _assign(root: Any, path: str, value: Any) -> None:
    steps = _path_steps(path)
    current = root
    for step in steps[:-1]:
        current = current[step]
    current[steps[-1]] = value


def _leaf_paths(value: Any, prefix: str = "") -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for key, child in value.items():
            joined = f"{prefix}.{key}" if prefix else str(key)
            result.extend(_leaf_paths(child, joined))
        return result or [prefix]
    if isinstance(value, list):
        result = []
        for index, child in enumerate(value):
            result.extend(_leaf_paths(child, f"{prefix}[{index}]"))
        return result or [prefix]
    return [prefix]


def _dependency_row(artifact: str, checker: str, review: str,
                    extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    row = {
        "artifact": artifact,
        "sha256": PINS[artifact],
        "checker": checker,
        "checkerSha256": PINS[checker],
        "review": review,
        "reviewSha256": PINS[review],
        "reviewDecision": REVIEW_BINDINGS[review]["decision"],
        "reviewBlockingFindingCount": REVIEW_BINDINGS[review]["blockingFindingCount"],
    }
    if extra:
        row.update(extra)
    return row


def build_dependencies(context: SemanticContext) -> dict[str, Any]:
    derived = context.derived
    projection = _dotted(context.rt22, "semanticBasisProjection")
    return {
        "evaluationProof": _dependency_row(EP8, EP8_CHECKER, EP8_REVIEW, {
            "acceptedVectorId": context.ep8["acceptedAuthorityVectorId"],
            "acceptedBundleCasRef": derived["values"]["evaluationProofBundleCasRef"],
        }),
        "retentionCustody": _dependency_row(RT22, RT22_CHECKER, RT22_REVIEW, {
            "acceptedClosureCommitment":
                derived["values"]["semanticCapabilityClosureCommitment"],
            "acceptedClosureCasRef":
                derived["values"]["semanticCapabilityClosureCasRef"],
            "semanticBasisArtifact": projection["sourceRetentionArtifact"],
            "semanticBasisSha256": projection["sourceRetentionSha256"],
        }),
        "terminationContract": _dependency_row(D9, D9_CHECKER, D9_REVIEW, {
            "referenceDerivation":
                _dotted(context.d9, "referenceDerivation.implementation"),
        }),
        "requestContext": _dependency_row(TRC3, TRC3_CHECKER, TRC3_REVIEW, {
            "capabilityType":
                _dotted(context.trc3, "capabilityContract.type"),
        }),
        "versioning": {
            "artifact": VERSIONING,
            "sha256": PINS[VERSIONING],
            "checker": VERSIONING_CHECKER,
            "checkerSha256": PINS[VERSIONING_CHECKER],
        },
        "dependencyDirection": (
            "EP8 and RT22 feed VERSIONING v8; the D9 v1.13 termination contract "
            "and the TrustedRequestContextV3 construction authority are "
            "consumed leaves. Evidence v9 binds all five and adds project-wide "
            "integrity enumeration plus serializable snapshot/CAS recovery. No "
            "dependency carries an Evidence back edge: none of the pinned "
            "dependency byte strings references this Evidence generation."),
    }


def build_grammar(predecessor_grammar: Any) -> dict[str, Any]:
    grammar = copy.deepcopy(predecessor_grammar)
    for path, before, after, _reason in GRAMMAR_DELTA:
        observed = _resolve(grammar, path)
        if observed != before:
            raise Malformed(
                f"predecessor grammar {path} is not the expected editorial base")
        _assign(grammar, path, after)
    return grammar


def build_recomputation_contract(derived: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "rule": (
            "Every published Evidence commitment is recomputed from the pinned "
            "evaluation-proof vector and the pinned retention closure under the "
            "tag table declared by canonicalWireGrammar. Byte equality with a "
            "predecessor is drift control and is never accepted as a substitute "
            "for recomputation."),
        "encoderSource": (
            "The record tags, field tags, field names and field order used by "
            "the checker are read from canonicalWireGrammar.records and "
            "canonicalWireGrammar.domainEnvelope of the candidate under test, "
            "so the grammar is mechanically consumed rather than documented."),
        "derivedFrom": {
            "evaluationProofVectorId": derived["vector"]["id"],
            "retentionClosureCommitment":
                derived["values"]["semanticCapabilityClosureCommitment"],
            "proofRefCount": len(derived["proofRefs"]),
        },
        "commitmentsRecomputed": [
            "RawProofInventoryV1 bytes",
            "SemanticEvidenceV1 bytes",
            "semanticEvidenceCasRef",
            "EvidenceDigest domain preimage",
            "EvidenceDigest",
            "RunIdentityPreimageV1 bytes",
            "RunId domain preimage",
            "RunId",
            "TerminalRunV1 bytes",
            "runSealRef",
            "universeCommitment",
            "outcomeSetCommitment",
            "verdictDerivationCommitment",
            "evaluationProofBundleCasRef",
            "semanticCapabilityClosureCasRef",
            "semanticCapabilityClosureCommitment",
            "all six runSubstitutionGoldens expectedRunId values",
        ],
        "rejectedSubstitutions": [
            "a valid-looking arbitrary digest at universeCommitment, "
            "outcomeSetCommitment or verdictDerivationCommitment",
            "a same-cardinality swap of universeCommitment and "
            "outcomeSetCommitment",
            "a same-shape substitution of one commitment for another",
            "a validly re-encoded inventory with one retained member dropped, "
            "added, substituted or reordered",
            "a self-consistently re-encoded SemanticEvidenceV1 carrying a lying "
            "commitment",
        ],
        "crossImplementationControl": {
            "artifact": V4_CHECKER,
            "sha256": PINS[V4_CHECKER],
            "rule": (
                "The retained independent framing, record and envelope "
                "primitives must reproduce the same bytes for all five records "
                "and both domain envelopes."),
        },
        "frozenHistoricalLabels": (
            "acceptedGolden.id and acceptedGolden.sourceVectorId are frozen "
            "labels from the predecessor generation. Neither is encoded into "
            "any record, enters any commitment, or is read by any derivation; "
            "the load-bearing accepted vector identity is "
            "dependencies.evaluationProof.acceptedVectorId, which is read from "
            "the pinned evaluation-proof artifact itself."),
    }


HOSTILE_INJECTIONS = ("null", "integer", "negative", "float", "true", "false",
                      "empty-text", "text", "empty-array", "empty-object",
                      "nested-array", "nested-object", "unknown-key")


def build_hostile_contract() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "rule": (
            "Every checking layer is total over hostile parsed JSON. Malformed "
            "input returns a deterministic finding and never an exception, at "
            "the root, at every root key and at every nested schema node."),
        "injections": list(HOSTILE_INJECTIONS),
        "requiredEscapes": 0,
        "measurement": (
            "The selftest calls the unguarded checking layers directly, so a "
            "broad exception handler cannot mask an escape. Both the unguarded "
            "escape count and the guarded escape count must be zero."),
        "exitDiscipline": (
            "An unexpected exception inside a layer becomes a reported finding "
            "and exit 1. An input that cannot be read or parsed exits 2. A "
            "selftest over a dirty base exits 3. Nothing exits 0 on a "
            "malformed candidate."),
    }


def build_checker_mode_contract() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "entrypoints": [
            "python3 -I -B artifacts/check-evidence-v9.py",
            "python3 -I -B artifacts/check-evidence-v9.py --selftest",
            "python3 -I -B artifacts/check-evidence-v9.py --emit-candidate",
        ],
        "startupTrustRoot": (
            "Caller-owned python3 -I -B. The in-script guard refuses any other "
            "invocation with exit 2; it cannot undo interpreter activity that "
            "happened before line 1."),
        "hashBeforeExecution": (
            "Every pinned byte string is read and SHA-256 verified before any "
            "of it is parsed, and retained Python authorities execute from the "
            "verified byte snapshot rather than from a second read."),
        "selftestReachability": (
            "There is no unconditional finding gate before the mutation suite "
            "and no second undocumented selftest entrypoint. --selftest always "
            "reaches the suite. If the base candidate is not clean the suite is "
            "refused with exit 3 and the dirty base is reported, because a "
            "mutation suite over a red base is not an oracle."),
        "escapeRule": (
            "A mutation that fails to apply, or that applies without changing "
            "the candidate bytes, is counted as an ESCAPE rather than as a "
            "pass."),
        "exitCodes": {"clean": 0, "findings": 1,
                      "unsupportedInvocationOrInput": 2,
                      "selftestRefusedDirtyBase": 3},
        "checkerScopeBoundary": (
            "A green run of this authored checker is checker-scope evidence "
            "ONLY. It demonstrates no production durability, atomicity, "
            "restart, crash or concurrency behavior, grants no seal, freeze, "
            "integration or product acceptance, and does not sign CD-RT-5. "
            "Independent re-review of the exact v9 bytes remains REQUIRED."),
    }


def _review_ids(review: Any, blocking_key: str,
                residual_key: str) -> tuple[list[str], list[str]]:
    if not isinstance(review, dict):
        raise Malformed("pinned review is not an object")
    def ids(key: str) -> list[str]:
        rows = review.get(key)
        if not isinstance(rows, list):
            raise Malformed(f"pinned review {key} is not an array")
        out = []
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise Malformed(f"pinned review {key}[{index}] has no string id")
            out.append(row["id"])
        return out
    return ids(blocking_key), ids(residual_key)


def build_review_transfers(context: SemanticContext) -> list[dict[str, Any]]:
    carried = context.predecessor.get("reviewFindingTransfers")
    if not isinstance(carried, list) or not carried:
        raise Malformed("predecessor reviewFindingTransfers is not a non-empty array")
    v7_blocking, v7_residual = _review_ids(
        context.authority.json(V7_REVIEW), "blockingFindings", "residualFindings")
    v8_blocking, v8_residual = _review_ids(
        context.review, "blockingFindings", "residuals")
    required = list(v7_blocking) + list(v7_residual) + \
        list(v8_blocking) + list(v8_residual)
    missing = [identifier for identifier in required
               if identifier not in DISPOSITIONS]
    if missing:
        raise Malformed("no disposition authored for " + ", ".join(missing))
    extra = [identifier for identifier in DISPOSITIONS if identifier not in required]
    if extra:
        raise Malformed("disposition names an identifier no pinned review "
                        "reports: " + ", ".join(extra))
    transfers = [copy.deepcopy(row) for row in carried]
    for identifier in required:
        row = DISPOSITIONS[identifier]
        source = V7_REVIEW if identifier.startswith("EV7-") else PREDECESSOR_REVIEW
        transfers.append({
            "id": identifier,
            "source": source,
            "sourceSha256": PINS[source],
            "state": row["state"],
            "closure": row["closure"],
            "provenBy": list(row["provenBy"]),
        })
    return transfers


def build_foundation(predecessor_foundation: Any) -> dict[str, Any]:
    if not isinstance(predecessor_foundation, dict):
        raise Malformed("predecessor foundationImplementation is not an object")
    foundation = copy.deepcopy(predecessor_foundation)
    if foundation.get("status") != "PARTIAL-CANDIDATE-RED":
        raise Malformed("predecessor foundation status is not the expected base")
    previous_todos = foundation.get("blockingTodos")
    if not isinstance(previous_todos, list) or len(previous_todos) != 3:
        raise Malformed("predecessor foundation does not declare three TODOs")
    foundation["status"] = "CANDIDATE-COMPLETE-CHECKER-SCOPE"
    foundation["blockingTodos"] = []
    foundation["closedTodos"] = [
        {"todo": previous_todos[0],
         "closure": (
             "Closed. d9-exit-contract.v1.13 and retention-tiers.v22 are each "
             "independently accepted with zero blocking findings, are pinned by "
             "exact SHA-256, and the termination class, ordered code payload "
             "and exit code of every d9Mapping row are produced by calling the "
             "pinned D9 reference derivation."),
         "provenBy": ["PR-05-D9-LIVE-DERIVATION", "PR-09-RETENTION-CHECKER-GREEN",
                      "PR-10-TERMINATION-CHECKER-GREEN"]},
        {"todo": previous_todos[1],
         "closure": (
             "Closed. trusted-request-context.v3 is independently accepted with "
             "zero blocking findings and is pinned by exact SHA-256. "
             "requestContextBinding projects its construction authority; the "
             "opaque predecessor test fixture is no longer the authority."),
         "provenBy": ["PR-06-REQUEST-CONTEXT-AUTHORITY"]},
        {"todo": previous_todos[2],
         "closure": (
             "Closed. The complete expected successor object is derived from "
             "the pinned predecessor and dependency bytes and compared for "
             "exact equality, and the semantic binding registry binds the "
             "changed-root obligations to predicates evaluated against pinned "
             "authority."),
         "provenBy": ["PR-18-EXPECTED-SUCCESSOR-EQUALITY",
                      "PR-20-SEMANTIC-BINDING-REGISTRY"]},
    ]
    foundation["retainedPredecessorFoundation"] = {
        "artifact": PREDECESSOR,
        "sha256": PINS[PREDECESSOR],
        "checker": PREDECESSOR_CHECKER,
        "checkerSha256": PINS[PREDECESSOR_CHECKER],
        "execution": (
            "The predecessor foundation contract, its executable probes and its "
            "complete authored mutation suite are executed against the pinned "
            "predecessor bytes from the verified snapshot on every run of this "
            "checker. The predecessor's own unconditional TODO gate is not "
            "carried; it is answered."),
        "provenBy": ["PR-07-RETAINED-PREDECESSOR-FOUNDATION",
                     "PR-08-RETAINED-PREDECESSOR-MUTATION-SUITE"],
    }
    return foundation


RESIDUALS_V9: tuple[str, ...] = (
    "The checker uses guarded durable-state and session test doubles plus "
    "copy/validate/swap. No production store, transaction, restart, crash "
    "durability or atomicity implementation was executed or demonstrated. The "
    "evidence grade remains IMPLEMENTABLE_UNEXECUTED and independent "
    "re-review of these exact bytes remains REQUIRED.",
    "A1-RTV4-02 is retained as a measurement residual. This artifact claims no "
    "cost advantage, no orders-of-magnitude advantage and no measured "
    "performance property of any kind.",
    "All Evidence v5/v6/v7/v8 SemanticEvidence, EvidenceDigest, RunId, "
    "TerminalRun and runSeal identities are unchanged. This successor changes "
    "how those identities are PROVED, not what they are: every published "
    "commitment now recomputes from the pinned dependencies instead of being "
    "carried.",
    "V10 remains unresolved. CD-RT-5 and G19 remain blocked. This artifact "
    "does not decide the product default and does not sign CD-RT-5.",
    "EV8-IR-R3 is retained: genuinely new prose in this successor is authored "
    "in the checker that emits it, so for that prose the equality comparison "
    "proves self-consistency only. The executable probes and the pinned "
    "dependency predicates, not the prose, are the semantic oracle.",
    "EV7-PF-R01 and EV8-IR-R6 are carried forward unverified: the 23-object "
    "acquire/retry/release, pending-expiry, crash-gap repin and contention "
    "probes are executed only by the retained predecessor foundation and have "
    "not been independently reimplemented.",
    "EV7-PF-R03 is carried forward: the recovery matrix alias rows inside the "
    "retained predecessor foundation remain author-summarised and are not "
    "claimed to be executed.",
    "acceptedGolden.id and acceptedGolden.sourceVectorId remain frozen labels "
    "from the predecessor generation. They enter no commitment and no encoded "
    "record; the load-bearing accepted vector identity is read from the pinned "
    "evaluation-proof artifact.",
    "The grammar is bound to the encoder through its machine-readable tag, "
    "field-name and field-order table. The prose of the scalar and record "
    "rules is checked for the exact set rule only; the remaining prose is not "
    "parsed and could still diverge from the table without detection.",
)

CARRIED_ROOT_ORDER_HINT = (
    "supersedes", "authority", "reviewFindingTransfers",
    "recursiveRequestIdExclusion", "dependencies", "importedAuthorityContract",
    "assurance", "canonicalWireGrammar", "semanticJoins",
    "persistedVsProjection", "apiContract", "storeContract",
    "admissionAndSealOrdering", "sealedCapabilityContract", "d9Mapping",
    "acceptedGolden", "runSubstitutionGoldens", "positiveControls",
    "adversarialControls", "invariants", "retainedResiduals",
    "sealRecommendation", "runAuthorityIndexContract",
    "correlationDifferential", "availabilityDifferential",
    "storeCapabilityContinuityContract", "identityStabilityFromEvidenceV5",
    "identityStabilityFromEvidenceV6", "durableRecoveryContract",
    "recoveryMatrixContract", "successorDelta", "foundationImplementation",
)


def expected_successor(authority: Authority) -> dict[str, Any]:
    """Derive the complete expected evidence.v9 object."""
    predecessor = authority.json(PREDECESSOR)
    if not isinstance(predecessor, dict):
        raise Malformed("predecessor evidence root is not an object")
    grammar = build_grammar(predecessor.get("canonicalWireGrammar"))
    derived = derive_identity(grammar, authority.json(EP8), authority.json(RT22))
    d9_mapping = derive_d9_mapping(authority)
    request_context = derive_request_context_binding(authority)
    context = SemanticContext(authority, derived, d9_mapping, request_context)
    registry_entries = semantic_entries(context)

    successor: dict[str, Any] = {}
    for key, value in predecessor.items():
        successor[key] = copy.deepcopy(value)
    successor["version"] = 9
    successor["status"] = EXPECTED_STATUS
    successor["role"] = EXPECTED_ROLE
    successor["author"] = EXPECTED_AUTHOR
    successor["date"] = EXPECTED_DATE
    successor["supersedes"] = {
        "artifact": PREDECESSOR,
        "sha256": PINS[PREDECESSOR],
        "checker": PREDECESSOR_CHECKER,
        "checkerSha256": PINS[PREDECESSOR_CHECKER],
        "review": PREDECESSOR_REVIEW,
        "reviewSha256": PINS[PREDECESSOR_REVIEW],
        "reviewDecision": REVIEW_BINDINGS[PREDECESSOR_REVIEW]["decision"],
        "lineagePredecessor": V7,
        "lineagePredecessorSha256": PINS[V7],
        "lineageRejection": V7_REVIEW,
        "lineageRejectionSha256": PINS[V7_REVIEW],
    }
    successor["reviewFindingTransfers"] = build_review_transfers(context)
    successor["dependencies"] = build_dependencies(context)
    successor["canonicalWireGrammar"] = grammar
    successor["d9Mapping"] = d9_mapping
    successor["acceptedGolden"] = golden_from_identity(
        predecessor.get("acceptedGolden"), derived)
    successor["runSubstitutionGoldens"] = copy.deepcopy(derived["substitutions"])
    successor["retainedResiduals"] = list(RESIDUALS_V9)
    successor["foundationImplementation"] = build_foundation(
        predecessor.get("foundationImplementation"))
    successor["evidenceRecomputationContract"] = build_recomputation_contract(derived)
    successor["requestContextBinding"] = request_context
    successor["semanticBindingRegistry"] = {
        "schemaVersion": 1,
        "rule": (
            "Each entry carries a prose claim, a closed machine-readable "
            "predicate and the artifact leaf paths whose semantic content it "
            "underwrites. The checker requires the prose to equal the "
            "deterministic rendering of the predicate AND requires the "
            "predicate to evaluate true against pinned dependency bytes. "
            "Editing the prose alone fails rendering; editing the predicate "
            "alone fails evaluation; editing both consistently fails "
            "evaluation. A declaration can therefore not act as its own "
            "oracle."),
        "escapeCoverageRule": (
            "Every leaf path listed by an entry must exist in this artifact, "
            "and the union of the listed paths must cover every surface the "
            "independent predecessor review reported as escaping or "
            "semantically unbound."),
        "entries": registry_entries,
    }
    successor["hostileInputTotalityContract"] = build_hostile_contract()
    successor["checkerModeContract"] = build_checker_mode_contract()

    added = [key for key in successor if key not in predecessor]
    changed = sorted(
        key for key in successor
        if key in predecessor and (
            key == "successorDelta" or successor[key] != predecessor[key]))
    carried = sorted(key for key in successor
                     if key in predecessor and key not in changed)
    successor["successorDelta"] = {
        "predecessor": f"{PREDECESSOR}@{PINS[PREDECESSOR]}",
        "predecessorChecker": f"{PREDECESSOR_CHECKER}@{PINS[PREDECESSOR_CHECKER]}",
        "rejection": f"{PREDECESSOR_REVIEW}@{PINS[PREDECESSOR_REVIEW]}",
        "rejectionDecision": REVIEW_BINDINGS[PREDECESSOR_REVIEW]["decision"],
        "rejectionBlockingFindingCount":
            REVIEW_BINDINGS[PREDECESSOR_REVIEW]["blockingFindingCount"],
        "changedRootKeys": changed,
        "addedRootKeys": sorted(added),
        "carriedRootKeys": carried,
        "protectedIdentityKeys": [],
        "grammarEditorialDelta": [
            {"path": path, "predecessorValue": before, "successorValue": after,
             "reason": reason}
            for path, before, after, reason in GRAMMAR_DELTA],
        "retainedHistoricalLabelPaths": list(RETAINED_HISTORICAL_LABEL_PATHS),
        "scope": (
            "There is no protected-identity freeze in this generation. The "
            "checker derives the complete expected successor object from the "
            "pinned predecessor bytes plus the pinned dependency bytes and "
            "requires exact equality, so every leaf is derived rather than "
            "declared. Carried roots equal the predecessor exactly; changed "
            "and added roots are recomputed from pinned authority or emitted "
            "by the same construction the checker verifies. Text-substring "
            "sampling is not a successor oracle, and freezing a root by "
            "byte-equality alone is not treated as semantic binding."),
    }
    authority.context = context
    authority.expected = successor
    return successor


# ---------------------------------------------------------------------------
# Section 6.  Total checking layers and the executed probe registry.
# ---------------------------------------------------------------------------

def _kind(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "text"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _first_difference(actual: Any, expected: Any, path: str = "") -> str | None:
    """Total structural comparison; never raises on hostile input."""
    label = path or "<root>"
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return f"{label}: expected object, found {_kind(actual)}"
        missing = [key for key in expected if key not in actual]
        if missing:
            return f"{label}: missing key {sorted(missing)[0]!r}"
        unknown = [key for key in actual if key not in expected]
        if unknown:
            return f"{label}: unknown key {sorted(unknown)[0]!r}"
        for key in expected:
            found = _first_difference(actual[key], expected[key],
                                      f"{path}.{key}" if path else str(key))
            if found is not None:
                return found
        return None
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return f"{label}: expected array, found {_kind(actual)}"
        if len(actual) != len(expected):
            return (f"{label}: expected {len(expected)} items, "
                    f"found {len(actual)}")
        for index, item in enumerate(expected):
            found = _first_difference(actual[index], item, f"{path}[{index}]")
            if found is not None:
                return found
        return None
    if isinstance(expected, bool) or isinstance(actual, bool):
        if actual is not expected:
            return f"{label}: expected {expected!r}, found {actual!r}"
        return None
    if actual != expected or _kind(actual) != _kind(expected):
        return f"{label}: expected {expected!r}, found {actual!r}"
    return None


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            if isinstance(key, str):
                yield key
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def _string_leaves(value: Any, prefix: str = ""):
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key, child in value.items():
            joined = f"{prefix}.{key}" if prefix else str(key)
            yield from _string_leaves(child, joined)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _string_leaves(child, f"{prefix}[{index}]")


def candidate_recomputation_findings(candidate: Any,
                                     authority: Authority) -> list[str]:
    """Recompute from the CANDIDATE's own grammar; total over hostile input."""
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return [f"<root>: expected object, found {_kind(candidate)}"]
    try:
        derived = derive_identity(candidate.get("canonicalWireGrammar"),
                                  authority.json(EP8), authority.json(RT22))
    except Malformed as exc:
        return [f"candidate-driven recomputation refused: {exc}"]
    golden = candidate.get("acceptedGolden")
    if not isinstance(golden, dict):
        return [f"acceptedGolden: expected object, found {_kind(golden)}"]
    expected_golden = None
    try:
        expected_golden = golden_from_identity(golden, derived)
    except Malformed as exc:
        findings.append(f"acceptedGolden cannot be rebuilt: {exc}")
    if expected_golden is not None:
        difference = _first_difference(golden, expected_golden, "acceptedGolden")
        if difference is not None:
            findings.append(
                "acceptedGolden is not the recomputation of the pinned "
                f"evaluation-proof vector and retention closure: {difference}")
    embedded = derived["inventory"].hex()
    if embedded not in derived["semantic"].hex():
        findings.append("SemanticEvidenceV1 does not embed the derived inventory")
    substitutions = candidate.get("runSubstitutionGoldens")
    difference = _first_difference(substitutions, derived["substitutions"],
                                   "runSubstitutionGoldens")
    if difference is not None:
        findings.append(f"run substitution goldens are not recomputed: {difference}")
    run_ids = {derived["runId"]}
    for row in derived["substitutions"]:
        run_ids.add(row["expectedRunId"])
    if len(run_ids) != 1 + len(derived["substitutions"]):
        findings.append("run substitution goldens are not pairwise distinct")
    authority.record_probe("PR-01-GRAMMAR-RECOMPUTATION", not findings)
    authority.record_probe("PR-04-RUN-SUBSTITUTION-GOLDENS", not findings)
    return findings


def pinned_finding_ids(authority: Authority) -> frozenset[str]:
    """Identifiers read live from the pinned reviews are quoted vocabulary.

    A predecessor finding identifier may legitimately carry a stale generation
    label because the reviewer named it that way; the identifier is not an
    Evidence surface assertion and is exempt from the nomenclature scans.
    """
    identifiers: set[str] = set()
    for name, blocking_key, residual_key in (
            (V7_REVIEW, "blockingFindings", "residualFindings"),
            (PREDECESSOR_REVIEW, "blockingFindings", "residuals")):
        try:
            blocking, residual = _review_ids(
                authority.json(name), blocking_key, residual_key)
        except Malformed:
            continue
        identifiers.update(blocking)
        identifiers.update(residual)
    return frozenset(identifiers)


def _nomenclature_findings(candidate: Any,
                           exempt: frozenset[str] = frozenset()) -> list[str]:
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["nomenclature scan requires an object root"]
    for text in _walk_strings(candidate):
        if text in exempt:
            continue
        if FORBIDDEN_ALIAS_RE.search(text):
            findings.append(f"forbidden custody-root alias on an E9 surface: {text[:60]!r}")
            break
    for text in _walk_strings(candidate):
        if text in exempt:
            continue
        match = STALE_GENERATION_RE.search(text)
        if match:
            findings.append(
                f"stale current-generation nomenclature {match.group(0)!r}: {text[:60]!r}")
            break
    observed = sorted({path for path, text in _string_leaves(candidate)
                       if text not in exempt and HISTORICAL_LABEL_RE.search(text)})
    declared = sorted(RETAINED_HISTORICAL_LABEL_PATHS)
    if observed != declared:
        unexpected = [path for path in observed if path not in declared]
        stale = [path for path in declared if path not in observed]
        if unexpected:
            findings.append(
                "predecessor-generation label at an undeclared path: "
                + unexpected[0])
        if stale:
            findings.append(
                "declared historical-label path carries no such label: " + stale[0])
    return findings


def _disposition_findings(candidate: Any, authority: Authority) -> list[str]:
    findings: list[str] = []
    transfers = candidate.get("reviewFindingTransfers") \
        if isinstance(candidate, dict) else None
    if not isinstance(transfers, list):
        return [f"reviewFindingTransfers: expected array, found {_kind(transfers)}"]
    try:
        v7_blocking, v7_residual = _review_ids(
            authority.json(V7_REVIEW), "blockingFindings", "residualFindings")
        v8_blocking, v8_residual = _review_ids(
            authority.json(PREDECESSOR_REVIEW), "blockingFindings", "residuals")
    except Malformed as exc:
        return [f"pinned review identifiers cannot be read: {exc}"]
    required = set(v7_blocking) | set(v7_residual) | set(v8_blocking) | set(v8_residual)
    # This layer IS probe PR-17.  Seed it so an entry may cite it; the final
    # record_probe below conjoins the real outcome and can only lower it.
    authority.probe_log.setdefault("PR-17-FINDING-DISPOSITION-CLOSURE", True)
    present: set[str] = set()
    for index, row in enumerate(transfers):
        if not isinstance(row, dict):
            findings.append(f"reviewFindingTransfers[{index}] is not an object")
            continue
        identifier = row.get("id")
        if not isinstance(identifier, str):
            findings.append(f"reviewFindingTransfers[{index}].id is not text")
            continue
        present.add(identifier)
        if identifier not in required:
            continue
        state = row.get("state")
        if state not in ALL_STATES:
            findings.append(
                f"{identifier}: state {state!r} is outside the closed set")
            continue
        proven = row.get("provenBy")
        if not isinstance(proven, list):
            findings.append(f"{identifier}: provenBy is not an array")
            continue
        if state in CLOSED_STATES and not proven:
            findings.append(
                f"{identifier}: declares {state} without naming an executed probe")
        for probe in proven:
            if probe not in PROBE_IDS:
                findings.append(f"{identifier}: names unknown probe {probe!r}")
            elif authority.probe_log.get(probe) is not True:
                findings.append(
                    f"{identifier}: names probe {probe} which did not run "
                    "and pass in this invocation")
    missing = sorted(required - present)
    if missing:
        findings.append(
            f"{len(missing)} pinned review finding(s) have no disposition, "
            f"first {missing[0]}")
    fabricated = sorted(
        identifier for identifier in present
        if (identifier.startswith("EV7-PF") or identifier.startswith("EV8-IR"))
        and identifier not in required)
    if fabricated:
        findings.append(
            f"fabricated predecessor finding disposition {fabricated[0]}")
    authority.record_probe("PR-17-FINDING-DISPOSITION-CLOSURE", not findings)
    return findings


def _registry_findings(candidate: Any, authority: Authority) -> list[str]:
    findings: list[str] = []
    context = getattr(authority, "context", None)
    if context is None:
        return ["semantic binding registry has no derivation context"]
    registry = candidate.get("semanticBindingRegistry") \
        if isinstance(candidate, dict) else None
    if not isinstance(registry, dict):
        return [f"semanticBindingRegistry: expected object, found {_kind(registry)}"]
    entries = registry.get("entries")
    if not isinstance(entries, list) or not entries:
        return ["semanticBindingRegistry.entries is not a non-empty array"]
    covered: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            findings.append(f"semanticBindingRegistry.entries[{index}] is not an object")
            continue
        identifier = entry.get("id")
        claim = entry.get("claim")
        if not isinstance(identifier, str) or not isinstance(claim, str):
            findings.append(
                f"semanticBindingRegistry.entries[{index}] has no id/claim text")
            continue
        try:
            rendered = _render(entry.get("kind"), entry.get("params") or {})
        except (Malformed, KeyError, TypeError, ValueError, IndexError) as exc:
            findings.append(f"{identifier}: predicate cannot be rendered: {exc}")
            continue
        if rendered != claim:
            findings.append(
                f"{identifier}: prose claim is not the rendering of its predicate")
            continue
        try:
            passed, detail = evaluate_semantic_entry(entry, context)
        except (Malformed, KeyError, TypeError, ValueError, IndexError) as exc:
            findings.append(
                f"{identifier}: predicate evaluation refused: "
                f"{type(exc).__name__}: {exc}")
            continue
        if not passed:
            findings.append(f"{identifier}: predicate is false against pinned "
                            f"authority ({detail})")
            continue
        paths = entry.get("boundArtifactPaths")
        if not isinstance(paths, list) or not paths:
            findings.append(f"{identifier}: boundArtifactPaths is empty")
            continue
        for path in paths:
            try:
                _resolve(candidate, str(path))
            except Malformed:
                findings.append(f"{identifier}: bound path {path} is absent")
                continue
            covered.add(str(path))
        probe = entry.get("provenBy")
        if probe not in PROBE_IDS:
            findings.append(f"{identifier}: provenBy {probe!r} is not a probe id")
    missing = [surface for surface in REVIEW_ESCAPE_SURFACES
               if not any(path == surface or path.startswith(surface + ".") or
                          surface.startswith(path + ".") or path == surface
                          for path in covered)]
    if missing:
        findings.append(
            f"{len(missing)} independently reported escaping surface(s) are not "
            f"covered by the registry, first {missing[0]}")
    authority.record_probe("PR-20-SEMANTIC-BINDING-REGISTRY", not findings)
    return findings


# The exact surfaces the independent predecessor review reported as escaping
# (P3, 22 cases) or semantically unbound (P5, 6 cases).  Every one must be
# covered by the semantic binding registry.
REVIEW_ESCAPE_SURFACES: tuple[str, ...] = (
    "dependencies.evaluationProof.acceptedVectorId",
    "dependencies.retentionCustody.acceptedClosureCommitment",
    "dependencies.dependencyDirection",
    "invariants",
    "semanticJoins.retention",
    "semanticJoins.versioning",
    "sealedCapabilityContract.productFork",
    "recursiveRequestIdExclusion.rule",
    "recursiveRequestIdExclusion.surfaces",
    "recursiveRequestIdExclusion.negativeControl",
    "acceptedGolden.values",
    "acceptedGolden.rawProofInventoryHex",
    "d9Mapping.rows",
    "authority",
    "assurance",
    "sealRecommendation",
    "reviewFindingTransfers",
)


def run_dependency_probes(authority: Authority) -> list[str]:
    """Execute every pinned authority from its verified snapshot."""
    findings: list[str] = []
    context = getattr(authority, "context", None)
    sink = io.StringIO()

    def guarded(probe_id: str, action: Callable[[], list[str] | int]) -> None:
        try:
            with redirect_stdout(sink):
                outcome = action()
        except Exception as exc:                      # noqa: BLE001 - reported
            findings.append(f"{probe_id}: raised {type(exc).__name__}: {exc}")
            authority.record_probe(probe_id, False)
            return
        if isinstance(outcome, int):
            ok = outcome == 0
            detail = f"exit {outcome}"
        else:
            ok = not outcome
            detail = (outcome[0] if outcome else "")
        if not ok:
            findings.append(f"{probe_id}: {detail}")
        authority.record_probe(probe_id, ok)

    v8 = authority.module(PREDECESSOR_CHECKER)
    predecessor = authority.json(PREDECESSOR)
    guarded("PR-07-RETAINED-PREDECESSOR-FOUNDATION",
            lambda: v8._foundation_contract_errors(
                copy.deepcopy(predecessor), run_probes=True))
    guarded("PR-08-RETAINED-PREDECESSOR-MUTATION-SUITE",
            lambda: v8.foundation_selftest(copy.deepcopy(predecessor)))
    guarded("PR-09-RETENTION-CHECKER-GREEN",
            lambda: authority.module(RT22_CHECKER).main([RT22_CHECKER]))
    d9mod = authority.module(D9_CHECKER)
    guarded("PR-10-TERMINATION-CHECKER-GREEN",
            lambda: d9mod._check_contract(
                authority.json(D9), d9mod._BOOTSTRAP_AUTHORITY,
                authority.snapshots[D9]))
    guarded("PR-11-EVALUATION-PROOF-CHECKER-GREEN",
            lambda: authority.module(EP8_CHECKER).check(authority.json(EP8)))
    guarded("PR-22-VERSIONING-CHECKER-GREEN",
            lambda: authority.module(VERSIONING_CHECKER).check(
                authority.json(VERSIONING)))
    guarded("PR-06-REQUEST-CONTEXT-AUTHORITY",
            lambda: authority.module(TRC3_CHECKER).check(authority.json(TRC3)))

    if context is None:
        findings.append("dependency probes have no derivation context")
        return findings
    derived = context.derived

    def cross_implementation() -> list[str]:
        v4 = authority.module(V4_CHECKER)
        problems: list[str] = []
        items = sorted(v4.record(0x80, [
            v4.frame(0x85, row["recordCasRef"]),
            v4.frame(0x86, row["recordKind"]),
            v4.frame(0x87, row["requiredForCapability"]),
        ]) for row in derived["proofRefs"])
        inventory = v4.record(0x81, [
            v4.frame(0x88, 1),
            v4.frame(0x89, derived["values"]["projectId"]),
            v4.frame(0x8A, b"".join(v4.frame(0x8B, item) for item in items)),
        ])
        if inventory != derived["inventory"]:
            problems.append("retained implementation disagrees on RawProofInventoryV1")
        if v4.envelope(DOMAIN_SEMANTIC_EVIDENCE, derived["semantic"]) != \
                derived["semanticPreimage"]:
            problems.append("retained implementation disagrees on the evidence envelope")
        if v4.envelope(DOMAIN_RUN_ID, derived["runRecord"]) != derived["runPreimage"]:
            problems.append("retained implementation disagrees on the run envelope")
        if v4.sha_ref(derived["semanticPreimage"]) != derived["evidenceDigest"]:
            problems.append("retained implementation disagrees on EvidenceDigest")
        if v4.canonical_json_bytes(derived["closure"]) != canonical(derived["closure"]):
            problems.append("retained implementation disagrees on canonical JSON")
        return problems

    guarded("PR-12-CROSS-IMPLEMENTATION-WIRE-CONTROL", cross_implementation)

    def inventory_member_binding() -> list[str]:
        problems: list[str] = []
        codec = derived["codec"]
        refs = derived["proofRefs"]
        project = derived["values"]["projectId"]

        def rebuild(rows: list[Any]) -> bytes:
            return codec.emit("RawProofInventoryV1", {
                "schemaVersion": 1, "projectId": project,
                "items": codec.inventory_items(rows)})

        if len(refs) < 3:
            return ["retention closure has too few members to falsify"]
        dropped = rebuild([row for row in refs[1:]])
        if dropped == derived["inventory"]:
            problems.append("dropping a retained member does not change the inventory")
        substituted = copy.deepcopy(refs)
        substituted[0] = dict(substituted[0])
        substituted[0]["recordCasRef"] = "sha256:" + "e" * 64
        if rebuild(substituted) == derived["inventory"]:
            problems.append("substituting a member does not change the inventory")
        added = copy.deepcopy(refs) + [{
            "identityKind": "raw-cas", "projectId": project,
            "recordCasRef": "sha256:" + "f" * 64,
            "recordKind": "historical-manifest",
            "requiredForCapability": "verifiable"}]
        if rebuild(added) == derived["inventory"]:
            problems.append("adding a member does not change the inventory")
        reordered = list(reversed(copy.deepcopy(refs)))
        if rebuild(reordered) != derived["inventory"]:
            problems.append("the item set commitment is order sensitive")
        duplicated = copy.deepcopy(refs) + [copy.deepcopy(refs[0])]
        try:
            rebuild(duplicated)
        except Malformed:
            pass
        else:
            problems.append("a duplicate member is silently deduplicated")
        if derived["inventory"] == derived["inventoryWrapperSorted"]:
            problems.append("wrapper-sorted and item-sorted inventories coincide, "
                            "so the disambiguation is untestable on this data")
        return problems

    guarded("PR-02-INVENTORY-MEMBER-BINDING", inventory_member_binding)

    def ep_commitment_derivation() -> list[str]:
        problems: list[str] = []
        bundle = derived["bundle"]
        values = derived["values"]
        pairs = (
            ("universeCommitment",
             _dotted(bundle, "requiredUniverse.universeCommitment")),
            ("outcomeSetCommitment",
             _dotted(bundle, "verdictProof.outcomeSetCommitment")),
            ("verdictDerivationCommitment",
             _dotted(bundle, "verdictProof.derivationCommitment")),
            ("verdict", _dotted(bundle, "verdictProof.verdict")),
        )
        for name, expected in pairs:
            if values[name] != expected:
                problems.append(f"{name} is not the accepted vector's value")
        universe = _dotted(bundle, "requiredUniverse")
        members = universe.get("memberIds")
        if not isinstance(members, list) or \
                universe.get("declaredCount") != len(members):
            problems.append("requiredUniverse declaredCount does not equal its members")
        partitions = bundle.get("partitionContents")
        if not isinstance(partitions, list) or not partitions:
            problems.append("the no-match claim has no partitionContents")
        codec = derived["codec"]
        for name in ("universeCommitment", "outcomeSetCommitment",
                     "verdictDerivationCommitment"):
            hostile = dict(values)
            hostile[name] = "sha256:" + "1" * 64
            if _reencode_semantic(codec, derived, hostile) == derived["semantic"]:
                problems.append(f"an arbitrary digest at {name} leaves the bytes equal")
        swapped = dict(values)
        swapped["universeCommitment"], swapped["outcomeSetCommitment"] = \
            values["outcomeSetCommitment"], values["universeCommitment"]
        if _reencode_semantic(codec, derived, swapped) == derived["semantic"]:
            problems.append("a same-cardinality commitment swap leaves the bytes equal")
        shaped = dict(values)
        shaped["universeCommitment"] = values["outcomeSetCommitment"]
        if _reencode_semantic(codec, derived, shaped) == derived["semantic"]:
            problems.append("a same-shape commitment substitution leaves the bytes equal")
        return problems

    guarded("PR-03-EP-COMMITMENT-DERIVATION", ep_commitment_derivation)

    def d9_live() -> list[str]:
        mapping = context.d9_mapping
        rebuilt = derive_d9_mapping(authority)
        difference = _first_difference(mapping, rebuilt, "d9Mapping")
        return [] if difference is None else [difference]

    guarded("PR-05-D9-LIVE-DERIVATION", d9_live)

    def token_exclusion() -> list[str]:
        problems: list[str] = []
        blobs = {
            "RawProofInventoryV1": derived["inventory"],
            "SemanticEvidenceV1": derived["semantic"],
            "EvidenceDigest preimage": derived["semanticPreimage"],
            "RunIdentityPreimageV1": derived["runRecord"],
            "RunId preimage": derived["runPreimage"],
            "TerminalRunV1": derived["terminal"],
        }
        for token in OPERATIONAL_TOKENS:
            needle = token.encode("utf-8")
            for name, blob in blobs.items():
                if needle in blob:
                    problems.append(f"{name} carries operational token {token!r}")
        return problems

    guarded("PR-14-OPERATIONAL-TOKEN-EXCLUSION", token_exclusion)

    def acyclicity() -> list[str]:
        problems: list[str] = []
        for name in (EP8, RT22, D9, TRC3, VERSIONING):
            if b"evidence.v9" in authority.snapshots[name]:
                problems.append(f"{name} carries an Evidence v9 back edge")
        return problems

    guarded("PR-16-DEPENDENCY-ACYCLICITY", acyclicity)
    return findings


def _reencode_semantic(codec: "WireCodec", derived: Mapping[str, Any],
                       values: Mapping[str, Any]) -> bytes:
    return codec.emit("SemanticEvidenceV1", {
        "schemaVersion": 1,
        "projectId": values["projectId"],
        "planId": values["planId"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "evaluationProofBundleCasRef": values["evaluationProofBundleCasRef"],
        "universeCommitment": values["universeCommitment"],
        "outcomeSetCommitment": values["outcomeSetCommitment"],
        "verdictDerivationCommitment": values["verdictDerivationCommitment"],
        "verdict": values["verdict"],
        "sealedCapability": values["sealedCapability"],
        "rawProofInventory": derived["inventory"],
        "semanticCapabilityClosureCasRef": values["semanticCapabilityClosureCasRef"],
        "semanticCapabilityClosureCommitment":
            values["semanticCapabilityClosureCommitment"],
    })


def _producer_obligation_findings(candidate: Any,
                                  authority: Authority) -> list[str]:
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["producer obligation scan requires an object root"]
    for path, expected in NO_AUTHORITY_FACTS:
        try:
            observed = _resolve(candidate, path)
        except Malformed as exc:
            findings.append(f"producer obligation: {exc}")
            continue
        if observed != expected:
            findings.append(
                f"producer obligation {path} is {observed!r}, expected {expected!r}")
    for text in _walk_strings(candidate):
        if re.search(r"CD-RT-5\s+(?:is\s+)?(?:signed|granted|accepted|closed)", text):
            findings.append("the artifact self-signs CD-RT-5")
            break
    authority.record_probe("PR-15-PRODUCER-OBLIGATION", not findings)
    return findings


def _grammar_delta_findings(candidate: Any, authority: Authority) -> list[str]:
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["grammar delta scan requires an object root"]
    grammar = candidate.get("canonicalWireGrammar")
    base = authority.json(PREDECESSOR).get("canonicalWireGrammar")
    if not isinstance(grammar, dict) or not isinstance(base, dict):
        return ["canonicalWireGrammar is not an object on both generations"]
    declared = _resolve(candidate, "successorDelta.grammarEditorialDelta") \
        if isinstance(candidate.get("successorDelta"), dict) and \
        isinstance(candidate["successorDelta"].get("grammarEditorialDelta"), list) \
        else None
    if declared is None:
        return ["successorDelta.grammarEditorialDelta is absent or not an array"]
    observed: dict[str, tuple[Any, Any]] = {}
    base_leaves = dict(_string_leaves(base))
    new_leaves = dict(_string_leaves(grammar))
    for path, value in new_leaves.items():
        if base_leaves.get(path) != value:
            observed[path] = (base_leaves.get(path), value)
    for path in base_leaves:
        if path not in new_leaves:
            observed[path] = (base_leaves[path], None)
    declared_paths: list[str] = []
    for index, row in enumerate(declared):
        if not isinstance(row, dict):
            findings.append(f"grammarEditorialDelta[{index}] is not an object")
            continue
        path = row.get("path")
        if not isinstance(path, str):
            findings.append(f"grammarEditorialDelta[{index}].path is not text")
            continue
        declared_paths.append(path)
        leaf = _path_steps(path)[-1]
        if leaf in GRAMMAR_DELTA_FORBIDDEN_LEAVES:
            findings.append(
                f"grammarEditorialDelta[{index}] edits derivation-relevant leaf {leaf!r}")
        if base_leaves.get(path) != row.get("predecessorValue"):
            findings.append(
                f"grammarEditorialDelta[{index}] predecessorValue is not the live "
                "predecessor value")
        if new_leaves.get(path) != row.get("successorValue"):
            findings.append(
                f"grammarEditorialDelta[{index}] successorValue is not the live "
                "successor value")
    if sorted(declared_paths) != sorted(observed):
        undeclared = sorted(set(observed) - set(declared_paths))
        phantom = sorted(set(declared_paths) - set(observed))
        if undeclared:
            findings.append(f"undeclared grammar edit at {undeclared[0]}")
        if phantom:
            findings.append(f"declared grammar edit does not exist at {phantom[0]}")
    try:
        base_codec = WireCodec(base)
        new_codec = WireCodec(grammar)
    except Malformed as exc:
        findings.append(f"grammar tag table refused: {exc}")
        return findings
    if base_codec.record_tag != new_codec.record_tag or \
            base_codec.fields != new_codec.fields or \
            (base_codec.envelope_tag, base_codec.domain_tag,
             base_codec.payload_tag) != (new_codec.envelope_tag,
                                         new_codec.domain_tag,
                                         new_codec.payload_tag):
        findings.append("the editorial delta changed the derivation tag table")
    return findings


def _source_findings(source: Any, expected: Mapping[str, Any]) -> list[str]:
    if not isinstance(source, (bytes, bytearray)):
        return []
    canonical_source = pretty(expected)
    if bytes(source) != canonical_source:
        return ["candidate file bytes are not the canonical emission of the "
                "derived successor (run --emit-candidate to see the exact bytes)"]
    return []


def _selftest_reachability_findings(authority: Authority) -> list[str]:
    findings: list[str] = []
    try:
        tree = ast.parse((HERE / CHECKER).read_bytes().decode("utf-8"))
    except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
        authority.record_probe("PR-21-SELFTEST-REACHABILITY", False)
        return [f"cannot parse this checker's own source: {type(exc).__name__}"]
    main_fn = [node for node in tree.body
               if isinstance(node, ast.FunctionDef) and node.name == "main"]
    if len(main_fn) != 1:
        findings.append("this checker does not define exactly one main()")
        authority.record_probe("PR-21-SELFTEST-REACHABILITY", False)
        return findings
    selftest_index = None
    findings_return_index = None
    for index, statement in enumerate(main_fn[0].body):
        text = ast.dump(statement)
        if selftest_index is None and "'--selftest'" in text and \
                "Name(id='selftest'" in text:
            selftest_index = index
        if findings_return_index is None and "Name(id='findings'" in text and \
                "Return(" in text:
            findings_return_index = index
    if selftest_index is None:
        findings.append("main() never dispatches to selftest()")
    elif findings_return_index is not None and \
            findings_return_index < selftest_index:
        findings.append(
            "main() can return on findings before reaching the selftest suite")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in {
                "TODO_FINDINGS", "TODO_DECLARATIONS"}:
            findings.append(
                "this checker carries an unconditional TODO findings gate")
            break
    authority.record_probe("PR-21-SELFTEST-REACHABILITY", not findings)
    return findings


def _derived_root_findings(candidate: Any, authority: Authority) -> list[str]:
    """Compare each derived root to its live derivation from pinned authority.

    This layer is independent of the whole-object successor comparison: it
    holds even when successor equality is disabled, which is how the mutation
    suite demonstrates that the binding is not carried by that comparison
    alone.
    """
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["derived-root scan requires an object root"]
    context = getattr(authority, "context", None)
    if context is None:
        return ["derived roots have no derivation context"]
    try:
        dependencies = build_dependencies(context)
        d9_mapping = derive_d9_mapping(authority)
        request_context = derive_request_context_binding(authority)
        grammar = build_grammar(authority.json(PREDECESSOR).get(
            "canonicalWireGrammar"))
    except Malformed as exc:
        return [f"derived roots cannot be rebuilt: {exc}"]
    for key, expected, probe in (
            ("dependencies", dependencies, None),
            ("d9Mapping", d9_mapping, "PR-05-D9-LIVE-DERIVATION"),
            ("requestContextBinding", request_context,
             "PR-06-REQUEST-CONTEXT-AUTHORITY"),
            ("canonicalWireGrammar", grammar, None)):
        difference = _first_difference(candidate.get(key), expected, key)
        if difference is not None:
            findings.append(
                f"{key} is not the live derivation from pinned authority: "
                f"{difference}")
        if probe is not None:
            authority.record_probe(probe, difference is None)
    return findings


def candidate_layers(candidate: Any, authority: Authority,
                     source: Any = None,
                     with_equality: bool = True) -> list[str]:
    """Every candidate-driven layer.  Total; no layer may raise."""
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return [f"<root>: expected object, found {_kind(candidate)}"]
    expected = getattr(authority, "expected", None)
    if with_equality and isinstance(expected, dict):
        difference = _first_difference(candidate, expected)
        if difference is not None:
            findings.append(
                "candidate is not the derived successor of the pinned "
                f"predecessor and dependencies: {difference}")
        authority.record_probe("PR-18-EXPECTED-SUCCESSOR-EQUALITY",
                               difference is None)
        findings.extend(_source_findings(source, expected))
    findings.extend(candidate_recomputation_findings(candidate, authority))
    findings.extend(_derived_root_findings(candidate, authority))
    nomenclature = _nomenclature_findings(candidate,
                                          pinned_finding_ids(authority))
    authority.record_probe("PR-19-NOMENCLATURE-CLOSURE", not nomenclature)
    findings.extend(nomenclature)
    findings.extend(_producer_obligation_findings(candidate, authority))
    findings.extend(_grammar_delta_findings(candidate, authority))
    findings.extend(_registry_findings(candidate, authority))
    findings.extend(_disposition_findings(candidate, authority))
    return findings


def check(candidate: Any, authority: Authority,
          source: Any = None) -> list[str]:
    """Full v9 check.  Returns findings; never raises on hostile input."""
    findings: list[str] = []
    try:
        expected = expected_successor(authority)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"expected successor construction failed: "
                f"{type(exc).__name__}: {exc}"]
    findings.extend(run_dependency_probes(authority))
    findings.extend(_selftest_reachability_findings(authority))
    saved = dict(authority.probe_log)
    hostile = hostile_matrix(expected, authority, full=False)
    authority.probe_log.clear()
    authority.probe_log.update(saved)
    authority.record_probe("PR-13-HOSTILE-INPUT-TOTALITY",
                           hostile["escapes"] == 0 and
                           hostile["guardedEscapes"] == 0)
    if hostile["escapes"] or hostile["guardedEscapes"]:
        findings.append(
            f"hostile input matrix: {hostile['escapes']} unguarded and "
            f"{hostile['guardedEscapes']} guarded escape(s)")
    try:
        findings.extend(candidate_layers(candidate, authority, source))
    except Exception as exc:                          # noqa: BLE001 - reported
        findings.append(
            f"checking layer raised {type(exc).__name__}: {exc}")
    return findings


# ---------------------------------------------------------------------------
# Section 7.  Hostile-input totality matrix (EV8-IR-07).
# ---------------------------------------------------------------------------

HOSTILE_VALUES: tuple[tuple[str, Any], ...] = (
    ("null", None), ("integer", 0), ("negative", -1), ("float", 1.5),
    ("true", True), ("false", False), ("empty-text", ""), ("text", "x"),
    ("empty-array", []), ("empty-object", {}), ("nested-array", [[]]),
    ("nested-object", [{"unknown": 1}]),
)


def _hostile_nodes(base: Mapping[str, Any], full: bool) -> list[str]:
    nodes: list[str] = [""]
    nodes.extend(sorted(base))
    frontier: list[tuple[str, Any]] = [
        (key, base[key]) for key in sorted(base)
        if isinstance(base[key], (dict, list))]
    depth = 0
    limit = 3 if full else 1
    while frontier and depth < limit:
        nxt: list[tuple[str, Any]] = []
        for path, value in frontier:
            if isinstance(value, dict):
                children = [(f"{path}.{key}", value[key]) for key in sorted(value)]
            else:
                children = [(f"{path}[{index}]", item)
                            for index, item in enumerate(value[:2])]
            for child_path, child in children:
                if isinstance(child, (dict, list)):
                    nodes.append(child_path)
                    nxt.append((child_path, child))
        frontier = nxt
        depth += 1
    seen: set[str] = set()
    ordered: list[str] = []
    for path in nodes:
        if path not in seen:
            seen.add(path)
            ordered.append(path)
    return ordered


def hostile_matrix(base: Mapping[str, Any], authority: Authority,
                   full: bool = True) -> dict[str, Any]:
    """Drive hostile parsed JSON through the UNGUARDED candidate layers."""
    nodes = _hostile_nodes(base, full)
    cases = 0
    escapes = 0
    guarded_escapes = 0
    silent = 0
    escaped_examples: list[str] = []
    silent_examples: list[str] = []
    for path in nodes:
        injections = list(HOSTILE_VALUES)
        try:
            target = base if path == "" else _resolve(base, path)
        except Malformed:
            continue
        if isinstance(target, dict):
            injections.append(("unknown-key", "<insert>"))
        for label, value in injections:
            candidate: Any
            if path == "":
                candidate = copy.deepcopy(base) if label == "unknown-key" \
                    else copy.deepcopy(value)
                if label == "unknown-key" and isinstance(candidate, dict):
                    candidate["ev9UnknownRootKey"] = 1
            else:
                candidate = copy.deepcopy(base)
                if label == "unknown-key":
                    node = _resolve(candidate, path)
                    if not isinstance(node, dict):
                        continue
                    node["ev9UnknownNestedKey"] = 1
                else:
                    _assign(candidate, path, copy.deepcopy(value))
            cases += 1
            try:
                findings = candidate_layers(candidate, authority)
            except Exception as exc:                  # noqa: BLE001 - measured
                escapes += 1
                if len(escaped_examples) < 5:
                    escaped_examples.append(
                        f"{path or '<root>'}:{label} -> {type(exc).__name__}: {exc}")
                continue
            if not findings:
                silent += 1
                if len(silent_examples) < 5:
                    silent_examples.append(f"{path or '<root>'}:{label}")
            try:
                _ = check_guarded(candidate, authority)
            except Exception:                         # noqa: BLE001 - measured
                guarded_escapes += 1
    return {"cases": cases, "nodes": len(nodes), "escapes": escapes,
            "guardedEscapes": guarded_escapes, "silent": silent,
            "escapedExamples": escaped_examples,
            "silentExamples": silent_examples}


def check_guarded(candidate: Any, authority: Authority) -> list[str]:
    try:
        return candidate_layers(candidate, authority)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"checking layer raised {type(exc).__name__}: {exc}"]


# ---------------------------------------------------------------------------
# Section 8.  Mutation suite.
#
# Every mutation the independent predecessor review reported as escaping (P3,
# 22 cases) or as semantically unbound (P5, 6 cases) appears below, together
# with the successor-specific surfaces.  A mutation that fails to apply, or
# that applies without changing the candidate bytes, is counted as an ESCAPE.
# ---------------------------------------------------------------------------

def _set(path: str, value: Any) -> Callable[[Any, Authority], None]:
    def apply(candidate: Any, _authority: Authority) -> None:
        _assign(candidate, path, copy.deepcopy(value))
    return apply


def _drop(path: str) -> Callable[[Any, Authority], None]:
    def apply(candidate: Any, _authority: Authority) -> None:
        steps = _path_steps(path)
        node = candidate
        for step in steps[:-1]:
            node = node[step]
        if isinstance(node, dict):
            node.pop(steps[-1])
        else:
            node.pop(steps[-1])
    return apply


def _swap_commitments(candidate: Any, _authority: Authority) -> None:
    values = candidate["acceptedGolden"]["values"]
    values["universeCommitment"], values["outcomeSetCommitment"] = \
        values["outcomeSetCommitment"], values["universeCommitment"]


def _drop_inventory_member(candidate: Any, authority: Authority) -> None:
    context = getattr(authority, "context", None)
    derived = context.derived
    codec = derived["codec"]
    refs = list(derived["proofRefs"])[1:]
    reduced = codec.emit("RawProofInventoryV1", {
        "schemaVersion": 1, "projectId": derived["values"]["projectId"],
        "items": codec.inventory_items(refs)})
    candidate["acceptedGolden"]["rawProofInventoryHex"] = reduced.hex()
    candidate["acceptedGolden"]["rawProofInventoryLength"] = len(reduced)


def _reopen_todos(candidate: Any, authority: Authority) -> None:
    predecessor = authority.json(PREDECESSOR)
    candidate["foundationImplementation"]["blockingTodos"] = copy.deepcopy(
        predecessor["foundationImplementation"]["blockingTodos"])


def _close_open_residual(candidate: Any, _authority: Authority) -> None:
    for row in candidate["reviewFindingTransfers"]:
        if isinstance(row, dict) and row.get("id") == "EV7-PF-R01-CUSTODY-AUTHORITY-JOIN":
            row["state"] = "CLOSED-BY-EXECUTED-PROBE"
            return
    raise Malformed("EV7-PF-R01 disposition is absent")


def _fabricate_disposition(candidate: Any, _authority: Authority) -> None:
    candidate["reviewFindingTransfers"].append({
        "id": "EV8-IR-09-INVENTED", "source": PREDECESSOR_REVIEW,
        "sourceSha256": PINS[PREDECESSOR_REVIEW],
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "invented", "provenBy": ["PR-01-GRAMMAR-RECOMPUTATION"]})


def _drop_disposition(candidate: Any, _authority: Authority) -> None:
    rows = candidate["reviewFindingTransfers"]
    for index, row in enumerate(rows):
        if isinstance(row, dict) and \
                row.get("id") == "EV7-PF-04-D9-NOT-TOTAL-OVER-COLD-RECOVERY":
            rows.pop(index)
            return
    raise Malformed("EV7-PF-04 disposition is absent")


def _prose_only_registry_edit(candidate: Any, _authority: Authority) -> None:
    candidate["semanticBindingRegistry"]["entries"][0]["claim"] = \
        "Indeterminate outcomes may be recorded as an authoritative pass."


def _predicate_only_registry_edit(candidate: Any, _authority: Authority) -> None:
    entries = candidate["semanticBindingRegistry"]["entries"]
    for entry in entries:
        if entry.get("kind") == "rt-proof-member-set":
            entry["params"]["count"] = 22
            entry["claim"] = _render(entry["kind"], entry["params"])
            return
    raise Malformed("no rt-proof-member-set entry")


def _grammar_tag_edit(candidate: Any, _authority: Authority) -> None:
    _assign(candidate,
            "canonicalWireGrammar.records.SemanticEvidenceV1.fields[5].tag",
            "0x9f")


def _grammar_order_edit(candidate: Any, _authority: Authority) -> None:
    fields = candidate["canonicalWireGrammar"]["records"]["TerminalRunV1"]["fields"]
    fields[10], fields[11] = fields[11], fields[10]


def _alias_injection(candidate: Any, _authority: Authority) -> None:
    candidate["retainedResiduals"].append("CustodyRootV1 is an accepted alias.")


def _stale_injection(candidate: Any, _authority: Authority) -> None:
    candidate["retainedResiduals"].append("EP7 remains the consumed generation.")


def _historical_label_injection(candidate: Any, _authority: Authority) -> None:
    candidate["retainedResiduals"].append("RT11 supplies the proof inventory.")


def _cd_rt_5_self_signature(candidate: Any, _authority: Authority) -> None:
    candidate["retainedResiduals"].append(
        "CD-RT-5 is granted by this artifact and the product default is decided.")


MUTATIONS: tuple[tuple[str, Callable[[Any, Authority], None], bool], ...] = (
    ("P3-accepted-vector-indeterminate",
     _set("dependencies.evaluationProof.acceptedVectorId",
          "EP8-POS-INDETERMINATE"), True),
    ("P3-accepted-vector-nonexistent",
     _set("dependencies.evaluationProof.acceptedVectorId", "NO-SUCH-VECTOR"), True),
    ("P3-closure-commitment-arbitrary",
     _set("dependencies.retentionCustody.acceptedClosureCommitment",
          "sha256:" + "a" * 64), True),
    ("P3-dependency-direction-reversed",
     _set("dependencies.dependencyDirection",
          "Evidence v9 feeds EP8 and RT22; Evidence may redefine lease and "
          "purge semantics."), True),
    ("P3-invariants-emptied", _set("invariants", []), False),
    ("P3-invariant-absorption",
     _set("invariants[0].assert",
          "Indeterminate outcomes may be recorded as an authoritative pass."),
     False),
    ("P3-semantic-join-retention",
     _set("semanticJoins.retention",
          "Evidence v9 defines its own lease, purge and D9 semantics locally."),
     False),
    ("P3-semantic-join-terminal-authority",
     _set("semanticJoins.terminalAuthority",
          "The producer self-declares terminal authority."), False),
    ("P3-projection-rule",
     _set("persistedVsProjection.projection.rule",
          "Projection fields may enter EvidenceDigest and RunId."), False),
    ("P3-persisted-emptied", _set("persistedVsProjection.persisted", []), False),
    ("P3-admission-ordering-emptied", _set("admissionAndSealOrdering", []), False),
    ("P3-product-fork-weakened",
     _set("sealedCapabilityContract.productFork",
          "The producer may self-declare a weaker proof obligation."), False),
    ("P3-read-time-self-asserted",
     _set("sealedCapabilityContract.readTime",
          "Read-time capability is whatever the producer asserts."), False),
    ("P3-availability-invariant-emptied",
     _set("availabilityDifferential.invariant", []), False),
    ("P3-availability-changes-identity",
     _set("availabilityDifferential.changesOnly",
          ["EvidenceDigest", "RunId", "runSealRef", "TerminalRunV1"]), False),
    ("P3-request-id-rule-inverted",
     _set("recursiveRequestIdExclusion.rule",
          "RequestId and ExecutionId may appear in any semantic record; "
          "unknown fields are ignored."), False),
    ("P3-request-id-surfaces-emptied",
     _set("recursiveRequestIdExclusion.surfaces", []), False),
    ("P3-request-id-negative-control-dropped",
     _set("recursiveRequestIdExclusion.negativeControl", "not tested"), False),
    ("P3-request-id-differential-inverted",
     _set("recursiveRequestIdExclusion.differential",
          "Distinct RequestIds produce distinct RunIds."), False),
    ("P3-role-arbitrary", _set("role", "arbitrary successor text"), False),
    ("P3-transfers-emptied", _set("reviewFindingTransfers", []), True),
    ("P3-transfer-state-sealed",
     _set("reviewFindingTransfers[1].state",
          "INDEPENDENTLY-ACCEPTED-AND-SEALED"), False),
    ("P5-universe-commitment-arbitrary",
     _set("acceptedGolden.values.universeCommitment", "sha256:" + "1" * 64), True),
    ("P5-outcome-commitment-arbitrary",
     _set("acceptedGolden.values.outcomeSetCommitment", "sha256:" + "1" * 64), True),
    ("P5-derivation-commitment-arbitrary",
     _set("acceptedGolden.values.verdictDerivationCommitment",
          "sha256:" + "1" * 64), True),
    ("P5-commitment-same-cardinality-swap", _swap_commitments, True),
    ("P5-commitment-same-shape-substitution",
     _set("acceptedGolden.values.universeCommitment",
          "sha256:1d33209c51f64793e8535bfa116204fbadb6de06b3fedec9d2650b0260061568"),
     True),
    ("P5-inventory-member-dropped", _drop_inventory_member, True),
    ("d9-exit-code-absorbed",
     _set("d9Mapping.rows[0].derivedExitCode", 0), True),
    ("d9-class-absorbed",
     _set("d9Mapping.rows[0].derivedClass", "success"), True),
    ("d9-rows-emptied", _set("d9Mapping.rows", []), True),
    ("d9-axes-relabelled",
     _set("d9Mapping.rows[0].axes.faultCause", "host-io"), True),
    ("d9-vocabulary-rule-weakened",
     _set("d9Mapping.vocabularyRule",
          "New D9 classes and codes may be introduced by the producer."), True),
    ("registry-prose-only-edit", _prose_only_registry_edit, True),
    ("registry-predicate-only-edit", _predicate_only_registry_edit, True),
    ("registry-bound-paths-emptied",
     _set("semanticBindingRegistry.entries[0].boundArtifactPaths", []), True),
    ("registry-entries-emptied",
     _set("semanticBindingRegistry.entries", []), True),
    ("request-context-public-constructor",
     _set("requestContextBinding.publicConstructors", ["from_json"]), True),
    ("request-context-exclusion-emptied",
     _set("requestContextBinding.forbiddenSemanticParticipation", []), True),
    ("foundation-status-sealed",
     _set("foundationImplementation.status", "SEALED"), False),
    ("foundation-todos-reopened", _reopen_todos, False),
    ("successor-refreeze",
     _set("successorDelta.protectedIdentityKeys", ["acceptedGolden"]), False),
    ("successor-changed-roots-emptied",
     _set("successorDelta.changedRootKeys", []), False),
    ("successor-rejection-detached",
     _set("successorDelta.rejection", "anything"), False),
    ("grammar-tag-edit", _grammar_tag_edit, True),
    ("grammar-field-order-edit", _grammar_order_edit, True),
    ("grammar-set-rule-inverted",
     _set("canonicalWireGrammar.recordRules.sets",
          "sort the framed item wrappers unsigned"), True),
    ("version-regressed", _set("version", 8), False),
    ("status-applied", _set("status", "APPLIED"), False),
    ("authority-claimed", _set("authority.authorityClaim", "FULL"), True),
    ("assurance-upgraded", _set("assurance.evidenceGrade", "QUALIFIED"), True),
    ("seal-recommended", _set("sealRecommendation", "SEAL"), True),
    ("evidence-digest-substituted",
     _set("acceptedGolden.evidenceDigest", "sha256:" + "f" * 64), True),
    ("run-id-substituted",
     _set("acceptedGolden.runId", "run1:" + "f" * 64), True),
    ("run-seal-ref-substituted",
     _set("acceptedGolden.runSealRef", "sha256:" + "f" * 64), True),
    ("run-substitution-golden-substituted",
     _set("runSubstitutionGoldens[0].expectedRunId", "run1:" + "0" * 64), True),
    ("run-substitution-goldens-emptied",
     _set("runSubstitutionGoldens", []), True),
    ("supersedes-hash-detached", _set("supersedes.sha256", "0" * 64), False),
    ("termination-dependency-hash-detached",
     _set("dependencies.terminationContract.sha256", "0" * 64), True),
    ("request-context-review-flipped",
     _set("dependencies.requestContext.reviewDecision", "REJECT"), True),
    ("disposition-dropped", _drop_disposition, True),
    ("residual-declared-closed", _close_open_residual, True),
    ("disposition-fabricated", _fabricate_disposition, True),
    ("residuals-emptied", _set("retainedResiduals", []), False),
    ("hostile-contract-escapes-allowed",
     _set("hostileInputTotalityContract.requiredEscapes", 5), False),
    ("selftest-exit-code-collapsed",
     _set("checkerModeContract.exitCodes.selftestRefusedDirtyBase", 0), False),
    ("unknown-root-key",
     _set("ev9UnknownRootKey", "injected"), False),
    ("dropped-root-key", _drop("availabilityDifferential"), False),
    ("alias-injection", _alias_injection, True),
    ("stale-generation-injection", _stale_injection, True),
    ("historical-label-injection", _historical_label_injection, True),
    ("cd-rt-5-self-signature", _cd_rt_5_self_signature, True),
)


def run_mutation_suite(base: Mapping[str, Any],
                       authority: Authority) -> dict[str, Any]:
    """Apply every mutation; a no-op or an unapplied mutation is an ESCAPE."""
    escapes: list[str] = []
    semantic_escapes: list[str] = []
    applied = 0
    semantic_checked = 0
    baseline = canonical(base)
    for label, mutate, semantic_expected in MUTATIONS:
        candidate = copy.deepcopy(dict(base))
        try:
            mutate(candidate, authority)
        except Exception as exc:                      # noqa: BLE001 - measured
            escapes.append(f"{label}: mutation failed to apply "
                           f"({type(exc).__name__}: {exc})")
            continue
        if canonical(candidate) == baseline:
            escapes.append(f"{label}: mutation applied without changing bytes")
            continue
        applied += 1
        saved_full = dict(authority.probe_log)
        try:
            full_findings = check_guarded(candidate, authority)
        finally:
            authority.probe_log.clear()
            authority.probe_log.update(saved_full)
        if not full_findings:
            escapes.append(f"{label}: escaped the full checking layers")
        if semantic_expected:
            semantic_checked += 1
            saved = dict(authority.probe_log)
            try:
                findings = candidate_layers(candidate, authority,
                                            with_equality=False)
            except Exception as exc:                  # noqa: BLE001 - measured
                findings = [f"raised {type(exc).__name__}: {exc}"]
                semantic_escapes.append(
                    f"{label}: semantic layer raised {type(exc).__name__}")
                findings = []
            finally:
                authority.probe_log.clear()
                authority.probe_log.update(saved)
            if not findings:
                semantic_escapes.append(
                    f"{label}: escaped every layer other than successor equality")
    return {"total": len(MUTATIONS), "applied": applied, "escapes": escapes,
            "semanticChecked": semantic_checked,
            "semanticEscapes": semantic_escapes}


def selftest(candidate: Any, source: bytes, authority: Authority) -> int:
    """Always reaches the suite; refuses a dirty base with a distinct code."""
    base_findings = check(candidate, authority, source)
    if base_findings:
        print("SELFTEST-REFUSED: the base candidate is not clean, so the "
              "mutation suite is not an oracle over it.")
        print(f"  dirty base: {len(base_findings)} finding(s) in the candidate")
        for finding in base_findings[:10]:
            print("  base-finding:", finding)
        if len(base_findings) > 10:
            print(f"  ... {len(base_findings) - 10} further base finding(s)")
        print("SELFTEST-NOT-RUN: 0 of "
              f"{len(MUTATIONS)} mutations executed; exit 3 distinguishes this "
              "refusal from a green selftest and from an ordinary failure.")
        return 3
    if not isinstance(candidate, dict):
        print("SELFTEST-REFUSED: selftest requires an object root", file=sys.stderr)
        return 3
    suite = run_mutation_suite(candidate, authority)
    saved = dict(authority.probe_log)
    try:
        hostile = hostile_matrix(candidate, authority, full=True)
    finally:
        authority.probe_log.clear()
        authority.probe_log.update(saved)
    failures: list[str] = list(suite["escapes"]) + list(suite["semanticEscapes"])
    if hostile["escapes"]:
        failures.append(
            f"{hostile['escapes']} hostile case(s) escaped the unguarded layers; "
            f"first {hostile['escapedExamples'][0]}")
    if hostile["guardedEscapes"]:
        failures.append(
            f"{hostile['guardedEscapes']} hostile case(s) escaped the guarded layers")
    if hostile["silent"]:
        failures.append(
            f"{hostile['silent']} hostile case(s) produced no finding at all; "
            f"first {hostile['silentExamples'][0]}")
    if failures:
        for failure in failures:
            print("SELFTEST-FAIL:", failure)
        return 1
    print("SELFTEST-PASS: evidence.v9.json")
    print(f"  mutations: {suite['applied']}/{suite['total']} applied and "
          f"rejected; 0 escapes; {suite['semanticChecked']} of them also "
          "rejected with successor-equality disabled, so the binding is not "
          "carried by whole-object comparison alone")
    print(f"  hostile parsed JSON: {hostile['cases']} cases over "
          f"{hostile['nodes']} schema nodes; {hostile['escapes']} unguarded "
          f"escapes, {hostile['guardedEscapes']} guarded escapes, "
          f"{hostile['silent']} silent cases")
    print(f"  executed probes: {sum(1 for value in authority.probe_log.values() if value)}"
          f"/{len(PROBE_IDS)} green")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; independent re-review REQUIRED; no seal, "
          "freeze, integration, product acceptance or CD-RT-5 disposition")
    return 0


def main(argv: list[str]) -> int:
    authority = _BOOTSTRAP_AUTHORITY
    flags = set(argv[1:])
    if "--emit-candidate" in flags:
        try:
            sys.stdout.buffer.write(pretty(expected_successor(authority)))
        except Exception as exc:                      # noqa: BLE001 - reported
            print(f"cannot emit candidate: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            return 2
        return 0
    positional = [item for item in argv[1:]
                  if item not in ("--selftest", "--emit-candidate")]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate, source = load_source(path)
    except (OSError, UnicodeError, AuthorityLoadError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load Evidence candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in flags:
        return selftest(candidate, source, authority)
    findings = check(candidate, authority, source)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    green = sum(1 for value in authority.probe_log.values() if value)
    print(f"Evidence v9 OK - {path.name}; {len(PINS)} inputs hash-verified "
          "before execution; complete successor derived from the pinned "
          "predecessor and dependencies; every published commitment recomputed "
          f"under the declared grammar; {len(D9_SITUATIONS) + 1} termination "
          f"rows derived live from D9 v1.13; {green}/{len(PROBE_IDS)} probes green")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; no seal, freeze, integration, product "
          "acceptance or CD-RT-5 disposition is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
