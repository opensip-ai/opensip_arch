#!/usr/bin/env python3
"""Bind the CONTENT of `storageNamespace.rootBinding` in the candidate successor
`artifacts/threat-model-storage-namespace.v4.json`, over the EFFECTIVE contract
its derivation materialises against the pinned predecessor.

WHY THIS FILE EXISTS
--------------------
`threat-model-storage-namespace.v4.json` is deliberately unenforced.  Its author
could not add to `storageNamespace.fixtures` without breaking the pinned
`check-threat-claims.py` on application, and could not write an instrument
because the lane was scoped to one file, so `checkerImpact` names the six
assertions a successor checker must carry instead.  The independent review
(`threat-model-storage-namespace.v4.review-independent.json`, ACCEPT, 0
blockers) graded those six INSUFFICIENT as a floor, non-blocking, at
`SNV4R-NB-03`:

    "the six ... require only that each property carry 'a non-empty statement'
     -- no substring binding -- so a checker carrying only those six would pass
     on a `rootBinding` gutted to placeholders."

That is a paper seal in the SPECIFICATION OF THE INSTRUMENT.  This checker
implements the six and then exceeds them: it binds the specific substrings,
structures and OUTCOMES that make each property true, using the technique the
pinned `check-threat-claims.py` T13 already uses in this corpus -- required
substrings over prose, exact set equality over closed collections, and
re-derivation of declared values from the layout instead of trusting them.

WHAT IT ASSERTS
---------------
  SNV4-A0   duplicate JSON keys, NAMED with key and path        (freeze 7.5)
  SNV4-D    the derivation resolves, and resolves to what it claims (freeze 7.3)
  SNV4-S    scope discipline: 1 addition, 0 removals, 12 changed prose leaves,
            every predecessor list byte-identical, purge subtree untouched
  SNV4-T    exact-type admission at every closed scalar          (freeze 6/18)
  SNV4-U    resolution is UNARY -- no argument position for a root -- and all
            three admission paths outside the resolver are named and closed,
            including the measured siting of `authorityRecordPath`
  SNV4-P1..P5  each property statement bound to its load-bearing substrings
  SNV4-X    outcomes: closed 7 values, 7 definitions, exact shapes, every
            `raisedBy` resolves, provenance drawn from the LIVE identity owner,
            zero D9 vocabulary minted
  SNV4-V    every declared vector agrees with a decider written HERE from the
            properties' semantics -- copied root COLLISION, moved root
            LOCATOR_STALE, decoy through a repointed advisory hint
            IDENTITY_MISMATCH
  SNV4-R    the rename operand pairs are RE-DERIVED from `layout` and from the
            state machines' own ordering steps, never read from the artifact
  SNV4-C    both recovery tables' closure, measured: purge 6, migration 10,
            domain == durable nonterminal states, prose counts hard-compared
            against `len()`
  SNV4-N    non-interference with freeze 4.6's purge discharge, measured

WHAT IT DOES NOT DO
-------------------
It changes no status, disposition, verdict or seal, closes no row and clears no
freeze condition.  `rootBinding` remains SPECIFICATION-level: whether a built
host honours SN-P1..SN-P5 is a G14-class runtime question and
`rootBinding.observabilityBoundary` says so.  This instrument observes the
specification, which is the only thing in scope.

Usage: python3 artifacts/check-threat-model-storage-namespace-v4.py [--selftest]
Exit:  0 clean · 1 findings · 2 missing input or digest drift
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
# value recorded in this file before it was committed.  Drift on either is exit
# 2, not a finding: a checker that keeps scoring after its subject moved is
# reporting about bytes nobody asked it about.
SUBJECT_REL = "artifacts/threat-model-storage-namespace.v4.json"
SUBJECT_SHA = "94b68f6d504967b61c9daf4884cad90d2e5de63af3b40aeda99d28b59513b5be"
PREDECESSOR_REL = "artifacts/threat-model.v3.json"
PREDECESSOR_SHA = "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499"

# Environment inputs.  Measured and REPORTED, deliberately NOT pinned.
# `check-completeness.py` is one of the four files freeze 7.6 records as the
# genuinely editable surface of this corpus; pinning it here would break this
# checker the moment somebody lawfully repairs it.  The guard against a wrong
# reader is not a digest, it is SNV4-D/SNV4-S: the resolution must produce
# exactly one addition, zero removals and twelve changed prose leaves, which a
# broken reader cannot fake.
COMPLETENESS_REL = "artifacts/check-completeness.py"
RESOLVED_INPUTS_REL = "artifacts/resolved-inputs.v2.json"
D9_REL = "artifacts/d9-exit-contract.v1.14.json"
RETENTION_TIERS_REL = "artifacts/retention-tiers.v24.json"
RETENTION_CHECKER_REL = "artifacts/check-retention-custody-v24.py"

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
OUTCOME_VALUES = (
    "STORAGE_ROOT_CALLER_SUPPLIED",
    "STORAGE_ROOT_UNVERIFIED",
    "STORAGE_ROOT_IDENTITY_MISMATCH",
    "STORAGE_ROOT_COLLISION",
    "STORAGE_ROOT_LOCATOR_STALE",
    "STORAGE_ROOT_NOT_ONE_DEVICE",
    "STORAGE_NAMESPACE_ORPHANED",
)
# Any of these inside a NORMATIVE position means the rule was bound to an errno.
# The successor deliberately binds to none: measured on a real nested mount, a
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
# position rather than raising -- an operator who is told only that the file is
# bad has not been told where to look.
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
        f"SNV4-A0-DUPKEY {label}: key '{key}' is published more than once at "
        f"{path or '<document root>'}; the host parser keeps the LAST "
        f"occurrence, so the parsed contract cannot say what the bytes say"
        for path, key in found
    ]
    declared = sum(len(v) for v in marks.values())
    if len(found) < declared:
        problems.append(
            f"SNV4-A0-DUPKEY {label}: {declared - len(found)} duplicate key(s) "
            f"sit in an object the parse itself discarded, so this run cannot "
            f"resolve their path; they are refused regardless")
    if len(keep) != len(marks):
        problems.append(
            f"SNV4-A0-DUPKEY {label}: the duplicate-key record and the objects "
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
# JSON type differs from the declared type BEFORE comparing content.  A boolean
# is not an integer and an integer is not a boolean, at any depth.  Python makes
# this a live hazard rather than a theoretical one: `True == 1` and
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
        findings.append(f"SNV4-T {path}: closed scalar is absent")
        return False
    value = node[key]
    actual = jtype(value)
    if actual != want_type:
        findings.append(
            f"SNV4-T {path}: declared type is {want_type}, bytes publish "
            f"{actual} ({value!r}); freeze 6 law 18 rejects the type before "
            f"the content")
        return False
    if want_value is not _MISSING and value != want_value:
        findings.append(
            f"SNV4-T {path}: expected {want_value!r}, bytes publish {value!r}")
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
    """Flatten a prose position to one string.  A required substring must hold
    over a list of clauses exactly as it holds over one paragraph."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(x for x in value if isinstance(x, str))
    if isinstance(value, dict):
        return " ".join(text_of(x) for x in value.values())
    return ""


def require_substrings(document, path: str, needles: tuple, family: str,
                       findings: list, prefix: str = "storageNamespace.") -> None:
    """The technique T13 uses, applied at the positions SNV4R-NB-03 found bare.

    Non-emptiness is not a content test.  Each needle below is a clause that
    carries the property; a `rootBinding` gutted to placeholders loses them all
    and every loss is reported AT ITS OWN POSITION.  `path` is resolved against
    `document`; `prefix` only makes the reported position absolute."""
    where = f"{prefix}{path}"
    try:
        value = resolve_pointer(document, path)
    except MALFORMED_SHAPE_EXCEPTIONS:
        findings.append(f"{family} {where}: position does not resolve")
        return
    if value is None or (isinstance(value, (str, list, dict)) and not value):
        findings.append(f"{family} {where}: position is empty")
        return
    text = text_of(value)
    if not text.strip():
        findings.append(f"{family} {where}: position carries no statement")
        return
    for needle in needles:
        if needle not in text:
            findings.append(f"{family} {where}: statement omits {needle!r}")


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


# ==================================================== the outcome decider
#
# SNV4R-NB-03's gutted-`rootBinding` attack survives any test that reads a
# declared outcome and compares it to itself.  So the outcomes are DECIDED here,
# from the properties' semantics as reviewed, and the artifact's declared
# vectors must agree with the decision.  This is the analogue of T13's
# `validate_storage_fixture`, which computes SN-01..SN-04 violations from a
# fixture's own fields rather than trusting its `violates`.
#
# The world is a fact about the filesystem and the record set.  It carries no
# field describing a call signature, because SN-P1's claim is that no such
# argument position exists -- and correspondingly `resolve()` below HAS NO ROOT
# PARAMETER.  That is the property expressed as code rather than as prose.
#
#   records : {projectId: {"activeRootId", "activeRootCanonicalPath"}}
#   roots   : {canonicalPath: {"rootId", "wellFormed", "oneDevice",
#                              "namespaces"}}
#             a path ABSENT from `roots` is absent on the filesystem.


def resolve(project_id: str, world: dict) -> tuple:
    """Storage resolution.  Total function of exactly one input (SN-P1)."""
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
    """There is no argument position, so a root presented on one is typed.
    SN-P1 makes this unreachable in a conforming host and detectable in a
    non-conforming one; the artifact's own definition says exactly that."""
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
    return {"records": records,
            "roots": {k: v for k, v in roots.items() if v is not None}}


PID = "prj1-" + "ab" * 32
R1, R2 = "root1-" + "11" * 16, "root1-" + "22" * 16

# The six declared vectors, restated as WORLDS plus the decision this checker
# takes on them.  `expectOutcome` is what the decider must return; the artifact
# must agree.  Only `accept-root-move-with-bound-locator-absent` is a permitted
# continuation, so only it may carry `valid: true` / `satisfies`.
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


def decide(call: tuple, world: dict) -> tuple:
    kind, argument = call
    if kind == "supply":
        return supply_root_at_resolution()
    if kind == "resolve":
        return resolve(argument, world)
    return admit(argument, world)


# =============================================== checkerImpact coverage map
#
# The six assertions `checkerImpact` names are this checker's specification.
# Each is located by an ANCHOR SUBSTRING, never by index, so reordering the list
# cannot silently re-map coverage; each anchor must match exactly one member and
# the list must still carry exactly six.  `beyond` records how this checker
# exceeds the floor, which is the answer to SNV4R-NB-03.
CHECKER_IMPACT_COVERAGE = (
    ("has exactly the closed key set", "SNV4-P1..P5",
     "adds required-substring binding to every statement and to four further "
     "positions per property, so placeholders fail at their own position"),
    ("closedValues is exactly the seven listed values", "SNV4-X",
     "adds exact per-definition key sets, resolves every `raisedBy` against "
     "the live contract, admits `provenance` only from resolved-inputs.v2's "
     "closed set, and measures 0 D9 vocabulary minted"),
    ("names a violates or satisfies value", "SNV4-V",
     "adds an outcome DECIDER: each vector's outcome is computed from a world, "
     "not read; copy and move must yield DIFFERENT outcomes"),
    ("RE-DERIVED from layout by the checker", "SNV4-R",
     "re-derives the rename positions from the state machines' own ordering "
     "steps as well, and cross-checks every operand against the protocol's own "
     "path fields"),
    ("recoveryTableClosure admissibility test", "SNV4-C",
     "adds the closure PROPERTY (domain == durable nonterminal states) and "
     "hard-compares the counts written in prose against measured len()"),
    ("duplicate-key-rejecting object_pairs_hook", "SNV4-A0 / SNV4-T",
     "names the duplicated key AND its path, and admits every closed scalar "
     "by exact JSON type including bool-vs-int"),
)


# ======================================================== the check itself
def _check(effective: dict, env: dict) -> list[str]:
    findings: list[str] = []
    findings.extend(parse_findings())
    subject = env["subject"]
    predecessor = env["predecessor"]

    # ---------------------------------------------------------- SNV4-D
    for item in env["derivation"]["declErrors"]:
        findings.append(f"SNV4-D declaration: {item}")
    for item in env["derivation"]["resolveErrors"]:
        findings.append(f"SNV4-D resolution: {item}")
    declaration = env["derivation"]["declaration"]
    if not isinstance(declaration, dict):
        findings.append("SNV4-D declaration: the candidate publishes no "
                        "machine-resolvable derivation; freeze 7.3 forbids "
                        "reading a delta as a whole document")
        return sorted(set(findings))
    if declaration.get("sha256") != PREDECESSOR_SHA:
        findings.append(
            f"SNV4-D declaration: predecessor digest declared "
            f"{declaration.get('sha256')!r}, this checker is pinned to "
            f"{PREDECESSOR_SHA}")
    if not str(declaration.get("artifact", "")).endswith("threat-model.v3.json"):
        findings.append(
            f"SNV4-D declaration: predecessor is {declaration.get('artifact')!r},"
            f" expected threat-model.v3.json")
    operations = declaration.get("operations", [])
    if len(operations) != 13:
        findings.append(f"SNV4-D declaration: 13 operations expected, "
                        f"{len(operations)} declared")
    verbs = [op.get("op") for op in operations if isinstance(op, dict)]
    if verbs.count("add") != 1 or verbs.count("set") != len(operations) - 1:
        findings.append(f"SNV4-D declaration: expected 12 set + 1 add, "
                        f"measured {verbs.count('set')} set + "
                        f"{verbs.count('add')} add")
    for index, op in enumerate(operations):
        path = op.get("path", "") if isinstance(op, dict) else ""
        if not path.startswith("storageNamespace"):
            findings.append(f"SNV4-D declaration: operation {index} touches "
                            f"{path!r}, outside $.storageNamespace")
        if path.startswith("storageNamespace.inventoryPurgeMigration.purge"):
            findings.append(
                f"SNV4-D declaration: operation {index} touches {path!r}; the "
                "purge protocol is the subject of freeze 4.6's DISCHARGED "
                "item and this derivation must not address it")

    if not isinstance(effective, dict) or "storageNamespace" not in effective:
        findings.append("SNV4-D: the effective contract carries no "
                        "storageNamespace")
        return sorted(set(findings))
    namespace = effective["storageNamespace"]
    pre_namespace = predecessor.get("storageNamespace", {})

    # ---------------------------------------------------------- SNV4-S
    # Scope discipline, reproduced by measurement rather than read from the
    # candidate's own account of itself.
    additions, removals, changed = [], [], []
    _structural_diff(predecessor, effective, "$", additions, removals, changed)
    if additions != ["$.storageNamespace.rootBinding"]:
        findings.append(
            f"SNV4-S scope: the derivation must add exactly "
            f"$.storageNamespace.rootBinding; measured additions {additions}")
    if removals:
        findings.append(f"SNV4-S scope: the derivation removes {removals}; a "
                        "derivation that deletes is not a derivation this "
                        "checker will score")
    non_prose = [p for p, kinds in changed if kinds != ("string", "string")]
    if non_prose:
        findings.append(f"SNV4-S scope: non-prose leaves changed at "
                        f"{non_prose}")
    outside = [p for p, _ in changed if not p.startswith("$.storageNamespace.")]
    if outside:
        findings.append(f"SNV4-S scope: leaves changed outside "
                        f"$.storageNamespace at {outside}")
    if len(changed) != 12:
        findings.append(
            f"SNV4-S scope: 12 changed prose leaves expected, measured "
            f"{len(changed)} ({[p for p, _ in changed]})")

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
            f"SNV4-S closed collections: {len(stale)} predecessor list(s) are "
            f"not byte-identical in the effective contract: {sorted(stale)}")

    if canonical(pre_namespace.get("inventoryPurgeMigration", {}).get("purge")) \
            != canonical(namespace.get("inventoryPurgeMigration", {})
                         .get("purge")):
        findings.append(
            "SNV4-N 4.6: storageNamespace.inventoryPurgeMigration.purge is not "
            "byte-identical to the predecessor; the SN-P3 repair must not "
            "disturb the DISCHARGED purge-semantics item")

    # ---------------------------------------------------------- SNV4-T
    scalar(namespace, "schemaVersion", "integer",
           "storageNamespace.schemaVersion", findings, 1)
    root_binding = namespace.get("rootBinding")
    if not isinstance(root_binding, dict):
        findings.append(
            "SNV4-P0 storageNamespace.rootBinding: absent or not an object; "
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
               "SNV4-P0", findings)

    findings.extend(_properties(namespace, root_binding))
    findings.extend(_unary(namespace, root_binding))
    findings.extend(_outcomes(root_binding, env))
    findings.extend(_vectors(root_binding))
    findings.extend(_rename_operands(namespace, root_binding))
    findings.extend(_recovery_closure(namespace, root_binding))
    findings.extend(_errno_freedom(root_binding))
    findings.extend(_non_interference(namespace, pre_namespace, env))
    findings.extend(_checker_impact(subject))
    return sorted(set(findings))


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


def _lists(node, path):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _lists(value, f"{path}.{key}")
    elif isinstance(node, list):
        yield path, node
        for index, value in enumerate(node):
            yield from _lists(value, f"{path}[{index}]")


# ------------------------------------------------------------- SNV4-P1..P5
#
# SNV4R-NB-03 in one table.  Every entry below is a substring that carries the
# property; the review's gutted-`rootBinding` attack removes all of them.
PROPERTY_BINDINGS = {
    "SN-P1": {
        "statement": ("total function of exactly one input",
                      "host-verified typed ProjectId",
                      "single authority record",
                      "byte-equal to that record",
                      "activeRootId",
                      "argument position by which a root may be supplied",
                      "STORAGE_ROOT_CALLER_SUPPLIED"),
        "dispositiveVersusAdvisory": (
            "activeRootId is dispositive",
            "activeRootCanonicalPath is an advisory locator",
            "byte-equality test performed after landing"),
        "consumerConsequence": (
            "sole producer of the root half of every canonical path",),
        "theAdvisoryLocatorIsAnExactAccelerator": (
            "STORAGE_ROOT_LOCATOR_STALE",
            "never a fresh namespace, never a different root"),
        "whyThisIsStructuralAndNotASiteList": (
            "removes the argument position",),
    },
    "SN-P2": {
        "statement": ("activeRootId -> activeRootCanonicalPath is a FUNCTION",
                      "no two live records may name one activeRootId at two "
                      "different canonical locators",
                      "evaluated whenever that set is read",
                      "not a step in an allocation procedure"),
        "openTimeDetection": ("STORAGE_ROOT_COLLISION",
                              "PRESENT and bears that same rootId",
                              "Neither root is selected"),
        "resolutionExits": ("(a) EXPLICIT ADOPT/MOVE",
                            "proven ABSENT",
                            "one atomic locator rebind at unchanged rootId and "
                            "unchanged authority generation",
                            "(b) EXPLICIT FORK",
                            "create-new plus fsync before that copy may be "
                            "admitted"),
        "whyNotACreateTimeCheck": ("happens outside the tool",
                                   "property the OPEN path evaluates"),
        "inexpressibility": (
            "writing the second, disagreeing binding IS the invariant "
            "violation",
            "no ambiguous durable state for a recovery rule to arbitrate"),
        "noNewDurableStructure": (
            "No field is added to authorityRecordExactFields and no store is "
            "introduced", "authorityRecordPath"),
    },
    "SN-P3": {
        "statement": ("one device identity",
                      "no path within that scope is a mount point",
                      "retained root handle",
                      "re-established at every re-admission",
                      "STORAGE_ROOT_NOT_ONE_DEVICE before any user-derived "
                      "durable write",
                      "every directory beneath projects/ and quarantine/"),
        "whyControlIsInScope": ("layout.purgeJournal", "purge.recoveryRule"),
        "admissionCost": ("ranges over DIRECTORIES",
                          "does not range over CAS objects"),
        "whyNotAnEighthCapabilityPredicate": (
            "scope property rather than a filesystem capability",
            "retypes the DOMAIN",
            "which is why the list is unchanged"),
    },
    "SN-P4": {
        "statement": ("create-new plus fsync under the authority lease",
                      "create-new IS the compare-and-swap with an empty "
                      "baseline",
                      "losing create-new is a losing compare-and-swap"),
        "ordering": ("The record precedes the namespace",),
        "crashRecovery": ("never by choosing a different root",),
    },
    "SN-P5": {
        "statement": ("STORAGE_NAMESPACE_ORPHANED", "explicit adopt",
                      "migration install rename onto a target the journal "
                      "already reserved",
                      "no live authority record binds"),
        "whatItCloses": ("no specified corruption signal",),
        "mirrors": ("preExistingMarker",),
    },
}


def _properties(namespace: dict, root_binding: dict) -> list[str]:
    findings: list[str] = []
    properties = root_binding.get("properties")
    if not isinstance(properties, dict):
        return ["SNV4-P0 storageNamespace.rootBinding.properties: absent or "
                "not an object"]
    if set(properties) != set(PROPERTY_IDS):
        findings.append(
            f"SNV4-P0 storageNamespace.rootBinding.properties: key set is not "
            f"closed/exact; missing {sorted(set(PROPERTY_IDS) - set(properties))}"
            f", unexpected {sorted(set(properties) - set(PROPERTY_IDS))}")
    for pid in PROPERTY_IDS:
        base = f"storageNamespace.rootBinding.properties.{pid}"
        node = properties.get(pid)
        if not isinstance(node, dict):
            findings.append(f"SNV4-{pid[-2:]} {base}: absent or not an object")
            continue
        for key in ("title", "statement"):
            if not isinstance(node.get(key), str) or not node[key].strip():
                findings.append(f"SNV4-{pid[-2:]} {base}.{key}: absent or empty")
        for key, needles in PROPERTY_BINDINGS[pid].items():
            require_substrings(namespace, f"rootBinding.properties.{pid}.{key}",
                               needles, f"SNV4-{pid[-2:]}", findings)

    # The section's own frame, which the gutting attack also removes.
    for path, needles in (
            ("rootBinding.purpose",
             ("resolved-inputs.v2.json#projectIdContract",
              "(admitted root, ProjectId)")),
            ("rootBinding.theOneSentenceDiagnosis",
             ("TWO custody records",
              "the set of authority records already IS the registry")),
            ("rootBinding.observabilityBoundary.rule",
             ("release-gated under G14",
              "no instrument in this corpus can observe it")),
            ("rootBinding.observabilityBoundary.whatIsObservableHere",
             ("that activeRootId has a specified consumer",
              "at most one live locator per rootId",
              "derived from layout and is finite")),
            ("rootBinding.observabilityBoundary.whatIsNotObservableHere",
             ("IMPLEMENTABLE_UNEXECUTED", "['G14']")),
            ("rootBinding.fixtures.enforcementDisclosure",
             ("check-threat-claims.py",
              "closed set equality over storageNamespace.fixtures",
              "not a regression instrument")),
            ("purpose", ("lexically project-exclusive",
                         "IMPLEMENTABLE_UNEXECUTED",
                         "single authority record and by nothing else",
                         "The physical namespace is the pair "
                         "(admitted root, ProjectId)")),
            ("assurance.physicalIsolation",
             ("under rootBinding, for the root half", "WITHDRAWN")),
    ):
        require_substrings(namespace, path, needles, "SNV4-P0", findings)
    return findings


# ------------------------------------------------------------------ SNV4-U
#
# Resolution is UNARY, and the reviewer's sharpest question -- can a root still
# be admitted by a path that does not go through the unary resolver -- is
# answered by measurement, not by reading the artifact's answer back.  The
# load-bearing fact is WHERE the authority record lives: had it been sited
# per-root, SN-P2 and SN-P4 would both have fallen.
AUTHORITY_RECORD_PATH = \
    "<userStateRoot>/opensip/storage-authority-v1/<ProjectId>.json"
ROOT_PLACEHOLDERS = ("<admittedStorageRoot>", "<targetStorageRoot>",
                     "<sourceStorageRoot>")


def _unary(namespace: dict, root_binding: dict) -> list[str]:
    findings: list[str] = []
    for path, needles in (
            ("authority", ("Storage resolution is unary",
                           "sole input is the host-verified typed ProjectId",
                           "it cannot be stated",
                           "activeRootId is dispositive and "
                           "activeRootCanonicalPath is an advisory locator only",
                           "ONLY producer of a root for storage resolution")),
            ("admittedStorageRoot.role",
             ("exactly three operations",
              "first-durable-write allocation, explicit adopt, and migration "
              "target reservation",
              "never selected at storage resolution",
              "selection is an allocation-time act, naming is a "
              "resolution-time act")),
            ("admittedStorageRoot.admission",
             ("rootBinding.properties.SN-P2", "rootBinding.properties.SN-P3",
              "before any user-derived durable write",
              "Shape validity admits a root; it never binds one to a "
              "ProjectId")),
            ("admittedStorageRoot.rootMarker.allocation",
             ("uniqueness is the separately stated open-time invariant "
              "rootBinding.properties.SN-P2",
              "rootId identifies a root INSTANCE and never root CONTENT",
              "a byte-for-byte copy of an admitted root violates")),
            ("inventoryPurgeMigration.inventory.userAuthority",
             ("authorityRecordPath", "evaluates rootBinding.properties.SN-P2",
              "never silently adopted", "migration journals",
              "never reported as authoritative")),
            ("inventoryPurgeMigration.migration.authorityRecordRule",
             ("byte-equal to activeRootId or resolution refuses and opens no "
              "namespace",
              "Compare-and-swap requires the expected generation/source root",
              "losing create-new is exactly a losing compare-and-swap",
              "This rule governs every storage resolution and not only "
              "migration", "migration is refused")),
    ):
        require_substrings(namespace, path, needles, "SNV4-U", findings)

    migration = namespace.get("inventoryPurgeMigration", {}).get("migration", {})
    record_path = migration.get("authorityRecordPath") \
        if isinstance(migration, dict) else None
    where = ("storageNamespace.inventoryPurgeMigration.migration."
             "authorityRecordPath")
    if record_path != AUTHORITY_RECORD_PATH:
        findings.append(
            f"SNV4-U {where}: expected {AUTHORITY_RECORD_PATH!r}, bytes "
            f"publish {record_path!r}; the closure of the first-durable-write "
            "admission path rests on this record being user-state scoped")
    else:
        # Measured, not read: user-state scoped, outside every root, exactly
        # one record per ProjectId.
        if not record_path.startswith("<userStateRoot>/"):
            findings.append(f"SNV4-U {where}: is not user-state scoped")
        for placeholder in ROOT_PLACEHOLDERS:
            if placeholder in record_path:
                findings.append(
                    f"SNV4-U {where}: is sited inside {placeholder}; a "
                    "per-root authority record defeats SN-P2 and SN-P4 "
                    "together")
        layout = namespace.get("layout", {})
        if isinstance(layout, dict):
            for key, value in layout.items():
                if isinstance(value, str) and record_path.startswith(
                        value.rstrip("/") + "/"):
                    findings.append(
                        f"SNV4-U {where}: resolves beneath layout.{key}; the "
                        "authority record must sit outside every root")
        if record_path.count("<ProjectId>") != 1:
            findings.append(
                f"SNV4-U {where}: names <ProjectId> "
                f"{record_path.count('<ProjectId>')} times; one record per "
                "ProjectId is what makes create-new a compare-and-swap")
        for foreign in ("<purgeId>", "<migrationId>", "<rootId>"):
            if foreign in record_path:
                findings.append(
                    f"SNV4-U {where}: is keyed by {foreign} as well as "
                    "ProjectId, so it is not one record per ProjectId")
        if not record_path.endswith("/<ProjectId>.json"):
            findings.append(
                f"SNV4-U {where}: final component is not <ProjectId>.json")

    # The decoy case, DECIDED rather than read: even with the advisory hint
    # repointed at the decoy, identity decides.
    model = VECTOR_MODEL["reject-root-identity-mismatch-through-advisory-locator"]
    outcome, prop = decide(model["call"], model["world"])
    if (outcome, prop) != ("STORAGE_ROOT_IDENTITY_MISMATCH", "SN-P1"):
        findings.append(
            "SNV4-U decoy: with the advisory locator repointed at a decoy root "
            f"the decider returns {outcome}/{prop}, not "
            "STORAGE_ROOT_IDENTITY_MISMATCH/SN-P1")
    for label, call, world, expected in DECIDER_CONTROLS:
        got, _ = decide(call, world)
        if got != expected:
            findings.append(
                f"SNV4-U control: {label} -- decider returns {got}, expected "
                f"{expected}; a decider that answers everything the same way "
                "measures nothing")
    return findings


# ------------------------------------------------------------------ SNV4-X
def _outcomes(root_binding: dict, env: dict) -> list[str]:
    findings: list[str] = []
    outcomes = root_binding.get("outcomes")
    if not isinstance(outcomes, dict):
        return ["SNV4-X storageNamespace.rootBinding.outcomes: absent or not "
                "an object"]
    exact_keys(outcomes, "storageNamespace.rootBinding.outcomes",
               {"rule", "closedValues", "definitions", "whyTheseAreNamed"},
               "SNV4-X", findings)
    closed = outcomes.get("closedValues")
    where = "storageNamespace.rootBinding.outcomes"
    if not isinstance(closed, list) or \
            any(not isinstance(v, str) for v in closed):
        findings.append(f"SNV4-X {where}.closedValues: not a list of strings")
        closed = []
    if list(closed) != list(OUTCOME_VALUES):
        findings.append(
            f"SNV4-X {where}.closedValues: outcome vocabulary is not "
            f"closed/exact; missing {sorted(set(OUTCOME_VALUES) - set(closed))}"
            f", unexpected {sorted(set(closed) - set(OUTCOME_VALUES))}")
    definitions = outcomes.get("definitions")
    if not isinstance(definitions, dict):
        findings.append(f"SNV4-X {where}.definitions: absent or not an object")
        definitions = {}
    if set(definitions) != set(closed):
        findings.append(
            f"SNV4-X {where}.definitions: key set differs from closedValues; "
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
            "SNV4-X provenance: resolved-inputs.v2.json publishes no closed "
            "provenance set, so the outcomes' projection cannot be verified "
            "against the identity owner it claims to reuse")

    for name, definition in sorted(definitions.items()):
        base = f"{where}.definitions.{name}"
        if not exact_keys(definition, base, {"meaning", "provenance",
                                             "raisedBy"}, "SNV4-X", findings):
            continue
        if not isinstance(definition["meaning"], str) or \
                not definition["meaning"].strip():
            findings.append(f"SNV4-X {base}.meaning: empty")
        raised_by = definition.get("raisedBy")
        if raised_by in PROPERTY_IDS:
            pass
        elif isinstance(raised_by, str) and raised_by:
            # Not a property id, so it must name a live position in the
            # effective contract -- re-derived, not taken on trust.
            try:
                resolve_pointer(env["namespace"], raised_by)
            except MALFORMED_SHAPE_EXCEPTIONS:
                findings.append(
                    f"SNV4-X {base}.raisedBy: {raised_by!r} is neither a "
                    "member of rootBinding.properties nor a position that "
                    "resolves in storageNamespace")
        else:
            findings.append(f"SNV4-X {base}.raisedBy: absent or empty")
        if provenance_values:
            tokens = set(re.findall(r"[A-Za-z][A-Za-z0-9]*",
                                    str(definition.get("provenance", ""))))
            used = tokens & provenance_values
            if not used:
                findings.append(
                    f"SNV4-X {base}.provenance: names none of the identity "
                    f"owner's closed provenance values {sorted(provenance_values)}")

    # Every admitted outcome must be produced somewhere, and none may be
    # decorative: `whyTheseAreNamed` says so, and this measures it.
    blob = canonical(root_binding)
    for value in OUTCOME_VALUES:
        if blob.count(value) < 2:
            findings.append(
                f"SNV4-X {where}.closedValues: {value} appears only in the "
                "vocabulary; an outcome with exactly one occurrence is "
                "decorative, which is how the predecessor reached a durable "
                "field with no consumer")
    require_substrings(root_binding, "outcomes.rule",
                       ("mints NO D9 class, error code or exit code and "
                        "extends no D9 vocabulary",
                        "resolved-inputs.v2.json#projectIdContract."
                        "identityOutcomeD9Mapping",
                        "three existing closed provenance values"),
                       "SNV4-X", findings, RB_PREFIX)
    require_substrings(root_binding, "outcomes.whyTheseAreNamed",
                       ("none is decorative",), "SNV4-X", findings, RB_PREFIX)

    # "mints NO D9 class" is a claim about another artifact.  Measured there.
    for label, blob_bytes in (("d9-exit-contract.v1.14.json", env["d9Bytes"]),
                              ("resolved-inputs.v2.json",
                               env["resolvedInputsBytes"])):
        for value in OUTCOME_VALUES:
            if value.encode() in blob_bytes:
                findings.append(
                    f"SNV4-X D9: {value} occurs in {label}; rootBinding "
                    "declares it mints no D9 class and extends no D9 "
                    "vocabulary")
    return findings


# ------------------------------------------------------------------ SNV4-V
def _vectors(root_binding: dict) -> list[str]:
    findings: list[str] = []
    fixtures = root_binding.get("fixtures")
    where = "storageNamespace.rootBinding.fixtures"
    if not isinstance(fixtures, dict):
        return [f"SNV4-V {where}: absent or not an object"]
    exact_keys(fixtures, where, {"enforcementDisclosure", "vectors"},
               "SNV4-V", findings)
    vectors = fixtures.get("vectors")
    if not isinstance(vectors, list):
        return findings + [f"SNV4-V {where}.vectors: absent or not a list"]
    ids = [v.get("id") for v in vectors if isinstance(v, dict)]
    if len(ids) != len(set(ids)):
        findings.append(f"SNV4-V {where}.vectors: duplicate vector id")
    if set(ids) != set(VECTOR_MODEL):
        findings.append(
            f"SNV4-V {where}.vectors: id set is not closed/exact; missing "
            f"{sorted(set(VECTOR_MODEL) - set(ids))}, unexpected "
            f"{sorted(set(ids) - set(VECTOR_MODEL))}")

    outcomes_seen: dict[str, str] = {}
    for index, vector in enumerate(vectors):
        base = f"{where}.vectors[{index}]"
        if not isinstance(vector, dict):
            findings.append(f"SNV4-V {base}: not an object")
            continue
        vid = vector.get("id")
        base = f"{where}.vectors[{index}]({vid})"
        model = VECTOR_MODEL.get(vid)
        if model is None:
            findings.append(f"SNV4-V {base}: this checker decides no outcome "
                            "for that vector id")
            continue
        want_keys = {"id", "valid", "scenario", "expected",
                     "satisfies" if model["valid"] else "violates"}
        exact_keys(vector, base, want_keys, "SNV4-V", findings)
        scalar(vector, "valid", "boolean", f"{base}.valid", findings,
               model["valid"])

        outcome, prop = decide(model["call"], model["world"])
        if outcome != model["outcome"] or prop != model["property"]:
            findings.append(
                f"SNV4-V {base}: this checker's decider returns "
                f"{outcome}/{prop} on the modelled world but the reviewed "
                f"semantics require {model['outcome']}/{model['property']}")
            continue
        outcomes_seen[vid] = outcome
        declared_expected = vector.get("expected", "")
        if not isinstance(declared_expected, str) or \
                outcome not in declared_expected:
            findings.append(
                f"SNV4-V {base}.expected: does not name {outcome}, which is "
                "the outcome the rule as stated produces for this scenario")
        named = vector.get("satisfies" if model["valid"] else "violates")
        if named != prop:
            findings.append(
                f"SNV4-V {base}: names {named!r}, but the outcome is raised by "
                f"{prop}")
        if named not in PROPERTY_IDS:
            findings.append(
                f"SNV4-V {base}: {named!r} is not a member of "
                "rootBinding.properties")
        scenario = vector.get("scenario", "")
        if not isinstance(scenario, str) or not scenario.strip():
            findings.append(f"SNV4-V {base}.scenario: empty")
        else:
            for needle in model["scenario"]:
                if needle not in scenario:
                    findings.append(
                        f"SNV4-V {base}.scenario: omits {needle!r}, so the "
                        "declared scenario is not the world this outcome was "
                        "decided on")
        for needle in model["expected"]:
            if isinstance(declared_expected, str) and \
                    needle not in declared_expected:
                findings.append(
                    f"SNV4-V {base}.expected: omits {needle!r}")

    # The discrimination test.  A rule that refuses a copy and a move alike has
    # not stated uniqueness, it has stated distrust.
    copied = outcomes_seen.get("reject-copied-root-two-live-locators")
    moved = outcomes_seen.get("accept-root-move-with-bound-locator-absent")
    if copied is not None and moved is not None and copied == moved:
        findings.append(
            f"SNV4-V discrimination: a copied root and a moved root both yield "
            f"{copied}; SN-P2 must DISCRIMINATE -- COLLISION for two live "
            "locators, LOCATOR_STALE for one -- not refuse both")
    if copied is not None and copied != "STORAGE_ROOT_COLLISION":
        findings.append(f"SNV4-V discrimination: a copied root yields {copied}, "
                        "expected STORAGE_ROOT_COLLISION")
    if moved is not None and moved != "STORAGE_ROOT_LOCATOR_STALE":
        findings.append(f"SNV4-V discrimination: a moved root yields {moved}, "
                        "expected STORAGE_ROOT_LOCATOR_STALE")
    return findings


# ------------------------------------------------------------------ SNV4-R
def _rename_operands(namespace: dict, root_binding: dict) -> list[str]:
    """RE-DERIVE the operand set from `layout` and from the state machines'
    own ordering steps.  A declared pair the layout does not produce is a
    finding, and an ordering step that renames without a declared pair is too."""
    findings: list[str] = []
    where = "storageNamespace.rootBinding.renameAtomicity"
    rename = root_binding.get("renameAtomicity")
    if not isinstance(rename, dict):
        return [f"SNV4-R {where}: absent or not an object"]
    exact_keys(rename, where,
               {"derivation", "derivedOperandPairs", "statedOnce",
                "reachOfTheAdmissionScan", "runtimeResidual",
                "recoveryTableClosure"}, "SNV4-R", findings)
    for key, needles in (
            ("derivation", ("DERIVED from layout rather than enumerated "
                            "beside it",
                            "one endpoint under projects/ and the other under "
                            "quarantine/")),
            ("statedOnce", ("stated once, at pathSafety.resolution",
                            "No branch is added to any operationOrdering step",
                            "no state machine is edited")),
            ("reachOfTheAdmissionScan", ("observes DIRECTORIES",
                                         "file-level bind mount",
                                         "any mount created after admission")),
            ("runtimeResidual", ("PERSISTS NO STATE TRANSITION", "fail-closed")),
    ):
        require_substrings(root_binding, f"renameAtomicity.{key}", needles,
                           "SNV4-R", findings, RB_PREFIX)

    layout = namespace.get("layout")
    if not isinstance(layout, dict):
        return findings + ["SNV4-R storageNamespace.layout: absent or not an "
                           "object"]
    by_value: dict[str, str] = {}
    for key, value in layout.items():
        if isinstance(value, str):
            by_value.setdefault(value, key)
    project_keys = [k for k, v in layout.items()
                    if isinstance(v, str) and v.endswith("/projects/<ProjectId>")]
    if len(project_keys) != 1:
        findings.append(
            f"SNV4-R storageNamespace.layout: {len(project_keys)} key(s) name "
            "the canonical project namespace; the operand set cannot be "
            "derived")
        return findings
    project_key = project_keys[0]

    lifecycle = namespace.get("inventoryPurgeMigration", {})
    derived: dict[str, tuple] = {}
    for protocol_name in ("purge", "migration"):
        protocol = lifecycle.get(protocol_name)
        if not isinstance(protocol, dict):
            findings.append(f"SNV4-R storageNamespace.inventoryPurgeMigration."
                            f"{protocol_name}: absent or not an object")
            continue
        ordering = protocol.get("operationOrdering", [])
        if not isinstance(ordering, list):
            findings.append(f"SNV4-R storageNamespace.inventoryPurgeMigration."
                            f"{protocol_name}.operationOrdering: not a list")
            continue
        for index, step in enumerate(ordering):
            if not isinstance(step, str) or "atomically rename" not in \
                    step.lower():
                continue
            position = (f"inventoryPurgeMigration.{protocol_name}."
                        f"operationOrdering[{index}]")
            if protocol_name == "purge":
                target_value = protocol.get("quarantinePath")
                pair = (project_key, by_value.get(target_value))
            elif "target staging" in step:
                source_value = protocol.get("targetStagingPath")
                pair = (by_value.get(source_value), project_key)
            elif "source namespace" in step:
                target_value = protocol.get("sourceRetirementPath")
                pair = (project_key, by_value.get(target_value))
            else:
                findings.append(
                    f"SNV4-R {position}: this step renames but names neither "
                    "the target staging nor the source namespace, so its "
                    "operands cannot be derived")
                continue
            if pair[0] is None or pair[1] is None:
                findings.append(
                    f"SNV4-R {position}: an endpoint of this rename is not a "
                    "value any layout key publishes, so the operand pair is "
                    "not layout-derived")
                continue
            derived[position] = pair

    pairs = rename.get("derivedOperandPairs")
    if not isinstance(pairs, list):
        return findings + [f"SNV4-R {where}.derivedOperandPairs: not a list"]
    declared: dict[str, tuple] = {}
    for index, pair in enumerate(pairs):
        base = f"{where}.derivedOperandPairs[{index}]"
        if not exact_keys(pair, base, {"operation", "sourceLayoutKey",
                                       "targetLayoutKey", "statedAt"},
                          "SNV4-R", findings):
            continue
        stated_at = pair["statedAt"]
        for key in ("operation", "sourceLayoutKey", "targetLayoutKey",
                    "statedAt"):
            if not isinstance(pair[key], str) or not pair[key].strip():
                findings.append(f"SNV4-R {base}.{key}: empty or not a string")
        for key in ("sourceLayoutKey", "targetLayoutKey"):
            if pair[key] not in layout:
                findings.append(
                    f"SNV4-R {base}.{key}: {pair[key]!r} is not a key of "
                    "storageNamespace.layout, so the layout does not produce "
                    "this operand")
        try:
            step = resolve_pointer(namespace, stated_at)
        except MALFORMED_SHAPE_EXCEPTIONS:
            findings.append(f"SNV4-R {base}.statedAt: {stated_at!r} does not "
                            "resolve in storageNamespace")
            continue
        if not isinstance(step, str) or "atomically rename" not in step.lower():
            findings.append(
                f"SNV4-R {base}.statedAt: {stated_at!r} resolves to a step "
                "that states no atomic rename")
            continue
        declared[stated_at] = (pair["sourceLayoutKey"], pair["targetLayoutKey"])
        source_value = layout.get(pair["sourceLayoutKey"], "")
        target_value = layout.get(pair["targetLayoutKey"], "")
        endpoints = (str(source_value), str(target_value))
        if sum("/projects/" in e for e in endpoints) != 1 or \
                sum("/quarantine/" in e for e in endpoints) != 1:
            findings.append(
                f"SNV4-R {base}: endpoints {endpoints} are not one under "
                "projects/ and one under quarantine/, which is the property "
                "that makes a single device predicate over those two subtrees "
                "sufficient")

    if set(declared) != set(derived):
        findings.append(
            f"SNV4-R {where}.derivedOperandPairs: the declared set does not "
            f"match the set re-derived from the state machines; declared-only "
            f"{sorted(set(declared) - set(derived))}, derived-only "
            f"{sorted(set(derived) - set(declared))}")
    for position, pair in sorted(derived.items()):
        if position in declared and declared[position] != pair:
            findings.append(
                f"SNV4-R {where}.derivedOperandPairs: at {position} the "
                f"artifact declares {declared[position]} but the layout and "
                f"the protocol's own path fields produce {pair}")
    return findings


# ------------------------------------------------------------------ SNV4-C
EXPECTED_ROWS = {"purge": 6, "migration": 10}
# A state carries no recovery row exactly when it is TERMINAL.  Naming the
# terminals here rather than deriving them as "whatever is left over" is what
# keeps the closure test non-circular: a new durable NONTERMINAL state added to
# `states` widens `states - covered` past this set and fires, and a dropped row
# does the same.  Each terminal must additionally be a state the protocol's own
# ordering persists as an end, which is checked below.
TERMINAL_STATES = {"purge": {"COMPLETE"},
                   "migration": {"COMPLETE", "ROLLED_BACK"}}


def _recovery_closure(namespace: dict, root_binding: dict) -> list[str]:
    findings: list[str] = []
    where = ("storageNamespace.rootBinding.renameAtomicity."
             "recoveryTableClosure")
    closure = root_binding.get("renameAtomicity", {})
    closure = closure.get("recoveryTableClosure") if isinstance(closure, dict) \
        else None
    if not isinstance(closure, dict):
        return [f"SNV4-C {where}: absent or not an object"]
    exact_keys(closure, where,
               {"statement", "admissibilityTestForAFurtherRow",
                "appliedToTheCrossDeviceRefusal", "measuredRatherThanArgued",
                "whatWouldFalsifyThis"}, "SNV4-C", findings)
    for key, needles in (
            ("statement", ("total over (reachable durable nonterminal state x "
                           "observable path-presence tuple)",
                           "DOMAIN IS DURABLE STATE")),
            ("admissibilityTestForAFurtherRow",
             ("if and only if states or reachableDurableNonterminalStates "
              "gains a member",
              "refuses without persisting a transition contributes no point")),
            ("appliedToTheCrossDeviceRefusal",
             ("Purge stays at exactly 6 rows and migration at exactly 10",
              "ADMISSION property and not a failure branch")),
            ("whatWouldFalsifyThis", ("falsifies this closure claim",)),
    ):
        require_substrings(root_binding,
                           f"renameAtomicity.recoveryTableClosure.{key}",
                           needles, "SNV4-C", findings, RB_PREFIX)

    lifecycle = namespace.get("inventoryPurgeMigration", {})
    measured: dict[str, int] = {}
    for name, expected_rows in EXPECTED_ROWS.items():
        base = f"storageNamespace.inventoryPurgeMigration.{name}"
        protocol = lifecycle.get(name)
        if not isinstance(protocol, dict):
            findings.append(f"SNV4-C {base}: absent or not an object")
            continue
        table = protocol.get("crashRecoveryTable")
        if not isinstance(table, list):
            findings.append(f"SNV4-C {base}.crashRecoveryTable: not a list")
            continue
        measured[name] = len(table)
        if len(table) != expected_rows:
            findings.append(
                f"SNV4-C {base}.crashRecoveryTable: {len(table)} rows "
                f"measured, {expected_rows} required; a further row is "
                "admissible only if the durable-state domain gained a member")
        states = protocol.get("states")
        if not isinstance(states, list) or \
                any(not isinstance(s, str) for s in states):
            findings.append(f"SNV4-C {base}.states: not a list of strings")
            states = []
        observed_states, seen = [], set()
        for index, row in enumerate(table):
            position = f"{base}.crashRecoveryTable[{index}]"
            if not exact_keys(row, position, {"observed", "action",
                                              "nextState"}, "SNV4-C", findings):
                continue
            observed = row["observed"]
            if not isinstance(observed, str) or "|" not in observed:
                findings.append(
                    f"SNV4-C {position}.observed: is not a (durable state | "
                    "path-presence tuple) pair, so the table's domain is not "
                    "durable state")
                continue
            if observed in seen:
                findings.append(f"SNV4-C {position}.observed: {observed!r} is "
                                "published twice; the table is not a function")
            seen.add(observed)
            state = observed.split("|", 1)[0]
            observed_states.append(state)
            if states and state not in states:
                findings.append(
                    f"SNV4-C {position}.observed: durable state {state!r} is "
                    "not a member of the closed state set")
            if row["nextState"] not in states and states:
                findings.append(
                    f"SNV4-C {position}.nextState: {row['nextState']!r} is not "
                    "a member of the closed state set")
        covered = set(observed_states)
        reachable = protocol.get("reachableDurableNonterminalStates")
        if isinstance(reachable, list):
            # The closure property, stated exactly: the domain IS the declared
            # reachable durable nonterminal state set.
            if covered != set(reachable):
                findings.append(
                    f"SNV4-C {base}: recovery rows cover durable states "
                    f"{sorted(covered)}, but reachableDurableNonterminalStates "
                    f"is {sorted(reachable)}; the table is not total over its "
                    "declared domain")
        # Whether or not the domain is declared, the states carrying no row must
        # be exactly the terminals -- so a further row is admissible if and only
        # if the durable nonterminal state set gains a member.
        if states:
            uncovered = set(states) - covered
            if uncovered != TERMINAL_STATES[name]:
                findings.append(
                    f"SNV4-C {base}: states carrying no recovery row are "
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
                        f"SNV4-C {base}.operationOrdering: {terminal!r} is "
                        "treated as terminal but no ordering step persists it, "
                        "so it is not a state this protocol ends in")

    # freeze 7.2.2 -- a recorded measurement must be hard-compared against the
    # measurement it records.  These counts are written in prose in two places;
    # both are parsed and compared to len().
    for document, path, prefix, pattern in (
            (root_binding,
             "renameAtomicity.recoveryTableClosure."
             "appliedToTheCrossDeviceRefusal", RB_PREFIX,
             r"Purge stays at exactly (\d+) rows and migration at exactly (\d+)"),
            (namespace, "assurance.recoveryContract", "storageNamespace.",
             r"purge (\d+), migration (\d+)"),
    ):
        where = f"{prefix}{path}"
        match = re.search(pattern, text_of(_safe(document, path)))
        if match is None:
            findings.append(f"SNV4-C {where}: publishes no row counts to "
                            "compare")
            continue
        for name, recorded in zip(("purge", "migration"), match.groups()):
            if name in measured and int(recorded) != measured[name]:
                findings.append(
                    f"SNV4-C {where}: records {name} at {recorded} rows, live "
                    f"table measures {measured[name]}")
    require_substrings(namespace, "assurance.recoveryContract",
                       ("purge 6, migration 10",
                        "rootBinding.renameAtomicity.recoveryTableClosure"),
                       "SNV4-C", findings)
    return findings


def _safe(document, path):
    try:
        return resolve_pointer(document, path)
    except MALFORMED_SHAPE_EXCEPTIONS:
        return ""


# ------------------------------------------------ SNV4-P3 device / errno
PREDICATE_HEAD = "lacking the "
PREDICATE_TAIL = " required by the operation being admitted."
RENAME_PRECONDITION = "atomically rename only within one admitted root"


def _errno_freedom(root_binding: dict) -> list[str]:
    """The successor binds to NO errno, deliberately: a mount can present
    EXDEV(18), EBUSY(16), or silently succeed while relocating the mount --
    three behaviours, measured.  Naming one would under-specify the property.
    Exactly one position is exempt, and it must frame itself as an observation
    about a host rather than as a rule."""
    findings: list[str] = []
    for path, value in _strings(root_binding, "rootBinding"):
        if not ERRNO_RE.search(value):
            continue
        if path == ERRNO_OBSERVATION_EXEMPTION:
            if "not about any built storage engine" not in value:
                findings.append(
                    f"SNV4-P3 storageNamespace.{path}: names an errno without "
                    "framing it as a fact about rename(2) on a host")
            continue
        findings.append(
            f"SNV4-P3 storageNamespace.{path}: binds an errno "
            f"({ERRNO_RE.search(value).group(0)}); the rule must be a "
            "device-identity and mount-point property, because a mount can "
            "present EXDEV, EBUSY, or silently succeed while relocating the "
            "mount")
    return findings


def _strings(node, path):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _strings(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _strings(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


# ------------------------------------------------------------------ SNV4-N
def _non_interference(namespace: dict, pre_namespace: dict,
                      env: dict) -> list[str]:
    findings: list[str] = []

    # SN-P3 is stated ONCE, at pathSafety.resolution, by RETYPING the domain of
    # pathSafety.unsupported rather than extending it.
    for path, needles in (
            ("pathSafety.resolution",
             ("atomically rename only within one admitted root whose "
              "layout-derived rename operand set satisfies "
              "rootBinding.properties.SN-P3",
              "does not imply a DEVICE property",
              "established once at admission rather than discovered inside a "
              "state machine")),
            ("pathSafety.unsupported",
             ("The domain of each predicate is the OPERANDS of that operation "
              "and not a filesystem",
              "no predicate was added", "Retyping the domain",
              "atomic rename is a capability of the ordered (source directory, "
              "target directory) pair")),
    ):
        require_substrings(namespace, path, needles, "SNV4-P3", findings)

    # "No predicate was added", measured: the predicate list must be BYTE
    # IDENTICAL to the predecessor's, with only the domain word retyped.
    live = _predicate_list(namespace)
    before = _predicate_list(pre_namespace)
    if live is None or before is None:
        findings.append("SNV4-P3 storageNamespace.pathSafety.unsupported: the "
                        "capability-predicate list cannot be located, so "
                        "'no predicate was added' cannot be measured")
    else:
        if live != before:
            findings.append(
                f"SNV4-P3 storageNamespace.pathSafety.unsupported: the "
                f"predicate list changed; predecessor {before!r}, effective "
                f"{live!r} -- SN-P3 must retype the domain, never extend the "
                "list")
        members = [m for m in re.split(r",\s*|\s+or\s+", live) if m]
        if len(members) != 7:
            findings.append(
                f"SNV4-P3 storageNamespace.pathSafety.unsupported: "
                f"{len(members)} capability predicates measured, 7 required "
                f"({members})")

    # The rename precondition is stated ONCE outside rootBinding, and no
    # ordering step gained a device branch.
    sites = [p for p, v in _strings(namespace, "storageNamespace")
             if RENAME_PRECONDITION in v
             and not p.startswith("storageNamespace.rootBinding")]
    if sites != ["storageNamespace.pathSafety.resolution"]:
        findings.append(
            f"SNV4-P3: the rename precondition {RENAME_PRECONDITION!r} is "
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
                    f"SNV4-P3 storageNamespace.inventoryPurgeMigration.{name}."
                    f"operationOrdering: mentions {token!r}; SN-P3 adds no "
                    "branch to any ordering step")

    # freeze 4.6's purge discharge: the surfaces do not read each other, and
    # physicalLocators is a forbidden input to effective_capability.
    for label, blob_bytes in (("retention-tiers.v24.json",
                               env["retentionTiersBytes"]),
                              ("check-retention-custody-v24.py",
                               env["retentionCheckerBytes"])):
        count = blob_bytes.count(b"storageNamespace")
        if count:
            findings.append(
                f"SNV4-N 4.6: {label} contains {count} occurrence(s) of "
                "'storageNamespace'; the discharge rests on these surfaces not "
                "reading each other")
    tiers = env.get("retentionTiers")
    forbidden = _safe(tiers, "partB_purgeSemantics.effectiveCapabilityDerivation"
                             ".forbiddenInputs") if isinstance(tiers, dict) \
        else ""
    if not isinstance(forbidden, list) or "physicalLocators" not in forbidden:
        findings.append(
            "SNV4-N 4.6: retention-tiers.v24.json "
            "partB_purgeSemantics.effectiveCapabilityDerivation."
            "forbiddenInputs does not list 'physicalLocators'; SN-P3's "
            "device property could then reach effective_capability")
    return findings


def _predicate_list(namespace) -> str | None:
    text = _safe(namespace, "pathSafety.unsupported")
    if not isinstance(text, str) or PREDICATE_HEAD not in text or \
            PREDICATE_TAIL not in text:
        return None
    start = text.index(PREDICATE_HEAD) + len(PREDICATE_HEAD)
    end = text.index(PREDICATE_TAIL, start)
    return text[start:end]


# ------------------------------------------------------ checkerImpact map
def _checker_impact(subject: dict) -> list[str]:
    findings: list[str] = []
    impact = subject.get("checkerImpact")
    if not isinstance(impact, dict):
        return ["SNV4-P0 $.checkerImpact: absent or not an object; this "
                "checker's specification is the list it publishes"]
    listed = impact.get(
        "whatASuccessorCheckerMUSTaddBeforeTheNewMaterialIsMECHANICALLYbound")
    where = ("$.checkerImpact."
             "whatASuccessorCheckerMUSTaddBeforeTheNewMaterialIsMECHANICALLYbound")
    if not isinstance(listed, list):
        return [f"SNV4-P0 {where}: absent or not a list"]
    if len(listed) != len(CHECKER_IMPACT_COVERAGE):
        findings.append(
            f"SNV4-P0 {where}: {len(listed)} assertions published, this "
            f"checker's coverage map discharges {len(CHECKER_IMPACT_COVERAGE)}; "
            "the map is stale and cannot be trusted to name what is covered")
    for anchor, family, _beyond in CHECKER_IMPACT_COVERAGE:
        hits = [i for i, item in enumerate(listed)
                if isinstance(item, str) and anchor in item]
        if len(hits) != 1:
            findings.append(
                f"SNV4-P0 {where}: anchor {anchor!r} (discharged by {family}) "
                f"matches {len(hits)} member(s), expected exactly 1")
    if "paperSealDisclosure" not in impact:
        findings.append("SNV4-P0 $.checkerImpact.paperSealDisclosure: absent; "
                        "the candidate must disclose that rootBinding is "
                        "specification text until a successor checker exists")
    return findings


def check(effective, env) -> list[str]:
    """Total boundary for malformed parsed JSON shapes."""
    if not isinstance(effective, dict) or not effective:
        return ["SNV4-TOTALITY-ROOT: the effective contract must be a "
                "non-empty object"]
    if not isinstance(effective.get("storageNamespace"), dict):
        return ["SNV4-TOTALITY-SHAPE: storageNamespace must be an object"]
    env = dict(env)
    env["namespace"] = effective["storageNamespace"]
    try:
        return _check(effective, env)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"SNV4-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__}: {exc})"]


# ============================================================= observations
def observations(effective, env) -> list[str]:
    """Measured facts a coordinator must carry forward.  Not findings: the
    independent review graded them non-blocking and this instrument closes no
    row and changes no disposition."""
    notes: list[str] = []
    namespace = effective.get("storageNamespace", {})
    root_binding = namespace.get("rootBinding", {})
    statement = text_of(_safe(root_binding, "properties.SN-P3.statement"))
    layout = namespace.get("layout", {})
    journal = layout.get("purgeJournal", "") if isinstance(layout, dict) else ""

    # SNV4R-NB-01, COMPUTED rather than quoted.  Recursion is granted by the
    # clause "every directory beneath X and Y"; the journal's depth below
    # control/ is read off layout.purgeJournal.  If a successor either grants
    # control/ recursion or discloses the bound where the two comparable bounds
    # already sit, this observation reports that instead of repeating itself.
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
            "SNV4-OBS-SCAN-DEPTH: the control/ scan bound is now "
            + ("scanned recursively" if granted
               else "disclosed at renameAtomicity.reachOfTheAdmissionScan")
            + "; review finding SNV4R-NB-01 no longer reproduces against these "
              "bytes.")
    elif depth >= 0:
        notes.append(
            f"SNV4-OBS-SCAN-DEPTH (review SNV4R-NB-01, NON-BLOCKING, owner "
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
            "SNV4-OBS-SCAN-DEPTH: layout.purgeJournal does not sit beneath "
            "<admittedStorageRoot>/control/, so the SNV4R-NB-01 scan-depth "
            "measurement does not apply to these bytes and is not reported.")

    notes.append(
        "SNV4-OBS-UNENFORCED-ELSEWHERE: this checker binds rootBinding at the "
        "SPECIFICATION level only. rootBinding.observabilityBoundary is "
        "correct that whether a built host honours SN-P1..SN-P5 is a G14-class "
        "runtime property no instrument in this corpus can observe. Nothing "
        "here clears the TM row, whose two other conditions are untouched.")
    notes.append(
        "SNV4-OBS-DISCLOSURE-SCOPE: rootBinding.fixtures.enforcementDisclosure "
        "scopes its non-enforcement claim to check-threat-claims.py, whose "
        "T13 closed-set equality over storageNamespace.fixtures still would "
        "reject an addition there. That sentence remains true of that checker "
        "and is not made stale by this file.")
    return notes


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
    subject = jloads(subject_raw.decode("utf-8"), SUBJECT_REL)
    predecessor = jloads(predecessor_raw.decode("utf-8"), PREDECESSOR_REL)

    completeness_path = ROOT / COMPLETENESS_REL
    if not completeness_path.exists():
        print(f"missing derivation reader: {completeness_path}",
              file=sys.stderr)
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location(
        "_snv4_completeness", completeness_path)
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
    checker_path = ROOT / RETENTION_CHECKER_REL
    checker_raw = checker_path.read_bytes() if checker_path.exists() else b""

    env = {
        "subject": subject,
        "predecessor": predecessor,
        "resolvedInputs": resolved_inputs,
        "resolvedInputsBytes": resolved_raw,
        "d9Bytes": d9_raw,
        "retentionTiers": tiers,
        "retentionTiersBytes": tiers_raw,
        "retentionCheckerBytes": checker_raw,
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


# =============================================================== mutations
#
# Each mutation names the finding family that MUST fire.  freeze 7.4 records
# that a non-zero exit is not evidence a guard fired, so the selftest asserts a
# SPECIFIC finding by ID prefix and prints it, rather than counting exits.
def _gut_properties(state):
    for pid in PROPERTY_IDS:
        node = state["effective"]["storageNamespace"]["rootBinding"][
            "properties"][pid]
        for key in list(node):
            if key != "title":
                node[key] = "TBD"


def _delete_root_binding(state):
    del state["effective"]["storageNamespace"]["rootBinding"]


def _drop_argument_position(state):
    node = state["effective"]["storageNamespace"]["rootBinding"]["properties"][
        "SN-P1"]
    node["statement"] = node["statement"].replace(
        "argument position by which a root may be supplied", "path")


def _drop_byte_equality(state):
    node = state["effective"]["storageNamespace"]["rootBinding"]["properties"][
        "SN-P1"]
    node["dispositiveVersusAdvisory"] = \
        "activeRootCanonicalPath decides which root is authoritative."


def _demote_unary_authority(state):
    state["effective"]["storageNamespace"]["authority"] = \
        "Resolution compares the supplied root against activeRootId."


def _refuse_move_and_copy_alike(state):
    for vector in state["effective"]["storageNamespace"]["rootBinding"][
            "fixtures"]["vectors"]:
        if vector["id"] == "accept-root-move-with-bound-locator-absent":
            vector["expected"] = "STORAGE_ROOT_COLLISION"


def _swap_vector_property(state):
    for vector in state["effective"]["storageNamespace"]["rootBinding"][
            "fixtures"]["vectors"]:
        if vector["id"] == "reject-copied-root-two-live-locators":
            vector["violates"] = "SN-P1"


def _drop_a_vector(state):
    vectors = state["effective"]["storageNamespace"]["rootBinding"][
        "fixtures"]["vectors"]
    del vectors[2]


def _vector_valid_as_integer(state):
    state["effective"]["storageNamespace"]["rootBinding"]["fixtures"][
        "vectors"][0]["valid"] = 0


def _schema_version_as_boolean(state):
    state["effective"]["storageNamespace"]["rootBinding"]["schemaVersion"] = True


def _add_a_predicate(state):
    node = state["effective"]["storageNamespace"]["pathSafety"]
    node["unsupported"] = node["unsupported"].replace(
        "fsync or SQLite semantics", "fsync, same-device rename or SQLite "
        "semantics")


def _bind_an_errno(state):
    node = state["effective"]["storageNamespace"]["rootBinding"]["properties"][
        "SN-P3"]
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
    table = state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "purge"]["crashRecoveryTable"]
    table.append({"observed": "PREPARED|canonical-present|quarantine-present",
                  "action": "refuse-cross-device", "nextState": "PREPARED"})


def _drop_migration_row(state):
    del state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "migration"]["crashRecoveryTable"][0]


def _sixth_property(state):
    state["effective"]["storageNamespace"]["rootBinding"]["properties"][
        "SN-P6"] = {"title": "extra", "statement": "extra"}


def _undefined_outcome(state):
    state["effective"]["storageNamespace"]["rootBinding"]["outcomes"][
        "closedValues"].append("STORAGE_ROOT_SURPRISE")


def _undeclared_definition(state):
    state["effective"]["storageNamespace"]["rootBinding"]["outcomes"][
        "definitions"]["STORAGE_ROOT_SURPRISE"] = {
            "meaning": "x", "provenance": "callerOrConfig", "raisedBy": "SN-P1"}


def _phantom_raised_by(state):
    state["effective"]["storageNamespace"]["rootBinding"]["outcomes"][
        "definitions"]["STORAGE_ROOT_UNVERIFIED"]["raisedBy"] = \
        "admittedStorageRoot.thisDoesNotExist"


def _operand_pair_layout_does_not_produce(state):
    pairs = state["effective"]["storageNamespace"]["rootBinding"][
        "renameAtomicity"]["derivedOperandPairs"]
    pairs[0]["targetLayoutKey"] = "cache"


def _drop_an_operand_pair(state):
    del state["effective"]["storageNamespace"]["rootBinding"][
        "renameAtomicity"]["derivedOperandPairs"][1]


def _per_root_authority_record(state):
    state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "migration"]["authorityRecordPath"] = \
        "<admittedStorageRoot>/control/storage-authority/<ProjectId>.json"


def _shrink_a_closed_list(state):
    state["effective"]["storageNamespace"]["inventoryPurgeMigration"][
        "purge"]["reachableDurableNonterminalStates"].pop()


def _permit_physical_locators(state):
    tiers = state["env"]["retentionTiers"]
    tiers["partB_purgeSemantics"]["effectiveCapabilityDerivation"][
        "forbiddenInputs"].remove("physicalLocators")


def _couple_retention_to_namespace(state):
    state["env"]["retentionCheckerBytes"] += b"\n# storageNamespace\n"


def _mint_a_d9_class(state):
    state["env"]["d9Bytes"] += b"\nSTORAGE_ROOT_COLLISION\n"


def _stale_checker_impact_map(state):
    state["env"]["subject"]["checkerImpact"][
        "whatASuccessorCheckerMUSTaddBeforeTheNewMaterialIsMECHANICALLYbound"] \
        .pop()


def _paper_seal_the_disclosure(state):
    state["effective"]["storageNamespace"]["rootBinding"]["fixtures"][
        "enforcementDisclosure"] = "These vectors are enforced."


MUTATIONS = (
    ("gut every rootBinding property to placeholders", _gut_properties,
     "SNV4-P1"),
    ("delete rootBinding entirely", _delete_root_binding, "SNV4-P0"),
    ("SN-P1: replace 'argument position' with a site", _drop_argument_position,
     "SNV4-P1"),
    ("SN-P1: re-promote the advisory path to the decider", _drop_byte_equality,
     "SNV4-P1"),
    ("demote resolution from unary to a comparison", _demote_unary_authority,
     "SNV4-U"),
    ("SN-P2: refuse a moved root the same way as a copied one",
     _refuse_move_and_copy_alike, "SNV4-V"),
    ("SN-P2: attribute the collision vector to the wrong property",
     _swap_vector_property, "SNV4-V"),
    ("drop the copied-root vector", _drop_a_vector, "SNV4-V"),
    ("publish a vector's `valid` as integer 0", _vector_valid_as_integer,
     "SNV4-T"),
    ("publish rootBinding.schemaVersion as boolean true",
     _schema_version_as_boolean, "SNV4-T"),
    ("SN-P3: add an eighth capability predicate", _add_a_predicate, "SNV4-P3"),
    ("SN-P3: bind the rule to EXDEV", _bind_an_errno, "SNV4-P3"),
    ("SN-P3: drop the rename precondition from pathSafety.resolution",
     _drop_rename_precondition, "SNV4-P3"),
    ("SN-P3: branch a purge ordering step on device", _branch_the_state_machine,
     "SNV4-P3"),
    ("add a seventh purge recovery row", _seventh_purge_row, "SNV4-C"),
    ("drop a migration recovery row", _drop_migration_row, "SNV4-C"),
    ("add a sixth property SN-P6", _sixth_property, "SNV4-P0"),
    ("admit an outcome with no definition", _undefined_outcome, "SNV4-X"),
    ("define an outcome that is not admitted", _undeclared_definition,
     "SNV4-X"),
    ("point raisedBy at a position that does not resolve", _phantom_raised_by,
     "SNV4-X"),
    ("declare an operand pair the layout does not produce",
     _operand_pair_layout_does_not_produce, "SNV4-R"),
    ("drop a declared operand pair the state machines still perform",
     _drop_an_operand_pair, "SNV4-R"),
    ("site the authority record inside an admitted root",
     _per_root_authority_record, "SNV4-U"),
    ("shrink a closed collection the derivation must not touch",
     _shrink_a_closed_list, "SNV4-S"),
    ("let physicalLocators reach effective_capability",
     _permit_physical_locators, "SNV4-N"),
    ("couple the retention checker to storageNamespace",
     _couple_retention_to_namespace, "SNV4-N"),
    ("mint a D9 class from a rootBinding outcome", _mint_a_d9_class, "SNV4-X"),
    ("drop a checkerImpact assertion this map claims to discharge",
     _stale_checker_impact_map, "SNV4-P0"),
    ("claim the unenforced vectors are enforced", _paper_seal_the_disclosure,
     "SNV4-P0"),
)

DUPLICATE_KEY_PROBE = (
    '{"storageNamespace": {"schemaVersion": 1, "rootBinding": '
    '{"schemaVersion": 1, "schemaVersion": 2}}}')


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
        state = {"effective": copy.deepcopy(effective),
                 "env": copy.deepcopy(env)}
        try:
            mutate(state)
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            print(f"  ESCAPE  {label}")
            print(f"          mutation could not be applied ({exc!r})")
            escaped += 1
            continue
        found = check(state["effective"], state["env"])
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
          "with its path  [SNV4-A0]")
    print("         ", dupes[0] if dupes
          else "NO FINDING - duplicate key survived")

    print()
    if escaped:
        print(f"{escaped}/{total} retained cases ESCAPED")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations, "
          f"{len(TOTALITY_ROOT_CASES)} root-shape cases and 1 duplicate-key "
          "case rejected by the family named for them - the assertions are "
          "load-bearing")
    return 0


def main() -> int:
    effective, env = load_environment()
    if "--selftest" in sys.argv:
        if effective is None:
            print("cannot self-test: the derivation did not resolve",
                  file=sys.stderr)
            for item in env["derivation"]["declErrors"] + \
                    env["derivation"]["resolveErrors"]:
                print("  -", item, file=sys.stderr)
            return 2
        return selftest(effective, env)

    found = check(effective if effective is not None else {}, env)
    notes = observations(effective, env) if isinstance(effective, dict) else []
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
    print(f"storage-namespace rootBinding OK over the EFFECTIVE contract - "
          f"{provenance['predecessor']} at {provenance['measuredDigest'][:12]}"
          f"... + {provenance['operations']} operations")
    print(f"  subject      {SUBJECT_REL} @ {SUBJECT_SHA[:12]}... (verified)")
    print(f"  predecessor  {PREDECESSOR_REL} @ {PREDECESSOR_SHA[:12]}... "
          "(verified)")
    print(f"  reader       {COMPLETENESS_REL} @ {env['readerDigest'][:12]}... "
          "(measured, not pinned - freeze 7.6 records it as editable)")
    print(f"  bound        {len(root_binding['properties'])} properties, "
          f"{len(root_binding['outcomes']['closedValues'])} closed outcomes, "
          f"{len(root_binding['fixtures']['vectors'])} vectors decided from "
          f"worlds, "
          f"{len(root_binding['renameAtomicity']['derivedOperandPairs'])} "
          "operand pairs re-derived from layout")
    purge_table = lifecycle["purge"]["crashRecoveryTable"]
    migration_table = lifecycle["migration"]["crashRecoveryTable"]
    migration_domain = {row["observed"].split("|", 1)[0]
                        for row in migration_table}
    print(f"  closure      purge {len(purge_table)} rows over "
          f"{len(lifecycle['purge']['reachableDurableNonterminalStates'])} "
          f"durable nonterminal states, migration {len(migration_table)} rows "
          f"over {len(migration_domain)} (measured each run, hard-compared to "
          "the counts written in prose)")
    print("  scope        1 addition (rootBinding), 0 removals, 12 changed "
          "prose leaves, 26 predecessor lists byte-identical, purge subtree "
          "untouched")
    print("\n  observations (not findings):")
    for note in notes:
        print("   ", note)
    print("\n  this instrument changes no status, disposition, verdict or "
          "seal, and closes no row. TM remains UNSET - BLOCKS FREEZE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
