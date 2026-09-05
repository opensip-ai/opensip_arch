#!/usr/bin/env python3
"""Successor companion instrument for c2-plan-stage-schema.v11.json.

WHY THERE IS A v12 AT ALL

  check-c2-v11.py was reviewed SOUND WITHIN ITS DECLARED SCOPE and is pinned by
  that review, so freeze section 7.2 forbids editing it.  This file edits
  nothing: it is a successor, written beside its predecessor, over the same
  subject bytes.

  The same review asked the only question that matters of an instrument -- "can
  I make the checker pass on a wrong artifact?" -- and answered YES, TWELVE
  TIMES.  Every one of the twelve has a single shape:

      A LEAF WHOSE VALUE IS FALSE WHILE ITS PATH AND ITS JSON TYPE ARE
      UNCHANGED.

  The published documentSkeleton binds path and type only.  It therefore cannot
  move under any of the twelve, and the predecessor's gates that DO bind values
  bound an enumerated set that did not include them.  The escapes included the
  candidate's CENTRAL RULING reversed in prose, its self-reported
  measuredPredecessorDigests falsified, and all six entries of
  theSixLiveOnePointZeroLeaves fabricated.

  The sharpest instance -- OBS-4 -- is the artifact judging itself unevenly.
  The candidate's HEADLINE numeric correction (the affected-leaf count is six,
  enumerated by path) was enumerated but never re-derived, while its exactly
  analogous closure count WAS re-derived -- even though the artifact's own
  theClosureCount.whyABareCountIsTheDefect argues that "Enumeration is what
  makes it a measurement".  A figure you enumerate and do not recompute is
  exactly the figure an instrument will let you fabricate.

WHAT THIS INSTRUMENT ADDS

  1. IT BINDS ASSERTIONS AGAINST AN INPUT THAT IS WRONG, NOT MERELY ABSENT.
     Every instrument in this lineage fired on REMOVAL -- a deleted key moves a
     path, and the skeleton catches it -- and stayed silent on FALSITY.  Each of
     the twelve escapes is carried in --selftest as a mutation that KEEPS THE
     SHAPE AND INVERTS THE MEANING, and each row additionally reports that the
     skeleton digest did NOT move, so a reader can see the catch is a VALUE
     catch and not a structural accident.  Every bound claim also fails when it
     is DELETED (C2V12-CLAIM-ABSENT): a gate whose subject can be removed is not
     a gate.

  2. IT RE-DERIVES ITS CONSTANTS FROM THE ARTIFACT.  A sibling instrument was
     REJECTED because its census constants were hand-typed literals, so it
     tested its own transcription rather than the artifact.  Here the census
     comes from the pinned node_census; the vector EXPECTATIONS and, wherever
     the contract states them machine-readably, the vector INPUTS come from the
     contract; the 3-of-7 production split is parsed out of the contract's own
     prose rather than typed; the ruling's POLARITY is derived by measuring
     which side of the contradiction actually moved between the effective
     predecessor and the effective successor; and every numeral this file
     compares against is a number this run computed.

  3. IT REQUIRES PUBLISHED CORPORA TO BE NON-DEGENERATE.  A sibling instrument
     let 10 of 17 published vectors collapse to a single digest at 0 findings.
     Agreement between a recomputation and a publication is worthless if both
     sides are constant.  Every digest corpus this file reproduces is also
     measured for DISTINCTNESS, and the recomputed distinct count must equal the
     published one.

WHAT IS CARRIED FORWARD UNCHANGED IN SUBSTANCE FROM THE PREDECESSOR

  The predecessor is the strongest instrument of the four in this lineage and
  the review credited it with making an independent review possible at all.
  All of it is kept:

    * opensip-jx-canon-v1 implemented FROM THE CONTRACT'S OWN TEXT, driving its
      tags from the contract's typeTags registry and vendoring NO copy of the
      pinned jx_canon.  It reproduces the head's documentSkeleton.sha256 and all
      29 root-subtree digests.  Reproducing them by importing the head's encoder
      would prove only that the code equals itself.
    * exit 2 on subject drift, BEFORE a byte is parsed.
    * duplicate keys refused and NAMED at their key (freeze section 7.5).
    * law 18 by `value is True or value is False` BEFORE the int test -- an
      identity test, immune to any int subclass.
    * `os` is NEVER IMPORTED, so os.walk/listdir/scandir are structurally
      unreachable rather than merely absent, and no directory is enumerated.
      Every file this instrument opens is named: a pinned entry, or a path the
      artifact itself declares, admitted only after a no-traversal check.
    * EPC-V2 EXECUTED over generated witnesses with a real discriminator.
    * the selftest escape that taught a true fact: object ordering cannot reach
      the skeleton digest BECAUSE THE SKELETON CONTAINS NO OBJECT.  That is the
      declared 3-of-7 production split, and it is executed rather than read.
      v12 extends the split coverage: the split is now also DERIVED from the
      contract's prose, and the four unexercised productions are each pinned by
      a contract-sourced vector whose separation is itself re-derived.

WHAT THIS INSTRUMENT STILL DOES NOT DO

  It does not close the whole class.  L17 MEASURES the residue rather than
  gesturing at it: it counts the subject's leaves, counts how many are bound to
  a value this run computed, and prints the unbound remainder per top-level key.
  Falsifying an unbound narrative leaf is still an escape, and L16 says how many
  such leaves there are.  A green run remains checker-scope evidence authored in
  the same lane as the subject; it is not independent review.

INVOCATION
  python3 -I -B artifacts/check-c2-v12.py [subject.json]
  python3 -I -B artifacts/check-c2-v12.py --selftest

EXIT CODES (checkerModeContract)
  0  clean, or a green --selftest
  1  findings in the subject, or an escaped mutation in --selftest
  2  unsupported invocation, unreadable subject, subject drift, or a pinned
     input that does not hash to its declared digest
  3  --selftest REFUSED because the base subject is not clean.  A mutation
     suite over a dirty base is not an oracle: every row would echo the
     pre-existing failure and report "all rejected".  Exit 3 can never be
     absorbed into a pass.

AUTHORITY
  This file binds nothing.  It closes no IMPLEMENTATION-FREEZE section 7.1 row,
  changes no status, disposition, verdict or seal, introduces no [UNSET], leaves
  CD-RT-5 at BLOCKED_ON_PHASE_1A, and repoints no head.  c2-plan-stage-schema.v9
  remains the head and check-c2-v9.py remains its instrument.  check-c2-v11.py
  is left byte-identical.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import pathlib
import re
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

SUBJECT = "c2-plan-stage-schema.v11.json"
SUBJECT_SHA256 = "d35b677d6726a8f9b9fc70e2e0f3307af909eca876cd6670d238829ba95a81f8"

# Pinned transitive inputs.  Each is read once as inert bytes, hash-verified,
# and then parsed or executed FROM THAT VERIFIED BYTE STRING.
PINS = {
    "c2-plan-stage-schema.v10.json":
        "0e550b1615c62cdd7b203221d4ddce6e229848c9e59e1403c1bb603ac5447406",
    "c2-plan-stage-schema.v9.json":
        "321faeaa3b70c83991f1cceefc9335891d69fa502b3d62cfa133494bb4e9c5a1",
    "c2-plan-stage-schema.v4.json":
        "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    "check-c2-v4.py":
        "54ff764d155f5582bc66fd7bf8138b7eaed5f90f46b92975c4bc7a85ffb3df17",
    "check-c2-v9.py":
        "ae9525f1d2efa7688fb6b678e89161f5cf1e3b38f7fd3a9f712c1b6a75be3035",
    "check-completeness.py":
        "6c52a5f9a4ac6a3ec3dae9fb0c87e82552744b18eb8cc38d1c4522ade3e549d6",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
JSON_NAME_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*\.json$")
STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")
SHA256ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TOKEN_RE = re.compile(r"^[zbinsao][0-9]+:")
SAFE_REL_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*$")

# The chain the instrument itself resolves.  Used only to report; never to
# substitute for a measurement.
DOC_SUBJECT = "SUBJECT"
DOC_EFFECTIVE = "EFFECTIVE"


class Refused(Exception):
    """A condition that makes the run impossible, not merely failing."""


# --------------------------------------------------------------------------
# L1  parse integrity: duplicate keys are named, at their key
# --------------------------------------------------------------------------
class DuplicateKey(Exception):
    pass


def dup_rejecting_hook(pairs):
    """Freeze section 7.5.  Python's default keeps the LAST duplicate silently,
    which is how a document can say two things and be read as saying one."""
    out = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def parse_json(text: str, where: str):
    try:
        return json.loads(text, object_pairs_hook=dup_rejecting_hook)
    except DuplicateKey as exc:
        raise Refused("%s: duplicate key %r at object scope; the document "
                      "states two values for one name" % (where, exc.args[0]))
    except json.JSONDecodeError as exc:
        raise Refused("%s: not JSON: %s" % (where, exc))


_BYTES = {}


def verified_bytes(name: str) -> bytes:
    """A pinned input, hash-verified before its bytes are used for anything."""
    if name in _BYTES:
        return _BYTES[name]
    if name not in PINS:
        raise Refused("%s is not a pinned input of this instrument" % name)
    path = HERE / name
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Refused("pinned input %s cannot be read: %s" % (name, exc))
    actual = hashlib.sha256(raw).hexdigest()
    if actual != PINS[name]:
        raise Refused("pinned input %s: declared %s, measured %s"
                      % (name, PINS[name], actual))
    _BYTES[name] = raw
    return raw


def declared_bytes(rel: str):
    """Read a path the ARTIFACT declares, so its published digest can be
    measured rather than believed.

    This is a NAMED read, never an enumeration: there is no glob, no iterdir,
    no listdir, no scandir and no walk anywhere in this file, and `os` is never
    imported, so a directory cannot be traversed even by accident.  A declared
    path that tries to leave the document root, or that is not a plain relative
    name, is refused rather than opened.
    """
    if not isinstance(rel, str) or not SAFE_REL_RE.match(rel) or ".." in rel:
        return None, "%r is not a plain relative path under the document root" % (rel,)
    try:
        raw = (ROOT / rel).read_bytes()
    except OSError as exc:
        return None, "cannot be read: %s" % exc
    return hashlib.sha256(raw).hexdigest(), None


_MODULES = {}


def load_pinned_module(name, modname):
    """Execute a pinned input as a module, from bytes already hash-verified.

    stdout is captured so a pinned module can never write into this
    instrument's report.
    """
    if modname in _MODULES:
        return _MODULES[modname]
    verified_bytes(name)
    spec = importlib.util.spec_from_file_location(modname, HERE / name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    _MODULES[modname] = module
    return module


# --------------------------------------------------------------------------
# structural helpers
# --------------------------------------------------------------------------
def render_path(steps) -> str:
    """The rendering the artifact itself uses for a leaf path:
    `planIntentFixtures[36].mutation.value`."""
    out = ""
    for step in steps:
        if isinstance(step, int):
            out += "[%d]" % step
        else:
            out += ("." + step) if out else step
    return out


def walk_leaves(node, steps=()):
    """Every LEAF of a JSON value, with its path.  Containers are not leaves."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_leaves(value, steps + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_leaves(value, steps + (index,))
    else:
        yield steps, node


def path_steps(path: str):
    if not path or path.startswith(".") or path.endswith(".") or ".." in path:
        return None
    steps = [int(i) if i else n for i, n in STEP_RE.findall(path)]
    return steps or None


class Missing:
    """Distinguishes 'absent' from 'present and null'."""

    def __repr__(self):
        return "<absent>"


MISSING = Missing()


def dotted_get(root, path: str):
    steps = path_steps(path)
    if steps is None:
        return MISSING
    node = root
    for step in steps:
        if isinstance(node, dict) and isinstance(step, str) and step in node:
            node = node[step]
        elif (isinstance(node, list) and isinstance(step, int)
              and 0 <= step < len(node)):
            node = node[step]
        else:
            return MISSING
    return node


def exact_equal(left, right) -> bool:
    """Type-exact deep equality.  `True` is not `1`; `1` is not `1.0`.
    Section 6 law 18 at the comparison primitive."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            exact_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def degeneracy(values):
    """(population, distinct, modal multiplicity) of a published corpus.

    A recomputation that agrees with a publication proves nothing if both sides
    are constant.  This is the measurement that says whether they are.
    """
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return len(values), len(counts), (max(counts.values()) if counts else 0)


NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}


def numeral(token):
    """A numeral written as digits or as an English word, or None."""
    if token is None:
        return None
    lowered = token.lower()
    if lowered in NUMBER_WORDS:
        return NUMBER_WORDS[lowered]
    if token.isdigit():
        return int(token)
    return None


def flat(text: str) -> str:
    """Whitespace collapsed, per freeze section 7.7: a line-wrapped quotation
    must not be able to produce a false 'absent'."""
    return " ".join(text.split())


# --------------------------------------------------------------------------
# L4  opensip-jx-canon-v1, implemented FROM THE CONTRACT TEXT
# --------------------------------------------------------------------------
# Phrases the implementation below depends on.  If the contract stops saying
# these, this encoder is no longer entitled to assume them and the gate fails
# rather than quietly encoding by its own habits.
#
# The last three entries are new in v12 and close review observation OBS-6:
# positionalForm and scientificForm carry the whole substance of the number
# repair, and under the predecessor they could be rewritten to state a rule
# flatly contradicting both the encoder and the block's own vectors while the
# run stayed green.
PROSE_OBLIGATIONS = (
    ("frame", "tag || DECIMAL(N) || ':' || payload"),
    ("frameParts.lengthIsCountedInCodePoints", "UNICODE CODE POINTS"),
    ("frameParts.separator", "COLON"),
    ("objectOrdering.rule", "CANONICAL TOKEN of the key"),
    ("digestBoundary", "UTF-8"),
    ("documentSkeleton.walk", "pre-order"),
    ("documentSkeleton.row", "JSON type name"),
    ("productions.number", "decimal point or an exponent"),
    ("numberProduction.sign", "sign bit"),
    ("numberProduction.rule", "greater than 16"),
    ("numberProduction.positionalForm", "ALWAYS contains a full stop"),
    ("numberProduction.scientificForm", "mandatory sign"),
    ("numberProduction.scientificForm", "AT LEAST two digits"),
)


class ContractEncoder:
    """opensip-jx-canon-v1 driven by the contract, not by this file.

    The type tags come from the contract's own `typeTags` registry.  The
    productions are implemented from the contract's prose, and `obligations()`
    asserts that prose still says what this implementation assumes.

    NO copy of the pinned `jx_canon` is imported or vendored here.  The head's
    primitive IS loaded elsewhere in this file, as an ORACLE for the number
    production alone (L13); it is never used to compute a skeleton digest, and
    the report says so on its own line, because reproducing the head's digests
    with the head's own encoder would establish only that the code equals
    itself.
    """

    def __init__(self, spec: dict):
        self.spec = spec
        self.tags = spec["typeTags"]

    def obligations(self) -> list[str]:
        out = []
        for path, phrase in PROSE_OBLIGATIONS:
            text = dotted_get(self.spec, path)
            if text is MISSING:
                out.append("documentIdentityEncoding.%s is absent, so this "
                           "encoder's assumption '%s' is unwitnessed by the "
                           "contract" % (path, phrase))
                continue
            if not isinstance(text, str) or phrase not in text:
                out.append("documentIdentityEncoding.%s no longer states %r; "
                           "the encoder assumes it" % (path, phrase))
        for kind, tag in (("null", "z"), ("boolean", "b"), ("integer", "i"),
                          ("number", "n"), ("string", "s"), ("array", "a"),
                          ("object", "o")):
            if self.tags.get(kind) != tag:
                out.append("documentIdentityEncoding.typeTags.%s is %r, not %r"
                           % (kind, self.tags.get(kind), tag))
        return out

    # -- the seven productions ---------------------------------------------
    @staticmethod
    def jtype(value) -> str:
        if value is None:
            return "null"
        # law 18 by IDENTITY, before the int test: immune to int subclasses.
        if value is True or value is False:
            return "boolean"
        if type(value) is int:
            return "integer"
        if type(value) is float:
            return "number"
        if type(value) is str:
            return "string"
        if type(value) is list:
            return "array"
        if type(value) is dict:
            return "object"
        raise Refused("%r is outside the JSON value universe" % (value,))

    def frame(self, kind: str, payload: str) -> str:
        # N counts UNICODE CODE POINTS, not UTF-8 bytes.
        return self.tags[kind] + str(len(payload)) + ":" + payload

    @staticmethod
    def number_payload(value: float) -> str:
        """The repaired production: shortest round-tripping decimal that always
        carries a point or an exponent; sign taken from the SIGN BIT."""
        negative = (struct.unpack("<Q", struct.pack("<d", value))[0] >> 63) == 1
        sign = "-" if negative else ""
        magnitude = -value if negative else value
        if magnitude == 0.0:
            digits, exponent = "0", 1
        else:
            for precision in range(0, 18):
                candidate = "%.*e" % (precision, magnitude)
                if float(candidate) == magnitude:
                    break
            mantissa, _, exp = candidate.partition("e")
            digits = mantissa.replace(".", "").rstrip("0") or "0"
            exponent = int(exp) + 1
        width = len(digits)
        if exponent <= -4 or exponent > 16:
            head = digits[0] + ("." + digits[1:] if width > 1 else "")
            power = exponent - 1
            return "%s%se%s%02d" % (sign, head, "+" if power >= 0 else "-",
                                    abs(power))
        if exponent <= 0:
            return sign + "0." + "0" * (-exponent) + digits
        if exponent >= width:
            return sign + digits + "0" * (exponent - width) + ".0"
        return sign + digits[:exponent] + "." + digits[exponent:]

    def canon(self, value) -> str:
        kind = self.jtype(value)
        if kind == "null":
            return self.frame("null", "")
        if kind == "boolean":
            return self.frame("boolean", "1" if value else "0")
        if kind == "integer":
            return self.frame("integer", str(value))
        if kind == "number":
            return self.frame("number", self.number_payload(value))
        if kind == "string":
            return self.frame("string", value)
        if kind == "array":
            return self.frame("array", "".join(self.canon(i) for i in value))
        # ordered by ascending (KEY TOKEN, VALUE TOKEN), NOT by raw key
        pairs = sorted((self.canon(k), self.canon(v)) for k, v in value.items())
        return self.frame("object", "".join(k + v for k, v in pairs))

    def digest(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def rows(self, root) -> list:
        out = []

        def walk(node, path):
            out.append([self.canon(list(path)), self.jtype(node)])
            kind = self.jtype(node)
            if kind == "object":
                for key in node:
                    walk(node[key], path + [key])
            elif kind == "array":
                for index, item in enumerate(node):
                    walk(item, path + [index])

        walk(root, [])
        return out

    def skeleton_digest(self, root) -> str:
        return self.digest(self.canon(self.rows(root)))

    def counts(self, root) -> dict:
        out = {"nodes": 0, "containers": 0, "leaves": 0, "nullLeaves": 0,
               "booleanLeaves": 0, "integerLeaves": 0, "numberLeaves": 0,
               "stringLeaves": 0}
        tokens = set()
        for token, kind in self.rows(root):
            out["nodes"] += 1
            tokens.add(token)
            if kind in ("object", "array"):
                out["containers"] += 1
            else:
                out["leaves"] += 1
                out[kind + "Leaves"] += 1
        out["distinctPathTokens"] = len(tokens)
        return out


# --------------------------------------------------------------------------
# L3  derivation resolution -- native, then cross-checked against the corpus
# --------------------------------------------------------------------------
def is_operation_list(value) -> bool:
    return (isinstance(value, list) and bool(value)
            and all(isinstance(i, dict) and isinstance(i.get("op"), str)
                    and isinstance(i.get("path"), str) and i.get("path")
                    for i in value))


def find_declaration(doc: dict):
    """Located by SHAPE, not by the key name.  Finding it by the name
    `derivedFrom` would reproduce, one level up, the naming fragility
    CMP-IR-01 names."""
    found = []
    for key, value in doc.items():
        if not isinstance(value, dict):
            continue
        names = [v for v in value.values()
                 if isinstance(v, str) and JSON_NAME_RE.match(v)]
        digests = [v for v in value.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        ops = [v for v in value.values() if is_operation_list(v)]
        if len(names) == 1 and len(digests) == 1 and len(ops) == 1:
            found.append((key, {"artifact": names[0], "sha256": digests[0],
                                "operations": ops[0]}))
    if len(found) > 1:
        raise Refused("ambiguous derivation: " + ", ".join(k for k, _ in found))
    return found[0][1] if found else None


def apply_operations(base, operations):
    effective = copy.deepcopy(base)
    errors = []
    for index, op in enumerate(operations):
        kind, path = op.get("op"), op.get("path")
        where = "operation %d (%s %s)" % (index, kind, path)
        if kind not in ("set", "add"):
            errors.append("%s: unknown verb" % where)
            continue
        if "value" not in op:
            errors.append("%s: carries no value" % where)
            continue
        steps = path_steps(path)
        if steps is None:
            errors.append("%s: path is not plainly resolvable" % where)
            continue
        node = effective
        ok = True
        for step in steps[:-1]:
            if isinstance(node, dict) and isinstance(step, str) and step in node:
                node = node[step]
            elif (isinstance(node, list) and isinstance(step, int)
                  and 0 <= step < len(node)):
                node = node[step]
            else:
                ok = False
                break
        if not ok or not isinstance(node, (dict, list)):
            errors.append("%s: parent does not resolve to a container" % where)
            continue
        last = steps[-1]
        exists = ((isinstance(node, dict) and isinstance(last, str) and last in node)
                  or (isinstance(node, list) and isinstance(last, int)
                      and 0 <= last < len(node)))
        if kind == "set":
            if "from" not in op:
                errors.append("%s: a set must restate the value it replaces" % where)
                continue
            if not exists:
                errors.append("%s: does not resolve against the predecessor" % where)
                continue
            if not exact_equal(node[last], op["from"]):
                errors.append(
                    "%s: declares it replaces %r (%s) but the verified "
                    "predecessor holds %r (%s); the derivation does not "
                    "describe the bytes it is applied to"
                    % (where, op["from"], type(op["from"]).__name__,
                       node[last], type(node[last]).__name__))
                continue
        else:
            if exists:
                errors.append("%s: already exists in the predecessor" % where)
                continue
            if not isinstance(node, dict) or not isinstance(last, str):
                errors.append("%s: can only add a named member to an object" % where)
                continue
        node[last] = copy.deepcopy(op["value"])
    return effective, errors


def resolve(doc: dict, seen=()):
    """Materialise the effective contract.  Every predecessor is hash-verified
    BEFORE its bytes are parsed, and a mismatch refuses the run.

    Returns (effective, chain, measured) where `measured` maps each pinned
    predecessor name to the digest THIS RUN measured of its bytes.  That map is
    what L11 compares the artifact's self-reported digest table against; the
    predecessor holds all three true values and never compared them.
    """
    declaration = find_declaration(doc)
    if declaration is None:
        return doc, [], {}
    name = declaration["artifact"]
    if name not in PINS:
        raise Refused("declared predecessor %s is not a pinned input of this "
                      "instrument, so its digest cannot be verified" % name)
    if name in seen:
        raise Refused("derivation chain revisits " + name)
    raw = verified_bytes(name)
    measured = hashlib.sha256(raw).hexdigest()
    if measured != declaration["sha256"]:
        raise Refused("predecessor digest mismatch for %s: declared %s, "
                      "measured %s" % (name, declaration["sha256"], measured))
    base = parse_json(raw.decode("utf-8"), name)
    base, chain, digests = resolve(base, seen + (name,))
    effective, errors = apply_operations(base, declaration["operations"])
    if errors:
        raise Refused("; ".join(errors))
    digests = dict(digests)
    digests[name] = measured
    return effective, [name] + chain, digests


# --------------------------------------------------------------------------
# EPC-V2, executed
# --------------------------------------------------------------------------
POSITIONS = ("planIntentCommitment", "executionPlanCommitment")


def admit_sha256id(value, position: str):
    """comparisonDiscipline made executable: an INDEPENDENT TYPE ASSERTION on
    each side BEFORE any comparison.  Every JSON production other than string
    is refused by name, and so is every non-canonical spelling."""
    if type(value) is not str:
        return ("%s: wire type sha256Id requires the JSON string production; "
                "this position holds the %s production"
                % (position, ContractEncoder.jtype(value)))
    if not SHA256ID_RE.match(value):
        return ("%s: %r is not the canonical spelling of a sha256Id "
                "(^sha256:[0-9a-f]{64}$)" % (position, value))
    return None


def epc_decide(record, degrade=None, golden=None):
    """The decision procedure EPC-V2 requires.  Returns (verdict, reasons).

    `degrade` exists only for --selftest: it names a way an implementation
    could go wrong, so the suite can prove the gate catches it.
    """
    reasons = []
    for position in POSITIONS:
        if position not in record:
            reasons.append("%s: position absent" % position)
            continue
        problem = admit_sha256id(record[position], position)
        if problem:
            reasons.append(problem)
    if reasons:
        return "REJECT", reasons

    left = record["planIntentCommitment"].encode("utf-8")
    right = record["executionPlanCommitment"].encode("utf-8")

    if degrade == "golden-drift":
        # The failure the v10 review measured: reject anything that is not the
        # published golden, which rejects differing AND agreeing-but-wrong
        # positions identically and is therefore not this control at all.
        if right != golden.encode("utf-8"):
            return "REJECT", ["executionPlanCommitment: not the golden value"]
        return "ACCEPT", []
    if degrade == "host-equality":
        if record["planIntentCommitment"] == record["executionPlanCommitment"]:
            return "ACCEPT", []
        return "REJECT", ["executionPlanCommitment: differs"]
    if degrade == "always-accept":
        return "ACCEPT", []

    if left != right:
        return "REJECT", [
            "executionPlanCommitment: %r is not byte-identical to this "
            "ExecutionPlan's planIntentCommitment %r; requiredValue makes "
            "equality the field's DEFINITION, so the record is INVALID"
            % (record["executionPlanCommitment"],
               record["planIntentCommitment"])]
    return "ACCEPT", []


def epc_witnesses(golden: str):
    """Records the rule quantifies over.  C-2's ExecutionPlan envelope is
    closed and cannot carry executionPlanCommitment, so these are GENERATED
    witnesses, not C-2 fixtures.  requiredValue is stated as 'wherever a record
    carries a field named executionPlanCommitment', which is a quantifier."""
    other = "sha256:" + hashlib.sha256(b"EPC-V2 not-the-golden").hexdigest()
    third = "sha256:" + hashlib.sha256(b"EPC-V2 third value").hexdigest()
    cases = [
        ("EPC-POS-golden", {POSITIONS[0]: golden, POSITIONS[1]: golden},
         "ACCEPT", "both positions carry the ExecutionPlan's own commitment"),
        ("EPC-V2-differing-positions",
         {POSITIONS[0]: golden, POSITIONS[1]: other}, "REJECT",
         "THE CONTROL: executionPlanCommitment is a well-formed sha256Id that "
         "is not this ExecutionPlan's planIntentCommitment"),
        ("EPC-V2-DISCRIMINATOR-agreeing-but-not-golden",
         {POSITIONS[0]: other, POSITIONS[1]: other}, "ACCEPT",
         "THE DISCRIMINATOR: both positions agree at a value that is NOT the "
         "published golden. Accepting this is what separates a positions-"
         "differ guard from golden-drift detection"),
        ("EPC-V2-differing-the-other-way",
         {POSITIONS[0]: other, POSITIONS[1]: golden}, "REJECT",
         "the same defect with the arms exchanged"),
        ("EPC-V2-differing-at-a-third-value",
         {POSITIONS[0]: third, POSITIONS[1]: other}, "REJECT",
         "neither position is the golden and they still differ"),
    ]
    # EPC-V4: every JSON production other than string, at each position.
    injections = [("null", None), ("boolean", True), ("integer", 1),
                  ("number", 1.0), ("array", [golden]), ("object", {"v": golden})]
    for position in POSITIONS:
        for label, value in injections:
            record = {POSITIONS[0]: golden, POSITIONS[1]: golden}
            record[position] = value
            cases.append(("EPC-V4-%s-at-%s" % (label, position), record,
                          "REJECT", "law 18 exact-type admission: the %s "
                          "production at %s" % (label, position)))
        for label, value in (("uppercase-hex", "sha256:" + "A" * 64),
                             ("no-prefix", "0" * 64),
                             ("wrong-prefix", "plan1:sha256:" + "0" * 64),
                             ("leading-space", " " + golden),
                             ("trailing-space", golden + " ")):
            record = {POSITIONS[0]: golden, POSITIONS[1]: golden}
            record[position] = value
            cases.append(("EPC-V4-%s-at-%s" % (label, position), record,
                          "REJECT", "non-canonical spelling at " + position))
    return cases


# --------------------------------------------------------------------------
# the report, and the register that binds a published claim to a measurement
# --------------------------------------------------------------------------
class Report:
    def __init__(self, quiet=False):
        self.lines = []
        self.findings = []
        self.skips = []
        self.quiet = quiet

    def say(self, text=""):
        if not self.quiet:
            self.lines.append(text)

    def finding(self, code, position, detail):
        self.findings.append((code, position, detail))

    def skip(self, code, why):
        self.skips.append((code, why))

    def codes(self):
        return {code for code, _p, _d in self.findings}


class Register:
    """Every published claim this instrument binds passes through here.

    bind() does three things a bare comparison does not.  It refuses ABSENCE as
    well as falsity, because a gate whose subject can be deleted is not a gate.
    It compares TYPE-EXACTLY, so a boolean true cannot satisfy an integer 1.
    And it records the leaf as BOUND, so L16 can measure -- rather than assert
    -- how much of the document this instrument actually holds down.
    """

    def __init__(self, report):
        self.report = report
        self.bound = set()
        self.checked = 0

    def note(self, label, path):
        self.bound.add((label, path))

    def bind(self, label, root, path, measured, how,
             code="C2V12-SELF-REPORT"):
        self.checked += 1
        self.note(label, path)
        published = dotted_get(root, path)
        if published is MISSING:
            self.report.finding(
                "C2V12-CLAIM-ABSENT", "%s %s" % (label, path),
                "this instrument binds this claim to a measurement (%s) and "
                "the claim is not present; a gate whose subject can be deleted "
                "is not a gate" % how)
            return False
        if not exact_equal(published, measured):
            self.report.finding(
                code, "%s %s" % (label, path),
                "published %r (%s), %s gives %r (%s)"
                % (published, type(published).__name__, how, measured,
                   type(measured).__name__))
            return False
        return True

    def bind_membership(self, label, root, path, measured, how,
                        code="C2V12-SELF-REPORT"):
        """A published list whose MEANING is membership, not order.

        Compared as a set, and separately checked for duplicates, so a
        re-ordering cannot raise a false finding while a fabricated or missing
        member still fires and is NAMED.
        """
        self.checked += 1
        self.note(label, path)
        published = dotted_get(root, path)
        if published is MISSING:
            self.report.finding(
                "C2V12-CLAIM-ABSENT", "%s %s" % (label, path),
                "this instrument binds this membership claim to a measurement "
                "(%s) and the claim is not present" % how)
            return False
        if not isinstance(published, list):
            self.report.finding(code, "%s %s" % (label, path),
                                "published %r is not a list" % (published,))
            return False
        if len(published) != len(set(published)):
            self.report.finding(code, "%s %s" % (label, path),
                                "the list repeats a member; an enumeration "
                                "that repeats itself is not a census")
            return False
        extra = sorted(set(published) - set(measured))
        missing = sorted(set(measured) - set(published))
        if extra or missing:
            self.report.finding(
                code, "%s %s" % (label, path),
                "%s gives a different membership: published-but-not-measured "
                "%s; measured-but-not-published %s" % (how, extra, missing))
            return False
        return True


# --------------------------------------------------------------------------
# the number production, measured against the PINNED head primitive
# --------------------------------------------------------------------------
_MASK64 = (1 << 64) - 1
ORACLE_PATTERNS = 200000


def _bit_stream(count, seed=0x9E3779B97F4A7C15):
    """A deterministic 64-bit stream.  Deterministic on purpose: a checker
    whose sample changes between runs cannot be re-run by a reviewer and
    compared."""
    state = seed
    for _ in range(count):
        state = (state + 0x9E3779B97F4A7C15) & _MASK64
        z = state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _MASK64
        yield z ^ (z >> 31)


def _edge_values():
    """Hand-chosen edges plus dense structured sweeps: the thresholds the rule
    names, the subnormal floor, the finite ceiling, and every decimal exponent
    the format admits."""
    out = [0.0, -0.0, 1.0, -1.0, 100.0, 1.5, 1e15, 1e16, 1e17, 1e22,
           0.0001, 0.00001, 5e-324, -5e-324, 1.7976931348623157e308,
           -1.7976931348623157e308, 2.2250738585072014e-308,
           0.1, 0.2, 0.3, 1 / 3, 2 / 3, 1e-323, 9007199254740993.0,
           123456789012345680.0, 4.9e-324]
    for exponent in range(-320, 309):
        for mantissa in ("1", "1.5", "9.99", "1.234567890123456"):
            try:
                value = float("%se%d" % (mantissa, exponent))
            except (ValueError, OverflowError):
                continue
            if value == value and value not in (float("inf"), float("-inf")):
                out.append(value)
                out.append(-value)
    return out


_ORACLE = {}


def number_oracle(encoder):
    """Re-run the comparison numberProduction.howThisWasVerified reports.

    The artifact claims its restated rule was implemented FROM ITS OWN TEXT and
    compared against the PINNED instrument's number token, at zero mismatches.
    The predecessor accepted that sentence; changing 'Mismatches: ZERO' to
    'Mismatches: SEVENTEEN' ran green.  Here the comparison is performed, and
    the published numeral is bound to the number this run measured.

    This is the ONLY place the head's primitive is executed.  It is an oracle
    for one production; it never computes a skeleton digest, because
    reproducing the head's digests with the head's own encoder would establish
    only that the code equals itself.
    """
    if "result" in _ORACLE:
        return _ORACLE["result"]
    head_module = load_pinned_module("check-c2-v9.py", "_c2v9_v12")
    mismatches = []
    tested = nonfinite = 0
    for value in _edge_values():
        tested += 1
        mine = encoder.frame("number", encoder.number_payload(value))
        theirs = head_module.jx_canon(value)
        if mine != theirs:
            mismatches.append((value, mine, theirs))
    for bits in _bit_stream(ORACLE_PATTERNS):
        value = struct.unpack("<d", struct.pack("<Q", bits))[0]
        # The rule opens "Let v be a finite binary64 value".  RFC 8259 has no
        # syntax for NaN or the infinities, so they cannot reach the encoder
        # through the parse path; they are counted and skipped, which is
        # review observation OBS-2 made explicit.
        if value != value or value in (float("inf"), float("-inf")):
            nonfinite += 1
            continue
        tested += 1
        mine = encoder.frame("number", encoder.number_payload(value))
        theirs = head_module.jx_canon(value)
        if mine != theirs:
            mismatches.append((value, mine, theirs))
    result = {"tested": tested, "nonfinite": nonfinite,
              "mismatches": len(mismatches), "examples": mismatches[:3]}
    _ORACLE["result"] = result
    return result


# --------------------------------------------------------------------------
# the context every gate reads
# --------------------------------------------------------------------------
class Context:
    def __init__(self, subject, report, register):
        self.subject = subject
        self.report = report
        self.register = register
        self.effective, self.chain, self.measured_digests = resolve(subject)
        if "documentIdentityEncoding" not in self.effective:
            raise Refused("the effective contract carries no "
                          "documentIdentityEncoding; this instrument cannot "
                          "encode from a contract that does not state the "
                          "encoding")
        self.spec = self.effective["documentIdentityEncoding"]
        self.encoder = ContractEncoder(self.spec)
        head_raw = verified_bytes("c2-plan-stage-schema.v9.json")
        self.head = parse_json(head_raw.decode("utf-8"),
                               "c2-plan-stage-schema.v9.json")
        self.head_pub = self.head["documentSkeleton"]
        # the EFFECTIVE PREDECESSOR: resolved, never read as a document.
        pred_raw = verified_bytes("c2-plan-stage-schema.v10.json")
        pred = parse_json(pred_raw.decode("utf-8"),
                          "c2-plan-stage-schema.v10.json")
        self.effective_predecessor, _c, _d = resolve(pred)
        self.pred_spec = self.effective_predecessor.get(
            "documentIdentityEncoding", {})

    def doc(self, label):
        return self.subject if label == DOC_SUBJECT else self.effective


# --------------------------------------------------------------------------
# L3  derivation
# --------------------------------------------------------------------------
def gate_derivation(ctx):
    report, subject = ctx.report, ctx.subject
    report.say("L3 derivation")
    report.say("  chain            : " + " -> ".join(["(subject)"] + ctx.chain))
    report.say("  depth            : %d" % len(ctx.chain))
    report.say("  every predecessor hash-verified before parse: yes")
    if not ctx.chain:
        report.finding("C2V12-NO-DERIVATION", "(root)",
                       "the subject declares no derivation; this instrument's "
                       "subject is a delta document")
    completeness = load_pinned_module("check-completeness.py", "_cc_v12")
    other_decl, other_errs = completeness.derivation_declaration(subject)
    if other_errs:
        report.finding("C2V12-RESOLVER-DISAGREE", "derivedFrom",
                       "check-completeness.py reports " + "; ".join(other_errs))
    elif other_decl is not None:
        other_eff, _prov, other_resolve_errs = completeness.resolve_derivation(
            "artifacts/" + SUBJECT, other_decl)
        if other_resolve_errs:
            report.finding("C2V12-RESOLVER-DISAGREE", "derivedFrom",
                           "; ".join(other_resolve_errs))
        elif not exact_equal(other_eff, ctx.effective):
            report.finding("C2V12-RESOLVER-DISAGREE", "derivedFrom",
                           "this instrument's resolver and check-completeness.py "
                           "materialise DIFFERENT effective contracts")
        else:
            report.say("  second resolver  : check-completeness.py agrees, type-exact")
    report.say()


# --------------------------------------------------------------------------
# L4  the encoding, implemented from the contract text
# --------------------------------------------------------------------------
def _corpus_gate(ctx, position, published_values, recomputed_values):
    """Requirement: a reproduction is not evidence if the corpus is constant."""
    pop_p, distinct_p, modal_p = degeneracy(published_values)
    pop_r, distinct_r, modal_r = degeneracy(recomputed_values)
    if pop_p >= 2 and distinct_p < 2:
        ctx.report.finding(
            "C2V12-DEGENERATE-CORPUS", position,
            "%d published values collapse to %d distinct value; agreeing with "
            "a constant corpus is not evidence" % (pop_p, distinct_p))
    if distinct_r != distinct_p:
        ctx.report.finding(
            "C2V12-DEGENERATE-CORPUS", position,
            "published values hold %d distinct entries, recomputed values hold "
            "%d; the agreement is degenerate on one side" % (distinct_p, distinct_r))
    return pop_p, distinct_p, modal_p


def gate_encoding(ctx, expect_own_digest=True):
    report, encoder = ctx.report, ctx.encoder
    report.say("L4 opensip-jx-canon-v1, implemented from the contract text")
    problems = encoder.obligations()
    for problem in problems:
        report.finding("C2V12-ENCODING-PROSE", "documentIdentityEncoding", problem)
    report.say("  prose obligations: %d checked, %d unmet"
               % (len(PROSE_OBLIGATIONS) + 7, len(problems)))
    report.say("  no copy of jx_canon is imported or vendored for this gate")

    head, head_pub = ctx.head, ctx.head_pub
    got = encoder.skeleton_digest(head)
    if got != head_pub["sha256"]:
        report.finding("C2V12-HEAD-SKELETON", "c2-plan-stage-schema.v9.json"
                       ".documentSkeleton.sha256",
                       "recomputed %s, published %s" % (got, head_pub["sha256"]))
    published_subtrees, recomputed_subtrees, differing = [], [], []
    for name, want in head_pub["subtrees"].items():
        mine = encoder.skeleton_digest(head[name])
        published_subtrees.append(want)
        recomputed_subtrees.append(mine)
        if mine != want:
            differing.append(name)
    for name in differing:
        report.finding("C2V12-HEAD-SUBTREE",
                       "c2-plan-stage-schema.v9.json.documentSkeleton.subtrees."
                       + name, "recomputed digest differs from published")
    report.say("  head documentSkeleton.sha256 reproduced: %s"
               % ("yes" if got == head_pub["sha256"] else "NO"))
    pop, distinct, modal = _corpus_gate(
        ctx, "c2-plan-stage-schema.v9.json.documentSkeleton.subtrees",
        published_subtrees, recomputed_subtrees)
    report.say("  head root-subtree digests    : %d/%d reproduced, %d differing"
               % (pop - len(differing), pop, len(differing)))
    report.say("  head corpus non-degeneracy   : %d published, %d DISTINCT, "
               "modal multiplicity %d" % (pop, distinct, modal))
    head_counts = encoder.counts(head)
    bad_counts = [k for k, v in head_counts.items() if head_pub.get(k) != v]
    for key in bad_counts:
        report.finding("C2V12-HEAD-COUNT",
                       "c2-plan-stage-schema.v9.json.documentSkeleton." + key,
                       "recomputed %s, published %s"
                       % (head_counts[key], head_pub.get(key)))
    report.say("  head node/leaf counters      : %d/%d reproduced"
               % (len(head_counts) - len(bad_counts), len(head_counts)))
    if head_counts["distinctPathTokens"] != head_counts["nodes"]:
        report.finding("C2V12-DEGENERATE-CORPUS",
                       "c2-plan-stage-schema.v9.json.documentSkeleton"
                       ".distinctPathTokens",
                       "%d nodes share only %d distinct path tokens, so the "
                       "skeleton is not injective over paths"
                       % (head_counts["nodes"], head_counts["distinctPathTokens"]))

    subject = ctx.subject
    if "documentSkeleton" in subject:
        own = subject["documentSkeleton"]
        got_own = encoder.skeleton_digest(subject)
        if expect_own_digest and got_own != own.get("sha256"):
            report.finding("C2V12-OWN-SKELETON", "documentSkeleton.sha256",
                           "recomputed %s, published %s"
                           % (got_own, own.get("sha256")))
        ctx.register.note(DOC_SUBJECT, "documentSkeleton.sha256")
        pub_own, rec_own, bad = [], [], []
        for name, want in own.get("subtrees", {}).items():
            mine = encoder.skeleton_digest(subject[name])
            pub_own.append(want)
            rec_own.append(mine)
            ctx.register.note(DOC_SUBJECT, "documentSkeleton.subtrees." + name)
            if mine != want:
                bad.append(name)
        for name in bad:
            report.finding("C2V12-OWN-SUBTREE",
                           "documentSkeleton.subtrees." + name,
                           "recomputed digest differs from published")
        ctx.register.bind(DOC_SUBJECT, subject, "documentSkeleton.rootSubtrees",
                          len(own.get("subtrees", {})),
                          "a count of the subtree digests this document "
                          "publishes", code="C2V12-OWN-COUNT")
        own_counts = encoder.counts(subject)
        bad_own = []
        for key, value in own_counts.items():
            if not ctx.register.bind(DOC_SUBJECT, subject,
                                     "documentSkeleton." + key, value,
                                     "recomputation of this document's own nodes",
                                     code="C2V12-OWN-COUNT"):
                bad_own.append(key)
        pop2, distinct2, modal2 = _corpus_gate(
            ctx, "documentSkeleton.subtrees", pub_own, rec_own)
        report.say("  subject documentSkeleton     : %s, subtrees %d/%d, counters %d/%d"
                   % ("reproduced" if got_own == own.get("sha256") else "DIFFERS",
                      pop2 - len(bad), pop2,
                      len(own_counts) - len(bad_own), len(own_counts)))
        report.say("  subject corpus non-degeneracy: %d published, %d DISTINCT, "
                   "modal multiplicity %d" % (pop2, distinct2, modal2))
        report.say("  this is the gate that makes documentSkeleton.fixpointNote")
        report.say("  HARD: the fixpoint itself cannot detect an edited digest")
        report.say("  string, because path and type are unchanged; recomputation can.")
    report.say()


# --------------------------------------------------------------------------
# L5  the encoding's own vectors -- INPUTS and EXPECTATIONS from the contract
# --------------------------------------------------------------------------
BINARY64_RE = re.compile(r"the binary64 value (\S+?)[\s,.]*$")


def _binary64_input(text):
    if not isinstance(text, str):
        return None
    match = BINARY64_RE.search(flat(text))
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _vector_assertions(ctx, vector):
    """(label, computed, published_key) triples for one contract vector.

    Wherever the contract states the INPUT machine-readably -- FF-1's `input`,
    FF-2's `input`, FF-3's step arrays, FF-4's and FF-5's inputs, and every
    FF-N's prose "the binary64 value X" -- the input is taken FROM THE CONTRACT.
    Only where the input is named rather than stated (FF-6's integer/number/
    boolean one, FF-7's degenerate forms) is it supplied here, and even then the
    EXPECTED TOKEN is always read from the contract and never typed.
    """
    encoder = ctx.encoder
    out = []
    vid = vector.get("id", "")
    if vid.startswith("FF-1") or vid.startswith("FF-2"):
        out.append((vid, encoder.canon(vector["input"]), "underThisText"))
    elif vid.startswith("FF-3"):
        out.append((vid + "A", encoder.canon(vector["inputStepsArrayA"]),
                    "underThisTextA"))
        out.append((vid + "B", encoder.canon(vector["inputStepsArrayB"]),
                    "underThisTextB"))
    elif vid.startswith("FF-4"):
        out.append((vid + "A", encoder.canon(vector["inputA"]), "underThisTextA"))
        out.append((vid + "B", encoder.canon(vector["inputB"]), "underThisTextB"))
    elif vid.startswith("FF-5"):
        out.append((vid + "A", encoder.skeleton_digest(vector["inputA"]),
                    "skeletonDigestA"))
        out.append((vid + "B", encoder.skeleton_digest(vector["inputB"]),
                    "skeletonDigestB"))
    elif vid.startswith("FF-6"):
        out.append((vid + "-integerOne", encoder.canon(1), "integerOne"))
        out.append((vid + "-numberOne", encoder.canon(1.0), "numberOne"))
        out.append((vid + "-booleanTrue", encoder.canon(True), "booleanTrue"))
    elif vid.startswith("FF-7"):
        out.append((vid + "-emptyString", encoder.canon(""), "emptyString"))
        out.append((vid + "-emptyArray", encoder.canon([]), "emptyArray"))
        out.append((vid + "-emptyObject", encoder.canon({}), "emptyObject"))
        out.append((vid + "-null", encoder.canon(None), "null"))
        out.append((vid + "-ten", encoder.canon("0123456789"),
                    "tenCharacterString"))
    elif vid.startswith("FF-N"):
        for suffix in ("", "A", "B"):
            value = _binary64_input(vector.get("input" + suffix))
            if value is None:
                continue
            out.append((vid + suffix, encoder.canon(value),
                        "underThisText" + suffix))
    return out


def gate_vectors(ctx):
    report, encoder, spec = ctx.report, ctx.encoder, ctx.spec
    report.say("L5 the encoding's own vectors, recomputed -- inputs AND")
    report.say("   expectations read from the contract, not typed here")
    families = [("documentIdentityEncoding.vectors", spec.get("vectors", [])),
                ("documentIdentityEncoding.numberProduction.vectors",
                 spec.get("numberProduction", {}).get("vectors", []))]
    total = failures = 0
    published_all, computed_all = [], []
    degenerate = 0
    for base, vectors in families:
        for index, vector in enumerate(vectors):
            where = "%s[%d]" % (base, index)
            assertions = _vector_assertions(ctx, vector)
            if not assertions:
                report.finding("C2V12-VECTOR", where,
                               "vector %r states no assertion this instrument "
                               "can recompute; a vector that cannot be executed "
                               "is prose" % vector.get("id"))
                continue
            computed = []
            for label, value, key in assertions:
                total += 1
                ctx.register.note(DOC_EFFECTIVE, where + "." + key)
                want = vector.get(key, MISSING)
                if want is MISSING:
                    failures += 1
                    report.finding("C2V12-VECTOR", where + "." + key,
                                   "the vector no longer publishes the value "
                                   "%s pins" % label)
                    continue
                published_all.append(want)
                computed_all.append(value)
                computed.append(value)
                if value != want:
                    failures += 1
                    report.finding("C2V12-VECTOR", where + "." + key,
                                   "recomputed %r, contract states %r"
                                   % (value, want))
            # separation, RE-DERIVED.  A vector that claims to separate two
            # readings and does not is a vector that cannot fail.
            rejected = [v for k, v in vector.items()
                        if k.startswith("underTheRejectedReading")
                        and isinstance(v, str) and TOKEN_RE.match(v)]
            derived = (bool(rejected) and all(r not in computed for r in rejected)) \
                or len(set(computed)) >= 2
            if "separates" in vector:
                ctx.register.note(DOC_EFFECTIVE, where + ".separates")
                if vector["separates"] is not derived:
                    degenerate += 1
                    report.finding(
                        "C2V12-VECTOR-DEGENERATE", where + ".separates",
                        "the vector publishes separates=%r; re-derived from its "
                        "own inputs and rejected readings it is %r"
                        % (vector["separates"], derived))
    report.say("  %d vector assertions recomputed from the contract, %d failing"
               % (total, failures))
    pop, distinct, modal = _corpus_gate(
        ctx, "documentIdentityEncoding vector corpus", published_all, computed_all)
    report.say("  vector corpus non-degeneracy : %d values, %d DISTINCT, "
               "modal multiplicity %d" % (pop, distinct, modal))
    report.say("  vectors whose published `separates` was re-derived: %d, %d wrong"
               % (sum(len(v) for _b, v in families), degenerate))
    # FF-6 is law 18 itself: the three tokens must be pairwise distinct.
    trio = {encoder.canon(1), encoder.canon(1.0), encoder.canon(True)}
    if len(trio) != 3:
        report.finding("C2V12-LAW18-COLLAPSE", "documentIdentityEncoding",
                       "1, 1.0 and true do not produce three distinct tokens")
    report.say("  law 18: 1, 1.0 and true produce %d distinct tokens (must be 3)"
               % len(trio))
    for vector in spec.get("vectors", []):
        if not vector.get("id", "").startswith("FF-6"):
            continue
        base = "documentIdentityEncoding.vectors[%d]" % spec["vectors"].index(vector)
        ctx.register.bind(DOC_EFFECTIVE, ctx.effective, base + ".distinctTokens",
                          len(trio), "recomputation of the three tokens")
        ctx.register.bind(DOC_EFFECTIVE, ctx.effective,
                          base + ".hostEqualityWouldConflateAllThree",
                          1 == 1.0 == True,
                          "host equality applied to 1, 1.0 and true")
    report.say()


# --------------------------------------------------------------------------
# L6  EPC-V2, executed
# --------------------------------------------------------------------------
def gate_epc(ctx):
    report = ctx.report
    report.say("L6 EPC-V2, EXECUTED")
    ruling = (ctx.effective.get("planIntent", {}).get("attemptAndExecutionJoin", {})
              .get("executionPlanCommitment"))
    if not isinstance(ruling, dict):
        report.skip("EPC-V2",
                    "the effective contract carries no "
                    "planIntent.attemptAndExecutionJoin.executionPlanCommitment "
                    "ruling, so there is no rule to execute")
        report.say()
        return
    golden = None
    for vector in ruling.get("vectors", []):
        if "planIntentCommitmentBothArms" in vector:
            golden = vector["planIntentCommitmentBothArms"]
    if golden is None or not SHA256ID_RE.match(str(golden)):
        report.skip("EPC-V2",
                    "no published sha256Id golden could be read out of the "
                    "ruling's own vectors, so the witnesses would be this "
                    "instrument's invention rather than the contract's")
        report.say()
        return
    cases = epc_witnesses(golden)
    failed = 0
    verdicts = []
    for name, record, expected, why in cases:
        verdict, reasons = epc_decide(record)
        verdicts.append(verdict)
        if verdict != expected:
            failed += 1
            report.finding("C2V12-EPC", name,
                           "expected %s (%s), got %s%s"
                           % (expected, why, verdict,
                              "; " + "; ".join(reasons) if reasons else ""))
        elif verdict == "REJECT" and not reasons:
            failed += 1
            report.finding("C2V12-EPC-UNNAMED", name,
                           "rejected without naming a position")
    report.say("  witnesses executed          : %d" % len(cases))
    report.say("  failing                     : %d" % failed)
    if len(set(verdicts)) < 2:
        report.finding("C2V12-DEGENERATE-CORPUS", "EPC-V2 witness suite",
                       "all %d witnesses receive the verdict %r; a suite that "
                       "cannot produce both verdicts tests nothing"
                       % (len(verdicts), verdicts[0] if verdicts else None))
    report.say("  verdicts present            : %s"
               % ", ".join(sorted(set(verdicts))))
    differ = epc_decide({POSITIONS[0]: golden,
                         POSITIONS[1]: "sha256:" + "1" * 64})[0]
    agree_wrong = epc_decide({POSITIONS[0]: "sha256:" + "1" * 64,
                              POSITIONS[1]: "sha256:" + "1" * 64})[0]
    report.say("  differing positions         : %s" % differ)
    report.say("  agreeing-but-not-golden     : %s" % agree_wrong)
    if differ == agree_wrong:
        report.finding("C2V12-EPC-DEGENERATE",
                       "planIntent.attemptAndExecutionJoin.executionPlanCommitment",
                       "differing positions and agreeing-but-wrong positions "
                       "receive the SAME verdict, so this procedure is "
                       "golden-drift detection and not the EPC-V2 control")
    else:
        report.say("  DISCRIMINATED: the two readings receive different")
        report.say("  verdicts, which is the named condition the v10")
        report.say("  review measured at 0 hits.")
    # The closed envelope, re-derived rather than believed.  This is the premise
    # the whole fixture/quantifier distinction rests on.
    plan = ctx.effective.get("executionPlan", {})
    required = plan.get("requiredFields")
    ctx.register.bind(DOC_EFFECTIVE, ctx.effective, "executionPlan.closedTopLevel",
                      True, "the envelope's own marker, matched by identity")
    if isinstance(required, list):
        ctx.register.note(DOC_EFFECTIVE, "executionPlan.requiredFields")
        carries = "executionPlanCommitment" in json.dumps(plan)
        report.say("  closed envelope re-derived  : requiredFields holds %d "
                   "members, executionPlanCommitment %s"
                   % (len(required), "PRESENT" if carries else "absent"))
        if carries:
            report.finding("C2V12-EPC", "executionPlan",
                           "the block names executionPlanCommitment, which "
                           "contradicts the unexpressibility premise the "
                           "quantifier reading rests on")
    report.say("  scope: executed over GENERATED witnesses. C-2's")
    report.say("  ExecutionPlan envelope is closed and cannot carry")
    report.say("  executionPlanCommitment, so this is NOT executed over")
    report.say("  a live ActivationManifestV1/EvaluationAuthoritySealV1/")
    report.say("  TerminalRunV1 record and does NOT discharge the freeze")
    report.say("  section 7.1 row.")
    report.say()


# --------------------------------------------------------------------------
# L7  law 18 exact-type admission
# --------------------------------------------------------------------------
def gate_law18(ctx):
    report = ctx.report
    report.say("L7 section 6 law 18, exact-type admission")
    defects = 0
    for probe, other in ((1, 1.0), (1, True), (0, False), (1.0, True)):
        if exact_equal(probe, other):
            defects += 1
            report.finding("C2V12-LAW18", "exact_equal",
                           "%r and %r compare equal type-exactly" % (probe, other))
        if not exact_equal(probe, probe):
            defects += 1
            report.finding("C2V12-LAW18", "exact_equal",
                           "%r is not equal to itself" % (probe,))
    report.say("  type-exact comparison primitive: %d defects" % defects)
    declaration = find_declaration(ctx.subject)
    operations = declaration["operations"] if declaration else []
    sets = [o for o in operations if o.get("op") == "set"]
    report.say("  set operations whose `from` was type-exactly verified: %d"
               % len(sets))
    ctx.register.bind(DOC_SUBJECT, ctx.subject, "operationAccounting.total",
                      len(operations),
                      "a count of the derivation's own operation list")
    report.say()


# --------------------------------------------------------------------------
# L8  census, from the pinned measurement function
# --------------------------------------------------------------------------
def gate_census(ctx):
    report = ctx.report
    report.say("L8 hostileScalarLeafTotality.contractRoot census")
    c2v4 = load_pinned_module("check-c2-v4.py", "_c2v4_v12")
    measured = c2v4.node_census(ctx.effective, c2v4.CONTRACT_HOSTILE_VALUES)
    published = ctx.effective.get("hostileScalarLeafTotality", {}).get("contractRoot", {})
    bad = 0
    for key, value in measured.items():
        have = published.get(key)
        ctx.register.note(DOC_EFFECTIVE,
                          "hostileScalarLeafTotality.contractRoot." + key)
        if type(have) is not type(value) or have != value:
            bad += 1
            report.finding("C2V12-CENSUS",
                           "hostileScalarLeafTotality.contractRoot." + key,
                           "recomputed %r, published %r" % (value, have))
    report.say("  counters recomputed by the pinned node_census: %d, %d differing"
               % (len(measured), bad))
    # Which counters MOVED is itself a published claim, and it is re-derivable
    # by running the same census over the EFFECTIVE PREDECESSOR.
    before = c2v4.node_census(ctx.effective_predecessor,
                              c2v4.CONTRACT_HOSTILE_VALUES)
    moved = sorted(k for k in measured if before.get(k) != measured[k])
    stood = sorted(k for k in measured if before.get(k) == measured[k])
    ctx.register.bind_membership(
        DOC_SUBJECT, ctx.subject, "operationAccounting.countersThatMoved",
        moved, "the same census run over the effective predecessor")
    ctx.register.bind_membership(
        DOC_SUBJECT, ctx.subject, "operationAccounting.countersThatDidNotMove",
        stood, "the same census run over the effective predecessor")
    report.say("  counters that moved v10 -> v11, re-derived: %d" % len(moved))
    report.say("  counters that stood, re-derived            : %d" % len(stood))
    report.say()


# --------------------------------------------------------------------------
# L9  closure marks, re-derived
# --------------------------------------------------------------------------
LOOSE_CLOSURE_KEYS = ("admitThenCommitClosure", "closedJsonTypes",
                      "closedTaggedUnion", "closure", "step1ClosedEnvelope")


def _closure_marks(root):
    marks = []

    def walk(node, steps):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("closed", "closedTopLevel") and value is True:
                    marks.append(render_path(steps) or "(root)")
                walk(value, steps + (key,))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, steps + (index,))

    walk(root, ())
    return marks


def _loose_closure_objects(root):
    out = []

    def walk(node, steps):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in LOOSE_CLOSURE_KEYS:
                    out.append(render_path(steps) or "(root)")
                walk(value, steps + (key,))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, steps + (index,))

    walk(root, ())
    return out


def gate_closure(ctx):
    report, subject = ctx.report, ctx.subject
    report.say("L9 closure marks, re-derived")
    raw = _closure_marks(ctx.effective)
    marks = sorted(set(raw))
    loose = sorted(set(_loose_closure_objects(ctx.effective)) | set(marks))
    if len(raw) != len(marks):
        report.finding("C2V12-DEGENERATE-CORPUS", "theClosureCount.members",
                       "the re-derived closure set holds %d marks at %d "
                       "distinct paths" % (len(raw), len(marks)))
    # The count, the member list, and the looser reading the definition names,
    # all bound to this run's re-derivation.
    for label, root, prefix in ((DOC_SUBJECT, subject, "theClosureCount"),
                                (DOC_SUBJECT, subject,
                                 "selfVerification.preservedByteForByte")):
        if prefix == "theClosureCount":
            ctx.register.bind(label, root, prefix + ".compared", len(marks),
                              "a walk of the resolved effective contract",
                              code="C2V12-CLOSURE")
            ctx.register.bind(label, root, prefix + ".identical", len(marks),
                              "the same walk, compared token-wise against the "
                              "effective predecessor", code="C2V12-CLOSURE")
            ctx.register.bind_membership(label, root, prefix + ".members", marks,
                                         "the enumerated re-derivation",
                                         code="C2V12-CLOSURE-MEMBERS")
        else:
            ctx.register.bind(label, root, prefix + ".closedCollectionsCompared",
                              len(marks), "a walk of the resolved effective "
                              "contract", code="C2V12-CLOSURE")
            ctx.register.bind(label, root, prefix + ".closedCollectionsIdentical",
                              len(marks), "the same walk", code="C2V12-CLOSURE")
            ctx.register.bind_membership(
                label, root, prefix + ".closedCollectionMembers", marks,
                "the enumerated re-derivation", code="C2V12-CLOSURE-MEMBERS")
    # `identical` says each marked object canonicalises the same in both
    # effective contracts.  That is a measurement, so it is measured.
    identical = 0
    for mark in marks:
        left = dotted_get(ctx.effective_predecessor, mark)
        right = dotted_get(ctx.effective, mark)
        if left is not MISSING and right is not MISSING and \
                ctx.encoder.canon(left) == ctx.encoder.canon(right):
            identical += 1
    if identical != len(marks):
        report.finding("C2V12-CLOSURE", "theClosureCount.identical",
                       "%d of %d closure-marked objects canonicalise "
                       "identically against the effective predecessor"
                       % (identical, len(marks)))
    report.say("  closure-marked objects re-derived : %d (all distinct paths)"
               % len(marks))
    report.say("  token-identical against effective v10: %d" % identical)
    report.say("  the looser reading the definition names, re-derived: %d"
               % len(loose))
    ctx.closure_count = len(marks)
    ctx.loose_closure_count = len(loose)
    report.say()


# --------------------------------------------------------------------------
# L10  the six live 1.0 leaves, RE-DERIVED     <- review observation OBS-4
# --------------------------------------------------------------------------
def gate_six_live(ctx):
    """The candidate's headline correction, measured instead of read.

    The predecessor accepted a fabricated list here three separate ways: one
    entry replaced by a nonexistent path, one entry replaced by a REAL path that
    holds 1.5, and all six replaced with inventions inside the operation
    payload.  All three ran green.  theClosureCount.whyABareCountIsTheDefect
    says "Enumeration is what makes it a measurement" -- so this enumeration is
    now measured, by the same standard the artifact applies to the other one.
    """
    report = ctx.report
    report.say("L10 theSixLiveOnePointZeroLeaves, RE-DERIVED (review OBS-4)")
    floats = [(render_path(p), v) for p, v in walk_leaves(ctx.effective)
              if type(v) is float]
    ones = [p for p, v in floats if v == 1.0]
    not_ones = [(p, v) for p, v in floats if v != 1.0]
    # A third, independent method: token equality under the very encoding the
    # repair restates.  If the encoder and the typed walk disagreed, the count
    # would be unsafe to publish at all.
    one_token = ctx.encoder.canon(1.0)
    by_token = [render_path(p) for p, v in walk_leaves(ctx.effective)
                if type(v) is float and ctx.encoder.canon(v) == one_token]
    if sorted(by_token) != sorted(ones):
        report.finding("C2V12-SIX-LIVE", "documentIdentityEncoding"
                       ".numberProduction.theSixLiveOnePointZeroLeaves",
                       "a typed walk and token equality under this contract's "
                       "own encoding disagree about which float leaves are 1.0")
    path = "documentIdentityEncoding.numberProduction.theSixLiveOnePointZeroLeaves"
    ctx.register.note(DOC_EFFECTIVE, path)
    published = dotted_get(ctx.effective, path)
    report.say("  float leaves of the effective contract : %d" % len(floats))
    report.say("  of which exactly 1.0                   : %d" % len(ones))
    report.say("  of which are not 1.0                   : %d  (%s)"
               % (len(not_ones),
                  ", ".join("%s = %r" % (p, v) for p, v in not_ones) or "none"))
    if published is MISSING or not isinstance(published, list):
        report.finding("C2V12-CLAIM-ABSENT", path,
                       "the enumeration this instrument re-derives is absent or "
                       "is not a list; a gate whose subject can be deleted is "
                       "not a gate")
    else:
        duplicates = len(published) - len(set(published))
        if duplicates:
            report.finding("C2V12-SIX-LIVE", path,
                           "%d duplicate entries; an enumeration that repeats "
                           "itself is not a census" % duplicates)
        extra = sorted(set(published) - set(ones))
        missing = sorted(set(ones) - set(published))
        for entry in extra:
            value = dotted_get(ctx.effective, entry)
            report.finding(
                "C2V12-SIX-LIVE", path,
                "enumerated path %r is not a float leaf equal to 1.0 in the "
                "resolved effective contract; it holds %r (%s)"
                % (entry, value,
                   "absent" if value is MISSING else type(value).__name__))
        for entry in missing:
            report.finding(
                "C2V12-SIX-LIVE", path,
                "float leaf %r is exactly 1.0 in the resolved effective "
                "contract and is NOT enumerated" % entry)
        if len(published) != len(ones):
            report.finding("C2V12-SIX-LIVE", path,
                           "the enumeration holds %d entries; the re-derivation "
                           "finds %d" % (len(published), len(ones)))
        report.say("  enumerated                             : %d" % len(published))
        report.say("  symmetric difference against the walk  : %d"
                   % (len(extra) + len(missing)))
        report.say("  document order preserved               : %s"
                   % ("yes" if list(published) == ones else "no"))
    ctx.float_total = len(floats)
    ctx.float_ones = len(ones)
    ctx.float_not_ones = len(not_ones)
    report.say()


# --------------------------------------------------------------------------
# L11  digests the artifact says it measured -- MEASURED
# --------------------------------------------------------------------------
def gate_digests(ctx):
    """review observation OBS-5.

    The candidate publishes a table of three predecessor digests it says it
    measured, and a list of recorded inputs with a digest each.  The predecessor
    instrument held all three predecessor digests in its own PINS table and
    never compared them: replacing the recorded v9 digest with sixty-four 1s ran
    green.  Here every published digest is compared against the bytes it names.
    """
    report, subject = ctx.report, ctx.subject
    report.say("L11 published digests, MEASURED against the named bytes "
               "(review OBS-5)")
    table_path = "selfVerification.measuredPredecessorDigests"
    published = dotted_get(subject, table_path)
    ctx.register.note(DOC_SUBJECT, table_path)
    expected = {"artifacts/" + name: digest
                for name, digest in ctx.measured_digests.items()}
    if published is MISSING or not isinstance(published, dict):
        report.finding("C2V12-CLAIM-ABSENT", table_path,
                       "the self-reported predecessor digest table is absent")
    else:
        for name in sorted(set(published) | set(expected)):
            if name not in expected:
                report.finding("C2V12-PREDECESSOR-DIGEST",
                               table_path + "." + name,
                               "the table names %r, which is not on the chain "
                               "this run resolved (%s)"
                               % (name, ", ".join(sorted(expected))))
            elif name not in published:
                report.finding("C2V12-PREDECESSOR-DIGEST", table_path,
                               "the chain this run resolved includes %r, which "
                               "the table omits" % name)
            elif published[name] != expected[name]:
                report.finding("C2V12-PREDECESSOR-DIGEST",
                               table_path + "." + name,
                               "published %r, this run measured %r of those "
                               "bytes" % (published[name], expected[name]))
        report.say("  predecessor digests compared          : %d" % len(expected))
    # every OTHER place the document states a digest for a file it names
    named = []
    for index, entry in enumerate(subject.get("recordedInputs", []) or []):
        if isinstance(entry, dict) and "path" in entry and "sha256" in entry:
            # the PRECISE leaf, so L17's coverage figure counts what is really
            # bound and not the `role` prose sitting beside it
            named.append(("recordedInputs[%d].sha256" % index,
                          entry["path"], entry["sha256"]))
    for path, key in (("bindingDeclaration.predecessorPath",
                       "bindingDeclaration.predecessorSha256"),
                      ("bindingDeclaration.headPath",
                       "bindingDeclaration.headSha256"),
                      ("derivedFrom.predecessor", "derivedFrom.predecessorSha256")):
        rel, digest = dotted_get(subject, path), dotted_get(subject, key)
        if isinstance(rel, str) and isinstance(digest, str):
            if "/" not in rel:
                rel = "artifacts/" + rel
            named.append((key, rel, digest))
    good = bad = unreadable = 0
    for where, rel, digest in named:
        measured, problem = declared_bytes(rel)
        if measured is None:
            unreadable += 1
            report.finding("C2V12-RECORDED-INPUT", "%s -> %s" % (where, rel),
                           "the document declares a digest for this path and "
                           "the path %s" % problem)
            continue
        ctx.register.note(DOC_SUBJECT, where)
        if measured != digest:
            bad += 1
            report.finding("C2V12-RECORDED-INPUT", "%s -> %s" % (where, rel),
                           "published %s, this run measured %s"
                           % (digest, measured))
        else:
            good += 1
    report.say("  declared paths whose digest was measured: %d, %d wrong, "
               "%d unreadable" % (good + bad, bad, unreadable))
    report.say("  (every read here is of a path the ARTIFACT names; no directory")
    report.say("   is enumerated and `os` is never imported)")
    report.say()


# --------------------------------------------------------------------------
# L12  the self-report register
# --------------------------------------------------------------------------
def _structural_diff(before, after):
    left = {render_path(p): v for p, v in walk_leaves(before)}
    right = {render_path(p): v for p, v in walk_leaves(after)}
    added = sorted(set(right) - set(left))
    removed = sorted(set(left) - set(right))
    changed = sorted(k for k in set(left) & set(right)
                     if not exact_equal(left[k], right[k]))
    return added, removed, changed


def gate_self_reports(ctx):
    """Every self-reported measurement this instrument can recompute.

    The escapes this closes: chainDepth 3 -> 9, leavesAdded 73 -> 7, and
    twoIndependentEncoders.encoderBReproducedIt true -> false all ran green
    against the predecessor.  Each is a claim ABOUT A MEASUREMENT, and a claim
    about a measurement can be settled by taking the measurement.
    """
    report, subject, effective = ctx.report, ctx.subject, ctx.effective
    register = ctx.register
    report.say("L12 self-reported measurements, recomputed")

    register.bind(DOC_SUBJECT, subject, "selfVerification.chainDepth",
                  len(ctx.chain), "the chain this run resolved")
    register.bind(DOC_SUBJECT, subject, "selfVerification.declarationErrors", 0,
                  "this run's declaration reading")
    register.bind(DOC_SUBJECT, subject, "selfVerification.resolveErrors", 0,
                  "this run's resolution")
    register.bind(DOC_SUBJECT, subject,
                  "selfVerification.everyPredecessorDigestVerifiedBeforeParse",
                  True, "this resolver, which hash-verifies before parsing")

    added, removed, changed = _structural_diff(ctx.effective_predecessor, effective)
    base = "selfVerification.structuralDiffAgainstTheEffectivePredecessor"
    register.bind(DOC_SUBJECT, subject, base + ".leavesAdded", len(added),
                  "a leaf-by-leaf diff against the effective predecessor")
    register.bind(DOC_SUBJECT, subject, base + ".leavesRemoved", len(removed),
                  "the same diff")
    register.bind(DOC_SUBJECT, subject, base + ".leavesChanged", len(changed),
                  "the same diff")
    register.bind_membership(DOC_SUBJECT, subject, base + ".changedLeafPaths",
                             changed, "the same diff, enumerated")
    register.bind_membership(
        DOC_SUBJECT, subject, base + ".newTopLevelKeys",
        sorted(set(effective) - set(ctx.effective_predecessor)),
        "top-level members present in the successor and not the predecessor")
    report.say("  structural diff re-derived   : +%d / -%d / ~%d leaves"
               % (len(added), len(removed), len(changed)))

    # the fixture arrays, and the goldens they hold
    preserved = "selfVerification.preservedByteForByte"
    arrays = dotted_get(subject, preserved + ".fiveFixtureArrays")
    if isinstance(arrays, dict):
        total = 0
        identical = True
        for name in arrays:
            here = effective.get(name)
            there = ctx.effective_predecessor.get(name)
            size = len(here) if isinstance(here, list) else MISSING
            register.bind(DOC_SUBJECT, subject,
                          preserved + ".fiveFixtureArrays." + name, size,
                          "a length measurement of the effective contract's "
                          "own array")
            if isinstance(size, int):
                total += size
            if not exact_equal(here, there):
                identical = False
        register.bind(DOC_SUBJECT, subject,
                      preserved + ".fiveFixtureArraysTotalGoldens", total,
                      "the sum of those measured lengths")
        register.bind(DOC_SUBJECT, subject,
                      preserved + ".fiveFixtureArraysIdentical", identical,
                      "a type-exact comparison of each array against the "
                      "effective predecessor")
        report.say("  five fixture arrays re-derived: %d goldens, identical to "
                   "the predecessor: %s" % (total, identical))

    # this document's OWN leaf census, published twice and checked nowhere
    census = {"nullLeaves": 0, "booleanLeaves": 0, "integerLeaves": 0,
              "numberLeaves": 0, "stringLeaves": 0}
    for _p, value in walk_leaves(subject):
        census[ContractEncoder.jtype(value) + "Leaves"] += 1
    leaf_base = "selfVerification.leafCensusOfTheseOwnBytes"
    for key, value in census.items():
        register.bind(DOC_SUBJECT, subject, leaf_base + "." + key, value,
                      "a typed walk of this document's own leaves")
    register.bind(DOC_SUBJECT, subject, leaf_base + ".noFloatLeaves",
                  census["numberLeaves"] == 0, "the same walk")
    register.bind(DOC_SUBJECT, subject, leaf_base + ".noNullLeaves",
                  census["nullLeaves"] == 0, "the same walk")
    report.say("  own leaf census re-derived   : %s"
               % ", ".join("%s %d" % (k[:-6], v) for k, v in sorted(census.items())))

    # the reproduction claims -- in the contract, and again in the subject
    got = ctx.encoder.skeleton_digest(ctx.head)
    subtrees = ctx.head_pub.get("subtrees", {})
    reproduced = sum(1 for n, w in subtrees.items()
                     if ctx.encoder.skeleton_digest(ctx.head[n]) == w)
    differing = len(subtrees) - reproduced
    head_ok = got == ctx.head_pub.get("sha256")
    repro = "documentIdentityEncoding.reproduction"
    for label, root, prefix, keys in (
            (DOC_EFFECTIVE, effective, repro,
             {"publishedDocumentSkeletonSha256": ctx.head_pub.get("sha256"),
              "subjectSha256": ctx.measured_digests.get(
                  "c2-plan-stage-schema.v9.json"),
              "encoderAReproducedIt": head_ok,
              "encoderBReproducedIt": head_ok,
              "rootSubtreeDigestsPublished": len(subtrees),
              "rootSubtreeDigestsReproduced": reproduced,
              "rootSubtreeDigestsDiffering": differing}),
            (DOC_SUBJECT, subject, "selfVerification.twoIndependentEncoders",
             {"headSkeletonDigestPublished": ctx.head_pub.get("sha256"),
              "encoderAReproducedIt": head_ok,
              "encoderBReproducedIt": head_ok,
              "rootSubtreeDigestsPublished": len(subtrees),
              "encoderAReproducedSubtrees": reproduced,
              "encoderBReproducedSubtrees": reproduced,
              "rootSubtreeDigestsDiffering": differing})):
        for key, value in keys.items():
            if dotted_get(root, prefix + "." + key) is MISSING:
                continue
            register.bind(label, root, prefix + "." + key, value,
                          "this run's own encoder, written from the contract "
                          "text alone")
    counters = dotted_get(effective, repro + ".publishedCountsAlsoReproduced")
    if isinstance(counters, dict):
        mine = ctx.encoder.counts(ctx.head)
        for key in counters:
            register.bind(DOC_EFFECTIVE, effective,
                          repro + ".publishedCountsAlsoReproduced." + key,
                          mine.get(key), "recomputation over the head")
    report.say("  reproduction self-reports    : head digest %s, subtrees "
               "%d/%d, differing %d"
               % ("reproduced" if head_ok else "NOT REPRODUCED",
                  reproduced, len(subtrees), differing))

    # the head instrument's structure, which the subject makes claims about
    head_module = load_pinned_module("check-c2-v9.py", "_c2v9_v12")
    head_source = verified_bytes("check-c2-v9.py").decode("utf-8")
    enumeration = {}
    for token in (r"os\.walk", r"\biterdir\b", r"\blistdir\b", r"\bscandir\b",
                  r"\brglob\b", r"\bglob\b"):
        enumeration[token] = len(re.findall(token, head_source))
    report.say("  head instrument, structurally: PINS %d entries, BINDING %r"
               % (len(getattr(head_module, "PINS", {})),
                  getattr(head_module, "BINDING", None)))
    report.say("    enumeration primitives present: %s"
               % (", ".join("%s=%d" % (t, c) for t, c in enumeration.items()
                            if c) or "none"))
    report.say("    `os` imported by it          : %s"
               % ("YES" if hasattr(head_module, "os") else "no"))
    report.say("    (\\bglob\\b is matched with word boundaries, so the keyword")
    report.say("     `global` cannot produce the false positive freeze section")
    report.say("     7.7 names; `global` occurs %d times and is not counted)"
               % len(re.findall(r"\bglobal\b", head_source)))
    if any(enumeration.values()) or hasattr(head_module, "os"):
        report.finding("C2V12-SELF-REPORT",
                       "theUnsoundStdoutEvidence.theStructuralProofAdopted",
                       "the structural proof asserts the head instrument "
                       "contains no directory enumeration, and this run finds "
                       "one")
    runtime_fields = getattr(head_module, "RUNTIME_ONLY_FIELDS", ())
    if "sweepElapsedSeconds" not in runtime_fields or \
            "{sweepElapsedSeconds} seconds" not in head_source:
        report.finding("C2V12-SELF-REPORT", "theUnsoundStdoutEvidence.confirmedHere",
                       "the claim that the head instrument's report embeds a "
                       "wall-clock field, and classifies it as runtime-varying, "
                       "is not confirmed by its bytes")
    ctx.head_pins = len(getattr(head_module, "PINS", {}))
    ctx.exercised_names = None

    # Word counts the document says it MEASURED over a pinned predecessor.
    # 'objection' 0, 'concede' 0, 'accommodation' 0 is a measurement over bytes
    # this instrument already holds, so it is taken rather than believed.
    finding_text = dotted_get(subject, "theFreezeMisattribution.finding")
    if isinstance(finding_text, str):
        register.note(DOC_SUBJECT, "theFreezeMisattribution.finding")
        pred_text = verified_bytes("c2-plan-stage-schema.v10.json").decode("utf-8")
        counted = 0
        for match in re.finditer(r"'([a-z]+)' (\d+)", flat(finding_text)):
            counted += 1
            word, stated = match.group(1), int(match.group(2))
            actual = pred_text.count(word)
            if actual != stated:
                report.finding(
                    "C2V12-SELF-REPORT", "theFreezeMisattribution.finding",
                    "the text states %r occurs %d times in the v10 bytes; this "
                    "run counts %d" % (word, stated, actual))
        report.say("  word counts over the pinned predecessor re-counted: %d"
                   % counted)

    # A named-but-absent path is a dead link in a binding artifact -- which is
    # the exact reason v10 declined to name one.  So the name is resolved.
    instrument_path = dotted_get(effective, "companionInstrument.path")
    if isinstance(instrument_path, str):
        for index, operation in enumerate(
                subject.get("derivedFrom", {}).get("operations", [])):
            if operation.get("path") == "companionInstrument":
                register.note(DOC_SUBJECT,
                              "derivedFrom.operations[%d].value.path" % index)
        register.note(DOC_EFFECTIVE, "companionInstrument.path")
        measured, problem = declared_bytes(instrument_path)
        report.say("  companionInstrument.path %r: %s"
                   % (instrument_path, "resolves" if measured else problem))
        if measured is None:
            report.finding("C2V12-SELF-REPORT", "companionInstrument.path",
                           "the contract names a companion instrument at %r "
                           "and the path %s; a named-but-absent path is the "
                           "dead link the block itself says it exists to avoid"
                           % (instrument_path, problem))

    # checkerModeContract, which the candidate says it did not repoint
    register.bind(DOC_EFFECTIVE, effective, "checkerModeContract.checker",
                  "check-c2-v9.py",
                  "a read of the resolved effective contract, which no "
                  "operation in this derivation touches")
    declaration = find_declaration(subject)
    touched = [o["path"] for o in (declaration["operations"] if declaration else [])
               if o.get("path", "").startswith("checkerModeContract")]
    if touched:
        report.finding("C2V12-SELF-REPORT",
                       "bindingDeclaration.checkerModeContractUntouched",
                       "operations touch checkerModeContract: " + ", ".join(touched))
    report.say()


# --------------------------------------------------------------------------
# L13  the number production: oracle, prose vectors, numerals
# --------------------------------------------------------------------------
WRITTEN_RE = re.compile(
    r"(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s+is\s+written\s+"
    r"(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")


def gate_number_production(ctx):
    """review observation OBS-6, and the 'Mismatches: ZERO' escape.

    Two things happen here.  First the restated rule is compared against the
    PINNED head primitive, so 'Mismatches: ZERO' becomes a number this run
    measured.  Second, every "X is written Y" the block states is EXECUTED: the
    prose stops being a phrase the encoder merely asserts is present and becomes
    a claim the encoder must satisfy.  Rewriting positionalForm to say "1.0 is
    written 1.00" ran green against the predecessor; it cannot here.
    """
    report, encoder = ctx.report, ctx.encoder
    report.say("L13 the number production, executed against the pinned primitive")
    result = number_oracle(encoder)
    report.say("  values compared against check-c2-v9.py's own number token: %d"
               % result["tested"])
    report.say("  non-finite bit patterns skipped (the rule is finite-only): %d"
               % result["nonfinite"])
    report.say("  MISMATCHES: %d" % result["mismatches"])
    for value, mine, theirs in result["examples"]:
        report.finding("C2V12-NUMBER-ORACLE",
                       "documentIdentityEncoding.numberProduction",
                       "for %r this text gives %r and the pinned primitive "
                       "gives %r" % (value, mine, theirs))
    report.say("  (this is the ONLY place the head's encoder is executed; it is")
    report.say("   an oracle for one production and never computes a skeleton")
    report.say("   digest, because reproducing the head's digests with the")
    report.say("   head's own encoder would show only that code equals itself)")
    ctx.oracle_mismatches = result["mismatches"]

    block = ctx.spec.get("numberProduction", {})
    pairs = wrong = 0
    for steps, value in walk_leaves(block):
        if not isinstance(value, str):
            continue
        where = ("documentIdentityEncoding.numberProduction."
                 + render_path(steps))
        for match in WRITTEN_RE.finditer(flat(value)):
            pairs += 1
            ctx.register.note(DOC_EFFECTIVE, where)
            try:
                given = float(match.group(1))
            except ValueError:
                continue
            mine = encoder.number_payload(given)
            if mine != match.group(2):
                wrong += 1
                report.finding(
                    "C2V12-PROSE-VECTOR", where,
                    "the prose states %r is written %r; this text's own rule "
                    "writes it %r" % (match.group(1), match.group(2), mine))
    report.say("  'X is written Y' pairs executed from the prose: %d, %d wrong"
               % (pairs, wrong))
    if pairs == 0:
        report.finding("C2V12-CLAIM-ABSENT",
                       "documentIdentityEncoding.numberProduction",
                       "the block states no executable 'X is written Y' pair; "
                       "the substance of the repair would rest on pinned "
                       "phrases alone")
    report.say()


# --------------------------------------------------------------------------
# L16  numerals stated in prose, bound to what this run measured
# --------------------------------------------------------------------------
def gate_numerals(ctx):
    report = ctx.report
    report.say("L16 numerals stated in prose, bound to this run's measurements")
    head_subtrees = len(ctx.head_pub.get("subtrees", {}))
    head_counters = len(ctx.encoder.counts(ctx.head))
    exercised, _unexercised = ctx.split_declared
    v10_raw = verified_bytes("c2-plan-stage-schema.v10.json").decode("utf-8")
    epcv_in_v10_bytes = v10_raw.count("EPC-V")
    epcv_in_effective_pred = sum(
        v.count("EPC-V") for _p, v in walk_leaves(ctx.effective_predecessor)
        if isinstance(v, str))

    # (scope, path or None, pattern, measured value, what the measurement is)
    rules = [
        ("*", None, r"([A-Za-z]+|\d+) root-subtree digests", head_subtrees,
         "the head's published subtree count"),
        ("*", None, r"chain of depth ([A-Za-z]+|\d+)", len(ctx.chain),
         "the chain this run resolved"),
        ("*", None, r"Mismatches: ([A-Za-z]+|\d+)", ctx.oracle_mismatches,
         "L13's comparison against the pinned primitive"),
        ("*", None, r"holds ([A-Za-z]+|\d+) such objects", ctx.closure_count,
         "L9's closure walk"),
        ("*", None, r"Counting them would give ([A-Za-z]+|\d+)",
         ctx.loose_closure_count, "L9's looser walk"),
        ("*", None, r"([A-Za-z]+|\d+) published node and leaf-type counters",
         head_counters, "the head counters this run recomputed"),
        ("*", None, r"exercises exactly ([A-Za-z]+|\d+) productions",
         len(exercised), "L15's perturbation of each production in turn"),
        ("*", None, r"PINS table, which holds ([A-Za-z]+|\d+) entries",
         ctx.head_pins, "the head instrument's own PINS mapping"),
        ("*", None, r"occurs ([A-Za-z]+|\d+) times in the v10 delta bytes",
         epcv_in_v10_bytes, "a count over the pinned v10 bytes"),
        ("*", None,
         r"and ([A-Za-z]+|\d+) times in the resolved effective contract",
         epcv_in_effective_pred,
         "a count over the EFFECTIVE PREDECESSOR contract, which is the "
         "contract that finding describes"),
        (DOC_EFFECTIVE,
         "documentIdentityEncoding.numberProduction.whereThisIsLive",
         r"carries ([A-Za-z]+|\d+) float leaves", ctx.float_total,
         "L10's typed walk"),
        (DOC_EFFECTIVE,
         "documentIdentityEncoding.numberProduction.whereThisIsLive",
         r"([A-Za-z]+|\d+) of them exactly 1\.0", ctx.float_ones, "L10"),
        (DOC_EFFECTIVE,
         "documentIdentityEncoding.numberProduction.whereThisIsLive",
         r"and ([A-Za-z]+|\d+) exactly 1\.5", ctx.float_not_ones, "L10"),
        (DOC_EFFECTIVE,
         "documentIdentityEncoding.numberProduction.aCountThisRepairCorrects",
         r"the count is ([A-Za-z]+|\d+)", ctx.float_ones, "L10"),
        (DOC_EFFECTIVE,
         "documentIdentityEncoding.numberProduction.aCountThisRepairCorrects",
         r"reports ([A-Za-z]+|\d+) float leaves in total", ctx.float_total, "L10"),
        (DOC_EFFECTIVE,
         "documentIdentityEncoding.numberProduction.aCountThisRepairCorrects",
         r"holds exactly ([A-Za-z]+|\d+) float leaves that are not 1\.0",
         ctx.float_not_ones, "L10"),
        (DOC_SUBJECT, "theNumberProductionDefect.liveLeaves",
         r"^([A-Za-z]+|\d+) float leaves", ctx.float_ones, "L10"),
        (DOC_SUBJECT, "theNumberProductionDefect.liveLeaves",
         r"and ([A-Za-z]+|\d+) more are 1\.5", ctx.float_not_ones, "L10"),
    ]
    checked = wrong = absent = 0
    for scope, path, pattern, measured, how in rules:
        compiled = re.compile(pattern)
        sites = []
        if scope == "*":
            for label in (DOC_SUBJECT, DOC_EFFECTIVE):
                for steps, value in walk_leaves(ctx.doc(label)):
                    if isinstance(value, str):
                        sites.append((label, render_path(steps), value))
        else:
            value = dotted_get(ctx.doc(scope), path)
            if value is MISSING or not isinstance(value, str):
                absent += 1
                ctx.report.finding("C2V12-CLAIM-ABSENT", "%s %s" % (scope, path),
                                   "a numeral claim this instrument binds to %s "
                                   "is absent" % how)
                continue
            sites.append((scope, path, value))
        hits = 0
        for label, where, text in sites:
            for match in compiled.finditer(flat(text)):
                hits += 1
                checked += 1
                ctx.register.note(label, where)
                stated = numeral(match.group(1))
                if stated != measured:
                    wrong += 1
                    ctx.report.finding(
                        "C2V12-NUMERAL", "%s %s" % (label, where),
                        "the text states %r where %s gives %r  (matched %r)"
                        % (match.group(1), how, measured, match.group(0)))
        if hits == 0:
            absent += 1
            ctx.report.finding(
                "C2V12-CLAIM-ABSENT", scope if scope != "*" else "(any leaf)",
                "the numeral claim %r is no longer stated anywhere; this "
                "instrument bound it to %s" % (pattern, how))
    report.say("  numeral claims bound to a measurement: %d sites, %d wrong, "
               "%d no longer stated" % (checked, wrong, absent))
    report.say("  one reading is declared rather than assumed: theEpcV2Control")
    report.say("  .finding's 'N times in the resolved effective contract' is")
    report.say("  read as the EFFECTIVE PREDECESSOR, because that finding")
    report.say("  describes the v10 state; measured there it is %d, and the"
               % epcv_in_effective_pred)
    report.say("  successor's own effective contract holds %d, which is the"
               % sum(v.count("EPC-V") for _p, v in walk_leaves(ctx.effective)
                     if isinstance(v, str)))
    report.say("  growth this candidate's own executability block causes.")
    report.say()


# --------------------------------------------------------------------------
# L14  the ruling's polarity, and L15 the declared production split
# --------------------------------------------------------------------------
SIDE_ALIASES = {"vector": "vector", "ff-6": "vector", "ff6": "vector",
                "production": "production"}
VERDICT_ALIASES = {"right": "right", "correct": "right",
                   "wrong": "wrong", "incorrect": "wrong"}
RULING_RE = re.compile(
    r"\b(vector|ff-6|ff6|production)\b[^.;:]{0,60}?\b(?:is|was|were|are)\s+"
    r"(right|correct|wrong|incorrect)\b", re.I)


def _ff6_number_one(spec):
    for vector in spec.get("vectors", []) or []:
        if isinstance(vector, dict) and vector.get("id", "").startswith("FF-6"):
            return vector.get("numberOne")
    return None


def gate_ruling_polarity(ctx):
    """The central ruling, bound to which side actually moved.

    "THE VECTOR IS RIGHT AND THE PRODUCTION WAS WRONG" reversed to its exact
    opposite ran green against the predecessor, in the subject's narrative and
    again inside the operation payload.  The required polarity is NOT typed
    here.  It is MEASURED: which of the two sides differs between the effective
    predecessor and the effective successor, and which of the two the pinned
    head primitive agrees with.  If the artifact had repaired the vector instead
    of the production, this gate would require the opposite polarity by itself.
    """
    report = ctx.report
    report.say("L14 the ruling's polarity, derived from which side moved")
    before_vector = _ff6_number_one(ctx.pred_spec)
    after_vector = _ff6_number_one(ctx.spec)
    before_production = dotted_get(ctx.pred_spec, "productions.number")
    after_production = dotted_get(ctx.spec, "productions.number")
    head_module = load_pinned_module("check-c2-v9.py", "_c2v9_v12")
    head_token = head_module.jx_canon(1.0)

    vector_moved = before_vector != after_vector
    production_moved = before_production != after_production
    instrument_agrees_with_vector = (head_token == after_vector)
    report.say("  FF-6 numberOne, effective v10 -> v11 : %s"
               % ("MOVED" if vector_moved else "unchanged"))
    report.say("  productions.number, effective v10 -> v11: %s"
               % ("MOVED" if production_moved else "unchanged"))
    report.say("  pinned check-c2-v9.py on the value 1.0 : %r" % head_token)
    report.say("  it agrees with the VECTOR              : %s"
               % instrument_agrees_with_vector)

    if not (production_moved and not vector_moved and instrument_agrees_with_vector):
        report.skip("C2V12-RULING-POLARITY",
                    "the direction of the repair could not be measured from the "
                    "two effective contracts and the pinned primitive "
                    "(vectorMoved=%r productionMoved=%r instrumentAgreesWith"
                    "Vector=%r), so no polarity is asserted rather than a "
                    "guessed one being enforced"
                    % (vector_moved, production_moved,
                       instrument_agrees_with_vector))
        report.say()
        return
    required = {"vector": "right", "production": "wrong"}
    report.say("  derived requirement                    : the %s is RIGHT and "
               "the %s was WRONG"
               % ("vector", "production"))
    stated = agreeing = disagreeing = 0
    for label in (DOC_SUBJECT, DOC_EFFECTIVE):
        for steps, value in walk_leaves(ctx.doc(label)):
            if not isinstance(value, str):
                continue
            where = render_path(steps)
            for match in RULING_RE.finditer(flat(value)):
                side = SIDE_ALIASES[match.group(1).lower()]
                verdict = VERDICT_ALIASES[match.group(2).lower()]
                stated += 1
                ctx.register.note(label, where)
                if required[side] == verdict:
                    agreeing += 1
                else:
                    disagreeing += 1
                    report.finding(
                        "C2V12-RULING-POLARITY", "%s %s" % (label, where),
                        "the text states %r, so it rules that the %s is %s; the "
                        "measurement above shows the %s is the side that moved "
                        "and the pinned instrument agrees with the %s"
                        % (match.group(0), side, verdict, "production", "vector"))
    if stated == 0:
        report.finding("C2V12-CLAIM-ABSENT", "(any leaf)",
                       "the document no longer states the ruling this "
                       "instrument binds to the measured direction of repair")
    report.say("  ruling verdicts found in prose         : %d, %d agreeing, "
               "%d contradicting the measurement" % (stated, agreeing, disagreeing))
    report.say()


def _declared_split(ctx):
    """Parse the declared 3-of-7 split OUT OF THE CONTRACT'S PROSE.

    The predecessor hard-coded ['array','integer','string'] into its selftest.
    That tests the transcription.  Here the two sets are read from
    exercisedByTheSkeletonDigest.measurement, so if the contract changed what it
    claims, the executed check would change with it.
    """
    names = list(ctx.spec.get("productions", {}))
    text = flat(str(dotted_get(ctx.spec,
                               "exercisedByTheSkeletonDigest.measurement")))
    marker = "does NOT exercise"
    head, _, tail = text.partition(marker)
    if not tail:
        return sorted(names), []
    exercised = sorted(n for n in names if re.search(r"\b%s\b" % n, head))
    unexercised = sorted(n for n in names if re.search(r"\b%s\b" % n, tail))
    return exercised, unexercised


def gate_split(ctx):
    """The 3-of-7 split, DERIVED from prose and EXECUTED by perturbation.

    A claim about which productions a measurement reaches is exactly the
    coverage-over-an-unobserved-region class this contract exists to refuse, so
    it is executed: each production's frame is perturbed in turn and the head's
    skeleton digest must move for the ones the contract says are exercised and
    stand for the ones it says are not.
    """
    report = ctx.report
    report.say("L15 the declared production split, derived and executed")
    ctx.split_declared = _declared_split(ctx)
    declared_exercised, declared_unexercised = ctx.split_declared
    reference = ctx.encoder.skeleton_digest(ctx.head)
    moved, stood = [], []
    for kind in ctx.spec.get("productions", {}):
        class Perturbed(ContractEncoder):
            def frame(self, k, payload, _kind=kind):
                if k == _kind:
                    return self.tags[k] + str(len(payload)) + ";" + payload
                return ContractEncoder.frame(self, k, payload)

        if Perturbed(ctx.spec).skeleton_digest(ctx.head) != reference:
            moved.append(kind)
        else:
            stood.append(kind)
    moved.sort()
    stood.sort()
    report.say("  contract declares exercised : %s" % declared_exercised)
    report.say("  perturbation moves the digest for: %s" % moved)
    report.say("  contract declares unexercised: %s" % declared_unexercised)
    report.say("  perturbation leaves it standing for: %s" % stood)
    ctx.register.note(DOC_EFFECTIVE,
                      "documentIdentityEncoding.exercisedByTheSkeletonDigest"
                      ".measurement")
    if declared_exercised != moved or declared_unexercised != stood:
        report.finding("C2V12-SPLIT",
                       "documentIdentityEncoding.exercisedByTheSkeletonDigest"
                       ".measurement",
                       "the contract declares exercised=%s unexercised=%s; "
                       "perturbing each production in turn gives moved=%s "
                       "stood=%s"
                       % (declared_exercised, declared_unexercised, moved, stood))
    if set(declared_exercised) & set(declared_unexercised) or \
            set(declared_exercised) | set(declared_unexercised) != \
            set(ctx.spec.get("productions", {})):
        report.finding("C2V12-SPLIT",
                       "documentIdentityEncoding.exercisedByTheSkeletonDigest"
                       ".measurement",
                       "the declared split does not partition the seven "
                       "productions")
    # The four the skeleton cannot reach are pinned by vectors instead; L5
    # re-derives every one of those vectors' separation, which is the
    # compensating control.  Extending the split coverage means saying which
    # vector carries which unexercised production.
    carriers = {"object": "FF-2", "number": "FF-6", "boolean": "FF-6",
                "null": "FF-7"}
    report.say("  unexercised productions are witnessed instead by: %s"
               % ", ".join("%s<-%s" % (k, carriers.get(k, "?"))
                           for k in declared_unexercised))
    report.say()


# --------------------------------------------------------------------------
# L17  the boundary, measured
# --------------------------------------------------------------------------
def gate_coverage(ctx):
    """Freeze section 7.8 records the escape class as the boundary of this whole
    instrument class.  A boundary that is described in prose is exactly the
    thing this corpus keeps failing to hold.  So it is MEASURED: how many leaves
    of the subject does this instrument actually bind to a value it computed,
    and which regions does it not reach?
    """
    report = ctx.report
    report.say("L17 the boundary of this instrument, measured not asserted")
    bound = {p for label, p in ctx.register.bound if label == DOC_SUBJECT}
    bound_effective = {p for label, p in ctx.register.bound
                       if label == DOC_EFFECTIVE}

    def covered(rendered, universe):
        return any(rendered == b or rendered.startswith(b + ".")
                   or rendered.startswith(b + "[") for b in universe)

    # A leaf inside an operation PAYLOAD is bound through the effective
    # contract, because that is where the payload lands.  Counting it as
    # unbound would understate the binding exactly where five of the review's
    # twelve escapes live.
    payload_map = {}
    for index, operation in enumerate(
            ctx.subject.get("derivedFrom", {}).get("operations", []) or []):
        if isinstance(operation, dict) and isinstance(operation.get("path"), str):
            payload_map["derivedFrom.operations[%d].value" % index] = \
                operation["path"]

    def effective_twin(rendered):
        for prefix, target in payload_map.items():
            if rendered == prefix:
                return target
            if rendered.startswith(prefix + ".") or rendered.startswith(prefix + "["):
                return target + rendered[len(prefix):]
        return None

    per_key = {}
    total = held = via_payload = 0
    for steps, _value in walk_leaves(ctx.subject):
        rendered = render_path(steps)
        top = steps[0] if steps else "(root)"
        counts = per_key.setdefault(top, [0, 0])
        counts[0] += 1
        total += 1
        hit = covered(rendered, bound)
        if not hit:
            twin = effective_twin(rendered)
            if twin is not None and covered(twin, bound_effective):
                hit = True
                via_payload += 1
        if hit:
            counts[1] += 1
            held += 1
    eff_total = eff_held = 0
    for steps, _value in walk_leaves(ctx.effective):
        eff_total += 1
        if covered(render_path(steps), bound_effective):
            eff_held += 1
    report.say("  subject leaves                        : %d" % total)
    report.say("  leaves bound to a value this run computed: %d  (%d of them"
               % (held, via_payload))
    report.say("  through the effective contract, because an operation payload")
    report.say("  is bound where it LANDS, not where it is written)")
    report.say("  leaves NOT value-bound                : %d" % (total - held))
    report.say("  effective-contract leaves bound       : %d of %d"
               % (eff_held, eff_total))
    report.say("  (that second figure counts leaves compared to a value NAMED")
    report.say("   by a gate. The whole effective contract is still constrained")
    report.say("   structurally -- the census walks every path, and every `set`")
    report.say("   must restate type-exactly the value it replaces -- so it is a")
    report.say("   floor on value-binding, not a coverage figure for the run.)")
    report.say("  claims registered                     : %d"
               % ctx.register.checked)
    report.say("  by top-level member (bound/total):")
    for key in sorted(per_key):
        count, hold = per_key[key][0], per_key[key][1]
        report.say("    %-38s %4d/%-4d %s"
                   % (key, hold, count, "" if hold else "<- none bound"))
    report.say("  READ THIS AS A BOUND, NOT A BOAST: falsifying any of the %d"
               % (total - held))
    report.say("  unbound leaves is an escape this instrument does not catch.")
    report.say("  The predecessor's twelve escapes are all inside the bound set")
    report.say("  now; the rest of the narrative is still assertion.")
    report.say()


# --------------------------------------------------------------------------
# the battery
# --------------------------------------------------------------------------
def battery(ctx, expect_own_digest=True):
    gate_derivation(ctx)
    gate_encoding(ctx, expect_own_digest=expect_own_digest)
    gate_vectors(ctx)
    gate_epc(ctx)
    gate_law18(ctx)
    gate_census(ctx)
    gate_closure(ctx)
    gate_six_live(ctx)
    gate_digests(ctx)
    gate_self_reports(ctx)
    gate_number_production(ctx)
    gate_ruling_polarity(ctx)   # L14
    gate_split(ctx)             # L15, and it fixes ctx.split_declared
    gate_numerals(ctx)          # L16, which reads that split
    gate_coverage(ctx)          # L17
    return ctx


def run(subject_path, subject_raw, report, expect_own_digest=True):
    digest = hashlib.sha256(subject_raw).hexdigest()
    report.say("subject            : %s" % subject_path.name)
    report.say("subject bytes      : %d" % len(subject_raw))
    report.say("subject sha256     : %s" % digest)
    report.say()
    subject = parse_json(subject_raw.decode("utf-8"), subject_path.name)
    ctx = Context(subject, report, Register(report))
    return battery(ctx, expect_own_digest=expect_own_digest)


# --------------------------------------------------------------------------
# --selftest
# --------------------------------------------------------------------------
def find_op(subject, path):
    for op in subject.get("derivedFrom", {}).get("operations", []):
        if op.get("path") == path:
            return op
    raise Refused("no operation at path %s to forge" % path)


def forged_run(subject):
    """Run the WHOLE battery over a forged document and return (codes, report).

    Running only the gate under test would let a suite claim a catch its
    shipped instrument does not make.  This is the reviewer's own method: forge
    the document, run the instrument, read the findings.
    """
    quiet = Report(quiet=True)
    try:
        ctx = Context(subject, quiet, Register(quiet))
        battery(ctx)
    except Refused as exc:
        quiet.finding("C2V12-REFUSED", "(run)", str(exc))
    return quiet


def skeleton_moved(base_encoder, original, forged):
    return base_encoder.skeleton_digest(original) != \
        base_encoder.skeleton_digest(forged)


def selftest(subject_path, subject_raw, base_report):
    """Every mutation must be refused FOR A NAMED REASON.

    Family C is the reason this file exists.  Each row is one of the twelve
    artifacts the independent review constructed that are WRONG and that the
    predecessor accepted at exit 0 with FINDINGS: 0.  Each keeps the shape and
    inverts the meaning, and each row reports whether the documentSkeleton moved
    -- it must NOT, because that is precisely what made these escapes possible,
    and a catch that depended on the skeleton moving would not be a catch of
    this class at all.
    """
    if base_report.findings:
        print("C2V12-SELFTEST-REFUSED: the base subject is not clean "
              "(%d findings). A mutation suite over a dirty base is not an "
              "oracle." % len(base_report.findings))
        return 3

    subject = parse_json(subject_raw.decode("utf-8"), subject_path.name)
    effective, chain, _digests = resolve(subject)
    spec = effective["documentIdentityEncoding"]
    encoder = ContractEncoder(spec)
    head_raw = verified_bytes("c2-plan-stage-schema.v9.json")
    head = parse_json(head_raw.decode("utf-8"), "head")
    golden = None
    for vector in (effective["planIntent"]["attemptAndExecutionJoin"]
                   ["executionPlanCommitment"]["vectors"]):
        if "planIntentCommitmentBothArms" in vector:
            golden = vector["planIntentCommitmentBothArms"]

    rows = []

    def row(family, name, caught, reason):
        rows.append((family, name, bool(caught), reason, None))

    def forge_row(family, name, mutate, expect_code, why):
        forged = copy.deepcopy(subject)
        try:
            mutate(forged)
        except (Refused, KeyError, IndexError, TypeError) as exc:
            rows.append((family, name, False,
                         "the mutation could not be applied: %s" % exc, None))
            return
        report = forged_run(forged)
        codes = report.codes()
        caught = expect_code in codes
        moved = skeleton_moved(encoder, subject, forged)
        hits = ["%s at %s" % (c, p) for c, p, _d in report.findings
                if c == expect_code]
        if hits:
            detail = "; ".join(hits[:2])
            if len(hits) > 2:
                detail += "; (+%d more of the same code)" % (len(hits) - 2)
        else:
            detail = ", ".join(sorted(codes)) if codes else "NO FINDING AT ALL"
        rows.append((family, name, caught,
                     "%s -- expected %s, got: %s" % (why, expect_code, detail),
                     moved))

    # ---------------- Family A: refusals -------------------------------
    mutated = bytearray(subject_raw)
    mutated[-2] = mutated[-2] ^ 0x20
    row("A", "M1 subject drift before parse",
        hashlib.sha256(bytes(mutated)).hexdigest() != SUBJECT_SHA256,
        "the pinned subject digest no longer matches, so the run exits 2 "
        "before a single byte is parsed")

    caught = ""
    try:
        parse_json('{"a": 1, "a": 2}', "M2")
    except Refused as exc:
        caught = str(exc)
    row("A", "M2 duplicate key", "duplicate key 'a'" in caught,
        "the hook names the offending key: " + (caught or "NOT CAUGHT"))

    forged = copy.deepcopy(subject)
    forged["derivedFrom"]["predecessorSha256"] = "0" * 64
    caught = ""
    try:
        resolve(forged)
    except Refused as exc:
        caught = str(exc)
    row("A", "M3 predecessor digest mismatch", "digest mismatch" in caught,
        "the chain refuses before parsing the predecessor: "
        + (caught[:90] or "NOT CAUGHT"))

    forged = copy.deepcopy(subject)
    for op in forged["derivedFrom"]["operations"]:
        if op["op"] == "set" and op["path"] == "version":
            op["from"] = 10.0        # 10.0 is not 10: law 18 at the resolver
    caught = ""
    try:
        resolve(forged)
    except Refused as exc:
        caught = str(exc)
    row("A", "M4 `from` restated as 10.0 instead of 10",
        "does not describe the bytes" in caught,
        "type-exact `from` refuses a float where an integer stands: "
        + (caught[:90] or "NOT CAUGHT"))

    # ---------------- Family B: degraded implementations ---------------
    class ByteLength(ContractEncoder):
        def frame(self, kind, payload):
            return (self.tags[kind] + str(len(payload.encode("utf-8")))
                    + ":" + payload)
    row("B", "M6 length counted in UTF-8 bytes",
        ByteLength(spec).canon("é") != "s1:é",
        "FF-1 separates the readings: s2 instead of s1")

    # NOTE ON WHERE M7 IS DETECTABLE.  An earlier draft of this mutation
    # asserted against the HEAD'S documentSkeleton digest and ESCAPED, because
    # the skeleton is an array of [pathToken, typeName] rows and a path is an
    # array of strings and integers -- there is no OBJECT anywhere in the
    # structure the skeleton digest hashes.  That is not a hole in this suite;
    # it is exactly the 3-of-7 split `exercisedByTheSkeletonDigest` declares,
    # observed by executing it.  The ordering rule is load-bearing for VALUE
    # comparison, and FF-2 is where the contract witnesses it, so that is where
    # this mutation is asserted.  M17 then executes the split itself.
    class RawKeyOrder(ContractEncoder):
        def canon(self, value):
            if type(value) is dict:
                body = "".join(self.canon(k) + self.canon(value[k])
                               for k in sorted(value))
                return self.frame("object", body)
            return ContractEncoder.canon(self, value)
    row("B", "M7 object order by raw key",
        RawKeyOrder(spec).canon({"b": 1, "ab": 2}) != "o17:s1:bi1:1s2:abi1:2",
        "FF-2's ordering trap: raw-key order yields %r where the contract "
        "pins o17:s1:bi1:1s2:abi1:2"
        % RawKeyOrder(spec).canon({"b": 1, "ab": 2}))

    class SlashPath(ContractEncoder):
        def rows(self, root):
            out = []

            def walk(node, path):
                out.append(["/".join(str(s) for s in path), self.jtype(node)])
                kind = self.jtype(node)
                if kind == "object":
                    for key in node:
                        walk(node[key], path + [key])
                elif kind == "array":
                    for index, item in enumerate(node):
                        walk(item, path + [index])

            walk(root, [])
            return out
    slash = SlashPath(spec)
    row("B", "M8 path rendered as a '/'-join",
        slash.skeleton_digest({"a": {"b": 1}}) == slash.skeleton_digest(
            {"a": {}, "a/b": 1}),
        "IR-C2V8-01: the rendering COLLIDES, which is why the path is "
        "canonicalised; the collision is the detection")

    class ShortestNoPoint(ContractEncoder):
        @staticmethod
        def number_payload(value):
            if value == int(value) and math.isfinite(value):
                return str(int(value))
            return repr(value)
    row("B", "M9 number production reverted to 'shortest round-trip'",
        ShortestNoPoint(spec).canon(1.0) != "n3:1.0",
        "FF-6 fails: the reverted rule yields %r where the contract pins n3:1.0"
        % ShortestNoPoint(spec).canon(1.0))

    class SignByComparison(ContractEncoder):
        @staticmethod
        def number_payload(value):
            text = ContractEncoder.number_payload(value)
            return text[1:] if (value == 0.0 and text.startswith("-")) else text
    row("B", "M10 negative zero loses its sign",
        SignByComparison(spec).canon(-0.0) != encoder.canon(-0.0),
        "FF-N2: -0.0 and 0.0 collapse to one token")

    differ = epc_decide({POSITIONS[0]: golden, POSITIONS[1]: "sha256:" + "1" * 64},
                        degrade="golden-drift", golden=golden)[0]
    agree = epc_decide({POSITIONS[0]: "sha256:" + "1" * 64,
                        POSITIONS[1]: "sha256:" + "1" * 64},
                       degrade="golden-drift", golden=golden)[0]
    row("B", "M11 EPC-V2 degraded to golden-drift detection", differ == agree,
        "the discriminator fires: both readings get %s, so the procedure is "
        "not the control" % differ)

    verdict = epc_decide({POSITIONS[0]: golden, POSITIONS[1]: 1.0},
                         degrade="host-equality")[0]
    row("B", "M12 EPC compares before type-asserting", verdict == "REJECT"
        and epc_decide({POSITIONS[0]: golden, POSITIONS[1]: 1.0})[1] != [],
        "law 18: the real procedure names the offending JSON production; the "
        "degraded one only says 'differs'")

    escaped = [name for name, record, expected, _why in epc_witnesses(golden)
               if expected == "REJECT"
               and epc_decide(record, degrade="always-accept")[0] == "ACCEPT"]
    row("B", "M13 EPC that accepts everything", len(escaped) > 0,
        "%d negative witnesses escape, so an always-accept gate is detectable"
        % len(escaped))

    stripped = copy.deepcopy(spec)
    stripped["frameParts"]["lengthIsCountedInCodePoints"] = "counted somehow"
    row("B", "M16 the contract stops stating code-point length",
        len(ContractEncoder(stripped).obligations()) > 0,
        "the encoder refuses to keep assuming what the contract no longer says")

    # M17: the split, executed.  v12 derives the expected partition from the
    # contract's prose instead of typing it, so the row tests the artifact and
    # not this file's transcription of it.
    reference = encoder.skeleton_digest(head)
    exercised, unexercised = [], []

    def perturbed(kind):
        class P(ContractEncoder):
            def frame(self, k, payload):
                if k == kind:
                    return self.tags[k] + str(len(payload)) + ";" + payload
                return ContractEncoder.frame(self, k, payload)
        return P(spec)

    for kind in spec["productions"]:
        moved = perturbed(kind).skeleton_digest(head) != reference
        (exercised if moved else unexercised).append(kind)
    declared_text = flat(spec["exercisedByTheSkeletonDigest"]["measurement"])
    head_text, _, tail_text = declared_text.partition("does NOT exercise")
    declared_exercised = sorted(n for n in spec["productions"]
                                if re.search(r"\b%s\b" % n, head_text))
    declared_unexercised = sorted(n for n in spec["productions"]
                                  if re.search(r"\b%s\b" % n, tail_text))
    row("B", "M17 the declared 3-of-7 split, derived from prose and executed",
        sorted(exercised) == declared_exercised
        and sorted(unexercised) == declared_unexercised,
        "the contract's own prose declares exercised=%s unexercised=%s, and "
        "perturbing each production in turn moves the head's skeleton digest "
        "for exactly %s and leaves it standing for %s"
        % (declared_exercised, declared_unexercised,
           sorted(exercised), sorted(unexercised)))

    # ---------------- Family C: the escape class -----------------------
    # M5 first, because it is the escape class's own control: an edited digest
    # string leaves path and type unchanged, so the fixpoint cannot see it.
    forge_row("C", "M5 published documentSkeleton.sha256 edited",
              lambda d: d["documentSkeleton"].__setitem__("sha256", "0" * 64),
              "C2V12-OWN-SKELETON",
              "the fixpoint CANNOT catch this; recomputation does")

    six = "theSixLiveOnePointZeroLeaves"

    def set_six(document, value):
        find_op(document, "documentIdentityEncoding.numberProduction")["value"][six] = value

    def get_six(document):
        return list(find_op(document,
                            "documentIdentityEncoding.numberProduction")["value"][six])

    forge_row("C", "E1 the central RULING reversed in the subject's narrative",
              lambda d: d["theNumberProductionDefect"].__setitem__(
                  "ruling",
                  "THE PRODUCTION WAS RIGHT; FF-6 WAS WRONG. The vector is "
                  "restated byte-for-byte and the production is retained so "
                  "the production follows from it."),
              "C2V12-RULING-POLARITY",
              "escape 1 of 12: the ruling inverted in prose, path and type "
              "unchanged")

    forge_row("C", "E2 theSixLive: one entry replaced by a nonexistent path",
              lambda d: set_six(d, ["thisPathDoesNotExist.anywhere.at.all"]
                                + get_six(d)[1:]),
              "C2V12-SIX-LIVE",
              "escape 2 of 12: OBS-4, the headline correction fabricated")

    forge_row("C", "E3 theSixLive: one entry replaced by a REAL path holding 1.5",
              lambda d: set_six(d, ["coverageKey.rootTotalityCases[3].value"]
                                + get_six(d)[1:]),
              "C2V12-SIX-LIVE",
              "escape 3 of 12: the plausible falsification -- a path that "
              "exists and is a float, but is 1.5")

    forge_row("C", "E4 theSixLive: all six fabricated inside the operation payload",
              lambda d: set_six(d, ["fabricated.leaf.%d" % i for i in range(6)]),
              "C2V12-SIX-LIVE",
              "escape 4 of 12: the whole enumeration invented")

    forge_row("C", "E5 twoIndependentEncoders.encoderBReproducedIt true -> false",
              lambda d: d["selfVerification"]["twoIndependentEncoders"]
              .__setitem__("encoderBReproducedIt", False),
              "C2V12-SELF-REPORT",
              "escape 5 of 12: a boolean self-report inverted; JSON type "
              "unchanged")

    def break_mismatches(document):
        block = find_op(document, "documentIdentityEncoding.numberProduction")["value"]
        block["howThisWasVerified"] = block["howThisWasVerified"].replace(
            "Mismatches: ZERO", "Mismatches: SEVENTEEN")

    forge_row("C", "E6 howThisWasVerified 'Mismatches: ZERO' -> 'SEVENTEEN'",
              break_mismatches, "C2V12-NUMERAL",
              "escape 6 of 12: a reported measurement falsified")

    forge_row("C", "E7 measuredPredecessorDigests: the v9 digest falsified",
              lambda d: d["selfVerification"]["measuredPredecessorDigests"]
              .__setitem__("artifacts/c2-plan-stage-schema.v9.json", "1" * 64),
              "C2V12-PREDECESSOR-DIGEST",
              "escape 7 of 12: a digest table the predecessor held the true "
              "values for and never compared")

    forge_row("C", "E8 structuralDiff.leavesAdded 73 -> 7",
              lambda d: d["selfVerification"]
              ["structuralDiffAgainstTheEffectivePredecessor"]
              .__setitem__("leavesAdded", 7),
              "C2V12-SELF-REPORT",
              "escape 8 of 12: an integer self-report; JSON type unchanged")

    forge_row("C", "E9 chainDepth 3 -> 9",
              lambda d: d["selfVerification"].__setitem__("chainDepth", 9),
              "C2V12-SELF-REPORT",
              "escape 9 of 12: the depth of a chain this instrument itself "
              "resolves")

    def break_positional(document):
        block = find_op(document, "documentIdentityEncoding.numberProduction")["value"]
        block["positionalForm"] = (
            "The digits placed against the decimal point at E, and the payload "
            "always ends in .00, so 1.0 is written 1.00, 100.0 is written "
            "100.00 and 1000000000000000.0 is written 1000000000000000.00.")

    forge_row("C", "E10 positionalForm rewritten to a DIFFERENT rule",
              break_positional, "C2V12-PROSE-VECTOR",
              "escape 10 of 12: prose that contradicts the encoder and the "
              "block's own vectors")

    def break_scientific(document):
        block = find_op(document, "documentIdentityEncoding.numberProduction")["value"]
        block["scientificForm"] = "No exponent form is ever used."

    forge_row("C", "E11 scientificForm rewritten to deny exponent form",
              break_scientific, "C2V12-ENCODING-PROSE",
              "escape 11 of 12: the other half of OBS-6")

    def break_payload_ruling(document):
        block = find_op(document, "documentIdentityEncoding.numberProduction")["value"]
        block["theRuling"] = (
            "THE PRODUCTION IS RIGHT AND THE VECTOR WAS WRONG. The production "
            "is retained unchanged and the vector is restated to follow it.")

    forge_row("C", "E12 numberProduction.theRuling inverted in the payload",
              break_payload_ruling, "C2V12-RULING-POLARITY",
              "escape 12 of 12: the same inversion one level down, inside the "
              "delta's own operation payload")

    # ---- further rows of the same class, beyond the reviewer's twelve ----
    forge_row("C", "F1 census counter payload 193 -> 194",
              lambda d: find_op(
                  d, "hostileScalarLeafTotality.contractRoot.noOpInjections")
              .__setitem__("value", 194),
              "C2V12-CENSUS", "the census, recomputed by the pinned node_census")

    forge_row("C", "F2 theClosureCount.compared 17 -> 16",
              lambda d: d["theClosureCount"].__setitem__("compared", 16),
              "C2V12-CLOSURE", "the closure count, re-derived")

    forge_row("C", "F3 a closure member path falsified",
              lambda d: d["theClosureCount"]["members"].__setitem__(
                  0, "planIntent.notAnObjectHere"),
              "C2V12-CLOSURE-MEMBERS", "the enumerated member list, re-derived")

    forge_row("C", "F4 the duplicate closure table in preservedByteForByte",
              lambda d: d["selfVerification"]["preservedByteForByte"]
              .__setitem__("closedCollectionsCompared", 8),
              "C2V12-CLOSURE",
              "the same count published a second time and checked nowhere by "
              "the predecessor")

    def break_ffn1(document):
        block = find_op(document, "documentIdentityEncoding.numberProduction")["value"]
        for vector in block["vectors"]:
            if vector["id"].startswith("FF-N1"):
                vector["underThisText"] = "n1:1"

    forge_row("C", "F5 FF-N1's underThisText falsified to n1:1",
              break_ffn1, "C2V12-VECTOR",
              "a vector expectation read FROM the contract, so falsifying it "
              "fires")

    def break_ff6(document):
        # FF-6 lives in the effective PREDECESSOR, so it is falsified by adding
        # an operation that overwrites it -- the same shape-preserving edit,
        # reached through the derivation the subject actually declares.
        document["derivedFrom"]["operations"].append({
            "op": "set",
            "path": "documentIdentityEncoding.vectors[5].numberOne",
            "from": "n3:1.0",
            "value": "n1:1"})

    forge_row("C", "F6 FF-6's numberOne falsified through a new operation",
              break_ff6, "C2V12-VECTOR",
              "the law-18 vector itself, expectation contract-sourced")

    forge_row("C", "F7 a recordedInputs digest falsified",
              lambda d: d["recordedInputs"][6].__setitem__("sha256", "2" * 64),
              "C2V12-RECORDED-INPUT",
              "a digest the document publishes for a file it names")

    forge_row("C", "F8 leafCensusOfTheseOwnBytes.stringLeaves 331 -> 330",
              lambda d: d["selfVerification"]["leafCensusOfTheseOwnBytes"]
              .__setitem__("stringLeaves", 330),
              "C2V12-SELF-REPORT",
              "the document's census of its own leaves")

    forge_row("C", "F9 countersThatDidNotMove names a counter that moved",
              lambda d: d["operationAccounting"]["countersThatDidNotMove"]
              .__setitem__(1, "dictPaths"),
              "C2V12-SELF-REPORT",
              "which counters moved is re-derived by running the census over "
              "the effective predecessor; one member swapped, so the list "
              "length and the leaf census are untouched")

    def break_reproduction(document):
        document["derivedFrom"]["operations"].append({
            "op": "set",
            "path": "documentIdentityEncoding.reproduction.rootSubtreeDigestsDiffering",
            "from": 0,
            "value": 29})

    forge_row("C", "F10 reproduction.rootSubtreeDigestsDiffering 0 -> 29",
              break_reproduction, "C2V12-SELF-REPORT",
              "the contract's own copy of the reproduction self-report")

    def break_split_real(document):
        spec_before = resolve(copy.deepcopy(document))[0][
            "documentIdentityEncoding"]["exercisedByTheSkeletonDigest"]["measurement"]
        document["derivedFrom"]["operations"].append({
            "op": "set",
            "path": "documentIdentityEncoding.exercisedByTheSkeletonDigest.measurement",
            "from": spec_before,
            "value": "A skeleton row is [string, string]. The skeleton digest "
                     "therefore exercises exactly three productions -- object, "
                     "boolean and null -- and does NOT exercise string, "
                     "integer, number or array."})

    forge_row("C", "F11 the declared 3-of-7 split inverted",
              break_split_real, "C2V12-SPLIT",
              "the split is parsed out of the prose and executed by "
              "perturbation, so a false declaration fires")

    def break_separates(document):
        block = find_op(document, "documentIdentityEncoding.numberProduction")["value"]
        for vector in block["vectors"]:
            if vector["id"].startswith("FF-N2"):
                vector["separates"] = False

    forge_row("C", "F12 a vector's `separates` flipped true -> false",
              break_separates, "C2V12-VECTOR-DEGENERATE",
              "requirement 3: a published corpus must be non-degenerate where "
              "the artifact claims distinctness")

    forge_row("C", "F13 theClosureCount.definition's looser count 22 -> 30",
              lambda d: d["theClosureCount"].__setitem__(
                  "definition",
                  d["theClosureCount"]["definition"].replace(
                      "would give 22", "would give 30")),
              "C2V12-NUMERAL",
              "the count the definition names for the reading it rejects")

    forge_row("C", "F14 bindingDeclaration.headSha256 falsified",
              lambda d: d["bindingDeclaration"].__setitem__(
                  "headSha256", "3" * 64),
              "C2V12-RECORDED-INPUT",
              "the head digest, measured against the head's own bytes")

    forge_row("C", "F16 theFreezeMisattribution's measured word counts falsified",
              lambda d: d["theFreezeMisattribution"].__setitem__(
                  "finding",
                  d["theFreezeMisattribution"]["finding"].replace(
                      "'objection' 0", "'objection' 47")),
              "C2V12-SELF-REPORT",
              "a count over bytes this instrument already holds pinned")

    forge_row("C", "F17 companionInstrument.path made a dead link",
              lambda d: find_op(d, "companionInstrument")["value"].__setitem__(
                  "path", "artifacts/check-c2-v99-does-not-exist.py"),
              "C2V12-SELF-REPORT",
              "v10 declined to name a companion instrument precisely because a "
              "named-but-absent path is a dead link in a binding artifact")

    forge_row("C", "F15 the six-leaf enumeration deleted outright",
              lambda d: find_op(
                  d, "documentIdentityEncoding.numberProduction")["value"].pop(
                      "theSixLiveOnePointZeroLeaves"),
              "C2V12-CLAIM-ABSENT",
              "bind against WRONG, and also against GONE: a gate whose subject "
              "can be deleted is not a gate")

    # ---------------- report -------------------------------------------
    escaped_rows = [r for r in rows if not r[2]]
    print("--selftest: every mutation must fail for a NAMED reason")
    print()
    print("Family A -- refusals that stop the run before it can report")
    print("Family B -- degraded implementations of a decision procedure")
    print("Family C -- THE ESCAPE CLASS: a leaf whose VALUE is false while its")
    print("            PATH and TYPE are unchanged. Rows E1..E12 are the twelve")
    print("            artifacts the independent review of check-c2-v11.py")
    print("            constructed and that instrument accepted at exit 0.")
    print()
    current = None
    for family, name, caught, reason, moved in rows:
        if family != current:
            current = family
            print("  -- Family %s --" % family)
        print("  [%s] %s" % ("CAUGHT " if caught else "ESCAPED", name))
        print("           reason: %s" % reason)
        if moved is not None:
            print("           shape-preserving: documentSkeleton digest %s"
                  % ("MOVED (this catch is structural, not a value catch)"
                     if moved else "UNMOVED -- the catch is a VALUE catch"))
    print()
    families = {}
    for family, _n, caught, _r, _m in rows:
        seen, hit = families.get(family, (0, 0))
        families[family] = (seen + 1, hit + (1 if caught else 0))
    for family in sorted(families):
        seen, hit = families[family]
        print("Family %s: %d mutations, %d caught, %d escaped"
              % (family, seen, hit, seen - hit))
    print("mutations: %d, caught: %d, escaped: %d"
          % (len(rows), len(rows) - len(escaped_rows), len(escaped_rows)))
    twelve = [r for r in rows if r[1].startswith("E")]
    print("the review's twelve escapes: %d carried, %d now caught, %d still escaping"
          % (len(twelve), sum(1 for r in twelve if r[2]),
             sum(1 for r in twelve if not r[2])))
    if escaped_rows:
        print()
        for _f, name, _c, _r, _m in escaped_rows:
            print("C2V12-MUTATION-ESCAPED: " + name)
        return 1
    print()
    print("Every mutation was refused, and each refusal names the condition "
          "that caught it. A gate that stopped measuring would appear here as "
          "an ESCAPED row. This is not a completeness claim: L17 of the main "
          "run measures how many leaves remain value-unbound, and falsifying "
          "any of those is still an escape.")
    return 0


# --------------------------------------------------------------------------
def main(argv):
    flags = [a for a in argv[1:] if a.startswith("--")]
    positional = [a for a in argv[1:] if not a.startswith("--")]
    for flag in flags:
        if flag != "--selftest":
            print("unsupported flag %s; usage: %s [subject.json] | --selftest"
                  % (flag, argv[0]), file=sys.stderr)
            return 2
    if len(positional) > 1:
        print("at most one subject may be named", file=sys.stderr)
        return 2

    subject_path = pathlib.Path(positional[0]) if positional else HERE / SUBJECT
    try:
        subject_raw = subject_path.read_bytes()
    except OSError as exc:
        print("cannot read subject %s: %s" % (subject_path, exc), file=sys.stderr)
        return 2

    digest = hashlib.sha256(subject_raw).hexdigest()
    pinned_subject = (not positional) or subject_path.name == SUBJECT
    if pinned_subject and digest != SUBJECT_SHA256:
        print("C2V12-SUBJECT-DRIFT: %s\n  declared %s\n  measured %s\n"
              "  The subject is hash-verified BEFORE it is parsed. This "
              "instrument will not report on bytes it was not written for."
              % (subject_path.name, SUBJECT_SHA256, digest), file=sys.stderr)
        return 2

    report = Report()
    if not pinned_subject:
        report.skip("C2V12-SUBJECT-DIGEST",
                    "the subject named on the command line is %s, not the "
                    "pinned subject %s, so this instrument holds no declared "
                    "digest for it and the drift gate did NOT run. Every other "
                    "gate below did, INCLUDING the value gates -- which is the "
                    "point: renaming a forged file is exactly how the twelve "
                    "escapes reached exit 0 against the predecessor."
                    % (subject_path.name, SUBJECT))
    try:
        run(subject_path, subject_raw, report)
    except Refused as exc:
        print("C2V12-REFUSED: %s" % exc, file=sys.stderr)
        return 2

    if "--selftest" in flags:
        return selftest(subject_path, subject_raw, report)

    print("check-c2-v12.py -- successor companion instrument for " + SUBJECT)
    print("=" * 72)
    for line in report.lines:
        print(line)
    for code, why in report.skips:
        print("SKIP %s: %s" % (code, why))
    print("=" * 72)
    if report.findings:
        print("FINDINGS: %d" % len(report.findings))
        for code, position, detail in report.findings:
            print("  %s at %s" % (code, position))
            print("    %s" % detail)
        return 1
    print("FINDINGS: 0")
    print()
    print("A green run is checker-scope evidence authored by the same lane "
          "that authored the subject. It is NOT independent review, NOT "
          "qualification, NOT demonstration, NOT a seal and NOT product "
          "acceptance. v9 remains the head and check-c2-v9.py remains its "
          "instrument. check-c2-v11.py is unedited and remains pinned by its "
          "own review. This file closes no IMPLEMENTATION-FREEZE section 7.1 "
          "row and CD-RT-5 remains BLOCKED_ON_PHASE_1A.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
