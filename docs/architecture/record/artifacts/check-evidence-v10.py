#!/usr/bin/env python3
"""Evidence v10 successor checker: hostile-input totality repaired at the leaf.

evidence.v9 was independently REJECTED on exactly ONE blocking finding.  The
reviewer independently CONFIRMED everything else: all eight EV8-IR findings
repaired, a from-scratch encoder reproducing all seventeen commitments and the
six run-substitution goldens, --emit-candidate regenerating the frozen
candidate byte-identically from the pinned inputs alone, a 105-mutation battery
with zero label overlap producing zero escapes, ten fully self-consistent
forged goldens all rejected by the recomputation layer, a genuinely live
--selftest with an exit-3 dirty-base refusal that survived seven bypass
attempts, and hash-before-execution with no check/read gap.  This successor is
a NARROW REPAIR of the one defect; every confirmed property is preserved and
re-executed here rather than re-declared.

  EV9-IR-01  hostileInputTotalityContract declared requiredEscapes = 0 over
             "every nested schema node", but _grammar_delta_findings consumed a
             candidate-supplied path string unguarded while its two sibling
             consumers were guarded, and the author's node enumerator never
             injected at SCALAR LEAF positions, so the instrument could not
             observe the region where the claim failed.  Two repairs:
               (a) STRUCTURAL, not per-site: every candidate-supplied path
                   consumption inside the closure reachable from the checking
                   entrypoints must be enclosed by a handler for Malformed, and
                   this checker enforces that over its own AST (PR-23).  A
                   fourth omitted site cannot recur silently.
               (b) The generator now enumerates EVERY path of the artifact at
                   unlimited depth and every array index, INCLUDING scalar leaf
                   positions, and the published measurement is the live census
                   of that space rather than of a strictly smaller one.
             Both repairs are proved load-bearing by executed batteries: an AST
             self-mutation battery that removes each guard and requires the
             scan to report it, and a generator-narrowing battery that requires
             the container-only enumeration to be detectably smaller than the
             published counts.
  EV9-IR-02  the unenforced sub-clause "no second undocumented selftest
             entrypoint" is now mechanically enforced: the set of "--" string
             literals in this checker's source must equal DECLARED_FLAGS, must
             equal the flags implied by checkerModeContract.entrypoints, and
             the single call to selftest() must be guarded by a declared flag.
  EV9-IR-O1  a second positional argument or an unknown flag is refused with
             exit 2 instead of being silently ignored.
  EV9-IR-O2  the selftest banner prints the candidate path it actually checked.
  EV9-IR-O3  no checking layer degrades silently when the derivation context is
             cold; it is warmed from pinned authority instead (PR-25).

Carried forward from the confirmed v9 architecture, and re-executed here:
whole-object derivation of the successor from pinned bytes (EV8-IR-02), wire
recomputation of every published commitment (EV8-IR-03/04), the live D9 v1.13
termination derivation (EV8-IR-05), selftest reachability with the exit-3 dirty
base refusal (EV8-IR-06), and the disposition-closure layer that refuses a
closure claim naming a probe that did not run and pass (EV8-IR-08).

Trust root: caller-owned ``python3 -I -B``.  Every pinned byte string is
hash-verified BEFORE any of it is parsed or executed.

Authorship: CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW.  A green run
of this authored checker is checker-scope evidence ONLY.  It declares no seal,
no freeze, no integration and no product acceptance, and it does not sign
CD-RT-5.

Supported usage only:
  python3 -I -B artifacts/check-evidence-v10.py [candidate] [--selftest]
  python3 -I -B artifacts/check-evidence-v10.py --emit-candidate
Exit: 0 clean; 1 findings; 2 unsupported invocation/input; 3 selftest refused
      because the base candidate is not clean.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "EV10-UNSUPPORTED-INVOCATION: caller must use "
    "python3 -I -B artifacts/check-evidence-v10.py"
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
BINDING = "evidence.v10.json"
CHECKER = "check-evidence-v10.py"

PREDECESSOR = "evidence.v9.json"
PREDECESSOR_CHECKER = "check-evidence-v9.py"
PREDECESSOR_REVIEW = "evidence.v9.review-independent-prefreeze.json"
LINEAGE = "evidence.v8.json"
LINEAGE_CHECKER = "check-evidence-v8.py"
LINEAGE_REVIEW = "evidence.v8.review-independent-prefreeze.json"
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

# Twenty-four pinned byte strings, exactly as many as evidence.v9 pinned.  The
# predecessor triple advances v8 -> v9 and the lineage triple advances v7 -> v8;
# the v7 generation is no longer pinned directly, because the pinned v9 checker
# verifies its own inherited v7 pins when it executes here (PR-26), so the
# lineage remains transitively hash-bound rather than assumed.
#
# d9-exit-contract.v1.13 and check-d9-v1.13.py are retained deliberately.  That
# surface PASSED independent review with zero blocking findings and has not
# drifted.  A v1.14 successor is under concurrent authorship and has NOT been
# reviewed; pinning an unreviewed successor would import an unaccepted
# dependency, so it is not pinned here.  Re-pinning is separate successor work.
PINS: dict[str, str] = {
    PREDECESSOR:
        "ddb4e6b80420c90bcb112a36b1ec372c2ed08ed5ad98742f62a8406f5cc8253e",
    PREDECESSOR_CHECKER:
        "22f4e53775b3b2e70a3fb42b461f8c3d3308778e24edfcf75e61e6fbf0bcd452",
    PREDECESSOR_REVIEW:
        "25af2beafb81805e87ce6406b17e45740e9ee15eed4326e8c346464ba35d2746",
    LINEAGE: "4ef262d156a0c66d9cefef4c2fd5c1b80883b5573164754558a42ed139f3921c",
    LINEAGE_CHECKER:
        "0771f3e1079b99b8e28f6b7a7154c722d2195ba5142e91f350438a2eae7ae525",
    LINEAGE_REVIEW:
        "ad07b4ae3f5c5fa8886ea1b838373e0b5d134dfcc5ab5e894c1e3d7c86f9b7f0",
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
    PREDECESSOR: "rejected v9 candidate; carried root values and predecessor identity",
    PREDECESSOR_CHECKER: "retained executable v9 checker, re-executed here in full",
    PREDECESSOR_REVIEW: "independent v9 REJECT whose single blocking finding this successor repairs",
    LINEAGE: "v8 lineage referenced by the v9 supersedes chain",
    LINEAGE_CHECKER: "retained executable v8 foundation suite",
    LINEAGE_REVIEW: "independent v8 REJECT whose EV8-IR finding ids remain disposed",
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
    PREDECESSOR_REVIEW: {"decision": "REJECT", "blockingFindingCount": 1},
    LINEAGE_REVIEW: {"decision": "REJECT", "blockingFindingCount": 8},
    RT22_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
    D9_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
    TRC3_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
    EP8_REVIEW: {"decision": "PASS", "blockingFindingCount": 0},
}

DECLARED_FLAGS: tuple[str, ...] = ("--selftest", "--emit-candidate")


class DuplicateKeyError(ValueError):
    """A JSON object repeated a key; the document is not canonical."""


class AuthorityLoadError(RuntimeError):
    """A pinned input could not be admitted as authority."""


class PinMismatch(AuthorityLoadError):
    """A pinned byte string does not hash to its declared digest."""


class Malformed(Exception):
    """A candidate-driven layer met a shape it cannot consume."""


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this checker does not accept."""


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
        self.context: Any = None
        self.expected: Any = None
        self.census: Any = None

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
        PREDECESSOR_CHECKER, LINEAGE_CHECKER, V4_CHECKER, D9_CHECKER,
        TRC3_CHECKER, RT22_CHECKER, EP8_CHECKER, VERSIONING_CHECKER,
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
            module_name = "opensip_ev10_verified_" + \
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
# and therefore the EvidenceDigest, the RunId and the runSealRef.  Carried
# unchanged from the independently re-derived v9 encoder: the reviewer's
# from-scratch decoder reproduced these bytes on the first attempt.
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
# pinned reference derivation.  Independently falsified six ways at v9 and
# carried unchanged; row COVERAGE remains checker-authored (EV9-IR-R5).
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
# Section 3.  TrustedRequestContext construction authority.  Every field is
# projected from the independently accepted trusted-request-context.v3
# authority; nothing here is authored.
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
# Section 4.  Semantic binding registry.
#
# Each entry carries a prose claim, a closed machine-readable predicate, and
# the artifact leaf paths whose semantic content the entry underwrites.  The
# checker requires BOTH that the prose equals the deterministic rendering of
# the predicate AND that the predicate evaluates true against pinned
# dependency bytes.  Editing the prose alone fails rendering; editing the
# predicate alone fails evaluation; editing both consistently fails
# evaluation.  A prose claim can therefore not act as its own oracle.
#
# SB-17, SB-18 and SB-19 are new in this generation.  They bind the three
# claims the independent v9 review found unenforced - the measured hostile
# space, the guarding of candidate-supplied path consumers, and the closed
# set of command entrypoints - to predicates that are executed rather than
# declared.
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
    if kind == "predecessor-review-binding":
        return ("The pinned predecessor review is the exact "
                f"{params['decision']} with {params['blockingCount']} blocking "
                f"finding, {params['newFindingCount']} new findings, "
                f"{params['residualCount']} residuals and "
                f"{params['observationCount']} observations; it independently "
                f"confirms {params['confirmedCount']} predecessor findings "
                "repaired; and every identifier it reports carries a "
                "disposition in reviewFindingTransfers.")
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
    if kind == "hostile-space-census":
        return ("The hostile-input generator enumerates all "
                f"{params['enumeratedPaths']} paths of this artifact at "
                "unlimited depth and at every array index, of which "
                f"{params['scalarLeafPaths']} are scalar leaf positions and "
                f"{params['containerPaths']} are container positions, and "
                f"executes {params['executedCases']} hostile cases through the "
                "unguarded checking layers. The measured space is therefore "
                "the same space the totality rule quantifies over, and not a "
                "strictly smaller one.")
    if kind == "path-consumer-guard":
        return (f"Every one of the {params['guardedCallSites']} "
                "candidate-supplied path consumptions inside the "
                f"{params['scannedFunctions']} functions reachable from the "
                "checking entrypoints is enclosed by a handler for Malformed, "
                f"and {params['unguardedCallSites']} are not, so an empty or "
                "unparsable path string returns a deterministic finding "
                "instead of propagating an exception out of a checking layer.")
    if kind == "selftest-entrypoint-closure":
        return (f"This checker's source contains exactly {params['flagCount']} "
                f"command flag literals ({', '.join(params['flags'])}), each "
                "one declared in checkerModeContract.entrypoints, and exactly "
                f"{params['dispatchCount']} call to the selftest suite, guarded "
                "by a declared flag; a second undocumented selftest entrypoint "
                "is therefore refused rather than merely disclaimed.")
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
        self.lineage_review = authority.json(LINEAGE_REVIEW)


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
    review_ids = predecessor_review_ids(context.review)
    census = context.authority.census
    if not isinstance(census, dict):
        raise Malformed("the hostile-space census has not been derived")
    guard = _path_guard_scan()
    entrypoints = _selftest_entrypoint_scan()
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
         "params": {"token": "evidence.v10"},
         "boundArtifactPaths": ["dependencies.dependencyDirection"],
         "provenBy": "PR-16-DEPENDENCY-ACYCLICITY"},
        {"id": "SB-14-PREDECESSOR-REVIEW-IS-BOUND",
         "kind": "predecessor-review-binding",
         "params": {
             "decision": _dotted(context.review, "verdict.decision"),
             "blockingCount": _dotted(context.review,
                                      "verdict.blockingFindingCount"),
             "newFindingCount": len(review_ids["new"]),
             "residualCount": len(review_ids["residual"]),
             "observationCount": len(review_ids["observation"]),
             "confirmedCount": len(review_ids["confirmed"])},
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
        {"id": "SB-17-HOSTILE-SPACE-IS-THE-QUANTIFIED-SPACE",
         "kind": "hostile-space-census",
         "params": {key: census[key] for key in CENSUS_KEYS},
         "boundArtifactPaths": [
             "hostileInputTotalityContract.rule",
             "hostileInputTotalityContract.injections",
             "hostileInputTotalityContract.measurement"],
         "provenBy": "PR-13-HOSTILE-INPUT-TOTALITY"},
        {"id": "SB-18-CANDIDATE-PATH-CONSUMERS-ARE-GUARDED",
         "kind": "path-consumer-guard",
         "params": {key: guard[key] for key in GUARD_KEYS},
         "boundArtifactPaths": [
             "hostileInputTotalityContract.pathConsumerGuard"],
         "provenBy": "PR-23-CANDIDATE-PATH-CONSUMER-GUARD"},
        {"id": "SB-19-SELFTEST-ENTRYPOINT-SET-IS-CLOSED",
         "kind": "selftest-entrypoint-closure",
         "params": {"flags": list(entrypoints["flags"]),
                    "flagCount": entrypoints["flagCount"],
                    "dispatchCount": entrypoints["dispatchCount"]},
         "boundArtifactPaths": [
             "checkerModeContract.selftestReachability",
             "checkerModeContract.entrypoints",
             "checkerModeContract.declaredFlags"],
         "provenBy": "PR-21-SELFTEST-REACHABILITY"},
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
    if kind == "predecessor-review-binding":
        review = context.review
        ids = predecessor_review_ids(review)
        ok = (_dotted(review, "verdict.decision") == params.get("decision")
              == "REJECT" and
              _dotted(review, "verdict.blockingFindingCount") ==
              params.get("blockingCount") == 1 and
              len(ids["new"]) == params.get("newFindingCount") and
              len(ids["residual"]) == params.get("residualCount") and
              len(ids["observation"]) == params.get("observationCount") and
              len(ids["confirmed"]) == params.get("confirmedCount") == 8)
        return ok, "predecessor review binding"
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
    if kind == "hostile-space-census":
        expected = getattr(context.authority, "expected", None)
        if not isinstance(expected, dict):
            return False, "no derived successor to enumerate"
        live = _node_census(expected)
        for key in CENSUS_KEYS:
            if params.get(key) != live[key]:
                return False, (f"{key} is {params.get(key)!r} but the live "
                               f"enumeration measures {live[key]!r}")
        if live["scalarLeafPaths"] <= 0 or live["pathsNotRoundTripping"] != 0:
            return False, "the enumeration does not reach scalar leaves cleanly"
        narrowed = _node_census(expected, leaves=False)
        if narrowed["enumeratedPaths"] >= live["enumeratedPaths"] or \
                narrowed["enumeratedCases"] >= live["enumeratedCases"]:
            return False, "the container-only enumeration is not strictly smaller"
        return True, f"{live['enumeratedPaths']} paths enumerated"
    if kind == "path-consumer-guard":
        scan = _path_guard_scan()
        for key in GUARD_KEYS:
            if params.get(key) != scan[key]:
                return False, (f"{key} is {params.get(key)!r} but the live scan "
                               f"measures {scan[key]!r}")
        if scan["unguardedCallSites"] != 0 or scan["guardedCallSites"] < 3:
            return False, "the path-consumer guard scan is not satisfied"
        return True, f"{scan['guardedCallSites']} guarded call sites"
    if kind == "selftest-entrypoint-closure":
        scan = _selftest_entrypoint_scan()
        ok = (list(params.get("flags", [])) == list(scan["flags"]) ==
              sorted(DECLARED_FLAGS) and
              list(scan["declaredLiterals"]) == sorted(DECLARED_FLAGS) and
              params.get("flagCount") == scan["flagCount"] == len(DECLARED_FLAGS) and
              params.get("dispatchCount") == scan["dispatchCount"] == 1 and
              scan["guardedDispatchCount"] == 1 and
              not scan["bindingLiteralInSelftest"])
        return ok, "selftest entrypoint closure"
    return False, f"unknown predicate kind {kind!r}"


# ---------------------------------------------------------------------------
# Section 5.  Expected successor construction.
#
# check() derives the COMPLETE expected v10 object from the pinned predecessor
# bytes plus the pinned dependency bytes and requires exact equality with the
# candidate.  Every leaf of the artifact is therefore derived rather than
# declared.  The independent v9 review confirmed this property empirically
# (--emit-candidate regenerated the frozen candidate byte-identically from the
# pinned inputs alone, and 50 of its 104 mutations were rejected by this
# comparison alone); it is preserved here unchanged.
# ---------------------------------------------------------------------------

EXPECTED_STATUS = "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW"
EXPECTED_AUTHOR = "phase1a-evidence-v10-successor-lane"
EXPECTED_DATE = "2026-08-02"
EXPECTED_ROLE = (
    "E10 leaf-total Evidence successor: the recomputed EP8/RT22 Run terminal "
    "identity and live D9 v1.13 termination derivation of the predecessor, "
    "with candidate-supplied path consumption guarded structurally over the "
    "whole reachable checking closure and the hostile-input measurement widened "
    "to the space its own totality rule quantifies over"
)

PROBE_IDS: tuple[str, ...] = (
    "PR-01-GRAMMAR-RECOMPUTATION",
    "PR-02-INVENTORY-MEMBER-BINDING",
    "PR-03-EP-COMMITMENT-DERIVATION",
    "PR-04-RUN-SUBSTITUTION-GOLDENS",
    "PR-05-D9-LIVE-DERIVATION",
    "PR-06-REQUEST-CONTEXT-AUTHORITY",
    "PR-07-RETAINED-LINEAGE-FOUNDATION",
    "PR-08-RETAINED-LINEAGE-MUTATION-SUITE",
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
    "PR-23-CANDIDATE-PATH-CONSUMER-GUARD",
    "PR-24-CLI-ARGUMENT-DISCIPLINE",
    "PR-25-COLD-CONTEXT-FULL-STRENGTH",
    "PR-26-RETAINED-PREDECESSOR-CHECKER-GREEN",
)
CLOSED_STATES = ("CLOSED-BY-EXECUTED-PROBE", "CLOSED-BY-DERIVATION")
OPEN_STATES = ("OPEN-CARRIED-RESIDUAL", "CARRIED-FROM-PREDECESSOR")
ALL_STATES = CLOSED_STATES + OPEN_STATES

DISPOSITIONS: dict[str, dict[str, Any]] = {
    "EV9-IR-01-HOSTILE-TOTALITY-CONTRACT-IS-FALSIFIED-AT-SCALAR-LEAVES": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "Repaired in two places rather than one. (1) STRUCTURAL: every candidate-supplied path consumption inside the function closure reachable from the checking entrypoints must be lexically enclosed by a handler for Malformed, and this checker enforces that over its own abstract syntax tree, so a fourth omitted site cannot recur silently as the third one did. The grammar editorial delta path is consumed through a total accessor that returns a deterministic finding on an empty or unparsable path. (2) MEASUREMENT: the hostile-input generator now enumerates every path of this artifact at unlimited depth and at every array index, INCLUDING scalar leaf positions, which is exactly the space the totality rule quantifies over; the published counts are the live census of that space and are recomputed and compared on every run. Both repairs are proved load-bearing by executed batteries: removing any guard from a copy of this checker's own syntax tree is reported by the scan, and narrowing the generator back to container positions yields a strictly smaller enumeration that no longer matches the published counts.",
        "provenBy": ["PR-13-HOSTILE-INPUT-TOTALITY",
                     "PR-23-CANDIDATE-PATH-CONSUMER-GUARD"]},
    "EV9-IR-02-SECOND-SELFTEST-ENTRYPOINT-CLAIM-IS-NOT-ENFORCED": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "The unenforced sub-clause is now mechanically enforced. The reachability scan collects every string literal beginning with two hyphens anywhere in this checker's source and requires that set to equal the declared flag set, requires the declared flag set to equal the flags implied by checkerModeContract.entrypoints, and requires exactly one call to the selftest suite, lexically guarded by a declared flag. Inserting a second dispatch under an undocumented flag into a copy of this checker's syntax tree is reported rather than silently accepted.",
        "provenBy": ["PR-21-SELFTEST-REACHABILITY"]},
    "EV9-IR-R1-TAUTOLOGICAL-PROSE-BINDING": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Retained, not claimed closed. Genuinely new prose in this successor is still authored in the checker that emits it, so for that prose the equality comparison proves self-consistency rather than truth. The mitigation is unchanged and real: the prose is not the oracle, because each semantic obligation is separately evaluated against pinned dependency bytes and the executable probes remain the semantic authority. The three new registry entries reduce the residual slightly by binding the totality, path-guard and entrypoint prose to executed predicates, but they do not eliminate it.",
        "provenBy": []},
    "EV9-IR-R2-CUSTODY-AUTHORITY-JOIN-STILL-UNVERIFIED-BY-ANY-REVIEWER": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward unverified for a fourth generation, and flagged as such. The 23-object acquire/retry/release, pending-expiry, crash-gap repin and contention probes are executed only by the retained lineage foundation. No reviewer of v7, v8 or v9 reimplemented them independently, and this successor does not either. It should be assigned to a reviewer with an explicit brief to reimplement it.",
        "provenBy": []},
    "EV9-IR-R3-RECOVERY-MATRIX-ALIASES": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward. The recovery matrix alias rows inside the retained lineage foundation remain author-summarised. This successor does not repair them and does not claim they are executed.",
        "provenBy": []},
    "EV9-IR-R4-PRE-LINE-1-INTERPRETER-ACTIVITY": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward as an accurately disclosed limitation. The trust root is caller-owned and cannot be moved inside the script: interpreter activity that happens before line 1 cannot be undone by an in-script guard. The guard still refuses any invocation that is not the supported isolated start with exit 2, and the isolated start prevents the shadowing from taking effect. checkerModeContract.startupTrustRoot states this rather than claiming more.",
        "provenBy": []},
    "EV9-IR-R5-D9-AXES-AND-SITUATIONS-ARE-CHECKER-CONSTRUCTED": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward. Every row derives its class, ordered code payload and exit code from the pinned reference derivation, but the fault axes and situation prose that select those rows are constructed in the checker. Row CONTENT is derived; row COVERAGE is the checker author's choice, bounded only by the enforced requirement that the rows cover every pinned termination class. This matches what the predecessor repair specified and is not claimed to be more.",
        "provenBy": []},
    "EV9-IR-R6-SINGLE-ACCEPTED-VECTOR": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward. Exactly one accepted evaluation-proof vector is bound, so only the no-match claim shape is exercised at the Evidence layer. Other claim shapes remain unexercised at this layer.",
        "provenBy": []},
    "EV9-IR-O1-EXTRA-POSITIONAL-ARGUMENTS-SILENTLY-IGNORED": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "Argument handling is now total and explicit. A second positional candidate path, an unknown flag, a flag combination that asserts two modes at once, and a candidate path supplied alongside the emission mode are each refused with exit 2 and a named reason instead of being silently discarded. The refusal battery is executed on every run against the argument parser itself, so the discipline is measured rather than described.",
        "provenBy": ["PR-24-CLI-ARGUMENT-DISCIPLINE"]},
    "EV9-IR-O2-SELFTEST-PASS-LABEL-IS-A-SOURCE-LITERAL": {
        "state": "CLOSED-BY-DERIVATION",
        "closure": "The selftest banner prints the candidate path that was actually checked rather than a fixed source literal, and the reachability scan additionally requires the selftest function to contain no string constant equal to this generation's binding filename, so the label cannot silently drift back into a constant.",
        "provenBy": ["PR-21-SELFTEST-REACHABILITY"]},
    "EV9-IR-O3-DERIVED-ROOT-LAYER-COLLAPSES-WITHOUT-A-WARM-CONTEXT": {
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "No checking layer degrades silently on a cold context. The derived-root, registry and hostile-totality layers warm the derivation context from pinned authority when it is absent instead of returning a single generic finding, so a caller invoking the layers directly gets the same strength as the command line. This is measured: the probe clears the context, re-runs the complete checking layers over the derived successor, requires zero findings, and requires the context to have been rebuilt.",
        "provenBy": ["PR-25-COLD-CONTEXT-FULL-STRENGTH"]},
    "EV9-IR-O4-GRAMMAR-PROSE-IS-ONLY-PARTIALLY-BOUND": {
        "state": "OPEN-CARRIED-RESIDUAL",
        "closure": "Carried forward and disclosed in retainedResiduals. The grammar is bound to the encoder through its machine-readable tag, field-name and field-order table, and the prose is checked for the exact set rule only. The remaining prose is not parsed and could still diverge from the table without detection. The reviewer's independent decoder, written from the prose alone, reproduced the shipped bytes, which bounds the residual empirically without closing it.",
        "provenBy": []},
}

# This generation makes no editorial change to the wire grammar: the predecessor
# grammar already names the consumed evaluation-proof and retention generations
# and already disambiguates the inventory sort order.  The delta is therefore
# empty, and the layer that consumes it is exercised by the mutation suite and
# by the hostile matrix rather than by a manufactured edit.
GRAMMAR_DELTA: tuple[tuple[str, str, str, str], ...] = ()
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


def _steps_or_none(path: Any) -> list[Any] | None:
    """Total path parse for CANDIDATE-SUPPLIED strings (EV9-IR-01).

    Returns None instead of raising, so a caller can emit a deterministic
    finding.  Every candidate-supplied path consumption inside the checking
    closure goes through this accessor or through an explicit handler for
    Malformed, and PR-23 enforces that structurally over this source.
    """
    if not isinstance(path, str):
        return None
    try:
        return _path_steps(path)
    except Malformed:
        return None


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


def _get(root: Any, *keys: Any) -> Any:
    """Total member access; never raises and never needs a guard."""
    current = root
    for key in keys:
        if isinstance(key, int):
            if not isinstance(current, list) or not 0 <= key < len(current):
                return None
            current = current[key]
        else:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
    return current


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
            "successorPinPolicy": (
                "The pinned termination contract passed independent review with "
                "zero blocking findings and has not drifted. A v1.14 successor "
                "under concurrent authorship is deliberately NOT pinned here, "
                "because pinning a dependency whose own independent review does "
                "not yet exist would import an unaccepted authority. Re-pinning "
                "is separate successor work."),
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
            "consumed leaves. Evidence v10 binds all five and adds project-wide "
            "integrity enumeration plus serializable snapshot/CAS recovery. No "
            "dependency carries an Evidence back edge: none of the pinned "
            "dependency byte strings references this Evidence generation."),
    }


def build_grammar(predecessor_grammar: Any) -> dict[str, Any]:
    grammar = copy.deepcopy(predecessor_grammar)
    for path, before, after, _reason in GRAMMAR_DELTA:
        try:
            observed = _resolve(grammar, path)
            if observed != before:
                raise Malformed(
                    f"predecessor grammar {path} is not the expected "
                    "editorial base")
            _assign(grammar, path, after)
        except (Malformed, KeyError, IndexError, TypeError) as exc:
            raise Malformed(
                f"predecessor grammar {path} cannot be edited: {exc}") from exc
    if not isinstance(grammar, dict):
        raise Malformed("predecessor canonicalWireGrammar is not an object")
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
            "labels from an earlier generation. Neither is encoded into any "
            "record, enters any commitment, or is read by any derivation; the "
            "load-bearing accepted vector identity is "
            "dependencies.evaluationProof.acceptedVectorId, which is read from "
            "the pinned evaluation-proof artifact itself."),
    }


def build_hostile_contract(census: Mapping[str, Any],
                           guard: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 2,
        "rule": (
            "Every checking layer is total over hostile parsed JSON. Malformed "
            "input returns a deterministic finding and never an exception, at "
            "the root, at every root key, at every nested schema node and at "
            "every scalar leaf position."),
        "injections": [label for label, _ in HOSTILE_VALUES] + ["unknown-key"],
        "requiredEscapes": 0,
        "measurement": dict(
            [("generator",
              "The selftest calls the unguarded checking layers directly, so a "
              "broad exception handler cannot mask an escape. The generator "
              "enumerates the root and then EVERY path of the artifact at "
              "unlimited depth and at every array index, container positions "
              "and scalar leaf positions alike, and every enumerated path is "
              "round-trip verified before it is injected at. An injection that "
              "would leave the canonical bytes unchanged is not hostile input; "
              "it is skipped and counted rather than reported as a case."),
             ("quantifiedSpace",
              "The measured space is the same space the rule quantifies over. "
              "The "
              "predecessor measured 2992 cases over 240 container-only nodes "
              "and published zero escapes; its independent review enumerated "
              "the leaf-inclusive space and measured 44 unguarded escapes that "
              "the predecessor's own instrument could not observe. This "
              "generation enumerates that space in its own selftest.")] +
            [(key, census[key]) for key in CENSUS_KEYS] +
            [("requiredUnguardedEscapes", 0),
             ("requiredGuardedEscapes", 0),
             ("requiredSilentCases", 0)]),
        "pathConsumerGuard": dict(
            [("rule",
              "Every candidate-supplied string consumed as a path, index or key "
              "inside a checking layer is consumed through a total accessor, or "
              "inside a handler for Malformed that emits a deterministic "
              "finding. This is enforced structurally rather than site by site: "
              "the checker parses its own source, computes the function closure "
              "reachable from the checking entrypoints, and requires every "
              "consumption inside that closure to be lexically enclosed by a "
              "handler for Malformed."),
             ("consumers", list(PATH_CONSUMER_NAMES)),
             ("entryFunctions", list(PATH_GUARD_ENTRYPOINTS))] +
            [(key, guard[key]) for key in GUARD_KEYS] +
            [("predecessorDefect",
              "The predecessor guarded two of its three candidate-supplied path "
              "consumers and missed the third, which its independent review "
              "measured as 44 unguarded escapes out of a single leaf position "
              "family. A per-site fix would not have prevented a fourth site, "
              "so the property is enforced over the whole reachable closure "
              "instead.")]),
        "exitDiscipline": (
            "An unexpected exception inside a layer becomes a reported finding "
            "and exit 1. An input that cannot be read or parsed exits 2. An "
            "unsupported argument vector exits 2. A selftest over a dirty base "
            "exits 3. Nothing exits 0 on a malformed candidate."),
    }


def build_checker_mode_contract() -> dict[str, Any]:
    return {
        "schemaVersion": 2,
        "entrypoints": [
            f"python3 -I -B artifacts/{CHECKER}",
            f"python3 -I -B artifacts/{CHECKER} {DECLARED_FLAGS[0]}",
            f"python3 -I -B artifacts/{CHECKER} {DECLARED_FLAGS[1]}",
        ],
        "declaredFlags": list(DECLARED_FLAGS),
        "argumentDiscipline": (
            "Exactly one optional positional candidate path is accepted. A "
            "second positional path, an unknown flag, a candidate path supplied "
            "alongside the emission mode, and a request for both the emission "
            "mode and the selftest mode at once are each refused with exit 2 "
            "and a named reason rather than silently ignored. A repeated "
            "declared flag is accepted under set semantics and asserts nothing "
            "additional."),
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
            "and no second undocumented selftest entrypoint. Both clauses are "
            "mechanically enforced over this checker's own syntax tree: the "
            "selftest dispatch must precede any findings return, the set of "
            "command flag literals in the source must equal declaredFlags and "
            "the flags implied by entrypoints, and there must be exactly one "
            "call to the selftest suite, lexically guarded by a declared flag. "
            "--selftest always reaches the suite. If the base candidate is not "
            "clean the suite is refused with exit 3 and the dirty base is "
            "reported, because a mutation suite over a red base is not an "
            "oracle."),
        "escapeRule": (
            "A mutation that fails to apply, or that applies without changing "
            "the candidate bytes, is counted as an ESCAPE rather than as a "
            "pass. The same rule governs the source self-mutation battery: a "
            "syntax-tree mutation that does not change the tree, or that the "
            "corresponding scan does not report, is counted as an ESCAPE."),
        "exitCodes": {"clean": 0, "findings": 1,
                      "unsupportedInvocationOrInput": 2,
                      "selftestRefusedDirtyBase": 3},
        "checkerScopeBoundary": (
            "A green run of this authored checker is checker-scope evidence "
            "ONLY. It demonstrates no production durability, atomicity, "
            "restart, crash or concurrency behavior, grants no seal, freeze, "
            "integration or product acceptance, and does not sign CD-RT-5. "
            "Independent re-review of the exact v10 bytes remains REQUIRED."),
    }


def _id_list(review: Any, key: str) -> list[str]:
    rows = _get(review, key)
    if not isinstance(rows, list):
        raise Malformed(f"pinned review {key} is not an array")
    out: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise Malformed(f"pinned review {key}[{index}] has no string id")
        out.append(row["id"])
    return out


def predecessor_review_ids(review: Any) -> dict[str, list[str]]:
    """Read the required disposition vocabulary live from the pinned review."""
    if not isinstance(review, dict):
        raise Malformed("pinned predecessor review is not an object")
    confirmed = _get(review, "perFindingDisposition")
    if not isinstance(confirmed, list) or not confirmed:
        raise Malformed("pinned review perFindingDisposition is not a non-empty array")
    for index, row in enumerate(confirmed):
        if not isinstance(row, dict) or row.get("reviewerVerdict") != "PASS":
            raise Malformed(
                f"pinned review perFindingDisposition[{index}] is not a "
                "confirmed PASS; the predecessor repairs are not all confirmed")
    return {
        "new": _id_list(review, "newFindings"),
        "residual": _id_list(review, "residuals"),
        "observation": _id_list(review, "observations"),
        "confirmed": _id_list(review, "perFindingDisposition"),
    }


def lineage_review_ids(review: Any) -> list[str]:
    if not isinstance(review, dict):
        raise Malformed("pinned lineage review is not an object")
    return _id_list(review, "blockingFindings") + _id_list(review, "residuals")


def build_review_transfers(context: SemanticContext) -> list[dict[str, Any]]:
    carried = context.predecessor.get("reviewFindingTransfers")
    if not isinstance(carried, list) or not carried:
        raise Malformed("predecessor reviewFindingTransfers is not a non-empty array")
    ids = predecessor_review_ids(context.review)
    required = list(ids["new"]) + list(ids["residual"]) + list(ids["observation"])
    missing = [identifier for identifier in required
               if identifier not in DISPOSITIONS]
    if missing:
        raise Malformed("no disposition authored for " + ", ".join(missing))
    extra = [identifier for identifier in DISPOSITIONS if identifier not in required]
    if extra:
        raise Malformed("disposition names an identifier no pinned review "
                        "reports: " + ", ".join(extra))
    carried_ids = {row.get("id") for row in carried if isinstance(row, dict)}
    absent = [identifier
              for identifier in lineage_review_ids(context.lineage_review) +
              list(ids["confirmed"])
              if identifier not in carried_ids]
    if absent:
        raise Malformed(
            "the predecessor does not carry a disposition for " + ", ".join(absent))
    transfers = [copy.deepcopy(row) for row in carried]
    for identifier in required:
        row = DISPOSITIONS[identifier]
        transfers.append({
            "id": identifier,
            "source": PREDECESSOR_REVIEW,
            "sourceSha256": PINS[PREDECESSOR_REVIEW],
            "state": row["state"],
            "closure": row["closure"],
            "provenBy": list(row["provenBy"]),
        })
    return transfers


def build_foundation(predecessor_foundation: Any) -> dict[str, Any]:
    if not isinstance(predecessor_foundation, dict):
        raise Malformed("predecessor foundationImplementation is not an object")
    foundation = copy.deepcopy(predecessor_foundation)
    if foundation.get("status") != "CANDIDATE-COMPLETE-CHECKER-SCOPE":
        raise Malformed("predecessor foundation status is not the expected base")
    if foundation.get("blockingTodos") != []:
        raise Malformed("predecessor foundation still declares a blocking TODO")
    if not isinstance(foundation.get("closedTodos"), list) or \
            len(foundation["closedTodos"]) != 3:
        raise Malformed("predecessor foundation does not carry three closed TODOs")
    foundation["retainedPredecessorFoundation"] = {
        "artifact": PREDECESSOR,
        "sha256": PINS[PREDECESSOR],
        "checker": PREDECESSOR_CHECKER,
        "checkerSha256": PINS[PREDECESSOR_CHECKER],
        "execution": (
            "The pinned predecessor checker is executed from its verified byte "
            "snapshot on every run of this checker, and its own complete check "
            "is required to return zero findings against the pinned predecessor "
            "candidate in the same invocation. The predecessor was rejected on "
            "a reviewer judgement about a claim it published, not on a failure "
            "of its own checker, and that distinction is measured here rather "
            "than asserted. Executing it also verifies its 24 inherited pins, "
            "so the v7 and v8 lineage stays hash-bound without being pinned "
            "again in this generation."),
        "lineageFoundation": {
            "artifact": LINEAGE,
            "sha256": PINS[LINEAGE],
            "checker": LINEAGE_CHECKER,
            "checkerSha256": PINS[LINEAGE_CHECKER],
            "execution": (
                "The lineage foundation contract, its executable probes and its "
                "complete authored mutation suite are executed against the "
                "pinned lineage bytes from the verified snapshot on every run."),
        },
        "provenBy": ["PR-07-RETAINED-LINEAGE-FOUNDATION",
                     "PR-08-RETAINED-LINEAGE-MUTATION-SUITE",
                     "PR-26-RETAINED-PREDECESSOR-CHECKER-GREEN"],
    }
    return foundation


RESIDUALS_V10: tuple[str, ...] = (
    "The checker uses guarded durable-state and session test doubles plus "
    "copy/validate/swap. No production store, transaction, restart, crash "
    "durability or atomicity implementation was executed or demonstrated. The "
    "evidence grade remains IMPLEMENTABLE_UNEXECUTED and independent "
    "re-review of these exact bytes remains REQUIRED.",
    "A1-RTV4-02 is retained as a measurement residual. This artifact claims no "
    "cost advantage, no orders-of-magnitude advantage and no measured "
    "performance property of any kind.",
    "All Evidence v5/v6/v8/v9 SemanticEvidence, EvidenceDigest, RunId, "
    "TerminalRun and runSeal identities are unchanged. This successor changes "
    "neither what those identities are nor how they are proved; it repairs the "
    "totality of the checking layers over hostile input and the honesty of the "
    "measurement that quantifies it.",
    "V10 remains unresolved. CD-RT-5 and G19 remain blocked. This artifact "
    "does not decide the product default and does not sign CD-RT-5.",
    "The tautology residual is retained: genuinely new prose in this successor "
    "is authored in the checker that emits it, so for that prose the equality "
    "comparison proves self-consistency only. The executable probes and the "
    "pinned dependency predicates, not the prose, are the semantic oracle.",
    "The 23-object acquire/retry/release, pending-expiry, crash-gap repin and "
    "contention probes are executed only by the retained lineage foundation "
    "and have now been carried across four generations without any reviewer "
    "reimplementing them independently.",
    "The recovery matrix alias rows inside the retained lineage foundation "
    "remain author-summarised and are not claimed to be executed.",
    "acceptedGolden.id and acceptedGolden.sourceVectorId remain frozen labels "
    "from an earlier generation. They enter no commitment and no encoded "
    "record; the load-bearing accepted vector identity is read from the pinned "
    "evaluation-proof artifact.",
    "The grammar is bound to the encoder through its machine-readable tag, "
    "field-name and field-order table. The prose of the scalar and record "
    "rules is checked for the exact set rule only; the remaining prose is not "
    "parsed and could still diverge from the table without detection.",
    "The hostile-input measurement injects a single value at a single position "
    "per case. Combinatorial multi-position hostile inputs are not explored, "
    "so a zero escape count over this space is a bound on single-position "
    "non-totality and not a proof of totality over all hostile inputs.",
    "d9Mapping row COVERAGE remains checker-authored. Every row derives its "
    "class, ordered code payload and exit code from the pinned reference "
    "derivation, but the fault axes and situation prose that select the rows "
    "are constructed in this checker, bounded only by the enforced requirement "
    "that the rows cover every pinned termination class.",
    "Exactly one accepted evaluation-proof vector is bound, so only the "
    "no-match claim shape is exercised at this layer.",
    "The pinned termination contract is d9-exit-contract.v1.13, which passed "
    "independent review with zero blocking findings. A v1.14 successor is "
    "under concurrent authorship and is deliberately not pinned here, because "
    "its own independent review does not yet exist.",
)


def expected_successor(authority: Authority) -> dict[str, Any]:
    """Derive the complete expected evidence.v10 object.

    The hostile-space census is a property OF this object, so the assembly is
    run to a fixed point: assemble with a placeholder census, measure, and
    reassemble until the measurement of the assembled object equals the
    measurement published inside it.  Convergence is required, never assumed.
    """
    predecessor = authority.json(PREDECESSOR)
    if not isinstance(predecessor, dict):
        raise Malformed("predecessor evidence root is not an object")
    grammar = build_grammar(predecessor.get("canonicalWireGrammar"))
    derived = derive_identity(grammar, authority.json(EP8), authority.json(RT22))
    d9_mapping = derive_d9_mapping(authority)
    request_context = derive_request_context_binding(authority)
    context = SemanticContext(authority, derived, d9_mapping, request_context)
    guard = _path_guard_scan()

    def assemble(census: Mapping[str, Any]) -> dict[str, Any]:
        authority.census = dict(census)
        registry_entries = semantic_entries(context)
        successor: dict[str, Any] = {}
        for key, value in predecessor.items():
            successor[key] = copy.deepcopy(value)
        successor["version"] = 10
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
            "reviewBlockingFindingCount":
                REVIEW_BINDINGS[PREDECESSOR_REVIEW]["blockingFindingCount"],
            "lineagePredecessor": LINEAGE,
            "lineagePredecessorSha256": PINS[LINEAGE],
            "lineageRejection": LINEAGE_REVIEW,
            "lineageRejectionSha256": PINS[LINEAGE_REVIEW],
        }
        successor["reviewFindingTransfers"] = build_review_transfers(context)
        successor["dependencies"] = build_dependencies(context)
        successor["canonicalWireGrammar"] = grammar
        successor["d9Mapping"] = d9_mapping
        successor["acceptedGolden"] = golden_from_identity(
            predecessor.get("acceptedGolden"), derived)
        successor["runSubstitutionGoldens"] = copy.deepcopy(derived["substitutions"])
        successor["retainedResiduals"] = list(RESIDUALS_V10)
        successor["foundationImplementation"] = build_foundation(
            predecessor.get("foundationImplementation"))
        successor["evidenceRecomputationContract"] = \
            build_recomputation_contract(derived)
        successor["requestContextBinding"] = request_context
        successor["semanticBindingRegistry"] = {
            "schemaVersion": 1,
            "rule": (
                "Each entry carries a prose claim, a closed machine-readable "
                "predicate and the artifact leaf paths whose semantic content "
                "it underwrites. The checker requires the prose to equal the "
                "deterministic rendering of the predicate AND requires the "
                "predicate to evaluate true against pinned dependency bytes or "
                "against this checker's own executed measurements. Editing the "
                "prose alone fails rendering; editing the predicate alone fails "
                "evaluation; editing both consistently fails evaluation. A "
                "declaration can therefore not act as its own oracle."),
            "escapeCoverageRule": (
                "Every leaf path listed by an entry must exist in this "
                "artifact, and the union of the listed paths must cover every "
                "surface an independent review reported as escaping, "
                "semantically unbound or quantitatively false."),
            "entries": registry_entries,
        }
        successor["hostileInputTotalityContract"] = \
            build_hostile_contract(census, guard)
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
            "predecessorChecker":
                f"{PREDECESSOR_CHECKER}@{PINS[PREDECESSOR_CHECKER]}",
            "rejection": f"{PREDECESSOR_REVIEW}@{PINS[PREDECESSOR_REVIEW]}",
            "rejectionDecision": REVIEW_BINDINGS[PREDECESSOR_REVIEW]["decision"],
            "rejectionBlockingFindingCount":
                REVIEW_BINDINGS[PREDECESSOR_REVIEW]["blockingFindingCount"],
            "changedRootKeys": changed,
            "addedRootKeys": sorted(added),
            "carriedRootKeys": carried,
            "protectedIdentityKeys": [],
            "grammarEditorialDelta": [
                {"path": path, "predecessorValue": before,
                 "successorValue": after, "reason": reason}
                for path, before, after, reason in GRAMMAR_DELTA],
            "retainedHistoricalLabelPaths": list(RETAINED_HISTORICAL_LABEL_PATHS),
            "scope": (
                "There is no protected-identity freeze in this generation. The "
                "checker derives the complete expected successor object from "
                "the pinned predecessor bytes plus the pinned dependency bytes "
                "and requires exact equality, so every leaf is derived rather "
                "than declared. Carried roots equal the predecessor exactly; "
                "changed and added roots are recomputed from pinned authority, "
                "from this checker's own executed measurements, or by the same "
                "construction the checker verifies. The wire grammar is carried "
                "unchanged, so the editorial delta is empty in this generation. "
                "Text-substring sampling is not a successor oracle, and "
                "freezing a root by byte-equality alone is not treated as "
                "semantic binding."),
        }
        return successor

    census: dict[str, Any] = {key: 0 for key in CENSUS_KEYS}
    successor = assemble(census)
    for _ in range(8):
        measured = _node_census(successor)
        if measured == census:
            break
        census = measured
        successor = assemble(census)
    else:
        raise Malformed("the hostile-space census did not reach a fixed point")
    if _node_census(successor) != census:
        raise Malformed("the hostile-space census is not a fixed point")
    authority.context = context
    authority.expected = successor
    authority.census = dict(census)
    return successor


def _ensure_context(authority: Authority) -> Any:
    """Warm the derivation context from pinned authority when it is cold.

    EV9-IR-O3: no checking layer may silently degrade to a weaker check merely
    because no earlier call warmed the context.  Nothing here reads the
    candidate, so warming cannot make the comparison self-referential.
    """
    context = getattr(authority, "context", None)
    if context is not None:
        return context
    expected_successor(authority)
    return getattr(authority, "context", None)


# ---------------------------------------------------------------------------
# Section 6.  Total checking layers and the executed probe registry.
#
# EVERY candidate-supplied string consumed as a path in this section goes
# through _steps_or_none or through an explicit handler for Malformed.  That is
# not a convention: PR-23 parses this source, computes the function closure
# reachable from the checking entrypoints and refuses any consumption inside
# that closure which is not lexically enclosed by such a handler.
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
    try:
        identifiers.update(lineage_review_ids(authority.json(LINEAGE_REVIEW)))
    except Malformed:
        pass
    try:
        for group in predecessor_review_ids(
                authority.json(PREDECESSOR_REVIEW)).values():
            identifiers.update(group)
    except Malformed:
        pass
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
            findings.append(f"forbidden custody-root alias on an E10 surface: {text[:60]!r}")
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
        ids = predecessor_review_ids(authority.json(PREDECESSOR_REVIEW))
        lineage = lineage_review_ids(authority.json(LINEAGE_REVIEW))
    except Malformed as exc:
        return [f"pinned review identifiers cannot be read: {exc}"]
    required = set(ids["new"]) | set(ids["residual"]) | set(ids["observation"])
    carried_required = set(lineage) | set(ids["confirmed"])
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
    dropped = sorted(carried_required - present)
    if dropped:
        findings.append(
            f"{len(dropped)} independently confirmed predecessor disposition(s) "
            f"were dropped rather than carried, first {dropped[0]}")
    fabricated = sorted(
        identifier for identifier in present
        if identifier.startswith("EV9-IR") and identifier not in required)
    if fabricated:
        findings.append(
            f"fabricated predecessor finding disposition {fabricated[0]}")
    authority.record_probe("PR-17-FINDING-DISPOSITION-CLOSURE", not findings)
    return findings


def _registry_findings(candidate: Any, authority: Authority) -> list[str]:
    findings: list[str] = []
    try:
        context = _ensure_context(authority)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"semantic binding registry has no derivation context: "
                f"{type(exc).__name__}: {exc}"]
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
                findings.append(f"{identifier}: bound path {path!r} is absent "
                                "or not a parsable path")
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


# The exact surfaces the independent reviews reported as escaping, semantically
# unbound, or quantitatively false.  Every one must be covered by the semantic
# binding registry.  The last three are the v9 review's own findings.
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
    "hostileInputTotalityContract.rule",
    "hostileInputTotalityContract.measurement",
    "checkerModeContract.selftestReachability",
)


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
    """EV9-IR-01 repair site.

    grammarEditorialDelta[N].path is CANDIDATE-SUPPLIED.  The predecessor
    consumed it as _path_steps(path)[-1] with no handler, which its independent
    review measured as 44 unguarded escapes.  It is consumed here through the
    total accessor, so an empty or unparsable path is a deterministic finding.
    """
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["grammar delta scan requires an object root"]
    grammar = candidate.get("canonicalWireGrammar")
    base = _get(authority.json(PREDECESSOR), "canonicalWireGrammar")
    if not isinstance(grammar, dict) or not isinstance(base, dict):
        return ["canonicalWireGrammar is not an object on both generations"]
    declared = _get(candidate, "successorDelta", "grammarEditorialDelta")
    if not isinstance(declared, list):
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
        steps = _steps_or_none(path)
        if steps is None:
            findings.append(
                f"grammarEditorialDelta[{index}].path {path!r} is not a "
                "parsable path")
            continue
        declared_paths.append(path)
        leaf = steps[-1]
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


def _hostile_totality_findings(candidate: Any,
                               authority: Authority) -> list[str]:
    """The published totality measurement must be the live census.

    EV9-IR-01: the predecessor published counts taken over a strictly smaller
    space than the rule it offered them as evidence for.  Here the counts are
    recomputed from the derived successor on every run and compared leaf for
    leaf, so understating the space is a finding rather than an omission.
    """
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["hostile totality scan requires an object root"]
    try:
        _ensure_context(authority)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"hostile totality census unavailable: "
                f"{type(exc).__name__}: {exc}"]
    census = getattr(authority, "census", None)
    if not isinstance(census, dict):
        return ["the hostile-space census has not been derived"]
    contract = candidate.get("hostileInputTotalityContract")
    if not isinstance(contract, dict):
        return [f"hostileInputTotalityContract: expected object, "
                f"found {_kind(contract)}"]
    if contract.get("requiredEscapes") != 0 or \
            isinstance(contract.get("requiredEscapes"), bool):
        findings.append("hostileInputTotalityContract.requiredEscapes is not 0")
    injections = contract.get("injections")
    live_injections = [label for label, _ in HOSTILE_VALUES] + ["unknown-key"]
    if injections != live_injections:
        findings.append(
            "hostileInputTotalityContract.injections is not the live injection "
            f"table of {len(live_injections)} values")
    published = contract.get("measurement")
    if not isinstance(published, dict):
        findings.append(f"hostileInputTotalityContract.measurement: expected "
                        f"object, found {_kind(published)}")
    else:
        for key in CENSUS_KEYS:
            difference = _first_difference(
                published.get(key), census[key],
                f"hostileInputTotalityContract.measurement.{key}")
            if difference is not None:
                findings.append(
                    "the published hostile-space measurement is not the live "
                    f"enumeration over the derived successor: {difference}")
        for key in ("requiredUnguardedEscapes", "requiredGuardedEscapes",
                    "requiredSilentCases"):
            if published.get(key) != 0 or isinstance(published.get(key), bool):
                findings.append(
                    f"hostileInputTotalityContract.measurement.{key} is not 0")
    guard = contract.get("pathConsumerGuard")
    if not isinstance(guard, dict):
        findings.append(f"hostileInputTotalityContract.pathConsumerGuard: "
                        f"expected object, found {_kind(guard)}")
    else:
        scan = _path_guard_scan()
        for key in GUARD_KEYS:
            difference = _first_difference(
                guard.get(key), scan[key],
                f"hostileInputTotalityContract.pathConsumerGuard.{key}")
            if difference is not None:
                findings.append(
                    "the published path-consumer guard measurement is not the "
                    f"live scan of this checker: {difference}")
        if guard.get("consumers") != list(PATH_CONSUMER_NAMES):
            findings.append("pathConsumerGuard.consumers is not the live "
                            "consumer set")
        if guard.get("entryFunctions") != list(PATH_GUARD_ENTRYPOINTS):
            findings.append("pathConsumerGuard.entryFunctions is not the live "
                            "entrypoint set")
    return findings


def _source_mode_findings(candidate: Any, authority: Authority) -> list[str]:
    """Bind the declared entrypoint set to this checker's actual flag set."""
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["checker mode scan requires an object root"]
    contract = candidate.get("checkerModeContract")
    if not isinstance(contract, dict):
        return [f"checkerModeContract: expected object, found {_kind(contract)}"]
    if contract.get("declaredFlags") != list(DECLARED_FLAGS):
        findings.append(
            "checkerModeContract.declaredFlags is not this checker's flag set")
    entrypoints = contract.get("entrypoints")
    if not isinstance(entrypoints, list) or not entrypoints:
        findings.append("checkerModeContract.entrypoints is not a non-empty array")
        return findings
    implied: set[str] = set()
    for line in entrypoints:
        if not isinstance(line, str):
            findings.append("checkerModeContract.entrypoints carries a non-text row")
            return findings
        implied.update(word for word in line.split() if word.startswith("--"))
    scan = _selftest_entrypoint_scan()
    if implied != set(DECLARED_FLAGS) or implied != set(scan["flags"]):
        findings.append(
            "the flags implied by checkerModeContract.entrypoints "
            f"{sorted(implied)} are not the flag literals present in this "
            f"checker's source {sorted(scan['flags'])}")
    return findings


def _source_findings(source: Any, expected: Mapping[str, Any]) -> list[str]:
    if not isinstance(source, (bytes, bytearray)):
        return []
    canonical_source = pretty(expected)
    if bytes(source) != canonical_source:
        return ["candidate file bytes are not the canonical emission of the "
                "derived successor (run --emit-candidate to see the exact bytes)"]
    return []


def _derived_root_findings(candidate: Any, authority: Authority) -> list[str]:
    """Compare each derived root to its live derivation from pinned authority.

    This layer is independent of the whole-object successor comparison: it
    holds even when successor equality is disabled, which is how the mutation
    suite demonstrates that the binding is not carried by that comparison
    alone.  EV9-IR-O3: a cold context is warmed rather than degraded.
    """
    findings: list[str] = []
    if not isinstance(candidate, dict):
        return ["derived-root scan requires an object root"]
    try:
        context = _ensure_context(authority)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"derived roots have no derivation context: "
                f"{type(exc).__name__}: {exc}"]
    if context is None:
        return ["derived roots have no derivation context"]
    try:
        dependencies = build_dependencies(context)
        d9_mapping = derive_d9_mapping(authority)
        request_context = derive_request_context_binding(authority)
        grammar = build_grammar(_get(authority.json(PREDECESSOR),
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
    findings.extend(_hostile_totality_findings(candidate, authority))
    findings.extend(_source_mode_findings(candidate, authority))
    findings.extend(_registry_findings(candidate, authority))
    findings.extend(_disposition_findings(candidate, authority))
    return findings


# ---------------------------------------------------------------------------
# Section 7.  Self-inspection: argument discipline, the candidate-path guard
# scan (EV9-IR-01) and the entrypoint-closure scan (EV9-IR-02).
#
# All three read this checker's own source.  The source cannot change during a
# run, so it is read and parsed once and the parse is reused; every scan is a
# pure function of that tree and can therefore also be run against a MUTATED
# tree, which is how the selftest proves each scan is load-bearing.
# ---------------------------------------------------------------------------

_OWN_SOURCE: bytes | None = None
_OWN_TREE: Any = None
_GUARD_SCAN_CACHE: dict[str, Any] | None = None
_ENTRYPOINT_SCAN_CACHE: dict[str, Any] | None = None


def _own_tree() -> Any:
    global _OWN_SOURCE, _OWN_TREE
    if _OWN_TREE is None:
        try:
            _OWN_SOURCE = (HERE / CHECKER).read_bytes()
            _OWN_TREE = ast.parse(_OWN_SOURCE.decode("utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
            raise Malformed(
                f"cannot parse this checker's own source: {type(exc).__name__}"
            ) from exc
    return _OWN_TREE


def _parse_argv(argv: Any) -> tuple[frozenset[str], Any]:
    """Total argument discipline (EV9-IR-O1).

    An unknown flag, a second positional path, a candidate path supplied with
    the emission mode, or a request for two modes at once is refused with a
    named reason instead of being silently discarded.
    """
    if not isinstance(argv, (list, tuple)) or not argv:
        raise UnsupportedInvocation("no argument vector was supplied")
    flags: list[str] = []
    positional: list[Any] = []
    for item in list(argv)[1:]:
        if isinstance(item, str) and item.startswith("--"):
            if item not in DECLARED_FLAGS:
                raise UnsupportedInvocation(f"unknown flag {item!r}")
            flags.append(item)
        else:
            positional.append(item)
    if len(positional) > 1:
        raise UnsupportedInvocation(
            f"{len(positional)} positional candidate paths supplied; exactly "
            "one is accepted")
    if DECLARED_FLAGS[0] in flags and DECLARED_FLAGS[1] in flags:
        raise UnsupportedInvocation(
            f"{DECLARED_FLAGS[0]} and {DECLARED_FLAGS[1]} are mutually exclusive")
    if DECLARED_FLAGS[1] in flags and positional:
        raise UnsupportedInvocation(
            f"{DECLARED_FLAGS[1]} takes no candidate path")
    return frozenset(flags), (positional[0] if positional else None)


_ARGUMENT_BATTERY: tuple[tuple[str, list[Any], bool], ...] = (
    ("bare", ["x"], True),
    ("candidate-only", ["x", "cand.json"], True),
    ("selftest", ["x", "--selftest"], True),
    ("selftest-with-candidate", ["x", "cand.json", "--selftest"], True),
    ("selftest-repeated", ["x", "--selftest", "--selftest"], True),
    ("selftest-before-path", ["x", "--selftest", "cand.json"], True),
    ("emit", ["x", "--emit-candidate"], True),
    ("unknown-flag", ["x", "--foundation-selftest"], False),
    ("unknown-flag-with-selftest", ["x", "--selftest", "--bogus"], False),
    ("bare-double-dash", ["x", "--"], False),
    ("two-positionals", ["x", "a.json", "b.json"], False),
    ("two-positionals-with-selftest", ["x", "a.json", "b.json", "--selftest"], False),
    ("emit-with-candidate", ["x", "--emit-candidate", "a.json"], False),
    ("emit-and-selftest", ["x", "--emit-candidate", "--selftest"], False),
    ("empty-vector", [], False),
    ("not-a-vector", "x --selftest", False),
)


def _cli_argument_findings(authority: Authority) -> list[str]:
    findings: list[str] = []
    for label, argv, accepted in _ARGUMENT_BATTERY:
        try:
            _parse_argv(argv)
        except UnsupportedInvocation:
            if accepted:
                findings.append(
                    f"argument discipline: {label} is a supported invocation "
                    "but was refused")
            continue
        except Exception as exc:                      # noqa: BLE001 - reported
            findings.append(
                f"argument discipline: {label} raised "
                f"{type(exc).__name__} instead of a refusal")
            continue
        if not accepted:
            findings.append(
                f"argument discipline: {label} is not a supported invocation "
                "but was accepted silently")
    authority.record_probe("PR-24-CLI-ARGUMENT-DISCIPLINE", not findings)
    return findings


PATH_CONSUMER_NAMES: tuple[str, ...] = ("_path_steps", "_resolve", "_assign")
PATH_GUARD_ENTRYPOINTS: tuple[str, ...] = (
    "check", "check_guarded", "candidate_layers", "hostile_matrix",
    "_hostile_nodes", "_node_census",
)
PATH_GUARD_REQUIRED_FUNCTIONS: tuple[str, ...] = (
    "_grammar_delta_findings", "_registry_findings",
    "_producer_obligation_findings", "_steps_or_none",
)
GUARD_KEYS: tuple[str, ...] = (
    "scannedFunctions", "guardedCallSites", "unguardedCallSites",
)


def _handles_malformed(handler: Any) -> bool:
    declared = handler.type
    if declared is None:
        return True
    candidates = declared.elts if isinstance(declared, ast.Tuple) else [declared]
    for node in candidates:
        if isinstance(node, ast.Name) and node.id in (
                "Malformed", "Exception", "BaseException"):
            return True
    return False


def _collect_path_calls(node: Any, protected: bool,
                        sites: list[tuple[int, bool]]) -> None:
    """Record every candidate-path consumption and whether it is guarded."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
            node.func.id in PATH_CONSUMER_NAMES:
        sites.append((getattr(node, "lineno", 0), protected))
    if isinstance(node, ast.Try):
        guarded = protected or any(_handles_malformed(handler)
                                   for handler in node.handlers)
        for child in node.body:
            _collect_path_calls(child, guarded, sites)
        for handler in node.handlers:
            for child in handler.body:
                _collect_path_calls(child, protected, sites)
        for child in list(node.orelse) + list(node.finalbody):
            _collect_path_calls(child, protected, sites)
        return
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        # A nested definition runs later, possibly elsewhere; it inherits no
        # protection from the handler that lexically encloses its definition.
        for child in ast.iter_child_nodes(node):
            _collect_path_calls(child, False, sites)
        return
    for child in ast.iter_child_nodes(node):
        _collect_path_calls(child, protected, sites)


def _path_guard_scan(tree: Any = None) -> dict[str, Any]:
    """EV9-IR-01 structural repair.

    Every candidate-supplied path consumption inside the function closure
    reachable from the checking entrypoints must be lexically enclosed by a
    handler for Malformed.  This is what makes the repair systemic instead of
    per-site: a fourth omitted consumer is reported, not missed.
    """
    global _GUARD_SCAN_CACHE
    cached = tree is None
    if cached and _GUARD_SCAN_CACHE is not None:
        return _GUARD_SCAN_CACHE
    subject = _own_tree() if tree is None else tree
    functions = {node.name: node for node in subject.body
                 if isinstance(node, ast.FunctionDef)}
    reachable: set[str] = set()
    frontier = [name for name in PATH_GUARD_ENTRYPOINTS if name in functions]
    missing_entrypoints = [name for name in PATH_GUARD_ENTRYPOINTS
                           if name not in functions]
    while frontier:
        name = frontier.pop()
        if name in reachable:
            continue
        reachable.add(name)
        for child in ast.walk(functions[name]):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) \
                    and child.func.id in functions and \
                    child.func.id not in reachable:
                frontier.append(child.func.id)
    # A consumer's own body defines the raising contract it exists to provide;
    # the obligation is on its CALLERS, so the consumers are not scanned.
    reachable -= set(PATH_CONSUMER_NAMES)
    guarded = 0
    unguarded: list[str] = []
    for name in sorted(reachable):
        sites: list[tuple[int, bool]] = []
        for child in ast.iter_child_nodes(functions[name]):
            _collect_path_calls(child, False, sites)
        for lineno, protected in sites:
            if protected:
                guarded += 1
            else:
                unguarded.append(f"{name} line {lineno}")
    result = {
        "scannedFunctions": len(reachable),
        "guardedCallSites": guarded,
        "unguardedCallSites": len(unguarded),
        "unguarded": unguarded,
        "missingEntrypoints": missing_entrypoints,
        "absentRequired": [name for name in PATH_GUARD_REQUIRED_FUNCTIONS
                           if name not in reachable],
    }
    if cached:
        _GUARD_SCAN_CACHE = result
    return result


def _path_guard_findings(authority: Authority, tree: Any = None) -> list[str]:
    findings: list[str] = []
    try:
        scan = _path_guard_scan(tree)
    except Malformed as exc:
        authority.record_probe("PR-23-CANDIDATE-PATH-CONSUMER-GUARD", False)
        return [str(exc)]
    for site in scan["unguarded"]:
        findings.append(
            "candidate-supplied path consumption is not enclosed by a handler "
            f"for Malformed: {site}")
    if scan["missingEntrypoints"]:
        findings.append(
            "the path-guard scan cannot find checking entrypoint "
            f"{scan['missingEntrypoints'][0]}")
    if scan["absentRequired"]:
        findings.append(
            "the path-guard scan does not reach known path-consuming layer "
            f"{scan['absentRequired'][0]}")
    if scan["guardedCallSites"] < 3:
        findings.append(
            f"the path-guard scan found only {scan['guardedCallSites']} guarded "
            "call site(s), so it cannot be distinguished from a vacuous scan")
    if tree is None:
        authority.record_probe("PR-23-CANDIDATE-PATH-CONSUMER-GUARD", not findings)
    return findings


def _selftest_entrypoint_scan(tree: Any = None) -> dict[str, Any]:
    """EV9-IR-02: the command flag set and the selftest dispatch set."""
    global _ENTRYPOINT_SCAN_CACHE
    cached = tree is None
    if cached and _ENTRYPOINT_SCAN_CACHE is not None:
        return _ENTRYPOINT_SCAN_CACHE
    subject = _own_tree() if tree is None else tree
    # A string literal only acts as a command flag when it is TESTED against
    # the argument vector, so the closed set is the literals that appear inside
    # a comparison, together with the literals of the DECLARED_FLAGS constant
    # itself.  Flag-shaped strings that appear only as inert data - the
    # refusal battery's hostile vectors, the source self-mutation battery's
    # payloads - gate nothing and are not entrypoints.
    flags: set[str] = set()
    for node in ast.walk(subject):
        if isinstance(node, ast.Compare):
            for child in ast.walk(node):
                if isinstance(child, ast.Constant) and \
                        isinstance(child.value, str) and \
                        child.value.startswith("--"):
                    flags.add(child.value)
    declared_literals: set[str] = set()
    for node in subject.body:
        if isinstance(node, ast.AnnAssign) and \
                isinstance(node.target, ast.Name) and \
                node.target.id == "DECLARED_FLAGS" and node.value is not None:
            declared_literals.update(
                child.value for child in ast.walk(node.value)
                if isinstance(child, ast.Constant) and
                isinstance(child.value, str))
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "DECLARED_FLAGS"
                for target in node.targets):
            declared_literals.update(
                child.value for child in ast.walk(node.value)
                if isinstance(child, ast.Constant) and
                isinstance(child.value, str))
    flags |= declared_literals
    dispatches = 0
    guarded_dispatches = 0

    def visit(node: Any, inside_selftest: bool, guarded_by: Any) -> None:
        nonlocal dispatches, guarded_dispatches
        if isinstance(node, ast.FunctionDef) and node.name == "selftest":
            inside_selftest = True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                node.func.id == "selftest" and not inside_selftest:
            dispatches += 1
            if guarded_by is not None:
                guarded_dispatches += 1
        if isinstance(node, ast.If):
            literals = {child.value for child in ast.walk(node.test)
                        if isinstance(child, ast.Constant) and
                        isinstance(child.value, str)}
            declared = literals & set(DECLARED_FLAGS)
            for child in node.body:
                visit(child, inside_selftest,
                      sorted(declared)[0] if declared else guarded_by)
            for child in node.orelse:
                visit(child, inside_selftest, guarded_by)
            visit(node.test, inside_selftest, guarded_by)
            return
        for child in ast.iter_child_nodes(node):
            visit(child, inside_selftest, guarded_by)

    visit(subject, False, None)
    selftest_literals: set[str] = set()
    for node in ast.walk(subject):
        if isinstance(node, ast.FunctionDef) and node.name == "selftest":
            selftest_literals.update(
                child.value for child in ast.walk(node)
                if isinstance(child, ast.Constant) and
                isinstance(child.value, str))
    result = {
        "flags": sorted(flags),
        "flagCount": len(flags),
        "declaredLiterals": sorted(declared_literals),
        "dispatchCount": dispatches,
        "guardedDispatchCount": guarded_dispatches,
        "bindingLiteralInSelftest": BINDING in selftest_literals,
    }
    if cached:
        _ENTRYPOINT_SCAN_CACHE = result
    return result


def _selftest_reachability_findings(authority: Authority,
                                    tree: Any = None) -> list[str]:
    findings: list[str] = []
    try:
        subject = _own_tree() if tree is None else tree
    except Malformed as exc:
        authority.record_probe("PR-21-SELFTEST-REACHABILITY", False)
        return [str(exc)]
    main_fn = [node for node in subject.body
               if isinstance(node, ast.FunctionDef) and node.name == "main"]
    if len(main_fn) != 1:
        findings.append("this checker does not define exactly one main()")
        if tree is None:
            authority.record_probe("PR-21-SELFTEST-REACHABILITY", False)
        return findings
    selftest_index = None
    findings_return_index = None
    for index, statement in enumerate(main_fn[0].body):
        text = ast.dump(statement)
        if selftest_index is None and f"'{DECLARED_FLAGS[0]}'" in text and \
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
    for node in ast.walk(subject):
        if isinstance(node, ast.Name) and node.id in {
                "TODO_FINDINGS", "TODO_DECLARATIONS"}:
            findings.append(
                "this checker carries an unconditional TODO findings gate")
            break
    scan = _selftest_entrypoint_scan(tree)
    if scan["declaredLiterals"] != sorted(DECLARED_FLAGS):
        findings.append(
            f"the DECLARED_FLAGS constant in this checker's source declares "
            f"{scan['declaredLiterals']}, which is not the flag set this run "
            f"uses, {sorted(DECLARED_FLAGS)}")
    if scan["flags"] != sorted(DECLARED_FLAGS):
        findings.append(
            f"this checker's source carries command flag literals {scan['flags']}, "
            f"which is not the declared entrypoint set {sorted(DECLARED_FLAGS)}; "
            "a second undocumented entrypoint is refused")
    if scan["dispatchCount"] != 1:
        findings.append(
            f"main() dispatches to the selftest suite {scan['dispatchCount']} "
            "time(s); exactly one dispatch is permitted")
    if scan["guardedDispatchCount"] != scan["dispatchCount"]:
        findings.append(
            "a dispatch to the selftest suite is not guarded by a declared flag")
    if scan["bindingLiteralInSelftest"]:
        findings.append(
            "selftest() carries the binding filename as a source literal "
            "instead of reporting the candidate path it actually checked")
    if tree is None:
        authority.record_probe("PR-21-SELFTEST-REACHABILITY", not findings)
    return findings


# ---------------------------------------------------------------------------
# Section 8.  Hostile-input totality matrix (EV8-IR-07, EV9-IR-01).
#
# The enumeration is the whole document: the root, every root key, and every
# nested position at unlimited depth and every array index, CONTAINER AND
# SCALAR LEAF alike.  The predecessor descended only into dict/list children,
# so scalar leaf positions - including the one family that falsified its own
# published claim - were structurally unreachable by its own instrument.
# ---------------------------------------------------------------------------

HOSTILE_VALUES: tuple[tuple[str, Any], ...] = (
    ("null", None), ("integer", 0), ("negative", -1), ("float", 1.5),
    ("true", True), ("false", False), ("empty-text", ""), ("text", "x"),
    ("empty-array", []), ("empty-object", {}), ("nested-array", [[]]),
    ("nested-object", [{"unknown": 1}]),
    # Path-shaped negatives.  Every one of these is unparsable or empty as a
    # path, which is exactly the family the independent review used to falsify
    # the predecessor's totality claim at scalar leaf positions.
    ("control-text", "a\x00b\x1fc\x7f"),
    ("bom-text", "é﻿\U0001f600"),
    ("digest-text", "sha256:" + "0" * 64),
)
CENSUS_KEYS: tuple[str, ...] = (
    "enumeratedPaths", "containerPaths", "scalarLeafPaths", "dictPaths",
    "pathsNotRoundTripping", "injectionValues", "enumeratedCases",
    "noOpInjections", "executedCases",
)
_SHALLOW_DEPTH = 2


def _enumerate_positions(base: Any, full: bool = True,
                         leaves: bool = True) -> list[tuple[str, Any]]:
    positions: list[tuple[str, Any]] = [("", base)]

    def walk(value: Any, prefix: str, depth: int) -> None:
        if not full and depth >= _SHALLOW_DEPTH:
            return
        if isinstance(value, dict):
            children = [(f"{prefix}.{key}" if prefix else str(key), value[key])
                        for key in value]
        elif isinstance(value, list):
            children = [(f"{prefix}[{index}]", item)
                        for index, item in enumerate(value)]
        else:
            return
        for child_path, child in children:
            container = isinstance(child, (dict, list))
            if container or leaves:
                positions.append((child_path, child))
            if container:
                walk(child, child_path, depth + 1)

    walk(base, "", 0)
    return positions


def _round_trips(base: Any, path: str, value: Any) -> bool:
    if path == "":
        return True
    try:
        return _resolve(base, path) is value
    except Malformed:
        return False


def _hostile_nodes(base: Any, full: bool = True,
                   leaves: bool = True) -> list[str]:
    """Injection positions, round-trip verified.

    ``leaves`` exists so the selftest can narrow the generator back to the
    container-only enumeration the predecessor used and demonstrate that the
    published counts then become detectably wrong.
    """
    ordered: list[str] = []
    seen: set[str] = set()
    for path, value in _enumerate_positions(base, full, leaves):
        if path in seen or not _round_trips(base, path, value):
            continue
        seen.add(path)
        ordered.append(path)
    return ordered


def _same_leaf(left: Any, right: Any) -> bool:
    return type(left) is type(right) and left == right


def _node_census(base: Any, full: bool = True,
                 leaves: bool = True) -> dict[str, Any]:
    """The live measurement of the enumerated hostile space."""
    containers = 0
    scalars = 0
    dicts = 0
    not_round_tripping = 0
    no_ops = 0
    counted: set[str] = set()
    for path, value in _enumerate_positions(base, full, leaves):
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
        for _label, injected in HOSTILE_VALUES:
            if path != "" and _same_leaf(value, injected):
                no_ops += 1
    paths = len(counted)
    enumerated = paths * len(HOSTILE_VALUES) + dicts
    return {
        "enumeratedPaths": paths,
        "containerPaths": containers,
        "scalarLeafPaths": scalars,
        "dictPaths": dicts,
        "pathsNotRoundTripping": not_round_tripping,
        "injectionValues": len(HOSTILE_VALUES),
        "enumeratedCases": enumerated,
        "noOpInjections": no_ops,
        "executedCases": enumerated - no_ops,
    }


def _invoke_layers(candidate: Any,
                   authority: Authority) -> tuple[Any, Any]:
    """One unguarded pass.  Returns (findings, escaped-exception-or-None)."""
    try:
        return candidate_layers(candidate, authority), None
    except Exception as exc:                          # noqa: BLE001 - measured
        return None, exc


def check_guarded(candidate: Any, authority: Authority) -> list[str]:
    findings, escaped = _invoke_layers(candidate, authority)
    if escaped is not None:
        return [f"checking layer raised {type(escaped).__name__}: {escaped}"]
    return findings


def hostile_matrix(base: Any, authority: Authority, full: bool = True,
                   leaves: bool = True) -> dict[str, Any]:
    """Drive hostile parsed JSON through the UNGUARDED candidate layers.

    The probe log is restored to its entry state before every case, so the
    silent-case count is a genuine per-case measurement and not an artifact of
    state left behind by an earlier case.
    """
    nodes = _hostile_nodes(base, full, leaves)
    cases = 0
    skipped = 0
    escapes = 0
    guarded_escapes = 0
    guarded_exercised = 0
    silent = 0
    escaped_examples: list[str] = []
    silent_examples: list[str] = []
    baseline_log = dict(authority.probe_log)

    def restore() -> None:
        authority.probe_log.clear()
        authority.probe_log.update(baseline_log)

    for path in nodes:
        injections = list(HOSTILE_VALUES)
        try:
            target = base if path == "" else _resolve(base, path)
        except Malformed:
            continue
        if isinstance(target, dict):
            injections.append(("unknown-key", "<insert>"))
        first = True
        for label, value in injections:
            if label != "unknown-key" and path != "" and \
                    _same_leaf(target, value):
                skipped += 1
                continue
            candidate: Any
            if path == "":
                candidate = copy.deepcopy(base) if label == "unknown-key" \
                    else copy.deepcopy(value)
                if label == "unknown-key" and isinstance(candidate, dict):
                    candidate["ev10UnknownRootKey"] = 1
            else:
                candidate = copy.deepcopy(base)
                if label == "unknown-key":
                    try:
                        node = _resolve(candidate, path)
                    except Malformed:
                        continue
                    if not isinstance(node, dict):
                        continue
                    node["ev10UnknownNestedKey"] = 1
                else:
                    try:
                        _assign(candidate, path, copy.deepcopy(value))
                    except (Malformed, KeyError, IndexError, TypeError):
                        continue
            cases += 1
            restore()
            findings, escaped = _invoke_layers(candidate, authority)
            if escaped is not None:
                escapes += 1
                if len(escaped_examples) < 5:
                    escaped_examples.append(
                        f"{path or '<root>'}:{label} -> "
                        f"{type(escaped).__name__}: {escaped}")
            elif not findings:
                silent += 1
                if len(silent_examples) < 5:
                    silent_examples.append(f"{path or '<root>'}:{label}")
            # The guarded entrypoint wrapper is exercised on every case where
            # the unguarded layer raised - the only cases where it can matter -
            # and additionally once per enumerated path as a live control.
            if escaped is not None or first:
                guarded_exercised += 1
                restore()
                try:
                    _ = check_guarded(candidate, authority)
                except BaseException:                 # noqa: BLE001 - measured
                    guarded_escapes += 1
            first = False
    restore()
    return {"cases": cases, "nodes": len(nodes), "escapes": escapes,
            "guardedEscapes": guarded_escapes,
            "guardedExercised": guarded_exercised,
            "skippedNoOps": skipped, "silent": silent,
            "escapedExamples": escaped_examples,
            "silentExamples": silent_examples}


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

    v8 = authority.module(LINEAGE_CHECKER)
    lineage = authority.json(LINEAGE)
    guarded("PR-07-RETAINED-LINEAGE-FOUNDATION",
            lambda: v8._foundation_contract_errors(
                copy.deepcopy(lineage), run_probes=True))
    guarded("PR-08-RETAINED-LINEAGE-MUTATION-SUITE",
            lambda: v8.foundation_selftest(copy.deepcopy(lineage)))
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

    def retained_predecessor_checker() -> list[str]:
        """The predecessor was rejected on a judgement, not a checker failure.

        Executing its complete check here measures that distinction instead of
        asserting it, and verifies its own 24 inherited pins in passing, so the
        v7/v8 lineage stays hash-bound without being pinned again.
        """
        module = authority.module(PREDECESSOR_CHECKER)
        outcome = module.check(copy.deepcopy(authority.json(PREDECESSOR)),
                               module._BOOTSTRAP_AUTHORITY,
                               authority.snapshots[PREDECESSOR])
        if not isinstance(outcome, list):
            return ["the retained predecessor checker did not return findings"]
        return list(outcome)

    guarded("PR-26-RETAINED-PREDECESSOR-CHECKER-GREEN",
            retained_predecessor_checker)

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
            if b"evidence.v10" in authority.snapshots[name]:
                problems.append(f"{name} carries an Evidence v10 back edge")
        return problems

    guarded("PR-16-DEPENDENCY-ACYCLICITY", acyclicity)

    def cold_context() -> list[str]:
        """EV9-IR-O3: the layers must be full strength on a cold context."""
        expected = getattr(authority, "expected", None)
        if not isinstance(expected, dict):
            return ["there is no derived successor to re-check from a cold context"]
        saved_context = authority.context
        saved_census = authority.census
        # Seed so a disposition may cite this probe; the conjunction below can
        # only lower the recorded outcome, never raise it.
        authority.probe_log.setdefault("PR-25-COLD-CONTEXT-FULL-STRENGTH", True)
        try:
            authority.context = None
            authority.census = None
            cold = candidate_layers(copy.deepcopy(expected), authority)
            rewarmed = authority.context is not None
        finally:
            authority.context = saved_context
            authority.census = saved_census
        if cold:
            return ["a cold-context run of the checking layers is not full "
                    f"strength: {cold[0]}"]
        if not rewarmed:
            return ["the cold-context run did not warm the derivation context"]
        return []

    guarded("PR-25-COLD-CONTEXT-FULL-STRENGTH", cold_context)
    return findings


def check(candidate: Any, authority: Authority,
          source: Any = None) -> list[str]:
    """Full v10 check.  Returns findings; never raises on hostile input.

    The self-inspection scans and the hostile matrix run BEFORE the dependency
    probes, so that by the time the cold-context probe re-runs the complete
    checking layers every probe a disposition may cite has already been
    recorded.  The candidate-driven layers run last.
    """
    findings: list[str] = []
    try:
        expected = expected_successor(authority)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"expected successor construction failed: "
                f"{type(exc).__name__}: {exc}"]
    findings.extend(_selftest_reachability_findings(authority))
    findings.extend(_path_guard_findings(authority))
    findings.extend(_cli_argument_findings(authority))
    saved = dict(authority.probe_log)
    hostile = hostile_matrix(expected, authority, full=False)
    authority.probe_log.clear()
    authority.probe_log.update(saved)
    authority.record_probe("PR-13-HOSTILE-INPUT-TOTALITY",
                           hostile["escapes"] == 0 and
                           hostile["guardedEscapes"] == 0 and
                           hostile["silent"] == 0)
    if hostile["escapes"] or hostile["guardedEscapes"] or hostile["silent"]:
        findings.append(
            f"hostile input matrix: {hostile['escapes']} unguarded, "
            f"{hostile['guardedEscapes']} guarded escape(s) and "
            f"{hostile['silent']} silent case(s)")
    findings.extend(run_dependency_probes(authority))
    try:
        findings.extend(candidate_layers(candidate, authority, source))
    except Exception as exc:                          # noqa: BLE001 - reported
        findings.append(
            f"checking layer raised {type(exc).__name__}: {exc}")
    return findings


# ---------------------------------------------------------------------------
# Section 9.  Mutation suite.
#
# Every mutation the independent reviews reported as escaping or as
# semantically unbound appears below, together with the successor-specific
# surfaces and the negatives that make THIS generation's two repairs
# load-bearing.  A mutation that fails to apply, or that applies without
# changing the candidate bytes, is counted as an ESCAPE.
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


def _close_open_residual(candidate: Any, _authority: Authority) -> None:
    for row in candidate["reviewFindingTransfers"]:
        if isinstance(row, dict) and row.get("id") == \
                "EV9-IR-R2-CUSTODY-AUTHORITY-JOIN-STILL-UNVERIFIED-BY-ANY-REVIEWER":
            row["state"] = "CLOSED-BY-EXECUTED-PROBE"
            return
    raise Malformed("the custody-join residual disposition is absent")


def _fabricate_disposition(candidate: Any, _authority: Authority) -> None:
    candidate["reviewFindingTransfers"].append({
        "id": "EV9-IR-03-INVENTED", "source": PREDECESSOR_REVIEW,
        "sourceSha256": PINS[PREDECESSOR_REVIEW],
        "state": "CLOSED-BY-EXECUTED-PROBE",
        "closure": "invented", "provenBy": ["PR-01-GRAMMAR-RECOMPUTATION"]})


def _drop_disposition(candidate: Any, _authority: Authority) -> None:
    rows = candidate["reviewFindingTransfers"]
    for index, row in enumerate(rows):
        if isinstance(row, dict) and row.get("id") == \
                "EV9-IR-01-HOSTILE-TOTALITY-CONTRACT-IS-FALSIFIED-AT-SCALAR-LEAVES":
            rows.pop(index)
            return
    raise Malformed("the EV9-IR-01 disposition is absent")


def _drop_confirmed_disposition(candidate: Any, _authority: Authority) -> None:
    rows = candidate["reviewFindingTransfers"]
    for index, row in enumerate(rows):
        if isinstance(row, dict) and row.get("id") == \
                "EV8-IR-07-HOSTILE-PARSED-JSON-RAISES-INSTEAD-OF-REPORTING":
            rows.pop(index)
            return
    raise Malformed("the confirmed predecessor disposition is absent")


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


def _census_registry_edit(candidate: Any, _authority: Authority) -> None:
    """Understate the measured space consistently in prose AND predicate."""
    entries = candidate["semanticBindingRegistry"]["entries"]
    for entry in entries:
        if entry.get("kind") == "hostile-space-census":
            entry["params"]["scalarLeafPaths"] = 0
            entry["params"]["enumeratedPaths"] = 240
            entry["claim"] = _render(entry["kind"], entry["params"])
            return
    raise Malformed("no hostile-space-census entry")


def _guard_registry_edit(candidate: Any, _authority: Authority) -> None:
    entries = candidate["semanticBindingRegistry"]["entries"]
    for entry in entries:
        if entry.get("kind") == "path-consumer-guard":
            entry["params"]["unguardedCallSites"] = 44
            entry["claim"] = _render(entry["kind"], entry["params"])
            return
    raise Malformed("no path-consumer-guard entry")


def _entrypoint_registry_edit(candidate: Any, _authority: Authority) -> None:
    entries = candidate["semanticBindingRegistry"]["entries"]
    for entry in entries:
        if entry.get("kind") == "selftest-entrypoint-closure":
            entry["params"]["flags"] = sorted(
                list(DECLARED_FLAGS) + ["--foundation-selftest"])
            entry["params"]["flagCount"] = 3
            entry["claim"] = _render(entry["kind"], entry["params"])
            return
    raise Malformed("no selftest-entrypoint-closure entry")


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


def _delta_row(path: Any) -> Callable[[Any, Authority], None]:
    """A hostile grammar editorial delta row carrying a candidate path."""
    def apply(candidate: Any, _authority: Authority) -> None:
        candidate["successorDelta"]["grammarEditorialDelta"] = [{
            "path": path,
            "predecessorValue": "a declared predecessor value",
            "successorValue": "a declared successor value",
            "reason": "a declared editorial reason"}]
    return apply


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
          "Evidence v10 feeds EP8 and RT22; Evidence may redefine lease and "
          "purge semantics."), True),
    ("P3-invariants-emptied", _set("invariants", []), False),
    ("P3-invariant-absorption",
     _set("invariants[0].assert",
          "Indeterminate outcomes may be recorded as an authoritative pass."),
     False),
    ("P3-semantic-join-retention",
     _set("semanticJoins.retention",
          "Evidence v10 defines its own lease, purge and D9 semantics locally."),
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
    ("foundation-todos-reopened",
     _set("foundationImplementation.blockingTodos",
          ["TODO: the changed-root binding is unresolved"]), False),
    ("foundation-retained-checker-detached",
     _set("foundationImplementation.retainedPredecessorFoundation.checkerSha256",
          "0" * 64), False),
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
    ("version-regressed", _set("version", 9), False),
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
    ("supersedes-rejection-downgraded",
     _set("supersedes.reviewDecision", "PASS"), False),
    ("termination-dependency-hash-detached",
     _set("dependencies.terminationContract.sha256", "0" * 64), True),
    ("request-context-review-flipped",
     _set("dependencies.requestContext.reviewDecision", "REJECT"), True),
    ("disposition-dropped", _drop_disposition, True),
    ("confirmed-disposition-dropped", _drop_confirmed_disposition, True),
    ("residual-declared-closed", _close_open_residual, True),
    ("disposition-fabricated", _fabricate_disposition, True),
    ("residuals-emptied", _set("retainedResiduals", []), False),
    ("selftest-exit-code-collapsed",
     _set("checkerModeContract.exitCodes.selftestRefusedDirtyBase", 0), False),
    ("unknown-root-key",
     _set("ev10UnknownRootKey", "injected"), False),
    ("dropped-root-key", _drop("availabilityDifferential"), False),
    ("alias-injection", _alias_injection, True),
    ("stale-generation-injection", _stale_injection, True),
    ("historical-label-injection", _historical_label_injection, True),
    ("cd-rt-5-self-signature", _cd_rt_5_self_signature, True),
    # --- EV9-IR-01: the repaired path-consumer site, driven directly. -------
    # Each of these carries a candidate-supplied path string through the layer
    # the predecessor consumed unguarded.  If the guard is removed, the
    # semantic layers RAISE and the suite records a semantic ESCAPE.
    ("delta-path-empty", _delta_row(""), True),
    ("delta-path-unparsable", _delta_row("["), True),
    ("delta-path-control-text", _delta_row("a\x00b\x1fc\x7f"), True),
    ("delta-path-digest-text", _delta_row("sha256:" + "0" * 64), True),
    ("delta-path-nonstring", _delta_row(5), True),
    ("delta-path-null", _delta_row(None), True),
    ("delta-path-phantom",
     _delta_row("records.SemanticEvidenceV1.fields[5].type"), True),
    ("registry-bound-path-empty",
     _set("semanticBindingRegistry.entries[0].boundArtifactPaths[0]", ""), True),
    ("registry-bound-path-unparsable",
     _set("semanticBindingRegistry.entries[0].boundArtifactPaths[0]", "["), True),
    ("registry-bound-path-nonstring",
     _set("semanticBindingRegistry.entries[0].boundArtifactPaths[0]", 5), True),
    # --- EV9-IR-01: the republished measurement must be the live census. ----
    ("hostile-escapes-allowed",
     _set("hostileInputTotalityContract.requiredEscapes", 5), True),
    ("hostile-paths-understated",
     _set("hostileInputTotalityContract.measurement.enumeratedPaths", 240), True),
    ("hostile-cases-understated",
     _set("hostileInputTotalityContract.measurement.executedCases", 2992), True),
    ("hostile-leaves-erased",
     _set("hostileInputTotalityContract.measurement.scalarLeafPaths", 0), True),
    ("hostile-required-escapes-nonzero",
     _set("hostileInputTotalityContract.measurement.requiredUnguardedEscapes",
          44), True),
    ("hostile-injections-narrowed",
     _set("hostileInputTotalityContract.injections",
          [label for label, _ in HOSTILE_VALUES[:12]] + ["unknown-key"]), True),
    ("hostile-rule-narrowed",
     _set("hostileInputTotalityContract.rule",
          "Every checking layer is total over hostile parsed JSON at the root "
          "and at every root key."), False),
    ("registry-census-consistently-understated", _census_registry_edit, True),
    # --- EV9-IR-01: the path-consumer guard measurement. --------------------
    ("guard-unguarded-sites-declared",
     _set("hostileInputTotalityContract.pathConsumerGuard.unguardedCallSites",
          44), True),
    ("guard-sites-understated",
     _set("hostileInputTotalityContract.pathConsumerGuard.guardedCallSites", 0),
     True),
    ("guard-consumers-narrowed",
     _set("hostileInputTotalityContract.pathConsumerGuard.consumers",
          ["_resolve"]), True),
    ("guard-entrypoints-narrowed",
     _set("hostileInputTotalityContract.pathConsumerGuard.entryFunctions",
          ["check"]), True),
    ("registry-guard-consistently-falsified", _guard_registry_edit, True),
    # --- EV9-IR-02: the entrypoint set. -------------------------------------
    ("checker-flags-widened",
     _set("checkerModeContract.declaredFlags",
          list(DECLARED_FLAGS) + ["--foundation-selftest"]), True),
    ("checker-entrypoint-added",
     _set("checkerModeContract.entrypoints",
          [f"python3 -I -B artifacts/{CHECKER}",
           f"python3 -I -B artifacts/{CHECKER} --selftest",
           f"python3 -I -B artifacts/{CHECKER} --emit-candidate",
           f"python3 -I -B artifacts/{CHECKER} --foundation-selftest"]), True),
    ("registry-entrypoints-consistently-widened", _entrypoint_registry_edit, True),
    ("selftest-reachability-claim-weakened",
     _set("checkerModeContract.selftestReachability",
          "The selftest is reachable."), False),
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
                semantic_escapes.append(
                    f"{label}: semantic layer raised {type(exc).__name__}: {exc}")
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


# ---------------------------------------------------------------------------
# Section 10.  Source self-mutation battery.
#
# The two repairs this generation makes are enforced by scans over this
# checker's own syntax tree.  A scan that reports nothing is worthless unless
# it is shown to report SOMETHING, so every scan is re-run against a mutated
# copy of the tree in which the property it enforces has been broken.  A
# mutation that does not change the tree, or that the scan does not report, is
# an ESCAPE under the same rule that governs the candidate mutation suite.
# ---------------------------------------------------------------------------

class _UnwrapGuard(ast.NodeTransformer):
    """Delete the try/except Malformed that guards a path consumer."""

    def __init__(self, consumer: str):
        self.consumer = consumer
        self.done = False

    def visit_Try(self, node: Any) -> Any:
        self.generic_visit(node)
        if self.done:
            return node
        uses = any(isinstance(child, ast.Call) and
                   isinstance(child.func, ast.Name) and
                   child.func.id == self.consumer for child in ast.walk(node))
        if uses and any(_handles_malformed(handler) for handler in node.handlers):
            self.done = True
            return node.body
        return node


class _RenameFlag(ast.NodeTransformer):
    def __init__(self, old: str, new: str):
        self.old = old
        self.new = new

    def visit_Constant(self, node: Any) -> Any:
        if isinstance(node.value, str) and node.value == self.old:
            return ast.copy_location(ast.Constant(value=self.new), node)
        return node


def _function_def(tree: Any, name: str) -> Any:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise Malformed(f"the mutated tree has no function {name}")


def _selftest_dispatch_index(main_fn: Any) -> int:
    for index, statement in enumerate(main_fn.body):
        text = ast.dump(statement)
        if f"'{DECLARED_FLAGS[0]}'" in text and "Name(id='selftest'" in text:
            return index
    raise Malformed("the mutated tree has no selftest dispatch")


def _unwrap(function_name: str,
            consumer: str) -> Callable[[Any], Any]:
    def mutate(tree: Any) -> Any:
        new = copy.deepcopy(tree)
        _UnwrapGuard(consumer).visit(_function_def(new, function_name))
        return ast.fix_missing_locations(new)
    return mutate


def _mutate_second_dispatch(tree: Any) -> Any:
    new = copy.deepcopy(tree)
    main_fn = _function_def(new, "main")
    injected = ast.parse(
        'if "--foundation-selftest" in flags:\n'
        '    return selftest(candidate, source, authority, path)\n').body[0]
    main_fn.body.insert(0, injected)
    return ast.fix_missing_locations(new)


def _mutate_dispatch_after_findings(tree: Any) -> Any:
    new = copy.deepcopy(tree)
    main_fn = _function_def(new, "main")
    index = _selftest_dispatch_index(main_fn)
    main_fn.body.append(main_fn.body.pop(index))
    return ast.fix_missing_locations(new)


def _mutate_dispatch_removed(tree: Any) -> Any:
    new = copy.deepcopy(tree)
    main_fn = _function_def(new, "main")
    main_fn.body.pop(_selftest_dispatch_index(main_fn))
    return ast.fix_missing_locations(new)


def _mutate_unguarded_dispatch(tree: Any) -> Any:
    """Call the suite from main() without any flag guarding the call."""
    new = copy.deepcopy(tree)
    main_fn = _function_def(new, "main")
    injected = ast.parse(
        "selftest(candidate, source, authority, path)\n").body[0]
    main_fn.body.insert(0, injected)
    return ast.fix_missing_locations(new)


def _mutate_todo_gate(tree: Any) -> Any:
    new = copy.deepcopy(tree)
    main_fn = _function_def(new, "main")
    main_fn.body.insert(0, ast.parse("if TODO_FINDINGS:\n    return 1\n").body[0])
    return ast.fix_missing_locations(new)


def _mutate_renamed_flag(tree: Any) -> Any:
    new = copy.deepcopy(tree)
    _RenameFlag(DECLARED_FLAGS[1], "--emit").visit(new)
    return ast.fix_missing_locations(new)


def _mutate_selftest_literal_label(tree: Any) -> Any:
    new = copy.deepcopy(tree)
    selftest_fn = _function_def(new, "selftest")
    selftest_fn.body.insert(
        1, ast.Expr(value=ast.Constant(value=BINDING)))
    return ast.fix_missing_locations(new)


def _mutate_noop(tree: Any) -> Any:
    return copy.deepcopy(tree)


SOURCE_MUTATIONS: tuple[tuple[str, Callable[[Any], Any], str, bool], ...] = (
    ("guard-removed-from-grammar-delta-consumer",
     _unwrap("_steps_or_none", "_path_steps"), "path-guard", True),
    ("guard-removed-from-registry-consumer",
     _unwrap("_registry_findings", "_resolve"), "path-guard", True),
    ("guard-removed-from-producer-obligation-consumer",
     _unwrap("_producer_obligation_findings", "_resolve"), "path-guard", True),
    ("guard-removed-from-hostile-enumerator",
     _unwrap("_round_trips", "_resolve"), "path-guard", True),
    ("second-undocumented-selftest-entrypoint",
     _mutate_second_dispatch, "selftest-reachability", True),
    ("selftest-dispatch-after-findings-return",
     _mutate_dispatch_after_findings, "selftest-reachability", True),
    ("selftest-dispatch-removed",
     _mutate_dispatch_removed, "selftest-reachability", True),
    ("selftest-dispatch-unguarded",
     _mutate_unguarded_dispatch, "selftest-reachability", True),
    ("unconditional-todo-gate", _mutate_todo_gate, "selftest-reachability", True),
    ("declared-flag-renamed", _mutate_renamed_flag, "selftest-reachability", True),
    ("selftest-label-is-a-literal",
     _mutate_selftest_literal_label, "selftest-reachability", True),
    # Controls: an unchanged tree must be reported CLEAN by both scans, so a
    # scan that reports unconditionally is itself an escape.
    ("control-unmutated-tree-path-guard", _mutate_noop, "path-guard", False),
    ("control-unmutated-tree-reachability",
     _mutate_noop, "selftest-reachability", False),
)


def run_source_mutation_suite(authority: Authority) -> dict[str, Any]:
    escapes: list[str] = []
    applied = 0
    try:
        tree = _own_tree()
    except Malformed as exc:
        return {"total": len(SOURCE_MUTATIONS), "applied": 0,
                "escapes": [str(exc)]}
    baseline = ast.dump(tree)
    for label, mutate, scan, must_report in SOURCE_MUTATIONS:
        try:
            mutated = mutate(tree)
        except Exception as exc:                      # noqa: BLE001 - measured
            escapes.append(f"{label}: source mutation failed to apply "
                           f"({type(exc).__name__}: {exc})")
            continue
        changed = ast.dump(mutated) != baseline
        if must_report and not changed:
            escapes.append(f"{label}: source mutation applied without changing "
                           "the syntax tree")
            continue
        if not must_report and changed:
            escapes.append(f"{label}: the control mutation changed the tree")
            continue
        applied += 1
        if scan == "path-guard":
            reported = _path_guard_findings(authority, mutated)
        else:
            reported = _selftest_reachability_findings(authority, mutated)
        if must_report and not reported:
            escapes.append(f"{label}: the scan did not report the broken "
                           "property, so it is not load-bearing")
        if not must_report and reported:
            escapes.append(f"{label}: the scan reports on an unmutated tree: "
                           f"{reported[0]}")
    return {"total": len(SOURCE_MUTATIONS), "applied": applied,
            "escapes": escapes}


def run_generator_narrowing_suite(base: Any,
                                  census: Mapping[str, Any]) -> dict[str, Any]:
    """Prove the widened enumeration is load-bearing (EV9-IR-01).

    Narrowing the generator back to the container-only enumeration the
    predecessor used must produce a strictly smaller space whose counts no
    longer match the published measurement, and must lose the scalar leaf
    positions at which candidate-supplied paths actually live.
    """
    escapes: list[str] = []
    live = _node_census(base)
    narrowed = _node_census(base, leaves=False)
    for key in CENSUS_KEYS:
        if live[key] != census.get(key):
            escapes.append(
                f"published measurement {key} {census.get(key)!r} is not the "
                f"live enumeration {live[key]!r}")
    if narrowed["enumeratedPaths"] >= live["enumeratedPaths"]:
        escapes.append("the container-only enumeration is not strictly smaller "
                       "in paths, so widening the generator changed nothing")
    if narrowed["enumeratedCases"] >= live["enumeratedCases"]:
        escapes.append("the container-only enumeration is not strictly smaller "
                       "in cases")
    if narrowed["scalarLeafPaths"] != 0:
        escapes.append("the container-only enumeration still reports scalar "
                       "leaf positions")
    if live["scalarLeafPaths"] <= 0:
        escapes.append("the widened enumeration reports no scalar leaf position")
    if live["pathsNotRoundTripping"] != 0:
        escapes.append(
            f"{live['pathsNotRoundTripping']} enumerated path(s) do not round "
            "trip, so part of the artifact is not addressable by the generator")
    if any(narrowed[key] == live[key] for key in
           ("enumeratedPaths", "enumeratedCases")):
        escapes.append("narrowing the generator left a published count intact")
    widened_nodes = set(_hostile_nodes(base))
    narrow_nodes = set(_hostile_nodes(base, leaves=False))
    witnesses = [path for path in widened_nodes
                 if path.startswith("semanticBindingRegistry.entries[") and
                 ".boundArtifactPaths[" in path]
    if not witnesses:
        escapes.append("the widened enumeration does not reach any "
                       "candidate-supplied path leaf")
    elif any(path in narrow_nodes for path in witnesses):
        escapes.append("the container-only enumeration already reached a "
                       "candidate-supplied path leaf, so it cannot demonstrate "
                       "the predecessor's blind spot")
    return {"paths": live["enumeratedPaths"],
            "narrowedPaths": narrowed["enumeratedPaths"],
            "cases": live["executedCases"],
            "narrowedCases": narrowed["enumeratedCases"],
            "witnesses": len(witnesses), "escapes": escapes}


def selftest(candidate: Any, source: bytes, authority: Authority,
             path: pathlib.Path) -> int:
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
    source_suite = run_source_mutation_suite(authority)
    census = getattr(authority, "census", None)
    narrowing = run_generator_narrowing_suite(
        candidate, census if isinstance(census, dict) else {})
    saved = dict(authority.probe_log)
    try:
        hostile = hostile_matrix(candidate, authority, full=True)
    finally:
        authority.probe_log.clear()
        authority.probe_log.update(saved)
    failures: list[str] = list(suite["escapes"]) + list(suite["semanticEscapes"])
    failures.extend(source_suite["escapes"])
    failures.extend(narrowing["escapes"])
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
    if isinstance(census, dict):
        if hostile["cases"] != census["executedCases"]:
            failures.append(
                f"the matrix executed {hostile['cases']} cases but the "
                f"published measurement declares {census['executedCases']}")
        if hostile["nodes"] != census["enumeratedPaths"]:
            failures.append(
                f"the matrix enumerated {hostile['nodes']} paths but the "
                f"published measurement declares {census['enumeratedPaths']}")
        if hostile["skippedNoOps"] != census["noOpInjections"]:
            failures.append(
                f"the matrix skipped {hostile['skippedNoOps']} no-op injections "
                f"but the published measurement declares "
                f"{census['noOpInjections']}")
    else:
        failures.append("the hostile-space census is not available")
    if failures:
        for failure in failures:
            print("SELFTEST-FAIL:", failure)
        return 1
    print(f"SELFTEST-PASS: {path.name}")
    print(f"  mutations: {suite['applied']}/{suite['total']} applied and "
          f"rejected; 0 escapes; {suite['semanticChecked']} of them also "
          "rejected with successor-equality disabled, so the binding is not "
          "carried by whole-object comparison alone")
    print(f"  source self-mutations: {source_suite['applied']}/"
          f"{source_suite['total']} applied; every broken property reported by "
          "its scan and neither scan reports on an unmutated tree")
    print(f"  generator narrowing: the leaf-inclusive enumeration reaches "
          f"{narrowing['paths']} paths and {narrowing['cases']} executed cases; "
          f"narrowing it back to container positions reaches "
          f"{narrowing['narrowedPaths']} paths and {narrowing['narrowedCases']} "
          f"cases and loses all {narrowing['witnesses']} candidate-supplied "
          "path leaves, so the published counts become detectably wrong")
    print(f"  hostile parsed JSON: {hostile['cases']} cases over "
          f"{hostile['nodes']} enumerated paths "
          f"({hostile['skippedNoOps']} no-op injections skipped); "
          f"{hostile['escapes']} unguarded escapes, "
          f"{hostile['guardedEscapes']} guarded escapes over "
          f"{hostile['guardedExercised']} guarded exercises, "
          f"{hostile['silent']} silent cases")
    print(f"  executed probes: {sum(1 for value in authority.probe_log.values() if value)}"
          f"/{len(PROBE_IDS)} green")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; independent re-review REQUIRED; no seal, "
          "freeze, integration, product acceptance or CD-RT-5 disposition")
    return 0


def main(argv: list[str]) -> int:
    authority = _BOOTSTRAP_AUTHORITY
    try:
        flags, requested = _parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"EV10-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    if "--emit-candidate" in flags:
        try:
            sys.stdout.buffer.write(pretty(expected_successor(authority)))
        except Exception as exc:                      # noqa: BLE001 - reported
            print(f"cannot emit candidate: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            return 2
        return 0
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        candidate, source = load_source(path)
    except (OSError, UnicodeError, AuthorityLoadError, json.JSONDecodeError,
            DuplicateKeyError, TypeError, ValueError) as exc:
        print(f"cannot load Evidence candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in flags:
        return selftest(candidate, source, authority, path)
    findings = check(candidate, authority, source)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    green = sum(1 for value in authority.probe_log.values() if value)
    census = getattr(authority, "census", None)
    measured = census["enumeratedPaths"] if isinstance(census, dict) else 0
    print(f"Evidence v10 OK - {path.name}; {len(PINS)} inputs hash-verified "
          "before execution; complete successor derived from the pinned "
          "predecessor and dependencies; every published commitment recomputed "
          f"under the declared grammar; {len(D9_SITUATIONS) + 1} termination "
          f"rows derived live from D9 v1.13; hostile-input totality quantified "
          f"over all {measured} paths including scalar leaves; "
          f"{green}/{len(PROBE_IDS)} probes green")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; no seal, freeze, integration, product "
          "acceptance or CD-RT-5 disposition is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
