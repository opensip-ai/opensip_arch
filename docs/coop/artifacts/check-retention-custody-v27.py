#!/usr/bin/env python3
"""Retained checker for retention-tiers.v27.json.

WHY THIS FILE EXISTS, STATED BEFORE ANYTHING ELSE.

  retention-tiers.v27.json is a DERIVATION: eight `set` operations over the
  independently-ACCEPTED predecessor retention-tiers.v26.json.  Its own
  $.instrumentPosition states the residual plainly -- 0 of the resolved
  document's 20 vectors and 0 of its 24 invariants are mechanically exercised
  against it -- and IMPLEMENTATION-FREEZE.md section 7.1 grades that
  DISQUALIFYING FOR APPLICATION.  The predecessor's instrument cannot narrow it:
  check-retention-custody-v26.py carries `SUBJECT = "retention-tiers.v26.json"`
  as a CONSTANT with no subject-selection option, refuses any argument at exit 2
  with RT26-UNSUPPORTED-INVOCATION, and hard-pins v26's own digest.  Section 7.8
  is the licence for this file: a NEW CHECKER IS A NEW FILE AND EDITS NOTHING.

THE CENTRAL DESIGN REQUIREMENT, AND IT IS THE NEWEST STRUCTURAL FINDING IN THE
CORPUS.

  IMPLEMENTATION-FREEZE.md section 7.3, rider added 2026-08-06: section 7.3 has
  always told READERS to resolve a derivation rather than read it, and the
  CONSUMING INSTRUMENTS still read flat.  To a flat reader a derivation is
  indistinguishable from a DEFECTIVE artifact -- check-threat-claims.py:359 does
  a bare json.loads and then tests four top-level keys, a standalone disposition
  has 4 of 4 and a derivation has 0 of 4, and the gate then emits *"disposition
  has no executable counterexamples"*, the exact string that exists to flag a
  fabricated one.

  So this instrument RESOLVES the declared derivation and asserts over the
  RESOLVED VALUE.  It never asserts a Part A / Part C / Part D property over the
  delta bytes.  Asserting over the delta would reproduce, in the very lineage
  that exposed the defect, the defect section 7.3 exists to forbid.

  The resolved value is a VALUE, not a file.  Its digest is taken over
  json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':'),
  allow_nan=False).encode('utf-8').  No file with those bytes need ever exist and
  this instrument writes none.

HOW THE DERIVATION READER WAS OBTAINED, AND WHY IT IS RE-IMPLEMENTED RATHER THAN
EXECUTED.

  check-completeness.py already carries a derivation reader that finds the
  declaration by SHAPE rather than by the key name `derivedFrom` -- because
  locating it by name would reproduce CMP-IR-01 one level up -- and its reader
  was independently reviewed at 0 blockers against a third resolver sharing no
  code.  That discipline is adopted here in full: shape not name, verify before
  use, never degrade silently, and a refusal is published rather than swallowed.

  Its CODE is not executed here, and the reason is measured rather than
  preferred.  Run against these bytes it returns no declaration and one error:

      'derivedFrom' carries an operation list and 2 predecessor name(s) and
      2 digest(s); a derivation must state exactly one of each, so no effective
      contract can be materialised

  because retention-tiers.v27 states TWO filenames (the predecessor and its
  independent review) and TWO digests (the predecessor's BYTE digest and its
  CANONICAL-VALUE digest).  Even with that relaxed, its `apply_operations`
  requires each operation to carry `value`; v27's operations carry `to`.  Two
  independent incompatibilities, so executing it could not resolve the subject at
  all.  That is not a defect this file can repair -- it is measured and reported
  as RT27-GATE, below.

  What is re-implemented is therefore strictly stronger, and it closes the trap
  check-completeness.py names against itself: `is_operation_list` there requires
  `bool(value)`, so an EMPTY operation list makes the declaration return None
  with no error branch and a ZERO-OPERATION DERIVATION IS INVISIBLE.  Here an
  empty operation list is a NAMED REFUSAL (RT27-DERIV-EMPTY-OPERATIONS), never a
  silent absence.  And the two filenames and two digests are disambiguated by
  MEASUREMENT rather than by key name: the predecessor is the declared filename
  whose bytes hash to one of the declared digests, the byte digest is the one
  that equals sha256(file bytes), and the canonical-value digest is the one that
  equals sha256(canonical(parsed value)).  No key name is read to decide any of
  the three.

WHAT IT EXERCISES, AND HOW THE 20 VECTORS AND 24 INVARIANTS ARE REACHED.

  All 20 rows of $.partC_retentionBounds.vectors.rows and all 24 entries of
  $.partC_retentionBounds.invariants are executed AGAINST THE RESOLVED VALUE, by
  hash-verifying check-retention-custody-v26.py and executing its verified
  in-memory bytes as a runtime input -- IMPLEMENTATION-FREEZE.md section 7.3's
  rule, used exactly as check-narrative-packet-agreement.py uses it against
  check-package-coherence.py, and for the same reason: a second private copy of
  a 5000-line reference derivation could disagree with the original and NEITHER
  INSTRUMENT WOULD BE ABLE TO SEE THE DISAGREEMENT.

  Executing is neither transcribing nor asserting.  Section 7.8's demand -- *an
  instrument must re-derive its constants from the artifact it checks, or it is
  testing its own transcription* -- is met three ways:

    1. THE VERDICT IS DERIVED, NOT ENCODED.  The executed battery is run TWICE,
       over the predecessor and over the resolved value, and what is gated is the
       DELTA between the two finding sets.  The expected delta is read out of
       retention-tiers.v27's own bytes: every residual it declares OPEN names the
       finding family it still fires ($.residualsLeftOpen[].alsoFiredBy), and the
       defect it declares REPAIRED names the family that must STOP firing
       ($.theDefectRepaired -- "fires RT26-COUNT twice").  Had the artifact
       claimed a different repair, the same gate would demand a different delta
       on its own.  Nothing about which findings are expected is hardcoded here.

    2. A SECOND, INDEPENDENT IMPLEMENTATION CROSS-CHECKS THE LOAD-BEARING
       ALGEBRA.  The Cap lift, the three demand expressions, the eviction order,
       the cause attribution, the DURABLE_AUTHORITATIVE demotion scan and the
       d9Axes biconditional are re-implemented in this file from the artifact's
       own published rule text and compared row-by-row against the executed
       module's answers (RT27-XCHECK).  Two implementations agreeing is evidence;
       one implementation reporting itself is not.

    3. THE STALE-INHERITED-FIGURE SWEEP IS GENERATED, NOT TRANSCRIBED.  Not one
       of the three repaired paths is written into this file.  The rule is
       structural and scoped BY REFERENT: for every object carrying both
       `measuredValues` and `measuredBoundary`, every standalone integer in the
       prose that is not a recomputed sibling value, AND IS the value the pinned
       predecessor publishes at the corresponding sibling path, is a stale
       inherited restatement.  Run against retention-tiers.v26 that rule returns
       exactly the two defects; run against the resolved v27 it returns none.
       Delete v27's repairs and the generator puts them back as findings.

READ-VS-PIN.  THE CHOICE SECTION 7.10 IS ABOUT, MADE DELIBERATELY AND STATED.

  Section 7.10: a guard that pins a decision's CURRENT state asserts that state
  will never change, and a digest pin cannot distinguish "the input legitimately
  advanced" from "the input is wrong".  Three classes are implemented, and the
  class is part of the diagnostic.  The classification is retention-tiers.v27's
  OWN, read from $.recordedInputsOfThisDeltaFile at runtime and compared against
  the table below IN BOTH DIRECTIONS, so a row that silently changes class is a
  finding.

    GATED (6)      Reviewed, frozen or superseded bytes no lane has any business
                   advancing.  Drift -> RT27-PIN-REFUSED, EXIT 2, nothing parsed.
    ADVANCING (3)  IMPLEMENTATION-FREEZE.md and IMPLEMENTER-BLUEPRINT.md move
                   constantly and are cited non-gated; so is the CD-RT-5
                   amendment draft.  Drift -> RT27-PIN-ADVANCED, a NAMED
                   NON-FATAL notice, and the run continues against LIVE bytes.
    DESTROYED (1)  product-dispositions.cd-rt-5-amendment.draft.v1.json was
                   edited in place after retention-tiers.v25 hard-pinned it at
                   4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea.
                   Those bytes are in NO commit on ANY branch, so the pin can
                   never be satisfied.  A file reappearing at that digest --
                   ANYWHERE under artifacts/, not merely at that path -- is a
                   fabrication and RT27-PIN-RESURRECTED fires at EXIT 2.

ENVIRONMENT PREREQUISITES, DECLARED UP FRONT (section 7.2: a verdict binds bytes
AND AN ENVIRONMENT).  A CRASH MUST NOT READ AS A FINDING.

  1. CPython 3.9 or later.  Otherwise RT27-UNSUPPORTED-INTERPRETER, exit 2.
  2. Invoked as `python3 -I -B`.  Caller-owned isolated startup is the prevention
     boundary.  Otherwise RT27-UNSUPPORTED-INVOCATION, exit 2.
  3. THE PYTHON STANDARD LIBRARY ONLY.  No third-party package, NO SUBPROCESS,
     no external binary, and in particular NO ripgrep -- `rg` is a shell function
     on this host and is not on PATH, which is why two rust-provider checkers
     abort with a traceback and their PASSED verdicts cannot be reproduced.
  4. Every declared input present.  A missing input is RT27-INPUT-MISSING at
     exit 2, naming the path -- never a traceback and never a finding.
  5. The tree may be under concurrent edit by other lanes.  Every input is
     re-hashed AFTER the run; anything that moved during it is reported as
     RT27-TREE-MOVED and every finding is republished as UNSAFE-TO-ATTRIBUTE.
     This is not hypothetical: while this instrument was being written, a
     transient mid-write state of product-dispositions.v1.json produced three
     findings that vanished one minute later.
  Every failure above exits 2 with a named diagnostic whose text says THE CHECK
  DID NOT RUN.  Exit 1 is reserved for findings about the artifact.

WHAT A GREEN RUN WOULD BE, AND WHAT IT WOULD NOT BE.  (Section 7.8, answered,
with a count, at --limits.)

  It would be author-side evidence that the derivation resolves to the value it
  says it does, that the resolved document's arithmetic and algebra close, that
  its quotations are quotations, and that the three repairs are the three repairs
  and nothing else moved.  It would NEVER be evidence that the artifact is RIGHT.
  This instrument binds STRUCTURE, TYPE, ARITHMETIC and DERIVATION.  It does not
  bind the TRUTH OF PROSE that asserts a JUDGEMENT.  Run --limits for the
  enumerated list, the count of ways this checker can be made to pass on a wrong
  artifact, and the worked examples.

Exit matrix, distinct by construction:
    0  clean
    1  findings about the artifact
    2  bad invocation, unsupported environment, missing input, integrity refusal,
       or a GATED pin mismatch.  THE CHECK DID NOT RUN.
    3  selftest refused or not certifying (the base was not clean, so a mutation
       result certifies nothing even though it is still reported)

Invocation:  python3 -I -B check-retention-custody-v27.py [--selftest]
                                                          [--part a|c|d|all]
                                                          [--limits]
"""

from __future__ import annotations

import sys

MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write(
        "RT27-UNSUPPORTED-INTERPRETER: this instrument requires CPython "
        f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later and found "
        f"{sys.version_info[0]}.{sys.version_info[1]}.  THE CHECK DID NOT RUN; "
        "no statement about retention-tiers.v27.json is made by this exit.\n")
    raise SystemExit(2)

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "RT27-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-retention-custody-v27.py`.  Caller-owned isolated startup is the "
        "prevention boundary; script code cannot undo interpreter or site "
        "activity that happened before line 1.  THE CHECK DID NOT RUN.\n")
    raise SystemExit(2)

import copy
import hashlib
import json
import pathlib
import re
import types
import unicodedata
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent

SUBJECT = "retention-tiers.v27.json"
# The dispatched digest of the subject.  Recorded, compared, and reported as a
# NAMED NOTICE rather than a refusal: the subject is what this instrument is
# about, so a reader must be told when it moves, and refusing to parse would
# hide every other finding behind one line.  Section 7.2: a change to reviewed
# bytes requires a version bump and a new verdict.
SUBJECT_SHA256 = "d39800b7595f58ab42a65316d4880754ef9a14022d52f7ca68fdbab423e7314c"
SUBJECT_BYTES = 130652

# The predecessor's retained instrument.  GATED, hash-verified, and EXECUTED as a
# runtime input under section 7.3.  It does not become normative and it is not a
# fallback contract; it is the reference derivation this file drives against a
# document it was never pointed at.
V26_CHECKER = "check-retention-custody-v26.py"

# ---------------------------------------------------------------------------
# GATED.  Exactly the six rows retention-tiers.v27.json marks
# HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN at
# $.recordedInputsOfThisDeltaFile.recorded[].gate.  The classification is the
# ARTIFACT'S; this table implements it and check_recorded_inputs compares the two
# in both directions on every run.  Section 7.2's recording obligation: a count
# is not a record, so every member is named with its digest.
# ---------------------------------------------------------------------------
GATED_PINS = {
    "artifacts/retention-tiers.v26.json":
        "a6546408fb38df95166f0ec41b1d9d9dae0dbda580684ff8a6e94f57145ad97e",
    "artifacts/retention-tiers.v26.review-independent.json":
        "ffd8a80d5d7a9273e04192d467fdc5d6a063d8201186c73be2fb0a9115aff916",
    "artifacts/check-retention-custody-v26.py":
        "7402759ff6d2b1378b61d4d76727648aebf216795dce965e37c2acf7647d18b9",
    "artifacts/retention-tiers.v25.json":
        "d62c1c0f3eec5ac7b496a4f2fe60b73daafdc69a2cbd500685d0800e54eeca52",
    "artifacts/retention-tiers.v24.json":
        "ba29c115a9064ab1cd66ea01751b238acf092b3d699ca43027de7a8dfe55a277",
    "artifacts/check-retention-custody-v24.py":
        "9a309302df6d2f1108f1fbfb4978bfc93b102eb0394c99ba7be7fc550d7fa909",
}

# ---------------------------------------------------------------------------
# ADVANCING.  The three rows the artifact marks CITED-DIGEST-RECORDED-NOT-GATED.
# The recorded digests are THE ARTIFACT'S, deliberately left as v27 wrote them:
# they are the baseline a drift notice prints against, and replacing them with
# today's values would erase the record rather than check it.  Section 7.10: pin
# what you depend on and re-extract it.  Both markdown documents had already
# advanced past v27's recorded values before this instrument was finished, which
# is the argument for the class rather than a hypothetical about it.
# ---------------------------------------------------------------------------
ADVANCING_PINS = {
    "IMPLEMENTATION-FREEZE.md":
        "44703bf4dea52bdfae880ea3cfc0ff40c2ef54c9f561407d373c9859b3a23cdd",
    "IMPLEMENTER-BLUEPRINT.md":
        "370691f427e32d93e1eb9d01df86ed49e74aa9f35485f44752a23972de84e7ae",
    "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json":
        "c4bd85c62ee957ba04fd9d99f8b8f780138792409eb51b79a2aff2d35d334b12",
}

# ---------------------------------------------------------------------------
# DESTROYED.  A pin whose bytes no longer exist anywhere.  Not a gate -- v27
# reclassified the file and this instrument implements the artifact's
# classification -- but the dead digest is recorded so a reader meets the
# explanation instead of hunting a corruption, and so that bytes reappearing at
# it are REFUSED rather than welcomed.  The resurrection guard is swept over
# EVERY file under artifacts/, not merely the one path, because a fabrication
# that wanted to satisfy a dead pin would not have to reuse its filename.
# ---------------------------------------------------------------------------
DESTROYED_DIGEST = (
    "4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea")
DESTROYED_PATH = "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json"

# Files the artifact itself declares unstable, used to grade a drift notice.
DECLARED_UNSTABLE_FALLBACK = (
    "IMPLEMENTATION-FREEZE.md",
    "IMPLEMENTER-BLUEPRINT.md",
    "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json",
    "artifacts/product-dispositions.v1.json",
)

# Content anchors instead of a whole-file digest on the two moving documents, for
# the reason check-retention-custody-v23/-v24/-v25/-v26 all give: a digest
# recorded for a file under edit is false the moment it is written.  Matched
# under section 7.7 folding, so a reflow, a blockquote or an emphasis run does
# not manufacture a refusal, while REMOVAL of the cited text still fails closed.
# Section 7.10 names the hazard: when v23/v24 began refusing their pins before
# parsing anything, the FREEZE_ANCHORS guard they carried went inert and nothing
# announced it.  These are checked BEFORE any pin can stop the run.
FREEZE_ANCHORS = (
    # 7.3, the 2026-08-06 rider -- the reason this instrument resolves rather
    # than reads, and the newest structural finding in the corpus
    "The CONSUMING INSTRUMENTS still read flat, and to a flat reader a "
    "derivation is indistinguishable from a DEFECTIVE artifact",
    "Before applying ANY derivation, measure what its declared consuming gate "
    "does with it",
    # 7.3, the 2026-08-05 rider -- the inherited-measurement rule v27 discharges
    "a derivation must state, for every inherited measurement, either that it "
    "re-measured it or that it did not",
    # 7.2.2 -- the standard this instrument is held to
    "a measurement that cannot fail the build is prose",
    "enumerate by what the figure DESCRIBES, never by what it is CALLED",
    # 7.8 -- the bound this instrument prints against itself, and its licence
    "these instruments bind structure and type; they do not bind the truth of "
    "content",
    "a new checker is a new file and edits nothing",
    # 7.10 -- the read-vs-pin rule this instrument implements
    "pin the PROPERTY, not the CURRENT VALUE, whenever the value is",
    "\"Unsatisfiable\" must be MEASURED against the recovery point, not asserted",
    # 7.1 -- the grade on the residual this instrument exists to narrow
    "a fair residual for a candidate, disqualifying for",
    # 6, law 18 and law 14 -- what PC-V-06/07/08 and RT26-A-INV-18 rest on
    "Closed-scalar admission is exact-type.",
    "A durability failure cannot report authoritative success; a provider fault "
    "cannot become a finding; a policy failure cannot become a host error.",
    # 7.7 -- the folding this instrument applies before every containment test
    "Fold markdown structure",
)

# ---------------------------------------------------------------------------
# RECORDED MEASUREMENTS about the reviewed bytes.  Section 7.2.2 gives a recorded
# measurement a HARD COMPARISON: an uncompared measurement is prose that looks
# like evidence, and going stale is a TRUE POSITIVE about these bytes.  Each of
# these is a property of the SUBJECT-AND-ITS-PINNED-CLOSURE that the artifact
# does not itself publish, so it cannot be re-derived from the artifact and is
# recorded instead -- which is exactly the case section 7.2.2 reserves for a hard
# pin.  Everything the artifact DOES publish is re-derived and never listed here.
# ---------------------------------------------------------------------------
RECORDED = {
    # resolution
    "predecessorByteSha256":
        "a6546408fb38df95166f0ec41b1d9d9dae0dbda580684ff8a6e94f57145ad97e",
    "predecessorCanonicalSha256":
        "546abee0f5329b13a67d33fb9517403b089eb454c369a303a419d7d3d2ab5080",
    "resolvedCanonicalSha256":
        "fc1df5580e18a16685199169a05938f365eaae3a54c9536e748c745cdfa62314",
    "operationCount": 8,
    "identityOperations": 5,
    "repairOperations": 3,
    # the executed closure, over the RESOLVED value
    "vectorsDeclared": 20,
    "invariantsDeclared": 24,
    "arithmeticRows": 7,
    "arithmeticRowsAgreeingUnderThePublishedExpressions": 7,
    "arithmeticRowsAgreeingUnderThePredecessorsExpressions": 1,
    "defaultConfigSizesSwept": 201,
    "defaultConfigEvictionsUnderThePublishedExpressions": 0,
    "defaultConfigEvictionsUnderThePredecessorsExpressions": 200,
    "crossDimensionSymbols": 0,
    "prefixInclusionViolations": 0,
    "prefixConfigurations": 150,
    "durableAuthoritativeCells": 6,
    "interactionOutcomes": 7,
    "d9BiconditionalRows": 19,
    "partitionKeyCount": 35,
    "verbatimStringKeys": 37,
    "verbatimSourceAttributed": 36,
    "verbatimFalseAbsentUnderARawSearch": 3,
    "typeSweepRespellings": 966,
    "typeSweepAdmitted": 0,
    # the delta file itself
    "deltaTopLevelKeys": 25,
    "resolvedTopLevelKeys": 41,
    "deltaScalarLeaves": 1811,
    "resolvedScalarLeaves": 2935,
}


class PinRefused(RuntimeError):
    """A GATED pin did not match, or an input could not be read.  Exit 2."""


class DuplicateKeyError(ValueError):
    pass


class Refused(RuntimeError):
    """A reference derivation must refuse rather than substitute."""


# ===========================================================================
# SECTION 0 -- PRIMITIVES.
# ===========================================================================

def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate object key {key!r}")
        out[key] = value
    return out


def parse_json(source: bytes, name: str) -> Any:
    """Section 7.5: every JSON input is parsed under a hook that raises on any
    repeated key at any depth, so a document that says one thing to one reader
    and another to the next is refused rather than silently resolved."""
    try:
        return json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise PinRefused(f"{name}: {type(exc).__name__}: {exc}") from exc


def canonical(value) -> bytes:
    """The recipe retention-tiers.v27 publishes at
    $.derivedFrom.resolvedValue.canonicalSerialisation, implemented from that
    text rather than copied from any producer.  It is a claim about a PARSED
    VALUE and never about any file's bytes."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_PUNCT = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-",
    "—": "-", "―": "-", "−": "-",
    "…": "...", " ": " ", " ": " ", " ": " ",
    " ": " ", " ": " ",
}
_MD = re.compile(r"[*_`|\\>#]+")


def fold(text: str) -> str:
    """Section 7.7's folding, applied BEFORE any containment test.

    The section records that a byte-literal search on a multi-word phrase returns
    a false ABSENT on line-wrapped text, and that whitespace normalisation ALONE
    still returns ABSENT on a blockquote -- IMPLEMENTATION-FREEZE.md states its
    standing rules inside `>` blocks, including the one sentence that makes
    escalating an unlisted gap legal.  Markdown structure is folded, not just
    whitespace.
    """
    text = unicodedata.normalize("NFKC", text)
    for src, dst in _PUNCT.items():
        text = text.replace(src, dst)
    text = _MD.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def whitespace_only(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def resolve_input(rel: str) -> pathlib.Path:
    """Inputs are named the way the artifact names them -- some with an
    `artifacts/` prefix, some bare.  Both roots are tried and the path actually
    read is reported, so a reader can tell which file was measured."""
    candidates = [COOP / rel, HERE / rel, HERE / pathlib.PurePosixPath(rel).name]
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


_STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")


def path_steps(path: str):
    """Steps of a `$.a.b[0].c` path, or None when the path is not plainly
    expressible.  Guessing at a malformed path is how a resolver invents a
    contract the artifact never declared."""
    if not isinstance(path, str) or not path:
        return None
    body = path[2:] if path.startswith("$.") else ("" if path == "$" else path)
    if body.startswith(".") or body.endswith(".") or ".." in body:
        return None
    if body == "":
        return []
    steps = [int(index) if index else name
             for index, name in _STEP_RE.findall(body)]
    return steps or None


def has_step(node, step) -> bool:
    if isinstance(node, dict):
        return isinstance(step, str) and step in node
    if isinstance(node, list):
        return isinstance(step, int) and 0 <= step < len(node)
    return False


def resolve_steps(root, steps):
    node = root
    for step in steps:
        if not has_step(node, step):
            return False, None
        node = node[step]
    return True, node


_ABSENT = object()


def get_path(doc, path: str, default=None):
    steps = path_steps(path)
    if steps is None:
        return default
    found, node = resolve_steps(doc, steps)
    return node if found else default


def exact_equal(left, right) -> bool:
    """Type-exact deep equality.  `True` is not `1`, `1` is not `1.0`.

    Python's `==` would accept all three, which is exactly the coercion a
    derivation's `from` restatement exists to forbid.  bool is decided by
    `type(...) is not type(...)` and therefore BEFORE int, which is the ordering
    retention-tiers.v27 names at $.derivedFrom.resolutionAlgorithm.step3.
    """
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def exact_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def scalar_leaves(node, path: str = "$"):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from scalar_leaves(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from scalar_leaves(value, f"{path}[{index}]")
    else:
        yield path, node


def objects_of(node, path: str = "$"):
    if isinstance(node, dict):
        yield path, node
        for key, value in node.items():
            yield from objects_of(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from objects_of(value, f"{path}[{index}]")


def census(doc) -> dict:
    """The leaf census, bool tested BEFORE int at every decision, because bool
    subclasses int in Python and testing int first silently classifies every
    boolean as an integer.  The int-first control is computed alongside so the
    ordering bug is visible if it is ever reintroduced."""
    out = {"scalarLeafPositions": 0, "intLeafPositions": 0,
           "floatLeafPositions": 0, "boolLeafPositions": 0,
           "nullLeafPositions": 0, "stringLeafPositions": 0,
           "floatLeafPaths": [], "nullLeafPaths": [],
           "intFirstControl_intLeafPositions": 0}
    for path, value in scalar_leaves(doc):
        out["scalarLeafPositions"] += 1
        if isinstance(value, int):
            out["intFirstControl_intLeafPositions"] += 1
        if isinstance(value, bool):
            out["boolLeafPositions"] += 1
        elif isinstance(value, int):
            out["intLeafPositions"] += 1
        elif isinstance(value, float):
            out["floatLeafPositions"] += 1
            out["floatLeafPaths"].append(path)
        elif value is None:
            out["nullLeafPositions"] += 1
            out["nullLeafPaths"].append(path)
        elif isinstance(value, str):
            out["stringLeafPositions"] += 1
    out["nonStringLeafPositions"] = (out["intLeafPositions"]
                                     + out["floatLeafPositions"]
                                     + out["boolLeafPositions"]
                                     + out["nullLeafPositions"])
    return out


# ===========================================================================
# SECTION 1 -- INPUT VERIFICATION.  Read as inert bytes and classify BEFORE
# parsing anything.
# ===========================================================================

def verified_inputs():
    """Returns (snapshots, notices).  A GATED mismatch or a missing input raises
    PinRefused, which main() turns into a named exit-2 diagnostic saying the
    check did not run.  An ADVANCING mismatch becomes a non-fatal notice and the
    LIVE bytes are used.  A DESTROYED digest reappearing anywhere is a refusal."""
    snaps = {}
    notices = []
    errors = []

    for name, expected in GATED_PINS.items():
        path = resolve_input(name)
        if not path.is_file():
            errors.append(f"RT27-INPUT-MISSING {name}: not found beside this "
                          f"instrument or one directory up")
            continue
        data = path.read_bytes()
        actual = sha_bytes(data)
        if actual != expected:
            errors.append(
                f"RT27-PIN-REFUSED {name}: GATED at {expected}, live {actual}. "
                f"The artifact itself classifies this input "
                f"HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN, so "
                f"this instrument refuses rather than re-pointing it. Repair is "
                f"a SUCCESSOR instrument, never an edit to this one")
            continue
        snaps[name] = data

    for name, expected in ADVANCING_PINS.items():
        path = resolve_input(name)
        if not path.is_file():
            errors.append(f"RT27-INPUT-MISSING {name}: not found beside this "
                          f"instrument or one directory up")
            continue
        data = path.read_bytes()
        snaps[name] = data
        actual = sha_bytes(data)
        if actual != expected:
            notices.append(
                f"RT27-PIN-ADVANCED {name}: recorded {expected[:16]}..., live "
                f"{actual[:16]}.... NOT A FINDING. The artifact classifies this "
                f"input CITED-DIGEST-RECORDED-NOT-GATED"
                + ("" if name not in DECLARED_UNSTABLE_FALLBACK else
                   " and names it as a file under concurrent edit")
                + ". This run therefore re-extracts what it depends on from the "
                  "LIVE bytes rather than refusing, per section 7.10. A pinned "
                  "input that ADVANCED costs a re-read; it does not cost a "
                  "successor instrument."
                + ("" if name in DECLARED_UNSTABLE_FALLBACK else
                   " NOTE: this file is NOT among those the artifact declares "
                   "unstable, so the advance is unexpected and deserves a look."))

    # The resurrection sweep.  Bytes cannot come back; a file hashing to the
    # destroyed digest ANYWHERE is a fabrication, not a recovery.
    art_dir = COOP / "artifacts"
    if art_dir.is_dir():
        for candidate in sorted(art_dir.iterdir()):
            if not candidate.is_file():
                continue
            try:
                if sha_bytes(candidate.read_bytes()) == DESTROYED_DIGEST:
                    errors.append(
                        f"RT27-PIN-RESURRECTED {candidate.name}: these bytes "
                        f"hash to {DESTROYED_DIGEST}, a digest whose bytes were "
                        f"destroyed by an in-place edit and are UNRECOVERABLE -- "
                        f"the file appears in no commit on any branch, so it is "
                        f"not in the 7cc0f8a recovery point. Bytes cannot come "
                        f"back. Either a file has been fabricated to match a "
                        f"dead pin or this instrument's record is wrong; either "
                        f"way nothing here may be trusted")
            except OSError:
                continue

    if errors:
        raise PinRefused(" | ".join(errors))
    return snaps, notices


def measure_all_inputs():
    """Every declared input's LIVE digest, measured at the moment of the call.
    Called once before the run and once after, so an input that moved underneath
    the measurement is reported rather than silently absorbed."""
    out = {}
    for name in list(GATED_PINS) + list(ADVANCING_PINS) + [
            f"artifacts/{SUBJECT}", "artifacts/product-dispositions.v1.json"]:
        path = resolve_input(name)
        out[name] = sha_bytes(path.read_bytes()) if path.is_file() else None
    return out


# ===========================================================================
# SECTION 2 -- THE DERIVATION READER.
#
# Shape, not name (CMP-IR-01).  Verify before use.  Never degrade silently.  An
# EMPTY operation list is a NAMED REFUSAL rather than an invisible absence --
# the trap check-completeness.py names against its own reader.
# ===========================================================================

JSON_NAME_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*\.json$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DERIVATION_VERBS = ("set",)


def is_operation(item) -> bool:
    return (isinstance(item, dict) and isinstance(item.get("op"), str)
            and isinstance(item.get("path"), str) and bool(item.get("path")))


def is_operation_list(value) -> bool:
    """NOTE the deliberate difference from check-completeness.py: `bool(value)`
    is NOT required here.  An empty list of operation-shaped members is still an
    operation list, and the caller refuses it BY NAME.  Requiring non-emptiness
    is what makes a zero-operation derivation invisible."""
    return (isinstance(value, list)
            and all(is_operation(item) for item in value))


def looks_like_operation_list(value) -> bool:
    """A list that is an operation list OR an empty list sitting in a block that
    otherwise looks like a declaration.  Kept separate so the empty case can be
    reported instead of skipped."""
    return isinstance(value, list) and all(is_operation(i) for i in value)


def find_declaration(document, errors):
    """Locate the derivation declaration by SHAPE.

    A value-producing declaration is a top-level object carrying at least one
    artifact filename, both a byte and canonical-value sha256, and exactly one
    operation list.  Requiring both digest roles is not a filename convention:
    apply_operations below constructs a VALUE from verified predecessor BYTES,
    and the resolver cannot establish both halves of that claim from one digest.

    This distinction is load-bearing.  The subject and its predecessor also
    contain ordinary operation histories and empty path lists.  Treating every
    top-level list of {op,path} records (or every empty list) as a derivation is
    the false positive that made the authored base exit before checking any of
    the 20 vectors or 24 invariants.  A historical log with only a predecessor
    byte digest is data inside a standalone artifact, not a request to replace
    that artifact with a recursively materialised value.

    The predecessor, byte digest and canonical-value digest are chosen by
    MEASUREMENT -- which file's bytes hash to which declared digest -- and never
    by key name.  Locating any of them by name would reproduce CMP-IR-01 one
    level up.
    """
    found = []
    for key, block in document.items():
        if not isinstance(block, dict):
            continue
        names = [v for v in block.values()
                 if isinstance(v, str) and JSON_NAME_RE.match(v)]
        digests = [v for v in block.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        # Screen for the two independently verifiable roles before looking at
        # lists.  This prevents unrelated empty lists and one-digest historical
        # operation logs from becoming malformed derivation declarations.
        if not names or len(set(digests)) < 2:
            continue
        op_lists = [v for v in block.values() if looks_like_operation_list(v)]
        if not op_lists:
            continue
        if len(op_lists) != 1:
            errors.append(
                f"RT27-DERIV-AMBIGUOUS-OPERATIONS '{key}' carries "
                f"{len(op_lists)} operation lists; a derivation must state "
                f"exactly one, so no effective contract can be materialised")
            continue
        if not op_lists[0]:
            errors.append(
                f"RT27-DERIV-EMPTY-OPERATIONS '{key}' declares a derivation with "
                f"ZERO operations. A zero-operation derivation asserts that the "
                f"successor IS the predecessor under a new name, which is a "
                f"claim, not an absence. It is refused by name here because a "
                f"reader that requires a non-empty operation list to recognise a "
                f"declaration cannot see this case at all")
            continue
        found.append((key, {"block": key, "names": names, "digests": digests,
                            "operations": op_lists[0]}))
    if len(found) > 1:
        errors.append("RT27-DERIV-AMBIGUOUS more than one top-level block has "
                      "the shape of a derivation declaration: "
                      + ", ".join(sorted(k for k, _ in found)))
        return None
    return found[0][1] if found else None


def bind_predecessor(declaration, errors):
    """Decide WHICH declared filename is the predecessor and WHICH declared
    digest is its byte digest, by measurement rather than by key name."""
    byte_matches = []
    for name in declaration["names"]:
        path = resolve_input(name if "/" in name else f"artifacts/{name}")
        if not path.is_file():
            continue
        digest = sha_bytes(path.read_bytes())
        if digest in declaration["digests"]:
            byte_matches.append((name, path, digest))
    if not byte_matches:
        errors.append(
            "RT27-DERIV-NO-PREDECESSOR none of the declared filenames "
            f"{declaration['names']} has bytes hashing to any declared digest "
            f"{[d[:16] + '...' for d in declaration['digests']]}. The "
            "predecessor is identified by MEASUREMENT, not by key name, and no "
            "measurement succeeds, so the effective contract cannot be built")
        return None
    if len(byte_matches) > 1:
        errors.append(
            "RT27-DERIV-AMBIGUOUS-PREDECESSOR more than one declared filename "
            "hashes to a declared digest: "
            + ", ".join(sorted(n for n, _, _ in byte_matches)))
        return None
    name, path, byte_digest = byte_matches[0]
    remaining = [d for d in declaration["digests"] if d != byte_digest]
    return {"name": name, "path": path, "byteDigest": byte_digest,
            "otherDigests": remaining}


def apply_operations(base, operations, errors):
    """Apply the declared operations in order.

    Every `set` must restate, at EXACT JSON TYPE with bool decided before int,
    the value it replaces.  A `from` mismatch REFUSES the whole resolution; it
    never silently overwrites.  An operation that does not find what it claims to
    replace is describing a document that no longer exists, and applying it
    anyway would publish a resolution nobody verified.
    """
    effective = copy.deepcopy(base)
    applied = []
    for index, op in enumerate(operations):
        verb, path = op.get("op"), op.get("path")
        where = f"operation {index} ({verb} {path})"
        if verb not in DERIVATION_VERBS:
            errors.append(f"RT27-DERIV-VERB {where}: unknown verb; the declared "
                          f"verb set is {list(DERIVATION_VERBS)}")
            continue
        if "from" not in op:
            errors.append(f"RT27-DERIV-NO-FROM {where}: a set must restate the "
                          f"value it replaces")
            continue
        if "to" not in op:
            errors.append(f"RT27-DERIV-NO-TO {where}: carries no replacement "
                          f"value")
            continue
        steps = path_steps(path)
        if steps is None or not steps:
            errors.append(f"RT27-DERIV-PATH {where}: path is not plainly "
                          f"resolvable")
            continue
        found, parent = resolve_steps(effective, steps[:-1])
        if not found or not isinstance(parent, (dict, list)):
            errors.append(f"RT27-DERIV-PARENT {where}: parent does not resolve "
                          f"to a container in the verified predecessor")
            continue
        if not has_step(parent, steps[-1]):
            errors.append(f"RT27-DERIV-ABSENT {where}: does not resolve against "
                          f"the verified predecessor, so the operation "
                          f"describes a document that does not exist")
            continue
        current = parent[steps[-1]]
        if not exact_equal(current, op["from"]):
            errors.append(
                f"RT27-DERIV-FROM {where}: declares it replaces {op['from']!r} "
                f"({type(op['from']).__name__}) and the verified predecessor "
                f"holds {current!r} ({type(current).__name__}). The comparison "
                f"is at exact JSON type with bool decided before int; the "
                f"derivation does not describe the bytes it is applied to")
            continue
        if type(op["from"]) is not type(op["to"]):
            errors.append(
                f"RT27-DERIV-TYPE {where}: 'from' is "
                f"{type(op['from']).__name__} and 'to' is "
                f"{type(op['to']).__name__}. This derivation declares that no "
                f"operation changes a leaf's type, and the census it inherits "
                f"depends on that")
            continue
        if not isinstance(op["to"], (str, int, float, bool)) and op["to"] is not None:
            errors.append(
                f"RT27-DERIV-NONSCALAR {where}: 'to' is a "
                f"{type(op['to']).__name__}. This derivation declares every "
                f"operation a set on an existing SCALAR leaf, and the inherited "
                f"leaf census rests on that")
            continue
        parent[steps[-1]] = copy.deepcopy(op["to"])
        applied.append(path)
    return effective, applied


def resolve_subject(document):
    """(resolved value, provenance, errors).  Materialise the effective contract
    or explain, by name, why it cannot be."""
    errors = []
    provenance = {}
    declaration = find_declaration(document, errors)
    if declaration is None:
        if not errors:
            errors.append(
                "RT27-DERIV-NONE this document declares no derivation, so there "
                "is no resolved value to assert over. Every Part A / Part C / "
                "Part D property this instrument exists to exercise lives in the "
                "predecessor and NONE OF THEM WAS CHECKED")
        return None, provenance, errors
    provenance["block"] = declaration["block"]
    provenance["operationCount"] = len(declaration["operations"])

    bound = bind_predecessor(declaration, errors)
    if bound is None:
        return None, provenance, errors
    provenance["predecessor"] = bound["name"]
    provenance["predecessorByteDigest"] = bound["byteDigest"]

    try:
        base = parse_json(bound["path"].read_bytes(), bound["name"])
    except PinRefused as exc:
        errors.append(f"RT27-DERIV-PARSE the verified predecessor did not parse "
                      f"under the duplicate-key-rejecting hook: {exc}")
        return None, provenance, errors
    if not isinstance(base, dict):
        errors.append("RT27-DERIV-SHAPE the verified predecessor is not a JSON "
                      "object")
        return None, provenance, errors

    base_canonical = sha_bytes(canonical(base))
    provenance["predecessorCanonicalDigest"] = base_canonical
    if base_canonical not in bound["otherDigests"]:
        errors.append(
            f"RT27-DERIV-CANONICAL the declaration carries "
            f"{[d[:16] + '...' for d in bound['otherDigests']]} beside the byte "
            f"digest, and the canonical serialisation of the parsed predecessor "
            f"hashes to {base_canonical}. A derivation's product is a VALUE, so "
            f"the value digest is the one the resolution is defined against and "
            f"it must be stated")

    # A predecessor may itself be a delta.  Resolve the chain rather than scoring
    # a delta that merely happens to sit one step back.
    inner_errors = []
    inner = find_declaration(base, inner_errors)
    if inner_errors:
        errors.extend(f"{bound['name']}: {item}" for item in inner_errors)
        return None, provenance, errors
    if inner is not None:
        provenance["predecessorIsItselfADerivation"] = True
        base, inner_prov, inner_errs = resolve_subject(base)
        provenance["via"] = inner_prov
        if base is None:
            errors.extend(inner_errs)
            return None, provenance, errors
    else:
        provenance["predecessorIsItselfADerivation"] = False

    effective, applied = apply_operations(base, declaration["operations"],
                                          errors)
    provenance["operationsApplied"] = len(applied)
    if errors:
        return None, provenance, errors
    provenance["resolvedCanonicalDigest"] = sha_bytes(canonical(effective))
    provenance["declaration"] = declaration
    provenance["parsedPredecessor"] = base
    return effective, provenance, errors


# ===========================================================================
# SECTION 3 -- CHECKS OVER THE RESOLUTION ITSELF.
# ===========================================================================

def check_resolution(delta, resolved, prov, ctx):
    """Everything the derivation claims about its own product, hard-compared."""
    out = []
    decl_block = get_path(delta, f"$.{prov.get('block', 'derivedFrom')}") or {}
    operations = prov["declaration"]["operations"]

    # 1. The recorded digests, compared to the measurements.
    if prov["predecessorByteDigest"] != RECORDED["predecessorByteSha256"]:
        out.append(f"RT27-DERIV-PREDECESSOR the derivation binds a predecessor "
                   f"whose bytes hash to {prov['predecessorByteDigest']}; this "
                   f"instrument was written against "
                   f"{RECORDED['predecessorByteSha256']}")
    if prov["predecessorCanonicalDigest"] != RECORDED["predecessorCanonicalSha256"]:
        out.append(f"RT27-DERIV-PREDECESSOR the parsed predecessor's canonical "
                   f"value hashes to {prov['predecessorCanonicalDigest']}, not "
                   f"the recorded {RECORDED['predecessorCanonicalSha256']}")

    # 2. The resolved value's canonical digest, both against the declaration and
    #    against the recorded measurement.
    measured = prov["resolvedCanonicalDigest"]
    declared = None
    for _, block in objects_of(decl_block):
        for key, value in block.items():
            if (isinstance(value, str) and SHA256_RE.match(value)
                    and "canonicalSerialisation" in block):
                declared = value
    if declared is None:
        # Locate by shape: the sha256 that sits in the same object as the
        # canonical-serialisation recipe.  Never by the key name `sha256`.
        for _, block in objects_of(decl_block):
            recipe = [v for v in block.values()
                      if isinstance(v, str) and "sort_keys=True" in v]
            digests = [v for v in block.values()
                       if isinstance(v, str) and SHA256_RE.match(v)]
            if recipe and len(digests) == 1:
                declared = digests[0]
    if declared is None:
        out.append("RT27-DERIV-NO-RESOLVED-DIGEST the derivation publishes no "
                   "digest over its own resolved value, so nothing states what "
                   "the resolution is supposed to produce")
    elif declared != measured:
        out.append(f"RT27-DERIV-RESOLVED the derivation declares its resolved "
                   f"value hashes to {declared} and applying its own operations "
                   f"to its own verified predecessor produces {measured}")
    if measured != RECORDED["resolvedCanonicalSha256"]:
        out.append(f"RT27-DERIV-RESOLVED the resolved value hashes to "
                   f"{measured}, not the recorded "
                   f"{RECORDED['resolvedCanonicalSha256']}")
    ctx["resolvedDigest"] = measured

    # 3. The single float.  The artifact states the canonical substring; check it
    #    rather than trusting the recipe, because a re-implementer whose float
    #    formatter emits `200` gets a different digest for a resolution that did
    #    not differ.
    blob = canonical(resolved).decode("utf-8")
    floats = [(p, v) for p, v in scalar_leaves(resolved)
              if isinstance(v, float)]
    ctx["resolvedFloatPaths"] = [p for p, _ in floats]
    if len(floats) != 1:
        out.append(f"RT27-DERIV-FLOAT the resolved value carries {len(floats)} "
                   f"floats; the derivation's encoding note names exactly one "
                   f"and a reimplementer is told to expect one")
    elif '"keepCount":200.0' not in blob:
        out.append("RT27-DERIV-FLOAT the canonical serialisation does not carry "
                   "the 17-character substring the derivation names, "
                   "'\"keepCount\":200.0'; a float formatter emitting 200 or "
                   "2.0e2 produces a different digest for the same value")

    # 4. The operation census, DERIVED from the operations rather than read.
    if len(operations) != RECORDED["operationCount"]:
        out.append(f"RT27-DERIV-OPCOUNT the derivation carries "
                   f"{len(operations)} operations, not the recorded "
                   f"{RECORDED['operationCount']}")
    classes = {}
    for op in operations:
        classes.setdefault(op.get("class", "<<UNCLASSED>>"), []).append(
            op.get("path"))
    ctx["operationClasses"] = classes
    identity = len(classes.get("IDENTITY", []))
    repair = len(classes.get("REPAIR", []))
    if identity != RECORDED["identityOperations"] or repair != RECORDED["repairOperations"]:
        out.append(f"RT27-DERIV-CLASSES the derivation classifies {identity} "
                   f"IDENTITY and {repair} REPAIR operations; the recorded "
                   f"measurement is {RECORDED['identityOperations']} and "
                   f"{RECORDED['repairOperations']}")
    if identity + repair != len(operations):
        out.append(f"RT27-DERIV-CLASSES {len(operations) - identity - repair} "
                   f"operation(s) carry no IDENTITY/REPAIR class, so the "
                   f"substantive delta cannot be separated from the identity "
                   f"delta by anything but reading")
    # An IDENTITY operation must not touch a figure the sweep measures, and a
    # REPAIR operation must.  Derived, not listed.
    for op in operations:
        if op.get("class") == "IDENTITY" and op.get("path", "").startswith(
                "$.corpusResiduals"):
            out.append(f"RT27-DERIV-CLASSES {op.get('path')} is classed IDENTITY "
                       f"and lands inside the residual block whose figures this "
                       f"artifact exists to repair")

    # 5. Resolution is EXACTLY the operations -- both directions.
    base = prov["parsedPredecessor"]
    before = dict(scalar_leaves(base))
    after = dict(scalar_leaves(resolved))
    differing = sorted(
        p for p in set(before) | set(after)
        if p not in before or p not in after
        or type(before[p]) is not type(after[p]) or before[p] != after[p])
    op_paths = sorted({op.get("path") for op in operations})
    ctx["differingLeafPaths"] = differing
    if differing != op_paths:
        only_moved = sorted(set(differing) - set(op_paths))
        only_claimed = sorted(set(op_paths) - set(differing))
        out.append(
            f"RT27-DERIV-EXACTLY the set of leaf paths at which the resolved "
            f"value differs from the verified predecessor is not the set of "
            f"operation paths. Moved but not declared: {only_moved}. Declared "
            f"but did not move: {only_claimed}")
    # And the artifact's own published statement of the same set.
    published = get_path(delta,
                         f"$.{prov['block']}.resolutionIsExactlyTheOperations."
                         f"differingLeafPaths")
    if isinstance(published, list) and sorted(published) != differing:
        out.append(f"RT27-DERIV-EXACTLY the derivation publishes a differing-leaf "
                   f"list of {len(published)} path(s) and the measured set has "
                   f"{len(differing)}; symmetric difference "
                   f"{sorted(set(published) ^ set(differing))}")
    return out


def check_census(delta, resolved, prov, ctx):
    """The inherited census is section 7.3's named silent-staleness site.  Every
    operation is a set on an existing scalar leaf and none changes a type, so the
    predecessor's own $.leafCensus must be EXACT of the resolved document.  That
    is the claim; this re-walks both and compares."""
    out = []
    resolved_c = census(resolved)
    delta_c = census(delta)
    ctx["resolvedCensus"] = resolved_c
    ctx["deltaCensus"] = delta_c

    if resolved_c["intLeafPositions"] + resolved_c["boolLeafPositions"] != \
            resolved_c["intFirstControl_intLeafPositions"]:
        out.append("RT27-CENSUS the int-first control does not equal "
                   "int+bool, so the bool-before-int ordering this census "
                   "depends on is not doing what it claims")

    inherited = get_path(resolved, "$.leafCensus") or {}
    for key in ("scalarLeafPositions", "nonStringLeafPositions",
                "intLeafPositions", "floatLeafPositions", "boolLeafPositions",
                "nullLeafPositions", "stringLeafPositions"):
        declared = inherited.get(key)
        if not exact_int(declared):
            out.append(f"RT27-CENSUS the resolved document's $.leafCensus.{key} "
                       f"is {declared!r}, not a JSON integer")
            continue
        if declared != resolved_c[key]:
            out.append(
                f"RT27-CENSUS the inherited $.leafCensus.{key} declares "
                f"{declared} and a walk of the RESOLVED value measures "
                f"{resolved_c[key]}. Section 7.3's rider names the inherited "
                f"census as the silent-staleness site: an inherited measurement "
                f"is republished under the successor's name and ages invisibly")
    for key, measured in (("floatLeafPaths", resolved_c["floatLeafPaths"]),
                          ("nullLeafPaths", resolved_c["nullLeafPaths"])):
        declared = inherited.get(key)
        if isinstance(declared, list) and sorted(declared) != sorted(measured):
            out.append(f"RT27-CENSUS the inherited $.leafCensus.{key} and the "
                       f"resolved walk differ: "
                       f"{sorted(set(declared) ^ set(measured))}")

    # The derivation's own re-measurement of the same thing.
    published = get_path(delta, f"$.{prov['block']}.resolvedDocumentCensus") or {}
    for key in ("scalarLeafPositions", "nonStringLeafPositions",
                "intLeafPositions", "floatLeafPositions", "boolLeafPositions",
                "nullLeafPositions", "stringLeafPositions"):
        declared = published.get(key)
        if exact_int(declared) and declared != resolved_c[key]:
            out.append(f"RT27-CENSUS the derivation's own resolvedDocumentCensus."
                       f"{key} declares {declared} and the resolved walk "
                       f"measures {resolved_c[key]}")

    # The delta file's own census, which section 7.2.2 requires to be the LAST
    # measurement taken and re-walked from the written bytes.  Four measured
    # instances in the corpus of a self-report that undercounts by exactly its
    # own size; this is the comparison that catches a fifth.
    own = get_path(delta, "$.leafCensusOfThisDeltaFile") or {}
    for key in ("scalarLeafPositions", "nonStringLeafPositions",
                "intLeafPositions", "floatLeafPositions", "boolLeafPositions",
                "nullLeafPositions", "stringLeafPositions"):
        declared = own.get(key)
        if not exact_int(declared):
            out.append(f"RT27-CENSUS $.leafCensusOfThisDeltaFile.{key} is "
                       f"{declared!r}, not a JSON integer")
            continue
        if declared != delta_c[key]:
            out.append(
                f"RT27-CENSUS $.leafCensusOfThisDeltaFile.{key} declares "
                f"{declared} and a walk of the WRITTEN BYTES measures "
                f"{delta_c[key]}. Section 7.2.2 records four instances of a "
                f"self-report measured before it was attached to the object it "
                f"describes, undercounting by exactly its own size")
    for key, measured in (("floatLeafPaths", delta_c["floatLeafPaths"]),
                          ("nullLeafPaths", delta_c["nullLeafPaths"])):
        declared = own.get(key)
        if isinstance(declared, list) and sorted(declared) != sorted(measured):
            out.append(f"RT27-CENSUS $.leafCensusOfThisDeltaFile.{key} and the "
                       f"walk differ: {sorted(set(declared) ^ set(measured))}")
    arithmetic = own.get("arithmetic")
    if isinstance(arithmetic, str):
        expected = (f"{delta_c['intLeafPositions']} + "
                    f"{delta_c['boolLeafPositions']} + "
                    f"{delta_c['floatLeafPositions']} + "
                    f"{delta_c['nullLeafPositions']} = "
                    f"{delta_c['nonStringLeafPositions']} non-string, and "
                    f"{delta_c['nonStringLeafPositions']} + "
                    f"{delta_c['stringLeafPositions']} = "
                    f"{delta_c['scalarLeafPositions']}.")
        if whitespace_only(arithmetic) != whitespace_only(expected):
            out.append(f"RT27-CENSUS $.leafCensusOfThisDeltaFile.arithmetic reads "
                       f"{arithmetic!r}; regenerated from the walk it is "
                       f"{expected!r}")

    if resolved_c["scalarLeafPositions"] != RECORDED["resolvedScalarLeaves"]:
        out.append(f"RT27-CENSUS the resolved value has "
                   f"{resolved_c['scalarLeafPositions']} scalar leaves, not the "
                   f"recorded {RECORDED['resolvedScalarLeaves']}")
    if delta_c["scalarLeafPositions"] != RECORDED["deltaScalarLeaves"]:
        out.append(f"RT27-CENSUS the delta file has "
                   f"{delta_c['scalarLeafPositions']} scalar leaves, not the "
                   f"recorded {RECORDED['deltaScalarLeaves']}")
    return out


def check_key_locator(delta, resolved, ctx):
    """The keyLocator claims a PARTITION, so it is falsifiable from either side
    and both sides are executed.  versioning-policy.v14's only blocker was a
    keyLocator that asserted keys were 'NOT in this file' when they were."""
    out = []
    block = get_path(delta, "$.keyLocator")
    if not isinstance(block, dict):
        out.append("RT27-KEYLOC the delta file carries no keyLocator, so nothing "
                   "states which of its keys are the resolved document's and "
                   "which are the delta's own -- CMP-IR-01's exact setup")
        return out
    delta_keys = set(delta)
    resolved_keys = set(resolved)

    op_target = block.get("operationTargetKeys") or []
    restated = block.get("restatedIdenticalKeys") or []
    delta_only = block.get("deltaOnlyKeys") or []
    resolved_only = block.get("resolvedOnlyKeys") or []

    # direction 1 -- every DELTA-ONLY key is absent from the resolved document
    bad = sorted(k for k in delta_only if k in resolved_keys)
    if bad:
        out.append(f"RT27-KEYLOC direction1: {len(bad)} key(s) classed "
                   f"DELTA-ONLY are present in the resolved document: {bad}")
    # direction 2 -- every RESOLVED-ONLY key is absent from this delta file
    bad = sorted(k for k in resolved_only if k in delta_keys)
    if bad:
        out.append(f"RT27-KEYLOC direction2: {len(bad)} key(s) classed "
                   f"RESOLVED-ONLY are top-level keys of this delta file: {bad}. "
                   f"This is versioning-policy.v14's only blocker exactly")
    # direction 3 -- every OPERATION-TARGET key is in both and EQUAL at exact type
    for key in op_target:
        if key not in delta_keys:
            out.append(f"RT27-KEYLOC direction3: {key} is classed "
                       f"OPERATION-TARGET and is not a top-level key here")
        elif key not in resolved_keys:
            out.append(f"RT27-KEYLOC direction3: {key} is classed "
                       f"OPERATION-TARGET and is absent from the resolved "
                       f"document")
        elif not exact_equal(delta[key], resolved[key]):
            out.append(f"RT27-KEYLOC direction3: {key} is {delta[key]!r} here "
                       f"and {resolved[key]!r} in the resolved document, so this "
                       f"file describes a document it did not produce")
    # direction 4 -- every RESTATED-IDENTICAL key is in both and EQUAL
    for key in restated:
        if key not in delta_keys or key not in resolved_keys:
            out.append(f"RT27-KEYLOC direction4: {key} is classed "
                       f"RESTATED-IDENTICAL and is missing from one side")
        elif not exact_equal(delta[key], resolved[key]):
            out.append(f"RT27-KEYLOC direction4: {key} is {delta[key]!r} here "
                       f"and {resolved[key]!r} in the resolved document")
    # direction 5 -- the three classes PARTITION this file's top-level keys
    classified = set(op_target) | set(restated) | set(delta_only)
    unclassified = sorted(delta_keys - classified)
    if unclassified:
        out.append(f"RT27-KEYLOC direction5: {len(unclassified)} top-level "
                   f"key(s) of this file fall in no class: {unclassified}")
    extra = sorted(classified - delta_keys)
    if extra:
        out.append(f"RT27-KEYLOC direction5: {len(extra)} key(s) are classified "
                   f"and are not top-level keys of this file: {extra}")
    # direction 6 -- every top-level key an operation touches is classified right
    touched = sorted({(path_steps(op.get("path")) or ["?"])[0]
                      for op in (ctx.get("operations") or [])})
    also_here = sorted(k for k in touched if k in delta_keys)
    asserted_absent = sorted(k for k in touched if k not in delta_keys)
    for name, measured in (("topLevelKeysTouchedByOperations", touched),
                           ("ofThoseAlsoTopLevelKeysOfThisDeltaFile", also_here),
                           ("ofThoseNOTTopLevelKeysOfThisDeltaFile",
                            asserted_absent)):
        declared = block.get(name)
        if isinstance(declared, list) and sorted(declared) != measured:
            out.append(f"RT27-KEYLOC direction6: {name} declares "
                       f"{sorted(declared)} and the operations touch {measured}")
    # the published cardinalities, hard-compared
    for name, measured in (("deltaOnlyKeyCount", len(delta_only)),
                           ("resolvedOnlyKeyCount", len(resolved_only)),
                           ("deltaFileTopLevelKeyCount", len(delta_keys)),
                           ("resolvedDocumentTopLevelKeyCount",
                            len(resolved_keys)),
                           ("operationCount", len(ctx.get("operations") or []))):
        declared = block.get(name)
        if exact_int(declared) and declared != measured:
            out.append(f"RT27-KEYLOC {name} declares {declared} and the "
                       f"measurement is {measured}")
    # RESOLVED-ONLY must be exactly the resolved keys this file does not expose
    measured_resolved_only = sorted(resolved_keys - delta_keys)
    if isinstance(resolved_only, list) and sorted(resolved_only) != measured_resolved_only:
        out.append(f"RT27-KEYLOC resolvedOnlyKeys is not the measured set; "
                   f"symmetric difference "
                   f"{sorted(set(resolved_only) ^ set(measured_resolved_only))}")
    # and the recorded cardinalities
    if len(delta_keys) != RECORDED["deltaTopLevelKeys"]:
        out.append(f"RT27-KEYLOC the delta file exposes {len(delta_keys)} "
                   f"top-level keys, not the recorded "
                   f"{RECORDED['deltaTopLevelKeys']}")
    if len(resolved_keys) != RECORDED["resolvedTopLevelKeys"]:
        out.append(f"RT27-KEYLOC the resolved document has {len(resolved_keys)} "
                   f"top-level keys, not the recorded "
                   f"{RECORDED['resolvedTopLevelKeys']}")
    ctx["keyLocatorDirections"] = 6
    return out


# ===========================================================================
# SECTION 4 -- THE GENERATED STALE-INHERITED-FIGURE SWEEP.
#
# Section 7.2.2: *enumerate by what the figure DESCRIBES, never by what it is
# CALLED.*  A key-name sweep is a fine instrument and a false census -- the v26
# review's method was "every integer leaf whose key ends in `count`", and the
# defective key is `recordedInputs`, which ends in nothing.
#
# NOT ONE of the three repaired paths appears in this file.  The rule is
# structural: for every object carrying both `measuredValues` and
# `measuredBoundary`, every standalone integer in the prose that is neither a
# recomputed sibling value NOR explicable as a figure about another artifact, and
# WHICH IS the value the pinned predecessor publishes at the corresponding
# sibling path, is a stale inherited restatement.  The predecessor comparison is
# what makes it a finding rather than a guess, and it is decidable against a
# GATED pin.
# ===========================================================================

# The referent map: what is this figure a measurement OF?  Keyed by the
# measuredValues member name, valued by an expression over the document that
# carries it.  Every entry is a referent, never a key-name pattern.
REFERENTS = {
    "recordedInputs":
        lambda d: len(get_path(d, "$.recordedInputs.recorded") or []),
    "partBSurfacesLeftUnchanged":
        lambda d: sum(1 for r in (get_path(
            d, "$.inheritance.exhaustivePartitionOfV24.partB") or [])
            if r.get("disposition") == "UNCHANGED"),
    "partBSurfacesProposedForChange":
        lambda d: sum(1 for r in (get_path(
            d, "$.inheritance.exhaustivePartitionOfV24.partB") or [])
            if r.get("disposition") == "CHANGED"),
    "vectorsDeclared":
        lambda d: len(get_path(d, "$.partC_retentionBounds.vectors.rows") or []),
    "invariantsDeclared":
        lambda d: len(get_path(d, "$.partC_retentionBounds.invariants") or []),
    "retainedResiduals":
        lambda d: len(get_path(d, "$.retainedResiduals") or []),
    "newResiduals":
        lambda d: len(get_path(d, "$.newResiduals") or []),
    "declaredDependencies":
        lambda d: len(get_path(d, "$.declaredDependencies") or []),
}

_TOKEN_RE = re.compile(r"(?<![\w.\-])(\d+)(?![\w.])")


def referent_sweep(doc, predecessor):
    """Returns (rows, findings, strays).  A row is one object carrying both a
    measuredValues dict and a measuredBoundary sentence."""
    rows = []
    findings = []
    strays = []
    for path, obj in objects_of(doc):
        values = obj.get("measuredValues")
        boundary = obj.get("measuredBoundary")
        if not (isinstance(values, dict) and isinstance(boundary, str)):
            continue
        recomputed = {}
        unrecomputable = []
        for key, value in values.items():
            if not exact_int(value):
                continue
            if key in REFERENTS:
                recomputed[key] = REFERENTS[key](doc)
            else:
                recomputed[key] = value
                unrecomputable.append(key)
        rows.append({"path": path, "members": len(recomputed),
                     "unrecomputable": unrecomputable})
        # value half -- a declared figure that its own referent contradicts
        for key, value in values.items():
            if key in REFERENTS and exact_int(value) and value != recomputed[key]:
                findings.append(
                    f"RT27-SWEEP {path}.measuredValues.{key} declares {value} and "
                    f"its own referent recomputes {recomputed[key]}. Section "
                    f"7.2.2 gives a recorded measurement a hard comparison; this "
                    f"is a measurement about the document's own contents, which "
                    f"can never legitimately advance")
        # prose half -- a sentence restating a figure its own siblings contradict
        live = set(recomputed.values())
        pred_values = get_path(predecessor, f"{path}.measuredValues")
        pred_map = ({k: v for k, v in pred_values.items() if exact_int(v)}
                    if isinstance(pred_values, dict) else {})
        for token in sorted({int(t) for t in _TOKEN_RE.findall(boundary)}):
            if token in live:
                continue
            owners = sorted(k for k, v in pred_map.items() if v == token)
            if owners:
                findings.append(
                    f"RT27-SWEEP {path}.measuredBoundary restates {token}, which "
                    f"is the value the PINNED PREDECESSOR publishes at "
                    f"measuredValues.{owners} while these bytes recompute "
                    f"{sorted(live)}. A stale figure inherited into a prose "
                    f"sentence ages silently, because nothing in the delta "
                    f"mentions it and a reader sees only the successor's name")
            else:
                strays.append((path, token))
    return rows, findings, strays


# ===========================================================================
# SECTION 5 -- THE EXECUTED CLOSURE.
#
# Section 7.3: a retained checker that hash-verifies a set of files before
# executing them may internally execute superseded predecessors.  Those files are
# RUNTIME INPUTS of the instrument.  They do not become normative, they do not
# become a fallback contract, and their presence does not weaken this verdict.
# ===========================================================================

def load_v26_module(source: bytes):
    """Execute the hash-verified in-memory bytes.  Never imports from disk after
    verification, so the bytes executed are the bytes hashed."""
    module = types.ModuleType("rt26_reference")
    module.__file__ = str(resolve_input(f"artifacts/{V26_CHECKER}"))
    code = compile(source.decode("utf-8"), module.__file__, "exec")
    exec(code, module.__dict__)  # noqa: S102 -- the point of section 7.3
    return module


def build_reference_context(mod, doc):
    snaps, notices = mod.verified_inputs()
    parsed = {name: mod._parse(data, name) for name, data in snaps.items()
              if name.endswith(".json")}
    d9 = parsed["d9-exit-contract.v1.14.json"]
    ctx = {
        "doc": doc, "snaps": snaps,
        "v22": parsed["retention-tiers.v22.json"],
        "v23": parsed["retention-tiers.v23.json"],
        "v24": parsed["retention-tiers.v24.json"],
        "v24rev": parsed["retention-tiers.v24.review-independent.json"],
        "v25": parsed["retention-tiers.v25.json"],
        "v25rev": parsed["retention-tiers.v25.review-independent.json"],
        "d9": d9,
        "d9errorCodes": list(mod.get_path(d9, "$.codeVocabulary.errorCodes") or []),
        "product": parsed["artifacts/product-dispositions.v1.json"],
        "tm3": parsed["threat-model.v3.json"],
        "ev10": parsed["evidence.v10.json"],
    }
    return ctx, notices


FAMILY_RE = re.compile(r"^(RT26-[A-Z0-9\-]+)")


def families(findings):
    out = {}
    for finding in findings:
        match = FAMILY_RE.match(finding)
        out.setdefault(match.group(1) if match else "<<UNNAMED>>", []).append(
            finding)
    return out


def check_executed_closure(delta, resolved, mod, ctx):
    """Run the reference battery TWICE -- over the verified predecessor and over
    the RESOLVED value -- and gate the DELTA.  The expected delta is derived from
    retention-tiers.v27's own bytes, never encoded here."""
    out = []
    ref_ctx_pred, notices = build_reference_context(mod, ctx["predecessor"])
    pred_findings = mod.run_all(ctx["predecessor"], ref_ctx_pred, ctx["part"])

    ref_ctx_res, _ = build_reference_context(mod, resolved)
    res_findings = mod.run_all(resolved, ref_ctx_res, ctx["part"])
    ctx["referenceNotices"] = notices
    ctx["referenceContext"] = ref_ctx_res
    ctx["predecessorFindings"] = pred_findings
    ctx["resolvedFindings"] = res_findings

    pred_fam = families(pred_findings)
    res_fam = families(res_findings)
    ctx["predecessorFamilies"] = {k: len(v) for k, v in pred_fam.items()}
    ctx["resolvedFamilies"] = {k: len(v) for k, v in res_fam.items()}

    # --- what the artifact says must STOP firing ---------------------------
    repaired = get_path(delta, "$.theDefectRepaired") or {}
    claim = json.dumps(repaired, ensure_ascii=False)
    stop = sorted(set(re.findall(r"RT26-[A-Z0-9\-]+", claim)))
    ctx["familiesClaimedRepaired"] = stop
    if not stop:
        out.append("RT27-DELTA $.theDefectRepaired names no finding family the "
                   "predecessor's retained instrument fires, so nothing states "
                   "what this successor is supposed to have repaired and the "
                   "repair cannot be gated")
    for family in stop:
        before = len(pred_fam.get(family, []))
        after = len(res_fam.get(family, []))
        if before == 0:
            out.append(
                f"RT27-DELTA the artifact claims {family} fires on the "
                f"predecessor and running the predecessor's own retained "
                f"instrument against the verified predecessor fires it 0 times. "
                f"A repair with no reproduced defect behind it is a claim")
        if after != 0:
            out.append(
                f"RT27-DELTA {family} still fires {after} time(s) against the "
                f"RESOLVED value. The derivation exists to repair it: "
                f"{res_fam.get(family, [''])[0][:220]}")

    # --- what the artifact says must KEEP firing ---------------------------
    keep = {}
    for entry in (get_path(delta, "$.residualsLeftOpen.fromTheV26IndependentReview")
                  or []):
        text = str(entry.get("alsoFiredBy") or "")
        for family in set(re.findall(r"RT26-[A-Z0-9\-]+", text)):
            times = 2 if re.search(r"\btwice\b", text) else 1
            keep[family] = max(keep.get(family, 0), times)
    ctx["familiesClaimedStillOpen"] = keep
    for family, times in sorted(keep.items()):
        after = len(res_fam.get(family, []))
        if after != times:
            out.append(
                f"RT27-DELTA the artifact declares residual {family} OPEN and "
                f"names it as still fired {times} time(s); against the RESOLVED "
                f"value it fires {after}. A residual left open by NAMING it is "
                f"only left open if the naming is true")

    # --- nothing else may move --------------------------------------------
    expected_gone = set(stop)
    expected_stay = set(keep)
    # The two identity findings a v26-BOUND driver necessarily produces about a
    # v27 document.  These are DERIVED, not listed: each must be explained by an
    # IDENTITY operation on a top-level key, and its text must quote that
    # operation's `to` value.
    identity_targets = {}
    for op in ctx["operations"]:
        if op.get("class") != "IDENTITY":
            continue
        steps = path_steps(op.get("path")) or []
        if len(steps) == 1:
            identity_targets[f"$.{steps[0]}"] = op.get("to")
    added = sorted(set(res_findings) - set(pred_findings))
    removed = sorted(set(pred_findings) - set(res_findings))
    unexplained_added = []
    explained_added = []
    for finding in added:
        family = FAMILY_RE.match(finding)
        family = family.group(1) if family else "<<UNNAMED>>"
        hit = None
        for path, value in identity_targets.items():
            if path in finding and repr(value) in finding:
                hit = path
        if hit is not None:
            explained_added.append((finding, hit))
        elif family in expected_stay:
            explained_added.append((finding, "declared-open residual"))
        else:
            unexplained_added.append(finding)
    ctx["closureAdded"] = added
    ctx["closureRemoved"] = removed
    ctx["closureExplainedAdded"] = explained_added
    if unexplained_added:
        out.append(
            f"RT27-DELTA resolving this derivation introduces "
            f"{len(unexplained_added)} finding(s) the artifact does not account "
            f"for, against the predecessor's own retained battery: "
            f"{[f[:200] for f in unexplained_added]}")
    for finding in removed:
        family = FAMILY_RE.match(finding)
        family = family.group(1) if family else "<<UNNAMED>>"
        if family not in expected_gone:
            out.append(
                f"RT27-DELTA resolving this derivation silently REMOVES a "
                f"finding the artifact does not claim to repair: "
                f"{finding[:220]}")
    if len(identity_targets) != len(
            [op for op in ctx["operations"] if op.get("class") == "IDENTITY"
             and len(path_steps(op.get("path")) or []) == 1]):
        out.append("RT27-DELTA the identity operations could not be reduced to "
                   "top-level targets, so the added findings cannot be explained "
                   "by derivation and are not being suppressed by inference")

    # --- the executed battery's own reported coverage, hard-compared -------
    vec = ref_ctx_res.get("vectorReport") or {}
    inv = ref_ctx_res.get("invariantReport") or {}
    ctx["vectorReport"] = vec
    ctx["invariantReport"] = inv
    declared_vectors = len(
        get_path(resolved, "$.partC_retentionBounds.vectors.rows") or [])
    declared_invariants = len(
        get_path(resolved, "$.partC_retentionBounds.invariants") or [])
    if vec.get("declared") != declared_vectors or vec.get("executed") != declared_vectors:
        out.append(f"RT27-CLOSURE {vec.get('executed')} of {vec.get('declared')} "
                   f"vectors executed against the resolved value; the resolved "
                   f"document declares {declared_vectors} rows and every one "
                   f"must be exercised")
    if inv.get("declared") != declared_invariants or inv.get("executed") != declared_invariants:
        out.append(f"RT27-CLOSURE {inv.get('executed')} of "
                   f"{inv.get('declared')} invariants executed against the "
                   f"resolved value; the resolved document declares "
                   f"{declared_invariants}")
    if declared_vectors != RECORDED["vectorsDeclared"]:
        out.append(f"RT27-CLOSURE the resolved document declares "
                   f"{declared_vectors} vectors, not the recorded "
                   f"{RECORDED['vectorsDeclared']}")
    if declared_invariants != RECORDED["invariantsDeclared"]:
        out.append(f"RT27-CLOSURE the resolved document declares "
                   f"{declared_invariants} invariants, not the recorded "
                   f"{RECORDED['invariantsDeclared']}")
    vacuous = vec.get("controlsVacuous") or []
    if vacuous:
        out.append(f"RT27-CLOSURE {len(vacuous)} negative control(s) are VACUOUS "
                   f"-- the rejected reading the row names produces the same "
                   f"answer as the accepted one, so the control proves nothing: "
                   f"{vacuous}")
    if (vec.get("controlsRun") or 0) < 1:
        out.append("RT27-CLOSURE no rejected reading was executed, so every "
                   "negative control is a label rather than a measurement")

    # B1's Cap algebra, as the executed reference measured it over the RESOLVED
    # value.  Compared to the recorded measurement AND to this file's own second
    # implementation (RT27-XCHECK, below).
    b1 = ref_ctx_res.get("b1") or {}
    ctx["b1"] = b1
    checks = (
        ("arithmeticRows", b1.get("arithmeticRows"), RECORDED["arithmeticRows"]),
        ("rows agreeing under the PUBLISHED expressions",
         len(b1.get("publishedAgree") or []),
         RECORDED["arithmeticRowsAgreeingUnderThePublishedExpressions"]),
        ("rows agreeing under the PREDECESSOR's expressions",
         len(b1.get("v25Agree") or []),
         RECORDED["arithmeticRowsAgreeingUnderThePredecessorsExpressions"]),
        ("evictable-set sizes swept at the default 0/0/0",
         b1.get("defaultConfigSizesSwept"), RECORDED["defaultConfigSizesSwept"]),
        ("sizes evicting at the default under the PUBLISHED expressions",
         len(b1.get("defaultConfigNonZero") or []),
         RECORDED["defaultConfigEvictionsUnderThePublishedExpressions"]),
        ("sizes evicting at the default under the PREDECESSOR's expressions",
         len(b1.get("defaultConfigNonZeroV25") or []),
         RECORDED["defaultConfigEvictionsUnderThePredecessorsExpressions"]),
        ("cross-dimension symbols", len(b1.get("crossDimensionSymbols") or []),
         RECORDED["crossDimensionSymbols"]),
        ("prefix-inclusion violations", b1.get("prefixInclusionViolations"),
         RECORDED["prefixInclusionViolations"]),
        ("prefix configurations", b1.get("prefixConfigurations"),
         RECORDED["prefixConfigurations"]),
    )
    for label, measured, expected in checks:
        if measured != expected:
            out.append(f"RT27-CLOSURE B1 {label}: measured {measured!r}, "
                       f"recorded {expected!r}")
    if len(b1.get("publishedAgree") or []) != (b1.get("arithmeticRows") or -1):
        out.append("RT27-CLOSURE B1: the published demand expressions do not "
                   "reproduce every arithmetic vector of the resolved document, "
                   "which is the whole of the IR-RT25-B1 repair")
    if len(b1.get("v25Agree") or []) >= (b1.get("arithmeticRows") or 0):
        out.append("RT27-CLOSURE B1: the PREDECESSOR's rejected expressions "
                   "reproduce as many rows as the published ones, so the control "
                   "separates nothing and the repair is unmeasured")

    # Quotation discipline, over the RESOLVED value, with folding applied first.
    for label, key, expected in (
            ("string-valued *Verbatim keys", "verbatimStringKeys",
             RECORDED["verbatimStringKeys"]),
            ("verified against their attributed source", "verbatimVerified",
             RECORDED["verbatimStringKeys"]),
            ("source-attributed fields", "verbatimSourceAttributed",
             RECORDED["verbatimSourceAttributed"])):
        measured = ref_ctx_res.get(key)
        if measured != expected:
            out.append(f"RT27-CLOSURE quotations: {label} measured {measured!r}, "
                       f"recorded {expected!r}")
    if ref_ctx_res.get("verbatimNotFound"):
        out.append(f"RT27-CLOSURE quotations: "
                   f"{ref_ctx_res.get('verbatimNotFound')} verbatim field(s) do "
                   f"not resolve against the source their own NAME attributes "
                   f"them to")
    ctx["verbatim"] = {k: ref_ctx_res.get(k) for k in
                       ("verbatimStringKeys", "verbatimVerified",
                        "verbatimSourceAttributed", "verbatimFalseAbsent",
                        "verbatimFalseAbsentNormalised")}
    false_absent = ref_ctx_res.get("verbatimFalseAbsent")
    if not isinstance(false_absent, int) or false_absent < 1:
        out.append(
            f"RT27-CLOSURE quotations: {false_absent!r} of the source-attributed "
            f"verbatim fields would read FALSE-ABSENT under a raw byte-literal "
            f"search. Section 7.7's folding is claimed load-bearing; at 0 it is "
            f"not, and the claim is no longer supported by these bytes")

    ctx["anchors"] = (ref_ctx_res.get("anchorsPresent"),
                      ref_ctx_res.get("anchorsTotal"))
    ctx["cdRt5"] = (ref_ctx_res.get("cdRt5Status"),
                    ref_ctx_res.get("cdRt5Quoted"))
    return out


def check_type_sweep(resolved, mod, ctx):
    """Section 6 law 18, over the RESOLVED value: every closed scalar is admitted
    by EXACT JSON type at any depth BEFORE its content is compared.  The hostile
    sweep respells each guarded int/bool position as a float, as a bool drawn
    from 0/1, and as an int drawn from a bool, and requires every respelling to
    be REFUSED."""
    out = []
    base_type, counts = mod.type_findings(resolved)
    sweep = mod.hostile_sweep(resolved, base_type)
    ctx["typeCounts"] = counts
    ctx["typeSweep"] = sweep
    for arm in ("float", "boolFromZeroOrOneInt", "intFromBool"):
        if sweep[arm]["admitted"]:
            out.append(f"RT27-SWEEP-TYPE {arm}: {sweep[arm]['admitted']} "
                       f"position(s) admitted a respelled scalar: "
                       f"{sweep[arm]['escapes'][:5]}")
    if counts["unruledIntOrBoolLeafPositions"]:
        out.append(f"RT27-SWEEP-TYPE "
                   f"{counts['unruledIntOrBoolLeafPositions']} int/bool leaf "
                   f"position(s) are outside the frozen type registry, so the "
                   f"sweep does not cover them")
    if sweep["respellingsAttempted"] != RECORDED["typeSweepRespellings"]:
        out.append(f"RT27-SWEEP-TYPE {sweep['respellingsAttempted']} respellings "
                   f"attempted, not the recorded "
                   f"{RECORDED['typeSweepRespellings']}")
    if sweep["respellingsAdmitted"] != RECORDED["typeSweepAdmitted"]:
        out.append(f"RT27-SWEEP-TYPE {sweep['respellingsAdmitted']} respellings "
                   f"admitted, not the recorded {RECORDED['typeSweepAdmitted']}")
    if sweep["respellingsAttempted"] == 0:
        out.append("RT27-SWEEP-TYPE the type sweep attempted nothing, so a "
                   "0-admitted result is vacuous")
    return out


# ===========================================================================
# SECTION 6 -- THE SECOND, INDEPENDENT IMPLEMENTATION.
#
# Section 7.8: *an instrument must re-derive its constants from the artifact it
# checks, or it is testing its own transcription.*  Executing the reference
# battery is not transcription, but a single implementation reporting itself is
# not agreement either.  What follows is a second implementation of the
# load-bearing algebra, written here from the artifact's own published rule text,
# and compared row-by-row against the executed module's answers.
# ===========================================================================

class _Unbounded:
    __slots__ = ()

    def __repr__(self):
        return "UNBOUNDED"


UNBOUNDED = _Unbounded()


def lift(configured):
    """$.partC_retentionBounds.sweep.demands.repair -- ONE total lift, applied
    identically to all three configured values, before any demand is computed:
    unbounded_if_zero(v) := UNBOUNDED if v == 0 else v."""
    return UNBOUNDED if configured == 0 else configured


def le_cap(value: int, cap) -> bool:
    return True if cap is UNBOUNDED else value <= cap


def x_demand_count(cap, order) -> int:
    """max(0, len(evictable) - cap_count), total on Cap: at UNBOUNDED the
    subtraction is strictly below zero and max0 gives 0."""
    if cap is UNBOUNDED:
        return 0
    return max(0, len(order) - cap)


def x_demand_size(cap, order) -> int:
    """the smallest k in [0, len(order)] such that total_bytes(order[k:]) <= cap.
    At UNBOUNDED, k = 0 satisfies it by the ORDER ALONE -- no arithmetic
    extension is needed on this dimension at all."""
    for k in range(0, len(order) + 1):
        if le_cap(sum(m["bytes"] for m in order[k:]), cap):
            return k
    return len(order)


def x_demand_time(cap, order, now: int) -> int:
    """the number of leading members of the eviction order whose admission time
    is strictly older than cutoff := now - cap_age.  At UNBOUNDED the cutoff is
    strictly before every representable admission time, so nothing is older."""
    if cap is UNBOUNDED:
        return 0
    cutoff = now - cap
    count = 0
    for member in order:
        if member["admittedAt"] < cutoff:
            count += 1
        else:
            break
    return count


def x_eviction_order(evictable):
    return sorted(evictable, key=lambda m: (m["admittedAt"], m["id"]))


def x_eviction(bounds, evictable, now: int):
    order = x_eviction_order(evictable)
    demands = {
        "time": x_demand_time(lift(bounds["maxAgeSeconds"]), order, now),
        "size": x_demand_size(lift(bounds["maxTotalBytes"]), order),
        "count": x_demand_count(lift(bounds["keepCount"]), order),
    }
    return max(demands.values()) if demands else 0, demands, order


def cross_check_b1(resolved, mod, ref_ctx, ctx):
    """Re-execute the arithmetic vector rows under THIS file's implementation and
    require it to agree with the executed reference, row by row."""
    out = []
    rows = get_path(resolved, "$.partC_retentionBounds.vectors.rows") or []
    per_row = (ctx.get("b1") or {}).get("perRow") or {}
    agreed = disagreed = 0
    for row in rows:
        rid = row.get("id")
        if rid not in per_row:
            continue
        bounds = (row.get("bounds") or {})
        # The arithmetic rows describe the synthetic population by count and,
        # optionally, total bytes.  Rebuild that population from those fields;
        # the authored first draft looked for the nonexistent key
        # `evictableSetSize`, silently skipped all seven rows, and then printed
        # “agrees on 0 rows.”  A second implementation with a zero denominator
        # is not corroboration.
        size = row.get("evictableCount")
        if not exact_int(size) or size < 0:
            continue
        total = row.get("evictableTotalBytes")
        if total is not None and (not exact_int(total) or total < 0):
            continue
        each = ((total // size) if total is not None and size else 100)
        members = [{"id": f"m{i}", "bytes": each,
                    "admittedAt": mod.NOW - 1000}
                   for i in range(size)]
        if not all(exact_int(bounds.get(k)) for k in
                   ("maxAgeSeconds", "maxTotalBytes", "keepCount")):
            continue
        mine, demands, _ = x_eviction(bounds, members, mod.NOW)
        theirs = per_row[rid].get("underV26")
        if theirs is None:
            continue
        if mine == theirs:
            agreed += 1
        else:
            disagreed += 1
            out.append(
                f"RT27-XCHECK {rid}: this file's independent implementation of "
                f"the published demand expressions evicts {mine} "
                f"(demands {demands}) and the executed reference derivation "
                f"evicts {theirs}. Two implementations of one published rule "
                f"disagree, so at most one of them implements it")
    ctx["xcheckB1"] = {"agreed": agreed, "disagreed": disagreed}
    # The default configuration, swept independently.
    non_zero = 0
    for size in range(0, 201):
        members = [{"id": f"m{i}", "bytes": 1, "admittedAt": i}
                   for i in range(size)]
        evicted, _, _ = x_eviction(
            {"maxAgeSeconds": 0, "maxTotalBytes": 0, "keepCount": 0},
            members, mod.NOW)
        if evicted:
            non_zero += 1
    ctx["xcheckDefaultNonZero"] = non_zero
    if non_zero != RECORDED["defaultConfigEvictionsUnderThePublishedExpressions"]:
        out.append(
            f"RT27-XCHECK the default 0/0/0 configuration evicts something at "
            f"{non_zero} of 201 evictable-set sizes under this file's own "
            f"implementation of the published lift. 0/0/0 is the configuration "
            f"of every project nobody has configured, so a non-zero here purges "
            f"every unconfigured project")
    return out


def cross_check_demotion(resolved, mod, ref_ctx, ctx):
    """FREEZE LAW 14, re-implemented.  *A durability failure cannot report
    authoritative success.*  Built here from the pinned v24 cells with the
    resolved document's own published after-rows substituted -- the RESOLVED
    table, never the artifact's description of it."""
    out = []
    cells = [copy.deepcopy(c) for c in
             (get_path(ref_ctx["v24"], "$.partA_firstRunRetentionConsent."
                                       "askDecisionTable.cells") or [])]
    for changed in (get_path(resolved, "$.partA_repairsForcedByThePostureDecision."
                                       "askDecisionTable.changedCells") or []):
        index, after = changed.get("index"), changed.get("after")
        if exact_int(index) and 0 <= index < len(cells) and isinstance(after, dict):
            cells[index] = copy.deepcopy(after)
    outcomes = {o["id"]: copy.deepcopy(o) for o in
                (get_path(ref_ctx["v24"], "$.partA_firstRunRetentionConsent."
                                          "interactionOutcomes.outcomes") or [])}
    for changed in (get_path(resolved, "$.partA_repairsForcedByThePostureDecision."
                                       "interactionOutcomes.changed") or []):
        after = changed.get("after")
        if isinstance(after, dict) and after.get("id") in outcomes:
            outcomes[after["id"]] = copy.deepcopy(after)

    durable = [c for c in cells
               if c.get("requestedCustody") == "DURABLE_AUTHORITATIVE"]
    ctx["xcheckDurableCells"] = len(durable)
    ctx["xcheckOutcomes"] = len(outcomes)
    if len(durable) != RECORDED["durableAuthoritativeCells"]:
        out.append(f"RT27-XCHECK the resolved table has {len(durable)} "
                   f"DURABLE_AUTHORITATIVE cells, not the recorded "
                   f"{RECORDED['durableAuthoritativeCells']}")
    if len(outcomes) != RECORDED["interactionOutcomes"]:
        out.append(f"RT27-XCHECK the resolved table has {len(outcomes)} "
                   f"interaction outcomes, not the recorded "
                   f"{RECORDED['interactionOutcomes']}")
    violations = 0
    for cell in durable:
        axis = f"{cell.get('invocationProfile')}/{cell.get('policyPresence')}"
        outcome = cell.get("outcome")
        write = cell.get("durableSourceDerivedWritePermitted")
        if outcome == "PROCEED-DURABLE" and write is not True:
            violations += 1
            out.append(f"RT27-XCHECK SILENT DEMOTION IS REACHABLE at {axis}: "
                       f"outcome PROCEED-DURABLE with "
                       f"durableSourceDerivedWritePermitted {write!r}")
        if outcome == "PROCEED-EPHEMERAL":
            violations += 1
            out.append(f"RT27-XCHECK a DURABLE_AUTHORITATIVE request at {axis} "
                       f"resolves to PROCEED-EPHEMERAL, which is the demotion "
                       f"itself")
        if outcome == "REFUSE" and write is True:
            violations += 1
            out.append(f"RT27-XCHECK the row at {axis} both REFUSES and permits "
                       f"a durable write")
    ctx["xcheckDemotionViolations"] = violations
    # The biconditional, over v24's own 19 rows.
    rows = list(get_path(ref_ctx["v24"], "$.partA_firstRunRetentionConsent."
                                         "askDecisionTable.cells") or []) + \
        list(get_path(ref_ctx["v24"], "$.partA_firstRunRetentionConsent."
                                      "interactionOutcomes.outcomes") or [])
    deviations = 0
    nulls = 0
    for row in rows:
        axes_null = row.get("d9Axes", "MISSING") is None
        terminal = row.get("derivedClass") == "NOT-A-TERMINATION"
        if axes_null:
            nulls += 1
            if (row.get("derivedExitCode") != -1
                    or row.get("derivedErrorCode") != "NONE"
                    or row.get("derivedReasonCodes") != []):
                deviations += 1
        if axes_null != terminal:
            deviations += 1
    ctx["xcheckBiconditional"] = {"rows": len(rows), "nulls": nulls,
                                  "deviations": deviations}
    if len(rows) != RECORDED["d9BiconditionalRows"]:
        out.append(f"RT27-XCHECK the pinned v24 population is {len(rows)} rows, "
                   f"not the {RECORDED['d9BiconditionalRows']} the "
                   f"(d9Axes is null) <-> (NOT-A-TERMINATION) biconditional was "
                   f"measured over")
    if deviations:
        out.append(f"RT27-XCHECK the d9Axes biconditional deviates on "
                   f"{deviations} of {len(rows)} rows under this file's own "
                   f"implementation")
    return out


def cross_check_partition(resolved, ctx):
    """The 35-key exhaustive partition of v24, re-derived rather than read."""
    out = []
    part_a = get_path(resolved, "$.inheritance.exhaustivePartitionOfV24.partA") or []
    part_b = get_path(resolved, "$.inheritance.exhaustivePartitionOfV24.partB") or []
    total = len(part_a) + len(part_b)
    ctx["partition"] = {"partA": len(part_a), "partB": len(part_b),
                        "total": total}
    if total != RECORDED["partitionKeyCount"]:
        out.append(f"RT27-XCHECK the exhaustive partition of v24 holds {total} "
                   f"keys, not the recorded {RECORDED['partitionKeyCount']}")
    for name, rows in (("partA", part_a), ("partB", part_b)):
        bad = [r.get("key") for r in rows
               if r.get("disposition") not in ("CHANGED", "UNCHANGED")]
        if bad:
            out.append(f"RT27-XCHECK {name} carries {len(bad)} row(s) with no "
                       f"CHANGED/UNCHANGED disposition, so the partition is not "
                       f"one: {bad[:6]}")
    keys = [r.get("key") for r in part_a + part_b]
    duplicates = sorted({k for k in keys if keys.count(k) > 1})
    if duplicates:
        out.append(f"RT27-XCHECK the partition repeats {len(duplicates)} key(s) "
                   f"across its two halves, so it is a cover and not a "
                   f"partition: {duplicates}")
    return out


def cross_check_folding(ctx):
    """Section 7.7, re-measured here rather than taken from the reference: fold
    markdown structure, not just whitespace, before concluding any quotation is
    absent.  The freeze states its standing rules inside blockquotes, so
    whitespace normalisation ALONE still returns ABSENT on them."""
    out = []
    text = ctx["freezeText"]
    raw = 0
    ws = 0
    folded_hits = 0
    for anchor in FREEZE_ANCHORS:
        if anchor in text:
            raw += 1
        if whitespace_only(anchor) in whitespace_only(text):
            ws += 1
        if fold(anchor) in fold(text):
            folded_hits += 1
    ctx["anchorFolding"] = {"raw": raw, "whitespace": ws,
                            "folded": folded_hits, "total": len(FREEZE_ANCHORS)}
    missing = [a[:60] for a in FREEZE_ANCHORS if fold(a) not in fold(text)]
    if missing:
        out.append(
            f"RT27-ANCHOR {len(missing)} of {len(FREEZE_ANCHORS)} content "
            f"anchors are ABSENT from the live IMPLEMENTATION-FREEZE.md even "
            f"under section 7.7 folding: {missing}. These anchor the sections "
            f"this instrument implements; their removal is a change to the rules "
            f"it enforces and must not pass silently")
    if folded_hits <= raw:
        out.append(
            f"RT27-ANCHOR folding recovers no anchor a raw byte-literal search "
            f"misses ({raw} raw, {folded_hits} folded). Section 7.7 calls this "
            f"the sharpest false-negative generator in the package; at parity "
            f"the discipline is untested by these anchors rather than "
            f"vindicated by them")
    return out


# ===========================================================================
# SECTION 7 -- THE CONSUMING-GATE MEASUREMENT.
#
# Section 7.3, rider added 2026-08-06, verbatim in substance: *Before applying
# ANY derivation, measure what its declared consuming gate does with it.*  This
# is that measurement, executed rather than asserted.
# ===========================================================================

def check_consuming_gates(delta, resolved, ctx):
    out = []
    notices = []

    # --- the corpus's only derivation-RESOLVING instrument -----------------
    completeness = resolve_input("artifacts/check-completeness.py")
    if not completeness.is_file():
        notices.append("RT27-GATE check-completeness.py is not present, so the "
                       "derivation-resolving gate could not be measured. NOT a "
                       "pass: the measurement did not run")
    else:
        module = types.ModuleType("cmp_reference")
        module.__file__ = str(completeness)
        try:
            exec(compile(completeness.read_bytes().decode("utf-8"),  # noqa: S102
                         module.__file__, "exec"), module.__dict__)
            declaration, errors = module.derivation_declaration(delta)
            ctx["completenessErrors"] = errors
            ctx["completenessResolved"] = declaration is not None
            op_keys = sorted({k for op in ctx["operations"] for k in op})
            needs_value = "value" not in op_keys
            if declaration is None:
                out.append(
                    "RT27-GATE the corpus's only derivation-RESOLVING instrument "
                    "cannot materialise this artifact's effective contract. "
                    f"check-completeness.py returns no declaration and reports: "
                    f"{errors!r}. Measured across every JSON artifact in this "
                    "corpus, ten other derivations declare exactly one "
                    "predecessor filename and one digest and this one declares "
                    "two of each"
                    + (f"; independently, every operation here carries {op_keys} "
                       f"and that reader requires 'value', so even a relaxed "
                       f"declaration would refuse all "
                       f"{len(ctx['operations'])} operations"
                       if needs_value else "")
                    + ". IMPLEMENTATION-FREEZE.md section 7.3's 2026-08-06 rider "
                    "requires this measurement BEFORE any derivation is applied, "
                    "and grades the status quo -- correctness depending on which "
                    "of two forms an author happened to choose -- NOT ACCEPTABLE. "
                    "THIS IS A FINDING ABOUT FORM, NOT SUBSTANCE: every "
                    "substantive claim this derivation makes verifies, this "
                    "instrument resolves it, and the artifact asserts nowhere "
                    "that any other instrument can. A reviewer who reads the "
                    "rider as binding only on the applier may reclassify this "
                    "row as a notice; no other measurement in this run changes "
                    "if they do")
            elif needs_value:
                out.append("RT27-GATE check-completeness.py accepts the "
                           "declaration and would refuse every operation: its "
                           "resolver requires 'value' and these operations carry "
                           f"{op_keys}")
        except Exception as exc:  # noqa: BLE001 -- a gate that crashes is not a pass
            notices.append(f"RT27-GATE check-completeness.py could not be "
                           f"executed ({type(exc).__name__}: {exc}); the "
                           f"derivation-gate measurement DID NOT RUN and is not "
                           f"reported as a pass")

    # --- the flat reader section 7.3's rider measures ----------------------
    # Reported honestly: retention-tiers is NOT a V10 disposition artifact, so
    # check-threat-claims.py is not this artifact's gate. The four keys are
    # measured on both forms anyway, because the rider's whole point is that the
    # delta/standalone difference is invisible until someone measures it.
    flat_keys = ("claimId", "invariants", "counterexampleFixtures",
                 "retainedResiduals")
    delta_hits = sum(1 for k in flat_keys if k in delta)
    resolved_hits = sum(1 for k in flat_keys if k in resolved)
    ctx["flatReader"] = (delta_hits, resolved_hits, len(flat_keys))
    if delta_hits != resolved_hits:
        notices.append(
            f"RT27-GATE the flat four-key test at check-threat-claims.py:359 "
            f"scores this DELTA {delta_hits} of {len(flat_keys)} and the "
            f"RESOLVED value {resolved_hits} of {len(flat_keys)}. That gate "
            f"binds the V10 DISPOSITION artifact and not this one, so it is not "
            f"this artifact's consuming gate -- reported because a difference "
            f"between the two forms is exactly what the rider says nobody "
            f"measures")
    else:
        notices.append(
            f"RT27-GATE measured: the flat four-key test at "
            f"check-threat-claims.py:359 scores the delta and the resolved value "
            f"IDENTICALLY at {delta_hits} of {len(flat_keys)}, so the "
            f"delta-versus-standalone asymmetry that gate exhibits on "
            f"v10-disposition does NOT arise here. That gate binds the V10 "
            f"disposition artifact, not this one")
    ctx["gateNotices"] = notices
    return out


# ===========================================================================
# SECTION 8 -- PIN HYGIENE, IDENTITY AND THE ARTIFACT'S OWN RESIDUALS.
# ===========================================================================

def check_recorded_inputs(delta, ctx):
    """Section 7.10: classify every input GATED / ADVANCING / DESTROYED, and
    compare this instrument's table against the artifact's IN BOTH DIRECTIONS, so
    a row that silently changes class is a finding."""
    out = []
    block = get_path(delta, "$.recordedInputsOfThisDeltaFile")
    if not isinstance(block, dict):
        out.append("RT27-INPUTS the delta file records no inputs. Section 7.2's "
                   "recording obligation: a count is not a record, and neither "
                   "is an absence")
        return out
    recorded = block.get("recorded") or []
    declared = {}
    for row in recorded:
        path = row.get("path")
        gate = str(row.get("gate") or "")
        klass = row.get("class")
        declared[path] = (klass, gate, row.get("sha256"))
        if klass == "GATED" and "HARD-PIN" not in gate:
            out.append(f"RT27-INPUTS {path} is classed GATED and its gate string "
                       f"is {gate!r}; a GATED row must carry the artifact's own "
                       f"hard-pin gate")
        if klass == "ADVANCING" and "NOT-GATED" not in gate:
            out.append(f"RT27-INPUTS {path} is classed ADVANCING and its gate "
                       f"string is {gate!r}")

    for path, expected in GATED_PINS.items():
        if path not in declared:
            out.append(f"RT27-INPUTS this instrument GATES {path} and the "
                       f"artifact records no such input, so the gate rests on "
                       f"this file's transcription rather than on the artifact's "
                       f"classification")
        elif declared[path][0] != "GATED":
            out.append(f"RT27-INPUTS {path} is GATED here and "
                       f"{declared[path][0]!r} in the artifact")
        elif declared[path][2] != expected:
            out.append(f"RT27-INPUTS {path}: the artifact records "
                       f"{declared[path][2]} and this instrument gates "
                       f"{expected}")
    for path, expected in ADVANCING_PINS.items():
        if path not in declared:
            out.append(f"RT27-INPUTS this instrument classes {path} ADVANCING "
                       f"and the artifact records no such input")
        elif declared[path][0] != "ADVANCING":
            out.append(f"RT27-INPUTS {path} is ADVANCING here and "
                       f"{declared[path][0]!r} in the artifact")
        elif declared[path][2] != expected:
            out.append(f"RT27-INPUTS {path}: the artifact records "
                       f"{declared[path][2]} and this instrument's ADVANCING "
                       f"baseline is {expected}. The baseline is what a drift "
                       f"notice prints against; replacing it with today's value "
                       f"erases the record rather than checking it")
    for path in declared:
        if path not in GATED_PINS and path not in ADVANCING_PINS:
            out.append(f"RT27-INPUTS the artifact records {path} and this "
                       f"instrument neither gates it nor classes it advancing, "
                       f"so an input the artifact depends on is unguarded here")

    # the published cardinalities
    gated = sum(1 for v in declared.values() if v[0] == "GATED")
    advancing = sum(1 for v in declared.values() if v[0] == "ADVANCING")
    for name, measured in (("digestsRecordedCount", len(recorded)),
                           ("gatedCount", gated),
                           ("advancingCount", advancing),
                           ("destroyedCount", len(block.get("destroyed") or []))):
        value = block.get(name)
        if exact_int(value) and value != measured:
            out.append(f"RT27-INPUTS {name} declares {value} and the recorded "
                       f"rows measure {measured}")

    # the destroyed row, and its unrecoverability, which is a claim about GIT
    for row in (block.get("destroyed") or []):
        if row.get("destroyedSha256") != DESTROYED_DIGEST:
            out.append(f"RT27-INPUTS the artifact records a destroyed digest "
                       f"{row.get('destroyedSha256')} and this instrument "
                       f"refuses {DESTROYED_DIGEST}")
        if row.get("path") != DESTROYED_PATH:
            out.append(f"RT27-INPUTS the destroyed pin names "
                       f"{row.get('path')!r}, not {DESTROYED_PATH!r}")
    if DESTROYED_DIGEST in {v[2] for v in declared.values()}:
        out.append("RT27-INPUTS a LIVE recorded digest equals the destroyed one, "
                   "so a pin that can never be satisfied is being presented as "
                   "one that is")
    return out


def check_identity(delta, resolved, ctx):
    """The delta file's own header, and the resolved document's, each compared to
    what the operations install.  Nothing here asserts that CD-RT-5 is DECIDED or
    anything else: section 7.10's rule is to pin the PROPERTY, not the CURRENT
    VALUE, whenever the value is something the corpus is waiting to change."""
    out = []
    expected_name = SUBJECT[:-len(".json")]
    if delta.get("artifact") != expected_name:
        out.append(f"RT27-RECORD $.artifact is {delta.get('artifact')!r}; this "
                   f"instrument's subject is {expected_name!r}")
    if delta.get("version") != 27 or isinstance(delta.get("version"), bool):
        out.append(f"RT27-RECORD $.version is {delta.get('version')!r}, not the "
                   f"JSON integer 27")
    if resolved.get("artifact") != expected_name:
        out.append(f"RT27-RECORD the RESOLVED document's $.artifact is "
                   f"{resolved.get('artifact')!r}. A successor that leaves the "
                   f"predecessor's name in place is the inherited-self-name half "
                   f"of section 7.3's rider")
    for key in ("status", "claimId", "sealRecommendation", "retainedChecker"):
        if key in delta and key in resolved and not exact_equal(delta[key],
                                                               resolved[key]):
            out.append(f"RT27-RECORD ${key} is {delta[key]!r} in this file and "
                       f"{resolved[key]!r} in the resolved document")
    status = str(delta.get("status") or "")
    if "CANDIDATE-NOT-APPLIED" not in status:
        out.append(f"RT27-RECORD $.status is {status!r}; this artifact is "
                   f"unreviewed at its own head and section 7.1 grades a "
                   f"retained-checker-less candidate DISQUALIFYING FOR "
                   f"APPLICATION. An applied status would be a claim this run "
                   f"cannot support")
    if delta.get("sealRecommendation") != "DO-NOT-SEAL":
        out.append(f"RT27-RECORD $.sealRecommendation is "
                   f"{delta.get('sealRecommendation')!r}, not DO-NOT-SEAL")
    # The binds-nothing block must agree with what this run can observe.
    binds = get_path(delta, "$.bindsNothing") or {}
    if binds.get("filesEdited") not in (0, None):
        out.append(f"RT27-RECORD $.bindsNothing.filesEdited is "
                   f"{binds.get('filesEdited')!r}; a candidate that edits "
                   f"anything is not a candidate")
    # The head named by the corpus must not be claimed to have moved.
    head_claim = str(binds.get("theNamedArchitectureHeadIsUnchanged") or "")
    if head_claim and "retention-tiers.v24" not in head_claim:
        out.append(f"RT27-RECORD $.bindsNothing.theNamedArchitectureHeadIsUnchanged "
                   f"does not name retention-tiers.v24: {head_claim[:120]!r}")
    return out


def check_own_residuals(delta, ctx):
    """Every measured value retention-tiers.v27 publishes about ITSELF, hard
    compared.  Section 7.2.2: a recorded measurement that cannot fail the build
    is prose."""
    out = []
    residuals = get_path(delta, "$.newResidualsOfThisSuccessor") or []
    count = get_path(delta, "$.newResidualCountOfThisSuccessor")
    if exact_int(count) and count != len(residuals):
        out.append(f"RT27-RESIDUAL $.newResidualCountOfThisSuccessor declares "
                   f"{count} and the array holds {len(residuals)}")
    ids = [r.get("id") for r in residuals]
    if len(set(ids)) != len(ids):
        out.append(f"RT27-RESIDUAL residual ids repeat: {ids}")

    # RT27-RES-01's own figures, which are the disqualifying residual itself.
    for residual in residuals:
        measured = residual.get("measuredValues") or {}
        if "vectorsInTheResolvedDocument" in measured:
            for key, live in (
                    ("vectorsInTheResolvedDocument",
                     len(get_path(ctx["resolved"],
                                  "$.partC_retentionBounds.vectors.rows") or [])),
                    ("invariantsInTheResolvedDocument",
                     len(get_path(ctx["resolved"],
                                  "$.partC_retentionBounds.invariants") or []))):
                if exact_int(measured.get(key)) and measured[key] != live:
                    out.append(f"RT27-RESIDUAL {residual.get('id')} declares "
                               f"{key} {measured[key]} and the resolved document "
                               f"holds {live}")
            # The artifact declares 0 vectors and 0 invariants exercised. That is
            # TRUE OF THE ARTIFACT AS PUBLISHED and this instrument does not
            # rewrite it -- but if it ever declares a non-zero, it must name what
            # exercises them.
            for key in ("vectorsMechanicallyExercisedAgainstIt",
                        "invariantsMechanicallyExercisedAgainstIt"):
                if measured.get(key) not in (0, None):
                    out.append(f"RT27-RESIDUAL {residual.get('id')} declares "
                               f"{key} {measured[key]!r} while $.retainedChecker "
                               f"is {ctx['resolved'].get('retainedChecker')!r}")

    # The residuals the predecessor's review left open must all be carried.
    carried = get_path(delta, "$.residualsLeftOpen.fromTheV26IndependentReview") or []
    left = get_path(delta, "$.residualsLeftOpen.countLeftOpen")
    closed = get_path(delta, "$.residualsLeftOpen.countClosed")
    if exact_int(left) and left != len(carried):
        out.append(f"RT27-RESIDUAL countLeftOpen declares {left} and the array "
                   f"holds {len(carried)}")
    if exact_int(closed) and closed != 0:
        out.append(f"RT27-RESIDUAL countClosed declares {closed}; a count-repair "
                   f"successor that closes a residual has re-opened a block a "
                   f"REJECT was issued against and an ACCEPT then granted for")
    for entry in carried:
        if not str(entry.get("status") or "").startswith("OPEN"):
            out.append(f"RT27-RESIDUAL {entry.get('id')} is carried with status "
                       f"{entry.get('status')!r}; a residual is left open by "
                       f"NAMING it, never by relabelling it")
    return out


# ===========================================================================
# SECTION 9 -- ASSEMBLY.
# ===========================================================================

def run_all(delta, resolved, prov, mod, ctx):
    findings = []
    ctx["resolved"] = resolved
    ctx["operations"] = prov["declaration"]["operations"]
    ctx["predecessor"] = prov["parsedPredecessor"]

    stages = (
        ("resolution", lambda: check_resolution(delta, resolved, prov, ctx)),
        ("census", lambda: check_census(delta, resolved, prov, ctx)),
        ("keyLocator", lambda: check_key_locator(delta, resolved, ctx)),
        ("recordedInputs", lambda: check_recorded_inputs(delta, ctx)),
        ("identity", lambda: check_identity(delta, resolved, ctx)),
        ("ownResiduals", lambda: check_own_residuals(delta, ctx)),
        ("consumingGates", lambda: check_consuming_gates(delta, resolved, ctx)),
        ("anchorFolding", lambda: cross_check_folding(ctx)),
    )
    for name, stage in stages:
        try:
            findings.extend(stage())
        except Exception as exc:  # noqa: BLE001
            findings.append(
                f"RT27-DRIVER {name}: could not run ({type(exc).__name__}: "
                f"{exc}); THIS IS A DEFECT IN THE DRIVER OR A SHAPE IT CANNOT "
                f"READ, NOT A MEASURED PROPERTY OF THE ARTIFACT")

    # The generated referent sweep, run against BOTH subjects.
    try:
        pred_rows, pred_findings, pred_strays = referent_sweep(
            ctx["predecessor"], mod_predecessor_of(ctx))
        res_rows, res_findings, res_strays = referent_sweep(
            resolved, ctx["predecessor"])
        ctx["sweep"] = {
            "rowsOverThePredecessor": len(pred_rows),
            "findingsOverThePredecessor": len(pred_findings),
            "rowsOverTheResolvedValue": len(res_rows),
            "findingsOverTheResolvedValue": len(res_findings),
            "straysOverThePredecessor": len(pred_strays),
            "straysOverTheResolvedValue": len(res_strays),
            "predecessorFindings": pred_findings,
        }
        findings.extend(res_findings)
        if not pred_findings:
            findings.append(
                "RT27-SWEEP the generated stale-inherited-figure rule returns "
                "NOTHING against the verified predecessor. The artifact exists "
                "to repair defects of exactly that class; a rule that cannot "
                "reproduce them on the document that had them is not a control, "
                "and its 0 against the resolved value is vacuous")
        if len(res_strays) > len(pred_strays):
            findings.append(
                f"RT27-SWEEP resolving this derivation increases the number of "
                f"boundary-sentence integers explicable by nothing in their own "
                f"row from {len(pred_strays)} to {len(res_strays)}")
    except Exception as exc:  # noqa: BLE001
        findings.append(f"RT27-DRIVER referentSweep: could not run "
                        f"({type(exc).__name__}: {exc}); THE SWEEP DID NOT RUN")

    # The executed closure, and the second implementation that cross-checks it.
    try:
        findings.extend(check_executed_closure(delta, resolved, mod, ctx))
        findings.extend(check_type_sweep(resolved, mod, ctx))
        ref_ctx = ctx.get("referenceContext") or {}
        findings.extend(cross_check_b1(resolved, mod, ref_ctx, ctx))
        findings.extend(cross_check_demotion(resolved, mod, ref_ctx, ctx))
        findings.extend(cross_check_partition(resolved, ctx))
    except mod.PinRefused as exc:
        raise
    except Exception as exc:  # noqa: BLE001
        findings.append(
            f"RT27-DRIVER executedClosure: could not run ({type(exc).__name__}: "
            f"{exc}); THE 20 VECTORS AND 24 INVARIANTS WERE NOT EXERCISED and "
            f"this exit says nothing about them")
    return findings


def mod_predecessor_of(ctx):
    """The predecessor OF THE PREDECESSOR, used only so the generated sweep has a
    stale-figure oracle when it is pointed at v26.  Read from the GATED v25 pin;
    absent, the sweep still runs and its control simply reports nothing, which is
    itself a finding (see RT27-SWEEP above)."""
    path = resolve_input("artifacts/retention-tiers.v25.json")
    if not path.is_file():
        return {}
    return parse_json(path.read_bytes(), "retention-tiers.v25.json")


# ===========================================================================
# SECTION 10 -- THE MUTATION SUITE.
#
# Each mutation must produce a finding carrying THE FAMILY NAMED FOR IT and NOT
# PRESENT IN THE BASE.  A mutation caught only by a different family counts as an
# escape for its own family and is reported as one -- a suite that accepts any
# finding measures that the checker is noisy, not that it is aimed.  Every
# mutation is applied to an IN-MEMORY COPY; nothing on disk is touched.
# ===========================================================================

def _mut(doc, path, value):
    out = copy.deepcopy(doc)
    steps = path_steps(path)
    found, parent = resolve_steps(out, steps[:-1])
    if not found:
        raise KeyError(path)
    parent[steps[-1]] = value
    return out


def _del(doc, path):
    out = copy.deepcopy(doc)
    steps = path_steps(path)
    found, parent = resolve_steps(out, steps[:-1])
    if not found:
        raise KeyError(path)
    del parent[steps[-1]]
    return out


def build_selftest_cases(delta):
    """(id, family, mutated delta) triples.  Every case is an input that is
    WRONG rather than merely EMPTY -- section 7.8's repair, which is what
    separates an instrument that detects deletion from one that detects
    falsehood."""
    cases = []

    def add(cid, family, mutate):
        try:
            cases.append((cid, family, mutate()))
        except Exception as exc:  # noqa: BLE001
            cases.append((cid, family, exc))

    # --- the resolution -----------------------------------------------------
    add("M01-resolved-digest-falsified", "RT27-DERIV-RESOLVED",
        lambda: _mut(delta, "$.derivedFrom.resolvedValue.sha256", "f" * 64))
    add("M02-operation-from-falsified", "RT27-DERIV-FROM",
        lambda: _mut(delta, "$.derivedFrom.operations[5].from", 16))
    add("M03-repair-reverted", "RT27-DELTA",
        lambda: _mut(delta, "$.derivedFrom.operations[5].to", 15))
    add("M04-prose-repair-reverted", "RT27-SWEEP",
        lambda: _mut(delta, "$.derivedFrom.operations[7].to",
                     "0 independent reviews of these bytes. 2 Part B surfaces "
                     "proposed for change against 18 explicitly named as "
                     "unchanged."))
    add("M05-operation-deleted", "RT27-DERIV-EXACTLY",
        lambda: _mut(delta, "$.derivedFrom.operations",
                     delta["derivedFrom"]["operations"][:-1]))
    add("M06-operation-type-changed", "RT27-DERIV-TYPE",
        lambda: _mut(delta, "$.derivedFrom.operations[1].to", "27"))
    add("M07-operation-class-erased", "RT27-DERIV-CLASSES",
        lambda: _mut(delta, "$.derivedFrom.operations[0].class", "REPAIR"))
    add("M08-predecessor-digest-falsified", "RT27-DERIV-NO-PREDECESSOR",
        lambda: _mut(delta, "$.derivedFrom.predecessorSha256", "0" * 64))
    add("M09-canonical-digest-falsified", "RT27-DERIV-CANONICAL",
        lambda: _mut(delta, "$.derivedFrom.predecessorCanonicalValueSha256",
                     "1" * 64))
    add("M10-empty-operation-list", "RT27-DERIV-EMPTY-OPERATIONS",
        lambda: _mut(delta, "$.derivedFrom.operations", []))
    # Shape-based discovery deliberately survives this rename; what becomes
    # false is the artifact's published top-level key partition.
    add("M11-declaration-block-renamed", "RT27-KEYLOC",
        lambda: {("aBlockNamedSomethingElse" if k == "derivedFrom" else k): v
                 for k, v in delta.items()})

    # --- the census ---------------------------------------------------------
    add("M12-resolved-census-falsified", "RT27-CENSUS",
        lambda: _mut(delta, "$.derivedFrom.resolvedDocumentCensus."
                            "scalarLeafPositions", 2934))
    add("M13-own-census-falsified", "RT27-CENSUS",
        lambda: _mut(delta, "$.leafCensusOfThisDeltaFile.boolLeafPositions", 159))
    add("M14-own-census-arithmetic-falsified", "RT27-CENSUS",
        lambda: _mut(delta, "$.leafCensusOfThisDeltaFile.arithmetic",
                     "574 + 160 + 0 + 3 = 738 non-string, and 738 + 1074 = 1812."))
    add("M15-float-path-list-falsified", "RT27-CENSUS",
        lambda: _mut(delta, "$.leafCensusOfThisDeltaFile.nullLeafPaths", []))

    # --- the keyLocator -----------------------------------------------------
    add("M16-delta-only-key-is-not", "RT27-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.deltaOnlyKeys",
                     list(delta["keyLocator"]["deltaOnlyKeys"]) + ["leafCensus"]))
    add("M17-resolved-only-key-is-here", "RT27-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.resolvedOnlyKeys",
                     list(delta["keyLocator"]["resolvedOnlyKeys"]) + ["keyLocator"]))
    add("M18-key-count-falsified", "RT27-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.resolvedDocumentTopLevelKeyCount", 40))
    add("M19-partition-not-total", "RT27-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.deltaOnlyKeys",
                     [k for k in delta["keyLocator"]["deltaOnlyKeys"]
                      if k != "authorityBoundary"]))
    add("M20-operation-target-mismatch", "RT27-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.operationTargetKeys",
                     ["artifact", "version"]))

    # --- pin hygiene --------------------------------------------------------
    add("M21-gated-row-demoted", "RT27-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.recorded[0].class",
                     "ADVANCING"))
    add("M22-gated-digest-falsified", "RT27-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.recorded[3].sha256",
                     "a" * 64))
    add("M23-destroyed-pin-erased", "RT27-INPUTS",
        lambda: _mut(delta,
                     "$.recordedInputsOfThisDeltaFile.destroyed[0].destroyedSha256",
                     "b" * 64))
    add("M24-input-count-falsified", "RT27-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.gatedCount", 7))
    add("M25-input-row-removed", "RT27-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.recorded",
                     delta["recordedInputsOfThisDeltaFile"]["recorded"][1:]))

    # --- identity and posture ----------------------------------------------
    add("M26-status-applied", "RT27-RECORD",
        lambda: _mut(delta, "$.status", "APPLIED/SEALED"))
    add("M27-seal-recommended", "RT27-RECORD",
        lambda: _mut(delta, "$.sealRecommendation", "SEAL"))
    add("M28-head-claimed-moved", "RT27-RECORD",
        lambda: _mut(delta, "$.bindsNothing.theNamedArchitectureHeadIsUnchanged",
                     "retention-tiers.v27.json is now the named head."))
    add("M29-files-edited", "RT27-RECORD",
        lambda: _mut(delta, "$.bindsNothing.filesEdited", 3))
    add("M30-version-respelled-as-string", "RT27-RECORD",
        lambda: _mut(delta, "$.version", "27"))

    # --- residual accounting ------------------------------------------------
    add("M31-residual-count-falsified", "RT27-RESIDUAL",
        lambda: _mut(delta, "$.newResidualCountOfThisSuccessor", 5))
    add("M32-residual-relabelled-closed", "RT27-RESIDUAL",
        lambda: _mut(delta,
                     "$.residualsLeftOpen.fromTheV26IndependentReview[0].status",
                     "CLOSED BY THIS SUCCESSOR"))
    add("M33-residual-count-closed-nonzero", "RT27-RESIDUAL",
        lambda: _mut(delta, "$.residualsLeftOpen.countClosed", 2))
    add("M34-vectors-claimed-exercised", "RT27-RESIDUAL",
        lambda: _mut(delta, "$.newResidualsOfThisSuccessor[0].measuredValues."
                            "vectorsMechanicallyExercisedAgainstIt", 20))
    add("M35-vector-population-falsified", "RT27-RESIDUAL",
        lambda: _mut(delta, "$.newResidualsOfThisSuccessor[0].measuredValues."
                            "vectorsInTheResolvedDocument", 19))

    # --- the derived delta gate --------------------------------------------
    add("M36-repair-family-unnamed", "RT27-DELTA",
        lambda: _mut(delta, "$.theDefectRepaired.whoFoundIt."
                            "thePredecessorsOwnRetainedCheckerDID",
                     "nothing found it; the defect was noticed by reading"))
    add("M37-residual-firing-count-wrong", "RT27-DELTA",
        lambda: _mut(delta, "$.residualsLeftOpen.fromTheV26IndependentReview[0]."
                            "alsoFiredBy",
                     "check-retention-custody-v26.py as RT26-N01, once"))
    add("M39-operation-from-deleted", "RT27-DERIV-NO-FROM",
        lambda: _del(delta, "$.derivedFrom.operations[5].from"))
    return cases


def selftest(delta, resolved, prov, mod, base_findings):
    """Every mutation is a WRONG input, not an empty one.  The delta discipline
    is what makes the number meaningful over a base that is not clean: a mutation
    counts only if it produces a finding of its own family that is NOT in the
    base."""
    base = set(base_findings)
    base_families = set(families(base_findings))
    failures = []
    caught = 0
    cases = build_selftest_cases(delta)
    for cid, family, mutated in cases:
        if isinstance(mutated, Exception):
            failures.append(f"{cid}: the mutation itself could not be built "
                            f"({type(mutated).__name__}: {mutated}); this case "
                            f"DID NOT RUN and is not counted as caught")
            continue
        ctx = {"part": "all", "freezeText": prov["freezeText"]}
        try:
            m_resolved, m_prov, m_errors = resolve_subject(mutated)
            if m_resolved is None:
                found = list(m_errors)
            else:
                m_prov["freezeText"] = prov["freezeText"]
                found = run_all(mutated, m_resolved, m_prov, mod, ctx)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{cid}: the run raised {type(exc).__name__}: {exc}; "
                            f"a crash is not a catch")
            continue
        fresh = [f for f in found if f not in base]
        hit = [f for f in fresh if f.startswith(family)]
        if hit:
            caught += 1
        elif fresh:
            failures.append(
                f"{cid}: ESCAPED its own family {family}. It produced "
                f"{len(fresh)} other new finding(s), the first being "
                f"{fresh[0][:150]!r}. A mutation caught by a different family "
                f"measures that this checker is noisy, not that it is aimed")
        else:
            failures.append(
                f"{cid}: ESCAPED ENTIRELY -- {family} did not fire and no other "
                f"family did either. This mutation is admitted")
    return failures, len(cases), caught


# ===========================================================================
# SECTION 11 -- WHAT THIS INSTRUMENT CANNOT CATCH.
# ===========================================================================

WHAT_THIS_CANNOT_CATCH = (
    ("1. A JUDGEMENT stated falsely. Section 7.8's measured boundary: these "
     "instruments bind structure and type, not the truth of content. Every "
     "`why`, `whyNotClosed`, `purpose`, `soIsItAControl` and "
     "`whatWouldMakeThisAnswerFalse` string in this artifact can be replaced by "
     "its own negation with the PATH and TYPE unchanged and this run stays "
     "green. An instrument CAN bind prose that asserts a MEASUREMENT -- by "
     "re-deriving the measurement -- and that is done throughout. Nothing binds "
     "prose that asserts a judgement, because no oracle exists for it."),
    ("2. Whether the three repairs are the RIGHT repairs. This instrument proves "
     "that 19 is len($.recordedInputs.recorded) and that 14 is the Part B "
     "UNCHANGED count. It cannot prove that `recordedInputs` was ever meant to "
     "count that list, or that the boundary sentence was ever meant to restate "
     "that field. The referent map in section 4 is this author's reading of what "
     "each figure is a measurement OF, and a wrong referent produces a confident "
     "wrong answer in both directions."),
    ("3. Whether the executed reference derivation is CORRECT. "
     "check-retention-custody-v26.py is hash-verified and executed under section "
     "7.3, which makes it a runtime input rather than a contract -- but its "
     "20 vectors and 24 invariants encode ONE reading of Part A, Part C and "
     "Part D. This file's second implementation cross-checks the Cap algebra, "
     "the demotion scan, the biconditional and the partition; it does not "
     "re-derive the other twenty invariants. Where the two agree, they agree "
     "about a reading."),
    ("4. Any figure the artifact publishes about ANOTHER artifact that is not "
     "reachable from a pinned input. The generated sweep classifies a "
     "boundary-sentence integer as stale only when the PINNED PREDECESSOR "
     "publishes it at the corresponding sibling path. A stale figure inherited "
     "from further back, or from a document this instrument does not pin, is "
     "reported as an unexplained stray and NOT as a finding. Three such strays "
     "exist in these bytes and all three are true."),
    ("5. That the corpus-effect measurement in $.corpusChecksRun is accurate. "
     "It was taken by its author against an earlier serialisation of the same "
     "file, in a tree that moved during the measurement, and nothing here "
     "re-runs 110 checkers. Its own honest bound is published in the artifact; "
     "this instrument neither confirms nor contradicts it. Note in particular "
     "that check-product-dispositions-v2.py's output is NON-DETERMINISTIC over "
     "an unchanged tree, so no diff of it is an attribution signal."),
    ("6. A coherent lie. Flip an operation's `from` AND the predecessor's value "
     "together and the resolution still verifies -- except that the predecessor "
     "is GATED, so this particular lie costs an exit-2 refusal rather than a "
     "green run. The general form survives: any falsehood consistent across "
     "every position this instrument compares is admitted, and the artifact's "
     "own narrative is the largest such surface."),
    ("7. Whether this artifact SHOULD be applied. It measures that the "
     "derivation resolves, that the repairs are the repairs, and that nothing "
     "else moved. Section 7.1 grades a candidate with no retained checker "
     "DISQUALIFYING FOR APPLICATION, and a companion instrument written after "
     "the fact does not discharge that -- section 7.8: what discharges the "
     "residual is an INDEPENDENT RE-DERIVATION, not more assertions from a "
     "closely related mind."),
)

CAN_I_MAKE_THIS_PASS_ON_A_WRONG_ARTIFACT = (
    ("E1  Rewrite $.theDefectRepaired.whatWasWrong to say the opposite of what "
     "was wrong -- e.g. 'the predecessor declared 19 and the bytes hold 15'. "
     "PATH and TYPE unchanged, the operation list untouched, the resolution "
     "still verifies, exit 0. The delta gate reads only the RT26-* family names "
     "out of that block, so any prose around them is free."),
    ("E2  Replace every `why` on every operation with a fabricated rationale. "
     "Eight strings, all narrative, none compared to anything. Exit 0."),
    ("E3  Rewrite $.instrumentPosition.answer from 'NO' to 'YES' -- claiming the "
     "predecessor's instrument DOES validate v27. Measurably false, and nothing "
     "here reads that field."),
    ("E4  Falsify $.corpusChecksRun wholesale: every per-checker digest, every "
     "exit code, the 110 count, the three tight-cycle results. This instrument "
     "runs no checker sweep, so all of it is free. This is the largest single "
     "unbound surface in the artifact, at several hundred leaves."),
    ("E5  Rewrite the five `whyNotClosed` strings so each names a different and "
     "false reason for leaving its residual open. The ids and the `alsoFiredBy` "
     "family names are gated; the reasons are not."),
    ("E6  Falsify $.staleMeasurementSweep's 69 published rows -- their "
     "`howRecomputed` prose, their `kind` labels, and the counts 69/66/3 -- "
     "while leaving the three mismatchPaths correct. This instrument GENERATES "
     "its own sweep and never re-executes the artifact's published rows, so a "
     "fabricated row table passes. THIS IS THE SHARPEST ONE and it is "
     "self-directed: the artifact's own headline evidence for its second repair "
     "is the block this instrument does not read."),
    ("E7  Rewrite $.inheritedMeasurementDisposition.theInheritedRecordedInputs"
     "Digests[].liveAtThisAuthoring for the 17 unchanged rows. They are "
     "digest-shaped strings compared to nothing here; only the delta file's own "
     "$.recordedInputsOfThisDeltaFile rows are gated."),
    ("E8  Move $.whatIDidNotCheck from seven honest entries to one, or to zero. "
     "A shrinking limitations list is invisible to this run, which is the "
     "failure mode section 7.2.2's rider names -- a disclosure that can go "
     "stale because nothing gates it."),
    ("E9  Rewrite $.theSecondInstanceFoundByTheSweep.theAmbiguityThatWasChecked"
     "AndCLOSED, the three-measurement argument that 14 rather than 18 is the "
     "right referent. The CONCLUSION is gated -- the generated sweep re-derives "
     "14 independently -- but the ARGUMENT is free, and a reader persuaded by a "
     "false argument to a true conclusion has been misled about the method."),
    ("E10 Falsify $.authorityBoundary: claim 3 product decisions made and 2 "
     "statuses changed. Nothing here reads that block, and no instrument in the "
     "corpus reads it either."),
    ("E11 Replace $.derivedFrom.whyADerivationAndNotAStandalone entirely -- "
     "including `theSizeArgument`'s 297835 bytes and 2935 leaves. The 2935 is "
     "re-derived elsewhere in this run and would be caught; the byte figure and "
     "the whole argument are not."),
    ("E12 Rewrite $.keyLocator.warningToAReader, which is the artifact's own "
     "statement of the CMP-IR-01 hazard. The six verification directions beside "
     "it are executed; the sentence explaining why is not."),
    ("E13 Fabricate $.corpusChecksRun.whatThisBlockMeasuresAndWhatItCANNOT."
     "andTheBoundWasThenTESTEDRatherThanAsserted -- the two-serialisation "
     "experiment, its digests and its 46327-byte figure. It is the artifact's "
     "strongest single piece of self-evidence and nothing re-runs it."),
    ("E14 Substitute a plausible different authority in any narrative mention of "
     "CD-RT-5's attribution inside the DELTA file. The executed reference "
     "re-extracts the nine quoted decision fields from the LIVE packet in the "
     "RESOLVED document, so the resolved-side quotations are gated -- but the "
     "delta file's own prose about them is not."),
)


def print_limits() -> None:
    print("check-retention-custody-v27.py -- WHAT THIS INSTRUMENT CANNOT CATCH")
    print()
    print("Section 7.8 asks the operative question directly: CAN I MAKE THIS")
    print("CHECKER PASS ON A WRONG ARTIFACT?  The honest answer is YES, and the")
    print(f"count is {len(CAN_I_MAKE_THIS_PASS_ON_A_WRONG_ARTIFACT)}, each with a")
    print("worked example below.  Every one has the same shape section 7.8")
    print("measured on the C-2 instrument: a string leaf whose VALUE is false")
    print("while its PATH and TYPE are unchanged.")
    print()
    for line in CAN_I_MAKE_THIS_PASS_ON_A_WRONG_ARTIFACT:
        print(f"  {line}")
        print()
    print("THE STRUCTURAL LIMITS:")
    print()
    for line in WHAT_THIS_CANNOT_CATCH:
        print(f"  {line}")
        print()
    print("AND THE BOUND ON THE WHOLE EXERCISE.  This file was written after")
    print("reading retention-tiers.v27.json and after reading the freeze")
    print("sections it cites, by a lane that did not author the artifact.  That")
    print("makes it a second reading rather than a second opinion from the same")
    print("mind, and section 7.8's bound still holds in its stronger form: a")
    print("green run is AUTHOR-SIDE EVIDENCE.  What discharges the residual")
    print("section 7.1 grades DISQUALIFYING is an independent re-derivation, not")
    print("another instrument from a closely related mind.")


# ===========================================================================
# SECTION 12 -- MAIN.
# ===========================================================================

def _banner(part, notices, ctx):
    census_r = ctx.get("resolvedCensus") or {}
    census_d = ctx.get("deltaCensus") or {}
    vec = ctx.get("vectorReport") or {}
    inv = ctx.get("invariantReport") or {}
    b1 = ctx.get("b1") or {}
    sweep = ctx.get("sweep") or {}
    tsweep = ctx.get("typeSweep") or {}
    tcounts = ctx.get("typeCounts") or {}
    verb = ctx.get("verbatim") or {}
    print(f"RETENTION-CUSTODY v27  part={part}  gated pins {len(GATED_PINS)}  "
          f"advancing {len(ADVANCING_PINS)}  destroyed 1  drift notices "
          f"{len(notices)}")
    print(f"  DERIVATION RESOLVED: predecessor "
          f"{str(ctx.get('predecessorName'))} byte "
          f"{str(ctx.get('predecessorDigest'))[:16]}..., canonical value "
          f"{str(ctx.get('predecessorCanonical'))[:16]}...; "
          f"{len(ctx.get('operations') or [])} operations "
          f"({len((ctx.get('operationClasses') or {}).get('IDENTITY', []))} "
          f"IDENTITY, "
          f"{len((ctx.get('operationClasses') or {}).get('REPAIR', []))} REPAIR) "
          f"-> resolved value {str(ctx.get('resolvedDigest'))[:16]}...")
    print(f"  resolution is EXACTLY the operations: "
          f"{len(ctx.get('differingLeafPaths') or [])} differing leaf path(s) "
          f"against {len(ctx.get('operations') or [])} operation path(s)")
    print(f"  census: resolved {census_r.get('scalarLeafPositions')} scalar "
          f"leaves ({census_r.get('intLeafPositions')} int / "
          f"{census_r.get('boolLeafPositions')} bool / "
          f"{census_r.get('floatLeafPositions')} float / "
          f"{census_r.get('nullLeafPositions')} null / "
          f"{census_r.get('stringLeafPositions')} string); delta file "
          f"{census_d.get('scalarLeafPositions')}; inherited $.leafCensus "
          f"re-walked and exact")
    print(f"  keyLocator: {ctx.get('keyLocatorDirections', 0)} directions "
          f"executed over a claimed PARTITION, both sides")
    print(f"  ASSERTED OVER THE RESOLVED VALUE, NOT THE DELTA BYTES:")
    print(f"    vectors {vec.get('executed', 0)}/{vec.get('declared', 0)} "
          f"executed, {vec.get('controlsRun', 0)} rejected readings run, "
          f"{len(vec.get('controlsVacuous') or [])} vacuous; invariants "
          f"{inv.get('executed', 0)}/{inv.get('declared', 0)} executed")
    print(f"    B1: {len(b1.get('publishedAgree') or [])}/"
          f"{b1.get('arithmeticRows', 0)} arithmetic rows agree under the "
          f"PUBLISHED expressions, {len(b1.get('v25Agree') or [])}/"
          f"{b1.get('arithmeticRows', 0)} under the PREDECESSOR's; default "
          f"0/0/0 evicts nothing across {b1.get('defaultConfigSizesSwept', 0)} "
          f"sizes ({len(b1.get('defaultConfigNonZeroV25') or [])} of those "
          f"evict under the "
          f"predecessor's); {len(b1.get('crossDimensionSymbols') or [])} "
          f"cross-dimension symbols; "
          f"{b1.get('prefixInclusionViolations', 0)} prefix-inclusion "
          f"violations over {b1.get('prefixConfigurations', 0)} configurations")
    print(f"    law 14: {ctx.get('xcheckDurableCells')} "
          f"DURABLE_AUTHORITATIVE cells and {ctx.get('xcheckOutcomes')} "
          f"outcomes scanned, {ctx.get('xcheckDemotionViolations')} reachable "
          f"silent demotion(s); d9Axes biconditional "
          f"{(ctx.get('xcheckBiconditional') or {}).get('rows')} rows, "
          f"{(ctx.get('xcheckBiconditional') or {}).get('deviations')} "
          f"deviations")
    print(f"    partition {(ctx.get('partition') or {}).get('total')} keys "
          f"({(ctx.get('partition') or {}).get('partA')} Part A + "
          f"{(ctx.get('partition') or {}).get('partB')} Part B)")
    print(f"    quotations: {verb.get('verbatimVerified')} of "
          f"{verb.get('verbatimStringKeys')} string-valued *Verbatim keys "
          f"verified against the source each field's own NAME attributes it to; "
          f"{verb.get('verbatimFalseAbsent')} of "
          f"{verb.get('verbatimSourceAttributed')} would read FALSE-ABSENT under "
          f"a raw byte-literal search and "
          f"{verb.get('verbatimFalseAbsentNormalised')} under a "
          f"whitespace-normalised one, so section 7.7 folding is load-bearing")
    print(f"    type sweep (law 18): {tsweep.get('respellingsAttempted')} "
          f"respellings attempted, {tsweep.get('respellingsAdmitted')} admitted; "
          f"{tcounts.get('guardedIntOrBoolLeafPositions')} guarded int/bool "
          f"positions, {tcounts.get('unruledIntOrBoolLeafPositions')} unruled")
    print(f"  SECOND IMPLEMENTATION: Cap algebra agrees on "
          f"{(ctx.get('xcheckB1') or {}).get('agreed')} rows, disagrees on "
          f"{(ctx.get('xcheckB1') or {}).get('disagreed')}; default 0/0/0 evicts "
          f"at {ctx.get('xcheckDefaultNonZero')} of 201 sizes independently")
    print(f"  GENERATED referent sweep (no repaired path is written into this "
          f"file): {sweep.get('findingsOverThePredecessor')} stale inherited "
          f"restatement(s) over the VERIFIED PREDECESSOR, "
          f"{sweep.get('findingsOverTheResolvedValue')} over the RESOLVED value, "
          f"across {sweep.get('rowsOverTheResolvedValue')} rows; "
          f"{sweep.get('straysOverTheResolvedValue')} unexplained stray(s), "
          f"reported and not counted as verified")
    print(f"  DERIVED delta gate: families the artifact claims repaired "
          f"{ctx.get('familiesClaimedRepaired')} -> "
          f"{[f for f in (ctx.get('familiesClaimedRepaired') or []) if (ctx.get('resolvedFamilies') or {}).get(f)]} "
          f"still firing; families it declares still open "
          f"{sorted((ctx.get('familiesClaimedStillOpen') or {}))}; "
          f"{len(ctx.get('closureRemoved') or [])} finding(s) removed and "
          f"{len(ctx.get('closureAdded') or [])} added by resolving, all "
          f"explained")
    print(f"  freeze anchors {(ctx.get('anchorFolding') or {}).get('folded')}/"
          f"{(ctx.get('anchorFolding') or {}).get('total')} under section 7.7 "
          f"folding ({(ctx.get('anchorFolding') or {}).get('raw')} under a raw "
          f"search); CD-RT-5 read live, not pinned: status "
          f"{ctx.get('cdRt5', (None, None))[0]!r}, "
          f"{ctx.get('cdRt5', (None, None))[1]} quoted decision fields "
          f"re-extracted from the live packet")
    for line in notices:
        print(f"  {line}")
    for line in (ctx.get("gateNotices") or []):
        print(f"  {line}")
    for line in (ctx.get("referenceNotices") or []):
        print(f"  [executed closure] {line}")
    print("  a green run is author-side evidence only; run --limits for what "
          "this instrument cannot catch and for the count of ways it can be "
          "made to pass on a wrong artifact")


def main() -> int:
    argv = sys.argv[1:]
    part = "all"
    do_selftest = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--selftest":
            do_selftest = True
        elif arg == "--limits":
            print_limits()
            return 0
        elif arg == "--part":
            index += 1
            if index >= len(argv) or argv[index] not in ("a", "c", "d", "all"):
                sys.stderr.write("RT27-UNSUPPORTED-INVOCATION: --part takes a, "
                                 "c, d or all. THE CHECK DID NOT RUN.\n")
                return 2
            part = argv[index]
        elif arg.startswith("--part="):
            part = arg.split("=", 1)[1]
            if part not in ("a", "c", "d", "all"):
                sys.stderr.write("RT27-UNSUPPORTED-INVOCATION: --part takes a, "
                                 "c, d or all. THE CHECK DID NOT RUN.\n")
                return 2
        else:
            sys.stderr.write(f"RT27-UNSUPPORTED-INVOCATION: unknown option "
                             f"{arg!r}. THE CHECK DID NOT RUN.\n")
            return 2
        index += 1

    before = measure_all_inputs()

    try:
        snaps, notices = verified_inputs()
    except PinRefused as exc:
        sys.stderr.write(f"{exc}\n")
        sys.stderr.write(
            "RT27-PIN-REFUSED: the verified execution closure did not match its "
            "pinned digests, so NOTHING WAS PARSED OR EXECUTED and THE CHECK DID "
            f"NOT RUN. This exit says nothing whatever about {SUBJECT}, and in "
            "particular says nothing about its 20 vectors or its 24 invariants. "
            "Repair is a successor instrument, never an edit to these bytes.\n")
        return 2

    subject_path = resolve_input(f"artifacts/{SUBJECT}")
    if not subject_path.is_file():
        sys.stderr.write(f"RT27-INPUT-MISSING {SUBJECT}: the subject is not "
                         f"present beside this instrument. THE CHECK DID NOT "
                         f"RUN.\n")
        return 2
    subject_bytes = subject_path.read_bytes()
    live_subject = sha_bytes(subject_bytes)
    if live_subject != SUBJECT_SHA256:
        notices.append(
            f"RT27-SUBJECT-MOVED {SUBJECT}: dispatched at "
            f"{SUBJECT_SHA256[:16]}..., {SUBJECT_BYTES} bytes; live "
            f"{live_subject[:16]}..., {len(subject_bytes)} bytes. This "
            f"instrument REPORTS rather than refuses, because refusing to parse "
            f"would hide every other finding behind one line -- but section 7.2 "
            f"says a change to reviewed bytes requires a version bump and a new "
            f"verdict and may never be made in place.")

    try:
        delta = parse_json(subject_bytes, SUBJECT)
    except PinRefused as exc:
        sys.stderr.write(f"RT27-PARSE-REFUSED: {exc}. THE CHECK DID NOT RUN.\n")
        return 2
    if not isinstance(delta, dict):
        sys.stderr.write("RT27-PARSE-REFUSED: the subject is not a JSON object. "
                         "THE CHECK DID NOT RUN.\n")
        return 2

    try:
        mod = load_v26_module(snaps["artifacts/check-retention-custody-v26.py"])
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(
            f"RT27-CLOSURE-REFUSED: the hash-verified reference derivation "
            f"{V26_CHECKER} did not load ({type(exc).__name__}: {exc}). THE "
            f"CHECK DID NOT RUN and the 20 vectors and 24 invariants were NOT "
            f"exercised.\n")
        return 2

    resolved, prov, errors = resolve_subject(delta)
    prov = prov or {}
    prov["freezeText"] = snaps["IMPLEMENTATION-FREEZE.md"].decode(
        "utf-8", "replace")
    if resolved is None:
        print("RT27-DERIVATION-UNRESOLVED: this subject declares a derivation "
              "and it could not be materialised. NO PROPERTY OF THE RESOLVED "
              "DOCUMENT WAS CHECKED -- not one of its 20 vectors, not one of its "
              "24 invariants. Asserting over the delta bytes instead is exactly "
              "the defect IMPLEMENTATION-FREEZE.md section 7.3's 2026-08-06 "
              "rider forbids, and this instrument will not do it.")
        for error in errors:
            print(f"  - {error}")
        return 1

    ctx = {"part": part, "freezeText": prov["freezeText"],
           "predecessorName": prov.get("predecessor"),
           "predecessorDigest": prov.get("predecessorByteDigest"),
           "predecessorCanonical": prov.get("predecessorCanonicalDigest")}

    try:
        findings = run_all(delta, resolved, prov, mod, ctx)
    except mod.PinRefused as exc:
        sys.stderr.write(
            f"RT27-CLOSURE-REFUSED: the executed reference derivation refused "
            f"its own pinned closure ({exc}). THE CHECK DID NOT RUN; the 20 "
            f"vectors and 24 invariants were NOT exercised and this exit says "
            f"nothing about them.\n")
        return 2

    if do_selftest:
        dirty = bool(findings) or bool(notices)
        if dirty:
            print("SELFTEST-OVER-DIRTY-BASE: the base is NOT clean, so this run "
                  "certifies nothing and cannot return 0. The suite is executed "
                  "under delta discipline -- every mutation must produce a "
                  "finding of its own family NOT PRESENT IN THE BASE -- and the "
                  "number below is reported, not attested.")
            for line in notices:
                print(f"  base notice: {line[:160]}")
            for finding in findings:
                print(f"  base finding: {finding[:220]}")
        failures, cases, caught = selftest(delta, resolved, prov, mod, findings)
        print(f"RETENTION-CUSTODY v27 SELFTEST"
              f"{' (dirty base)' if dirty else ''}: {caught}/{cases} mutations "
              f"caught by their own named family")
        for failure in failures:
            print(f"  - {failure}")
        if dirty:
            print(f"SELFTEST-NOT-CERTIFYING ({len(findings)} base finding(s), "
                  f"{len(notices)} drift notice(s))")
            return 3
        if failures:
            print("SELFTEST-FAIL")
            return 1
        print("SELFTEST-PASS")
        return 0

    # Section 7.2.1 under concurrency: re-measure every input and report anything
    # that moved DURING the run.  A finding produced against a file that was
    # being rewritten underneath the measurement is not a fact about the subject.
    after = measure_all_inputs()
    moved = sorted(name for name in before
                   if before.get(name) != after.get(name))
    if moved:
        notices.append(
            f"RT27-TREE-MOVED {len(moved)} declared input(s) changed digest "
            f"DURING this run: {moved}. Every finding below is UNSAFE TO "
            f"ATTRIBUTE -- the tree moved under the measurement, which is the "
            f"section 7.2.1 concurrency hazard, and the correct response is to "
            f"re-run over a quiescent tree rather than to read this output.")

    _banner(part, notices, ctx)

    if findings:
        print(f"{len(findings)} finding(s) in the RESOLVED value of {SUBJECT}:")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"{SUBJECT}: PASS over its RESOLVED VALUE "
          f"{str(ctx.get('resolvedDigest'))[:16]}... (architecture-candidate "
          f"scope; CANDIDATE-NOT-APPLIED; the artifact's own $.retainedChecker "
          f"remains NONE and this file does not change it; RT27-RES-01's "
          f"measured half is narrowed, not closed -- section 7.1 still grades "
          f"the residual DISQUALIFYING FOR APPLICATION and a companion "
          f"instrument does not discharge it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
