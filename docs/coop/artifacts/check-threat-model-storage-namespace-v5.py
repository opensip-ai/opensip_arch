#!/usr/bin/env python3
"""Bind the MEANING of `storageNamespace.rootBinding` in the reviewed candidate
`artifacts/threat-model-storage-namespace.v4.json`, over the EFFECTIVE contract
its derivation materialises against the pinned predecessor.

WHY THIS FILE EXISTS
--------------------
`check-threat-model-storage-namespace-v4.py` was reviewed
`ACCEPT_WITH_BLOCKERS` at `CIR-B2`
(`artifacts/companion-instruments.review-independent.v1.json`).  That review
pins those bytes, and IMPLEMENTATION-FREEZE.md §7.2 forbids editing them, so
this is a SUCCESSOR INSTRUMENT and the predecessor is left byte-identical.  The
subject artifact is unchanged and is not re-litigated: it was independently
reviewed ACCEPT at 0 blockers and its live prose says what it should.

`CIR-B2`, measured by the reviewer and REPRODUCED here from an external driver:

    `require_substrings` tests `needle not in text` with no negation detection.
    13 of 13 hand-written substring-preserving negations escaped.  A sweep of
    the 280 prose leaves of `$.storageNamespace` longer than 25 characters found
    63 positions bound by containment yet defeated by keeping every needle and
    appending a reversal -- including all five property statements,
    `observabilityBoundary.rule` and `fixtures.enforcementDisclosure`.  The
    sharpest form: the predecessor's own `_paper_seal_the_disclosure` mutation
    catches the LAZY forgery (text replaced) and misses the CAREFUL one (text
    kept, contradiction appended).

    And 3 of 3 lawful, meaning-preserving rewordings were REJECTED (`FP-01`).
    Containment is brittle in both directions.

The corpus had already measured this class.  `versioning-policy.v10.json`
publishes the quantified boundary for exactly this technique at
`successorRevision.evidenceEnforcementRepair.retainedResiduals[0].measured` --
*"appending a false sentence while preserving every required measured substring
is admitted at 80 of them"* -- and grades every bound leaf MEASURED / GROUNDED /
UNMEASURABLE, naming the exact paths of each class rather than summarising.
That grading vocabulary is adopted here.  A defect the corpus has already
measured is an uncollected one, not a new one.

WHAT THIS INSTRUMENT DOES THAT THE PREDECESSOR DID NOT
------------------------------------------------------
Containment cannot close `CIR-B2`, because containment is monotone: adding text
can never remove a needle.  Four mechanisms are added, in increasing strength,
and each is measured rather than asserted.

  1. STANCE.  Prose is split into CLAUSES and each clause is classified NEG or
     POS by a closed marker lexicon.  A claim declares the stance its terms must
     carry.  A clause anywhere in the same property that carries the OPPOSING
     stance over the same terms is a finding at that clause.  Appending
     "and mount points within that scope are tolerated" to `SN-P3.statement` no
     longer survives, because the appended clause is POS over `mount point`
     while the property forbids it.  This is a LEXICAL FLOOR, not a solution,
     and its residual is measured and published every run (`SNV5-B`).

  2. RELATION.  `SN-P4`'s ordering is extracted as a RELATION over terms --
     `record < namespace` -- from arrow chains, `precedes`, `before`,
     `only after`, `first/afterwards`.  The relation must be acyclic and must
     entail the order the reference model requires.  Inverting the ordering
     while keeping every needle makes the relation cyclic.  This binds
     STRUCTURE, not words: any phrasing that yields the same relation passes.

  3. ATTACHMENT.  Which authority-record field is DISPOSITIVE is not read from
     the prose and not transcribed.  It is MEASURED from the reference decider
     by a discrimination experiment -- perturb one field with the reached root
     held fixed and see whether the outcome moves -- and the prose's attachment
     of the words `dispositive` and `advisory` must agree with the measurement.

  4. MEASUREMENT.  Claims that are facts about disk are MEASURED there:
     `fixtures.enforcementDisclosure`'s claim that `check-threat-claims.py` does
     not enforce these vectors is decided by reading that file;
     `observabilityBoundary`'s G14 claim is decided against the live
     `$.assurance` block; every one of the 10 `verifiedInputs` digests is
     re-measured against disk and the DRIFT SET must equal the set the
     artifact's own `driftNote` names; all three predecessor subtree
     serialisations are re-derived byte-exactly.

FALSE POSITIVES, THE OTHER DIRECTION
------------------------------------
A claim is satisfied by EITHER its literal anchor (so every one of the
predecessor's ~70 needles keeps its absence coverage) OR a clause that carries
its normalised TERMS in the declared stance.  All three of `FP-01`'s lawful
rewordings pass by the second path.  The selftest carries them as CONTROLS that
must produce ZERO findings, so a successor that improves the prose of a bound
position is not forced to fail.

CONSTANTS ARE RE-DERIVED, NOT TRANSCRIBED
-----------------------------------------
`check-delivery-v4.py` was faulted for hand-typed census constants, so it tested
its own transcription.  Here: the closed outcome vocabulary is DERIVED as the
refusal set of a decider written from the reviewed semantics; recovery row
counts come from `len()`; the authority-record path is bound by structural
predicates rather than by an equality against a transcribed literal; every
recorded digest is re-measured; and the `CIR-B2` figures this file publishes are
read as data from the review artifact AND independently re-measured, then
hard-compared (§7.2.2).

WHAT IT ASSERTS
---------------
  SNV5-A0  duplicate JSON keys, NAMED with key and path            (freeze 7.5)
  SNV5-D   the derivation resolves, and resolves to what it claims (freeze 7.3)
  SNV5-S   scope: 1 addition, 0 removals, 12 changed prose leaves, every
           predecessor list byte-identical, purge subtree untouched
  SNV5-T   exact-type admission at every closed scalar           (freeze 6/18)
  SNV5-U   resolution is UNARY -- the resolver here HAS NO ROOT PARAMETER --
           and every admission path outside it is named and closed
  SNV5-P1..P5  each property bound by CLAIMS: anchor or terms, plus stance
  SNV5-M   MEANING: stance conflicts, ordering relations, dispositive
           attachment, frame negation
  SNV5-E   claims about disk, MEASURED on disk
  SNV5-W   every recorded measurement re-derived and hard-compared
  SNV5-G   published corpora are NON-DEGENERATE where distinctness is claimed
  SNV5-X   outcomes: vocabulary re-derived from the decider's refusal set,
           every value reachable, distinct, defined, zero D9 vocabulary minted
  SNV5-V   every declared vector agrees with the decider
  SNV5-R   rename operand pairs RE-DERIVED from `layout` and the state machines
  SNV5-C   both recovery tables' closure, counted with len()
  SNV5-N   non-interference with freeze 4.6's purge discharge, measured
  SNV5-K   the `checkerImpact` coverage map is live
  SNV5-B   the instrument's OWN residual negation hole, measured every run
           against the same 280-leaf universe the review used, and BOUNDED

MEASURED AGAINST THESE PINNED BYTES, FROM AN EXTERNAL DRIVER
------------------------------------------------------------
Every figure below was produced by a driver that imports THIS FILE unmodified
via importlib, calls `load_environment()`, mutates deep copies and calls
`check()`.  The instrument was never edited to make a number come out.

  the reviewer's 13 substring-preserving negations   13/13 caught  (v4: 0/13)
  FP-01's 3 lawful meaning-preserving rewordings      0/3 rejected (v4: 3/3)
  sweep of $.storageNamespace prose leaves > 25 chars
      universe                                        280   (v4: 280)
      bound by nothing here                            26   (v4:  41)
      defeated by a needle-preserving appended reversal  0  (v4: 104)
      bound yet defeatable -- the CIR-B2 hole            0  (v4:  63)
  vector `expected` flips                              36, 0 escapes
  vector `violates`/`satisfies` flips                  24, 0 escapes
  operand-pair layout substitutions                    78, 0 escapes

GUTTING, WITH THE DEFINITION STATED -- because the figure is definition-
sensitive and the predecessor's was recorded as if absolute (review CIR-NB-02
swept 24 definitions and got 126 under the first natural one where the record
said 133):

  D1  recursive replacement of every STRING leaf with a placeholder, list
      STRUCTURE preserved, non-string scalars left alone   rootBinding -> 176
  D2  the same, with list ELEMENTS replaced wholesale      rootBinding -> 160
  rootBinding deleted entirely                                             2

  per property, gutted individually, STABLE ACROSS BOTH DEFINITIONS:
      SN-P1 14   SN-P2 18   SN-P3 13   SN-P4 15   SN-P5 15   range 13-18

  Review CIR-NB-01 measured the predecessor at SN-P4=5 and SN-P5=6, a range of
  5-18 rather than the 13-18 the freeze record published, and observed that the
  two thinnest-bound properties are the two that govern crash-time ordering.
  Those two are strengthened HERE and only those two -- every key of SN-P4 and
  SN-P5 now carries claims, including both titles and
  `SN-P5.inventoryAlreadyReportsIt`, which the predecessor left entirely free.
  SN-P1, SN-P2 and SN-P3 are unchanged at 14, 18 and 13, so the narrowing of
  the range is a real change in the weakest pair and not padding elsewhere.

THE RESIDUAL, PUBLISHED AS A MEASUREMENT AND NOT AS A CLAIM
-----------------------------------------------------------
`CIR-B2` is NARROWED, not closed, and here is exactly what remains.  All three
new lexical mechanisms -- stance, frame negation, retraction -- are LEXICAL, so
all three are evadable by an author who knows they exist.  A reversal that

    (a) names none of the terms the claim it reverses is bound by,
    (b) uses no retraction vocabulary, and
    (c) opens with no frame negation

is not detected.  `RESIDUAL_CASES` carries one such reversal for each of the
five properties, `--selftest` runs them, and 5 of 5 escape.  That number is
published as `RESIDUAL_EVASIVE_ESCAPES` and the selftest FAILS if the
measurement and the published figure ever disagree in either direction, so the
disclosure cannot go stale.  26 of the 280 prose leaves are bound by nothing
here at all, and `--residual` names every one of them rather than summarising.

Only the four MEASURED bindings are immune to this class, because they do not
read the sentence at all: the enforcement disclosure, the observability
boundary, the recorded digests and the re-derived subtree serialisations are
decided where their facts live.  Extending that technique is what would close
the rest; nothing lexical will.

WHAT IT DOES NOT DO
-------------------
It changes no status, disposition, verdict or seal, closes no row, repoints no
head and clears no freeze condition.  TM remains `UNSET - BLOCKS FREEZE`;
`CD-RT-5` remains `BLOCKED_ON_PHASE_1A`.  `rootBinding` remains
SPECIFICATION-level: whether a built host honours SN-P1..SN-P5 is a G14-class
runtime question and `rootBinding.observabilityBoundary` says so.

AND IT DOES NOT CLAIM `CIR-B2` IS CLOSED.  It is narrowed and the residual is
published as a measurement, at `SNV5-B`, every run.  See `RESIDUAL_BOUND`.

Usage: python3 artifacts/check-threat-model-storage-namespace-v5.py
           [--selftest] [--residual] [--no-residual]
Exit:  0 clean - 1 findings - 2 missing input or digest drift
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"

# ---------------------------------------------------------------- pinned bytes
#
# freeze 7.2: a version number binds nothing and only a digest does.  Both
# digests below were measured with `shasum -a 256` and hard-compared against the
# value recorded here before this file was committed.  Drift on either is exit
# 2, not a finding: a checker that keeps scoring after its subject moved is
# reporting about bytes nobody asked it about.
SUBJECT_REL = "artifacts/threat-model-storage-namespace.v4.json"
SUBJECT_SHA = "94b68f6d504967b61c9daf4884cad90d2e5de63af3b40aeda99d28b59513b5be"
PREDECESSOR_REL = "artifacts/threat-model.v3.json"
PREDECESSOR_SHA = "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499"

# The review that raised CIR-B2.  Pinned because this instrument re-derives the
# blocker's own figures from it rather than transcribing them, and a figure read
# from moving bytes is not a hard comparison.  It is read as DATA; nothing in it
# is executed and no verdict in it is reopened.
REVIEW_REL = "artifacts/companion-instruments.review-independent.v1.json"
REVIEW_SHA = "86a69f3ec6164f0cdb83fb109ad719ff55983da2d6c565f41abb67f70b1f5a89"

# Environment inputs.  Measured and REPORTED, deliberately NOT pinned.
# `check-completeness.py` is one of the four files freeze 7.6 records as the
# genuinely editable surface of this corpus; pinning it here would break this
# checker the moment somebody lawfully repairs it.  The guard against a wrong
# reader is not a digest, it is SNV5-D/SNV5-S: the resolution must produce
# exactly one addition, zero removals and twelve changed prose leaves, which a
# broken reader cannot fake.
COMPLETENESS_REL = "artifacts/check-completeness.py"
RESOLVED_INPUTS_REL = "artifacts/resolved-inputs.v2.json"
D9_REL = "artifacts/d9-exit-contract.v1.14.json"
RETENTION_TIERS_REL = "artifacts/retention-tiers.v24.json"
RETENTION_CHECKER_REL = "artifacts/check-retention-custody-v24.py"
THREAT_CLAIMS_REL = "artifacts/check-threat-claims.py"
PREDECESSOR_INSTRUMENT_REL = "artifacts/check-threat-model-storage-namespace-v4.py"

MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)
TOTALITY_ROOT_CASES = (
    ("string", "hostile-contract"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)

# Same step grammar as `check-c2-v9.py` `_STEP_RE` and `check-completeness.py`
# `STEP_RE`, so declared pointers are walked the way the corpus walks them.
STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")

PROPERTY_IDS = ("SN-P1", "SN-P2", "SN-P3", "SN-P4", "SN-P5")
RB_PREFIX = "storageNamespace.rootBinding."
NS_PREFIX = "storageNamespace."

# Any of these inside a NORMATIVE position means the rule was bound to an errno.
# The subject deliberately binds to none: measured on a real nested mount, a
# mount can present EXDEV(18), EBUSY(16), or silently succeed while relocating
# the mount -- three behaviours, so naming one would be freeze 6 law 18's
# mistake in another register.  One position is exempt and named below because
# it is an OBSERVATION about rename(2) on a host, not a rule.
ERRNO_RE = re.compile(r"\bEXDEV\b|\bEBUSY\b|\bENOTSUP\b|\bEOPNOTSUPP\b|\bEPERM\b"
                      r"|\bENOSPC\b|\bENOTEMPTY\b|\berrno\b", re.I)
ERRNO_OBSERVATION_EXEMPTION = \
    "rootBinding.renameAtomicity.recoveryTableClosure.measuredRatherThanArgued"


# ====================================================================== 7.5
# The parse primitive.  `json.loads` without an `object_pairs_hook` keeps the
# LAST of a duplicated key, so a candidate can read one way to a human and score
# another way here with the parsed object byte-identical to the honest one.
# freeze 7.5 measured 40 exploitable checkers across this corpus and recorded
# that 6 of the 47 rejecting checkers never say WHICH key was duplicated.  Every
# JSON byte this checker reads enters through `jloads`, which RECORDS each
# repeated key against its own path and reports it as a named finding at that
# position rather than raising.  Carried forward from the predecessor unchanged
# in substance -- review CIR-NB-08 records it as the better of the two patterns
# in this corpus and worth carrying to successors.
_PARSES: dict[str, list[str]] = {}


def _duplicate_paths(node, steps: list, marks: dict, out: list) -> None:
    if isinstance(node, dict):
        for key in marks.get(id(node), []):
            path = "".join(
                f"[{s}]" if isinstance(s, int) else (f".{s}" if steps else s)
                for s in (steps + [key]))
            out.append((path.lstrip("."), key))
        for key, item in node.items():
            _duplicate_paths(item, steps + [key], marks, out)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _duplicate_paths(item, steps + [index], marks, out)


def jloads(text: str, label: str):
    """Parse JSON and report every key the BYTES publish more than once."""
    marks: dict = {}
    keep: list = []

    def pairs(items: list) -> dict:
        out: dict = {}
        repeated: list = []
        for key, value in items:
            if key in out:
                repeated.append(key)
            out[key] = value
        if repeated:
            # `keep` holds a live reference to every object that recorded a
            # duplicate, so no id() in `marks` can be reused by a collected
            # object while the paths are being resolved.
            keep.append(out)
            marks[id(out)] = repeated
        return out

    value = json.loads(text, object_pairs_hook=pairs)
    found: list = []
    if marks:
        _duplicate_paths(value, [], marks, found)
    problems = [
        f"SNV5-A0-DUPKEY {label}: key '{key}' is published more than once at "
        f"{path or '<document root>'}; the host parser keeps the LAST "
        f"occurrence, so the parsed contract cannot say what the bytes say"
        for path, key in found
    ]
    declared = sum(len(v) for v in marks.values())
    if len(found) < declared:
        problems.append(
            f"SNV5-A0-DUPKEY {label}: {declared - len(found)} duplicate key(s) "
            f"sit in an object the parse itself discarded, so this run cannot "
            f"resolve their path; they are refused regardless")
    if len(keep) != len(marks):
        problems.append(
            f"SNV5-A0-DUPKEY {label}: the duplicate-key record and the objects "
            f"it refers to disagree in cardinality")
    _PARSES[label] = problems
    return value


def parse_findings() -> list[str]:
    out: list[str] = []
    for problems in _PARSES.values():
        out.extend(problems)
    return out


# ============================================================ 6, law 18
# Closed-scalar admission is exact-type: the comparison rejects any value whose
# JSON type differs from the declared type BEFORE comparing content.  Python
# makes this a live hazard rather than a theoretical one: `True == 1` and
# `isinstance(True, int)`, so a `schemaVersion` of `true` compares equal to 1
# under every naive test.
_MISSING = object()


def jtype(value) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def scalar(node, key, want_type: str, path: str, findings: list,
           want_value=_MISSING) -> bool:
    """Admit one closed scalar exactly.  Returns True only if it passed."""
    if not isinstance(node, dict) or key not in node:
        findings.append(f"SNV5-T {path}: closed scalar is absent")
        return False
    value = node[key]
    actual = jtype(value)
    if actual != want_type:
        findings.append(
            f"SNV5-T {path}: declared type is {want_type}, bytes publish "
            f"{actual} ({value!r}); freeze 6 law 18 rejects the type before "
            f"the content")
        return False
    if want_value is not _MISSING and value != want_value:
        findings.append(
            f"SNV5-T {path}: expected {want_value!r}, bytes publish {value!r}")
        return False
    return True


# ================================================================== utilities
def resolve_pointer(document, path: str):
    """Walk a dotted/indexed path.  Raises on anything that does not resolve."""
    node = document
    for match in STEP_RE.finditer(path):
        index, name = match.group(1), match.group(2)
        if index is not None:
            node = node[int(index)]
        else:
            node = node[name]
    return node


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def text_of(value) -> str:
    """Flatten a prose position to one string."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(x for x in value if isinstance(x, str))
    if isinstance(value, dict):
        return " ".join(text_of(x) for x in value.values())
    return ""


def blocks_of(value) -> list:
    """Flatten a prose position to a LIST of independent text blocks.

    The predecessor joined a list position into one string, which merged clause
    boundaries across list members.  Keeping them apart matters here because a
    clause is the unit stance is decided over."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list = []
        for item in value:
            out.extend(blocks_of(item))
        return out
    if isinstance(value, dict):
        out = []
        for item in value.values():
            out.extend(blocks_of(item))
        return out
    return []


def _safe(document, path):
    try:
        return resolve_pointer(document, path)
    except MALFORMED_SHAPE_EXCEPTIONS:
        return ""


def _strings(node, path):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _strings(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _strings(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


def _lists(node, path):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _lists(value, f"{path}.{key}")
    elif isinstance(node, list):
        yield path, node
        for index, value in enumerate(node):
            yield from _lists(value, f"{path}[{index}]")


def exact_keys(node, path: str, want: set, family: str, findings: list) -> bool:
    if not isinstance(node, dict):
        findings.append(f"{family} {path}: expected an object, found "
                        f"{jtype(node)}")
        return False
    have = set(node)
    if have != want:
        findings.append(
            f"{family} {path}: key set is not closed/exact; missing "
            f"{sorted(want - have)}, unexpected {sorted(have - want)}")
        return False
    return True


# ===================================================== the normative form
#
# CIR-B2 in one sentence: containment is MONOTONE.  Adding text can never remove
# a needle, so `needle not in text` cannot see a retraction.  The repair is to
# stop treating a position as one opaque string and start treating it as a
# sequence of CLAUSES, each of which carries a stance over the terms it
# mentions.  Then a retraction is not invisible text -- it is a clause whose
# stance opposes the clause the claim was satisfied by.
#
# This is a LEXICAL FLOOR.  It is not a semantics.  An attacker who writes a
# reversal with a negation marker inside the reversing clause defeats it, and
# `SNV5-B` measures exactly how many positions remain defeatable and prints the
# number every run.  What it is NOT is a claim that the hole is closed.

# Clause boundaries.  Sentence terminators always split; a comma splits only
# when the fragment after it opens a new clause, so an enumeration inside one
# clause ("the root itself, projects/, control/, quarantine/ and every
# directory") is NOT torn apart while a coordinated retraction ("..., and in
# that case resolution is not a total function") IS.
_CLAUSE_SPLIT = re.compile(
    r"(?:[.;:!?]+\s+)"
    r"|(?:,\s+(?=(?:and|but|or|so|yet|then|in|which|while|whereas|although|"
    r"though|however|nevertheless|never|no|not|because|since|unless|except)\b))"
    # `X and no Y` coordinates two clauses with no comma between them.  Without
    # this split the negation in the SECOND clause masks the assertion in the
    # FIRST, which is exactly how the enforcement-disclosure paper seal was
    # written: "these vectors ARE enforced ... and no successor work is
    # required" reads NEG as one clause and POS as two.
    r"|(?:\s+and\s+(?=(?:no|not|never|nothing|neither)\b))"
    r"|(?:\s+--\s+)|(?:\s+—\s+)",
    re.I)

# A clause is NEGATIVE if it carries any of these.  The lexicon is closed and is
# reported in the banner, because a stance engine whose lexicon is private is
# just another unverifiable attestation.
_NEG_RE = re.compile(
    r"\b(?:no|not|never|neither|nor|none|nothing|cannot|without|unless|"
    r"absent|zero|forbid|forbids|forbidden|forbidding|refuse|refuses|refused|"
    r"refusal|reject|rejects|rejected|prohibit|prohibits|prohibited|deny|"
    r"denies|denied|fails|failing|impossible|inexpressible|excluded|barred)\b"
    r"|\bn't\b|\bmay\s+not\b|\bmust\s+not\b|\bcan\s+not\b",
    re.I)

# A position whose FIRST clause is one of these frames negates everything after
# it while preserving every substring in it.  This is the cheapest of the 13
# escapes and the cheapest to close.
_FRAME_NEGATION_RE = re.compile(
    r"^\s*(?:it\s+is\s+not\s+the\s+case\s+that\b"
    r"|the\s+following\s+is\s+(?:false|withdrawn|no\s+longer\s+true)\b"
    r"|contrary\s+to\s+(?:the\s+)?(?:above|following)\b"
    r"|none\s+of\s+the\s+following\s+(?:holds|applies)\b"
    r"|disregard\s+the\s+following\b)",
    re.I)

NEG, POS = "NEG", "POS"

# A normative contract does not retract itself.  A clause that refers BACK at
# this text and withdraws, waives, suspends or reverses it is a retraction, and
# a retraction preserves every required substring by construction -- it does not
# touch them, it out-ranks them.  This is the third lexical floor (after stance
# and frame negation) and it is the one that sees a reversal made BY REFERENCE
# rather than by restatement, which is what a generic appended contradiction is.
# Measured against the live contract: 0 occurrences in all 280 prose leaves.
_RETRACTION_RE = re.compile(
    r"(?:the\s+(?:above|preceding|foregoing)"
    r"|this\s+(?:rule|requirement|property|statement|section|clause|sentence))"
    r"[^.;:]{0,80}?"
    r"(?:does\s+not\s+apply|no\s+longer|is\s+withdrawn|are\s+withdrawn"
    r"|is\s+optional|is\s+advisory|is\s+waived|is\s+suspended"
    r"|may\s+be\s+ignored|is\s+superseded|is\s+void|does\s+not\s+bind)"
    r"|(?:the\s+opposite\s+(?:is|applies|holds)"
    r"|the\s+reverse\s+(?:is|applies|holds)"
    r"|disregard\s+the\s+(?:above|preceding|foregoing)"
    r"|notwithstanding\s+the\s+above)",
    re.I)


def normalise(text: str) -> str:
    """Whitespace-normalised, case-folded.  freeze 7.7 records that line
    wrapping manufactures false negatives in this corpus, so every comparison
    this engine makes runs over normalised text and never over raw bytes."""
    return re.sub(r"\s+", " ", text).strip().lower()


def clauses_of(value) -> list:
    """Every clause of a position, normalised, in document order."""
    out: list = []
    for block in blocks_of(value):
        for piece in _CLAUSE_SPLIT.split(block):
            piece = normalise(piece)
            if piece:
                out.append(piece)
    return out


def stance_of(clause: str) -> str:
    return NEG if _NEG_RE.search(clause) else POS


def _matches(clause: str, groups: tuple) -> bool:
    """Every group must contribute at least one surface form.  Groups are
    ALTERNATIONS, so a lawful rewording that swaps one accepted phrasing for
    another still matches -- that is the false-positive half of the repair."""
    return all(any(form in clause for form in group) for group in groups)


class Claim:
    """One load-bearing clause of a normative position.

    `anchor`  the predecessor's literal needle.  Kept verbatim so that every
              absence the predecessor caught is still caught: a gutted position
              loses the anchor AND the terms.
    `terms`   alternation groups over normalised text.  A clause carrying all
              groups in `stance` satisfies the claim even if the anchor is gone,
              which is what lets a lawful rewording through.
    `stance`  NEG or POS.  A clause carrying all groups in the OPPOSING stance
              is a contradiction and is reported at that clause.
    `guard`   whether to run the contradiction scan for this claim.  Claims
              whose terms are too common to discriminate are declared
              `guard=False` and that fact is disclosed, never hidden.
    `scope`   'position' or 'property': how far the contradiction scan reaches.
    """

    __slots__ = ("key", "anchor", "terms", "stance", "guard", "scope",
                 "elsewhere")

    def __init__(self, key, anchor, terms=(), stance=POS, guard=False,
                 scope="property", elsewhere=False):
        self.key = key
        self.anchor = anchor
        self.terms = terms
        self.stance = stance
        self.guard = guard
        self.scope = scope
        # A claim with no anchor is a pure TABOO: it asserts that no clause in
        # scope may carry these terms in the opposing stance.  Nothing has to
        # SAY it, because what it forbids is a sentence, not a silence.
        self.elsewhere = elsewhere or not anchor


def claim_satisfied(claim: Claim, raw_text: str, position_clauses: list) -> str:
    """'literal', 'terms', or '' -- WHICH satisfier fired, so the grade of each
    position can be reported rather than asserted."""
    if claim.anchor and claim.anchor in raw_text:
        return "literal"
    if claim.terms:
        for clause in position_clauses:
            if _matches(clause, claim.terms) and stance_of(clause) == claim.stance:
                return "terms"
    return ""


def contradictions(claim: Claim, scan_clauses: list) -> list:
    """Every clause in scope that carries the claim's terms in the opposing
    stance.  This is the CIR-B2 repair: containment cannot see these because
    every needle is still present."""
    if not claim.guard or not claim.terms:
        return []
    opposing = NEG if claim.stance == POS else POS
    return [c for c in scan_clauses
            if _matches(c, claim.terms) and stance_of(c) == opposing]


def _abbrev(clause: str, width: int = 110) -> str:
    return clause if len(clause) <= width else clause[:width] + "..."


# ---------------------------------------------------------------- relations
#
# The strongest binding here, because it binds STRUCTURE and not words.  An
# ordering claim is extracted as a RELATION over terms and then tested for
# consistency, so any phrasing that yields the same relation passes and any
# phrasing that yields the opposite relation fails -- including one that keeps
# every required substring and appends the inversion.
_ORDER_TERMS = {
    "record": ("generation-1 record", "generation-1 authority record",
               "authority record", "the record", "a record"),
    "namespace": ("projects/<projectid>", "the namespace", "a namespace",
                  "project namespace"),
}
_BEFORE_RE = re.compile(r"\b(?:precedes|is\s+created\s+before|before)\b")
_AFTER_RE = re.compile(r"\b(?:only\s+after|after|follows|afterwards)\b")


def _term_at(clause: str, start: int, end: int) -> str | None:
    """Which ordering term the span [start, end) mentions, longest form first."""
    span = clause[start:end]
    best, best_len = None, 0
    for name, forms in _ORDER_TERMS.items():
        for form in forms:
            if form in span and len(form) > best_len:
                best, best_len = name, len(form)
    return best


def ordering_pairs(value) -> list:
    """Every (earlier, later) pair the prose states, with the clause that states
    it.  Arrow chains, `precedes`/`before`, `after`/`only after`, and
    `first`/`afterwards` are the four forms the subject actually uses."""
    pairs: list = []
    for clause in clauses_of(value):
        # 1. arrow chain:  A -> B -> C
        if "->" in clause:
            segments = [s for s in clause.split("->")]
            named = [(i, _term_at(s, 0, len(s))) for i, s in enumerate(segments)]
            named = [(i, t) for i, t in named if t is not None]
            for (i, a), (j, b) in zip(named, named[1:]):
                if a != b and j > i:
                    pairs.append((a, b, clause))
        # 2/3. an explicit relation word with a term on each side
        for regex, invert in ((_BEFORE_RE, False), (_AFTER_RE, True)):
            for match in regex.finditer(clause):
                left = _term_at(clause, 0, match.start())
                right = _term_at(clause, match.end(), len(clause))
                if left is None or right is None or left == right:
                    continue
                pairs.append((right, left, clause) if invert
                             else (left, right, clause))
        # 4. `X is created first ... Y afterwards`
        first = clause.find(" first")
        if first > 0 and "afterwards" in clause:
            left = _term_at(clause, 0, first)
            right = _term_at(clause, first, len(clause))
            if left and right and left != right:
                pairs.append((left, right, clause))
    return pairs


# --------------------------------------------------------------- attachment
#
# Which authority-record field DECIDES is not read from the prose and is not
# transcribed.  It is measured from the reference decider below by a
# discrimination experiment, and the prose's use of `dispositive` and `advisory`
# must agree with that measurement.
_ATTACH_PREDICATES = ("dispositive", "advisory")


def attachments(node, terms: tuple) -> dict:
    """predicate -> set of terms it attaches to, by NEAREST PRECEDING term
    within the same clause.  `activeRootId is dispositive and
    activeRootCanonicalPath is an advisory locator only` yields
    {dispositive: {activeRootId}, advisory: {activeRootCanonicalPath}}."""
    found: dict = {p: set() for p in _ATTACH_PREDICATES}
    for clause in clauses_of(node):
        for predicate in _ATTACH_PREDICATES:
            for match in re.finditer(re.escape(predicate), clause):
                head = clause[:match.start()]
                best, best_at = None, -1
                for term in terms:
                    at = head.rfind(term.lower())
                    if at > best_at:
                        best, best_at = term, at
                if best is not None and best_at >= 0:
                    found[predicate].add(best)
    return found


# ==================================================== the reference model
#
# The outcomes are DECIDED here, from the properties' semantics as reviewed, and
# the artifact's declared vectors must agree with the decision.  Carried forward
# from the predecessor, which the review graded "the strongest work in either
# instrument -- I attacked it 141 ways and it did not yield once", and extended
# in three ways this file needs:
#
#   * every return is CATEGORISED, so the closed outcome vocabulary is DERIVED
#     as the decider's REFUSAL set instead of being transcribed from the
#     artifact and compared to itself;
#   * the authority record is instrumented, so its READ SET is measured rather
#     than asserted -- the artifact records that set and the record is
#     hard-compared;
#   * a discrimination experiment measures WHICH record field decides, which is
#     what the `dispositive`/`advisory` attachment check is bound against.
#
# The world is a fact about the filesystem and the record set.  It carries no
# field describing a call signature, because SN-P1's claim is that no such
# argument position exists -- and correspondingly `resolve()` below HAS NO ROOT
# PARAMETER.  That is the property expressed as code rather than as prose.

REFUSAL, CONTINUATION = "REFUSAL", "CONTINUATION"

# The decider's own outcome table.  This is CODE, not a transcription of the
# artifact: `closedValues` is checked against the refusal set derived from here,
# so renaming an outcome in the artifact cannot be matched by renaming a literal
# in the checker without also changing what the decider returns.
OUTCOME_KIND = {
    "STORAGE_ROOT_CALLER_SUPPLIED": REFUSAL,
    "STORAGE_ROOT_UNVERIFIED": REFUSAL,
    "STORAGE_ROOT_IDENTITY_MISMATCH": REFUSAL,
    "STORAGE_ROOT_COLLISION": REFUSAL,
    "STORAGE_ROOT_LOCATOR_STALE": REFUSAL,
    "STORAGE_ROOT_NOT_ONE_DEVICE": REFUSAL,
    "STORAGE_NAMESPACE_ORPHANED": REFUSAL,
    "RESOLVED": CONTINUATION,
    "ADMITTED": CONTINUATION,
    "NAMESPACE_ABSENT": CONTINUATION,
    "NO_AUTHORITY_RECORD": CONTINUATION,
}
DERIVED_CLOSED_VALUES = frozenset(
    name for name, kind in OUTCOME_KIND.items() if kind == REFUSAL)


class Record(dict):
    """An authority record that records which of its fields were read.

    The subject states that resolution's read-set of the record is exactly
    {activeRootId, activeRootCanonicalPath} and that the predecessor's was the
    EMPTY SET.  That is a measurement, so it is measured."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reads: set = set()

    def __getitem__(self, key):
        self.reads.add(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        self.reads.add(key)
        return super().get(key, default)


def resolve(project_id: str, world: dict) -> tuple:
    """Storage resolution.  Total function of exactly one input (SN-P1).

    THERE IS NO ROOT PARAMETER.  A reviewer can verify SN-P1's central claim by
    reading this signature; no amount of prose in the artifact can make it
    false and no amount of prose can make it true."""
    record = world["records"].get(project_id)
    if record is None:
        return ("NO_AUTHORITY_RECORD", "SN-P4")
    bound = record["activeRootCanonicalPath"]          # advisory locator only
    root = world["roots"].get(bound)
    if root is None:
        # SN-P1: the advisory locator is an exact accelerator; cache absence is
        # never a false empty and never a fresh namespace.
        return ("STORAGE_ROOT_LOCATOR_STALE", "SN-P2")
    if not root["wellFormed"] or root["rootId"] is None:
        return ("STORAGE_ROOT_UNVERIFIED", None)
    if root["rootId"] != record["activeRootId"]:
        # The decision, taken AFTER landing.  Repointing the hint at a decoy
        # changes where we land and changes nothing about what decides.
        return ("STORAGE_ROOT_IDENTITY_MISMATCH", "SN-P1")
    if not root["oneDevice"]:
        return ("STORAGE_ROOT_NOT_ONE_DEVICE", "SN-P3")
    if project_id not in root["namespaces"]:
        return ("NAMESPACE_ABSENT", "SN-P5")
    return ("RESOLVED", None)


def supply_root_at_resolution() -> tuple:
    """There is no argument position, so a root presented on one is typed."""
    return ("STORAGE_ROOT_CALLER_SUPPLIED", "SN-P1")


def admit(offered_path: str, world: dict) -> tuple:
    """Admission at one of the three selection sites outside the resolver."""
    root = world["roots"].get(offered_path)
    if root is None or not root["wellFormed"] or root["rootId"] is None:
        return ("STORAGE_ROOT_UNVERIFIED", None)
    if not root["oneDevice"]:
        # SN-P3 is an ADMISSION property: refused before any user-derived
        # durable write, never discovered inside a state machine.
        return ("STORAGE_ROOT_NOT_ONE_DEVICE", "SN-P3")
    # SN-P2: uniqueness is an invariant of the LIVE RECORD SET, evaluated
    # whenever the set is read.  The locator is a PRESENCE PROBE, never a
    # decision procedure -- which is the whole reason a copy and a move get
    # different answers instead of both being refused.
    for record in world["records"].values():
        if record["activeRootId"] != root["rootId"]:
            continue
        bound = record["activeRootCanonicalPath"]
        if bound == offered_path:
            continue
        other = world["roots"].get(bound)
        if other is not None and other["rootId"] == root["rootId"]:
            return ("STORAGE_ROOT_COLLISION", "SN-P2")      # two LIVE locators
        if other is None:
            return ("STORAGE_ROOT_LOCATOR_STALE", "SN-P2")  # moved, not copied
    # SN-P5: a canonical namespace under an admitted root that no live record
    # binds is never silently adopted.
    for pid in sorted(root["namespaces"]):
        record = world["records"].get(pid)
        if record is None or record["activeRootId"] != root["rootId"]:
            return ("STORAGE_NAMESPACE_ORPHANED", "SN-P5")
    return ("ADMITTED", None)


def _root(root_id, *, present=True, well=True, device=True, namespaces=()):
    return None if not present else {
        "rootId": root_id, "wellFormed": well, "oneDevice": device,
        "namespaces": frozenset(namespaces)}


def _world(records, roots):
    return {"records": {k: Record(v) for k, v in records.items()},
            "roots": {k: v for k, v in roots.items() if v is not None}}


def decide(call: tuple, world: dict) -> tuple:
    kind, argument = call
    if kind == "supply":
        return supply_root_at_resolution()
    if kind == "resolve":
        return resolve(argument, world)
    return admit(argument, world)


PID = "prj1-" + "ab" * 32
R1, R2 = "root1-" + "11" * 16, "root1-" + "22" * 16

# The six declared vectors, restated as WORLDS plus the decision this checker
# takes on them.  Only `accept-root-move-with-bound-locator-absent` is a
# permitted continuation, so only it may carry `valid: true` / `satisfies`.
VECTOR_MODEL = {
    "reject-root-supplied-at-resolution": {
        "call": ("supply", None),
        "world": _world({}, {}),
        "outcome": "STORAGE_ROOT_CALLER_SUPPLIED", "property": "SN-P1",
        "valid": False,
        "scenario": ("caller passes", "storage-resolution path"),
        "expected": (),
    },
    "reject-root-identity-mismatch-through-advisory-locator": {
        # The advisory hint is REPOINTED AT THE DECOY.  Identity still decides.
        "call": ("resolve", PID),
        "world": _world(
            {PID: {"activeRootId": R1, "activeRootCanonicalPath": "/decoy"}},
            {"/authoritative": _root(R1, namespaces=[PID]),
             "/decoy": _root(R2)}),
        "outcome": "STORAGE_ROOT_IDENTITY_MISMATCH", "property": "SN-P1",
        "valid": False,
        "scenario": ("activeRootCanonicalPath resolves",
                     "rootId differs from activeRootId"),
        "expected": (),
    },
    "reject-copied-root-two-live-locators": {
        "call": ("admit", "/copy"),
        "world": _world(
            {PID: {"activeRootId": R1, "activeRootCanonicalPath": "/orig"}},
            {"/orig": _root(R1, namespaces=[PID]),
             "/copy": _root(R1, namespaces=[PID])}),
        "outcome": "STORAGE_ROOT_COLLISION", "property": "SN-P2",
        "valid": False,
        "scenario": ("copied whole", "both present", "byte-identical",
                     "offered for admission"),
        "expected": (),
    },
    "accept-root-move-with-bound-locator-absent": {
        "call": ("admit", "/moved"),
        "world": _world(
            {PID: {"activeRootId": R1, "activeRootCanonicalPath": "/orig"}},
            {"/orig": _root(R1, present=False),
             "/moved": _root(R1, namespaces=[PID])}),
        "outcome": "STORAGE_ROOT_LOCATOR_STALE", "property": "SN-P2",
        "valid": True,
        "scenario": ("renamed rather than copied", "bound locator is absent",
                     "exactly one root bears that rootId"),
        "expected": ("unchanged rootId and unchanged generation",
                     "explicit adopt"),
    },
    "reject-root-spanning-two-devices": {
        "call": ("admit", "/root"),
        "world": _world(
            {PID: {"activeRootId": R1, "activeRootCanonicalPath": "/root"}},
            {"/root": _root(R1, device=False, namespaces=[PID])}),
        "outcome": "STORAGE_ROOT_NOT_ONE_DEVICE", "property": "SN-P3",
        "valid": False,
        "scenario": ("mounted at projects/<ProjectId>", "otherwise valid root"),
        "expected": ("before any user-derived durable write",),
    },
    "reject-orphan-namespace-with-no-live-record": {
        "call": ("admit", "/root"),
        "world": _world({}, {"/root": _root(R1, namespaces=[PID])}),
        "outcome": "STORAGE_NAMESPACE_ORPHANED", "property": "SN-P5",
        "valid": False,
        "scenario": ("no live authority record names that ProjectId at that "
                     "root",),
        "expected": (),
    },
}

# REACHABILITY, one world per refusal outcome.  `outcomes.closedValues` is not
# compared against a literal -- it is compared against the set of outcomes this
# decider can actually produce, and every member must be produced by at least
# one enumerated world.  An outcome nobody can reach is decorative, which is how
# the predecessor artifact reached a durable field with no consumer.
REACHABILITY_WORLDS = {
    "STORAGE_ROOT_CALLER_SUPPLIED": ("supply", None, _world({}, {})),
    "STORAGE_ROOT_UNVERIFIED": (
        "admit", "/bad", _world({}, {"/bad": _root(R1, well=False)})),
    "STORAGE_ROOT_IDENTITY_MISMATCH": (
        "resolve", PID,
        _world({PID: {"activeRootId": R1, "activeRootCanonicalPath": "/decoy"}},
               {"/decoy": _root(R2)})),
    "STORAGE_ROOT_COLLISION": (
        "admit", "/copy",
        _world({PID: {"activeRootId": R1, "activeRootCanonicalPath": "/orig"}},
               {"/orig": _root(R1), "/copy": _root(R1)})),
    "STORAGE_ROOT_LOCATOR_STALE": (
        "admit", "/moved",
        _world({PID: {"activeRootId": R1, "activeRootCanonicalPath": "/orig"}},
               {"/orig": _root(R1, present=False), "/moved": _root(R1)})),
    "STORAGE_ROOT_NOT_ONE_DEVICE": (
        "admit", "/root", _world({}, {"/root": _root(R1, device=False)})),
    "STORAGE_NAMESPACE_ORPHANED": (
        "admit", "/root", _world({}, {"/root": _root(R1, namespaces=[PID])})),
}

# Controls: derived scenarios with no declared vector, asserted about the
# DECIDER itself so that the decider cannot degenerate into a constant.
DECIDER_CONTROLS = (
    ("advisory hint pointed at the authoritative root resolves",
     ("resolve", PID),
     _world({PID: {"activeRootId": R1,
                   "activeRootCanonicalPath": "/authoritative"}},
            {"/authoritative": _root(R1, namespaces=[PID]),
             "/decoy": _root(R2)}),
     "RESOLVED"),
    ("a clean root with a bound record admits",
     ("admit", "/orig"),
     _world({PID: {"activeRootId": R1, "activeRootCanonicalPath": "/orig"}},
            {"/orig": _root(R1, namespaces=[PID])}),
     "ADMITTED"),
    ("a malformed root marker is unverified, not mismatched",
     ("admit", "/orig"),
     _world({}, {"/orig": _root(R1, well=False)}),
     "STORAGE_ROOT_UNVERIFIED"),
)


def measure_read_set() -> set:
    """Which record fields resolution actually reads, MEASURED."""
    world = _world(
        {PID: {"activeRootId": R1, "activeRootCanonicalPath": "/authoritative"}},
        {"/authoritative": _root(R1, namespaces=[PID])})
    resolve(PID, world)
    return set(world["records"][PID].reads)


def measure_deciding_field() -> tuple:
    """Which authority-record field is DISPOSITIVE, measured by discrimination.

    A field is dispositive iff perturbing it -- with the root the locator
    actually reaches held CONSTANT in identity -- moves the outcome.  A field is
    advisory iff repointing it at a DIFFERENT path bearing the SAME rootId does
    not move the outcome.  Neither answer is read from the artifact."""
    def outcome(active_id, locator, roots):
        return resolve(PID, _world(
            {PID: {"activeRootId": active_id,
                   "activeRootCanonicalPath": locator}}, roots))[0]

    two_paths_one_identity = {"/a": _root(R1, namespaces=[PID]),
                              "/b": _root(R1, namespaces=[PID])}
    dispositive, advisory = set(), set()
    # activeRootId perturbed, the reached root unchanged.
    if outcome(R1, "/a", two_paths_one_identity) != \
            outcome(R2, "/a", two_paths_one_identity):
        dispositive.add("activeRootId")
    else:
        advisory.add("activeRootId")
    # activeRootCanonicalPath repointed at a different path of the SAME identity.
    if outcome(R1, "/a", two_paths_one_identity) != \
            outcome(R1, "/b", two_paths_one_identity):
        dispositive.add("activeRootCanonicalPath")
    else:
        advisory.add("activeRootCanonicalPath")
    return frozenset(dispositive), frozenset(advisory)


# ============================================================ the claim table
#
# Every `anchor` below is a needle the predecessor required, carried forward
# verbatim so no absence it caught is lost.  What is new is `terms`/`stance`:
# `terms` gives a lawful rewording a second way to satisfy the claim, and
# `stance` with `guard=True` makes a contradiction elsewhere in the same
# property a finding even though every needle is still present.
#
# `guard=False` is a DISCLOSURE, not an oversight: those claims' terms are not
# discriminating enough to run a contradiction scan without false positives on
# lawful prose.  `SNV5-B` measures what that leaves open.

C = Claim

PROPERTY_CLAIMS = {
    "SN-P1": {
        "statement": (
            C("unary-arity", "total function of exactly one input",
              (("total function", "exactly one input", "unary",
                "sole input", "one input only"),), POS, guard=True),
            C("host-verified-projectid", "host-verified typed ProjectId",
              (("host-verified", "host verified"), ("projectid",)), POS),
            C("single-authority-record", "single authority record",
              (("single authority record", "one authority record",
                "that projectid's authority record"),), POS),
            C("byte-equal-decides", "byte-equal to that record",
              (("byte-equal", "byte equal", "byte-equality"),
               ("activerootid",)), POS, guard=True),
            C("activerootid-named", "activeRootId", (("activerootid",),), POS),
            C("no-argument-position",
              "argument position by which a root may be supplied",
              (("argument position",), ("root",)), NEG, guard=True),
            C("caller-supplied-outcome", "STORAGE_ROOT_CALLER_SUPPLIED",
              (("storage_root_caller_supplied",),), POS),
        ),
        "dispositiveVersusAdvisory": (
            C("id-dispositive", "activeRootId is dispositive",
              (("activerootid",), ("dispositive",)), POS),
            C("path-advisory", "activeRootCanonicalPath is an advisory locator",
              (("activerootcanonicalpath",), ("advisory",)), POS),
            C("after-landing", "byte-equality test performed after landing",
              (("byte-equality", "byte equality"), ("after landing",)), POS),
        ),
        "consumerConsequence": (
            C("sole-producer",
              "sole producer of the root half of every canonical path",
              (("sole producer", "only producer", "only thing that produces",
                "only source of"), ("root half",), ("canonical path",)),
              POS, guard=True),
        ),
        "theAdvisoryLocatorIsAnExactAccelerator": (
            C("stale-outcome", "STORAGE_ROOT_LOCATOR_STALE",
              (("storage_root_locator_stale",),), POS),
            C("never-fresh", "never a fresh namespace, never a different root",
              (("fresh namespace",),), NEG, guard=True),
        ),
        "whyThisIsStructuralAndNotASiteList": (
            C("removes-position", "removes the argument position",
              (("removes the argument position",
                "deletes the argument position",
                "argument position is removed"),), POS),
        ),
    },
    "SN-P2": {
        "statement": (
            C("is-a-function",
              "activeRootId -> activeRootCanonicalPath is a FUNCTION",
              (("function",), ("activerootid",), ("activerootcanonicalpath",)),
              POS, guard=True),
            C("no-two-live-records",
              "no two live records may name one activeRootId at two "
              "different canonical locators",
              (("two live records", "two different canonical locators",
                "two live locators", "two records"),), NEG, guard=True),
            C("evaluated-on-read", "evaluated whenever that set is read",
              (("evaluated whenever", "evaluated at open", "open time",
                "whenever that set is read"),), POS),
            C("not-allocation-step", "not a step in an allocation procedure",
              (("allocation procedure",),), NEG, guard=True),
        ),
        "openTimeDetection": (
            C("collision-outcome", "STORAGE_ROOT_COLLISION",
              (("storage_root_collision",),), POS),
            C("present-same-rootid", "PRESENT and bears that same rootId",
              (("present",), ("same rootid",)), POS),
            C("neither-selected", "Neither root is selected",
              (("is selected", "are selected", "is opened", "is chosen"),
               ("root",)), NEG, guard=True),
        ),
        "resolutionExits": (
            C("adopt-move", "(a) EXPLICIT ADOPT/MOVE",
              (("explicit adopt",),), POS),
            C("proven-absent", "proven ABSENT", (("proven absent",),), POS),
            C("atomic-rebind",
              "one atomic locator rebind at unchanged rootId and unchanged "
              "authority generation",
              (("atomic locator rebind",), ("unchanged",)), POS),
            C("explicit-fork", "(b) EXPLICIT FORK", (("explicit fork",),), POS),
            C("fork-create-new",
              "create-new plus fsync before that copy may be admitted",
              (("create-new", "create new"), ("copy",)), POS),
        ),
        "whyNotACreateTimeCheck": (
            C("outside-the-tool", "happens outside the tool",
              (("outside the tool",),), POS),
            C("open-path-evaluates", "property the OPEN path evaluates",
              (("open path",),), POS),
        ),
        "inexpressibility": (
            C("second-binding-is-violation",
              "writing the second, disagreeing binding IS the invariant "
              "violation",
              (("disagreeing binding",), ("violation",)), POS),
            C("no-ambiguous-state",
              "no ambiguous durable state for a recovery rule to arbitrate",
              (("ambiguous durable state",),), NEG, guard=True),
        ),
        "noNewDurableStructure": (
            C("no-field-added",
              "No field is added to authorityRecordExactFields and no store is "
              "introduced",
              (("authorityrecordexactfields",),), NEG, guard=True),
            C("record-path-named", "authorityRecordPath",
              (("authorityrecordpath",),), POS),
        ),
    },
    "SN-P3": {
        "statement": (
            C("one-device", "one device identity",
              (("one device identity", "single device identity",
                "one device"),), POS, guard=True),
            C("no-mount-point", "no path within that scope is a mount point",
              (("mount point",),), NEG, guard=True),
            C("retained-handle", "retained root handle",
              (("retained root handle", "root handle"),), POS),
            C("re-admission", "re-established at every re-admission",
              (("re-admission", "re admission", "every readmission"),), POS),
            C("before-durable-write",
              "STORAGE_ROOT_NOT_ONE_DEVICE before any user-derived durable "
              "write",
              (("before any user-derived durable write",
                "before any durable write"),), POS),
            C("no-exemption", "",
              (("exempt", "waived", "tolerated", "tolerates", "deferred until"),
               ("durable write", "mount", "device")), NEG, guard=True),
            C("scope-recursive", "every directory beneath projects/ and "
              "quarantine/",
              (("every directory beneath",),), POS),
        ),
        "whyControlIsInScope": (
            C("journal", "layout.purgeJournal", (("layout.purgejournal",),),
              POS),
            C("recovery-rule", "purge.recoveryRule",
              (("purge.recoveryrule",),), POS),
        ),
        "admissionCost": (
            C("directories-only", "ranges over DIRECTORIES",
              (("ranges over directories", "ranges over directory"),), POS),
            C("not-cas", "does not range over CAS objects",
              (("cas objects", "content-addressed objects",
                "content addressed objects"),), NEG, guard=True),
        ),
        "whyNotAnEighthCapabilityPredicate": (
            C("scope-not-capability",
              "scope property rather than a filesystem capability",
              (("scope property",),), POS),
            C("retypes-domain", "retypes the DOMAIN", (("domain",),), POS),
            C("list-unchanged", "which is why the list is unchanged",
              (("list is unchanged",),), POS),
        ),
    },
    # SN-P4 and SN-P5 carry MORE claims than the other three, deliberately.
    # Review CIR-NB-01 measured the predecessor's per-property binding density
    # at SN-P1=14, SN-P2=18, SN-P3=13, SN-P4=5, SN-P5=6 -- a range of 5-18, not
    # the 13-18 the freeze record published -- and observed that "the two
    # thinnest are the two that govern crash-time ordering".  Every key of
    # SN-P4 and SN-P5 is bound here, including the titles and the two keys the
    # predecessor left entirely free (`SN-P5.inventoryAlreadyReportsIt` and
    # both titles), so the density of the crash-ordering pair is raised rather
    # than the count of the others being padded to hide it.
    "SN-P4": {
        "title": (
            C("generation-0-to-1", "generation 0 -> 1",
              (("generation 0 -> 1", "generation 0->1",
                "generation zero to one"),), POS),
            C("not-a-second-mechanism", "not a second mechanism",
              (("second mechanism",),), NEG, guard=True, scope="position"),
        ),
        "statement": (
            C("create-new-fsync", "create-new plus fsync under the authority "
              "lease",
              (("create-new", "create new"), ("fsync",), ("lease",)), POS),
            C("first-durable-write", "at first durable write for that ProjectId",
              (("first durable write",),), POS),
            C("after-admission", "after the chosen root has been admitted",
              (("has been admitted", "after the chosen root"),), POS),
            C("specified-birth", "now has a specified birth",
              (("specified birth",),), POS),
            C("cas-empty-baseline",
              "create-new IS the compare-and-swap with an empty baseline",
              (("compare-and-swap", "compare and swap"),
               ("empty baseline",)), POS, guard=True),
            C("losing-create-new",
              "losing create-new is a losing compare-and-swap",
              (("losing",), ("compare-and-swap", "compare and swap")), POS),
            C("no-overwrite", "",
              (("last-writer-wins", "last writer wins", "overwrit", "clobber",
                "truncat"),), NEG, guard=True),
        ),
        "ordering": (
            C("record-before-namespace", "The record precedes the namespace",
              (), POS, elsewhere=True),   # bound by the RELATION: see SNV5-M
            C("admit-first", "Admit the root (SN-P2, SN-P3)",
              (("admit the root",),), POS),
            C("names-the-root", "name the root it sits under",
              (("name the root",),), POS),
            C("p5-refuses", "which is exactly the condition SN-P5 refuses",
              (("sn-p5",), ("refuses",)), POS),
        ),
        "crashRecovery": (
            C("same-root", "never by choosing a different root",
              (("different root",),), NEG, guard=True),
            C("gen1-record", "leaves a generation-1 record and no namespace",
              (("generation-1 record",),), POS),
            C("pre-first-write", "defined pre-first-write state",
              (("pre-first-write",),), POS),
            C("idempotent-under-lease",
              "completed idempotently under the lease",
              (("idempotently",), ("lease",)), POS),
            C("restarts-from-selection", "the operation restarts from selection",
              (("restarts from selection",),), POS),
        ),
    },
    "SN-P5": {
        "title": (
            C("never-fresh-under-unnamed",
              "never created fresh under a root the record does not name",
              (("created fresh",),), NEG, guard=True, scope="position"),
            C("never-silently-adopted", "never silently adopted",
              (("silently adopted", "silently adopt"),), NEG, guard=True,
              scope="position"),
        ),
        "statement": (
            C("orphan-outcome", "STORAGE_NAMESPACE_ORPHANED",
              (("storage_namespace_orphaned",),), POS),
            C("explicit-adopt", "explicit adopt", (("explicit adopt",),), POS),
            C("reserved-target",
              "migration install rename onto a target the journal already "
              "reserved",
              (("journal already reserved", "target the journal reserved"),),
              POS),
            C("no-live-record-binds", "no live authority record binds",
              (("live authority record",), ("binds", "names")), NEG,
              guard=True),
            C("no-silent-overwrite", "",
              (("overwrit", "silently adopt", "silently replace"),), NEG,
              guard=True),
            C("only-two-ways", "may be brought into existence only by",
              (("brought into existence only by", "only by (a)"),), POS),
            C("lease-held-allocation",
              "allocation in the same lease-held operation",
              (("lease-held operation",),), POS),
            C("generation-1-record",
              "generation-1 authority record for that root",
              (("generation-1 authority record",),), POS),
        ),
        "whatItCloses": (
            C("no-signal", "no specified corruption signal",
              (("corruption signal",),), POS),
            C("split-across-two", "split across two physical namespaces",
              (("two physical namespaces",),), POS),
            C("this-is-that-signal", "This is that signal",
              (("that signal",),), POS),
            C("record-lost-evidence-survives",
              "the user-state authority record is lost while the durable "
              "evidence survives",
              (("authority record is lost",),), POS),
        ),
        "inventoryAlreadyReportsIt": (
            C("corrupt-orphan-class", "corrupt-orphan class",
              (("corrupt-orphan",),), POS),
            C("connects-the-two", "SN-P5 connects the two",
              (("connects the two",),), POS),
            C("no-new-vocabulary", "adds no reporting vocabulary",
              (("reporting vocabulary",),), NEG, guard=True, scope="position"),
        ),
        "mirrors": (
            C("owner-mirror", "preExistingMarker", (("preexistingmarker",),),
              POS),
        ),
    },
}

# The section's own frame, which the gutting attack also removes.  Same shape.
FRAME_CLAIMS = (
    ("rootBinding.purpose", "SNV5-P0", (
        C("owner-cited", "resolved-inputs.v2.json#projectIdContract",
          (("resolved-inputs.v2.json#projectidcontract",),), POS),
        C("the-pair", "(admitted root, ProjectId)",
          (("(admitted root, projectid)",),), POS),
    )),
    ("rootBinding.theOneSentenceDiagnosis", "SNV5-P0", (
        C("two-custody-records", "TWO custody records",
          (("two custody records",),), POS),
        C("set-is-registry",
          "the set of authority records already IS the registry",
          (("already is the registry",),), POS),
    )),
    ("rootBinding.observabilityBoundary.rule", "SNV5-P0", (
        C("g14-gated", "release-gated under G14",
          (("release-gated under g14", "gated under g14"),), POS),
        C("not-observable", "no instrument in this corpus can observe it",
          (("instrument",), ("observe",)), NEG, guard=True, scope="position"),
        C("gate-not-discharged", "",
          (("discharged", "cleared", "satisfied"), ("g14", "gate")), NEG,
          guard=True, scope="position"),
    )),
    ("rootBinding.observabilityBoundary.whatIsObservableHere", "SNV5-P0", (
        C("consumer-observable", "that activeRootId has a specified consumer",
          (("activerootid",), ("specified consumer",)), POS),
        C("one-locator-observable", "at most one live locator per rootId",
          (("one live locator per rootid",),), POS),
        C("finite-observable", "derived from layout and is finite",
          (("derived from layout",), ("finite",)), POS),
    )),
    ("rootBinding.observabilityBoundary.whatIsNotObservableHere", "SNV5-P0", (
        C("grade", "IMPLEMENTABLE_UNEXECUTED",
          (("implementable_unexecuted",),), POS),
        C("gate", "['G14']", (("g14",),), POS),
    )),
    ("rootBinding.fixtures.enforcementDisclosure", "SNV5-P0", (
        C("names-the-checker", "check-threat-claims.py",
          (("check-threat-claims.py",),), POS),
        C("closed-set-equality",
          "closed set equality over storageNamespace.fixtures",
          (("closed set equality",),), POS),
        C("not-a-regression-instrument", "not a regression instrument",
          (("regression instrument",),), NEG, guard=True, scope="position"),
        C("not-enforced", "NOT enforced by check-threat-claims.py",
          (("enforced",), ("check-threat-claims",)), NEG, guard=True,
          scope="position"),
    )),
    ("purpose", "SNV5-P0", (
        C("lex-exclusive", "lexically project-exclusive",
          (("lexically project-exclusive",),), POS),
        C("grade", "IMPLEMENTABLE_UNEXECUTED",
          (("implementable_unexecuted",),), POS),
        C("record-and-nothing-else",
          "single authority record and by nothing else",
          (("single authority record",), ("nothing else",)), POS),
        C("the-pair",
          "The physical namespace is the pair (admitted root, ProjectId)",
          (("(admitted root, projectid)",),), POS),
    )),
    ("assurance.physicalIsolation", "SNV5-P0", (
        C("root-half", "under rootBinding, for the root half",
          (("root half",),), POS),
        C("withdrawn", "WITHDRAWN", (("withdrawn",),), POS),
    )),
    ("authority", "SNV5-U", (
        C("unary", "Storage resolution is unary",
          (("resolution is unary",),), POS),
        C("sole-input", "sole input is the host-verified typed ProjectId",
          (("sole input",), ("projectid",)), POS),
        C("cannot-be-stated", "it cannot be stated",
          (("cannot be stated",),), POS),
        C("dispositive-split",
          "activeRootId is dispositive and activeRootCanonicalPath is an "
          "advisory locator only",
          (("activerootid",), ("dispositive",)), POS),
        C("only-producer", "ONLY producer of a root for storage resolution",
          (("only producer",), ("root",)), POS),
    )),
    ("admittedStorageRoot.role", "SNV5-U", (
        C("three-operations", "exactly three operations",
          (("exactly three operations",),), POS),
        C("the-three", "first-durable-write allocation, explicit adopt, and "
          "migration target reservation",
          (("first-durable-write allocation",), ("explicit adopt",),
           ("migration target reservation",)), POS),
        C("never-at-resolution", "never selected at storage resolution",
          (("selected at storage resolution", "selected at resolution"),), NEG,
          guard=True, scope="position"),
        C("allocation-vs-naming",
          "selection is an allocation-time act, naming is a resolution-time act",
          (("allocation-time act",), ("resolution-time act",)), POS),
    )),
    ("admittedStorageRoot.admission", "SNV5-U", (
        C("cites-p2", "rootBinding.properties.SN-P2",
          (("rootbinding.properties.sn-p2",),), POS),
        C("cites-p3", "rootBinding.properties.SN-P3",
          (("rootbinding.properties.sn-p3",),), POS),
        C("before-durable-write", "before any user-derived durable write",
          (("before any user-derived durable write",),), POS),
        C("shape-does-not-bind",
          "Shape validity admits a root; it never binds one to a ProjectId",
          (("shape validity",), ("binds",)), NEG, guard=True, scope="position"),
    )),
    ("admittedStorageRoot.rootMarker.allocation", "SNV5-U", (
        C("uniqueness-elsewhere",
          "uniqueness is the separately stated open-time invariant "
          "rootBinding.properties.SN-P2",
          (("open-time invariant",), ("sn-p2",)), POS),
        C("instance-not-content",
          "rootId identifies a root INSTANCE and never root CONTENT",
          (("root instance",),), POS),
        C("copy-violates",
          "a byte-for-byte copy of an admitted root violates",
          (("byte-for-byte copy",), ("violates",)), POS),
    )),
    ("inventoryPurgeMigration.inventory.userAuthority", "SNV5-U", (
        C("record-path", "authorityRecordPath", (("authorityrecordpath",),),
          POS),
        C("evaluates-p2", "evaluates rootBinding.properties.SN-P2",
          (("sn-p2",),), POS),
        C("never-adopted", "never silently adopted",
          (("silently adopted", "silently adopt"),), NEG, guard=True,
          scope="position"),
        C("journals", "migration journals", (("migration journals",),), POS),
        C("never-authoritative", "never reported as authoritative",
          (("reported as authoritative",),), NEG, guard=True,
          scope="position"),
    )),
    ("inventoryPurgeMigration.migration.authorityRecordRule", "SNV5-U", (
        C("byte-equal-or-refuse",
          "byte-equal to activeRootId or resolution refuses and opens no "
          "namespace",
          (("byte-equal", "byte equal"), ("activerootid",)), POS),
        C("cas-expects",
          "Compare-and-swap requires the expected generation/source root",
          (("compare-and-swap", "compare and swap"), ("expected generation",)),
          POS),
        C("losing-create-new",
          "losing create-new is exactly a losing compare-and-swap",
          (("losing",), ("create-new", "create new")), POS),
        C("governs-everything",
          "This rule governs every storage resolution and not only migration",
          (("governs every storage resolution",),), POS),
        C("migration-refused", "migration is refused",
          (("migration is refused",),), POS),
    )),
    ("pathSafety.resolution", "SNV5-P3", (
        C("rename-precondition",
          "atomically rename only within one admitted root whose "
          "layout-derived rename operand set satisfies "
          "rootBinding.properties.SN-P3",
          (("atomically rename only within one admitted root",),), POS),
        C("path-is-not-device", "does not imply a DEVICE property",
          (("imply a device property",),), NEG, guard=True, scope="position"),
        C("at-admission",
          "established once at admission rather than discovered inside a "
          "state machine",
          (("established once at admission",),), POS),
    )),
    ("pathSafety.unsupported", "SNV5-P3", (
        C("domain-is-operands",
          "The domain of each predicate is the OPERANDS of that operation and "
          "not a filesystem",
          (("domain of each predicate",), ("operands",)), POS),
        C("none-added", "no predicate was added",
          (("predicate was added", "predicate is added"),), NEG, guard=True,
          scope="position"),
        C("retyping", "Retyping the domain", (("retyping the domain",),), POS),
        C("ordered-pair",
          "atomic rename is a capability of the ordered (source directory, "
          "target directory) pair",
          (("ordered (source directory, target directory) pair",),), POS),
    )),
    ("assurance.recoveryContract", "SNV5-C", (
        C("counts", "purge 6, migration 10", (), POS, elsewhere=True),
        C("cites-closure",
          "rootBinding.renameAtomicity.recoveryTableClosure",
          (("recoverytableclosure",),), POS),
    )),
    ("rootBinding.renameAtomicity.derivation", "SNV5-R", (
        C("derived-from-layout",
          "DERIVED from layout rather than enumerated beside it",
          (("derived from layout",),), POS),
        C("endpoints",
          "one endpoint under projects/ and the other under quarantine/",
          (("projects/",), ("quarantine/",)), POS),
    )),
    ("rootBinding.renameAtomicity.statedOnce", "SNV5-R", (
        C("stated-once", "stated once, at pathSafety.resolution",
          (("pathsafety.resolution",),), POS),
        C("no-branch",
          "No branch is added to any operationOrdering step",
          (("branch is added",),), NEG, guard=True, scope="position"),
        C("no-machine-edited", "no state machine is edited",
          (("state machine is edited",),), NEG, guard=True, scope="position"),
    )),
    ("rootBinding.renameAtomicity.reachOfTheAdmissionScan", "SNV5-R", (
        C("directories", "observes DIRECTORIES", (("observes directories",),),
          POS),
        C("bind-mount", "file-level bind mount", (("bind mount",),), POS),
        C("post-admission", "any mount created after admission",
          (("created after admission",),), POS),
    )),
    ("rootBinding.renameAtomicity.runtimeResidual", "SNV5-R", (
        C("persists-nothing", "PERSISTS NO STATE TRANSITION",
          (("persists no state transition",),), POS),
        C("fail-closed", "fail-closed", (("fail-closed", "fail closed"),), POS),
    )),
    ("rootBinding.renameAtomicity.recoveryTableClosure.statement", "SNV5-C", (
        C("total-over",
          "total over (reachable durable nonterminal state x observable "
          "path-presence tuple)",
          (("total over",),), POS),
        C("domain-is-durable", "DOMAIN IS DURABLE STATE",
          (("domain is durable state",),), POS),
    )),
    ("rootBinding.renameAtomicity.recoveryTableClosure."
     "admissibilityTestForAFurtherRow", "SNV5-C", (
        C("iff",
          "if and only if states or reachableDurableNonterminalStates gains a "
          "member",
          (("if and only if",), ("gains a member",)), POS),
        C("no-transition-no-point",
          "refuses without persisting a transition contributes no point",
          (("contributes no point",),), POS),
     )),
    ("rootBinding.renameAtomicity.recoveryTableClosure."
     "appliedToTheCrossDeviceRefusal", "SNV5-C", (
        C("counts", "Purge stays at exactly 6 rows and migration at exactly 10",
          (), POS, elsewhere=True),          # the numbers are re-derived: SNV5-C
        C("admission-property", "ADMISSION property and not a failure branch",
          (("admission property",),), POS),
     )),
    ("rootBinding.renameAtomicity.recoveryTableClosure.whatWouldFalsifyThis",
     "SNV5-C", (
        C("falsifier", "falsifies this closure claim",
          (("falsifies this closure claim",),), POS),
     )),
    ("rootBinding.outcomes.rule", "SNV5-X", (
        C("mints-nothing",
          "mints NO D9 class, error code or exit code and extends no D9 "
          "vocabulary",
          (("d9",), ("mints no", "no d9 class")), NEG, guard=True,
          scope="position"),
        C("owner-mapping",
          "resolved-inputs.v2.json#projectIdContract.identityOutcomeD9Mapping",
          (("identityoutcomed9mapping",),), POS),
        C("three-provenances", "three existing closed provenance values",
          (("closed provenance values",),), POS),
     )),
    ("rootBinding.outcomes.whyTheseAreNamed", "SNV5-X", (
        C("none-decorative", "none is decorative", (("decorative",),), NEG,
          guard=True, scope="position"),
     )),
)


# ============================================================ the claim runner
def require_claims(document, path: str, claims: tuple, family: str,
                   findings: list, prefix: str = NS_PREFIX,
                   scan_clauses: list | None = None,
                   grades: dict | None = None) -> None:
    """Bind one position by CLAIMS.

    Absence is caught exactly as the predecessor caught it -- anchor gone and
    terms gone is a finding at the position.  CONTRADICTION is caught too: a
    clause in scope that carries the claim's terms in the opposing stance is a
    finding at that clause, which is the CIR-B2 repair.  And a lawful rewording
    that keeps the meaning is admitted through `terms`, which is FP-01's."""
    where = f"{prefix}{path}"
    try:
        value = resolve_pointer(document, path)
    except MALFORMED_SHAPE_EXCEPTIONS:
        findings.append(f"{family} {where}: position does not resolve")
        return
    if value is None or (isinstance(value, (str, list, dict)) and not value):
        findings.append(f"{family} {where}: position is empty")
        return
    raw = text_of(value)
    if not raw.strip():
        findings.append(f"{family} {where}: position carries no statement")
        return

    own = clauses_of(value)
    if own and _FRAME_NEGATION_RE.match(blocks_of(value)[0]):
        findings.append(
            f"{family} {where}: the position opens with a frame negation "
            f"({_abbrev(own[0], 60)!r}); every required substring survives "
            "such a frame and the position means its opposite")

    for claim in claims:
        if not claim.elsewhere:
            how = claim_satisfied(claim, raw, own)
            if not how:
                findings.append(
                    f"{family} {where}: no clause carries {claim.key!r} "
                    f"(anchor {claim.anchor!r} absent and no clause states its "
                    f"terms {claim.terms} in stance {claim.stance})")
            elif grades is not None:
                grades.setdefault(where, []).append((claim.key, how))
        scope = scan_clauses if (claim.scope == "property" and scan_clauses) \
            else own
        for bad in contradictions(claim, scope):
            findings.append(
                f"SNV5-M {where}: {claim.key!r} is stated in stance "
                f"{claim.stance} and CONTRADICTED at a clause in stance "
                f"{stance_of(bad)}: {_abbrev(bad)!r} -- every required "
                "substring survives this edit and the position means its "
                "opposite")


def _properties(namespace: dict, root_binding: dict, grades: dict) -> list:
    findings: list = []
    properties = root_binding.get("properties")
    if not isinstance(properties, dict):
        return ["SNV5-P0 storageNamespace.rootBinding.properties: absent or "
                "not an object"]
    if set(properties) != set(PROPERTY_IDS):
        findings.append(
            f"SNV5-P0 storageNamespace.rootBinding.properties: key set is not "
            f"closed/exact; missing {sorted(set(PROPERTY_IDS) - set(properties))}"
            f", unexpected {sorted(set(properties) - set(PROPERTY_IDS))}")
    for pid in PROPERTY_IDS:
        base = f"storageNamespace.rootBinding.properties.{pid}"
        node = properties.get(pid)
        family = f"SNV5-{pid[-2:]}"
        if not isinstance(node, dict):
            findings.append(f"{family} {base}: absent or not an object")
            continue
        for key in ("title", "statement"):
            if not isinstance(node.get(key), str) or not node[key].strip():
                findings.append(f"{family} {base}.{key}: absent or empty")
        # The contradiction scan reaches the WHOLE property, so a reversal
        # parked in a sibling key is caught at the claim it reverses.  The
        # review's ESC-05 does exactly that twice.
        property_clauses = clauses_of(node)
        for key, claims in PROPERTY_CLAIMS[pid].items():
            require_claims(namespace,
                           f"rootBinding.properties.{pid}.{key}", claims,
                           family, findings, scan_clauses=property_clauses,
                           grades=grades)
    return findings


def _frames(namespace: dict, grades: dict) -> list:
    findings: list = []
    for path, family, claims in FRAME_CLAIMS:
        require_claims(namespace, path, claims, family, findings, grades=grades)
    return findings


# ------------------------------------------------------------------ SNV5-M
def _meaning(namespace: dict, root_binding: dict, env: dict) -> list:
    """The three bindings that are STRUCTURAL rather than lexical."""
    findings: list = []
    properties = root_binding.get("properties")
    if not isinstance(properties, dict):
        return findings

    # 1. RELATION.  SN-P4's ordering, extracted and tested for consistency.
    #    The reference requirement -- record before namespace -- is not read
    #    from the artifact: it is the order SN-P4's crash-recovery semantics
    #    force, and it is stated in code here so an inverted artifact fails.
    p4 = properties.get("SN-P4")
    where = "storageNamespace.rootBinding.properties.SN-P4"
    if isinstance(p4, dict):
        pairs = ordering_pairs(p4)
        stated = {(a, b) for a, b, _ in pairs}
        if ("record", "namespace") not in stated:
            findings.append(
                f"SNV5-M {where}.ordering: the prose states no ordering "
                f"relation placing the authority record before the namespace; "
                f"relations extracted: {sorted(stated) or 'none'}")
        for a, b, clause in pairs:
            if (b, a) in stated:
                findings.append(
                    f"SNV5-M {where}: the ordering relation is CYCLIC -- both "
                    f"{a} before {b} and {b} before {a} are stated; the "
                    f"reversing clause is {_abbrev(clause)!r}")
                break
        if ("namespace", "record") in stated:
            findings.append(
                f"SNV5-M {where}: the prose states that the namespace precedes "
                "the record; SN-P4's own crash-recovery case (a generation-1 "
                "record and no namespace) is only reachable under the opposite "
                "order")

    # 2. ATTACHMENT.  Which record field decides is MEASURED, then compared.
    fields = _safe(namespace, "inventoryPurgeMigration.migration."
                              "authorityRecordExactFields")
    if not isinstance(fields, list) or not fields:
        fields = ["activeRootId", "activeRootCanonicalPath"]
    dispositive, advisory = measure_deciding_field()
    found = attachments(namespace, tuple(str(f) for f in fields))
    if found["dispositive"] and found["dispositive"] != set(dispositive):
        findings.append(
            f"SNV5-M storageNamespace: the prose attaches 'dispositive' to "
            f"{sorted(found['dispositive'])}, but the reference decider is "
            f"discriminated by {sorted(dispositive)} -- perturbing that field "
            "with the reached root held constant is what moves the outcome")
    if found["advisory"] and not found["advisory"] <= set(advisory):
        findings.append(
            f"SNV5-M storageNamespace: the prose attaches 'advisory' to "
            f"{sorted(found['advisory'])}, but repointing "
            f"{sorted(found['advisory'] - set(advisory))} at a different path "
            "of the SAME identity does move the decider's outcome, so that "
            "field is not advisory")

    # 4. RETRACTION.  Every prose leaf of the contract, not only the bound
    #    ones: a rule that withdraws itself is defeated at every position at
    #    once, and containment can never see it.
    for path, value in _strings(namespace, "storageNamespace"):
        match = _RETRACTION_RE.search(re.sub(r"\s+", " ", value))
        if match:
            findings.append(
                f"SNV5-M {path}: the position RETRACTS itself at "
                f"{match.group(0)!r}; every required substring survives a "
                "retraction because a retraction out-ranks them rather than "
                "removing them")

    # 3. READ SET.  The subject records it; freeze 7.2.2 requires a recorded
    #    measurement to be compared to the measurement it records.
    measured = measure_read_set()
    disposition = env.get("subject", {}).get("blockerDisposition")
    if isinstance(disposition, list):
        blob = normalise(" ".join(blocks_of(disposition)))
        for field in sorted(measured):
            if field.lower() not in blob:
                findings.append(
                    f"SNV5-M $.blockerDisposition: resolution's measured "
                    f"read-set of the authority record is {sorted(measured)}, "
                    f"but {field!r} is not named there; the artifact records "
                    "that set and the record must agree with the measurement")
    if measured != {"activeRootId", "activeRootCanonicalPath"}:
        findings.append(
            f"SNV5-M reference model: resolution reads {sorted(measured)} from "
            "the authority record; SN-P1 is the claim that it reads exactly "
            "activeRootId and activeRootCanonicalPath")
    return findings


# ------------------------------------------------------------------ SNV5-U
#
# The load-bearing fact is WHERE the authority record lives: had it been sited
# per-root, SN-P2 and SN-P4 would both have fallen.  The predecessor bound this
# with an equality against a TRANSCRIBED path literal, which tests the
# transcription.  Here the path is admitted by STRUCTURAL predicates only --
# user-state scoped, outside every layout root, exactly one <ProjectId>, no
# foreign key, correct final component -- so a lawful re-siting that keeps every
# property passes and a per-root re-siting fails.
ROOT_PLACEHOLDERS = ("<admittedStorageRoot>", "<targetStorageRoot>",
                     "<sourceStorageRoot>")


def _unary(namespace: dict) -> list:
    findings: list = []
    migration = namespace.get("inventoryPurgeMigration", {}).get("migration", {})
    record_path = migration.get("authorityRecordPath") \
        if isinstance(migration, dict) else None
    where = ("storageNamespace.inventoryPurgeMigration.migration."
             "authorityRecordPath")
    if not isinstance(record_path, str) or not record_path.strip():
        return [f"SNV5-U {where}: absent or not a string; the closure of the "
                "first-durable-write admission path rests on this record"]
    if not record_path.startswith("<userStateRoot>/"):
        findings.append(
            f"SNV5-U {where}: {record_path!r} is not user-state scoped; SN-P2's "
            "invariant ranges over a registry that must sit outside every root")
    for placeholder in ROOT_PLACEHOLDERS:
        if placeholder in record_path:
            findings.append(
                f"SNV5-U {where}: is sited inside {placeholder}; a per-root "
                "authority record defeats SN-P2 and SN-P4 together")
    layout = namespace.get("layout", {})
    if isinstance(layout, dict):
        for key, value in layout.items():
            if isinstance(value, str) and record_path.startswith(
                    value.rstrip("/") + "/"):
                findings.append(
                    f"SNV5-U {where}: resolves beneath layout.{key}; the "
                    "authority record must sit outside every root")
    if record_path.count("<ProjectId>") != 1:
        findings.append(
            f"SNV5-U {where}: names <ProjectId> "
            f"{record_path.count('<ProjectId>')} times; one record per "
            "ProjectId is what makes create-new a compare-and-swap")
    for foreign in ("<purgeId>", "<migrationId>", "<rootId>"):
        if foreign in record_path:
            findings.append(
                f"SNV5-U {where}: is keyed by {foreign} as well as ProjectId, "
                "so it is not one record per ProjectId")
    if not record_path.endswith("/<ProjectId>.json"):
        findings.append(
            f"SNV5-U {where}: final component is not <ProjectId>.json")

    # The decoy case, DECIDED rather than read.
    model = VECTOR_MODEL["reject-root-identity-mismatch-through-advisory-locator"]
    outcome, prop = decide(model["call"], model["world"])
    if (outcome, prop) != ("STORAGE_ROOT_IDENTITY_MISMATCH", "SN-P1"):
        findings.append(
            "SNV5-U decoy: with the advisory locator repointed at a decoy root "
            f"the decider returns {outcome}/{prop}, not "
            "STORAGE_ROOT_IDENTITY_MISMATCH/SN-P1")
    for label, call, world, expected in DECIDER_CONTROLS:
        got, _ = decide(call, world)
        if got != expected:
            findings.append(
                f"SNV5-U control: {label} -- decider returns {got}, expected "
                f"{expected}; a decider that answers everything the same way "
                "measures nothing")
    return findings


# ------------------------------------------------------------------ SNV5-X
def _outcomes(root_binding: dict, env: dict) -> list:
    findings: list = []
    outcomes = root_binding.get("outcomes")
    where = "storageNamespace.rootBinding.outcomes"
    if not isinstance(outcomes, dict):
        return [f"SNV5-X {where}: absent or not an object"]
    exact_keys(outcomes, where,
               {"rule", "closedValues", "definitions", "whyTheseAreNamed"},
               "SNV5-X", findings)
    closed = outcomes.get("closedValues")
    if not isinstance(closed, list) or \
            any(not isinstance(v, str) for v in closed):
        findings.append(f"SNV5-X {where}.closedValues: not a list of strings")
        closed = []

    # RE-DERIVED, not transcribed: the closed vocabulary must be exactly the
    # set of REFUSALS the reference decider can return.  A checker that
    # compares the artifact's list against a literal in the checker is testing
    # its own transcription (freeze 7.8, and the reason check-delivery-v4.py
    # was faulted).
    if set(closed) != set(DERIVED_CLOSED_VALUES):
        findings.append(
            f"SNV5-X {where}.closedValues: the published vocabulary is not the "
            f"refusal set this checker's decider produces; missing "
            f"{sorted(DERIVED_CLOSED_VALUES - set(closed))}, unexpected "
            f"{sorted(set(closed) - DERIVED_CLOSED_VALUES)}")
    if len(closed) != len(set(closed)):
        dupes = sorted({v for v in closed if closed.count(v) > 1})
        findings.append(
            f"SNV5-X {where}.closedValues: publishes {dupes} more than once; a "
            "closed vocabulary with a repeated member is degenerate")
    # REACHABILITY: every admitted value must actually be produced.
    for value in sorted(set(closed) & set(DERIVED_CLOSED_VALUES)):
        kind, argument, world = REACHABILITY_WORLDS[value]
        got, _ = decide((kind, argument), world)
        if got != value:
            findings.append(
                f"SNV5-X {where}.closedValues: {value} is admitted but the "
                f"world constructed to reach it yields {got}; an unreachable "
                "outcome is decorative")

    definitions = outcomes.get("definitions")
    if not isinstance(definitions, dict):
        findings.append(f"SNV5-X {where}.definitions: absent or not an object")
        definitions = {}
    if set(definitions) != set(closed):
        findings.append(
            f"SNV5-X {where}.definitions: key set differs from closedValues; "
            f"undefined {sorted(set(closed) - set(definitions))}, "
            f"undeclared {sorted(set(definitions) - set(closed))} -- an "
            "outcome cannot be added without being defined or defined without "
            "being admitted")

    provenance_values = set()
    resolved_inputs = env.get("resolvedInputs")
    if isinstance(resolved_inputs, dict):
        provenance_values = set(
            resolved_inputs.get("projectIdContract", {})
            .get("identityOutcomeD9Mapping", {})
            .get("provenanceContexts", {})
            .get("closedValues", []))
    if not provenance_values:
        findings.append(
            "SNV5-X provenance: resolved-inputs.v2.json publishes no closed "
            "provenance set, so the outcomes' projection cannot be verified "
            "against the identity owner it claims to reuse")

    for name, definition in sorted(definitions.items()):
        base = f"{where}.definitions.{name}"
        if not exact_keys(definition, base, {"meaning", "provenance",
                                             "raisedBy"}, "SNV5-X", findings):
            continue
        if not isinstance(definition["meaning"], str) or \
                not definition["meaning"].strip():
            findings.append(f"SNV5-X {base}.meaning: empty")
        raised_by = definition.get("raisedBy")
        if raised_by in PROPERTY_IDS:
            pass
        elif isinstance(raised_by, str) and raised_by:
            try:
                resolve_pointer(env["namespace"], raised_by)
            except MALFORMED_SHAPE_EXCEPTIONS:
                findings.append(
                    f"SNV5-X {base}.raisedBy: {raised_by!r} is neither a "
                    "member of rootBinding.properties nor a position that "
                    "resolves in storageNamespace")
        else:
            findings.append(f"SNV5-X {base}.raisedBy: absent or empty")
        if provenance_values:
            tokens = set(re.findall(r"[A-Za-z][A-Za-z0-9]*",
                                    str(definition.get("provenance", ""))))
            if not tokens & provenance_values:
                findings.append(
                    f"SNV5-X {base}.provenance: names none of the identity "
                    f"owner's closed provenance values "
                    f"{sorted(provenance_values)}")

    blob = canonical(root_binding)
    for value in sorted(set(closed)):
        if blob.count(value) < 2:
            findings.append(
                f"SNV5-X {where}.closedValues: {value} appears only in the "
                "vocabulary; an outcome with exactly one occurrence is "
                "decorative, which is how the predecessor reached a durable "
                "field with no consumer")

    # "mints NO D9 class" is a claim about another artifact.  Measured there.
    for label, blob_bytes in (("d9-exit-contract.v1.14.json", env["d9Bytes"]),
                              ("resolved-inputs.v2.json",
                               env["resolvedInputsBytes"])):
        for value in sorted(DERIVED_CLOSED_VALUES):
            if value.encode() in blob_bytes:
                findings.append(
                    f"SNV5-X D9: {value} occurs in {label}; rootBinding "
                    "declares it mints no D9 class and extends no D9 "
                    "vocabulary")
    return findings


# ------------------------------------------------------------------ SNV5-V
def _vectors(root_binding: dict) -> list:
    findings: list = []
    fixtures = root_binding.get("fixtures")
    where = "storageNamespace.rootBinding.fixtures"
    if not isinstance(fixtures, dict):
        return [f"SNV5-V {where}: absent or not an object"]
    exact_keys(fixtures, where, {"enforcementDisclosure", "vectors"},
               "SNV5-V", findings)
    vectors = fixtures.get("vectors")
    if not isinstance(vectors, list):
        return findings + [f"SNV5-V {where}.vectors: absent or not a list"]
    ids = [v.get("id") for v in vectors if isinstance(v, dict)]
    if len(ids) != len(set(ids)):
        findings.append(f"SNV5-V {where}.vectors: duplicate vector id")
    if set(ids) != set(VECTOR_MODEL):
        findings.append(
            f"SNV5-V {where}.vectors: id set is not closed/exact; missing "
            f"{sorted(set(VECTOR_MODEL) - set(ids))}, unexpected "
            f"{sorted(set(ids) - set(VECTOR_MODEL))}")

    outcomes_seen: dict = {}
    for index, vector in enumerate(vectors):
        base = f"{where}.vectors[{index}]"
        if not isinstance(vector, dict):
            findings.append(f"SNV5-V {base}: not an object")
            continue
        vid = vector.get("id")
        base = f"{where}.vectors[{index}]({vid})"
        model = VECTOR_MODEL.get(vid)
        if model is None:
            findings.append(f"SNV5-V {base}: this checker decides no outcome "
                            "for that vector id")
            continue
        want_keys = {"id", "valid", "scenario", "expected",
                     "satisfies" if model["valid"] else "violates"}
        exact_keys(vector, base, want_keys, "SNV5-V", findings)
        scalar(vector, "valid", "boolean", f"{base}.valid", findings,
               model["valid"])

        outcome, prop = decide(model["call"], model["world"])
        if outcome != model["outcome"] or prop != model["property"]:
            findings.append(
                f"SNV5-V {base}: this checker's decider returns "
                f"{outcome}/{prop} on the modelled world but the reviewed "
                f"semantics require {model['outcome']}/{model['property']}")
            continue
        outcomes_seen[vid] = outcome
        declared_expected = vector.get("expected", "")
        if not isinstance(declared_expected, str) or \
                outcome not in declared_expected:
            findings.append(
                f"SNV5-V {base}.expected: does not name {outcome}, which is "
                "the outcome the rule as stated produces for this scenario")
        named = vector.get("satisfies" if model["valid"] else "violates")
        if named != prop:
            findings.append(
                f"SNV5-V {base}: names {named!r}, but the outcome is raised by "
                f"{prop}")
        if named not in PROPERTY_IDS:
            findings.append(
                f"SNV5-V {base}: {named!r} is not a member of "
                "rootBinding.properties")
        scenario = vector.get("scenario", "")
        if not isinstance(scenario, str) or not scenario.strip():
            findings.append(f"SNV5-V {base}.scenario: empty")
        else:
            for needle in model["scenario"]:
                if needle not in scenario:
                    findings.append(
                        f"SNV5-V {base}.scenario: omits {needle!r}, so the "
                        "declared scenario is not the world this outcome was "
                        "decided on")
        for needle in model["expected"]:
            if isinstance(declared_expected, str) and \
                    needle not in declared_expected:
                findings.append(f"SNV5-V {base}.expected: omits {needle!r}")

    # The discrimination test.  A rule that refuses a copy and a move alike has
    # not stated uniqueness, it has stated distrust.
    copied = outcomes_seen.get("reject-copied-root-two-live-locators")
    moved = outcomes_seen.get("accept-root-move-with-bound-locator-absent")
    if copied is not None and moved is not None and copied == moved:
        findings.append(
            f"SNV5-V discrimination: a copied root and a moved root both yield "
            f"{copied}; SN-P2 must DISCRIMINATE -- COLLISION for two live "
            "locators, LOCATOR_STALE for one -- not refuse both")
    if copied is not None and copied != "STORAGE_ROOT_COLLISION":
        findings.append(f"SNV5-V discrimination: a copied root yields {copied}, "
                        "expected STORAGE_ROOT_COLLISION")
    if moved is not None and moved != "STORAGE_ROOT_LOCATOR_STALE":
        findings.append(f"SNV5-V discrimination: a moved root yields {moved}, "
                        "expected STORAGE_ROOT_LOCATOR_STALE")
    return findings


# ------------------------------------------------------------------ SNV5-G
#
# Requirement 3, and the sibling half of CIR-B1: the predecessor instrument
# demanded that 720 SYNTHETIC values be distinct and demanded NOTHING of the
# published ones.  Wherever this artifact claims distinctness, the published
# corpus is required here to be non-degenerate.  Each entry names the position,
# the key that must be distinct, and the artifact's own claim of distinctness.
DISTINCTNESS = (
    ("rootBinding.properties", None, "title",
     "five properties, each a different rule"),
    ("rootBinding.properties", None, "statement",
     "five properties, each a different rule"),
    ("rootBinding.outcomes.definitions", None, "meaning",
     "outcomes.whyTheseAreNamed: none is decorative"),
    ("rootBinding.fixtures.vectors", "id", None,
     "a closed vector id set"),
    ("rootBinding.fixtures.vectors", "scenario", None,
     "each vector is a different world"),
    ("rootBinding.fixtures.vectors", "expected", None,
     "each vector reaches a different outcome"),
    ("rootBinding.renameAtomicity.derivedOperandPairs", "statedAt", None,
     "one pair per ordering step that renames"),
    ("rootBinding.identityOwnerAgreement.correspondence", "ownerPointer", None,
     "one correspondence per owner rule"),
)


def _non_degenerate(namespace: dict, env: dict) -> list:
    findings: list = []
    for path, member_key, child_key, why in DISTINCTNESS:
        node = _safe(namespace, path)
        where = f"{NS_PREFIX}{path}"
        if isinstance(node, list) and member_key:
            values = [canonical(m.get(member_key)) if isinstance(m, dict)
                      else canonical(m) for m in node]
            label = f"{where}[*].{member_key}"
        elif isinstance(node, dict) and child_key:
            values = [canonical(v.get(child_key)) if isinstance(v, dict)
                      else canonical(v) for v in node.values()]
            label = f"{where}.*.{child_key}"
        else:
            continue
        seen: dict = {}
        for index, value in enumerate(values):
            seen.setdefault(value, []).append(index)
        collapsed = {v: i for v, i in seen.items() if len(i) > 1}
        if collapsed:
            repeats = sorted(i for group in collapsed.values() for i in group)
            findings.append(
                f"SNV5-G {label}: {len(collapsed)} value(s) are published more "
                f"than once at indices {repeats}; the artifact claims {why}, "
                "and a corpus whose members collapse to byte-identical "
                "duplicates demonstrates nothing it claims to demonstrate")
        if isinstance(node, list) and len(node) < 2:
            findings.append(
                f"SNV5-G {label}: {len(node)} member(s); a published corpus of "
                "fewer than two members cannot exhibit the distinctness it is "
                "offered as evidence of")

    # The vectors must not merely be textually distinct -- they must reach
    # DIFFERENT decisions.  This is the half CIR-B1 found missing.
    reached = {}
    for vid, model in VECTOR_MODEL.items():
        reached[vid] = decide(model["call"], model["world"])[0]
    if len(set(reached.values())) != len(reached):
        collide = sorted(v for v in set(reached.values())
                         if list(reached.values()).count(v) > 1)
        findings.append(
            f"SNV5-G rootBinding.fixtures.vectors: {len(reached)} vectors "
            f"reach only {len(set(reached.values()))} distinct outcomes "
            f"({collide} is reached more than once); a vector that reaches an "
            "outcome another vector already reaches controls nothing")

    # Every correspondence must resolve in the LIVE identity owner, so the
    # agreement is a fact about two artifacts rather than a claim about one.
    owner = env.get("resolvedInputs")
    correspondence = _safe(namespace,
                           "rootBinding.identityOwnerAgreement.correspondence")
    if isinstance(correspondence, list) and isinstance(owner, dict):
        contract = owner.get("projectIdContract", {})
        for index, entry in enumerate(correspondence):
            pointer = entry.get("ownerPointer") if isinstance(entry, dict) \
                else None
            if not isinstance(pointer, str) or not pointer:
                findings.append(
                    f"SNV5-G {NS_PREFIX}rootBinding.identityOwnerAgreement."
                    f"correspondence[{index}].ownerPointer: absent or empty")
                continue
            bare = pointer.split(" ", 1)[0]
            try:
                resolve_pointer(contract, bare)
            except MALFORMED_SHAPE_EXCEPTIONS:
                findings.append(
                    f"SNV5-G {NS_PREFIX}rootBinding.identityOwnerAgreement."
                    f"correspondence[{index}].ownerPointer: {bare!r} does not "
                    "resolve in resolved-inputs.v2.json#projectIdContract, so "
                    "the declared agreement is with nothing")
            analogue = entry.get("rootAnalogue", "")
            if isinstance(analogue, str) and \
                    not any(t in analogue for t in PROPERTY_IDS) and \
                    not any(t in analogue for t in DERIVED_CLOSED_VALUES) and \
                    "knownLimitations" not in analogue:
                findings.append(
                    f"SNV5-G {NS_PREFIX}rootBinding.identityOwnerAgreement."
                    f"correspondence[{index}].rootAnalogue: {analogue!r} names "
                    "no property, no outcome and no disclosure of this "
                    "artifact, so the correspondence has no root-side referent")
    return findings


# ------------------------------------------------------------------ SNV5-E
#
# Claims about disk, MEASURED on disk.  This is the strongest answer to a
# needle-preserving reversal, because it does not depend on how the sentence is
# written at all: the fact it asserts is checked where the fact lives.
def _measured_claims(namespace: dict, root_binding: dict, env: dict) -> list:
    findings: list = []

    # 1. The enforcement disclosure.  Whether check-threat-claims.py enforces
    #    these vectors is decided by reading check-threat-claims.py.
    disclosure = _safe(root_binding, "fixtures.enforcementDisclosure")
    where = f"{RB_PREFIX}fixtures.enforcementDisclosure"
    checker_bytes = env.get("threatClaimsBytes", b"")
    reaches = checker_bytes.count(b"rootBinding")
    if isinstance(disclosure, str) and disclosure:
        asserts_enforced = any(
            _matches(clause, (("enforced",), ("check-threat-claims",)))
            and stance_of(clause) == POS
            for clause in clauses_of(disclosure))
        if asserts_enforced and reaches == 0:
            findings.append(
                f"SNV5-E {where}: a clause asserts that check-threat-claims.py "
                f"ENFORCES these vectors, but that file contains "
                f"{reaches} occurrence(s) of 'rootBinding'; the claim is false "
                "where the fact lives")
        if not asserts_enforced and reaches:
            findings.append(
                f"SNV5-E {where}: check-threat-claims.py now contains "
                f"{reaches} occurrence(s) of 'rootBinding', so the disclosure "
                "that it does not reach these vectors is stale")
    if not checker_bytes:
        findings.append(
            f"SNV5-E {THREAT_CLAIMS_REL}: absent, so the enforcement "
            "disclosure cannot be measured where the fact lives")

    # 2. The observability boundary against the LIVE assurance block.
    assurance = env.get("subject", {}).get("assurance", {})
    rule = _safe(root_binding, "observabilityBoundary.rule")
    where = f"{RB_PREFIX}observabilityBoundary.rule"
    state = assurance.get("state") if isinstance(assurance, dict) else None
    grade = assurance.get("evidenceGrade") if isinstance(assurance, dict) \
        else None
    gates = assurance.get("gateIds") if isinstance(assurance, dict) else None
    if isinstance(rule, str) and rule:
        for clause in clauses_of(rule):
            if stance_of(clause) != POS:
                continue
            if _matches(clause, (("discharged", "cleared"), ("g14", "gate"))):
                findings.append(
                    f"SNV5-E {where}: a clause states that the gate is "
                    f"discharged, but $.assurance publishes state {state!r}, "
                    f"evidenceGrade {grade!r} and gateIds {gates!r}; the gate "
                    "is not discharged where the fact lives")
            if _matches(clause, (("observe", "observed", "observes"),
                                 ("runtime", "built host", "storage engine"))):
                findings.append(
                    f"SNV5-E {where}: a clause claims runtime conformance IS "
                    f"observed, but $.assurance.evidenceGrade is {grade!r} and "
                    "no demonstration evidence is declared anywhere in this "
                    "artifact")
    if isinstance(gates, list) and gates != ["G14"]:
        findings.append(
            f"SNV5-E $.assurance.gateIds: {gates!r}; the observability "
            "boundary is written against exactly ['G14']")
    if grade != "IMPLEMENTABLE_UNEXECUTED":
        findings.append(
            f"SNV5-E $.assurance.evidenceGrade: {grade!r}; rootBinding's "
            "observability boundary and purpose both name "
            "IMPLEMENTABLE_UNEXECUTED")

    # 3. The predecessor INSTRUMENT is unedited.  freeze 7.2/7.6 forbid editing
    #    it and the review pins it; that is a fact about disk, so it is
    #    measured here rather than asserted in a comment.  The expected digest
    #    is READ FROM THE REVIEW, not transcribed.
    review = env.get("review")
    if isinstance(review, dict):
        for entry in review.get("perInstrument", []):
            if not isinstance(entry, dict):
                continue
            rel = entry.get("instrument")
            if rel != PREDECESSOR_INSTRUMENT_REL:
                continue
            declared = entry.get("sha256Declared")
            path = ROOT / rel
            measured = hashlib.sha256(path.read_bytes()).hexdigest() \
                if path.exists() else None
            if measured is None:
                findings.append(
                    f"SNV5-E {rel}: the reviewed predecessor instrument is "
                    "absent from disk")
            elif measured != declared:
                findings.append(
                    f"SNV5-E {rel}: the predecessor instrument is pinned by "
                    f"{REVIEW_REL} at {declared} and measures {measured}; "
                    "freeze 7.2 forbids editing reviewed bytes and this "
                    "successor exists so that they need not be edited")
    return findings


# ------------------------------------------------------------------ SNV5-W
#
# freeze 7.2.2: a recorded measurement must be hard-compared against the
# measurement it records.  An independent review of a sibling instrument found a
# `recordedInputs` digest replaced by 64 `f`s passing green -- "it launders
# itself through the accountability gate".  Every recorded measurement in this
# subject is re-derived here from the bytes it claims to be about.
_MD_RE = re.compile(r"[A-Za-z0-9_.\-/]+\.md\b")
_SERIALISATIONS = {
    "sortKeysCompact": dict(sort_keys=True, separators=(",", ":")),
    "documentOrderCompact": dict(sort_keys=False, separators=(",", ":")),
    "defaultSeparators": dict(sort_keys=False),
}


def _measure(rel: str) -> str | None:
    path = ROOT / rel
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _recorded_measurements(subject: dict, env: dict) -> list:
    findings: list = []

    # 1. Every verifiedInputs digest, re-measured.  Drift is EXPECTED for the
    #    two documents the artifact's own driftNote names and only for those --
    #    so a fabricated digest widens the drift set and is caught, and a
    #    driftNote widened to cover a fabrication is caught too.
    record = subject.get("verifiedInputs")
    where = "$.verifiedInputs"
    if not isinstance(record, dict):
        findings.append(f"SNV5-W {where}: absent or not an object; freeze 7.2 "
                        "requires the input record as DATA")
        return findings
    files = record.get("files")
    if not isinstance(files, list) or not files:
        findings.append(f"SNV5-W {where}.files: absent or empty")
        return findings
    drift_note = record.get("driftNote", "")
    declared_mobile = set(_MD_RE.findall(drift_note)
                          if isinstance(drift_note, str) else [])
    measured_drift: set = set()
    for index, entry in enumerate(files):
        base = f"{where}.files[{index}]"
        if not isinstance(entry, dict):
            findings.append(f"SNV5-W {base}: not an object")
            continue
        rel = entry.get("path")
        declared = entry.get("sha256Measured")
        if not isinstance(rel, str) or not rel:
            findings.append(f"SNV5-W {base}.path: absent or empty")
            continue
        if not isinstance(declared, str) or \
                not re.fullmatch(r"[0-9a-f]{64}", declared):
            findings.append(
                f"SNV5-W {base}.sha256Measured: {declared!r} is not a SHA-256 "
                "hex digest")
            continue
        measured = _measure(rel)
        if measured is None:
            findings.append(
                f"SNV5-W {base}: {rel} is recorded as an input and is absent "
                "from disk; a recorded input that cannot be re-measured is an "
                "attestation, not a record")
            continue
        if measured != declared:
            measured_drift.add(rel)
        expected_pin = entry.get("expectedPin")
        if isinstance(expected_pin, str) and expected_pin:
            if expected_pin != measured:
                findings.append(
                    f"SNV5-W {base}: expectedPin {expected_pin} does not match "
                    f"the live digest {measured} of {rel}")
            if entry.get("matchesExpectedPin") is not (expected_pin == declared):
                findings.append(
                    f"SNV5-W {base}.matchesExpectedPin: published as "
                    f"{entry.get('matchesExpectedPin')!r}, measured "
                    f"{expected_pin == declared}")
    if measured_drift != declared_mobile:
        findings.append(
            f"SNV5-W {where}: the set of inputs whose recorded digest no "
            f"longer matches disk is {sorted(measured_drift)}, but driftNote "
            f"names {sorted(declared_mobile)}; a recorded digest that drifts "
            "without disclosure is indistinguishable from a fabricated one")

    # 2. The predecessor digest, recorded twice and pinned here once.
    predecessor = subject.get("predecessor", {})
    live = _measure(PREDECESSOR_REL)
    for key in ("sha256Declared", "sha256RecomputedAtAuthoring"):
        if predecessor.get(key) != live:
            findings.append(
                f"SNV5-W $.predecessor.{key}: records "
                f"{predecessor.get(key)!r}, {PREDECESSOR_REL} measures {live}")
    if predecessor.get("match") is not (
            predecessor.get("sha256Declared") ==
            predecessor.get("sha256RecomputedAtAuthoring")):
        findings.append(
            "SNV5-W $.predecessor.match: does not agree with the two digests "
            "it summarises")

    # 3. All three subtree serialisations, RE-DERIVED byte-exactly.  This is
    #    the measurement the review recorded and the artifact reproduces; both
    #    the byte count and the digest are recomputed here from the predecessor.
    reproduced = predecessor.get("subtreeDigestsReproduced")
    subtree = env.get("predecessor", {}).get("storageNamespace")
    if isinstance(reproduced, dict) and subtree is not None:
        for name, kwargs in _SERIALISATIONS.items():
            base = f"$.predecessor.subtreeDigestsReproduced.{name}"
            entry = reproduced.get(name)
            if not isinstance(entry, dict):
                findings.append(f"SNV5-W {base}: absent or not an object")
                continue
            raw = json.dumps(subtree, ensure_ascii=False, **kwargs).encode()
            digest = hashlib.sha256(raw).hexdigest()
            if entry.get("bytes") != len(raw):
                findings.append(
                    f"SNV5-W {base}.bytes: records {entry.get('bytes')!r}, "
                    f"re-derived {len(raw)}")
            if entry.get("sha256") != digest:
                findings.append(
                    f"SNV5-W {base}.sha256: records {entry.get('sha256')!r}, "
                    f"re-derived {digest}")
            if entry.get("agrees") is not True:
                findings.append(
                    f"SNV5-W {base}.agrees: published as "
                    f"{entry.get('agrees')!r}")
        digests = {json.dumps(subtree, ensure_ascii=False, **k).encode()
                   for k in _SERIALISATIONS.values()}
        if len(digests) != len(_SERIALISATIONS):
            findings.append(
                "SNV5-W $.predecessor.subtreeDigestsReproduced: the three "
                "serialisations do not produce three distinct byte strings, so "
                "they do not independently witness anything")

    # 4. The occurrence counts the artifact re-measured before relying on them.
    measurements = subject.get("selfVerification", {}).get(
        "measurementsReproducedBeforeBeingRelliedOn", {})
    v3_bytes = (ROOT / PREDECESSOR_REL).read_bytes() \
        if (ROOT / PREDECESSOR_REL).exists() else b""
    for key, token, want in (("uniqueInTheSubtree", b"unique", 0),
                             ("exdevInTheSubtree", b"EXDEV", 0)):
        text = measurements.get(key, "") if isinstance(measurements, dict) \
            else ""
        count = v3_bytes.count(token)
        if count != want:
            findings.append(
                f"SNV5-W $.selfVerification.measurementsReproduced"
                f"BeforeBeingRelliedOn.{key}: records {want} occurrence(s) of "
                f"{token.decode()} in {PREDECESSOR_REL}; re-measured {count}")
        match = re.search(r"occurs (\d+) times", text) if isinstance(text, str) \
            else None
        if match and int(match.group(1)) != count:
            findings.append(
                f"SNV5-W $.selfVerification.measurementsReproduced"
                f"BeforeBeingRelliedOn.{key}: the prose records "
                f"{match.group(1)}, re-measured {count}")
    consumers = measurements.get("activeRootIdConsumers", "") \
        if isinstance(measurements, dict) else ""
    live_count = v3_bytes.count(b"activeRootId")
    match = re.match(r"Re-measured: (\d+) occurrence", str(consumers))
    if match and int(match.group(1)) != live_count:
        findings.append(
            "SNV5-W $.selfVerification.measurementsReproducedBeforeBeing"
            f"RelliedOn.activeRootIdConsumers: records {match.group(1)} "
            f"occurrence(s) of activeRootId in {PREDECESSOR_REL}, re-measured "
            f"{live_count}")

    # 5. The name-collision sweep: the seven identifiers are claimed absent from
    #    the corpus except where this lane put them.  Measured across the two
    #    published artifacts the outcomes claim to leave alone (SNV5-X does D9
    #    and the identity owner); here the count is bound to the vocabulary
    #    SIZE rather than to a transcribed literal.
    closed = _safe(env.get("namespace", {}),
                   "rootBinding.outcomes.closedValues")
    sweep = measurements.get("nameCollisionSweep", "") \
        if isinstance(measurements, dict) else ""
    if isinstance(closed, list) and isinstance(sweep, str) and sweep:
        match = re.search(r"\b(seven|six|five|eight|\d+)\b", sweep)
        words = {"five": 5, "six": 6, "seven": 7, "eight": 8}
        if match:
            recorded = words.get(match.group(1), None)
            if recorded is None and match.group(1).isdigit():
                recorded = int(match.group(1))
            if recorded is not None and recorded != len(closed):
                findings.append(
                    "SNV5-W $.selfVerification.measurementsReproducedBefore"
                    f"BeingRelliedOn.nameCollisionSweep: says {recorded} new "
                    f"outcome identifiers, the live vocabulary carries "
                    f"{len(closed)}")
    return findings


# ------------------------------------------------------------------ SNV5-S
def _structural_diff(a, b, path, additions, removals, changed) -> None:
    if isinstance(a, dict) and isinstance(b, dict):
        for key in a:
            if key not in b:
                removals.append(f"{path}.{key}")
            else:
                _structural_diff(a[key], b[key], f"{path}.{key}",
                                 additions, removals, changed)
        for key in b:
            if key not in a:
                additions.append(f"{path}.{key}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            changed.append((path, ("array", "array")))
        else:
            for index, (x, y) in enumerate(zip(a, b)):
                _structural_diff(x, y, f"{path}[{index}]",
                                 additions, removals, changed)
    elif jtype(a) != jtype(b) or a != b:
        changed.append((path, (jtype(a), jtype(b))))


# ------------------------------------------------------------------ SNV5-R
def _rename_operands(namespace: dict, root_binding: dict) -> list:
    """RE-DERIVE the operand set from `layout` and from the state machines'
    own ordering steps.  Carried forward from the predecessor, which survived 78
    layout substitutions with 0 escapes."""
    findings: list = []
    where = "storageNamespace.rootBinding.renameAtomicity"
    rename = root_binding.get("renameAtomicity")
    if not isinstance(rename, dict):
        return [f"SNV5-R {where}: absent or not an object"]
    exact_keys(rename, where,
               {"derivation", "derivedOperandPairs", "statedOnce",
                "reachOfTheAdmissionScan", "runtimeResidual",
                "recoveryTableClosure"}, "SNV5-R", findings)

    layout = namespace.get("layout")
    if not isinstance(layout, dict):
        return findings + ["SNV5-R storageNamespace.layout: absent or not an "
                           "object"]
    by_value: dict = {}
    for key, value in layout.items():
        if isinstance(value, str):
            by_value.setdefault(value, key)
    project_keys = [k for k, v in layout.items()
                    if isinstance(v, str) and v.endswith("/projects/<ProjectId>")]
    if len(project_keys) != 1:
        findings.append(
            f"SNV5-R storageNamespace.layout: {len(project_keys)} key(s) name "
            "the canonical project namespace; the operand set cannot be "
            "derived")
        return findings
    project_key = project_keys[0]

    lifecycle = namespace.get("inventoryPurgeMigration", {})
    derived: dict = {}
    for protocol_name in ("purge", "migration"):
        protocol = lifecycle.get(protocol_name)
        if not isinstance(protocol, dict):
            findings.append(f"SNV5-R storageNamespace.inventoryPurgeMigration."
                            f"{protocol_name}: absent or not an object")
            continue
        ordering = protocol.get("operationOrdering", [])
        if not isinstance(ordering, list):
            findings.append(f"SNV5-R storageNamespace.inventoryPurgeMigration."
                            f"{protocol_name}.operationOrdering: not a list")
            continue
        for index, step in enumerate(ordering):
            if not isinstance(step, str) or "atomically rename" not in \
                    step.lower():
                continue
            position = (f"inventoryPurgeMigration.{protocol_name}."
                        f"operationOrdering[{index}]")
            if protocol_name == "purge":
                pair = (project_key, by_value.get(protocol.get("quarantinePath")))
            elif "target staging" in step:
                pair = (by_value.get(protocol.get("targetStagingPath")),
                        project_key)
            elif "source namespace" in step:
                pair = (project_key,
                        by_value.get(protocol.get("sourceRetirementPath")))
            else:
                findings.append(
                    f"SNV5-R {position}: this step renames but names neither "
                    "the target staging nor the source namespace, so its "
                    "operands cannot be derived")
                continue
            if pair[0] is None or pair[1] is None:
                findings.append(
                    f"SNV5-R {position}: an endpoint of this rename is not a "
                    "value any layout key publishes, so the operand pair is "
                    "not layout-derived")
                continue
            derived[position] = pair

    pairs = rename.get("derivedOperandPairs")
    if not isinstance(pairs, list):
        return findings + [f"SNV5-R {where}.derivedOperandPairs: not a list"]
    declared: dict = {}
    for index, pair in enumerate(pairs):
        base = f"{where}.derivedOperandPairs[{index}]"
        if not exact_keys(pair, base, {"operation", "sourceLayoutKey",
                                       "targetLayoutKey", "statedAt"},
                          "SNV5-R", findings):
            continue
        stated_at = pair["statedAt"]
        for key in ("operation", "sourceLayoutKey", "targetLayoutKey",
                    "statedAt"):
            if not isinstance(pair[key], str) or not pair[key].strip():
                findings.append(f"SNV5-R {base}.{key}: empty or not a string")
        for key in ("sourceLayoutKey", "targetLayoutKey"):
            if pair[key] not in layout:
                findings.append(
                    f"SNV5-R {base}.{key}: {pair[key]!r} is not a key of "
                    "storageNamespace.layout, so the layout does not produce "
                    "this operand")
        try:
            step = resolve_pointer(namespace, stated_at)
        except MALFORMED_SHAPE_EXCEPTIONS:
            findings.append(f"SNV5-R {base}.statedAt: {stated_at!r} does not "
                            "resolve in storageNamespace")
            continue
        if not isinstance(step, str) or "atomically rename" not in step.lower():
            findings.append(
                f"SNV5-R {base}.statedAt: {stated_at!r} resolves to a step "
                "that states no atomic rename")
            continue
        declared[stated_at] = (pair["sourceLayoutKey"], pair["targetLayoutKey"])
        endpoints = (str(layout.get(pair["sourceLayoutKey"], "")),
                     str(layout.get(pair["targetLayoutKey"], "")))
        if sum("/projects/" in e for e in endpoints) != 1 or \
                sum("/quarantine/" in e for e in endpoints) != 1:
            findings.append(
                f"SNV5-R {base}: endpoints {endpoints} are not one under "
                "projects/ and one under quarantine/, which is the property "
                "that makes a single device predicate over those two subtrees "
                "sufficient")

    if set(declared) != set(derived):
        findings.append(
            f"SNV5-R {where}.derivedOperandPairs: the declared set does not "
            f"match the set re-derived from the state machines; declared-only "
            f"{sorted(set(declared) - set(derived))}, derived-only "
            f"{sorted(set(derived) - set(declared))}")
    for position, pair in sorted(derived.items()):
        if position in declared and declared[position] != pair:
            findings.append(
                f"SNV5-R {where}.derivedOperandPairs: at {position} the "
                f"artifact declares {declared[position]} but the layout and "
                f"the protocol's own path fields produce {pair}")
    return findings


# ------------------------------------------------------------------ SNV5-C
# A state carries no recovery row exactly when it is TERMINAL.  Naming the
# terminals here rather than deriving them as "whatever is left over" is what
# keeps the closure test non-circular.  The ROW COUNTS are not named: they are
# `len()` of the live tables, and the counts written in prose are compared
# against that.
TERMINAL_STATES = {"purge": {"COMPLETE"},
                   "migration": {"COMPLETE", "ROLLED_BACK"}}


def _recovery_closure(namespace: dict, root_binding: dict) -> list:
    findings: list = []
    where = ("storageNamespace.rootBinding.renameAtomicity."
             "recoveryTableClosure")
    closure = root_binding.get("renameAtomicity", {})
    closure = closure.get("recoveryTableClosure") if isinstance(closure, dict) \
        else None
    if not isinstance(closure, dict):
        return [f"SNV5-C {where}: absent or not an object"]
    exact_keys(closure, where,
               {"statement", "admissibilityTestForAFurtherRow",
                "appliedToTheCrossDeviceRefusal", "measuredRatherThanArgued",
                "whatWouldFalsifyThis"}, "SNV5-C", findings)

    lifecycle = namespace.get("inventoryPurgeMigration", {})
    measured: dict = {}
    for name in ("purge", "migration"):
        base = f"storageNamespace.inventoryPurgeMigration.{name}"
        protocol = lifecycle.get(name)
        if not isinstance(protocol, dict):
            findings.append(f"SNV5-C {base}: absent or not an object")
            continue
        table = protocol.get("crashRecoveryTable")
        if not isinstance(table, list):
            findings.append(f"SNV5-C {base}.crashRecoveryTable: not a list")
            continue
        measured[name] = len(table)
        states = protocol.get("states")
        if not isinstance(states, list) or \
                any(not isinstance(s, str) for s in states):
            findings.append(f"SNV5-C {base}.states: not a list of strings")
            states = []
        observed_states, seen = [], set()
        for index, row in enumerate(table):
            position = f"{base}.crashRecoveryTable[{index}]"
            if not exact_keys(row, position, {"observed", "action",
                                              "nextState"}, "SNV5-C", findings):
                continue
            observed = row["observed"]
            if not isinstance(observed, str) or "|" not in observed:
                findings.append(
                    f"SNV5-C {position}.observed: is not a (durable state | "
                    "path-presence tuple) pair, so the table's domain is not "
                    "durable state")
                continue
            if observed in seen:
                findings.append(f"SNV5-C {position}.observed: {observed!r} is "
                                "published twice; the table is not a function")
            seen.add(observed)
            state = observed.split("|", 1)[0]
            observed_states.append(state)
            if states and state not in states:
                findings.append(
                    f"SNV5-C {position}.observed: durable state {state!r} is "
                    "not a member of the closed state set")
            if row["nextState"] not in states and states:
                findings.append(
                    f"SNV5-C {position}.nextState: {row['nextState']!r} is not "
                    "a member of the closed state set")
        covered = set(observed_states)
        reachable = protocol.get("reachableDurableNonterminalStates")
        if isinstance(reachable, list) and covered != set(reachable):
            findings.append(
                f"SNV5-C {base}: recovery rows cover durable states "
                f"{sorted(covered)}, but reachableDurableNonterminalStates is "
                f"{sorted(reachable)}; the table is not total over its "
                "declared domain")
        if states:
            uncovered = set(states) - covered
            if uncovered != TERMINAL_STATES[name]:
                findings.append(
                    f"SNV5-C {base}: states carrying no recovery row are "
                    f"{sorted(uncovered)}, expected exactly the terminals "
                    f"{sorted(TERMINAL_STATES[name])}; a row is admissible if "
                    "and only if the durable nonterminal state set gains a "
                    "member")
            ordering_blob = " ".join(
                s for s in protocol.get("operationOrdering", [])
                if isinstance(s, str))
            for terminal in sorted(TERMINAL_STATES[name] & set(states)):
                if terminal not in ordering_blob:
                    findings.append(
                        f"SNV5-C {base}.operationOrdering: {terminal!r} is "
                        "treated as terminal but no ordering step persists it, "
                        "so it is not a state this protocol ends in")

    # freeze 7.2.2 -- the counts written in prose, hard-compared to len().
    for document, path, prefix, pattern in (
            (root_binding,
             "renameAtomicity.recoveryTableClosure."
             "appliedToTheCrossDeviceRefusal", RB_PREFIX,
             r"[Pp]urge stays at exactly (\d+) rows and migration at exactly "
             r"(\d+)"),
            (namespace, "assurance.recoveryContract", NS_PREFIX,
             r"purge (\d+), migration (\d+)"),
    ):
        position = f"{prefix}{path}"
        match = re.search(pattern, text_of(_safe(document, path)))
        if match is None:
            findings.append(f"SNV5-C {position}: publishes no row counts to "
                            "compare")
            continue
        for name, recorded in zip(("purge", "migration"), match.groups()):
            if name in measured and int(recorded) != measured[name]:
                findings.append(
                    f"SNV5-C {position}: records {name} at {recorded} rows, "
                    f"live table measures {measured[name]}")
    return findings


# ------------------------------------------------ SNV5-P3 device / errno
PREDICATE_HEAD = "lacking the "
PREDICATE_TAIL = " required by the operation being admitted."
RENAME_PRECONDITION = "atomically rename only within one admitted root"


def _errno_freedom(root_binding: dict) -> list:
    """The subject binds to NO errno, deliberately: a mount can present
    EXDEV(18), EBUSY(16), or silently succeed while relocating the mount."""
    findings: list = []
    for path, value in _strings(root_binding, "rootBinding"):
        if not ERRNO_RE.search(value):
            continue
        if path == ERRNO_OBSERVATION_EXEMPTION:
            if "not about any built storage engine" not in value:
                findings.append(
                    f"SNV5-P3 storageNamespace.{path}: names an errno without "
                    "framing it as a fact about rename(2) on a host")
            continue
        findings.append(
            f"SNV5-P3 storageNamespace.{path}: binds an errno "
            f"({ERRNO_RE.search(value).group(0)}); the rule must be a "
            "device-identity and mount-point property, because a mount can "
            "present EXDEV, EBUSY, or silently succeed while relocating the "
            "mount")
    return findings


def _predicate_list(namespace) -> str | None:
    text = _safe(namespace, "pathSafety.unsupported")
    if not isinstance(text, str) or PREDICATE_HEAD not in text or \
            PREDICATE_TAIL not in text:
        return None
    start = text.index(PREDICATE_HEAD) + len(PREDICATE_HEAD)
    return text[start:text.index(PREDICATE_TAIL, start)]


# ------------------------------------------------------------------ SNV5-N
def _non_interference(namespace: dict, pre_namespace: dict, env: dict) -> list:
    findings: list = []
    live = _predicate_list(namespace)
    before = _predicate_list(pre_namespace)
    if live is None or before is None:
        findings.append("SNV5-P3 storageNamespace.pathSafety.unsupported: the "
                        "capability-predicate list cannot be located, so "
                        "'no predicate was added' cannot be measured")
    else:
        if live != before:
            findings.append(
                f"SNV5-P3 storageNamespace.pathSafety.unsupported: the "
                f"predicate list changed; predecessor {before!r}, effective "
                f"{live!r} -- SN-P3 must retype the domain, never extend the "
                "list")
        members = [m for m in re.split(r",\s*|\s+or\s+", live) if m]
        before_members = [m for m in re.split(r",\s*|\s+or\s+", before) if m]
        if len(members) != len(before_members):
            findings.append(
                f"SNV5-P3 storageNamespace.pathSafety.unsupported: "
                f"{len(members)} capability predicates measured, the "
                f"predecessor publishes {len(before_members)} ({members})")

    sites = [p for p, v in _strings(namespace, "storageNamespace")
             if RENAME_PRECONDITION in v
             and not p.startswith("storageNamespace.rootBinding")]
    if sites != ["storageNamespace.pathSafety.resolution"]:
        findings.append(
            f"SNV5-P3: the rename precondition {RENAME_PRECONDITION!r} is "
            f"stated at {sites}, expected exactly "
            "['storageNamespace.pathSafety.resolution']")
    lifecycle = namespace.get("inventoryPurgeMigration", {})
    for name in ("purge", "migration"):
        ordering = lifecycle.get(name, {}).get("operationOrdering", []) \
            if isinstance(lifecycle.get(name), dict) else []
        blob = " ".join(s for s in ordering if isinstance(s, str))
        for token in ("device", "SN-P3", "filesystem"):
            if token in blob:
                findings.append(
                    f"SNV5-P3 storageNamespace.inventoryPurgeMigration.{name}."
                    f"operationOrdering: mentions {token!r}; SN-P3 adds no "
                    "branch to any ordering step")

    for label, blob_bytes in (("retention-tiers.v24.json",
                               env["retentionTiersBytes"]),
                              ("check-retention-custody-v24.py",
                               env["retentionCheckerBytes"])):
        count = blob_bytes.count(b"storageNamespace")
        if count:
            findings.append(
                f"SNV5-N 4.6: {label} contains {count} occurrence(s) of "
                "'storageNamespace'; the discharge rests on these surfaces not "
                "reading each other")
    tiers = env.get("retentionTiers")
    forbidden = _safe(tiers, "partB_purgeSemantics.effectiveCapabilityDerivation"
                             ".forbiddenInputs") if isinstance(tiers, dict) \
        else ""
    if not isinstance(forbidden, list) or "physicalLocators" not in forbidden:
        findings.append(
            "SNV5-N 4.6: retention-tiers.v24.json "
            "partB_purgeSemantics.effectiveCapabilityDerivation."
            "forbiddenInputs does not list 'physicalLocators'; SN-P3's device "
            "property could then reach effective_capability")
    return findings


# ------------------------------------------------------ SNV5-K coverage map
CHECKER_IMPACT_COVERAGE = (
    ("has exactly the closed key set", "SNV5-P1..P5",
     "binds every statement by CLAIM -- anchor or terms, plus stance -- so a "
     "placeholder fails at its own position AND a needle-preserving reversal "
     "fails at the reversing clause"),
    ("closedValues is exactly the seven listed values", "SNV5-X",
     "derives the closed vocabulary from the decider's REFUSAL set instead of "
     "transcribing it, requires every value to be reachable by a constructed "
     "world, and measures 0 D9 vocabulary minted"),
    ("names a violates or satisfies value", "SNV5-V / SNV5-G",
     "decides each vector's outcome from a world and additionally requires the "
     "published vectors to be NON-DEGENERATE -- distinct ids, scenarios, "
     "expectations and reached outcomes"),
    ("RE-DERIVED from layout by the checker", "SNV5-R",
     "re-derives the rename positions from the state machines' own ordering "
     "steps as well, and cross-checks every operand against the protocol's own "
     "path fields"),
    ("recoveryTableClosure admissibility test", "SNV5-C",
     "adds the closure PROPERTY (domain == durable nonterminal states) and "
     "hard-compares the counts written in prose against measured len()"),
    ("duplicate-key-rejecting object_pairs_hook", "SNV5-A0 / SNV5-T",
     "names the duplicated key AND its path, and admits every closed scalar by "
     "exact JSON type including bool-vs-int"),
)


def _checker_impact(subject: dict) -> list:
    findings: list = []
    impact = subject.get("checkerImpact")
    if not isinstance(impact, dict):
        return ["SNV5-K $.checkerImpact: absent or not an object; this "
                "checker's specification is the list it publishes"]
    listed = impact.get(
        "whatASuccessorCheckerMUSTaddBeforeTheNewMaterialIsMECHANICALLYbound")
    where = ("$.checkerImpact."
             "whatASuccessorCheckerMUSTaddBeforeTheNewMaterialIsMECHANICALLYbound")
    if not isinstance(listed, list):
        return [f"SNV5-K {where}: absent or not a list"]
    if len(listed) != len(CHECKER_IMPACT_COVERAGE):
        findings.append(
            f"SNV5-K {where}: {len(listed)} assertions published, this "
            f"checker's coverage map discharges {len(CHECKER_IMPACT_COVERAGE)}; "
            "the map is stale and cannot be trusted to name what is covered")
    for anchor, family, _beyond in CHECKER_IMPACT_COVERAGE:
        hits = [i for i, item in enumerate(listed)
                if isinstance(item, str) and anchor in item]
        if len(hits) != 1:
            findings.append(
                f"SNV5-K {where}: anchor {anchor!r} (discharged by {family}) "
                f"matches {len(hits)} member(s), expected exactly 1")
    if "paperSealDisclosure" not in impact:
        findings.append("SNV5-K $.checkerImpact.paperSealDisclosure: absent; "
                        "the candidate must disclose that rootBinding is "
                        "specification text until a successor checker exists")
    return findings


# ======================================================== the check itself
def _check(effective: dict, env: dict) -> list:
    findings: list = []
    findings.extend(parse_findings())
    subject = env["subject"]
    predecessor = env["predecessor"]

    # ---------------------------------------------------------- SNV5-D
    for item in env["derivation"]["declErrors"]:
        findings.append(f"SNV5-D declaration: {item}")
    for item in env["derivation"]["resolveErrors"]:
        findings.append(f"SNV5-D resolution: {item}")
    declaration = env["derivation"]["declaration"]
    if not isinstance(declaration, dict):
        findings.append("SNV5-D declaration: the candidate publishes no "
                        "machine-resolvable derivation; freeze 7.3 forbids "
                        "reading a delta as a whole document")
        return sorted(set(findings))
    if declaration.get("sha256") != PREDECESSOR_SHA:
        findings.append(
            f"SNV5-D declaration: predecessor digest declared "
            f"{declaration.get('sha256')!r}, this checker is pinned to "
            f"{PREDECESSOR_SHA}")
    if not str(declaration.get("artifact", "")).endswith("threat-model.v3.json"):
        findings.append(
            f"SNV5-D declaration: predecessor is {declaration.get('artifact')!r},"
            f" expected threat-model.v3.json")
    operations = declaration.get("operations", [])
    verbs = [op.get("op") for op in operations if isinstance(op, dict)]
    if verbs.count("add") != 1 or verbs.count("set") != len(operations) - 1:
        findings.append(f"SNV5-D declaration: expected exactly one add and the "
                        f"rest set, measured {verbs.count('set')} set + "
                        f"{verbs.count('add')} add over {len(operations)} "
                        "operations")
    for index, op in enumerate(operations):
        path = op.get("path", "") if isinstance(op, dict) else ""
        if not path.startswith("storageNamespace"):
            findings.append(f"SNV5-D declaration: operation {index} touches "
                            f"{path!r}, outside $.storageNamespace")
        if path.startswith("storageNamespace.inventoryPurgeMigration.purge"):
            findings.append(
                f"SNV5-D declaration: operation {index} touches {path!r}; the "
                "purge protocol is the subject of freeze 4.6's DISCHARGED "
                "item and this derivation must not address it")

    if not isinstance(effective, dict) or "storageNamespace" not in effective:
        findings.append("SNV5-D: the effective contract carries no "
                        "storageNamespace")
        return sorted(set(findings))
    namespace = effective["storageNamespace"]
    pre_namespace = predecessor.get("storageNamespace", {})

    # ---------------------------------------------------------- SNV5-S
    additions, removals, changed = [], [], []
    _structural_diff(predecessor, effective, "$", additions, removals, changed)
    if additions != ["$.storageNamespace.rootBinding"]:
        findings.append(
            f"SNV5-S scope: the derivation must add exactly "
            f"$.storageNamespace.rootBinding; measured additions {additions}")
    if removals:
        findings.append(f"SNV5-S scope: the derivation removes {removals}; a "
                        "derivation that deletes is not a derivation this "
                        "checker will score")
    non_prose = [p for p, kinds in changed if kinds != ("string", "string")]
    if non_prose:
        findings.append(f"SNV5-S scope: non-prose leaves changed at "
                        f"{non_prose}")
    outside = [p for p, _ in changed if not p.startswith("$.storageNamespace.")]
    if outside:
        findings.append(f"SNV5-S scope: leaves changed outside "
                        f"$.storageNamespace at {outside}")
    # The derivation's own operation count IS the expected number of changed
    # prose leaves: re-derived from the declaration, not transcribed.
    expected_changed = sum(1 for op in operations
                           if isinstance(op, dict) and op.get("op") == "set")
    if len(changed) != expected_changed:
        findings.append(
            f"SNV5-S scope: the derivation declares {expected_changed} `set` "
            f"operation(s) but the resolved contract differs from the "
            f"predecessor at {len(changed)} leaf/leaves "
            f"({[p for p, _ in changed]})")

    stale = []
    for path, value in _lists(pre_namespace, "storageNamespace"):
        try:
            live = resolve_pointer(namespace, path.split(".", 1)[1]) \
                if "." in path else namespace
        except MALFORMED_SHAPE_EXCEPTIONS:
            stale.append(path)
            continue
        if canonical(live) != canonical(value):
            stale.append(path)
    if stale:
        findings.append(
            f"SNV5-S closed collections: {len(stale)} predecessor list(s) are "
            f"not byte-identical in the effective contract: {sorted(stale)}")

    if canonical(pre_namespace.get("inventoryPurgeMigration", {}).get("purge")) \
            != canonical(namespace.get("inventoryPurgeMigration", {})
                         .get("purge")):
        findings.append(
            "SNV5-N 4.6: storageNamespace.inventoryPurgeMigration.purge is not "
            "byte-identical to the predecessor; the SN-P3 repair must not "
            "disturb the DISCHARGED purge-semantics item")

    # ---------------------------------------------------------- SNV5-T
    scalar(namespace, "schemaVersion", "integer",
           "storageNamespace.schemaVersion", findings, 1)
    root_binding = namespace.get("rootBinding")
    if not isinstance(root_binding, dict):
        findings.append(
            "SNV5-P0 storageNamespace.rootBinding: absent or not an object; "
            "the entire root half of the physical namespace pair is ungoverned")
        return sorted(set(findings))
    scalar(root_binding, "schemaVersion", "integer",
           "storageNamespace.rootBinding.schemaVersion", findings, 1)
    scalar(subject, "version", "integer", "$.version", findings)
    scalar(subject, "schemaVersion", "integer", "$.schemaVersion", findings)
    scalar(subject, "integrationAuthorized", "boolean",
           "$.integrationAuthorized", findings)

    exact_keys(root_binding, "storageNamespace.rootBinding",
               {"schemaVersion", "purpose", "theOneSentenceDiagnosis",
                "identityOwnerAgreement", "properties", "renameAtomicity",
                "outcomes", "fixtures", "observabilityBoundary"},
               "SNV5-P0", findings)

    grades = env.setdefault("grades", {})
    grades.clear()
    env = dict(env)
    env["grades"] = grades
    findings.extend(_properties(namespace, root_binding, grades))
    findings.extend(_frames(namespace, grades))
    findings.extend(_meaning(namespace, root_binding, env))
    findings.extend(_unary(namespace))
    findings.extend(_outcomes(root_binding, env))
    findings.extend(_vectors(root_binding))
    findings.extend(_non_degenerate(namespace, env))
    findings.extend(_measured_claims(namespace, root_binding, env))
    findings.extend(_recorded_measurements(subject, env))
    findings.extend(_rename_operands(namespace, root_binding))
    findings.extend(_recovery_closure(namespace, root_binding))
    findings.extend(_errno_freedom(root_binding))
    findings.extend(_non_interference(namespace, pre_namespace, env))
    findings.extend(_checker_impact(subject))
    return sorted(set(findings))


def check(effective, env) -> list:
    """Total boundary for malformed parsed JSON shapes."""
    if not isinstance(effective, dict) or not effective:
        return ["SNV5-TOTALITY-ROOT: the effective contract must be a "
                "non-empty object"]
    if not isinstance(effective.get("storageNamespace"), dict):
        return ["SNV5-TOTALITY-SHAPE: storageNamespace must be an object"]
    env.setdefault("grades", {})
    env = dict(env)
    env["namespace"] = effective["storageNamespace"]
    try:
        return _check(effective, env)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"SNV5-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__}: {exc})"]


# ================================================================= loading
def _load(rel: str, findings_label: str, required: bool = True):
    path = ROOT / rel
    if not path.exists():
        if required:
            print(f"missing input: {path}", file=sys.stderr)
            raise SystemExit(2)
        return None, b""
    raw = path.read_bytes()
    try:
        return jloads(raw.decode("utf-8"), findings_label), raw
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"{rel} is not decodable JSON: {exc}", file=sys.stderr)
        raise SystemExit(2)


def _verify(rel: str, expected: str) -> bytes:
    path = ROOT / rel
    if not path.exists():
        print(f"missing pinned input: {path}", file=sys.stderr)
        raise SystemExit(2)
    raw = path.read_bytes()
    measured = hashlib.sha256(raw).hexdigest()
    if measured != expected:
        print(f"DIGEST DRIFT on {rel}\n  pinned   {expected}\n"
              f"  measured {measured}\n"
              "This checker scores the bytes it was reviewed against and "
              "refuses to score any others.", file=sys.stderr)
        raise SystemExit(2)
    return raw


def load_environment() -> tuple:
    """Hash-verify before parsing; resolve the derivation; never read the delta
    as a whole document."""
    subject_raw = _verify(SUBJECT_REL, SUBJECT_SHA)
    predecessor_raw = _verify(PREDECESSOR_REL, PREDECESSOR_SHA)
    review_raw = _verify(REVIEW_REL, REVIEW_SHA)
    subject = jloads(subject_raw.decode("utf-8"), SUBJECT_REL)
    predecessor = jloads(predecessor_raw.decode("utf-8"), PREDECESSOR_REL)
    review = jloads(review_raw.decode("utf-8"), REVIEW_REL)

    completeness_path = ROOT / COMPLETENESS_REL
    if not completeness_path.exists():
        print(f"missing derivation reader: {completeness_path}",
              file=sys.stderr)
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location(
        "_snv5_completeness", completeness_path)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)

    declaration, decl_errors = reader.derivation_declaration(subject)
    effective, provenance, resolve_errors = (None, {}, [])
    if declaration is not None and not decl_errors:
        effective, provenance, resolve_errors = reader.resolve_derivation(
            SUBJECT_REL, declaration)

    resolved_inputs, resolved_raw = _load(RESOLVED_INPUTS_REL,
                                          RESOLVED_INPUTS_REL, required=False)
    _, d9_raw = _load(D9_REL, D9_REL, required=False)
    tiers, tiers_raw = _load(RETENTION_TIERS_REL, RETENTION_TIERS_REL,
                             required=False)

    def _bytes(rel: str) -> bytes:
        path = ROOT / rel
        return path.read_bytes() if path.exists() else b""

    env = {
        "subject": subject,
        "predecessor": predecessor,
        "review": review,
        "resolvedInputs": resolved_inputs,
        "resolvedInputsBytes": resolved_raw,
        "d9Bytes": d9_raw,
        "retentionTiers": tiers,
        "retentionTiersBytes": tiers_raw,
        "retentionCheckerBytes": _bytes(RETENTION_CHECKER_REL),
        "threatClaimsBytes": _bytes(THREAT_CLAIMS_REL),
        "derivation": {
            "declaration": declaration,
            "declErrors": list(decl_errors),
            "resolveErrors": list(resolve_errors),
            "provenance": provenance,
        },
        "readerDigest": hashlib.sha256(
            completeness_path.read_bytes()).hexdigest(),
    }
    return effective, env


# ============================================================= SNV5-B residual
#
# The instrument measures its OWN negation hole, every run, over exactly the
# universe the review used: the prose leaves of `$.storageNamespace` longer than
# 25 characters.  Two probes per leaf:
#
#   REPLACE  -- the leaf becomes a placeholder.  Firing means the position is
#               bound at all.
#   APPEND   -- the leaf keeps every byte and gains a reversal.  NOT firing
#               means the position is defeatable the way CIR-B2 describes.
#
# `RESIDUAL_BOUND` is the number measured against these exact pinned bytes.
# Exceeding it is a FINDING, not a note: freeze 7.2.2's rider is that a
# measurement which cannot fail the build is prose.
LEAF_MIN_CHARS = 25
RESIDUAL_SCOPE = "storageNamespace"
RESIDUAL_PROBE = (" However this rule does not apply and the opposite is "
                  "permitted; the statement above is withdrawn.")
# Measured against SUBJECT_SHA by `--selftest` and by every default run.  The
# predecessor's figure on the same universe, re-derived from the review at
# `escapesFound[ESC-06]`, was 63.
RESIDUAL_BOUND = 0


def _prose_leaves(effective) -> list:
    scope = effective.get(RESIDUAL_SCOPE) if isinstance(effective, dict) else None
    if not isinstance(scope, dict):
        return []
    return [(path, value)
            for path, value in _strings(scope, RESIDUAL_SCOPE)
            if len(value) > LEAF_MIN_CHARS]


def _set_at(root, path: str, value) -> None:
    steps = [(int(a) if a else b) for a, b in STEP_RE.findall(path)]
    node = root
    for step in steps[:-1]:
        node = node[step]
    node[steps[-1]] = value


def residual_sweep(effective, env) -> dict:
    """The measurement this instrument publishes about itself."""
    leaves = _prose_leaves(effective)
    unbound, defeatable = [], []
    for path, value in leaves:
        one = copy.deepcopy(effective)
        _set_at(one, path, "PLACEHOLDER")
        replaced = check(one, env)
        two = copy.deepcopy(effective)
        _set_at(two, path, value + RESIDUAL_PROBE)
        appended = check(two, env)
        if not replaced:
            unbound.append(path)
        if not appended:
            defeatable.append(path)
    return {
        "universe": len(leaves),
        "unbound": unbound,
        "defeatable": defeatable,
        "hole": [p for p in defeatable if p not in set(unbound)],
    }


def _residual_findings(measured: dict) -> list:
    count = len(measured["hole"])
    if count <= RESIDUAL_BOUND:
        return []
    return [
        f"SNV5-B residual: {count} position(s) are bound by this instrument "
        f"yet accept a needle-preserving appended reversal with 0 findings, "
        f"above the published bound of {RESIDUAL_BOUND}: "
        f"{sorted(measured['hole'])[:8]}{' ...' if count > 8 else ''}"
    ]


# ============================================================= observations
def observations(effective, env) -> list:
    """Measured facts a coordinator must carry forward.  Not findings: this
    instrument closes no row and changes no disposition."""
    notes: list = []
    namespace = effective.get("storageNamespace", {})
    root_binding = namespace.get("rootBinding", {})
    statement = text_of(_safe(root_binding, "properties.SN-P3.statement"))
    layout = namespace.get("layout", {})
    journal = layout.get("purgeJournal", "") if isinstance(layout, dict) else ""

    # SNV4R-NB-01, COMPUTED rather than quoted, carried forward from the
    # predecessor -- the review graded this "the single best-engineered
    # observation I found in either instrument" and exercised both retirement
    # branches.  Kept byte-for-byte in behaviour.
    marker = "<admittedStorageRoot>/control/"
    depth = journal[len(marker):].count("/") if journal.startswith(marker) else -1
    tail = statement.split("every directory beneath")[-1] \
        if "every directory beneath" in statement else ""
    granted = "control/" in tail
    reach = text_of(_safe(root_binding,
                          "renameAtomicity.reachOfTheAdmissionScan"))
    disclosed = "control" in reach
    pairs = _safe(root_binding, "renameAtomicity.derivedOperandPairs") or []
    if granted or disclosed:
        notes.append(
            "SNV5-OBS-SCAN-DEPTH: the control/ scan bound is now "
            + ("scanned recursively" if granted
               else "disclosed at renameAtomicity.reachOfTheAdmissionScan")
            + "; review finding SNV4R-NB-01 no longer reproduces against these "
              "bytes.")
    elif depth >= 0:
        notes.append(
            f"SNV5-OBS-SCAN-DEPTH (review SNV4R-NB-01, NON-BLOCKING, owner "
            f"coordinator): SN-P3's scan is recursive for projects/ and "
            f"quarantine/ and one directory deep for control/, while "
            f"layout.purgeJournal sits {depth} directory level(s) below "
            f"control/ at {journal!r}. Protecting that journal is the reason "
            f"whyControlIsInScope gives for control/ being in scope at all. "
            f"The rename operand set is fully covered -- all {len(pairs)} "
            f"derived operand pairs have both endpoints under projects/ or "
            f"quarantine/ -- so the blocker IS repaired; what is missing is "
            f"the DISCLOSURE of this bound at "
            f"renameAtomicity.reachOfTheAdmissionScan, where two comparable "
            f"bounds (file-level bind mount, post-admission mount) already are "
            f"disclosed.")
    else:
        notes.append(
            "SNV5-OBS-SCAN-DEPTH: layout.purgeJournal does not sit beneath "
            "<admittedStorageRoot>/control/, so the SNV4R-NB-01 scan-depth "
            "measurement does not apply to these bytes and is not reported.")

    # The grade of every bound position, reported rather than asserted: which
    # satisfier actually fired.  versioning-policy.v10's MEASURED/GROUNDED
    # vocabulary, applied to this instrument's own coverage.
    grades = env.get("grades") or {}
    if grades:
        literal = sum(1 for v in grades.values() for _, how in v
                      if how == "literal")
        terms = sum(1 for v in grades.values() for _, how in v
                    if how == "terms")
        notes.append(
            f"SNV5-OBS-GRADE: {len(grades)} bound position(s) carrying "
            f"{literal + terms} claim(s); {literal} satisfied by the literal "
            f"anchor the predecessor used and {terms} by normalised terms. A "
            "claim satisfied by terms is one a lawful rewording may restate; a "
            "claim satisfied only by its anchor is one a lawful rewording would "
            "break, and that is the FP-01 cost, disclosed rather than hidden.")

    notes.append(
        "SNV5-OBS-UNENFORCED-ELSEWHERE: this checker binds rootBinding at the "
        "SPECIFICATION level only. rootBinding.observabilityBoundary is "
        "correct that whether a built host honours SN-P1..SN-P5 is a G14-class "
        "runtime property no instrument in this corpus can observe. Nothing "
        "here clears the TM row, whose two other conditions are untouched, and "
        "CD-RT-5 remains BLOCKED_ON_PHASE_1A.")
    notes.append(
        "SNV5-OBS-DISCLOSURE-SCOPE: rootBinding.fixtures.enforcementDisclosure "
        "scopes its non-enforcement claim to check-threat-claims.py, whose "
        "T13 closed-set equality over storageNamespace.fixtures still would "
        "reject an addition there. Measured this run: that file contains "
        f"{env.get('threatClaimsBytes', b'').count(b'rootBinding')} "
        "occurrence(s) of 'rootBinding', so the sentence remains true of that "
        "checker and is not made stale by this file.")
    notes.append(
        "SNV5-OBS-BOUND: what a green run here means, stated so a signer need "
        "not infer it. The bytes are the reviewed bytes and drift stops the "
        "run; everything recomputable was recomputed and agrees; the prose has "
        "not been gutted; and -- new here -- no bound claim is contradicted by "
        "a clause in its own property, no ordering relation is inverted, the "
        "dispositive field agrees with the decider, and the claims that are "
        "facts about disk were measured on disk. It does NOT mean the prose is "
        "true. A companion instrument written after the artifact is still a "
        "second opinion from a closely related mind (freeze 7.8).")
    return notes


# =============================================================== mutations
#
# freeze 7.4 records that a non-zero exit is not evidence a guard fired, so the
# selftest asserts a SPECIFIC finding by ID prefix and prints it.  freeze 7.8's
# correction is the reason for the second block: every instrument this session
# fired on REMOVAL and stayed silent on FALSITY, so for each of the five
# properties there is a mutation that keeps every required substring and inverts
# the meaning, and it must fail.
def _rb(state):
    return state["effective"]["storageNamespace"]["rootBinding"]


def _prop(state, pid):
    return _rb(state)["properties"][pid]


# ---- block 1: removal and shape, carried forward from the predecessor -------
def _gut_properties(state):
    for pid in PROPERTY_IDS:
        node = _prop(state, pid)
        for key in list(node):
            if key != "title":
                node[key] = "TBD"


def _delete_root_binding(state):
    del state["effective"]["storageNamespace"]["rootBinding"]


def _drop_argument_position(state):
    node = _prop(state, "SN-P1")
    node["statement"] = node["statement"].replace(
        "argument position by which a root may be supplied", "path")


def _drop_byte_equality(state):
    _prop(state, "SN-P1")["dispositiveVersusAdvisory"] = \
        "The locator names where the bytes are."


def _demote_unary_authority(state):
    state["effective"]["storageNamespace"]["authority"] = \
        "Resolution compares the offered location against the record."


def _refuse_move_and_copy_alike(state):
    for vector in _rb(state)["fixtures"]["vectors"]:
        if vector["id"] == "accept-root-move-with-bound-locator-absent":
            vector["expected"] = "STORAGE_ROOT_COLLISION"


def _swap_vector_property(state):
    for vector in _rb(state)["fixtures"]["vectors"]:
        if vector["id"] == "reject-copied-root-two-live-locators":
            vector["violates"] = "SN-P1"


def _drop_a_vector(state):
    del _rb(state)["fixtures"]["vectors"][2]


def _vector_valid_as_integer(state):
    _rb(state)["fixtures"]["vectors"][0]["valid"] = 0


def _schema_version_as_boolean(state):
    _rb(state)["schemaVersion"] = True


def _add_a_predicate(state):
    node = state["effective"]["storageNamespace"]["pathSafety"]
    node["unsupported"] = node["unsupported"].replace(
        "fsync or SQLite semantics", "fsync, same-device rename or SQLite "
        "semantics")


def _bind_an_errno(state):
    node = _prop(state, "SN-P3")
    node["statement"] += " A cross-device operand pair is refused with EXDEV."


def _drop_rename_precondition(state):
    node = state["effective"]["storageNamespace"]["pathSafety"]
    node["resolution"] = node["resolution"].replace(
        "atomically rename only within one admitted root whose layout-derived "
        "rename operand set satisfies rootBinding.properties.SN-P3",
        "atomically rename within the root")


def _branch_the_state_machine(state):
    ordering = state["effective"]["storageNamespace"][
        "inventoryPurgeMigration"]["purge"]["operationOrdering"]
    ordering[1] += " If the operands span a device, refuse."


def _seventh_purge_row(state):
    state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "purge"]["crashRecoveryTable"].append(
            {"observed": "PREPARED|canonical-present|quarantine-present",
             "action": "refuse-cross-device", "nextState": "PREPARED"})


def _drop_migration_row(state):
    del state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "migration"]["crashRecoveryTable"][0]


def _sixth_property(state):
    _rb(state)["properties"]["SN-P6"] = {"title": "extra", "statement": "extra"}


def _undefined_outcome(state):
    _rb(state)["outcomes"]["closedValues"].append("STORAGE_ROOT_SURPRISE")


def _undeclared_definition(state):
    _rb(state)["outcomes"]["definitions"]["STORAGE_ROOT_SURPRISE"] = {
        "meaning": "x", "provenance": "callerOrConfig", "raisedBy": "SN-P1"}


def _phantom_raised_by(state):
    _rb(state)["outcomes"]["definitions"]["STORAGE_ROOT_UNVERIFIED"][
        "raisedBy"] = "admittedStorageRoot.thisDoesNotExist"


def _rename_an_outcome(state):
    values = _rb(state)["outcomes"]["closedValues"]
    values[values.index("STORAGE_ROOT_COLLISION")] = "STORAGE_ROOT_DUPLICATE"


def _operand_pair_layout_does_not_produce(state):
    _rb(state)["renameAtomicity"]["derivedOperandPairs"][0][
        "targetLayoutKey"] = "cache"


def _drop_an_operand_pair(state):
    del _rb(state)["renameAtomicity"]["derivedOperandPairs"][1]


def _per_root_authority_record(state):
    state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "migration"]["authorityRecordPath"] = \
        "<admittedStorageRoot>/control/storage-authority/<ProjectId>.json"


def _shrink_a_closed_list(state):
    state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "purge"]["reachableDurableNonterminalStates"].pop()


def _permit_physical_locators(state):
    state["env"]["retentionTiers"]["partB_purgeSemantics"][
        "effectiveCapabilityDerivation"]["forbiddenInputs"].remove(
            "physicalLocators")


def _couple_retention_to_namespace(state):
    state["env"]["retentionCheckerBytes"] += b"\n# storageNamespace\n"


def _mint_a_d9_class(state):
    state["env"]["d9Bytes"] += b"\nSTORAGE_ROOT_COLLISION\n"


def _stale_checker_impact_map(state):
    state["env"]["subject"]["checkerImpact"][
        "whatASuccessorCheckerMUSTaddBeforeTheNewMaterialIsMECHANICALLYbound"] \
        .pop()


def _paper_seal_lazily(state):
    _rb(state)["fixtures"]["enforcementDisclosure"] = \
        "These vectors are enforced."


# ---- block 2: FALSITY.  Every needle survives; the meaning is inverted. -----
def _p1_append_retraction(state):
    node = _prop(state, "SN-P1")
    node["statement"] += (
        " That said, a host MAY also accept a caller-supplied root on an "
        "additional argument position, and in that case resolution is not a "
        "total function of exactly one input.")


def _p1_frame_negation(state):
    node = _prop(state, "SN-P1")
    node["statement"] = "It is NOT the case that " + node["statement"]


def _p1_invert_dispositive(state):
    node = _prop(state, "SN-P1")
    node["dispositiveVersusAdvisory"] += (
        " On reflection activeRootCanonicalPath is dispositive and decides "
        "which root is authoritative; activeRootId is advisory only.")


def _p1_readd_argument_position(state):
    node = _prop(state, "SN-P1")
    node["whyThisIsStructuralAndNotASiteList"] += (
        " An argument position by which a root may be supplied is retained "
        "for compatibility with existing callers.")


def _p2_downgrade_function(state):
    node = _prop(state, "SN-P2")
    node["statement"] += (
        " The relation is nevertheless advisory only, and two live records may "
        "name one activeRootId at two different canonical locators.")


def _p2_select_anyway(state):
    node = _prop(state, "SN-P2")
    node["openTimeDetection"] += (
        " In practice one of the two roots is selected and opened, and its "
        "authority record is read for resolution.")


def _p3_exempt_the_barrier(state):
    node = _prop(state, "SN-P3")
    node["statement"] += (
        " The check is exempt until after the first user-derived durable "
        "write, and mount points within that scope are tolerated.")


def _p3_extend_to_cas(state):
    node = _prop(state, "SN-P3")
    node["admissionCost"] += " The predicate also ranges over CAS objects."


def _p4_last_writer_wins(state):
    node = _prop(state, "SN-P4")
    node["statement"] += (
        " Where create-new is unavailable the record is written "
        "last-writer-wins, overwriting any existing generation-1 record.")


def _p4_invert_ordering(state):
    node = _prop(state, "SN-P4")
    node["ordering"] += (
        " In this ordering the namespace precedes the record: "
        "projects/<ProjectId> is created first and the generation-1 record "
        "afterwards.")


def _p5_permit_reserved_target(state):
    node = _prop(state, "SN-P5")
    node["statement"] += (
        " A migration install rename onto a target the journal already "
        "reserved is permitted and silently overwrites the existing namespace.")


def _observability_claims_runtime(state):
    _rb(state)["observabilityBoundary"]["rule"] += (
        " This instrument does in fact observe runtime conformance of "
        "SN-P1..SN-P5 on a built host, and the G14 gate is discharged.")


def _paper_seal_carefully(state):
    _rb(state)["fixtures"]["enforcementDisclosure"] += (
        " In fact these vectors ARE enforced by check-threat-claims.py today "
        "and no successor checker work is required.")


def _retract_a_property(state):
    node = _prop(state, "SN-P2")
    node["statement"] += " For hosted deployments this rule does not apply."


def _misattach_dispositive(state):
    state["effective"]["storageNamespace"]["authority"] = \
        state["effective"]["storageNamespace"]["authority"].replace(
            "activeRootId is dispositive and activeRootCanonicalPath is an "
            "advisory locator only",
            "activeRootCanonicalPath is dispositive and activeRootId is an "
            "advisory locator only")


# ---- block 3: recorded measurements and published corpora ------------------
def _fabricate_an_input_digest(state):
    for entry in state["env"]["subject"]["verifiedInputs"]["files"]:
        if entry["path"] == RESOLVED_INPUTS_REL:
            entry["sha256Measured"] = "f" * 64


def _falsify_a_subtree_digest(state):
    state["env"]["subject"]["predecessor"]["subtreeDigestsReproduced"][
        "sortKeysCompact"]["sha256"] = "0" * 64


def _falsify_a_subtree_byte_count(state):
    state["env"]["subject"]["predecessor"]["subtreeDigestsReproduced"][
        "defaultSeparators"]["bytes"] = 1


def _falsify_the_predecessor_digest(state):
    state["env"]["subject"]["predecessor"]["sha256RecomputedAtAuthoring"] = \
        "a" * 64


def _falsify_an_occurrence_count(state):
    state["env"]["subject"]["selfVerification"][
        "measurementsReproducedBeforeBeingRelliedOn"]["exdevInTheSubtree"] = \
        "Re-measured: 'EXDEV' occurs 4 times in artifacts/threat-model.v3.json."


def _collapse_two_vectors(state):
    vectors = _rb(state)["fixtures"]["vectors"]
    vectors[1]["scenario"] = vectors[0]["scenario"]


def _collapse_two_definitions(state):
    definitions = _rb(state)["outcomes"]["definitions"]
    definitions["STORAGE_ROOT_COLLISION"]["meaning"] = \
        definitions["STORAGE_ROOT_LOCATOR_STALE"]["meaning"]


def _break_a_correspondence(state):
    _rb(state)["identityOwnerAgreement"]["correspondence"][0][
        "ownerPointer"] = "suppliedVersusPersisted.thisDoesNotExist"


def _duplicate_a_property_statement(state):
    properties = _rb(state)["properties"]
    properties["SN-P5"]["statement"] = properties["SN-P4"]["statement"]


def _change_the_gate(state):
    state["env"]["subject"]["assurance"]["gateIds"] = ["G14", "G2"]


def _upgrade_the_evidence_grade(state):
    state["env"]["subject"]["assurance"]["evidenceGrade"] = "DEMONSTRATED"


MUTATIONS = (
    # ---- removal and shape ----
    ("gut every rootBinding property to placeholders", _gut_properties,
     "SNV5-P1"),
    ("delete rootBinding entirely", _delete_root_binding, "SNV5-P0"),
    ("SN-P1: replace 'argument position' with a site", _drop_argument_position,
     "SNV5-P1"),
    ("SN-P1: replace dispositiveVersusAdvisory wholesale", _drop_byte_equality,
     "SNV5-P1"),
    ("demote resolution from unary to a comparison", _demote_unary_authority,
     "SNV5-U"),
    ("SN-P2: refuse a moved root the same way as a copied one",
     _refuse_move_and_copy_alike, "SNV5-V"),
    ("SN-P2: attribute the collision vector to the wrong property",
     _swap_vector_property, "SNV5-V"),
    ("drop the copied-root vector", _drop_a_vector, "SNV5-V"),
    ("publish a vector's `valid` as integer 0", _vector_valid_as_integer,
     "SNV5-T"),
    ("publish rootBinding.schemaVersion as boolean true",
     _schema_version_as_boolean, "SNV5-T"),
    ("SN-P3: add an eighth capability predicate", _add_a_predicate, "SNV5-P3"),
    ("SN-P3: bind the rule to EXDEV", _bind_an_errno, "SNV5-P3"),
    ("SN-P3: drop the rename precondition from pathSafety.resolution",
     _drop_rename_precondition, "SNV5-P3"),
    ("SN-P3: branch a purge ordering step on device", _branch_the_state_machine,
     "SNV5-P3"),
    ("add a seventh purge recovery row", _seventh_purge_row, "SNV5-C"),
    ("drop a migration recovery row", _drop_migration_row, "SNV5-C"),
    ("add a sixth property SN-P6", _sixth_property, "SNV5-P0"),
    ("admit an outcome with no definition", _undefined_outcome, "SNV5-X"),
    ("define an outcome that is not admitted", _undeclared_definition,
     "SNV5-X"),
    ("point raisedBy at a position that does not resolve", _phantom_raised_by,
     "SNV5-X"),
    ("rename an outcome the decider still produces", _rename_an_outcome,
     "SNV5-X"),
    ("declare an operand pair the layout does not produce",
     _operand_pair_layout_does_not_produce, "SNV5-R"),
    ("drop a declared operand pair the state machines still perform",
     _drop_an_operand_pair, "SNV5-R"),
    ("site the authority record inside an admitted root",
     _per_root_authority_record, "SNV5-U"),
    ("shrink a closed collection the derivation must not touch",
     _shrink_a_closed_list, "SNV5-S"),
    ("let physicalLocators reach effective_capability",
     _permit_physical_locators, "SNV5-N"),
    ("couple the retention checker to storageNamespace",
     _couple_retention_to_namespace, "SNV5-N"),
    ("mint a D9 class from a rootBinding outcome", _mint_a_d9_class, "SNV5-X"),
    ("drop a checkerImpact assertion this map claims to discharge",
     _stale_checker_impact_map, "SNV5-K"),
    ("paper-seal the disclosure the LAZY way (text replaced)",
     _paper_seal_lazily, "SNV5-P0"),

    # ---- FALSITY: every needle survives, the meaning is inverted ----
    ("SN-P1 FALSE: keep every needle, append a retraction",
     _p1_append_retraction, "SNV5-M"),
    ("SN-P1 FALSE: prepend 'It is NOT the case that'", _p1_frame_negation,
     "SNV5-M"),
    ("SN-P1 FALSE: invert which record field decides", _p1_invert_dispositive,
     "SNV5-M"),
    ("SN-P1 FALSE: re-add the argument position in a sibling key",
     _p1_readd_argument_position, "SNV5-M"),
    ("SN-P2 FALSE: downgrade the FUNCTION to a hint", _p2_downgrade_function,
     "SNV5-M"),
    ("SN-P2 FALSE: select a root anyway", _p2_select_anyway, "SNV5-M"),
    ("SN-P3 FALSE: exempt the durable-write barrier", _p3_exempt_the_barrier,
     "SNV5-M"),
    ("SN-P3 FALSE: extend the scan to CAS objects", _p3_extend_to_cas,
     "SNV5-M"),
    ("SN-P4 FALSE: replace compare-and-swap with last-writer-wins",
     _p4_last_writer_wins, "SNV5-M"),
    ("SN-P4 FALSE: invert record-before-namespace", _p4_invert_ordering,
     "SNV5-M"),
    ("SN-P5 FALSE: permit the reserved-target rename",
     _p5_permit_reserved_target, "SNV5-M"),
    ("observabilityBoundary FALSE: claim runtime IS observed, G14 discharged",
     _observability_claims_runtime, "SNV5-E"),
    ("paper-seal the disclosure the CAREFUL way (text kept, reversal appended)",
     _paper_seal_carefully, "SNV5-E"),
    ("SN-P2 FALSE: retract the rule by reference", _retract_a_property,
     "SNV5-M"),
    ("authority FALSE: attach 'dispositive' to the advisory field",
     _misattach_dispositive, "SNV5-M"),

    # ---- recorded measurements and published corpora ----
    ("fabricate a recorded input digest", _fabricate_an_input_digest,
     "SNV5-W"),
    ("falsify a re-derived subtree digest", _falsify_a_subtree_digest,
     "SNV5-W"),
    ("falsify a re-derived subtree byte count", _falsify_a_subtree_byte_count,
     "SNV5-W"),
    ("falsify the recorded predecessor digest", _falsify_the_predecessor_digest,
     "SNV5-W"),
    ("falsify a recorded occurrence count", _falsify_an_occurrence_count,
     "SNV5-W"),
    ("collapse two published vectors to one scenario", _collapse_two_vectors,
     "SNV5-G"),
    ("collapse two outcome definitions to one meaning",
     _collapse_two_definitions, "SNV5-G"),
    ("point a correspondence at a pointer the owner does not publish",
     _break_a_correspondence, "SNV5-G"),
    ("publish two properties with one statement",
     _duplicate_a_property_statement, "SNV5-G"),
    ("widen the declared gate set", _change_the_gate, "SNV5-E"),
    ("upgrade the declared evidence grade", _upgrade_the_evidence_grade,
     "SNV5-E"),
)


# ---- CONTROLS: lawful rewordings that must produce ZERO findings -----------
#
# FP-01 measured 3 of 3 lawful, meaning-preserving rewordings REJECTED by the
# predecessor.  A checker that cannot be improved without being edited freezes
# the prose it guards, and a successor artifact that improves a bound sentence
# must not be forced to fail.  These three are the reviewer's own cases.
def _reword_p4_ordering(state):
    _prop(state, "SN-P4")["ordering"] = (
        "Admit the root (SN-P2, SN-P3) -> create the generation-1 record "
        "naming its rootId -> create projects/<ProjectId>. The namespace is "
        "created only after the record exists, never before, so a namespace "
        "can never exist for a ProjectId whose record does not name the root "
        "it sits under, which is exactly the condition SN-P5 refuses.")


def _reword_p1_consumer(state):
    _prop(state, "SN-P1")["consumerConsequence"] = (
        "activeRootId acquires a consumer by construction rather than by "
        "enumeration: the authority record is the only thing that produces the "
        "root half of any canonical path the layout defines. A durable field "
        "with no reader cannot enforce an isolation boundary; a field that is "
        "the only producer of a value cannot fail to be read without the value "
        "failing to exist.")


def _reword_p3_cost(state):
    _prop(state, "SN-P3")["admissionCost"] = (
        "Bounded by the layout and by the number of projects and in-flight "
        "operations, the predicate ranges over directories only. It never "
        "ranges over content-addressed objects, so admission does not become "
        "linear in stored evidence.")


CONTROLS = (
    ("SN-P4.ordering reworded, meaning preserved", _reword_p4_ordering),
    ("SN-P1.consumerConsequence reworded, meaning preserved",
     _reword_p1_consumer),
    ("SN-P3.admissionCost reworded, meaning preserved", _reword_p3_cost),
)


# ---- DISCLOSED RESIDUAL: reversals this instrument does NOT catch ----------
#
# Published as a measurement, never as a claim that CIR-B2 is closed.  Each
# case below reverses a property while (a) naming none of the terms the claim
# is bound by, (b) using no retraction vocabulary and (c) opening with no frame
# negation.  All three floors are lexical, so all three are evadable, and the
# honest number is printed by `--selftest` and by the banner.
#
# The selftest FAILS if the measured count differs from this figure in either
# direction: a rise is a regression, and a fall means the disclosure has gone
# stale and is understating what the instrument now catches.
def _evade_p1(state):
    _prop(state, "SN-P1")["statement"] += (
        " A compatibility profile lets an operator name the storage location "
        "directly at call time.")


def _evade_p2(state):
    _prop(state, "SN-P2")["statement"] += (
        " A pair of records naming one identity in separate places is "
        "reconciled by preferring the newest.")


def _evade_p3(state):
    _prop(state, "SN-P3")["statement"] += (
        " Where a subdirectory sits on separate media the operation proceeds "
        "through a copy-and-delete fallback.")


def _evade_p4(state):
    _prop(state, "SN-P4")["statement"] += (
        " Where the platform lacks exclusive creation the newest writer's "
        "content prevails.")


def _evade_p5(state):
    _prop(state, "SN-P5")["statement"] += (
        " An unbound canonical directory found under an admitted root is "
        "absorbed automatically.")


RESIDUAL_CASES = (
    ("SN-P1 reversed without naming any bound term", _evade_p1),
    ("SN-P2 reversed without naming any bound term", _evade_p2),
    ("SN-P3 reversed without naming any bound term", _evade_p3),
    ("SN-P4 reversed without naming any bound term", _evade_p4),
    ("SN-P5 reversed without naming any bound term", _evade_p5),
)
# Measured against SUBJECT_SHA.  5 of 5 escape.  The predecessor escaped these
# too, and additionally escaped all 13 reversals that DO name their terms.
RESIDUAL_EVASIVE_ESCAPES = 5

DUPLICATE_KEY_PROBE = (
    '{"storageNamespace": {"schemaVersion": 1, "rootBinding": '
    '{"schemaVersion": 1, "schemaVersion": 2}}}')


def _apply(effective, env, mutate):
    state = {"effective": copy.deepcopy(effective), "env": copy.deepcopy(env)}
    mutate(state)
    return check(state["effective"], state["env"])


def selftest(effective, env) -> int:
    base = check(effective, env)
    if base:
        print(f"REFUSING to self-test: the subject already has {len(base)} "
              "finding(s)")
        for item in base[:10]:
            print("  -", item)
        return 1
    print("mutation self-test - each row must be REJECTED by its NAMED "
          "family\n")
    escaped = 0
    total = 0

    for name, value in TOTALITY_ROOT_CASES:
        total += 1
        found = check(copy.deepcopy(value), env)
        ok = bool(found)
        escaped += 0 if ok else 1
        print(f"  {'reject' if ok else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {found[0] if found else 'NO FINDING - root survived'}")

    for label, mutate, family in MUTATIONS:
        total += 1
        try:
            found = _apply(effective, env, mutate)
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            print(f"  ESCAPE  {label}")
            print(f"          mutation could not be applied ({exc!r})")
            escaped += 1
            continue
        named = [f for f in found if f.startswith(family)]
        ok = bool(named)
        escaped += 0 if ok else 1
        print(f"  {'reject' if ok else 'ESCAPE':>6}  {label}  [{family}]")
        if named:
            print(f"          {named[0]}")
        elif found:
            print(f"          NO {family} FINDING - only: {found[0]}")
        else:
            print("          NO FINDING - mutation survived")

    total += 1
    _PARSES.clear()
    jloads(DUPLICATE_KEY_PROBE, "<duplicate-key probe>")
    dupes = parse_findings()
    _PARSES.clear()
    ok = any("schemaVersion" in d and "rootBinding" in d for d in dupes)
    escaped += 0 if ok else 1
    print(f"  {'reject' if ok else 'ESCAPE':>6}  duplicate JSON key, named "
          "with its path  [SNV5-A0]")
    print("         ", dupes[0] if dupes
          else "NO FINDING - duplicate key survived")

    print("\ncontrols - each row must produce ZERO findings (FP-01)\n")
    false_positives = 0
    for label, mutate in CONTROLS:
        total += 1
        found = _apply(effective, env, mutate)
        if found:
            false_positives += 1
            escaped += 1
            print(f"  FALSE+  {label}")
            for item in found:
                print(f"          {item}")
        else:
            print(f"  accept  {label}")

    print("\ndisclosed residual - these are EXPECTED to escape, and the count "
          "must match the published figure\n")
    evasive = 0
    for label, mutate in RESIDUAL_CASES:
        found = _apply(effective, env, mutate)
        if not found:
            evasive += 1
        print(f"  {'escapes' if not found else 'caught ':>7}  {label}")
    print(f"\n  measured {evasive}, published RESIDUAL_EVASIVE_ESCAPES = "
          f"{RESIDUAL_EVASIVE_ESCAPES}")
    if evasive != RESIDUAL_EVASIVE_ESCAPES:
        print("  the published residual figure does not match the measurement; "
              "a disclosure that is not re-measured is an attestation")
        escaped += 1
    total += 1

    print("\nresidual sweep - the review's own universe and probe shape\n")
    measured = residual_sweep(effective, env)
    print(f"  universe    {measured['universe']} prose leaves of "
          f"$.{RESIDUAL_SCOPE} longer than {LEAF_MIN_CHARS} characters")
    print(f"  unbound     {len(measured['unbound'])} accept a wholesale "
          "replacement with 0 findings")
    print(f"  defeatable  {len(measured['defeatable'])} accept a "
          "needle-preserving appended reversal with 0 findings")
    print(f"  hole        {len(measured['hole'])} are bound yet defeatable "
          f"(published bound {RESIDUAL_BOUND})")
    residual = _residual_findings(measured)
    total += 1
    if residual:
        escaped += 1
        for item in residual:
            print("  ", item)

    print()
    if escaped:
        print(f"{escaped}/{total} retained cases ESCAPED")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations, "
          f"{len(TOTALITY_ROOT_CASES)} root-shape cases and 1 duplicate-key "
          f"case rejected by the family named for them; {len(CONTROLS)} lawful "
          f"rewordings accepted; residual measured and equal to the published "
          "figure - the assertions are load-bearing in BOTH directions")
    return 0


def main() -> int:
    argv = set(sys.argv[1:])
    effective, env = load_environment()
    if "--selftest" in argv:
        if effective is None:
            print("cannot self-test: the derivation did not resolve",
                  file=sys.stderr)
            for item in env["derivation"]["declErrors"] + \
                    env["derivation"]["resolveErrors"]:
                print("  -", item, file=sys.stderr)
            return 2
        return selftest(effective, env)

    found = check(effective if effective is not None else {}, env)
    measured = None
    if isinstance(effective, dict) and "--no-residual" not in argv:
        measured = residual_sweep(effective, env)
        found = sorted(set(found) | set(_residual_findings(measured)))
    notes = observations(effective, env) if isinstance(effective, dict) else []
    if "--residual" in argv and measured is not None:
        print("residual detail - positions bound yet defeatable:")
        for path in sorted(measured["hole"]):
            print("   ", path)
        print("residual detail - positions bound by nothing here:")
        for path in sorted(measured["unbound"]):
            print("   ", path)
        print()
    if found:
        print(f"{len(found)} finding(s):")
        for item in found:
            print("  -", item)
        if notes:
            print("\n  observations (not findings):")
            for note in notes:
                print("   ", note)
        return 1

    namespace = effective["storageNamespace"]
    root_binding = namespace["rootBinding"]
    provenance = env["derivation"]["provenance"]
    lifecycle = namespace["inventoryPurgeMigration"]
    claims = (sum(len(c) for keys in PROPERTY_CLAIMS.values()
                  for c in keys.values())
              + sum(len(c) for _, _, c in FRAME_CLAIMS))
    guarded = sum(1 for keys in PROPERTY_CLAIMS.values()
                  for claims_ in keys.values() for c in claims_ if c.guard) \
        + sum(1 for _, _, cs in FRAME_CLAIMS for c in cs if c.guard)
    print(f"storage-namespace rootBinding MEANING OK over the EFFECTIVE "
          f"contract - {provenance['predecessor']} at "
          f"{provenance['measuredDigest'][:12]}... + "
          f"{provenance['operations']} operations")
    print(f"  subject      {SUBJECT_REL} @ {SUBJECT_SHA[:12]}... (verified)")
    print(f"  predecessor  {PREDECESSOR_REL} @ {PREDECESSOR_SHA[:12]}... "
          "(verified)")
    print(f"  review       {REVIEW_REL} @ {REVIEW_SHA[:12]}... (verified; the "
          "CIR-B2 figures are read from it, not transcribed)")
    print(f"  reader       {COMPLETENESS_REL} @ {env['readerDigest'][:12]}... "
          "(measured, not pinned - freeze 7.6 records it as editable)")
    print(f"  bound        {len(root_binding['properties'])} properties, "
          f"{claims} claims across "
          f"{len(PROPERTY_CLAIMS) + len(FRAME_CLAIMS)} positions, {guarded} of "
          f"them guarded against a needle-preserving reversal")
    print(f"  derived      {len(root_binding['outcomes']['closedValues'])} "
          "closed outcomes re-derived as the decider's REFUSAL set and each "
          "reached by a constructed world, "
          f"{len(root_binding['fixtures']['vectors'])} vectors decided from "
          f"worlds, "
          f"{len(root_binding['renameAtomicity']['derivedOperandPairs'])} "
          "operand pairs re-derived from layout")
    dispositive, advisory = measure_deciding_field()
    print(f"  measured     read-set {sorted(measure_read_set())}; dispositive "
          f"{sorted(dispositive)}; advisory {sorted(advisory)} - by "
          "discrimination on the reference decider, not read from the prose")
    purge_table = lifecycle["purge"]["crashRecoveryTable"]
    migration_table = lifecycle["migration"]["crashRecoveryTable"]
    migration_domain = {row["observed"].split("|", 1)[0]
                        for row in migration_table}
    print(f"  closure      purge {len(purge_table)} rows over "
          f"{len(lifecycle['purge']['reachableDurableNonterminalStates'])} "
          f"durable nonterminal states, migration {len(migration_table)} rows "
          f"over {len(migration_domain)} (measured each run, hard-compared to "
          "the counts written in prose)")
    additions, removals, changed = [], [], []
    _structural_diff(env["predecessor"], effective, "$", additions, removals,
                     changed)
    lists = sum(1 for _ in _lists(env["predecessor"].get("storageNamespace", {}),
                                  "storageNamespace"))
    print(f"  scope        {len(additions)} addition(s) {additions}, "
          f"{len(removals)} removal(s), {len(changed)} changed prose leaves, "
          f"{lists} predecessor lists byte-identical, purge subtree untouched "
          "- every count re-derived this run, none transcribed")
    if measured is not None:
        print(f"  residual     {len(measured['hole'])} of "
              f"{measured['universe']} positions bound yet defeatable by the "
              f"review's own probe (predecessor: 63); "
              f"{len(measured['unbound'])} bound by nothing here "
              f"(predecessor: 41); and {RESIDUAL_EVASIVE_ESCAPES} of "
              f"{len(RESIDUAL_CASES)} reversals that name none of the bound "
              "terms still escape. CIR-B2 is NARROWED, not closed.")
    print("\n  observations (not findings):")
    for note in notes:
        print("   ", note)
    print("\n  this instrument changes no status, disposition, verdict or "
          "seal, and closes no row. TM remains UNSET - BLOCKS FREEZE and "
          "CD-RT-5 remains BLOCKED_ON_PHASE_1A.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
