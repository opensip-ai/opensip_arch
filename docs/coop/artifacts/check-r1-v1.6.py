#!/usr/bin/env python3
"""Retained checker for r1-lifetime-neutrality.conformance.v1.6.json.

Why this file exists, stated before anything else.

  v1.6 concedes, in its own bytes, that no retained checker reads them, and
  IMPLEMENTATION-FREEZE.md section 7.1 grades an unread artifact as
  disqualifying for application.  v1.6's author was scoped to one file and
  section 7.6 forbids editing the pinned check-r1-v1.5.py.  Neither constraint
  reaches a NEW file.  This is that file.  It edits nothing pinned, it repoints
  no head, it closes no row, and writing it does not apply the candidate.

  check-r1-v1.5.py is NOT touched, NOT imported and NOT executed.  It is read
  as inert bytes for one purpose only: to confirm that v1.6's recorded
  measuredSelfReport.checkerSha256AtEmit_readOnly still describes the live file.

What is MEASURED here, in the order the checks run:

  0  Integrity.   Every input this instrument computes over is read as inert
                  bytes, hashed, and compared against a digest pinned in THIS
                  source, BEFORE any of it is decoded or parsed.  A mismatch
                  prints one named refusal and exits 2.
  1  Posture.     status, reviewStatus, binds, sealRecommendation and
                  evidenceGrade are the reviewed values.  A checker that would
                  stay green across `status: APPLIED` measures nothing.
  2  Closure.     All seventeen frozenInputs rows are verified against live
                  bytes.  Exactly two coordinator-owned prose documents are
                  DECLARED MOBILE by the artifact's own driftDisclosure and are
                  allowed to move; drift on any other row is a refusal.
  3  Carry.       Every key v1.6 claims to carry from v1.5 is compared
                  canonically against the LIVE v1.5 bytes, including the ten
                  positive vectors WITH their 5555../6666../8888../9999..
                  derivationDigest placeholders, the 25 closed types, the 30
                  adversarial controls and the 9 static-closure fixtures.
  4  Law 18.      Exact-type scalar admission over every leaf of
                  $.policyDerivationIdentity, and over every recordValue before
                  a single byte of it is encoded.  A JSON type that differs
                  from the declared type is rejected BEFORE content is compared.
                  This class defeated C-2 at v3, v5, v6, v7 and v8, each time
                  inside the repair's own self-certification.
  5  Recipe.      The grammar, tags, framing, namespace and domain are declared
                  in THIS source and are then compared against the artifact's
                  recordGrammar and preimage steps.  Nothing is read out of the
                  artifact and handed back to it.
  6  Arithmetic.  Every published digest is RECOMPUTED from the published
                  recordValue by TWO independently written encoders -- one
                  table-driven, one flat imperative with hand-rolled big-endian
                  -- and the two are compared against each other and against the
                  artifact.  recordBytes, recordSha256, leafRootHex,
                  outerPreimageHex, derivationDigest and completeRecordHex.
  7  Injectivity. A TOTAL grammar-directed decoder is exhibited.
                  decode(encode(x)) == x is asserted LITERALLY -- as canonical
                  bytes, so a bool never passes for an int -- on all 21 records,
                  and encode(decode(r)) == r on the same 21.  Beyond the
                  published corpus, 720 admissible values are enumerated and
                  required to produce 720 distinct encodings, 0 collisions and
                  720 literal round-trips.
  8  Falsifier.   EXECUTED, not declared.  The rejected set reading is
                  implemented and RUN.  PDD-01 and PDD-17 are required to be
                  554 bytes each, distinct under the adopted sequence reading,
                  and COLLIDING under the set reading on a value that is
                  required to be PDD-01's own published digest -- so a
                  set-reading implementation passes PDD-01 and mints PDD-01's id
                  for PDD-17.  IMPLEMENTATION-FREEZE 7.2.2's rider is that a
                  measurement that cannot fail the build is prose; a sibling
                  declared a control named EPC-V2 that occurs in no executable
                  and therefore never fires.  This one fires.
  9  Guards.      All 15 rejection controls are EXECUTED against constructed
                  inputs, and each must raise on the condition it NAMES, with
                  the exact message the artifact publishes, from BOTH encoders.
                  A non-zero exit is not evidence a guard fired; the reason is
                  compared.  All 6 decoder probes likewise.
 10  Rulings.     planStageIds is SEQUENCE and the three content orderRules are
                  quoted verbatim from LIVE v1.5.  The encoder REJECTS a
                  mis-ordered list rather than repairing it -- executed, per
                  list, against the named condition.  That refusal is what buys
                  LITERAL rather than quotient injectivity.
 11  Field set.   The fieldSetRule is applied to the LIVE v1.5 vectors and must
                  reproduce PDD-01..PDD-04's recordValue and all four
                  equivalence controls.  Rebuilt from v1.5, not read from v1.6.
 12  Separation.  Five (namespace, domain) pairs recomputed; five distinct
                  values; XD-5 reproduces PDD-01.  R-1's carried conformance
                  oracle prefix is taken from LIVE v1.5 and its first two bytes
                  (6f 70) are required to differ from this identity's outer
                  preimage bytes (30 31), so the two cannot share a preimage.
 13  Worked ex.   The complete CoreCompletion::completed carries a REAL
                  derivationDigest derived from the rule, not the 5555..
                  placeholder, and its remaining fields equal v1.5's POS-01.
 14  EP8.         The framing clauses are compared verbatim against LIVE
                  evaluation-proof.v8 bytes, its 44 grammar clauses are
                  enumerated mechanically and matched against the artifact's
                  classification in BOTH directions, and its nine-member domain
                  list is required to be unextended.
 15  Self-report. Every recorded measurement gets a hard comparison.

What this instrument does NOT verify is stated in full at NOT_VERIFIED below.
It is stated in the source rather than in a report because a limitation that
lives only in a report is not carried with the instrument.

Counts are bound to constants declared in THIS file, never sized from the
artifact.  IMPLEMENTATION-FREEZE 7.2.2's corollary, which defeated B-VER9R-01:
a partition sized from the artifact cannot police the artifact.

No repository Python checker is imported or executed.

Exit matrix, distinct by construction:
    0  clean run over the pinned subject
    1  findings
    2  bad invocation, integrity refusal, or pin drift
    3  selftest refused -- the base was not clean, so mutation results would be
       meaningless.  Freeze 7.2's EVIDENCE v8 row: a dead --selftest produced
       byte-identical output to a normal run.
    4  diagnostic run over UNPINNED bytes (--subject PATH).  Findings are
       printed; the exit code can never be mistaken for a verdict.

Invocation:
    python3 -I -B docs/coop/artifacts/check-r1-v1.6.py [--selftest]
    python3 -I -B docs/coop/artifacts/check-r1-v1.6.py --subject PATH
"""

from __future__ import annotations

import sys

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "R1V16-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-r1-v1.6.py`.  Caller-owned isolated startup is the prevention "
        "boundary; script code cannot undo interpreter or site activity that "
        "happened before line 1.\n")
    raise SystemExit(2)

import binascii
import copy
import hashlib
import itertools
import json
import pathlib
import struct
import unicodedata
from typing import Any, Callable

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent
REPO = COOP.parent.parent

SUBJECT = "r1-lifetime-neutrality.conformance.v1.6.json"

# ---------------------------------------------------------------------------
# Section 0.  Pinned execution closure.
#
# Paths are repository-relative so they read the same as the artifact's own
# frozenInputs rows, which are cross-compared against this table below.  Every
# one of these is hashed as inert bytes before anything is decoded.
# ---------------------------------------------------------------------------
PINS: dict[str, str] = {
    "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.6.json":
        "14c46b6582b573c1ac253d891e4813bcc436117adacaa5fc74ede0ab5ae23d3c",
    "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.5.json":
        "557b9f973c22b7ea959a884f56d5bac81c5383e227cac73a47605c1be317a815",
    "docs/coop/artifacts/evaluation-proof.v8.json":
        "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    "docs/coop/artifacts/c2-plan-stage-schema.v4.json":
        "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    # HASHED ONLY.  Never opened, never decoded, never parsed.  Pinned in this
    # table so that a change to it refuses the run rather than being noticed
    # later, and so that the value can be read out of this source.
    "docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md":
        "47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e",
    # Read as inert bytes only, to confirm v1.6's recorded read-only digest of
    # it.  NOT imported.  NOT executed.  NOT edited.  Freeze section 7.6.
    "docs/coop/artifacts/check-r1-v1.5.py":
        "79bd26785ab91c34e12a5f9cccc007a656d1598fea4c0e9f8674fd67114e6776",
}

SUBJECT_PATH = "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.6.json"
V15_PATH = "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.5.json"
EP8_PATH = "docs/coop/artifacts/evaluation-proof.v8.json"
C2V4_PATH = "docs/coop/artifacts/c2-plan-stage-schema.v4.json"
ARCH_PLAN_PATH = "docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md"
V15_CHECKER_PATH = "docs/coop/artifacts/check-r1-v1.5.py"

# The two coordinator-owned prose documents the artifact's own driftDisclosure
# names as having moved during its authoring, and which it states carry none of
# its arithmetic.  They are the ONLY rows permitted to differ from their pin.
# The permission is hard-coded here, not read from the artifact, and the
# artifact's disclosure is separately required to name exactly these two.
DECLARED_MOBILE = {
    "docs/coop/IMPLEMENTATION-FREEZE.md",
    "docs/coop/IMPLEMENTER-BLUEPRINT.md",
}

# ---------------------------------------------------------------------------
# Section 1.  Expectations bound OUTSIDE the artifact.
# ---------------------------------------------------------------------------
EXPECT_ARTIFACT = "opensip.r1-lifetime-neutrality.conformance"
EXPECT_VERSION = "v1.6"
EXPECT_STATUS = "CANDIDATE-NOT-APPLIED"
EXPECT_REVIEW_STATUS = "AWAITING-INDEPENDENT-REVIEW"
EXPECT_BINDS = "NOTHING"
EXPECT_SEAL = "DO-NOT-SEAL"
EXPECT_GRADE = "IMPLEMENTABLE_UNEXECUTED"

EXPECT_FROZEN_INPUTS = 17
EXPECT_CARRIED_KEYS = 20
EXPECT_CLOSED_TYPES = 25
EXPECT_POSITIVE_VECTORS = 10
EXPECT_ADVERSARIAL = 30
EXPECT_STATIC_FIXTURES = 9
EXPECT_V15_REVIEW_REQUESTS = 5
EXPECT_V15_RESIDUALS = 5

EXPECT_PINNED_VECTORS = 17
EXPECT_EQUIVALENCE = 4
EXPECT_SEPARATION = 5
EXPECT_REJECTIONS = 15
EXPECT_DECODER_PROBES = 6
EXPECT_ROUNDTRIP_RECORDS = 21
EXPECT_ENUMERATED_VALUES = 720
EXPECT_EP8_CLAUSES = 44
EXPECT_EP8_DOMAINS = 9
EXPECT_EP8_RECORD_TYPES = 11
EXPECT_COMPONENT_FRAME_OCCURRENCES = 50
EXPECT_MAX_TEXT_BYTES = 71
EXPECT_PLACEHOLDER_VALUES = 4
EXPECT_PLACEHOLDER_POSITIONS = 7
EXPECT_PROJECTION_EQUAL_DECLARERS = 4
EXPECT_C2V4_PINNED_FIXTURES = 7
EXPECT_SECTION_INT_LEAVES = 5

# The recipe, declared HERE.  The artifact's own statement of it is compared
# against this, not the other way round.
NAMESPACE = "opensip.r1-core.v1"
DOMAIN = "policy-derivation-v1"
TEXT_MAX_BYTES = 4096
RECORD_TAG = 0x80
OUTER_RECORD_TAG = 0x30
OUTER_NAMESPACE_TAG = 0x31
OUTER_DOMAIN_TAG = 0x32
OUTER_ROOT_TAG = 0x33
LEAF_TAG = 0x00

TEXT = "text"

# (name, tag, shape, presence).  Shape is TEXT, ("scalar-array", itemTag,
# scalarTag), ("record-array", itemTag, recordName) or ("record", recordName).
TOP_FIELDS: list[tuple[str, int, Any, str]] = [
    ("variant", 0x81, TEXT, "required"),
    ("observationSetKind", 0x82, TEXT, "required"),
    ("observationSetDigest", 0x83, TEXT, "required"),
    ("targetUniverseId", 0x84, TEXT, "required"),
    ("coverageContextKind", 0x85, TEXT, "required"),
    ("coverageContextDigest", 0x86, TEXT, "required"),
    ("planStageIds", 0x87, ("scalar-array", 0x88, 0x89), "required"),
    ("rules", 0x8a, ("record-array", 0x8b, "RuleValueV1"), "required"),
    ("policy", 0x8c, ("record", "PolicyValueV1"), "required"),
    ("findings", 0x8d, ("record-array", 0x8e, "FindingValueV1"), "required"),
    ("exactCoverage", 0x8f, ("record-array", 0x90, "CoverageEntryV1"), "required"),
    ("deficiency", 0x91, TEXT, "incomplete-only"),
]

NESTED: dict[str, tuple[int, list[tuple[str, int]]]] = {
    "RuleValueV1": (0xa0, [("ruleId", 0xa1), ("artifactDigest", 0xa2)]),
    "PolicyValueV1": (0xb0, [("policyId", 0xb1), ("artifactDigest", 0xb2)]),
    "FindingValueV1": (0xc0, [("ruleId", 0xc1), ("findingId", 0xc2),
                              ("valueDigest", 0xc3)]),
    "CoverageEntryV1": (0xd0, [("coverageKey", 0xd1), ("state", 0xd2)]),
}

TOP_FIELD_NAMES = [name for name, _, _, _ in TOP_FIELDS]
VARIANTS = ("completed", "incomplete")

# The three CONTENT-ordered lists and the sort key each R-1 orderRule names.
# planStageIds is deliberately absent: it is a SEQUENCE and its order is not a
# function of its content.
CONTENT_ORDERED: dict[str, tuple[str, ...]] = {
    "rules": ("ruleId",),
    "findings": ("ruleId", "findingId", "valueDigest"),
    "exactCoverage": ("coverageKey",),
}

# Quoted from LIVE v1.5 at the pointers named on the right and compared there.
V15_ORDER_RULES = {
    "planStageIds": ("caller-declared Plan stage order; preserve byte-for-byte",
                     ["closedTypes", "SealedStageInput", "fields",
                      "planStageIds", "orderRule"]),
    "rules": ("strict ascending UTF-8 byte order by ruleId",
              ["closedTypes", "RuleSet", "fields", "entries", "orderRule"]),
    "findings": ("strict ascending tuple of UTF-8 bytes "
                 "(ruleId, findingId, valueDigest)",
                 ["closedTypes", "FindingList", "orderRule"]),
    "exactCoverage": ("strict ascending UTF-8 byte order by coverageKey",
                      ["closedTypes", "ExactCoverage", "fields", "entries",
                       "orderRule"]),
}

# EP8 clauses this recipe transcribes, compared verbatim against live bytes.
EP8_VERBATIM = {
    ("canonicalCommitmentGrammar", "component"):
        "uint8(typeTag) || uint32be(len(utf8)) || utf8",
    ("canonicalCommitmentGrammar", "leaf"):
        "sha256(0x00 || uint64be(len(record)) || record)",
    ("canonicalCommitmentGrammar", "outer"):
        "sha256(0x30 || frameBlob(0x31,namespace) || frameBlob(0x32,domain) "
        "|| frameBlob(0x33,merkleRoot))",
    ("canonicalCommitmentGrammar", "oddNode"): "promote unchanged",
    ("canonicalCommitmentGrammar", "truncation"): "FORBIDDEN",
}

# The single declared carve-out in the mechanical clause enumeration: EP8's
# record-type table is a table of records, not a rule, and is counted once.
EP8_CLAUSE_AGGREGATES = {"normativePreimageGrammar.records"}

# The four v1.5 vectors PDD-01..PDD-04 model, and which completion object the
# migration table says the derived values are taken from.
V15_MODELLED = [
    ("PDD-01", "R1V15-POS-01-COMPLETED-NO-DIAGNOSTICS", "expectedCompletion"),
    ("PDD-02", "R1V15-POS-04-RULE-BUDGET-EXHAUSTION", "expectedCompletion"),
    ("PDD-03", "R1V15-POS-05-POLICY-BUDGET-EXHAUSTION", "expectedCompletion"),
    ("PDD-04", "R1V15-POS-06-INCOMPLETE-FACT-DEFICIENCY", "completionTemplate"),
]

# Positions inside $.policyDerivationIdentity where an exact JSON integer is
# the DECLARED type.  Everything else in that section must be an exact string.
SECTION_INT_LEAVES = {
    "$.policyDerivationIdentity.workedExample.completion.diagnostics.droppedCount",
    "$.policyDerivationIdentity.workedExample.completion.budgetUsage.ruleUnits",
    "$.policyDerivationIdentity.workedExample.completion.budgetUsage.policyUnits",
    "$.policyDerivationIdentity.workedExample.completion.budgetUsage"
    ".diagnosticRecordsAccepted",
    "$.policyDerivationIdentity.workedExample.completion.budgetUsage"
    ".diagnosticRecordsDropped",
}

NOT_VERIFIED = [
    "evaluation-proof.v8's 69-assertion framing gate (12 record goldens and 9 "
    "commitment goldens re-encoded by a generic EP8-driven re-encoder).  This "
    "instrument verifies that the framing CLAUSES it transcribes read verbatim "
    "in live EP8 bytes and that the recipe reproduces every digest R-1 "
    "publishes; it does not re-run EP8's own goldens.",
    "measuredSelfReport.shasumCrossCheck -- 47 raw byte strings hashed by "
    "shasum(1) outside Python.  A stdlib-only instrument with no ambient "
    "authority cannot spawn a process, and doing so would be the very reach "
    "staticAndRuntimeClosure.forbiddenReach denies.  Its recorded shape is "
    "compared; its execution is not reproduced.",
    "encoderAgreement.comparisons == 180.  Two independent encoders ARE run "
    "here and compared on every record, but the artifact's tally counts its own "
    "two encoders over its own worklist; this instrument reports its own count "
    "rather than asserting a number it did not produce.",
    "Every prose rationale: whyThisIsARuleAndNotAList, the narrowing arguments, "
    "the proposal evaluation and the strongestObjections rows.  They are "
    "arguments, not measurements, and no instrument can grade them.",
    "Whether the field set is the RIGHT one.  v1.6 states plainly that nothing "
    "forces its inclusions and that it RULES them as the owning surface.  This "
    "instrument measures that the ruling is applied consistently and is "
    "vector-addressable; it cannot measure that it is correct.",
]


# ---------------------------------------------------------------------------
# Section 2.  Strict parsing.  Freeze section 7.5: json.loads without a hook
# keeps the LAST of duplicate keys, so a document can say one thing to a reader
# and another to every instrument.  Section 7.5 found 6 of 47 rejecting
# checkers that never say WHICH key duplicated, so this one names it.
# ---------------------------------------------------------------------------
class PinRefusal(RuntimeError):
    pass


class StrictJsonError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise StrictJsonError(
                "R1V16-JSON-DUPLICATE",
                f"duplicate object key {key!r}")
        out[key] = value
    return out


def _reject_float(token: str) -> Any:
    raise StrictJsonError("R1V16-JSON-FLOAT", f"JSON float forbidden: {token}")


def _reject_constant(token: str) -> Any:
    raise StrictJsonError("R1V16-JSON-NONFINITE",
                          f"non-finite forbidden: {token}")


def strict_loads(text: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_pairs,
                          parse_float=_reject_float,
                          parse_constant=_reject_constant)
    except StrictJsonError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise StrictJsonError("R1V16-JSON-SYNTAX", str(exc)) from exc


def strict_parse(raw: bytes, name: str) -> Any:
    try:
        return strict_loads(raw.decode("utf-8"))
    except UnicodeError as exc:
        raise PinRefusal(f"{name}: {type(exc).__name__}: {exc}") from exc
    except StrictJsonError as exc:
        raise PinRefusal(f"{name}: {exc.code}: {exc}") from exc


def lenient_parse(raw: bytes, name: str) -> Any:
    """For a pinned neighbour whose own wire legitimately carries decimals.

    Bytes are authenticated first.  Duplicate names and non-finite values still
    reject, and the duplicated key is still named.
    """
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_constant=_reject_constant)
    except StrictJsonError as exc:
        raise PinRefusal(f"{name}: {exc.code}: {exc}") from exc
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PinRefusal(f"{name}: {type(exc).__name__}: {exc}") from exc


def verified_snapshots() -> dict[str, bytes]:
    """Read every pinned input as inert bytes and verify BEFORE anything runs."""
    snaps: dict[str, bytes] = {}
    errors: list[str] = []
    for rel, expected in PINS.items():
        try:
            data = (REPO / rel).read_bytes()
        except OSError as exc:
            errors.append(f"{rel}: read {type(exc).__name__}")
            continue
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            errors.append(f"{rel}: {actual} != {expected}")
            continue
        snaps[rel] = data
    if errors:
        raise PinRefusal("; ".join(sorted(errors)))
    if set(snaps) != set(PINS):
        raise PinRefusal("not every pinned input produced a snapshot")
    return snaps


# ---------------------------------------------------------------------------
# Section 3.  Findings.  Every one names its JSON position.  Freeze 7.4: a
# non-zero exit is not evidence a guard fired, so the reason travels with it.
# ---------------------------------------------------------------------------
def _add(findings: list[str], code: str, where: str, detail: str) -> None:
    findings.append(f"{code} {where}: {detail}")


def _codes(findings: list[str]) -> set[str]:
    return {item.split(" ", 1)[0] for item in findings}


def _get(node: Any, path: list[Any], default: Any = None) -> Any:
    cur = node
    for key in path:
        if isinstance(cur, dict) and isinstance(key, str) and key in cur:
            cur = cur[key]
        elif isinstance(cur, list) and isinstance(key, int) and -len(cur) <= key < len(cur):
            cur = cur[key]
        else:
            return default
    return cur


def canon(value: Any) -> bytes:
    """Canonical bytes.  json.dumps(True) is 'true' and json.dumps(1) is '1',
    so equality here is law-18 aware in a way Python's `==` is not."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


JSON_TYPE_NAMES = {"str": "string", "int": "integer", "bool": "boolean",
                   "float": "number", "NoneType": "null", "list": "array",
                   "dict": "object"}


def json_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    name = type(value).__name__
    return JSON_TYPE_NAMES.get(name, name)


def _eq(findings: list[str], code: str, where: str, actual: Any,
        expected: Any) -> bool:
    if (not isinstance(actual, type(expected))
            or isinstance(actual, bool) != isinstance(expected, bool)):
        _add(findings, code, where,
             f"declared {json_type(expected)}, found {json_type(actual)}; the "
             f"JSON type is compared before the content")
        return False
    if actual != expected:
        _add(findings, code, where, f"expected {expected!r}; got {actual!r}")
        return False
    return True


# ---------------------------------------------------------------------------
# Section 4.  Encoder A -- table-driven.
#
# One declarative grammar table walked recursively; struct.pack for big-endian;
# bytes.hex for output.  Exception messages are the artifact's published
# encoderA strings, byte for byte, so a recorded measurement gets a hard
# comparison rather than a family resemblance.
# ---------------------------------------------------------------------------
def a_text(value: Any) -> bytes:
    # Law 18 FIRST.  A bool is a subclass of int in Python and an int is not a
    # string in JSON; the type is refused before any content rule is reached.
    if not isinstance(value, str):
        raise TypeError(f"text component must be a JSON string, got {type(value)}")
    if value == "":
        raise ValueError("text component is empty (EP8: non-empty)")
    if value.startswith("\ufeff"):
        raise ValueError("text component carries a BOM")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"text component is not NFC: {value!r}")
    for ch in value:
        point = ord(ch)
        if point <= 0x1F or point == 0x7F:
            raise ValueError(f"text component carries U+{point:04X}")
    raw = value.encode("utf-8")
    if len(raw) > TEXT_MAX_BYTES:
        raise ValueError(
            f"text component exceeds {TEXT_MAX_BYTES} bytes ({len(raw)})")
    return raw


def a_frame(tag: int, payload: bytes) -> bytes:
    return struct.pack(">B", tag) + struct.pack(">I", len(payload)) + payload


def a_component(tag: int, value: Any) -> bytes:
    return a_frame(tag, a_text(value))


def a_nested(name: str, value: Any) -> bytes:
    record_tag, fields = NESTED[name]
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a JSON object, got {type(value)}")
    declared = [field for field, _ in fields]
    extra = sorted(set(value) - set(declared))
    if extra:
        raise ValueError(f"undeclared field(s) {extra} in {name}")
    missing = [field for field in declared if field not in value]
    if missing:
        raise ValueError(f"missing required field(s) {missing} in {name}")
    out = struct.pack(">B", record_tag)
    for field, tag in fields:
        out += a_component(tag, value[field])
    return out


def _sort_key(item: Any, keys: tuple[str, ...], name: str) -> tuple[bytes, ...]:
    parts = []
    for key in keys:
        value = item[key]
        if not isinstance(value, str):
            raise TypeError(f"text component must be a JSON string, got {type(value)}")
        parts.append(value.encode("utf-8"))
    return tuple(parts)


def a_order_gate(name: str, items: list[Any]) -> None:
    """R-1's own strict-ascending orderRule, RE-CHECKED at the encoder.

    The list is REFUSED, never repaired.  Repairing would make the encoder
    many-to-one and would cost the LITERAL round-trip that injectivity is
    argued from -- the exact retreat plan-and-policy-identity-recipes.v2 had to
    make after B-PPIR-01.
    """
    keys = CONTENT_ORDERED[name]
    previous: tuple[bytes, ...] | None = None
    for index, item in enumerate(items):
        current = _sort_key(item, keys, name)
        if previous is not None and not previous < current:
            raise ValueError(
                f"{name} violates R-1's strict-ascending orderRule at index "
                f"{index}")
        previous = current


def encode_a(value: Any, *, set_reading: frozenset[str] = frozenset()) -> bytes:
    """The adopted recipe.  `set_reading` implements the REJECTED reading for
    the named lists and exists only so the falsifier can be EXECUTED."""
    if not isinstance(value, dict):
        raise TypeError(
            f"PolicyDerivationInputV1 must be a JSON object, got {type(value)}")
    extra = sorted(set(value) - set(TOP_FIELD_NAMES))
    if extra:
        raise ValueError(
            f"undeclared field(s) {extra} in PolicyDerivationInputV1")

    variant = value.get("variant")
    if not isinstance(variant, str):
        raise TypeError(f"text component must be a JSON string, got {type(variant)}")
    if variant not in VARIANTS:
        raise ValueError(
            f"variant must be completed|incomplete, got {variant!r}")
    if variant == "completed" and "deficiency" in value:
        raise ValueError("variant=completed FORBIDS deficiency")
    if variant == "incomplete" and "deficiency" not in value:
        raise ValueError("variant=incomplete REQUIRES deficiency")

    out = struct.pack(">B", RECORD_TAG)
    for name, tag, shape, presence in TOP_FIELDS:
        if presence == "incomplete-only" and variant != "incomplete":
            continue
        if name not in value:
            raise ValueError(
                f"missing required field {name} in PolicyDerivationInputV1")
        item = value[name]
        if shape is TEXT:
            out += a_component(tag, item)
            continue
        if shape[0] == "record":
            out += a_frame(tag, a_nested(shape[1], item))
            continue
        if not isinstance(item, list):
            raise TypeError(f"{name} must be a JSON array, got {type(item)}")
        if shape[0] == "scalar-array":
            _, item_tag, scalar_tag = shape
            seen: list[str] = []
            for member in item:
                if not isinstance(member, str):
                    raise TypeError(
                        f"text component must be a JSON string, got {type(member)}")
                if member in seen:
                    raise ValueError(
                        f"duplicate logical list member in {name}")
                seen.append(member)
            frames = [a_frame(item_tag, a_component(scalar_tag, member))
                      for member in item]
        else:
            _, item_tag, record_name = shape
            for member in item:
                if not isinstance(member, dict):
                    raise TypeError(
                        f"{record_name} must be a JSON object, got {type(member)}")
            # Under the REJECTED reading the sort REPLACES the order gate --
            # that is precisely what makes it many-to-one -- so the gate is
            # bypassed for a list the caller has named.  The adopted path
            # always runs it.
            if name not in set_reading:
                a_order_gate(name, item)
            frames = [a_frame(item_tag, a_nested(record_name, member))
                      for member in item]
        if name in set_reading:
            frames = sorted(frames)
        out += a_frame(tag, b"".join(frames))
    return out


def a_leaf_root(record: bytes) -> bytes:
    return hashlib.sha256(
        struct.pack(">B", LEAF_TAG) + struct.pack(">Q", len(record)) + record
    ).digest()


def a_outer(root: bytes, namespace: str = NAMESPACE,
            domain: str = DOMAIN) -> bytes:
    return (struct.pack(">B", OUTER_RECORD_TAG)
            + a_component(OUTER_NAMESPACE_TAG, namespace)
            + a_component(OUTER_DOMAIN_TAG, domain)
            + a_frame(OUTER_ROOT_TAG, root))


def a_derivation_digest(record: bytes, namespace: str = NAMESPACE,
                        domain: str = DOMAIN) -> str:
    preimage = a_outer(a_leaf_root(record), namespace, domain)
    return "sha256:" + hashlib.sha256(preimage).hexdigest()


# ---------------------------------------------------------------------------
# Section 5.  Encoder B -- flat imperative.
#
# One function per record type, every tag written out at its site, big-endian
# hand-rolled by shift-and-mask, bytearray accumulation, binascii for hex.
# Shares NO code and NO helper with encoder A, including its text validator.
# Freeze 7.1: a sibling sweep "used no second encoder, so it does not meet the
# two-encoder standard this corpus set for itself".
# ---------------------------------------------------------------------------
def b_u32(number: int) -> bytes:
    return bytes([(number >> 24) & 0xFF, (number >> 16) & 0xFF,
                  (number >> 8) & 0xFF, number & 0xFF])


def b_u64(number: int) -> bytes:
    return bytes([(number >> shift) & 0xFF
                  for shift in (56, 48, 40, 32, 24, 16, 8, 0)])


def b_txt(value: Any) -> bytes:
    if isinstance(value, bool) or not isinstance(value, str):
        raise TypeError("not a string")
    if len(value) == 0:
        raise ValueError("empty text")
    if value[:1] == "\ufeff":
        raise ValueError("BOM")
    if value != unicodedata.normalize("NFC", value):
        raise ValueError("not NFC")
    index = 0
    while index < len(value):
        code = ord(value[index])
        if code < 0x20 or code == 0x7F:
            raise ValueError("forbidden control code point")
        index += 1
    encoded = value.encode("utf-8")
    if len(encoded) > 4096:
        raise ValueError("over 4096 bytes")
    return encoded


def b_c(tag: int, value: Any) -> bytearray:
    body = b_txt(value)
    buf = bytearray()
    buf.append(tag)
    buf += b_u32(len(body))
    buf += body
    return buf


def b_blob(tag: int, body: bytes) -> bytearray:
    buf = bytearray()
    buf.append(tag)
    buf += b_u32(len(body))
    buf += body
    return buf


def b_rule(entry: Any) -> bytearray:
    if not isinstance(entry, dict):
        raise TypeError("not an object")
    for key in entry:
        if key not in ("ruleId", "artifactDigest"):
            raise ValueError("undeclared field " + key)
    buf = bytearray()
    buf.append(0xA0)
    buf += b_c(0xA1, entry["ruleId"])
    buf += b_c(0xA2, entry["artifactDigest"])
    return buf


def b_policy(entry: Any) -> bytearray:
    if not isinstance(entry, dict):
        raise TypeError("not an object")
    for key in entry:
        if key not in ("policyId", "artifactDigest"):
            raise ValueError("undeclared field " + key)
    buf = bytearray()
    buf.append(0xB0)
    buf += b_c(0xB1, entry["policyId"])
    buf += b_c(0xB2, entry["artifactDigest"])
    return buf


def b_finding(entry: Any) -> bytearray:
    if not isinstance(entry, dict):
        raise TypeError("not an object")
    for key in entry:
        if key not in ("ruleId", "findingId", "valueDigest"):
            raise ValueError("undeclared field " + key)
    buf = bytearray()
    buf.append(0xC0)
    buf += b_c(0xC1, entry["ruleId"])
    buf += b_c(0xC2, entry["findingId"])
    buf += b_c(0xC3, entry["valueDigest"])
    return buf


def b_coverage(entry: Any) -> bytearray:
    if not isinstance(entry, dict):
        raise TypeError("not an object")
    for key in entry:
        if key not in ("coverageKey", "state"):
            raise ValueError("undeclared field " + key)
    buf = bytearray()
    buf.append(0xD0)
    buf += b_c(0xD1, entry["coverageKey"])
    buf += b_c(0xD2, entry["state"])
    return buf


def b_ascending(items: list[Any], keys: list[str], label: str) -> None:
    index = 1
    while index < len(items):
        left = []
        right = []
        for key in keys:
            lv = items[index - 1][key]
            rv = items[index][key]
            if isinstance(lv, bool) or not isinstance(lv, str):
                raise TypeError("not a string")
            if isinstance(rv, bool) or not isinstance(rv, str):
                raise TypeError("not a string")
            left.append(lv.encode("utf-8"))
            right.append(rv.encode("utf-8"))
        if not tuple(left) < tuple(right):
            raise ValueError(label + " not strictly ascending")
        index += 1


def encode_b(value: Any, sorted_lists: tuple[str, ...] = ()) -> bytes:
    if not isinstance(value, dict):
        raise TypeError("not an object")
    known = ("variant", "observationSetKind", "observationSetDigest",
             "targetUniverseId", "coverageContextKind", "coverageContextDigest",
             "planStageIds", "rules", "policy", "findings", "exactCoverage",
             "deficiency")
    for key in value:
        if key not in known:
            raise ValueError("undeclared field " + key)
    variant = value.get("variant")
    if isinstance(variant, bool) or not isinstance(variant, str):
        raise TypeError("not a string")
    if variant != "completed" and variant != "incomplete":
        raise ValueError("bad variant")
    if variant == "completed" and "deficiency" in value:
        raise ValueError("completed forbids deficiency")
    if variant == "incomplete" and "deficiency" not in value:
        raise ValueError("incomplete requires deficiency")
    for key in ("observationSetKind", "observationSetDigest", "targetUniverseId",
                "coverageContextKind", "coverageContextDigest", "planStageIds",
                "rules", "policy", "findings", "exactCoverage"):
        if key not in value:
            raise ValueError("missing field " + key)

    buf = bytearray()
    buf.append(0x80)
    buf += b_c(0x81, value["variant"])
    buf += b_c(0x82, value["observationSetKind"])
    buf += b_c(0x83, value["observationSetDigest"])
    buf += b_c(0x84, value["targetUniverseId"])
    buf += b_c(0x85, value["coverageContextKind"])
    buf += b_c(0x86, value["coverageContextDigest"])

    stages = value["planStageIds"]
    if not isinstance(stages, list):
        raise TypeError("not an array")
    position = 0
    while position < len(stages):
        other = 0
        while other < position:
            if stages[other] == stages[position]:
                raise ValueError("duplicate planStageIds member")
            other += 1
        position += 1
    stage_frames = [bytes(b_blob(0x88, bytes(b_c(0x89, s)))) for s in stages]
    if "planStageIds" in sorted_lists:
        stage_frames = sorted(stage_frames)
    buf += b_blob(0x87, b"".join(stage_frames))

    rules = value["rules"]
    if not isinstance(rules, list):
        raise TypeError("not an array")
    for entry in rules:
        if not isinstance(entry, dict):
            raise TypeError("not an object")
    b_ascending(rules, ["ruleId"], "rules")
    rule_frames = [bytes(b_blob(0x8B, bytes(b_rule(r)))) for r in rules]
    if "rules" in sorted_lists:
        rule_frames = sorted(rule_frames)
    buf += b_blob(0x8A, b"".join(rule_frames))

    buf += b_blob(0x8C, bytes(b_policy(value["policy"])))

    findings = value["findings"]
    if not isinstance(findings, list):
        raise TypeError("not an array")
    for entry in findings:
        if not isinstance(entry, dict):
            raise TypeError("not an object")
    b_ascending(findings, ["ruleId", "findingId", "valueDigest"], "findings")
    finding_frames = [bytes(b_blob(0x8E, bytes(b_finding(f)))) for f in findings]
    if "findings" in sorted_lists:
        finding_frames = sorted(finding_frames)
    buf += b_blob(0x8D, b"".join(finding_frames))

    coverage = value["exactCoverage"]
    if not isinstance(coverage, list):
        raise TypeError("not an array")
    for entry in coverage:
        if not isinstance(entry, dict):
            raise TypeError("not an object")
    b_ascending(coverage, ["coverageKey"], "exactCoverage")
    coverage_frames = [bytes(b_blob(0x90, bytes(b_coverage(c))))
                       for c in coverage]
    if "exactCoverage" in sorted_lists:
        coverage_frames = sorted(coverage_frames)
    buf += b_blob(0x8F, b"".join(coverage_frames))

    if variant == "incomplete":
        buf += b_c(0x91, value["deficiency"])
    return bytes(buf)


def b_digest(record: bytes, namespace: str = NAMESPACE,
             domain: str = DOMAIN) -> str:
    leaf = bytearray()
    leaf.append(0x00)
    leaf += b_u64(len(record))
    leaf += record
    root = hashlib.sha256(bytes(leaf)).digest()
    outer = bytearray()
    outer.append(0x30)
    outer += b_c(0x31, namespace)
    outer += b_c(0x32, domain)
    outer += b_blob(0x33, root)
    return "sha256:" + binascii.hexlify(
        hashlib.sha256(bytes(outer)).digest()).decode("ascii")


def b_hex(raw: bytes) -> str:
    return binascii.hexlify(raw).decode("ascii")


# ---------------------------------------------------------------------------
# Section 6.  The TOTAL decoder.
#
# Grammar-directed recursive descent: it walks the DECLARED field list and asks
# the bytes whether the next frame is the field it wants.  It returns exactly
# one value or raises.  It enforces the record tag, declared tag order,
# at-most-once per field, exact frame lengths with no trailing bytes, the text
# admission rule on every scalar, and the variant/deficiency rule.
# ---------------------------------------------------------------------------
def d_frame(buf: bytes, offset: int) -> tuple[int, bytes, int]:
    if offset + 5 > len(buf):
        raise ValueError("truncated frame header")
    tag = buf[offset]
    length = int.from_bytes(buf[offset + 1:offset + 5], "big")
    end = offset + 5 + length
    if end > len(buf):
        raise ValueError("frame length exceeds buffer")
    return tag, buf[offset + 5:end], end


def d_peek_tag(buf: bytes, offset: int) -> int | None:
    if offset >= len(buf):
        return None
    if offset + 5 > len(buf):
        raise ValueError("truncated frame header")
    return buf[offset]


def d_text(payload: bytes) -> str:
    try:
        value = payload.decode("utf-8")
    except UnicodeError as exc:
        raise ValueError("text component is not UTF-8") from exc
    if value == "":
        raise ValueError("text component is empty (EP8: non-empty)")
    if value.startswith("\ufeff"):
        raise ValueError("text component carries a BOM")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"text component is not NFC: {value!r}")
    for ch in value:
        point = ord(ch)
        if point <= 0x1F or point == 0x7F:
            raise ValueError(f"text component carries U+{point:04X}")
    if len(payload) > TEXT_MAX_BYTES:
        raise ValueError(
            f"text component exceeds {TEXT_MAX_BYTES} bytes ({len(payload)})")
    return value


def d_nested(name: str, payload: bytes) -> dict[str, str]:
    record_tag, fields = NESTED[name]
    if not payload or payload[0] != record_tag:
        raise ValueError(f"bad record tag for {name}")
    offset = 1
    out: dict[str, str] = {}
    for field, tag in fields:
        got = d_peek_tag(payload, offset)
        if got != tag:
            raise ValueError(f"missing required field {field}")
        _, body, offset = d_frame(payload, offset)
        out[field] = d_text(body)
    if offset != len(payload):
        tag = d_peek_tag(payload, offset)
        raise ValueError(f"undeclared or out-of-order tag 0x{tag:02x}")
    return out


def decode(buf: bytes) -> dict[str, Any]:
    if not buf or buf[0] != RECORD_TAG:
        raise ValueError("bad record tag for PolicyDerivationInputV1")
    offset = 1
    out: dict[str, Any] = {}
    for name, tag, shape, presence in TOP_FIELDS:
        got = d_peek_tag(buf, offset)
        if got != tag:
            if presence == "incomplete-only":
                continue
            raise ValueError(f"missing required field {name}")
        _, payload, offset = d_frame(buf, offset)
        if shape is TEXT:
            out[name] = d_text(payload)
        elif shape[0] == "record":
            out[name] = d_nested(shape[1], payload)
        elif shape[0] == "scalar-array":
            _, item_tag, scalar_tag = shape
            members: list[str] = []
            inner = 0
            while inner < len(payload):
                item_got, item_body, inner = d_frame(payload, inner)
                if item_got != item_tag:
                    raise ValueError(
                        f"undeclared or out-of-order tag 0x{item_got:02x}")
                scalar_got, scalar_body, scalar_end = d_frame(item_body, 0)
                if scalar_got != scalar_tag:
                    raise ValueError(
                        f"undeclared or out-of-order tag 0x{scalar_got:02x}")
                if scalar_end != len(item_body):
                    raise ValueError("trailing bytes inside list item frame")
                member = d_text(scalar_body)
                if member in members:
                    raise ValueError(
                        f"duplicate logical list member in {name}")
                members.append(member)
            out[name] = members
        else:
            _, item_tag, record_name = shape
            entries: list[dict[str, str]] = []
            inner = 0
            while inner < len(payload):
                item_got, item_body, inner = d_frame(payload, inner)
                if item_got != item_tag:
                    raise ValueError(
                        f"undeclared or out-of-order tag 0x{item_got:02x}")
                entries.append(d_nested(record_name, item_body))
            out[name] = entries
    if offset != len(buf):
        tag = d_peek_tag(buf, offset)
        raise ValueError(f"undeclared or out-of-order tag 0x{tag:02x}")
    variant = out.get("variant")
    if variant not in VARIANTS:
        raise ValueError(
            f"variant must be completed|incomplete, got {variant!r}")
    if variant == "completed" and "deficiency" in out:
        raise ValueError("variant=completed FORBIDS deficiency")
    if variant == "incomplete" and "deficiency" not in out:
        raise ValueError("variant=incomplete REQUIRES deficiency")
    # The decoder deliberately does NOT re-apply R-1's content orderRules.
    # decoderTotality declares its contract exactly -- record tag, declared tag
    # order, at-most-once per field, exact frame lengths with no trailing
    # bytes, the text admission rule on every scalar, and the variant rule --
    # and adding a gate here would make the decoder refuse the rejected-reading
    # exhibit records it must be TOTAL on.  Admission is the encoder's job.
    return out


# ---------------------------------------------------------------------------
# Section 7.  v1.5 vector resolution and the fieldSetRule, applied to the LIVE
# predecessor bytes rather than to v1.6's copy of them.
# ---------------------------------------------------------------------------
def _set_dotted(node: dict[str, Any], dotted: str, value: Any) -> bool:
    parts = dotted.split(".")
    cur: Any = node
    for part in parts[:-1]:
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    if not isinstance(cur, dict) or parts[-1] not in cur:
        return False
    cur[parts[-1]] = value
    return True


def resolve_v15(v15: dict[str, Any], vector_id: str,
                seen: tuple[str, ...] = ()) -> dict[str, Any] | None:
    if vector_id in seen:
        return None
    table = {v["id"]: v for v in v15["positiveVectors"]
             if isinstance(v, dict) and isinstance(v.get("id"), str)}
    vector = table.get(vector_id)
    if vector is None:
        return None
    if "cloneOf" in vector:
        base = resolve_v15(v15, vector["cloneOf"], seen + (vector_id,))
        if base is None:
            return None
        base = copy.deepcopy(base)
    else:
        base = {
            "stageInput": copy.deepcopy(vector.get("stageInput")),
            "deps": copy.deepcopy(vector.get("deps")),
            "attempt": copy.deepcopy(vector.get("attempt")),
        }
    for dotted, value in (vector.get("overrides") or {}).items():
        if not _set_dotted(base, dotted, value):
            return None
    return base


def field_set_record(resolved: dict[str, Any],
                     completion: dict[str, Any]) -> dict[str, Any] | None:
    """PolicyDerivationInputV1 = (0) the variant, then (I) every leaf of the
    closed argument domain minus the declared evidence-neutral subtrees, then
    (D) projectionByVariant[variant] minus variant and minus policyOutcome."""
    stage = _get(resolved, ["stageInput"])
    deps = _get(resolved, ["deps"])
    if not isinstance(stage, dict) or not isinstance(deps, dict):
        return None
    variant = completion.get("variant")
    findings = completion.get("findings")
    if findings is None:
        findings = completion.get("partialFindings")
    out = {
        "variant": variant,
        "observationSetKind": _get(stage, ["observationSet", "kind"]),
        "observationSetDigest": _get(stage, ["observationSet", "digest"]),
        "targetUniverseId": _get(stage, ["targetUniverseId"]),
        "coverageContextKind": _get(stage, ["coverageContext", "kind"]),
        "coverageContextDigest": _get(stage, ["coverageContext", "digest"]),
        "planStageIds": _get(stage, ["planStageIds"]),
        "rules": _get(deps, ["rules", "entries"]),
        "policy": _get(deps, ["policy"]),
        "findings": findings,
        "exactCoverage": _get(completion, ["exactCoverage", "entries"]),
    }
    if variant == "incomplete":
        out["deficiency"] = completion.get("deficiency")
    if any(value is None for value in out.values()):
        return None
    return out


# ---------------------------------------------------------------------------
# Section 8.  Checks.
# ---------------------------------------------------------------------------
def check_posture(doc: Any, findings: list[str]) -> None:
    _eq(findings, "R1V16-POSTURE", "$.artifact", doc.get("artifact"),
        EXPECT_ARTIFACT)
    _eq(findings, "R1V16-POSTURE", "$.version", doc.get("version"),
        EXPECT_VERSION)
    _eq(findings, "R1V16-POSTURE", "$.status", doc.get("status"), EXPECT_STATUS)
    _eq(findings, "R1V16-POSTURE", "$.reviewStatus", doc.get("reviewStatus"),
        EXPECT_REVIEW_STATUS)
    _eq(findings, "R1V16-POSTURE", "$.binds", doc.get("binds"), EXPECT_BINDS)
    _eq(findings, "R1V16-POSTURE", "$.sealRecommendation",
        doc.get("sealRecommendation"), EXPECT_SEAL)
    _eq(findings, "R1V16-POSTURE", "$.evidenceGrade", doc.get("evidenceGrade"),
        EXPECT_GRADE)
    _eq(findings, "R1V16-POSTURE", "$.supersedesIfAccepted",
        doc.get("supersedesIfAccepted"), V15_PATH)
    for pointer, value in _iter_leaves(doc, "$"):
        if isinstance(value, str) and value.strip() == "[UNSET]":
            _add(findings, "R1V16-POSTURE", pointer,
                 "a placeholder verdict token survived into the emitted bytes")


def check_frozen_inputs(doc: Any, findings: list[str]) -> None:
    rows = doc.get("frozenInputs")
    if not isinstance(rows, list):
        _add(findings, "R1V16-PIN", "$.frozenInputs",
             f"declared array, found {json_type(rows)}")
        return
    if len(rows) != EXPECT_FROZEN_INPUTS:
        _add(findings, "R1V16-PIN", "$.frozenInputs",
             f"expected {EXPECT_FROZEN_INPUTS} rows, found {len(rows)}")
    seen_paths: set[str] = set()
    drifted: set[str] = set()
    for index, row in enumerate(rows):
        where = f"$.frozenInputs[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V16-PIN", where,
                 f"declared object, found {json_type(row)}")
            continue
        path = row.get("path")
        digest = row.get("sha256")
        for name, value in (("path", path), ("sha256", digest),
                            ("id", row.get("id")), ("role", row.get("role"))):
            if not isinstance(value, str):
                _add(findings, "R1V16-TYPE", f"{where}.{name}",
                     f"declared string, found {json_type(value)}")
        if not isinstance(path, str) or not isinstance(digest, str):
            continue
        if path in seen_paths:
            _add(findings, "R1V16-PIN", where, f"duplicate path {path!r}")
        seen_paths.add(path)
        target = pathlib.Path(path)
        target = target if target.is_absolute() else REPO / target
        try:
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
        except OSError as exc:
            _add(findings, "R1V16-PIN", f"{where}.path",
                 f"{path}: unreadable ({type(exc).__name__})")
            continue
        if actual == digest:
            continue
        drifted.add(path)
        if path not in DECLARED_MOBILE:
            _add(findings, "R1V16-PIN", f"{where}.sha256",
                 f"{path}: live {actual} != recorded {digest}; this row is not "
                 f"one of the two coordinator-owned documents the artifact "
                 f"declares mobile")
    # The declared-mobile permission is hard-coded above.  Require the
    # artifact's own disclosure to name exactly those two documents, so the
    # permission cannot be widened from the artifact side.
    disclosure = _get(doc, ["measuredSelfReport", "driftDisclosure",
                            "twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING"])
    if not isinstance(disclosure, str):
        _add(findings, "R1V16-TYPE",
             "$.measuredSelfReport.driftDisclosure"
             ".twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING",
             f"declared string, found {json_type(disclosure)}")
    else:
        for path in sorted(DECLARED_MOBILE):
            if path.rsplit("/", 1)[-1] not in disclosure:
                _add(findings, "R1V16-PIN",
                     "$.measuredSelfReport.driftDisclosure"
                     ".twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING",
                     f"the disclosure does not name {path}, which this "
                     f"instrument permits to move")
        for path in sorted(seen_paths - DECLARED_MOBILE):
            name = path.rsplit("/", 1)[-1]
            if name in disclosure and path.endswith(".md"):
                _add(findings, "R1V16-PIN",
                     "$.measuredSelfReport.driftDisclosure"
                     ".twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING",
                     f"the disclosure names {path}, which is not declared "
                     f"mobile by this instrument")
    # Cross-table: this checker's own PINS must agree with the artifact's rows.
    declared = {row["path"]: row["sha256"] for row in rows
                if isinstance(row, dict) and isinstance(row.get("path"), str)
                and isinstance(row.get("sha256"), str)}
    for rel, expected in PINS.items():
        if rel == SUBJECT_PATH:
            continue
        if rel not in declared:
            _add(findings, "R1V16-PIN", "$.frozenInputs",
                 f"this checker pins {rel} but the artifact records no row "
                 f"for it")
        elif declared[rel] != expected:
            _add(findings, "R1V16-PIN", "$.frozenInputs",
                 f"{rel}: artifact records {declared[rel]}, this checker pins "
                 f"{expected}")
    # Every drifted row outside DECLARED_MOBILE was reported at its own
    # position above.  The permitted drift is not a finding, but it is not
    # silence either: it is printed in the banner by declared_mobile_drift().
    del drifted


def declared_mobile_drift(doc: Any) -> list[str]:
    """The permitted drift, measured and REPORTED rather than absorbed.

    Freeze 7.2.1 rule 4: drift is a fact about the conditions and is recorded,
    not silently re-baselined.  These rows are not findings -- the artifact
    declares them mobile and states no published digest depends on them, and
    this instrument never reads either document -- but they are printed.
    """
    out: list[str] = []
    rows = doc.get("frozenInputs") if isinstance(doc, dict) else None
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        path, digest = row.get("path"), row.get("sha256")
        if path not in DECLARED_MOBILE or not isinstance(digest, str):
            continue
        try:
            actual = hashlib.sha256((REPO / path).read_bytes()).hexdigest()
        except OSError:
            continue
        if actual != digest:
            out.append(f"{path}: recorded {digest}, live {actual}")
    return out


def check_predecessor(doc: Any, findings: list[str]) -> None:
    _eq(findings, "R1V16-PREDECESSOR", "$.predecessor.path",
        _get(doc, ["predecessor", "path"]), V15_PATH)
    _eq(findings, "R1V16-PREDECESSOR", "$.predecessor.sha256",
        _get(doc, ["predecessor", "sha256"]), PINS[V15_PATH])
    report = doc.get("measuredSelfReport")
    if not isinstance(report, dict):
        _add(findings, "R1V16-TYPE", "$.measuredSelfReport",
             f"declared object, found {json_type(report)}")
        return
    for key, expected in (
            ("predecessorSha256AtStartOfAuthoring", PINS[V15_PATH]),
            ("predecessorSha256AtEmit", PINS[V15_PATH]),
            ("archPlanSha256AtStartOfAuthoring", PINS[ARCH_PLAN_PATH]),
            ("archPlanSha256AtEmit", PINS[ARCH_PLAN_PATH]),
            ("checkerSha256AtEmit_readOnly", PINS[V15_CHECKER_PATH])):
        _eq(findings, "R1V16-PREDECESSOR", f"$.measuredSelfReport.{key}",
            report.get(key), expected)


def check_carry(doc: Any, v15: Any, findings: list[str]) -> None:
    preservation = doc.get("preservationOfV15")
    if not isinstance(preservation, dict):
        _add(findings, "R1V16-TYPE", "$.preservationOfV15",
             f"declared object, found {json_type(preservation)}")
        return
    rows = preservation.get("carriedKeys")
    if not isinstance(rows, list) or len(rows) != EXPECT_CARRIED_KEYS:
        _add(findings, "R1V16-CARRY", "$.preservationOfV15.carriedKeys",
             f"expected {EXPECT_CARRIED_KEYS} rows, found "
             f"{len(rows) if isinstance(rows, list) else json_type(rows)}")
        rows = rows if isinstance(rows, list) else []
    carried: list[str] = []
    for index, row in enumerate(rows):
        where = f"$.preservationOfV15.carriedKeys[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V16-TYPE", where,
                 f"declared object, found {json_type(row)}")
            continue
        key = row.get("key")
        claim = row.get("identicalToV15")
        if not isinstance(key, str) or not isinstance(claim, str):
            _add(findings, "R1V16-TYPE", where,
                 "key and identicalToV15 are declared strings")
            continue
        carried.append(key)
        if claim != "YES":
            _add(findings, "R1V16-CARRY", f"{where}.identicalToV15",
                 f"expected 'YES'; got {claim!r}")
        if key not in v15:
            _add(findings, "R1V16-CARRY", f"{where}.key",
                 f"{key!r} is claimed carried but is absent from live v1.5")
            continue
        if key not in doc:
            _add(findings, "R1V16-CARRY", f"{where}.key",
                 f"{key!r} is claimed carried but is absent from v1.6")
            continue
        if canon(doc[key]) != canon(v15[key]):
            _add(findings, "R1V16-CARRY", f"$.{key}",
                 f"canonical bytes differ from live v1.5 at the same key")
    _eq(findings, "R1V16-CARRY", "$.preservationOfV15.allCarriedKeysIdentical",
        preservation.get("allCarriedKeysIdentical"), "YES")

    differ = preservation.get("keysThatDIFFERByDesign")
    added = preservation.get("keysADDED")
    if isinstance(differ, dict) and isinstance(added, list):
        expected_differ = sorted(set(v15) - set(carried))
        if sorted(differ) != expected_differ:
            _add(findings, "R1V16-CARRY",
                 "$.preservationOfV15.keysThatDIFFERByDesign",
                 f"declared {sorted(differ)}; live v1.5 keys not carried are "
                 f"{expected_differ}")
        expected_added = sorted(set(doc) - set(v15))
        if sorted(added) != expected_added:
            _add(findings, "R1V16-CARRY", "$.preservationOfV15.keysADDED",
                 f"declared {sorted(added)}; measured {expected_added}")
    else:
        _add(findings, "R1V16-TYPE", "$.preservationOfV15",
             "keysThatDIFFERByDesign is an object and keysADDED an array")

    for key, expect_len, code_where in (
            ("reviewRequests", EXPECT_V15_REVIEW_REQUESTS,
             "$.preservationOfV15.reviewRequestsPrefixIdentical"),
            ("residuals", EXPECT_V15_RESIDUALS,
             "$.preservationOfV15.residualsPrefixIdentical")):
        old = v15.get(key)
        new = doc.get(key)
        if not isinstance(old, list) or not isinstance(new, list):
            _add(findings, "R1V16-TYPE", f"$.{key}",
                 "declared array in both v1.5 and v1.6")
            continue
        if len(old) != expect_len:
            _add(findings, "R1V16-CARRY", f"v1.5 $.{key}",
                 f"expected {expect_len} rows in the predecessor, found "
                 f"{len(old)}")
        if len(new) < len(old) or canon(new[:len(old)]) != canon(old):
            _add(findings, "R1V16-CARRY", f"$.{key}",
                 "the v1.5 prefix is not carried verbatim")
        claim = preservation.get(code_where.rsplit(".", 1)[-1])
        _eq(findings, "R1V16-CARRY", code_where, claim, "YES")

    for key, expect_len in (("closedTypes", EXPECT_CLOSED_TYPES),
                            ("positiveVectors", EXPECT_POSITIVE_VECTORS),
                            ("adversarialControls", EXPECT_ADVERSARIAL),
                            ("staticClosureFixtures", EXPECT_STATIC_FIXTURES)):
        node = doc.get(key)
        size = len(node) if isinstance(node, (list, dict)) else None
        if size != expect_len:
            _add(findings, "R1V16-CARRY", f"$.{key}",
                 f"expected {expect_len} members, found {size}")

    # The placeholders themselves.  A successor that quietly replaced
    # sha256:5555.. with a real digest would have edited the carried vectors.
    values: set[str] = set()
    positions: list[str] = []
    for pointer, value in _iter_leaves(doc.get("positiveVectors"),
                                       "$.positiveVectors"):
        if (pointer.endswith(".derivationDigest") and isinstance(value, str)
                and value.startswith("sha256:")
                and len(set(value[7:])) == 1):
            values.add(value)
            positions.append(pointer)
    if len(values) != EXPECT_PLACEHOLDER_VALUES:
        _add(findings, "R1V16-CARRY", "$.positiveVectors",
             f"expected {EXPECT_PLACEHOLDER_VALUES} distinct derivationDigest "
             f"placeholders, found {len(values)}: {sorted(values)}")
    if len(positions) != EXPECT_PLACEHOLDER_POSITIONS:
        _add(findings, "R1V16-CARRY", "$.positiveVectors",
             f"expected {EXPECT_PLACEHOLDER_POSITIONS} positions carrying a "
             f"placeholder, found {len(positions)}")
    for expected in ("5" * 64, "6" * 64, "8" * 64, "9" * 64):
        if "sha256:" + expected not in values:
            _add(findings, "R1V16-CARRY", "$.positiveVectors",
                 f"the carried placeholder sha256:{expected[:4]}.. is gone")


def _iter_leaves(node: Any, prefix: str):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _iter_leaves(value, f"{prefix}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _iter_leaves(value, f"{prefix}[{index}]")
    else:
        yield prefix, node


def check_law_eighteen(doc: Any, findings: list[str]) -> None:
    """Exact-type scalar admission over $.policyDerivationIdentity.

    IMPLEMENTATION-FREEZE.md section 6 law 18.  This class defeated C-2 at v3,
    v5, v6, v7 and v8 successively, each time inside the repair's own
    self-certification, and a sibling reintroduced it through the generator
    written to fix a blocker.  The section publishes every count as a JSON
    STRING precisely so that 17.0 and true cannot pass for 17.
    """
    section = doc.get("policyDerivationIdentity")
    if not isinstance(section, dict):
        _add(findings, "R1V16-TYPE", "$.policyDerivationIdentity",
             f"declared object, found {json_type(section)}")
        return
    int_leaves = 0
    for pointer, value in _iter_leaves(section, "$.policyDerivationIdentity"):
        if pointer in SECTION_INT_LEAVES:
            int_leaves += 1
            if isinstance(value, bool) or not isinstance(value, int):
                _add(findings, "R1V16-TYPE", pointer,
                     f"declared exact integer, found {json_type(value)}; a "
                     f"float is not an integer and a boolean is not an integer")
            continue
        if not isinstance(value, str):
            _add(findings, "R1V16-TYPE", pointer,
                 f"declared string, found {json_type(value)}; every leaf of "
                 f"this section is a string except the five carried "
                 f"workedExample.completion integers")
    if int_leaves != EXPECT_SECTION_INT_LEAVES:
        _add(findings, "R1V16-TYPE", "$.policyDerivationIdentity",
             f"expected {EXPECT_SECTION_INT_LEAVES} declared integer leaves, "
             f"reached {int_leaves}")
    _eq(findings, "R1V16-TYPE",
        "$.policyDerivationIdentity.lawEighteenScope.rule",
        _get(section, ["lawEighteenScope", "rule"]),
        "IMPLEMENTATION-FREEZE.md section 6 law 18 -- closed-scalar admission "
        "is exact-type.")


def admit_record_value(value: Any, where: str,
                       findings: list[str]) -> bool:
    """Exact-type admission of a published recordValue BEFORE it is encoded."""
    if not isinstance(value, dict):
        _add(findings, "R1V16-TYPE", where,
             f"declared object, found {json_type(value)}")
        return False
    ok = True
    extra = sorted(set(value) - set(TOP_FIELD_NAMES))
    if extra:
        _add(findings, "R1V16-TYPE", where,
             f"undeclared field(s) {extra} in PolicyDerivationInputV1")
        ok = False
    for name, _tag, shape, presence in TOP_FIELDS:
        if name not in value:
            if presence == "required":
                _add(findings, "R1V16-TYPE", f"{where}.{name}",
                     "required field absent")
                ok = False
            continue
        item = value[name]
        if shape is TEXT:
            if not isinstance(item, str):
                _add(findings, "R1V16-TYPE", f"{where}.{name}",
                     f"declared string, found {json_type(item)}")
                ok = False
            continue
        if shape[0] == "record":
            if not _admit_nested(item, shape[1], f"{where}.{name}", findings):
                ok = False
            continue
        if not isinstance(item, list):
            _add(findings, "R1V16-TYPE", f"{where}.{name}",
                 f"declared array, found {json_type(item)}")
            ok = False
            continue
        if shape[0] == "scalar-array":
            for index, member in enumerate(item):
                if not isinstance(member, str):
                    _add(findings, "R1V16-TYPE", f"{where}.{name}[{index}]",
                         f"declared string, found {json_type(member)}")
                    ok = False
        else:
            for index, member in enumerate(item):
                if not _admit_nested(member, shape[2],
                                     f"{where}.{name}[{index}]", findings):
                    ok = False
    return ok


def _admit_nested(value: Any, name: str, where: str,
                  findings: list[str]) -> bool:
    if not isinstance(value, dict):
        _add(findings, "R1V16-TYPE", where,
             f"declared object, found {json_type(value)}")
        return False
    _record_tag, fields = NESTED[name]
    declared = [field for field, _ in fields]
    ok = True
    extra = sorted(set(value) - set(declared))
    if extra:
        _add(findings, "R1V16-TYPE", where,
             f"undeclared field(s) {extra} in {name}")
        ok = False
    for field in declared:
        if field not in value:
            _add(findings, "R1V16-TYPE", f"{where}.{field}",
                 "required field absent")
            ok = False
        elif not isinstance(value[field], str):
            _add(findings, "R1V16-TYPE", f"{where}.{field}",
                 f"declared string, found {json_type(value[field])}")
            ok = False
    return ok


def check_recipe_declaration(doc: Any, findings: list[str]) -> None:
    """The grammar is declared in THIS source; the artifact's statement of it is
    compared against that, never adopted from it."""
    section = _get(doc, ["policyDerivationIdentity"], {})
    _eq(findings, "R1V16-RECIPE", "$.policyDerivationIdentity.id",
        section.get("id"), "POLICY-DERIVATION-DIGEST-V1")
    _eq(findings, "R1V16-RECIPE", "$.policyDerivationIdentity.field",
        section.get("field"), "policyOutcome.derivationDigest")
    _eq(findings, "R1V16-RECIPE",
        "$.policyDerivationIdentity.wireType.regex",
        _get(section, ["wireType", "regex"]), "^sha256:[0-9a-f]{64}$")
    sep = _get(section, ["namespaceAndDomainSeparator"], {})
    _eq(findings, "R1V16-RECIPE",
        "$.policyDerivationIdentity.namespaceAndDomainSeparator.namespace",
        sep.get("namespace"), NAMESPACE)
    _eq(findings, "R1V16-RECIPE",
        "$.policyDerivationIdentity.namespaceAndDomainSeparator.domain",
        sep.get("domain"), DOMAIN)
    _eq(findings, "R1V16-RECIPE",
        "$.policyDerivationIdentity.primitives.componentFrame.bytes",
        _get(section, ["primitives", "componentFrame", "bytes"]),
        "uint8(t) || uint32be(byteLength(b)) || b")
    leaf = _get(section, ["primitives", "leaf"])
    if not isinstance(leaf, str):
        _add(findings, "R1V16-TYPE",
             "$.policyDerivationIdentity.primitives.leaf",
             f"declared string, found {json_type(leaf)}")
    elif "SHA-256( 0x00 || uint64be(byteLength(r)) || r )" not in leaf:
        _add(findings, "R1V16-RECIPE",
             "$.policyDerivationIdentity.primitives.leaf",
             "the leaf rule this checker implements, "
             "SHA-256( 0x00 || uint64be(byteLength(r)) || r ), is not stated")
    step4 = _get(section, ["preimage", "step4_OUTER"])
    if not isinstance(step4, str):
        _add(findings, "R1V16-TYPE",
             "$.policyDerivationIdentity.preimage.step4_OUTER",
             f"declared string, found {json_type(step4)}")
    else:
        for token in ("0x30", "C(0x31, UTF8('opensip.r1-core.v1'))",
                      "C(0x32, ASCII('policy-derivation-v1'))", "C(0x33, root)"):
            if token not in step4:
                _add(findings, "R1V16-RECIPE",
                     "$.policyDerivationIdentity.preimage.step4_OUTER",
                     f"the outer preimage this checker builds names {token}, "
                     f"which the artifact's step 4 does not")

    # The tag table.  Every declared tag must be the tag this checker encodes.
    grammar = _get(section, ["recordGrammar"], {})
    top = _get(grammar, ["PolicyDerivationInputV1"], {})
    _eq(findings, "R1V16-GRAMMAR",
        "$.policyDerivationIdentity.recordGrammar.PolicyDerivationInputV1"
        ".recordTag", top.get("recordTag"), f"0x{RECORD_TAG:02x}")
    rows = top.get("fields")
    if not isinstance(rows, list):
        _add(findings, "R1V16-TYPE",
             "$.policyDerivationIdentity.recordGrammar"
             ".PolicyDerivationInputV1.fields",
             f"declared array, found {json_type(rows)}")
        rows = []
    declared_tags: dict[str, str] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        tag = row.get("tag")
        if isinstance(name, str) and isinstance(tag, str):
            declared_tags[name] = tag
    expected_tags = {name: f"0x{tag:02x}" for name, tag, _, _ in TOP_FIELDS}
    expected_tags["planStageIds[]"] = "0x88"
    expected_tags["rules[]"] = "0x8b"
    expected_tags["findings[]"] = "0x8e"
    expected_tags["exactCoverage[]"] = "0x90"
    for name, expected in sorted(expected_tags.items()):
        got = declared_tags.get(name)
        if got != expected:
            _add(findings, "R1V16-GRAMMAR",
                 "$.policyDerivationIdentity.recordGrammar"
                 f".PolicyDerivationInputV1.fields[{name}].tag",
                 f"this checker encodes {name} at {expected}; the artifact "
                 f"declares {got!r}")
    for name, (record_tag, fields) in sorted(NESTED.items()):
        node = _get(grammar, [name], {})
        _eq(findings, "R1V16-GRAMMAR",
            f"$.policyDerivationIdentity.recordGrammar.{name}.recordTag",
            node.get("recordTag"), f"0x{record_tag:02x}")
        rows = node.get("fields")
        rows = rows if isinstance(rows, list) else []
        got = {row.get("name"): row.get("tag") for row in rows
               if isinstance(row, dict)}
        for field, tag in fields:
            if got.get(field) != f"0x{tag:02x}":
                _add(findings, "R1V16-GRAMMAR",
                     f"$.policyDerivationIdentity.recordGrammar.{name}"
                     f".fields[{field}].tag",
                     f"this checker encodes {field} at 0x{tag:02x}; the "
                     f"artifact declares {got.get(field)!r}")


def check_vectors(doc: Any, findings: list[str]) -> dict[str, Any]:
    """Recompute every published value.  Comparing stored strings tests
    nothing, so nothing published here is read back as an answer."""
    out: dict[str, Any] = {"records": {}, "values": {}, "digests": {}}
    node = _get(doc, ["policyDerivationIdentity", "pinnedVectors"], {})
    _eq(findings, "R1V16-VECTOR",
        "$.policyDerivationIdentity.pinnedVectors.count",
        node.get("count"), str(EXPECT_PINNED_VECTORS))
    vectors = node.get("vectors")
    if not isinstance(vectors, list):
        _add(findings, "R1V16-TYPE",
             "$.policyDerivationIdentity.pinnedVectors.vectors",
             f"declared array, found {json_type(vectors)}")
        return out
    if len(vectors) != EXPECT_PINNED_VECTORS:
        _add(findings, "R1V16-VECTOR",
             "$.policyDerivationIdentity.pinnedVectors.vectors",
             f"expected {EXPECT_PINNED_VECTORS} vectors, found {len(vectors)}")
    seen: set[str] = set()
    max_text = 0
    for index, vector in enumerate(vectors):
        where = f"$.policyDerivationIdentity.pinnedVectors.vectors[{index}]"
        if not isinstance(vector, dict):
            _add(findings, "R1V16-TYPE", where,
                 f"declared object, found {json_type(vector)}")
            continue
        vid = vector.get("id")
        if not isinstance(vid, str):
            _add(findings, "R1V16-TYPE", f"{where}.id",
                 f"declared string, found {json_type(vid)}")
            continue
        if vid in seen:
            _add(findings, "R1V16-VECTOR", f"{where}.id",
                 f"duplicate vector id {vid!r}")
        seen.add(vid)
        value = vector.get("recordValue")
        if not admit_record_value(value, f"{where}.recordValue", findings):
            continue
        for _pointer, leaf in _iter_leaves(value, ""):
            if isinstance(leaf, str):
                max_text = max(max_text, len(leaf.encode("utf-8")))
        try:
            record_a = encode_a(value)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V16-VECTOR", f"{where}.recordValue",
                 f"{vid}: encoder A refused a published vector: "
                 f"{type(exc).__name__}: {exc}")
            continue
        try:
            record_b = encode_b(value)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V16-VECTOR", f"{where}.recordValue",
                 f"{vid}: encoder B refused a published vector: "
                 f"{type(exc).__name__}: {exc}")
            continue
        if record_a != record_b:
            _add(findings, "R1V16-ENCODER-DISAGREE", f"{where}.recordValue",
                 f"{vid}: the two independent encoders produced different "
                 f"record bytes")
            continue
        digest_a = a_derivation_digest(record_a)
        digest_b = b_digest(record_b)
        if digest_a != digest_b:
            _add(findings, "R1V16-ENCODER-DISAGREE", f"{where}",
                 f"{vid}: the two independent encoders produced different "
                 f"derivationDigest values")
            continue
        out["records"][vid] = record_a
        out["values"][vid] = value
        out["digests"][vid] = digest_a

        root = a_leaf_root(record_a)
        preimage = a_outer(root)
        published = {
            "recordBytes": str(len(record_a)),
            "recordSha256": "sha256:" + hashlib.sha256(record_a).hexdigest(),
            "leafRootHex": root.hex(),
            "outerPreimageHex": preimage.hex(),
            "derivationDigest": digest_a,
        }
        if "completeRecordHex" in vector:
            published["completeRecordHex"] = record_a.hex()
        for key, expected in published.items():
            _eq(findings, "R1V16-VECTOR", f"{where}.{key} [{vid}]",
                vector.get(key), expected)
        _eq(findings, "R1V16-VECTOR", f"{where}.decoderRoundTripLiteral [{vid}]",
            vector.get("decoderRoundTripLiteral"), "YES")
        if b_hex(record_b) != record_a.hex():
            _add(findings, "R1V16-ENCODER-DISAGREE", where,
                 f"{vid}: the two hex renderings differ")
    if max_text != EXPECT_MAX_TEXT_BYTES:
        _add(findings, "R1V16-VECTOR",
             "$.policyDerivationIdentity.pinnedVectors.vectors",
             f"the longest text component across all vectors measures "
             f"{max_text} bytes; {EXPECT_MAX_TEXT_BYTES} is expected")
    return out


def check_roundtrip(doc: Any, recomputed: dict[str, Any],
                    findings: list[str]) -> int:
    """decode(encode(x)) == x LITERALLY, as canonical bytes."""
    node = _get(doc, ["policyDerivationIdentity",
                      "injectivityByExhibitedTotalDecoder"], {})
    records: list[tuple[str, bytes]] = []
    for vid, record in recomputed["records"].items():
        value = recomputed["values"][vid]
        try:
            back = decode(record)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V16-ROUNDTRIP", vid,
                 f"the total decoder refused a record this recipe produced: "
                 f"{type(exc).__name__}: {exc}")
            continue
        if canon(back) != canon(value):
            _add(findings, "R1V16-ROUNDTRIP", vid,
                 "decode(encode(x)) != x literally")
        records.append((vid, record))
    # The four rejected-reading exhibit records.  The decoder must be TOTAL on
    # them and must recover exactly the value the rejected encoder framed.
    exhibit_records: list[tuple[str, bytes, frozenset[str]]] = []
    for label, vid, lists in (
            ("exhibitA/documentA-set-reading", "PDD-01", frozenset({"planStageIds"})),
            ("exhibitA/documentB-set-reading", "PDD-17", frozenset({"planStageIds"})),
            ("exhibitB/exactCoverage-length-major", "PDD-01", frozenset({"exactCoverage"})),
            ("exhibitB/rules-length-major", "PDD-16", frozenset({"rules"}))):
        value = recomputed["values"].get(vid)
        if value is None:
            continue
        record = encode_a(value, set_reading=lists)
        records.append((label, record))
        exhibit_records.append((label, record, lists))
    for label, record in records[:len(recomputed["records"])]:
        try:
            back = decode(record)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V16-ROUNDTRIP", label,
                 f"the total decoder refused a record: {type(exc).__name__}: "
                 f"{exc}")
            continue
        if encode_a(back) != record:
            _add(findings, "R1V16-ROUNDTRIP", label,
                 "encode(decode(r)) != r; the decoder is not a left inverse")
    for label, record, lists in exhibit_records:
        try:
            back = decode(record)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V16-ROUNDTRIP", label,
                 f"the total decoder refused a rejected-reading exhibit "
                 f"record: {type(exc).__name__}: {exc}")
            continue
        if encode_a(back, set_reading=lists) != record:
            _add(findings, "R1V16-ROUNDTRIP", label,
                 "the decoder did not recover the value the rejected-reading "
                 "encoder framed")
    if len(records) != EXPECT_ROUNDTRIP_RECORDS:
        _add(findings, "R1V16-ROUNDTRIP",
             "$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder",
             f"expected {EXPECT_ROUNDTRIP_RECORDS} records, round-tripped "
             f"{len(records)}")
    _eq(findings, "R1V16-ROUNDTRIP",
        "$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder"
        ".recordsRoundTripped", node.get("recordsRoundTripped"),
        str(EXPECT_ROUNDTRIP_RECORDS))
    _eq(findings, "R1V16-ROUNDTRIP",
        "$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder"
        ".literalRoundTripsPassing", node.get("literalRoundTripsPassing"),
        str(EXPECT_ROUNDTRIP_RECORDS))
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.recordsLiterallyRoundTripped",
        _get(doc, ["measuredSelfReport", "recordsLiterallyRoundTripped"]),
        f"{EXPECT_ROUNDTRIP_RECORDS} of {EXPECT_ROUNDTRIP_RECORDS}")
    return len(records)


def check_enumerated_injectivity(findings: list[str]) -> int:
    """Beyond the published corpus: 720 admissible values, enumerated here.

    Permuted planStageIds (k=1..3 from a four-id pool) x both variants x three
    rules lists x three exactCoverage lists = 40 * 2 * 3 * 3 = 720.  Required:
    720 distinct encodings, 0 collisions, 720 literal round-trips.
    """
    pool = ["stage:rules", "stage:policy", "stage:third", "stage:fourth"]
    stage_lists = [list(p) for k in (1, 2, 3)
                   for p in itertools.permutations(pool, k)]
    rule_lists = [
        [],
        [{"ruleId": "rule:a", "artifactDigest": "sha256:" + "3" * 64}],
        [{"ruleId": "rule:a", "artifactDigest": "sha256:" + "3" * 64},
         {"ruleId": "rule:b", "artifactDigest": "sha256:" + "c" * 64}],
    ]
    coverage_lists = [
        [{"coverageKey": "coverage:policy", "state": "satisfied"}],
        [{"coverageKey": "coverage:rule", "state": "satisfied"}],
        [{"coverageKey": "coverage:policy", "state": "satisfied"},
         {"coverageKey": "coverage:rule", "state": "satisfied"}],
    ]
    seen: dict[bytes, str] = {}
    total = 0
    collisions = 0
    trips = 0
    for stages in stage_lists:
        for variant in VARIANTS:
            for rules in rule_lists:
                for coverage in coverage_lists:
                    value = {
                        "variant": variant,
                        "observationSetKind": "observation-set",
                        "observationSetDigest": "sha256:" + "1" * 64,
                        "targetUniverseId": "universe:one",
                        "coverageContextKind": "coverage-context",
                        "coverageContextDigest": "sha256:" + "2" * 64,
                        "planStageIds": stages,
                        "rules": rules,
                        "policy": {"policyId": "policy:a",
                                   "artifactDigest": "sha256:" + "4" * 64},
                        "findings": [],
                        "exactCoverage": coverage,
                    }
                    if variant == "incomplete":
                        value["deficiency"] = "budget-exhausted"
                    total += 1
                    try:
                        record = encode_a(value)
                        other = encode_b(value)
                    except (ValueError, TypeError) as exc:
                        _add(findings, "R1V16-INJECTIVITY",
                             f"enumerated[{total}]",
                             f"an admissible value was refused: "
                             f"{type(exc).__name__}: {exc}")
                        continue
                    if record != other:
                        _add(findings, "R1V16-ENCODER-DISAGREE",
                             f"enumerated[{total}]",
                             "the two independent encoders disagreed")
                        continue
                    if record in seen:
                        collisions += 1
                        _add(findings, "R1V16-INJECTIVITY",
                             f"enumerated[{total}]",
                             f"encoding collides with {seen[record]}")
                    seen[record] = canon(value).decode("utf-8")
                    if canon(decode(record)) == canon(value):
                        trips += 1
                    else:
                        _add(findings, "R1V16-INJECTIVITY",
                             f"enumerated[{total}]",
                             "decode(encode(x)) != x literally")
    if total != EXPECT_ENUMERATED_VALUES:
        _add(findings, "R1V16-INJECTIVITY", "enumerated",
             f"expected {EXPECT_ENUMERATED_VALUES} enumerated values, built "
             f"{total}")
    if len(seen) != EXPECT_ENUMERATED_VALUES or collisions:
        _add(findings, "R1V16-INJECTIVITY", "enumerated",
             f"expected {EXPECT_ENUMERATED_VALUES} distinct encodings, found "
             f"{len(seen)} with {collisions} collision(s)")
    if trips != EXPECT_ENUMERATED_VALUES:
        _add(findings, "R1V16-INJECTIVITY", "enumerated",
             f"expected {EXPECT_ENUMERATED_VALUES} literal round-trips, "
             f"measured {trips}")
    return total


def check_falsifier(doc: Any, recomputed: dict[str, Any],
                    findings: list[str]) -> None:
    """The 554-byte falsifier, EXECUTED.

    A sibling artifact declared a control named EPC-V2 that occurs in no
    executable and therefore never fires.  Freeze 7.2.2's rider: a measurement
    that cannot fail the build is prose.  This one runs the rejected reading and
    requires the collision to be real.
    """
    exhibit = _get(doc, ["policyDerivationIdentity", "orderingRuling",
                         "exhibitA_planStageIdsSequenceVsSet"], {})
    where = ("$.policyDerivationIdentity.orderingRuling"
             ".exhibitA_planStageIdsSequenceVsSet")
    value_a = recomputed["values"].get("PDD-01")
    value_b = recomputed["values"].get("PDD-17")
    if value_a is None or value_b is None:
        _add(findings, "R1V16-FALSIFIER", where,
             "PDD-01 or PDD-17 did not encode, so the falsifier cannot run")
        return

    record_a = recomputed["records"]["PDD-01"]
    record_b = recomputed["records"]["PDD-17"]
    adopted_a = recomputed["digests"]["PDD-01"]
    adopted_b = recomputed["digests"]["PDD-17"]

    # Both records the same length: no length check anywhere can tell them apart.
    for label, record, node in (("documentA", record_a, exhibit.get("documentA")),
                                ("documentB", record_b, exhibit.get("documentB"))):
        if len(record) != 554:
            _add(findings, "R1V16-FALSIFIER", f"{where}.{label}",
                 f"the falsifier requires a 554-byte record; measured "
                 f"{len(record)}")
        if isinstance(node, dict):
            _eq(findings, "R1V16-FALSIFIER", f"{where}.{label}.recordBytes",
                node.get("recordBytes"), str(len(record)))
        else:
            _add(findings, "R1V16-TYPE", f"{where}.{label}",
                 f"declared object, found {json_type(node)}")
    _eq(findings, "R1V16-FALSIFIER", f"{where}.documentA.derivationDigest",
        _get(exhibit, ["documentA", "derivationDigest"]), adopted_a)
    _eq(findings, "R1V16-FALSIFIER", f"{where}.documentB.derivationDigest",
        _get(exhibit, ["documentB", "derivationDigest"]), adopted_b)
    _eq(findings, "R1V16-FALSIFIER", f"{where}.recordHexDocumentA",
        exhibit.get("recordHexDocumentA"), record_a.hex())
    _eq(findings, "R1V16-FALSIFIER", f"{where}.recordHexDocumentB",
        exhibit.get("recordHexDocumentB"), record_b.hex())
    if adopted_a == adopted_b:
        _add(findings, "R1V16-FALSIFIER", where,
             "under the ADOPTED sequence reading the two documents are not "
             "distinct; the sequence ruling buys nothing")
    _eq(findings, "R1V16-FALSIFIER", f"{where}.underTheADOPTEDSequenceReading"
        ".distinct", _get(exhibit, ["underTheADOPTEDSequenceReading",
                                    "distinct"]), "YES")

    # Now RUN the rejected reading.
    rejected = frozenset({"planStageIds"})
    set_a = a_derivation_digest(encode_a(value_a, set_reading=rejected))
    set_b = a_derivation_digest(encode_a(value_b, set_reading=rejected))
    node = _get(exhibit, ["underTheREJECTEDSetReading"], {})
    _eq(findings, "R1V16-FALSIFIER", f"{where}.underTheREJECTEDSetReading"
        ".documentA", node.get("documentA"), set_a)
    _eq(findings, "R1V16-FALSIFIER", f"{where}.underTheREJECTEDSetReading"
        ".documentB", node.get("documentB"), set_b)
    _eq(findings, "R1V16-FALSIFIER", f"{where}.underTheREJECTEDSetReading"
        ".collide", node.get("collide"), "YES")
    if set_a != set_b:
        _add(findings, "R1V16-FALSIFIER", where,
             f"the rejected set reading does NOT collide ({set_a} vs {set_b}); "
             f"the artifact's whole case for a SEQUENCE ruling rests on it "
             f"colliding")
    elif set_a != adopted_a:
        _add(findings, "R1V16-FALSIFIER", where,
             f"the set reading collides on {set_a}, which is not PDD-01's own "
             f"published digest {adopted_a}; the published claim is that a "
             f"set-reading implementation PASSES PDD-01 and mints PDD-01's id "
             f"for PDD-17")
    dangerous = node.get("andTHEDANGEROUSPART")
    if isinstance(dangerous, str) and adopted_a[7:] not in dangerous:
        _add(findings, "R1V16-FALSIFIER",
             f"{where}.underTheREJECTEDSetReading.andTHEDANGEROUSPART",
             "the prose does not name the digest the executed control lands on")

    # Exhibit B: WHICH sort, not whether to sort.
    exb = _get(doc, ["policyDerivationIdentity", "orderingRuling",
                     "exhibitB_keyMajorVersusLengthMajor"], {})
    wb = ("$.policyDerivationIdentity.orderingRuling"
          ".exhibitB_keyMajorVersusLengthMajor")
    for key, vid, lists in (("onExactCoverage", "PDD-01",
                             frozenset({"exactCoverage"})),
                            ("onRules", "PDD-16", frozenset({"rules"}))):
        node = _get(exb, [key], {})
        value = recomputed["values"].get(vid)
        if value is None:
            _add(findings, "R1V16-FALSIFIER", f"{wb}.{key}",
                 f"{vid} did not encode")
            continue
        adopted = recomputed["digests"][vid]
        length_major = a_derivation_digest(encode_a(value, set_reading=lists))
        _eq(findings, "R1V16-FALSIFIER", f"{wb}.{key}.adoptedDigest",
            node.get("adoptedDigest"), adopted)
        _eq(findings, "R1V16-FALSIFIER",
            f"{wb}.{key}.digestIfEP8sSortedListsWereApplied",
            node.get("digestIfEP8sSortedListsWereApplied"), length_major)
        _eq(findings, "R1V16-FALSIFIER", f"{wb}.{key}.ordersDiffer",
            node.get("ordersDiffer"), "YES")
        _eq(findings, "R1V16-FALSIFIER", f"{wb}.{key}.distinct",
            node.get("distinct"), "YES")
        if adopted == length_major:
            _add(findings, "R1V16-FALSIFIER", f"{wb}.{key}",
                 "key-major and length-major produce the same digest here, so "
                 "this exhibit separates nothing")


def check_order_rulings(doc: Any, v15: Any, recomputed: dict[str, Any],
                        findings: list[str]) -> None:
    """The rulings, their v1.5 provenance, and the REFUSAL that buys literal
    injectivity -- executed per list against the named condition."""
    ruling = _get(doc, ["policyDerivationIdentity", "orderingRuling"], {})
    where = "$.policyDerivationIdentity.orderingRuling"
    plan = _get(ruling, ["planStageIds"], {})
    _eq(findings, "R1V16-ORDER-RULING", f"{where}.planStageIds.ruling",
        plan.get("ruling"),
        "SEQUENCE. Order is semantic and is preserved byte-for-byte. It is NOT "
        "a set.")
    quoted = _get(ruling, ["rules_findings_exactCoverage", "orderRulesQuoted"],
                  {})
    for name, (expected, pointer) in V15_ORDER_RULES.items():
        live = _get(v15, pointer)
        if live != expected:
            _add(findings, "R1V16-ORDER-RULING",
                 "v1.5 $." + ".".join(pointer),
                 f"this checker implements {expected!r}; live v1.5 states "
                 f"{live!r}")
        if name == "planStageIds":
            if expected not in str(plan.get("derivedFrom")):
                _add(findings, "R1V16-ORDER-RULING",
                     f"{where}.planStageIds.derivedFrom",
                     f"the SEQUENCE ruling is derived from v1.5's orderRule, "
                     f"but the stated provenance does not quote it verbatim: "
                     f"{expected!r}")
            continue
        _eq(findings, "R1V16-ORDER-RULING",
            f"{where}.rules_findings_exactCoverage.orderRulesQuoted.{name}",
            quoted.get(name), expected)
    _eq(findings, "R1V16-ORDER-RULING",
        f"{where}.fourListsInThePreimage",
        ruling.get("fourListsInThePreimage"),
        "planStageIds, rules, findings, exactCoverage. All four are ruled below.")

    # planStageIds uniqueness is NOT an order rule; it is what makes both
    # orders VALID inputs and therefore makes the set reading lossy.
    _eq(findings, "R1V16-ORDER-RULING",
        "v1.5 $.closedTypes.SealedStageInput.fields.planStageIds.uniquenessRule",
        _get(v15, ["closedTypes", "SealedStageInput", "fields", "planStageIds",
                   "uniquenessRule"]), "exact string uniqueness")

    # EXECUTE the refusal, per list, and require the NAMED condition.
    base = recomputed["values"].get("PDD-01")
    if not isinstance(base, dict):
        _add(findings, "R1V16-ORDER", where, "PDD-01 unavailable")
        return
    cases = [
        ("exactCoverage",
         lambda v: v.update({"exactCoverage": list(reversed(v["exactCoverage"]))}),
         "exactCoverage violates R-1's strict-ascending orderRule at index 1"),
        ("rules",
         lambda v: v.update({"rules": [
             {"ruleId": "rule:b", "artifactDigest": "sha256:" + "c" * 64},
             {"ruleId": "rule:a", "artifactDigest": "sha256:" + "3" * 64}]}),
         "rules violates R-1's strict-ascending orderRule at index 1"),
        ("findings",
         lambda v: v.update({"findings": [
             {"ruleId": "rule:b", "findingId": "finding:1",
              "valueDigest": "sha256:" + "e" * 64},
             {"ruleId": "rule:a", "findingId": "finding:1",
              "valueDigest": "sha256:" + "e" * 64}]}),
         "findings violates R-1's strict-ascending orderRule at index 1"),
    ]
    for name, mutate, expected in cases:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        try:
            encode_a(candidate)
        except ValueError as exc:
            if str(exc) != expected:
                _add(findings, "R1V16-ORDER", f"{where}/{name}",
                     f"the encoder refused a mis-ordered {name}, but on "
                     f"{str(exc)!r} rather than the named condition "
                     f"{expected!r}")
        except TypeError as exc:
            _add(findings, "R1V16-ORDER", f"{where}/{name}",
                 f"a mis-ordered {name} was refused on a type error "
                 f"({exc}), not on the order rule")
        else:
            _add(findings, "R1V16-ORDER", f"{where}/{name}",
                 f"the encoder ACCEPTED a mis-ordered {name}; a repairing "
                 f"encoder is many-to-one and the LITERAL round-trip claim "
                 f"does not survive it")
    # And the refusal is not a repair in disguise.  A REPAIRING encoder maps
    # two DISTINCT admitted inputs onto ONE record -- the many-to-one shape
    # that cost plan-and-policy-identity-recipes its literal claim at
    # B-PPIR-01 and forced the retreat to decode(encode(x)) == canonical(x).
    # The adopted encoder is shown above to REFUSE instead; this asserts that
    # the repairing shape really would have collapsed them, so the stated
    # reason for refusing is a live property of these bytes and not a slogan.
    repaired = copy.deepcopy(base)
    repaired["exactCoverage"] = list(reversed(base["exactCoverage"]))
    sorting = frozenset({"exactCoverage"})
    if canon(repaired) == canon(base):
        _add(findings, "R1V16-ORDER", f"{where}/repair-would-collapse",
             "the reversed exactCoverage is not a distinct input, so this "
             "control separates nothing")
    elif encode_a(repaired, set_reading=sorting) != encode_a(base,
                                                             set_reading=sorting):
        _add(findings, "R1V16-ORDER", f"{where}/repair-would-collapse",
             "a repairing encoder would NOT have mapped the ordered and the "
             "reversed exactCoverage onto one record, so the stated reason for "
             "refusing to repair does not hold on these bytes")


def check_rejection_controls(doc: Any, recomputed: dict[str, Any],
                             findings: list[str]) -> int:
    """Fifteen controls, EXECUTED, each on the condition it NAMES.

    Freeze 7.4: a non-zero exit is not evidence a guard fired.  An admitted row
    is an escape, and a row that raises for the wrong reason is a finding.
    """
    node = _get(doc, ["policyDerivationIdentity", "rejectionControls"], {})
    where = "$.policyDerivationIdentity.rejectionControls"
    _eq(findings, "R1V16-REJ", f"{where}.count", node.get("count"),
        str(EXPECT_REJECTIONS))
    _eq(findings, "R1V16-REJ", f"{where}.allRejectedByBothEncoders",
        node.get("allRejectedByBothEncoders"), "YES")
    rows = node.get("controls")
    if not isinstance(rows, list):
        _add(findings, "R1V16-TYPE", f"{where}.controls",
             f"declared array, found {json_type(rows)}")
        return 0
    if len(rows) != EXPECT_REJECTIONS:
        _add(findings, "R1V16-REJ", f"{where}.controls",
             f"expected {EXPECT_REJECTIONS} controls, found {len(rows)}")
    base = recomputed["values"].get("PDD-01")
    if not isinstance(base, dict):
        _add(findings, "R1V16-REJ", where, "PDD-01 unavailable")
        return 0

    def with_universe(value: Any) -> dict[str, Any]:
        candidate = copy.deepcopy(base)
        candidate["targetUniverseId"] = value
        return candidate

    def build(control_id: str) -> dict[str, Any] | None:
        candidate = copy.deepcopy(base)
        if control_id == "REJ-01":
            return with_universe("universe:A\u0300")
        if control_id == "REJ-02":
            return with_universe("u" * 4097)
        if control_id == "REJ-03":
            return with_universe("universe:\u0007one")
        if control_id == "REJ-04":
            return with_universe("")
        if control_id == "REJ-05":
            return with_universe("\ufeffuniverse:one")
        if control_id == "REJ-06":
            candidate["planStageIds"] = ["stage:rules", "stage:rules"]
            return candidate
        if control_id == "REJ-07":
            entry = candidate["exactCoverage"][0]
            candidate["exactCoverage"] = [copy.deepcopy(entry),
                                          copy.deepcopy(entry)]
            return candidate
        if control_id == "REJ-08":
            candidate["exactCoverage"] = list(
                reversed(candidate["exactCoverage"]))
            return candidate
        if control_id == "REJ-09":
            candidate["rules"] = [
                {"ruleId": "rule:b", "artifactDigest": "sha256:" + "c" * 64},
                {"ruleId": "rule:a", "artifactDigest": "sha256:" + "3" * 64}]
            return candidate
        if control_id == "REJ-10":
            candidate["deficiency"] = "budget-exhausted"
            return candidate
        if control_id == "REJ-11":
            candidate["variant"] = "incomplete"
            return candidate
        if control_id == "REJ-12":
            candidate["variant"] = "cancelled"
            return candidate
        if control_id == "REJ-13":
            candidate["budgetUsage"] = "sha256:" + "0" * 64
            return candidate
        if control_id == "REJ-14":
            return with_universe(7)
        if control_id == "REJ-15":
            return with_universe(True)
        return None

    executed = 0
    for index, row in enumerate(rows):
        row_where = f"{where}.controls[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V16-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        control_id = row.get("id")
        if not isinstance(control_id, str):
            _add(findings, "R1V16-TYPE", f"{row_where}.id",
                 f"declared string, found {json_type(control_id)}")
            continue
        _eq(findings, "R1V16-REJ", f"{row_where}.bothReject",
            row.get("bothReject"), "YES")
        candidate = build(control_id)
        if candidate is None:
            _add(findings, "R1V16-REJ", f"{row_where}.id",
                 f"{control_id}: this instrument has no executable input for "
                 f"this control, so the row is declared and not measured")
            continue
        executed += 1
        for label, encoder, declared_key in (("encoderA", encode_a, "encoderA"),
                                             ("encoderB", encode_b, "encoderB")):
            declared = row.get(declared_key)
            try:
                encoder(copy.deepcopy(candidate))
            except (ValueError, TypeError) as exc:
                actual = f"{type(exc).__name__}: {exc}"
                if actual != declared:
                    _add(findings, "R1V16-REJ",
                         f"{row_where}.{declared_key} [{control_id}]",
                         f"{label} refused, but on {actual!r}; the artifact "
                         f"records {declared!r}")
            else:
                _add(findings, "R1V16-REJ",
                     f"{row_where}.{declared_key} [{control_id}]",
                     f"{label} ADMITTED the input this control names; an "
                     f"admitted row is an escape, not a finding about the row")
    if executed != EXPECT_REJECTIONS:
        _add(findings, "R1V16-REJ", f"{where}.controls",
             f"expected {EXPECT_REJECTIONS} controls to be EXECUTED, executed "
             f"{executed}")
    _eq(findings, "R1V16-SELFREPORT", "$.measuredSelfReport.rejectionControls",
        _get(doc, ["measuredSelfReport", "rejectionControls"]),
        str(EXPECT_REJECTIONS))
    return executed


def check_decoder_probes(doc: Any, recomputed: dict[str, Any],
                         findings: list[str]) -> int:
    """Six malformed probes, executed against a record this recipe produced."""
    rows = _get(doc, ["policyDerivationIdentity", "decoderProbes"])
    where = "$.policyDerivationIdentity.decoderProbes"
    record = recomputed["records"].get("PDD-01")
    if record is None:
        _add(findings, "R1V16-DECODER-PROBE", where, "PDD-01 unavailable")
        return 0
    probes: dict[str, bytes] = {
        "the record truncated by one byte": record[:-1],
        "the record tag replaced by 0x81": b"\x81" + record[1:],
        "one extra 0x00 byte appended": record + b"\x00",
        "the first field length inflated to 0xffffffff":
            record[:2] + b"\xff\xff\xff\xff" + record[6:],
        "an undeclared field tag 0x99 appended":
            record + b"\x99\x00\x00\x00\x00",
        "two declared fields transposed":
            record[:1] + record[10:29] + record[1:10] + record[29:],
    }
    if not isinstance(rows, list):
        _add(findings, "R1V16-TYPE", where,
             f"declared array, found {json_type(rows)}")
        return 0
    if len(rows) != EXPECT_DECODER_PROBES:
        _add(findings, "R1V16-DECODER-PROBE", where,
             f"expected {EXPECT_DECODER_PROBES} probes, found {len(rows)}")
    executed = 0
    for index, row in enumerate(rows):
        row_where = f"{where}[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V16-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        probe = row.get("probe")
        outcome = row.get("outcome")
        if not isinstance(probe, str) or not isinstance(outcome, str):
            _add(findings, "R1V16-TYPE", row_where,
                 "probe and outcome are declared strings")
            continue
        buf = probes.get(probe)
        if buf is None:
            _add(findings, "R1V16-DECODER-PROBE", f"{row_where}.probe",
                 f"{probe!r}: this instrument has no executable form of this "
                 f"probe, so the row is declared and not measured")
            continue
        executed += 1
        try:
            decode(buf)
        except (ValueError, TypeError) as exc:
            actual = f"{type(exc).__name__}: {exc}"
            if actual != outcome:
                _add(findings, "R1V16-DECODER-PROBE", f"{row_where}.outcome",
                     f"{probe!r}: the decoder raised {actual!r}; the artifact "
                     f"records {outcome!r}")
        else:
            _add(findings, "R1V16-DECODER-PROBE", f"{row_where}.outcome",
                 f"{probe!r}: the total decoder ACCEPTED a malformed record")
    if executed != EXPECT_DECODER_PROBES:
        _add(findings, "R1V16-DECODER-PROBE", where,
             f"expected {EXPECT_DECODER_PROBES} probes EXECUTED, executed "
             f"{executed}")
    malformed = _get(doc, ["policyDerivationIdentity",
                           "injectivityByExhibitedTotalDecoder",
                           "malformedProbes"])
    if canon(malformed) != canon(rows):
        _add(findings, "R1V16-DECODER-PROBE",
             "$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder"
             ".malformedProbes",
             "the two published probe lists are not the same list")
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.decoderMalformedProbes",
        _get(doc, ["measuredSelfReport", "decoderMalformedProbes"]),
        str(EXPECT_DECODER_PROBES))
    return executed


def check_field_set_rule(doc: Any, v15: Any, recomputed: dict[str, Any],
                         findings: list[str]) -> None:
    """The rule, applied to LIVE v1.5, must reproduce the published records."""
    vectors = v15.get("positiveVectors")
    if not isinstance(vectors, list):
        _add(findings, "R1V16-TYPE", "v1.5 $.positiveVectors",
             f"declared array, found {json_type(vectors)}")
        return
    table = {v["id"]: v for v in vectors
             if isinstance(v, dict) and isinstance(v.get("id"), str)}

    # The measured basis for the exclusions: every override touches only
    # deps.budgetLimits.* and attempt.executionId, and every vector clones
    # POS-01, so no v1.5 vector can discriminate any INCLUSION.
    declarers = 0
    base_id = "R1V15-POS-01-COMPLETED-NO-DIAGNOSTICS"
    for vector in vectors:
        if not isinstance(vector, dict):
            continue
        vid = vector.get("id")
        if vid != base_id and vector.get("cloneOf") != base_id:
            _add(findings, "R1V16-FIELDSET", f"v1.5 $.positiveVectors[{vid}]",
                 f"expected cloneOf {base_id!r}; got "
                 f"{vector.get('cloneOf')!r}")
        for dotted in (vector.get("overrides") or {}):
            if not (dotted.startswith("deps.budgetLimits.")
                    or dotted == "attempt.executionId"):
                _add(findings, "R1V16-FIELDSET",
                     f"v1.5 $.positiveVectors[{vid}].overrides",
                     f"{dotted!r} touches a subtree outside the declared "
                     f"evidence-neutral set, so the exclusion argument does "
                     f"not hold as stated")
        if "expectProjectionEqualTo" in vector:
            declarers += 1
    if declarers != EXPECT_PROJECTION_EQUAL_DECLARERS:
        _add(findings, "R1V16-FIELDSET", "v1.5 $.positiveVectors",
             f"expected {EXPECT_PROJECTION_EQUAL_DECLARERS} vectors declaring "
             f"expectProjectionEqualTo, measured {declarers}")
    resolved_all = [resolve_v15(v15, vid) for vid in table]
    stage_forms = {canon(_get(r, ["stageInput"])) for r in resolved_all
                   if r is not None}
    dep_forms = {canon({k: v for k, v in (_get(r, ["deps"]) or {}).items()
                        if k != "budgetLimits"})
                 for r in resolved_all if r is not None}
    if len(stage_forms) != 1 or len(dep_forms) != 1:
        _add(findings, "R1V16-FIELDSET", "v1.5 $.positiveVectors",
             f"the ten vectors do not share one stageInput and one non-budget "
             f"deps ({len(stage_forms)} stageInput form(s), {len(dep_forms)} "
             f"deps form(s))")

    # PDD-01..PDD-04 must be reproducible from the rule.
    for pdd_id, v15_id, source in V15_MODELLED:
        published = recomputed["values"].get(pdd_id)
        if published is None:
            continue
        vector = table.get(v15_id)
        if vector is None:
            _add(findings, "R1V16-FIELDSET", f"v1.5 {v15_id}",
                 "the modelled vector is absent from live v1.5")
            continue
        completion = vector.get(source)
        if completion is None:
            parent = table.get(vector.get("cloneOf"), {})
            completion = parent.get(source)
        resolved = resolve_v15(v15, v15_id)
        if resolved is None or not isinstance(completion, dict):
            _add(findings, "R1V16-FIELDSET", f"v1.5 {v15_id}",
                 f"could not resolve the vector or its {source}")
            continue
        rebuilt = field_set_record(resolved, completion)
        if rebuilt is None:
            _add(findings, "R1V16-FIELDSET", f"v1.5 {v15_id}",
                 "the fieldSetRule did not yield a complete record")
            continue
        if canon(rebuilt) != canon(published):
            _add(findings, "R1V16-FIELDSET",
                 f"$.policyDerivationIdentity.pinnedVectors[{pdd_id}]"
                 ".recordValue",
                 f"the fieldSetRule applied to live v1.5 {v15_id} does not "
                 f"reproduce the published recordValue")

    # The four equivalence controls, rebuilt from v1.5 rather than read back.
    node = _get(doc, ["policyDerivationIdentity", "equivalenceControls"], {})
    where = "$.policyDerivationIdentity.equivalenceControls"
    rows = node.get("controls")
    if not isinstance(rows, list):
        _add(findings, "R1V16-TYPE", f"{where}.controls",
             f"declared array, found {json_type(rows)}")
        return
    if len(rows) != EXPECT_EQUIVALENCE:
        _add(findings, "R1V16-EQ", f"{where}.controls",
             f"expected {EXPECT_EQUIVALENCE} controls, found {len(rows)}")
    _eq(findings, "R1V16-EQ", f"{where}.allEqualPDD01",
        node.get("allEqualPDD01"), "YES")
    target = recomputed["digests"].get("PDD-01")
    for index, row in enumerate(rows):
        row_where = f"{where}.controls[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V16-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        built_from = row.get("builtFrom")
        if not isinstance(built_from, str) or built_from not in table:
            _add(findings, "R1V16-EQ", f"{row_where}.builtFrom",
                 f"{built_from!r} is not a live v1.5 vector")
            continue
        vector = table[built_from]
        overrides = vector.get("overrides") or {}
        declared_overrides = row.get("v15Overrides")
        if not isinstance(declared_overrides, dict):
            _add(findings, "R1V16-TYPE", f"{row_where}.v15Overrides",
                 f"declared object, found {json_type(declared_overrides)}")
        else:
            measured = {key: str(value) for key, value in overrides.items()}
            for key, value in sorted(declared_overrides.items()):
                if not isinstance(value, str):
                    _add(findings, "R1V16-TYPE",
                         f"{row_where}.v15Overrides.{key}",
                         f"declared string, found {json_type(value)}")
            if measured != declared_overrides:
                _add(findings, "R1V16-EQ", f"{row_where}.v15Overrides",
                     f"live v1.5 overrides {measured}; the artifact records "
                     f"{declared_overrides}")
        equal_to = vector.get("expectProjectionEqualTo")
        peer = table.get(equal_to) if isinstance(equal_to, str) else None
        completion = (peer or {}).get("expectedCompletion")
        resolved = resolve_v15(v15, built_from)
        if resolved is None or not isinstance(completion, dict):
            _add(findings, "R1V16-EQ", row_where,
                 f"could not rebuild {built_from} from live v1.5")
            continue
        rebuilt = field_set_record(resolved, completion)
        if rebuilt is None:
            _add(findings, "R1V16-EQ", row_where,
                 "the fieldSetRule did not yield a complete record")
            continue
        digest = a_derivation_digest(encode_a(rebuilt))
        if b_digest(encode_b(rebuilt)) != digest:
            _add(findings, "R1V16-ENCODER-DISAGREE", row_where,
                 "the two independent encoders disagreed on an equivalence "
                 "control")
        _eq(findings, "R1V16-EQ", f"{row_where}.derivationDigest",
            row.get("derivationDigest"), digest)
        _eq(findings, "R1V16-EQ", f"{row_where}.equalsPDD01",
            row.get("equalsPDD01"), "YES")
        if target is not None and digest != target:
            _add(findings, "R1V16-EQ", row_where,
                 f"rebuilt from live v1.5 {built_from}, the control yields "
                 f"{digest}, not PDD-01's {target}; the exclusion claim would "
                 f"be false")
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.equivalenceControls",
        _get(doc, ["measuredSelfReport", "equivalenceControls"]),
        str(EXPECT_EQUIVALENCE))


def check_separation(doc: Any, v15: Any, recomputed: dict[str, Any],
                     findings: list[str]) -> None:
    node = _get(doc, ["policyDerivationIdentity", "separationControls"], {})
    where = "$.policyDerivationIdentity.separationControls"
    rows = node.get("controls")
    if not isinstance(rows, list):
        _add(findings, "R1V16-TYPE", f"{where}.controls",
             f"declared array, found {json_type(rows)}")
        return
    if len(rows) != EXPECT_SEPARATION:
        _add(findings, "R1V16-SEP", f"{where}.controls",
             f"expected {EXPECT_SEPARATION} controls, found {len(rows)}")
    record = recomputed["records"].get("PDD-01")
    target = recomputed["digests"].get("PDD-01")
    if record is None:
        _add(findings, "R1V16-SEP", where, "PDD-01 unavailable")
        return
    computed: list[str] = []
    for index, row in enumerate(rows):
        row_where = f"{where}.controls[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V16-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        namespace = row.get("namespace")
        domain = row.get("domain")
        if not isinstance(namespace, str) or not isinstance(domain, str):
            _add(findings, "R1V16-TYPE", row_where,
                 "namespace and domain are declared strings")
            continue
        digest = a_derivation_digest(record, namespace, domain)
        if b_digest(record, namespace, domain) != digest:
            _add(findings, "R1V16-ENCODER-DISAGREE", row_where,
                 "the two independent encoders disagreed on a separation "
                 "control")
        computed.append(digest)
        _eq(findings, "R1V16-SEP", f"{row_where}.derivationDigest",
            row.get("derivationDigest"), digest)
        expected_equal = "YES" if (namespace == NAMESPACE
                                   and domain == DOMAIN) else "NO"
        _eq(findings, "R1V16-SEP", f"{row_where}.equalsPDD01",
            row.get("equalsPDD01"), expected_equal)
        if expected_equal == "YES" and digest != target:
            _add(findings, "R1V16-SEP", row_where,
                 f"the identity control does not reproduce PDD-01: {digest} "
                 f"!= {target}")
        if expected_equal == "NO" and digest == target:
            _add(findings, "R1V16-SEP", row_where,
                 "a separator that does not separate: this pair reproduces "
                 "PDD-01's digest")
    if len(set(computed)) != EXPECT_SEPARATION:
        _add(findings, "R1V16-SEP", f"{where}.controls",
             f"expected {EXPECT_SEPARATION} distinct values, computed "
             f"{len(set(computed))}")
    _eq(findings, "R1V16-SEP", f"{where}.fiveDistinctValues",
        node.get("fiveDistinctValues"), "YES")
    _eq(findings, "R1V16-SEP", f"{where}.xd5ReproducesPDD01",
        node.get("xd5ReproducesPDD01"), "YES")

    # R-1's carried conformance oracle cannot share a preimage with this
    # identity.  The oracle's prefix is read from LIVE v1.5, not from v1.6.
    grammar = _get(v15, ["evidenceIdentity", "conformanceCommitmentGrammar"])
    oracle_where = f"{where}.conformanceOracleNonCollision"
    if not isinstance(grammar, str):
        _add(findings, "R1V16-TYPE",
             "v1.5 $.evidenceIdentity.conformanceCommitmentGrammar",
             f"declared string, found {json_type(grammar)}")
        return
    prefix = "opensip:r1-v1.5:projection"
    if prefix not in grammar:
        _add(findings, "R1V16-SEP",
             "v1.5 $.evidenceIdentity.conformanceCommitmentGrammar",
             f"live v1.5 does not carry the oracle prefix {prefix!r} this "
             f"separation argument is built on")
        return
    oracle_first_two = (prefix + "\u0000").encode("utf-8")[:2].hex()
    identity_first_two = a_outer(a_leaf_root(record))[:2].hex()
    _eq(findings, "R1V16-SEP", f"{oracle_where}.oraclePreimageFirstTwoBytesHex",
        _get(node, ["conformanceOracleNonCollision",
                    "oraclePreimageFirstTwoBytesHex"]), oracle_first_two)
    _eq(findings, "R1V16-SEP",
        f"{oracle_where}.identityOuterPreimageFirstTwoBytesHex",
        _get(node, ["conformanceOracleNonCollision",
                    "identityOuterPreimageFirstTwoBytesHex"]),
        identity_first_two)
    _eq(findings, "R1V16-SEP", f"{oracle_where}.canShareAPreimage",
        _get(node, ["conformanceOracleNonCollision", "canShareAPreimage"]), "NO")
    if oracle_first_two[:2] == identity_first_two[:2]:
        _add(findings, "R1V16-SEP", oracle_where,
             f"the two constructions agree in their first byte "
             f"(0x{oracle_first_two[:2]}), so the non-collision argument does "
             f"not hold")
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.separationControls",
        _get(doc, ["measuredSelfReport", "separationControls"]),
        str(EXPECT_SEPARATION))


def check_worked_example(doc: Any, v15: Any, recomputed: dict[str, Any],
                         findings: list[str]) -> None:
    """A real derivationDigest in a complete CoreCompletion::completed."""
    node = _get(doc, ["policyDerivationIdentity", "workedExample"], {})
    where = "$.policyDerivationIdentity.workedExample"
    value = node.get("derivationInputRecord")
    if not admit_record_value(value, f"{where}.derivationInputRecord", findings):
        return
    digest = a_derivation_digest(encode_a(value))
    if b_digest(encode_b(value)) != digest:
        _add(findings, "R1V16-ENCODER-DISAGREE", where,
             "the two independent encoders disagreed on the worked example")
    published = _get(node, ["completion", "policyOutcome", "derivationDigest"])
    _eq(findings, "R1V16-WORKED",
        f"{where}.completion.policyOutcome.derivationDigest", published, digest)
    if isinstance(published, str) and len(set(published[7:])) == 1:
        _add(findings, "R1V16-WORKED",
             f"{where}.completion.policyOutcome.derivationDigest",
             "the worked example carries a repeated-digit placeholder, not a "
             "value derived from the rule")
    target = recomputed["digests"].get("PDD-01")
    if target is not None and digest != target:
        _add(findings, "R1V16-WORKED", where,
             f"the worked example's semantics are POS-01's, so its digest must "
             f"be PDD-01's {target}; computed {digest}")
    # Everything except that one field must be v1.5's POS-01 expectedCompletion.
    live = _get(v15, ["positiveVectors", 0, "expectedCompletion"])
    completion = node.get("completion")
    if isinstance(live, dict) and isinstance(completion, dict):
        left = copy.deepcopy(live)
        right = copy.deepcopy(completion)
        for side in (left, right):
            outcome = side.get("policyOutcome")
            if isinstance(outcome, dict):
                outcome.pop("derivationDigest", None)
        if canon(left) != canon(right):
            _add(findings, "R1V16-WORKED", f"{where}.completion",
                 "the worked example differs from live v1.5 POS-01's "
                 "expectedCompletion in more than derivationDigest")
        placeholder = _get(live, ["policyOutcome", "derivationDigest"])
        stated = str(node.get("theOnlyDifferenceFromTheCarriedVector"))
        if not isinstance(placeholder, str) or placeholder[:11] not in stated:
            _add(findings, "R1V16-WORKED",
                 f"{where}.theOnlyDifferenceFromTheCarriedVector",
                 f"the stated difference does not name the placeholder "
                 f"{placeholder!r} that live v1.5 POS-01 actually carries")
    else:
        _add(findings, "R1V16-TYPE", f"{where}.completion",
             "declared object in both v1.5 and the worked example")

    # The migration table: every position v1.5 carries a placeholder at, and
    # the value this rule produces there.
    rows = _get(doc, ["policyDerivationIdentity",
                      "relationToTheCarriedPositiveVectors",
                      "migrationTable"])
    census = _get(doc, ["policyDerivationIdentity",
                        "relationToTheCarriedPositiveVectors",
                        "placeholderCensusMeasuredHere"], {})
    _eq(findings, "R1V16-WORKED",
        "$.policyDerivationIdentity.relationToTheCarriedPositiveVectors"
        ".placeholderCensusMeasuredHere.distinctPlaceholderValues",
        census.get("distinctPlaceholderValues"),
        str(EXPECT_PLACEHOLDER_VALUES))
    _eq(findings, "R1V16-WORKED",
        "$.policyDerivationIdentity.relationToTheCarriedPositiveVectors"
        ".placeholderCensusMeasuredHere.positionsCarrying",
        census.get("positionsCarrying"), str(EXPECT_PLACEHOLDER_POSITIONS))
    if not isinstance(rows, list):
        _add(findings, "R1V16-TYPE",
             "$.policyDerivationIdentity.relationToTheCarriedPositiveVectors"
             ".migrationTable",
             f"declared array, found {json_type(rows)}")
        return
    counted = 0
    for index, row in enumerate(rows):
        row_where = ("$.policyDerivationIdentity"
                     f".relationToTheCarriedPositiveVectors"
                     f".migrationTable[{index}]")
        if not isinstance(row, dict):
            _add(findings, "R1V16-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        vid = row.get("vector")
        positions = row.get("positions")
        placeholder = row.get("carriedPlaceholder")
        if isinstance(positions, list):
            counted += len(positions)
            for pointer in positions:
                if not isinstance(pointer, str):
                    continue
                live_value = _pointer(v15, pointer.lstrip("#"))
                if live_value != placeholder:
                    _add(findings, "R1V16-WORKED", f"{row_where}.positions",
                         f"live v1.5 {pointer} carries {live_value!r}; the "
                         f"table records {placeholder!r}")
        expected = recomputed["digests"].get(vid)
        if expected is not None:
            _eq(findings, "R1V16-WORKED", f"{row_where}.valueThisRuleProduces",
                row.get("valueThisRuleProduces"), expected)
    if counted != EXPECT_PLACEHOLDER_POSITIONS:
        _add(findings, "R1V16-WORKED",
             "$.policyDerivationIdentity.relationToTheCarriedPositiveVectors"
             ".migrationTable",
             f"the table names {counted} positions; "
             f"{EXPECT_PLACEHOLDER_POSITIONS} carry a placeholder")


def _pointer(node: Any, pointer: str) -> Any:
    cur = node
    if not pointer.startswith("/"):
        return None
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            try:
                cur = cur[int(token)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict) and token in cur:
            cur = cur[token]
        else:
            return None
    return cur


def _ep8_clauses(ep8: Any) -> list[str]:
    out: list[str] = []

    def walk(node: Any, prefix: str) -> None:
        if isinstance(node, dict) and prefix not in EP8_CLAUSE_AGGREGATES:
            for key, value in node.items():
                walk(value, f"{prefix}.{key}" if prefix else key)
        else:
            out.append(prefix)

    for grammar in ("normativePreimageGrammar", "canonicalCommitmentGrammar"):
        walk(_get(ep8, [grammar]), grammar)
    return out


def check_ep8(doc: Any, ep8: Any, findings: list[str]) -> None:
    for pointer, expected in sorted(EP8_VERBATIM.items()):
        live = _get(ep8, list(pointer))
        if live != expected:
            _add(findings, "R1V16-EP8", "EP8 $." + ".".join(pointer),
                 f"this checker transcribes {expected!r}; live EP8 states "
                 f"{live!r}")
    domains = _get(ep8, ["canonicalCommitmentGrammar", "domains"])
    if not isinstance(domains, list) or len(domains) != EXPECT_EP8_DOMAINS:
        _add(findings, "R1V16-EP8", "EP8 $.canonicalCommitmentGrammar.domains",
             f"expected {EXPECT_EP8_DOMAINS} members, found "
             f"{len(domains) if isinstance(domains, list) else json_type(domains)}")
    elif DOMAIN in domains:
        _add(findings, "R1V16-EP8", "EP8 $.canonicalCommitmentGrammar.domains",
             f"{DOMAIN!r} has been added to EP8's closed domain list; law 19 "
             f"requires R-1 to mint its own under its own namespace, not to "
             f"extend EP8's")
    records = _get(ep8, ["normativePreimageGrammar", "records"])
    if not isinstance(records, list) or len(records) != EXPECT_EP8_RECORD_TYPES:
        _add(findings, "R1V16-EP8", "EP8 $.normativePreimageGrammar.records",
             f"the clause enumeration counts this table ONCE on the stated "
             f"basis that it is EP8's table of {EXPECT_EP8_RECORD_TYPES} "
             f"record types rather than a rule; found "
             f"{len(records) if isinstance(records, list) else json_type(records)}")
    occurrences = json.dumps(ep8, sort_keys=True).count("componentFrame")
    _eq(findings, "R1V16-EP8",
        "$.policyDerivationIdentity.primitives"
        ".componentFrameOccurrencesMeasuredHere",
        _get(doc, ["policyDerivationIdentity", "primitives",
                   "componentFrameOccurrencesMeasuredHere"]),
        str(EXPECT_COMPONENT_FRAME_OCCURRENCES))
    if occurrences != EXPECT_COMPONENT_FRAME_OCCURRENCES:
        _add(findings, "R1V16-EP8", "EP8",
             f"componentFrame occurs {occurrences} times in live EP8; "
             f"{EXPECT_COMPONENT_FRAME_OCCURRENCES} is expected")

    clauses = _ep8_clauses(ep8)
    if len(clauses) != EXPECT_EP8_CLAUSES:
        _add(findings, "R1V16-EP8", "EP8",
             f"the mechanical clause enumeration yields {len(clauses)} "
             f"clauses; {EXPECT_EP8_CLAUSES} is expected")
    node = _get(doc, ["policyDerivationIdentity", "declaredDepartures"], {})
    where = "$.policyDerivationIdentity.declaredDepartures"
    classification = node.get("fullClassification")
    if not isinstance(classification, dict):
        _add(findings, "R1V16-TYPE", f"{where}.fullClassification",
             f"declared object, found {json_type(classification)}")
        return
    missing = sorted(set(clauses) - set(classification))
    extra = sorted(set(classification) - set(clauses))
    for clause in missing:
        _add(findings, "R1V16-EP8", f"{where}.fullClassification",
             f"live EP8 clause {clause!r} is not classified; a silently "
             f"dropped clause looks identical to a forgotten one")
    for clause in extra:
        _add(findings, "R1V16-EP8", f"{where}.fullClassification",
             f"{clause!r} is classified but is not a live EP8 clause")
    _eq(findings, "R1V16-EP8", f"{where}.clausesEnumerated",
        node.get("clausesEnumerated"), str(EXPECT_EP8_CLAUSES))
    _eq(findings, "R1V16-EP8", f"{where}.clausesClassified",
        node.get("clausesClassified"), str(EXPECT_EP8_CLAUSES))
    _eq(findings, "R1V16-EP8", f"{where}.silentlyDropped",
        node.get("silentlyDropped"), "0")
    for key in ("unclassifiedClauses", "classifiedButNotPresent"):
        value = node.get(key)
        if not isinstance(value, list):
            _add(findings, "R1V16-TYPE", f"{where}.{key}",
                 f"declared array, found {json_type(value)}")
        elif value:
            _add(findings, "R1V16-EP8", f"{where}.{key}",
                 f"declared empty; carries {len(value)} member(s)")
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.ep8ClausesClassified",
        _get(doc, ["measuredSelfReport", "ep8ClausesClassified"]),
        f"{EXPECT_EP8_CLAUSES} of {EXPECT_EP8_CLAUSES} enumerated")
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.componentFrameOccurrencesInEP8",
        _get(doc, ["measuredSelfReport", "componentFrameOccurrencesInEP8"]),
        str(EXPECT_COMPONENT_FRAME_OCCURRENCES))
    _eq(findings, "R1V16-SELFREPORT",
        "$.measuredSelfReport.ep8DomainListMembers",
        _get(doc, ["measuredSelfReport", "ep8DomainListMembers"]),
        f"{EXPECT_EP8_DOMAINS} -- NOT EXTENDED")


def check_self_report(doc: Any, c2v4: Any, findings: list[str]) -> None:
    report = doc.get("measuredSelfReport")
    if not isinstance(report, dict):
        return
    for key, expected in (
            ("pinnedVectors", str(EXPECT_PINNED_VECTORS)),
            ("maxTextComponentBytesAcrossAllVectors",
             str(EXPECT_MAX_TEXT_BYTES)),
            ("v15PositiveVectorCount", str(EXPECT_POSITIVE_VECTORS)),
            ("v15VectorsDeclaringExpectProjectionEqualTo",
             str(EXPECT_PROJECTION_EQUAL_DECLARERS)),
            ("v15DistinctDerivationDigestPlaceholders",
             str(EXPECT_PLACEHOLDER_VALUES)),
            ("v15PositionsCarryingOne", str(EXPECT_PLACEHOLDER_POSITIONS)),
            ("v15VectorsSharingOneStageInputAndDeps",
             f"{EXPECT_POSITIVE_VECTORS} of {EXPECT_POSITIVE_VECTORS}"),
            ("c2PlanIntentCommitmentPinnedFixtures",
             str(EXPECT_C2V4_PINNED_FIXTURES)),
            ("encoderDisagreements", "0"),
            ("ep8FramingGateFailures", "0")):
        _eq(findings, "R1V16-SELFREPORT", f"$.measuredSelfReport.{key}",
            report.get(key), expected)
    fixtures = c2v4.get("planIntentFixtures")
    measured = (sum(1 for row in fixtures
                    if isinstance(row, dict) and "expectedCommitment" in row)
                if isinstance(fixtures, list) else None)
    if measured != EXPECT_C2V4_PINNED_FIXTURES:
        _add(findings, "R1V16-SELFREPORT",
             "c2-plan-stage-schema.v4 $.planIntentFixtures",
             f"the standard being matched carries {measured} fixtures with an "
             f"expectedCommitment; {EXPECT_C2V4_PINNED_FIXTURES} is expected")
    cross = report.get("shasumCrossCheck")
    if not isinstance(cross, dict):
        _add(findings, "R1V16-TYPE", "$.measuredSelfReport.shasumCrossCheck",
             f"declared object, found {json_type(cross)}")
    else:
        _eq(findings, "R1V16-SELFREPORT",
            "$.measuredSelfReport.shasumCrossCheck.mismatches",
            cross.get("mismatches"), "0")
        examples = cross.get("mismatchExamples")
        if not isinstance(examples, list) or examples:
            _add(findings, "R1V16-SELFREPORT",
                 "$.measuredSelfReport.shasumCrossCheck.mismatchExamples",
                 "declared an empty array")
    _eq(findings, "R1V16-SELFREPORT", "$.parseDiscipline.duplicateKeysFound",
        _get(doc, ["parseDiscipline", "duplicateKeysFound"]), "0")
    # The section's own environment statement, which this instrument shares.
    _eq(findings, "R1V16-SELFREPORT", "$.environment.thirdPartyPackages",
        _get(doc, ["environment", "thirdPartyPackages"]), "none")
    _eq(findings, "R1V16-SELFREPORT", "$.environment.network",
        _get(doc, ["environment", "network"]), "none")


def check_binding_disclaimer(doc: Any, findings: list[str]) -> None:
    """Writing an instrument does not apply a candidate.  If the artifact ever
    starts claiming otherwise, that is a finding here."""
    node = doc.get("bindingDisclaimer")
    if not isinstance(node, dict):
        _add(findings, "R1V16-TYPE", "$.bindingDisclaimer",
             f"declared object, found {json_type(node)}")
        return
    _eq(findings, "R1V16-POSTURE", "$.bindingDisclaimer.binds",
        node.get("binds"),
        "NOTHING. This file is CANDIDATE-NOT-APPLIED and "
        "AWAITING-INDEPENDENT-REVIEW.")
    boundary = _get(doc, ["authorityBoundary", "notAuthorityFor"])
    if not isinstance(boundary, list) or not boundary:
        _add(findings, "R1V16-POSTURE", "$.authorityBoundary.notAuthorityFor",
             "declared a non-empty array")


def check(doc: Any, v15: Any, ep8: Any, c2v4: Any) -> list[str]:
    findings: list[str] = []
    try:
        if not isinstance(doc, dict):
            _add(findings, "R1V16-TOPLEVEL-TYPE", "$",
                 f"the subject must be a JSON object, found "
                 f"{json_type(doc)}")
            return findings
        check_posture(doc, findings)
        check_binding_disclaimer(doc, findings)
        check_frozen_inputs(doc, findings)
        check_predecessor(doc, findings)
        check_carry(doc, v15, findings)
        check_law_eighteen(doc, findings)
        check_recipe_declaration(doc, findings)
        recomputed = check_vectors(doc, findings)
        check_roundtrip(doc, recomputed, findings)
        check_enumerated_injectivity(findings)
        check_falsifier(doc, recomputed, findings)
        check_order_rulings(doc, v15, recomputed, findings)
        check_rejection_controls(doc, recomputed, findings)
        check_decoder_probes(doc, recomputed, findings)
        check_field_set_rule(doc, v15, recomputed, findings)
        check_separation(doc, v15, recomputed, findings)
        check_worked_example(doc, v15, recomputed, findings)
        check_ep8(doc, ep8, findings)
        check_self_report(doc, c2v4, findings)
    except Exception as exc:  # total checker boundary
        _add(findings, "R1V16-TOTALITY-EXCEPTION", "$",
             f"{type(exc).__name__}: {exc}")
    return findings


# ---------------------------------------------------------------------------
# Section 9.  Selftest.  Every mutation is APPLIED and EXECUTED and must
# produce the finding code it names.  Reporting a count is not running them.
# ---------------------------------------------------------------------------
def _set(parts: list[Any], value: Any) -> Callable[[Any], None]:
    def apply(node: Any) -> None:
        cur = node
        for part in parts[:-1]:
            cur = cur[part]
        cur[parts[-1]] = value
    return apply


def _del(parts: list[Any]) -> Callable[[Any], None]:
    def apply(node: Any) -> None:
        cur = node
        for part in parts[:-1]:
            cur = cur[part]
        del cur[parts[-1]]
    return apply


PDI = "policyDerivationIdentity"


def _mutations() -> list[tuple[str, str, Callable[[Any], None]]]:
    return [
        # --- the ordering channel -------------------------------------------
        ("M01-planStageIds-reversed", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 0, "recordValue",
               "planStageIds"], ["stage:policy", "stage:rules"])),
        ("M02-exactCoverage-mis-ordered", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 0, "recordValue",
               "exactCoverage"],
              [{"coverageKey": "coverage:rule", "state": "satisfied"},
               {"coverageKey": "coverage:policy", "state": "satisfied"}])),
        ("M03-rules-mis-ordered", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 15, "recordValue", "rules"],
              [{"ruleId": "rule:b", "artifactDigest": "sha256:" + "2" * 64},
               {"ruleId": "rule:aa", "artifactDigest": "sha256:" + "1" * 64}])),
        ("M04-ruling-becomes-set", "R1V16-ORDER-RULING",
         _set([PDI, "orderingRuling", "planStageIds", "ruling"],
              "SET. Order is not semantic.")),
        ("M05-orderRule-quote-drift", "R1V16-ORDER-RULING",
         _set([PDI, "orderingRuling", "rules_findings_exactCoverage",
               "orderRulesQuoted", "rules"], "any order")),
        # --- law 18 channels -------------------------------------------------
        ("M06-text-position-as-integer", "R1V16-TYPE",
         _set([PDI, "pinnedVectors", "vectors", 0, "recordValue",
               "targetUniverseId"], 7)),
        ("M07-text-position-as-boolean", "R1V16-TYPE",
         _set([PDI, "pinnedVectors", "vectors", 0, "recordValue",
               "targetUniverseId"], True)),
        ("M08-count-as-integer", "R1V16-TYPE",
         _set([PDI, "pinnedVectors", "count"], 17)),
        ("M09-count-as-float-shaped-int", "R1V16-TYPE",
         _set([PDI, "rejectionControls", "count"], 15)),
        ("M10-record-value-as-array", "R1V16-TYPE",
         _set([PDI, "workedExample", "derivationInputRecord"], [])),
        # --- arithmetic ------------------------------------------------------
        ("M11-digest-drift", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 1, "derivationDigest"],
              "sha256:" + "0" * 64)),
        ("M12-recordBytes-drift", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 2, "recordBytes"], "999")),
        ("M13-leafRoot-drift", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 3, "leafRootHex"], "00" * 32)),
        ("M14-outerPreimage-drift", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 4, "outerPreimageHex"], "3031")),
        ("M15-completeRecordHex-drift", "R1V16-VECTOR",
         _set([PDI, "pinnedVectors", "vectors", 16, "completeRecordHex"],
              "8081")),
        ("M16-vector-dropped", "R1V16-VECTOR",
         _del([PDI, "pinnedVectors", "vectors", 16])),
        # --- the falsifier ---------------------------------------------------
        ("M17-set-reading-digest-drift", "R1V16-FALSIFIER",
         _set([PDI, "orderingRuling", "exhibitA_planStageIdsSequenceVsSet",
               "underTheREJECTEDSetReading", "documentB"],
              "sha256:" + "0" * 64)),
        ("M18-falsifier-record-length", "R1V16-FALSIFIER",
         _set([PDI, "orderingRuling", "exhibitA_planStageIdsSequenceVsSet",
               "documentB", "recordBytes"], "555")),
        ("M19-falsifier-collide-denied", "R1V16-FALSIFIER",
         _set([PDI, "orderingRuling", "exhibitA_planStageIdsSequenceVsSet",
               "underTheREJECTEDSetReading", "collide"], "NO")),
        ("M20-exhibitB-length-major-drift", "R1V16-FALSIFIER",
         _set([PDI, "orderingRuling", "exhibitB_keyMajorVersusLengthMajor",
               "onRules", "digestIfEP8sSortedListsWereApplied"],
              "sha256:" + "0" * 64)),
        # --- guards ----------------------------------------------------------
        ("M21-rejection-message-drift", "R1V16-REJ",
         _set([PDI, "rejectionControls", "controls", 7, "encoderA"],
              "ValueError: something happened")),
        ("M22-rejection-both-denied", "R1V16-REJ",
         _set([PDI, "rejectionControls", "controls", 5, "bothReject"], "NO")),
        ("M23-rejection-dropped", "R1V16-REJ",
         _del([PDI, "rejectionControls", "controls", 14])),
        ("M24-decoder-probe-outcome-drift", "R1V16-DECODER-PROBE",
         _set([PDI, "decoderProbes", 0, "outcome"], "ValueError: nope")),
        ("M25-decoder-probe-dropped", "R1V16-DECODER-PROBE",
         _del([PDI, "decoderProbes", 5])),
        # --- equivalence, separation, worked example -------------------------
        ("M26-equivalence-digest-drift", "R1V16-EQ",
         _set([PDI, "equivalenceControls", "controls", 2, "derivationDigest"],
              "sha256:" + "0" * 64)),
        ("M27-equivalence-override-drift", "R1V16-EQ",
         _set([PDI, "equivalenceControls", "controls", 0, "v15Overrides"],
              {"attempt.executionId": "execution:two"})),
        ("M28-separation-identity-drift", "R1V16-SEP",
         _set([PDI, "separationControls", "controls", 4, "derivationDigest"],
              "sha256:" + "0" * 64)),
        ("M29-separator-claims-equality", "R1V16-SEP",
         _set([PDI, "separationControls", "controls", 2, "equalsPDD01"],
              "YES")),
        ("M30-oracle-prefix-bytes-drift", "R1V16-SEP",
         _set([PDI, "separationControls", "conformanceOracleNonCollision",
               "oraclePreimageFirstTwoBytesHex"], "3031")),
        ("M31-worked-example-placeholder", "R1V16-WORKED",
         _set([PDI, "workedExample", "completion", "policyOutcome",
               "derivationDigest"], "sha256:" + "5" * 64)),
        ("M32-migration-table-drift", "R1V16-WORKED",
         _set([PDI, "relationToTheCarriedPositiveVectors", "migrationTable", 0,
               "valueThisRuleProduces"], "sha256:" + "0" * 64)),
        # --- namespace, domain, grammar --------------------------------------
        ("M33-namespace-repointed", "R1V16-RECIPE",
         _set([PDI, "namespaceAndDomainSeparator", "namespace"],
              "opensip.evaluation-proof.v2")),
        ("M34-domain-repointed", "R1V16-RECIPE",
         _set([PDI, "namespaceAndDomainSeparator", "domain"], "verdict-input")),
        ("M35-leaf-rule-rewritten", "R1V16-RECIPE",
         _set([PDI, "primitives", "leaf"], "leafHash(r) = SHA-256(r)")),
        ("M36-field-tag-moved", "R1V16-GRAMMAR",
         _set([PDI, "recordGrammar", "PolicyDerivationInputV1", "fields", 6,
               "tag"], "0x92")),
        ("M37-nested-record-tag-moved", "R1V16-GRAMMAR",
         _set([PDI, "recordGrammar", "RuleValueV1", "recordTag"], "0xa5")),
        # --- EP8 transcription ------------------------------------------------
        ("M38-clause-dropped", "R1V16-EP8",
         _del([PDI, "declaredDepartures", "fullClassification",
               "normativePreimageGrammar.recordRules.sortedLists"])),
        ("M39-clause-count-drift", "R1V16-EP8",
         _set([PDI, "declaredDepartures", "clausesEnumerated"], "43")),
        ("M40-silently-dropped-admitted", "R1V16-EP8",
         _set([PDI, "declaredDepartures", "silentlyDropped"], "2")),
        # --- injectivity, round-trip ------------------------------------------
        ("M41-roundtrip-count-drift", "R1V16-ROUNDTRIP",
         _set([PDI, "injectivityByExhibitedTotalDecoder",
               "recordsRoundTripped"], "20")),
        ("M42-roundtrip-passing-drift", "R1V16-ROUNDTRIP",
         _set([PDI, "injectivityByExhibitedTotalDecoder",
               "literalRoundTripsPassing"], "20")),
        # --- posture, pins, carry ---------------------------------------------
        ("M43-status-applied", "R1V16-POSTURE", _set(["status"], "APPLIED")),
        ("M44-review-pass", "R1V16-POSTURE",
         _set(["reviewStatus"], "PASS")),
        ("M45-seal-recommended", "R1V16-POSTURE",
         _set(["sealRecommendation"], "SEAL")),
        ("M46-binds-something", "R1V16-POSTURE",
         _set(["binds"], "THE IMPLEMENTATION")),
        ("M47-grade-demonstrated", "R1V16-POSTURE",
         _set(["evidenceGrade"], "DEMONSTRATED")),
        ("M48-unset-token", "R1V16-POSTURE",
         _set([PDI, "pinnedVectors", "standardBeingMatched"], "[UNSET]")),
        ("M49-pin-drift", "R1V16-PIN",
         _set(["frozenInputs", 0, "sha256"], "0" * 64)),
        ("M50-predecessor-drift", "R1V16-PREDECESSOR",
         _set(["predecessor", "sha256"], "0" * 64)),
        ("M51-archplan-drift", "R1V16-PREDECESSOR",
         _set(["measuredSelfReport", "archPlanSha256AtEmit"], "0" * 64)),
        ("M52-checker-digest-drift", "R1V16-PREDECESSOR",
         _set(["measuredSelfReport", "checkerSha256AtEmit_readOnly"],
              "0" * 64)),
        ("M53-carried-type-added", "R1V16-CARRY",
         _set(["closedTypes", "Injected"], {"kind": "string",
                                            "pattern": "^x$"})),
        ("M54-placeholder-replaced", "R1V16-CARRY",
         _set(["positiveVectors", 0, "expectedCompletion", "policyOutcome",
               "derivationDigest"],
              "sha256:567284c2b1bff1b5c2c502f49147033d19be83b07888b80574da35"
              "e179dd3cf4")),
        ("M55-carry-claim-denied", "R1V16-CARRY",
         _set(["preservationOfV15", "allCarriedKeysIdentical"], "NO")),
        ("M56-residual-prefix-edited", "R1V16-CARRY",
         _set(["residuals", 0, "state"], "CLOSED")),
        ("M57-review-request-prefix-edited", "R1V16-CARRY",
         _set(["reviewRequests", 0], "nothing to review")),
        # --- self-report -------------------------------------------------------
        ("M58-selfreport-frame-count", "R1V16-SELFREPORT",
         _set(["measuredSelfReport", "componentFrameOccurrencesInEP8"], "49")),
        ("M59-selfreport-roundtrip", "R1V16-SELFREPORT",
         _set(["measuredSelfReport", "recordsLiterallyRoundTripped"],
              "20 of 21")),
        ("M60-selfreport-c2-standard", "R1V16-SELFREPORT",
         _set(["measuredSelfReport", "c2PlanIntentCommitmentPinnedFixtures"],
              "8")),
        ("M61-fieldset-override-widened", "R1V16-FIELDSET", None),
        ("M62-disclaimer-binds", "R1V16-POSTURE",
         _set(["bindingDisclaimer", "binds"], "the implementation")),
    ]


def _apply_special(mutation_id: str, doc: Any, v15: Any) -> Any:
    """M61 mutates the LIVE-PREDECESSOR side, so it needs its own applier."""
    if mutation_id == "M61-fieldset-override-widened":
        mutated = copy.deepcopy(v15)
        mutated["positiveVectors"][8]["overrides"]["stageInput.targetUniverseId"] = \
            "universe:nine"
        return mutated
    return v15


PARSER_CASES = [
    ("duplicate-top", '{"a":1,"a":2}', "R1V16-JSON-DUPLICATE", "'a'"),
    ("duplicate-nested", '{"a":{"bb":1,"bb":2}}', "R1V16-JSON-DUPLICATE", "'bb'"),
    ("duplicate-in-array", '[{"cc":1,"cc":2}]', "R1V16-JSON-DUPLICATE", "'cc'"),
    ("nan", '{"a":NaN}', "R1V16-JSON-NONFINITE", "NaN"),
    ("infinity", '{"a":Infinity}', "R1V16-JSON-NONFINITE", "Infinity"),
    ("negative-infinity", '{"a":-Infinity}', "R1V16-JSON-NONFINITE", "-Infinity"),
    ("decimal", '{"a":1.0}', "R1V16-JSON-FLOAT", "1.0"),
    ("exponent", '{"a":1e0}', "R1V16-JSON-FLOAT", "1e0"),
]

HOSTILE = [None, True, 0, "subject", [], {}, {"artifact": None},
           {"closedTypes": []}, {"policyDerivationIdentity": []},
           {"policyDerivationIdentity": {"pinnedVectors": {"vectors": [None]}}},
           {"frozenInputs": "x"}, {"preservationOfV15": {"carriedKeys": [1]}}]


def selftest(doc: Any, v15: Any, ep8: Any, c2v4: Any,
             original: bytes) -> tuple[list[str], int, int, int]:
    escapes: list[str] = []
    base = check(doc, v15, ep8, c2v4)
    if base:
        return (["SELFTEST-REFUSED: the unmutated base has "
                 f"{len(base)} finding(s), so mutation results would be "
                 f"meaningless"] + base, 0, 0, 0)

    mutations = _mutations()
    ids = [item[0] for item in mutations]
    if len(ids) != len(set(ids)):
        return ["SELFTEST-ESCAPE: duplicate mutation id"], 0, 0, 0
    applied = 0
    for mutation_id, expected_code, fn in mutations:
        candidate = copy.deepcopy(doc)
        peer = _apply_special(mutation_id, candidate, v15)
        if fn is not None:
            try:
                fn(candidate)
            except Exception as exc:  # noqa: BLE001
                escapes.append(
                    f"SELFTEST-ESCAPE {mutation_id}: could not apply: "
                    f"{type(exc).__name__}: {exc}")
                continue
            if canon(candidate) == canon(doc):
                escapes.append(f"SELFTEST-ESCAPE {mutation_id}: no-op")
                continue
        elif canon(peer) == canon(v15):
            escapes.append(f"SELFTEST-ESCAPE {mutation_id}: no-op")
            continue
        applied += 1
        result = check(candidate, peer, ep8, c2v4)
        if not result:
            escapes.append(
                f"SELFTEST-ESCAPE {mutation_id}: the mutation PASSED")
        elif expected_code not in _codes(result):
            escapes.append(
                f"SELFTEST-ESCAPE {mutation_id}: expected {expected_code}; got "
                f"{sorted(_codes(result))}")
    if applied != len(mutations):
        escapes.append(
            f"SELFTEST-ESCAPE: {len(mutations) - applied} mutation(s) never ran")

    for case_id, raw, expected_code, named in PARSER_CASES:
        try:
            strict_loads(raw)
        except StrictJsonError as exc:
            if exc.code != expected_code:
                escapes.append(
                    f"SELFTEST-ESCAPE parser {case_id}: {exc.code} != "
                    f"{expected_code}")
            elif named not in str(exc):
                escapes.append(
                    f"SELFTEST-ESCAPE parser {case_id}: the refusal does not "
                    f"NAME {named}: {exc}")
        else:
            escapes.append(f"SELFTEST-ESCAPE parser {case_id}: accepted")

    for index, value in enumerate(HOSTILE):
        try:
            result = check(value, v15, ep8, c2v4)
        except Exception as exc:  # noqa: BLE001
            escapes.append(
                f"SELFTEST-ESCAPE totality[{index}]: raised "
                f"{type(exc).__name__}: {exc}")
            continue
        if not result:
            escapes.append(f"SELFTEST-ESCAPE totality[{index}]: no finding")

    try:
        final = (REPO / SUBJECT_PATH).read_bytes()
    except OSError as exc:
        escapes.append(f"SELFTEST-ESCAPE: cannot re-read the subject: {exc}")
    else:
        if final != original:
            escapes.append(
                "SELFTEST-ESCAPE: the subject changed during the selftest")
    return escapes, applied, len(PARSER_CASES), len(HOSTILE)


# ---------------------------------------------------------------------------
# Section 10.  Entry.
# ---------------------------------------------------------------------------
def _usage() -> None:
    sys.stderr.write(
        "usage: python3 -I -B check-r1-v1.6.py [--selftest]\n"
        "       python3 -I -B check-r1-v1.6.py --subject PATH\n")


def main(argv: list[str]) -> int:
    do_selftest = False
    subject_override: str | None = None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--selftest":
            do_selftest = True
        elif arg == "--subject":
            index += 1
            if index >= len(argv):
                sys.stderr.write(
                    "R1V16-UNSUPPORTED-INVOCATION: --subject takes a path\n")
                return 2
            subject_override = argv[index]
        else:
            sys.stderr.write(
                f"R1V16-UNSUPPORTED-INVOCATION: unknown option {arg!r}\n")
            _usage()
            return 2
        index += 1
    if do_selftest and subject_override is not None:
        sys.stderr.write(
            "R1V16-UNSUPPORTED-INVOCATION: --selftest runs against the pinned "
            "subject only\n")
        return 2

    # INERT BYTES FIRST.  Nothing below this point runs if a pinned input moved.
    try:
        snaps = verified_snapshots()
    except PinRefusal as exc:
        sys.stderr.write(
            f"R1V16-PIN-REFUSED: a pinned input did not match its digest, so "
            f"nothing was decoded, parsed or executed: {exc}\n")
        return 2

    if subject_override is None:
        subject_bytes = snaps[SUBJECT_PATH]
        subject_name = SUBJECT
    else:
        try:
            subject_bytes = pathlib.Path(subject_override).read_bytes()
        except OSError as exc:
            sys.stderr.write(
                f"R1V16-UNSUPPORTED-INVOCATION: cannot read "
                f"{subject_override}: {type(exc).__name__}: {exc}\n")
            return 2
        subject_name = subject_override

    try:
        doc = strict_parse(subject_bytes, subject_name)
        v15 = strict_parse(snaps[V15_PATH], V15_PATH)
        ep8 = lenient_parse(snaps[EP8_PATH], EP8_PATH)
        c2v4 = lenient_parse(snaps[C2V4_PATH], C2V4_PATH)
    except PinRefusal as exc:
        sys.stderr.write(f"R1V16-PARSE-REFUSED: {exc}\n")
        return 2 if subject_override is None else 4

    if do_selftest:
        escapes, mutations, parsers, hostiles = selftest(
            doc, v15, ep8, c2v4, subject_bytes)
        if escapes and escapes[0].startswith("SELFTEST-REFUSED"):
            for line in escapes:
                print(line)
            print("R1 v1.6 selftest: NOT RUN (the base was not clean)")
            return 3
        if escapes:
            for line in escapes:
                print(line)
            print(f"R1 v1.6 selftest: FAIL ({len(escapes)} escapes)")
            return 1
        print(f"R1 v1.6 selftest: PASS ({mutations} mutations APPLIED and "
              f"EXECUTED, {parsers} raw parser probes each naming its token, "
              f"{hostiles} hostile totality shapes)")
        return 0

    findings = check(doc, v15, ep8, c2v4)

    if subject_override is not None:
        digest = hashlib.sha256(subject_bytes).hexdigest()
        print(f"R1V16-DIAGNOSTIC: {subject_name}")
        print(f"R1V16-DIAGNOSTIC: sha256 {digest}")
        print("R1V16-DIAGNOSTIC: the subject pin was NOT enforced; this run is "
              "not a verdict")
        if findings:
            print(f"{len(findings)} finding(s):")
            for item in findings:
                print("  -", item)
        else:
            print("0 findings")
        return 4

    if findings:
        print(f"{len(findings)} finding(s) in {SUBJECT}:")
        for item in findings:
            print("  -", item)
        return 1

    print(f"{SUBJECT}: PASS")
    print(f"  subject sha256 {PINS[SUBJECT_PATH]}, verified before parsing")
    print(f"  predecessor v1.5 {PINS[V15_PATH]} UNTOUCHED; "
          f"check-r1-v1.5.py read-only at {PINS[V15_CHECKER_PATH]}")
    print(f"  ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md "
          f"{PINS[ARCH_PLAN_PATH]}, hashed only, never opened")
    print(f"  {EXPECT_PINNED_VECTORS} vectors recomputed on every published "
          f"field by TWO independent encoders, 0 disagreements")
    print(f"  {EXPECT_ROUNDTRIP_RECORDS} records literally round-tripped; "
          f"{EXPECT_ENUMERATED_VALUES} enumerated values -> "
          f"{EXPECT_ENUMERATED_VALUES} distinct encodings, 0 collisions")
    print(f"  the 554-byte falsifier EXECUTED: the rejected set reading "
          f"collides on PDD-01's own digest")
    print(f"  {EXPECT_REJECTIONS} rejection controls and "
          f"{EXPECT_DECODER_PROBES} decoder probes EXECUTED, each on the "
          f"condition it names")
    print(f"  {EXPECT_EQUIVALENCE} equivalence controls rebuilt from live "
          f"v1.5; {EXPECT_SEPARATION} separation controls recomputed")
    print(f"  {EXPECT_EP8_CLAUSES} live EP8 clauses classified in both "
          f"directions; EP8's {EXPECT_EP8_DOMAINS}-member domain list "
          f"unextended")
    for line in declared_mobile_drift(doc):
        print(f"  DECLARED-MOBILE DRIFT (recorded, not absorbed; not read by "
              f"this instrument): {line}")
    print("  STATUS UNCHANGED: CANDIDATE-NOT-APPLIED / binds NOTHING / "
          "DO-NOT-SEAL.  A green run is bounded author-side evidence; it is "
          "not acceptance, application, seal or qualification, and it closes "
          "no row.")
    print(f"  NOT verified by this instrument ({len(NOT_VERIFIED)} items; see "
          f"NOT_VERIFIED in this source)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
