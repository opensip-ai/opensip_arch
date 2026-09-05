#!/usr/bin/env python3
"""Retained checker for retention-tiers.v25.json.

WHAT THIS INSTRUMENT IS FOR, STATED BEFORE ANYTHING ELSE.

  retention-tiers.v25.json landed as a candidate whose own most serious
  self-declared weakness is RT25-RES-01: *no retained checker -- 0 of 16 vectors
  and 0 of 19 invariants are mechanically exercised.*  IMPLEMENTATION-FREEZE.md
  section 7.1 grades that residual "a fair residual for a candidate,
  DISQUALIFYING for application".  Section 7.8 records that the residual was
  misread as a wall: sections 7.2 and 7.6 forbid EDITING a reviewed artifact,
  and a new checker is a new file and edits nothing.  This file is that new
  file.  It edits nothing, and it names every byte it reads.

  It executes all 16 vectors of $.partC_retentionBounds.vectors.rows and all 19
  invariants of $.partC_retentionBounds.invariants.  Every one can fail: the
  selftest mutates the artifact and requires each mutation to be caught by the
  check named for it, and each negative-control vector additionally runs the
  REJECTED reading it names and requires that reading to produce the DIFFERENT
  result the row declares.  Section 7.2.2's rider -- "a measurement that cannot
  fail the build is prose" -- is the standard, and section 7.8's repair is the
  one applied: for every assertion, exhibit an input that is WRONG rather than
  merely EMPTY.

THIS CHECKER DOES NOT PASS ON retention-tiers.v25.json, AND THAT IS THE POINT.

  It exits 2 on the current tree for TWO independent and correctly-reported
  reasons.  Neither is tuned away, because a checker adjusted until it agrees
  with a defective artifact launders the defect and is worse than no checker.

  RT25-C-B1  THE PUBLISHED DEMAND EXPRESSIONS EVICT EVERYTHING AT THE VALUE
             DECLARED TO DISABLE THEM.  Read literally, and they are published
             as executable rows:
               count : max(0, len(evictable) - keepCount)   at keepCount 0  -> n
               size  : smallest k with total_bytes(order[k:]) <= maxTotalBytes,
                       else len(evictable)                  at maxTotalBytes 0 -> n
               time  : leading members older than now - maxAgeSeconds
                                                            at maxAgeSeconds 0 -> n
             This instrument implements both readings -- AS-PUBLISHED and
             GUARDED, the latter applying `disabledWhen` as an outer guard --
             runs all 16 vectors under each, and reports which agrees.  Measured:
             4 of the 5 arithmetic vectors CONTRADICT the published expressions
             and 5 of 5 agree with the guarded reading, so the artifact's own
             vectors and its own expressions cannot both be right.  The default
             configuration of every unconfigured project is 0/0/0, so under the
             published expressions the defect fires in exactly the default case
             -- and $.partC.sweep.neverRunsWhenBoundsAreDefaulted declares the
             opposite in the same file.  The time dimension is worst: DEP-RT25-01
             forces maxAgeSeconds to 0 and 0 is precisely the catastrophic value.
             Independently corroborates the reviewer's blocker B1.

  RT25-PIN-UNSATISFIABLE  A HARD-PINNED INPUT CAN NO LONGER SATISFY ITS PIN, AND
             THE CAUSE IS KNOWN.  v25 pins
             product-dispositions.cd-rt-5-amendment.draft.v1.json at
             4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea
             under the gate string
             HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN, a gate
             aimed at exactly this file.  The live digest is
             872c67be307866a645d246104a61065d1ab6c6d812618e0a40bbd837c4b0edb0.
             CAUSE, RECORDED SO NOBODY HUNTS A CORRUPTION THAT HAS AN
             EXPLANATION: the coordinator edited that draft IN PLACE after v25
             was authored, to withdraw a false claim it carried (that a retention
             reason code closes RT23-B-RES-01; measured live it does not -- still
             0/9, 0/9, 0/19).  A successor draft.v2 was the compliant move and
             was not taken.  The file is untracked, has no git history, and the
             original bytes are UNRECOVERABLE.  The pin is therefore permanently
             unsatisfiable and this instrument reports it rather than re-pointing
             it.  A pin you quietly re-point is not a pin.  v25's SUCCESSOR
             re-pins the live digest; this checker does not.

  This instrument is built to outlive v25 and serve that successor.

AN INDEPENDENT REVIEW OF v25 RETURNED `REJECT FOR REPAIR` AT 4 BLOCKERS, AND THIS
INSTRUMENT AS FIRST WRITTEN CAUGHT ONE OF THEM.

  Measured, not conceded in the abstract.  B1 was caught by construction.  B2, B3
  and B4 were MISSED, and SECTION 7 was written afterwards to close them:

    B1  demand expressions evict everything at their own disable values
        -> RT25-C-B1.  Caught on the first run, before the review was read.
    B2  the one rule that generates the Part A repair does not resolve to the
        stated repair -> RT25-B2, added.  Diffs v24's ABSENT cells against its
        PRESENT-DURABLE_RETAINED cells field by field; measured, the generator
        silently changes `firstRunDisclosureEmitted` at 4 of 4 pairs.
    B3  the changed-surface set is incomplete and falsifies inherited Part A
        -> RT25-B3, added.  Partitions v24's Part A and Part B key sets against
        the two declared lists; measured, 19 of 35 keys appear in neither.
    B4  a field named Verbatim quotes text that exists nowhere in its source
        -> RT25-B4, added.  Sweeps EVERY `*Verbatim` leaf.  Both of the review's
        instances now fire, and the second only because the search is SCOPED to
        the source the field's own name attributes it to: `d9OwnRuleVerbatim`
        misquotes D9 and the misquotation was already carried by v23 and v24, so
        a union-wide search finds it and reports nothing.  AN INHERITED
        MISQUOTATION IS INVISIBLE TO A CORPUS-WIDE TOKEN SEARCH.  That is a
        general lesson and it is the reason SECTION 7 exists as its own section.

  This is 7.8's bound observed on this file rather than quoted: an instrument
  written from the same reading as the artifact sees what that reading already
  looked at.  Three of four blockers required a different reader.  What
  discharges the residual is an independent re-derivation, not more assertions
  from the same lane -- and the review supplied one.

WHAT A GREEN RUN IS, AND IS NOT.  (Section 7.8, answered directly.)

  A green run is author-side evidence that this artifact says what it says
  consistently, that its arithmetic closes, and that drift in any pinned input
  will be caught.  It is NEVER evidence that the artifact is RIGHT.  The same
  reading produced both the design and this instrument, so a shared misreading
  is invisible to it.  The bound is stated in five places by three earlier
  authors and it holds here unchanged: this instrument binds STRUCTURE, TYPE,
  ARITHMETIC and DERIVATION; it does not bind the TRUTH OF PROSE.  A string leaf
  whose VALUE is false while its PATH and TYPE are unchanged passes.  See
  $.whatThisCannotCatch, printed by --limits, for the enumerated list and the
  count of ways this checker can be made to pass on a wrong artifact.

TRUST ORDER.  Every input is read as inert bytes, hashed, and compared against a
pinned digest BEFORE any of it is parsed.  A mismatch on a HARD pin prints one
named refusal line and exits 2; it never reaches a findings path.

PIN CLASSES, taken from the artifact's own $.recordedInputs.recorded[].gate --
this checker does not invent the classification, it implements it:

  HARD (12)          every input v25 gates
                     HARD-PIN-EXIT-2-ON-MISMATCH-IF-A-CHECKER-IS-EVER-WRITTEN.
                     Drift -> EXIT 2, nothing parsed.  One of the twelve --
                     the CD-RT-5 amendment draft -- is permanently unsatisfiable
                     for the recorded reason above; it is pinned anyway, because
                     softening a pin to obtain a green run is the failure the pin
                     exists to prevent.
  RECORDED (3)       IMPLEMENTATION-FREEZE.md, IMPLEMENTER-BLUEPRINT.md and
                     ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md.  v25 itself gates
                     these as CITED-DIGEST-RECORDED-NOT-GATED because they are
                     under concurrent edit.  Digest printed, drift never a
                     finding.  The freeze is instead bound by FREEZE_ANCHORS,
                     which fail closed on removal of the cited text.

  --allow-unsatisfiable-pin runs the SEMANTIC body against the live draft bytes
  after reporting the unsatisfiable pin.  It NEVER returns 0: the best outcome it
  can reach is 1.  It exists so the semantic checks can be exercised and reported
  against a damaged input, not so the pin can be evaded.

WHY 11 HARD PINS AND NOT v24's 37.  check-retention-custody-v24.py imports and
EXECUTES check-d9-v1.14.py, so its pin table carries that module's whole
transitive closure -- 26 of its 37 pins are that closure.  This instrument does
not execute the D9 module: v25 recomputes no D9 derivation (DEP-RT25-08 records
0 of 4 outcomes recomputed), and every D9 claim v25 makes is a COUNT or a
MEMBERSHIP over d9-exit-contract.v1.14.json, which this checker reads directly
from the pinned bytes using v25's own stated method.  That is a REDUCTION IN
SCOPE relative to v24 and it is declared here, not disguised as an improvement:
this instrument cannot catch a D9 REFERENCE-DERIVATION defect, only a vocabulary
one.

Exit matrix, distinct by construction:
    0  clean
    1  findings
    2  bad invocation, integrity refusal, or HARD pin mismatch
    3  selftest refused / not run (the base was not clean, so mutation results
       would be meaningless)

Invocation:  python3 -I -B check-retention-custody-v25.py [--selftest]
                                                          [--part c|d|a|all]
                                                          [--limits]
                                                          [--allow-unsatisfiable-pin]
"""

from __future__ import annotations

import sys

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "RT25-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-retention-custody-v25.py`.  Caller-owned isolated startup is the "
        "prevention boundary; script code cannot undo interpreter or site "
        "activity that happened before line 1.\n")
    raise SystemExit(2)

import copy
import hashlib
import itertools
import json
import pathlib
import random
import re
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent
SUBJECT = "retention-tiers.v25.json"

# ---------------------------------------------------------------------------
# Pinned execution closure.  IMPLEMENTATION-FREEZE 7.2 recording obligation: a
# count is not a record, so every member is named with its digest here and again
# as data inside the subject artifact, and the two are compared on every run.
# ---------------------------------------------------------------------------
PINS: dict[str, str] = {
    # the predecessor candidate, inherited BY-REFERENCE and never edited
    "retention-tiers.v24.json":
        "ba29c115a9064ab1cd66ea01751b238acf092b3d699ca43027de7a8dfe55a277",
    "retention-tiers.v24.review-independent.json":
        "633301d5fb6400858a1e10acca50aefe8e58502ef346d5f3d06f6da5cff0084a",
    # the origin of the Part B purge semantics carried through v24
    "retention-tiers.v23.json":
        "3f8c1df562bde9dbaa6e6d87cfb611a7f2a88710f01519344ca72c5005a0891b",
    "retention-tiers.v23.review-independent.json":
        "039419b49d06999d4142346f8982eadb511ab6efc635b5e116f0694d6412719f",
    # the availability fixtures (AF-01..AF-04) and the overridden recommendation
    "retention-tiers.v22.json":
        "52aa540df75a047f0abc09b4fab4b472ab2934ad1f488146bb370ed6050743e1",
    # the predecessor instruments.  Read, hashed, NOT executed and NOT modified.
    "check-retention-custody-v24.py":
        "9a309302df6d2f1108f1fbfb4978bfc93b102eb0394c99ba7be7fc550d7fa909",
    "check-retention-custody-v23.py":
        "18e94f7603869e8fdf295664f8d7eb46d9075ea8fc1791769045fb194b4a96a8",
    # the closed D9 vocabulary this artifact measures and may not amend
    "d9-exit-contract.v1.14.json":
        "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31",
    # The only place a product decision is constituted.  RE-PINNED at the LIVE
    # digest, measured from disk by this instrument's author at
    # 2026-08-06T00:20:36Z, NOT transcribed from a report.  It moved because the
    # CD-RT-5 amendment was APPLIED: the row left $.pendingDecisions for
    # $.decisions with status DECIDED.
    #
    # THE ASYMMETRY THIS TABLE EXISTS TO MAKE VISIBLE.  Two pins below are
    # unsatisfiable against v25's recorded digests, and they are NOT the same
    # failure:
    #   ADVANCED   -- this file.  A pinned input legitimately moved forward
    #                 because a decision was taken.  Its old bytes are not needed
    #                 and its new bytes are authoritative, so a checker that is
    #                 still mutable RE-PINS.  That is what this line is.
    #   MUTATED    -- the amendment draft.  A pinned input was overwritten in
    #                 place and the pinned bytes destroyed.  Re-pinning would
    #                 adopt bytes no verdict ever covered, so this instrument
    #                 refuses instead.
    # Both surface as a refused pin.  An instrument that reports them identically
    # is telling a reader less than it knows, so this one names the class.
    #
    # check-retention-custody-v23.py and -v24.py pin the OLD digest, are retained
    # and immutable under 7.2, and have therefore gone from exit 0 to exit 2 with
    # RT23-PIN-REFUSED.  They can never be repaired.  That is 7.6 -- immutability
    # prevents a proven fix from propagating -- observed live, and this file is
    # repairable only because it is not yet reviewed.
    "product-dispositions.v1.json":
        "5fc59ad26c1f99c2bb963f2aa31b8567a8cb694dd5dd343cc403982517aef4c9",
    # V10 requiredResolution item 3 and the DeletionProtocol boundary
    "threat-model.v3.json":
        "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    # the availabilityDifferential lists and sealedCapabilityContract.finalization
    "evidence.v10.json":
        "62a3a07194062c8499f6e943b4986d7a77bdecc0c4ec499851ac078fd548e9b4",
    # PERMANENTLY UNSATISFIABLE.  Pinned anyway.  See RT25-PIN-UNSATISFIABLE in
    # the module docstring: the coordinator edited these bytes in place after v25
    # was authored, the file is untracked, and the original bytes are gone.  The
    # correct behaviour for a checker meeting a re-pointed input is to refuse and
    # say why, not to adopt the new digest.
    "product-dispositions.cd-rt-5-amendment.draft.v1.json":
        "4bbcd6fa9113a689063ce880611e98dcf3599eaa0f5846419886deb4033922ea",
}

# Named so the refusal line can explain itself instead of looking like corruption.
UNSATISFIABLE_PINS = {
    "product-dispositions.cd-rt-5-amendment.draft.v1.json":
        "coordinator-caused: edited IN PLACE after v25 was authored, to withdraw "
        "a false claim that a retention reason code closes RT23-B-RES-01 "
        "(measured live it does not; still 0/9, 0/9, 0/19).  A draft.v2 successor "
        "was the compliant move and was not taken.  The file is untracked, has no "
        "git history, and the pinned bytes are UNRECOVERABLE.  This pin can never "
        "be satisfied again and is NOT re-pointed here.",
}

# v25's own CITED-DIGEST-RECORDED-NOT-GATED class.  These are THE ARTIFACT'S
# recorded values, deliberately left as v25 wrote them: they are the baseline the
# runtime comparison prints against, and replacing them with today's digests would
# erase the record rather than check it.  Re-measured from disk 2026-08-06T00:20:36Z:
# the freeze and the blueprint have both moved (they now carry the applied PRODUCT
# decision and name check-product-dispositions-v2.py as its validator) and the plan
# has not.  Drift here is a re-baseline, never a finding -- v25 says so and this
# instrument implements v25's classification rather than its own.
RECORDED_NOT_GATED = {
    "IMPLEMENTATION-FREEZE.md":
        "3e0b0195890720b1592dd3a589c42ec3fab64992334ed33ccee1ca25063a2463",
    "IMPLEMENTER-BLUEPRINT.md":
        "f6963a5c35758e7c80483f140bb08934d236e1f132ba373798848b4bbbbc9b5f",
    "ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md":
        "47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e",
}

# Content anchors instead of a whole-file digest, for the same reason
# check-retention-custody-v24.py gives: these documents are under concurrent
# edit and a digest recorded for a file under edit is false the moment it is
# written.  Matched whitespace-normalised, so a reflow does not manufacture a
# refusal, while REMOVAL of the cited text still fails closed.
FREEZE_ANCHORS = (
    # law 18 -- the exact-type rule PC-V-06/07/08 and RT25-C-INV-09 rest on
    "18. **Closed-scalar admission is exact-type.**",
    "A boolean is not an integer, a float is not an integer, and a numeric "
    "string is not a number, in any admission path, at any depth, including "
    "inside records the host only forwards.",
    # law 14 -- quoted verbatim by v25 twice, and the basis of PC-V-10/14
    "A durability failure cannot report authoritative success; a provider fault "
    "cannot become a finding; a policy failure cannot become a host error.",
    # law 6 -- the separate-identity rule behind RETENTION-BOUNDS-ID-V1
    "separate identities with separate descriptors and separate custody",
    # law 8 -- the one-ledger-per-ProjectId rule behind DEP-RT25-03
    "Each canonical ProjectId owns `projects/<ProjectId>/ledger.sqlite` and its "
    "own physical CAS; cross-project physical deduplication is forbidden.",
    # 7.2 -- why the predecessor is inherited by reference and never edited
    "An independent review verdict binds the exact bytes reviewed and the "
    "environment",
    # 7.2.2 rider -- the standard this instrument is held to
    "a measurement that cannot fail the build is prose",
    # 7.8 -- the bound this instrument prints against itself
    "these instruments bind structure and type; they do not bind the truth of "
    "content",
    # 4.5 -- the section v25's whole authority argument rests on.  Anchored on the
    # STABLE prefix, not the disposition suffix: the suffix legitimately advances
    # (it read "— NOT a signature" when v25 was authored and reads "— SUPERSEDED
    # 2026-08-05 by an actual decision" now), and 7.2.2 says a continuing invariant
    # gets a semantic gate while a recorded measurement gets a hard comparison.
    # The SECTION EXISTING is the invariant and is anchored here; its DISPOSITION
    # is a measurement and is compared in check_record, separately, so an advance
    # and a deletion cannot be confused for one another.
    "4.5 Recorded product intent on `CD-RT-5`",
)

# What section 4.5's heading said when v25 was authored, and what it must still say
# for v25's authority framing to describe the live corpus.
FREEZE_4_5_DISPOSITION_AT_AUTHORING = "NOT a signature"

# Exercised only under --allow-unsatisfiable-pin, against the LIVE draft bytes,
# after RT25-PIN-UNSATISFIABLE has already been reported.  They are a semantic
# floor, not a substitute for the pin.
DRAFT_ANCHORS = (
    # the load-bearing design input v25 states it designs against.  If the
    # authority applies the draft, or guts it, or reverses the posture, these
    # fail closed on the LIVE bytes regardless of what the digest says.
    ("$.constitutesADecision", False),
    ("$.bindsAnything", False),
    ("$.amendsAnything", False),
    ("$.proposedReplacement.defaultPosture.durableDefault", "DURABLE_RETAINED"),
    ("$.proposedReplacement.defaultPosture.implicitDurableRetention", "YES"),
)

# The two v25 claims whose subject bytes no longer exist.  Hard-compared as a
# COUNT and as a PATH SET: a third one appearing is a finding.
UNVERIFIABLE_DRAFT_CLAIM_PATHS = (
    "$.productAuthorityBoundary.amendmentDraft."
    "twoInternalStalenessObservations.observations[0]",
    "$.productAuthorityBoundary.amendmentDraft."
    "twoInternalStalenessObservations.observations[1]",
)


class PinMismatch(RuntimeError):
    def __init__(self, message: str, unsatisfiable: list[str] | None = None) -> None:
        super().__init__(message)
        self.unsatisfiable = unsatisfiable or []


class DuplicateKeyError(ValueError):
    pass


class RefusedError(RuntimeError):
    """Raised by a reference derivation that must refuse rather than substitute."""


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate object key {key!r}")
        out[key] = value
    return out


def _parse(source: bytes, name: str) -> Any:
    try:
        return json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise PinMismatch(f"{name}: {type(exc).__name__}: {exc}") from exc


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def verified_snapshots(allow_unsatisfiable: bool = False) -> tuple[dict[str, bytes],
                                                                  list[str]]:
    """Read every HARD-pinned input as inert bytes and verify before anything runs.

    Returns (snapshots, unsatisfiableReports).  `allow_unsatisfiable` admits ONLY
    the pins named in UNSATISFIABLE_PINS, only after reporting them, and the
    caller is required to floor its exit code at 1.  Every other mismatch raises.
    """
    snaps: dict[str, bytes] = {}
    errors: list[str] = []
    unsatisfiable: list[str] = []
    for name, expected in PINS.items():
        try:
            data = (HERE / name).read_bytes()
        except OSError as exc:
            errors.append(f"{name}: read {type(exc).__name__}")
            continue
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            if name in UNSATISFIABLE_PINS:
                unsatisfiable.append(
                    f"RT25-PIN-UNSATISFIABLE {name}: pinned {expected}, live {actual}. "
                    f"{UNSATISFIABLE_PINS[name]}")
            else:
                unsatisfiable.append(
                    f"RT25-PIN-DRIFT {name}: pinned {expected}, live {actual}. "
                    f"NOT a known-unrecoverable pin: this input drifted while this "
                    f"instrument was being written and its pinned bytes may still "
                    f"exist. It is NOT re-pointed here. A successor artifact re-pins "
                    f"the live digest; a checker does not.")
            if allow_unsatisfiable:
                snaps[name] = data
                continue
            errors.append(f"{name}: {actual} != {expected}")
            continue
        snaps[name] = data
    if errors:
        raise PinMismatch("; ".join(errors), unsatisfiable)
    if set(snaps) != set(PINS):
        raise PinMismatch("not every pinned input produced a snapshot", unsatisfiable)
    return snaps, unsatisfiable


def measured_digest(rel: str) -> str | None:
    for root in (HERE, COOP):
        path = root / rel
        if path.is_file():
            return hashlib.sha256(path.read_bytes()).hexdigest()
    return None


# ===========================================================================
# SECTION 1 -- REFERENCE DERIVATIONS.
# Re-implemented here from the pinned contract text, never imported from the
# subject: an instrument that reads its answers out of the artifact it is
# checking measures nothing.  Each is paired below with the REJECTED reading the
# artifact names, so every control has a wrong input and not merely an empty one.
# ===========================================================================

CAPABILITY_RANK = {"recorded": 0, "verifiable": 1, "replayable": 2}
AVAIL_STATES = ("AVAILABLE", "OUTAGE", "MISSING-DEPENDENCY", "PURGED")
TERMINAL_STATES = ("PURGED",)

CAUSE_PARTITION = ("RETENTION_AGE_BOUND", "RETENTION_SIZE_BOUND",
                   "RETENTION_COUNT_BOUND", "RETENTION_USER_REQUEST")
# The attribution tiebreak, fixed by $.partC.causeVocabulary.
CAUSE_TIEBREAK = ("RETENTION_AGE_BOUND", "RETENTION_SIZE_BOUND",
                  "RETENTION_COUNT_BOUND")
DIMENSION_CAUSE = {"time": "RETENTION_AGE_BOUND", "size": "RETENTION_SIZE_BOUND",
                   "count": "RETENTION_COUNT_BOUND"}

POSTURE_ENUM = ("DURABLE_RETAINED", "EPHEMERAL_ONLY")
POSTURE_PROVENANCE_ENUM = ("CONSENTED", "DEFAULTED")
BOUNDS_PROVENANCE_ENUM = ("CONFIGURED", "DEFAULTED")
ABSENT = "ABSENT"

# The shipping product's live default values, present in v25 only as the values
# a REJECTED reading produces.  Re-derived here so PC-V-09 and PC-V-12 have a
# wrong input to run, not a sentence to read.
PRODUCT_KEEP = 200
PRODUCT_MAX_AGE_DAYS = 60
PRODUCT_MAX_AGE_SECONDS = PRODUCT_MAX_AGE_DAYS * 24 * 60 * 60   # 5184000
PRODUCT_MAX_SIZE_MB = 150
PRODUCT_MAX_TOTAL_BYTES = PRODUCT_MAX_SIZE_MB * 1024 * 1024

BOUNDS_ORDERED_FIELDS = ("schemaVersion", "projectId", "retentionPolicyId",
                         "maxAgeSeconds", "maxTotalBytes", "keepCount",
                         "boundsRevision", "retentionBoundsId")
BOUNDS_CLOSED_INTS = ("maxAgeSeconds", "maxTotalBytes", "keepCount",
                      "boundsRevision", "schemaVersion")


class Poison:
    """A value that raises on ANY access.

    Used to prove a derivation does not READ a field, rather than to argue it.
    Every dunder a derivation could plausibly reach raises, so a single touch is
    an exception rather than a silent pass.
    """

    __slots__ = ("label",)

    def __init__(self, label: str) -> None:
        object.__setattr__(self, "label", label)

    def _boom(self, *_args: Any, **_kwargs: Any) -> Any:
        raise RefusedError(f"POISON TOUCHED: {object.__getattribute__(self, 'label')}")

    __eq__ = _boom
    __ne__ = _boom
    __lt__ = _boom
    __le__ = _boom
    __gt__ = _boom
    __ge__ = _boom
    __hash__ = _boom
    __str__ = _boom
    __repr__ = _boom
    __bool__ = _boom
    __len__ = _boom
    __iter__ = _boom
    __contains__ = _boom
    __getitem__ = _boom
    __call__ = _boom
    __int__ = _boom
    __index__ = _boom
    __add__ = _boom
    __format__ = _boom


# --- Part B: the effective-capability derivation, re-derived from v24's own
# --- pinned algorithm text.  Used by PC-V-11 and RT25-C-INV-01/05/13.

def raw_key(obj: dict[str, Any]) -> tuple[str, str, str]:
    return obj["projectId"], obj["recordCasRef"], obj["recordKind"]


def availability_map(records: list[dict[str, Any]]) -> dict[str, dict[tuple, str]]:
    return {r["unitId"]: {raw_key(s): s["state"] for s in r["objectStates"]}
            for r in records}


def unit_satisfied(unit: dict[str, Any], amap: dict[str, dict[tuple, str]]) -> bool:
    states = amap.get(unit["unitId"])
    if states is None or not unit["objectRefs"]:
        return False
    if set(states) != {raw_key(r) for r in unit["objectRefs"]}:
        return False
    return all(state == "AVAILABLE" for state in states.values())


def satisfied_at(candidate: str, units: list[dict[str, Any]],
                 amap: dict[str, dict[tuple, str]]) -> bool:
    return all(unit_satisfied(u, amap) for u in units
               if CAPABILITY_RANK[u["requiredForCapability"]] <= CAPABILITY_RANK[candidate])


def effective_capability(sealed: str, units: list[dict[str, Any]],
                         records: list[dict[str, Any]]) -> str:
    """Reads sealedCapability, units and availabilityRecords.  Nothing else.

    In particular it never reaches a ledger entry at all -- it reads the FOLD --
    so `cause` has no path into the result.  RT25-C-INV-05 is executed against
    this function with a Poison in every cause field, and against a deliberately
    cause-reading variant as the positive control.
    """
    if sealed not in CAPABILITY_RANK:
        raise RefusedError("sealed capability outside the closed enum")
    amap = availability_map(records)
    ok = [c for c in CAPABILITY_RANK
          if CAPABILITY_RANK[c] <= CAPABILITY_RANK[sealed]
          and satisfied_at(c, units, amap)]
    return max(ok, key=lambda c: CAPABILITY_RANK[c]) if ok else "recorded"


def effective_capability_CAUSE_LEAKING(sealed: str, units: list[dict[str, Any]],
                                       records: list[dict[str, Any]],
                                       entries: list[dict[str, Any]]) -> str:
    """POSITIVE CONTROL for RT25-C-INV-05 and PC-V-11.

    A derivation that DOES read `cause`.  Without this, "the two ledgers agree"
    proves nothing, because a comparison that cannot distinguish anything agrees
    with everything.  This one must DISAGREE where the real one agrees.
    """
    base = effective_capability(sealed, units, records)
    for entry in entries:
        if entry.get("cause") == "RETENTION_USER_REQUEST":
            return "recorded" if base != "recorded" else "verifiable"
    return base


def fold_ledger(entries: list[dict[str, Any]]) -> dict[tuple, str]:
    """UnitAvailabilityLedgerV1 fold.  Append-only with terminal loss.

    Reads schemaVersion? no.  projectId, recordCasRef, recordKind, toState and
    atSequence only.  `cause` is ordered field 7 and is never named here.
    """
    state: dict[tuple, str] = {}
    terminal: set[tuple] = set()
    sequence = 0
    for entry in entries:
        if entry["atSequence"] != sequence + 1:
            raise RefusedError(f"ledger sequence break at {entry['atSequence']}")
        sequence = entry["atSequence"]
        key = (entry["projectId"], entry["recordCasRef"], entry["recordKind"])
        if key in terminal and entry["toState"] != "PURGED":
            raise RefusedError(
                f"terminal-loss append-only violation at {entry['recordCasRef']}")
        state[key] = entry["toState"]
        if entry["toState"] in TERMINAL_STATES:
            terminal.add(key)
    return state


def apply_states(records: list[dict[str, Any]],
                 overrides: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = copy.deepcopy(records)
    hits = 0
    for override in overrides:
        key = raw_key(override)
        for record in out:
            for state in record["objectStates"]:
                if raw_key(state) == key:
                    state["state"] = override["state"]
                    hits += 1
    if overrides and hits == 0:
        raise RefusedError("state override matched no object state")
    return out


# --- Part C: bounds admission.  Law 18 lives here.

def admit_bounds(record: Any, trace: list[str] | None = None) -> tuple[str, str | None,
                                                                      dict | None]:
    """ProjectRetentionBoundsV1 admission.

    Returns (verdict, errorCode, admittedRecord).  There is NO branch that maps
    an invalid value to a valid one: an invalid record produces (REFUSED, code,
    None).  RT25-C-INV-08's "never silently defaulted" is that absence, and it is
    proved by enumeration below rather than asserted.

    bool is tested BEFORE int at every position, because in Python bool is a
    subclass of int; testing int first would admit True as 1, which is exactly
    the class freeze law 18 exists to prevent (LB-C2-01).
    """
    say = trace.append if trace is not None else (lambda _s: None)
    if record is ABSENT:
        say("absent")
        return "ABSENT", None, None
    say("type-check:record")
    if not isinstance(record, dict):
        return "REFUSED", "CONFIG.INVALID", None
    say("closed-key-set")
    if set(record) != set(BOUNDS_ORDERED_FIELDS):
        return "REFUSED", "CONFIG.INVALID", None
    for field in BOUNDS_ORDERED_FIELDS:
        value = record[field]
        if field in BOUNDS_CLOSED_INTS:
            say(f"type-check:{field}")
            # bool BEFORE int.  Order is load-bearing and the trace records it.
            if isinstance(value, bool):
                return "REFUSED", "CONFIG.INVALID", None
            if not isinstance(value, int):
                return "REFUSED", "CONFIG.INVALID", None
        else:
            say(f"type-check:{field}")
            if not isinstance(value, str):
                return "REFUSED", "CONFIG.INVALID", None
    # Only now may content be compared.  Every step above is a TYPE step.
    say("compare:schemaVersion")
    if record["schemaVersion"] != 1:
        return "REFUSED", "CONFIG.INVALID", None
    for field in ("maxAgeSeconds", "maxTotalBytes", "keepCount"):
        say(f"compare:{field}")
        if record[field] < 0:
            return "REFUSED", "CONFIG.INVALID", None
    say("compare:boundsRevision")
    if record["boundsRevision"] < 1:
        return "REFUSED", "CONFIG.INVALID", None
    # DEP-RT25-01.  No reviewed surface carries a per-object admission time, so
    # a non-zero maxAgeSeconds is REFUSED.  There is no skip branch to reach.
    say("compare:maxAgeSeconds-satisfiability")
    if record["maxAgeSeconds"] != 0:
        return "REFUSED", "CONFIG.INVALID", None
    say("admit")
    return "ADMITTED", None, record


def admit_bounds_SILENT_REVERT(record: Any) -> tuple[str, str | None, dict | None]:
    """REJECTED READING for PC-V-05: the shipping product's substitution.

    A negative or non-finite configured value silently reverts to the built-in
    default rather than to 0.  The direction is toward MORE deletion than the
    operator asked for.
    """
    if record is ABSENT:
        return "ABSENT", None, None
    out = dict(record)
    for field, default in (("maxAgeSeconds", PRODUCT_MAX_AGE_SECONDS),
                           ("maxTotalBytes", PRODUCT_MAX_TOTAL_BYTES),
                           ("keepCount", PRODUCT_KEEP)):
        value = out.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            out[field] = default
    return "ADMITTED", None, out


def admit_bounds_COERCING(record: Any) -> tuple[str, str | None, dict | None]:
    """REJECTED READING for PC-V-06/07/08: bare equality / coercion at admission.

    `True == 1`, `200.0 == 200` and `int("200") == 200` all hold, so every one of
    the three law-18 controls is ADMITTED with a live bound.
    """
    if record is ABSENT:
        return "ABSENT", None, None
    out = dict(record)
    for field in ("maxAgeSeconds", "maxTotalBytes", "keepCount", "boundsRevision"):
        value = out.get(field)
        try:
            out[field] = int(value)          # coerces bool, float and str alike
        except (TypeError, ValueError):
            return "REFUSED", "CONFIG.INVALID", None
    return "ADMITTED", None, out


def admit_bounds_SILENT_SKIP(record: Any) -> tuple[str, str | None, dict | None]:
    """REJECTED READING for PC-V-09: an unsatisfiable dimension is silently skipped.

    The record is ADMITTED and the configured age bound simply never fires --
    "the parasitic size bound wearing different clothes".
    """
    if record is ABSENT:
        return "ABSENT", None, None
    verdict, code, admitted = admit_bounds(dict(record, maxAgeSeconds=0))
    if verdict != "ADMITTED":
        return verdict, code, None
    return "ADMITTED", None, dict(record)


def effective_bounds(record: Any) -> tuple[int, int, int, str]:
    """effective_bounds(ProjectRetentionBoundsV1 | ABSENT).  Total by construction."""
    if record is ABSENT:
        return 0, 0, 0, "DEFAULTED"
    return (record["maxAgeSeconds"], record["maxTotalBytes"], record["keepCount"],
            "CONFIGURED")


def effective_bounds_PRODUCT_DEFAULTS(record: Any) -> tuple[int, int, int, str]:
    """REJECTED READING for PC-V-12: absent bounds read as the product's values."""
    if record is ABSENT:
        return (PRODUCT_MAX_AGE_SECONDS, PRODUCT_MAX_TOTAL_BYTES, PRODUCT_KEEP,
                "DEFAULTED")
    return effective_bounds(record)


# --- Part C: the eviction order and the demands.

def eviction_order(evictable: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ascending atSequence, tiebroken by recordCasRef lexicographic ascending.

    Reads no clock.  The tiebreak is what makes the order TOTAL rather than a
    preorder; RT25-C-INV-03 requires the total order because the prefix property
    depends on it.
    """
    return sorted(evictable, key=lambda o: (o["atSequence"], o["recordCasRef"]))


def order_is_total(evictable: list[dict[str, Any]]) -> bool:
    keys = [(o["atSequence"], o["recordCasRef"]) for o in evictable]
    return len(set(keys)) == len(keys)


def demand_count(keep_count: int, order: list[dict[str, Any]]) -> int:
    """Reads keepCount and the order.  No other bound's value appears."""
    if keep_count == 0:                       # disabledWhen: keepCount == 0
        return 0
    return max(0, len(order) - keep_count)


def demand_size(max_total_bytes: int, order: list[dict[str, Any]]) -> int:
    """Reads maxTotalBytes and the order.  No other bound's value appears."""
    if max_total_bytes == 0:                  # disabledWhen: maxTotalBytes == 0
        return 0
    sizes = [o["bytes"] for o in order]
    for k in range(len(order) + 1):
        if sum(sizes[k:]) <= max_total_bytes:
            return k
    return len(order)


def demand_time(max_age_seconds: int, order: list[dict[str, Any]]) -> int:
    """Reads maxAgeSeconds and the order.  No other bound's value appears.

    DEP-RT25-01: no reviewed surface carries a per-raw-object admission time, so
    the only admissible value is 0 and admission refuses anything else.  Reaching
    this function with a non-zero value is unreachable through admit_bounds, and
    it REFUSES rather than skipping if it ever is reached.
    """
    if max_age_seconds == 0:                  # disabledWhen: maxAgeSeconds == 0
        return 0
    raise RefusedError(
        "maxAgeSeconds != 0 has no per-raw-object admission time to evaluate "
        "against; DEP-RT25-01 is unresolved and admission refuses this record")


# --- RT25-C-B1.  The SAME three demands, implemented EXACTLY AS PUBLISHED at
# --- $.partC_retentionBounds.sweep.demands.rows[].demand, with no outer guard.
# --- These are not a strawman: the artifact calls those rows executable and a
# --- reader implementing from them writes precisely this.

def demand_count_AS_PUBLISHED(keep_count: int, order: list[dict[str, Any]]) -> int:
    """`max(0, len(evictable) - keepCount)` -- verbatim.  At keepCount 0 this is
    len(evictable): the value declared to DISABLE the dimension evicts the whole
    set."""
    return max(0, len(order) - keep_count)


def demand_size_AS_PUBLISHED(max_total_bytes: int, order: list[dict[str, Any]]) -> int:
    """`the smallest k such that total_bytes(evictable[k:]) <= maxTotalBytes, or
    len(evictable) if no such k exists` -- verbatim.  At maxTotalBytes 0 the only
    satisfying k is len(evictable), because only the empty suffix sums to <= 0."""
    sizes = [o["bytes"] for o in order]
    for k in range(len(order) + 1):
        if sum(sizes[k:]) <= max_total_bytes:
            return k
    return len(order)


def demand_time_AS_PUBLISHED(max_age_seconds: int, order: list[dict[str, Any]],
                             now: int) -> int:
    """`the number of leading members of the eviction order whose admission time
    is older than now - maxAgeSeconds` -- verbatim.  At maxAgeSeconds 0 the
    threshold is `now`, and every already-admitted record is older than now, so
    the demand is len(evictable).

    DEP-RT25-01 forces maxAgeSeconds to 0, so 0 is not an edge case here -- it is
    the ONLY legal value, and it is the catastrophic one.
    """
    threshold = now - max_age_seconds
    n = 0
    for obj in order:
        if obj["admittedAt"] < threshold:
            n += 1
        else:
            break
    return n


def demands(bounds: tuple[int, int, int], order: list[dict[str, Any]]) -> dict[str, int]:
    """GUARDED reading: `disabledWhen` applied as an outer guard.  This is the
    only reading under which all five arithmetic vectors agree."""
    max_age, max_bytes, keep = bounds
    return {"time": demand_time(max_age, order),
            "size": demand_size(max_bytes, order),
            "count": demand_count(keep, order)}


def demands_AS_PUBLISHED(bounds: tuple[int, int, int], order: list[dict[str, Any]],
                         now: int = 10 ** 9) -> dict[str, int]:
    max_age, max_bytes, keep = bounds
    return {"time": demand_time_AS_PUBLISHED(max_age, order, now),
            "size": demand_size_AS_PUBLISHED(max_bytes, order),
            "count": demand_count_AS_PUBLISHED(keep, order)}


def eviction_count_AS_PUBLISHED(bounds: tuple[int, int, int],
                                order: list[dict[str, Any]]) -> int:
    return max(demands_AS_PUBLISHED(bounds, order).values())


def eviction_count(bounds: tuple[int, int, int],
                   order: list[dict[str, Any]]) -> int:
    """evictionCount := max(demand_count, demand_size, demand_time)."""
    return max(demands(bounds, order).values())


def eviction_count_SUM(bounds: tuple[int, int, int],
                       order: list[dict[str, Any]]) -> int:
    """REJECTED READING for PC-V-04: demands summed rather than maxed."""
    return sum(demands(bounds, order).values())


def eviction_count_PARASITIC(bounds: tuple[int, int, int],
                             order: list[dict[str, Any]]) -> int:
    """REJECTED READING for PC-V-02 and PC-V-03: the shipping product's defect.

    The size bound is computed INSIDE the count bound's branch, guarded by a test
    of the form `if aggressiveKeep <= 0 or configuredKeep <= 1: return`.  With
    keep set to 0 or 1, maxSizeMb silently deletes nothing.  Both arms of the
    disjunction are exercised, because a control exercising only one would pass
    against a half-repaired implementation.
    """
    max_age, max_bytes, keep = bounds
    aggressive_keep = keep // 2
    if aggressive_keep <= 0 or keep <= 1:
        return 0                              # size never evaluated
    return max(demand_count(keep, order), demand_size(max_bytes, order))


def evicted_set(bounds: tuple[int, int, int],
                order: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return order[:eviction_count(bounds, order)]


def attribute_causes(bounds: tuple[int, int, int],
                     order: list[dict[str, Any]]) -> list[str]:
    """One cause per evicted record: the LARGEST covering demand, ties broken in
    the fixed order AGE, SIZE, COUNT."""
    per = demands(bounds, order)
    out: list[str] = []
    for index in range(eviction_count(bounds, order)):
        covering = [dim for dim in ("time", "size", "count") if per[dim] > index]
        largest = max(per[dim] for dim in covering)
        winners = [dim for dim in covering if per[dim] == largest]
        names = [DIMENSION_CAUSE[dim] for dim in winners]
        out.append(next(c for c in CAUSE_TIEBREAK if c in names))
    return out


def over_bound(footprint: int, max_total_bytes: int,
               evictable: list[dict[str, Any]]) -> bool:
    """DERIVED, NOT RECORDED.  Both operands are already readable."""
    return footprint > max_total_bytes and not evictable


def admit_write(_bounds: tuple[int, int, int], _footprint: int,
                _evictable: list[dict[str, Any]]) -> str:
    """A bound is a TRIGGER, not a GATE.  There is no argument for which this
    returns REFUSE, and RT25-C-INV-07 proves that by enumeration."""
    return "ADMITTED"


def admit_write_THROWING(bounds: tuple[int, int, int], footprint: int,
                         evictable: list[dict[str, Any]]) -> str:
    """REJECTED READING for PC-V-10: the graph snapshot store throws and refuses."""
    _, max_bytes, _ = bounds
    if max_bytes and footprint > max_bytes and not evictable:
        return "REFUSED"
    return "ADMITTED"


def admit_transition(entry: Any) -> tuple[str, str | None]:
    """AvailabilityTransitionV1 admission, for the closed PURGED cause partition.

    cause is admitted as a JSON string AT EXACT TYPE before its content is
    compared.  A boolean is not a string, a number is not a string and null is
    not a string, at any depth.
    """
    if not isinstance(entry, dict):
        return "REFUSED", "CONFIG.INVALID"
    if entry.get("toState") != "PURGED":
        return "ADMITTED", None              # other partitions are open, DEP-RT25-04
    if "cause" not in entry:
        return "REFUSED", "CONFIG.INVALID"
    cause = entry["cause"]
    if isinstance(cause, bool) or not isinstance(cause, str):
        return "REFUSED", "CONFIG.INVALID"   # exact type BEFORE content
    if cause not in CAUSE_PARTITION:
        return "REFUSED", "CONFIG.INVALID"
    return "ADMITTED", None


def evictable_set(fold: dict[tuple, str]) -> list[tuple]:
    """Exactly the raw keys whose folded state is AVAILABLE.  OUTAGE is never
    evictable: it is reversible and PURGED is terminal."""
    return [key for key, state in fold.items() if state == "AVAILABLE"]


def retention_sweep(bounds: tuple[int, int, int], evictable: list[dict[str, Any]],
                    project_id: str, start_sequence: int) -> tuple[list[dict[str, Any]],
                                                                   set[str]]:
    """Emits AvailabilityTransitionV1 entries with toState PURGED and no other.

    Returns (entries, touched), where `touched` names every mutation surface the
    sweep claims.  RT25-C-INV-12 requires `touched` to be a subset of
    purgeMutationBoundary.mutatesExactly and disjoint from doesNotMutate.
    """
    order = eviction_order(evictable)
    causes = attribute_causes(bounds, order)
    entries: list[dict[str, Any]] = []
    sequence = start_sequence
    for obj, cause in zip(order, causes):
        sequence += 1
        entries.append({"schemaVersion": 1, "projectId": project_id,
                        "recordCasRef": obj["recordCasRef"],
                        "recordKind": obj["recordKind"], "toState": "PURGED",
                        "atSequence": sequence, "cause": cause})
    touched: set[str] = set()
    if entries:
        touched = {"rawObjectBytes", "unitAvailabilityLedger"}
    return entries, touched


def retention_sweep_RAISING(bounds: tuple[int, int, int],
                            evictable: list[dict[str, Any]], project_id: str,
                            start_sequence: int) -> list[dict[str, Any]]:
    """POSITIVE CONTROL for RT25-C-INV-01: a sweep that emits a non-PURGED
    transition and therefore CAN raise effectiveCapability."""
    entries, _ = retention_sweep(bounds, evictable, project_id, start_sequence)
    if entries:
        entries[0] = dict(entries[0], toState="AVAILABLE")
        entries[0].pop("cause", None)
    return entries


# --- Part D: the posture resolution.

def effective_posture(policy: Any) -> tuple[str, str]:
    """effective_posture(ProjectRetentionPolicyV1 | ABSENT).  Total, pure, no clock."""
    if policy is ABSENT:
        return "DURABLE_RETAINED", "DEFAULTED"
    if not isinstance(policy, dict):
        raise RefusedError("policy is neither ABSENT nor a record")
    posture = policy.get("posture")
    if isinstance(posture, bool) or not isinstance(posture, str):
        raise RefusedError("posture is not an exact-typed string")
    if posture not in POSTURE_ENUM:
        raise RefusedError(f"posture {posture!r} outside the closed enum")
    return posture, "CONSENTED"


def durable_authoritative_outcome(policy: Any) -> str:
    """Refused if and only if the effective posture is EPHEMERAL_ONLY.

    There is no branch producing ephemeral evidence for a durable-authoritative
    request, which is why the default removes a refusal without opening a
    demotion (freeze law 14, first clause).
    """
    posture, _ = effective_posture(policy)
    return "REFUSE" if posture == "EPHEMERAL_ONLY" else "PROCEED-DURABLE"


def durable_authoritative_outcome_NO_REFUSAL(policy: Any) -> str:
    """REJECTED READING for PC-V-14: the default removes every retention refusal."""
    effective_posture(policy)
    return "PROCEED-DURABLE"


def resolve_and_maybe_persist(policy: Any, interaction: str) -> tuple[str, str, Any]:
    """Returns (posture, provenance, policyWrittenToDisk).

    RT25-D-INV-03: no code path persists a policy whose posture came from the
    default.  The only writer is an ANSWER.
    """
    posture, provenance = effective_posture(policy)
    if policy is ABSENT and interaction in ("ANSWERED-RETAIN", "ANSWERED-EPHEMERAL"):
        answered = ("DURABLE_RETAINED" if interaction == "ANSWERED-RETAIN"
                    else "EPHEMERAL_ONLY")
        return answered, "CONSENTED", {"posture": answered}
    return posture, provenance, (policy if policy is not ABSENT else None)


def resolve_and_maybe_persist_PERSISTING(policy: Any,
                                         interaction: str) -> tuple[str, str, Any]:
    """REJECTED READING for PC-V-15: the resolution persists what it resolved,
    manufacturing CONSENTED provenance from a default."""
    posture, provenance, written = resolve_and_maybe_persist(policy, interaction)
    if policy is ABSENT and written is None:
        return posture, provenance, {"posture": posture}
    return posture, provenance, written


def ask_performed(profile: str, policy: Any, custody: str,
                  prior_dismissals: int) -> bool:
    """The ask exists to obtain consent provenance.  A dismissal does not
    suppress the next ask, and the risk direction under the new default is
    unconsented retention rather than under-retention."""
    del prior_dismissals                      # deliberately unread
    return (profile == "local-interactive" and policy is ABSENT
            and custody == "DURABLE_AUTHORITATIVE")


def ask_performed_SUPPRESSING(profile: str, policy: Any, custody: str,
                              prior_dismissals: int) -> bool:
    """REJECTED READING for PC-V-16: a dismissal suppresses the next ask."""
    if prior_dismissals:
        return False
    return ask_performed(profile, policy, custody, 0)


# ===========================================================================
# SECTION 2 -- LEAF CENSUS AND THE EXACT-TYPE SWEEP.
# ===========================================================================

_STEP = re.compile(r"\[\d+\]$")


def _walk_path_keys(path: str) -> list[Any]:
    """Robust JSONPath-lite splitter for the shapes this artifact uses."""
    out: list[Any] = []
    for token in re.findall(r"\.([A-Za-z0-9_\-]+)|\[(\d+)\]", path):
        name, index = token
        out.append(name if name else int(index))
    return out


def get_path(doc: Any, path: str, default: Any = None) -> Any:
    node = doc
    for key in _walk_path_keys(path):
        try:
            node = node[key]
        except (KeyError, IndexError, TypeError):
            return default
    return node


def set_path(doc: Any, path: str, value: Any) -> None:
    keys = _walk_path_keys(path)
    node = doc
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = value


def del_path(doc: Any, path: str) -> None:
    keys = _walk_path_keys(path)
    node = doc
    for key in keys[:-1]:
        node = node[key]
    del node[keys[-1]]


def scalar_leaves(node: Any, path: str = "$") -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            out.extend(scalar_leaves(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out.extend(scalar_leaves(value, f"{path}[{index}]"))
    else:
        out.append((path, node))
    return out


def leaf_name(path: str) -> str:
    return _STEP.sub("", path).split(".")[-1]


def census(doc: Any) -> dict[str, Any]:
    """Re-walked from the parsed bytes.  bool is tested BEFORE int, because in
    Python bool subclasses int and testing int first would silently classify
    every boolean as an integer -- the same exact-type class law 18 exists to
    prevent, applied to the census instrument itself."""
    counts = {"int": 0, "bool": 0, "float": 0, "null": 0, "str": 0}
    floats: list[str] = []
    nulls: list[str] = []
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
    counts["scalar"] = sum(counts[k] for k in ("int", "bool", "float", "null", "str"))
    counts["nonString"] = counts["scalar"] - counts["str"]
    return {"counts": counts, "floatLeafPaths": sorted(floats),
            "nullLeafPaths": sorted(nulls)}


# The three deliberate law-18 controls, keyed POSITIONALLY.  Everything else
# named `keepCount` in this artifact is an ordinary integer.
KEEPCOUNT_BOOL_PATH = "$.partC_retentionBounds.vectors.rows[5].bounds.keepCount"
KEEPCOUNT_FLOAT_PATH = "$.partC_retentionBounds.vectors.rows[6].bounds.keepCount"
KEEPCOUNT_STRING_PATH = "$.partC_retentionBounds.vectors.rows[7].bounds.keepCount"

# Hand-transcribed, never read from the data being checked: a registry sized
# from the artifact cannot police that artifact (7.2.2 corollary).  A new
# int/bool leaf under a name absent from both sets is UNRULED and is a finding.
INT_LEAF_NAMES = frozenset({
    "adoptionsRestingOnlyOnProductEvidence",
    "adoptionsWithAnIndependentCorpusJustification", "amendmentDraftsApplied",
    "architecturalRecommendationsOverridden", "askPerformedCellCountAfter",
    "askPerformedCellCountBefore", "availabilityStatesAfter",
    "availabilityStatesBefore", "boolLeafPositions", "case",
    "causeComparisonsReRunHere", "cellCount", "cellsChanged", "cellsFoundChanged",
    "cellsUnchanged", "censusWalksPerformed", "codesAddedByThisArtifact", "count",
    "decisionTableCells", "declaredDependencyCount", "deduplicationCasesConsidered",
    "deficiencyMemberCount", "deficiencyMembersAddedByThisArtifact",
    "deficiencyMembersMatchingPredicate", "derivedExitCode", "digestsRecordedCount",
    "duplicateKeysFound", "effectiveCapabilityForbiddenInputsAfter",
    "effectiveCapabilityForbiddenInputsBefore", "effectiveCapabilityInputsAfter",
    "effectiveCapabilityInputsBefore", "errorCodeCount",
    "errorCodesAddedByThisArtifact", "errorCodesMatchingPredicate",
    "evictableCount", "evictableTotalBytes", "exhaustiveDerivationsReRunHere",
    "exitCode", "expectedEvictionCount", "fieldCount", "fieldsAdded",
    "fieldsRemoved", "fieldsReordered", "filesCreated", "filesEdited",
    "filesWrittenByThisArtifact", "floatLeafPositions", "footprintModelsSpecified",
    "frozenArtifactCount", "howManyReasonCodesAreRequested",
    "identityRecipeVersionAfter", "identityRecipeVersionBefore",
    "independentReviewsOfTheseBytes", "independentReviewsOfThisArtifact",
    "inputsActuallyGated", "intLeafPositions", "intentClausesConstitutedAsDecisions",
    "intentClausesRecorded", "interactionOutcomes", "invariantCount", "keepCount",
    "invariantsDeclared", "invariantsMechanicallyChecked", "item",
    "ledgerEntryOrderedFieldsAfter", "ledgerEntryOrderedFieldsBefore",
    "ledgerEntryTypesAfter", "ledgerEntryTypesBefore", "maxAgeSeconds",
    "maxTotalBytes", "memberCount", "mutationArmsRun", "mutationSweepsRun", "n",
    "negativeControlCount", "newAvailabilityStates",
    "newAvailabilityStatesIntroduced", "newLedgerEntries",
    "newLedgerMutationsIntroduced", "newRecordTypes", "newRecordTypesIntroduced",
    "newResidualCount", "noAskCaseCount", "noAskCasesReDerivedCount",
    "noAskCasesSilentlyDeleted", "nonControlRowCount", "nonStringLeafPositions",
    "nullLeafPositions", "orderedFieldsAfter", "orderedFieldsBefore",
    "orderedPosition", "outcomesAffected", "outcomesChanged",
    "outcomesFoundChanged", "outcomesNeedingRecomputation", "outcomesRecomputed",
    "outcomesRecomputedHere", "outcomesUnchanged", "partABlockingFindingCount",
    "partASurfacesSearchedByInstrument", "partBBlockingFindingCount",
    "partBSurfacesLeftUnchanged", "partBSurfacesProposedForChange",
    "partBSurfacesTouchedByThePostureDecision", "policyPersistingOutcomesUnchanged",
    "postureEnumMembersAdded", "postureEnumMembersAfter", "postureEnumMembersBefore",
    "predecessorHardPinnedInputs", "predecessorMutationArmsRun",
    "predecessorRetainedCheckers", "productClaimsReMeasuredHere",
    "productClaimsRecorded", "productPacketAmendments", "purgeDoesNotMutateAfter",
    "purgeDoesNotMutateBefore", "purgeMutatesExactlyAfter",
    "purgeMutatesExactlyBefore", "randomisedTrialsReRunHere", "realObjectsMeasured",
    "reasonCodeCount", "reasonCodesMatchingPredicate", "recipeVersion",
    "recordedInputs", "recordsAddedToTheSurface", "resolutionRulesAddedToTheSurface",
    "resultUnderRejectedReading", "retainedCheckers", "retainedResidualCount",
    "reviewedRecordShapesEdited", "rowCount", "scalarLeafPositions",
    "stringLeafPositions", "structuralArgumentsOffered", "surfacesChangedCount",
    "surfacesExplicitlyUnchangedCount", "terminalStatesAfter", "terminalStatesBefore",
    "totalBlockingFindingCount", "typedRefusalKindsAfter", "typedRefusalKindsBefore",
    "unsetFieldsTouched", "vectorsDeclared", "vectorsExecuted",
    "verifiedPropertiesTouched", "version",
})

BOOL_LEAF_NAMES = frozenset({
    "aPurgedEntryWithACauseOutsideThePartitionIsRefused",
    "aPurgedEntryWithNoCauseIsRefused", "aReviewerMayDisagree",
    "absenceIsADistinctState", "absenceStateNameRetained",
    "absentAndAllZeroAgreeOnValuesAndDifferOnProvenance",
    "agreesWithTheShippingProduct", "allFourStillPersistNoPolicy", "answeredHere",
    "appendsToTheExistingLedger", "appliedByThisArtifact", "askStillPerformed",
    "atMostOnePerProject", "bindsNothing", "boundsRecordPresent",
    "butTheClaimItCarriedIsWithdrawn", "bytesAreReclaimedFromObjectsNeverFromTheLedger",
    "callersCannotSupplyIt", "canItHaveBounds", "carriedForwardUnchanged",
    "cellCountUnchanged", "censusIncludesItsOwnIntegers", "changesAnyOtherArtifact",
    "changesAnyStatus", "claimSplit", "closed", "closedByThisArtifact",
    "codeAlreadyExistsInTheLiveVocabulary", "constitutedInTheBindingPacket",
    "constitutesASealOrSignature", "countUnchanged", "derivedNotEnumerated",
    "emitsNoOtherToState", "everyFloatIsDeliberate", "everyPurgedEntryCarriesACause",
    "exactlyOneCausePerEntry", "executed", "executionIdAllocatedWhileTheQuestionIsOpen",
    "expectedEqual", "expectedFirstRunAskPerformed", "expectedOverBound",
    "expectedPolicyPersisted", "expectedSecondRunAskPerformed", "fieldIsNotNew",
    "fixedPointReached", "fromUnderRetentionToUnconsentedRetention", "global",
    "hasACauseMember", "hasNoDefaultField", "introducesNoNewMutation",
    "isATriggerNotAGate", "isAlgebraicallyMonotone", "isDerivedFromEffectivePosture",
    "isDerivedFromTheTable", "isDerivedNotPreferred", "isDeterministic",
    "isItAlreadyTrue", "isItReachableUnderTheNewDefault", "isNegativeControl",
    "isOpen", "isPure", "isTheRiskiestPartOfThisChange", "isThisANewReason",
    "isThisANewRule", "isThisArtifactBlockedByThat", "isTotal", "mayAmendD9Vocabulary",
    "mayAmendOperabilityGates", "mayAmendTheProductDispositionPacket",
    "mayAmendThreatModel", "mayApplyTheCdRt5AmendmentDraft", "mayCiteAProductDecision",
    "mayConstituteAProductDecision", "measuredPresent",
    "negativeOrNonIntegerIsRefusedNotDefaulted", "neitherIsAdoptedUnchanged",
    "neverReturnsAbsent", "noBoundCanShrinkIt", "noInputWasWritten",
    "noPostureEnumMemberIsAdded", "notAResolvedConfigurationLayer", "notInTheWorktree",
    "notSilentlySkipped", "notUnderTheAnalysisSnapshotRoot", "outageIsNeverEvictable",
    "partAPrimeDependsOnPartD", "partCDependsOnPartD", "perProject",
    "planDigestConfirmedUnchanged", "policyPersistedByThisCell",
    "policyPersistedOnlyByTheAnswer", "policyPersistingOutcomeCountUnchanged",
    "policyPresent", "positionUnchanged", "postureEnumIsClosed",
    "predecessorIsNotEdited", "predecessorValue", "predecessorVerdictStillApplies",
    "protectedSetIsNotEvictableByAnyBound", "provenanceEnumIsClosed",
    "provenanceIsNeverPersisted", "quotedNotParaphrased",
    "reParsedWithDuplicateKeyRejectingHook", "reRunByThisArtifact", "readsNoClock",
    "readsNoOtherBoundsValue", "readsNoOtherProject",
    "recordedIntentPostureIsNotAPacketValue", "refusalStillReachableInCi",
    "requiresNoNewTrials", "restatedByThisArtifact", "restatedNotDeleted",
    "reversibilityIsAFeatureOfTheDesignNotAPredictionAboutTheProduct",
    "sameOrderForEveryDimension", "satisfiableToday", "silentDemotionIsStillForbidden",
    "soAbsenceIsNeverUnexplained", "soNoBoundEverFiresUntilSomeoneConfiguresOne",
    "soTheAskIsStillStrictlyBeforeAttemptAdmission", "soTheDefaultConfigurationNeverPurges",
    "successorValue", "terminatesAfter", "terminatesBefore",
    "theDefaultDesignedAgainstIsRecordedIntentNotAPacketValue",
    "theDefaultIsNeverWrittenToDisk", "theLedgerGrowsWithoutBound",
    "theRiskDirectionHasReversed", "theTwoHalvesOfThatAnswerAreDifferent",
    "thisIsNotABlockerOnTheDraft", "thisIsTheProductIntentDelivered", "unchanged",
    "unchangedFromThePredecessor", "valueUnchanged", "zeroDisables",
})


def type_findings(doc: Any) -> tuple[list[str], dict[str, int]]:
    """The exact-type rule over the artifact's own leaves.

    Every int/bool/float/null leaf must match the type its NAME declares, except
    the three deliberate law-18 controls, which are keyed POSITIONALLY and whose
    spellings are REQUIRED to stay bool / float / string.  An int/bool leaf whose
    name is in neither set is UNRULED, and unruled must be 0.
    """
    findings: list[str] = []
    counts = {"scalarLeafPositions": 0, "intLeafPositions": 0, "boolLeafPositions": 0,
              "floatLeafPositions": 0, "nullLeafPositions": 0, "stringLeafPositions": 0,
              "guardedIntOrBoolLeafPositions": 0, "unruledIntOrBoolLeafPositions": 0}
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

        if path == KEEPCOUNT_BOOL_PATH:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if not isinstance(value, bool):
                findings.append(
                    f"RT25-TYPE {path}: PC-V-06-EXACT-TYPE-BOOL's payload MUST stay a "
                    f"JSON boolean; a control spelled as an integer is not a control. "
                    f"got {type(value).__name__}")
            continue
        if path == KEEPCOUNT_FLOAT_PATH:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if isinstance(value, bool) or not isinstance(value, float):
                findings.append(
                    f"RT25-TYPE {path}: PC-V-07-EXACT-TYPE-FLOAT's payload MUST stay a "
                    f"JSON float; the artifact's ONLY float leaf is this law-18 "
                    f"control. got {type(value).__name__}")
            continue
        if path == KEEPCOUNT_STRING_PATH:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if isinstance(value, bool) or not isinstance(value, str):
                findings.append(
                    f"RT25-TYPE {path}: PC-V-08-EXACT-TYPE-NUMERIC-STRING's payload "
                    f"MUST stay a JSON string. got {type(value).__name__}")
            continue

        if value is None:
            findings.append(
                f"RT25-TYPE {path}: null leaf, but $.leafCensus records "
                f"nullLeafPositions 0 and an empty nullLeafPaths")
            continue
        if isinstance(value, float):
            findings.append(
                f"RT25-TYPE {path}: float leaf outside the single declared law-18 "
                f"float control at {KEEPCOUNT_FLOAT_PATH}")
            continue
        if isinstance(value, (bool, int)):
            name = leaf_name(path)
            if name in BOOL_LEAF_NAMES:
                counts["guardedIntOrBoolLeafPositions"] += 1
                if not isinstance(value, bool):
                    findings.append(
                        f"RT25-TYPE {path}: {name!r} is a declarative flag and must be "
                        f"a JSON boolean; got {type(value).__name__} {value!r}")
            elif name in INT_LEAF_NAMES:
                counts["guardedIntOrBoolLeafPositions"] += 1
                if isinstance(value, bool):
                    findings.append(
                        f"RT25-TYPE {path}: {name!r} is a counted integer and must not "
                        f"be a JSON boolean (bool subclasses int in Python, which is "
                        f"why this is tested first)")
            else:
                counts["unruledIntOrBoolLeafPositions"] += 1
                findings.append(
                    f"RT25-TYPE {path}: int/bool leaf under UNRULED name {name!r}; "
                    f"the type registry is hand-transcribed and must cover every "
                    f"position, so an unruled leaf is an uncovered position")
    return findings, counts


def hostile_sweep(doc: Any, base_findings: list[str]) -> dict[str, Any]:
    """Respell every int/bool leaf three ways and require each to be rejected.

    IMPLEMENTATION-FREEZE 7 dominant failure mode: a coverage claim quantifying
    over a region the instrument cannot observe.  Every position is enumerated
    and injected; counts are recomputed on every run.
    """
    positions = [(p, v) for p, v in scalar_leaves(doc)
                 if isinstance(v, bool) or (isinstance(v, int) and not isinstance(v, bool))]
    arms = {
        "float": lambda v: float(v) if not isinstance(v, bool) else None,
        "boolFromZeroOrOneInt": lambda v: (bool(v) if not isinstance(v, bool)
                                           and v in (0, 1) else None),
        "intFromBool": lambda v: (1 if v else 0) if isinstance(v, bool) else None,
    }
    result: dict[str, Any] = {}
    for arm, spell in arms.items():
        swept = admitted = by_position = collateral = 0
        escapes: list[str] = []
        for path, value in positions:
            replacement = spell(value)
            if replacement is None:
                continue
            swept += 1
            mutated = copy.deepcopy(doc)
            set_path(mutated, path, replacement)
            findings, _ = type_findings(mutated)
            new = [f for f in findings if f not in base_findings]
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
    return result


# ===========================================================================
# SECTION 3 -- VECTOR EXECUTION.
# All 16 rows of $.partC_retentionBounds.vectors.rows.  Every row is driven, and
# every row can fail.  Where a row is a negative control, the REJECTED reading it
# names is also executed and REQUIRED to produce the different result the row
# declares -- section 7.8's repair: exhibit an input that is WRONG, not merely
# EMPTY.  A control whose rejected reading agrees with the accepted one is
# reported as VACUOUS, which is itself a finding.
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
)

PROJECT = "prj1-" + "a" * 64


def population(count: int, total_bytes: int | None = None) -> list[dict[str, Any]]:
    """A synthetic evictable set.  atSequence ascending, distinct recordCasRefs,
    uniform byte sizes so the size demand is exactly reproducible."""
    each = 0 if not count else (total_bytes // count if total_bytes else 0)
    return [{"projectId": PROJECT,
             "recordCasRef": "sha256:" + f"{index:064x}",
             "recordKind": "file-bytes",
             "atSequence": index + 1,
             "admittedAt": 1000 + index,
             "bytes": each}
            for index in range(count)]


def bounds_record(max_age: Any = 0, max_bytes: Any = 0, keep: Any = 0,
                  **over: Any) -> dict[str, Any]:
    record = {"schemaVersion": 1, "projectId": PROJECT,
              "retentionPolicyId": "rpol1:sha256:" + "b" * 64,
              "maxAgeSeconds": max_age, "maxTotalBytes": max_bytes,
              "keepCount": keep, "boundsRevision": 1,
              "retentionBoundsId": "rbnd1:sha256:" + "c" * 64}
    record.update(over)
    return record


def _row_bounds(row: dict[str, Any]) -> tuple[int, int, int]:
    b = row.get("bounds") or {}
    return b.get("maxAgeSeconds"), b.get("maxTotalBytes"), b.get("keepCount")


def _arith_rows(doc: Any) -> list[dict[str, Any]]:
    """The rows that state an arithmetic expectation: an evictable population and
    an expectedEvictionCount.  Measured, never enumerated."""
    out = []
    for row in get_path(doc, "$.partC_retentionBounds.vectors.rows", []) or []:
        if "expectedEvictionCount" in row and "evictableCount" in row:
            out.append(row)
    return out


def measure_b1(doc: Any) -> dict[str, Any]:
    """RT25-C-B1.  Run every arithmetic vector under BOTH readings of the demand
    expressions and report which one the artifact's own vectors agree with.

    This is the central measurement of this instrument.  It is not an opinion
    about which reading is intended; it is a count of agreements, and the two
    counts cannot both be high.
    """
    rows = _arith_rows(doc)
    published_agree: list[str] = []
    published_disagree: list[dict[str, Any]] = []
    guarded_agree: list[str] = []
    guarded_disagree: list[dict[str, Any]] = []
    for row in rows:
        bounds = _row_bounds(row)
        if any(not isinstance(v, int) or isinstance(v, bool) for v in bounds):
            continue                       # a type control, not an arithmetic row
        order = eviction_order(population(row["evictableCount"],
                                          row.get("evictableTotalBytes")))
        expected = row["expectedEvictionCount"]
        pub = eviction_count_AS_PUBLISHED(bounds, order)
        if pub == expected:
            published_agree.append(row["id"])
        else:
            published_disagree.append({
                "id": row["id"], "bounds": bounds, "n": len(order),
                "expected": expected, "asPublished": pub,
                "perDimension": demands_AS_PUBLISHED(bounds, order)})
        try:
            grd = eviction_count(bounds, order)
        except RefusedError:
            grd = None
        if grd == expected:
            guarded_agree.append(row["id"])
        else:
            guarded_disagree.append({"id": row["id"], "expected": expected,
                                     "guarded": grd})

    # The default configuration of every unconfigured project.
    default_order = eviction_order(population(5, 500))
    default_published = eviction_count_AS_PUBLISHED((0, 0, 0), default_order)
    default_guarded = eviction_count((0, 0, 0), default_order)
    return {"arithmeticRows": len(rows),
            "publishedAgree": published_agree, "publishedDisagree": published_disagree,
            "guardedAgree": guarded_agree, "guardedDisagree": guarded_disagree,
            "defaultConfigEvictableCount": len(default_order),
            "defaultConfigAsPublished": default_published,
            "defaultConfigGuarded": default_guarded,
            "declaredDefaultSweepEmitsNothing":
                get_path(doc, "$.partC_retentionBounds.sweep."
                              "neverRunsWhenBoundsAreDefaulted."
                              "soTheDefaultConfigurationNeverPurges")}


def check_b1(doc: Any, ctx: dict[str, Any]) -> list[str]:
    b1 = ctx["b1"]
    findings: list[str] = []
    if b1["publishedDisagree"]:
        detail = "; ".join(
            f"{d['id']} bounds={d['bounds']} n={d['n']} expected {d['expected']} "
            f"but the published expressions give {d['asPublished']} "
            f"(time {d['perDimension']['time']}, size {d['perDimension']['size']}, "
            f"count {d['perDimension']['count']})"
            for d in b1["publishedDisagree"])
        findings.append(
            f"RT25-C-B1 $.partC_retentionBounds.sweep.demands.rows: "
            f"{len(b1['publishedDisagree'])} of {b1['arithmeticRows']} arithmetic "
            f"vectors CONTRADICT the artifact's own published demand expressions, "
            f"while {len(b1['guardedAgree'])} of {b1['arithmeticRows']} agree with "
            f"the guarded reading. The published expressions and the published "
            f"vectors cannot both be right. {detail}")
    if b1["defaultConfigAsPublished"] != 0:
        findings.append(
            f"RT25-C-B1 $.partC_retentionBounds.sweep.demands.rows: at the DEFAULT "
            f"configuration 0/0/0 -- the resolved bounds of every project that has "
            f"configured nothing -- the published expressions demand "
            f"{b1['defaultConfigAsPublished']} of {b1['defaultConfigEvictableCount']} "
            f"evictable records, i.e. the whole set, while "
            f"$.partC_retentionBounds.sweep.neverRunsWhenBoundsAreDefaulted"
            f".soTheDefaultConfigurationNeverPurges declares "
            f"{b1['declaredDefaultSweepEmitsNothing']!r} in the same file. The "
            f"guarded reading gives {b1['defaultConfigGuarded']}. Worst on the time "
            f"dimension: DEP-RT25-01 forces maxAgeSeconds to 0 and 0 is exactly the "
            f"value at which the published time expression demands everything.")
    if b1["guardedDisagree"]:
        findings.append(
            f"RT25-C-B1 the guarded reading does not rescue every row either: "
            f"{b1['guardedDisagree']}")
    return findings


def run_vectors(doc: Any, ctx: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    """Execute all 16 vectors.  Returns (findings, report)."""
    findings: list[str] = []
    executed: list[str] = []
    controls_run = 0
    controls_vacuous: list[str] = []

    def fail(vid: str, detail: str) -> None:
        findings.append(f"RT25-VEC {vid}: {detail}")

    def control(vid: str, accepted: Any, rejected: Any, declared: Any = None) -> None:
        nonlocal controls_run
        controls_run += 1
        if accepted == rejected:
            controls_vacuous.append(vid)
            fail(vid, f"VACUOUS CONTROL: the rejected reading produces the same "
                      f"result as the accepted one ({accepted!r}); a control that "
                      f"cannot separate the two readings measures nothing")
        elif declared is not None and rejected != declared:
            fail(vid, f"the rejected reading produces {rejected!r} but the row "
                      f"declares resultUnderRejectedReading {declared!r}")

    rows = {r.get("id"): r for r in
            get_path(doc, "$.partC_retentionBounds.vectors.rows", []) or []}
    missing = [v for v in VECTOR_IDS if v not in rows]
    if missing:
        findings.append(
            f"RT25-VEC $.partC_retentionBounds.vectors.rows: the executed vector "
            f"registry names {missing}, which the artifact does not carry")
    extra = [v for v in rows if v not in VECTOR_IDS]
    if extra:
        findings.append(
            f"RT25-VEC $.partC_retentionBounds.vectors.rows: {extra} present in the "
            f"artifact and NOT executed by this instrument; an unexecuted row is "
            f"exactly the residual this checker exists to close")

    # -- PC-V-01 ------------------------------------------------------------
    vid = "PC-V-01-COUNT-ONLY"
    if vid in rows:
        row = rows[vid]
        order = eviction_order(population(row["evictableCount"]))
        got = eviction_count(_row_bounds(row), order)
        if got != row["expectedEvictionCount"]:
            fail(vid, f"guarded reading gives {got}, row expects "
                      f"{row['expectedEvictionCount']}")
        causes = set(attribute_causes(_row_bounds(row), order))
        if causes != set(row["expectedCauses"]):
            fail(vid, f"causes {sorted(causes)} != expected {row['expectedCauses']}")
        if row.get("isNegativeControl") is not False:
            fail(vid, "the row declares itself a negative control; the artifact's "
                      "nonControlRowCount says exactly one row is not")
        executed.append(vid)

    # -- PC-V-02 / PC-V-03: the parasitism controls -------------------------
    for vid, arm in (("PC-V-02-PARASITISM-CONTROL-KEEP-ZERO", "keep<=0"),
                     ("PC-V-03-PARASITISM-CONTROL-KEEP-ONE", "keep<=1")):
        if vid not in rows:
            continue
        row = rows[vid]
        order = eviction_order(population(row["evictableCount"],
                                          row["evictableTotalBytes"]))
        bounds = _row_bounds(row)
        got = eviction_count(bounds, order)
        if got != row["expectedEvictionCount"]:
            fail(vid, f"guarded reading gives {got}, row expects "
                      f"{row['expectedEvictionCount']} (arm {arm})")
        causes = set(attribute_causes(bounds, order))
        if causes != set(row["expectedCauses"]):
            fail(vid, f"causes {sorted(causes)} != expected {row['expectedCauses']}")
        parasitic = eviction_count_PARASITIC(bounds, order)
        control(vid, got, parasitic, row.get("resultUnderRejectedReading"))
        executed.append(vid)

    # -- PC-V-04: max, not sum ----------------------------------------------
    vid = "PC-V-04-INDEPENDENCE-MAX-NOT-SUM"
    if vid in rows:
        row = rows[vid]
        order = eviction_order(population(row["evictableCount"],
                                          row["evictableTotalBytes"]))
        bounds = _row_bounds(row)
        got = eviction_count(bounds, order)
        per = demands(bounds, order)
        if got != row["expectedEvictionCount"]:
            fail(vid, f"guarded reading gives {got}, row expects "
                      f"{row['expectedEvictionCount']}")
        note = row.get("note", "")
        if "size demand is 2" in note and per["size"] != 2:
            fail(vid, f"the row's note says the size demand is 2; measured "
                      f"{per['size']}")
        if "count demand is 3" in note and per["count"] != 3:
            fail(vid, f"the row's note says the count demand is 3; measured "
                      f"{per['count']}")
        summed = eviction_count_SUM(bounds, order)
        control(vid, got, summed, row.get("resultUnderRejectedReading"))
        executed.append(vid)

    # -- PC-V-05: silent revert ---------------------------------------------
    vid = "PC-V-05-SILENT-REVERT-CONTROL"
    if vid in rows:
        row = rows[vid]
        max_age, max_bytes, keep = _row_bounds(row)
        record = bounds_record(max_age, max_bytes, keep)
        verdict, code, admitted = admit_bounds(record)
        if verdict != row["expectedAdmission"]:
            fail(vid, f"admission is {verdict}, row expects {row['expectedAdmission']}")
        if code != row["expectedErrorCode"]:
            fail(vid, f"error code {code!r}, row expects {row['expectedErrorCode']!r}")
        if admitted is not None:
            fail(vid, "a refused record produced a substituted value; "
                      "structuralRepair claims no code path maps an invalid value "
                      "to a valid one")
        rverdict, _, radmitted = admit_bounds_SILENT_REVERT(record)
        rejected = f"{rverdict} keepCount={radmitted and radmitted.get('keepCount')}"
        control(vid, f"{verdict} keepCount=None", rejected)
        if radmitted is None or radmitted.get("keepCount") != PRODUCT_KEEP:
            fail(vid, f"the rejected reading must ADMIT with keepCount "
                      f"{PRODUCT_KEEP}, the live bound the operator tried to switch "
                      f"off; got {radmitted and radmitted.get('keepCount')}")
        executed.append(vid)

    # -- PC-V-06 / 07 / 08: law 18 exact-type controls ----------------------
    law18 = (("PC-V-06-EXACT-TYPE-BOOL", True, 1),
             ("PC-V-07-EXACT-TYPE-FLOAT", 200.0, 200),
             ("PC-V-08-EXACT-TYPE-NUMERIC-STRING", "200", 200))
    for vid, payload, coerced in law18:
        if vid not in rows:
            continue
        row = rows[vid]
        declared = (row.get("bounds") or {}).get("keepCount")
        if type(declared) is not type(payload) or declared != payload:
            fail(vid, f"the row's own payload is {declared!r} "
                      f"({type(declared).__name__}); this control requires "
                      f"{payload!r} ({type(payload).__name__}) and a control "
                      f"spelled as the accepted type is not a control")
        record = bounds_record(0, 0, payload)
        trace: list[str] = []
        verdict, code, admitted = admit_bounds(record, trace)
        if verdict != row["expectedAdmission"]:
            fail(vid, f"admission is {verdict}, row expects {row['expectedAdmission']}")
        if code != row["expectedErrorCode"]:
            fail(vid, f"error code {code!r}, row expects {row['expectedErrorCode']!r}")
        if admitted is not None:
            fail(vid, "a refused record produced an admitted value")
        # refusedBefore: any comparison of the value.  The trace is the proof.
        if any(step.startswith("compare:") for step in trace):
            fail(vid, f"law 18 requires refusal BEFORE any comparison of the value; "
                      f"the admission trace reached a comparison step: {trace}")
        cverdict, _, cadmitted = admit_bounds_COERCING(record)
        control(vid, f"{verdict}", f"{cverdict}")
        if cadmitted is None or cadmitted.get("keepCount") != coerced:
            fail(vid, f"the rejected reading must ADMIT as keepCount {coerced}; got "
                      f"{cadmitted and cadmitted.get('keepCount')}")
        executed.append(vid)

    # -- PC-V-09: the unsatisfiable age bound -------------------------------
    vid = "PC-V-09-UNSATISFIABLE-AGE-BOUND"
    if vid in rows:
        row = rows[vid]
        max_age, max_bytes, keep = _row_bounds(row)
        if max_age != PRODUCT_MAX_AGE_SECONDS:
            fail(vid, f"the row's note calls {max_age} the shipping product's 60-day "
                      f"default expressed exactly; 60*24*60*60 is "
                      f"{PRODUCT_MAX_AGE_SECONDS}")
        record = bounds_record(max_age, max_bytes, keep)
        verdict, code, admitted = admit_bounds(record)
        if verdict != row["expectedAdmission"] or code != row["expectedErrorCode"]:
            fail(vid, f"admission {verdict}/{code!r}, row expects "
                      f"{row['expectedAdmission']}/{row['expectedErrorCode']!r}")
        # The silent-skip path must be UNREACHABLE, not merely unused.  Enumerated.
        admitting = [v for v in (0, 1, 2, 59, 3600, 86400, PRODUCT_MAX_AGE_SECONDS,
                                 2 ** 31, 2 ** 63)
                     if admit_bounds(bounds_record(v, 0, 0))[0] == "ADMITTED"]
        if admitting != [0]:
            fail(vid, f"maxAgeSeconds values admitted: {admitting}; DEP-RT25-01 "
                      f"permits exactly [0] and every other value must be REFUSED, "
                      f"never silently skipped")
        sverdict, _, sadmitted = admit_bounds_SILENT_SKIP(record)
        control(vid, verdict, sverdict)
        if sadmitted is None or sadmitted.get("maxAgeSeconds") != max_age:
            fail(vid, "the rejected reading must ADMIT and carry the configured "
                      "60-day bound that then evicts nothing forever")
        else:
            order = eviction_order(population(5, 500))
            skipped = max(demand_size(0, order), demand_count(0, order))
            if skipped != 0:
                fail(vid, f"under the silently-skipped reading the configured bound "
                          f"must evict nothing; measured {skipped}")
        executed.append(vid)

    # -- PC-V-10: protected set exceeds the bound ---------------------------
    vid = "PC-V-10-PROTECTED-SET-EXCEEDS-BOUND"
    if vid in rows:
        row = rows[vid]
        bounds = _row_bounds(row)
        evictable = population(row["evictableCount"])
        footprint = 500
        verdict, code, _ = admit_bounds(bounds_record(*bounds))
        if verdict != "ADMITTED":
            fail(vid, f"the bounds record itself must be admissible; got "
                      f"{verdict}/{code!r}")
        got_write = admit_write(bounds, footprint, evictable)
        if got_write != row["expectedWriteAdmission"]:
            fail(vid, f"write admission {got_write}, row expects "
                      f"{row['expectedWriteAdmission']}")
        got_evict = eviction_count(bounds, eviction_order(evictable))
        if got_evict != row["expectedEvictionCount"]:
            fail(vid, f"eviction count {got_evict}, row expects "
                      f"{row['expectedEvictionCount']}")
        got_over = over_bound(footprint, bounds[1], evictable)
        if got_over != row["expectedOverBound"]:
            fail(vid, f"over_bound {got_over}, row expects {row['expectedOverBound']}")
        control(vid, got_write, admit_write_THROWING(bounds, footprint, evictable))
        executed.append(vid)

    # -- PC-V-11: cause blindness within PURGED -----------------------------
    vid = "PC-V-11-CAUSE-BLINDNESS-WITHIN-PURGED"
    if vid in rows:
        row = rows[vid]
        findings.extend(_drive_cause_blindness(row, ctx, vid, control))
        executed.append(vid)

    # -- PC-V-12: absent bounds resolve to unbounded ------------------------
    vid = "PC-V-12-ABSENT-BOUNDS-RESOLVE-TO-UNBOUNDED"
    if vid in rows:
        row = rows[vid]
        age, size, keep, prov = effective_bounds(ABSENT)
        spelled = f"{age} / {size} / {keep}"
        if spelled != row["expectedResolvedBounds"]:
            fail(vid, f"resolved bounds {spelled!r}, row expects "
                      f"{row['expectedResolvedBounds']!r}")
        if prov != row["expectedProvenance"]:
            fail(vid, f"provenance {prov!r}, row expects "
                      f"{row['expectedProvenance']!r}")
        order = eviction_order(population(5, 500))
        got = eviction_count((age, size, keep), order)
        if got != row["expectedEvictionCount"]:
            fail(vid, f"eviction count {got}, row expects "
                      f"{row['expectedEvictionCount']}")
        rejected = effective_bounds_PRODUCT_DEFAULTS(ABSENT)
        control(vid, (age, size, keep, prov), rejected)
        if rejected[:3] != (PRODUCT_MAX_AGE_SECONDS, PRODUCT_MAX_TOTAL_BYTES,
                            PRODUCT_KEEP):
            fail(vid, f"the rejected reading must resolve to the product's live "
                      f"defaults keep 200 / 60 days / 150 MB; got {rejected[:3]}")
        # the two readings are separable at admission as well as at resolution
        if admit_bounds(bounds_record(*rejected[:3]))[0] != "REFUSED":
            fail(vid, "the product's default maxAgeDays 60 must be REFUSED at "
                      "admission under DEP-RT25-01, which is a second independent "
                      "separation between the two readings")
        executed.append(vid)

    # -- PC-V-13..16: Part D and Part A-prime -------------------------------
    for vid in ("PC-V-13-ABSENT-POLICY-RESOLVES-DURABLE",
                "PC-V-14-EPHEMERAL-IS-ALWAYS-CONSENTED",
                "PC-V-15-DEFAULT-IS-NEVER-PERSISTED",
                "PC-V-16-DISMISSAL-DOES-NOT-SUPPRESS-THE-NEXT-ASK"):
        if vid not in rows:
            continue
        findings.extend(_drive_posture_vector(rows[vid], ctx, vid, control))
        executed.append(vid)

    report = {"declared": len(rows), "executed": len(set(executed)),
              "controlsRun": controls_run, "controlsVacuous": controls_vacuous}
    return findings, report


def _drive_cause_blindness(row: dict[str, Any], ctx: dict[str, Any], vid: str,
                           control: Any) -> list[str]:
    """PC-V-11, anchored on AF-03-VERIFY-PURGED in v22's PINNED bytes.

    Two ledgers identical except in `cause`.  The accepted derivation must agree;
    a deliberately cause-reading derivation must DISAGREE, or the comparison
    proves nothing.  A Poison in every cause field proves non-reading rather than
    arguing it.
    """
    findings: list[str] = []
    sbp = ctx["v22"]["semanticBasisProjection"]
    closure = sbp["semanticCapabilityClosure"]
    fixture = next((f for f in sbp["availabilityFixtures"]
                    if f["id"] == "AF-03-VERIFY-PURGED"), None)
    if fixture is None:
        return [f"RT25-VEC {vid}: AF-03-VERIFY-PURGED is absent from the pinned "
                f"retention-tiers.v22.json fixtures this row anchors on"]
    records = apply_states(sbp["unitAvailabilityRecords"], fixture["stateOverrides"])
    sealed = closure["sealedCapability"]
    units = closure["units"]

    def entry(cause: Any) -> dict[str, Any]:
        override = fixture["stateOverrides"][0]
        return {"schemaVersion": 1, "projectId": override["projectId"],
                "recordCasRef": override["recordCasRef"],
                "recordKind": override["recordKind"], "toState": "PURGED",
                "atSequence": 1, "cause": cause}

    results = {}
    for cause in CAUSE_PARTITION:
        ledger = [entry(cause)]
        fold_ledger(ledger)                # must not read `cause`
        results[cause] = effective_capability(sealed, units, records)
    if len(set(results.values())) != 1:
        findings.append(
            f"RT25-VEC {vid}: the four causes derive different capabilities "
            f"{results}; RT25-C-INV-05 requires them equal")
    expected = fixture["expectedEffectiveCapability"]
    if row.get("expectedEffectiveCapabilityA") != expected:
        findings.append(
            f"RT25-VEC {vid}: the row declares expectedEffectiveCapabilityA "
            f"{row.get('expectedEffectiveCapabilityA')!r}, but the anchor fixture "
            f"AF-03-VERIFY-PURGED in the pinned v22 bytes expects {expected!r}")
    for cause, got in results.items():
        if got != expected:
            findings.append(
                f"RT25-VEC {vid}: cause {cause} derives {got!r}, the pinned anchor "
                f"fixture expects {expected!r}")
    if row.get("expectedEqual") is not True:
        findings.append(f"RT25-VEC {vid}: expectedEqual must be true")

    # Poison: proves the fold and the derivation never touch `cause`.
    poisoned = [dict(entry(None), cause=Poison(f"{vid}.cause"))]
    try:
        fold_ledger(poisoned)
        effective_capability(sealed, units, records)
    except RefusedError as exc:
        findings.append(
            f"RT25-VEC {vid}: the derivation TOUCHED the poisoned cause field "
            f"({exc}); cause is declared unreachable from the effective-capability "
            f"fold, which reads only toState")

    # POSITIVE CONTROL: without it, "the two agree" is unfalsifiable.
    leaked_a = effective_capability_CAUSE_LEAKING(
        sealed, units, records, [entry("RETENTION_SIZE_BOUND")])
    leaked_b = effective_capability_CAUSE_LEAKING(
        sealed, units, records, [entry("RETENTION_USER_REQUEST")])
    control(vid, results["RETENTION_SIZE_BOUND"] == results["RETENTION_USER_REQUEST"],
            leaked_a == leaked_b)
    return findings


def _drive_posture_vector(row: dict[str, Any], ctx: dict[str, Any], vid: str,
                          control: Any) -> list[str]:
    """PC-V-13 through PC-V-16.

    PC-V-13's and PC-V-14's REJECTED readings are not re-implementations: they are
    read from retention-tiers.v24.json's PINNED askDecisionTable cells, so the
    negative control is a measurement of reviewed bytes rather than a model.
    """
    findings: list[str] = []
    cells = get_path(ctx["v24"],
                     "$.partA_firstRunRetentionConsent.askDecisionTable.cells", [])

    def cell(profile: str, presence: str, custody: str) -> dict[str, Any]:
        return next((c for c in cells if c["invocationProfile"] == profile
                     and c["policyPresence"] == presence
                     and c["requestedCustody"] == custody), {})

    def fail(detail: str) -> None:
        findings.append(f"RT25-VEC {vid}: {detail}")

    if vid == "PC-V-13-ABSENT-POLICY-RESOLVES-DURABLE":
        posture, provenance = effective_posture(ABSENT)
        if posture != row["expectedPosture"]:
            fail(f"posture {posture!r}, row expects {row['expectedPosture']!r}")
        if provenance != row["expectedProvenance"]:
            fail(f"provenance {provenance!r}, row expects "
                 f"{row['expectedProvenance']!r}")
        outcome = durable_authoritative_outcome(ABSENT)
        if outcome != row["expectedDurableAuthoritativeOutcome"]:
            fail(f"outcome {outcome!r}, row expects "
                 f"{row['expectedDurableAuthoritativeOutcome']!r}")
        _, _, written = resolve_and_maybe_persist(ABSENT, "DISMISSED-TIMEOUT")
        if (written is not None) != row["expectedPolicyPersisted"]:
            fail(f"policyPersisted {written is not None}, row expects "
                 f"{row['expectedPolicyPersisted']}")
        v24cell = cell("ci", "ABSENT", "DURABLE_AUTHORITATIVE")
        control(vid, outcome, v24cell.get("outcome"))
        declared = row.get("resultUnderRejectedReading", "")
        for token in (v24cell.get("derivedErrorCode"),
                      str(v24cell.get("derivedExitCode"))):
            if token and token not in declared:
                fail(f"the row's resultUnderRejectedReading must name the pinned v24 "
                     f"cell's own {token!r}; got {declared!r}")

    elif vid == "PC-V-14-EPHEMERAL-IS-ALWAYS-CONSENTED":
        policy = {"posture": row["policyPosture"]}
        posture, provenance = effective_posture(policy)
        if posture != row["expectedPosture"] or provenance != row["expectedProvenance"]:
            fail(f"({posture!r}, {provenance!r}) != declared "
                 f"({row['expectedPosture']!r}, {row['expectedProvenance']!r})")
        outcome = durable_authoritative_outcome(policy)
        if outcome != row["expectedDurableAuthoritativeOutcome"]:
            fail(f"outcome {outcome!r}, row expects "
                 f"{row['expectedDurableAuthoritativeOutcome']!r}")
        for profile in ("ci", "local-interactive"):
            v24cell = cell(profile, "PRESENT-EPHEMERAL_ONLY", "DURABLE_AUTHORITATIVE")
            if v24cell.get("derivedErrorCode") != row["expectedErrorCode"]:
                fail(f"the surviving refusal's error code is carried unchanged from "
                     f"v24's {profile} cell; pinned {v24cell.get('derivedErrorCode')!r} "
                     f"!= declared {row['expectedErrorCode']!r}")
        if row["expectedErrorCode"] not in ctx["d9errorCodes"]:
            fail(f"{row['expectedErrorCode']!r} is not a member of the live pinned "
                 f"D9 closed error-code vocabulary")
        control(vid, outcome, durable_authoritative_outcome_NO_REFUSAL(policy))
        # exhaustive: no input yields (EPHEMERAL_ONLY, DEFAULTED)
        for candidate in (ABSENT, {"posture": "DURABLE_RETAINED"},
                          {"posture": "EPHEMERAL_ONLY"}):
            got = effective_posture(candidate)
            if got == ("EPHEMERAL_ONLY", "DEFAULTED"):
                fail(f"input {candidate!r} yields (EPHEMERAL_ONLY, DEFAULTED)")

    elif vid == "PC-V-15-DEFAULT-IS-NEVER-PERSISTED":
        persisted: list[str] = []
        for interaction in ("DISMISSED-TIMEOUT", "DISMISSED-EOF",
                            "DISMISSED-MALFORMED-EXHAUSTED", "DISMISSED-SIGINT",
                            "NOT-ASKED"):
            _, _, written = resolve_and_maybe_persist(ABSENT, interaction)
            if written is not None:
                persisted.append(interaction)
        if persisted:
            fail(f"these non-answer interactions persisted a policy: {persisted}")
        on_disk = "ABSENT" if resolve_and_maybe_persist(
            ABSENT, "DISMISSED-TIMEOUT")[2] is None else "PRESENT"
        if on_disk != row["expectedPolicyOnDiskAfter"]:
            fail(f"policy on disk {on_disk!r}, row expects "
                 f"{row['expectedPolicyOnDiskAfter']!r}")
        next_provenance = effective_posture(ABSENT)[1]
        if next_provenance != row["expectedProvenanceOnNextRun"]:
            fail(f"provenance on the next run {next_provenance!r}, row expects "
                 f"{row['expectedProvenanceOnNextRun']!r}")
        rejected = resolve_and_maybe_persist_PERSISTING(ABSENT, "DISMISSED-TIMEOUT")[2]
        control(vid, on_disk, "ABSENT" if rejected is None else "PRESENT")
        if rejected is not None:
            manufactured = effective_posture(rejected)[1]
            if manufactured != "CONSENTED":
                fail(f"the rejected reading must manufacture CONSENTED provenance "
                     f"from a default; got {manufactured!r}")

    elif vid == "PC-V-16-DISMISSAL-DOES-NOT-SUPPRESS-THE-NEXT-ASK":
        first = ask_performed("local-interactive", ABSENT, "DURABLE_AUTHORITATIVE", 0)
        second = ask_performed("local-interactive", ABSENT, "DURABLE_AUTHORITATIVE", 1)
        if first != row["expectedFirstRunAskPerformed"]:
            fail(f"first-run ask {first}, row expects "
                 f"{row['expectedFirstRunAskPerformed']}")
        if second != row["expectedSecondRunAskPerformed"]:
            fail(f"second-run ask {second}, row expects "
                 f"{row['expectedSecondRunAskPerformed']}")
        posture, provenance = effective_posture(ABSENT)
        outcome = f"{durable_authoritative_outcome(ABSENT)} under {provenance}"
        if not row["expectedFirstRunOutcome"].startswith(outcome):
            fail(f"first-run outcome {outcome!r} does not open the row's declared "
                 f"{row['expectedFirstRunOutcome']!r}")
        _, _, written = resolve_and_maybe_persist(ABSENT, "DISMISSED-TIMEOUT")
        if written is not None:
            fail("the row declares 'no policy written' on the first run")
        control(vid, second,
                ask_performed_SUPPRESSING("local-interactive", ABSENT,
                                          "DURABLE_AUTHORITATIVE", 1))
        v24flag = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent.noAskCases[2]"
                                       ".dismissalSuppressesTheNextAsk")
        if v24flag is None:
            v24flag = _find_flag(ctx["v24"], "dismissalSuppressesTheNextAsk")
        if v24flag is not False:
            fail(f"v24's pinned dismissalSuppressesTheNextAsk is {v24flag!r}; this "
                 f"row carries the rule forward and requires false")
    return findings


def _find_flag(node: Any, name: str) -> Any:
    if isinstance(node, dict):
        if name in node:
            return node[name]
        for value in node.values():
            found = _find_flag(value, name)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_flag(value, name)
            if found is not None:
                return found
    return None


# ===========================================================================
# SECTION 4 -- INVARIANT EXECUTION.
# All 19 invariants of $.partC_retentionBounds.invariants.  Each has an
# executable driver, each can fail, and each that asserts a NEGATIVE ("never",
# "no path", "cannot") is paired with a POSITIVE CONTROL -- an implementation
# that violates it -- so the driver is shown able to detect a violation rather
# than merely to observe its absence.
# ===========================================================================

INVARIANT_IDS = tuple(f"RT25-C-INV-{n:02d}" for n in range(1, 15)) + \
    tuple(f"RT25-D-INV-{n:02d}" for n in range(1, 6))

GRID_KEEP = (0, 1, 2, 3, 5, 7, 11)
GRID_BYTES = (0, 1, 50, 100, 300, 500, 10 ** 9)
GRID_AGE = (0,)                    # DEP-RT25-01: the only admissible value
GRID_POPULATIONS = ((0, 0), (1, 100), (3, 300), (5, 500), (7, 700))


def _grid_orders() -> list[list[dict[str, Any]]]:
    return [eviction_order(population(n, total)) for n, total in GRID_POPULATIONS]


def inv_01(ctx: dict[str, Any]) -> list[str]:
    """A sweep emits only PURGED, and therefore can never raise effectiveCapability."""
    out: list[str] = []
    emitted = 0
    for order in _grid_orders():
        for keep, size in itertools.product(GRID_KEEP, GRID_BYTES):
            entries, _ = retention_sweep((0, size, keep), order, PROJECT, 0)
            emitted += len(entries)
            bad = {e["toState"] for e in entries} - {"PURGED"}
            if bad:
                out.append(f"RT25-C-INV-01: a sweep emitted toState {sorted(bad)}")
    # capability may only fall or stay, over the pinned closure
    sbp = ctx["v22"]["semanticBasisProjection"]
    closure = sbp["semanticCapabilityClosure"]
    base_records = sbp["unitAvailabilityRecords"]
    sealed, units = closure["sealedCapability"], closure["units"]
    before = effective_capability(sealed, units, base_records)
    keys = [(s["projectId"], s["recordCasRef"], s["recordKind"])
            for r in base_records for s in r["objectStates"]]
    rng = random.Random(20260805)
    for _ in range(400):
        chosen = rng.sample(keys, rng.randint(1, min(4, len(keys))))
        overrides = [{"projectId": k[0], "recordCasRef": k[1], "recordKind": k[2],
                      "state": "PURGED"} for k in chosen]
        after = effective_capability(sealed, units,
                                     apply_states(base_records, overrides))
        if CAPABILITY_RANK[after] > CAPABILITY_RANK[before]:
            out.append(f"RT25-C-INV-01: purging {chosen} RAISED capability "
                       f"{before} -> {after}")
            break
    # POSITIVE CONTROL: a sweep that emits a non-PURGED transition is detected.
    raising = retention_sweep_RAISING((0, 100, 0), _grid_orders()[3], PROJECT, 0)
    if {e["toState"] for e in raising} <= {"PURGED"}:
        out.append("RT25-C-INV-01: VACUOUS -- the positive control sweep, which is "
                   "written to emit AVAILABLE, was not distinguishable from a "
                   "compliant one")
    if emitted == 0:
        out.append("RT25-C-INV-01: VACUOUS -- the grid emitted no transitions at all")
    return out


def inv_02(_ctx: dict[str, Any]) -> list[str]:
    """Each demand is a function of the order and that bound's OWN value only.

    Proved by enumeration rather than asserted: for every dimension, group every
    grid point by (its own value, the population) and require exactly one distinct
    demand in each group.  If any other bound's value could reach the expression,
    some group would carry two values.
    """
    out: list[str] = []
    groups: dict[tuple, set[int]] = {}
    for index, order in enumerate(_grid_orders()):
        for age, size, keep in itertools.product(GRID_AGE, GRID_BYTES, GRID_KEEP):
            per = demands((age, size, keep), order)
            groups.setdefault(("count", keep, index), set()).add(per["count"])
            groups.setdefault(("size", size, index), set()).add(per["size"])
            groups.setdefault(("time", age, index), set()).add(per["time"])
    impure = {k: sorted(v) for k, v in groups.items() if len(v) != 1}
    if impure:
        out.append(f"RT25-C-INV-02: {len(impure)} (dimension, ownValue, population) "
                   f"groups carry more than one demand, so a demand depends on "
                   f"another bound's value: {list(impure.items())[:4]}")
    # monotonicity: disabling any one dimension cannot reduce another's demand
    for index, order in enumerate(_grid_orders()):
        for size, keep in itertools.product(GRID_BYTES, GRID_KEEP):
            full = eviction_count((0, size, keep), order)
            if full < eviction_count((0, 0, keep), order):
                out.append(f"RT25-C-INV-02: disabling size reduced the count "
                           f"dimension's effect at pop{index} keep={keep}")
            if full < eviction_count((0, size, 0), order):
                out.append(f"RT25-C-INV-02: disabling count reduced the size "
                           f"dimension's effect at pop{index} size={size}")
    # POSITIVE CONTROL: the parasitic implementation MUST fail the same test.
    parasitic_groups: dict[tuple, set[int]] = {}
    for index, order in enumerate(_grid_orders()):
        for size, keep in itertools.product(GRID_BYTES, GRID_KEEP):
            value = eviction_count_PARASITIC((0, size, keep), order)
            parasitic_groups.setdefault(("size", size, index), set()).add(value)
    if all(len(v) == 1 for v in parasitic_groups.values()):
        out.append("RT25-C-INV-02: VACUOUS -- the parasitic implementation, whose "
                   "whole defect is that the size demand depends on the count "
                   "configuration, passed this test, so the test cannot detect the "
                   "class it exists for")
    return out


def inv_03(_ctx: dict[str, Any]) -> list[str]:
    """Evicted set is a PREFIX of one total order; the count is the MAX, not the sum."""
    out: list[str] = []
    separations = 0
    for order in _grid_orders():
        if not order_is_total(order):
            out.append("RT25-C-INV-03: the eviction order is not total, so prefixes "
                       "are not totally ordered by inclusion")
        # determinism under permutation
        rng = random.Random(4242)
        for _ in range(20):
            shuffled = order[:]
            rng.shuffle(shuffled)
            if eviction_order(shuffled) != order:
                out.append("RT25-C-INV-03: the eviction order is not deterministic "
                           "under input permutation")
                break
        for size, keep in itertools.product(GRID_BYTES, GRID_KEEP):
            bounds = (0, size, keep)
            n = eviction_count(bounds, order)
            got = evicted_set(bounds, order)
            if got != order[:n]:
                out.append(f"RT25-C-INV-03: the evicted set is not a prefix at "
                           f"{bounds}")
            per = demands(bounds, order)
            if n != max(per.values()):
                out.append(f"RT25-C-INV-03: count {n} != max(demands) at {bounds}")
            # every shorter demand's prefix is contained in the evicted prefix
            for dim, demand in per.items():
                if order[:demand] != got[:demand]:
                    out.append(f"RT25-C-INV-03: the {dim} demand's prefix is not "
                               f"contained in the evicted prefix at {bounds}")
            if eviction_count_SUM(bounds, order) != n:
                separations += 1
    if separations == 0:
        out.append("RT25-C-INV-03: VACUOUS -- sum and max agreed at every grid "
                   "point, so no point in the grid distinguishes them")
    # the tiebreak is exercised, and must be total and deterministic
    tied = [{"projectId": PROJECT, "recordCasRef": ref, "recordKind": "file-bytes",
             "atSequence": 7, "admittedAt": 1, "bytes": 10}
            for ref in ("sha256:c", "sha256:a", "sha256:b")]
    ordered = eviction_order(tied)
    if [o["recordCasRef"] for o in ordered] != ["sha256:a", "sha256:b", "sha256:c"]:
        out.append("RT25-C-INV-03: equal atSequence is not resolved by recordCasRef "
                   "lexicographic ascending")
    if not order_is_total(tied):
        out.append("RT25-C-INV-03: equal atSequence produced a non-total order")
    ambiguous = tied + [dict(tied[0])]
    if order_is_total(ambiguous):
        out.append("RT25-C-INV-03: VACUOUS -- order_is_total accepted a duplicated "
                   "(atSequence, recordCasRef), so it cannot detect ambiguity")
    return out


def inv_04(_ctx: dict[str, Any]) -> list[str]:
    """Every PURGED entry carries exactly one cause from the closed four-member
    partition; an absent or out-of-partition cause is refused."""
    out: list[str] = []
    base = {"schemaVersion": 1, "projectId": PROJECT,
            "recordCasRef": "sha256:" + "0" * 64, "recordKind": "file-bytes",
            "toState": "PURGED", "atSequence": 1}
    for cause in CAUSE_PARTITION:
        verdict, _ = admit_transition(dict(base, cause=cause))
        if verdict != "ADMITTED":
            out.append(f"RT25-C-INV-04: partition member {cause} was refused")
    refusable = [None, "", "RETENTION_OTHER", "retention_size_bound", True, False, 1,
                 1.0, ["RETENTION_SIZE_BOUND"], {"cause": "RETENTION_SIZE_BOUND"}]
    for bad in refusable:
        verdict, code = admit_transition(dict(base, cause=bad))
        if verdict != "REFUSED" or code != "CONFIG.INVALID":
            out.append(f"RT25-C-INV-04: cause {bad!r} was {verdict} with {code!r}; "
                       f"an out-of-partition or type-variant cause must be REFUSED "
                       f"with CONFIG.INVALID")
    absent = dict(base)
    if admit_transition(absent)[0] != "REFUSED":
        out.append("RT25-C-INV-04: a PURGED entry with NO cause was admitted")
    # exactly one cause per entry, over the whole grid
    for order in _grid_orders():
        for size, keep in itertools.product(GRID_BYTES, GRID_KEEP):
            entries, _ = retention_sweep((0, size, keep), order, PROJECT, 0)
            for e in entries:
                if not isinstance(e.get("cause"), str) or \
                        e["cause"] not in CAUSE_PARTITION:
                    out.append(f"RT25-C-INV-04: sweep emitted cause {e.get('cause')!r}")
    return out


def inv_05(ctx: dict[str, Any]) -> list[str]:
    """Entries agreeing on toState and differing only in cause derive the same
    effectiveCapability.  Exhaustive over all four fixtures and all four causes,
    plus a Poison probe and a cause-reading positive control."""
    out: list[str] = []
    sbp = ctx["v22"]["semanticBasisProjection"]
    closure = sbp["semanticCapabilityClosure"]
    sealed, units = closure["sealedCapability"], closure["units"]
    comparisons = 0
    for fixture in sbp["availabilityFixtures"]:
        base_records = sbp["unitAvailabilityRecords"]
        results = set()
        poison_touches: list[str] = []
        for cause in CAUSE_PARTITION + (Poison("inv05.cause"),):
            # Build a REAL ledger per cause and derive THROUGH THE FOLD, so the runs
            # differ in their input.  Deriving from one pre-computed record set N
            # times would compare a value with itself and agree unconditionally --
            # vacuous in exactly the way this driver reports elsewhere.  The Poison
            # arm proves the fold and the derivation never TOUCH the field, rather
            # than arguing it from the absence of a mention.
            entries = [{"schemaVersion": 1, "projectId": override["projectId"],
                        "recordCasRef": override["recordCasRef"],
                        "recordKind": override["recordKind"],
                        "toState": override["state"], "atSequence": position + 1,
                        "cause": cause}
                       for position, override in enumerate(fixture["stateOverrides"])]
            try:
                fold = fold_ledger(entries)
                overrides = [{"projectId": key[0], "recordCasRef": key[1],
                              "recordKind": key[2], "state": state}
                             for key, state in fold.items()]
                records = apply_states(base_records, overrides)
                results.add(effective_capability(sealed, units, records))
            except RefusedError as exc:
                poison_touches.append(f"{fixture['id']}: {exc}")
                continue
            if not isinstance(cause, Poison):
                comparisons += 1
        if poison_touches:
            out.append(f"RT25-C-INV-05: the fold or the derivation TOUCHED the "
                       f"poisoned cause field: {poison_touches}")
        # POSITIVE CONTROL: a cause-reading derivation must SEPARATE the same inputs,
        # or "they all agree" is a statement about a comparison that cannot disagree.
        records = apply_states(base_records, fixture["stateOverrides"])
        leaked = {effective_capability_CAUSE_LEAKING(
            sealed, units, records,
            [{"toState": "PURGED", "cause": c}]) for c in CAUSE_PARTITION}
        if len(leaked) < 2:
            out.append(f"RT25-C-INV-05: VACUOUS at fixture {fixture['id']} -- the "
                       f"cause-reading positive control also agreed across the four "
                       f"causes, so this comparison cannot detect a cause leak")
        if len(results) != 1:
            out.append(f"RT25-C-INV-05: fixture {fixture['id']} derives {results} "
                       f"across the four causes")
        if results != {fixture["expectedEffectiveCapability"]}:
            out.append(f"RT25-C-INV-05: fixture {fixture['id']} derives {results}, "
                       f"the pinned v22 fixture expects "
                       f"{fixture['expectedEffectiveCapability']!r}")
    if comparisons != 16:
        out.append(f"RT25-C-INV-05: {comparisons} cause comparisons run, 4 fixtures "
                   f"x 4 causes = 16 expected")
    # the derivation's declared inputs are 3 and none is a ledger entry field
    inputs = get_path(ctx["v24"], "$.partB_purgeSemantics."
                                  "effectiveCapabilityDerivation.inputs", [])
    names = [i.get("name") for i in inputs]
    if names != ["sealedCapability", "units", "availabilityRecords"]:
        out.append(f"RT25-C-INV-05: v24's pinned derivation inputs are {names}; the "
                   f"cause-unreachability argument rests on exactly these three")
    forbidden = get_path(ctx["v24"], "$.partB_purgeSemantics."
                                     "effectiveCapabilityDerivation.forbiddenInputs", [])
    if "cause" in forbidden:
        out.append("RT25-C-INV-05: 'cause' is already in v24's pinned forbiddenInputs; "
                   "v25's whole 11->12 widening claim requires it absent there")
    return out


def inv_06(ctx: dict[str, Any]) -> list[str]:
    """No ledger entry is ever removed, rewritten or expired."""
    out: list[str] = []
    ledger = get_path(ctx["v24"], "$.partB_purgeSemantics.ledger", {})
    for flag in ("appendOnly", "entriesAreNeverEditedOrRemoved"):
        if ledger.get(flag) is not True:
            out.append(f"RT25-C-INV-06: v24's pinned ledger.{flag} is "
                       f"{ledger.get(flag)!r}")
    entry = {"schemaVersion": 1, "projectId": PROJECT,
             "recordCasRef": "sha256:" + "1" * 64, "recordKind": "file-bytes"}
    hostile = {
        "terminal reversal": [dict(entry, toState="PURGED", atSequence=1),
                              dict(entry, toState="AVAILABLE", atSequence=2)],
        "sequence break": [dict(entry, toState="AVAILABLE", atSequence=1),
                           dict(entry, toState="PURGED", atSequence=3)],
        "restart": [dict(entry, toState="AVAILABLE", atSequence=1),
                    dict(entry, toState="PURGED", atSequence=1)],
        "non-1 start": [dict(entry, toState="AVAILABLE", atSequence=0)],
    }
    for name, entries in hostile.items():
        try:
            fold_ledger(entries)
        except RefusedError:
            continue
        out.append(f"RT25-C-INV-06: the hostile ledger '{name}' was accepted by the "
                   f"fold; append-only with terminal loss must refuse it")
    # POSITIVE CONTROL: a compliant ledger must still fold, or the four refusals
    # above prove only that the fold rejects everything.
    try:
        fold_ledger([dict(entry, toState="AVAILABLE", atSequence=1),
                     dict(entry, toState="PURGED", atSequence=2)])
    except RefusedError as exc:
        out.append(f"RT25-C-INV-06: VACUOUS -- a compliant ledger was also refused "
                   f"({exc}), so the hostile refusals prove nothing")
    # repurge is idempotent, so it must NOT be refused
    try:
        fold_ledger([dict(entry, toState="PURGED", atSequence=1),
                     dict(entry, toState="PURGED", atSequence=2)])
    except RefusedError as exc:
        out.append(f"RT25-C-INV-06: repurge must be idempotent, not refused ({exc})")
    return out


def inv_07(_ctx: dict[str, Any]) -> list[str]:
    """A bound is never an admission gate."""
    out: list[str] = []
    refusals = 0
    for order in _grid_orders():
        for size, keep, footprint in itertools.product(GRID_BYTES, GRID_KEEP,
                                                       (0, 1, 500, 10 ** 12)):
            if admit_write((0, size, keep), footprint, order) != "ADMITTED":
                refusals += 1
    if refusals:
        out.append(f"RT25-C-INV-07: {refusals} grid points refused a write; no "
                   f"configured bound and no unsatisfiable bound may refuse one")
    # an UNSATISFIABLE bound must refuse the BOUNDS RECORD and still admit the write
    if admit_bounds(bounds_record(PRODUCT_MAX_AGE_SECONDS, 0, 0))[0] != "REFUSED":
        out.append("RT25-C-INV-07: an unsatisfiable bounds record must be refused")
    if admit_write((0, 1, 0), 10 ** 12, []) != "ADMITTED":
        out.append("RT25-C-INV-07: a write was refused while over bound with nothing "
                   "evictable, which is the structurally unfixable case")
    # POSITIVE CONTROL: the throwing store must refuse somewhere.
    if admit_write_THROWING((0, 1, 0), 10 ** 12, []) != "REFUSED":
        out.append("RT25-C-INV-07: VACUOUS -- the rejected reading, which is written "
                   "to throw, did not refuse anywhere in the grid")
    return out


def inv_08(_ctx: dict[str, Any]) -> list[str]:
    """Invalid or unsatisfiable bounds are refused at admission and never silently
    defaulted or silently skipped."""
    out: list[str] = []
    invalid = [bounds_record(0, 0, -1), bounds_record(-1, 0, 0),
               bounds_record(0, -5, 0), bounds_record(0, 0, True),
               bounds_record(0, 0, 200.0), bounds_record(0, 0, "200"),
               bounds_record(0, 0, None), bounds_record(1, 0, 0),
               bounds_record(PRODUCT_MAX_AGE_SECONDS, 0, 0),
               bounds_record(0, 0, 0, boundsRevision=0),
               bounds_record(0, 0, 0, schemaVersion=2),
               bounds_record(0, 0, 0, schemaVersion=True),
               bounds_record(0, 0, 0, projectId=1),
               bounds_record(0, 0, 0, retentionPolicyId=None)]
    for record in invalid:
        verdict, code, admitted = admit_bounds(record)
        if verdict != "REFUSED" or code != "CONFIG.INVALID":
            out.append(f"RT25-C-INV-08: {record} was {verdict}/{code!r}")
        if admitted is not None:
            out.append(f"RT25-C-INV-08: a refused record produced a SUBSTITUTED "
                       f"value {admitted}; there must be no code path mapping an "
                       f"invalid value to a valid one")
    # unknown and missing keys are refused: the record is closed
    extra = bounds_record(0, 0, 0)
    extra["posture"] = "DURABLE_RETAINED"
    if admit_bounds(extra)[0] != "REFUSED":
        out.append("RT25-C-INV-08: a bounds record carrying a forbidden field "
                   "(posture) was admitted; forbiddenFields makes the record closed")
    short = bounds_record(0, 0, 0)
    del short["keepCount"]
    if admit_bounds(short)[0] != "REFUSED":
        out.append("RT25-C-INV-08: a bounds record missing a closed field was admitted")
    # POSITIVE CONTROLS: both wrong readings must ADMIT where the right one refuses.
    if admit_bounds_SILENT_REVERT(bounds_record(0, 0, -1))[0] != "ADMITTED":
        out.append("RT25-C-INV-08: VACUOUS -- the silent-revert reading did not "
                   "admit the negative value it exists to admit")
    if admit_bounds_SILENT_SKIP(
            bounds_record(PRODUCT_MAX_AGE_SECONDS, 0, 0))[0] != "ADMITTED":
        out.append("RT25-C-INV-08: VACUOUS -- the silent-skip reading did not admit "
                   "the unsatisfiable bound it exists to admit")
    return out


def inv_09(_ctx: dict[str, Any]) -> list[str]:
    """Every closed scalar is admitted by exact JSON type at any depth BEFORE its
    content is compared."""
    out: list[str] = []
    wrong = [True, False, 1.0, 0.0, "1", "0", None, [], {}, [1], {"v": 1}]
    admitted = 0
    for field in BOUNDS_CLOSED_INTS:
        for value in wrong:
            record = bounds_record(0, 0, 0)
            record[field] = value
            trace: list[str] = []
            verdict, code, _ = admit_bounds(record, trace)
            if verdict != "REFUSED" or code != "CONFIG.INVALID":
                admitted += 1
                out.append(f"RT25-C-INV-09: {field}={value!r} was {verdict}")
            elif any(step.startswith("compare:") for step in trace):
                out.append(f"RT25-C-INV-09: {field}={value!r} was refused only AFTER "
                           f"a content comparison; law 18 requires the type gate "
                           f"first. trace={trace}")
    for field in ("projectId", "retentionPolicyId", "retentionBoundsId"):
        for value in (1, True, 1.0, None, [], {}):
            record = bounds_record(0, 0, 0)
            record[field] = value
            if admit_bounds(record)[0] != "REFUSED":
                out.append(f"RT25-C-INV-09: {field}={value!r} was admitted; a "
                           f"non-string is not a string at any depth")
    # AT ANY DEPTH: a record the host only forwards, nested inside a wrapper
    nested = {"forwarded": {"bounds": bounds_record(0, 0, True)}}
    if admit_bounds(nested["forwarded"]["bounds"])[0] != "REFUSED":
        out.append("RT25-C-INV-09: the type gate did not hold at depth, which is "
                   "the clause law 18 states explicitly for forwarded records")
    # bool BEFORE int is load-bearing: prove the ORDER, not just the outcome
    trace: list[str] = []
    admit_bounds(bounds_record(0, 0, True), trace)
    if "type-check:keepCount" not in trace:
        out.append(f"RT25-C-INV-09: the admission trace does not record a type check "
                   f"for keepCount; trace={trace}")
    if admitted:
        out.append(f"RT25-C-INV-09: {admitted} type-variant values were admitted")
    return out


def inv_10(_ctx: dict[str, Any]) -> list[str]:
    """ABSENT and all-zero agree on every value and differ on provenance; neither
    purges anything."""
    out: list[str] = []
    absent = effective_bounds(ABSENT)
    zero = effective_bounds(bounds_record(0, 0, 0))
    if absent[:3] != zero[:3]:
        out.append(f"RT25-C-INV-10: values differ, {absent[:3]} vs {zero[:3]}")
    if absent[3] == zero[3]:
        out.append(f"RT25-C-INV-10: provenance is identical ({absent[3]!r}); the "
                   f"distinction is the whole reason both states exist")
    if {absent[3], zero[3]} != set(BOUNDS_PROVENANCE_ENUM):
        out.append(f"RT25-C-INV-10: the two provenances are not exactly "
                   f"{BOUNDS_PROVENANCE_ENUM}")
    for order in _grid_orders():
        for resolved in (absent, zero):
            if eviction_count(resolved[:3], order) != 0:
                out.append(f"RT25-C-INV-10: {resolved[3]} bounds purged something")
    return out


def inv_11(_ctx: dict[str, Any]) -> list[str]:
    """A sweep reads no ledger, footprint or bounds record of any other ProjectId.

    Proved with Poison rather than argued: every other project's data raises on
    ANY access, so a single touch is an exception.
    """
    out: list[str] = []
    mine = eviction_order(population(5, 500))
    world = {PROJECT: mine,
             "prj1-" + "d" * 64: Poison("otherProjectLedger"),
             "prj1-" + "e" * 64: Poison("otherProjectBounds")}
    try:
        entries, _ = retention_sweep((0, 100, 2), world[PROJECT], PROJECT, 0)
        for entry in entries:
            if entry["projectId"] != PROJECT:
                out.append("RT25-C-INV-11: a sweep emitted an entry for another "
                           "ProjectId")
    except RefusedError as exc:
        out.append(f"RT25-C-INV-11: the sweep TOUCHED another project's data ({exc})")
    # POSITIVE CONTROL: a leaky sweep must raise, or Poison proves nothing.
    try:
        _ = world["prj1-" + "d" * 64] == mine
        out.append("RT25-C-INV-11: VACUOUS -- Poison did not raise on comparison, so "
                   "the non-reading proof is unfalsifiable")
    except RefusedError:
        pass
    return out


def inv_12(ctx: dict[str, Any]) -> list[str]:
    """purgeMutationBoundary.mutatesExactly still has exactly two members and no
    member of doesNotMutate is touched by any sweep."""
    out: list[str] = []
    boundary = get_path(ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary", {})
    mutates = boundary.get("mutatesExactly") or []
    does_not = boundary.get("doesNotMutate") or []
    if len(mutates) != 2:
        out.append(f"RT25-C-INV-12: v24's pinned mutatesExactly has {len(mutates)} "
                   f"members, not 2")
    if len(does_not) != 16:
        out.append(f"RT25-C-INV-12: v24's pinned doesNotMutate has {len(does_not)} "
                   f"members; v25's protectedSet derivation names 16")
    surfaces = {"rawObjectBytes", "unitAvailabilityLedger"}
    for order in _grid_orders():
        for size, keep in itertools.product(GRID_BYTES, GRID_KEEP):
            _, touched = retention_sweep((0, size, keep), order, PROJECT, 0)
            if not touched <= surfaces:
                out.append(f"RT25-C-INV-12: a sweep touched {sorted(touched - surfaces)}, "
                           f"outside the two-member mutation boundary")
    # the two surfaces map onto the two declared members, and onto nothing in
    # doesNotMutate.  Checked by token, against the PINNED text.
    joined = " ".join(mutates).lower()
    for token in ("raw object bytes", "unitavailabilityledger"):
        if token not in joined:
            out.append(f"RT25-C-INV-12: v24's pinned mutatesExactly does not name "
                       f"{token!r}, so this sweep's touched-surface set cannot be "
                       f"mapped onto it")
    forbidden_tokens = ("sealed run", "closure commitment", "evidence digest",
                        "planid", "snapshotid")
    for member in does_not:
        low = member.lower()
        for token in forbidden_tokens:
            if token in low and token in joined:
                out.append(f"RT25-C-INV-12: {token!r} appears in BOTH mutatesExactly "
                           f"and doesNotMutate")
    return out


def inv_13(_ctx: dict[str, Any]) -> list[str]:
    """A record in OUTAGE is never evictable.  Exhaustive over all state assignments."""
    out: list[str] = []
    keys = [(PROJECT, f"sha256:{i:064x}", "file-bytes") for i in range(4)]
    checked = 0
    for assignment in itertools.product(AVAIL_STATES, repeat=len(keys)):
        fold = dict(zip(keys, assignment))
        evictable = set(evictable_set(fold))
        checked += 1
        for key, state in fold.items():
            if state != "AVAILABLE" and key in evictable:
                out.append(f"RT25-C-INV-13: a record in {state} was evictable")
            if state == "AVAILABLE" and key not in evictable:
                out.append("RT25-C-INV-13: an AVAILABLE record was not evictable")
    if checked != len(AVAIL_STATES) ** len(keys):
        out.append(f"RT25-C-INV-13: {checked} assignments enumerated, "
                   f"{len(AVAIL_STATES) ** len(keys)} expected")
    return out


def inv_14(ctx: dict[str, Any]) -> list[str]:
    """This artifact adds no D9 member and the measured gap remains 0/9, 0/9, 0/19."""
    out: list[str] = []
    d9 = ctx["d9"]
    declared = get_path(ctx["doc"], "$.partC_retentionBounds.d9ReasonCodePosition."
                                    "measuredLiveFromPinnedD9Bytes", {})
    deficiencies = list(d9["codeMaps"]["deficiencyToReasonCode"])
    reasons = list(d9["codeVocabulary"]["reasonCodes"])
    errors = list(d9["codeVocabulary"]["errorCodes"])
    # The artifact records the digest of the bytes it measured.  Compared against
    # the file this instrument actually read, so "measured live from pinned bytes"
    # names the same bytes in both sentences.  The selftest caught the omission as
    # escape MX-34-D9-DIGEST-DRIFT.
    live_d9 = hashlib.sha256(ctx["snaps"]["d9-exit-contract.v1.14.json"]).hexdigest()
    if declared.get("sha256") != live_d9:
        out.append(f"RT25-C-INV-14 ...measuredLiveFromPinnedD9Bytes.sha256: declared "
                   f"{declared.get('sha256')!r}, but the bytes this instrument "
                   f"measured hash to {live_d9}")
    if declared.get("source") != "d9-exit-contract.v1.14.json":
        out.append(f"RT25-C-INV-14 ...measuredLiveFromPinnedD9Bytes.source: "
                   f"{declared.get('source')!r} is not the file this instrument pins")
    measured = {"deficiencyMemberCount": len(deficiencies),
                "reasonCodeCount": len(reasons), "errorCodeCount": len(errors)}
    for key, value in measured.items():
        if declared.get(key) != value:
            out.append(f"RT25-C-INV-14 $.partC_retentionBounds.d9ReasonCodePosition."
                       f"measuredLiveFromPinnedD9Bytes.{key}: declared "
                       f"{declared.get(key)!r}, measured {value}")
    predicate = tuple(declared.get("retentionTokenPredicate") or ())
    if not predicate:
        out.append("RT25-C-INV-14: retentionTokenPredicate is empty, so the 0/0/0 "
                   "measurement would be vacuously true")
    def hits(names: list[str]) -> int:
        return sum(1 for n in names if any(t in n.upper() for t in predicate))
    for key, names in (("deficiencyMembersMatchingPredicate", deficiencies),
                       ("reasonCodesMatchingPredicate", reasons),
                       ("errorCodesMatchingPredicate", errors)):
        got = hits(names)
        if declared.get(key) != got:
            out.append(f"RT25-C-INV-14 ...{key}: declared {declared.get(key)!r}, "
                       f"measured {got}")
    # POSITIVE CONTROL: the predicate must actually match something somewhere,
    # or "0 of 9" is a statement about a predicate that matches nothing at all.
    if hits(["RETENTION.EVIDENCE_PURGED"]) == 0:
        out.append("RT25-C-INV-14: VACUOUS -- the token predicate does not even "
                   "match the reason code this artifact proposes, so measuring 0 "
                   "hits against the live vocabulary proves nothing")
    # REQUESTED-NOT-ADDED: the proposal must be ABSENT from the live vocabulary
    requested = get_path(ctx["doc"], "$.partC_retentionBounds.d9ReasonCodePosition."
                                     "requestedSuccessorNotAdded", {})
    if requested.get("proposedReasonCode") in reasons:
        out.append("RT25-C-INV-14: the proposed reason code is ALREADY in the live "
                   "vocabulary, so REQUESTED-NOT-ADDED does not describe it")
    if requested.get("proposedDeficiencyId") in deficiencies:
        out.append("RT25-C-INV-14: the proposed deficiency member is already live")
    for key in ("codesAddedByThisArtifact", "deficiencyMembersAddedByThisArtifact",
                "errorCodesAddedByThisArtifact"):
        if requested.get(key) != 0:
            out.append(f"RT25-C-INV-14 ...requestedSuccessorNotAdded.{key}: "
                       f"{requested.get(key)!r}, must be 0")
    # the union-of-maps arithmetic the artifact records against itself
    union = set(d9["codeMaps"]["rejectionCauseToErrorCode"].values()) | \
        set(d9["codeMaps"]["faultCauseToErrorCode"].values())
    note = declared.get("whyTheCountsAreTakenFromCodeVocabularyAndNotTheMaps", "")
    match = re.search(r"has (\d+) distinct values", note)
    if match and int(match.group(1)) != len(union):
        out.append(f"RT25-C-INV-14: the note says the union of the two maps has "
                   f"{match.group(1)} distinct values; measured {len(union)}")
    if "CONFIG.INVALID" not in errors:
        out.append("RT25-C-INV-14: CONFIG.INVALID, the code every bounds refusal "
                   "reports, is not in the live closed error-code vocabulary")
    return out


def inv_d01(_ctx: dict[str, Any]) -> list[str]:
    """effective_posture is total: every input yields exactly one (posture, provenance)."""
    out: list[str] = []
    inputs = [ABSENT] + [{"posture": p} for p in POSTURE_ENUM]
    for candidate in inputs:
        try:
            posture, provenance = effective_posture(candidate)
        except RefusedError as exc:
            out.append(f"RT25-D-INV-01: input {candidate!r} produced no result ({exc})")
            continue
        if posture not in POSTURE_ENUM:
            out.append(f"RT25-D-INV-01: posture {posture!r} outside the closed enum")
        if provenance not in POSTURE_PROVENANCE_ENUM:
            out.append(f"RT25-D-INV-01: provenance {provenance!r} outside the enum")
        if posture == ABSENT:
            out.append("RT25-D-INV-01: the resolution returned ABSENT")
    # hostile inputs must REFUSE, not silently resolve
    for hostile in ({"posture": "ABSENT"}, {"posture": True}, {"posture": 1},
                    {"posture": None}, {"posture": "durable_retained"}, {}):
        try:
            effective_posture(hostile)
        except RefusedError:
            continue
        out.append(f"RT25-D-INV-01: hostile input {hostile!r} silently resolved")
    return out


def inv_d02(_ctx: dict[str, Any]) -> list[str]:
    """EPHEMERAL_ONLY is reachable only with provenance CONSENTED."""
    out: list[str] = []
    reachable = set()
    for candidate in [ABSENT] + [{"posture": p} for p in POSTURE_ENUM]:
        reachable.add(effective_posture(candidate))
    if ("EPHEMERAL_ONLY", "DEFAULTED") in reachable:
        out.append("RT25-D-INV-02: (EPHEMERAL_ONLY, DEFAULTED) is reachable")
    if ("EPHEMERAL_ONLY", "CONSENTED") not in reachable:
        out.append("RT25-D-INV-02: VACUOUS -- EPHEMERAL_ONLY is not reachable at all, "
                   "so 'only with CONSENTED' is empty")
    if reachable != {("DURABLE_RETAINED", "DEFAULTED"),
                     ("DURABLE_RETAINED", "CONSENTED"),
                     ("EPHEMERAL_ONLY", "CONSENTED")}:
        out.append(f"RT25-D-INV-02: the reachable set is {sorted(reachable)}; the "
                   f"declared table has exactly three rows")
    return out


def inv_d03(_ctx: dict[str, Any]) -> list[str]:
    """No code path persists a policy whose posture came from the default."""
    out: list[str] = []
    interactions = ("ANSWERED-RETAIN", "ANSWERED-EPHEMERAL", "DISMISSED-TIMEOUT",
                    "DISMISSED-EOF", "DISMISSED-MALFORMED-EXHAUSTED",
                    "DISMISSED-SIGINT", "NOT-ASKED")
    persisted = []
    for interaction in interactions:
        posture, provenance, written = resolve_and_maybe_persist(ABSENT, interaction)
        if written is not None:
            persisted.append(interaction)
            if provenance != "CONSENTED":
                out.append(f"RT25-D-INV-03: {interaction} persisted a policy with "
                           f"provenance {provenance!r}")
        del posture
    if set(persisted) != {"ANSWERED-RETAIN", "ANSWERED-EPHEMERAL"}:
        out.append(f"RT25-D-INV-03: the persisting interactions are {persisted}; "
                   f"only an ANSWER may write a policy")
    # POSITIVE CONTROL
    if resolve_and_maybe_persist_PERSISTING(ABSENT, "DISMISSED-TIMEOUT")[2] is None:
        out.append("RT25-D-INV-03: VACUOUS -- the persisting reading, written to "
                   "write a policy from a default, did not write one")
    return out


def inv_d04(_ctx: dict[str, Any]) -> list[str]:
    """A durable-authoritative request is refused iff the effective posture is
    EPHEMERAL_ONLY; it is never silently demoted."""
    out: list[str] = []
    for candidate in [ABSENT] + [{"posture": p} for p in POSTURE_ENUM]:
        posture, _ = effective_posture(candidate)
        outcome = durable_authoritative_outcome(candidate)
        refused = outcome == "REFUSE"
        if refused != (posture == "EPHEMERAL_ONLY"):
            out.append(f"RT25-D-INV-04: input {candidate!r} posture {posture!r} "
                       f"outcome {outcome!r} breaks the iff")
        if outcome not in ("REFUSE", "PROCEED-DURABLE"):
            out.append(f"RT25-D-INV-04: outcome {outcome!r} is neither a refusal nor "
                       f"a durable proceed, so a demotion branch exists")
    # POSITIVE CONTROL
    if durable_authoritative_outcome_NO_REFUSAL({"posture": "EPHEMERAL_ONLY"}) \
            == "REFUSE":
        out.append("RT25-D-INV-04: VACUOUS -- the no-refusal reading still refused")
    return out


def inv_d05(ctx: dict[str, Any]) -> list[str]:
    """The posture enum retains exactly two members and ABSENT is never one."""
    out: list[str] = []
    v24enum = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent.policyObject."
                                   "postureEnum", [])
    declared = get_path(ctx["doc"], "$.postureResolution.theDerivation.postureEnum", [])
    if list(v24enum) != list(POSTURE_ENUM):
        out.append(f"RT25-D-INV-05: v24's pinned postureEnum is {v24enum}")
    if list(declared) != list(POSTURE_ENUM):
        out.append(f"RT25-D-INV-05: v25's declared postureEnum is {declared}")
    if len(declared) != 2:
        out.append(f"RT25-D-INV-05: the enum has {len(declared)} members, not 2")
    if ABSENT in declared:
        out.append("RT25-D-INV-05: ABSENT is a posture enum member")
    added = get_path(ctx["doc"],
                     "$.postureResolution.theDerivation.postureEnumMembersAdded")
    if added != 0:
        out.append(f"RT25-D-INV-05: postureEnumMembersAdded is {added!r}, must be 0")
    forbidden = get_path(ctx["doc"],
                         "$.partC_retentionBounds.boundsRecord.forbiddenFields", [])
    if "posture" not in forbidden:
        out.append("RT25-D-INV-05: posture must be forbidden on the bounds record, "
                   "so there is no second place a posture could be spelled")
    return out


INVARIANT_DRIVERS = {
    "RT25-C-INV-01": inv_01, "RT25-C-INV-02": inv_02, "RT25-C-INV-03": inv_03,
    "RT25-C-INV-04": inv_04, "RT25-C-INV-05": inv_05, "RT25-C-INV-06": inv_06,
    "RT25-C-INV-07": inv_07, "RT25-C-INV-08": inv_08, "RT25-C-INV-09": inv_09,
    "RT25-C-INV-10": inv_10, "RT25-C-INV-11": inv_11, "RT25-C-INV-12": inv_12,
    "RT25-C-INV-13": inv_13, "RT25-C-INV-14": inv_14,
    "RT25-D-INV-01": inv_d01, "RT25-D-INV-02": inv_d02, "RT25-D-INV-03": inv_d03,
    "RT25-D-INV-04": inv_d04, "RT25-D-INV-05": inv_d05,
}


def run_invariants(doc: Any, ctx: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    findings: list[str] = []
    # The drivers read the SUBJECT through ctx["doc"].  Rebinding it here is what
    # makes them see a mutated document during the selftest; without this the
    # invariant family silently checks the pristine artifact under every mutation,
    # which is the "gathered the evidence and then did not use it" shape B-VER9R-01
    # names.  The selftest found it: MX-16..18 and MX-29..34 escaped until this line
    # existed.
    ctx = dict(ctx, doc=doc)
    declared = [i.get("id") for i in
                get_path(doc, "$.partC_retentionBounds.invariants", []) or []]
    if sorted(declared) != sorted(INVARIANT_IDS):
        findings.append(
            f"RT25-INV $.partC_retentionBounds.invariants: the artifact declares "
            f"{sorted(set(declared) - set(INVARIANT_IDS))} which this instrument does "
            f"not execute, and this instrument executes "
            f"{sorted(set(INVARIANT_IDS) - set(declared))} which the artifact does "
            f"not declare")
    executed = 0
    for inv_id in INVARIANT_IDS:
        driver = INVARIANT_DRIVERS.get(inv_id)
        if driver is None:
            findings.append(f"RT25-INV {inv_id}: no driver")
            continue
        executed += 1
        findings.extend(driver(ctx))
    return findings, {"declared": len(declared), "executed": executed}


# ===========================================================================
# SECTION 5 -- STRUCTURAL AND RECORDED-MEASUREMENT CHECKS.
# 7.2.2: a recorded measurement gets a HARD comparison against the measurement it
# records; a continuing invariant gets a semantic gate.  Every number below is
# RE-DERIVED from a pinned source and compared, never transcribed and narrated.
# ===========================================================================

def check_record(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """The 7.2 recording obligation: the artifact's own $.recordedInputs must
    agree with this checker's pin tables and with the live bytes."""
    out: list[str] = []
    recorded = get_path(doc, "$.recordedInputs.recorded", []) or []
    declared_count = get_path(doc, "$.recordedInputs.digestsRecordedCount")
    if declared_count != len(recorded):
        out.append(f"RT25-RECORD $.recordedInputs.digestsRecordedCount: declared "
                   f"{declared_count!r}, measured {len(recorded)}")
    by_path = {}
    for entry in recorded:
        path = entry.get("path")
        if path in by_path:
            out.append(f"RT25-RECORD $.recordedInputs.recorded: {path!r} recorded twice")
        by_path[path] = entry
    hard_declared = {p for p, e in by_path.items()
                     if e.get("gate", "").startswith("HARD-PIN")}
    hard_here = {f"artifacts/{n}" for n in PINS}
    if hard_declared != hard_here:
        out.append(
            f"RT25-RECORD $.recordedInputs.recorded: the artifact gates "
            f"{sorted(hard_declared - hard_here)} HARD and this instrument does not "
            f"pin them; this instrument pins {sorted(hard_here - hard_declared)} the "
            f"artifact does not gate HARD. A pin table and a recorded closure that "
            f"disagree mean one of them is describing a different execution")
    for path, entry in by_path.items():
        live = measured_digest(path)
        if live is None:
            out.append(f"RT25-RECORD {path}: recorded input is not readable on disk")
            continue
        if entry.get("sha256") == live:
            continue
        gate = entry.get("gate", "")
        if gate.startswith("HARD-PIN"):
            # already reported as an unsatisfiable pin or a refusal; restated here
            # against the ARTIFACT's own record so the finding names the position.
            out.append(
                f"RT25-RECORD {path}: the artifact records {entry.get('sha256')} "
                f"under gate {gate!r}; live is {live}. Recorded measurement, hard "
                f"comparison, 7.2.2.")
    # the two files v25 itself declares moved during authoring
    moved = get_path(doc, "$.recordedInputs.citedDigestsThatMovedDuringAuthoring", {})
    if moved.get("count") != len(moved.get("files") or []):
        out.append(f"RT25-RECORD ...citedDigestsThatMovedDuringAuthoring.count: "
                   f"{moved.get('count')!r} != {len(moved.get('files') or [])}")
    for name in moved.get("files") or []:
        if name not in RECORDED_NOT_GATED:
            out.append(f"RT25-RECORD ...citedDigestsThatMovedDuringAuthoring.files: "
                       f"{name!r} is not in this instrument's recorded-not-gated set")
    # the plan digest the artifact asserts is unchanged
    if moved.get("planDigestConfirmedUnchanged") is True:
        live = measured_digest("ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md")
        if moved.get("planDigestVerbatim") != live:
            out.append(f"RT25-RECORD ...planDigestVerbatim: declared "
                       f"{moved.get('planDigestVerbatim')}, live {live}, while "
                       f"planDigestConfirmedUnchanged is true")
    if get_path(doc, "$.recordedInputs.duplicateKeysFound") != 0:
        out.append("RT25-RECORD $.recordedInputs.duplicateKeysFound must be 0; this "
                   "checker parses with a duplicate-key-rejecting hook and would "
                   "have refused otherwise")
    if get_path(doc, "$.recordedInputs.filesWrittenByThisArtifact") != 1:
        out.append("RT25-RECORD $.recordedInputs.filesWrittenByThisArtifact must be 1")
    # FREEZE ANCHORS.  Removal of cited text fails closed.
    freeze = (COOP / "IMPLEMENTATION-FREEZE.md")
    if not freeze.is_file():
        out.append("RT25-RECORD IMPLEMENTATION-FREEZE.md is not readable")
    else:
        text = _norm(freeze.read_text(encoding="utf-8"))
        for anchor in FREEZE_ANCHORS:
            if _norm(anchor) not in text:
                out.append(f"RT25-FREEZE-ANCHOR absent from the live freeze: "
                           f"{anchor[:90]!r}")
        heading = re.search(r"### 4\.5 Recorded product intent on `CD-RT-5`([^\n]*)",
                            freeze.read_text(encoding="utf-8"))
        live_disposition = (heading.group(1) if heading else "").strip(" —-")
        if FREEZE_4_5_DISPOSITION_AT_AUTHORING not in live_disposition:
            out.append(
                f"RT25-FREEZE-4.5 the section this artifact's whole authority framing "
                f"rests on has changed disposition: it read "
                f"{FREEZE_4_5_DISPOSITION_AT_AUTHORING!r} when v25 was authored and "
                f"reads {live_disposition!r} now. $.recordedProductIntent describes "
                f"the intent as recorded-and-not-constituted; if 4.5 is superseded by "
                f"an actual decision, that framing no longer describes the corpus. "
                f"Reported as an ADVANCE in a concurrently-edited document, not as a "
                f"defect in these bytes.")
    return out


def check_authority(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """The authority boundary.  A candidate that quietly acquires standing is the
    failure section 4.4 is the forensic record of."""
    out: list[str] = []
    expect = {"$.status": "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REVIEW",
              "$.sealRecommendation": "DO-NOT-SEAL",
              "$.retainedChecker": "NONE",
              "$.authority.candidateState": "NOT-APPLIED",
              "$.authority.authorityClaim": "NONE",
              "$.authority.productionExecutionClaim": "NONE",
              "$.authority.evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
              "$.integrationState.candidateState": "NOT-APPLIED",
              "$.integrationState.independentAcceptance": "NOT-GRANTED",
              "$.integrationState.V10": "UNRESOLVED",
              "$.integrationState.CD-RT-5": "BLOCKED_ON_PHASE_1A",
              "$.productAuthorityBoundary.CD-RT-5": "BLOCKED_ON_PHASE_1A",
              "$.productAuthorityBoundary.durableDefault": "UNSELECTED",
              "$.closedRecordExtension.durableDefaultInThePacketRemains": "UNSELECTED",
              "$.v10Item3Position.claimedStatusForTheseBytes": "NO CLAIM MADE",
              "$.v10Item3Position.statusChangesMadeByThisArtifact": "NONE"}
    for path, value in expect.items():
        got = get_path(doc, path)
        if got != value:
            out.append(f"RT25-AUTH {path}: {got!r}, must be {value!r}")
    for path in ("$.authority.mayConstituteAProductDecision",
                 "$.authority.mayAmendD9Vocabulary",
                 "$.authority.mayAmendOperabilityGates",
                 "$.authority.mayAmendThreatModel",
                 "$.authority.mayAmendTheProductDispositionPacket",
                 "$.authority.mayApplyTheCdRt5AmendmentDraft",
                 "$.freezeDeclaration.constitutesASealOrSignature",
                 "$.freezeDeclaration.changesAnyStatus",
                 "$.freezeDeclaration.changesAnyOtherArtifact",
                 "$.productAuthorityBoundary.amendmentDraft.appliedByThisArtifact"):
        got = get_path(doc, path)
        if got is not False:
            out.append(f"RT25-AUTH {path}: {got!r}, must be false")
    if get_path(doc, "$.authority.bindsNothing") is not True:
        out.append("RT25-AUTH $.authority.bindsNothing must be true")
    if get_path(doc, "$.freezeDeclaration.filesEdited") != 0:
        out.append("RT25-AUTH $.freezeDeclaration.filesEdited must be 0")
    if get_path(doc, "$.freezeDeclaration.filesCreated") != 1:
        out.append("RT25-AUTH $.freezeDeclaration.filesCreated must be 1")
    # the LIVE packet must still say what the artifact reports it says.  v25 reads
    # it from a NAMED position, so the position is resolved rather than searched:
    # a decision that MOVES from pendingDecisions to decisions is exactly the event
    # this artifact's whole productAuthorityBoundary block is written to survive,
    # and it must be reported rather than absorbed by looking the row up elsewhere.
    where = get_path(doc, "$.productAuthorityBoundary.packetStateReadLiveFrom", "")
    pointer = where.split("#")[-1].lstrip("/").replace("/", ".") if where else ""
    packet = get_path(ctx["product"], "$." + pointer, {}) if pointer else {}
    if not packet:
        decided = get_path(ctx["product"], "$.decisions.CD-RT-5", {})
        out.append(
            f"RT25-AUTH $.productAuthorityBoundary.packetStateReadLiveFrom: the named "
            f"position {where!r} no longer resolves in the pinned packet"
            + (f"; CD-RT-5 has MOVED to $.decisions with status "
               f"{decided.get('status')!r} (decidedOn {decided.get('decidedOn')!r}). "
               f"The amendment this artifact designs against as DRAFT-NOT-APPLIED has "
               f"been APPLIED, so every statement in $.productAuthorityBoundary about "
               f"holding the tension open now describes a state that no longer exists."
               if decided else ""))
    if packet.get("status") != get_path(doc, "$.productAuthorityBoundary."
                                             "packetStateAsMeasured"):
        out.append(f"RT25-AUTH $.productAuthorityBoundary.packetStateAsMeasured: "
                   f"declared {get_path(doc, '$.productAuthorityBoundary.packetStateAsMeasured')!r}, "
                   f"the pinned packet says {packet.get('status')!r}")
    rule = get_path(doc, "$.productAuthorityBoundary.packetRuleWhilePendingVerbatim")
    if rule != packet.get("ruleWhilePending"):
        out.append("RT25-AUTH $.productAuthorityBoundary."
                   "packetRuleWhilePendingVerbatim is not verbatim from the pinned "
                   "packet")
    if "durableDefault" in packet:
        out.append("RT25-AUTH the pinned packet has acquired a durableDefault field; "
                   "this artifact reports it as UNSELECTED because the packet has "
                   "selected nothing")
    # the overridden recommendation, quoted from PINNED v22 bytes
    rec = get_path(doc, "$.overriddenArchitecturalRecommendation.theRecommendation", {})
    v22rec = get_path(ctx["v22"], "$.custodyPolicy.recommendedDefaultPosture", {})
    for key, source in (("recommendationVerbatim", "recommendation"),
                        ("whenPolicyMissingVerbatim", "whenPolicyMissing"),
                        ("statusVerbatim", "status"),
                        ("authorityVerbatim", "authority"),
                        ("currentProductStateVerbatim", "currentProductState"),
                        ("durableDefaultVerbatim", "durableDefault")):
        if rec.get(key) != v22rec.get(source):
            out.append(f"RT25-AUTH $.overriddenArchitecturalRecommendation."
                       f"theRecommendation.{key}: {rec.get(key)!r} is not verbatim "
                       f"from the pinned v22 {source} {v22rec.get(source)!r}")
    return out


def check_inheritance(doc: Any, ctx: dict[str, Any]) -> list[str]:
    out: list[str] = []
    pred = get_path(doc, "$.inheritance.predecessor", {})
    if pred.get("sha256") != PINS["retention-tiers.v24.json"]:
        out.append(f"RT25-INHERIT $.inheritance.predecessor.sha256: "
                   f"{pred.get('sha256')} != the pinned v24 digest")
    rev = get_path(doc, "$.inheritance.predecessorReview", {})
    if rev.get("sha256") != PINS["retention-tiers.v24.review-independent.json"]:
        out.append("RT25-INHERIT $.inheritance.predecessorReview.sha256 != the "
                   "pinned v24 review digest")
    verdict = get_path(ctx["v24rev"], "$.verdict", {})
    text = json.dumps(verdict)
    for key in ("partABlockingFindingCount", "partBBlockingFindingCount",
                "totalBlockingFindingCount"):
        if rev.get(key) != 0:
            out.append(f"RT25-INHERIT $.inheritance.predecessorReview.{key} is "
                       f"{rev.get(key)!r}; the inheritance rests on 0 blockers")
    quoted = rev.get("overallVerdictVerbatim", "")
    if quoted and _norm(quoted) not in _norm(text) and _norm(quoted) not in \
            _norm(json.dumps(ctx["v24rev"])):
        out.append(f"RT25-INHERIT $.inheritance.predecessorReview."
                   f"overallVerdictVerbatim {quoted!r} does not occur in the pinned "
                   f"review bytes")
    if get_path(doc, "$.inheritance.predecessorIsNotEdited") is not True:
        out.append("RT25-INHERIT $.inheritance.predecessorIsNotEdited must be true")
    changed = get_path(doc, "$.inheritance.surfacesThisArtifactChanges", []) or []
    unchanged = get_path(doc, "$.inheritance.surfacesThisArtifactDoesNotChange", []) or []
    if get_path(doc, "$.inheritance.surfacesChangedCount") != len(changed):
        out.append("RT25-INHERIT $.inheritance.surfacesChangedCount != len(changes)")
    if get_path(doc, "$.inheritance.surfacesExplicitlyUnchangedCount") != len(unchanged):
        out.append("RT25-INHERIT $.inheritance.surfacesExplicitlyUnchangedCount "
                   "!= len(unchanged)")
    overlap = {c.get("surface") for c in changed} & set(unchanged)
    if overlap:
        out.append(f"RT25-INHERIT surfaces named BOTH changed and unchanged: "
                   f"{sorted(overlap)}")
    # every named surface must resolve in the PINNED predecessor
    for surface in [c.get("surface") for c in changed] + list(unchanged):
        base = surface.split(" ")[0]
        if base.startswith("$.partA_") or base.startswith("$.partB_"):
            if get_path(ctx["v24"], base, "__MISSING__") == "__MISSING__":
                out.append(f"RT25-INHERIT {surface!r} does not resolve in the pinned "
                           f"retention-tiers.v24.json")
    # the 11 -> 12 forbiddenInputs widening, measured
    forbidden = get_path(ctx["v24"], "$.partB_purgeSemantics."
                                     "effectiveCapabilityDerivation.forbiddenInputs", [])
    deltas = get_path(doc, "$.partC_retentionBounds.whyThisIsSmallerThanItLooks."
                           "measuredDeltas", {})
    checks = {
        "effectiveCapabilityForbiddenInputsBefore": len(forbidden),
        "effectiveCapabilityForbiddenInputsAfter": len(forbidden) + 1,
        "effectiveCapabilityInputsBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.effectiveCapabilityDerivation.inputs", [])),
        "effectiveCapabilityInputsAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.effectiveCapabilityDerivation.inputs", [])),
        "availabilityStatesBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.availabilityStateLattice.states", [])),
        "availabilityStatesAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.availabilityStateLattice.states", [])),
        "terminalStatesBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.availabilityStateLattice."
                        "terminalStates", [])),
        "terminalStatesAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.availabilityStateLattice."
                        "terminalStates", [])),
        "ledgerEntryOrderedFieldsBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.ledger.entryOrderedFields", [])),
        "ledgerEntryOrderedFieldsAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.ledger.entryOrderedFields", [])),
        "purgeMutatesExactlyBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary."
                        "mutatesExactly", [])),
        "purgeMutatesExactlyAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary."
                        "mutatesExactly", [])),
        "purgeDoesNotMutateBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary."
                        "doesNotMutate", [])),
        "purgeDoesNotMutateAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary."
                        "doesNotMutate", [])),
        "typedRefusalKindsBefore": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.availabilityStateLattice."
                        "refusalKinds", {}) or {}),
        "typedRefusalKindsAfter": len(get_path(
            ctx["v24"], "$.partB_purgeSemantics.availabilityStateLattice."
                        "refusalKinds", {}) or {}),
    }
    for key, measured in checks.items():
        if deltas.get(key) != measured:
            out.append(f"RT25-INHERIT ...measuredDeltas.{key}: declared "
                       f"{deltas.get(key)!r}, measured {measured} from the pinned "
                       f"retention-tiers.v24.json")
    # cause must be at ordered position 7 and must not be a new field
    fields = get_path(ctx["v24"], "$.partB_purgeSemantics.ledger.entryOrderedFields", [])
    if list(fields)[-1:] != ["cause"]:
        out.append(f"RT25-INHERIT the pinned entryOrderedFields end {fields[-1:]}, "
                   f"not ['cause']; v25's orderedPosition 7 rests on this")
    if get_path(doc, "$.partC_retentionBounds.causeVocabulary.orderedPosition") != \
            len(fields):
        out.append("RT25-INHERIT $.partC.causeVocabulary.orderedPosition != the "
                   "pinned position of cause in entryOrderedFields")
    for flag in ("positionUnchanged", "fieldIsNotNew"):
        if get_path(doc, f"$.partC_retentionBounds.causeVocabulary.{flag}") is not True:
            out.append(f"RT25-INHERIT $.partC.causeVocabulary.{flag} must be true")
    return out


def check_part_a_prime(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """Part A-prime, measured against the PINNED predecessor's own tables.

    v25 claims the changed cells were found BY MEASUREMENT ("exactly the cells
    whose policyPresence is ABSENT and whose requestedCustody is
    DURABLE_AUTHORITATIVE").  That claim is executable, so it is executed.
    """
    out: list[str] = []
    A = get_path(doc, "$.partA_repairsForcedByThePostureDecision", {})
    cells = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                 "askDecisionTable.cells", []) or []
    table = A.get("askDecisionTable", {})
    if table.get("cellCount") != len(cells):
        out.append(f"RT25-A' ...askDecisionTable.cellCount: {table.get('cellCount')!r}, "
                   f"pinned v24 has {len(cells)}")
    asked = sum(1 for c in cells if c.get("askPerformed"))
    for key in ("askPerformedCellCountBefore", "askPerformedCellCountAfter"):
        if table.get(key) != asked:
            out.append(f"RT25-A' ...{key}: {table.get(key)!r}, measured {asked}")
    measured_changed = [c for c in cells if c.get("policyPresence") == "ABSENT"
                        and c.get("requestedCustody") == "DURABLE_AUTHORITATIVE"]
    if table.get("cellsChanged") != len(measured_changed):
        out.append(f"RT25-A' ...cellsChanged: {table.get('cellsChanged')!r}, the "
                   f"stated rule selects {len(measured_changed)} cells from the "
                   f"pinned table")
    if table.get("cellsUnchanged") != len(cells) - len(measured_changed):
        out.append(f"RT25-A' ...cellsUnchanged: {table.get('cellsUnchanged')!r}, "
                   f"measured {len(cells) - len(measured_changed)}")
    declared_changed = table.get("changedCells") or []
    key_of = lambda c: (c.get("invocationProfile"), c.get("policyPresence"),
                        c.get("requestedCustody"))
    if {key_of(c) for c in declared_changed} != {key_of(c) for c in measured_changed}:
        out.append(f"RT25-A' ...changedCells: the declared set "
                   f"{sorted(key_of(c) for c in declared_changed)} is not the set the "
                   f"stated rule selects "
                   f"{sorted(key_of(c) for c in measured_changed)}")
    for declared in declared_changed:
        live = next((c for c in cells if key_of(c) == key_of(declared)), None)
        if live is None:
            continue
        before = declared.get("outcomeBefore")
        if before is not None and not before.startswith(live.get("outcome", "")):
            out.append(f"RT25-A' changed cell {key_of(declared)} outcomeBefore "
                       f"{before!r} does not open with the pinned v24 outcome "
                       f"{live.get('outcome')!r}")
        d9before = declared.get("d9Before")
        if d9before:
            for key in ("derivedClass", "derivedExitCode", "derivedErrorCode"):
                if d9before.get(key) != live.get(key):
                    out.append(f"RT25-A' changed cell {key_of(declared)} d9Before."
                               f"{key}: declared {d9before.get(key)!r}, pinned "
                               f"{live.get(key)!r}")
        d9after = declared.get("d9After")
        if d9after:
            sentinel = (d9after.get("derivedClass"), d9after.get("derivedExitCode"),
                        d9after.get("derivedErrorCode"))
            users = [c for c in cells if (c.get("derivedClass"),
                                          c.get("derivedExitCode"),
                                          c.get("derivedErrorCode")) == sentinel]
            if not users:
                out.append(f"RT25-A' changed cell {key_of(declared)} d9After "
                           f"{sentinel} is AUTHORED: no cell in the pinned v24 table "
                           f"uses it, so d9AfterIsStructuralNotAuthored is false")
            # the artifact's own cardinality claim about that sentinel, measured.
            claim = d9after and declared.get("d9AfterIsStructuralNotAuthored", "")
            match = re.search(r"\b(?:the )?(\w+) other non-terminating cells", claim or "")
            if match:
                words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                         "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                         "eleven": 11, "twelve": 12}
                stated = words.get(match.group(1))
                others = [c for c in users if key_of(c) not in
                          {key_of(x) for x in declared_changed}]
                if stated is not None and stated != len(users) and \
                        stated != len(others):
                    out.append(
                        f"RT25-A' changed cell {key_of(declared)} "
                        f"d9AfterIsStructuralNotAuthored says {match.group(1)!r} other "
                        f"non-terminating cells; measured on the pinned v24 table "
                        f"there are {len(users)} cells carrying that sentinel "
                        f"({len(others)} excluding the cells this artifact changes). "
                        f"Recorded measurement, hard comparison, 7.2.2.")
    outcomes = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                    "interactionOutcomes.outcomes", []) or []
    IO = A.get("interactionOutcomes", {})
    if IO.get("count") != len(outcomes):
        out.append(f"RT25-A' ...interactionOutcomes.count: {IO.get('count')!r}, "
                   f"pinned v24 has {len(outcomes)}")
    persisting = [o["id"] for o in outcomes if o.get("policyPersisted")]
    for key in ("policyPersistingOutcomeIdsBefore", "policyPersistingOutcomeIdsAfter"):
        if IO.get(key) != persisting:
            out.append(f"RT25-A' ...{key}: {IO.get(key)!r}, measured {persisting}")
    declared_io = [c.get("id") for c in IO.get("changed") or []]
    declared_un = [c.get("id") for c in IO.get("unchanged") or []]
    if IO.get("outcomesChanged") != len(declared_io):
        out.append("RT25-A' ...outcomesChanged != len(changed)")
    if IO.get("outcomesUnchanged") != len(declared_un):
        out.append("RT25-A' ...outcomesUnchanged != len(unchanged)")
    if len(declared_io) + len(declared_un) != len(outcomes):
        out.append(f"RT25-A' the changed and unchanged outcome lists cover "
                   f"{len(declared_io) + len(declared_un)} of {len(outcomes)} outcomes")
    if set(declared_io) & set(declared_un):
        out.append(f"RT25-A' outcomes named both changed and unchanged: "
                   f"{sorted(set(declared_io) & set(declared_un))}")
    rule_set = {o["id"] for o in outcomes
                if o.get("terminatesTheRequest") and not o.get("policyPersisted")}
    if set(declared_io) != rule_set:
        out.append(f"RT25-A' the changed outcomes {sorted(declared_io)} are not the "
                   f"terminating-and-not-persisting set {sorted(rule_set)} the "
                   f"posture rule selects from the pinned table")
    for entry in IO.get("changed") or []:
        live = next((o for o in outcomes if o["id"] == entry.get("id")), {})
        if entry.get("terminatesBefore") != live.get("terminatesTheRequest"):
            out.append(f"RT25-A' {entry.get('id')} terminatesBefore "
                       f"{entry.get('terminatesBefore')!r}, pinned "
                       f"{live.get('terminatesTheRequest')!r}")
    if IO.get("allFourStillPersistNoPolicy") is not True:
        out.append("RT25-A' ...allFourStillPersistNoPolicy must be true")
    d9r = IO.get("d9DerivationsAreNotRecomputedHere", {})
    if d9r.get("outcomesNeedingRecomputation") != len(declared_io):
        out.append(f"RT25-A' ...outcomesNeedingRecomputation "
                   f"{d9r.get('outcomesNeedingRecomputation')!r} != "
                   f"{len(declared_io)} changed outcomes")
    if d9r.get("outcomesRecomputedHere") != 0:
        out.append("RT25-A' ...outcomesRecomputedHere must be 0; this artifact "
                   "retains no checker that could execute the D9 derivation")
    cases = A.get("noAskCasesReDerived") or []
    v24cases = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent.noAskCases", [])
    if A.get("noAskCaseCount") != len(v24cases):
        out.append(f"RT25-A' ...noAskCaseCount {A.get('noAskCaseCount')!r}, pinned "
                   f"v24 has {len(v24cases)}")
    if A.get("noAskCasesReDerivedCount") != len(cases):
        out.append("RT25-A' ...noAskCasesReDerivedCount != len(noAskCasesReDerived)")
    if A.get("noAskCasesSilentlyDeleted") != 0:
        out.append("RT25-A' ...noAskCasesSilentlyDeleted must be 0")
    if len(cases) != len(v24cases):
        out.append(f"RT25-A' {len(cases)} of {len(v24cases)} pinned noAskCases were "
                   f"re-derived; a case dropped silently is exactly what "
                   f"noAskCasesSilentlyDeleted 0 denies")
    for case in cases:
        for key in ("predecessorDecisionVerbatim", "predecessorChoiceVerbatim"):
            quoted = case.get(key)
            if quoted and _norm(quoted) not in _norm(json.dumps(v24cases)):
                out.append(f"RT25-A' noAskCase {case.get('case')} {key} is not "
                           f"verbatim from the pinned v24 noAskCases")
        for quoted in case.get("predecessorPropertiesVerbatim") or []:
            key = quoted.split(":")[0].strip()
            if key and key not in json.dumps(v24cases):
                out.append(f"RT25-A' noAskCase {case.get('case')} quotes "
                           f"{key!r}, absent from the pinned v24 noAskCases")
    return out


def check_part_d(doc: Any, _ctx: dict[str, Any]) -> list[str]:
    out: list[str] = []
    D = get_path(doc, "$.postureResolution", {})
    der = D.get("theDerivation", {})
    rows = der.get("rows") or []
    if der.get("rowCount") != len(rows):
        out.append(f"RT25-D ...theDerivation.rowCount {der.get('rowCount')!r} != "
                   f"{len(rows)}")
    inputs = []
    for row in rows:
        spec = row.get("input", "")
        candidate = ABSENT if spec == "ABSENT" else (
            {"posture": spec.split("== ")[-1].strip()} if "==" in spec else None)
        if candidate is None:
            out.append(f"RT25-D ...theDerivation.rows: input {spec!r} is not one this "
                       f"instrument can execute, so a declared row is unexercised")
            continue
        inputs.append(candidate)
        try:
            posture, provenance = effective_posture(candidate)
        except RefusedError as exc:
            out.append(f"RT25-D row {spec!r} refused ({exc})")
            continue
        if posture != row.get("posture") or provenance != row.get("provenance"):
            out.append(f"RT25-D row {spec!r}: declared "
                       f"({row.get('posture')!r}, {row.get('provenance')!r}), derived "
                       f"({posture!r}, {provenance!r})")
    if len(inputs) != 3:
        out.append(f"RT25-D the derivation table exercises {len(inputs)} inputs; "
                   f"ABSENT plus the two posture enum members is 3, and totality is "
                   f"a claim about all of them")
    for flag in ("isTotal", "neverReturnsAbsent", "isPure", "readsNoClock",
                 "readsNoOtherProject", "postureEnumIsClosed", "provenanceEnumIsClosed"):
        if der.get(flag) is not True:
            out.append(f"RT25-D ...theDerivation.{flag} must be true")
    if list(der.get("provenanceEnum") or []) != list(POSTURE_PROVENANCE_ENUM):
        out.append(f"RT25-D ...provenanceEnum {der.get('provenanceEnum')}")
    key = D.get("theKeyProperty", {})
    if key.get("id") != "EPHEMERAL_ONLY-IS-ALWAYS-CONSENTED":
        out.append("RT25-D ...theKeyProperty.id drifted")
    law14 = D.get("lawFourteenPosition", {})
    if law14.get("silentDemotionIsStillForbidden") is not True:
        out.append("RT25-D ...lawFourteenPosition.silentDemotionIsStillForbidden "
                   "must be true")
    demotion = law14.get("theDemotionThatIsStillForbidden", {})
    if demotion.get("isItReachableUnderTheNewDefault") is not False:
        out.append("RT25-D ...isItReachableUnderTheNewDefault must be false")
    verbatim = law14.get("lawVerbatim", "")
    freeze = COOP / "IMPLEMENTATION-FREEZE.md"
    if freeze.is_file() and verbatim and \
            _norm(verbatim) not in _norm(freeze.read_text(encoding="utf-8")):
        out.append("RT25-D ...lawFourteenPosition.lawVerbatim is not verbatim in the "
                   "live freeze")
    # the bounds resolution table, executed the same way
    br = get_path(doc, "$.partC_retentionBounds.boundsRecord."
                       "effectiveBoundsResolution", {})
    for row in br.get("rows") or []:
        candidate = ABSENT if row.get("input") == "ABSENT" else bounds_record(0, 0, 0)
        age, size, keep, prov = effective_bounds(candidate)
        if prov != row.get("provenance"):
            out.append(f"RT25-D ...effectiveBoundsResolution row {row.get('input')!r}: "
                       f"declared provenance {row.get('provenance')!r}, derived "
                       f"{prov!r}")
        if row.get("input") == "ABSENT" and f"{age} / {size} / {keep}" != \
                row.get("values"):
            out.append(f"RT25-D ...effectiveBoundsResolution ABSENT values "
                       f"{row.get('values')!r} != derived {age} / {size} / {keep}")
    if br.get("isTotal") is not True:
        out.append("RT25-D ...effectiveBoundsResolution.isTotal must be true")
    if list(br.get("provenanceEnum") or []) != list(BOUNDS_PROVENANCE_ENUM):
        out.append(f"RT25-D ...effectiveBoundsResolution.provenanceEnum "
                   f"{br.get('provenanceEnum')}")
    for flag in ("provenanceIsNeverPersisted", "theDefaultIsNeverWrittenToDisk",
                 "absentAndAllZeroAgreeOnValuesAndDifferOnProvenance"):
        if br.get(flag) is not True:
            out.append(f"RT25-D ...effectiveBoundsResolution.{flag} must be true")
    return out


def check_part_c_structure(doc: Any, ctx: dict[str, Any]) -> list[str]:
    out: list[str] = []
    C = get_path(doc, "$.partC_retentionBounds", {})
    record = C.get("boundsRecord", {})
    if list(record.get("orderedFields") or []) != list(BOUNDS_ORDERED_FIELDS):
        out.append(f"RT25-C $.partC.boundsRecord.orderedFields "
                   f"{record.get('orderedFields')}")
    if record.get("fieldCount") != len(record.get("orderedFields") or []):
        out.append("RT25-C $.partC.boundsRecord.fieldCount != len(orderedFields)")
    if set(record.get("fieldTypes") or {}) != set(record.get("orderedFields") or []):
        out.append("RT25-C $.partC.boundsRecord.fieldTypes does not cover exactly "
                   "orderedFields")
    identity = C.get("identity", {})
    preimage = identity.get("preimage", "")
    tags = re.findall(r"0x0([1-9a-f])", preimage)
    if identity.get("fieldCount") != len(set(tags)):
        out.append(f"RT25-C $.partC.identity.fieldCount {identity.get('fieldCount')!r} "
                   f"!= {len(set(tags))} distinct field tags in the preimage")
    for field in ("projectId", "retentionPolicyId", "maxAgeSeconds", "maxTotalBytes",
                  "keepCount", "boundsRevision"):
        if field not in preimage:
            out.append(f"RT25-C $.partC.identity.preimage does not name {field!r}, "
                       f"which fieldCount {identity.get('fieldCount')!r} counts")
    for excluded in identity.get("excluded") or []:
        if re.fullmatch(r"[A-Za-z]+", excluded) and excluded in preimage:
            out.append(f"RT25-C $.partC.identity: {excluded!r} is declared excluded "
                       f"and appears in the preimage")
    if not re.fullmatch(r"\^rbnd1:sha256:\[0-9a-f\]\{64\}\$",
                        identity.get("textPattern", "")):
        out.append(f"RT25-C $.partC.identity.textPattern "
                   f"{identity.get('textPattern')!r} is not the declared shape")
    # forbidden fields must be genuinely absent from the record's own field set
    for forbidden in record.get("forbiddenFields") or []:
        if forbidden in (record.get("orderedFields") or []):
            out.append(f"RT25-C {forbidden!r} is both a forbidden field and an "
                       f"ordered field of the bounds record")
    # the cause partition
    cv = C.get("causeVocabulary", {})
    closed = (cv.get("closedPartitions") or [{}])[0]
    members = closed.get("members") or []
    if list(members) != list(CAUSE_PARTITION):
        out.append(f"RT25-C the closed PURGED cause partition is {members}; this "
                   f"instrument executes {list(CAUSE_PARTITION)}")
    if closed.get("memberCount") != len(members):
        out.append("RT25-C ...closedPartitions[0].memberCount != len(members)")
    if set(closed.get("meanings") or {}) != set(members):
        out.append("RT25-C ...closedPartitions[0].meanings does not cover exactly "
                   "the members")
    rule = (closed.get("attributionRuleWhenSeveralDemandsCover") or {}).get("rule", "")
    # Ordered BY POSITION IN THE TEXT, not by this instrument's own order.  Filtering
    # CAUSE_TIEBREAK by membership would reproduce the checker's order whatever the
    # artifact said, which is a check that cannot fail -- the selftest caught it as
    # escape MX-78-TIEBREAK-ORDER-REVERSED.
    stated = [m for _, m in sorted((rule.index(m), m) for m in CAUSE_TIEBREAK
                                   if m in rule)]
    if [m for m in CAUSE_TIEBREAK] != stated:
        out.append(f"RT25-C the attribution tiebreak order stated in the rule is "
                   f"{stated}; this instrument executes {list(CAUSE_TIEBREAK)}")
    lattice_states = get_path(ctx["v24"], "$.partB_purgeSemantics."
                                          "availabilityStateLattice.states", [])
    open_partitions = [p.get("toState") for p in cv.get("unclosedPartitions") or []]
    if sorted(open_partitions + [closed.get("toState")]) != sorted(lattice_states):
        out.append(f"RT25-C the closed and unclosed partitions cover "
                   f"{sorted(open_partitions + [closed.get('toState')])}; the pinned "
                   f"lattice has {sorted(lattice_states)}")
    # the demands rows, and the disable semantics
    rows = get_path(doc, "$.partC_retentionBounds.sweep.demands.rows", []) or []
    if len(rows) != 3:
        out.append(f"RT25-C $.partC.sweep.demands.rows has {len(rows)} rows, 3 "
                   f"dimensions expected")
    for row in rows:
        dim = row.get("dimension")
        if dim not in DIMENSION_CAUSE:
            out.append(f"RT25-C demand row dimension {dim!r} is not one of "
                       f"{sorted(DIMENSION_CAUSE)}")
            continue
        disabled = row.get("disabledWhen", "")
        if not re.search(r"==\s*0\s*$", disabled):
            out.append(f"RT25-C demand row {dim!r} disabledWhen {disabled!r} is not "
                       f"'<field> == 0'; the zeroDisables convention is what makes "
                       f"the default 0/0/0 expressible")
    if get_path(doc, "$.partC_retentionBounds.sweep.disableSemantics."
                     "zeroDisables") is not True:
        out.append("RT25-C $.partC.sweep.disableSemantics.zeroDisables must be true")
    composition = get_path(doc, "$.partC_retentionBounds.sweep.demands.composition", "")
    if "max(" not in composition or "sum" in composition.lower():
        out.append(f"RT25-C $.partC.sweep.demands.composition {composition!r} must be "
                   f"a max, never a sum")
    # the D9 error code the disable semantics report, against the PINNED vocabulary
    report = get_path(doc, "$.partC_retentionBounds.sweep.disableSemantics."
                           "howAnInvalidConfigurationIsReported", {})
    if report.get("errorCode") not in ctx["d9errorCodes"]:
        out.append(f"RT25-C the invalid-configuration error code "
                   f"{report.get('errorCode')!r} is not in the live pinned D9 "
                   f"closed error-code vocabulary")
    if report.get("measuredPresent") is not True or \
            report.get("codeAlreadyExistsInTheLiveVocabulary") is not True:
        out.append("RT25-C ...howAnInvalidConfigurationIsReported must record the "
                   "code as measured present in the live vocabulary")
    if report.get("exitCode") != get_path(ctx["d9"], "$.classToExitCode.request-rejected",
                                          report.get("exitCode")):
        out.append(f"RT25-C the declared exit code {report.get('exitCode')!r} does not "
                   f"match the pinned D9 classToExitCode for its class")
    # the protected set is DERIVED, not enumerated
    protected = C.get("protectedSet", {})
    members = protected.get("membersAndTheInvariantThatProtectsThem") or []
    does_not = get_path(ctx["v24"], "$.partB_purgeSemantics.purgeMutationBoundary."
                                    "doesNotMutate", [])
    joined = " ".join(m.get("member", "") for m in members)
    if str(len(does_not)) not in joined:
        out.append(f"RT25-C $.partC.protectedSet does not name the pinned "
                   f"doesNotMutate cardinality {len(does_not)}, so the derivation "
                   f"cannot be checked against its source")
    for flag in ("protectedSetIsNotEvictableByAnyBound", "noBoundCanShrinkIt"):
        if protected.get(flag) is not True:
            out.append(f"RT25-C $.partC.protectedSet.{flag} must be true")
    if C.get("evictableSet", {}).get("outageIsNeverEvictable") is not True:
        out.append("RT25-C $.partC.evictableSet.outageIsNeverEvictable must be true")
    sweep = C.get("sweep", {})
    for flag in ("isATriggerNotAGate", "emitsNoOtherToState",
                 "appendsToTheExistingLedger", "introducesNoNewMutation"):
        if sweep.get(flag) is not True:
            out.append(f"RT25-C $.partC.sweep.{flag} must be true")
    order = sweep.get("evictionOrder", {})
    for flag in ("isTotal", "isDeterministic", "readsNoClock",
                 "sameOrderForEveryDimension"):
        if order.get(flag) is not True:
            out.append(f"RT25-C $.partC.sweep.evictionOrder.{flag} must be true")
    independence = sweep.get("boundIndependence", {})
    for flag in ("readsNoOtherBoundsValue", "isAlgebraicallyMonotone"):
        if independence.get(flag) is not True:
            out.append(f"RT25-C $.partC.sweep.boundIndependence.{flag} must be true")
    scope = sweep.get("scope", {})
    if scope.get("perProject") is not True or scope.get("global") is not False:
        out.append("RT25-C $.partC.sweep.scope must be perProject and not global")
    for fact in scope.get("supportingFacts") or []:
        if "ledgerSequenceOfAnyOtherProject" in fact:
            forbidden = get_path(ctx["v24"], "$.partB_purgeSemantics."
                                             "effectiveCapabilityDerivation."
                                             "forbiddenInputs", [])
            if "ledgerSequenceOfAnyOtherProject" not in forbidden:
                out.append("RT25-C the scope derivation rests on "
                           "ledgerSequenceOfAnyOtherProject already being a "
                           "forbidden input; it is not one in the pinned v24 bytes")
    over = sweep.get("whenTheBoundCannotBeSatisfied", {}).get("whatIsDoneInstead", {})
    for key in ("newRecordTypes", "newLedgerEntries", "newAvailabilityStates"):
        if over.get(key) != 0:
            out.append(f"RT25-C ...whatIsDoneInstead.{key} must be 0")
    if over.get("mechanism") != "DERIVED, NOT RECORDED":
        out.append("RT25-C ...whatIsDoneInstead.mechanism drifted")
    return out


def check_census(doc: Any, _ctx: dict[str, Any]) -> list[str]:
    """7.2.2 corollary: the only census that can be published is one re-walked from
    the written bytes AFTER the write.  So this one is re-walked here, from the
    bytes on disk, and hard-compared."""
    out: list[str] = []
    declared = get_path(doc, "$.leafCensus", {})
    walked = census(doc)
    counts = walked["counts"]
    expect = {"scalarLeafPositions": counts["scalar"],
              "nonStringLeafPositions": counts["nonString"],
              "intLeafPositions": counts["int"], "floatLeafPositions": counts["float"],
              "boolLeafPositions": counts["bool"], "nullLeafPositions": counts["null"],
              "stringLeafPositions": counts["str"]}
    for key, value in expect.items():
        if declared.get(key) != value:
            out.append(f"RT25-CENSUS $.leafCensus.{key}: declared "
                       f"{declared.get(key)!r}, re-walked {value}")
    if counts["nonString"] != counts["int"] + counts["bool"] + counts["float"] + \
            counts["null"]:
        out.append("RT25-CENSUS the non-string arithmetic does not close")
    if counts["scalar"] != counts["nonString"] + counts["str"]:
        out.append("RT25-CENSUS the total arithmetic does not close")
    if list(declared.get("floatLeafPaths") or []) != walked["floatLeafPaths"]:
        out.append(f"RT25-CENSUS $.leafCensus.floatLeafPaths: declared "
                   f"{declared.get('floatLeafPaths')}, re-walked "
                   f"{walked['floatLeafPaths']}")
    if list(declared.get("nullLeafPaths") or []) != walked["nullLeafPaths"]:
        out.append(f"RT25-CENSUS $.leafCensus.nullLeafPaths: declared "
                   f"{declared.get('nullLeafPaths')}, re-walked "
                   f"{walked['nullLeafPaths']}")
    if walked["floatLeafPaths"] != [KEEPCOUNT_FLOAT_PATH]:
        out.append(f"RT25-CENSUS the single deliberate float control must be the "
                   f"only float leaf; re-walked {walked['floatLeafPaths']}")
    for key in ("censusIncludesItsOwnIntegers", "fixedPointReached",
                "everyFloatIsDeliberate", "reParsedWithDuplicateKeyRejectingHook"):
        if declared.get(key) is not True:
            out.append(f"RT25-CENSUS $.leafCensus.{key} must be true")
    if declared.get("walkedFrom") != "WRITTEN-BYTES":
        out.append("RT25-CENSUS $.leafCensus.walkedFrom must be WRITTEN-BYTES")
    method = declared.get("method", "")
    if "bool is tested BEFORE int" not in method:
        out.append("RT25-CENSUS $.leafCensus.method must state that bool is tested "
                   "before int; testing int first classifies every boolean as an "
                   "integer, which is the same class law 18 exists to prevent")
    # the three deliberate wire-value spellings, checked against the RAW BYTES so a
    # re-serialisation cannot quietly normalise 200.0 to 200
    raw = (HERE / SUBJECT).read_bytes().decode("utf-8")
    if '"keepCount": 200.0' not in raw:
        out.append('RT25-CENSUS the raw bytes do not contain "keepCount": 200.0; '
                   "PC-V-07's float control must survive serialisation as a float")
    if '"keepCount": true' not in raw:
        out.append('RT25-CENSUS the raw bytes do not contain "keepCount": true; '
                   "PC-V-06's boolean control must survive as a JSON boolean")
    if '"keepCount": "200"' not in raw:
        out.append('RT25-CENSUS the raw bytes do not contain "keepCount": "200"')
    used = declared.get("booleanLeavesUsedAsWireValues") or []
    if not any(KEEPCOUNT_BOOL_PATH in u for u in used):
        out.append(f"RT25-CENSUS $.leafCensus.booleanLeavesUsedAsWireValues does not "
                   f"name {KEEPCOUNT_BOOL_PATH}")
    return out


def check_residual_measurements(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """Every residual's measuredValues, re-derived and hard-compared."""
    out: list[str] = []
    C = get_path(doc, "$.partC_retentionBounds", {})
    vectors = C.get("vectors", {})
    invariants = C.get("invariants") or []
    rows = vectors.get("rows") or []
    if vectors.get("count") != len(rows):
        out.append(f"RT25-MEASURED $.partC.vectors.count {vectors.get('count')!r} != "
                   f"{len(rows)}")
    controls = sum(1 for r in rows if r.get("isNegativeControl"))
    if vectors.get("negativeControlCount") != controls:
        out.append(f"RT25-MEASURED $.partC.vectors.negativeControlCount "
                   f"{vectors.get('negativeControlCount')!r} != {controls}")
    if vectors.get("nonControlRowCount") != len(rows) - controls:
        out.append(f"RT25-MEASURED $.partC.vectors.nonControlRowCount "
                   f"{vectors.get('nonControlRowCount')!r} != {len(rows) - controls}")
    if C.get("invariantCount") != len(invariants):
        out.append(f"RT25-MEASURED $.partC.invariantCount {C.get('invariantCount')!r} "
                   f"!= {len(invariants)}")
    ids = [i.get("id") for i in invariants]
    if len(set(ids)) != len(ids):
        out.append("RT25-MEASURED duplicate invariant ids")
    row_ids = [r.get("id") for r in rows]
    if len(set(row_ids)) != len(row_ids):
        out.append("RT25-MEASURED duplicate vector ids")

    retained = get_path(doc, "$.retainedResiduals") or []
    if get_path(doc, "$.retainedResidualCount") != len(retained):
        out.append("RT25-MEASURED $.retainedResidualCount != len(retainedResiduals)")
    new = get_path(doc, "$.newResiduals") or []
    if get_path(doc, "$.newResidualCount") != len(new):
        out.append("RT25-MEASURED $.newResidualCount != len(newResiduals)")
    deps = get_path(doc, "$.declaredDependencies") or []
    if get_path(doc, "$.declaredDependencyCount") != len(deps):
        out.append("RT25-MEASURED $.declaredDependencyCount != len(declaredDependencies)")
    dep_ids = {d.get("id") for d in deps}
    if len(dep_ids) != len(deps):
        out.append("RT25-MEASURED duplicate dependency ids")
    # every DEP- referenced anywhere must exist in the register
    referenced = set(re.findall(r"DEP-RT25-\d+", json.dumps(doc)))
    missing = sorted(referenced - dep_ids)
    if missing:
        out.append(f"RT25-MEASURED {missing} are cited as declaredAs and are not "
                   f"members of $.declaredDependencies")
    unused = sorted(dep_ids - referenced)
    if unused:
        out.append(f"RT25-MEASURED {unused} are declared and cited nowhere")

    by_id = {r.get("id"): r for r in new}
    r1 = by_id.get("RT25-RES-01", {}).get("measuredValues", {})
    for key, value in (("vectorsDeclared", len(rows)),
                       ("invariantsDeclared", len(invariants))):
        if r1.get(key) != value:
            out.append(f"RT25-MEASURED RT25-RES-01.{key}: {r1.get(key)!r} != {value}")
    # RT25-RES-01 is a statement about THIS ARTIFACT's bytes, and this instrument
    # is a different file.  The residual therefore stays literally true here and is
    # hard-compared as the recorded measurement it is.  Its DISCHARGE is reported
    # separately, because only a successor artifact can record it.
    for key in ("retainedCheckers", "vectorsExecuted", "invariantsMechanicallyChecked",
                "mutationSweepsRun"):
        if r1.get(key) != 0:
            out.append(f"RT25-MEASURED RT25-RES-01.{key} is {r1.get(key)!r}; the "
                       f"artifact retains no checker and may not claim otherwise in "
                       f"its own bytes")
    boundary = by_id.get("RT25-RES-01", {}).get("measuredBoundary", "")
    if str(len(rows)) not in boundary or str(len(invariants)) not in boundary:
        out.append("RT25-MEASURED RT25-RES-01.measuredBoundary does not carry the "
                   "measured vector and invariant counts")
    r5 = by_id.get("RT25-RES-05", {}).get("measuredValues", {})
    cells = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                 "askDecisionTable.cells", []) or []
    outcomes = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                    "interactionOutcomes.outcomes", []) or []
    changed_cells = [c for c in cells if c.get("policyPresence") == "ABSENT"
                     and c.get("requestedCustody") == "DURABLE_AUTHORITATIVE"]
    changed_out = [o for o in outcomes
                   if o.get("terminatesTheRequest") and not o.get("policyPersisted")]
    for key, value in (("decisionTableCells", len(cells)),
                       ("cellsFoundChanged", len(changed_cells)),
                       ("interactionOutcomes", len(outcomes)),
                       ("outcomesFoundChanged", len(changed_out)),
                       ("partASurfacesSearchedByInstrument", 0)):
        if r5.get(key) != value:
            out.append(f"RT25-MEASURED RT25-RES-05.{key}: {r5.get(key)!r} != {value}")
    r4 = by_id.get("RT25-RES-04", {}).get("measuredValues", {})
    spe = get_path(doc, "$.shippingProductEvidence", {})
    for key, value in (("productClaimsRecorded", len(spe.get("departed") or [])),
                       ("adoptionsWithAnIndependentCorpusJustification",
                        len(spe.get("adopted") or [])),
                       ("productClaimsReMeasuredHere", 0),
                       ("adoptionsRestingOnlyOnProductEvidence", 0)):
        if r4.get(key) != value:
            out.append(f"RT25-MEASURED RT25-RES-04.{key}: {r4.get(key)!r} != {value}")
    if spe.get("reRunByThisArtifact") is not False:
        out.append("RT25-MEASURED $.shippingProductEvidence.reRunByThisArtifact "
                   "must be false")
    # every controlledBy id must name a real vector
    for departed in spe.get("departed") or []:
        for vid in departed.get("controlledBy") or []:
            if vid not in row_ids:
                out.append(f"RT25-MEASURED $.shippingProductEvidence departure "
                           f"controlledBy {vid!r}, which is not a vector row")
    corpus = {c.get("id"): c for c in get_path(doc, "$.corpusResiduals") or []}
    c1 = corpus.get("RT25-RES-CORPUS-01", {}).get("measuredValues", {})
    recorded = get_path(doc, "$.recordedInputs.recorded") or []
    for key, value in (("recordedInputs", len(recorded)), ("inputsActuallyGated", 0),
                       ("independentReviewsOfThisArtifact", 0),
                       ("retainedCheckers", 0), ("predecessorRetainedCheckers", 1)):
        if c1.get(key) != value:
            out.append(f"RT25-MEASURED RT25-RES-CORPUS-01.{key}: {c1.get(key)!r} != "
                       f"{value}")
    c3 = corpus.get("RT25-RES-CORPUS-03", {}).get("measuredValues", {})
    changed_surfaces = get_path(doc, "$.inheritance.surfacesThisArtifactChanges") or []
    part_b_changed = [s for s in changed_surfaces
                      if str(s.get("surface", "")).startswith("$.partB_")]
    if c3.get("partBSurfacesProposedForChange") != len(part_b_changed):
        out.append(f"RT25-MEASURED RT25-RES-CORPUS-03.partBSurfacesProposedForChange: "
                   f"{c3.get('partBSurfacesProposedForChange')!r} != "
                   f"{len(part_b_changed)}")
    unchanged_surfaces = get_path(
        doc, "$.inheritance.surfacesThisArtifactDoesNotChange") or []
    if c3.get("partBSurfacesLeftUnchanged") != len(unchanged_surfaces):
        out.append(f"RT25-MEASURED RT25-RES-CORPUS-03.partBSurfacesLeftUnchanged: "
                   f"{c3.get('partBSurfacesLeftUnchanged')!r} != "
                   f"{len(unchanged_surfaces)}")
    c4 = corpus.get("RT25-RES-CORPUS-04", {}).get("measuredValues", {})
    clauses = get_path(doc, "$.recordedProductIntent.clauses") or []
    for key, value in (("intentClausesRecorded", len(clauses)),
                       ("intentClausesConstitutedAsDecisions", 0),
                       ("productPacketAmendments", 0), ("amendmentDraftsApplied", 0),
                       ("architecturalRecommendationsOverridden", 1)):
        if c4.get(key) != value:
            out.append(f"RT25-MEASURED RT25-RES-CORPUS-04.{key}: {c4.get(key)!r} != "
                       f"{value}")
    # every residual must carry a number that is bound to something
    for residual in new + list(corpus.values()):
        boundary = residual.get("measuredBoundary", "")
        if boundary and not re.search(r"\d", boundary):
            out.append(f"RT25-MEASURED {residual.get('id')}.measuredBoundary carries "
                       f"no number; an unquantified boundary is prose")
        if not residual.get("measuredValues"):
            out.append(f"RT25-MEASURED {residual.get('id')} has no measuredValues")
    return out


def check_separability(doc: Any, _ctx: dict[str, Any]) -> list[str]:
    out: list[str] = []
    sep = get_path(doc, "$.separability", {})
    prefixes = {"partCInvariantPrefix": "RT25-C-INV-",
                "partDInvariantPrefix": "RT25-D-INV-",
                "partCFixturePrefix": "PC-V-", "residualPrefix": "RT25-RES-",
                "dependencyPrefix": "DEP-RT25-"}
    for key, value in prefixes.items():
        if sep.get(key) != value:
            out.append(f"RT25-SEP $.separability.{key}: {sep.get(key)!r} != {value!r}")
    invariants = [i.get("id") for i in
                  get_path(doc, "$.partC_retentionBounds.invariants") or []]
    for inv_id in invariants:
        if not (inv_id.startswith(sep.get("partCInvariantPrefix", "\0"))
                or inv_id.startswith(sep.get("partDInvariantPrefix", "\0"))):
            out.append(f"RT25-SEP invariant {inv_id!r} carries neither declared prefix")
    for row in get_path(doc, "$.partC_retentionBounds.vectors.rows") or []:
        if not str(row.get("id")).startswith(sep.get("partCFixturePrefix", "\0")):
            out.append(f"RT25-SEP vector {row.get('id')!r} does not carry the "
                       f"declared fixture prefix")
    if sep.get("partCDependsOnPartD") is not False:
        out.append("RT25-SEP $.separability.partCDependsOnPartD must be false")
    if sep.get("partAPrimeDependsOnPartD") is not True:
        out.append("RT25-SEP $.separability.partAPrimeDependsOnPartD must be true")
    # Part C must be executable with the Part D surfaces removed, or the declared
    # independence is a sentence rather than a property.
    order = eviction_order(population(5, 500))
    try:
        eviction_count((0, 100, 2), order)
        admit_bounds(bounds_record(0, 100, 2))
        attribute_causes((0, 100, 2), order)
    except Exception as exc:                                       # noqa: BLE001
        out.append(f"RT25-SEP the Part C derivations did not run independently of "
                   f"Part D ({type(exc).__name__}: {exc})")
    return out


def check_draft(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """Semantic floor over the LIVE amendment-draft bytes.

    Reached only under --allow-unsatisfiable-pin, and only after
    RT25-PIN-UNSATISFIABLE has already been reported.  It gates the design input
    that survives the edit, and it hard-compares the COUNT and the PATHS of the
    v25 claims whose subject bytes no longer exist.
    """
    out: list[str] = []
    draft = ctx.get("draft")
    if draft is None:
        return out
    for path, expected in DRAFT_ANCHORS:
        got = get_path(draft, path, "__MISSING__")
        if got != expected:
            out.append(f"RT25-DRAFT {path}: live draft has {got!r}, v25 designs "
                       f"against {expected!r}")
    block = get_path(doc, "$.productAuthorityBoundary.amendmentDraft", {})
    if block.get("state") != "DRAFT-NOT-APPLIED":
        out.append("RT25-DRAFT $.productAuthorityBoundary.amendmentDraft.state drifted")
    would = block.get("whatItWouldDoIfApplied", "")
    target = get_path(draft, "$.target.path", "") or get_path(draft, "$.target", "")
    if isinstance(target, str) and target and "CD-RT-5" not in would:
        out.append("RT25-DRAFT whatItWouldDoIfApplied does not name CD-RT-5")
    observations = get_path(
        doc, "$.productAuthorityBoundary.amendmentDraft."
             "twoInternalStalenessObservations.observations") or []
    if len(observations) != len(UNVERIFIABLE_DRAFT_CLAIM_PATHS):
        out.append(
            f"RT25-DRAFT $.productAuthorityBoundary.amendmentDraft."
            f"twoInternalStalenessObservations.observations carries "
            f"{len(observations)} entries; this instrument classifies exactly "
            f"{len(UNVERIFIABLE_DRAFT_CLAIM_PATHS)} as UNVERIFIABLE because their "
            f"subject bytes no longer exist. A third claim about those bytes is a "
            f"new unverifiable position and must be enumerated, not absorbed.")
    return out


def check_answered_questions(doc: Any, _ctx: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for question in get_path(doc, "$.answeredQuestions") or []:
        where = question.get("answeredAt", "")
        primary = where.split(" and ")[0].strip()
        if primary.startswith("$.") and \
                get_path(doc, primary, "__MISSING__") == "__MISSING__":
            out.append(f"RT25-ANSWER question {question.get('n')} answeredAt "
                       f"{primary!r} does not resolve in this artifact")
        if question.get("isOpen") is not False:
            out.append(f"RT25-ANSWER question {question.get('n')} is not closed")
    return out


# ===========================================================================
# SECTION 6 -- SELFTEST, LIMITS DISCLOSURE, AND MAIN.
# ===========================================================================

def run_all(doc: Any, ctx: dict[str, Any], part: str) -> list[str]:
    findings: list[str] = []
    type_out, _ = type_findings(doc)
    findings.extend(type_out)
    findings.extend(check_record(doc, ctx))
    findings.extend(check_authority(doc, ctx))
    findings.extend(check_inheritance(doc, ctx))
    findings.extend(check_census(doc, ctx))
    findings.extend(check_residual_measurements(doc, ctx))
    findings.extend(check_separability(doc, ctx))
    findings.extend(check_answered_questions(doc, ctx))
    findings.extend(check_draft(doc, ctx))
    findings.extend(check_surface_partition(doc, ctx))
    findings.extend(check_verbatim_fields(doc, ctx))
    if part in ("c", "all"):
        findings.extend(check_part_c_structure(doc, ctx))
        findings.extend(check_b1(doc, ctx))
        vec_out, ctx["vectorReport"] = run_vectors(doc, ctx)
        findings.extend(vec_out)
        inv_out, ctx["invariantReport"] = run_invariants(doc, ctx)
        findings.extend(inv_out)
    if part in ("d", "all"):
        findings.extend(check_part_d(doc, ctx))
    if part in ("a", "all"):
        findings.extend(check_part_a_prime(doc, ctx))
        findings.extend(check_rule_field_closure(doc, ctx))
    return findings


# The finding id each mutation ASSERTS.  Every case names the check that must
# catch it, so a mutation caught by the wrong check is a failure, not a pass.
SELFTEST_CASES: dict[str, str] = {
    "MX-01-VECTOR-EXPECTATION-MOVED": "RT25-VEC",
    "MX-02-VECTOR-CAUSE-MOVED": "RT25-VEC",
    "MX-03-VECTOR-DELETED": "RT25-VEC",
    "MX-04-CONTROL-DEMOTED-TO-NON-CONTROL": "RT25-MEASURED",
    "MX-05-FLOAT-CONTROL-RESPELLED-AS-INT": "RT25-TYPE",
    "MX-06-BOOL-CONTROL-RESPELLED-AS-INT": "RT25-TYPE",
    "MX-07-STRING-CONTROL-RESPELLED-AS-INT": "RT25-TYPE",
    "MX-08-AGE-CONTROL-VALUE-MOVED": "RT25-VEC",
    "MX-09-EXPECTED-ADMISSION-FLIPPED": "RT25-VEC",
    "MX-10-EXPECTED-ERROR-CODE-INVENTED": "RT25-VEC",
    "MX-11-CAUSE-BLINDNESS-EXPECTATION-FLIPPED": "RT25-VEC",
    "MX-12-ANCHOR-CAPABILITY-MOVED": "RT25-VEC",
    "MX-13-POSTURE-ROW-INVERTED": "RT25-D",
    "MX-14-PROVENANCE-ROW-INVERTED": "RT25-D",
    "MX-15-BOUNDS-RESOLUTION-ROW-MOVED": "RT25-D",
    "MX-16-POSTURE-ENUM-GAINS-A-MEMBER": "RT25-D-INV-05",
    "MX-17-POSTURE-ENUM-GAINS-ABSENT": "RT25-D-INV-05",
    "MX-18-POSTURE-FORBIDDEN-FIELD-DROPPED": "RT25-D-INV-05",
    "MX-19-INVARIANT-DELETED": "RT25-INV",
    "MX-20-INVARIANT-ID-RENAMED": "RT25-INV",
    "MX-21-INVARIANT-COUNT-DRIFT": "RT25-MEASURED",
    "MX-22-VECTOR-COUNT-DRIFT": "RT25-MEASURED",
    "MX-23-CENSUS-SCALAR-DRIFT": "RT25-CENSUS",
    "MX-24-CENSUS-BOOL-DRIFT": "RT25-CENSUS",
    "MX-25-CENSUS-FLOAT-PATH-FABRICATED": "RT25-CENSUS",
    "MX-26-CENSUS-NULL-CLAIM-FABRICATED": "RT25-CENSUS",
    "MX-27-CENSUS-METHOD-REORDERED": "RT25-CENSUS",
    "MX-28-CENSUS-WALK-SOURCE-MOVED": "RT25-CENSUS",
    "MX-29-D9-DEFICIENCY-COUNT-DRIFT": "RT25-C-INV-14",
    "MX-30-D9-ERROR-COUNT-DRIFT": "RT25-C-INV-14",
    "MX-31-D9-GAP-CLOSED-BY-FIAT": "RT25-C-INV-14",
    "MX-32-D9-TOKEN-PREDICATE-GUTTED": "RT25-C-INV-14",
    "MX-33-D9-CODE-CLAIMED-ADDED": "RT25-C-INV-14",
    "MX-34-D9-DIGEST-DRIFT": "RT25-C-INV-14",
    "MX-35-FORBIDDEN-INPUTS-COUNT-DRIFT": "RT25-INHERIT",
    "MX-36-MUTATION-BOUNDARY-COUNT-DRIFT": "RT25-INHERIT",
    "MX-37-LEDGER-FIELD-COUNT-DRIFT": "RT25-INHERIT",
    "MX-38-CAUSE-POSITION-MOVED": "RT25-INHERIT",
    "MX-39-CAUSE-DECLARED-NEW": "RT25-INHERIT",
    "MX-40-PREDECESSOR-DIGEST-DRIFT": "RT25-INHERIT",
    "MX-41-REVIEW-DIGEST-DRIFT": "RT25-INHERIT",
    "MX-42-REVIEW-BLOCKER-COUNT-FALSIFIED": "RT25-INHERIT",
    "MX-43-CHANGED-SURFACE-ALSO-UNCHANGED": "RT25-INHERIT",
    "MX-44-SURFACE-DOES-NOT-RESOLVE": "RT25-INHERIT",
    "MX-45-CELL-COUNT-DRIFT": "RT25-A'",
    "MX-46-CHANGED-CELL-SET-FALSIFIED": "RT25-A'",
    "MX-47-D9-BEFORE-FALSIFIED": "RT25-A'",
    "MX-48-D9-AFTER-SENTINEL-AUTHORED": "RT25-A'",
    "MX-49-OUTCOME-COUNT-DRIFT": "RT25-A'",
    "MX-50-CHANGED-OUTCOME-SET-FALSIFIED": "RT25-A'",
    "MX-51-D9-RECOMPUTATION-CLAIMED": "RT25-A'",
    "MX-52-NOASK-CASE-DELETED": "RT25-A'",
    "MX-53-NOASK-QUOTATION-FABRICATED": "RT25-A'",
    "MX-54-SEAL-RECOMMENDATION-FLIPPED": "RT25-AUTH",
    "MX-55-STATUS-PROMOTED": "RT25-AUTH",
    "MX-56-CD-RT-5-MARKED-RESOLVED": "RT25-AUTH",
    "MX-57-DURABLE-DEFAULT-SELECTED": "RT25-AUTH",
    "MX-58-AMENDMENT-DECLARED-APPLIED": "RT25-AUTH",
    "MX-59-FREEZE-BECOMES-A-SEAL": "RT25-AUTH",
    "MX-60-RETAINED-CHECKER-CLAIMED": "RT25-AUTH",
    "MX-61-V10-DISCHARGE-CLAIMED": "RT25-AUTH",
    "MX-62-RECOMMENDATION-QUOTE-FABRICATED": "RT25-AUTH",
    "MX-63-PACKET-STATE-MISREPORTED": "RT25-AUTH",
    "MX-64-RECORDED-DIGEST-DRIFT": "RT25-RECORD",
    "MX-65-RECORDED-COUNT-DRIFT": "RT25-RECORD",
    "MX-66-GATE-DOWNGRADED": "RT25-RECORD",
    "MX-67-DUPLICATE-KEY-CLAIM-FALSIFIED": "RT25-RECORD",
    "MX-68-RES-01-CLAIMS-EXECUTION": "RT25-MEASURED",
    "MX-69-RES-01-BOUNDARY-STRIPPED-OF-NUMBERS": "RT25-MEASURED",
    "MX-70-RES-05-MEASUREMENT-FALSIFIED": "RT25-MEASURED",
    "MX-71-CORPUS-01-GATED-COUNT-FALSIFIED": "RT25-MEASURED",
    "MX-72-DEPENDENCY-CITED-BUT-UNDECLARED": "RT25-MEASURED",
    "MX-73-DEPENDENCY-COUNT-DRIFT": "RT25-MEASURED",
    "MX-74-SEPARABILITY-PREFIX-MOVED": "RT25-SEP",
    "MX-75-PART-C-DECLARED-DEPENDENT": "RT25-SEP",
    "MX-76-CAUSE-PARTITION-GAINS-A-MEMBER": "RT25-C",
    "MX-77-CAUSE-PARTITION-COUNT-DRIFT": "RT25-C",
    "MX-78-TIEBREAK-ORDER-REVERSED": "RT25-C",
    "MX-79-COMPOSITION-BECOMES-A-SUM": "RT25-C",
    "MX-80-DISABLE-SEMANTICS-DROPPED": "RT25-C",
    "MX-81-BOUNDS-FIELD-ADDED": "RT25-C",
    "MX-82-IDENTITY-FIELD-COUNT-DRIFT": "RT25-C",
    "MX-83-IDENTITY-EXCLUSION-VIOLATED": "RT25-C",
    "MX-84-CONFIG-INVALID-CODE-INVENTED": "RT25-C",
    "MX-85-OVER-BOUND-RECORDS-A-NEW-TYPE": "RT25-C",
    "MX-86-SCOPE-BECOMES-GLOBAL": "RT25-C",
    "MX-87-ANSWERED-QUESTION-REOPENED": "RT25-ANSWER",
    "MX-88-ANSWER-POINTER-DANGLES": "RT25-ANSWER",
    "MX-89-INT-LEAF-RESPELLED-AS-BOOL": "RT25-TYPE",
    "MX-90-BOOL-LEAF-RESPELLED-AS-INT": "RT25-TYPE",
    "MX-91-UNRULED-INT-LEAF-INTRODUCED": "RT25-TYPE",
    "MX-92-NULL-LEAF-INTRODUCED": "RT25-TYPE",
    # Added after an independent review found B2, B3 and B4 uncovered.  Each
    # family already fires on the base, so these must produce a NEW finding --
    # the delta discipline means a driver that merely restates its base finding
    # counts as an escape.
    "MX-93-GENERATOR-EXCEPTION-DROPPED": "RT25-B2",
    "MX-94-UNCHANGED-SURFACE-LIST-EMPTIED": "RT25-B3",
    "MX-95-VERBATIM-FIELD-FABRICATED": "RT25-B4",
    "MX-96-VERBATIM-FIELD-EMPTIED": "RT25-B4",
}


def _mut(doc: Any, path: str, value: Any) -> Any:
    out = copy.deepcopy(doc)
    set_path(out, path, value)
    return out


def _del(doc: Any, path: str) -> Any:
    out = copy.deepcopy(doc)
    del_path(out, path)
    return out


def selftest(doc: Any, ctx: dict[str, Any]) -> tuple[list[str], int, int, list[str]]:
    """Returns (failures, cases, caught, escapes).

    Each mutation must produce a finding carrying the id named for it AND not
    present in the base.  A mutation caught only by a different family counts as
    an escape for its own family and is reported as one.
    """
    failures: list[str] = []
    cases: list[tuple[str, Any, str]] = []
    V = "$.partC_retentionBounds.vectors"
    C = "$.partC_retentionBounds"
    A = "$.partA_repairsForcedByThePostureDecision"

    def add(name: str, mutated: Any) -> None:
        cases.append((name, mutated, SELFTEST_CASES[name]))

    rows = get_path(doc, f"{V}.rows")
    index = {r["id"]: i for i, r in enumerate(rows)}
    i01 = index["PC-V-01-COUNT-ONLY"]
    i02 = index["PC-V-02-PARASITISM-CONTROL-KEEP-ZERO"]
    i06 = index["PC-V-06-EXACT-TYPE-BOOL"]
    i07 = index["PC-V-07-EXACT-TYPE-FLOAT"]
    i08 = index["PC-V-08-EXACT-TYPE-NUMERIC-STRING"]
    i09 = index["PC-V-09-UNSATISFIABLE-AGE-BOUND"]
    i11 = index["PC-V-11-CAUSE-BLINDNESS-WITHIN-PURGED"]

    add("MX-01-VECTOR-EXPECTATION-MOVED",
        _mut(doc, f"{V}.rows[{i01}].expectedEvictionCount", 4))
    add("MX-02-VECTOR-CAUSE-MOVED",
        _mut(doc, f"{V}.rows[{i01}].expectedCauses", ["RETENTION_USER_REQUEST"]))
    add("MX-03-VECTOR-DELETED", _del(doc, f"{V}.rows[{i02}]"))
    add("MX-04-CONTROL-DEMOTED-TO-NON-CONTROL",
        _mut(doc, f"{V}.rows[{i02}].isNegativeControl", False))
    add("MX-05-FLOAT-CONTROL-RESPELLED-AS-INT",
        _mut(doc, f"{V}.rows[{i07}].bounds.keepCount", 200))
    add("MX-06-BOOL-CONTROL-RESPELLED-AS-INT",
        _mut(doc, f"{V}.rows[{i06}].bounds.keepCount", 1))
    add("MX-07-STRING-CONTROL-RESPELLED-AS-INT",
        _mut(doc, f"{V}.rows[{i08}].bounds.keepCount", 200))
    add("MX-08-AGE-CONTROL-VALUE-MOVED",
        _mut(doc, f"{V}.rows[{i09}].bounds.maxAgeSeconds", 5184001))
    add("MX-09-EXPECTED-ADMISSION-FLIPPED",
        _mut(doc, f"{V}.rows[{i09}].expectedAdmission", "ADMITTED"))
    add("MX-10-EXPECTED-ERROR-CODE-INVENTED",
        _mut(doc, f"{V}.rows[{i09}].expectedErrorCode", "RETENTION.BOUND_INVALID"))
    add("MX-11-CAUSE-BLINDNESS-EXPECTATION-FLIPPED",
        _mut(doc, f"{V}.rows[{i11}].expectedEqual", False))
    add("MX-12-ANCHOR-CAPABILITY-MOVED",
        _mut(doc, f"{V}.rows[{i11}].expectedEffectiveCapabilityA", "replayable"))
    add("MX-13-POSTURE-ROW-INVERTED",
        _mut(doc, "$.postureResolution.theDerivation.rows[0].posture",
             "EPHEMERAL_ONLY"))
    add("MX-14-PROVENANCE-ROW-INVERTED",
        _mut(doc, "$.postureResolution.theDerivation.rows[0].provenance", "CONSENTED"))
    add("MX-15-BOUNDS-RESOLUTION-ROW-MOVED",
        _mut(doc, f"{C}.boundsRecord.effectiveBoundsResolution.rows[0].values",
             "200 / 157286400 / 5184000"))
    add("MX-16-POSTURE-ENUM-GAINS-A-MEMBER",
        _mut(doc, "$.postureResolution.theDerivation.postureEnum",
             ["DURABLE_RETAINED", "EPHEMERAL_ONLY", "DURABLE_BOUNDED"]))
    add("MX-17-POSTURE-ENUM-GAINS-ABSENT",
        _mut(doc, "$.postureResolution.theDerivation.postureEnum",
             ["DURABLE_RETAINED", "EPHEMERAL_ONLY", "ABSENT"]))
    add("MX-18-POSTURE-FORBIDDEN-FIELD-DROPPED",
        _mut(doc, f"{C}.boundsRecord.forbiddenFields",
             [f for f in get_path(doc, f"{C}.boundsRecord.forbiddenFields")
              if f != "posture"]))
    add("MX-19-INVARIANT-DELETED", _del(doc, f"{C}.invariants[4]"))
    add("MX-20-INVARIANT-ID-RENAMED",
        _mut(doc, f"{C}.invariants[4].id", "RT25-C-INV-99"))
    add("MX-21-INVARIANT-COUNT-DRIFT", _mut(doc, f"{C}.invariantCount", 18))
    add("MX-22-VECTOR-COUNT-DRIFT", _mut(doc, f"{V}.count", 15))
    add("MX-23-CENSUS-SCALAR-DRIFT", _mut(doc, "$.leafCensus.scalarLeafPositions", 1417))
    add("MX-24-CENSUS-BOOL-DRIFT", _mut(doc, "$.leafCensus.boolLeafPositions", 183))
    add("MX-25-CENSUS-FLOAT-PATH-FABRICATED",
        _mut(doc, "$.leafCensus.floatLeafPaths", ["$.partC_retentionBounds.nowhere"]))
    add("MX-26-CENSUS-NULL-CLAIM-FABRICATED",
        _mut(doc, "$.leafCensus.nullLeafPaths", ["$.leafCensus.nullLeafPaths[0]"]))
    add("MX-27-CENSUS-METHOD-REORDERED",
        _mut(doc, "$.leafCensus.method",
             "a recursive walk descending dicts and lists. int is tested before bool."))
    add("MX-28-CENSUS-WALK-SOURCE-MOVED",
        _mut(doc, "$.leafCensus.walkedFrom", "IN-MEMORY-OBJECT"))
    D9 = f"{C}.d9ReasonCodePosition.measuredLiveFromPinnedD9Bytes"
    add("MX-29-D9-DEFICIENCY-COUNT-DRIFT", _mut(doc, f"{D9}.deficiencyMemberCount", 10))
    add("MX-30-D9-ERROR-COUNT-DRIFT", _mut(doc, f"{D9}.errorCodeCount", 20))
    add("MX-31-D9-GAP-CLOSED-BY-FIAT",
        _mut(doc, f"{D9}.reasonCodesMatchingPredicate", 1))
    add("MX-32-D9-TOKEN-PREDICATE-GUTTED",
        _mut(doc, f"{D9}.retentionTokenPredicate", []))
    add("MX-33-D9-CODE-CLAIMED-ADDED",
        _mut(doc, f"{C}.d9ReasonCodePosition.requestedSuccessorNotAdded"
                  f".codesAddedByThisArtifact", 1))
    add("MX-34-D9-DIGEST-DRIFT", _mut(doc, f"{D9}.sha256", "0" * 64))
    MD = f"{C}.whyThisIsSmallerThanItLooks.measuredDeltas"
    add("MX-35-FORBIDDEN-INPUTS-COUNT-DRIFT",
        _mut(doc, f"{MD}.effectiveCapabilityForbiddenInputsBefore", 12))
    add("MX-36-MUTATION-BOUNDARY-COUNT-DRIFT",
        _mut(doc, f"{MD}.purgeDoesNotMutateBefore", 15))
    add("MX-37-LEDGER-FIELD-COUNT-DRIFT",
        _mut(doc, f"{MD}.ledgerEntryOrderedFieldsBefore", 8))
    add("MX-38-CAUSE-POSITION-MOVED",
        _mut(doc, f"{C}.causeVocabulary.orderedPosition", 6))
    add("MX-39-CAUSE-DECLARED-NEW",
        _mut(doc, f"{C}.causeVocabulary.fieldIsNotNew", False))
    add("MX-40-PREDECESSOR-DIGEST-DRIFT",
        _mut(doc, "$.inheritance.predecessor.sha256", "0" * 64))
    add("MX-41-REVIEW-DIGEST-DRIFT",
        _mut(doc, "$.inheritance.predecessorReview.sha256", "1" * 64))
    add("MX-42-REVIEW-BLOCKER-COUNT-FALSIFIED",
        _mut(doc, "$.inheritance.predecessorReview.totalBlockingFindingCount", 3))
    add("MX-43-CHANGED-SURFACE-ALSO-UNCHANGED",
        _mut(doc, "$.inheritance.surfacesThisArtifactDoesNotChange",
             get_path(doc, "$.inheritance.surfacesThisArtifactDoesNotChange")
             + [get_path(doc, "$.inheritance.surfacesThisArtifactChanges[6].surface")]))
    add("MX-44-SURFACE-DOES-NOT-RESOLVE",
        _mut(doc, "$.inheritance.surfacesThisArtifactChanges[0].surface",
             "$.partA_firstRunRetentionConsent.policyObject.noSuchField"))
    add("MX-45-CELL-COUNT-DRIFT", _mut(doc, f"{A}.askDecisionTable.cellCount", 11))
    add("MX-46-CHANGED-CELL-SET-FALSIFIED",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].policyPresence",
             "PRESENT-DURABLE_RETAINED"))
    add("MX-47-D9-BEFORE-FALSIFIED",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].d9Before.derivedExitCode", 1))
    add("MX-48-D9-AFTER-SENTINEL-AUTHORED",
        _mut(doc, f"{A}.askDecisionTable.changedCells[0].d9After.derivedClass",
             "retention-degraded"))
    add("MX-49-OUTCOME-COUNT-DRIFT", _mut(doc, f"{A}.interactionOutcomes.count", 6))
    add("MX-50-CHANGED-OUTCOME-SET-FALSIFIED",
        _mut(doc, f"{A}.interactionOutcomes.changed[0].id",
             "PA-INT-01-ANSWERED-RETAIN"))
    add("MX-51-D9-RECOMPUTATION-CLAIMED",
        _mut(doc, f"{A}.interactionOutcomes.d9DerivationsAreNotRecomputedHere"
                  f".outcomesRecomputedHere", 4))
    add("MX-52-NOASK-CASE-DELETED", _del(doc, f"{A}.noAskCasesReDerived[2]"))
    add("MX-53-NOASK-QUOTATION-FABRICATED",
        _mut(doc, f"{A}.noAskCasesReDerived[0].predecessorDecisionVerbatim",
             "CI prompts, writes a policy and infers one when absent."))
    add("MX-54-SEAL-RECOMMENDATION-FLIPPED", _mut(doc, "$.sealRecommendation", "SEAL"))
    add("MX-55-STATUS-PROMOTED", _mut(doc, "$.status", "APPLIED/ACCEPTED"))
    add("MX-56-CD-RT-5-MARKED-RESOLVED",
        _mut(doc, "$.integrationState.CD-RT-5", "RESOLVED"))
    add("MX-57-DURABLE-DEFAULT-SELECTED",
        _mut(doc, "$.productAuthorityBoundary.durableDefault", "DURABLE_RETAINED"))
    add("MX-58-AMENDMENT-DECLARED-APPLIED",
        _mut(doc, "$.authority.mayApplyTheCdRt5AmendmentDraft", True))
    add("MX-59-FREEZE-BECOMES-A-SEAL",
        _mut(doc, "$.freezeDeclaration.constitutesASealOrSignature", True))
    add("MX-60-RETAINED-CHECKER-CLAIMED",
        _mut(doc, "$.retainedChecker", "check-retention-custody-v25.py"))
    add("MX-61-V10-DISCHARGE-CLAIMED",
        _mut(doc, "$.v10Item3Position.claimedStatusForTheseBytes", "DISCHARGED"))
    add("MX-62-RECOMMENDATION-QUOTE-FABRICATED",
        _mut(doc, "$.overriddenArchitecturalRecommendation.theRecommendation"
                  ".recommendationVerbatim",
             "durable retention is the recommended default"))
    add("MX-63-PACKET-STATE-MISREPORTED",
        _mut(doc, "$.productAuthorityBoundary.packetStateAsMeasured", "DECIDED"))
    add("MX-64-RECORDED-DIGEST-DRIFT",
        _mut(doc, "$.recordedInputs.recorded[0].sha256", "2" * 64))
    add("MX-65-RECORDED-COUNT-DRIFT",
        _mut(doc, "$.recordedInputs.digestsRecordedCount", 14))
    add("MX-66-GATE-DOWNGRADED",
        _mut(doc, "$.recordedInputs.recorded[0].gate", "CITED-DIGEST-RECORDED-NOT-GATED"))
    add("MX-67-DUPLICATE-KEY-CLAIM-FALSIFIED",
        _mut(doc, "$.recordedInputs.duplicateKeysFound", 2))
    add("MX-68-RES-01-CLAIMS-EXECUTION",
        _mut(doc, "$.newResiduals[0].measuredValues.vectorsExecuted", 16))
    add("MX-69-RES-01-BOUNDARY-STRIPPED-OF-NUMBERS",
        _mut(doc, "$.newResiduals[0].measuredBoundary",
             "a number of vectors and invariants are not exercised by any instrument"))
    add("MX-70-RES-05-MEASUREMENT-FALSIFIED",
        _mut(doc, "$.newResiduals[4].measuredValues.cellsFoundChanged", 3))
    add("MX-71-CORPUS-01-GATED-COUNT-FALSIFIED",
        _mut(doc, "$.corpusResiduals[0].measuredValues.inputsActuallyGated", 15))
    add("MX-72-DEPENDENCY-CITED-BUT-UNDECLARED",
        _mut(doc, f"{C}.sweep.scope.declaredAs", "DEP-RT25-99"))
    add("MX-73-DEPENDENCY-COUNT-DRIFT", _mut(doc, "$.declaredDependencyCount", 9))
    add("MX-74-SEPARABILITY-PREFIX-MOVED",
        _mut(doc, "$.separability.partCFixturePrefix", "PCV-"))
    add("MX-75-PART-C-DECLARED-DEPENDENT",
        _mut(doc, "$.separability.partCDependsOnPartD", True))
    add("MX-76-CAUSE-PARTITION-GAINS-A-MEMBER",
        _mut(doc, f"{C}.causeVocabulary.closedPartitions[0].members",
             list(CAUSE_PARTITION) + ["RETENTION_POSTURE_CHANGE"]))
    add("MX-77-CAUSE-PARTITION-COUNT-DRIFT",
        _mut(doc, f"{C}.causeVocabulary.closedPartitions[0].memberCount", 5))
    add("MX-78-TIEBREAK-ORDER-REVERSED",
        _mut(doc, f"{C}.causeVocabulary.closedPartitions[0]"
                  f".attributionRuleWhenSeveralDemandsCover.rule",
             "when more than one demand covers the same record, ties break in the "
             "fixed order RETENTION_COUNT_BOUND, RETENTION_SIZE_BOUND, "
             "RETENTION_AGE_BOUND"))
    add("MX-79-COMPOSITION-BECOMES-A-SUM",
        _mut(doc, f"{C}.sweep.demands.composition",
             "evictionCount := sum(demand_count, demand_size, demand_time)"))
    add("MX-80-DISABLE-SEMANTICS-DROPPED",
        _mut(doc, f"{C}.sweep.demands.rows[0].disabledWhen", "never"))
    add("MX-81-BOUNDS-FIELD-ADDED",
        _mut(doc, f"{C}.boundsRecord.orderedFields",
             list(BOUNDS_ORDERED_FIELDS) + ["posture"]))
    add("MX-82-IDENTITY-FIELD-COUNT-DRIFT", _mut(doc, f"{C}.identity.fieldCount", 7))
    add("MX-83-IDENTITY-EXCLUSION-VIOLATED",
        _mut(doc, f"{C}.identity.excluded",
             get_path(doc, f"{C}.identity.excluded") + ["keepCount"]))
    add("MX-84-CONFIG-INVALID-CODE-INVENTED",
        _mut(doc, f"{C}.sweep.disableSemantics.howAnInvalidConfigurationIsReported"
                  f".errorCode", "RETENTION.CONFIG_INVALID"))
    add("MX-85-OVER-BOUND-RECORDS-A-NEW-TYPE",
        _mut(doc, f"{C}.sweep.whenTheBoundCannotBeSatisfied.whatIsDoneInstead"
                  f".newRecordTypes", 1))
    add("MX-86-SCOPE-BECOMES-GLOBAL", _mut(doc, f"{C}.sweep.scope.global", True))
    add("MX-87-ANSWERED-QUESTION-REOPENED",
        _mut(doc, "$.answeredQuestions[0].isOpen", True))
    add("MX-88-ANSWER-POINTER-DANGLES",
        _mut(doc, "$.answeredQuestions[1].answeredAt",
             "$.partC_retentionBounds.sweep.nowhereAtAll"))
    add("MX-89-INT-LEAF-RESPELLED-AS-BOOL",
        _mut(doc, f"{C}.invariantCount", True))
    add("MX-90-BOOL-LEAF-RESPELLED-AS-INT",
        _mut(doc, f"{C}.sweep.isATriggerNotAGate", 1))
    add("MX-91-UNRULED-INT-LEAF-INTRODUCED",
        _mut(doc, f"{C}.sweep.demands.aBrandNewUnruledCounter", 7))
    add("MX-92-NULL-LEAF-INTRODUCED",
        _mut(doc, f"{C}.sweep.isATriggerNotAGate", None))
    add("MX-93-GENERATOR-EXCEPTION-DROPPED",
        _mut(doc, f"{A}.theOneRuleThatGeneratesAllOfIt.rule",
             "every ABSENT row now behaves exactly as the corresponding "
             "PRESENT-DURABLE_RETAINED row"))
    add("MX-94-UNCHANGED-SURFACE-LIST-EMPTIED",
        _mut(doc, "$.inheritance.surfacesThisArtifactDoesNotChange", []))
    add("MX-95-VERBATIM-FIELD-FABRICATED",
        _mut(doc, "$.inheritance.section72Position.ruleVerbatim",
             "A review verdict binds whatever the reviewer felt at the time."))
    add("MX-96-VERBATIM-FIELD-EMPTIED",
        _mut(doc, "$.postureResolution.lawFourteenPosition.lawVerbatim", "   "))

    executed = [name for name, _, _ in cases]
    if sorted(executed) != sorted(SELFTEST_CASES):
        failures.append(
            f"SELFTEST case registry mismatch; only-executed="
            f"{sorted(set(executed) - set(SELFTEST_CASES))} only-registered="
            f"{sorted(set(SELFTEST_CASES) - set(executed))}")
    if len(set(executed)) != len(executed):
        failures.append("SELFTEST duplicate case names")

    base = set(run_all(doc, ctx, "all"))
    caught = 0
    escapes: list[str] = []
    for name, mutated, finding_id in cases:
        try:
            findings = run_all(mutated, ctx, "all")
        except Exception as exc:                                    # noqa: BLE001
            failures.append(f"SELFTEST {name}: the checker raised "
                            f"{type(exc).__name__}: {exc}")
            escapes.append(name)
            continue
        new = [f for f in findings if f not in base]
        hits = [f for f in new if f.startswith(finding_id)]
        if hits:
            caught += 1
        else:
            escapes.append(name)
            others = sorted({f.split(" ")[0] for f in new})
            failures.append(
                f"SELFTEST {name}: expected a NEW {finding_id} finding; got "
                f"{len(new)} new finding(s) from families {others}")
    return failures, len(cases), caught, escapes


WHAT_THIS_CANNOT_CATCH = (
    "A prose leaf whose VALUE is false while its PATH and TYPE are unchanged. Every "
    "explanatory string in this artifact -- every `why`, `argument`, `rationale` and "
    "`statedCost` -- can be replaced with its own negation and this instrument stays "
    "silent unless the sentence carries a number bound to a measurable source.",
    "A required substring kept and a reversal appended after it. This instrument uses "
    "containment in a handful of places and containment has no negation detection; "
    "versioning-policy.v10 already published the quantified boundary for this exact "
    "technique.",
    "Whether the DESIGN is right. It measures agreement between two statements of the "
    "same rule -- the artifact's and this file's -- not the rule's truth. The same "
    "reading produced both.",
    "Whether the reference derivations in SECTION 1 model what an implementer would "
    "build. effective_posture, resolve_and_maybe_persist and ask_performed are models "
    "written from v25's own tables. They test v25's SELF-CONSISTENCY, not its "
    "correctness, and a shared misreading survives every one of them.",
    "Any D9 REFERENCE-DERIVATION defect. This instrument reads the pinned D9 "
    "vocabulary directly and never executes check-d9-v1.14.py, so it verifies "
    "membership and counts and verifies no derivation.",
    "Anything about a real store: no vector touches a real object, an unlink, an "
    "fsync or a crash. RT25-RES-03 stays open and this instrument does not narrow it.",
    "Whether the RECORDED PRODUCT INTENT is what the product owner meant. Nothing in "
    "this corpus could, and RT25-RES-CORPUS-04 says so.",
    "The two v25 claims about the CD-RT-5 amendment draft's INTERNAL STALENESS. Their "
    "subject bytes were overwritten and are unrecoverable, so they are UNVERIFIABLE "
    "rather than true or false. This instrument counts them and refuses to score them.",
    "A defect in this checker's own hand-transcribed type registry. INT_LEAF_NAMES and "
    "BOOL_LEAF_NAMES are literals; a name wrongly classified here is a wrong rule "
    "applied consistently, and `unruled == 0` cannot see it.",
    "Three of the four blockers an independent review found. B2, B3 and B4 were "
    "invisible to this instrument until the review named them, and SECTION 7 was "
    "written from the review's METHOD afterwards. There is no reason to believe a "
    "fifth class does not exist for the same reason: this file and the artifact "
    "were read by minds close enough to share a blind spot, and the measured rate "
    "at which that happened here is 3 of 4.",
    "An inherited misquotation in any field NOT named `*Verbatim`. RT25-B4 sweeps "
    "leaves whose NAME ends in Verbatim; a quotation asserted in prose, or in a "
    "field called `statedVerbatimAbove` or `theRuleItself`, is not swept at all.",
)


def print_limits() -> None:
    print("check-retention-custody-v25.py -- WHAT A GREEN RUN IS NOT")
    print()
    print("  A green run is author-side evidence that this artifact says what it says")
    print("  consistently and that drift in a pinned input will be caught. It is NEVER")
    print("  evidence that the artifact is right. IMPLEMENTATION-FREEZE 7.8: these")
    print("  instruments bind structure and type; they do not bind the truth of")
    print("  content.")
    print()
    print(f"CAN I MAKE THIS CHECKER PASS ON A WRONG ARTIFACT?  YES, "
          f"{len(WHAT_THIS_CANNOT_CATCH)} WAYS FOUND:")
    for index, item in enumerate(WHAT_THIS_CANNOT_CATCH, 1):
        print(f"  {index}. {item}")
    print()
    print("  This list is examples, not the boundary. It was written by the author of")
    print("  the instrument and is bounded by the same reading that produced it.")


def main() -> int:
    argv = sys.argv[1:]
    part = "all"
    do_selftest = False
    allow_unsatisfiable = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--selftest":
            do_selftest = True
        elif arg == "--limits":
            print_limits()
            return 0
        elif arg == "--allow-unsatisfiable-pin":
            allow_unsatisfiable = True
        elif arg == "--part":
            index += 1
            if index >= len(argv) or argv[index] not in ("a", "c", "d", "all"):
                sys.stderr.write("RT25-UNSUPPORTED-INVOCATION: --part takes a, c, d "
                                 "or all\n")
                return 2
            part = argv[index]
        elif arg.startswith("--part="):
            part = arg.split("=", 1)[1]
            if part not in ("a", "c", "d", "all"):
                sys.stderr.write("RT25-UNSUPPORTED-INVOCATION: --part takes a, c, d "
                                 "or all\n")
                return 2
        else:
            sys.stderr.write(f"RT25-UNSUPPORTED-INVOCATION: unknown option {arg!r}\n")
            return 2
        index += 1

    try:
        snaps, unsatisfiable = verified_snapshots(allow_unsatisfiable)
    except PinMismatch as exc:
        for line in exc.unsatisfiable:
            sys.stderr.write(line + "\n")
        sys.stderr.write(
            f"RT25-PIN-REFUSED: the verified execution closure did not match its "
            f"pinned digests, so nothing was parsed or executed: {exc}\n")
        if exc.unsatisfiable:
            sys.stderr.write(
                "RT25-PIN-REFUSED: at least one mismatch is a KNOWN UNSATISFIABLE PIN "
                "(see above). Re-run with --allow-unsatisfiable-pin to execute the "
                "semantic body against the live bytes; that mode can never return 0.\n")
        return 2

    for line in unsatisfiable:
        print(line)

    try:
        subject_bytes = (HERE / SUBJECT).read_bytes()
    except OSError as exc:
        sys.stderr.write(f"RT25-PIN-REFUSED: cannot read {SUBJECT} "
                         f"({type(exc).__name__})\n")
        return 2
    try:
        doc = _parse(subject_bytes, SUBJECT)
        parsed = {name: _parse(data, name) for name, data in snaps.items()
                  if name.endswith(".json")}
    except PinMismatch as exc:
        sys.stderr.write(f"RT25-PIN-REFUSED: {exc}\n")
        return 2

    d9 = parsed["d9-exit-contract.v1.14.json"]
    ctx: dict[str, Any] = {
        "doc": doc, "snaps": snaps,
        "v22": parsed["retention-tiers.v22.json"],
        "v23": parsed["retention-tiers.v23.json"],
        "v23rev": parsed["retention-tiers.v23.review-independent.json"],
        "v24": parsed["retention-tiers.v24.json"],
        "v24rev": parsed["retention-tiers.v24.review-independent.json"],
        "d9": d9,
        "d9errorCodes": list(d9["codeVocabulary"]["errorCodes"]),
        "product": parsed["product-dispositions.v1.json"],
        "tm3": parsed["threat-model.v3.json"],
        "ev10": parsed["evidence.v10.json"],
        "draft": parsed.get("product-dispositions.cd-rt-5-amendment.draft.v1.json"),
        "b1": measure_b1(doc),
    }

    findings = run_all(doc, ctx, part)

    if do_selftest:
        dirty = bool(findings) or bool(unsatisfiable)
        if dirty:
            # IMPLEMENTATION-FREEZE 7.2 requires "the suite did not run" to be a
            # DISTINCT OBSERVABLE and requires a dirty base never to produce a green
            # banner.  Both hold here.  The suite is still executed, under the DELTA
            # discipline -- every mutation must produce a finding NOT PRESENT IN THE
            # BASE -- which is what makes the result meaningful over a dirty base
            # rather than meaningless.  The exit code is 3 unconditionally: this mode
            # reports a number, it does not certify anything.
            print("SELFTEST-OVER-DIRTY-BASE: the base is NOT clean, so this run "
                  "certifies nothing and cannot return 0. The suite is executed under "
                  "delta discipline and the number below is reported, not attested.")
            for line in unsatisfiable:
                print(f"  base pin: {line.split('.')[0]}")
            for finding in findings:
                print(f"  base finding: {finding[:160]}")
        failures, cases, caught, escapes = selftest(doc, ctx)
        if dirty:
            base_type, _ = type_findings(doc)
            sweep = hostile_sweep(doc, base_type)
            print(f"RETENTION-CUSTODY v25 SELFTEST (dirty base): {caught}/{cases} "
                  f"mutations caught by their own named check")
            for arm, row in sweep.items():
                if isinstance(row, dict):
                    print(f"  sweep[{arm}]: swept {row['sweptPositions']} admitted "
                          f"{row['admitted']} by-position {row['rejectedByPosition']} "
                          f"collateral {row['rejectedCollateral']}")
            if escapes:
                print(f"  escapes: {escapes}")
            for failure in failures:
                print(f"  - {failure}")
            print(f"SELFTEST-NOT-CERTIFYING ({len(findings)} base finding(s), "
                  f"{len(unsatisfiable)} unsatisfiable pin(s))")
            return 3
        base_type, _ = type_findings(doc)
        sweep = hostile_sweep(doc, base_type)
        print(f"RETENTION-CUSTODY v25 SELFTEST: {caught}/{cases} mutations caught by "
              f"their own named check")
        for arm, row in sweep.items():
            if isinstance(row, dict):
                print(f"  sweep[{arm}]: swept {row['sweptPositions']} admitted "
                      f"{row['admitted']} by-position {row['rejectedByPosition']} "
                      f"collateral {row['rejectedCollateral']}")
        if escapes:
            print(f"  escapes: {escapes}")
        if failures:
            for failure in failures:
                print(f"  - {failure}")
            print("SELFTEST-FAIL")
            return 1
        print("SELFTEST-PASS")
        return 0

    base_type, _ = type_findings(doc)
    _, counts = type_findings(doc)
    sweep = hostile_sweep(doc, base_type)
    for arm in ("float", "boolFromZeroOrOneInt", "intFromBool"):
        if sweep[arm]["admitted"]:
            findings.append(
                f"RT25-SWEEP {arm}: {sweep[arm]['admitted']} position(s) admitted a "
                f"respelled scalar: {sweep[arm]['escapes'][:5]}")
    if counts["unruledIntOrBoolLeafPositions"]:
        findings.append(
            f"RT25-SWEEP {counts['unruledIntOrBoolLeafPositions']} int/bool leaf "
            f"position(s) are outside the hand-transcribed type registry, so the "
            f"sweep does not cover them")

    b1 = ctx["b1"]
    vec = ctx.get("vectorReport", {})
    inv = ctx.get("invariantReport", {})
    print(f"RETENTION-CUSTODY v25  part={part}  pins {len(PINS)} "
          f"(unsatisfiable {len(unsatisfiable)})  scalar leaves "
          f"{counts['scalarLeafPositions']}  guarded int/bool "
          f"{counts['guardedIntOrBoolLeafPositions']}  unruled "
          f"{counts['unruledIntOrBoolLeafPositions']}")
    print(f"  vectors {vec.get('executed', 0)}/{vec.get('declared', 0)} executed, "
          f"{vec.get('controlsRun', 0)} negative controls run, "
          f"{len(vec.get('controlsVacuous') or [])} vacuous; "
          f"invariants {inv.get('executed', 0)}/{inv.get('declared', 0)} executed")
    print(f"  demand expressions: {len(b1['publishedAgree'])}/{b1['arithmeticRows']} "
          f"arithmetic vectors agree AS PUBLISHED, "
          f"{len(b1['guardedAgree'])}/{b1['arithmeticRows']} agree GUARDED; "
          f"default config 0/0/0 evicts {b1['defaultConfigAsPublished']}"
          f"/{b1['defaultConfigEvictableCount']} as published, "
          f"{b1['defaultConfigGuarded']}/{b1['defaultConfigEvictableCount']} guarded")
    print(f"  sweep float {sweep['float']['sweptPositions']}/"
          f"{sweep['float']['admitted']} admitted; bool<-0|1 "
          f"{sweep['boolFromZeroOrOneInt']['sweptPositions']}/"
          f"{sweep['boolFromZeroOrOneInt']['admitted']}; int<-bool "
          f"{sweep['intFromBool']['sweptPositions']}/"
          f"{sweep['intFromBool']['admitted']}")
    for name, recorded in RECORDED_NOT_GATED.items():
        live = measured_digest(name)
        if live != recorded:
            print(f"  RT25-RECORDED-NOT-GATED {name}: recorded {recorded[:12]}..., "
                  f"live {(live or 'MISSING')[:12]}... (v25 declares this class "
                  f"CITED-DIGEST-RECORDED-NOT-GATED; drift here is a re-baseline, "
                  f"not a finding)")
    print("  a green run is author-side evidence only; run --limits for what this "
          "instrument cannot catch")
    if findings:
        print(f"{len(findings)} finding(s) in {SUBJECT}:")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    if unsatisfiable:
        print(f"{SUBJECT}: NO FINDINGS, but {len(unsatisfiable)} pin(s) are "
              f"permanently unsatisfiable; this run cannot be green")
        return 1
    print(f"{SUBJECT}: PASS (architecture-candidate scope; CANDIDATE-NOT-APPLIED; "
          f"CD-RT-5 BLOCKED_ON_PHASE_1A; V10 UNRESOLVED)")
    return 0



# ===========================================================================
# SECTION 7 -- COVERAGE ADDED AFTER AN INDEPENDENT REVIEW FOUND IT MISSING.
#
# The independent review of retention-tiers.v25.json returned REJECT FOR REPAIR
# at 4 blockers.  This instrument, as first written, caught B1 and MISSED B2, B3
# and B4.  That is the 7.8 bound observed on this file rather than quoted: an
# instrument written from the same reading as the artifact sees what that reading
# already looked at.  The three drivers below close the measured gaps, so the
# instrument is worth more to v25's SUCCESSOR than it was to v25.
#
# Each is written from the review's stated METHOD, not from its stated ANSWER: it
# re-derives the partition, the diff and the token search rather than asserting
# the numbers the review published.  A driver that hard-coded "20 keys in neither
# list" would pass on a successor that fixed nothing.
# ===========================================================================

def check_rule_field_closure(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """B2.  The one rule that generates the whole Part A repair, RESOLVED.

    $.partA_repairsForcedByThePostureDecision.theOneRuleThatGeneratesAllOfIt says
    every ABSENT row now behaves exactly as the corresponding
    PRESENT-DURABLE_RETAINED row, with two named exceptions, and marks itself
    derivedNotEnumerated.  A rule stated that way is executable: diff v24's ABSENT
    cells against its PRESENT-DURABLE_RETAINED cells field by field, and every
    field on which they differ is a field the rule silently changes.  Any such
    field outside the named exception set is an unstated exception.
    """
    out: list[str] = []
    A = get_path(doc, "$.partA_repairsForcedByThePostureDecision", {})
    rule_block = A.get("theOneRuleThatGeneratesAllOfIt", {})
    if rule_block.get("derivedNotEnumerated") is not True:
        return out                       # the artifact no longer claims a generator
    rule = rule_block.get("rule", "")
    cells = get_path(ctx["v24"], "$.partA_firstRunRetentionConsent."
                                 "askDecisionTable.cells", []) or []

    # The exceptions the rule NAMES, derived from its own text rather than listed
    # here, so a restated rule is measured against what it now says.
    named: set[str] = set()
    if "no policy is persisted" in rule:
        named |= {"policyPersistedByThisCell"}
    if "provenance is DEFAULTED" in rule:
        named |= {"provenance"}
    # fields the artifact itself publishes as changed on the changed cells
    for changed in A.get("askDecisionTable", {}).get("changedCells") or []:
        if "outcomeBefore" in changed or "outcomeAfter" in changed:
            named.add("outcome")
        if "d9Before" in changed or "d9After" in changed:
            named |= {"d9Axes", "derivedClass", "derivedExitCode", "derivedErrorCode",
                      "derivedReasonCodes"}
        if "askStillPerformed" in changed:
            named.add("askPerformed")

    silent: dict[str, list[str]] = {}
    pairs = 0
    for profile in sorted({c["invocationProfile"] for c in cells}):
        for custody in sorted({c["requestedCustody"] for c in cells}):
            absent = next((c for c in cells if c["invocationProfile"] == profile
                           and c["policyPresence"] == "ABSENT"
                           and c["requestedCustody"] == custody), None)
            present = next((c for c in cells if c["invocationProfile"] == profile
                            and c["policyPresence"] == "PRESENT-DURABLE_RETAINED"
                            and c["requestedCustody"] == custody), None)
            if absent is None or present is None:
                continue
            pairs += 1
            differing = [k for k in absent
                         if k != "policyPresence" and absent.get(k) != present.get(k)]
            unnamed = [k for k in differing if k not in named]
            if unnamed:
                silent[f"{profile} / {custody}"] = unnamed
    if pairs == 0:
        out.append("RT25-B2 no (profile, custody) pair had both an ABSENT and a "
                   "PRESENT-DURABLE_RETAINED cell in the pinned v24 table, so the "
                   "rule cannot be resolved and derivedNotEnumerated is unchecked")
    if silent:
        detail = "; ".join(f"{pair}: {fields}" for pair, fields in sorted(silent.items()))
        out.append(
            f"RT25-B2 $.partA_repairsForcedByThePostureDecision."
            f"theOneRuleThatGeneratesAllOfIt: the rule is marked derivedNotEnumerated "
            f"and names {len(named)} exception field(s), but resolved against the "
            f"pinned v24 cells it silently changes further fields at "
            f"{len(silent)} of {pairs} (profile, custody) pairs -- {detail}. Applied "
            f"literally it produces a Part A the artifact does not describe. A "
            f"generator is only derivedNotEnumerated if its exception set is complete.")
    # The two consequences the review singled out, checked by name because they are
    # the ones that change what a user experiences.
    for field, why in (
            ("askPerformed",
             "the ask is the ONLY path by which provenance can ever become CONSENTED"),
            ("firstRunDisclosureEmitted",
             "the disclosure is what tells a user durable evidence is being written")):
        offenders = [pair for pair, fields in silent.items() if field in fields]
        if offenders:
            out.append(
                f"RT25-B2 the generating rule silently changes {field!r} at "
                f"{offenders}; {why}, so an implementer applying the artifact's own "
                f"stated generator deletes it")
    return out


def check_surface_partition(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """B3.  surfacesChangedCount is published as a measurement of a CLOSED set, and
    $.partA_repairsForcedByThePostureDecision.scope adds a blanket 'everything else
    is unchanged'.  Resolved against v24's actual key sets, the two lists must
    partition those key sets or the blanket sentence covers surfaces nobody looked
    at.  BY-REFERENCE inheritance is justified only if the delta is complete: an
    incomplete delta over an unread predecessor is worse than a copy, because the
    reader cannot notice the omission.
    """
    out: list[str] = []
    named: set[str] = set()
    for entry in get_path(doc, "$.inheritance.surfacesThisArtifactChanges") or []:
        named.add(str(entry.get("surface", "")).split(" ")[0])
    for surface in get_path(doc, "$.inheritance.surfacesThisArtifactDoesNotChange") or []:
        named.add(str(surface).split(" ")[0])

    uncovered: dict[str, list[str]] = {}
    for root in ("partA_firstRunRetentionConsent", "partB_purgeSemantics"):
        keys = list(get_path(ctx["v24"], f"${'.' + root}", {}) or {})
        missing = [k for k in sorted(keys)
                   if not any(n.startswith(f"$.{root}.{k}") for n in named)]
        if missing:
            uncovered[root] = missing
    total_keys = sum(len(get_path(ctx["v24"], f"$.{r}", {}) or {})
                     for r in ("partA_firstRunRetentionConsent", "partB_purgeSemantics"))
    total_missing = sum(len(v) for v in uncovered.values())
    if total_missing:
        out.append(
            f"RT25-B3 $.inheritance.surfacesThisArtifactChanges + "
            f"surfacesThisArtifactDoesNotChange: {total_missing} of {total_keys} "
            f"top-level Part A and Part B keys of the pinned retention-tiers.v24.json "
            f"appear in NEITHER list, while "
            f"$.partA_repairsForcedByThePostureDecision.scope asserts everything else "
            f"in Part A is inherited BY-REFERENCE and unchanged. surfacesChangedCount "
            f"is a recorded measurement of a closed partition and 7.2.2 gives it a "
            f"hard comparison. Uncovered: "
            + "; ".join(f"{root}: {keys}" for root, keys in sorted(uncovered.items())))
    # The specific instance the review demonstrated: v24's derive-never-author
    # obligation, which DEP-RT25-08 leaves unmet while the surface is listed nowhere.
    invariants = get_path(ctx["v24"],
                          "$.partA_firstRunRetentionConsent.invariants", []) or []
    derive_rule = [i for i in invariants
                   if "error code" in str(i.get("statement", "")).lower()
                   and "derived" in str(i.get("statement", "")).lower()]
    recomputed = get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                               "interactionOutcomes.d9DerivationsAreNotRecomputedHere."
                               "outcomesRecomputedHere")
    needed = get_path(doc, "$.partA_repairsForcedByThePostureDecision."
                           "interactionOutcomes.d9DerivationsAreNotRecomputedHere."
                           "outcomesNeedingRecomputation")
    if derive_rule and recomputed == 0 and needed:
        ids = [i.get("id") for i in derive_rule]
        if not any(any(str(i) in n for n in named) for i in ids):
            out.append(
                f"RT25-B3 the pinned v24 invariant(s) {ids} require every terminal "
                f"class, code and exit in Part A to be DERIVED and never authored. "
                f"This artifact leaves {needed} outcome(s) needing recomputation and "
                f"recomputes {recomputed}, so that obligation is unmet -- and the "
                f"surface appears in neither surfacesThisArtifactChanges nor "
                f"surfacesThisArtifactDoesNotChange, so a reader is told nothing "
                f"about it.")
    return out


# A Verbatim field that names its own source can be searched against THAT source
# rather than against the union.  This matters: the union search is DEFEATED when a
# misquotation is INHERITED, because the predecessor carries the same wrong text.
# Measured on these bytes -- `d9OwnRuleVerbatim` misquotes D9 and the union finds it
# in v23 and v24, which carried the same error forward.  Scoping separates
# "fabricated" from "misquoted and inherited", and only the scoped search catches
# the second.  Keys are tokens that appear in the leaf's own NAME or PATH.
VERBATIM_SOURCE_HINTS = (
    ("d9", "d9-exit-contract.v1.14.json"),
    ("predecessorReason", "retention-tiers.v24.json"),
    ("predecessorDecision", "retention-tiers.v24.json"),
    ("predecessorChoice", "retention-tiers.v24.json"),
    ("predecessorJustification", "retention-tiers.v24.json"),
    ("overallVerdict", "retention-tiers.v24.review-independent.json"),
    ("overriddenArchitecturalRecommendation", "retention-tiers.v22.json"),
    ("packetRuleWhilePending", "product-dispositions.v1.json"),
)

# A rendering of a JSON member -- `someFlag: true` -- is not a prose quotation, and
# requiring the rendered STRING to occur would report a field that is faithfully
# reproducing a key and its value.  For these, the KEY is what must exist.
_KEY_RENDERING = re.compile(r"^([A-Za-z][A-Za-z0-9_]*): (true|false|null|-?\d+|\".*\")$")


def _markdown_text(path: pathlib.Path) -> str:
    """Markdown with blockquote markers stripped.

    IMPLEMENTATION-FREEZE.md states its standing rules inside `>` blockquotes, so a
    field quoting one faithfully does not match the raw bytes.  Reporting that as a
    fabricated quotation would be a false positive of this instrument, and it was:
    $.inheritance.section72Position.ruleVerbatim quotes 7.2 exactly and was flagged
    until this function existed.
    """
    return re.sub(r"(?m)^\s*>\s?", "", path.read_text(encoding="utf-8",
                                                      errors="replace"))


def _verbatim_corpus(ctx: dict[str, Any]) -> str:
    """Whitespace-normalised concatenation of every source a Verbatim field in this
    artifact could legitimately be quoting: every pinned input plus the live
    recorded-not-gated documents."""
    parts: list[str] = []
    for data in ctx["snaps"].values():
        try:
            parts.append(data.decode("utf-8"))
        except UnicodeDecodeError:
            continue
    for name in RECORDED_NOT_GATED:
        for root in (HERE, COOP):
            path = root / name
            if path.is_file():
                parts.append(_markdown_text(path))
                break
    # JSON escaping means a quoted sentence appears in the raw bytes with \" and
    # \n; comparing against the PARSED text of each JSON input as well removes that
    # difference without weakening the search.
    for name, data in ctx["snaps"].items():
        if name.endswith(".json"):
            try:
                parts.append(json.dumps(json.loads(data.decode("utf-8")),
                                        ensure_ascii=False))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
    return _norm(" ".join(parts))


def check_verbatim_fields(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """B4.  Every field whose NAME ends in `Verbatim` asserts a claim about BYTES.

    Section 7.8 records this exact failure three times in one session and names it:
    a lane's summary is testimony about an artifact, it is not the artifact.  So
    every such field is searched for, whitespace-normalised, across the whole
    pinned closure plus the live recorded documents.  A Verbatim field whose text
    occurs in NO source is a fabricated quotation.

    Deliberately conservative: it searches the UNION of every source rather than
    the single source the field names, so a field that quotes correctly from an
    unexpected place is not reported.  A hit here is therefore strong.
    """
    out: list[str] = []
    corpus = _verbatim_corpus(ctx)
    scoped = {name: _norm(data.decode("utf-8", errors="replace"))
              for name, data in ctx["snaps"].items()}
    checked = 0
    for path, value in scalar_leaves(doc):
        name = leaf_name(path)
        if not name.endswith("Verbatim") or not isinstance(value, str):
            continue
        if not value.strip():
            out.append(f"RT25-B4 {path}: a Verbatim field is empty")
            continue
        checked += 1
        needle = _norm(value)

        rendering = _KEY_RENDERING.match(needle)
        if rendering:
            # A rendering of a JSON member: require the KEY, not the rendering.
            if f'"{rendering.group(1)}"' in corpus:
                continue
            out.append(f"RT25-B4 {path}: renders a member "
                       f"{rendering.group(1)!r} that exists in no pinned source")
            continue

        # SCOPED search first, because the union is defeated by inheritance.
        source = next((f for token, f in VERBATIM_SOURCE_HINTS
                       if token.lower() in path.lower()), None)
        if source and source in scoped and needle not in scoped[source]:
            elsewhere = needle in corpus
            out.append(
                f"RT25-B4 {path}: a field named Verbatim, whose own name attributes "
                f"it to {source}, carries text that does NOT occur in that file. "
                + (f"It DOES occur elsewhere in the pinned closure, so this is a "
                   f"misquotation that a predecessor already carried and this "
                   f"artifact inherited -- which is exactly the case a union-wide "
                   f"search cannot see. "
                   if elsewhere else "It occurs nowhere in the closure either. ")
                + f"Text: {needle[:180]!r}")
            continue

        if needle in corpus:
            continue
        # An ellipsis is an explicit signal that the quotation is partial; the
        # fragments are then each required to occur, which still fails closed on a
        # fabricated one.
        fragments = [f for f in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", needle)
                     if len(f) > 24]
        if fragments and all(f in corpus for f in fragments):
            continue
        longest = max((f for f in re.split(r"[.;]", needle) if len(f) > 24),
                      key=len, default=needle)
        out.append(
            f"RT25-B4 {path}: a field named Verbatim carries text that occurs in NO "
            f"pinned input and in none of the live recorded documents, searched "
            f"whitespace-normalised over the whole closure. A claim of verbatimness "
            f"is a claim about bytes. Unmatched fragment: {longest.strip()[:160]!r}")
    if checked == 0:
        out.append("RT25-B4 VACUOUS: no Verbatim field was found to check, so this "
                   "driver measured nothing")
    return out

if __name__ == "__main__":
    raise SystemExit(main())
