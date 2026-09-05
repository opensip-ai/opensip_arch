#!/usr/bin/env python3
"""Retained checker for retention-tiers.v26.json.

WHY THIS FILE EXISTS, STATED BEFORE ANYTHING ELSE.

  retention-tiers.v26.json was independently reviewed and ACCEPTED at 0 blocking
  findings and 5 non-blocking observations.  Its own largest live residual is
  RT25-RES-01: *no retained checker -- 0 of 20 vectors and 0 of 24 invariants are
  mechanically exercised.*  IMPLEMENTATION-FREEZE.md section 7.1 grades that
  residual "a fair residual for a candidate, DISQUALIFYING for application", and
  the review says so in the same words at
  $.verdict.applicationDisposition.  Section 7.8 records that the residual has now
  been misread as a wall five times: sections 7.2 and 7.6 forbid EDITING a
  reviewed artifact, and a NEW CHECKER IS A NEW FILE AND EDITS NOTHING.  The
  review noted expressly that "the route was therefore open to v26 and was not
  taken."  This file takes it.

  It executes all 20 rows of $.partC_retentionBounds.vectors.rows and all 24
  entries of $.partC_retentionBounds.invariants.  Every one can fail.  Section
  7.2.2's rider is the standard -- a measurement that cannot fail the build is
  prose -- and section 7.8's repair is the one applied: for every assertion,
  exhibit an input that is WRONG rather than merely EMPTY.  Each negative-control
  row additionally executes the REJECTED READING the row itself names, and
  requires that reading to produce the DIFFERENT result the row declares.  A
  control whose rejected reading produces the same answer as the accepted one is
  reported as VACUOUS rather than counted as a pass.

  It edits nothing.  It writes nothing.  It reads twenty files and names every
  one of them with the digest it expects.

THIS CHECKER DOES NOT EXIT 0 ON THE LIVE ARTIFACT, AND THE REASON IS A FINDING,
NOT A DEFECT IN THE CHECKER.

  RT26-COUNT  $.corpusResiduals[0].measuredValues.recordedInputs declares 15 and
              $.corpusResiduals[0].measuredBoundary reads "15 inputs recorded
              with a digest and 0 gated".  These bytes record NINETEEN, and
              $.recordedInputs.digestsRecordedCount says 19 four keys away.  The
              figure is retention-tiers.v25's, carried forward verbatim into a
              successor that recorded four more inputs.  It is a RECORDED
              MEASUREMENT about the artifact's own bytes, so section 7.2.2 gives
              it a hard comparison, and it fails one.  The independent review's
              publishedCountsSweep hard-compared fifteen structural counts and
              this was not among them; its residualGrading block grades six
              residuals by name and $.corpusResiduals is not among those either.
              So this is not a re-report of a known observation.  It is not
              tuned away, not scoped out, and not downgraded to a notice: a
              checker adjusted until it agrees with its subject launders the
              defect and is worth less than no checker.

READ-VS-PIN.  THE CHOICE SECTION 7.10 IS ABOUT, MADE DELIBERATELY AND STATED.

  Section 7.10 is the most expensive structural fact this corpus has produced: a
  guard that pins a decision's CURRENT state asserts that state will never
  change, and on 2026-08-05 applying the real CD-RT-5 decision flipped nineteen
  checkers from exit 0 to non-zero on one string.  Within the hour two lanes
  faced the identical choice about product-dispositions.v1.json and chose
  oppositely; the digest-pinner (check-versioning-v14.py) went red inside forty
  minutes when the packet legitimately advanced again, and the content-pinner
  (retention-tiers.v26.json itself) survived unchanged.

  A DIGEST PIN CANNOT DISTINGUISH "the input legitimately advanced" FROM "the
  input is wrong."  Both present as a hash mismatch and both remedies are a new
  instrument, which is unsustainable by inspection.  So this file implements
  three classes, and the class is part of the diagnostic:

    GATED (14)      Exactly the rows retention-tiers.v26.json itself marks
                    HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN at
                    $.recordedInputs.recorded[].gate.  This checker does not
                    invent the classification; it implements the artifact's.
                    Every one is reviewed, frozen or superseded bytes that no
                    lane has any business advancing.  Drift -> RT26-PIN-REFUSED,
                    EXIT 2, nothing parsed.

    ADVANCING (5)   The five rows the artifact marks
                    CITED-DIGEST-RECORDED-NOT-GATED: the binding product packet,
                    the CD-RT-5 amendment draft, and the three markdown
                    documents.  Four of the five are named by the artifact at
                    $.recordedInputs.citedDigestsThatMovedDuringAuthoring as
                    under concurrent edit.  Drift here is a NAMED, NON-FATAL
                    NOTICE -- RT26-PIN-ADVANCED -- printed with both digests, and
                    the run continues against the LIVE bytes.  What is checked
                    against those live bytes is the PROPERTY, not the value.

    DESTROYED (1)   product-dispositions.cd-rt-5-amendment.draft.v1.json was
                    edited IN PLACE after retention-tiers.v25 hard-pinned it at
                    4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea.
                    The file is untracked, has no git history, and those bytes
                    are UNRECOVERABLE, so that pin can never be satisfied by
                    anything.  This checker does not carry the dead pin as a
                    gate -- v26 reclassified the file and this instrument
                    implements v26's classification -- but it records the digest
                    and refuses to let the live bytes be mistaken for the pinned
                    ones: if the live draft ever hashes to 4bbcd6fa..., that is
                    a fabrication and RT26-PIN-RESURRECTED fires at EXIT 2.
                    A pin that ADVANCED is re-pinnable.  A pin that was MUTATED
                    AND DESTROYED is not, and the two must not print the same.

  THE PROPERTY PIN ON CD-RT-5, which is the whole point of the rule.  Nothing in
  this file asserts that CD-RT-5 is DECIDED, or BLOCKED_ON_PHASE_1A, or anything
  else.  It asserts, against whatever the live packet says today:

    * the packet parses under a duplicate-key-rejecting hook and carries exactly
      one CD-RT-5 row, in $.decisions or in $.pendingDecisions but not both;
    * that row's status is drawn from a closed vocabulary and is not a bracketed
      placeholder;
    * if the status is DECIDED then decidedBy and decidedOn are both filled by a
      NAMED authority on a REAL ISO date -- no "[UNSET]", no "[NAME]", no "TBD",
      no empty string -- which is the fabrication section 4.4 is the forensic
      record of;
    * the artifact's own six statements of that state agree with the live packet
      and with each other, so a silent reversion in either direction is a
      finding;
    * every *Verbatim field the artifact attributes to the packet re-extracts
      from the LIVE packet under section 7.7 folding, by deriving the packet
      field name from the artifact's own key name rather than from a table here;
    * the posture fields agree across packet and artifact: durableDefault and
      implicitDurableRetention are the same values in both.

  All of that survives a legitimate amendment of the packet -- the corpus is
  explicitly waiting for further amendments -- and none of it survives
  fabrication, silent reversion or an unfilled placeholder.  If the packet
  advances, this checker costs a re-read.  It does not cost a successor.

ENVIRONMENT PREREQUISITES, DECLARED UP FRONT (section 7.2: a verdict binds bytes
AND AN ENVIRONMENT, and an undeclared dependency makes the verdict
environment-conditional).  A CRASH MUST NOT READ AS A FINDING.

  1. CPython 3.9 or later.  Checked at startup; a lower version prints
     RT26-UNSUPPORTED-INTERPRETER and exits 2 saying the check DID NOT RUN.
  2. Invoked as `python3 -I -B`.  Caller-owned isolated startup is the
     prevention boundary; script code cannot undo interpreter or site activity
     that happened before line 1.  Otherwise RT26-UNSUPPORTED-INVOCATION, exit 2.
  3. THE PYTHON STANDARD LIBRARY ONLY.  No third-party package, no subprocess,
     no external binary, and in particular NO ripgrep.  `rg` is a shell function
     on this host and is not on PATH; check-rust-provider-protocol-v2 and -v4
     abort with a traceback for exactly that reason and their PASSED verdicts
     cannot be reproduced.  This file shells out to nothing.
  4. All twenty read inputs present beside this file or one directory up.  A
     missing input is RT26-INPUT-MISSING at exit 2, naming the path -- never a
     traceback and never a finding.
  Every failure above exits 2 with a named diagnostic whose text says the check
  did not run.  Exit 1 is reserved for findings about the artifact.

WHAT A GREEN RUN WOULD BE, AND WHAT IT WOULD NOT BE.  (Section 7.8, answered.)

  It would be author-side evidence that this artifact says what it says
  consistently, that its arithmetic and its algebra close, that its quotations
  are quotations, and that drift in a gated input will be caught.  It would
  NEVER be evidence that the artifact is RIGHT.  This instrument binds
  STRUCTURE, TYPE, ARITHMETIC and DERIVATION.  It does not bind the TRUTH OF
  PROSE: a string leaf whose VALUE is false while its PATH and TYPE are
  unchanged passes.  Run --limits for the enumerated list and the count.

  One asymmetry is worth a signer's attention.  This file was NOT written by the
  lane that authored retention-tiers.v26.json, and it was written AFTER an
  independent review of those bytes.  That makes it a second reading rather than
  a second opinion from the same mind -- but section 7.8's bound still holds in
  its stronger form, because this author read the review before writing the
  instrument.  Where the review named a property, this file re-derives it rather
  than asserting the review's number: it re-executes the seven arithmetic rows,
  re-walks the census, re-partitions the thirty-five keys and re-folds the
  thirty-seven quotations from the sources themselves.  A driver that hardcoded
  "37 of 37" would pass on a successor that fabricated all of them.

Exit matrix, distinct by construction:
    0  clean
    1  findings about the artifact
    2  bad invocation, unsupported environment, missing input, integrity refusal,
       or a GATED pin mismatch.  THE CHECK DID NOT RUN.
    3  selftest refused or not certifying (the base was not clean, so a mutation
       result certifies nothing even though it is still reported)

Invocation:  python3 -I -B check-retention-custody-v26.py [--selftest]
                                                          [--part a|c|d|all]
                                                          [--limits]
"""

from __future__ import annotations

import sys

MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write(
        "RT26-UNSUPPORTED-INTERPRETER: this instrument requires CPython "
        f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later and found "
        f"{sys.version_info[0]}.{sys.version_info[1]}.  THE CHECK DID NOT RUN; "
        "no statement about retention-tiers.v26.json is made by this exit.\n")
    raise SystemExit(2)

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "RT26-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-retention-custody-v26.py`.  Caller-owned isolated startup is the "
        "prevention boundary; script code cannot undo interpreter or site "
        "activity that happened before line 1.  THE CHECK DID NOT RUN.\n")
    raise SystemExit(2)

import copy
import hashlib
import itertools
import json
import pathlib
import re
import unicodedata
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent
SUBJECT = "retention-tiers.v26.json"

# The dispatched and reviewed digest of the subject.  Recorded, compared, and
# reported as a NAMED NOTICE rather than a refusal: the subject is what this
# instrument is about, so a reader must be told when it moves, and a successor
# artifact is the lawful way for it to move.  Refusing to parse would hide every
# other finding behind one line.
SUBJECT_SHA256 = "a6546408fb38df95166f0ec41b1d9d9dae0dbda580684ff8a6e94f57145ad97e"
SUBJECT_BYTES = 297835

# ---------------------------------------------------------------------------
# GATED.  Exactly the fourteen rows retention-tiers.v26.json marks
# HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN at
# $.recordedInputs.recorded[].gate.  The classification is the ARTIFACT'S; this
# table implements it and check_recorded_inputs compares the two in both
# directions on every run, so a row that silently changes class is a finding.
# Section 7.2's recording obligation: a count is not a record, so every member is
# named with its digest.
# ---------------------------------------------------------------------------
GATED_PINS = {
    "retention-tiers.v25.json":
        "d62c1c0f3eec5ac7b496a4f2fe60b73daafdc69a2cbd500685d0800e54eeca52",
    "retention-tiers.v25.review-independent.json":
        "479355a5b2d4338131d952f72db45e7382ab79bdda7a5aadd70bcd7a7dc2789d",
    "retention-tiers.v24.json":
        "ba29c115a9064ab1cd66ea01751b238acf092b3d699ca43027de7a8dfe55a277",
    "retention-tiers.v24.review-independent.json":
        "633301d5fb6400858a1e10acca50aefe8e58502ef346d5f3d06f6da5cff0084a",
    "retention-tiers.v23.json":
        "3f8c1df562bde9dbaa6e6d87cfb611a7f2a88710f01519344ca72c5005a0891b",
    "retention-tiers.v23.review-independent.json":
        "039419b49d06999d4142346f8982eadb511ab6efc635b5e116f0694d6412719f",
    "retention-tiers.v22.json":
        "52aa540df75a047f0abc09b4fab4b472ab2934ad1f488146bb370ed6050743e1",
    "check-retention-custody-v24.py":
        "9a309302df6d2f1108f1fbfb4978bfc93b102eb0394c99ba7be7fc550d7fa909",
    "check-retention-custody-v23.py":
        "18e94f7603869e8fdf295664f8d7eb46d9075ea8fc1791769045fb194b4a96a8",
    "check-retention-custody-v25.py":
        "8e7b86d59b3276dc9ee998c059684e834a82e2d9b9d9f4c200eb1e3da9b57d2d",
    "d9-exit-contract.v1.14.json":
        "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31",
    "check-product-dispositions-v2.py":
        "71999471340e53389227a11ee1886865b9822f4f4229f5fc83c8a4b968d4daad",
    "threat-model.v3.json":
        "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    "evidence.v10.json":
        "62a3a07194062c8499f6e943b4986d7a77bdecc0c4ec499851ac078fd548e9b4",
}

# ---------------------------------------------------------------------------
# ADVANCING.  The five rows the artifact marks CITED-DIGEST-RECORDED-NOT-GATED.
# These are the files the corpus is explicitly waiting to change.  The recorded
# digests are THE ARTIFACT'S, deliberately left as v26 wrote them: they are the
# baseline a drift notice prints against, and replacing them with today's values
# would erase the record rather than check it.  Drift is a named non-fatal
# notice.  Section 7.10: pin what you depend on and re-extract it.
# ---------------------------------------------------------------------------
ADVANCING_PINS = {
    "artifacts/product-dispositions.v1.json":
        "bbe24527f732f9c265f9cf71b988303a326e45fec0c6adb0d934536d515d6017",
    "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json":
        "c4bd85c62ee957ba04fd9d99f8b8f780138792409eb51b79a2aff2d35d334b12",
    "ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md":
        "47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e",
    "IMPLEMENTATION-FREEZE.md":
        "2fedf9250fe3f9d1685dc81f2672a0d2905630a5fd8a04fd191affec84e32e02",
    "IMPLEMENTER-BLUEPRINT.md":
        "7b2efc2d3bcdbd5ba0cdbb05b450e258299976b54242dca9d740e2eb673c817d",
}

# ---------------------------------------------------------------------------
# DESTROYED.  A pin whose bytes no longer exist anywhere.  This is NOT a gate --
# retention-tiers.v26.json reclassified the file and this instrument implements
# the artifact's classification -- but the dead digest is recorded so a reader
# meets the explanation instead of hunting a corruption, and so that a file
# reappearing at the destroyed digest is refused rather than welcomed.
# ---------------------------------------------------------------------------
DESTROYED_PINS = {
    "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json": (
        "4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea",
        "retention-tiers.v25 hard-pinned these bytes under the gate string "
        "HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN.  The "
        "coordinator then edited the file IN PLACE, to withdraw a false claim it "
        "carried (that a retention reason code closes RT23-B-RES-01; measured "
        "live it does not -- still 0 of 9, 0 of 9, 0 of 19).  A draft.v2 "
        "successor was the compliant move and was not taken.  The file is "
        "untracked, has no git history, and the pinned bytes are UNRECOVERABLE. "
        "check-retention-custody-v25.py refuses at exit 2 on this pin and can "
        "never be repaired, which is section 7.6 observed live.  A pin that "
        "ADVANCED is re-pinnable; a pin that was MUTATED AND DESTROYED is not."),
}

# The artifact's own list of files it declares unstable, used to grade a drift
# notice.  Read from the artifact at runtime as well, and compared: a file that
# drifts while NOT declared unstable gets a sharper notice than one that does.
DECLARED_UNSTABLE_FALLBACK = (
    "IMPLEMENTATION-FREEZE.md",
    "IMPLEMENTER-BLUEPRINT.md",
    "artifacts/product-dispositions.cd-rt-5-amendment.draft.v1.json",
    "artifacts/product-dispositions.v1.json",
)

# Content anchors instead of a whole-file digest, for the reason
# check-retention-custody-v23/-v24/-v25 all give: these documents are under
# concurrent edit and a digest recorded for a file under edit is false the moment
# it is written.  Matched under section 7.7 folding, so a reflow, a blockquote or
# an emphasis run does not manufacture a refusal, while REMOVAL of the cited text
# still fails closed.  Section 7.10 names the hazard these guard against: when
# check-retention-custody-v23/-v24 began refusing their pins before parsing
# anything, the FREEZE_ANCHORS guard they carried went inert and nothing
# announced it.  These anchors are checked before any pin can stop the run.
FREEZE_ANCHORS = (
    # law 18 -- the exact-type rule PC-V-06/07/08 and RT25-C-INV-09 rest on
    "Closed-scalar admission is exact-type.",
    "A boolean is not an integer, a float is not an integer, and a numeric "
    "string is not a number, in any admission path, at any depth, including "
    "inside records the host only forwards.",
    # law 14 -- quoted verbatim by v26 twice, and the basis of PC-V-10/14 and
    # of the entire silent-demotion adjudication
    "A durability failure cannot report authoritative success; a provider fault "
    "cannot become a finding; a policy failure cannot become a host error.",
    # law 6 -- the separate-identity rule behind RETENTION-BOUNDS-ID-V1
    "separate identities with separate descriptors and separate custody",
    # law 8 -- the one-ledger-per-ProjectId rule behind DEP-RT25-03
    "cross-project physical deduplication is forbidden",
    # 7.2 -- why v24 is inherited by reference and never edited
    "An independent review verdict binds the exact bytes reviewed and the "
    "environment",
    # 7.2.2 rider -- the standard this instrument is held to
    "a measurement that cannot fail the build is prose",
    # 7.8 -- the bound this instrument prints against itself
    "these instruments bind structure and type; they do not bind the truth of "
    "content",
    # 7.8 -- the sentence that makes this file lawful at all
    "a new checker is a new file and edits nothing",
    # 7.10 -- the read-vs-pin rule this instrument implements
    "pin the PROPERTY, not the CURRENT VALUE, whenever the value is",
    # 7.1 -- the grade on the residual this instrument exists to narrow
    "a fair residual for a candidate, disqualifying for",
)


class PinRefused(RuntimeError):
    """A GATED pin did not match, or an input could not be read.  Exit 2."""


class DuplicateKeyError(ValueError):
    pass


class RefusedError(RuntimeError):
    """A reference derivation must refuse rather than substitute."""


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate object key {key!r}")
        out[key] = value
    return out


def _parse(source: bytes, name: str) -> Any:
    """Section 7.5: every JSON input is parsed under a hook that raises on any
    repeated key at any depth, so a document that says one thing to one reader
    and another to the next is refused rather than silently resolved."""
    try:
        return json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise PinRefused(f"{name}: {type(exc).__name__}: {exc}") from exc


_PUNCT = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-",
    "—": "-", "―": "-", "−": "-",
    "…": "...", " ": " ", " ": " ", " ": " ",
    " ": " ", " ": " ",
}
_MD = re.compile(r"[*_`|\\>#]+")


def fold(text: str) -> str:
    """Section 7.7's folding, applied BEFORE any containment test.

    The section records that a byte-literal search on a multi-word phrase returns
    a false ABSENT on line-wrapped text, and that whitespace normalisation ALONE
    still returns ABSENT on a blockquote -- IMPLEMENTATION-FREEZE.md states its
    standing rules inside `>` blocks.  Measured on these bytes: three of the
    thirty-six source-attributed verbatim fields return ABSENT under a raw
    byte-literal search and PRESENT under this folding, so a reviewer who skipped
    the discipline would publish three false findings.  The count is recomputed
    on every run and printed, not asserted.
    """
    text = unicodedata.normalize("NFKC", text)
    for src, dst in _PUNCT.items():
        text = text.replace(src, dst)
    text = _MD.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _resolve(rel: str) -> pathlib.Path:
    """Inputs are named the way the artifact names them -- some with an
    `artifacts/` prefix, some bare.  Both roots are tried and the path actually
    read is reported, so a reader can tell which file was measured."""
    candidates = [COOP / rel, HERE / rel, HERE / pathlib.PurePosixPath(rel).name]
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


def measured_digest(rel: str):
    path = _resolve(rel)
    if not path.is_file():
        return None
    return sha_bytes(path.read_bytes())


def verified_inputs():
    """Read every declared input as inert bytes and classify BEFORE parsing.

    Returns (snapshots, notices).  A GATED mismatch or a missing input raises
    PinRefused, which main() turns into a named exit-2 diagnostic saying the
    check did not run.  An ADVANCING mismatch becomes a non-fatal notice and the
    live bytes are used.  A DESTROYED digest reappearing is a refusal.
    """
    snaps = {}
    notices = []
    errors = []

    for name, expected in GATED_PINS.items():
        path = _resolve(name)
        if not path.is_file():
            errors.append(f"RT26-INPUT-MISSING {name}: not found beside this "
                          f"instrument or one directory up")
            continue
        data = path.read_bytes()
        actual = sha_bytes(data)
        if actual != expected:
            errors.append(
                f"RT26-PIN-REFUSED {name}: GATED at {expected}, live {actual}. "
                f"The artifact itself classifies this input "
                f"HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN, so "
                f"this instrument refuses rather than re-pointing it. Repair is "
                f"a SUCCESSOR instrument, never an edit to this one")
            continue
        snaps[name] = data

    for name, expected in ADVANCING_PINS.items():
        path = _resolve(name)
        if not path.is_file():
            errors.append(f"RT26-INPUT-MISSING {name}: not found beside this "
                          f"instrument or one directory up")
            continue
        data = path.read_bytes()
        snaps[name] = data
        actual = sha_bytes(data)
        dead = DESTROYED_PINS.get(name)
        if dead and actual == dead[0]:
            errors.append(
                f"RT26-PIN-RESURRECTED {name}: the live bytes hash to {dead[0]}, "
                f"a digest whose bytes were destroyed and are unrecoverable. "
                f"Bytes cannot come back. Either the file has been fabricated to "
                f"match a dead pin or this instrument's record is wrong; either "
                f"way nothing here may be trusted. {dead[1]}")
            continue
        if actual != expected:
            notices.append(
                f"RT26-PIN-ADVANCED {name}: recorded {expected[:16]}..., live "
                f"{actual[:16]}.... NOT A FINDING. The artifact classifies this "
                f"input CITED-DIGEST-RECORDED-NOT-GATED"
                + ("" if name not in DECLARED_UNSTABLE_FALLBACK else
                   " and names it at $.recordedInputs."
                   "citedDigestsThatMovedDuringAuthoring as a file under "
                   "concurrent edit")
                + ". This run therefore re-extracts what it depends on from the "
                  "LIVE bytes rather than refusing, per section 7.10. A pinned "
                  "input that ADVANCED costs a re-read; it does not cost a "
                  "successor instrument."
                + ("" if name in DECLARED_UNSTABLE_FALLBACK else
                   " NOTE: this file is NOT among the four the artifact declares "
                   "unstable, so the advance is unexpected and deserves a look."))

    if errors:
        raise PinRefused(" | ".join(errors))
    return snaps, notices


# ===========================================================================
# SECTION 1 -- REFERENCE DERIVATIONS.
#
# Re-implemented here from the artifact's own published text, never imported
# from it and never read out of it: an instrument that reads its answers out of
# the artifact it is checking measures nothing.  Each accepted reading is paired
# with the REJECTED reading the artifact names, so every negative control has an
# input that is WRONG rather than merely EMPTY (section 7.8's repair).
# ===========================================================================

CAPABILITY_RANK = {"recorded": 0, "verifiable": 1, "replayable": 2}
AVAIL_STATES = ("AVAILABLE", "OUTAGE", "MISSING-DEPENDENCY", "PURGED")

CAUSE_PARTITION = ("RETENTION_AGE_BOUND", "RETENTION_SIZE_BOUND",
                   "RETENTION_COUNT_BOUND", "RETENTION_USER_REQUEST")
# $.partC_retentionBounds.causeVocabulary.closedPartitions[0]
#   .attributionRuleWhenSeveralDemandsCover.rule -- "ties break in the fixed
# order RETENTION_AGE_BOUND, RETENTION_SIZE_BOUND, RETENTION_COUNT_BOUND".
# PC-V-03 is a 4-4 tie between the size and count demands and resolves to SIZE
# ONLY because that order is stated.  check_cause_rule below re-derives the order
# from the artifact's own sentence and compares it to this tuple, so reversing
# the published rule is caught rather than ignored.
CAUSE_TIEBREAK = ("RETENTION_AGE_BOUND", "RETENTION_SIZE_BOUND",
                  "RETENTION_COUNT_BOUND")
DIMENSION_CAUSE = {"time": "RETENTION_AGE_BOUND", "size": "RETENTION_SIZE_BOUND",
                   "count": "RETENTION_COUNT_BOUND"}

POSTURE_ENUM = ("DURABLE_RETAINED", "EPHEMERAL_ONLY")
POSTURE_PROVENANCE_ENUM = ("CONSENTED", "DEFAULTED")
BOUNDS_PROVENANCE_ENUM = ("CONFIGURED", "DEFAULTED")
ABSENT = "ABSENT"

# The shipping product's values, recorded so PC-V-12's rejected reading can be
# executed rather than described.
PRODUCT_KEEP = 200
PRODUCT_MAX_AGE_SECONDS = 60 * 24 * 60 * 60          # 5184000
PRODUCT_MAX_TOTAL_BYTES = 150 * 1024 * 1024

BOUNDS_ORDERED_FIELDS = ("schemaVersion", "projectId", "retentionPolicyId",
                         "maxAgeSeconds", "maxTotalBytes", "keepCount",
                         "boundsRevision", "retentionBoundsId")
BOUNDS_CLOSED_INTS = ("maxAgeSeconds", "maxTotalBytes", "keepCount",
                      "boundsRevision", "schemaVersion")


# --- The Cap domain.  Cap := u64 | UNBOUNDED, totally ordered by <=, with
# --- UNBOUNDED strictly greater than every u64.  EXACTLY TWO arithmetic
# --- extensions follow from that order and they are the only ones implemented:
# ---   (n - UNBOUNDED) is strictly less than 0 for every u64 n
# ---   (now - UNBOUNDED) is strictly less than every representable admission time
# --- The size dimension needs NO extension at all: k = 0 already satisfies
# --- total_bytes <= UNBOUNDED by the ORDER ALONE.  There is no third extension
# --- and inv_c15 measures that there is none.

class _Unbounded:
    __slots__ = ()

    def __repr__(self):
        return "UNBOUNDED"


class _BelowZero:
    """The value of (u64 - UNBOUNDED).  Not an int, deliberately: making it -1
    would let an arithmetic slip read as an ordinary quantity.  max0() is the
    only thing that consumes it."""
    __slots__ = ()

    def __repr__(self):
        return "BELOW-ZERO"


class _BeforeAllTimes:
    """The value of (now - UNBOUNDED).  Strictly less than every representable
    admission time, so no member is strictly older than it."""
    __slots__ = ()

    def __repr__(self):
        return "BEFORE-ALL-TIMES"


UNBOUNDED = _Unbounded()
BELOW_ZERO = _BelowZero()
BEFORE_ALL_TIMES = _BeforeAllTimes()


def unbounded_if_zero(configured):
    """$.partC_retentionBounds.sweep.demands.theDisableConvention.rule --
    `unbounded_if_zero(v) := UNBOUNDED if v == 0 else v`.  ONE total lift,
    applied identically to all three configured values, before any demand is
    computed.  Exact-type: a bool is not a u64 (law 18), so it is refused here
    rather than silently lifted."""
    if isinstance(configured, bool) or not isinstance(configured, int):
        raise RefusedError(f"unbounded_if_zero: not a u64: {configured!r}")
    if configured < 0:
        raise RefusedError(f"unbounded_if_zero: negative: {configured!r}")
    return UNBOUNDED if configured == 0 else configured


def cap_le(value: int, cap) -> bool:
    """The Cap order.  Every u64 is <= UNBOUNDED."""
    return True if cap is UNBOUNDED else value <= cap


def sub_cap(n: int, cap):
    """Extension 1.  (n - UNBOUNDED) is strictly less than 0."""
    return BELOW_ZERO if cap is UNBOUNDED else n - cap


def sub_time(now: int, cap):
    """Extension 2.  (now - UNBOUNDED) is below every representable time."""
    return BEFORE_ALL_TIMES if cap is UNBOUNDED else now - cap


def max0(value):
    if value is BELOW_ZERO:
        return 0
    return value if value > 0 else 0


def strictly_older(admission_time: int, cutoff) -> bool:
    if cutoff is BEFORE_ALL_TIMES:
        return False
    return admission_time < cutoff


# --- The eviction order.  ONE total order shared by every dimension, which is
# --- what makes every demand a prefix LENGTH and therefore makes independence a
# --- property of the evicted SET and not merely of its size.

def eviction_order(evictable):
    return sorted(evictable, key=lambda m: (m["atSequence"], m["recordCasRef"]))


def order_is_total(evictable) -> bool:
    keys = [(m["atSequence"], m["recordCasRef"]) for m in evictable]
    return len(set(keys)) == len(keys)


def total_bytes(members) -> int:
    return sum(m["bytes"] for m in members)


# --- The three demand expressions, AS PUBLISHED at
# --- $.partC_retentionBounds.sweep.demands.rows[].demand.  No branch, no guard,
# --- no sibling field.  Each is total on Cap and each evaluates to 0 at
# --- UNBOUNDED by its own derivation.

def demand_count(cap_count, order) -> int:
    """demand_count := max(0, len(evictable) - cap_count)"""
    return max0(sub_cap(len(order), cap_count))


def demand_size(cap_size, order, fallback_probe=None) -> int:
    """demand_size := the smallest k in [0, len(evictable)] such that
    total_bytes(evictable[k:]) <= cap_size.

    The predecessor's trailing clause `or len(evictable) if no such k exists`
    is REMOVED and was measured dead: at k = len(evictable) the suffix is empty
    and its total is 0, which is <= every member of Cap.  `fallback_probe` is
    the assertion hook the reachability sweep drives; if the loop ever falls
    through, the probe records it and the sweep reports a live fallback.
    """
    for k in range(len(order) + 1):
        if cap_le(total_bytes(order[k:]), cap_size):
            return k
    if fallback_probe is not None:
        fallback_probe.append(True)
    raise RefusedError("demand_size: the removed fallback clause was reached, "
                       "so it was NOT dead")


def demand_time(cap_age, order, now: int) -> int:
    """demand_time := the number of leading members of the eviction order whose
    admission time is strictly older than cutoff, where cutoff := now - cap_age.
    """
    cutoff = sub_time(now, cap_age)
    n = 0
    for member in order:
        if not strictly_older(member["admissionTime"], cutoff):
            break
        n += 1
    return n


# --- The SAME three demands under the PREDECESSOR'S published expressions:
# --- written over the RAW configured value with the disable behaviour carried
# --- in a sibling scalar named `disabledWhen`, outside the expression.  This is
# --- not a strawman.  retention-tiers.v25 published these rows as executable and
# --- IR-RT25-B1 graded them BLOCKING for exactly this reason.  Implementing both
# --- readings is what makes "7 of 7 agree here, 1 of 7 agreed there" a
# --- measurement rather than a claim.

def demand_count_V25(keep_count: int, order) -> int:
    return max(0, len(order) - keep_count)


def demand_size_V25(max_total_bytes: int, order) -> int:
    for k in range(len(order) + 1):
        if total_bytes(order[k:]) <= max_total_bytes:
            return k
    return len(order)


def demand_time_V25(max_age_seconds: int, order, now: int) -> int:
    cutoff = now - max_age_seconds
    n = 0
    for member in order:
        if not member["admissionTime"] < cutoff:
            break
        n += 1
    return n


def demands(bounds, order, now: int, probe=None):
    max_age, max_bytes, keep = bounds
    cap_age = unbounded_if_zero(max_age)
    cap_size = unbounded_if_zero(max_bytes)
    cap_count = unbounded_if_zero(keep)
    return {"time": demand_time(cap_age, order, now),
            "size": demand_size(cap_size, order, probe),
            "count": demand_count(cap_count, order)}


def demands_V25(bounds, order, now: int):
    max_age, max_bytes, keep = bounds
    return {"time": demand_time_V25(max_age, order, now),
            "size": demand_size_V25(max_bytes, order),
            "count": demand_count_V25(keep, order)}


def eviction_count(bounds, order, now: int, probe=None) -> int:
    """evictionCount := max(demand_count, demand_size, demand_time)"""
    return max(demands(bounds, order, now, probe).values())


def eviction_count_V25(bounds, order, now: int) -> int:
    return max(demands_V25(bounds, order, now).values())


def eviction_count_SUM(bounds, order, now: int) -> int:
    """PC-V-04's rejected reading: demands are summed rather than maxed."""
    return sum(demands(bounds, order, now).values())


def eviction_count_PARASITIC(bounds, order, now: int) -> int:
    """PC-V-02/PC-V-03's rejected reading, and the shipping product's actual
    defect: the size demand is computed INSIDE the count branch, guarded by
    `if keepCount <= 0 or keepCount <= 1: return early`.  A user who disables
    count pruning silently loses size pruning."""
    _, _, keep = bounds
    if keep <= 1:
        return 0
    return max(demands(bounds, order, now).values())


def evicted_set(bounds, order, now: int):
    return order[:eviction_count(bounds, order, now)]


def attribute_causes(bounds, order, now: int):
    """The cause recorded is the one belonging to the LARGEST demand, ties
    breaking in the fixed order AGE, SIZE, COUNT.  Every evicted record is
    covered by the maximum demand, so the set of causes over the evicted set is
    a singleton -- or empty when nothing is evicted."""
    values = demands(bounds, order, now)
    top = max(values.values())
    if top == 0:
        return []
    for cause in CAUSE_TIEBREAK:
        for dimension, name in DIMENSION_CAUSE.items():
            if name == cause and values[dimension] == top:
                return [name]
    raise RefusedError("attribute_causes: no dimension carried the maximum")


def attribute_causes_REVERSED(bounds, order, now: int):
    """The rejected reading for the tiebreak: COUNT ahead of SIZE.  PC-V-03 is
    the row that separates them and it is the only one that does."""
    values = demands(bounds, order, now)
    top = max(values.values())
    if top == 0:
        return []
    for cause in reversed(CAUSE_TIEBREAK):
        for dimension, name in DIMENSION_CAUSE.items():
            if name == cause and values[dimension] == top:
                return [name]
    return []


# --- Bounds admission.  Freeze section 6 law 18 lives here: every closed scalar
# --- is admitted by EXACT JSON type at any depth BEFORE its content is compared.
# --- bool is tested before int throughout, because bool subclasses int.

def _exact_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def admit_bounds(record, trace=None):
    """Returns (admission, errorCode, resolvedRecord).

    REFUSED carries CONFIG.INVALID, a member of the live D9 error-code
    vocabulary; no new code is minted.  An unsatisfiable dimension is REFUSED,
    never silently skipped: DEP-RT25-01 leaves maxAgeSeconds with 0 as its only
    legal value, so a non-zero age bound is refused at admission.
    """
    def fail(why):
        if trace is not None:
            trace.append(why)
        return "REFUSED", "CONFIG.INVALID", None

    if record is ABSENT or record is None:
        return "ABSENT", None, None
    if not isinstance(record, dict):
        return fail("bounds record is not a JSON object")
    for field in BOUNDS_CLOSED_INTS:
        if field not in record:
            continue
        value = record[field]
        if not _exact_int(value):
            return fail(f"{field} is {type(value).__name__}, not a JSON integer")
        if value < 0:
            return fail(f"{field} is negative")
    for field in ("maxAgeSeconds", "maxTotalBytes", "keepCount"):
        if field not in record:
            return fail(f"{field} absent")
    if record.get("boundsRevision", 1) < 1:
        return fail("boundsRevision below its minimum of 1")
    if record["maxAgeSeconds"] != 0:
        return fail("maxAgeSeconds is non-zero while no per-raw-object admission "
                    "time exists (DEP-RT25-01); an unsatisfiable bound is "
                    "REFUSED, never silently skipped")
    for field in record:
        if field not in BOUNDS_ORDERED_FIELDS:
            return fail(f"{field} is outside the closed record shape")
    return "ADMITTED", None, dict(record)


def admit_bounds_SILENT_REVERT(record):
    """PC-V-05's rejected reading: a negative value silently reverts to the
    built-in default rather than being refused."""
    if not isinstance(record, dict):
        return "REFUSED", "CONFIG.INVALID", None
    out = dict(record)
    if isinstance(out.get("keepCount"), int) and out["keepCount"] < 0:
        out["keepCount"] = PRODUCT_KEEP
    return "ADMITTED", None, out


def admit_bounds_COERCING(record):
    """PC-V-06/07/08's rejected reading: a bare equality or ordering test, under
    which True == 1, 200.0 == 200 and int("200") == 200 all hold."""
    if not isinstance(record, dict):
        return "REFUSED", "CONFIG.INVALID", None
    out = dict(record)
    for field in ("maxAgeSeconds", "maxTotalBytes", "keepCount"):
        value = out.get(field)
        try:
            out[field] = int(value)
        except (TypeError, ValueError):
            return "REFUSED", "CONFIG.INVALID", None
    return "ADMITTED", None, out


def admit_bounds_SILENT_SKIP(record):
    """PC-V-09's rejected reading: an unsatisfiable dimension is silently
    skipped instead of refused, so a configured 60-day bound evicts nothing
    forever and nothing says so."""
    if not isinstance(record, dict):
        return "REFUSED", "CONFIG.INVALID", None
    out = dict(record)
    out["maxAgeSeconds"] = 0
    return "ADMITTED", None, out


def effective_bounds(record):
    """effective_bounds(ABSENT) = (0, 0, 0, DEFAULTED).  An absent record and an
    all-zero record agree on every value and differ on provenance."""
    if record is ABSENT or record is None:
        return 0, 0, 0, "DEFAULTED"
    return (record["maxAgeSeconds"], record["maxTotalBytes"],
            record["keepCount"], "CONFIGURED")


def effective_bounds_PRODUCT_DEFAULTS(record):
    """PC-V-12's rejected reading: absent bounds are read as the shipping
    product's values, so a project that configured nothing begins purging on a
    schedule nobody chose."""
    if record is ABSENT or record is None:
        return (PRODUCT_MAX_AGE_SECONDS, PRODUCT_MAX_TOTAL_BYTES, PRODUCT_KEEP,
                "DEFAULTED")
    return (record["maxAgeSeconds"], record["maxTotalBytes"],
            record["keepCount"], "CONFIGURED")


# --- Part D.  The posture resolution, total and pure.

def effective_posture(policy):
    """effective_posture: ProjectRetentionPolicyV1 | ABSENT -> (posture,
    provenance).  Total, never returns ABSENT, reads no clock, reads no other
    project.  EPHEMERAL_ONLY is reachable only with provenance CONSENTED."""
    if policy is ABSENT or policy is None:
        return "DURABLE_RETAINED", "DEFAULTED"
    if not isinstance(policy, dict) or "posture" not in policy:
        raise RefusedError("effective_posture: policy without a posture")
    posture = policy["posture"]
    if not isinstance(posture, str) or posture not in POSTURE_ENUM:
        raise RefusedError(f"effective_posture: posture {posture!r} outside the "
                           f"closed enum")
    return posture, "CONSENTED"


def effective_posture_LEAKING_DEFAULT(policy):
    """The rejected reading behind RT25-D-INV-02: a resolution that can return
    (EPHEMERAL_ONLY, DEFAULTED), which would let the tool refuse a durable
    request on the strength of a posture nobody chose."""
    if policy is ABSENT or policy is None:
        return "EPHEMERAL_ONLY", "DEFAULTED"
    return policy["posture"], "CONSENTED"


def durable_authoritative_outcome(policy) -> str:
    posture, _ = effective_posture(policy)
    return "REFUSE" if posture == "EPHEMERAL_ONLY" else "PROCEED-DURABLE"


def durable_authoritative_outcome_DEMOTING(policy) -> str:
    """PC-V-14's rejected reading: the default removes every retention refusal,
    so a durable request under a recorded EPHEMERAL_ONLY is silently demoted to
    ephemeral while reporting success.  Freeze law 14 forbids exactly this."""
    return "PROCEED-EPHEMERAL-REPORTING-SUCCESS"


def resolve_and_maybe_persist(policy, interaction: str):
    """No code path persists a ProjectRetentionPolicyV1 whose posture came from
    the default, so ABSENT survives on disk until a person answers."""
    posture, provenance = effective_posture(policy)
    if policy is not ABSENT and policy is not None:
        return posture, provenance, policy
    if interaction == "ANSWERED-RETAIN":
        return "DURABLE_RETAINED", "CONSENTED", {"posture": "DURABLE_RETAINED"}
    if interaction == "ANSWERED-EPHEMERAL":
        return "EPHEMERAL_ONLY", "CONSENTED", {"posture": "EPHEMERAL_ONLY"}
    return posture, provenance, ABSENT


def resolve_and_maybe_persist_PERSISTING(policy, interaction: str):
    """PC-V-15's rejected reading: the resolution persists what it resolved, so
    a later ask is suppressed and CONSENTED provenance is manufactured from a
    default."""
    posture, provenance = effective_posture(policy)
    if policy is ABSENT or policy is None:
        return posture, provenance, {"posture": posture}
    return posture, provenance, policy


def ask_performed(profile: str, policy, custody: str, dismissed_before: bool
                  ) -> bool:
    """The ask is performed at exactly one axis: local-interactive, policy
    ABSENT, durable-authoritative.  A dismissal does NOT suppress the next ask,
    because no policy was written by the dismissal."""
    return (profile == "local-interactive"
            and (policy is ABSENT or policy is None)
            and custody == "DURABLE_AUTHORITATIVE")


def ask_performed_SUPPRESSING(profile: str, policy, custody: str,
                              dismissed_before: bool) -> bool:
    """PC-V-16's rejected reading: a dismissal suppresses the next ask, so the
    user is never asked again and the project is retained durably and unboundedly
    forever with provenance DEFAULTED."""
    if dismissed_before:
        return False
    return ask_performed(profile, policy, custody, dismissed_before)


# --- Part B, re-derived from v24's own pinned algorithm text.  Used by PC-V-11
# --- and by RT25-C-INV-01 / -05 / -13.  Cause must NOT reach the derivation.

def fold_ledger(entries):
    state = {}
    for entry in sorted(entries, key=lambda e: e["atSequence"]):
        state[entry["rawKey"]] = entry["toState"]
    return state


def unit_satisfied(unit, states) -> bool:
    return all(states.get(key, "AVAILABLE") == "AVAILABLE"
               for key in unit["requires"])


def effective_capability(sealed: str, units, states) -> str:
    """Derived at read time from availability alone.  cause is NOT an input."""
    best = "recorded"
    for unit in units:
        if unit_satisfied(unit, states):
            candidate = unit["grants"]
            if CAPABILITY_RANK[candidate] > CAPABILITY_RANK[best]:
                best = candidate
    if CAPABILITY_RANK[best] > CAPABILITY_RANK[sealed]:
        return sealed
    return best


def effective_capability_CAUSE_LEAKING(sealed: str, units, states, causes) -> str:
    """PC-V-11's rejected reading: cause reaches the derivation, so a
    user-requested purge and a size-driven purge become different kinds of loss
    at the one place a consumer branches on what it can do."""
    base = effective_capability(sealed, units, states)
    if any(c == "RETENTION_USER_REQUEST" for c in causes):
        return "recorded"
    if base == "recorded" and causes:
        return "verifiable"
    return base


def admit_transition(entry):
    """Every ledger entry with toState PURGED carries exactly one cause drawn
    from the closed four-member partition.  Exact type first: a boolean is not a
    string, a number is not a string, null is not a string."""
    if not isinstance(entry, dict):
        return "REFUSED", "not an object"
    to_state = entry.get("toState")
    if not isinstance(to_state, str) or to_state not in AVAIL_STATES:
        return "REFUSED", "toState outside the closed lattice"
    if to_state != "PURGED":
        return "ADMITTED", None
    if "cause" not in entry:
        return "REFUSED", "a PURGED entry with no cause"
    cause = entry["cause"]
    if isinstance(cause, bool) or not isinstance(cause, str):
        return "REFUSED", f"cause is {type(cause).__name__}, not a JSON string"
    if cause not in CAUSE_PARTITION:
        return "REFUSED", "cause outside the closed four-member partition"
    return "ADMITTED", None


def over_bound(footprint: int, max_total_bytes: int, evictable) -> bool:
    """DERIVED, NOT RECORDED.  Both operands are already readable."""
    return footprint > max_total_bytes and not evictable


def admit_write(_bounds, _footprint, _evictable) -> str:
    """A bound is a purge TRIGGER, not an admission GATE.  No configured bound
    and no unsatisfiable bound can refuse a write."""
    return "ADMITTED"


def admit_write_THROWING(bounds, footprint, evictable) -> str:
    """PC-V-10's rejected reading, and the shipping graph-snapshot store's actual
    behaviour: the store throws and refuses the write when a bound cannot be
    satisfied, converting a policy failure into a host error -- freeze law 14's
    third clause named exactly."""
    _, max_bytes, _ = bounds
    if max_bytes and footprint > max_bytes and not evictable:
        return "REFUSED"
    return "ADMITTED"


def retention_sweep(bounds, evictable, now: int):
    """Emits ONLY AvailabilityTransitionV1 entries with toState PURGED, so it
    can never raise effectiveCapability."""
    order = eviction_order(evictable)
    count = eviction_count(bounds, order, now)
    causes = attribute_causes(bounds, order, now)
    cause = causes[0] if causes else None
    return [{"rawKey": m["recordCasRef"], "toState": "PURGED", "cause": cause,
             "atSequence": m["atSequence"]} for m in order[:count]]


# --- The identity recipes.  These are the ONLY values in the artifact computed
# --- by running code, so they are the one place an executed claim can be
# --- falsified.  The encoder is required to reproduce a golden it did not
# --- author BEFORE any new value is computed -- v24's two published rpol1
# --- identities -- exactly as the artifact's own encoderControl does.

def _frame(tag: int, text: str) -> bytes:
    raw = unicodedata.normalize("NFC", text).encode("utf-8")
    return bytes([tag]) + len(raw).to_bytes(4, "big") + raw


def _fixed(tag: int, value: int) -> bytes:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RefusedError(f"u64be frame of a non-u64: {value!r}")
    return bytes([tag]) + (8).to_bytes(4, "big") + value.to_bytes(8, "big")


def retention_policy_id(project_id: str, posture: str, consent_ref: str):
    preimage = (b"opensip.project-retention-policy.v1" + b"\x00"
                + (1).to_bytes(2, "big") + (3).to_bytes(2, "big")
                + _frame(0x01, project_id) + _frame(0x02, posture)
                + _frame(0x03, consent_ref))
    return len(preimage), "rpol1:sha256:" + sha_bytes(preimage)


def retention_bounds_id(project_id: str, policy_id: str, max_age: int,
                        max_bytes: int, keep: int, revision: int):
    preimage = (b"opensip.project-retention-bounds.v1" + b"\x00"
                + (1).to_bytes(2, "big") + (6).to_bytes(2, "big")
                + _frame(0x01, project_id) + _frame(0x02, policy_id)
                + _fixed(0x03, max_age) + _fixed(0x04, max_bytes)
                + _fixed(0x05, keep) + _fixed(0x06, revision))
    return len(preimage), "rbnd1:sha256:" + sha_bytes(preimage)


def retention_bounds_id_OVER_CAPS(project_id: str, policy_id: str, max_age: int,
                                  max_bytes: int, keep: int, revision: int):
    """PC-V-20's rejected reading: the identity preimage frames the LIFTED CAPS
    rather than the configured values.  UNBOUNDED has no u64be encoding, so the
    preimage is unconstructible for every project that disables any dimension --
    and any implementation that substituted a value to make it constructible
    would give two different configurations the same identity, or one
    configuration two identities.  This function must RAISE, and PC-V-20 requires
    it to."""
    caps = [unbounded_if_zero(max_age), unbounded_if_zero(max_bytes),
            unbounded_if_zero(keep)]
    for cap in caps:
        if cap is UNBOUNDED:
            raise RefusedError(
                "RETENTION-BOUNDS-ID-V1 over lifted caps: UNBOUNDED has no u64be "
                "encoding, so the preimage is unconstructible")
    return retention_bounds_id(project_id, policy_id, caps[0], caps[1], caps[2],
                               revision)


# ===========================================================================
# SECTION 2 -- THE DOCUMENT WALK, THE CENSUS, THE TYPE REGISTRY AND THE SWEEP.
# ===========================================================================

_STEP = re.compile(r"\[\d+\]$")
_SEG = re.compile(r"([^\[\].]*)((?:\[\d+\])*)")


def _walk_path_keys(path: str):
    keys = []
    for raw in path.lstrip("$").lstrip(".").split("."):
        if not raw:
            continue
        match = _SEG.match(raw)
        name, indices = match.group(1), match.group(2)
        if name:
            keys.append(name)
        for index in re.findall(r"\[(\d+)\]", indices):
            keys.append(int(index))
    return keys


def get_path(doc, path: str, default=None):
    node = doc
    for key in _walk_path_keys(path):
        if isinstance(key, int):
            if not isinstance(node, list) or key >= len(node):
                return default
            node = node[key]
        else:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
    return node


def set_path(doc, path: str, value) -> None:
    keys = _walk_path_keys(path)
    node = doc
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = value


def del_path(doc, path: str) -> None:
    keys = _walk_path_keys(path)
    node = doc
    for key in keys[:-1]:
        node = node[key]
    del node[keys[-1]]


def scalar_leaves(node, path: str = "$"):
    out = []
    if isinstance(node, dict):
        for key, value in node.items():
            out.extend(scalar_leaves(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out.extend(scalar_leaves(value, f"{path}[{index}]"))
    else:
        out.append((path, node))
    return out


def all_keys(node, path: str = "$"):
    out = []
    if isinstance(node, dict):
        for key, value in node.items():
            out.append((f"{path}.{key}", value))
            out.extend(all_keys(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out.extend(all_keys(value, f"{path}[{index}]"))
    return out


def leaf_name(path: str) -> str:
    return _STEP.sub("", path).split(".")[-1]


def census(doc):
    """Re-walked from the parsed bytes.  bool is tested BEFORE int, because in
    Python bool subclasses int and testing int first silently classifies every
    boolean as an integer -- the same exact-type class law 18 exists to prevent,
    applied to the census instrument itself.  The int-first control is computed
    alongside and published, so the ordering bug is visible if reintroduced."""
    counts = {"int": 0, "bool": 0, "float": 0, "null": 0, "str": 0}
    control = {"intFirstInt": 0, "intFirstBool": 0}
    floats = []
    nulls = []
    for path, value in scalar_leaves(doc):
        if isinstance(value, bool):
            counts["bool"] += 1
        elif isinstance(value, int):
            counts["int"] += 1
        elif isinstance(value, float):
            counts["float"] += 1
            floats.append(path)
        elif value is None:
            counts["null"] += 1
            nulls.append(path)
        elif isinstance(value, str):
            counts["str"] += 1
        else:
            raise RefusedError(f"leaf {path} is not a JSON scalar")
        # the WRONG order, run deliberately as a control
        if isinstance(value, int):
            control["intFirstInt"] += 1
        elif isinstance(value, bool):
            control["intFirstBool"] += 1
    counts["scalar"] = sum(counts[k] for k in ("int", "bool", "float", "null",
                                               "str"))
    counts["nonString"] = counts["scalar"] - counts["str"]
    return {"counts": counts, "control": control, "floatLeafPaths": sorted(floats),
            "nullLeafPaths": sorted(nulls)}


# The three deliberate law-18 controls, keyed POSITIONALLY by vector id rather
# than by index, so reordering the rows does not silently move the guard.
CONTROL_VECTOR_TYPES = {
    "PC-V-06-EXACT-TYPE-BOOL": bool,
    "PC-V-07-EXACT-TYPE-FLOAT": float,
    "PC-V-08-EXACT-TYPE-NUMERIC-STRING": str,
}

# Transcribed ONCE from these bytes and frozen as literals.  A registry sized
# from the artifact cannot police that artifact (section 7.2.2's corollary), so
# this must never be recomputed from the data under check.  A new int/bool leaf
# under a name in neither set is UNRULED, and unruled must be 0.  The honest
# limit is stated in --limits: a name wrongly classified HERE is a wrong rule
# applied consistently, and `unruled == 0` cannot see it.
INT_LEAF_NAMES = frozenset({
    "AGE", "COUNT", "SIZE", "adoptionsRestingOnlyOnProductEvidence",
    "adoptionsWithAnIndependentCorpusJustification", "applicationsOfThisFile",
    "architecturalRecommendationsOverridden",
    "arithmeticVectorsAgreeingUnderV25sPublishedExpressions",
    "arithmeticVectorsTotal", "askCells", "askPerformedCellCountAfter",
    "askPerformedCellCountBefore", "askingCells", "availabilityStatesAfter",
    "availabilityStatesBefore", "biconditionalDeviationsMeasured",
    "blockersRepaired", "blockersRepairedAndInstrumented", "boolLeafPositions",
    "boundsRevision", "branchesInsideAnExpression", "case",
    "causeAttributionsAgreeing", "causeComparisonsReRunHere", "cellCount",
    "cellsFoundChanged", "cellsSelectedByTheRule",
    "cellsWithAtLeastOneChangedFieldValue", "cellsWithNoChangedFieldValue",
    "censusWalksPerformed", "changedKeyCount", "chars",
    "codesAddedByThisArtifact", "conflictsClearedByThisFilesExistence",
    "correctedByThisArtifact", "count", "counterexampleFixturesRun",
    "decisionTableCells", "declaredDependencyCount",
    "deduplicationCasesConsidered", "deficiencyMemberCount",
    "deficiencyMembersAddedByThisArtifact", "deficiencyMembersMatchingPredicate",
    "derivationsExecutedByThisArtifact", "derivationsPublished",
    "derivedExitCode", "deviationCount", "digestsRecordedCount",
    "dimensionCount", "dimensionsLifted", "dimensionsWithTheirOwnDisableRule",
    "duplicateKeysFound", "effectiveCapabilityForbiddenInputsAfter",
    "effectiveCapabilityForbiddenInputsBefore", "effectiveCapabilityInputsAfter",
    "effectiveCapabilityInputsBefore", "errorCodeCount",
    "errorCodesAddedByThisArtifact", "errorCodesMatchingPredicate",
    "evictableCount", "evictableSetSizeInThatEvaluation", "evictableTotalBytes",
    "evictionCountAtTheDefaultUnderV25sPublishedExpressions",
    "exceptionsDiscoveredByInspection", "exhaustiveDerivationsReRunHere",
    "exitCode", "exitWithThisFile", "exitWithoutThisFile",
    "expectedEvictionCount", "expectedPreimageByteLength",
    "expressionsTotalOnCap", "extensionsRequired", "fieldCount", "fieldsAdded",
    "fieldsChangedCount", "fieldsPartitionedByAxis", "fieldsRemoved",
    "fieldsReordered", "filesCreated", "filesEdited",
    "filesWrittenByThisArtifact", "findingsReported",
    "firstRunDisclosureEmittedCellCountAfter",
    "firstRunDisclosureEmittedCellCountBefore", "fixedPointIterations",
    "floatLeafPositions", "footprintModelsSpecified", "frozenArtifactCount",
    "goldensAttempted", "goldensReproduced", "guardsOutsideAnExpression",
    "guardsOutsideAnyExpression", "howManyOfTheFourAreFullyResolvedHere",
    "howManyReasonCodesAreRequested", "howManyRemainUndecided",
    "identityRecipeVersionAfter", "identityRecipeVersionBefore",
    "independentReviewsOfTheseBytes", "independentReviewsOfThisArtifact",
    "index", "inputsActuallyGated", "instrumentSays",
    "instrumentsPerformingItPerRun", "instrumentsTested",
    "instrumentsWhoseResultChanges", "intLeafPositions",
    "intentClausesNowConstituted", "intentClausesRecorded",
    "interactionOutcomes", "invariantCount", "invariantsDeclared",
    "invariantsMechanicallyChecked", "item", "keepCount", "keysInNeitherList",
    "ledgerEntryOrderedFieldsAfter", "ledgerEntryOrderedFieldsBefore",
    "ledgerEntryTypesAfter", "ledgerEntryTypesBefore", "ledgerRowsTouched",
    "maxAgeSeconds", "maxTotalBytes", "measuredNonAskingCells",
    "mechanismsInThisCorpusThatCouldVerifyAuthorialIntent", "memberCount",
    "mutationArmsRun", "mutationSweepsRun", "n", "negativeControlCount",
    "newAvailabilityStates", "newAvailabilityStatesIntroduced",
    "newLedgerEntries", "newLedgerMutationsIntroduced", "newRecordTypes",
    "newRecordTypesIntroduced", "newResidualCount", "noAskCaseCount",
    "noAskCasesReDerivedCount", "noAskCasesSilentlyDeleted", "nonAskingCells",
    "nonBlockingObservationsDispositioned", "nonControlRowCount",
    "nonStringLeafPositions", "notFoundInTheirAttributedSource",
    "nullLeafPositions", "operationCount", "orderedFieldsAfter",
    "orderedFieldsBefore", "orderedPosition", "outcomesAffected",
    "outcomesChanged", "outcomesFoundChanged", "outcomesNeedingRecomputation",
    "outcomesRecomputed", "outcomesResolvedStructurally",
    "outcomesStillNeedingAnExecutedDerivation", "outcomesUnchanged",
    "partABlockingFindingCount", "partAKeyCount",
    "partASurfacesSearchedByInstrument", "partBBlockingFindingCount",
    "partBKeyCount", "partBSurfacesLeftUnchanged",
    "partBSurfacesProposedForChange", "partBSurfacesTouchedByThePostureDecision",
    "policyPersistingOutcomesUnchanged", "postureEnumMembersAdded",
    "postureEnumMembersAfter", "postureEnumMembersBefore",
    "predecessorHardPinnedInputs", "predecessorMutationArmsRun",
    "predecessorRetainedCheckers", "preimageByteLength",
    "productClaimsReMeasuredHere", "productClaimsRecorded",
    "productPacketAmendmentsMadeByThisArtifact", "purgeDoesNotMutateAfter",
    "purgeDoesNotMutateBefore", "purgeMutatesExactlyAfter",
    "purgeMutatesExactlyBefore", "quotedFieldsReVerified",
    "quotedFieldsThatDrifted", "randomisedTrialsReRunHere",
    "realObjectsMeasured", "reasonCodeCount", "reasonCodesMatchingPredicate",
    "recipeVersion", "recomputationsPerformedAtAuthoring", "recordedInputs",
    "recordsAddedToTheSurface", "refusingCells",
    "refusingCellsBecauseThePolicySaysNo", "refusingCellsForWantOfAPolicy",
    "resolutionRulesAddedToTheSurface", "resultUnderRejectedReading",
    "retainedCheckers", "retainedResidualCount",
    "retainedResidualsWhoseBasisMovedCount", "reviewedRecordShapesEdited",
    "reviewsOfThisFile", "rowCount", "rowsAddedByThisArtifact",
    "rowsAgreeingUnderThePredecessorsPublishedExpressions",
    "rowsAgreeingUnderThesePublishedExpressions", "rowsAssignedFromTheConvention",
    "rowsExecuted", "rowsMeasured", "rowsResolvedThisWayCount",
    "rowsStillOwingAnExecutedDerivationCount", "rowsWithAnAxesObject",
    "rowsWithAnExecutedD9Derivation", "rowsWithNullAxes", "scalarLeafPositions",
    "selectedCellIndices", "siblingDisableFields", "sitesCorrected",
    "sitesRewritten", "size", "sourceCount", "stringLeafPositions",
    "structuralArgumentsOffered", "surfacesChangedCount",
    "surfacesExplicitlyUnchangedCount", "terminalStatesAfter",
    "terminalStatesBefore", "theIndependentReviewEnumerates",
    "thisArtifactMeasures", "time", "totalBlockingFindingCount", "totalKeyCount",
    "typedRefusalKindsAfter", "typedRefusalKindsBefore", "unchangedKeyCount",
    "underThePredecessorsPublishedExpressions", "underThesePublishedExpressions",
    "unsetFieldsTouched", "unverifiedButFoundElsewhereInTheCorpus",
    "v24OwnResidualSays", "v24RowsTheBiconditionalWasMeasuredOver",
    "v24SentinelSays", "v25RowsCarryingATripleItsOwnTextSaysIsWrong",
    "v25RowsWithNoDeclaredAxes",
    "v26RowsCarryingATripleThisArtifactSaysIsWrong", "v26RowsWithNoDeclaredAxes",
    "valueAtUNBOUNDED", "vectorsDeclared", "vectorsExecuted",
    "verbatimFieldsInTheseBytes", "verifiedAgainstTheirAttributedSource",
    "verifiedPropertiesTouched", "version",
})

BOOL_LEAF_NAMES = frozenset({
    "aPurgedEntryWithACauseOutsideThePartitionIsRefused",
    "aPurgedEntryWithNoCauseIsRefused", "aReviewerMayDisagree",
    "absenceIsADistinctState", "absenceStateNameRetained",
    "absentAndAllZeroAgreeOnValuesAndDifferOnProvenance", "agree",
    "agreedInThePredecessor", "agreesHere", "agreesWithTheShippingProduct",
    "allFourStillPersistNoPolicy", "answeredHere", "appendsToTheExistingLedger",
    "appliedByThisArtifact", "appliedIdenticallyToEveryDimension",
    "askPerformed", "askStillPerformed", "atMostOnePerProject", "bindsNothing",
    "boundsRecordPresent", "butTheClaimItCarriedIsWithdrawn",
    "bytesAreReclaimedFromObjectsNeverFromTheLedger", "callersCannotSupplyIt",
    "canItHaveBounds", "carriedForwardUnchanged", "cellCountUnchanged",
    "censusIncludesItsOwnIntegers", "changesAnyOtherArtifact",
    "changesAnyStatus", "citesAConstitutedProductDecision", "claimSplit",
    "closed", "closedByThisArtifact", "codeAlreadyExistsInTheLiveVocabulary",
    "complete", "compositionIsUnchangedFromThePredecessor",
    "constitutedInTheBindingPacket", "constitutesASealOrSignature",
    "containsNoBranch", "countUnchanged", "derivedAndEnumerated",
    "derivedNotEnumerated", "durableSourceDerivedWritePermitted",
    "emitsNoOtherToState", "everyChangedFieldIsPostureSensitiveInV24",
    "everyFloatIsDeliberate", "everyNullIsDeliberate",
    "everyPurgedEntryCarriesACause", "exactlyOneCausePerEntry", "executed",
    "executionIdAllocatedAtThisPoint",
    "executionIdAllocatedWhileTheQuestionIsOpen", "expectedEqual",
    "expectedFirstRunAskPerformed", "expectedOverBound",
    "expectedPolicyPersisted", "expectedSecondRunAskPerformed", "fieldIsNotNew",
    "firstRunDisclosureEmitted", "fixedPointReached",
    "fromUnderRetentionToUnconsentedRetention", "global", "hasACauseMember",
    "hasNoDefaultField", "holds", "holdsOverEveryRow",
    "identityIsOverConfiguredValuesNotCaps", "introducesNoNewMutation",
    "isATriggerNotAGate", "isAlgebraicallyMonotone", "isAnAnswer",
    "isComputedOverConfiguredValuesNotLiftedCaps",
    "isDerivedFromEffectivePosture", "isDerivedFromTheTable",
    "isDerivedNotPreferred", "isDeterministic", "isItAlreadyTrue",
    "isItReachableUnderTheNewDefault", "isNegativeControl", "isOpen", "isPure",
    "isTerminatingAfter", "isTheRiskiestPartOfThisChange", "isThisANewReason",
    "isThisANewRule", "isTotal", "isTotalOnCap", "mayAmendD9Vocabulary",
    "mayAmendOperabilityGates", "mayAmendTheProductDispositionPacket",
    "mayAmendThreatModel", "mayApplyTheCdRt5AmendmentDraft",
    "mayCiteAProductDecision", "mayConstituteAProductDecision",
    "measuredPresent", "mentionsAnyOtherDimensionsValue",
    "negativeOrNonIntegerIsRefusedNotDefaulted", "neitherIsAdoptedUnchanged",
    "neverReturnsAbsent", "newInThisArtifact", "noBoundCanShrinkIt",
    "noInputWasWritten", "noPostureEnumMemberIsAdded", "noSentinelIsAdmitted",
    "notAResolvedConfigurationLayer", "notInTheWorktree", "notSilentlySkipped",
    "notUnderTheAnalysisSnapshotRoot", "onlyThenWereTheBoundsValuesComputed",
    "outageIsNeverEvictable", "partAPrimeDependsOnPartD", "partCDependsOnPartD",
    "perProject", "planDigestConfirmedUnchanged", "policyPersisted",
    "policyPersistedByThisCell", "policyPersistedOnlyByTheAnswer",
    "policyPersistingOutcomeCountUnchanged", "policyPresent",
    "positionUnchanged", "postureEnumIsClosed", "predecessorIsNotEdited",
    "predecessorValue", "predecessorVerdictStillApplies",
    "protectedSetIsNotEvictableByAnyBound", "provenanceEnumIsClosed",
    "provenanceIsNeverPersisted", "quotedNotParaphrased",
    "reDerivedIndependently", "reMeasuredHere",
    "reParsedWithDuplicateKeyRejectingHook", "reRunByThisArtifact",
    "readsNoClock", "readsNoOtherBoundsValue", "readsNoOtherProject",
    "refusalStillReachableInCi", "reproducedHere", "requiresNoNewTrials",
    "restatedByThisArtifact", "restatedNotDeleted",
    "reversibilityIsAFeatureOfTheDesignNotAPredictionAboutTheProduct",
    "sameOrderForEveryDimension", "satisfiableToday",
    "silentDemotionIsStillForbidden", "soAbsenceIsNeverUnexplained",
    "soIsThereACellWithOutcomePROCEEDDURABLEAndTheWriteFlagFalse",
    "soNoBoundEverFiresUntilSomeoneConfiguresOne",
    "soTheAskIsStillStrictlyBeforeAttemptAdmission",
    "soTheDefaultConfigurationNeverPurges", "soTheExceptionsAreDerived",
    "statedAgainstThisArtifactsOwnInterest", "substanceUnaffected",
    "successorValue", "terminatesAfter", "terminatesBefore",
    "terminatesTheRequest",
    "theDefaultDesignedAgainstIsAConstitutedPacketValue",
    "theDefaultIsNeverWrittenToDisk", "theLedgerGrowsWithoutBound",
    "thePredecessorsRuleIsWithdrawn", "theProofIsAboutThePublishedExpressions",
    "theRiskDirectionHasReversed", "theTwoHalvesOfThatAnswerAreDifferent",
    "thisIsTheProductIntentDelivered", "unchanged",
    "unchangedFromThePredecessor", "valueUnchanged",
    "verifiedAgainstThatSource", "wasTerminating", "zeroDisables",
    "zeroIsLiftedNotBranchedOn",
})


def _control_paths(doc):
    """The three law-18 control payload paths, located by VECTOR ID."""
    paths = {}
    rows = get_path(doc, "$.partC_retentionBounds.vectors.rows") or []
    for index, row in enumerate(rows):
        if isinstance(row, dict) and row.get("id") in CONTROL_VECTOR_TYPES:
            paths[f"$.partC_retentionBounds.vectors.rows[{index}].bounds."
                  f"keepCount"] = (row["id"], CONTROL_VECTOR_TYPES[row["id"]])
    return paths


def type_findings(doc):
    """The exact-type rule over the artifact's own leaves, at any depth.

    Every int/bool leaf must match the type its NAME declares, except the three
    deliberate law-18 controls, which are keyed by VECTOR ID and whose spellings
    are REQUIRED to stay bool / float / string -- a control spelled as an integer
    is not a control.  An int/bool leaf whose name is in neither registry is
    UNRULED, and unruled must be 0.
    """
    findings = []
    counts = {"scalarLeafPositions": 0, "intLeafPositions": 0,
              "boolLeafPositions": 0, "floatLeafPositions": 0,
              "nullLeafPositions": 0, "stringLeafPositions": 0,
              "guardedIntOrBoolLeafPositions": 0,
              "unruledIntOrBoolLeafPositions": 0}
    controls = _control_paths(doc)
    declared_nulls = set(get_path(doc, "$.leafCensus.nullLeafPaths") or [])
    for path, value in scalar_leaves(doc):
        counts["scalarLeafPositions"] += 1
        if isinstance(value, bool):
            counts["boolLeafPositions"] += 1
        elif isinstance(value, int):
            counts["intLeafPositions"] += 1
        elif isinstance(value, float):
            counts["floatLeafPositions"] += 1
        elif value is None:
            counts["nullLeafPositions"] += 1
        else:
            counts["stringLeafPositions"] += 1

        if path in controls:
            vid, required = controls[path]
            counts["guardedIntOrBoolLeafPositions"] += 1
            ok = (isinstance(value, bool) if required is bool
                  else (not isinstance(value, bool)) and isinstance(value, required))
            if not ok:
                findings.append(
                    f"RT26-TYPE {path}: {vid}'s payload MUST stay a JSON "
                    f"{required.__name__}; a control respelled as another type is "
                    f"not a control. got {type(value).__name__}")
            continue

        if value is None:
            if path not in declared_nulls:
                findings.append(
                    f"RT26-TYPE {path}: null leaf outside the six declared "
                    f"d9Axes nulls at $.leafCensus.nullLeafPaths")
            continue
        if isinstance(value, float):
            findings.append(
                f"RT26-TYPE {path}: float leaf outside the single declared "
                f"law-18 float control (PC-V-07-EXACT-TYPE-FLOAT)")
            continue
        if isinstance(value, (bool, int)):
            name = leaf_name(path)
            if name in BOOL_LEAF_NAMES:
                counts["guardedIntOrBoolLeafPositions"] += 1
                if not isinstance(value, bool):
                    findings.append(
                        f"RT26-TYPE {path}: {name!r} is a declarative flag and "
                        f"must be a JSON boolean; got {type(value).__name__} "
                        f"{value!r}")
            elif name in INT_LEAF_NAMES:
                counts["guardedIntOrBoolLeafPositions"] += 1
                if isinstance(value, bool):
                    findings.append(
                        f"RT26-TYPE {path}: {name!r} is a counted integer and "
                        f"must not be a JSON boolean (bool subclasses int in "
                        f"Python, which is why this is tested first)")
            else:
                counts["unruledIntOrBoolLeafPositions"] += 1
                findings.append(
                    f"RT26-TYPE {path}: int/bool leaf under UNRULED name "
                    f"{name!r}; the type registry is a frozen literal and must "
                    f"cover every position, so an unruled leaf is an uncovered "
                    f"position")
    return findings, counts


def hostile_sweep(doc, base_findings):
    """Respell every int/bool leaf three ways and require each to be rejected.

    Section 7's dominant failure mode is a coverage claim quantifying over a
    region the instrument cannot observe.  So every position is enumerated and
    injected and the counts are recomputed on every run.  Mutation is in place
    and restored, not by deep copy: the sweep is ~2400 evaluations and a copy per
    position is the difference between seconds and minutes.
    """
    positions = [(p, v) for p, v in scalar_leaves(doc)
                 if isinstance(v, bool)
                 or (isinstance(v, int) and not isinstance(v, bool))]
    arms = {
        "float": lambda v: None if isinstance(v, bool) else float(v),
        "boolFromZeroOrOneInt": lambda v: (
            bool(v) if not isinstance(v, bool) and v in (0, 1) else None),
        "intFromBool": lambda v: (1 if v else 0) if isinstance(v, bool) else None,
    }
    base = set(base_findings)
    result = {}
    for arm, spell in arms.items():
        swept = admitted = by_position = collateral = 0
        escapes = []
        for path, value in positions:
            replacement = spell(value)
            if replacement is None:
                continue
            swept += 1
            set_path(doc, path, replacement)
            try:
                findings, _ = type_findings(doc)
            finally:
                set_path(doc, path, value)
            new = [f for f in findings if f not in base]
            if not new:
                admitted += 1
                escapes.append(path)
            elif any(path in f for f in new):
                by_position += 1
            else:
                collateral += 1
                escapes.append(path + " (collateral)")
        result[arm] = {"sweptPositions": swept, "admitted": admitted,
                       "rejectedByPosition": by_position,
                       "rejectedCollateral": collateral, "escapes": escapes[:20]}
    result["scalarLeafPositions"] = len(scalar_leaves(doc))
    result["intOrBoolLeafPositions"] = len(positions)
    result["respellingsAttempted"] = sum(
        row["sweptPositions"] for row in result.values() if isinstance(row, dict))
    result["respellingsAdmitted"] = sum(
        row["admitted"] for row in result.values() if isinstance(row, dict))
    return result


# ===========================================================================
# SECTION 3 -- VECTOR EXECUTION.  All 20 rows of
# $.partC_retentionBounds.vectors.rows, every one driven, every one able to fail.
#
# Section 7.8's repair, applied row by row: where a row is a negative control it
# NAMES a rejected reading, and this section EXECUTES that reading and requires
# it to produce the DIFFERENT result the row declares.  A control whose rejected
# reading agrees with the accepted one is reported VACUOUS -- an input that is
# merely EMPTY, not WRONG -- rather than counted as a pass.
# ===========================================================================

VECTOR_IDS = (
    "PC-V-01-COUNT-ONLY",
    "PC-V-02-PARASITISM-CONTROL-KEEP-ZERO",
    "PC-V-03-PARASITISM-CONTROL-KEEP-ONE",
    "PC-V-04-INDEPENDENCE-MAX-NOT-SUM",
    "PC-V-05-SILENT-REVERT-CONTROL",
    "PC-V-06-EXACT-TYPE-BOOL",
    "PC-V-07-EXACT-TYPE-FLOAT",
    "PC-V-08-EXACT-TYPE-NUMERIC-STRING",
    "PC-V-09-UNSATISFIABLE-AGE-BOUND",
    "PC-V-10-PROTECTED-SET-EXCEEDS-BOUND",
    "PC-V-11-CAUSE-BLINDNESS-WITHIN-PURGED",
    "PC-V-12-ABSENT-BOUNDS-RESOLVE-TO-UNBOUNDED",
    "PC-V-13-ABSENT-POLICY-RESOLVES-DURABLE",
    "PC-V-14-EPHEMERAL-IS-ALWAYS-CONSENTED",
    "PC-V-15-DEFAULT-IS-NEVER-PERSISTED",
    "PC-V-16-DISMISSAL-DOES-NOT-SUPPRESS-THE-NEXT-ASK",
    "PC-V-17-DEFAULT-CONFIGURATION-EVICTS-NOTHING",
    "PC-V-18-TIME-DIMENSION-AT-ITS-ONLY-LEGAL-VALUE",
    "PC-V-19-BOUNDS-IDENTITY-WORKED-VECTORS",
    "PC-V-20-IDENTITY-IS-OVER-CONFIGURED-VALUES-NOT-LIFTED-CAPS",
)

PROJECT = "prj1-" + "a" * 64
NOW = 1785110400


def population(count: int, total=None, admitted_at=None):
    """A synthetic evictable set.  Equal object size is the reading PC-V-04's own
    note confirms: 'the size demand is 2 and the count demand is 3' holds at
    5 members and 500 bytes only if each object is 100 bytes."""
    if count == 0:
        return []
    each = (total // count) if total else 100
    when = NOW - 1000 if admitted_at is None else admitted_at
    return [{"atSequence": i + 1, "recordCasRef": f"cas-{i:04d}",
             "bytes": each, "admissionTime": when} for i in range(count)]


def _row_bounds(row):
    b = row.get("bounds") or {}
    return (b.get("maxAgeSeconds"), b.get("maxTotalBytes"), b.get("keepCount"))


def _is_arithmetic(row) -> bool:
    """The population predicate, derived rather than listed: a row carrying
    bounds with three non-negative EXACT integers, an evictableCount and an
    expectedEvictionCount.  The artifact's own method sentence claims to have
    executed 'every arithmetic row' and its rowsExecuted is 5; this predicate
    finds 7, which is IR-RT26-N02 mechanised."""
    bounds = _row_bounds(row)
    return (all(_exact_int(v) and v >= 0 for v in bounds)
            and _exact_int(row.get("evictableCount"))
            and _exact_int(row.get("expectedEvictionCount")))


def _arith_rows(doc):
    return [r for r in (get_path(doc, "$.partC_retentionBounds.vectors.rows") or [])
            if isinstance(r, dict) and _is_arithmetic(r)]


def measure_b1(doc):
    """B1's algebra, executed.  Every arithmetic row under BOTH readings, the
    default configuration swept over evictable-set sizes 0..200, the removed
    fallback driven for reachability, the cross-dimension symbol scan, and the
    prefix-inclusion property that makes independence a fact about the evicted
    SET rather than about its size."""
    rows = _arith_rows(doc)
    published_agree, v25_agree, cause_agree = [], [], []
    per_row = {}
    for row in rows:
        bounds = _row_bounds(row)
        order = eviction_order(population(row["evictableCount"],
                                          row.get("evictableTotalBytes")))
        try:
            here = eviction_count(bounds, order, NOW)
            causes = attribute_causes(bounds, order, NOW)
            values = demands(bounds, order, NOW)
        except RefusedError as exc:
            per_row[row["id"]] = {"error": str(exc)}
            continue
        there = eviction_count_V25(bounds, order, NOW)
        expected = row["expectedEvictionCount"]
        if here == expected:
            published_agree.append(row["id"])
        if there == expected:
            v25_agree.append(row["id"])
        # a row that evicts nothing and publishes no expectedCauses expects the
        # empty attribution; the artifact says so in prose ("eviction count is 0,
        # so no cause is attributed") and this derives it rather than skipping
        # the row, which is what makes the denominator 7 and not 6.
        declared_causes = row.get("expectedCauses")
        if declared_causes is None and row["expectedEvictionCount"] == 0:
            declared_causes = []
        if declared_causes is not None and list(causes) == list(declared_causes):
            cause_agree.append(row["id"])
        per_row[row["id"]] = {"expected": expected, "underV26": here,
                              "underV25": there, "demands": values,
                              "causes": causes,
                              "expectedCauses": declared_causes}

    # the default configuration, swept
    default_evictions = {}
    default_evictions_v25 = {}
    for size in range(0, 201):
        order = eviction_order(population(size, size * 100))
        default_evictions[size] = eviction_count((0, 0, 0), order, NOW)
        default_evictions_v25[size] = eviction_count_V25((0, 0, 0), order, NOW)
    default_nonzero = [s for s, v in default_evictions.items() if v != 0]
    default_nonzero_v25 = [s for s, v in default_evictions_v25.items() if v != 0]

    # demand_X(UNBOUNDED) == 0, swept over sizes and byte weights
    unbounded_nonzero = []
    for size in (0, 1, 5, 50, 1000):
        for weight in (0, 1, 7, 10 ** 6, 2 ** 40):
            order = eviction_order(population(size, weight * size or None))
            for dim, value in demands((0, 0, 0), order, NOW).items():
                if value != 0:
                    unbounded_nonzero.append((dim, size, weight, value))

    # the removed fallback: driven, with an assertion at the fallback position
    probe = []
    configurations = 0
    for size in range(0, 60):
        for weight in (0, 1, 7, 999, 10 ** 9):
            order = eviction_order(population(size, weight * size or None))
            for cap in (UNBOUNDED, 0, 1, 5, 10 ** 9):
                configurations += 1
                try:
                    demand_size(cap, order, probe)
                except RefusedError:
                    pass
    fallback_reached = bool(probe)

    # prefix inclusion: independence of the SET, not merely of the count
    inclusion_violations = 0
    set_changes = 0
    configs = 0
    for size in (0, 1, 2, 3, 5):
        order = eviction_order(population(size, size * 100))
        for keep in (0, 1, 2, 3, 5):
            for max_bytes in (0, 100, 200, 300, 500, 600):
                configs += 1
                live = demands((0, max_bytes, keep), order, NOW)
                prefixes = sorted(live.values())
                for shorter, longer in zip(prefixes, prefixes[1:]):
                    if set(range(shorter)) - set(range(longer)):
                        inclusion_violations += 1
                with_size = evicted_set((0, max_bytes, keep), order, NOW)
                without_size = evicted_set((0, 0, keep), order, NOW)
                shared = min(len(with_size), len(without_size))
                if with_size[:shared] != without_size[:shared]:
                    set_changes += 1

    # cross-dimension symbols, measured over the artifact's own expression text
    expressions = {}
    foreign = []
    other_names = {"count": ("cap_size", "cap_age", "maxTotalBytes",
                             "maxAgeSeconds"),
                   "size": ("cap_count", "cap_age", "keepCount",
                            "maxAgeSeconds"),
                   "time": ("cap_count", "cap_size", "keepCount",
                            "maxTotalBytes")}
    for entry in (get_path(doc, "$.partC_retentionBounds.sweep.demands.rows")
                  or []):
        dimension = entry.get("dimension")
        text = str(entry.get("demand", ""))
        expressions[dimension] = text
        for token in other_names.get(dimension, ()):  # noqa: B007
            if token in text:
                foreign.append((dimension, token))

    return {"arithmeticRows": len(rows), "publishedAgree": published_agree,
            "v25Agree": v25_agree, "causeAgree": cause_agree, "perRow": per_row,
            "defaultConfigNonZero": default_nonzero,
            "defaultConfigNonZeroV25": default_nonzero_v25,
            "defaultConfigSizesSwept": len(default_evictions),
            "unboundedNonZero": unbounded_nonzero,
            "fallbackReached": fallback_reached,
            "fallbackConfigurations": configurations,
            "prefixInclusionViolations": inclusion_violations,
            "evictedSetChangedByDisablingASibling": set_changes,
            "prefixConfigurations": configs,
            "crossDimensionSymbols": foreign,
            "expressions": expressions}


def check_b1(doc, ctx):
    """B1's algebra, hard-compared.  IR-RT25-B1 was the strongest finding of the
    predecessor's review and this is the check that would reproduce it."""
    out = []
    b1 = ctx["b1"]
    rows = b1["arithmeticRows"]
    if rows == 0:
        return ["RT26-B1 VACUOUS: no arithmetic row was identified, so the "
                "demand algebra was not exercised at all"]
    if len(b1["publishedAgree"]) != rows:
        disagreeing = {rid: row for rid, row in b1["perRow"].items()
                       if rid not in b1["publishedAgree"]}
        out.append(
            f"RT26-B1 the published demand expressions agree with only "
            f"{len(b1['publishedAgree'])} of {rows} arithmetic vectors. The "
            f"artifact's own vectors and its own expressions cannot both be "
            f"right: {disagreeing}")
    if len(b1["causeAgree"]) != len([r for r in b1["perRow"].values()
                                     if r.get("expectedCauses") is not None]):
        out.append(
            f"RT26-B1 cause attribution disagrees with the published "
            f"expectedCauses on at least one row: "
            f"{[(k, v.get('causes'), v.get('expectedCauses')) for k, v in b1['perRow'].items() if v.get('expectedCauses') is not None and list(v.get('causes') or []) != list(v['expectedCauses'])]}")
    if b1["defaultConfigNonZero"]:
        out.append(
            f"RT26-B1 the DEFAULT configuration 0/0/0 evicts a non-zero number "
            f"of records at evictable-set size(s) {b1['defaultConfigNonZero'][:8]}. "
            f"Under the CD-RT-5 decision 0/0/0 is the configuration of every "
            f"project nobody has configured, so this is the common case and the "
            f"direction is toward deleting all of their evidence")
    if b1["unboundedNonZero"]:
        out.append(
            f"RT26-B1 a demand expression is non-zero at cap = UNBOUNDED: "
            f"{b1['unboundedNonZero'][:5]}. RT26-C-INV-15 requires every demand "
            f"to be total on Cap and to evaluate to 0 there")
    if b1["fallbackReached"]:
        out.append(
            "RT26-B1 the fallback clause the artifact declares UNREACHABLE and "
            "removed was reached, so removing it changed the expression")
    if b1["prefixInclusionViolations"]:
        out.append(
            f"RT26-B1 {b1['prefixInclusionViolations']} prefix-inclusion "
            f"violation(s) over {b1['prefixConfigurations']} configurations; the "
            f"single-total-order argument at boundIndependence.proof.step4 does "
            f"not hold")
    if b1["evictedSetChangedByDisablingASibling"]:
        out.append(
            f"RT26-B1 disabling the size bound changed WHICH records the "
            f"remaining bounds remove in "
            f"{b1['evictedSetChangedByDisablingASibling']} configuration(s). "
            f"Independence of the SET, not merely of the count, is the property "
            f"that makes the shipping product's parasitism class unrepresentable")
    if b1["crossDimensionSymbols"]:
        out.append(
            f"RT26-B1 a demand expression names another dimension's value or "
            f"lifted cap: {b1['crossDimensionSymbols']}. This is the shipping "
            f"product's defect by construction")
    # THE LIFT IS THE WHOLE REPAIR, so the published expression must be written
    # over its own LIFTED CAP and must not name its own RAW CONFIGURED VALUE.
    # Section 7.8: an instrument must re-derive its constants from the artifact
    # it checks, or it is testing its own transcription.  Without this, the
    # published expression could revert to the predecessor's raw-value form while
    # this file went on evaluating its own faithful copy of the repaired one.
    own_cap = {"count": "cap_count", "size": "cap_size", "time": "cap_age"}
    own_raw = {"count": "keepCount", "size": "maxTotalBytes",
               "time": "maxAgeSeconds"}
    for dimension in ("count", "size", "time"):
        text = b1["expressions"].get(dimension)
        if text is None:
            out.append(f"RT26-B1 no published demand expression for the "
                       f"{dimension} dimension")
            continue
        if own_cap[dimension] not in text:
            out.append(
                f"RT26-B1 the published {dimension} demand does not mention its "
                f"own lifted cap {own_cap[dimension]!r}: {text!r}. The lift is "
                f"what makes the disable point a value of the expression instead "
                f"of a guard beside it")
        if own_raw[dimension] in text:
            out.append(
                f"RT26-B1 the published {dimension} demand is written over the "
                f"RAW configured value {own_raw[dimension]!r} rather than over "
                f"its lifted cap: {text!r}. That is the predecessor's form, and "
                f"IR-RT25-B1 graded it BLOCKING because the expression is then "
                f"wrong at the value that is supposed to switch the dimension off")
        if re.search(r"\bif\b|\bunless\b|\botherwise\b|\bdisabledWhen\b", text):
            out.append(
                f"RT26-B1 the published {dimension} demand carries a "
                f"conditional token, so the disable behaviour is a branch rather "
                f"than a value of the expression: {text!r}")
    # the sibling-guard shape the predecessor was rejected for, hunted by name
    for path, value in scalar_leaves(doc):
        if leaf_name(path) == "disabledWhen":
            out.append(
                f"RT26-B1 {path}: a sibling `disabledWhen` field has returned. "
                f"IR-RT25-B1 graded exactly this BLOCKING -- a guard is a second "
                f"statement that has to agree with the first, and the whole class "
                f"of defect is the two disagreeing")
    # the artifact's own published re-measurement table, hard-compared
    table = get_path(doc, "$.partC_retentionBounds.sweep.demands."
                          "everyDemandIsZeroAtItsOwnDisableValue."
                          "reMeasuredAgainstTheArithmeticVectors") or {}
    for entry in table.get("perRow") or []:
        rid = entry.get("id")
        mine = b1["perRow"].get(rid)
        if mine is None:
            out.append(f"RT26-B1 the artifact's re-measurement table names {rid}, "
                       f"which this instrument did not identify as arithmetic")
            continue
        if entry.get("underThesePublishedExpressions") != mine["underV26"]:
            out.append(
                f"RT26-B1 {rid}: the artifact publishes "
                f"underThesePublishedExpressions "
                f"{entry.get('underThesePublishedExpressions')!r} and this "
                f"instrument computes {mine['underV26']!r}")
        if entry.get("underThePredecessorsPublishedExpressions") != mine["underV25"]:
            out.append(
                f"RT26-B1 {rid}: the artifact publishes "
                f"underThePredecessorsPublishedExpressions "
                f"{entry.get('underThePredecessorsPublishedExpressions')!r} and "
                f"this instrument computes {mine['underV25']!r}")
        declared = entry.get("demandsHere") or {}
        mapped = {"AGE": mine["demands"]["time"], "SIZE": mine["demands"]["size"],
                  "COUNT": mine["demands"]["count"]}
        if declared and declared != mapped:
            out.append(f"RT26-B1 {rid}: demandsHere {declared} disagrees with the "
                       f"recomputed {mapped}")
    declared_rows = table.get("rowsExecuted")
    if _exact_int(declared_rows) and declared_rows != rows:
        out.append(
            f"RT26-B1-SCOPE $.partC_retentionBounds.sweep.demands."
            f"everyDemandIsZeroAtItsOwnDisableValue."
            f"reMeasuredAgainstTheArithmeticVectors.method claims to have "
            f"re-executed 'every arithmetic row' of $.partC_retentionBounds."
            f"vectors and rowsExecuted is {declared_rows}; that path holds {rows} "
            f"arithmetic rows. Section 7.2.2's self-report class, in the mild "
            f"form -- mild only because the two omitted rows pass. Omitted: "
            f"{[r['id'] for r in _arith_rows(doc) if r['id'] not in {e.get('id') for e in table.get('perRow') or []}]}")
    return out


def _bounds_record(max_age=0, max_bytes=0, keep=0, revision=1):
    return {"schemaVersion": 1, "projectId": PROJECT,
            "retentionPolicyId": "rpol1:sha256:" + "0" * 64,
            "maxAgeSeconds": max_age, "maxTotalBytes": max_bytes,
            "keepCount": keep, "boundsRevision": revision,
            "retentionBoundsId": "rbnd1:sha256:" + "0" * 64}


def run_vectors(doc, ctx):
    """Drive all 20 rows.  Returns (findings, report)."""
    out = []
    rows = get_path(doc, "$.partC_retentionBounds.vectors.rows") or []
    by_id = {}
    for row in rows:
        if not isinstance(row, dict) or "id" not in row:
            out.append("RT26-VEC a vectors row has no id")
            continue
        if row["id"] in by_id:
            out.append(f"RT26-VEC duplicate vector id {row['id']!r}")
        by_id[row["id"]] = row

    missing = [v for v in VECTOR_IDS if v not in by_id]
    invented = [v for v in by_id if v not in VECTOR_IDS]
    if missing:
        out.append(f"RT26-VEC {len(missing)} declared vector id(s) absent from "
                   f"the artifact: {missing}. The id set is a frozen literal in "
                   f"this instrument precisely so that deleting a row is a "
                   f"finding rather than a smaller run")
    if invented:
        out.append(f"RT26-VEC {len(invented)} vector id(s) present that this "
                   f"instrument does not know: {invented}. A new row is not "
                   f"exercised by anything and must not be counted as coverage")

    executed = 0
    controls_run = 0
    controls_vacuous = []
    d9_codes = set(ctx["d9errorCodes"])

    def expect(vid, label, got, want):
        if got != want:
            out.append(f"RT26-VEC {vid}: {label} -- computed {got!r}, the row "
                       f"declares {want!r}")

    def control(vid, label, rejected, accepted):
        nonlocal controls_run
        controls_run += 1
        if rejected == accepted:
            controls_vacuous.append(f"{vid}:{label}")
            out.append(
                f"RT26-VEC-VACUOUS {vid}: the REJECTED reading ({label}) "
                f"produces the same result {rejected!r} as the accepted one, so "
                f"this control exhibits an input that is merely EMPTY rather "
                f"than WRONG (section 7.8)")

    for vid in VECTOR_IDS:
        row = by_id.get(vid)
        if row is None:
            continue
        executed += 1
        try:
            if vid in ("PC-V-01-COUNT-ONLY", "PC-V-04-INDEPENDENCE-MAX-NOT-SUM",
                       "PC-V-17-DEFAULT-CONFIGURATION-EVICTS-NOTHING",
                       "PC-V-18-TIME-DIMENSION-AT-ITS-ONLY-LEGAL-VALUE"):
                bounds = _row_bounds(row)
                order = eviction_order(population(row["evictableCount"],
                                                  row.get("evictableTotalBytes")))
                got = eviction_count(bounds, order, NOW)
                expect(vid, "evictionCount", got, row["expectedEvictionCount"])
                expect(vid, "attributed causes",
                       attribute_causes(bounds, order, NOW),
                       list(row.get("expectedCauses", [])))
                if "expectedDemands" in row:
                    mine = demands(bounds, order, NOW)
                    expect(vid, "expectedDemands", mine,
                           dict(row["expectedDemands"]))
                if "expectedCaps" in row:
                    caps = [unbounded_if_zero(v) for v in bounds]
                    declared = str(row["expectedCaps"])
                    if all(c is UNBOUNDED for c in caps) != (
                            declared.count("UNBOUNDED") == 3):
                        expect(vid, "expectedCaps",
                               [repr(c) for c in caps], declared)
                if row.get("isNegativeControl"):
                    if vid == "PC-V-04-INDEPENDENCE-MAX-NOT-SUM":
                        rejected = eviction_count_SUM(bounds, order, NOW)
                        control(vid, "demands summed rather than maxed",
                                rejected, got)
                        expect(vid, "resultUnderRejectedReading (sum)", rejected,
                               row.get("resultUnderRejectedReading"))
                    else:
                        rejected = eviction_count_V25(bounds, order, NOW)
                        control(vid, "the predecessor's published expressions",
                                rejected, got)
                        expect(vid, "resultUnderRejectedReading (v25 "
                                    "expressions)", rejected,
                               row.get("resultUnderRejectedReading"))

            elif vid in ("PC-V-02-PARASITISM-CONTROL-KEEP-ZERO",
                         "PC-V-03-PARASITISM-CONTROL-KEEP-ONE"):
                bounds = _row_bounds(row)
                order = eviction_order(population(row["evictableCount"],
                                                  row.get("evictableTotalBytes")))
                got = eviction_count(bounds, order, NOW)
                expect(vid, "evictionCount", got, row["expectedEvictionCount"])
                expect(vid, "attributed causes",
                       attribute_causes(bounds, order, NOW),
                       list(row.get("expectedCauses", [])))
                rejected = eviction_count_PARASITIC(bounds, order, NOW)
                control(vid, "the size demand computed inside the count branch",
                        rejected, got)
                expect(vid, "resultUnderRejectedReading (parasitic guard)",
                       rejected, row.get("resultUnderRejectedReading"))
                if vid == "PC-V-03-PARASITISM-CONTROL-KEEP-ONE":
                    values = demands(bounds, order, NOW)
                    if values["size"] != values["count"]:
                        out.append(
                            f"RT26-VEC {vid}: this row exists to exercise the "
                            f"tiebreak and its size and count demands are no "
                            f"longer equal ({values}); the tiebreak order is now "
                            f"unexercised by any row")
                    reversed_cause = attribute_causes_REVERSED(bounds, order, NOW)
                    control(vid, "the tiebreak order reversed", reversed_cause,
                            attribute_causes(bounds, order, NOW))

            elif vid == "PC-V-05-SILENT-REVERT-CONTROL":
                record = _bounds_record(keep=row["bounds"]["keepCount"])
                admission, code, _ = admit_bounds(record)
                expect(vid, "admission", admission, row["expectedAdmission"])
                expect(vid, "errorCode", code, row["expectedErrorCode"])
                rejected, _, resolved = admit_bounds_SILENT_REVERT(record)
                control(vid, "a negative value silently reverts to the default",
                        rejected, admission)
                if resolved is not None and resolved.get("keepCount") != PRODUCT_KEEP:
                    out.append(f"RT26-VEC {vid}: the rejected reading did not "
                               f"reproduce the declared "
                               f"resultUnderRejectedReading")

            elif vid in ("PC-V-06-EXACT-TYPE-BOOL", "PC-V-07-EXACT-TYPE-FLOAT",
                         "PC-V-08-EXACT-TYPE-NUMERIC-STRING"):
                payload = row["bounds"]["keepCount"]
                required = CONTROL_VECTOR_TYPES[vid]
                ok = (isinstance(payload, bool) if required is bool
                      else (not isinstance(payload, bool))
                      and isinstance(payload, required))
                if not ok:
                    out.append(
                        f"RT26-VEC {vid}: the control payload is spelled "
                        f"{type(payload).__name__}, not {required.__name__}; a "
                        f"control respelled as an ordinary integer is not a "
                        f"control and this row would then test nothing")
                record = _bounds_record(keep=payload)
                admission, code, _ = admit_bounds(record)
                expect(vid, "admission", admission, row["expectedAdmission"])
                expect(vid, "errorCode", code, row["expectedErrorCode"])
                rejected, _, resolved = admit_bounds_COERCING(record)
                control(vid, "a bare equality or coercion at admission",
                        rejected, admission)
                if resolved is not None and resolved.get("keepCount") != 200 \
                        and vid != "PC-V-06-EXACT-TYPE-BOOL":
                    out.append(f"RT26-VEC {vid}: the coercing reading did not "
                               f"admit the value as 200 as the row declares")

            elif vid == "PC-V-09-UNSATISFIABLE-AGE-BOUND":
                record = _bounds_record(max_age=row["bounds"]["maxAgeSeconds"])
                admission, code, _ = admit_bounds(record)
                expect(vid, "admission", admission, row["expectedAdmission"])
                expect(vid, "errorCode", code, row["expectedErrorCode"])
                if row["bounds"]["maxAgeSeconds"] != PRODUCT_MAX_AGE_SECONDS:
                    out.append(
                        f"RT26-VEC {vid}: the row's maxAgeSeconds is "
                        f"{row['bounds']['maxAgeSeconds']} and the note declares "
                        f"it is the shipping product's 60-day default expressed "
                        f"exactly, which is {PRODUCT_MAX_AGE_SECONDS}")
                rejected, _, _ = admit_bounds_SILENT_SKIP(record)
                control(vid, "an unsatisfiable dimension silently skipped",
                        rejected, admission)

            elif vid == "PC-V-10-PROTECTED-SET-EXCEEDS-BOUND":
                bounds = _row_bounds(row)
                order = eviction_order(population(row["evictableCount"]))
                footprint = 10 ** 6
                expect(vid, "write admission", admit_write(bounds, footprint,
                                                            order),
                       row["expectedWriteAdmission"])
                expect(vid, "evictionCount",
                       eviction_count(bounds, order, NOW),
                       row["expectedEvictionCount"])
                expect(vid, "overBound",
                       over_bound(footprint, bounds[1], order),
                       row["expectedOverBound"])
                rejected = admit_write_THROWING(bounds, footprint, order)
                control(vid, "the store throws and refuses the write", rejected,
                        row["expectedWriteAdmission"])

            elif vid == "PC-V-11-CAUSE-BLINDNESS-WITHIN-PURGED":
                units = [{"requires": ["k1"], "grants": "replayable"},
                         {"requires": ["k2"], "grants": "verifiable"}]
                states = {"k1": "PURGED", "k2": "PURGED"}
                a = effective_capability("replayable", units, states)
                b = effective_capability("replayable", units, states)
                expect(vid, "effectiveCapability A", a,
                       row["expectedEffectiveCapabilityA"])
                expect(vid, "effectiveCapability B", b,
                       row["expectedEffectiveCapabilityB"])
                expect(vid, "expectedEqual", a == b, row["expectedEqual"])
                leak_a = effective_capability_CAUSE_LEAKING(
                    "replayable", units, states, ["RETENTION_SIZE_BOUND"])
                leak_b = effective_capability_CAUSE_LEAKING(
                    "replayable", units, states, ["RETENTION_USER_REQUEST"])
                control(vid, "cause reaches the derivation", leak_a == leak_b,
                        a == b)

            elif vid == "PC-V-12-ABSENT-BOUNDS-RESOLVE-TO-UNBOUNDED":
                age, size, keep, provenance = effective_bounds(ABSENT)
                expect(vid, "resolved bounds", f"{age} / {size} / {keep}",
                       row["expectedResolvedBounds"])
                expect(vid, "provenance", provenance, row["expectedProvenance"])
                order = eviction_order(population(5, 500))
                got = eviction_count((age, size, keep), order, NOW)
                expect(vid, "evictionCount", got, row["expectedEvictionCount"])
                p_age, p_size, p_keep, _ = effective_bounds_PRODUCT_DEFAULTS(ABSENT)
                # the control is on the RESOLVED BOUNDS, because that is what the
                # rejected reading changes.  Comparing eviction counts at a
                # five-member population would be vacuous -- a keepCount of 200
                # evicts nothing there either -- so the eviction difference is
                # exercised at a population the product's own default reaches.
                control(vid, "absent bounds read as the product's values",
                        (p_age, p_size, p_keep), (age, size, keep))
                big = eviction_order(population(PRODUCT_KEEP + 1))
                rejected = eviction_count((0, 0, p_keep), big, NOW)
                control(vid, "the product's keepCount applied to an unconfigured "
                             "project", rejected,
                        eviction_count((age, size, keep), big, NOW))
                if row.get("boundsRecordPresent") is not False:
                    out.append(f"RT26-VEC {vid}: boundsRecordPresent must be "
                               f"false for this row to be about absence")

            elif vid == "PC-V-13-ABSENT-POLICY-RESOLVES-DURABLE":
                posture, provenance = effective_posture(ABSENT)
                expect(vid, "posture", posture, row["expectedPosture"])
                expect(vid, "provenance", provenance, row["expectedProvenance"])
                expect(vid, "durable-authoritative outcome",
                       durable_authoritative_outcome(ABSENT),
                       row["expectedDurableAuthoritativeOutcome"])
                _, _, on_disk = resolve_and_maybe_persist(ABSENT, "DISMISSED")
                expect(vid, "policy persisted", on_disk is not ABSENT,
                       row["expectedPolicyPersisted"])
                v24_cell = _v24_cell(ctx, "ci", "ABSENT", "DURABLE_AUTHORITATIVE")
                rejected = v24_cell.get("outcome") if v24_cell else None
                control(vid, "the predecessor's premise (absence has no posture)",
                        rejected, row["expectedDurableAuthoritativeOutcome"])

            elif vid == "PC-V-14-EPHEMERAL-IS-ALWAYS-CONSENTED":
                policy = {"posture": "EPHEMERAL_ONLY"}
                posture, provenance = effective_posture(policy)
                expect(vid, "posture", posture, row["expectedPosture"])
                expect(vid, "provenance", provenance, row["expectedProvenance"])
                outcome = durable_authoritative_outcome(policy)
                expect(vid, "durable-authoritative outcome", outcome,
                       row["expectedDurableAuthoritativeOutcome"])
                if row["expectedErrorCode"] not in d9_codes:
                    out.append(
                        f"RT26-VEC {vid}: expectedErrorCode "
                        f"{row['expectedErrorCode']!r} is not a member of the "
                        f"live D9 closed error-code vocabulary")
                rejected = durable_authoritative_outcome_DEMOTING(policy)
                control(vid, "the default removes every retention refusal",
                        rejected, outcome)

            elif vid == "PC-V-15-DEFAULT-IS-NEVER-PERSISTED":
                _, _, on_disk = resolve_and_maybe_persist(ABSENT, "PROCEED")
                expect(vid, "policy on disk after", "ABSENT" if on_disk is ABSENT
                       else "PRESENT", row["expectedPolicyOnDiskAfter"])
                _, provenance = effective_posture(on_disk if on_disk is not ABSENT
                                                  else ABSENT)
                expect(vid, "provenance on the next run", provenance,
                       row["expectedProvenanceOnNextRun"])
                _, _, leaked = resolve_and_maybe_persist_PERSISTING(ABSENT,
                                                                    "PROCEED")
                control(vid, "the resolution persists what it resolved",
                        leaked is ABSENT, on_disk is ABSENT)
                if leaked is not ABSENT:
                    _, leaked_provenance = effective_posture(leaked)
                    if leaked_provenance != "CONSENTED":
                        out.append(
                            f"RT26-VEC {vid}: the rejected reading was expected "
                            f"to manufacture CONSENTED provenance from a default "
                            f"and produced {leaked_provenance!r}")

            elif vid == "PC-V-16-DISMISSAL-DOES-NOT-SUPPRESS-THE-NEXT-ASK":
                first = ask_performed("local-interactive", ABSENT,
                                      "DURABLE_AUTHORITATIVE", False)
                second = ask_performed("local-interactive", ABSENT,
                                       "DURABLE_AUTHORITATIVE", True)
                expect(vid, "first-run ask", first,
                       row["expectedFirstRunAskPerformed"])
                expect(vid, "second-run ask", second,
                       row["expectedSecondRunAskPerformed"])
                _, _, on_disk = resolve_and_maybe_persist(ABSENT, "DISMISSED")
                if on_disk is not ABSENT:
                    out.append(f"RT26-VEC {vid}: a dismissal wrote a policy, so "
                               f"the second ask is suppressed by a record no "
                               f"human answered")
                rejected = ask_performed_SUPPRESSING("local-interactive", ABSENT,
                                                     "DURABLE_AUTHORITATIVE", True)
                control(vid, "a dismissal suppresses the next ask", rejected,
                        second)

            elif vid == "PC-V-19-BOUNDS-IDENTITY-WORKED-VECTORS":
                control_rows = get_path(
                    doc, "$.partC_retentionBounds.identity.encoderControl.rows") or []
                reproduced = 0
                for entry in control_rows:
                    source = _v24_policy_vector(ctx, entry.get("id"))
                    if source is None:
                        out.append(f"RT26-VEC {vid}: encoder control names "
                                   f"{entry.get('id')!r}, which is not a "
                                   f"policyVectors row of the pinned v24")
                        continue
                    policy = source["policy"]
                    length, value = retention_policy_id(
                        policy["projectId"], policy["posture"],
                        policy["consentRecordRef"])
                    if value != policy["retentionPolicyId"]:
                        out.append(
                            f"RT26-VEC {vid}: the ENCODER CONTROL failed. "
                            f"{entry.get('id')} recomputes to {value}, and the "
                            f"pinned v24 publishes {policy['retentionPolicyId']}. "
                            f"An encoder that cannot reproduce a golden it did "
                            f"not author produces digests nobody can check, so "
                            f"the rbnd1 values below are not evidence")
                        continue
                    if entry.get("preimageByteLength") != length:
                        out.append(
                            f"RT26-VEC {vid}: {entry.get('id')} preimage is "
                            f"{length} bytes, published "
                            f"{entry.get('preimageByteLength')!r}")
                    if entry.get("recomputedHere") != value:
                        out.append(
                            f"RT26-VEC {vid}: {entry.get('id')} recomputedHere "
                            f"{entry.get('recomputedHere')!r} != {value}")
                    reproduced += 1
                declared_reproduced = get_path(
                    doc, "$.partC_retentionBounds.identity.encoderControl."
                         "goldensReproduced")
                if declared_reproduced != reproduced:
                    out.append(
                        f"RT26-VEC {vid}: goldensReproduced declares "
                        f"{declared_reproduced!r}, measured {reproduced}")
                identities = set()
                lengths = set()
                for entry in row.get("rows") or []:
                    length, value = retention_bounds_id(
                        row["projectId"], row["retentionPolicyId"],
                        entry["maxAgeSeconds"], entry["maxTotalBytes"],
                        entry["keepCount"], entry["boundsRevision"])
                    identities.add(value)
                    lengths.add(length)
                    if value != entry["retentionBoundsId"]:
                        out.append(
                            f"RT26-VEC {vid}: row {entry.get('label')!r} "
                            f"recomputes to {value} and the artifact publishes "
                            f"{entry['retentionBoundsId']}")
                    if length != entry["preimageByteLength"]:
                        out.append(
                            f"RT26-VEC {vid}: row {entry.get('label')!r} preimage "
                            f"is {length} bytes and the artifact publishes "
                            f"{entry['preimageByteLength']!r}")
                if len(identities) != len(row.get("rows") or []):
                    out.append(
                        f"RT26-VEC {vid}: the four worked vectors do not have "
                        f"four distinct identities, so the recipe does not "
                        f"separate on VALUE")
                if len(lengths) > 1:
                    out.append(
                        f"RT26-VEC {vid}: the preimages are not all the same "
                        f"length ({sorted(lengths)}), so the separating property "
                        f"the row states does not hold")

            elif vid == "PC-V-20-IDENTITY-IS-OVER-CONFIGURED-VALUES-NOT-LIFTED-CAPS":
                bounds = _row_bounds(row)
                anchor = by_id.get("PC-V-19-BOUNDS-IDENTITY-WORKED-VECTORS") or {}
                project = anchor.get("projectId", PROJECT)
                policy_id = anchor.get("retentionPolicyId", "")
                length, value = retention_bounds_id(project, policy_id, bounds[0],
                                                     bounds[1], bounds[2], 1)
                expect(vid, "preimage byte length", length,
                       row["expectedPreimageByteLength"])
                expect(vid, "retentionBoundsId", value,
                       row["expectedRetentionBoundsId"])
                raised = False
                try:
                    retention_bounds_id_OVER_CAPS(project, policy_id, bounds[0],
                                                   bounds[1], bounds[2], 1)
                except RefusedError:
                    raised = True
                control(vid, "the preimage frames the lifted caps", raised, False)
                if not raised:
                    out.append(
                        f"RT26-VEC {vid}: the rejected reading did NOT become "
                        f"unconstructible. UNBOUNDED has no u64be encoding, so an "
                        f"identity over lifted caps must be impossible to build "
                        f"rather than merely discouraged")
        except RefusedError as exc:
            out.append(f"RT26-VEC {vid}: a reference derivation refused: {exc}")
        except (KeyError, TypeError, IndexError) as exc:
            out.append(f"RT26-VEC {vid}: the row is missing a field this driver "
                       f"needs ({type(exc).__name__}: {exc}), so the vector could "
                       f"not be driven")

    declared = get_path(doc, "$.partC_retentionBounds.vectors.count")
    report = {"declared": declared if _exact_int(declared) else len(rows),
              "executed": executed, "controlsRun": controls_run,
              "controlsVacuous": controls_vacuous}
    ctx["vectorReport"] = report
    if executed != len(VECTOR_IDS):
        out.append(f"RT26-VEC only {executed} of {len(VECTOR_IDS)} vectors were "
                   f"executed")
    return out, report


def _v24_cells(ctx):
    return get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                "askDecisionTable.cells") or []


def _v24_cell(ctx, profile, presence, custody):
    for cell in _v24_cells(ctx):
        if (cell.get("invocationProfile") == profile
                and cell.get("policyPresence") == presence
                and cell.get("requestedCustody") == custody):
            return cell
    return None


def _v24_outcomes(ctx):
    return get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                "interactionOutcomes.outcomes") or []


def _v24_policy_vector(ctx, vid):
    for row in (get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                     "policyVectors") or []):
        if row.get("id") == vid:
            return row
    return None


# ===========================================================================
# SECTION 4 -- INVARIANT EXECUTION.  All 24 entries of
# $.partC_retentionBounds.invariants, each with a driver that can fail.
#
# The id list is a FROZEN LITERAL, not a length read from the artifact.  Section
# 7.2.2's corollary: a registry sized from the artifact cannot police that
# artifact, and `for i in invariants: check(i)` is structurally unable to notice
# a deleted invariant.
# ===========================================================================

INVARIANT_IDS = (
    tuple(f"RT25-C-INV-{n:02d}" for n in range(1, 15))
    + tuple(f"RT25-D-INV-{n:02d}" for n in range(1, 6))
    + ("RT26-C-INV-15", "RT26-C-INV-16", "RT26-A-INV-17", "RT26-A-INV-18",
       "RT26-A-INV-19")
)

GRID_KEEP = (0, 1, 2, 3, 5, 7)
GRID_BYTES = (0, 1, 50, 100, 300, 500, 10 ** 9)
GRID_AGE = (0,)                     # DEP-RT25-01: the only admissible value
GRID_SIZES = (0, 1, 3, 5, 7)


def _grids():
    for size in GRID_SIZES:
        order = eviction_order(population(size, size * 100))
        for keep, max_bytes, age in itertools.product(GRID_KEEP, GRID_BYTES,
                                                      GRID_AGE):
            yield (age, max_bytes, keep), order


def inv_c01(doc, ctx):
    """A sweep emits only PURGED entries and can never raise capability."""
    out = []
    for bounds, order in _grids():
        for entry in retention_sweep(bounds, order, NOW):
            if entry["toState"] != "PURGED":
                out.append(f"RT25-C-INV-01 the sweep emitted toState "
                           f"{entry['toState']!r} at bounds {bounds}")
                return out
    units = [{"requires": ["k1"], "grants": "replayable"}]
    before = effective_capability("replayable", units, {"k1": "AVAILABLE"})
    after = effective_capability("replayable", units, {"k1": "PURGED"})
    if CAPABILITY_RANK[after] > CAPABILITY_RANK[before]:
        out.append("RT25-C-INV-01 a purge RAISED effectiveCapability")
    if get_path(doc, "$.partC_retentionBounds.sweep.emitsNoOtherToState") is not True:
        out.append("RT25-C-INV-01 $.partC_retentionBounds.sweep."
                   "emitsNoOtherToState is not true")
    return out


def inv_c02(doc, ctx):
    """Each demand is a total expression over the shared order and its OWN
    lifted cap; no bound's value or cap appears in another's demand."""
    out = []
    if ctx["b1"]["crossDimensionSymbols"]:
        out.append(f"RT25-C-INV-02 cross-dimension symbols in a published "
                   f"expression: {ctx['b1']['crossDimensionSymbols']}")
    # executable half: vary one dimension's configured value and require the
    # other two demands to be pointwise unchanged
    for size in GRID_SIZES:
        order = eviction_order(population(size, size * 100))
        base = demands((0, 0, 0), order, NOW)
        for keep in GRID_KEEP:
            here = demands((0, 0, keep), order, NOW)
            if here["size"] != base["size"] or here["time"] != base["time"]:
                out.append(f"RT25-C-INV-02 changing keepCount to {keep} moved "
                           f"the size or time demand at n={size}: {base} -> "
                           f"{here}")
                return out
        for max_bytes in GRID_BYTES:
            here = demands((0, max_bytes, 0), order, NOW)
            if here["count"] != base["count"] or here["time"] != base["time"]:
                out.append(f"RT25-C-INV-02 changing maxTotalBytes to "
                           f"{max_bytes} moved the count or time demand at "
                           f"n={size}: {base} -> {here}")
                return out
    return out


def inv_c03(doc, ctx):
    """The evicted set is a prefix of one total order and the count is the
    MAXIMUM of the demands, never their sum."""
    out = []
    separated = False
    for bounds, order in _grids():
        values = demands(bounds, order, NOW)
        count = eviction_count(bounds, order, NOW)
        if count != max(values.values()):
            out.append(f"RT25-C-INV-03 evictionCount {count} != max{values} at "
                       f"{bounds}")
            return out
        # max and sum coincide whenever at most one demand is non-zero, so the
        # separating test is only meaningful where two are.  Recorded as a
        # SEPARATION, not as a per-configuration assertion.
        if sum(1 for v in values.values() if v) > 1:
            separated = True
            if count == sum(values.values()):
                out.append(f"RT25-C-INV-03 evictionCount agrees with the SUM at "
                           f"{bounds} where two demands are non-zero, so the "
                           f"composition is indistinguishable from a sum here")
                return out
        chosen = evicted_set(bounds, order, NOW)
        if chosen != order[:len(chosen)]:
            out.append(f"RT25-C-INV-03 the evicted set is not a prefix at "
                       f"{bounds}")
            return out
    if not separated:
        out.append("RT25-C-INV-03 VACUOUS: no grid configuration made two demands "
                   "non-zero at once, so max and sum were never distinguishable "
                   "and this invariant tested nothing")
    if not order_is_total(population(7, 700)):
        out.append("RT25-C-INV-03 the eviction order is not total")
    return out


def inv_c04(doc, ctx):
    """Every PURGED entry carries exactly one cause from the closed partition;
    an absent or out-of-partition cause is refused."""
    out = []
    good = {"toState": "PURGED", "cause": "RETENTION_COUNT_BOUND"}
    if admit_transition(good)[0] != "ADMITTED":
        out.append("RT25-C-INV-04 a well-formed PURGED entry was refused")
    for bad in ({"toState": "PURGED"},
                {"toState": "PURGED", "cause": None},
                {"toState": "PURGED", "cause": True},
                {"toState": "PURGED", "cause": 1},
                {"toState": "PURGED", "cause": "RETENTION_POSTURE_CHANGE"},
                {"toState": "PURGED", "cause": ["RETENTION_COUNT_BOUND"]}):
        if admit_transition(bad)[0] != "REFUSED":
            out.append(f"RT25-C-INV-04 admitted a PURGED entry with cause "
                       f"{bad.get('cause')!r}")
    members = get_path(doc, "$.partC_retentionBounds.causeVocabulary."
                            "closedPartitions[0].members") or []
    if list(members) != list(CAUSE_PARTITION):
        out.append(f"RT25-C-INV-04 the published partition {members} is not the "
                   f"closed four-member partition {list(CAUSE_PARTITION)}")
    # `cause` is an EXISTING field of v24's ledger entry, not a new one, and its
    # position is derived from v24's own ordered field list rather than asserted.
    ordered = list(get_path(ctx["v24"], "$.partB_purgeSemantics.ledger."
                                        "entryOrderedFields") or [])
    declared_position = get_path(doc, "$.partC_retentionBounds.causeVocabulary."
                                      "orderedPosition")
    if "cause" not in ordered:
        out.append("RT25-C-INV-04 the pinned v24 ledger entry has no `cause` "
                   "field, so this artifact's 'the field is not new' claim is "
                   "false")
    else:
        measured_position = ordered.index("cause") + 1
        if declared_position != measured_position:
            out.append(f"RT25-C-INV-04 causeVocabulary.orderedPosition declares "
                       f"{declared_position!r} and `cause` sits at position "
                       f"{measured_position} of the pinned v24 ledger entry's "
                       f"{len(ordered)} ordered fields")
    if get_path(doc, "$.partC_retentionBounds.causeVocabulary.fieldIsNotNew") \
            is not True:
        out.append("RT25-C-INV-04 fieldIsNotNew is not true, yet the field is "
                   "present in the pinned v24 ledger entry")
    if get_path(doc, "$.partC_retentionBounds.causeVocabulary.positionUnchanged") \
            is not True:
        out.append("RT25-C-INV-04 positionUnchanged is not true")
    return out


def inv_c05(doc, ctx):
    """Two entries agreeing on toState and differing only in cause derive the
    same effectiveCapability."""
    out = []
    units = [{"requires": ["k1"], "grants": "replayable"},
             {"requires": ["k2"], "grants": "verifiable"}]
    states = {"k1": "PURGED", "k2": "AVAILABLE"}
    results = {c: effective_capability("replayable", units, states)
               for c in CAUSE_PARTITION}
    if len(set(results.values())) != 1:
        out.append(f"RT25-C-INV-05 cause changed the derived capability: "
                   f"{results}")
    leaking = {c: effective_capability_CAUSE_LEAKING("replayable", units, states,
                                                     [c])
               for c in CAUSE_PARTITION}
    if len(set(leaking.values())) == 1:
        out.append("RT25-C-INV-05 VACUOUS: the cause-leaking control derives the "
                   "same capability for every cause, so this invariant is not "
                   "distinguishing anything")
    return out


def inv_c06(doc, ctx):
    """No ledger entry is ever removed, rewritten or expired."""
    out = []
    entries = [{"rawKey": "k1", "toState": "AVAILABLE", "atSequence": 1},
               {"rawKey": "k1", "toState": "PURGED", "atSequence": 2}]
    before = len(entries)
    order = eviction_order(population(3, 300))
    emitted = retention_sweep((0, 0, 1), order, NOW)
    after = entries + emitted
    if len(after) < before:
        out.append("RT25-C-INV-06 the sweep removed ledger entries")
    if any(e is not entries[i] for i, e in enumerate(after[:before])):
        out.append("RT25-C-INV-06 the sweep rewrote an existing ledger entry")
    folded = fold_ledger(after)
    if folded.get("k1") != "PURGED":
        out.append("RT25-C-INV-06 folding the ledger lost a recorded transition")
    return out


def inv_c07(doc, ctx):
    """A bound is never an admission gate."""
    out = []
    for bounds, order in _grids():
        if admit_write(bounds, 10 ** 9, order) != "ADMITTED":
            out.append(f"RT25-C-INV-07 a write was refused at bounds {bounds}")
            return out
    if admit_write_THROWING((0, 1, 0), 10 ** 9, []) != "REFUSED":
        out.append("RT25-C-INV-07 VACUOUS: the throwing control did not refuse, "
                   "so the invariant distinguishes nothing")
    return out


def inv_c08(doc, ctx):
    """An invalid or unsatisfiable bounds record is refused at admission and is
    never silently defaulted or silently skipped."""
    out = []
    for record, why in (
            (_bounds_record(keep=-1), "negative keepCount"),
            (_bounds_record(max_age=5184000), "unsatisfiable age bound"),
            (_bounds_record(keep=True), "boolean keepCount"),
            (_bounds_record(keep=200.0), "float keepCount"),
            (_bounds_record(keep="200"), "numeric-string keepCount"),
            (dict(_bounds_record(), posture="DURABLE_RETAINED"),
             "a posture field inside the bounds record")):
        admission, code, resolved = admit_bounds(record)
        if admission != "REFUSED":
            out.append(f"RT25-C-INV-08 admitted a record with {why}")
        elif code != "CONFIG.INVALID":
            out.append(f"RT25-C-INV-08 refused {why} with {code!r} rather than "
                       f"CONFIG.INVALID")
        if resolved is not None:
            out.append(f"RT25-C-INV-08 a refused record still produced resolved "
                       f"values ({why})")
    if "CONFIG.INVALID" not in set(ctx["d9errorCodes"]):
        out.append("RT25-C-INV-08 CONFIG.INVALID is not a member of the live D9 "
                   "closed error-code vocabulary, so the refusal has no spelling")
    return out


def inv_c09(doc, ctx):
    """Every closed scalar of ProjectRetentionBoundsV1 is admitted by exact JSON
    type at any depth before its content is compared."""
    out = []
    for field in ("maxAgeSeconds", "maxTotalBytes", "keepCount",
                  "boundsRevision", "schemaVersion"):
        for spelling in (True, False, 1.0, "1", None, [1], {"v": 1}):
            record = _bounds_record()
            record[field] = spelling
            if admit_bounds(record)[0] != "REFUSED":
                out.append(f"RT25-C-INV-09 admitted {field}={spelling!r} "
                           f"({type(spelling).__name__})")
    if admit_bounds(_bounds_record())[0] != "ADMITTED":
        out.append("RT25-C-INV-09 VACUOUS: the well-formed record is refused "
                   "too, so nothing distinguishes an exact-type failure")
    if admit_bounds_COERCING(_bounds_record(keep=True))[0] != "ADMITTED":
        out.append("RT25-C-INV-09 VACUOUS: the coercing control did not admit a "
                   "boolean, so the control is not wrong")
    return out


def inv_c10(doc, ctx):
    """An absent record and an all-zero record agree on every value and differ
    on provenance; neither purges anything."""
    out = []
    absent = effective_bounds(ABSENT)
    zeroed = effective_bounds(_bounds_record())
    if absent[:3] != zeroed[:3]:
        out.append(f"RT25-C-INV-10 values differ: {absent[:3]} vs {zeroed[:3]}")
    if absent[3] == zeroed[3]:
        out.append(f"RT25-C-INV-10 provenance does NOT differ: both "
                   f"{absent[3]!r}; the CONSENTED/DEFAULTED distinction has "
                   f"collapsed at the point it is load bearing")
    if absent[3] not in BOUNDS_PROVENANCE_ENUM or zeroed[3] not in BOUNDS_PROVENANCE_ENUM:
        out.append("RT25-C-INV-10 a provenance outside the closed enum")
    for size in GRID_SIZES:
        order = eviction_order(population(size, size * 100))
        if eviction_count(absent[:3], order, NOW) != 0:
            out.append(f"RT25-C-INV-10 the absent resolution purged at n={size}")
            break
        if eviction_count(zeroed[:3], order, NOW) != 0:
            out.append(f"RT25-C-INV-10 the all-zero record purged at n={size}")
            break
    return out


def inv_c11(doc, ctx):
    """A sweep reads no ledger, footprint or bounds record of any other
    ProjectId.  Executable: the sweep's signature takes exactly three arguments
    and none of them is a project handle, so a second project's data cannot be
    reached; and the artifact must still declare the scope per-project."""
    out = []
    if get_path(doc, "$.partC_retentionBounds.sweep.scope.perProject") is not True:
        out.append("RT25-C-INV-11 sweep.scope.perProject is not true")
    if get_path(doc, "$.partC_retentionBounds.sweep.scope.global") is not False:
        out.append("RT25-C-INV-11 sweep.scope.global is not false")
    order_a = eviction_order(population(3, 300))
    order_b = eviction_order(population(9, 900))
    a1 = retention_sweep((0, 0, 1), order_a, NOW)
    a2 = retention_sweep((0, 0, 1), order_a, NOW)
    if [e["rawKey"] for e in a1] != [e["rawKey"] for e in a2]:
        out.append("RT25-C-INV-11 the sweep is not deterministic on one project")
    keys_b = {m["recordCasRef"] for m in order_b[3:]}
    if any(e["rawKey"] in keys_b for e in a1):
        out.append("RT25-C-INV-11 the sweep reached a key outside the evictable "
                   "set it was handed")
    return out


def inv_c12(doc, ctx):
    """purgeMutationBoundary.mutatesExactly still has exactly two members and no
    member of doesNotMutate is touched."""
    out = []
    mutates = get_path(ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary."
                                   "mutatesExactly") or []
    not_mutated = get_path(ctx["v24"], "$.partB_purgeSemantics."
                                       "purgeMutationBoundary.doesNotMutate") or []
    if len(mutates) != 2:
        out.append(f"RT25-C-INV-12 the pinned v24 mutation boundary has "
                   f"{len(mutates)} members, not 2")
    declared = get_path(doc, "$.partC_retentionBounds.whyThisIsSmallerThanItLooks."
                             "measuredDeltas.purgeMutatesExactlyAfter")
    if _exact_int(declared) and declared != len(mutates):
        out.append(f"RT25-C-INV-12 purgeMutatesExactlyAfter declares "
                   f"{declared!r}, the pinned v24 has {len(mutates)}")
    declared_not = get_path(doc, "$.partC_retentionBounds."
                                 "whyThisIsSmallerThanItLooks.measuredDeltas."
                                 "purgeDoesNotMutateAfter")
    if _exact_int(declared_not) and declared_not != len(not_mutated):
        out.append(f"RT25-C-INV-12 purgeDoesNotMutateAfter declares "
                   f"{declared_not!r}, the pinned v24 has {len(not_mutated)}")
    emitted = retention_sweep((0, 0, 1), eviction_order(population(3, 300)), NOW)
    for entry in emitted:
        if set(entry) - {"rawKey", "toState", "cause", "atSequence"}:
            out.append(f"RT25-C-INV-12 the sweep emitted a field outside the "
                       f"transition record: {sorted(entry)}")
            break
    return out


def inv_c13(doc, ctx):
    """A record in OUTAGE is never evictable, so a reversible fault is never
    converted into a terminal loss."""
    out = []
    ledger = [{"rawKey": "k1", "toState": "AVAILABLE", "atSequence": 1},
              {"rawKey": "k2", "toState": "OUTAGE", "atSequence": 2},
              {"rawKey": "k3", "toState": "MISSING-DEPENDENCY", "atSequence": 3}]
    folded = fold_ledger(ledger)
    evictable = [k for k, state in folded.items() if state == "AVAILABLE"]
    if "k2" in evictable:
        out.append("RT25-C-INV-13 a record in OUTAGE was evictable")
    if "k3" in evictable:
        out.append("RT25-C-INV-13 a record in MISSING-DEPENDENCY was evictable")
    if "k1" not in evictable:
        out.append("RT25-C-INV-13 VACUOUS: no record was evictable at all, so "
                   "excluding OUTAGE distinguishes nothing")
    if get_path(doc, "$.partC_retentionBounds.evictableSet.outageIsNeverEvictable") \
            is not True:
        out.append("RT25-C-INV-13 $.partC_retentionBounds.evictableSet."
                   "outageIsNeverEvictable is not true")
    return out


def inv_c14(doc, ctx):
    """This artifact adds no D9 deficiency member, reason code or error code,
    and the measured retention gap is RECOMPUTED FROM THE PINNED D9 BYTES ON
    EVERY RUN.  RT26-RES-03 records that nothing performed that per-run
    recomputation.  This driver is the thing that performs it."""
    out = []
    d9 = ctx["d9"]
    block = get_path(doc, "$.partC_retentionBounds.d9ReasonCodePosition."
                          "measuredLiveFromPinnedD9Bytes") or {}
    predicate = [str(t).upper() for t in (block.get("retentionTokenPredicate")
                                           or [])]
    if not predicate:
        out.append("RT25-C-INV-14 the retention token predicate is empty, so "
                   "'0 matching' is true of everything and measures nothing")
        return out
    error_codes = list(get_path(d9, "$.codeVocabulary.errorCodes") or [])
    reason_codes = list(get_path(d9, "$.codeVocabulary.reasonCodes") or [])
    deficiency = list((get_path(d9, "$.codeMaps.deficiencyToReasonCode") or {}))
    measured = {
        "deficiencyMemberCount": len(deficiency),
        "reasonCodeCount": len(reason_codes),
        "errorCodeCount": len(error_codes),
        "deficiencyMembersMatchingPredicate":
            sum(1 for m in deficiency if any(t in str(m).upper() for t in predicate)),
        "reasonCodesMatchingPredicate":
            sum(1 for m in reason_codes if any(t in str(m).upper() for t in predicate)),
        "errorCodesMatchingPredicate":
            sum(1 for m in error_codes if any(t in str(m).upper() for t in predicate)),
    }
    for field, value in measured.items():
        if block.get(field) != value:
            out.append(f"RT25-C-INV-14 {field} declares {block.get(field)!r} and "
                       f"the pinned D9 bytes measure {value}")
    if block.get("sha256") != GATED_PINS["d9-exit-contract.v1.14.json"]:
        out.append(f"RT25-C-INV-14 the D9 digest recorded in the artifact "
                   f"({block.get('sha256')!r}) is not the digest this instrument "
                   f"gates")
    for field in ("deficiencyMembersAddedByThisArtifact",
                  "errorCodesAddedByThisArtifact", "codesAddedByThisArtifact"):
        for path, value in scalar_leaves(doc):
            if leaf_name(path) == field and value != 0:
                out.append(f"RT25-C-INV-14 {path} declares {value!r}; this "
                           f"artifact may not amend a vocabulary it does not own")
    # the 18-versus-19 distinction, recomputed
    union = set()
    for name in ("rejectionCauseToErrorCode", "faultCauseToErrorCode"):
        union |= set((get_path(d9, f"$.codeMaps.{name}") or {}).values())
    if len(error_codes) - len(union) != 1:
        out.append(f"RT25-C-INV-14 the vocabulary/map difference is "
                   f"{len(error_codes) - len(union)}, not the 1 the artifact "
                   f"records (19 in codeVocabulary, 18 across the two maps)")
    return out


def inv_d01(doc, ctx):
    """effective_posture is total: every input yields exactly one posture and
    one provenance."""
    out = []
    inputs = [ABSENT, {"posture": "DURABLE_RETAINED"},
              {"posture": "EPHEMERAL_ONLY"}]
    seen = []
    for value in inputs:
        posture, provenance = effective_posture(value)
        if posture not in POSTURE_ENUM:
            out.append(f"RT25-D-INV-01 posture {posture!r} outside the enum")
        if provenance not in POSTURE_PROVENANCE_ENUM:
            out.append(f"RT25-D-INV-01 provenance {provenance!r} outside the enum")
        seen.append((posture, provenance))
    if len(seen) != 3:
        out.append("RT25-D-INV-01 the resolution is not total over its three "
                   "declared inputs")
    if effective_posture(ABSENT) != ("DURABLE_RETAINED", "DEFAULTED"):
        out.append("RT25-D-INV-01 effective_posture(ABSENT) is not "
                   "(DURABLE_RETAINED, DEFAULTED)")
    rows = get_path(doc, "$.postureResolution.theDerivation.rows") or []
    if len(rows) != 3:
        out.append(f"RT25-D-INV-01 the published derivation has {len(rows)} "
                   f"rows, not 3")
    for row in rows:
        if row.get("posture") not in POSTURE_ENUM:
            out.append(f"RT25-D-INV-01 published row posture "
                       f"{row.get('posture')!r} is outside the closed enum")
        if row.get("provenance") not in POSTURE_PROVENANCE_ENUM:
            out.append(f"RT25-D-INV-01 published row provenance "
                       f"{row.get('provenance')!r} is outside the closed enum")
    return out


def inv_d02(doc, ctx):
    """EPHEMERAL_ONLY is reachable only with provenance CONSENTED."""
    out = []
    for value in (ABSENT, {"posture": "DURABLE_RETAINED"},
                  {"posture": "EPHEMERAL_ONLY"}):
        posture, provenance = effective_posture(value)
        if posture == "EPHEMERAL_ONLY" and provenance != "CONSENTED":
            out.append(f"RT25-D-INV-02 ({posture}, {provenance}) is producible "
                       f"from {value!r}")
    rows = get_path(doc, "$.postureResolution.theDerivation.rows") or []
    if [r for r in rows if r.get("posture") == "EPHEMERAL_ONLY"
            and r.get("provenance") == "DEFAULTED"]:
        out.append("RT25-D-INV-02 the published derivation carries a "
                   "(EPHEMERAL_ONLY, DEFAULTED) row")
    if effective_posture_LEAKING_DEFAULT(ABSENT) != ("EPHEMERAL_ONLY",
                                                     "DEFAULTED"):
        out.append("RT25-D-INV-02 VACUOUS: the leaking control does not produce "
                   "the forbidden pair, so the invariant distinguishes nothing")
    return out


def inv_d03(doc, ctx):
    """No code path persists a policy whose posture came from the default."""
    out = []
    for interaction in ("PROCEED", "DISMISSED-TIMEOUT", "DISMISSED-EOF",
                        "DISMISSED-MALFORMED", "DISMISSED-SIGINT", "NOT-ASKED"):
        _, _, on_disk = resolve_and_maybe_persist(ABSENT, interaction)
        if on_disk is not ABSENT:
            out.append(f"RT25-D-INV-03 interaction {interaction!r} persisted a "
                       f"policy from the default")
    for interaction, expected in (("ANSWERED-RETAIN", "DURABLE_RETAINED"),
                                  ("ANSWERED-EPHEMERAL", "EPHEMERAL_ONLY")):
        _, _, on_disk = resolve_and_maybe_persist(ABSENT, interaction)
        if on_disk is ABSENT or on_disk.get("posture") != expected:
            out.append(f"RT25-D-INV-03 an ANSWER did not persist "
                       f"{expected}; the ask would then be unable to reach "
                       f"CONSENTED at all")
    if get_path(doc, "$.partC_retentionBounds.boundsRecord."
                     "effectiveBoundsResolution.theDefaultIsNeverWrittenToDisk") \
            is not True:
        out.append("RT25-D-INV-03 theDefaultIsNeverWrittenToDisk is not true")
    if get_path(doc, "$.partC_retentionBounds.boundsRecord."
                     "effectiveBoundsResolution.provenanceIsNeverPersisted") \
            is not True:
        out.append("RT25-D-INV-03 provenanceIsNeverPersisted is not true")
    persisting = get_path(doc, "$.postureResolution.theDefaultIsNeverPersisted."
                               "policyPersistingOutcomesUnchanged")
    v24_persisting = len(get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                              "interactionOutcomes."
                                              "policyPersistingOutcomeIds") or [])
    if _exact_int(persisting) and persisting != v24_persisting:
        out.append(f"RT25-D-INV-03 policyPersistingOutcomesUnchanged declares "
                   f"{persisting!r} and the pinned v24 has {v24_persisting} "
                   f"policy-persisting outcomes")
    return out


def inv_d04(doc, ctx):
    """A durable-authoritative request is refused FOR RETENTION REASONS if and
    only if the effective posture is EPHEMERAL_ONLY."""
    out = []
    for value in (ABSENT, {"posture": "DURABLE_RETAINED"},
                  {"posture": "EPHEMERAL_ONLY"}):
        posture, _ = effective_posture(value)
        outcome = durable_authoritative_outcome(value)
        refused = outcome == "REFUSE"
        if refused != (posture == "EPHEMERAL_ONLY"):
            out.append(f"RT25-D-INV-04 the biconditional fails at {value!r}: "
                       f"posture {posture}, outcome {outcome}")
        if outcome.startswith("PROCEED-EPHEMERAL"):
            out.append(f"RT25-D-INV-04 a durable-authoritative request was "
                       f"DEMOTED at {value!r}, which freeze law 14 forbids")
    statement = str(_invariant_statement(doc, "RT25-D-INV-04"))
    if "FOR RETENTION REASONS" not in statement:
        out.append("RT25-D-INV-04 the restated invariant no longer carries the "
                   "FOR RETENTION REASONS qualifier, so the unqualified 'only "
                   "if' is false on the undecided SIGINT branch again")
    return out


def inv_d05(doc, ctx):
    """The posture enum retains exactly two members and ABSENT is never one."""
    out = []
    members = get_path(doc, "$.postureResolution.theDerivation.postureEnum") or []
    if list(members) != list(POSTURE_ENUM):
        out.append(f"RT25-D-INV-05 the posture enum is {members}, not "
                   f"{list(POSTURE_ENUM)}")
    if ABSENT in members:
        out.append("RT25-D-INV-05 ABSENT has become a posture enum member; every "
                   "consumer would then branch on the state the resolution exists "
                   "to remove")
    v24_members = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                       "policyObject.postureEnum") or []
    if list(v24_members) != list(members):
        out.append(f"RT25-D-INV-05 the enum differs from the pinned v24's "
                   f"{v24_members}, so a member was added or removed")
    return out


def _invariant_statement(doc, iid):
    for entry in (get_path(doc, "$.partC_retentionBounds.invariants") or []):
        if isinstance(entry, dict) and entry.get("id") == iid:
            return entry.get("statement", "")
    return ""


def inv_c15(doc, ctx):
    """Every demand expression is total on Cap and evaluates to 0 at UNBOUNDED.
    The disable behaviour is a value of that dimension's own expression."""
    out = []
    b1 = ctx["b1"]
    if b1["unboundedNonZero"]:
        out.append(f"RT26-C-INV-15 a demand is non-zero at UNBOUNDED: "
                   f"{b1['unboundedNonZero'][:5]}")
    if b1["defaultConfigNonZero"]:
        out.append(f"RT26-C-INV-15 the default configuration evicts at "
                   f"sizes {b1['defaultConfigNonZero'][:8]}")
    if not b1["defaultConfigNonZeroV25"]:
        out.append("RT26-C-INV-15 VACUOUS: the PREDECESSOR's expressions also "
                   "evict nothing at the default, so this invariant is not "
                   "distinguishing the repair from the defect it repairs")
    for entry in (get_path(doc, "$.partC_retentionBounds.sweep.demands.rows")
                  or []):
        if entry.get("isTotalOnCap") is not True:
            out.append(f"RT26-C-INV-15 the {entry.get('dimension')!r} row does "
                       f"not declare isTotalOnCap")
        if entry.get("containsNoBranch") is not True:
            out.append(f"RT26-C-INV-15 the {entry.get('dimension')!r} row does "
                       f"not declare containsNoBranch")
        if entry.get("valueAtUNBOUNDED") != 0:
            out.append(f"RT26-C-INV-15 the {entry.get('dimension')!r} row "
                       f"declares valueAtUNBOUNDED "
                       f"{entry.get('valueAtUNBOUNDED')!r}")
    extensions = get_path(doc, "$.partC_retentionBounds.sweep.demands."
                               "theDisableConvention.extensionsRequired")
    if extensions != 2:
        out.append(f"RT26-C-INV-15 extensionsRequired declares {extensions!r}; "
                   f"this instrument implements exactly two -- (n - UNBOUNDED) "
                   f"below 0 and (now - UNBOUNDED) below every admission time -- "
                   f"and the size dimension needs none")
    for field, expected in (("dimensionsLifted", 3),
                            ("dimensionsWithTheirOwnDisableRule", 0)):
        value = get_path(doc, f"$.partC_retentionBounds.sweep.demands."
                              f"theDisableConvention.{field}")
        if value != expected:
            out.append(f"RT26-C-INV-15 {field} declares {value!r}, expected "
                       f"{expected}")
    return out


def inv_c16(doc, ctx):
    """UNBOUNDED is never admitted, never persisted and never framed."""
    out = []
    for sentinel in ("UNBOUNDED", -1, None, "unbounded"):
        record = _bounds_record()
        record["keepCount"] = sentinel
        if admit_bounds(record)[0] != "REFUSED":
            out.append(f"RT26-C-INV-16 admitted keepCount={sentinel!r} as a "
                       f"sentinel for UNBOUNDED")
    raised = False
    try:
        retention_bounds_id_OVER_CAPS(PROJECT, "rpol1:sha256:" + "0" * 64,
                                       0, 0, 0, 1)
    except RefusedError:
        raised = True
    if not raised:
        out.append("RT26-C-INV-16 an identity over lifted caps was constructible; "
                   "UNBOUNDED has no u64be encoding and must make the preimage "
                   "impossible to build")
    if get_path(doc, "$.partC_retentionBounds.identity."
                     "isComputedOverConfiguredValuesNotLiftedCaps") is not True:
        out.append("RT26-C-INV-16 the identity block no longer declares that it "
                   "is computed over configured values")
    if get_path(doc, "$.partC_retentionBounds.sweep.demands.theDisableConvention."
                     "unboundedIsNotAWireValue.noSentinelIsAdmitted") is not True:
        out.append("RT26-C-INV-16 noSentinelIsAdmitted is not true")
    length_a, _ = retention_bounds_id(PROJECT, "rpol1:sha256:" + "0" * 64,
                                       0, 0, 0, 1)
    length_b, _ = retention_bounds_id(PROJECT, "rpol1:sha256:" + "0" * 64,
                                       0, 104857600, 200, 1)
    if length_a != length_b:
        out.append(f"RT26-C-INV-16 a disabled dimension changed the preimage "
                   f"length ({length_a} vs {length_b}), so a disabled dimension "
                   f"is not framing u64be(0)")
    return out


def resolved_table(doc, ctx):
    """v24's twelve cells with v26's PUBLISHED after-rows substituted for the
    rows it changes.  This is what an implementer would build, and it is what
    RT26-A-INV-17/-18/-19 are evaluated over -- the RESOLVED table, never the
    artifact's description of it."""
    cells = [copy.deepcopy(c) for c in _v24_cells(ctx)]
    for changed in (get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                                  "askDecisionTable.changedCells") or []):
        index = changed.get("index")
        after = changed.get("after")
        if _exact_int(index) and 0 <= index < len(cells) and isinstance(after, dict):
            cells[index] = copy.deepcopy(after)
    outcomes = {o["id"]: copy.deepcopy(o) for o in _v24_outcomes(ctx)}
    for changed in (get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                                  "interactionOutcomes.changed") or []):
        after = changed.get("after")
        if isinstance(after, dict) and after.get("id") in outcomes:
            outcomes[after["id"]] = copy.deepcopy(after)
    return cells, outcomes


def _posture_sensitive_fields(ctx):
    """Step 1, re-derived from v24's own cells: the fields on which the two
    PRESENT postures differ, at any axis."""
    fields = set()
    cells = _v24_cells(ctx)
    for profile in sorted({c["invocationProfile"] for c in cells}):
        for custody in sorted({c["requestedCustody"] for c in cells}):
            eph = _v24_cell(ctx, profile, "PRESENT-EPHEMERAL_ONLY", custody)
            dur = _v24_cell(ctx, profile, "PRESENT-DURABLE_RETAINED", custody)
            if eph is None or dur is None:
                continue
            for key in eph:
                if key == "policyPresence":
                    continue
                if eph.get(key) != dur.get(key):
                    fields.add(key)
    return fields


def _absent_vs_present_durable_fields(ctx):
    """Step 2, re-derived: the fields on which ABSENT and PRESENT-DURABLE_RETAINED
    differ, at any axis."""
    fields = set()
    cells = _v24_cells(ctx)
    for profile in sorted({c["invocationProfile"] for c in cells}):
        for custody in sorted({c["requestedCustody"] for c in cells}):
            absent = _v24_cell(ctx, profile, ABSENT, custody)
            dur = _v24_cell(ctx, profile, "PRESENT-DURABLE_RETAINED", custody)
            if absent is None or dur is None:
                continue
            for key in absent:
                if key == "policyPresence":
                    continue
                if absent.get(key) != dur.get(key):
                    fields.add(key)
    return fields


def inv_a17(doc, ctx):
    """A field v24 computes from policy PRESENCE is unchanged by the posture
    resolution.  Exactly two such fields exist and both are derived by
    SUBTRACTION rather than listed -- so this driver subtracts."""
    out = []
    step1 = _posture_sensitive_fields(ctx)
    step2 = _absent_vs_present_durable_fields(ctx)
    step3 = step2 - step1
    block = get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                          "theOneRuleThatGeneratesAllOfIt."
                          "theExceptionSetIsDerivedNotListed") or {}
    for key, measured in (("step1_postureSensitiveFields", step1),
                          ("step2_fieldsDifferingAbsentVsPresentDurable", step2),
                          ("step3_theExceptionSetIsStep2MinusStep1", step3)):
        declared = block.get(key) or {}
        published = declared.get("measured") or declared.get("fields") or []
        if published and set(published) != measured:
            out.append(
                f"RT26-A-INV-17 {key}: the artifact publishes "
                f"{sorted(published)} and the pinned v24 cells give "
                f"{sorted(measured)}")
    if step3 != {"askPerformed", "firstRunDisclosureEmitted"}:
        out.append(f"RT26-A-INV-17 the subtraction gives {sorted(step3)}, not "
                   f"exactly askPerformed and firstRunDisclosureEmitted")
    # the corroboration: both are pure functions of policy PRESENCE
    for cell in _v24_cells(ctx):
        expected = cell.get("policyPresence") == ABSENT
        if cell.get("firstRunDisclosureEmitted") is not expected:
            out.append(
                f"RT26-A-INV-17 firstRunDisclosureEmitted is not identical to "
                f"(policyPresence == ABSENT) at "
                f"{cell.get('invocationProfile')}/{cell.get('policyPresence')}/"
                f"{cell.get('requestedCustody')}, so a posture-keyed rule COULD "
                f"move it")
    ask_cells = [c for c in _v24_cells(ctx) if c.get("askPerformed") is True]
    if len(ask_cells) != 1:
        out.append(f"RT26-A-INV-17 the pinned v24 has {len(ask_cells)} cells "
                   f"with askPerformed true, not 1")
    for profile in sorted({c["invocationProfile"] for c in _v24_cells(ctx)}):
        for custody in sorted({c["requestedCustody"] for c in _v24_cells(ctx)}):
            eph = _v24_cell(ctx, profile, "PRESENT-EPHEMERAL_ONLY", custody)
            dur = _v24_cell(ctx, profile, "PRESENT-DURABLE_RETAINED", custody)
            if eph and dur and eph.get("askPerformed") != dur.get("askPerformed"):
                out.append(f"RT26-A-INV-17 askPerformed is posture-sensitive at "
                           f"{profile}/{custody}, so it is not an exception")
    # and the resolved table must preserve both counts
    cells, _ = resolved_table(doc, ctx)
    after_ask = sum(1 for c in cells if c.get("askPerformed") is True)
    after_disclosure = sum(1 for c in cells
                           if c.get("firstRunDisclosureEmitted") is True)
    for path, measured in (
            ("$.partA_repairsForcedByThePostureDecision.askDecisionTable."
             "askPerformedCellCountAfter", after_ask),
            ("$.partA_repairsForcedByThePostureDecision.askDecisionTable."
             "firstRunDisclosureEmittedCellCountAfter", after_disclosure)):
        declared = get_path(doc, path)
        if _exact_int(declared) and declared != measured:
            out.append(f"RT26-A-INV-17 {path} declares {declared!r}; the "
                       f"RESOLVED table gives {measured}")
    return out


def inv_a18(doc, ctx):
    """FREEZE LAW 14, AND THE PROPERTY THE WHOLE LINEAGE EXISTS TO PROTECT.

    No cell has outcome PROCEED-DURABLE with durableSourceDerivedWritePermitted
    false, and no row both refuses a request and permits a durable write.
    Evaluated over the RESOLVED table by enumerating every path from a
    DURABLE_AUTHORITATIVE request to a terminal behaviour.
    """
    out = []
    cells, outcomes = resolved_table(doc, ctx)
    durable_cells = [c for c in cells
                     if c.get("requestedCustody") == "DURABLE_AUTHORITATIVE"]
    if len(durable_cells) != 6:
        out.append(f"RT26-A-INV-18 the resolved table has {len(durable_cells)} "
                   f"DURABLE_AUTHORITATIVE cells, not the 6 the lineage models")
    for cell in durable_cells:
        axis = (f"{cell.get('invocationProfile')}/{cell.get('policyPresence')}")
        outcome = cell.get("outcome")
        write = cell.get("durableSourceDerivedWritePermitted")
        if outcome == "PROCEED-DURABLE" and write is not True:
            out.append(
                f"RT26-A-INV-18 SILENT DEMOTION IS REACHABLE at {axis}: outcome "
                f"PROCEED-DURABLE with durableSourceDerivedWritePermitted "
                f"{write!r}. A run reporting PROCEED-DURABLE that writes nothing "
                f"durable is a durability failure reporting authoritative "
                f"success, which freeze law 14 forbids")
        if outcome == "REFUSE" and write is True:
            out.append(
                f"RT26-A-INV-18 the row at {axis} both REFUSES and permits a "
                f"durable write")
        if outcome == "PROCEED-EPHEMERAL":
            out.append(
                f"RT26-A-INV-18 a DURABLE_AUTHORITATIVE request at {axis} "
                f"resolves to PROCEED-EPHEMERAL, which is the demotion itself")
        if outcome == "REFUSE" and cell.get("derivedClass") == "NOT-A-TERMINATION":
            out.append(
                f"RT26-A-INV-18 the row at {axis} refuses without terminating, "
                f"so the refusal is unobservable in the exit contract")
        if outcome not in ("PROCEED-DURABLE", "REFUSE", "ASK"):
            out.append(f"RT26-A-INV-18 unknown outcome {outcome!r} at {axis}; "
                       f"this driver cannot grade it and must not pass it")
    # every interaction outcome reachable from the ask cell
    ask_axis = [c for c in cells if c.get("outcome") == "ASK"]
    for cell in ask_axis:
        if cell.get("durableSourceDerivedWritePermitted") is not False:
            out.append(
                "RT26-A-INV-18 an ASK cell grants a durable write of its own; "
                "the write permission belongs to whichever interaction outcome "
                "follows, and RT24-A-INV-05 permits a durable write only where "
                "the outcome is PROCEED-DURABLE")
    for oid, outcome in sorted(outcomes.items()):
        terminates = outcome.get("terminatesTheRequest")
        klass = outcome.get("derivedClass")
        if terminates is True and klass == "NOT-A-TERMINATION":
            out.append(f"RT26-A-INV-18 {oid} terminates while declaring "
                       f"NOT-A-TERMINATION")
        if terminates is False and klass not in (None, "NOT-A-TERMINATION"):
            out.append(f"RT26-A-INV-18 {oid} does not terminate while declaring "
                       f"a terminating class {klass!r}")
        if terminates is False and outcome.get("policyPersisted") is False \
                and oid.startswith("PA-INT-0") and "DISMISSED" in oid:
            # a non-terminating dismissal must proceed durably under DEFAULTED,
            # which is the only reading that is not a silent demotion
            proceeds = None
            for changed in (get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                                          "interactionOutcomes.changed") or []):
                if changed.get("id") == oid:
                    proceeds = changed.get("afterProceedsUnder")
            if not proceeds or "DURABLE_RETAINED" not in str(proceeds):
                out.append(
                    f"RT26-A-INV-18 {oid} stops terminating and nothing states "
                    f"what it proceeds under. A non-terminating dismissal with "
                    f"no durable write behind it reports success and does less "
                    f"than asked")
    declared = get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                             "interactionOutcomes.writePermissionOnTheAskPath."
                             "soIsThereACellWithOutcomePROCEEDDURABLEAndTheWrite"
                             "FlagFalse")
    measured = any(c.get("outcome") == "PROCEED-DURABLE"
                   and c.get("durableSourceDerivedWritePermitted") is not True
                   for c in cells)
    if declared is not None and declared != measured:
        out.append(f"RT26-A-INV-18 the artifact declares "
                   f"soIsThereACellWithOutcomePROCEEDDURABLEAndTheWriteFlagFalse "
                   f"{declared!r} and the resolved table measures {measured!r}")
    if get_path(doc, "$.postureResolution.lawFourteenPosition."
                     "silentDemotionIsStillForbidden") is not True:
        out.append("RT26-A-INV-18 silentDemotionIsStillForbidden is not true")
    if get_path(doc, "$.postureResolution.lawFourteenPosition."
                     "theDemotionThatIsStillForbidden."
                     "isItReachableUnderTheNewDefault") is not False:
        out.append("RT26-A-INV-18 the artifact no longer declares the demotion "
                   "unreachable")
    return out


NON_TERMINATING_SENTINEL = {"derivedClass": "NOT-A-TERMINATION",
                            "derivedExitCode": -1, "derivedErrorCode": "NONE",
                            "derivedReasonCodes": []}


def inv_a19(doc, ctx):
    """Every Part A row this artifact changes publishes an explicit d9Axes value,
    and a row whose d9Axes is null carries exactly NOT-A-TERMINATION / -1 / NONE
    / [] -- the biconditional measured over all 19 of v24's own rows."""
    out = []
    rows = list(_v24_cells(ctx)) + list(_v24_outcomes(ctx))
    deviations = []
    nulls = objects = 0
    for row in rows:
        axes_null = row.get("d9Axes", "MISSING") is None
        not_a_termination = row.get("derivedClass") == "NOT-A-TERMINATION"
        if axes_null:
            nulls += 1
            for field, value in NON_TERMINATING_SENTINEL.items():
                if row.get(field) != value:
                    deviations.append((row.get("id") or row.get("outcome")
                                       or row.get("invocationProfile"), field,
                                       row.get(field)))
        else:
            objects += 1
        if axes_null != not_a_termination:
            deviations.append((row.get("id") or row.get("invocationProfile"),
                               "biconditional", row.get("derivedClass")))
    if len(rows) != 19:
        out.append(f"RT26-A-INV-19 the pinned v24 population is {len(rows)} rows, "
                   f"not the 19 the biconditional was measured over")
    if deviations:
        out.append(f"RT26-A-INV-19 the biconditional (d9Axes is null) <-> "
                   f"(derivedClass == NOT-A-TERMINATION) deviates on "
                   f"{len(deviations)} row(s): {deviations[:6]}")
    block = get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                          "d9RowsForRowsThatStopTerminating."
                          "theConventionMeasuredOverV24sOwnRows") or {}
    for field, measured in (("rowsMeasured", len(rows)),
                            ("rowsWithNullAxes", nulls),
                            ("rowsWithAnAxesObject", objects),
                            ("deviationCount", len(deviations))):
        if block.get(field) is not None and block.get(field) != measured:
            out.append(f"RT26-A-INV-19 {field} declares {block.get(field)!r}, "
                       f"measured {measured}")
    # every row this artifact CHANGES must publish an explicit d9Axes value
    for changed in (get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                                  "askDecisionTable.changedCells") or []):
        after = changed.get("after")
        if not isinstance(after, dict) or "d9Axes" not in after:
            out.append(f"RT26-A-INV-19 changed cell {changed.get('index')!r} "
                       f"publishes no explicit d9Axes value")
            continue
        if after["d9Axes"] is None:
            for field, value in NON_TERMINATING_SENTINEL.items():
                if after.get(field) != value:
                    out.append(
                        f"RT26-A-INV-19 changed cell {changed.get('index')!r} "
                        f"has null d9Axes and {field} {after.get(field)!r}, not "
                        f"{value!r}")
    for changed in (get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                                  "interactionOutcomes.changed") or []):
        after = changed.get("after")
        if isinstance(after, str):
            continue                     # the deliberately undecided SIGINT row
        if not isinstance(after, dict) or "d9Axes" not in after:
            out.append(f"RT26-A-INV-19 changed outcome {changed.get('id')!r} "
                       f"publishes no explicit d9Axes value")
            continue
        if after["d9Axes"] is None:
            for field, value in NON_TERMINATING_SENTINEL.items():
                if after.get(field) != value:
                    out.append(
                        f"RT26-A-INV-19 changed outcome {changed.get('id')!r} "
                        f"has null d9Axes and {field} {after.get(field)!r}")
    return out


INVARIANT_DRIVERS = {
    "RT25-C-INV-01": inv_c01, "RT25-C-INV-02": inv_c02, "RT25-C-INV-03": inv_c03,
    "RT25-C-INV-04": inv_c04, "RT25-C-INV-05": inv_c05, "RT25-C-INV-06": inv_c06,
    "RT25-C-INV-07": inv_c07, "RT25-C-INV-08": inv_c08, "RT25-C-INV-09": inv_c09,
    "RT25-C-INV-10": inv_c10, "RT25-C-INV-11": inv_c11, "RT25-C-INV-12": inv_c12,
    "RT25-C-INV-13": inv_c13, "RT25-C-INV-14": inv_c14,
    "RT25-D-INV-01": inv_d01, "RT25-D-INV-02": inv_d02, "RT25-D-INV-03": inv_d03,
    "RT25-D-INV-04": inv_d04, "RT25-D-INV-05": inv_d05,
    "RT26-C-INV-15": inv_c15, "RT26-C-INV-16": inv_c16,
    "RT26-A-INV-17": inv_a17, "RT26-A-INV-18": inv_a18, "RT26-A-INV-19": inv_a19,
}


def run_invariants(doc, ctx):
    out = []
    declared = get_path(doc, "$.partC_retentionBounds.invariants") or []
    published = [e.get("id") for e in declared if isinstance(e, dict)]
    missing = [i for i in INVARIANT_IDS if i not in published]
    invented = [i for i in published if i not in INVARIANT_IDS]
    if missing:
        out.append(f"RT26-INV {len(missing)} invariant id(s) this instrument "
                   f"drives are absent from the artifact: {missing}")
    if invented:
        out.append(f"RT26-INV {len(invented)} invariant id(s) present that this "
                   f"instrument does not drive: {invented}; an unexercised "
                   f"invariant must not be counted as coverage")
    if len(published) != len(set(published)):
        out.append("RT26-INV duplicate invariant ids")
    for entry in declared:
        if isinstance(entry, dict) and not str(entry.get("statement", "")).strip():
            out.append(f"RT26-INV {entry.get('id')!r} has an empty statement")
    executed = 0
    for iid in INVARIANT_IDS:
        driver = INVARIANT_DRIVERS[iid]
        executed += 1
        try:
            out.extend(driver(doc, ctx))
        except RefusedError as exc:
            out.append(f"RT26-INV {iid}: a reference derivation refused: {exc}")
        except (KeyError, TypeError, IndexError) as exc:
            out.append(f"RT26-INV {iid}: the driver could not run "
                       f"({type(exc).__name__}: {exc})")
    declared_count = get_path(doc, "$.partC_retentionBounds.invariantCount")
    if _exact_int(declared_count) and declared_count != len(declared):
        out.append(f"RT26-INV invariantCount declares {declared_count!r}, the "
                   f"list holds {len(declared)}")
    report = {"declared": len(declared), "executed": executed}
    ctx["invariantReport"] = report
    return out, report


# ===========================================================================
# SECTION 5 -- THE RECORD, THE PROPERTY PIN, AND THE HARD COMPARISONS.
# ===========================================================================

PLACEHOLDER = re.compile(r"\[[^\]]*\]|^\s*$|^(TBD|TODO|UNSET|UNKNOWN|N/?A|"
                         r"PENDING|XXX)$", re.I)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DECISION_STATUSES = ("DECIDED", "BLOCKED_ON_PHASE_1A", "PENDING", "WITHDRAWN",
                     "SUPERSEDED", "DEFERRED")


def check_record(doc, ctx):
    """The artifact's own authority boundary.  A candidate that promotes itself
    is the §4.4 mechanism, and these are the fields it would promote."""
    out = []
    expectations = {
        "$.artifact": "retention-tiers.v26",
        "$.version": 26,
        "$.claimId": "ARCH.RETENTION-TIERS",
        "$.sealRecommendation": "DO-NOT-SEAL",
        "$.retainedChecker": "NONE",
        "$.authority.candidateState": "NOT-APPLIED",
        "$.authority.authorityClaim": "NONE",
        "$.authority.mayConstituteAProductDecision": False,
        "$.authority.mayAmendD9Vocabulary": False,
        "$.authority.mayAmendOperabilityGates": False,
        "$.authority.mayAmendThreatModel": False,
        "$.authority.mayAmendTheProductDispositionPacket": False,
        "$.authority.mayApplyTheCdRt5AmendmentDraft": False,
        "$.authority.bindsNothing": True,
        "$.integrationState.candidateState": "NOT-APPLIED",
        "$.integrationState.independentAcceptance": "NOT-GRANTED",
        "$.integrationState.V10": "UNRESOLVED",
        "$.freezeDeclaration.constitutesASealOrSignature": False,
        "$.freezeDeclaration.changesAnyStatus": False,
        "$.freezeDeclaration.changesAnyOtherArtifact": False,
        "$.freezeDeclaration.filesEdited": 0,
        "$.freezeDeclaration.unsetFieldsTouched": 0,
        "$.v10Item3Position.claimedStatusForTheseBytes": "NO CLAIM MADE",
    }
    for path, expected in expectations.items():
        value = get_path(doc, path, "<<ABSENT>>")
        if value != expected or type(value) is not type(expected):
            out.append(f"RT26-RECORD {path} is {value!r}, expected {expected!r}")
    status = get_path(doc, "$.status")
    if not isinstance(status, str) or "CANDIDATE-NOT-APPLIED" not in status:
        out.append(f"RT26-RECORD $.status is {status!r}; this artifact is a "
                   f"candidate and a status that reads as applied or accepted is "
                   f"the §4.4 mechanism -- a recommendation converted into "
                   f"accomplished acceptance")
    # $.retainedChecker is NONE and stays NONE.  THIS FILE DOES NOT CHANGE IT.
    # §7.2 forbids editing reviewed bytes, so the field remains true of the
    # artifact and the residual RT25-RES-01 remains live against it.  What this
    # instrument narrows is the MEASURED half of the residual, and
    # check_residual_measurements reports the narrowing without asserting the
    # artifact says so.
    if get_path(doc, "$.supersedesAsArchitectureCandidate") is None:
        out.append("RT26-RECORD $.supersedesAsArchitectureCandidate is absent")
    lineage = str(get_path(doc, "$.supersedesAsArchitectureCandidate") or "")
    if "retention-tiers.v24" not in lineage:
        out.append("RT26-RECORD the supersession statement no longer says the "
                   "named architecture head remains retention-tiers.v24, so a "
                   "reader could take this candidate for the head")
    return out


def check_cd_rt_5(doc, ctx):
    """THE PROPERTY PIN.  Section 7.10, implemented rather than quoted.

    Nothing here asserts what CD-RT-5's state IS.  It asserts that whatever the
    live packet says is well-formed, attributed, internally consistent, and
    consistent with what this artifact says about it.  A legitimate amendment
    costs a re-read; a fabrication, a silent reversion or an unfilled placeholder
    fails.
    """
    out = []
    packet = ctx["product"]
    decided = get_path(packet, "$.decisions.CD-RT-5")
    pending = get_path(packet, "$.pendingDecisions.CD-RT-5")
    if decided is None and pending is None:
        out.append("RT26-CDRT5 the binding packet carries no CD-RT-5 row at all, "
                   "in $.decisions or $.pendingDecisions. The decision this whole "
                   "Phase-1A effort waited for has been DELETED rather than "
                   "amended")
        return out
    if decided is not None and pending is not None:
        out.append("RT26-CDRT5 the packet carries CD-RT-5 in BOTH $.decisions "
                   "and $.pendingDecisions, so two readers get two answers")
    row = decided if decided is not None else pending
    status = row.get("status")
    if not isinstance(status, str) or status not in DECISION_STATUSES:
        out.append(f"RT26-CDRT5 status {status!r} is outside the closed "
                   f"vocabulary {list(DECISION_STATUSES)}")
    if isinstance(status, str) and PLACEHOLDER.match(status.strip()):
        out.append(f"RT26-CDRT5 status {status!r} is a placeholder")

    if status == "DECIDED":
        for field in ("decidedBy", "decidedOn"):
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                out.append(f"RT26-CDRT5 a DECIDED row whose {field} is "
                           f"{value!r}. §4.4 is this corpus's forensic record of "
                           f"a fabricated authority attribution; an unfilled "
                           f"amendment must never read as a taken decision")
                continue
            if PLACEHOLDER.match(value.strip()):
                out.append(f"RT26-CDRT5 {field} is the placeholder {value!r}; a "
                           f"bracketed name or date is an UNFILLED amendment "
                           f"reading as a taken decision")
        if isinstance(row.get("decidedOn"), str) and not ISO_DATE.match(
                row["decidedOn"].strip()):
            out.append(f"RT26-CDRT5 decidedOn {row['decidedOn']!r} is not an ISO "
                       f"calendar date, so 'a real date' cannot be checked")
    else:
        for field in ("decidedBy", "decidedOn"):
            if row.get(field):
                out.append(f"RT26-CDRT5 the row is {status!r} and yet carries "
                           f"{field}={row.get(field)!r}; an attribution without a "
                           f"decision is the §4.4 shape in the other direction")

    # the artifact's six statements of that state, hard-compared to the packet
    artifact_state = {
        "$.cdRt5DecisionRecord.state": row.get("status"),
        "$.cdRt5DecisionRecord.decidedOn": row.get("decidedOn"),
        "$.cdRt5DecisionRecord.decidedBy": row.get("decidedBy"),
        "$.productAuthorityBoundary.packetStateAsMeasured": row.get("status"),
    }
    for path, expected in artifact_state.items():
        value = get_path(doc, path)
        if value != expected:
            out.append(f"RT26-CDRT5 {path} says {value!r} and the LIVE packet "
                       f"says {expected!r}. A silent reversion in either "
                       f"direction is what this comparison exists to catch")
    for path in ("$.integrationState.CD-RT-5", "$.productAuthorityBoundary.CD-RT-5"):
        value = str(get_path(doc, path) or "")
        if row.get("status") and row["status"] not in value:
            out.append(f"RT26-CDRT5 {path} reads {value!r} and does not carry the "
                       f"live packet status {row['status']!r}")
        if row.get("decidedBy") and row["decidedBy"] not in value:
            out.append(f"RT26-CDRT5 {path} reads {value!r} and does not name the "
                       f"live authority {row['decidedBy']!r}")

    # the posture fields must agree with each other, in both documents
    posture_pairs = (
        ("$.productAuthorityBoundary.durableDefault",
         "$.defaultPosture.durableDefault"),
        ("$.productAuthorityBoundary.implicitDurableRetention",
         "$.defaultPosture.implicitDurableRetention"),
    )
    for artifact_path, packet_path in posture_pairs:
        mine = get_path(doc, artifact_path)
        theirs = get_path(row, packet_path)
        if mine != theirs:
            out.append(f"RT26-CDRT5 {artifact_path} is {mine!r} and the live "
                       f"packet's {packet_path} is {theirs!r}; the posture "
                       f"fields do not agree")
        if isinstance(mine, str) and PLACEHOLDER.match(mine.strip()):
            out.append(f"RT26-CDRT5 {artifact_path} is a placeholder {mine!r}")
    if get_path(doc, "$.closedRecordExtension.durableDefaultInThePacketIsNow") \
            != get_path(row, "$.defaultPosture.durableDefault"):
        out.append("RT26-CDRT5 $.closedRecordExtension."
                   "durableDefaultInThePacketIsNow disagrees with the live packet")

    # every quoted decision field, re-extracted from the LIVE packet by DERIVING
    # the packet field name from the artifact's own key.  No table here maps
    # them, so a renamed quotation is caught rather than skipped.
    terms = get_path(doc, "$.cdRt5DecisionRecord.theTermsAsDecided") or {}
    checked = 0
    for key, value in terms.items():
        if not key.endswith("Verbatim") or not isinstance(value, str):
            continue
        checked += 1
        field = key[: -len("Verbatim")]
        found = [v for p, v in scalar_leaves(row)
                 if leaf_name(p) == field and isinstance(v, str)]
        if not found:
            out.append(f"RT26-CDRT5 $.cdRt5DecisionRecord.theTermsAsDecided.{key} "
                       f"quotes a packet field named {field!r} that the live "
                       f"CD-RT-5 row does not have")
            continue
        if not any(fold(value) == fold(candidate) for candidate in found):
            if any(fold(value) in fold(candidate) for candidate in found):
                out.append(f"RT26-CDRT5 {key} is a PARTIAL quotation of "
                           f"{field!r} while quotedSpan declares "
                           f"COMPLETE-FIELD-VALUE")
            else:
                out.append(f"RT26-CDRT5 {key} does not match the live packet's "
                           f"{field!r}. Quoted: {_norm(value)[:120]!r}; live: "
                           f"{_norm(found[0])[:120]!r}")
    if checked < 9:
        out.append(f"RT26-CDRT5 only {checked} quoted decision field(s) were "
                   f"found to re-extract; the artifact quotes nine and a "
                   f"shrinking quotation set is a shrinking check")
    ctx["cdRt5Quoted"] = checked
    ctx["cdRt5Status"] = row.get("status")
    if get_path(doc, "$.cdRt5DecisionRecord.theTermsAsDecided.quotedNotParaphrased") \
            is not True:
        out.append("RT26-CDRT5 quotedNotParaphrased is not true")
    # the packet digest the artifact records is RECORDED, not gated: compare and
    # report, never refuse.
    recorded = get_path(doc, "$.productAuthorityBoundary.packetDigestAtMeasurement")
    live = sha_bytes(ctx["snaps"]["artifacts/product-dispositions.v1.json"])
    if recorded != live:
        ctx.setdefault("notices", []).append(
            f"RT26-PACKET-ADVANCED the artifact records the packet at "
            f"{str(recorded)[:16]}... and it is live at {live[:16]}.... NOT A "
            f"FINDING: this instrument pins the packet's CONTENT, not its digest, "
            f"and every field above was re-extracted from the live bytes")
    return out


def check_recorded_inputs(doc, ctx):
    """The artifact's recorded input set, and the classification this instrument
    implements, compared in BOTH directions."""
    out = []
    rows = get_path(doc, "$.recordedInputs.recorded") or []
    declared = get_path(doc, "$.recordedInputs.digestsRecordedCount")
    if _exact_int(declared) and declared != len(rows):
        out.append(f"RT26-INPUTS digestsRecordedCount declares {declared!r} and "
                   f"the list holds {len(rows)}")
    gated_here = set(GATED_PINS)
    advancing_here = set(ADVANCING_PINS)
    gated_there, advancing_there = set(), set()
    for row in rows:
        path = str(row.get("path", ""))
        gate = str(row.get("gate", ""))
        digest = row.get("sha256")
        base = pathlib.PurePosixPath(path).name
        if gate.startswith("HARD-PIN"):
            gated_there.add(base)
            expected = GATED_PINS.get(base)
            if expected is None:
                out.append(f"RT26-INPUTS {path} is gated by the artifact and is "
                           f"NOT in this instrument's GATED table, so a hard pin "
                           f"the artifact declares is not being enforced")
            elif expected != digest:
                out.append(f"RT26-INPUTS {path}: the artifact records {digest!r} "
                           f"and this instrument gates {expected!r}")
        elif gate.startswith("CITED-DIGEST-RECORDED-NOT-GATED"):
            advancing_there.add(path)
            expected = ADVANCING_PINS.get(path)
            if expected is None:
                out.append(f"RT26-INPUTS {path} is cited-not-gated by the "
                           f"artifact and is absent from this instrument's "
                           f"ADVANCING table")
            elif expected != digest:
                out.append(f"RT26-INPUTS {path}: the artifact records {digest!r} "
                           f"and this instrument's ADVANCING baseline is "
                           f"{expected!r}")
        else:
            out.append(f"RT26-INPUTS {path} carries an unknown gate {gate!r}; "
                       f"this instrument implements the artifact's two classes "
                       f"and cannot grade a third")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            out.append(f"RT26-INPUTS {path} records {digest!r}, which is not a "
                       f"lowercase sha256")
    for name in gated_here - gated_there:
        out.append(f"RT26-INPUTS this instrument gates {name!r}, which the "
                   f"artifact does not record as a HARD-PIN row; the "
                   f"classification must come from the artifact, not from here")
    for path in advancing_here - advancing_there:
        out.append(f"RT26-INPUTS this instrument classes {path!r} ADVANCING and "
                   f"the artifact does not record it as cited-not-gated")
    if get_path(doc, "$.recordedInputs.duplicateKeysFound") != 0:
        out.append("RT26-INPUTS duplicateKeysFound is not 0, yet every input was "
                   "parsed here under a duplicate-key-rejecting hook and none "
                   "raised")
    if get_path(doc, "$.recordedInputs.noInputWasWritten") is not True:
        out.append("RT26-INPUTS noInputWasWritten is not true")
    if get_path(doc, "$.recordedInputs.filesWrittenByThisArtifact") != 1:
        out.append("RT26-INPUTS filesWrittenByThisArtifact is not 1")
    # the plan digest, which the artifact quotes as a verbatim value
    quoted = get_path(doc, "$.recordedInputs.citedDigestsThatMovedDuringAuthoring."
                           "planDigestVerbatim")
    live_plan = measured_digest("ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md")
    if quoted is not None and live_plan is not None and quoted != live_plan:
        ctx.setdefault("notices", []).append(
            f"RT26-PLAN-ADVANCED planDigestVerbatim records {str(quoted)[:16]}... "
            f"and the live plan is {live_plan[:16]}.... The artifact classes this "
            f"file cited-not-gated; reported, not a finding")
    return out


def _self_referential_counts(doc, ctx):
    """Every count this artifact publishes ABOUT ITS OWN BYTES, paired with the
    thing it counts.  These can never legitimately advance -- the bytes are
    frozen -- so §7.2.2 gives every one of them a hard comparison.  Counts about
    the surrounding TREE are deliberately NOT in this table; they are reported as
    notices, because the tree is what the corpus is waiting to change."""
    pc = "$.partC_retentionBounds"
    a = "$.partA_repairsForcedByThePostureDecision"
    pairs = [
        ("$.retainedResidualCount", len(get_path(doc, "$.retainedResiduals") or [])),
        ("$.newResidualCount", len(get_path(doc, "$.newResiduals") or [])),
        ("$.declaredDependencyCount",
         len(get_path(doc, "$.declaredDependencies") or [])),
        ("$.retainedResidualsWhoseBasisMovedCount",
         len(get_path(doc, "$.retainedResidualsWhoseBasisMoved") or [])),
        (f"{pc}.invariantCount", len(get_path(doc, f"{pc}.invariants") or [])),
        (f"{pc}.vectors.count", len(get_path(doc, f"{pc}.vectors.rows") or [])),
        (f"{pc}.vectors.negativeControlCount",
         sum(1 for r in (get_path(doc, f"{pc}.vectors.rows") or [])
             if r.get("isNegativeControl") is True)),
        (f"{pc}.vectors.nonControlRowCount",
         sum(1 for r in (get_path(doc, f"{pc}.vectors.rows") or [])
             if r.get("isNegativeControl") is not True)),
        (f"{pc}.causeVocabulary.closedPartitions[0].memberCount",
         len(get_path(doc, f"{pc}.causeVocabulary.closedPartitions[0].members")
             or [])),
        (f"{pc}.identity.encoderControl.goldensAttempted",
         len(get_path(doc, f"{pc}.identity.encoderControl.rows") or [])),
        ("$.derivationFromThePredecessor.operationCount",
         len(get_path(doc, "$.derivationFromThePredecessor.operations") or [])),
        ("$.quotationDiscipline.sourceCount",
         len(get_path(doc, "$.quotationDiscipline.sourcesSearched") or [])),
        ("$.recordedInputs.digestsRecordedCount",
         len(get_path(doc, "$.recordedInputs.recorded") or [])),
        ("$.inheritance.surfacesChangedCount",
         len(get_path(doc, "$.inheritance.surfacesThisArtifactChanges") or [])),
        ("$.inheritance.surfacesExplicitlyUnchangedCount",
         len(get_path(doc, "$.inheritance.surfacesThisArtifactDoesNotChange")
             or [])),
        ("$.inheritance.exhaustivePartitionOfV24.partAKeyCount",
         len(get_path(doc, "$.inheritance.exhaustivePartitionOfV24.partA") or [])),
        ("$.inheritance.exhaustivePartitionOfV24.partBKeyCount",
         len(get_path(doc, "$.inheritance.exhaustivePartitionOfV24.partB") or [])),
        ("$.freezeDeclaration.frozenArtifactCount",
         len(get_path(doc, "$.freezeDeclaration.frozenArtifacts") or [])),
        (f"{a}.noAskCasesReDerivedCount",
         len(get_path(doc, f"{a}.noAskCasesReDerived") or [])),
        (f"{a}.noAskCaseCount", len(get_path(doc, f"{a}.noAskCasesReDerived") or [])),
        (f"{a}.askDecisionTable.cellsSelectedByTheRule",
         len(get_path(doc, f"{a}.askDecisionTable.changedCells") or [])),
        (f"{a}.interactionOutcomes.outcomesChanged",
         len(get_path(doc, f"{a}.interactionOutcomes.changed") or [])),
        (f"{a}.interactionOutcomes.outcomesUnchanged",
         len(get_path(doc, f"{a}.interactionOutcomes.unchanged") or [])),
        ("$.newResiduals[0].measuredValues.vectorsDeclared",
         len(get_path(doc, f"{pc}.vectors.rows") or [])),
        ("$.newResiduals[0].measuredValues.invariantsDeclared",
         len(get_path(doc, f"{pc}.invariants") or [])),
        ("$.corpusResiduals[0].measuredValues.recordedInputs",
         len(get_path(doc, "$.recordedInputs.recorded") or [])),
        ("$.quotationDiscipline.verbatimFieldsInTheseBytes",
         ctx.get("verbatimStringKeys", -1)),
        ("$.quotationDiscipline.verifiedAgainstTheirAttributedSource",
         ctx.get("verbatimVerified", -1)),
        ("$.quotationDiscipline.notFoundInTheirAttributedSource",
         ctx.get("verbatimNotFound", -1)),
    ]
    return pairs


def check_counts(doc, ctx):
    """§7.2.2: a recorded measurement gets a HARD COMPARISON.  An uncompared
    measurement is prose that looks like evidence, and going stale is a TRUE
    POSITIVE about these bytes rather than a false alarm."""
    out = []
    for path, measured in _self_referential_counts(doc, ctx):
        if measured < 0:
            continue                     # the producer did not run this pass
        declared = get_path(doc, path, "<<ABSENT>>")
        if declared == "<<ABSENT>>":
            out.append(f"RT26-COUNT {path} is absent, so a published count this "
                       f"instrument compares has been deleted rather than "
                       f"corrected")
            continue
        if not _exact_int(declared):
            out.append(f"RT26-COUNT {path} is {declared!r} "
                       f"({type(declared).__name__}), not a JSON integer")
            continue
        if declared != measured:
            out.append(f"RT26-COUNT {path} declares {declared} and these bytes "
                       f"measure {measured}. §7.2.2 gives a recorded measurement "
                       f"a hard comparison, and this is a measurement about the "
                       f"artifact's own contents, which can never legitimately "
                       f"advance")
    # the boundary sentence beside the count, which restates the same figure
    boundary = str(get_path(doc, "$.corpusResiduals[0].measuredBoundary") or "")
    rows = len(get_path(doc, "$.recordedInputs.recorded") or [])
    match = re.match(r"\s*(\d+)\s+inputs recorded", boundary)
    if match and int(match.group(1)) != rows:
        out.append(
            f"RT26-COUNT $.corpusResiduals[0].measuredBoundary reads "
            f"{boundary[:70]!r} while these bytes record {rows} inputs. A wrong "
            f"figure in a document is a defect; the same wrong figure restated "
            f"in prose beside its own field is the §7.2.2 stale-figure class")
    # the two delta statements the artifact invites a reader to cross-check
    surfaces = get_path(doc, "$.inheritance.surfacesThisArtifactChanges") or []
    tops = set()
    for entry in surfaces:
        surface = str(entry.get("surface", ""))
        parts = surface.split(" ")[0].split(".")
        if len(parts) >= 3:
            tops.add(parts[1] + "." + parts[2])
    changed_rows = [r for r in ((get_path(doc, "$.inheritance."
                                               "exhaustivePartitionOfV24.partA")
                                 or [])
                                + (get_path(doc, "$.inheritance."
                                                 "exhaustivePartitionOfV24.partB")
                                   or []))
                    if r.get("disposition") == "CHANGED"]
    if len(tops) != len(changed_rows):
        out.append(
            f"RT26-COUNT the 9 changed surface paths reduce to {len(tops)} "
            f"distinct top-level keys and the exhaustive partition marks "
            f"{len(changed_rows)} CHANGED; the artifact publishes both and asks "
            f"a reader to check them against each other")
    return out


def check_census(doc, ctx):
    """The leaf census, RE-WALKED from the parsed bytes, bool before int, with
    the int-first control published so the ordering bug is visible if
    reintroduced."""
    out = []
    result = census(doc)
    counts = result["counts"]
    declared = {
        "scalarLeafPositions": counts["scalar"],
        "nonStringLeafPositions": counts["nonString"],
        "intLeafPositions": counts["int"],
        "boolLeafPositions": counts["bool"],
        "floatLeafPositions": counts["float"],
        "nullLeafPositions": counts["null"],
        "stringLeafPositions": counts["str"],
    }
    for field, measured in declared.items():
        value = get_path(doc, f"$.leafCensus.{field}", "<<ABSENT>>")
        if value != measured:
            out.append(f"RT26-CENSUS $.leafCensus.{field} declares {value!r} and "
                       f"a re-walk of these bytes measures {measured}")
    if counts["int"] + counts["bool"] + counts["float"] + counts["null"] \
            != counts["nonString"]:
        out.append("RT26-CENSUS the published arithmetic does not close")
    if result["control"]["intFirstInt"] != counts["int"] + counts["bool"] \
            or result["control"]["intFirstBool"] != 0:
        out.append("RT26-CENSUS the int-first control did not behave as the "
                   "ordering bug would; the control is not controlling anything")
    for field, measured in (("floatLeafPaths", result["floatLeafPaths"]),
                            ("nullLeafPaths", result["nullLeafPaths"])):
        published = get_path(doc, f"$.leafCensus.{field}")
        if published is None:
            out.append(f"RT26-CENSUS $.leafCensus.{field} is absent")
        elif sorted(published) != measured:
            out.append(f"RT26-CENSUS $.leafCensus.{field} publishes "
                       f"{sorted(published)[:4]} and these bytes carry "
                       f"{measured[:4]}")
    for path in result["nullLeafPaths"]:
        if leaf_name(path) != "d9Axes":
            out.append(f"RT26-CENSUS {path} is a null leaf that is not a d9Axes "
                       f"value, so 'every null is a declared absence of a "
                       f"termination' is false")
    for path in result["floatLeafPaths"]:
        row = get_path(doc, path.rsplit(".bounds.", 1)[0] + ".id") \
            if ".bounds." in path else None
        if row != "PC-V-07-EXACT-TYPE-FLOAT":
            out.append(f"RT26-CENSUS {path} is a float leaf outside "
                       f"PC-V-07-EXACT-TYPE-FLOAT")
    if get_path(doc, "$.leafCensus.walkedFrom") != "WRITTEN-BYTES":
        out.append("RT26-CENSUS $.leafCensus.walkedFrom is not WRITTEN-BYTES; "
                   "§7.2.2 records four measured instances of a census computed "
                   "before the self-report was attached, each undercounting by "
                   "exactly the size of its own self-report")
    if get_path(doc, "$.leafCensus.censusIncludesItsOwnIntegers") is not True:
        out.append("RT26-CENSUS censusIncludesItsOwnIntegers is not true")
    method = str(get_path(doc, "$.leafCensus.method") or "").lower()
    if "bool is tested before int" not in method:
        out.append("RT26-CENSUS the census method no longer states that bool is "
                   "tested before int, which is the ordering the control exists "
                   "to prove was used")
    # the predecessor census, recomputed from the PINNED v25 bytes
    v25_counts = census(ctx["v25"])["counts"]
    published = get_path(doc, "$.leafCensus.predecessorCensusForComparison") or {}
    for field, key in (("scalarLeafPositions", "scalar"),
                       ("nonStringLeafPositions", "nonString"),
                       ("intLeafPositions", "int"), ("boolLeafPositions", "bool"),
                       ("floatLeafPositions", "float"),
                       ("nullLeafPositions", "null"),
                       ("stringLeafPositions", "str")):
        if field in published and published[field] != v25_counts[key]:
            out.append(f"RT26-CENSUS predecessorCensus.{field} declares "
                       f"{published[field]!r} and the pinned v25 bytes measure "
                       f"{v25_counts[key]}")
    return out


def check_partition(doc, ctx):
    """B3.  The exhaustive partition of v24's Part A and Part B top-level keys,
    RE-DERIVED from v24's bytes.  A driver that hardcoded '35' would pass on a
    successor that partitioned nothing."""
    out = []
    block = get_path(doc, "$.inheritance.exhaustivePartitionOfV24") or {}
    for root, key in (("partA_firstRunRetentionConsent", "partA"),
                      ("partB_purgeSemantics", "partB")):
        actual = set(get_path(ctx["v24"], f"${'.' + root}") or {})
        rows = block.get(key) or []
        named = []
        for row in rows:
            path = str(row.get("key", ""))
            prefix = f"$.{root}."
            if path.startswith(prefix):
                named.append(path[len(prefix):].split(".")[0])
            elif path:
                out.append(f"RT26-B3 partition row {path!r} is not a top-level "
                           f"key of $.{root}")
            if row.get("disposition") not in ("CHANGED", "UNCHANGED"):
                out.append(f"RT26-B3 partition row {path!r} has disposition "
                           f"{row.get('disposition')!r}, outside the two-member "
                           f"partition")
        missing = sorted(actual - set(named))
        invented = sorted(set(named) - actual)
        duplicated = sorted({k for k in named if named.count(k) > 1})
        if missing:
            out.append(f"RT26-B3 {len(missing)} of {len(actual)} top-level "
                       f"$.{root} keys of the pinned v24 appear in NO partition "
                       f"row: {missing}. An incomplete delta over an unread "
                       f"predecessor is worse than a copy, because the reader "
                       f"cannot notice the omission")
        if invented:
            out.append(f"RT26-B3 the partition names {len(invented)} $.{root} "
                       f"key(s) the pinned v24 does not have: {invented}")
        if duplicated:
            out.append(f"RT26-B3 duplicated partition row(s) for {duplicated}")
        declared = block.get(f"{key}KeyCount")
        if _exact_int(declared) and declared != len(actual):
            out.append(f"RT26-B3 {key}KeyCount declares {declared!r} and the "
                       f"pinned v24 has {len(actual)}")
    total = len(get_path(ctx["v24"], "$.partA_firstRunRetentionConsent") or {}) \
        + len(get_path(ctx["v24"], "$.partB_purgeSemantics") or {})
    if _exact_int(block.get("totalKeyCount")) and block["totalKeyCount"] != total:
        out.append(f"RT26-B3 totalKeyCount declares {block['totalKeyCount']!r} "
                   f"and the pinned v24 has {total}")
    if block.get("keysInNeitherList") != 0:
        out.append(f"RT26-B3 keysInNeitherList is {block.get('keysInNeitherList')!r}; "
                   f"the whole repair is that there is no residual class")
    rows = (block.get("partA") or []) + (block.get("partB") or [])
    changed = sum(1 for r in rows if r.get("disposition") == "CHANGED")
    unchanged = sum(1 for r in rows if r.get("disposition") == "UNCHANGED")
    for field, measured in (("changedKeyCount", changed),
                            ("unchangedKeyCount", unchanged)):
        if field in block and block[field] != measured:
            out.append(f"RT26-B3 {field} declares {block[field]!r}, measured "
                       f"{measured}")
    if changed + unchanged != total:
        out.append(f"RT26-B3 the two dispositions sum to {changed + unchanged} "
                   f"and the key set has {total} members")
    # every named changed surface must resolve in the pinned v24
    for entry in (get_path(doc, "$.inheritance.surfacesThisArtifactChanges")
                  or []):
        surface = str(entry.get("surface", "")).split(" ")[0]
        if surface.startswith("$.part") and get_path(ctx["v24"], surface,
                                                     "<<ABSENT>>") == "<<ABSENT>>":
            out.append(f"RT26-B3 surfacesThisArtifactChanges names {surface!r}, "
                       f"which does not resolve in the pinned v24")
    return out


def check_part_a_prime(doc, ctx):
    """Every published before-row is a CLAIM ABOUT v24'S BYTES, and is
    hard-compared against them field by field."""
    out = []
    a = "$.partA_repairsForcedByThePostureDecision"
    cells = _v24_cells(ctx)
    outcomes = {o["id"]: o for o in _v24_outcomes(ctx)}
    before_rows = 0
    mismatches = 0
    extra_fields = []

    for changed in (get_path(doc, f"{a}.askDecisionTable.changedCells") or []):
        index = changed.get("index")
        if not _exact_int(index) or not 0 <= index < len(cells):
            out.append(f"RT26-A index {index!r} is not a cell of the pinned v24 "
                       f"table")
            continue
        source = cells[index]
        before = changed.get("before")
        if not isinstance(before, dict):
            out.append(f"RT26-A changed cell {index} publishes no before-row")
            continue
        before_rows += 1
        for key, value in before.items():
            if key not in source:
                extra_fields.append(f"changedCells[{index}].before.{key}")
            elif source[key] != value:
                mismatches += 1
                out.append(f"RT26-A changedCells index {index} before.{key} is "
                           f"{value!r} and the pinned v24 cell has "
                           f"{source[key]!r}. A 'before' row is a claim about the "
                           f"predecessor's bytes")
        after = changed.get("after") or {}
        declared_changed = set(changed.get("fieldsChanged") or [])
        measured_changed = {k for k in after
                            if k in source and after[k] != source[k]}
        if declared_changed != measured_changed:
            out.append(f"RT26-A changedCells index {index}: fieldsChanged "
                       f"declares {sorted(declared_changed)} and the after-row "
                       f"differs from the pinned v24 cell on "
                       f"{sorted(measured_changed)}")
        if changed.get("fieldsChangedCount") != len(measured_changed):
            out.append(f"RT26-A changedCells index {index}: fieldsChangedCount "
                       f"declares {changed.get('fieldsChangedCount')!r}, measured "
                       f"{len(measured_changed)}")
        if changed.get("everyChangedFieldIsPostureSensitiveInV24") is True:
            sensitive = _posture_sensitive_fields(ctx)
            stray = measured_changed - sensitive
            if stray:
                out.append(f"RT26-A changedCells index {index} claims every "
                           f"changed field is posture-sensitive in v24 and "
                           f"{sorted(stray)} is not")

    for changed in (get_path(doc, f"{a}.interactionOutcomes.changed") or []):
        oid = changed.get("id")
        source = outcomes.get(oid)
        if source is None:
            out.append(f"RT26-A interaction outcome {oid!r} is not an outcome of "
                       f"the pinned v24")
            continue
        before = changed.get("before")
        if not isinstance(before, dict):
            out.append(f"RT26-A changed outcome {oid} publishes no before-row")
            continue
        before_rows += 1
        for key, value in before.items():
            if key not in source:
                extra_fields.append(f"interactionOutcomes.{oid}.before.{key}")
            elif source[key] != value:
                mismatches += 1
                out.append(f"RT26-A outcome {oid} before.{key} is {value!r} and "
                           f"the pinned v24 has {source[key]!r}")
        if changed.get("terminatesBefore") != source.get("terminatesTheRequest"):
            out.append(f"RT26-A outcome {oid}: terminatesBefore is "
                       f"{changed.get('terminatesBefore')!r} and the pinned v24 "
                       f"says {source.get('terminatesTheRequest')!r}")

    if extra_fields:
        out.append(
            f"RT26-A {len(extra_fields)} field(s) appear in a row labelled "
            f"'before' and are absent from the pinned v24 row it describes: "
            f"{extra_fields}. No value is misstated -- a field is ADDED -- but "
            f"the placement in a before-row makes it a claim about the "
            f"predecessor")
    if before_rows == 0:
        out.append("RT26-A VACUOUS: no before-row was found to compare, so this "
                   "driver measured nothing")

    # the counts the block publishes about the RESOLVED table
    resolved_cells, resolved_outcomes = resolved_table(doc, ctx)
    selected = [c.get("index") for c in
                (get_path(doc, f"{a}.askDecisionTable.changedCells") or [])]
    declared_indices = get_path(doc, f"{a}.askDecisionTable.selectedCellIndices")
    if declared_indices is not None and list(declared_indices) != list(selected):
        out.append(f"RT26-A selectedCellIndices declares {declared_indices} and "
                   f"the changedCells rows are at {selected}")
    derived = [i for i, c in enumerate(cells)
               if c.get("policyPresence") == ABSENT
               and c.get("requestedCustody") == "DURABLE_AUTHORITATIVE"]
    if list(selected) != derived:
        out.append(f"RT26-A the rule selects the ABSENT / DURABLE_AUTHORITATIVE "
                   f"cells of the pinned v24, which are {derived}; the artifact "
                   f"publishes changed cells at {selected}")
    with_changes = [c.get("index") for c in
                    (get_path(doc, f"{a}.askDecisionTable.changedCells") or [])
                    if c.get("fieldsChangedCount")]
    for field, measured in (
            ("cellsWithAtLeastOneChangedFieldValue", len(with_changes)),
            ("cellsWithNoChangedFieldValue", len(cells) - len(with_changes))):
        declared = get_path(doc, f"{a}.askDecisionTable.{field}")
        if _exact_int(declared) and declared != measured:
            out.append(f"RT26-A {field} declares {declared!r}, measured "
                       f"{measured}")
    persisting = [oid for oid, o in resolved_outcomes.items()
                  if o.get("policyPersisted") is True]
    declared_persisting = get_path(doc, f"{a}.interactionOutcomes."
                                        f"policyPersistingOutcomeIdsAfter") or []
    if sorted(persisting) != sorted(declared_persisting):
        out.append(f"RT26-A policyPersistingOutcomeIdsAfter declares "
                   f"{sorted(declared_persisting)} and the resolved table gives "
                   f"{sorted(persisting)}")
    if get_path(doc, f"{a}.noAskCasesSilentlyDeleted") != 0:
        out.append("RT26-A noAskCasesSilentlyDeleted is not 0")
    v24_cases = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                     "noAskCases") or []
    if len(get_path(doc, f"{a}.noAskCasesReDerived") or []) != len(v24_cases):
        out.append(f"RT26-A the pinned v24 has {len(v24_cases)} noAskCases and "
                   f"this artifact re-derives "
                   f"{len(get_path(doc, f'{a}.noAskCasesReDerived') or [])}")
    return out


def check_exception_set_closure(doc, ctx):
    """IR-RT26-N01, MECHANISED.

    The artifact declares its exception set DERIVED BY SUBTRACTION and closed,
    with exceptionsDiscoveredByInspection 0.  This driver RESOLVES the published
    rule plus that exception set against v24's own cells and compares the result
    to the artifact's own published after-rows.  Any field the resolution moves
    that the artifact holds at v24's value is an exception the subtraction did
    not find, and the count of them is what exceptionsDiscoveredByInspection
    claims to be zero.

    §7.2.2 gives that figure a hard comparison.  The review graded the resulting
    divergence NON-BLOCKING because it moves no published value and its direction
    rescues the ask -- and said expressly that a reader who trusts
    soTheExceptionsAreDerived and re-derives the rule for a row the enumeration
    does not cover gets the wrong answer.  Mechanising it is what stops a future
    successor leaving it unstated.
    """
    out = []
    a = "$.partA_repairsForcedByThePostureDecision"
    block = get_path(doc, f"{a}.theOneRuleThatGeneratesAllOfIt") or {}
    exception_block = block.get("theExceptionSetIsDerivedNotListed") or {}
    exceptions = set(
        (exception_block.get("step3_theExceptionSetIsStep2MinusStep1") or {})
        .get("measured") or [])
    if not exceptions:
        exceptions = _absent_vs_present_durable_fields(ctx) \
            - _posture_sensitive_fields(ctx)
    sensitive = _posture_sensitive_fields(ctx)
    cells = _v24_cells(ctx)
    changed_by_index = {c.get("index"): c for c in
                        (get_path(doc, f"{a}.askDecisionTable.changedCells")
                         or [])}

    inspected = []
    for index, cell in enumerate(cells):
        if cell.get("policyPresence") != ABSENT:
            continue
        counterpart = _v24_cell(ctx, cell.get("invocationProfile"),
                                "PRESENT-DURABLE_RETAINED",
                                cell.get("requestedCustody"))
        if counterpart is None:
            continue
        # resolve the rule: every posture-derived field takes the corresponding
        # PRESENT-DURABLE_RETAINED value, except the derived exception set
        resolved = dict(cell)
        for field in sensitive - exceptions:
            if field in counterpart:
                resolved[field] = counterpart[field]
        published = (changed_by_index.get(index) or {}).get("after")
        if not isinstance(published, dict):
            published = cell            # a cell the artifact does not change
        for field in sorted(sensitive - exceptions):
            if field not in published:
                continue
            if published[field] != resolved.get(field):
                inspected.append({
                    "cell": index,
                    "axis": f"{cell.get('invocationProfile')}/"
                            f"{cell.get('requestedCustody')}",
                    "field": field,
                    "ruleGives": resolved.get(field),
                    "artifactPublishes": published[field],
                })
    declared = exception_block.get("exceptionsDiscoveredByInspection")
    measured = len({(row["field"]) for row in inspected})
    if declared is not None and declared != measured:
        out.append(
            f"RT26-N01 $.partA_repairsForcedByThePostureDecision."
            f"theOneRuleThatGeneratesAllOfIt.theExceptionSetIsDerivedNotListed."
            f"exceptionsDiscoveredByInspection declares {declared!r} and "
            f"resolving the artifact's OWN rule plus its OWN derived exception "
            f"set against the pinned v24 cells moves {measured} further field(s) "
            f"that the artifact holds at v24's values: {inspected}. The "
            f"subtraction is at the FIELD level and takes a union over the whole "
            f"table, so a field that is posture-sensitive somewhere and "
            f"presence-derived at a particular cell falls through it -- which is "
            f"precisely the class the derivation claims to have closed. The "
            f"carve-out is principled and stated in prose "
            f"(whyNoFieldChanges, whyTheWriteFlagStaysFalseHere); it is simply "
            f"not the subtraction, and 'exceptionsDiscoveredByInspection 0' "
            f"asserts that no such statement was needed")
    if block.get("derivedNotEnumerated") is not False:
        out.append("RT26-N01 derivedNotEnumerated is not false; IR-RT25-B2's "
                   "repair menu required either a complete exception set or a "
                   "dropped derivation claim, and the enumerated table is the "
                   "half that is performed completely")
    if block.get("derivedAndEnumerated") is not True:
        out.append("RT26-N01 derivedAndEnumerated is not true")
    if exception_block.get("soTheExceptionsAreDerived") is True and inspected:
        out.append(
            f"RT26-N01 soTheExceptionsAreDerived is true while {len(inspected)} "
            f"published field value(s) are held by prose rather than by the "
            f"derivation. A future successor generalising the generator gets the "
            f"wrong answer for exactly these positions")
    ctx["exceptionsByInspection"] = inspected
    return out


VERBATIM_SOURCE_HINTS = (
    ("$.cdRt5DecisionRecord.", "pkt"),
    ("$.repairsAgainstTheV25Review.", "v25rev"),
    (".predecessorReview.", "v24rev"),
    (".section72Position.", "freeze"),
    ("lawverbatim", "freeze"),
    (".overriddenarchitecturalrecommendation.", "v22"),
    ("thepredecessorsruleverbatim", "v25"),
    ("predecessorclauseverbatim", "v25"),
    ("predecessorstatementverbatim", "v25"),
    ("d9ownruleverbatim", "d9"),
    ("obligationverbatim", "tm"),
    ("plandigestverbatim", "DIGEST"),
    ("predecessordecisionverbatim", "v24"),
    ("predecessorchoiceverbatim", "v24"),
    ("predecessorpropertiesverbatim", "v24"),
    ("predecessorreasonverbatim", "v24"),
    ("predecessorjustificationverbatim", "v24"),
    ("mutationverbatim", "v24"),
    ("statementverbatim", "v24"),
)

_KEY_RENDERING = re.compile(
    r"^([A-Za-z][A-Za-z0-9_]*): (true|false|null|-?\d+|\".*\")$")


def _verbatim_sources(ctx):
    """Folded text of every source a Verbatim field could name.  Built once and
    cached: the freeze alone is 300+ KB and the mutation suite would otherwise
    re-fold it a hundred times."""
    if "verbatimSources" in ctx:
        return ctx["verbatimSources"]
    mapping = {
        "v22": "retention-tiers.v22.json",
        "v23": "retention-tiers.v23.json",
        "v24": "retention-tiers.v24.json",
        "v24rev": "retention-tiers.v24.review-independent.json",
        "v25": "retention-tiers.v25.json",
        "v25rev": "retention-tiers.v25.review-independent.json",
        "d9": "d9-exit-contract.v1.14.json",
        "tm": "threat-model.v3.json",
        "ev": "evidence.v10.json",
        "pkt": "artifacts/product-dispositions.v1.json",
        "freeze": "IMPLEMENTATION-FREEZE.md",
        "bp": "IMPLEMENTER-BLUEPRINT.md",
        "plan": "ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md",
    }
    folded, raw = {}, {}
    for key, name in mapping.items():
        data = ctx["snaps"].get(name)
        if data is None:
            path = _resolve(name)
            data = path.read_bytes() if path.is_file() else b""
        text = data.decode("utf-8", errors="replace")
        parsed = ""
        if name.endswith(".json") and text:
            try:
                parsed = json.dumps(json.loads(text), ensure_ascii=False)
            except json.JSONDecodeError:
                parsed = ""
        raw[key] = text + " " + parsed
        folded[key] = fold(raw[key])
    ctx["verbatimSources"] = (folded, raw)
    return folded, raw


def check_verbatim_fields(doc, ctx):
    """B4.  Every field whose KEY ends in `verbatim` asserts a fact about BYTES,
    and is searched in THE SOURCE ITS OWN NAME ATTRIBUTES IT TO -- never in a
    union.

    The scoping is the whole point.  A union search is DEFEATED when a
    misquotation is INHERITED, because the predecessor carries the same wrong
    text: the predecessor's `d9OwnRuleVerbatim` misquoted D9 and v23 and v24
    carried the same error, so a corpus-wide search found it and reported
    nothing.  This driver derives the attribution from the field's own name and
    then HARD-COMPARES its derivation against the artifact's published
    attributedSource, so a re-attributed field is caught rather than skipped.
    """
    out = []
    folded, raw = _verbatim_sources(ctx)
    published = {r.get("path"): r for r in
                 (get_path(doc, "$.quotationDiscipline.results") or [])}
    keys = [(p, v) for p, v in all_keys(doc)
            if p.split(".")[-1].lower().endswith("verbatim")]
    string_keys = [(p, v) for p, v in keys if isinstance(v, str)]
    other_keys = [(p, v) for p, v in keys if not isinstance(v, str)]

    verified = 0
    not_found = 0
    false_absent = 0
    false_absent_normalised = 0
    source_attributed = 0
    for path, value in string_keys:
        low = path.lower()
        source = None
        for token, key in VERBATIM_SOURCE_HINTS:
            if token.lower() in low:
                source = key
                break
        declared_source = (published.get(path) or {}).get("attributedSource")
        if declared_source is not None and source is not None \
                and declared_source != source:
            out.append(f"RT26-B4 {path}: this instrument derives the attribution "
                       f"{source!r} from the field's own name and the artifact "
                       f"publishes {declared_source!r}")
        if not value.strip():
            out.append(f"RT26-B4 {path}: a Verbatim field is empty")
            not_found += 1
            continue
        if source == "DIGEST":
            live = measured_digest("ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md")
            if live is not None and value != live:
                ctx.setdefault("notices", []).append(
                    f"RT26-B4-DIGEST {path}: records {value[:16]}..., live "
                    f"{live[:16]}...; the file is cited-not-gated, so reported "
                    f"rather than found")
            verified += 1
            continue
        if source is None:
            out.append(f"RT26-B4 {path}: no source can be derived from this "
                       f"field's own name, so a scoped search is impossible and "
                       f"the claim of verbatimness is unbindable")
            not_found += 1
            continue
        source_attributed += 1
        needle = fold(value)
        rendering = _KEY_RENDERING.match(_norm(value))
        if rendering:
            if fold(f'"{rendering.group(1)}"') in folded[source]:
                verified += 1
                continue
            out.append(f"RT26-B4 {path}: renders a member "
                       f"{rendering.group(1)!r} that does not exist in {source}")
            not_found += 1
            continue
        if needle in folded[source]:
            verified += 1
            # §7.7's own two measurements, both taken: a RAW BYTE-LITERAL search
            # and a whitespace-normalised one.  The section records that the
            # first returns a false ABSENT on line-wrapped text and that the
            # second STILL returns ABSENT on a blockquote.
            if value not in raw[source]:
                false_absent += 1
            if _norm(value) not in _norm(raw[source]):
                false_absent_normalised += 1
            continue
        not_found += 1
        elsewhere = [k for k, text in folded.items() if needle in text]
        out.append(
            f"RT26-B4 {path}: a field named Verbatim, whose own name attributes "
            f"it to {source}, carries text that does NOT occur in that file "
            f"under §7.7 folding. "
            + (f"It DOES occur in {elsewhere}, so this is a misquotation a "
               f"predecessor already carried and this artifact inherited -- "
               f"exactly the case a union-wide search cannot see. "
               if elsewhere else "It occurs in no source either. ")
            + f"Text: {_norm(value)[:180]!r}")

    for path, value in other_keys:
        if isinstance(value, list) and all(isinstance(m, str) for m in value):
            for member in value:
                rendering = _KEY_RENDERING.match(_norm(member))
                if rendering is None:
                    out.append(f"RT26-B4 {path}: a list-valued Verbatim field "
                               f"carries {member!r}, which is neither a "
                               f"quotation this driver can scope nor a rendering "
                               f"of a JSON member")
                elif fold(f'"{rendering.group(1)}"') not in folded["v24"]:
                    out.append(f"RT26-B4 {path}: renders a member "
                               f"{rendering.group(1)!r} that does not exist in "
                               f"the pinned v24")
        else:
            out.append(f"RT26-B4 {path}: a Verbatim key whose value is a "
                       f"{type(value).__name__}, which no scoped search covers")

    declared_total = get_path(doc, "$.quotationDiscipline.verbatimFieldsInTheseBytes")
    if _exact_int(declared_total) and declared_total != len(keys):
        out.append(
            f"RT26-B4-CENSUS $.quotationDiscipline.method says 'every field in "
            f"these bytes whose key ends in verbatim was extracted, folded, and "
            f"searched'. A full walk finds {len(keys)} such keys and "
            f"verbatimFieldsInTheseBytes is {declared_total}. The "
            f"{len(other_keys)} outside the census "
            f"{[p for p, _ in other_keys]} are non-string-valued, and a census "
            f"that silently scopes itself to string leaves -- in the document "
            f"whose quotation discipline is the repair of a blocker -- is the "
            f"shape the artifact polices elsewhere with real care")
    ctx["verbatimStringKeys"] = len(string_keys)
    ctx["verbatimVerified"] = verified
    ctx["verbatimNotFound"] = not_found
    ctx["verbatimFalseAbsent"] = false_absent
    ctx["verbatimFalseAbsentNormalised"] = false_absent_normalised
    ctx["verbatimSourceAttributed"] = source_attributed
    if verified == 0:
        out.append("RT26-B4 VACUOUS: no Verbatim field was verified against any "
                   "source, so this driver measured nothing")
    if false_absent == 0 and source_attributed:
        out.append(
            "RT26-B4 the §7.7 folding is not load-bearing on these bytes: every "
            "quotation would also have been found by a raw search. Reported "
            "because the artifact's own method claims the folding is what makes "
            "the result correct, and a claim that costs nothing is a claim worth "
            "re-checking")
    return out


def check_freeze_anchors(doc, ctx):
    """The freeze is CITED-NOT-GATED, so its digest cannot fail the run -- but
    the passages this instrument and this artifact depend on must still exist.

    §7.10 records what happens otherwise: when check-retention-custody-v23/-v24
    began refusing their pins BEFORE parsing anything, the FREEZE_ANCHORS guard
    they carried went inert and nothing announced it, and in that window a §4.5
    heading rewrite deleted an anchor outright.  So these are checked here, in
    the findings body, where a pin refusal cannot silence them.
    """
    out = []
    path = _resolve("IMPLEMENTATION-FREEZE.md")
    if not path.is_file():
        out.append("RT26-ANCHOR IMPLEMENTATION-FREEZE.md is not present, so every "
                   "law this artifact quotes is unanchored")
        return out
    text = fold(path.read_text(encoding="utf-8", errors="replace"))
    missing = [a for a in FREEZE_ANCHORS if fold(a) not in text]
    if missing:
        out.append(
            f"RT26-ANCHOR {len(missing)} of {len(FREEZE_ANCHORS)} cited freeze "
            f"passages are absent from the live document under §7.7 folding: "
            f"{[m[:60] for m in missing]}. Matching is folded so a reflow cannot "
            f"manufacture a refusal, which means an absence here is a REMOVAL")
    ctx["anchorsPresent"] = len(FREEZE_ANCHORS) - len(missing)
    ctx["anchorsTotal"] = len(FREEZE_ANCHORS)
    return out


def check_residual_measurements(doc, ctx):
    """Each declared residual's own measuredValues, hard-compared where the
    figure is about these bytes.  RT25-RES-01's numbers are the ones this
    instrument moves, and it reports the movement WITHOUT asserting the artifact
    says so: §7.2 forbids editing the reviewed bytes, so the artifact's
    retainedChecker stays NONE and the residual stays live against it."""
    out = []
    residuals = {r.get("id"): r for r in (get_path(doc, "$.newResiduals") or [])
                 if isinstance(r, dict)}
    corpus = {r.get("id"): r for r in (get_path(doc, "$.corpusResiduals") or [])
              if isinstance(r, dict)}
    res01 = residuals.get("RT25-RES-01") or {}
    measured = res01.get("measuredValues") or {}
    for field, expected in (("retainedCheckers", 0), ("vectorsExecuted", 0),
                            ("invariantsMechanicallyChecked", 0),
                            ("mutationSweepsRun", 0)):
        if measured.get(field) != expected:
            out.append(f"RT26-RES RT25-RES-01.measuredValues.{field} is "
                       f"{measured.get(field)!r}, expected {expected}. The "
                       f"residual is a statement about the ARTIFACT, which "
                       f"retains no checker; this instrument is a companion and "
                       f"does not change what the artifact declares")
    for rid, block in list(residuals.items()) + list(corpus.items()):
        if not str(block.get("statement", "")).strip():
            out.append(f"RT26-RES {rid} has an empty statement")
        values = block.get("measuredValues")
        if values is not None and not isinstance(values, dict):
            out.append(f"RT26-RES {rid}.measuredValues is not an object")
        if values is not None and not values:
            out.append(f"RT26-RES {rid}.measuredValues is empty, so the residual "
                       f"has been stripped of the numbers that make it a "
                       f"measurement")
    ids = [r.get("id") for r in (get_path(doc, "$.newResiduals") or [])]
    if len(ids) != len(set(ids)):
        out.append("RT26-RES duplicate residual ids")
    for prefix in (get_path(doc, "$.separability.newPrefixesInThisArtifact")
                   or []):
        if not any(str(i).startswith(str(prefix)) for i in ids) \
                and not any(str(i).startswith(str(prefix))
                            for i in INVARIANT_IDS) \
                and not any(str(d.get("id", "")).startswith(str(prefix))
                            for d in (get_path(doc, "$.declaredDependencies")
                                      or [])):
            out.append(f"RT26-RES the artifact declares the new prefix "
                       f"{prefix!r} and nothing in these bytes carries it")
    # every DEP- id cited anywhere must be declared
    declared_deps = {d.get("id") for d in
                     (get_path(doc, "$.declaredDependencies") or [])
                     if isinstance(d, dict)}
    cited = set()
    for _, value in scalar_leaves(doc):
        if isinstance(value, str):
            cited.update(re.findall(r"\bDEP-RT2[56]-\d+\b", value))
    undeclared = sorted(cited - declared_deps)
    if undeclared:
        out.append(f"RT26-RES {len(undeclared)} dependency id(s) are cited in "
                   f"these bytes and declared nowhere: {undeclared}")
    return out


def check_companion_instrument(doc, ctx):
    """The artifact records having run another lane's instrument against its
    PREDECESSOR before finalising.  That is a claim about a file on disk."""
    out = []
    block = get_path(doc, "$.theCompanionInstrumentForThePredecessor") or {}
    recorded = block.get("sha256")
    live = measured_digest("check-retention-custody-v25.py")
    if recorded != live:
        out.append(f"RT26-COMPANION the artifact records "
                   f"check-retention-custody-v25.py at {recorded!r} and the live "
                   f"file is {live!r}")
    if recorded != GATED_PINS["check-retention-custody-v25.py"]:
        out.append("RT26-COMPANION the recorded companion digest is not the "
                   "digest this instrument gates")
    named = str(block.get("instrument", ""))
    if "check-retention-custody-v25.py" not in named:
        out.append(f"RT26-COMPANION the named instrument is {named!r}")
    return out


def check_answered_questions(doc, ctx):
    out = []
    for entry in (get_path(doc, "$.answeredQuestions") or []):
        if not str(entry.get("answer", "")).strip():
            out.append(f"RT26-ANSWERED question {entry.get('n')!r} has an empty "
                       f"answer")
        if entry.get("isOpen") is True:
            out.append(f"RT26-ANSWERED question {entry.get('n')!r} is listed "
                       f"under answeredQuestions and marked open")
        # answeredAt is prose that may name more than one path, so the pointers
        # are EXTRACTED rather than assumed to be the whole string.
        pointer = entry.get("answeredAt")
        if isinstance(pointer, str):
            targets = re.findall(r"\$(?:\.[A-Za-z0-9_]+|\[\d+\])+", pointer)
            if not targets:
                out.append(f"RT26-ANSWERED question {entry.get('n')!r} names no "
                           f"resolvable path at all in {pointer!r}")
            dangling = [t for t in targets
                        if get_path(doc, t, "<<ABSENT>>") == "<<ABSENT>>"]
            if dangling:
                out.append(f"RT26-ANSWERED question {entry.get('n')!r} points at "
                           f"{dangling}, which does not resolve in these bytes")
    if get_path(doc, "$.separability.partCDependsOnPartD") is not False:
        out.append("RT26-SEP partCDependsOnPartD is not false, so Part C can no "
                   "longer be adjudicated without Part D")
    if get_path(doc, "$.separability.partAPrimeDependsOnPartD") is not True:
        out.append("RT26-SEP partAPrimeDependsOnPartD is not true")
    for field, prefix in (("partCInvariantPrefix", "RT25-C-INV-"),
                          ("partDInvariantPrefix", "RT25-D-INV-"),
                          ("partCFixturePrefix", "PC-V-")):
        value = get_path(doc, f"$.separability.{field}")
        if value != prefix:
            out.append(f"RT26-SEP {field} is {value!r}, expected {prefix!r}")
        if not any(str(i).startswith(prefix) for i in INVARIANT_IDS + VECTOR_IDS):
            out.append(f"RT26-SEP no id in these bytes carries {prefix!r}")
    return out


# ===========================================================================
# SECTION 6 -- THE RUNNER.
# ===========================================================================

DRIVERS = (
    ("all", check_record),
    ("all", check_cd_rt_5),
    ("all", check_recorded_inputs),
    ("all", check_freeze_anchors),
    ("all", check_companion_instrument),
    ("all", check_answered_questions),
    ("c", check_b1),
    ("c", check_partition),
    ("a", check_part_a_prime),
    ("a", check_exception_set_closure),
    ("all", check_verbatim_fields),
    ("all", check_census),
    ("all", check_residual_measurements),
    ("all", check_counts),
)


def run_all(doc, ctx, part: str):
    findings = []
    ctx["b1"] = measure_b1(doc)
    ctx["notices"] = []
    if part in ("c", "all"):
        vector_findings, _ = run_vectors(doc, ctx)
        findings.extend(vector_findings)
        invariant_findings, _ = run_invariants(doc, ctx)
        findings.extend(invariant_findings)
    for scope, driver in DRIVERS:
        if scope != "all" and part not in ("all", scope):
            continue
        try:
            findings.extend(driver(doc, ctx))
        except RefusedError as exc:
            findings.append(f"RT26-DRIVER {driver.__name__}: a reference "
                            f"derivation refused: {exc}")
        except (KeyError, TypeError, IndexError, AttributeError) as exc:
            findings.append(f"RT26-DRIVER {driver.__name__}: could not run "
                            f"({type(exc).__name__}: {exc}); this is a defect in "
                            f"the driver or a shape it cannot read, NOT a "
                            f"measured property of the artifact")
    type_f, _ = type_findings(doc)
    findings.extend(type_f)
    return findings


# ===========================================================================
# SECTION 7 -- THE MUTATION SUITE.
#
# Each mutation must produce a finding carrying THE ID NAMED FOR IT and NOT
# PRESENT IN THE BASE.  A mutation caught only by a different family counts as an
# escape for its own family and is reported as one -- a suite that accepts any
# finding measures that the checker is noisy, not that it is aimed.
#
# The delta discipline is what makes the number meaningful over a base that is
# not clean.  It is still reported as a number and never as a certification.
# ===========================================================================

V = "$.partC_retentionBounds.vectors"
C = "$.partC_retentionBounds"
A = "$.partA_repairsForcedByThePostureDecision"


def _mut(doc, path, value):
    out = copy.deepcopy(doc)
    set_path(out, path, value)
    return out


def _del(doc, path):
    out = copy.deepcopy(doc)
    del_path(out, path)
    return out


def _vector_index(doc, vid):
    for index, row in enumerate(get_path(doc, f"{V}.rows") or []):
        if row.get("id") == vid:
            return index
    raise RefusedError(f"selftest: vector {vid} not present")


def _invariant_index(doc, iid):
    for index, row in enumerate(get_path(doc, f"{C}.invariants") or []):
        if row.get("id") == iid:
            return index
    raise RefusedError(f"selftest: invariant {iid} not present")


def build_selftest_cases(doc):
    """Returns [(name, mutatedDoc, expectedFindingIdPrefix)]."""
    i01 = _vector_index(doc, "PC-V-01-COUNT-ONLY")
    i02 = _vector_index(doc, "PC-V-02-PARASITISM-CONTROL-KEEP-ZERO")
    i03 = _vector_index(doc, "PC-V-03-PARASITISM-CONTROL-KEEP-ONE")
    i04 = _vector_index(doc, "PC-V-04-INDEPENDENCE-MAX-NOT-SUM")
    i05 = _vector_index(doc, "PC-V-05-SILENT-REVERT-CONTROL")
    i06 = _vector_index(doc, "PC-V-06-EXACT-TYPE-BOOL")
    i07 = _vector_index(doc, "PC-V-07-EXACT-TYPE-FLOAT")
    i08 = _vector_index(doc, "PC-V-08-EXACT-TYPE-NUMERIC-STRING")
    i09 = _vector_index(doc, "PC-V-09-UNSATISFIABLE-AGE-BOUND")
    i10 = _vector_index(doc, "PC-V-10-PROTECTED-SET-EXCEEDS-BOUND")
    i11 = _vector_index(doc, "PC-V-11-CAUSE-BLINDNESS-WITHIN-PURGED")
    i12 = _vector_index(doc, "PC-V-12-ABSENT-BOUNDS-RESOLVE-TO-UNBOUNDED")
    i13 = _vector_index(doc, "PC-V-13-ABSENT-POLICY-RESOLVES-DURABLE")
    i14 = _vector_index(doc, "PC-V-14-EPHEMERAL-IS-ALWAYS-CONSENTED")
    i15 = _vector_index(doc, "PC-V-15-DEFAULT-IS-NEVER-PERSISTED")
    i16 = _vector_index(doc, "PC-V-16-DISMISSAL-DOES-NOT-SUPPRESS-THE-NEXT-ASK")
    i17 = _vector_index(doc, "PC-V-17-DEFAULT-CONFIGURATION-EVICTS-NOTHING")
    i18 = _vector_index(doc, "PC-V-18-TIME-DIMENSION-AT-ITS-ONLY-LEGAL-VALUE")
    i19 = _vector_index(doc, "PC-V-19-BOUNDS-IDENTITY-WORKED-VECTORS")
    i20 = _vector_index(
        doc, "PC-V-20-IDENTITY-IS-OVER-CONFIGURED-VALUES-NOT-LIFTED-CAPS")
    n02 = _invariant_index(doc, "RT25-C-INV-02")
    n15 = _invariant_index(doc, "RT26-C-INV-15")
    n18 = _invariant_index(doc, "RT26-A-INV-18")
    d04 = _invariant_index(doc, "RT25-D-INV-04")

    cases = []

    def add(name, mutated, expect):
        cases.append((name, mutated, expect))

    # --- the vectors -------------------------------------------------------
    add("MX-01-VECTOR-EXPECTATION-MOVED",
        _mut(doc, f"{V}.rows[{i01}].expectedEvictionCount", 4), "RT26-VEC")
    add("MX-02-VECTOR-CAUSE-MOVED",
        _mut(doc, f"{V}.rows[{i01}].expectedCauses", ["RETENTION_USER_REQUEST"]),
        "RT26-VEC")
    add("MX-03-VECTOR-DELETED", _del(doc, f"{V}.rows[{i02}]"), "RT26-VEC")
    add("MX-04-VECTOR-ID-RENAMED", _mut(doc, f"{V}.rows[{i04}].id", "PC-V-99"),
        "RT26-VEC")
    add("MX-05-CONTROL-DEMOTED-TO-NON-CONTROL",
        _mut(doc, f"{V}.rows[{i02}].isNegativeControl", False), "RT26-COUNT")
    add("MX-06-PARASITIC-RESULT-FALSIFIED",
        _mut(doc, f"{V}.rows[{i02}].resultUnderRejectedReading", 4), "RT26-VEC")
    add("MX-07-TIEBREAK-ROW-DE-TIED",
        _mut(doc, f"{V}.rows[{i03}].bounds.keepCount", 3), "RT26-VEC")
    add("MX-08-TIEBREAK-CAUSE-FLIPPED",
        _mut(doc, f"{V}.rows[{i03}].expectedCauses", ["RETENTION_COUNT_BOUND"]),
        "RT26-VEC")
    add("MX-09-SUM-CONTROL-RESULT-MOVED",
        _mut(doc, f"{V}.rows[{i04}].resultUnderRejectedReading", 3), "RT26-VEC")
    add("MX-10-SILENT-REVERT-ADMISSION-FLIPPED",
        _mut(doc, f"{V}.rows[{i05}].expectedAdmission", "ADMITTED"), "RT26-VEC")
    add("MX-11-BOOL-CONTROL-RESPELLED-AS-INT",
        _mut(doc, f"{V}.rows[{i06}].bounds.keepCount", 1), "RT26-TYPE")
    add("MX-12-FLOAT-CONTROL-RESPELLED-AS-INT",
        _mut(doc, f"{V}.rows[{i07}].bounds.keepCount", 200), "RT26-TYPE")
    add("MX-13-STRING-CONTROL-RESPELLED-AS-INT",
        _mut(doc, f"{V}.rows[{i08}].bounds.keepCount", 200), "RT26-TYPE")
    add("MX-14-EXACT-TYPE-ERROR-CODE-INVENTED",
        _mut(doc, f"{V}.rows[{i06}].expectedErrorCode", "RETENTION.BAD_TYPE"),
        "RT26-VEC")
    add("MX-15-AGE-CONTROL-VALUE-MOVED",
        _mut(doc, f"{V}.rows[{i09}].bounds.maxAgeSeconds", 5184001), "RT26-VEC")
    add("MX-16-AGE-CONTROL-ADMISSION-FLIPPED",
        _mut(doc, f"{V}.rows[{i09}].expectedAdmission", "ADMITTED"), "RT26-VEC")
    add("MX-17-OVER-BOUND-EXPECTATION-FLIPPED",
        _mut(doc, f"{V}.rows[{i10}].expectedOverBound", False), "RT26-VEC")
    add("MX-18-WRITE-ADMISSION-FLIPPED",
        _mut(doc, f"{V}.rows[{i10}].expectedWriteAdmission", "REFUSED"),
        "RT26-VEC")
    add("MX-19-CAUSE-BLINDNESS-EXPECTATION-FLIPPED",
        _mut(doc, f"{V}.rows[{i11}].expectedEqual", False), "RT26-VEC")
    add("MX-20-ANCHOR-CAPABILITY-MOVED",
        _mut(doc, f"{V}.rows[{i11}].expectedEffectiveCapabilityA", "replayable"),
        "RT26-VEC")
    add("MX-21-ABSENT-BOUNDS-RESOLUTION-MOVED",
        _mut(doc, f"{V}.rows[{i12}].expectedResolvedBounds", "200 / 0 / 0"),
        "RT26-VEC")
    add("MX-22-ABSENT-BOUNDS-PROVENANCE-FLIPPED",
        _mut(doc, f"{V}.rows[{i12}].expectedProvenance", "CONFIGURED"),
        "RT26-VEC")
    add("MX-23-ABSENT-POSTURE-INVERTED",
        _mut(doc, f"{V}.rows[{i13}].expectedPosture", "EPHEMERAL_ONLY"),
        "RT26-VEC")
    add("MX-24-ABSENT-OUTCOME-INVERTED",
        _mut(doc, f"{V}.rows[{i13}].expectedDurableAuthoritativeOutcome",
             "REFUSE"), "RT26-VEC")
    add("MX-25-EPHEMERAL-PROVENANCE-DEFAULTED",
        _mut(doc, f"{V}.rows[{i14}].expectedProvenance", "DEFAULTED"),
        "RT26-VEC")
    add("MX-26-EPHEMERAL-REFUSAL-DELETED",
        _mut(doc, f"{V}.rows[{i14}].expectedDurableAuthoritativeOutcome",
             "PROCEED-DURABLE"), "RT26-VEC")
    add("MX-27-EPHEMERAL-ERROR-CODE-INVENTED",
        _mut(doc, f"{V}.rows[{i14}].expectedErrorCode", "RETENTION.REFUSED"),
        "RT26-VEC")
    add("MX-28-DEFAULT-PERSISTED",
        _mut(doc, f"{V}.rows[{i15}].expectedPolicyOnDiskAfter", "PRESENT"),
        "RT26-VEC")
    add("MX-29-NEXT-ASK-SUPPRESSED",
        _mut(doc, f"{V}.rows[{i16}].expectedSecondRunAskPerformed", False),
        "RT26-VEC")
    add("MX-30-DEFAULT-CONFIG-EVICTS",
        _mut(doc, f"{V}.rows[{i17}].expectedEvictionCount", 5), "RT26-VEC")
    add("MX-31-DEFAULT-CONFIG-DEMANDS-FALSIFIED",
        _mut(doc, f"{V}.rows[{i17}].expectedDemands",
             {"time": 0, "size": 5, "count": 0}), "RT26-VEC")
    add("MX-32-TIME-DIMENSION-EXPECTATION-MOVED",
        _mut(doc, f"{V}.rows[{i18}].expectedEvictionCount", 5), "RT26-VEC")
    add("MX-33-TIME-DIMENSION-DEMANDS-FALSIFIED",
        _mut(doc, f"{V}.rows[{i18}].expectedDemands",
             {"time": 5, "size": 0, "count": 2}), "RT26-VEC")
    add("MX-34-IDENTITY-DIGEST-FABRICATED",
        _mut(doc, f"{V}.rows[{i19}].rows[0].retentionBoundsId",
             "rbnd1:sha256:" + "0" * 64), "RT26-VEC")
    add("MX-35-IDENTITY-PREIMAGE-LENGTH-MOVED",
        _mut(doc, f"{V}.rows[{i19}].rows[1].preimageByteLength", 249),
        "RT26-VEC")
    add("MX-36-IDENTITY-INPUT-MOVED",
        _mut(doc, f"{V}.rows[{i19}].rows[2].keepCount", 7), "RT26-VEC")
    add("MX-37-IDENTITY-COLLAPSED",
        _mut(doc, f"{V}.rows[{i19}].rows[1].retentionBoundsId",
             get_path(doc, f"{V}.rows[{i19}].rows[0].retentionBoundsId")),
        "RT26-VEC")
    add("MX-38-ENCODER-CONTROL-GOLDEN-FABRICATED",
        _mut(doc, f"{C}.identity.encoderControl.rows[0].recomputedHere",
             "rpol1:sha256:" + "1" * 64), "RT26-VEC")
    add("MX-39-ENCODER-CONTROL-COUNT-DRIFT",
        _mut(doc, f"{C}.identity.encoderControl.goldensReproduced", 1),
        "RT26-VEC")
    add("MX-40-PCV20-IDENTITY-FABRICATED",
        _mut(doc, f"{V}.rows[{i20}].expectedRetentionBoundsId",
             "rbnd1:sha256:" + "2" * 64), "RT26-VEC")
    add("MX-41-PCV20-PREIMAGE-LENGTH-MOVED",
        _mut(doc, f"{V}.rows[{i20}].expectedPreimageByteLength", 256),
        "RT26-VEC")
    add("MX-42-VECTOR-COUNT-DRIFT", _mut(doc, f"{V}.count", 19), "RT26-COUNT")
    add("MX-43-NEGATIVE-CONTROL-COUNT-DRIFT",
        _mut(doc, f"{V}.negativeControlCount", 17), "RT26-COUNT")

    # --- the B1 algebra ----------------------------------------------------
    add("MX-44B-DEMAND-EXPRESSION-LOSES-ITS-CAP",
        _mut(doc, f"{C}.sweep.demands.rows[0].demand",
             "demand_count := max(0, len(evictable) - keep)"), "RT26-B1")
    add("MX-44-DEMAND-EXPRESSION-REVERTED-TO-THE-PREDECESSORS",
        _mut(doc, f"{C}.sweep.demands.rows[2].demand",
             "demand_time := the number of leading members of the eviction order "
             "whose admission time is strictly older than now - maxAgeSeconds"),
        "RT26-B1")
    add("MX-45-CROSS-DIMENSION-SYMBOL-INTRODUCED",
        _mut(doc, f"{C}.sweep.demands.rows[1].demand",
             "demand_size := the smallest k in [0, len(evictable)] such that "
             "total_bytes(evictable[k:]) <= cap_size and keepCount > 1"),
        "RT26-B1")
    add("MX-46-BRANCH-INTRODUCED-INTO-AN-EXPRESSION",
        _mut(doc, f"{C}.sweep.demands.rows[0].demand",
             "demand_count := 0 if cap_count is UNBOUNDED else max(0, "
             "len(evictable) - cap_count)"), "RT26-B1")
    add("MX-47-SIBLING-DISABLE-FIELD-RETURNS",
        _mut(doc, f"{C}.sweep.demands.rows[0].disabledWhen", "keepCount == 0"),
        "RT26-B1")
    add("MX-48-VALUE-AT-UNBOUNDED-FALSIFIED",
        _mut(doc, f"{C}.sweep.demands.rows[0].valueAtUNBOUNDED", 5),
        "RT26-C-INV-15")
    add("MX-49-TOTALITY-CLAIM-WITHDRAWN",
        _mut(doc, f"{C}.sweep.demands.rows[1].isTotalOnCap", False),
        "RT26-C-INV-15")
    add("MX-50-EXTENSION-COUNT-DRIFT",
        _mut(doc, f"{C}.sweep.demands.theDisableConvention.extensionsRequired", 3),
        "RT26-C-INV-15")
    add("MX-51-LIFT-APPLIED-TO-FEWER-DIMENSIONS",
        _mut(doc, f"{C}.sweep.demands.theDisableConvention.dimensionsLifted", 2),
        "RT26-C-INV-15")
    add("MX-52-RE-MEASUREMENT-TABLE-FALSIFIED",
        _mut(doc, f"{C}.sweep.demands.everyDemandIsZeroAtItsOwnDisableValue."
                  f"reMeasuredAgainstTheArithmeticVectors.perRow[0]."
                  f"underThesePublishedExpressions", 5), "RT26-B1")
    add("MX-53-PREDECESSOR-COLUMN-FALSIFIED",
        _mut(doc, f"{C}.sweep.demands.everyDemandIsZeroAtItsOwnDisableValue."
                  f"reMeasuredAgainstTheArithmeticVectors.perRow[0]."
                  f"underThePredecessorsPublishedExpressions", 3), "RT26-B1")
    add("MX-54-PER-ROW-DEMANDS-FALSIFIED",
        _mut(doc, f"{C}.sweep.demands.everyDemandIsZeroAtItsOwnDisableValue."
                  f"reMeasuredAgainstTheArithmeticVectors.perRow[1].demandsHere",
             {"AGE": 0, "SIZE": 0, "COUNT": 4}), "RT26-B1")

    # --- the cause vocabulary ---------------------------------------------
    add("MX-55-CAUSE-PARTITION-GAINS-A-MEMBER",
        _mut(doc, f"{C}.causeVocabulary.closedPartitions[0].members",
             list(CAUSE_PARTITION) + ["RETENTION_POSTURE_CHANGE"]),
        "RT25-C-INV-04")
    add("MX-56-CAUSE-PARTITION-COUNT-DRIFT",
        _mut(doc, f"{C}.causeVocabulary.closedPartitions[0].memberCount", 5),
        "RT26-COUNT")
    add("MX-57-CAUSE-POSITION-MOVED",
        _mut(doc, f"{C}.causeVocabulary.orderedPosition", 6), "RT25-C-INV-04")
    add("MX-57B-CAUSE-DECLARED-NEW",
        _mut(doc, f"{C}.causeVocabulary.fieldIsNotNew", False), "RT25-C-INV-04")

    # --- the posture resolution -------------------------------------------
    add("MX-58-POSTURE-ROW-INVERTED",
        _mut(doc, "$.postureResolution.theDerivation.rows[0].posture",
             "EPHEMERAL_ONLY"), "RT25-D-INV-02")
    add("MX-59-PROVENANCE-ROW-INVERTED",
        _mut(doc, "$.postureResolution.theDerivation.rows[2].provenance",
             "DEFAULTED"), "RT25-D-INV-02")
    add("MX-60-POSTURE-ENUM-GAINS-A-MEMBER",
        _mut(doc, "$.postureResolution.theDerivation.postureEnum",
             ["DURABLE_RETAINED", "EPHEMERAL_ONLY", "DURABLE_BOUNDED"]),
        "RT25-D-INV-05")
    add("MX-61-POSTURE-ENUM-GAINS-ABSENT",
        _mut(doc, "$.postureResolution.theDerivation.postureEnum",
             ["DURABLE_RETAINED", "EPHEMERAL_ONLY", "ABSENT"]),
        "RT25-D-INV-05")
    add("MX-62-DERIVATION-ROW-DELETED",
        _del(doc, "$.postureResolution.theDerivation.rows[1]"),
        "RT25-D-INV-01")
    add("MX-63-DEFAULT-WRITTEN-TO-DISK",
        _mut(doc, f"{C}.boundsRecord.effectiveBoundsResolution."
                  f"theDefaultIsNeverWrittenToDisk", False), "RT25-D-INV-03")
    add("MX-63B-PROVENANCE-PERSISTED",
        _mut(doc, f"{C}.boundsRecord.effectiveBoundsResolution."
                  f"provenanceIsNeverPersisted", False), "RT25-D-INV-03")
    add("MX-63C-PERSISTING-OUTCOME-COUNT-DRIFT",
        _mut(doc, "$.postureResolution.theDefaultIsNeverPersisted."
                  "policyPersistingOutcomesUnchanged", 3), "RT25-D-INV-03")
    add("MX-64-SILENT-DEMOTION-PERMITTED",
        _mut(doc, "$.postureResolution.lawFourteenPosition."
                  "silentDemotionIsStillForbidden", False), "RT26-A-INV-18")
    add("MX-65-DEMOTION-DECLARED-REACHABLE",
        _mut(doc, "$.postureResolution.lawFourteenPosition."
                  "theDemotionThatIsStillForbidden."
                  "isItReachableUnderTheNewDefault", True), "RT26-A-INV-18")
    add("MX-66-INV-D04-QUALIFIER-STRIPPED",
        _mut(doc, f"{C}.invariants[{d04}].statement",
             "A durable-authoritative request is refused if and only if the "
             "effective posture is EPHEMERAL_ONLY; it is never silently demoted "
             "to ephemeral."), "RT25-D-INV-04")
    add("MX-67-INV-02-DELETED", _del(doc, f"{C}.invariants[{n02}]"), "RT26-INV")
    add("MX-68-INV-15-ID-RENAMED",
        _mut(doc, f"{C}.invariants[{n15}].id", "RT26-C-INV-99"), "RT26-INV")
    add("MX-69-INV-18-STATEMENT-EMPTIED",
        _mut(doc, f"{C}.invariants[{n18}].statement", "   "), "RT26-INV")
    add("MX-70-INVARIANT-COUNT-DRIFT", _mut(doc, f"{C}.invariantCount", 23),
        "RT26-COUNT")

    # --- Part A prime ------------------------------------------------------
    add("MX-71-BEFORE-ROW-FALSIFIED",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].before.outcome",
             "PROCEED-DURABLE"), "RT26-A")
    add("MX-72-AFTER-ROW-DEMOTES-SILENTLY",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].after."
                  f"durableSourceDerivedWritePermitted", False),
        "RT26-A-INV-18")
    add("MX-73-ASK-CELL-GRANTS-A-WRITE",
        _mut(doc, f"{A}.askDecisionTable.changedCells[1].after."
                  f"durableSourceDerivedWritePermitted", True),
        "RT26-A-INV-18")
    add("MX-74-ASK-CELL-STOPS-ASKING",
        _mut(doc, f"{A}.askDecisionTable.changedCells[1].after.askPerformed",
             False), "RT26-A-INV-17")
    add("MX-75-DISCLOSURE-DELETED-AT-AN-ABSENT-CELL",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].after."
                  f"firstRunDisclosureEmitted", False), "RT26-A-INV-17")
    add("MX-76-D9-AXES-AUTHORED-ON-A-NON-TERMINATING-ROW",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].after.derivedExitCode",
             2), "RT26-A-INV-19")
    add("MX-77-D9-CLASS-AUTHORED",
        _mut(doc, f"{A}.interactionOutcomes.changed[0].after.derivedClass",
             "retention-degraded"), "RT26-A-INV-19")
    add("MX-78-D9-ERROR-CODE-AUTHORED",
        _mut(doc, f"{A}.interactionOutcomes.changed[1].after.derivedErrorCode",
             "RETENTION.EVIDENCE_PURGED"), "RT26-A-INV-19")
    add("MX-79-CHANGED-FIELD-SET-FALSIFIED",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].fieldsChanged",
             ["outcome"]), "RT26-A")
    add("MX-80-CHANGED-FIELD-COUNT-DRIFT",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].fieldsChangedCount", 5),
        "RT26-A")
    add("MX-81-SELECTED-CELL-SET-FALSIFIED",
        _mut(doc, f"{A}.askDecisionTable.selectedCellIndices", [1, 5]),
        "RT26-A")
    add("MX-82-EXCEPTION-SET-GUTTED",
        _mut(doc, f"{A}.theOneRuleThatGeneratesAllOfIt."
                  f"theExceptionSetIsDerivedNotListed."
                  f"step3_theExceptionSetIsStep2MinusStep1.measured",
             ["askPerformed"]), "RT26-A-INV-17")
    add("MX-83-DERIVATION-CLAIM-REINSTATED",
        _mut(doc, f"{A}.theOneRuleThatGeneratesAllOfIt.derivedNotEnumerated",
             True), "RT26-N01")
    add("MX-84-INSPECTION-COUNT-FALSIFIED",
        _mut(doc, f"{A}.theOneRuleThatGeneratesAllOfIt."
                  f"theExceptionSetIsDerivedNotListed."
                  f"exceptionsDiscoveredByInspection", 9), "RT26-N01")
    add("MX-85-POSTURE-SENSITIVE-SET-FALSIFIED",
        _mut(doc, f"{A}.theOneRuleThatGeneratesAllOfIt."
                  f"theExceptionSetIsDerivedNotListed."
                  f"step1_postureSensitiveFields.measured",
             ["outcome", "derivedClass"]), "RT26-A-INV-17")
    add("MX-86-OUTCOME-COUNT-DRIFT",
        _mut(doc, f"{A}.interactionOutcomes.outcomesChanged", 3), "RT26-COUNT")
    add("MX-87-OUTCOME-ID-INVENTED",
        _mut(doc, f"{A}.interactionOutcomes.changed[0].id", "PA-INT-99"),
        "RT26-A")
    add("MX-88-TERMINATION-HISTORY-FALSIFIED",
        _mut(doc, f"{A}.interactionOutcomes.changed[0].terminatesBefore", False),
        "RT26-A")
    add("MX-89-PERSISTING-OUTCOME-SET-FALSIFIED",
        _mut(doc, f"{A}.interactionOutcomes.policyPersistingOutcomeIdsAfter",
             ["PA-INT-01-ANSWERED-RETAIN"]), "RT26-A")
    add("MX-90-NOASK-CASE-DELETED", _del(doc, f"{A}.noAskCasesReDerived[2]"),
        "RT26-COUNT")
    add("MX-91-BICONDITIONAL-COUNT-FALSIFIED",
        _mut(doc, f"{A}.d9RowsForRowsThatStopTerminating."
                  f"theConventionMeasuredOverV24sOwnRows.rowsWithNullAxes", 6),
        "RT26-A-INV-19")
    add("MX-92-BICONDITIONAL-DEVIATIONS-HIDDEN",
        _mut(doc, f"{A}.d9RowsForRowsThatStopTerminating."
                  f"theConventionMeasuredOverV24sOwnRows.deviationCount", 3),
        "RT26-A-INV-19")

    # --- the record, the packet and the inputs ----------------------------
    add("MX-93-STATUS-PROMOTED", _mut(doc, "$.status", "APPLIED/ACCEPTED"),
        "RT26-RECORD")
    add("MX-94-SEAL-RECOMMENDATION-FLIPPED",
        _mut(doc, "$.sealRecommendation", "SEAL"), "RT26-RECORD")
    add("MX-95-RETAINED-CHECKER-CLAIMED",
        _mut(doc, "$.retainedChecker", "check-retention-custody-v26.py"),
        "RT26-RECORD")
    add("MX-96-AMENDMENT-DECLARED-APPLIED",
        _mut(doc, "$.authority.mayApplyTheCdRt5AmendmentDraft", True),
        "RT26-RECORD")
    add("MX-97-FREEZE-BECOMES-A-SEAL",
        _mut(doc, "$.freezeDeclaration.constitutesASealOrSignature", True),
        "RT26-RECORD")
    add("MX-98-V10-DISCHARGE-CLAIMED",
        _mut(doc, "$.v10Item3Position.claimedStatusForTheseBytes", "DISCHARGED"),
        "RT26-RECORD")
    add("MX-99-DECISION-STATE-REVERTED",
        _mut(doc, "$.cdRt5DecisionRecord.state", "BLOCKED_ON_PHASE_1A"),
        "RT26-CDRT5")
    add("MX-100-AUTHORITY-FABRICATED",
        _mut(doc, "$.cdRt5DecisionRecord.decidedBy", "the product authority"),
        "RT26-CDRT5")
    add("MX-101-DECISION-DATE-MOVED",
        _mut(doc, "$.cdRt5DecisionRecord.decidedOn", "2026-08-04"), "RT26-CDRT5")
    add("MX-102-AUTHORITY-PLACEHOLDER",
        _mut(doc, "$.integrationState.CD-RT-5", "DECIDED [DATE] by [NAME]"),
        "RT26-CDRT5")
    add("MX-103-POSTURE-FIELD-DISAGREES-WITH-THE-PACKET",
        _mut(doc, "$.productAuthorityBoundary.durableDefault", "EPHEMERAL_ONLY"),
        "RT26-CDRT5")
    add("MX-104-IMPLICIT-RETENTION-FLIPPED",
        _mut(doc, "$.productAuthorityBoundary.implicitDurableRetention", "NO"),
        "RT26-CDRT5")
    add("MX-105-QUOTED-DECISION-TERM-FABRICATED",
        _mut(doc, "$.cdRt5DecisionRecord.theTermsAsDecided."
                  "boundedRetentionVerbatim",
             "Retention is unbounded and the bounds are global."), "RT26-CDRT5")
    add("MX-106-QUOTED-DECISION-TERM-TRUNCATED",
        _mut(doc, "$.cdRt5DecisionRecord.theTermsAsDecided.tombstonesSurviveVerbatim",
             "A tombstone outlives the bytes it describes."), "RT26-CDRT5")
    add("MX-107-QUOTED-TERM-RENAMED",
        _mut(doc, "$.cdRt5DecisionRecord.theTermsAsDecided."
                  "durableDefaultVerbatim", "DURABLE_BOUNDED"), "RT26-CDRT5")
    add("MX-108-RECORDED-DIGEST-DRIFT",
        _mut(doc, "$.recordedInputs.recorded[0].sha256", "2" * 64), "RT26-INPUTS")
    add("MX-109-GATE-DOWNGRADED",
        _mut(doc, "$.recordedInputs.recorded[0].gate",
             "CITED-DIGEST-RECORDED-NOT-GATED"), "RT26-INPUTS")
    add("MX-110-GATE-UPGRADED-ON-AN-UNSTABLE-FILE",
        _mut(doc, "$.recordedInputs.recorded[11].gate",
             "HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN"),
        "RT26-INPUTS")
    add("MX-111-RECORDED-COUNT-DRIFT",
        _mut(doc, "$.recordedInputs.digestsRecordedCount", 18), "RT26-COUNT")
    add("MX-112-DUPLICATE-KEY-CLAIM-FALSIFIED",
        _mut(doc, "$.recordedInputs.duplicateKeysFound", 2), "RT26-INPUTS")
    add("MX-113-COMPANION-DIGEST-FABRICATED",
        _mut(doc, "$.theCompanionInstrumentForThePredecessor.sha256", "3" * 64),
        "RT26-COMPANION")

    # --- the census, the partition and the quotations ---------------------
    add("MX-114-CENSUS-SCALAR-DRIFT",
        _mut(doc, "$.leafCensus.scalarLeafPositions", 2936), "RT26-CENSUS")
    add("MX-115-CENSUS-BOOL-DRIFT",
        _mut(doc, "$.leafCensus.boolLeafPositions", 348), "RT26-CENSUS")
    add("MX-116-CENSUS-INT-FIRST-PUBLISHED",
        _mut(doc, "$.leafCensus.intLeafPositions", 788), "RT26-CENSUS")
    add("MX-117-CENSUS-NULL-PATHS-FABRICATED",
        _mut(doc, "$.leafCensus.nullLeafPaths", ["$.leafCensus.nullLeafPaths[0]"]),
        "RT26-CENSUS")
    add("MX-118-CENSUS-FLOAT-PATH-FABRICATED",
        _mut(doc, "$.leafCensus.floatLeafPaths", ["$.partC_retentionBounds.nowhere"]),
        "RT26-CENSUS")
    add("MX-119-CENSUS-METHOD-REORDERED",
        _mut(doc, "$.leafCensus.method",
             "a recursive walk descending dicts and lists. int is tested before "
             "bool."), "RT26-CENSUS")
    add("MX-120-CENSUS-WALK-SOURCE-MOVED",
        _mut(doc, "$.leafCensus.walkedFrom", "IN-MEMORY-OBJECT"), "RT26-CENSUS")
    add("MX-121-PREDECESSOR-CENSUS-FALSIFIED",
        _mut(doc, "$.leafCensus.predecessorCensusForComparison.boolLeafPositions", 183),
        "RT26-CENSUS")
    add("MX-122-PARTITION-ROW-DELETED",
        _del(doc, "$.inheritance.exhaustivePartitionOfV24.partA[3]"), "RT26-B3")
    add("MX-123-PARTITION-ROW-INVENTED",
        _mut(doc, "$.inheritance.exhaustivePartitionOfV24.partA[3].key",
             "$.partA_firstRunRetentionConsent.noSuchKey"), "RT26-B3")
    add("MX-124-PARTITION-RESIDUAL-CLASS-RETURNS",
        _mut(doc, "$.inheritance.exhaustivePartitionOfV24.keysInNeitherList", 20),
        "RT26-B3")
    add("MX-125-PARTITION-DISPOSITION-INVENTED",
        _mut(doc, "$.inheritance.exhaustivePartitionOfV24.partB[0].disposition",
             "PARTIALLY-CHANGED"), "RT26-B3")
    add("MX-126-PARTITION-TOTAL-DRIFT",
        _mut(doc, "$.inheritance.exhaustivePartitionOfV24.totalKeyCount", 34),
        "RT26-B3")
    add("MX-127-CHANGED-SURFACE-DOES-NOT-RESOLVE",
        _mut(doc, "$.inheritance.surfacesThisArtifactChanges[0].surface",
             "$.partA_firstRunRetentionConsent.noSuchField"), "RT26-B3")
    add("MX-128-VERBATIM-FIELD-FABRICATED",
        _mut(doc, "$.inheritance.section72Position.ruleVerbatim",
             "A review verdict binds whatever the reviewer felt at the time."),
        "RT26-B4")
    add("MX-129-VERBATIM-FIELD-EMPTIED",
        _mut(doc, "$.postureResolution.lawFourteenPosition.lawVerbatim", "   "),
        "RT26-B4")
    add("MX-130-VERBATIM-INHERITED-MISQUOTATION",
        _mut(doc, f"{C}.d9ReasonCodePosition.whyOneAndNotFour.d9OwnRuleVerbatim",
             "two codes with the same remedy are a smell and two remedies behind "
             "one code are a defect"), "RT26-B4")
    add("MX-131-VERBATIM-RE-ATTRIBUTED",
        _mut(doc, "$.quotationDiscipline.results[2].attributedSource", "v25"),
        "RT26-B4")
    add("MX-132-VERBATIM-CENSUS-DRIFT",
        _mut(doc, "$.quotationDiscipline.verbatimFieldsInTheseBytes", 36),
        "RT26-COUNT")
    add("MX-133-VERBATIM-NOT-FOUND-COUNT-FALSIFIED",
        _mut(doc, "$.quotationDiscipline.notFoundInTheirAttributedSource", 2),
        "RT26-COUNT")

    # --- the D9 vocabulary and the residuals ------------------------------
    D9 = f"{C}.d9ReasonCodePosition.measuredLiveFromPinnedD9Bytes"
    add("MX-134-D9-DEFICIENCY-COUNT-DRIFT",
        _mut(doc, f"{D9}.deficiencyMemberCount", 10), "RT25-C-INV-14")
    add("MX-135-D9-ERROR-COUNT-DRIFT", _mut(doc, f"{D9}.errorCodeCount", 20),
        "RT25-C-INV-14")
    add("MX-136-D9-GAP-CLOSED-BY-FIAT",
        _mut(doc, f"{D9}.reasonCodesMatchingPredicate", 1), "RT25-C-INV-14")
    add("MX-137-D9-TOKEN-PREDICATE-GUTTED",
        _mut(doc, f"{D9}.retentionTokenPredicate", []), "RT25-C-INV-14")
    add("MX-138-D9-DIGEST-DRIFT", _mut(doc, f"{D9}.sha256", "0" * 64),
        "RT25-C-INV-14")
    add("MX-139-D9-CODE-CLAIMED-ADDED",
        _mut(doc, f"{C}.d9ReasonCodePosition.requestedSuccessorNotAdded."
                  f"codesAddedByThisArtifact", 1), "RT25-C-INV-14")
    add("MX-140-RES-01-CLAIMS-EXECUTION",
        _mut(doc, "$.newResiduals[0].measuredValues.vectorsExecuted", 20),
        "RT26-RES")
    add("MX-141-RES-01-DECLARED-COUNT-DRIFT",
        _mut(doc, "$.newResiduals[0].measuredValues.invariantsDeclared", 19),
        "RT26-COUNT")
    add("MX-142-RESIDUAL-STATEMENT-EMPTIED",
        _mut(doc, "$.newResiduals[4].statement", "  "), "RT26-RES")
    add("MX-143-RESIDUAL-COUNT-DRIFT", _mut(doc, "$.newResidualCount", 9),
        "RT26-COUNT")
    add("MX-144-DEPENDENCY-COUNT-DRIFT",
        _mut(doc, "$.declaredDependencyCount", 10), "RT26-COUNT")
    add("MX-145-DEPENDENCY-CITED-BUT-UNDECLARED",
        _mut(doc, f"{C}.sweep.scope.declaredAs", "DEP-RT26-99"), "RT26-RES")
    add("MX-146-SCOPE-BECOMES-GLOBAL", _mut(doc, f"{C}.sweep.scope.global", True),
        "RT25-C-INV-11")
    add("MX-147-OUTAGE-BECOMES-EVICTABLE",
        _mut(doc, f"{C}.evictableSet.outageIsNeverEvictable", False),
        "RT25-C-INV-13")
    add("MX-148-EMITS-OTHER-STATES",
        _mut(doc, f"{C}.sweep.emitsNoOtherToState", False), "RT25-C-INV-01")
    add("MX-149-SEPARABILITY-PREFIX-MOVED",
        _mut(doc, "$.separability.partCFixturePrefix", "PCV-"), "RT26-SEP")
    add("MX-150-PART-C-DECLARED-DEPENDENT",
        _mut(doc, "$.separability.partCDependsOnPartD", True), "RT26-SEP")
    add("MX-151-ANSWERED-QUESTION-REOPENED",
        _mut(doc, "$.answeredQuestions[0].isOpen", True), "RT26-ANSWERED")
    add("MX-152-INT-LEAF-RESPELLED-AS-BOOL",
        _mut(doc, f"{C}.invariantCount", True), "RT26-TYPE")
    add("MX-153-BOOL-LEAF-RESPELLED-AS-INT",
        _mut(doc, f"{C}.sweep.isATriggerNotAGate", 1), "RT26-TYPE")
    add("MX-154-UNRULED-INT-LEAF-INTRODUCED",
        _mut(doc, f"{C}.sweep.demands.aBrandNewUnruledCounter", 7), "RT26-TYPE")
    add("MX-155-NULL-LEAF-INTRODUCED",
        _mut(doc, f"{C}.sweep.isATriggerNotAGate", None), "RT26-TYPE")
    add("MX-156-STRAY-FLOAT-INTRODUCED",
        _mut(doc, f"{C}.sweep.demands.theDisableConvention.dimensionsLifted", 3.0),
        "RT26-TYPE")
    return cases


def selftest(doc, ctx):
    """Returns (failures, cases, caught, escapes)."""
    failures = []
    try:
        cases = build_selftest_cases(doc)
    except (RefusedError, KeyError, IndexError, TypeError) as exc:
        # A mutation that cannot be BUILT means the artifact no longer has the
        # position the mutation targets.  That is a fact about the artifact and
        # about this suite's aim, and it must be REPORTED as a named failure --
        # never as a traceback, which a reader would mistake for a finding.
        return ([f"SELFTEST-NOT-BUILT: a mutation targets a position these bytes "
                 f"do not have ({type(exc).__name__}: {exc}), so the suite could "
                 f"not be assembled and NO MUTATION RESULT IS REPORTED"],
                0, 0, [])
    names = [name for name, _, _ in cases]
    if len(set(names)) != len(names):
        failures.append("SELFTEST duplicate case names")
    base = set(run_all(doc, ctx, "all"))
    caught = 0
    escapes = []
    for name, mutated, expected in cases:
        try:
            findings = run_all(mutated, ctx, "all")
        except Exception as exc:                                   # noqa: BLE001
            failures.append(f"SELFTEST {name}: the checker raised "
                            f"{type(exc).__name__}: {exc}")
            escapes.append(name)
            continue
        new = [f for f in findings if f not in base]
        if any(f.startswith(expected) for f in new):
            caught += 1
        else:
            escapes.append(name)
            families = sorted({f.split(" ")[0] for f in new})
            failures.append(
                f"SELFTEST {name}: expected a NEW {expected} finding; got "
                f"{len(new)} new finding(s) from families {families}")
    return failures, len(cases), caught, escapes


# ===========================================================================
# SECTION 8 -- THE BOUND, STATED AS A COUNT WITH WORKED EXAMPLES.
#
# Section 7.8 asks the operative question directly: CAN I MAKE THIS CHECKER PASS
# ON A WRONG ARTIFACT?  The predecessor instrument's author answered eleven, and
# -- more valuably -- reported that THREE OF THE REVIEWER'S FOUR BLOCKERS WERE
# INVISIBLE TO IT until another reader named them.  A flattering limits count is
# worse than none.  This is the equivalent list for this file.
# ===========================================================================

WHAT_THIS_CANNOT_CATCH = (
    "A prose leaf whose VALUE is false while its PATH and TYPE are unchanged. "
    "Every `why`, `argument`, `rationale`, `whyItMatters` and `statedCost` in "
    "this artifact can be replaced by its own negation and this instrument stays "
    "silent, unless the sentence carries a number bound to a measurable source. "
    "WORKED: replace $.partC_retentionBounds.sweep.evictionOrder."
    "statedCostOfTheSingleOrder with 'oldest-first is size-optimal' -- the exact "
    "opposite of what it says -- and this run is unchanged.",

    "A required substring kept and a reversal APPENDED after it. Containment is "
    "monotone: adding text can never remove a needle. This file uses containment "
    "for the freeze anchors, for the verbatim search and for the census method "
    "sentence. WORKED: append 'This sentence is withdrawn.' to $.leafCensus."
    "method and the `bool is tested before int` check still passes. "
    "versioning-policy.v10 already published the quantified boundary for this "
    "technique and it applies here unchanged.",

    "Whether the DESIGN is right. This instrument measures agreement between two "
    "statements of the same rule -- the artifact's and this file's -- not the "
    "rule's truth. No oracle for the second exists anywhere in this corpus.",

    "Whether the reference derivations in SECTION 1 model what an implementer "
    "would build. effective_posture, ask_performed, resolve_and_maybe_persist, "
    "effective_capability and admit_bounds are models written FROM the artifact's "
    "own tables. They test SELF-CONSISTENCY. A misreading shared between the "
    "artifact and this file survives every one of them.",

    "Any D9 REFERENCE-DERIVATION defect. This instrument reads the pinned D9 "
    "vocabulary directly and never executes check-d9-v1.14.py, so it verifies "
    "MEMBERSHIP and COUNTS and verifies no derivation. The four Part A rows whose "
    "D9 triples are assigned from v24's measured convention are exactly the rows "
    "an executed derivation would test, and RT26-RES-01 stays open. This is a "
    "declared REDUCTION IN SCOPE relative to check-retention-custody-v24.py, "
    "whose 37 pins are mostly that module's transitive closure.",

    "Anything about a real store. No vector touches a real object, a footprint, "
    "an unlink, an fsync or a crash. The size dimension rests on a byte length "
    "nothing here measures. RT25-RES-03 stays open and this file does not narrow "
    "it by one byte.",

    "Whether the product authority meant what the packet records. The property "
    "pin checks that CD-RT-5 is well-formed, attributed and internally "
    "consistent; it cannot check that sfbreen decided what the row says. "
    "RT25-RES-CORPUS-04 says the same and no mechanism in this corpus could.",

    "A defect in this file's own frozen type registry. INT_LEAF_NAMES and "
    "BOOL_LEAF_NAMES are literals transcribed once from these bytes. A name "
    "wrongly classified HERE is a wrong rule applied consistently, and "
    "`unruled == 0` cannot see it. WORKED: had `complete` been transcribed into "
    "INT_LEAF_NAMES instead of BOOL_LEAF_NAMES, every boolean at that name would "
    "be admitted forever and the sweep would report zero escapes.",

    "The 24 invariants as a JOINTLY SATISFIABLE SET. Each driver evaluates its "
    "own invariant against models and against the artifact's published values. "
    "Nothing here proves the 24 are consistent with one another, and nothing "
    "proves any of them is true of an implementation that does not yet exist.",

    "13 of the 20 vectors AS VECTORS AGAINST A SYSTEM. Seven arithmetic rows are "
    "executed against a real implementation of the algebra; the identity rows are "
    "executed against a real encoder. The remaining rows are executed against "
    "MODELS OF ADMISSION AND RESOLUTION written in Section 1 of this file. That "
    "is a stronger claim than the artifact's `executed: false` and a much weaker "
    "one than 'the vectors pass'.",

    "An inherited misquotation in any field NOT named `*Verbatim`. The B4 sweep "
    "keys on the KEY NAME. A quotation asserted in ordinary prose, or in a field "
    "called `predecessorStatement` or `theRuleItself`, is not swept at all. "
    "WORKED: $.partA_repairsForcedByThePostureDecision.theOneRuleThatGeneratesAll"
    "OfIt.rule is the artifact's statement of the generating rule and is bound "
    "here only by the resolution in check_exception_set_closure, not by any "
    "quotation check.",

    "A wrong ATTRIBUTION that this file and the artifact share. The verbatim "
    "scoping table VERBATIM_SOURCE_HINTS is hand-written here and compared "
    "against the artifact's published attributedSource. Agreement means two "
    "readers agree; it does not mean the field quotes the document it should.",

    "THE CLASS THAT IS MOST LIKELY TO EXIST AND IS NOT LISTED ABOVE. The "
    "predecessor instrument's author measured that THREE OF FOUR blockers found "
    "by an independent review were invisible to that instrument until the review "
    "named them. This file was written AFTER a review of its subject and with "
    "that review read, so its coverage is shaped by what one reviewer looked at. "
    "The review's own whatIDidNotCheck names ten things, and this instrument "
    "closes only some of them. There is no reason to believe a further class does "
    "not exist for exactly the same reason.",
)

WHAT_THIS_DOES_CATCH_THAT_NOTHING_ELSE_DID = (
    "$.corpusResiduals[0].measuredValues.recordedInputs declares 15 against 19 "
    "recorded rows, and the boundary sentence beside it restates the same wrong "
    "figure. The independent review hard-compared 15 structural counts and graded "
    "6 residuals by name; this field was in neither set.",
)


def print_limits() -> None:
    print("check-retention-custody-v26.py -- WHAT A GREEN RUN IS NOT")
    print()
    print("  A green run would be author-side evidence that this artifact says")
    print("  what it says consistently, that its algebra and arithmetic close,")
    print("  that its quotations are quotations, and that drift in a GATED input")
    print("  will be caught. It would NEVER be evidence that the artifact is")
    print("  right. IMPLEMENTATION-FREEZE 7.8: these instruments bind structure")
    print("  and type; they do not bind the truth of content.")
    print()
    print(f"CAN I MAKE THIS CHECKER PASS ON A WRONG ARTIFACT?  YES, "
          f"{len(WHAT_THIS_CANNOT_CATCH)} WAYS FOUND:")
    for index, item in enumerate(WHAT_THIS_CANNOT_CATCH, 1):
        print(f"  {index}. {item}")
    print()
    print("  This list is examples, not the boundary. It was written by the")
    print("  author of the instrument and is bounded by the same reading.")
    print()
    print("WHAT THIS INSTRUMENT FOUND THAT NO PRIOR READER REPORTED:")
    for index, item in enumerate(WHAT_THIS_DOES_CATCH_THAT_NOTHING_ELSE_DID, 1):
        print(f"  {index}. {item}")


def _banner(part, notices, counts, sweep, ctx):
    b1 = ctx.get("b1") or {}
    vec = ctx.get("vectorReport") or {}
    inv = ctx.get("invariantReport") or {}
    print(f"RETENTION-CUSTODY v26  part={part}  gated pins {len(GATED_PINS)}  "
          f"advancing {len(ADVANCING_PINS)}  drift notices {len(notices)}  "
          f"scalar leaves {counts['scalarLeafPositions']}  guarded int/bool "
          f"{counts['guardedIntOrBoolLeafPositions']}  unruled "
          f"{counts['unruledIntOrBoolLeafPositions']}")
    print(f"  vectors {vec.get('executed', 0)}/{vec.get('declared', 0)} executed, "
          f"{vec.get('controlsRun', 0)} rejected readings run, "
          f"{len(vec.get('controlsVacuous') or [])} vacuous; invariants "
          f"{inv.get('executed', 0)}/{inv.get('declared', 0)} executed")
    print(f"  B1: {len(b1.get('publishedAgree') or [])}/"
          f"{b1.get('arithmeticRows', 0)} arithmetic rows agree under the "
          f"PUBLISHED expressions, {len(b1.get('v25Agree') or [])}/"
          f"{b1.get('arithmeticRows', 0)} under the PREDECESSOR's; "
          f"{len(b1.get('causeAgree') or [])} cause attributions agree; default "
          f"0/0/0 evicts nothing across {b1.get('defaultConfigSizesSwept', 0)} "
          f"evictable-set sizes "
          f"({len(b1.get('defaultConfigNonZeroV25') or [])} of those sizes evict "
          f"under the predecessor's expressions)")
    print(f"  B1: {len(b1.get('crossDimensionSymbols') or [])} cross-dimension "
          f"symbols; {b1.get('prefixInclusionViolations', 0)} prefix-inclusion "
          f"violations over {b1.get('prefixConfigurations', 0)} configurations; "
          f"removed fallback reached {b1.get('fallbackReached')} over "
          f"{b1.get('fallbackConfigurations', 0)} configurations")
    print(f"  type sweep: {sweep['respellingsAttempted']} respellings attempted, "
          f"{sweep['respellingsAdmitted']} admitted "
          f"(float {sweep['float']['sweptPositions']}/"
          f"{sweep['float']['admitted']}; bool<-0|1 "
          f"{sweep['boolFromZeroOrOneInt']['sweptPositions']}/"
          f"{sweep['boolFromZeroOrOneInt']['admitted']}; int<-bool "
          f"{sweep['intFromBool']['sweptPositions']}/"
          f"{sweep['intFromBool']['admitted']})")
    print(f"  quotations: {ctx.get('verbatimVerified', 0)} of "
          f"{ctx.get('verbatimStringKeys', 0)} string-valued *Verbatim keys "
          f"verified against the source each field's own NAME attributes it to; "
          f"{ctx.get('verbatimFalseAbsent', 0)} of "
          f"{ctx.get('verbatimSourceAttributed', 0)} would read FALSE-ABSENT "
          f"under a raw byte-literal search and "
          f"{ctx.get('verbatimFalseAbsentNormalised', 0)} under a "
          f"whitespace-normalised one, so the section 7.7 folding is "
          f"load-bearing")
    print(f"  CD-RT-5 read live, not pinned: status "
          f"{ctx.get('cdRt5Status')!r}, {ctx.get('cdRt5Quoted', 0)} quoted "
          f"decision fields re-extracted from the live packet; freeze anchors "
          f"{ctx.get('anchorsPresent', 0)}/{ctx.get('anchorsTotal', 0)}")
    for line in notices:
        print(f"  {line}")
    for line in ctx.get("notices") or []:
        print(f"  {line}")
    print("  a green run is author-side evidence only; run --limits for what "
          "this instrument cannot catch")


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
                sys.stderr.write("RT26-UNSUPPORTED-INVOCATION: --part takes a, "
                                 "c, d or all. THE CHECK DID NOT RUN.\n")
                return 2
            part = argv[index]
        elif arg.startswith("--part="):
            part = arg.split("=", 1)[1]
            if part not in ("a", "c", "d", "all"):
                sys.stderr.write("RT26-UNSUPPORTED-INVOCATION: --part takes a, "
                                 "c, d or all. THE CHECK DID NOT RUN.\n")
                return 2
        else:
            sys.stderr.write(f"RT26-UNSUPPORTED-INVOCATION: unknown option "
                             f"{arg!r}. THE CHECK DID NOT RUN.\n")
            return 2
        index += 1

    try:
        snaps, notices = verified_inputs()
    except PinRefused as exc:
        sys.stderr.write(f"{exc}\n")
        sys.stderr.write(
            "RT26-PIN-REFUSED: the verified execution closure did not match its "
            "pinned digests, so NOTHING WAS PARSED OR EXECUTED and THE CHECK DID "
            "NOT RUN. This exit says nothing whatever about "
            f"{SUBJECT}. Repair is a successor instrument, never an edit to "
            "these bytes.\n")
        return 2

    subject_path = _resolve(SUBJECT)
    if not subject_path.is_file():
        sys.stderr.write(f"RT26-INPUT-MISSING {SUBJECT}: the subject is not "
                         f"present beside this instrument. THE CHECK DID NOT "
                         f"RUN.\n")
        return 2
    subject_bytes = subject_path.read_bytes()
    live_subject = sha_bytes(subject_bytes)
    if live_subject != SUBJECT_SHA256:
        notices.append(
            f"RT26-SUBJECT-MOVED {SUBJECT}: reviewed at {SUBJECT_SHA256[:16]}..., "
            f"{SUBJECT_BYTES} bytes; live {live_subject[:16]}..., "
            f"{len(subject_bytes)} bytes. This instrument REPORTS rather than "
            f"refuses, because refusing to parse would hide every other finding "
            f"behind one line -- but the independent verdict binds the reviewed "
            f"bytes and does not cover these. Section 7.2: a change to reviewed "
            f"bytes requires a version bump and a new verdict, and may never be "
            f"made in place.")

    try:
        doc = _parse(subject_bytes, SUBJECT)
        parsed = {name: _parse(data, name) for name, data in snaps.items()
                  if name.endswith(".json")}
    except PinRefused as exc:
        sys.stderr.write(f"RT26-PARSE-REFUSED: {exc}. THE CHECK DID NOT RUN.\n")
        return 2

    try:
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
            "d9errorCodes": list(get_path(d9, "$.codeVocabulary.errorCodes") or []),
            "product": parsed["artifacts/product-dispositions.v1.json"],
            "tm3": parsed["threat-model.v3.json"],
            "ev10": parsed["evidence.v10.json"],
        }
    except KeyError as exc:
        sys.stderr.write(f"RT26-INPUT-MISSING: a parsed input this instrument "
                         f"requires is absent ({exc}). THE CHECK DID NOT RUN.\n")
        return 2

    findings = run_all(doc, ctx, part)

    if do_selftest:
        dirty = bool(findings) or bool(notices)
        if dirty:
            # Section 7.2 requires "the suite did not run" to be a DISTINCT
            # OBSERVABLE and requires a dirty base never to produce a green
            # banner. Both hold. The suite is still EXECUTED, under the delta
            # discipline -- every mutation must produce a finding NOT PRESENT IN
            # THE BASE -- which is what makes the result meaningful over a dirty
            # base rather than meaningless. The exit code is 3 unconditionally:
            # this mode reports a number, it does not certify anything.
            print("SELFTEST-OVER-DIRTY-BASE: the base is NOT clean, so this run "
                  "certifies nothing and cannot return 0. The suite is executed "
                  "under delta discipline and the number below is reported, not "
                  "attested.")
            for line in notices:
                print(f"  base notice: {line[:150]}")
            for finding in findings:
                print(f"  base finding: {finding[:200]}")
        failures, cases, caught, escapes = selftest(doc, ctx)
        print(f"RETENTION-CUSTODY v26 SELFTEST"
              f"{' (dirty base)' if dirty else ''}: {caught}/{cases} mutations "
              f"caught by their own named check")
        if escapes:
            print(f"  escapes: {escapes}")
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

    base_type, counts = type_findings(doc)
    sweep = hostile_sweep(doc, base_type)
    for arm in ("float", "boolFromZeroOrOneInt", "intFromBool"):
        if sweep[arm]["admitted"]:
            findings.append(
                f"RT26-SWEEP {arm}: {sweep[arm]['admitted']} position(s) admitted "
                f"a respelled scalar: {sweep[arm]['escapes'][:5]}")
    if counts["unruledIntOrBoolLeafPositions"]:
        findings.append(
            f"RT26-SWEEP {counts['unruledIntOrBoolLeafPositions']} int/bool leaf "
            f"position(s) are outside the frozen type registry, so the sweep does "
            f"not cover them")

    _banner(part, notices, counts, sweep, ctx)

    if findings:
        print(f"{len(findings)} finding(s) in {SUBJECT}:")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"{SUBJECT}: PASS (architecture-candidate scope; "
          f"CANDIDATE-NOT-APPLIED; the artifact's own $.retainedChecker remains "
          f"NONE and this file does not change it; RT25-RES-01's measured half is "
          f"narrowed, not closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())












