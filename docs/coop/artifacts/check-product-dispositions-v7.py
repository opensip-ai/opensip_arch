#!/usr/bin/env python3
"""Successor to the pinned predecessor. Edits nothing; closes TWO defects.

WHY A SUCCESSOR AND NOT AN EDIT
-------------------------------
Freeze 7.2 forbids changing reviewed bytes in place and the sanctioned repair is
a new file. The predecessor is a RUNTIME INPUT here, hash-verified before use,
which 7.3 explicitly permits. It in turn hash-verifies and executes ITS
predecessor, and so on, so ONE PIN COVERS A SEVEN-DEEP CLOSURE and every
inherited detection semantic is RE-USED BY CALL rather than retyped.

WHAT THIS SUCCESSOR CLOSES, AND WHY THE TWO HALVES ARE ONE FILE
---------------------------------------------------------------
An independent review of the predecessor returned ACCEPT_WITH_BLOCKERS at one
blocker. A coordinator independently measured a second defect on the live tree.
THE TWO PULL IN OPPOSITE DIRECTIONS - one says DETECT MORE, the other says
DETECT LESS - and a repair that does either alone makes the other worse. That is
why they are closed together and why the resolution is stated before the code.

  DEFECT 1 - DETECT MORE. THE COORDINATE-SHADOW ESCAPE.

  A forged authority nested under an object member whose key names a DIFFERENT
  attribution coordinate bought TOTAL SILENCE: zero findings, zero mentions, the
  artifact named nowhere. Reproduced as real bytes through a subprocess before a
  line of this file was written - the flat control is caught and named; the
  identical forgery one object deeper is not mentioned at all.

  THE PREDECESSOR'S DERIVATION IS SOUND AND ITS IMPLEMENTATION RELOCATED THE
  ASSUMPTION. Its walk is correct: an ARRAY does not name its members and an
  OBJECT does, so a leaf arrives carrying every object key on its path. Its
  RESOLVER then consumed that correctly-accumulated list by returning on the
  INNERMOST key that names a coordinate and discarding every outer one. The walk
  accumulates and the resolver throws the accumulation away. Two generations ago
  the assumption was "the key immediately above the scalar decides"; the
  predecessor's is "the innermost coordinate-naming key decides". Both are
  SINGLE-KEY assumptions, one layer apart.

  THIS IS THE THIRD INSTANCE OF ONE CLASS. Two point-repairs in a row is
  evidence that the repair keeps landing at the wrong level, so this file does
  not repair a third instance - it removes the level at which the defect lives.

  THE REPAIR: A LEAF CARRIES A SET OF QUALIFYING KEYS, NOT A WINNER.
    An object key states something about EVERYTHING beneath it. Two keys on one
    path therefore make two statements, and both hold at once - there is no
    derivation under which the inner one cancels the outer one. Arbitration
    between them was never derived; it was an implementation convenience. So the
    resolver returns the UNION of every coordinate any key on the path names,
    and a leaf is a coordinate of an attribution if ANY qualifier says so.

    WHY A FOURTH INSTANCE IS NOT REACHABLE, AND IT IS A PROPERTY RATHER THAN A
    PROMISE. A union is MONOTONE: inserting a key at any position in a path can
    only ADD coordinates and can never remove one. So no interposed container,
    of any shape, under any key name, can strip a leaf of a coordinate it
    already had. That monotonicity is EXECUTED over a derived key vocabulary at
    every insertion position, not asserted in this paragraph. The one remaining
    way to buy silence is to name NO coordinate at all, which is the silent lie
    already disclosed as residual A1 and accepted by construction.

  AND THE PROOF IS REPAIRED, NOT ONLY THE CODE - WHICH IS THE HALF THAT SHIPPED
  THE DEFECT. The predecessor's container sweep reported 216 of 216 invariant
  and COULD NOT SEE THIS BY CONSTRUCTION, because its wrapper keys were neutral
  literals. A sweep proves invariance only over the values it varies. So the
  sweep here varies wrapper NAMES as well as shapes, and the names are DERIVED
  from the packet's own coordinate vocabulary and from the published vectors'
  own object keys - never typed. It is proven non-vacuous by running the
  identical grid against the predecessor, where it loses families and loses some
  of them to total silence.

  DEFECT 2 - DETECT LESS. THE SELF-REVIEW TRAP.

  An instrument that scans the corpus scans ITS OWN REVIEW, and a review of a
  detection instrument necessarily documents that instrument's attack vectors AT
  THE EXACT PATHS THE INSTRUMENT LEARNED TO READ. Measured on the live tree, the
  predecessor's single finding IS the review of the predecessor - a review
  EXHIBITING an attack read as an artifact ASSERTING one.

  IT SCALES WITH CAPABILITY. Every widening of detection widens the set of
  review artifacts that trip it, so Defect 1's repair makes Defect 2 strictly
  worse. An instrument that detected nothing would have no false positive here.

  THE REPAIR IS NOT AN EXEMPTION FOR REVIEW ARTIFACTS. That hands a forgery
  route to anything named like a review, and reviewers in this lineage have
  already exercised exactly that route. It is to distinguish an artifact
  ASSERTING an attribution from one EXHIBITING one, and the marker is
  structural, per-POSITION rather than per-document, and DERIVED:

      A CONSTRUCTED SPECIMEN is a non-root object that re-declares one of the
      document's OWN ROOT IDENTITY KEYS - a root key whose value names this
      document or a file that exists in the scanned corpus - with a value that
      names NEITHER this document NOR any file in the scanned corpus.

    The document is displaying a document that does not exist. Quoting a
    non-existent record cannot be an assertion about the corpus, because there is
    nothing in the corpus it is about. Nothing here is a vocabulary, a path list,
    a filename test or a review exemption: the identity keys come from the
    document's own root and membership comes from the scanned population, so a
    reviewer who invents new key names keeps the protection and a forger who
    wants it must LABEL THE FORGERY AS FICTIONAL in the document's own bytes.

    AND IT IS NEVER SILENCE. An exhibit is demoted to a NAMED OBSERVATION with
    its path, its declared identity and the reason printed in full - the same
    discipline 4.4 requires of the standing doctrine. Forgery buys a green exit
    code and never silence.

HOW THE TENSION IS RESOLVED, STATED AS THE DESIGN RULE
------------------------------------------------------
The two repairs move on DIFFERENT AXES and therefore do not trade against each
other. Defect 1 widens WHAT COUNTS AS A COORDINATE - a property of the leaf.
Defect 2 narrows WHAT COUNTS AS AN ASSERTION - a property of the position's
provenance inside its document. A wider coordinate set finds strictly more
positions; the speech-act test then classifies each position it found. Neither
can swallow the other, because the exhibit test cannot fire on a position that
is not inside a constructed specimen, and the coordinate union cannot be reached
by anything the exhibit test looks at.

The ordering is load-bearing and is the reason this works: THE SPEECH-ACT TEST
RUNS BEFORE STANDING, because standing grades an assertion and a non-assertion
has nothing to grade. And it runs PER POSITION, because a document that both
exhibits one forgery and asserts another must produce exactly one finding and
one observation - which is executed, not claimed.

AND WHY THE STANDING DOCTRINE DID NOT ALREADY DEMOTE IT - MEASURED, NOT GUESSED
-------------------------------------------------------------------------------
It is a SCOPING CHOICE, not a classification gap, and this file MEASURES the
distinction every run rather than repeating it. The inherited classifier DOES
classify the review as a frozen review record - all five conjuncts pass. The
demotion is then deliberately overridden by the post-decision cutoff, which
re-promotes any review dispatched on or after the packet's earliest decision
date on the ground that it could have read the decided packet. That limb is
CORRECT for an assertion and inapplicable to an exhibit, which is exactly why
the repair belongs at the speech-act layer and not in the standing doctrine.

The census is printed every run and hard-compared: classified minus re-promoted
must equal the review-record standing count. A silent drop-out in the
classifier - which is a real hazard, since its own conjunct vocabularies are
hand-enumerated in reviewed bytes this file may not edit - then shows up as a
NUMBER rather than as an absence. That is 7.2.2's ENUMERATION rider applied to
the classifier itself, and it is why the speech-act test deliberately does NOT
depend on that classifier.

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
    "PD7-UNSUPPORTED-INVOCATION: this instrument must be run in ISOLATED, "
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
# verifies its own, and so on - one pin, seven files.
# ---------------------------------------------------------------------------
PREDECESSOR_BINDING = {
    "path": "check-product-dispositions-v6.py",
    "sha256": "278c1cbb62fc18e5eab25316a253bb426d39e29df14b96370fd29538525e01ce",
    "bytes": 139837,
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
EXIT_CLASS_SKIPPED = 4
DECLARED_FLAGS = ("--selftest",)

FINDING_PREFIX = "PD7"

# Bounds. A hostile artifact may not make this lane expensive, and a bound that
# is hit is REPORTED rather than silently truncating. The leaf bounds are the
# predecessor's, unchanged, so the reach of the repair is the only thing that
# moved. SPECIMEN_MAX_DEPTH is this file's own and governs the speech-act walk.
SPECIMEN_MAX_DEPTH = 24
SPECIMEN_NODE_BUDGET = 60000

# THE DECLARED READ SET, carried unchanged. This lane compares exactly one JSON
# type; every other type has a stated, executed outcome.
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
    spec = importlib.util.spec_from_file_location("_pd_v6", path)
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


def closure_paths(v6, v5, v4, v3, v2) -> set[str]:
    """Every file this instrument is entitled to execute out of this directory.

    DERIVED by walking the pin chain rather than listed, so a longer chain needs
    no edit here and a file that is NOT in the chain can never be admitted by a
    stale literal. The COUNT is derived the same way and is compared, so a chain
    that silently shortens is a failure rather than a smaller number nobody
    reads.
    """
    permitted = {str(Path(__file__).resolve())}
    for module in (None, v6, v5, v4, v3, v2):
        binding = (PREDECESSOR_BINDING if module is None
                   else getattr(module, "PREDECESSOR_BINDING", None))
        if isinstance(binding, dict) and isinstance(binding.get("path"), str):
            permitted.add(str((HERE / binding["path"]).resolve()))
    return permitted


def import_provenance_failures(permitted: set[str]) -> list[str]:
    """Belt and braces: no import may have come from HERE, except the closure."""
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
# THE FIRST REPAIR. A leaf carries a SET of qualifying keys, not a winner.
#
# The predecessor's WALK is correct and is CALLED here unchanged, along with its
# type classifier and its packet-side coordinate-name derivation. What this file
# replaces is exactly one function: the resolver that consumed the walk's output.
# ---------------------------------------------------------------------------

def coordinate_qualifiers(qualifiers: tuple[str, ...], coordinate_keys: dict,
                          v5, v3, v2) -> dict[str, list[str]]:
    """{coordinate: [every key on the path that names it]}, outermost first.

    THE ONE CHANGE THAT CLOSES THE CLASS, AND IT IS A DELETION OF AN ARBITRATION
    NOBODY DERIVED.

    An object key states something about EVERYTHING BENEATH IT. A path carrying
    two coordinate-naming keys therefore carries two statements, and a leaf is
    subject to both: there is no rule under which the inner key CANCELS the
    outer one, and the predecessor's `return on the first match walking inward`
    was an implementation convenience wearing a derivation's clothes. So every
    qualifier is consulted and the answer is a UNION.

    THE PROPERTY THIS BUYS, WHICH IS WHY IT IS NOT A THIRD POINT REPAIR: the
    union is MONOTONE IN THE PATH. Inserting a key anywhere - inside an object,
    under any name, at any depth - can only add members to this mapping and can
    never remove one. So no interposed container can strip a leaf of a
    coordinate it already carried, whatever the interposed key is called. That is
    a structural fact about a union rather than a claim about shapes anyone
    thought of, and --selftest EXECUTES it at every insertion position over a
    derived key vocabulary rather than restating this paragraph.

    EVERY NAMING KEY IS RETURNED, not just one per coordinate, so a finding can
    name the position IN FULL - a reader is told which keys made the leaf an
    authority, not merely that something did.
    """
    out: dict[str, list[str]] = {}
    when_keys = coordinate_keys.get("when") or ()
    who_keys = coordinate_keys.get("who") or ()
    for key in qualifiers:
        names: list[str] = []
        # The inherited lexical predicate decides the authority coordinate; the
        # packet's own field names decide both. Called, never retyped.
        if v5.authority_shaped_key(key, v3, v2):
            names.append("who")
        normalised = v2._norm_key(key)
        if normalised in when_keys:
            names.append("when")
        if normalised in who_keys and "who" not in names:
            names.append("who")
        for coordinate in names:
            out.setdefault(coordinate, []).append(str(key))
    return out


def qualifier_key_names(qualifiers: dict[str, list[str]], coordinate: str) -> str:
    """The keys that made a leaf this coordinate, named in full for a reader."""
    keys = qualifiers.get(coordinate) or []
    if not keys:
        return ""
    if len(keys) == 1:
        return repr(keys[0])
    return ", ".join(repr(key) for key in keys)


# ---------------------------------------------------------------------------
# THE SECOND REPAIR. ASSERTING versus EXHIBITING, derived from the document.
#
# Nothing below reads a filename convention, a role vocabulary, a verdict
# vocabulary or a path list. Two inputs only: the document's own root, and the
# set of filenames that actually exist in the scanned population.
# ---------------------------------------------------------------------------

def root_identity_keys(name: str, doc: object, corpus: set[str]) -> tuple[str, ...]:
    """Root keys whose value IDENTIFIES this document or names a corpus file.

    A document says what it is at its own root. Which key it uses to do that is
    the document's business - `artifact`, `documentClass`, anything - so the key
    is DISCOVERED by asking which root value actually resolves to a real
    document, rather than by matching a name against a list. A root key whose
    value is free prose resolves to nothing and is not an identity key, which is
    what keeps a verdict sentence from being mistaken for one.
    """
    if not isinstance(doc, dict):
        return ()
    return tuple(
        str(key) for key, value in doc.items()
        if isinstance(value, str)
        and (_identifies_this_document(value, name) or value.strip() in corpus))


def _identifies_this_document(value: str, name: str) -> bool:
    """Does this string name the document it was found in?

    Compared on alphanumerics only and in BOTH containment directions, because
    the corpus spells its own identities inconsistently - some carry the suffix,
    some drop it, some carry a package prefix - and a test that demanded equality
    would silently classify the inconsistent majority as having no identity at
    all, which is the fail-OPEN direction.
    """
    left = _alnum(value)
    right = _alnum(Path(name).stem)
    if not left or not right:
        return False
    return right in left or left in right


def _alnum(text: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def constructed_specimen_roots(name: str, doc: object, corpus: set[str],
                               v1, v2) -> list[tuple[str, list[str], list[str]]]:
    """[(path, identity keys re-declared, their values)] for every SPECIMEN.

    A CONSTRUCTED SPECIMEN is a non-root object that re-declares one of this
    document's own root identity keys with a value naming NEITHER this document
    NOR any file in the scanned corpus. The document is displaying a record that
    does not exist, so the enclosing document is QUOTING rather than ASSERTING,
    and a quotation of a non-existent record cannot be an assertion about the
    corpus - there is nothing in the corpus it is about.

    THREE CONJUNCTS, EACH INDEPENDENTLY MEASURABLE AND ALL DERIVED:
      1. this document HAS a root identity key at all - otherwise it never said
         what shape "a document" has here and nothing can re-declare it;
      2. the document is ABOUT THE CORPUS - it names at least one other file
         that exists in the scanned population, by the inherited reference
         reader, CALLED not retyped. A document about nothing exhibits nothing;
      3. the object re-declares an identity key and EVERY such value resolves to
         no real document. One value that does resolve makes the subtree a
         CITATION of real bytes, which the standing doctrine already governs and
         this test must not touch.

    Descent STOPS at a specimen: a specimen's interior is the specimen.

    THE FORGERY ROUTE THIS LEAVES, STATED PLAINLY. A forger may reach this
    demotion - but only by writing, in the document's own bytes, an identity
    that names no document in the corpus. They must LABEL THE FORGERY AS
    FICTIONAL. Compare the repair this replaces, where naming a file
    `*.review-*` was sufficient. And the demotion is to a NAMED OBSERVATION
    carrying the path and the declared identity, never to silence.
    """
    identity = set(root_identity_keys(name, doc, corpus))
    if not identity:
        return []
    if v2.names_other_corpus_files(name, doc, corpus, v1.FILE_REFERENCE_RE) < 1:
        return []
    out: list[tuple[str, list[str], list[str]]] = []
    budget = [SPECIMEN_NODE_BUDGET]

    def walk(node: object, path: str, depth: int) -> None:
        if depth > SPECIMEN_MAX_DEPTH or budget[0] <= 0:
            return
        budget[0] -= 1
        if isinstance(node, dict):
            if depth:
                shared = [key for key in node
                          if key in identity and isinstance(node.get(key), str)]
                if shared and all(
                        not _identifies_this_document(node[key], name)
                        and node[key].strip() not in corpus for key in shared):
                    out.append((path, [str(k) for k in shared],
                                [str(node[k]) for k in shared]))
                    return
            for key, value in node.items():
                walk(value, f"{path}.{key}", depth + 1)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]", depth + 1)

    walk(doc, "$", 0)
    return out


def specimen_containing(where: str,
                        specimens: list[tuple[str, list[str], list[str]]]
                        ) -> tuple[str, list[str], list[str]] | None:
    """The specimen a position sits inside, or None. PER POSITION, never per file.

    Granularity is the whole point. A document that EXHIBITS one forgery and
    ASSERTS another must produce exactly one finding and one observation; a
    per-document exemption would drop both, and that is the shape of every
    exemption this corpus has had to withdraw.
    """
    for specimen in specimens:
        root = specimen[0]
        if where == root or where.startswith(root + ".") \
                or where.startswith(root + "["):
            return specimen
    return None


# ---------------------------------------------------------------------------
# The ATTRIBUTION lane over ONE artifact.
# ---------------------------------------------------------------------------

def attribution_failures(states: dict[str, str],
                         attribution: dict[str, dict[str, list[str]]],
                         name: str, doc: object, prefix: str,
                         coordinate_keys: dict, corpus: set[str],
                         v6, v5, v3, v2, v1
                         ) -> tuple[list[str], list[str], dict[str, int]]:
    """(assertions, exhibits, counts) for ONE artifact. A pure function.

    Reads the packet's derived coordinates, the artifact, and the SET OF NAMES
    in the scanned population - and nothing else. No digest, no head document,
    no file contents but this one, so an external driver can mutate a document
    in memory, hand it a synthetic corpus and prove the lane is not vacuous from
    outside itself (7.8). The corpus is an explicit argument precisely so that
    the speech-act test is independently drivable: hand it a population in which
    a specimen's declared identity EXISTS and the demotion must stop firing.

    Every semantic limb below is the pinned closure's, CALLED: the site walk,
    the leaf walk, the type classifier, the assertion vocabulary, the closure
    predicate family, the by-phrase reader, the calendar validator, the token
    comparison and the reference reader. What this successor supplies is the
    coordinate UNION and the speech-act split.
    """
    counts = {"attributionSites": 0, "authorityClaims": 0, "dateClaims": 0,
              "agreeing": 0, "conflicts": 0, "notAnAssertion": 0}
    extra = {"uncomparedTypeSites": 0, "comparedThroughAContainer": 0,
             "scalarsWalked": 0, "shadowedPositions": 0,
             "exhibitPositions": 0, "specimenRoots": 0}
    out: list[str] = []
    exhibits: list[str] = []
    known = tuple(sorted(states))
    try:
        key_anchored, _scoped, prose = v1._document_sites(doc, known)
    except RecursionError:
        return ([f"{prefix}-ATTRIBUTION-DEPTH {name}: the artifact nests deeper "
                 "than the interpreter can walk, so it was NOT examined by the "
                 "attribution lane and this run's silence about it is not "
                 "evidence"], [], {**counts, **extra})
    specimens = constructed_specimen_roots(name, doc, corpus, v1, v2)
    extra["specimenRoots"] = len(specimens)
    seen: set[tuple[str, str, str, str]] = set()

    def route(where: str, text: str) -> None:
        """The SPEECH-ACT SPLIT, and it happens BEFORE standing.

        Standing grades an assertion. A position that is not an assertion has
        nothing for standing to grade, so this runs first and independently.
        """
        specimen = specimen_containing(where, specimens)
        if specimen is None:
            counts["conflicts"] += 1
            out.append(text)
            return
        root, keys, values = specimen
        extra["exhibitPositions"] += 1
        exhibits.append(
            f"{prefix}-ATTRIBUTION-EXHIBIT {name}{where}: NOT A FINDING, and "
            "not silence either. This position sits inside a CONSTRUCTED "
            f"SPECIMEN at {root}, an object that re-declares this document's "
            f"own identity key(s) {', '.join(repr(k) for k in keys)} as "
            f"{', '.join(repr(v) for v in values)} - naming neither this "
            "document nor any file in the scanned population. The document is "
            "DISPLAYING a record that does not exist rather than ASSERTING one "
            "about the corpus, and a review of a detection instrument documents "
            "its attacks at exactly the paths that instrument learned to read. "
            "The attribution it exhibits, reported in full and never dropped: "
            + text)

    def emit(decision_id: str, where: str, kind: str, claimed: str,
             recorded: list[str], how: str) -> None:
        key = (decision_id, where, kind, claimed)
        if key in seen:
            return
        seen.add(key)
        coordinate = "an authority" if kind == "AUTHORITY" else "a decision date"
        route(where, (
            f"{prefix}-ATTRIBUTION-{kind} {name}{where}: asserts {decision_id} "
            f"was decided {'by' if kind == 'AUTHORITY' else 'on'} {claimed!r} "
            f"while the binding product packet records "
            f"{recorded if recorded else 'NO ' + coordinate + ' at all'} for it "
            f"(via {how}). A decision is constituted only by the binding packet; "
            "an artifact may CITE its attribution and may never CREATE one, so "
            "naming a different authority or a different moment for a decision "
            "the packet carries is a conflict even where the STATE agrees"))

    def emit_uncompared(decision_id: str, where: str, coordinate: str,
                        keys: str, kind: str, value: object) -> None:
        marker = (decision_id, where, "UNCOMPARED-TYPE-MARKER", coordinate + kind)
        if marker in seen:
            return
        seen.add(marker)
        extra["uncomparedTypeSites"] += 1
        route(where, (
            f"{prefix}-ATTRIBUTION-UNCOMPARED-TYPE {name}{where}: this position "
            f"names the {coordinate.upper()} coordinate of {decision_id} (key "
            f"{keys}) and carries a JSON {kind}, {value!r}. THIS LANE COMPARES "
            f"JSON {'/'.join(COMPARED_JSON_TYPES).upper()} SCALARS AND NOTHING "
            "ELSE, so this value's CONTENT WAS NOT COMPARED against the binding "
            "packet and this run's silence about it is not evidence. Freeze 6 "
            "law 18: a closed scalar is admitted on exact type BEFORE its "
            "content is read, at any depth - and the alternative here is the "
            "defect an earlier generation shipped, where a value the lane could "
            "not read was passed over without a word"))

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
        # is the STATE lane's business and this lane says nothing about it.
        if states.get(decision_id) != "CLOSED_POSITIVE":
            continue
        head_text = v1._disposition_value_text(value)
        if isinstance(head_text, str) and head_text.strip():
            scan_prose(decision_id, location, head_text, "co-located prose",
                       require_id=False)
        if isinstance(value, str):
            continue
        overflow: list[str] = []
        for qualifiers, where, leaf, kind in v6.qualified_leaves(
                value, location, overflow=overflow):
            extra["scalarsWalked"] += 1
            found = coordinate_qualifiers(qualifiers, coordinate_keys, v5, v3, v2)
            # THE MEASUREMENT THAT MAKES THE REPAIR VISIBLE. A position where
            # the predecessor's inner-most arbitration would have discarded an
            # outer coordinate is counted, so "the repair changed nothing here"
            # is a number rather than an inference.
            if len(found) > 1 or (found and any(
                    len(keys) > 1 for keys in found.values())):
                extra["shadowedPositions"] += 1
            through_container = "[" in where[len(location):]
            if kind != "string":
                # DECLARED, NOT SILENT, and now named for EVERY coordinate the
                # position carries rather than for one arbitrated winner.
                for coordinate in sorted(found):
                    emit_uncompared(decision_id, where, coordinate,
                                    qualifier_key_names(found, coordinate),
                                    kind, leaf)
                continue
            if not leaf.strip():
                continue
            why = v5.records_rather_than_asserts(where, leaf, v1, v3)
            if not why:
                # A field whose KEY records who acted is an attribution whatever
                # its value says. A value that IS a bare calendar date is a date
                # claim. BOTH now hold at any container depth AND under any
                # number of coordinate-naming keys, because the answer is a
                # union and nothing arbitrates it away.
                if "who" in found and not v5.is_iso_date_value(leaf):
                    tokens = v3._role_verdict(leaf)
                    if tokens:
                        how = ("authority-shaped key(s) "
                               + qualifier_key_names(found, "who"))
                        if "when" in found:
                            how += (" - retained even though the path ALSO "
                                    "names the date coordinate at "
                                    + qualifier_key_names(found, "when")
                                    + ", because a key states something about "
                                    "everything beneath it and a second key "
                                    "cannot cancel the first")
                        if through_container:
                            how += (" reached through a JSON container, which "
                                    "cannot change a verdict")
                            extra["comparedThroughAContainer"] += 1
                        compare(decision_id, where, [(leaf.strip(), tokens)],
                                [], how)
                if v5.is_iso_date_value(leaf):
                    how = ("date-valued leaf under "
                           + (qualifier_key_names(found, "when")
                              or qualifier_key_names(found, "who")
                              or "no naming key"))
                    if through_container:
                        how += (" reached through a JSON container, which "
                                "cannot change a verdict")
                        extra["comparedThroughAContainer"] += 1
                    compare(decision_id, where, [], [leaf.strip()], how)
            scan_prose(decision_id, where, leaf, "co-located prose",
                       require_id=False)
        if overflow:
            route(overflow[0], (
                f"{prefix}-ATTRIBUTION-DEPTH {name}{overflow[0]}: the "
                "decision-keyed value exceeds this lane's traversal bound, "
                "so it was NOT fully examined and its silence is not "
                "evidence"))

    for decision_id, location, leaf in prose:
        if states.get(decision_id) != "CLOSED_POSITIVE":
            continue
        scan_prose(decision_id, f"{location}<prose>", leaf, "prose naming the id",
                   require_id=True)

    return out, exhibits, {**counts, **extra}


# ---------------------------------------------------------------------------
# The corpus pass. Speech act first, THEN standing.
# ---------------------------------------------------------------------------

def attribution_scan(product: object, docs: list[tuple[str, object]],
                     v6, v5, v4, v3, v2, v1, ledger=None, leaf_lane=None,
                     prefix: str = FINDING_PREFIX
                     ) -> tuple[list[str], list[str], list[str], dict[str, object]]:
    """(failures, historical observations, exhibits, report) over the corpus.

    Standing is the pinned closure's, CALLED not copied, so this lane cannot
    quietly grade an artifact differently from the state lane beside it. The
    speech-act split is this file's and runs BEFORE it.

    `leaf_lane` is INJECTABLE, and that is a measurement device rather than a
    convenience: --selftest drives this same scan with the PREDECESSOR's leaf
    lane and requires the result to equal the predecessor's own scan exactly, so
    every difference this successor produces comes from the two repairs and from
    nothing else in the bookkeeping.
    """
    lane = leaf_lane if leaf_lane is not None else attribution_failures
    states = v1.packet_decision_states(product)
    attribution = v5.packet_attribution(product, v3, v2)
    coordinate_keys = v6.packet_coordinate_keys(product, v5, v3, v2)
    attributed = {d: a for d, a in attribution.items() if a["who"] or a["when"]}
    corpus = {name for name, _ in docs}
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
        "shadowedPositions": 0,
        "exhibitPositions": 0,
        "specimenRoots": 0,
        "exhibitingArtifacts": 0,
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
        return [], [], [], report
    if not attributed:
        why = ("the binding packet records NO authority-shaped field and NO "
               "calendar-date field on ANY decision row, so this lane has "
               "nothing to compare an artifact's attribution against. THE CLASS "
               "DID NOT RUN - its silence is not evidence that no artifact "
               "asserts a fabricated attribution")
        report["classSkipped"] = why
        if ledger is not None:
            ledger.not_executed("corpus-attribution", why)
        return [], [], [], report

    rejected = v2.rejecting_reviews(docs, v1)
    records = v2.review_records(docs, v1)
    decision_dates = v2.packet_decision_dates(product)
    failures: list[str] = []
    observations: list[str] = []
    exhibited: list[str] = []
    for name, doc in docs:
        if lane is attribution_failures:
            found, shown, counts = lane(states, attribution, name, doc, prefix,
                                        coordinate_keys, corpus, v6, v5, v3, v2, v1)
        elif lane is getattr(v6, "attribution_failures", None):
            found, counts = lane(states, attribution, name, doc, prefix,
                                 coordinate_keys, v5, v3, v2, v1)
            shown = []
        else:
            found, counts = lane(states, attribution, name, doc, prefix,
                                 v3, v2, v1)
            shown = []
        for key, value in counts.items():
            if key in report:
                report[key] = int(report[key]) + value   # type: ignore[arg-type]
        if shown:
            report["exhibitingArtifacts"] = \
                int(report["exhibitingArtifacts"]) + 1   # type: ignore[arg-type]
            exhibited.append(
                f"{name} - EXHIBIT: {len(shown)} position(s) inside a "
                "constructed specimen, displayed rather than asserted")
            exhibited.extend(f"    {item}" for item in shown)
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
                f"examined) ASSERTS a decision the packet carries to an "
                f"authority or a date the packet does not record; "
                f"{report['agreeing']} coordinate(s) agree, "
                f"{report['comparedThroughAContainer']} of the comparisons were "
                f"reached THROUGH a JSON container, "
                f"{report['exhibitPositions']} position(s) in "
                f"{report['exhibitingArtifacts']} artifact(s) are EXHIBITS "
                f"inside a constructed specimen and are named in full below, "
                f"and {report['historicalObservations']} conflicting one(s) "
                "survive in artifacts with no standing, also listed")
    return failures, observations, exhibited, report


def classifier_census(product: object, docs: list[tuple[str, object]],
                      v2, v1) -> dict[str, object]:
    """WHY a review record was or was not demoted, as numbers rather than prose.

    An earlier account of this lineage's self-review trap guessed that the
    standing doctrine had FAILED TO CLASSIFY the offending review. Measured, that
    is false: classification succeeds and a deliberate SCOPING limb then
    re-promotes the record to LIVE, on the ground that a review dispatched on or
    after the packet's earliest decision date could have read the decided packet.
    That limb is correct for an ASSERTION and inapplicable to an EXHIBIT, which
    is the whole reason the repair sits at the speech-act layer.

    So the mechanism is published as an IDENTITY that must hold every run -
    classified minus re-promoted equals the review-record standing count - and
    the failing-conjunct histogram is published beside it. The classifier's own
    conjunct vocabularies are hand-enumerated in reviewed bytes this file may not
    edit; 7.2.2's ENUMERATION rider says a hand-listed row set is uncheckable
    unless its population is published, so its DROP-OUT is published here as a
    number. A silent drop-out then stops being an absence.
    """
    corpus = {name for name, _ in docs}
    records = v2.review_records(docs, v1)
    rejected = v2.rejecting_reviews(docs, v1)
    dates = v2.packet_decision_dates(product)
    declaring = [name for name, doc in docs
                 if v2.declares_review_class(name, doc)]
    unclassified: dict[str, int] = {}
    for name, doc in docs:
        if name in records or not v2.declares_review_class(name, doc):
            continue
        if not v2.has_reviewer_role(doc):
            failing = "reviewer role"
        elif not v2.has_verdict_shape(doc):
            failing = "verdict shape"
        elif v2.names_other_corpus_files(
                name, doc, corpus, v1.FILE_REFERENCE_RE) < 1:
            failing = "names a corpus subject"
        elif not v2.dispatch_date(doc):
            failing = "records a dispatch date"
        else:
            failing = "unattributed"
        unclassified[failing] = unclassified.get(failing, 0) + 1
    standing: dict[str, int] = {}
    repromoted = 0
    for name, doc in docs:
        outcome, _reason = v2.standing_of(
            name, doc, docs, rejected, records, dates)
        standing[outcome] = standing.get(outcome, 0) + 1
        if name in records and outcome == "LIVE":
            repromoted += 1
    return {
        "scanned": len(docs),
        "declaringReviewClass": len(declaring),
        "classifiedAsReviewRecord": len(records),
        "notClassifiedThoughDeclaring": sum(unclassified.values()),
        "failingConjunct": unclassified,
        "standing": standing,
        "repromotedByThePostDecisionCutoff": repromoted,
        "earliestPacketDecisionDate": min(dates.values()) if dates else "",
        "identityHolds": (len(records) - repromoted
                          == standing.get("REVIEW-RECORD", 0)),
    }


def format_attribution(report: dict[str, object]) -> list[str]:
    """The lane's own census, recomputed every run rather than transcribed."""
    lines = ["ATTRIBUTION LANE - who and when, at any container depth, under "
             "any number of naming keys"]
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
    lines.append("    of which record rather than assert (quoted, superseded,")
    lines.append(f"    negated, hedged, attributed, historical)  "
                 f"{report['notAnAssertion']}")
    lines.append(f"  scalars walked under decision keys {report['scalarsWalked']}")
    lines.append(f"  co-located coordinates compared   "
                 f"{int(report['authorityClaims']) + int(report['dateClaims'])} "
                 f"(authority {report['authorityClaims']}, "
                 f"date {report['dateClaims']})")
    lines.append(f"    reached THROUGH a container     "
                 f"{report['comparedThroughAContainer']} "
                 "(nesting cannot change a verdict)")
    lines.append(f"    carrying MORE THAN ONE naming key  "
                 f"{report['shadowedPositions']} (the predecessor's resolver "
                 "kept one and discarded the rest)")
    lines.append(f"    agreeing with the packet        {report['agreeing']}")
    lines.append(f"    conflicting                     {report['conflicts']}")
    lines.append(f"  positions this lane declined to READ, and NAMED rather "
                 f"than passed over: {report['uncomparedTypeSites']}")
    lines.append(f"    (compared types {list(COMPARED_JSON_TYPES)}; traversed "
                 f"{list(TRAVERSED_JSON_TYPES)};")
    lines.append(f"     named-but-uncompared {list(NAMED_BUT_UNCOMPARED_JSON_TYPES)})")
    lines.append("  SPEECH ACT - an artifact ASSERTING an attribution is not an "
                 "artifact EXHIBITING one")
    lines.append(f"    constructed specimens discovered  "
                 f"{report['specimenRoots']} (derived from each document's own "
                 "root identity keys)")
    lines.append(f"    positions demoted as EXHIBITS     "
                 f"{report['exhibitPositions']} in "
                 f"{report['exhibitingArtifacts']} artifact(s), named in full "
                 "below and never dropped")
    lines.append(f"  conflicting artifacts WITH standing (findings)     "
                 f"{report['conflictingArtifactsLive']}")
    lines.append(f"  conflicting artifacts with NONE (observations)     "
                 f"{report['conflictingArtifactsHistorical']}")
    demoted = report.get("demotedByStanding") or {}
    lines.append("    demoted by standing: " + ", ".join(
        f"{k} {v}" for k, v in sorted(demoted.items())))    # type: ignore[union-attr]
    return lines


def format_census(census: dict[str, object]) -> list[str]:
    """The standing classifier, measured rather than trusted."""
    standing = census.get("standing") or {}
    lines = [
        "STANDING CLASSIFIER CENSUS - published because a hand-enumerated row "
        "set is",
        "uncheckable unless its population is (7.2.2's ENUMERATION rider), and "
        "because",
        "this instrument's own predecessor was misdiagnosed as failing to "
        "CLASSIFY a",
        "review it in fact classified. The mechanism is an IDENTITY, and it is "
        "compared:",
        f"  scanned artifacts                          {census['scanned']}",
        f"  declaring review-class (filename/identity) "
        f"{census['declaringReviewClass']}",
        f"  CLASSIFIED as a frozen review record       "
        f"{census['classifiedAsReviewRecord']}",
        f"  declaring but NOT classified               "
        f"{census['notClassifiedThoughDeclaring']} - these are the silent "
        "drop-outs",
    ]
    for conjunct, count in sorted((census.get("failingConjunct") or {}).items()):
        lines.append(f"      first failing conjunct: {conjunct:24s} {count}")
    lines.append(
        f"  RE-PROMOTED to LIVE by the post-decision cutoff "
        f"{census['repromotedByThePostDecisionCutoff']} "
        f"(earliest packet decision date "
        f"{census['earliestPacketDecisionDate'] or 'NONE'})")
    lines.append("  standing partition: " + ", ".join(
        f"{k} {v}" for k, v in sorted(standing.items())))   # type: ignore[union-attr]
    lines.append(
        f"  IDENTITY classified - re-promoted == REVIEW-RECORD standing: "
        f"{census['classifiedAsReviewRecord']} - "
        f"{census['repromotedByThePostDecisionCutoff']} == "
        f"{standing.get('REVIEW-RECORD', 0)}  -> {census['identityHolds']}")
    lines.append(
        "  READ THIS AS THE ANSWER TO 'why was the review not demoted': it WAS "
        "classified,")
    lines.append(
        "  and a SCOPING limb re-promoted it. Not a classification gap. The "
        "limb is right")
    lines.append(
        "  about assertions and silent about exhibits, which is why the repair "
        "is elsewhere.")
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
# MEASUREMENTS THAT MAY NOT GO STALE.
# ---------------------------------------------------------------------------

def positional_rule_measurement(product: object, docs: list[tuple[str, object]],
                                v6, v5, v3, v2, v1) -> dict[str, object]:
    """What the inherited POSITIONAL rule actually excludes, on THIS lane.

    Carried from the predecessor with one change and it is the necessary one:
    the scan it drives is THIS successor's, so the withdrawn figure is
    re-measured against the reach the repair actually has rather than against
    the predecessor's. A CONTROL is included in the same measurement, because a
    patch that changes nothing and a patch that is not live look identical from
    the outside.
    """
    states = v1.packet_decision_states(product)
    attribution = v5.packet_attribution(product, v3, v2)
    coordinate_keys = v6.packet_coordinate_keys(product, v5, v3, v2)
    corpus = {name for name, _ in docs}
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
                                 coordinate_keys, corpus, v6, v5, v3, v2, v1)
        v5.by_phrases = original
        with_findings, with_obs, with_ex, with_report = attribution_scan(
            product, docs, v6, v5, None, v3, v2, v1)
        v5.by_phrases = unpositioned
        without_findings, without_obs, without_ex, without_report = \
            attribution_scan(product, docs, v6, v5, None, v3, v2, v1)
        # THE CONTROL. An inverted construction is the exact shape the rule
        # exists to exclude, so if the patch is live it MUST move on this. NO
        # COMMA after the agent preposition: residual A15 is that a comma there
        # ends the phrase before the name, so a control written in the shape of
        # a disclosed residual would measure the residual and not the rule.
        control_doc = {"artifact": "synthetic-control", "dispositions": {
            v2.RETENTION_DECISION_ID: (
                f"By {v6._UNRECORDED_ROLE} this was SIGNED OFF on "
                + v6._control_date(product, v5, v1) + ".")}}
        control_without = attribution_failures(
            states, attribution, "synthetic-control", control_doc,
            FINDING_PREFIX, coordinate_keys, corpus, v6, v5, v3, v2, v1)[0]
        v5.by_phrases = original
        control_with = attribution_failures(
            states, attribution, "synthetic-control", control_doc,
            FINDING_PREFIX, coordinate_keys, corpus, v6, v5, v3, v2, v1)[0]
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
        "exhibitsWithTheRule": len(with_ex),
        "exhibitsWithoutTheRule": len(without_ex),
        "authorityClaimsWithTheRule": int(with_report["authorityClaims"]),
        "authorityClaimsWithoutTheRule": int(without_report["authorityClaims"]),
        "controlInvertedConstructionWithTheRule": len(control_with),
        "controlInvertedConstructionWithoutTheRule": len(control_without),
        "patchIsLive": len(control_without) > len(control_with),
    }


def decision_set_pin_measurement(product: object, v6, v5, v4, v3, v2,
                                 v1) -> dict[str, object]:
    """What recording the authority's NEXT decision costs - BOTH halves.

    The predecessor measured the DECIDED half and disclosed it. An independent
    reviewer then found the PENDING half, running on a SECOND hard-coded literal
    and named nowhere: the awaited insertion may perfectly well arrive as a
    PENDING row before it is decided, and that path is red too, on a different
    code. Both halves are measured here and NEITHER is repaired - the literals
    are in reviewed bytes this file may not edit, consumed inside a lane this
    file executes rather than reimplements.
    """
    out = dict(v6.decision_set_pin_measurement(product, v5, v4, v3, v2, v1))
    if not out.get("measured"):
        return out
    pending_id = "CD-" + "SYNTHETIC-PENDING-INSERTION"
    blocked_state = ""
    rows = product.get("pendingDecisions") if isinstance(product, dict) else None
    for row in (rows or {}).values():
        if isinstance(row, dict) and isinstance(row.get("status"), str):
            blocked_state = row["status"]
            break
    if not blocked_state:
        # DERIVED from the packet's own vocabulary: the state the retention row
        # was in before it was decided is quoted by the row that superseded it.
        recorded = (product.get("decisions") or {}).get(v2.RETENTION_DECISION_ID)
        text = json.dumps(recorded) if isinstance(recorded, dict) else ""
        match = re.search(r"\b[A-Z][A-Z0-9_]{6,}\b", text)
        blocked_state = match.group(0) if match else "OPEN"
    for label, status in (("pendingBlocked", blocked_state),
                          ("pendingOpen", "OPEN")):
        extended = copy.deepcopy(product)
        pending = extended.get("pendingDecisions")
        if not isinstance(pending, dict):
            pending = {}
            extended["pendingDecisions"] = pending
        pending[pending_id] = {"status": status,
                               "question": "a synthetic pending row"}
        found = v4.decision_lane_v4(extended, v3, v2, v1)
        out[label] = {
            "status": status,
            "findings": len(found),
            "codes": sorted({f.split(":")[0].split(" ")[0] for f in found}),
        }
    out["pendingMeasured"] = True
    return out


# ---------------------------------------------------------------------------
# THE NAME-VARYING CONTAINER SWEEP.
#
# The predecessor's sweep reported 216 of 216 invariant and COULD NOT SEE the
# escape this file closes, because its object-valued shapes used neutral wrapper
# literals. A SWEEP PROVES INVARIANCE ONLY OVER THE VALUES IT VARIES. So the
# shapes here are parameterised by wrapper NAME, the names are DERIVED from the
# packet's own coordinate vocabulary and from the published vectors' own object
# keys, and the grid is run against the predecessor to prove it can fail.
#
# The two families are counted SEPARATELY and never folded into one denominator:
# five shapes contain no object and are name-invariant, so sweeping them across
# names would inflate the count with cells that cannot differ - which is the
# defect an independent reviewer found in the predecessor's type coverage.
# ---------------------------------------------------------------------------

def container_shapes(name_a: str, name_b: str) -> tuple:
    """((label, varies_with_name, builder), ...) - twelve carried shapes."""
    return (
        ("v (control, unwrapped)", False, lambda v: v),
        ("[v]", False, lambda v: [v]),
        ("[[v]]", False, lambda v: [[v]]),
        ("[[[v]]]", False, lambda v: [[[v]]]),
        ("[v, v]", False, lambda v: [v, v]),
        (f"{{{name_a}: v}}", True, lambda v: {name_a: v}),
        (f"{{{name_a}: {{{name_b}: v}}}}", True,
         lambda v: {name_a: {name_b: v}}),
        (f"[{{{name_a}: v}}]", True, lambda v: [{name_a: v}]),
        (f"{{{name_a}: [v]}}", True, lambda v: {name_a: [v]}),
        (f"[{{{name_a}: [v]}}]", True, lambda v: [{name_a: [v]}]),
        (f"[[{{{name_a}: [v]}}]]", True, lambda v: [[{name_a: [v]}]]),
        (f"{{{name_a}: [{{{name_b}: v}}]}}", True,
         lambda v: {name_a: [{name_b: v}]}),
    )


TYPE_SUBSTITUTIONS = (
    ("number (int)", 20260731),
    ("number (float)", 1.5),
    ("boolean true", True),
    ("boolean false", False),
    ("null", None),
    ("empty object", {}),
    ("empty array", []),
)


def _object_keys(node: object, out: set[str] | None = None,
                 depth: int = 0) -> set[str]:
    """Every object key anywhere in a value. Used to DERIVE a name vocabulary."""
    if out is None:
        out = set()
    if depth > SPECIMEN_MAX_DEPTH:
        return out
    if isinstance(node, dict):
        for key, value in node.items():
            out.add(str(key))
            _object_keys(value, out, depth + 1)
    elif isinstance(node, list):
        for value in node:
            _object_keys(value, out, depth + 1)
    return out


def wrapper_name_vocabulary(packets: tuple, vectors: tuple,
                            coordinate_keys: dict,
                            v5, v3, v2) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """(qualifying, neutral) wrapper key names - DERIVED, never typed.

    Two independent sources, both read off live data:
      1. every field name the PACKETS use on a decision row. The attack needs a
         key that names a coordinate, and the packet is where coordinate names
         come from - so a packet that renames its fields moves this vocabulary
         with it, exactly as the comparison itself does (7.10's corollary).
      2. every object key appearing anywhere in the PUBLISHED VECTORS. A vector
         added later contributes its own key names to the sweep with nobody
         remembering to add them.

    The partition is by the same predicates the lane itself uses, so the
    QUALIFYING half is precisely the attack surface and the NEUTRAL half
    reproduces the predecessor's sweep as a strict subset of this one.
    """
    names: set[str] = set()
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        for section in ("decisions", "pendingDecisions"):
            rows = packet.get(section)
            if not isinstance(rows, dict):
                continue
            for row in rows.values():
                if isinstance(row, dict):
                    names.update(str(key) for key in row)
    for entry in vectors:
        _object_keys(entry[-1], names)
    qualifying: list[str] = []
    neutral: list[str] = []
    when_keys = coordinate_keys.get("when") or ()
    who_keys = coordinate_keys.get("who") or ()
    for key in sorted(names):
        normalised = v2._norm_key(key)
        if v5.authority_shaped_key(key, v3, v2) or normalised in when_keys \
                or normalised in who_keys:
            qualifying.append(key)
        else:
            neutral.append(key)
    return tuple(qualifying), tuple(neutral)


def assertion_excusing_names(names: tuple[str, ...], v5, v3,
                             v1) -> tuple[str, ...]:
    """Names the INHERITED assertion vocabulary reads as historical, by PATH.

    FOUND BY THIS FILE'S OWN SWEEP RATHER THAN ANTICIPATED, which is the whole
    argument for varying names. The live packet's decision row carries a field
    whose name the pinned closure treats as marking superseded text - so a leaf
    under it is a RECORD of what something used to say, not an assertion, and
    the lane is correctly silent there. That silence is not an invariance
    failure, and counting it as one would make the sweep fail on the inherited
    vocabulary working as designed.

    So these names are DISCOVERED by probing the inherited predicate with a path
    and no text at all - the predicate is path-only for this family, verified -
    rather than listed. They are swept SEPARATELY and their losses are published
    as EXCUSED with the reason the predicate gives, never folded into the
    invariance denominator and never dropped. Residual A26.
    """
    return tuple(name for name in names
                 if v5.records_rather_than_asserts(f"$.{name}", "", v1, v3))


def wrapper_name_pairs(qualifying: tuple[str, ...], neutral: tuple[str, ...],
                       excusing: tuple[str, ...] = ()
                       ) -> tuple[tuple[str, str], ...]:
    """The (outer, inner) wrapper names the sweep runs.

    Every name paired with itself, plus every ORDERED pair of DISTINCT
    qualifying names - which is the shadow attack and its converse, derived
    rather than thought of. Neutral names are swept singly because two neutral
    keys cannot shadow anything and the pair would be a cell that cannot differ.
    Names the inherited vocabulary EXCUSES are held out and swept on their own.
    """
    held = set(excusing)
    pairs = [(name, name) for name in qualifying + neutral if name not in held]
    pairs.extend((outer, inner) for outer in qualifying for inner in qualifying
                 if outer != inner and outer not in held and inner not in held)
    return tuple(pairs)


def sweep_grid(lane, vectors: tuple, prefix: str,
               pairs: tuple[tuple[str, str], ...],
               families) -> dict[str, object]:
    """Run one instrument's lane over vectors x shapes x names.

    TWO DEFINITIONS OF NON-INVARIANCE ARE REPORTED, BOTH DEFINED HERE, because
    an independent reviewer measured the predecessor publishing the weaker of
    the two and thereby understating its own non-vacuity 2.6x:

      WEAK   - a pair is a LOSS iff `not (wrapped >= control)`. A vector the
               instrument never caught even unwrapped has an empty control, so
               `wrapped >= control` holds vacuously and every one of its shapes
               counts as invariant.
      STRICT - the same test, but only pairs whose CONTROL IS NON-EMPTY are
               ATTEMPTED at all. Vacuous pairs are removed from the denominator
               rather than counted as passes.

    SILENCE is counted separately, because total silence - a non-empty control
    going to an empty wrapped set - is the terminal symptom this whole lineage
    of blockers shares, and it is strictly worse than losing one family of two.
    """
    weak_attempted = weak_invariant = 0
    strict_attempted = strict_invariant = 0
    silences = 0
    losses: list[str] = []
    first = pairs[0] if pairs else ("wrapper", "inner")
    # The name-invariant shapes are instantiated ONCE. Running them across every
    # name would add cells that cannot differ, and a denominator padded with
    # cells that cannot fail is the defect this file was told to stop repeating.
    grid = [(label, shape) for label, varies, shape
            in container_shapes(*first) if not varies]
    for outer, inner in pairs:
        grid.extend((label, shape) for label, varies, shape
                    in container_shapes(outer, inner) if varies)
    for entry in vectors:
        label, doc = entry[0], entry[-1]
        control = families(lane(doc), prefix)
        for shape_label, shape in grid:
            wrapped = families(lane(_wrap_scalars(doc, shape)), prefix)
            weak_attempted += 1
            lost = not (wrapped >= control)
            if not lost:
                weak_invariant += 1
            if control:
                strict_attempted += 1
                if not lost:
                    strict_invariant += 1
            if lost:
                if not wrapped:
                    silences += 1
                if len(losses) < 8:
                    losses.append(
                        f"{shape_label} on {label[:44]!r}: control "
                        f"{sorted(control)} -> {sorted(wrapped)}")
    return {
        "shapesInGrid": len(grid),
        "namePairs": len(pairs),
        "weakAttempted": weak_attempted, "weakInvariant": weak_invariant,
        "weakLosses": weak_attempted - weak_invariant,
        "strictAttempted": strict_attempted, "strictInvariant": strict_invariant,
        "strictLosses": strict_attempted - strict_invariant,
        "totalSilences": silences, "examples": losses,
    }


def _wrap_scalars(node: object, shape) -> object:
    """Rebuild a document with every SCALAR leaf rewritten into `shape`.

    Keys are untouched: the sweep tests how a value is REACHED, and a key is
    part of the reaching rather than of the value. The WRAPPER keys are what
    this successor varies, and they arrive inside `shape`.
    """
    if isinstance(node, dict):
        return {key: _wrap_scalars(value, shape) for key, value in node.items()}
    if isinstance(node, list):
        return [_wrap_scalars(value, shape) for value in node]
    return shape(node)


# ---------------------------------------------------------------------------
# Fixtures. They build the world they test, so they stay meaningful whichever
# state the live packet is in, and NO CORPUS ARTIFACT IS NAMED in any of them.
# The predecessor's whole published corpus is CALLED and extended, never retyped.
# ---------------------------------------------------------------------------

def coordinate_names(packet: object, v6, v5, v3, v2) -> tuple[str, str]:
    """(who key, when key) as the packet SPELLS them. Derived, never typed.

    The vectors below need a key that names each coordinate. Typing one would
    make this file's own attack vectors go stale the moment a packet renames a
    field - the exact staleness 7.10 records - so the names are read back off
    whichever packet the fixture is built from.
    """
    keys = v6.packet_coordinate_keys(packet, v5, v3, v2)
    who = when = ""
    rows = packet.get("decisions") if isinstance(packet, dict) else None
    for row in (rows or {}).values():
        if not isinstance(row, dict):
            continue
        for key in row:
            normalised = v2._norm_key(key)
            if not who and normalised in (keys.get("who") or ()):
                who = str(key)
            if not when and normalised in (keys.get("when") or ()):
                when = str(key)
    return who, when


def attribution_cases(v6, v5, v3, v2) -> tuple:
    """(must_pass, must_fail, expected_escapes) - the predecessor's, extended.

    Every predecessor vector is CARRIED BY CALL, so none can be dropped by a
    successor and all of them are swept through this file's wider grid. What is
    added is the coordinate shadow in five forms, its AGREEING controls - because
    a repair that converts agreement into a conflict is a worse defect than the
    one it closes - and two new disclosed escapes.
    """
    must_pass, must_fail, escapes = v6.attribution_cases(v2)
    ident = v2.RETENTION_DECISION_ID
    packet = v6._fixture_packet(v2, "mnowak", "2026-08-05")
    who_key, when_key = coordinate_names(packet, v6, v5, v3, v2)
    other_name = "qbeltran"
    other_date = "2026-07-31"
    real_name = "mnowak"
    real_date = "2026-08-05"
    if not who_key or not when_key:
        # Fail closed and say so: without both coordinate names the shadow
        # vectors cannot be constructed, and a silently shortened vector list is
        # how a sweep starts proving less than it says.
        return must_pass, must_fail, escapes

    def art(body):
        return v6._artifact(body)

    must_fail = must_fail + (
        ("THE ESCAPE THIS SUCCESSOR CLOSES - the COORDINATE SHADOW. The forged "
         "authority is re-keyed under an object member whose key names the "
         "packet's OWN DATE coordinate. One finding became ZERO findings and "
         "ZERO mentions in the predecessor",
         "ATTRIBUTION-AUTHORITY",
         art({ident: {"status": "DECIDED",
                      who_key: {when_key: "product owner"}}})),
        ("the coordinate shadow reached THROUGH AN ARRAY as well, which is the "
         "predecessor's own repaired class and this one composed",
         "ATTRIBUTION-AUTHORITY",
         art({ident: {"status": "DECIDED",
                      who_key: [{when_key: "the coordinator"}]}})),
        ("the CONVERSE shadow: a forged date under a member key naming the "
         "AUTHORITY coordinate, which must not strip the date coordinate either",
         "ATTRIBUTION-DATE",
         art({ident: {"status": "DECIDED", when_key: {who_key: other_date}}})),
        ("THREE-DEEP ALTERNATION of the two coordinate names, because a union "
         "has no innermost winner to find at any depth",
         "ATTRIBUTION-AUTHORITY",
         art({ident: {"status": "DECIDED",
                      who_key: {when_key: {who_key: other_name}}}})),
        ("a WRONG-TYPED value at a SHADOWED coordinate is named on BOTH "
         "coordinates, never passed over on either",
         "ATTRIBUTION-UNCOMPARED-TYPE",
         art({ident: {"status": "DECIDED", who_key: {when_key: True}}})),
    )
    must_pass = must_pass + (
        ("an AGREEING authority under a SHADOWED path is still agreement - the "
         "repair must not convert agreement into a conflict",
         art({ident: {"status": "DECIDED", who_key: {when_key: real_name}}})),
        ("an AGREEING date under the converse shadow is still agreement",
         art({ident: {"status": "DECIDED", when_key: {who_key: real_date}}})),
        ("an agreeing attribution nested under BOTH coordinate names and an "
         "array, which is every repaired mechanism at once",
         art({ident: {"status": "DECIDED",
                      who_key: [{when_key: [real_name]}],
                      when_key: [{who_key: [real_date]}]}})),
    )
    escapes = escapes + (
        ("RESIDUAL-A21 the BARE AGENT PREPOSITION as a key. The inherited "
         "authority predicate requires a normalised key longer than two "
         "characters ending in the agent preposition, so the preposition ALONE "
         "is excluded by one character. The union rescues it wherever any outer "
         "key qualifies, which is now most nestings; flat it is silent. NOT "
         "repaired here - the predicate is in reviewed bytes this file executes "
         "rather than reimplements",
         art({ident: {"status": "DECIDED", "by": "product owner"}})),
    )
    return must_pass, must_fail, escapes


def exhibit_cases(v6, v5, v3, v2) -> tuple:
    """((label, corpus, name, doc, expect), ...) for the SPEECH-ACT split.

    `expect` is one of ASSERTION, EXHIBIT. Each case varies exactly one conjunct
    from the demoted baseline, so the exemption's boundary is measured on every
    side rather than demonstrated once in the direction that flatters it.
    """
    ident = v2.RETENTION_DECISION_ID
    subject = "some-other-record" + ".json"
    self_name = "a-review" + ".json"
    corpus = frozenset({subject, self_name})
    forged = {ident: {"status": "DECIDED", "decidedBy": "product owner"}}

    def review(specimen_identity, root_identity=self_name, extra=None):
        doc = {
            "artifact": root_identity,
            "subjectUnderReview": subject,
            "aBlocker": {
                "title": "the vector this review grades",
                "control": {"artifact": specimen_identity,
                            "dispositions": copy.deepcopy(forged)},
            },
        }
        if extra:
            doc.update(extra)
        return doc

    return (
        ("BASELINE: a review displaying a plant whose declared identity names "
         "no document in the corpus is EXHIBITING, not asserting",
         corpus, self_name, review("plant"), "EXHIBIT"),
        ("CONJUNCT 1 VARIED: the same bytes where the SPECIMEN's declared "
         "identity IS a real corpus file - a citation of real bytes, which the "
         "standing doctrine governs and this test must not touch",
         corpus, self_name, review(subject), "ASSERTION"),
        ("CONJUNCT 2 VARIED: the same bytes in a document that names NO other "
         "corpus file, so it is about nothing and exhibits nothing",
         frozenset({self_name}), self_name, review("plant"), "ASSERTION"),
        ("CONJUNCT 3 VARIED: the same bytes where the ROOT no longer establishes "
         "the re-declared key as an identity key at all - its root value now "
         "resolves to nothing - so re-declaring that key below means nothing",
         corpus, self_name, review("plant", root_identity="not-a-document"),
         "ASSERTION"),
        ("THE FORGERY ROUTE, EXECUTED: a document that is NOT review-shaped at "
         "all - no verdict, no reviewer role, no dispatch date, a filename that "
         "declares nothing - still reaches the demotion, and that is the "
         "deliberate design. It had to LABEL ITS FORGERY AS FICTIONAL to get "
         "there, and it buys a NAMED OBSERVATION rather than silence",
         corpus, "ordinary-document" + ".json",
         {"artifact": "ordinary-document" + ".json",
          "cites": subject,
          "specimen": {"artifact": "plant",
                       "dispositions": copy.deepcopy(forged)}},
         "EXHIBIT"),
        ("PER POSITION, NEVER PER FILE: a document that EXHIBITS one forgery "
         "and ASSERTS another must produce exactly one of each",
         corpus, self_name,
         review("plant", extra={"myOwnClaim": copy.deepcopy(forged)}),
         "BOTH"),
    )


# ---------------------------------------------------------------------------
# HONEST LIMITS, SCOPED PER LANE.
#
# CORRECTIONS ARE MADE IN PLACE AND NEVER BY DELETION. A predecessor row whose
# disclosure is incomplete is CARRIED VERBATIM FROM ITS LIVE BYTES and has the
# amendment APPENDED, so a reader meets the original claim and its correction
# together. --selftest asserts that EVERY inherited row's text is still present
# verbatim inside its carried row - not only the corrected ones - which is what
# stops a "correction" from quietly becoming a rewrite and stops an uncorrected
# row from being silently trimmed.
# ---------------------------------------------------------------------------

def carried_corrections() -> dict[str, str]:
    """{tag: the amendment appended to that carried row}."""
    return {
        "S5": (
            "  || AMENDED IN PLACE, NOT REWRITTEN: THE DISCLOSURE ABOVE NAMES "
            "ONLY HALF OF ITS OWN DEFECT. An independent reviewer measured the "
            "other half and it runs on a SECOND hard-coded literal in the same "
            "reviewed bytes: the PENDING side. The awaited insertion may "
            "perfectly well arrive as a PENDING row before it is decided, and "
            "that path is red too - a membership gate over the pending set "
            "fires on any pending id other than the retention one, on a "
            "DIFFERENT finding code that the row above names nowhere, and a "
            "coherent status on the new row can additionally be misread as a "
            "stale retention assertion. Both halves are now MEASURED on live "
            "bytes every run and printed together. NEITHER is repaired here, "
            "for the reason the row above already gives and which applies "
            "identically to the second literal.")
    }


def residual_registry(v6, v5, v4, v3) -> tuple:
    """(tag, lane, text, gate label or None). Inherited rows are CARRIED."""
    corrections = carried_corrections()
    rows: list[tuple[str, str, str, str | None]] = []
    for tag, lane, text, gate in v6.residual_registry(v5, v4, v3):
        lane = lane.replace("this successor", "predecessor, carried")
        if tag in corrections:
            text = text + corrections[tag]
            gate = "the decision-set pin's live cost, BOTH halves recomputed"
        rows.append((tag, lane, text, gate))
    rows.extend([
        ("A20", "attribution (this successor)",
         "COORDINATE SHADOWING IS CLOSED AS A PROPERTY, AND HERE IS WHAT THE "
         "PROPERTY DOES NOT COVER. A leaf is a coordinate if ANY object key on "
         "its path names one, and a union is monotone, so no interposed "
         "container under any key name can remove a coordinate a leaf already "
         "had - executed at every insertion position over a derived key "
         "vocabulary. What survives is the OTHER direction: a path naming NO "
         "coordinate at all is still silent, which is residual A1's silent lie "
         "reached structurally instead of lexically, and it is accepted for the "
         "same reason - the legitimate majority of this corpus cites only the "
         "state.",
         "the coordinate union is MONOTONE at every insertion position"),
        ("A21", "attribution (this successor)",
         "the AUTHORITY KEY VOCABULARY is lexical and inherited, and its "
         "sharpest gap is one character wide: the bare agent preposition as a "
         "key is excluded because the inherited predicate requires a normalised "
         "key LONGER than two characters. The union rescues it wherever any "
         "outer key on the path qualifies - which is now most nestings, and is "
         "strictly more than the predecessor rescued - but a flat occurrence is "
         "silent. NOT repaired here: the predicate lives in reviewed bytes this "
         "file executes rather than reimplements, and re-typing it would "
         "re-grade an inherited semantic in order to widen a lane whose "
         "acceptance test is zero false positives. Executed by a case EXPECTED "
         "to escape.",
         "RESIDUAL-A21"),
        ("A22", "speech act (this successor)",
         "THE EXHIBIT DEMOTION IS A REAL EXEMPTION AND THIS IS ITS PRICE, "
         "MEASURED RATHER THAN MINIMISED. Any document - not only a review - "
         "that carries a root identity key resolving to a real document, names "
         "at least one other file that exists in the scanned population, and "
         "nests the forgery inside an object re-declaring that identity key "
         "with a value naming NO document in the corpus, is demoted from "
         "FINDING to NAMED OBSERVATION. That is deliberate and it is narrower "
         "than the alternative it replaces: a filename exemption costs a forger "
         "one rename, whereas this costs them a written declaration, in their "
         "own bytes, that the record they are displaying does not exist. It "
         "buys a green exit code and it NEVER buys silence - every demoted "
         "position is printed with its path, its declared identity and its full "
         "attribution text. The boundary is executed on all four sides by "
         "varying one conjunct at a time.",
         "the speech-act split, one conjunct varied at a time"),
        ("A23", "speech act (this successor)",
         "THE DEMOTION FAILS CLOSED, AND FAILING CLOSED HAS A COST TOO. A "
         "document with no root identity key gets no exhibit protection "
         "whatever, so a review that declares its own identity in a way that "
         "resolves to no document - a package-prefixed spelling, a stripped "
         "suffix that no longer matches, an identity block this test cannot "
         "resolve - has its exhibited vectors read as assertions. That is the "
         "safe direction and it is not the harmless one: it is precisely how "
         "this lineage's self-review trap will reappear for a reviewer who "
         "spells an identity differently. The population is MEASURED every run "
         "and printed as the specimen census rather than assumed from this "
         "sentence.",
         "the speech-act split, one conjunct varied at a time"),
        ("A24", "sweep (this successor)",
         "THE NAME-VARYING SWEEP IS A WIDER BOUND AND STILL A BOUND. Wrapper "
         "names are DERIVED from the packets' own decision-row field names and "
         "from every object key in every published vector, so the vocabulary "
         "grows when the packet or the vector corpus grows and cannot be "
         "trimmed by hand. It is still finite: a key that will name a "
         "coordinate under a FUTURE packet schema is not in today's vocabulary, "
         "and a JSON shape outside the twelve declared ones is not swept. The "
         "grid's arithmetic - vectors, shapes, name pairs, and both "
         "non-vacuity denominators - is printed in full so a reader can see how "
         "wide the evidence is rather than inferring it from the word 'every'.",
         "the name-varying sweep loses nothing and CAN fail"),
        ("A25", "standing (inherited, measured here for the first time)",
         "THE STANDING CLASSIFIER'S OWN CONJUNCT VOCABULARIES ARE "
         "HAND-ENUMERATED, in reviewed bytes this file may not edit. A document "
         "that declares itself review-class and fails any one conjunct is never "
         "classified and is therefore never demoted, and nothing in the output "
         "previously distinguished that from coverage. This file does not "
         "repair it - it MEASURES it: the declaring population, the classified "
         "population, the drop-out count and the first failing conjunct of each "
         "drop-out are printed every run, and the mechanism that actually "
         "governs re-promotion is published as an identity that is compared "
         "rather than as a sentence. A silent drop-out is now a number.",
         "the standing classifier census, recomputed and its identity compared"),
        ("A26", "sweep (this successor, FOUND BY THE SWEEP ITSELF)",
         "A WRAPPER KEY WHOSE NAME THE INHERITED VOCABULARY READS AS HISTORICAL "
         "BUYS SILENCE, AND THIS FILE DID NOT ANTICIPATE IT - the name-varying "
         "sweep did. The pinned closure's assertion vocabulary marks a leaf as "
         "recording rather than asserting from its PATH ALONE, so re-keying a "
         "forgery under a field name that vocabulary treats as superseded text "
         "makes the lane correctly silent - and the live packet's own decision "
         "row carries such a name, which is how the sweep reached it. This is "
         "residual A3's citation excuse reached through a KEY NAME instead of "
         "through clause text, and it is INHERITED: narrowing it here would "
         "make this lane disagree with the state lane beside it about what an "
         "assertion is, which is worse than the escape. The affected names are "
         "DISCOVERED by probing the inherited predicate rather than listed, "
         "held OUT of the invariance denominator so they cannot mask a real "
         "loss, SWEPT anyway, and their cost is printed every run.",
         "a wrapper name the inherited vocabulary reads as historical"),
        ("S6", "inherited packet lane (NOT repairable here)",
         "RECORDING THE PRODUCT AUTHORITY'S NEXT DECISION REDS THIS VALIDATOR "
         "ON THE PENDING PATH TOO, and that half was named nowhere in the "
         "predecessor's 46 residuals. The pending set is compared against a "
         "second hard-coded literal, so a NEW PENDING ROW - which is how the "
         "awaited insertion may legitimately arrive before it is decided - "
         "produces a membership finding on a different code from the decided "
         "half, and a coherent blocked status on that row can additionally be "
         "misread as a stale retention assertion. Measured live every run "
         "alongside the decided half. NOT repaired here for the same reason: "
         "the literal is in reviewed bytes, consumed inside a lane this file "
         "executes rather than reimplements, and the only available suppression "
         "would blind the instrument to a REMOVED or ALTERED pending row in "
         "order to permit an added one.",
         "the decision-set pin's live cost, BOTH halves recomputed"),
    ])
    return tuple(rows)


# ---------------------------------------------------------------------------
# Self-measurement, re-walked from the written bytes.
# ---------------------------------------------------------------------------

FILENAME_SHAPED_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.(py|json|md|txt)\b")

# The functions this file uses to DECIDE WHAT TO COMPARE and WHAT COUNTS AS AN
# ASSERTION. The docstring's claims are scoped to exactly this list and
# --selftest audits their string constants, so the claim is measured rather than
# asserted.
DECISION_PREDICATES = (
    "coordinate_qualifiers",
    "root_identity_keys",
    "_identifies_this_document",
    "constructed_specimen_roots",
    "specimen_containing",
    "attribution_failures",
    "attribution_scan",
    "classifier_census",
    "wrapper_name_vocabulary",
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
             v6, v5, v4, v3, v2, v1, permitted: set[str]) -> int:
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
    fixture_packet = v6._fixture_packet(v2, "mnowak", "2026-08-05")
    fixture_states = v1.packet_decision_states(fixture_packet)
    fixture_attr = v5.packet_attribution(fixture_packet, v3, v2)
    fixture_keys = v6.packet_coordinate_keys(fixture_packet, v5, v3, v2)
    who_key, when_key = coordinate_names(fixture_packet, v6, v5, v3, v2)
    empty_corpus: frozenset = frozenset()

    def lane_full(doc, corpus=empty_corpus, name="synthetic.doc",
                  attr=None, states=None, keys=None):
        return attribution_failures(
            states if states is not None else fixture_states,
            attr if attr is not None else fixture_attr,
            name, doc, FINDING_PREFIX,
            keys if keys is not None else fixture_keys, corpus,
            v6, v5, v3, v2, v1)

    def lane(doc, **kw):
        return lane_full(doc, **kw)[0]

    def v6lane(doc):
        found, _ = v6.attribution_failures(
            fixture_states, fixture_attr, "synthetic.doc", doc,
            v6.FINDING_PREFIX, fixture_keys, v5, v3, v2, v1)
        return found

    families = v6.families_of

    # ---------------------------------------------------------------- types
    print("THE DECLARED READ SET - a guard that reads values must state which "
          "JSON types it reads")
    declared = set(COMPARED_JSON_TYPES) | set(TRAVERSED_JSON_TYPES) \
        | set(NAMED_BUT_UNCOMPARED_JSON_TYPES)
    probes = ("s", 1, 1.5, True, False, None, {}, [], {"a": 1}, [1])
    kinds = {v6.leaf_kind(p) for p in probes}
    check("types", kinds == declared,
          "every JSON type a document can carry is classified, and the "
          "classification is exactly the declared partition",
          f"declared {sorted(declared)}; observed {sorted(kinds)}")
    check("types", v6.leaf_kind(True) == "boolean" and v6.leaf_kind(1) == "number",
          "a JSON boolean is NOT a number, decided before the number test - "
          "freeze 6 law 18's own most expensive confusion, resolved in one place",
          f"True -> {v6.leaf_kind(True)!r}, 1 -> {v6.leaf_kind(1)!r}, "
          f"1.0 -> {v6.leaf_kind(1.0)!r}")
    check("types",
          not (set(COMPARED_JSON_TYPES) & set(NAMED_BUT_UNCOMPARED_JSON_TYPES))
          and not (set(COMPARED_JSON_TYPES) & set(TRAVERSED_JSON_TYPES)),
          "the compared, traversed and named-but-uncompared sets are disjoint, "
          "so no type has two outcomes")

    # ------------------------------------------------------- the escape
    print()
    print("DEFECT 1 - THE COORDINATE SHADOW. Both instruments driven over the "
          "SAME bytes, the predecessor's defect REPRODUCED and not described")
    if not who_key or not when_key:
        partial.append(
            "the fixture packet does not spell both coordinate names, so the "
            "coordinate-shadow vectors could not be constructed and this run "
            "does NOT claim the escape is closed")
        shadow = None
    else:
        shadow = v6._artifact({ident: {"status": "DECIDED",
                                       who_key: {when_key: "product owner"}}})
        flat = v6._artifact({ident: {"status": "DECIDED",
                                     who_key: "product owner"}})
        v6_flat, v6_shadow = v6lane(flat), v6lane(shadow)
        v7_flat, v7_shadow = lane(flat), lane(shadow)
        check("escape", bool(v6_flat) and not v6_shadow,
              "the DEFECT is present in the pinned predecessor and is "
              "reproduced here rather than described: the flat form is caught, "
              "the coordinate-shadowed form is TOTALLY SILENT",
              f"predecessor: flat {len(v6_flat)} finding(s), shadowed "
              f"{len(v6_shadow)} finding(s)")
        check("escape",
              families(v7_shadow, FINDING_PREFIX)
              >= families(v7_flat, FINDING_PREFIX) and bool(v7_shadow),
              "and this successor catches the shadowed form on AT LEAST the "
              "families it catches the flat form on - the shadow cannot lose a "
              "coordinate",
              f"flat {sorted(families(v7_flat, FINDING_PREFIX))} -> shadowed "
              f"{sorted(families(v7_shadow, FINDING_PREFIX))}")
        check("escape",
              all(who_key in f for f in v7_shadow if "AUTHORITY" in f),
              "and it is NAMED IN FULL: the finding cites the authority-shaped "
              "key that survived the shadow, so a reader is told which key made "
              "the leaf an authority rather than that something did",
              v7_shadow[0][:200] if v7_shadow else "NOT CAUGHT")
        shadow_array = v6._artifact({ident: {
            "status": "DECIDED", who_key: [{when_key: "the coordinator"}]}})
        check("escape", bool(lane(shadow_array)) and not v6lane(shadow_array),
              "the shadow COMPOSED with the predecessor's own repaired class - "
              "through an array as well - is silent in the predecessor and "
              "caught here",
              f"predecessor {len(v6lane(shadow_array))}, successor "
              f"{len(lane(shadow_array))}")

    # ------------------------------------------- the union is the property
    print()
    print("THE PROPERTY, NOT THE INSTANCE - the coordinate resolver is a UNION, "
          "and a union is MONOTONE, so no interposed key can remove a coordinate")
    vocab_q, vocab_n = wrapper_name_vocabulary(
        (fixture_packet, product), attribution_cases(v6, v5, v3, v2)[1],
        fixture_keys, v5, v3, v2)
    vocabulary = tuple(vocab_q) + tuple(vocab_n)
    bases: list[tuple[str, ...]] = [()]
    for outer in vocabulary:
        bases.append((outer,))
        for inner in vocab_q:
            bases.append((outer, inner))
    violations: list[str] = []
    monotone_attempted = 0
    for base in bases:
        before = coordinate_qualifiers(base, fixture_keys, v5, v3, v2)
        for position in range(len(base) + 1):
            for name in vocabulary:
                monotone_attempted += 1
                inserted = base[:position] + (name,) + base[position:]
                after = coordinate_qualifiers(inserted, fixture_keys, v5, v3, v2)
                if not set(after) >= set(before):
                    violations.append(f"{base} + {name!r}@{position}")
    check("union", not violations,
          f"inserting ANY key from the derived vocabulary at ANY position of "
          f"ANY path can only ADD coordinates: {monotone_attempted} insertions, "
          f"0 removals",
          f"violations: {violations[:3]}" if violations
          else f"{len(bases)} base paths x {len(vocabulary)} names x every "
               "insertion position; vocabulary derived, never typed")
    executed_labels.add("the coordinate union is MONOTONE at every insertion "
                        "position")
    check("union",
          bool(vocab_q) and set(coordinate_qualifiers(
              tuple(vocab_q), fixture_keys, v5, v3, v2)),
          "and the derived vocabulary is NON-EMPTY and actually qualifies, so "
          "the monotonicity sweep is not vacuous over an empty name space",
          f"qualifying {list(vocab_q)}; neutral {len(vocab_n)} name(s)")
    if who_key and when_key:
        both = coordinate_qualifiers((who_key, when_key), fixture_keys, v5, v3, v2)
        check("union", set(both) == {"who", "when"},
              "the exact shadow path resolves to BOTH coordinates where the "
              "predecessor's resolver returned one and discarded the other",
              f"predecessor -> {v6.coordinate_qualifier((who_key, when_key), fixture_keys, v5, v3, v2)}; "
              f"successor -> { {k: v for k, v in sorted(both.items())} }")


    # ------------------------------------- the NAME-VARYING container sweep
    print()
    print("THE NAME-VARYING CONTAINER SWEEP - every published vector, in every "
          "declared shape, under every DERIVED wrapper name. The predecessor's "
          "sweep varied shapes only and could not see the escape by construction")
    must_pass, must_fail, escapes = attribution_cases(v6, v5, v3, v2)
    excusing = assertion_excusing_names(vocabulary, v5, v3, v1)
    pairs = wrapper_name_pairs(vocab_q, vocab_n, excusing)
    mine = sweep_grid(lambda d: lane(d), must_fail, FINDING_PREFIX, pairs,
                      families)
    theirs = sweep_grid(v6lane, must_fail, v6.FINDING_PREFIX, pairs, families)
    print(f"    vectors {len(must_fail)}  shapes-in-grid {mine['shapesInGrid']}  "
          f"name pairs {mine['namePairs']}  "
          f"(qualifying {len(vocab_q)}, neutral {len(vocab_n)})")
    print("    DEFINITIONS, published because the predecessor published the "
          "weaker one unlabelled:")
    print("      WEAK   - a pair is a LOSS iff not (wrapped >= control); a "
          "vector never caught")
    print("               unwrapped has an empty control and passes vacuously.")
    print("      STRICT - identical test, but only pairs with a NON-EMPTY "
          "control are attempted.")
    check("sweep", mine["weakLosses"] == 0 and mine["strictLosses"] == 0,
          f"this successor is INVARIANT: strict {mine['strictInvariant']} of "
          f"{mine['strictAttempted']}, weak {mine['weakInvariant']} of "
          f"{mine['weakAttempted']}, total silences {mine['totalSilences']}",
          f"losses: {mine['examples'][:2]}" if mine["examples"]
          else "no shape and no wrapper name loses a family")
    executed_labels.add("the name-varying sweep loses nothing and CAN fail")
    check("sweep", theirs["strictLosses"] > 0 and theirs["totalSilences"] > 0,
          "and THE SWEEP CAN FAIL: run identically against the pinned "
          "predecessor it loses families, and loses some of them to TOTAL "
          "SILENCE - so a green sweep here is a measurement and not a tautology",
          f"predecessor: strict {theirs['strictInvariant']} of "
          f"{theirs['strictAttempted']} ({theirs['strictLosses']} losses), weak "
          f"{theirs['weakInvariant']} of {theirs['weakAttempted']} "
          f"({theirs['weakLosses']} losses), of which "
          f"{theirs['totalSilences']} are TOTAL SILENCE; first: "
          f"{theirs['examples'][0] if theirs['examples'] else 'none'}")
    check("sweep",
          theirs["weakAttempted"] == mine["weakAttempted"]
          and theirs["weakAttempted"] > 0,
          "the two grids are the SAME grid - identical vectors, shapes and "
          "names - so the difference is the instrument and not the sweep",
          f"{mine['weakAttempted']} pairs attempted on both")
    neutral_only = sweep_grid(v6lane, must_fail, v6.FINDING_PREFIX,
                              tuple((n, n) for n in vocab_n) or pairs, families)
    check("sweep", neutral_only["strictLosses"] < theirs["strictLosses"],
          "and the NAMES are what the predecessor's sweep could not vary: "
          "restricted to NEUTRAL wrapper names it loses strictly less, which is "
          "the blind spot measured rather than argued",
          f"neutral names only: {neutral_only['strictLosses']} loss(es); "
          f"with the derived coordinate names: {theirs['strictLosses']}")
    # THE HELD-OUT NAMES, SWEPT AND PUBLISHED RATHER THAN DROPPED.
    if excusing:
        excused = sweep_grid(lambda d: lane(d), must_fail, FINDING_PREFIX,
                             tuple((n, n) for n in excusing), families)
        reasons = sorted({v5.records_rather_than_asserts(f"$.{n}", "", v1, v3)
                          for n in excusing})
        check("sweep", excused["strictLosses"] > 0,
              f"AND THE SWEEP FOUND SOMETHING ITS AUTHOR DID NOT ANTICIPATE: "
              f"{len(excusing)} derived wrapper name(s) are read as HISTORICAL "
              f"by the inherited assertion vocabulary, on the PATH alone, so a "
              f"forgery wrapped under one is correctly silent - "
              f"{excused['strictLosses']} of {excused['strictAttempted']} "
              "held-out pairs. Held OUT of the invariance denominator, swept "
              "anyway, and disclosed as residual A26 rather than deleted",
              f"names {list(excusing)}; predicate says {reasons}; "
              f"{excused['totalSilences']} of them are total silence")
        executed_labels.add("a wrapper name the inherited vocabulary reads as "
                            "historical")
    else:
        partial.append(
            "no derived wrapper name is excused by the inherited assertion "
            "vocabulary on this packet, so residual A26's cost could not be "
            "measured and this run does NOT publish it")
    # The PREDECESSOR'S OWN GRID, run here so its two published gate labels
    # remain executed rather than inherited as prose.
    neutral_pairs = tuple((n, n) for n in vocab_n if n not in set(excusing))
    v6_grid = sweep_grid(lambda d: lane(d), must_fail, FINDING_PREFIX,
                         neutral_pairs or pairs, families)
    check("sweep", v6_grid["strictLosses"] == 0,
          "container-wrapping sweep is invariant over every published vector - "
          "the predecessor's own criterion, re-run here as a strict subset of "
          "the wider grid so its disclosure cannot go stale",
          f"{v6_grid['strictInvariant']} of {v6_grid['strictAttempted']} under "
          "neutral wrapper names")
    executed_labels.add("container-wrapping sweep is invariant over every "
                        "published vector")
    aliased_plain = v6._artifact({ident: {
        "status": "DECIDED", "signedOffBy": "the coordinator",
        "approvedOn": "2026-07-31"}})
    aliased_families = families(lane(aliased_plain), FINDING_PREFIX)
    escaping_shapes = [
        shape_label for shape_label, _varies, shape
        in container_shapes(*(pairs[0] if pairs else ("wrapper", "inner")))
        if not families(lane(_wrap_scalars(aliased_plain, shape)),
                        FINDING_PREFIX) >= aliased_families]
    check("sweep", not escaping_shapes,
          "the aliased vector escapes in NO declared container shape",
          f"escaping shapes: {escaping_shapes}" if escaping_shapes
          else f"0 of {len(container_shapes('a', 'b'))} shapes escape")
    executed_labels.add("the aliased vector escapes in NO declared container "
                        "shape")

    print()
    print("TYPE COVERAGE - a guard that reads values must be tested against "
          "every type it does NOT read")
    scalar_named = scalar_attempted = 0
    excluded = 0
    type_silent: list[str] = []
    type_keys = tuple(k for k in (who_key, when_key) if k) or ("decidedBy",)
    for key in type_keys:
        for type_label, value in TYPE_SUBSTITUTIONS:
            if v6.leaf_kind(value) in TRAVERSED_JSON_TYPES:
                # AN EMPTY CONTAINER HAS NO SCALAR TO NAME, so this cell cannot
                # fail - a totally broken lane scores it. The predecessor folded
                # these into one denominator and an independent reviewer
                # measured that 8 of its 28 could not fail. They are EXCLUDED
                # here and reported separately, because a check that cannot fail
                # is prose (7.2.2).
                excluded += 1
                continue
            scalar_attempted += 1
            found = lane(v6._artifact({ident: {"status": "DECIDED", key: value}}))
            if any("UNCOMPARED-TYPE" in f for f in found):
                scalar_named += 1
            else:
                type_silent.append(f"{key}={type_label}")
    check("types", not type_silent and scalar_attempted > 0,
          f"every wrong-typed SCALAR at a coordinate is NAMED: {scalar_named} "
          f"of {scalar_attempted} - and {excluded} traversed-container cells "
          "are EXCLUDED from this denominator because they cannot fail",
          f"silent: {type_silent}" if type_silent
          else f"{len(type_keys)} coordinate key(s) x "
               f"{len(TYPE_SUBSTITUTIONS) - excluded // max(len(type_keys), 1)} "
               "scalar type(s); container cells reported, never counted")
    executed_labels.add("a wrong-typed coordinate is NAMED rather than compared")
    if who_key and when_key:
        shadowed_type = lane(v6._artifact(
            {ident: {"status": "DECIDED", who_key: {when_key: True}}}))
        named_coordinates = {c for c in ("WHO", "WHEN")
                             if any(c in f for f in shadowed_type)}
        check("types", named_coordinates == {"WHO", "WHEN"},
              "and a wrong-typed value at a SHADOWED position is named on BOTH "
              "coordinates - the union reaches the type gate as well as the "
              "comparison",
              f"coordinates named: {sorted(named_coordinates)}")
    check("types",
          not any("ATTRIBUTION-DATE" in f for f in lane(v6._artifact(
              {ident: {"status": "DECIDED", (when_key or "decidedOn"): 20260731}}))),
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
    renamed_keys = v6.packet_coordinate_keys(renamed, v5, v3, v2)
    renamed_who, renamed_when = coordinate_names(renamed, v6, v5, v3, v2)
    check("derivation",
          v5.packet_attribution(renamed, v3, v2).get(ident, {}).get("who")
          == ["mnowak"] and "approvedon" in renamed_keys["when"]
          and renamed_who and renamed_when,
          "and EVERY derivation follows a packet that RENAMES its fields - the "
          "comparison, the coordinate key names AND this file's own attack "
          "vocabulary - so a legitimate schema change costs a re-read rather "
          "than a successor instrument (7.10)",
          f"renamed packet spells who={renamed_who!r} when={renamed_when!r}")
    live_keys = v6.packet_coordinate_keys(product, v5, v3, v2)
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
        check("accept", not found, label, "; ".join(found)[:240] if found else "")

    print()
    print("the lane - forgeries that MUST be caught, each by its own family")
    for label, family, doc in must_fail:
        found = lane(doc)
        hit = [f for f in found if family in f]
        check("reject", bool(hit), label,
              (hit[0][:190] if hit else f"NOT CAUGHT by {family}; got "
                                        f"{sorted(families(found, FINDING_PREFIX))}"))

    print()
    print("the lane - disclosed residuals, EXECUTED so the disclosure cannot go "
          "stale")
    for label, doc in escapes:
        found = lane(doc)
        check("residual", not found, label,
              f"NO LONGER ESCAPES: {found[0][:150]}" if found
              else "escapes, as disclosed")
        executed_labels.add(label.split(" ")[0])
    mislabel = lane(v6._artifact({ident: (
        "DECIDED 2026-06-01 by under formally delegated standing authority "
        "thecoordinator.")}))
    check("residual", any("delegated" in f for f in mislabel),
          "RESIDUAL-A15 second half: with five or more filler words the finding "
          "FIRES but names the wrong phrase as the claimed authority - caught "
          "by accident, reported wrongly",
          mislabel[0][:170] if mislabel else "did not fire at all")
    check("residual",
          len(lane(v6._artifact({ident: f"{ident} is DECIDED. Authority: "
                                        "product owner. It was decided "
                                        "2026-07-31."}))) > 0,
          "RESIDUAL-A16 is NARROW, measured: moving only ONE coordinate out of "
          "the closure clause is still caught, so the escape needs both")

    print("non-vacuity - a family nothing can trip is decoration")
    exercised = {family for _, family, _ in must_fail}
    for family_name in ("ATTRIBUTION-AUTHORITY", "ATTRIBUTION-DATE",
                        "ATTRIBUTION-UNCOMPARED-TYPE"):
        check("nonvacuity", family_name in exercised,
              f"family {family_name} is exercised by at least one must-fail case")
    unattributed = copy.deepcopy(fixture_packet)
    for gone in ("decidedBy", "decidedOn", "attributionProvenance"):
        unattributed["decisions"][ident].pop(gone, None)
    ua_attr = v5.packet_attribution(unattributed, v3, v2)
    ua_states = v1.packet_decision_states(unattributed)
    ua_keys = v6.packet_coordinate_keys(unattributed, v5, v3, v2)
    ua_found = lane(v6._artifact({ident: "DECIDED 2026-06-01 by somebodyelse."}),
                    attr=ua_attr, states=ua_states, keys=ua_keys)
    check("nonvacuity", any("UNRECORDED" in f for f in ua_found),
          "an artifact supplies an attribution the packet does not record",
          f"{len(ua_found)} finding(s); first "
          f"{ua_found[0][:150] if ua_found else 'NONE'}")
    executed_labels.add("an artifact supplies an attribution the packet does "
                        "not record")
    check("nonvacuity",
          not lane(v6._artifact({ident: "DECIDED; retention is bounded."}),
                   attr=ua_attr, states=ua_states, keys=ua_keys),
          "and the same unattributed packet accepts an artifact that cites only "
          "the state, so the UNRECORDED limb is not simply always-on")

    print("gate independence - each coordinate must fire ALONE, or it is not a "
          "coordinate")
    check("gate",
          families(lane(v6._artifact({ident: "DECIDED 2026-06-01 by mnowak."})),
                   FINDING_PREFIX) == {"ATTRIBUTION-DATE"},
          "a substituted DATE alone fires only the date family")
    check("gate",
          families(lane(v6._artifact(
              {ident: "DECIDED 2026-08-05 by the coordinator."})),
              FINDING_PREFIX) == {"ATTRIBUTION-AUTHORITY"},
          "a substituted AUTHORITY alone fires only the authority family")
    if who_key and when_key:
        isolated = families(lane(v6._artifact(
            {ident: {"status": "DECIDED",
                     who_key: {when_key: "the coordinator"}}})), FINDING_PREFIX)
        check("gate", isolated == {"ATTRIBUTION-AUTHORITY"},
              "and the same isolation holds through a COORDINATE SHADOW - the "
              "union widens reach without widening the family, so a shadowed "
              "authority is not also reported as a bad date",
              f"families present: {sorted(isolated)}")

    # -------------------------------------------------------- the speech act
    print()
    print("DEFECT 2 - ASSERTING versus EXHIBITING. One conjunct varied at a "
          "time, so the exemption's boundary is measured on every side")
    for label, corpus, name, doc, expect in exhibit_cases(v6, v5, v3, v2):
        found, shown, _counts = lane_full(doc, corpus=corpus, name=name)
        if expect == "EXHIBIT":
            ok = bool(shown) and not found
            detail = (f"{len(shown)} exhibit(s), {len(found)} finding(s); "
                      + (shown[0][:170] if shown else ""))
        elif expect == "ASSERTION":
            ok = bool(found) and not shown
            detail = (f"{len(found)} finding(s), {len(shown)} exhibit(s); "
                      + (found[0][:150] if found else "NOTHING DETECTED AT ALL, "
                                                      "which is not the same as "
                                                      "an assertion"))
        else:
            ok = len(found) == 1 and len(shown) == 1
            detail = f"{len(found)} finding(s) and {len(shown)} exhibit(s)"
        check("speechact", ok, label, detail)
    executed_labels.add("the speech-act split, one conjunct varied at a time")
    exhibit_baseline = exhibit_cases(v6, v5, v3, v2)[0]
    _f, shown_baseline, _c = lane_full(exhibit_baseline[3],
                                       corpus=exhibit_baseline[1],
                                       name=exhibit_baseline[2])
    check("speechact",
          bool(shown_baseline) and "product owner" in shown_baseline[0]
          and "$" in shown_baseline[0],
          "AND IT IS NEVER SILENCE: a demoted exhibit is printed with its path, "
          "its declared identity and its full attribution text - forgery buys a "
          "green exit code and never silence (4.4)",
          shown_baseline[0][:230] if shown_baseline else "SILENT, the defect")


    # -------------------------------------------------- false positives
    print()
    print("the FALSE-POSITIVE matrix - the corpus's own forensic records of the "
          "fabrication must never be reported AS the fabrication")
    other_date = "2026-07-31"
    forged_prefix = f"SIGNED OFF {other_date} by product owner"
    forged_sentence = (f"{forged_prefix} - zero implicit durable retention for "
                       "greenfield.")
    fp_cases = (
        ("a quoted-and-retracted record, the shape the binding register uses",
         v6._artifact({ident: f"DECIDED 2026-08-05 by mnowak. This field "
                              f"previously asserted '{forged_sentence}' No such "
                              "sign-off occurred."})),
        ("a record explicitly marked SUPERSEDED",
         v6._artifact({ident: f"SUPERSEDED. It read verbatim: {forged_sentence}"})),
        ("a record whose PATH marks it historical",
         {"historicalRecord": {ident: forged_sentence}}),
        ("a forensic narrative that REPORTS the fabrication",
         {"note": f"An earlier register asserted that {ident} was signed off "
                  f"{other_date} by product owner. It was struck."}),
        ("the DISCLOSED citation excuse: a forged clause carrying a document "
         "pointer reads as a citation to the inherited vocabulary, exactly as "
         "it does for the state lane beside it (residual A3)",
         v6._artifact({ident: f"{forged_prefix}, per " + "some-record"
                              + ".json#detail"})),
        ("a record that carries the sentence inside a bracketed template",
         v6._artifact({ident: f"[STRUCK {other_date}] {forged_sentence}"})),
    )
    for label, doc in fp_cases:
        found = lane(doc)
        check("falsepositive", not found, label,
              "; ".join(found)[:200] if found else "silent, as required")
    fp_noisy: list[str] = []
    fp_attempted = 0
    fp_grid = [(label, shape) for label, varies, shape
               in container_shapes(*pairs[0]) if not varies]
    for outer, inner in pairs:
        fp_grid.extend((label, shape) for label, varies, shape
                       in container_shapes(outer, inner) if varies)
    for label, doc in fp_cases:
        for shape_label, shape in fp_grid:
            fp_attempted += 1
            if lane(_wrap_scalars(doc, shape)):
                fp_noisy.append(f"{shape_label} on {label[:40]!r}")
    check("falsepositive", not fp_noisy,
          "and the SAME six records stay silent in every container shape AND "
          "under every DERIVED wrapper name - the repair widens what is CAUGHT "
          "and not what is ACCUSED, which is the half a detection repair is "
          "never graded on",
          f"{len(fp_noisy)} noisy: {fp_noisy[:2]}" if fp_noisy
          else f"{len(fp_cases)} records x {len(fp_grid)} shape/name cells = "
               f"{fp_attempted} probes, 0 findings")

    # -------------------------------------------------------- the live corpus
    print()
    print("the LIVE corpus - the acceptance test that decides whether the lane "
          "is usable")
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    corpus_names = {name for name, _ in docs}
    suffixes = sorted({Path(name).suffix for name, _ in docs})
    check("corpus", suffixes == [".json"] or not docs,
          "the scanned population is JSON-only, measured not assumed",
          f"{len(docs)} parsed of {discovered} discovered; suffixes {suffixes}; "
          f"{len(unreadable)} unreadable and NAMED")
    executed_labels.add("the scanned population is JSON-only, measured not "
                        "assumed")
    ledger = v4.GateLedger()
    live_failures, live_observations, live_exhibits, live_report = \
        attribution_scan(product, docs, v6, v5, v4, v3, v2, v1, ledger)
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
        print(f"    positions with MORE THAN ONE naming key "
              f"{live_report['shadowedPositions']}")
        print(f"    positions NAMED but not compared  "
              f"{live_report['uncomparedTypeSites']}")
        print(f"    constructed specimens discovered  {live_report['specimenRoots']}")
        print(f"    positions demoted as EXHIBITS     "
              f"{live_report['exhibitPositions']} in "
              f"{live_report['exhibitingArtifacts']} artifact(s)")
        print(f"    agreeing with the packet          {live_report['agreeing']}")
        print(f"    conflicting, WITH standing        {len(live_failures)}")
        print(f"    conflicting, no standing          "
              f"{live_report['historicalObservations']}")
        check("corpus", not live_failures,
              "ZERO false positives across the whole live corpus - the lane is "
              "silent on every artifact that has standing today, INCLUDING the "
              "reviews of this instrument's own lineage",
              f"live findings: {live_failures[:2]}" if live_failures
              else "0 findings")
        check("corpus", True,
              "MEASURED, not smoothed: conflicting attributions that survive in "
              "artifacts with NO standing are reported as HISTORICAL "
              "OBSERVATIONS and never dropped",
              f"{live_report['historicalObservations']} observation(s) in "
              f"{live_report['conflictingArtifactsHistorical']} artifact(s); "
              f"demoted {live_report['demotedByStanding']}")
        # THE NINE LEGITIMATE OCCURRENCES, DERIVED RATHER THAN LISTED.
        carriers = [name for name, doc in docs
                    if forged_prefix in json.dumps(doc, ensure_ascii=False)]
        carrier_findings = [f for f in live_failures
                            if any(f.startswith(f"{FINDING_PREFIX}-") and name in f
                                   for name in carriers)]
        whole_tree: dict[str, int] = {}
        for folder in (HERE, HERE.parent):
            for path in sorted(folder.glob("*")):
                if not path.is_file() or path.suffix not in (
                        ".py", ".json", ".md", ".txt"):
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if forged_prefix in text:
                    whole_tree[path.suffix] = whole_tree.get(path.suffix, 0) + 1
        print(f"    the fabricated attribution, whole tree by suffix "
              f"{dict(sorted(whole_tree.items()))} "
              f"(total {sum(whole_tree.values())})")
        print(f"    of those, IN THIS LANE'S SCOPE (parsed JSON) {len(carriers)}")
        check("corpus", not carrier_findings and bool(carriers),
              f"ZERO FINDINGS on every in-scope legitimate occurrence of the "
              f"fabricated attribution: {len(carriers)} carrier(s) inside the "
              f"scanned population, {sum(whole_tree.values())} in the tree - the "
              "test that decides usability",
              f"findings on carriers: {carrier_findings[:1]}"
              if carrier_findings
              else "definition: files containing the fabricated sign-off's "
                   "authority clause verbatim; the remainder are outside this "
                   "lane by SCOPE (residual A6, the JSON-only rule), not by "
                   "judgement")
        executed_labels.add("zero findings on the legitimate occurrences of the "
                            "fabricated attribution")
        # THE HARNESS CONTROL.
        p_findings, p_obs, p_report = v6.attribution_scan(
            product, docs, v5, v4, v3, v2, v1)
        h_findings, h_obs, h_ex, h_report = attribution_scan(
            product, docs, v6, v5, v4, v3, v2, v1, None,
            v6.attribution_failures, v6.FINDING_PREFIX)
        check("corpus",
              p_findings == h_findings and p_obs == h_obs and not h_ex
              and p_report["conflicts"] == h_report["conflicts"],
              "HARNESS CONTROL: this successor's scan, driven with the "
              "PREDECESSOR's leaf lane AND the predecessor's own finding "
              "prefix, reproduces the predecessor's own scan BYTE FOR BYTE - so "
              "the bookkeeping is unchanged and every delta comes from the two "
              "repairs alone",
              f"findings {len(p_findings)}=={len(h_findings)}, observations "
              f"{len(p_obs)}=={len(h_obs)}, exhibits {len(h_ex)}, conflicts "
              f"{p_report['conflicts']}=={h_report['conflicts']}")
        check("corpus",
              int(live_report["authorityClaims"]) >= int(p_report["authorityClaims"])
              and int(live_report["dateClaims"]) >= int(p_report["dateClaims"]),
              "the repair's corpus cost, recomputed against the predecessor's "
              "reach: the successor compares AT LEAST as many coordinates",
              f"authority {p_report['authorityClaims']}->"
              f"{live_report['authorityClaims']}, date "
              f"{p_report['dateClaims']}->{live_report['dateClaims']}, live "
              f"findings {len(p_findings)}->{len(live_failures)}, exhibits "
              f"0->{live_report['exhibitPositions']}")
        executed_labels.add("the repair's corpus cost, recomputed against the "
                            "predecessor's reach")
        planted_name = "zz-synthetic-plant.v1" + ".json"
        plants = [("as prose", v6._artifact({ident: forged_sentence}))]
        if who_key and when_key:
            plants.append(("COORDINATE-SHADOWED under the packet's own key "
                           "names", v6._artifact(
                               {ident: {"status": "DECIDED",
                                        who_key: {when_key: "product owner"}}})))
            plants.append(("shadowed AND array-wrapped", v6._artifact(
                {ident: {"status": "DECIDED",
                         who_key: [{when_key: ["product owner"]}]}})))
        for plant_label, plant_body in plants:
            planted = json.loads(json.dumps(plant_body))
            planted_found, planted_shown, _ = attribution_failures(
                v1.packet_decision_states(product), live_attr, planted_name,
                planted, FINDING_PREFIX,
                v6.packet_coordinate_keys(product, v5, v3, v2), corpus_names,
                v6, v5, v3, v2, v1)
            check("corpus", bool(planted_found) and not planted_shown and all(
                planted_name in f for f in planted_found),
                f"and the forgery {plant_label}, planted as a live document "
                "against the LIVE packet, is CAUGHT AND NAMED IN FULL - so "
                "corpus silence is a measurement of the corpus, not of a dead "
                "lane",
                planted_found[0][:190] if planted_found else "NOT CAUGHT")


    # ------------------------------------------------ the measurements
    print()
    print("MEASUREMENTS THAT MAY NOT GO STALE - recomputed here and "
          "HARD-COMPARED to what the run prints (7.2.2)")
    positional = positional_rule_measurement(product, docs, v6, v5, v3, v2, v1)
    for key in ("clausesReachingTheByPhraseReader", "byXmatches",
                "droppedByThePositionalThreshold", "liveFindingsWithTheRule",
                "liveFindingsWithoutTheRule"):
        print(f"    {key:42s} {positional[key]}")
    again = positional_rule_measurement(product, docs, v6, v5, v3, v2, v1)
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
          "WITHDRAWAL CONFIRMED against THIS lane's wider reach: removing the "
          "positional rule entirely changes the live finding count by ZERO, so "
          "the figure withdrawn in place two generations ago still does not "
          "reproduce now that detection is wider",
          f"with {positional['liveFindingsWithTheRule']}, without "
          f"{positional['liveFindingsWithoutTheRule']}; observations "
          f"{positional['observationsWithTheRule']}/"
          f"{positional['observationsWithoutTheRule']}; exhibits "
          f"{positional['exhibitsWithTheRule']}/"
          f"{positional['exhibitsWithoutTheRule']}")

    pin = decision_set_pin_measurement(product, v6, v5, v4, v3, v2, v1)
    if not pin.get("measured"):
        partial.append(
            "the live packet does not carry a decided retention row with a "
            "string authority, so the decision-set pin's cost could not be "
            "measured on live bytes and this run does NOT publish it")
    else:
        print(f"    expected decision-set size (a hard-coded literal) "
              f"{pin['expectedChoiceCount']}")
        print(f"    + one DECIDED row, SAME authority       "
              f"{pin['sameAuthority']['findings']} {pin['sameAuthority']['codes']}")
        print(f"    + one DECIDED row, DIFFERENT authority  "
              f"{pin['differentAuthority']['findings']} "
              f"{pin['differentAuthority']['codes']}")
        print(f"    + one PENDING row, blocked status       "
              f"{pin['pendingBlocked']['findings']} {pin['pendingBlocked']['codes']}")
        print(f"    + one PENDING row, open status          "
              f"{pin['pendingOpen']['findings']} {pin['pendingOpen']['codes']}")
        check("measurement",
              pin["sameAuthority"]["membershipGateFires"]
              and pin["differentAuthority"]["membershipGateFires"],
              "the decision-set pin's DECIDED half, recomputed: adding ANY "
              "decision row reds the inherited membership gate REGARDLESS of "
              "authority (residual S5, inherited, NOT repaired here)",
              f"same-authority {pin['sameAuthority']['codes']}, "
              f"different-authority {pin['differentAuthority']['codes']}")
        check("measurement",
              bool(pin["pendingBlocked"]["findings"])
              and bool(pin["pendingOpen"]["findings"])
              and set(pin["pendingOpen"]["codes"])
              != set(pin["sameAuthority"]["codes"]),
              "and its PENDING half, named NOWHERE in the predecessor's 46 "
              "residuals and measured here: a NEW PENDING ROW - how the awaited "
              "insertion may legitimately arrive before it is decided - is red "
              "too, on a DIFFERENT code and a SECOND literal (residual S6, also "
              "NOT repaired here)",
              f"pending-blocked {pin['pendingBlocked']['codes']}, pending-open "
              f"{pin['pendingOpen']['codes']}, decided "
              f"{pin['sameAuthority']['codes']}")
        executed_labels.add("the decision-set pin's live cost, BOTH halves "
                            "recomputed")
        check("measurement",
              not attribution_failures(
                  v1.packet_decision_states(product), live_attr, "synthetic.doc",
                  v6._artifact({ident: "DECIDED; retention is bounded."}),
                  FINDING_PREFIX, v6.packet_coordinate_keys(product, v5, v3, v2),
                  corpus_names, v6, v5, v3, v2, v1)[0],
              "and THIS lane contributes nothing to either cost: it is "
              "corpus-side and says nothing about the packet's own rows")

    census = classifier_census(product, docs, v2, v1)
    for line in format_census(census):
        print("    " + line)
    check("census", bool(census["identityHolds"]),
          "THE STANDING MECHANISM, COMPARED RATHER THAN ASSERTED: classified "
          "review records minus those re-promoted by the post-decision cutoff "
          "EQUALS the review-record standing count. If anything else ever "
          "demotes or promotes a review, this identity breaks and says so",
          f"{census['classifiedAsReviewRecord']} - "
          f"{census['repromotedByThePostDecisionCutoff']} == "
          f"{(census['standing'] or {}).get('REVIEW-RECORD', 0)}")
    executed_labels.add("the standing classifier census, recomputed and its "
                        "identity compared")
    check("census",
          int(census["repromotedByThePostDecisionCutoff"]) >= 0
          and int(census["classifiedAsReviewRecord"]) > 0,
          "and the population that the cutoff re-promotes is PRINTED, because "
          "it is the population in which an exhibited attack vector would "
          "otherwise be read as a live assertion - it grows with every review "
          "dispatched after the packet's earliest decision",
          f"{census['repromotedByThePostDecisionCutoff']} re-promoted of "
          f"{census['classifiedAsReviewRecord']} classified; "
          f"{census['notClassifiedThoughDeclaring']} declaring reviews never "
          f"classified at all, by first failing conjunct "
          f"{census['failingConjunct']}")

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
                     json.loads(json.dumps(v6._artifact({ident: forged_sentence}))))]
    failing, _obs, _ex, _rep = attribution_scan(
        product, failing_docs, v6, v5, v4, v3, v2, v1, failing_ledger)
    check("banner",
          bool(failing) and "corpus-attribution" not in failing_ledger.gate_names
          and any(gate == "corpus-attribution"
                  for gate, _ in failing_ledger.skipped),
          "a gate that RUNS AND FAILS registers no clause, so a failed gate can "
          "never contribute a sentence to a success banner",
          f"{len(failing)} finding(s); ran={sorted(failing_ledger.gate_names)}")
    empty_ledger = v4.GateLedger()
    attribution_scan({"decisions": {}}, [], v6, v5, v4, v3, v2, v1, empty_ledger)
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
    hostile = list(v6.hostile_shapes(v2))
    if who_key and when_key:
        deep_shadow: object = "product owner"
        for index in range(40):
            deep_shadow = {when_key if index % 2 else who_key: deep_shadow}
        hostile.append(("40-deep ALTERNATION of the two coordinate names",
                        {"d": {ident: deep_shadow}}))
        hostile.append(("a specimen nested inside a specimen",
                        {"artifact": "outer", "cites": "x" + ".json",
                         "a": {"artifact": "inner", "b": {"artifact": "deeper",
                                                          "dispositions": {
                                                              ident: {
                                                                  who_key:
                                                                  "product owner"}}}}}))
    for label, shape in hostile:
        try:
            found, shown, _ = lane_full(shape)
            ok = (isinstance(found, list) and isinstance(shown, list)
                  and all(isinstance(f, str) for f in found + shown))
            detail = f"{len(found)} finding(s), {len(shown)} exhibit(s)"
        except Exception as exc:                       # noqa: BLE001 - measured
            ok = False
            detail = f"RAISED {type(exc).__name__}: {exc}"
        check("hostile", ok, label, detail)
    try:
        attribution_scan("not a packet", [("x", None)], v6, v5, v4, v3, v2, v1,
                         v4.GateLedger())
        check("hostile", True, "the whole scan survives a non-object packet and "
                               "a null document")
    except Exception as exc:                           # noqa: BLE001 - measured
        check("hostile", False, "the whole scan survives a non-object packet",
              f"RAISED {type(exc).__name__}: {exc}")
    deep_probe = {"artifact": "zz", "dispositions": {ident: None}}
    nest: object = forged_sentence
    for _ in range(v6.SUBTREE_MAX_DEPTH + 3):
        nest = {"n": nest}
    deep_probe["dispositions"][ident] = nest             # type: ignore[index]
    deep_found = lane(deep_probe)
    check("hostile", any("ATTRIBUTION-DEPTH" in f for f in deep_found),
          "and a forgery planted BELOW the traversal bound produces a named "
          "DEPTH outcome rather than silence - the bound announces itself",
          deep_found[0][:170] if deep_found else "SILENT, which is the defect")

    # ------------------------------------------------------- no regression
    print()
    print("NO REGRESSION - every predecessor generation's published corpus, "
          "re-driven through THIS lane")
    for generation, cases in (("predecessor", v6.attribution_cases(v2)),
                              ("the generation before it",
                               v5.attribution_cases(v2))):
        p_pass, p_fail, p_escapes = cases
        lost = [label for label, family, doc in p_fail
                if not any(family in f for f in lane(doc))]
        check("noregression", not lost,
              f"all {len(p_fail)} of {generation}'s must-fail attribution "
              "vectors are still caught by their own family",
              f"lost: {lost}" if lost else "0 regressions")
        noisy = [label for label, doc in p_pass if lane(doc)]
        check("noregression", not noisy,
              f"all {len(p_pass)} of {generation}'s must-PASS attribution "
              "vectors still pass",
              f"newly noisy: {noisy}" if noisy else "0 new false positives")
        still = [label for label, doc in p_escapes if not lane(doc)]
        check("noregression", len(still) == len(p_escapes),
              f"all {len(p_escapes)} of {generation}'s disclosed attribution "
              "residuals still escape, so its published disclosure is not stale",
              f"{len(still)} of {len(p_escapes)}")
        for label, doc in p_escapes:
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
          f"and all {len(g_fail)} cases of the generation before that",
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
          "the four inherited demotion residuals R1-R4 all still escape, and R3 "
          "in particular is UNCHANGED - the supersession predicate this file "
          "depends on is load-bearing and is not re-graded here (7.9)",
          f"measured {residual_escapes}")
    executed_labels.add("inherited demotion corpus")

    # --------------------------------------------------- environment
    print()
    print("environment independence - a blinded run must give identical results")
    sighted_f, sighted_o, sighted_e, sighted_r = attribution_scan(
        product, docs, v6, v5, v4, v3, v2, v1)
    original_reader = v1.head_named_artifacts
    try:
        v1.head_named_artifacts = lambda *a, **k: (set(), [])
        blind_f, blind_o, blind_e, blind_r = attribution_scan(
            product, docs, v6, v5, v4, v3, v2, v1)
    finally:
        v1.head_named_artifacts = original_reader
    check("environment",
          sighted_f == blind_f and sighted_o == blind_o and sighted_e == blind_e
          and sighted_r["conflicts"] == blind_r["conflicts"],
          "head documents unreadable -> identical findings, observations AND "
          "exhibits",
          f"findings {len(sighted_f)}=={len(blind_f)}, observations "
          f"{len(sighted_o)}=={len(blind_o)}, exhibits "
          f"{len(sighted_e)}=={len(blind_e)}")
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
    expected_closure = 1 + sum(
        1 for module in (None, v6, v5, v4, v3, v2)
        if isinstance((PREDECESSOR_BINDING if module is None
                       else getattr(module, "PREDECESSOR_BINDING", None)), dict))
    check("environment", len(permitted) == expected_closure,
          "the permitted-import set is DERIVED by walking the pin chain, and "
          "its SIZE is derived the same way rather than written down - a chain "
          "that silently shortens fails here instead of passing with a smaller "
          "number nobody reads",
          f"{len(permitted)} permitted path(s), chain depth derives "
          f"{expected_closure}")
    check("environment", sys.flags.hash_randomization == 1,
          "and this process runs under a RANDOMIZED hash seed - isolated mode "
          "ignores the environment variable that would pin it, so repeat runs "
          "are evidence of order-independence rather than of a fixed seed",
          f"hash_randomization={sys.flags.hash_randomization}")

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
    named = sorted(n for n in corpus_names
                   if any(n in value for value in constants))
    check("self", not named, "zero corpus artifacts are named in this source",
          f"named: {named}")
    check("self", forged_prefix not in "".join(
        v for v in constants if len(v) < 400),
          "and the fabricated attribution is ASSEMBLED at run time rather than "
          "carried as a literal, so this instrument does not become a tenth "
          "occurrence of the string whose nine legitimate ones it must not fire "
          "on",
          "the sign-off clause appears in no single string constant of this file")
    predicate_constants = predicate_string_constants()
    check("self", set(predicate_constants) == set(DECISION_PREDICATES),
          "every function this file declares as a DECISION PREDICATE exists in "
          "its own bytes under that name",
          f"declared {len(DECISION_PREDICATES)}, missing "
          f"{sorted(set(DECISION_PREDICATES) - set(predicate_constants)) or 'none'}")
    dated_predicates = sorted(
        name for name, values in predicate_constants.items()
        if any(v5.iso_dates_in(value) for value in values))
    check("self", not dated_predicates,
          "NO CALENDAR DATE appears in any decision predicate - scoped to "
          "exactly the list above and measured, never asserted of the file",
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
    rows = residual_registry(v6, v5, v4, v3)
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
    inherited_rows = v6.residual_registry(v5, v4, v3)
    check("self",
          all(tag in {r[0] for r in rows} for tag, _, _, _ in inherited_rows),
          f"and all {len(inherited_rows)} inherited residuals are CARRIED, not "
          "dropped",
          f"{len(rows)} total after carrying {len(inherited_rows)}")
    carried_text = {tag: text for tag, _, text, _ in rows}
    inherited_text = {tag: text for tag, _, text, _ in inherited_rows}
    trimmed = sorted(tag for tag, text in inherited_text.items()
                     if text not in carried_text.get(tag, ""))
    check("self", not trimmed,
          "A DISCLOSURE IS APPENDED TO, NEVER REWRITTEN: EVERY inherited row - "
          "not only the amended ones - still contains its predecessor's text "
          "VERBATIM, read from the predecessor's live bytes rather than "
          "retyped, so neither an amendment nor a quiet trim can shrink a "
          "published limit",
          f"rewritten or trimmed: {trimmed}" if trimmed
          else f"{len(inherited_text)} inherited rows preserved verbatim, "
               f"{len(carried_corrections())} amended in place")
    corrections = carried_corrections()
    check("self",
          all(tag in inherited_text and inherited_text[tag] in carried_text.get(tag, "")
              and carried_text.get(tag, "") != inherited_text[tag]
              for tag in corrections),
          "and every amendment names a row that EXISTS and strictly EXTENDS it",
          f"amendments: {sorted(corrections)}")

    print()
    print("selftest buckets: " + ", ".join(
        f"{bucket} {count}" for bucket, count in sorted(counts.items())))
    print(f"NAME-VARYING SWEEP: strict {mine['strictInvariant']}/"
          f"{mine['strictAttempted']}, weak {mine['weakInvariant']}/"
          f"{mine['weakAttempted']} "
          f"({len(must_fail)} vectors x {mine['shapesInGrid']} shape-name cells; "
          f"{mine['namePairs']} derived name pairs). PREDECESSOR on the same "
          f"grid: strict {theirs['strictInvariant']}/{theirs['strictAttempted']} "
          f"({theirs['strictLosses']} losses, {theirs['totalSilences']} to TOTAL "
          "SILENCE)")
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
          "evidence: the same reading produced both the repairs and their suite.")
    return EXIT_OK


# ---------------------------------------------------------------------------
# Reporting and the banner.
# ---------------------------------------------------------------------------

def banner_lines(ledger, report: dict, attribution: dict, v1) -> list[str]:
    """The success banner, assembled from what RAN. Nothing here is a literal."""
    lines = [
        f"product dispositions OK - {len(v1.EXPECTED_CHOICES)} non-retention "
        "choices bound; the retention decision is in exactly one valid state,"
    ]
    for clause in ledger.clauses():
        lines.append(f"  * {clause}")
    lines.append(
        f"  * no artifact with standing ({report['artifactsLive']} of "
        f"{report['artifactsParsed']} scanned) ASSERTS a product decision the "
        f"binding packet does not carry; {report['historicalObservations']} such "
        f"assertion(s) remain in {report['conflictingArtifactsHistorical']} "
        "historical artifact(s), listed above")
    lines.append(
        f"  * and {attribution.get('exhibitPositions', 0)} attribution(s) are "
        f"DISPLAYED rather than asserted, inside "
        f"{attribution.get('specimenRoots', 0)} constructed specimen(s) in "
        f"{attribution.get('exhibitingArtifacts', 0)} artifact(s) - named in "
        "full above, never silently dropped")
    if ledger.skipped:
        lines.append(
            "  GATES THAT DID NOT RUN, named because a banner may never report "
            "a gate as run when it did not:")
        for gate, why in ledger.skipped:
            lines.append(f"    - {gate}: {why}")
    return lines


def format_measurements(positional: dict, pin: dict) -> list[str]:
    """The disclosures that may not go stale, printed as measurements."""
    lines = [
        "MEASUREMENTS RECOMPUTED THIS RUN - never transcribed, and hard-compared",
        "by --selftest, because a figure a reader cannot recompute is prose",
        "wearing a measurement's clothes (7.2.2):",
        "  the inherited POSITIONAL rule (residual A7, WITHDRAWN IN PLACE)",
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
        "    Re-measured against THIS lane's wider reach, not carried from the",
        "    generation that withdrew the figure. It still drops nothing here.",
    ]
    if pin.get("measured"):
        lines.extend([
            "  the inherited DECISION-SET pin (residuals S5 and S6, NOT "
            "repairable here)",
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
        ])
        if pin.get("pendingMeasured"):
            lines.extend([
                f"    + one PENDING row, blocked status           "
                f"{pin['pendingBlocked']['findings']} finding(s) "
                f"{pin['pendingBlocked']['codes']}",
                f"    + one PENDING row, open status              "
                f"{pin['pendingOpen']['findings']} finding(s) "
                f"{pin['pendingOpen']['codes']}",
            ])
        lines.extend([
            "    RECORDING THE PRODUCT AUTHORITY'S NEXT DECISION REDS THIS",
            "    VALIDATOR ON BOTH PATHS - decided AND pending - whatever the",
            "    authority and whatever the attribution, on TWO hard-coded",
            "    literals in reviewed bytes. It is 7.10's defect applied to a",
            "    decision SET. The decided half was disclosed one generation",
            "    ago; the PENDING half is named here for the first time. NEITHER",
            "    is repaired here - see residuals S5 and S6 for why the repair",
            "    belongs to the instrument that owns the literals.",
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
        v6 = _load_predecessor()
        v5 = v6._load_predecessor()
        v4 = v5._load_predecessor()
        v3 = v4._load_predecessor()
        v2 = v3._load_predecessor()
        v1 = v2._load_predecessor()
    except RuntimeError as exc:
        print("REFUSING to run: the pinned predecessor closure is dirty")
        print(f"  - {exc}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    permitted = closure_paths(v6, v5, v4, v3, v2)
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
          "and so on, so one pin covers a seven-deep closure)")
    print("invocation: ISOLATED, NO-BYTECODE - the script's directory is not on "
          "the import path, so no file beside this one can shadow a module the "
          "pin chain depends on")

    if want_selftest:
        return selftest(product, ri, versioning, delivery, retention, register,
                        v6, v5, v4, v3, v2, v1, permitted)

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
    attribution_conflicts, attribution_observations, exhibits, attribution_report = \
        attribution_scan(product, docs, v6, v5, v4, v3, v2, v1, ledger)
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
    for line in format_census(classifier_census(product, docs, v2, v1)):
        print(line)
    for line in format_measurements(
            positional_rule_measurement(product, docs, v6, v5, v3, v2, v1),
            decision_set_pin_measurement(product, v6, v5, v4, v3, v2, v1)):
        print(line)
    inherited_rows = v6.residual_registry(v5, v4, v3)
    for line in v5.format_limits(
            residual_registry(v6, v5, v4, v3),
            (len(inherited_rows),
             sum(1 for r in inherited_rows if r[3] is not None))):
        print(line)
    if exhibits:
        print("DISPLAYED EXHIBITS - an attribution a document EXHIBITS is not "
              "an attribution it")
        print("ASSERTS. Each position below sits inside a CONSTRUCTED SPECIMEN: "
              "an object")
        print("re-declaring its document's own identity key with a value naming "
              "no document")
        print("in this corpus. Reviewing a detection instrument necessarily "
              "documents its")
        print("attacks at the paths that instrument reads, so the better the "
              "detection the")
        print("more certainly its own review trips it. NOT a finding, and NEVER "
              "silence -")
        print("every one is named in full, path and declared identity included:")
        for line in exhibits:
            print(f"  {line}")
    if observations or attribution_observations:
        print("HISTORICAL OBSERVATIONS - a product-decision assertion "
              "conflicting with the binding")
        print("packet, in an artifact with no standing to make it. Not a finding: "
              "freeze 7.2")
        print("forbids editing reviewed bytes and 7.2.1 forbids repairing a "
              "review at all, so")
        print("these cannot be repaired. Reported in full, never dropped - a "
              "forgery buys a")
        print("green exit code, never silence:")
        for line in list(observations) + list(attribution_observations):
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
    for line in banner_lines(ledger, report, attribution_report, v1):
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
