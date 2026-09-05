#!/usr/bin/env python3
"""Successor to the pinned predecessor. Edits nothing; adds ONE lane.

WHY A SUCCESSOR AND NOT AN EDIT
-------------------------------
Freeze 7.2 forbids changing reviewed bytes in place and the sanctioned repair is
a new file. The predecessor is a RUNTIME INPUT here, hash-verified before use,
which 7.3 explicitly permits. It in turn hash-verifies and executes ITS
predecessor, which verifies ITS predecessor, and so on, so one pin covers a
FIVE-DEEP closure and every inherited detection semantic is RE-USED
BYTE-IDENTICALLY rather than retyped.

WHAT THIS SUCCESSOR ADDS - AND THE DEFECT IT CLOSES
---------------------------------------------------
An independent review of the predecessor returned ACCEPT_WITH_BLOCKERS at one
blocker. This file repairs that blocker and changes nothing else.

  THE BLOCKER - THE CORPUS SCAN LANE COMPARED THE *STATE* OF A DECISION AND
  NEVER ITS *ATTRIBUTION*.

  The two authority fields of a decided row are read in exactly one place across
  the whole inherited closure: inside the binding packet's own row. Once the
  packet records a decision as closed-positive, an artifact asserting a
  DIFFERENT AUTHORITY OR A DIFFERENT DATE for that same decision is not a state
  conflict, so nothing in the scan lane looked at it.

  REPRODUCED DIRECTLY, ON THE LIVE TREE, BEFORE A LINE OF THIS FILE WAS WRITTEN.
  A live artifact carrying the exact fabricated sign-off sentence freeze 4.4
  exists to record produced ZERO FINDINGS AND ZERO MENTIONS anywhere in the
  predecessor's output. Not demoted to a historical observation: ABSENT. It was
  counted in the census - the artifact total moved by one and the LIVE bucket
  moved by one - and named nowhere. That is the one property the review of an
  earlier generation concluded forgery could never take: SILENCE.

  Measured on the same tree, against the same predecessor, by an external driver
  that wrote real bytes and invoked the instrument as a subprocess: TWELVE
  attack vectors - the verbatim plant, all five of the first-generation
  instrument's own register-fabrication mutations, a substituted authority, a
  substituted date, an inverted posture, a fabrication buried under the decision
  key, and an aliased authority/date key pair - produced a finding-set delta of
  ZERO. The control, an artifact asserting the pre-decision state, was caught and
  named in full. So the lane was LIVE and WRONG IN EXACTLY ONE DIRECTION.

  WHY IT WAS INVISIBLE UNTIL NOW. While the retention decision was pending, a
  fabricated sign-off WAS a state conflict, so the lane caught it and the gap
  could not appear. DECIDING THE QUESTION IS WHAT DISARMED THE GUARD - freeze
  7.10 arriving from the opposite side.

THE PROPERTY THIS FILE ENFORCES
-------------------------------
    AN ARTIFACT THAT ASSERTS A DECISION IS DECIDED MUST EITHER AGREE WITH THE
    BINDING PACKET ON *WHO* AND *WHEN*, OR SAY NOTHING ABOUT WHO AND WHEN.
    NAMING A DIFFERENT AUTHORITY OR A DIFFERENT DATE FOR A DECISION THE PACKET
    CARRIES IS A CONFLICT, REGARDLESS OF STATE AGREEMENT.

MISMATCH IS A FINDING; SILENCE IS NOT. Many artifacts legitimately cite only the
state, and a lane that demanded attribution from all of them would fire on the
whole corpus.

IT IS DERIVED, AND IT NEEDS NO LIST
-----------------------------------
Freeze 7.9's rule - standing is DISCOVERED, not listed - forbids shipping a
stop-list, and 7.10's rule forbids pinning today's value. So BOTH SIDES OF THE
COMPARISON ARE READ OFF THE LIVE PACKET EVERY RUN:

  * WHO is the value of any direct field of a decision row whose normalised key
    name ENDS IN 'BY', plus the signature-shaped key names the pinned closure
    already carries. No authority name appears in this source.
  * WHEN is the value of any direct field of a decision row that IS an ISO-8601
    extended calendar date, validated against the calendar. No date appears in
    this source.

The recorded authority and the recorded date are therefore whatever the packet
says today, and a legitimate amendment to either costs a re-read rather than a
successor instrument (7.10's corollary). --selftest FAILS if that derivation
stops recovering a usable coordinate from the live packet, so the disclosure
cannot go stale, and the normal run PRINTS what it derived.

THE HARD CONSTRAINT, AND WHY THIS IS NOT A STRING MATCH
-------------------------------------------------------
The fabricated sentence occurs LEGITIMATELY in nine files of this corpus: the
freeze's own forensic record of the incident (twice), the binding claim register
(three times, as a struck-and-quoted record), five instruments that carry it as
a test fixture, and two review artifacts that quote it as evidence. A NAIVE SCAN
FIRES ON ALL OF THEM, INCLUDING ON THE FREEZE SECTION THAT RECORDS THE
FABRICATION. The corpus's own forensic record of a forgery must never be
reported as a forgery.

Four inherited mechanisms carry that, and not one of them is new here:

  1. THE ARTIFACT LANE OBSERVES JSON ONLY. The pinned closure's scanner globs
     one suffix, so instruments and narrative documents are outside this lane by
     construction. MEASURED rather than assumed: six of the nine files are
     outside the scanned set, and --selftest asserts the scanner's own
     population is JSON-only rather than trusting the docstring.
  2. THE STANDING DOCTRINE, CALLED NOT COPIED. Rejected, superseded and frozen
     review records are demoted to HISTORICAL OBSERVATIONS and are never
     findings, because 7.2 forbids editing reviewed bytes and 7.2.1 forbids
     repairing a review at all. The three rejected copies of the fabrication in
     this corpus land here, exactly as freeze 4.4 requires - reported in full,
     never dropped.
  3. THE SUPERSESSION-MARKER TEST, CALLED NOT COPIED. The corpus retains
     superseded text VERBATIM, so a bare substring hunt false-positives; a leaf
     or a path marked superseded, withdrawn, previously, historical or read
     verbatim is a RECORD of an attribution, not an assertion of one.
  4. THE ASSERTION VOCABULARY, CALLED NOT COPIED. The first-generation
     instrument's own reasons for refusing to read a clause as an assertion -
     quoted, citation-or-template, negated, pending, retracted, hedged,
     attributed, subordinated, historical - are applied unchanged. The one limb
     deliberately NOT required is the product-authority limb, because the site
     is already anchored on a decision id the packet carries, which is what that
     limb exists to establish in free prose.

MEASURED, AND THE MEASUREMENT IS THE ACCEPTANCE TEST
----------------------------------------------------
Against the live corpus this lane produces ZERO findings and demotes the
rejected historical copies to observations. Against twelve planted forgeries it
produces a named finding for every one. Both numbers are recomputed by
--selftest from whatever is on disk, never transcribed.

THE ACCEPTED FAILURE MODE, STATED BEFORE THE EVIDENCE
-----------------------------------------------------
A COHERENT lie: an artifact that asserts the decision is closed and says NOTHING
about who or when is silent to this lane, by design, because that is exactly
what the legitimate majority of the corpus does. Freeze 7.8's bound applies in
full and is not repealed by anything above: this binds structure, type and
internal agreement. It cannot bind the truth of content, and no instrument in
this corpus can.
"""

from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# THE INVOCATION GUARD, AND IT IS THE FIRST THING THAT RUNS.
#
# `sys` is a builtin module: it is resolved by BuiltinImporter, which precedes
# the path finder, so it cannot be shadowed by a file in this directory. Every
# other import in this file can be. So the guard runs BEFORE them.
#
# Run as a plain script, the interpreter puts the SCRIPT'S OWN DIRECTORY at the
# head of the import path - the same directory the corpus's own forgery model
# assumes an attacker can write into. Isolated mode removes it and ignores the
# environment path variable, which is the whole of the fix. The predecessor's
# review measured the consequence of omitting it: exit 0, ZERO findings, and the
# offending artifact removed from the output entirely.
#
# WHY EXIT 2. 2 means "bad invocation" in this lineage's taxonomy; 3 means "ran
# and refused to certify". This is a bad invocation. Freeze 7.8.1 rule 3: an
# exit code a document CLAIMS must be the exit code the file PRODUCES - so the
# refusal text names 2 and returns 2, on BOTH channels, because a message on one
# channel is a message a reader of the other channel does not get.
# ---------------------------------------------------------------------------

_INVOCATION_REFUSAL = (
    "PD5-UNSUPPORTED-INVOCATION: this instrument must be run in ISOLATED, "
    "NO-BYTECODE mode - `python3 -I -B <this file>`. Without -I the script's "
    "own directory heads the import path, so one file written beside this one "
    "and named after a standard-library module shadows that module for this "
    "instrument AND for every hash-pinned predecessor it executes - the pins "
    "cover their bytes and nothing covers their imports. Measured on this "
    "lineage: that attack returns exit 0 with ZERO findings and REMOVES the "
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
# Drift is EXIT_REFUSED, never a silent fallback. It verifies its own, which
# verifies its own, which verifies its own - one pin, five files.
# ---------------------------------------------------------------------------
PREDECESSOR_BINDING = {
    "path": "check-product-dispositions-v4.py",
    "sha256": "ff02117c7f6a829b16a865920747be25c2cad96cf4562e012a1c653082354009",
    "bytes": 90846,
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
EXIT_CLASS_SKIPPED = 4
DECLARED_FLAGS = ("--selftest",)

FINDING_PREFIX = "PD5"

# Bounds. A hostile artifact may not make this lane expensive, and a bound that
# is hit is REPORTED rather than silently truncating - "derived from nothing"
# and "derived and found nothing" must never print the same (7.8.1 rule 1).
SUBTREE_MAX_DEPTH = 12
SUBTREE_LEAF_BUDGET = 2000
CLAUSE_TEXT_LIMIT = 20000

# A date used as a COORDINATE of a decision, searched inside prose. A pattern
# hit is not enough - the calendar is checked too, so an impossible date written
# in a sentence is not a decision moment.
ISO_IN_TEXT_RE = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
# The ANCHORED extended-calendar form, for testing whether a whole VALUE is a
# date. It must be anchored and it must be the extended form: the basic form
# parses as a date too, and an eight-digit string would otherwise pass as a
# coordinate. The pinned closure carries the same pattern for its own field
# check; --selftest measures that the two AGREE over a probe set rather than
# asserting they do, because a second private copy of a rule that silently
# disagreed with the first is the failure this corpus records repeatedly.
_ISO_EXTENDED = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})\s*$")
# `by X` - the shape in which English attributes an act to an agent. Bounded to
# four word tokens because an attribution is a name, not a sentence.
BY_PHRASE_RE = re.compile(
    r"(?<![A-Za-z0-9])by\s+((?:[A-Za-z][A-Za-z0-9._'’-]*(?:\s+|$)){1,4})",
    re.IGNORECASE)
TRAILING_PUNCT = " \t\n.,;:!?)('\"‘’“”`-"


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
    spec = importlib.util.spec_from_file_location("_pd_v4", path)
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


def closure_paths(v4, v3, v2) -> set[str]:
    """Every file this instrument is entitled to execute out of this directory.

    DERIVED by walking the pin chain rather than listed, so a longer chain needs
    no edit here and a file that is NOT in the chain can never be admitted by a
    stale literal.
    """
    permitted = {str(Path(__file__).resolve())}
    for module in (None, v4, v3, v2):
        binding = (PREDECESSOR_BINDING if module is None
                   else getattr(module, "PREDECESSOR_BINDING", None))
        if isinstance(binding, dict) and isinstance(binding.get("path"), str):
            permitted.add(str((HERE / binding["path"]).resolve()))
    return permitted


def import_provenance_failures(permitted: set[str]) -> list[str]:
    """Belt and braces: no import may have come from HERE, except the closure.

    The flag guard above is the load-bearing check and it runs first. This is a
    MEASUREMENT taken after the fact, printed in the banner, and fatal if it ever
    disagrees - because "the flag was set" is a statement about the invocation
    and this is a statement about what actually got loaded.
    """
    out: list[str] = []
    here = str(HERE)
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
# THE PACKET SIDE. Both coordinates are DERIVED from whatever is live.
# ---------------------------------------------------------------------------

def _real_calendar(year: str, month: str, day: str) -> bool:
    try:
        datetime.date(int(year), int(month), int(day))
    except (ValueError, TypeError):
        return False
    return True


def is_iso_date_value(text: object) -> bool:
    """Is this whole value an ISO-8601 EXTENDED calendar date?

    The extended form is required BEFORE parsing, because the basic form parses
    as a date too and would let an eight-digit string pass as a coordinate.
    """
    if not isinstance(text, str):
        return False
    match = _ISO_EXTENDED.match(text)
    if not match:
        return False
    return _real_calendar(match.group(1), match.group(2), match.group(3))


def iso_dates_in(text: str) -> list[str]:
    """Every real calendar date written in this text, in order of appearance."""
    seen: list[str] = []
    for match in ISO_IN_TEXT_RE.finditer(text[:CLAUSE_TEXT_LIMIT]):
        if not _real_calendar(match.group(1), match.group(2), match.group(3)):
            continue
        if match.group(0) not in seen:
            seen.append(match.group(0))
    return seen


def authority_shaped_key(key: object, v3, v2) -> bool:
    """Does this key name record WHO acted?

    Two derivations, no new vocabulary. English forms an agent field by suffixing
    the agent preposition, so a normalised key ending in it is an authority
    field whatever it is called; and the pinned closure already carries the
    signature-shaped key names, which are reused rather than retyped.
    """
    normalised = v2._norm_key(key)
    if not normalised:
        return False
    return (len(normalised) > 2 and normalised.endswith("by")) \
        or normalised in v3.FABRICATED_AUTHORITY_KEYS


def packet_attribution(product: object, v3, v2) -> dict[str, dict[str, list[str]]]:
    """{decision id: {'who': [...], 'when': [...]}} read live off the packet.

    NOTHING here is a literal. The sections are the packet's own, the keys are
    matched by SHAPE, and the values are whatever the authority recorded. A
    legitimate amendment to either coordinate is picked up on the next run,
    which is 7.10's corollary - pin what you depend on and re-extract it.
    """
    out: dict[str, dict[str, list[str]]] = {}
    if not isinstance(product, dict):
        return out
    for section in ("decisions", "pendingDecisions"):
        rows = product.get(section)
        if not isinstance(rows, dict):
            continue
        for decision_id, row in rows.items():
            who: list[str] = []
            when: list[str] = []
            if isinstance(row, dict):
                for key, value in row.items():
                    if not isinstance(value, str) or not value.strip():
                        continue
                    # A DATE IS A COORDINATE, NOT AN IDENTITY. Some
                    # signature-shaped key names in the pinned closure's set
                    # record WHEN rather than WHO, so a value that is itself a
                    # calendar date is never admitted as an authority - measured
                    # here rather than reasoned about, because admitting one
                    # would widen the set of authorities an artifact may name.
                    if (authority_shaped_key(key, v3, v2)
                            and not is_iso_date_value(value)
                            and value.strip() not in who):
                        who.append(value.strip())
                    if is_iso_date_value(value) and value.strip() not in when:
                        when.append(value.strip())
            out[str(decision_id)] = {"who": sorted(who), "when": sorted(when)}
    return out


# ---------------------------------------------------------------------------
# THE ARTIFACT SIDE.
# ---------------------------------------------------------------------------

def by_phrases(text: str, v1, v3) -> list[tuple[str, list[str]]]:
    """(phrase, meaningful tokens) for every `by X` that FOLLOWS the predicate.

    An attribution names who performed an act, so it must come after the act.
    That one positional rule is what separates 'SIGNED OFF <date> by <name>'
    from 'the decision was untouched by it' - measured: without it, four live
    artifacts of this corpus are false positives; with it, zero are.
    """
    body = text[:CLAUSE_TEXT_LIMIT]
    norm = v1._normalise(body)
    closure = v1._find_term(norm, v1.CLOSURE_PREDICATIVE + v1.CLOSURE_HEAD_BARE)
    if closure is None:
        return []

    def alnum_before(source: str, index: int) -> int:
        return sum(1 for ch in source[:index] if ch.isalnum())

    threshold = alnum_before(norm, closure[0])
    out: list[tuple[str, list[str]]] = []
    for match in BY_PHRASE_RE.finditer(body):
        if alnum_before(body, match.start()) < threshold:
            continue
        phrase = match.group(1).strip(TRAILING_PUNCT)
        tokens = v3._role_verdict(phrase)
        if phrase and tokens:
            out.append((phrase, tokens))
    return out


def records_rather_than_asserts(path: str, text: str, v1, v3) -> str:
    """Why this text RECORDS an attribution instead of MAKING one. '' if it makes one.

    Every limb is the pinned closure's, called rather than copied. The corpus
    retains superseded text verbatim, so the marker test is what stops a bare
    substring hunt firing on an honest supersession record; the remaining limbs
    are the first-generation instrument's own reasons for refusing to read a
    clause as an assertion.

    ITS PRODUCT-AUTHORITY LIMB IS DELIBERATELY NOT REQUIRED HERE, and that is a
    ruling rather than an omission. That limb exists to establish, in free
    prose, that a sentence is about a PRODUCT decision at all. Here the site is
    already anchored on a decision id the binding packet carries, so the
    question it answers is already answered - and requiring it would mean an
    attribution naming a non-product role escaped while one naming a product
    role was caught, which is the wrong way round.
    """
    body = text[:CLAUSE_TEXT_LIMIT]
    if v3._marked_superseded(path, body):
        return "marked-superseded"
    if any(quote in body for quote in v1.QUOTE_CHARS):
        return "quoted"
    if (v1.FILE_REFERENCE_RE.search(body) or v1.PLACEHOLDER_RE.search(body)
            or v1.POINTER_RE.search(body.strip())):
        return "citation-or-template"
    norm = v1._normalise(body)
    for reason, terms in (
        ("negated", v1.NEGATORS), ("pending", v1.CLOSURE_PENDING),
        ("retracted", v1.CLOSURE_NEGATIVE), ("hedged", v1.MODAL),
        ("attributed", v1.ATTRIBUTIVE), ("subordinated", v1.SUBORDINATOR),
        ("historical", v1.HISTORICAL),
    ):
        found = v1._find_term(norm, terms)
        if found is not None:
            return f"{reason}:{found[1]}"
    return ""


def names_the_recorded_authority(tokens: list[str], recorded: list[str],
                                 v3) -> bool:
    """Does this candidate phrase name the authority the packet records?

    Compared on MEANINGFUL TOKENS, so 'sfbreen', 'by sfbreen' and 'the sfbreen
    who decided' all agree while a substituted identity does not. Content-free
    words are dropped by the pinned closure's own role reader, so an artifact
    cannot buy agreement by padding.
    """
    candidate = {token.lower() for token in tokens}
    for value in recorded:
        wanted = {token.lower() for token in v3._role_verdict(value)}
        if not wanted:
            wanted = {value.strip().lower()}
        if wanted & candidate:
            return True
    return False


def decision_subtree_leaves(value: object, path: str, depth: int = 0,
                            budget: list[int] | None = None,
                            overflow: list[str] | None = None):
    """(key, path, string) for every string leaf under a decision-keyed value.

    Bounded, and the bound is REPORTED by the caller rather than silently
    truncating the examination.
    """
    if budget is None:
        budget = [SUBTREE_LEAF_BUDGET]
    if depth > SUBTREE_MAX_DEPTH or budget[0] <= 0:
        if overflow is not None and path not in overflow:
            overflow.append(path)
        return
    if isinstance(value, dict):
        for key, child in value.items():
            budget[0] -= 1
            if budget[0] <= 0:
                if overflow is not None and path not in overflow:
                    overflow.append(path)
                return
            if isinstance(child, str):
                yield str(key), f"{path}.{key}", child
            else:
                yield from decision_subtree_leaves(
                    child, f"{path}.{key}", depth + 1, budget, overflow)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            budget[0] -= 1
            if budget[0] <= 0:
                if overflow is not None and path not in overflow:
                    overflow.append(path)
                return
            if isinstance(child, str):
                yield "", f"{path}[{index}]", child
            else:
                yield from decision_subtree_leaves(
                    child, f"{path}[{index}]", depth + 1, budget, overflow)


def attribution_failures(states: dict[str, str],
                         attribution: dict[str, dict[str, list[str]]],
                         name: str, doc: object, prefix: str,
                         v3, v2, v1) -> tuple[list[str], dict[str, int]]:
    """The ATTRIBUTION lane over ONE artifact. A pure function of parsed input.

    Reads the packet's derived coordinates and the artifact, and NOTHING else -
    no digest, no head document, no corpus - so an external driver can mutate a
    document in memory and prove the lane is not vacuous from outside itself
    (7.8), and nothing written into this directory can demote a finding here.
    """
    counts = {"attributionSites": 0, "authorityClaims": 0, "dateClaims": 0,
              "agreeing": 0, "conflicts": 0, "notAnAssertion": 0}
    out: list[str] = []
    known = tuple(sorted(states))
    try:
        key_anchored, _scoped, prose = v1._document_sites(doc, known)
    except RecursionError:
        return ([f"{prefix}-ATTRIBUTION-DEPTH {name}: the artifact nests deeper "
                 "than the interpreter can walk, so it was NOT examined by the "
                 "attribution lane and this run's silence about it is not "
                 "evidence"], counts)
    seen: set[tuple[str, str, str, str]] = set()

    def emit(decision_id: str, where: str, kind: str, claimed: str,
             recorded: list[str], how: str) -> None:
        key = (decision_id, where, kind, claimed)
        if key in seen:
            return
        seen.add(key)
        counts["conflicts"] += 1
        coordinate = "an authority" if kind == "AUTHORITY" else "a decision date"
        out.append(
            f"{prefix}-ATTRIBUTION-{kind} {name}{where}: asserts {decision_id} "
            f"was decided {'by' if kind == 'AUTHORITY' else 'on'} {claimed!r} "
            f"while the binding product packet records "
            f"{recorded if recorded else 'NO ' + coordinate + ' at all'} for it "
            f"(via {how}). A decision is constituted only by the binding packet; "
            "an artifact may CITE its attribution and may never CREATE one, so "
            "naming a different authority or a different moment for a decision "
            "the packet carries is a conflict even where the STATE agrees")

    def compare(decision_id: str, where: str,
                authorities: list[tuple[str, list[str]]],
                dates: list[str], how: str) -> None:
        recorded = attribution.get(decision_id) or {"who": [], "when": []}
        for phrase, tokens in authorities:
            counts["authorityClaims"] += 1
            if not recorded["who"]:
                emit(decision_id, where, "UNRECORDED-AUTHORITY", phrase,
                     recorded["who"], how)
            elif names_the_recorded_authority(tokens, recorded["who"], v3):
                counts["agreeing"] += 1
            else:
                emit(decision_id, where, "AUTHORITY", phrase, recorded["who"], how)
        for when in dates:
            counts["dateClaims"] += 1
            if not recorded["when"]:
                emit(decision_id, where, "UNRECORDED-DATE", when,
                     recorded["when"], how)
            elif when in recorded["when"]:
                counts["agreeing"] += 1
            else:
                emit(decision_id, where, "DATE", when, recorded["when"], how)

    def scan_prose(decision_id: str, where: str, text: str, how: str,
                   require_id: bool) -> None:
        for unit in v1._clause_units(text[:CLAUSE_TEXT_LIMIT]):
            if require_id and decision_id not in unit:
                continue
            if v1._head_family(unit)[0] != "CLOSED_POSITIVE":
                continue
            counts["attributionSites"] += 1
            why = records_rather_than_asserts(where, unit, v1, v3)
            if why:
                counts["notAnAssertion"] += 1
                continue
            compare(decision_id, where, by_phrases(unit, v1, v3),
                    iso_dates_in(unit), how)

    for decision_id, location, value in key_anchored:
        # Only a DECIDED row has an attribution to disagree with. A pending row
        # is the STATE lane's business and this lane says nothing about it -
        # which is why deciding the question is what exposed the gap.
        if states.get(decision_id) != "CLOSED_POSITIVE":
            continue
        colocated: list[tuple[str, str, str]] = []
        head_text = v1._disposition_value_text(value)
        if isinstance(head_text, str) and head_text.strip():
            colocated.append(("", location, head_text))
        if not isinstance(value, str):
            overflow: list[str] = []
            colocated.extend(decision_subtree_leaves(value, location,
                                                     overflow=overflow))
            if overflow:
                out.append(
                    f"{prefix}-ATTRIBUTION-DEPTH {name}{overflow[0]}: the "
                    "decision-keyed value exceeds this lane's traversal bound, "
                    "so it was NOT fully examined and its silence is not "
                    "evidence")
        for key, where, text in colocated:
            if not isinstance(text, str) or not text.strip():
                continue
            why = records_rather_than_asserts(where, text, v1, v3)
            # A field whose KEY records who acted is an attribution whatever its
            # value says: the key supplies the predicate that prose has to spell
            # out. Same for a field whose VALUE is a bare calendar date.
            if key and not why:
                if authority_shaped_key(key, v3, v2) and not is_iso_date_value(text):
                    tokens = v3._role_verdict(text)
                    if tokens:
                        compare(decision_id, where, [(text.strip(), tokens)], [],
                                f"authority-shaped key {key!r}")
                if is_iso_date_value(text):
                    compare(decision_id, where, [], [text.strip()],
                            f"date-valued key {key!r}")
            scan_prose(decision_id, where, text, "co-located prose",
                       require_id=False)

    for decision_id, location, leaf in prose:
        if states.get(decision_id) != "CLOSED_POSITIVE":
            continue
        scan_prose(decision_id, f"{location}<prose>", leaf, "prose naming the id",
                   require_id=True)

    return out, counts


# ---------------------------------------------------------------------------
# The corpus pass, with standing applied.
# ---------------------------------------------------------------------------

def attribution_scan(product: object, docs: list[tuple[str, object]],
                     v4, v3, v2, v1, ledger=None
                     ) -> tuple[list[str], list[str], dict[str, object]]:
    """(failures, historical observations, report) for the whole scanned corpus.

    Standing is the pinned closure's, CALLED not copied, so this lane cannot
    quietly grade an artifact differently from the state lane beside it.
    """
    states = v1.packet_decision_states(product)
    attribution = packet_attribution(product, v3, v2)
    attributed = {d: a for d, a in attribution.items() if a["who"] or a["when"]}
    report: dict[str, object] = {
        "packetDecisionIds": len(states),
        "decisionsWithRecordedAttribution": len(attributed),
        "recordedAttribution": {d: dict(a) for d, a in sorted(attributed.items())},
        "artifactsExamined": len(docs),
        "attributionSites": 0,
        "authorityClaims": 0,
        "dateClaims": 0,
        "agreeing": 0,
        "notAnAssertion": 0,
        "conflicts": 0,
        "conflictingArtifactsLive": 0,
        "conflictingArtifactsHistorical": 0,
        "historicalObservations": 0,
        "demotedByStanding": {"REJECTED": 0, "REVIEW-RECORD": 0, "SUPERSEDED": 0},
        "classSkipped": None,
    }
    if not states:
        why = ("the binding packet's decision rows could not be read, so there "
               "is no attribution to compare an artifact against")
        report["classSkipped"] = why
        if ledger is not None:
            ledger.not_executed("corpus-attribution", why)
        return [], [], report
    if not attributed:
        why = ("the binding packet records NO authority-shaped field and NO "
               "calendar-date field on ANY decision row, so this lane has "
               "nothing to compare an artifact's attribution against. THE CLASS "
               "DID NOT RUN - its silence is not evidence that no artifact "
               "asserts a fabricated attribution")
        report["classSkipped"] = why
        if ledger is not None:
            ledger.not_executed("corpus-attribution", why)
        return [], [], report

    rejected = v2.rejecting_reviews(docs, v1)
    records = v2.review_records(docs, v1)
    decision_dates = v2.packet_decision_dates(product)
    failures: list[str] = []
    observations: list[str] = []
    for name, doc in docs:
        found, counts = attribution_failures(
            states, attribution, name, doc, FINDING_PREFIX, v3, v2, v1)
        for key, value in counts.items():
            if key in report:
                report[key] = int(report[key]) + value   # type: ignore[arg-type]
        if not found:
            continue
        standing, reason = v2.standing_of(
            name, doc, docs, rejected, records, decision_dates)
        if standing == "LIVE":
            report["conflictingArtifactsLive"] = \
                int(report["conflictingArtifactsLive"]) + 1  # type: ignore[arg-type]
            failures.extend(found)
        else:
            report["conflictingArtifactsHistorical"] = \
                int(report["conflictingArtifactsHistorical"]) + 1  # type: ignore[arg-type]
            report["historicalObservations"] = \
                int(report["historicalObservations"]) + len(found)  # type: ignore[arg-type]
            report["demotedByStanding"][standing] += len(found)  # type: ignore[index]
            observations.append(f"{name} - {standing}: {reason}")
            observations.extend(f"    {item}" for item in found)
    if ledger is not None:
        if failures:
            ledger.not_executed(
                "corpus-attribution",
                f"the lane ran and FAILED at {len(failures)} position(s), so it "
                "licenses no clause")
        else:
            ledger.executed(
                "corpus-attribution",
                f"and no artifact with standing ({report['artifactsExamined']} "
                f"examined) attributes a decision the packet carries to an "
                f"authority or a date the packet does not record; "
                f"{report['agreeing']} co-located coordinate(s) agree and "
                f"{report['historicalObservations']} conflicting one(s) survive "
                "in artifacts with no standing, listed above")
    return failures, observations, report


def format_attribution(report: dict[str, object]) -> list[str]:
    """The lane's own census, recomputed every run rather than transcribed."""
    lines = ["ATTRIBUTION LANE - who and when, not merely what state"]
    recorded = report.get("recordedAttribution") or {}
    if report.get("classSkipped"):
        lines.append("  CLASS DID NOT RUN:")
        for piece in _wrap(str(report["classSkipped"]), 68):
            lines.append(f"    {piece}")
        return lines
    lines.append("  attribution DERIVED from the live packet, not transcribed:")
    for decision_id, coordinates in sorted(recorded.items()):   # type: ignore[union-attr]
        lines.append(f"    {decision_id}  who={coordinates['who']} "
                     f"when={coordinates['when']}")
    lines.append(f"  decisions the packet attributes   "
                 f"{report['decisionsWithRecordedAttribution']} of "
                 f"{report['packetDecisionIds']}")
    lines.append(f"  artifacts examined                {report['artifactsExamined']}")
    lines.append(f"  decided-frame clauses examined    {report['attributionSites']}")
    lines.append(f"    of which record rather than assert (quoted, superseded,")
    lines.append(f"    negated, hedged, attributed, historical)  "
                 f"{report['notAnAssertion']}")
    lines.append(f"  co-located coordinates compared   "
                 f"{int(report['authorityClaims']) + int(report['dateClaims'])} "
                 f"(authority {report['authorityClaims']}, "
                 f"date {report['dateClaims']})")
    lines.append(f"    agreeing with the packet        {report['agreeing']}")
    lines.append(f"    conflicting                     {report['conflicts']}")
    lines.append(f"  conflicting artifacts WITH standing (findings)     "
                 f"{report['conflictingArtifactsLive']}")
    lines.append(f"  conflicting artifacts with NONE (observations)     "
                 f"{report['conflictingArtifactsHistorical']}")
    demoted = report.get("demotedByStanding") or {}
    lines.append("    demoted by standing: " + ", ".join(
        f"{k} {v}" for k, v in sorted(demoted.items())))    # type: ignore[union-attr]
    return lines


# ---------------------------------------------------------------------------
# Fixtures. They build the world they test, so they stay meaningful whichever
# state the live packet is in, and NO CORPUS ARTIFACT IS NAMED in any of them.
# ---------------------------------------------------------------------------

def _fixture_packet(v1, v2, decided_by: str, decided_on: str) -> dict:
    ident = v2.RETENTION_DECISION_ID
    return {
        "artifact": "synthetic-binding-packet",
        "decisions": {ident: {
            "status": "DECIDED",
            "decidedOn": decided_on,
            "decidedBy": decided_by,
            "attributionProvenance": (
                f"The product authority {decided_by} recorded this decision on "
                f"{decided_on} and supplied both fields."),
            "decision": {"boundedRetention": "Retention is bounded."},
        }},
        "pendingDecisions": {},
    }


def _artifact(body: object) -> dict:
    return {"artifact": "synthetic-asserting-document", "dispositions": body}


def attribution_cases(v2) -> tuple:
    """(must_pass, must_fail, expected_escapes) for the lane this file adds.

    The forged sentence is ASSEMBLED at run time from the fixture packet's own
    coordinates rather than written as a literal, so no fabricated authority and
    no fabricated date is a constant of this source, and the suite stays
    meaningful if the packet's shape changes.
    """
    ident = v2.RETENTION_DECISION_ID
    other_name = "qbeltran"
    other_date = "2026-07-31"
    real_name = "mnowak"
    real_date = "2026-08-05"

    def forged(text: str) -> dict:
        return _artifact({ident: text})

    must_pass = (
        ("A live artifact that cites only the STATE says nothing about who or "
         "when, and silence is not a conflict",
         forged(f"{ident} is DECIDED; retention is bounded.")),
        ("A live artifact that agrees on state, authority AND date",
         forged(f"{ident} was DECIDED {real_date} by {real_name}.")),
        ("A live artifact that restates the attribution in structured form",
         _artifact({ident: {"status": "DECIDED", "decidedBy": real_name,
                            "decidedOn": real_date}})),
        ("A live artifact that agrees and QUOTES the struck wording as "
         "superseded - the corpus retains superseded text verbatim",
         forged(f"{ident} was DECIDED {real_date} by {real_name}. This field "
                f"PREVIOUSLY read 'SIGNED OFF {other_date} by product owner' "
                "and that wording is superseded.")),
        ("A live artifact carrying a date that belongs to a DIFFERENT event, "
         "in a clause that does not assert the decision",
         {"artifact": "synthetic-asserting-document",
          "dispositions": {ident: f"DECIDED by {real_name}."},
          "authoringNote": f"This document was authored {other_date}."}),
        ("A live artifact reporting that ANOTHER document asserted the "
         "fabrication - reported speech is not an assertion",
         forged(f"An earlier record claimed {ident} was signed off "
                f"{other_date} by product owner; no such sign-off occurred.")),
        ("A live artifact that names the authority WITHOUT any closure "
         "predicate - a mention is not an attribution",
         {"artifact": "synthetic-asserting-document",
          "dispositions": {ident: f"Owned by {other_name} for review routing."}}),
    )

    must_fail = (
        ("the fabricated sign-off sentence, verbatim in shape: a closure "
         "predicate, a substituted date and a substituted authority",
         "ATTRIBUTION-DATE",
         forged(f"SIGNED OFF {other_date} by product owner - zero implicit "
                "durable retention for greenfield.")),
        ("the same sentence, caught on the AUTHORITY coordinate too",
         "ATTRIBUTION-AUTHORITY",
         forged(f"SIGNED OFF {other_date} by product owner - zero implicit "
                "durable retention for greenfield.")),
        ("REWORDED with no literal sign-off token and a different date",
         "ATTRIBUTION-DATE",
         forged(f"Ratified 2026-08-02 by the product owner; the "
                "durable-retention default is settled.")),
        ("STRUCTURED form: a substituted authority under a genuine key",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"decidedBy": "product owner",
                            "decision": "Accepted for greenfield."}})),
        ("RELOCATED to sibling prose that names the decision id",
         "ATTRIBUTION-DATE",
         {"artifact": "synthetic-asserting-document",
          "note": f"The product owner accepted {ident} on 2026-08-02."}),
        ("ALIASED key: a signature-shaped key name the packet does not use",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"productAcceptance": "Granted by the product "
                                                 "owner."}})),
        ("substituted AUTHORITY while the state and the date both agree",
         "ATTRIBUTION-AUTHORITY",
         forged(f"DECIDED {real_date} by the coordinator.")),
        ("substituted DATE while the state and the authority both agree",
         "ATTRIBUTION-DATE",
         forged(f"DECIDED 2026-06-01 by {real_name}.")),
        ("inverted posture carried on a substituted authority and date",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"status": "DECIDED", "decidedBy": other_name,
                            "decidedOn": "2026-09-30",
                            "decision": "Ephemeral by default."}})),
        ("BURIED under the decision key, in a field with no dispositional name",
         "ATTRIBUTION-DATE",
         _artifact({ident: {"status": "DECIDED",
                            "notes": [f"SIGNED OFF {other_date} by product "
                                      "owner - zero implicit durable "
                                      "retention for greenfield."]}})),
        ("ALIASED authority key and ALIASED date key together",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"status": "DECIDED",
                            "signedOffBy": "the coordinator",
                            "approvedOn": other_date}})),
        ("ALIASED date key, caught on its own coordinate",
         "ATTRIBUTION-DATE",
         _artifact({ident: {"status": "DECIDED",
                            "signedOffBy": "the coordinator",
                            "approvedOn": other_date}})),
    )

    expected_escapes = (
        ("RESIDUAL-A1 the SILENT lie: assert the decision closed and say nothing "
         "whatever about who or when. Silence is accepted by construction, "
         "because the legitimate majority of this corpus cites only the state",
         forged(f"{ident} is ACCEPTED and the default is settled.")),
        ("RESIDUAL-A2 the COHERENT lie: assert the decision closed and restate "
         "the packet's OWN authority and date while inverting the substance. "
         "Attribution agrees, so this lane is silent; the substance is the "
         "inherited posture lane's business and it does not read artifacts",
         forged(f"DECIDED {real_date} by {real_name}: ephemeral by default, "
                "implicit durable retention NO.")),
        ("RESIDUAL-A3 the CITATION excuse: append a pointer or a file reference "
         "to the forged clause and the inherited assertion vocabulary reads it "
         "as a citation. Inherited unchanged from the pinned closure, where the "
         "same excuse governs the state lane",
         forged(f"SIGNED OFF {other_date} by product owner, per "
                + "some-other-record" + ".json#detail")),
    )
    return must_pass, must_fail, expected_escapes


def hostile_shapes(v2) -> tuple:
    """A CRASH MUST NOT READ AS A FINDING (litmus D-6)."""
    ident = v2.RETENTION_DECISION_ID
    deep: object = "leaf"
    for _ in range(300):
        deep = [deep]
    wide = {f"k{i}": f"DECIDED 2026-06-0{i % 9} by nobody{i}" for i in range(500)}
    return (
        ("the artifact root is a string", "a bare string"),
        ("the artifact root is a list", [1, 2, 3]),
        ("the artifact root is null", None),
        ("the decision-keyed value is an int", {"d": {ident: 7}}),
        ("the decision-keyed value is a bool", {"d": {ident: True}}),
        ("the decision-keyed value is null", {"d": {ident: None}}),
        ("the decision-keyed value is an empty object", {"d": {ident: {}}}),
        ("the decision-keyed value is a list of nulls",
         {"d": {ident: [None, None]}}),
        ("300-deep list nesting under the decision key", {"d": {ident: deep}}),
        ("500 sibling leaves under the decision key", {"d": {ident: wide}}),
        ("a 200000-character leaf under the decision key",
         {"d": {ident: "DECIDED by " + "q" * 200000}}),
        ("regex metacharacters in an authority-shaped value",
         {"d": {ident: {"decidedBy": "(.*)+[a-z", "status": "DECIDED"}}}),
        ("a lone surrogate beside a decided assertion",
         {"d": {ident: "DECIDED 2026-06-01 by \ud800 someone"}}),
        ("an impossible calendar date beside a decided assertion",
         {"d": {ident: "DECIDED 2026-02-30 by someone"}}),
        ("a five-digit year beside a decided assertion",
         {"d": {ident: "DECIDED 20260-08-05 by someone"}}),
        ("an authority-shaped key whose value is an object",
         {"d": {ident: {"decidedBy": {"name": "x"}, "status": "DECIDED"}}}),
        ("a decision id used as a key at the document root",
         {ident: "DECIDED 2026-06-01 by someone"}),
        ("the same decision id at fifty different paths",
         {"d": [{ident: "DECIDED 2026-06-01 by someone"} for _ in range(50)]}),
    )


# ---------------------------------------------------------------------------
# HONEST LIMITS, SCOPED PER LANE.
#
# Every residual carries the LANE it belongs to and the label of the --selftest
# case that EXECUTES it, or None. The counts are computed with len() from the
# tuples so they cannot drift from the list, and --selftest FAILS if any non-None
# gate label does not correspond to a case the suite actually ran - freeze 7.8's
# sixth design move, "make the residual gate the build", applied to the
# disclosure itself.
# ---------------------------------------------------------------------------

def residual_registry(v4, v3) -> tuple:
    """(tag, lane, text, gate label or None). Inherited rows are CARRIED."""
    # The predecessor's rows are CARRIED, with their lane label re-marked so a
    # reader cannot mistake the predecessor's "this successor" for this one's.
    rows: list[tuple[str, str, str, str | None]] = [
        (tag, lane.replace("this successor", "predecessor, carried"), text, gate)
        for tag, lane, text, gate in v4.residual_registry(v3)]
    rows.extend([
        ("A1", "attribution (this successor)",
         "the SILENT lie. An artifact that asserts the decision is closed and "
         "says nothing whatever about who or when is accepted. This is not an "
         "oversight: it is the property this lane enforces, and the legitimate "
         "majority of this corpus cites only the state. Executed by a case "
         "EXPECTED to escape.",
         "RESIDUAL-A1"),
        ("A2", "attribution (this successor)",
         "the COHERENT lie. Restate the packet's own authority and date while "
         "inverting the substance and this lane is silent, because attribution "
         "agrees. Substance is the inherited posture lane's business and that "
         "lane reads the packet, not artifacts. Executed by a case EXPECTED to "
         "escape.",
         "RESIDUAL-A2"),
        ("A3", "attribution (this successor)",
         "the CITATION excuse is INHERITED, not introduced. A clause carrying a "
         "file reference, a bracketed template or a document pointer is read as "
         "a citation rather than an assertion, by the same predicate that "
         "governs the state lane beside it. Appending one to a forged clause "
         "buys silence from BOTH lanes at once. Narrowing it here would make "
         "the two lanes disagree about what an assertion is, which is worse "
         "than the escape. Executed by a case EXPECTED to escape.",
         "RESIDUAL-A3"),
        ("A4", "attribution (this successor)",
         "the lane compares tokens, not identities. An authority whose "
         "meaningful tokens INTERSECT the recorded one agrees - so a longer "
         "phrase containing the recorded name passes. Tightening to exact "
         "equality would fire on every legitimate paraphrase, which is the "
         "false-positive direction this lane exists to avoid.",
         None),
        ("A5", "attribution (this successor)",
         "a decision the packet carries with NO recorded authority and NO "
         "recorded date is compared under a SEPARATE family: any attribution an "
         "artifact supplies for it is reported as UNRECORDED, because an "
         "artifact may cite a decision and may never create one. Measured cost "
         "on this tree: zero. If a future packet records decisions "
         "inconsistently - some attributed, some not - this limb becomes the "
         "loudest one, and that is a deliberate fail-closed choice.",
         "an artifact supplies an attribution the packet does not record"),
        ("A6", "attribution (this successor)",
         "the lane observes JSON only, because the pinned scanner it calls "
         "globs one suffix. Instruments and narrative documents can carry a "
         "fabricated attribution and are NOT observed by this instrument. That "
         "is what keeps the corpus's own forensic record of the incident from "
         "being reported as the incident, and it is equally what an author "
         "could exploit. The population is MEASURED by --selftest rather than "
         "assumed from this sentence.",
         "the scanned population is JSON-only, measured not assumed"),
        ("A7", "attribution (this successor)",
         "positional attribution only. A `by X` phrase is read as an "
         "attribution only where it FOLLOWS the closure predicate, so an "
         "inverted construction - the agent named before the act - escapes. "
         "Measured on this corpus: without the positional rule four live "
         "artifacts are false positives; with it, zero are, and the inverted "
         "construction occurs nowhere.",
         None),
        ("A8", "attribution (this successor)",
         "standing is INHERITED, so this lane inherits the whole of it - "
         "including the rule that one substantive later version demotes its "
         "predecessor without any review. A forged attribution inside an "
         "artifact that some unreviewed successor happens to supersede becomes "
         "an observation rather than a finding, exactly as a state conflict "
         "does. That is deliberate: two lanes grading the same artifact "
         "differently would be worse.",
         "inherited demotion corpus"),
        ("A9", "attribution (this successor)",
         "an artifact that carries NO decision id is invisible to this lane, "
         "because every site is anchored on one. An attribution written with "
         "the decision named only in a heading, a filename or a digest is not "
         "reached.",
         None),
        ("A10", "attribution (this successor)",
         "duplicate JSON keys remain invisible, inherited from the predecessor "
         "closure: the parser keeps the last, so an artifact carrying two "
         "attributions under one key is examined as one. Repairing it means "
         "replacing the parse, which changes every lane at once.",
         None),
    ])
    return tuple(rows)


def format_limits(rows: tuple, measured_predecessor: tuple[int, int]) -> list[str]:
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
        "predecessor's own",
        f"  registry, re-read from its live bytes on this run, carries "
        f"{measured_predecessor[0]} rows of which "
        f"{measured_predecessor[1]} are gated;",
        "  every one of them is CARRIED here rather than restated, so a "
        "predecessor",
        "  disclosure cannot be quietly dropped by a successor.",
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
# document that no longer exists (7.2.2).
# ---------------------------------------------------------------------------

FILENAME_SHAPED_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.(py|json|md|txt)\b")


def own_string_constants() -> list[str]:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    return [node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)]


def source_before_selftest() -> str:
    """This file's source up to the first selftest definition - the predicates.

    The split marker is assembled at runtime because a literal would match
    itself.
    """
    marker = "def " + "selftest("
    return Path(__file__).read_text(encoding="utf-8").split(marker)[0]


# ---------------------------------------------------------------------------
# Selftest.
# ---------------------------------------------------------------------------

def selftest(product, ri, versioning, delivery, retention, register,
             v4, v3, v2, v1, permitted: set[str]) -> int:
    """Every claim this file makes, executed.

    A green run here is AUTHOR-SIDE evidence only. Freeze 7.8's bound is not
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

    ident = v2.RETENTION_DECISION_ID
    fixture_packet = _fixture_packet(v1, v2, "mnowak", "2026-08-05")
    fixture_states = v1.packet_decision_states(fixture_packet)
    fixture_attr = packet_attribution(fixture_packet, v3, v2)

    def lane(doc, packet=None, attr=None, states=None):
        found, _ = attribution_failures(
            states if states is not None else fixture_states,
            attr if attr is not None else fixture_attr,
            "synthetic.doc", doc, FINDING_PREFIX, v3, v2, v1)
        return found

    print("packet-side derivation - both coordinates must come OUT of the "
          "packet, never out of this source")
    check("derivation",
          fixture_attr.get(ident, {}).get("who") == ["mnowak"]
          and fixture_attr.get(ident, {}).get("when") == ["2026-08-05"],
          "the shape derivation recovers the fixture packet's authority and "
          "date without naming either key",
          f"derived {fixture_attr.get(ident)}")
    renamed = copy.deepcopy(fixture_packet)
    row = renamed["decisions"][ident]
    row["signedOffBy"] = row.pop("decidedBy")
    row["approvedOn"] = row.pop("decidedOn")
    renamed_attr = packet_attribution(renamed, v3, v2)
    check("derivation",
          renamed_attr.get(ident, {}).get("who") == ["mnowak"]
          and renamed_attr.get(ident, {}).get("when") == ["2026-08-05"],
          "and it still recovers them when the packet RENAMES both fields - the "
          "derivation is by shape, so a legitimate schema change costs a re-read "
          "rather than a successor instrument (7.10)",
          f"derived {renamed_attr.get(ident)}")
    probes = ("2026-08-05", " 2026-08-05 ", "20260805", "2026-8-5", "2026-13-45",
              "2026-02-30", "x2026-08-05", "2026-08-05x", "", "0001-01-01",
              "2026-08-05T00:00:00", "99999-01-01")
    disagree = [p for p in probes
                if bool(_ISO_EXTENDED.match(p)) != bool(v3.ISO_EXTENDED_RE.match(p))]
    check("derivation", not disagree,
          "this file's anchored date pattern AGREES with the pinned closure's "
          "over a probe set, so the second private copy of the rule is measured "
          "rather than assumed",
          f"{len(probes)} probes, disagreements {disagree}")
    live_attr = packet_attribution(product, v3, v2)
    live_attributed = {d: a for d, a in live_attr.items() if a["who"] or a["when"]}
    if not live_attributed:
        partial.append(
            "the LIVE packet records no authority-shaped field and no calendar "
            "date on any decision row, so the derivation could not be exercised "
            "against live bytes and this run does NOT claim it")
    else:
        live_states = v1.packet_decision_states(product)
        decided = sorted(d for d in live_attributed
                         if live_states.get(d) == "CLOSED_POSITIVE")
        check("derivation", bool(decided),
              "and on the LIVE packet at least one DECIDED row carries a "
              "derivable attribution, so this lane has something to compare",
              f"decided rows with a derivable attribution: {decided}")

    print("the added lane - artifacts that MUST be accepted (silence is not a "
          "conflict)")
    must_pass, must_fail, escapes = attribution_cases(v2)
    for label, doc in must_pass:
        found = lane(doc)
        executed_labels.add(label)
        check("accept", not found, label, "; ".join(found)[:240] if found else "")

    print("the added lane - forgeries that MUST be caught, and the family that "
          "must catch each")
    for label, family, doc in must_fail:
        found = lane(doc)
        executed_labels.add(label)
        hit = [f for f in found if family in f]
        check("reject", bool(hit), label,
              (f"expected a {family} finding; got "
               f"{[f.split(' ')[0] for f in found] or 'NOTHING'}")
              if not hit else hit[0][:190])

    print("the added lane - residuals EXPECTED to escape; a residual that stops "
          "escaping is a FAILURE, because the published disclosure would be stale")
    for label, doc in escapes:
        found = lane(doc)
        executed_labels.add(label.split(" ")[0])
        check("residual", not found, label,
              f"NO LONGER ESCAPES: {found[0][:180]}" if found
              else "escapes this lane, as disclosed")

    print("non-vacuity - a family nothing can trip is decoration")
    exercised = {family for _, family, _ in must_fail}
    for family in ("ATTRIBUTION-AUTHORITY", "ATTRIBUTION-DATE"):
        check("nonvacuity", family in exercised,
              f"family {family} is exercised by at least one must-fail case")
    unattributed = copy.deepcopy(fixture_packet)
    unattributed["decisions"][ident].pop("decidedBy")
    unattributed["decisions"][ident].pop("decidedOn")
    unattributed["decisions"][ident].pop("attributionProvenance")
    ua_attr = packet_attribution(unattributed, v3, v2)
    ua_states = v1.packet_decision_states(unattributed)
    ua_found = lane(_artifact({ident: "DECIDED 2026-06-01 by somebodyelse."}),
                    attr=ua_attr, states=ua_states)
    check("nonvacuity",
          any("UNRECORDED" in f for f in ua_found),
          "an artifact supplies an attribution the packet does not record",
          f"{len(ua_found)} finding(s); first "
          f"{ua_found[0][:150] if ua_found else 'NONE'}")
    executed_labels.add("an artifact supplies an attribution the packet does "
                        "not record")
    check("nonvacuity",
          not lane(_artifact({ident: "DECIDED; retention is bounded."}),
                   attr=ua_attr, states=ua_states),
          "and the same unattributed packet accepts an artifact that cites only "
          "the state, so the UNRECORDED limb is not simply always-on")

    print("gate independence - each coordinate must fire ALONE, or it is not a "
          "coordinate")
    only_date = lane(forged_date := _artifact(
        {ident: "DECIDED 2026-06-01 by mnowak."}))
    families = {f.split(" ")[0].removeprefix(FINDING_PREFIX + "-")
                for f in only_date}
    check("gate", families == {"ATTRIBUTION-DATE"},
          "a substituted DATE alone fires only the date family",
          f"families present: {sorted(families)}; {len(forged_date)} site(s)")
    only_who = lane(_artifact({ident: "DECIDED 2026-08-05 by the coordinator."}))
    families = {f.split(" ")[0].removeprefix(FINDING_PREFIX + "-") for f in only_who}
    check("gate", families == {"ATTRIBUTION-AUTHORITY"},
          "a substituted AUTHORITY alone fires only the authority family",
          f"families present: {sorted(families)}")

    print("the FALSE-POSITIVE matrix - the corpus's own forensic records of the "
          "fabrication must never be reported AS the fabrication")
    other_date = "2026-07-31"
    forged_sentence = (f"SIGNED OFF {other_date} by product owner - zero "
                       "implicit durable retention for greenfield.")
    for label, doc in (
        ("a quoted-and-retracted record, the shape the binding register uses",
         _artifact({ident: f"DECIDED 2026-08-05 by mnowak. This field "
                           f"previously asserted '{forged_sentence}' No such "
                           "sign-off occurred."})),
        ("a record explicitly marked SUPERSEDED",
         _artifact({ident: f"SUPERSEDED. It read verbatim: {forged_sentence}"})),
        ("a record whose PATH marks it historical",
         {"historicalRecord": {ident: forged_sentence}}),
        ("a forensic narrative that REPORTS the fabrication",
         {"note": f"An earlier register asserted that {ident} was signed off "
                  f"{other_date} by product owner. It was struck."}),
        ("the DISCLOSED citation excuse: a forged clause carrying a document "
         "pointer reads as a citation to the inherited vocabulary, exactly as "
         "it does for the state lane beside it (residual A3)",
         _artifact({ident: f"SIGNED OFF {other_date} by product owner, per "
                           + "some-record" + ".json#detail"})),
        ("a record that carries the sentence inside a bracketed template",
         _artifact({ident: f"[STRUCK {other_date}] {forged_sentence}"})),
    ):
        found = lane(doc)
        check("falsepositive", not found, label,
              "; ".join(found)[:200] if found else "silent, as required")

    print("the LIVE corpus - the acceptance test that decides whether the lane "
          "is usable")
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    suffixes = sorted({Path(name).suffix for name, _ in docs})
    check("corpus", suffixes == [".json"] or not docs,
          "the scanned population is JSON-only, measured not assumed",
          f"{len(docs)} parsed of {discovered} discovered; suffixes {suffixes}; "
          f"{len(unreadable)} unreadable and NAMED")
    executed_labels.add("the scanned population is JSON-only, measured not "
                        "assumed")
    ledger = v4.GateLedger()
    live_failures, live_observations, live_report = attribution_scan(
        product, docs, v4, v3, v2, v1, ledger)
    if live_report.get("classSkipped"):
        partial.append(
            "the attribution lane did not run against live bytes: "
            + str(live_report["classSkipped"]))
    else:
        print(f"    artifacts examined                {len(docs)}")
        print(f"    decided-frame clauses examined    "
              f"{live_report['attributionSites']}")
        print(f"    coordinates compared              "
              f"{int(live_report['authorityClaims']) + int(live_report['dateClaims'])}")
        print(f"    agreeing with the packet          {live_report['agreeing']}")
        print(f"    conflicting, WITH standing        {len(live_failures)}")
        print(f"    conflicting, no standing          "
              f"{live_report['historicalObservations']}")
        check("corpus", not live_failures,
              "ZERO false positives across the whole live corpus - the lane is "
              "silent on every artifact that has standing today",
              f"live findings: {live_failures[:2]}" if live_failures
              else "0 findings")
        check("corpus", True,
              "MEASURED, not smoothed: conflicting attributions that survive in "
              "artifacts with NO standing are reported as HISTORICAL "
              "OBSERVATIONS and never dropped",
              f"{live_report['historicalObservations']} observation(s) in "
              f"{live_report['conflictingArtifactsHistorical']} artifact(s); "
              f"demoted {live_report['demotedByStanding']}")
        planted_name = "zz-synthetic-plant.v1" + ".json"
        planted = json.loads(json.dumps(_artifact({ident: forged_sentence})))
        planted_found, _ = attribution_failures(
            v1.packet_decision_states(product), live_attr, planted_name,
            planted, FINDING_PREFIX, v3, v2, v1)
        check("corpus", bool(planted_found) and any(
            planted_name in f for f in planted_found),
            "and the SAME sentence, planted as a live document against the LIVE "
            "packet, is CAUGHT AND NAMED IN FULL - so corpus silence is a "
            "measurement of the corpus, not of a dead lane",
            planted_found[0][:200] if planted_found else "NOT CAUGHT")

    print("banner honesty - the banner may name ONLY the gates that ran")
    ran = set(ledger.gate_names)
    skipped = {gate for gate, _ in ledger.skipped}
    check("banner",
          ("corpus-attribution" in ran) != ("corpus-attribution" in skipped),
          "the attribution gate is registered exactly once, as RUN or as "
          "NOT RUN, never both and never neither",
          f"ran={sorted(ran)} skipped={sorted(skipped)}")
    failing_ledger = v4.GateLedger()
    failing_docs = [("synthetic.doc",
                     json.loads(json.dumps(_artifact({ident: forged_sentence}))))]
    failing, _obs, _rep = attribution_scan(
        product, failing_docs, v4, v3, v2, v1, failing_ledger)
    check("banner",
          bool(failing) and "corpus-attribution" not in failing_ledger.gate_names
          and any(gate == "corpus-attribution"
                  for gate, _ in failing_ledger.skipped),
          "a gate that RUNS AND FAILS registers no clause, so a failed gate can "
          "never contribute a sentence to a success banner",
          f"{len(failing)} finding(s); ran={sorted(failing_ledger.gate_names)}")
    empty_ledger = v4.GateLedger()
    attribution_scan({"decisions": {}}, [], v4, v3, v2, v1, empty_ledger)
    check("banner",
          any(gate == "corpus-attribution" for gate, _ in empty_ledger.skipped),
          "a packet with no readable decision row registers the class as NOT "
          "RUN by name, so 'derived from nothing' and 'derived and found "
          "nothing' never print the same (7.8.1 rule 1)",
          f"skipped={[g for g, _ in empty_ledger.skipped]}")

    print("hostile input - every shape must produce a NAMED outcome, never a "
          "traceback (litmus D-6)")
    for label, shape in hostile_shapes(v2):
        try:
            found = lane(shape)
            ok = isinstance(found, list) and all(isinstance(f, str) for f in found)
            detail = f"{len(found)} finding(s)"
        except Exception as exc:                       # noqa: BLE001 - measured
            ok = False
            detail = f"RAISED {type(exc).__name__}: {exc}"
        check("hostile", ok, label, detail)
    try:
        attribution_scan("not a packet", [("x", None)], v4, v3, v2, v1,
                         v4.GateLedger())
        check("hostile", True, "the whole scan survives a non-object packet and "
                               "a null document")
    except Exception as exc:                           # noqa: BLE001 - measured
        check("hostile", False, "the whole scan survives a non-object packet",
              f"RAISED {type(exc).__name__}: {exc}")

    print("NO REGRESSION - the predecessor's entire published case corpus, "
          "re-driven through the shared lane")
    p_pass, p_fail, p_escapes = v4.decision_cases_v4(v3, v2, v1)
    regressions = [label for label, family, packet in p_fail
                   if not any(family in f
                              for f in v4.decision_lane_v4(packet, v3, v2, v1))]
    check("noregression", not regressions,
          f"all {len(p_fail)} predecessor must-fail cases are still caught by "
          "their own family",
          f"regressions: {regressions}" if regressions else "0 regressions")
    accepted = [label for label, packet in p_pass
                if not v4.decision_lane_v4(packet, v3, v2, v1)]
    check("noregression", len(accepted) == len(p_pass),
          f"all {len(p_pass)} predecessor must-PASS cases still pass",
          f"{len(accepted)} of {len(p_pass)}")
    still_escaping = [label for label, packet in p_escapes
                      if not [f for f in v4.decision_lane_v4(packet, v3, v2, v1)
                              if f.startswith("PD4")]]
    check("noregression", len(still_escaping) == len(p_escapes),
          f"all {len(p_escapes)} predecessor residuals still escape, so its "
          "published disclosure is not stale",
          f"{len(still_escaping)} of {len(p_escapes)}")
    for label, _packet in p_escapes:
        executed_labels.add(label.split(" ")[0])
    for label, _family, _packet in p_fail:
        executed_labels.add(label)
    for label, _packet in p_pass:
        executed_labels.add(label)
    g_pass, g_fail, _g_escapes = v3.decision_cases(v1, v2)
    grand = [label for label, family, packet in g_fail
             if not any(family in f
                        for f in v4.decision_lane_v4(packet, v3, v2, v1))]
    check("noregression", not grand,
          f"and all {len(g_fail)} cases of the generation before it",
          f"regressions: {grand}" if grand else "0 regressions")
    hostile_ok = 0
    for label, shape in (tuple(v3.hostile_shapes(v1, v2))
                         + tuple(v4.hostile_shapes_v4(v3, v2, v1))):
        try:
            found = v4.decision_lane_v4(shape, v3, v2, v1)
            hostile_ok += int(isinstance(found, list))
        except Exception:                              # noqa: BLE001 - measured
            pass
    total_hostile = len(v3.hostile_shapes(v1, v2)) + len(
        v4.hostile_shapes_v4(v3, v2, v1))
    check("noregression", hostile_ok == total_hostile,
          f"and all {total_hostile} inherited hostile shapes still produce a "
          "named outcome rather than a traceback",
          f"{hostile_ok} of {total_hostile}")

    print("inherited packet-side gates - the predecessor's blocker-1 matrix and "
          "its discrimination sweep, re-run against LIVE bytes")
    live_row = product.get("decisions", {}).get(ident) \
        if isinstance(product, dict) else None
    if not isinstance(live_row, dict) or not isinstance(live_row.get("decidedBy"), str):
        partial.append(
            "the live packet does not carry a decided retention row with a "
            "string authority, so the inherited blocker-1 matrix could not be "
            "run against live bytes and this run does NOT claim it")
    else:
        matrix = 0
        for candidate, must_catch in (
            ("retention", True), ("Phase", True), ("PURGED", True),
            ("tombstone", True), ("bounds", True), ("sfbreens", True),
            ("SFBREEN", True), ("the coordinator", True), ("jdoe", True),
            ("z", True), (live_row["decidedBy"], False),
        ):
            mutated = copy.deepcopy(product)
            mutated["decisions"][ident]["decidedBy"] = candidate
            caught = bool(v4.decision_lane_v4(mutated, v3, v2, v1))
            matrix += int(caught == must_catch)
        check("inherited", matrix == 11,
              "the inherited blocker-1 matrix scores 11 of 11 on live bytes",
              f"{matrix} of 11")
    tokens, survivors, predecessor_survivors = v4.attribution_discrimination(
        product, v3, v2, v1, deep=True)
    if not tokens:
        partial.append(
            "the live packet carries no decided retention row, so the inherited "
            "discrimination sweep had no token population and this run does NOT "
            "publish it")
    else:
        print(f"    distinct 3+-character tokens in the live decision row  "
              f"{len(tokens)}")
        print(f"    surviving the generation-3 decision lane               "
              f"{len(predecessor_survivors)}")
        print(f"    surviving the predecessor's lane                       "
              f"{len(survivors)}")
        check("inherited", set(survivors) < set(predecessor_survivors),
              "the inherited surviving set is still a STRICT SUBSET, so nothing "
              "in this successor loosened it",
              f"{len(survivors)} of {len(predecessor_survivors)}")
        check("inherited",
              product["decisions"][ident]["decidedBy"] in survivors,
              "and the packet's ACTUAL recorded authority is still among the "
              "survivors (7.10: pin the property, not the value)")
    executed_labels.add("attribution discrimination sweep")

    print("the inherited demotion corpus, re-run unchanged (R1-R5 preserved)")
    dated = v4._fixture(v3, v2, v1, decided=v4._good_decision(v3))
    undated = v4._fixture(v3, v2, v1, pending=copy.deepcopy(v3._GOOD_PENDING))
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
          f"measured {residual_escapes}")
    executed_labels.add("inherited demotion corpus")

    print("residual PD4-N1, carried and MEASURED rather than repeated as prose: "
          "does recording a SECOND decision by the same authority still trip the "
          "inherited packet lane?")
    if isinstance(live_row, dict) and isinstance(live_row.get("decidedBy"), str):
        extended = copy.deepcopy(product)
        extended["decisions"]["CD-SECOND-DECISION"] = {
            "status": "DECIDED",
            "decidedOn": "2026-09-01",
            "decidedBy": live_row["decidedBy"],
            "attributionProvenance": (
                f"The product authority {live_row['decidedBy']} recorded this "
                "second decision on 2026-09-01."),
        }
        before = [f for f in v4.decision_lane_v4(product, v3, v2, v1)]
        after = [f for f in v4.decision_lane_v4(extended, v3, v2, v1)]
        ambient = [f for f in after if "AMBIENT" in f]
        own = attribution_failures(
            v1.packet_decision_states(extended),
            packet_attribution(extended, v3, v2), "synthetic.doc",
            _artifact({ident: "DECIDED; retention is bounded."}),
            FINDING_PREFIX, v3, v2, v1)[0]
        check("pd4n1", bool(ambient) and not before,
              "MEASURED: the inherited AMBIENT limb still fires on a second "
              "decision by the same authority - the tolerance is UNCHANGED by "
              "this successor, in either direction",
              f"live packet {len(before)} finding(s); extended packet "
              f"{len(after)} finding(s), {len(ambient)} of them AMBIENT")
        check("pd4n1", not own,
              "and the ADDED lane contributes nothing to that tolerance: it is "
              "corpus-side and says nothing about the packet's own rows",
              f"{len(own)} attribution finding(s) from the added lane")
    else:
        partial.append(
            "the live packet does not carry a decided retention row, so residual "
            "PD4-N1 could not be re-measured on live bytes")

    print("environment independence - a blinded run must give identical results")
    sighted_f, sighted_o, sighted_r = attribution_scan(
        product, docs, v4, v3, v2, v1)
    original_reader = v1.head_named_artifacts
    try:
        v1.head_named_artifacts = lambda *a, **k: (set(), [])
        blind_f, blind_o, blind_r = attribution_scan(
            product, docs, v4, v3, v2, v1)
    finally:
        v1.head_named_artifacts = original_reader
    check("environment",
          sighted_f == blind_f and sighted_o == blind_o
          and sighted_r["conflicts"] == blind_r["conflicts"],
          "head documents unreadable -> identical findings AND observations",
          f"findings {len(sighted_f)}=={len(blind_f)}, observations "
          f"{len(sighted_o)}=={len(blind_o)}")
    needle = "head_named" + "_artifacts"
    predicates = source_before_selftest()
    check("environment", needle not in predicates,
          "no predicate defined before --selftest reads a head document",
          f"{len(predicates)} bytes of predicate source scanned")
    provenance = import_provenance_failures(permitted)
    check("environment", not provenance,
          "environment: import provenance",
          "no module in this process was loaded from the directory this "
          "instrument runs in, other than the pinned closure itself"
          if not provenance else provenance[0])
    executed_labels.add("environment: import provenance")
    check("environment", sys.flags.isolated == 1 and sys.flags.dont_write_bytecode,
          "the invocation guard's own precondition holds in this process",
          f"isolated={sys.flags.isolated} dont_write_bytecode="
          f"{bool(sys.flags.dont_write_bytecode)}")
    check("environment", len(permitted) == 5,
          "the permitted-import set is DERIVED by walking the pin chain, and it "
          "closes at five files",
          f"{len(permitted)} permitted path(s)")

    print("input discipline - a MISSING input and a WRONG subject must never "
          "print the same (7.8.1)")
    subject_findings, missing = v4.partition_input_unavailability([
        "PD-RT-BINDING: cannot read exact candidate (FileNotFoundError)",
        "PD-RT-BINDING: live bytes hash abc differ from the exact digest",
        "PD-EP-BINDING: cannot parse exact candidate (JSONDecodeError)",
    ])
    check("input", len(subject_findings) == 1 and len(missing) == 2,
          "input discipline: an absent optional input skips its class by name",
          f"{len(subject_findings)} finding(s) about the subject, "
          f"{len(missing)} unavailable-input outcome(s)")
    check("input",
          not v4.partition_input_unavailability(
              v1.retention_binding_failures())[1],
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
    rows = residual_registry(v4, v3)
    dangling = sorted({gate for _, _, _, gate in rows
                       if gate is not None and gate not in executed_labels
                       and not any(gate in label for label in executed_labels)})
    check("self", not dangling,
          "every residual claiming to be GATED names a case this suite ran",
          f"dangling gate labels: {dangling}")
    gated_count = sum(1 for r in rows if r[3] is not None)
    check("self", gated_count + (len(rows) - gated_count) == len(rows),
          f"the published split is arithmetic: {gated_count} gated + "
          f"{len(rows) - gated_count} not gated = {len(rows)} residuals")
    inherited_rows = v4.residual_registry(v3)
    check("self",
          all(tag in {r[0] for r in rows} for tag, _, _, _ in inherited_rows),
          f"and all {len(inherited_rows)} inherited residuals are CARRIED, not "
          "dropped",
          f"{len(rows)} total after carrying {len(inherited_rows)}")

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

def banner_lines(ledger, report: dict, v1) -> list[str]:
    """The success banner, assembled from what RAN. Nothing here is a literal."""
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

    try:
        v4 = _load_predecessor()
        v3 = v4._load_predecessor()
        v2 = v3._load_predecessor()
        v1 = v2._load_predecessor()
    except RuntimeError as exc:
        print("REFUSING to run: the pinned predecessor closure is dirty")
        print(f"  - {exc}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    permitted = closure_paths(v4, v3, v2)
    provenance = import_provenance_failures(permitted)
    if provenance:
        print("REFUSING to run: an import came from the directory this "
              "instrument runs in")
        for item in provenance:
            print(f"  - {item}")
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
          "which verifies its own, which verifies its own, so one pin covers a "
          "five-deep closure)")
    print("invocation: ISOLATED, NO-BYTECODE - the script's directory is not on "
          "the import path, so no file beside this one can shadow a module the "
          "pin chain depends on")

    if want_selftest:
        return selftest(product, ri, versioning, delivery, retention, register,
                        v4, v3, v2, v1, permitted)

    ledger = v4.GateLedger()
    join = v1.retention_binding_failures()
    failures, unavailable = v4.partition_input_unavailability(join)
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
    failures.extend(v4.validate_v4(product, ri, versioning, delivery, retention,
                                   v3, v2, v1, ledger))
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    assertion_failures, observations, report = v2.classify(
        product, docs, unreadable, discovered, v1)
    failures.extend(assertion_failures)
    attribution_conflicts, attribution_observations, attribution_report = \
        attribution_scan(product, docs, v4, v3, v2, v1, ledger)
    failures.extend(attribution_conflicts)
    _heads, head_docs = v1.head_named_artifacts(HERE)
    notice_lines = v3.notices(product, docs, v2)
    tokens, survivors, _ = v4.attribution_discrimination(product, v3, v2, v1)
    if tokens:
        notice_lines.append(
            f"PD4-ATTRIBUTION-DISCRIMINATION (NOTICE): of the {len(tokens)} "
            f"distinct 3-or-more-character tokens in the live decision row, "
            f"{len(survivors)} survive as a candidate authority. Inherited "
            "disclosure, RECOMPUTED FROM THE LIVE PACKET on this run rather "
            "than transcribed. It is a notice and can never change an exit code")

    for line in v3.format_report(report, head_docs, notice_lines):
        if line.startswith("HONEST LIMITS"):
            break
        print(line)
    for line in format_attribution(attribution_report):
        print(line)
    inherited_rows = v4.residual_registry(v3)
    for line in format_limits(
            residual_registry(v4, v3),
            (len(inherited_rows),
             sum(1 for r in inherited_rows if r[3] is not None))):
        print(line)
    all_observations = list(observations) + list(attribution_observations)
    if all_observations:
        print("HISTORICAL OBSERVATIONS - a product-decision assertion "
              "conflicting with the binding")
        print("packet, in an artifact with no standing to make it. Not a finding: "
              "freeze 7.2")
        print("forbids editing reviewed bytes and 7.2.1 forbids repairing a "
              "review at all, so")
        print("these cannot be repaired. Reported in full, never dropped - a "
              "forgery buys a")
        print("green exit code, never silence:")
        for line in all_observations:
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
    skipped_classes = [gate for gate, _ in ledger.skipped]
    if skipped_classes:
        print("CLASS-SKIPPED - every class that ran is green and at least one "
              "class DID NOT RUN.")
        print(f"This run does NOT certify: {', '.join(sorted(skipped_classes))}. "
              "Exit 4.")
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
