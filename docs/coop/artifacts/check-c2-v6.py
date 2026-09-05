#!/usr/bin/env python3
"""Retained executable checker for the C-2 plan/stage contract, v6.

WHY v6 EXISTS
-------------
`1.0 == 1` has now defeated three consecutive artifacts written to defeat it,
each time in the repair's own self-certification rather than in the surface it
repaired:

    v3   LB-C2-01: a bare `!= 1` on schemaVersion              REJECTED
    v4   repairs the wire surface; its own census comparison   BLOCKING
         admits 57 of 136 integer leaves to a green banner     (IR-C2V4-01)
    v5   repairs the census and adds a document-wide type      REJECTED
         lock; its own `if not adjudicated <= lines:` at       (IR-C2V5-01..04)
         line 1815 admits `{2487} <= {2487.0}`

c2-plan-stage-schema.v5.review-independent.json, at
b8ec85cf46b2e2ae7e9e8a1f5b56b26a83e014d6c59f99d77798040284c4a92c, is a REJECT
carrying four blocking findings.  The decisive one, IR-C2V5-01, needs ONE JSON
edit and zero bytes of Python:

    c2-plan-stage-schema.v5.json
      theDefect.repairedComparisonSites[0].line: 2487 -> 2487.0
    python3 -I -B check-c2-v5.py <that file>   ->   exit 0, full green banner,
      including the line certifying `0 type-distinct admissions`.

That vector is retained here as a live executable case (L6b) and runs on every
invocation against the PINNED bytes of check-c2-v5.py.

WHAT WENT WRONG THREE TIMES, AND THE ONE THING v6 DOES DIFFERENTLY
-----------------------------------------------------------------
Every previous repair guarded CALL SITES.  v4 guarded the wire validator and
left its census bare.  v5 guarded the census and left its own repro enumeration
bare.  Each repair was a list of places, and the defect moved to a place not on
the list.  A spelling enumeration cannot close a class.

v6 does not add another guard.  It builds ONE primitive -- the `jx` block in
section 1 -- that decides, in a single place, whether two values are comparable
and whether they are equal, with JSON-type exactness, and then routes the whole
operator space through it.  IMPLEMENTATION-FREEZE.md section 6 law 18 says:

    closed-scalar admission is exact-type -- the comparison rejects any value
    whose JSON type differs from the declared type, before comparing content,
    at any depth, and no identity may be derived from an ungated record.

`jx` is law 18 made executable.  Its single decision point is `jx_canon`, a
total, length-framed, type-tagged canonical encoding of a JSON value.  Every
comparison, ordering, membership test, set operation, key lookup, dedup and
sort in this file is decided by STRING equality or STRING ordering over those
tokens.  No numeric coercion is possible anywhere, because no numeric operator
is ever executed on a wire operand.

`jx_canon` is INVERTIBLE -- `jx_decanon(jx_canon(v))` reconstructs v exactly,
type and all -- so it is injective, so it can never conflate two distinct JSON
values.  That is not asserted; it is executed over the whole corpus on every
run and the count is published.

THE OPERATOR SPACE, ENUMERATED
------------------------------
Every Python operation below has int/float/bool equivalence semantics.  It is
not enough to patch `!=` and `<=`; the class is this wide, and section 1
publishes this table, executes a live hazard demonstration for every row, and
names the primitive that covers it.  See `OPERATOR_SPACE`.

    equality        ==  !=  operator.eq  operator.ne
    ordering        <  <=  >  >=  operator.lt/le/gt/ge
    membership      in  not in  operator.contains  .count  .index  .remove
    key lookup      d[k]  d.get  d.pop  d.setdefault  d.fromkeys  k in d
    set algebra     <=  <  >=  >  |  &  -  ^  .issubset  .issuperset
                    .isdisjoint  .union  .intersection  .difference
    dedup           set()  frozenset()  {..} literal  set/dict comprehension
    aggregation     sorted  min  max  sum  Counter  heapq  bisect
    depth           [1] == [1.0]  and  {"a": 1} == {"a": 1.0}  are True
    boolean         True == 1, hash(True) == hash(1), {True: x}[1]
    signed zero     -0.0 == 0 == 0.0  is True
    foreign numeric Decimal/Fraction/complex compare equal to int

`hash(1) == hash(1.0) == hash(True)` is the reason the container half of that
table is as dangerous as the operator half: `len({1, 1.0, True})` is 1.  Three
distinct JSON values silently become one, and a cardinality published from that
set is a false measurement that no equality guard would ever see.

WHAT AN ADOPTING CHECKER MUST DO
--------------------------------
The primitive is delimited by `# --- BEGIN JX PRIMITIVE ---` and
`# --- END JX PRIMITIVE ---`.  That region is verified on every run to have NO
free name outside the declared portability boundary, so it can be copied into
another checker verbatim with no edits.  check-evidence-v10.py,
check-retention-custody-v22.py and check-evaluation-proof-v11.py show indicative
susceptibility of 113/130, 155/183 and 45/48 integer leaves on v5's own scan.
v6 does NOT repair them and does not grade them.  To adopt:

  1. Copy the delimited region and `jx_selftest()`.  Call `jx_selftest()` from
     your own run and fail closed unless `escapes` is empty; publish its counts.
  2. Replace every wire-touching `==`/`!=`/`in`/`<`/`<=`/`>`/`>=`/subset with
     the `jx_` equivalent.  Replace `d[k]`/`d.get(k)` on wire keys with
     `jx_get`.  Replace `set(...)`/`{...}` over wire values with `jx_keyset`.
     Replace `sorted`/`min`/`max` over wire values with `jx_sorted`/`jx_min`/
     `jx_max`, which REFUSE a heterogeneous JSON type set instead of ordering it.
  3. Compare a published counter against a measured one with `jx_bind` ONLY.
     `jx_bind` asserts the JSON type of both operands independently and then
     compares CANONICAL STRINGS.  No numeric operator runs.
  4. Copy `wire_comparison_scan` and run it over your own tree.  Drive the
     ungated count to zero by repair, never by narrowing the model.
  5. Publish your own blind spots.  `jx` has them; they are in KNOWN BLIND SPOTS
     below and in the contract's guardInventory.

SHOULD A CHECKER COMPARE A MEASURED VALUE AGAINST A WIRE-SUPPLIED ONE AT ALL?
----------------------------------------------------------------------------
This was posed as an open design question and v6 answers it in code.  The
comparison exists to catch contract drift and it is also what creates the
false-accept surface.  v6 keeps the comparison but removes the surface: the
measured value is recomputed, CANONICALISED TO A STRING, and bound to the
published value by string equality after an explicit, independent type
assertion on each side.  `jx_bind` never executes `==` between two numbers.
The residual risk is no longer numeric coercion; it is that the measurement
function measures the wrong space, which is a different failure mode, is named
as RES-C2V6-04, and is not repaired here.

KNOWN BLIND SPOTS OF THIS INSTRUMENT
------------------------------------
1. `jx_canon` diverges from Python `==` in exactly two places, both measured and
   published every run: it is STRICTER at every cross-type corpus pair and at
   -0.0 against 0.0, and LOOSER at exactly one -- NaN, which
   Python makes non-reflexive and `jx` makes reflexive.  An admission gate needs
   an equivalence relation; Python float equality is not one.  Non-finite floats
   are never JSON integers and are refused by `jx_int` regardless.
2. L4 is still SYNTACTIC and its excusal test is still textual.  MEASURED THIS
   RUN AND STATED PLAINLY, because v5's residual pointed away from the live
   hazard: gate dominance currently excuses a published number of comparisons
   in this file, and the mechanism that actually hid IR-C2V5-01 was the TAINT
   MODEL, not the excusal test.  v6 extends taint to comprehension, generator,
   map/filter and container-constructor RESULTS -- the exact shape that
   laundered `lines` at check-c2-v5.py line 1815 -- and publishes both figures.
3. L4 cannot see a comparison built at run time (eval, exec, a dispatch table).
   It counts those primitives and requires eval and getattr-dispatch to be zero
   and exec to be exactly the two declared verified-snapshot loaders.
4. L4 cannot see `operator.ne` unless the name is visible.  v6 treats
   `operator.*` and bare `eq/ne/lt/le/gt/ge/contains` calls as comparison sites
   AND requires the `operator` module to be unimported here.  A checker that
   imports it must scan for it; that is stated for adopters.
5. This file cannot hash-pin itself.  Its own digest is REPORTED, never verified.
6. v6 does not re-run check-c2-v4.py --selftest, the predecessor's ~24k-case
   contract-root execution matrix.  Retained as RES-C2V6-03.
7. The type lock closes JSON TYPE.  A type-correct integer with a wrong VALUE at
   a position no layer measures is outside it.  v6 narrows that gap by requiring
   EVERY integer leaf of its own candidate document to be bound to a live
   measurement or to a verified pinned byte, with no unbound bucket -- but the
   effective contract inherited from the predecessor still has type-correct
   value drift outside the counter register.  Retained as RES-C2V6-05.
8. The primitive canonicalises a value it is GIVEN.  The host language collapses
   equal-hashing dict keys at CONSTRUCTION, before `jx_canon` ever sees them:
   `{1: "a", True: "b", 1.0: "c"}` is already `{1: "c"}` with one entry, and no
   later canonicalisation can recover what was lost.  `jx_keyset` and `jx_unique`
   close this for sequences, and `json.loads` cannot produce it because JSON
   object keys are always strings, so it is unreachable from the wire -- but an
   internally built dict can lose information upstream of the gate.  Measured and
   declared rather than mitigated, because a mitigation that only looked like one
   would be worse than the disclosure.
9. L7 is terminal.  A mutation battery cannot falsify itself.  Nothing stands
   behind it but independent review, and every row is printed for that reason.

Usage: python3 -I -B artifacts/check-c2-v6.py [contract]  ·  --selftest
Exit:  0 clean or green selftest · 1 findings · 2 unsupported invocation or a
       pinned input that does not hash to its declared digest · 3 --selftest
       REFUSED over a dirty base, which can never be absorbed into a pass.

Cost: the whole-document predecessor sweep is EXHAUSTIVE on every run, not
sampled.  That is the repair for the reviewer's finding that a published
measurement the run does not recompute is not evidence.  It costs about a
minute and the elapsed time is published in the banner.

Scope: checker-scope evidence only.  SPECIFIED / IMPLEMENTABLE_UNEXECUTED.
CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW.  This checker signs, seals,
freezes and integrates nothing, closes no finding, and changes no status.
CD-RT-5 remains BLOCKED_ON_PHASE_1A.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import sys
import time
import types
from contextlib import redirect_stdout

BINDING = "c2-plan-stage-schema.v6.json"
DECLARED_FLAGS = ("--selftest",)
DECLARED_EXIT_CODES = frozenset({"0", "1", "2", "3"})
HERE = pathlib.Path(__file__).resolve().parent
ARTIFACT_ID = "opensip.c2-plan-stage-schema.v6"


# --- BEGIN JX PRIMITIVE ---
# =============================================================================
# Section 1.  `jx` -- IMPLEMENTATION-FREEZE.md section 6 law 18, executable.
#
# ONE place decides whether two values are comparable and whether they are
# equal.  That place is `jx_canon`.  Everything else in this block is defined
# in terms of it, so there is exactly one thing to review, exactly one thing to
# break, and exactly one thing to adopt.
#
# PORTABILITY BOUNDARY.  This region depends on NOTHING outside itself except
# the names in JX_PORTABILITY_BOUNDARY.  That is verified structurally on every
# run (see `jx_portability_findings`), so the region can be copied into another
# checker verbatim.  Do not add a reference to anything above or below it.
# =============================================================================

JX_TYPES = ("null", "boolean", "integer", "number", "string", "array", "object")
JX_UNSUPPORTED = "unsupported"
# Names this block is permitted to reference from outside itself.  Builtins and
# the block's own definitions are excluded automatically.  If this list is not
# exactly the measured free-name set, the portability claim is false and the
# run fails; a claim that a component is reusable is a coverage claim like any
# other and is held to the same standard.
JX_PORTABILITY_BOUNDARY = ("math",)

import math  # noqa: E402  -- inside the portability boundary on purpose


class JxDomainError(TypeError):
    """A value outside the JSON value universe reached the primitive."""


def jx_type(value) -> str:
    """The JSON type of a Python value, with boolean decided BEFORE integer.

    `isinstance(True, int)` is True in the host language and that single fact
    is the root of LB-C2-01.  Every ordering below is `type(x) is C`, never
    `isinstance`, so no subclass can be mistaken for its base.
    """
    if value is None:
        return "null"
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
    return JX_UNSUPPORTED


def jx_frame(tag: str, payload: str) -> str:
    """Length-framed token.  Framing is what makes concatenation decodable, and
    decodability is what makes `jx_canon` injective."""
    return tag + str(len(payload)) + ":" + payload


def jx_canon(value) -> str:
    """THE single decision point.  A total, injective, type-tagged encoding.

    Two JSON values have the same token if and only if they are the same JSON
    value: same type, same content, at every depth.  Injectivity is not
    asserted -- `jx_decanon` inverts this function and the round trip is
    executed over the whole corpus on every run.
    """
    kind = jx_type(value)
    if kind == "null":
        return jx_frame("z", "")
    if kind == "boolean":
        return jx_frame("b", "1" if value else "0")
    if kind == "integer":
        return jx_frame("i", str(value))
    if kind == "number":
        return jx_frame("n", repr(value))
    if kind == "string":
        return jx_frame("s", value)
    if kind == "array":
        return jx_frame("a", "".join(jx_canon(item) for item in value))
    if kind == "object":
        pairs = sorted((jx_canon(key), jx_canon(item)) for key, item in value.items())
        return jx_frame("o", "".join(key + item for key, item in pairs))
    raise JxDomainError(
        type(value).__name__ + " is outside the JSON value universe; the "
        "primitive refuses to guess rather than compare something it cannot "
        "canonicalise")


def jx_decanon(text: str):
    """Inverse of `jx_canon`.  Its existence is the injectivity proof."""
    value, position = _jx_decanon_at(text, 0)
    if position != len(text):
        raise JxDomainError("trailing bytes after a canonical token")
    return value


def _jx_decanon_at(text: str, position: int):
    tag = text[position]
    colon = text.index(":", position + 1)
    size = int(text[position + 1:colon])
    start = colon + 1
    payload = text[start:start + size]
    nxt = start + size
    if tag == "z":
        return None, nxt
    if tag == "b":
        return payload == "1", nxt
    if tag == "i":
        return int(payload), nxt
    if tag == "n":
        return float(payload), nxt
    if tag == "s":
        return payload, nxt
    if tag == "a":
        out, inner = [], 0
        while inner < len(payload):
            item, inner = _jx_decanon_at(payload, inner)
            out.append(item)
        return out, nxt
    if tag == "o":
        out, inner = {}, 0
        while inner < len(payload):
            key, inner = _jx_decanon_at(payload, inner)
            item, inner = _jx_decanon_at(payload, inner)
            out[key] = item
        return out, nxt
    raise JxDomainError("unknown canonical tag " + repr(tag))


def jx_in_domain(value) -> bool:
    """Total.  True when `jx_canon` will succeed."""
    if jx_type(value) == JX_UNSUPPORTED:
        return False
    if type(value) is list:
        return all(jx_in_domain(item) for item in value)
    if type(value) is dict:
        return all(jx_in_domain(key) and jx_in_domain(item)
                   for key, item in value.items())
    return True


def jx_key(value) -> str:
    """The hashable proxy.  Put THIS in a set or a dict key, never the value.

    `len({1, 1.0, True})` is 1 in the host language: three distinct JSON values
    collapse to one set element and any cardinality read off that set is a
    false measurement.  `len({jx_key(1), jx_key(1.0), jx_key(True)})` is 3.
    """
    return jx_canon(value)


# ---- equality ---------------------------------------------------------------

def jx_equal(a, b) -> bool:
    """Type-exact deep equality.  STRING equality over canonical tokens.

    No numeric operator is executed.  There is no coercion path, at the top
    level or at any depth, for any operand type.
    """
    if not jx_in_domain(a) or not jx_in_domain(b):
        return False
    return jx_canon(a) == jx_canon(b)


def jx_ne(a, b) -> bool:
    """`not jx_equal`.  Named so the scan can see the inverse spelling too."""
    return not jx_equal(a, b)


def jx_same_type(a, b) -> bool:
    """Law 18's precondition as a named gate: the same JSON type, exactly."""
    return jx_type(a) == jx_type(b) and jx_type(a) != JX_UNSUPPORTED


# ---- the closed-scalar admission gates --------------------------------------

def jx_int(value) -> bool:
    """True only for a JSON integer.  A JSON boolean is NOT a JSON integer."""
    return jx_type(value) == "integer"


def jx_exact_int(value, constant) -> bool:
    """Exact-type integer constant guard.  Refuses true, false, 1.0 and "1"."""
    return jx_int(value) and jx_int(constant) and jx_canon(value) == jx_canon(constant)


def jx_int_in_range(value, low, high) -> bool:
    """Exact-type integer range guard.  All three operands must be integers."""
    if not jx_int(value) or not jx_int(low) or not jx_int(high):
        return False
    return low <= value <= high


def jx_finite_number(value) -> bool:
    return jx_type(value) == "number" and math.isfinite(value)


# ---- ordering ---------------------------------------------------------------

def jx_order(a, b):
    """-1 / 0 / 1, or None when the two values are not comparable.

    Comparability requires the SAME JSON type.  `1 <= 1.0` is True in the host
    language; here it is not comparable at all, which is the answer an
    admission gate needs.
    """
    if not jx_same_type(a, b):
        return None
    kind = jx_type(a)
    if kind in ("array", "object", "null", "boolean"):
        return 0 if jx_canon(a) == jx_canon(b) else None
    if a < b:
        return -1
    if b < a:
        return 1
    return 0


def jx_lt(a, b) -> bool:
    return jx_order(a, b) == -1


def jx_le(a, b) -> bool:
    return jx_order(a, b) in (-1, 0)


def jx_gt(a, b) -> bool:
    return jx_order(a, b) == 1


def jx_ge(a, b) -> bool:
    return jx_order(a, b) in (0, 1)


# ---- membership, containers, dedup ------------------------------------------

def jx_keyset(values) -> set:
    """A set of canonical tokens.  Type-exact by construction."""
    return {jx_key(item) for item in values}


def jx_in(needle, haystack) -> bool:
    """Type-exact membership over any iterable, including a dict's KEYS."""
    token = jx_key(needle)
    if type(haystack) is dict:
        return token in {jx_key(key) for key in haystack}
    return token in {jx_key(item) for item in haystack}


def jx_not_in(needle, haystack) -> bool:
    return not jx_in(needle, haystack)


def jx_subset(left, right) -> bool:
    """`{2487} <= {2487.0}` is True in the host language.  This is the
    operation that produced IR-C2V5-01, and it is not an equality test."""
    return jx_keyset(left) <= jx_keyset(right)


def jx_superset(left, right) -> bool:
    return jx_keyset(left) >= jx_keyset(right)


def jx_disjoint(left, right) -> bool:
    return jx_keyset(left).isdisjoint(jx_keyset(right))


def jx_difference(left, right) -> list:
    """Values of `left` whose JSON value is not in `right`, order preserved."""
    other = jx_keyset(right)
    out, seen = [], set()
    for item in left:
        token = jx_key(item)
        if token not in other and token not in seen:
            seen.add(token)
            out.append(item)
    return out


def jx_unique(values) -> list:
    """Dedup that does not collapse 1, 1.0 and True into one element."""
    out, seen = [], set()
    for item in values:
        token = jx_key(item)
        if token not in seen:
            seen.add(token)
            out.append(item)
    return out


def jx_count(values, needle) -> int:
    token = jx_key(needle)
    return sum(1 for item in values if jx_key(item) == token)


def jx_index(values, needle):
    token = jx_key(needle)
    for position, item in enumerate(values):
        if jx_key(item) == token:
            return position
    return None


# ---- key lookup -------------------------------------------------------------

def jx_has(mapping, key) -> bool:
    """`1 in {1.0: x}` is True in the host language, because the hashes agree."""
    token = jx_key(key)
    return token in {jx_key(existing) for existing in mapping}


def jx_get(mapping, key, default=None):
    """Type-exact key lookup.  Returns `default` when the key is absent."""
    token = jx_key(key)
    for existing, value in mapping.items():
        if jx_key(existing) == token:
            return value
    return default


def jx_at(container, key, default=None):
    """Type-exact lookup that is total over BOTH container shapes.

    For an object it is a canonical-key lookup, so `d[1]` cannot reach a value
    stored under `1.0`.  For an array it requires a genuine Python integer
    index, because `[10, 20][1.0]` is a TypeError and a float index must be a
    named refusal rather than a crash.
    """
    if jx_type(container) == "object":
        return jx_get(container, key, default)
    if jx_type(container) == "array":
        if not jx_int(key):
            return default
        if key < -len(container) or key >= len(container):
            return default
        return container[key]
    return default


def jx_has_at(container, key) -> bool:
    if jx_type(container) == "object":
        return jx_has(container, key)
    if jx_type(container) == "array":
        return jx_int(key) and -len(container) <= key < len(container)
    return False


def jx_put(container, key, value) -> bool:
    """Type-exact assignment.  Returns False rather than creating a second
    key that the host language would consider equal to an existing one."""
    if jx_type(container) == "object":
        for existing in list(container):
            if jx_canon(existing) == jx_canon(key):
                container[existing] = value
                return True
        if jx_type(key) == JX_UNSUPPORTED:
            return False
        container[key] = value
        return True
    if jx_type(container) == "array":
        if not jx_int(key) or key < -len(container) or key >= len(container):
            return False
        container[key] = value
        return True
    return False


def jx_string_set(values):
    """(set, reason).  A set of STRINGS.  Refuses any non-string element rather
    than letting `set()` silently collapse 1, 1.0 and True into one member."""
    out = set()
    for item in values:
        if jx_type(item) != "string":
            return None, ("a non-string element " + repr(item) + " of JSON type " +
                          jx_type(item) + " reached a string set, where the host "
                          "language would have collapsed equal-hashing values")
        out.add(item)
    return out, None


# ---- aggregation ------------------------------------------------------------

def jx_sorted(values) -> list:
    """Sorted by canonical token.  Total, deterministic, never raises on a
    heterogeneous JSON type set -- and never silently interleaves 1 with 1.0
    the way `sorted` does, because the ordering is over tokens, not numbers."""
    return sorted(values, key=jx_key)


def jx_sorted_by(records, field) -> list:
    """Sort records by the canonical token of one field.

    `sorted(rows, key=lambda r: r["n"])` orders 1 and 1.0 arbitrarily and lets
    the host language decide; ordering by canonical token is total and stable
    and never asks two different JSON types to compare.
    """
    return sorted(records, key=lambda record: jx_key(jx_get(record, field)))


def jx_sorted_homogeneous(values):
    """(sorted, reason).  Refuses a mixed JSON type set BY NAME rather than
    ordering it, because ordering a mixed set is where `min`/`max` launder."""
    kinds = {jx_type(item) for item in values}
    if len(kinds) > 1:
        return None, ("a mixed JSON type set " + repr(sorted(kinds)) +
                      " cannot be ordered; law 18 rejects the type before the "
                      "content is compared")
    if kinds and JX_UNSUPPORTED in kinds:
        return None, "the sequence carries a value outside the JSON universe"
    return jx_sorted(values), None


def jx_sum_int(values):
    """(total, reason).  `sum` over a wire list silently returns a float the
    moment one element is a float.  This refuses instead."""
    total = 0
    for item in values:
        if not jx_int(item):
            return None, ("a non-integer element " + repr(item) + " of JSON type " +
                          jx_type(item) + " reached an integer summation")
        total = total + item
    return total, None


# ---- the published-counter binding ------------------------------------------

def jx_bind(published, measured):
    """THE binding.  Returns None when bound, otherwise a reason string.

    This is the answer to "should a checker compare a measured value against a
    wire-supplied one at all".  It does, and it does it without any numeric
    operator: each side's JSON type is asserted independently and FIRST, and
    the values are then compared as CANONICAL STRINGS.  There is no coercion
    path.  `jx_bind(2538.0, 2538)` is a reason, not a pass, and so is
    `jx_bind(False, 0)`, and so is `jx_bind("2538", 2538)`.
    """
    if not jx_int(measured):
        return ("the value this run MEASURED is " + repr(measured) + ", whose JSON "
                "type is " + jx_type(measured) + " and not an integer; the COMPUTED "
                "side of the comparison is the operand IR-C2V4-01 shows nobody was "
                "checking")
    if not jx_int(published):
        return ("it is published as " + repr(published) + ", whose JSON type is " +
                jx_type(published) + ", not the JSON integer this run measured (" +
                str(measured) + "); freeze section 6 law 18 requires the type to be "
                "rejected before the content is compared, and this is the exact "
                "shape of LB-C2-01, IR-C2V4-01 and IR-C2V5-01")
    if jx_canon(published) != jx_canon(measured):
        return ("it is published as " + repr(published) + " but this run measured " +
                str(measured))
    return None


def jx_bind_text(published, measured):
    """The same binding for a closed STRING scalar.  Law 18 names strings too."""
    if jx_type(measured) != "string":
        return "the value this run measured is not a string but a " + jx_type(measured)
    if jx_type(published) != "string":
        return ("it is published as " + repr(published) + ", whose JSON type is " +
                jx_type(published) + ", not the JSON string this run measured")
    if jx_canon(published) != jx_canon(measured):
        return "it is published as " + repr(published) + " but this run measured " + \
            repr(measured)
    return None


# ---- the operator space, and the primitive that covers each row -------------
# Each row is (id, the host-language operation, the hazard, the jx entry point,
# a live demonstration that the hazard is real, and what jx answers instead).
# `jx_selftest` EXECUTES every demonstration; a row whose hazard stops
# reproducing is a finding, because a table of hazards nobody re-runs is the
# failure mode this whole artifact exists to close.

OPERATOR_SPACE = (
    ("OP-EQ", "a == b", "jx_equal", lambda: 2538.0 == 2538, lambda: jx_equal(2538.0, 2538)),
    ("OP-NE", "a != b", "jx_ne", lambda: not (2538.0 != 2538), lambda: not jx_ne(2538.0, 2538)),
    ("OP-EQ-BOOL", "True == 1", "jx_equal", lambda: True == 1, lambda: jx_equal(True, 1)),
    ("OP-EQ-ZERO", "-0.0 == 0", "jx_equal", lambda: -0.0 == 0, lambda: jx_equal(-0.0, 0)),
    ("OP-EQ-DEPTH-ARRAY", "[1] == [1.0]", "jx_equal", lambda: [1] == [1.0],
     lambda: jx_equal([1], [1.0])),
    ("OP-EQ-DEPTH-OBJECT", '{"a": 1} == {"a": 1.0}', "jx_equal",
     lambda: {"a": 1} == {"a": 1.0}, lambda: jx_equal({"a": 1}, {"a": 1.0})),
    ("OP-LT", "a < b", "jx_lt", lambda: 1 < 1.5, lambda: jx_lt(1, 1.5)),
    ("OP-LE", "a <= b", "jx_le", lambda: 2538 <= 2538.0, lambda: jx_le(2538, 2538.0)),
    ("OP-GT", "a > b", "jx_gt", lambda: 2539 > 2538.0, lambda: jx_gt(2539, 2538.0)),
    ("OP-GE", "a >= b", "jx_ge", lambda: 2538 >= 2538.0, lambda: jx_ge(2538, 2538.0)),
    ("OP-IN-LIST", "x in [..]", "jx_in", lambda: 2538 in [2538.0], lambda: jx_in(2538, [2538.0])),
    ("OP-IN-TUPLE", "x in (..)", "jx_in", lambda: 1 in (1.0,), lambda: jx_in(1, (1.0,))),
    ("OP-IN-SET", "x in {..}", "jx_in", lambda: 2538 in {2538.0}, lambda: jx_in(2538, {2538.0})),
    ("OP-IN-DICTKEY", "k in d", "jx_has", lambda: 1 in {1.0: "x"}, lambda: jx_has({1.0: "x"}, 1)),
    ("OP-NOTIN", "x not in [..]", "jx_not_in", lambda: not (1 not in [1.0]),
     lambda: not jx_not_in(1, [1.0])),
    ("OP-SUBSET", "s <= t", "jx_subset", lambda: {2487} <= {2487.0},
     lambda: jx_subset([2487], [2487.0])),
    ("OP-SUPERSET", "s >= t", "jx_superset", lambda: {2487.0} >= {2487},
     lambda: jx_superset([2487.0], [2487])),
    ("OP-DISJOINT", "s.isdisjoint(t)", "jx_disjoint", lambda: not {1}.isdisjoint({1.0}),
     lambda: not jx_disjoint([1], [1.0])),
    ("OP-DIFFERENCE", "s - t", "jx_difference", lambda: not ({1} - {1.0}),
     lambda: not jx_difference([1], [1.0])),
    ("OP-DEDUP", "set(values)", "jx_unique", lambda: len({1, 1.0, True}) == 1,
     lambda: len(jx_unique([1, 1.0, True])) == 1),
    ("OP-DICT-COLLAPSE", "dict literal key collapse", "jx_keyset",
     lambda: len({1: "a", 1.0: "b", True: "c"}) == 1,
     lambda: len(jx_keyset([1, 1.0, True])) == 1),
    ("OP-GETITEM", "d[k] / d.get(k)", "jx_get", lambda: {1.0: "x"}.get(1) == "x",
     lambda: jx_get({1.0: "x"}, 1) == "x"),
    ("OP-COUNT", "list.count(x)", "jx_count", lambda: [1.0].count(1) == 1,
     lambda: jx_count([1.0], 1) == 1),
    ("OP-INDEX", "list.index(x)", "jx_index", lambda: [1.0].index(1) == 0,
     lambda: jx_index([1.0], 1) == 0),
    ("OP-SORTED", "sorted(values)", "jx_sorted_homogeneous",
     lambda: sorted([1, 1.0]) == [1, 1.0], lambda: jx_sorted_homogeneous([1, 1.0])[0] is not None),
    ("OP-MINMAX", "max(values)", "jx_sorted_homogeneous",
     lambda: jx_type(max([1, 1.0])) == "integer",
     lambda: jx_sorted_homogeneous([1, 1.0])[0] is not None),
    ("OP-SUM", "sum(values)", "jx_sum_int", lambda: jx_type(sum([1, 1.0])) == "number",
     lambda: jx_sum_int([1, 1.0])[0] is not None),
    ("OP-BIND", "published != measured", "jx_bind", lambda: not (2538.0 != 2538),
     lambda: jx_bind(2538.0, 2538) is None),
)

# Row ids whose hazard is demonstrated through a Call rather than an operator,
# so a scan that only walks ast.Compare cannot see them by construction.
OPERATOR_SPACE_CALL_SHAPED = ("OP-IN-DICTKEY", "OP-DISJOINT", "OP-DIFFERENCE",
                              "OP-DEDUP", "OP-DICT-COLLAPSE", "OP-GETITEM",
                              "OP-COUNT", "OP-INDEX", "OP-SORTED", "OP-MINMAX",
                              "OP-SUM")

# The corpus.  Every JSON type, and inside the numeric types every spelling that
# the host language makes equivalent to another.  This is not a spelling
# enumeration standing in for a property: the property is proved by the
# round-trip and by the cross-product, and the corpus only has to be WIDE
# enough to exhibit each equivalence class at least once.
JX_CORPUS = (
    None, True, False,
    0, 1, -1, 2487, 2538, -2538, 10 ** 60,
    0.0, -0.0, 1.0, -1.0, 2487.0, 2538.0, 2538.5, float("inf"), float("-inf"),
    float("nan"),
    "", "0", "1", "2538", "2538.0", "true", "null", "i4:2538", "s1:a",
    [], [1], [1.0], [True], [1, 2], [[1]], [{"a": 1}],
    {}, {"a": 1}, {"a": 1.0}, {"a": True}, {"a": {"b": 1}}, {"1": 1},
)


def jx_selftest() -> dict:
    """Exhaustive over the cross-product of the corpus, with measured counts.

    An adopting checker MUST call this and fail closed unless `escapes` is
    empty.  Nothing here is a spelling enumeration: the round trip proves
    injectivity, and the cross-product measures the divergence from the host
    language's own equality in both directions.
    """
    escapes = []
    corpus = list(JX_CORPUS)
    round_trips = 0
    for value in corpus:
        # Total per value.  A primitive broken badly enough to raise must still
        # let the remaining phases run, because the phase that NAMES the broken
        # entry point comes later and a suite that aborts cannot name anything.
        try:
            token = jx_canon(value)
            back = jx_decanon(token)
            ok = jx_canon(back) == token and jx_type(back) == jx_type(value)
        except Exception as exc:                        # noqa: BLE001 - measured
            escapes.append("round trip raised " + type(exc).__name__ + " on " +
                           repr(value))
            continue
        if not ok:
            escapes.append("round trip lost " + repr(value) + " through " + token)
            continue
        round_trips += 1
    tokens = {}
    collisions = 0
    for value in corpus:
        try:
            token = jx_canon(value)
        except Exception as exc:                        # noqa: BLE001 - measured
            escapes.append("jx_canon raised " + type(exc).__name__ + " on " + repr(value))
            continue
        if token in tokens:
            collisions += 1
            escapes.append("token collision: " + repr(value) + " and " +
                           repr(tokens[token]) + " share " + token)
        tokens[token] = value

    pairs = stricter = looser = agree = 0
    reflexive_failures = 0
    for a in corpus:
        for b in corpus:
            pairs += 1
            mine = jx_equal(a, b)
            try:
                host = bool(a == b)
            except Exception:                               # noqa: BLE001 - measured
                host = None
            if host is mine:
                agree += 1
            elif host and not mine:
                stricter += 1
            else:
                looser += 1
        if not jx_equal(a, a):
            reflexive_failures += 1
            escapes.append("jx_equal is not reflexive at " + repr(a))

    # Every cross-type pair must be refused, at every depth.  This is law 18's
    # actual sentence, executed rather than restated.
    cross_type_admissions = 0
    for a in corpus:
        for b in corpus:
            if jx_type(a) != jx_type(b) and jx_equal(a, b):
                cross_type_admissions += 1
                escapes.append("cross-type admission: " + repr(a) + " (" + jx_type(a) +
                               ") equals " + repr(b) + " (" + jx_type(b) + ")")

    # The gates, over the whole corpus.
    gate_cases = gate_admissions = 0
    for value in corpus:
        gate_cases += 1
        for gate, admits in (
                ("jx_int", lambda item: jx_int(item) and jx_type(item) != "integer"),
                ("jx_exact_int", lambda item: jx_exact_int(item, 2538) and
                 jx_canon(item) != jx_canon(2538)),
                ("jx_int_in_range", lambda item: jx_int_in_range(item, 0, 10 ** 6) and
                 jx_type(item) != "integer"),
                ("jx_bind", lambda item: jx_bind(item, 2538) is None and
                 jx_canon(item) != jx_canon(2538)),
                ("jx_bind/measured", lambda item: jx_bind(2538, item) is None and
                 jx_canon(item) != jx_canon(2538))):
            # Per gate, per value, total.  A gate stripped of its type check
            # raises on some corpus members and admits others; both are the
            # same finding and neither may abort the suite before the entry
            # point block names which gate it was.
            try:
                admitted_here = bool(admits(value))
            except Exception as exc:                    # noqa: BLE001 - measured
                gate_admissions += 1
                escapes.append(gate + " raised " + type(exc).__name__ + " on " +
                               repr(value) + "; a gate that raises instead of "
                               "refusing is not a gate")
                continue
            if admitted_here:
                gate_admissions += 1
                escapes.append(gate + " admitted " + repr(value) + ", whose JSON type "
                               "is " + jx_type(value))

    # The operator space: the hazard must still reproduce, and jx must answer
    # differently.  A row whose hazard has stopped reproducing is reported,
    # because it would silently become a row that proves nothing.
    rows = hazards = covered = 0
    for row_id, _spelling, entry, hazard, repaired in OPERATOR_SPACE:
        rows += 1
        try:
            hazard_live = bool(hazard())
        except Exception as exc:                            # noqa: BLE001 - measured
            hazard_live = False
            escapes.append(row_id + ": the hazard demonstration raised " +
                           type(exc).__name__)
        try:
            repaired_live = bool(repaired())
        except Exception as exc:                            # noqa: BLE001 - measured
            repaired_live = True
            escapes.append(row_id + ": the " + entry + " demonstration raised " +
                           type(exc).__name__)
        if hazard_live:
            hazards += 1
        else:
            escapes.append(row_id + ": the host-language hazard no longer "
                           "reproduces, so this row proves nothing")
        if not repaired_live:
            covered += 1
        else:
            escapes.append(row_id + ": " + entry + " answers the same way the "
                           "host language does, so the row is not covered")

    # Every entry point of the primitive, with a case that DISTINGUISHES it from
    # the host-language operation it replaces.  Without this an accessor could be
    # rewritten to the host spelling and nothing would notice, which is exactly
    # the shape of IR-C2V5-02: three of v5's five declared gates could be
    # stripped with zero findings.
    entry_cases = entry_failures = 0
    for label, produce, expected in (
            ("jx_type/boolean", lambda: jx_type(True), "boolean"),
            ("jx_type/integer", lambda: jx_type(1), "integer"),
            ("jx_type/number", lambda: jx_type(1.0), "number"),
            ("jx_frame", lambda: jx_frame("s", "ab"), "s2:ab"),
            ("jx_canon/tagged", lambda: jx_canon(1) != jx_canon(1.0), True),
            ("jx_canon/token", lambda: jx_canon(2538), "i4:2538"),
            ("jx_canon/depth", lambda: jx_canon([1]) != jx_canon([1.0]), True),
            ("jx_decanon", lambda: jx_decanon(jx_canon(2538.0)), 2538.0),
            ("jx_decanon/type", lambda: jx_type(jx_decanon(jx_canon(2538))), "integer"),
            ("jx_in_domain/set", lambda: jx_in_domain(set()), False),
            ("jx_in_domain/list", lambda: jx_in_domain([1]), True),
            ("jx_key/distinguishes", lambda: jx_key(1) != jx_key(True), True),
            ("jx_key/is-a-string", lambda: jx_type(jx_key(1)), "string"),
            ("jx_key/is-jx_canon", lambda: jx_key(2538) == jx_canon(2538), True),
            ("jx_key/is-jx_canon-at-depth",
             lambda: jx_key([1, {"a": 2}]) == jx_canon([1, {"a": 2}]), True),
            ("jx_equal", lambda: jx_equal(2538, 2538.0), False),
            ("jx_ne", lambda: jx_ne(2538, 2538.0), True),
            ("jx_same_type", lambda: jx_same_type(1, 1.0), False),
            ("jx_int/boolean", lambda: jx_int(True), False),
            ("jx_exact_int/float", lambda: jx_exact_int(2538.0, 2538), False),
            ("jx_exact_int/control", lambda: jx_exact_int(2538, 2538), True),
            ("jx_int_in_range/float", lambda: jx_int_in_range(5.0, 1, 10), False),
            ("jx_int_in_range/control", lambda: jx_int_in_range(5, 1, 10), True),
            ("jx_finite_number/inf", lambda: jx_finite_number(float("inf")), False),
            ("jx_finite_number/control", lambda: jx_finite_number(1.5), True),
            ("jx_order/cross-type", lambda: jx_order(1, 1.0), None),
            ("jx_order/control", lambda: jx_order(1, 2), -1),
            ("jx_lt", lambda: jx_lt(1, 1.5), False),
            ("jx_le", lambda: jx_le(2538, 2538.0), False),
            ("jx_gt", lambda: jx_gt(2539, 2538.0), False),
            ("jx_ge", lambda: jx_ge(2538, 2538.0), False),
            ("jx_keyset/cardinality", lambda: len(jx_keyset([1, 1.0, True])), 3),
            ("jx_in", lambda: jx_in(2538, [2538.0]), False),
            ("jx_in/control", lambda: jx_in(2538, [2538]), True),
            ("jx_not_in", lambda: jx_not_in(1, [1.0]), True),
            ("jx_subset", lambda: jx_subset([2487], [2487.0]), False),
            ("jx_subset/control", lambda: jx_subset([2487], [2487]), True),
            ("jx_superset", lambda: jx_superset([2487.0], [2487]), False),
            ("jx_disjoint", lambda: jx_disjoint([1], [1.0]), True),
            ("jx_difference", lambda: jx_difference([1], [1.0]), [1]),
            ("jx_unique/cardinality", lambda: len(jx_unique([1, 1.0, True])), 3),
            ("jx_count", lambda: jx_count([1.0], 1), 0),
            ("jx_count/control", lambda: jx_count([1, 1], 1), 2),
            ("jx_index", lambda: jx_index([1.0], 1), None),
            ("jx_index/control", lambda: jx_index([0, 1], 1), 1),
            ("jx_has", lambda: jx_has({1.0: "x"}, 1), False),
            ("jx_has/control", lambda: jx_has({"a": 1}, "a"), True),
            ("jx_get", lambda: jx_get({1.0: "x"}, 1), None),
            ("jx_get/control", lambda: jx_get({"a": "x"}, "a"), "x"),
            ("jx_at/object", lambda: jx_at({1.0: "x"}, 1), None),
            ("jx_at/array", lambda: jx_at([10, 20], 1), 20),
            ("jx_at/float-index", lambda: jx_at([10, 20], 1.0), None),
            ("jx_has_at/float-index", lambda: jx_has_at([10, 20], 1.0), False),
            ("jx_has_at/control", lambda: jx_has_at([10, 20], 1), True),
            ("jx_put/float-index", lambda: jx_put([10, 20], 1.0, 9), False),
            ("jx_put/control", lambda: jx_put([10, 20], 1, 9), True),
            ("jx_sorted/by-token", lambda: jx_sorted([1.0, 1]), [1, 1.0]),
            ("jx_sorted/token-order", lambda: jx_sorted([10, 2]), [2, 10]),
            ("jx_sorted_by", lambda: jx_sorted_by([{"k": 1.0}, {"k": 1}], "k"),
             [{"k": 1}, {"k": 1.0}]),
            ("jx_sorted_homogeneous/mixed", lambda: jx_sorted_homogeneous([1, 1.0])[0], None),
            ("jx_sorted_homogeneous/control", lambda: jx_sorted_homogeneous([2, 1])[0], [1, 2]),
            ("jx_sum_int/float", lambda: jx_sum_int([1, 1.0])[0], None),
            ("jx_sum_int/control", lambda: jx_sum_int([1, 2])[0], 3),
            ("jx_string_set/number", lambda: jx_string_set(["a", 1])[0], None),
            ("jx_string_set/control", lambda: jx_string_set(["a"])[1], None),
            ("jx_bind/float", lambda: jx_bind(2538.0, 2538) is None, False),
            ("jx_bind/boolean", lambda: jx_bind(False, 0) is None, False),
            ("jx_bind/string", lambda: jx_bind("2538", 2538) is None, False),
            ("jx_bind/control", lambda: jx_bind(2538, 2538) is None, True),
            ("jx_bind_text/number", lambda: jx_bind_text(1, "1") is None, False),
            ("jx_bind_text/drift", lambda: jx_bind_text("a", "b") is None, False),
            ("jx_bind_text/control", lambda: jx_bind_text("a", "a") is None, True),
    ):
        entry_cases += 1
        try:
            actual = produce()
            same = jx_type(actual) == jx_type(expected) and \
                jx_canon(actual) == jx_canon(expected)
        except Exception as exc:                        # noqa: BLE001 - measured
            entry_failures += 1
            escapes.append("entry point " + label + " raised " + type(exc).__name__ +
                           "; the primitive no longer answers for the operation it "
                           "replaces")
            continue
        if not same:
            entry_failures += 1
            escapes.append("entry point " + label + " answered " + repr(actual) +
                           " where " + repr(expected) + " is required; the primitive "
                           "no longer differs from the host-language operation it "
                           "replaces")

    # Domain totality: a value outside the JSON universe must be refused by
    # name, never silently compared.
    domain_refusals = 0
    for outside in (set(), (1, 2), b"x", 1 + 2j, jx_canon):
        try:
            if not jx_in_domain(outside):
                domain_refusals += 1
            else:
                escapes.append("jx_in_domain admitted a " + type(outside).__name__ +
                               ", which is outside the JSON value universe")
            if jx_equal(outside, outside) or jx_equal(outside, 1):
                escapes.append("a value outside the JSON universe was admitted as equal")
        except Exception as exc:                        # noqa: BLE001 - measured
            escapes.append("jx_in_domain or jx_equal raised " + type(exc).__name__ +
                           " on a " + type(outside).__name__ + " instead of refusing it")
        try:
            jx_canon(outside)
            escapes.append("jx_canon did not refuse " + type(outside).__name__)
        except JxDomainError:
            pass
        except Exception as exc:                        # noqa: BLE001 - measured
            escapes.append("jx_canon raised " + type(exc).__name__ + " rather than a "
                           "named domain refusal on a " + type(outside).__name__)

    return {
        "corpusValues": len(corpus),
        "corpusPairs": pairs,
        "roundTrips": round_trips,
        "distinctTokens": len(tokens),
        "tokenCollisions": collisions,
        "stricterThanHostEquality": stricter,
        "looserThanHostEquality": looser,
        "agreeWithHostEquality": agree,
        "reflexiveFailures": reflexive_failures,
        "crossTypeAdmissions": cross_type_admissions,
        "gateCases": gate_cases,
        "gateAdmissions": gate_admissions,
        "operatorSpaceRows": rows,
        "operatorSpaceHazardsReproduced": hazards,
        "operatorSpaceRowsCovered": covered,
        "entryPointCases": entry_cases,
        "entryPointFailures": entry_failures,
        "domainRefusals": domain_refusals,
        "escapes": escapes,
    }


# --- END JX PRIMITIVE ---


# =============================================================================
# Section 2.  L0 -- hash before execution.
#
# Freeze section 7.2 recording obligation: filename AND digest for every input
# this verdict depends on.  A count is not a record.  Every entry is read once
# as inert bytes, verified, and then parsed or executed from that verified byte
# string -- never a second disk read between verification and execution.
# =============================================================================

V4_CHECKER = "check-c2-v4.py"
V4_CONTRACT = "c2-plan-stage-schema.v4.json"
V5_CHECKER = "check-c2-v5.py"
V5_CONTRACT = "c2-plan-stage-schema.v5.json"
V5_REVIEW = "c2-plan-stage-schema.v5.review-independent.json"
ADJUDICATION = "c2-plan-stage-schema.v4.adjudication-ir-c2v4-01.json"
PREFREEZE_REVIEW = "c2-plan-stage-schema.v4.review-independent-prefreeze.json"
V3_REVIEW = "c2-plan-stage-schema.v3.review-independent-livebytes.json"
V3_CONTRACT = "c2-plan-stage-schema.v3.json"
V3_CHECKER = "check-c2.py"
D9 = "d9-exit-contract.v1.6.json"
FP = "fact-plane.v1.json"
TM = "threat-model.v3.json"
OP = "operability.v2.json"
DELIVERY = "delivery.v2.json"
RESOLVED_INPUTS = "resolved-inputs.v2.json"

PINS: dict[str, str] = {
    V4_CHECKER: "54ff764d155f5582bc66fd7bf8138b7eaed5f90f46b92975c4bc7a85ffb3df17",
    V4_CONTRACT: "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    V5_CHECKER: "3518a9c1253a09300bc76c0f13a88e133f0dd2f3589f45e724c2da8e1971a081",
    V5_CONTRACT: "fe5748963db1724123dbc82b2381feb708d8f3836de6f99e10ca3134534547bd",
    V5_REVIEW: "b8ec85cf46b2e2ae7e9e8a1f5b56b26a83e014d6c59f99d77798040284c4a92c",
    ADJUDICATION: "211a7798a621341191b296c1e7c5308ca2e87657b72b7295261ce0d5cac49851",
    PREFREEZE_REVIEW: "c74612ef4519750aa529db543c2f0cc81fce50d57c3d636486fd2f0ddc0c41f3",
    V3_REVIEW: "0f297bed7d8c83e6bd96e54fe40bcda14281b3e4bcedf96e1173d14fbe60a3a3",
    V3_CONTRACT: "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    V3_CHECKER: "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3",
    D9: "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    FP: "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    TM: "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    OP: "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    DELIVERY: "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    RESOLVED_INPUTS: "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
}

# A repair lane that quietly points at a softened disposition is refused at
# load, not reported.  v6 discharges TWO dispositions and both are pinned.
ADJUDICATION_BINDING = {
    "findingId": "IR-C2V4-01",
    "disposition": "BLOCKING",
    "artifact": "c2-plan-stage-schema.v4.adjudication-ir-c2v4-01",
}
V5_REVIEW_BINDING = {
    "artifact": "opensip.c2-plan-stage-schema.v5.review-independent",
}
# The four blockers of the REJECT this successor exists to repair.  If the
# pinned review stops carrying all four, or stops grading them BLOCKING, this
# checker refuses to run rather than reporting a repair of something else.
V5_BLOCKER_IDS = ("IR-C2V5-01", "IR-C2V5-02", "IR-C2V5-03", "IR-C2V5-04")
V3_REVIEW_BINDING = {"verdict": "REJECT", "blockingFindingCount": 2}

MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
    ZeroDivisionError, OverflowError, RecursionError, JxDomainError,
)

# The declared law-18 gates.  Scanning the body of `jx_int` for the absence of
# a type gate is circular: it IS the gate.  The exclusion is not free coverage;
# L7 breaks EVERY ONE of these in turn and requires each break to be detected
# by the layer it breaks, with the counters republished.  v5 declared this debt
# and paid two fifths of it (IR-C2V5-02); the matrix below pays all of it.
GUARD_HELPERS = (
    "jx_type", "jx_canon", "jx_decanon", "jx_frame", "jx_in_domain", "jx_key",
    "jx_equal", "jx_ne", "jx_same_type", "jx_int", "jx_exact_int",
    "jx_int_in_range", "jx_finite_number", "jx_order", "jx_lt", "jx_le",
    "jx_gt", "jx_ge", "jx_keyset", "jx_in", "jx_not_in", "jx_subset",
    "jx_superset", "jx_disjoint", "jx_difference", "jx_unique", "jx_count",
    "jx_index", "jx_has", "jx_get", "jx_at", "jx_has_at", "jx_put",
    "jx_string_set", "jx_sorted", "jx_sorted_by", "jx_sorted_homogeneous",
    "jx_sum_int", "jx_bind", "jx_bind_text",
)
TYPE_GATES = GUARD_HELPERS + ("isinstance",)
# The only two exec() sites this file permits: the verified-snapshot module
# loader and the self-mutation tree executor.  Both compile bytes that were
# hash-verified or derived from this file's own verified-at-read tree.  L4
# counts them and refuses any third.  Nothing here evaluates caller input.
DECLARED_EXEC_SITES = 2
NON_NUMERIC_CLASSES = frozenset({"str", "bytes", "dict", "list", "tuple", "set",
                                 "frozenset", "type(None)"})
_AST_CLASS_GATES = frozenset({"ast.AST", "ast.stmt", "ast.expr", "ast.Name",
                              "ast.Call", "ast.Attribute", "ast.Constant"})


class AuthorityLoadError(RuntimeError):
    """A pinned input could not be admitted as authority."""


class PinMismatch(AuthorityLoadError):
    """A pinned byte string does not hash to its declared digest."""


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this checker does not accept."""


class _VerifiedSourceLoader:
    """Execute exactly the bytes that were hash-verified, never a re-read."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec):
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_snapshot(name: str, filename: str, source: bytes,
                      directory: pathlib.Path) -> types.ModuleType:
    path = (directory / filename).resolve()
    loader = _VerifiedSourceLoader(path, source)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    if spec is None or spec.loader is None:
        raise AuthorityLoadError("cannot construct a verified spec for " + filename)
    module = importlib.util.module_from_spec(spec)
    prior = sys.modules.get(name)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if prior is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = prior
    return module


class Authority:
    """Everything admitted after hash verification, and nothing else.

    `pinned` caches results that are a pure function of hash-verified bytes and
    of nothing else -- the whole-document predecessor sweep and the v5
    false-accept admissions.  Caching those is sound precisely because no
    mutation of THIS file can change them; a mutation that targets the code
    computing them clears the entry explicitly (see SWEEP_SENSITIVE).
    """

    def __init__(self, snapshots, parsed, v4, v4_authority, directory):
        self.snapshots = snapshots
        self.parsed = parsed
        self.v4 = v4
        self.v4_authority = v4_authority
        self.directory = directory
        self.pinned = {}
        self.measurement = None
        self.scan_self = None
        self.scan_predecessor = None
        self.scan_v5 = None
        self.behavioural = None
        self.differential = None
        self.successor = None
        self.document_lock = None
        self.candidate_lock = None
        self.sweep = None
        self.primitive = None
        self.effective = None
        self.banner = None
        self.base = None
        self.live = None
        self.partial_live = None
        self.portability = {"freeNames": 0, "names": []}
        self.document_name = BINDING

    def json(self, name: str):
        return self.parsed.get(name)


def load_authority(directory: pathlib.Path = HERE) -> Authority:
    """Read every pinned input as inert bytes, verify, then execute."""
    snapshots: dict[str, bytes] = {}
    errors: list[str] = []
    for name in sorted(PINS):
        expected = PINS[name]
        try:
            source = (directory / name).read_bytes()
        except OSError as exc:
            errors.append(name + ": read " + type(exc).__name__ + ": " + str(exc))
            continue
        actual = hashlib.sha256(source).hexdigest()
        if jx_bind_text(actual, expected) is not None:
            errors.append(name + ": " + actual + " != " + expected)
            continue
        snapshots[name] = source
    if errors:
        raise PinMismatch("; ".join(sorted(errors)))

    parsed: dict[str, object] = {}
    for name in sorted(PINS):
        if name.endswith(".json"):
            try:
                parsed[name] = json.loads(snapshots[name].decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise AuthorityLoadError(
                    "cannot parse pinned data " + name + ": " + type(exc).__name__) from exc

    _refuse_softened_provenance(parsed)

    sink = io.StringIO()
    with redirect_stdout(sink):
        v4 = _execute_snapshot("opensip_c2v6_pinned_v4_checker", V4_CHECKER,
                               snapshots[V4_CHECKER], directory)
        v4._OWN_TREE_CACHE = ast.parse(snapshots[V4_CHECKER])
        v3_module = v4._execute_snapshot("opensip_c2v6_pinned_v3_checker", V3_CHECKER,
                                         snapshots[V3_CHECKER])
    _refuse_pin_table_disagreement(v4)
    v4_authority = v4.Authority(dict(snapshots), dict(parsed), {V3_CHECKER: v3_module})
    return Authority(snapshots, parsed, v4, v4_authority, directory)


def _refuse_softened_provenance(parsed) -> None:
    """Both dispositions v6 discharges are read from pinned bytes, by name."""
    adjudication = parsed.get(ADJUDICATION)
    if jx_type(adjudication) != "object":
        raise AuthorityLoadError("pinned adjudication " + ADJUDICATION +
                                 " is not a JSON object")
    for key in sorted(ADJUDICATION_BINDING):
        expected = ADJUDICATION_BINDING[key]
        if jx_bind_text(adjudication.get(key), expected) is not None:
            raise AuthorityLoadError(
                "pinned adjudication " + ADJUDICATION + " carries " + key + "=" +
                repr(adjudication.get(key)) + ", not " + repr(expected) + "; this "
                "successor exists only to discharge a BLOCKING disposition and "
                "refuses to run against a softened one")
    review = parsed.get(V5_REVIEW)
    if jx_type(review) != "object":
        raise AuthorityLoadError("pinned review " + V5_REVIEW + " is not a JSON object")
    for key in sorted(V5_REVIEW_BINDING):
        if jx_bind_text(review.get(key), V5_REVIEW_BINDING[key]) is not None:
            raise AuthorityLoadError(
                "pinned review " + V5_REVIEW + " carries " + key + "=" +
                repr(review.get(key)) + ", not " + repr(V5_REVIEW_BINDING[key]))
    verdict = review.get("verdict")
    if jx_type(verdict) != "string" or "REJECT" not in verdict:
        raise AuthorityLoadError(
            "pinned review " + V5_REVIEW + " no longer carries the REJECT verdict "
            "this successor exists to repair")
    blockers = review.get("blockers")
    blockers = blockers if jx_type(blockers) == "array" else []
    ids = [item.get("id") for item in blockers if jx_type(item) == "object"]
    graded = [item for item in blockers if jx_type(item) == "object"]
    missing = [name for name in V5_BLOCKER_IDS if not jx_in(name, ids)]
    if missing:
        raise AuthorityLoadError(
            "pinned review " + V5_REVIEW + " does not carry the blocking findings "
            "this successor exists to repair: " + repr(missing))
    softened = []
    for name in V5_BLOCKER_IDS:
        rows = [item for item in graded if jx_equal(item.get("id"), name)]
        if not rows or jx_bind_text(rows[0].get("severity"), "BLOCKING") is not None:
            softened.append(name)
    if softened:
        raise AuthorityLoadError(
            "pinned review " + V5_REVIEW + " no longer grades " + repr(softened) +
            " BLOCKING; this successor refuses to run against a softened disposition")
    v3_review = parsed.get(V3_REVIEW)
    v3_review = v3_review if jx_type(v3_review) == "object" else {}
    if jx_bind_text(v3_review.get("verdict"), V3_REVIEW_BINDING["verdict"]) is not None \
            or not jx_exact_int(v3_review.get("blockingFindingCount"),
                                V3_REVIEW_BINDING["blockingFindingCount"]):
        raise AuthorityLoadError(
            "pinned review " + V3_REVIEW + " no longer carries the REJECT verdict and "
            "the two blocking findings the C-2 repair chain is anchored to")
    if jx_type(parsed.get(PREFREEZE_REVIEW)) != "object":
        raise AuthorityLoadError("pinned review " + PREFREEZE_REVIEW +
                                 " is not a JSON object")


def _refuse_pin_table_disagreement(v4) -> None:
    """This pin table must agree with the predecessor's, digit for digit."""
    inherited = getattr(v4, "PINS", None)
    if jx_type(inherited) != "object" or not inherited:
        raise AuthorityLoadError("the pinned predecessor exposes no PINS table")
    disagreements = []
    for name in jx_sorted(list(inherited)):
        if not jx_has(PINS, name):
            continue
        reason = jx_bind_text(inherited[name], jx_get(PINS, name))
        if reason is not None:
            disagreements.append(name + ": v4 pins " + repr(inherited[name]) +
                                 ", v6 pins " + repr(jx_get(PINS, name)))
    if disagreements:
        raise AuthorityLoadError("pin tables disagree - " + "; ".join(disagreements))
    unshared = jx_sorted(jx_difference(list(inherited), list(PINS)))
    if unshared:
        raise AuthorityLoadError(
            "the predecessor depends on inputs this successor does not record, which "
            "would break the recording obligation: " + repr(unshared))


# =============================================================================
# Section 3.  The derivation.  The effective v6 contract is the VERIFIED v4
# document with a typed, self-verifying operation list applied.  Nothing is
# transcribed; every `set` op restates the byte it replaces and is refused if
# the verified predecessor does not hold that value -- type-exactly, through
# `jx_equal`, at any depth.
# =============================================================================

_STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")
DECLARED_OPS = ("set", "add")
DECLARED_PROJECTION_FIELDS = (
    ("version", 4),
    ("supersedes", 3),
    ("checkerModeContract.checker", "check-c2-v4.py"),
)


def _path_steps(path: str) -> list:
    return [int(index) if index else name for index, name in _STEP_RE.findall(path)]


def _steps_text(steps) -> str:
    """Canonical text of a path.  Annotated `-> str` and behaviourally probed by
    L5, which is what lets L4 treat a call to it as provably non-numeric."""
    return "/".join(str(step) for step in steps)


def _resolve_steps(root, steps):
    """Walk a parsed document by steps, type-exactly.

    `node[step]` is a hash lookup when `node` is an object, and `{1.0: x}[1]`
    succeeds in the host language.  `jx_has_at`/`jx_at` decide membership and
    retrieval on CANONICAL keys, so a float step cannot reach an integer key.
    """
    node = root
    for step in steps:
        if not jx_has_at(node, step):
            raise KeyError(_steps_text(list(steps)))
        node = jx_at(node, step)
    return node


def _assign_steps(root, steps, value) -> None:
    node = root
    for step in steps[:-1]:
        if not jx_has_at(node, step):
            raise KeyError(_steps_text(list(steps)))
        node = jx_at(node, step)
    if not jx_put(node, steps[-1], value):
        raise KeyError(_steps_text(list(steps)))


def apply_derivation(base, operations):
    """Return (effective, findings).  Every op is checked against the base."""
    effective = copy.deepcopy(base)
    findings = []
    if jx_type(operations) != "array" or not operations:
        return effective, ["C2V6-DERIVATION: derivedFrom.operations must be a non-empty "
                           "JSON array; the effective contract is not derivable"]
    for index, op in enumerate(operations):
        if jx_type(op) != "object":
            findings.append("C2V6-DERIVATION: operation " + str(index) +
                            " is not a JSON object")
            continue
        kind, path = op.get("op"), op.get("path")
        if not jx_in(kind, DECLARED_OPS) or jx_type(path) != "string" or not path:
            findings.append("C2V6-DERIVATION: operation " + str(index) + " declares op=" +
                            repr(kind) + " path=" + repr(path) + "; the declared ops are " +
                            repr(list(DECLARED_OPS)))
            continue
        if not jx_has(op, "value"):
            findings.append("C2V6-DERIVATION: operation " + str(index) + " at " + path +
                            " carries no value")
            continue
        steps = _path_steps(path)
        try:
            if jx_equal(kind, "set"):
                current = _resolve_steps(effective, steps)
                if not jx_equal(current, op.get("from")):
                    findings.append(
                        "C2V6-DERIVATION: operation " + str(index) + " at " + path +
                        " declares it replaces " + repr(op.get("from")) + " (" +
                        jx_type(op.get("from")) + ") but the verified predecessor holds " +
                        repr(current) + " (" + jx_type(current) + "); the derivation does "
                        "not describe the bytes it is applied to")
                    continue
                _assign_steps(effective, steps, copy.deepcopy(op["value"]))
            else:
                parent = _resolve_steps(effective, steps[:-1])
                if jx_has_at(parent, steps[-1]):
                    findings.append("C2V6-DERIVATION: operation " + str(index) + " adds " +
                                    path + ", which already exists in the predecessor")
                    continue
                if not jx_put(parent, steps[-1], copy.deepcopy(op["value"])):
                    findings.append("C2V6-DERIVATION: operation " + str(index) +
                                    " cannot add " + path + " type-exactly")
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append("C2V6-DERIVATION: operation " + str(index) + " at " + path +
                            " does not resolve against the verified predecessor (" +
                            type(exc).__name__ + ")")
    return effective, findings


def project_to_v4_identity(effective, projection):
    """Restore exactly the identity fields the inherited oracle is pinned to."""
    projected = copy.deepcopy(effective)
    fields = projection.get("fields") if jx_type(projection) == "object" else None
    findings = []
    if jx_type(fields) != "object" or not fields:
        return projected, ["C2V6-PROJECTION: v4InheritanceProjection.fields must be a "
                           "non-empty JSON object"]
    if not jx_equal(fields, dict(DECLARED_PROJECTION_FIELDS)):
        findings.append(
            "C2V6-PROJECTION: the declared projection is " + repr(fields) + "; this "
            "checker admits exactly " + repr(dict(DECLARED_PROJECTION_FIELDS)) + " and "
            "nothing else, because a projection carrying any other field is a second "
            "contract the inherited oracle would be validating instead of this one")
        return projected, findings
    for path in jx_sorted(list(fields)):
        try:
            _assign_steps(projected, _path_steps(path), copy.deepcopy(fields[path]))
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append("C2V6-PROJECTION: " + path + " does not resolve (" +
                            type(exc).__name__ + ")")
    drift = jx_sorted(_wire_diff_paths(effective, projected))
    declared = jx_sorted(list(fields))
    if not jx_equal(drift, declared):
        findings.append("C2V6-PROJECTION: the projection handed to the inherited oracle "
                        "differs from the effective contract at " + repr(drift) + ", but "
                        "declares only " + repr(declared) + "; a projection that changes "
                        "anything beyond the declared identity fields is a second contract")
    return projected, findings


def _wire_diff_paths(left, right, prefix="") -> list:
    """Every path at which two parsed documents differ, type-exactly."""
    if not jx_same_type(left, right):
        return [prefix]
    if jx_type(left) == "object":
        out = []
        for key in jx_sorted(jx_unique(list(left) + list(right))):
            here = prefix + "." + str(key) if prefix else str(key)
            if not jx_has(left, key) or not jx_has(right, key):
                out.append(here)
            else:
                out.extend(_wire_diff_paths(jx_get(left, key), jx_get(right, key), here))
        return out
    if jx_type(left) == "array":
        if not jx_bind(len(left), len(right)) is None:
            return [prefix]
        out = []
        for index, item in enumerate(left):
            out.extend(_wire_diff_paths(item, right[index],
                                        prefix + "[" + str(index) + "]"))
        return out
    return [] if jx_equal(left, right) else [prefix]


# =============================================================================
# Section 4.  L2 / L3 -- the repair and the register.
#
# The position set is DERIVED from the live measurement, never hand-listed, so
# a counter that appears in the measurement without appearing in the register
# is a finding and a counter registered without being measured is a finding.
# =============================================================================

CENSUS_STAT_KEYS = ("executedCases", "unguardedEscapes", "guardedEscapes",
                    "silentAccepts", "admitThenRaise",
                    "typeDistinctConstantAdmissions")
CENSUS_SITE_LINE_2487 = "surfaces-census"
CENSUS_SITE_LINE_2493 = "surfaces-stats"
CENSUS_SITE_LINE_2517 = "contract-root"


def measure(effective, authority):
    """The measured side, computed by the PINNED predecessor's instrument.

    v6 authors the comparison; v4 -- reviewed, pinned, and confirmed sound at
    the wire surface by the adjudication -- provides the measurement.  Keeping
    those in different, separately reviewed bytes is deliberate and is named as
    a trust relationship in RES-C2V6-04.
    """
    v4 = authority.v4
    fp = authority.json(FP)
    relations, reason = jx_string_set(_resolve_steps(
        fp, ("relationRegistry", "relations")) if fp else [])
    if reason is not None:
        relations = set()
    values = v4._matrix_values(effective.get("planIntentTotalityMatrix", {}))
    intent_values, _ = v4._intent_fixture_values(effective)
    surfaces = v4.measure_surfaces(effective, relations, fp, values, intent_values)
    root_census, _root_stats = v4.measure_contract_root(
        effective, authority.v4_authority, execute=False)
    return {"surfaces": surfaces, "contractRoot": root_census}


def measured_positions(measurement) -> dict:
    """(position -> measured value), derived from the measurement itself."""
    positions = {}
    for name in jx_sorted(list(measurement["surfaces"])):
        entry = measurement["surfaces"][name]
        for key in jx_sorted(list(entry["census"])):
            positions["surfaces[" + name + "]." + key] = entry["census"][key]
        for key in CENSUS_STAT_KEYS:
            positions["surfaces[" + name + "]." + key] = entry["stats"][key]
    for key in jx_sorted(list(measurement["contractRoot"])):
        positions["contractRoot." + key] = measurement["contractRoot"][key]
    return positions


def census_site_positions(measurement) -> dict:
    """Which of the predecessor's three ungated comparisons reads each position.

    This is what makes the candidate's per-site `wireIntegerPositionsRead`
    figures MEASURED rather than transcribed.  check-c2-v4.py line 2487
    iterates the per-surface census map, line 2493 iterates the per-surface
    stat block, line 2517 iterates the contract-root map.
    """
    sites = {CENSUS_SITE_LINE_2487: [], CENSUS_SITE_LINE_2493: [],
             CENSUS_SITE_LINE_2517: []}
    for name in jx_sorted(list(measurement["surfaces"])):
        entry = measurement["surfaces"][name]
        for key in jx_sorted(list(entry["census"])):
            sites[CENSUS_SITE_LINE_2487].append("surfaces[" + name + "]." + key)
        for key in CENSUS_STAT_KEYS:
            sites[CENSUS_SITE_LINE_2493].append("surfaces[" + name + "]." + key)
    for key in jx_sorted(list(measurement["contractRoot"])):
        sites[CENSUS_SITE_LINE_2517].append("contractRoot." + key)
    return sites


def published_value(effective, position):
    """Read one published counter out of the candidate.  May be absent."""
    block = effective.get("hostileScalarLeafTotality", {})
    if jx_type(block) != "object":
        return None, False
    if position.startswith("surfaces["):
        name, _, key = position[len("surfaces["):].partition("].")
        rows = block.get("surfaces")
        rows = rows if jx_type(rows) == "array" else []
        for row in rows:
            if jx_type(row) == "object" and jx_equal(row.get("id"), name):
                return jx_get(row, key), jx_has(row, key)
        return None, False
    key = position[len("contractRoot."):]
    root = block.get("contractRoot")
    root = root if jx_type(root) == "object" else {}
    return jx_get(root, key), jx_has(root, key)


def census_comparison_findings(effective, measurement) -> list:
    """L2.  The repair.  ONE acceptance path, and it is `jx_bind`.

    Every branch below is a rejection, so weakening the gate cannot be hidden
    behind a redundant second test -- which is what made the predecessor's
    inline checks look load-bearing.
    """
    findings = []
    positions = measured_positions(measurement)
    for position in jx_sorted(list(positions)):
        measured_value = jx_get(positions, position)
        published, present = published_value(effective, position)
        if not present:
            findings.append("C2V6-CENSUS: " + position + " is measured by this run at " +
                            repr(measured_value) + " but the candidate publishes no "
                            "value for it")
            continue
        reason = jx_bind(published, measured_value)
        if reason is None:
            continue
        if not jx_int(measured_value):
            findings.append("C2V6-INSTRUMENT: " + position + ": " + reason)
        elif not jx_int(published):
            findings.append("C2V6-TYPE: " + position + ": " + reason)
        else:
            findings.append("C2V6-CENSUS: " + position + ": " + reason)
    return findings


def register_findings(effective, measurement, authority) -> list:
    """L3.  The register must equal the measurement, in both directions."""
    findings = []
    spec = effective.get("planIntent", {})
    spec = spec.get("integerConstantRegisterV6") if jx_type(spec) == "object" else None
    if jx_type(spec) != "object":
        findings.append("C2V6-REGISTER: the effective contract declares no "
                        "planIntent.integerConstantRegisterV6; the census counters the "
                        "adjudication names as the fifth site would be unregistered")
        return findings
    raw_inherited = spec.get("inheritedFromV4")
    declared_inherited = raw_inherited if jx_type(raw_inherited) == "array" else []
    predecessor_ids = list(
        getattr(authority.v4, "DECLARED_INTEGER_CONSTANT_IDS", frozenset()))
    if not jx_equal(jx_sorted(jx_unique(declared_inherited)),
                    jx_sorted(jx_unique(predecessor_ids))):
        findings.append(
            "C2V6-REGISTER: the inherited half of the register is " +
            repr(jx_sorted(declared_inherited)) + " but the executed predecessor "
            "declares " + repr(jx_sorted(predecessor_ids)) + "; the v4 register may not "
            "be narrowed, widened or restated by this successor")
    raw_added = spec.get("censusCounterPositions")
    declared_added = raw_added if jx_type(raw_added) == "array" else []
    measured = list(measured_positions(measurement))
    missing = jx_sorted(jx_difference(measured, declared_added))
    extra = jx_sorted(jx_difference(declared_added, measured))
    if missing:
        findings.append("C2V6-REGISTER: " + str(len(missing)) + " published counter "
                        "position(s) are measured and compared but are not registered, "
                        "so a site could be added silently: " + repr(missing[:6]))
    if extra:
        findings.append("C2V6-REGISTER: " + str(len(extra)) + " registered position(s) "
                        "are not reached by the measurement, so the register overstates "
                        "what is observed: " + repr(extra[:6]))
    count_reason = jx_bind(spec.get("censusCounterPositionCount"), len(measured))
    if count_reason is not None:
        findings.append("C2V6-REGISTER: censusCounterPositionCount: " + count_reason)
    sites = census_site_positions(measurement)
    covered = []
    for key in jx_sorted(list(sites)):
        covered.extend(jx_get(sites, key))
    uncovered = jx_sorted(jx_difference(measured, covered))
    if uncovered or not jx_int_in_range(len(covered), 1, 10 ** 9):
        findings.append(
            "C2V6-REGISTER: the per-comparison-site partition covers " +
            str(len(jx_unique(covered))) + " of " + str(len(measured)) + " measured "
            "position(s); the figures the candidate publishes for how many wire "
            "integers each of the predecessor's three ungated comparisons reads would "
            "then be a claim over an unobserved region")
    rule = spec.get("rule")
    rule = rule if jx_type(rule) == "string" else ""
    if "type" not in rule or "before" not in rule:
        findings.append("C2V6-REGISTER: the register does not state plainly that the "
                        "JSON type is rejected before the content is compared")
    return findings


# =============================================================================
# Section 5.  L2b -- the document-wide integer type lock over the EFFECTIVE
# contract, and L2c -- the TOTAL binding of the CANDIDATE document's own
# integer leaves.
#
# L2c is the repair for IR-C2V5-03.  v5 locked the effective contract and left
# its own 66 integer leaves governed by nothing: 13 admitted a float to a full
# green run and 11 admitted arbitrary drift, boolean or string, including a
# block literally named `retainedFalseAcceptVectors.measuredThisRun`.
#
# The rule here is TOTAL over the class rather than enumerated over its known
# members: every integer leaf of the candidate is either bound to a value this
# run MEASURED, or bound to a byte of a hash-verified pinned input.  There is no
# third bucket.  A leaf nobody binds is itself a named finding, so narrowing the
# binding table fails closed instead of silently exempting a counter.
# =============================================================================

def _integer_leaf_steps(node, steps=()) -> list:
    """Every path holding a JSON integer, as a LIST of steps.

    Paths are lists, never tuples: a tuple is outside the JSON value universe,
    `jx_canon` refuses it by name, and `(1,) == (1.0,)` is True in the host
    language.  Using the primitive's own domain as the path representation
    removes a hazard rather than documenting one.
    """
    out = []
    if jx_type(node) == "object":
        for key in list(node):
            out.extend(_integer_leaf_steps(jx_at(node, key), list(steps) + [key]))
    elif jx_type(node) == "array":
        for index, value in enumerate(node):
            out.extend(_integer_leaf_steps(value, list(steps) + [index]))
    elif jx_int(node):
        out.append(list(steps))
    return out


def locked_integer_leaves(base, effective) -> list:
    """Every path holding a JSON integer in EITHER document.  Both directions,
    so neither a predecessor leaf the derivation retypes nor a leaf the
    derivation introduces can escape the lock."""
    locked = list(_integer_leaf_steps(base))
    locked.extend(_integer_leaf_steps(effective))
    return jx_sorted(jx_unique(locked))


def document_type_findings(effective, locked, prefix="C2V6-TYPE") -> list:
    findings = []
    for steps in locked:
        text = _steps_text(steps)
        try:
            value = _resolve_steps(effective, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            findings.append(prefix + ": " + text + " holds a JSON integer in the "
                            "verified predecessor but does not resolve in the effective "
                            "contract, so the type lock cannot be applied to it")
            continue
        if not jx_int(value):
            findings.append(
                prefix + ": " + text + " is published as " + repr(value) + ", whose "
                "JSON type is " + jx_type(value) + ", where a JSON integer is declared; "
                "freeze section 6 law 18 is not confined to the counters the "
                "adjudication named, and a float substituted here drives the pinned "
                "predecessor to a full green run")
    return findings


def document_type_probe(effective, locked, prefix="C2V6-TYPE") -> dict:
    """Behavioural, reads no source.  A float at EVERY locked leaf in turn."""
    cases = named = admitted = 0
    escapes = []
    for steps in locked:
        try:
            current = _resolve_steps(effective, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        if not jx_int(current):
            continue
        _assign_steps(effective, steps, float(current))
        try:
            cases += 1
            text = _steps_text(steps)
            findings = document_type_findings(effective, locked, prefix)
            if [item for item in findings
                    if item.startswith(prefix + ":") and text in item]:
                named += 1
            else:
                admitted += 1
                escapes.append(text + ": a float substitution was ADMITTED")
        finally:
            _assign_steps(effective, steps, current)
    return {"lockedLeaves": len(locked), "executedCases": cases,
            "namedTypeRejections": named, "admissions": admitted, "escapes": escapes}


def document_type_lock_findings(base, effective, authority) -> list:
    locked = locked_integer_leaves(base, effective)
    findings = []
    # BOTH DIRECTIONS, asserted by this layer rather than inferred from a drift
    # on a published count.  v5's version of this was guarded only by the number
    # 137, and republishing 137 as 136 alongside the break silenced it entirely.
    for label, document in (("verified predecessor", base),
                            ("effective contract", effective)):
        missing = jx_sorted(jx_difference(_integer_leaf_steps(document), locked))
        if missing:
            findings.append(
                "C2V6-DOCLOCK: " + str(len(missing)) + " integer leaf/leaves of the " +
                label + " are outside the lock, the first being " +
                _steps_text(missing[0]) + "; the lock must cover BOTH documents, "
                "because a leaf the derivation introduces and a leaf the derivation "
                "retypes are different escapes and neither direction is optional")
    findings.extend(document_type_findings(effective, locked))
    probe = document_type_probe(effective, locked)
    authority.document_lock = probe
    findings.extend("C2V6-DOCLOCK: " + item for item in probe["escapes"])
    if not jx_int_in_range(probe["executedCases"], 1, 10 ** 9):
        findings.append("C2V6-DOCLOCK: the document-wide type lock probed no position, "
                        "so it is a claim over an unobserved region")
    if jx_bind(probe["admissions"], 0) is not None:
        findings.append("C2V6-DOCLOCK: " + str(probe["admissions"]) + " float "
                        "substitution(s) at declared integer leaves were admitted")
    if jx_bind(probe["namedTypeRejections"], probe["executedCases"]) is not None:
        findings.append("C2V6-DOCLOCK: " + str(probe["namedTypeRejections"]) + " of " +
                        str(probe["executedCases"]) + " probes produced a named finding")
    return findings


# ---- L2c: the candidate document's own integer leaves -----------------------

# Prose copies of measured figures, bound to the live register key they claim to
# report.  This table may be WIDENED freely; narrowing it cannot hide anything,
# because a leaf that leaves the table becomes an unbound leaf and an unbound
# leaf is a named finding.  That asymmetry is the whole design.
CANDIDATE_COUNTER_ALIASES = (
    (["theDefect", "wholeDocumentSweep", "integerLeavesInjected"], "sweepIntegerLeavesInjected"),
    (["theDefect", "wholeDocumentSweep", "admittedByPredecessorToAFullGreenRun"], "sweepAdmittedToFullGreen"),
    (["theDefect", "wholeDocumentSweep", "rejectedByPredecessor"], "sweepRejectedByPredecessor"),
    (["theDefect", "wholeDocumentSweep", "ofWhichCensusCounters"], "sweepAdmittedCensusCounters"),
    (["theDefect", "wholeDocumentSweep", "ofWhichOutsideTheCensusBlock"], "sweepAdmittedOutsideCensus"),
    (["theDefect", "wireIntegerPositionsReadThroughThoseSites"], "registeredCensusPositions"),
    (["theDefect", "positionsBooleanExploitable"], "censusPositionsBooleanExploitable"),
    (["theDefect", "enumeratedComparisonSiteCount"], "adjudicatedComparisonSites"),
    (["retainedFalseAcceptVectors", "measuredThisRun", "predecessorAdmittedThePosition"], "differentialPredecessorAdmitted"),
    (["retainedFalseAcceptVectors", "measuredThisRun", "predecessorFullyGreenRuns"], "differentialPredecessorFullyGreen"),
    (["retainedFalseAcceptVectors", "measuredThisRun", "successorRejectedByName"], "differentialSuccessorRejectedByName"),
    (["theSuccessorDefect", "measuredThisRun", "vectors"], "successorDifferentialVectors"),
    (["theSuccessorDefect", "measuredThisRun", "v5AdmittedToAFullGreenRun"],
     "successorV5AdmittedFullyGreen"),
    (["theSuccessorDefect", "measuredThisRun", "v6RejectedByName"],
     "successorV6RejectedByName"),
)

# Per-comparison-site read counts, bound to the live census-site measurement.
CANDIDATE_SITE_KEYS = (CENSUS_SITE_LINE_2487, CENSUS_SITE_LINE_2493,
                       CENSUS_SITE_LINE_2517)


def candidate_bindings(c, live, authority, base, measurement):
    """Return (bindings, findings).

    `bindings` maps a steps tuple of the CANDIDATE to
    (kind, expected value, what the expectation came from).  Every integer leaf
    of the candidate must appear.  Nothing is exempt, including this checker's
    own counters and including the block that reports how many false accepts
    were measured.
    """
    bindings, findings = [], []

    def bind(steps, kind, value, source):
        bindings.append({"steps": list(steps), "kind": kind, "expected": value,
                         "source": source})

    bind(["version"], "identity", 6, "this checker's declared successor identity")
    bind(["supersedes"], "identity", 5,
         "this checker's declared successor identity")
    for path, value in DECLARED_PROJECTION_FIELDS:
        if jx_int(value):
            bind(["v4InheritanceProjection", "fields", path], "projection", value,
                 "the identity byte the pinned inherited oracle is bound to")

    # The derivation.  `from` leaves are bound to the VERIFIED PREDECESSOR;
    # `value` leaves are bound to whatever layer measures the effective
    # contract at the path the operation writes to.
    derived = c.get("derivedFrom")
    derived = derived if jx_type(derived) == "object" else {}
    operations = derived.get("operations")
    operations = operations if jx_type(operations) == "array" else []
    positions = measured_positions(measurement)
    for index, op in enumerate(operations):
        if jx_type(op) != "object" or jx_type(op.get("path")) != "string":
            continue
        target = _path_steps(op["path"])
        for sub in _integer_leaf_steps(op.get("from")):
            try:
                expected = _resolve_steps(base, list(target) + list(sub))
            except MALFORMED_SHAPE_EXCEPTIONS:
                findings.append(
                    "C2V6-UNBOUND: derivedFrom/operations/" + str(index) + "/from/" +
                    _steps_text(sub) + " does not resolve in the verified predecessor, "
                    "so the derivation restates a byte that does not exist")
                continue
            bind(["derivedFrom", "operations", index, "from"] + list(sub),
                 "predecessor", expected,
                 "the byte the verified predecessor actually holds at " +
                 _steps_text(list(target) + list(sub)))
        for sub in _integer_leaf_steps(op.get("value")):
            steps = ["derivedFrom", "operations", index, "value"] + list(sub)
            expected, source = _effective_expected(
                list(target) + list(sub), live, positions)
            if expected is None:
                findings.append(
                    "C2V6-UNBOUND: the derivation writes a JSON integer into the "
                    "effective contract at " + _steps_text(list(target) + list(sub)) +
                    " which no layer of this checker measures; a value a layer does "
                    "not measure is a published claim, not evidence")
                continue
            bind(steps, "derivation", expected, source)

    # The adjudicated comparison sites, read from the PINNED adjudication.
    adjudicated = jx_sorted(adjudicated_census_lines(authority))
    sites = c.get("theDefect")
    sites = sites.get("repairedComparisonSites") if jx_type(sites) == "object" else None
    sites = sites if jx_type(sites) == "array" else []
    site_positions = census_site_positions(measurement)
    for index, site in enumerate(sites):
        if index < len(adjudicated):
            bind(["theDefect", "repairedComparisonSites", index, "line"],
                 "adjudication", adjudicated[index],
                 "the line number the pinned adjudication names")
        if jx_type(site) == "object" and index < len(CANDIDATE_SITE_KEYS):
            key = CANDIDATE_SITE_KEYS[index]
            bind(["theDefect", "repairedComparisonSites", index,
                  "wireIntegerPositionsRead"],
                 "measured", len(jx_get(site_positions, key, [])),
                 "the number of published counter positions this run measured at the " +
                 key + " comparison site")

    for steps, key in CANDIDATE_COUNTER_ALIASES:
        if jx_has(live, key):
            bind(steps, "measured", jx_get(live, key),
                 "the value this run measured for " + key)

    for key in jx_sorted(list(live)):
        bind(["v6MeasuredCounters", key], "measured", jx_get(live, key),
             "the value this run measured for " + key)
    return bindings, findings


def _effective_expected(steps, live, positions):
    """What a layer of this checker measures at an EFFECTIVE-contract path."""
    text = _steps_text(steps)
    if jx_equal(list(steps[:1]), ["version"]):
        return 6, "this checker's declared successor identity"
    if jx_equal(list(steps[:1]), ["supersedes"]):
        return 5, "this checker's declared successor identity"
    if jx_equal(list(steps[:1]), ["hostileScalarLeafTotality"]):
        position = _effective_census_position(steps)
        if position is not None and jx_has(positions, position):
            return jx_get(positions, position), \
                "the value this run measured at census position " + position
    if text.endswith("censusCounterPositionCount"):
        return jx_get(live, "registeredCensusPositions"), \
            "the number of census positions this run measured"
    return None, "unmeasured"


def _effective_census_position(steps):
    parts = list(steps)
    if len(parts) == 3 and jx_equal(parts[1], "contractRoot"):
        return "contractRoot." + str(parts[2])
    if len(parts) == 4 and jx_equal(parts[1], "surfaces"):
        return None
    return None


def candidate_lock_findings(c, live, authority, base, measurement) -> list:
    """L2c.  Total: every integer leaf of the candidate is bound, and every
    binding is checked through `jx_bind`.  Then every one of them is float-,
    boolean-, string- and drift-probed live, and each probe must be named."""
    findings = []
    bindings, findings_from_bindings = candidate_bindings(
        c, live, authority, base, measurement)
    findings.extend(findings_from_bindings)
    leaves = _integer_leaf_steps(c)
    bound_paths = [record["steps"] for record in bindings]
    unbound = jx_sorted(jx_difference(leaves, bound_paths))
    for steps in unbound:
        findings.append(
            "C2V6-UNBOUND: the candidate publishes a JSON integer at " +
            _steps_text(steps) + " that no layer of this run binds to a measurement or "
            "to a verified pinned byte; v5 shipped thirteen of these and the reviewer "
            "floated every one of them to a full green run")
    duplicates = [record["steps"] for record in bindings
                  if jx_count(bound_paths, record["steps"]) > 1]
    for steps in jx_sorted(jx_unique(duplicates)):
        findings.append("C2V6-UNBOUND: " + _steps_text(steps) + " is bound twice, so "
                        "one of the two bindings is not the one being enforced")
    for steps in jx_sorted(jx_difference(bound_paths, leaves)):
        findings.append(
            "C2V6-UNBOUND: this run binds " + _steps_text(steps) + " but the candidate "
            "publishes no JSON integer there; a binding over an absent leaf is a "
            "coverage claim over an unobserved region")
    for record in jx_sorted_by(bindings, "steps"):
        steps, kind = record["steps"], record["kind"]
        expected, source = record["expected"], record["source"]
        try:
            published = _resolve_steps(c, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        reason = jx_bind(published, expected)
        if reason is None:
            continue
        prefix = "C2V6-TYPE" if not jx_int(published) else "C2V6-CANDIDATE"
        findings.append(prefix + ": " + _steps_text(steps) + " (" + kind + "): " +
                        reason + "; the expectation is " + source)
    probe = candidate_type_probe(c, bindings)
    authority.candidate_lock = probe
    findings.extend("C2V6-CANDLOCK: " + item for item in probe["escapes"])
    if not jx_int_in_range(probe["executedCases"], 1, 10 ** 9):
        findings.append("C2V6-CANDLOCK: the candidate lock probed no position, so it is "
                        "a claim over an unobserved region")
    if jx_bind(probe["admissions"], 0) is not None:
        findings.append("C2V6-CANDLOCK: " + str(probe["admissions"]) + " hostile "
                        "spelling(s) at the candidate's own integer leaves were admitted")
    return findings


CANDIDATE_HOSTILE_SPELLINGS = ("float-equal", "boolean-true", "boolean-false",
                               "numeric-string", "null", "array", "object",
                               "drift-plus-one", "drift-to-zero")


def _hostile_spelling(label, value):
    if jx_equal(label, "float-equal"):
        return float(value)
    if jx_equal(label, "boolean-true"):
        return True
    if jx_equal(label, "boolean-false"):
        return False
    if jx_equal(label, "numeric-string"):
        return str(value)
    if jx_equal(label, "null"):
        return None
    if jx_equal(label, "array"):
        return []
    if jx_equal(label, "object"):
        return {}
    if jx_equal(label, "drift-plus-one"):
        return value + 1
    return 0


def candidate_type_probe(c, bindings) -> dict:
    """Behavioural, reads no source.  Every hostile spelling AND arbitrary value
    drift at EVERY bound leaf of the candidate, driven through the live
    binding.  This is the layer v5 did not have."""
    cases = named = admitted = controls = 0
    escapes = []
    for record in jx_sorted_by(bindings, "steps"):
        steps, expected = record["steps"], record["expected"]
        try:
            current = _resolve_steps(c, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        if not jx_int(current):
            continue
        for label in CANDIDATE_HOSTILE_SPELLINGS:
            # Every (leaf, spelling) pair is executed, including the ones that
            # reproduce the bound value: those are CONTROLS and must be
            # accepted.  Counting them keeps executedCases a function of the
            # bound leaf set alone, so a counter this block publishes can never
            # change the number of cases that measure it.
            cases += 1
            value = _hostile_spelling(label, current)
            bound = jx_bind(value, expected) is None
            if jx_equal(value, expected):
                controls += 1
                if not bound:
                    escapes.append(_steps_text(steps) + "/" + label + ": the control "
                                   "spelling reproducing the measured value was "
                                   "REFUSED, so this probe is not an oracle")
                continue
            if bound:
                admitted += 1
                escapes.append(_steps_text(steps) + "/" + label + ": " + repr(value) +
                               " was ADMITTED where the JSON integer " + repr(expected) +
                               " is measured")
            else:
                named += 1
    return {"boundLeaves": len(bindings), "executedCases": cases,
            "namedRejections": named, "controls": controls,
            "admissions": admitted, "escapes": escapes}


def adjudicated_census_lines(authority) -> list:
    """The line numbers the adjudication names, read from the PINNED document.

    v5 read these into a set and then compared that set against a set built
    from the WIRE with `<=`.  `{2487} <= {2487.0}` is True.  Here the value is
    a list of JSON integers, every downstream comparison goes through `jx_`,
    and the parse itself is type-asserted.
    """
    verdict = authority.json(ADJUDICATION)
    verdict = verdict if jx_type(verdict) == "object" else {}
    sites = verdict.get("reachabilityVerdict")
    sites = sites.get("theUnguardedSites") if jx_type(sites) == "object" else None
    sites = sites if jx_type(sites) == "array" else []
    lines = []
    for site in sites:
        location = site.get("location") if jx_type(site) == "object" else None
        match = re.search(r"line (\d+)", location if jx_type(location) == "string" else "")
        if match is not None:
            lines.append(int(match.group(1)))
    return jx_sorted(jx_unique(lines))


# =============================================================================
# Section 6.  L4 -- the inverted wire-comparison scan.
#
# v4 asked "is the other operand a numeric LITERAL", so a computed integer was
# invisible.  v5 inverted that and asked "is this wire operand gated", which
# was right, and then MISSED ITS OWN LINE 1815 for two separate reasons:
#
#   1. TAINT.  `lines = {item.get("line") for item in sites}` binds a name to a
#      comprehension RESULT.  v5 tainted comprehension TARGETS but never the
#      name bound to the result, so `lines` was laundered clean.  Fixed here:
#      a comprehension, generator, map/filter or container-constructor RESULT
#      is wire when anything it is built from is wire.
#   2. OPERATOR SPACE.  The site was `adjudicated <= lines`, a SET SUBSET test,
#      and v5's `_NON_NUMERIC_CALLS` additionally excused `set(...)` and
#      `sorted(...)` results as "container comparisons, not integer
#      comparisons".  A container comparison is exactly as dangerous:
#      `{2487} <= {2487.0}` is True and `[1] == [1.0]` is True.  That excusal
#      is removed.  Membership is no longer narrowed to literal containers,
#      `operator.*` calls are comparison sites, hash-keyed method calls and
#      subscripts are comparison sites, and set/dict construction over wire
#      values is a comparison site because it silently dedups.
#
# The scan is not the defence.  L5 reads no source and L6 is anchored to
# external pinned bytes; both stand behind it precisely because a syntactic
# instrument is not a proof.
# =============================================================================

_ORDER_OPS = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)
_MEMBER_OPS = (ast.In, ast.NotIn)
_SET_ALGEBRA_OPS = (ast.BitOr, ast.BitAnd, ast.BitXor, ast.Sub)
_LITERAL_CONTAINERS = (ast.Tuple, ast.List, ast.Set)
_SET_SHAPED = (ast.Set, ast.SetComp)
_SET_CALLS = frozenset({"set", "frozenset", "jx_keyset"})
# Calls whose RESULT carries whatever their arguments carried.  This is the
# closure v5 did not have.
_PROPAGATING_CALLS = frozenset({
    "sorted", "set", "frozenset", "list", "tuple", "dict", "reversed", "enumerate",
    "zip", "map", "filter", "next", "iter", "sum", "min", "max", "deepcopy", "copy",
    "loads", "get", "pop", "setdefault", "values", "items", "keys", "getattr",
})
# Method calls with hash or equality semantics on their receiver.
_HASH_METHODS = frozenset({
    "get", "pop", "setdefault", "fromkeys", "count", "index", "remove", "discard",
    "issubset", "issuperset", "isdisjoint", "union", "intersection", "difference",
    "symmetric_difference", "update", "add", "__contains__",
})
# Bare comparison functions.  `operator.ne(a, b)` is an ast.Call and is never an
# ast.Compare, so a scan that walks only ast.Compare cannot see it at all.
_OPERATOR_FUNCS = frozenset({"eq", "ne", "lt", "le", "gt", "ge", "contains",
                            "countOf", "indexOf", "is_", "is_not"})
# Builtins that build a HASHED container or an ORDERED one out of their input,
# and therefore collapse or interleave values the host language calls equal.
_HASHING_BUILTINS = frozenset({"set", "frozenset", "dict", "sorted", "min", "max",
                               "sum", "Counter", "OrderedDict", "defaultdict"})
# Returns a str or a type; cannot equal a number.  `sorted`, `set`, `list`,
# `tuple`, `dict` and `frozenset` are deliberately NOT here: a container is
# compared element-by-element and `[1] == [1.0]` is True.
_NON_NUMERIC_BUILTINS = frozenset({"str", "repr", "ascii", "chr", "hex", "oct",
                                   "bin", "type", "unparse"})
_WIRE_ACCESSORS = frozenset({"get", "pop", "setdefault"})
_WIRE_CALLS = frozenset({"next", "getattr", "iter"})
_MAX_SCAN_DEPTH = 6


def _function_universe(tree) -> list:
    """Every function-like node at any depth: defs, methods, nested defs, lambdas.

    The declared type gates are excluded.  Scanning the body of `jx_int` for the
    absence of a type gate is circular: it IS the gate.  That exclusion is a
    DEBT, not free coverage, and L7 discharges it in full by breaking every one
    of the gates in turn and requiring each break to be caught by the layer it
    breaks even after every published counter has been republished.
    """
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            and getattr(node, "name", "<lambda>") not in GUARD_HELPERS]


def _bound_names(target) -> set:
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, ast.Starred):
        return _bound_names(target.value)
    if isinstance(target, (ast.Tuple, ast.List)):
        out = set()
        for element in target.elts:
            out |= _bound_names(element)
        return out
    return set()


def _is_wire(node, tainted, literals=frozenset()):
    """A value that came off the wire, or is built from one.

    A subscript into a MODULE-LEVEL LITERAL is this file's own constant table,
    not wire; calling it wire would flood the scan with noise that would then
    have to be excused, which is how a scan stops being read.  Everything else
    that touches a wire value, INCLUDING A COMPREHENSION RESULT, is wire.
    """
    if node is None:
        return False
    if isinstance(node, ast.Subscript):
        if isinstance(node.value, ast.Name) and node.value.id in literals:
            return False
        return True
    if isinstance(node, ast.Starred):
        return _is_wire(node.value, tainted, literals)
    if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
        parts = [node.elt] + [gen.iter for gen in node.generators]
        return any(_is_wire(part, tainted, literals) for part in parts)
    if isinstance(node, ast.DictComp):
        parts = [node.key, node.value] + [gen.iter for gen in node.generators]
        return any(_is_wire(part, tainted, literals) for part in parts)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return any(_is_wire(item, tainted, literals) for item in node.elts)
    if isinstance(node, ast.Dict):
        parts = [item for item in list(node.keys) + list(node.values) if item is not None]
        return any(_is_wire(part, tainted, literals) for part in parts)
    if isinstance(node, ast.IfExp):
        return _is_wire(node.body, tainted, literals) or \
            _is_wire(node.orelse, tainted, literals)
    if isinstance(node, ast.BoolOp):
        return any(_is_wire(item, tainted, literals) for item in node.values)
    if isinstance(node, ast.BinOp):
        return _is_wire(node.left, tainted, literals) or \
            _is_wire(node.right, tainted, literals)
    if isinstance(node, ast.Call):
        name = None
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
            if name in _WIRE_ACCESSORS:
                return True
            if _is_wire(node.func.value, tainted, literals) and name in _PROPAGATING_CALLS:
                return True
        elif isinstance(node.func, ast.Name):
            name = node.func.id
            if name in _WIRE_CALLS:
                return True
        if name in _PROPAGATING_CALLS:
            arguments = list(node.args) + [kw.value for kw in node.keywords]
            return any(_is_wire(item, tainted, literals) for item in arguments)
        return False
    if isinstance(node, ast.Attribute):
        return _is_wire(node.value, tainted, literals)
    if isinstance(node, ast.NamedExpr):
        return _is_wire(node.value, tainted, literals)
    return isinstance(node, ast.Name) and node.id in tainted


def _taint_fixpoint(function, literals=frozenset()) -> set:
    """Args, kwonly, vararg, kwarg, every assignment form, walrus, unpack,
    for-targets, comprehension targets, with-targets AND -- the shape that
    laundered check-c2-v5.py line 1815 -- the name bound to a comprehension,
    generator or container-constructor RESULT.  To a fixpoint."""
    args = function.args
    tainted = set()
    for group in (args.posonlyargs, args.args, args.kwonlyargs):
        tainted |= {item.arg for item in group}
    if args.vararg is not None:
        tainted.add(args.vararg.arg)
    if args.kwarg is not None:
        tainted.add(args.kwarg.arg)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(function):
            fresh = set()
            if isinstance(node, ast.Assign) and _is_wire(node.value, tainted, literals):
                for target in node.targets:
                    fresh |= _bound_names(target)
            elif isinstance(node, (ast.AnnAssign, ast.AugAssign)) and \
                    node.value is not None and _is_wire(node.value, tainted, literals):
                fresh |= _bound_names(node.target)
            elif isinstance(node, ast.NamedExpr) and \
                    _is_wire(node.value, tainted, literals):
                fresh |= _bound_names(node.target)
            elif isinstance(node, (ast.For, ast.AsyncFor)) and \
                    _is_wire(node.iter, tainted, literals):
                fresh |= _bound_names(node.target)
            elif isinstance(node, ast.comprehension) and \
                    _is_wire(node.iter, tainted, literals):
                fresh |= _bound_names(node.target)
            elif isinstance(node, ast.withitem) and \
                    node.optional_vars is not None and \
                    _is_wire(node.context_expr, tainted, literals):
                fresh |= _bound_names(node.optional_vars)
            if fresh - tainted:
                tainted |= fresh
                changed = True
    return tainted


def _module_constants(tree) -> dict:
    """Module-level Name -> value node, so a named constant is not a hiding place."""
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.value is not None:
            constants[node.target.id] = node.value
    return constants


def str_returning_functions(tree) -> list:
    """Module-level functions annotated `-> str`, read STRUCTURALLY from the tree.

    A call to one of these is provably non-numeric.  That is a real proof only
    if the annotation is honest, so L5 CALLS every one of them over the JSON
    corpus and requires every result to be a `str`.  Structure and behaviour,
    not one or the other.
    """
    out = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and isinstance(node.returns, ast.Name) \
                and node.returns.id == "str":
            out.append(node.name)
    return jx_sorted(out)


# ---- the named non-numeric proofs -------------------------------------------
# The hazard class is NEVER narrowed: every operator-space row stays in scope
# and every wire operand stays in scope.  What is added here is a PROOF that a
# particular operand cannot carry a JSON number.  Each proof is named, each is
# counted, the counts are published and bound, and L7 breaks each one.  An
# excusal budget that is visible cannot become the silent narrowing that
# produced IR-C2V4-01.
#
#   AST-STR-FIELD    `X.id`, `X.attr`, `X.arg`, `X.name`, `X.module` are `str`
#                    or None on every ast node that has them.  PROBED live over
#                    this file's own tree by L5, not assumed.
#   STR-ANNOTATION   a parameter annotated `str`, or a call to a module-level
#                    function annotated `-> str`.  PROBED for the `-> str` half.
#   INTERNAL-INDEX   a name bound by `enumerate`, `range` or `len`.  A Python
#                    loop index is an `int` produced by the interpreter; no wire
#                    value can make it a float.
#   NON-NUMERIC-FLOW the transitive closure of the three above through
#                    assignment, walrus and for-targets.
_AST_STR_FIELDS = frozenset({"id", "attr", "arg", "name", "module"})
_INDEX_PRODUCERS = frozenset({"enumerate", "range", "len"})
# `ast.<fn>` returns AST nodes or source text, never a number.  `literal_eval`
# is deliberately absent: it returns whatever the literal was, including a float.
_AST_MODULE_NON_NUMERIC = frozenset({"walk", "parse", "iter_child_nodes", "unparse",
                                     "fix_missing_locations", "get_source_segment",
                                     "iter_fields"})
_CONTAINER_CONSTRUCTORS = frozenset({"set", "frozenset", "list", "tuple", "sorted",
                                     "reversed", "dict"})
# Parameter annotations that cannot carry a JSON number.  Annotations are not
# enforced at run time, so this is a declared, counted, L7-breakable proof and
# never a substitute for a gate on a value that came off the wire.
_NON_NUMERIC_ANNOTATIONS = frozenset({"str", "bytes"})
_INDEX_ANNOTATIONS = frozenset({"int"})
NON_NUMERIC_PROOFS = ("LITERAL", "AST-STR-FIELD", "AST-MODULE-CALL",
                      "STR-RETURNING-CALL", "TYPE-ANNOTATION", "INTERNAL-INDEX",
                      "CONTAINER-OF-NON-NUMERIC", "NON-NUMERIC-FLOW")


def _str_annotated_parameters(function) -> set:
    """Proofs TYPE-ANNOTATION and INTERNAL-INDEX, seeded from the signature."""
    args = function.args
    out = set()
    for group in (args.posonlyargs, args.args, args.kwonlyargs):
        for item in group:
            annotation = item.annotation
            if isinstance(annotation, ast.Name) and (
                    annotation.id in _NON_NUMERIC_ANNOTATIONS or
                    annotation.id in _INDEX_ANNOTATIONS):
                out.add(item.arg)
            elif isinstance(annotation, ast.Attribute) and \
                    isinstance(annotation.value, ast.Name) and \
                    annotation.value.id == "ast":
                out.add(item.arg)
    return out


def _non_numeric_names(function, constants, str_proofs, seed) -> set:
    """Fixpoint dual to the taint fixpoint: names PROVABLY not numeric.

    `name = node.func.id` makes `name` a str.  Without this closure the proof
    would stop at the attribute access and every downstream use would have to
    be excused by hand, which is how excusal tables rot.
    """
    proven = set()
    for name in seed:
        if jx_type(name) != "string":
            continue
        proven.add(name)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(function):
            fresh = set()
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)) and \
                    getattr(node, "value", None) is not None and \
                    _provably_non_numeric(node.value, constants, str_proofs, 0, proven):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    fresh |= _bound_names(target)
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
                iterator = node.iter
                if isinstance(iterator, ast.Call) and \
                        isinstance(iterator.func, ast.Name) and \
                        iterator.func.id in _INDEX_PRODUCERS:
                    names = sorted(_bound_names(node.target))
                    if iterator.func.id == "range":
                        fresh |= {item for item in names if jx_type(item) == "string"}
                    elif names:
                        bound = names[0] if isinstance(node.target, ast.Name) \
                            else _enumerate_index_name(node.target)
                        if jx_type(bound) == "string":
                            fresh.add(bound)
                elif _provably_non_numeric(iterator, constants, str_proofs, 0, proven):
                    fresh |= _bound_names(node.target)
            fresh.discard(None)
            if fresh - proven:
                proven |= fresh
                changed = True
    return proven


def _enumerate_index_name(target):
    """`for index, value in enumerate(x)` -- only `index` is the internal int."""
    if isinstance(target, (ast.Tuple, ast.List)) and target.elts and \
            isinstance(target.elts[0], ast.Name):
        return target.elts[0].id
    return None


def _provably_non_numeric(node, constants, str_proofs, depth=0, proven=frozenset()):
    """Conservative: only SHAPES that cannot possibly equal a number are excused.

    A bool constant is NUMERIC here.  `x != True` is exactly the LB-C2-01 shape
    and must never be excused.  A container is NOT excused: `[1] == [1.0]` is
    True, so a container is excused only when every element is itself excused.
    """
    if not jx_int_in_range(depth, 0, _MAX_SCAN_DEPTH) or node is None:
        return False
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or isinstance(node.value, (int, float, complex)):
            return False
        return node.value is None or isinstance(node.value, (str, bytes)) or \
            node.value is Ellipsis
    if isinstance(node, (ast.JoinedStr, ast.FormattedValue)):
        return True
    if isinstance(node, _LITERAL_CONTAINERS):
        return all(_provably_non_numeric(item, constants, str_proofs, depth + 1)
                   for item in node.elts)
    if isinstance(node, ast.Dict):
        parts = [item for item in list(node.keys) + list(node.values) if item is not None]
        return bool(parts) and all(
            _provably_non_numeric(item, constants, str_proofs, depth + 1)
            for item in parts)
    if isinstance(node, ast.Call):
        arguments = list(node.args) + [kw.value for kw in node.keywords]
        if isinstance(node.func, ast.Name):
            if node.func.id in _NON_NUMERIC_BUILTINS or node.func.id in str_proofs:
                return True                             # proof STR-RETURNING-CALL
            if node.func.id in _CONTAINER_CONSTRUCTORS:
                # proof CONTAINER-OF-NON-NUMERIC: `set(ast.walk(x))` can hold
                # only what `ast.walk(x)` yields.  A container is excused when
                # everything it is built from is excused, and never otherwise.
                return bool(arguments) and all(
                    _provably_non_numeric(item, constants, str_proofs, depth + 1, proven)
                    for item in arguments)
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in _NON_NUMERIC_BUILTINS:
                return True
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "ast" \
                    and node.func.attr in _AST_MODULE_NON_NUMERIC:
                return True                             # proof AST-MODULE-CALL
        return False
    if isinstance(node, (ast.GeneratorExp, ast.ListComp, ast.SetComp)):
        return _provably_non_numeric(node.elt, constants, str_proofs, depth + 1, proven)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        return _provably_non_numeric(node.left, constants, str_proofs, depth + 1, proven)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and all(
            _provably_non_numeric(item, constants, str_proofs, depth + 1, proven)
            for item in (node.left, node.right)):
        return True                                     # concatenation of two strings
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
        # proof INTERNAL-INDEX: an interpreter-produced index offset by an
        # integer literal is still an interpreter-produced index.
        parts = (node.left, node.right)
        return all(
            (isinstance(item, ast.Constant) and type(item.value) is int) or
            (isinstance(item, ast.Name) and item.id in proven)
            for item in parts) and any(
            isinstance(item, ast.Name) and item.id in proven for item in parts)
    if isinstance(node, ast.Attribute) and node.attr in _AST_STR_FIELDS:
        return True                                     # proof AST-STR-FIELD
    if isinstance(node, ast.Name) and node.id in proven:
        return True                                     # proof NON-NUMERIC-FLOW
    if isinstance(node, ast.Name) and node.id in constants:
        return _provably_non_numeric(constants[node.id], constants, str_proofs,
                                     depth + 1, proven)
    return False


def _gate_calls(function) -> dict:
    """Type-gate calls keyed by the unparsed text of each of their arguments."""
    gates: dict[str, list] = {}
    for node in ast.walk(function):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id not in TYPE_GATES or not node.args:
            continue
        if node.func.id == "isinstance":
            if len(node.args) < 2 or not _isinstance_is_a_gate(node.args[1]):
                continue
        for argument in node.args:
            gates.setdefault(ast.unparse(argument), []).append(node)
    return gates


def _isinstance_is_a_gate(classinfo) -> bool:
    """isinstance(x, int) is NOT a law-18 gate: True is an int.

    `isinstance(x, ast.AST)` IS one: no syntax-tree node is a number, and the
    host language's numeric tower cannot reach it.
    """
    nodes = classinfo.elts if isinstance(classinfo, _LITERAL_CONTAINERS) else [classinfo]
    named = set()
    for node in nodes:
        if isinstance(node, ast.Name):
            named.add(node.id)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id == "ast":
            named.add("ast." + node.attr)
        else:
            return False
    return bool(named) and named <= (NON_NUMERIC_CLASSES | _AST_CLASS_GATES)


def _parent_map(function) -> dict:
    parents = {}
    for node in ast.walk(function):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    return parents


def _position(node):
    return (getattr(node, "lineno", 0), getattr(node, "col_offset", 0))


def _enclosing_statements(node: ast.AST, parents) -> list:
    chain = []
    current = node
    while isinstance(current, ast.AST):
        if isinstance(current, ast.stmt):
            chain.append(current)
        current = parents.get(current)
    return chain


def _gate_dominates(site, wire_node, gates, parents) -> bool:
    """Textual excusal.  Declared as a blind spot -- not a dominance proof.

    MEASURED, and published as `scanSelfGateExcusedSites`.  v5's residual said
    this was the live hazard; the reviewer measured that it excused exactly
    nothing and that the real hazard was the taint model.  v6 publishes the
    number so the residual is grounded in a measurement rather than in a story.
    """
    candidates = gates.get(ast.unparse(wire_node), [])
    if not candidates:
        return False
    here = _position(site)
    chain = _enclosing_statements(site, parents)
    if not chain:
        return False
    inside = set(ast.walk(chain[0]))
    for gate in candidates:
        if gate in inside and _position(gate) <= here:
            return True
    for statement in chain:
        if not isinstance(statement, ast.AST):
            continue
        parent = parents.get(statement)
        while isinstance(parent, ast.AST) and not isinstance(parent, (ast.If, ast.While)):
            parent = parents.get(parent)
        if parent is None:
            continue
        test_nodes = set(ast.walk(parent.test))
        if any(gate in test_nodes for gate in candidates):
            return True
    for statement in chain:
        if not isinstance(statement, ast.AST):
            continue
        parent = parents.get(statement)
        block = None
        if parent is not None:
            for field in ("body", "orelse", "finalbody"):
                items = getattr(parent, field, None)
                if isinstance(items, list) and statement in items:
                    block = items
                    break
        if block is None:
            continue
        for sibling in block[:block.index(statement)]:
            if not isinstance(sibling, ast.If):
                continue
            if not all(isinstance(item, (ast.Return, ast.Raise, ast.Continue))
                       for item in sibling.body):
                continue
            if any(gate in set(ast.walk(sibling.test)) for gate in candidates):
                return True
    return False


def _hazard_pairs(node, constants, str_proofs):
    """(kind, wire-candidate, far operand) for every int/float-equivalence site.

    This is the enumerated operator space of the module docstring, as code.
    """
    out = []
    if isinstance(node, ast.Compare):
        operands = [node.left] + list(node.comparators)
        for index, operator_node in enumerate(node.ops):
            left, right = operands[index], operands[index + 1]
            if isinstance(operator_node, _ORDER_OPS):
                kind = "set-order" if (isinstance(left, _SET_SHAPED) or
                                       isinstance(right, _SET_SHAPED)) else "compare"
                out.append((kind, left, right))
                out.append((kind, right, left))
            elif isinstance(operator_node, _MEMBER_OPS):
                out.append(("membership", left, right))
    elif isinstance(node, ast.BinOp) and isinstance(node.op, _SET_ALGEBRA_OPS):
        set_shaped = _is_set_shaped(node.left) or _is_set_shaped(node.right)
        if set_shaped:
            out.append(("set-algebra", node.left, node.right))
            out.append(("set-algebra", node.right, node.left))
    elif isinstance(node, ast.Subscript):
        slice_node = node.slice
        if not isinstance(slice_node, ast.Slice):
            out.append(("key-lookup", slice_node, node.value))
    elif isinstance(node, (ast.SetComp, ast.DictComp)):
        key = node.elt if isinstance(node, ast.SetComp) else node.key
        out.append(("hash-construct", key, key))
    elif isinstance(node, ast.Set):
        for item in node.elts:
            out.append(("hash-construct", item, item))
    elif isinstance(node, ast.Dict):
        for item in node.keys:
            if item is not None:
                out.append(("hash-construct", item, item))
    elif isinstance(node, ast.Call):
        name = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        arguments = list(node.args) + [kw.value for kw in node.keywords]
        if name in _OPERATOR_FUNCS and len(arguments) >= 2:
            out.append(("operator-call", arguments[0], arguments[1]))
            out.append(("operator-call", arguments[1], arguments[0]))
        elif name in _HASHING_BUILTINS and isinstance(node.func, ast.Name):
            for item in arguments:
                out.append(("hash-builtin", item, item))
        elif name in _HASH_METHODS and isinstance(node.func, ast.Attribute):
            receiver = node.func.value
            for item in arguments:
                out.append(("hash-method", item, receiver))
    return out


def _is_set_shaped(node) -> bool:
    if isinstance(node, _SET_SHAPED):
        return True
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
        node.func.id in _SET_CALLS


def wire_comparison_scan(tree, label="subject") -> dict:
    """L4.  A wire operand in ANY operation with int/float equivalence semantics
    is a finding unless it is routed through a declared type gate."""
    constants = _module_constants(tree)
    literals = set()
    for name in list(constants):
        if jx_type(name) != "string":
            continue
        if isinstance(jx_at(constants, name),
                      (ast.Dict, ast.Tuple, ast.List, ast.Set, ast.Constant)):
            literals.add(name)
    literals = frozenset(literals)
    str_proofs = frozenset(str_returning_functions(tree))
    universe = _function_universe(tree)
    sites, gate_sites, excused, seen = [], 0, 0, set()
    kinds = {}
    for function in universe:
        tainted = _taint_fixpoint(function, literals)
        proven = _non_numeric_names(function, constants, str_proofs,
                                    _str_annotated_parameters(function))
        gates = _gate_calls(function)
        parents = _parent_map(function)
        name = getattr(function, "name", "<lambda>")
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                    node.func.id in GUARD_HELPERS:
                gate_sites += 1
            for kind, wire_node, other in _hazard_pairs(node, constants, str_proofs):
                if not _is_wire(wire_node, tainted, literals):
                    continue
                if _provably_non_numeric(wire_node, constants, str_proofs, 0, proven):
                    continue
                if kind in ("compare", "set-order", "membership", "operator-call",
                            "set-algebra") and \
                        _provably_non_numeric(other, constants, str_proofs, 0, proven):
                    continue
                # A sequence subscript and a sequence search are POSITIONAL, not
                # hash-keyed: `"abc"[1.0]` and `[10, 20][1.0]` raise rather than
                # collide.  The excusal is on the CONTAINER, and only when the
                # container is provably not a mapping of numbers.
                if kind in ("key-lookup", "hash-method") and \
                        _provably_non_numeric(other, constants, str_proofs, 0, proven):
                    continue
                if _gate_dominates(node, wire_node, gates, parents):
                    excused += 1
                    continue
                key = (_position(node), ast.unparse(node), ast.unparse(wire_node), kind)
                if key in seen:
                    continue
                seen.add(key)
                kinds[kind] = kinds.get(kind, 0) + 1
                sites.append({
                    "function": name,
                    "line": getattr(node, "lineno", 0),
                    "kind": kind,
                    "source": ast.unparse(node)[:200],
                    "wireOperand": ast.unparse(wire_node)[:120],
                    "farOperand": ast.unparse(other)[:120],
                    "farOperandIsComputed": not isinstance(other, ast.Constant),
                })
    return {
        "label": label,
        "functionLikeNodes": len(universe),
        "gateCallSites": gate_sites,
        "gateExcusedSites": excused,
        "strProofFunctions": len(str_proofs),
        "ungatedWireComparisons": len(sites),
        "ungatedComputedOperandComparisons":
            sum(1 for site in sites if site["farOperandIsComputed"]),
        "kinds": kinds,
        "sites": sorted(sites, key=lambda site: (site["line"], site["source"])),
        "indirectionPrimitives": _indirection_primitives(tree),
    }


def _indirection_primitives(tree) -> dict:
    """What L4 structurally cannot see.  Measured, published, must be zero here."""
    evals = execs = getattr_dispatch = operator_imports = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                evals += 1
            elif node.func.id == "exec":
                execs += 1
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Call) and \
                isinstance(node.func.func, ast.Name) and node.func.func.id == "getattr":
            getattr_dispatch += 1
        if isinstance(node, ast.Import):
            operator_imports += sum(1 for alias in node.names if alias.name == "operator")
        if isinstance(node, ast.ImportFrom) and node.module == "operator":
            operator_imports += 1
    return {"evalCalls": evals, "execCalls": execs,
            "getattrDispatchCalls": getattr_dispatch,
            "operatorModuleImports": operator_imports}


def scan_findings(authority, self_tree=None) -> list:
    """L4 gate over this file, plus the published evidence over BOTH predecessors."""
    findings = []
    tree = own_tree() if self_tree is None else self_tree
    self_scan = wire_comparison_scan(tree, "check-c2-v6.py")
    predecessor_scan = wire_comparison_scan(
        ast.parse(authority.snapshots[V4_CHECKER]), V4_CHECKER)
    v5_scan = wire_comparison_scan(ast.parse(authority.snapshots[V5_CHECKER]), V5_CHECKER)
    authority.scan_self = self_scan
    authority.scan_predecessor = predecessor_scan
    authority.scan_v5 = v5_scan
    for site in self_scan["sites"]:
        findings.append(
            "C2V6-SCAN: " + site["function"] + " line " + str(site["line"]) + " (" +
            site["kind"] + ") lets the wire-sourced " + site["wireOperand"] +
            " meet " + site["farOperand"] + ", which is not provably non-numeric and "
            "is not routed through a declared type gate: " + site["source"])
    if not jx_int_in_range(self_scan["gateCallSites"], 8, 10 ** 6):
        findings.append("C2V6-SCAN: only " + str(self_scan["gateCallSites"]) +
                        " guard-helper call site(s) were seen in this file, so the scan "
                        "cannot be distinguished from a vacuous one")
    primitives = self_scan["indirectionPrimitives"]
    for key, allowed, why in (
            ("evalCalls", 0, "which L4 structurally cannot follow"),
            ("getattrDispatchCalls", 0, "which L4 structurally cannot follow"),
            ("operatorModuleImports", 0,
             "and operator.ne is an ast.Call that no ast.Compare walk can ever see"),
            ("execCalls", DECLARED_EXEC_SITES,
             "and exactly two are declared: the verified-snapshot module loader and "
             "the self-mutation tree executor")):
        if jx_bind(jx_get(primitives, key), allowed) is not None:
            findings.append("C2V6-SCAN: this file carries " +
                            str(jx_get(primitives, key)) + " " + key + ", " + why)
    # The universe, recounted independently of the function that produces it.
    # `_function_universe` narrowed to top-level defs was caught in v5's lineage
    # only by new sites appearing, which is collateral; this is the layer saying
    # so directly.
    walked = [node for node in ast.walk(tree)
              if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))]
    gated = [node for node in walked
             if getattr(node, "name", "<lambda>") in GUARD_HELPERS]
    if jx_bind(self_scan["functionLikeNodes"], len(walked) - len(gated)) is not None:
        findings.append(
            "C2V6-SCAN-BLIND: the scan reports " + str(self_scan["functionLikeNodes"]) +
            " function-like node(s) but this file holds " + str(len(walked)) +
            " of them and excludes " + str(len(gated)) + " declared gates; a scan that "
            "does not walk nested defs, methods and lambdas is the narrowing that made "
            "IR-C2V4-01 invisible")
    # The scan is load-bearing only if it SEES the defects it was written for.
    adjudicated = adjudicated_census_lines(authority)
    if not jx_int_in_range(len(adjudicated), 1, 10 ** 6):
        findings.append(
            "C2V6-SCAN-BLIND: the pinned adjudication yields no comparison line at all, "
            "so the anchor that proves this scan sees the defect it exists to catch is "
            "vacuous; v5 could be silenced completely by exactly this, and the reviewer "
            "found it with zero findings")
    found = [site["line"] for site in predecessor_scan["sites"]]
    unseen = jx_sorted(jx_difference(adjudicated, found))
    if unseen:
        findings.append(
            "C2V6-SCAN-BLIND: run over the pinned predecessor this scan does NOT report "
            "the adjudicated census comparison(s) at line(s) " + repr(unseen) + "; a "
            "scan that cannot see the defect it exists to catch is decorative")
    # ... and the one its OWN predecessor could not see in its own file.
    v5_found = [site["line"] for site in v5_scan["sites"]]
    if not jx_in(V5_DEFECT_LINE, v5_found):
        findings.append(
            "C2V6-SCAN-BLIND: run over the pinned check-c2-v5.py this scan does NOT "
            "report line " + str(V5_DEFECT_LINE) + ", the subset test that produced "
            "IR-C2V5-01 and that v5's own scan classified as having no wire operand at "
            "all; if v6's model cannot see it, v6's model is v5's model")
    if not jx_int_in_range(predecessor_scan["ungatedComputedOperandComparisons"],
                           1, 10 ** 6):
        findings.append("C2V6-SCAN-BLIND: the scan reports no computed-operand "
                        "comparison anywhere in the predecessor, which contradicts the "
                        "measured adjudication and means the computed-operand model is "
                        "inert")
    return findings


V5_DEFECT_LINE = 1815
_OWN_SOURCE_CACHE = None


def own_source() -> bytes:
    """Read this file's bytes ONCE.  A checker cannot hash-pin itself; its own
    digest is reported, never verified."""
    global _OWN_SOURCE_CACHE
    if _OWN_SOURCE_CACHE is None:
        _OWN_SOURCE_CACHE = pathlib.Path(__file__).resolve().read_bytes()
    return _OWN_SOURCE_CACHE


def own_tree():
    return ast.parse(own_source())


# =============================================================================
# Section 7.  L5 -- the behavioural layer.  Reads no source at all.
#
# A NON-ZERO EXIT IS NOT EVIDENCE A GUARD FIRED.  Every assertion here is on a
# specific finding id AND on the finding naming the position under test.
# =============================================================================

HOSTILE_SPELLINGS = ("boolean-true", "boolean-false", "float-equal", "float-one",
                     "numeric-string", "null", "array", "object")


def _spelling_value(label, measured_value):
    if jx_equal(label, "float-equal"):
        return float(measured_value)
    if jx_equal(label, "float-one"):
        return 1.0
    if jx_equal(label, "numeric-string"):
        return str(measured_value)
    if jx_equal(label, "boolean-true"):
        return True
    if jx_equal(label, "boolean-false"):
        return False
    if jx_equal(label, "null"):
        return None
    if jx_equal(label, "array"):
        return []
    return {}


def _set_published(effective, position, value) -> bool:
    block = jx_get(effective, "hostileScalarLeafTotality")
    if jx_type(block) != "object":
        return False
    if position.startswith("surfaces["):
        name, _, key = position[len("surfaces["):].partition("].")
        rows = jx_get(block, "surfaces")
        for row in rows if jx_type(rows) == "array" else []:
            if jx_type(row) == "object" and jx_equal(jx_get(row, "id"), name):
                return jx_put(row, key, value)
        return False
    root = jx_get(block, "contractRoot")
    if jx_type(root) != "object":
        return False
    return jx_put(root, position[len("contractRoot."):], value)


def behavioural_layer(effective, measurement) -> dict:
    """L5.  Every registered position x every hostile JSON spelling."""
    positions = measured_positions(measurement)
    cases = named = admitted = misnamed = 0
    escapes = []
    for position in jx_sorted(list(positions)):
        measured_value = jx_get(positions, position)
        for label in HOSTILE_SPELLINGS:
            value = _spelling_value(label, measured_value)
            if jx_equal(value, measured_value):
                continue
            mutant = copy.deepcopy(effective)
            if not _set_published(mutant, position, value):
                escapes.append(position + "/" + label + ": the position could not be "
                               "reached")
                continue
            cases += 1
            findings = census_comparison_findings(mutant, measurement)
            hit = [item for item in findings
                   if item.startswith("C2V6-TYPE:") and position in item]
            if hit:
                named += 1
                continue
            if not findings:
                admitted += 1
                escapes.append(position + "/" + label + ": ADMITTED - " + repr(value) +
                               " was accepted where a JSON integer " +
                               str(measured_value) + " is declared")
                continue
            misnamed += 1
            escapes.append(position + "/" + label + ": rejected, but by " +
                           findings[0].split(":")[0] + " rather than a C2V6-TYPE "
                           "finding naming the position - a non-zero result that is "
                           "not evidence the type gate fired")
    # The COMPUTED operand is the one nobody was gating.  Corrupt the MEASUREMENT
    # rather than the document and require the instrument-side gate to fire.
    probes = probes_named = probes_escaped = 0
    for position in jx_sorted(list(positions)):
        measured_value = jx_get(positions, position)
        corrupt = copy.deepcopy(measurement)
        if not _corrupt_measurement(corrupt, position, float(measured_value)):
            continue
        probes += 1
        findings = census_comparison_findings(effective, corrupt)
        if [item for item in findings
                if item.startswith("C2V6-INSTRUMENT:") and position in item]:
            probes_named += 1
        else:
            probes_escaped += 1
            escapes.append(position + ": a float MEASURED value was not refused by the "
                           "computed-side gate")
    return {"positions": len(positions), "spellings": len(HOSTILE_SPELLINGS),
            "executedCases": cases, "namedTypeRejections": named,
            "admissions": admitted, "rejectedWithoutNamingThePosition": misnamed,
            "instrumentProbes": probes, "instrumentProbesNamed": probes_named,
            "instrumentProbesEscaped": probes_escaped, "escapes": escapes}


def _corrupt_measurement(measurement, position, value) -> bool:
    if position.startswith("surfaces["):
        name, _, key = position[len("surfaces["):].partition("].")
        entry = jx_get(jx_get(measurement, "surfaces"), name)
        if entry is None:
            return False
        for block in ("census", "stats"):
            target = jx_get(entry, block)
            if jx_type(target) == "object" and jx_has(target, key):
                jx_put(target, key, value)
        return True
    root = jx_get(measurement, "contractRoot")
    key = position[len("contractRoot."):]
    if not jx_has(root, key):
        return False
    return jx_put(root, key, value)


def str_proof_probe(tree) -> dict:
    """L5's proof-honesty probe.

    L4 excuses an operand when it is a call to a module-level function annotated
    `-> str`.  That is a proof only if the annotation is true, so every one of
    those functions is CALLED here over the JSON corpus and every result must be
    a `str`.  A structural claim about a signature, checked behaviourally.
    """
    declared = str_returning_functions(tree)
    probes = {
        "jx_type": lambda value: jx_type(value),
        "jx_canon": lambda value: jx_canon(value),
        "jx_key": lambda value: jx_key(value),
        "jx_frame": lambda value: jx_frame("s", str(value)),
        "_steps_text": lambda value: _steps_text([value, "x", 0]),
    }
    escapes = []
    unprobed = jx_sorted(jx_difference(declared, list(probes)))
    for name in unprobed:
        escapes.append(name + " is annotated `-> str` and L4 treats a call to it as "
                       "provably non-numeric, but no probe calls it, so the proof rests "
                       "on an unchecked signature")
    unknown = jx_sorted(jx_difference(list(probes), declared))
    for name in unknown:
        escapes.append(name + " is probed as a `-> str` proof but carries no `-> str` "
                       "annotation in the tree under test")
    cases = failures = 0
    for name in jx_sorted(list(probes)):
        if not jx_in(name, declared):
            continue
        for value in JX_CORPUS:
            cases += 1
            try:
                result = jx_get(probes, name)(value)
            except JxDomainError:
                continue
            except MALFORMED_SHAPE_EXCEPTIONS as exc:
                failures += 1
                escapes.append(name + " raised " + type(exc).__name__ + " on " +
                               repr(value))
                continue
            if jx_type(result) != "string":
                failures += 1
                escapes.append(name + " is annotated `-> str` but returned a " +
                               jx_type(result) + " for " + repr(value))
    return {"declared": len(declared), "probed": len(probes), "executedCases": cases,
            "failures": failures, "escapes": escapes}


def ast_field_probe(tree) -> dict:
    """L5's second proof-honesty probe.

    L4's AST-STR-FIELD proof asserts that `.id`, `.attr`, `.arg`, `.name` and
    `.module` are strings on every node that carries them.  That is a fact about
    the host's `ast` module, so it is MEASURED over this file's own tree rather
    than assumed.
    """
    cases = failures = 0
    escapes = []
    for node in ast.walk(tree):
        for field in jx_sorted(list(_AST_STR_FIELDS)):
            if not hasattr(node, field):
                continue
            value = getattr(node, field)
            if value is None:
                continue
            cases += 1
            if jx_type(value) != "string":
                failures += 1
                escapes.append(type(node).__name__ + "." + field + " is a " +
                               jx_type(value) + ", so the AST-STR-FIELD proof is false")
    return {"executedCases": cases, "failures": failures, "escapes": escapes}


def behavioural_findings(effective, measurement, authority, tree) -> list:
    result = behavioural_layer(effective, measurement)
    authority.behavioural = result
    result["strProof"] = str_proof_probe(tree)
    result["astProof"] = ast_field_probe(tree)
    findings = []
    if not jx_int_in_range(result["executedCases"], 1, 10 ** 9):
        findings.append("C2V6-BEHAVIOUR: the behavioural layer executed no case at all")
    if jx_bind(result["admissions"], 0) is not None:
        findings.append("C2V6-BEHAVIOUR: " + str(result["admissions"]) +
                        " type-distinct spelling(s) of a published integer counter were "
                        "ADMITTED by the repaired comparator")
    if jx_bind(result["rejectedWithoutNamingThePosition"], 0) is not None:
        findings.append(
            "C2V6-BEHAVIOUR: " + str(result["rejectedWithoutNamingThePosition"]) +
            " case(s) were rejected without a C2V6-TYPE finding naming the position; "
            "that is the adjudication's trap, where a non-zero exit came from unrelated "
            "arithmetic")
    if jx_bind(result["namedTypeRejections"], result["executedCases"]) is not None:
        findings.append("C2V6-BEHAVIOUR: " + str(result["namedTypeRejections"]) + " of " +
                        str(result["executedCases"]) + " cases produced a named type "
                        "finding")
    if not jx_int_in_range(result["instrumentProbes"], 1, 10 ** 9):
        findings.append("C2V6-BEHAVIOUR: the computed-operand gate was never probed, so "
                        "the half of the repair that guards the instrument's own side "
                        "is unfalsified")
    if jx_bind(result["instrumentProbesEscaped"], 0) is not None:
        findings.append("C2V6-BEHAVIOUR: " + str(result["instrumentProbesEscaped"]) +
                        " float MEASURED value(s) were accepted; the computed side of "
                        "the comparison is ungated, which is the operand type "
                        "IR-C2V4-01 names")
    findings.extend("C2V6-PROOF: " + item for item in result["strProof"]["escapes"])
    findings.extend("C2V6-PROOF: " + item for item in result["astProof"]["escapes"])
    if not jx_int_in_range(result["strProof"]["executedCases"], 1, 10 ** 9) or \
            not jx_int_in_range(result["astProof"]["executedCases"], 1, 10 ** 9):
        findings.append("C2V6-PROOF: L4's non-numeric proofs were not exercised, so the "
                        "excusals they grant rest on unchecked signatures")
    primitive = authority.primitive
    findings.extend("C2V6-PRIMITIVE: " + item for item in primitive["escapes"])
    for key, expected in (("tokenCollisions", 0), ("crossTypeAdmissions", 0),
                          ("gateAdmissions", 0), ("reflexiveFailures", 0),
                          ("entryPointFailures", 0)):
        if jx_bind(jx_get(primitive, key), expected) is not None:
            findings.append("C2V6-PRIMITIVE: " + key + " is " +
                            str(jx_get(primitive, key)) + ", not " + str(expected) +
                            "; the single decision point every other layer is built on "
                            "does not hold its own property")
    # Vacuity floors.  Zeroing the primitive's own test must not look like a
    # pass: every count below is required to be positive before the equalities
    # above mean anything.
    for key in ("corpusValues", "corpusPairs", "operatorSpaceRows", "gateCases",
                "entryPointCases", "domainRefusals"):
        if not jx_int_in_range(jx_get(primitive, key), 1, 10 ** 9):
            findings.append("C2V6-PRIMITIVE: " + key + " is " +
                            repr(jx_get(primitive, key)) + "; the primitive's own "
                            "exhaustive test has stopped executing, so every equality "
                            "it reports is a statement about an empty set")
    if jx_bind(primitive["roundTrips"], primitive["corpusValues"]) is not None or \
            jx_bind(primitive["distinctTokens"], primitive["corpusValues"]) is not None:
        findings.append("C2V6-PRIMITIVE: the canonical encoding is not invertible over "
                        "the corpus, so it is not injective, so it can conflate two "
                        "distinct JSON values and nothing built on it holds")
    if jx_bind(primitive["operatorSpaceHazardsReproduced"],
               primitive["operatorSpaceRows"]) is not None or \
            jx_bind(primitive["operatorSpaceRowsCovered"],
                    primitive["operatorSpaceRows"]) is not None:
        findings.append("C2V6-PRIMITIVE: the operator space is not fully demonstrated "
                        "and covered; a hazard table nobody re-runs is the failure mode "
                        "this artifact exists to close")
    return findings


# =============================================================================
# Section 8.  L6 -- the predecessor differential, L6b -- the EXHAUSTIVE
# whole-document sweep, and L6c -- the differential against the REJECTED v5.
#
# L6b is the repair for OBS-01 / IR-C2V5-03's sweep half.  v5 printed
# `136 / 57 / 32` as literal f-string text and range-tested the contract's
# copies at 1..10**6, so the reviewer republished them as 1 / 1 / 1 / 0 and the
# run stayed green with the banner unchanged.  A published measurement the run
# does not recompute is not evidence.  Every one of those figures is now
# recomputed here, on every invocation, by executing the pinned predecessor once
# per integer leaf of the pinned predecessor document, and bound.  It costs
# about a minute and the elapsed time is published.
#
# The result is a pure function of two hash-verified inputs, so it is cached on
# the Authority for the process.  That is sound precisely because no mutation of
# THIS file can change it -- and the L7 rows that target the code computing it
# clear the cache explicitly rather than being served a stale answer.
# =============================================================================

DIFFERENTIAL_VECTORS = (
    ("FA-1-minimal-single-edit", "contractRoot.scalarLeafPaths", "float-equal",
     "the adjudication's record: ONE JSON edit, zero bytes of Python, exit 0"),
    ("FA-1-replicated-enumerated-paths", "contractRoot.enumeratedPaths", "float-equal",
     "replicated position from the adjudication"),
    ("FA-1-replicated-surface-paths", "surfaces[plan-intent].enumeratedPaths",
     "float-equal", "replicated position from the adjudication"),
    ("FA-2-boolean-at-the-self-referential-counter",
     "surfaces[coverage].typeDistinctConstantAdmissions", "boolean-false",
     "the counter admitted in a type-distinct spelling IS the counter whose declared "
     "meaning is that no type-distinct spelling may be admitted"),
    ("FA-3-admit-then-raise-as-boolean", "surfaces[stage-plan].admitThenRaise",
     "boolean-false", "one of the nine positions of the combined mutation"),
    ("FA-3-unguarded-escapes-as-float", "surfaces[plan-intent].unguardedEscapes",
     "float-one", "one of the nine positions of the combined mutation"),
)

# The v5 REJECT's own blocking vectors, retained as executable cases.  Each is
# applied to the PINNED c2-plan-stage-schema.v5.json and driven through the
# PINNED check-c2-v5.py, which must still admit it to a FULLY GREEN run, and
# then applied to the analogous position of THIS candidate, which must be named.
SUCCESSOR_DIFFERENTIAL_VECTORS = (
    ("IR-C2V5-01-subset-test-float",
     ["theDefect", "repairedComparisonSites", 0, "line"],
     ["theDefect", "repairedComparisonSites", 0, "line"], "float-equal",
     "one JSON edit, zero bytes of Python: `{2487} <= {2487.0}` is True, so v5's own "
     "repro enumeration admitted a float at the site certifying the repair"),
    ("IR-C2V5-03-false-accept-counter-as-boolean",
     ["retainedFalseAcceptVectors", "measuredThisRun", "predecessorFullyGreenRuns"],
     ["retainedFalseAcceptVectors", "measuredThisRun", "predecessorFullyGreenRuns"],
     "boolean-true",
     "the FA-2 spelling admitted at a counter whose stated meaning is the number of "
     "false accepts measured this run"),
    ("IR-C2V5-03-sweep-figure-arbitrary-drift",
     ["theDefect", "wholeDocumentSweep", "admittedByPredecessorToAFullGreenRun"],
     ["theDefect", "wholeDocumentSweep", "admittedByPredecessorToAFullGreenRun"],
     "drift-to-one",
     "the headline sweep figure republished as 1 with the banner still asserting the "
     "authoring-time number, because the run never recomputed it"),
)


def _v4_measurement(authority):
    v4 = authority.v4
    contract = copy.deepcopy(authority.json(V4_CONTRACT))
    fp = authority.json(FP)
    relations, _reason = jx_string_set(
        _resolve_steps(fp, ("relationRegistry", "relations")) if fp else [])
    values = v4._matrix_values(contract.get("planIntentTotalityMatrix", {}))
    intent_values, _ = v4._intent_fixture_values(contract)
    surfaces = v4.measure_surfaces(contract, relations or set(), fp, values, intent_values)
    root_census, _ = v4.measure_contract_root(contract, authority.v4_authority,
                                              execute=False)
    return contract, {"surfaces": surfaces, "contractRoot": root_census}


def predecessor_differential(authority) -> dict:
    """L6.  Executed against BOTH checkers, on the pinned predecessor document."""
    v4 = authority.v4
    contract, measurement = _v4_measurement(authority)
    positions = measured_positions(measurement)
    rows, escapes = [], []
    predecessor_admitted = successor_rejected = fully_green = 0
    for vector, position, spelling, note in DIFFERENTIAL_VECTORS:
        if not jx_has(positions, position):
            escapes.append(vector + ": " + position + " is not a measured position of "
                           "the pinned predecessor document")
            continue
        value = _spelling_value(spelling, jx_get(positions, position))
        mutant = copy.deepcopy(contract)
        if not _set_published(mutant, position, value):
            escapes.append(vector + ": " + position + " could not be reached")
            continue
        cache_key = "differential/" + vector
        v4_findings = jx_get(authority.pinned, cache_key)
        if v4_findings is None:
            try:
                v4_findings = v4.check(copy.deepcopy(mutant), authority.v4_authority)
            except BaseException as exc:                # noqa: BLE001 - measured
                v4_findings = ["pinned predecessor raised " + type(exc).__name__]
            jx_put(authority.pinned, cache_key, [str(item) for item in v4_findings])
        v4_named = [item for item in v4_findings if position in str(item)]
        v6_findings = census_comparison_findings(mutant, measurement)
        v6_named = [item for item in v6_findings
                    if item.startswith("C2V6-TYPE:") and position in item]
        if not v4_named:
            predecessor_admitted += 1
        if not v4_findings:
            fully_green += 1
        if v6_named:
            successor_rejected += 1
        else:
            escapes.append(vector + ": this checker did NOT reject " + position +
                           " spelled " + spelling + " with a C2V6-TYPE finding naming "
                           "the position")
        rows.append({"vector": vector, "position": position, "spelling": spelling,
                     "note": note, "predecessorFindingCount": len(v4_findings),
                     "predecessorNamedThePosition": bool(v4_named),
                     "predecessorFullyGreen": not v4_findings,
                     "successorNamedThePosition": bool(v6_named)})
    return {"vectors": len(DIFFERENTIAL_VECTORS), "rows": rows,
            "predecessorAdmittedThePosition": predecessor_admitted,
            "predecessorFullyGreenRuns": fully_green,
            "successorRejectedByName": successor_rejected, "escapes": escapes}


def predecessor_sweep(authority) -> dict:
    """L6b.  EXHAUSTIVE, not sampled.  A float at every integer leaf of the
    pinned predecessor document in turn, each mutant driven through a complete
    run of the pinned predecessor checker."""
    cached = jx_get(authority.pinned, "sweep")
    if cached is not None:
        return cached
    v4 = authority.v4
    base = authority.json(V4_CONTRACT)
    leaves = _integer_leaf_steps(base)
    started = time.time()
    admitted, census, outside, rejected = [], [], [], []
    sink = io.StringIO()
    for steps in leaves:
        mutant = copy.deepcopy(base)
        current = _resolve_steps(mutant, steps)
        _assign_steps(mutant, steps, float(current))
        try:
            with redirect_stdout(sink):
                findings = v4.check(copy.deepcopy(mutant), authority.v4_authority)
        except BaseException as exc:                    # noqa: BLE001 - measured
            findings = ["pinned predecessor raised " + type(exc).__name__]
        text = _steps_text(steps)
        if findings:
            rejected.append(text)
            continue
        admitted.append(text)
        if jx_equal(steps[:1], ["hostileScalarLeafTotality"]):
            census.append(text)
        else:
            outside.append(text)
    result = {
        "integerLeavesInjected": len(leaves),
        "admittedToAFullGreenRun": len(admitted),
        "rejectedByPredecessor": len(rejected),
        "admittedCensusCounters": len(census),
        "admittedOutsideTheCensusBlock": len(outside),
        "admittedPaths": jx_sorted(admitted),
        "outsidePaths": jx_sorted(outside),
        "elapsedSeconds": int(time.time() - started),
    }
    jx_put(authority.pinned, "sweep", result)
    return result


# A position the sweep MUST find admitted.  It is the sharpest of the 25: the
# upper bound of a range inside the predecessor's OWN integer-constant register,
# the register whose stated purpose is that a fifth site cannot be added
# silently.  If the sweep stops naming it, the sweep has stopped measuring.
SWEEP_ANCHOR_PATHS = (
    "planIntent/integerConstantFields/fields/4/range/1",
    "planIntent/wireTypes/stageBudgetV1/limit/maximum",
    "planIntent/admissionDescriptorV1/budgets/maxEntries",
)


def sweep_findings(authority) -> list:
    """The sweep's own consistency, asserted by the LAYER and not by a counter.

    Every check here fires from the sweep's internal arithmetic and from named
    anchor positions.  None of them reads a published number, so republishing a
    counter cannot silence any of them.
    """
    sweep = predecessor_sweep(authority)
    authority.sweep = sweep
    findings = []
    base = authority.json(V4_CONTRACT)
    live_leaves = len(_integer_leaf_steps(base))
    if jx_bind(sweep["integerLeavesInjected"], live_leaves) is not None:
        findings.append("C2V6-SWEEP: the sweep reports " +
                        str(sweep["integerLeavesInjected"]) + " integer leaves injected "
                        "but the pinned predecessor document holds " + str(live_leaves))
    total = sweep["admittedToAFullGreenRun"] + sweep["rejectedByPredecessor"]
    if jx_bind(total, sweep["integerLeavesInjected"]) is not None:
        findings.append("C2V6-SWEEP: admitted plus rejected is " + str(total) + " but " +
                        str(sweep["integerLeavesInjected"]) + " leaves were injected; "
                        "the sweep did not run to completion")
    parts = sweep["admittedCensusCounters"] + sweep["admittedOutsideTheCensusBlock"]
    if jx_bind(parts, sweep["admittedToAFullGreenRun"]) is not None:
        findings.append("C2V6-SWEEP: the census and non-census admissions sum to " +
                        str(parts) + " but " + str(sweep["admittedToAFullGreenRun"]) +
                        " leaves were admitted")
    if not jx_int_in_range(sweep["admittedOutsideTheCensusBlock"], 1, 10 ** 6):
        findings.append("C2V6-SWEEP: no leaf OUTSIDE the census block drives the pinned "
                        "predecessor to a fully green run, so the measured claim that "
                        "three sites was not the complete set is no longer reproduced")
    missing = jx_sorted(jx_difference(list(SWEEP_ANCHOR_PATHS), sweep["outsidePaths"]))
    if missing:
        findings.append("C2V6-SWEEP: the sweep no longer finds " + repr(missing) +
                        " admitted to a fully green predecessor run; the sharpest of "
                        "these is the upper bound inside the predecessor's own "
                        "integer-constant register, and a sweep that stops seeing it "
                        "has stopped measuring the thing it is cited for")
    return findings


def successor_differential(authority, candidate) -> dict:
    """L6c.  The v5 REJECT's blocking vectors, executed against the PINNED v5.

    This is what stands behind the repair without trusting anything this file
    believes about itself.  check-c2-v5.py is pinned; it cannot change; it still
    admits every one of these to a fully green run.  v6 must name each.
    """
    cached = jx_get(authority.pinned, "v5admissions")
    if cached is None:
        cached = _v5_admissions(authority)
        jx_put(authority.pinned, "v5admissions", cached)
    rows, escapes = [], []
    admitted = rejected = 0
    for vector, v5_path, v6_path, spelling, note in SUCCESSOR_DIFFERENTIAL_VECTORS:
        record = [item for item in cached if jx_equal(jx_get(item, "vector"), vector)]
        v5_green = bool(record) and jx_get(record[0], "fullyGreen") is True
        if v5_green:
            admitted += 1
        else:
            escapes.append(vector + ": the PINNED check-c2-v5.py no longer admits " +
                           _steps_text(v5_path) + " to a fully green run, so the "
                           "differential this repair is measured against has collapsed")
        mutant = copy.deepcopy(candidate)
        named = False
        try:
            current = _resolve_steps(mutant, v6_path)
        except MALFORMED_SHAPE_EXCEPTIONS:
            escapes.append(vector + ": " + _steps_text(v6_path) + " does not resolve in "
                           "this candidate, so the vector is not retained as an "
                           "executable case")
            rows.append({"vector": vector, "path": _steps_text(v6_path), "note": note,
                         "v5FullyGreen": v5_green, "v6NamedThePosition": False})
            continue
        value = float(current) if jx_equal(spelling, "float-equal") else \
            (True if jx_equal(spelling, "boolean-true") else 1)
        _assign_steps(mutant, v6_path, value)
        findings = candidate_probe_findings(mutant, authority)
        named = bool([item for item in findings if _steps_text(v6_path) in item])
        if named:
            rejected += 1
        else:
            escapes.append(vector + ": this checker did NOT name " +
                           _steps_text(v6_path) + " when it was spelled " + spelling)
        rows.append({"vector": vector, "path": _steps_text(v6_path), "note": note,
                     "v5FullyGreen": v5_green, "v6NamedThePosition": named})
    return {"vectors": len(SUCCESSOR_DIFFERENTIAL_VECTORS), "rows": rows,
            "v5AdmittedToAFullGreenRun": admitted, "v6RejectedByName": rejected,
            "escapes": escapes}


def _v5_admissions(authority) -> list:
    """Execute the PINNED check-c2-v5.py over the PINNED v5 contract, mutated.

    Read as inert bytes, hash-verified at load, executed from that verified
    snapshot.  Never a second disk read between verification and execution.
    """
    sink = io.StringIO()
    out = []
    try:
        with redirect_stdout(sink):
            v5 = _execute_snapshot("opensip_c2v6_pinned_v5_checker", V5_CHECKER,
                                   authority.snapshots[V5_CHECKER], authority.directory)
            v5_authority = v5.load_authority(authority.directory)
    except BaseException as exc:                        # noqa: BLE001 - measured
        return [{"vector": vector, "fullyGreen": None,
                 "why": "the pinned v5 checker could not be executed: " +
                        type(exc).__name__ + ": " + str(exc)}
                for vector, _a, _b, _c, _d in SUCCESSOR_DIFFERENTIAL_VECTORS]
    contract = authority.json(V5_CONTRACT)
    for vector, v5_path, _v6_path, spelling, _note in SUCCESSOR_DIFFERENTIAL_VECTORS:
        mutant = copy.deepcopy(contract)
        try:
            current = _resolve_steps(mutant, v5_path)
        except MALFORMED_SHAPE_EXCEPTIONS:
            out.append({"vector": vector, "fullyGreen": None,
                        "why": "the position does not resolve in the pinned v5 contract"})
            continue
        value = float(current) if jx_equal(spelling, "float-equal") else \
            (True if jx_equal(spelling, "boolean-true") else 1)
        _assign_steps(mutant, v5_path, value)
        try:
            with redirect_stdout(sink):
                findings = v5.check(copy.deepcopy(mutant), v5_authority)
        except BaseException as exc:                    # noqa: BLE001 - measured
            findings = ["pinned v5 raised " + type(exc).__name__ + ": " + str(exc)]
        out.append({"vector": vector, "fullyGreen": not findings,
                    "findingCount": len(findings),
                    "why": "" if not findings else str(findings[0])[:160]})
    return out


# =============================================================================
# Section 9.  The measured register, and a banner that cannot carry a number the
# run did not compute.
#
# This is the repair for OBS-01 and for the sweep half of IR-C2V5-03.  In v5 the
# banner's headline figures were literal f-string text: the reviewer republished
# the contract to 1 / 1 / 1 / 0 and the run stayed green with the banner
# unchanged, still asserting 136 / 57 / 32.
#
# In v6 there is no f-string in the banner.  Every line is a TEMPLATE rendered
# by `str.format_map` over the live register, so a number can only reach the
# banner by being looked up under the name of the thing it claims to measure --
# and a template naming a key the run does not measure raises rather than
# printing.  A separate structural check refuses any template that carries a
# digit outside an alphanumeric token, so `0 type-distinct admissions` cannot be
# written as text at all.  L7 breaks both halves.
# =============================================================================

RUNTIME_ONLY_FIELDS = ("sweepElapsedSeconds",)


def live_register(authority) -> dict:
    """Every number this run measured, under the name of what it measures."""
    positions = measured_positions(authority.measurement)
    scan, pre, v5s = authority.scan_self, authority.scan_predecessor, authority.scan_v5
    beh, lock = authority.behavioural, authority.document_lock
    cand, sweep = authority.candidate_lock, authority.sweep
    diff, succ, prim = authority.differential, authority.successor, authority.primitive
    boolean_exploitable = 0
    for position in positions:
        value = jx_get(positions, position)
        if jx_int(value) and jx_in(value, [0, 1]):
            boolean_exploitable += 1
    return {
        "registeredCensusPositions": len(positions),
        "censusPositionsBooleanExploitable": boolean_exploitable,
        "adjudicatedComparisonSites": len(adjudicated_census_lines(authority)),
        "primitiveCorpusValues": prim["corpusValues"],
        "primitiveCorpusPairs": prim["corpusPairs"],
        "primitiveRoundTrips": prim["roundTrips"],
        "primitiveDistinctTokens": prim["distinctTokens"],
        "primitiveStricterThanHostEquality": prim["stricterThanHostEquality"],
        "primitiveLooserThanHostEquality": prim["looserThanHostEquality"],
        "primitiveCrossTypeAdmissions": prim["crossTypeAdmissions"],
        "primitiveGateCases": prim["gateCases"],
        "primitiveGateAdmissions": prim["gateAdmissions"],
        "primitiveOperatorSpaceRows": prim["operatorSpaceRows"],
        "primitiveOperatorSpaceHazardsReproduced":
            prim["operatorSpaceHazardsReproduced"],
        "primitiveOperatorSpaceRowsCovered": prim["operatorSpaceRowsCovered"],
        "primitiveEntryPointCases": prim["entryPointCases"],
        "primitiveDomainRefusals": prim["domainRefusals"],
        "primitiveFreeNamesOutsideTheBoundary": authority.portability["freeNames"],
        "effectiveIntegerLeavesTypeLocked": lock["lockedLeaves"],
        "effectiveTypeProbeCases": lock["executedCases"],
        "effectiveTypeProbeNamedRejections": lock["namedTypeRejections"],
        "effectiveTypeProbeAdmissions": lock["admissions"],
        "candidateIntegerLeavesBound": cand["boundLeaves"],
        "candidateProbeCases": cand["executedCases"],
        "candidateProbeAdmissions": cand["admissions"],
        "scanSelfUngatedWireComparisons": scan["ungatedWireComparisons"],
        "scanSelfFunctionLikeNodes": scan["functionLikeNodes"],
        "scanSelfGateCallSites": scan["gateCallSites"],
        "scanSelfGateExcusedSites": scan["gateExcusedSites"],
        "scanPredecessorUngatedWireComparisons": pre["ungatedWireComparisons"],
        "scanPredecessorUngatedComputedOperandComparisons":
            pre["ungatedComputedOperandComparisons"],
        "scanPredecessorFunctionLikeNodes": pre["functionLikeNodes"],
        "scanV5UngatedWireComparisons": v5s["ungatedWireComparisons"],
        "scanV5FunctionLikeNodes": v5s["functionLikeNodes"],
        "behaviouralExecutedCases": beh["executedCases"],
        "behaviouralNamedTypeRejections": beh["namedTypeRejections"],
        "behaviouralAdmissions": beh["admissions"],
        "behaviouralInstrumentProbes": beh["instrumentProbes"],
        "behaviouralInstrumentProbesNamed": beh["instrumentProbesNamed"],
        "strProofFunctions": beh["strProof"]["declared"],
        "strProofExecutedCases": beh["strProof"]["executedCases"],
        "astFieldProofExecutedCases": beh["astProof"]["executedCases"],
        "differentialVectors": diff["vectors"],
        "differentialPredecessorAdmitted": diff["predecessorAdmittedThePosition"],
        "differentialPredecessorFullyGreen": diff["predecessorFullyGreenRuns"],
        "differentialSuccessorRejectedByName": diff["successorRejectedByName"],
        "successorDifferentialVectors": succ["vectors"],
        "successorV5AdmittedFullyGreen": succ["v5AdmittedToAFullGreenRun"],
        "successorV6RejectedByName": succ["v6RejectedByName"],
        "sweepIntegerLeavesInjected": sweep["integerLeavesInjected"],
        "sweepAdmittedToFullGreen": sweep["admittedToAFullGreenRun"],
        "sweepRejectedByPredecessor": sweep["rejectedByPredecessor"],
        "sweepAdmittedCensusCounters": sweep["admittedCensusCounters"],
        "sweepAdmittedOutsideCensus": sweep["admittedOutsideTheCensusBlock"],
        "selftestContractMutations": len(CONTRACT_MUTATIONS),
        "selftestSourceMutations": len(SOURCE_MUTATIONS),
        "selftestScanMutations": len(SCAN_MUTATIONS),
        "pinnedInputs": len(PINS),
    }


BANNER_TEMPLATES = (
    "C-2 v6 contract OK - {documentName}; IR-C2V4-01 and the four blocking findings "
    "of the v5 REJECT repaired at the comparison primitive, {pinnedInputs} inputs "
    "hash-verified before execution, and the pinned check-c2-v4.py executed from its "
    "verified snapshot as the inherited oracle over the v4-identity projection",
    "  law eighteen, executable: the jx primitive canonicalises "
    "{primitiveCorpusValues} corpus values to {primitiveDistinctTokens} distinct "
    "tokens, inverts every one of them ({primitiveRoundTrips} round trips, so the "
    "encoding is injective), refuses {primitiveCrossTypeAdmissions} cross-type pairs "
    "over {primitiveCorpusPairs} pairs, and is stricter than host equality at "
    "{primitiveStricterThanHostEquality} of them and looser at "
    "{primitiveLooserThanHostEquality} (NaN, which host equality makes non-reflexive)",
    "  operator space: {primitiveOperatorSpaceRows} rows, "
    "{primitiveOperatorSpaceHazardsReproduced} with the host-language hazard "
    "demonstrated live this run and {primitiveOperatorSpaceRowsCovered} answered "
    "differently by the primitive; the primitive block has "
    "{primitiveFreeNamesOutsideTheBoundary} free name(s) outside its declared "
    "portability boundary, so another checker can adopt it unchanged",
    "  L2/L3 law eighteen: {registeredCensusPositions} published counter positions "
    "bound by canonical-string equality after an independent type assertion on each "
    "side, all of them registered against the live measurement in both directions; "
    "{censusPositionsBooleanExploitable} of them currently hold a value the host "
    "language would also accept as a boolean",
    "  L2b effective-contract type lock: {effectiveIntegerLeavesTypeLocked} integer "
    "leaves locked against the verified predecessor and float-probed live; "
    "{effectiveTypeProbeNamedRejections} named, {effectiveTypeProbeAdmissions} admitted",
    "  L2c candidate-document binding: {candidateIntegerLeavesBound} integer leaves of "
    "THIS document bound to a value this run measured or to a verified pinned byte, "
    "with no unbound bucket; {candidateProbeCases} hostile spelling and value-drift "
    "and control probes at those leaves, of which {candidateProbeAdmissions} were "
    "admitted",
    "  L4 inverted scan: {scanSelfUngatedWireComparisons} ungated wire comparison(s) in "
    "this file over {scanSelfFunctionLikeNodes} function-like nodes, with "
    "{scanSelfGateCallSites} gate call sites and {scanSelfGateExcusedSites} site(s) "
    "excused by textual gate dominance; over the pinned check-c2-v4.py it reports "
    "{scanPredecessorUngatedWireComparisons} of which "
    "{scanPredecessorUngatedComputedOperandComparisons} have a COMPUTED far operand, "
    "and over the pinned check-c2-v5.py it reports {scanV5UngatedWireComparisons}, "
    "including the subset test that produced IR-C2V5-01 and that v5's own scan "
    "classified as having no wire operand at all",
    "  L5 behavioural (reads no source): {behaviouralExecutedCases} cases over "
    "{registeredCensusPositions} positions, {behaviouralNamedTypeRejections} rejected "
    "by a finding naming the position, {behaviouralAdmissions} admitted; "
    "{behaviouralInstrumentProbes} instrument probes corrupt the COMPUTED side and "
    "{behaviouralInstrumentProbesNamed} were refused by name; L4's non-numeric proofs "
    "are themselves probed at {strProofExecutedCases} and "
    "{astFieldProofExecutedCases} cases",
    "  L6 differential: {differentialVectors} retained false-accept vectors; the pinned "
    "check-c2-v4.py admitted {differentialPredecessorAdmitted} of them "
    "({differentialPredecessorFullyGreen} to a fully green run) and this checker "
    "rejected {differentialSuccessorRejectedByName} by name",
    "  L6b whole-document sweep, EXHAUSTIVE this run and not sampled: a float at each "
    "of {sweepIntegerLeavesInjected} integer leaves of the pinned predecessor "
    "document, each mutant driven through a complete run of the pinned predecessor; "
    "{sweepAdmittedToFullGreen} drive it to a full green run and "
    "{sweepRejectedByPredecessor} are refused, of the admitted only "
    "{sweepAdmittedCensusCounters} are census counters and "
    "{sweepAdmittedOutsideCensus} lie outside the census block entirely; measured in "
    "{sweepElapsedSeconds} seconds",
    "  L6c successor differential: {successorDifferentialVectors} blocking vectors from "
    "the pinned v5 REJECT; the pinned check-c2-v5.py still admits "
    "{successorV5AdmittedFullyGreen} of them to a FULLY GREEN run and this checker "
    "named {successorV6RejectedByName} at the analogous position of its own document",
    "  own bytes reported not verified (a checker cannot pin itself): sha256:{ownDigest}",
    "  scope: checker-scope evidence only; SPECIFIED / IMPLEMENTABLE_UNEXECUTED; "
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW; independent re-review "
    "REQUIRED; no seal, freeze, integration or product acceptance is declared; "
    "CD-RT-5 remains BLOCKED_ON_PHASE_1A",
)

_TOKEN_RE = re.compile(r"[A-Za-z0-9_.\-]+")
_FIELD_RE = re.compile(r"\{([A-Za-z0-9_]+)\}")


def banner_digit_tokens(templates) -> list:
    """Every digit run in banner literal text that is not part of a word.

    `L2b`, `sha256` and `IR-C2V4-01` are tokens that carry letters and are
    labels.  A bare `57` is a measurement, and a measurement may not be written
    as text -- it has to arrive through the register, under the name of the
    thing it measures.
    """
    out = []
    for template in templates:
        for token in _TOKEN_RE.findall(_FIELD_RE.sub(" ", template)):
            if not any(character.isdigit() for character in token):
                continue
            if any("a" <= character.lower() <= "z" for character in token):
                continue
            out.append(token)
    return out


def render_banner(templates, live, runtime) -> list:
    values = {}
    for key in live:
        jx_put(values, key, str(jx_get(live, key)))
    for key in runtime:
        jx_put(values, key, str(jx_get(runtime, key)))
    return [template.format_map(values) for template in templates]


BANNER_DETECTOR_PROBE = ("an authoring-time sweep of all 136 integer leaves found 57",)
PORTABILITY_DETECTOR_PROBE = (
    "\n# --- BEGIN JX PRIMITIVE ---\ndef f():\n    return _something_outside\n"
    "\n# --- END JX PRIMITIVE ---\n")


def banner_findings(live, runtime) -> list:
    """The banner is evidence only if the run computed everything in it."""
    findings = []
    # The detector, probed.  `banner_digit_tokens` returning [] is
    # indistinguishable from a clean banner unless the detector is shown to fire
    # on text that carries a bare measurement -- which is the exact sentence v5
    # printed over a contract republished to contradict it.
    if not jx_int_in_range(len(banner_digit_tokens(BANNER_DETECTOR_PROBE)), 1, 10 ** 6):
        findings.append(
            "C2V6-BANNER: the bare-digit detector does not fire on " +
            repr(BANNER_DETECTOR_PROBE[0]) + ", so its clean verdict over the real "
            "templates is a statement about an instrument that detects nothing")
    rendered = render_banner(("probe {sweepIntegerLeavesInjected} probe",),
                             live, runtime) if jx_has(live, "sweepIntegerLeavesInjected") \
        else ["probe {sweepIntegerLeavesInjected} probe"]
    if "{" in rendered[0] or "}" in rendered[0]:
        findings.append(
            "C2V6-BANNER: the renderer left an uninterpolated field in " +
            repr(rendered[0]) + ", so the banner would print the NAME of a measurement "
            "instead of the measurement")
    for token in jx_sorted(jx_unique(banner_digit_tokens(BANNER_TEMPLATES))):
        findings.append(
            "C2V6-BANNER: the banner carries the literal figure " + repr(token) +
            " as source text; a number the run does not recompute and bind is not "
            "evidence, and v5's banner asserted its headline sweep figures over a "
            "contract that had been republished to contradict them")
    referenced = []
    for template in BANNER_TEMPLATES:
        referenced.extend(_FIELD_RE.findall(template))
    available = list(live) + list(runtime)
    unknown = jx_sorted(jx_difference(jx_unique(referenced), available))
    for key in unknown:
        findings.append("C2V6-BANNER: the banner interpolates " + key + ", which this "
                        "run does not measure")
    if not jx_int_in_range(len(jx_unique(referenced)), 1, 10 ** 6):
        findings.append("C2V6-BANNER: the banner interpolates nothing, so every figure "
                        "in it would be source text")
    declared = jx_sorted(list(RUNTIME_ONLY_FIELDS))
    if not jx_equal(jx_sorted(list(runtime)), declared):
        findings.append("C2V6-BANNER: the run-only banner fields are " +
                        repr(jx_sorted(list(runtime))) + ", not the declared " +
                        repr(declared) + "; a field that cannot be bound must be "
                        "declared, because an undeclared one is a published number "
                        "nobody checks")
    return findings


def jx_portability_findings(source: bytes) -> dict:
    """Is the primitive block genuinely self-contained?

    `usable by other checkers unchanged` is a coverage claim like any other and
    is held to the same standard: the delimited region is parsed, every free
    name it loads is collected, and anything outside its own definitions, the
    Python builtins and the declared boundary is reported.
    """
    text = source.decode("utf-8")
    # The markers are matched at the start of a line, so the copies of them in
    # the module docstring cannot be mistaken for the block itself.
    open_marker = "\n# --- BEGIN JX PRIMITIVE ---\n"
    close_marker = "\n# --- END JX PRIMITIVE ---\n"
    start = text.find(open_marker)
    end = text.find(close_marker)
    if start < 0 or end < 0 or end < start:
        return {"freeNames": -1, "names": ["the primitive block delimiters are absent"]}
    block = ast.parse(text[start + len(open_marker):end])
    defined, loaded = set(), set()
    for node in ast.walk(block):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
            for group in ():
                defined |= group
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                defined.add(node.id)
            else:
                loaded.add(node.id)
        elif isinstance(node, ast.arg):
            defined.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                bound = alias.asname or alias.name.split(".")[0]
                if jx_type(bound) != "string":
                    continue
                defined.add(bound)
        elif isinstance(node, ast.ExceptHandler) and node.name is not None:
            defined.add(node.name)
        elif isinstance(node, (ast.comprehension,)):
            defined |= _bound_names(node.target)
    builtins = set(dir(__builtins__)) if isinstance(__builtins__, types.ModuleType) \
        else set(__builtins__)
    free = jx_sorted(jx_difference(
        jx_sorted(loaded - defined - builtins), list(JX_PORTABILITY_BOUNDARY)))
    return {"freeNames": len(free), "names": free}


# =============================================================================
# Section 10.  The candidate's own obligations, and the total boundary.
# =============================================================================

REQUIRED_RESIDUAL_IDS = ("RES-C2V6-01", "RES-C2V6-02", "RES-C2V6-03", "RES-C2V6-04",
                         "RES-C2V6-05", "RES-C2V6-06", "RES-C2V6-07")
REQUIRED_LAYER_IDS = ("L0", "L1", "L2", "L2b", "L2c", "L3", "L4", "L5", "L6", "L6b",
                      "L6c", "L7")
DISCHARGED_FINDING_IDS = ("IR-C2V4-01", "IR-C2V5-01", "IR-C2V5-02", "IR-C2V5-03",
                          "IR-C2V5-04")


def _identity_findings(c) -> list:
    findings = []
    if jx_bind_text(c.get("artifact"), ARTIFACT_ID) is not None:
        findings.append("C2V6: candidate is not " + ARTIFACT_ID)
    if not jx_exact_int(c.get("version"), 6) or not jx_exact_int(c.get("supersedes"), 5):
        findings.append("C2V6: candidate must declare version 6 superseding 5 as JSON "
                        "integers; a float or boolean spelling is refused by the same "
                        "rule this successor exists to enforce")
    status = c.get("status")
    status = status if jx_type(status) == "string" else ""
    if "CANDIDATE-NOT-APPLIED" not in status or "AWAITING-INDEPENDENT-REVIEW" not in status:
        findings.append("C2V6: candidate status must remain CANDIDATE-NOT-APPLIED / "
                        "AWAITING-INDEPENDENT-REVIEW")
    resolves = c.get("resolves")
    resolves = resolves if jx_type(resolves) == "object" else {}
    for finding_id in DISCHARGED_FINDING_IDS:
        if not jx_has(resolves, finding_id):
            findings.append("C2V6: the candidate does not name " + finding_id +
                            ", one of the dispositions it exists to repair")
    return findings


def _inventory_findings(c) -> list:
    """Every guard has a blind spot.  A total-coverage claim is refused."""
    findings = []
    inventory = c.get("guardInventory")
    inventory = inventory if jx_type(inventory) == "object" else {}
    layers = inventory.get("layers")
    layers = layers if jx_type(layers) == "array" else []
    seen = []
    for layer in layers:
        if jx_type(layer) != "object":
            continue
        seen.append(layer.get("id"))
        spots = layer.get("blindSpots")
        if jx_type(spots) != "array" or not spots:
            findings.append("C2V6-INVENTORY: layer " + repr(layer.get("id")) +
                            " publishes no blind spot; a guard inventory claiming total "
                            "coverage is refused")
    if not jx_equal(jx_sorted(jx_unique(seen)), jx_sorted(list(REQUIRED_LAYER_IDS))):
        findings.append("C2V6-INVENTORY: the guard inventory declares layers " +
                        repr(jx_sorted(seen)) + ", not the " +
                        repr(jx_sorted(list(REQUIRED_LAYER_IDS))) + " this checker "
                        "carries")
    behind = inventory.get("whatStandsBehindTheBackstop")
    behind = behind if jx_type(behind) == "string" else ""
    if not jx_int_in_range(len(behind), 80, 10 ** 6):
        findings.append("C2V6-INVENTORY: the inventory does not state what stands behind "
                        "the behavioural backstop, which is the structural question the "
                        "adjudication graded BLOCKING")
    terminal = inventory.get("terminalLayerAndWhatStandsBehindIt")
    terminal = terminal if jx_type(terminal) == "string" else ""
    if "nothing" not in terminal.lower():
        findings.append("C2V6-INVENTORY: the inventory does not state plainly that the "
                        "terminal layer has nothing behind it but independent review")
    return findings


def _residual_findings(c) -> list:
    findings = []
    residuals = c.get("residuals")
    residuals = residuals if jx_type(residuals) == "array" else []
    ids = [item.get("id") for item in residuals if jx_type(item) == "object"]
    missing = jx_sorted(jx_difference(list(REQUIRED_RESIDUAL_IDS), ids))
    if missing:
        findings.append("C2V6-RESIDUAL: the candidate does not retain " + repr(missing) +
                        "; a residual that is absorbed rather than retained is the "
                        "corpus's dominant failure mode")
    for item in residuals:
        if jx_type(item) != "object":
            continue
        status = item.get("status")
        if not jx_in(status, ["RETAINED", "RETAINED-OPEN"]):
            findings.append("C2V6-RESIDUAL: " + repr(item.get("id")) + " is not RETAINED")
        why = item.get("whyNotClosed")
        why = why if jx_type(why) == "string" else ""
        if not jx_int_in_range(len(why), 40, 10 ** 6):
            findings.append("C2V6-RESIDUAL: " + repr(item.get("id")) + " does not say "
                            "why it is not closed")
    return findings


def _recording_findings(c) -> list:
    """Freeze 7.2: filename AND digest for every input.  A count is not a record."""
    findings = []
    recorded = c.get("recordedInputs")
    recorded = recorded if jx_type(recorded) == "array" else []
    names = [item.get("filename") for item in recorded if jx_type(item) == "object"]
    missing = jx_sorted(jx_difference(list(PINS), names))
    if missing:
        findings.append("C2V6-RECORD: " + str(len(missing)) + " pinned input(s) are "
                        "executed or parsed by this checker but carry no record: " +
                        repr(missing))
    for item in recorded:
        if jx_type(item) != "object":
            continue
        name = item.get("filename")
        if jx_has(PINS, name):
            reason = jx_bind_text(item.get("sha256"), jx_get(PINS, name))
            if reason is not None:
                findings.append("C2V6-RECORD: " + str(name) + ": " + reason +
                                "; the recorded digest is not the digest this run "
                                "verified")
        role = item.get("role")
        role = role if jx_type(role) == "string" else ""
        if not jx_int_in_range(len(role), 12, 10 ** 6):
            findings.append("C2V6-RECORD: " + repr(name) + " is recorded without a role, "
                            "so the record does not say what it is depended on for")
    return findings


def _mode_findings(c) -> list:
    findings = []
    mode = c.get("checkerModeContract")
    mode = mode if jx_type(mode) == "object" else {}
    codes = mode.get("exitCodes")
    codes = codes if jx_type(codes) == "object" else {}
    refusal = codes.get("3")
    refusal = refusal if jx_type(refusal) == "string" else ""
    if jx_bind_text(mode.get("checker"), "check-c2-v6.py") is not None or \
            not jx_equal(jx_sorted(list(codes)), jx_sorted(list(DECLARED_EXIT_CODES))) or \
            "REFUSED" not in refusal:
        findings.append("C2V6: the checker mode contract does not declare exactly the "
                        "four exit codes with the last reserved for the dirty-base "
                        "selftest refusal")
    return findings


def _repro_findings(c, authority) -> list:
    """The minimal repros must be RECORDED, and recorded as what they are.

    The enumeration test that produced IR-C2V5-01 lived here.  v5 wrote
    `if not adjudicated <= lines:` -- a set-subset test between a computed
    integer set and a set built from the wire -- and `{2487} <= {2487.0}` is
    True.  Here every line is type-asserted before it is compared, the
    comparison is `jx_subset` over canonical tokens, and a non-integer at any
    of those positions is a named finding rather than a silent admission.
    """
    findings = []
    defect = c.get("theDefect")
    defect = defect if jx_type(defect) == "object" else {}
    repro = defect.get("minimalReproduction")
    repro = repro if jx_type(repro) == "object" else {}
    if jx_bind_text(repro.get("sourceModification"), "NONE") is not None:
        findings.append("C2V6-REPRO: the minimal reproduction is not recorded as "
                        "requiring no source modification, which is the whole reason "
                        "IR-C2V4-01 is BLOCKING rather than advisory")
    if jx_bind_text(repro.get("predecessorSha256"), jx_get(PINS, V4_CHECKER)) is not None:
        findings.append("C2V6-REPRO: the reproduction is recorded against " +
                        repr(repro.get("predecessorSha256")) + ", not the verified "
                        "predecessor digest " + jx_get(PINS, V4_CHECKER))
    sites = defect.get("repairedComparisonSites")
    sites = sites if jx_type(sites) == "array" else []
    lines = []
    for index, site in enumerate(sites):
        value = site.get("line") if jx_type(site) == "object" else None
        if not jx_int(value):
            findings.append(
                "C2V6-TYPE: theDefect/repairedComparisonSites/" + str(index) +
                "/line is published as " + repr(value) + ", whose JSON type is " +
                jx_type(value) + ", not the JSON integer the pinned adjudication names; "
                "this is the exact position and the exact spelling of IR-C2V5-01, where "
                "a set-subset test admitted it with one JSON edit and no source change")
            continue
        lines.append(value)
    adjudicated = adjudicated_census_lines(authority)
    if not jx_subset(adjudicated, lines):
        findings.append("C2V6-REPRO: the candidate enumerates comparison sites " +
                        repr(jx_sorted(lines)) + " but the pinned adjudication names " +
                        repr(jx_sorted(adjudicated)))
    successor = c.get("theSuccessorDefect")
    successor = successor if jx_type(successor) == "object" else {}
    vectors = successor.get("vectors")
    vectors = vectors if jx_type(vectors) == "array" else []
    declared = [item.get("id") for item in vectors if jx_type(item) == "object"]
    expected = [vector for vector, _a, _b, _c, _d in SUCCESSOR_DIFFERENTIAL_VECTORS]
    if not jx_equal(jx_sorted(jx_unique(declared)), jx_sorted(jx_unique(expected))):
        findings.append("C2V6-REPRO: the candidate records successor false-accept "
                        "vectors " + repr(jx_sorted(declared)) + " but this run executes "
                        + repr(jx_sorted(expected)) + "; a retained vector that is not "
                        "executed is prose")
    return findings


def candidate_probe_findings(candidate, authority) -> list:
    """The binding comparison alone, for L6c's successor vectors."""
    bindings, _problems = candidate_bindings(
        candidate, authority.partial_live, authority, authority.base,
        authority.measurement)
    findings = []
    for record in jx_sorted_by(bindings, "steps"):
        try:
            published = _resolve_steps(candidate, record["steps"])
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        reason = jx_bind(published, record["expected"])
        if reason is not None:
            prefix = "C2V6-TYPE" if not jx_int(published) else "C2V6-CANDIDATE"
            findings.append(prefix + ": " + _steps_text(record["steps"]) + ": " + reason)
    return findings


def differential_findings(authority) -> list:
    result = authority.differential
    findings = ["C2V6-DIFFERENTIAL: " + item for item in result["escapes"]]
    if jx_bind(result["successorRejectedByName"], result["vectors"]) is not None:
        findings.append("C2V6-DIFFERENTIAL: " + str(result["successorRejectedByName"]) +
                        " of " + str(result["vectors"]) + " retained false-accept "
                        "vectors were rejected by name")
    if not jx_int_in_range(result["predecessorAdmittedThePosition"], 1, 10 ** 6):
        findings.append("C2V6-DIFFERENTIAL: the pinned predecessor named every vector "
                        "position, so the differential is vacuous; either the "
                        "predecessor's bytes are not the adjudicated ones or this layer "
                        "has stopped measuring anything")
    if not jx_int_in_range(result["predecessorFullyGreenRuns"], 1, 10 ** 6):
        findings.append("C2V6-DIFFERENTIAL: no retained vector reproduces the "
                        "adjudication's headline - a fully green predecessor run over a "
                        "defective document - so the repair is no longer demonstrably "
                        "load-bearing")
    successor = authority.successor
    findings.extend("C2V6-SUCCESSOR: " + item for item in successor["escapes"])
    if jx_bind(successor["v6RejectedByName"], successor["vectors"]) is not None:
        findings.append("C2V6-SUCCESSOR: " + str(successor["v6RejectedByName"]) + " of " +
                        str(successor["vectors"]) + " blocking vectors from the pinned "
                        "v5 REJECT were named by this checker at the analogous position "
                        "of its own document")
    if not jx_int_in_range(successor["v5AdmittedToAFullGreenRun"], 1, 10 ** 6):
        findings.append("C2V6-SUCCESSOR: the pinned check-c2-v5.py admits none of its "
                        "own blocking vectors to a fully green run, so the differential "
                        "this repair is measured against has collapsed and the repair is "
                        "no longer demonstrably load-bearing")
    return findings


_EMPTY_SUCCESSOR = {"vectors": 0, "rows": [], "v5AdmittedToAFullGreenRun": 0,
                    "v6RejectedByName": 0, "escapes": []}


def _banner_register(live, document_name, own_digest) -> dict:
    """The register the banner renders from: every measured number, plus the two
    STRING labels.  Built through the primitive so no key can collide with
    another under host-language equality."""
    out = {}
    for key in jx_sorted(list(live)):
        jx_put(out, key, jx_get(live, key))
    jx_put(out, "documentName", document_name)
    jx_put(out, "ownDigest", own_digest)
    return out


_EMPTY_PRIMITIVE = {
    "corpusValues": 0, "corpusPairs": 0, "roundTrips": 0, "distinctTokens": 0,
    "tokenCollisions": 0, "stricterThanHostEquality": 0, "looserThanHostEquality": 0,
    "agreeWithHostEquality": 0, "reflexiveFailures": 0, "crossTypeAdmissions": 0,
    "gateCases": 0, "gateAdmissions": 0, "operatorSpaceRows": 0,
    "operatorSpaceHazardsReproduced": 0, "operatorSpaceRowsCovered": 0,
    "entryPointCases": 0, "entryPointFailures": 0, "domainRefusals": 0, "escapes": [],
}


def _safe_jx_selftest() -> dict:
    """Total.  A primitive broken badly enough to raise must still be REPORTED by
    the layer that owns it, not crash the traversal into a generic finding."""
    try:
        result = jx_selftest()
    except BaseException as exc:                        # noqa: BLE001 - measured
        result = dict(_EMPTY_PRIMITIVE)
        result["escapes"] = ["the primitive's own exhaustive test raised " +
                             type(exc).__name__ + ": " + str(exc) + "; the single "
                             "decision point every other layer is built on does not run"]
        return result
    for key in _EMPTY_PRIMITIVE:
        if key not in result:
            result[key] = _EMPTY_PRIMITIVE[key]
            result["escapes"] = list(result["escapes"]) + [
                "the primitive's own exhaustive test no longer reports " + key]
    return result


def check(c, authority, self_tree=None) -> list:
    """Total boundary: malformed parsed JSON becomes a named finding."""
    if jx_type(c) != "object" or not c:
        return ["C2V6-TOTALITY-ROOT: contract root must be a non-empty JSON object"]
    try:
        return _check(c, authority, self_tree)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        primitive = _safe_jx_selftest()
        prefix = ["C2V6-PRIMITIVE: " + item for item in primitive["escapes"]]
        if not prefix and jx_bind(primitive["entryPointFailures"], 0) is not None:
            prefix = ["C2V6-PRIMITIVE: " + str(primitive["entryPointFailures"]) +
                      " entry point(s) of the primitive no longer differ from the "
                      "host-language operation they replace"]
        return prefix + ["C2V6-TOTALITY: the candidate could not be traversed (" +
                         type(exc).__name__ + ": " + str(exc) + ")"]


def _check(c, authority, self_tree=None) -> list:
    tree = own_tree() if self_tree is None else self_tree
    findings = []
    # The primitive is the foundation every other layer stands on, so its own
    # exhaustive test runs FIRST and is total.  If it were run late, a break in
    # jx_canon would crash the traversal into a generic totality finding before
    # the layer that owns the primitive ever reported -- which is a fail-closed
    # exit, but it is not evidence that the guard fired.
    authority.primitive = _safe_jx_selftest()
    findings.extend(_identity_findings(c))

    derived = c.get("derivedFrom")
    derived = derived if jx_type(derived) == "object" else {}
    if jx_bind_text(derived.get("artifact"), V4_CONTRACT) is not None or \
            jx_bind_text(derived.get("sha256"), jx_get(PINS, V4_CONTRACT)) is not None:
        return findings + [
            "C2V6-DERIVATION: the candidate must derive from " + V4_CONTRACT + " at " +
            jx_get(PINS, V4_CONTRACT) + "; it names " + repr(derived.get("artifact")) +
            " at " + repr(derived.get("sha256")) + ", so no effective contract can be "
            "materialised"]

    base = copy.deepcopy(authority.json(V4_CONTRACT))
    effective, derivation_findings = apply_derivation(base, derived.get("operations"))
    findings.extend(derivation_findings)
    authority.effective = effective
    authority.base = base

    projection, projection_findings = project_to_v4_identity(
        effective, c.get("v4InheritanceProjection"))
    findings.extend(projection_findings)

    # ---- L1 inherited: the reviewed predecessor over the projection ----------
    inherited_key = "inherited/" + hashlib.sha256(
        jx_canon(projection).encode("utf-8")).hexdigest()
    inherited = jx_get(authority.pinned, inherited_key)
    if inherited is None:
        try:
            inherited = [str(item) for item in authority.v4.check(
                copy.deepcopy(projection), authority.v4_authority)]
        except BaseException as exc:                    # noqa: BLE001 - reported
            inherited = ["the pinned predecessor raised " + type(exc).__name__ + ": " +
                         str(exc)]
        jx_put(authority.pinned, inherited_key, inherited)
    findings.extend("C2V6-INHERITED: " + str(item) for item in inherited)

    # ---- the measurement, then L2 / L2b / L3 --------------------------------
    measurement = measure(effective, authority)
    authority.measurement = measurement
    findings.extend(census_comparison_findings(effective, measurement))
    findings.extend(register_findings(effective, measurement, authority))
    findings.extend(document_type_lock_findings(base, effective, authority))

    # ---- L4, L5, L6, L6b ----------------------------------------------------
    findings.extend(scan_findings(authority, tree))
    findings.extend(behavioural_findings(effective, measurement, authority, tree))
    findings.extend(sweep_findings(authority))
    authority.differential = predecessor_differential(authority)
    authority.portability = jx_portability_findings(own_source())
    for name in authority.portability["names"]:
        findings.append("C2V6-PRIMITIVE: the primitive block references " + name +
                        " from outside its declared portability boundary, so the claim "
                        "that another checker can adopt it unchanged is false")
    probe = jx_portability_findings(PORTABILITY_DETECTOR_PROBE.encode("utf-8"))
    if not jx_int_in_range(probe["freeNames"], 1, 10 ** 6):
        findings.append(
            "C2V6-PRIMITIVE: the portability detector reports a block that plainly "
            "references a name from outside itself as self-contained, so the measured "
            "claim that another checker can adopt this primitive unchanged is a "
            "statement about an instrument that detects nothing")

    # ---- L6c needs a register; the successor figures are the only part of it
    # that depends on L6c, so the partial register is built first and the two
    # are never allowed to define each other.
    authority.successor = _EMPTY_SUCCESSOR
    authority.candidate_lock = {"boundLeaves": 0, "executedCases": 0,
                                "namedRejections": 0, "controls": 0, "admissions": 0,
                                "escapes": []}
    authority.partial_live = live_register(authority)
    authority.successor = successor_differential(authority, c)
    findings.extend(differential_findings(authority))

    # ---- L2c: the candidate's own integer leaves ----------------------------
    # Pass one populates authority.candidate_lock; pass two reports against a
    # register that already carries it.  The probe's counts are a function of the
    # bound leaf SET and not of any published value, so the two passes agree --
    # and if they ever stop agreeing, pass two's findings say so by name.
    candidate_lock_findings(c, live_register(authority), authority, base, measurement)
    live = live_register(authority)
    findings.extend(candidate_lock_findings(c, live, authority, base, measurement))
    authority.live = live_register(authority)
    live = authority.live
    runtime = {"sweepElapsedSeconds": authority.sweep["elapsedSeconds"]}
    labelled = _banner_register(live, authority.document_name,
                                hashlib.sha256(own_source()).hexdigest())
    banner_problems = banner_findings(labelled, runtime)
    findings.extend(banner_problems)
    if not banner_problems:
        authority.banner = render_banner(BANNER_TEMPLATES, labelled, runtime)

    # ---- the candidate's own obligations ------------------------------------
    findings.extend(_repro_findings(c, authority))
    findings.extend(_inventory_findings(c))
    findings.extend(_residual_findings(c))
    findings.extend(_recording_findings(c))
    findings.extend(_mode_findings(c))
    return findings


# =============================================================================
# Section 11.  L7 -- self-mutation.  Break each gate and each layer, require
# detection BY THE LAYER IT BREAKS, and then prove that republishing every
# counter cannot hide the break.
#
# This is the repair for IR-C2V5-02 and IR-C2V5-04 and for the reviewer's ruling
# on the self-binding: SOUND AS A BINDING, UNSOUND AS A GUARD.  In v5 three of
# the five declared gates could be stripped with ZERO findings, and two genuine
# layer breaks were caught ONLY by a drift on a self-published counter -- so
# republishing that counter, which the design's own cost model instructs the
# maintainer to do, converted the catch into silence.
#
# Two rules follow and both are enforced here for EVERY source row:
#   1. every declared gate is broken, and
#   2. every break is re-run against a candidate whose every bound integer leaf
#      has been REPUBLISHED from the mutant's own live measurements.  The named
#      finding must fire in BOTH runs.  A row whose finding survives only the
#      first run is reported as COUNTER-ONLY and fails the suite.
#
# Nothing stands behind this layer but independent review.  It is terminal by
# construction and every row is printed so a reviewer can be that thing.
# =============================================================================

def _replace_body(tree, name, source):
    subject = copy.deepcopy(tree)
    replacement = ast.parse(source).body
    for node in ast.walk(subject):
        if isinstance(node, ast.FunctionDef) and jx_equal(node.name, name):
            node.body = replacement
            return ast.fix_missing_locations(subject)
    raise AuthorityLoadError("cannot find " + str(name) + " to mutate")


def _execute_tree(tree):
    module = types.ModuleType("opensip_c2v6_mutated")
    module.__file__ = str(pathlib.Path(__file__).resolve())
    exec(compile(tree, module.__file__, "exec"), module.__dict__)
    return module


# (name, function, replacement body, expected finding id, subject substring)
# Every one of the declared gates appears here.  v5 declared this debt in L4's
# blindSpots and paid two fifths of it; this table pays all of it.
_GATE_MUTATIONS = (
    ("a JSON boolean counts as a JSON integer (LB-C2-01 at the root)", "jx_type",
     "if value is None:\n    return 'null'\n"
     "if type(value) is int or value is True or value is False:\n    return 'integer'\n"
     "if type(value) is float:\n    return 'number'\n"
     "if type(value) is str:\n    return 'string'\n"
     "if type(value) is list:\n    return 'array'\n"
     "if type(value) is dict:\n    return 'object'\n"
     "return JX_UNSUPPORTED", "C2V6-PRIMITIVE", ""),
    ("drop the type tag from the canonical encoding", "jx_canon",
     "return str(value)", "C2V6-PRIMITIVE", ""),
    ("drop the length framing that makes the encoding decodable", "jx_frame",
     "return tag + payload", "C2V6-PRIMITIVE", ""),
    ("compare canonical tokens with host equality instead of string equality",
     "jx_equal", "return a == b", "C2V6-PRIMITIVE", ""),
    ("invert equality with the host operator", "jx_ne", "return a != b",
     "C2V6-PRIMITIVE", "jx_ne"),
    ("let the canonical encoding stop being invertible", "jx_decanon",
     "return None", "C2V6-PRIMITIVE", "round trip"),
    ("admit every value into the JSON domain", "jx_in_domain", "return True",
     "C2V6-PRIMITIVE", "jx_in_domain"),
    ("hash a raw value instead of its canonical token", "jx_key",
     "return str(value)", "C2V6-PRIMITIVE", ""),
    ("let isinstance decide integerhood (True is an int)", "jx_int",
     "return isinstance(value, int)", "C2V6-PRIMITIVE", ""),
    ("strip the type gate from the integer CONSTANT guard", "jx_exact_int",
     "return value == constant", "C2V6-PRIMITIVE", "jx_exact_int"),
    ("strip the type gate from the integer RANGE guard", "jx_int_in_range",
     "return low <= value <= high", "C2V6-PRIMITIVE", "jx_int_in_range"),
    ("let two different JSON types count as the same type", "jx_same_type",
     "return True", "C2V6-PRIMITIVE", ""),
    ("restore the predecessor's ungated published-counter comparison", "jx_bind",
     "return None if published == measured else 'drift'", "C2V6-PRIMITIVE", "jx_bind"),
    ("gate only the wire side of the binding and trust the computed side", "jx_bind",
     "if not jx_int(published):\n    return 'type'\n"
     "return None if published == measured else 'drift'",
     "C2V6-BEHAVIOUR", "computed side"),
    ("compare published strings with host equality", "jx_bind_text",
     "return None", "C2V6-PRIMITIVE", "jx_bind_text"),
    ("use host membership instead of canonical membership", "jx_in",
     "return needle in list(haystack)", "C2V6-PRIMITIVE", ""),
    ("invert membership with the host operator", "jx_not_in",
     "return needle not in list(haystack)", "C2V6-PRIMITIVE", ""),
    ("restore the IR-C2V5-01 subset test verbatim", "jx_subset",
     "return set(left) <= set(right)", "C2V6-PRIMITIVE", ""),
    ("restore the host superset test", "jx_superset",
     "return set(left) >= set(right)", "C2V6-PRIMITIVE", ""),
    ("restore the host disjointness test", "jx_disjoint",
     "return set(left).isdisjoint(set(right))", "C2V6-PRIMITIVE", ""),
    ("restore host set difference", "jx_difference",
     "return list(set(left) - set(right))", "C2V6-PRIMITIVE", ""),
    ("let set() dedup collapse 1, 1.0 and True", "jx_unique",
     "return list(dict.fromkeys(values))", "C2V6-PRIMITIVE", ""),
    ("build a hashed key set out of raw values", "jx_keyset",
     "return set(values)", "C2V6-PRIMITIVE", ""),
    ("use host counting", "jx_count", "return list(values).count(needle)",
     "C2V6-PRIMITIVE", "jx_count"),
    ("use host index lookup", "jx_index",
     "return list(values).index(needle) if needle in list(values) else None",
     "C2V6-PRIMITIVE", "jx_index"),
    ("use host key membership", "jx_has", "return key in mapping",
     "C2V6-PRIMITIVE", "jx_has"),
    ("use host key lookup", "jx_get", "return mapping.get(key, default)",
     "C2V6-PRIMITIVE", "jx_get"),
    ("use host lookup for the total accessor", "jx_at",
     "try:\n    return container[key]\nexcept Exception:\n    return default",
     "C2V6-PRIMITIVE", "jx_at"),
    ("use host membership for the total accessor", "jx_has_at",
     "return key in container", "C2V6-PRIMITIVE", ""),
    ("use host assignment for the total mutator", "jx_put",
     "container[key] = value\nreturn True", "C2V6-PRIMITIVE", ""),
    ("order two different JSON types against each other", "jx_order",
     "return 0 if a == b else (-1 if a < b else 1)", "C2V6-PRIMITIVE", ""),
    ("restore the host ordering operators", "jx_le", "return a <= b",
     "C2V6-PRIMITIVE", "jx_le"),
    ("restore the host strict ordering operator", "jx_lt", "return a < b",
     "C2V6-PRIMITIVE", "jx_lt"),
    ("restore the host reverse ordering operator", "jx_ge", "return a >= b",
     "C2V6-PRIMITIVE", "jx_ge"),
    ("restore the host strict reverse ordering operator", "jx_gt", "return a > b",
     "C2V6-PRIMITIVE", "jx_gt"),
    ("sort by raw value instead of canonical token", "jx_sorted",
     "return sorted(values, key=repr)", "C2V6-PRIMITIVE", ""),
    ("sort records by raw field value", "jx_sorted_by",
     "return sorted(records, key=lambda record: repr(record))", "C2V6-PRIMITIVE", ""),
    ("order a heterogeneous JSON type set instead of refusing it",
     "jx_sorted_homogeneous", "return list(values), None", "C2V6-PRIMITIVE", ""),
    ("let a float element into an integer summation", "jx_sum_int",
     "return sum(values), None", "C2V6-PRIMITIVE", ""),
    ("let a non-string into a string set", "jx_string_set",
     "return set(values), None", "C2V6-PRIMITIVE", ""),
    ("admit a non-finite float as a finite number", "jx_finite_number",
     "return jx_type(value) == 'number'", "C2V6-PRIMITIVE", ""),
)

# Every row that expects the primitive's own layer asserts on the NAME OF THE
# GATE IT BREAKS, not merely on the finding id.  v5's suite was measured to
# assert on a bare id for 25 of its 38 rows and on nothing at all for 3, and a
# rejection that does not name the position under test is the trap the
# adjudication records.  The transformation is explicit so a reviewer can see
# that no row is exempt.
GATE_MUTATIONS = tuple(
    (name, function, body, expected,
     function if expected == "C2V6-PRIMITIVE" and not subject else subject)
    for name, function, body, expected, subject in _GATE_MUTATIONS)


# (name, function, replacement body, expected finding id, subject substring,
#  clears the pinned-sweep cache)
LAYER_MUTATIONS = (
    ("narrow the numeric model back to ast.Constant (IR-C2V4-01's root cause)",
     "_provably_non_numeric", "return not isinstance(node, ast.Constant)",
     "C2V6-SCAN-BLIND", "2487", False),
    ("launder comprehension results the way v5 did (IR-C2V5-01's root cause)",
     "_is_wire",
     "if node is None:\n    return False\n"
     "if isinstance(node, ast.Subscript):\n"
     "    return not (isinstance(node.value, ast.Name) and node.value.id in literals)\n"
     "if isinstance(node, ast.Attribute):\n"
     "    return _is_wire(node.value, tainted, literals)\n"
     "return isinstance(node, ast.Name) and node.id in tainted",
     "C2V6-SCAN-BLIND", str(V5_DEFECT_LINE), False),
    ("stop the scan seeing the whole function universe", "_function_universe",
     "return [node for node in tree.body if isinstance(node, ast.FunctionDef)]",
     "C2V6-SCAN-BLIND", "function-like node", False),
    ("excuse every comparison by textual gate dominance", "_gate_dominates",
     "return True", "C2V6-SCAN-BLIND", "adjudicated census comparison", False),
    ("erase the adjudicated line numbers the scan must be shown to see",
     "adjudicated_census_lines", "return []", "C2V6-SCAN-BLIND", "vacuous", False),
    ("stop deriving the register from the live measurement", "measured_positions",
     "return {}", "C2V6-REGISTER", "not reached by the measurement", False),
    ("disable the behavioural layer", "behavioural_layer",
     "return {'positions': 0, 'spellings': 0, 'executedCases': 0, "
     "'namedTypeRejections': 0, 'admissions': 0, "
     "'rejectedWithoutNamingThePosition': 0, 'instrumentProbes': 0, "
     "'instrumentProbesNamed': 0, 'instrumentProbesEscaped': 0, 'escapes': []}",
     "C2V6-BEHAVIOUR", "executed no case", False),
    ("confine the document lock to the census block", "locked_integer_leaves",
     "return []", "C2V6-DOCLOCK", "outside the lock", False),
    ("lock only the base direction, so a derived leaf escapes",
     "locked_integer_leaves", "return jx_sorted(jx_unique(_integer_leaf_steps(base)))",
     "C2V6-DOCLOCK", "outside the lock", False),
    ("probe only the first leaf of the document lock", "document_type_probe",
     "return {'lockedLeaves': len(locked), 'executedCases': 0, "
     "'namedTypeRejections': 0, 'admissions': 0, 'escapes': []}",
     "C2V6-DOCLOCK", "probed no position", False),
    ("stop binding the candidate's own integer leaves", "candidate_bindings",
     "return [], []", "C2V6-UNBOUND", "no layer of this run binds", False),
    ("stop probing the candidate's own integer leaves", "candidate_type_probe",
     "return {'boundLeaves': len(bindings), 'executedCases': 0, "
     "'namedRejections': 0, 'controls': 0, 'admissions': 0, 'escapes': []}",
     "C2V6-CANDLOCK", "probed no position", False),
    ("let the candidate binding table be narrowed silently", "_effective_expected",
     "return None, 'unmeasured'", "C2V6-UNBOUND", "the derivation writes a JSON integer",
     False),
    ("hollow out the whole-document sweep", "predecessor_sweep",
     "return {'integerLeavesInjected': 0, 'admittedToAFullGreenRun': 0, "
     "'rejectedByPredecessor': 0, 'admittedCensusCounters': 0, "
     "'admittedOutsideTheCensusBlock': 0, 'admittedPaths': [], 'outsidePaths': [], "
     "'elapsedSeconds': 0}", "C2V6-SWEEP", "integer leaves injected", True),
    ("sweep only the census block, as a scoped repair would",
     "predecessor_sweep",
     "authority.pinned.clear()\n"
     "result = {'integerLeavesInjected': 0, 'admittedToAFullGreenRun': 0, "
     "'rejectedByPredecessor': 0, 'admittedCensusCounters': 0, "
     "'admittedOutsideTheCensusBlock': 0, 'admittedPaths': [], 'outsidePaths': []," 
     "'elapsedSeconds': 0}\nreturn result", "C2V6-SWEEP", "integer leaves", True),
    ("stop enumerating the candidate's integer leaves", "_integer_leaf_steps",
     "return []", "C2V6-SWEEP", "OUTSIDE the census block", True),
    ("bake the banner figures back into source text", "banner_digit_tokens",
     "return []", "C2V6-BANNER", "detects nothing", False),
    ("stop the banner interpolating the register at all",
     "render_banner", "return list(templates)", "C2V6-BANNER", "uninterpolated", False),
    ("stop probing the honesty of L4's `-> str` proofs", "str_proof_probe",
     "return {'declared': 0, 'probed': 0, 'executedCases': 0, 'failures': 0, "
     "'escapes': []}", "C2V6-PROOF", "were not exercised", False),
    ("stop probing the honesty of L4's AST-STR-FIELD proof", "ast_field_probe",
     "return {'executedCases': 0, 'failures': 0, 'escapes': []}",
     "C2V6-PROOF", "were not exercised", False),
    ("declare the primitive self-contained without measuring it",
     "jx_portability_findings", "return {'freeNames': 0, 'names': []}",
     "C2V6-PRIMITIVE", "detects nothing", False),
    ("stop executing the primitive's own exhaustive test", "jx_selftest",
     "return {'corpusValues': 0, 'corpusPairs': 0, 'roundTrips': 0, "
     "'distinctTokens': 0, 'tokenCollisions': 0, 'stricterThanHostEquality': 0, "
     "'looserThanHostEquality': 0, 'agreeWithHostEquality': 0, "
     "'reflexiveFailures': 0, 'crossTypeAdmissions': 0, 'gateCases': 0, "
     "'gateAdmissions': 0, 'operatorSpaceRows': 0, "
     "'operatorSpaceHazardsReproduced': 0, 'operatorSpaceRowsCovered': 0, "
     "'domainRefusals': 0, 'entryPointCases': 0, 'entryPointFailures': 0, "
     "'escapes': []}", "C2V6-PRIMITIVE", "empty set", False),
    ("collapse the differential against the pinned v5 REJECT", "_v5_admissions",
     "return []", "C2V6-SUCCESSOR", "collapsed", True),
    ("stop measuring the census comparison sites", "census_site_positions",
     "return {}", "C2V6-REGISTER", "partition", False),
)

SOURCE_MUTATIONS = tuple(
    (name, function, body, expected, subject, False)
    for name, function, body, expected, subject in GATE_MUTATIONS) + LAYER_MUTATIONS


def _m_unregister_a_census_position(c):
    for op in c["derivedFrom"]["operations"]:
        if jx_equal(op.get("path"), "planIntent.integerConstantRegisterV6"):
            op["value"]["censusCounterPositions"].pop()
            return
    raise AuthorityLoadError("cannot find the register operation to mutate")


def _m_overstate_the_register(c):
    for op in c["derivedFrom"]["operations"]:
        if jx_equal(op.get("path"), "planIntent.integerConstantRegisterV6"):
            op["value"]["censusCounterPositions"].append("surfaces[imaginary].nothing")
            return
    raise AuthorityLoadError("cannot find the register operation to mutate")


def _census_counter_op(c, key):
    for op in c["derivedFrom"]["operations"]:
        if jx_equal(op.get("path"), "hostileScalarLeafTotality.contractRoot." + key):
            return op
    raise AuthorityLoadError("cannot find the contractRoot." + key + " operation")


def _m_float_census_counter(c):
    op = _census_counter_op(c, "scalarLeafPaths")
    op["value"] = float(op["value"])


def _m_boolean_census_counter(c):
    _census_counter_op(c, "pathsNotRoundTripping")["value"] = False


def _m_string_census_counter(c):
    op = _census_counter_op(c, "enumeratedPaths")
    op["value"] = str(op["value"])


def _m_drift_census_counter(c):
    op = _census_counter_op(c, "executedCases")
    op["value"] = op["value"] + 1


def _m_widen_the_projection(c):
    c["v4InheritanceProjection"]["fields"]["planIntent.integerConstantRegisterV6"] = None


def _m_misdescribe_the_derivation(c):
    for op in c["derivedFrom"]["operations"]:
        if jx_equal(op.get("op"), "set") and jx_has(op, "from"):
            op["from"] = "a byte the predecessor does not hold"
            return
    raise AuthorityLoadError("cannot find a set operation to mutate")


def _m_claim_total_coverage(c):
    for layer in c["guardInventory"]["layers"]:
        layer["blindSpots"] = []


def _m_absorb_a_residual(c):
    c["residuals"] = [item for item in c["residuals"]
                      if not jx_equal(item.get("id"), "RES-C2V6-03")]


def _m_drop_an_input_record(c):
    c["recordedInputs"] = [item for item in c["recordedInputs"]
                           if not jx_equal(item.get("filename"), V4_CHECKER)]


def _m_float_the_repro_line(c):
    """IR-C2V5-01, verbatim: ONE JSON edit, the float spelling of a line number."""
    site = c["theDefect"]["repairedComparisonSites"][0]
    site["line"] = float(site["line"])


def _m_drift_the_repro_line(c):
    site = c["theDefect"]["repairedComparisonSites"][0]
    site["line"] = site["line"] + 1


def _m_float_a_sweep_figure(c):
    sweep = c["theDefect"]["wholeDocumentSweep"]
    sweep["admittedByPredecessorToAFullGreenRun"] = float(
        sweep["admittedByPredecessorToAFullGreenRun"])


def _m_republish_a_sweep_figure(c):
    """The reviewer's own probe: republish the headline sweep figure as one."""
    c["theDefect"]["wholeDocumentSweep"]["integerLeavesInjected"] = 1


def _m_boolean_the_false_accept_counter(c):
    """The FA-2 spelling at the block literally named measuredThisRun."""
    c["retainedFalseAcceptVectors"]["measuredThisRun"]["predecessorFullyGreenRuns"] = True


def _m_drift_the_false_accept_counter(c):
    c["retainedFalseAcceptVectors"]["measuredThisRun"]["successorRejectedByName"] = 0


def _m_understate_a_v6_counter(c):
    c["v6MeasuredCounters"]["behaviouralExecutedCases"] = 1


def _m_float_a_v6_counter(c):
    counters = c["v6MeasuredCounters"]
    counters["registeredCensusPositions"] = float(counters["registeredCensusPositions"])


def _m_publish_an_unmeasured_counter(c):
    c["v6MeasuredCounters"]["counterNobodyMeasures"] = 7


def _m_soften_the_repro(c):
    c["theDefect"]["minimalReproduction"]["sourceModification"] = "a small patch"


def _m_drop_a_successor_vector(c):
    c["theSuccessorDefect"]["vectors"] = c["theSuccessorDefect"]["vectors"][:1]


def _m_float_a_site_read_count(c):
    site = c["theDefect"]["repairedComparisonSites"][0]
    site["wireIntegerPositionsRead"] = float(site["wireIntegerPositionsRead"])


CONTRACT_MUTATIONS = (
    ("unregister one census counter position", _m_unregister_a_census_position,
     "C2V6-REGISTER", "not registered"),
    ("register a position the measurement does not reach", _m_overstate_the_register,
     "C2V6-REGISTER", "imaginary"),
    ("spell a census counter as a JSON float (the v4 minimal repro)",
     _m_float_census_counter, "C2V6-TYPE", "contractRoot.scalarLeafPaths"),
    ("spell a census counter as a JSON boolean", _m_boolean_census_counter,
     "C2V6-TYPE", "contractRoot.pathsNotRoundTripping"),
    ("spell a census counter as a JSON string", _m_string_census_counter,
     "C2V6-TYPE", "contractRoot.enumeratedPaths"),
    ("drift a census counter by one", _m_drift_census_counter,
     "C2V6-CENSUS", "contractRoot.executedCases"),
    ("widen the inherited-oracle projection beyond the identity fields",
     _m_widen_the_projection, "C2V6-PROJECTION", "integerConstantRegisterV6"),
    ("misdescribe the bytes the derivation is applied to", _m_misdescribe_the_derivation,
     "C2V6-DERIVATION", "verified predecessor holds"),
    ("claim total guard coverage", _m_claim_total_coverage, "C2V6-INVENTORY",
     "blind spot"),
    ("absorb a retained residual", _m_absorb_a_residual, "C2V6-RESIDUAL",
     "RES-C2V6-03"),
    ("drop the record of an executed input", _m_drop_an_input_record, "C2V6-RECORD",
     V4_CHECKER),
    ("spell an adjudicated comparison line as a float (IR-C2V5-01 verbatim)",
     _m_float_the_repro_line, "C2V6-TYPE",
     "theDefect/repairedComparisonSites/0/line"),
    ("drift an adjudicated comparison line by one", _m_drift_the_repro_line,
     "C2V6-CANDIDATE", "theDefect/repairedComparisonSites/0/line"),
    ("spell a per-site read count as a float", _m_float_a_site_read_count,
     "C2V6-TYPE", "wireIntegerPositionsRead"),
    ("spell a whole-document sweep figure as a float", _m_float_a_sweep_figure,
     "C2V6-TYPE", "admittedByPredecessorToAFullGreenRun"),
    ("republish the headline sweep figure as one (the reviewer's own probe)",
     _m_republish_a_sweep_figure, "C2V6-CANDIDATE", "integerLeavesInjected"),
    ("spell the measured false-accept counter as a JSON boolean (the FA-2 spelling)",
     _m_boolean_the_false_accept_counter, "C2V6-TYPE",
     "retainedFalseAcceptVectors/measuredThisRun/predecessorFullyGreenRuns"),
    ("drift the measured false-accept counter to zero",
     _m_drift_the_false_accept_counter, "C2V6-CANDIDATE",
     "retainedFalseAcceptVectors/measuredThisRun/successorRejectedByName"),
    ("understate one of this checker's own published counters",
     _m_understate_a_v6_counter, "C2V6-CANDIDATE", "behaviouralExecutedCases"),
    ("spell one of this checker's own published counters as a float",
     _m_float_a_v6_counter, "C2V6-TYPE", "registeredCensusPositions"),
    ("publish a counter this run does not measure", _m_publish_an_unmeasured_counter,
     "C2V6-UNBOUND", "counterNobodyMeasures"),
    ("soften the recorded minimal reproduction", _m_soften_the_repro, "C2V6-REPRO",
     "no source modification"),
    ("stop retaining one of the v5 blocking vectors", _m_drop_a_successor_vector,
     "C2V6-REPRO", "IR-C2V5"),
)


def _s_inject_computed_operand_comparison(tree):
    """A wire value against a COMPUTED int -- the shape v4 missed."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_computed_probe(row, measured):\n"
        "    for _k, _v in measured.items():\n"
        "        if row.get(_k) != _v:\n"
        "            return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_comprehension_subset(tree):
    """IR-C2V5-01's exact shape: a set comprehension result meeting a computed
    set through `<=`.  v5's scan classified BOTH operands of this as non-wire."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_subset_probe(sites, authority):\n"
        "    lines = {item.get('line') for item in sites}\n"
        "    adjudicated = adjudicated_census_lines(authority)\n"
        "    if not set(adjudicated) <= lines:\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_operator_call(tree):
    """`operator.ne` is an ast.Call and never an ast.Compare."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_operator_probe(row, measured):\n"
        "    if ne(row.get('schemaVersion'), measured):\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_dict_key_lookup(tree):
    """`1 in {1.0: x}` is True: the hashes agree."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_keylookup_probe(row, table):\n"
        "    if table[row.get('schemaVersion')]:\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_dedup_cardinality(tree):
    """`len({1, 1.0, True})` is 1: three JSON values become one measurement."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_dedup_probe(rows):\n"
        "    seen = set(row.get('count') for row in rows)\n"
        "    return list(seen)\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_named_constant_comparison(tree):
    """A wire value against a module-level named integer, not a literal."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "_LAW18_PROBE = 1\n"
        "def _c2v6_named_constant_probe(row):\n"
        "    if row.get('schemaVersion') != _LAW18_PROBE:\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_membership_comparison(tree):
    """`not in (1,)` -- membership in a numeric literal container."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_membership_probe(row):\n"
        "    if row.get('schemaVersion') not in (1,):\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_sorted_launder(tree):
    """`max` over a mixed set returns whichever the host language reached first."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v6_sorted_probe(rows):\n"
        "    return max(row.get('count') for row in rows)\n").body)
    return ast.fix_missing_locations(subject)


# Each scan row names the function it injects, so the assertion is on a specific
# finding id AND on the position under test.  v5's three scan rows carried no
# expected id at all and asserted only that a count rose.
SCAN_MUTATIONS = (
    ("inject a wire value compared against a COMPUTED integer",
     _s_inject_computed_operand_comparison, "C2V6-SCAN", "_c2v6_computed_probe"),
    ("inject IR-C2V5-01's comprehension-result subset test verbatim",
     _s_inject_comprehension_subset, "C2V6-SCAN", "_c2v6_subset_probe"),
    ("inject an operator.ne call, which is never an ast.Compare",
     _s_inject_operator_call, "C2V6-SCAN", "_c2v6_operator_probe"),
    ("inject a dict key lookup on a wire key", _s_inject_dict_key_lookup,
     "C2V6-SCAN", "_c2v6_keylookup_probe"),
    ("inject a set() dedup that collapses 1, 1.0 and True",
     _s_inject_dedup_cardinality, "C2V6-SCAN", "_c2v6_dedup_probe"),
    ("inject a wire value compared against a module-level named integer",
     _s_inject_named_constant_comparison, "C2V6-SCAN", "_c2v6_named_constant_probe"),
    ("inject membership in a numeric literal container",
     _s_inject_membership_comparison, "C2V6-SCAN", "_c2v6_membership_probe"),
    ("inject a max() over a wire sequence", _s_inject_sorted_launder,
     "C2V6-SCAN", "_c2v6_sorted_probe"),
)


def republish_every_counter(candidate, module, authority, tree):
    """Overwrite every bound integer leaf with the MUTANT's own measurements.

    This is the ordinary maintenance action the self-binding's cost model tells
    a maintainer to perform: run the checker, read the number out of the
    finding, paste it back.  The reviewer showed that performing it converted a
    genuine v5 layer break from caught to silent.  Here it is performed
    deliberately, on every row, and the named finding must survive it.
    """
    republished = copy.deepcopy(candidate)
    written = 0
    try:
        module.check(copy.deepcopy(republished), authority, tree)
        live = module.live_register(authority)
        bindings, _problems = module.candidate_bindings(
            republished, live, authority, authority.base, authority.measurement)
    except BaseException:                               # noqa: BLE001 - measured
        return republished, written
    for record in bindings:
        try:
            module._assign_steps(republished, record["steps"], record["expected"])
            written += 1
        except BaseException:                           # noqa: BLE001 - measured
            continue
    return republished, written


def selftest(candidate, authority, path):
    """Always reaches the suite; refuses a dirty base with a distinct code."""
    base_findings = check(candidate, authority)
    total = len(CONTRACT_MUTATIONS) + len(SOURCE_MUTATIONS) + len(SCAN_MUTATIONS)
    if base_findings:
        print("SELFTEST-REFUSED: the base candidate is not clean, so the mutation suite "
              "is not an oracle over it - every row would echo the pre-existing failure "
              "and report 'all rejected'.")
        print("  dirty base: " + str(len(base_findings)) + " finding(s) in " + path.name)
        for finding in base_findings[:10]:
            print("  base-finding:", finding)
        if jx_int_in_range(len(base_findings) - 10, 1, 10 ** 9):
            print("  ... " + str(len(base_findings) - 10) + " further base finding(s)")
        print("SELFTEST-NOT-RUN: zero of " + str(total) + " mutations executed. The "
              "distinct refusal code separates this from a green selftest, from "
              "ordinary findings and from a bad invocation, and can never be absorbed "
              "into a pass.")
        return 3
    clean_differential = authority.differential
    clean_successor = authority.successor
    print("C-2 v6 mutation self-test over " + path.name + " - each row must be REJECTED "
          "BY THE NAMED FINDING at the POSITION UNDER TEST, and every source row must "
          "stay rejected after every counter it publishes has been republished from the "
          "mutant's own measurements\n")
    escaped, rows, counter_only = [], 0, 0

    def report(ok, name, detail):
        nonlocal rows
        rows += 1
        print("  " + ("reject" if ok else "ESCAPE").rjust(6) + "  " + name)
        print("          " + detail)

    def hit_for(findings, expected, subject):
        out = []
        for item in findings:
            if jx_type(item) != "string" or jx_type(subject) != "string":
                continue
            if item.startswith(expected + ":") and subject in item:
                out.append(item)
        return out

    for name, root in (("string", "hostile-root"), ("null", None), ("list", []),
                       ("empty-object", {})):
        findings = check(copy.deepcopy(root), authority)
        named = hit_for(findings, "C2V6-TOTALITY-ROOT", "non-empty JSON object")
        if not named:
            escaped.append("parsed-JSON root " + name + ": no named C2V6-TOTALITY-ROOT "
                           "finding")
        report(bool(named), "parsed-JSON contract root " + name,
               named[0] if named else "NO NAMED FINDING - root survived")

    for name, mutate, expected, subject in CONTRACT_MUTATIONS:
        mutant = copy.deepcopy(candidate)
        try:
            mutate(mutant)
        except BaseException as exc:                    # noqa: BLE001 - reported
            escaped.append(name + ": mutation could not be applied (" +
                           type(exc).__name__ + ")")
            report(False, name, "mutation could not be applied")
            continue
        findings = check(mutant, authority)
        hit = hit_for(findings, expected, subject)
        if not hit:
            escaped.append(name + ": " + str(len(findings)) + " finding(s) but none is " +
                           expected + " naming " + repr(subject) + " - a non-zero result "
                           "is not evidence the guard fired")
        report(bool(hit), name, hit[0] if hit else
               (str(len(findings)) + " unrelated finding(s); first: " + findings[0]
                if findings else "NO FINDING"))

    tree = own_tree()
    for name, function, body, expected, subject, sweep_sensitive in SOURCE_MUTATIONS:
        label = name + " [" + function + "]"
        if sweep_sensitive:
            authority.pinned.clear()
        try:
            module = _execute_tree(_replace_body(tree, function, body))
            findings = module.check(copy.deepcopy(candidate), authority, tree)
        except BaseException as exc:                    # noqa: BLE001 - reported
            module, findings = None, ["mutated checker raised " + type(exc).__name__ +
                                      ": " + str(exc)]
        hit = hit_for(findings, expected, subject)
        survived = False
        written = 0
        if hit and module is not None:
            republished, written = republish_every_counter(
                candidate, module, authority, tree)
            try:
                after = module.check(republished, authority, tree)
            except BaseException as exc:                # noqa: BLE001 - reported
                after = ["mutated checker raised " + type(exc).__name__]
            survived = bool(hit_for(after, expected, subject))
        if sweep_sensitive:
            authority.pinned.clear()
            check(copy.deepcopy(candidate), authority)
        if not hit:
            escaped.append(
                label + ": " + str(len(findings)) + " finding(s) but none is " +
                expected + " naming " + repr(subject) + " - the break was not detected "
                "BY THE LAYER IT BREAKS, and a rejection from somewhere else is not "
                "evidence that layer is load-bearing")
        elif not survived:
            counter_only += 1
            escaped.append(
                label + ": " + expected + " fired, but republishing all " + str(written) +
                " bound counters from the mutant's own measurements SILENCED it. A "
                "counter is the sole detector of this break, and republishing a counter "
                "is the exact act this design's cost model instructs a maintainer to "
                "perform.")
        report(bool(hit) and survived, label,
               (hit[0][:180] + " | survives republication of " + str(written) +
                " bound counters") if hit and survived else
               (hit[0][:180] + " | COUNTER-ONLY: silenced by republication" if hit else
                (str(len(findings)) + " unrelated finding(s); first: " + findings[0][:150]
                 if findings else "NO FINDING")))

    for name, mutate, expected, subject in SCAN_MUTATIONS:
        try:
            broken = wire_comparison_scan(mutate(tree), "broken")
            findings = ["C2V6-SCAN: " + site["function"] + " line " +
                        str(site["line"]) + " (" + site["kind"] + ") " + site["source"]
                        for site in broken["sites"]]
        except BaseException as exc:                    # noqa: BLE001 - reported
            findings = ["scan raised " + type(exc).__name__ + ": " + str(exc)]
        hit = hit_for(findings, expected, subject)
        if not hit:
            escaped.append(name + ": the scan did not report " + expected + " naming " +
                           repr(subject) + "; an injected hazard the scan cannot see is "
                           "the defect that produced IR-C2V4-01 and IR-C2V5-01")
        report(bool(hit), name, hit[0][:180] if hit else
               "NO C2V6-SCAN finding naming " + subject)

    for row in clean_differential["rows"]:
        ok = row["successorNamedThePosition"] and not row["predecessorNamedThePosition"]
        if not ok:
            escaped.append(row["vector"] + ": differential lost")
        report(ok, "retained false accept " + row["vector"] + " at " + row["position"] +
               " spelled " + row["spelling"],
               "pinned check-c2-v4.py produced " + str(row["predecessorFindingCount"]) +
               " finding(s) and named the position: " +
               str(row["predecessorNamedThePosition"]) +
               (" (FULLY GREEN)" if row["predecessorFullyGreen"] else "") +
               "; this checker named it: " + str(row["successorNamedThePosition"]))

    for row in clean_successor["rows"]:
        ok = row["v6NamedThePosition"] and row["v5FullyGreen"]
        if not ok:
            escaped.append(row["vector"] + ": successor differential lost")
        report(ok, "retained v5 blocking vector " + row["vector"] + " at " + row["path"],
               "pinned check-c2-v5.py ran FULLY GREEN over it: " +
               str(row["v5FullyGreen"]) + "; this checker named the analogous position "
               "of its own document: " + str(row["v6NamedThePosition"]))

    print()
    if escaped:
        for item in escaped:
            print("SELFTEST-FAIL:", item)
        print(str(len(escaped)) + " of " + str(rows) + " retained cases ESCAPED (" +
              str(counter_only) + " of them detected only by a republishable counter) - "
              "the proof path is optional")
        return 1
    print("SELFTEST-PASS: all " + str(rows) + " retained cases rejected by their named "
          "finding at the position under test, and every one of the " +
          str(len(SOURCE_MUTATIONS)) + " source rows stayed rejected after every bound "
          "counter was republished from the mutant's own measurements - no counter is "
          "the sole detector of any break")
    print("  every one of the " + str(len(GUARD_HELPERS)) + " declared type gates is "
          "broken by this suite and every break is caught by the layer it breaks; L4's "
          "exclusion of the gates from its own scan is a debt and this is where it is "
          "paid")
    print("  L7 is terminal: nothing stands behind this suite but independent review, "
          "and every one of its " + str(rows) + " rows is printed above so a reviewer "
          "can be that thing")
    return 0


# =============================================================================
# Section 12.  Entry.
# =============================================================================

def _parse_argv(argv):
    flags, positional = set(), []
    for arg in argv[1:]:
        if jx_in(arg, list(DECLARED_FLAGS)):
            flags.add(arg)
        elif jx_type(arg) == "string" and arg.startswith("-"):
            raise UnsupportedInvocation("unknown flag " + repr(arg) + "; the declared "
                                        "flags are " + repr(list(DECLARED_FLAGS)))
        else:
            positional.append(arg)
    if jx_int_in_range(len(positional), 2, 10 ** 6):
        raise UnsupportedInvocation("at most one contract path may be supplied")
    return flags, (positional[0] if positional else None)


def main(argv):
    try:
        flags, requested = _parse_argv(argv)
    except UnsupportedInvocation as exc:
        print("C2V6-UNSUPPORTED-INVOCATION: " + str(exc), file=sys.stderr)
        return 2
    try:
        authority = load_authority()
    except AuthorityLoadError as exc:
        print("C2V6-PINNED-INPUT-REFUSED: " + type(exc).__name__ + ": " + str(exc),
              file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        candidate = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print("cannot load C-2 v6 candidate " + str(path) + ": " + type(exc).__name__ +
              ": " + str(exc), file=sys.stderr)
        return 2
    authority.document_name = path.name
    if jx_in("--selftest", list(flags)):
        return selftest(candidate, authority, path)
    findings = check(candidate, authority)
    if findings:
        print(str(len(findings)) + " finding(s) in " + path.name + ":")
        for item in findings:
            print("  -", item)
        return 1
    for line in authority.banner:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
