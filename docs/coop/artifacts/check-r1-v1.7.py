#!/usr/bin/env python3
"""Retained checker for r1-lifetime-neutrality.conformance.v1.6.json.

Successor to check-r1-v1.6.py, which is PINNED by its own independent review
(ACCEPT_WITH_BLOCKERS, blocker CIR-B1) and is therefore not edited here.
IMPLEMENTATION-FREEZE.md section 7.2 forbids editing a reviewed instrument;
section 7.6 forbids editing the pinned check-r1-v1.5.py.  Neither constraint
reaches a NEW file.  This is that file.  It edits nothing, it repoints no head,
it closes no row, it changes no status, and writing it does not apply the
candidate.  The subject bytes are IDENTICAL to the ones v1.6 was reviewed on.

WHY THIS FILE EXISTS -- the blocker, stated before anything else.

  CIR-B1: published corpora were never required to be non-degenerate.

  Measured against the predecessor, from an external driver importing it
  unmodified: collapsing eleven of the seventeen published vectors onto
  PDD-01's recordValue and republishing every dependent digest WITH THE
  PREDECESSOR'S OWN ENCODER yields twelve of seventeen vectors byte-identical
  to PDD-01, sharing ONE derivationDigest, at ZERO findings.  Neutralising any
  single inclusion control escapes.  A malformed `sha856:` prefix escapes.  A
  well-formed-but-wrong digest escapes.  A semantically inverted `models`
  claim escapes.

  The shape of the defect: the predecessor demanded that 720 SYNTHETIC values
  be distinct and demanded NOTHING of the 17 PUBLISHED ones.  Its strongest
  evidence -- the enumerated distinctness sweep -- was aimed away from the
  corpus it was certifying.  A vector that only has to hash consistently is
  not a vector.

WHAT THIS INSTRUMENT DOES ABOUT IT, in the order the checks run:

  0  Integrity.   Every input is read as inert bytes, hashed, and compared
                  against a digest pinned in THIS source BEFORE any of it is
                  decoded or parsed.  A mismatch prints one named refusal and
                  exits 2.
  1  Posture.     status, reviewStatus, binds, sealRecommendation and
                  evidenceGrade are the reviewed values.  A checker that would
                  stay green across `status: APPLIED` measures nothing.
  2  Closure.     All seventeen frozenInputs rows are verified against live
                  bytes.  Exactly two coordinator-owned prose documents are
                  DECLARED MOBILE and may move; drift on any other row is a
                  refusal.  NEW: the two mobile rows' RECORDED digests are no
                  longer unanchored -- each must equal, character for
                  character, the finalisation digest named in the artifact's
                  independently-written driftDisclosure prose, must be a
                  well-formed 64-hex value, must differ from the read-time
                  digest of its own disclosed pair, and the live value is
                  measured and printed.  The four digests the same disclosure
                  says did NOT move are hard-compared against live bytes.
  3  Carry.       Every key v1.6 claims to carry from v1.5 is compared
                  canonically against LIVE v1.5 bytes.
  4  Law 18.      Exact-type scalar admission over every leaf of
                  $.policyDerivationIdentity and over every recordValue before
                  a single byte of it is encoded.
  5  RECIPE, DERIVED.  NEW.  The predecessor conceded that its TOP_FIELDS,
                  tags, namespace and domain "were derived by reading v1.6"
                  and then hand-typed, so it tested its own transcription.
                  Here NOTHING of the recipe is hand-typed.  The framing tags
                  are PARSED OUT OF LIVE evaluation-proof.v8 CLAUSE TEXT.  The
                  text admission bound is parsed out of the EP8 sentence the
                  artifact quotes, after that sentence is confirmed to occur
                  verbatim in live EP8 bytes.  The record grammar, field
                  order, tags and shapes are DERIVED from the artifact's own
                  recordGrammar and then cross-checked four ways: tag
                  assignment is structurally re-derived, every nested record's
                  field order is compared against LIVE v1.5 closedTypes
                  through the artifact's own `mirrors` pointer, every leaf's
                  TYPE is resolved through LIVE v1.5's closed type graph, and
                  the three content orderRules are PARSED out of LIVE v1.5
                  orderRule sentences.  The admissible variant set is derived
                  from LIVE v1.5's projectionByVariant.  A derived recipe that
                  is wrong cannot simultaneously reproduce seventeen published
                  digests, the records rebuilt from live v1.5, and EP8's
                  clauses.
  6  Arithmetic.  Every published digest is RECOMPUTED from the recordValue by
                  TWO independently written encoders -- one table-driven, one
                  flat imperative with hand-rolled big-endian -- both driven by
                  the DERIVED recipe, sharing no helper, and compared against
                  each other and against the artifact.
  7  CORPUS DERIVATION.  NEW -- this is the CIR-B1 fix.  No published
                  recordValue is taken as given.  All seventeen are REBUILT:
                    * PDD-01..PDD-04 by applying the fieldSetRule to LIVE v1.5
                      vectors, resolving cloneOf and overrides;
                    * PDD-05..PDD-17 from the REBUILT PDD-01 by a derivation
                      DECLARED in this source -- a small algebra of swap,
                      reverse, copy-from-basis, append and generated-digest
                      operations -- so that most perturbed values are COMPUTED
                      from the basis rather than transcribed at all.
                  The rebuilt value is compared byte-for-byte against the
                  published one.  A collapsed vector, a wrong digest, a
                  `sha856:` prefix and an arbitrary universe id all fail here
                  identically, because none of them is what the derivation
                  produces.  Additionally: every perturbation must actually
                  MOVE the basis; the measured leaf-difference set must equal
                  the DECLARED axis exactly; every perturbed value must be
                  admissible under LIVE v1.5's closed type for that leaf; and
                  the seventeen records, leaf roots and digests must be
                  pairwise DISTINCT.
  8  Semantics.   NEW.  Each control's `models` prose is cross-checked against
                  the axis it actually moves, in BOTH directions, using
                  designators derived from the artifact's own recordGrammar
                  `source` values and from LIVE v1.5 type names.  A control
                  whose prose names a field it does not move, or fails to name
                  the field it does move, is a finding.  Separately, the ONE
                  vector that violates live v1.5's `requiredKind` constraint is
                  MEASURED and required to be the one whose prose says so.
  9  Injectivity. A TOTAL grammar-directed decoder is exhibited over the
                  DERIVED recipe.  decode(encode(x)) == x is asserted LITERALLY
                  -- as canonical bytes -- on all 21 records, and
                  encode(decode(r)) == r on the same 21.  Beyond the published
                  corpus, 720 admissible values are enumerated and required to
                  produce 720 distinct encodings, 0 collisions, 720 literal
                  round-trips.
 10  Falsifier.   EXECUTED, not declared.  The rejected set reading is
                  implemented and RUN.  PDD-01 and PDD-17 must both be 554
                  bytes, distinct under the adopted sequence reading, and
                  COLLIDING under the set reading on a value required to be
                  PDD-01's own digest.
 11  Guards.      All 15 rejection controls EXECUTED against constructed
                  inputs, each raising on the condition it NAMES with the exact
                  published message, from BOTH encoders.  All 6 decoder probes
                  likewise.  NEW: seven WRONGNESS probes -- malformed digest
                  prefix, well-formed-but-wrong digest, out-of-vocabulary enum,
                  collapsed control, widened axis, inverted prose, republished
                  digest -- each required to be refused on a NAMED condition.
                  Every instrument in this lineage fired on REMOVAL and stayed
                  silent on FALSITY.
 12  Rulings.     planStageIds is SEQUENCE; the three content orderRules are
                  parsed from LIVE v1.5.  The encoder REJECTS a mis-ordered
                  list rather than repairing it -- executed, per list, against
                  the named condition.
 13  Separation.  Five (namespace, domain) pairs recomputed; five distinct
                  values; XD-5 reproduces PDD-01.  R-1's carried conformance
                  oracle prefix is taken from LIVE v1.5.
 14  Worked ex.   The complete CoreCompletion::completed carries a REAL
                  derivationDigest derived from the rule, not a placeholder.
 15  EP8.         Framing clauses compared verbatim against LIVE EP8 bytes; 44
                  grammar clauses enumerated mechanically and matched in BOTH
                  directions; the nine-member domain list required unextended.
 16  Self-report. Every recorded measurement gets a hard comparison.

What this instrument does NOT verify is stated in full at NOT_VERIFIED below,
in the source rather than in a report, because a limitation that lives only in
a report is not carried with the instrument.  CIR-B1's resolution status is a
member of that list.

Census counts are bound to constants declared in THIS file and are never sized
from the artifact.  IMPLEMENTATION-FREEZE 7.2.2's corollary, which defeated
B-VER9R-01: a partition sized from the artifact cannot police the artifact.
The RECIPE, by contrast, is derived and externally cross-checked -- the
distinction is that a count is a claim ABOUT the artifact while the recipe is a
claim the artifact makes that live neighbours can adjudicate.

No repository Python checker is imported or executed.  check-r1-v1.5.py and
check-r1-v1.6.py are read as inert bytes only, to confirm their digests.

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
    python3 -I -B docs/coop/artifacts/check-r1-v1.7.py [--selftest]
    python3 -I -B docs/coop/artifacts/check-r1-v1.7.py --subject PATH
"""

from __future__ import annotations

import sys

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "R1V17-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-r1-v1.7.py`.  Caller-owned isolated startup is the prevention "
        "boundary; script code cannot undo interpreter or site activity that "
        "happened before line 1.\n")
    raise SystemExit(2)

import binascii
import copy
import hashlib
import itertools
import json
import pathlib
import re
import struct
import unicodedata
from typing import Any, Callable

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent
REPO = COOP.parent.parent

SUBJECT = "r1-lifetime-neutrality.conformance.v1.6.json"

# ---------------------------------------------------------------------------
# Section 0.  Pinned execution closure.
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
    # HASHED ONLY.  Never opened, never decoded, never parsed.
    "docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md":
        "47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e",
    # Read as inert bytes only.  NOT imported.  NOT executed.  NOT edited.
    "docs/coop/artifacts/check-r1-v1.5.py":
        "79bd26785ab91c34e12a5f9cccc007a656d1598fea4c0e9f8674fd67114e6776",
    # The PINNED PREDECESSOR INSTRUMENT.  Freeze 7.2 pins it by its review.
    # Hashed here so that this successor refuses to run if the file it must
    # leave byte-identical has moved.  NOT imported.  NOT executed.
    "docs/coop/artifacts/check-r1-v1.6.py":
        "8bf980a961e90647313d802e5ded37d21f84b5f77045527220e58f56b012fa39",
}

SUBJECT_PATH = "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.6.json"
V15_PATH = "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.5.json"
EP8_PATH = "docs/coop/artifacts/evaluation-proof.v8.json"
C2V4_PATH = "docs/coop/artifacts/c2-plan-stage-schema.v4.json"
ARCH_PLAN_PATH = "docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md"
V15_CHECKER_PATH = "docs/coop/artifacts/check-r1-v1.5.py"
V16_CHECKER_PATH = "docs/coop/artifacts/check-r1-v1.6.py"

# The two coordinator-owned prose documents the artifact's own driftDisclosure
# names as having moved during its authoring.  They are the ONLY rows permitted
# to differ from their pin.  The permission is hard-coded HERE, never read from
# the artifact; the artifact's disclosure is separately required to name exactly
# these two; and -- unlike the predecessor -- their RECORDED digests are
# anchored against the disclosure prose rather than left unchecked.
DECLARED_MOBILE = {
    "docs/coop/IMPLEMENTATION-FREEZE.md",
    "docs/coop/IMPLEMENTER-BLUEPRINT.md",
}

# ---------------------------------------------------------------------------
# Section 1.  Census counts, bound OUTSIDE the artifact.  These are claims
# ABOUT the artifact and are never sized from it.  (The RECIPE is derived --
# see Section 5 -- because a recipe is a claim the artifact makes that live
# neighbours can adjudicate, which a count is not.)
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

# NEW census, all measured by this instrument rather than read from the file.
EXPECT_TOP_FIELDS = 12          # PolicyDerivationInputV1 declared fields
EXPECT_NESTED_TYPES = 4         # RuleValueV1 / PolicyValueV1 / FindingValueV1 / CoverageEntryV1
EXPECT_DERIVED_FROM_V15 = 4     # PDD-01..PDD-04, rebuilt from live v1.5
EXPECT_DERIVED_FROM_BASIS = 13  # PDD-05..PDD-17, rebuilt from the rebuilt PDD-01
EXPECT_EXTERNALLY_ANCHORED = 17 # every published vector.  The predecessor: 6.
EXPECT_WRONGNESS_PROBES = 7     # inputs that are WRONG, not merely EMPTY
EXPECT_REQUIREDKIND_VIOLATORS = 1  # exactly PDD-15, MEASURED against live v1.5

# The single declared carve-out in the mechanical EP8 clause enumeration: EP8's
# record-type table is a table of records, not a rule, and is counted once.
EP8_CLAUSE_AGGREGATES = {"normativePreimageGrammar.records"}

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
    "CIR-B1 RESOLUTION STATUS -- RESOLVED HERE, WITH A NAMED RESIDUAL.  All "
    "seventeen published vectors are now rebuilt rather than read back: four "
    "from LIVE v1.5 through the fieldSetRule, thirteen from the rebuilt PDD-01 "
    "through the derivation algebra declared in this source.  The escapes the "
    "predecessor's reviewer measured -- collapse, republish, malformed prefix, "
    "wrong digest, inverted prose -- are each executed here as a wrongness "
    "probe and each fails on a named condition.  THE RESIDUAL: the derivation "
    "algebra's non-computed operands -- the LITERAL leaves, whose count this "
    "instrument MEASURES and prints rather than asserting -- are DECLARED in "
    "this source.  They are constrained "
    "-- each must be admissible under live v1.5's closed type for its leaf, "
    "must differ from the basis value it replaces, and must land on the axis "
    "the artifact's own prose names -- but they are not DERIVED, and an "
    "instrument cannot prove that the author of a control chose the right "
    "arbitrary constant.  What is now impossible is for the artifact to change "
    "them unilaterally.",
    "evaluation-proof.v8's 69-assertion framing gate (12 record goldens and 9 "
    "commitment goldens re-encoded by a generic EP8-driven re-encoder).  This "
    "instrument verifies that the framing CLAUSES it PARSES read verbatim in "
    "live EP8 bytes and that the recipe reproduces every digest R-1 publishes; "
    "it does not re-run EP8's own goldens.",
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
    "arguments, not measurements, and no instrument can grade them.  The prose "
    "that DOES carry a checkable claim -- each control's `models` axis and the "
    "requiredKind note -- is measured at section 8 and is no longer in this "
    "list.",
    "Whether the field set is the RIGHT one.  v1.6 states plainly that nothing "
    "forces its inclusions and that it RULES them as the owning surface.  This "
    "instrument measures that the ruling is applied consistently, is "
    "vector-addressable, and that every declared inclusion is exercised by a "
    "control that actually moves it; it cannot measure that the ruling is "
    "correct.",
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
                "R1V17-JSON-DUPLICATE", f"duplicate object key {key!r}")
        out[key] = value
    return out


def _reject_float(token: str) -> Any:
    raise StrictJsonError("R1V17-JSON-FLOAT", f"JSON float forbidden: {token}")


def _reject_constant(token: str) -> Any:
    raise StrictJsonError("R1V17-JSON-NONFINITE",
                          f"non-finite forbidden: {token}")


def strict_loads(text: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_pairs,
                          parse_float=_reject_float,
                          parse_constant=_reject_constant)
    except StrictJsonError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise StrictJsonError("R1V17-JSON-SYNTAX", str(exc)) from exc


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
        elif (isinstance(cur, list) and isinstance(key, int)
              and -len(cur) <= key < len(cur)):
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
    return JSON_TYPE_NAMES.get(type(value).__name__, type(value).__name__)


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


def _iter_leaves(node: Any, prefix: str):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _iter_leaves(value, f"{prefix}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _iter_leaves(value, f"{prefix}[{index}]")
    else:
        yield prefix, node


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


# ---------------------------------------------------------------------------
# Section 4.  THE DERIVED RECIPE.
#
# Nothing below is hand-typed.  The predecessor conceded that its TOP_FIELDS,
# tags, namespace and domain "were derived by reading v1.6" and then written
# down as literals, which means it compared the artifact against a transcript
# of itself.  A sibling instrument was REJECTED for exactly that shape.
#
# Here the recipe is BUILT, at run time, from three sources, and every element
# is adjudicated by at least one source that is not the subject:
#
#   * the framing primitives -- component width, leaf tag and width, and the
#     four outer tags -- are PARSED OUT OF LIVE evaluation-proof.v8 CLAUSE
#     TEXT and only then compared against the artifact's statement of them;
#   * the text admission bound is parsed out of the EP8 sentence the artifact
#     quotes, AFTER that sentence is confirmed to occur verbatim in live EP8
#     bytes;
#   * the record grammar -- field names, order, tags, shapes, presence -- is
#     derived from the artifact's own recordGrammar and then cross-checked:
#     structurally (the tag assignment rule is re-derived and re-applied),
#     against LIVE v1.5 closedTypes through the artifact's own `mirrors`
#     pointers, and against LIVE v1.5's closed type graph for every leaf type;
#   * the three content orderRules are PARSED out of LIVE v1.5 orderRule
#     sentences, not transcribed;
#   * the admissible variant set is derived from LIVE v1.5's
#     evidenceIdentity.projectionByVariant -- the variants that carry a
#     policyOutcome, which is the only reason a derivationDigest exists.
#
# A derived recipe that is wrong cannot simultaneously reproduce seventeen
# published digests, the four records rebuilt from live v1.5, and EP8's own
# clause text.  That is what makes derivation safe here where a transcript is
# not: the derivation is over-determined.
# ---------------------------------------------------------------------------
TEXT = "text"


class RecipeError(ValueError):
    """A recipe element could not be derived.  Carries the position."""

    def __init__(self, where: str, detail: str) -> None:
        super().__init__(detail)
        self.where = where
        self.detail = detail


class TypeSpec:
    """A leaf's type, as resolved through LIVE v1.5's closed type graph."""

    __slots__ = ("name", "kind", "pattern", "values")

    def __init__(self, name: str, kind: str, pattern: str | None = None,
                 values: tuple[str, ...] = ()) -> None:
        self.name = name
        self.kind = kind          # "pattern" | "enum" | "const"
        self.pattern = pattern
        self.values = values

    def admits(self, value: Any) -> str | None:
        """Return None if admitted, else the NAMED condition that refused it."""
        if isinstance(value, bool) or not isinstance(value, str):
            return (f"declared {self.name}, which live v1.5 makes a string; "
                    f"found {json_type(value)}")
        if self.kind == "pattern":
            if re.fullmatch(self.pattern or "", value) is None:
                return (f"does not match live v1.5 closedTypes.{self.name}"
                        f".pattern {self.pattern!r}")
            return None
        if self.kind in ("enum", "const"):
            if value not in self.values:
                return (f"is not a member of live v1.5's closed {self.name} "
                        f"vocabulary {list(self.values)!r}")
            return None
        return f"has no resolvable type under live v1.5 ({self.kind})"


class Recipe:
    __slots__ = ("record_tag", "top", "nested", "namespace", "domain",
                 "leaf_tag", "outer_tags", "component_width", "leaf_width",
                 "text_max", "variants", "content_ordered", "leaf_types",
                 "field_source", "type_of_field", "notes")

    def __init__(self) -> None:
        self.record_tag: int = 0
        self.top: list[tuple[str, int, Any, str]] = []
        self.nested: dict[str, tuple[int, list[tuple[str, int]]]] = {}
        self.namespace: str = ""
        self.domain: str = ""
        self.leaf_tag: int = 0
        self.outer_tags: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.component_width: int = 0
        self.leaf_width: int = 0
        self.text_max: int = 0
        self.variants: tuple[str, ...] = ()
        self.content_ordered: dict[str, tuple[str, ...]] = {}
        # keyed by "" for a top field name, or by the nested type name
        self.leaf_types: dict[tuple[str, str], TypeSpec] = {}
        self.field_source: dict[str, str] = {}
        self.type_of_field: dict[str, str] = {}
        self.notes: list[str] = []

    @property
    def top_names(self) -> list[str]:
        return [name for name, _, _, _ in self.top]


def _hexbyte(where: str, token: Any) -> int:
    if not isinstance(token, str) or not re.fullmatch(r"0x[0-9a-f]{2}", token):
        raise RecipeError(where, f"expected a lowercase 0xNN tag, got {token!r}")
    return int(token, 16)


def _derive_framing(recipe: Recipe, ep8: Any) -> None:
    """Framing tags and widths, PARSED OUT OF LIVE EP8 CLAUSE TEXT."""
    grammar = _get(ep8, ["canonicalCommitmentGrammar"])
    if not isinstance(grammar, dict):
        raise RecipeError("EP8 $.canonicalCommitmentGrammar",
                          f"declared object, found {json_type(grammar)}")

    component = grammar.get("component")
    if not isinstance(component, str):
        raise RecipeError("EP8 $.canonicalCommitmentGrammar.component",
                          f"declared string, found {json_type(component)}")
    widths = re.findall(r"uint(\d+)be", component)
    if widths != ["32"]:
        raise RecipeError(
            "EP8 $.canonicalCommitmentGrammar.component",
            f"the component frame's length width could not be derived from "
            f"live EP8 clause text {component!r}; found {widths}")
    if not component.startswith("uint8("):
        raise RecipeError(
            "EP8 $.canonicalCommitmentGrammar.component",
            f"live EP8's component clause does not begin with a uint8 tag: "
            f"{component!r}")
    recipe.component_width = 32

    leaf = grammar.get("leaf")
    if not isinstance(leaf, str):
        raise RecipeError("EP8 $.canonicalCommitmentGrammar.leaf",
                          f"declared string, found {json_type(leaf)}")
    tags = re.findall(r"0x([0-9a-f]{2})", leaf)
    widths = re.findall(r"uint(\d+)be", leaf)
    if len(tags) != 1 or widths != ["64"]:
        raise RecipeError(
            "EP8 $.canonicalCommitmentGrammar.leaf",
            f"the leaf tag and width could not be derived from live EP8 clause "
            f"text {leaf!r}; tags {tags}, widths {widths}")
    recipe.leaf_tag = int(tags[0], 16)
    recipe.leaf_width = 64

    outer = grammar.get("outer")
    if not isinstance(outer, str):
        raise RecipeError("EP8 $.canonicalCommitmentGrammar.outer",
                          f"declared string, found {json_type(outer)}")
    tags = re.findall(r"0x([0-9a-f]{2})", outer)
    if len(tags) != 4:
        raise RecipeError(
            "EP8 $.canonicalCommitmentGrammar.outer",
            f"the four outer tags could not be derived from live EP8 clause "
            f"text {outer!r}; found {tags}")
    recipe.outer_tags = tuple(int(t, 16) for t in tags)  # type: ignore[assignment]
    if len({*recipe.outer_tags}) != 4:
        raise RecipeError("EP8 $.canonicalCommitmentGrammar.outer",
                          f"the four outer tags are not distinct: {tags}")
    # The outer clause must name namespace, domain and root in that order, so
    # the tag-to-role assignment is derived rather than assumed.
    roles = re.findall(r"0x[0-9a-f]{2}\s*,\s*([A-Za-z]+)", outer)
    if roles != ["namespace", "domain", "merkleRoot"]:
        raise RecipeError(
            "EP8 $.canonicalCommitmentGrammar.outer",
            f"the outer clause's tag-to-role assignment could not be derived; "
            f"found {roles}")


def _derive_text_rule(recipe: Recipe, doc: Any, ep8_bytes: bytes) -> None:
    """The text admission bound, parsed out of the EP8 sentence the artifact
    quotes -- after that sentence is confirmed present in LIVE EP8 bytes."""
    where = ("$.policyDerivationIdentity.primitives.text"
             ".sourceSentenceCharacterForCharacter")
    sentence = _get(doc, ["policyDerivationIdentity", "primitives", "text",
                          "sourceSentenceCharacterForCharacter"])
    if not isinstance(sentence, str):
        raise RecipeError(where, f"declared string, found {json_type(sentence)}")
    # "character for character" is a checkable claim: the quoted sentence must
    # occur, as a JSON string body, inside live EP8's bytes.
    encoded = json.dumps(sentence, ensure_ascii=False)[1:-1].encode("utf-8")
    if encoded not in ep8_bytes:
        raise RecipeError(
            where,
            "the sentence the artifact claims to quote character for character "
            "does not occur in live evaluation-proof.v8 bytes")
    bound = re.search(r"<=\s*(\d+)\s*bytes", sentence)
    if bound is None:
        raise RecipeError(
            where,
            f"the byte bound could not be derived from the live EP8 sentence "
            f"{sentence!r}")
    recipe.text_max = int(bound.group(1))
    for clause in ("NFC-normalized", "no BOM", "non-empty",
                   "U+0000..U+001F", "U+007F"):
        if clause not in sentence:
            raise RecipeError(
                where,
                f"the live EP8 sentence does not carry the {clause!r} clause "
                f"this encoder applies")


def _derive_variants(recipe: Recipe, v15: Any) -> None:
    """The admissible variants, derived from LIVE v1.5.

    A derivationDigest exists only where a policyOutcome exists, so the
    admissible variant set is exactly the projectionByVariant members whose
    projection carries policyOutcome.  REJ-12 rejects `cancelled` on precisely
    this basis; here the basis is computed rather than asserted.
    """
    where = "v1.5 $.evidenceIdentity.projectionByVariant"
    projection = _get(v15, ["evidenceIdentity", "projectionByVariant"])
    if not isinstance(projection, dict) or not projection:
        raise RecipeError(where, f"declared object, found {json_type(projection)}")
    carriers: list[str] = []
    for variant, fields in projection.items():
        if not isinstance(fields, list):
            raise RecipeError(f"{where}.{variant}",
                              f"declared array, found {json_type(fields)}")
        if "policyOutcome" in fields:
            carriers.append(variant)
    if not carriers:
        raise RecipeError(where,
                          "no v1.5 variant carries policyOutcome, so this "
                          "identity has no admissible input at all")
    recipe.variants = tuple(carriers)


def _derive_separator(recipe: Recipe, doc: Any, ep8: Any) -> None:
    """namespace and domain, derived and adjudicated against live EP8."""
    node = _get(doc, ["policyDerivationIdentity", "namespaceAndDomainSeparator"])
    where = "$.policyDerivationIdentity.namespaceAndDomainSeparator"
    if not isinstance(node, dict):
        raise RecipeError(where, f"declared object, found {json_type(node)}")
    namespace = node.get("namespace")
    domain = node.get("domain")
    for label, value in (("namespace", namespace), ("domain", domain)):
        if not isinstance(value, str) or not value:
            raise RecipeError(f"{where}.{label}",
                              f"declared non-empty string, found "
                              f"{json_type(value)}")
    recipe.namespace = namespace          # type: ignore[assignment]
    recipe.domain = domain                # type: ignore[assignment]

    # Second, independent statement of the same two strings inside the
    # artifact: the preimage step must QUOTE them.  Two sections written apart
    # must agree, so a unilateral edit to either one is a finding.
    step4 = _get(doc, ["policyDerivationIdentity", "preimage", "step4_OUTER"])
    if not isinstance(step4, str):
        raise RecipeError("$.policyDerivationIdentity.preimage.step4_OUTER",
                          f"declared string, found {json_type(step4)}")
    quoted = re.findall(r"'([^']*)'", step4)
    if quoted != [recipe.namespace, recipe.domain]:
        raise RecipeError(
            "$.policyDerivationIdentity.preimage.step4_OUTER",
            f"the outer preimage step quotes {quoted}; the separator section "
            f"declares [{recipe.namespace!r}, {recipe.domain!r}]")

    # Law 19, adjudicated against LIVE EP8: R-1 mints its own domain under its
    # own namespace and does NOT extend EP8's closed list.
    domains = _get(ep8, ["canonicalCommitmentGrammar", "domains"])
    if not isinstance(domains, list):
        raise RecipeError("EP8 $.canonicalCommitmentGrammar.domains",
                          f"declared array, found {json_type(domains)}")
    if recipe.domain in domains:
        raise RecipeError(
            f"{where}.domain",
            f"{recipe.domain!r} has been added to live EP8's closed domain "
            f"list; law 19 requires R-1 to mint its own under its own "
            f"namespace, not to extend EP8's")
    ep8_namespace = _get(ep8, ["canonicalCommitmentGrammar", "namespace"])
    if recipe.namespace == ep8_namespace:
        raise RecipeError(
            f"{where}.namespace",
            f"R-1 has adopted EP8's own namespace {ep8_namespace!r}; a "
            f"separator that is shared separates nothing")
    listed = node.get("r1DomainList")
    if not isinstance(listed, list) or listed != [recipe.domain]:
        raise RecipeError(f"{where}.r1DomainList",
                          f"declared exactly [{recipe.domain!r}]; found "
                          f"{listed!r}")


_ENCODING_TEXT = re.compile(r"^C\(0x([0-9a-f]{2}), text\)$")
_ENCODING_SCALAR = re.compile(r"^C\(0x([0-9a-f]{2}), C\(0x([0-9a-f]{2}), text\)\)$")
_ENCODING_RECORD = re.compile(
    r"^C\(0x([0-9a-f]{2}), ([A-Za-z0-9]+) complete record bytes\)$")
_ENCODING_LIST = re.compile(r"^C\(0x([0-9a-f]{2}), concatenated item frames\b")


def _derive_record_grammar(recipe: Recipe, doc: Any) -> None:
    """Field names, order, tags, shapes and presence, DERIVED from the
    artifact's recordGrammar and structurally re-adjudicated."""
    grammar = _get(doc, ["policyDerivationIdentity", "recordGrammar"])
    base = "$.policyDerivationIdentity.recordGrammar"
    if not isinstance(grammar, dict):
        raise RecipeError(base, f"declared object, found {json_type(grammar)}")
    top = grammar.get("PolicyDerivationInputV1")
    if not isinstance(top, dict):
        raise RecipeError(f"{base}.PolicyDerivationInputV1",
                          f"declared object, found {json_type(top)}")
    recipe.record_tag = _hexbyte(f"{base}.PolicyDerivationInputV1.recordTag",
                                 top.get("recordTag"))
    rows = top.get("fields")
    if not isinstance(rows, list) or not rows:
        raise RecipeError(f"{base}.PolicyDerivationInputV1.fields",
                          f"declared non-empty array, found {json_type(rows)}")

    # Pass one: read every row, deriving its tag from BOTH the `tag` column and
    # the `encoding` column and requiring them to agree.  A table whose two
    # columns disagree is not a table.
    parsed: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        rw = f"{base}.PolicyDerivationInputV1.fields[{index}]"
        if not isinstance(row, dict):
            raise RecipeError(rw, f"declared object, found {json_type(row)}")
        name = row.get("name")
        ordinal = row.get("ordinal")
        encoding = row.get("encoding")
        for label, value in (("name", name), ("ordinal", ordinal),
                             ("encoding", encoding)):
            if not isinstance(value, str) or not value:
                raise RecipeError(f"{rw}.{label}",
                                  f"declared non-empty string, found "
                                  f"{json_type(value)}")
        tag = _hexbyte(f"{rw}.tag", row.get("tag"))
        from_encoding = re.findall(r"0x([0-9a-f]{2})", encoding)  # type: ignore[arg-type]
        if not from_encoding or int(from_encoding[0], 16) != tag:
            raise RecipeError(
                f"{rw}.encoding",
                f"the tag column says 0x{tag:02x} but the encoding column "
                f"{encoding!r} leads with "
                f"{from_encoding[0] if from_encoding else 'no tag'}")
        parsed.append({"where": rw, "name": name, "ordinal": ordinal,
                       "tag": tag, "encoding": encoding, "row": row})

    # Pass two: split item rows ("6i", "7i", ...) from field rows ("0".."11").
    item_rows: dict[str, dict[str, Any]] = {}
    field_rows: list[dict[str, Any]] = []
    for entry in parsed:
        ordinal = entry["ordinal"]
        if re.fullmatch(r"\d+i", ordinal):
            item_rows[ordinal[:-1]] = entry
        elif re.fullmatch(r"\d+", ordinal):
            field_rows.append(entry)
        else:
            raise RecipeError(entry["where"] + ".ordinal",
                              f"unrecognised ordinal {ordinal!r}")
    field_rows.sort(key=lambda e: int(e["ordinal"]))
    if [int(e["ordinal"]) for e in field_rows] != list(range(len(field_rows))):
        raise RecipeError(f"{base}.PolicyDerivationInputV1.fields",
                          "the field ordinals are not 0..n-1 without gaps")

    # Pass three: shapes.  The shape is read out of the encoding grammar, not
    # guessed from the field name.
    top_fields: list[tuple[str, int, Any, str]] = []
    nested_first_seen: list[str] = []
    for entry in field_rows:
        name, tag, encoding, rw = (entry["name"], entry["tag"],
                                   entry["encoding"], entry["where"])
        presence = entry["row"].get("presence")
        if not isinstance(presence, str) or not presence:
            raise RecipeError(f"{rw}.presence",
                              f"declared non-empty string, found "
                              f"{json_type(presence)}")
        source = entry["row"].get("source")
        if isinstance(source, str):
            recipe.field_source[name] = source
        match_text = _ENCODING_TEXT.fullmatch(encoding)
        match_record = _ENCODING_RECORD.fullmatch(encoding)
        match_list = _ENCODING_LIST.match(encoding)
        if match_text is not None:
            top_fields.append((name, tag, TEXT, presence))
            continue
        if match_record is not None:
            type_name = match_record.group(2)
            if type_name not in nested_first_seen:
                nested_first_seen.append(type_name)
            top_fields.append((name, tag, ("record", type_name), presence))
            continue
        if match_list is None:
            raise RecipeError(f"{rw}.encoding",
                              f"unrecognised encoding form {encoding!r}")
        item = item_rows.get(entry["ordinal"])
        if item is None:
            raise RecipeError(
                f"{rw}.encoding",
                f"{name} is encoded as a list of item frames but the grammar "
                f"carries no {entry['ordinal']}i item row")
        item_encoding = item["encoding"]
        scalar = _ENCODING_SCALAR.fullmatch(item_encoding)
        record = _ENCODING_RECORD.fullmatch(item_encoding)
        if scalar is not None:
            top_fields.append((name, tag, ("scalar-array",
                                           int(scalar.group(1), 16),
                                           int(scalar.group(2), 16)), presence))
        elif record is not None:
            type_name = record.group(2)
            if type_name not in nested_first_seen:
                nested_first_seen.append(type_name)
            top_fields.append((name, tag, ("record-array",
                                           int(record.group(1), 16),
                                           type_name), presence))
        else:
            raise RecipeError(item["where"] + ".encoding",
                              f"unrecognised item encoding {item_encoding!r}")
        if item["name"] != f"{name}[]":
            raise RecipeError(item["where"] + ".name",
                              f"the item row for {name} is named "
                              f"{item['name']!r}, not {name + '[]'!r}")
    recipe.top = top_fields

    # Pass four: RE-DERIVE the tag assignment rule and re-apply it.  The rule
    # the artifact states is "field tags run consecutively from recordTag+1 in
    # preimage order, an array consuming its container tag then its item tag
    # then, for an array of scalars, its scalar tag".  That is a computation,
    # so it is computed.
    expected = recipe.record_tag + 1
    for name, tag, shape, _presence in top_fields:
        if tag != expected:
            raise RecipeError(
                f"{base}.PolicyDerivationInputV1.fields[{name}].tag",
                f"the declared tag assignment rule places {name} at "
                f"0x{expected:02x}; the table declares 0x{tag:02x}")
        expected += 1
        if isinstance(shape, tuple) and shape[0] == "scalar-array":
            if shape[1] != expected or shape[2] != expected + 1:
                raise RecipeError(
                    f"{base}.PolicyDerivationInputV1.fields[{name}[]].tag",
                    f"the tag assignment rule places {name}'s item and scalar "
                    f"tags at 0x{expected:02x}/0x{expected + 1:02x}; the table "
                    f"declares 0x{shape[1]:02x}/0x{shape[2]:02x}")
            expected += 2
        elif isinstance(shape, tuple) and shape[0] == "record-array":
            if shape[1] != expected:
                raise RecipeError(
                    f"{base}.PolicyDerivationInputV1.fields[{name}[]].tag",
                    f"the tag assignment rule places {name}'s item tag at "
                    f"0x{expected:02x}; the table declares 0x{shape[1]:02x}")
            expected += 1

    # Pass five: the nested record types, in order of FIRST APPEARANCE, which
    # the artifact's own rule says take 0xa0, 0xb0, 0xc0, 0xd0.
    for position, type_name in enumerate(nested_first_seen):
        node = grammar.get(type_name)
        nw = f"{base}.{type_name}"
        if not isinstance(node, dict):
            raise RecipeError(nw, f"declared object, found {json_type(node)}")
        record_tag = _hexbyte(f"{nw}.recordTag", node.get("recordTag"))
        wanted = 0xa0 + 0x10 * position
        if record_tag != wanted:
            raise RecipeError(
                f"{nw}.recordTag",
                f"{type_name} first appears at position {position}, so the "
                f"declared rule places it at 0x{wanted:02x}; the table "
                f"declares 0x{record_tag:02x}")
        rows = node.get("fields")
        if not isinstance(rows, list) or not rows:
            raise RecipeError(f"{nw}.fields",
                              f"declared non-empty array, found "
                              f"{json_type(rows)}")
        fields: list[tuple[str, int]] = []
        cursor = record_tag + 1
        for index, row in enumerate(rows):
            rw = f"{nw}.fields[{index}]"
            if not isinstance(row, dict):
                raise RecipeError(rw, f"declared object, found {json_type(row)}")
            field = row.get("name")
            if not isinstance(field, str) or not field:
                raise RecipeError(f"{rw}.name",
                                  f"declared non-empty string, found "
                                  f"{json_type(field)}")
            tag = _hexbyte(f"{rw}.tag", row.get("tag"))
            encoding = row.get("encoding")
            if not isinstance(encoding, str):
                raise RecipeError(f"{rw}.encoding",
                                  f"declared string, found {json_type(encoding)}")
            match_text = _ENCODING_TEXT.fullmatch(encoding)
            if match_text is None or int(match_text.group(1), 16) != tag:
                raise RecipeError(
                    f"{rw}.encoding",
                    f"a nested field must encode as C(0x{tag:02x}, text); the "
                    f"table declares {encoding!r}")
            if tag != cursor:
                raise RecipeError(
                    f"{rw}.tag",
                    f"the declared rule makes {type_name}'s field tags "
                    f"consecutive from 0x{record_tag + 1:02x}; {field} should "
                    f"be 0x{cursor:02x} but is declared 0x{tag:02x}")
            cursor += 1
            fields.append((field, tag))
        recipe.nested[type_name] = (record_tag, fields)
    if len(recipe.nested) != len(nested_first_seen):
        raise RecipeError(base, "a nested record type was declared twice")


# --- the LIVE v1.5 closed type graph -------------------------------------
def _v15_type(v15: Any, name: str) -> Any:
    node = _get(v15, ["closedTypes", name])
    if not isinstance(node, dict):
        raise RecipeError(f"v1.5 $.closedTypes.{name}",
                          f"declared object, found {json_type(node)}")
    return node


def _spec_from_v15(v15: Any, node: Any, where: str, name: str) -> TypeSpec:
    """Resolve one live-v1.5 schema node to a leaf TypeSpec."""
    seen: set[str] = set()
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        if not isinstance(ref, str) or ref in seen:
            raise RecipeError(where, f"unresolvable $ref chain at {name}")
        seen.add(ref)
        name = ref
        node = _v15_type(v15, ref)
    if not isinstance(node, dict):
        raise RecipeError(where, f"declared object, found {json_type(node)}")
    kind = node.get("kind")
    if kind == "array":
        # A scalar array's leaf type is its ITEM type.  Descending here rather
        # than at the call site keeps the resolver total over the live graph.
        return _spec_from_v15(v15, node.get("items"), where, f"{name}[]")
    if kind == "string":
        pattern = node.get("pattern")
        if not isinstance(pattern, str):
            raise RecipeError(where, f"live v1.5 {name} declares no pattern")
        return TypeSpec(name, "pattern", pattern=pattern)
    if kind == "enum":
        values = node.get("values")
        if not isinstance(values, list) or not values:
            raise RecipeError(where,
                              f"live v1.5 {name} declares no enum vocabulary")
        for value in values:
            if not isinstance(value, str):
                raise RecipeError(where,
                                  f"live v1.5 {name} carries a non-string enum "
                                  f"member {value!r}")
        return TypeSpec(name, "enum", values=tuple(values))
    if kind == "const":
        value = node.get("value")
        if not isinstance(value, str):
            raise RecipeError(where, f"live v1.5 {name} const is not a string")
        return TypeSpec(name, "const", values=(value,))
    raise RecipeError(where, f"live v1.5 {name} is a {kind!r}, not a leaf type")


def _walk_v15(v15: Any, root: str, path: list[str],
              where: str) -> tuple[Any, str, dict[str, Any]]:
    """Walk a dotted source path through live v1.5's closed type graph.

    Returns (schema node, owning type name, owning type node).  Arrays are
    entered through `items`, so `deps.rules.entries` lands on RuleValue.
    """
    node: Any = _v15_type(v15, root)
    owner_name = root
    owner_node = node
    for step in path:
        while isinstance(node, dict) and "$ref" in node:
            ref = node["$ref"]
            if not isinstance(ref, str):
                raise RecipeError(where, f"unresolvable $ref at {step!r}")
            owner_name = ref
            node = _v15_type(v15, ref)
            owner_node = node
        if isinstance(node, dict) and node.get("kind") == "array":
            node = node.get("items")
            continue
        if not isinstance(node, dict) or not isinstance(node.get("fields"), dict):
            raise RecipeError(where,
                              f"live v1.5 {owner_name} has no field {step!r}")
        fields = node["fields"]
        if step not in fields:
            raise RecipeError(where,
                              f"live v1.5 {owner_name} has no field {step!r}")
        owner_node = node
        node = fields[step]
    return node, owner_name, owner_node


_SOURCE_ROOTS = {
    "stageInput": ("SealedStageInput", None),
    "deps": ("CoreDeps", None),
}


def _source_to_v15(recipe: Recipe, v15: Any, field: str,
                   where: str) -> tuple[Any, str] | None:
    """Map a recordGrammar `source` value onto a live v1.5 schema node.

    The source column is prose-bearing, so only its leading dotted path is
    consumed; everything after the first comma, semicolon or sentence break is
    commentary and is ignored deliberately rather than parsed.
    """
    source = recipe.field_source.get(field)
    if not isinstance(source, str):
        return None
    head = re.split(r"[,;]| -- ", source, maxsplit=1)[0].strip().rstrip(".")
    completion = re.fullmatch(r"CoreCompletion::(\*|\w+)\.(.+)", head)
    if completion is not None:
        variant, rest = completion.group(1), completion.group(2)
        union = _v15_type(v15, "CoreCompletion")
        variants = union.get("variants")
        if not isinstance(variants, dict):
            raise RecipeError("v1.5 $.closedTypes.CoreCompletion.variants",
                              f"declared object, found {json_type(variants)}")
        if variant == "*":
            for candidate in recipe.variants:
                if candidate in variants:
                    variant = candidate
                    break
        node = variants.get(variant)
        if not isinstance(node, dict):
            return None
        cursor: Any = node
        owner = f"CoreCompletion::{variant}"
        for step in rest.split("."):
            while isinstance(cursor, dict) and "$ref" in cursor:
                owner = cursor["$ref"]
                cursor = _v15_type(v15, owner)
            if isinstance(cursor, dict) and cursor.get("kind") == "array":
                cursor = cursor.get("items")
                continue
            fields = cursor.get("fields") if isinstance(cursor, dict) else None
            if not isinstance(fields, dict) or step not in fields:
                return None
            cursor = fields[step]
        return cursor, owner
    parts = head.split(".")
    root = _SOURCE_ROOTS.get(parts[0])
    if root is None:
        return None
    node, owner, _owner_node = _walk_v15(v15, root[0], parts[1:], where)
    return node, owner


def _derive_leaf_types(recipe: Recipe, doc: Any, v15: Any) -> None:
    """Every leaf's TYPE, resolved through LIVE v1.5's closed type graph.

    This is what makes a `sha856:` prefix a NAMED refusal rather than an
    invisible one: the Digest pattern is live v1.5's, not this file's.
    """
    base = "$.policyDerivationIdentity.recordGrammar"

    # (a) nested record types, adjudicated through the artifact's own
    #     `mirrors` pointer into LIVE v1.5.
    grammar = _get(doc, ["policyDerivationIdentity", "recordGrammar"], {})
    for type_name, (_tag, fields) in recipe.nested.items():
        node = grammar.get(type_name)
        mirrors = node.get("mirrors") if isinstance(node, dict) else None
        where = f"{base}.{type_name}.mirrors"
        if not isinstance(mirrors, str):
            raise RecipeError(where, f"declared string, found {json_type(mirrors)}")
        match = re.fullmatch(r"closedTypes\.(\w+)\.fieldOrder", mirrors)
        if match is None:
            raise RecipeError(
                where,
                f"{mirrors!r} is not a resolvable pointer of the form "
                f"closedTypes.<Type>.fieldOrder")
        v15_name = match.group(1)
        v15_node = _v15_type(v15, v15_name)
        order = v15_node.get("fieldOrder")
        derived = [name for name, _ in fields]
        if order != derived:
            raise RecipeError(
                where,
                f"{type_name} derives the field order {derived}; LIVE v1.5 "
                f"closedTypes.{v15_name}.fieldOrder is {order!r}")
        v15_fields = v15_node.get("fields")
        if not isinstance(v15_fields, dict):
            raise RecipeError(f"v1.5 $.closedTypes.{v15_name}.fields",
                              f"declared object, found {json_type(v15_fields)}")
        recipe.type_of_field[type_name] = v15_name
        for name, _tag2 in fields:
            spec = _spec_from_v15(v15, v15_fields.get(name),
                                  f"v1.5 $.closedTypes.{v15_name}.fields.{name}",
                                  f"{v15_name}.{name}")
            recipe.leaf_types[(type_name, name)] = spec

    # (b) the top record's own text leaves, via the `source` column.
    for name, _tag, shape, _presence in recipe.top:
        if shape is not TEXT and not (isinstance(shape, tuple)
                                      and shape[0] == "scalar-array"):
            continue
        where = f"{base}.PolicyDerivationInputV1.fields[{name}].source"
        if name == "variant":
            # The discriminant is not a v1.5 leaf; its vocabulary is the
            # DERIVED variant set, which came from live v1.5's projection.
            recipe.leaf_types[("", name)] = TypeSpec(
                "CoreCompletion.variant", "enum", values=recipe.variants)
            continue
        resolved = _source_to_v15(recipe, v15, name, where)
        if resolved is None:
            raise RecipeError(
                where,
                f"the source column for {name} does not resolve to a live v1.5 "
                f"closed type, so this leaf's admission rule would be this "
                f"file's opinion rather than the predecessor's")
        node, owner = resolved
        recipe.leaf_types[("", name)] = _spec_from_v15(
            v15, node, where, f"{owner}.{name}")


_ORDER_BY = re.compile(
    r"^strict ascending UTF-8 byte order by (\w+)$")
_ORDER_TUPLE = re.compile(
    r"^strict ascending tuple of UTF-8 bytes \(([^)]*)\)$")

# Where LIVE v1.5 states each list's orderRule.  These are POINTERS, not the
# rules; the rules themselves are parsed out of whatever the live bytes say.
V15_ORDER_POINTERS = {
    "planStageIds": ["closedTypes", "SealedStageInput", "fields",
                     "planStageIds", "orderRule"],
    "rules": ["closedTypes", "RuleSet", "fields", "entries", "orderRule"],
    "findings": ["closedTypes", "FindingList", "orderRule"],
    "exactCoverage": ["closedTypes", "ExactCoverage", "fields", "entries",
                      "orderRule"],
}


def _derive_order_rules(recipe: Recipe, v15: Any) -> None:
    """The sort keys, PARSED out of LIVE v1.5 orderRule sentences."""
    for name, pointer in V15_ORDER_POINTERS.items():
        where = "v1.5 $." + ".".join(pointer)
        rule = _get(v15, pointer)
        if not isinstance(rule, str) or not rule:
            raise RecipeError(where,
                              f"declared non-empty string, found "
                              f"{json_type(rule)}")
        single = _ORDER_BY.fullmatch(rule)
        tup = _ORDER_TUPLE.fullmatch(rule)
        if single is not None:
            recipe.content_ordered[name] = (single.group(1),)
        elif tup is not None:
            keys = tuple(part.strip() for part in tup.group(1).split(","))
            if not all(keys):
                raise RecipeError(where,
                                  f"the tuple sort key could not be parsed from "
                                  f"{rule!r}")
            recipe.content_ordered[name] = keys
        elif "preserve byte-for-byte" in rule:
            # A SEQUENCE.  Deliberately absent from content_ordered: its order
            # is not a function of its content, which is the whole of the
            # orderingRuling's case and the reason the falsifier exists.
            continue
        else:
            raise RecipeError(
                where,
                f"live v1.5's orderRule {rule!r} is neither a parseable content "
                f"sort nor a byte-for-byte sequence, so this encoder cannot "
                f"implement it without guessing")
    if "planStageIds" in recipe.content_ordered:
        raise RecipeError(
            "v1.5 $.closedTypes.SealedStageInput.fields.planStageIds.orderRule",
            "planStageIds parsed as a CONTENT-ordered list; the sequence ruling "
            "and the entire 554-byte falsifier rest on it not being one")
    # Every content-ordered list must be a list this grammar actually carries,
    # and every sort key must be a field of the item type.
    for name, keys in recipe.content_ordered.items():
        shape = None
        for field, _tag, form, _presence in recipe.top:
            if field == name:
                shape = form
        if not (isinstance(shape, tuple) and shape[0] == "record-array"):
            raise RecipeError(
                "v1.5 $." + ".".join(V15_ORDER_POINTERS[name]),
                f"live v1.5 content-orders {name}, but the derived grammar does "
                f"not carry it as an array of records")
        declared = [field for field, _ in recipe.nested[shape[2]][1]]
        for key in keys:
            if key not in declared:
                raise RecipeError(
                    "v1.5 $." + ".".join(V15_ORDER_POINTERS[name]),
                    f"live v1.5 sorts {name} by {key!r}, which is not a field of "
                    f"{shape[2]} ({declared})")


def derive_recipe(doc: Any, v15: Any, ep8: Any, ep8_bytes: bytes,
                  findings: list[str]) -> Recipe | None:
    """Build the whole recipe, or report the first position that refused."""
    recipe = Recipe()
    for step in (lambda: _derive_framing(recipe, ep8),
                 lambda: _derive_text_rule(recipe, doc, ep8_bytes),
                 lambda: _derive_variants(recipe, v15),
                 lambda: _derive_separator(recipe, doc, ep8),
                 lambda: _derive_record_grammar(recipe, doc),
                 lambda: _derive_leaf_types(recipe, doc, v15),
                 lambda: _derive_order_rules(recipe, v15)):
        try:
            step()
        except RecipeError as exc:
            _add(findings, "R1V17-RECIPE-DERIVATION", exc.where, exc.detail)
            return None
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            _add(findings, "R1V17-RECIPE-DERIVATION", "$",
                 f"the recipe could not be derived: {type(exc).__name__}: {exc}")
            return None
    if len(recipe.top) != EXPECT_TOP_FIELDS:
        _add(findings, "R1V17-RECIPE-DERIVATION",
             "$.policyDerivationIdentity.recordGrammar.PolicyDerivationInputV1"
             ".fields",
             f"derived {len(recipe.top)} top-level fields; "
             f"{EXPECT_TOP_FIELDS} is expected")
    if len(recipe.nested) != EXPECT_NESTED_TYPES:
        _add(findings, "R1V17-RECIPE-DERIVATION",
             "$.policyDerivationIdentity.recordGrammar",
             f"derived {len(recipe.nested)} nested record types; "
             f"{EXPECT_NESTED_TYPES} is expected")
    return recipe


# ---------------------------------------------------------------------------
# Section 5.  Encoder A -- table-driven, over the DERIVED recipe.
#
# One declarative walk of the derived grammar; struct.pack for big-endian;
# bytes.hex for output.  Exception messages are the artifact's published
# encoderA strings, byte for byte, so a recorded measurement gets a hard
# comparison rather than a family resemblance.
# ---------------------------------------------------------------------------
def a_text(recipe: Recipe, value: Any) -> bytes:
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
    if len(raw) > recipe.text_max:
        raise ValueError(
            f"text component exceeds {recipe.text_max} bytes ({len(raw)})")
    return raw


def a_frame(recipe: Recipe, tag: int, payload: bytes) -> bytes:
    if recipe.component_width != 32:
        raise ValueError(
            f"live EP8 declares a uint{recipe.component_width}be component "
            f"length; this encoder implements uint32be")
    return struct.pack(">B", tag) + struct.pack(">I", len(payload)) + payload


def a_component(recipe: Recipe, tag: int, value: Any) -> bytes:
    return a_frame(recipe, tag, a_text(recipe, value))


def a_nested(recipe: Recipe, name: str, value: Any) -> bytes:
    record_tag, fields = recipe.nested[name]
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
        out += a_component(recipe, tag, value[field])
    return out


def _sort_key(item: Any, keys: tuple[str, ...]) -> tuple[bytes, ...]:
    parts = []
    for key in keys:
        value = item[key]
        if not isinstance(value, str):
            raise TypeError(
                f"text component must be a JSON string, got {type(value)}")
        parts.append(value.encode("utf-8"))
    return tuple(parts)


def a_order_gate(recipe: Recipe, name: str, items: list[Any]) -> None:
    """R-1's own strict-ascending orderRule -- PARSED FROM LIVE v1.5 -- and
    RE-CHECKED at the encoder.

    The list is REFUSED, never repaired.  Repairing would make the encoder
    many-to-one and would cost the LITERAL round-trip that injectivity is
    argued from -- the exact retreat plan-and-policy-identity-recipes.v2 had to
    make after B-PPIR-01.
    """
    keys = recipe.content_ordered[name]
    previous: tuple[bytes, ...] | None = None
    for index, item in enumerate(items):
        current = _sort_key(item, keys)
        if previous is not None and not previous < current:
            raise ValueError(
                f"{name} violates R-1's strict-ascending orderRule at index "
                f"{index}")
        previous = current


def encode_a(recipe: Recipe, value: Any, *,
             set_reading: frozenset[str] = frozenset()) -> bytes:
    """The adopted recipe.  `set_reading` implements the REJECTED reading for
    the named lists and exists only so the falsifier can be EXECUTED."""
    if not isinstance(value, dict):
        raise TypeError(
            f"PolicyDerivationInputV1 must be a JSON object, got {type(value)}")
    extra = sorted(set(value) - set(recipe.top_names))
    if extra:
        raise ValueError(
            f"undeclared field(s) {extra} in PolicyDerivationInputV1")

    variant = value.get("variant")
    if not isinstance(variant, str):
        raise TypeError(
            f"text component must be a JSON string, got {type(variant)}")
    if variant not in recipe.variants:
        raise ValueError(
            f"variant must be {'|'.join(recipe.variants)}, got {variant!r}")
    conditional = [name for name, _t, _s, presence in recipe.top
                   if presence != "required"]
    for name in conditional:
        presence = [p for n, _t, _s, p in recipe.top if n == name][0]
        gate = presence.split("-only")[0]
        if variant != gate and name in value:
            raise ValueError(f"variant={variant} FORBIDS {name}")
        if variant == gate and name not in value:
            raise ValueError(f"variant={variant} REQUIRES {name}")

    out = struct.pack(">B", recipe.record_tag)
    for name, tag, shape, presence in recipe.top:
        if presence != "required" and variant != presence.split("-only")[0]:
            continue
        if name not in value:
            raise ValueError(
                f"missing required field {name} in PolicyDerivationInputV1")
        item = value[name]
        if shape is TEXT:
            out += a_component(recipe, tag, item)
            continue
        if shape[0] == "record":
            out += a_frame(recipe, tag, a_nested(recipe, shape[1], item))
            continue
        if not isinstance(item, list):
            raise TypeError(f"{name} must be a JSON array, got {type(item)}")
        if shape[0] == "scalar-array":
            _, item_tag, scalar_tag = shape
            seen: list[str] = []
            for member in item:
                if not isinstance(member, str):
                    raise TypeError(
                        f"text component must be a JSON string, got "
                        f"{type(member)}")
                if member in seen:
                    raise ValueError(f"duplicate logical list member in {name}")
                seen.append(member)
            frames = [a_frame(recipe, item_tag,
                              a_component(recipe, scalar_tag, member))
                      for member in item]
        else:
            _, item_tag, record_name = shape
            for member in item:
                if not isinstance(member, dict):
                    raise TypeError(
                        f"{record_name} must be a JSON object, got "
                        f"{type(member)}")
            # Under the REJECTED reading the sort REPLACES the order gate --
            # that is precisely what makes it many-to-one -- so the gate is
            # bypassed for a list the caller has named.  The adopted path
            # always runs it.
            if name not in set_reading and name in recipe.content_ordered:
                a_order_gate(recipe, name, item)
            frames = [a_frame(recipe, item_tag,
                              a_nested(recipe, record_name, member))
                      for member in item]
        if name in set_reading:
            frames = sorted(frames)
        out += a_frame(recipe, tag, b"".join(frames))
    return out


def a_leaf_root(recipe: Recipe, record: bytes) -> bytes:
    if recipe.leaf_width != 64:
        raise ValueError(
            f"live EP8 declares a uint{recipe.leaf_width}be leaf length; this "
            f"encoder implements uint64be")
    return hashlib.sha256(
        struct.pack(">B", recipe.leaf_tag)
        + struct.pack(">Q", len(record)) + record).digest()


def a_outer(recipe: Recipe, root: bytes, namespace: str | None = None,
            domain: str | None = None) -> bytes:
    record_tag, ns_tag, domain_tag, root_tag = recipe.outer_tags
    return (struct.pack(">B", record_tag)
            + a_component(recipe, ns_tag,
                          recipe.namespace if namespace is None else namespace)
            + a_component(recipe, domain_tag,
                          recipe.domain if domain is None else domain)
            + a_frame(recipe, root_tag, root))


def a_derivation_digest(recipe: Recipe, record: bytes,
                        namespace: str | None = None,
                        domain: str | None = None) -> str:
    preimage = a_outer(recipe, a_leaf_root(recipe, record), namespace, domain)
    return "sha256:" + hashlib.sha256(preimage).hexdigest()


# ---------------------------------------------------------------------------
# Section 6.  Encoder B -- flat imperative, over the DERIVED recipe.
#
# Written in a deliberately different style: an explicit worklist rather than
# recursion, big-endian hand-rolled by shift-and-mask, bytearray accumulation,
# binascii for hex, its own text validator, its own ordering scan.  Shares NO
# code and NO helper with encoder A.  Freeze 7.1: a sibling sweep "used no
# second encoder, so it does not meet the two-encoder standard this corpus set
# for itself".
# ---------------------------------------------------------------------------
def b_u32(number: int) -> bytes:
    return bytes([(number >> 24) & 0xFF, (number >> 16) & 0xFF,
                  (number >> 8) & 0xFF, number & 0xFF])


def b_u64(number: int) -> bytes:
    return bytes([(number >> shift) & 0xFF
                  for shift in (56, 48, 40, 32, 24, 16, 8, 0)])


def b_txt(limit: int, value: Any) -> bytes:
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
    if len(encoded) > limit:
        raise ValueError("over " + str(limit) + " bytes")
    return encoded


def b_c(limit: int, tag: int, value: Any) -> bytearray:
    body = b_txt(limit, value)
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


def b_record(recipe: Recipe, type_name: str, entry: Any) -> bytearray:
    if not isinstance(entry, dict):
        raise TypeError("not an object")
    record_tag, fields = recipe.nested[type_name]
    names = []
    position = 0
    while position < len(fields):
        names.append(fields[position][0])
        position += 1
    for key in entry:
        if key not in names:
            raise ValueError("undeclared field " + key)
    buf = bytearray()
    buf.append(record_tag)
    position = 0
    while position < len(fields):
        field, tag = fields[position]
        if field not in entry:
            raise ValueError("missing field " + field)
        buf += b_c(recipe.text_max, tag, entry[field])
        position += 1
    return buf


def b_ascending(items: list[Any], keys: tuple[str, ...], label: str) -> None:
    index = 1
    while index < len(items):
        left = []
        right = []
        position = 0
        while position < len(keys):
            key = keys[position]
            lv = items[index - 1][key]
            rv = items[index][key]
            if isinstance(lv, bool) or not isinstance(lv, str):
                raise TypeError("not a string")
            if isinstance(rv, bool) or not isinstance(rv, str):
                raise TypeError("not a string")
            left.append(lv.encode("utf-8"))
            right.append(rv.encode("utf-8"))
            position += 1
        if not tuple(left) < tuple(right):
            raise ValueError(label + " not strictly ascending")
        index += 1


def encode_b(recipe: Recipe, value: Any,
             sorted_lists: tuple[str, ...] = ()) -> bytes:
    if not isinstance(value, dict):
        raise TypeError("not an object")
    plan = recipe.top
    known = []
    slot = 0
    while slot < len(plan):
        known.append(plan[slot][0])
        slot += 1
    for key in value:
        if key not in known:
            raise ValueError("undeclared field " + key)
    variant = value.get("variant")
    if isinstance(variant, bool) or not isinstance(variant, str):
        raise TypeError("not a string")
    if variant not in recipe.variants:
        raise ValueError("bad variant")
    slot = 0
    while slot < len(plan):
        name, _tag, _shape, presence = plan[slot]
        if presence != "required":
            gate = presence.split("-only")[0]
            if variant != gate and name in value:
                raise ValueError(variant + " forbids " + name)
            if variant == gate and name not in value:
                raise ValueError(variant + " requires " + name)
        elif name not in value:
            raise ValueError("missing field " + name)
        slot += 1

    buf = bytearray()
    buf.append(recipe.record_tag)
    slot = 0
    while slot < len(plan):
        name, tag, shape, presence = plan[slot]
        slot += 1
        if presence != "required" and variant != presence.split("-only")[0]:
            continue
        item = value[name]
        if shape is TEXT:
            buf += b_c(recipe.text_max, tag, item)
            continue
        if shape[0] == "record":
            buf += b_blob(tag, bytes(b_record(recipe, shape[1], item)))
            continue
        if not isinstance(item, list):
            raise TypeError("not an array")
        if shape[0] == "scalar-array":
            position = 0
            while position < len(item):
                other = 0
                while other < position:
                    if item[other] == item[position]:
                        raise ValueError("duplicate " + name + " member")
                    other += 1
                position += 1
            frames = []
            position = 0
            while position < len(item):
                frames.append(bytes(b_blob(
                    shape[1], bytes(b_c(recipe.text_max, shape[2],
                                        item[position])))))
                position += 1
        else:
            position = 0
            while position < len(item):
                if not isinstance(item[position], dict):
                    raise TypeError("not an object")
                position += 1
            if name in recipe.content_ordered:
                b_ascending(item, recipe.content_ordered[name], name)
            frames = []
            position = 0
            while position < len(item):
                frames.append(bytes(b_blob(
                    shape[1], bytes(b_record(recipe, shape[2],
                                             item[position])))))
                position += 1
        if name in sorted_lists:
            frames = sorted(frames)
        buf += b_blob(tag, b"".join(frames))
    return bytes(buf)


def b_digest(recipe: Recipe, record: bytes, namespace: str | None = None,
             domain: str | None = None) -> str:
    leaf = bytearray()
    leaf.append(recipe.leaf_tag)
    leaf += b_u64(len(record))
    leaf += record
    root = hashlib.sha256(bytes(leaf)).digest()
    record_tag, ns_tag, domain_tag, root_tag = recipe.outer_tags
    outer = bytearray()
    outer.append(record_tag)
    outer += b_c(recipe.text_max, ns_tag,
                 recipe.namespace if namespace is None else namespace)
    outer += b_c(recipe.text_max, domain_tag,
                 recipe.domain if domain is None else domain)
    outer += b_blob(root_tag, root)
    return "sha256:" + binascii.hexlify(
        hashlib.sha256(bytes(outer)).digest()).decode("ascii")


def b_hex(raw: bytes) -> str:
    return binascii.hexlify(raw).decode("ascii")


# ---------------------------------------------------------------------------
# Section 7.  The TOTAL decoder, over the DERIVED recipe.
#
# Grammar-directed recursive descent: it walks the DERIVED field list and asks
# the bytes whether the next frame is the field it wants.  It returns exactly
# one value or raises.  It enforces the record tag, declared tag order,
# at-most-once per field, exact frame lengths with no trailing bytes, the text
# admission rule on every scalar, and the variant rule.
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


def d_text(recipe: Recipe, payload: bytes) -> str:
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
    if len(payload) > recipe.text_max:
        raise ValueError(
            f"text component exceeds {recipe.text_max} bytes ({len(payload)})")
    return value


def d_nested(recipe: Recipe, name: str, payload: bytes) -> dict[str, str]:
    record_tag, fields = recipe.nested[name]
    if not payload or payload[0] != record_tag:
        raise ValueError(f"bad record tag for {name}")
    offset = 1
    out: dict[str, str] = {}
    for field, tag in fields:
        got = d_peek_tag(payload, offset)
        if got != tag:
            raise ValueError(f"missing required field {field}")
        _, body, offset = d_frame(payload, offset)
        out[field] = d_text(recipe, body)
    if offset != len(payload):
        tag = d_peek_tag(payload, offset)
        raise ValueError(f"undeclared or out-of-order tag 0x{tag:02x}")
    return out


def decode(recipe: Recipe, buf: bytes) -> dict[str, Any]:
    if not buf or buf[0] != recipe.record_tag:
        raise ValueError("bad record tag for PolicyDerivationInputV1")
    offset = 1
    out: dict[str, Any] = {}
    for name, tag, shape, presence in recipe.top:
        got = d_peek_tag(buf, offset)
        if got != tag:
            if presence != "required":
                continue
            raise ValueError(f"missing required field {name}")
        _, payload, offset = d_frame(buf, offset)
        if shape is TEXT:
            out[name] = d_text(recipe, payload)
        elif shape[0] == "record":
            out[name] = d_nested(recipe, shape[1], payload)
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
                member = d_text(recipe, scalar_body)
                if member in members:
                    raise ValueError(f"duplicate logical list member in {name}")
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
                entries.append(d_nested(recipe, record_name, item_body))
            out[name] = entries
    if offset != len(buf):
        tag = d_peek_tag(buf, offset)
        raise ValueError(f"undeclared or out-of-order tag 0x{tag:02x}")
    variant = out.get("variant")
    if variant not in recipe.variants:
        raise ValueError(
            f"variant must be {'|'.join(recipe.variants)}, got {variant!r}")
    for name, _tag, _shape, presence in recipe.top:
        if presence == "required":
            continue
        gate = presence.split("-only")[0]
        if variant != gate and name in out:
            raise ValueError(f"variant={variant} FORBIDS {name}")
        if variant == gate and name not in out:
            raise ValueError(f"variant={variant} REQUIRES {name}")
    # The decoder deliberately does NOT re-apply R-1's content orderRules.
    # decoderTotality declares its contract exactly, and adding a gate here
    # would make the decoder refuse the rejected-reading exhibit records it
    # must be TOTAL on.  Admission is the encoder's job.
    return out


# ---------------------------------------------------------------------------
# Section 8.  v1.5 vector resolution and the fieldSetRule, applied to the LIVE
# predecessor bytes rather than to v1.6's copy of them.  The projection map is
# DERIVED from the artifact's own recordGrammar `source` column rather than
# hand-written, so a successor that renamed a source would be caught here.
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


def _read_dotted(node: Any, dotted: str) -> Any:
    cur = node
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def resolve_v15(v15: dict[str, Any], vector_id: str,
                seen: tuple[str, ...] = ()) -> dict[str, Any] | None:
    if vector_id in seen:
        return None
    vectors = v15.get("positiveVectors")
    if not isinstance(vectors, list):
        return None
    table = {v["id"]: v for v in vectors
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


# The two source roots the fieldSetRule reads from a resolved v1.5 vector, and
# the completion object it reads the derived half from.  Which FIELD comes from
# which root is not written here: it is taken from the DERIVED recipe's
# `source` column, so the projection follows the grammar rather than a copy.
_COMPLETION_ALIASES = {"findings": ("findings", "partialFindings")}


def field_set_record(recipe: Recipe, resolved: dict[str, Any],
                     completion: dict[str, Any]) -> dict[str, Any] | None:
    """PolicyDerivationInputV1 = (0) the variant, then (I) every leaf of the
    closed argument domain minus the declared evidence-neutral subtrees, then
    (D) projectionByVariant[variant] minus variant and minus policyOutcome.

    The per-field extraction path is READ OUT OF THE DERIVED GRAMMAR.
    """
    variant = completion.get("variant")
    out: dict[str, Any] = {}
    for name, _tag, _shape, presence in recipe.top:
        if name == "variant":
            out["variant"] = variant
            continue
        if presence != "required" and variant != presence.split("-only")[0]:
            continue
        source = recipe.field_source.get(name)
        if not isinstance(source, str):
            return None
        head = re.split(r"[,;]| -- ", source, maxsplit=1)[0].strip().rstrip(".")
        completion_match = re.fullmatch(r"CoreCompletion::(\*|\w+)\.(.+)", head)
        if completion_match is not None:
            rest = completion_match.group(2)
            value = _read_dotted(completion, rest)
            if value is None:
                for alias in _COMPLETION_ALIASES.get(name, ()):
                    value = _read_dotted(
                        completion, rest.replace(rest.split(".")[0], alias, 1))
                    if value is not None:
                        break
            out[name] = value
            continue
        parts = head.split(".")
        if parts[0] not in ("stageInput", "deps"):
            return None
        out[name] = _read_dotted(resolved, head)
    if any(value is None for value in out.values()):
        return None
    return out


# ---------------------------------------------------------------------------
# Section 9.  THE CORPUS DERIVATION.  This is the CIR-B1 fix.
#
# The predecessor recomputed each published digest FROM the published
# recordValue and compared the two.  That is arithmetic, and it is sound
# arithmetic, but it is circular as evidence: it certifies that the author
# hashed correctly, not that there is anything there to hash.  Collapsing
# eleven of the seventeen recordValues onto PDD-01's and republishing with the
# predecessor's own encoder passed at zero findings.
#
# Here NO published recordValue is read as an answer.  All seventeen are
# REBUILT:
#
#   * PDD-01..PDD-04 by applying the fieldSetRule to LIVE v1.5 vectors.
#   * PDD-05..PDD-17 from the REBUILT PDD-01 by the algebra below.  The
#     algebra is deliberately generative: SWAP, REVERSE and FROM_BASIS compute
#     their operands from the basis and transcribe nothing at all, and
#     NEXT_DIGEST generates successive hex-nibble constants from a counter
#     rather than copying them.  What remains -- four OpaqueId literals, two
#     closed-enum members and one findingId -- is DECLARED, and each is
#     separately required to be admissible under LIVE v1.5's closed type for
#     its leaf and to differ from the basis value it replaces.  That residual
#     is stated in NOT_VERIFIED rather than hidden.
#
# The AXIS column is the second half of the fix.  It is the set of JSON leaf
# paths the perturbation is permitted to move, and it is checked EXACTLY: the
# measured symmetric leaf-difference between the rebuilt basis and the
# published value must equal it.  Widening a control silently is therefore a
# finding, and so is neutralising one, because a neutralised control has an
# empty difference and an empty difference is not the declared axis.
# ---------------------------------------------------------------------------
BASIS = "PDD-01"

# operation ::= ("SET", path, operand) | ("SWAP", pathA, pathB)
#             | ("REVERSE", path) | ("APPEND", path, template)
#             | ("TO_VARIANT", variant, deficiencyOperand)
# operand   ::= ("NEXT_DIGEST",) | ("FROM_BASIS", path) | ("LITERAL", value)
NEXT_DIGEST = ("NEXT_DIGEST",)


def _lit(value: Any) -> tuple[str, Any]:
    return ("LITERAL", value)


def _from(path: str) -> tuple[str, Any]:
    return ("FROM_BASIS", path)


# id, class, axis (exact leaf paths that may move), operations
DERIVATION: list[tuple[str, str, tuple[str, ...], list[tuple]]] = [
    ("PDD-05", "variant-separation", ("variant", "deficiency"),
     [("TO_VARIANT", "incomplete", _lit("provider-unavailable"))]),
    ("PDD-06", "inclusion", ("observationSetDigest",),
     [("SET", "observationSetDigest", NEXT_DIGEST)]),
    ("PDD-07", "inclusion", ("targetUniverseId",),
     [("SET", "targetUniverseId", _lit("universe:two"))]),
    ("PDD-08", "inclusion", ("coverageContextDigest",),
     [("SET", "coverageContextDigest", NEXT_DIGEST)]),
    ("PDD-09", "inclusion", ("planStageIds[2]",),
     [("APPEND", "planStageIds", _lit("stage:third"))]),
    ("PDD-10", "inclusion", ("rules[1].ruleId", "rules[1].artifactDigest"),
     [("APPEND", "rules", {"ruleId": _lit("rule:b"),
                           "artifactDigest": NEXT_DIGEST})]),
    ("PDD-11", "inclusion", ("policy.artifactDigest",),
     [("SET", "policy.artifactDigest", NEXT_DIGEST)]),
    ("PDD-12", "inclusion", ("policy.policyId",),
     [("SET", "policy.policyId", _lit("policy:b"))]),
    ("PDD-13", "inclusion", ("findings[0].ruleId", "findings[0].findingId",
                             "findings[0].valueDigest"),
     [("APPEND", "findings", {"ruleId": _from("rules[0].ruleId"),
                              "findingId": _lit("finding:1"),
                              "valueDigest": NEXT_DIGEST})]),
    ("PDD-14", "inclusion", ("exactCoverage[1].state",),
     [("SET", "exactCoverage[1].state", _lit("provider-unavailable"))]),
    ("PDD-15", "inclusion", ("observationSetKind", "coverageContextKind"),
     [("SWAP", "observationSetKind", "coverageContextKind")]),
    ("PDD-16", "ordering",
     ("rules[0].ruleId", "rules[0].artifactDigest",
      "rules[1].ruleId", "rules[1].artifactDigest"),
     [("SET", "rules", ("BUILD", [
         {"ruleId": _lit("rule:aa"),
          "artifactDigest": _from("observationSetDigest")},
         {"ruleId": _lit("rule:b"),
          "artifactDigest": _from("coverageContextDigest")}]))]),
    ("PDD-17", "ordering", ("planStageIds[0]", "planStageIds[1]"),
     [("REVERSE", "planStageIds")]),
]

_PATH_STEP = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]")


def _path_steps(path: str) -> list[Any]:
    steps: list[Any] = []
    position = 0
    while position < len(path):
        if path[position] == ".":
            position += 1
            continue
        match = _PATH_STEP.match(path, position)
        if match is None:
            raise RecipeError("derivation", f"unparseable path {path!r}")
        steps.append(match.group(1) if match.group(1) is not None
                     else int(match.group(2)))
        position = match.end()
    return steps


def _path_read(node: Any, path: str) -> Any:
    cur = node
    for step in _path_steps(path):
        if isinstance(step, int):
            if not isinstance(cur, list) or step >= len(cur):
                return None
            cur = cur[step]
        else:
            if not isinstance(cur, dict) or step not in cur:
                return None
            cur = cur[step]
    return cur


def _path_write(node: Any, path: str, value: Any) -> bool:
    steps = _path_steps(path)
    cur = node
    for step in steps[:-1]:
        if isinstance(step, int):
            if not isinstance(cur, list) or step >= len(cur):
                return False
            cur = cur[step]
        else:
            if not isinstance(cur, dict) or step not in cur:
                return False
            cur = cur[step]
    last = steps[-1]
    if isinstance(last, int):
        if not isinstance(cur, list) or last >= len(cur):
            return False
        cur[last] = value
    else:
        if not isinstance(cur, dict) or last not in cur:
            return False
        cur[last] = value
    return True


class _Operands:
    """Generates the derivation's computed operands.

    NEXT_DIGEST yields successive hex-nibble Digest constants -- the k-th call
    produces 'sha256:' followed by 64 copies of the (10+k)-th hex digit.  The
    counter runs across the whole corpus in vector order, so the value a given
    control receives is a function of its POSITION in the derivation, not of
    anything read from the subject.  A reordered or inserted control shifts
    every later constant and the arithmetic stops reproducing.
    """

    def __init__(self) -> None:
        self.issued = 0
        self.literals: list[tuple[str, str, Any]] = []

    def resolve(self, vector_id: str, path: str, operand: Any,
                basis: dict[str, Any]) -> Any:
        if operand == NEXT_DIGEST:
            digit = "%x" % (10 + self.issued)
            if len(digit) != 1:
                raise RecipeError("derivation",
                                  "the digest generator ran out of hex digits")
            self.issued += 1
            return "sha256:" + digit * 64
        kind, payload = operand
        if kind == "FROM_BASIS":
            value = _path_read(basis, payload)
            if value is None:
                raise RecipeError(
                    "derivation",
                    f"{vector_id}: the basis carries nothing at {payload!r}")
            return copy.deepcopy(value)
        if kind == "LITERAL":
            self.literals.append((vector_id, path, payload))
            return copy.deepcopy(payload)
        raise RecipeError("derivation", f"unknown operand {kind!r}")


def _build_template(ops: _Operands, vector_id: str, path: str,
                    template: Any, basis: dict[str, Any]) -> Any:
    if isinstance(template, dict):
        return {key: ops.resolve(vector_id, f"{path}.{key}", value, basis)
                for key, value in template.items()}
    return ops.resolve(vector_id, path, template, basis)


def derive_corpus(recipe: Recipe, v15: Any,
                  findings: list[str]) -> dict[str, Any]:
    """Rebuild all seventeen recordValues.  Nothing is read from the subject."""
    built: dict[str, Any] = {}
    literals: list[tuple[str, str, Any]] = []

    vectors = v15.get("positiveVectors")
    table = ({v["id"]: v for v in vectors
              if isinstance(v, dict) and isinstance(v.get("id"), str)}
             if isinstance(vectors, list) else {})
    for pdd_id, v15_id, source_key in V15_MODELLED:
        vector = table.get(v15_id)
        if vector is None:
            _add(findings, "R1V17-CORPUS", f"v1.5 {v15_id}",
                 f"{pdd_id} is rebuilt from this live v1.5 vector, which is "
                 f"absent")
            continue
        completion = vector.get(source_key)
        if completion is None:
            completion = (table.get(vector.get("cloneOf")) or {}).get(source_key)
        resolved = resolve_v15(v15, v15_id)
        if resolved is None or not isinstance(completion, dict):
            _add(findings, "R1V17-CORPUS", f"v1.5 {v15_id}",
                 f"{pdd_id}: could not resolve the vector or its {source_key}")
            continue
        record = field_set_record(recipe, resolved, completion)
        if record is None:
            _add(findings, "R1V17-CORPUS", f"v1.5 {v15_id}",
                 f"{pdd_id}: the fieldSetRule applied to live v1.5 did not "
                 f"yield a complete record")
            continue
        built[pdd_id] = record

    basis = built.get(BASIS)
    if basis is None:
        _add(findings, "R1V17-CORPUS", "derivation",
             f"{BASIS} could not be rebuilt from live v1.5, so no synthetic "
             f"control has a basis and NONE of them can be checked")
        return {"values": built, "literals": literals}

    ops = _Operands()
    for vector_id, _cls, _axis, operations in DERIVATION:
        candidate = copy.deepcopy(basis)
        try:
            for operation in operations:
                verb = operation[0]
                if verb == "SET":
                    _, path, operand = operation
                    if isinstance(operand, tuple) and operand[0] == "BUILD":
                        value = [_build_template(ops, vector_id,
                                                 f"{path}[{index}]", item, basis)
                                 for index, item in enumerate(operand[1])]
                    else:
                        value = ops.resolve(vector_id, path, operand, basis)
                    if not _path_write(candidate, path, value):
                        raise RecipeError(
                            "derivation",
                            f"{vector_id}: nothing at {path!r} to set")
                elif verb == "SWAP":
                    _, left, right = operation
                    lv, rv = _path_read(candidate, left), _path_read(candidate,
                                                                     right)
                    if lv is None or rv is None:
                        raise RecipeError(
                            "derivation",
                            f"{vector_id}: cannot swap {left!r} and {right!r}")
                    _path_write(candidate, left, rv)
                    _path_write(candidate, right, lv)
                elif verb == "REVERSE":
                    _, path = operation
                    value = _path_read(candidate, path)
                    if not isinstance(value, list):
                        raise RecipeError(
                            "derivation",
                            f"{vector_id}: {path!r} is not a list to reverse")
                    _path_write(candidate, path, list(reversed(value)))
                elif verb == "APPEND":
                    _, path, template = operation
                    value = _path_read(candidate, path)
                    if not isinstance(value, list):
                        raise RecipeError(
                            "derivation",
                            f"{vector_id}: {path!r} is not a list to append to")
                    value.append(_build_template(
                        ops, vector_id, f"{path}[{len(value)}]", template,
                        basis))
                elif verb == "TO_VARIANT":
                    _, variant, operand = operation
                    candidate["variant"] = variant
                    for name, _tag, _shape, presence in recipe.top:
                        if presence == f"{variant}-only":
                            candidate[name] = ops.resolve(
                                vector_id, name, operand, basis)
                else:
                    raise RecipeError("derivation", f"unknown verb {verb!r}")
        except RecipeError as exc:
            _add(findings, "R1V17-CORPUS", "derivation", exc.detail)
            continue
        built[vector_id] = candidate
    literals = ops.literals
    if ops.issued == 0:
        _add(findings, "R1V17-CORPUS", "derivation",
             "the digest generator was never called, so every perturbed digest "
             "in the corpus would be a transcription")
    return {"values": built, "literals": literals, "generated": ops.issued}


# ---------------------------------------------------------------------------
# Section 10.  Checks.
# ---------------------------------------------------------------------------
def check_posture(doc: Any, findings: list[str]) -> None:
    _eq(findings, "R1V17-POSTURE", "$.artifact", doc.get("artifact"),
        EXPECT_ARTIFACT)
    _eq(findings, "R1V17-POSTURE", "$.version", doc.get("version"),
        EXPECT_VERSION)
    _eq(findings, "R1V17-POSTURE", "$.status", doc.get("status"), EXPECT_STATUS)
    _eq(findings, "R1V17-POSTURE", "$.reviewStatus", doc.get("reviewStatus"),
        EXPECT_REVIEW_STATUS)
    _eq(findings, "R1V17-POSTURE", "$.binds", doc.get("binds"), EXPECT_BINDS)
    _eq(findings, "R1V17-POSTURE", "$.sealRecommendation",
        doc.get("sealRecommendation"), EXPECT_SEAL)
    _eq(findings, "R1V17-POSTURE", "$.evidenceGrade", doc.get("evidenceGrade"),
        EXPECT_GRADE)
    _eq(findings, "R1V17-POSTURE", "$.supersedesIfAccepted",
        doc.get("supersedesIfAccepted"), V15_PATH)
    for pointer, value in _iter_leaves(doc, "$"):
        if isinstance(value, str) and value.strip() == "[UNSET]":
            _add(findings, "R1V17-POSTURE", pointer,
                 "a placeholder verdict token survived into the emitted bytes")


_HEX64 = re.compile(r"[0-9a-f]{64}")


def _mobile_disclosure(doc: Any) -> str:
    value = _get(doc, ["measuredSelfReport", "driftDisclosure",
                       "twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING"])
    return value if isinstance(value, str) else ""


def check_frozen_inputs(doc: Any, findings: list[str]) -> None:
    rows = doc.get("frozenInputs")
    if not isinstance(rows, list):
        _add(findings, "R1V17-PIN", "$.frozenInputs",
             f"declared array, found {json_type(rows)}")
        return
    if len(rows) != EXPECT_FROZEN_INPUTS:
        _add(findings, "R1V17-PIN", "$.frozenInputs",
             f"expected {EXPECT_FROZEN_INPUTS} rows, found {len(rows)}")
    seen_paths: set[str] = set()
    for index, row in enumerate(rows):
        where = f"$.frozenInputs[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V17-PIN", where,
                 f"declared object, found {json_type(row)}")
            continue
        path = row.get("path")
        digest = row.get("sha256")
        for name, value in (("path", path), ("sha256", digest),
                            ("id", row.get("id")), ("role", row.get("role"))):
            if not isinstance(value, str):
                _add(findings, "R1V17-TYPE", f"{where}.{name}",
                     f"declared string, found {json_type(value)}")
        if not isinstance(path, str) or not isinstance(digest, str):
            continue
        if path in seen_paths:
            _add(findings, "R1V17-PIN", where, f"duplicate path {path!r}")
        seen_paths.add(path)
        if _HEX64.fullmatch(digest) is None:
            _add(findings, "R1V17-PIN", f"{where}.sha256",
                 f"{path}: {digest!r} is not 64 lowercase hexadecimal digits")
            continue
        target = pathlib.Path(path)
        target = target if target.is_absolute() else REPO / target
        try:
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
        except OSError as exc:
            _add(findings, "R1V17-PIN", f"{where}.path",
                 f"{path}: unreadable ({type(exc).__name__})")
            continue
        if actual == digest:
            continue
        if path not in DECLARED_MOBILE:
            _add(findings, "R1V17-PIN", f"{where}.sha256",
                 f"{path}: live {actual} != recorded {digest}; this row is not "
                 f"one of the two coordinator-owned documents the artifact "
                 f"declares mobile")
    # The declared-mobile permission is hard-coded above.  Require the
    # artifact's own disclosure to name exactly those two documents, so the
    # permission cannot be widened from the artifact side.
    disclosure = _mobile_disclosure(doc)
    dw = ("$.measuredSelfReport.driftDisclosure"
          ".twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING")
    if not disclosure:
        _add(findings, "R1V17-TYPE", dw, "declared a non-empty string")
    else:
        for path in sorted(DECLARED_MOBILE):
            if path.rsplit("/", 1)[-1] not in disclosure:
                _add(findings, "R1V17-PIN", dw,
                     f"the disclosure does not name {path}, which this "
                     f"instrument permits to move")
        for path in sorted(seen_paths - DECLARED_MOBILE):
            name = path.rsplit("/", 1)[-1]
            if name in disclosure and path.endswith(".md"):
                _add(findings, "R1V17-PIN", dw,
                     f"the disclosure names {path}, which is not declared "
                     f"mobile by this instrument")
    # Cross-table: this checker's own PINS must agree with the artifact's rows.
    declared = {row["path"]: row["sha256"] for row in rows
                if isinstance(row, dict) and isinstance(row.get("path"), str)
                and isinstance(row.get("sha256"), str)}
    for rel, expected in PINS.items():
        if rel in (SUBJECT_PATH, V16_CHECKER_PATH):
            continue
        if rel not in declared:
            _add(findings, "R1V17-PIN", "$.frozenInputs",
                 f"this checker pins {rel} but the artifact records no row "
                 f"for it")
        elif declared[rel] != expected:
            _add(findings, "R1V17-PIN", "$.frozenInputs",
                 f"{rel}: artifact records {declared[rel]}, this checker pins "
                 f"{expected}")


def check_declared_mobile_anchoring(doc: Any, findings: list[str]) -> None:
    """ANCHOR the two mobile rows' RECORDED digests.

    The predecessor's residual, named by its reviewer: a DECLARED_MOBILE row is
    exempt from the live comparison, and its recorded digest was then compared
    against nothing at all.  A row that is checked against nothing can carry
    any value.

    The anchor is the artifact's own driftDisclosure, which is written in prose
    in a different section and states, for each mobile document, the digest it
    carried WHEN IT WAS READ and the digest it carried AT FINALISATION.  The
    frozenInputs row must equal the finalisation digest character for
    character; the pair must be an ordered pair of two DIFFERENT well-formed
    digests, because a document that did not move is not a mobile row; and the
    live value is measured here and printed in the banner rather than absorbed.
    """
    disclosure = _mobile_disclosure(doc)
    dw = ("$.measuredSelfReport.driftDisclosure"
          ".twoCoordinatorOwnedDOCUMENTSMOVEDDURINGTHISAUTHORING")
    rows = doc.get("frozenInputs")
    recorded = {row["path"]: row["sha256"] for row in
                (rows if isinstance(rows, list) else [])
                if isinstance(row, dict) and isinstance(row.get("path"), str)
                and isinstance(row.get("sha256"), str)}
    if not disclosure:
        return
    for path in sorted(DECLARED_MOBILE):
        name = path.rsplit("/", 1)[-1]
        where = f"{dw} [{path}]"
        # The clause for this document runs from its filename to the next
        # filename or the end.  Both digests are read out of that clause only.
        start = disclosure.find(name)
        if start < 0:
            continue
        rest = disclosure[start + len(name):]
        others = [disclosure.find(other.rsplit("/", 1)[-1])
                  for other in DECLARED_MOBILE if other != path]
        cut = len(rest)
        for other in others:
            if other > start:
                cut = min(cut, other - start - len(name))
        clause = rest[:cut]
        pair = _HEX64.findall(clause)
        if len(pair) != 2:
            _add(findings, "R1V17-MOBILE-ANCHOR", where,
                 f"the disclosure clause for {name} names {len(pair)} "
                 f"well-formed digest(s); a mobile row's disclosure must name "
                 f"the read-time digest and the finalisation digest, and "
                 f"nothing else can anchor the recorded value")
            continue
        read_time, finalised = pair
        if read_time == finalised:
            _add(findings, "R1V17-MOBILE-ANCHOR", where,
                 f"{name}'s disclosed read-time and finalisation digests are "
                 f"the same value {read_time}; the row is declared MOBILE and "
                 f"exempt from the live comparison on the stated basis that it "
                 f"MOVED, and this says it did not")
        row_digest = recorded.get(path)
        if row_digest is None:
            _add(findings, "R1V17-MOBILE-ANCHOR", where,
                 f"{path} is declared mobile but carries no frozenInputs row")
            continue
        if row_digest != finalised:
            _add(findings, "R1V17-MOBILE-ANCHOR",
                 f"$.frozenInputs[{path}].sha256",
                 f"the row records {row_digest}; the driftDisclosure states "
                 f"{name} was {finalised} at finalisation.  A mobile row is "
                 f"exempt from the live comparison, so these two independently "
                 f"written statements are the only thing anchoring it and they "
                 f"must agree")
        try:
            live = hashlib.sha256((REPO / path).read_bytes()).hexdigest()
        except OSError as exc:
            _add(findings, "R1V17-MOBILE-ANCHOR", f"$.frozenInputs[{path}]",
                 f"{path}: unreadable ({type(exc).__name__})")
            continue
        if live == row_digest:
            _add(findings, "R1V17-MOBILE-ANCHOR", f"$.frozenInputs[{path}]",
                 f"{path} is declared MOBILE but its live bytes match the "
                 f"recorded digest exactly; the exemption is being carried "
                 f"without cause and should be withdrawn rather than left "
                 f"standing")
    # The same disclosure asserts four inputs did NOT move.  That is a
    # checkable claim about live bytes and is checked here, not read.
    steady = _get(doc, ["measuredSelfReport", "driftDisclosure",
                        "theSUBJECTSDIDNOTMOVE"])
    sw = "$.measuredSelfReport.driftDisclosure.theSUBJECTSDIDNOTMOVE"
    if not isinstance(steady, str):
        _add(findings, "R1V17-TYPE", sw,
             f"declared string, found {json_type(steady)}")
        return
    named = 0
    for rel in (V15_PATH, EP8_PATH, ARCH_PLAN_PATH):
        leaf = rel.rsplit("/", 1)[-1]
        if leaf not in steady:
            continue
        named += 1
        try:
            live = hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
        except OSError:
            continue
        if live not in steady:
            _add(findings, "R1V17-MOBILE-ANCHOR", sw,
                 f"the disclosure says {leaf} did not move, but its live "
                 f"digest {live} does not occur in the disclosed values")
    if named == 0:
        _add(findings, "R1V17-MOBILE-ANCHOR", sw,
             "the disclosure names none of the pinned subjects, so its "
             "did-not-move claim cannot be adjudicated against live bytes")


def declared_mobile_drift(doc: Any) -> list[str]:
    """The permitted drift, MEASURED and REPORTED rather than absorbed.

    Freeze 7.2.1 rule 4: drift is a fact about the conditions and is recorded,
    not silently re-baselined.  These rows are not findings -- the artifact
    declares them mobile and states no published digest depends on them, and
    this instrument never reads either document's CONTENT -- but the values are
    printed, and (unlike the predecessor) the recorded side is anchored by
    check_declared_mobile_anchoring above.
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
            out.append(f"{path}: recorded {digest} (anchored to the "
                       f"driftDisclosure finalisation value), live {actual}")
    return out


def check_predecessor(doc: Any, findings: list[str]) -> None:
    _eq(findings, "R1V17-PREDECESSOR", "$.predecessor.path",
        _get(doc, ["predecessor", "path"]), V15_PATH)
    _eq(findings, "R1V17-PREDECESSOR", "$.predecessor.sha256",
        _get(doc, ["predecessor", "sha256"]), PINS[V15_PATH])
    report = doc.get("measuredSelfReport")
    if not isinstance(report, dict):
        _add(findings, "R1V17-TYPE", "$.measuredSelfReport",
             f"declared object, found {json_type(report)}")
        return
    for key, expected in (
            ("predecessorSha256AtStartOfAuthoring", PINS[V15_PATH]),
            ("predecessorSha256AtEmit", PINS[V15_PATH]),
            ("archPlanSha256AtStartOfAuthoring", PINS[ARCH_PLAN_PATH]),
            ("archPlanSha256AtEmit", PINS[ARCH_PLAN_PATH]),
            ("checkerSha256AtEmit_readOnly", PINS[V15_CHECKER_PATH])):
        _eq(findings, "R1V17-PREDECESSOR", f"$.measuredSelfReport.{key}",
            report.get(key), expected)


def check_carry(doc: Any, v15: Any, findings: list[str]) -> None:
    preservation = doc.get("preservationOfV15")
    if not isinstance(preservation, dict):
        _add(findings, "R1V17-TYPE", "$.preservationOfV15",
             f"declared object, found {json_type(preservation)}")
        return
    rows = preservation.get("carriedKeys")
    if not isinstance(rows, list) or len(rows) != EXPECT_CARRIED_KEYS:
        _add(findings, "R1V17-CARRY", "$.preservationOfV15.carriedKeys",
             f"expected {EXPECT_CARRIED_KEYS} rows, found "
             f"{len(rows) if isinstance(rows, list) else json_type(rows)}")
        rows = rows if isinstance(rows, list) else []
    carried: list[str] = []
    for index, row in enumerate(rows):
        where = f"$.preservationOfV15.carriedKeys[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V17-TYPE", where,
                 f"declared object, found {json_type(row)}")
            continue
        key = row.get("key")
        claim = row.get("identicalToV15")
        if not isinstance(key, str) or not isinstance(claim, str):
            _add(findings, "R1V17-TYPE", where,
                 "key and identicalToV15 are declared strings")
            continue
        carried.append(key)
        if claim != "YES":
            _add(findings, "R1V17-CARRY", f"{where}.identicalToV15",
                 f"expected 'YES'; got {claim!r}")
        if key not in v15:
            _add(findings, "R1V17-CARRY", f"{where}.key",
                 f"{key!r} is claimed carried but is absent from live v1.5")
            continue
        if key not in doc:
            _add(findings, "R1V17-CARRY", f"{where}.key",
                 f"{key!r} is claimed carried but is absent from v1.6")
            continue
        if canon(doc[key]) != canon(v15[key]):
            _add(findings, "R1V17-CARRY", f"$.{key}",
                 "canonical bytes differ from live v1.5 at the same key")
    _eq(findings, "R1V17-CARRY", "$.preservationOfV15.allCarriedKeysIdentical",
        preservation.get("allCarriedKeysIdentical"), "YES")

    differ = preservation.get("keysThatDIFFERByDesign")
    added = preservation.get("keysADDED")
    if isinstance(differ, dict) and isinstance(added, list):
        expected_differ = sorted(set(v15) - set(carried))
        if sorted(differ) != expected_differ:
            _add(findings, "R1V17-CARRY",
                 "$.preservationOfV15.keysThatDIFFERByDesign",
                 f"declared {sorted(differ)}; live v1.5 keys not carried are "
                 f"{expected_differ}")
        expected_added = sorted(set(doc) - set(v15))
        if sorted(added) != expected_added:
            _add(findings, "R1V17-CARRY", "$.preservationOfV15.keysADDED",
                 f"declared {sorted(added)}; measured {expected_added}")
    else:
        _add(findings, "R1V17-TYPE", "$.preservationOfV15",
             "keysThatDIFFERByDesign is an object and keysADDED an array")

    for key, expect_len, claim_key in (
            ("reviewRequests", EXPECT_V15_REVIEW_REQUESTS,
             "reviewRequestsPrefixIdentical"),
            ("residuals", EXPECT_V15_RESIDUALS, "residualsPrefixIdentical")):
        old = v15.get(key)
        new = doc.get(key)
        if not isinstance(old, list) or not isinstance(new, list):
            _add(findings, "R1V17-TYPE", f"$.{key}",
                 "declared array in both v1.5 and v1.6")
            continue
        if len(old) != expect_len:
            _add(findings, "R1V17-CARRY", f"v1.5 $.{key}",
                 f"expected {expect_len} rows in the predecessor, found "
                 f"{len(old)}")
        if len(new) < len(old) or canon(new[:len(old)]) != canon(old):
            _add(findings, "R1V17-CARRY", f"$.{key}",
                 "the v1.5 prefix is not carried verbatim")
        _eq(findings, "R1V17-CARRY", f"$.preservationOfV15.{claim_key}",
            preservation.get(claim_key), "YES")

    for key, expect_len in (("closedTypes", EXPECT_CLOSED_TYPES),
                            ("positiveVectors", EXPECT_POSITIVE_VECTORS),
                            ("adversarialControls", EXPECT_ADVERSARIAL),
                            ("staticClosureFixtures", EXPECT_STATIC_FIXTURES)):
        node = doc.get(key)
        size = len(node) if isinstance(node, (list, dict)) else None
        if size != expect_len:
            _add(findings, "R1V17-CARRY", f"$.{key}",
                 f"expected {expect_len} members, found {size}")

    # The placeholders themselves.  A successor that quietly replaced
    # sha256:5555.. with a real digest would have edited the carried vectors.
    values: set[str] = set()
    positions: list[str] = []
    for pointer, value in _iter_leaves(doc.get("positiveVectors"),
                                       "$.positiveVectors"):
        if (pointer.endswith(".derivationDigest") and isinstance(value, str)
                and value.startswith("sha256:") and len(set(value[7:])) == 1):
            values.add(value)
            positions.append(pointer)
    if len(values) != EXPECT_PLACEHOLDER_VALUES:
        _add(findings, "R1V17-CARRY", "$.positiveVectors",
             f"expected {EXPECT_PLACEHOLDER_VALUES} distinct derivationDigest "
             f"placeholders, found {len(values)}: {sorted(values)}")
    if len(positions) != EXPECT_PLACEHOLDER_POSITIONS:
        _add(findings, "R1V17-CARRY", "$.positiveVectors",
             f"expected {EXPECT_PLACEHOLDER_POSITIONS} positions carrying a "
             f"placeholder, found {len(positions)}")
    for expected in ("5" * 64, "6" * 64, "8" * 64, "9" * 64):
        if "sha256:" + expected not in values:
            _add(findings, "R1V17-CARRY", "$.positiveVectors",
                 f"the carried placeholder sha256:{expected[:4]}.. is gone")


def check_law_eighteen(doc: Any, findings: list[str]) -> None:
    """Exact-type scalar admission over $.policyDerivationIdentity.

    IMPLEMENTATION-FREEZE.md section 6 law 18.  This class defeated C-2 at v3,
    v5, v6, v7 and v8 successively, each time inside the repair's own
    self-certification.  The section publishes every count as a JSON STRING
    precisely so that 17.0 and true cannot pass for 17.
    """
    section = doc.get("policyDerivationIdentity")
    if not isinstance(section, dict):
        _add(findings, "R1V17-TYPE", "$.policyDerivationIdentity",
             f"declared object, found {json_type(section)}")
        return
    int_leaves = 0
    for pointer, value in _iter_leaves(section, "$.policyDerivationIdentity"):
        if pointer in SECTION_INT_LEAVES:
            int_leaves += 1
            if isinstance(value, bool) or not isinstance(value, int):
                _add(findings, "R1V17-TYPE", pointer,
                     f"declared exact integer, found {json_type(value)}; a "
                     f"float is not an integer and a boolean is not an integer")
            continue
        if not isinstance(value, str):
            _add(findings, "R1V17-TYPE", pointer,
                 f"declared string, found {json_type(value)}; every leaf of "
                 f"this section is a string except the five carried "
                 f"workedExample.completion integers")
    if int_leaves != EXPECT_SECTION_INT_LEAVES:
        _add(findings, "R1V17-TYPE", "$.policyDerivationIdentity",
             f"expected {EXPECT_SECTION_INT_LEAVES} declared integer leaves, "
             f"reached {int_leaves}")
    _eq(findings, "R1V17-TYPE",
        "$.policyDerivationIdentity.lawEighteenScope.rule",
        _get(section, ["lawEighteenScope", "rule"]),
        "IMPLEMENTATION-FREEZE.md section 6 law 18 -- closed-scalar admission "
        "is exact-type.")


def admit_record_value(recipe: Recipe, value: Any, where: str,
                       findings: list[str]) -> bool:
    """Exact-type AND live-v1.5-vocabulary admission of a published recordValue
    BEFORE it is encoded.

    The predecessor stopped at the JSON type.  That is why a `sha856:` prefix
    and a well-formed-but-wrong `state` both survived it: both are strings.
    Here every leaf is additionally put to LIVE v1.5's closed type for that
    position -- the Digest pattern, the OpaqueId pattern, the CoverageState and
    FactDeficiency vocabularies -- and a refusal NAMES the rule it failed.
    """
    if not isinstance(value, dict):
        _add(findings, "R1V17-TYPE", where,
             f"declared object, found {json_type(value)}")
        return False
    ok = True
    extra = sorted(set(value) - set(recipe.top_names))
    if extra:
        _add(findings, "R1V17-TYPE", where,
             f"undeclared field(s) {extra} in PolicyDerivationInputV1")
        ok = False

    def admit_leaf(owner: str, name: str, item: Any, position: str) -> bool:
        spec = recipe.leaf_types.get((owner, name))
        if spec is None:
            if not isinstance(item, str):
                _add(findings, "R1V17-TYPE", position,
                     f"declared string, found {json_type(item)}")
                return False
            return True
        refusal = spec.admits(item)
        if refusal is None:
            return True
        _add(findings, "R1V17-VOCABULARY", position,
             f"{item!r} {refusal}")
        return False

    for name, _tag, shape, presence in recipe.top:
        if name not in value:
            if presence == "required":
                _add(findings, "R1V17-TYPE", f"{where}.{name}",
                     "required field absent")
                ok = False
            continue
        item = value[name]
        if shape is TEXT:
            ok = admit_leaf("", name, item, f"{where}.{name}") and ok
            continue
        if shape[0] == "record":
            ok = _admit_nested(recipe, item, shape[1], f"{where}.{name}",
                               findings) and ok
            continue
        if not isinstance(item, list):
            _add(findings, "R1V17-TYPE", f"{where}.{name}",
                 f"declared array, found {json_type(item)}")
            ok = False
            continue
        if shape[0] == "scalar-array":
            for index, member in enumerate(item):
                ok = admit_leaf("", name, member,
                                f"{where}.{name}[{index}]") and ok
        else:
            for index, member in enumerate(item):
                ok = _admit_nested(recipe, member, shape[2],
                                   f"{where}.{name}[{index}]", findings) and ok
    return ok


def _admit_nested(recipe: Recipe, value: Any, name: str, where: str,
                  findings: list[str]) -> bool:
    if not isinstance(value, dict):
        _add(findings, "R1V17-TYPE", where,
             f"declared object, found {json_type(value)}")
        return False
    _record_tag, fields = recipe.nested[name]
    declared = [field for field, _ in fields]
    ok = True
    extra = sorted(set(value) - set(declared))
    if extra:
        _add(findings, "R1V17-TYPE", where,
             f"undeclared field(s) {extra} in {name}")
        ok = False
    for field in declared:
        if field not in value:
            _add(findings, "R1V17-TYPE", f"{where}.{field}",
                 "required field absent")
            ok = False
            continue
        spec = recipe.leaf_types.get((name, field))
        item = value[field]
        if spec is None:
            if not isinstance(item, str):
                _add(findings, "R1V17-TYPE", f"{where}.{field}",
                     f"declared string, found {json_type(item)}")
                ok = False
            continue
        refusal = spec.admits(item)
        if refusal is not None:
            _add(findings, "R1V17-VOCABULARY", f"{where}.{field}",
                 f"{item!r} {refusal}")
            ok = False
    return ok


def check_recipe_declaration(recipe: Recipe, doc: Any,
                             findings: list[str]) -> None:
    """The recipe was DERIVED above.  What is left to check is that the
    artifact's prose statement of it agrees with the derivation, and that the
    wire type it publishes is the one live v1.5 gives the field."""
    section = _get(doc, ["policyDerivationIdentity"], {})
    _eq(findings, "R1V17-RECIPE", "$.policyDerivationIdentity.id",
        section.get("id"), "POLICY-DERIVATION-DIGEST-V1")
    _eq(findings, "R1V17-RECIPE", "$.policyDerivationIdentity.field",
        section.get("field"), "policyOutcome.derivationDigest")
    # The published wireType must be the pattern live v1.5 gives a Digest.  The
    # artifact says it is "carried unchanged from closedTypes.Digest"; that is
    # a checkable claim and it is checked, not read.
    digest_spec = recipe.leaf_types.get(("", "observationSetDigest"))
    if digest_spec is None or digest_spec.kind != "pattern":
        _add(findings, "R1V17-RECIPE", "$.policyDerivationIdentity.wireType",
             "no live v1.5 Digest pattern was resolved, so the published wire "
             "type cannot be adjudicated")
    else:
        _eq(findings, "R1V17-RECIPE",
            "$.policyDerivationIdentity.wireType.regex",
            _get(section, ["wireType", "regex"]), digest_spec.pattern)
    _eq(findings, "R1V17-RECIPE",
        "$.policyDerivationIdentity.primitives.componentFrame.bytes",
        _get(section, ["primitives", "componentFrame", "bytes"]),
        "uint8(t) || uint32be(byteLength(b)) || b")
    leaf = _get(section, ["primitives", "leaf"])
    if not isinstance(leaf, str):
        _add(findings, "R1V17-TYPE", "$.policyDerivationIdentity.primitives.leaf",
             f"declared string, found {json_type(leaf)}")
    else:
        wanted = (f"SHA-256( 0x{recipe.leaf_tag:02x} || "
                  f"uint{recipe.leaf_width}be(byteLength(r)) || r )")
        if wanted not in leaf:
            _add(findings, "R1V17-RECIPE",
                 "$.policyDerivationIdentity.primitives.leaf",
                 f"the leaf rule DERIVED from live EP8, {wanted}, is not stated")
    step4 = _get(section, ["preimage", "step4_OUTER"])
    if isinstance(step4, str):
        record_tag, ns_tag, domain_tag, root_tag = recipe.outer_tags
        for token in (f"0x{record_tag:02x}",
                      f"C(0x{ns_tag:02x}, UTF8('{recipe.namespace}'))",
                      f"C(0x{domain_tag:02x}, ASCII('{recipe.domain}'))",
                      f"C(0x{root_tag:02x}, root)"):
            if token not in step4:
                _add(findings, "R1V17-RECIPE",
                     "$.policyDerivationIdentity.preimage.step4_OUTER",
                     f"the outer preimage DERIVED from live EP8 names {token}, "
                     f"which the artifact's step 4 does not")


def check_vectors(recipe: Recipe, doc: Any, corpus: dict[str, Any],
                  findings: list[str]) -> dict[str, Any]:
    """Recompute every published value FROM THE REBUILT ONE.

    The predecessor recomputed each digest from the PUBLISHED recordValue,
    which certifies hashing and nothing else.  Here the rebuilt value is
    compared against the published one FIRST, and the arithmetic then runs on
    the rebuilt value, so a corpus that was collapsed, widened, retyped or
    republished never reaches the encoder as an answer.
    """
    out: dict[str, Any] = {"records": {}, "values": {}, "digests": {},
                           "anchored": set(), "roots": {}}
    built = corpus.get("values", {})
    node = _get(doc, ["policyDerivationIdentity", "pinnedVectors"], {})
    base = "$.policyDerivationIdentity.pinnedVectors"
    _eq(findings, "R1V17-VECTOR", f"{base}.count", node.get("count"),
        str(EXPECT_PINNED_VECTORS))
    vectors = node.get("vectors")
    if not isinstance(vectors, list):
        _add(findings, "R1V17-TYPE", f"{base}.vectors",
             f"declared array, found {json_type(vectors)}")
        return out
    if len(vectors) != EXPECT_PINNED_VECTORS:
        _add(findings, "R1V17-VECTOR", f"{base}.vectors",
             f"expected {EXPECT_PINNED_VECTORS} vectors, found {len(vectors)}")
    seen: set[str] = set()
    max_text = 0
    for index, vector in enumerate(vectors):
        where = f"{base}.vectors[{index}]"
        if not isinstance(vector, dict):
            _add(findings, "R1V17-TYPE", where,
                 f"declared object, found {json_type(vector)}")
            continue
        vid = vector.get("id")
        if not isinstance(vid, str):
            _add(findings, "R1V17-TYPE", f"{where}.id",
                 f"declared string, found {json_type(vid)}")
            continue
        if vid in seen:
            _add(findings, "R1V17-VECTOR", f"{where}.id",
                 f"duplicate vector id {vid!r}")
        seen.add(vid)
        published = vector.get("recordValue")
        if not admit_record_value(recipe, published, f"{where}.recordValue",
                                  findings):
            continue

        # ---- THE ANCHOR.  CIR-B1.  ------------------------------------
        rebuilt = built.get(vid)
        if rebuilt is None:
            _add(findings, "R1V17-ANCHOR", f"{where}.recordValue",
                 f"{vid}: this instrument has no external derivation for this "
                 f"vector, so its content would be certified only by hashing "
                 f"it consistently.  A vector that only has to hash "
                 f"consistently is not a vector")
            continue
        if canon(rebuilt) != canon(published):
            _add(findings, "R1V17-ANCHOR", f"{where}.recordValue",
                 f"{vid}: the published recordValue is not what this vector's "
                 f"external derivation produces.  Rebuilt "
                 f"{canon(rebuilt).decode('utf-8')}; published "
                 f"{canon(published).decode('utf-8')}")
            continue
        out["anchored"].add(vid)
        value = rebuilt

        for _pointer, leaf in _iter_leaves(value, ""):
            if isinstance(leaf, str):
                max_text = max(max_text, len(leaf.encode("utf-8")))
        try:
            record_a = encode_a(recipe, value)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V17-VECTOR", f"{where}.recordValue",
                 f"{vid}: encoder A refused a derived vector: "
                 f"{type(exc).__name__}: {exc}")
            continue
        try:
            record_b = encode_b(recipe, value)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V17-VECTOR", f"{where}.recordValue",
                 f"{vid}: encoder B refused a derived vector: "
                 f"{type(exc).__name__}: {exc}")
            continue
        if record_a != record_b:
            _add(findings, "R1V17-ENCODER-DISAGREE", f"{where}.recordValue",
                 f"{vid}: the two independent encoders produced different "
                 f"record bytes")
            continue
        digest_a = a_derivation_digest(recipe, record_a)
        digest_b = b_digest(recipe, record_b)
        if digest_a != digest_b:
            _add(findings, "R1V17-ENCODER-DISAGREE", where,
                 f"{vid}: the two independent encoders produced different "
                 f"derivationDigest values")
            continue
        out["records"][vid] = record_a
        out["values"][vid] = value
        out["digests"][vid] = digest_a

        root = a_leaf_root(recipe, record_a)
        out["roots"][vid] = root.hex()
        expected = {
            "recordBytes": str(len(record_a)),
            "recordSha256": "sha256:" + hashlib.sha256(record_a).hexdigest(),
            "leafRootHex": root.hex(),
            "outerPreimageHex": a_outer(recipe, root).hex(),
            "derivationDigest": digest_a,
        }
        if "completeRecordHex" in vector:
            expected["completeRecordHex"] = record_a.hex()
        for key, want in expected.items():
            _eq(findings, "R1V17-VECTOR", f"{where}.{key} [{vid}]",
                vector.get(key), want)
        _eq(findings, "R1V17-VECTOR", f"{where}.decoderRoundTripLiteral [{vid}]",
            vector.get("decoderRoundTripLiteral"), "YES")
        if b_hex(record_b) != record_a.hex():
            _add(findings, "R1V17-ENCODER-DISAGREE", where,
                 f"{vid}: the two hex renderings differ")
    if max_text != EXPECT_MAX_TEXT_BYTES:
        _add(findings, "R1V17-VECTOR", f"{base}.vectors",
             f"the longest text component across all vectors measures "
             f"{max_text} bytes; {EXPECT_MAX_TEXT_BYTES} is expected")
    return out


def check_non_degeneracy(recipe: Recipe, doc: Any, corpus: dict[str, Any],
                         recomputed: dict[str, Any],
                         findings: list[str]) -> None:
    """The published corpus must be NON-DEGENERATE.  CIR-B1.

    Three requirements, each measured:
      (1) every vector is externally anchored -- four to LIVE v1.5 through the
          fieldSetRule, thirteen to the rebuilt PDD-01 through the declared
          derivation;
      (2) the corpus is pairwise DISTINCT on recordValue, record bytes, leaf
          root and derivationDigest, because the artifact publishes seventeen
          separate rows and a row that duplicates another is not a row;
      (3) every declared perturbation actually MOVES the basis, and moves
          EXACTLY the leaves its axis names -- no fewer (a neutralised control)
          and no more (a widened one).
    """
    base = "$.policyDerivationIdentity.pinnedVectors"
    anchored = recomputed.get("anchored", set())
    if len(anchored) != EXPECT_EXTERNALLY_ANCHORED:
        _add(findings, "R1V17-ANCHOR", f"{base}.vectors",
             f"{len(anchored)} of {EXPECT_EXTERNALLY_ANCHORED} published "
             f"vectors are externally anchored; the rest would be certified "
             f"only by being hashed consistently")
    from_v15 = {pdd for pdd, _v, _s in V15_MODELLED} & anchored
    from_basis = {vid for vid, _c, _a, _o in DERIVATION} & anchored
    if len(from_v15) != EXPECT_DERIVED_FROM_V15:
        _add(findings, "R1V17-ANCHOR", f"{base}.vectors",
             f"{len(from_v15)} vectors were rebuilt from live v1.5; "
             f"{EXPECT_DERIVED_FROM_V15} is expected")
    if len(from_basis) != EXPECT_DERIVED_FROM_BASIS:
        _add(findings, "R1V17-ANCHOR", f"{base}.vectors",
             f"{len(from_basis)} vectors were rebuilt from the derived basis; "
             f"{EXPECT_DERIVED_FROM_BASIS} is expected")

    # (2) pairwise distinctness, on every axis the artifact publishes.
    for label, table in (("recordValue", {k: canon(v) for k, v in
                                          recomputed["values"].items()}),
                         ("record bytes", recomputed["records"]),
                         ("leafRootHex", recomputed["roots"]),
                         ("derivationDigest", recomputed["digests"])):
        buckets: dict[Any, list[str]] = {}
        for vid, value in table.items():
            buckets.setdefault(value, []).append(vid)
        for value, members in sorted(buckets.items(),
                                     key=lambda item: sorted(item[1])):
            if len(members) > 1:
                _add(findings, "R1V17-DEGENERATE", f"{base}.vectors",
                     f"{len(members)} published vectors share one {label}: "
                     f"{sorted(members)}.  The artifact publishes them as "
                     f"separate rows; a row that duplicates another measures "
                     f"nothing that the row it duplicates did not already "
                     f"measure")

    # (3) axis exactness against the rebuilt basis.
    basis = corpus.get("values", {}).get(BASIS)
    if not isinstance(basis, dict):
        _add(findings, "R1V17-DEGENERATE", f"{base}.vectors",
             f"{BASIS} was not rebuilt, so no control's axis can be measured")
        return
    flat_basis = dict(_iter_leaves(basis, ""))
    covered: set[str] = set()
    for vid, _cls, axis, _ops in DERIVATION:
        value = recomputed["values"].get(vid)
        if not isinstance(value, dict):
            continue
        flat = dict(_iter_leaves(value, ""))
        moved = sorted({key for key in set(flat_basis) | set(flat)
                        if flat_basis.get(key, _MISSING)
                        != flat.get(key, _MISSING)})
        declared = sorted("." + name for name in axis)
        if not moved:
            _add(findings, "R1V17-DEGENERATE", f"{base}.vectors[{vid}]",
                 f"{vid} is byte-identical to {BASIS}.  A control that does "
                 f"not move the basis distinguishes nothing and its digest is "
                 f"{BASIS}'s own")
            continue
        if moved != declared:
            _add(findings, "R1V17-DEGENERATE", f"{base}.vectors[{vid}]",
                 f"{vid} moves {moved}; its declared axis is {declared}.  A "
                 f"control that moves less than its axis is neutralised and "
                 f"one that moves more is not the control it says it is")
            continue
        for leaf in axis:
            covered.add(leaf.split("[")[0].split(".")[0])
    # Every REQUIRED field of the record must be exercised by some control.
    # An inclusion nobody can move is an inclusion nobody can check.
    required = {name for name, _t, _s, presence in recipe.top
                if presence == "required"}
    variant_gated = {name for name, _t, _s, presence in recipe.top
                     if presence != "required"}
    unexercised = sorted((required | variant_gated) - covered)
    if unexercised:
        _add(findings, "R1V17-DEGENERATE", f"{base}.vectors",
             f"no published control moves {unexercised}; every declared "
             f"inclusion must be vector-addressable or the field set is not "
             f"exercised by the corpus that certifies it")

    # The DECLARED operands must be admissible under live v1.5 and must
    # actually differ from what they replace.  This is the residual named in
    # NOT_VERIFIED, bounded as tightly as an instrument can bound it.
    for vid, path, literal in corpus.get("literals", []):
        where = f"derivation[{vid}].{path}"
        owner, leaf = _leaf_owner(recipe, path)
        spec = recipe.leaf_types.get((owner, leaf))
        if spec is None:
            _add(findings, "R1V17-DEGENERATE", where,
                 f"the declared operand at {path!r} has no live v1.5 type, so "
                 f"nothing outside this file constrains it")
            continue
        refusal = spec.admits(literal)
        if refusal is not None:
            _add(findings, "R1V17-VOCABULARY", where, f"{literal!r} {refusal}")
        replaced = _path_read(basis, path)
        if replaced is not None and replaced == literal:
            _add(findings, "R1V17-DEGENERATE", where,
                 f"the declared operand {literal!r} equals the basis value it "
                 f"replaces, so the perturbation is a no-op")


class _Missing:
    def __repr__(self) -> str:
        return "<absent>"


_MISSING = _Missing()


def _leaf_owner(recipe: Recipe, path: str) -> tuple[str, str]:
    """Which (nested type, field) a derivation path addresses, so the operand
    can be put to the same live-v1.5 rule the encoder applies."""
    steps = [step for step in _path_steps(path) if isinstance(step, str)]
    if not steps:
        return "", path
    if len(steps) == 1:
        return "", steps[0]
    head, leaf = steps[0], steps[-1]
    for name, _tag, shape, _presence in recipe.top:
        if name != head or not isinstance(shape, tuple):
            continue
        if shape[0] == "record":
            return shape[1], leaf
        if shape[0] == "record-array":
            return shape[2], leaf
    return "", leaf


# ---------------------------------------------------------------------------
# Section 11.  Semantics.  The prose that carries a checkable claim.
#
# Requirement: bind against an input that is WRONG, not merely EMPTY.  The
# predecessor fired on removal and stayed silent on falsity -- measured, its
# `models` strings could be permuted arbitrarily at zero findings, so a control
# could claim to exercise deps.policy.policyId while exercising
# stageInput.targetUniverseId.
#
# The designators below are DERIVED, never typed: each record field's
# designator set is built from the artifact's own recordGrammar `source`
# column, the field's own name, and the LIVE v1.5 type name that owns the leaf.
# A control's prose must name at least one designator of the axis it moves and
# NO designator that belongs exclusively to a field it does not move.
# ---------------------------------------------------------------------------
def _designators(recipe: Recipe, v15: Any) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for name, _tag, shape, _presence in recipe.top:
        tokens = {name}
        source = recipe.field_source.get(name)
        if isinstance(source, str):
            head = re.split(r"[,;]| -- ", source, maxsplit=1)[0].strip().rstrip(".")
            if re.fullmatch(r"[\w:*.\[\]]+", head):
                tokens.add(head)
                # A source of the form a.b.entries also designates a.b, which
                # is how the corpus names a list without its container field.
                if head.endswith(".entries"):
                    tokens.add(head[:-len(".entries")])
        # The live v1.5 type that owns this leaf, qualified by the leaf name.
        # This is what lets a control name CanonicalValueRef.kind, which is a
        # live v1.5 identity and appears nowhere in the record's own field list.
        if isinstance(source, str):
            head = re.split(r"[,;]| -- ", source, maxsplit=1)[0].strip()
            tail = head.rstrip(".").split(".")[-1]
            owner = _leaf_owner_type(recipe, v15, name)
            if owner is not None and tail:
                tokens.add(f"{owner}.{tail}")
        if isinstance(shape, tuple) and shape[0] in ("record", "record-array"):
            nested = shape[1] if shape[0] == "record" else shape[2]
            for field, _t in recipe.nested[nested][1]:
                tokens.add(f"{name}.{field}")
                tokens.add(f"{nested}.{field}")
        out[name] = {token for token in tokens if len(token) >= 5}
    return out


def _leaf_owner_type(recipe: Recipe, v15: Any, field: str) -> str | None:
    """The LIVE v1.5 type that owns a top-level text leaf, e.g.
    observationSetKind -> CanonicalValueRef."""
    source = recipe.field_source.get(field)
    if not isinstance(source, str):
        return None
    head = re.split(r"[,;]| -- ", source, maxsplit=1)[0].strip().rstrip(".")
    parts = head.split(".")
    if len(parts) < 2 or parts[0] not in _SOURCE_ROOTS:
        return None
    try:
        node, owner, _owner_node = _walk_v15(
            v15, _SOURCE_ROOTS[parts[0]][0], parts[1:-1], "designator")
    except RecipeError:
        return None
    # _walk_v15 dereferences a $ref only when it needs to take another step, so
    # the container the LAST step lands in may still be an unfollowed $ref.
    # Follow it here: observationSet is a $ref to CanonicalValueRef, and
    # CanonicalValueRef -- not SealedStageInput -- is the identity a control
    # naming that leaf would use.
    seen: set[str] = set()
    while isinstance(node, dict) and isinstance(node.get("$ref"), str):
        ref = node["$ref"]
        if ref in seen:
            return owner
        seen.add(ref)
        owner = ref
        node = _get(v15, ["closedTypes", ref])
    return owner


def _nested_leaf_tokens(recipe: Recipe, axis: tuple[str, ...]) -> set[str]:
    """Leaf-level tokens, so two controls on the same container field --
    policy.policyId and policy.artifactDigest -- are still separable."""
    tokens: set[str] = set()
    for leaf in axis:
        steps = [step for step in _path_steps(leaf) if isinstance(step, str)]
        if len(steps) > 1:
            tokens.add(steps[-1])
    return tokens


def check_models_axis(recipe: Recipe, doc: Any, v15: Any,
                      findings: list[str]) -> int:
    """Each control's prose, cross-checked against the axis it moves, BOTH ways."""
    base = "$.policyDerivationIdentity.pinnedVectors"
    vectors = _get(doc, ["policyDerivationIdentity", "pinnedVectors",
                         "vectors"])
    if not isinstance(vectors, list):
        return 0
    prose = {}
    for index, vector in enumerate(vectors):
        if isinstance(vector, dict) and isinstance(vector.get("id"), str):
            prose[vector["id"]] = (index, vector.get("models"),
                                   vector.get("note"))
    designators = _designators(recipe, v15)
    checked = 0
    for vid, cls, axis, _ops in DERIVATION:
        if vid not in prose:
            _add(findings, "R1V17-SEMANTICS", f"{base}.vectors",
                 f"{vid} is derived here but is not published")
            continue
        index, models, _note = prose[vid]
        where = f"{base}.vectors[{index}].models [{vid}]"
        if not isinstance(models, str) or not models:
            _add(findings, "R1V17-TYPE", where, "declared a non-empty string")
            continue
        checked += 1
        axis_fields = {leaf.split("[")[0].split(".")[0] for leaf in axis}
        wanted: set[str] = set()
        for field in axis_fields:
            wanted |= designators.get(field, set())
        wanted |= _nested_leaf_tokens(recipe, axis)
        hits = sorted(token for token in wanted if token in models)
        if not hits:
            _add(findings, "R1V17-SEMANTICS", where,
                 f"{vid} moves {sorted(axis)} but its prose names none of the "
                 f"designators of {sorted(axis_fields)} ({sorted(wanted)}).  A "
                 f"control whose prose does not name what it exercises cannot "
                 f"be read as evidence for that field")
        # The other direction, and the one every instrument in this lineage
        # missed: prose that names a field this control does NOT move.
        for field, tokens in sorted(designators.items()):
            if field in axis_fields:
                continue
            exclusive = {token for token in tokens
                         if not any(token in other or other in token
                                    for other in wanted)}
            named = sorted(token for token in exclusive if token in models)
            if named:
                _add(findings, "R1V17-SEMANTICS", where,
                     f"{vid} moves {sorted(axis)}, but its prose names "
                     f"{named}, which designate {field!r} -- a field this "
                     f"control does not touch.  An inverted claim is a false "
                     f"claim even when the arithmetic under it is correct")
        # The class token: an inclusion control must say so, an ordering
        # control must say so.  Classes are this instrument's, not the file's.
        marker = {"inclusion": "inclusion control",
                  "ordering": "ordering",
                  "variant-separation": "variant"}[cls]
        if marker not in models.lower() and marker not in models:
            _add(findings, "R1V17-SEMANTICS", where,
                 f"{vid} is derived here as a {cls} control; its prose does "
                 f"not carry the {marker!r} marker")
    return checked


def check_required_kind(recipe: Recipe, doc: Any, v15: Any,
                        recomputed: dict[str, Any],
                        findings: list[str]) -> int:
    """LIVE v1.5 constrains observationSet.kind and coverageContext.kind by
    `requiredKind`.  Exactly one published vector violates it -- the control
    that exists to move those two leaves -- and its prose says so.  Both halves
    are MEASURED here rather than read.
    """
    base = "$.policyDerivationIdentity.pinnedVectors"
    stage = _get(v15, ["closedTypes", "SealedStageInput", "fields"])
    if not isinstance(stage, dict):
        _add(findings, "R1V17-TYPE", "v1.5 $.closedTypes.SealedStageInput.fields",
             f"declared object, found {json_type(stage)}")
        return 0
    required: dict[str, str] = {}
    for name, _tag, _shape, _presence in recipe.top:
        source = recipe.field_source.get(name)
        if not isinstance(source, str):
            continue
        head = re.split(r"[,;]| -- ", source, maxsplit=1)[0].strip().rstrip(".")
        parts = head.split(".")
        if len(parts) != 3 or parts[0] != "stageInput" or parts[2] != "kind":
            continue
        node = stage.get(parts[1])
        if isinstance(node, dict) and isinstance(node.get("requiredKind"), str):
            required[name] = node["requiredKind"]
    if not required:
        _add(findings, "R1V17-SEMANTICS", "v1.5 $.closedTypes.SealedStageInput",
             "live v1.5 declares no requiredKind constraint, so the CanonicalValueRef "
             "control has nothing outside this file to be measured against")
        return 0
    violators: list[str] = []
    for vid, value in sorted(recomputed["values"].items()):
        for name, wanted in sorted(required.items()):
            if value.get(name) != wanted:
                violators.append(vid)
                break
    if len(violators) != EXPECT_REQUIREDKIND_VIOLATORS:
        _add(findings, "R1V17-SEMANTICS", f"{base}.vectors",
             f"{len(violators)} published vectors violate live v1.5's "
             f"requiredKind constraint ({violators}); "
             f"{EXPECT_REQUIREDKIND_VIOLATORS} is expected, and a corpus that "
             f"cannot say which of its vectors is unreachable from a "
             f"conforming host is not describing a reachable field set")
    vectors = _get(doc, ["policyDerivationIdentity", "pinnedVectors",
                         "vectors"], [])
    prose = {v["id"]: (i, v) for i, v in enumerate(vectors)
             if isinstance(v, dict) and isinstance(v.get("id"), str)}
    for vid in violators:
        index, vector = prose.get(vid, (None, {}))
        note = str(vector.get("note", "")) + " " + str(vector.get("models", ""))
        if "INVALID" not in note:
            _add(findings, "R1V17-SEMANTICS",
                 f"{base}.vectors[{index}] [{vid}]",
                 f"{vid} violates live v1.5's requiredKind constraint "
                 f"({required}) and is therefore unreachable from a conforming "
                 f"host, but its prose does not say so.  An unreachable vector "
                 f"published as reachable misdescribes the corpus")
    for vid in sorted(recomputed["values"]):
        if vid in violators:
            continue
        index, vector = prose.get(vid, (None, {}))
        note = str(vector.get("note", ""))
        if "INVALID under v1.5" in note:
            _add(findings, "R1V17-SEMANTICS",
                 f"{base}.vectors[{index}] [{vid}]",
                 f"{vid} is declared INVALID under live v1.5, but measured "
                 f"against live v1.5's requiredKind it is valid")
    return len(violators)


# ---------------------------------------------------------------------------
# Section 12.  WRONGNESS PROBES.
#
# Requirement 2, stated by the reviewer as the shape every instrument in this
# session shared: they fired on REMOVAL and stayed silent on FALSITY.  Deleting
# a field, emptying a list and dropping a row were all caught; a value that was
# present, well-formed and WRONG was not.
#
# Each probe below constructs a subject that is WRONG rather than EMPTY, runs
# THE REAL CHECK over it, and requires a finding carrying a NAMED code.  A
# probe that produced no finding, or a finding under some unrelated code, is an
# escape and is reported as one.  These run inside the ordinary check pass, not
# only under --selftest, because a guard that is only exercised by a flag is a
# guard the ordinary run does not have.
# ---------------------------------------------------------------------------
def _republish(recipe: Recipe, doc: Any) -> Any:
    """Recompute every published field of every vector from its (mutated)
    recordValue, exactly as the predecessor's own encoder would.

    This is the manoeuvre that defeated the predecessor: after it, every
    arithmetic comparison it made was self-consistent.  It is performed here so
    that the probes are the real attack and not a weaker one.
    """
    vectors = _get(doc, ["policyDerivationIdentity", "pinnedVectors",
                         "vectors"], [])
    for vector in vectors:
        if not isinstance(vector, dict) or "recordValue" not in vector:
            continue
        try:
            record = encode_a(recipe, vector["recordValue"])
        except (ValueError, TypeError):
            continue
        root = a_leaf_root(recipe, record)
        vector["recordBytes"] = str(len(record))
        vector["recordSha256"] = "sha256:" + hashlib.sha256(record).hexdigest()
        vector["leafRootHex"] = root.hex()
        vector["outerPreimageHex"] = a_outer(recipe, root).hex()
        vector["derivationDigest"] = a_derivation_digest(recipe, record)
        if "completeRecordHex" in vector:
            vector["completeRecordHex"] = record.hex()
    return doc


def _vector_index(doc: Any, vid: str) -> int | None:
    vectors = _get(doc, ["policyDerivationIdentity", "pinnedVectors",
                         "vectors"], [])
    for index, vector in enumerate(vectors):
        if isinstance(vector, dict) and vector.get("id") == vid:
            return index
    return None


def _wrongness_cases() -> list[tuple[str, str, str, Callable[[Any], bool]]]:
    """(id, expected code, what it models, mutation).  The mutation returns
    True if it applied; a mutation that cannot apply is itself an escape."""

    def rv(doc: Any, vid: str) -> Any:
        index = _vector_index(doc, vid)
        if index is None:
            return None
        return _get(doc, ["policyDerivationIdentity", "pinnedVectors",
                          "vectors", index, "recordValue"])

    def collapse(doc: Any) -> bool:
        source = rv(doc, BASIS)
        target_index = _vector_index(doc, "PDD-07")
        if source is None or target_index is None:
            return False
        _get(doc, ["policyDerivationIdentity", "pinnedVectors", "vectors",
                   target_index])["recordValue"] = copy.deepcopy(source)
        return True

    def collapse_many(doc: Any) -> bool:
        source = rv(doc, BASIS)
        if source is None:
            return False
        moved = 0
        for vid in ("PDD-05", "PDD-06", "PDD-07", "PDD-08", "PDD-09",
                    "PDD-10", "PDD-11", "PDD-12", "PDD-13", "PDD-14"):
            index = _vector_index(doc, vid)
            if index is None:
                continue
            _get(doc, ["policyDerivationIdentity", "pinnedVectors", "vectors",
                       index])["recordValue"] = copy.deepcopy(source)
            moved += 1
        return moved == 10

    def bad_prefix(doc: Any) -> bool:
        value = rv(doc, "PDD-06")
        if not isinstance(value, dict):
            return False
        value["observationSetDigest"] = "sha856:" + "a" * 64
        return True

    def wrong_digest(doc: Any) -> bool:
        value = rv(doc, "PDD-08")
        if not isinstance(value, dict):
            return False
        value["coverageContextDigest"] = "sha256:" + "f" * 64
        return True

    def bad_enum(doc: Any) -> bool:
        value = rv(doc, "PDD-14")
        coverage = value.get("exactCoverage") if isinstance(value, dict) else None
        if not isinstance(coverage, list) or len(coverage) < 2:
            return False
        coverage[1]["state"] = "budget-exceeded"
        return True

    def widen(doc: Any) -> bool:
        value = rv(doc, "PDD-07")
        if not isinstance(value, dict):
            return False
        value["targetUniverseId"] = "universe:two"
        value["coverageContextDigest"] = "sha256:" + "9" * 64
        return True

    def invert(doc: Any) -> bool:
        index = _vector_index(doc, "PDD-07")
        if index is None:
            return False
        node = _get(doc, ["policyDerivationIdentity", "pinnedVectors",
                          "vectors", index])
        node["models"] = "SYNTHETIC -- inclusion control for deps.policy.policyId"
        return True

    return [
        ("W1-collapse-one-control-and-republish", "R1V17-ANCHOR",
         "a single inclusion control neutralised onto the basis, with every "
         "dependent digest recomputed by this instrument's own encoder",
         collapse),
        ("W2-collapse-ten-controls-and-republish", "R1V17-ANCHOR",
         "the reviewer's measured attack on the predecessor: ten controls "
         "collapsed onto the basis and republished, which the predecessor "
         "passed at 0 findings",
         collapse_many),
        ("W3-malformed-digest-prefix", "R1V17-VOCABULARY",
         "a leaf that is a string, is 71 bytes, and is NOT a Digest: the "
         "prefix reads sha856:",
         bad_prefix),
        ("W4-well-formed-but-wrong-digest", "R1V17-ANCHOR",
         "a Digest that satisfies live v1.5's pattern exactly and is still not "
         "the value this vector's derivation produces",
         wrong_digest),
        ("W5-out-of-vocabulary-enum", "R1V17-VOCABULARY",
         "a CoverageState that is plausible prose and is not a member of live "
         "v1.5's closed vocabulary",
         bad_enum),
        ("W6-widened-axis", "R1V17-ANCHOR",
         "a control that moves a second leaf beyond the one its prose names, "
         "so it no longer isolates the inclusion it claims to isolate",
         widen),
        ("W7-inverted-prose", "R1V17-SEMANTICS",
         "arithmetic left correct and the CLAIM inverted: a control that "
         "exercises targetUniverseId while saying it exercises "
         "deps.policy.policyId",
         invert),
    ]


def check_wrongness(recipe: Recipe, doc: Any, v15: Any, ep8: Any, c2v4: Any,
                    findings: list[str]) -> int:
    """Run every wrongness probe through the REAL check and require a NAMED
    refusal.  Escapes are reported at the probe, never merely counted."""
    cases = _wrongness_cases()
    if len(cases) != EXPECT_WRONGNESS_PROBES:
        _add(findings, "R1V17-WRONGNESS", "probes",
             f"declared {EXPECT_WRONGNESS_PROBES} probes, built {len(cases)}")
    executed = 0
    for probe_id, expected_code, models, mutate in cases:
        candidate = copy.deepcopy(doc)
        try:
            applied = mutate(candidate)
        except Exception as exc:  # noqa: BLE001
            _add(findings, "R1V17-WRONGNESS", probe_id,
                 f"the probe could not be constructed: {type(exc).__name__}: "
                 f"{exc}")
            continue
        if not applied or canon(candidate) == canon(doc):
            _add(findings, "R1V17-WRONGNESS", probe_id,
                 f"the probe is a no-op, so it measures nothing ({models})")
            continue
        # Republish, so the probe is the FULL attack: every dependent digest is
        # made self-consistent before the check runs.
        _republish(recipe, candidate)
        executed += 1
        try:
            result = check_core(candidate, v15, ep8, c2v4, probes=False)
        except Exception as exc:  # noqa: BLE001
            _add(findings, "R1V17-WRONGNESS", probe_id,
                 f"the check raised on the probe rather than reporting: "
                 f"{type(exc).__name__}: {exc}")
            continue
        if not result:
            _add(findings, "R1V17-WRONGNESS", probe_id,
                 f"ESCAPE -- this probe PASSED at 0 findings.  It models "
                 f"{models}")
        elif expected_code not in _codes(result):
            _add(findings, "R1V17-WRONGNESS", probe_id,
                 f"the probe was refused, but under {sorted(_codes(result))} "
                 f"rather than the named condition {expected_code}.  Freeze "
                 f"7.4: a non-zero result is not evidence the intended guard "
                 f"fired.  It models {models}")
    if executed != EXPECT_WRONGNESS_PROBES:
        _add(findings, "R1V17-WRONGNESS", "probes",
             f"{EXPECT_WRONGNESS_PROBES} probes declared, {executed} EXECUTED")
    return executed


# ---------------------------------------------------------------------------
# Section 13.  Injectivity, the falsifier, and the executed guards.  Carried
# forward from the predecessor, which its review found genuine, and re-pointed
# at the DERIVED recipe and the REBUILT corpus.
# ---------------------------------------------------------------------------
def check_roundtrip(recipe: Recipe, doc: Any, recomputed: dict[str, Any],
                    findings: list[str]) -> int:
    """decode(encode(x)) == x LITERALLY, as canonical bytes."""
    node = _get(doc, ["policyDerivationIdentity",
                      "injectivityByExhibitedTotalDecoder"], {})
    records: list[tuple[str, bytes]] = []
    for vid, record in recomputed["records"].items():
        value = recomputed["values"][vid]
        try:
            back = decode(recipe, record)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V17-ROUNDTRIP", vid,
                 f"the total decoder refused a record this recipe produced: "
                 f"{type(exc).__name__}: {exc}")
            continue
        if canon(back) != canon(value):
            _add(findings, "R1V17-ROUNDTRIP", vid,
                 "decode(encode(x)) != x literally")
        records.append((vid, record))
    exhibit_records: list[tuple[str, bytes, frozenset[str]]] = []
    for label, vid, lists in (
            ("exhibitA/documentA-set-reading", "PDD-01",
             frozenset({"planStageIds"})),
            ("exhibitA/documentB-set-reading", "PDD-17",
             frozenset({"planStageIds"})),
            ("exhibitB/exactCoverage-length-major", "PDD-01",
             frozenset({"exactCoverage"})),
            ("exhibitB/rules-length-major", "PDD-16", frozenset({"rules"}))):
        value = recomputed["values"].get(vid)
        if value is None:
            continue
        record = encode_a(recipe, value, set_reading=lists)
        records.append((label, record))
        exhibit_records.append((label, record, lists))
    for label, record in records[:len(recomputed["records"])]:
        try:
            back = decode(recipe, record)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V17-ROUNDTRIP", label,
                 f"the total decoder refused a record: {type(exc).__name__}: "
                 f"{exc}")
            continue
        if encode_a(recipe, back) != record:
            _add(findings, "R1V17-ROUNDTRIP", label,
                 "encode(decode(r)) != r; the decoder is not a left inverse")
    for label, record, lists in exhibit_records:
        try:
            back = decode(recipe, record)
        except (ValueError, TypeError) as exc:
            _add(findings, "R1V17-ROUNDTRIP", label,
                 f"the total decoder refused a rejected-reading exhibit "
                 f"record: {type(exc).__name__}: {exc}")
            continue
        if encode_a(recipe, back, set_reading=lists) != record:
            _add(findings, "R1V17-ROUNDTRIP", label,
                 "the decoder did not recover the value the rejected-reading "
                 "encoder framed")
    if len(records) != EXPECT_ROUNDTRIP_RECORDS:
        _add(findings, "R1V17-ROUNDTRIP",
             "$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder",
             f"expected {EXPECT_ROUNDTRIP_RECORDS} records, round-tripped "
             f"{len(records)}")
    for key in ("recordsRoundTripped", "literalRoundTripsPassing"):
        _eq(findings, "R1V17-ROUNDTRIP",
            f"$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder"
            f".{key}", node.get(key), str(EXPECT_ROUNDTRIP_RECORDS))
    _eq(findings, "R1V17-SELFREPORT",
        "$.measuredSelfReport.recordsLiterallyRoundTripped",
        _get(doc, ["measuredSelfReport", "recordsLiterallyRoundTripped"]),
        f"{EXPECT_ROUNDTRIP_RECORDS} of {EXPECT_ROUNDTRIP_RECORDS}")
    return len(records)


def check_enumerated_injectivity(recipe: Recipe, findings: list[str]) -> int:
    """Beyond the published corpus: 720 admissible values, enumerated here.

    Retained from the predecessor, where it was genuine.  It is no longer this
    instrument's strongest distinctness evidence -- CIR-B1's point was that a
    synthetic sweep aimed away from the published corpus certifies the sweep --
    but a recipe that is injective on 720 constructed values and on 17
    externally anchored ones is stronger than one that is injective on either
    alone.
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
        for variant in recipe.variants:
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
                        record = encode_a(recipe, value)
                        other = encode_b(recipe, value)
                    except (ValueError, TypeError) as exc:
                        _add(findings, "R1V17-INJECTIVITY",
                             f"enumerated[{total}]",
                             f"an admissible value was refused: "
                             f"{type(exc).__name__}: {exc}")
                        continue
                    if record != other:
                        _add(findings, "R1V17-ENCODER-DISAGREE",
                             f"enumerated[{total}]",
                             "the two independent encoders disagreed")
                        continue
                    if record in seen:
                        collisions += 1
                        _add(findings, "R1V17-INJECTIVITY",
                             f"enumerated[{total}]",
                             f"encoding collides with {seen[record]}")
                    seen[record] = canon(value).decode("utf-8")
                    if canon(decode(recipe, record)) == canon(value):
                        trips += 1
                    else:
                        _add(findings, "R1V17-INJECTIVITY",
                             f"enumerated[{total}]",
                             "decode(encode(x)) != x literally")
    if total != EXPECT_ENUMERATED_VALUES:
        _add(findings, "R1V17-INJECTIVITY", "enumerated",
             f"expected {EXPECT_ENUMERATED_VALUES} enumerated values, built "
             f"{total}")
    if len(seen) != EXPECT_ENUMERATED_VALUES or collisions:
        _add(findings, "R1V17-INJECTIVITY", "enumerated",
             f"expected {EXPECT_ENUMERATED_VALUES} distinct encodings, found "
             f"{len(seen)} with {collisions} collision(s)")
    if trips != EXPECT_ENUMERATED_VALUES:
        _add(findings, "R1V17-INJECTIVITY", "enumerated",
             f"expected {EXPECT_ENUMERATED_VALUES} literal round-trips, "
             f"measured {trips}")
    return total


def check_falsifier(recipe: Recipe, doc: Any, recomputed: dict[str, Any],
                    findings: list[str]) -> None:
    """The 554-byte falsifier, EXECUTED.

    Freeze 7.2.2's rider: a measurement that cannot fail the build is prose.  A
    sibling declared a control named EPC-V2 that occurs in no executable and
    therefore never fires.  This one fires.
    """
    exhibit = _get(doc, ["policyDerivationIdentity", "orderingRuling",
                         "exhibitA_planStageIdsSequenceVsSet"], {})
    where = ("$.policyDerivationIdentity.orderingRuling"
             ".exhibitA_planStageIdsSequenceVsSet")
    value_a = recomputed["values"].get("PDD-01")
    value_b = recomputed["values"].get("PDD-17")
    if value_a is None or value_b is None:
        _add(findings, "R1V17-FALSIFIER", where,
             "PDD-01 or PDD-17 did not encode, so the falsifier cannot run")
        return
    record_a = recomputed["records"]["PDD-01"]
    record_b = recomputed["records"]["PDD-17"]
    adopted_a = recomputed["digests"]["PDD-01"]
    adopted_b = recomputed["digests"]["PDD-17"]

    for label, record, node in (("documentA", record_a, exhibit.get("documentA")),
                                ("documentB", record_b, exhibit.get("documentB"))):
        if len(record) != 554:
            _add(findings, "R1V17-FALSIFIER", f"{where}.{label}",
                 f"the falsifier requires a 554-byte record; measured "
                 f"{len(record)}")
        if isinstance(node, dict):
            _eq(findings, "R1V17-FALSIFIER", f"{where}.{label}.recordBytes",
                node.get("recordBytes"), str(len(record)))
        else:
            _add(findings, "R1V17-TYPE", f"{where}.{label}",
                 f"declared object, found {json_type(node)}")
    _eq(findings, "R1V17-FALSIFIER", f"{where}.documentA.derivationDigest",
        _get(exhibit, ["documentA", "derivationDigest"]), adopted_a)
    _eq(findings, "R1V17-FALSIFIER", f"{where}.documentB.derivationDigest",
        _get(exhibit, ["documentB", "derivationDigest"]), adopted_b)
    _eq(findings, "R1V17-FALSIFIER", f"{where}.recordHexDocumentA",
        exhibit.get("recordHexDocumentA"), record_a.hex())
    _eq(findings, "R1V17-FALSIFIER", f"{where}.recordHexDocumentB",
        exhibit.get("recordHexDocumentB"), record_b.hex())
    if adopted_a == adopted_b:
        _add(findings, "R1V17-FALSIFIER", where,
             "under the ADOPTED sequence reading the two documents are not "
             "distinct; the sequence ruling buys nothing")
    _eq(findings, "R1V17-FALSIFIER",
        f"{where}.underTheADOPTEDSequenceReading.distinct",
        _get(exhibit, ["underTheADOPTEDSequenceReading", "distinct"]), "YES")

    rejected = frozenset({"planStageIds"})
    set_a = a_derivation_digest(recipe, encode_a(recipe, value_a,
                                                 set_reading=rejected))
    set_b = a_derivation_digest(recipe, encode_a(recipe, value_b,
                                                 set_reading=rejected))
    node = _get(exhibit, ["underTheREJECTEDSetReading"], {})
    _eq(findings, "R1V17-FALSIFIER",
        f"{where}.underTheREJECTEDSetReading.documentA",
        node.get("documentA"), set_a)
    _eq(findings, "R1V17-FALSIFIER",
        f"{where}.underTheREJECTEDSetReading.documentB",
        node.get("documentB"), set_b)
    _eq(findings, "R1V17-FALSIFIER",
        f"{where}.underTheREJECTEDSetReading.collide", node.get("collide"),
        "YES")
    if set_a != set_b:
        _add(findings, "R1V17-FALSIFIER", where,
             f"the rejected set reading does NOT collide ({set_a} vs {set_b}); "
             f"the artifact's whole case for a SEQUENCE ruling rests on it "
             f"colliding")
    elif set_a != adopted_a:
        _add(findings, "R1V17-FALSIFIER", where,
             f"the set reading collides on {set_a}, which is not PDD-01's own "
             f"published digest {adopted_a}; the published claim is that a "
             f"set-reading implementation PASSES PDD-01 and mints PDD-01's id "
             f"for PDD-17")
    dangerous = node.get("andTHEDANGEROUSPART")
    if isinstance(dangerous, str) and adopted_a[7:] not in dangerous:
        _add(findings, "R1V17-FALSIFIER",
             f"{where}.underTheREJECTEDSetReading.andTHEDANGEROUSPART",
             "the prose does not name the digest the executed control lands on")

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
            _add(findings, "R1V17-FALSIFIER", f"{wb}.{key}",
                 f"{vid} did not encode")
            continue
        adopted = recomputed["digests"][vid]
        length_major = a_derivation_digest(
            recipe, encode_a(recipe, value, set_reading=lists))
        _eq(findings, "R1V17-FALSIFIER", f"{wb}.{key}.adoptedDigest",
            node.get("adoptedDigest"), adopted)
        _eq(findings, "R1V17-FALSIFIER",
            f"{wb}.{key}.digestIfEP8sSortedListsWereApplied",
            node.get("digestIfEP8sSortedListsWereApplied"), length_major)
        _eq(findings, "R1V17-FALSIFIER", f"{wb}.{key}.ordersDiffer",
            node.get("ordersDiffer"), "YES")
        _eq(findings, "R1V17-FALSIFIER", f"{wb}.{key}.distinct",
            node.get("distinct"), "YES")
        if adopted == length_major:
            _add(findings, "R1V17-FALSIFIER", f"{wb}.{key}",
                 "key-major and length-major produce the same digest here, so "
                 "this exhibit separates nothing")


def check_order_rulings(recipe: Recipe, doc: Any, v15: Any,
                        recomputed: dict[str, Any],
                        findings: list[str]) -> None:
    """The rulings, their v1.5 provenance, and the REFUSAL that buys literal
    injectivity -- executed per list against the named condition."""
    ruling = _get(doc, ["policyDerivationIdentity", "orderingRuling"], {})
    where = "$.policyDerivationIdentity.orderingRuling"
    plan = _get(ruling, ["planStageIds"], {})
    _eq(findings, "R1V17-ORDER-RULING", f"{where}.planStageIds.ruling",
        plan.get("ruling"),
        "SEQUENCE. Order is semantic and is preserved byte-for-byte. It is NOT "
        "a set.")
    quoted = _get(ruling, ["rules_findings_exactCoverage", "orderRulesQuoted"],
                  {})
    for name, pointer in V15_ORDER_POINTERS.items():
        live = _get(v15, pointer)
        if name == "planStageIds":
            if not isinstance(live, str) or live not in str(
                    plan.get("derivedFrom")):
                _add(findings, "R1V17-ORDER-RULING",
                     f"{where}.planStageIds.derivedFrom",
                     f"the SEQUENCE ruling is derived from live v1.5's "
                     f"orderRule, but the stated provenance does not quote it "
                     f"verbatim: {live!r}")
            continue
        _eq(findings, "R1V17-ORDER-RULING",
            f"{where}.rules_findings_exactCoverage.orderRulesQuoted.{name}",
            quoted.get(name), live)
    _eq(findings, "R1V17-ORDER-RULING", f"{where}.fourListsInThePreimage",
        ruling.get("fourListsInThePreimage"),
        "planStageIds, rules, findings, exactCoverage. All four are ruled below.")
    _eq(findings, "R1V17-ORDER-RULING",
        "v1.5 $.closedTypes.SealedStageInput.fields.planStageIds.uniquenessRule",
        _get(v15, ["closedTypes", "SealedStageInput", "fields", "planStageIds",
                   "uniquenessRule"]), "exact string uniqueness")

    base = recomputed["values"].get("PDD-01")
    if not isinstance(base, dict):
        _add(findings, "R1V17-ORDER", where, "PDD-01 unavailable")
        return
    cases = [
        ("exactCoverage",
         lambda v: v.update(
             {"exactCoverage": list(reversed(v["exactCoverage"]))})),
        ("rules",
         lambda v: v.update({"rules": [
             {"ruleId": "rule:b", "artifactDigest": "sha256:" + "c" * 64},
             {"ruleId": "rule:a", "artifactDigest": "sha256:" + "3" * 64}]})),
        ("findings",
         lambda v: v.update({"findings": [
             {"ruleId": "rule:b", "findingId": "finding:1",
              "valueDigest": "sha256:" + "e" * 64},
             {"ruleId": "rule:a", "findingId": "finding:1",
              "valueDigest": "sha256:" + "e" * 64}]})),
    ]
    for name, mutate in cases:
        expected = (f"{name} violates R-1's strict-ascending orderRule at "
                    f"index 1")
        candidate = copy.deepcopy(base)
        mutate(candidate)
        try:
            encode_a(recipe, candidate)
        except ValueError as exc:
            if str(exc) != expected:
                _add(findings, "R1V17-ORDER", f"{where}/{name}",
                     f"the encoder refused a mis-ordered {name}, but on "
                     f"{str(exc)!r} rather than the named condition "
                     f"{expected!r}")
        except TypeError as exc:
            _add(findings, "R1V17-ORDER", f"{where}/{name}",
                 f"a mis-ordered {name} was refused on a type error ({exc}), "
                 f"not on the order rule")
        else:
            _add(findings, "R1V17-ORDER", f"{where}/{name}",
                 f"the encoder ACCEPTED a mis-ordered {name}; a repairing "
                 f"encoder is many-to-one and the LITERAL round-trip claim "
                 f"does not survive it")
    # And the refusal is not a repair in disguise: assert the repairing shape
    # really would have collapsed two distinct admitted inputs onto one record.
    repaired = copy.deepcopy(base)
    repaired["exactCoverage"] = list(reversed(base["exactCoverage"]))
    sorting = frozenset({"exactCoverage"})
    if canon(repaired) == canon(base):
        _add(findings, "R1V17-ORDER", f"{where}/repair-would-collapse",
             "the reversed exactCoverage is not a distinct input, so this "
             "control separates nothing")
    elif (encode_a(recipe, repaired, set_reading=sorting)
          != encode_a(recipe, base, set_reading=sorting)):
        _add(findings, "R1V17-ORDER", f"{where}/repair-would-collapse",
             "a repairing encoder would NOT have mapped the ordered and the "
             "reversed exactCoverage onto one record, so the stated reason for "
             "refusing to repair does not hold on these bytes")


def check_rejection_controls(recipe: Recipe, doc: Any,
                             recomputed: dict[str, Any],
                             findings: list[str]) -> int:
    """Fifteen controls, EXECUTED, each on the condition it NAMES.

    Freeze 7.4: a non-zero exit is not evidence a guard fired.  An admitted row
    is an escape, and a row that raises for the wrong reason is a finding.
    """
    node = _get(doc, ["policyDerivationIdentity", "rejectionControls"], {})
    where = "$.policyDerivationIdentity.rejectionControls"
    _eq(findings, "R1V17-REJ", f"{where}.count", node.get("count"),
        str(EXPECT_REJECTIONS))
    _eq(findings, "R1V17-REJ", f"{where}.allRejectedByBothEncoders",
        node.get("allRejectedByBothEncoders"), "YES")
    rows = node.get("controls")
    if not isinstance(rows, list):
        _add(findings, "R1V17-TYPE", f"{where}.controls",
             f"declared array, found {json_type(rows)}")
        return 0
    if len(rows) != EXPECT_REJECTIONS:
        _add(findings, "R1V17-REJ", f"{where}.controls",
             f"expected {EXPECT_REJECTIONS} controls, found {len(rows)}")
    base = recomputed["values"].get("PDD-01")
    if not isinstance(base, dict):
        _add(findings, "R1V17-REJ", where, "PDD-01 unavailable")
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
            return with_universe("u" * (recipe.text_max + 1))
        if control_id == "REJ-03":
            return with_universe("universe:\x07one")
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
            _add(findings, "R1V17-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        control_id = row.get("id")
        if not isinstance(control_id, str):
            _add(findings, "R1V17-TYPE", f"{row_where}.id",
                 f"declared string, found {json_type(control_id)}")
            continue
        _eq(findings, "R1V17-REJ", f"{row_where}.bothReject",
            row.get("bothReject"), "YES")
        candidate = build(control_id)
        if candidate is None:
            _add(findings, "R1V17-REJ", f"{row_where}.id",
                 f"{control_id}: this instrument has no executable input for "
                 f"this control, so the row is declared and not measured")
            continue
        executed += 1
        for label, encoder, key in (("encoderA", encode_a, "encoderA"),
                                    ("encoderB", encode_b, "encoderB")):
            declared = row.get(key)
            try:
                encoder(recipe, copy.deepcopy(candidate))
            except (ValueError, TypeError) as exc:
                actual = f"{type(exc).__name__}: {exc}"
                if actual != declared:
                    _add(findings, "R1V17-REJ",
                         f"{row_where}.{key} [{control_id}]",
                         f"{label} refused, but on {actual!r}; the artifact "
                         f"records {declared!r}")
            else:
                _add(findings, "R1V17-REJ", f"{row_where}.{key} [{control_id}]",
                     f"{label} ADMITTED the input this control names; an "
                     f"admitted row is an escape, not a finding about the row")
    if executed != EXPECT_REJECTIONS:
        _add(findings, "R1V17-REJ", f"{where}.controls",
             f"expected {EXPECT_REJECTIONS} controls to be EXECUTED, executed "
             f"{executed}")
    _eq(findings, "R1V17-SELFREPORT", "$.measuredSelfReport.rejectionControls",
        _get(doc, ["measuredSelfReport", "rejectionControls"]),
        str(EXPECT_REJECTIONS))
    return executed


def check_decoder_probes(recipe: Recipe, doc: Any, recomputed: dict[str, Any],
                         findings: list[str]) -> int:
    """Six malformed probes, executed against a record this recipe produced."""
    rows = _get(doc, ["policyDerivationIdentity", "decoderProbes"])
    where = "$.policyDerivationIdentity.decoderProbes"
    record = recomputed["records"].get("PDD-01")
    if record is None:
        _add(findings, "R1V17-DECODER-PROBE", where, "PDD-01 unavailable")
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
        _add(findings, "R1V17-TYPE", where,
             f"declared array, found {json_type(rows)}")
        return 0
    if len(rows) != EXPECT_DECODER_PROBES:
        _add(findings, "R1V17-DECODER-PROBE", where,
             f"expected {EXPECT_DECODER_PROBES} probes, found {len(rows)}")
    executed = 0
    for index, row in enumerate(rows):
        row_where = f"{where}[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V17-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        probe = row.get("probe")
        outcome = row.get("outcome")
        if not isinstance(probe, str) or not isinstance(outcome, str):
            _add(findings, "R1V17-TYPE", row_where,
                 "probe and outcome are declared strings")
            continue
        buf = probes.get(probe)
        if buf is None:
            _add(findings, "R1V17-DECODER-PROBE", f"{row_where}.probe",
                 f"{probe!r}: this instrument has no executable form of this "
                 f"probe, so the row is declared and not measured")
            continue
        executed += 1
        try:
            decode(recipe, buf)
        except (ValueError, TypeError) as exc:
            actual = f"{type(exc).__name__}: {exc}"
            if actual != outcome:
                _add(findings, "R1V17-DECODER-PROBE", f"{row_where}.outcome",
                     f"{probe!r}: the decoder raised {actual!r}; the artifact "
                     f"records {outcome!r}")
        else:
            _add(findings, "R1V17-DECODER-PROBE", f"{row_where}.outcome",
                 f"{probe!r}: the total decoder ACCEPTED a malformed record")
    if executed != EXPECT_DECODER_PROBES:
        _add(findings, "R1V17-DECODER-PROBE", where,
             f"expected {EXPECT_DECODER_PROBES} probes EXECUTED, executed "
             f"{executed}")
    malformed = _get(doc, ["policyDerivationIdentity",
                           "injectivityByExhibitedTotalDecoder",
                           "malformedProbes"])
    if canon(malformed) != canon(rows):
        _add(findings, "R1V17-DECODER-PROBE",
             "$.policyDerivationIdentity.injectivityByExhibitedTotalDecoder"
             ".malformedProbes",
             "the two published probe lists are not the same list")
    _eq(findings, "R1V17-SELFREPORT",
        "$.measuredSelfReport.decoderMalformedProbes",
        _get(doc, ["measuredSelfReport", "decoderMalformedProbes"]),
        str(EXPECT_DECODER_PROBES))
    return executed


def check_field_set_rule(recipe: Recipe, doc: Any, v15: Any,
                         recomputed: dict[str, Any],
                         findings: list[str]) -> None:
    """The rule's PREMISES, applied to LIVE v1.5.

    PDD-01..PDD-04 are already rebuilt from live v1.5 in the corpus derivation
    and compared there, so what is left here is the exclusion argument the
    field set rests on and the four equivalence controls.
    """
    vectors = v15.get("positiveVectors")
    if not isinstance(vectors, list):
        _add(findings, "R1V17-TYPE", "v1.5 $.positiveVectors",
             f"declared array, found {json_type(vectors)}")
        return
    table = {v["id"]: v for v in vectors
             if isinstance(v, dict) and isinstance(v.get("id"), str)}
    declarers = 0
    base_id = "R1V15-POS-01-COMPLETED-NO-DIAGNOSTICS"
    for vector in vectors:
        if not isinstance(vector, dict):
            continue
        vid = vector.get("id")
        if vid != base_id and vector.get("cloneOf") != base_id:
            _add(findings, "R1V17-FIELDSET", f"v1.5 $.positiveVectors[{vid}]",
                 f"expected cloneOf {base_id!r}; got {vector.get('cloneOf')!r}")
        for dotted in (vector.get("overrides") or {}):
            if not (dotted.startswith("deps.budgetLimits.")
                    or dotted == "attempt.executionId"):
                _add(findings, "R1V17-FIELDSET",
                     f"v1.5 $.positiveVectors[{vid}].overrides",
                     f"{dotted!r} touches a subtree outside the declared "
                     f"evidence-neutral set, so the exclusion argument does "
                     f"not hold as stated")
        if "expectProjectionEqualTo" in vector:
            declarers += 1
    if declarers != EXPECT_PROJECTION_EQUAL_DECLARERS:
        _add(findings, "R1V17-FIELDSET", "v1.5 $.positiveVectors",
             f"expected {EXPECT_PROJECTION_EQUAL_DECLARERS} vectors declaring "
             f"expectProjectionEqualTo, measured {declarers}")
    resolved_all = [resolve_v15(v15, vid) for vid in table]
    stage_forms = {canon(_get(r, ["stageInput"])) for r in resolved_all
                   if r is not None}
    dep_forms = {canon({k: v for k, v in (_get(r, ["deps"]) or {}).items()
                        if k != "budgetLimits"})
                 for r in resolved_all if r is not None}
    if len(stage_forms) != 1 or len(dep_forms) != 1:
        _add(findings, "R1V17-FIELDSET", "v1.5 $.positiveVectors",
             f"the ten vectors do not share one stageInput and one non-budget "
             f"deps ({len(stage_forms)} stageInput form(s), {len(dep_forms)} "
             f"deps form(s))")

    node = _get(doc, ["policyDerivationIdentity", "equivalenceControls"], {})
    where = "$.policyDerivationIdentity.equivalenceControls"
    rows = node.get("controls")
    if not isinstance(rows, list):
        _add(findings, "R1V17-TYPE", f"{where}.controls",
             f"declared array, found {json_type(rows)}")
        return
    if len(rows) != EXPECT_EQUIVALENCE:
        _add(findings, "R1V17-EQ", f"{where}.controls",
             f"expected {EXPECT_EQUIVALENCE} controls, found {len(rows)}")
    _eq(findings, "R1V17-EQ", f"{where}.allEqualPDD01",
        node.get("allEqualPDD01"), "YES")
    target = recomputed["digests"].get("PDD-01")
    for index, row in enumerate(rows):
        row_where = f"{where}.controls[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V17-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        built_from = row.get("builtFrom")
        if not isinstance(built_from, str) or built_from not in table:
            _add(findings, "R1V17-EQ", f"{row_where}.builtFrom",
                 f"{built_from!r} is not a live v1.5 vector")
            continue
        vector = table[built_from]
        overrides = vector.get("overrides") or {}
        declared_overrides = row.get("v15Overrides")
        if not isinstance(declared_overrides, dict):
            _add(findings, "R1V17-TYPE", f"{row_where}.v15Overrides",
                 f"declared object, found {json_type(declared_overrides)}")
        else:
            measured = {key: str(value) for key, value in overrides.items()}
            for key, value in sorted(declared_overrides.items()):
                if not isinstance(value, str):
                    _add(findings, "R1V17-TYPE",
                         f"{row_where}.v15Overrides.{key}",
                         f"declared string, found {json_type(value)}")
            if measured != declared_overrides:
                _add(findings, "R1V17-EQ", f"{row_where}.v15Overrides",
                     f"live v1.5 overrides {measured}; the artifact records "
                     f"{declared_overrides}")
        equal_to = vector.get("expectProjectionEqualTo")
        peer = table.get(equal_to) if isinstance(equal_to, str) else None
        completion = (peer or {}).get("expectedCompletion")
        resolved = resolve_v15(v15, built_from)
        if resolved is None or not isinstance(completion, dict):
            _add(findings, "R1V17-EQ", row_where,
                 f"could not rebuild {built_from} from live v1.5")
            continue
        rebuilt = field_set_record(recipe, resolved, completion)
        if rebuilt is None:
            _add(findings, "R1V17-EQ", row_where,
                 "the fieldSetRule did not yield a complete record")
            continue
        digest = a_derivation_digest(recipe, encode_a(recipe, rebuilt))
        if b_digest(recipe, encode_b(recipe, rebuilt)) != digest:
            _add(findings, "R1V17-ENCODER-DISAGREE", row_where,
                 "the two independent encoders disagreed on an equivalence "
                 "control")
        _eq(findings, "R1V17-EQ", f"{row_where}.derivationDigest",
            row.get("derivationDigest"), digest)
        _eq(findings, "R1V17-EQ", f"{row_where}.equalsPDD01",
            row.get("equalsPDD01"), "YES")
        if target is not None and digest != target:
            _add(findings, "R1V17-EQ", row_where,
                 f"rebuilt from live v1.5 {built_from}, the control yields "
                 f"{digest}, not PDD-01's {target}; the exclusion claim would "
                 f"be false")
    _eq(findings, "R1V17-SELFREPORT", "$.measuredSelfReport.equivalenceControls",
        _get(doc, ["measuredSelfReport", "equivalenceControls"]),
        str(EXPECT_EQUIVALENCE))


def check_separation(recipe: Recipe, doc: Any, v15: Any,
                     recomputed: dict[str, Any], findings: list[str]) -> None:
    node = _get(doc, ["policyDerivationIdentity", "separationControls"], {})
    where = "$.policyDerivationIdentity.separationControls"
    rows = node.get("controls")
    if not isinstance(rows, list):
        _add(findings, "R1V17-TYPE", f"{where}.controls",
             f"declared array, found {json_type(rows)}")
        return
    if len(rows) != EXPECT_SEPARATION:
        _add(findings, "R1V17-SEP", f"{where}.controls",
             f"expected {EXPECT_SEPARATION} controls, found {len(rows)}")
    record = recomputed["records"].get("PDD-01")
    target = recomputed["digests"].get("PDD-01")
    if record is None:
        _add(findings, "R1V17-SEP", where, "PDD-01 unavailable")
        return
    computed: list[str] = []
    for index, row in enumerate(rows):
        row_where = f"{where}.controls[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V17-TYPE", row_where,
                 f"declared object, found {json_type(row)}")
            continue
        namespace = row.get("namespace")
        domain = row.get("domain")
        if not isinstance(namespace, str) or not isinstance(domain, str):
            _add(findings, "R1V17-TYPE", row_where,
                 "namespace and domain are declared strings")
            continue
        digest = a_derivation_digest(recipe, record, namespace, domain)
        if b_digest(recipe, record, namespace, domain) != digest:
            _add(findings, "R1V17-ENCODER-DISAGREE", row_where,
                 "the two independent encoders disagreed on a separation "
                 "control")
        computed.append(digest)
        _eq(findings, "R1V17-SEP", f"{row_where}.derivationDigest",
            row.get("derivationDigest"), digest)
        expected_equal = "YES" if (namespace == recipe.namespace
                                   and domain == recipe.domain) else "NO"
        _eq(findings, "R1V17-SEP", f"{row_where}.equalsPDD01",
            row.get("equalsPDD01"), expected_equal)
        if expected_equal == "YES" and digest != target:
            _add(findings, "R1V17-SEP", row_where,
                 f"the identity control does not reproduce PDD-01: {digest} "
                 f"!= {target}")
        if expected_equal == "NO" and digest == target:
            _add(findings, "R1V17-SEP", row_where,
                 "a separator that does not separate: this pair reproduces "
                 "PDD-01's digest")
    if len(set(computed)) != EXPECT_SEPARATION:
        _add(findings, "R1V17-SEP", f"{where}.controls",
             f"expected {EXPECT_SEPARATION} distinct values, computed "
             f"{len(set(computed))}")
    _eq(findings, "R1V17-SEP", f"{where}.fiveDistinctValues",
        node.get("fiveDistinctValues"), "YES")
    _eq(findings, "R1V17-SEP", f"{where}.xd5ReproducesPDD01",
        node.get("xd5ReproducesPDD01"), "YES")

    grammar = _get(v15, ["evidenceIdentity", "conformanceCommitmentGrammar"])
    oracle_where = f"{where}.conformanceOracleNonCollision"
    if not isinstance(grammar, str):
        _add(findings, "R1V17-TYPE",
             "v1.5 $.evidenceIdentity.conformanceCommitmentGrammar",
             f"declared string, found {json_type(grammar)}")
        return
    prefix = "opensip:r1-v1.5:projection"
    if prefix not in grammar:
        _add(findings, "R1V17-SEP",
             "v1.5 $.evidenceIdentity.conformanceCommitmentGrammar",
             f"live v1.5 does not carry the oracle prefix {prefix!r} this "
             f"separation argument is built on")
        return
    oracle_first_two = (prefix + "\x00").encode("utf-8")[:2].hex()
    identity_first_two = a_outer(recipe, a_leaf_root(recipe, record))[:2].hex()
    _eq(findings, "R1V17-SEP", f"{oracle_where}.oraclePreimageFirstTwoBytesHex",
        _get(node, ["conformanceOracleNonCollision",
                    "oraclePreimageFirstTwoBytesHex"]), oracle_first_two)
    _eq(findings, "R1V17-SEP",
        f"{oracle_where}.identityOuterPreimageFirstTwoBytesHex",
        _get(node, ["conformanceOracleNonCollision",
                    "identityOuterPreimageFirstTwoBytesHex"]),
        identity_first_two)
    _eq(findings, "R1V17-SEP", f"{oracle_where}.canShareAPreimage",
        _get(node, ["conformanceOracleNonCollision", "canShareAPreimage"]), "NO")
    if oracle_first_two[:2] == identity_first_two[:2]:
        _add(findings, "R1V17-SEP", oracle_where,
             f"the two constructions agree in their first byte "
             f"(0x{oracle_first_two[:2]}), so the non-collision argument does "
             f"not hold")
    _eq(findings, "R1V17-SELFREPORT", "$.measuredSelfReport.separationControls",
        _get(doc, ["measuredSelfReport", "separationControls"]),
        str(EXPECT_SEPARATION))


def check_worked_example(recipe: Recipe, doc: Any, v15: Any,
                         recomputed: dict[str, Any],
                         findings: list[str]) -> None:
    """A real derivationDigest in a complete CoreCompletion::completed."""
    node = _get(doc, ["policyDerivationIdentity", "workedExample"], {})
    where = "$.policyDerivationIdentity.workedExample"
    value = node.get("derivationInputRecord")
    if not admit_record_value(recipe, value, f"{where}.derivationInputRecord",
                              findings):
        return
    # The worked example's INPUT is POS-01's, so it is anchored to the same
    # live v1.5 rebuild the corpus uses rather than to itself.
    basis = recomputed["values"].get("PDD-01")
    if isinstance(basis, dict) and canon(value) != canon(basis):
        _add(findings, "R1V17-WORKED", f"{where}.derivationInputRecord",
             "the worked example's input record is not the record the "
             "fieldSetRule builds from live v1.5 POS-01, so the example is not "
             "an example of this recipe")
    digest = a_derivation_digest(recipe, encode_a(recipe, value))
    if b_digest(recipe, encode_b(recipe, value)) != digest:
        _add(findings, "R1V17-ENCODER-DISAGREE", where,
             "the two independent encoders disagreed on the worked example")
    published = _get(node, ["completion", "policyOutcome", "derivationDigest"])
    _eq(findings, "R1V17-WORKED",
        f"{where}.completion.policyOutcome.derivationDigest", published, digest)
    if isinstance(published, str) and len(set(published[7:])) == 1:
        _add(findings, "R1V17-WORKED",
             f"{where}.completion.policyOutcome.derivationDigest",
             "the worked example carries a repeated-digit placeholder, not a "
             "value derived from the rule")
    target = recomputed["digests"].get("PDD-01")
    if target is not None and digest != target:
        _add(findings, "R1V17-WORKED", where,
             f"the worked example's semantics are POS-01's, so its digest must "
             f"be PDD-01's {target}; computed {digest}")
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
            _add(findings, "R1V17-WORKED", f"{where}.completion",
                 "the worked example differs from live v1.5 POS-01's "
                 "expectedCompletion in more than derivationDigest")
        placeholder = _get(live, ["policyOutcome", "derivationDigest"])
        stated = str(node.get("theOnlyDifferenceFromTheCarriedVector"))
        if not isinstance(placeholder, str) or placeholder[:11] not in stated:
            _add(findings, "R1V17-WORKED",
                 f"{where}.theOnlyDifferenceFromTheCarriedVector",
                 f"the stated difference does not name the placeholder "
                 f"{placeholder!r} that live v1.5 POS-01 actually carries")
    else:
        _add(findings, "R1V17-TYPE", f"{where}.completion",
             "declared object in both v1.5 and the worked example")

    rows = _get(doc, ["policyDerivationIdentity",
                      "relationToTheCarriedPositiveVectors", "migrationTable"])
    census = _get(doc, ["policyDerivationIdentity",
                        "relationToTheCarriedPositiveVectors",
                        "placeholderCensusMeasuredHere"], {})
    rel = ("$.policyDerivationIdentity.relationToTheCarriedPositiveVectors")
    _eq(findings, "R1V17-WORKED",
        f"{rel}.placeholderCensusMeasuredHere.distinctPlaceholderValues",
        census.get("distinctPlaceholderValues"), str(EXPECT_PLACEHOLDER_VALUES))
    _eq(findings, "R1V17-WORKED",
        f"{rel}.placeholderCensusMeasuredHere.positionsCarrying",
        census.get("positionsCarrying"), str(EXPECT_PLACEHOLDER_POSITIONS))
    if not isinstance(rows, list):
        _add(findings, "R1V17-TYPE", f"{rel}.migrationTable",
             f"declared array, found {json_type(rows)}")
        return
    counted = 0
    for index, row in enumerate(rows):
        row_where = f"{rel}.migrationTable[{index}]"
        if not isinstance(row, dict):
            _add(findings, "R1V17-TYPE", row_where,
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
                    _add(findings, "R1V17-WORKED", f"{row_where}.positions",
                         f"live v1.5 {pointer} carries {live_value!r}; the "
                         f"table records {placeholder!r}")
        expected = recomputed["digests"].get(vid)
        if expected is not None:
            _eq(findings, "R1V17-WORKED", f"{row_where}.valueThisRuleProduces",
                row.get("valueThisRuleProduces"), expected)
    if counted != EXPECT_PLACEHOLDER_POSITIONS:
        _add(findings, "R1V17-WORKED", f"{rel}.migrationTable",
             f"the table names {counted} positions; "
             f"{EXPECT_PLACEHOLDER_POSITIONS} carry a placeholder")


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


def check_ep8(recipe: Recipe, doc: Any, ep8: Any, findings: list[str]) -> None:
    for pointer, expected in sorted(EP8_VERBATIM.items()):
        live = _get(ep8, list(pointer))
        if live != expected:
            _add(findings, "R1V17-EP8", "EP8 $." + ".".join(pointer),
                 f"this checker transcribes {expected!r}; live EP8 states "
                 f"{live!r}")
    domains = _get(ep8, ["canonicalCommitmentGrammar", "domains"])
    if not isinstance(domains, list) or len(domains) != EXPECT_EP8_DOMAINS:
        _add(findings, "R1V17-EP8", "EP8 $.canonicalCommitmentGrammar.domains",
             f"expected {EXPECT_EP8_DOMAINS} members, found "
             f"{len(domains) if isinstance(domains, list) else json_type(domains)}")
    elif recipe.domain in domains:
        _add(findings, "R1V17-EP8", "EP8 $.canonicalCommitmentGrammar.domains",
             f"{recipe.domain!r} has been added to EP8's closed domain list; "
             f"law 19 requires R-1 to mint its own under its own namespace, "
             f"not to extend EP8's")
    records = _get(ep8, ["normativePreimageGrammar", "records"])
    if not isinstance(records, list) or len(records) != EXPECT_EP8_RECORD_TYPES:
        _add(findings, "R1V17-EP8", "EP8 $.normativePreimageGrammar.records",
             f"the clause enumeration counts this table ONCE on the stated "
             f"basis that it is EP8's table of {EXPECT_EP8_RECORD_TYPES} "
             f"record types rather than a rule; found "
             f"{len(records) if isinstance(records, list) else json_type(records)}")
    occurrences = json.dumps(ep8, sort_keys=True).count("componentFrame")
    _eq(findings, "R1V17-EP8",
        "$.policyDerivationIdentity.primitives"
        ".componentFrameOccurrencesMeasuredHere",
        _get(doc, ["policyDerivationIdentity", "primitives",
                   "componentFrameOccurrencesMeasuredHere"]),
        str(EXPECT_COMPONENT_FRAME_OCCURRENCES))
    if occurrences != EXPECT_COMPONENT_FRAME_OCCURRENCES:
        _add(findings, "R1V17-EP8", "EP8",
             f"componentFrame occurs {occurrences} times in live EP8; "
             f"{EXPECT_COMPONENT_FRAME_OCCURRENCES} is expected")

    clauses = _ep8_clauses(ep8)
    if len(clauses) != EXPECT_EP8_CLAUSES:
        _add(findings, "R1V17-EP8", "EP8",
             f"the mechanical clause enumeration yields {len(clauses)} "
             f"clauses; {EXPECT_EP8_CLAUSES} is expected")
    node = _get(doc, ["policyDerivationIdentity", "declaredDepartures"], {})
    where = "$.policyDerivationIdentity.declaredDepartures"
    classification = node.get("fullClassification")
    if not isinstance(classification, dict):
        _add(findings, "R1V17-TYPE", f"{where}.fullClassification",
             f"declared object, found {json_type(classification)}")
        return
    for clause in sorted(set(clauses) - set(classification)):
        _add(findings, "R1V17-EP8", f"{where}.fullClassification",
             f"live EP8 clause {clause!r} is not classified; a silently "
             f"dropped clause looks identical to a forgotten one")
    for clause in sorted(set(classification) - set(clauses)):
        _add(findings, "R1V17-EP8", f"{where}.fullClassification",
             f"{clause!r} is classified but is not a live EP8 clause")
    _eq(findings, "R1V17-EP8", f"{where}.clausesEnumerated",
        node.get("clausesEnumerated"), str(EXPECT_EP8_CLAUSES))
    _eq(findings, "R1V17-EP8", f"{where}.clausesClassified",
        node.get("clausesClassified"), str(EXPECT_EP8_CLAUSES))
    _eq(findings, "R1V17-EP8", f"{where}.silentlyDropped",
        node.get("silentlyDropped"), "0")
    for key in ("unclassifiedClauses", "classifiedButNotPresent"):
        value = node.get(key)
        if not isinstance(value, list):
            _add(findings, "R1V17-TYPE", f"{where}.{key}",
                 f"declared array, found {json_type(value)}")
        elif value:
            _add(findings, "R1V17-EP8", f"{where}.{key}",
                 f"declared empty; carries {len(value)} member(s)")
    _eq(findings, "R1V17-SELFREPORT", "$.measuredSelfReport.ep8ClausesClassified",
        _get(doc, ["measuredSelfReport", "ep8ClausesClassified"]),
        f"{EXPECT_EP8_CLAUSES} of {EXPECT_EP8_CLAUSES} enumerated")
    _eq(findings, "R1V17-SELFREPORT",
        "$.measuredSelfReport.componentFrameOccurrencesInEP8",
        _get(doc, ["measuredSelfReport", "componentFrameOccurrencesInEP8"]),
        str(EXPECT_COMPONENT_FRAME_OCCURRENCES))
    _eq(findings, "R1V17-SELFREPORT", "$.measuredSelfReport.ep8DomainListMembers",
        _get(doc, ["measuredSelfReport", "ep8DomainListMembers"]),
        f"{EXPECT_EP8_DOMAINS} -- NOT EXTENDED")


def check_self_report(doc: Any, c2v4: Any, findings: list[str]) -> None:
    report = doc.get("measuredSelfReport")
    if not isinstance(report, dict):
        return
    for key, expected in (
            ("pinnedVectors", str(EXPECT_PINNED_VECTORS)),
            ("maxTextComponentBytesAcrossAllVectors", str(EXPECT_MAX_TEXT_BYTES)),
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
        _eq(findings, "R1V17-SELFREPORT", f"$.measuredSelfReport.{key}",
            report.get(key), expected)
    fixtures = c2v4.get("planIntentFixtures")
    measured = (sum(1 for row in fixtures
                    if isinstance(row, dict) and "expectedCommitment" in row)
                if isinstance(fixtures, list) else None)
    if measured != EXPECT_C2V4_PINNED_FIXTURES:
        _add(findings, "R1V17-SELFREPORT",
             "c2-plan-stage-schema.v4 $.planIntentFixtures",
             f"the standard being matched carries {measured} fixtures with an "
             f"expectedCommitment; {EXPECT_C2V4_PINNED_FIXTURES} is expected")
    cross = report.get("shasumCrossCheck")
    if not isinstance(cross, dict):
        _add(findings, "R1V17-TYPE", "$.measuredSelfReport.shasumCrossCheck",
             f"declared object, found {json_type(cross)}")
    else:
        _eq(findings, "R1V17-SELFREPORT",
            "$.measuredSelfReport.shasumCrossCheck.mismatches",
            cross.get("mismatches"), "0")
        examples = cross.get("mismatchExamples")
        if not isinstance(examples, list) or examples:
            _add(findings, "R1V17-SELFREPORT",
                 "$.measuredSelfReport.shasumCrossCheck.mismatchExamples",
                 "declared an empty array")
    _eq(findings, "R1V17-SELFREPORT", "$.parseDiscipline.duplicateKeysFound",
        _get(doc, ["parseDiscipline", "duplicateKeysFound"]), "0")
    _eq(findings, "R1V17-SELFREPORT", "$.environment.thirdPartyPackages",
        _get(doc, ["environment", "thirdPartyPackages"]), "none")
    _eq(findings, "R1V17-SELFREPORT", "$.environment.network",
        _get(doc, ["environment", "network"]), "none")


def check_binding_disclaimer(doc: Any, findings: list[str]) -> None:
    """Writing an instrument does not apply a candidate.  If the artifact ever
    starts claiming otherwise, that is a finding here."""
    node = doc.get("bindingDisclaimer")
    if not isinstance(node, dict):
        _add(findings, "R1V17-TYPE", "$.bindingDisclaimer",
             f"declared object, found {json_type(node)}")
        return
    _eq(findings, "R1V17-POSTURE", "$.bindingDisclaimer.binds", node.get("binds"),
        "NOTHING. This file is CANDIDATE-NOT-APPLIED and "
        "AWAITING-INDEPENDENT-REVIEW.")
    boundary = _get(doc, ["authorityBoundary", "notAuthorityFor"])
    if not isinstance(boundary, list) or not boundary:
        _add(findings, "R1V17-POSTURE", "$.authorityBoundary.notAuthorityFor",
             "declared a non-empty array")


# ---------------------------------------------------------------------------
# Section 14.  The check driver.
# ---------------------------------------------------------------------------
_EP8_CACHE: dict[str, bytes] = {}


def ep8_bytes_pinned() -> bytes:
    """LIVE evaluation-proof.v8 bytes, re-authenticated against this file's own
    pin on first use.

    Loaded here rather than handed in by main() so that an external driver
    importing this module and calling check() directly gets exactly the checks
    a command-line run gets.  A reviewer should not have to know the entry path
    to reproduce the result.
    """
    if "bytes" not in _EP8_CACHE:
        try:
            raw = (REPO / EP8_PATH).read_bytes()
        except OSError:
            return b""
        if hashlib.sha256(raw).hexdigest() != PINS[EP8_PATH]:
            return b""
        _EP8_CACHE["bytes"] = raw
    return _EP8_CACHE["bytes"]


def check_core(doc: Any, v15: Any, ep8: Any, c2v4: Any,
               probes: bool = True, ep8_bytes: bytes = b"",
               stats: dict[str, Any] | None = None) -> list[str]:
    """One pass.  `probes` is False for the inner runs the wrongness probes
    make, so a probe cannot recurse into itself."""
    findings: list[str] = []
    try:
        if not isinstance(doc, dict):
            _add(findings, "R1V17-TOPLEVEL-TYPE", "$",
                 f"the subject must be a JSON object, found {json_type(doc)}")
            return findings
        check_posture(doc, findings)
        check_binding_disclaimer(doc, findings)
        check_frozen_inputs(doc, findings)
        check_declared_mobile_anchoring(doc, findings)
        check_predecessor(doc, findings)
        check_carry(doc, v15, findings)
        check_law_eighteen(doc, findings)
        recipe = derive_recipe(doc, v15, ep8, ep8_bytes or ep8_bytes_pinned(),
                               findings)
        if recipe is None:
            return findings
        check_recipe_declaration(recipe, doc, findings)
        corpus = derive_corpus(recipe, v15, findings)
        recomputed = check_vectors(recipe, doc, corpus, findings)
        check_non_degeneracy(recipe, doc, corpus, recomputed, findings)
        models_checked = check_models_axis(recipe, doc, v15, findings)
        violators = check_required_kind(recipe, doc, v15, recomputed, findings)
        check_roundtrip(recipe, doc, recomputed, findings)
        check_enumerated_injectivity(recipe, findings)
        check_falsifier(recipe, doc, recomputed, findings)
        check_order_rulings(recipe, doc, v15, recomputed, findings)
        check_rejection_controls(recipe, doc, recomputed, findings)
        check_decoder_probes(recipe, doc, recomputed, findings)
        check_field_set_rule(recipe, doc, v15, recomputed, findings)
        check_separation(recipe, doc, v15, recomputed, findings)
        check_worked_example(recipe, doc, v15, recomputed, findings)
        check_ep8(recipe, doc, ep8, findings)
        check_self_report(doc, c2v4, findings)
        if stats is not None:
            stats.update({
                "anchored": len(recomputed.get("anchored", set())),
                "literals": len(corpus.get("literals", [])),
                "generated": corpus.get("generated", 0),
                "models": models_checked,
                "requiredKindViolators": violators,
                "topFields": len(recipe.top),
                "nested": len(recipe.nested),
            })
        if probes:
            executed = check_wrongness(recipe, doc, v15, ep8, c2v4, findings)
            if stats is not None:
                stats["wrongness"] = executed
    except Exception as exc:  # total checker boundary
        _add(findings, "R1V17-TOTALITY-EXCEPTION", "$",
             f"{type(exc).__name__}: {exc}")
    return findings


def check(doc: Any, v15: Any, ep8: Any, c2v4: Any,
          stats: dict[str, Any] | None = None) -> list[str]:
    return check_core(doc, v15, ep8, c2v4, probes=True, stats=stats)


# ---------------------------------------------------------------------------
# Section 15.  Selftest.  Every mutation is APPLIED and EXECUTED and must
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
PV = [PDI, "pinnedVectors", "vectors"]


def _idx(doc: Any, vid: str) -> int:
    for index, vector in enumerate(_get(doc, PV, [])):
        if isinstance(vector, dict) and vector.get("id") == vid:
            return index
    raise KeyError(vid)


def _mutate_vector(vid: str, key: str, value: Any) -> Callable[[Any], None]:
    def apply(doc: Any) -> None:
        _get(doc, PV)[_idx(doc, vid)][key] = value
    return apply


def _mutate_leaf(vid: str, path: str, value: Any) -> Callable[[Any], None]:
    def apply(doc: Any) -> None:
        node = _get(doc, PV)[_idx(doc, vid)]["recordValue"]
        if not _path_write(node, path, value):
            raise KeyError(f"{vid}:{path}")
    return apply


def _mutations() -> list[tuple[str, str, Callable[[Any], None] | None, bool]]:
    """(id, expected code, mutation, republish).

    `republish` recomputes every dependent digest with this instrument's own
    encoder before the check runs.  A mutation checked WITHOUT republishing
    only proves the arithmetic is consistent; a mutation checked WITH it is the
    attack that defeated the predecessor.
    """
    return [
        # --- CIR-B1: the corpus must be non-degenerate ----------------------
        ("C01-collapse-PDD-06-onto-basis", "R1V17-ANCHOR", None, True),
        ("C02-collapse-PDD-15-onto-basis", "R1V17-ANCHOR", None, True),
        ("C03-wrong-universe-id", "R1V17-ANCHOR",
         _mutate_leaf("PDD-07", "targetUniverseId", "universe:elsewhere"), True),
        ("C04-wrong-but-wellformed-digest", "R1V17-ANCHOR",
         _mutate_leaf("PDD-11", "policy.artifactDigest",
                      "sha256:" + "0" * 64), True),
        ("C05-malformed-digest-prefix", "R1V17-VOCABULARY",
         _mutate_leaf("PDD-06", "observationSetDigest",
                      "sha856:" + "a" * 64), True),
        ("C06-uppercase-digest", "R1V17-VOCABULARY",
         _mutate_leaf("PDD-08", "coverageContextDigest",
                      "sha256:" + "B" * 64), True),
        ("C07-out-of-vocabulary-state", "R1V17-VOCABULARY",
         _mutate_leaf("PDD-14", "exactCoverage[1].state", "budget-exceeded"),
         True),
        ("C08-out-of-vocabulary-deficiency", "R1V17-VOCABULARY",
         _mutate_leaf("PDD-05", "deficiency", "provider-missing"), True),
        ("C09-out-of-vocabulary-kind", "R1V17-VOCABULARY",
         _mutate_leaf("PDD-15", "observationSetKind", "observation-sets"), True),
        ("C10-widened-axis", "R1V17-ANCHOR",
         _mutate_leaf("PDD-12", "targetUniverseId", "universe:two"), True),
        ("C11-ordering-trap-unreversed", "R1V17-ANCHOR",
         _mutate_leaf("PDD-17", "planStageIds",
                      ["stage:rules", "stage:policy"]), True),
        ("C12-basis-itself-moved", "R1V17-ANCHOR",
         _mutate_leaf("PDD-01", "targetUniverseId", "universe:two"), True),
        # --- CIR-B1: the prose must not invert ------------------------------
        ("C13-inverted-models", "R1V17-SEMANTICS",
         _mutate_vector("PDD-06", "models",
                        "SYNTHETIC -- inclusion control for "
                        "deps.policy.policyId"), False),
        ("C14-models-names-nothing", "R1V17-SEMANTICS",
         _mutate_vector("PDD-11", "models", "SYNTHETIC -- inclusion control"),
         False),
        ("C15-class-marker-dropped", "R1V17-SEMANTICS",
         _mutate_vector("PDD-09", "models",
                        "SYNTHETIC -- note about stageInput.planStageIds"),
         False),
        ("C16-requiredKind-note-dropped", "R1V17-SEMANTICS",
         _mutate_vector("PDD-15", "note", "an ordinary control"), False),
        # --- the recipe must be derivable and adjudicated -------------------
        ("C17-tag-out-of-sequence", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "recordGrammar", "PolicyDerivationInputV1", "fields", 3,
               "tag"], "0x8f"), False),
        ("C18-encoding-column-disagrees", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "recordGrammar", "PolicyDerivationInputV1", "fields", 3,
               "encoding"], "C(0x8f, text)"), False),
        ("C19-nested-mirrors-repointed", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "recordGrammar", "RuleValueV1", "mirrors"],
              "closedTypes.PolicyValue.fieldOrder"), False),
        ("C20-nested-record-tag-moved", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "recordGrammar", "CoverageEntryV1", "recordTag"], "0xe0"),
         False),
        ("C21-namespace-changed", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "namespaceAndDomainSeparator", "namespace"],
              "opensip.r1-core.v2"), False),
        ("C22-domain-changed", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "namespaceAndDomainSeparator", "domain"],
              "policy-derivation-v2"), False),
        ("C23-domain-adopts-an-EP8-domain", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "namespaceAndDomainSeparator", "domain"], "verdict-input"),
         False),
        ("C24-text-sentence-not-in-live-EP8", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "primitives", "text",
               "sourceSentenceCharacterForCharacter"],
              "NFC-normalized UTF-8 with no BOM; persisted values are "
              "non-empty, <=8192 bytes, and exclude U+0000..U+001F and U+007F"),
         False),
        ("C25-r1DomainList-widened", "R1V17-RECIPE-DERIVATION",
         _set([PDI, "namespaceAndDomainSeparator", "r1DomainList"],
              ["policy-derivation-v1", "policy-derivation-v2"]), False),
        # --- the mobile rows' recorded digests must stay anchored -----------
        ("C26-mobile-row-digest-rewritten", "R1V17-MOBILE-ANCHOR", None, False),
        ("C27-mobile-disclosure-rewritten", "R1V17-MOBILE-ANCHOR",
         _set(["measuredSelfReport", "driftDisclosure",
               "theSUBJECTSDIDNOTMOVE"],
              "r1-lifetime-neutrality.conformance.v1.5.json is "
              "0000000000000000000000000000000000000000000000000000000000000000"
              " -- measured at the start of this authoring and again at "
              "finalisation, unchanged."), False),
        # --- the arithmetic, the guards and the rulings ---------------------
        ("C28-planStageIds-reversed", "R1V17-ANCHOR",
         _mutate_leaf("PDD-01", "planStageIds",
                      ["stage:policy", "stage:rules"]), True),
        ("C29-published-digest-altered", "R1V17-VECTOR",
         _mutate_vector("PDD-02", "derivationDigest", "sha256:" + "1" * 64),
         False),
        ("C30-published-recordBytes-altered", "R1V17-VECTOR",
         _mutate_vector("PDD-03", "recordBytes", "999"), False),
        ("C31-rejection-message-altered", "R1V17-REJ",
         _set([PDI, "rejectionControls", "controls", 0, "encoderA"],
              "ValueError: nope"), False),
        ("C32-decoder-probe-outcome-altered", "R1V17-DECODER-PROBE",
         _set([PDI, "decoderProbes", 0, "outcome"], "ValueError: nope"), False),
        ("C33-falsifier-collide-denied", "R1V17-FALSIFIER",
         _set([PDI, "orderingRuling", "exhibitA_planStageIdsSequenceVsSet",
               "underTheREJECTEDSetReading", "collide"], "NO"), False),
        ("C34-separation-value-altered", "R1V17-SEP",
         _set([PDI, "separationControls", "controls", 0, "derivationDigest"],
              "sha256:" + "2" * 64), False),
        ("C35-equivalence-value-altered", "R1V17-EQ",
         _set([PDI, "equivalenceControls", "controls", 0, "derivationDigest"],
              "sha256:" + "3" * 64), False),
        ("C36-worked-example-placeholder", "R1V17-WORKED",
         _set([PDI, "workedExample", "completion", "policyOutcome",
               "derivationDigest"], "sha256:" + "5" * 64), False),
        ("C37-ep8-classification-dropped", "R1V17-EP8",
         _del([PDI, "declaredDepartures", "fullClassification",
               "canonicalCommitmentGrammar.truncation"]), False),
        ("C38-order-rule-quote-altered", "R1V17-ORDER-RULING",
         _set([PDI, "orderingRuling", "rules_findings_exactCoverage",
               "orderRulesQuoted", "rules"], "any order"), False),
        # --- posture, closure and carry -------------------------------------
        ("C39-status-applied", "R1V17-POSTURE", _set(["status"], "APPLIED"),
         False),
        ("C40-binds-something", "R1V17-POSTURE", _set(["binds"], "R-1"), False),
        ("C41-seal-recommended", "R1V17-POSTURE",
         _set(["sealRecommendation"], "SEAL"), False),
        ("C42-unset-token", "R1V17-POSTURE",
         _set([PDI, "wireType", "source"], "[UNSET]"), False),
        ("C43-frozen-input-digest-altered", "R1V17-PIN",
         _set(["frozenInputs", 0, "sha256"], "0" * 64), False),
        ("C44-frozen-input-digest-malformed", "R1V17-PIN",
         _set(["frozenInputs", 1, "sha256"], "not-a-digest"), False),
        ("C45-carried-key-edited", "R1V17-CARRY",
         _set(["closedTypes", "Digest", "pattern"], "^sha256:.*$"), False),
        ("C46-vector-count-changed", "R1V17-VECTOR",
         _set([PDI, "pinnedVectors", "count"], "16"), False),
        ("C47-law18-integer-leaf", "R1V17-TYPE",
         _set([PDI, "pinnedVectors", "count"], 17), False),
        ("C48-self-report-altered", "R1V17-SELFREPORT",
         _set(["measuredSelfReport", "encoderDisagreements"], "1"), False),
    ]


def _apply_special(mutation_id: str, doc: Any) -> bool:
    """Mutations that need more than a single positional write."""
    collapse = re.fullmatch(r"C\d+-collapse-(PDD-\d+)-onto-basis", mutation_id)
    if collapse is not None:
        source = _get(doc, PV)[_idx(doc, BASIS)]["recordValue"]
        target = _get(doc, PV)[_idx(doc, collapse.group(1))]
        target["recordValue"] = copy.deepcopy(source)
        return True
    if mutation_id == "C26-mobile-row-digest-rewritten":
        rows = doc.get("frozenInputs")
        for row in rows if isinstance(rows, list) else []:
            if isinstance(row, dict) and row.get("path") in DECLARED_MOBILE:
                row["sha256"] = "1" * 64
                return True
        return False
    return False


PARSER_CASES = [
    ("duplicate-top", '{"a":1,"a":2}', "R1V17-JSON-DUPLICATE", "'a'"),
    ("duplicate-nested", '{"a":{"bb":1,"bb":2}}', "R1V17-JSON-DUPLICATE", "'bb'"),
    ("duplicate-in-array", '[{"cc":1,"cc":2}]', "R1V17-JSON-DUPLICATE", "'cc'"),
    ("nan", '{"a":NaN}', "R1V17-JSON-NONFINITE", "NaN"),
    ("infinity", '{"a":Infinity}', "R1V17-JSON-NONFINITE", "Infinity"),
    ("negative-infinity", '{"a":-Infinity}', "R1V17-JSON-NONFINITE", "-Infinity"),
    ("decimal", '{"a":1.0}', "R1V17-JSON-FLOAT", "1.0"),
    ("exponent", '{"a":1e0}', "R1V17-JSON-FLOAT", "1e0"),
]

HOSTILE = [None, True, 0, "subject", [], {}, {"artifact": None},
           {"closedTypes": []}, {"policyDerivationIdentity": []},
           {"policyDerivationIdentity": {"pinnedVectors": {"vectors": [None]}}},
           {"frozenInputs": "x"}, {"preservationOfV15": {"carriedKeys": [1]}},
           {"policyDerivationIdentity": {"recordGrammar": {
               "PolicyDerivationInputV1": {"recordTag": "0x80", "fields": []}}}}]


def selftest(doc: Any, v15: Any, ep8: Any, c2v4: Any,
             original: bytes) -> tuple[list[str], int, int, int]:
    escapes: list[str] = []
    base = check(doc, v15, ep8, c2v4)
    if base:
        return (["SELFTEST-REFUSED: the unmutated base has "
                 f"{len(base)} finding(s), so mutation results would be "
                 f"meaningless"] + base, 0, 0, 0)

    recipe = derive_recipe(doc, v15, ep8, ep8_bytes_pinned(), [])
    mutations = _mutations()
    ids = [item[0] for item in mutations]
    if len(ids) != len(set(ids)):
        return ["SELFTEST-ESCAPE: duplicate mutation id"], 0, 0, 0
    applied = 0
    for mutation_id, expected_code, fn, republish in mutations:
        candidate = copy.deepcopy(doc)
        try:
            if fn is None:
                if not _apply_special(mutation_id, candidate):
                    escapes.append(f"SELFTEST-ESCAPE {mutation_id}: "
                                   f"the mutation could not be applied")
                    continue
            else:
                fn(candidate)
        except Exception as exc:  # noqa: BLE001
            escapes.append(f"SELFTEST-ESCAPE {mutation_id}: could not apply: "
                           f"{type(exc).__name__}: {exc}")
            continue
        if canon(candidate) == canon(doc):
            escapes.append(f"SELFTEST-ESCAPE {mutation_id}: no-op")
            continue
        if republish and recipe is not None:
            _republish(recipe, candidate)
            if canon(candidate) == canon(doc):
                escapes.append(
                    f"SELFTEST-ESCAPE {mutation_id}: republishing restored the "
                    f"original bytes, so the mutation measures nothing")
                continue
        applied += 1
        result = check_core(candidate, v15, ep8, c2v4, probes=False)
        if not result:
            escapes.append(f"SELFTEST-ESCAPE {mutation_id}: the mutation "
                           f"PASSED"
                           + (" even after every dependent digest was "
                              "recomputed by this instrument's own encoder"
                              if republish else ""))
        elif expected_code not in _codes(result):
            escapes.append(f"SELFTEST-ESCAPE {mutation_id}: expected "
                           f"{expected_code}; got {sorted(_codes(result))}")
    if applied != len(mutations):
        escapes.append(
            f"SELFTEST-ESCAPE: {len(mutations) - applied} mutation(s) never ran")

    for case_id, raw, expected_code, named in PARSER_CASES:
        try:
            strict_loads(raw)
        except StrictJsonError as exc:
            if exc.code != expected_code:
                escapes.append(f"SELFTEST-ESCAPE parser {case_id}: {exc.code} "
                               f"!= {expected_code}")
            elif named not in str(exc):
                escapes.append(f"SELFTEST-ESCAPE parser {case_id}: the refusal "
                               f"does not NAME {named}: {exc}")
        else:
            escapes.append(f"SELFTEST-ESCAPE parser {case_id}: accepted")

    for index, value in enumerate(HOSTILE):
        try:
            result = check(value, v15, ep8, c2v4)
        except Exception as exc:  # noqa: BLE001
            escapes.append(f"SELFTEST-ESCAPE totality[{index}]: raised "
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
# Section 16.  Entry.
# ---------------------------------------------------------------------------
def _usage() -> None:
    sys.stderr.write(
        "usage: python3 -I -B check-r1-v1.7.py [--selftest]\n"
        "       python3 -I -B check-r1-v1.7.py --subject PATH\n")


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
                    "R1V17-UNSUPPORTED-INVOCATION: --subject takes a path\n")
                return 2
            subject_override = argv[index]
        else:
            sys.stderr.write(
                f"R1V17-UNSUPPORTED-INVOCATION: unknown option {arg!r}\n")
            _usage()
            return 2
        index += 1
    if do_selftest and subject_override is not None:
        sys.stderr.write(
            "R1V17-UNSUPPORTED-INVOCATION: --selftest runs against the pinned "
            "subject only\n")
        return 2

    # INERT BYTES FIRST.  Nothing below this point runs if a pinned input moved.
    try:
        snaps = verified_snapshots()
    except PinRefusal as exc:
        sys.stderr.write(
            f"R1V17-PIN-REFUSED: a pinned input did not match its digest, so "
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
                f"R1V17-UNSUPPORTED-INVOCATION: cannot read "
                f"{subject_override}: {type(exc).__name__}: {exc}\n")
            return 2
        subject_name = subject_override

    try:
        doc = strict_parse(subject_bytes, subject_name)
        v15 = strict_parse(snaps[V15_PATH], V15_PATH)
        ep8 = lenient_parse(snaps[EP8_PATH], EP8_PATH)
        c2v4 = lenient_parse(snaps[C2V4_PATH], C2V4_PATH)
    except PinRefusal as exc:
        sys.stderr.write(f"R1V17-PARSE-REFUSED: {exc}\n")
        return 2 if subject_override is None else 4

    if do_selftest:
        escapes, mutations, parsers, hostiles = selftest(
            doc, v15, ep8, c2v4, subject_bytes)
        if escapes and escapes[0].startswith("SELFTEST-REFUSED"):
            for line in escapes:
                print(line)
            print("R1 v1.7 selftest: NOT RUN (the base was not clean)")
            return 3
        if escapes:
            for line in escapes:
                print(line)
            print(f"R1 v1.7 selftest: FAIL ({len(escapes)} escapes)")
            return 1
        print(f"R1 v1.7 selftest: PASS ({mutations} mutations APPLIED and "
              f"EXECUTED, {parsers} raw parser probes each naming its token, "
              f"{hostiles} hostile totality shapes)")
        return 0

    stats: dict[str, Any] = {}
    findings = check(doc, v15, ep8, c2v4, stats=stats)

    if subject_override is not None:
        digest = hashlib.sha256(subject_bytes).hexdigest()
        print(f"R1V17-DIAGNOSTIC: {subject_name}")
        print(f"R1V17-DIAGNOSTIC: sha256 {digest}")
        print("R1V17-DIAGNOSTIC: the subject pin was NOT enforced; this run is "
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
    print(f"  predecessor v1.5 {PINS[V15_PATH]} UNTOUCHED; check-r1-v1.5.py "
          f"read-only at {PINS[V15_CHECKER_PATH]}")
    print(f"  pinned predecessor instrument check-r1-v1.6.py "
          f"{PINS[V16_CHECKER_PATH]} UNTOUCHED, hashed only, not imported")
    print(f"  ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md {PINS[ARCH_PLAN_PATH]}, "
          f"hashed only, never opened")
    print(f"  CIR-B1: {stats.get('anchored')} of {EXPECT_PINNED_VECTORS} "
          f"published vectors EXTERNALLY ANCHORED and rebuilt -- "
          f"{EXPECT_DERIVED_FROM_V15} from live v1.5 through the fieldSetRule, "
          f"{EXPECT_DERIVED_FROM_BASIS} from the rebuilt basis through the "
          f"declared derivation ({stats.get('generated')} operands generated, "
          f"{stats.get('literals')} declared and each put to live v1.5's closed "
          f"type).  The predecessor anchored 6")
    print(f"  the corpus is pairwise DISTINCT on recordValue, record bytes, "
          f"leaf root and derivationDigest; every control's measured axis "
          f"equals its declared axis exactly")
    print(f"  RECIPE DERIVED, not transcribed: {stats.get('topFields')} record "
          f"fields and {stats.get('nested')} nested types built from the "
          f"artifact's own grammar; framing tags PARSED from live EP8 clause "
          f"text; order rules PARSED from live v1.5; every leaf type resolved "
          f"through live v1.5 closedTypes; variants derived from live v1.5's "
          f"projectionByVariant")
    print(f"  {stats.get('wrongness')} WRONGNESS probes executed -- collapse, "
          f"mass collapse, sha856: prefix, well-formed-but-wrong digest, "
          f"out-of-vocabulary enum, widened axis, inverted prose -- each "
          f"republished with this instrument's own encoder and each refused on "
          f"a NAMED condition")
    print(f"  {stats.get('models')} control prose claims cross-checked against "
          f"the axis they move, in BOTH directions; "
          f"{stats.get('requiredKindViolators')} vector measured unreachable "
          f"under live v1.5's requiredKind and required to say so")
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
    print(f"  NOT verified by this instrument ({len(NOT_VERIFIED)} items, "
          f"including CIR-B1's resolution status and its named residual; see "
          f"NOT_VERIFIED in this source)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
