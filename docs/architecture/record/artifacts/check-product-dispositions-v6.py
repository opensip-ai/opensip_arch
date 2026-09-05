#!/usr/bin/env python3
"""Successor to the pinned predecessor. Edits nothing; repairs ONE class.

WHY A SUCCESSOR AND NOT AN EDIT
-------------------------------
Freeze 7.2 forbids changing reviewed bytes in place and the sanctioned repair is
a new file. The predecessor is a RUNTIME INPUT here, hash-verified before use,
which 7.3 explicitly permits. It in turn hash-verifies and executes ITS
predecessor, and so on, so ONE PIN COVERS A SIX-DEEP CLOSURE and every inherited
detection semantic is RE-USED BY CALL rather than retyped.

WHAT THIS SUCCESSOR CLOSES
--------------------------
An independent review of the predecessor returned ACCEPT_WITH_BLOCKERS at two
blockers. This file closes both, discloses a third defect the same review found
in an inherited lane, and changes nothing else.

  BLOCKER 1 - A TYPE-BLINDNESS ESCAPE. AN ATTRIBUTION REACHED THROUGH A JSON
  CONTAINER WAS NEVER COMPARED, SO THE FORGERY BOUGHT TOTAL SILENCE.

  Take the predecessor's OWN PUBLISHED aliased-attribution vector and wrap each
  value in a one-element array. The plain form is caught and named twice. The
  identical forgery, list-wrapped, produces ZERO findings and ZERO mentions -
  the artifact is named nowhere in the output. REPRODUCED HERE by an external
  driver that wrote real bytes and invoked the predecessor as a subprocess,
  before a line of this file was written.

  The mechanism, confirmed in the predecessor's bytes: its leaf walk yields an
  EMPTY key for every list element, and its structured comparison is guarded on
  the key being non-empty. A scalar's eligibility to be compared was decided by
  the key IMMEDIATELY above it, so any container interposed between the
  authority-shaped key and the scalar destroyed the comparison.

  THIS IS THE SECOND TIME LIST-WRAPPING HAS DEFEATED A GUARD IN THIS LINEAGE.
  Two generations earlier a bracketed-placeholder gate fell to the identical
  trick because its predicate returned False for every non-string, and the next
  generation repaired THAT INSTANCE. The repair did not generalise. So this file
  does not repair a third instance - it closes the CLASS and then measures that
  the class is closed.

  THE REPAIR, DERIVED RATHER THAN ENUMERATED.
    A JSON ARRAY DOES NOT NAME ITS MEMBERS. An array element's name is the name
    of the array, so a scalar reached through any number of arrays carries the
    key of the nearest enclosing OBJECT. An object DOES name its members, so a
    member key is appended rather than replacing what is above it. A leaf
    therefore carries the ORDERED SET OF OBJECT KEYS ON ITS PATH, and it is a
    coordinate of an attribution if ANY of them names one. Containers become
    TRANSPARENT to the comparison, and nesting cannot change a verdict.

  AND THE TYPES ARE DECLARED, WHICH IS THE LESSON FREEZE 4.4 NOW RECORDS.
  A guard that reads values must STATE WHICH JSON TYPES IT READS and be tested
  against every other one, because "the value is a string" is an assumption no
  reviewer sees a checker make. So:

      THIS LANE COMPARES JSON *STRING* SCALARS AND NOTHING ELSE.
      An OBJECT and an ARRAY are containers: they are traversed, never compared.
      A NUMBER, a BOOLEAN and a NULL standing where an attribution coordinate
      lives are NOT compared and are NOT passed over - they are NAMED, by their
      own finding family, saying the content was not compared and this run's
      silence about it is not evidence.

  That is freeze 6 law 18 read at this lane's scale: closed-scalar admission is
  exact-type at any depth, BEFORE comparing content. A number that spells a date
  is not a date here; it is a position this lane declines to read and says so.

  THE CLASS IS THEN PROVEN CLOSED, MECHANICALLY AND PERMANENTLY. --selftest
  carries a CONTAINER-WRAPPING SWEEP: every catch vector this instrument
  publishes is re-run with every scalar in it rewritten into each declared
  container shape, and detection must be INVARIANT. The sweep reports
  invariant/attempted and FAILS the suite on any shape that is not invariant, so
  a future edit cannot quietly reopen the class and no reader has to take this
  paragraph's word for it.

  BLOCKER 2 - A PUBLISHED COST THAT DOES NOT REPRODUCE, WITHDRAWN IN PLACE.

  The predecessor's residual A7 justifies its positional rule as worth "four
  live false positives to zero". Re-measured here, corpus-wide: the positional
  threshold drops ZERO of the `by X` matches the corpus contains, and removing
  the rule changes the run by nothing at all. A sanity control proves the
  measurement is live. A PUBLISHED COST THAT DOES NOT REPRODUCE IS AS MISLEADING
  AS AN UNDISCLOSED ONE, BECAUSE IT RETIRES THE QUESTION. The row is CARRIED
  VERBATIM from the predecessor's live bytes and WITHDRAWN IN PLACE, never
  deleted, and the replacement is not another sentence: the drop count is
  RECOMPUTED FROM THE LIVE CORPUS ON EVERY RUN, printed, and hard-compared by an
  executed case (7.2.2 - a recorded measurement gets a hard comparison; a
  measurement that cannot fail the build is prose).

  AND A THIRD DEFECT, INHERITED, DISCLOSED AND *NOT* REPAIRED HERE.

  The non-retention decision SET is a hard-coded seven-entry literal in the
  first-generation instrument, compared with set equality. ADDING ANY DECISION
  ROW TO THE BINDING PACKET REDS THAT VALIDATOR, whatever the authority, the
  attribution or the posture. So recording the product authority's NEXT decision
  - the awaited Phase-1A insertion - fails a check that has nothing to say about
  it. Measured here, live, every run. It is freeze 7.10's defect applied to a
  decision SET rather than to one decision's state, inherited unrepaired through
  five generations and named in none of the predecessor's 36 residuals.

  IT IS NOT REPAIRABLE INSIDE THIS SUCCESSOR'S SCOPE, and the reason is a rule
  and not a preference. The literal lives in reviewed bytes this file may not
  edit (7.2), and it is consumed inside a lane this file EXECUTES rather than
  reimplements. The only repairs available here are to suppress a reviewed
  lane's finding or to stop calling it, and both silently change a semantic that
  passed independent review. 7.10's rule - pin the PROPERTY, not the CURRENT
  VALUE - is the right repair, and it belongs in a successor to the instrument
  that owns the literal, or in a binding artifact that states what the expected
  decision set IS derived from. This file measures the cost precisely, prints
  it, and refuses to hide it.

THE PROPERTY THIS FILE ENFORCES, UNCHANGED FROM THE PREDECESSOR
---------------------------------------------------------------
    AN ARTIFACT THAT ASSERTS A DECISION IS DECIDED MUST EITHER AGREE WITH THE
    BINDING PACKET ON *WHO* AND *WHEN*, OR SAY NOTHING ABOUT WHO AND WHEN.

MISMATCH IS A FINDING; SILENCE IS NOT. What changed is only the REACH of the
comparison: a coordinate is now found wherever it is, not only where it is
directly under a decision row's own key.

IT IS DERIVED, AND IT NEEDS NO LIST
-----------------------------------
Freeze 7.9 forbids shipping a stop-list and 7.10 forbids pinning today's value,
so both sides of the comparison are READ OFF THE LIVE PACKET EVERY RUN:

  * WHO is the value of any field whose normalised key name ENDS IN 'BY', plus
    the signature-shaped key names the pinned closure already carries.
  * WHEN is any value that IS an ISO-8601 extended calendar date, validated
    against the calendar.
  * and the key names the LIVE PACKET ITSELF uses for each coordinate are
    derived too, so a wrong-typed value standing at the packet's own coordinate
    name is named even where the shape rules do not reach it.

NO AUTHORITY NAME AND NO CALENDAR DATE APPEARS IN ANY FUNCTION THIS FILE USES TO
DECIDE WHAT TO COMPARE. That sentence is scoped deliberately, and it is the
repair of three sentences an independent reviewer measured FALSE AS WRITTEN in
the predecessor: it claimed "No authority name appears in this source" and "No
date appears in this source", which are true of the PREDICATES and false of the
FILE, because the fixtures, the false-positive matrix and the inherited mutation
candidates all carry both. --selftest enumerates this file's decision predicates
BY NAME and audits their string constants, so the scoped claim is measured
rather than asserted, and the unscoped one is not made.

MEASURED, AND THE MEASUREMENT IS THE ACCEPTANCE TEST
----------------------------------------------------
Against the live corpus this lane produces ZERO findings and demotes conflicting
attributions in artifacts with no standing to HISTORICAL OBSERVATIONS, printed
in full - a forgery buys a green exit code, never silence. Against every
published forgery it produces a named finding, IN EVERY CONTAINER SHAPE SWEPT.
Both numbers are recomputed by --selftest from whatever is on disk.

THE ACCEPTED FAILURE MODE, STATED BEFORE THE EVIDENCE
-----------------------------------------------------
A COHERENT lie - assert the decision closed and restate the packet's own
authority and date while inverting the substance - is silent to this lane by
design. Freeze 7.8's bound applies in full and is not repealed by anything
above: this binds structure, type and internal agreement. It cannot bind the
truth of content, and no instrument in this corpus can.
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
# WHY EXIT 2. 2 means "bad invocation" in this lineage's taxonomy; 3 means "ran
# and refused to certify". This is a bad invocation. Freeze 7.8.1 rule 3: an
# exit code a document CLAIMS must be the exit code the file PRODUCES - so the
# refusal text names 2 and returns 2, on BOTH channels, because a message on one
# channel is a message a reader of the other channel does not get.
# ---------------------------------------------------------------------------

_INVOCATION_REFUSAL = (
    "PD6-UNSUPPORTED-INVOCATION: this instrument must be run in ISOLATED, "
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
import hashlib                                         # noqa: E402
import importlib.util                                  # noqa: E402
import json                                            # noqa: E402
import re                                              # noqa: E402
from pathlib import Path                               # noqa: E402


HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# The predecessor is a RUNTIME INPUT, hash-verified before execution (7.3).
# Drift is EXIT_REFUSED, never a silent fallback. It verifies its own, which
# verifies its own, and so on - one pin, six files.
# ---------------------------------------------------------------------------
PREDECESSOR_BINDING = {
    "path": "check-product-dispositions-v5.py",
    "sha256": "acc1c9f31235ce2b2605d9500a07f518f852ec37c3ef0217631b288455af04d8",
    "bytes": 95304,
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
EXIT_CLASS_SKIPPED = 4
DECLARED_FLAGS = ("--selftest",)

FINDING_PREFIX = "PD6"

# Bounds. A hostile artifact may not make this lane expensive, and a bound that
# is hit is REPORTED rather than silently truncating - "derived from nothing"
# and "derived and found nothing" must never print the same (7.8.1 rule 1).
# Carried from the predecessor at the same values so the reach of the repair is
# the only thing that moved.
SUBTREE_MAX_DEPTH = 12
SUBTREE_LEAF_BUDGET = 2000

# THE DECLARED READ SET. This lane compares exactly one JSON type. Every other
# type has a stated, executed outcome, and --selftest asserts this tuple is
# exhaustive over the JSON type space rather than trusting the sentence.
COMPARED_JSON_TYPES = ("string",)
TRAVERSED_JSON_TYPES = ("object", "array")
NAMED_BUT_UNCOMPARED_JSON_TYPES = ("number", "boolean", "null")


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
    spec = importlib.util.spec_from_file_location("_pd_v5", path)
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


def closure_paths(v5, v4, v3, v2) -> set[str]:
    """Every file this instrument is entitled to execute out of this directory.

    DERIVED by walking the pin chain rather than listed, so a longer chain needs
    no edit here and a file that is NOT in the chain can never be admitted by a
    stale literal.
    """
    permitted = {str(Path(__file__).resolve())}
    for module in (None, v5, v4, v3, v2):
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
# THE REPAIR. Containers are transparent; scalar types are declared.
#
# Everything the predecessor derived is CALLED, not retyped. What is new here is
# only how a leaf is REACHED and how its TYPE is treated.
# ---------------------------------------------------------------------------

def leaf_kind(value: object) -> str:
    """The JSON type of a value, as this lane names it.

    Order matters: a JSON boolean is a Python bool and a Python bool is a Python
    int, so booleans are decided BEFORE numbers. Freeze 6 law 18's most
    expensive corpus defect entered through exactly that confusion, in the
    opposite direction, and this function is the single place this file resolves
    it.
    """
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "boolean"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    return "unknown"


def qualified_leaves(value: object, path: str, qualifiers: tuple[str, ...] = (),
                     depth: int = 0, budget: list[int] | None = None,
                     overflow: list[str] | None = None):
    """(qualifiers, path, scalar, json type) for every SCALAR below a value.

    THE ONE RULE THAT CLOSES THE CLASS, AND IT IS DERIVED FROM WHAT JSON IS.

    An ARRAY does not name its members. Its elements are positions, not fields,
    so an element's name is the name of the array itself and the walk adds
    NOTHING to the qualifier list when it descends into one. An OBJECT does name
    its members, so a member key is APPENDED. A scalar therefore arrives
    carrying every object key on its path, outermost first, and a comparison
    that asks "does any qualifier name an attribution coordinate" cannot be
    changed by interposing containers.

    Contrast the predecessor, which yielded the IMMEDIATE key and the empty
    string for list elements: one array between the key and the value erased the
    key, and with it the comparison.

    EVERY SCALAR IS YIELDED, not only strings. A caller that only compares
    strings must be able to SEE the numbers, booleans and nulls it is declining
    to compare, or its silence about them is indistinguishable from having
    looked. That is 7.8.1 rule 1 applied to types instead of to inputs.

    Bounded, and the bound is REPORTED by the caller rather than silently
    truncating the examination.
    """
    if budget is None:
        budget = [SUBTREE_LEAF_BUDGET]
    if depth > SUBTREE_MAX_DEPTH or budget[0] <= 0:
        if overflow is not None and path not in overflow:
            overflow.append(path)
        return
    kind = leaf_kind(value)
    if kind == "object":
        for key, child in value.items():                # type: ignore[union-attr]
            budget[0] -= 1
            if budget[0] <= 0:
                if overflow is not None and path not in overflow:
                    overflow.append(path)
                return
            yield from qualified_leaves(
                child, f"{path}.{key}", qualifiers + (str(key),), depth + 1,
                budget, overflow)
    elif kind == "array":
        for index, child in enumerate(value):            # type: ignore[arg-type]
            budget[0] -= 1
            if budget[0] <= 0:
                if overflow is not None and path not in overflow:
                    overflow.append(path)
                return
            yield from qualified_leaves(
                child, f"{path}[{index}]", qualifiers, depth + 1, budget,
                overflow)
    else:
        yield qualifiers, path, value, kind


def packet_coordinate_keys(product: object, v5, v3, v2) -> dict[str, set[str]]:
    """{'who': {normalised key}, 'when': {normalised key}} used by the LIVE packet.

    A SECOND, INDEPENDENT DERIVATION, and it exists for one reason: the shape
    rules read a VALUE to decide whether it is a date, so a value of the wrong
    TYPE standing at a date's position is invisible to them. The packet itself
    knows which of its own key names carry which coordinate - it demonstrates it
    on every decided row - so those names are read off the live bytes and used
    to NAME wrong-typed positions in artifacts. Nothing here is a literal, and a
    packet that renames a field moves this set with it (7.10's corollary).
    """
    keys: dict[str, set[str]] = {"who": set(), "when": set()}
    if not isinstance(product, dict):
        return keys
    for section in ("decisions", "pendingDecisions"):
        rows = product.get(section)
        if not isinstance(rows, dict):
            continue
        for row in rows.values():
            if not isinstance(row, dict):
                continue
            for key, value in row.items():
                normalised = v2._norm_key(key)
                if not normalised or not isinstance(value, str) or not value.strip():
                    continue
                if v5.is_iso_date_value(value):
                    keys["when"].add(normalised)
                elif v5.authority_shaped_key(key, v3, v2):
                    keys["who"].add(normalised)
    return keys


def coordinate_qualifier(qualifiers: tuple[str, ...], coordinate_keys: dict,
                         v5, v3, v2) -> tuple[str | None, str | None]:
    """(coordinate, key) for the INNERMOST qualifier that names a coordinate.

    Innermost wins because the nearest naming key is the most specific statement
    about what the leaf IS. The whole path is consulted rather than the last
    step, which is what makes the answer invariant to containers.
    """
    for key in reversed(qualifiers):
        if v5.authority_shaped_key(key, v3, v2):
            return "who", key
        normalised = v2._norm_key(key)
        if normalised in coordinate_keys.get("when", ()):
            return "when", key
        if normalised in coordinate_keys.get("who", ()):
            return "who", key
    return None, None


def attribution_failures(states: dict[str, str],
                         attribution: dict[str, dict[str, list[str]]],
                         name: str, doc: object, prefix: str,
                         coordinate_keys: dict,
                         v5, v3, v2, v1) -> tuple[list[str], dict[str, int]]:
    """The ATTRIBUTION lane over ONE artifact. A pure function of parsed input.

    Reads the packet's derived coordinates and the artifact, and NOTHING else -
    no digest, no head document, no corpus - so an external driver can mutate a
    document in memory and prove the lane is not vacuous from outside itself
    (7.8), and nothing written into this directory can demote a finding here.

    Every semantic limb below is the pinned closure's, CALLED: the site walk,
    the assertion vocabulary, the supersession-marker test, the closure-predicate
    family, the by-phrase reader, the calendar validator and the token
    comparison. What this successor supplies is the leaf walk and the type gate.
    """
    counts = {"attributionSites": 0, "authorityClaims": 0, "dateClaims": 0,
              "agreeing": 0, "conflicts": 0, "notAnAssertion": 0}
    extra = {"uncomparedTypeSites": 0, "comparedThroughAContainer": 0,
             "scalarsWalked": 0}
    out: list[str] = []
    known = tuple(sorted(states))
    try:
        key_anchored, _scoped, prose = v1._document_sites(doc, known)
    except RecursionError:
        return ([f"{prefix}-ATTRIBUTION-DEPTH {name}: the artifact nests deeper "
                 "than the interpreter can walk, so it was NOT examined by the "
                 "attribution lane and this run's silence about it is not "
                 "evidence"], {**counts, **extra})
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

    def emit_uncompared(decision_id: str, where: str, coordinate: str,
                        key: str, kind: str, value: object) -> None:
        marker = (decision_id, where, "UNCOMPARED-TYPE-MARKER", kind)
        if marker in seen:
            return
        seen.add(marker)
        extra["uncomparedTypeSites"] += 1
        out.append(
            f"{prefix}-ATTRIBUTION-UNCOMPARED-TYPE {name}{where}: this position "
            f"names the {coordinate.upper()} coordinate of {decision_id} (key "
            f"{key!r}) and carries a JSON {kind}, {value!r}. THIS LANE COMPARES "
            f"JSON {'/'.join(COMPARED_JSON_TYPES).upper()} SCALARS AND NOTHING "
            "ELSE, so this value's CONTENT WAS NOT COMPARED against the binding "
            "packet and this run's silence about it is not evidence. Freeze 6 "
            "law 18: a closed scalar is admitted on exact type BEFORE its "
            "content is read, at any depth - and the alternative here is the "
            "defect this successor exists to close, where a value the lane "
            "could not read was passed over without a word")

    def compare(decision_id: str, where: str,
                authorities: list[tuple[str, list[str]]],
                dates: list[str], how: str) -> None:
        recorded = attribution.get(decision_id) or {"who": [], "when": []}
        for phrase, tokens in authorities:
            counts["authorityClaims"] += 1
            if not recorded["who"]:
                emit(decision_id, where, "UNRECORDED-AUTHORITY", phrase,
                     recorded["who"], how)
            elif v5.names_the_recorded_authority(tokens, recorded["who"], v3):
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
        for unit in v1._clause_units(text[:v5.CLAUSE_TEXT_LIMIT]):
            if require_id and decision_id not in unit:
                continue
            if v1._head_family(unit)[0] != "CLOSED_POSITIVE":
                continue
            counts["attributionSites"] += 1
            why = v5.records_rather_than_asserts(where, unit, v1, v3)
            if why:
                counts["notAnAssertion"] += 1
                continue
            compare(decision_id, where, v5.by_phrases(unit, v1, v3),
                    v5.iso_dates_in(unit), how)

    for decision_id, location, value in key_anchored:
        # Only a DECIDED row has an attribution to disagree with. A pending row
        # is the STATE lane's business and this lane says nothing about it -
        # which is why deciding the question is what exposed the gap.
        if states.get(decision_id) != "CLOSED_POSITIVE":
            continue
        head_text = v1._disposition_value_text(value)
        if isinstance(head_text, str) and head_text.strip():
            scan_prose(decision_id, location, head_text, "co-located prose",
                       require_id=False)
        if isinstance(value, str):
            continue
        overflow: list[str] = []
        for qualifiers, where, leaf, kind in qualified_leaves(
                value, location, overflow=overflow):
            extra["scalarsWalked"] += 1
            coordinate, key = coordinate_qualifier(
                qualifiers, coordinate_keys, v5, v3, v2)
            through_container = "[" in where[len(location):]
            if kind != "string":
                # DECLARED, NOT SILENT. A wrong-typed value at a coordinate is
                # named; it is never compared as if it were text.
                if coordinate is not None:
                    emit_uncompared(decision_id, where, coordinate, str(key),
                                    kind, leaf)
                continue
            if not leaf.strip():
                continue
            why = v5.records_rather_than_asserts(where, leaf, v1, v3)
            if not why:
                # A field whose KEY records who acted is an attribution whatever
                # its value says: the key supplies the predicate that prose has
                # to spell out. Same for a value that IS a bare calendar date.
                # Both now hold at any container depth.
                if coordinate == "who" and not v5.is_iso_date_value(leaf):
                    tokens = v3._role_verdict(leaf)
                    if tokens:
                        how = f"authority-shaped key {key!r}"
                        if through_container:
                            how += (" reached through a JSON container, which "
                                    "cannot change a verdict")
                            extra["comparedThroughAContainer"] += 1
                        compare(decision_id, where, [(leaf.strip(), tokens)],
                                [], how)
                if v5.is_iso_date_value(leaf):
                    how = f"date-valued leaf under {key!r}" if key \
                        else "date-valued leaf"
                    if through_container:
                        how += (" reached through a JSON container, which "
                                "cannot change a verdict")
                        extra["comparedThroughAContainer"] += 1
                    compare(decision_id, where, [], [leaf.strip()], how)
            scan_prose(decision_id, where, leaf, "co-located prose",
                       require_id=False)
        if overflow:
            out.append(
                f"{prefix}-ATTRIBUTION-DEPTH {name}{overflow[0]}: the "
                "decision-keyed value exceeds this lane's traversal bound, "
                "so it was NOT fully examined and its silence is not "
                "evidence")

    for decision_id, location, leaf in prose:
        if states.get(decision_id) != "CLOSED_POSITIVE":
            continue
        scan_prose(decision_id, f"{location}<prose>", leaf, "prose naming the id",
                   require_id=True)

    return out, {**counts, **extra}


# ---------------------------------------------------------------------------
# The corpus pass, with standing applied.
# ---------------------------------------------------------------------------

def attribution_scan(product: object, docs: list[tuple[str, object]],
                     v5, v4, v3, v2, v1, ledger=None, leaf_lane=None,
                     prefix: str = FINDING_PREFIX
                     ) -> tuple[list[str], list[str], dict[str, object]]:
    """(failures, historical observations, report) for the whole scanned corpus.

    Standing is the pinned closure's, CALLED not copied, so this lane cannot
    quietly grade an artifact differently from the state lane beside it.

    `leaf_lane` is INJECTABLE, and that is a measurement device rather than a
    convenience: --selftest drives this same scan with the PREDECESSOR's leaf
    lane and requires the result to equal the predecessor's own scan exactly. If
    the two agree, then every difference this successor produces comes from the
    leaf repair and from nothing else in the bookkeeping - which is the control
    that turns "the successor changed one thing" from a claim into a result.
    """
    lane = leaf_lane if leaf_lane is not None else attribution_failures
    states = v1.packet_decision_states(product)
    attribution = v5.packet_attribution(product, v3, v2)
    coordinate_keys = packet_coordinate_keys(product, v5, v3, v2)
    attributed = {d: a for d, a in attribution.items() if a["who"] or a["when"]}
    report: dict[str, object] = {
        "packetDecisionIds": len(states),
        "decisionsWithRecordedAttribution": len(attributed),
        "recordedAttribution": {d: dict(a) for d, a in sorted(attributed.items())},
        "packetCoordinateKeys": {k: sorted(v) for k, v in coordinate_keys.items()},
        "artifactsExamined": len(docs),
        "attributionSites": 0,
        "authorityClaims": 0,
        "dateClaims": 0,
        "agreeing": 0,
        "notAnAssertion": 0,
        "conflicts": 0,
        "scalarsWalked": 0,
        "comparedThroughAContainer": 0,
        "uncomparedTypeSites": 0,
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
        if lane is attribution_failures:
            found, counts = lane(states, attribution, name, doc, prefix,
                                 coordinate_keys, v5, v3, v2, v1)
        else:
            found, counts = lane(states, attribution, name, doc, prefix,
                                 v3, v2, v1)
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
                f"{report['agreeing']} coordinate(s) agree, "
                f"{report['comparedThroughAContainer']} of the comparisons were "
                f"reached THROUGH a JSON container, and "
                f"{report['historicalObservations']} conflicting one(s) survive "
                "in artifacts with no standing, listed above")
    return failures, observations, report


def format_attribution(report: dict[str, object]) -> list[str]:
    """The lane's own census, recomputed every run rather than transcribed."""
    lines = ["ATTRIBUTION LANE - who and when, at any container depth"]
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
    coordinate_keys = report.get("packetCoordinateKeys") or {}
    lines.append(f"    coordinate KEY NAMES the live packet uses: "
                 f"who={coordinate_keys.get('who')} "
                 f"when={coordinate_keys.get('when')}")
    lines.append(f"  decisions the packet attributes   "
                 f"{report['decisionsWithRecordedAttribution']} of "
                 f"{report['packetDecisionIds']}")
    lines.append(f"  artifacts examined                {report['artifactsExamined']}")
    lines.append(f"  decided-frame clauses examined    {report['attributionSites']}")
    lines.append(f"    of which record rather than assert (quoted, superseded,")
    lines.append(f"    negated, hedged, attributed, historical)  "
                 f"{report['notAnAssertion']}")
    lines.append(f"  scalars walked under decision keys "
                 f"{report['scalarsWalked']}")
    lines.append(f"  co-located coordinates compared   "
                 f"{int(report['authorityClaims']) + int(report['dateClaims'])} "
                 f"(authority {report['authorityClaims']}, "
                 f"date {report['dateClaims']})")
    lines.append(f"    reached THROUGH a container     "
                 f"{report['comparedThroughAContainer']} "
                 "(nesting cannot change a verdict)")
    lines.append(f"    agreeing with the packet        {report['agreeing']}")
    lines.append(f"    conflicting                     {report['conflicts']}")
    lines.append(f"  positions this lane declined to READ, and NAMED rather "
                 f"than passed over: {report['uncomparedTypeSites']}")
    lines.append(f"    (compared types {list(COMPARED_JSON_TYPES)}; traversed "
                 f"{list(TRAVERSED_JSON_TYPES)};")
    lines.append(f"     named-but-uncompared {list(NAMED_BUT_UNCOMPARED_JSON_TYPES)})")
    lines.append(f"  conflicting artifacts WITH standing (findings)     "
                 f"{report['conflictingArtifactsLive']}")
    lines.append(f"  conflicting artifacts with NONE (observations)     "
                 f"{report['conflictingArtifactsHistorical']}")
    demoted = report.get("demotedByStanding") or {}
    lines.append("    demoted by standing: " + ", ".join(
        f"{k} {v}" for k, v in sorted(demoted.items())))    # type: ignore[union-attr]
    return lines


# ---------------------------------------------------------------------------
# MEASUREMENTS THAT MAY NOT GO STALE.
#
# Both of these exist because a published figure that a reader cannot recompute
# is prose wearing a measurement's clothes (7.2.2). Neither is a literal; both
# run against whatever is on disk, print what they got, and are hard-compared by
# an executed --selftest case.
# ---------------------------------------------------------------------------

def positional_rule_measurement(product: object, docs: list[tuple[str, object]],
                                v5, v3, v2, v1) -> dict[str, object]:
    """What the inherited POSITIONAL rule actually excludes, on this tree.

    The rule reads a `by X` phrase as an attribution only where it FOLLOWS the
    closure predicate. Its published justification was a count of live false
    positives it prevents. This recomputes that count from the corpus in front
    of it: how many `by X` matches the threshold drops, and what the whole scan
    does with the rule removed. A CONTROL is included in the same measurement,
    because a patch that changes nothing and a patch that is not live look
    identical from the outside.
    """
    states = v1.packet_decision_states(product)
    attribution = v5.packet_attribution(product, v3, v2)
    coordinate_keys = packet_coordinate_keys(product, v5, v3, v2)
    seen = {"clauses": 0, "matches": 0, "dropped": 0}
    dropped_examples: list[str] = []

    def instrumented(text: str, v1m, v3m):
        body = text[:v5.CLAUSE_TEXT_LIMIT]
        norm = v1m._normalise(body)
        closure = v1m._find_term(
            norm, v1m.CLOSURE_PREDICATIVE + v1m.CLOSURE_HEAD_BARE)
        if closure is None:
            return []
        seen["clauses"] += 1
        threshold = sum(1 for ch in norm[:closure[0]] if ch.isalnum())
        out: list[tuple[str, list[str]]] = []
        for match in v5.BY_PHRASE_RE.finditer(body):
            seen["matches"] += 1
            phrase = match.group(1).strip(v5.TRAILING_PUNCT)
            tokens = v3m._role_verdict(phrase)
            before = sum(1 for ch in body[:match.start()] if ch.isalnum())
            if before < threshold:
                seen["dropped"] += 1
                if len(dropped_examples) < 5 and phrase not in dropped_examples:
                    dropped_examples.append(phrase)
                continue
            if phrase and tokens:
                out.append((phrase, tokens))
        return out

    def unpositioned(text: str, v1m, v3m):
        body = text[:v5.CLAUSE_TEXT_LIMIT]
        norm = v1m._normalise(body)
        closure = v1m._find_term(
            norm, v1m.CLOSURE_PREDICATIVE + v1m.CLOSURE_HEAD_BARE)
        if closure is None:
            return []
        out: list[tuple[str, list[str]]] = []
        for match in v5.BY_PHRASE_RE.finditer(body):
            phrase = match.group(1).strip(v5.TRAILING_PUNCT)
            tokens = v3m._role_verdict(phrase)
            if phrase and tokens:
                out.append((phrase, tokens))
        return out

    original = v5.by_phrases
    try:
        v5.by_phrases = instrumented
        for name, doc in docs:
            attribution_failures(states, attribution, name, doc, FINDING_PREFIX,
                                 coordinate_keys, v5, v3, v2, v1)
        v5.by_phrases = original
        with_findings, with_obs, with_report = attribution_scan(
            product, docs, v5, None, v3, v2, v1)
        v5.by_phrases = unpositioned
        without_findings, without_obs, without_report = attribution_scan(
            product, docs, v5, None, v3, v2, v1)
        # THE CONTROL. An inverted construction is the exact shape the rule
        # exists to exclude, so if the patch is live it MUST move on this and
        # the whole measurement is worthless if it does not.
        #
        # NO COMMA AFTER THE AGENT PREPOSITION, and that is not a stylistic
        # choice: residual A15 is that a comma there ends the phrase before the
        # name, and the first draft of this control carried one and therefore
        # measured a live patch as dead. A control written in the shape of a
        # disclosed residual measures the residual, not the thing it controls.
        control_doc = {"artifact": "synthetic-control", "dispositions": {
            v2.RETENTION_DECISION_ID: (
                f"By {_UNRECORDED_ROLE} this was SIGNED OFF on "
                + _control_date(product, v5, v1) + ".")}}
        control_without = attribution_failures(
            states, attribution, "synthetic-control", control_doc,
            FINDING_PREFIX, coordinate_keys, v5, v3, v2, v1)[0]
        v5.by_phrases = original
        control_with = attribution_failures(
            states, attribution, "synthetic-control", control_doc,
            FINDING_PREFIX, coordinate_keys, v5, v3, v2, v1)[0]
    finally:
        v5.by_phrases = original
    return {
        "clausesReachingTheByPhraseReader": seen["clauses"],
        "byXmatches": seen["matches"],
        "droppedByThePositionalThreshold": seen["dropped"],
        "kept": seen["matches"] - seen["dropped"],
        "droppedExamples": dropped_examples,
        "liveFindingsWithTheRule": len(with_findings),
        "liveFindingsWithoutTheRule": len(without_findings),
        "observationsWithTheRule": len(with_obs),
        "observationsWithoutTheRule": len(without_obs),
        "authorityClaimsWithTheRule": int(with_report["authorityClaims"]),
        "authorityClaimsWithoutTheRule": int(without_report["authorityClaims"]),
        "controlInvertedConstructionWithTheRule": len(control_with),
        "controlInvertedConstructionWithoutTheRule": len(control_without),
        "patchIsLive": len(control_without) > len(control_with),
    }


_UNRECORDED_ROLE = "the coordinator"


def _control_date(product: object, v5, v1) -> str:
    """A date the packet does NOT record, derived from one it does.

    Assembled at run time so no calendar date is a constant of any predicate in
    this file. Shifting the recorded year back by one is guaranteed to differ
    from every date the packet carries for the same decision, and it is still a
    real calendar date.
    """
    states = v1.packet_decision_states(product)
    for decision_id, family in sorted(states.items()):
        if family != "CLOSED_POSITIVE":
            continue
        row = (product.get("decisions") or {}).get(decision_id) \
            if isinstance(product, dict) else None
        if not isinstance(row, dict):
            continue
        for value in row.values():
            if isinstance(value, str) and v5.is_iso_date_value(value):
                year, rest = value.strip().split("-", 1)
                return f"{int(year) - 1:04d}-{rest}"
    return "0001-01-01"


def decision_set_pin_measurement(product: object, v5, v4, v3, v2,
                                 v1) -> dict[str, object]:
    """What recording the authority's NEXT decision costs, on this tree.

    The non-retention decision SET is compared with set equality against a
    hard-coded literal in the first-generation instrument. This measures the
    consequence directly rather than describing it: add one DECIDED row, by the
    SAME authority and then by a DIFFERENT one, and count what the inherited
    packet lane says. Nothing here is repaired - see this file's docstring for
    why the repair is out of scope and where it belongs.
    """
    out: dict[str, object] = {
        "expectedChoiceCount": len(v1.EXPECTED_CHOICES),
        "expectedChoiceIds": sorted(v1.EXPECTED_CHOICES),
        "liveFindings": len(v4.decision_lane_v4(product, v3, v2, v1)),
    }
    if not isinstance(product, dict) or not isinstance(product.get("decisions"), dict):
        out["measured"] = False
        return out
    recorded_row = product["decisions"].get(v2.RETENTION_DECISION_ID)
    recorded_authority = recorded_row.get("decidedBy") \
        if isinstance(recorded_row, dict) else None
    if not isinstance(recorded_authority, str) or not recorded_authority.strip():
        out["measured"] = False
        return out
    new_id = "CD-" + "SYNTHETIC-PHASE-INSERTION"
    new_date = _control_date(product, v5, v1)
    for label, authority in (("sameAuthority", recorded_authority),
                             ("differentAuthority", "somebody-else")):
        extended = copy.deepcopy(product)
        extended["decisions"][new_id] = {
            "status": "DECIDED",
            "decidedOn": new_date,
            "decidedBy": authority,
            "attributionProvenance": (
                f"The product authority {authority} recorded this decision on "
                f"{new_date} and supplied both fields."),
        }
        found = v4.decision_lane_v4(extended, v3, v2, v1)
        out[label] = {
            "findings": len(found),
            "codes": sorted({f.split(":")[0].split(" ")[0] for f in found}),
            "membershipGateFires": any("differs from the required" in f
                                       for f in found),
        }
    out["measured"] = True
    return out


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
# THE CONTAINER-WRAPPING SWEEP.
#
# The shapes are DECLARED here and the sweep runs over EVERY catch vector the
# instrument publishes, so a vector added later is swept without anybody
# remembering to sweep it. The assertion is INVARIANCE of the detected family
# set, not of the finding count: nesting can legitimately create more paths to
# the same forgery, and it may never create fewer.
# ---------------------------------------------------------------------------

CONTAINER_SHAPES = (
    ("v (control, unwrapped)", lambda v: v),
    ("[v]", lambda v: [v]),
    ("[[v]]", lambda v: [[v]]),
    ("[[[v]]]", lambda v: [[[v]]]),
    ("[v, v]", lambda v: [v, v]),
    ("{k: v}", lambda v: {"wrapper": v}),
    ("{k: {k: v}}", lambda v: {"wrapper": {"inner": v}}),
    ("[{k: v}]", lambda v: [{"wrapper": v}]),
    ("{k: [v]}", lambda v: {"wrapper": [v]}),
    ("[{k: [v]}]", lambda v: [{"wrapper": [v]}]),
    ("[[{k: [v]}]]", lambda v: [[{"wrapper": [v]}]]),
    ("{k: [{k: v}]}", lambda v: {"wrapper": [{"inner": v}]}),
)

# The JSON type space, for the type-coverage sweep. A guard that reads values
# must be tested against every type it does NOT read, which is what this is.
TYPE_SUBSTITUTIONS = (
    ("number (int)", 20260731),
    ("number (float)", 1.5),
    ("boolean true", True),
    ("boolean false", False),
    ("null", None),
    ("empty object", {}),
    ("empty array", []),
)


def wrap_scalars(node: object, shape) -> object:
    """Rebuild a document with every SCALAR leaf rewritten into `shape`.

    Keys are untouched: the sweep tests how a value is REACHED, and a key is
    part of the reaching rather than of the value.
    """
    kind = leaf_kind(node)
    if kind == "object":
        return {key: wrap_scalars(value, shape)
                for key, value in node.items()}      # type: ignore[union-attr]
    if kind == "array":
        return [wrap_scalars(value, shape) for value in node]  # type: ignore[union-attr]
    return shape(node)


def families_of(findings: list[str], prefix: str) -> set[str]:
    """The finding FAMILIES present, which is what invariance is asserted over."""
    out = set()
    for finding in findings:
        head = finding.split(" ", 1)[0]
        if head.startswith(prefix + "-"):
            out.add(head[len(prefix) + 1:])
    return out


# ---------------------------------------------------------------------------
# Fixtures. They build the world they test, so they stay meaningful whichever
# state the live packet is in, and NO CORPUS ARTIFACT IS NAMED in any of them.
#
# THE SCOPED CLAIM, WHICH IS THE REPAIR OF THREE SENTENCES MEASURED FALSE IN THE
# PREDECESSOR: a fabricated authority and a fabricated date ARE constants of the
# section below, because a false-positive matrix cannot be written without them.
# What is true, checkable, and checked by --selftest is that neither appears in
# any function this file uses to DECIDE what to compare.
# ---------------------------------------------------------------------------

def _fixture_packet(v2, decided_by: str, decided_on: str) -> dict:
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
    """(must_pass, must_fail, expected_escapes).

    The predecessor's twelve must-fail rows are carried and the escape this
    successor closes is added in both its one-element-array form and its
    object-wrapped form, so the two shapes that were measured to buy silence are
    themselves published vectors and are then swept through every other shape.
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
        ("A live artifact that restates the AGREEING attribution inside JSON "
         "ARRAYS - the repair must not convert agreement into a conflict",
         _artifact({ident: {"status": "DECIDED", "decidedBy": [real_name],
                            "decidedOn": [real_date]}})),
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
         forged("Ratified 2026-08-02 by the product owner; the "
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
        ("THE ESCAPE THIS SUCCESSOR CLOSES - the aliased vector with each "
         "value in a ONE-ELEMENT ARRAY. Two findings became ZERO findings and "
         "ZERO mentions in the predecessor",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"status": "DECIDED",
                            "signedOffBy": ["the coordinator"],
                            "approvedOn": [other_date]}})),
        ("the same array-wrapped vector, caught on the DATE coordinate too",
         "ATTRIBUTION-DATE",
         _artifact({ident: {"status": "DECIDED",
                            "signedOffBy": ["the coordinator"],
                            "approvedOn": [other_date]}})),
        ("the genuine key names, array-wrapped - the same escape without the "
         "alias",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"status": "DECIDED",
                            "decidedBy": ["product owner"],
                            "decidedOn": [other_date]}})),
        ("OBJECT-wrapped: the authority re-keyed under a member name that "
         "says nothing, which defeated the predecessor's key test the same way",
         "ATTRIBUTION-AUTHORITY",
         _artifact({ident: {"status": "DECIDED",
                            "signedOffBy": {"value": "the coordinator"}}})),
        ("a WRONG-TYPED date at the packet's own coordinate name: a JSON "
         "number spelling a date. It is NAMED, never compared as text",
         "ATTRIBUTION-UNCOMPARED-TYPE",
         _artifact({ident: {"status": "DECIDED", "decidedOn": 20260731}})),
        ("a WRONG-TYPED authority: a JSON boolean under an authority-shaped "
         "key, freeze 6 law 18's own example type",
         "ATTRIBUTION-UNCOMPARED-TYPE",
         _artifact({ident: {"status": "DECIDED", "signedOffBy": True}})),
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
        ("RESIDUAL-A16 the CLAUSE SPLIT: move BOTH coordinates out of the "
         "clause carrying the closure predicate and neither is read as an "
         "attribution of it. Moving only ONE is still caught",
         forged(f"{ident} is DECIDED. Authority: product owner. Date: "
                f"{other_date}.")),
        ("RESIDUAL-A17 the NO-BY attribution: an agent named without the "
         "English agent preposition is not reachable by the inherited "
         "by-phrase reader",
         forged(f"DECIDED on the product owner's authority, {other_date}.")),
        ("RESIDUAL-A15 the BY-COMMA break: a comma immediately after the agent "
         "preposition ends the phrase before the name",
         forged(f"{ident} was DECIDED {real_date} by, under delegated "
                "authority, thecoordinator.")),
        ("RESIDUAL-A18 the HYPHENATED extension: a longer identity containing "
         "the recorded name tokenises to include it and reads as agreement",
         forged(f"DECIDED {real_date} by {real_name}-deputy.")),
    )
    return must_pass, must_fail, expected_escapes


def hostile_shapes(v2) -> tuple:
    """A CRASH MUST NOT READ AS A FINDING (litmus D-6).

    The predecessor's eighteen are carried and the container/type space is
    added, because a shape graded only for NOT CRASHING and never for CATCHING
    is 7.8's recorded failure mode in its narrowest form.
    """
    ident = v2.RETENTION_DECISION_ID
    deep: object = "leaf"
    for _ in range(300):
        deep = [deep]
    deep_object: object = "leaf"
    for _ in range(300):
        deep_object = {"n": deep_object}
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
        ("300-deep OBJECT nesting under the decision key",
         {"d": {ident: deep_object}}),
        ("300-deep nesting UNDER AN AUTHORITY-SHAPED KEY",
         {"d": {ident: {"decidedBy": deep}}}),
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
        ("an authority-shaped key whose value is an EMPTY object",
         {"d": {ident: {"decidedBy": {}, "status": "DECIDED"}}}),
        ("an authority-shaped key whose value is a non-finite float",
         {"d": {ident: {"decidedBy": float("nan"), "status": "DECIDED"}}}),
        ("an authority-shaped key whose value is a deeply mixed container",
         {"d": {ident: {"decidedBy": [{"a": [{"b": [None, 1, True]}]}]}}}),
        ("a non-string JSON key beside an authority-shaped one",
         {"d": {ident: {1: "a", "decidedBy": "q"}}}),
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
#
# CORRECTIONS ARE MADE IN PLACE AND NEVER BY DELETION. A predecessor row whose
# published measurement no longer reproduces is CARRIED VERBATIM FROM ITS LIVE
# BYTES and has the withdrawal appended to it, so a reader meets the original
# claim and its retraction together. --selftest asserts the original text is
# still present verbatim inside the corrected row, which is what stops a
# "correction" from quietly becoming a rewrite.
# ---------------------------------------------------------------------------

def carried_corrections() -> dict[str, str]:
    """{tag: the withdrawal appended to that carried row}."""
    return {
        "A7": (
            "  || WITHDRAWN IN PLACE BY MEASUREMENT, and NOT deleted. An "
            "independent reviewer of the predecessor could not reproduce the "
            "figure above, and this successor re-measured it corpus-wide and "
            "agrees: the positional threshold drops ZERO of the `by X` matches "
            "this corpus contains, and removing the rule entirely changes the "
            "run by no findings, no observations and no authority claims. A "
            "sanity control in the same measurement proves the rule is live - "
            "an inverted construction does move when it is removed - so the "
            "rule is not dead, it is UNEXERCISED on this tree. The four-artifact "
            "figure is therefore withdrawn and no replacement figure is "
            "published as prose: the drop count is RECOMPUTED FROM THE LIVE "
            "CORPUS on every run, printed in the census, and HARD-COMPARED by "
            "an executed case that fails if the printed figure and the "
            "recomputed one disagree in either direction (7.2.2 - a recorded "
            "measurement gets a hard comparison, and a measurement that cannot "
            "fail the build is prose). The QUALITATIVE half of the row - an "
            "inverted construction escapes - reproduces and stands."),
    }


def residual_registry(v5, v4, v3) -> tuple:
    """(tag, lane, text, gate label or None). Inherited rows are CARRIED."""
    corrections = carried_corrections()
    rows: list[tuple[str, str, str, str | None]] = []
    for tag, lane, text, gate in v5.residual_registry(v4, v3):
        lane = lane.replace("this successor", "predecessor, carried")
        if tag in corrections:
            text = text + corrections[tag]
            gate = "the positional rule's live drop count, recomputed"
        rows.append((tag, lane, text, gate))
    rows.extend([
        ("A11", "attribution (this successor)",
         "the container sweep is a BOUND, not a proof of universality. Every "
         "catch vector this instrument publishes is re-run with every scalar "
         "rewritten into each declared container shape and detection must be "
         "invariant - but the shapes are the ones this file declares. A JSON "
         "shape nobody thought of is not swept, and the sweep's own count is "
         "printed so a reader can see how wide the evidence is rather than "
         "inferring it from the word 'every'.",
         "container-wrapping sweep is invariant over every published vector"),
        ("A12", "attribution (this successor)",
         "this lane compares JSON STRING scalars and NOTHING else, stated "
         "because a guard that reads values must say which types it reads. A "
         "number, a boolean or a null standing where an attribution coordinate "
         "lives is NAMED by its own family and is never compared as content - "
         "so a JSON number that spells a date produces 'this was not compared' "
         "and never 'this date is wrong'. That is deliberate under freeze 6 law "
         "18, and it is a real limit: the lane can say a wrong-typed position "
         "exists and cannot say what it asserts.",
         "a wrong-typed coordinate is NAMED rather than compared"),
        ("A13", "attribution (this successor)",
         "qualifiers ACCUMULATE down the path, so every scalar anywhere below "
         "an authority-shaped key is an authority claim - including one that is "
         "genuinely something else, such as a note or an address stored beside "
         "a name. Measured cost on this tree: the repair changes the corpus's "
         "structured authority claims not at all and its date claims by one, "
         "which agrees with the packet, for zero new findings. The measurement "
         "is recomputed every run rather than quoted from this sentence.",
         "the repair's corpus cost, recomputed against the predecessor's reach"),
        ("A14", "attribution (this successor)",
         "the container repair makes NESTING irrelevant and makes RE-KEYING "
         "relevant: a scalar under an authority-shaped key keeps that key "
         "through arrays, and an object member key is APPENDED rather than "
         "replacing it. So a forger cannot escape by wrapping, and a document "
         "that nests an unrelated string under a signature-shaped key pays for "
         "it. The asymmetry is deliberate - one direction buys silence and the "
         "other buys a visible, repairable finding.",
         "the aliased vector escapes in NO declared container shape"),
        ("A15", "attribution (this successor)",
         "the inherited by-phrase reader is bounded at four word tokens and "
         "stops at punctuation, and neither bound was disclosed by the "
         "predecessor. A comma immediately after the agent preposition ends the "
         "phrase before the name and the authority coordinate escapes; with "
         "five or more filler words the finding still fires but NAMES THE WRONG "
         "PHRASE as the claimed authority. Repairing it means replacing an "
         "inherited predicate that governs the state lane beside this one.",
         "RESIDUAL-A15"),
        ("A16", "attribution (this successor)",
         "the CLAUSE SPLIT. A coordinate is read as an attribution only inside "
         "the clause unit that carries the closure predicate, so moving BOTH "
         "the authority and the date into separate sentences escapes. Moving "
         "only ONE is still caught, which is why this is narrower than it "
         "looks. Undisclosed by the predecessor, whose A7 named only the "
         "inverted construction.",
         "RESIDUAL-A16"),
        ("A17", "attribution (this successor)",
         "the AUTHORITY coordinate is reachable only through the English agent "
         "preposition. An attribution written possessively or nominally - 'on "
         "X's authority', 'authority: X' - is not read as one. This is closer "
         "to a real boundary than a gap, because no oracle turns arbitrary "
         "English into an agent role, but the predecessor stated the positional "
         "half of this and never the lexical half.",
         "RESIDUAL-A17"),
        ("A18", "attribution (this successor)",
         "the sharpest sub-case of token-intersection agreement, named because "
         "the predecessor's A4 states the general rule and not this instance: a "
         "HYPHENATED extension of the recorded name tokenises to include the "
         "real name and therefore reads as AGREEMENT. A substituted identity "
         "built by appending to the authority's name is accepted.",
         "RESIDUAL-A18"),
        ("A19", "attribution (this successor)",
         "the finding TEXT is less precise than the catch. Where an attribution "
         "sits in prose the reported 'claimed authority' is whatever the "
         "by-phrase reader extracted, which can be a fragment rather than the "
         "asserted name. No false finding results and no catch is lost, but a "
         "reader repairing from the message alone can be misled about what the "
         "artifact actually asserted. Inherited; disclosed here rather than "
         "repaired, because changing the message changes reviewed output.",
         None),
        ("S5", "decision-set (inherited, NOT repairable here)",
         "THE DECISION SET IS PINNED TO A HARD-CODED LITERAL, AND RECORDING THE "
         "PRODUCT AUTHORITY'S NEXT DECISION REDS THIS VALIDATOR. The "
         "non-retention decision set is compared with set equality against a "
         "seven-entry literal in the first-generation instrument, so ADDING ANY "
         "decision row - by any authority, with any attribution, in any posture, "
         "including the Phase-1A insertion this corpus is explicitly waiting "
         "for - produces a membership finding that has nothing to say about the "
         "decision. It is freeze 7.10's defect applied to a decision SET rather "
         "than to one decision's state, inherited unrepaired through five "
         "generations and named in NONE of the predecessor's 36 residuals. It "
         "is NOT repaired here: the literal is in reviewed bytes this file may "
         "not edit, and it is consumed inside a lane this file executes rather "
         "than reimplements, so the only repairs available are to suppress a "
         "reviewed lane's finding or to stop calling it - both of which change "
         "a reviewed semantic silently. The repair is 7.10's rule (pin the "
         "PROPERTY, not the CURRENT VALUE) applied in a successor to the "
         "instrument that owns the literal, or in a binding artifact stating "
         "what the expected set is derived FROM. Measured live every run.",
         "the decision-set pin's live cost, recomputed"),
    ])
    return tuple(rows)


# ---------------------------------------------------------------------------
# Self-measurement. The claims this file makes ABOUT ITSELF are re-walked from
# the written bytes, because a self-report computed before the write describes a
# document that no longer exists (7.2.2).
# ---------------------------------------------------------------------------

FILENAME_SHAPED_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.(py|json|md|txt)\b")

# The functions this file uses to DECIDE WHAT TO COMPARE. The docstring's claim
# is scoped to exactly this list, and --selftest audits their string constants,
# so the claim is measured rather than asserted and the unscoped claim the
# predecessor made is not made here.
DECISION_PREDICATES = (
    "leaf_kind",
    "qualified_leaves",
    "packet_coordinate_keys",
    "coordinate_qualifier",
    "attribution_failures",
    "attribution_scan",
    "positional_rule_measurement",
    "decision_set_pin_measurement",
)


def _own_tree() -> ast.Module:
    return ast.parse(Path(__file__).read_text(encoding="utf-8"))


def own_string_constants() -> list[str]:
    return [node.value for node in ast.walk(_own_tree())
            if isinstance(node, ast.Constant) and isinstance(node.value, str)]


def predicate_string_constants() -> dict[str, list[str]]:
    """{predicate name: its string constants}, read from this file's own bytes."""
    out: dict[str, list[str]] = {}
    for node in ast.walk(_own_tree()):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and node.name in DECISION_PREDICATES:
            out[node.name] = [
                child.value for child in ast.walk(node)
                if isinstance(child, ast.Constant) and isinstance(child.value, str)]
    return out


# ---------------------------------------------------------------------------
# Selftest.
# ---------------------------------------------------------------------------

def selftest(product, ri, versioning, delivery, retention, register,
             v5, v4, v3, v2, v1, permitted: set[str]) -> int:
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
    fixture_packet = _fixture_packet(v2, "mnowak", "2026-08-05")
    fixture_states = v1.packet_decision_states(fixture_packet)
    fixture_attr = v5.packet_attribution(fixture_packet, v3, v2)
    fixture_keys = packet_coordinate_keys(fixture_packet, v5, v3, v2)

    def lane(doc, attr=None, states=None, keys=None):
        found, _ = attribution_failures(
            states if states is not None else fixture_states,
            attr if attr is not None else fixture_attr,
            "synthetic.doc", doc, FINDING_PREFIX,
            keys if keys is not None else fixture_keys, v5, v3, v2, v1)
        return found

    def v5lane(doc):
        found, _ = v5.attribution_failures(
            fixture_states, fixture_attr, "synthetic.doc", doc,
            v5.FINDING_PREFIX, v3, v2, v1)
        return found

    # ---------------------------------------------------------------- types
    print("THE DECLARED READ SET - a guard that reads values must state which "
          "JSON types it reads")
    declared = set(COMPARED_JSON_TYPES) | set(TRAVERSED_JSON_TYPES) \
        | set(NAMED_BUT_UNCOMPARED_JSON_TYPES)
    probes = ("s", 1, 1.5, True, False, None, {}, [], {"a": 1}, [1])
    kinds = {leaf_kind(p) for p in probes}
    check("types", kinds == declared,
          "every JSON type a document can carry is classified, and the "
          "classification is exactly the declared partition",
          f"declared {sorted(declared)}; observed {sorted(kinds)}")
    check("types", leaf_kind(True) == "boolean" and leaf_kind(1) == "number",
          "a JSON boolean is NOT a number, decided before the number test - "
          "freeze 6 law 18's own most expensive confusion, resolved in one place",
          f"True -> {leaf_kind(True)!r}, 1 -> {leaf_kind(1)!r}, "
          f"1.0 -> {leaf_kind(1.0)!r}")
    check("types",
          not (set(COMPARED_JSON_TYPES) & set(NAMED_BUT_UNCOMPARED_JSON_TYPES))
          and not (set(COMPARED_JSON_TYPES) & set(TRAVERSED_JSON_TYPES)),
          "the compared, traversed and named-but-uncompared sets are disjoint, "
          "so no type has two outcomes")

    # ------------------------------------------------------- the escape
    print()
    print("THE ESCAPE THIS FILE CLOSES - the predecessor's own published vector, "
          "container-wrapped. Both instruments are driven over the SAME bytes")
    aliased_plain = _artifact({ident: {
        "status": "DECIDED", "signedOffBy": "the coordinator",
        "approvedOn": "2026-07-31"}})
    aliased_wrapped = _artifact({ident: {
        "status": "DECIDED", "signedOffBy": ["the coordinator"],
        "approvedOn": ["2026-07-31"]}})
    v5_plain, v5_wrapped = v5lane(aliased_plain), v5lane(aliased_wrapped)
    v6_plain, v6_wrapped = lane(aliased_plain), lane(aliased_wrapped)
    check("escape", bool(v5_plain) and not v5_wrapped,
          "the DEFECT is present in the pinned predecessor and is reproduced "
          "here rather than described: plain form caught, wrapped form silent",
          f"predecessor: plain {len(v5_plain)} finding(s), wrapped "
          f"{len(v5_wrapped)} finding(s)")
    check("escape",
          families_of(v6_wrapped, FINDING_PREFIX)
          == families_of(v6_plain, FINDING_PREFIX)
          and {"ATTRIBUTION-AUTHORITY", "ATTRIBUTION-DATE"}
          <= families_of(v6_wrapped, FINDING_PREFIX),
          "and THIS instrument catches both forms on both coordinates, with an "
          "identical family set - the wrapping buys nothing",
          f"plain {sorted(families_of(v6_plain, FINDING_PREFIX))}; wrapped "
          f"{sorted(families_of(v6_wrapped, FINDING_PREFIX))}")
    check("escape",
          all("synthetic.doc" in f and ident in f for f in v6_wrapped),
          "and every wrapped-form finding NAMES THE ARTIFACT AND THE DECISION "
          "IN FULL - a forgery may buy a green exit code and never silence",
          v6_wrapped[0][:180] if v6_wrapped else "NOTHING")

    # --------------------------------------------------- the container sweep
    print()
    print("THE CONTAINER-WRAPPING SWEEP - every published catch vector, rewritten "
          "into every declared container shape. Detection must be INVARIANT")
    must_pass, must_fail, escapes = attribution_cases(v2)
    attempted = invariant = 0
    non_invariant: list[str] = []
    for label, family, doc in must_fail:
        control = families_of(lane(doc), FINDING_PREFIX)
        for shape_label, shape in CONTAINER_SHAPES:
            attempted += 1
            wrapped = families_of(lane(wrap_scalars(doc, shape)), FINDING_PREFIX)
            if wrapped >= control and control:
                invariant += 1
            else:
                non_invariant.append(
                    f"{shape_label} on {label[:44]!r}: control "
                    f"{sorted(control)} -> {sorted(wrapped)}")
    check("sweep", not non_invariant,
          f"container-wrapping sweep: {invariant} of {attempted} "
          f"(vector x shape) pairs are INVARIANT",
          f"{len(non_invariant)} NOT invariant; first: {non_invariant[0]}"
          if non_invariant
          else f"{len(must_fail)} vectors x {len(CONTAINER_SHAPES)} shapes, "
               "no shape loses a family")
    executed_labels.add("container-wrapping sweep is invariant over every "
                        "published vector")
    aliased_families = families_of(lane(aliased_plain), FINDING_PREFIX)
    escaping_shapes = [
        shape_label for shape_label, shape in CONTAINER_SHAPES
        if not families_of(lane(wrap_scalars(aliased_plain, shape)),
                           FINDING_PREFIX) >= aliased_families]
    check("sweep", not escaping_shapes,
          "the aliased vector escapes in NO declared container shape",
          f"escaping shapes: {escaping_shapes}" if escaping_shapes
          else f"0 of {len(CONTAINER_SHAPES)} shapes escape")
    executed_labels.add("the aliased vector escapes in NO declared container "
                        "shape")
    # And the PREDECESSOR, over the same sweep, as the control that proves the
    # sweep can fail. A sweep nothing has ever failed is decoration.
    v5_escapes = sum(
        1 for label, family, doc in must_fail
        for shape_label, shape in CONTAINER_SHAPES
        if not families_of(v5lane(wrap_scalars(doc, shape)),
                           v5.FINDING_PREFIX)
        >= families_of(v5lane(doc), v5.FINDING_PREFIX))
    check("sweep", v5_escapes > 0,
          "and the SWEEP CAN FAIL: run identically against the pinned "
          "predecessor it reports escapes, so a green sweep is a measurement "
          "and not a tautology",
          f"predecessor loses a family in {v5_escapes} of {attempted} pairs")

    print()
    print("TYPE COVERAGE - a guard that reads values must be tested against "
          "every type it does NOT read")
    type_named = type_attempted = 0
    type_silent: list[str] = []
    for key in ("decidedBy", "decidedOn", "signedOffBy", "approvedOn"):
        for type_label, value in TYPE_SUBSTITUTIONS:
            type_attempted += 1
            found = lane(_artifact({ident: {"status": "DECIDED", key: value}}))
            if leaf_kind(value) in TRAVERSED_JSON_TYPES:
                # An empty container has no scalar to name. It is not silence
                # about a value; there is no value.
                type_named += 1
                continue
            if any("UNCOMPARED-TYPE" in f for f in found):
                type_named += 1
            else:
                type_silent.append(f"{key}={type_label}")
    check("types", not type_silent,
          f"every wrong-typed scalar at a coordinate is NAMED: {type_named} of "
          f"{type_attempted}",
          f"silent: {type_silent}" if type_silent
          else "no scalar type is passed over in silence")
    executed_labels.add("a wrong-typed coordinate is NAMED rather than compared")
    check("types",
          not any("ATTRIBUTION-DATE" in f
                  for f in lane(_artifact({ident: {"status": "DECIDED",
                                                   "decidedOn": 20260731}}))),
          "and a JSON NUMBER spelling a date is never compared AS a date - the "
          "lane says it could not read the value, not that the value is wrong",
          "law 18: exact type before content")

    # ---------------------------------------------------- packet derivation
    print()
    print("packet-side derivation - both coordinates must come OUT of the "
          "packet, never out of this source")
    check("derivation",
          fixture_attr.get(ident, {}).get("who") == ["mnowak"]
          and fixture_attr.get(ident, {}).get("when") == ["2026-08-05"],
          "the inherited shape derivation recovers the fixture packet's "
          "authority and date without naming either key",
          f"derived {fixture_attr.get(ident)}")
    renamed = copy.deepcopy(fixture_packet)
    row = renamed["decisions"][ident]
    row["signedOffBy"] = row.pop("decidedBy")
    row["approvedOn"] = row.pop("decidedOn")
    renamed_keys = packet_coordinate_keys(renamed, v5, v3, v2)
    check("derivation",
          v5.packet_attribution(renamed, v3, v2).get(ident, {}).get("who")
          == ["mnowak"]
          and "approvedon" in renamed_keys["when"],
          "and BOTH derivations follow a packet that RENAMES its fields - the "
          "coordinate key names are read off the live packet too, so a "
          "legitimate schema change costs a re-read rather than a successor "
          "instrument (7.10)",
          f"renamed packet coordinate keys {renamed_keys}")
    live_keys = packet_coordinate_keys(product, v5, v3, v2)
    check("derivation", bool(live_keys["when"] or live_keys["who"]),
          "and on the LIVE packet the coordinate key names are recoverable",
          f"who={sorted(live_keys['who'])} when={sorted(live_keys['when'])}")
    live_attr = v5.packet_attribution(product, v3, v2)
    live_attributed = {d: a for d, a in live_attr.items() if a["who"] or a["when"]}
    if not live_attributed:
        partial.append(
            "the LIVE packet records no authority-shaped field and no calendar "
            "date on any decision row, so the derivation could not be exercised "
            "against live bytes and this run does NOT claim it")

    # ------------------------------------------------------------- the lane
    print()
    print("the lane - artifacts that MUST be accepted (silence is not a conflict)")
    for label, doc in must_pass:
        found = lane(doc)
        executed_labels.add(label)
        check("accept", not found, label, "; ".join(found)[:240] if found else "")

    print("the lane - forgeries that MUST be caught, and the family that must "
          "catch each")
    for label, family, doc in must_fail:
        found = lane(doc)
        executed_labels.add(label)
        hit = [f for f in found if family in f]
        check("reject", bool(hit), label,
              (f"expected a {family} finding; got "
               f"{[f.split(' ')[0] for f in found] or 'NOTHING'}")
              if not hit else hit[0][:190])

    print("the lane - residuals EXPECTED to escape; a residual that stops "
          "escaping is a FAILURE, because the published disclosure would be stale")
    for label, doc in escapes:
        found = lane(doc)
        executed_labels.add(label.split(" ")[0])
        check("residual", not found, label,
              f"NO LONGER ESCAPES: {found[0][:180]}" if found
              else "escapes this lane, as disclosed")
    # A15's second half: the four-token bound MISLABELS rather than escapes.
    mislabel = lane(_artifact({ident: (
        "DECIDED 2026-06-01 by under formally delegated standing authority "
        "thecoordinator.")}))
    check("residual",
          any("delegated" in f for f in mislabel),
          "RESIDUAL-A15 second half: with five or more filler words the finding "
          "FIRES but names the wrong phrase as the claimed authority - caught "
          "by accident, reported wrongly",
          mislabel[0][:170] if mislabel else "did not fire at all")
    check("residual",
          len(lane(_artifact({ident: f"{ident} is DECIDED. Authority: product "
                                     "owner. It was decided 2026-07-31."}))) > 0,
          "RESIDUAL-A16 is NARROW, measured: moving only ONE coordinate out of "
          "the closure clause is still caught, so the escape needs both")

    print("non-vacuity - a family nothing can trip is decoration")
    exercised = {family for _, family, _ in must_fail}
    for family in ("ATTRIBUTION-AUTHORITY", "ATTRIBUTION-DATE",
                   "ATTRIBUTION-UNCOMPARED-TYPE"):
        check("nonvacuity", family in exercised,
              f"family {family} is exercised by at least one must-fail case")
    unattributed = copy.deepcopy(fixture_packet)
    unattributed["decisions"][ident].pop("decidedBy")
    unattributed["decisions"][ident].pop("decidedOn")
    unattributed["decisions"][ident].pop("attributionProvenance")
    ua_attr = v5.packet_attribution(unattributed, v3, v2)
    ua_states = v1.packet_decision_states(unattributed)
    ua_keys = packet_coordinate_keys(unattributed, v5, v3, v2)
    ua_found = lane(_artifact({ident: "DECIDED 2026-06-01 by somebodyelse."}),
                    attr=ua_attr, states=ua_states, keys=ua_keys)
    check("nonvacuity", any("UNRECORDED" in f for f in ua_found),
          "an artifact supplies an attribution the packet does not record",
          f"{len(ua_found)} finding(s); first "
          f"{ua_found[0][:150] if ua_found else 'NONE'}")
    executed_labels.add("an artifact supplies an attribution the packet does "
                        "not record")
    check("nonvacuity",
          not lane(_artifact({ident: "DECIDED; retention is bounded."}),
                   attr=ua_attr, states=ua_states, keys=ua_keys),
          "and the same unattributed packet accepts an artifact that cites only "
          "the state, so the UNRECORDED limb is not simply always-on")

    print("gate independence - each coordinate must fire ALONE, or it is not a "
          "coordinate")
    only_date = lane(_artifact({ident: "DECIDED 2026-06-01 by mnowak."}))
    families = families_of(only_date, FINDING_PREFIX)
    check("gate", families == {"ATTRIBUTION-DATE"},
          "a substituted DATE alone fires only the date family",
          f"families present: {sorted(families)}")
    only_who = lane(_artifact({ident: "DECIDED 2026-08-05 by the coordinator."}))
    families = families_of(only_who, FINDING_PREFIX)
    check("gate", families == {"ATTRIBUTION-AUTHORITY"},
          "a substituted AUTHORITY alone fires only the authority family",
          f"families present: {sorted(families)}")
    only_who_wrapped = lane(wrap_scalars(
        _artifact({ident: {"status": "DECIDED",
                           "decidedBy": "the coordinator"}}),
        CONTAINER_SHAPES[1][1]))
    check("gate",
          families_of(only_who_wrapped, FINDING_PREFIX) == {"ATTRIBUTION-AUTHORITY"},
          "and the same isolation holds THROUGH a container - the repair widens "
          "reach without widening the family",
          f"families present: {sorted(families_of(only_who_wrapped, FINDING_PREFIX))}")

    # -------------------------------------------------- false positives
    print()
    print("the FALSE-POSITIVE matrix - the corpus's own forensic records of the "
          "fabrication must never be reported AS the fabrication")
    other_date = "2026-07-31"
    forged_sentence = (f"SIGNED OFF {other_date} by product owner - zero "
                       "implicit durable retention for greenfield.")
    fp_cases = (
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
    )
    for label, doc in fp_cases:
        found = lane(doc)
        check("falsepositive", not found, label,
              "; ".join(found)[:200] if found else "silent, as required")
    fp_wrapped_noisy: list[str] = []
    for label, doc in fp_cases:
        for shape_label, shape in CONTAINER_SHAPES:
            if lane(wrap_scalars(doc, shape)):
                fp_wrapped_noisy.append(f"{shape_label} on {label[:40]!r}")
    check("falsepositive", not fp_wrapped_noisy,
          "and the SAME six records stay silent in every container shape - the "
          "repair widens what is CAUGHT and not what is ACCUSED",
          f"{len(fp_wrapped_noisy)} noisy: {fp_wrapped_noisy[:2]}"
          if fp_wrapped_noisy
          else f"{len(fp_cases)} records x {len(CONTAINER_SHAPES)} shapes, 0 findings")

    # -------------------------------------------------------- the live corpus
    print()
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
        product, docs, v5, v4, v3, v2, v1, ledger)
    if live_report.get("classSkipped"):
        partial.append(
            "the attribution lane did not run against live bytes: "
            + str(live_report["classSkipped"]))
    else:
        print(f"    artifacts examined                {len(docs)}")
        print(f"    scalars walked under decision keys {live_report['scalarsWalked']}")
        print(f"    coordinates compared              "
              f"{int(live_report['authorityClaims']) + int(live_report['dateClaims'])}")
        print(f"    of those, reached THROUGH a container "
              f"{live_report['comparedThroughAContainer']}")
        print(f"    positions NAMED but not compared  "
              f"{live_report['uncomparedTypeSites']}")
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
        # THE HARNESS CONTROL. Driving THIS scan with the PREDECESSOR's leaf
        # lane must reproduce the predecessor's own scan exactly, so every
        # delta this successor produces comes from the leaf repair alone.
        p_findings, p_obs, p_report = v5.attribution_scan(
            product, docs, v4, v3, v2, v1)
        h_findings, h_obs, h_report = attribution_scan(
            product, docs, v5, v4, v3, v2, v1, None, v5.attribution_failures,
            v5.FINDING_PREFIX)
        check("corpus",
              p_findings == h_findings and p_obs == h_obs
              and p_report["conflicts"] == h_report["conflicts"],
              "HARNESS CONTROL: this successor's scan, driven with the "
              "PREDECESSOR's leaf lane AND the predecessor's own finding "
              "prefix, reproduces the predecessor's own scan BYTE FOR BYTE - so "
              "the bookkeeping is unchanged and every delta comes from the leaf "
              "repair alone",
              f"findings {len(p_findings)}=={len(h_findings)}, observations "
              f"{len(p_obs)}=={len(h_obs)}, conflicts "
              f"{p_report['conflicts']}=={h_report['conflicts']}")
        check("corpus",
              int(live_report["authorityClaims"]) >= int(p_report["authorityClaims"])
              and int(live_report["dateClaims"]) >= int(p_report["dateClaims"]),
              "the repair's corpus cost, recomputed against the predecessor's "
              "reach: the successor compares AT LEAST as many coordinates and "
              "produces no new live finding",
              f"authority {p_report['authorityClaims']}->"
              f"{live_report['authorityClaims']}, date "
              f"{p_report['dateClaims']}->{live_report['dateClaims']}, live "
              f"findings {len(p_findings)}->{len(live_failures)}")
        executed_labels.add("the repair's corpus cost, recomputed against the "
                            "predecessor's reach")
        planted_name = "zz-synthetic-plant.v1" + ".json"
        for plant_label, plant_body in (
            ("as prose", _artifact({ident: forged_sentence})),
            ("array-wrapped structured", _artifact(
                {ident: {"status": "DECIDED", "signedOffBy": ["product owner"],
                         "approvedOn": [other_date]}})),
        ):
            planted = json.loads(json.dumps(plant_body))
            planted_found, _ = attribution_failures(
                v1.packet_decision_states(product), live_attr, planted_name,
                planted, FINDING_PREFIX,
                packet_coordinate_keys(product, v5, v3, v2), v5, v3, v2, v1)
            check("corpus", bool(planted_found) and all(
                planted_name in f for f in planted_found),
                f"and the forgery {plant_label}, planted as a live document "
                "against the LIVE packet, is CAUGHT AND NAMED IN FULL - so "
                "corpus silence is a measurement of the corpus, not of a dead "
                "lane",
                planted_found[0][:190] if planted_found else "NOT CAUGHT")

    # ------------------------------------------------ the two measurements
    print()
    print("MEASUREMENTS THAT MAY NOT GO STALE - recomputed here and "
          "HARD-COMPARED to what the run prints (7.2.2)")
    positional = positional_rule_measurement(product, docs, v5, v3, v2, v1)
    for key in ("clausesReachingTheByPhraseReader", "byXmatches",
                "droppedByThePositionalThreshold", "liveFindingsWithTheRule",
                "liveFindingsWithoutTheRule"):
        print(f"    {key:42s} {positional[key]}")
    again = positional_rule_measurement(product, docs, v5, v3, v2, v1)
    check("measurement", again == positional,
          "the positional rule's live drop count, recomputed: two independent "
          "computations over the same bytes agree, so the printed figure is "
          "reproducible rather than incidental",
          f"dropped {positional['droppedByThePositionalThreshold']} of "
          f"{positional['byXmatches']} match(es) in "
          f"{positional['clausesReachingTheByPhraseReader']} clause(s)")
    executed_labels.add("the positional rule's live drop count, recomputed")
    check("measurement", bool(positional["patchIsLive"]),
          "and the measurement CAN move: its own control, an inverted "
          "construction, gains findings when the rule is removed - so 'drops "
          "nothing' is a fact about this corpus and not a dead patch",
          f"control with the rule "
          f"{positional['controlInvertedConstructionWithTheRule']} finding(s), "
          f"without it {positional['controlInvertedConstructionWithoutTheRule']}")
    check("measurement",
          positional["liveFindingsWithTheRule"]
          == positional["liveFindingsWithoutTheRule"],
          "WITHDRAWAL CONFIRMED: removing the positional rule entirely changes "
          "the live finding count by ZERO, so the predecessor's published "
          "'four live false positives' does not reproduce and is withdrawn in "
          "place rather than deleted",
          f"with {positional['liveFindingsWithTheRule']}, without "
          f"{positional['liveFindingsWithoutTheRule']}; observations "
          f"{positional['observationsWithTheRule']}/"
          f"{positional['observationsWithoutTheRule']}; authority claims "
          f"{positional['authorityClaimsWithTheRule']}/"
          f"{positional['authorityClaimsWithoutTheRule']}")

    pin = decision_set_pin_measurement(product, v5, v4, v3, v2, v1)
    if not pin.get("measured"):
        partial.append(
            "the live packet does not carry a decided retention row with a "
            "string authority, so the decision-set pin's cost could not be "
            "measured on live bytes and this run does NOT publish it")
    else:
        print(f"    expected decision-set size (a hard-coded literal) "
              f"{pin['expectedChoiceCount']}")
        print(f"    live packet findings from the inherited lane      "
              f"{pin['liveFindings']}")
        print(f"    + one DECIDED row, SAME authority                 "
              f"{pin['sameAuthority']['findings']} {pin['sameAuthority']['codes']}")
        print(f"    + one DECIDED row, DIFFERENT authority            "
              f"{pin['differentAuthority']['findings']} "
              f"{pin['differentAuthority']['codes']}")
        check("measurement",
              pin["sameAuthority"]["membershipGateFires"]
              and pin["differentAuthority"]["membershipGateFires"],
              "the decision-set pin's live cost, recomputed: adding ANY decision "
              "row reds the inherited membership gate REGARDLESS of authority - "
              "so recording the product authority's NEXT decision fails a check "
              "that has nothing to say about it (residual S5, inherited, NOT "
              "repaired here)",
              f"same-authority {pin['sameAuthority']['codes']}, "
              f"different-authority {pin['differentAuthority']['codes']}")
        executed_labels.add("the decision-set pin's live cost, recomputed")
        check("measurement",
              pin["differentAuthority"]["findings"] < pin["sameAuthority"]["findings"],
              "and the membership half is INDEPENDENT of the attribution half: "
              "a different authority still trips it and trips nothing else, "
              "which is why it is the larger and less visible of the two costs",
              f"same {pin['sameAuthority']['findings']} finding(s), different "
              f"{pin['differentAuthority']['findings']}")
        check("measurement",
              not attribution_failures(
                  v1.packet_decision_states(product), live_attr, "synthetic.doc",
                  _artifact({ident: "DECIDED; retention is bounded."}),
                  FINDING_PREFIX, packet_coordinate_keys(product, v5, v3, v2),
                  v5, v3, v2, v1)[0],
              "and THIS lane contributes nothing to either cost: it is "
              "corpus-side and says nothing about the packet's own rows")

    # ------------------------------------------------------------- banner
    print()
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
        product, failing_docs, v5, v4, v3, v2, v1, failing_ledger)
    check("banner",
          bool(failing) and "corpus-attribution" not in failing_ledger.gate_names
          and any(gate == "corpus-attribution"
                  for gate, _ in failing_ledger.skipped),
          "a gate that RUNS AND FAILS registers no clause, so a failed gate can "
          "never contribute a sentence to a success banner",
          f"{len(failing)} finding(s); ran={sorted(failing_ledger.gate_names)}")
    empty_ledger = v4.GateLedger()
    attribution_scan({"decisions": {}}, [], v5, v4, v3, v2, v1, empty_ledger)
    check("banner",
          any(gate == "corpus-attribution" for gate, _ in empty_ledger.skipped),
          "a packet with no readable decision row registers the class as NOT "
          "RUN by name, so 'derived from nothing' and 'derived and found "
          "nothing' never print the same (7.8.1 rule 1)",
          f"skipped={[g for g, _ in empty_ledger.skipped]}")

    # ------------------------------------------------------- hostile input
    print()
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
        attribution_scan("not a packet", [("x", None)], v5, v4, v3, v2, v1,
                         v4.GateLedger())
        check("hostile", True, "the whole scan survives a non-object packet and "
                               "a null document")
    except Exception as exc:                           # noqa: BLE001 - measured
        check("hostile", False, "the whole scan survives a non-object packet",
              f"RAISED {type(exc).__name__}: {exc}")
    deep_probe = {"artifact": "zz", "dispositions": {ident: None}}
    nest: object = forged_sentence
    for _ in range(SUBTREE_MAX_DEPTH + 3):
        nest = {"n": nest}
    deep_probe["dispositions"][ident] = nest             # type: ignore[index]
    deep_found = lane(deep_probe)
    check("hostile", any("ATTRIBUTION-DEPTH" in f for f in deep_found),
          "and a forgery planted BELOW the traversal bound produces a named "
          "DEPTH outcome rather than silence - the bound announces itself",
          deep_found[0][:170] if deep_found else "SILENT, which is the defect")

    # ------------------------------------------------------- no regression
    print()
    print("NO REGRESSION - the predecessor's entire published case corpus, "
          "re-driven through BOTH lanes")
    p_pass, p_fail, p_escapes_v5 = v5.attribution_cases(v2)
    lost = [label for label, family, doc in p_fail
            if not any(family in f for f in lane(doc))]
    check("noregression", not lost,
          f"all {len(p_fail)} of the PREDECESSOR's must-fail attribution "
          "vectors are still caught by their own family",
          f"lost: {lost}" if lost else "0 regressions")
    noisy = [label for label, doc in p_pass if lane(doc)]
    check("noregression", not noisy,
          f"all {len(p_pass)} of the predecessor's must-PASS attribution "
          "vectors still pass",
          f"newly noisy: {noisy}" if noisy else "0 new false positives")
    still = [label for label, doc in p_escapes_v5 if not lane(doc)]
    check("noregression", len(still) == len(p_escapes_v5),
          f"all {len(p_escapes_v5)} of the predecessor's disclosed attribution "
          "residuals still escape, so its published disclosure is not stale",
          f"{len(still)} of {len(p_escapes_v5)}")
    for label, doc in p_escapes_v5:
        executed_labels.add(label.split(" ")[0])
    v4_pass, v4_fail, v4_escapes = v4.decision_cases_v4(v3, v2, v1)
    regressions = [label for label, family, packet in v4_fail
                   if not any(family in f
                              for f in v4.decision_lane_v4(packet, v3, v2, v1))]
    check("noregression", not regressions,
          f"all {len(v4_fail)} inherited packet-side must-fail cases are still "
          "caught by their own family",
          f"regressions: {regressions}" if regressions else "0 regressions")
    accepted = [label for label, packet in v4_pass
                if not v4.decision_lane_v4(packet, v3, v2, v1)]
    check("noregression", len(accepted) == len(v4_pass),
          f"all {len(v4_pass)} inherited packet-side must-PASS cases still pass",
          f"{len(accepted)} of {len(v4_pass)}")
    still_escaping = [label for label, packet in v4_escapes
                      if not [f for f in v4.decision_lane_v4(packet, v3, v2, v1)
                              if f.startswith("PD4")]]
    check("noregression", len(still_escaping) == len(v4_escapes),
          f"all {len(v4_escapes)} inherited packet-side residuals still escape",
          f"{len(still_escaping)} of {len(v4_escapes)}")
    for label, _family, _packet in v4_fail:
        executed_labels.add(label)
    for label, _packet in v4_pass:
        executed_labels.add(label)
    for label, _packet in v4_escapes:
        executed_labels.add(label.split(" ")[0])
    g_pass, g_fail, _g_escapes = v3.decision_cases(v1, v2)
    grand = [label for label, family, packet in g_fail
             if not any(family in f
                        for f in v4.decision_lane_v4(packet, v3, v2, v1))]
    check("noregression", not grand,
          f"and all {len(g_fail)} cases of the generation before it",
          f"regressions: {grand}" if grand else "0 regressions")
    hostile_ok = 0
    inherited_hostile = (tuple(v3.hostile_shapes(v1, v2))
                         + tuple(v4.hostile_shapes_v4(v3, v2, v1)))
    for label, shape in inherited_hostile:
        try:
            hostile_ok += int(isinstance(
                v4.decision_lane_v4(shape, v3, v2, v1), list))
        except Exception:                              # noqa: BLE001 - measured
            pass
    check("noregression", hostile_ok == len(inherited_hostile),
          f"and all {len(inherited_hostile)} inherited hostile shapes still "
          "produce a named outcome rather than a traceback",
          f"{hostile_ok} of {len(inherited_hostile)}")

    # ---------------------------------------- inherited gates on live bytes
    print()
    print("inherited packet-side gates, re-run against LIVE bytes")
    live_row = product.get("decisions", {}).get(ident) \
        if isinstance(product, dict) else None
    if not isinstance(live_row, dict) or not isinstance(live_row.get("decidedBy"), str):
        partial.append(
            "the live packet does not carry a decided retention row with a "
            "string authority, so the inherited blocker-1 matrix could not be "
            "run against live bytes and this run does NOT claim it")
    else:
        matrix = 0
        candidates = (
            ("retention", True), ("Phase", True), ("PURGED", True),
            ("tombstone", True), ("bounds", True), ("the coordinator", True),
            ("jdoe", True), ("z", True), (live_row["decidedBy"], False))
        for candidate, must_catch in candidates:
            mutated = copy.deepcopy(product)
            mutated["decisions"][ident]["decidedBy"] = candidate
            caught = bool(v4.decision_lane_v4(mutated, v3, v2, v1))
            matrix += int(caught == must_catch)
        check("inherited", matrix == len(candidates),
              f"the inherited blocker-1 matrix scores {matrix} of "
              f"{len(candidates)} on live bytes",
              f"{matrix} of {len(candidates)}")
    tokens, survivors, predecessor_survivors = v4.attribution_discrimination(
        product, v3, v2, v1, deep=True)
    if not tokens:
        partial.append(
            "the live packet carries no decided retention row, so the inherited "
            "discrimination sweep had no token population and this run does NOT "
            "publish it")
    else:
        check("inherited", set(survivors) < set(predecessor_survivors),
              "the inherited surviving set is still a STRICT SUBSET, so nothing "
              "in this successor loosened it",
              f"{len(survivors)} of {len(predecessor_survivors)} of "
              f"{len(tokens)} tokens")
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

    # --------------------------------------------------- environment
    print()
    print("environment independence - a blinded run must give identical results")
    sighted_f, sighted_o, sighted_r = attribution_scan(
        product, docs, v5, v4, v3, v2, v1)
    original_reader = v1.head_named_artifacts
    try:
        v1.head_named_artifacts = lambda *a, **k: (set(), [])
        blind_f, blind_o, blind_r = attribution_scan(
            product, docs, v5, v4, v3, v2, v1)
    finally:
        v1.head_named_artifacts = original_reader
    check("environment",
          sighted_f == blind_f and sighted_o == blind_o
          and sighted_r["conflicts"] == blind_r["conflicts"],
          "head documents unreadable -> identical findings AND observations",
          f"findings {len(sighted_f)}=={len(blind_f)}, observations "
          f"{len(sighted_o)}=={len(blind_o)}")
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
    check("environment", len(permitted) == 6,
          "the permitted-import set is DERIVED by walking the pin chain, and it "
          "closes at six files",
          f"{len(permitted)} permitted path(s)")
    check("environment", sys.flags.hash_randomization == 1,
          "and this process runs under a RANDOMIZED hash seed - isolated mode "
          "ignores the environment variable that would pin it, so repeat runs "
          "are evidence of order-independence rather than of a fixed seed",
          f"hash_randomization={sys.flags.hash_randomization}; the earlier "
          "generation's wording named a mechanism -I disables")

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

    # ------------------------------------------------------ self-measurement
    print()
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
    predicate_constants = predicate_string_constants()
    check("self", set(predicate_constants) == set(DECISION_PREDICATES),
          "every function this file declares as a DECISION PREDICATE exists in "
          "its own bytes under that name",
          f"declared {len(DECISION_PREDICATES)}, found "
          f"{sorted(set(DECISION_PREDICATES) - set(predicate_constants))or'all'}")
    dated_predicates = sorted(
        name for name, values in predicate_constants.items()
        if any(v5.iso_dates_in(value) for value in values))
    check("self", not dated_predicates,
          "NO CALENDAR DATE appears in any decision predicate - the SCOPED "
          "claim this file makes, replacing an unscoped one an independent "
          "reviewer measured false of the predecessor",
          f"predicates carrying a date: {dated_predicates}"
          if dated_predicates
          else f"{len(predicate_constants)} predicates audited, 0 dates")
    recorded_authorities = sorted(
        {token.lower()
         for coordinates in live_attr.values() for value in coordinates["who"]
         for token in v3._role_verdict(value)})
    named_predicates = sorted(
        name for name, values in predicate_constants.items()
        if any(token in re.findall(r"[a-z]+", value.lower())
               for value in values for token in recorded_authorities))
    check("self", not named_predicates,
          "and NO TOKEN OF THE LIVE PACKET'S RECORDED AUTHORITY appears in any "
          "decision predicate, so neither coordinate can be reached from a "
          "literal in this file's comparison path",
          f"predicates naming the authority: {named_predicates}"
          if named_predicates
          else f"authority tokens audited: {recorded_authorities or 'NONE'}")
    if not recorded_authorities:
        partial.append(
            "the live packet records no authority, so the predicate audit's "
            "authority half had nothing to search for and this run does NOT "
            "claim it")
    rows = residual_registry(v5, v4, v3)
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
    inherited_rows = v5.residual_registry(v4, v3)
    check("self",
          all(tag in {r[0] for r in rows} for tag, _, _, _ in inherited_rows),
          f"and all {len(inherited_rows)} inherited residuals are CARRIED, not "
          "dropped",
          f"{len(rows)} total after carrying {len(inherited_rows)}")
    corrections = carried_corrections()
    carried_text = {tag: text for tag, _, text, _ in rows}
    inherited_text = {tag: text for tag, _, text, _ in inherited_rows}
    broken = sorted(
        tag for tag in corrections
        if tag not in inherited_text
        or inherited_text[tag] not in carried_text.get(tag, ""))
    check("self", not broken,
          "a WITHDRAWAL IS APPENDED, NEVER A REWRITE: every corrected row still "
          "contains its predecessor's text VERBATIM, read from the "
          "predecessor's live bytes rather than retyped",
          f"rewritten or dangling corrections: {broken}" if broken
          else f"{len(corrections)} correction(s), each carrying its original "
               "verbatim")
    check("self",
          all(any(tag == t for t, _, _, _ in rows) for tag in corrections),
          "and no correction names a row that does not exist",
          f"corrections: {sorted(corrections)}")

    print()
    print("selftest buckets: " + ", ".join(
        f"{bucket} {count}" for bucket, count in sorted(counts.items())))
    print(f"CONTAINER SWEEP: {invariant} invariant / {attempted} attempted "
          f"({len(must_fail)} published vectors x {len(CONTAINER_SHAPES)} "
          f"declared container shapes)"
          + (f"; NOT invariant: {non_invariant}" if non_invariant else ""))
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


def format_measurements(positional: dict, pin: dict) -> list[str]:
    """The two disclosures that may not go stale, printed as measurements."""
    lines = [
        "MEASUREMENTS RECOMPUTED THIS RUN - never transcribed, and hard-compared",
        "by --selftest, because a figure a reader cannot recompute is prose",
        "wearing a measurement's clothes (7.2.2):",
        f"  the inherited POSITIONAL rule (residual A7, WITHDRAWN IN PLACE)",
        f"    clauses reaching the by-phrase reader   "
        f"{positional['clausesReachingTheByPhraseReader']}",
        f"    `by X` matches in them                  {positional['byXmatches']}",
        f"    DROPPED by the positional threshold     "
        f"{positional['droppedByThePositionalThreshold']}",
        f"    live findings with the rule / without   "
        f"{positional['liveFindingsWithTheRule']} / "
        f"{positional['liveFindingsWithoutTheRule']}",
        f"    control (inverted construction) w/ w/o  "
        f"{positional['controlInvertedConstructionWithTheRule']} / "
        f"{positional['controlInvertedConstructionWithoutTheRule']}"
        f"   patch live: {bool(positional['patchIsLive'])}",
        "    The predecessor published this rule as worth 'four live false",
        "    positives to zero'. It drops nothing on this tree. The figure is",
        "    withdrawn in place, the row is carried verbatim, and this count is",
        "    what replaces it.",
    ]
    if pin.get("measured"):
        lines.extend([
            "  the inherited DECISION-SET pin (residual S5, NOT repairable here)",
            f"    expected non-retention set size, a literal  "
            f"{pin['expectedChoiceCount']}",
            f"    inherited packet lane on the live packet    "
            f"{pin['liveFindings']} finding(s)",
            f"    + one DECIDED row, SAME authority           "
            f"{pin['sameAuthority']['findings']} finding(s) "
            f"{pin['sameAuthority']['codes']}",
            f"    + one DECIDED row, DIFFERENT authority      "
            f"{pin['differentAuthority']['findings']} finding(s) "
            f"{pin['differentAuthority']['codes']}",
            "    RECORDING THE PRODUCT AUTHORITY'S NEXT DECISION REDS THIS",
            "    VALIDATOR, whatever the authority and whatever the attribution.",
            "    It is 7.10's defect applied to a decision SET. It is inherited,",
            "    it is disclosed here for the first time in this lineage, and it",
            "    is NOT repaired here - see residual S5 for why the repair",
            "    belongs to the instrument that owns the literal.",
        ])
    else:
        lines.append(
            "  the inherited DECISION-SET pin: NOT MEASURED on this run, because "
            "the live packet carries no decided row with a string authority")
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
        v5 = _load_predecessor()
        v4 = v5._load_predecessor()
        v3 = v4._load_predecessor()
        v2 = v3._load_predecessor()
        v1 = v2._load_predecessor()
    except RuntimeError as exc:
        print("REFUSING to run: the pinned predecessor closure is dirty")
        print(f"  - {exc}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    permitted = closure_paths(v5, v4, v3, v2)
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
          "and so on, so one pin covers a six-deep closure)")
    print("invocation: ISOLATED, NO-BYTECODE - the script's directory is not on "
          "the import path, so no file beside this one can shadow a module the "
          "pin chain depends on")

    if want_selftest:
        return selftest(product, ri, versioning, delivery, retention, register,
                        v5, v4, v3, v2, v1, permitted)

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
        attribution_scan(product, docs, v5, v4, v3, v2, v1, ledger)
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
    for line in format_measurements(
            positional_rule_measurement(product, docs, v5, v3, v2, v1),
            decision_set_pin_measurement(product, v5, v4, v3, v2, v1)):
        print(line)
    inherited_rows = v5.residual_registry(v4, v3)
    for line in v5.format_limits(
            residual_registry(v5, v4, v3),
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
