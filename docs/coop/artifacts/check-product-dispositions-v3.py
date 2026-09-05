#!/usr/bin/env python3
"""Successor to check-product-dispositions-v2.py. Edits nothing; repairs one lane.

WHY A SUCCESSOR AND NOT AN EDIT
-------------------------------
Section 7.2 forbids changing reviewed bytes in place; the sanctioned repair is a
new file. The predecessor is a RUNTIME INPUT here, hash-verified before use,
which section 7.3 explicitly permits. It in turn hash-verifies and executes ITS
predecessor, so all three instruments' detection semantics are re-used
BYTE-IDENTICALLY rather than retyped.

WHAT THIS SUCCESSOR CHANGES, AND WHAT IT DELIBERATELY DOES NOT
--------------------------------------------------------------
An independent review of the predecessor returned ACCEPT_WITH_BLOCKERS at two
blockers and measured NINETEEN ESCAPES IN THIRTY ATTEMPTS against an instrument
publishing four residuals. Both blockers sit in ONE lane - the decision-set lane.
This file repairs exactly that lane and touches nothing else.

  UNCHANGED, ON PURPOSE - the standing/demotion lane.
  REJECTED / SUPERSEDED / REVIEW-RECORD artifacts are demoted to HISTORICAL
  OBSERVATIONS and never dropped; standing is DISCOVERED, not listed. That
  doctrine, its five review-record conjuncts, its four supersession gates and
  its residuals R1-R4 are the predecessor's and are CALLED, not copied. In
  particular residual R3 - one substantive key makes a successor, so repair
  QUALITY is not graded - is LOAD-BEARING and is left exactly as it is. Section
  7.9 records what it does and why changing it is a large semantic change that
  must be argued rather than slipped in. It is not argued here, so it is not
  changed. NOTE also that section 7.9's two figures justifying the rejection of
  stronger gates (149/758 and 232/758) are WITHDRAWN; nothing in this file
  re-quotes them, and no gate here rests on them.

  REPAIRED - blocker 1: the placeholder guard was TYPE-BLIND.
  The predecessor's `is_unfilled` returns False for every non-string, so the
  identical placeholder one level down was a filled authority. Reproduced
  against live bytes: `decidedBy: ["[UNSET - the authority's name]"]` added ZERO
  findings, as did `{...}`, `{}`, `[]`, `12345`, `true`, `decidedOn: 20260805`
  (which additionally bypassed the ISO-date check) and `decidedOn:
  ["2026-08-05"]`. EIGHT OF NINE ESCAPED; only `null` was caught, because
  `is_unfilled` special-cases None first. This contradicted the instrument's own
  printed bound ("binds structure and type"), and `_non_empty_leaf` eleven lines
  away already recursed into non-strings - an inconsistency inside one file
  rather than an unconsidered case.

  REPAIRED - blocker 2: the decision's SUBSTANCE was unbound.
  Reproduced against live bytes: flipping `durableDefault` from
  `DURABLE_RETAINED` to `EPHEMERAL_DISCARDED` added zero findings; so did
  flipping `implicitDurableRetention`; so did rewriting `decidedBy` from the
  authority's own git identity to `the coordinator`, to `the product authority`,
  to `z`, and to `jdoe`; so did moving `decidedOn` to `2099-12-31`; so did
  replacing the attribution provenance with a confession that a coordinator
  invented it. EIGHT OF EIGHT ESCAPED. The guard that made a coordinator ask the
  product authority for attribution instead of inventing it did not detect the
  attribution being changed afterwards. A GUARD THAT REFUSES A BLANK FIELD BUT
  ACCEPTS A SUBSTITUTED ONE PROTECTS THE CEREMONY AND NOT THE DECISION.

  The predecessor's own positive corpus encodes one of those escapes as CORRECT:
  its `_DECIDED_GOOD` fixture - the row its suite asserts MUST PASS - carries
  `decidedBy: "the product authority"`, which is the reviewer's measured escape
  "generic, names nobody". A suite that certifies the escape cannot find it.
  This file's positive corpus is therefore built fresh rather than inherited,
  and `--selftest` REPORTS that the predecessor's must-pass fixture now fails
  this lane, as a measured delta rather than as a claim.

THE REPAIR MODEL IS NOT INVENTED HERE
-------------------------------------
Two sibling instruments solved this and caught 17 of 17 mutations. Their moves
are adopted, and two are strengthened:

  1. require a NAMED authority, rejecting a closed set of non-authority ROLES
     BY NAME - which is section 4.4's shape, a recommendation converted into a
     declaration. STRENGTHENED: the siblings compare the whole normalised
     string, so `coordinator` is rejected and `the coordinator` is not. This
     file matches on TOKENS, so any string whose every meaningful word is a role
     term is rejected. Measured necessity, not decoration: `the coordinator` and
     `the product authority` are BOTH corroborated by the live decision's own
     narrative, so the corroboration gate below does not catch either. The two
     gates are complementary and both are load-bearing.
  2. require a real ISO-8601 calendar date that does not precede the packet's
     own authoring date. STRENGTHENED: the extended `YYYY-MM-DD` form is
     required BEFORE parsing, because `date.fromisoformat` accepts the basic
     form and would read `"20260805"` as a date. The predecessor's diagnostic
     for `1999-01-01` said it "carries no ISO date", which is false - its regex
     was a 21st-century test wearing an ISO label. That diagnostic is corrected.
  3. require the DECISION'S OWN NARRATIVE to corroborate both authority fields,
     so substituting a plausible human name fails as UNCORROBORATED.
     STRENGTHENED: corroboration is matched on WORD BOUNDARIES, not raw
     containment, so a one-character authority cannot be corroborated by the
     letter appearing inside an unrelated word.
  4. require the two posture fields to AGREE WITH EACH OTHER, so a single-field
     flip is incoherent. EXTENDED: the posture's own narrative must corroborate
     the selected posture and must not contradict it - which is what turns the
     both-fields-flipped "coherent" lie from an escape into a finding, because
     the narrative still says the opposite.
  5. require that NO OTHER POSITION in the packet still asserts the pre-decision
     state without a supersession marker. This corpus retains superseded text
     verbatim, so a bare substring hunt false-positives; the marker test is what
     makes it work. Measured on the live packet: 0 hits outside the row AND 0
     inside it - the row's own `supersedes` leaf quotes `BLOCKED_ON_PHASE_1A`
     and is correctly excused by its path.

  Plus one the siblings have and the predecessor lacks entirely: a decision is
  NOT a signature. A manufactured `signOff`/`approvedBy` key, or a state field
  declaring positive authority, is section 4.4 recurring. Section 11's *Product
  signer* line is still `[UNSET]`, and nothing in the packet may quietly supply
  one. This gate runs over the WHOLE packet, not only the retention row: section
  4.4's own general lesson is that a guard covering the artifact where a defect
  was first seen, rather than the CLASS that can carry it, produces confident
  green output over an unexamined region.

THE ACCEPTED FAILURE MODE, STATED BEFORE THE EVIDENCE
-----------------------------------------------------
A COHERENT lie. Substitute the authority AND rewrite every narrative leaf that
names it, and this file exits 0 - measured, not predicted, and executed by a
case in the suite that is EXPECTED to escape. The posture equivalent is
narrowed but not closed: flipping both posture fields is now CAUGHT because the
narrative contradicts them, so the surviving attack must also rewrite the
narrative. Section 7.8's bound applies in full and is not repealed by any of the
above: this binds structure, type and internal agreement. It cannot bind the
truth of content, and no instrument in this corpus can.
"""

from __future__ import annotations

import copy
import datetime
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# The predecessor is a RUNTIME INPUT, hash-verified before execution (7.3).
# Drift is EXIT_REFUSED, never a silent fallback: this file's claim to preserve
# the reviewed standing doctrine rests on these exact bytes, and the predecessor
# in turn hash-verifies ITS predecessor, so one pin covers the whole closure.
# ---------------------------------------------------------------------------
PREDECESSOR_BINDING = {
    "path": "check-product-dispositions-v2.py",
    "sha256": "71999471340e53389227a11ee1886865b9822f4f4229f5fc83c8a4b968d4daad",
    "bytes": 74716,
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
DECLARED_FLAGS = ("--selftest",)

# A hostile document must not be able to exhaust the interpreter stack. Every
# walker below is depth-bounded and the bound FAILS CLOSED: reaching it is a
# finding that says the region was not examined, never a silent truncation.
MAX_DEPTH = 60


def _load_predecessor():
    """Hash-verify then execute the predecessor as a library. Never falls back."""
    path = HERE / PREDECESSOR_BINDING["path"]
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RuntimeError(
            f"cannot read pinned predecessor {PREDECESSOR_BINDING['path']} "
            f"({type(exc).__name__})"
        ) from exc
    if len(raw) != PREDECESSOR_BINDING["bytes"]:
        raise RuntimeError(
            f"pinned predecessor {PREDECESSOR_BINDING['path']} is {len(raw)} "
            f"bytes, expected {PREDECESSOR_BINDING['bytes']}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PREDECESSOR_BINDING["sha256"]:
        raise RuntimeError(
            f"pinned predecessor {PREDECESSOR_BINDING['path']} hashes {digest}, "
            f"expected {PREDECESSOR_BINDING['sha256']}")
    spec = importlib.util.spec_from_file_location("_pd_v2", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot build an import spec for the pinned predecessor")
    module = importlib.util.module_from_spec(spec)
    # NO BYTECODE, EVER. Sibling instruments in this directory snapshot
    # `__pycache__/*.pyc` and compare the snapshot across a run. Executing a
    # predecessor as a library would drop a .pyc into a directory those
    # instruments measure - a new instrument silently perturbing another
    # instrument's evidence. The predecessor does the same for its own.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    _make_witnesses_reproducible(module)
    return module


class _OrderedKeySet(set):
    """A set that iterates in sorted order. Membership semantics are unchanged."""

    def __iter__(self):
        return iter(sorted(super().__iter__()))


def _make_witnesses_reproducible(module) -> None:
    """Give the predecessor's key-set helper a deterministic iteration order.

    WHY, AND WHY THIS IS NOT AN EDIT. The independent review of the predecessor
    recorded a non-blocking defect: its `has_reviewer_role` and
    `has_verdict_shape` return the FIRST match found while iterating a SET of
    normalised key names, so the `role~`/`verdict~` witness printed in every
    HISTORICAL OBSERVATION varies with PYTHONHASHSEED. Measured across three
    seeds, the review found three different output digests while the standing
    set and the exit code were byte-identical. Section 7.2 says a verdict binds
    bytes AND an environment; a review that captures this instrument's output as
    evidence captures something the next run will not reproduce.

    The predecessor's bytes are reviewed and may not be changed, so this does
    not change them: it replaces the value its helper RETURNS with a set that
    iterates in sorted order, in this process only. Every conjunct that consumes
    it is an EXISTENCE test - does ANY key match a stem - which is
    order-independent, so no standing decision can move. Only WHICH equally-
    valid witness gets printed becomes determinate. The selftest re-runs the
    predecessor's entire evasion and control corpora after this is installed, so
    the claim "no standing decision moves" is executed rather than asserted.
    """
    original = module._keys_within

    def deterministic(node, max_depth, depth=0, out=None, budget=None):
        result = original(node, max_depth, depth, out, budget)
        # Only the outermost call's return value is consumed; the recursive
        # calls mutate `out` in place and discard what they return, so wrapping
        # at depth 0 alone is both sufficient and free of per-node copying.
        return _OrderedKeySet(result) if depth == 0 else result

    module._keys_within = deterministic


# ---------------------------------------------------------------------------
# Closed vocabularies.
#
# Each of these is a CONTINUING INVARIANT (7.2.2) - "X must always hold of Y" -
# and gets a semantic gate. None of them is a snapshot of today's value; the
# authored values live in NOTICES below, which cannot change an exit code.
# ---------------------------------------------------------------------------

# Words that name a ROLE rather than an authority. Section 4.4's fabrication was
# a reviewer's RECOMMENDATION converted into a declaration and attributed to
# "product owner" - a role, not a person. A decision must name WHO.
NON_AUTHORITY_ROLE_TOKENS = frozenset({
    "coordinator", "coordination", "architecture", "architect", "reviewer",
    "review", "reviewers", "lane", "agent", "assistant", "checker", "instrument",
    "unknown", "tbd", "todo", "na", "none", "null", "nil", "system", "auto",
    "automated", "implementer", "implementor", "author", "authoring",
    "product", "authority", "owner", "ownership", "team", "management",
    "leadership", "someone", "somebody", "anon", "anonymous", "user",
    "customer", "consumer", "signer", "signatory", "lead", "manager",
    "maintainer", "committee", "board", "office", "session", "conversation",
    "chat", "verbal", "above", "below", "same", "self", "me", "us", "we",
    "them", "they", "it", "unnamed", "unspecified", "unattributed", "pending",
    "placeholder", "unset", "blank", "empty", "redacted", "withheld",
})
# Words carrying no identifying content, dropped before the role test so that
# "the coordinator" is measured as {coordinator}.
ROLE_STOPWORDS = frozenset({
    "the", "a", "an", "of", "by", "for", "and", "or", "our", "this", "that",
    "from", "on", "in", "to", "at", "as", "is", "was", "per", "via", "with",
})

# The extended ISO-8601 calendar form. Required BEFORE parsing, because
# `date.fromisoformat` also accepts the basic form and would read "20260805" as
# a valid date - which is one of the eight measured type escapes.
ISO_EXTENDED_RE = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})\s*$")

# Placeholder shapes, over and above the predecessor's own string vocabulary
# (which is reused unchanged for strings). These catch the bracketed template
# even when it is not the whole value.
PLACEHOLDER_RE = re.compile(
    r"\[\s*(UNSET|TBD|TODO|FIXME|PENDING|PLACEHOLDER|FILL|FILL[- ]?IN|NAME|"
    r"DATE|SIGNER|AUTHORITY|REDACTED|XXX)\b",
    re.IGNORECASE)

# A decision is NOT a signature (4.5). These keys manufacture one.
FABRICATED_AUTHORITY_KEYS = frozenset({
    "signoff", "signedoff", "signedoffby", "signature", "signatureblock",
    "signer", "productsigner", "productsignoff", "productacceptance",
    "acceptedby", "approvedby", "approval", "approvedon", "countersigned",
    "ratifiedby", "authorisedby", "authorizedby",
})
# ...and these values declare positive authority state in a status-shaped field.
FABRICATED_AUTHORITY_VALUES = frozenset({
    "SIGNED", "SIGNEDOFF", "PRODUCTSIGNEDOFF", "APPROVED", "SEALED", "ACCEPTED",
    "RATIFIED", "COUNTERSIGNED", "AUTHORISED", "AUTHORIZED",
})
STATE_SHAPED_KEYS = frozenset({
    "status", "state", "currentstate", "disposition", "verdict", "outcome",
    "signoffstatus", "acceptancestate",
})

# Strings that ASSERT the pre-decision retention state. The corpus retains
# superseded text VERBATIM (4.4, 4.5), so a bare substring hunt fires on an
# honest supersession record. A hit counts only when nothing in the leaf, and
# nothing in its path, marks it as superseded, overridden or withdrawn.
PENDING_STATE_TOKENS = (
    "BLOCKED_ON_PHASE_1A", "BLOCKED_ON_PHASE1A", "blocked on Phase 1A",
    "blocked on phase 1a", "remains visibly blocked", "intentionally unresolved",
    "UNSELECTED",
)
SUPERSESSION_MARKERS = (
    "supersed", "SUPERSED", "read verbatim", "retained here verbatim",
    "prior value", "historical", "no longer", "withdraw", "WITHDRAW",
    "used to say", "USED TO", "formerly", "overrid", "OVERRID", "overturn",
    "recommendation", "previously", "PREVIOUSLY",
)

# Posture. `durableDefault` selects a stance; `implicitDurableRetention`
# restates it; the row's own narrative must agree with both. The stance is
# DERIVED from the declared value rather than compared against a pinned literal,
# so a legitimate future amendment to a different durable posture still passes.
UNSELECTED_POSTURES = frozenset({
    "", "UNSELECTED", "UNDECIDED", "PENDING", "TBD", "TODO", "NONE", "NULL",
    "N/A", "NA", "UNKNOWN", "BLANK",
})
IMPLICIT_VALUES = frozenset({"YES", "NO"})
DURABLE_VALUE_TOKENS = ("durable", "retain", "persist")
EPHEMERAL_VALUE_TOKENS = ("ephemeral", "discard", "transient", "refuse",
                          "nonretain", "no_retention")
# Narrative stance vocabulary, applied to the posture subtree's prose. This is a
# TRANSCRIPTION and is declared as one (7.8: "an instrument must re-derive its
# constants from the artifact it checks, or it is testing its own
# transcription"). It cannot be derived - no oracle turns an enum into English -
# so instead it is gated in BOTH directions by `--selftest`: it must be silent
# on a coherent packet and must fire on a both-fields-flipped one.
DURABLE_NARRATIVE_TERMS = (
    " retains durably ", " retain durably ", " retained durably ",
    " durably and unboundedly ", " proceeds and writes ",
    " writes analysis evidence ", " proceeds and write ",
    " implicit durable retention is yes ", " retains durably and unboundedly ",
)
EPHEMERAL_NARRATIVE_TERMS = (
    " writes nothing ", " write nothing ", " refuse and write nothing ",
    " ephemeral only ", " never writes ", " never write ",
    " proceeds ephemeral ", " proceed ephemeral ", " refuses the request ",
    " implicit durable retention is no ", " advisory ephemeral only ",
    " retains nothing ", " discards ",
)

FINDING_PREFIX = "PD3"


# ---------------------------------------------------------------------------
# Depth-bounded traversal. Fail-closed at the bound.
# ---------------------------------------------------------------------------

def string_leaves(node: object, prefix: str, depth: int = 0,
                  overflow: list[str] | None = None):
    """(path, text) for every string leaf, bounded. Overflow is REPORTED."""
    if depth > MAX_DEPTH:
        if overflow is not None and prefix not in overflow:
            overflow.append(prefix)
        return
    if isinstance(node, dict):
        for key, child in node.items():
            yield from string_leaves(child, f"{prefix}.{key}", depth + 1, overflow)
    elif isinstance(node, list):
        for index, child in enumerate(node):
            yield from string_leaves(child, f"{prefix}[{index}]", depth + 1, overflow)
    elif isinstance(node, str):
        yield prefix, node


def _norm(text: str) -> str:
    lowered = str(text).lower()
    flat = "".join(ch if ch.isalnum() else " " for ch in lowered)
    return " " + " ".join(flat.split()) + " "


def _dotted(node: object, path: str) -> object:
    for step in path.split("."):
        if not isinstance(node, dict) or step not in node:
            return None
        node = node[step]
    return node


def _marked_superseded(path: str, text: str) -> bool:
    return (any(marker in text for marker in SUPERSESSION_MARKERS)
            or any(marker in path for marker in SUPERSESSION_MARKERS))


def _word_bounded(needle: str) -> re.Pattern:
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(needle) + r"(?![A-Za-z0-9])")


# ---------------------------------------------------------------------------
# (1) THE TYPE REPAIR. Blocker 1.
#
# The predecessor's ruling is CORRECT and is kept verbatim by delegation: a
# bracketed template in an authority field is strictly weaker evidence than the
# fabrication the instrument exists to catch, so it fails. What was wrong was
# the implementation's reach, not the ruling. An authority field is a SCALAR
# IDENTITY: a name, or a date. A container is not an authority under any
# reading, so the fail-closed direction is to refuse every non-string and to say
# so - and additionally to hunt the placeholder INSIDE the container, so the
# diagnostic names what is really there rather than only its shape.
# ---------------------------------------------------------------------------

def authority_field_failures(field: str, value: object, where: str, v2,
                             present: bool = True) -> list[str]:
    """Type + placeholder gate for a scalar authority field."""
    out: list[str] = []
    if isinstance(value, str):
        if v2.is_unfilled(value) or PLACEHOLDER_RE.search(value):
            out.append(
                f"{FINDING_PREFIX}-PLACEHOLDER: {where}.{field} is an UNFILLED "
                f"placeholder ({value!r}); a prepared amendment may never read "
                "as a taken decision")
        return out
    if not present:
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-ABSENT: {where}.{field} is not recorded "
            "at all; a decision with no recorded authority is not a decision")
        return out
    kind = "null" if value is None else type(value).__name__
    out.append(
        f"{FINDING_PREFIX}-AUTHORITY-TYPE: {where}.{field} is {kind}, not a "
        f"non-empty string ({value!r}). An authority field is a scalar identity; "
        "any other type is refused fail-closed, because the predecessor's guard "
        "returned False for every non-string and the identical placeholder one "
        "level down was read as a filled authority")
    overflow: list[str] = []
    nested = [(path, text)
              for path, text in string_leaves(value, f"{where}.{field}", 0, overflow)
              if v2.is_unfilled(text) or PLACEHOLDER_RE.search(text)]
    for path, text in nested:
        out.append(
            f"{FINDING_PREFIX}-PLACEHOLDER-NESTED: {path} carries the placeholder "
            f"{text[:72]!r} one level inside {where}.{field}. The literal "
            "template is present in the packet")
    if overflow:
        out.append(
            f"{FINDING_PREFIX}-DEPTH: {where}.{field} nests deeper than "
            f"{MAX_DEPTH}; it was NOT fully examined ({overflow[0]})")
    return out


# ---------------------------------------------------------------------------
# (2) THE SUBSTANCE REPAIR. Blocker 2.
# ---------------------------------------------------------------------------

def _role_verdict(name: str) -> list[str]:
    """The meaningful word tokens, and whether every one of them names a role."""
    return [t for t in re.findall(r"[a-z]+", name.lower())
            if t not in ROLE_STOPWORDS]


def authority_identity_failures(decided_by: str, leaves: list[tuple[str, str]],
                                where: str) -> list[str]:
    """A NAMED authority, corroborated by the decision's own narrative."""
    out: list[str] = []
    stripped = decided_by.strip()
    tokens = _role_verdict(stripped)
    if tokens and all(token in NON_AUTHORITY_ROLE_TOKENS for token in tokens):
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-ROLE: {where}.decidedBy is "
            f"{decided_by!r}, whose every meaningful token {sorted(set(tokens))!r} "
            "names a ROLE rather than an authority. Section 4.4's fabricated "
            "sign-off was attributed to a role in exactly this shape - a "
            "recommendation converted into a declaration")
        return out
    if len(stripped) < 3:
        out.append(
            f"{FINDING_PREFIX}-AUTHORITY-SHORT: {where}.decidedBy is "
            f"{decided_by!r}, too short to identify anybody")
        return out
    pattern = _word_bounded(stripped)
    corroborating = [path for path, text in leaves
                     if path != f"{where}.decidedBy" and pattern.search(text)]
    if not corroborating:
        out.append(
            f"{FINDING_PREFIX}-UNCORROBORATED: {where}.decidedBy is "
            f"{decided_by!r} and NO OTHER leaf of the decision names it. Section "
            "4.4's fabrication was a single-source attribution; a bare authority "
            "field is that shape, and a plausible substituted name is caught "
            "here and nowhere else")
    return out


def authority_date_failures(decided_on: str, leaves: list[tuple[str, str]],
                            packet_date: object, where: str) -> list[str]:
    out: list[str] = []
    match = ISO_EXTENDED_RE.match(decided_on)
    if not match:
        out.append(
            f"{FINDING_PREFIX}-DATE-FORM: {where}.decidedOn is {decided_on!r}, "
            "which is not an ISO-8601 extended calendar date (YYYY-MM-DD). The "
            "extended form is required BEFORE parsing because the basic form "
            "'20260805' parses as a date and would pass")
        return out
    try:
        when = datetime.date(int(match.group(1)), int(match.group(2)),
                             int(match.group(3)))
    except ValueError as exc:
        out.append(
            f"{FINDING_PREFIX}-DATE-REAL: {where}.decidedOn is {decided_on!r}, "
            f"which is not a real calendar date ({exc})")
        return out
    if isinstance(packet_date, str):
        authored = ISO_EXTENDED_RE.match(packet_date)
        if authored:
            try:
                origin = datetime.date(int(authored.group(1)),
                                       int(authored.group(2)),
                                       int(authored.group(3)))
            except ValueError:
                origin = None
            if origin is not None and when < origin:
                out.append(
                    f"{FINDING_PREFIX}-DATE-ORDER: {where}.decidedOn "
                    f"({decided_on}) PRECEDES the packet's own authoring date "
                    f"({packet_date}); a decision cannot predate the document "
                    "that constitutes it")
    pattern = _word_bounded(decided_on.strip())
    corroborating = [path for path, text in leaves
                     if path != f"{where}.decidedOn" and pattern.search(text)]
    if not corroborating:
        out.append(
            f"{FINDING_PREFIX}-UNCORROBORATED: {where}.decidedOn is "
            f"{decided_on!r} and NO OTHER leaf of the decision names it. "
            "A date nobody else in the row mentions was substituted, not recorded")
    # DELIBERATELY ABSENT: an upper bound on the date. A wall-clock comparison
    # would make this instrument's verdict depend on WHEN it is run, which is an
    # undeclared environment dependency under 7.2 and a time bomb under 7.10.
    # A far-future date is caught by the corroboration gate above instead -
    # measured: '2099-12-31' has zero corroborating leaves in the live row.
    return out


def _stance_of_value(value: str) -> str:
    normalised = re.sub(r"[^a-z]", "", value.lower())
    durable = any(token in normalised for token in DURABLE_VALUE_TOKENS)
    ephemeral = any(token in normalised for token in EPHEMERAL_VALUE_TOKENS)
    if durable and not ephemeral:
        return "DURABLE"
    if ephemeral and not durable:
        return "EPHEMERAL"
    return "UNKNOWN"


def posture_failures(decision: dict, where: str) -> list[str]:
    """The posture must be SELECTED, INTERNALLY COHERENT, and CORROBORATED.

    This is the half of blocker 2 that binds what was actually decided. Flipping
    `durableDefault` alone contradicts `implicitDurableRetention`; flipping both
    together - the sibling instruments' declared accepted failure mode -
    contradicts the posture's OWN NARRATIVE, which still describes the posture
    that was really chosen. The remaining attack must rewrite the narrative too.
    """
    out: list[str] = []
    posture = decision.get("defaultPosture")
    if not isinstance(posture, dict):
        out.append(
            f"{FINDING_PREFIX}-POSTURE-ABSENT: {where}.defaultPosture is "
            f"{type(posture).__name__ if posture is not None else 'absent'}, not "
            "an object. A decided retention row that selects no posture has "
            "decided nothing")
        return out

    durable = posture.get("durableDefault")
    implicit = posture.get("implicitDurableRetention")
    if not isinstance(durable, str) or not durable.strip():
        out.append(
            f"{FINDING_PREFIX}-POSTURE: {where}.defaultPosture.durableDefault is "
            f"{durable!r}, not a non-empty string")
        return out
    if durable.strip().upper() in UNSELECTED_POSTURES or PLACEHOLDER_RE.search(durable):
        out.append(
            f"{FINDING_PREFIX}-POSTURE: {where}.defaultPosture.durableDefault is "
            f"{durable!r}; a decided row must SELECT a posture")
        return out
    stance = _stance_of_value(durable)
    if stance == "UNKNOWN":
        out.append(
            f"{FINDING_PREFIX}-POSTURE-UNDECIDABLE: "
            f"{where}.defaultPosture.durableDefault is {durable!r}, which names "
            "neither a durable nor an ephemeral stance, so its agreement with "
            "implicitDurableRetention cannot be decided. Fail-closed: a novel "
            "posture vocabulary needs a successor instrument, not a silent pass")
        return out

    if not isinstance(implicit, str) or not implicit.strip() \
            or PLACEHOLDER_RE.search(implicit):
        out.append(
            f"{FINDING_PREFIX}-POSTURE: "
            f"{where}.defaultPosture.implicitDurableRetention is {implicit!r}; "
            "a decided row must state it")
        return out
    stated = implicit.strip().upper()
    if stated not in IMPLICIT_VALUES:
        out.append(
            f"{FINDING_PREFIX}-POSTURE: "
            f"{where}.defaultPosture.implicitDurableRetention is {implicit!r}, "
            f"outside the closed vocabulary {sorted(IMPLICIT_VALUES)!r}")
        return out
    expected = "YES" if stance == "DURABLE" else "NO"
    if stated != expected:
        out.append(
            f"{FINDING_PREFIX}-POSTURE-INCOHERENT: durableDefault={durable!r} is "
            f"a {stance} stance and requires implicitDurableRetention="
            f"{expected!r}; the packet says {implicit!r}. The two posture fields "
            "disagree, so ONE OF THEM WAS CHANGED WITHOUT THE OTHER")
        return out

    # Narrative stance. Only leaves that are not themselves marked as quoting a
    # superseded or overridden position count - the live row quotes the
    # architecture recommendation it OVERRODE, verbatim, and that quotation must
    # not be read as the row's own stance.
    overflow: list[str] = []
    narrative = [
        (path, text)
        for path, text in string_leaves(posture, f"{where}.defaultPosture", 0, overflow)
        if not path.endswith(".durableDefault")
        and not path.endswith(".implicitDurableRetention")
        and not _marked_superseded(path, text)
    ]
    own = DURABLE_NARRATIVE_TERMS if stance == "DURABLE" else EPHEMERAL_NARRATIVE_TERMS
    opposite = EPHEMERAL_NARRATIVE_TERMS if stance == "DURABLE" else DURABLE_NARRATIVE_TERMS
    supporting = [(path, term) for path, text in narrative
                  for term in own if term in _norm(text)]
    contradicting = [(path, term) for path, text in narrative
                     for term in opposite if term in _norm(text)]
    if not supporting:
        out.append(
            f"{FINDING_PREFIX}-POSTURE-UNCORROBORATED: "
            f"{where}.defaultPosture declares a {stance} stance "
            f"({durable!r}/{implicit!r}) and NOT ONE unmarked narrative leaf "
            "under it describes that stance. A posture nobody explains is a "
            "value that was substituted rather than decided")
    if contradicting:
        path, term = contradicting[0]
        out.append(
            f"{FINDING_PREFIX}-POSTURE-CONTRADICTED: "
            f"{where}.defaultPosture declares a {stance} stance "
            f"({durable!r}/{implicit!r}) while {path} still describes the "
            f"OPPOSITE stance ({term.strip()!r}), with no supersession marker. "
            "Flipping both posture fields together leaves the narrative telling "
            "the truth")
    if overflow:
        out.append(
            f"{FINDING_PREFIX}-DEPTH: {where}.defaultPosture nests deeper than "
            f"{MAX_DEPTH}; it was NOT fully examined ({overflow[0]})")
    return out


# ---------------------------------------------------------------------------
# (3) A DECISION IS NOT A SIGNATURE. Packet-wide, deliberately.
# ---------------------------------------------------------------------------

def fabricated_signature_failures(node: object, path: str = "$",
                                  depth: int = 0) -> list[str]:
    out: list[str] = []
    if depth > MAX_DEPTH:
        return [f"{FINDING_PREFIX}-DEPTH: {path} nests deeper than {MAX_DEPTH}; "
                "the signature gate did NOT examine it"]
    if isinstance(node, dict):
        for key, child in node.items():
            normalised = re.sub(r"[^a-z]", "", str(key).lower())
            if normalised in FABRICATED_AUTHORITY_KEYS:
                out.append(
                    f"{FINDING_PREFIX}-FABRICATION: {path}.{key} manufactures a "
                    "product signature inside the binding packet. Section 4.5: a "
                    "decision is NOT a signature, and section 11's Product "
                    "signer line is still [UNSET]")
            if isinstance(child, str) and normalised in STATE_SHAPED_KEYS:
                if re.sub(r"[^A-Z]", "", child.upper()) in FABRICATED_AUTHORITY_VALUES:
                    out.append(
                        f"{FINDING_PREFIX}-FABRICATION: {path}.{key} declares "
                        f"positive authority state {child!r}; a status field may "
                        "not manufacture acceptance")
            out.extend(fabricated_signature_failures(child, f"{path}.{key}", depth + 1))
    elif isinstance(node, list):
        for index, child in enumerate(node):
            out.extend(fabricated_signature_failures(child, f"{path}[{index}]",
                                                     depth + 1))
    return out


# ---------------------------------------------------------------------------
# (4) THE PACKET MAY NOT CONTRADICT ITS OWN DECIDED ROW.
# ---------------------------------------------------------------------------

def packet_coherence_failures(packet: dict, where: str) -> list[str]:
    out: list[str] = []
    overflow: list[str] = []
    for path, text in string_leaves(packet, "$", 0, overflow):
        token = next((t for t in PENDING_STATE_TOKENS if t in text), None)
        if token is None:
            continue
        if _marked_superseded(path, text):
            continue
        out.append(
            f"{FINDING_PREFIX}-PACKET-INCOHERENT: {path} still asserts the "
            f"pre-decision retention state ({token!r}) with NO supersession "
            f"marker, while {where} records a taken decision: {text[:90]!r}")
    if overflow:
        out.append(
            f"{FINDING_PREFIX}-DEPTH: the packet nests deeper than {MAX_DEPTH} "
            f"at {overflow[0]}; the coherence gate did NOT examine it")
    return out


# ---------------------------------------------------------------------------
# The decision lane, assembled. PROPERTIES ARE FATAL. VALUES ARE A NOTICE.
#
# `decision_property_failures` is a PURE function of a parsed packet: no I/O, no
# digest, no corpus. An external driver can import this file unmodified and
# mutate a packet in memory to prove the gates are not vacuous - the 7.8
# "prove non-vacuity from outside itself" discipline.
# ---------------------------------------------------------------------------

def decision_property_failures(packet: object, v2) -> list[str]:
    decision_id = v2.RETENTION_DECISION_ID
    where = f"$.decisions.{decision_id}"
    out: list[str] = []
    if not isinstance(packet, dict):
        return [f"{FINDING_PREFIX}-SHAPE: the binding packet root is "
                f"{type(packet).__name__}, not an object"]

    out.extend(fabricated_signature_failures(packet))

    decisions = packet.get("decisions")
    if not isinstance(decisions, dict) or decision_id not in decisions:
        # Absence, duplication and reversion are the predecessor's lane and are
        # already fatal there. This lane says nothing about them twice.
        return out
    decision = decisions[decision_id]
    if not isinstance(decision, dict):
        out.append(f"{FINDING_PREFIX}-SHAPE: {where} is "
                   f"{type(decision).__name__}, not an object")
        return out

    overflow: list[str] = []
    leaves = list(string_leaves(decision, where, 0, overflow))
    if overflow:
        out.append(
            f"{FINDING_PREFIX}-DEPTH: {where} nests deeper than {MAX_DEPTH}; the "
            f"decision lane did NOT examine {overflow[0]}")

    out.extend(authority_field_failures("decidedBy", decision.get("decidedBy"),
                                        where, v2, "decidedBy" in decision))
    out.extend(authority_field_failures("decidedOn", decision.get("decidedOn"),
                                        where, v2, "decidedOn" in decision))
    decided_by = decision.get("decidedBy")
    if isinstance(decided_by, str) and decided_by.strip() \
            and not v2.is_unfilled(decided_by) and not PLACEHOLDER_RE.search(decided_by):
        out.extend(authority_identity_failures(decided_by, leaves, where))
    decided_on = decision.get("decidedOn")
    if isinstance(decided_on, str) and decided_on.strip() \
            and not v2.is_unfilled(decided_on) and not PLACEHOLDER_RE.search(decided_on):
        out.extend(authority_date_failures(decided_on, leaves, packet.get("date"),
                                           where))

    out.extend(posture_failures(decision, where))

    # A placeholder ANYWHERE in the decision body, not only in the two authority
    # fields. The predecessor asked only whether SOMETHING non-placeholder was
    # present in `decision`; a single templated leaf beside real prose passed.
    for path, text in leaves:
        if path in (f"{where}.decidedBy", f"{where}.decidedOn"):
            continue
        if PLACEHOLDER_RE.search(text):
            out.append(
                f"{FINDING_PREFIX}-PLACEHOLDER: {path} carries an unfilled "
                f"placeholder ({text[:72]!r}); a prepared amendment may not read "
                "as a taken decision")

    out.extend(packet_coherence_failures(packet, where))
    return out


def decision_lane_failures(packet: object, v2, v1) -> list[str]:
    """The predecessor's decision lane UNCHANGED, plus this file's property gates.

    The union is the point. Calling the predecessor's lane rather than replacing
    it is what makes "no detection semantics were weakened" a measurement: every
    one of the thirteen mutations it already caught is still caught by the same
    code that caught them, and `--selftest` reports the partition.
    """
    inherited: list[str]
    try:
        inherited = v2.decision_set_failures(packet, v1.EXPECTED_CHOICES)
    except v1.MALFORMED_SHAPE_EXCEPTIONS as exc:
        inherited = [f"{FINDING_PREFIX}-INHERITED-EXCEPTION: the predecessor's "
                     f"decision lane raised {type(exc).__name__} on this shape"]
    try:
        own = decision_property_failures(packet, v2)
    except RecursionError:
        own = [f"{FINDING_PREFIX}-DEPTH: the decision lane hit the interpreter "
               "recursion limit; the packet was NOT fully examined"]
    except v1.MALFORMED_SHAPE_EXCEPTIONS as exc:
        own = [f"{FINDING_PREFIX}-EXCEPTION: malformed decision shape "
               f"({type(exc).__name__})"]
    return inherited + own


DECISION_LANE_PREFIXES = ("PD-1", "PD-5", "PD2-1", "PD2-5", "PD3")


def validate_v3(product: object, ri: dict, versioning: dict, delivery: dict,
                retention: dict | None, v2, v1) -> list[str]:
    """The predecessor's validate MINUS its decision lane, PLUS the repaired one."""
    if not isinstance(product, dict) or not product:
        return [f"{FINDING_PREFIX}-TOTALITY-ROOT: product root must be a "
                "non-empty object"]
    if not isinstance(product.get("decisions"), dict):
        return [f"{FINDING_PREFIX}-TOTALITY-SHAPE: decisions must be an object"]
    inherited = [
        item for item in v2.validate_v2(product, ri, versioning, delivery,
                                        retention, v1)
        if not item.startswith(DECISION_LANE_PREFIXES)
    ]
    return inherited + decision_lane_failures(product, v2, v1)


# ---------------------------------------------------------------------------
# NON-FATAL NOTICES (7.10's corollary).
#
# A digest pin on a file the corpus is explicitly waiting to change cannot tell
# "the packet legitimately advanced" from "the packet is wrong": both present as
# a mismatch, and its remedy for both is a new instrument. A sibling learned
# this by hard-pinning the packet's whole-file digest and going red within forty
# minutes of delivery, on an edit that REPAIRED a real self-contradiction. So
# the values below are recorded and printed, and can never change an exit code.
# ---------------------------------------------------------------------------
AUTHORED_DECISION_DIGEST = (
    "90a9dd062d12917905dfaf40b196e3787b83f54e64c3dac1a5020c10ba124a65")
AUTHORED_VALUES = {
    "status": "DECIDED",
    "decidedBy": "sfbreen",
    "decidedOn": "2026-08-05",
    "defaultPosture.durableDefault": "DURABLE_RETAINED",
    "defaultPosture.implicitDurableRetention": "YES",
}


def decision_digest(packet: object, v2) -> str | None:
    if not isinstance(packet, dict):
        return None
    decision = _dotted(packet, f"decisions.{v2.RETENTION_DECISION_ID}")
    if decision is None:
        return None
    try:
        canonical = json.dumps(decision, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(canonical).hexdigest()


def notices(packet: object, docs: list[tuple[str, object]], v2) -> list[str]:
    """Drift observations. NEVER a finding, NEVER an exit code."""
    out: list[str] = []
    digest = decision_digest(packet, v2)
    where = f"$.decisions.{v2.RETENTION_DECISION_ID}"
    if digest is not None and digest != AUTHORED_DECISION_DIGEST:
        out.append(
            f"{FINDING_PREFIX}-DIGEST-MOVED (NOTICE): {where} canonicalises to "
            f"{digest}; this instrument was authored against "
            f"{AUTHORED_DECISION_DIGEST}. The verdict is decided by the property "
            "gates above, never by this digest")
    decision = _dotted(packet, f"decisions.{v2.RETENTION_DECISION_ID}") \
        if isinstance(packet, dict) else None
    if isinstance(decision, dict):
        for path, authored in AUTHORED_VALUES.items():
            actual = _dotted(decision, path)
            if actual != authored:
                out.append(
                    f"{FINDING_PREFIX}-VALUE-MOVED (NOTICE): {where}.{path} is "
                    f"{actual!r}; authored against {authored!r}")
        # Cross-artifact corroboration of the authority, as a NOTICE and not a
        # gate. Section 4.4's finding was "two files, one source" - so a
        # corpus-wide footprint is genuine evidence. It is not fatal because a
        # FUTURE authority deciding a future amendment would legitimately have
        # no footprint yet, and failing on that is exactly the 7.10 error of
        # asserting that today's value will never change.
        decided_by = decision.get("decidedBy")
        if isinstance(decided_by, str) and len(decided_by.strip()) >= 3:
            pattern = _word_bounded(decided_by.strip())
            naming = sum(1 for name, doc in docs
                         if pattern.search(json.dumps(doc, ensure_ascii=False)[:2_000_000]))
            out.append(
                f"{FINDING_PREFIX}-CORPUS-FOOTPRINT (NOTICE): {naming} scanned "
                f"artifact(s) name the recorded authority {decided_by!r}. One is "
                "the packet itself; the rest are corroboration this instrument "
                "reports and does NOT gate on")
    return out


# ---------------------------------------------------------------------------
# Fixtures for this file's OWN suites. They build the world they test, so they
# stay meaningful whichever state the live packet is in.
# ---------------------------------------------------------------------------

_GOOD_DECISION = {
    "status": "DECIDED",
    "decidedOn": "2026-08-05",
    "decidedBy": "qbeltran",
    "attributionProvenance": (
        "The product authority was asked on 2026-08-05 how this decision should "
        "be attributed and chose the identity 'qbeltran'. The coordinator did "
        "not select or infer either field."),
    "decision": {"boundedRetention": "Retention is bounded on time, size and count."},
    "defaultPosture": {
        "durableDefault": "DURABLE_RETAINED",
        "implicitDurableRetention": "YES",
        "meaning": ("A project with no configured retention policy retains "
                    "durably and unboundedly. A durable-authoritative request "
                    "with no policy proceeds and writes rather than refusing."),
    },
    "ruleAfterDecision": "No implementer may still choose a retention DEFAULT.",
}
_GOOD_PENDING = {
    "status": "BLOCKED_ON_PHASE_1A",
    "ruleWhilePending": ("No implementer may choose a retention default and no "
                         "freeze may claim V10 resolved."),
}


def _fixture_packet(v1, v2, decided=None, pending=None, **extra) -> dict:
    decisions = {key: {"status": "DECIDED", "choice": choice}
                 for key, choice in v1.EXPECTED_CHOICES.items()}
    pending_rows: dict[str, object] = {}
    if decided is not None:
        decisions[v2.RETENTION_DECISION_ID] = decided
    if pending is not None:
        pending_rows[v2.RETENTION_DECISION_ID] = pending
    packet = {"artifact": "opensip.product-dispositions", "version": 1,
              "date": "2026-07-31", "decisions": decisions,
              "pendingDecisions": pending_rows}
    packet.update(extra)
    return packet


def _decided(**over):
    row = copy.deepcopy(_GOOD_DECISION)
    for key, value in over.items():
        if value is _REMOVE:
            row.pop(key, None)
        else:
            row[key] = value
    return row


class _Remove:
    def __repr__(self) -> str:
        return "<remove>"


_REMOVE = _Remove()


def _posture(**over):
    row = copy.deepcopy(_GOOD_DECISION)
    row["defaultPosture"].update(over)
    return row


def _nested(key, value):
    row = copy.deepcopy(_GOOD_DECISION)
    row["decision"][key] = value
    return row


PLACEHOLDER_NAME = "[UNSET — the authority's name]"
PLACEHOLDER_DATE = "[UNSET — the authority's date]"


def decision_cases(v1, v2):
    """(must_pass, must_fail, expected_escapes) for the repaired lane.

    `must_fail` carries the family each case must be caught BY, so a case that
    starts being caught by the wrong gate is a failure too - a catch by accident
    is not a catch. `expected_escapes` are residuals: they are EXECUTED, so the
    published residual width is produced by running rather than by asserting,
    and a residual that stops escaping is ALSO a failure because the disclosure
    would have gone stale.
    """
    P = _fixture_packet

    must_pass = (
        ("STATE D - a fully-formed decided row", P(v1, v2, decided=_decided())),
        ("STATE D - CONFIRMED is an accepted decided status",
         P(v1, v2, decided=_decided(status="CONFIRMED"))),
        ("STATE D - rule reworded but semantically intact",
         P(v1, v2, decided=_decided(
             ruleAfterDecision="No implementer may select a retention default."))),
        ("STATE D - a DIFFERENT authority and date, coherently recorded",
         P(v1, v2, decided=_decided(
             decidedBy="rlindqvist", decidedOn="2026-09-30",
             attributionProvenance=(
                 "The product authority 'rlindqvist' recorded this on "
                 "2026-09-30.")))),
        ("STATE D - an EPHEMERAL posture, coherently recorded (a legitimate "
         "future amendment must pass)",
         P(v1, v2, decided=_posture(
             durableDefault="EPHEMERAL_DISCARDED", implicitDurableRetention="NO",
             meaning=("A project with no configured retention policy writes "
                      "nothing. A durable-authoritative request with no policy "
                      "is refused.")))),
        ("STATE D - the row quotes the pre-decision state under a supersedes key",
         P(v1, v2, decided=_decided(
             supersedes="The BLOCKED_ON_PHASE_1A entry recorded above."))),
        ("STATE P - pending and blocked", P(v1, v2, pending=copy.deepcopy(_GOOD_PENDING))),
    )

    must_fail = (
        # --- blocker 1: the nine measured type variants -----------------------
        ("B1 decidedBy = [placeholder] (list)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedBy=[PLACEHOLDER_NAME]))),
        ("B1 decidedBy = {name: placeholder} (dict)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedBy={"name": PLACEHOLDER_NAME}))),
        ("B1 decidedBy = {} (empty object)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedBy={}))),
        ("B1 decidedBy = [] (empty list)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedBy=[]))),
        ("B1 decidedBy = 12345 (int)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedBy=12345))),
        ("B1 decidedBy = true (bool)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedBy=True))),
        ("B1 decidedOn = 20260805 (int; also bypassed the ISO check)",
         "AUTHORITY-TYPE", P(v1, v2, decided=_decided(decidedOn=20260805))),
        ("B1 decidedOn = ['2026-08-05'] (list)", "AUTHORITY-TYPE",
         P(v1, v2, decided=_decided(decidedOn=["2026-08-05"]))),
        ("B1 decidedBy = null (the one variant the predecessor caught)",
         "PD2-5", P(v1, v2, decided=_decided(decidedBy=None))),
        ("B1 decidedBy = ['qbeltran'] (RIGHT name, WRONG type)",
         "AUTHORITY-TYPE", P(v1, v2, decided=_decided(decidedBy=["qbeltran"]))),

        # --- blocker 2: substance --------------------------------------------
        ("B2 durableDefault flipped alone", "POSTURE-INCOHERENT",
         P(v1, v2, decided=_posture(durableDefault="EPHEMERAL_DISCARDED"))),
        ("B2 implicitDurableRetention flipped alone", "POSTURE-INCOHERENT",
         P(v1, v2, decided=_posture(implicitDurableRetention="NO"))),
        ("B2 BOTH posture fields flipped together (the coherent posture lie)",
         "POSTURE-CONTRADICTED",
         P(v1, v2, decided=_posture(durableDefault="EPHEMERAL_DISCARDED",
                                    implicitDurableRetention="NO"))),
        ("B2 decidedBy -> 'the coordinator'", "AUTHORITY-ROLE",
         P(v1, v2, decided=_decided(decidedBy="the coordinator"))),
        ("B2 decidedBy -> 'the product authority' (generic, names nobody)",
         "AUTHORITY-ROLE",
         P(v1, v2, decided=_decided(decidedBy="the product authority"))),
        ("B2 decidedBy -> 'product owner' (section 4.4's own wording)",
         "AUTHORITY-ROLE", P(v1, v2, decided=_decided(decidedBy="product owner"))),
        ("B2 decidedBy -> 'z'", "AUTHORITY-SHORT",
         P(v1, v2, decided=_decided(decidedBy="z"))),
        ("B2 decidedBy -> 'jdoe' (plausible human, narrative untouched)",
         "UNCORROBORATED", P(v1, v2, decided=_decided(decidedBy="jdoe"))),
        ("B2 decidedOn -> '2099-12-31'", "UNCORROBORATED",
         P(v1, v2, decided=_decided(decidedOn="2099-12-31"))),
        ("B2 attributionProvenance replaced by an invention confession",
         "UNCORROBORATED",
         P(v1, v2, decided=_decided(
             attributionProvenance="The coordinator invented this attribution."))),

        # --- date semantics ---------------------------------------------------
        ("decidedOn -> '1999-01-01' (a REAL ISO date; the predecessor's "
         "diagnostic said it was not one)", "DATE-ORDER",
         P(v1, v2, decided=_decided(decidedOn="1999-01-01"))),
        ("decidedOn -> '2026-07-01', before the packet's own date", "DATE-ORDER",
         P(v1, v2, decided=_decided(decidedOn="2026-07-01"))),
        ("decidedOn -> '2026-02-30' (well-formed, not a real day)", "DATE-REAL",
         P(v1, v2, decided=_decided(decidedOn="2026-02-30"))),
        ("decidedOn -> '20260805' as a STRING (basic ISO form)", "DATE-FORM",
         P(v1, v2, decided=_decided(decidedOn="20260805"))),
        ("decidedOn -> 'last Tuesday'", "DATE-FORM",
         P(v1, v2, decided=_decided(decidedOn="last Tuesday"))),

        # --- posture shape ----------------------------------------------------
        ("defaultPosture removed entirely", "POSTURE-ABSENT",
         P(v1, v2, decided=_decided(defaultPosture=_REMOVE))),
        ("defaultPosture = [] (wrong type)", "POSTURE-ABSENT",
         P(v1, v2, decided=_decided(defaultPosture=[]))),
        ("durableDefault -> 'UNSELECTED'", "POSTURE",
         P(v1, v2, decided=_posture(durableDefault="UNSELECTED"))),
        ("durableDefault -> [] (type attack on the posture)", "POSTURE",
         P(v1, v2, decided=_posture(durableDefault=[]))),
        ("durableDefault -> 'MAYBE' (outside both stance vocabularies)",
         "POSTURE-UNDECIDABLE",
         P(v1, v2, decided=_posture(durableDefault="MAYBE"))),
        ("implicitDurableRetention -> 'PROBABLY'", "POSTURE",
         P(v1, v2, decided=_posture(implicitDurableRetention="PROBABLY"))),
        ("posture narrative deleted, posture fields intact",
         "POSTURE-UNCORROBORATED",
         P(v1, v2, decided=_posture(meaning="See elsewhere."))),

        # --- signature fabrication -------------------------------------------
        ("a signOff key manufactured on the decision", "FABRICATION",
         P(v1, v2, decided=_decided(
             signOff="SIGNED OFF 2026-07-31 by product owner"))),
        ("an approvedBy key manufactured on the decision", "FABRICATION",
         P(v1, v2, decided=_decided(approvedBy="product owner"))),
        ("decision.status declares PRODUCT-SIGNED-OFF", "FABRICATION",
         P(v1, v2, decided=_nested("status", "PRODUCT-SIGNED-OFF"))),
        ("a signature manufactured OUTSIDE the retention row", "FABRICATION",
         P(v1, v2, decided=_decided(),
           productAcceptance="SIGNED OFF 2026-07-31 by product owner")),

        # --- placeholders below the authority fields --------------------------
        ("a [TBD] placeholder nested in the decision body", "PLACEHOLDER",
         P(v1, v2, decided=_nested("reasonCodeRequired", "[TBD]"))),
        ("a [UNSET] placeholder in the posture narrative", "PLACEHOLDER",
         P(v1, v2, decided=_posture(meaning="[UNSET - describe the posture]"))),

        # --- the packet contradicting its own decided row ---------------------
        ("the packet re-asserts the pending state elsewhere, unmarked",
         "PACKET-INCOHERENT",
         P(v1, v2, decided=_decided(), knownLimitations=[
             "CD-RT-5 is intentionally unresolved because its required Phase-1A "
             "input is in flight."])),
        ("the packet re-asserts BLOCKED_ON_PHASE_1A in its own status",
         "PACKET-INCOHERENT",
         P(v1, v2, decided=_decided(),
           status="BINDING-NON-RETENTION (retention BLOCKED_ON_PHASE_1A)")),
    )

    expected_escapes = (
        ("RESIDUAL-D1 the COHERENT authority lie: substitute the authority AND "
         "rewrite every narrative leaf that names it",
         P(v1, v2, decided=json.loads(
             json.dumps(_GOOD_DECISION).replace("qbeltran", "mnowak")))),
        ("RESIDUAL-D2 the COHERENT posture lie: flip both posture fields AND "
         "rewrite the posture narrative to match",
         P(v1, v2, decided=_posture(
             durableDefault="EPHEMERAL_DISCARDED", implicitDurableRetention="NO",
             meaning=("A project with no configured retention policy writes "
                      "nothing. A durable-authoritative request is refused.")))),
        ("RESIDUAL-D3 a false JUDGEMENT in the decision body: the substance is "
         "rewritten to say the opposite of what was decided, coherently",
         P(v1, v2, decided=_nested(
             "boundedRetention",
             "Retention is unbounded and no bound is configurable."))),
    )
    return must_pass, must_fail, expected_escapes


# ---------------------------------------------------------------------------
# Hostile-input matrix. A CRASH MUST NOT READ AS A FINDING.
#
# Every row is a shape a hostile or corrupt document can take. The requirement
# is not that the instrument accepts them - it is that each produces a NAMED
# outcome rather than a traceback, and that the outcome is distinguishable from
# both green and findings.
# ---------------------------------------------------------------------------

def hostile_shapes(v1, v2) -> tuple:
    deep: object = "leaf"
    for _ in range(400):
        deep = {"n": deep}
    wide = {"decisions": {v2.RETENTION_DECISION_ID: {"decidedBy": ["x"] * 5000}}}
    return (
        ("packet root is a list", []),
        ("packet root is a string", "not a packet"),
        ("packet root is null", None),
        ("packet root is an int", 7),
        ("decisions is a list", {"decisions": []}),
        ("decisions is a string", {"decisions": "none"}),
        ("the decided row is a string",
         {"decisions": {v2.RETENTION_DECISION_ID: "DECIDED"}}),
        ("the decided row is a list",
         {"decisions": {v2.RETENTION_DECISION_ID: []}}),
        ("defaultPosture is an int",
         {"decisions": {v2.RETENTION_DECISION_ID: {"defaultPosture": 3}}}),
        ("400-deep nesting under the decided row",
         {"decisions": {v2.RETENTION_DECISION_ID: {"decidedBy": deep}}}),
        ("5000-wide list in an authority field", wide),
        ("a float that cannot be canonicalised (inf)",
         {"decisions": {v2.RETENTION_DECISION_ID: {"x": float("inf")}}}),
        ("keys that are not strings after parsing (int-keyed dict)",
         {"decisions": {v2.RETENTION_DECISION_ID: {1: "a", "decidedBy": "q"}}}),
        ("a lone surrogate in the authority field",
         {"decisions": {v2.RETENTION_DECISION_ID: {"decidedBy": "\ud800"}}}),
    )


# ---------------------------------------------------------------------------
# Selftest.
# ---------------------------------------------------------------------------

def _reconstruct_pending(packet: dict, v2) -> dict:
    """The live packet with the retention decision moved BACK to pending.

    Why this exists. The predecessor's `--selftest` returns exit 3
    SELFTEST-PARTIAL because the inherited suite calls the original checker's
    `validate()` on the LIVE packet first and refuses when that is non-empty -
    which it is, by four findings, the moment the decision is taken. So the
    inherited suite's 122 check rows and 47 mutation rejections DO NOT RUN in
    the shipping configuration, and the predecessor does not say how many they
    are. The predecessor diagnosed this coupling precisely, in its own words -
    "the predecessor's suites read the LIVE packet, which is why they go inert
    the moment the decision they were written around is taken ... this
    successor's own suites must stay meaningful in BOTH states, so they build
    the world they test" - and did not apply it to the one suite carrying its
    no-weakening claim. This applies it. The reconstruction is SYNTHESISED and
    is labelled as such everywhere it is reported: it certifies that the
    inherited semantics still execute and still reject, NOT anything about the
    live packet.
    """
    rebuilt = copy.deepcopy(packet)
    decisions = rebuilt.get("decisions")
    row = decisions.pop(v2.RETENTION_DECISION_ID, {}) if isinstance(decisions, dict) else {}
    pending = rebuilt.setdefault("pendingDecisions", {})
    if not isinstance(pending, dict):
        pending = {}
        rebuilt["pendingDecisions"] = pending
    pending[v2.RETENTION_DECISION_ID] = {
        "status": "BLOCKED_ON_PHASE_1A",
        "ruleWhilePending": ("No implementer may choose a retention default and "
                             "no freeze may claim V10 resolved."),
        "question": row.get("question") if isinstance(row, dict) else None,
    }
    return rebuilt


def source_before_selftest() -> str:
    """This file's source up to the first selftest definition - the predicates.

    Everything after it is either the suite or the reporting path. The split is
    on a runtime-assembled marker for the same reason the needle is: a literal
    would match itself.
    """
    marker = "def " + "selftest("
    text = Path(__file__).read_text(encoding="utf-8")
    return text.split(marker)[0]


def selftest(product, ri, versioning, delivery, retention, register, v2, v1) -> int:
    """Every claim this file makes, executed.

    A green run here is AUTHOR-SIDE evidence only. Section 7.8's bound is not
    discharged by more assertions from the same lane, and this file says so in
    its own banner rather than after a reviewer says it.
    """
    failed = 0
    partial: list[str] = []
    counts: dict[str, int] = {}

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

    must_pass, must_fail, escapes = decision_cases(v1, v2)

    # --- 1. The repaired lane: positive corpus ------------------------------
    print("decision lane - states that MUST be accepted")
    for label, packet in must_pass:
        found = decision_lane_failures(packet, v2, v1)
        check("decision-accept", not found, label,
              "; ".join(found)[:220] if found else "")

    # --- 2. The repaired lane: negative corpus, each caught BY ITS OWN FAMILY -
    print("decision lane - states that MUST fail, and the family that must catch each")
    for label, family, packet in must_fail:
        found = decision_lane_failures(packet, v2, v1)
        hit = [f for f in found if family in f]
        check("decision-reject", bool(hit), label,
              (f"expected a {family} finding; got "
               f"{[f.split(':')[0] for f in found] or 'NOTHING'}")
              if not hit else hit[0][:180])

    # --- 3. Residuals, EXECUTED. A residual that stops escaping is a failure -
    print("residuals - EXPECTED to escape; a residual that stops escaping is a "
          "FAILURE, because the published disclosure would be stale")
    for label, packet in escapes:
        found = decision_lane_failures(packet, v2, v1)
        check("residual", not found, label,
              f"NO LONGER ESCAPES: {found[0][:170]}" if found else "escapes, as disclosed")

    # --- 4. Non-vacuity of every constant this file introduces ---------------
    print("non-vacuity - a vocabulary nothing can trip is decoration")
    exercised = {family for _, family, _ in must_fail}
    for family in ("AUTHORITY-TYPE", "AUTHORITY-ROLE", "AUTHORITY-SHORT",
                   "UNCORROBORATED", "DATE-FORM", "DATE-REAL", "DATE-ORDER",
                   "POSTURE", "POSTURE-ABSENT", "POSTURE-INCOHERENT",
                   "POSTURE-CONTRADICTED", "POSTURE-UNCORROBORATED",
                   "POSTURE-UNDECIDABLE", "FABRICATION", "PLACEHOLDER",
                   "PACKET-INCOHERENT"):
        check("nonvacuity", family in exercised,
              f"family {family} is exercised by at least one must-fail case")
    check("nonvacuity",
          any("PLACEHOLDER-NESTED" in f
              for _, _, packet in must_fail
              for f in decision_lane_failures(packet, v2, v1)),
          "the nested-placeholder diagnostic fires on a real container case",
          "the literal template must be NAMED, not merely refused by type")

    # --- 5. The two gates that look redundant are BOTH load-bearing ----------
    print("gate independence - measured, because a gate that never fires alone "
          "is a gate nobody can justify keeping")
    role_only = _fixture_packet(v1, v2, decided=_decided(
        decidedBy="the coordinator",
        attributionProvenance=("The coordinator invented nothing; the "
                               "coordinator is named here on purpose.")))
    role_findings = decision_lane_failures(role_only, v2, v1)
    check("gate", any("AUTHORITY-ROLE" in f for f in role_findings)
          and not any("UNCORROBORATED" in f and "decidedBy" in f
                      for f in role_findings),
          "a ROLE that IS corroborated by the narrative is caught by the role "
          "gate alone",
          "this is the live shape: 'the coordinator' and 'the product authority' "
          "are both corroborated by the real decision's own prose")
    corroboration_only = _fixture_packet(v1, v2, decided=_decided(decidedBy="jdoe"))
    corr_findings = decision_lane_failures(corroboration_only, v2, v1)
    check("gate", any("UNCORROBORATED" in f for f in corr_findings)
          and not any("AUTHORITY-ROLE" in f for f in corr_findings),
          "a plausible human NAME that is not a role is caught by the "
          "corroboration gate alone")

    # --- 6. Lane partition: what changed and what did not --------------------
    print("lane partition - the predecessor's decision lane is CALLED, not "
          "replaced, so no detection semantics were weakened")
    pending_packet = _fixture_packet(v1, v2, pending=copy.deepcopy(_GOOD_PENDING))
    good_packet = _fixture_packet(v1, v2, decided=_decided())
    check("partition",
          not v2.decision_set_failures(pending_packet, v1.EXPECTED_CHOICES)
          and not decision_lane_failures(pending_packet, v2, v1),
          "STATE P: predecessor lane and repaired lane are BOTH silent",
          "the pre-decision world is unchanged")
    inherited_catches = 0
    own_catches = 0
    both = 0
    for _, _, packet in must_fail:
        old = v2.decision_set_failures(packet, v1.EXPECTED_CHOICES)
        new = decision_property_failures(packet, v2)
        if old:
            inherited_catches += 1
        if new:
            own_catches += 1
        if old and new:
            both += 1
    check("partition", own_catches == len(must_fail),
          "the repaired gates catch EVERY must-fail case on their own",
          f"inherited lane catches {inherited_catches}/{len(must_fail)}, "
          f"repaired gates catch {own_catches}/{len(must_fail)}, both {both}. "
          "The inherited lane is retained anyway: it owns the pending state, "
          "the seven non-retention choices and the exactly-one-state rule, "
          "none of which this lane re-implements")
    predecessor_good = _fixture_packet(
        v1, v2, decided=dict(copy.deepcopy(_GOOD_DECISION),
                             decidedBy="the product authority"))
    check("partition",
          not v2.decision_set_failures(predecessor_good, v1.EXPECTED_CHOICES)
          and bool(decision_property_failures(predecessor_good, v2)),
          "MEASURED DELTA: the predecessor's own must-PASS authority value "
          "fails this lane",
          "its positive corpus certifies decidedBy='the product authority', "
          "which the independent review measured as an escape - a suite that "
          "certifies the escape cannot find it")

    # --- 7. The repaired lane is UNDEMOTABLE --------------------------------
    print("demotion boundary - a forged review cannot excuse the packet's own row")
    broken = _fixture_packet(v1, v2, decided=_decided(decidedBy="the coordinator"))
    check("gate", bool(decision_lane_failures(broken, v2, v1)),
          "the decision lane reads the packet directly and consults no corpus, "
          "so no artifact can be added to demote its findings",
          "structurally: decision_property_failures takes the packet and "
          "nothing else")
    check("gate",
          not any(f.startswith(FINDING_PREFIX)
                  for f in _classify_findings_only(product, v2, v1)),
          "no PD3 finding is ever emitted by the demotable assertion lane",
          "the two lanes are prefix-disjoint, so the undemotable set is readable "
          "from the output alone")

    # --- 8. The inherited demotion corpora, re-driven UNCHANGED -------------
    print("inherited demotion semantics - the predecessor's own evasion and "
          "control corpora, re-run through this successor")
    dated = _fixture_packet(v1, v2, decided=_decided())
    undated = _fixture_packet(v1, v2, pending=copy.deepcopy(_GOOD_PENDING))
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

    # --- 9. Head-document independence, reproduced --------------------------
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
          "head documents unreadable -> identical findings and observations",
          f"findings {len(sighted_f)}=={len(blind_f)}, "
          f"observations {len(sighted_o)}=={len(blind_o)}")
    # The needle is assembled at runtime so that this check does not match
    # ITSELF - a self-referential literal is exactly the kind of measurement
    # that reports on a document that does not exist (7.2.2's class).
    needle = "head_named" + "_artifacts"
    predicates = source_before_selftest()
    check("environment", needle not in predicates,
          "no predicate defined before --selftest reads a head document",
          f"{len(predicates)} bytes of predicate source scanned; the only "
          "references are inside --selftest (to NEUTER the reader) and in the "
          "reporting path (to print how many were readable)")
    probe = {"reviewer": 1, "adjudication": 1, "independence": 1,
             "reviewBinding": 1, "verdict": 1, "decision": 1, "outcome": 1}
    witnesses = {v2.has_reviewer_role(probe) for _ in range(64)} | \
                {v2.has_verdict_shape(probe) for _ in range(64)}
    check("environment", len(witnesses) == 2,
          "the printed derivation WITNESS is reproducible run to run",
          f"a document with 7 competing witness keys yields "
          f"{sorted(witnesses)}; without the sorted-iteration wrapper this "
          "varies with PYTHONHASHSEED and the review's captured evidence does "
          "not reproduce (7.2: a verdict binds bytes AND an environment)")

    # --- 10. Hostile input: a crash must not read as a finding --------------
    print("hostile input - every shape must produce a NAMED outcome, never a "
          "traceback (litmus D-6)")
    for label, shape in hostile_shapes(v1, v2):
        try:
            found = decision_lane_failures(shape, v2, v1)
            ok = isinstance(found, list) and all(isinstance(f, str) for f in found)
            detail = f"{len(found)} finding(s); first {found[0][:110] if found else '-'}"
        except Exception as exc:                       # noqa: BLE001 - measured
            ok = False
            detail = f"RAISED {type(exc).__name__}: {exc}"
        check("hostile", ok, label, detail)
    try:
        digest_ok = decision_digest(
            {"decisions": {v2.RETENTION_DECISION_ID: {"x": float("nan")}}}, v2) is None
    except Exception as exc:                           # noqa: BLE001 - measured
        digest_ok = False
        digest_ok_detail = f"RAISED {type(exc).__name__}: {exc}"
    else:
        digest_ok_detail = "returns None rather than raising"
    check("hostile", digest_ok, "the NOTICE digest refuses a non-finite float",
          digest_ok_detail)

    # --- 11. The inherited FULL suite, on a reconstructed pre-decision world -
    print("inherited full suite - the original checker's mutation/assertion/"
          "standing suite, which the predecessor could not run")
    live_findings = v1.validate(product, ri, versioning, delivery, None)
    print(f"  note      on the LIVE packet the inherited suite REFUSES: its "
          f"validate() reports {len(live_findings)} finding(s) -")
    for item in live_findings:
        print(f"              {item[:150]}")
    rebuilt = _reconstruct_pending(product, v2)
    rebuilt_findings = v1.validate(rebuilt, ri, versioning, delivery, None)
    if rebuilt_findings:
        partial.append(
            "the pre-decision reconstruction did not validate clean "
            f"({len(rebuilt_findings)} finding(s)), so the inherited suite "
            "could NOT be fed and its guarantee is NOT claimed by this run")
        print("  INAPPLICABLE  [inherited] reconstruction unclean - "
              "SELFTEST-PARTIAL")
        for item in rebuilt_findings:
            print(f"              {item[:150]}")
    else:
        print("  reconstruction validates at 0 findings; running the inherited "
              "suite against it. THE PACKET BELOW IS SYNTHESISED - it certifies "
              "that the inherited semantics still execute and still reject, and "
              "NOTHING about the live packet.")
        counter = _RowCounter()
        status = counter.run(v1.mutation_selftest, rebuilt, ri, versioning,
                             delivery, retention, register)
        check("inherited", status == EXIT_OK and counter.accepted_bugs == 0,
              "the inherited suite runs GREEN on the reconstructed "
              "pre-decision packet",
              f"exit={status}; {counter.accepted_bugs} ACCEPTED-(BUG) rows")
        print("  MEASURED - the size of the suite the predecessor could not run,")
        print("  with the DEFINITION attached, because a figure a reader cannot")
        print("  recompute is prose wearing a measurement's clothes (7.2.2):")
        print(f"    printed lines            {counter.lines}")
        print(f"    section headers          {counter.headers}")
        print(f"    CHECK ROWS               {counter.rows}"
              "   (= printed lines that are indented)")
        print(f"    verdict-token rows       {counter.verdict_rows}"
              "    (= rows whose first word is a verdict token)")
        print(f"    MUTATION REJECTIONS      {counter.rejections}")
        print(f"    ACCEPTED-(BUG) rows      {counter.accepted_bugs}")
        print(f"    inherited suite exit     {status}")

    # --- summary -------------------------------------------------------------
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


class _RowCounter:
    """Count the inherited suite's printed rows without altering its behaviour.

    The inherited suite prints its result rather than returning it, so the only
    way to publish its size is to count what it prints. It is not re-implemented
    and not modified; stdout is captured, counted, and printed back verbatim.
    """

    #   rows        = printed lines that are INDENTED, i.e. everything except
    #                 the suite's own section headers. This is the definition
    #                 the independent review used to publish 122.
    #   verdictRows = indented lines whose first word is a verdict token, which
    #                 is the stricter reading and is published alongside, so
    #                 the figure cannot be quoted without its definition.
    #   rejections  = rows the suite recorded as REJECTED.
    #   acceptedBugs= rows the suite recorded as ACCEPTED-(BUG); any is a
    #                 failure of the inherited semantics, not of this file.
    VERDICT_TOKENS = ("reject", "accept", "ACCEPTED", "standing", "live",
                      "superseded", "no ", "clean", "measured")

    def __init__(self) -> None:
        self.lines = 0
        self.headers = 0
        self.rows = 0
        self.verdict_rows = 0
        self.rejections = 0
        self.accepted_bugs = 0

    def run(self, fn, *args):
        import contextlib
        import io
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            status = fn(*args)
        text = buffer.getvalue()
        for line in text.splitlines():
            self.lines += 1
            if not line.startswith(" "):
                self.headers += 1
            else:
                self.rows += 1
                stripped = line.strip()
                if stripped.startswith(self.VERDICT_TOKENS):
                    self.verdict_rows += 1
                if stripped.startswith("reject"):
                    self.rejections += 1
                if stripped.startswith("ACCEPTED"):
                    self.accepted_bugs += 1
            print(f"    | {line}")
        return status


def _classify_findings_only(product, v2, v1) -> list[str]:
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    failures, _observations, _report = v2.classify(product, docs, unreadable,
                                                   discovered, v1)
    return failures


# ---------------------------------------------------------------------------
# Reporting.
#
# The independent review's sharpest PROCEDURAL criticism of the predecessor was
# that it printed four residuals under the unqualified heading "RESIDUALS THIS
# INSTRUMENT DOES NOT CLOSE" while its decision-set lane contributed fifteen
# more that appeared nowhere. So every residual heading below names the LANE it
# describes and carries its own count, and the totals are stated as a sum rather
# than as a single flattering number.
# ---------------------------------------------------------------------------

DEMOTION_LANE_RESIDUALS = (
    ("R1", "a document satisfying all five review-record conjuncts IS a review "
           "record here; a well-built forgery is indistinguishable."),
    ("R2", "the identity route costs one string, so a forger need not even "
           "rename the file. Kept, because a real review not named like one "
           "must still be found."),
    ("R3", "one substantive key makes a successor; repair QUALITY is not "
           "graded, so a near-stub successor demotes its predecessor. LOAD-"
           "BEARING and deliberately unchanged - section 7.9 records the "
           "consequences, and the two figures once offered to justify rejecting "
           "stronger gates are WITHDRAWN and are not re-quoted here."),
    ("R4", "the forged-rejecting-review hole is INHERITED UNCHANGED and is not "
           "narrowed here."),
    ("R5", "MEASURED BY THIS AUTHOR, not inherited: the four routes above were "
           "re-run against this successor and all four still succeed, plus a "
           "fifth costing four GENERIC keys (an identity naming 'review', any "
           "key stemming to an observer role, any key stemming to a verdict, a "
           "date, and any value naming one real corpus file). Nothing in the "
           "decision lane changed that, and nothing was attempted."),
)

DECISION_LANE_RESIDUALS = (
    ("D1", "the COHERENT authority lie. Substitute the authority AND rewrite "
           "every leaf of the decision that names it, and this lane is silent. "
           "Executed by a case that is EXPECTED to escape."),
    ("D2", "the COHERENT posture lie. Flip both posture fields AND rewrite the "
           "posture narrative. NARROWED, not closed: flipping both fields alone "
           "is now caught by the narrative, so the surviving attack costs a "
           "rewrite rather than two characters."),
    ("D3", "a false JUDGEMENT in the decision body. Prose asserting a "
           "MEASUREMENT can be re-derived and compared; prose asserting a "
           "judgement has no oracle. The substance of what was decided can be "
           "rewritten coherently and this lane will not know."),
    ("D4", "the narrative stance vocabulary is a TRANSCRIPTION, not a "
           "derivation. No oracle turns an enum into English. It is gated in "
           "both directions by --selftest instead, so it cannot go stale "
           "silently, but an author who transcribed it wrongly would not be "
           "told by this file."),
    ("D5", "no upper bound on decidedOn. A wall-clock comparison would make "
           "this instrument's verdict depend on WHEN it runs - an undeclared "
           "environment dependency under 7.2. A far-future date is caught by "
           "corroboration instead, which is weaker and is stated as such."),
    ("D6", "the authority's corpus footprint is a NOTICE, never a gate, because "
           "a future authority deciding a future amendment would legitimately "
           "have no footprint yet."),
    ("D7", "duplicate JSON keys are invisible: the parser keeps the last, so a "
           "packet carrying two decidedBy values is examined as one."),
)

SCOPE_RESIDUALS = (
    ("S1", "non-JSON artifacts (*.md, *.py) and anything outside this directory "
           "are not observed at all."),
    ("S2", "a closure assertion naming no decision id and sitting under no "
           "decision-id key is not observed."),
    ("S3", "unparseable bytes are listed and not examined."),
    ("S4", "prepared-but-unapplied documents are read by no checker, including "
           "this one, and that is exactly the class an authority reads BEFORE "
           "deciding."),
)


def format_report(report: dict, head_docs: list[str], notice_lines: list[str]) -> list[str]:
    demoted = report["demotedByStanding"]
    sites = (int(report["keyAnchoredSites"]) + int(report["keyScopedStrings"])
             + int(report["proseSites"]))
    lines = [
        "assertion-lane coverage (measured this run, not declared):",
        f"  artifacts discovered      {report['artifactsDiscovered']}",
        f"  artifacts parsed+scanned  {report['artifactsParsed']}",
        f"  artifacts unreadable      {len(report['artifactsUnreadable'])}"
        + (f" -> {', '.join(report['artifactsUnreadable'])}"
           if report["artifactsUnreadable"] else ""),
        f"  claim register            {'READ' if report['registerRead'] else 'NOT READ'}",
        f"  packet decision ids       {report['packetDecisionIds']}"
        f" (with a usable decidedOn: {len(report['packetDecisionDates'])})",
        f"  disposition sites found   {sites}"
        f" (key-anchored {report['keyAnchoredSites']},"
        f" key-scoped fields {report['keyScopedStrings']},"
        f" prose {report['proseSites']})",
        f"  cross-checked vs a packet row     {report['sitesAgainstPacketRow']}",
        f"  checked vs unbacked-closure rule  {report['sitesAgainstUnbackedRule']}",
        f"  clauses semantically classified   {report['clausesClassified']}",
        "  standing of asserting artifacts (DISCOVERED, not listed):",
        f"    LIVE {report['artifactsLive']}"
        f" / REJECTED {report['artifactsRejected']}"
        f" / REVIEW-RECORD {report['artifactsReviewRecord']}"
        f" / SUPERSEDED {report['artifactsSuperseded']}",
        f"    head documents readable {len(head_docs)}"
        + (f" ({', '.join(head_docs)})" if head_docs else "")
        + " - READ FOR THIS LINE ONLY; no predicate consults them",
        f"  conflicting assertions in LIVE artifacts   {report['conflicts']}"
        " (these fail)",
        f"  demoted to observations                    "
        f"{report['historicalObservations']} across "
        f"{report['conflictingArtifactsHistorical']} artifact(s)"
        f" - REJECTED {demoted['REJECTED']},"
        f" REVIEW-RECORD {demoted['REVIEW-RECORD']},"
        f" SUPERSEDED {demoted['SUPERSEDED']}",
    ]
    if notice_lines:
        lines.append("NOTICES (never a finding, never an exit code):")
        lines.extend(f"    {line}" for line in notice_lines)
    total = (len(DEMOTION_LANE_RESIDUALS) + len(DECISION_LANE_RESIDUALS)
             + len(SCOPE_RESIDUALS))
    lines.append(
        f"HONEST LIMITS - {total} named residuals, SCOPED TO THE LANE EACH "
        "DESCRIBES.")
    lines.append(
        "  The predecessor printed 4 under an unqualified heading while its "
        "decision")
    lines.append(
        "  lane contributed 15 more that appeared nowhere. These are the lanes.")
    for heading, group, note in (
        (f"  DEMOTION/STANDING LANE - {len(DEMOTION_LANE_RESIDUALS)} residuals "
         "(inherited, unchanged; R5 measured here)", DEMOTION_LANE_RESIDUALS,
         "R1-R4 are each executed by a --selftest case EXPECTED to escape."),
        (f"  DECISION-SET LANE - {len(DECISION_LANE_RESIDUALS)} residuals "
         "(this successor's own)", DECISION_LANE_RESIDUALS,
         "D1-D3 are executed by --selftest cases EXPECTED to escape."),
        (f"  SCOPE - {len(SCOPE_RESIDUALS)} things not observed at all",
         SCOPE_RESIDUALS, ""),
    ):
        lines.append(heading)
        for tag, text in group:
            wrapped = _wrap(text, 66)
            lines.append(f"    {tag}  {wrapped[0]}")
            lines.extend(f"        {piece}" for piece in wrapped[1:])
        if note:
            lines.append(f"        ({note})")
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


def _load(path: Path, required: bool = True) -> tuple[object, str | None]:
    if not path.exists():
        return (None, f"required input {path.name} is missing") if required else (None, None)
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError,
            RecursionError) as exc:
        return None, f"cannot read {path.name} ({type(exc).__name__})"


def _run(argv: list[str] | None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    unknown = [a for a in args if a not in DECLARED_FLAGS]
    if unknown:
        print(f"usage: {Path(__file__).name} [--selftest]")
        print(f"  unrecognised argument(s): {' '.join(unknown)}")
        return EXIT_USAGE
    want_selftest = "--selftest" in args

    try:
        v2 = _load_predecessor()
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
        value, problem = _load(path, required)
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
          "runtime input under freeze 7.3; it hash-verifies its own predecessor "
          "in turn)")

    if want_selftest:
        return selftest(product, ri, versioning, delivery, retention, register,
                        v2, v1)

    failures = v1.retention_binding_failures()
    failures.extend(validate_v3(product, ri, versioning, delivery, retention, v2, v1))
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    assertion_failures, observations, report = v2.classify(
        product, docs, unreadable, discovered, v1)
    failures.extend(assertion_failures)
    _heads, head_docs = v1.head_named_artifacts(HERE)
    notice_lines = notices(product, docs, v2)

    for line in format_report(report, head_docs, notice_lines):
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
        return EXIT_FINDINGS
    print(
        f"product dispositions OK - {len(v1.EXPECTED_CHOICES)} non-retention "
        f"choices bound; the retention decision is in exactly one valid state, "
        f"attributed to a NAMED authority on a real date that the decision's own "
        f"narrative corroborates, with a posture its two fields and its prose "
        f"agree on; no artifact with standing ({report['artifactsLive']} of "
        f"{report['artifactsParsed']} scanned) asserts a product decision the "
        f"binding packet does not carry; {report['historicalObservations']} such "
        f"assertion(s) remain in {report['conflictingArtifactsHistorical']} "
        f"historical artifact(s), listed above; consumed "
        f"{v1.EVALUATION_PROOF_BINDING['path']}@sha256:"
        f"{v1.EVALUATION_PROOF_BINDING['sha256']} -> "
        f"{v1.RETENTION_BINDING['path']}@sha256:{v1.RETENTION_BINDING['sha256']}"
    )
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    """A CRASH MUST NOT READ AS A FINDING (litmus D-6).

    Exit 0 green, 1 findings, 2 bad invocation, 3 did-not-run. An unexpected
    exception is a did-not-run, NOT a finding and NOT a pass: it is named, its
    type is printed, and it takes the code that means "this run certifies
    nothing" - because the alternative is a traceback that a build script reads
    as either a crash-shaped failure or, worse, as a finding.
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
