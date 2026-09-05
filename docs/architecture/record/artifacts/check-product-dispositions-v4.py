#!/usr/bin/env python3
"""Successor to check-product-dispositions-v3.py. Edits nothing; repairs three blockers.

WHY A SUCCESSOR AND NOT AN EDIT
-------------------------------
Section 7.2 forbids changing reviewed bytes in place and the sanctioned repair is
a new file. The predecessor is a RUNTIME INPUT here, hash-verified before use,
which section 7.3 explicitly permits. It in turn hash-verifies and executes ITS
predecessor, which verifies ITS predecessor, so one pin covers a four-deep
closure and every inherited detection semantic is RE-USED BYTE-IDENTICALLY
rather than retyped.

WHAT THIS SUCCESSOR CHANGES
---------------------------
An independent review of the predecessor returned ACCEPT_WITH_BLOCKERS at three
blockers and nine non-blocking findings. All three blockers are repaired here.
Nothing else is touched. In particular the standing/demotion lane, its five
review-record conjuncts, its four supersession gates and residuals R1-R5 are
CALLED, not copied, and residual R3 - one substantive key makes a successor, so
repair QUALITY is not graded - is LOAD-BEARING and is left exactly as it is,
because section 7.9 records its consequences and changing it is a semantic
change that must be argued rather than slipped into a repair scoped elsewhere.

  BLOCKER 1 - THE CORROBORATION GATE TESTED PRESENCE, NOT ATTRIBUTION.
  The predecessor asked only whether the `decidedBy` string appears as a whole
  word in some OTHER string leaf of the decision. The decided row is four
  kilobytes of prose about retention, so any word already in it satisfies the
  gate. REPRODUCED against live bytes on a green baseline: an attribution of
  'retention', 'PURGED', 'tombstone', 'bounds' or 'Phase' exits 0 with ZERO
  findings, while the controls ('sfbreens', 'SFBREEN', 'the coordinator',
  'jdoe', 'z') are correctly caught - so the gate was live and wrong rather than
  dead. An attribution naming NOBODY passed the guard whose entire reason for
  existing is section 4.4's fabricated attribution.

  AND IT MADE THE PREDECESSOR'S OWN RESIDUAL D1 WRONG IN THE FLATTERING
  DIRECTION. D1 reads: "Substitute the authority AND rewrite every leaf of the
  decision that names it." Measured, the AND was unnecessary: pick a word the
  row already contains and the cost is one field edit and zero rewrites. A
  residual that OVERSTATES the attacker's cost is worse than an undisclosed one,
  because it retires the question. D1 IS WITHDRAWN HERE AND REPLACED, and the
  replacement is executed by a case that is expected to escape, so the stated
  cost is a measurement rather than a claim.

  BLOCKER 2 - SILENT REVERSION EXITED 0 AND THE BANNER LIED ABOUT IT.
  Moving the decided row back into the pending section returned the repaired
  lane before every authority, date, posture and coherence gate, and the success
  banner then affirmatively stated that the authority, the date and the posture
  had been checked. Section 7.10 names silent reversion explicitly. A BANNER
  MUST NEVER REPORT A GATE AS RUN WHEN IT DID NOT RUN - that is section 7.8.1's
  shape (a missing measurement presenting as a substantive one) applied to an
  instrument's own output.

  The predecessor's only detection of this ever came from the STANDING lane -
  one live artifact asserting the decision - and residual R3 demoted that
  artifact 78 minutes after the predecessor was authored. A guard that depends
  on which unreviewed candidates happen to exist on disk is not a guard. The
  repair therefore lives in the packet-only lane, which no artifact can demote.

  BLOCKER 3 - THE PINNED CLOSURE WAS DEFEATED BY ONE FILE IN THE RUN DIRECTORY,
  AND IT BOUGHT SILENCE. Gutting the pinned predecessor alone gives exit 3: the
  pin works. Adding one module named after a standard-library module into the
  directory the instrument is run from shadows that module for the subject AND
  for every pinned predecessor, because the pins cover the checkers' bytes and
  nothing covered their imports. REPRODUCED: exit 0, ZERO findings, and the
  offending artifact vanished from the output entirely - the historical
  observations block was absent. Unlike every disclosed forgery route, which
  buys a green exit code and not silence, this one buys silence. The mitigation
  is one flag, the corpus already knows it, and thirty-eight of the hundred and
  twelve checkers in this directory already carry the guard. It is now the first
  executable statement in this file, before any shadowable import, and it is
  LOUD: a named refusal on BOTH channels at a distinct exit code, saying THE
  CHECK DID NOT RUN.

THE BLOCKER-1 REPAIR IS DERIVED, NOT ENUMERATED
-----------------------------------------------
Section 7.9's rule - standing is DISCOVERED, not listed - forbids shipping a
stop-list of retention words, and a list would go stale in both directions the
moment the decision text changed. So the repair asks a property instead:

    AN ATTRIBUTION IS A STATEMENT THAT TIES AN IDENTITY TO A DECISION MOMENT.
    A DECISION HAS EXACTLY TWO RECORDED COORDINATES IN THIS PACKET - WHO AND
    WHEN - AND THE PACKET SUPPLIES BOTH. SO A LEAF CORROBORATES AN AUTHORITY
    ONLY IF IT NAMES THE AUTHORITY *AND* THE DECISION DATE, AND AN IDENTITY
    MINTED FOR THIS DECISION OCCURS NOWHERE ELSE.

That needs no vocabulary at all: the two values come out of the packet's own
authority fields, and the instrument never has to know what any English word
means. Three limbs fall out of it, each with its own diagnostic:

  * SINGLE-SOURCE - fewer than two leaves outside the field itself name the
    authority. Section 4.4's forensic finding was "Two files, one source"; a
    single-sourced attribution is that shape, one level down.
  * UNATTRIBUTED - no leaf names the authority together with the decision date.
    Presence is not attribution.
  * AMBIENT - some leaf names the authority WITHOUT the decision date, so the
    string is vocabulary this packet uses for something other than saying who
    decided. This is the derivable half of "domain-vocabulary exclusion".

MEASURED, WITH THE DEFINITION ATTACHED, AND RECOMPUTED EVERY RUN (7.2.2). The
discriminating power of an attribution gate is not a claim, it is a sweep: take
EVERY distinct three-or-more-character token of the live decision row, install it
as the authority, and count how many survive. Measured at authoring, against the
decision subtree digest recorded in the notices block below:

    328 distinct tokens in the live decision row
    327 of the 327 non-authority tokens satisfy the predecessor's CORROBORATION
        LIMB read alone - so that limb, by itself, discriminated NOTHING
    312 of 328 survive the predecessor's WHOLE decision lane (its role gate and
        its length gate do real work; its corroboration limb does not)
      5 of 328 survive this file's lane, and ONE of the five is the real
        authority

Those three figures are not frozen into a gate. `--selftest` recomputes all of
them from whatever packet is live and PRINTS them, and the normal run prints the
current value as a notice, so the disclosure cannot go stale the way a
transcribed count does. What IS gated is the pair of properties the figures are
evidence for, because those are invariants rather than measurements: the set that
survives this lane must be a STRICT SUBSET of the set that survives the
predecessor's, and it must contain the packet's actual recorded authority.

The four survivors besides the real authority are ordinary English words that
happen to occur only inside date-bearing sentences. They are NOT listed in this
source and NOT stop-listed: naming four strings is exactly the enumeration
section 7.9 forbids, it would go stale the moment the decision text changed, and
the fifth such word would defeat it.

ONE HYPOTHESIS WAS TESTED AND FAILED, AND IT IS RECORDED BECAUSE A REPAIR THAT
ONLY REPORTS WHAT WORKED IS AN ADVERTISEMENT. The obvious form of
domain-vocabulary exclusion - a token appearing in OTHER decision rows of the
same packet is domain vocabulary - is VACUOUS on these bytes. The packet's seven
other decision rows are terse and share no vocabulary with the retention row:
'retention', 'PURGED' and 'tombstone' each occur there ZERO times, exactly as
'sfbreen' does, so that comparison discriminates nothing. The limb above keeps
the idea and derives its comparison corpus differently - from whether an
occurrence is attributive at all, rather than from where it sits.

THE ACCEPTED FAILURE MODE, STATED BEFORE THE EVIDENCE
-----------------------------------------------------
A COHERENT lie, and it now costs strictly more than the predecessor said.
Substituting the authority requires installing at least two leaves that each
name the substituted identity TOGETHER WITH the decision date, and leaving no
occurrence of it anywhere else in the packet. That is executed by a case
EXPECTED to escape, so the cost is measured rather than asserted. Section 7.8's
bound applies in full and is not repealed by anything above: this binds
structure, type and internal agreement. It cannot bind the truth of content, and
no instrument in this corpus can.
"""

from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# BLOCKER 3. THE INVOCATION GUARD, AND IT IS THE FIRST THING THAT RUNS.
#
# `sys` is a builtin module: it is resolved by BuiltinImporter, which precedes
# the path finder, so it cannot be shadowed by a file in this directory. Every
# other import in this file can be. So the guard runs BEFORE them.
#
# WHY THIS IS THE CONDITION. Run as `python3 <file>`, the interpreter puts the
# SCRIPT'S OWN DIRECTORY at the head of the import path - the same directory the
# corpus's own forgery model assumes an attacker can write into. Isolated mode
# removes it and ignores the environment path variable, which is the whole of
# the fix. Thirty-eight of the checkers in this directory already refuse this
# way, at a distinct exit code, including the instruments section 7.10 discusses
# beside this one.
#
# WHY EXIT 2 AND NOT 3. 2 means "bad invocation" in this lineage's own taxonomy
# and in the thirty-eight siblings'; 3 means "ran and refused to certify". This
# is a bad invocation. Section 7.8.1 rule 3: an exit code a document CLAIMS must
# be the exit code the file PRODUCES - so the refusal text names 2 and returns 2.
#
# WHY BOTH CHANNELS. Section 7.8.1's lesson is that a refusal must be impossible
# to read as a verdict about something else. A message on one channel is a
# message a reader of the other channel does not get.
# ---------------------------------------------------------------------------

_INVOCATION_REFUSAL = (
    "PD4-UNSUPPORTED-INVOCATION: this instrument must be run in ISOLATED, "
    "NO-BYTECODE mode - `python3 -I -B <this file>`. Without -I the script's "
    "own directory heads the import path, so one file written beside this one "
    "and named after a standard-library module shadows that module for this "
    "instrument AND for every hash-pinned predecessor it executes - the pins "
    "cover their bytes and nothing covers their imports. Measured on the "
    "predecessor: that attack returns exit 0 with ZERO findings and REMOVES the "
    "offending artifact from the output entirely. THE CHECK DID NOT RUN and "
    "this run certifies nothing. Exit 2."
)
if sys.flags.isolated != 1 or not sys.flags.dont_write_bytecode:
    print(_INVOCATION_REFUSAL, file=sys.stderr)
    print(_INVOCATION_REFUSAL)
    print("SCAN-NOT-RUN")
    raise SystemExit(2)

import ast                                             # noqa: E402
import copy                                            # noqa: E402
import datetime                                        # noqa: E402
import hashlib                                         # noqa: E402
import importlib.util                                  # noqa: E402
import json                                            # noqa: E402
import re                                              # noqa: E402
from pathlib import Path                               # noqa: E402


HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# The predecessor is a RUNTIME INPUT, hash-verified before execution (7.3).
# Drift is EXIT_REFUSED, never a silent fallback.
# ---------------------------------------------------------------------------
PREDECESSOR_BINDING = {
    "path": "check-product-dispositions-v3.py",
    "sha256": "b4e88027d3e4681445d3bee0a591d1629a68843fb6da7e02e8e6d7011d49994d",
    "bytes": 94440,
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
# A FIFTH code, and it repairs a non-blocking finding the review recorded
# against the predecessor: an OPTIONAL, per-class input that is ABSENT came out
# as an ordinary finding at exit 1, while the SAME input CORRUPTED came out as a
# whole-run refusal at exit 3 - the same input under two different disciplines,
# and a build reading the exit code could not tell "the packet is wrong" from "a
# file is not there". Section 7.8.1 rule 2 prescribes the shape: a required
# input refuses the whole run; a PER-CLASS input skips ONLY ITS OWN CLASS, BY
# NAME, at a DISTINCT exit code, leaving every other class measuring. A blanket
# stop would throw away real coverage. So: every class that ran is green, and at
# least one class did not run and is named. Precedence, highest first:
# 2 bad invocation, 3 nothing ran, 1 findings, 4 green but a class was skipped,
# 0 green.
EXIT_CLASS_SKIPPED = 4
DECLARED_FLAGS = ("--selftest",)
# The shape of an outcome that reports an INPUT rather than the SUBJECT. Derived
# from the wording the pinned closure already uses for exactly this condition,
# rather than from a list of its finding codes, so a new unreadable-input path
# in that closure is partitioned correctly without an edit here.
INPUT_UNAVAILABLE_MARKERS = ("cannot read ", "cannot parse ", "cannot load ")

MAX_DEPTH = 60
FINDING_PREFIX = "PD4"

# A date used as a COORDINATE of a decision. The predecessor's form check is
# anchored, because it validates a field; this one searches, because it hunts a
# date inside prose. A pattern hit is not enough - the calendar is checked too,
# so '2026-02-30' in a sentence is not a decision moment.
ISO_IN_TEXT_RE = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")


def _load_predecessor():
    """Hash-verify then execute the predecessor as a library. Never falls back."""
    path = HERE / PREDECESSOR_BINDING["path"]
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RuntimeError(
            f"cannot read pinned predecessor {PREDECESSOR_BINDING['path']} "
            f"({type(exc).__name__})") from exc
    if len(raw) != PREDECESSOR_BINDING["bytes"]:
        raise RuntimeError(
            f"pinned predecessor {PREDECESSOR_BINDING['path']} is {len(raw)} "
            f"bytes, expected {PREDECESSOR_BINDING['bytes']}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PREDECESSOR_BINDING["sha256"]:
        raise RuntimeError(
            f"pinned predecessor {PREDECESSOR_BINDING['path']} hashes {digest}, "
            f"expected {PREDECESSOR_BINDING['sha256']}")
    spec = importlib.util.spec_from_file_location("_pd_v3", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot build an import spec for the pinned predecessor")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def partition_input_unavailability(items: list[str]) -> tuple[list[str], list[str]]:
    """Split a class's outcomes into FINDINGS ABOUT THE SUBJECT and MISSING INPUT.

    Section 7.8.1's whole subject is that these two must never print the same:
    "derived from nothing" and "derived and found nothing" are different facts,
    and an absent input that presents as a finding is an accusation nobody made.
    """
    unavailable = [item for item in items
                   if any(marker in item for marker in INPUT_UNAVAILABLE_MARKERS)]
    findings = [item for item in items if item not in unavailable]
    return findings, unavailable


def import_provenance_failures() -> list[str]:
    """Belt and braces for blocker 3: no import may have come from HERE.

    The flag guard above is the load-bearing check and it runs first. This is a
    MEASUREMENT taken after the fact, printed in the banner, and fatal if it ever
    disagrees - because "the flag was set" is a statement about the invocation
    and this is a statement about what actually got loaded. If the two ever
    disagree, the assumption behind the whole pin chain is wrong and the run must
    not certify anything.
    """
    out: list[str] = []
    here = str(HERE)
    # This file, and the hash-pinned closure it deliberately executes out of
    # this directory, are the only admissible residents. Everything else loaded
    # from here is a module that shadowed a real one.
    permitted = {str(Path(__file__).resolve()),
                 str((HERE / PREDECESSOR_BINDING["path"]).resolve())}
    for name in sorted(sys.modules):
        module = sys.modules.get(name)
        origin = getattr(module, "__file__", None)
        if not isinstance(origin, str) or not origin:
            continue
        try:
            resolved = str(Path(origin).resolve())
        except (OSError, ValueError):
            continue
        if resolved.startswith(here + "/") and resolved not in permitted:
            out.append(
                f"{FINDING_PREFIX}-IMPORT-PROVENANCE: module {name!r} was loaded "
                f"from {resolved}, inside the directory this instrument is run "
                "from. A module beside the checker can shadow the one its pin "
                "chain depends on. THE CHECK DID NOT RUN")
    return out


# ---------------------------------------------------------------------------
# THE GATE LEDGER. Blocker 2's second half.
#
# The predecessor's success banner is one unconditional sentence asserting that
# the authority, the date and the posture were checked. On a reverted packet
# none of those gates runs and the sentence is printed anyway - prose asserting a
# measurement that was not taken, emitted by an instrument built to enforce the
# rule against exactly that. So no clause of this file's banner is a literal:
# every clause is REGISTERED BY THE GATE THAT PRODUCED IT, at the moment it runs,
# and the banner is assembled from the register. A gate that returns early
# registers nothing and its clause cannot be printed. A gate that is skipped
# registers WHY, and the skip is printed too - "derived from nothing" and
# "derived and found nothing" must never print the same (7.8.1 rule 1).
# ---------------------------------------------------------------------------

class GateLedger:
    """What ran, what did not, and why. The banner may say nothing else."""

    def __init__(self) -> None:
        self.ran: list[tuple[str, str]] = []
        self.skipped: list[tuple[str, str]] = []

    def executed(self, gate: str, clause: str) -> None:
        self.ran.append((gate, clause))

    def not_executed(self, gate: str, why: str) -> None:
        self.skipped.append((gate, why))

    @property
    def gate_names(self) -> list[str]:
        return [gate for gate, _ in self.ran]

    def clauses(self) -> list[str]:
        return [clause for _, clause in self.ran]


# ---------------------------------------------------------------------------
# BLOCKER 1. ATTRIBUTIVE CORROBORATION.
# ---------------------------------------------------------------------------

def _packet_leaves(packet: object, v3) -> tuple[list[tuple[str, str]], list[str]]:
    overflow: list[str] = []
    leaves = list(v3.string_leaves(packet, "$", 0, overflow))
    return leaves, overflow


def _names_a_decision_moment(text: str, coordinate: str) -> bool:
    """Does this leaf carry the decision's DATE coordinate as a real date?

    The value is compared as a whole token AND validated as a calendar date, so
    a leaf that merely contains the digits is not mistaken for a leaf that
    records when the decision was taken.
    """
    for match in ISO_IN_TEXT_RE.finditer(text):
        if match.group(0) != coordinate.strip():
            continue
        try:
            datetime.date(int(match.group(1)), int(match.group(2)),
                          int(match.group(3)))
        except ValueError:
            continue
        return True
    return False


def _witness_split(packet_leaves: list[tuple[str, str]], token: str,
                   own_path: str, carries_other_coordinate, v3
                   ) -> tuple[list[str], list[str], list[str]]:
    """(witnesses, attributive, ambient) for one authority coordinate.

    A WITNESS is any leaf other than the field itself that names the token on
    word boundaries. It is ATTRIBUTIVE if it ALSO carries the decision's OTHER
    coordinate - who plus when, in one statement. It is AMBIENT if it does not:
    the packet is using that string for something other than saying who decided.

    The two coordinates are tested by DIFFERENT predicates on purpose. A date is
    matched as a date and validated against the calendar, so digits that merely
    look like one do not count; a name is matched on word boundaries. Passing the
    date matcher a name - which is the shape of a real defect this file caught in
    its own first draft, against live bytes - would make every date look
    unattributed.
    """
    pattern = v3._word_bounded(token.strip())
    witnesses: list[str] = []
    attributive: list[str] = []
    ambient: list[str] = []
    for path, text in packet_leaves:
        if path == own_path or not pattern.search(text):
            continue
        witnesses.append(path)
        (attributive if carries_other_coordinate(text) else ambient).append(path)
    return witnesses, attributive, ambient


def attributive_authority_failures(packet: object, decision: dict, where: str,
                                   v3, ledger: GateLedger | None = None
                                   ) -> list[str]:
    """The repaired corroboration gate. A pure function of the parsed packet.

    Reads the packet and NOTHING else - no corpus, no digest, no head document -
    so nothing that can be written into this directory can demote a finding here.
    """
    out: list[str] = []
    decided_by = decision.get("decidedBy")
    decided_on = decision.get("decidedOn")
    usable_by = (isinstance(decided_by, str) and decided_by.strip()
                 and not v3.PLACEHOLDER_RE.search(decided_by))
    usable_on = (isinstance(decided_on, str) and decided_on.strip()
                 and not v3.PLACEHOLDER_RE.search(decided_on))
    if not usable_by or not usable_on:
        if ledger is not None:
            ledger.not_executed(
                "attributive-corroboration",
                "the row does not carry BOTH a usable authority and a usable "
                "date, so no attribution could be tested; the type and "
                "placeholder gates own that state and have reported it")
        return out

    leaves, overflow = _packet_leaves(packet, v3)
    if overflow:
        out.append(
            f"{FINDING_PREFIX}-DEPTH: the packet nests deeper than {MAX_DEPTH} at "
            f"{overflow[0]}; the attribution gate did NOT examine it")

    # A value made entirely of words that carry no identifying content names
    # nobody, and the predecessor's role gate cannot see it: its test is
    # "every meaningful token is a role", which is false when there are no
    # meaningful tokens at all. Same vocabulary, opposite corner.
    if not v3._role_verdict(decided_by.strip()):
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-VACUOUS: {where}.decidedBy is "
            f"{decided_by!r}, which has no meaningful word left once the "
            "content-free words are removed. It identifies nobody")
        if ledger is not None:
            ledger.not_executed(
                "attributive-corroboration",
                "the recorded authority carries no identifying word, so there "
                "was nothing to corroborate")
        return out

    authority_pattern = v3._word_bounded(decided_by.strip())

    def names_the_moment(text: str) -> bool:
        return _names_a_decision_moment(text, decided_on)

    def names_the_authority(text: str) -> bool:
        return bool(authority_pattern.search(text))

    by_w, by_attr, by_amb = _witness_split(
        leaves, decided_by, f"{where}.decidedBy", names_the_moment, v3)
    on_w, on_attr, _ = _witness_split(
        leaves, decided_on, f"{where}.decidedOn", names_the_authority, v3)

    if len(by_w) < 2:
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-SINGLE-SOURCE: {where}.decidedBy is "
            f"{decided_by!r} and only {len(by_w)} other leaf/leaves of the packet "
            f"name it ({sorted(by_w) or 'none'}). Section 4.4's fabrication was a "
            "single-source attribution - two files, one authoring pass, never "
            "independent corroboration. One position saying who decided is that "
            "shape one level down. Record the attribution in a second position, "
            "naming the authority together with the decision date")
    if not by_attr:
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-UNATTRIBUTED: {where}.decidedBy is "
            f"{decided_by!r}; {len(by_w)} leaf/leaves name it and NOT ONE of them "
            f"also names the decision date {decided_on!r}. PRESENCE IS NOT "
            "ATTRIBUTION: an attribution says who AND when, so a word that is "
            "merely already in the row corroborates nothing. This is the exact "
            "hole that let an attribution naming nobody pass the predecessor")
    elif by_amb:
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-AMBIENT: {where}.decidedBy is "
            f"{decided_by!r}, and {len(by_amb)} leaf/leaves name it WITHOUT the "
            f"decision date - first {sorted(by_amb)[0]}. The packet uses that "
            "string for something other than recording who decided, so it is "
            "this document's vocabulary rather than an identity minted for this "
            "decision. An identity that collides with the packet's own prose "
            "cannot be corroborated distinctly and is refused fail-closed")

    if len(on_w) < 2:
        out.append(
            f"{FINDING_PREFIX}-DATE-SINGLE-SOURCE: {where}.decidedOn is "
            f"{decided_on!r} and only {len(on_w)} other leaf/leaves of the packet "
            "name it. A decision moment nobody else records was substituted "
            "rather than recorded")
    if not on_attr:
        out.append(
            f"{FINDING_PREFIX}-DATE-UNATTRIBUTED: {where}.decidedOn is "
            f"{decided_on!r} and no leaf names it together with the recorded "
            f"authority {decided_by!r}. The two coordinates of the decision are "
            "never stated in one breath, so nothing in the packet attributes "
            "this decision to anybody on this date")
    # DELIBERATELY ABSENT: an AMBIENT limb for the date. A date is a coordinate,
    # not an identity, and dates legitimately recur throughout a packet that
    # records several events. Requiring every mention of a date to be attributive
    # would fire on any packet that records a second dated event, which is the
    # 7.10 error of asserting that today's shape will never change.

    if ledger is not None:
        if out:
            # A gate that RAN AND FAILED licenses no sentence. The predecessor's
            # banner asserted the authority had been checked in a state where
            # nothing checked it; the mirror error would be asserting it in a
            # state where the check ran and disagreed.
            ledger.not_executed(
                "attributive-corroboration",
                f"the gate ran and FAILED at {len(out)} position(s), so it "
                "licenses no clause")
        else:
            ledger.executed(
                "attributive-corroboration",
                f"whose authority {decided_by!r} is named by {len(by_w)} other "
                f"leaf/leaves of this packet, {len(by_attr)} of which name it "
                f"together with the decision date {decided_on!r}, and none of "
                "which uses it for anything else")
    return out


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,}")


def attribution_discrimination(packet: object, v3, v2, v1, deep: bool = False):
    """How many candidate authorities survive? A sweep, not a claim.

    Returns (tokens, survivors_v4, survivors_predecessor_or_None). The token
    population is DERIVED from whatever the live decision row says, so this is a
    census re-walked from the bytes at run time rather than a number transcribed
    at authoring - which is the only kind of self-measurement that cannot be
    wrong by construction (7.2.2, four measured instances of the opposite).
    """
    ident = v2.RETENTION_DECISION_ID
    if not isinstance(packet, dict):
        return [], [], None
    decisions = packet.get("decisions")
    if not isinstance(decisions, dict) or not isinstance(decisions.get(ident), dict):
        return [], [], None
    tokens = set()
    for _path, text in v3.string_leaves(decisions[ident], "x", 0, []):
        tokens.update(TOKEN_RE.findall(text))
    tokens = sorted(tokens)
    survivors: list[str] = []
    predecessor_survivors: list[str] | None = [] if deep else None
    for token in tokens:
        probe = copy.deepcopy(packet)
        probe["decisions"][ident]["decidedBy"] = token
        if not decision_property_failures_v4(probe, v3, v2):
            survivors.append(token)
        if predecessor_survivors is not None:
            if not v3.decision_lane_failures(probe, v2, v1):
                predecessor_survivors.append(token)
    return tokens, survivors, predecessor_survivors


# ---------------------------------------------------------------------------
# BLOCKER 2. SILENT REVERSION.
#
# Section 7.10's derived rule is to PIN THE PROPERTY, NOT THE CURRENT VALUE,
# whenever the value is something the corpus is explicitly waiting to change.
# Pinning "the row is DECIDED" is what broke nineteen checkers on the day the
# authority decided, and this file does not do it: the pending state remains a
# fully accepted state and a packet that has never decided passes in silence.
#
# The property is MONOTONICITY: a decision this packet's own record says was
# TAKEN may not quietly become pending again. And the record is DERIVED from the
# packet, not enumerated: applying a decision leaves residue - the packet points
# at the row's home, and the packet states the decision's moment beside its id.
# Both are constructed from the packet's own key names and the decision id, so
# no position is named in this source and a packet that grows new positions is
# covered without an edit.
#
# THE SUPERSESSION-MARKER EXCUSE IS DELIBERATELY NOT APPLIED HERE, and that is a
# ruling rather than an omission. That excuse exists so an honest record of a
# PRE-decision quotation is not read as a live assertion. Residue of a TAKEN
# decision is the opposite direction: a leaf that says the authority decided,
# under a heading that says the previous wording was superseded, is evidence FOR
# the decision, not a quotation of the state before it. Applying the excuse here
# would let a reverter keep every trace of the decision simply because the
# packet honestly labelled its own history.
# ---------------------------------------------------------------------------

def reversion_failures(packet: object, decision_id: str, v3,
                       ledger: GateLedger | None = None) -> list[str]:
    out: list[str] = []
    if not isinstance(packet, dict):
        if ledger is not None:
            ledger.not_executed("decision-monotonicity",
                                "the packet root is not an object")
        return out
    decisions = packet.get("decisions")
    still_decided = isinstance(decisions, dict) and decision_id in decisions
    if still_decided:
        if ledger is not None:
            ledger.executed(
                "decision-monotonicity",
                "which still sits where a taken decision lives, so no position "
                "in this packet is pointing at a decision that has been removed")
        return out

    pending_root = "$.pendingDecisions"
    leaves, overflow = _packet_leaves(packet, v3)
    if overflow:
        out.append(
            f"{FINDING_PREFIX}-DEPTH: the packet nests deeper than {MAX_DEPTH} at "
            f"{overflow[0]}; the reversion gate did NOT examine it, so its "
            "silence is not evidence")
    pointer = f"$.decisions.{decision_id}"
    id_pattern = v3._word_bounded(decision_id)

    pointer_sites: list[tuple[str, str]] = []
    moment_sites: list[tuple[str, str]] = []
    for path, text in leaves:
        if path.startswith(pending_root):
            continue
        if pointer in text:
            pointer_sites.append((path, text))
            continue
        if not id_pattern.search(text):
            continue
        for match in ISO_IN_TEXT_RE.finditer(text):
            try:
                datetime.date(int(match.group(1)), int(match.group(2)),
                              int(match.group(3)))
            except ValueError:
                continue
            moment_sites.append((path, text))
            break

    for path, text in pointer_sites:
        out.append(
            f"{FINDING_PREFIX}-DECISION-REVERTED: {decision_id} is NOT in this "
            f"packet's decided set, yet {path} points into {pointer} - the "
            "packet refers to a decided row that is not there: "
            f"{text.strip()[:110]!r}. A decision this packet's own record says "
            "was taken may not silently become pending; that is a MONOTONICITY "
            "property, not a snapshot, and section 7.10 asks for the property "
            "to be pinned")
    for path, text in moment_sites:
        out.append(
            f"{FINDING_PREFIX}-DECISION-REVERTED: {decision_id} is NOT in this "
            f"packet's decided set, yet {path} records it beside a real calendar "
            f"date: {text.strip()[:110]!r}. A pending decision has no moment. "
            "Either the row was reverted after being taken, or this position is "
            "recording a decision the packet does not carry")

    if ledger is not None:
        if out:
            ledger.not_executed(
                "decision-monotonicity",
                f"{decision_id} is absent from the decided set while "
                f"{len(out)} position(s) still record it as taken")
        else:
            ledger.executed(
                "decision-monotonicity",
                "and no position in this packet records it as ever having been "
                "taken, so the pending state is the packet's own consistent "
                "account rather than a reversion")
    return out


# ---------------------------------------------------------------------------
# The v4 decision lane, assembled.
#
# PURE FUNCTION OF A PARSED PACKET. No I/O, no digest, no corpus, no head
# document. An external driver can load this file and mutate a packet in memory
# to prove the gates are not vacuous - the 7.8 "prove non-vacuity from outside
# itself" discipline - and nothing written into this directory can demote a
# finding produced here.
# ---------------------------------------------------------------------------

def decision_property_failures_v4(packet: object, v3, v2,
                                  ledger: GateLedger | None = None) -> list[str]:
    decision_id = v2.RETENTION_DECISION_ID
    where = f"$.decisions.{decision_id}"
    out: list[str] = []
    if not isinstance(packet, dict):
        return [f"{FINDING_PREFIX}-SHAPE: the binding packet root is "
                f"{type(packet).__name__}, not an object"]

    out.extend(reversion_failures(packet, decision_id, v3, ledger))

    decisions = packet.get("decisions")
    if not isinstance(decisions, dict) or decision_id not in decisions:
        if ledger is not None:
            ledger.not_executed(
                "attributive-corroboration",
                f"{decision_id} is not in the decided set, so it records no "
                "authority and no date for this gate to examine")
        return out
    decision = decisions[decision_id]
    if not isinstance(decision, dict):
        if ledger is not None:
            ledger.not_executed("attributive-corroboration",
                                "the decided row is not an object")
        return out
    out.extend(attributive_authority_failures(packet, decision, where, v3, ledger))
    return out


def decision_lane_v4(packet: object, v3, v2, v1,
                     ledger: GateLedger | None = None) -> list[str]:
    """The predecessor's whole decision lane UNCHANGED, plus this file's gates.

    The union is the point. Calling rather than replacing is what makes "no
    detection semantics were weakened" a MEASUREMENT: every case the predecessor
    caught is still caught by the same bytes that caught it, and --selftest
    re-drives the predecessor's entire published case corpus to say so.
    """
    try:
        inherited = v3.decision_lane_failures(packet, v2, v1)
    except RecursionError:
        inherited = [f"{FINDING_PREFIX}-DEPTH: the inherited decision lane hit "
                     "the interpreter recursion limit; the packet was NOT fully "
                     "examined"]
    try:
        own = decision_property_failures_v4(packet, v3, v2, ledger)
    except RecursionError:
        own = [f"{FINDING_PREFIX}-DEPTH: the repaired decision lane hit the "
               "interpreter recursion limit; the packet was NOT fully examined"]
    except v1.MALFORMED_SHAPE_EXCEPTIONS as exc:
        own = [f"{FINDING_PREFIX}-EXCEPTION: malformed decision shape "
               f"({type(exc).__name__})"]
    return inherited + own


def validate_v4(product: object, ri: dict, versioning: dict, delivery: dict,
                retention: dict | None, v3, v2, v1,
                ledger: GateLedger | None = None) -> list[str]:
    if not isinstance(product, dict) or not product:
        return [f"{FINDING_PREFIX}-TOTALITY-ROOT: product root must be a "
                "non-empty object"]
    if not isinstance(product.get("decisions"), dict):
        return [f"{FINDING_PREFIX}-TOTALITY-SHAPE: decisions must be an object"]
    inherited = v3.validate_v3(product, ri, versioning, delivery, retention, v2, v1)
    return inherited + decision_property_failures_v4(product, v3, v2, ledger)


# ---------------------------------------------------------------------------
# Fixtures. They build the world they test, so they stay meaningful whichever
# state the live packet is in.
#
# WHY A FRESH POSITIVE CORPUS AGAIN. The predecessor built its own because ITS
# predecessor's must-pass fixture certified one of the escapes the review
# measured - a suite that certifies the escape cannot find it. The same is true
# one generation on: the predecessor's must-pass row names its authority in
# exactly ONE other leaf, which this lane calls SINGLE-SOURCE. That is reported
# by --selftest as a MEASURED DELTA rather than smoothed over, and it is the
# reason the fixtures below carry a second attributive position.
# ---------------------------------------------------------------------------

def _good_decision(v3) -> dict:
    row = copy.deepcopy(v3._GOOD_DECISION)
    row["attributionRestated"] = (
        "Recorded a second time on purpose: this row was decided on 2026-08-05 "
        "by qbeltran, and section 4.4's finding was that a single-source "
        "attribution is not corroboration.")
    return row


def _fixture(v3, v2, v1, decided=None, pending=None, **extra) -> dict:
    return v3._fixture_packet(v1, v2, decided=decided, pending=pending, **extra)


def _row(v3, **over) -> dict:
    row = _good_decision(v3)
    for key, value in over.items():
        if value is v3._REMOVE:
            row.pop(key, None)
        else:
            row[key] = value
    return row


def _renamed(v3, new_name: str) -> dict:
    """The good row with the authority coherently replaced everywhere in it."""
    return json.loads(json.dumps(_good_decision(v3)).replace("qbeltran", new_name))


def decision_cases_v4(v3, v2, v1):
    """(must_pass, must_fail, expected_escapes) for the gates this file adds."""
    must_pass = (
        ("STATE D - a decided row whose authority is attributively corroborated "
         "at two positions",
         _fixture(v3, v2, v1, decided=_good_decision(v3))),
        ("STATE D - a DIFFERENT authority and date, coherently recorded (a "
         "legitimate future amendment must pass)",
         _fixture(v3, v2, v1, decided=_row(
             v3, decidedBy="rlindqvist", decidedOn="2026-09-30",
             attributionProvenance=(
                 "The product authority rlindqvist recorded this decision on "
                 "2026-09-30 and chose that identity."),
             attributionRestated=(
                 "Decided 2026-09-30 by rlindqvist; recorded twice so the "
                 "attribution is not single-sourced.")))),
        ("STATE D - the second attributive position sits OUTSIDE the decision "
         "row, in the packet's own status line",
         _fixture(v3, v2, v1,
                  decided=_row(v3, attributionRestated=v3._REMOVE),
                  status=("BINDING (retention disposition DECIDED 2026-08-05 by "
                          "qbeltran)"))),
        ("STATE P - pending and blocked, with no residue of a taken decision",
         _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING))),
        ("STATE P - a pending packet may mention the decision id without a date",
         _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING),
                  purpose="Keep the CD-RT-5 choice fail-closed until its input exists.")),
        ("STATE P - a pending packet may carry a dated note that names no "
         "decision id",
         _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING),
                  authoringNote="Prepared 2026-07-31 by the coordinating lane.")),
    )

    ident = v2.RETENTION_DECISION_ID
    reverted = _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING),
                        status=(f"BINDING ({ident} DECIDED 2026-08-05 by "
                                "qbeltran)"))
    reverted_pointer = _fixture(
        v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING),
        knownLimitations=[f"{ident} is now resolved - see $.decisions.{ident}."])
    reverted_marked = _fixture(
        v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING),
        knownLimitations=[
            f"SUPERSEDED. It read verbatim: '{ident} is unresolved.' The "
            f"product authority decided {ident} on 2026-08-05."])
    vanished = _fixture(v3, v2, v1,
                        status=(f"BINDING ({ident} DECIDED 2026-08-05 by "
                                "qbeltran)"))
    vanished["pendingDecisions"] = {}

    must_fail = (
        # --- blocker 1: attribution that names nobody ------------------------
        ("B1 decidedBy -> a word the decision row already uses, naming nobody "
         "(the reviewer's measured escape class)", "AUTHORITY-UNATTRIBUTED",
         _fixture(v3, v2, v1, decided=_row(v3, decidedBy="Retention"))),
        ("B1 decidedBy -> a token of the posture narrative", "AUTHORITY-UNATTRIBUTED",
         _fixture(v3, v2, v1, decided=_row(v3, decidedBy="durably"))),
        ("B1 decidedBy is attributively corroborated TWICE but the packet also "
         "uses the same string outside any dated statement", "AUTHORITY-AMBIENT",
         _fixture(v3, v2, v1, decided=_renamed(v3, "Rutherford"),
                  purpose="Rutherford is named here for an unrelated reason.")),
        ("B1 decidedBy named in exactly ONE other leaf (single-source "
         "attribution, section 4.4's shape)", "AUTHORITY-SINGLE-SOURCE",
         _fixture(v3, v2, v1, decided=_row(v3, attributionRestated=v3._REMOVE))),
        ("B1 decidedBy corroborated twice but NEVER beside the decision date",
         "AUTHORITY-UNATTRIBUTED",
         _fixture(v3, v2, v1, decided=_row(
             v3,
             attributionProvenance="The authority chose the identity 'qbeltran'.",
             attributionRestated="Recorded again: qbeltran."))),
        ("B1 decidedBy is made only of content-free words, which the inherited "
         "role gate cannot see because it has no meaningful token to test",
         "AUTHORITY-VACUOUS",
         _fixture(v3, v2, v1, decided=_row(v3, decidedBy="this and that"))),
        ("B1 decidedOn substituted; no leaf records that moment",
         "DATE-SINGLE-SOURCE",
         _fixture(v3, v2, v1, decided=_row(v3, decidedOn="2027-03-04"))),
        ("B1 decidedOn recorded twice but never beside the authority",
         "DATE-UNATTRIBUTED",
         _fixture(v3, v2, v1, decided=_row(
             v3,
             attributionProvenance="The identity chosen was 'qbeltran'.",
             attributionRestated="Also recorded: qbeltran.",
             whenNoted="The moment was 2026-08-05.",
             alsoNoted="Recorded again on 2026-08-05."))),

        # --- blocker 2: silent reversion --------------------------------------
        ("B2 the decided row is moved back to pending while the packet's own "
         "status still records the decision", "DECISION-REVERTED", reverted),
        ("B2 the decided row is moved back to pending while the packet still "
         "points into the decided row's home", "DECISION-REVERTED",
         reverted_pointer),
        ("B2 the same reversion, with the residue carrying a supersession "
         "marker (the marker excuse must NOT apply in this direction)",
         "DECISION-REVERTED", reverted_marked),
        ("B2 the decided row vanishes from both sets while the packet still "
         "records the decision", "DECISION-REVERTED", vanished),
    )

    expected_escapes = (
        ("RESIDUAL-V1 the COHERENT authority lie, AT ITS MEASURED COST: "
         "substitute the authority AND install TWO leaves that each name the "
         "substituted identity beside the decision date AND leave no other "
         "occurrence of it anywhere in the packet",
         _fixture(v3, v2, v1, decided=_renamed(v3, "mnowak"))),
        ("RESIDUAL-V3 the COHERENT posture lie: flip both posture fields AND "
         "rewrite the posture narrative to match (inherited, unchanged)",
         _fixture(v3, v2, v1, decided=json.loads(json.dumps(
             dict(_good_decision(v3),
                  defaultPosture={
                      "durableDefault": "EPHEMERAL_DISCARDED",
                      "implicitDurableRetention": "NO",
                      "meaning": ("A project with no configured retention policy "
                                  "writes nothing. A durable-authoritative "
                                  "request is refused.")}))))),
        ("RESIDUAL-V4 a false JUDGEMENT in the decision body (inherited, "
         "unchanged): the substance is rewritten coherently",
         _fixture(v3, v2, v1, decided=_row(v3, decision={
             "boundedRetention": "Retention is unbounded and no bound is "
                                 "configurable."}))),
        ("RESIDUAL-V5 a reversion that also ERASES the residue: move the row "
         "back to pending AND remove every position that recorded the decision",
         _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING))),
    )
    return must_pass, must_fail, expected_escapes


# ---------------------------------------------------------------------------
# Hostile-input matrix. A CRASH MUST NOT READ AS A FINDING (litmus D-6).
# The predecessor's fourteen shapes are re-driven through this lane unchanged
# and are not re-typed; these are the shapes the new gates add reach over.
# ---------------------------------------------------------------------------

def hostile_shapes_v4(v3, v2, v1) -> tuple:
    ident = v2.RETENTION_DECISION_ID
    deep: object = "leaf"
    for _ in range(400):
        deep = [deep]
    return (
        ("pendingDecisions is a string",
         {"decisions": {}, "pendingDecisions": "none"}),
        ("pendingDecisions is a list", {"decisions": {}, "pendingDecisions": []}),
        ("the pending row is an int",
         {"decisions": {}, "pendingDecisions": {ident: 3}}),
        ("decidedOn is a well-formed but impossible calendar date",
         {"decisions": {ident: {"decidedBy": "qbeltran",
                                "decidedOn": "2026-02-30"}}}),
        ("decidedBy is a regex metacharacter soup",
         {"decisions": {ident: {"decidedBy": "(.*)+[a-z", "decidedOn": "2026-08-05"}}}),
        ("decidedOn is a regex metacharacter soup",
         {"decisions": {ident: {"decidedBy": "qbeltran", "decidedOn": "\\d{4}"}}}),
        ("decidedBy is 200000 characters",
         {"decisions": {ident: {"decidedBy": "q" * 200000,
                                "decidedOn": "2026-08-05"}}}),
        ("400-deep LIST nesting outside the decision row",
         {"decisions": {ident: {"decidedBy": "qbeltran",
                                "decidedOn": "2026-08-05"}},
          "note": deep}),
        ("a decision id that is itself a regex metacharacter",
         {"decisions": {ident: {"decidedBy": "qbeltran",
                                "decidedOn": "2026-08-05"}},
          "pendingDecisions": {}}),
        ("the packet reverts the row and carries a date with a 5-digit year",
         {"decisions": {}, "pendingDecisions": {ident: {}},
          "note": f"{ident} decided 20260-08-05."}),
        ("the packet reverts the row and carries a NON-calendar date beside "
         "the id", {"decisions": {}, "pendingDecisions": {ident: {}},
                    "note": f"{ident} decided 2026-13-45."}),
        ("a lone surrogate in a leaf that also names the decision date",
         {"decisions": {ident: {"decidedBy": "qbeltran",
                                "decidedOn": "2026-08-05"}},
          "note": "\ud800 2026-08-05 qbeltran"}),
        ("decidedBy equals decidedOn",
         {"decisions": {ident: {"decidedBy": "2026-08-05",
                                "decidedOn": "2026-08-05"}}}),
        ("decisions present, pendingDecisions absent, row absent",
         {"decisions": {}}),
    )


# ---------------------------------------------------------------------------
# HONEST LIMITS.
#
# Every residual carries the LANE it belongs to and the label of the --selftest
# case that EXECUTES it, or None. The counts below are computed with len() from
# the tuples, so they cannot drift from the list, and --selftest fails if any
# non-None gate label does not correspond to a case the suite actually ran -
# section 7.8's move 6, "make the residual gate the build", applied to the
# disclosure itself. The predecessor published sixteen and its reviewer measured
# that seven were gated by an executed case; that ratio is now published rather
# than left to a reader to compute.
# ---------------------------------------------------------------------------

def residual_registry(v3) -> tuple:
    """(tag, lane, text, gate label or None). Inherited rows are CARRIED."""
    rows: list[tuple[str, str, str, str | None]] = []
    gated_demotion = {"R1", "R2", "R3", "R4"}
    for tag, text in v3.DEMOTION_LANE_RESIDUALS:
        rows.append((tag, "demotion/standing (inherited, unchanged)", text,
                     "inherited demotion corpus" if tag in gated_demotion else None))
    for tag, text in v3.DECISION_LANE_RESIDUALS:
        if tag == "D1":
            rows.append((
                tag, "decision-set (inherited)",
                "WITHDRAWN AND CORRECTED BY THIS SUCCESSOR. It read verbatim: "
                + text.split(" Executed by")[0].strip()
                + " MEASURED FALSE: the AND was unnecessary, because the "
                "predecessor's corroboration gate accepted any word already "
                "present in the row, so the attack cost one field edit and zero "
                "rewrites. A residual that overstates the attacker's cost is "
                "worse than an undisclosed one, because it retires the "
                "question. The true cost is now residual V1.",
                "RESIDUAL-V1"))
            continue
        rows.append((tag, "decision-set (inherited)", text,
                     {"D2": "RESIDUAL-V3", "D3": "RESIDUAL-V4"}.get(tag)))
    for tag, text in v3.SCOPE_RESIDUALS:
        rows.append((tag, "scope (inherited)", text, None))

    rows.extend([
        ("V1", "decision-set (this successor)",
         "the COHERENT authority lie, at its MEASURED cost, replacing the "
         "withdrawn D1. Substitute the authority, install at least TWO leaves "
         "that each name the substituted identity together with the decision "
         "date, and leave no occurrence of it anywhere else in the packet. "
         "Executed by a case EXPECTED to escape, so the cost is measured.",
         "RESIDUAL-V1"),
        ("V2", "decision-set (this successor)",
         "the attribution gate is NARROWED, NOT CLOSED. Some candidate "
         "authorities that name nobody still survive it - ordinary words that "
         "happen to occur only inside sentences carrying the decision date. How "
         "many is a MEASUREMENT and is recomputed every run rather than "
         "transcribed here: the notices block above prints the current sweep, "
         "and --selftest prints it beside the predecessor's for comparison. The "
         "survivors are deliberately NOT listed in this source, because naming "
         "them is the enumeration section 7.9 forbids and the next such word "
         "would defeat it.",
         "attribution discrimination sweep"),
        ("V3", "decision-set (this successor)",
         "the COHERENT posture lie is inherited unchanged and is not narrowed "
         "here. Flip both posture fields AND rewrite the posture narrative.",
         "RESIDUAL-V3"),
        ("V4", "decision-set (this successor)",
         "a false JUDGEMENT in the decision body is inherited unchanged. Prose "
         "asserting a MEASUREMENT can be re-derived and compared; prose "
         "asserting a judgement has no oracle.",
         "RESIDUAL-V4"),
        ("V5", "decision-set (this successor)",
         "the reversion gate reads RESIDUE. A reverter who also erases every "
         "position recording the decision leaves a packet that is internally "
         "consistent about never having decided, and this lane cannot "
         "distinguish it from a packet that never did. That is a strictly "
         "larger edit than moving one row, and it is executed by a case "
         "EXPECTED to escape.",
         "RESIDUAL-V5"),
        ("V6", "decision-set (this successor)",
         "the attribution gate FAILS CLOSED in the false-positive direction, "
         "deliberately and at a cost. A legitimate amendment whose authority is "
         "named in only one position, or whose identity collides with a word "
         "the packet already uses outside a dated sentence, is a FINDING. The "
         "diagnostic says what to add. This is a real cost of the repair and it "
         "is stated here rather than discovered.",
         "B1 decidedBy named in exactly ONE other leaf (single-source "
         "attribution, section 4.4's shape)"),
        ("V7", "decision-set (this successor)",
         "the two corroborating positions are POSITIONALLY independent and not "
         "EVIDENTIALLY independent - two leaves of one document written in one "
         "pass, which is precisely the 'two files, one source' shape section "
         "4.4 rejects, one level down. The corpus-wide footprint that would be "
         "genuinely independent is deliberately kept a NOTICE, because the "
         "decision lane consults no corpus and nothing written into this "
         "directory may demote a finding it makes.",
         None),
        ("V8", "invocation (this successor)",
         "the invocation guard tests the interpreter's ISOLATION FLAGS, which "
         "is a statement about how the process was started. The import "
         "provenance check beside it is a statement about what was actually "
         "loaded, and the two are compared every run - but neither can see a "
         "module replaced in memory by something that ran even earlier.",
         "environment: import provenance"),
        ("V10", "input discipline (this successor)",
         "an absent OPTIONAL input now skips its own class BY NAME at a fifth "
         "exit code instead of presenting as a finding about the packet, which "
         "repairs a seam the review recorded against the predecessor. The "
         "partition is by the WORDING the pinned closure uses for an "
         "unreadable input, not by a list of its finding codes - so a new "
         "unreadable-input path there is partitioned correctly without an edit "
         "here, and a path that reports an unreadable input in DIFFERENT words "
         "would still be misfiled as a finding.",
         "input discipline: an absent optional input skips its class by name"),
        ("V9", "decision-set (this successor)",
         "duplicate JSON keys remain invisible: the parser keeps the last, so a "
         "packet carrying two decidedBy values is examined as one. Inherited "
         "from the predecessor's D7 and not repaired, because repairing it "
         "means replacing the parse, which changes every lane at once.",
         None),
    ])
    return tuple(rows)


def format_limits(rows: tuple) -> list[str]:
    lanes: dict[str, list[tuple[str, str, str | None]]] = {}
    for tag, lane, text, gate in rows:
        lanes.setdefault(lane, []).append((tag, text, gate))
    gated = [row for row in rows if row[3] is not None]
    lines = [
        f"HONEST LIMITS - {len(rows)} named residuals, SCOPED TO THE LANE EACH "
        "DESCRIBES,",
        f"  of which {len(gated)} are GATED BY AN EXECUTED --selftest CASE and "
        f"{len(rows) - len(gated)} are not.",
        "  A residual nothing executes is a disclosure that can go stale "
        "silently, so the",
        "  split is printed rather than left to a reader to compute. The "
        "predecessor",
        "  published 16 and an independent review measured 7 of them gated.",
    ]
    for lane in sorted(lanes):
        entries = lanes[lane]
        lane_gated = sum(1 for _, _, gate in entries if gate is not None)
        lines.append(f"  {lane.upper()} - {len(entries)} residuals, "
                     f"{lane_gated} gated")
        for tag, text, gate in entries:
            wrapped = _wrap(text, 66)
            lines.append(f"    {tag}  {wrapped[0]}")
            lines.extend(f"        {piece}" for piece in wrapped[1:])
            lines.append(f"        [{'GATED by ' + gate if gate else 'NOT GATED'}]")
    lines.append(
        "  Section 7.8's bound applies in full and is NOT repealed by any gate")
    lines.append(
        "  above: this binds structure, type and internal agreement. It cannot")
    lines.append(
        "  bind the truth of content, and no instrument in this corpus can.")
    return lines


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    out: list[str] = []
    line = ""
    for word in words:
        if line and len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        out.append(line)
    return out or [""]


# ---------------------------------------------------------------------------
# Self-measurement. The claims this file makes ABOUT ITSELF are re-walked from
# the written bytes, because a self-report computed before the write describes a
# document that no longer exists (7.2.2, four measured instances).
# ---------------------------------------------------------------------------

FILENAME_SHAPED_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.(py|json|md|txt)\b")


def own_string_constants() -> list[str]:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    return [node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)]


def source_before_selftest() -> str:
    """This file's source up to the first selftest definition - the predicates.

    The split marker is assembled at runtime for the same reason the head-reader
    needle is: a literal would match itself.
    """
    marker = "def " + "selftest("
    return Path(__file__).read_text(encoding="utf-8").split(marker)[0]


# ---------------------------------------------------------------------------
# Selftest.
# ---------------------------------------------------------------------------

def selftest(product, ri, versioning, delivery, retention, register, v3, v2, v1) -> int:
    """Every claim this file makes, executed.

    A green run here is AUTHOR-SIDE evidence only. Section 7.8's bound is not
    discharged by more assertions from the same lane, and this file says so in
    its own banner rather than after a reviewer says it.
    """
    failed = 0
    partial: list[str] = []
    counts: dict[str, int] = {}
    executed_labels: set[str] = set()

    def check(bucket: str, ok: bool, label: str, detail: str = "") -> None:
        nonlocal failed
        counts[bucket] = counts.get(bucket, 0) + 1
        if ok:
            print(f"  ok      [{bucket}] {label}")
            if detail:
                print(f"            {detail}")
        else:
            failed += 1
            print(f"  FAILED  [{bucket}] {label}")
            print(f"            {detail}")

    must_pass, must_fail, escapes = decision_cases_v4(v3, v2, v1)

    print("repaired lane - states that MUST be accepted")
    for label, packet in must_pass:
        found = decision_lane_v4(packet, v3, v2, v1)
        executed_labels.add(label)
        check("accept", not found, label, "; ".join(found)[:240] if found else "")

    print("repaired lane - states that MUST fail, and the family that must "
          "catch each")
    for label, family, packet in must_fail:
        found = decision_lane_v4(packet, v3, v2, v1)
        executed_labels.add(label)
        hit = [f for f in found if family in f]
        check("reject", bool(hit), label,
              (f"expected a {family} finding; got "
               f"{[f.split(':')[0] for f in found] or 'NOTHING'}")
              if not hit else hit[0][:190])

    print("residuals - EXPECTED to escape; a residual that stops escaping is a "
          "FAILURE, because the published disclosure would be stale")
    for label, packet in escapes:
        found = [f for f in decision_lane_v4(packet, v3, v2, v1)
                 if f.startswith(FINDING_PREFIX)]
        executed_labels.add(label.split(" ")[0])
        check("residual", not found, label,
              f"NO LONGER ESCAPES: {found[0][:180]}" if found
              else "escapes this lane, as disclosed")

    print("non-vacuity - a family nothing can trip is decoration")
    exercised = {family for _, family, _ in must_fail}
    for family in ("AUTHORITY-VACUOUS", "AUTHORITY-SINGLE-SOURCE",
                   "AUTHORITY-UNATTRIBUTED", "AUTHORITY-AMBIENT",
                   "DATE-SINGLE-SOURCE", "DATE-UNATTRIBUTED",
                   "DECISION-REVERTED"):
        check("nonvacuity", family in exercised,
              f"family {family} is exercised by at least one must-fail case")

    print("gate independence - each limb must fire ALONE within its own "
          "coordinate, or it is not a limb")
    lone = {
        "AUTHORITY-SINGLE-SOURCE":
            _fixture(v3, v2, v1, decided=_row(v3, attributionRestated=v3._REMOVE)),
        "AUTHORITY-UNATTRIBUTED":
            _fixture(v3, v2, v1, decided=_row(
                v3,
                attributionProvenance="The authority chose the identity 'qbeltran'.",
                attributionRestated="Recorded again: qbeltran.")),
        "AUTHORITY-AMBIENT":
            _fixture(v3, v2, v1, decided=_renamed(v3, "Rutherford"),
                     purpose="Rutherford is named here for an unrelated reason."),
        "AUTHORITY-VACUOUS":
            _fixture(v3, v2, v1, decided=_row(v3, decidedBy="this and that")),
    }
    for family, packet in sorted(lone.items()):
        found = [f for f in decision_lane_v4(packet, v3, v2, v1)
                 if f.startswith(FINDING_PREFIX)]
        families = {f.split(":")[0].removeprefix(FINDING_PREFIX + "-") for f in found}
        authority = {f for f in families if f.startswith("AUTHORITY-")}
        check("gate", authority == {family},
              f"{family} is the ONLY authority-coordinate family on its own shape",
              f"authority families present: {sorted(authority)}; the date "
              f"coordinate reports separately: {sorted(families - authority)}")
    # The two coordinates are deliberately SYMMETRIC and the symmetry is
    # ASSERTED here rather than forbidden: substituting the date necessarily
    # leaves the authority unattributed too, because attribution is the JOINT
    # statement and moving either end breaks it. What must NOT happen is the
    # authority's OTHER limbs firing on a packet whose authority is untouched.
    date_only = _fixture(v3, v2, v1, decided=_row(v3, decidedOn="2027-03-04"))
    families = {f.split(":")[0].removeprefix(FINDING_PREFIX + "-")
                for f in decision_lane_v4(date_only, v3, v2, v1)
                if f.startswith(FINDING_PREFIX)}
    check("gate",
          {"DATE-SINGLE-SOURCE", "DATE-UNATTRIBUTED"} <= families
          and not ({"AUTHORITY-SINGLE-SOURCE", "AUTHORITY-AMBIENT",
                    "AUTHORITY-VACUOUS"} & families),
          "a substituted DATE fires both date-coordinate families, and of the "
          "authority's four limbs only the JOINT one - which is the symmetry, "
          "not a spurious duplicate",
          f"families present: {sorted(families)}")

    print("blocker 1 - the reviewer's measured escapes, and the controls that "
          "prove the gate was live rather than dead")
    live_row = product.get("decisions", {}).get(v2.RETENTION_DECISION_ID) \
        if isinstance(product, dict) else None
    if not isinstance(live_row, dict) or not isinstance(live_row.get("decidedBy"), str):
        partial.append(
            "the live packet does not carry a decided retention row with a "
            "string authority, so the blocker-1 matrix could not be run against "
            "live bytes and this run does NOT claim it")
    else:
        for candidate, must_catch in (
            ("retention", True), ("Phase", True), ("PURGED", True),
            ("tombstone", True), ("bounds", True), ("sfbreens", True),
            ("SFBREEN", True), ("the coordinator", True), ("jdoe", True),
            ("z", True), (live_row["decidedBy"], False),
        ):
            mutated = copy.deepcopy(product)
            mutated["decisions"][v2.RETENTION_DECISION_ID]["decidedBy"] = candidate
            found = decision_lane_v4(mutated, v3, v2, v1)
            caught = bool(found)
            check("blocker1", caught == must_catch,
                  f"decidedBy -> {candidate!r} must be "
                  f"{'CAUGHT' if must_catch else 'ACCEPTED'}",
                  (found[0][:150] if found else "no finding"))

    print("attribution discrimination sweep - the residual V2 disclosure, "
          "RECOMPUTED from the live packet, published with its definition, and "
          "gated on the two PROPERTIES rather than on the counts (7.2.2)")
    tokens, survivors, predecessor = attribution_discrimination(
        product, v3, v2, v1, deep=True)
    if not tokens:
        partial.append(
            "the live packet carries no decided retention row, so the "
            "discrimination sweep had no token population and this run does NOT "
            "publish it")
    else:
        print(f"    distinct 3+-character tokens in the live decision row  "
              f"{len(tokens)}")
        print(f"    surviving the PREDECESSOR's whole decision lane        "
              f"{len(predecessor)}")
        print(f"    surviving THIS file's lane                             "
              f"{len(survivors)}")
        print("    definition: each token is installed as decidedBy on a copy "
              "of the live packet")
        print("    and the lane is run; a token SURVIVES if the lane returns "
              "no finding.")
        check("sweep", set(survivors) < set(predecessor),
              "the surviving set is a STRICT SUBSET of the predecessor's - the "
              "gate was narrowed and nothing was loosened",
              f"{len(survivors)} of {len(predecessor)}; tokens this lane "
              f"admits that the predecessor rejects: "
              f"{sorted(set(survivors) - set(predecessor))}")
        recorded = product["decisions"][v2.RETENTION_DECISION_ID]["decidedBy"]
        check("sweep", recorded in survivors,
              "and the packet's ACTUAL recorded authority is among the "
              "survivors, so the gate is narrow without being a pin on today's "
              "value (7.10)",
              f"recorded authority {recorded!r}")
    executed_labels.add("attribution discrimination sweep")

    print("blocker 2 - the reversion of the LIVE decision must be caught, and "
          "by THIS lane rather than by any artifact on disk")
    if isinstance(product, dict) and isinstance(product.get("decisions"), dict) \
            and v2.RETENTION_DECISION_ID in product["decisions"]:
        reverted = copy.deepcopy(product)
        row = reverted["decisions"].pop(v2.RETENTION_DECISION_ID)
        pending = reverted.setdefault("pendingDecisions", {})
        if not isinstance(pending, dict):
            pending = {}
            reverted["pendingDecisions"] = pending
        pending[v2.RETENTION_DECISION_ID] = {
            "status": "BLOCKED_ON_PHASE_1A",
            "ruleWhilePending": ("No implementer may choose a retention default "
                                 "and no freeze may claim V10 resolved."),
            "question": row.get("question") if isinstance(row, dict) else None,
        }
        own = [f for f in decision_property_failures_v4(reverted, v3, v2)
               if "DECISION-REVERTED" in f]
        check("blocker2", bool(own),
              "reverting the live decided row is caught by the packet-only lane",
              f"{len(own)} reversion finding(s); first "
              f"{own[0][:150] if own else 'NONE'}")
        check("blocker2",
              not decision_property_failures_v4(product, v3, v2),
              "and the UNREVERTED live packet produces no finding from this "
              "lane, so the gate is not simply always-on")
    else:
        partial.append(
            "the live packet does not carry a decided retention row, so the "
            "reversion matrix could not be run against live bytes")

    print("banner honesty - the banner may name ONLY the gates that ran")
    for label, packet, expect_ran, expect_skipped in (
        ("decided packet", _fixture(v3, v2, v1, decided=_good_decision(v3)),
         {"attributive-corroboration", "decision-monotonicity"}, set()),
        ("pending packet",
         _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING)),
         {"decision-monotonicity"}, {"attributive-corroboration"}),
    ):
        ledger = GateLedger()
        decision_property_failures_v4(packet, v3, v2, ledger)
        ran = set(ledger.gate_names)
        skipped = {gate for gate, _ in ledger.skipped}
        check("banner", ran == expect_ran and skipped == expect_skipped,
              f"on a {label} the ledger records exactly the gates that executed",
              f"ran={sorted(ran)} skipped={sorted(skipped)}")
    ledger = GateLedger()
    broken = _fixture(v3, v2, v1, decided=_row(v3, decidedBy="Retention"))
    produced = decision_property_failures_v4(broken, v3, v2, ledger)
    check("banner",
          bool(produced) and "attributive-corroboration" not in ledger.gate_names
          and any(gate == "attributive-corroboration" for gate, _ in ledger.skipped),
          "a gate that RUNS AND FAILS registers no clause, so a failed gate can "
          "never contribute a sentence to a success banner",
          f"{len(produced)} finding(s); ran={sorted(ledger.gate_names)}; "
          f"withheld={sorted(gate for gate, _ in ledger.skipped)}")

    print("no regression - the PREDECESSOR's entire published case corpus, "
          "re-driven through this lane")
    p_pass, p_fail, p_escapes = v3.decision_cases(v1, v2)
    regressions = []
    for label, family, packet in p_fail:
        found = decision_lane_v4(packet, v3, v2, v1)
        if not any(family in f for f in found):
            regressions.append(label)
    check("noregression", not regressions,
          f"all {len(p_fail)} predecessor must-fail cases are still caught by "
          "their own family",
          f"regressions: {regressions}" if regressions else "0 regressions")
    still_pass, now_fail = [], []
    for label, packet in p_pass:
        (now_fail if decision_lane_v4(packet, v3, v2, v1) else still_pass).append(label)
    check("noregression", True,
          "MEASURED DELTA on the predecessor's must-PASS corpus",
          f"{len(still_pass)} of {len(p_pass)} still pass; {len(now_fail)} now "
          f"FAIL this lane, every one of them because its fixture names the "
          f"authority in exactly one other leaf - the single-source shape. "
          f"Reported, not smoothed: {now_fail}")
    check("noregression",
          all(any("SINGLE-SOURCE" in f
                  for f in decision_lane_v4(dict(packet), v3, v2, v1))
              for label, packet in p_pass if label in now_fail),
          "and every newly-failing predecessor fixture fails for THAT reason "
          "and no other")
    d1_case = [packet for label, packet in p_escapes if label.startswith("RESIDUAL-D1")]
    if d1_case:
        d1_found = [f for f in decision_lane_v4(d1_case[0], v3, v2, v1)
                    if f.startswith(FINDING_PREFIX)]
        check("noregression", bool(d1_found),
              "the predecessor's published residual D1 case is now CAUGHT, "
              "which is why D1 is WITHDRAWN rather than carried",
              d1_found[0][:180] if d1_found else "STILL ESCAPES")

    print("inherited demotion semantics - the predecessor closure's own evasion "
          "and control corpora, re-run unchanged (R1-R5 preserved)")
    dated = _fixture(v3, v2, v1, decided=_good_decision(v3))
    undated = _fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING))
    residual_escapes = 0
    for case in v2.DEMOTION_EVASIONS:
        label, name, doc, extras, expected, note = case[:6]
        packet = dated if len(case) > 6 and case[6] == "DATED" else undated
        standing, _reason = v2._standing_in(name, doc, extras, packet, v1)
        check("evasion", standing == expected, f"{label} -> {expected}",
              note if standing == expected else f"got {standing}")
        if label.startswith("RESIDUAL") and expected != "LIVE":
            residual_escapes += 1
    for case in v2.DEMOTION_CONTROLS:
        label, name, doc, extras = case[:4]
        expected = case[4] if len(case) > 4 else "LIVE"
        standing, _reason = v2._standing_in(name, doc, extras, undated, v1)
        check("control", standing == expected, f"CONTROL {label} -> {expected}",
              "" if standing == expected else f"got {standing}")
    check("evasion", residual_escapes == 4,
          "the four inherited demotion residuals R1-R4 all still escape",
          f"measured {residual_escapes}; if this moves, the printed residual "
          "width is stale")
    executed_labels.add("inherited demotion corpus")

    print("environment independence - a blinded run must give identical results")
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    sighted_f, sighted_o, _ = v2.classify(product, docs, unreadable, discovered, v1)
    original_reader = v1.head_named_artifacts
    try:
        v1.head_named_artifacts = lambda *a, **k: (set(), [])
        blind_f, blind_o, _ = v2.classify(product, docs, unreadable, discovered, v1)
    finally:
        v1.head_named_artifacts = original_reader
    check("environment", sighted_f == blind_f and sighted_o == blind_o,
          "head documents unreadable -> identical findings AND observations",
          f"findings {len(sighted_f)}=={len(blind_f)}, "
          f"observations {len(sighted_o)}=={len(blind_o)}")
    needle = "head_named" + "_artifacts"
    predicates = source_before_selftest()
    check("environment", needle not in predicates,
          "no predicate defined before --selftest reads a head document",
          f"{len(predicates)} bytes of predicate source scanned")
    probe = {"reviewer": 1, "adjudication": 1, "independence": 1,
             "reviewBinding": 1, "verdict": 1, "decision": 1, "outcome": 1}
    witnesses = {v2.has_reviewer_role(probe) for _ in range(64)} | \
                {v2.has_verdict_shape(probe) for _ in range(64)}
    check("environment", len(witnesses) == 2,
          "the printed derivation WITNESS is reproducible run to run",
          f"a document with 7 competing witness keys yields {sorted(witnesses)}; "
          "the predecessor's sorted-iteration wrapper is carried through this "
          "file unchanged (7.2: a verdict binds bytes AND an environment)")
    provenance = import_provenance_failures()
    check("environment", not provenance,
          "environment: import provenance",
          "no module in this process was loaded from the directory this "
          "instrument runs in, other than the pinned predecessor itself"
          if not provenance else provenance[0])
    executed_labels.add("environment: import provenance")
    check("environment", sys.flags.isolated == 1 and sys.flags.dont_write_bytecode,
          "the invocation guard's own precondition holds in this process",
          f"isolated={sys.flags.isolated} dont_write_bytecode="
          f"{bool(sys.flags.dont_write_bytecode)}")

    print("hostile input - every shape must produce a NAMED outcome, never a "
          "traceback (litmus D-6)")
    for label, shape in (tuple(v3.hostile_shapes(v1, v2))
                         + tuple(hostile_shapes_v4(v3, v2, v1))):
        try:
            found = decision_lane_v4(shape, v3, v2, v1)
            ok = isinstance(found, list) and all(isinstance(f, str) for f in found)
            detail = f"{len(found)} finding(s)"
        except Exception as exc:                       # noqa: BLE001 - measured
            ok = False
            detail = f"RAISED {type(exc).__name__}: {exc}"
        check("hostile", ok, label, detail)

    print("input discipline - a MISSING input and a WRONG subject must never "
          "print the same (7.8.1)")
    subject_findings, missing = partition_input_unavailability([
        "PD-RT-BINDING: cannot read exact EP5/RT10 candidate (FileNotFoundError)",
        "PD-RT-BINDING: live retention bytes hash abc differ from exact v10 digest",
        "PD-EP-BINDING: cannot parse exact retention candidate (JSONDecodeError)",
    ])
    check("input", len(subject_findings) == 1 and len(missing) == 2,
          "input discipline: an absent optional input skips its class by name",
          f"{len(subject_findings)} finding(s) about the subject, "
          f"{len(missing)} unavailable-input outcome(s)")
    check("input",
          not partition_input_unavailability(v1.retention_binding_failures())[1],
          "and on THIS tree the class actually ran, so the run does not claim "
          "a skip it did not have")
    executed_labels.add("input discipline: an absent optional input skips its "
                        "class by name")

    print("self-measurement - the claims this file makes ABOUT ITSELF, "
          "re-walked from the written bytes")
    constants = own_string_constants()
    filename_shaped = sorted({m.group(0) for value in constants
                              for m in FILENAME_SHAPED_RE.finditer(value)})
    check("self", filename_shaped == [PREDECESSOR_BINDING["path"]],
          "exactly ONE filename-shaped literal, and it is the pin",
          f"found {filename_shaped}")
    corpus_names = {name for name, _ in docs}
    named = sorted(n for n in corpus_names
                   if any(n in value for value in constants))
    check("self", not named, "zero corpus artifacts are named in this source",
          f"named: {named}")
    rows = residual_registry(v3)
    ungated = [tag for tag, _, _, gate in rows if gate is None]
    dangling = sorted({gate for _, _, _, gate in rows
                       if gate is not None and gate not in executed_labels
                       and not any(gate in label for label in executed_labels)})
    check("self", not dangling,
          "every residual claiming to be GATED names a case this suite ran",
          f"dangling gate labels: {dangling}")
    gated_count = sum(1 for row in rows if row[3] is not None)
    check("self", gated_count + len(ungated) == len(rows),
          f"the published split is arithmetic: {gated_count} gated + "
          f"{len(ungated)} not gated = {len(rows)} residuals")

    print()
    print("selftest buckets: " + ", ".join(
        f"{bucket} {count}" for bucket, count in sorted(counts.items())))
    total = sum(counts.values())
    if failed:
        print(f"SELFTEST FAILED - {failed} of {total} checks failed")
        return EXIT_FINDINGS
    if partial:
        print(f"SELFTEST-PARTIAL - {total} checks executed, 0 failed, but:")
        for item in partial:
            print(f"  - {item}")
        print("A partial run is not a green run.")
        return EXIT_REFUSED
    print(f"SELFTEST OK - {total} checks executed, 0 failed. This is AUTHOR-SIDE "
          "evidence: the same reading produced both the repair and its suite.")
    return EXIT_OK


# ---------------------------------------------------------------------------
# Reporting and the banner.
# ---------------------------------------------------------------------------

def banner_lines(ledger: GateLedger, report: dict, v1) -> list[str]:
    """The success banner, assembled from what RAN. Nothing here is a literal.

    Section 7.8.1's rule, turned on an instrument's own output: a measurement
    that was not taken may not be printed as though it had been, and a gate that
    did not run must be visible as such rather than absent.
    """
    lines = [
        f"product dispositions OK - {len(v1.EXPECTED_CHOICES)} non-retention "
        "choices bound; the retention decision is in exactly one valid state,"
    ]
    for clause in ledger.clauses():
        lines.append(f"  * {clause}")
    lines.append(
        f"  * no artifact with standing ({report['artifactsLive']} of "
        f"{report['artifactsParsed']} scanned) asserts a product decision the "
        f"binding packet does not carry; {report['historicalObservations']} such "
        f"assertion(s) remain in {report['conflictingArtifactsHistorical']} "
        "historical artifact(s), listed above")
    if ledger.skipped:
        lines.append(
            "  GATES THAT DID NOT RUN, named because a banner may never report "
            "a gate as run when it did not:")
        for gate, why in ledger.skipped:
            lines.append(f"    - {gate}: {why}")
    return lines


def _run(argv: list[str] | None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    unknown = [a for a in args if a not in DECLARED_FLAGS]
    if unknown:
        print(f"usage: {Path(__file__).name} [--selftest]")
        print(f"  unrecognised argument(s): {' '.join(unknown)}")
        return EXIT_USAGE
    want_selftest = "--selftest" in args

    provenance = import_provenance_failures()
    if provenance:
        print("REFUSING to run: an import came from the directory this "
              "instrument runs in")
        for item in provenance:
            print(f"  - {item}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    try:
        v3 = _load_predecessor()
        v2 = v3._load_predecessor()
        v1 = v2._load_predecessor()
    except RuntimeError as exc:
        print("REFUSING to run: the pinned predecessor closure is dirty")
        print(f"  - {exc}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    inputs: dict[str, object] = {}
    refusals: list[str] = []
    for key, path, required in (
        ("product", v1.PRODUCT_PATH, True),
        ("ri", v1.RI_PATH, True),
        ("versioning", v1.VERSIONING_PATH, True),
        ("delivery", v1.DELIVERY_PATH, True),
        ("register", v1.REGISTER_PATH, True),
        ("retention", v1.RETENTION_PATH, False),
    ):
        value, problem = v3._load(path, required)
        if problem:
            refusals.append(problem)
        inputs[key] = value
    if refusals:
        print("REFUSING to run: the checker's own base is dirty")
        for problem in refusals:
            print(f"  - {problem}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    product = inputs["product"]
    ri, versioning, delivery = inputs["ri"], inputs["versioning"], inputs["delivery"]
    retention, register = inputs["retention"], inputs["register"]

    print(f"successor to {PREDECESSOR_BINDING['path']}"
          f"@sha256:{PREDECESSOR_BINDING['sha256']} "
          f"({PREDECESSOR_BINDING['bytes']} bytes, hash-verified, executed as a "
          "runtime input under freeze 7.3; it hash-verifies its own predecessor, "
          "which verifies its own, so one pin covers a four-deep closure)")
    print("invocation: ISOLATED, NO-BYTECODE - the script's directory is not on "
          "the import path, so no file beside this one can shadow a module the "
          "pin chain depends on")

    if want_selftest:
        return selftest(product, ri, versioning, delivery, retention, register,
                        v3, v2, v1)

    ledger = GateLedger()
    join = v1.retention_binding_failures()
    failures, unavailable = partition_input_unavailability(join)
    if unavailable:
        ledger.not_executed(
            "retention-binding join",
            "its input could not be read, so the class DID NOT RUN and is "
            "skipped BY NAME rather than reported as a finding about the "
            "packet: " + "; ".join(unavailable))
    else:
        ledger.executed(
            "retention-binding join",
            f"consumed {v1.EVALUATION_PROOF_BINDING['path']}@sha256:"
            f"{v1.EVALUATION_PROOF_BINDING['sha256']} -> "
            f"{v1.RETENTION_BINDING['path']}@sha256:"
            f"{v1.RETENTION_BINDING['sha256']}")
    failures.extend(validate_v4(product, ri, versioning, delivery, retention,
                                v3, v2, v1, ledger))
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    assertion_failures, observations, report = v2.classify(
        product, docs, unreadable, discovered, v1)
    failures.extend(assertion_failures)
    _heads, head_docs = v1.head_named_artifacts(HERE)
    notice_lines = v3.notices(product, docs, v2)
    tokens, survivors, _ = attribution_discrimination(product, v3, v2, v1)
    if tokens:
        notice_lines.append(
            f"{FINDING_PREFIX}-ATTRIBUTION-DISCRIMINATION (NOTICE): of the "
            f"{len(tokens)} distinct 3-or-more-character tokens in the live "
            f"decision row, {len(survivors)} survive as a candidate authority. "
            "This is residual V2's disclosure, RECOMPUTED FROM THE LIVE PACKET "
            "on this run rather than transcribed, so it cannot go stale. It is "
            "a notice and can never change an exit code")

    for line in v3.format_report(report, head_docs, notice_lines):
        if line.startswith("HONEST LIMITS"):
            break
        print(line)
    for line in format_limits(residual_registry(v3)):
        print(line)
    if observations:
        print("HISTORICAL OBSERVATIONS - a product-decision assertion conflicting "
              "with the binding")
        print("packet, in an artifact with no standing to make it. Not a finding: "
              "freeze 7.2")
        print("forbids editing reviewed bytes and 7.2.1 forbids repairing a "
              "review at all, so")
        print("these cannot be repaired. Reported in full, never dropped - a "
              "forgery buys a")
        print("green exit code, never silence:")
        for line in observations:
            print(f"  {line}")
    if failures:
        print("product dispositions INVALID")
        for failure in failures:
            print(f"  - {failure}")
        if ledger.skipped:
            print("AND AT LEAST ONE CLASS DID NOT RUN, so the finding list "
                  "above is not a complete account:")
            for gate, why in ledger.skipped:
                print(f"  ! {gate}: {why}")
        return EXIT_FINDINGS
    for line in banner_lines(ledger, report, v1):
        print(line)
    if any(gate == "retention-binding join" for gate, _ in ledger.skipped):
        print("CLASS-SKIPPED - every class that ran is green and at least one "
              "class DID NOT RUN.")
        print("This run does NOT certify the skipped class. Exit 4.")
        return EXIT_CLASS_SKIPPED
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    """A CRASH MUST NOT READ AS A FINDING (litmus D-6).

    Exit 0 green, 1 findings, 2 bad invocation, 3 nothing ran, 4 green but at
    least one CLASS did not run and is named. An unexpected exception is a
    did-not-run, NOT a finding and NOT a pass: it is named, its type is printed,
    and it takes the code that means "this run certifies nothing".
    """
    try:
        return _run(argv)
    except SystemExit:
        raise
    except BaseException as exc:                       # noqa: BLE001 - by design
        print("REFUSING to certify: this instrument raised while running")
        print(f"  - {type(exc).__name__}: {str(exc)[:400]}")
        print("SCAN-NOT-RUN")
        return EXIT_REFUSED


if __name__ == "__main__":
    raise SystemExit(main())
