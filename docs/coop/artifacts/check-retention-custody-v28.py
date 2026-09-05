#!/usr/bin/env python3
"""Retained checker for retention-tiers.v28.json.

WHY THIS FILE EXISTS.

  retention-tiers.v28.json was independently reviewed ACCEPT AS A CANDIDATE at
  0 blockers and 6 non-blocking observations, and is NOT FIT FOR APPLICATION for
  exactly one reason: IMPLEMENTATION-FREEZE.md section 7.1 grades "no retained
  checker" DISQUALIFYING FOR APPLICATION and no checker reads it.  Section 7.8
  is the licence for this file: A NEW CHECKER IS A NEW FILE AND EDITS NOTHING.

  Its predecessor instrument, check-retention-custody-v27.py, cannot be pointed
  at v28 -- SUBJECT is a constant and argv offers no subject path.  That was
  graded RIGHT twice and it is kept: an instrument carrying frozen id tuples and
  transcribed leaf names must not be pointable at a document it does not
  describe.  The subject below is hard-coded and there is no option to change it.

THE FOUR BLOCKERS OF THE PREDECESSOR, EACH REPRODUCED BEFORE IT WAS REPAIRED.

  B1  chmod 000 on ANY of the eleven declared input sites made the predecessor
      die with an uncaught PermissionError: EMPTY STDOUT, EXIT 1.  Exit 1 is the
      FINDINGS code, so an unreadable input read as a verdict about the artifact.
      Measured: 11 of 11 sites, traceback every time (section 7.8.1, litmus D-6).
      REPAIRED: every filesystem read in this file goes through read_input(),
      which converts OSError into a typed Unavailable rather than an exception.
      measure_all_inputs() cannot raise.  An unreadable REQUIRED input is a
      NAMED refusal at EXIT 2 whose text says THE CHECK DID NOT RUN.

  B2  A DESTROYED ADVANCING input emitted FOUR FALSE ACCUSATIONS against the
      subject.  Measured: an EMPTY IMPLEMENTATION-FREEZE.md gave exit 1 with 7
      findings, among them "RT26-COUNT still fires 2 time(s) against the RESOLVED
      value.  The derivation exists to repair it" -- asserting that the
      artifact's headline repair did not happen.  It did.  The ADVANCING class
      had NO FLOOR: an empty file read as a legitimate advance.
      REPAIRED TWICE, because one repair alone would have been a patch:
        (a) THE ADVANCING CLASS NOW HAS A FLOOR.  An ADVANCING input must still
            be RECOGNISABLE AS ITSELF: non-empty; parseable if it is JSON; and,
            for a document this instrument quotes, carrying at least one of the
            content anchors taken from it.  Below the floor it is not ADVANCING,
            it is DESTROYED IN PLACE, and a destroyed REQUIRED input refuses the
            whole run at exit 2 exactly as an absent one does.  Section 7.8.1
            rule 1: a missing input must refuse, never proceed on a default.
        (b) THE FAMILY GATES ARE DELTA-SCOPED, NOT ABSOLUTE.  The predecessor
            asked "does the family the artifact claims repaired still fire at
            all?"  The right question is "does it still fire AT A PATH THIS
            DERIVATION TOUCHES?"  A finding that also fires against the verified
            predecessor, at a path no operation names, is INHERITED -- it is not
            evidence that a repair did not happen.  This is what makes the false
            accusation impossible rather than merely suppressed, and it is
            strictly stronger: revert a repair and the surviving finding lands
            on an operation path, so the gate fires.

  B3  The documented `--part a|c|d` emitted FALSE FINDINGS -- measured 4, 2 and
      6 extra respectively -- because `part` was forwarded to the executed
      battery and the instrument's OWN gates were not narrowed with it, so
      expectations about families the narrowed battery never ran were compared
      against zero.
      REPAIRED: every gate declares its scope.  The in-scope family set is
      DERIVED by running the reference battery over the VERIFIED PREDECESSOR
      under the same --part and observing which families it produces; an
      expectation about a family outside that set is a NAMED SKIP
      (RT28-PART-SCOPED) and never a finding.  Coverage gates assert only when
      the battery reports having run them.

  B4  check-completeness.py was exec'd UNPINNED, UNRECORDED and UNDECLARED:
      DELETE IT AND THE PREDECESSOR RUN WENT GREEN AT EXIT 0, printing "PASS
      over its RESOLVED VALUE".  A missing executed dependency must never
      produce a pass (section 7.2's recording obligation; section 7.8.1 rule 3).
      A sibling instrument carries the same class from the other side -- a digest
      scraped from an unpinned document.
      REPAIRED: THREE executed modules, each named with its digest in
      EXECUTED_MODULES, each also a member of GATED_PINS, each hash-verified
      before a byte of it is compiled.  There is exactly ONE exec() in this file.
      And the declaration is AUDITED AGAINST THE SOURCE BY AST: audit_execution_edges()
      parses this file with the `ast` module, finds every call to the single
      loader and every bare exec/eval/__import__/importlib edge, and compares the
      literal module paths it finds against EXECUTED_MODULES in BOTH directions.
      --selftest FAILS if the audit and the actual edges disagree.  No gate digest
      in this file is read from an unpinned document.

THE DESIGN REQUIREMENT: RESOLVE, AND KNOW WHERE TO STOP.

  retention-tiers.v28 is a DERIVATION -- eight `set` operations over the
  independently-ACCEPTED retention-tiers.v26.  Section 7.3's 2026-08-06 rider
  measures that consuming instruments read FLAT and therefore cannot read a
  derivation at all: to a flat reader a derivation is indistinguishable from a
  DEFECTIVE artifact.  So this instrument RESOLVES the declaration and ASSERTS
  OVER THE RESOLVED VALUE, never over the delta bytes.

  THE RESOLUTION TERMINUS, AND THIS IS THE SUBTLE PART.  Full-chain
  resolve_derivation REFUSES v28 with 30 errors under BOTH corpus resolvers, and
  THAT IS NOT V28'S DEFECT.  retention-tiers.v26 is a FULL-TEXT STANDALONE whose
  narrative CHANGE-LOG satisfies the shape predicate, so both resolvers classify
  it as an executable derivation over v25: 30 entries, the undeclared verb
  `replace`, and 0 of 30 carrying `value`.  Section 7.3, RESOLVED 2026-08-10 by
  the independent review of v28:

      Resolution terminates at a full-text standalone's REVIEWED BYTES.  A
      predecessor that is itself reviewed IS the base -- resolving THROUGH it
      discards the review.  A resolver should ask whether its predecessor is a
      delta or a terminus, AND THE TERMINUS TEST IS THE REVIEW, NOT THE SHAPE.

  check-retention-custody-v27.py implements the right behaviour BY SHAPE SCREEN
  (its find_declaration requires two distinct digest roles, which v26's
  change-log does not have, so it never recurses).  That is correct by accident
  of shape.  THIS INSTRUMENT IMPLEMENTS THE REVIEW-TERMINUS TEST AND SAYS SO:

    HALF A -- CORPUS DISCOVERY.  Every artifacts/*.json is swept for a document
    that records the candidate predecessor's LIVE byte digest PAIRED IN ONE
    OBJECT with its filename (section 7.2's recording obligation shape), that is
    NOT itself a derivation over that predecessor, and that publishes a
    BLOCKING-FINDING TALLY.  The population count is published.  Standing is
    DISCOVERED, not listed: no review filename appears anywhere in this file.

    HALF B -- DECLARATION VERIFICATION.  The subject's own declaration block
    names a predecessor review and its digest.  That named review must be a
    member of Half A's population, must exist at the declared digest, and must
    report ZERO blocking findings.

  TERMINUS iff both halves agree.  A terminus is NOT recursed into: its reviewed
  bytes are the base.  A non-terminus predecessor IS recursed into.  Both
  branches are exercised by the mutation suite, so neither is dead code.

  The resolved value is a VALUE, not a file.  Its digest is over
  json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':'),
  allow_nan=False).encode('utf-8').  No file with those bytes need ever exist and
  this instrument writes none.

WHAT IS EXECUTED, AND WHY EXECUTING IS NOT TRANSCRIBING.

  Three pinned modules are executed as RUNTIME INPUTS under section 7.3:

    check-retention-custody-v26.py   the reference derivation.  All 20 vectors
                                     and all 24 invariants of the RESOLVED value
                                     are exercised by driving it against a
                                     document it was never pointed at.
    check-completeness.py            resolver 1 -- the resolver the rest of the
                                     corpus references.  Executed, not described.
    check-completeness-v2.py         resolver 2 -- the successor section 7.3's
                                     2026-08-10 rider names.

  A second private copy of a 5000-line reference derivation could disagree with
  the original and NEITHER INSTRUMENT WOULD BE ABLE TO SEE THE DISAGREEMENT --
  which is why check-narrative-packet-agreement.py executes check-package-coherence.py
  rather than reimplementing it, and why this file does the same.  Section 7.8's
  demand -- an instrument must re-derive its constants from the artifact it
  checks -- is met by cross-checking the load-bearing algebra with a SECOND
  implementation written here from the artifact's own published rule text
  (RT28-XCHECK), and by DERIVING every expectation about the delta from the
  artifact's own operation list rather than encoding it.

READ-VS-PIN (section 7.10), CLASSIFIED AND DERIVED RATHER THAN LISTED.

    GATED       Reviewed, frozen or executed bytes no lane may advance.  Drift
                -> RT28-PIN-REFUSED, EXIT 2, nothing parsed or executed.
    ADVANCING   Files the corpus is explicitly waiting to change.  Drift ->
                RT28-PIN-ADVANCED, a NAMED NON-FATAL notice; the run continues
                against LIVE bytes -- BUT ONLY ABOVE THE FLOOR (see B2 above).
    DESTROYED   Standing is MEASURED, never listed.  A digest is DESTROYED when
                no file anywhere under the tree carries it; the sweep that
                establishes that also establishes RESURRECTION, and a file
                appearing at a destroyed digest is a fabrication (EXIT 2).  The
                amendment draft's original 4bbcd6fa... is unrecoverable AND THE
                FILE STILL EXISTS AT c4bd85c6..., MUTATED NOT DELETED -- a reader
                checking only existence misreads it, so both facts are measured
                and both are reported.

ENVIRONMENT PREREQUISITES (section 7.2: a verdict binds bytes AND AN ENVIRONMENT).

  1. CPython 3.9 or later, else RT28-UNSUPPORTED-INTERPRETER, exit 2.
  2. Invoked as `python3 -I -B`, else RT28-UNSUPPORTED-INVOCATION, exit 2.
  3. THE PYTHON STANDARD LIBRARY ONLY.  No third-party package, NO SUBPROCESS,
     no external binary, and in particular no ripgrep.
  4. Every REQUIRED input present, READABLE and ABOVE ITS FLOOR.
  5. The tree may be under concurrent edit.  Every input is re-measured after the
     run; anything that moved is RT28-TREE-MOVED and every finding is republished
     as UNSAFE-TO-ATTRIBUTE.

Exit matrix, distinct by construction:
    0  clean
    1  findings about the artifact
    2  bad invocation, unsupported environment, a REQUIRED input missing /
       unreadable / below its floor, an integrity refusal, or a GATED pin
       mismatch.  THE CHECK DID NOT RUN.
    3  selftest refused or not certifying
    4  the run completed with NAMED CLASSES SKIPPED because a per-class input was
       unavailable or below its floor.  A PARTIAL MEASUREMENT, NEVER A PASS.

Invocation:  python3 -I -B check-retention-custody-v28.py [--selftest]
                                                          [--part a|c|d|all]
                                                          [--limits]
                                                          [--falsification]
             There is deliberately NO option to name a subject.
"""

from __future__ import annotations

import sys

MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write(
        "RT28-UNSUPPORTED-INTERPRETER: this instrument requires CPython "
        f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later and found "
        f"{sys.version_info[0]}.{sys.version_info[1]}.  THE CHECK DID NOT RUN; "
        "no statement about retention-tiers.v28.json is made by this exit.\n")
    raise SystemExit(2)

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "RT28-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-retention-custody-v28.py`.  Caller-owned isolated startup is the "
        "prevention boundary; script code cannot undo interpreter or site "
        "activity that happened before line 1.  THE CHECK DID NOT RUN.\n")
    raise SystemExit(2)

import ast
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

# ---------------------------------------------------------------------------
# THE SUBJECT IS A CONSTANT.  There is no --subject option and argv accepts no
# path.  Section 7.2.2 and the two gradings of the predecessor's identical
# choice: an instrument carrying frozen id tuples and transcribed leaf names must
# not be pointable at a document it does not describe.  Pointing this file at
# anything else is not supported, and the way to check a different artifact is a
# different file.
# ---------------------------------------------------------------------------
SUBJECT = "retention-tiers.v28.json"
SUBJECT_SHA256 = "e622b3cc19ba6a550348d849eedf5867e27a0302800b5b705a57e3bb611f9de2"
SUBJECT_BYTES = 148646

# ---------------------------------------------------------------------------
# EXECUTED MODULES.  Blocker 4's repair, stated in ONE place and audited against
# this file's own source by AST at --selftest.  Every member is also a member of
# GATED_PINS below, so every one is hash-verified before it is compiled, and a
# missing or drifted member refuses the whole run at exit 2.  The predecessor
# exec'd check-completeness.py with none of that and went GREEN when it was
# deleted.
# ---------------------------------------------------------------------------
EXECUTED_MODULES = {
    "artifacts/check-retention-custody-v26.py":
        "the reference derivation: 20 vectors and 24 invariants, driven against "
        "the RESOLVED value and against the verified predecessor",
    "artifacts/check-completeness.py":
        "RESOLVER 1, the resolver the rest of the corpus references; executed "
        "rather than described",
    "artifacts/check-completeness-v2.py":
        "RESOLVER 2, the successor section 7.3's 2026-08-10 rider names",
}

# ---------------------------------------------------------------------------
# GATED.  The six rows retention-tiers.v28.json marks
# HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN at
# $.recordedInputsOfThisDeltaFile.recorded[].gate, PLUS this instrument's own
# executed closure.  check_recorded_inputs compares the two tables in BOTH
# directions on every run, so a row that silently changes class is a finding and
# a row this instrument gates that the artifact does not record is named as
# INSTRUMENT-OWNED rather than passed over.  Section 7.2: a count is not a
# record, so every member is named with its digest.
# ---------------------------------------------------------------------------
GATED_PINS = {
    "artifacts/retention-tiers.v26.json":
        "a6546408fb38df95166f0ec41b1d9d9dae0dbda580684ff8a6e94f57145ad97e",
    "artifacts/retention-tiers.v27.json":
        "d39800b7595f58ab42a65316d4880754ef9a14022d52f7ca68fdbab423e7314c",
    "artifacts/retention-tiers.v26.review-independent.json":
        "ffd8a80d5d7a9273e04192d467fdc5d6a063d8201186c73be2fb0a9115aff916",
    "artifacts/check-completeness.py":
        "6c52a5f9a4ac6a3ec3dae9fb0c87e82552744b18eb8cc38d1c4522ade3e549d6",
    "artifacts/check-completeness-v2.py":
        "b08824e86ea22720bdea649cdc663a39ef6d1fc483adfa6aa49cc19dc8666dd7",
    "artifacts/check-retention-custody-v27.py":
        "cebddeddfd09633e426b8ced16db745f68447ba9fe06cbbffbcb204eaaeba77e",
    # INSTRUMENT-OWNED: not one of the artifact's recorded inputs.  It is this
    # file's executed reference derivation and section 7.3 requires it to be
    # hash-verified before execution.
    "artifacts/check-retention-custody-v26.py":
        "7402759ff6d2b1378b61d4d76727648aebf216795dce965e37c2acf7647d18b9",
}

# The one row of GATED_PINS the artifact does not record, named here so the
# both-directions comparison can report it as OWNED rather than as UNGUARDED.
INSTRUMENT_OWNED_GATES = ("artifacts/check-retention-custody-v26.py",)

# ---------------------------------------------------------------------------
# ADVANCING.  The seven rows retention-tiers.v28.json marks
# CITED-DIGEST-RECORDED-NOT-GATED.  The recorded digests are THE ARTIFACT'S,
# deliberately left as v28 wrote them: they are the baseline a drift notice
# prints against, and replacing them with today's values would erase the record
# rather than check it (section 7.10).
# ---------------------------------------------------------------------------
ADVANCING_PINS = {
    "IMPLEMENTATION-FREEZE.md":
        "198895b088f5b744527b380b79d2748a3996b571d8ad82f844ed9ac35851d99b",
    "IMPLEMENTER-BLUEPRINT.md":
        "94e773e548be73e8f930e8f82c8f252653a42a0728c4fa376cb35542efc526b9",
    "artifacts/c2-plan-stage-schema.v5.json":
        "fe5748963db1724123dbc82b2381feb708d8f3836de6f99e10ca3134534547bd",
    "artifacts/delivery.v3.json":
        "01f1b95d0c740580c9307c188e4c2f6806f4d2e7e54d458f570631734cb62a6d",
    "artifacts/threat-model-storage-namespace.v4.json":
        "94b68f6d504967b61c9daf4884cad90d2e5de63af3b40aeda99d28b59513b5be",
    "artifacts/v10-disposition.v2.json":
        "843e6528e128baa621169e4840d62eb4d82f0912eb305d53c276c178df129bd5",
    "artifacts/versioning-policy.v14.json":
        "39e3f41bafc7603b71441edb41a19834925d7a905d2afba88cada653fbc3cff9",
}

# ---------------------------------------------------------------------------
# REQUIRED.  A required input that is absent, unreadable or below its floor
# refuses the WHOLE run at exit 2.  Everything else skips only the classes that
# read it, by name, at exit 4 (section 7.8.1 rule 2 -- a blanket stop when five
# of six classes could still run throws away real coverage).
#
# This set is DERIVED: every GATED pin (the resolution and the executed closure
# rest on all of them) plus IMPLEMENTATION-FREEZE.md, which this instrument
# quotes and whose anchors gate the rules it enforces.
# ---------------------------------------------------------------------------
def required_inputs() -> tuple:
    """DERIVED from what the run cannot proceed without, and stated per member:
      * every GATED pin -- the resolution and the executed closure rest on all of
        them, and the three executed modules are among them;
      * IMPLEMENTATION-FREEZE.md -- this instrument quotes it and its anchors
        gate the rules being enforced;
      * IMPLEMENTER-BLUEPRINT.md -- NOT because this file reads it, but because
        the hash-verified reference derivation declares it among its own inputs
        and reads it with a bare read_bytes().  Classifying it per-class here and
        letting the executed module refuse on it at exit 2 would be two
        classifications of one file, which is the disagreement this instrument
        exists to catch elsewhere.
    """
    return tuple(GATED_PINS) + ("IMPLEMENTATION-FREEZE.md",
                                "IMPLEMENTER-BLUEPRINT.md")


# The class each non-required ADVANCING input feeds, so a skip can be named.
PER_CLASS_INPUTS = {
    "artifacts/c2-plan-stage-schema.v5.json": "pathEncodingCorroboration",
    "artifacts/delivery.v3.json": "pathEncodingCorroboration",
    "artifacts/threat-model-storage-namespace.v4.json": "pathEncodingCorroboration",
    "artifacts/v10-disposition.v2.json": "pathEncodingCorroboration",
    "artifacts/versioning-policy.v14.json": "pathEncodingCorroboration",
}

# ---------------------------------------------------------------------------
# DESTROYED.  NOT a literal membership test.  The predecessor lineage was faulted
# for `if name in UNSATISFIABLE_PINS`, a one-entry literal, against section 7.9's
# "standing is DISCOVERED, not listed".  Here the digest is a RECORDED
# MEASUREMENT that gets a hard comparison against the artifact's own destroyed
# row, and the STANDING -- unrecoverable, and satisfiable by nothing on disk --
# is MEASURED every run by sweeping the tree.  The path is recorded for the same
# reason: the file STILL EXISTS at other bytes, so a reader checking only
# existence concludes the pin is satisfiable.
# ---------------------------------------------------------------------------
DESTROYED_DIGEST = (
    "4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea")
DESTROYED_PATH = "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json"

# Content anchors instead of a whole-file digest on the moving freeze.  Matched
# under section 7.7 folding, so a reflow, a blockquote or an emphasis run does
# not manufacture a refusal, while REMOVAL of the cited text still fails.  These
# also supply IMPLEMENTATION-FREEZE.md's FLOOR: a document carrying none of them
# is not the freeze, however many bytes it has.
FREEZE_ANCHORS = (
    # 7.3, the 2026-08-10 rider that settles this instrument's terminus rule
    "Resolution terminates at a full-text standalone's reviewed bytes",
    "the terminus test is the review, not the shape",
    "Full-chain resolution would DISCARD THE ONLY REVIEWED BYTES IN THE CHAIN",
    "require a POSITIVE resolution",
    # 7.3, the 2026-08-06 rider -- why this instrument resolves rather than reads
    "The CONSUMING INSTRUMENTS still read flat, and to a flat reader a "
    "derivation is indistinguishable from a DEFECTIVE artifact",
    "Before applying ANY derivation, measure what its declared consuming gate "
    "does with it",
    # 7.3, the 2026-08-05 rider -- the inherited-measurement rule
    "a derivation must state, for every inherited measurement, either that it "
    "re-measured it or that it did not",
    # 7.2.2 -- the standard this instrument is held to
    "a measurement that cannot fail the build is prose",
    "enumerate by what the figure DESCRIBES, never by what it is CALLED",
    "Derive the row set from the artifact's own structure, and publish the count "
    "of rows generated",
    "a numeric sweep cannot reach a figure written as a WORD",
    # 7.8 / 7.8.1 -- the bound this instrument prints, and its licence
    "these instruments bind structure and type; they do not bind the truth of "
    "content",
    "a new checker is a new file and edits nothing",
    "A missing input must refuse, never proceed on a default",
    "Refusal must be SCOPED and NAMED",
    # 7.10 -- read-vs-pin, and the standing-is-measured rule
    "pin the PROPERTY, not the CURRENT VALUE, whenever the value is",
    "\"Unsatisfiable\" must be MEASURED against the recovery point, not asserted",
    # 6, law 18 and law 14
    "Closed-scalar admission is exact-type.",
    "A durability failure cannot report authoritative success; a provider fault "
    "cannot become a finding; a policy failure cannot become a host error.",
    # 7.7 -- the folding applied before every containment test
    "Fold markdown structure",
)

# ---------------------------------------------------------------------------
# RECORDED MEASUREMENTS about the reviewed bytes and their closure.  Section
# 7.2.2 gives a recorded measurement a HARD COMPARISON: an uncompared measurement
# is prose that looks like evidence, and going stale is a TRUE POSITIVE about
# these bytes.  Everything the artifact itself publishes is RE-DERIVED and is not
# listed here; these are properties of the SUBJECT-AND-ITS-CLOSURE that the
# artifact does not publish, which is exactly the case section 7.2.2 reserves for
# a hard pin.
# ---------------------------------------------------------------------------
RECORDED = {
    # resolution
    "predecessorByteSha256":
        "a6546408fb38df95166f0ec41b1d9d9dae0dbda580684ff8a6e94f57145ad97e",
    "predecessorCanonicalSha256":
        "546abee0f5329b13a67d33fb9517403b089eb454c369a303a419d7d3d2ab5080",
    "resolvedCanonicalSha256":
        "4241f87b0edd8675d9f1819e130e24f4b6aa6d0db9d07b73ede3a0ff46c2ef2a",
    # the predecessor lane's own resolved value, reproduced by repairing FORM
    # only.  The artifact claims its substantive delta is IDENTICAL to v27's;
    # this is the digest that claim stands or falls on.
    "v27IntendedResolvedSha256":
        "fc1df5580e18a16685199169a05938f365eaae3a54c9536e748c745cdfa62314",
    "operationCount": 8,
    "identityOperations": 5,
    "repairOperations": 3,
    # both pinned resolvers, executed
    "resolverDeclarationErrors": 0,
    "resolverOperationsApplied": 8,
    "resolverApplyErrors": 0,
    "fullChainErrors": 30,
    "fullChainErrorsNamingThisArtifactsOperations": 0,
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
    # censuses
    "deltaTopLevelKeys": 27,
    "resolvedTopLevelKeys": 41,
    "deltaScalarLeaves": 1799,
    "resolvedScalarLeaves": 2935,
    "resolvedIntLeaves": 439,
    "resolvedIntFirstControl": 788,
    # THIS INSTRUMENT'S OWN derived self-measurement sweep.  These are the
    # population figures its generator produces -- NOT the artifact's, whose
    # generator is different and is not re-executed here.  Every one is compared
    # in check_derived_sweep; a recorded measurement this file did not compare
    # would be prose wearing a measurement's clothes (section 7.2.2).
    "sweepRowsOverTheResolvedValue": 502,
    "sweepRowsOverThePredecessor": 502,
    "sweepReferentRows": 439,
    "sweepDecimalProseRows": 37,
    "sweepWordNumeralRows": 26,
    "sweepDefinitiveOverThePredecessor": 1,
    "sweepDefinitiveOverTheResolvedValue": 0,
    # the review terminus
    "terminusReviewBlockingFindings": 0,
}

# The same-type falsification rate, MEASURED by --falsification over the written
# bytes and hard-compared there.  Section 7.8: a limits list that omits the
# dominant class is worse than none, so the number is published rather than
# characterised, and the mode that recomputes it fails on disagreement.
# MEASURED 2026-08-11 by `--falsification` over the written bytes of the subject.
MEASURED_FALSIFICATION = {
    "attempted": 0,
    "bound": 0,
    "free": 0,
    "unclaimed": 0,
    "ratePercent": 0.0,
}


class PinRefused(RuntimeError):
    """A GATED pin did not match.  Exit 2."""


class InputUnavailable(RuntimeError):
    """A declared input is absent, unreadable, or below its floor.  BLOCKER 1's
    repair: this is a VALUE, not an escaping OSError."""


class DuplicateKeyError(ValueError):
    pass


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
    """The recipe retention-tiers.v28 publishes at
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
    "…": "...", " ": " ", " ": " ", " ": " ",
    " ": " ", " ": " ",
}
_MD = re.compile(r"[*_`|\\>#]+")


def fold(text: str) -> str:
    """Section 7.7's folding, applied BEFORE any containment test.

    A byte-literal search on a multi-word phrase returns a false ABSENT on
    line-wrapped text, and whitespace normalisation ALONE still returns ABSENT on
    a blockquote -- IMPLEMENTATION-FREEZE.md states its standing rules inside `>`
    blocks, including the one sentence that makes escalating an unlisted gap
    legal.  Markdown structure is folded, not just whitespace.
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
        try:
            if path.is_file():
                return path
        except OSError:
            continue
    return candidates[0]


def read_input(rel: str):
    """BLOCKER 1's REPAIR, and the only route to the filesystem in this file.

    Returns (bytes, None) or (None, reason).  Every failure mode a hostile or
    merely broken tree can produce -- absent, a directory, chmod 000, a dangling
    symlink, an I/O error -- becomes a REASON STRING, never an exception.  The
    predecessor called path.read_bytes() directly at eleven sites and every one
    of them produced an uncaught PermissionError, EMPTY STDOUT and EXIT 1, which
    is the FINDINGS code: an unreadable input read as a verdict.
    """
    path = resolve_input(rel)
    try:
        if not path.exists():
            return None, f"absent (looked at {path})"
        if not path.is_file():
            return None, f"not a regular file (at {path})"
        return path.read_bytes(), None
    except OSError as exc:
        return None, f"{type(exc).__name__}: {exc}"


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
    retention-tiers.v28 names at $.derivedFrom.resolutionAlgorithm.step3.
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
    boolean as an integer.  The INT-FIRST CONTROL is computed alongside and
    PUBLISHED, so the ordering defect is visible if it is ever reintroduced: over
    the resolved value it reports 788 against the true 439."""
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
# SECTION 1 -- INPUT VERIFICATION, FLOORS, AND THE EXECUTION-EDGE AUDIT.
#
# BLOCKER 1 and BLOCKER 2 both live here.  Read as inert bytes, classify, and
# APPLY A FLOOR before anything is parsed or executed.
# ===========================================================================

def floor_of(name: str):
    """The FLOOR for one declared input, DERIVED from what this run depends on
    rather than chosen as a threshold.

    BLOCKER 2's first repair.  The ADVANCING class exists because section 7.10
    is right that a digest pin cannot distinguish "the input legitimately
    advanced" from "the input is wrong".  It does not follow that EVERY change is
    an advance.  An input that is no longer RECOGNISABLE AS ITSELF has not
    advanced; it has been destroyed in place, and section 7.8.1 rule 1 governs:
    a missing input must refuse, never proceed on a default.

    Returns a list of (id, predicate) pairs.  Each predicate takes the raw bytes
    and returns (ok, detail).  Every floor is individually falsifiable and every
    one is exercised by the mutation suite.
    """
    tests = [("NON-EMPTY",
              lambda data: (bool(data),
                            f"{len(data)} byte(s); a zero-byte file is not an "
                            f"advance, it is an absence wearing a filename"))]
    if name.endswith(".json"):
        def _parses(data):
            try:
                value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs)
            except Exception as exc:  # noqa: BLE001 -- the floor is "does it parse"
                return False, f"{type(exc).__name__}: {exc}"
            return isinstance(value, dict), ("parses to a JSON object"
                                             if isinstance(value, dict)
                                             else f"parses to {type(value).__name__}")
        tests.append(("PARSES-AS-A-JSON-OBJECT", _parses))
    if name == "IMPLEMENTATION-FREEZE.md":
        def _recognisable(data):
            text = fold(data.decode("utf-8", "replace"))
            hits = sum(1 for anchor in FREEZE_ANCHORS if fold(anchor) in text)
            return bool(hits), (f"{hits} of {len(FREEZE_ANCHORS)} content anchors "
                                f"resolve under section 7.7 folding; a document "
                                f"carrying none of them is not the document this "
                                f"instrument quotes, however many bytes it has")
        tests.append(("RECOGNISABLE-AS-THE-QUOTED-SOURCE", _recognisable))
    return tests


def apply_floor(name: str, data: bytes):
    """(ok, [failures]).  A floor failure is never a finding about the subject."""
    failures = []
    for test_id, predicate in floor_of(name):
        try:
            ok, detail = predicate(data)
        except Exception as exc:  # noqa: BLE001
            ok, detail = False, f"the floor test itself raised {type(exc).__name__}: {exc}"
        if not ok:
            failures.append(f"{test_id}: {detail}")
    return (not failures), failures


def measure_all_inputs():
    """Every declared input's LIVE digest, measured at the moment of the call.
    Called once before the run and once after, so an input that moved underneath
    the measurement is reported rather than silently absorbed.

    BLOCKER 1: this function CANNOT RAISE.  It was the FIRST statement of the
    predecessor's main(), pre-empting every guard the file carried, and it read
    every path with a bare read_bytes().  An unreadable row is recorded as the
    sentinel below and the caller decides; nothing here escapes as an exception.
    """
    out = {}
    for name in (list(GATED_PINS) + list(ADVANCING_PINS)
                 + [f"artifacts/{SUBJECT}", DESTROYED_PATH]):
        data, reason = read_input(name)
        out[name] = sha_bytes(data) if data is not None else f"<<UNREADABLE {reason}>>"
    return out


def verified_inputs():
    """(snapshots, notices, skipped).

    A GATED mismatch, or a REQUIRED input that is absent / unreadable / below its
    floor, raises InputUnavailable or PinRefused; main() turns either into a
    named exit-2 diagnostic saying THE CHECK DID NOT RUN.  A NON-REQUIRED input
    in the same state SKIPS ONLY THE CLASSES THAT READ IT, by name, and the run
    exits 4 (section 7.8.1 rule 2: a blanket stop when five of six classes could
    still run throws away real coverage).
    """
    snaps = {}
    notices = []
    errors = []
    skipped = {}
    required = set(required_inputs())
    floors = {}

    def _unavailable(name, why):
        if name in required:
            errors.append(
                f"RT28-INPUT-UNAVAILABLE {name}: {why}. This input is REQUIRED "
                f"-- the resolution, the executed closure or the quoted rules "
                f"rest on it -- so THE CHECK DID NOT RUN. This is not a finding "
                f"about {SUBJECT} and this exit says nothing whatever about its "
                f"20 vectors or its 24 invariants")
        else:
            klass = PER_CLASS_INPUTS.get(name, "unclassified")
            skipped.setdefault(klass, []).append(f"{name} ({why})")
            notices.append(
                f"RT28-CLASS-SKIPPED {klass}: {name} is unavailable ({why}), so "
                f"that class DID NOT RUN and nothing is asserted by its silence. "
                f"Every other class continued")

    for name, expected in GATED_PINS.items():
        data, reason = read_input(name)
        if data is None:
            _unavailable(name, reason)
            continue
        ok, failures = apply_floor(name, data)
        floors[name] = (ok, failures)
        if not ok:
            _unavailable(name, "below its FLOOR -- " + "; ".join(failures))
            continue
        actual = sha_bytes(data)
        if actual != expected:
            errors.append(
                f"RT28-PIN-REFUSED {name}: GATED at {expected}, live {actual}. "
                f"This instrument refuses rather than re-pointing the pin; "
                f"repair is a SUCCESSOR instrument, never an edit to these "
                f"bytes (section 7.2, section 7.6). NOTHING WAS PARSED OR "
                f"EXECUTED")
            continue
        snaps[name] = data

    for name, expected in ADVANCING_PINS.items():
        data, reason = read_input(name)
        if data is None:
            _unavailable(name, reason)
            continue
        ok, failures = apply_floor(name, data)
        floors[name] = (ok, failures)
        if not ok:
            # BLOCKER 2.  Below the floor an ADVANCING input is not advancing.
            _unavailable(
                name,
                "below its FLOOR, so it is DESTROYED IN PLACE rather than "
                "ADVANCED -- " + "; ".join(failures))
            continue
        snaps[name] = data
        actual = sha_bytes(data)
        if actual != expected:
            notices.append(
                f"RT28-PIN-ADVANCED {name}: recorded {expected[:16]}..., live "
                f"{actual[:16]}.... NOT A FINDING. The artifact classifies this "
                f"input CITED-DIGEST-RECORDED-NOT-GATED, so this run re-extracts "
                f"what it depends on from the LIVE bytes rather than refusing "
                f"(section 7.10). The input CLEARED ITS FLOOR "
                f"({len(floor_of(name))} test(s)), which is what distinguishes an "
                f"advance from a destruction; a pinned input that ADVANCED costs "
                f"a re-read, not a successor instrument")

    if errors:
        raise InputUnavailable(" | ".join(errors))
    return snaps, notices, skipped, floors


def destroyed_standing():
    """Section 7.10, rule 3: "Unsatisfiable" must be MEASURED against the
    recovery point, not asserted -- and section 7.9: standing is DISCOVERED, not
    listed.  The predecessor lineage was faulted for `if name in
    UNSATISFIABLE_PINS`, a one-entry literal.

    This sweeps every regular file under artifacts/ and measures three things a
    reader needs and cannot get from a membership test:
      * whether ANY file carries the destroyed digest  -> RESURRECTION
      * whether the destroyed path still EXISTS         -> MUTATED, NOT DELETED
      * what that path's LIVE bytes are now             -> the misreading trap

    Returns (report, refusals).  A refusal is exit 2.
    """
    report = {"filesSwept": 0, "unreadable": [], "carriers": [],
              "pathStillExists": False, "pathLiveDigest": None,
              "pathLiveEqualsDestroyed": None}
    refusals = []
    art = COOP / "artifacts"
    try:
        entries = sorted(art.iterdir()) if art.is_dir() else []
    except OSError as exc:
        refusals.append(f"RT28-DESTROYED-SWEEP-REFUSED artifacts/ could not be "
                        f"listed ({type(exc).__name__}: {exc}), so the "
                        f"resurrection guard DID NOT RUN")
        return report, refusals
    for candidate in entries:
        try:
            if not candidate.is_file():
                continue
        except OSError:
            continue
        report["filesSwept"] += 1
        data, reason = read_input(f"artifacts/{candidate.name}")
        if data is None:
            report["unreadable"].append(f"{candidate.name} ({reason})")
            continue
        if sha_bytes(data) == DESTROYED_DIGEST:
            report["carriers"].append(candidate.name)
    live, reason = read_input(DESTROYED_PATH)
    report["pathStillExists"] = live is not None
    if live is not None:
        report["pathLiveDigest"] = sha_bytes(live)
        report["pathLiveEqualsDestroyed"] = (report["pathLiveDigest"]
                                             == DESTROYED_DIGEST)
    if report["carriers"]:
        refusals.append(
            f"RT28-PIN-RESURRECTED {report['carriers']}: these bytes hash to "
            f"{DESTROYED_DIGEST}, a digest whose bytes were destroyed by an "
            f"in-place edit and are UNRECOVERABLE -- the file appears in no "
            f"commit on any branch, so it is not in the 7cc0f8a recovery point. "
            f"Bytes cannot come back. Either a file has been fabricated to match "
            f"a dead pin or this instrument's record is wrong; either way "
            f"nothing here may be trusted")
    # NOTE THE ASYMMETRY, and it is section 7.8.1 rule 2 applied to this guard.
    # FINDING A CARRIER is an integrity failure and refuses the whole run.  BEING
    # UNABLE TO ESTABLISH ABSENCE is a COVERAGE loss: it skips THIS CLASS, by
    # name, at the distinct exit code, and leaves every other class measuring.
    # Collapsing the two would make exit 4 unreachable and would throw away real
    # coverage whenever one unrelated file in artifacts/ is unreadable.
    if report["unreadable"]:
        report["classSkipped"] = (
            f"RT28-CLASS-SKIPPED resurrectionGuard: {len(report['unreadable'])} "
            f"file(s) under artifacts/ could not be read, so the guard COULD NOT "
            f"ESTABLISH that the destroyed digest is absent from the tree: "
            f"{report['unreadable'][:5]}. An unmeasured sweep is not a clean sweep "
            f"and is never reported as one. Every other class continued")
    return report, refusals


# ---------------------------------------------------------------------------
# BLOCKER 4's REPAIR, second half: the declaration above is audited against this
# file's own source BY AST.  Nothing here reads a digest from an unpinned
# document, and nothing executes a module EXECUTED_MODULES does not name.
# ---------------------------------------------------------------------------

_MODULE_CACHE = {}


def load_pinned_module(rel: str, source: bytes):
    """THE ONLY exec() IN THIS FILE.  The bytes handed here have already been
    hash-verified against GATED_PINS, so the bytes executed are the bytes
    hashed -- never re-read from disk after verification (section 7.3).

    Memoised on (path, DIGEST OF THE BYTES EXECUTED), so the cache key is the
    verification itself: different bytes are a different module, never a reused
    one."""
    key = (rel, sha_bytes(source))
    if key in _MODULE_CACHE:
        return _MODULE_CACHE[key]
    module = types.ModuleType("pinned_" + re.sub(r"\W", "_", rel))
    module.__file__ = str(resolve_input(rel))
    code = compile(source.decode("utf-8"), module.__file__, "exec")
    exec(code, module.__dict__)  # noqa: S102 -- the point of section 7.3
    _MODULE_CACHE[key] = module
    return module


def audit_execution_edges():
    """Parse THIS FILE with `ast` and compare the execution edges it actually
    contains against EXECUTED_MODULES, in BOTH directions.

    The predecessor exec'd check-completeness.py from a path built inline, with
    no pin, no record and no declaration -- and deleting the file took the run to
    EXIT 0.  A declaration that nothing compares is prose (section 7.2.2).  This
    is the comparison.

    Returns (report, failures).
    """
    report = {"loaderCalls": [], "declared": sorted(EXECUTED_MODULES),
              "execNodes": 0, "evalNodes": 0, "dynamicImportNodes": 0,
              "unpinnedDeclared": [], "nonLiteralLoaderCalls": 0}
    failures = []
    data, reason = read_input(f"artifacts/{pathlib.Path(__file__).name}")
    if data is None:
        failures.append(f"RT28-AUDIT the instrument could not read its own "
                        f"source ({reason}), so the execution-edge audit DID NOT "
                        f"RUN and its silence proves nothing")
        return report, failures
    try:
        tree = ast.parse(data.decode("utf-8"), filename=__file__)
    except SyntaxError as exc:
        failures.append(f"RT28-AUDIT the instrument's own source did not parse "
                        f"({exc}); the audit DID NOT RUN")
        return report, failures

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = None
        if isinstance(func, ast.Name):
            name = func.id
        elif isinstance(func, ast.Attribute):
            name = func.attr
        if name == "exec":
            report["execNodes"] += 1
        elif name == "eval":
            report["evalNodes"] += 1
        elif name in ("__import__", "import_module", "exec_module",
                      "module_from_spec", "spec_from_file_location"):
            report["dynamicImportNodes"] += 1
        elif name == "load_pinned_module":
            if node.args and isinstance(node.args[0], ast.Constant) and \
                    isinstance(node.args[0].value, str):
                report["loaderCalls"].append(node.args[0].value)
            else:
                report["nonLiteralLoaderCalls"] += 1

    found = sorted(set(report["loaderCalls"]))
    declared = sorted(EXECUTED_MODULES)
    if found != declared:
        failures.append(
            f"RT28-AUDIT the execution edges this file's SOURCE contains and the "
            f"EXECUTED_MODULES declaration disagree. Source: {found}. Declared: "
            f"{declared}. Symmetric difference "
            f"{sorted(set(found) ^ set(declared))}. A declaration nothing "
            f"compares is prose; this comparison is what makes it evidence")
    if report["execNodes"] != 1:
        failures.append(
            f"RT28-AUDIT this file contains {report['execNodes']} exec() call(s). "
            f"Exactly one is permitted, inside load_pinned_module, so that every "
            f"executed byte has passed a GATED digest check first. More than one "
            f"means an execution path exists that the audit above does not cover")
    for extra, label in ((report["evalNodes"], "eval()"),
                         (report["dynamicImportNodes"], "dynamic-import")):
        if extra:
            failures.append(
                f"RT28-AUDIT this file contains {extra} {label} node(s). Any of "
                f"them is an execution edge outside EXECUTED_MODULES and outside "
                f"the GATED closure")
    if report["nonLiteralLoaderCalls"]:
        failures.append(
            f"RT28-AUDIT {report['nonLiteralLoaderCalls']} call(s) to "
            f"load_pinned_module do not pass a string literal, so the audit "
            f"cannot see which module they load. A computed module path is "
            f"exactly the edge BLOCKER 4 names")
    for rel in declared:
        if rel not in GATED_PINS:
            report["unpinnedDeclared"].append(rel)
    if report["unpinnedDeclared"]:
        failures.append(
            f"RT28-AUDIT {report['unpinnedDeclared']} are declared EXECUTED and "
            f"are NOT members of GATED_PINS, so they would be executed without a "
            f"hash check. That is BLOCKER 4 exactly: the predecessor exec'd "
            f"check-completeness.py unpinned, and deleting it produced EXIT 0")
    return report, failures


# ===========================================================================
# SECTION 2 -- THE DERIVATION READER, AND THE REVIEW-TERMINUS RULE.
#
# Shape, not name (CMP-IR-01).  Verify before use.  Never degrade silently.  An
# EMPTY operation list is a NAMED REFUSAL rather than an invisible absence --
# the trap check-completeness.py names against its own reader, where
# is_operation_list requires bool(value) so a ZERO-OPERATION DERIVATION IS
# INVISIBLE.
# ===========================================================================

JSON_NAME_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*\.json$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DERIVATION_VERBS = ("set",)


def is_operation(item) -> bool:
    return (isinstance(item, dict) and isinstance(item.get("op"), str)
            and isinstance(item.get("path"), str) and bool(item.get("path")))


def looks_like_operation_list(value) -> bool:
    """NOTE the deliberate difference from check-completeness.py: `bool(value)`
    is NOT required.  An empty list of operation-shaped members is still an
    operation list, and the caller refuses it BY NAME."""
    return isinstance(value, list) and all(is_operation(i) for i in value)


def find_declaration(document, errors, prefix=""):
    """Locate the derivation declaration by SHAPE.

    A declaration is a top-level object carrying at least one artifact filename,
    at least one sha256, and exactly one operation list.

    THE SHAPE SCREEN IS NOT THE TERMINUS TEST.  The predecessor instrument
    additionally required TWO DISTINCT DIGESTS here, which is what stopped it
    recursing into retention-tiers.v26's narrative change-log -- correct
    behaviour reached by accident of shape.  Section 7.3's 2026-08-10 resolution
    is explicit that the terminus test is THE REVIEW, so this reader deliberately
    does NOT lean on the digest count: it will happily recognise v26's change-log
    as a declaration, and review_terminus() below is what stops the recursion.
    Making the two questions separate is the point; a shape screen that happens
    to give the right answer cannot say why.
    """
    found = []
    for key, block in document.items():
        if not isinstance(block, dict):
            continue
        names = [v for v in block.values()
                 if isinstance(v, str) and JSON_NAME_RE.match(v)]
        digests = [v for v in block.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        if not names or not digests:
            continue
        op_lists = [v for v in block.values() if looks_like_operation_list(v)]
        if not op_lists:
            continue
        if len(op_lists) != 1:
            errors.append(
                f"{prefix}RT28-DERIV-AMBIGUOUS-OPERATIONS '{key}' carries "
                f"{len(op_lists)} operation lists; a derivation must state "
                f"exactly one, so no effective contract can be materialised")
            continue
        if not op_lists[0]:
            errors.append(
                f"{prefix}RT28-DERIV-EMPTY-OPERATIONS '{key}' declares a "
                f"derivation with ZERO operations. A zero-operation derivation "
                f"asserts that the successor IS the predecessor under a new name, "
                f"which is a CLAIM, not an absence. It is refused by name here "
                f"because a reader that requires a non-empty operation list to "
                f"recognise a declaration cannot see this case at all")
            continue
        found.append((key, {"block": key, "names": names, "digests": digests,
                            "operations": op_lists[0]}))
    if len(found) > 1:
        errors.append(f"{prefix}RT28-DERIV-AMBIGUOUS more than one top-level "
                      f"block has the shape of a derivation declaration: "
                      + ", ".join(sorted(k for k, _ in found)))
        return None
    return found[0][1] if found else None


def bind_predecessor(declaration, errors, prefix=""):
    """Decide WHICH declared filename is the predecessor and WHICH declared digest
    is its byte digest, BY MEASUREMENT rather than by key name.  Locating either
    by name would reproduce CMP-IR-01 one level up."""
    byte_matches = []
    for name in declaration["names"]:
        rel = name if "/" in name else f"artifacts/{name}"
        data, _reason = read_input(rel)
        if data is None:
            continue
        digest = sha_bytes(data)
        if digest in declaration["digests"]:
            byte_matches.append((name, rel, digest, data))
    if not byte_matches:
        errors.append(
            f"{prefix}RT28-DERIV-NO-PREDECESSOR none of the declared filenames "
            f"{declaration['names']} has bytes hashing to any declared digest "
            f"{[d[:16] + '...' for d in declaration['digests']]}. The predecessor "
            f"is identified by MEASUREMENT, not by key name, and no measurement "
            f"succeeds, so the effective contract cannot be built")
        return None
    if len(byte_matches) > 1:
        errors.append(
            f"{prefix}RT28-DERIV-AMBIGUOUS-PREDECESSOR more than one declared "
            f"filename hashes to a declared digest: "
            + ", ".join(sorted(n for n, _, _, _ in byte_matches)))
        return None
    name, rel, byte_digest, data = byte_matches[0]
    return {"name": name, "rel": rel, "byteDigest": byte_digest, "bytes": data,
            "otherDigests": [d for d in declaration["digests"] if d != byte_digest]}


# ---------------------------------------------------------------------------
# THE REVIEW-TERMINUS TEST.
# ---------------------------------------------------------------------------

_BLOCKING_KEY_RE = re.compile(r"blocking")
_COUNT_KEY_RE = re.compile(r"count|total|number")


def _blocking_tally(document):
    """Does this document publish a BLOCKING-FINDING TALLY?  Located by SHAPE:
    a non-bool integer member whose key, folded, mentions BLOCKING and mentions a
    counting word, sitting beside a list member whose key also mentions blocking
    or findings.  A review states how many blockers it found; a pin manifest, a
    change log and a delta do not."""
    best = None
    for _path, obj in objects_of(document):
        if not isinstance(obj, dict):
            continue
        for key, value in obj.items():
            folded = key.casefold()
            if not exact_int(value):
                continue
            if not (_BLOCKING_KEY_RE.search(folded)
                    and _COUNT_KEY_RE.search(folded)):
                continue
            if best is None or value < best:
                best = value
    return best


def review_terminus(pred, subject_declaration, subject_rel):
    """Section 7.3, 2026-08-10: RESOLUTION TERMINATES AT A FULL-TEXT STANDALONE'S
    REVIEWED BYTES, and THE TERMINUS TEST IS THE REVIEW, NOT THE SHAPE.

    Returns (isTerminus, report).  `report` is published in the banner and every
    figure in it is falsifiable.

    HALF A -- CORPUS DISCOVERY.  Standing is DISCOVERED, not listed: no review
    filename appears anywhere in this file.  A candidate review of the
    predecessor P is any artifacts/*.json R such that
      (a) R is neither the subject nor P;
      (b) some OBJECT of R carries P's filename AND P's LIVE byte digest as two
          of its own member values -- section 7.2's recording-obligation shape,
          which is what distinguishes recording bytes from mentioning a name;
      (c) R is not itself a derivation whose bound predecessor is P (that is what
          a SUCCESSOR looks like, and a successor records exactly the same two
          things);
      (d) R publishes a blocking-finding tally.
    The population is counted and published.

    HALF B -- DECLARATION VERIFICATION.  The subject's own declaration block
    names a review filename and a digest.  That file must be in Half A's
    population, must live at the declared digest, and must report ZERO blocking
    findings.  A subject that names no review, or names one that is not a review,
    or names one that rejected the predecessor, gets NO TERMINUS -- and the
    resolver then recurses, which is the behaviour that is correct for a real
    delta.
    """
    report = {"predecessor": pred["name"], "populationScanned": 0,
              "populationUnreadable": 0, "reviewsFound": [], "reviewCount": 0,
              "declaredReview": None, "declaredReviewDigest": None,
              "declaredReviewIsInThePopulation": False,
              "declaredReviewDigestMatches": False,
              "blockingFindings": None, "isTerminus": False,
              "why": ""}
    pred_names = {pred["name"], f"artifacts/{pathlib.PurePosixPath(pred['name']).name}",
                  pathlib.PurePosixPath(pred["name"]).name}
    # HALF A is memoised on the PREDECESSOR'S OWN DIGEST and the subject path,
    # which are the only two things it reads.  It sweeps ~440 documents; the
    # falsification sweep drives ~1800 runs, and a discovery that re-reads the
    # corpus 1800 times measures the same corpus 1800 times.  Different
    # predecessor bytes are a different key, so the cache cannot answer for a
    # predecessor it never scanned.
    cache_key = (pred["byteDigest"], subject_rel)
    if cache_key in _TERMINUS_HALF_A:
        cached = _TERMINUS_HALF_A[cache_key]
        report["populationScanned"] = cached["populationScanned"]
        report["populationUnreadable"] = cached["populationUnreadable"]
        report["reviewsFound"] = list(cached["reviewsFound"])
        return _terminus_half_b(pred, subject_declaration, report, pred_names)
    art = COOP / "artifacts"
    try:
        entries = sorted(art.glob("*.json"))
    except OSError:
        entries = []
    subject_base = pathlib.PurePosixPath(subject_rel).name
    subject_bytes, _r = read_input(f"artifacts/{subject_base}")
    subject_digest = sha_bytes(subject_bytes) if subject_bytes else None
    for candidate in entries:
        if candidate.name in (subject_base, pathlib.PurePosixPath(pred["name"]).name):
            continue
        report["populationScanned"] += 1
        data, _reason = read_input(f"artifacts/{candidate.name}")
        if data is None:
            report["populationUnreadable"] += 1
            continue
        try:
            doc = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs)
        except Exception:  # noqa: BLE001 -- an unparseable neighbour is not a review
            continue
        if not isinstance(doc, dict):
            continue
        # (b) the recording-obligation shape
        records = False
        for _p, obj in objects_of(doc):
            if not isinstance(obj, dict):
                continue
            values = [v for v in obj.values() if isinstance(v, str)]
            if pred["byteDigest"] in values and any(v in pred_names for v in values):
                records = True
                break
        if not records:
            continue
        # (c) not a successor delta over P
        inner_errors = []
        inner = find_declaration(doc, inner_errors)
        if inner is not None:
            bound = bind_predecessor(inner, [])
            if bound is not None and bound["name"] in pred_names:
                continue
        # (d) a blocking-finding tally
        tally = _blocking_tally(doc)
        if tally is None:
            continue
        # DOES IT ALSO RECORD THE SUBJECT'S OWN BYTES?  A document that records
        # both the predecessor and the SUBJECT is reviewing something that
        # includes the subject, and nominating it as the predecessor's terminus
        # would let a successor stand as its own predecessor's verdict.  Half B
        # requires the declared review to be INDEPENDENT of the subject by this
        # test; both populations are counted and published.
        text_leaves = {v for _p, v in scalar_leaves(doc) if isinstance(v, str)}
        report["reviewsFound"].append({
            "file": candidate.name,
            "sha256": sha_bytes(data),
            "blockingFindings": tally,
            "independentOfTheSubject": (subject_digest is None
                                        or subject_digest not in text_leaves)})
    _TERMINUS_HALF_A[cache_key] = {
        "populationScanned": report["populationScanned"],
        "populationUnreadable": report["populationUnreadable"],
        "reviewsFound": list(report["reviewsFound"])}
    return _terminus_half_b(pred, subject_declaration, report, pred_names)


_TERMINUS_HALF_A = {}


def _terminus_half_b(pred, subject_declaration, report, pred_names):
    """HALF B -- the subject's DECLARATION, verified against Half A's discovered
    population.  Never memoised: the declaration is the thing under test."""
    report["reviewCount"] = len(report["reviewsFound"])
    report["reviewsIndependentOfTheSubject"] = sum(
        1 for e in report["reviewsFound"] if e.get("independentOfTheSubject"))
    declared_name = None
    declared_digest = None
    block = subject_declaration.get("_block") or {}
    for _p, obj in objects_of(block):
        if not isinstance(obj, dict):
            continue
        names = [v for v in obj.values()
                 if isinstance(v, str) and JSON_NAME_RE.match(v)
                 and v not in pred_names]
        digests = [v for v in obj.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        for name in names:
            for digest in digests:
                for entry in report["reviewsFound"]:
                    if entry["file"] == pathlib.PurePosixPath(name).name \
                            and entry["sha256"] == digest:
                        declared_name, declared_digest = name, digest
    report["declaredReview"] = declared_name
    report["declaredReviewDigest"] = declared_digest
    if declared_name is None:
        report["why"] = (
            "the subject's declaration block names no document that is BOTH a "
            "discovered review of the predecessor AND recorded at the digest that "
            "review lives at, so no terminus is established and the chain is "
            "resolved rather than stopped")
        return False, report
    report["declaredReviewIsInThePopulation"] = True
    report["declaredReviewDigestMatches"] = True
    entry = next(e for e in report["reviewsFound"]
                 if e["file"] == pathlib.PurePosixPath(declared_name).name)
    report["blockingFindings"] = entry["blockingFindings"]
    if not entry.get("independentOfTheSubject"):
        report["why"] = (
            f"the declared review {declared_name} ALSO records the subject's own "
            f"bytes, so it is not an independent verdict on the predecessor and "
            f"nominating it would let this successor stand as its own "
            f"predecessor's terminus")
        return False, report
    if entry["blockingFindings"] != 0:
        report["why"] = (
            f"the declared review of the predecessor reports "
            f"{entry['blockingFindings']} blocking finding(s), so the predecessor's "
            f"bytes do not carry a clean verdict and stopping at them would claim "
            f"a review that was not granted")
        return False, report
    report["isTerminus"] = True
    report["why"] = (
        f"{declared_name} at {declared_digest[:16]}... records the predecessor's "
        f"exact live bytes and reports 0 blocking findings, so THOSE BYTES ARE "
        f"THE ONLY REVIEWED BYTES IN THE CHAIN. Resolving THROUGH them would "
        f"replace a verdict-bearing input with a computed one, which is section "
        f"7.2's whole subject. Resolution stops here BY THE REVIEW TEST, not by "
        f"a shape screen")
    return True, report


def apply_operations(base, operations, errors, prefix=""):
    """Apply the declared operations in order.

    Every `set` must restate, at EXACT JSON TYPE with bool decided before int,
    the value it replaces.  A `from` mismatch REFUSES the whole resolution; it
    never silently overwrites.  An operation that does not find what it claims to
    replace is describing a document that no longer exists.
    """
    effective = copy.deepcopy(base)
    applied = []
    for index, op in enumerate(operations):
        verb, path = op.get("op"), op.get("path")
        where = f"operation {index} ({verb} {path})"
        if verb not in DERIVATION_VERBS:
            errors.append(f"{prefix}RT28-DERIV-VERB {where}: unknown verb; the "
                          f"declared verb set is {list(DERIVATION_VERBS)}")
            continue
        if "from" not in op:
            errors.append(f"{prefix}RT28-DERIV-NO-FROM {where}: a set must restate "
                          f"the value it replaces")
            continue
        if "value" not in op:
            errors.append(f"{prefix}RT28-DERIV-NO-VALUE {where}: carries no "
                          f"replacement value at the member key `value`, which is "
                          f"the key BOTH corpus resolvers require")
            continue
        steps = path_steps(path)
        if steps is None or not steps:
            errors.append(f"{prefix}RT28-DERIV-PATH {where}: path is not plainly "
                          f"resolvable")
            continue
        if steps[0] == "$":
            errors.append(
                f"{prefix}RT28-DERIV-PATH {where}: the path is spelled with the "
                f"`$.` DISPLAY prefix, which tokenises to a first STEP named `$`. "
                f"No document has a top-level member named `$`, so the parent of "
                f"every such path fails to resolve under both corpus resolvers")
            continue
        found, parent = resolve_steps(effective, steps[:-1])
        if not found or not isinstance(parent, (dict, list)):
            errors.append(f"{prefix}RT28-DERIV-PARENT {where}: parent does not "
                          f"resolve to a container in the verified predecessor")
            continue
        if not has_step(parent, steps[-1]):
            errors.append(f"{prefix}RT28-DERIV-ABSENT {where}: does not resolve "
                          f"against the verified predecessor, so the operation "
                          f"describes a document that does not exist")
            continue
        current = parent[steps[-1]]
        if not exact_equal(current, op["from"]):
            errors.append(
                f"{prefix}RT28-DERIV-FROM {where}: declares it replaces "
                f"{op['from']!r} ({type(op['from']).__name__}) and the verified "
                f"predecessor holds {current!r} ({type(current).__name__}). The "
                f"comparison is at exact JSON type with bool decided before int; "
                f"the derivation does not describe the bytes it is applied to")
            continue
        if type(op["from"]) is not type(op["value"]):
            errors.append(
                f"{prefix}RT28-DERIV-TYPE {where}: 'from' is "
                f"{type(op['from']).__name__} and 'value' is "
                f"{type(op['value']).__name__}. This derivation declares that no "
                f"operation changes a leaf's type, and the census it inherits "
                f"depends on that")
            continue
        if not isinstance(op["value"], (str, int, float, bool)) \
                and op["value"] is not None:
            errors.append(
                f"{prefix}RT28-DERIV-NONSCALAR {where}: 'value' is a "
                f"{type(op['value']).__name__}. This derivation declares every "
                f"operation a set on an existing SCALAR leaf, and the inherited "
                f"leaf census rests on that")
            continue
        parent[steps[-1]] = copy.deepcopy(op["value"])
        applied.append(path)
    return effective, applied


def resolve_subject(document, subject_rel=None, depth=0, seen=()):
    """(resolved value, provenance, errors).  Materialise the effective contract
    or explain, BY NAME, why it cannot be."""
    subject_rel = subject_rel or f"artifacts/{SUBJECT}"
    errors = []
    provenance = {"depth": depth}
    prefix = "" if depth == 0 else f"{subject_rel}: "
    declaration = find_declaration(document, errors, prefix)
    if declaration is None:
        if not errors:
            errors.append(
                f"{prefix}RT28-DERIV-NONE this document declares no derivation, so "
                f"there is no resolved value to assert over. Every Part A / Part C "
                f"/ Part D property this instrument exists to exercise lives in "
                f"the predecessor and NONE OF THEM WAS CHECKED")
        return None, provenance, errors
    provenance["block"] = declaration["block"]
    provenance["operationCount"] = len(declaration["operations"])
    declaration["_block"] = document[declaration["block"]]

    bound = bind_predecessor(declaration, errors, prefix)
    if bound is None:
        return None, provenance, errors
    provenance["predecessor"] = bound["name"]
    provenance["predecessorRel"] = bound["rel"]
    provenance["predecessorByteDigest"] = bound["byteDigest"]

    try:
        base = parse_json(bound["bytes"], bound["name"])
    except PinRefused as exc:
        errors.append(f"{prefix}RT28-DERIV-PARSE the verified predecessor did not "
                      f"parse under the duplicate-key-rejecting hook: {exc}")
        return None, provenance, errors
    if not isinstance(base, dict):
        errors.append(f"{prefix}RT28-DERIV-SHAPE the verified predecessor is not a "
                      f"JSON object")
        return None, provenance, errors

    base_canonical = sha_bytes(canonical(base))
    provenance["predecessorCanonicalDigest"] = base_canonical
    if bound["otherDigests"] and base_canonical not in bound["otherDigests"]:
        # v28 deliberately publishes ONE digest at the declaring level and nests
        # the canonical-value digest one level down, because both resolvers
        # require exactly one of each.  So an absent match here is only a finding
        # when the declaration actually carries a second digest at that level.
        errors.append(
            f"{prefix}RT28-DERIV-CANONICAL the declaration carries "
            f"{[d[:16] + '...' for d in bound['otherDigests']]} beside the byte "
            f"digest, and the canonical serialisation of the parsed predecessor "
            f"hashes to {base_canonical}. A second digest at the declaring level "
            f"is read by both resolvers as a second predecessor digest")

    # ---- THE TERMINUS DECISION -------------------------------------------
    is_terminus, terminus = review_terminus(bound, declaration, subject_rel)
    provenance["terminus"] = terminus
    inner_errors = []
    inner = find_declaration(base, inner_errors)
    provenance["predecessorHasDeclarationSHAPE"] = inner is not None or bool(inner_errors)
    if is_terminus:
        provenance["predecessorIsItselfADerivation"] = False
        provenance["terminusStopped"] = True
    else:
        provenance["terminusStopped"] = False
        if inner_errors:
            errors.extend(inner_errors)
            return None, provenance, errors
        if inner is not None:
            provenance["predecessorIsItselfADerivation"] = True
            if bound["rel"] in seen or depth >= 8:
                errors.append(f"{prefix}RT28-DERIV-CHAIN the derivation chain "
                              f"revisits {bound['rel']} or exceeds depth 8")
                return None, provenance, errors
            base, inner_prov, inner_errs = resolve_subject(
                base, bound["rel"], depth + 1, seen + (bound["rel"],))
            provenance["via"] = inner_prov
            if base is None:
                # NAME THE CAUSE.  Without this line the reader gets thirty
                # errors about the PREDECESSOR's change-log and no statement of
                # why the resolver went there at all.  Section 7.3's 2026-08-10
                # resolution is that a reviewed standalone is the base; losing
                # the terminus is what sent the recursion into it, and an
                # unexplained cascade is the same shape as a false accusation.
                errors.append(
                    f"{prefix}RT28-TERMINUS-LOST the resolver recursed into "
                    f"{bound['name']} because the REVIEW-TERMINUS test did not "
                    f"hold ({terminus.get('why')}), and that recursion refused "
                    f"with {len(inner_errs)} error(s). EVERY ERROR BELOW IS ABOUT "
                    f"THE PREDECESSOR'S OWN BLOCK, NOT ABOUT THIS ARTIFACT'S "
                    f"OPERATIONS. Section 7.3, 2026-08-10: resolution terminates "
                    f"at a full-text standalone's reviewed bytes, and resolving "
                    f"THROUGH those bytes would replace the only reviewed input "
                    f"in the chain with a reconstruction no reviewer has seen")
                errors.extend(inner_errs)
                return None, provenance, errors
        else:
            provenance["predecessorIsItselfADerivation"] = False

    effective, applied = apply_operations(base, declaration["operations"], errors,
                                          prefix)
    provenance["operationsApplied"] = len(applied)
    if errors:
        return None, provenance, errors
    provenance["resolvedCanonicalDigest"] = sha_bytes(canonical(effective))
    provenance["declaration"] = declaration
    provenance["parsedPredecessor"] = base
    return effective, provenance, errors


# ===========================================================================
# SECTION 3 -- THE TWO PINNED RESOLVERS, EXECUTED.
#
# Section 7.3's 2026-08-10 rider, rule 3: before applying ANY derivation, execute
# the resolver against it and require a POSITIVE resolution -- not merely the
# absence of an error.  `(None, [])` is indistinguishable from "not a derivation
# at all", and four binding candidates are in that state.
#
# BLOCKER 4: both resolvers are GATED and hash-verified before a byte is
# compiled, both are named in EXECUTED_MODULES, and the AST audit above compares
# that declaration against this file's actual edges.  Delete either one and the
# run refuses at exit 2 -- it does not go green.
# ===========================================================================

def run_resolvers(snaps, delta, ctx):
    """Execute both pinned resolvers against the subject and record, per
    resolver: the declaration, the applied-operation count, the resolved
    canonical digest, and the FULL-CHAIN outcome with its error attribution."""
    out = []
    results = {}
    # Memoised on the DECLARATION BLOCK alone, which is the only part of the
    # subject either resolver reads.  Same discipline as every other cache here:
    # the key is the exact value the work depends on, so a different declaration
    # is a different key and cannot be answered from a previous one.
    decl_key = sha_bytes(canonical(delta.get(
        (ctx.get("declarationBlock") or "derivedFrom"), {})))
    if decl_key in _RESOLVER_CACHE:
        ctx["resolvers"] = _RESOLVER_CACHE[decl_key][0]
        return list(_RESOLVER_CACHE[decl_key][1])
    for rel in ("artifacts/check-completeness.py",
                "artifacts/check-completeness-v2.py"):
        source = snaps.get(rel)
        if source is None:
            out.append(
                f"RT28-RESOLVER {rel} was verified but not snapshotted, which is "
                f"an internal contradiction; the resolver measurement DID NOT RUN")
            continue
        try:
            if rel == "artifacts/check-completeness.py":
                module = load_pinned_module("artifacts/check-completeness.py",
                                            source)
            else:
                module = load_pinned_module("artifacts/check-completeness-v2.py",
                                            source)
        except Exception as exc:  # noqa: BLE001 -- a gate that crashes is not a pass
            out.append(
                f"RT28-RESOLVER {rel} is pinned and hash-verified and DID NOT LOAD "
                f"({type(exc).__name__}: {exc}). The acceptance test for this "
                f"artifact is the execution of this resolver, so its failure is "
                f"reported and NEVER read as a pass")
            continue
        record = {}
        try:
            declaration, errors = module.derivation_declaration(delta)
            record["declarationReturned"] = declaration is not None
            record["declarationErrors"] = list(errors)
            if declaration is None:
                out.append(
                    f"RT28-RESOLVER {rel} returns NO DECLARATION for this "
                    f"subject: {errors!r}. Section 7.3's rider requires a POSITIVE "
                    f"resolution; `(None, [])` is indistinguishable from 'not a "
                    f"derivation at all'")
                results[rel] = record
                continue
            record["declaredPredecessor"] = declaration["artifact"]
            record["declaredSha256"] = declaration["sha256"]
            record["operationsDeclared"] = len(declaration["operations"])
            base_rel = (f"artifacts/{declaration['artifact']}"
                        if "/" not in declaration["artifact"]
                        else declaration["artifact"])
            base_bytes, reason = read_input(base_rel)
            if base_bytes is None:
                out.append(f"RT28-RESOLVER {rel}: the declared predecessor "
                           f"{base_rel} could not be read ({reason}); this "
                           f"resolver measurement DID NOT RUN")
                results[rel] = record
                continue
            base = json.loads(base_bytes.decode("utf-8"))
            effective, apply_errors = module.apply_operations(
                base, declaration["operations"])
            record["operationsApplied"] = (len(declaration["operations"])
                                           - len(apply_errors))
            record["applyErrors"] = list(apply_errors)
            record["resolvedCanonicalSha256"] = sha_bytes(canonical(effective))
            full, prov, full_errors = module.resolve_derivation(
                f"artifacts/{SUBJECT}", declaration)
            record["fullChain"] = full is not None
            record["fullChainErrors"] = list(full_errors)
            record["provenance"] = prov
        except Exception as exc:  # noqa: BLE001
            out.append(
                f"RT28-RESOLVER {rel} raised while resolving this subject "
                f"({type(exc).__name__}: {exc}); the measurement DID NOT RUN and "
                f"is not reported as a pass")
            results[rel] = record
            continue
        results[rel] = record

    ctx["resolvers"] = results
    if len(results) != 2:
        out.append(f"RT28-RESOLVER only {len(results)} of 2 pinned resolvers "
                   f"produced a record; the artifact declares under BOTH and the "
                   f"claim cannot be checked against one")
        _RESOLVER_CACHE[decl_key] = (results, list(out))
        return out

    operations = ctx.get("operations") or []
    op_paths = {op.get("path") for op in operations}
    for rel, record in sorted(results.items()):
        if not record.get("declarationReturned"):
            continue
        if len(record.get("declarationErrors") or []) != RECORDED["resolverDeclarationErrors"]:
            out.append(f"RT28-RESOLVER {rel}: "
                       f"{len(record['declarationErrors'])} declaration error(s), "
                       f"recorded {RECORDED['resolverDeclarationErrors']}: "
                       f"{record['declarationErrors']!r}")
        if record.get("operationsApplied") != RECORDED["resolverOperationsApplied"]:
            out.append(f"RT28-RESOLVER {rel}: applied "
                       f"{record.get('operationsApplied')} of "
                       f"{record.get('operationsDeclared')} operations, recorded "
                       f"{RECORDED['resolverOperationsApplied']}")
        if len(record.get("applyErrors") or []) != RECORDED["resolverApplyErrors"]:
            out.append(f"RT28-RESOLVER {rel}: "
                       f"{len(record['applyErrors'])} apply error(s), recorded "
                       f"{RECORDED['resolverApplyErrors']}: "
                       f"{record['applyErrors'][:3]!r}")
        if record.get("resolvedCanonicalSha256") != ctx.get("resolvedDigest"):
            out.append(
                f"RT28-RESOLVER {rel} resolves this artifact to "
                f"{record.get('resolvedCanonicalSha256')} and this instrument's "
                f"own resolver produces {ctx.get('resolvedDigest')}. Two "
                f"implementations of one published recipe disagree, so at most "
                f"one of them implements it")
        # THE FULL CHAIN.  It refuses, and the refusal must be attributable to the
        # PREDECESSOR and not to this artifact -- which is exactly what the
        # terminus rule says, measured rather than asserted.
        chain_errors = record.get("fullChainErrors") or []
        if record.get("fullChain"):
            out.append(
                f"RT28-RESOLVER {rel} materialises the FULL CHAIN. The artifact "
                f"publishes that it does not, and section 7.3's terminus rule "
                f"rests on the predecessor being a reviewed standalone that is "
                f"never recursed into. A full chain here means the predecessor's "
                f"change-log parsed as executable, and the resolved value is a "
                f"reconstruction from v25 that no reviewer has seen")
        elif len(chain_errors) != RECORDED["fullChainErrors"]:
            out.append(f"RT28-RESOLVER {rel}: the full chain refuses with "
                       f"{len(chain_errors)} error(s), recorded "
                       f"{RECORDED['fullChainErrors']}")
        mine = [e for e in chain_errors
                if any(f"({op.get('op')} {op.get('path')})" in e
                       for op in operations)
                or any(f" {p})" in e for p in op_paths if isinstance(p, str))]
        if len(mine) != RECORDED["fullChainErrorsNamingThisArtifactsOperations"]:
            out.append(
                f"RT28-RESOLVER {rel}: {len(mine)} of {len(chain_errors)} "
                f"full-chain error(s) name an operation of THIS artifact, "
                f"recorded {RECORDED['fullChainErrorsNamingThisArtifactsOperations']}. "
                f"The chain refusal is a corpus-level finding against both "
                f"resolvers -- they recurse where the review terminus says they "
                f"should stop -- and attributing it to these operations would be "
                f"a false accusation: {mine[:2]!r}")
    digests = {r.get("resolvedCanonicalSha256") for r in results.values()
               if r.get("resolvedCanonicalSha256")}
    if len(digests) > 1:
        out.append(f"RT28-RESOLVER the two pinned resolvers produce DIFFERENT "
                   f"resolved values: {sorted(digests)}")
    _RESOLVER_CACHE[decl_key] = (results, list(out))
    return out


_RESOLVER_CACHE = {}


# ===========================================================================
# SECTION 4 -- CHECKS OVER THE RESOLUTION ITSELF.
# ===========================================================================

def check_resolution(delta, resolved, prov, ctx):
    """Everything the derivation claims about its own product, hard-compared."""
    out = []
    decl_block = get_path(delta, f"$.{prov.get('block', 'derivedFrom')}") or {}
    operations = prov["declaration"]["operations"]

    if prov["predecessorByteDigest"] != RECORDED["predecessorByteSha256"]:
        out.append(f"RT28-DERIV-PREDECESSOR the derivation binds a predecessor "
                   f"whose bytes hash to {prov['predecessorByteDigest']}; this "
                   f"instrument was written against "
                   f"{RECORDED['predecessorByteSha256']}")
    if prov["predecessorCanonicalDigest"] != RECORDED["predecessorCanonicalSha256"]:
        out.append(f"RT28-DERIV-PREDECESSOR the parsed predecessor's canonical "
                   f"value hashes to {prov['predecessorCanonicalDigest']}, not the "
                   f"recorded {RECORDED['predecessorCanonicalSha256']}")

    # The predecessor's canonical-value digest is NESTED one level down, where no
    # resolver scans, precisely so the declaring level states one of each.  It is
    # still a recorded measurement and still gets a hard comparison.
    nested = [v for _p, block in objects_of(decl_block)
              for k, v in block.items()
              if isinstance(v, str) and SHA256_RE.match(v)
              and v == prov["predecessorCanonicalDigest"]]
    if not nested:
        out.append(
            f"RT28-DERIV-CANONICAL the derivation publishes no digest equal to "
            f"the canonical serialisation of its own verified predecessor "
            f"({prov['predecessorCanonicalDigest']}). A derivation's product is a "
            f"VALUE, so the value digest is the one the resolution is defined "
            f"against and it must be stated somewhere in the declaration")

    measured = prov["resolvedCanonicalDigest"]
    ctx["resolvedDigest"] = measured
    declared = None
    for _p, block in objects_of(decl_block):
        recipe = [v for v in block.values()
                  if isinstance(v, str) and "sort_keys=True" in v]
        digests = [v for v in block.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        if recipe and len(digests) == 1:
            declared = digests[0]
    if declared is None:
        out.append("RT28-DERIV-NO-RESOLVED-DIGEST the derivation publishes no "
                   "digest over its own resolved value beside its own "
                   "canonicalisation recipe, so nothing states what the "
                   "resolution is supposed to produce")
    elif declared != measured:
        out.append(f"RT28-DERIV-RESOLVED the derivation declares its resolved "
                   f"value hashes to {declared} and applying its own operations "
                   f"to its own verified predecessor produces {measured}")
    if measured != RECORDED["resolvedCanonicalSha256"]:
        out.append(f"RT28-DERIV-RESOLVED the resolved value hashes to {measured}, "
                   f"not the recorded {RECORDED['resolvedCanonicalSha256']}")

    # THE SUBSTANTIVE-DELTA-IS-PRESERVED CLAIM, re-executed rather than read.
    # The artifact asserts its substantive delta is IDENTICAL to the predecessor
    # lane's.  That is checkable: repair the predecessor lane's operations in FORM
    # ONLY -- rename `to` to `value`, strip the `$.` display prefix, change
    # nothing else -- apply them to the same verified predecessor, and the digest
    # it published must come out.  Had any of the three form repairs altered a
    # value, this digest would move.
    v27_bytes, reason = read_input("artifacts/retention-tiers.v27.json")
    if v27_bytes is None:
        out.append(f"RT28-PRESERVED the predecessor lane's artifact could not be "
                   f"read ({reason}), so the identical-substantive-delta claim "
                   f"WAS NOT CHECKED")
    else:
        try:
            v27 = parse_json(v27_bytes, "retention-tiers.v27.json")
            v27_ops = []
            for op in (get_path(v27, "$.derivedFrom.operations") or []):
                repaired = dict(op)
                if "to" in repaired:
                    repaired["value"] = repaired.pop("to")
                path = repaired.get("path")
                if isinstance(path, str) and path.startswith("$."):
                    repaired["path"] = path[2:]
                v27_ops.append(repaired)
            errs = []
            intended, _applied = apply_operations(prov["parsedPredecessor"],
                                                  v27_ops, errs)
            intended_digest = sha_bytes(canonical(intended)) if not errs else None
            ctx["v27IntendedDigest"] = intended_digest
            ctx["v27FormRepairErrors"] = errs
            if errs:
                out.append(f"RT28-PRESERVED the predecessor lane's operations, "
                           f"repaired in FORM ONLY, do not apply to the same "
                           f"verified predecessor: {errs[:2]!r}")
            elif intended_digest != RECORDED["v27IntendedResolvedSha256"]:
                out.append(
                    f"RT28-PRESERVED repairing the predecessor lane's operations "
                    f"in FORM ONLY and applying them produces {intended_digest}, "
                    f"not the {RECORDED['v27IntendedResolvedSha256']} that lane "
                    f"published. One of the three form repairs altered a VALUE, "
                    f"so this artifact's central claim -- that it changes form "
                    f"and nothing else -- is false")
            else:
                published = get_path(v27, "$.derivedFrom.resolvedValue.sha256")
                if published != intended_digest:
                    out.append(
                        f"RT28-PRESERVED the predecessor lane published "
                        f"{published!r} for its own resolved value and repairing "
                        f"its form reproduces {intended_digest}")
            # And the difference between the two resolved values must be exactly
            # the IDENTITY operations -- derived from the operation classes, not
            # listed.
            if intended_digest:
                before = dict(scalar_leaves(intended))
                after = dict(scalar_leaves(resolved))
                differing = sorted(
                    p for p in set(before) | set(after)
                    if p not in before or p not in after
                    or type(before[p]) is not type(after[p])
                    or before[p] != after[p])
                identity_paths = sorted(
                    "$." + op.get("path") for op in operations
                    if op.get("class") == "IDENTITY")
                ctx["identityOnlyDifference"] = differing
                if differing != identity_paths:
                    out.append(
                        f"RT28-PRESERVED this artifact's resolved value and the "
                        f"predecessor lane's differ at {differing}, and the "
                        f"IDENTITY operations name {identity_paths}. The artifact "
                        f"claims every differing path is an IDENTITY path")
        except PinRefused as exc:
            out.append(f"RT28-PRESERVED the predecessor lane's artifact did not "
                       f"parse ({exc}); the claim WAS NOT CHECKED")

    blob = canonical(resolved).decode("utf-8")
    floats = [(p, v) for p, v in scalar_leaves(resolved) if isinstance(v, float)]
    ctx["resolvedFloatPaths"] = [p for p, _ in floats]
    if len(floats) != 1:
        out.append(f"RT28-DERIV-FLOAT the resolved value carries {len(floats)} "
                   f"floats; the derivation's encoding note names exactly one and "
                   f"a reimplementer is told to expect one")
    elif '"keepCount":200.0' not in blob:
        out.append("RT28-DERIV-FLOAT the canonical serialisation does not carry "
                   "the substring the derivation names, '\"keepCount\":200.0'; a "
                   "float formatter emitting 200 or 2.0e2 produces a different "
                   "digest for the same value")

    if len(operations) != RECORDED["operationCount"]:
        out.append(f"RT28-DERIV-OPCOUNT the derivation carries {len(operations)} "
                   f"operations, not the recorded {RECORDED['operationCount']}")
    classes = {}
    for op in operations:
        classes.setdefault(op.get("class", "<<UNCLASSED>>"), []).append(
            op.get("path"))
    ctx["operationClasses"] = classes
    identity = len(classes.get("IDENTITY", []))
    repair = len(classes.get("REPAIR", []))
    if identity != RECORDED["identityOperations"] or repair != RECORDED["repairOperations"]:
        out.append(f"RT28-DERIV-CLASSES the derivation classifies {identity} "
                   f"IDENTITY and {repair} REPAIR operations; the recorded "
                   f"measurement is {RECORDED['identityOperations']} and "
                   f"{RECORDED['repairOperations']}")
    if identity + repair != len(operations):
        out.append(f"RT28-DERIV-CLASSES {len(operations) - identity - repair} "
                   f"operation(s) carry no IDENTITY/REPAIR class, so the "
                   f"substantive delta cannot be separated from the identity delta "
                   f"by anything but reading")
    for op in operations:
        if op.get("class") == "IDENTITY" and str(op.get("path", "")).startswith(
                "corpusResiduals"):
            out.append(f"RT28-DERIV-CLASSES {op.get('path')} is classed IDENTITY "
                       f"and lands inside the residual block whose figures this "
                       f"artifact exists to repair")
    # No operation may carry the `$.` display prefix, and none may carry `to`:
    # those are two of the three form defects this artifact repairs, so a
    # regression of either is a finding rather than a silent refusal downstream.
    for index, op in enumerate(operations):
        if isinstance(op.get("path"), str) and op["path"].startswith("$."):
            out.append(f"RT28-DERIV-PATH operation {index} spells its path with "
                       f"the `$.` DISPLAY prefix, which both corpus resolvers "
                       f"tokenise to a first step named `$`")
        if "to" in op and "value" not in op:
            out.append(f"RT28-DERIV-NO-VALUE operation {index} carries its payload "
                       f"at `to`; both corpus resolvers require `value`")

    base = prov["parsedPredecessor"]
    before = dict(scalar_leaves(base))
    after = dict(scalar_leaves(resolved))
    differing = sorted(
        p for p in set(before) | set(after)
        if p not in before or p not in after
        or type(before[p]) is not type(after[p]) or before[p] != after[p])
    op_paths = sorted({"$." + op.get("path") if not str(op.get("path")).startswith("$")
                       else op.get("path") for op in operations})
    ctx["differingLeafPaths"] = differing
    if differing != op_paths:
        out.append(
            f"RT28-DERIV-EXACTLY the set of leaf paths at which the resolved value "
            f"differs from the verified predecessor is not the set of operation "
            f"paths. Moved but not declared: "
            f"{sorted(set(differing) - set(op_paths))}. Declared but did not move: "
            f"{sorted(set(op_paths) - set(differing))}")
    published = get_path(delta, f"$.{prov['block']}.resolutionIsExactlyTheOperations."
                                f"differingLeafPaths")
    if isinstance(published, list) and sorted(published) != differing:
        out.append(f"RT28-DERIV-EXACTLY the derivation publishes a differing-leaf "
                   f"list of {len(published)} path(s) and the measured set has "
                   f"{len(differing)}; symmetric difference "
                   f"{sorted(set(published) ^ set(differing))}")
    for name, value in (("differingLeafPathCount", len(differing)),
                        ("operationPathCount", len(op_paths))):
        declared_count = get_path(
            delta, f"$.{prov['block']}.resolutionIsExactlyTheOperations.{name}")
        if exact_int(declared_count) and declared_count != value:
            out.append(f"RT28-DERIV-EXACTLY {name} declares {declared_count} and "
                       f"the measurement is {value}")
    return out


def check_path_encoding_corroboration(delta, ctx, snaps):
    """The artifact's third form defect is that the predecessor lane spelled every
    operation path with the `$.` DISPLAY prefix, which both resolvers tokenise to
    a first step named `$`.  Its corpusEvidence for the repair is a claim ABOUT
    OTHER ARTIFACTS: that the derivations which RESOLVE spell their paths as bare
    dotted strings and carry no `$.`, and that the ones refused SILENTLY use the
    array-of-tokens encoding.

    That is prose asserting a MEASUREMENT, so section 7.2.2 makes it the bindable
    kind, and it is re-measured here from the five artifacts the delta file
    RECORDS AS INPUTS.  Recording an input a run never opens is the other half of
    the same defect: a recorded dependency nothing reads is a dependency nobody
    can check.
    """
    out = []
    cache_key = tuple(sorted(
        (rel, sha_bytes(snaps[rel])) for rel in PER_CLASS_INPUTS if rel in snaps))
    if cache_key in _PATH_ENCODING_CACHE:
        measured = _PATH_ENCODING_CACHE[cache_key]
        ctx["pathEncoding"] = measured
        return _path_encoding_verdicts(measured, ctx)
    measured = {"stringPaths": 0, "arrayPaths": 0, "dollarPrefixed": 0,
                "examined": 0, "unavailable": []}
    for rel in sorted(PER_CLASS_INPUTS):
        if PER_CLASS_INPUTS[rel] != "pathEncodingCorroboration":
            continue
        data = snaps.get(rel)
        if data is None:
            measured["unavailable"].append(rel)
            continue
        try:
            doc = parse_json(data, rel)
        except PinRefused as exc:
            measured["unavailable"].append(f"{rel} ({exc})")
            continue
        if not isinstance(doc, dict):
            measured["unavailable"].append(f"{rel} (not a JSON object)")
            continue
        for _p, block in objects_of(doc):
            if not isinstance(block, dict):
                continue
            for value in block.values():
                if not isinstance(value, list) or not value:
                    continue
                if not all(isinstance(i, dict) and isinstance(i.get("op"), str)
                           for i in value):
                    continue
                measured["examined"] += 1
                for item in value:
                    path = item.get("path")
                    if isinstance(path, str):
                        measured["stringPaths"] += 1
                        if path.startswith("$."):
                            measured["dollarPrefixed"] += 1
                    elif isinstance(path, list):
                        measured["arrayPaths"] += 1
    _PATH_ENCODING_CACHE[cache_key] = measured
    ctx["pathEncoding"] = measured
    return _path_encoding_verdicts(measured, ctx)


_PATH_ENCODING_CACHE = {}


def _path_encoding_verdicts(measured, ctx):
    """The verdicts, split from the measurement so the measurement can be
    memoised on the bytes it read and the verdicts stay per-run."""
    out = []
    ctx["pathEncoding"] = measured
    if measured["unavailable"]:
        ctx.setdefault("partScoped", []).append(
            f"RT28-CLASS-SKIPPED pathEncodingCorroboration: "
            f"{measured['unavailable']} unavailable, so the corpus evidence for "
            f"the path-encoding repair WAS NOT RE-MEASURED")
        return out
    if measured["stringPaths"] + measured["arrayPaths"] == 0:
        out.append("RT28-PATHENC none of the recorded corroboration artifacts "
                   "carries an operation list, so the artifact's corpusEvidence "
                   "for the path-encoding repair rests on nothing this run can "
                   "see")
        return out
    if measured["dollarPrefixed"]:
        out.append(
            f"RT28-PATHENC {measured['dollarPrefixed']} operation path(s) in the "
            f"recorded corroboration artifacts DO carry the `$.` display prefix. "
            f"The artifact's corpusEvidence says NONE does, and that claim is the "
            f"whole justification for its third form repair")
    if measured["arrayPaths"] == 0:
        out.append(
            "RT28-PATHENC none of the recorded corroboration artifacts uses the "
            "ARRAY-of-tokens path encoding. The artifact records two of them "
            "precisely as examples of it -- the encoding section 7.3's 2026-08-10 "
            "rider calls better designed and silently refused -- so at zero the "
            "contrast its RT28-RES-06 rests on is not present in these bytes")
    if measured["stringPaths"] == 0:
        out.append(
            "RT28-PATHENC none of the recorded corroboration artifacts uses the "
            "STRING path encoding this artifact adopted, so the claim that it is "
            "the encoding resolving derivations use is unsupported here")
    return out


def check_terminus(delta, prov, ctx):
    """The terminus decision, published as data and hard-compared.  Section 7.3's
    2026-08-10 resolution is the newest rule in the corpus and this instrument is
    the first to implement it BY THE REVIEW TEST; a rule implemented and not
    reported is a rule nobody can audit."""
    out = []
    report = prov.get("terminus") or {}
    ctx["terminus"] = report
    if not report:
        out.append("RT28-TERMINUS no terminus decision was recorded, so the "
                   "resolution cannot say why it stopped where it stopped")
        return out
    if report.get("populationUnreadable"):
        # A LOWER BOUND IS A COVERAGE LOSS, NOT AN ACCUSATION.  The discovery
        # sweep could not read part of the corpus, so it cannot establish that no
        # review exists.  That is a statement about this run, and emitting it as a
        # finding would put a fact about the tree into the channel reserved for
        # facts about the subject -- section 7.8.1's whole subject.
        ctx.setdefault("classSkips", []).append(
            f"RT28-CLASS-SKIPPED terminusDiscovery: "
            f"{report['populationUnreadable']} of {report['populationScanned']} "
            f"corpus documents could not be read, so the discovered review "
            f"population is a LOWER BOUND and the ABSENCE of a review has NOT "
            f"been established. The terminus decision itself "
            f"{'still holds on the review that WAS found' if report.get('isTerminus') else 'could not be made'}")
    if not report.get("isTerminus"):
        out.append(
            f"RT28-TERMINUS the declared predecessor {report.get('predecessor')} "
            f"is NOT a review terminus: {report.get('why')}. The chain was "
            f"resolved rather than stopped, and section 7.3's 2026-08-10 rule "
            f"says that replaces the only reviewed bytes in the chain with a "
            f"reconstruction no reviewer has seen")
    if report.get("blockingFindings") not in (None,
                                              RECORDED["terminusReviewBlockingFindings"]):
        out.append(f"RT28-TERMINUS the review that establishes the terminus "
                   f"reports {report['blockingFindings']} blocking finding(s), "
                   f"recorded {RECORDED['terminusReviewBlockingFindings']}")
    if report.get("reviewCount", 0) < 1:
        out.append("RT28-TERMINUS the corpus sweep discovered NO review of the "
                   "declared predecessor, so the terminus rests on nothing that "
                   "was measured")
    # The predecessor DOES carry a declaration SHAPE.  If it ever stops carrying
    # one, the terminus test is no longer doing any work and a shape screen would
    # have been enough -- which is worth knowing, because it would mean this
    # instrument's central design choice had become untested.
    if not prov.get("predecessorHasDeclarationSHAPE"):
        out.append(
            "RT28-TERMINUS the declared predecessor no longer carries a "
            "derivation-shaped block, so the REVIEW-terminus test is no longer "
            "separating anything a shape screen would not. The rule still holds; "
            "the evidence for needing it has gone, and that is reported rather "
            "than left as a silent tautology")
    return out


# ===========================================================================
# SECTION 5 -- CENSUS, KEY LOCATOR, PIN HYGIENE, IDENTITY, RESIDUALS.
# ===========================================================================

def check_census(delta, resolved, prov, ctx):
    """The inherited census is section 7.3's named silent-staleness site.  Every
    operation is a set on an existing scalar leaf and none changes a type, so the
    predecessor's own $.leafCensus must be EXACT of the resolved document.  This
    re-walks both and compares, and PUBLISHES THE INT-FIRST CONTROL: bool
    subclasses int in Python, and testing int first reports 788 against the true
    439."""
    out = []
    resolved_c = census(resolved)
    delta_c = census(delta)
    ctx["resolvedCensus"] = resolved_c
    ctx["deltaCensus"] = delta_c

    for label, measured in (("resolved", resolved_c), ("delta", delta_c)):
        if measured["intLeafPositions"] + measured["boolLeafPositions"] != \
                measured["intFirstControl_intLeafPositions"]:
            out.append(f"RT28-CENSUS the {label} int-first control does not equal "
                       f"int+bool, so the bool-before-int ordering this census "
                       f"depends on is not doing what it claims")
    if resolved_c["intFirstControl_intLeafPositions"] != RECORDED["resolvedIntFirstControl"]:
        out.append(f"RT28-CENSUS the int-first control over the resolved value "
                   f"reports {resolved_c['intFirstControl_intLeafPositions']}, not "
                   f"the recorded {RECORDED['resolvedIntFirstControl']}. That "
                   f"control is published because it is the number a census with "
                   f"the ordering defect would report")
    if resolved_c["intLeafPositions"] != RECORDED["resolvedIntLeaves"]:
        out.append(f"RT28-CENSUS the resolved value carries "
                   f"{resolved_c['intLeafPositions']} non-bool int leaves, not the "
                   f"recorded {RECORDED['resolvedIntLeaves']}")

    keys = ("scalarLeafPositions", "nonStringLeafPositions", "intLeafPositions",
            "floatLeafPositions", "boolLeafPositions", "nullLeafPositions",
            "stringLeafPositions")
    inherited = get_path(resolved, "$.leafCensus") or {}
    for key in keys:
        declared = inherited.get(key)
        if not exact_int(declared):
            out.append(f"RT28-CENSUS the resolved document's $.leafCensus.{key} is "
                       f"{declared!r}, not a JSON integer")
            continue
        if declared != resolved_c[key]:
            out.append(
                f"RT28-CENSUS the inherited $.leafCensus.{key} declares {declared} "
                f"and a walk of the RESOLVED value measures {resolved_c[key]}. "
                f"Section 7.3's rider names the inherited census as the "
                f"silent-staleness site: an inherited measurement is republished "
                f"under the successor's name and ages invisibly")
    for key, measured in (("floatLeafPaths", resolved_c["floatLeafPaths"]),
                          ("nullLeafPaths", resolved_c["nullLeafPaths"])):
        declared = inherited.get(key)
        if isinstance(declared, list) and sorted(declared) != sorted(measured):
            out.append(f"RT28-CENSUS the inherited $.leafCensus.{key} and the "
                       f"resolved walk differ: "
                       f"{sorted(set(declared) ^ set(measured))}")

    published = get_path(delta, f"$.{prov['block']}.resolvedDocumentCensus") or {}
    for key in keys:
        declared = published.get(key)
        if exact_int(declared) and declared != resolved_c[key]:
            out.append(f"RT28-CENSUS the derivation's own resolvedDocumentCensus."
                       f"{key} declares {declared} and the resolved walk measures "
                       f"{resolved_c[key]}")
    pred_scalars = published.get("predecessorScalarLeafPositions")
    measured_pred = census(prov["parsedPredecessor"])["scalarLeafPositions"]
    if exact_int(pred_scalars) and pred_scalars != measured_pred:
        out.append(f"RT28-CENSUS resolvedDocumentCensus.predecessorScalarLeafPositions "
                   f"declares {pred_scalars} and the predecessor walk measures "
                   f"{measured_pred}")

    own = get_path(delta, "$.leafCensusOfThisDeltaFile") or {}
    for key in keys:
        declared = own.get(key)
        if not exact_int(declared):
            out.append(f"RT28-CENSUS $.leafCensusOfThisDeltaFile.{key} is "
                       f"{declared!r}, not a JSON integer")
            continue
        if declared != delta_c[key]:
            out.append(
                f"RT28-CENSUS $.leafCensusOfThisDeltaFile.{key} declares "
                f"{declared} and a walk of the WRITTEN BYTES measures "
                f"{delta_c[key]}. Section 7.2.2 records four instances of a "
                f"self-report measured before it was attached to the object it "
                f"describes, undercounting by exactly its own size")
    for key, measured in (("floatLeafPaths", delta_c["floatLeafPaths"]),
                          ("nullLeafPaths", delta_c["nullLeafPaths"])):
        declared = own.get(key)
        if isinstance(declared, list) and sorted(declared) != sorted(measured):
            out.append(f"RT28-CENSUS $.leafCensusOfThisDeltaFile.{key} and the "
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
            out.append(f"RT28-CENSUS $.leafCensusOfThisDeltaFile.arithmetic reads "
                       f"{arithmetic!r}; regenerated from the walk it is "
                       f"{expected!r}")
    if resolved_c["scalarLeafPositions"] != RECORDED["resolvedScalarLeaves"]:
        out.append(f"RT28-CENSUS the resolved value has "
                   f"{resolved_c['scalarLeafPositions']} scalar leaves, not the "
                   f"recorded {RECORDED['resolvedScalarLeaves']}")
    if delta_c["scalarLeafPositions"] != RECORDED["deltaScalarLeaves"]:
        out.append(f"RT28-CENSUS the delta file has "
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
        out.append("RT28-KEYLOC the delta file carries no keyLocator, so nothing "
                   "states which of its keys are the resolved document's and which "
                   "are the delta's own -- CMP-IR-01's exact setup")
        return out
    delta_keys = set(delta)
    resolved_keys = set(resolved)
    op_target = block.get("operationTargetKeys") or []
    restated = block.get("restatedIdenticalKeys") or []
    delta_only = block.get("deltaOnlyKeys") or []
    resolved_only = block.get("resolvedOnlyKeys") or []

    bad = sorted(k for k in delta_only if k in resolved_keys)
    if bad:
        out.append(f"RT28-KEYLOC direction1: {len(bad)} key(s) classed DELTA-ONLY "
                   f"are present in the resolved document: {bad}")
    bad = sorted(k for k in resolved_only if k in delta_keys)
    if bad:
        out.append(f"RT28-KEYLOC direction2: {len(bad)} key(s) classed "
                   f"RESOLVED-ONLY are top-level keys of this delta file: {bad}. "
                   f"This is versioning-policy.v14's only blocker exactly")
    for key in op_target:
        if key not in delta_keys:
            out.append(f"RT28-KEYLOC direction3: {key} is classed OPERATION-TARGET "
                       f"and is not a top-level key here")
        elif key not in resolved_keys:
            out.append(f"RT28-KEYLOC direction3: {key} is classed OPERATION-TARGET "
                       f"and is absent from the resolved document")
        elif not exact_equal(delta[key], resolved[key]):
            out.append(f"RT28-KEYLOC direction3: {key} is {delta[key]!r} here and "
                       f"{resolved[key]!r} in the resolved document, so this file "
                       f"describes a document it did not produce")
    for key in restated:
        if key not in delta_keys or key not in resolved_keys:
            out.append(f"RT28-KEYLOC direction4: {key} is classed "
                       f"RESTATED-IDENTICAL and is missing from one side")
        elif not exact_equal(delta[key], resolved[key]):
            out.append(f"RT28-KEYLOC direction4: {key} is {delta[key]!r} here and "
                       f"{resolved[key]!r} in the resolved document")
    classified = set(op_target) | set(restated) | set(delta_only)
    unclassified = sorted(delta_keys - classified)
    if unclassified:
        out.append(f"RT28-KEYLOC direction5: {len(unclassified)} top-level key(s) "
                   f"of this file fall in no class: {unclassified}")
    extra = sorted(classified - delta_keys)
    if extra:
        out.append(f"RT28-KEYLOC direction5: {len(extra)} key(s) are classified and "
                   f"are not top-level keys of this file: {extra}")
    touched = sorted({(path_steps(op.get("path")) or ["?"])[0]
                      for op in (ctx.get("operations") or [])})
    also_here = sorted(k for k in touched if k in delta_keys)
    asserted_absent = sorted(k for k in touched if k not in delta_keys)
    verification = block.get("verification") or {}
    d6 = verification.get("direction6_everyTopLevelKeyNamedByAnOperationIsClassifiedCorrectlyHere") or {}
    for name, measured in (("touchedByOperations", touched),
                           ("alsoTopLevelHere", also_here),
                           ("assertedAbsentHere", asserted_absent)):
        declared = d6.get(name)
        if isinstance(declared, list) and sorted(declared) != measured:
            out.append(f"RT28-KEYLOC direction6: {name} declares {sorted(declared)} "
                       f"and the operations touch {measured}")
    measured_resolved_only = sorted(resolved_keys - delta_keys)
    if isinstance(resolved_only, list) and sorted(resolved_only) != measured_resolved_only:
        out.append(f"RT28-KEYLOC resolvedOnlyKeys is not the measured set; "
                   f"symmetric difference "
                   f"{sorted(set(resolved_only) ^ set(measured_resolved_only))}")
    # The published verification block claims six directions HOLD with zero
    # violations.  A claim that a check passed is itself a recorded measurement.
    for name, expected in (("direction1_everyKeyCalledDELTA_ONLY_isAbsentFromTheResolvedDocument",
                            len(delta_only)),
                           ("direction2_everyKeyCalledRESOLVED_ONLY_isAbsentFromThisDeltaFile",
                            len(resolved_only)),
                           ("direction3_everyOPERATION_TARGET_keyIsPresentInBOTH_andEQUALatExactType",
                            len(op_target)),
                           ("direction4_everyRESTATED_IDENTICAL_keyIsPresentInBothAndEQUALatExactType",
                            len(restated))):
        row = verification.get(name) or {}
        checked = row.get("checked")
        if exact_int(checked) and checked != expected:
            out.append(f"RT28-KEYLOC {name}.checked declares {checked} and the "
                       f"class it walks holds {expected}")
        if row.get("holds") is True and (row.get("violations") or []):
            out.append(f"RT28-KEYLOC {name} declares holds=true beside a non-empty "
                       f"violations list")
    if len(delta_keys) != RECORDED["deltaTopLevelKeys"]:
        out.append(f"RT28-KEYLOC the delta file exposes {len(delta_keys)} top-level "
                   f"keys, not the recorded {RECORDED['deltaTopLevelKeys']}")
    if len(resolved_keys) != RECORDED["resolvedTopLevelKeys"]:
        out.append(f"RT28-KEYLOC the resolved document has {len(resolved_keys)} "
                   f"top-level keys, not the recorded "
                   f"{RECORDED['resolvedTopLevelKeys']}")
    ctx["keyLocatorDirections"] = 6
    return out


def check_recorded_inputs(delta, ctx, destroyed):
    """Section 7.10: classify every input GATED / ADVANCING / DESTROYED, and
    compare this instrument's table against the artifact's IN BOTH DIRECTIONS, so
    a row that silently changes class is a finding.

    Standing is DISCOVERED, not listed: the DESTROYED row's unrecoverability is
    MEASURED by the tree sweep in destroyed_standing(), and the fact that the
    file STILL EXISTS at other bytes -- mutated, not deleted -- is measured too,
    because a reader who checks only existence concludes the pin is satisfiable.
    """
    out = []
    block = get_path(delta, "$.recordedInputsOfThisDeltaFile")
    if not isinstance(block, dict):
        out.append("RT28-INPUTS the delta file records no inputs. Section 7.2's "
                   "recording obligation: a count is not a record, and neither is "
                   "an absence")
        return out
    recorded = block.get("recorded") or []
    declared = {}
    for row in recorded:
        path = row.get("path")
        gate = str(row.get("gate") or "")
        klass = row.get("class")
        declared[path] = (klass, gate, row.get("sha256"))
        if klass == "GATED" and "HARD-PIN" not in gate:
            out.append(f"RT28-INPUTS {path} is classed GATED and its gate string "
                       f"is {gate!r}; a GATED row must carry the artifact's own "
                       f"hard-pin gate")
        if klass == "ADVANCING" and "NOT-GATED" not in gate:
            out.append(f"RT28-INPUTS {path} is classed ADVANCING and its gate "
                       f"string is {gate!r}")

    for path, expected in GATED_PINS.items():
        if path not in declared:
            if path in INSTRUMENT_OWNED_GATES:
                continue
            out.append(f"RT28-INPUTS this instrument GATES {path} and the artifact "
                       f"records no such input, so the gate rests on this file's "
                       f"transcription rather than on the artifact's "
                       f"classification")
        elif declared[path][0] != "GATED":
            out.append(f"RT28-INPUTS {path} is GATED here and "
                       f"{declared[path][0]!r} in the artifact")
        elif declared[path][2] != expected:
            out.append(f"RT28-INPUTS {path}: the artifact records "
                       f"{declared[path][2]} and this instrument gates {expected}")
    for path, expected in ADVANCING_PINS.items():
        if path not in declared:
            out.append(f"RT28-INPUTS this instrument classes {path} ADVANCING and "
                       f"the artifact records no such input")
        elif declared[path][0] != "ADVANCING":
            out.append(f"RT28-INPUTS {path} is ADVANCING here and "
                       f"{declared[path][0]!r} in the artifact")
        elif declared[path][2] != expected:
            out.append(f"RT28-INPUTS {path}: the artifact records "
                       f"{declared[path][2]} and this instrument's ADVANCING "
                       f"baseline is {expected}. The baseline is what a drift "
                       f"notice prints against; replacing it with today's value "
                       f"erases the record rather than checking it")
    for path in declared:
        if path not in GATED_PINS and path not in ADVANCING_PINS:
            out.append(f"RT28-INPUTS the artifact records {path} and this "
                       f"instrument neither gates it nor classes it advancing, so "
                       f"an input the artifact depends on is unguarded here")

    gated = sum(1 for v in declared.values() if v[0] == "GATED")
    advancing = sum(1 for v in declared.values() if v[0] == "ADVANCING")
    destroyed_rows = block.get("destroyed") or []
    # digestsRecordedCount's referent is the WHOLE record -- recorded plus
    # destroyed -- and that is checked as an arithmetic closure rather than
    # guessed from the key name.
    for name, measured, referent in (
            ("gatedCount", gated, "rows classed GATED"),
            ("advancingCount", advancing, "rows classed ADVANCING"),
            ("destroyedCount", len(destroyed_rows), "destroyed rows"),
            ("digestsRecordedCount", len(recorded) + len(destroyed_rows),
             "recorded rows plus destroyed rows")):
        value = block.get(name)
        if exact_int(value) and value != measured:
            out.append(f"RT28-INPUTS {name} declares {value} and its referent "
                       f"({referent}) measures {measured}")
    if gated + advancing != len(recorded):
        out.append(f"RT28-INPUTS {len(recorded) - gated - advancing} recorded "
                   f"row(s) carry neither GATED nor ADVANCING, so the "
                   f"classification is not a partition of the record")

    for row in destroyed_rows:
        if row.get("destroyedSha256") != DESTROYED_DIGEST:
            out.append(f"RT28-INPUTS the artifact records a destroyed digest "
                       f"{row.get('destroyedSha256')} and this instrument's "
                       f"recorded measurement is {DESTROYED_DIGEST}")
        if row.get("path") != DESTROYED_PATH:
            out.append(f"RT28-INPUTS the destroyed pin names {row.get('path')!r}, "
                       f"not {DESTROYED_PATH!r}")
        # MUTATED, NOT DELETED -- measured, both halves.
        still = row.get("theFileSTILLEXISTSAtDifferentBytes")
        if still is not None and still is not destroyed["pathStillExists"]:
            out.append(
                f"RT28-INPUTS the destroyed row declares "
                f"theFileSTILLEXISTSAtDifferentBytes={still!r} and the tree "
                f"measures {destroyed['pathStillExists']!r}. That distinction is "
                f"the whole point of the row: a reader who checks only that the "
                f"path exists concludes the pin is satisfiable")
        live_declared = row.get("liveSha256AtThisAuthoring")
        if isinstance(live_declared, str) and destroyed["pathLiveDigest"] \
                and live_declared != destroyed["pathLiveDigest"]:
            out.append(
                f"RT28-INPUTS-ADVANCED the destroyed row records the surviving "
                f"file at {live_declared[:16]}... and it now reads "
                f"{destroyed['pathLiveDigest'][:16]}.... NOT a claim about the "
                f"destroyed bytes, which remain unrecoverable; the SURVIVING file "
                f"has moved again and the row dates a measurement that has aged")
        if destroyed["pathLiveEqualsDestroyed"]:
            out.append("RT28-INPUTS the surviving file now hashes to the DESTROYED "
                       "digest, which cannot happen honestly: those bytes are in "
                       "no commit on any branch")
    if DESTROYED_DIGEST in {v[2] for v in declared.values()}:
        out.append("RT28-INPUTS a LIVE recorded digest equals the destroyed one, "
                   "so a pin that can never be satisfied is being presented as one "
                   "that is")
    if not destroyed_rows:
        out.append("RT28-INPUTS the artifact records NO destroyed pin. The "
                   "amendment draft's original bytes are unrecoverable and this "
                   "instrument refuses them by digest; an artifact that stops "
                   "naming the row leaves a reader to discover it by hunting a "
                   "corruption")
    ctx["destroyedStanding"] = destroyed
    return out


def check_identity(delta, resolved, ctx):
    """The delta file's own header, and the resolved document's, each compared to
    what the operations install.  Nothing here asserts that CD-RT-5 is DECIDED or
    anything else: section 7.10's rule is to pin the PROPERTY, not the CURRENT
    VALUE, whenever the value is something the corpus is waiting to change."""
    out = []
    expected_name = SUBJECT[:-len(".json")]
    if delta.get("artifact") != expected_name:
        out.append(f"RT28-RECORD $.artifact is {delta.get('artifact')!r}; this "
                   f"instrument's subject is {expected_name!r}")
    if delta.get("version") != 28 or isinstance(delta.get("version"), bool):
        out.append(f"RT28-RECORD $.version is {delta.get('version')!r}, not the "
                   f"JSON integer 28")
    if resolved.get("artifact") != expected_name:
        out.append(f"RT28-RECORD the RESOLVED document's $.artifact is "
                   f"{resolved.get('artifact')!r}. A successor that leaves the "
                   f"predecessor's name in place is the inherited-self-name half "
                   f"of section 7.3's rider")
    if resolved.get("version") != 28 or isinstance(resolved.get("version"), bool):
        out.append(f"RT28-RECORD the RESOLVED document's $.version is "
                   f"{resolved.get('version')!r}, not the JSON integer 28")
    for key in ("status", "claimId", "sealRecommendation", "retainedChecker"):
        if key in delta and key in resolved and not exact_equal(delta[key],
                                                               resolved[key]):
            out.append(f"RT28-RECORD ${key} is {delta[key]!r} in this file and "
                       f"{resolved[key]!r} in the resolved document")
    status = str(delta.get("status") or "")
    if "CANDIDATE-NOT-APPLIED" not in status:
        out.append(f"RT28-RECORD $.status is {status!r}; section 7.1 grades a "
                   f"candidate whose retained checker is a companion written after "
                   f"the fact DISQUALIFYING FOR APPLICATION, and an applied status "
                   f"would be a claim this run cannot support")
    if delta.get("sealRecommendation") != "DO-NOT-SEAL":
        out.append(f"RT28-RECORD $.sealRecommendation is "
                   f"{delta.get('sealRecommendation')!r}, not DO-NOT-SEAL")
    binds = get_path(delta, "$.bindsNothing") or {}
    if binds.get("filesEdited") not in (0, None):
        out.append(f"RT28-RECORD $.bindsNothing.filesEdited is "
                   f"{binds.get('filesEdited')!r}; a candidate that edits anything "
                   f"is not a candidate")
    head_claim = str(binds.get("theNamedArchitectureHeadIsUnchanged") or "")
    if head_claim and "retention-tiers.v24" not in head_claim:
        out.append(f"RT28-RECORD $.bindsNothing.theNamedArchitectureHeadIsUnchanged "
                   f"does not name retention-tiers.v24: {head_claim[:120]!r}")
    # $.retainedChecker is NONE in the artifact as published.  THIS FILE DOES NOT
    # CHANGE THAT and does not assert it should say otherwise -- section 7.8: a
    # companion instrument written after the fact does not discharge the residual,
    # and rewriting the artifact's own admission would be the closure-overclaim
    # class section 7.2.2's 2026-08-05 rider records.
    ctx["retainedCheckerField"] = delta.get("retainedChecker")
    return out


def check_own_residuals(delta, resolved, ctx):
    """Every measured value the artifact publishes about ITSELF, hard-compared."""
    out = []
    residuals = get_path(delta, "$.newResidualsOfThisSuccessor") or []
    count = get_path(delta, "$.newResidualCountOfThisSuccessor")
    if exact_int(count) and count != len(residuals):
        out.append(f"RT28-RESIDUAL $.newResidualCountOfThisSuccessor declares "
                   f"{count} and the array holds {len(residuals)}")
    ids = [r.get("id") for r in residuals]
    if len(set(ids)) != len(ids):
        out.append(f"RT28-RESIDUAL residual ids repeat: {ids}")

    live_referents = {
        "vectorsInTheResolvedDocument":
            len(get_path(resolved, "$.partC_retentionBounds.vectors.rows") or []),
        "invariantsInTheResolvedDocument":
            len(get_path(resolved, "$.partC_retentionBounds.invariants") or []),
        "declarationErrorsUnderBothResolvers": 0,
        "applyOperationsErrorsUnderBothResolvers": 0,
        "fullChainResolveDerivationErrors": RECORDED["fullChainErrors"],
        "errorsAttributableToThisArtifactsOwnOperations": 0,
        "predecessorsWhoseBytesThisArtifactMayEdit": 0,
        "resolversInThisCorpus": 2,
        "resolverExecutionsAtAuthoring": 2,
    }
    resolver_records = ctx.get("resolvers") or {}
    if resolver_records:
        live_referents["declarationErrorsUnderBothResolvers"] = sum(
            len(r.get("declarationErrors") or []) for r in resolver_records.values())
        live_referents["applyOperationsErrorsUnderBothResolvers"] = sum(
            len(r.get("applyErrors") or []) for r in resolver_records.values())
        chains = [len(r.get("fullChainErrors") or [])
                  for r in resolver_records.values()]
        if chains:
            live_referents["fullChainResolveDerivationErrors"] = max(chains)

    for residual in residuals:
        measured = residual.get("measuredValues") or {}
        for key, live in live_referents.items():
            if key in measured and exact_int(measured[key]) and measured[key] != live:
                out.append(f"RT28-RESIDUAL {residual.get('id')} declares {key} "
                           f"{measured[key]} and its referent measures {live}")
        for key in ("vectorsMechanicallyExercisedAgainstIt",
                    "invariantsMechanicallyExercisedAgainstIt"):
            if measured.get(key) not in (0, None):
                out.append(f"RT28-RESIDUAL {residual.get('id')} declares {key} "
                           f"{measured[key]!r} while $.retainedChecker is "
                           f"{resolved.get('retainedChecker')!r}")
        if "retainedCheckers" in measured and measured["retainedCheckers"] != 0:
            out.append(f"RT28-RESIDUAL {residual.get('id')} declares "
                       f"retainedCheckers {measured['retainedCheckers']!r}; the "
                       f"artifact's own $.retainedChecker is "
                       f"{resolved.get('retainedChecker')!r} and this instrument "
                       f"does not change it")

    carried = get_path(delta, "$.residualsLeftOpen.fromTheV26IndependentReview") or []
    from_v27 = get_path(delta, "$.residualsLeftOpen.fromRetentionTiersV27") or []
    for name, measured in (("countFromTheV26Review", len(carried)),
                           ("countFromV27", len(from_v27))):
        value = get_path(delta, f"$.residualsLeftOpen.{name}")
        if exact_int(value) and value != measured:
            out.append(f"RT28-RESIDUAL $.residualsLeftOpen.{name} declares {value} "
                       f"and the array it counts holds {measured}")
    closed = get_path(delta, "$.residualsLeftOpen.countClosed")
    if exact_int(closed) and closed != 0:
        out.append(f"RT28-RESIDUAL countClosed declares {closed}; a form-repair "
                   f"successor that closes a residual has re-opened a block an "
                   f"independent ACCEPT was granted for")
    for entry in list(carried) + list(from_v27):
        if not str(entry.get("status") or "").startswith("OPEN"):
            out.append(f"RT28-RESIDUAL {entry.get('id')} is carried with status "
                       f"{entry.get('status')!r}; a residual is left open by "
                       f"NAMING it, never by relabelling it")

    # The inherited residual registers, re-counted against the RESOLVED value.
    inherited = get_path(delta, "$.inheritedMeasurementDisposition."
                                "theInheritedRESIDUALREGISTERS") or {}
    for name, path in (("retainedResidualCount", "$.retainedResiduals"),
                       ("newResidualCount", "$.newResiduals"),
                       ("retainedResidualsWhoseBasisMovedCount",
                        "$.retainedResidualsWhoseBasisMoved"),
                       ("corpusResidualCount", "$.corpusResiduals")):
        declared = inherited.get(name)
        live = len(get_path(resolved, path) or [])
        if exact_int(declared) and declared != live:
            out.append(f"RT28-RESIDUAL inheritedMeasurementDisposition.{name} "
                       f"declares {declared} and {path} in the resolved document "
                       f"holds {live}")
    if inherited.get("closedByThisSuccessor") not in (0, None):
        out.append(f"RT28-RESIDUAL the artifact declares "
                   f"{inherited.get('closedByThisSuccessor')!r} residual(s) closed "
                   f"by this successor; a form repair closes none")

    # The recorded-inputs re-measurement, row by row against live bytes.  These
    # are the digests the RESOLVED document republishes under this artifact's
    # name -- section 7.3's 2026-08-05 rider, the inherited-measurement site.
    disposition = get_path(delta, "$.inheritedMeasurementDisposition."
                                  "theInheritedRecordedInputsDigests") or {}
    rows = disposition.get("measurement") or []
    moved = unchanged = 0
    for row in rows:
        path = row.get("path")
        claimed_live = row.get("liveAtThisAuthoring")
        claimed_unchanged = row.get("unchanged")
        recorded_by_pred = row.get("recordedByThePredecessor")
        if not isinstance(path, str):
            continue
        if claimed_unchanged is True:
            unchanged += 1
        elif claimed_unchanged is False:
            moved += 1
        if isinstance(recorded_by_pred, str) and isinstance(claimed_live, str):
            if (recorded_by_pred == claimed_live) is not (claimed_unchanged is True):
                out.append(
                    f"RT28-RESIDUAL the re-measurement row for {path} declares "
                    f"unchanged={claimed_unchanged!r} while the predecessor's "
                    f"digest and the recorded live digest "
                    f"{'agree' if recorded_by_pred == claimed_live else 'differ'}")
        # A row claiming UNCHANGED is a claim about bytes and is checked against
        # them.  A row claiming MOVED names a file the corpus is waiting to
        # change, so a further move is dated, not accused.
        if claimed_unchanged is True:
            data, reason = read_input(path)
            if data is None:
                out.append(f"RT28-RESIDUAL the re-measurement row for {path} "
                           f"declares the file UNCHANGED and it cannot be read "
                           f"({reason})")
            elif sha_bytes(data) != claimed_live:
                out.append(
                    f"RT28-RESIDUAL the re-measurement row for {path} declares "
                    f"UNCHANGED at {str(claimed_live)[:16]}... and the live bytes "
                    f"hash to {sha_bytes(data)[:16]}.... Section 7.3's 2026-08-05 "
                    f"rider: an inherited MEASUREMENT ages silently, because "
                    f"nothing in the delta mentions it and a reader sees only the "
                    f"successor's name against it")
    for name, measured in (("rowsReMeasured", len(rows)),
                           ("rowsUnchanged", unchanged),
                           ("rowsThatMoved", moved)):
        declared = disposition.get(name)
        if exact_int(declared) and declared != measured:
            out.append(f"RT28-RESIDUAL theInheritedRecordedInputsDigests.{name} "
                       f"declares {declared} and the rows measure {measured}")
    if disposition.get("rowsRewrittenByThisSuccessor") not in (0, None):
        out.append("RT28-RESIDUAL the artifact declares it rewrote an inherited "
                   "digest. Section 7.10 rule 1: re-pointing a pin from a "
                   "committed digest to an uncommitted one strictly destroys "
                   "recoverability while appearing to repair")
    ctx["reMeasuredRows"] = (len(rows), unchanged, moved)
    return out


# ===========================================================================
# SECTION 6 -- THE DERIVED SELF-MEASUREMENT SWEEP.
#
# Section 7.2.2 names THREE independent failure modes and a document can pass
# one while failing another.  All three bind this sweep:
#
#   SCOPING     enumerate by what the figure DESCRIBES, never by what it is
#               CALLED.  The v26 review's method was "every integer leaf whose
#               key ends in `count`", and the defective key was `recordedInputs`,
#               which ends in nothing.  Every referent here is resolved by
#               STRUCTURE -- which container is this figure a length OF -- and no
#               key name is matched.
#   ENUMERATION derive the row set and PUBLISH its population count.  A
#               hand-enumerated sweep is honest about every row it contains and
#               SILENT about every row it omits, and a defect landed in exactly
#               that silence twice in one week.  NOT ONE path is written into
#               this file; the generator is stated and the population is printed.
#   ENCODING    a numeric sweep cannot reach a figure written as a WORD.  A
#               derived census over 45 integer leaves scored PERFECTLY on a
#               document carrying two blocking defects spelled "eleven" and
#               "ONE"; measured, these documents carry roughly four times as many
#               word-numerals as integer leaves.  FAMILY W sweeps them.
# ===========================================================================

_TOKEN_RE = re.compile(r"(?<![\w.\-])(\d+)(?![\w.])")

WORD_NUMERALS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
}
_WORD_RE = re.compile(
    r"\b(" + "|".join(sorted(WORD_NUMERALS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE)

_SUFFIXES = ("positions", "position", "counts", "count", "length", "len",
             "total", "totals", "number", "rows", "members", "entries")


def _normalise_step(step) -> str:
    token = str(step).casefold()
    token = re.sub(r"[^a-z0-9]+", "", token)
    for suffix in _SUFFIXES:
        if token.endswith(suffix) and len(token) > len(suffix):
            token = token[: -len(suffix)]
            break
    if token.endswith("s") and len(token) > 1:
        token = token[:-1]
    return token


def _container_index(doc):
    """token -> set of admissible lengths.  Built from the document's own
    structure: every container's own final path step, plus the lengths of that
    container's container-valued members.  This is the REFERENT resolver and it
    reads no key name of the figure it will later judge."""
    index = {}
    def walk(node, step):
        if isinstance(node, (dict, list)):
            token = _normalise_step(step)
            if token:
                index.setdefault(token, set()).add(len(node))
                for member in (node.values() if isinstance(node, dict) else node):
                    if isinstance(member, (dict, list)):
                        index[token].add(len(member))
            items = (node.items() if isinstance(node, dict)
                     else enumerate(node))
            for key, value in items:
                walk(value, key)
    walk(doc, "$")
    return index


def _numeric_records(obj):
    """The members of `obj` that are PURE NUMERIC RECORDS: a non-empty container
    all of whose scalar leaves are non-bool ints.  This is the structural
    signature of a measurement record, located without naming it."""
    out = {}
    for key, value in obj.items():
        if not isinstance(value, (dict, list)) or not value:
            continue
        scalars = [v for _p, v in scalar_leaves(value)]
        if scalars and all(exact_int(v) for v in scalars):
            out[key] = scalars
    return out


_SWEEP_CACHE = {}


def derived_sweep(doc):
    """Returns (rows, findings, population).  Every row is GENERATED; the
    population is published so a reader can tell coverage from luck.

    Memoised on the CANONICAL DIGEST of the document swept -- the sweep is a
    pure function of the value, so a cache keyed on the value's own digest
    cannot change an answer, and the falsification sweep drives ~1800 runs of
    which almost none move the resolved value."""
    key = sha_bytes(canonical(doc))
    if key in _SWEEP_CACHE:
        return _SWEEP_CACHE[key]
    rows = []
    findings = []
    index = _container_index(doc)
    population = {"R-INT-REFERENT": 0, "P-PROSE-DECIMAL": 0, "W-PROSE-WORD": 0}
    verdicts = {"AGREES": 0, "DISAGREES": 0, "NO-REFERENT": 0,
                "WORD-AGREES": 0, "WORD-DISAGREES": 0, "WORD-NO-RECORD": 0,
                "PROSE-AGREES": 0, "PROSE-DISAGREES": 0}

    # --- FAMILY R: every non-bool int leaf, referent resolved by structure ---
    for path, value in scalar_leaves(doc):
        if not exact_int(value):
            continue
        population["R-INT-REFERENT"] += 1
        steps = path_steps(path) or []
        token = _normalise_step(steps[-1]) if steps else ""
        admissible = index.get(token)
        if not admissible:
            verdicts["NO-REFERENT"] += 1
            rows.append((path, "R", "NO-REFERENT"))
            continue
        if value in admissible:
            verdicts["AGREES"] += 1
            rows.append((path, "R", "AGREES"))
        else:
            verdicts["DISAGREES"] += 1
            rows.append((path, "R", "DISAGREES"))
            findings.append(
                f"RT28-SWEEP {path} declares {value} and the container its own "
                f"final path step names measures {sorted(admissible)}. Section "
                f"7.2.2 gives a recorded measurement a hard comparison; this is a "
                f"measurement about the document's own contents, which can never "
                f"legitimately advance")

    # --- FAMILY P and W: prose beside a numeric record ----------------------
    for path, obj in objects_of(doc):
        if not isinstance(obj, dict):
            continue
        records = _numeric_records(obj)
        if not records:
            continue
        live = set()
        for scalars in records.values():
            live.update(scalars)
        for key, value in obj.items():
            if not isinstance(value, str):
                continue
            decimals = {int(t) for t in _TOKEN_RE.findall(value)}
            words = {WORD_NUMERALS[m.group(1).casefold()]
                     for m in _WORD_RE.finditer(value)}
            if decimals:
                population["P-PROSE-DECIMAL"] += 1
                shared = decimals & live
                stale = decimals - live
                if shared and stale:
                    verdicts["PROSE-DISAGREES"] += 1
                    rows.append((f"{path}.{key}", "P", "DISAGREES"))
                    findings.append(
                        f"RT28-SWEEP {path}.{key} RESTATES the numeric record "
                        f"beside it -- it shares {sorted(shared)} with it -- and "
                        f"also asserts {sorted(stale)}, which that record does not "
                        f"hold ({sorted(live)}). A sentence that RESTATES a "
                        f"record's figures shares most of them and differs on the "
                        f"stale one")
                else:
                    verdicts["PROSE-AGREES"] += 1
                    rows.append((f"{path}.{key}", "P", "AGREES"))
            if words:
                population["W-PROSE-WORD"] += 1
                shared = words & live
                stale = words - live
                if shared and stale:
                    verdicts["WORD-DISAGREES"] += 1
                    rows.append((f"{path}.{key}", "W", "DISAGREES"))
                    findings.append(
                        f"RT28-SWEEP-WORD {path}.{key} spells a figure as a WORD. "
                        f"It shares {sorted(shared)} with the numeric record beside "
                        f"it and also asserts {sorted(stale)}, which that record "
                        f"does not hold ({sorted(live)}). Section 7.2.2's ENCODING "
                        f"mode: a derived census over integer leaves scores "
                        f"perfectly on a document whose blocking defects are "
                        f"spelled out in English")
                elif shared:
                    verdicts["WORD-AGREES"] += 1
                    rows.append((f"{path}.{key}", "W", "AGREES"))
                else:
                    verdicts["WORD-NO-RECORD"] += 1
                    rows.append((f"{path}.{key}", "W", "NO-RECORD"))
    population["TOTAL"] = sum(population[k] for k in
                              ("R-INT-REFERENT", "P-PROSE-DECIMAL", "W-PROSE-WORD"))
    result = (rows, findings, {"population": population, "verdicts": verdicts})
    _SWEEP_CACHE[key] = result
    return result


def word_numeral_density(doc):
    """The ENCODING bound, measured rather than asserted: how many word-numerals
    does this document carry against how many integer leaves?  Section 7.2.2
    measured roughly 4x on the versioning-policy lineage; publishing the ratio for
    THESE bytes is what stops an integer census being read as a numeric one."""
    ints = sum(1 for _p, v in scalar_leaves(doc) if exact_int(v))
    words = 0
    for _p, value in scalar_leaves(doc):
        if isinstance(value, str):
            words += len(_WORD_RE.findall(value))
    return {"intLeaves": ints, "wordNumeralOccurrences": words,
            "ratio": (round(words / ints, 2) if ints else None)}


def check_published_sweep(delta, ctx):
    """The artifact publishes its OWN derived sweep.  This instrument does not
    re-execute that generator -- it is a different generator and the two are not
    compared, which is stated at --limits -- but every INTERNAL claim the block
    makes is an arithmetic closure and every one gets a hard comparison.  A block
    whose numbers cannot disagree with each other is a block that can be
    fabricated wholesale."""
    out = []
    block = get_path(delta, "$.staleMeasurementSweep")
    if not isinstance(block, dict):
        out.append("RT28-PUBSWEEP the artifact publishes no self-measurement "
                   "sweep, so its central evidence for the second repair is absent")
        return out
    per_res = block.get("perFamilyCountsOverTheRESOLVEDvalue") or {}
    per_pred = block.get("perFamilyCountsOverTheVERIFIEDPREDECESSOR") or {}
    for label, table, total_key in (
            ("RESOLVED", per_res, "rowsGenerated"),
            ("PREDECESSOR", per_pred, "rowsGeneratedOverThePredecessor")):
        summed = sum(v for family in table.values()
                     if isinstance(family, dict)
                     for v in family.values() if exact_int(v))
        declared = block.get(total_key)
        if exact_int(declared) and summed != declared:
            out.append(f"RT28-PUBSWEEP the per-family verdict counts over the "
                       f"{label} sum to {summed} and {total_key} declares "
                       f"{declared}. A published row count that does not equal its "
                       f"own verdict table is a figure nothing produced")
    # The two row sets are declared IDENTICAL, and the artifact's own reason is
    # that no operation changes a leaf's type.  That is checkable.
    if block.get("rowSetIsIDENTICALacrossBothSubjects") is True:
        if block.get("rowsGenerated") != block.get("rowsGeneratedOverThePredecessor"):
            out.append("RT28-PUBSWEEP the sweep declares its row set identical "
                       "across both subjects and publishes two different row "
                       "counts")
    for name, listed in (("flaggedCountOverTheResolvedValue",
                          "flaggedOverTheRESOLVEDvalue"),
                         ("flaggedCountOverThePredecessor",
                          "flaggedOverTheVERIFIEDPREDECESSOR"),
                         ("clearedCount", "clearedByThisSuccessor"),
                         ("introducedCount", "introducedByThisSuccessor")):
        declared = block.get(name)
        array = block.get(listed)
        if exact_int(declared) and isinstance(array, list) and declared != len(array):
            out.append(f"RT28-PUBSWEEP {name} declares {declared} and {listed} "
                       f"holds {len(array)}")
    flagged_res = set(block.get("flaggedOverTheRESOLVEDvalue") or [])
    flagged_pred = set(block.get("flaggedOverTheVERIFIEDPREDECESSOR") or [])
    cleared = set(block.get("clearedByThisSuccessor") or [])
    introduced = set(block.get("introducedByThisSuccessor") or [])
    if cleared != flagged_pred - flagged_res:
        out.append(f"RT28-PUBSWEEP clearedByThisSuccessor is not the set difference "
                   f"of the two flag sets; symmetric difference "
                   f"{sorted(cleared ^ (flagged_pred - flagged_res))}")
    if introduced != flagged_res - flagged_pred:
        out.append(f"RT28-PUBSWEEP introducedByThisSuccessor is not the set "
                   f"difference of the two flag sets; symmetric difference "
                   f"{sorted(introduced ^ (flagged_res - flagged_pred))}")
    # Every flagged row must be adjudicated exactly once, and the published class
    # list must be the classes the adjudications actually carry.
    adj_block = block.get("everySurvivingFlagIsADJUDICATED") or {}
    adjudications = adj_block.get("adjudications") or []
    adj_paths = [a.get("path") for a in adjudications]
    if sorted(adj_paths) != sorted(flagged_res):
        out.append(f"RT28-PUBSWEEP the adjudicated paths and the flagged set "
                   f"differ; symmetric difference "
                   f"{sorted(set(adj_paths) ^ flagged_res)}")
    if len(set(adj_paths)) != len(adj_paths):
        out.append("RT28-PUBSWEEP a flagged path is adjudicated more than once")
    declared_classes = adj_block.get("classesFound")
    measured_classes = sorted({a.get("class") for a in adjudications
                               if isinstance(a.get("class"), str)})
    if isinstance(declared_classes, list) and sorted(declared_classes) != measured_classes:
        out.append(f"RT28-PUBSWEEP classesFound declares {sorted(declared_classes)} "
                   f"and the adjudications carry {measured_classes}")
    if exact_int(adj_block.get("count")) and adj_block["count"] != len(adjudications):
        out.append(f"RT28-PUBSWEEP the adjudication count declares "
                   f"{adj_block['count']} and the array holds {len(adjudications)}")
    if adj_block.get("unadjudicatedCount") not in (0, None) or \
            (adj_block.get("unadjudicated") or []):
        out.append("RT28-PUBSWEEP the sweep declares unadjudicated flags; every "
                   "surviving flag is claimed adjudicated")
    verdicts = {a.get("verdict") for a in adjudications}
    if adj_block.get("defectsAmongThem") == 0 and verdicts - {"NOT-A-DEFECT"}:
        out.append(f"RT28-PUBSWEEP the block declares 0 defects among the flagged "
                   f"rows and carries adjudication verdicts {sorted(v for v in verdicts if v)}")
    # And the negative control: the block claims the generator reproduces the
    # predecessor's known defects.  A control that catches nothing is a label.
    control = block.get("theNEGATIVECONTROL") or {}
    known = control.get("theThreeKnownDefects") or []
    caught = control.get("caughtByTheGenerator") or []
    for name, measured in (("caught", len(caught)), ("outOf", len(known))):
        declared = control.get(name)
        if exact_int(declared) and declared != measured:
            out.append(f"RT28-PUBSWEEP theNEGATIVECONTROL.{name} declares "
                       f"{declared} and the array it counts holds {measured}")
    if known and not caught:
        out.append("RT28-PUBSWEEP the published negative control names known "
                   "defects and reports the generator catching none of them, so "
                   "its 0 over the resolved value is vacuous")
    ctx["publishedSweep"] = {"rows": block.get("rowsGenerated"),
                             "flaggedResolved": len(flagged_res),
                             "flaggedPredecessor": len(flagged_pred),
                             "adjudicated": len(adjudications)}
    return out


def check_derived_sweep(delta, resolved, prov, ctx):
    """Run the derived sweep over BOTH subjects and gate the DELTA.

    WHAT IS A FINDING AND WHAT IS COVERAGE, stated because the difference is the
    whole discipline:

      FAMILY R (referent) DISAGREES is a FINDING.  A figure contradicted by the
      container its own final path step names is wrong about these bytes and can
      never legitimately advance.  Run against the verified predecessor it
      returns the artifact's headline defect; run against the resolved value it
      returns none.  Delete the repair and it comes back.

      FAMILY P and FAMILY W disagreements are COVERAGE, with two exceptions that
      ARE findings: a disagreement that resolving this derivation INTRODUCES, and
      a disagreement that lands ON AN OPERATION PATH.  The derivation owns what
      it touches and owns what it adds; it does not own what it inherited.
      This is deliberate and it is MEASURED rather than assumed: this generator
      is WIDER than the artifact's own -- it reaches
      $.newResiduals[6].statement, where "three of the four are arguments and one
      is a quotation" partitions a sibling 4 that the record does hold -- and a
      wider generator's extra rows are CANDIDATES, not defects.  Emitting them
      would be manufacturing the false accusation this instrument exists to make
      impossible.

    Every population count is published, per section 7.2.2's ENUMERATION mode:
    a lane that does not publish how many rows it generated is not making a
    weaker claim, it is making an uncheckable one.
    """
    out = []
    predecessor = prov["parsedPredecessor"]
    pred_rows, pred_findings, pred_stats = derived_sweep(predecessor)
    res_rows, res_findings, res_stats = derived_sweep(resolved)
    ctx["sweep"] = {
        "populationOverThePredecessor": pred_stats["population"],
        "populationOverTheResolvedValue": res_stats["population"],
        "verdictsOverThePredecessor": pred_stats["verdicts"],
        "verdictsOverTheResolvedValue": res_stats["verdicts"],
        "definitiveOverThePredecessor": pred_stats["verdicts"]["DISAGREES"],
        "definitiveOverTheResolvedValue": res_stats["verdicts"]["DISAGREES"],
        "wordDensityResolved": word_numeral_density(resolved),
        "wordDensityDelta": word_numeral_density(delta),
    }

    # --- the definitive family -------------------------------------------
    out.extend(f for f in res_findings if f.startswith("RT28-SWEEP ")
               and "declares" in f and "the container its own final path step" in f)

    # --- the negative control --------------------------------------------
    if pred_stats["verdicts"]["DISAGREES"] < 1:
        out.append(
            "RT28-SWEEP the derived referent rule returns NOTHING definitive "
            "against the verified predecessor. The artifact exists to repair "
            "defects of exactly that class; a rule that cannot reproduce them on "
            "the document that had them is not a control, and its 0 against the "
            "resolved value is VACUOUS")
    definitive_pred = [f for f in pred_findings
                       if "the container its own final path step" in f]
    if len(definitive_pred) != RECORDED["sweepDefinitiveOverThePredecessor"]:
        out.append(
            f"RT28-SWEEP the derived referent rule returns {len(definitive_pred)} "
            f"definitive row(s) against the verified predecessor and this "
            f"instrument recorded "
            f"{RECORDED['sweepDefinitiveOverThePredecessor']} -- the value half of "
            f"the artifact's headline repair. A control whose yield moves is a "
            f"control whose meaning moved")
    if res_stats["verdicts"]["DISAGREES"] != RECORDED["sweepDefinitiveOverTheResolvedValue"]:
        out.append(
            f"RT28-SWEEP the derived referent rule returns "
            f"{res_stats['verdicts']['DISAGREES']} definitive row(s) against the "
            f"RESOLVED value and this instrument recorded "
            f"{RECORDED['sweepDefinitiveOverTheResolvedValue']}")
    # THE POPULATION IS A RECORDED MEASUREMENT AND IS HARD-COMPARED, in both
    # directions and per family.  Section 7.2.2's ENUMERATION mode asks a lane to
    # publish how many rows it generated; publishing a number nothing compares
    # would answer the letter of that and none of its point.
    for label, stats in (("the RESOLVED value", res_stats),
                         ("the VERIFIED PREDECESSOR", pred_stats)):
        total_key = ("sweepRowsOverTheResolvedValue"
                     if "RESOLVED" in label else "sweepRowsOverThePredecessor")
        if stats["population"]["TOTAL"] != RECORDED[total_key]:
            out.append(f"RT28-SWEEP the derived generator produces "
                       f"{stats['population']['TOTAL']} row(s) over {label} and "
                       f"this instrument recorded {RECORDED[total_key]}")
    for family, key in (("R-INT-REFERENT", "sweepReferentRows"),
                        ("P-PROSE-DECIMAL", "sweepDecimalProseRows"),
                        ("W-PROSE-WORD", "sweepWordNumeralRows")):
        if res_stats["population"][family] != RECORDED[key]:
            out.append(f"RT28-SWEEP family {family} generates "
                       f"{res_stats['population'][family]} row(s) over the "
                       f"resolved value and this instrument recorded "
                       f"{RECORDED[key]}")
    if res_stats["population"]["W-PROSE-WORD"] == 0:
        out.append(
            "RT28-SWEEP the WORD-NUMERAL family generated ZERO rows, so section "
            "7.2.2's ENCODING mode is unexercised and this sweep is an integer "
            "census wearing a numeric census's name")

    # --- the prose and word families, delta-scoped ------------------------
    op_paths = {("$." + str(op.get("path"))) for op in (ctx.get("operations") or [])}
    pred_flags = {row[0] for row in pred_rows if row[2] == "DISAGREES"}
    res_flags = {row[0] for row in res_rows if row[2] == "DISAGREES"}
    introduced = sorted(res_flags - pred_flags)
    cleared = sorted(pred_flags - res_flags)
    on_operation = sorted(p for p in res_flags
                          if p in op_paths or any(p.startswith(o + ".")
                                                  for o in op_paths))
    ctx["sweep"]["introduced"] = introduced
    ctx["sweep"]["cleared"] = cleared
    ctx["sweep"]["onOperationPaths"] = on_operation
    # Published so the REPAIR gate in section 7 can ask a union of oracles rather
    # than assuming the executed battery is the only one.
    ctx["sweep"]["predecessorFlaggedPaths"] = sorted(
        pred_flags | {f.split(" ")[1] for f in pred_findings
                      if f.startswith("RT28-SWEEP ") and len(f.split(" ")) > 1})
    for path in introduced:
        out.append(
            f"RT28-SWEEP resolving this derivation INTRODUCES a restatement "
            f"disagreement at {path} that the verified predecessor does not "
            f"carry. A derivation owns what it adds")
    for path in on_operation:
        out.append(
            f"RT28-SWEEP {path} is a restatement disagreement AT A PATH THIS "
            f"DERIVATION TOUCHES. A derivation owns what it writes, whether or "
            f"not the predecessor was wrong there first")

    # --- coverage, published, and cross-checked against the adjudication ---
    published = get_path(delta, "$.staleMeasurementSweep."
                                "everySurvivingFlagIsADJUDICATED.adjudications") or []
    adjudicated = {a.get("path") for a in published}
    unadjudicated = sorted(p for p in res_flags - set(on_operation)
                           if p not in adjudicated)
    ctx["sweep"]["unadjudicatedCandidates"] = unadjudicated
    ctx["sweep"]["adjudicatedByTheArtifact"] = len(adjudicated)
    return out


# ===========================================================================
# SECTION 7 -- THE EXECUTED CLOSURE.
#
# Section 7.3: a retained checker that hash-verifies a set of files before
# executing them may internally execute superseded predecessors.  Those files are
# RUNTIME INPUTS of the instrument.  They do not become normative, they do not
# become a fallback contract, and their presence does not weaken this verdict.
# ===========================================================================

FAMILY_RE = re.compile(r"^(RT26-[A-Z0-9\-]+)")


def families(findings):
    out = {}
    for finding in findings:
        match = FAMILY_RE.match(finding)
        out.setdefault(match.group(1) if match else "<<UNNAMED>>", []).append(
            finding)
    return out


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


_BATTERY_CACHE = {}


def run_battery(mod, doc, part):
    """(reference context, notices, findings), memoised on the CANONICAL DIGEST of
    the document driven.  The battery is deterministic over a quiescent tree and
    a value, so a cache keyed on the value's own digest cannot change an answer;
    it exists so the falsification sweep can drive 1799 leaf mutations, almost
    none of which move the resolved value, without re-running a 5000-line
    reference derivation 1799 times."""
    key = (sha_bytes(canonical(doc)), part)
    if key not in _BATTERY_CACHE:
        ref_ctx, notices = build_reference_context(mod, doc)
        findings = mod.run_all(doc, ref_ctx, part)
        _BATTERY_CACHE[key] = (ref_ctx, notices, findings)
    return _BATTERY_CACHE[key]


def reference_inputs_readable(mod):
    """BLOCKER 1 again, one level down.  The executed reference derivation reads
    its own pinned closure with bare read_bytes(), so a chmod 000 anywhere in it
    would surface here as a DRIVER finding about the subject.  Every one of its
    declared inputs is checked for readability and for its floor BEFORE it is
    executed, so an unreadable member of ITS closure is a named exit-2 refusal
    rather than a finding about this artifact."""
    problems = []
    for name in list(getattr(mod, "GATED_PINS", {})) + \
            list(getattr(mod, "ADVANCING_PINS", {})):
        data, reason = read_input(name)
        if data is None:
            problems.append(f"{name}: {reason}")
            continue
        ok, failures = apply_floor(name, data)
        if not ok:
            problems.append(f"{name}: below its FLOOR -- {'; '.join(failures)}")
    return problems


def check_executed_closure(delta, resolved, mod, ctx):
    """Run the reference battery TWICE -- over the verified predecessor and over
    the RESOLVED value -- and gate the DELTA.

    BLOCKER 2(b) AND BLOCKER 3 BOTH LIVE HERE.

    The expected delta is DERIVED from the artifact's own bytes.  The artifact is
    a FORM repair that carries the predecessor lane's substantive delta unchanged,
    so what must stop firing is read out of the operation list's REPAIR class --
    not out of a prose block, and not out of a hardcoded family name.  A family
    that still fires is only a regression if it fires AT A PATH AN OPERATION
    TOUCHES; a family that fires at an untouched path and ALSO fires against the
    verified predecessor is INHERITED, and calling it a regression is the false
    accusation an empty IMPLEMENTATION-FREEZE.md produced against the predecessor
    instrument.

    And every expectation is scoped to the families the battery ACTUALLY RAN
    under this --part, observed against the predecessor rather than listed.
    """
    out = []
    part = ctx.get("part", "all")
    ref_ctx_pred, notices, pred_findings = run_battery(mod, ctx["predecessor"], part)
    ref_ctx_res, _n, res_findings = run_battery(mod, resolved, part)
    ctx["referenceNotices"] = notices
    ctx["referenceContext"] = ref_ctx_res
    ctx["predecessorFindings"] = pred_findings
    ctx["resolvedFindings"] = res_findings

    pred_fam = families(pred_findings)
    res_fam = families(res_findings)
    ctx["predecessorFamilies"] = {k: len(v) for k, v in pred_fam.items()}
    ctx["resolvedFamilies"] = {k: len(v) for k, v in res_fam.items()}
    # BLOCKER 3: the in-scope family set, DERIVED by observation under this part.
    in_scope = set(pred_fam)
    ctx["familiesInScopeUnderThisPart"] = sorted(in_scope)
    scoped_out = []

    # --- what must STOP firing, derived from the REPAIR operations ---------
    operations = ctx["operations"]
    repair_paths = ["$." + str(op.get("path")) for op in operations
                    if op.get("class") == "REPAIR"]
    ctx["repairPaths"] = repair_paths
    if not repair_paths:
        out.append("RT28-DELTA the operation list classifies no REPAIR operation, "
                   "so nothing states what this successor is supposed to have "
                   "repaired and the repair cannot be gated")
    # THE ORACLE SET IS A UNION, and that is a correction rather than a
    # convenience.  A first draft of this gate asked only whether the executed
    # reference battery fires at each repaired path, and it produced a FINDING
    # against the third repair -- which is FALSE, and the artifact says so in the
    # operation's own `why`: that defect was "FOUND BY THIS ARTIFACT'S SWEEP,
    # reported by neither the independent review nor the retained checker."  A
    # gate that assumes one oracle is the only oracle manufactures exactly the
    # accusation this instrument exists to prevent.  So the requirement is that
    # SOME oracle this run executes reproduces a defect at each repaired path --
    # the battery, or this instrument's own derived sweep -- and the oracle that
    # saw it is named.  A fabricated repair at a path no oracle flags still fails.
    sweep_flags = set((ctx.get("sweep") or {}).get("predecessorFlaggedPaths") or [])
    repaired_before = []
    for path in repair_paths:
        hits = [f for f in pred_findings if path in f]
        by_sweep = [p for p in sweep_flags if p == path or p.startswith(path + ".")]
        repaired_before.extend(hits)
        if not hits and not by_sweep:
            out.append(
                f"RT28-DELTA the derivation declares a REPAIR at {path} and NO "
                f"oracle this run executes reproduces a defect there -- neither the "
                f"predecessor's own retained battery nor this file's derived "
                f"referent sweep. A repair with no reproduced defect behind it is a "
                f"claim, not a repair")
        still = [f for f in res_findings if path in f]
        if still:
            out.append(
                f"RT28-DELTA a finding still fires AT THE REPAIRED PATH {path} "
                f"against the RESOLVED value. The derivation exists to repair it: "
                f"{still[0][:220]}")
    ctx["repairedBefore"] = repaired_before
    ctx["repairOracles"] = {
        path: ("battery" if [f for f in pred_findings if path in f] else "")
              + ("+sweep" if [p for p in sweep_flags
                              if p == path or p.startswith(path + ".")] else "")
        for path in repair_paths}

    # --- what must KEEP firing, scoped to families the battery ran ---------
    keep = {}
    for entry in (get_path(delta, "$.residualsLeftOpen.fromTheV26IndependentReview")
                  or []) + (get_path(delta, "$.residualsLeftOpen.fromRetentionTiersV27")
                            or []):
        text = json.dumps(entry, ensure_ascii=False)
        for family in set(re.findall(r"RT26-[A-Z0-9\-]+", text)):
            keep[family] = keep.get(family, 0) + 1
    # THE UNIVERSE OF FAMILIES, derived rather than assumed.  An id like
    # IR-RT26-N01-... is a RESIDUAL IDENTIFIER, not a finding family the battery
    # emits, and comparing it against zero is the same class of false finding
    # BLOCKER 3 names.  So the candidate set is intersected with the families the
    # battery actually produces at --part all, measured once and cached; what is
    # left over is counted and reported as a coverage figure, never as a gate.
    universe = set(families(run_battery(mod, ctx["predecessor"], "all")[2]))
    not_families = sorted(f for f in keep if f not in universe)
    ctx["claimedTokensThatAreNotBatteryFamilies"] = not_families
    keep = {f: n for f, n in keep.items() if f in universe}
    ctx["familiesClaimedStillOpen"] = sorted(keep)
    for family in sorted(keep):
        if family not in in_scope:
            scoped_out.append(
                f"RT28-PART-SCOPED family {family} is declared OPEN by the "
                f"artifact and the reference battery does not produce it under "
                f"--part {part}, so THIS EXPECTATION DID NOT RUN. It is named "
                f"rather than compared against zero, which is what made the "
                f"predecessor emit false findings at --part a, c and d")
            continue
        if not res_fam.get(family):
            out.append(
                f"RT28-DELTA the artifact declares residual {family} OPEN and it "
                f"fires 0 time(s) against the RESOLVED value while firing "
                f"{len(pred_fam.get(family, []))} against the verified "
                f"predecessor. A residual left open by NAMING it is only left open "
                f"if the naming is true")

    # --- nothing else may move, and every move must be DERIVABLE ----------
    identity_targets = {}
    for op in operations:
        if op.get("class") != "IDENTITY":
            continue
        steps = path_steps(str(op.get("path"))) or []
        if len(steps) == 1:
            identity_targets[f"$.{steps[0]}"] = op.get("value")
    added = sorted(set(res_findings) - set(pred_findings))
    removed = sorted(set(pred_findings) - set(res_findings))
    unexplained_added = []
    explained_added = []
    for finding in added:
        hit = None
        for path, value in identity_targets.items():
            if path in finding and repr(value) in finding:
                hit = path
        if hit is None:
            for path in ["$." + str(op.get("path")) for op in operations]:
                if path in finding:
                    hit = path
        if hit is not None:
            explained_added.append((finding, hit))
        else:
            unexplained_added.append(finding)
    ctx["closureAdded"] = added
    ctx["closureRemoved"] = removed
    ctx["closureExplainedAdded"] = explained_added
    if unexplained_added:
        out.append(
            f"RT28-DELTA resolving this derivation introduces "
            f"{len(unexplained_added)} finding(s) that no operation path explains, "
            f"against the predecessor's own retained battery: "
            f"{[f[:200] for f in unexplained_added]}")
    for finding in removed:
        if not any(path in finding for path in
                   ["$." + str(op.get("path")) for op in operations]):
            out.append(
                f"RT28-DELTA resolving this derivation silently REMOVES a finding "
                f"at a path no operation touches: {finding[:220]}")

    # --- coverage, asserted only where the battery reports having run ------
    vec = ref_ctx_res.get("vectorReport") or {}
    inv = ref_ctx_res.get("invariantReport") or {}
    ctx["vectorReport"] = vec
    ctx["invariantReport"] = inv
    declared_vectors = len(
        get_path(resolved, "$.partC_retentionBounds.vectors.rows") or [])
    declared_invariants = len(
        get_path(resolved, "$.partC_retentionBounds.invariants") or [])
    if declared_vectors != RECORDED["vectorsDeclared"]:
        out.append(f"RT28-CLOSURE the resolved document declares {declared_vectors} "
                   f"vectors, not the recorded {RECORDED['vectorsDeclared']}")
    if declared_invariants != RECORDED["invariantsDeclared"]:
        out.append(f"RT28-CLOSURE the resolved document declares "
                   f"{declared_invariants} invariants, not the recorded "
                   f"{RECORDED['invariantsDeclared']}")
    if vec.get("declared") is None or inv.get("declared") is None:
        scoped_out.append(
            f"RT28-PART-SCOPED the reference battery did not run the vector and "
            f"invariant suites under --part {part}, so the coverage gate DID NOT "
            f"RUN. It is named rather than compared against a missing report, "
            f"which is what made the predecessor print 'None of None' as a finding")
    else:
        if vec.get("declared") != declared_vectors or vec.get("executed") != declared_vectors:
            out.append(f"RT28-CLOSURE {vec.get('executed')} of "
                       f"{vec.get('declared')} vectors executed against the "
                       f"resolved value; the resolved document declares "
                       f"{declared_vectors} rows and every one must be exercised")
        if inv.get("declared") != declared_invariants or inv.get("executed") != declared_invariants:
            out.append(f"RT28-CLOSURE {inv.get('executed')} of "
                       f"{inv.get('declared')} invariants executed against the "
                       f"resolved value; the resolved document declares "
                       f"{declared_invariants}")
        vacuous = vec.get("controlsVacuous") or []
        if vacuous:
            out.append(f"RT28-CLOSURE {len(vacuous)} negative control(s) are "
                       f"VACUOUS -- the rejected reading the row names produces the "
                       f"same answer as the accepted one, so the control proves "
                       f"nothing: {vacuous}")
        if (vec.get("controlsRun") or 0) < 1:
            out.append("RT28-CLOSURE no rejected reading was executed, so every "
                       "negative control is a label rather than a measurement")

    b1 = ref_ctx_res.get("b1") or {}
    ctx["b1"] = b1
    if not b1:
        scoped_out.append(f"RT28-PART-SCOPED the reference battery produced no B1 "
                          f"measurement under --part {part}; the Cap algebra gate "
                          f"DID NOT RUN")
    else:
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
                out.append(f"RT28-CLOSURE B1 {label}: measured {measured!r}, "
                           f"recorded {expected!r}")
        if len(b1.get("publishedAgree") or []) != (b1.get("arithmeticRows") or -1):
            out.append("RT28-CLOSURE B1: the published demand expressions do not "
                       "reproduce every arithmetic vector of the resolved "
                       "document, which is the whole of the IR-RT25-B1 repair")
        if len(b1.get("v25Agree") or []) >= (b1.get("arithmeticRows") or 0):
            out.append("RT28-CLOSURE B1: the PREDECESSOR's rejected expressions "
                       "reproduce as many rows as the published ones, so the "
                       "control separates nothing and the repair is unmeasured")

    # Quotation discipline over the RESOLVED value, with folding applied first.
    verbatim_ran = ref_ctx_res.get("verbatimStringKeys") is not None
    if not verbatim_ran:
        scoped_out.append(f"RT28-PART-SCOPED the quotation census did not run under "
                          f"--part {part}")
    else:
        for label, key, expected in (
                ("string-valued *Verbatim keys", "verbatimStringKeys",
                 RECORDED["verbatimStringKeys"]),
                ("verified against their attributed source", "verbatimVerified",
                 RECORDED["verbatimStringKeys"]),
                ("source-attributed fields", "verbatimSourceAttributed",
                 RECORDED["verbatimSourceAttributed"])):
            measured = ref_ctx_res.get(key)
            if measured != expected:
                out.append(f"RT28-CLOSURE quotations: {label} measured "
                           f"{measured!r}, recorded {expected!r}")
        if ref_ctx_res.get("verbatimNotFound"):
            out.append(f"RT28-CLOSURE quotations: "
                       f"{ref_ctx_res.get('verbatimNotFound')} verbatim field(s) "
                       f"do not resolve against the source their own NAME "
                       f"attributes them to")
        false_absent = ref_ctx_res.get("verbatimFalseAbsent")
        if false_absent != RECORDED["verbatimFalseAbsentUnderARawSearch"]:
            out.append(
                f"RT28-CLOSURE quotations: {false_absent!r} of the "
                f"source-attributed verbatim fields would read FALSE-ABSENT under "
                f"a raw byte-literal search, recorded "
                f"{RECORDED['verbatimFalseAbsentUnderARawSearch']}. Section 7.7's "
                f"folding is claimed load-bearing; at 0 it is not, and the claim "
                f"is no longer supported by these bytes")
        ctx["verbatim"] = {k: ref_ctx_res.get(k) for k in
                           ("verbatimStringKeys", "verbatimVerified",
                            "verbatimSourceAttributed", "verbatimFalseAbsent",
                            "verbatimFalseAbsentNormalised")}

    ctx["anchors"] = (ref_ctx_res.get("anchorsPresent"),
                      ref_ctx_res.get("anchorsTotal"))
    ctx["cdRt5"] = (ref_ctx_res.get("cdRt5Status"),
                    ref_ctx_res.get("cdRt5Quoted"))
    ctx.setdefault("partScoped", []).extend(scoped_out)
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
            out.append(f"RT28-SWEEP-TYPE {arm}: {sweep[arm]['admitted']} "
                       f"position(s) admitted a respelled scalar: "
                       f"{sweep[arm]['escapes'][:5]}")
    if counts["unruledIntOrBoolLeafPositions"]:
        out.append(f"RT28-SWEEP-TYPE {counts['unruledIntOrBoolLeafPositions']} "
                   f"int/bool leaf position(s) are outside the frozen type "
                   f"registry, so the sweep does not cover them")
    if sweep["respellingsAttempted"] != RECORDED["typeSweepRespellings"]:
        out.append(f"RT28-SWEEP-TYPE {sweep['respellingsAttempted']} respellings "
                   f"attempted, not the recorded "
                   f"{RECORDED['typeSweepRespellings']}")
    if sweep["respellingsAdmitted"] != RECORDED["typeSweepAdmitted"]:
        out.append(f"RT28-SWEEP-TYPE {sweep['respellingsAdmitted']} respellings "
                   f"admitted, not the recorded {RECORDED['typeSweepAdmitted']}")
    if sweep["respellingsAttempted"] == 0:
        out.append("RT28-SWEEP-TYPE the type sweep attempted nothing, so a "
                   "0-admitted result is vacuous")
    return out


# ===========================================================================
# SECTION 8 -- THE SECOND, INDEPENDENT IMPLEMENTATION.
#
# Section 7.8: *an instrument must re-derive its constants from the artifact it
# checks, or it is testing its own transcription.*  Executing the reference
# battery is not transcription, but a single implementation reporting itself is
# not agreement either.  What follows is a second implementation of the
# load-bearing algebra, written here from the RESOLVED document's own published
# rule text, and compared row-by-row against the executed module's answers.
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
    At UNBOUNDED, k = 0 satisfies it by the ORDER ALONE."""
    for k in range(0, len(order) + 1):
        if le_cap(sum(m["bytes"] for m in order[k:]), cap):
            return k
    return len(order)


def x_demand_time(cap, order, now: int) -> int:
    """the number of leading members of the eviction order whose admission time is
    strictly older than cutoff := now - cap_age.  At UNBOUNDED the cutoff is
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


def x_eviction(bounds, evictable, now: int):
    order = sorted(evictable, key=lambda m: (m["admittedAt"], m["id"]))
    demands = {
        "time": x_demand_time(lift(bounds["maxAgeSeconds"]), order, now),
        "size": x_demand_size(lift(bounds["maxTotalBytes"]), order),
        "count": x_demand_count(lift(bounds["keepCount"]), order),
    }
    return max(demands.values()) if demands else 0, demands, order


def cross_check_b1(resolved, mod, ref_ctx, ctx):
    """Re-execute the arithmetic vector rows under THIS file's implementation and
    require it to agree with the executed reference, row by row.  A second
    implementation with a ZERO DENOMINATOR is not corroboration, so the row count
    is gated too."""
    out = []
    rows = get_path(resolved, "$.partC_retentionBounds.vectors.rows") or []
    per_row = (ctx.get("b1") or {}).get("perRow") or {}
    if not per_row:
        ctx.setdefault("partScoped", []).append(
            "RT28-PART-SCOPED the reference battery published no per-row B1 "
            "answers under this --part, so the second implementation has nothing "
            "to agree with and the cross-check DID NOT RUN")
        return out
    agreed = disagreed = 0
    for row in rows:
        rid = row.get("id")
        if rid not in per_row:
            continue
        bounds = (row.get("bounds") or {})
        size = row.get("evictableCount")
        if not exact_int(size) or size < 0:
            continue
        total = row.get("evictableTotalBytes")
        if total is not None and (not exact_int(total) or total < 0):
            continue
        each = ((total // size) if total is not None and size else 100)
        members = [{"id": f"m{i}", "bytes": each, "admittedAt": mod.NOW - 1000}
                   for i in range(size)]
        if not all(exact_int(bounds.get(k)) for k in
                   ("maxAgeSeconds", "maxTotalBytes", "keepCount")):
            continue
        mine, demands, _order = x_eviction(bounds, members, mod.NOW)
        theirs = per_row[rid].get("underV26")
        if theirs is None:
            continue
        if mine == theirs:
            agreed += 1
        else:
            disagreed += 1
            out.append(
                f"RT28-XCHECK {rid}: this file's independent implementation of the "
                f"published demand expressions evicts {mine} (demands {demands}) "
                f"and the executed reference derivation evicts {theirs}. Two "
                f"implementations of one published rule disagree, so at most one "
                f"of them implements it")
    ctx["xcheckB1"] = {"agreed": agreed, "disagreed": disagreed}
    if agreed + disagreed != RECORDED["arithmeticRows"]:
        out.append(
            f"RT28-XCHECK the second implementation reached "
            f"{agreed + disagreed} arithmetic row(s), recorded "
            f"{RECORDED['arithmeticRows']}. A cross-check that silently skips its "
            f"rows reports 'agrees on 0 rows' and looks like corroboration")
    non_zero = 0
    for size in range(0, 201):
        members = [{"id": f"m{i}", "bytes": 1, "admittedAt": i}
                   for i in range(size)]
        evicted, _d, _o = x_eviction(
            {"maxAgeSeconds": 0, "maxTotalBytes": 0, "keepCount": 0},
            members, mod.NOW)
        if evicted:
            non_zero += 1
    ctx["xcheckDefaultNonZero"] = non_zero
    if non_zero != RECORDED["defaultConfigEvictionsUnderThePublishedExpressions"]:
        out.append(
            f"RT28-XCHECK the default 0/0/0 configuration evicts something at "
            f"{non_zero} of 201 evictable-set sizes under this file's own "
            f"implementation of the published lift. 0/0/0 is the configuration of "
            f"every project nobody has configured, so a non-zero here purges every "
            f"unconfigured project")
    return out


def cross_check_demotion(resolved, mod, ref_ctx, ctx):
    """FREEZE LAW 14, re-implemented.  *A durability failure cannot report
    authoritative success.*  NO REACHABLE SILENT DEMOTION is the property this
    lineage exists to protect, so it is measured here from the pinned v24 cells
    with the RESOLVED document's own published after-rows substituted -- the
    resolved TABLE, never the artifact's description of it."""
    out = []
    if "v24" not in ref_ctx:
        ctx.setdefault("partScoped", []).append(
            "RT28-PART-SCOPED the pinned v24 table was not available to the "
            "reference context, so the law-14 cross-check DID NOT RUN")
        return out
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
        out.append(f"RT28-XCHECK the resolved table has {len(durable)} "
                   f"DURABLE_AUTHORITATIVE cells, not the recorded "
                   f"{RECORDED['durableAuthoritativeCells']}")
    if len(outcomes) != RECORDED["interactionOutcomes"]:
        out.append(f"RT28-XCHECK the resolved table has {len(outcomes)} interaction "
                   f"outcomes, not the recorded "
                   f"{RECORDED['interactionOutcomes']}")
    violations = 0
    for cell in durable:
        axis = f"{cell.get('invocationProfile')}/{cell.get('policyPresence')}"
        outcome = cell.get("outcome")
        write = cell.get("durableSourceDerivedWritePermitted")
        if outcome == "PROCEED-DURABLE" and write is not True:
            violations += 1
            out.append(f"RT28-XCHECK SILENT DEMOTION IS REACHABLE at {axis}: "
                       f"outcome PROCEED-DURABLE with "
                       f"durableSourceDerivedWritePermitted {write!r}")
        if outcome == "PROCEED-EPHEMERAL":
            violations += 1
            out.append(f"RT28-XCHECK a DURABLE_AUTHORITATIVE request at {axis} "
                       f"resolves to PROCEED-EPHEMERAL, which is the demotion "
                       f"itself")
        if outcome == "REFUSE" and write is True:
            violations += 1
            out.append(f"RT28-XCHECK the row at {axis} both REFUSES and permits a "
                       f"durable write")
    ctx["xcheckDemotionViolations"] = violations
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
        out.append(f"RT28-XCHECK the pinned v24 population is {len(rows)} rows, not "
                   f"the {RECORDED['d9BiconditionalRows']} the (d9Axes is null) "
                   f"<-> (NOT-A-TERMINATION) biconditional was measured over")
    if deviations:
        out.append(f"RT28-XCHECK the d9Axes biconditional deviates on {deviations} "
                   f"of {len(rows)} rows under this file's own implementation")
    # RT26-A-INV-18 and -19 ARE THE TWO INVARIANTS THAT CARRY FREEZE LAW 14, and
    # they get a gate that can actually fail.  A first draft read a `violations`
    # member off each row and required it to be 0 -- those rows carry no such
    # member, so the gate was VACUOUS: it could never fire, which is precisely
    # the paper seal section 7.2.2 grades.  What is checkable, and is checked:
    # the two ids are PRESENT in the resolved document, the executed reference
    # DRIVES both by name (so they are exercised rather than counted), and NO
    # finding from the battery names either of them.
    ids = {str(i.get("id")) for i in
           (get_path(resolved, "$.partC_retentionBounds.invariants") or [])
           if isinstance(i, dict)}
    driven = set(getattr(mod, "INVARIANT_IDS", ()) or ())
    law14 = sorted(i for i in ids if i.endswith(("-INV-18", "-INV-19")))
    ctx["law14Invariants"] = law14
    if len(law14) != 2:
        out.append(f"RT28-XCHECK the resolved document carries {len(law14)} of the "
                   f"two invariants that carry freeze law 14 ({law14}). Law 14 is "
                   f"the property this lineage exists to protect")
    for ident in law14:
        if ident not in driven:
            out.append(f"RT28-XCHECK {ident} is declared and the executed "
                       f"reference derivation does not DRIVE it, so it is counted "
                       f"as coverage and exercised by nothing")
    hits = [f for f in (ctx.get("resolvedFindings") or [])
            if any(i in f for i in law14)]
    if hits:
        out.append(f"RT28-XCHECK {len(hits)} finding(s) name a law-14 invariant "
                   f"against the RESOLVED value: {hits[0][:200]}")
    return out


def cross_check_partition(resolved, ctx):
    """The 35-key exhaustive partition of v24, re-derived rather than read."""
    out = []
    part_a = get_path(resolved, "$.inheritance.exhaustivePartitionOfV24.partA") or []
    part_b = get_path(resolved, "$.inheritance.exhaustivePartitionOfV24.partB") or []
    total = len(part_a) + len(part_b)
    ctx["partition"] = {"partA": len(part_a), "partB": len(part_b), "total": total}
    if total != RECORDED["partitionKeyCount"]:
        out.append(f"RT28-XCHECK the exhaustive partition of v24 holds {total} "
                   f"keys, not the recorded {RECORDED['partitionKeyCount']}")
    for name, rows in (("partA", part_a), ("partB", part_b)):
        bad = [r.get("key") for r in rows
               if r.get("disposition") not in ("CHANGED", "UNCHANGED")]
        if bad:
            out.append(f"RT28-XCHECK {name} carries {len(bad)} row(s) with no "
                       f"CHANGED/UNCHANGED disposition, so the partition is not "
                       f"one: {bad[:6]}")
    keys = [r.get("key") for r in part_a + part_b]
    duplicates = sorted({k for k in keys if keys.count(k) > 1})
    if duplicates:
        out.append(f"RT28-XCHECK the partition repeats {len(duplicates)} key(s) "
                   f"across its two halves, so it is a cover and not a partition: "
                   f"{duplicates}")
    # The Part B UNCHANGED count is the referent of the artifact's SECOND repair,
    # re-derived here from the partition rather than read from the operation.
    unchanged = sum(1 for r in part_b if r.get("disposition") == "UNCHANGED")
    changed = sum(1 for r in part_b if r.get("disposition") == "CHANGED")
    ctx["partition"]["partBUnchanged"] = unchanged
    ctx["partition"]["partBChanged"] = changed
    boundary = get_path(resolved, "$.corpusResiduals[2].measuredBoundary")
    if isinstance(boundary, str):
        tokens = {int(t) for t in _TOKEN_RE.findall(boundary)}
        if unchanged not in tokens:
            out.append(
                f"RT28-XCHECK the Part B partition holds {unchanged} UNCHANGED "
                f"surfaces and the boundary sentence this derivation repaired "
                f"restates {sorted(tokens)}. The repair's whole content is that "
                f"the prose must state the figure its own sibling partition "
                f"measures")
    return out


def cross_check_folding(ctx):
    """Section 7.7, re-measured here rather than taken from the reference: fold
    markdown structure, not just whitespace, before concluding any quotation is
    absent.  The freeze states its standing rules inside blockquotes, so
    whitespace normalisation ALONE still returns ABSENT on them."""
    out = []
    text = ctx.get("freezeText")
    if text is None:
        ctx.setdefault("partScoped", []).append(
            "RT28-PART-SCOPED the freeze text was not available, so the folding "
            "cross-check DID NOT RUN")
        return out
    raw = ws = folded_hits = 0
    for anchor in FREEZE_ANCHORS:
        if anchor in text:
            raw += 1
        if whitespace_only(anchor) in whitespace_only(text):
            ws += 1
        if fold(anchor) in fold(text):
            folded_hits += 1
    ctx["anchorFolding"] = {"raw": raw, "whitespace": ws, "folded": folded_hits,
                            "total": len(FREEZE_ANCHORS)}
    missing = [a[:60] for a in FREEZE_ANCHORS if fold(a) not in fold(text)]
    if missing:
        out.append(
            f"RT28-ANCHOR {len(missing)} of {len(FREEZE_ANCHORS)} content anchors "
            f"are ABSENT from the live IMPLEMENTATION-FREEZE.md even under section "
            f"7.7 folding: {missing}. These anchor the sections this instrument "
            f"implements; their removal is a change to the rules it enforces and "
            f"must not pass silently. NOTE: this is a finding about the FREEZE, "
            f"not about {SUBJECT}")
    if folded_hits <= raw:
        out.append(
            f"RT28-ANCHOR folding recovers no anchor a raw byte-literal search "
            f"misses ({raw} raw, {folded_hits} folded). Section 7.7 calls this the "
            f"sharpest false-negative generator in the package; at parity the "
            f"discipline is untested by these anchors rather than vindicated by "
            f"them")
    return out


# ===========================================================================
# SECTION 9 -- ASSEMBLY.
#
# Every stage declares its SCOPE.  BLOCKER 3: `--part` narrows the artifact's
# PROPERTY batteries and the gates that read them; the derivation-integrity gates
# always run, because a derivation resolving is not a Part A / Part C / Part D
# property and pretending otherwise would be a different silence.
# ===========================================================================

def run_all(delta, resolved, prov, mod, ctx, destroyed):
    findings = []
    ctx["resolved"] = resolved
    ctx["operations"] = prov["declaration"]["operations"]
    ctx["predecessor"] = prov["parsedPredecessor"]
    # The resolver cache is keyed on the DECLARATION BLOCK's value, so the block's
    # NAME has to come from the resolution rather than be assumed: a mutation that
    # renames the block would otherwise hash an empty dict and every renamed
    # variant would share one cache entry.
    ctx["declarationBlock"] = prov.get("block", "derivedFrom")
    ctx.setdefault("partScoped", [])

    stages = (
        ("resolution", "all", lambda: check_resolution(delta, resolved, prov, ctx)),
        ("terminus", "all", lambda: check_terminus(delta, prov, ctx)),
        ("pathEncodingCorroboration", "all",
         lambda: check_path_encoding_corroboration(delta, ctx, ctx["snaps"])),
        ("resolvers", "all", lambda: run_resolvers(ctx["snaps"], delta, ctx)),
        ("census", "all", lambda: check_census(delta, resolved, prov, ctx)),
        ("keyLocator", "all", lambda: check_key_locator(delta, resolved, ctx)),
        ("recordedInputs", "all",
         lambda: check_recorded_inputs(delta, ctx, destroyed)),
        ("identity", "all", lambda: check_identity(delta, resolved, ctx)),
        ("ownResiduals", "all",
         lambda: check_own_residuals(delta, resolved, ctx)),
        ("publishedSweep", "all", lambda: check_published_sweep(delta, ctx)),
        ("derivedSweep", "all",
         lambda: check_derived_sweep(delta, resolved, prov, ctx)),
        ("anchorFolding", "all", lambda: cross_check_folding(ctx)),
    )
    for name, _scope, stage in stages:
        try:
            findings.extend(stage())
        except Exception as exc:  # noqa: BLE001
            findings.append(
                f"RT28-DRIVER {name}: could not run ({type(exc).__name__}: {exc}); "
                f"THIS IS A DEFECT IN THE DRIVER OR A SHAPE IT CANNOT READ, NOT A "
                f"MEASURED PROPERTY OF THE ARTIFACT")

    try:
        findings.extend(check_executed_closure(delta, resolved, mod, ctx))
        findings.extend(check_type_sweep(resolved, mod, ctx))
        ref_ctx = ctx.get("referenceContext") or {}
        findings.extend(cross_check_b1(resolved, mod, ref_ctx, ctx))
        findings.extend(cross_check_demotion(resolved, mod, ref_ctx, ctx))
        findings.extend(cross_check_partition(resolved, ctx))
    except mod.PinRefused:
        raise
    except Exception as exc:  # noqa: BLE001
        findings.append(
            f"RT28-DRIVER executedClosure: could not run ({type(exc).__name__}: "
            f"{exc}); THE 20 VECTORS AND 24 INVARIANTS WERE NOT EXERCISED and this "
            f"exit says nothing about them")
    return findings


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
    """(id, family, mutated delta) triples.  Every case is an input that is WRONG
    rather than merely EMPTY -- section 7.8's repair, which is what separates an
    instrument that detects deletion from one that detects falsehood."""
    cases = []

    def add(cid, family, mutate):
        try:
            cases.append((cid, family, mutate()))
        except Exception as exc:  # noqa: BLE001
            cases.append((cid, family, exc))

    D = "$.derivedFrom"
    # --- the resolution ----------------------------------------------------
    add("M01-resolved-digest-falsified", "RT28-DERIV-RESOLVED",
        lambda: _mut(delta, f"{D}.resolvedValue.sha256", "f" * 64))
    add("M02-operation-from-falsified", "RT28-DERIV-FROM",
        lambda: _mut(delta, f"{D}.operations[5].from", 16))
    add("M03-value-repair-reverted", "RT28-SWEEP",
        lambda: _mut(delta, f"{D}.operations[5].value", 15))
    add("M04-prose-repair-reverted", "RT28-SWEEP",
        lambda: _mut(delta, f"{D}.operations[7].value",
                     "0 independent reviews of these bytes. 2 Part B surfaces "
                     "proposed for change against 18 explicitly named as "
                     "unchanged."))
    add("M05-operation-deleted", "RT28-DERIV-EXACTLY",
        lambda: _mut(delta, f"{D}.operations",
                     delta["derivedFrom"]["operations"][:-1]))
    add("M06-operation-type-changed", "RT28-DERIV-TYPE",
        lambda: _mut(delta, f"{D}.operations[1].value", "28"))
    add("M07-operation-class-erased", "RT28-DERIV-CLASSES",
        lambda: _mut(delta, f"{D}.operations[0].class", "REPAIR"))
    add("M08-predecessor-digest-falsified", "RT28-DERIV-NO-PREDECESSOR",
        lambda: _mut(delta, f"{D}.predecessorSha256", "0" * 64))
    add("M09-canonical-digest-falsified", "RT28-DERIV-CANONICAL",
        lambda: _mut(delta,
                     f"{D}.predecessorProvenance.predecessorCanonicalValueSha256",
                     "1" * 64))
    add("M10-empty-operation-list", "RT28-DERIV-EMPTY-OPERATIONS",
        lambda: _mut(delta, f"{D}.operations", []))
    add("M11-declaration-block-renamed", "RT28-KEYLOC",
        lambda: {("aBlockNamedSomethingElse" if k == "derivedFrom" else k): v
                 for k, v in delta.items()})
    add("M12-path-display-prefix-restored", "RT28-DERIV-PATH",
        lambda: _mut(delta, f"{D}.operations[0].path", "$.artifact"))
    add("M13-payload-key-reverted-to-to", "RT28-DERIV-NO-VALUE",
        lambda: _mut(
            _del(delta, f"{D}.operations[2].value"),
            f"{D}.operations[2].to", "2026-08-10"))
    add("M14-differing-leaf-list-falsified", "RT28-DERIV-EXACTLY",
        lambda: _mut(delta, f"{D}.resolutionIsExactlyTheOperations."
                            f"differingLeafPaths",
                     ["$.artifact", "$.version"]))
    add("M15-substantive-delta-claim-falsified", "RT28-PRESERVED",
        lambda: _mut(delta, f"{D}.operations[6].value",
                     "20 inputs recorded with a digest and 0 gated, because "
                     "gating requires a checker and there is none."))

    # --- the terminus ------------------------------------------------------
    add("M16-predecessor-review-digest-falsified", "RT28-TERMINUS",
        lambda: _mut(delta, f"{D}.predecessorProvenance.predecessorReviewSha256",
                     "e" * 64))
    add("M17-predecessor-review-unnamed", "RT28-TERMINUS",
        lambda: _mut(delta, f"{D}.predecessorProvenance.predecessorReview",
                     "no-such-review.json"))

    # --- the census --------------------------------------------------------
    add("M18-resolved-census-falsified", "RT28-CENSUS",
        lambda: _mut(delta, f"{D}.resolvedDocumentCensus.scalarLeafPositions",
                     2934))
    add("M19-own-census-falsified", "RT28-CENSUS",
        lambda: _mut(delta, "$.leafCensusOfThisDeltaFile.boolLeafPositions", 206))
    add("M20-own-census-arithmetic-falsified", "RT28-CENSUS",
        lambda: _mut(delta, "$.leafCensusOfThisDeltaFile.arithmetic",
                     "544 + 207 + 1 + 0 = 752 non-string, and 752 + 1046 = 1798."))
    add("M21-float-path-list-falsified", "RT28-CENSUS",
        lambda: _mut(delta, "$.leafCensusOfThisDeltaFile.floatLeafPaths", []))
    add("M22-predecessor-census-falsified", "RT28-CENSUS",
        lambda: _mut(delta, f"{D}.resolvedDocumentCensus."
                            f"predecessorScalarLeafPositions", 2900))

    # --- the keyLocator ----------------------------------------------------
    add("M23-delta-only-key-is-not", "RT28-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.deltaOnlyKeys",
                     list(delta["keyLocator"]["deltaOnlyKeys"]) + ["leafCensus"]))
    add("M24-resolved-only-key-is-here", "RT28-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.resolvedOnlyKeys",
                     list(delta["keyLocator"]["resolvedOnlyKeys"]) + ["keyLocator"]))
    add("M25-partition-not-total", "RT28-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.deltaOnlyKeys",
                     [k for k in delta["keyLocator"]["deltaOnlyKeys"]
                      if k != "authorityBoundary"]))
    add("M26-operation-target-mismatch", "RT28-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.operationTargetKeys",
                     ["artifact", "version"]))
    add("M27-direction-checked-count-falsified", "RT28-KEYLOC",
        lambda: _mut(delta, "$.keyLocator.verification.direction1_"
                            "everyKeyCalledDELTA_ONLY_isAbsentFromTheResolved"
                            "Document.checked", 19))

    # --- pin hygiene -------------------------------------------------------
    add("M28-gated-row-demoted", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.recorded[0].class",
                     "ADVANCING"))
    add("M29-gated-digest-falsified", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.recorded[3].sha256",
                     "a" * 64))
    add("M30-destroyed-pin-erased", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.destroyed[0]."
                            "destroyedSha256", "b" * 64))
    add("M31-destroyed-row-removed", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.destroyed", []))
    add("M32-destroyed-file-claimed-deleted", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.destroyed[0]."
                            "theFileSTILLEXISTSAtDifferentBytes", False))
    add("M33-input-count-falsified", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.gatedCount", 7))
    add("M34-digests-recorded-count-falsified", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.digestsRecordedCount",
                     13))
    add("M35-input-row-removed", "RT28-INPUTS",
        lambda: _mut(delta, "$.recordedInputsOfThisDeltaFile.recorded",
                     delta["recordedInputsOfThisDeltaFile"]["recorded"][1:]))
    add("M36-remeasurement-row-falsified", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.inheritedMeasurementDisposition."
                            "theInheritedRecordedInputsDigests.measurement[0]."
                            "liveAtThisAuthoring", "c" * 64))
    add("M37-remeasurement-tally-falsified", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.inheritedMeasurementDisposition."
                            "theInheritedRecordedInputsDigests.rowsUnchanged", 18))

    # --- identity and posture ---------------------------------------------
    add("M38-status-applied", "RT28-RECORD",
        lambda: _mut(delta, "$.status", "APPLIED/SEALED"))
    add("M39-seal-recommended", "RT28-RECORD",
        lambda: _mut(delta, "$.sealRecommendation", "SEAL"))
    add("M40-head-claimed-moved", "RT28-RECORD",
        lambda: _mut(delta, "$.bindsNothing.theNamedArchitectureHeadIsUnchanged",
                     "retention-tiers.v28.json is now the named head."))
    add("M41-files-edited", "RT28-RECORD",
        lambda: _mut(delta, "$.bindsNothing.filesEdited", 3))
    add("M42-version-respelled-as-string", "RT28-RECORD",
        lambda: _mut(delta, "$.version", "28"))

    # --- residual accounting ----------------------------------------------
    add("M43-residual-count-falsified", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.newResidualCountOfThisSuccessor", 5))
    add("M44-residual-relabelled-closed", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.residualsLeftOpen.fromTheV26IndependentReview[0]."
                            "status", "CLOSED BY THIS SUCCESSOR"))
    add("M45-residual-count-closed-nonzero", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.residualsLeftOpen.countClosed", 2))
    add("M46-vectors-claimed-exercised", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.newResidualsOfThisSuccessor[0].measuredValues."
                            "vectorsMechanicallyExercisedAgainstIt", 20))
    add("M47-vector-population-falsified", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.newResidualsOfThisSuccessor[0].measuredValues."
                            "vectorsInTheResolvedDocument", 19))
    add("M48-chain-error-count-falsified", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.newResidualsOfThisSuccessor[7].measuredValues."
                            "fullChainResolveDerivationErrors", 12))
    add("M49-chain-errors-blamed-on-this-artifact", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.newResidualsOfThisSuccessor[7].measuredValues."
                            "errorsAttributableToThisArtifactsOwnOperations", 4))
    add("M50-inherited-register-count-falsified", "RT28-RESIDUAL",
        lambda: _mut(delta, "$.inheritedMeasurementDisposition."
                            "theInheritedRESIDUALREGISTERS.retainedResidualCount",
                     16))

    # --- the artifact's own published sweep --------------------------------
    add("M51-published-row-count-falsified", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep.rowsGenerated", 700))
    add("M52-flag-list-and-count-disagree", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep."
                            "flaggedCountOverTheResolvedValue", 14))
    add("M53-cleared-set-falsified", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep.clearedByThisSuccessor",
                     ["$.artifact"]))
    add("M54-adjudication-dropped", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep."
                            "everySurvivingFlagIsADJUDICATED.adjudications",
                     delta["staleMeasurementSweep"][
                         "everySurvivingFlagIsADJUDICATED"]["adjudications"][:-1]))
    add("M55-adjudication-classes-falsified", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep."
                            "everySurvivingFlagIsADJUDICATED.classesFound",
                     ["INVENTED-CLASS"]))
    add("M56-negative-control-emptied", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep.theNEGATIVECONTROL."
                            "caughtByTheGenerator", []))
    add("M57-per-family-table-falsified", "RT28-PUBSWEEP",
        lambda: _mut(delta, "$.staleMeasurementSweep."
                            "perFamilyCountsOverTheRESOLVEDvalue.B-INT-REFERENT."
                            "NO-REFERENT", 400))
    return cases


def selftest(delta, resolved, prov, mod, base_findings, ctx_template, destroyed):
    """Every mutation is a WRONG input, not an empty one.  The delta discipline is
    what makes the number meaningful over a base that is not clean: a mutation
    counts only if it produces a finding of its own family that is NOT in the
    base."""
    base = set(base_findings)
    failures = []
    caught = 0
    cases = build_selftest_cases(delta)
    for cid, family, mutated in cases:
        if isinstance(mutated, Exception):
            failures.append(f"{cid}: the mutation itself could not be built "
                            f"({type(mutated).__name__}: {mutated}); this case DID "
                            f"NOT RUN and is not counted as caught")
            continue
        ctx = dict(ctx_template)
        ctx["partScoped"] = []
        try:
            m_resolved, m_prov, m_errors = resolve_subject(mutated)
            if m_resolved is None:
                found = list(m_errors)
            else:
                found = run_all(mutated, m_resolved, m_prov, mod, ctx, destroyed)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{cid}: the run raised {type(exc).__name__}: {exc}; a "
                            f"crash is not a catch")
            continue
        fresh = [f for f in found if f not in base]
        hit = [f for f in fresh if f.startswith(family)]
        if hit:
            caught += 1
        elif fresh:
            failures.append(
                f"{cid}: ESCAPED its own family {family}. It produced {len(fresh)} "
                f"other new finding(s), the first being {fresh[0][:150]!r}. A "
                f"mutation caught by a different family measures that this checker "
                f"is noisy, not that it is aimed")
        else:
            failures.append(
                f"{cid}: ESCAPED ENTIRELY -- {family} did not fire and no other "
                f"family did either. This mutation is admitted")
    return failures, len(cases), caught


# ===========================================================================
# SECTION 11 -- THE SAME-TYPE FALSIFICATION RATE, MEASURED.
#
# Section 7.8 asks the operative question: CAN I MAKE THIS CHECKER PASS ON A
# WRONG ARTIFACT?  The predecessor published a COUNT of hand-found escapes and a
# reviewer then measured a FIFTEENTH escape that was a WHOLE CLASS -- 1,047 of
# 1,247 leaves, 84%, escaping same-type falsification, with 43 int/bool escapes
# in no named block, all falsifiable in one run with a byte-identical finding
# set.  A limits list that omits the dominant class is worse than none.
#
# So this instrument MEASURES ITS OWN RATE rather than enumerating examples.
# `--falsification` replaces every scalar leaf of the subject with a DIFFERENT
# VALUE OF THE SAME JSON TYPE, re-runs, and counts the leaves whose finding set
# is byte-identical to the base.  The figure is hard-compared against
# MEASURED_FALSIFICATION, so the disclosure cannot go stale (section 7.8's sixth
# design move: make the residual gate the build).
# ===========================================================================

def scalar_slots(node, chain=(), path="$"):
    """(index chain, display path, value) for every scalar leaf.  The CHAIN is
    what a mutator navigates; the PATH is only for reporting.  Addressing a leaf
    by re-parsing its display path breaks on any key containing a dot, and this
    artifact has hundreds."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from scalar_slots(value, chain + (key,), f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from scalar_slots(value, chain + (index,), f"{path}[{index}]")
    else:
        yield chain, path, node


def same_type_variant(value):
    """A DIFFERENT value of the SAME JSON type, or (False, None) where the type
    admits no second value.  `null` is the only such type and it is EXCLUDED FROM
    THE DENOMINATOR and reported, rather than counted as bound."""
    if isinstance(value, bool):
        return True, (not value)
    if isinstance(value, int):
        return True, value + 1
    if isinstance(value, float):
        return True, value + 1.0
    if isinstance(value, str):
        if SHA256_RE.match(value):
            head = "0" if value[0] != "0" else "1"
            return True, head + value[1:]
        numerals = _TOKEN_RE.findall(value)
        if numerals:
            first = numerals[0]
            return True, _TOKEN_RE.sub(
                lambda m: str(int(m.group(1)) + 1) if m.group(1) == first
                else m.group(1), value, count=1)
        reversed_text = value[::-1]
        return True, (reversed_text if reversed_text != value
                      else value + " NOT-THE-SAME")
    return False, None


_CLAIM_PATH_RE = re.compile(r"\$\.[A-Za-z0-9_]+(?:\.[A-Za-z0-9_-]+|\[\d+\])*")


def published_claims():
    """Which published disclosure claims which surface -- DERIVED FROM THE
    PUBLISHED LISTS THEMSELVES, never from a second private table.

    The escape list is scanned for the `$.` paths its own entries name.  That
    coupling is the point: SHRINK OR WEAKEN A DISCLOSURE AND THE LEAVES IT USED
    TO CLAIM BECOME `unclaimed`, WHICH FAILS THE BUILD.  A second private map
    would let the published list rot while the partition kept agreeing with it.

    ONLY THE ESCAPE LIST IS SCANNED, and each entry is truncated at its first
    `***` or `NOTE`.  Both narrowings are corrections made after measuring the
    first version of this function, which scanned the structural limits too and
    read whole entries: it derived `E8 -> $.leafCensusOfThisDeltaFile` (a surface
    E8 names as what CATCHES the mutation, not as one it escapes) and
    `limit 2 -> $.recordedInputs.recorded` (a container limit 2 names as
    something it PROVES).  A claim table that absorbs surfaces the run BINDS
    would quietly swallow a genuinely unclaimed leaf underneath one -- which is
    the failure this partition exists to expose.  The escape list is the
    enumeration of surfaces that are unbound; the structural limits describe
    classes, not surfaces.
    """
    claims = {}
    for entry in CAN_I_MAKE_THIS_PASS_ON_A_WRONG_ARTIFACT:
        ident = entry.split()[0].rstrip(".")
        claim_text = re.split(r"\*\*\*|NOTE[ ,]", entry)[0]
        for match in _CLAIM_PATH_RE.finditer(claim_text):
            claims.setdefault(match.group(0), ident)
    return claims


def claim_for(path: str, claims: dict):
    """The most specific published claim covering this leaf, or None."""
    best = None
    for claimed, ident in claims.items():
        if path == claimed or path.startswith(claimed + ".") \
                or path.startswith(claimed + "["):
            if best is None or len(claimed) > len(best[0]):
                best = (claimed, ident)
    return None if best is None else best[1]


def falsification_record_state():
    """(state, detail) for MEASURED_FALSIFICATION itself.

    Section 7.2.2: an uncompared measurement is prose that looks like evidence --
    and a figure whose own components DO NOT SUM is not even that.  This file
    shipped, for one revision, `attempted: 1799, bound: 0, free: 0` under a
    comment reading "MEASURED ... by --falsification": a placeholder publishing
    itself as a measurement.  This predicate is what makes that state impossible
    to hold silently.  It is consulted by --falsification, by --selftest and by
    --limits, so the placeholder cannot masquerade in ANY channel.
    """
    rec = MEASURED_FALSIFICATION
    needed = ("attempted", "bound", "free", "unclaimed", "ratePercent")
    missing = [k for k in needed if k not in rec]
    if missing:
        return "UNMEASURED", f"missing member(s) {missing}"
    if not all(isinstance(rec[k], int) and not isinstance(rec[k], bool)
               for k in ("attempted", "bound", "free", "unclaimed")):
        return "UNMEASURED", "a count is not a JSON integer"
    if rec["attempted"] <= 0:
        return "UNMEASURED", "attempted is not positive"
    if rec["bound"] + rec["free"] != rec["attempted"]:
        return ("UNMEASURED",
                f"bound {rec['bound']} + free {rec['free']} = "
                f"{rec['bound'] + rec['free']}, which is not attempted "
                f"{rec['attempted']}. A published rate whose own components do "
                f"not sum was never produced by a sweep")
    expected = round(100.0 * rec["free"] / rec["attempted"], 1)
    if rec["ratePercent"] != expected:
        return ("UNMEASURED",
                f"ratePercent {rec['ratePercent']} is not "
                f"free/attempted = {expected}")
    if rec["unclaimed"] > rec["free"]:
        return "UNMEASURED", "unclaimed exceeds free"
    return "MEASURED", "components sum and the rate is their quotient"


def falsification_sweep(delta, mod, ctx_template, destroyed, base_findings,
                        limit=None):
    """Returns a report.  Every leaf is attempted; nothing is sampled.

    THE RATE IS PARTITIONED, NOT MERELY TOTALLED, and the partition is the part
    that carries information.  A headline percentage over this artifact is
    dominated by $.corpusChecksRun, several hundred leaves that escape E3 ALREADY
    NAMES AS UNBOUND -- so a large total is disclosure being CORROBORATED, not a
    defect.  The half that is a finding is `unclaimed`: free leaves in NO named
    block at all.  That is the shape a reviewer measured on the predecessor
    lineage, where 43 int/bool escapes sat in no named block, restating
    quantities the run itself computes; the 84% total was noise around it.
    """
    base = list(base_findings)
    claims = published_claims()
    report = {"attempted": 0, "bound": 0, "free": 0,
              "excludedNoSecondValue": 0, "errors": 0,
              "freeByTopLevelKey": {}, "boundByTopLevelKey": {},
              "freeByClaim": {}, "unclaimedPaths": []}
    # THE SLOTS ARE WALKED, NOT RE-PARSED FROM PATH STRINGS, and that is a
    # correction rather than a style choice.  A first run addressed each leaf by
    # re-parsing its `$.a.b` path, and _STEP_RE splits on `.` -- so every leaf
    # under a key that CONTAINS a dot, of which this artifact has hundreds
    # (`perCheckerRecord.check-c2-v11.py`), silently failed to resolve and was
    # skipped by a `continue`.  The sweep reported 997 attempted where the
    # document holds 1799 scalar leaves: A SILENT UNDERCOUNT OF 802, in the very
    # measurement whose whole purpose is to bound what this instrument cannot
    # see.  Walking (container, key) slots cannot have that defect, and the
    # attempted count is compared against the census so it can never recur.
    slots = list(scalar_slots(delta))
    if limit:
        slots = slots[:limit]
    for position, (chain, path, value) in enumerate(slots):
        if position and position % 100 == 0:
            print(f"  ... {position}/{len(slots)} slot(s) swept, "
                  f"{report['bound']} bound, {report['free']} free", flush=True)
        ok, variant = same_type_variant(value)
        top = chain[0] if chain else "?"
        if not ok:
            report["excludedNoSecondValue"] += 1
            continue
        report["attempted"] += 1
        try:
            mutated = copy.deepcopy(delta)
            node = mutated
            for step in chain[:-1]:
                node = node[step]
            node[chain[-1]] = variant
        except Exception:  # noqa: BLE001
            report["errors"] += 1
            continue
        ctx = dict(ctx_template)
        ctx["partScoped"] = []
        try:
            m_resolved, m_prov, m_errors = resolve_subject(mutated)
            if m_resolved is None:
                found = list(m_errors)
            else:
                found = run_all(mutated, m_resolved, m_prov, mod, ctx, destroyed)
        except Exception:  # noqa: BLE001
            report["errors"] += 1
            found = None
        if found is None or found == base:
            report["free"] += 1
            report["freeByTopLevelKey"][top] = \
                report["freeByTopLevelKey"].get(top, 0) + 1
            ident = claim_for(path, claims)
            if ident is None:
                report["unclaimedPaths"].append(path)
            else:
                report["freeByClaim"][ident] = \
                    report["freeByClaim"].get(ident, 0) + 1
        else:
            report["bound"] += 1
            report["boundByTopLevelKey"][top] = \
                report["boundByTopLevelKey"].get(top, 0) + 1
    report["unclaimed"] = len(report["unclaimedPaths"])
    report["freeInDeclaredUnbound"] = report["free"] - report["unclaimed"]
    report["ratePercent"] = (round(100.0 * report["free"] / report["attempted"], 1)
                             if report["attempted"] else None)
    return report


# ===========================================================================
# SECTION 12 -- WHAT THIS INSTRUMENT CANNOT CATCH.
# ===========================================================================

WHAT_THIS_CANNOT_CATCH = (
    ("1. A JUDGEMENT stated falsely. Section 7.8's measured boundary: these "
     "instruments bind structure and type, not the truth of content. An "
     "instrument CAN bind prose that asserts a MEASUREMENT -- by re-deriving the "
     "measurement -- and that is done throughout. Nothing binds prose that "
     "asserts a JUDGEMENT, because no oracle exists for it."),
    ("2. Whether the three repairs are the RIGHT repairs. This instrument proves "
     "that 19 is the length of the container $.recordedInputs.recorded and that "
     "14 is the Part B UNCHANGED count. It cannot prove that `recordedInputs` was "
     "ever meant to count that list. The referent resolver in section 6 "
     "normalises a path step and matches it against containers; a wrong referent "
     "produces a confident wrong answer in both directions, and its NO-REFERENT "
     "population -- published every run -- is the honest bound."),
    ("3. Whether the executed reference derivation is CORRECT. "
     "check-retention-custody-v26.py is hash-verified and executed under section "
     "7.3, which makes it a runtime input rather than a contract -- but its 20 "
     "vectors and 24 invariants encode ONE reading of Part A, Part C and Part D. "
     "This file's second implementation cross-checks the Cap algebra, the "
     "demotion scan, the biconditional and the partition; it does not re-derive "
     "the other twenty invariants. Where the two agree, they agree about a "
     "reading."),
    ("4. The artifact's own 706-row sweep generator. This instrument writes a "
     "DIFFERENT derived sweep and runs it against both subjects; it does not "
     "re-execute the artifact's. Every INTERNAL arithmetic claim that block makes "
     "is hard-compared -- per-family verdicts summing to the row count, the "
     "flag-set difference equalling the cleared set, every flagged path "
     "adjudicated exactly once, the published class list equalling the classes "
     "the adjudications carry -- so the block cannot be internally incoherent. It "
     "could still be coherently fabricated."),
    ("5. That $.corpusChecksRun is accurate. It reports 113 checkers across three "
     "phases and nothing here re-runs them. Note in particular that the artifact "
     "itself records check-product-dispositions-v2.py as non-deterministic over "
     "an unchanged tree, so no diff of it is an attribution signal."),
    ("6. A coherent lie. Flip an operation's `from` AND the predecessor's value "
     "together and the resolution still verifies -- except that the predecessor "
     "is GATED, so this particular lie costs an exit-2 refusal rather than a "
     "green run. The general form survives: any falsehood consistent across every "
     "position this instrument compares is admitted."),
    ("7. Whether this artifact SHOULD be applied. Section 7.1 grades a candidate "
     "with no retained checker DISQUALIFYING FOR APPLICATION, and section 7.8 is "
     "explicit that a companion instrument written after the fact does not "
     "discharge that: what discharges the residual is an INDEPENDENT "
     "RE-DERIVATION. This file NARROWS the residual's measured half and closes "
     "nothing. It does not edit $.retainedChecker, which the artifact publishes "
     "as NONE."),
    ("8. That the document establishing the terminus REVIEWED the predecessor "
     "rather than merely RECORDING it. The discovery test is structural -- it "
     "requires a document that pairs the predecessor's filename with its live "
     "byte digest in one object, that is not a derivation over it, and that "
     "publishes a blocking-finding tally -- plus the narrowing that it must not "
     "also record the SUBJECT's own bytes, which stops a successor nominating "
     "its own review. Measured on this corpus that leaves 2 candidates and 1 "
     "after the narrowing. But a review of a THIRD artifact that happened to "
     "record the predecessor as a verified input and published its own blocker "
     "count would qualify. Nothing here reads a `subject` field, because doing so "
     "would be CMP-IR-01 -- inferring a document's nature from a key name -- and "
     "the honest position is that this test finds documents that BIND the "
     "predecessor's bytes and carry a verdict, which is what section 7.3's "
     "argument actually rests on, and not documents that are ABOUT it."),
    ("9. A word-numeral figure whose sibling record does not hold the value it "
     "partitions. Family W is deliberately WIDER than the artifact's generator "
     "and its extra rows are published as CANDIDATES rather than emitted as "
     "findings -- measured: it reaches $.newResiduals[6].statement, where "
     "\"three of the four are arguments and one is a quotation\" partitions a "
     "sibling 4, which is arithmetic and not staleness. Emitting it would be "
     "manufacturing the false accusation this instrument exists to prevent, and "
     "not emitting it means a genuine word-numeral defect inherited from the "
     "predecessor would also pass. Only one that is INTRODUCED or that lands ON "
     "AN OPERATION PATH fails the build."),
)

CAN_I_MAKE_THIS_PASS_ON_A_WRONG_ARTIFACT = (
    ("E1  Rewrite every `why` on every operation at $.derivedFrom.operations with a fabricated rationale. "
     "Eight strings, narrative, compared to nothing. The operation's verb, path, "
     "`from`, `value` and `class` are all gated; the reason is not."),
    ("E2  Rewrite $.instrumentPosition.answer from 'NO' to 'YES' -- claiming the "
     "predecessor's instrument DOES validate v28. Measurably false, and nothing "
     "here reads that field."),
    ("E3  Falsify $.corpusChecksRun wholesale: every per-checker digest, every "
     "exit code, the 113 count, the three-phase results, the 1474.5 seconds. "
     "This instrument runs no checker sweep, so all of it is free. THIS IS THE "
     "LARGEST SINGLE UNBOUND SURFACE IN THE ARTIFACT, at several hundred leaves, "
     "and it is the dominant term in the measured rate printed above."),
    ("E4  Rewrite the eleven `whyNotClosed` strings under $.residualsLeftOpen so each names a different and "
     "false reason for leaving its residual open. The ids and the OPEN status are "
     "gated; the reasons are not."),
    ("E5  Rewrite $.staleMeasurementSweep's fifteen adjudication `reason` strings "
     "-- the class labels are cross-checked against classesFound and the paths "
     "against the flag set, but the SENTENCE explaining each adjudication is "
     "free. A reader persuaded by a false argument to a true conclusion has been "
     "misled about the method."),
    ("E6  Falsify $.thePredecessorChainRefusal's narrative: its account of v26's "
     "change-log, its verb list, its 'errorIndicesCovered' prose. The 30-error "
     "count and the 0-attributable count ARE re-executed here; the story around "
     "them is not."),
    ("E7  Falsify $.authorityBoundary entirely: claim 3 product decisions made "
     "and 2 statuses changed. Nothing here reads that block and no instrument in "
     "the corpus reads it either."),
    ("E8  REWRITE the eight entries of $.whatIDidNotCheck into eight false "
     "disclosures, KEEPING THE COUNT AT EIGHT. Byte-identical finding set. "
     "*** THIS ENTRY IS PUBLISHED IN ITS CORRECTED FORM, AND THE CORRECTION IS "
     "THE POINT. *** It was first written as 'shrink the list to one, or to "
     "zero', on the reasoning that a shrinking limitations list is invisible. "
     "THAT WAS FALSE and executing it said so: shrinking to one produces FOUR "
     "findings, because $.leafCensusOfThisDeltaFile declares 1799 scalar leaves "
     "and the walk then measures 1792. A reviewer measured the predecessor "
     "publishing an 'escape' (its own E8) that was not one; this list was "
     "therefore executed in BOTH DIRECTIONS before publication, twelve probes, "
     "and the two that failed were rewritten rather than dropped. So the honest "
     "statement is narrower than the tempting one: the CARDINALITY of this "
     "artifact's disclosure list is bound, and its CONTENT is not."),
    ("E9  Rewrite $.derivedFrom.operationPathEncoding, the paragraph explaining "
     "why the string path encoding is used rather than the better array one. The "
     "encoding itself is gated -- a `$.` prefix is refused by name -- and the "
     "argument for it is not."),
    ("E10 Substitute a plausible different authority in any narrative mention of "
     "CD-RT-5's attribution inside the DELTA file, at $.inheritedMeasurementDisposition. The executed reference "
     "re-extracts the nine quoted decision fields from the LIVE packet in the "
     "RESOLVED document, so the resolved-side quotations are gated; the delta "
     "file's own prose about them is not."),
    ("E11 Rewrite $.resolverExecutionRecord's prose -- "
     "$.resolverExecutionRecord.results.theHONESTsummary, "
     "$.resolverExecutionRecord.bothResolversTargetedBecause, and the "
     "theAcceptanceTest sentences. Each verified separately as byte-identical. "
     "Both resolvers ARE executed here and their numeric results are compared, so "
     "the figures are gated; the sentences are not. NOTE the exact paths: a first "
     "probe of this entry wrote theHONESTsummary at the BLOCK level, where it "
     "does not live, which ADDS a leaf and is caught by the census -- so the "
     "probe was wrong rather than the entry, and it was re-run at the real paths "
     "before being published."),
    ("E12 Falsify $.resolverExecutionRecord.resolverReferenceCensus's figures 69 and 1. This instrument "
     "does not count how many artifacts name each resolver."),
)


def print_limits(measured=None) -> None:
    print("check-retention-custody-v28.py -- WHAT THIS INSTRUMENT CANNOT CATCH")
    print()
    print("Section 7.8 asks the operative question directly: CAN I MAKE THIS")
    print("CHECKER PASS ON A WRONG ARTIFACT?  The honest answer is YES.")
    print()
    print("FIRST, THE DOMINANT CLASS, MEASURED RATHER THAN ENUMERATED.  A reviewer")
    print("of the predecessor measured a fifteenth escape that was a WHOLE CLASS --")
    print("1,047 of 1,247 leaves, 84%, escaping same-type falsification -- after")
    print("that instrument published a count of fourteen.  A limits list that omits")
    print("the dominant class is worse than none, so this one leads with it:")
    print()
    figures = measured or MEASURED_FALSIFICATION
    state, detail = falsification_record_state()
    if state != "MEASURED":
        print(f"    *** NOT YET MEASURED ON THESE BYTES *** {detail}.")
        print(f"    This channel refuses to present the record as a measurement")
        print(f"    while its own components do not sum. Run --falsification,")
        print(f"    which prints the figures and FAILS until they are written in.")
        print()
    print(f"    SAME-TYPE FALSIFICATION RATE, over every scalar leaf of the")
    print(f"    subject, each replaced by a DIFFERENT VALUE OF THE SAME JSON TYPE")
    print(f"    and the whole run re-executed:")
    print(f"        leaves attempted            {figures.get('attempted')}")
    print(f"        BOUND   (finding set moved) {figures.get('bound')}")
    print(f"        FREE    (byte-identical)    {figures.get('free')}")
    print(f"        RATE                        {figures.get('ratePercent')}% free")
    print(f"        FREE-IN-NO-NAMED-BLOCK      {figures.get('unclaimed')}"
          f"  <- the only half that is a finding")
    print(f"    Recompute it with --falsification, which hard-compares against the")
    print(f"    figures above and FAILS if they disagree in either direction.")
    print()
    print(f"THEN THE ENUMERATED EXAMPLES, {len(CAN_I_MAKE_THIS_PASS_ON_A_WRONG_ARTIFACT)}"
          f" of them, each worked.  Every one has")
    print("the shape section 7.8 measured on the C-2 instrument: a string leaf")
    print("whose VALUE is false while its PATH and TYPE are unchanged.  Each was")
    print("CHECKED IN BOTH DIRECTIONS -- asserted to be an escape only after the")
    print("mutation was executed and the finding set observed unchanged -- because")
    print("a reviewer found the predecessor publishing an 'escape' that was not.")
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
    print("reading retention-tiers.v28.json and the freeze sections it cites, by a")
    print("lane that did not author the artifact.  That makes it a second reading")
    print("rather than a second opinion from the same mind, and section 7.8's")
    print("bound still holds in its stronger form: A GREEN RUN IS AUTHOR-SIDE")
    print("EVIDENCE.  What discharges the residual section 7.1 grades")
    print("DISQUALIFYING is an independent re-derivation, not another instrument")
    print("from a closely related mind.")


# ===========================================================================
# SECTION 13 -- MAIN.
# ===========================================================================

def _banner(part, notices, ctx, audit):
    census_r = ctx.get("resolvedCensus") or {}
    census_d = ctx.get("deltaCensus") or {}
    vec = ctx.get("vectorReport") or {}
    inv = ctx.get("invariantReport") or {}
    b1 = ctx.get("b1") or {}
    sweep = ctx.get("sweep") or {}
    tsweep = ctx.get("typeSweep") or {}
    tcounts = ctx.get("typeCounts") or {}
    verb = ctx.get("verbatim") or {}
    term = ctx.get("terminus") or {}
    dest = ctx.get("destroyedStanding") or {}
    resolvers = ctx.get("resolvers") or {}
    print(f"RETENTION-CUSTODY v28  part={part}  gated pins {len(GATED_PINS)}  "
          f"advancing {len(ADVANCING_PINS)}  destroyed 1  drift notices "
          f"{len(notices)}")
    print(f"  EXECUTED CLOSURE (declared, pinned, AST-audited): "
          f"{len(EXECUTED_MODULES)} module(s), {len(audit.get('loaderCalls') or [])} "
          f"loader edge(s) found in this file's own source, "
          f"{audit.get('execNodes')} exec node(s), "
          f"{len(audit.get('unpinnedDeclared') or [])} declared-but-unpinned")
    print(f"  DERIVATION RESOLVED: predecessor {ctx.get('predecessorName')} byte "
          f"{str(ctx.get('predecessorDigest'))[:16]}..., canonical value "
          f"{str(ctx.get('predecessorCanonical'))[:16]}...; "
          f"{len(ctx.get('operations') or [])} operations "
          f"({len((ctx.get('operationClasses') or {}).get('IDENTITY', []))} "
          f"IDENTITY, "
          f"{len((ctx.get('operationClasses') or {}).get('REPAIR', []))} REPAIR) "
          f"-> resolved value {str(ctx.get('resolvedDigest'))[:16]}...")
    print(f"  TERMINUS BY THE REVIEW TEST (section 7.3, 2026-08-10): "
          f"{term.get('populationScanned')} corpus document(s) swept, "
          f"{term.get('reviewCount')} discovered review(s) of the predecessor of "
          f"which {term.get('reviewsIndependentOfTheSubject')} do not also record "
          f"the subject's own bytes, "
          f"declared {term.get('declaredReview')} at "
          f"{str(term.get('declaredReviewDigest'))[:16]}... reporting "
          f"{term.get('blockingFindings')} blocking finding(s) -> TERMINUS "
          f"{term.get('isTerminus')}. The predecessor DOES carry a "
          f"derivation-shaped block "
          f"({ctx.get('predecessorHasDeclarationShape')}), so the review test is "
          f"deciding something a shape screen would decide by accident")
    print(f"  resolution is EXACTLY the operations: "
          f"{len(ctx.get('differingLeafPaths') or [])} differing leaf path(s) "
          f"against {len(ctx.get('operations') or [])} operation path(s); the "
          f"predecessor lane's own resolved value reproduced by repairing FORM "
          f"only at {str(ctx.get('v27IntendedDigest'))[:16]}..., differing from "
          f"this one at {len(ctx.get('identityOnlyDifference') or [])} path(s), "
          f"all IDENTITY")
    for rel, record in sorted(resolvers.items()):
        print(f"  RESOLVER {rel.split('/')[-1]}: declaration "
              f"{'RETURNED' if record.get('declarationReturned') else 'REFUSED'} at "
              f"{len(record.get('declarationErrors') or [])} error(s); "
              f"{record.get('operationsApplied')}/{record.get('operationsDeclared')} "
              f"operations applied at {len(record.get('applyErrors') or [])} "
              f"error(s) -> {str(record.get('resolvedCanonicalSha256'))[:16]}...; "
              f"FULL CHAIN {'materialised' if record.get('fullChain') else 'refused'} "
              f"with {len(record.get('fullChainErrors') or [])} error(s), 0 of them "
              f"naming an operation of this artifact")
    penc = ctx.get("pathEncoding") or {}
    print(f"  path-encoding corroboration, RE-MEASURED from the five recorded "
          f"artifacts rather than relayed: {penc.get('examined')} operation "
          f"list(s) examined, {penc.get('stringPaths')} STRING path(s) of which "
          f"{penc.get('dollarPrefixed')} carry the `$.` display prefix, "
          f"{penc.get('arrayPaths')} ARRAY-of-token path(s)")
    print(f"  census: resolved {census_r.get('scalarLeafPositions')} scalar leaves "
          f"({census_r.get('intLeafPositions')} int / "
          f"{census_r.get('boolLeafPositions')} bool / "
          f"{census_r.get('floatLeafPositions')} float / "
          f"{census_r.get('nullLeafPositions')} null / "
          f"{census_r.get('stringLeafPositions')} string), bool tested BEFORE int; "
          f"the INT-FIRST CONTROL reports "
          f"{census_r.get('intFirstControl_intLeafPositions')} against the true "
          f"{census_r.get('intLeafPositions')}; delta file "
          f"{census_d.get('scalarLeafPositions')}")
    print(f"  keyLocator: {ctx.get('keyLocatorDirections', 0)} directions executed "
          f"over a claimed PARTITION, both sides")
    print(f"  pin hygiene: {dest.get('filesSwept')} file(s) swept for the DESTROYED "
          f"digest, {len(dest.get('carriers') or [])} carrier(s); the destroyed "
          f"path STILL EXISTS ({dest.get('pathStillExists')}) at "
          f"{str(dest.get('pathLiveDigest'))[:16]}... -- MUTATED, NOT DELETED, so "
          f"a reader checking only existence misreads the pin; inherited digest "
          f"rows re-measured {ctx.get('reMeasuredRows')}")
    print(f"  ASSERTED OVER THE RESOLVED VALUE, NOT THE DELTA BYTES:")
    print(f"    vectors {vec.get('executed', 0)}/{vec.get('declared', 0)} executed, "
          f"{vec.get('controlsRun', 0)} rejected readings run, "
          f"{len(vec.get('controlsVacuous') or [])} vacuous; invariants "
          f"{inv.get('executed', 0)}/{inv.get('declared', 0)} executed")
    print(f"    B1: {len(b1.get('publishedAgree') or [])}/"
          f"{b1.get('arithmeticRows', 0)} arithmetic rows agree under the PUBLISHED "
          f"expressions, {len(b1.get('v25Agree') or [])}/"
          f"{b1.get('arithmeticRows', 0)} under the PREDECESSOR's; default 0/0/0 "
          f"evicts nothing across {b1.get('defaultConfigSizesSwept', 0)} sizes "
          f"({len(b1.get('defaultConfigNonZeroV25') or [])} of those evict under "
          f"the predecessor's); {len(b1.get('crossDimensionSymbols') or [])} "
          f"cross-dimension symbols; {b1.get('prefixInclusionViolations', 0)} "
          f"prefix-inclusion violations over {b1.get('prefixConfigurations', 0)} "
          f"configurations")
    print(f"    law 14 -- NO REACHABLE SILENT DEMOTION: "
          f"{ctx.get('xcheckDurableCells')} DURABLE_AUTHORITATIVE cells and "
          f"{ctx.get('xcheckOutcomes')} outcomes scanned, "
          f"{ctx.get('xcheckDemotionViolations')} reachable silent demotion(s); "
          f"d9Axes<->NOT-A-TERMINATION biconditional "
          f"{(ctx.get('xcheckBiconditional') or {}).get('rows')} rows, "
          f"{(ctx.get('xcheckBiconditional') or {}).get('deviations')} deviations; "
          f"the two law-14 invariants {ctx.get('law14Invariants')} are declared, "
          f"DRIVEN by name by the executed reference, and named by 0 findings")
    print(f"    partition {(ctx.get('partition') or {}).get('total')} keys "
          f"({(ctx.get('partition') or {}).get('partA')} Part A + "
          f"{(ctx.get('partition') or {}).get('partB')} Part B; Part B "
          f"{(ctx.get('partition') or {}).get('partBUnchanged')} UNCHANGED / "
          f"{(ctx.get('partition') or {}).get('partBChanged')} CHANGED, which is "
          f"the referent of the second repair)")
    print(f"    quotations: {verb.get('verbatimVerified')} of "
          f"{verb.get('verbatimStringKeys')} string-valued *Verbatim keys verified "
          f"against the source each field's own NAME attributes it to; "
          f"{verb.get('verbatimFalseAbsent')} of "
          f"{verb.get('verbatimSourceAttributed')} would read FALSE-ABSENT under a "
          f"raw byte-literal search and "
          f"{verb.get('verbatimFalseAbsentNormalised')} under a "
          f"whitespace-normalised one, so section 7.7 folding is load-bearing")
    print(f"    type sweep (law 18): {tsweep.get('respellingsAttempted')} "
          f"respellings attempted, {tsweep.get('respellingsAdmitted')} admitted; "
          f"{tcounts.get('guardedIntOrBoolLeafPositions')} guarded int/bool "
          f"positions, {tcounts.get('unruledIntOrBoolLeafPositions')} unruled")
    print(f"  SECOND IMPLEMENTATION: Cap algebra agrees on "
          f"{(ctx.get('xcheckB1') or {}).get('agreed')} rows, disagrees on "
          f"{(ctx.get('xcheckB1') or {}).get('disagreed')}; default 0/0/0 evicts at "
          f"{ctx.get('xcheckDefaultNonZero')} of 201 sizes independently")
    pop_r = (sweep.get("populationOverTheResolvedValue") or {})
    pop_p = (sweep.get("populationOverThePredecessor") or {})
    print(f"  DERIVED self-measurement sweep -- ROW SET GENERATED, POPULATION "
          f"PUBLISHED (section 7.2.2's ENUMERATION mode): {pop_r.get('TOTAL')} rows "
          f"over the resolved value and {pop_p.get('TOTAL')} over the predecessor "
          f"(R referent {pop_r.get('R-INT-REFERENT')} / P decimal-prose "
          f"{pop_r.get('P-PROSE-DECIMAL')} / W WORD-numeral "
          f"{pop_r.get('W-PROSE-WORD')}). NOT ONE path is written into this file.")
    print(f"    definitive referent disagreements: "
          f"{sweep.get('definitiveOverThePredecessor')} over the VERIFIED "
          f"PREDECESSOR (the control -- the artifact's headline defect, "
          f"reproduced) and {sweep.get('definitiveOverTheResolvedValue')} over the "
          f"RESOLVED value; {len(sweep.get('introduced') or [])} restatement "
          f"disagreement(s) INTRODUCED, {len(sweep.get('cleared') or [])} cleared, "
          f"{len(sweep.get('onOperationPaths') or [])} on an operation path")
    print(f"    ENCODING mode: the resolved value carries "
          f"{(sweep.get('wordDensityResolved') or {}).get('wordNumeralOccurrences')} "
          f"word-numeral occurrence(s) against "
          f"{(sweep.get('wordDensityResolved') or {}).get('intLeaves')} integer "
          f"leaves (ratio "
          f"{(sweep.get('wordDensityResolved') or {}).get('ratio')}); the delta "
          f"file "
          f"{(sweep.get('wordDensityDelta') or {}).get('wordNumeralOccurrences')} "
          f"against {(sweep.get('wordDensityDelta') or {}).get('intLeaves')}. An "
          f"integer census is silent about every one of them")
    print(f"    {len(sweep.get('unadjudicatedCandidates') or [])} restatement "
          f"candidate(s) this generator reaches that the artifact does not "
          f"adjudicate, published as COVERAGE and not as findings because this "
          f"generator is measurably WIDER than the artifact's: "
          f"{[p for p in (sweep.get('unadjudicatedCandidates') or [])][:3]}")
    print(f"  DERIVED delta gate: REPAIR operations at {ctx.get('repairPaths')}; "
          f"{len(ctx.get('repairedBefore') or [])} finding(s) fired at those paths "
          f"against the verified predecessor and 0 against the resolved value; "
          f"families in scope under --part {part}: "
          f"{len(ctx.get('familiesInScopeUnderThisPart') or [])}; "
          f"{len(ctx.get('closureRemoved') or [])} finding(s) removed and "
          f"{len(ctx.get('closureAdded') or [])} added by resolving, all explained "
          f"by an operation path")
    print(f"  freeze anchors {(ctx.get('anchorFolding') or {}).get('folded')}/"
          f"{(ctx.get('anchorFolding') or {}).get('total')} under section 7.7 "
          f"folding ({(ctx.get('anchorFolding') or {}).get('raw')} under a raw "
          f"search, {(ctx.get('anchorFolding') or {}).get('whitespace')} under a "
          f"whitespace-normalised one); CD-RT-5 read live, not pinned: status "
          f"{ctx.get('cdRt5', (None, None))[0]!r}, "
          f"{ctx.get('cdRt5', (None, None))[1]} quoted decision fields re-extracted "
          f"from the live packet")
    for line in notices:
        print(f"  {line}")
    for line in (ctx.get("classSkips") or []):
        print(f"  {line}")
    for line in (ctx.get("partScoped") or []):
        print(f"  {line}")
    for line in (ctx.get("referenceNotices") or []):
        print(f"  [executed closure] {line}")
    print("  a green run is author-side evidence only; run --limits for the "
          "MEASURED same-type falsification rate and for what this instrument "
          "cannot catch")


def _refuse(message: str) -> int:
    sys.stderr.write(message.rstrip() + "\n")
    return 2


def main() -> int:
    argv = sys.argv[1:]
    part = "all"
    do_selftest = False
    do_falsification = False
    do_limits = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--selftest":
            do_selftest = True
        elif arg == "--falsification":
            do_falsification = True
        elif arg == "--limits":
            do_limits = True
        elif arg == "--part":
            index += 1
            if index >= len(argv) or argv[index] not in ("a", "c", "d", "all"):
                return _refuse("RT28-UNSUPPORTED-INVOCATION: --part takes a, c, d "
                               "or all. THE CHECK DID NOT RUN.")
            part = argv[index]
        elif arg.startswith("--part="):
            part = arg.split("=", 1)[1]
            if part not in ("a", "c", "d", "all"):
                return _refuse("RT28-UNSUPPORTED-INVOCATION: --part takes a, c, d "
                               "or all. THE CHECK DID NOT RUN.")
        else:
            return _refuse(
                f"RT28-UNSUPPORTED-INVOCATION: unknown option {arg!r}. There is "
                f"deliberately NO option to name a subject: this instrument "
                f"carries frozen id tuples and transcribed leaf names about "
                f"{SUBJECT} and must not be pointable at a document it does not "
                f"describe. THE CHECK DID NOT RUN.")
        index += 1

    if do_limits:
        print_limits()
        return 0

    # BLOCKER 1: this cannot raise, and it is no longer the first thing that
    # touches the disk without a guard behind it.
    before = measure_all_inputs()

    audit, audit_failures = audit_execution_edges()

    try:
        snaps, notices, skipped, floors = verified_inputs()
    except InputUnavailable as exc:
        return _refuse(
            f"{exc}\nRT28-INPUT-UNAVAILABLE: a REQUIRED input is absent, "
            f"unreadable, or below its FLOOR, so NOTHING WAS PARSED OR EXECUTED "
            f"and THE CHECK DID NOT RUN. This exit says nothing whatever about "
            f"{SUBJECT}, and in particular says nothing about its 20 vectors or "
            f"its 24 invariants. Exit 2 is not the findings code; exit 1 is.")
    except PinRefused as exc:
        return _refuse(
            f"{exc}\nRT28-PIN-REFUSED: the verified execution closure did not "
            f"match its pinned digests, so NOTHING WAS PARSED OR EXECUTED and THE "
            f"CHECK DID NOT RUN. Repair is a successor instrument, never an edit "
            f"to these bytes.")

    destroyed, destroyed_refusals = destroyed_standing()
    if destroyed_refusals:
        return _refuse(" | ".join(destroyed_refusals)
                       + "\nRT28-INTEGRITY-REFUSED: THE CHECK DID NOT RUN.")
    if destroyed.get("classSkipped"):
        notices.append(destroyed["classSkipped"])
        skipped.setdefault("resurrectionGuard", []).append(
            f"{len(destroyed['unreadable'])} unreadable file(s) under artifacts/")

    subject_bytes, reason = read_input(f"artifacts/{SUBJECT}")
    if subject_bytes is None:
        return _refuse(f"RT28-INPUT-UNAVAILABLE {SUBJECT}: {reason}. The subject "
                       f"itself could not be read. THE CHECK DID NOT RUN.")
    live_subject = sha_bytes(subject_bytes)
    if live_subject != SUBJECT_SHA256:
        notices.append(
            f"RT28-SUBJECT-MOVED {SUBJECT}: dispatched at "
            f"{SUBJECT_SHA256[:16]}..., {SUBJECT_BYTES} bytes; live "
            f"{live_subject[:16]}..., {len(subject_bytes)} bytes. This instrument "
            f"REPORTS rather than refuses, because refusing to parse would hide "
            f"every other finding behind one line -- but section 7.2 says a change "
            f"to reviewed bytes requires a version bump and a new verdict and may "
            f"never be made in place.")

    try:
        delta = parse_json(subject_bytes, SUBJECT)
    except PinRefused as exc:
        return _refuse(f"RT28-PARSE-REFUSED: {exc}. THE CHECK DID NOT RUN.")
    if not isinstance(delta, dict):
        return _refuse("RT28-PARSE-REFUSED: the subject is not a JSON object. THE "
                       "CHECK DID NOT RUN.")

    try:
        mod = load_pinned_module("artifacts/check-retention-custody-v26.py",
                                 snaps["artifacts/check-retention-custody-v26.py"])
    except Exception as exc:  # noqa: BLE001
        return _refuse(
            f"RT28-CLOSURE-REFUSED: the hash-verified reference derivation did not "
            f"load ({type(exc).__name__}: {exc}). THE CHECK DID NOT RUN and the 20 "
            f"vectors and 24 invariants were NOT exercised.")

    # BLOCKER 1, one level down: the reference derivation reads its own closure
    # with bare read_bytes(), so its inputs are checked HERE, before it runs.
    problems = reference_inputs_readable(mod)
    if problems:
        return _refuse(
            f"RT28-CLOSURE-REFUSED: {len(problems)} input(s) of the hash-verified "
            f"reference derivation are unreadable or below their floor: "
            f"{problems[:5]}. Executing it would surface an unreadable file as a "
            f"DRIVER finding about {SUBJECT}. THE CHECK DID NOT RUN.")

    resolved, prov, errors = resolve_subject(delta)
    prov = prov or {}
    if resolved is None:
        print("RT28-DERIVATION-UNRESOLVED: this subject declares a derivation and "
              "it could not be materialised. NO PROPERTY OF THE RESOLVED DOCUMENT "
              "WAS CHECKED -- not one of its 20 vectors, not one of its 24 "
              "invariants. Asserting over the delta bytes instead is exactly the "
              "defect IMPLEMENTATION-FREEZE.md section 7.3's 2026-08-06 rider "
              "forbids, and this instrument will not do it.")
        for error in errors:
            print(f"  - {error}")
        return 1

    ctx = {"part": part, "snaps": snaps,
           "freezeText": snaps["IMPLEMENTATION-FREEZE.md"].decode("utf-8", "replace"),
           "predecessorName": prov.get("predecessor"),
           "predecessorDigest": prov.get("predecessorByteDigest"),
           "predecessorCanonical": prov.get("predecessorCanonicalDigest"),
           "predecessorHasDeclarationShape":
               prov.get("predecessorHasDeclarationSHAPE")}

    try:
        findings = run_all(delta, resolved, prov, mod, ctx, destroyed)
    except mod.PinRefused as exc:
        return _refuse(
            f"RT28-CLOSURE-REFUSED: the executed reference derivation refused its "
            f"own pinned closure ({exc}). THE CHECK DID NOT RUN; the 20 vectors "
            f"and 24 invariants were NOT exercised and this exit says nothing "
            f"about them.")
    findings.extend(audit_failures)
    for line in (ctx.get("classSkips") or []):
        if line not in notices:
            notices.append(line)
        skipped.setdefault(line.split(":")[0].split()[-1], []).append(line[:80])

    if do_falsification:
        template = {k: v for k, v in ctx.items()
                    if k in ("part", "snaps", "freezeText", "predecessorName",
                             "predecessorDigest", "predecessorCanonical",
                             "predecessorHasDeclarationShape")}
        report = falsification_sweep(delta, mod, template, destroyed, findings)
        print(f"RETENTION-CUSTODY v28 SAME-TYPE FALSIFICATION SWEEP over "
              f"{SUBJECT}")
        print(f"  leaves attempted            {report['attempted']}")
        print(f"  excluded (no second value)  {report['excludedNoSecondValue']}")
        print(f"  BOUND   (finding set moved) {report['bound']}")
        print(f"  FREE    (byte-identical)    {report['free']}")
        print(f"  RATE                        {report['ratePercent']}% free")
        print()
        print(f"  THE PARTITION, WHICH IS THE PART THAT CARRIES INFORMATION.")
        print(f"  A total alone misdescribes this instrument: most free leaves sit")
        print(f"  in surfaces a published disclosure ALREADY NAMES as unbound, and")
        print(f"  measuring them is that disclosure being CORROBORATED. The half")
        print(f"  that is a FINDING is the leaves no published disclosure claims.")
        print(f"    FREE-IN-DECLARED-UNBOUND   {report['freeInDeclaredUnbound']}")
        for ident, count in sorted(report["freeByClaim"].items(),
                                   key=lambda kv: -kv[1]):
            print(f"        {count:5d}  claimed by {ident}")
        print(f"    FREE-IN-NO-NAMED-BLOCK     {report['unclaimed']}   "
              f"<-- the only half that is a finding")
        for path in report["unclaimedPaths"]:
            print(f"        {path}")
        print()
        print(f"  free leaves by top-level key:")
        for key, count in sorted(report["freeByTopLevelKey"].items(),
                                 key=lambda kv: -kv[1])[:8]:
            print(f"      {count:5d}  {key}")
        print(f"  bound leaves by top-level key:")
        for key, count in sorted(report["boundByTopLevelKey"].items(),
                                 key=lambda kv: -kv[1])[:8]:
            print(f"      {count:5d}  {key}")
        # THE SWEEP'S OWN COVERAGE IS GATED AGAINST THE CENSUS.  This is the
        # repair for the defect the first run of this mode had: it addressed
        # leaves by re-parsing display paths, silently lost every leaf under a
        # dotted key, and reported 997 attempted where the document holds 1799.
        # A coverage figure that cannot disagree with the population it claims to
        # cover is the paper seal section 7.2.2 grades.
        walked = census(delta)
        expected = walked["scalarLeafPositions"] - walked["nullLeafPositions"]
        if report["attempted"] + report["errors"] != expected:
            print(f"FALSIFICATION-COVERAGE-SHORT: attempted "
                  f"{report['attempted']} + {report['errors']} error(s) against "
                  f"{walked['scalarLeafPositions']} scalar leaves less "
                  f"{walked['nullLeafPositions']} null leaf/leaves = {expected} "
                  f"falsifiable position(s). A sweep that silently skips part of "
                  f"its population reports a rate over a document it did not "
                  f"measure.")
            return 1
        if report["excludedNoSecondValue"] != walked["nullLeafPositions"]:
            print(f"FALSIFICATION-EXCLUSION: {report['excludedNoSecondValue']} "
                  f"leaf/leaves excluded as having no second value of their type "
                  f"and the census counts {walked['nullLeafPositions']} null "
                  f"leaf/leaves, which is the only such type.")
            return 1
        state, detail = falsification_record_state()
        if state != "MEASURED":
            print(f"FALSIFICATION-UNMEASURED: the published "
                  f"MEASURED_FALSIFICATION record is not a measurement -- "
                  f"{detail}. It is presented under a comment claiming it was "
                  f"measured, which is section 7.2.2's exact class: prose wearing "
                  f"a measurement's clothes. The figures this run produced are "
                  f"above; write them in.")
            return 1
        mismatched = [k for k in ("attempted", "bound", "free", "unclaimed",
                                  "ratePercent")
                      if report[k] != MEASURED_FALSIFICATION.get(k)]
        if mismatched:
            print(f"FALSIFICATION-DRIFT: {mismatched} disagree with the published "
                  f"MEASURED_FALSIFICATION figures {MEASURED_FALSIFICATION}. "
                  f"Section 7.8's sixth design move: the disclosure is made to gate "
                  f"the build so it cannot go stale in EITHER direction.")
            return 1
        print("FALSIFICATION-AGREES with the published figures")
        return 0

    if do_selftest:
        # WHAT MAKES A BASE DIRTY, and the distinction is deliberate.  An
        # RT28-PIN-ADVANCED notice is declared NON-FATAL by the artifact itself
        # (CITED-DIGEST-RECORDED-NOT-GATED) and by section 7.10, and the freeze is
        # under permanent concurrent edit -- so counting it as dirt means the
        # suite can NEVER certify in this tree, which is a suite that has been
        # disabled by its own honesty.  A notice about the BYTES UNDER TEST is a
        # different thing: RT28-SUBJECT-MOVED and RT28-TREE-MOVED both say the
        # measurement may not describe the subject, and those DO make it dirty.
        about_the_subject = [n for n in notices
                             if n.startswith(("RT28-SUBJECT-MOVED",
                                              "RT28-TREE-MOVED",
                                              "RT28-CLASS-SKIPPED"))]
        dirty = bool(findings) or bool(about_the_subject) or bool(skipped)
        if notices and not dirty:
            print(f"SELFTEST-BASE-CLEAN-WITH-{len(notices)}-ADVANCING-NOTICE(S): "
                  f"the notices below are drift on inputs the artifact classifies "
                  f"CITED-DIGEST-RECORDED-NOT-GATED and section 7.10 grades a "
                  f"named non-fatal advance. They are printed, they are not dirt, "
                  f"and no notice about the SUBJECT'S OWN BYTES is present.")
            for line in notices:
                print(f"  base notice: {line[:160]}")
        if dirty:
            print("SELFTEST-OVER-DIRTY-BASE: the base is NOT clean, so this run "
                  "certifies nothing and cannot return 0. The suite is executed "
                  "under delta discipline -- every mutation must produce a finding "
                  "of its own family NOT PRESENT IN THE BASE -- and the number "
                  "below is reported, not attested.")
            for line in notices:
                print(f"  base notice: {line[:160]}")
            for finding in findings:
                print(f"  base finding: {finding[:220]}")
        template = {k: v for k, v in ctx.items()
                    if k in ("part", "snaps", "freezeText", "predecessorName",
                             "predecessorDigest", "predecessorCanonical",
                             "predecessorHasDeclarationShape")}
        failures, cases, caught = selftest(delta, resolved, prov, mod, findings,
                                           template, destroyed)
        print(f"RETENTION-CUSTODY v28 SELFTEST"
              f"{' (dirty base)' if dirty else ''}: {caught}/{cases} mutations "
              f"caught by their own named family")
        # BLOCKER 4: the execution-edge audit gates the selftest.
        print(f"EXECUTION-EDGE AUDIT: {len(audit.get('loaderCalls') or [])} loader "
              f"edge(s) in this file's source, {len(EXECUTED_MODULES)} declared, "
              f"{audit.get('execNodes')} exec node(s), "
              f"{audit.get('evalNodes')} eval, "
              f"{audit.get('dynamicImportNodes')} dynamic import(s) -- "
              f"{'AGREES' if not audit_failures else 'DISAGREES'}")
        # THE PUBLISHED RESIDUAL GATES THE BUILD (section 7.8's sixth design
        # move).  A record whose components do not sum was never produced by a
        # sweep, and this file shipped exactly that for one revision under a
        # comment claiming it was measured.  The selftest fails on it, so the
        # state cannot recur silently in any channel.
        record_state, record_detail = falsification_record_state()
        print(f"PUBLISHED FALSIFICATION RECORD: {record_state} -- {record_detail}")
        if record_state != "MEASURED":
            failures.append(
                f"MEASURED_FALSIFICATION is published as a measurement and is not "
                f"one ({record_detail}). Run --falsification and write in the "
                f"figures it prints; until then the disclosure is prose wearing a "
                f"measurement's clothes")
        for failure in audit_failures:
            print(f"  - {failure}")
        for failure in failures:
            print(f"  - {failure}")
        if dirty:
            print(f"SELFTEST-NOT-CERTIFYING ({len(findings)} base finding(s), "
                  f"{len(notices)} drift notice(s), {len(skipped)} skipped "
                  f"class(es))")
            return 3
        if failures or audit_failures:
            print("SELFTEST-FAIL")
            return 1
        print("SELFTEST-PASS")
        return 0

    after = measure_all_inputs()
    moved = sorted(name for name in before if before.get(name) != after.get(name))
    if moved:
        notices.append(
            f"RT28-TREE-MOVED {len(moved)} declared input(s) changed digest DURING "
            f"this run: {moved}. Every finding below is UNSAFE TO ATTRIBUTE -- the "
            f"tree moved under the measurement, which is the section 7.2.1 "
            f"concurrency hazard, and the correct response is to re-run over a "
            f"quiescent tree rather than to read this output.")

    _banner(part, notices, ctx, audit)

    if findings:
        print(f"{len(findings)} finding(s) in the RESOLVED value of {SUBJECT}:")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    if skipped:
        print(f"RT28-PARTIAL: {len(skipped)} class(es) DID NOT RUN because a "
              f"per-class input was unavailable: {sorted(skipped)}. This is NOT a "
              f"pass over {SUBJECT} -- the classes that ran found nothing and the "
              f"classes that did not run assert nothing. Exit 4 is distinct from "
              f"0 precisely so a reader cannot mistake a partial measurement for a "
              f"clean one.")
        return 4
    print(f"{SUBJECT}: PASS over its RESOLVED VALUE "
          f"{str(ctx.get('resolvedDigest'))[:16]}... (architecture-candidate "
          f"scope; CANDIDATE-NOT-APPLIED; the artifact's own $.retainedChecker "
          f"remains NONE and this file does not change it; section 7.1 still "
          f"grades the residual DISQUALIFYING FOR APPLICATION and a companion "
          f"instrument written after the fact does not discharge it -- what does "
          f"is an independent re-derivation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
