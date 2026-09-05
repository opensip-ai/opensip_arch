#!/usr/bin/env python3
"""Retained executable checker for the C-2 plan/stage contract, v9.

WHY v9 EXISTS
-------------
`1.0 == 1` has now defeated six consecutive artifacts written to defeat it, each
time in the repair's own self-certification rather than in the surface it
repaired:

    v3   LB-C2-01: a bare `!= 1` on schemaVersion              REJECTED
    v4   repairs the wire surface; its own census comparison   BLOCKING
         admits 57 of 136 integer leaves to a green banner     (IR-C2V4-01)
    v5   repairs the census and adds a document-wide type      REJECTED
         lock; its own `if not adjudicated <= lines:` at       (IR-C2V5-01..04)
         line 1815 admits `{2487} <= {2487.0}`
    v6   builds the comparison PRIMITIVE and routes the whole  REJECTED
         operator space through it -- and never reads the      (IR-C2V6-01)
         candidate's BYTES, so a duplicate key shadows a leaf
    v7   makes the PARSE a gate and closes IR-C2V6-01 -- and   REJECTED
         its own candidate totality enumerates integer and     (IR-C2V7-01)
         number leaves, so a BOOLEAN leaf is bound by nothing
    v8   makes the totality TOTAL over the JSON type space --  REJECTED
         and identifies a node by the `/`-JOIN of its path,    (IR-C2V8-01)
         which is not injective, so a leaf reparented across
         a `/` boundary leaves the skeleton digest unchanged

c2-plan-stage-schema.v8.review-independent.json, at
ae90724fb972bd16e6e1979d1777d190c80dcd6bf2747a0d7ed659c20eb5d785, is a REJECT on
ONE blocking finding and seven non-blocking ones.  The reviewer upheld v8's
central claim in terms this successor does not reopen:

    DERIVE-VS-ENUMERATE: YES OVER THE TYPE DIMENSION, NO OVER THE IDENTITY
    DIMENSION.

The type half was attacked and held.  `jx_leaf_census` could not be narrowed by
type: the reviewer transplanted v7's defect into v8's own tables, removing
`boolean` from all four, and the unconditional fall-through still caught an
injected root boolean with C2V9-LEAFRULE.  The 176-row suite ran to termination
with 0 escapes and 0 COUNTER-ONLY rows; a 228-case sweep admitted nothing;
`residualAccounting` resisted four attacks; `jx_bind_value` was total over 361
pairs; IR-C2V7-02 held at depth 20000.  NONE OF THAT IS REBUILT HERE.  What is
repaired is the IDENTITY half, which none of it touched:

    `document_skeleton` hashed `_steps_text(steps)` -- a `/`-join with NO
    ESCAPING.  The map from a structural path to its text is NOT INJECTIVE:
    the path ["a", "b"] and the path ["a/b"] both render as "a/b", so

        {"a": {"b": 1}}          and          {"a": {}, "a/b": 1}

    have IDENTICAL skeletons.  Against c2-plan-stage-schema.v8.json, ONE
    contiguous +11-byte edit -- relocating `thePrimitive/theEnumerationIsAGateToo`
    to a root key of that literal name -- left `documentSkeleton.sha256` and
    every published count byte-identical: exit 0, zero findings, full green
    banner (mutant 232b6499194a158b01614773a01bad226ea71421f5aed7d82b26422eb11620d8).
    12 leaf sites and 7 container subtrees of that document collide.

THE PATTERN, WHICH MATTERS MORE THAN THE BYTE
---------------------------------------------
v8's totality REACHED every node and then could not tell two nodes apart.  Every
version of this lineage has failed at the same joint: a place where one
representation stands in for another and the substitution is not injective.

    the comparison   v6   `1.0 == 1`: two values, one truth
    the parse        v7   a duplicate key: two leaves, one object
    the enumeration  v8   a boolean leaf: a type off the list
    the identity     v9   "a/b": two paths, one string

The repair is ONE LINE, and it is the property that already makes the VALUE half
sound, applied to the PATH half:

    document_skeleton hashes `jx_canon(list(steps))`, not `_steps_text(steps)`.

`jx_canon` is length-framed and type-tagged; `jx_decanon` inverts it; the round
trip is executed over the whole corpus on every run.  Its injectivity is not
asserted -- it is the existence of the inverse.  `skeleton_path_identity_probe`
executes BOTH halves every run: the pairs that collide under the joined text,
and the same pairs separating under the canonical token, plus a round trip of
every one of this document's own paths back through `jx_decanon`.  `_steps_text`
keeps its current form for FINDING TEXT, where a human reads it, and the
residual for that is RES-C2V9-19 with its own measured boundary.

WHAT ELSE THE v8 REJECT NAMED, AND WHAT WAS DONE
------------------------------------------------
  OBS-C2V8-01  `jx_type_space` measured at ONE fixed shallow path, so a census
               narrowed by DEPTH agreed with it silently.  It now places every
               witness at a declared LADDER of depths and inside an array, and
               `census_walk_agreement` cross-checks `jx_leaf_census` against
               `jx_walk` over the REAL 945-node document in both directions --
               so a depth-narrowed walk is a NAMED SEMANTIC finding and not
               only a counter drift.
  OBS-C2V8-02  "every residual carries a MEASURED BOUNDARY clause citing bound
               counters" was FALSE and unenforced.  `_residual_findings` now
               REQUIRES the literal clause and at least one live register key
               in every residual, and a detector probe proves the requirement
               is non-vacuous.
  OBS-C2V8-03  RETAINED-OPEN was interchangeable with RETAINED.  The open set
               is declared and required in BOTH directions.
  OBS-C2V8-04  three types were rejected COLLATERALLY.  The skeleton now
               publishes a PER-ROOT-SUBTREE digest table, so an injection at
               the root is named AT ITS OWN KEY and an injection at depth is
               named at its containing root subtree.
  OBS-C2V8-06  `_integer_leaf_steps`, the last type-named walker AND the last
               RECURSIVE one, is DELETED.  `census_leaves_of_type(node, kind)`
               takes the type as a PARAMETER and reads it back out of the total
               census.  No walk in this file names a scalar type.
  OBS-C2V8-07  a bogus eighth RFC production was contained only by a count.
               `JX_RFC8259_PRODUCTIONS` is now required to EQUAL a measurement
               taken by PARSING a corpus of JSON texts and dispatching each on
               its first significant byte, exactly as the grammar does.
  OBS-C2V7-03  the adoption text now says `AVAILABILITY ONLY` in those words,
               and the words are required by a guard.

v9 keeps v8's design entirely -- the primitive, the parse gate, the total leaf
census, the type space, the scan, the sweeps, the differentials and the mutation
suite are all preserved -- and changes exactly one thing: path identity.

v8 does not add another guard.  It builds ONE primitive -- the `jx` block in
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
tokens.

STATED ACCURATELY, BECAUSE v6 STATED IT WRONGLY.  v6 said "no numeric operator
is ever executed on a wire operand", and that is FALSE as worded: `jx_order`
runs `a < b` and `jx_int_in_range` runs `low <= value <= high`.  The property
that is true, and that is the one doing the work, is:

    NO COMPARISON BETWEEN OPERANDS OF DIFFERENT JSON TYPE IS EVER EXECUTED.

Both of those functions gate every operand to the SAME JSON type FIRST, so no
coercion path is reachable; `<` between two values already proved to be JSON
integers cannot coerce anything.  Equality never runs a numeric operator at all
-- it is string equality over canonical tokens.

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
    truthiness      bool(1) == bool(1.0) == bool(True)  -- `if x:` has exactly
                    the equivalence semantics this table exists to enumerate
    stringification "%d" % 1 == "%d" % 1.0 == "%d" % True
    THE PARSE       json.loads keeps the LAST duplicate key; NaN and Infinity
                    are accepted and are not JSON; `-0` parses to 0 and `1E2`
                    to 100.0, so the token in the bytes and the value every
                    guard compares are different texts

The last three rows arrived in v7.  The truthiness and stringification rows
were omitted from v6's table, which called itself the operator space, and the
independent reviewer found the omission; the parse rows are IR-C2V6-01.  Bare
truthiness is additionally MEASURED over real source by `bare_truthiness_sites`
and the count is published and bound -- deliberately not as a finding, because
every site this run inspected is a container or a syntax-tree object where
truthiness is emptiness and not numeric value.  That scope is RES-C2V9-09.

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
v8 does NOT repair them and does not grade them.  To adopt:

EVERY STEP BELOW NAMES ONLY FUNCTIONS THIS FILE DEFINES, AND THAT IS CHECKED ON
EVERY RUN.  v6's step 2 told an adopter to call `jx_min` and `jx_max`, NEITHER
OF WHICH EXISTED -- following the normative instructions verbatim produced a
NameError -- and v6's step 3 attributed to `jx_sorted` a refusal it does not
perform.  Both documents said it.  `declared_string_findings` now reads every
`jx_*` name out of this docstring AND out of the candidate document and refuses
any that this file does not define, so a wrong adoption step is a finding
instead of a defect a reader has to discover by trying it.

  1. Copy the delimited region and `jx_selftest()`.  Call `jx_selftest()` from
     your own run and fail closed unless `escapes` is empty; publish its counts.
  2. PARSE EVERY JSON INPUT WITH `jx_loads`, NOT ONLY THE ONE YOU CALL THE
     CANDIDATE, and emit a named finding at the position for every problem it
     reports.  `jx_loads` returns `(value, problems)`; a caller that discards
     `problems` is visible in its own source.  STATED PRECISELY, BECAUSE v7
     STATED IT LOOSELY (OBS-C2V7-03) AND v8 REPAIRED THE SUBSTANCE WITHOUT THE
     WORDS, WHICH WERE THE THING UNDER REVIEW: copying the delimited region gives
     you the parse gate's AVAILABILITY ONLY, never its USE.  `json_load_sites`,
     `json_parse_evasion_sites` and `parse_scan_findings` -- the things that make
     USING it structural -- are OUTSIDE the region, at module scope, and an
     adopter who copies only the region gets `jx_loads` without anything that
     requires it.  Copy those three as well and require every `json.load` and
     `json.loads` in YOUR tree to pass an `object_pairs_hook`, and every
     `JSONDecoder`, `raw_decode` and `getattr`-dispatch onto the json module to
     be zero.  The property has to be structural, because a parse defence
     applied to one input and not its siblings is the list-of-places failure
     this lineage exists to escape.  Note also that the copied region contains
     five bare `json.loads` calls of its own -- the OPERATOR_SPACE hazard
     demonstrations; they parse string literals and cannot reach adopter input,
     but a naive "no bare json.loads" grep over the region will find them.
     This step is IR-C2V6-01.
  2b. COPY `jx_leaf_census` AND `jx_type_space` AND USE THEM FOR ANY TOTALITY
     OVER A DOCUMENT.  Do not write a walker per JSON type.  Three consecutive
     versions of this artifact shipped a totality that enumerated the types its
     author thought of, and each time the live defect was at a type one step off
     the list.  `jx_leaf_census` names only the two container cases;
     `jx_type_space` measures that the fall-through reaches every type in the
     data model.  This step is IR-C2V7-01.
  3. Replace every wire-touching `==`/`!=`/`in`/`<`/`<=`/`>`/`>=`/subset with
     the `jx_` equivalent.  Replace `d[k]`/`d.get(k)` on wire keys with
     `jx_get`.  Replace `set(...)`/`{...}` over wire values with `jx_keyset`.
  4. Replace `sorted` over wire values with `jx_sorted` -- which ORDERS a
     heterogeneous JSON type set by canonical token and DOES NOT REFUSE ONE --
     or with `jx_sorted_homogeneous`, which refuses it by name.  Replace `min`
     and `max` with `jx_min` and `jx_max`, which refuse a mixed type set, an
     empty sequence, a non-orderable JSON type and a non-finite number, each by
     name.  Do NOT take an extreme off `jx_sorted`: token order is not value
     order, because the length prefix sorts first.
  5. Compare a published counter against a measured one with `jx_bind` ONLY, and
     a published string with `jx_bind_text`.  `jx_bind` asserts the JSON type of
     both operands independently and then compares CANONICAL STRINGS; no
     comparison between different JSON types is executed.
  6. Copy `wire_comparison_scan` and run it over your own tree.  Drive the
     ungated count to zero by repair, never by narrowing the model.  Copy
     `bare_truthiness_sites` too and publish what it finds: `if x:` on a wire
     number has the same equivalence semantics as `==`, and the scan does not
     model it.
  7. Publish your own blind spots.  `jx` has them; they are in KNOWN BLIND SPOTS
     below and in the contract's guardInventory.

SHOULD A CHECKER COMPARE A MEASURED VALUE AGAINST A WIRE-SUPPLIED ONE AT ALL?
----------------------------------------------------------------------------
This was posed as an open design question and v8 answers it in code.  The
comparison exists to catch contract drift and it is also what creates the
false-accept surface.  v8 keeps the comparison but removes the surface: the
measured value is recomputed, CANONICALISED TO A STRING, and bound to the
published value by string equality after an explicit, independent type
assertion on each side.  `jx_bind` never executes `==` between two numbers.
The residual risk is no longer numeric coercion; it is that the measurement
function measures the wrong space, which is a different failure mode, is named
as RES-C2V9-04, and is not repaired here.

KNOWN BLIND SPOTS OF THIS INSTRUMENT
------------------------------------
1. `jx_canon` diverges from Python `==` in exactly two places, both measured and
   published every run: it is STRICTER at every cross-type corpus pair and at
   -0.0 against 0.0, and LOOSER at exactly one -- NaN, which
   Python makes non-reflexive and `jx` makes reflexive.  An admission gate needs
   an equivalence relation; Python float equality is not one.  Non-finite floats
   are never JSON integers and are refused by `jx_int` regardless.
   v6 ADDITIONALLY had `jx_order` disagreeing with `jx_equal` -- it reported
   EQUAL for 0.0 against -0.0 and for NaN against every float -- and disclosed
   only the equality half of that.  v7 did not disclose the ordering half; it
   removes it.  `jx_order` decides the equal case by the same canonical string
   comparison `jx_equal` uses, the agreement is measured over the whole corpus
   cross-product every run as `primitiveOrderEqualityDivergences`, and it is 0.
2. L4 is still SYNTACTIC and its excusal test is still textual.  MEASURED THIS
   RUN AND STATED PLAINLY, because v5's residual pointed away from the live
   hazard: gate dominance currently excuses a published number of comparisons
   in this file, and the mechanism that actually hid IR-C2V5-01 was the TAINT
   MODEL, not the excusal test.  v7 extended taint to comprehension, generator,
   map/filter and container-constructor RESULTS -- the exact shape that
   laundered `lines` at check-c2-v5.py line 1815 -- and publishes both figures.
3. L4 cannot see a comparison built at run time (eval, exec, a dispatch table).
   It counts those primitives and requires eval and getattr-dispatch to be zero
   and exec to be exactly the two declared verified-snapshot loaders.
4. L4 cannot see `operator.ne` unless the name is visible.  v8 treats
   `operator.*` and bare `eq/ne/lt/le/gt/ge/contains` calls as comparison sites
   AND requires the `operator` module to be unimported here.  A checker that
   imports it must scan for it; that is stated for adopters.
5. This file cannot hash-pin itself.  Its own digest is REPORTED, never verified.
6. v8 does not re-run check-c2-v4.py --selftest, the predecessor's ~24k-case
   contract-root execution matrix.  Retained as RES-C2V9-03.
7. The type lock closes JSON TYPE.  A type-correct integer with a wrong VALUE at
   a position no layer measures is outside it.  v8 narrows that gap by requiring
   EVERY leaf of its own candidate document whose JSON type is ruled BIND -- null,
   boolean, integer and number -- to be bound to a live measurement or to a
   verified pinned byte, with no unbound bucket, and by binding the PATH and TYPE
   of every node through the skeleton digest -- but the effective contract
   inherited from the predecessor still has type-correct value drift outside the
   counter register.  Retained as RES-C2V9-05.
7b. A NARRATIVE STRING LEAF'S TEXT IS NOT BOUND.  Its path and its type are, and
   its existence is, and the number of them is published; the words are not.
   The size of that gap is a measured number in RES-C2V9-07 and in the banner,
   not an adjective.  Two JSON edits -- the leaf and a recomputed skeleton
   digest -- admit a new narrative string; one does not.
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
10. L8 covers ONE class -- "the bytes on disk and the object every guard reads
   are different documents" -- and covers three members of it: duplicate keys at
   any depth in every input this checker parses, non-RFC constants, and number
   tokens whose spelling is not the canonical spelling of their value.  It does
   NOT cover STRING escape spellings: `"a"` and `"a"` parse identically and
   this checker does not object, because legitimate documents escape strings and
   a canonical-escaping rule would refuse them.  It also does not reach the
   parses performed INSIDE the pinned check-c2-v4.py and check-c2-v5.py, which
   are their own reviewed bytes and are not v8's to change.  RES-C2V9-08.
11. L9 closes "a declared string that names something that exists NOWHERE".  It
   does not close "a declared string that names something that exists SOMEWHERE
   OTHER than the guard it asserts on" -- which is the exact shape of the v6 row
   that asserted `outside the census block` while its guard emitted `OUTSIDE the
   census block`, because the lower-case spelling genuinely occurs in a banner
   template.  The emit-site figure is published so the size of that gap is
   visible rather than described.  RES-C2V9-10.
12. Everything this run does NOT recompute is in RES-C2V9-11, in the artifact,
   not in prose to a coordinator.  v6's incomplete selftest was disclosed
   conversationally and never written into the document, and its residual list
   was described as ten when it held seven.
13. L8's structural parse scan is SYNTACTIC.  v8 counts the two evasions the v7
   reviewer measured -- `json.JSONDecoder().decode` and `getattr(json, "loads")`
   -- and requires both to be zero, which is what L4 already does for its own
   analogous evasions and what L8 did not do.  It remains a syntactic scan: a
   parse reached through a name this file computes at run time is outside it.
   RES-C2V9-12.
14. The DEPTH at which "every duplicate key at any depth" holds is now a MEASURED
   NUMBER.  v7's duplicate-path walk was recursive and raised an uncaught
   RecursionError past depth 1000 -- traceback, exit 1, zero findings, on exactly
   and only the vector the gate exists to catch (IR-C2V7-02).  The walk is
   iterative; the claim is executed at a declared depth on every run and the
   depth is published.  What is still bounded is `jx_canon` itself, which is
   recursive over a VALUE; it is never applied to a whole candidate document.
   RES-C2V9-13.

Usage: python3 -I -B artifacts/check-c2-v9.py [contract]  ·  --selftest
Exit:  0 clean or green selftest · 1 findings · 2 unsupported invocation, or a
       pinned input that does not hash to its declared digest, or a softened
       disposition, or a candidate whose bytes are not a JSON document at all ·
       3 --selftest REFUSED over a dirty base, which can never be absorbed into
       a pass.  The fourth clause of exit 2 is OBS-C2V7-06: a BOM prefix and
       trailing content after the top-level value both exit 2 in v7 and its
       published exit contract did not describe them.

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

BINDING = "c2-plan-stage-schema.v9.json"
DECLARED_FLAGS = ("--selftest",)
DECLARED_EXIT_CODES = frozenset({"0", "1", "2", "3"})
HERE = pathlib.Path(__file__).resolve().parent
ARTIFACT_ID = "opensip.c2-plan-stage-schema.v9"


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
# RFC 8259 sections 3 to 7: a JSON value is one of exactly these seven
# productions and there is no eighth.  `jx_type` REFINES `number` into `integer`
# and `number`, because the host language distinguishes them and every finding
# in this lineage is about that distinction.  The refinement is declared here,
# beside the standard it refines, and `jx_type_space` MEASURES that the union of
# the refinements is exactly JX_TYPES, that every member of JX_TYPES refines
# some production, and that every member is realised by a witness.
#
# THIS IS WHERE v8 DIFFERS FROM v7 AT THE ENUMERATION LAYER.  v7's candidate
# totality was built from two walkers that named the types they covered --
# integer and number -- and a boolean leaf was enumerated by neither, so a
# one-byte edit flipping this document's own claim that it reproduced
# IR-C2V6-01 reached a full green run (IR-C2V7-01).  That is the same shape as
# v6's float gap and v5's taint gap: a totality that is a LIST OF TYPES is a
# list of places, and the defect moves to a place not on the list.  v8's
# totality names no scalar type at all.  `jx_leaf_census` names the two
# CONTAINER cases and lets every other type fall through to a leaf, so the type
# coverage is generated by the data model rather than enumerated by an author,
# and `jx_type_space` measures that the fall-through actually reaches each
# declared type rather than asserting it.
JX_RFC8259_PRODUCTIONS = (
    ("null", ("null",)),
    ("true", ("boolean",)),
    ("false", ("boolean",)),
    ("number", ("integer", "number")),
    ("string", ("string",)),
    ("array", ("array",)),
    ("object", ("object",)),
)
# At least one witness for every production, including both spellings of a JSON
# number, both boolean values, and both container shapes empty and non-empty.
# `jx_type_space` refuses if any member of JX_TYPES has no witness, so the
# corpus cannot silently stop covering a type.
JX_TYPE_WITNESSES = (None, True, False, 0, 1, -1, 10 ** 60,
                     0.0, -0.0, 1.5, float("inf"), float("nan"),
                     "", "x", "1", [], [1], [[]], {}, {"k": 1}, {"k": {}})
# OBS-C2V8-01.  v8 evaluated every witness at ONE fixed path -- `{"probe": w}`,
# depth 1 -- so a census narrowed by DEPTH rather than by TYPE agreed with the
# measurement silently: a census dropping every leaf deeper than two steps
# discards 577 of this document's 797 leaves and produced ZERO type-space
# escapes.  What refused it was the counter binding, not the type space.  Every
# witness is now placed at each depth on this LADDER and inside an ARRAY, so a
# depth-narrowed census reports a type as a leaf at one placement and as a
# container at another -- and the "neither a leaf nor a container" and "both"
# escapes below name it.  The ladder is a declared table of DEPTHS, not of
# types; the type coverage is still generated by the data model.
JX_TYPE_SPACE_PLACEMENTS = ((0, False), (1, False), (3, False), (12, False),
                            (2, True), (7, True))
# RFC 8259 dispatches a value on its FIRST significant byte.  The corpus below
# is JSON TEXT, not values; `_jx_rfc_production` performs exactly that dispatch
# and `jx_type_space` requires JX_RFC8259_PRODUCTIONS to EQUAL the measurement
# taken by PARSING it.  OBS-C2V8-07: v8 caught the REMOVAL of a production
# semantically but contained the ADDITION of a bogus eighth one only with a
# published count, because a refinement into an already-declared type narrows
# nothing.  Both directions are semantic now: a production no JSON text
# realises, and a text no production covers, are each a named finding.  What is
# still DECLARED is that this corpus covers the grammar -- RES-C2V9-15.
JX_RFC8259_GRAMMAR_CORPUS = ("null", "true", "false", "0", "-1", "1.5", "100.0",
                             "\"\"", "\"x\"", "[]", "[1]", "{}", "{\"k\": 1}")
JX_RFC8259_DISPATCH = (("n", "null"), ("t", "true"), ("f", "false"),
                       ("\"", "string"), ("[", "array"), ("{", "object"))
JX_RFC8259_NUMBER_LEADS = ("-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
# Names this block is permitted to reference from outside itself.  Builtins and
# the block's own definitions are excluded automatically.  If this list is not
# exactly the measured free-name set, the portability claim is false and the
# run fails; a claim that a component is reusable is a coverage claim like any
# other and is held to the same standard.
JX_PORTABILITY_BOUNDARY = ("json", "math")

import json  # noqa: E402  -- inside the portability boundary on purpose
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


def _jx_deep_witness(depth):
    """A nested object `depth` levels deep holding exactly one leaf, built
    ITERATIVELY.  It exists so the claim that the walks have no depth limit of
    their own is executed rather than asserted -- IR-C2V7-02 was precisely a
    walk whose depth limit nobody had measured."""
    node = True
    for _step in range(depth):
        node = {"n": node}
    return node


def jx_walk(value) -> list:
    """EVERY node of a JSON value as `[path, jx type]`, containers included.

    Iterative, so no host recursion limit stands between this walker and a
    deeply nested document; `_jx_duplicate_paths` used to be the recursive
    version of this shape and raised an uncaught RecursionError past depth 1000
    (IR-C2V7-02).  Paths are LISTS of steps, never tuples: a tuple is outside
    the JSON value universe, `jx_canon` refuses it by name, and `(1,) == (1.0,)`
    is True in the host language.
    """
    out, stack = [], [[[], value]]
    while stack:
        steps, node = stack.pop()
        kind = jx_type(node)
        out.append([list(steps), kind])
        if kind == "object":
            keys = list(node)
            for position in range(len(keys) - 1, -1, -1):
                stack.append([list(steps) + [keys[position]],
                              jx_at(node, keys[position])])
        elif kind == "array":
            for position in range(len(node) - 1, -1, -1):
                stack.append([list(steps) + [position], node[position]])
    return out


def jx_leaf_census(value) -> list:
    """EVERY leaf of a JSON value as `[path, jx type]`.  Total by construction.

    THE SCALAR TYPES ARE NOT ENUMERATED HERE.  Only the two CONTAINER cases are
    named; everything else falls through to a leaf, so a JSON type this author
    did not think of is reported as a leaf rather than vanishing from the
    totality.  That is the whole difference between this and the two walkers it
    replaces: `_integer_leaf_steps` and `_number_leaf_steps` each named the type
    they covered, three consecutive versions shipped with the live hazard one
    type away from the list, and IR-C2V7-01 is the third of them.

    `jx_type_space` measures that the fall-through reaches every member of
    JX_TYPES, so the coverage is a MEASUREMENT over the JSON data model and not
    a claim about a list.  Iterative for the same reason `jx_walk` is.
    """
    out, stack = [], [[[], value]]
    while stack:
        steps, node = stack.pop()
        kind = jx_type(node)
        if kind == "object":
            keys = list(node)
            for position in range(len(keys) - 1, -1, -1):
                stack.append([list(steps) + [keys[position]],
                              jx_at(node, keys[position])])
        elif kind == "array":
            for position in range(len(node) - 1, -1, -1):
                stack.append([list(steps) + [position], node[position]])
        else:
            out.append([list(steps), kind])
    return out


def _jx_place(witness, depth, in_array):
    """`witness` inside `depth` nested containers, and the path to it.

    Built ITERATIVELY, and the path is returned rather than assumed, so the
    caller reads the census AT THE PLACE IT PUT THE WITNESS instead of at one
    hard-coded shallow key."""
    node, steps = witness, []
    for level in range(depth):
        if in_array and jx_exact_int(level, 0):
            node = [node]
            steps = [0] + steps
        else:
            node = {"probe" + str(level): node}
            steps = ["probe" + str(level)] + steps
    return node, steps


def _jx_rfc_production(text):
    """The RFC 8259 production a JSON TEXT belongs to, by its first byte.

    This is the grammar's own dispatch, not a table of names: `null` is the
    null production because it begins with `n`, and nothing that begins with
    `d` is a production at all.  OBS-C2V8-07."""
    for first, production in JX_RFC8259_DISPATCH:
        if text.startswith(first):
            return production
    for lead in JX_RFC8259_NUMBER_LEADS:
        if text.startswith(lead):
            return "number"
    return JX_UNSUPPORTED


def jx_rfc_production_space() -> dict:
    """The RFC 8259 productions this primitive can be SHOWN to realise.

    Every text is dispatched on its first byte and then PARSED, and the JSON
    type of the parsed value is what the production refines into.  Nothing here
    reads JX_RFC8259_PRODUCTIONS; `jx_type_space` compares the two.
    """
    measured, escapes, texts = {}, [], 0
    for text in JX_RFC8259_GRAMMAR_CORPUS:
        texts += 1
        production = _jx_rfc_production(text)
        if jx_equal(production, JX_UNSUPPORTED):
            escapes.append("the JSON grammar corpus holds " + repr(text) + ", whose "
                           "first byte dispatches to no RFC 8259 production, so the "
                           "corpus is not a corpus of JSON values")
            continue
        try:
            value, problems = jx_loads(text)
        except Exception as exc:                        # noqa: BLE001 - measured
            escapes.append("the JSON grammar witness " + repr(text) + " raised " +
                           type(exc).__name__ + " rather than parsing, so the "
                           "production it dispatches to is not realised by execution")
            continue
        if problems:
            escapes.append("the JSON grammar witness " + repr(text) + " does not say "
                           "the same thing to a reader as to this instrument")
            continue
        jx_put(measured, production,
               jx_sorted(jx_unique(list(jx_get(measured, production, [])) +
                                   [jx_type(value)])))
    return {"texts": texts, "productions": len(measured), "measured": measured,
            "escapes": escapes}


def jx_type_space() -> dict:
    """MEASURED, not declared: the type space this primitive actually realises.

    For every witness: which JSON type it is, and whether `jx_leaf_census`
    reports it as a LEAF of that type or DESCENDS THROUGH it as a container.
    Then: every member of JX_TYPES must be realised by some witness, every
    member must refine some RFC 8259 production, every production must refine
    into declared types, and no type may be both a leaf and a container.

    This is the published demonstration that the enumeration is total over the
    TYPE SPACE rather than over the types the author remembered.  Narrowing the
    census to the types v7 covered is caught here as well as by the live
    injection probe, because the types the census reports as leaves would then
    no longer be the scalar half of the data model.
    """
    realised, containers, scalars, escapes = [], [], [], []
    placements = 0
    for witness in JX_TYPE_WITNESSES:
        kind = jx_type(witness)
        if jx_equal(kind, JX_UNSUPPORTED):
            escapes.append("the witness " + repr(witness) + " is outside the JSON value "
                           "universe, so it witnesses no JSON type")
            continue
        realised.append(kind)
        for depth, in_array in JX_TYPE_SPACE_PLACEMENTS:
            placements += 1
            document, steps = _jx_place(witness, depth, in_array)
            here = [row for row in jx_leaf_census(document)
                    if jx_equal(row[0], list(steps))]
            if jx_int_in_range(len(here), 1, 1) and jx_equal(here[0][1], kind):
                scalars.append(kind)
            elif jx_int_in_range(len(here), 0, 0):
                containers.append(kind)
            else:
                escapes.append("the leaf census reports " + str(len(here)) + " leaf/"
                               "leaves at the depth-" + str(depth) + " position holding "
                               "the JSON " + kind + " witness " + repr(witness) + ", so "
                               "that type is neither a leaf nor a container and the "
                               "census is not total over it")
    realised = jx_sorted(jx_unique(realised))
    containers = jx_sorted(jx_unique(containers))
    scalars = jx_sorted(jx_unique(scalars))
    unwitnessed = jx_sorted(jx_difference(list(JX_TYPES), realised))
    for kind in unwitnessed:
        escapes.append("JX_TYPES declares the JSON type " + repr(kind) + " and no "
                       "witness realises it, so nothing measures whether the leaf "
                       "census reaches it; an unwitnessed type is exactly how a "
                       "totality comes to be narrower than the data model")
    for kind in jx_sorted(jx_difference(realised, list(JX_TYPES))):
        escapes.append("a witness realises the JSON type " + repr(kind) + ", which "
                       "JX_TYPES does not declare")
    for kind in jx_sorted([item for item in containers if jx_in(item, scalars)]):
        escapes.append("the leaf census treats the JSON type " + repr(kind) + " as a "
                       "container at one witness or DEPTH and as a leaf at another, so "
                       "its totality is not well defined over that type; a census "
                       "narrowed by depth rather than by type lands here")
    # OBS-C2V8-07.  The production table must EQUAL what parsing the grammar
    # corpus realises, in BOTH directions, so a bogus eighth production is a
    # named finding rather than a moved count.
    grammar = jx_rfc_production_space()
    for item in grammar["escapes"]:
        escapes.append(item)
    declared_productions = jx_sorted(jx_unique([name for name, _r
                                                in JX_RFC8259_PRODUCTIONS]))
    realised_productions = jx_sorted(list(grammar["measured"]))
    for name in jx_sorted(jx_difference(declared_productions, realised_productions)):
        escapes.append("JX_RFC8259_PRODUCTIONS declares the production " + repr(name) +
                       ", which NO JSON text in the grammar corpus realises; a "
                       "production that is a name rather than a shape of the standard "
                       "widens the declared type space without widening the measured "
                       "one")
    for name in jx_sorted(jx_difference(realised_productions, declared_productions)):
        escapes.append("parsing the grammar corpus realises the RFC 8259 production " +
                       repr(name) + ", which JX_RFC8259_PRODUCTIONS does not declare")
    for name, refinement in JX_RFC8259_PRODUCTIONS:
        seen = jx_get(grammar["measured"], name)
        if seen is None:
            continue
        if not jx_equal(jx_sorted(jx_unique(list(refinement))), seen):
            escapes.append("the production " + repr(name) + " is declared to refine "
                           "into " + repr(jx_sorted(jx_unique(list(refinement)))) +
                           " and parsing its witnesses realises " + repr(seen))
    refined = []
    for production, refinement in JX_RFC8259_PRODUCTIONS:
        if not jx_int_in_range(len(refinement), 1, 10 ** 6):
            escapes.append("RFC 8259 production " + repr(production) + " is refined "
                           "into nothing, so a value the standard admits has no type "
                           "in this primitive")
        for kind in refinement:
            refined.append(kind)
            if not jx_in(kind, list(JX_TYPES)):
                escapes.append("RFC 8259 production " + repr(production) + " is refined "
                               "into " + repr(kind) + ", which JX_TYPES does not "
                               "declare")
    for kind in jx_sorted(jx_difference(list(JX_TYPES), refined)):
        escapes.append("JX_TYPES declares " + repr(kind) + ", which refines no RFC 8259 "
                       "production, so the type space has drifted away from the data "
                       "model it claims to enumerate")
    return {"witnesses": len(JX_TYPE_WITNESSES), "declaredTypes": len(JX_TYPES),
            "types": len(realised), "containers": len(containers),
            "scalars": len(scalars), "unwitnessed": len(unwitnessed),
            "rfcProductions": len(JX_RFC8259_PRODUCTIONS),
            "placements": placements, "grammarTexts": grammar["texts"],
            "grammarProductions": grammar["productions"],
            "containerTypes": containers, "scalarTypes": scalars, "escapes": escapes}


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

    ORDERING AND EQUALITY AGREE, BY CONSTRUCTION.  This returns 0 if and only if
    `jx_equal` is True, because the equal case is decided by the SAME canonical
    string comparison `jx_equal` uses, before any `<` runs.  v6 decided the
    equal case by falling through `a < b` and `b < a`, which reported EQUAL for
    `0.0` against `-0.0` and for NaN against every float -- both pairs that
    `jx_equal` calls distinct.  A gate whose ordering and whose equality
    disagree has two answers to one question; the divergence is removed here
    rather than disclosed.  Two distinct values of the same JSON type that do
    not order -- which after this change is NaN and only NaN -- are NOT
    comparable, and `None` is the honest answer for them.
    """
    if not jx_same_type(a, b):
        return None
    if jx_canon(a) == jx_canon(b):
        return 0
    kind = jx_type(a)
    if kind in ("array", "object", "null", "boolean"):
        return None
    if a < b:
        return -1
    if b < a:
        return 1
    return None


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
    """Sorted by canonical TOKEN.  Total and deterministic.

    IT ORDERS A HETEROGENEOUS JSON TYPE SET; IT DOES NOT REFUSE ONE.  Both v6
    documents said it refused, and it does not: the function that refuses is
    `jx_sorted_homogeneous`, and `jx_min`/`jx_max` refuse through it.  What this
    function guarantees is weaker and still worth having -- the order is over
    tokens rather than numbers, so 1 and 1.0 are never interleaved by a
    host-language comparison between two different JSON types, and the result is
    stable across runs.  TOKEN ORDER IS NOT VALUE ORDER: the length prefix sorts
    first, so `jx_sorted([3, -5])` is `[3, -5]`.  Use it for determinism, never
    for extremes.
    """
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


JX_ORDERABLE = ("integer", "number", "string")


def jx_min(values):
    """(minimum, reason).  REFUSES rather than ordering what cannot be ordered.

    v6's module docstring told an adopter to call this and it DID NOT EXIST, so
    step 2 of the normative adoption instructions raised NameError.  It exists
    now, and it is a real replacement for `min`, not an alias for `jx_sorted`:
    `min([1, 1.0])` returns whichever the host language reached first and tells
    you nothing about which JSON type you got, and token order is not value
    order, so the extreme is taken through `jx_lt` over a set already proved
    homogeneous.  A mixed type set, an empty sequence, a non-orderable JSON type
    and a non-finite number are each refused BY NAME.
    """
    ordered, reason = jx_sorted_homogeneous(values)
    if reason is not None:
        return None, reason
    if not jx_int_in_range(len(ordered), 1, 10 ** 9):
        return None, "an empty sequence has no minimum"
    kind = jx_type(ordered[0])
    if not jx_in(kind, list(JX_ORDERABLE)):
        return None, ("a sequence of JSON " + kind + " values has no total order; law "
                      "18 rejects the type before the content is compared")
    for item in ordered:
        if jx_type(item) == "number" and not math.isfinite(item):
            return None, ("the non-finite number " + repr(item) + " orders against "
                          "nothing, so an extreme taken over this sequence would "
                          "silently skip an element rather than answer for it")
    best = ordered[0]
    for item in ordered:
        if jx_lt(item, best):
            best = item
    return best, None


def jx_max(values):
    """(maximum, reason).  The mirror of `jx_min`, and refuses the same things."""
    ordered, reason = jx_sorted_homogeneous(values)
    if reason is not None:
        return None, reason
    if not jx_int_in_range(len(ordered), 1, 10 ** 9):
        return None, "an empty sequence has no maximum"
    kind = jx_type(ordered[0])
    if not jx_in(kind, list(JX_ORDERABLE)):
        return None, ("a sequence of JSON " + kind + " values has no total order; law "
                      "18 rejects the type before the content is compared")
    for item in ordered:
        if jx_type(item) == "number" and not math.isfinite(item):
            return None, ("the non-finite number " + repr(item) + " orders against "
                          "nothing, so an extreme taken over this sequence would "
                          "silently skip an element rather than answer for it")
    best = ordered[0]
    for item in ordered:
        if jx_gt(item, best):
            best = item
    return best, None


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


def jx_bind_value(published, measured):
    """THE binding a TOTALITY calls.  Total over the whole JSON scalar space.

    `jx_bind` answers for the integer case and `jx_bind_text` for the string
    case, and each carries the diagnostic of the finding it exists for.  Both
    are specialised, and a totality built on a specialised binding is only as
    wide as the specialisations somebody remembered to write: v7's candidate
    ledger had an integer walker and a number walker, and a BOOLEAN leaf -- the
    document's own claim that this lane reproduced IR-C2V6-01 -- was bound by
    neither, so flipping it was a one-byte edit to a full green run.

    This entry point asks no question about which JSON type it is holding.  It
    asserts that both sides have the SAME type, refuses a container by name
    because a container is bound by the leaves it holds rather than as a leaf,
    and then compares CANONICAL STRINGS.  No numeric operator runs, at any type.
    """
    kind = jx_type(measured)
    if jx_equal(kind, JX_UNSUPPORTED):
        return ("the value this run MEASURED is outside the JSON value universe, so "
                "there is nothing a binding could assert about it")
    if jx_in(kind, ["array", "object"]):
        return ("the value this run MEASURED is a JSON " + kind + "; a container is "
                "bound by the leaves it holds and never as a leaf, so a binding here "
                "would be a coverage claim over its contents that nothing checks")
    if jx_type(published) != kind:
        return ("it is published as " + repr(published) + ", whose JSON type is " +
                jx_type(published) + ", not the JSON " + kind + " this run measured (" +
                repr(measured) + "); freeze section 6 law 18 requires the type to be "
                "rejected before the content is compared, and the type that escaped "
                "v7's totality was boolean")
    if jx_canon(published) != jx_canon(measured):
        return ("it is published as " + repr(published) + " but this run measured " +
                repr(measured))
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


# ---- the parse: where the BYTES and the PARSED OBJECT are forced to agree ----
#
# IR-C2V6-01.  Everything above canonicalises a value it is GIVEN, and every
# guard in every checker that adopts this block reads a value the host parser
# produced.  `json.loads` is not injective over bytes, in three separate ways,
# and each of them lets a document say one thing to a reader and another thing
# to every instrument:
#
#   duplicate-key      `{"version": 6.0, "version": 6}` parses to a dict that is
#                      byte-for-byte the parse of `{"version": 6}`.  CPython
#                      keeps the LAST occurrence.  Eighteen bytes inserted into
#                      c2-plan-stage-schema.v6.json put a JSON float at the one
#                      key whose integer-ness check-c2-v6.py enforces by an
#                      explicit named rule, and check-c2-v6.py printed a full
#                      green banner over it.  No amount of strengthening the
#                      comparison primitive closes that, because the comparison
#                      never sees the shadowed value.
#   non-rfc-constant   `NaN`, `Infinity` and `-Infinity` are not JSON.  CPython
#                      accepts them and hands back a float.
#   number-text        `-0` parses to the integer 0.  `1E2` parses to 100.0.
#                      `1.10` parses to 1.1.  The token in the file and the
#                      value every guard compares are different texts.
#
# `jx_loads` parses and REPORTS all three, each with a position.  It repairs
# nothing and guesses nothing: it returns the parse the host produced AND an
# explicit account of what the host threw away, so a caller that ignores the
# account is visible in the caller's own source rather than invisible in the
# parser's.  `check-trusted-request-context-v3.py` in this corpus already
# refuses duplicate keys by raising from an `object_pairs_hook`; this reports
# instead of raising, so the refusal can be a NAMED FINDING AT THE POSITION
# rather than an exit code, because a non-zero exit is not evidence a guard
# fired.

JX_PARSE_KINDS = ("duplicate-key", "non-rfc-constant", "number-text")


class JxDuplicateKeyError(ValueError):
    """A JSON object carries the same key twice, so the bytes and the parse
    cannot both be believed."""


def jx_number_tokens(text) -> list:
    """Every JSON number token of `text` that is NOT inside a string literal.

    Returns `[[offset, token], ...]`.  The string state is tracked explicitly
    because a regular expression cannot tell a number inside a string from one
    outside it, and reading the BYTES is the entire purpose of this function.
    Digits are tested by range rather than by `str.isdigit`, which is True for
    Unicode digits that JSON does not accept.
    """
    if jx_type(text) != "string":
        raise JxDomainError("jx_number_tokens requires document TEXT, not a value")
    out = []
    position, size, inside = 0, len(text), False
    while position < size:
        character = text[position]
        if inside:
            if character == "\\":
                position = position + 2
                continue
            if character == '"':
                inside = False
            position = position + 1
            continue
        if character == '"':
            inside = True
            position = position + 1
            continue
        if character == "-" or ("0" <= character <= "9"):
            end = position + 1
            while end < size and (("0" <= text[end] <= "9") or text[end] in ".eE+-"):
                end = end + 1
            out.append([position, text[position:end]])
            position = end
            continue
        position = position + 1
    return out


def jx_refusing_pairs(items):
    """`object_pairs_hook` that RAISES on a duplicate key.

    `jx_loads` reports instead, because a named finding at a position is better
    evidence than an exception.  This variant exists for the places where a
    duplicate key cannot occur and a report would have nowhere to go, so that
    EVERY `json.loads` in a file that adopts this block passes a hook and the
    property "no bare parse anywhere" is structural rather than per-call-site.
    """
    result, seen = {}, set()
    for key, value in items:
        token = jx_key(key)
        if token in seen:
            raise JxDuplicateKeyError("duplicate JSON key " + repr(key))
        seen.add(token)
        jx_put(result, key, value)
    return result


def jx_number_text_problems(text) -> list:
    """Number tokens whose BYTES are not the canonical spelling of the value the
    host parser produces from them."""
    out = []
    for offset, token in jx_number_tokens(text):
        try:
            value = json.loads(token, object_pairs_hook=jx_refusing_pairs)
        except ValueError:
            out.append({"kind": "number-text", "path": [], "key": token,
                        "offset": offset, "token": token,
                        "detail": "is not a JSON number at all"})
            continue
        canonical = jx_canon(value)
        spelling = canonical[canonical.index(":") + 1:]
        if not jx_equal(spelling, token):
            out.append({"kind": "number-text", "path": [], "key": token,
                        "offset": offset, "token": token,
                        "detail": "parses to the JSON " + jx_type(value) + " whose "
                                  "canonical spelling is " + spelling + ", so the "
                                  "bytes and the value every guard compares are "
                                  "different texts"})
    return out


def _jx_duplicate_paths(node, steps, marks, out) -> None:
    """Walk the parse and report every recorded duplicate under its OWN path.

    ITERATIVE.  IR-C2V7-02: the recursive version of this walk raised an
    UNCAUGHT RecursionError past nesting depth 1000 -- traceback, exit 1, zero
    findings -- and it recursed only when `marks` was non-empty, which is
    exactly and only the vector this gate exists to catch.  The banner's claim
    is "every duplicate key AT ANY DEPTH", so the walk must not have a depth
    limit of its own.  The host parser's own limit is measured and published by
    `parse_depth_probe` rather than described.
    """
    stack = [[list(steps), node]]
    while stack:
        here, current = stack.pop()
        kind = jx_type(current)
        if kind == "object":
            for key in jx_get(marks, id(current), []):
                out.append({"kind": "duplicate-key", "path": list(here) + [key],
                            "key": key, "offset": -1, "token": "",
                            "detail": "is published more than once in the bytes; the "
                                      "host parser keeps the LAST occurrence, so the "
                                      "parsed object cannot say what the document says"})
            keys = list(current)
            for position in range(len(keys) - 1, -1, -1):
                stack.append([list(here) + [keys[position]],
                              jx_at(current, keys[position])])
        elif kind == "array":
            for position in range(len(current) - 1, -1, -1):
                stack.append([list(here) + [position], current[position]])


def jx_loads(text):
    """Parse JSON and REPORT every way the BYTES and the PARSE disagree.

    Returns `(value, problems)`.  Each problem carries `kind`, `path`, `key`,
    `offset` and `detail`.  This is the ONLY parse any adopting checker should
    perform, for EVERY input it loads and not only for the one it calls the
    candidate: a defence applied to one input and not to its siblings is the
    list-of-places failure this lineage exists to escape.
    """
    if jx_type(text) != "string":
        raise JxDomainError("jx_loads requires the document TEXT, not a parsed value")
    marks, keep, constants = {}, [], []

    def pairs(items):
        result, seen, repeated = {}, set(), []
        for key, value in items:
            token = jx_key(key)
            if token in seen:
                repeated.append(key)
            seen.add(token)
            jx_put(result, key, value)
        if jx_int_in_range(len(repeated), 1, 10 ** 9):
            keep.append(result)
            jx_put(marks, id(result), repeated)
        return result

    def constant(token):
        constants.append(token)
        if jx_equal(token, "NaN"):
            return float("nan")
        if jx_equal(token, "Infinity"):
            return float("inf")
        return float("-inf")

    value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    problems = []
    for token in constants:
        problems.append({"kind": "non-rfc-constant", "path": [], "key": token,
                         "offset": -1, "token": token,
                         "detail": "is not a JSON value at all; RFC 8259 has no NaN "
                                   "and no Infinity, and the host parser accepts both"})
    found = []
    if jx_int_in_range(len(marks), 1, 10 ** 9):
        _jx_duplicate_paths(value, [], marks, found)
    problems.extend(found)
    declared = 0
    for identity in list(marks):
        declared = declared + len(jx_get(marks, identity, []))
    if jx_lt(len(found), declared):
        problems.append({"kind": "duplicate-key", "path": [], "key": "",
                         "offset": -1, "token": "",
                         "detail": "a duplicate key was found in an object that the "
                                   "parse itself discarded, so this run cannot report "
                                   "its path; the count is still refused"})
    problems.extend(jx_number_text_problems(text))
    # `keep` holds a live reference to every object that recorded a duplicate, so
    # no id() in `marks` can be reused by a collected object while the paths are
    # being resolved.  It is read here for that reason and for no other.
    if not jx_int_in_range(len(keep), len(marks), len(marks)):
        problems.append({"kind": "duplicate-key", "path": [], "key": "",
                         "offset": -1, "token": "",
                         "detail": "the duplicate-key record and the objects it "
                                   "refers to disagree in cardinality, so a path in "
                                   "this report may name the wrong object"})
    return value, problems


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
    # Added in v7.  The v6 table called itself the operator space and omitted
    # these; the independent reviewer found the omission and it is not cosmetic,
    # because every adopter is told to copy `wire_comparison_scan` and drive its
    # count to zero over a model that inherits whatever this table forgets.
    ("OP-TRUTHY", "if x:", "jx_type", lambda: bool(1) == bool(1.0) == bool(True),
     lambda: jx_equal(jx_type(1), jx_type(1.0)) or jx_equal(jx_type(1), jx_type(True))),
    ("OP-TRUTHY-ZERO", "if not x:", "jx_type",
     lambda: bool(0) == bool(0.0) == bool(False),
     lambda: jx_equal(jx_type(0), jx_type(0.0)) or jx_equal(jx_type(0), jx_type(False))),
    ("OP-PERCENT-D", "'%d' % x", "jx_canon",
     lambda: "%d" % 1 == "%d" % 1.0 == "%d" % True,
     lambda: jx_equal(jx_canon(1), jx_canon(1.0)) or jx_equal(jx_canon(1), jx_canon(True))),
    ("OP-DUPLICATE-KEY", 'json.loads(\'{"a":1,"a":2}\')', "jx_loads",
     lambda: jx_equal(json.loads('{"a": 1.0, "a": 1}'), json.loads('{"a": 1}')),
     lambda: jx_int_in_range(len(jx_loads('{"a": 1.0, "a": 1}')[1]), 0, 0)),
    ("OP-NONRFC", "json.loads('NaN')", "jx_loads",
     lambda: jx_type(json.loads("NaN")) == "number",
     lambda: jx_int_in_range(len(jx_loads("NaN")[1]), 0, 0)),
    ("OP-NUMBER-TEXT", "json.loads('-0')", "jx_loads",
     lambda: jx_equal(json.loads("-0"), 0) and jx_type(json.loads("-0")) == "integer",
     lambda: jx_int_in_range(len(jx_loads("-0")[1]), 0, 0)),
)

# Row ids whose hazard is demonstrated through a Call rather than an operator,
# so a scan that only walks ast.Compare cannot see them by construction.
OPERATOR_SPACE_CALL_SHAPED = ("OP-IN-DICTKEY", "OP-DISJOINT", "OP-DIFFERENCE",
                              "OP-DEDUP", "OP-DICT-COLLAPSE", "OP-GETITEM",
                              "OP-COUNT", "OP-INDEX", "OP-SORTED", "OP-MINMAX",
                              "OP-SUM", "OP-TRUTHY", "OP-TRUTHY-ZERO",
                              "OP-DUPLICATE-KEY", "OP-NONRFC", "OP-NUMBER-TEXT")

# Texts whose BYTES and PARSE disagree, each with the kind `jx_loads` must
# report and a control that must produce nothing.  Executed on every run.
JX_PARSE_CORPUS = (
    ("duplicate at the root", '{"version": 6.0, "version": 6}', "duplicate-key",
     "version"),
    ("duplicate one level down", '{"a": {"n": 1.0, "n": 1}}', "duplicate-key", "a/n"),
    ("duplicate inside an array element", '[{"k": true, "k": 1}]', "duplicate-key",
     "0/k"),
    ("duplicate repeated three times", '{"z": 1, "z": 2, "z": 3}', "duplicate-key", "z"),
    ("duplicate whose two values are equal", '{"q": 1, "q": 1}', "duplicate-key", "q"),
    ("NaN", '{"a": NaN}', "non-rfc-constant", "NaN"),
    ("Infinity", '{"a": Infinity}', "non-rfc-constant", "Infinity"),
    ("negative Infinity", '{"a": -Infinity}', "non-rfc-constant", "-Infinity"),
    ("negative zero spelled as an integer", '{"a": -0}', "number-text", "-0"),
    ("exponent notation", '{"a": 1E2}', "number-text", "1E2"),
    ("trailing zero in a fraction", '{"a": 1.10}', "number-text", "1.10"),
    ("a number that overflows to infinity", '{"a": 1e400}', "number-text", "1e400"),
    ("CONTROL: the same keys, no duplicate", '{"version": 6, "a": {"n": 1}}', "", ""),
    ("CONTROL: a canonical float", '{"a": 6.0, "b": -1, "c": 0}', "", ""),
    ("CONTROL: numbers inside strings", '{"a": "1E2", "b": "-0", "c": "\\"x\\": 1"}',
     "", ""),
)

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
            # v7: ordering agrees with equality at every pair, and the two
            # divergences v6 carried are gone rather than disclosed.
            ("jx_order/signed-zero", lambda: jx_order(0.0, -0.0), None),
            ("jx_order/nan-against-a-float", lambda: jx_order(float("nan"), 1.0), None),
            ("jx_order/nan-reflexive", lambda: jx_order(float("nan"), float("nan")), 0),
            ("jx_order/array", lambda: jx_order([1], [1]), 0),
            ("jx_order/array-distinct", lambda: jx_order([1], [2]), None),
            ("jx_le/signed-zero", lambda: jx_le(0.0, -0.0), False),
            ("jx_ge/signed-zero", lambda: jx_ge(0.0, -0.0), False),
            # v7: the two functions v6's own adoption instructions named and did
            # not define.  Token order is not value order, so these are real
            # replacements for min/max and not aliases for jx_sorted.
            ("jx_min/mixed", lambda: jx_min([1, 1.0])[0], None),
            ("jx_min/negative", lambda: jx_min([3, -5, 2])[0], -5),
            ("jx_min/token-order-is-not-value-order",
             lambda: jx_equal(jx_min([3, -5])[0], jx_sorted([3, -5])[0]), False),
            ("jx_min/empty", lambda: jx_min([])[0], None),
            ("jx_min/objects", lambda: jx_min([{"a": 1}, {"a": 2}])[0], None),
            ("jx_min/nan", lambda: jx_min([1.0, float("nan")])[0], None),
            ("jx_min/strings", lambda: jx_min(["b", "a"])[0], "a"),
            ("jx_max/mixed", lambda: jx_max([1, 1.0])[0], None),
            ("jx_max/negative", lambda: jx_max([3, -5, 2])[0], 3),
            ("jx_max/token-order-is-not-value-order",
             lambda: jx_equal(jx_max([-5, 3])[0], jx_sorted([-5, 3])[-1]), False),
            ("jx_max/empty", lambda: jx_max([])[0], None),
            ("jx_max/nan", lambda: jx_max([1.0, float("nan")])[0], None),
            ("jx_max/boolean-is-not-an-integer", lambda: jx_max([1, True])[0], None),
            # v7: the parse.  IR-C2V6-01.
            ("jx_loads/duplicate", lambda: jx_int_in_range(
                len(jx_loads('{"a": 1.0, "a": 1}')[1]), 1, 10 ** 6), True),
            ("jx_loads/duplicate-names-the-key", lambda: jx_loads(
                '{"a": 1.0, "a": 1}')[1][0]["key"], "a"),
            ("jx_loads/duplicate-names-the-kind", lambda: jx_loads(
                '{"a": 1.0, "a": 1}')[1][0]["kind"], "duplicate-key"),
            ("jx_loads/duplicate-path-at-depth", lambda: jx_loads(
                '{"o": {"a": 1, "a": 2}}')[1][0]["path"], ["o", "a"]),
            ("jx_loads/duplicate-path-in-an-array", lambda: jx_loads(
                '[{"a": 1, "a": 2}]')[1][0]["path"], [0, "a"]),
            ("jx_loads/parse-is-still-the-host-parse", lambda: jx_equal(
                jx_loads('{"a": 1.0, "a": 1}')[0],
                json.loads('{"a": 1}', object_pairs_hook=jx_refusing_pairs)), True),
            ("jx_loads/non-rfc", lambda: jx_loads("NaN")[1][0]["kind"],
             "non-rfc-constant"),
            ("jx_loads/number-text", lambda: jx_loads("-0")[1][0]["kind"],
             "number-text"),
            ("jx_loads/control", lambda: jx_int_in_range(
                len(jx_loads('{"a": 1, "b": 6.0, "c": "1E2"}')[1]), 0, 0), True),
            ("jx_number_tokens/outside-strings",
             lambda: jx_number_tokens('{"a": 1, "b": "2"}'), [[6, "1"]]),
            ("jx_number_tokens/escaped-quote",
             lambda: jx_number_tokens('{"a": "\\" 9", "b": 1}'), [[19, "1"]]),
            ("jx_number_tokens/exponent",
             lambda: jx_number_tokens("[1e-5]"), [[1, "1e-5"]]),
            # v8: the total leaf census and the total binding.  IR-C2V7-01.
            # Every one of these is a case where v7's two type-named walkers
            # returned nothing and this census returns the leaf.
            ("jx_leaf_census/boolean-is-a-leaf",
             lambda: jx_leaf_census({"a": True}), [[["a"], "boolean"]]),
            ("jx_leaf_census/null-is-a-leaf",
             lambda: jx_leaf_census({"a": None}), [[["a"], "null"]]),
            ("jx_leaf_census/string-is-a-leaf",
             lambda: jx_leaf_census({"a": "x"}), [[["a"], "string"]]),
            ("jx_leaf_census/integer-and-number-are-distinct-leaves",
             lambda: jx_leaf_census([1, 1.0]), [[[0], "integer"], [[1], "number"]]),
            ("jx_leaf_census/descends-through-both-containers",
             lambda: jx_leaf_census({"a": [{"b": False}]}), [[["a", 0, "b"], "boolean"]]),
            ("jx_leaf_census/an-empty-container-holds-no-leaf",
             lambda: jx_leaf_census({"a": [], "b": {}}), []),
            ("jx_leaf_census/depth-4000-is-not-a-recursion-error",
             lambda: len(jx_leaf_census(_jx_deep_witness(4000))), 1),
            ("jx_walk/depth-4000-is-not-a-recursion-error",
             lambda: len(jx_walk(_jx_deep_witness(4000))), 4001),
            ("jx_walk/reports-containers-too",
             lambda: len(jx_walk({"a": [1]})), 3),
            ("jx_bind_value/boolean-against-boolean",
             lambda: jx_bind_value(True, True) is None, True),
            ("jx_bind_value/boolean-drift", lambda: jx_bind_value(False, True) is None,
             False),
            ("jx_bind_value/integer-spelling-of-a-boolean",
             lambda: jx_bind_value(1, True) is None, False),
            ("jx_bind_value/boolean-spelling-of-an-integer",
             lambda: jx_bind_value(True, 1) is None, False),
            ("jx_bind_value/null-against-null",
             lambda: jx_bind_value(None, None) is None, True),
            ("jx_bind_value/null-against-a-boolean",
             lambda: jx_bind_value(None, False) is None, False),
            ("jx_bind_value/float", lambda: jx_bind_value(2538.0, 2538) is None, False),
            ("jx_bind_value/signed-zero",
             lambda: jx_bind_value(-0.0, 0.0) is None, False),
            ("jx_bind_value/string", lambda: jx_bind_value("a", "a") is None, True),
            ("jx_bind_value/refuses-a-container",
             lambda: jx_bind_value([1], [1]) is None, False),
            ("jx_type_space/every-declared-type-is-witnessed",
             lambda: jx_type_space()["unwitnessed"], 0),
            ("jx_type_space/the-census-splits-the-space-in-two",
             lambda: jx_type_space()["containers"] + jx_type_space()["scalars"],
             len(JX_TYPES)),
            ("jx_type_space/containers-are-exactly-array-and-object",
             lambda: jx_type_space()["containerTypes"], ["array", "object"]),
            # OBS-C2V8-01.  The witness is read back AT DEPTH, not at one fixed
            # shallow key, and the depth-narrowed census the v8 reviewer built
            # is exactly what these two rows refuse.
            ("jx_type_space/every-witness-is-placed-at-every-declared-depth",
             lambda: jx_type_space()["placements"],
             len(JX_TYPE_WITNESSES) * len(JX_TYPE_SPACE_PLACEMENTS)),
            ("jx_place/a-witness-twelve-objects-deep-is-still-one-leaf",
             lambda: jx_leaf_census(_jx_place(True, 12, False)[0]), [[
                 ["probe11", "probe10", "probe9", "probe8", "probe7", "probe6",
                  "probe5", "probe4", "probe3", "probe2", "probe1", "probe0"],
                 "boolean"]]),
            # OBS-C2V8-07.  The production table is a MEASUREMENT over parsed
            # JSON text, so an eighth production nothing realises is named.
            ("jx_rfc_production_space/realises-exactly-the-declared-productions",
             lambda: jx_sorted(list(jx_rfc_production_space()["measured"])),
             jx_sorted(jx_unique([name for name, _r in JX_RFC8259_PRODUCTIONS]))),
            ("jx_rfc_production_space/the-number-production-refines-into-two-types",
             lambda: jx_get(jx_rfc_production_space()["measured"], "number"),
             jx_sorted(["integer", "number"])),
            ("jx_rfc_production_space/a-name-that-is-not-a-grammar-shape",
             lambda: _jx_rfc_production("date"), JX_UNSUPPORTED),
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

    # v7.  ORDERING AND EQUALITY MUST AGREE AT EVERY PAIR.  v6 disclosed that
    # `jx_order` called 0.0 and -0.0 equal, and NaN equal to every float, while
    # `jx_equal` called both distinct -- and disclosed only the equality half of
    # that.  A divergence that is measured every run cannot be forgotten, and a
    # divergence that is zero is better than one that is documented.
    order_equality_divergences = 0
    order_pairs = 0
    for a in corpus:
        for b in corpus:
            order_pairs += 1
            try:
                agrees = (jx_order(a, b) == 0) is jx_equal(a, b)
            except Exception as exc:                        # noqa: BLE001 - measured
                order_equality_divergences += 1
                escapes.append("jx_order raised " + type(exc).__name__ + " on " +
                               repr(a) + " and " + repr(b))
                continue
            if not agrees:
                order_equality_divergences += 1
                escapes.append("jx_order and jx_equal disagree at " + repr(a) + " and " +
                               repr(b) + ": ordering says " + repr(jx_order(a, b)) +
                               " and equality says " + repr(jx_equal(a, b)) + "; a gate "
                               "with two answers to one question is not a gate")

    # v7.  THE PARSE.  Every text whose bytes and parse disagree must be
    # reported by `jx_loads` under the declared kind and at the declared
    # position, and every control must produce nothing.  This is the executable
    # half of the IR-C2V6-01 repair and it lives inside the primitive so that an
    # adopting checker gets it by copying the block.
    parse_cases = parse_named = parse_admitted = parse_controls = 0
    for label, text, kind, position in JX_PARSE_CORPUS:
        parse_cases += 1
        try:
            _value, problems = jx_loads(text)
        except Exception as exc:                            # noqa: BLE001 - measured
            parse_admitted += 1
            escapes.append("jx_loads raised " + type(exc).__name__ + " on the parse "
                           "corpus case " + label + "; a parse gate that raises "
                           "instead of reporting cannot name a position")
            continue
        if not kind:
            parse_controls += 1
            if problems:
                parse_admitted += 1
                escapes.append("the parse corpus CONTROL " + label + " was refused: " +
                               repr(problems[0]) + "; a probe that refuses its own "
                               "control is not an oracle")
            continue
        hit = [item for item in problems
               if jx_equal(item["kind"], kind) and
               jx_equal("/".join(str(step) for step in item["path"]) or item["key"],
                        position)]
        if hit:
            parse_named += 1
        else:
            parse_admitted += 1
            escapes.append("the parse corpus case " + label + " was ADMITTED: jx_loads "
                           "reported " + repr(problems) + ", none of which is a " +
                           kind + " at " + position)

    # v8.  THE TYPE SPACE, MEASURED.  IR-C2V7-01.  Everything above measures
    # what the primitive does with a value it is given; this measures that the
    # set of values it can be given is the JSON data model's and not a list.
    # `jx_type_space` reports its own disagreements, and they are escapes here
    # for the same reason a token collision is: a totality whose type coverage
    # is wrong is not a weaker totality, it is a different one.
    space = jx_type_space()
    for item in space["escapes"]:
        escapes.append("type space: " + item)
    # The census must reach every scalar type as a LEAF, not merely realise it.
    # This is the positive half: a census narrowed the way v7's was would still
    # realise `boolean` here and would stop reporting it as a leaf.
    type_space_cases = type_space_admissions = 0
    for kind in JX_TYPES:
        type_space_cases += 1
        expected_leaf = jx_in(kind, space["scalarTypes"])
        expected_container = jx_in(kind, space["containerTypes"])
        if not expected_leaf and not expected_container:
            type_space_admissions += 1
            escapes.append("the JSON type " + repr(kind) + " is neither a leaf nor a "
                           "container of the leaf census, so a document holding one "
                           "would have a leaf no totality built on the census can see")

    # v7.  A declared table that names a row id no row carries is the same
    # defect as an adoption step that names a function that does not exist.
    declared_call_shaped = 0
    row_ids = [row[0] for row in OPERATOR_SPACE]
    for row_id in OPERATOR_SPACE_CALL_SHAPED:
        declared_call_shaped += 1
        if not jx_in(row_id, row_ids):
            escapes.append("OPERATOR_SPACE_CALL_SHAPED declares " + row_id +
                           ", which is not a row of OPERATOR_SPACE")

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

    # v7.  The parse entry points take TEXT.  Handing them a value that has
    # already been parsed is the mistake that makes a duplicate-key defence
    # vacuous, so it is refused by name rather than silently accepted.
    for entry, produce in (("jx_loads", lambda item: jx_loads(item)),
                           ("jx_number_tokens", lambda item: jx_number_tokens(item))):
        for outside in ({"a": 1}, [1], 1, None, b"{}"):
            try:
                produce(outside)
                escapes.append(entry + " accepted an already-parsed " +
                               type(outside).__name__ + " instead of document TEXT; a "
                               "parse gate handed a parse is vacuous")
            except JxDomainError:
                continue
            except Exception as exc:                    # noqa: BLE001 - measured
                escapes.append(entry + " raised " + type(exc).__name__ + " rather than "
                               "a named domain refusal on a " + type(outside).__name__)

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
        "orderPairs": order_pairs,
        "orderEqualityDivergences": order_equality_divergences,
        "parseCases": parse_cases,
        "parseControls": parse_controls,
        "parseNamedAtThePosition": parse_named,
        "parseAdmissions": parse_admitted,
        "callShapedRowsDeclared": declared_call_shaped,
        "typeSpaceWitnesses": space["witnesses"],
        "typeSpaceDeclaredTypes": space["declaredTypes"],
        "typeSpaceRealisedTypes": space["types"],
        "typeSpaceContainerTypes": space["containers"],
        "typeSpaceScalarTypes": space["scalars"],
        "typeSpaceUnwitnessedTypes": space["unwitnessed"],
        "typeSpaceRfcProductions": space["rfcProductions"],
        "typeSpaceCases": type_space_cases,
        "typeSpaceAdmissions": type_space_admissions,
        "typeSpacePlacements": space["placements"],
        "typeSpaceGrammarTexts": space["grammarTexts"],
        "typeSpaceGrammarProductions": space["grammarProductions"],
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
V6_CHECKER = "check-c2-v6.py"
V6_CONTRACT = "c2-plan-stage-schema.v6.json"
V6_REVIEW = "c2-plan-stage-schema.v6.review-independent.json"
V7_CHECKER = "check-c2-v7.py"
V7_CONTRACT = "c2-plan-stage-schema.v7.json"
V7_REVIEW = "c2-plan-stage-schema.v7.review-independent.json"
V8_CHECKER = "check-c2-v8.py"
V8_CONTRACT = "c2-plan-stage-schema.v8.json"
V8_REVIEW = "c2-plan-stage-schema.v8.review-independent.json"
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
    V6_CHECKER: "08c283d45c42e9e53781197e5b7cab5b22213a0ebdddc3a90d3a6b1da55ba9d6",
    V6_CONTRACT: "f9c25ccba272c8306610dd1f3886b0449cf554a369a3e91d0e01cec05faa8786",
    V6_REVIEW: "cb2e50e19e38fb786990852758a29d7fb1479688fe81f5851b926e09b448b13b",
    V7_CHECKER: "d96faeee9e26abcca518c08a1a1399642dbe9ff2e452a60058e455d912b900c7",
    V7_CONTRACT: "51da54489618cc8af5946686e6b0a8a84d5725f421e7aa5ea3f8ecf8747906d1",
    V7_REVIEW: "eaeb43b4a912da253518b88500757c852391e2f6846927defd5048f2bc5d0622",
    V8_CHECKER: "b1470e788cad17fef4f4526a50f026d1a0402a9b485d108ca1f444c2d1360d11",
    V8_CONTRACT: "a7e309d4a58a89e117c0b84d06eccb093e1f087d4dcf8ff116062b754d7ec353",
    V8_REVIEW: "ae90724fb972bd16e6e1979d1777d190c80dcd6bf2747a0d7ed659c20eb5d785",
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
# load, not reported.  v8 discharges TWO dispositions and both are pinned.
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
V6_REVIEW_BINDING = {
    "artifact": "opensip.c2-plan-stage-schema.v6.review-independent",
}
# The ONE blocking finding of the v6 REJECT.  v8 exists to discharge it, and
# refuses to run against a softened version of it for exactly the reason v6
# refused to run against a softened IR-C2V4-01.
V6_BLOCKER_IDS = ("IR-C2V6-01",)
V7_REVIEW_BINDING = {
    "artifact": "opensip.c2-plan-stage-schema.v7.review-independent",
}
# The ONE blocking finding of the v7 REJECT.  v8 exists to discharge it and to
# repair the ten non-blocking findings recorded with it, and it refuses to run
# against a softened version of it for the same reason every predecessor did.
V7_BLOCKER_IDS = ("IR-C2V7-01",)
V8_REVIEW_BINDING = {
    "artifact": "opensip.c2-plan-stage-schema.v8.review-independent",
}
# The ONE blocking finding of the v8 REJECT.  IR-C2V8-01: `document_skeleton`
# hashed a `/`-JOIN of the path, which is not injective, so a narrative leaf
# reparented across a `/` boundary left the digest and every count unchanged.
# v9 exists to discharge it and refuses to run against a softened version of
# it, exactly as every predecessor did.
V8_BLOCKER_IDS = ("IR-C2V8-01",)
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
    "jx_min", "jx_max", "jx_sum_int", "jx_bind", "jx_bind_text",
    "jx_loads", "jx_number_tokens",
    # v8's four new gates.  The first three are the repair for IR-C2V7-01: the
    # walk that reaches every leaf without naming a scalar type, the walk that
    # reaches every node, and the binding that works at every JSON type rather
    # than at the two somebody specialised for.  The fourth is the measurement
    # that says the first is total over the data model.
    "jx_leaf_census", "jx_walk", "jx_bind_value", "jx_type_space",
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
        # L8.  The candidate's BYTES, and what this run read out of them before
        # anything downstream saw a parsed object.  `external` holds results
        # that are a pure function of hash-verified bytes AND of nothing this
        # file can change, so unlike `pinned` it is not cleared by a mutation.
        self.parse_findings = []
        self.parse_scan = None
        self.parse_probe = None
        self.parse_differential = None
        self.candidate_digest = "not-read-as-bytes"
        self.candidate_bytes = 0
        self.external = {}
        self.declared_strings = None
        self.truthiness = None
        # v8.  L2c is now a TOTAL leaf ledger rather than two type-named
        # walkers, and L6d is the differential against the pinned v7's own
        # enumeration.  IR-C2V7-01.
        self.type_space = None
        self.candidate_ledger = None
        self.candidate_totality = {"executedCases": 0, "namedRejections": 0,
                                   "admissions": 0, "namedBySkeletonOnly": 0,
                                   "localisedToASubtree": 0,
                                   "typesCovered": 0, "escapes": []}
        # v9.  IR-C2V8-01: path identity, and the census measured against the
        # node walk over the real document rather than at one shallow probe.
        self.path_identity = {"pairs": 0, "collidesUnderTheJoinedText": 0,
                              "separatesUnderTheCanonicalToken": 0, "stepPairs": 0,
                              "stepPairsCollidingUnderTheJoinedText": 0,
                              "stepPairsSeparatedByTheCanonicalToken": 0, "nodes": 0,
                              "pathsInverted": 0, "distinctPathTokens": 0,
                              "distinctJoinedTexts": 0, "escapes": []}
        self.census_agreement = {"walkNodes": 0, "walkLeaves": 0, "censusLeaves": 0,
                                 "agreed": 0, "escapes": []}
        self.skeleton_differential = None
        self.root_subtrees = 0
        self.enumeration_differential = None
        self.parse_depth = None
        self.pinned_number_tokens = None

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

    # EVERY JSON input this checker loads goes through the SAME parse, not only
    # the one it calls the candidate.  IR-C2V6-01 is a parser defect, and a
    # parser defence applied to one input and not to its siblings is exactly the
    # list-of-places failure this lineage exists to escape.  A pinned input is
    # hash-verified, so a duplicate key here can only mean the pin table was
    # updated to match a tampered file -- which is the fail-closed vector this
    # corpus already drives -- and it is refused at load with a distinct code.
    parsed: dict[str, object] = {}
    for name in sorted(PINS):
        if name.endswith(".json"):
            try:
                value, problems = jx_loads(snapshots[name].decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError, JxDomainError) as exc:
                raise AuthorityLoadError(
                    "cannot parse pinned data " + name + ": " + type(exc).__name__) from exc
            if problems:
                raise AuthorityLoadError(
                    "pinned input " + name + " does not say the same thing to a reader "
                    "as to this instrument: " + str(len(problems)) + " byte/parse "
                    "divergence(s), the first being a " + str(problems[0]["kind"]) +
                    " at " + _parse_problem_position(problems[0]) + " (" +
                    str(problems[0]["detail"]) + ")")
            parsed[name] = value

    _refuse_softened_provenance(parsed)

    sink = io.StringIO()
    with redirect_stdout(sink):
        v4 = _execute_snapshot("opensip_c2v9_pinned_v4_checker", V4_CHECKER,
                               snapshots[V4_CHECKER], directory)
        v4._OWN_TREE_CACHE = ast.parse(snapshots[V4_CHECKER])
        v3_module = v4._execute_snapshot("opensip_c2v9_pinned_v3_checker", V3_CHECKER,
                                         snapshots[V3_CHECKER])
    _refuse_pin_table_disagreement(v4)
    v4_authority = v4.Authority(dict(snapshots), dict(parsed), {V3_CHECKER: v3_module})
    return Authority(snapshots, parsed, v4, v4_authority, directory)


def _refuse_softened_provenance(parsed) -> None:
    """Both dispositions v8 discharges are read from pinned bytes, by name."""
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
    # The v6 REJECT.  v8 exists to discharge ONE blocking finding and refuses to
    # run against a softened version of it, for the reason v6 refused to run
    # against a softened IR-C2V4-01: a repair lane pointed at a softened
    # disposition is repairing something else.
    v6_review = parsed.get(V6_REVIEW)
    if jx_type(v6_review) != "object":
        raise AuthorityLoadError("pinned review " + V6_REVIEW + " is not a JSON object")
    for key in sorted(V6_REVIEW_BINDING):
        if jx_bind_text(v6_review.get(key), V6_REVIEW_BINDING[key]) is not None:
            raise AuthorityLoadError(
                "pinned review " + V6_REVIEW + " carries " + key + "=" +
                repr(v6_review.get(key)) + ", not " + repr(V6_REVIEW_BINDING[key]))
    v6_verdict = v6_review.get("verdict")
    if jx_type(v6_verdict) != "string" or "REJECT" not in v6_verdict:
        raise AuthorityLoadError(
            "pinned review " + V6_REVIEW + " no longer carries the REJECT verdict this "
            "successor exists to repair")
    v6_blockers = v6_review.get("blockers")
    v6_blockers = v6_blockers if jx_type(v6_blockers) == "array" else []
    v6_graded = [item for item in v6_blockers if jx_type(item) == "object"]
    for name in V6_BLOCKER_IDS:
        rows = [item for item in v6_graded if jx_equal(item.get("id"), name)]
        if not rows or jx_bind_text(rows[0].get("severity"), "BLOCKING") is not None:
            raise AuthorityLoadError(
                "pinned review " + V6_REVIEW + " no longer grades " + name + " BLOCKING; "
                "this successor refuses to run against a softened disposition")
    # The v7 REJECT.  IR-C2V7-01 is the finding this successor exists to
    # discharge: v7's candidate totality enumerated integer and JSON number
    # leaves and not BOOLEAN leaves, so a one-byte flip of the document's own
    # claim that this lane reproduced IR-C2V6-01 reached a full green run.
    v7_review = parsed.get(V7_REVIEW)
    if jx_type(v7_review) != "object":
        raise AuthorityLoadError("pinned review " + V7_REVIEW + " is not a JSON object")
    for key in sorted(V7_REVIEW_BINDING):
        if jx_bind_text(v7_review.get(key), V7_REVIEW_BINDING[key]) is not None:
            raise AuthorityLoadError(
                "pinned review " + V7_REVIEW + " carries " + key + "=" +
                repr(v7_review.get(key)) + ", not " + repr(V7_REVIEW_BINDING[key]))
    v7_verdict = v7_review.get("verdict")
    if jx_type(v7_verdict) != "string" or "REJECT" not in v7_verdict:
        raise AuthorityLoadError(
            "pinned review " + V7_REVIEW + " no longer carries the REJECT verdict this "
            "successor exists to repair")
    v7_blockers = v7_review.get("blockers")
    v7_blockers = v7_blockers if jx_type(v7_blockers) == "array" else []
    v7_graded = [item for item in v7_blockers if jx_type(item) == "object"]
    for name in V7_BLOCKER_IDS:
        rows = [item for item in v7_graded if jx_equal(item.get("id"), name)]
        if not rows or jx_bind_text(rows[0].get("severity"), "BLOCKING") is not None:
            raise AuthorityLoadError(
                "pinned review " + V7_REVIEW + " no longer grades " + name + " BLOCKING; "
                "this successor refuses to run against a softened disposition")
    # The v8 REJECT.  IR-C2V8-01 is the finding this successor exists to
    # discharge: v8's skeleton bound a LOSSY ENCODING of a node's path, so one
    # contiguous +11-byte edit relocating a narrative leaf across a `/`
    # boundary left documentSkeleton.sha256 and every published count
    # byte-identical and reached a full green banner.
    v8_review = parsed.get(V8_REVIEW)
    if jx_type(v8_review) != "object":
        raise AuthorityLoadError("pinned review " + V8_REVIEW + " is not a JSON object")
    for key in sorted(V8_REVIEW_BINDING):
        if jx_bind_text(v8_review.get(key), V8_REVIEW_BINDING[key]) is not None:
            raise AuthorityLoadError(
                "pinned review " + V8_REVIEW + " carries " + key + "=" +
                repr(v8_review.get(key)) + ", not " + repr(V8_REVIEW_BINDING[key]))
    v8_verdict = v8_review.get("verdict")
    if jx_type(v8_verdict) != "string" or "REJECT" not in v8_verdict:
        raise AuthorityLoadError(
            "pinned review " + V8_REVIEW + " no longer carries the REJECT verdict this "
            "successor exists to repair")
    v8_blockers = v8_review.get("blockers")
    v8_blockers = v8_blockers if jx_type(v8_blockers) == "array" else []
    v8_graded = [item for item in v8_blockers if jx_type(item) == "object"]
    for name in V8_BLOCKER_IDS:
        rows = [item for item in v8_graded if jx_equal(item.get("id"), name)]
        if not rows or jx_bind_text(rows[0].get("severity"), "BLOCKING") is not None:
            raise AuthorityLoadError(
                "pinned review " + V8_REVIEW + " no longer grades " + name + " BLOCKING; "
                "this successor refuses to run against a softened disposition")
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
                                 ", v9 pins " + repr(jx_get(PINS, name)))
    if disagreements:
        raise AuthorityLoadError("pin tables disagree - " + "; ".join(disagreements))
    unshared = jx_sorted(jx_difference(list(inherited), list(PINS)))
    if unshared:
        raise AuthorityLoadError(
            "the predecessor depends on inputs this successor does not record, which "
            "would break the recording obligation: " + repr(unshared))


# =============================================================================
# Section 2b.  L8 -- PARSE INTEGRITY.  The repair for IR-C2V6-01.
#
# The v6 REJECT is one blocking finding and it is not about the comparison
# primitive at all.  `jx_canon` survived a direct attack -- 82,368 distinct
# tokens of hostile and random input, 0 collisions -- and it was never the thing
# that failed.  What failed is that EVERY LAYER OF v6 OPERATES ON THE PARSED
# OBJECT AND NOTHING READ THE CANDIDATE'S RAW BYTES.  Eighteen bytes inserted
# into c2-plan-stage-schema.v6.json put `"version": 6.0` into the document of
# record while `json.loads` handed every instrument the unedited `6`, and
# check-c2-v6.py printed a full green banner certifying that 105 integer leaves
# of THIS document were bound with no unbound bucket.
#
# The class is wider than duplicate keys.  It is "the bytes on disk and the
# object every guard reads are different documents".  What L8 covers:
#
#   duplicate-key        every duplicated key, at any depth, in EVERY input this
#                        checker parses, reported by a NAMED FINDING AT ITS PATH
#   non-rfc-constant     NaN / Infinity / -Infinity, which are not JSON
#   number-text          a number token whose bytes are not the canonical
#                        spelling of the value the parser produces (`-0`, `1E2`)
#   no bare parse        a STRUCTURAL scan of this file's own tree: every
#                        json.load/json.loads call must pass an object_pairs_hook
#   bytes of record      the sha256 of the exact candidate bytes that were
#                        parsed is computed here and printed in the banner, so
#                        the verdict names the bytes it is a verdict about
#
# What L8 does NOT cover is in the contract's L8 blindSpots and in RES-C2V9-08,
# RES-C2V9-12 and RES-C2V9-13: string-escape spellings; the parses performed
# INSIDE the pinned predecessor checkers, which are their own reviewed bytes and
# are not v8's to change; a parse reached through a name computed at run time,
# which the scan is syntactic about and now COUNTS two shapes of rather than
# leaving to a counter binding (OBS-C2V7-01); and nesting deeper than the depth
# the duplicate-key claim is executed at, which is published rather than left as
# the word "any" (IR-C2V7-02).
# =============================================================================

# (id, pinned document, the line to duplicate, the shadowing line to insert
#  BEFORE it, the position v8 must name, note)
PARSE_DIFFERENTIAL_VECTORS = (
    ("IR-C2V6-01-duplicate-key-at-version", V6_CONTRACT,
     '  "version": 6,\n', '  "version": 6.0,\n', "version",
     "the v6 REJECT's own minimal reproduction: eighteen bytes, no source "
     "modification, exit 0 and a full green banner from check-c2-v6.py"),
    ("IR-C2V6-01-replicated-on-the-v5-document", V5_CONTRACT,
     '  "version": 5,\n', '  "version": 5.0,\n', "version",
     "the same eighteen-byte shape against the REJECTED v5 document, so the "
     "class is shown not to be specific to one candidate"),
    ("IR-C2V6-01-replicated-on-the-verified-predecessor", V4_CONTRACT,
     '  "version": 4,\n', '  "version": 4.0,\n', "version",
     "and against the VERIFIED PREDECESSOR, whose bytes the whole derivation "
     "rests on"),
)

_PARSE_FINDING_IDS = {"duplicate-key": "C2V9-DUPKEY",
                      "non-rfc-constant": "C2V9-NONRFC",
                      "number-text": "C2V9-NUMBER-TEXT"}


def _parse_problem_position(problem) -> str:
    """The position of a byte/parse divergence, as text.

    A duplicate key has a PATH; a non-RFC constant and a non-canonical number
    token have a byte OFFSET and the token itself.  Every kind has a position,
    because `a non-zero exit is not evidence a guard fired` applies here too and
    an assertion has to have something to assert against.
    """
    steps = problem.get("path")
    steps = steps if jx_type(steps) == "array" else []
    if steps:
        return "/".join(str(step) for step in steps)
    key = problem.get("key")
    if jx_type(key) == "string" and key:
        return key
    return "offset " + str(problem.get("offset"))


def parse_problem_findings(problems, label) -> list:
    """L8's findings.  One per divergence, named, at its position."""
    findings = []
    for problem in problems:
        kind = problem.get("kind")
        prefix = jx_get(_PARSE_FINDING_IDS, kind, "C2V9-PARSE")
        findings.append(
            prefix + ": " + _parse_problem_position(problem) + " in " + str(label) +
            " " + str(problem.get("detail")) + "; the bytes of record and the object "
            "every layer of this checker reads are then different documents, which is "
            "IR-C2V6-01 and is invisible to every guard that reads only the parse")
    return findings


# STATED CORRECTLY, BECAUSE v7 STATED IT WRONGLY (OBS-C2V7-02).  v7's comment
# here read "The ONLY places this file is permitted to parse JSON the way the
# REJECTED predecessor does ... Both exist to reproduce the predecessor's own
# behaviour", and its contract said "two exemptions".  There are TWO EXEMPTION
# CLASSES, not two call sites, and they account for eight unhooked parses:
#
#   PREDECESSOR-PARSE   the functions named below, which reproduce the
#                       predecessor's own unhooked parse as evidence
#   HAZARD-DEMO         the bare parses inside the OPERATOR_SPACE table, which
#                       demonstrate the host-language hazard live on every run
#
# Both classes are named, counted, published and BOUND, the banner prints the
# decomposition rather than a subtraction that does not add up, and the
# arithmetic identity hooked + hazard + predecessor + ungated == sites is itself
# a finding if it fails.  Anywhere else, a bare parse is a finding.
DECLARED_UNHOOKED_PARSE_FUNCTIONS = ("parse_differential",
                                     "pinned_v6_over_a_duplicate_key",
                                     "pinned_v7_over_a_boolean_flip",
                                     "pinned_v8_over_a_path_collision")

# OBS-C2V7-01, CLOSED rather than only disclosed.  `json_load_sites` matches an
# ast.Call whose func is an Attribute or a Name spelled load/loads.
# `json.JSONDecoder().decode(text)` and `getattr(json, "loads")(text)` are
# neither: against v7 both were real, bare, unhooked parses of caller input that
# the scan could not see and that changed no published counter.  L4 already
# treats its own analogous evasions this way -- it COUNTS eval, exec and
# getattr-dispatch and requires all but the two declared exec sites to be zero
# -- and L8 now does the same, instead of resting on a counter binding that
# happens to stop a different attack.  What remains DISCLOSED rather than closed
# is that the scan is still syntactic: RES-C2V9-12.
PARSE_EVASION_ATTRIBUTES = ("JSONDecoder", "raw_decode", "scanstring")
# The predecessors that PREDATE the IR-C2V6-01 repair, and whose zero hooked
# parses are the external anchor L8's differential is measured against.
PARSE_UNHOOKED_PREDECESSORS = (V4_CHECKER, V5_CHECKER, V6_CHECKER)
PARSE_EVASION_GETATTR_NAMES = ("load", "loads", "JSONDecoder", "raw_decode")
PARSE_EVASION_DETECTOR_PROBE = (
    "value = json.JSONDecoder().decode(text)\n"
    "other = getattr(json, 'loads')(text)\n")


def json_parse_evasion_sites(tree) -> list:
    """Every syntactic evasion of `json_load_sites`, with its position."""
    out = []
    for node in ast.walk(tree):
        name = None
        if isinstance(node, ast.Attribute):
            name = node.attr
        elif isinstance(node, ast.Name):
            name = node.id
        if jx_in(name, list(PARSE_EVASION_ATTRIBUTES)):
            out.append({"line": getattr(node, "lineno", 0), "kind": "decoder-object",
                        "source": ast.unparse(node)[:160]})
            continue
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if not jx_equal(node.func.id, "getattr") or len(node.args) < 2:
            continue
        target = node.args[1]
        if not isinstance(target, ast.Constant) or jx_type(target.value) != "string":
            continue
        if jx_in(target.value, list(PARSE_EVASION_GETATTR_NAMES)):
            out.append({"line": getattr(node, "lineno", 0), "kind": "getattr-dispatch",
                        "source": ast.unparse(node)[:160]})
    return out


# IR-C2V7-02, MEASURED rather than described.  v7's duplicate-path walk was
# recursive and recursed ONLY when a duplicate had actually been recorded, so
# past nesting depth 1000 the one vector L8 exists to catch produced an uncaught
# RecursionError -- traceback, exit 1, ZERO findings -- while the same document
# WITHOUT a duplicate was handled gracefully by a sibling guard.  The banner said
# "every duplicate key at any depth".  The walk is iterative now and this probe
# executes the claim at a declared depth, so "any depth" is a number a reader
# can check rather than a word.
PARSE_DEPTH_PROBE_DEPTH = 4000


def parse_depth_probe(depth=PARSE_DEPTH_PROBE_DEPTH) -> dict:
    """Behavioural, reads no source.  A duplicate key nested `depth` objects
    deep must be a NAMED FINDING at its full path, and the control at the same
    depth must produce nothing."""
    escapes = []
    named = controls = 0
    text = '{"n": ' * depth + '{"dup": 1.0, "dup": 1}' + "}" * depth
    expected = "/".join(["n"] * depth + ["dup"])
    try:
        _value, problems = jx_loads(text)
        findings = parse_problem_findings(problems, "the depth probe")
    except BaseException as exc:                        # noqa: BLE001 - measured
        findings = []
        escapes.append("a duplicate key nested " + str(depth) + " objects deep raised " +
                       type(exc).__name__ + " instead of being named at its path; that "
                       "is IR-C2V7-02 verbatim, and a non-zero exit is not evidence a "
                       "guard fired")
    if [item for item in findings
            if item.startswith("C2V9-DUPKEY:") and expected in item]:
        named += 1
    elif not escapes:
        escapes.append("a duplicate key nested " + str(depth) + " objects deep produced " +
                       str(len(findings)) + " finding(s) and none names its path, so "
                       "the claim that every duplicate key at any depth is named is "
                       "false at this depth")
    control = '{"n": ' * depth + '{"dup": 1}' + "}" * depth
    try:
        _value, problems = jx_loads(control)
        if problems:
            escapes.append("the CONTROL at depth " + str(depth) + " was refused, so "
                           "this probe is not an oracle")
        else:
            controls += 1
    except BaseException as exc:                        # noqa: BLE001 - measured
        escapes.append("the CONTROL at depth " + str(depth) + " raised " +
                       type(exc).__name__)
    return {"depth": depth, "named": named, "controls": controls, "escapes": escapes}


def pinned_number_token_census(authority) -> dict:
    """The `960 tokens` figure, PUBLISHED because it is MEASURED.

    The v7 reviewer audited the number-token scanner hard -- 148 tokens over the
    candidate, 0 false positives, 0 false negatives, a 4000-case fuzz with 0
    failures -- and recorded that the brief's "960 tokens" figure, the total
    over the pinned .json inputs, is correct and appears in NEITHER artifact.  A
    measured figure that is not published is not evidence.  It is measured here
    on every run over the bytes this run verified, published, and bound, so it
    is a figure rather than a recollection.
    """
    cached = jx_get(authority.external, "pinned-number-tokens")
    if cached is not None:
        return cached
    total, files = 0, 0
    for name in jx_sorted(list(PINS)):
        if not name.endswith(".json"):
            continue
        files += 1
        total = total + len(jx_number_tokens(
            authority.snapshots[name].decode("utf-8")))
    result = {"files": files, "tokens": total}
    jx_put(authority.external, "pinned-number-tokens", result)
    return result


def json_load_sites(tree) -> list:
    """Every `json.load`/`json.loads` call, and whether it passes a real hook.

    This is the structural half of the repair and the reason it is not a list of
    places: a parse that refuses duplicate keys at ONE call site and not at its
    siblings is the failure this lineage exists to escape, so the property is
    asserted over the whole tree instead of over an enumeration.  Passing
    `object_pairs_hook=None` is NOT a hook -- it is the host default spelled out
    -- and is counted as bare, so the exemption cannot be bought with a keyword.
    """
    span = (0, 0)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "OPERATOR_SPACE"
                for target in node.targets):
            span = (getattr(node, "lineno", 0), getattr(node, "end_lineno", 0))
    declared = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                node.name in DECLARED_UNHOOKED_PARSE_FUNCTIONS:
            for child in ast.walk(node):
                declared[id(child)] = node.name
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = None
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
        elif isinstance(node.func, ast.Name):
            name = node.func.id
        if not jx_in(name, ["loads", "load"]):
            continue
        hooked = False
        for keyword in node.keywords:
            if not jx_equal(keyword.arg, "object_pairs_hook"):
                continue
            if isinstance(keyword.value, ast.Constant) and keyword.value.value is None:
                continue
            hooked = True
        line = getattr(node, "lineno", 0)
        out.append({"line": line, "source": ast.unparse(node)[:160], "hooked": hooked,
                    "inDeclaredHazardTable": jx_int_in_range(line, span[0], span[1]),
                    "inDeclaredPredecessorParse": id(node) in declared})
    return out


def parse_scan_findings(tree, authority) -> dict:
    """L8's structural scan over this file and over the pinned predecessors."""
    own = json_load_sites(tree)
    # A TRUE PARTITION, in declared priority order, so the four counts sum to the
    # site count exactly.  OBS-C2V7-02: v7 printed "11 parse call sites of which
    # 3 pass an object_pairs_hook and 0 do not", and 3 + 0 is not 11, because
    # `ungated` means "neither hooked nor declared-exempt" and the sentence
    # asserted the stronger and false thing.  Eight sites do not pass a hook.
    hooked = [site for site in own if site["hooked"]]
    hazard = [site for site in own
              if not site["hooked"] and site["inDeclaredHazardTable"]]
    reproductions = [site for site in own
                     if not site["hooked"] and not site["inDeclaredHazardTable"]
                     and site["inDeclaredPredecessorParse"]]
    ungated = [site for site in own
               if not site["hooked"] and not site["inDeclaredHazardTable"]
               and not site["inDeclaredPredecessorParse"]]
    predecessors = {}
    for name in (V4_CHECKER, V5_CHECKER, V6_CHECKER, V7_CHECKER):
        sites = json_load_sites(ast.parse(authority.snapshots[name]))
        jx_put(predecessors, name, {
            "sites": len(sites),
            "hooked": len([site for site in sites if site["hooked"]])})
    return {"sites": len(own), "ungated": ungated, "declaredHazardSites": len(hazard),
            "declaredPredecessorParses": len(reproductions),
            "declaredUnhookedSites": len(hazard) + len(reproductions),
            "hooked": len(hooked), "evasions": json_parse_evasion_sites(tree),
            "predecessors": predecessors}


def parse_probe(label="probe") -> dict:
    """Behavioural, reads no source.  Every declared byte/parse hazard driven
    through the LIVE parse and the LIVE finding function, and each must be named
    AT ITS POSITION.  The controls must produce nothing."""
    cases = named = admitted = controls = 0
    escapes = []
    for name, text, kind, position in JX_PARSE_CORPUS:
        cases += 1
        try:
            _value, problems = jx_loads(text)
            findings = parse_problem_findings(problems, label)
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            admitted += 1
            escapes.append(name + ": the live parse raised " + type(exc).__name__ +
                           " instead of naming the divergence")
            continue
        if not kind:
            controls += 1
            if findings:
                admitted += 1
                escapes.append(name + ": the CONTROL was refused by " + findings[0][:90] +
                               "; a probe that refuses its own control is not an oracle")
            continue
        expected = jx_get(_PARSE_FINDING_IDS, kind, "C2V9-PARSE")
        hit = [item for item in findings
               if item.startswith(expected + ":") and position in item]
        if hit:
            named += 1
        else:
            admitted += 1
            escapes.append(name + ": ADMITTED - " + str(len(findings)) + " finding(s) "
                           "but none is " + expected + " naming " + repr(position))
    return {"executedCases": cases, "namedAtThePosition": named, "controls": controls,
            "admissions": admitted, "escapes": escapes}


def parse_differential(authority) -> dict:
    """L8's differential, against the PINNED bytes of the REJECTED v6.

    This does not re-execute check-c2-v6.py; it re-executes the MECHANISM, which
    is what the finding is about.  For each retained vector the pinned document's
    bytes are edited, and this run measures that the parse the pinned predecessor
    performs -- `json.loads` with no hook, which this run reads structurally out
    of the pinned predecessor's own tree -- cannot tell the edited bytes from the
    unedited ones, while this checker's parse names the position.  The pinned
    predecessor's blindness is therefore recomputed every run rather than
    asserted, and it cannot change, because those bytes are hash-verified.
    """
    rows, escapes = [], []
    blind = named = 0
    for vector, document, needle, insert, position, note in PARSE_DIFFERENTIAL_VECTORS:
        original = authority.snapshots[document].decode("utf-8")
        if not jx_int_in_range(original.count(needle), 1, 1):
            escapes.append(vector + ": " + document + " does not carry " + repr(needle) +
                           " exactly once, so the retained vector is not executable "
                           "against the pinned bytes")
            continue
        mutant = original.replace(needle, insert + needle, 1)
        added = len(mutant.encode("utf-8")) - len(original.encode("utf-8"))
        # The predecessor's parse, executed exactly as the predecessor performs
        # it: no object_pairs_hook, so the LAST duplicate wins.
        host_blind = jx_equal(json.loads(mutant, object_pairs_hook=None),
                              json.loads(original, object_pairs_hook=None))
        if host_blind:
            blind += 1
        else:
            escapes.append(vector + ": an unhooked host parse of the edited bytes is no "
                           "longer identical to the parse of the unedited bytes, so the "
                           "mechanism this repair is measured against has collapsed")
        _value, problems = jx_loads(mutant)
        findings = parse_problem_findings(problems, document)
        hit = [item for item in findings
               if item.startswith("C2V9-DUPKEY:") and position in item]
        if hit:
            named += 1
        else:
            escapes.append(vector + ": this checker did NOT name " + position +
                           " when the pinned " + document + " was given a duplicate key")
        rows.append({"vector": vector, "document": document, "position": position,
                     "bytesAdded": added, "note": note,
                     "predecessorParseIsBlind": host_blind,
                     "successorNamedThePosition": bool(hit)})
    return {"vectors": len(PARSE_DIFFERENTIAL_VECTORS), "rows": rows,
            "predecessorParseBlind": blind, "successorNamedByPosition": named,
            "escapes": escapes}


def parse_integrity_findings(authority, tree) -> list:
    """L8, assembled.  Structure, behaviour and an external differential.

    The candidate's own byte/parse findings are emitted by `check`, not here, so
    that they survive every early return.
    """
    findings = []
    scan = parse_scan_findings(tree, authority)
    authority.parse_scan = scan
    for site in scan["ungated"]:
        findings.append(
            "C2V9-PARSE-SCAN: line " + str(site["line"]) + " parses JSON without an "
            "object_pairs_hook: " + site["source"] + "; CPython keeps the LAST "
            "occurrence of a duplicated key, so this call site cannot tell the bytes "
            "from the parse, and a defence applied to one input and not to its "
            "siblings is the list-of-places failure IR-C2V6-01 records")
    if not jx_int_in_range(scan["sites"], 1, 10 ** 6):
        findings.append("C2V9-PARSE-SCAN: this file appears to parse no JSON at all, so "
                        "the scan's clean verdict is a statement about an instrument "
                        "that detects nothing")
    if not jx_int_in_range(scan["declaredHazardSites"], 1, 10 ** 6):
        findings.append("C2V9-PARSE-SCAN: the operator space no longer demonstrates the "
                        "bare-parse hazard live, so the row that covers it proves "
                        "nothing")
    if not jx_int_in_range(scan["declaredPredecessorParses"], 1, 10 ** 6):
        findings.append("C2V9-PARSE-SCAN: this file no longer reproduces the "
                        "predecessor's own unhooked parse anywhere, so the differential "
                        "that shows what that parse cannot see is no longer executed")
    # OBS-C2V7-02.  The decomposition the banner prints must actually add up, and
    # it is a finding when it does not.  A sentence about a partition that is not
    # one is the same defect as a counter the run did not recompute.
    decomposed = (scan["hooked"] + scan["declaredHazardSites"] +
                  scan["declaredPredecessorParses"] + len(scan["ungated"]))
    if jx_bind(decomposed, scan["sites"]) is not None:
        findings.append(
            "C2V9-PARSE-SCAN: the parse call sites decompose into " +
            str(scan["hooked"]) + " hooked, " + str(scan["declaredHazardSites"]) +
            " hazard-demonstration exempt, " + str(scan["declaredPredecessorParses"]) +
            " predecessor-parse exempt and " + str(len(scan["ungated"])) +
            " ungated, which is " + str(decomposed) + " and not the " +
            str(scan["sites"]) + " call sites this file holds; the banner would then "
            "print a subtraction that does not add up, which is what v7 printed")
    # OBS-C2V7-01.  The evasions L4 already counts for its own model, counted for
    # this one, and required to be zero rather than left to a counter binding.
    # The detector is PROBED first: a count of zero over this file is
    # indistinguishable from a detector that sees nothing, and `parseEvasionSites`
    # is already zero, so its binding cannot tell the difference either.
    if not jx_int_in_range(
            len(json_parse_evasion_sites(ast.parse(PARSE_EVASION_DETECTOR_PROBE))),
            2, 10 ** 6):
        findings.append(
            "C2V9-PARSE-SCAN: the decoder-evasion detector reports no site in a probe "
            "that plainly calls json.JSONDecoder().decode and getattr(json, 'loads'), "
            "so its clean verdict over this file is a statement about an instrument "
            "that detects nothing")
    for site in scan["evasions"]:
        findings.append(
            "C2V9-PARSE-SCAN: line " + str(site["line"]) + " reaches the JSON decoder "
            "through a " + site["kind"] + " that the structural parse scan cannot "
            "see: " + site["source"] + "; json.JSONDecoder().decode and "
            "getattr(json, 'loads') are real bare unhooked parses that match neither "
            "shape json_load_sites looks for, and against v7 both were invisible and "
            "changed no published counter")
    depth = parse_depth_probe()
    authority.parse_depth = depth
    findings.extend("C2V9-PARSE-DEPTH: " + item for item in depth["escapes"])
    if jx_bind(depth["named"], 1) is not None:
        findings.append("C2V9-PARSE-DEPTH: the duplicate key nested " +
                        str(depth["depth"]) + " objects deep was not named at its "
                        "path, so `every duplicate key at any depth` is false at a "
                        "depth this run can reach")
    if jx_bind(depth["controls"], 1) is not None:
        findings.append("C2V9-PARSE-DEPTH: the control at depth " +
                        str(depth["depth"]) + " did not pass, so the depth probe is "
                        "not an oracle")
    authority.pinned_number_tokens = pinned_number_token_census(authority)
    if not jx_int_in_range(authority.pinned_number_tokens["tokens"], 1, 10 ** 9):
        findings.append("C2V9-PARSE-SCAN: the number-token scanner finds no token at "
                        "all across " + str(authority.pinned_number_tokens["files"]) +
                        " pinned JSON inputs, so its clean verdict over the candidate "
                        "is a statement about an instrument that detects nothing")
    for name in jx_sorted(list(scan["predecessors"])):
        entry = jx_get(scan["predecessors"], name)
        if not jx_int_in_range(entry["sites"], 1, 10 ** 6):
            findings.append("C2V9-PARSE-SCAN: the pinned " + name + " reports no JSON "
                            "parse site at all, so the scan cannot be shown to see the "
                            "shape it exists to catch")
        # The three checkers that PREDATE the parse repair must still hook nothing;
        # the pinned v7, which carries the repair, must still hook something.  A
        # single expectation over both would be wrong in one direction or the
        # other, and an anchor that is wrong is not an anchor.
        if jx_in(name, list(PARSE_UNHOOKED_PREDECESSORS)):
            if jx_bind(entry["hooked"], 0) is not None:
                findings.append("C2V9-PARSE-SCAN: the pinned " + name + " now hooks " +
                                str(entry["hooked"]) + " of its parses, so the external "
                                "anchor for IR-C2V6-01 has changed and the differential "
                                "is no longer measuring a known-defective instrument")
        elif not jx_int_in_range(entry["hooked"], 1, 10 ** 6):
            findings.append("C2V9-PARSE-SCAN: the pinned " + name + " no longer hooks "
                            "any of its parses, so the IR-C2V6-01 repair this successor "
                            "INHERITS is no longer present in the bytes it inherits it "
                            "from")
    probe = parse_probe(authority.document_name)
    authority.parse_probe = probe
    findings.extend("C2V9-PARSE-PROBE: " + item for item in probe["escapes"])
    if not jx_int_in_range(probe["executedCases"], 1, 10 ** 6):
        findings.append("C2V9-PARSE-PROBE: the parse layer probed no case, so it is a "
                        "claim over an unobserved region")
    if jx_bind(probe["admissions"], 0) is not None:
        findings.append("C2V9-PARSE-PROBE: " + str(probe["admissions"]) + " byte/parse "
                        "divergence(s) were admitted or their control refused")
    differential = parse_differential(authority)
    authority.parse_differential = differential
    findings.extend("C2V9-PARSE-DIFFERENTIAL: " + item for item in differential["escapes"])
    if jx_bind(differential["predecessorParseBlind"], differential["vectors"]) is not None:
        findings.append(
            "C2V9-PARSE-DIFFERENTIAL: " + str(differential["predecessorParseBlind"]) +
            " of " + str(differential["vectors"]) + " retained vectors still show the "
            "unhooked host parse unable to distinguish the edited bytes from the "
            "unedited ones")
    if jx_bind(differential["successorNamedByPosition"],
               differential["vectors"]) is not None:
        findings.append(
            "C2V9-PARSE-DIFFERENTIAL: " + str(differential["successorNamedByPosition"]) +
            " of " + str(differential["vectors"]) + " retained vectors were named by "
            "this checker at the position under test")
    return findings


# =============================================================================
# Section 3.  The derivation.  The effective v8 contract is the VERIFIED v4
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
        return effective, ["C2V9-DERIVATION: derivedFrom.operations must be a non-empty "
                           "JSON array; the effective contract is not derivable"]
    for index, op in enumerate(operations):
        if jx_type(op) != "object":
            findings.append("C2V9-DERIVATION: operation " + str(index) +
                            " is not a JSON object")
            continue
        kind, path = op.get("op"), op.get("path")
        if not jx_in(kind, DECLARED_OPS) or jx_type(path) != "string" or not path:
            findings.append("C2V9-DERIVATION: operation " + str(index) + " declares op=" +
                            repr(kind) + " path=" + repr(path) + "; the declared ops are " +
                            repr(list(DECLARED_OPS)))
            continue
        if not jx_has(op, "value"):
            findings.append("C2V9-DERIVATION: operation " + str(index) + " at " + path +
                            " carries no value")
            continue
        steps = _path_steps(path)
        try:
            if jx_equal(kind, "set"):
                current = _resolve_steps(effective, steps)
                if not jx_equal(current, op.get("from")):
                    findings.append(
                        "C2V9-DERIVATION: operation " + str(index) + " at " + path +
                        " declares it replaces " + repr(op.get("from")) + " (" +
                        jx_type(op.get("from")) + ") but the verified predecessor holds " +
                        repr(current) + " (" + jx_type(current) + "); the derivation does "
                        "not describe the bytes it is applied to")
                    continue
                _assign_steps(effective, steps, copy.deepcopy(op["value"]))
            else:
                parent = _resolve_steps(effective, steps[:-1])
                if jx_has_at(parent, steps[-1]):
                    findings.append("C2V9-DERIVATION: operation " + str(index) + " adds " +
                                    path + ", which already exists in the predecessor")
                    continue
                if not jx_put(parent, steps[-1], copy.deepcopy(op["value"])):
                    findings.append("C2V9-DERIVATION: operation " + str(index) +
                                    " cannot add " + path + " type-exactly")
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append("C2V9-DERIVATION: operation " + str(index) + " at " + path +
                            " does not resolve against the verified predecessor (" +
                            type(exc).__name__ + ")")
    return effective, findings


def project_to_v4_identity(effective, projection):
    """Restore exactly the identity fields the inherited oracle is pinned to."""
    projected = copy.deepcopy(effective)
    fields = projection.get("fields") if jx_type(projection) == "object" else None
    findings = []
    if jx_type(fields) != "object" or not fields:
        return projected, ["C2V9-PROJECTION: v4InheritanceProjection.fields must be a "
                           "non-empty JSON object"]
    if not jx_equal(fields, dict(DECLARED_PROJECTION_FIELDS)):
        findings.append(
            "C2V9-PROJECTION: the declared projection is " + repr(fields) + "; this "
            "checker admits exactly " + repr(dict(DECLARED_PROJECTION_FIELDS)) + " and "
            "nothing else, because a projection carrying any other field is a second "
            "contract the inherited oracle would be validating instead of this one")
        return projected, findings
    for path in jx_sorted(list(fields)):
        try:
            _assign_steps(projected, _path_steps(path), copy.deepcopy(fields[path]))
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append("C2V9-PROJECTION: " + path + " does not resolve (" +
                            type(exc).__name__ + ")")
    drift = jx_sorted(_wire_diff_paths(effective, projected))
    declared = jx_sorted(list(fields))
    if not jx_equal(drift, declared):
        findings.append("C2V9-PROJECTION: the projection handed to the inherited oracle "
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

    v8 authors the comparison; v4 -- reviewed, pinned, and confirmed sound at
    the wire surface by the adjudication -- provides the measurement.  Keeping
    those in different, separately reviewed bytes is deliberate and is named as
    a trust relationship in RES-C2V9-04.
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
            findings.append("C2V9-CENSUS: " + position + " is measured by this run at " +
                            repr(measured_value) + " but the candidate publishes no "
                            "value for it")
            continue
        reason = jx_bind(published, measured_value)
        if reason is None:
            continue
        if not jx_int(measured_value):
            findings.append("C2V9-INSTRUMENT: " + position + ": " + reason)
        elif not jx_int(published):
            findings.append("C2V9-TYPE: " + position + ": " + reason)
        else:
            findings.append("C2V9-CENSUS: " + position + ": " + reason)
    return findings


def register_findings(effective, measurement, authority) -> list:
    """L3.  The register must equal the measurement, in both directions."""
    findings = []
    spec = effective.get("planIntent", {})
    spec = spec.get("integerConstantRegisterV8") if jx_type(spec) == "object" else None
    if jx_type(spec) != "object":
        findings.append("C2V9-REGISTER: the effective contract declares no "
                        "planIntent.integerConstantRegisterV8; the census counters the "
                        "adjudication names as the fifth site would be unregistered")
        return findings
    raw_inherited = spec.get("inheritedFromV4")
    declared_inherited = raw_inherited if jx_type(raw_inherited) == "array" else []
    predecessor_ids = list(
        getattr(authority.v4, "DECLARED_INTEGER_CONSTANT_IDS", frozenset()))
    if not jx_equal(jx_sorted(jx_unique(declared_inherited)),
                    jx_sorted(jx_unique(predecessor_ids))):
        findings.append(
            "C2V9-REGISTER: the inherited half of the register is " +
            repr(jx_sorted(declared_inherited)) + " but the executed predecessor "
            "declares " + repr(jx_sorted(predecessor_ids)) + "; the v4 register may not "
            "be narrowed, widened or restated by this successor")
    raw_added = spec.get("censusCounterPositions")
    declared_added = raw_added if jx_type(raw_added) == "array" else []
    measured = list(measured_positions(measurement))
    missing = jx_sorted(jx_difference(measured, declared_added))
    extra = jx_sorted(jx_difference(declared_added, measured))
    if missing:
        findings.append("C2V9-REGISTER: " + str(len(missing)) + " published counter "
                        "position(s) are measured and compared but are not registered, "
                        "so a site could be added silently: " + repr(missing[:6]))
    if extra:
        findings.append("C2V9-REGISTER: " + str(len(extra)) + " registered position(s) "
                        "are not reached by the measurement, so the register overstates "
                        "what is observed: " + repr(extra[:6]))
    count_reason = jx_bind(spec.get("censusCounterPositionCount"), len(measured))
    if count_reason is not None:
        findings.append("C2V9-REGISTER: censusCounterPositionCount: " + count_reason)
    sites = census_site_positions(measurement)
    covered = []
    for key in jx_sorted(list(sites)):
        covered.extend(jx_get(sites, key))
    uncovered = jx_sorted(jx_difference(measured, covered))
    if uncovered or not jx_int_in_range(len(covered), 1, 10 ** 9):
        findings.append(
            "C2V9-REGISTER: the per-comparison-site partition covers " +
            str(len(jx_unique(covered))) + " of " + str(len(measured)) + " measured "
            "position(s); the figures the candidate publishes for how many wire "
            "integers each of the predecessor's three ungated comparisons reads would "
            "then be a claim over an unobserved region")
    rule = spec.get("rule")
    rule = rule if jx_type(rule) == "string" else ""
    if "type" not in rule or "before" not in rule:
        findings.append("C2V9-REGISTER: the register does not state plainly that the "
                        "JSON type is rejected before the content is compared")
    return findings


# =============================================================================
# Section 5.  L2b -- the document-wide INTEGER type lock over the EFFECTIVE
# contract, and L2c -- the TOTAL leaf ledger over the CANDIDATE document.
#
# THE TWO ARE SCOPED DIFFERENTLY AND SAY SO.  L2b is a claim about INTEGERS: it
# locks every integer leaf of the effective contract against the verified
# predecessor and float-probes each one.  That is a scoped claim about a scoped
# surface and it is stated as one.  L2c is a claim about EVERY LEAF, and after
# IR-C2V7-01 it may not be built out of walkers that name the types they cover.
#
# L2c is the repair for IR-C2V5-03, OBS-C2V6-01 and IR-C2V7-01, which are the
# same defect at three widths.  v5 locked the effective contract and left its
# own 66 integer leaves governed by nothing.  v6 bound its integer leaves and a
# new leaf spelled 17.0 reached a full green run.  v7 bound integer AND number
# leaves and a BOOLEAN leaf -- the document's own claim to have reproduced the
# finding v7 existed to discharge -- was bound by nothing, so one byte flipped
# it under a banner still reading `with no unbound bucket`.
#
# The rule is TOTAL OVER THE TYPE SPACE and not enumerated over its known
# members.  `jx_leaf_census` names the two container cases and nothing else;
# `jx_type_space` measures which types that fall-through reaches; the
# disposition table must EQUAL that measurement; a type with no rule is a named
# finding; and the PATH and JSON TYPE of every node are bound by one digest so
# that the one disposition which does not bind a VALUE -- a narrative string --
# still cannot be added, renamed or retyped silently.
# =============================================================================

def census_leaves_of_type(node, kind) -> list:
    """Every path at which the TOTAL leaf census reports a leaf of `kind`.

    OBS-C2V8-06.  `_integer_leaf_steps` is DELETED.  It was the last walker in
    this file that named the JSON type it looked for, and it was also the last
    RECURSIVE walk -- the shape IR-C2V7-02 was, raising an uncaught
    RecursionError past depth 1000.  Both defects are removed by the same edit.

    THE TYPE IS A PARAMETER, NOT A NAME IN THIS FUNCTION.  L2b and L6b genuinely
    are about integers -- the type lock locks integer leaves against the verified
    predecessor and the sweep injects a float at each of them -- so the SELECTION
    is type-named and has to be, at the call site, by the layer whose contract is
    about that type.  The TRAVERSAL is `jx_leaf_census`, which names no scalar
    type at all and whose coverage `jx_type_space` measures against the data
    model.  A type-named selection over a total walk cannot miss a leaf; a
    type-named WALK can, and that is IR-C2V7-01.

    Paths are lists, never tuples: a tuple is outside the JSON value universe,
    `jx_canon` refuses it by name, and `(1,) == (1.0,)` is True in the host
    language.
    """
    return [list(steps) for steps, reported in jx_leaf_census(node)
            if jx_equal(reported, kind)]


# `_number_leaf_steps` is GONE and so, in v9, is `_integer_leaf_steps`.  The
# first was v7's second type-named walker: v6's
# totality enumerated integer leaves, a new leaf spelled 17.0 reached a full
# green run, and v7 answered by adding a walker for the type that had escaped.
# That answer was the defect: `"reproducedByThisLane": true` is a BOOLEAN, a
# third walker nobody had written, and one byte flipped this lane's own claim
# that it reproduced IR-C2V6-01 under a full green banner (IR-C2V7-01).  The
# candidate totality is now `jx_leaf_census`, which names no scalar type at all,
# and `jx_type_space` measures that its fall-through reaches every member of the
# JSON data model.  v8 kept `_integer_leaf_steps` BELOW, unchanged, for L2b and
# L6b, and the v8 reviewer named that survival: one type-named walker was still
# in the file, and it was recursive besides.  v9 deletes it.  The scoped claims
# L2b and L6b make about integers are still scoped and still say so -- but the
# SELECTION is now a parameter passed to `census_leaves_of_type`, which reads
# the type back out of the total census, so no WALK in this file names a type.


def locked_integer_leaves(base, effective) -> list:
    """Every path holding a JSON integer in EITHER document.  Both directions,
    so neither a predecessor leaf the derivation retypes nor a leaf the
    derivation introduces can escape the lock.  The type is a PARAMETER of the
    selection and no walk names it (OBS-C2V8-06)."""
    locked = list(census_leaves_of_type(base, "integer"))
    locked.extend(census_leaves_of_type(effective, "integer"))
    return jx_sorted(jx_unique(locked))


def document_type_findings(effective, locked, prefix="C2V9-TYPE") -> list:
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


def document_type_probe(effective, locked, prefix="C2V9-TYPE") -> dict:
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
        missing = jx_sorted(jx_difference(census_leaves_of_type(document, "integer"), locked))
        if missing:
            findings.append(
                "C2V9-DOCLOCK: " + str(len(missing)) + " integer leaf/leaves of the " +
                label + " are outside the lock, the first being " +
                _steps_text(missing[0]) + "; the lock must cover BOTH documents, "
                "because a leaf the derivation introduces and a leaf the derivation "
                "retypes are different escapes and neither direction is optional")
    findings.extend(document_type_findings(effective, locked))
    probe = document_type_probe(effective, locked)
    authority.document_lock = probe
    findings.extend("C2V9-DOCLOCK: " + item for item in probe["escapes"])
    if not jx_int_in_range(probe["executedCases"], 1, 10 ** 9):
        findings.append("C2V9-DOCLOCK: the document-wide type lock probed no position, "
                        "so it is a claim over an unobserved region")
    if jx_bind(probe["admissions"], 0) is not None:
        findings.append("C2V9-DOCLOCK: " + str(probe["admissions"]) + " float "
                        "substitution(s) at declared integer leaves were admitted")
    if jx_bind(probe["namedTypeRejections"], probe["executedCases"]) is not None:
        findings.append("C2V9-DOCLOCK: " + str(probe["namedTypeRejections"]) + " of " +
                        str(probe["executedCases"]) + " probes produced a named finding")
    return findings


# ---- L2c: the candidate document's OWN leaves, ALL OF THEM ------------------
#
# IR-C2V7-01, and the pattern behind it.
#
#   v5   the residual pointed at gate dominance;  the live hazard was the TAINT
#        MODEL
#   v6   L2c's blind spot named STRINGS;          the live hazard was FLOATS
#   v7   RES-C2V7-07 named STRINGS;               the live hazard was BOOLEANS
#
# Three consecutive versions shipped with the residual pointing exactly one JSON
# type away from the live defect.  Not because three authors were careless: a
# totality built as an ENUMERATION OF TYPES is a list of places, and the defect
# moves to a place not on the list.  That is the failure v6 was authored to
# escape at the COMPARISON layer -- it stopped patching operators and built a
# primitive -- and it reappeared here at the ENUMERATION layer.
#
# So v8 does not add a boolean walker.  `_number_leaf_steps` is deleted rather
# than joined by a sibling.  The candidate totality is `jx_leaf_census`, which
# names the two CONTAINER cases and lets EVERY other JSON type fall through to a
# leaf; the disposition of a leaf is looked up by its JSON type in
# LEAF_TYPE_RULES; and that table is required to equal the type space
# `jx_type_space` MEASURES, which is itself required to be exactly the RFC 8259
# value space under the one refinement declared beside it.  A leaf whose type
# has no rule is a NAMED FINDING, not a silent pass.  There is no list left for
# a future residual to point one type away from.
#
# Every leaf of this document is under three obligations at once:
#
#   VALUE       every leaf whose rule is BIND -- null, boolean, integer, number
#               -- is bound to a value this run measured or to a byte of a
#               hash-verified pinned input.  An unbound one is C2V9-UNBOUND.
#   SHAPE       the PATH and the JSON TYPE of every NODE of the document,
#               container nodes included, are hashed into one digest published
#               in the document and bound to what this run measures.  Adding,
#               removing, renaming or retyping any node anywhere is
#               C2V9-SKELETON, whatever JSON type is involved and whether or not
#               the node's value is bound.
#   POPULATION  the per-type leaf counts are published and bound, so the
#               document's own account of what it contains cannot drift.
#
# What is NOT closed is the TEXT of a narrative string leaf.  That is
# RES-C2V9-07 and its boundary is a measured number, not a description.

CANDIDATE_STATUS = "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW"

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
    (["theSuccessorDefect", "measuredThisRun", "v9RejectedByName"],
     "successorV9RejectedByName"),
    (["theParseDefect", "minimalReproduction", "bytesAdded"],
     "parseDifferentialBytesAdded"),
    (["theParseDefect", "measuredThisRun", "vectors"], "parseDifferentialVectors"),
    (["theParseDefect", "measuredThisRun", "predecessorParseBlind"],
     "parseDifferentialPredecessorBlind"),
    (["theParseDefect", "measuredThisRun", "v9NamedByPosition"],
     "parseDifferentialSuccessorNamed"),
    (["theEnumerationDefect", "measuredThisRun", "vectors"],
     "enumerationDifferentialVectors"),
    (["theEnumerationDefect", "measuredThisRun", "v7EnumerationBlind"],
     "enumerationPredecessorBlind"),
    (["theEnumerationDefect", "measuredThisRun", "v9EnumeratedTheLeaf"],
     "enumerationSuccessorEnumerated"),
    (["theEnumerationDefect", "minimalReproduction", "bytesAdded"],
     "enumerationDifferentialBytesAdded"),
    (["documentSkeleton", "nodes"], "candidateNodes"),
    (["documentSkeleton", "containers"], "candidateContainers"),
    (["documentSkeleton", "leaves"], "candidateLeaves"),
    (["documentSkeleton", "nullLeaves"], "candidateLeavesNull"),
    (["documentSkeleton", "booleanLeaves"], "candidateLeavesBoolean"),
    (["documentSkeleton", "integerLeaves"], "candidateLeavesInteger"),
    (["documentSkeleton", "numberLeaves"], "candidateLeavesNumber"),
    (["documentSkeleton", "stringLeaves"], "candidateLeavesString"),
    (["documentSkeleton", "boundLeaves"], "candidateLeavesBound"),
    (["documentSkeleton", "narrativeStringLeaves"], "candidateNarrativeStringLeaves"),
    (["documentSkeleton", "unboundLeaves"], "candidateLeavesUnbound"),
    (["documentSkeleton", "rootSubtrees"], "candidateRootSubtreesBound"),
    (["documentSkeleton", "distinctPathTokens"], "pathIdentityDistinctPathTokens"),
    (["theSkeletonDefect", "measuredThisRun", "vectors"],
     "skeletonDifferentialVectors"),
    (["theSkeletonDefect", "measuredThisRun", "v8SkeletonBlind"],
     "skeletonPredecessorBlind"),
    (["theSkeletonDefect", "measuredThisRun", "v9SkeletonSeparated"],
     "skeletonSuccessorSeparated"),
    (["theSkeletonDefect", "minimalReproduction", "bytesAdded"],
     "skeletonDifferentialBytesAdded"),
)

# Per-comparison-site read counts, bound to the live census-site measurement.
CANDIDATE_SITE_KEYS = (CENSUS_SITE_LINE_2487, CENSUS_SITE_LINE_2493,
                       CENSUS_SITE_LINE_2517)


# ---- the leaf disposition table, checked against the MEASURED type space ----

LEAF_TYPE_RULES = (
    ("null", "BIND"),
    ("boolean", "BIND"),
    ("integer", "BIND"),
    ("number", "BIND"),
    ("string", "BIND-OR-NARRATIVE"),
    ("array", "CONTAINER"),
    ("object", "CONTAINER"),
)
LEAF_RULE_KINDS = ("BIND", "BIND-OR-NARRATIVE", "CONTAINER")
# A measured type space that plainly disagrees with the table above.  It exists so
# that `leaf_rule_findings` returning nothing over the REAL measurement is
# distinguishable from a check that has stopped looking.
LEAF_RULE_DETECTOR_PROBE = {
    "containerTypes": ["object"], "scalarTypes": ["integer", "number"],
    "types": 3, "escapes": [],
}


def leaf_rule_findings(space) -> list:
    """The disposition table must cover the MEASURED type space exactly.

    THIS IS WHERE THE COVERAGE IS DERIVED RATHER THAN DECLARED.  `space` is
    `jx_type_space()`: it measures which JSON types `jx_leaf_census` reports as
    leaves and which it descends through, over a witness corpus required to
    realise every member of JX_TYPES, which is in turn required to be exactly
    the RFC 8259 value space under one declared refinement.  If this table
    gains, loses or misclassifies a type -- or if the census stops reaching one
    -- the two stop agreeing and the disagreement is named.  A rule table that
    merely asserted its own coverage would be the enumeration defect again in a
    new place.
    """
    findings = []
    ruled = [kind for kind, _rule in LEAF_TYPE_RULES]
    for kind in jx_sorted(jx_difference(list(JX_TYPES), ruled)):
        findings.append("C2V9-LEAFRULE: the JSON type " + repr(kind) + " has no leaf "
                        "disposition rule, so a leaf of that type would be neither "
                        "bound nor named; three consecutive versions of this artifact "
                        "shipped with the live hazard exactly one JSON type outside "
                        "the totality")
    for kind in jx_sorted(jx_difference(ruled, list(JX_TYPES))):
        findings.append("C2V9-LEAFRULE: the leaf disposition table rules on " +
                        repr(kind) + ", which the primitive's declared type space "
                        "does not contain")
    for kind, rule in LEAF_TYPE_RULES:
        if not jx_in(rule, list(LEAF_RULE_KINDS)):
            findings.append("C2V9-LEAFRULE: the JSON type " + repr(kind) + " is ruled " +
                            repr(rule) + ", which is not one of the declared leaf "
                            "dispositions " + repr(list(LEAF_RULE_KINDS)))
    declared_containers = jx_sorted([kind for kind, rule in LEAF_TYPE_RULES
                                     if jx_equal(rule, "CONTAINER")])
    declared_leaves = jx_sorted([kind for kind, rule in LEAF_TYPE_RULES
                                 if not jx_equal(rule, "CONTAINER")])
    if not jx_equal(declared_containers, jx_sorted(list(space["containerTypes"]))):
        findings.append("C2V9-LEAFRULE: the table calls " + repr(declared_containers) +
                        " container types while the leaf census measurably descends "
                        "through " + repr(jx_sorted(list(space["containerTypes"]))) +
                        "; the disposition of a JSON type may not be a claim about the "
                        "walker, it has to be the walker's own measured behaviour")
    if not jx_equal(declared_leaves, jx_sorted(list(space["scalarTypes"]))):
        findings.append("C2V9-LEAFRULE: the table gives leaf dispositions to " +
                        repr(declared_leaves) + " while the leaf census measurably "
                        "reports " + repr(jx_sorted(list(space["scalarTypes"]))) +
                        " as leaves; it has to be the walker's own measured behaviour")
    for item in space["escapes"]:
        findings.append("C2V9-LEAFRULE: " + item)
    if not jx_int_in_range(space["types"], len(JX_TYPES), len(JX_TYPES)):
        findings.append("C2V9-LEAFRULE: the witness corpus realises " +
                        str(space["types"]) + " of the " + str(len(JX_TYPES)) +
                        " declared JSON types, so the type space is measured over less "
                        "than the data model it claims to enumerate")
    return findings


# ---- the SHAPE half: every node's path and type, in one bound digest --------

def document_skeleton(c) -> list:
    """`[canonical path token, JSON type]` for EVERY node, containers too.

    THIS IS THE REPAIR FOR IR-C2V8-01, AND IT IS ONE LINE.  v8 returned
    `[[_steps_text(steps), kind] ...]`.  `_steps_text` is `"/".join(...)` WITH
    NO ESCAPING, so the map from a structural path to its text is NOT
    INJECTIVE: `["a", "b"]` and `["a/b"]` both render as `"a/b"`, and `[0]` and
    `["0"]` both render as `"0"`.  A totality that reaches every node and then
    cannot tell two nodes apart binds a document other than this one.  Against
    c2-plan-stage-schema.v8.json ONE contiguous +11-byte edit, zero bytes of
    Python, relocating `thePrimitive/theEnumerationIsAGateToo` to a root key of
    that literal name, left the digest and every published count byte-identical
    and reached exit 0 with a full green banner.

    The path is now bound by `jx_canon` of the STEPS LIST.  `jx_canon` is
    length-framed and type-tagged, `jx_decanon` INVERTS it, and the round trip
    is executed on every run -- so the encoding is injective by construction,
    which is the same property that already made the VALUE half sound.  It also
    distinguishes an array INDEX from an object KEY that happens to be spelled
    with the same digits, which the joined text did not.
    `skeleton_path_identity_probe` executes both halves every run.

    Values are deliberately absent, and that is what makes the digest a
    FIXPOINT: publishing it inside the document it describes cannot change what
    it describes.  A narrative string's TEXT is outside this (RES-C2V9-07 and
    its measured size), but its PATH and its TYPE are inside it, and so are the
    path and type of every array, every object and every leaf of every type --
    so an added, removed, renamed, REPARENTED or retyped node anywhere in the
    document is a named finding regardless of which JSON type it happens to be.
    An empty array or an empty object holds no leaf at all and is invisible to
    any leaf census; this is the layer that sees it.
    """
    return [[jx_canon(list(steps)), kind] for steps, kind in jx_walk(c)]


def _v8_joined_skeleton(c) -> list:
    """v8's `document_skeleton` VERBATIM.  IR-C2V8-01's defect, RETAINED AS AN
    INSTRUMENT so the falsification is EXECUTED on every run rather than
    described.  Nothing binds this; `skeleton_path_identity_probe` requires it
    to COLLIDE on the corpus below, and requires `document_skeleton` not to."""
    return [[_steps_text(steps), kind] for steps, kind in jx_walk(c)]


# Pairs of DISTINCT JSON documents whose v8 skeletons are IDENTICAL.  The first
# is the reviewer's own minimal demonstration; the third and fourth are the
# array-index-versus-object-key collision the joined text also admits, which the
# reviewer did not need but which is the same defect.
SKELETON_COLLISION_CORPUS = (
    ("a nested leaf reparented across a `/` boundary",
     {"a": {"b": 1}}, {"a": {}, "a/b": 1}),
    ("a leaf reparented two levels",
     {"a": {"b": {"c": 1}}}, {"a": {"b": {}}, "a/b/c": 1}),
    ("a leaf reparented out of an ARRAY element, where the joined text carries "
     "the index",
     {"a": [{"b": 1}]}, {"a": [{}], "a/0/b": 1}),
    ("a whole SUBTREE reparented, which is seven of this lineage's positions",
     {"a": {"b": {"c": 1, "d": 2}}}, {"a": {}, "a/b": {"c": 1, "d": 2}}),
    ("an empty-string key, which joins to nothing at all",
     {"": {"a": 1}}, {"": {}, "/a": 1}),
)
# Path-level collisions, which are a strictly wider class than the document-level
# ones above: a JOINED TEXT can conflate two paths that no single pair of
# documents can exhibit side by side, because the container KIND on the way down
# differs and v8's skeleton did bind that.  These are the pairs `_steps_text`
# maps together and `jx_canon` does not, and the array INDEX against the object
# KEY of the same spelling is the sharpest of them: v8 could not tell `[0]` from
# `["0"]` at the path layer at all.
SKELETON_PATH_TEXT_COLLISIONS = (
    (["a", "b"], ["a/b"]),
    (["a", "b", "c"], ["a/b", "c"]),
    (["a", "b", "c"], ["a", "b/c"]),
    (["a", "b", "c"], ["a/b/c"]),
    ([0], ["0"]),
    (["x", 0], ["x/0"]),
    (["x", 0], ["x", "0"]),
    (["", "a"], ["/a"]),
)


def skeleton_path_identity_probe(c) -> dict:
    """PATH IDENTITY IS INJECTIVE, executed rather than asserted.  IR-C2V8-01.

    Three measurements, and all three must hold:

      COLLIDES    v8's joined-text encoding gives the two documents of every
                  corpus pair the SAME skeleton.  If this stops being true the
                  probe is measuring nothing and says so, because a repair
                  whose defect corpus no longer reproduces the defect is not a
                  measured repair.
      SEPARATES   this checker's encoding gives them DIFFERENT skeletons.
      INVERTS     every path of the REAL document round-trips: `jx_decanon` of
                  the canonical token is the steps list `jx_walk` produced, type
                  for type.  The existence of the inverse IS the injectivity
                  proof; nothing here asserts it.

    And one derived count: the number of DISTINCT canonical path tokens must
    equal the number of nodes, so no two nodes of this document share an
    identity.
    """
    escapes = []
    pairs = collided = separated = 0
    steps_pairs = steps_collided = steps_separated = 0
    for left_steps, right_steps in SKELETON_PATH_TEXT_COLLISIONS:
        steps_pairs += 1
        if jx_equal(_steps_text(left_steps), _steps_text(right_steps)):
            steps_collided += 1
        else:
            escapes.append("the paths " + repr(left_steps) + " and " +
                           repr(right_steps) + " no longer render to the same joined "
                           "text, so this corpus pair no longer reproduces the encoding "
                           "IR-C2V8-01 is about")
        if jx_ne(jx_canon(list(left_steps)), jx_canon(list(right_steps))):
            steps_separated += 1
        else:
            escapes.append("the paths " + repr(left_steps) + " and " +
                           repr(right_steps) + " share a canonical token, so path "
                           "identity is NOT INJECTIVE and IR-C2V8-01 is not discharged")
    for label, left, right in SKELETON_COLLISION_CORPUS:
        pairs += 1
        if jx_equal(_v8_joined_skeleton(left), _v8_joined_skeleton(right)):
            collided += 1
        else:
            escapes.append(label + ": the joined-text encoding no longer conflates "
                           "these two documents, so this corpus pair no longer "
                           "reproduces IR-C2V8-01 and the repair is measured against "
                           "a defect that is not there")
        if jx_ne(document_skeleton(left), document_skeleton(right)):
            separated += 1
        else:
            escapes.append(label + ": this checker's own skeleton gives two DISTINCT "
                           "JSON documents the same shape, so path identity is not "
                           "injective and IR-C2V8-01 is not discharged")
    nodes = jx_walk(c)
    tokens, inverted = [], 0
    for steps, _kind in nodes:
        token = jx_canon(list(steps))
        tokens.append(token)
        try:
            back = jx_decanon(token)
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            escapes.append(_steps_text(steps) + ": the canonical path token does not "
                           "invert (" + type(exc).__name__ + "), so the identity this "
                           "skeleton binds is not recoverable from the digest")
            continue
        if jx_equal(back, list(steps)):
            inverted += 1
        else:
            escapes.append(_steps_text(steps) + ": the canonical path token inverts to " +
                           repr(back) + ", which is a different path")
    distinct = len(jx_unique(tokens))
    if jx_bind(distinct, len(nodes)) is not None:
        escapes.append("this document has " + str(len(nodes)) + " nodes but only " +
                       str(distinct) + " distinct canonical path token(s), so two nodes "
                       "of it share one identity")
    joined_distinct = len(jx_unique([_steps_text(steps) for steps, _k in nodes]))
    return {"pairs": pairs, "collidesUnderTheJoinedText": collided,
            "separatesUnderTheCanonicalToken": separated,
            "stepPairs": steps_pairs, "stepPairsCollidingUnderTheJoinedText":
                steps_collided,
            "stepPairsSeparatedByTheCanonicalToken": steps_separated,
            "nodes": len(nodes),
            "pathsInverted": inverted, "distinctPathTokens": distinct,
            "distinctJoinedTexts": joined_distinct, "escapes": escapes}


# ---- the SHAPE half, LOCALISED: one digest per ROOT SUBTREE -----------------
# OBS-C2V8-04.  A string leaf and an empty container are named by the skeleton
# and not by the value ledger, and against v8 the ONLY finding was at
# documentSkeleton/sha256 -- a rejection that names no position.  The table
# below binds the skeleton of EVERY ROOT SUBTREE separately, so a new root key
# is named AT ITS OWN KEY and an injection at depth is named at the root subtree
# that contains it.  It is derived from the document's own root keys in both
# directions, so it cannot be narrowed silently.

def document_subtree_skeletons(c) -> dict:
    """The skeleton digest of each ROOT SUBTREE, keyed by its root key."""
    out = {}
    for key in list(c):
        jx_put(out, key, hashlib.sha256(
            jx_canon(document_skeleton(jx_at(c, key))).encode("utf-8")).hexdigest())
    return out


def document_skeleton_digest(c) -> str:
    return hashlib.sha256(
        jx_canon(document_skeleton(c)).encode("utf-8")).hexdigest()


def census_walk_agreement(c) -> dict:
    """`jx_leaf_census` against `jx_walk`, over the REAL document, BOTH WAYS.

    OBS-C2V8-01 recorded that `jx_type_space` measured the census at one fixed
    shallow path, and that what actually refused a DEPTH-narrowed census was the
    counter binding rather than the type space.  A count is a weaker instrument
    than an identity: it says a number moved, not which leaf went missing.

    Two total walks are computed here over THIS document, at every depth it
    actually has, and their leaf sets are required to be EQUAL as canonical
    tokens in both directions.  A census that drops leaves below some depth
    names the first leaf it dropped, at its own path.  A census that reports a
    leaf the node walk does not have names that one too.  Neither direction
    reads a published number, so republishing a counter cannot silence either.
    """
    walk = jx_walk(c)
    census = jx_leaf_census(c)
    walk_leaves = [[list(steps), kind] for steps, kind in walk
                   if jx_not_in(kind, ["array", "object"])]
    left = [jx_canon(row) for row in census]
    right = [jx_canon(row) for row in walk_leaves]
    escapes = []
    for token in jx_sorted(jx_difference(right, left)):
        row = jx_decanon(token)
        escapes.append("the node walk reports a JSON " + str(row[1]) + " leaf at " +
                       _steps_text(row[0]) + " that the leaf census does not reach, so "
                       "the totality every layer above stands on is narrower than this "
                       "document at that position")
    for token in jx_sorted(jx_difference(left, right)):
        row = jx_decanon(token)
        escapes.append("the leaf census reports a JSON " + str(row[1]) + " leaf at " +
                       _steps_text(row[0]) + " that the node walk does not have")
    return {"walkNodes": len(walk), "walkLeaves": len(walk_leaves),
            "censusLeaves": len(census),
            "agreed": len(right) - len(jx_difference(right, left)),
            "escapes": escapes}


def candidate_leaf_ledger(c, bound_paths) -> dict:
    """Dispose of EVERY leaf of the candidate.  Total by construction.

    Returns the counts and the findings.  The walk names no scalar type; the
    disposition is looked up by the type the census reports, and a type with no
    rule is a finding rather than a value that quietly vanishes from the
    totality.  `jx_difference` preserves the order of its left operand and the
    census has no repeated path, so one ordered pass disposes of every leaf
    without a per-leaf membership test.
    """
    rules = {}
    for kind, rule in LEAF_TYPE_RULES:
        jx_put(rules, kind, rule)
    counts = {}
    for kind in JX_TYPES:
        jx_put(counts, kind, 0)
    census = jx_leaf_census(c)
    unbound = jx_difference([row[0] for row in census], bound_paths)
    findings, position = [], 0
    bound = narrative = unruled = unbound_count = 0
    for steps, kind in census:
        jx_put(counts, kind, jx_get(counts, kind, 0) + 1)
        here = jx_int_in_range(position, 0, len(unbound) - 1) and \
            jx_equal(unbound[position], steps)
        if not here:
            bound += 1
            continue
        position = position + 1
        rule = jx_get(rules, kind)
        if rule is None:
            unruled += 1
            findings.append(
                "C2V9-LEAFRULE: the candidate publishes a leaf of JSON type " +
                repr(kind) + " at " + _steps_text(steps) + " and no disposition rule "
                "covers that type, so nothing in this run decides whether that leaf is "
                "evidence or prose")
            continue
        if jx_equal(rule, "BIND-OR-NARRATIVE"):
            narrative += 1
            continue
        unbound_count += 1
        findings.append(
            "C2V9-UNBOUND: the candidate publishes a JSON " + kind + " at " +
            _steps_text(steps) + " that no layer of this run binds to a measurement or "
            "to a verified pinned byte; v7 enumerated integer and number leaves only, "
            "so a BOOLEAN leaf was bound by nothing and one byte flipped this "
            "document's own claim that this lane reproduced the finding it exists to "
            "discharge, under a full green banner")
    nodes = jx_walk(c)
    return {"leaves": len(census), "counts": counts, "bound": bound,
            "nodes": len(nodes), "containers": len(nodes) - len(census),
            "narrative": narrative, "unruled": unruled, "unbound": unbound_count,
            "findings": findings}


# The shapes `live_register` renders from before L2c and L6d have run.  Their
# keys are the ledger's, so a register built early and a register built late
# carry the same NAMES and only ever differ in values -- which is what makes the
# two-pass binding of this document's own counters converge.
_EMPTY_LEDGER = {"leaves": 0, "counts": {}, "bound": 0, "nodes": 0, "containers": 0,
                 "narrative": 0, "unruled": 0, "unbound": 0, "findings": []}
_EMPTY_ENUMERATION = {"vectors": 0, "rows": [], "controls": 0, "predecessorBlind": 0,
                      "predecessorReachedControls": 0, "successorEnumerated": 0,
                      "bytesAdded": 0, "mutantDigest": "", "escapes": []}


def candidate_bindings(c, live, authority, base, measurement):
    """Return (bindings, findings).

    `bindings` maps a steps list of the CANDIDATE to (kind, expected value, what
    the expectation came from).  Every leaf whose disposition rule is BIND must
    appear -- null, boolean, integer and number alike -- and so must every
    closed string scalar a layer of this run actually measures.  Nothing is
    exempt, including this checker's own counters, the block that reports how
    many false accepts were measured, and the two BOOLEAN leaves that are this
    document's own claim to have reproduced the defects it discharges.
    """
    bindings, findings = [], []

    def bind(steps, kind, value, source):
        bindings.append({"steps": list(steps), "kind": kind, "expected": value,
                         "source": source})

    bind(["version"], "identity", 9, "this checker's declared successor identity")
    bind(["supersedes"], "identity", 8,
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
        for sub in census_leaves_of_type(op.get("from"), "integer"):
            try:
                expected = _resolve_steps(base, list(target) + list(sub))
            except MALFORMED_SHAPE_EXCEPTIONS:
                findings.append(
                    "C2V9-UNBOUND: derivedFrom/operations/" + str(index) + "/from/" +
                    _steps_text(sub) + " does not resolve in the verified predecessor, "
                    "so the derivation restates a byte that does not exist")
                continue
            bind(["derivedFrom", "operations", index, "from"] + list(sub),
                 "predecessor", expected,
                 "the byte the verified predecessor actually holds at " +
                 _steps_text(list(target) + list(sub)))
        for sub in census_leaves_of_type(op.get("value"), "integer"):
            steps = ["derivedFrom", "operations", index, "value"] + list(sub)
            expected, source = _effective_expected(
                list(target) + list(sub), live, positions)
            if expected is None:
                findings.append(
                    "C2V9-UNBOUND: the derivation writes a JSON integer into the "
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

    # The candidate's own residual accounting, bound to the candidate's own
    # lists.  A count that must equal what it counts cannot be overstated.
    residuals = c.get("residuals")
    residuals = residuals if jx_type(residuals) == "array" else []
    limitations = c.get("knownLimitations")
    limitations = limitations if jx_type(limitations) == "object" else {}
    bind(["residualAccounting", "residuals"], "measured", len(residuals),
         "the number of entries this document's own residuals list actually holds")
    bind(["residualAccounting", "knownLimitations"], "measured", len(limitations),
         "the number of entries this document's own knownLimitations block holds")
    bind(["residualAccounting", "total"], "measured", len(residuals) + len(limitations),
         "the sum of this document's own residuals and knownLimitations entries")

    for key in jx_sorted(list(live)):
        bind(["v9MeasuredCounters", key], "measured", jx_get(live, key),
             "the value this run measured for " + key)

    # ---- the BOOLEAN leaves.  THIS IS IR-C2V7-01. --------------------------
    # These are this document's own claims that this lane reproduced the three
    # defects it discharges.  In v7 they were bound by nothing at all -- neither
    # walker enumerated a boolean -- and one byte flipped either of them to
    # `false` under a banner still reading `with no unbound bucket`.  They are
    # bound here to what this run ACTUALLY MEASURED about each reproduction, so
    # the claim and the evidence cannot disagree in either direction.
    differential = authority.differential if authority.differential else {}
    parsediff = authority.parse_differential if authority.parse_differential else {}
    enumdiff = (authority.enumeration_differential
                if authority.enumeration_differential else {})
    bind(["theDefect", "minimalReproduction", "reproducedByThisLane"], "measured",
         jx_int_in_range(jx_get(differential, "predecessorFullyGreenRuns", 0),
                         1, 10 ** 9),
         "whether L6 drove the pinned predecessor to a FULLY GREEN run over a "
         "defective document at least once during THIS run")
    bind(["theParseDefect", "minimalReproduction", "reproducedByThisLane"], "measured",
         jx_int_in_range(jx_get(parsediff, "predecessorParseBlind", 0), 1, 10 ** 9) and
         jx_int_in_range(jx_get(parsediff, "successorNamedByPosition", 0), 1, 10 ** 9),
         "whether L8 measured, during THIS run, that the unhooked host parse cannot "
         "distinguish the edited bytes from the unedited ones while this checker names "
         "the position")
    bind(["theEnumerationDefect", "minimalReproduction", "reproducedByThisLane"],
         "measured",
         jx_int_in_range(jx_get(enumdiff, "predecessorBlind", 0), 1, 10 ** 9) and
         jx_int_in_range(jx_get(enumdiff, "successorEnumerated", 0), 1, 10 ** 9),
         "whether L6d measured, during THIS run, that the pinned check-c2-v7.py's own "
         "leaf enumeration does not reach the leaf while this checker's census does")
    skeldiff = (authority.skeleton_differential
                if authority.skeleton_differential else {})
    bind(["theSkeletonDefect", "minimalReproduction", "reproducedByThisLane"],
         "measured",
         jx_int_in_range(jx_get(skeldiff, "predecessorBlind", 0), 1, 10 ** 9) and
         jx_int_in_range(jx_get(skeldiff, "successorSeparated", 0), 1, 10 ** 9),
         "whether L6e measured, during THIS run, that the pinned check-c2-v8.py's own "
         "skeleton does not move when a node is reparented across a `/` boundary while "
         "this checker's does")

    # ---- the closed STRING scalars this run measures ------------------------
    # v7 bound integer and number leaves only, so every string leaf of the
    # document sat outside the ledger and the ledger could not be honest about
    # how much of the document it covered.  These are the strings a layer of
    # this run genuinely computes; the rest are NARRATIVE, counted and published
    # as such rather than left unmentioned.
    for steps, value, source in _declared_text_bindings():
        bind(steps, "identity", value, source)
    # The recorded digests, bound BY NAME rather than by position: `jx_sorted`
    # orders by canonical TOKEN and a token's length prefix sorts first, so a
    # position-indexed binding here would require this document's record table
    # to be ordered by string length, which is not an order a reader can check.
    # The recorded NAMES are covered instead by `_recording_findings`, which
    # requires the recorded set to equal the pinned set in both directions, and
    # by the skeleton, which binds the shape of the array.
    recorded = c.get("recordedInputs")
    recorded = recorded if jx_type(recorded) == "array" else []
    for index, item in enumerate(recorded):
        if jx_type(item) != "object":
            continue
        name = item.get("filename")
        if jx_has(PINS, name):
            bind(["recordedInputs", index, "sha256"], "identity", jx_get(PINS, name),
                 "the digest this run actually verified for " + str(name))
    bind(["documentSkeleton", "sha256"], "skeleton", document_skeleton_digest(c),
         "the sha256 of the path-and-type skeleton of this document, computed from "
         "the parsed document this run read")
    # OBS-C2V8-04.  ONE DIGEST PER ROOT SUBTREE, derived from this document's own
    # root keys.  A string leaf and an empty container are named by the SHAPE and
    # not by the value ledger, and against v8 the only finding was at
    # documentSkeleton/sha256 -- a rejection that named no position.  Because the
    # table is derived from the live root key set, a NEW root key produces a
    # binding at documentSkeleton/subtrees/<that key> which the candidate does not
    # publish, and the unbound-binding check below names it AT ITS OWN KEY.
    subtrees = document_subtree_skeletons(c)
    authority.root_subtrees = len(subtrees)
    for key in jx_sorted(list(subtrees)):
        bind(["documentSkeleton", "subtrees", key], "skeleton", jx_get(subtrees, key),
             "the sha256 of the path-and-type skeleton of the root subtree " +
             repr(key) + " of this document")
    return bindings, findings


def _declared_text_bindings():
    """Closed string scalars whose value a layer of this run measures.

    Built at call time because most of them are pinned digests, and a pinned
    digest transcribed into a table would be the second copy of a byte the
    recording obligation exists to keep singular.
    """
    return (
        (["artifact"], ARTIFACT_ID, "this checker's declared artifact id"),
        (["status"], CANDIDATE_STATUS,
         "the status this checker requires a candidate to hold"),
        (["derivedFrom", "artifact"], V4_CONTRACT,
         "the document the derivation is applied to"),
        (["derivedFrom", "sha256"], jx_get(PINS, V4_CONTRACT),
         "the digest this run verified for the document the derivation is applied to"),
        (["checkerModeContract", "checker"], "check-c2-v9.py",
         "the retained instrument this candidate is bound to"),
        (["theDefect", "findingId"], "IR-C2V4-01",
         "the disposition the pinned adjudication carries"),
        (["theDefect", "disposition"], "BLOCKING",
         "the grade the pinned adjudication carries"),
        (["theDefect", "minimalReproduction", "predecessor"], V4_CHECKER,
         "the checker this reproduction is measured against"),
        (["theDefect", "minimalReproduction", "predecessorSha256"],
         jx_get(PINS, V4_CHECKER), "the digest this run verified for " + V4_CHECKER),
        (["theDefect", "minimalReproduction", "input"], V4_CONTRACT,
         "the document this reproduction is measured over"),
        (["theDefect", "minimalReproduction", "inputSha256"],
         jx_get(PINS, V4_CONTRACT), "the digest this run verified for " + V4_CONTRACT),
        (["theDefect", "minimalReproduction", "sourceModification"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theDefect", "minimalReproduction", "compensationRequired"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theDefect", "minimalReproduction", "reproducedPerRun"], "EXHAUSTIVE",
         "how much of this reproduction an ordinary invocation recomputes"),
        (["theSuccessorDefect", "findingId"], "IR-C2V5-01",
         "the blocking finding of the pinned v5 REJECT this lane discharges"),
        (["theSuccessorDefect", "disposition"], "BLOCKING",
         "the grade the pinned v5 REJECT carries"),
        (["theParseDefect", "findingId"], "IR-C2V6-01",
         "the blocking finding of the pinned v6 REJECT this lane discharges"),
        (["theParseDefect", "disposition"], "BLOCKING",
         "the grade the pinned v6 REJECT carries"),
        (["theParseDefect", "minimalReproduction", "predecessor"], V6_CHECKER,
         "the checker this reproduction is measured against"),
        (["theParseDefect", "minimalReproduction", "predecessorSha256"],
         jx_get(PINS, V6_CHECKER), "the digest this run verified for " + V6_CHECKER),
        (["theParseDefect", "minimalReproduction", "input"], V6_CONTRACT,
         "the document this reproduction is measured over"),
        (["theParseDefect", "minimalReproduction", "inputSha256"],
         jx_get(PINS, V6_CONTRACT), "the digest this run verified for " + V6_CONTRACT),
        (["theParseDefect", "minimalReproduction", "sourceModification"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theParseDefect", "minimalReproduction", "compensationRequired"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theParseDefect", "minimalReproduction", "reproducedPerRun"], "MECHANISM",
         "how much of this reproduction an ordinary invocation recomputes"),
        (["theEnumerationDefect", "findingId"], "IR-C2V7-01",
         "the blocking finding of the pinned v7 REJECT this lane discharges"),
        (["theEnumerationDefect", "disposition"], "BLOCKING",
         "the grade the pinned v7 REJECT carries"),
        (["theEnumerationDefect", "minimalReproduction", "predecessor"], V7_CHECKER,
         "the checker this reproduction is measured against"),
        (["theEnumerationDefect", "minimalReproduction", "predecessorSha256"],
         jx_get(PINS, V7_CHECKER), "the digest this run verified for " + V7_CHECKER),
        (["theEnumerationDefect", "minimalReproduction", "input"], V7_CONTRACT,
         "the document this reproduction is measured over"),
        (["theEnumerationDefect", "minimalReproduction", "inputSha256"],
         jx_get(PINS, V7_CONTRACT), "the digest this run verified for " + V7_CONTRACT),
        (["theEnumerationDefect", "minimalReproduction", "sourceModification"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theEnumerationDefect", "minimalReproduction", "compensationRequired"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theEnumerationDefect", "minimalReproduction", "reproducedPerRun"],
         "MECHANISM", "how much of this reproduction an ordinary invocation recomputes"),
        (["theSkeletonDefect", "findingId"], "IR-C2V8-01",
         "the blocking finding of the pinned v8 REJECT this lane discharges"),
        (["theSkeletonDefect", "disposition"], "BLOCKING",
         "the grade the pinned v8 REJECT carries"),
        (["theSkeletonDefect", "minimalReproduction", "predecessor"], V8_CHECKER,
         "the checker this reproduction is measured against"),
        (["theSkeletonDefect", "minimalReproduction", "predecessorSha256"],
         jx_get(PINS, V8_CHECKER), "the digest this run verified for " + V8_CHECKER),
        (["theSkeletonDefect", "minimalReproduction", "input"], V8_CONTRACT,
         "the document this reproduction is measured over"),
        (["theSkeletonDefect", "minimalReproduction", "inputSha256"],
         jx_get(PINS, V8_CONTRACT), "the digest this run verified for " + V8_CONTRACT),
        (["theSkeletonDefect", "minimalReproduction", "sourceModification"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theSkeletonDefect", "minimalReproduction", "compensationRequired"], "NONE",
         "the bright line under which this disposition was graded BLOCKING"),
        (["theSkeletonDefect", "minimalReproduction", "reproducedPerRun"], "MECHANISM",
         "how much of this reproduction an ordinary invocation recomputes"),
    )


def _effective_expected(steps, live, positions):
    """What a layer of this checker measures at an EFFECTIVE-contract path."""
    text = _steps_text(steps)
    if jx_equal(list(steps[:1]), ["version"]):
        return 9, "this checker's declared successor identity"
    if jx_equal(list(steps[:1]), ["supersedes"]):
        return 8, "this checker's declared successor identity"
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
    """L2c.  TOTAL OVER THE TYPE SPACE, not over a list of types.

    Every leaf of the candidate is reached by `jx_leaf_census`, disposed of by
    the rule its JSON type carries, and a type with no rule is a finding.  Every
    bound leaf is then compared through `jx_bind_value`, which is total over the
    scalar space, and probed with a witness of EVERY member of JX_TYPES plus
    arbitrary value drift.  The document's whole SHAPE is bound by one digest.
    """
    findings = []
    space = jx_type_space()
    authority.type_space = space
    findings.extend(leaf_rule_findings(space))
    # The detector, probed.  `leaf_rule_findings` returning [] is
    # indistinguishable from a table that matches the measurement unless the
    # check is shown to fire on a type space that plainly disagrees with it.
    if not jx_int_in_range(len(leaf_rule_findings(LEAF_RULE_DETECTOR_PROBE)),
                           1, 10 ** 6):
        findings.append(
            "C2V9-LEAFRULE: the leaf disposition check does not fire on a measured type "
            "space that plainly disagrees with the declared table, so its clean verdict "
            "over the real one is a statement about an instrument that detects nothing")
    # The hostile spelling set is a module-level table, so this is asserted here
    # rather than inside the probe that reads it: a check a mutation can delete by
    # replacing the function that performs it is not a check on the table.
    produced = jx_sorted(jx_unique([kind for _label, kind, _produce
                                    in CANDIDATE_SPELLINGS if kind is not None]))
    for kind in jx_sorted(jx_difference(list(JX_TYPES), produced)):
        findings.append(
            "C2V9-CANDLOCK: the hostile spelling table declares no witness of the JSON "
            "type " + repr(kind) + ", so no bound leaf of this document is ever probed "
            "with one; a spelling set narrower than the data model is how IR-C2V7-01 "
            "stayed invisible for a whole version")
    bindings, findings_from_bindings = candidate_bindings(
        c, live, authority, base, measurement)
    findings.extend(findings_from_bindings)
    bound_paths = [record["steps"] for record in bindings]
    ledger = candidate_leaf_ledger(c, bound_paths)
    authority.candidate_ledger = ledger
    findings.extend(ledger["findings"])
    duplicates = [record["steps"] for record in bindings
                  if jx_count(bound_paths, record["steps"]) > 1]
    for steps in jx_sorted(jx_unique(duplicates)):
        findings.append("C2V9-UNBOUND: " + _steps_text(steps) + " is bound twice, so "
                        "one of the two bindings is not the one being enforced")
    census_paths = [row[0] for row in jx_leaf_census(c)]
    for steps in jx_sorted(jx_difference(bound_paths, census_paths)):
        findings.append(
            "C2V9-UNBOUND: this run binds " + _steps_text(steps) + " but the candidate "
            "publishes no leaf there; a binding over an absent leaf is a coverage claim "
            "over an unobserved region")
    # The SHAPE, named on its own so a probe can assert on it: an empty array or
    # an empty object holds no leaf and is invisible to any leaf census.
    #
    # STRUCTURALLY FIRST, because the digest is a counter this document publishes
    # and republishing a counter is the ordinary maintenance action this design's
    # cost model instructs a maintainer to perform.  A skeleton that stopped
    # describing every node would agree with a republished digest perfectly; it
    # cannot agree with the walk.
    skeleton = document_skeleton(c)
    if jx_bind(len(skeleton), ledger["nodes"]) is not None:
        findings.append(
            "C2V9-SKELETON: the skeleton describes " + str(len(skeleton)) + " node(s) "
            "where the walk over this document finds " + str(ledger["nodes"]) + "; a "
            "skeleton that does not cover every node binds the shape of a document "
            "other than this one, and republishing its digest would hide that")
    containers = [row for row in skeleton if jx_in(row[1], ["array", "object"])]
    if not jx_int_in_range(len(containers), 1, 10 ** 9):
        findings.append(
            "C2V9-SKELETON: the skeleton describes no container node at all, so an "
            "EMPTY array or object - which holds no leaf for any census to reach - "
            "could be added, removed or retyped with nothing to see it")
    # OBS-C2V8-01's second half, and it is not a counter: two total walks over
    # THIS document, compared as identities in both directions.
    agreement = census_walk_agreement(c)
    authority.census_agreement = agreement
    findings.extend("C2V9-CENSUS: " + item for item in agreement["escapes"])
    if jx_bind(agreement["walkNodes"], ledger["nodes"]) is not None:
        findings.append(
            "C2V9-CENSUS: the census-against-walk measurement saw " +
            str(agreement["walkNodes"]) + " node(s) where the walk over this document "
            "finds " + str(ledger["nodes"]) + "; a cross-check narrower than the "
            "document agrees with anything")
    if jx_bind(agreement["agreed"], agreement["walkLeaves"]) is not None:
        findings.append(
            "C2V9-CENSUS: the leaf census and the node walk agree at " +
            str(agreement["agreed"]) + " of the " + str(agreement["walkLeaves"]) +
            " leaf positions of this document; the census is the totality every layer "
            "above stands on and it may not be a claim about a walker")
    # IR-C2V8-01.  Path identity, executed: the corpus that COLLIDES under the
    # joined text must still collide, this encoding must separate every pair, and
    # every path of this document must invert.
    identity = skeleton_path_identity_probe(c)
    authority.path_identity = identity
    findings.extend("C2V9-SKELETON: " + item for item in identity["escapes"])
    if jx_bind(identity["pairs"], len(SKELETON_COLLISION_CORPUS)) is not None or \
            jx_bind(identity["stepPairs"],
                    len(SKELETON_PATH_TEXT_COLLISIONS)) is not None or \
            jx_bind(identity["nodes"], ledger["nodes"]) is not None:
        findings.append(
            "C2V9-SKELETON: the path-identity proof executed " + str(identity["pairs"]) +
            " of " + str(len(SKELETON_COLLISION_CORPUS)) + " document pair(s), " +
            str(identity["stepPairs"]) + " of " +
            str(len(SKELETON_PATH_TEXT_COLLISIONS)) + " path pair(s) and " +
            str(identity["nodes"]) + " of " + str(ledger["nodes"]) + " node path(s); "
            "injectivity here is the EXISTENCE OF THE INVERSE, executed on every run, "
            "and a probe that executes nothing proves nothing about it")
    if jx_bind(identity["separatesUnderTheCanonicalToken"], identity["pairs"]) is not None:
        findings.append(
            "C2V9-SKELETON: this checker's path encoding separates " +
            str(identity["separatesUnderTheCanonicalToken"]) + " of " +
            str(identity["pairs"]) + " document pairs that v8's joined-text encoding "
            "conflated; IR-C2V8-01 is exactly the pairs it does not separate")
    if jx_bind(identity["collidesUnderTheJoinedText"], identity["pairs"]) is not None:
        findings.append(
            "C2V9-SKELETON: the joined-text encoding conflates " +
            str(identity["collidesUnderTheJoinedText"]) + " of " +
            str(identity["pairs"]) + " corpus pairs, so this repair is measured "
            "against a defect that no longer reproduces and the measurement is vacuous")
    if jx_bind(identity["stepPairsSeparatedByTheCanonicalToken"],
               identity["stepPairs"]) is not None:
        findings.append(
            "C2V9-SKELETON: the canonical path token separates " +
            str(identity["stepPairsSeparatedByTheCanonicalToken"]) + " of " +
            str(identity["stepPairs"]) + " PATH pairs that the joined text maps "
            "together, including an array INDEX against an object KEY of the same "
            "spelling; a path identity that conflates two of them is v8's")
    if jx_bind(identity["stepPairsCollidingUnderTheJoinedText"],
               identity["stepPairs"]) is not None:
        findings.append(
            "C2V9-SKELETON: the joined text maps " +
            str(identity["stepPairsCollidingUnderTheJoinedText"]) + " of " +
            str(identity["stepPairs"]) + " retained path pairs together, so the corpus "
            "this repair is measured against no longer reproduces the defect")
    if jx_bind(identity["pathsInverted"], identity["nodes"]) is not None:
        findings.append(
            "C2V9-SKELETON: " + str(identity["pathsInverted"]) + " of " +
            str(identity["nodes"]) + " path token(s) of this document invert; "
            "injectivity here is the EXISTENCE OF THE INVERSE and nothing else")
    measured_digest = document_skeleton_digest(c)
    published_digest = None
    try:
        published_digest = _resolve_steps(c, ["documentSkeleton", "sha256"])
    except MALFORMED_SHAPE_EXCEPTIONS:
        findings.append("C2V9-SKELETON: the candidate publishes no "
                        "documentSkeleton/sha256, so the PATH and JSON TYPE of every "
                        "node of this document are unbound and a leaf whose value is "
                        "narrative could be added, renamed or retyped silently")
    if published_digest is not None:
        reason = jx_bind_text(published_digest, measured_digest)
        if reason is not None:
            findings.append(
                "C2V9-SKELETON: documentSkeleton/sha256: " + reason + "; the skeleton "
                "is the path and the JSON type of every node of this document, "
                "container nodes included, so this run and this document disagree "
                "about what the document CONTAINS and not merely about a value")
    for record in jx_sorted_by(bindings, "steps"):
        steps, kind = record["steps"], record["kind"]
        expected, source = record["expected"], record["source"]
        try:
            published = _resolve_steps(c, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        reason = jx_bind_value(published, expected)
        if reason is None:
            continue
        prefix = "C2V9-CANDIDATE" if jx_same_type(published, expected) else "C2V9-TYPE"
        findings.append(prefix + ": " + _steps_text(steps) + " (" + kind + "): " +
                        reason + "; the expectation is " + source)
    # The published subtree table must name exactly this document's root keys.
    # The other direction -- a root key the table does not name -- is already a
    # named finding at its own path, because the binding above produces one.
    published_subtrees = None
    try:
        published_subtrees = _resolve_steps(c, ["documentSkeleton", "subtrees"])
    except MALFORMED_SHAPE_EXCEPTIONS:
        findings.append("C2V9-SKELETON: the candidate publishes no "
                        "documentSkeleton/subtrees table, so a narrative leaf or an "
                        "empty container added anywhere is named only by the whole "
                        "document's digest and no finding says WHERE")
    localiser = document_subtree_skeletons(c)
    if not jx_equal(jx_sorted(list(localiser)), jx_sorted(list(c))):
        findings.append(
            "C2V9-SKELETON: the subtree localiser reports " + str(len(localiser)) +
            " root subtree(s) where this document has " + str(len(c)) + "; a localiser "
            "narrower than the document names no position for the leaves it dropped, "
            "which is the COLLATERAL rejection OBS-C2V8-04 recorded")
    if jx_type(published_subtrees) == "object":
        for key in jx_sorted(jx_difference(list(c), list(published_subtrees))):
            findings.append("C2V9-SKELETON: this document has the root subtree " +
                            repr(key) + ", which documentSkeleton/subtrees does not "
                            "name; an unnamed subtree is a region whose shape moves "
                            "without a finding that says where")
        for key in jx_sorted(jx_difference(list(published_subtrees), list(c))):
            findings.append("C2V9-SKELETON: documentSkeleton/subtrees names the root "
                            "subtree " + repr(key) + ", which this document does not "
                            "have; a shape table that describes a document other than "
                            "this one localises nothing")
    totality = candidate_totality_probe(c, bound_paths, measured_digest)
    authority.candidate_totality = totality
    findings.extend("C2V9-TOTALITY: " + item for item in totality["escapes"])
    if not jx_int_in_range(totality["executedCases"], 1, 10 ** 9):
        findings.append("C2V9-TOTALITY: the candidate totality probed no position, so "
                        "the claim that a leaf of ANY JSON type that no layer binds is "
                        "a named finding is a claim over an unobserved region - which "
                        "is exactly what it was in v7, where it was false for booleans")
    if jx_bind(totality["typesCovered"], len(JX_TYPES)) is not None:
        findings.append("C2V9-TOTALITY: the totality probe covered " +
                        str(totality["typesCovered"]) + " of the " + str(len(JX_TYPES)) +
                        " JSON types; a probe narrower than the data model measures a "
                        "totality narrower than the data model")
    if jx_bind(totality["admissions"], 0) is not None:
        findings.append("C2V9-TOTALITY: " + str(totality["admissions"]) + " injected "
                        "leaf/leaves that no layer binds were ADMITTED")
    if jx_bind(totality["localisedToASubtree"], totality["namedBySkeletonOnly"]) \
            is not None:
        findings.append(
            "C2V9-TOTALITY: " + str(totality["localisedToASubtree"]) + " of the " +
            str(totality["namedBySkeletonOnly"]) + " injection(s) the value ledger "
            "does not name are localised to a named root subtree; the rest are "
            "rejected COLLATERALLY, by a digest over the whole document, and a "
            "rejection that names no position is what OBS-C2V8-04 recorded")
    probe = candidate_type_probe(c, bindings)
    authority.candidate_lock = probe
    findings.extend("C2V9-CANDLOCK: " + item for item in probe["escapes"])
    if not jx_int_in_range(probe["executedCases"], 1, 10 ** 9):
        findings.append("C2V9-CANDLOCK: the candidate lock probed no position, so it is "
                        "a claim over an unobserved region")
    if jx_bind(probe["admissions"], 0) is not None:
        findings.append("C2V9-CANDLOCK: " + str(probe["admissions"]) + " hostile "
                        "spelling(s) at the candidate's own bound leaves were admitted")
    return findings


# ---- the totality probe: a leaf of EVERY JSON type, at the root and at depth -

CANDIDATE_TOTALITY_PROBE_KEY = "c2v8ProbeInjectedLeaf"
CANDIDATE_TOTALITY_TARGETS = ([], ["theDefect"], ["v9MeasuredCounters"],
                              ["documentSkeleton"])
# (label, the JSON type the injection introduces, the value, the sub-path of the
#  leaf it creates).  DERIVED COVERAGE: the probe refuses unless the labels
#  cover every member of JX_TYPES, so it cannot be narrower than the data model.
# An EMPTY container introduces no leaf at all, which is precisely why the
# skeleton exists; those rows assert on the skeleton finding instead.
CANDIDATE_TOTALITY_WITNESSES = (
    ("null", "null", None, []),
    ("boolean-true", "boolean", True, []),
    ("boolean-false", "boolean", False, []),
    ("integer", "integer", 17, []),
    ("number", "number", 17.0, []),
    ("string", "string", "17", []),
    ("array-empty", "array", [], None),
    ("array-holding-a-boolean", "array", [True], [0]),
    ("object-empty", "object", {}, None),
    ("object-holding-a-null", "object", {"n": None}, ["n"]),
)


def candidate_totality_probe(c, bound_paths, clean_digest) -> dict:
    """Behavioural, reads no source.  A leaf of EVERY JSON type that no layer
    binds must be a NAMED FINDING, at the root and at depth.

    This is the executable half of the IR-C2V7-01 repair and it is the reason
    the repair is not another walker.  Against v7, the `boolean-true`,
    `boolean-false`, `null`, `string` and both empty-container rows below were
    all ADMITTED to a full green run; only the integer and number rows were
    refused.  The probe is generated from JX_TYPES, so it cannot cover fewer
    types than the data model without saying so.
    """
    covered = jx_sorted(jx_unique([kind for _l, kind, _v, _s in
                                   CANDIDATE_TOTALITY_WITNESSES]))
    clean_subtrees = document_subtree_skeletons(c)
    rules = {}
    for kind, rule in LEAF_TYPE_RULES:
        jx_put(rules, kind, rule)
    cases = named = admitted = skeleton_only = localised = 0
    escapes = []
    for kind in jx_sorted(jx_difference(list(JX_TYPES), covered)):
        escapes.append("no witness of the JSON type " + repr(kind) + " is injected, so "
                       "nothing measures whether a leaf of that type that no layer "
                       "binds is named; v7 had no boolean witness and a boolean leaf "
                       "was admitted to a full green run")
    for target in CANDIDATE_TOTALITY_TARGETS:
        try:
            node = _resolve_steps(c, target)
        except MALFORMED_SHAPE_EXCEPTIONS:
            escapes.append(_steps_text(target) + ": the probe target does not resolve "
                           "in this candidate, so the totality is unobserved there")
            continue
        if jx_type(node) != "object" or jx_has(node, CANDIDATE_TOTALITY_PROBE_KEY):
            escapes.append(_steps_text(target) + ": the probe target is not an object "
                           "this run can extend, so the probe is not an oracle there")
            continue
        for label, _kind, value, sub in CANDIDATE_TOTALITY_WITNESSES:
            cases += 1
            jx_put(node, CANDIDATE_TOTALITY_PROBE_KEY, copy.deepcopy(value))
            try:
                position = _steps_text(list(target) + [CANDIDATE_TOTALITY_PROBE_KEY] +
                                       (list(sub) if sub is not None else []))
                # WHICH mechanism must fire is DERIVED from the disposition of the
                # JSON type the injection actually creates, read back out of the
                # census rather than declared in this table.  Accepting either
                # mechanism for every witness would let a totality narrowed back to
                # v7's coverage pass, because the skeleton would still fire.
                created = [row for row in jx_leaf_census(c)
                           if jx_equal(row[0], list(target) +
                                       [CANDIDATE_TOTALITY_PROBE_KEY] +
                                       (list(sub) if sub is not None else []))]
                rule = jx_get(rules, created[0][1]) if created else None
                ledger_must_name = jx_equal(rule, "BIND")
                # TWO mechanisms, and which one fires is PUBLISHED rather than
                # smoothed over.  A leaf whose JSON type is ruled BIND is named
                # by the ledger AT ITS OWN PATH.  A NARRATIVE string, and an
                # EMPTY container which holds no leaf for any census to reach,
                # are named by the SKELETON, because what they violate is the
                # document's shape and not a value anybody measured.  Both are
                # named findings; the split is `namedBySkeletonOnly` and it is
                # the measured size of RES-C2V9-07.
                ledger = candidate_leaf_ledger(c, bound_paths)
                by_ledger = bool([item for item in ledger["findings"]
                                  if position in item])
                by_skeleton = jx_ne(document_skeleton_digest(c), clean_digest)
                # OBS-C2V8-04.  WHERE the skeleton says the shape moved, measured
                # rather than described: the root subtree that contains the
                # injection must be the one whose digest moved, or must be a root
                # key the published table does not name at all.
                root = (list(target) + [CANDIDATE_TOTALITY_PROBE_KEY])[0]
                now = document_subtree_skeletons(c)
                by_subtree = (not jx_has(clean_subtrees, root)) or \
                    jx_ne(jx_get(now, root), jx_get(clean_subtrees, root))
                if ledger_must_name and by_ledger:
                    named += 1
                elif not ledger_must_name and by_skeleton:
                    named += 1
                    skeleton_only += 1
                    if by_subtree:
                        localised += 1
                else:
                    admitted += 1
                    escapes.append(
                        _steps_text(target) + "/" + label + ": a leaf that no layer "
                        "binds was ADMITTED at " + position + "; the disposition of the "
                        "JSON type it creates requires " +
                        ("the value ledger" if ledger_must_name
                         else "the document skeleton") + " to name it and it did not. "
                        "IR-C2V7-01 measured exactly this against v7 for the boolean, "
                        "null and string spellings and every one of them reached a full "
                        "green run")
            finally:
                del node[CANDIDATE_TOTALITY_PROBE_KEY]
    return {"executedCases": cases, "namedRejections": named, "admissions": admitted,
            "namedBySkeletonOnly": skeleton_only, "localisedToASubtree": localised,
            "typesCovered": len(covered), "escapes": escapes}


# ---- the hostile spelling set, generated from the type space ----------------

def _as_integer(value):
    try:
        if jx_type(value) == "boolean":
            return 1 if value else 0
        if jx_type(value) == "number":
            return int(value)
        if jx_type(value) == "string":
            return int(value)
        if jx_int(value):
            return value
    except (ValueError, OverflowError):
        return 0
    return 0


def _as_number(value):
    try:
        if jx_type(value) == "boolean":
            return 1.0 if value else 0.0
        if jx_in(jx_type(value), ["integer", "number", "string"]):
            return float(value)
    except (ValueError, OverflowError):
        return 0.0
    return 0.0


def _drift(value):
    """A DIFFERENT value of the SAME JSON type, wherever the type has one.

    `null` has exactly one inhabitant, so its drift is itself and the case
    scores as a control.  That is the honest answer rather than a skipped row.
    """
    kind = jx_type(value)
    if jx_equal(kind, "integer"):
        return value + 1
    if jx_equal(kind, "number"):
        return value + 1.0
    if jx_equal(kind, "boolean"):
        return not value
    if jx_equal(kind, "string"):
        return value + "-drift"
    return None


# (label, the JSON type it produces, the producer).  The type column is what
# `candidate_type_probe` checks against JX_TYPES: the spelling set is REQUIRED
# to realise every member of the data model, so it cannot be a nine-row list
# that happens to miss the type the defect is at.  v7's list carried
# `drift-plus-one`, which RAISES on a boolean leaf rather than probing it.
CANDIDATE_SPELLINGS = (
    ("null", "null", lambda value: None),
    ("boolean-true", "boolean", lambda value: True),
    ("boolean-false", "boolean", lambda value: False),
    ("integer", "integer", _as_integer),
    ("number", "number", _as_number),
    ("string", "string", lambda value: str(value)),
    ("array", "array", lambda value: []),
    ("object", "object", lambda value: {}),
    ("value-drift", None, _drift),
)


def candidate_type_probe(c, bindings) -> dict:
    """Behavioural, reads no source.  A witness of EVERY JSON type AND arbitrary
    value drift at EVERY bound leaf of the candidate, driven through the live
    binding.  The spelling set is generated from the type space rather than
    listed, so it covers boolean and null at an integer leaf and integer and
    null at a boolean leaf without anybody having to remember to add them."""
    cases = named = admitted = controls = 0
    escapes = []
    produced = jx_sorted(jx_unique([kind for _l, kind, _p in CANDIDATE_SPELLINGS
                                    if kind is not None]))
    for kind in jx_sorted(jx_difference(list(JX_TYPES), produced)):
        escapes.append("the hostile spelling set produces no witness of the JSON type " +
                       repr(kind) + ", so no bound leaf is probed with one; a spelling "
                       "set narrower than the data model is how IR-C2V7-01 stayed "
                       "invisible")
    for record in jx_sorted_by(bindings, "steps"):
        steps, expected = record["steps"], record["expected"]
        try:
            current = _resolve_steps(c, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        for label, _kind, produce in CANDIDATE_SPELLINGS:
            # Every (leaf, spelling) pair is executed, including the ones that
            # reproduce the bound value: those are CONTROLS and must be
            # accepted.  Counting them keeps executedCases a function of the
            # bound leaf set alone, so a counter this block publishes can never
            # change the number of cases that measure it.
            cases += 1
            try:
                value = produce(current)
            except MALFORMED_SHAPE_EXCEPTIONS as exc:
                admitted += 1
                escapes.append(_steps_text(steps) + "/" + label + ": producing the "
                               "spelling raised " + type(exc).__name__ + ", so this "
                               "leaf is not probed with a witness of that JSON type")
                continue
            bound = jx_bind_value(value, expected) is None
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
                               " was ADMITTED where the JSON " + jx_type(expected) +
                               " " + repr(expected) + " is measured")
            else:
                named += 1
    return {"boundLeaves": len(bindings), "executedCases": cases,
            "namedRejections": named, "controls": controls,
            "spellingTypes": len(produced),
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
    nothing and that the real hazard was the taint model.  v8 publishes the
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


def bare_truthiness_sites(tree) -> list:
    """`if x:` on a wire operand.  MEASURED, PUBLISHED, and NOT a finding.

    `bool(1) == bool(1.0) == bool(True)` and `bool(0) == bool(0.0) ==
    bool(False)`, so bare truthiness has exactly the int/float/bool equivalence
    semantics OPERATOR_SPACE exists to enumerate -- and v6's table omitted it,
    which the independent reviewer found.  The rows are added; this is the other
    half, the measurement over real source.

    It is deliberately NOT a finding.  Every site this reports in this file is a
    container or a syntax-tree object, where truthiness is emptiness and not
    numeric value, and no run has produced a false accept through one.  The
    count is BOUND to the candidate instead, so it cannot drift silently, and
    the honest scope is in RES-C2V9-09 rather than in a guard that would have to
    be suppressed 24 times to be green.
    """
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
    out, seen = [], set()
    for function in _function_universe(tree):
        tainted = _taint_fixpoint(function, literals)
        proven = _non_numeric_names(function, constants, str_proofs,
                                    _str_annotated_parameters(function))
        name = getattr(function, "name", "<lambda>")
        for node in ast.walk(function):
            tests = []
            if isinstance(node, (ast.If, ast.While, ast.IfExp, ast.Assert)):
                tests.append(node.test)
            elif isinstance(node, ast.BoolOp):
                tests.extend(node.values)
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                tests.append(node.operand)
            elif isinstance(node, ast.comprehension):
                tests.extend(node.ifs)
            for test in tests:
                if isinstance(test, (ast.Compare, ast.BoolOp, ast.UnaryOp)):
                    continue
                if not _is_wire(test, tainted, literals):
                    continue
                if _provably_non_numeric(test, constants, str_proofs, 0, proven):
                    continue
                key = (_position(test), ast.unparse(test))
                if key in seen:
                    continue
                seen.add(key)
                out.append({"function": name, "line": getattr(test, "lineno", 0),
                            "source": ast.unparse(test)[:120]})
    return sorted(out, key=lambda site: (site["line"], site["source"]))


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
    self_scan = wire_comparison_scan(tree, "check-c2-v9.py")
    predecessor_scan = wire_comparison_scan(
        ast.parse(authority.snapshots[V4_CHECKER]), V4_CHECKER)
    v5_scan = wire_comparison_scan(ast.parse(authority.snapshots[V5_CHECKER]), V5_CHECKER)
    authority.scan_self = self_scan
    authority.scan_predecessor = predecessor_scan
    authority.scan_v5 = v5_scan
    for site in self_scan["sites"]:
        findings.append(
            "C2V9-SCAN: " + site["function"] + " line " + str(site["line"]) + " (" +
            site["kind"] + ") lets the wire-sourced " + site["wireOperand"] +
            " meet " + site["farOperand"] + ", which is not provably non-numeric and "
            "is not routed through a declared type gate: " + site["source"])
    if not jx_int_in_range(self_scan["gateCallSites"], 8, 10 ** 6):
        findings.append("C2V9-SCAN: only " + str(self_scan["gateCallSites"]) +
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
            findings.append("C2V9-SCAN: this file carries " +
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
            "C2V9-SCAN-BLIND: the scan reports " + str(self_scan["functionLikeNodes"]) +
            " function-like node(s) but this file holds " + str(len(walked)) +
            " of them and excludes " + str(len(gated)) + " declared gates; a scan that "
            "does not walk nested defs, methods and lambdas is the narrowing that made "
            "IR-C2V4-01 invisible")
    # The scan is load-bearing only if it SEES the defects it was written for.
    adjudicated = adjudicated_census_lines(authority)
    if not jx_int_in_range(len(adjudicated), 1, 10 ** 6):
        findings.append(
            "C2V9-SCAN-BLIND: the pinned adjudication yields no comparison line at all, "
            "so the anchor that proves this scan sees the defect it exists to catch is "
            "vacuous; v5 could be silenced completely by exactly this, and the reviewer "
            "found it with zero findings")
    found = [site["line"] for site in predecessor_scan["sites"]]
    unseen = jx_sorted(jx_difference(adjudicated, found))
    if unseen:
        findings.append(
            "C2V9-SCAN-BLIND: run over the pinned predecessor this scan does NOT report "
            "the adjudicated census comparison(s) at line(s) " + repr(unseen) + "; a "
            "scan that cannot see the defect it exists to catch is decorative")
    # ... and the one its OWN predecessor could not see in its own file.
    v5_found = [site["line"] for site in v5_scan["sites"]]
    if not jx_in(V5_DEFECT_LINE, v5_found):
        findings.append(
            "C2V9-SCAN-BLIND: run over the pinned check-c2-v5.py this scan does NOT "
            "report line " + str(V5_DEFECT_LINE) + ", the subset test that produced "
            "IR-C2V5-01 and that v5's own scan classified as having no wire operand at "
            "all; if v8's model cannot see it, v8's model is v5's model")
    if not jx_int_in_range(predecessor_scan["ungatedComputedOperandComparisons"],
                           1, 10 ** 6):
        findings.append("C2V9-SCAN-BLIND: the scan reports no computed-operand "
                        "comparison anywhere in the predecessor, which contradicts the "
                        "measured adjudication and means the computed-operand model is "
                        "inert")
    # Bare truthiness: measured over this file and over the pinned v6, published,
    # bound, and deliberately not a finding.  See `bare_truthiness_sites`.
    truthiness = {"self": len(bare_truthiness_sites(tree)),
                  V6_CHECKER: len(bare_truthiness_sites(
                      ast.parse(authority.snapshots[V6_CHECKER])))}
    authority.truthiness = truthiness
    if not jx_int_in_range(jx_get(truthiness, V6_CHECKER), 1, 10 ** 6):
        findings.append("C2V9-SCAN-BLIND: the bare-truthiness model reports nothing at "
                        "all over the pinned " + V6_CHECKER + ", where it is known to "
                        "report sites; a detector with a clean verdict over this file "
                        "and no positive anywhere is an instrument that detects nothing")
    return findings


# =============================================================================
# Section 6b.  L9 -- THE DECLARED STRINGS.
#
# Two v6 defects have the same shape and neither had any instrument behind it:
#
#   * one SOURCE_MUTATIONS row asserted the subject 'outside the census block'
#     while the guard it asserts on emits 'OUTSIDE the census block', so the row
#     scored ESCAPE on the dispatched bytes.  Nothing detected that except
#     running the whole 109-row matrix to termination, which is the thing this
#     corpus has repeatedly not done.
#   * the module docstring's normative adoption step told an adopter to call
#     `jx_min` and `jx_max`, WHICH DID NOT EXIST.  Following the instructions
#     verbatim produced a NameError.
#
# Both are "a declared string that names something that is not there", and both
# now run on EVERY invocation rather than only under --selftest.  The honest
# scope is published: this closes "names a string that exists nowhere"; it does
# NOT close "names a string that exists somewhere OTHER than the guard it
# asserts on", because the lower-case spelling above genuinely occurs in a
# banner template.  The emit-site figure is published so a reader can see how
# much of the table is proved at the guard it asserts on rather than merely
# somewhere in the file.  That residual is RES-C2V9-10.
# =============================================================================

# OBS-C2V7-04.  `declared_assertion_rows` reads FOUR tables and v7's exclusion
# set named three: PARSE_MUTATIONS was absent, so its own thirty-five string
# constants stood in the evidence pool as proof of their own claims -- exactly
# the vacuity `_assertion_table_constants` exists to prevent -- and two published
# bound counters were wrong by four as a result.  The reviewer verified that
# `unresolved` stayed 0 either way, so nothing was bought by the omission; the
# counters were simply measured over a pool that violated the layer's own rule.
_ASSERTION_TABLE_NAMES = ("_GATE_MUTATIONS", "GATE_MUTATIONS", "LAYER_MUTATIONS",
                          "SOURCE_MUTATIONS", "CONTRACT_MUTATIONS", "SCAN_MUTATIONS",
                          "PARSE_MUTATIONS")
_JX_NAME_RE = re.compile(r"jx_[A-Za-z0-9_]+")


def declared_assertion_rows() -> list:
    """(table, expected finding id, subject) for every retained assertion."""
    out = []
    for _name, _mutate, expected, subject in CONTRACT_MUTATIONS:
        out.append(["contract", expected, subject])
    for _name, _function, _body, expected, subject, _sweep in SOURCE_MUTATIONS:
        out.append(["source", expected, subject])
    for _name, _mutate, expected, subject in SCAN_MUTATIONS:
        out.append(["scan", expected, subject])
    for _name, _needle, _replacement, expected, subject in PARSE_MUTATIONS:
        if jx_int_in_range(len(expected), 1, 10 ** 6):
            out.append(["parse", expected, subject])
    return out


def _assertion_table_constants(tree) -> set:
    """The string constants of the assertion tables THEMSELVES, which may never
    stand as evidence that a string exists: a table proving its own claims is
    the vacuity this layer is here to avoid."""
    out = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        named = [target for target in node.targets
                 if isinstance(target, ast.Name) and target.id in _ASSERTION_TABLE_NAMES]
        if not named:
            continue
        for item in ast.walk(node):
            if isinstance(item, ast.Constant) and jx_type(item.value) == "string":
                out.add(id(item))
    return out


def source_string_pool(tree) -> list:
    """Every string constant of this file EXCEPT the assertion tables' own."""
    skip = _assertion_table_constants(tree)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and jx_type(node.value) == "string" and \
                id(node) not in skip:
            out.append(node.value)
    return out


def emit_site_pool(tree, finding_ids) -> dict:
    """finding id -> the string constants of every function that emits it."""
    skip = _assertion_table_constants(tree)
    pool = {}
    for function in ast.walk(tree):
        if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        texts = [node.value for node in ast.walk(function)
                 if isinstance(node, ast.Constant) and jx_type(node.value) == "string"
                 and id(node) not in skip]
        for finding_id in finding_ids:
            emits = [item for item in texts
                     if item.startswith(finding_id + ":") or jx_equal(item, finding_id)]
            if emits:
                jx_put(pool, finding_id, jx_get(pool, finding_id, []) + texts)
    return pool


def document_string_pool(c) -> list:
    """Every path text and every string value of the candidate document."""
    out = []

    def descend(node, steps):
        out.append(_steps_text(steps))
        kind = jx_type(node)
        if kind == "object":
            for key in list(node):
                descend(jx_at(node, key), list(steps) + [key])
        elif kind == "array":
            for index, item in enumerate(node):
                descend(item, list(steps) + [index])
        elif kind == "string":
            out.append(node)

    descend(c, [])
    return out


def defined_names(tree) -> list:
    """Every function and class this file defines, at any depth."""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append(node.name)
    return jx_sorted(jx_unique(out))


def declared_string_layer(c, tree) -> dict:
    """L9's measurement.  Returns counts and escapes; the caller names them."""
    rows = declared_assertion_rows()
    ids = jx_sorted(jx_unique([row[1] for row in rows]))
    source_pool = source_string_pool(tree)
    emit_pool = emit_site_pool(tree, ids)
    document_pool = document_string_pool(c)
    escapes = []
    in_source = in_document = at_emit_site = unresolved = 0
    for finding_id in ids:
        present = [item for item in source_pool
                   if (finding_id + ":") in item or jx_equal(item, finding_id)]
        if not present:
            escapes.append("the assertion tables expect the finding id " +
                           repr(finding_id) + ", which no string constant of this file "
                           "outside those tables ever emits; the rows asserting on it "
                           "can only ever ESCAPE")
    for table, expected, subject in rows:
        if jx_int_in_range(len(subject), 0, 0):
            continue
        emitted = [item for item in jx_get(emit_pool, expected, []) if subject in item]
        sourced = [item for item in source_pool if subject in item]
        documented = [item for item in document_pool if subject in item]
        if emitted:
            at_emit_site += 1
        if sourced:
            in_source += 1
        elif documented:
            in_document += 1
        else:
            unresolved += 1
            escapes.append("the " + table + " assertion table asserts on " +
                           repr(subject) + " for " + expected + ", and that string "
                           "occurs neither in this file outside the assertion tables "
                           "nor anywhere in the candidate document; a row that names a "
                           "string nothing produces can only ever ESCAPE, which is how "
                           "one v6 row scored ESCAPE on its own dispatched bytes")
    named = []
    docstring = ast.get_docstring(tree)
    docstring = docstring if jx_type(docstring) == "string" else ""
    for match in _JX_NAME_RE.findall(docstring):
        named.append(["the module docstring", match])
    for item in document_pool:
        for match in _JX_NAME_RE.findall(item):
            named.append(["the candidate document", match])
    defined = defined_names(tree)
    missing = 0
    for where, name in named:
        if not jx_in(name, defined):
            missing += 1
            escapes.append(where + " names " + name + ", which this file does not "
                           "define; v6's normative adoption step named jx_min and "
                           "jx_max and an adopter following it verbatim got a NameError, "
                           "and a wrong adoption step is a live defect and not a typo")
    return {"rows": len(rows), "findingIds": len(ids), "inSource": in_source,
            "inDocument": in_document, "atEmitSite": at_emit_site,
            "unresolved": unresolved, "namesChecked": len(named),
            "namesUndefined": missing, "escapes": escapes}


def declared_string_findings(c, authority, tree) -> list:
    result = declared_string_layer(c, tree)
    authority.declared_strings = result
    findings = ["C2V9-DECLARED-STRING: " + item for item in result["escapes"]]
    if not jx_int_in_range(result["rows"], 1, 10 ** 6):
        findings.append("C2V9-DECLARED-STRING: there are no retained assertion rows to "
                        "check, so this layer is a statement about an empty set")
    if not jx_int_in_range(result["namesChecked"], 1, 10 ** 6):
        findings.append("C2V9-DECLARED-STRING: no primitive name is named by the "
                        "docstring or the candidate, so the adoption-instruction check "
                        "detects nothing")
    if not jx_int_in_range(result["atEmitSite"], 1, 10 ** 6):
        findings.append("C2V9-DECLARED-STRING: not one declared subject is proved at "
                        "the emit site of the finding it asserts on, so the stronger "
                        "half of this layer is inert and only the weak module-wide "
                        "corpus is doing any work")
    if jx_bind(result["unresolved"], 0) is not None:
        findings.append("C2V9-DECLARED-STRING: " + str(result["unresolved"]) +
                        " declared subject(s) name a string that exists nowhere")
    if jx_bind(result["namesUndefined"], 0) is not None:
        findings.append("C2V9-DECLARED-STRING: " + str(result["namesUndefined"]) +
                        " named primitive entry point(s) do not exist")
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
                   if item.startswith("C2V9-TYPE:") and position in item]
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
                           findings[0].split(":")[0] + " rather than a C2V9-TYPE "
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
                if item.startswith("C2V9-INSTRUMENT:") and position in item]:
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
        "_parse_problem_position":
            lambda value: _parse_problem_position({"path": [], "key": value,
                                                   "offset": 0}),
        "document_skeleton_digest": lambda value: document_skeleton_digest(
            {"probe": value}),
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
        findings.append("C2V9-BEHAVIOUR: the behavioural layer executed no case at all")
    if jx_bind(result["admissions"], 0) is not None:
        findings.append("C2V9-BEHAVIOUR: " + str(result["admissions"]) +
                        " type-distinct spelling(s) of a published integer counter were "
                        "ADMITTED by the repaired comparator")
    if jx_bind(result["rejectedWithoutNamingThePosition"], 0) is not None:
        findings.append(
            "C2V9-BEHAVIOUR: " + str(result["rejectedWithoutNamingThePosition"]) +
            " case(s) were rejected without a C2V9-TYPE finding naming the position; "
            "that is the adjudication's trap, where a non-zero exit came from unrelated "
            "arithmetic")
    if jx_bind(result["namedTypeRejections"], result["executedCases"]) is not None:
        findings.append("C2V9-BEHAVIOUR: " + str(result["namedTypeRejections"]) + " of " +
                        str(result["executedCases"]) + " cases produced a named type "
                        "finding")
    if not jx_int_in_range(result["instrumentProbes"], 1, 10 ** 9):
        findings.append("C2V9-BEHAVIOUR: the computed-operand gate was never probed, so "
                        "the half of the repair that guards the instrument's own side "
                        "is unfalsified")
    if jx_bind(result["instrumentProbesEscaped"], 0) is not None:
        findings.append("C2V9-BEHAVIOUR: " + str(result["instrumentProbesEscaped"]) +
                        " float MEASURED value(s) were accepted; the computed side of "
                        "the comparison is ungated, which is the operand type "
                        "IR-C2V4-01 names")
    findings.extend("C2V9-PROOF: " + item for item in result["strProof"]["escapes"])
    findings.extend("C2V9-PROOF: " + item for item in result["astProof"]["escapes"])
    if not jx_int_in_range(result["strProof"]["executedCases"], 1, 10 ** 9) or \
            not jx_int_in_range(result["astProof"]["executedCases"], 1, 10 ** 9):
        findings.append("C2V9-PROOF: L4's non-numeric proofs were not exercised, so the "
                        "excusals they grant rest on unchecked signatures")
    primitive = authority.primitive
    findings.extend("C2V9-PRIMITIVE: " + item for item in primitive["escapes"])
    for key, expected in (("tokenCollisions", 0), ("crossTypeAdmissions", 0),
                          ("gateAdmissions", 0), ("reflexiveFailures", 0),
                          ("entryPointFailures", 0),
                          ("orderEqualityDivergences", 0), ("parseAdmissions", 0)):
        if jx_bind(jx_get(primitive, key), expected) is not None:
            findings.append("C2V9-PRIMITIVE: " + key + " is " +
                            str(jx_get(primitive, key)) + ", not " + str(expected) +
                            "; the single decision point every other layer is built on "
                            "does not hold its own property")
    # Vacuity floors.  Zeroing the primitive's own test must not look like a
    # pass: every count below is required to be positive before the equalities
    # above mean anything.
    for key in ("corpusValues", "corpusPairs", "operatorSpaceRows", "gateCases",
                "entryPointCases", "domainRefusals", "orderPairs", "parseCases",
                "parseControls", "parseNamedAtThePosition", "callShapedRowsDeclared"):
        if not jx_int_in_range(jx_get(primitive, key), 1, 10 ** 9):
            findings.append("C2V9-PRIMITIVE: " + key + " is " +
                            repr(jx_get(primitive, key)) + "; the primitive's own "
                            "exhaustive test has stopped executing, so every equality "
                            "it reports is a statement about an empty set")
    if jx_bind(primitive["roundTrips"], primitive["corpusValues"]) is not None or \
            jx_bind(primitive["distinctTokens"], primitive["corpusValues"]) is not None:
        findings.append("C2V9-PRIMITIVE: the canonical encoding is not invertible over "
                        "the corpus, so it is not injective, so it can conflate two "
                        "distinct JSON values and nothing built on it holds")
    if jx_bind(primitive["operatorSpaceHazardsReproduced"],
               primitive["operatorSpaceRows"]) is not None or \
            jx_bind(primitive["operatorSpaceRowsCovered"],
                    primitive["operatorSpaceRows"]) is not None:
        findings.append("C2V9-PRIMITIVE: the operator space is not fully demonstrated "
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
        v9_findings = census_comparison_findings(mutant, measurement)
        v9_named = [item for item in v9_findings
                    if item.startswith("C2V9-TYPE:") and position in item]
        if not v4_named:
            predecessor_admitted += 1
        if not v4_findings:
            fully_green += 1
        if v9_named:
            successor_rejected += 1
        else:
            escapes.append(vector + ": this checker did NOT reject " + position +
                           " spelled " + spelling + " with a C2V9-TYPE finding naming "
                           "the position")
        rows.append({"vector": vector, "position": position, "spelling": spelling,
                     "note": note, "predecessorFindingCount": len(v4_findings),
                     "predecessorNamedThePosition": bool(v4_named),
                     "predecessorFullyGreen": not v4_findings,
                     "successorNamedThePosition": bool(v9_named)})
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
    leaves = census_leaves_of_type(base, "integer")
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
    live_leaves = len(census_leaves_of_type(base, "integer"))
    if jx_bind(sweep["integerLeavesInjected"], live_leaves) is not None:
        findings.append("C2V9-SWEEP: the sweep reports " +
                        str(sweep["integerLeavesInjected"]) + " integer leaves injected "
                        "but the pinned predecessor document holds " + str(live_leaves))
    total = sweep["admittedToAFullGreenRun"] + sweep["rejectedByPredecessor"]
    if jx_bind(total, sweep["integerLeavesInjected"]) is not None:
        findings.append("C2V9-SWEEP: admitted plus rejected is " + str(total) + " but " +
                        str(sweep["integerLeavesInjected"]) + " leaves were injected; "
                        "the sweep did not run to completion")
    parts = sweep["admittedCensusCounters"] + sweep["admittedOutsideTheCensusBlock"]
    if jx_bind(parts, sweep["admittedToAFullGreenRun"]) is not None:
        findings.append("C2V9-SWEEP: the census and non-census admissions sum to " +
                        str(parts) + " but " + str(sweep["admittedToAFullGreenRun"]) +
                        " leaves were admitted")
    if not jx_int_in_range(sweep["admittedOutsideTheCensusBlock"], 1, 10 ** 6):
        findings.append("C2V9-SWEEP: no leaf OUTSIDE the census block drives the pinned "
                        "predecessor to a fully green run, so the measured claim that "
                        "three sites was not the complete set is no longer reproduced")
    missing = jx_sorted(jx_difference(list(SWEEP_ANCHOR_PATHS), sweep["outsidePaths"]))
    if missing:
        findings.append("C2V9-SWEEP: the sweep no longer finds " + repr(missing) +
                        " admitted to a fully green predecessor run; the sharpest of "
                        "these is the upper bound inside the predecessor's own "
                        "integer-constant register, and a sweep that stops seeing it "
                        "has stopped measuring the thing it is cited for")
    return findings


def successor_differential(authority, candidate) -> dict:
    """L6c.  The v5 REJECT's blocking vectors, executed against the PINNED v5.

    This is what stands behind the repair without trusting anything this file
    believes about itself.  check-c2-v5.py is pinned; it cannot change; it still
    admits every one of these to a fully green run.  v8 must name each.
    """
    cached = jx_get(authority.pinned, "v5admissions")
    if cached is None:
        cached = _v5_admissions(authority)
        jx_put(authority.pinned, "v5admissions", cached)
    rows, escapes = [], []
    admitted = rejected = 0
    for vector, v5_path, v9_path, spelling, note in SUCCESSOR_DIFFERENTIAL_VECTORS:
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
            current = _resolve_steps(mutant, v9_path)
        except MALFORMED_SHAPE_EXCEPTIONS:
            escapes.append(vector + ": " + _steps_text(v9_path) + " does not resolve in "
                           "this candidate, so the vector is not retained as an "
                           "executable case")
            rows.append({"vector": vector, "path": _steps_text(v9_path), "note": note,
                         "v5FullyGreen": v5_green, "v9NamedThePosition": False})
            continue
        value = float(current) if jx_equal(spelling, "float-equal") else \
            (True if jx_equal(spelling, "boolean-true") else 1)
        _assign_steps(mutant, v9_path, value)
        findings = candidate_probe_findings(mutant, authority)
        named = bool([item for item in findings if _steps_text(v9_path) in item])
        if named:
            rejected += 1
        else:
            escapes.append(vector + ": this checker did NOT name " +
                           _steps_text(v9_path) + " when it was spelled " + spelling)
        rows.append({"vector": vector, "path": _steps_text(v9_path), "note": note,
                     "v5FullyGreen": v5_green, "v9NamedThePosition": named})
    return {"vectors": len(SUCCESSOR_DIFFERENTIAL_VECTORS), "rows": rows,
            "v5AdmittedToAFullGreenRun": admitted, "v9RejectedByName": rejected,
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
            v5 = _execute_snapshot("opensip_c2v9_pinned_v5_checker", V5_CHECKER,
                                   authority.snapshots[V5_CHECKER], authority.directory)
            v5_authority = v5.load_authority(authority.directory)
    except BaseException as exc:                        # noqa: BLE001 - measured
        return [{"vector": vector, "fullyGreen": None,
                 "why": "the pinned v5 checker could not be executed: " +
                        type(exc).__name__ + ": " + str(exc)}
                for vector, _a, _b, _c, _d in SUCCESSOR_DIFFERENTIAL_VECTORS]
    contract = authority.json(V5_CONTRACT)
    for vector, v5_path, _v9_path, spelling, _note in SUCCESSOR_DIFFERENTIAL_VECTORS:
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
# Section 8b.  L6d -- the ENUMERATION differential, against the PINNED v7.
#
# IR-C2V7-01.  The repair is not a boolean walker, so the evidence cannot be
# "a boolean is now enumerated".  What is measured, on every invocation and
# against hash-verified bytes, is the MECHANISM: the pinned check-c2-v7.py's own
# candidate enumeration -- `_integer_leaf_steps` and `_number_leaf_steps`, read
# out of its verified snapshot and executed -- does not reach a leaf of any
# other JSON type, while `jx_leaf_census` reaches every one of them.  The
# predecessor's blindness is therefore recomputed every run rather than
# asserted, and it cannot change, because those bytes are pinned.
#
# The CONTROL rows matter as much as the blind ones: the pinned v7 enumeration
# must still REACH an integer and a number leaf, or this differential would be
# measuring a broken snapshot rather than a known blind spot.
#
# What an ordinary invocation does NOT do is execute check-c2-v7.py over the
# one-byte edit; that costs about eighty seconds.  It is a retained --selftest
# row (`pinned_v7_over_a_boolean_flip`), which must still find it FULLY GREEN.
# RES-C2V9-11 records that split, in the artifact, as v7 recorded its own.
# =============================================================================

# The byte-level edit that IS IR-C2V7-01: one token, ONE BYTE, in the pinned v7
# document, flipping that document's own claim that the v7 lane reproduced
# IR-C2V6-01 -- the single finding v7 existed to discharge.  The anchor carries
# the following line too, because that key occurs twice in that document and the
# other occurrence is followed by EXHAUSTIVE rather than MECHANISM.
PINNED_V7_BOOLEAN_EDIT = (
    '      "reproducedByThisLane": true,\n      "reproducedPerRun": "MECHANISM"',
    '      "reproducedByThisLane": false,\n      "reproducedPerRun": "MECHANISM"',
    ["theParseDefect", "minimalReproduction", "reproducedByThisLane"],
)

# (id, steps into the pinned v7 document, the value to write, the JSON type it
#  introduces, whether the pinned v7 enumeration is EXPECTED to reach it, note)
ENUMERATION_DIFFERENTIAL_VECTORS = (
    ("IR-C2V7-01-boolean-flip-at-the-IR-C2V6-01-reproduction-claim",
     ["theParseDefect", "minimalReproduction", "reproducedByThisLane"], False,
     "boolean", False,
     "the v7 REJECT\'s own minimal reproduction: one byte, no source modification, "
     "exit 0 and a full green banner still reading `with no unbound bucket`"),
    ("IR-C2V7-01-boolean-flip-at-the-IR-C2V4-01-reproduction-claim",
     ["theDefect", "minimalReproduction", "reproducedByThisLane"], False,
     "boolean", False,
     "the twin claim, for the disposition the whole chain is anchored to"),
    ("IR-C2V7-01-new-boolean-leaf-at-the-document-root",
     ["c2v8InjectedBooleanLeaf"], True, "boolean", False,
     "a boolean leaf nobody binds, added at the root"),
    ("IR-C2V7-01-new-boolean-leaf-at-depth",
     ["theDefect", "c2v8InjectedBooleanLeaf"], False, "boolean", False,
     "the same leaf at depth, so the gap is not a property of the root"),
    ("OBS-C2V7-09-new-null-leaf-at-the-document-root",
     ["c2v8InjectedNullLeaf"], None, "null", False,
     "the null spelling, which the v7 reviewer measured green and scoped as "
     "honestly declared; v8 closes it with the same mechanism"),
    ("OBS-C2V7-09-new-string-leaf-at-the-document-root",
     ["c2v8InjectedStringLeaf"], "x", "string", False,
     "the string spelling, which RES-C2V7-07 named and did not close"),
    ("CONTROL-integer-leaf-the-pinned-v7-enumeration-does-reach",
     ["c2v8InjectedIntegerLeaf"], 17, "integer", True,
     "the control: v7 refused this one by name, and if it stopped doing so this "
     "differential would be measuring a broken snapshot rather than a blind spot"),
    ("CONTROL-number-leaf-the-pinned-v7-enumeration-does-reach",
     ["c2v8InjectedNumberLeaf"], 17.0, "number", True,
     "the second control, and the leaf OBS-C2V6-01 was about"),
)


def _pinned_v7_module(authority):
    """The pinned check-c2-v7.py, executed from its VERIFIED snapshot.

    Cached on `external` rather than on `pinned`, because it is a pure function
    of hash-verified bytes and of nothing this file can change.
    """
    cached = jx_get(authority.external, "v7-module")
    if cached is not None:
        return cached
    sink = io.StringIO()
    with redirect_stdout(sink):
        module = _execute_snapshot("opensip_c2v9_pinned_v7_checker", V7_CHECKER,
                                   authority.snapshots[V7_CHECKER],
                                   authority.directory)
    jx_put(authority.external, "v7-module", module)
    return module


def enumeration_differential(authority) -> dict:
    """L6d.  The pinned v7's own enumeration, executed over each vector."""
    rows, escapes = [], []
    blind = enumerated = controls = controls_reached = 0
    try:
        module = _pinned_v7_module(authority)
    except BaseException as exc:                        # noqa: BLE001 - measured
        return {"vectors": len(ENUMERATION_DIFFERENTIAL_VECTORS), "rows": [],
                "controls": 0, "predecessorBlind": 0, "predecessorReachedControls": 0,
                "successorEnumerated": 0, "bytesAdded": 0, "mutantDigest": "",
                "escapes": ["the pinned " + V7_CHECKER + " could not be executed (" +
                            type(exc).__name__ + ": " + str(exc) + "), so the "
                            "enumeration differential is not measured this run"]}
    document = authority.json(V7_CONTRACT)
    for vector, steps, value, kind, reached, _note in ENUMERATION_DIFFERENTIAL_VECTORS:
        mutant = copy.deepcopy(document)
        try:
            _assign_steps(mutant, steps, copy.deepcopy(value))
        except MALFORMED_SHAPE_EXCEPTIONS:
            escapes.append(vector + ": " + _steps_text(steps) + " cannot be written "
                           "into the pinned v7 document, so the retained vector is not "
                           "executable against those bytes")
            continue
        try:
            predecessor = list(module._integer_leaf_steps(mutant)) + \
                list(module._number_leaf_steps(mutant))
        except BaseException as exc:                    # noqa: BLE001 - measured
            escapes.append(vector + ": the pinned v7 enumeration raised " +
                           type(exc).__name__)
            continue
        seen_by_v7 = jx_in(list(steps), predecessor)
        seen_by_v8 = [row for row in jx_leaf_census(mutant)
                      if jx_equal(row[0], list(steps)) and jx_equal(row[1], kind)]
        if reached:
            controls += 1
            if seen_by_v7:
                controls_reached += 1
            else:
                escapes.append(vector + ": the pinned v7 enumeration no longer reaches "
                               "a JSON " + kind + " leaf either, so this differential "
                               "is measuring a broken snapshot and not a blind spot")
        elif seen_by_v7:
            escapes.append(vector + ": the pinned v7 enumeration DOES reach the JSON " +
                           kind + " leaf at " + _steps_text(steps) + ", so the "
                           "mechanism IR-C2V7-01 records has changed")
        else:
            blind += 1
        if seen_by_v8:
            enumerated += 1
        else:
            escapes.append(vector + ": this checker's own leaf census does NOT report a "
                           "JSON " + kind + " leaf at " + _steps_text(steps) + ", so "
                           "the repair is not doing the thing it exists to do")
        rows.append({"vector": vector, "path": _steps_text(steps), "type": kind,
                     "predecessorEnumeratedIt": bool(seen_by_v7),
                     "predecessorExpectedToReachIt": bool(reached),
                     "successorEnumeratedIt": bool(seen_by_v8)})
    needle, replacement, _position = PINNED_V7_BOOLEAN_EDIT
    original = authority.snapshots[V7_CONTRACT].decode("utf-8")
    added, digest = 0, ""
    if jx_int_in_range(original.count(needle), 1, 1):
        edited = original.replace(needle, replacement, 1)
        added = len(edited.encode("utf-8")) - len(original.encode("utf-8"))
        digest = hashlib.sha256(edited.encode("utf-8")).hexdigest()
    else:
        escapes.append("the one-byte boolean edit's anchor text does not occur exactly "
                       "once in the pinned " + V7_CONTRACT + ", so the headline "
                       "reproduction is not executable against those bytes")
    return {"vectors": len(ENUMERATION_DIFFERENTIAL_VECTORS), "rows": rows,
            "controls": controls, "predecessorBlind": blind,
            "predecessorReachedControls": controls_reached,
            "successorEnumerated": enumerated, "bytesAdded": added,
            "mutantDigest": digest, "escapes": escapes}


def enumeration_findings(authority) -> list:
    result = authority.enumeration_differential
    findings = ["C2V9-ENUMERATION: " + item for item in result["escapes"]]
    expected_blind = result["vectors"] - result["controls"]
    if jx_bind(result["predecessorBlind"], expected_blind) is not None:
        findings.append(
            "C2V9-ENUMERATION: " + str(result["predecessorBlind"]) + " of the " +
            str(expected_blind) + " non-control vectors still show the pinned " +
            V7_CHECKER + " enumeration unable to reach the leaf; that blindness is "
            "what IR-C2V7-01 records and it is recomputed here rather than restated")
    if jx_bind(result["successorEnumerated"], result["vectors"]) is not None:
        findings.append(
            "C2V9-ENUMERATION: this checker's leaf census reached " +
            str(result["successorEnumerated"]) + " of " + str(result["vectors"]) +
            " retained vectors; a totality that misses one of them is v7's totality "
            "with a different list")
    if jx_bind(result["predecessorReachedControls"], result["controls"]) is not None:
        findings.append(
            "C2V9-ENUMERATION: the pinned predecessor reached " +
            str(result["predecessorReachedControls"]) + " of " +
            str(result["controls"]) + " CONTROL vectors, so this differential can no "
            "longer be shown to be measuring a blind spot rather than a broken "
            "snapshot")
    if not jx_int_in_range(result["bytesAdded"], 1, 1):
        findings.append(
            "C2V9-ENUMERATION: the headline reproduction is recorded as adding " +
            str(result["bytesAdded"]) + " byte(s) to the pinned " + V7_CONTRACT +
            "; IR-C2V7-01 is a ONE-BYTE edit and the bright line it was graded under "
            "is the size of that edit")
    return findings


# =============================================================================
# Section 8c.  L6e -- the SKELETON differential, against the PINNED v8.
#
# IR-C2V8-01.  The repair is one line, so the evidence cannot be "the digest
# changed".  What is measured, on every invocation and against hash-verified
# bytes, is the MECHANISM: the pinned check-c2-v8.py's OWN `document_skeleton`,
# read out of its verified snapshot and executed, gives the ORIGINAL pinned v8
# document and a reparented mutant of it the SAME digest, while this checker's
# gives them different ones.  The predecessor's blindness is recomputed every
# run rather than asserted, and it cannot change, because those bytes are
# pinned.
#
# The CONTROL rows matter as much as the blind ones: the pinned v8 skeleton must
# still MOVE for an edit that carries no `/` collision, or this differential
# would be measuring a broken snapshot rather than a known blind spot.
#
# What an ordinary invocation does NOT do is execute check-c2-v8.py over the
# +11-byte edit; that costs about eighty seconds.  It is a retained --selftest
# row (`pinned_v8_over_a_path_collision`), which must still find it FULLY GREEN.
# RES-C2V9-11 records that split, in the artifact.
# =============================================================================

# The byte-level edit that IS IR-C2V8-01: ONE contiguous replacement in the
# pinned v8 document, +11 bytes, zero bytes of Python, relocating that document's
# own account of why the enumeration is a gate out of `thePrimitive` and onto a
# root key named with the literal text of its old path.  Expressed as an opener
# and a closer so the narrative VALUE between them is never transcribed: a
# reproduction that carried a second copy of the bytes it edits would be the
# recording obligation's own failure mode.
PINNED_V8_PATH_COLLISION_EDIT = (
    ',\n    "theEnumerationIsAGateToo": ',
    '\n  },\n  "guardInventory": {',
    '\n  },\n  "thePrimitive/theEnumerationIsAGateToo": ',
    ',\n  "guardInventory": {',
    ["thePrimitive", "theEnumerationIsAGateToo"],
)

# (id, steps into the pinned v8 document, operation, whether the pinned v8
#  skeleton is EXPECTED to move, note).  REPARENT is the collision: the node is
#  removed and reinserted as a ROOT key named with the `/`-join of its old path,
#  positioned immediately after its own top-level ancestor so that even the WALK
#  ORDER is preserved.  Every REPARENT row is a position at which this lane
#  measured, by execution, that the pinned v8 digest does not move.
SKELETON_DIFFERENTIAL_VECTORS = (
    ("IR-C2V8-01-narrative-leaf-reparented-across-a-slash",
     ["thePrimitive", "theEnumerationIsAGateToo"], "reparent", False,
     "the +11-byte headline: that document\'s own account of why the enumeration "
     "is a gate, moved out of the block that gives it meaning, with the pinned v8 "
     "digest and all of 945/148/797 byte-identical and a full green banner"),
    ("IR-C2V8-01-the-defect-block-s-own-rationale-reparented",
     ["theDefect", "whyThisIsBlockingAndNotAdvisory"], "reparent", False,
     "the reviewer\'s second independent reproduction: that document\'s own account "
     "of why the lineage\'s founding finding was BLOCKING rather than advisory"),
    ("IR-C2V8-01-a-whole-container-subtree-reparented",
     ["derivedFrom", "operations"], "reparent", False,
     "a 141-node array, not a leaf: the class covers whole subtrees and the v8 "
     "skeleton is the only layer advertised as seeing their shape"),
    ("IR-C2V8-01-a-narrative-leaf-at-the-end-of-a-limitations-block",
     ["knownLimitations", "residualsAreInTheArtifactAndNotInProse"], "reparent", False,
     "a third position, in the block whose whole job is to be accurate about what "
     "the artifact is NOT"),
    ("CONTROL-a-new-root-key-that-carries-no-slash",
     ["c2v9SkeletonControlLeaf"], "add-root-key", True,
     "the control: an added leaf with no `/` collision available MUST move the "
     "pinned v8 digest, or this differential is measuring a broken snapshot "
     "rather than a blind spot"),
    ("CONTROL-a-leaf-retyped-in-place",
     ["documentSkeleton", "nodes"], "retype-leaf", True,
     "the second control: v8 binds PATH and TYPE, and the TYPE half was never in "
     "question; it must still move the digest"),
)


def _skeleton_reparent(document, steps):
    """Remove the node at `steps` and reinsert it as a ROOT key named with the
    `/`-join of its old path, immediately after its own top-level ancestor.

    This is the shape of IR-C2V8-01 as a STRUCTURAL edit rather than a byte one.
    Position matters: `document_skeleton` is an ordered list, so a relocation
    that also preserved the walk order is what made the v8 digest byte-identical
    rather than merely equal as a set.
    """
    parent = document
    for step in list(steps)[:-1]:
        parent = jx_at(parent, step)
    if jx_type(parent) != "object" or not jx_has_at(parent, list(steps)[-1]):
        return None
    value = copy.deepcopy(jx_at(parent, list(steps)[-1]))
    del parent[list(steps)[-1]]
    key = _steps_text(steps)
    if jx_has(document, key):
        return None
    out = {}
    for name in list(document):
        jx_put(out, name, jx_at(document, name))
        if jx_equal(name, list(steps)[0]):
            jx_put(out, key, value)
    return out


def _skeleton_mutant(document, steps, operation):
    """The mutant a skeleton-differential vector describes.  Returns None if the
    vector cannot be applied to those bytes, which is itself an escape."""
    mutant = copy.deepcopy(document)
    if jx_equal(operation, "reparent"):
        return _skeleton_reparent(mutant, steps)
    if jx_equal(operation, "add-root-key"):
        if jx_has(mutant, list(steps)[0]):
            return None
        jx_put(mutant, list(steps)[0], "x")
        return mutant
    if jx_equal(operation, "retype-leaf"):
        try:
            current = _resolve_steps(mutant, list(steps))
        except MALFORMED_SHAPE_EXCEPTIONS:
            return None
        _assign_steps(mutant, list(steps), str(current))
        return mutant
    return None


def _pinned_v8_module(authority):
    """The pinned check-c2-v8.py, executed from its VERIFIED snapshot."""
    cached = jx_get(authority.external, "v8-module")
    if cached is not None:
        return cached
    sink = io.StringIO()
    with redirect_stdout(sink):
        module = _execute_snapshot("opensip_c2v9_pinned_v8_checker", V8_CHECKER,
                                   authority.snapshots[V8_CHECKER],
                                   authority.directory)
    jx_put(authority.external, "v8-module", module)
    return module


def skeleton_differential(authority) -> dict:
    """L6e.  The pinned v8\'s own skeleton, executed over each vector."""
    rows, escapes = [], []
    blind = separated = controls = controls_moved = 0
    try:
        module = _pinned_v8_module(authority)
    except BaseException as exc:                        # noqa: BLE001 - measured
        return dict(_EMPTY_SKELETON_DIFFERENTIAL,
                    vectors=len(SKELETON_DIFFERENTIAL_VECTORS),
                    escapes=["the pinned " + V8_CHECKER + " could not be executed (" +
                             type(exc).__name__ + ": " + str(exc) + "), so the "
                             "skeleton differential is not measured this run"])
    document = authority.json(V8_CONTRACT)
    try:
        clean_predecessor = module.document_skeleton_digest(document)
    except BaseException as exc:                        # noqa: BLE001 - measured
        return dict(_EMPTY_SKELETON_DIFFERENTIAL,
                    vectors=len(SKELETON_DIFFERENTIAL_VECTORS),
                    escapes=["the pinned " + V8_CHECKER + " could not skeletonise its "
                             "own document (" + type(exc).__name__ + ")"])
    clean_successor = document_skeleton_digest(document)
    for vector, steps, operation, moves, _note in SKELETON_DIFFERENTIAL_VECTORS:
        mutant = _skeleton_mutant(document, steps, operation)
        if mutant is None:
            escapes.append(vector + ": " + _steps_text(steps) + " cannot be " +
                           operation + "ed in the pinned v8 document, so the retained "
                           "vector is not executable against those bytes")
            continue
        try:
            predecessor_moved = jx_ne(module.document_skeleton_digest(mutant),
                                      clean_predecessor)
        except BaseException as exc:                    # noqa: BLE001 - measured
            escapes.append(vector + ": the pinned v8 skeleton raised " +
                           type(exc).__name__)
            continue
        successor_moved = jx_ne(document_skeleton_digest(mutant), clean_successor)
        if moves:
            controls += 1
            if predecessor_moved:
                controls_moved += 1
            else:
                escapes.append(vector + ": the pinned v8 skeleton does not move for an "
                               "edit that carries no path collision either, so this "
                               "differential is measuring a broken snapshot and not a "
                               "blind spot")
        elif predecessor_moved:
            escapes.append(vector + ": the pinned v8 skeleton DOES move when " +
                           _steps_text(steps) + " is reparented across a `/` boundary, "
                           "so the mechanism IR-C2V8-01 records has changed")
        else:
            blind += 1
        if successor_moved:
            separated += 1
        else:
            escapes.append(vector + ": THIS checker\'s skeleton does not move when " +
                           _steps_text(steps) + " is " + operation + "ed, so the repair "
                           "is not doing the thing it exists to do")
        rows.append({"vector": vector, "path": _steps_text(steps),
                     "operation": operation,
                     "predecessorSkeletonMoved": bool(predecessor_moved),
                     "predecessorExpectedToMove": bool(moves),
                     "successorSkeletonMoved": bool(successor_moved)})
    opener, closer, new_open, new_close, _position = PINNED_V8_PATH_COLLISION_EDIT
    original = authority.snapshots[V8_CONTRACT].decode("utf-8")
    added, digest = 0, ""
    if jx_int_in_range(original.count(opener), 1, 1) and \
            jx_int_in_range(original.count(closer), 1, 1):
        head = original.index(opener)
        tail = original.index(closer, head)
        edited = (original[:head] + new_open +
                  original[head + len(opener):tail] + new_close +
                  original[tail + len(closer):])
        added = len(edited.encode("utf-8")) - len(original.encode("utf-8"))
        digest = hashlib.sha256(edited.encode("utf-8")).hexdigest()
    else:
        escapes.append("the +11-byte reparenting edit\'s anchor text does not occur "
                       "exactly once in the pinned " + V8_CONTRACT + ", so the headline "
                       "reproduction is not executable against those bytes")
    return {"vectors": len(SKELETON_DIFFERENTIAL_VECTORS), "rows": rows,
            "controls": controls, "predecessorBlind": blind,
            "predecessorMovedControls": controls_moved,
            "successorSeparated": separated, "bytesAdded": added,
            "mutantDigest": digest, "escapes": escapes}


def skeleton_findings(authority) -> list:
    result = authority.skeleton_differential
    findings = ["C2V9-SKELDIFF: " + item for item in result["escapes"]]
    expected_blind = result["vectors"] - result["controls"]
    if jx_bind(result["predecessorBlind"], expected_blind) is not None:
        findings.append(
            "C2V9-SKELDIFF: " + str(result["predecessorBlind"]) + " of the " +
            str(expected_blind) + " non-control vectors still show the pinned " +
            V8_CHECKER + " skeleton unable to see the reparenting; that blindness is "
            "what IR-C2V8-01 records and it is recomputed here rather than restated")
    if jx_bind(result["successorSeparated"], result["vectors"]) is not None:
        findings.append(
            "C2V9-SKELDIFF: this checker\'s skeleton separated " +
            str(result["successorSeparated"]) + " of " + str(result["vectors"]) +
            " retained vectors; a path identity that misses one of them is v8\'s "
            "identity with a longer name")
    if jx_bind(result["predecessorMovedControls"], result["controls"]) is not None:
        findings.append(
            "C2V9-SKELDIFF: the pinned predecessor moved for " +
            str(result["predecessorMovedControls"]) + " of " + str(result["controls"]) +
            " CONTROL vectors, so this differential can no longer be shown to be "
            "measuring a blind spot rather than a broken snapshot")
    if not jx_int_in_range(result["bytesAdded"], 11, 11):
        findings.append(
            "C2V9-SKELDIFF: the headline reproduction is recorded as adding " +
            str(result["bytesAdded"]) + " byte(s) to the pinned " + V8_CONTRACT +
            "; IR-C2V8-01 is a +11-BYTE contiguous edit and the bright line it was "
            "graded under is the size of that edit")
    return findings


_EMPTY_SKELETON_DIFFERENTIAL = {"vectors": 0, "rows": [], "controls": 0,
                                "predecessorBlind": 0, "predecessorMovedControls": 0,
                                "successorSeparated": 0, "bytesAdded": 0,
                                "mutantDigest": "", "escapes": []}


# =============================================================================
# Section 9.  The measured register, and a banner that cannot carry a number the
# run did not compute.
#
# This is the repair for OBS-01 and for the sweep half of IR-C2V5-03.  In v5 the
# banner's headline figures were literal f-string text: the reviewer republished
# the contract to 1 / 1 / 1 / 0 and the run stayed green with the banner
# unchanged, still asserting 136 / 57 / 32.
#
# In v8 there is no f-string in the banner.  Every line is a TEMPLATE rendered
# by `str.format_map` over the live register, so a number can only reach the
# banner by being looked up under the name of the thing it claims to measure --
# and a template naming a key the run does not measure raises rather than
# printing.  A separate structural check refuses any template that carries a
# digit outside an alphanumeric token, so `0 type-distinct admissions` cannot be
# written as text at all.  L7 breaks both halves.
# =============================================================================

# Fields the banner carries that CANNOT be bound to the candidate.  The elapsed
# time differs between runs; the candidate's own byte length cannot be published
# INSIDE the candidate without the digits changing the length they report.  Both
# are declared, and `banner_findings` refuses any run-only field that is not.
RUNTIME_ONLY_FIELDS = ("candidateDocumentBytes", "sweepElapsedSeconds")


def live_register(authority) -> dict:
    """Every number this run measured, under the name of what it measures."""
    positions = measured_positions(authority.measurement)
    scan, pre, v5s = authority.scan_self, authority.scan_predecessor, authority.scan_v5
    beh, lock = authority.behavioural, authority.document_lock
    cand, sweep = authority.candidate_lock, authority.sweep
    diff, succ, prim = authority.differential, authority.successor, authority.primitive
    parse, probe = authority.parse_scan, authority.parse_probe
    parsediff, declared = authority.parse_differential, authority.declared_strings
    truthiness = authority.truthiness
    ledger = authority.candidate_ledger if authority.candidate_ledger else _EMPTY_LEDGER
    totality = authority.candidate_totality
    enumdiff = (authority.enumeration_differential
                if authority.enumeration_differential else _EMPTY_ENUMERATION)
    skeldiff = (authority.skeleton_differential
                if authority.skeleton_differential else _EMPTY_SKELETON_DIFFERENTIAL)
    identity = authority.path_identity
    agreement = authority.census_agreement
    depth = authority.parse_depth if authority.parse_depth else {"depth": 0, "named": 0}
    tokens = (authority.pinned_number_tokens if authority.pinned_number_tokens
              else {"files": 0, "tokens": 0})
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
        "primitiveOrderPairs": prim["orderPairs"],
        "primitiveOrderEqualityDivergences": prim["orderEqualityDivergences"],
        "primitiveParseCases": prim["parseCases"],
        "primitiveParseControls": prim["parseControls"],
        "primitiveParseNamedAtThePosition": prim["parseNamedAtThePosition"],
        "primitiveParseAdmissions": prim["parseAdmissions"],
        "primitiveFreeNamesOutsideTheBoundary": authority.portability["freeNames"],
        "effectiveIntegerLeavesTypeLocked": lock["lockedLeaves"],
        "effectiveTypeProbeCases": lock["executedCases"],
        "effectiveTypeProbeNamedRejections": lock["namedTypeRejections"],
        "effectiveTypeProbeAdmissions": lock["admissions"],
        # L2c.  The TOTAL leaf ledger.  IR-C2V7-01.
        "candidateBoundLeafBindings": cand["boundLeaves"],
        "candidateProbeCases": cand["executedCases"],
        "candidateProbeAdmissions": cand["admissions"],
        "candidateSpellingTypes": jx_get(cand, "spellingTypes", 0),
        "candidateNodes": ledger["nodes"],
        "candidateContainers": ledger["containers"],
        "candidateLeaves": ledger["leaves"],
        "candidateLeavesNull": jx_get(ledger["counts"], "null", 0),
        "candidateLeavesBoolean": jx_get(ledger["counts"], "boolean", 0),
        "candidateLeavesInteger": jx_get(ledger["counts"], "integer", 0),
        "candidateLeavesNumber": jx_get(ledger["counts"], "number", 0),
        "candidateLeavesString": jx_get(ledger["counts"], "string", 0),
        "candidateLeavesBound": ledger["bound"],
        "candidateNarrativeStringLeaves": ledger["narrative"],
        "candidateLeavesUnbound": ledger["unbound"],
        "candidateLeavesUnruled": ledger["unruled"],
        "candidateTotalityCases": totality["executedCases"],
        "candidateTotalityNamed": totality["namedRejections"],
        "candidateTotalityAdmissions": totality["admissions"],
        "candidateTotalityNamedBySkeletonOnly": totality["namedBySkeletonOnly"],
        "candidateTotalityTypes": totality["typesCovered"],
        # The primitive's own measurement of the type space the ledger stands on.
        "primitiveTypeSpaceWitnesses": prim["typeSpaceWitnesses"],
        "primitiveTypeSpaceDeclaredTypes": prim["typeSpaceDeclaredTypes"],
        "primitiveTypeSpaceRealisedTypes": prim["typeSpaceRealisedTypes"],
        "primitiveTypeSpaceContainerTypes": prim["typeSpaceContainerTypes"],
        "primitiveTypeSpaceScalarTypes": prim["typeSpaceScalarTypes"],
        "primitiveTypeSpaceUnwitnessedTypes": prim["typeSpaceUnwitnessedTypes"],
        "primitiveTypeSpaceRfcProductions": prim["typeSpaceRfcProductions"],
        "primitiveTypeSpaceCases": prim["typeSpaceCases"],
        "primitiveTypeSpaceAdmissions": prim["typeSpaceAdmissions"],
        # L6d.  The enumeration differential against the pinned v7.
        "enumerationDifferentialVectors": enumdiff["vectors"],
        "enumerationDifferentialControls": enumdiff["controls"],
        "enumerationPredecessorBlind": enumdiff["predecessorBlind"],
        "enumerationPredecessorReachedControls": enumdiff["predecessorReachedControls"],
        "enumerationSuccessorEnumerated": enumdiff["successorEnumerated"],
        "enumerationDifferentialBytesAdded": enumdiff["bytesAdded"],
        # L6e.  The skeleton differential against the pinned v8.  IR-C2V8-01.
        "skeletonDifferentialVectors": skeldiff["vectors"],
        "skeletonDifferentialControls": skeldiff["controls"],
        "skeletonPredecessorBlind": skeldiff["predecessorBlind"],
        "skeletonPredecessorMovedControls": skeldiff["predecessorMovedControls"],
        "skeletonSuccessorSeparated": skeldiff["successorSeparated"],
        "skeletonDifferentialBytesAdded": skeldiff["bytesAdded"],
        # Path identity, measured over this document and over the defect corpus.
        "pathIdentityPairs": identity["pairs"],
        "pathIdentityCollidesUnderTheJoinedText":
            identity["collidesUnderTheJoinedText"],
        "pathIdentitySeparatesUnderTheCanonicalToken":
            identity["separatesUnderTheCanonicalToken"],
        "pathIdentityPathsInverted": identity["pathsInverted"],
        "pathIdentityDistinctPathTokens": identity["distinctPathTokens"],
        "pathIdentityDistinctJoinedTexts": identity["distinctJoinedTexts"],
        "pathIdentityStepPairs": identity["stepPairs"],
        "pathIdentityStepPairsColliding":
            identity["stepPairsCollidingUnderTheJoinedText"],
        "pathIdentityStepPairsSeparated":
            identity["stepPairsSeparatedByTheCanonicalToken"],
        "candidateRootSubtreesBound": authority.root_subtrees,
        # The census measured against the node walk, over the real document.
        "censusWalkNodes": agreement["walkNodes"],
        "censusWalkLeaves": agreement["walkLeaves"],
        "censusLeavesAgreed": agreement["agreed"],
        "candidateTotalityLocalisedToASubtree": totality["localisedToASubtree"],
        "primitiveTypeSpacePlacements": prim["typeSpacePlacements"],
        "primitiveTypeSpaceGrammarTexts": prim["typeSpaceGrammarTexts"],
        "primitiveTypeSpaceGrammarProductions": prim["typeSpaceGrammarProductions"],
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
        "successorV9RejectedByName": succ["v9RejectedByName"],
        "sweepIntegerLeavesInjected": sweep["integerLeavesInjected"],
        "sweepAdmittedToFullGreen": sweep["admittedToAFullGreenRun"],
        "sweepRejectedByPredecessor": sweep["rejectedByPredecessor"],
        "sweepAdmittedCensusCounters": sweep["admittedCensusCounters"],
        "sweepAdmittedOutsideCensus": sweep["admittedOutsideTheCensusBlock"],
        "selftestContractMutations": len(CONTRACT_MUTATIONS),
        "selftestSourceMutations": len(SOURCE_MUTATIONS),
        "selftestScanMutations": len(SCAN_MUTATIONS),
        "selftestParseMutations": len(PARSE_MUTATIONS),
        "pinnedInputs": len(PINS),
        "declaredTypeGates": len(GUARD_HELPERS),
        # L8 -- parse integrity.
        "parseJsonLoadSites": parse["sites"],
        "parseHookedLoadSites": parse["hooked"],
        "parseDeclaredHazardSites": parse["declaredHazardSites"],
        "parseDeclaredPredecessorParses": parse["declaredPredecessorParses"],
        "parseUngatedLoadSites": len(parse["ungated"]),
        "parsePredecessorLoadSites": jx_get(parse["predecessors"], V6_CHECKER)["sites"],
        "parsePredecessorHookedLoadSites":
            jx_get(parse["predecessors"], V6_CHECKER)["hooked"],
        "parseProbeCases": probe["executedCases"],
        "parseProbeNamedAtThePosition": probe["namedAtThePosition"],
        "parseProbeControls": probe["controls"],
        "parseProbeAdmissions": probe["admissions"],
        "parseDifferentialVectors": parsediff["vectors"],
        "parseDifferentialBytesAdded":
            parsediff["rows"][0]["bytesAdded"] if parsediff["rows"] else 0,
        "parseDifferentialPredecessorBlind": parsediff["predecessorParseBlind"],
        "parseDifferentialSuccessorNamed": parsediff["successorNamedByPosition"],
        "parseDeclaredUnhookedSites": parse["declaredUnhookedSites"],
        "parseEvasionSites": len(parse["evasions"]),
        "parseDepthProbeDepth": depth["depth"],
        "parseDepthNamedAtThePosition": depth["named"],
        "parsePinnedJsonInputs": tokens["files"],
        "parsePinnedNumberTokens": tokens["tokens"],
        # L9 -- the declared strings.
        "declaredAssertionRows": declared["rows"],
        "declaredFindingIds": declared["findingIds"],
        "declaredSubjectsInSource": declared["inSource"],
        "declaredSubjectsInDocument": declared["inDocument"],
        "declaredSubjectsProvedAtEmitSite": declared["atEmitSite"],
        "declaredSubjectsUnresolved": declared["unresolved"],
        "declaredPrimitiveNamesChecked": declared["namesChecked"],
        "declaredPrimitiveNamesUndefined": declared["namesUndefined"],
        # The bare-truthiness measurement.  Published, bound, not a finding.
        "scanSelfBareTruthinessSites": jx_get(truthiness, "self"),
        "scanPredecessorBareTruthinessSites": jx_get(truthiness, V6_CHECKER),
    }


BANNER_TEMPLATES = (
    "C-2 v9 contract OK - {documentName}; IR-C2V4-01 and the four blocking findings "
    "of the v5 REJECT repaired at the comparison primitive, IR-C2V6-01 repaired at the "
    "PARSE, IR-C2V7-01 repaired at the ENUMERATION - which names no scalar type and "
    "derives its coverage from the JSON data model - IR-C2V7-02 repaired by making "
    "the duplicate-path walk iterative, and IR-C2V8-01 repaired at the IDENTITY: the "
    "skeleton binds jx_canon of the STEPS LIST rather than a slash-join of it, so two "
    "distinct paths can no longer share one name; {pinnedInputs} inputs hash-verified "
    "before "
    "execution, and the pinned check-c2-v4.py executed from its verified snapshot as "
    "the inherited oracle over the v4-identity projection",
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
    "  L2c candidate-document TOTAL leaf ledger, over the JSON data model and not "
    "over a list of types: this document holds {candidateNodes} nodes, of which "
    "{candidateContainers} are containers and {candidateLeaves} are leaves - "
    "{candidateLeavesNull} null, {candidateLeavesBoolean} boolean, "
    "{candidateLeavesInteger} integer, {candidateLeavesNumber} number and "
    "{candidateLeavesString} string.  {candidateLeavesBound} leaves are bound to a "
    "value this run measured or to a verified pinned byte, "
    "{candidateNarrativeStringLeaves} are string leaves declared NARRATIVE and counted, "
    "{candidateLeavesUnbound} are unbound and {candidateLeavesUnruled} are of a JSON "
    "type this checker has no disposition rule for; the leaf census names no scalar "
    "type at all, so its coverage is the data model's",
    "  L2c totality, measured over the TYPE SPACE: the primitive realises "
    "{primitiveTypeSpaceRealisedTypes} JSON types from "
    "{primitiveTypeSpaceWitnesses} witnesses over "
    "{primitiveTypeSpaceRfcProductions} productions of the JSON data model, with "
    "{primitiveTypeSpaceUnwitnessedTypes} declared type(s) unwitnessed; the leaf "
    "census descends through {primitiveTypeSpaceContainerTypes} of them and reports "
    "{primitiveTypeSpaceScalarTypes} as leaves, and {primitiveTypeSpaceAdmissions} are "
    "neither.  {candidateTotalityCases} live injections of a leaf of every one of "
    "{candidateTotalityTypes} JSON types at unbound paths at the root and at depth, of "
    "which {candidateTotalityNamed} were named ({candidateTotalityNamedBySkeletonOnly} "
    "by the document skeleton rather than by the value ledger, which is every narrative "
    "string and every empty container) and {candidateTotalityAdmissions} were admitted; "
    "and "
    "{candidateProbeCases} hostile-spelling, value-drift and control probes at "
    "{candidateBoundLeafBindings} bound leaves using a witness of every one of "
    "{candidateSpellingTypes} JSON types, of which {candidateProbeAdmissions} were "
    "admitted",
    "  L6d enumeration differential, the repair for IR-C2V7-01: "
    "{enumerationDifferentialVectors} retained vectors against the PINNED "
    "check-c2-v7.py, {enumerationDifferentialControls} of them CONTROLS the "
    "predecessor must still reach.  Its own leaf enumeration cannot reach "
    "{enumerationPredecessorBlind} of the non-control vectors and does reach "
    "{enumerationPredecessorReachedControls} of the controls, while this checker's "
    "census reports {enumerationSuccessorEnumerated} of "
    "{enumerationDifferentialVectors}; the headline reproduction adds "
    "{enumerationDifferentialBytesAdded} byte to the pinned v7 document",
    "  L6e skeleton differential, the repair for IR-C2V8-01: "
    "{skeletonDifferentialVectors} retained vectors against the PINNED "
    "check-c2-v8.py, {skeletonDifferentialControls} of them CONTROLS whose skeleton "
    "the predecessor must still move.  Its own path-and-type skeleton cannot see "
    "{skeletonPredecessorBlind} of the non-control reparentings and does move for "
    "{skeletonPredecessorMovedControls} of the controls, while this checker's "
    "separates {skeletonSuccessorSeparated} of {skeletonDifferentialVectors}; the "
    "headline reproduction adds {skeletonDifferentialBytesAdded} bytes to the pinned "
    "v8 document",
    "  path identity, executed rather than asserted: over {pathIdentityPairs} document "
    "pairs the joined-text encoding v8 hashed conflates "
    "{pathIdentityCollidesUnderTheJoinedText} and this checker's canonical path token "
    "separates {pathIdentitySeparatesUnderTheCanonicalToken}, and over "
    "{pathIdentityStepPairs} PATH pairs it conflates {pathIdentityStepPairsColliding} "
    "and this checker separates {pathIdentityStepPairsSeparated}; every one of "
    "{pathIdentityPathsInverted} paths of this document inverts through jx_decanon "
    "back to the steps the walk produced, and its {censusWalkNodes} nodes carry "
    "{pathIdentityDistinctPathTokens} distinct path tokens against "
    "{pathIdentityDistinctJoinedTexts} distinct joined texts.  The leaf census is "
    "measured against the node walk over THIS document and not at one shallow probe: "
    "{censusWalkLeaves} leaves, {censusLeavesAgreed} agreed; the type space is "
    "measured at {primitiveTypeSpacePlacements} placements down a depth ladder, and "
    "its productions by PARSING {primitiveTypeSpaceGrammarTexts} JSON texts into "
    "{primitiveTypeSpaceGrammarProductions} productions.  The shape is localised to "
    "{candidateRootSubtreesBound} bound root-subtree digests, and "
    "{candidateTotalityLocalisedToASubtree} of the "
    "{candidateTotalityNamedBySkeletonOnly} injections the value ledger does not name "
    "are named at their containing root subtree rather than only by a digest over the "
    "whole document",
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
    "named {successorV9RejectedByName} at the analogous position of its own document",
    "  L8 parse integrity, the repair for IR-C2V6-01: the candidate was read as "
    "{candidateDocumentBytes} inert bytes whose sha256 is {candidateDigest}, and THOSE "
    "bytes are what every layer above read; every duplicate key at any depth, every "
    "non-RFC constant and every number token whose spelling is not the canonical "
    "spelling of its value is a named finding at its position, in EVERY input this "
    "checker parses and not only in the candidate; structurally this file holds "
    "{parseJsonLoadSites} JSON parse call site(s), which decompose exactly as "
    "{parseHookedLoadSites} passing an object_pairs_hook plus "
    "{parseDeclaredHazardSites} declared operator-space hazard demonstrations plus "
    "{parseDeclaredPredecessorParses} declared reproductions of the predecessor's own "
    "unhooked parse plus {parseUngatedLoadSites} ungated - so "
    "{parseDeclaredUnhookedSites} sites do NOT pass a hook and every one of them is "
    "declared and counted, against {parsePredecessorHookedLoadSites} hooked of "
    "{parsePredecessorLoadSites} in the pinned check-c2-v6.py; "
    "{parseEvasionSites} site(s) reach the decoder by a shape the structural scan "
    "cannot match; a duplicate key nested {parseDepthProbeDepth} objects deep is named "
    "at its full path {parseDepthNamedAtThePosition} time(s); the number-token scanner "
    "reads {parsePinnedNumberTokens} tokens out of the bytes of "
    "{parsePinnedJsonInputs} pinned JSON inputs; {parseProbeCases} live parse probes "
    "including {parseProbeControls} controls, of which {parseProbeAdmissions} were "
    "admitted",
    "  L8 parse differential: {parseDifferentialVectors} retained duplicate-key vectors "
    "against pinned documents; an unhooked host parse cannot distinguish the edited "
    "bytes from the unedited ones in {parseDifferentialPredecessorBlind} of them, which "
    "is exactly why check-c2-v6.py printed a full green banner over the eighteen-byte "
    "edit, and this checker named {parseDifferentialSuccessorNamed} at the position",
    "  L9 declared strings: {declaredAssertionRows} retained assertion rows over "
    "{declaredFindingIds} finding ids; {declaredSubjectsProvedAtEmitSite} subject(s) "
    "are proved at the emit site of the finding they assert on, "
    "{declaredSubjectsInSource} occur in this file outside the assertion tables, "
    "{declaredSubjectsInDocument} only in the candidate document and "
    "{declaredSubjectsUnresolved} nowhere; {declaredPrimitiveNamesChecked} primitive "
    "names are named by the docstring or the candidate and "
    "{declaredPrimitiveNamesUndefined} of them do not exist",
    "  measured and NOT a finding: {scanSelfBareTruthinessSites} bare-truthiness site(s) "
    "on a tainted operand in this file and {scanPredecessorBareTruthinessSites} in the "
    "pinned check-c2-v6.py; every one this run inspected is a container or a syntax "
    "tree where truthiness is emptiness, the count is bound so it cannot drift "
    "silently, and the scope is RES-C2V9-09 rather than a guard nobody could keep green",
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
            "C2V9-BANNER: the bare-digit detector does not fire on " +
            repr(BANNER_DETECTOR_PROBE[0]) + ", so its clean verdict over the real "
            "templates is a statement about an instrument that detects nothing")
    rendered = render_banner(("probe {sweepIntegerLeavesInjected} probe",),
                             live, runtime) if jx_has(live, "sweepIntegerLeavesInjected") \
        else ["probe {sweepIntegerLeavesInjected} probe"]
    if "{" in rendered[0] or "}" in rendered[0]:
        findings.append(
            "C2V9-BANNER: the renderer left an uninterpolated field in " +
            repr(rendered[0]) + ", so the banner would print the NAME of a measurement "
            "instead of the measurement")
    for token in jx_sorted(jx_unique(banner_digit_tokens(BANNER_TEMPLATES))):
        findings.append(
            "C2V9-BANNER: the banner carries the literal figure " + repr(token) +
            " as source text; a number the run does not recompute and bind is not "
            "evidence, and v5's banner asserted its headline sweep figures over a "
            "contract that had been republished to contradict them")
    referenced = []
    for template in BANNER_TEMPLATES:
        referenced.extend(_FIELD_RE.findall(template))
    available = list(live) + list(runtime)
    unknown = jx_sorted(jx_difference(jx_unique(referenced), available))
    for key in unknown:
        findings.append("C2V9-BANNER: the banner interpolates " + key + ", which this "
                        "run does not measure")
    if not jx_int_in_range(len(jx_unique(referenced)), 1, 10 ** 6):
        findings.append("C2V9-BANNER: the banner interpolates nothing, so every figure "
                        "in it would be source text")
    declared = jx_sorted(list(RUNTIME_ONLY_FIELDS))
    if not jx_equal(jx_sorted(list(runtime)), declared):
        findings.append("C2V9-BANNER: the run-only banner fields are " +
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

REQUIRED_RESIDUAL_IDS = ("RES-C2V9-01", "RES-C2V9-02", "RES-C2V9-03", "RES-C2V9-04",
                         "RES-C2V9-05", "RES-C2V9-06", "RES-C2V9-07", "RES-C2V9-08",
                         "RES-C2V9-09", "RES-C2V9-10", "RES-C2V9-11", "RES-C2V9-12",
                         "RES-C2V9-13", "RES-C2V9-14", "RES-C2V9-15", "RES-C2V9-16",
                         "RES-C2V9-17", "RES-C2V9-18", "RES-C2V9-19")
# OBS-C2V8-03.  v8 accepted RETAINED and RETAINED-OPEN interchangeably, so the
# ONE residual the author designated genuinely open -- the one the reviewer
# called the first that names the real hazard -- could be downgraded to
# RETAINED by a single edit to a green run.  The open set is declared here and
# required in BOTH directions: an id in it that is not RETAINED-OPEN, and an id
# outside it that is, are each a named finding.
OPEN_RESIDUAL_IDS = ("RES-C2V9-15", "RES-C2V9-17")
# OBS-C2V8-02.  v8 CLAIMED that "every residual carries a MEASURED BOUNDARY
# clause citing bound counters".  It was false -- RES-C2V8-11 carried none and
# cited zero counters -- and nothing in the checker enforced it: the whole
# requirement was that `whyNotClosed` be 40 characters long.  The clause is now
# a REQUIRED FIELD, it must carry this literal text, and it must name at least
# one key of the live register, so a boundary stated as an adjective is a
# finding rather than a house style.
MEASURED_BOUNDARY_CLAUSE = "MEASURED BOUNDARY"
# A residual that plainly fails the rule, so that the rule returning nothing over
# the real list is distinguishable from a rule that has stopped looking.
RESIDUAL_BOUNDARY_DETECTOR_PROBE = {
    "id": "RES-DETECTOR-PROBE", "status": "RETAINED",
    "title": "a residual whose boundary is an adjective",
    "whyNotClosed": "it is stated in prose and its size is described rather than "
                    "measured, which is the shape OBS-C2V8-02 recorded",
    "whatStandsInFrontOfIt": "nothing measurable",
    "measuredBoundary": "the exposure here is small and well understood",
}
REQUIRED_LAYER_IDS = ("L0", "L1", "L2", "L2b", "L2c", "L3", "L4", "L5", "L6", "L6b",
                      "L6c", "L6d", "L6e", "L7", "L8", "L9")
DISCHARGED_FINDING_IDS = ("IR-C2V4-01", "IR-C2V5-01", "IR-C2V5-02", "IR-C2V5-03",
                          "IR-C2V5-04", "IR-C2V6-01", "IR-C2V7-01", "IR-C2V7-02",
                          "IR-C2V8-01")


def _identity_findings(c) -> list:
    findings = []
    if jx_bind_text(c.get("artifact"), ARTIFACT_ID) is not None:
        findings.append("C2V9: candidate is not " + ARTIFACT_ID)
    if not jx_exact_int(c.get("version"), 9) or not jx_exact_int(c.get("supersedes"), 8):
        findings.append("C2V9: candidate must declare version 9 superseding 8 as JSON "
                        "integers; a float or boolean spelling is refused by the same "
                        "rule this successor exists to enforce")
    status = c.get("status")
    status = status if jx_type(status) == "string" else ""
    if "CANDIDATE-NOT-APPLIED" not in status or "AWAITING-INDEPENDENT-REVIEW" not in status:
        findings.append("C2V9: candidate status must remain CANDIDATE-NOT-APPLIED / "
                        "AWAITING-INDEPENDENT-REVIEW")
    resolves = c.get("resolves")
    resolves = resolves if jx_type(resolves) == "object" else {}
    for finding_id in DISCHARGED_FINDING_IDS:
        if not jx_has(resolves, finding_id):
            findings.append("C2V9: the candidate does not name " + finding_id +
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
            findings.append("C2V9-INVENTORY: layer " + repr(layer.get("id")) +
                            " publishes no blind spot; a guard inventory claiming total "
                            "coverage is refused")
    if not jx_equal(jx_sorted(jx_unique(seen)), jx_sorted(list(REQUIRED_LAYER_IDS))):
        findings.append("C2V9-INVENTORY: the guard inventory declares layers " +
                        repr(jx_sorted(seen)) + ", not the " +
                        repr(jx_sorted(list(REQUIRED_LAYER_IDS))) + " this checker "
                        "carries")
    behind = inventory.get("whatStandsBehindTheBackstop")
    behind = behind if jx_type(behind) == "string" else ""
    if not jx_int_in_range(len(behind), 80, 10 ** 6):
        findings.append("C2V9-INVENTORY: the inventory does not state what stands behind "
                        "the behavioural backstop, which is the structural question the "
                        "adjudication graded BLOCKING")
    terminal = inventory.get("terminalLayerAndWhatStandsBehindIt")
    terminal = terminal if jx_type(terminal) == "string" else ""
    if "nothing" not in terminal.lower():
        findings.append("C2V9-INVENTORY: the inventory does not state plainly that the "
                        "terminal layer has nothing behind it but independent review")
    return findings


def _residual_boundary_problems(item, live) -> list:
    """OBS-C2V8-02, ENFORCED.  What a residual owes, checked rather than claimed.

    Returns the reasons ONE residual fails the discipline this artifact holds
    itself to.  It is a separate function so that the SAME predicate can be run
    over `RESIDUAL_BOUNDARY_DETECTOR_PROBE`, which must fail it -- a rule that
    reports nothing over the real list and would also report nothing over a
    plainly non-compliant one is a rule that has stopped looking.
    """
    problems = []
    boundary = item.get("measuredBoundary")
    boundary = boundary if jx_type(boundary) == "string" else ""
    if MEASURED_BOUNDARY_CLAUSE not in boundary:
        problems.append("carries no " + MEASURED_BOUNDARY_CLAUSE + " clause; v8 claimed "
                        "every residual had one and one of them had none at all, and "
                        "nothing in v8 checked")
        return problems
    cited = [key for key in jx_sorted(list(live)) if key in boundary]
    if not jx_int_in_range(len(cited), 1, 10 ** 6):
        problems.append("states a " + MEASURED_BOUNDARY_CLAUSE + " that names none of "
                        "the " + str(len(live)) + " counters this run measures and "
                        "binds, so its boundary is a sentence rather than a number")
    return problems


def _residual_findings(c, live) -> list:
    findings = []
    residuals = c.get("residuals")
    residuals = residuals if jx_type(residuals) == "array" else []
    ids = [item.get("id") for item in residuals if jx_type(item) == "object"]
    missing = jx_sorted(jx_difference(list(REQUIRED_RESIDUAL_IDS), ids))
    if missing:
        findings.append("C2V9-RESIDUAL: the candidate does not retain " + repr(missing) +
                        "; a residual that is absorbed rather than retained is the "
                        "corpus's dominant failure mode")
    # The detector, probed.  OBS-C2V8-02.
    if not jx_int_in_range(len(_residual_boundary_problems(
            RESIDUAL_BOUNDARY_DETECTOR_PROBE, live)), 1, 10 ** 6):
        findings.append(
            "C2V9-RESIDUAL: the measured-boundary rule admits " +
            repr(RESIDUAL_BOUNDARY_DETECTOR_PROBE["measuredBoundary"]) + ", so its "
            "clean verdict over the real residual list is a statement about an "
            "instrument that detects nothing")
    for item in residuals:
        if jx_type(item) != "object":
            continue
        status = item.get("status")
        if not jx_in(status, ["RETAINED", "RETAINED-OPEN"]):
            findings.append("C2V9-RESIDUAL: " + repr(item.get("id")) + " is not RETAINED")
        # OBS-C2V8-03.  BOTH DIRECTIONS.
        expected_open = jx_in(item.get("id"), list(OPEN_RESIDUAL_IDS))
        is_open = jx_equal(status, "RETAINED-OPEN")
        if expected_open and not is_open:
            findings.append(
                "C2V9-RESIDUAL: " + repr(item.get("id")) + " is declared OPEN by this "
                "checker and the candidate carries " + repr(status) + "; v8 treated "
                "the two spellings as interchangeable and the one residual its "
                "reviewer called the first to name the real hazard could be "
                "downgraded by a single edit to a fully green run")
        if is_open and not expected_open:
            findings.append(
                "C2V9-RESIDUAL: " + repr(item.get("id")) + " is carried as "
                "RETAINED-OPEN and this checker does not declare it open; the "
                "distinction has to be measured in both directions or it is prose")
        for reason in _residual_boundary_problems(item, live):
            findings.append("C2V9-RESIDUAL: " + repr(item.get("id")) + " " + reason)
        why = item.get("whyNotClosed")
        why = why if jx_type(why) == "string" else ""
        if not jx_int_in_range(len(why), 40, 10 ** 6):
            findings.append("C2V9-RESIDUAL: " + repr(item.get("id")) + " does not say "
                            "why it is not closed")
        front = item.get("whatStandsInFrontOfIt")
        front = front if jx_type(front) == "string" else ""
        if not jx_int_in_range(len(front), 20, 10 ** 6):
            findings.append("C2V9-RESIDUAL: " + repr(item.get("id")) + " does not say "
                            "what stands in front of it")
    # The COUNT, bound to the list.  v6 was described to its coordinator as
    # carrying "ten retained residuals including the incomplete selftest": it
    # carried seven, eleven counting knownLimitations, and the incomplete
    # selftest was disclosed in prose to the coordinator and never written into
    # the artifact at all.  A residual disclosed conversationally is not
    # retained.  The count is now published IN the document and bound to the
    # document, so it cannot be overstated to anybody.
    accounting = c.get("residualAccounting")
    if jx_type(accounting) != "object":
        findings.append("C2V9-RESIDUAL: the candidate publishes no residualAccounting "
                        "block, so its own residual count is unbound and can be "
                        "overstated in prose to a coordinator the way v6's was")
    return findings


def _recording_findings(c) -> list:
    """Freeze 7.2: filename AND digest for every input.  A count is not a record."""
    findings = []
    recorded = c.get("recordedInputs")
    recorded = recorded if jx_type(recorded) == "array" else []
    names = [item.get("filename") for item in recorded if jx_type(item) == "object"]
    missing = jx_sorted(jx_difference(list(PINS), names))
    if missing:
        findings.append("C2V9-RECORD: " + str(len(missing)) + " pinned input(s) are "
                        "executed or parsed by this checker but carry no record: " +
                        repr(missing))
    for item in recorded:
        if jx_type(item) != "object":
            continue
        name = item.get("filename")
        if jx_has(PINS, name):
            reason = jx_bind_text(item.get("sha256"), jx_get(PINS, name))
            if reason is not None:
                findings.append("C2V9-RECORD: " + str(name) + ": " + reason +
                                "; the recorded digest is not the digest this run "
                                "verified")
        role = item.get("role")
        role = role if jx_type(role) == "string" else ""
        if not jx_int_in_range(len(role), 12, 10 ** 6):
            findings.append("C2V9-RECORD: " + repr(name) + " is recorded without a role, "
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
    if jx_bind_text(mode.get("checker"), "check-c2-v9.py") is not None or \
            not jx_equal(jx_sorted(list(codes)), jx_sorted(list(DECLARED_EXIT_CODES))) or \
            "REFUSED" not in refusal:
        findings.append("C2V9: the checker mode contract does not declare exactly the "
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
        findings.append("C2V9-REPRO: the minimal reproduction is not recorded as "
                        "requiring no source modification, which is the whole reason "
                        "IR-C2V4-01 is BLOCKING rather than advisory")
    if jx_bind_text(repro.get("predecessorSha256"), jx_get(PINS, V4_CHECKER)) is not None:
        findings.append("C2V9-REPRO: the reproduction is recorded against " +
                        repr(repro.get("predecessorSha256")) + ", not the verified "
                        "predecessor digest " + jx_get(PINS, V4_CHECKER))
    sites = defect.get("repairedComparisonSites")
    sites = sites if jx_type(sites) == "array" else []
    lines = []
    for index, site in enumerate(sites):
        value = site.get("line") if jx_type(site) == "object" else None
        if not jx_int(value):
            findings.append(
                "C2V9-TYPE: theDefect/repairedComparisonSites/" + str(index) +
                "/line is published as " + repr(value) + ", whose JSON type is " +
                jx_type(value) + ", not the JSON integer the pinned adjudication names; "
                "this is the exact position and the exact spelling of IR-C2V5-01, where "
                "a set-subset test admitted it with one JSON edit and no source change")
            continue
        lines.append(value)
    adjudicated = adjudicated_census_lines(authority)
    if not jx_subset(adjudicated, lines):
        findings.append("C2V9-REPRO: the candidate enumerates comparison sites " +
                        repr(jx_sorted(lines)) + " but the pinned adjudication names " +
                        repr(jx_sorted(adjudicated)))
    successor = c.get("theSuccessorDefect")
    successor = successor if jx_type(successor) == "object" else {}
    vectors = successor.get("vectors")
    vectors = vectors if jx_type(vectors) == "array" else []
    declared = [item.get("id") for item in vectors if jx_type(item) == "object"]
    expected = [vector for vector, _a, _b, _c, _d in SUCCESSOR_DIFFERENTIAL_VECTORS]
    if not jx_equal(jx_sorted(jx_unique(declared)), jx_sorted(jx_unique(expected))):
        findings.append("C2V9-REPRO: the candidate records successor false-accept "
                        "vectors " + repr(jx_sorted(declared)) + " but this run executes "
                        + repr(jx_sorted(expected)) + "; a retained vector that is not "
                        "executed is prose")
    return findings


def _parse_repro_findings(c, authority) -> list:
    """IR-C2V6-01 must be RECORDED, and recorded as what it is."""
    findings = []
    defect = c.get("theParseDefect")
    defect = defect if jx_type(defect) == "object" else {}
    if jx_bind_text(defect.get("findingId"), "IR-C2V6-01") is not None or \
            jx_bind_text(defect.get("disposition"), "BLOCKING") is not None:
        findings.append("C2V9-PARSE-REPRO: the candidate does not record IR-C2V6-01 as "
                        "the BLOCKING finding this successor exists to discharge")
    repro = defect.get("minimalReproduction")
    repro = repro if jx_type(repro) == "object" else {}
    if jx_bind_text(repro.get("sourceModification"), "NONE") is not None:
        findings.append("C2V9-PARSE-REPRO: the minimal reproduction is not recorded as "
                        "requiring no source modification, which is the whole reason "
                        "IR-C2V6-01 is BLOCKING rather than advisory")
    if jx_bind_text(repro.get("predecessorSha256"), jx_get(PINS, V6_CHECKER)) is not None:
        findings.append("C2V9-PARSE-REPRO: the reproduction is recorded against " +
                        repr(repro.get("predecessorSha256")) + ", not the verified "
                        "predecessor digest " + jx_get(PINS, V6_CHECKER))
    if jx_bind_text(repro.get("inputSha256"), jx_get(PINS, V6_CONTRACT)) is not None:
        findings.append("C2V9-PARSE-REPRO: the reproduction is recorded against " +
                        repr(repro.get("inputSha256")) + ", not the verified document "
                        "digest " + jx_get(PINS, V6_CONTRACT))
    perrun = repro.get("reproducedPerRun")
    perrun = perrun if jx_type(perrun) == "string" else ""
    if jx_bind_text(perrun, "MECHANISM") is not None:
        findings.append("C2V9-PARSE-REPRO: the candidate must say plainly WHICH HALF of "
                        "this reproduction an ordinary invocation recomputes; v6's "
                        "lineage grades a published measurement the run does not "
                        "recompute as not evidence, and overclaiming here would be the "
                        "same defect in a new place")
    vectors = defect.get("vectors")
    vectors = vectors if jx_type(vectors) == "array" else []
    declared = [item.get("id") for item in vectors if jx_type(item) == "object"]
    expected = [vector for vector, _a, _b, _c, _d, _e in PARSE_DIFFERENTIAL_VECTORS]
    if not jx_equal(jx_sorted(jx_unique(declared)), jx_sorted(jx_unique(expected))):
        findings.append("C2V9-PARSE-REPRO: the candidate records parse vectors " +
                        repr(jx_sorted(declared)) + " but this run executes " +
                        repr(jx_sorted(expected)) + "; a retained vector that is not "
                        "executed is prose")
    return findings


def _enumeration_repro_findings(c, authority) -> list:
    """IR-C2V7-01 must be RECORDED, and recorded as what it is."""
    findings = []
    defect = c.get("theEnumerationDefect")
    defect = defect if jx_type(defect) == "object" else {}
    if jx_bind_text(defect.get("findingId"), "IR-C2V7-01") is not None or \
            jx_bind_text(defect.get("disposition"), "BLOCKING") is not None:
        findings.append("C2V9-ENUM-REPRO: the candidate does not record IR-C2V7-01 as "
                        "the BLOCKING finding this successor exists to discharge")
    repro = defect.get("minimalReproduction")
    repro = repro if jx_type(repro) == "object" else {}
    if jx_bind_text(repro.get("sourceModification"), "NONE") is not None:
        findings.append("C2V9-ENUM-REPRO: the minimal reproduction is not recorded as "
                        "requiring no source modification, which is the whole reason "
                        "IR-C2V7-01 is BLOCKING rather than advisory")
    if jx_bind_text(repro.get("predecessorSha256"),
                    jx_get(PINS, V7_CHECKER)) is not None:
        findings.append("C2V9-ENUM-REPRO: the reproduction is recorded against " +
                        repr(repro.get("predecessorSha256")) + ", not the verified "
                        "predecessor digest " + jx_get(PINS, V7_CHECKER))
    if jx_bind_text(repro.get("inputSha256"), jx_get(PINS, V7_CONTRACT)) is not None:
        findings.append("C2V9-ENUM-REPRO: the reproduction is recorded against " +
                        repr(repro.get("inputSha256")) + ", not the verified document "
                        "digest " + jx_get(PINS, V7_CONTRACT))
    if jx_bind_text(repro.get("reproducedPerRun"), "MECHANISM") is not None:
        findings.append("C2V9-ENUM-REPRO: the candidate must say plainly WHICH HALF of "
                        "this reproduction an ordinary invocation recomputes; the full "
                        "execution of the pinned check-c2-v7.py over the one-byte edit "
                        "is a retained --selftest row and not a per-run measurement, "
                        "and overclaiming here would be the same defect in a new place")
    if jx_bind_text(repro.get("mutantSha256"),
                    jx_get(authority.enumeration_differential, "mutantDigest",
                           "")) is not None:
        findings.append("C2V9-ENUM-REPRO: the candidate records the one-byte mutant of "
                        "the pinned v7 document as " + repr(repro.get("mutantSha256")) +
                        ", and this run computed " +
                        repr(jx_get(authority.enumeration_differential, "mutantDigest",
                                    "")) + " by performing the edit on the pinned "
                        "bytes; a reproduction recorded against a digest nobody "
                        "recomputes is prose")
    vectors = defect.get("vectors")
    vectors = vectors if jx_type(vectors) == "array" else []
    declared = [item.get("id") for item in vectors if jx_type(item) == "object"]
    expected = [vector for vector, _a, _b, _c, _d, _e
                in ENUMERATION_DIFFERENTIAL_VECTORS]
    if not jx_equal(jx_sorted(jx_unique(declared)), jx_sorted(jx_unique(expected))):
        findings.append("C2V9-ENUM-REPRO: the candidate records enumeration vectors " +
                        repr(jx_sorted(declared)) + " but this run executes " +
                        repr(jx_sorted(expected)) + "; a retained vector that is not "
                        "executed is prose")
    return findings


def _skeleton_repro_findings(c, authority) -> list:
    """IR-C2V8-01 must be RECORDED, and recorded as what it is."""
    findings = []
    defect = c.get("theSkeletonDefect")
    defect = defect if jx_type(defect) == "object" else {}
    if jx_bind_text(defect.get("findingId"), "IR-C2V8-01") is not None or \
            jx_bind_text(defect.get("disposition"), "BLOCKING") is not None:
        findings.append("C2V9-SKEL-REPRO: the candidate does not record IR-C2V8-01 as "
                        "the BLOCKING finding this successor exists to discharge")
    repro = defect.get("minimalReproduction")
    repro = repro if jx_type(repro) == "object" else {}
    if jx_bind_text(repro.get("sourceModification"), "NONE") is not None:
        findings.append("C2V9-SKEL-REPRO: the minimal reproduction is not recorded as "
                        "requiring no source modification, which is the whole reason "
                        "IR-C2V8-01 is BLOCKING rather than advisory")
    if jx_bind_text(repro.get("predecessorSha256"),
                    jx_get(PINS, V8_CHECKER)) is not None:
        findings.append("C2V9-SKEL-REPRO: the reproduction is recorded against " +
                        repr(repro.get("predecessorSha256")) + ", not the verified "
                        "predecessor digest " + jx_get(PINS, V8_CHECKER))
    if jx_bind_text(repro.get("inputSha256"), jx_get(PINS, V8_CONTRACT)) is not None:
        findings.append("C2V9-SKEL-REPRO: the reproduction is recorded against " +
                        repr(repro.get("inputSha256")) + ", not the verified document "
                        "digest " + jx_get(PINS, V8_CONTRACT))
    if jx_bind_text(repro.get("reproducedPerRun"), "MECHANISM") is not None:
        findings.append("C2V9-SKEL-REPRO: the candidate must say plainly WHICH HALF of "
                        "this reproduction an ordinary invocation recomputes; the full "
                        "execution of the pinned check-c2-v8.py over the +11-byte edit "
                        "is a retained --selftest row and not a per-run measurement, "
                        "and overclaiming here would be the same defect in a new place")
    if jx_bind_text(repro.get("mutantSha256"),
                    jx_get(authority.skeleton_differential, "mutantDigest",
                           "")) is not None:
        findings.append("C2V9-SKEL-REPRO: the candidate records the +11-byte mutant of "
                        "the pinned v8 document as " + repr(repro.get("mutantSha256")) +
                        ", and this run computed " +
                        repr(jx_get(authority.skeleton_differential, "mutantDigest",
                                    "")) + " by performing the edit on the pinned "
                        "bytes; a reproduction recorded against a digest nobody "
                        "recomputes is prose")
    vectors = defect.get("vectors")
    vectors = vectors if jx_type(vectors) == "array" else []
    declared = [item.get("id") for item in vectors if jx_type(item) == "object"]
    expected = [vector for vector, _a, _b, _c, _d in SKELETON_DIFFERENTIAL_VECTORS]
    if not jx_equal(jx_sorted(jx_unique(declared)), jx_sorted(jx_unique(expected))):
        findings.append("C2V9-SKEL-REPRO: the candidate records skeleton vectors " +
                        repr(jx_sorted(declared)) + " but this run executes " +
                        repr(jx_sorted(expected)) + "; a retained vector that is not "
                        "executed is prose")
    return findings


def _disclaimer_findings(c) -> list:
    """OBS-C2V7-05, made a finding rather than only fixed.

    v7's `knownLimitations.thisIsNotAVerdict` read "A green run of check-c2-v6.py
    is authored by the same lane that authored the repair."  The version bump was
    missed exactly once, so the document of record disclaimed a green run of the
    checker that had been REJECTED and said nothing about the green run it was
    actually asking a reader to discount.  L9 could not catch it -- the string
    `check-c2-v6.py` occurs legitimately twenty-one times in that document -- and
    that is exactly the class RES-C2V9-10 concedes L9 does not close.  A guard
    that names the specific place is what closes it here.
    """
    findings = []
    limitations = c.get("knownLimitations")
    limitations = limitations if jx_type(limitations) == "object" else {}
    text = limitations.get("thisIsNotAVerdict")
    text = text if jx_type(text) == "string" else ""
    if "check-c2-v9.py" not in text:
        findings.append(
            "C2V9-DISCLAIMER: knownLimitations/thisIsNotAVerdict does not name "
            "check-c2-v9.py, the checker whose green run it exists to discount; v7's "
            "named check-c2-v6.py, the REJECTED predecessor, and nothing in that "
            "artifact could see it")
    for predecessor in (V4_CHECKER, V5_CHECKER, V6_CHECKER, V7_CHECKER, V8_CHECKER):
        if predecessor in text:
            findings.append(
                "C2V9-DISCLAIMER: knownLimitations/thisIsNotAVerdict names " +
                predecessor + ", a predecessor checker; the one block in this artifact "
                "whose whole job is to be accurate about what the artifact is NOT may "
                "not disclaim somebody else's run")
    return findings


ADOPTION_AVAILABILITY_CLAUSE = "availability only"


def _adoption_findings(c) -> list:
    """OBS-C2V7-03, finished.  The v7 reviewer\'s sentence was that the parse
    gate\'s placement inside the primitive means an adopter cannot take the
    comparison and leave the parse `only of availability, not of use`.  v8
    repaired the SUBSTANCE and the v8 reviewer measured that the phrase itself
    occurred NOWHERE in either file, so the adoption text said the right thing in
    different words and the words were the thing under review.  Both files now
    carry it, and a guard requires it -- because a wording repair nobody executes
    is exactly the class this lineage keeps rediscovering."""
    findings = []
    source = own_source().decode("utf-8", "replace").lower()
    if ADOPTION_AVAILABILITY_CLAUSE not in source:
        findings.append(
            "C2V9-ADOPTION: this checker\'s own adoption step does not say " +
            repr(ADOPTION_AVAILABILITY_CLAUSE) + "; the v8 reviewer measured that the "
            "substance was present and the words were not, and the words are what an "
            "adopter reads")
    primitive = c.get("thePrimitive")
    primitive = primitive if jx_type(primitive) == "object" else {}
    corpus = []
    for value in [primitive.get("theParseIsAGateToo")] + \
            list(primitive.get("whatAnAdoptingCheckerMustDo") or []):
        if jx_type(value) == "string":
            corpus.append(value.lower())
    if not [item for item in corpus if ADOPTION_AVAILABILITY_CLAUSE in item]:
        findings.append(
            "C2V9-ADOPTION: the candidate\'s adoption text does not say " +
            repr(ADOPTION_AVAILABILITY_CLAUSE) + " anywhere in thePrimitive; the "
            "property that is true of the parse gate\'s placement is AVAILABILITY and "
            "not USE, and stating it any other way is the overclaim OBS-C2V7-03 named")
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
            prefix = "C2V9-TYPE" if not jx_int(published) else "C2V9-CANDIDATE"
            findings.append(prefix + ": " + _steps_text(record["steps"]) + ": " + reason)
    return findings


def differential_findings(authority) -> list:
    result = authority.differential
    findings = ["C2V9-DIFFERENTIAL: " + item for item in result["escapes"]]
    if jx_bind(result["successorRejectedByName"], result["vectors"]) is not None:
        findings.append("C2V9-DIFFERENTIAL: " + str(result["successorRejectedByName"]) +
                        " of " + str(result["vectors"]) + " retained false-accept "
                        "vectors were rejected by name")
    if not jx_int_in_range(result["predecessorAdmittedThePosition"], 1, 10 ** 6):
        findings.append("C2V9-DIFFERENTIAL: the pinned predecessor named every vector "
                        "position, so the differential is vacuous; either the "
                        "predecessor's bytes are not the adjudicated ones or this layer "
                        "has stopped measuring anything")
    if not jx_int_in_range(result["predecessorFullyGreenRuns"], 1, 10 ** 6):
        findings.append("C2V9-DIFFERENTIAL: no retained vector reproduces the "
                        "adjudication's headline - a fully green predecessor run over a "
                        "defective document - so the repair is no longer demonstrably "
                        "load-bearing")
    successor = authority.successor
    findings.extend("C2V9-SUCCESSOR: " + item for item in successor["escapes"])
    if jx_bind(successor["v9RejectedByName"], successor["vectors"]) is not None:
        findings.append("C2V9-SUCCESSOR: " + str(successor["v9RejectedByName"]) + " of " +
                        str(successor["vectors"]) + " blocking vectors from the pinned "
                        "v5 REJECT were named by this checker at the analogous position "
                        "of its own document")
    if not jx_int_in_range(successor["v5AdmittedToAFullGreenRun"], 1, 10 ** 6):
        findings.append("C2V9-SUCCESSOR: the pinned check-c2-v5.py admits none of its "
                        "own blocking vectors to a fully green run, so the differential "
                        "this repair is measured against has collapsed and the repair is "
                        "no longer demonstrably load-bearing")
    return findings


_EMPTY_SUCCESSOR = {"vectors": 0, "rows": [], "v5AdmittedToAFullGreenRun": 0,
                    "v9RejectedByName": 0, "escapes": []}


def _banner_register(live, document_name, own_digest, candidate_digest) -> dict:
    """The register the banner renders from: every measured number, plus the two
    STRING labels.  Built through the primitive so no key can collide with
    another under host-language equality."""
    out = {}
    for key in jx_sorted(list(live)):
        jx_put(out, key, jx_get(live, key))
    jx_put(out, "documentName", document_name)
    jx_put(out, "ownDigest", own_digest)
    # Freeze 7.2 binds BYTES.  IR-C2V6-01's sharpest sentence is that the bytes
    # of record and the object certified were different documents and the
    # divergence was invisible from the banner.  It is not invisible now.
    jx_put(out, "candidateDigest", candidate_digest)
    return out


_EMPTY_PRIMITIVE = {
    "corpusValues": 0, "corpusPairs": 0, "roundTrips": 0, "distinctTokens": 0,
    "tokenCollisions": 0, "stricterThanHostEquality": 0, "looserThanHostEquality": 0,
    "agreeWithHostEquality": 0, "reflexiveFailures": 0, "crossTypeAdmissions": 0,
    "gateCases": 0, "gateAdmissions": 0, "operatorSpaceRows": 0,
    "operatorSpaceHazardsReproduced": 0, "operatorSpaceRowsCovered": 0,
    "entryPointCases": 0, "entryPointFailures": 0, "domainRefusals": 0,
    "orderPairs": 0, "orderEqualityDivergences": 0, "parseCases": 0,
    "parseControls": 0, "parseNamedAtThePosition": 0, "parseAdmissions": 0,
    "callShapedRowsDeclared": 0, "typeSpaceWitnesses": 0,
    "typeSpaceDeclaredTypes": 0, "typeSpaceRealisedTypes": 0,
    "typeSpaceContainerTypes": 0, "typeSpaceScalarTypes": 0,
    "typeSpaceUnwitnessedTypes": 0, "typeSpaceRfcProductions": 0,
    "typeSpaceCases": 0, "typeSpaceAdmissions": 0, "typeSpacePlacements": 0,
    "typeSpaceGrammarTexts": 0, "typeSpaceGrammarProductions": 0, "escapes": [],
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
    """Total boundary: malformed parsed JSON becomes a named finding.

    L8's findings about the candidate's BYTES are emitted here rather than
    inside `_check`, because every early return below it is a path on which the
    bytes-versus-parse divergence would otherwise be dropped, and a defence that
    survives only the happy path is not a defence.
    """
    parsed_bytes = list(authority.parse_findings)
    if jx_type(c) != "object" or not c:
        return parsed_bytes + [
            "C2V9-TOTALITY-ROOT: contract root must be a non-empty JSON object"]
    try:
        return parsed_bytes + _check(c, authority, self_tree)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        primitive = _safe_jx_selftest()
        prefix = ["C2V9-PRIMITIVE: " + item for item in primitive["escapes"]]
        if not prefix and jx_bind(primitive["entryPointFailures"], 0) is not None:
            prefix = ["C2V9-PRIMITIVE: " + str(primitive["entryPointFailures"]) +
                      " entry point(s) of the primitive no longer differ from the "
                      "host-language operation they replace"]
        return parsed_bytes + prefix + [
            "C2V9-TOTALITY: the candidate could not be traversed (" +
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
            "C2V9-DERIVATION: the candidate must derive from " + V4_CONTRACT + " at " +
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
    findings.extend("C2V9-INHERITED: " + str(item) for item in inherited)

    # ---- the measurement, then L2 / L2b / L3 --------------------------------
    measurement = measure(effective, authority)
    authority.measurement = measurement
    findings.extend(census_comparison_findings(effective, measurement))
    findings.extend(register_findings(effective, measurement, authority))
    findings.extend(document_type_lock_findings(base, effective, authority))

    # ---- L8 parse integrity, and L9 the declared strings ---------------------
    # L8 runs BEFORE the scan and the behavioural layers for the same reason the
    # primitive's own test runs first: everything below reads a parsed object,
    # and if the parse does not say what the bytes say then everything below is
    # a statement about a different document.
    findings.extend(parse_integrity_findings(authority, tree))
    findings.extend(declared_string_findings(c, authority, tree))

    # ---- L4, L5, L6, L6b ----------------------------------------------------
    findings.extend(scan_findings(authority, tree))
    findings.extend(behavioural_findings(effective, measurement, authority, tree))
    findings.extend(sweep_findings(authority))
    authority.differential = predecessor_differential(authority)
    authority.portability = jx_portability_findings(own_source())
    for name in authority.portability["names"]:
        findings.append("C2V9-PRIMITIVE: the primitive block references " + name +
                        " from outside its declared portability boundary, so the claim "
                        "that another checker can adopt it unchanged is false")
    probe = jx_portability_findings(PORTABILITY_DETECTOR_PROBE.encode("utf-8"))
    if not jx_int_in_range(probe["freeNames"], 1, 10 ** 6):
        findings.append(
            "C2V9-PRIMITIVE: the portability detector reports a block that plainly "
            "references a name from outside itself as self-contained, so the measured "
            "claim that another checker can adopt this primitive unchanged is a "
            "statement about an instrument that detects nothing")

    # ---- L6c needs a register; the successor figures are the only part of it
    # that depends on L6c, so the partial register is built first and the two
    # are never allowed to define each other.
    authority.successor = _EMPTY_SUCCESSOR
    authority.candidate_lock = {"boundLeaves": 0, "executedCases": 0,
                                "namedRejections": 0, "controls": 0, "admissions": 0,
                                "spellingTypes": 0, "escapes": []}
    # L6d runs before the register is built, because the two BOOLEAN leaves that
    # are this document's own reproduction claims are bound to what L6, L8 and
    # L6d measured, and a claim bound to a layer that has not run yet would be
    # bound to nothing -- which is the state v7 shipped them in.
    authority.enumeration_differential = enumeration_differential(authority)
    # L6e runs beside L6d and for the same reason: the counters this document
    # publishes about its own repair are bound to what this layer measured.
    authority.skeleton_differential = skeleton_differential(authority)
    authority.partial_live = live_register(authority)
    authority.successor = successor_differential(authority, c)
    findings.extend(differential_findings(authority))
    findings.extend(enumeration_findings(authority))
    findings.extend(skeleton_findings(authority))

    # ---- L2c: the candidate's own leaves, ALL of them ------------------------
    # Pass one populates authority.candidate_lock and authority.candidate_ledger;
    # pass two reports against a register that already carries them.  Every count
    # here is a function of the bound leaf SET and of the document's SHAPE, never
    # of a published value, so the two passes agree -- and if they ever stop
    # agreeing, pass two's findings say so by name.
    candidate_lock_findings(c, live_register(authority), authority, base, measurement)
    live = live_register(authority)
    findings.extend(candidate_lock_findings(c, live, authority, base, measurement))
    authority.live = live_register(authority)
    live = authority.live
    runtime = {"candidateDocumentBytes": authority.candidate_bytes,
               "sweepElapsedSeconds": authority.sweep["elapsedSeconds"]}
    labelled = _banner_register(live, authority.document_name,
                                hashlib.sha256(own_source()).hexdigest(),
                                authority.candidate_digest)
    banner_problems = banner_findings(labelled, runtime)
    findings.extend(banner_problems)
    if not banner_problems:
        authority.banner = render_banner(BANNER_TEMPLATES, labelled, runtime)

    # ---- the candidate's own obligations ------------------------------------
    findings.extend(_repro_findings(c, authority))
    findings.extend(_parse_repro_findings(c, authority))
    findings.extend(_enumeration_repro_findings(c, authority))
    findings.extend(_skeleton_repro_findings(c, authority))
    findings.extend(_disclaimer_findings(c))
    findings.extend(_adoption_findings(c))
    findings.extend(_inventory_findings(c))
    findings.extend(_residual_findings(c, live))
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
    module = types.ModuleType("opensip_c2v9_mutated")
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
     "return JX_UNSUPPORTED", "C2V9-PRIMITIVE", ""),
    ("drop the type tag from the canonical encoding", "jx_canon",
     "return str(value)", "C2V9-PRIMITIVE", ""),
    ("drop the length framing that makes the encoding decodable", "jx_frame",
     "return tag + payload", "C2V9-PRIMITIVE", ""),
    ("compare canonical tokens with host equality instead of string equality",
     "jx_equal", "return a == b", "C2V9-PRIMITIVE", ""),
    ("invert equality with the host operator", "jx_ne", "return a != b",
     "C2V9-PRIMITIVE", "jx_ne"),
    ("let the canonical encoding stop being invertible", "jx_decanon",
     "return None", "C2V9-PRIMITIVE", "round trip"),
    ("admit every value into the JSON domain", "jx_in_domain", "return True",
     "C2V9-PRIMITIVE", "jx_in_domain"),
    ("hash a raw value instead of its canonical token", "jx_key",
     "return str(value)", "C2V9-PRIMITIVE", ""),
    ("let isinstance decide integerhood (True is an int)", "jx_int",
     "return isinstance(value, int)", "C2V9-PRIMITIVE", ""),
    ("strip the type gate from the integer CONSTANT guard", "jx_exact_int",
     "return value == constant", "C2V9-PRIMITIVE", "jx_exact_int"),
    ("strip the type gate from the integer RANGE guard", "jx_int_in_range",
     "return low <= value <= high", "C2V9-PRIMITIVE", "jx_int_in_range"),
    ("let two different JSON types count as the same type", "jx_same_type",
     "return True", "C2V9-PRIMITIVE", ""),
    ("restore the predecessor's ungated published-counter comparison", "jx_bind",
     "return None if published == measured else 'drift'", "C2V9-PRIMITIVE", "jx_bind"),
    ("gate only the wire side of the binding and trust the computed side", "jx_bind",
     "if not jx_int(published):\n    return 'type'\n"
     "return None if published == measured else 'drift'",
     "C2V9-BEHAVIOUR", "computed side"),
    ("compare published strings with host equality", "jx_bind_text",
     "return None", "C2V9-PRIMITIVE", "jx_bind_text"),
    ("use host membership instead of canonical membership", "jx_in",
     "return needle in list(haystack)", "C2V9-PRIMITIVE", ""),
    ("invert membership with the host operator", "jx_not_in",
     "return needle not in list(haystack)", "C2V9-PRIMITIVE", ""),
    ("restore the IR-C2V5-01 subset test verbatim", "jx_subset",
     "return set(left) <= set(right)", "C2V9-PRIMITIVE", ""),
    ("restore the host superset test", "jx_superset",
     "return set(left) >= set(right)", "C2V9-PRIMITIVE", ""),
    ("restore the host disjointness test", "jx_disjoint",
     "return set(left).isdisjoint(set(right))", "C2V9-PRIMITIVE", ""),
    ("restore host set difference", "jx_difference",
     "return list(set(left) - set(right))", "C2V9-PRIMITIVE", ""),
    ("let set() dedup collapse 1, 1.0 and True", "jx_unique",
     "return list(dict.fromkeys(values))", "C2V9-PRIMITIVE", ""),
    ("build a hashed key set out of raw values", "jx_keyset",
     "return set(values)", "C2V9-PRIMITIVE", ""),
    ("use host counting", "jx_count", "return list(values).count(needle)",
     "C2V9-PRIMITIVE", "jx_count"),
    ("use host index lookup", "jx_index",
     "return list(values).index(needle) if needle in list(values) else None",
     "C2V9-PRIMITIVE", "jx_index"),
    ("use host key membership", "jx_has", "return key in mapping",
     "C2V9-PRIMITIVE", "jx_has"),
    ("use host key lookup", "jx_get", "return mapping.get(key, default)",
     "C2V9-PRIMITIVE", "jx_get"),
    ("use host lookup for the total accessor", "jx_at",
     "try:\n    return container[key]\nexcept Exception:\n    return default",
     "C2V9-PRIMITIVE", "jx_at"),
    ("use host membership for the total accessor", "jx_has_at",
     "return key in container", "C2V9-PRIMITIVE", ""),
    ("use host assignment for the total mutator", "jx_put",
     "container[key] = value\nreturn True", "C2V9-PRIMITIVE", ""),
    ("order two different JSON types against each other", "jx_order",
     "return 0 if a == b else (-1 if a < b else 1)", "C2V9-PRIMITIVE", ""),
    ("restore the host ordering operators", "jx_le", "return a <= b",
     "C2V9-PRIMITIVE", "jx_le"),
    ("restore the host strict ordering operator", "jx_lt", "return a < b",
     "C2V9-PRIMITIVE", "jx_lt"),
    ("restore the host reverse ordering operator", "jx_ge", "return a >= b",
     "C2V9-PRIMITIVE", "jx_ge"),
    ("restore the host strict reverse ordering operator", "jx_gt", "return a > b",
     "C2V9-PRIMITIVE", "jx_gt"),
    ("sort by raw value instead of canonical token", "jx_sorted",
     "return sorted(values, key=repr)", "C2V9-PRIMITIVE", ""),
    ("sort records by raw field value", "jx_sorted_by",
     "return sorted(records, key=lambda record: repr(record))", "C2V9-PRIMITIVE", ""),
    ("order a heterogeneous JSON type set instead of refusing it",
     "jx_sorted_homogeneous", "return list(values), None", "C2V9-PRIMITIVE", ""),
    ("let a float element into an integer summation", "jx_sum_int",
     "return sum(values), None", "C2V9-PRIMITIVE", ""),
    ("let a non-string into a string set", "jx_string_set",
     "return set(values), None", "C2V9-PRIMITIVE", ""),
    ("admit a non-finite float as a finite number", "jx_finite_number",
     "return jx_type(value) == 'number'", "C2V9-PRIMITIVE", ""),
    # v7's four gates.  Every one of them exists because a v6 document said it
    # did (jx_min, jx_max) or because IR-C2V6-01 showed the parse itself is a
    # gate (jx_loads, jx_number_tokens).  They are preserved unchanged.
    ("take the extreme by canonical TOKEN, which is not value order", "jx_min",
     "return jx_sorted(values)[0], None", "C2V9-PRIMITIVE", "jx_min"),
    ("take the extreme by canonical TOKEN, which is not value order", "jx_max",
     "return jx_sorted(values)[-1], None", "C2V9-PRIMITIVE", "jx_max"),
    ("parse the way the predecessor did, keeping the LAST duplicate key silently",
     "jx_loads", "return json.loads(text), []", "C2V9-PRIMITIVE", "jx_loads"),
    ("stop reading number tokens out of the bytes", "jx_number_tokens",
     "return []", "C2V9-PRIMITIVE", "jx_number_tokens"),
    # v8's four new gates.  IR-C2V7-01: the totality's type coverage is now a
    # property of these functions rather than of a list, so breaking them is
    # how the totality is falsified.
    ("restore v7's type-named enumeration: report only integer and number "
     "leaves, which is the exact shape that let a boolean leaf through",
     "jx_leaf_census",
     "return [row for row in jx_walk(value) if jx_in(row[1], ['integer', 'number'])]",
     "C2V9-PRIMITIVE", "jx_leaf_census"),
    ("stop the node walk seeing containers", "jx_walk",
     "return jx_leaf_census(value)", "C2V9-PRIMITIVE", "jx_walk"),
    ("let the total binding compare across JSON types", "jx_bind_value",
     "return None if published == measured else 'drift'",
     "C2V9-PRIMITIVE", "jx_bind_value"),
    # DECLARED instead of MEASURED, and declared as v7's coverage: the table
    # below still says five scalar types and this says two, and the whole point
    # of the layer is that the table may not be a claim about the walker.
    ("declare the type space instead of measuring it", "jx_type_space",
     "return {'witnesses': 0, 'declaredTypes': len(JX_TYPES), 'types': 2, "
     "'containers': 0, 'scalars': 2, 'unwitnessed': 0, "
     "'rfcProductions': len(JX_RFC8259_PRODUCTIONS), 'containerTypes': [], "
     "'scalarTypes': ['integer', 'number'], 'escapes': []}",
     "C2V9-LEAFRULE", "the walker's own measured behaviour"),
)

# Every row that expects the primitive's own layer asserts on the NAME OF THE
# GATE IT BREAKS, not merely on the finding id.  v5's suite was measured to
# assert on a bare id for 25 of its 38 rows and on nothing at all for 3, and a
# rejection that does not name the position under test is the trap the
# adjudication records.  The transformation is explicit so a reviewer can see
# that no row is exempt.
GATE_MUTATIONS = tuple(
    (name, function, body, expected,
     function if expected == "C2V9-PRIMITIVE" and not subject else subject)
    for name, function, body, expected, subject in _GATE_MUTATIONS)


# (name, function, replacement body, expected finding id, subject substring,
#  clears the pinned-sweep cache)
LAYER_MUTATIONS = (
    ("narrow the numeric model back to ast.Constant (IR-C2V4-01's root cause)",
     "_provably_non_numeric", "return not isinstance(node, ast.Constant)",
     "C2V9-SCAN-BLIND", "2487", False),
    ("launder comprehension results the way v5 did (IR-C2V5-01's root cause)",
     "_is_wire",
     "if node is None:\n    return False\n"
     "if isinstance(node, ast.Subscript):\n"
     "    return not (isinstance(node.value, ast.Name) and node.value.id in literals)\n"
     "if isinstance(node, ast.Attribute):\n"
     "    return _is_wire(node.value, tainted, literals)\n"
     "return isinstance(node, ast.Name) and node.id in tainted",
     "C2V9-SCAN-BLIND", str(V5_DEFECT_LINE), False),
    ("stop the scan seeing the whole function universe", "_function_universe",
     "return [node for node in tree.body if isinstance(node, ast.FunctionDef)]",
     "C2V9-SCAN-BLIND", "function-like node", False),
    ("excuse every comparison by textual gate dominance", "_gate_dominates",
     "return True", "C2V9-SCAN-BLIND", "adjudicated census comparison", False),
    ("erase the adjudicated line numbers the scan must be shown to see",
     "adjudicated_census_lines", "return []", "C2V9-SCAN-BLIND", "vacuous", False),
    ("stop deriving the register from the live measurement", "measured_positions",
     "return {}", "C2V9-REGISTER", "not reached by the measurement", False),
    ("disable the behavioural layer", "behavioural_layer",
     "return {'positions': 0, 'spellings': 0, 'executedCases': 0, "
     "'namedTypeRejections': 0, 'admissions': 0, "
     "'rejectedWithoutNamingThePosition': 0, 'instrumentProbes': 0, "
     "'instrumentProbesNamed': 0, 'instrumentProbesEscaped': 0, 'escapes': []}",
     "C2V9-BEHAVIOUR", "executed no case", False),
    ("confine the document lock to the census block", "locked_integer_leaves",
     "return []", "C2V9-DOCLOCK", "outside the lock", False),
    ("lock only the base direction, so a derived leaf escapes",
     "locked_integer_leaves",
     "return jx_sorted(jx_unique(census_leaves_of_type(base, 'integer')))",
     "C2V9-DOCLOCK", "outside the lock", False),
    ("probe only the first leaf of the document lock", "document_type_probe",
     "return {'lockedLeaves': len(locked), 'executedCases': 0, "
     "'namedTypeRejections': 0, 'admissions': 0, 'escapes': []}",
     "C2V9-DOCLOCK", "probed no position", False),
    ("stop binding the candidate's own integer leaves", "candidate_bindings",
     "return [], []", "C2V9-UNBOUND", "no layer of this run binds", False),
    ("stop probing the candidate's own integer leaves", "candidate_type_probe",
     "return {'boundLeaves': len(bindings), 'executedCases': 0, "
     "'namedRejections': 0, 'controls': 0, 'admissions': 0, 'escapes': []}",
     "C2V9-CANDLOCK", "probed no position", False),
    ("let the candidate binding table be narrowed silently", "_effective_expected",
     "return None, 'unmeasured'", "C2V9-UNBOUND", "the derivation writes a JSON integer",
     False),
    ("hollow out the whole-document sweep", "predecessor_sweep",
     "return {'integerLeavesInjected': 0, 'admittedToAFullGreenRun': 0, "
     "'rejectedByPredecessor': 0, 'admittedCensusCounters': 0, "
     "'admittedOutsideTheCensusBlock': 0, 'admittedPaths': [], 'outsidePaths': [], "
     "'elapsedSeconds': 0}", "C2V9-SWEEP", "integer leaves injected", True),
    ("sweep only the census block, as a scoped repair would",
     "predecessor_sweep",
     "authority.pinned.clear()\n"
     "result = {'integerLeavesInjected': 0, 'admittedToAFullGreenRun': 0, "
     "'rejectedByPredecessor': 0, 'admittedCensusCounters': 0, "
     "'admittedOutsideTheCensusBlock': 0, 'admittedPaths': [], 'outsidePaths': []," 
     "'elapsedSeconds': 0}\nreturn result", "C2V9-SWEEP", "integer leaves", True),
    ("stop selecting the predecessor's integer leaves out of the total census",
     "census_leaves_of_type",
     "return []", "C2V9-SWEEP", "OUTSIDE the census block", True),
    ("bake the banner figures back into source text", "banner_digit_tokens",
     "return []", "C2V9-BANNER", "detects nothing", False),
    ("stop the banner interpolating the register at all",
     "render_banner", "return list(templates)", "C2V9-BANNER", "uninterpolated", False),
    ("stop probing the honesty of L4's `-> str` proofs", "str_proof_probe",
     "return {'declared': 0, 'probed': 0, 'executedCases': 0, 'failures': 0, "
     "'escapes': []}", "C2V9-PROOF", "were not exercised", False),
    ("stop probing the honesty of L4's AST-STR-FIELD proof", "ast_field_probe",
     "return {'executedCases': 0, 'failures': 0, 'escapes': []}",
     "C2V9-PROOF", "were not exercised", False),
    ("declare the primitive self-contained without measuring it",
     "jx_portability_findings", "return {'freeNames': 0, 'names': []}",
     "C2V9-PRIMITIVE", "detects nothing", False),
    ("stop executing the primitive's own exhaustive test", "jx_selftest",
     "return {'corpusValues': 0, 'corpusPairs': 0, 'roundTrips': 0, "
     "'distinctTokens': 0, 'tokenCollisions': 0, 'stricterThanHostEquality': 0, "
     "'looserThanHostEquality': 0, 'agreeWithHostEquality': 0, "
     "'reflexiveFailures': 0, 'crossTypeAdmissions': 0, 'gateCases': 0, "
     "'gateAdmissions': 0, 'operatorSpaceRows': 0, "
     "'operatorSpaceHazardsReproduced': 0, 'operatorSpaceRowsCovered': 0, "
     "'domainRefusals': 0, 'entryPointCases': 0, 'entryPointFailures': 0, "
     "'escapes': []}", "C2V9-PRIMITIVE", "empty set", False),
    ("collapse the differential against the pinned v5 REJECT", "_v5_admissions",
     "return []", "C2V9-SUCCESSOR", "collapsed", True),
    ("stop measuring the census comparison sites", "census_site_positions",
     "return {}", "C2V9-REGISTER", "partition", False),
    # v7's parse layers, preserved.  Every one of them is broken here and every
    # break must be caught by the layer it breaks, after every counter has been
    # republished.
    ("stop reporting the byte/parse divergences at all", "parse_problem_findings",
     "return []", "C2V9-PARSE-PROBE", "duplicate at the root", False),
    ("stop looking for unhooked JSON parses in this file's own tree",
     "json_load_sites", "return []", "C2V9-PARSE-SCAN", "detects nothing", False),
    ("hollow out the parse probe", "parse_probe",
     "return {'executedCases': 0, 'namedAtThePosition': 0, 'controls': 0, "
     "'admissions': 0, 'escapes': []}", "C2V9-PARSE-PROBE", "probed no case", False),
    ("collapse the differential against the REJECTED v6's own parse",
     "parse_differential",
     "return {'vectors': len(PARSE_DIFFERENTIAL_VECTORS), 'rows': [], "
     "'predecessorParseBlind': 0, 'successorNamedByPosition': 0, 'escapes': []}",
     "C2V9-PARSE-DIFFERENTIAL", "unable to distinguish", False),
    # v8's totality.  IR-C2V7-01.  Narrowing a totality produces SILENCE, so the
    # rows that break it are the injection probe's, not the walker's: restoring
    # v7's exact type coverage must make the boolean, null and string injections
    # ADMITTED and must be reported as such.
    ("restore v7's type-named candidate totality verbatim (IR-C2V7-01's own shape)",
     "candidate_leaf_ledger",
     "rules = {}\n"
     "for kind, rule in LEAF_TYPE_RULES:\n"
     "    jx_put(rules, kind, rule)\n"
     "counts = {}\n"
     "for kind in JX_TYPES:\n"
     "    jx_put(counts, kind, 0)\n"
     "census = [row for row in jx_leaf_census(c)\n"
     "          if jx_in(row[1], ['integer', 'number'])]\n"
     "unbound = jx_difference([row[0] for row in census], bound_paths)\n"
     "findings = []\n"
     "for steps in unbound:\n"
     "    findings.append('C2V9-UNBOUND: the candidate publishes a JSON leaf at ' +\n"
     "                    _steps_text(steps) + ' that no layer of this run binds')\n"
     "for steps, kind in census:\n"
     "    jx_put(counts, kind, jx_get(counts, kind, 0) + 1)\n"
     "nodes = jx_walk(c)\n"
     "return {'leaves': len(census), 'counts': counts, 'bound': 0,\n"
     "        'nodes': len(nodes), 'containers': len(nodes) - len(census),\n"
     "        'narrative': 0, 'unruled': 0, 'unbound': len(findings),\n"
     "        'findings': findings}",
     "C2V9-TOTALITY", "ADMITTED", False),
    ("hollow out the whole-type-space injection probe", "candidate_totality_probe",
     "return {'executedCases': 0, 'namedRejections': 0, 'admissions': 0, "
     "'namedBySkeletonOnly': 0, 'localisedToASubtree': 0, "
     "'typesCovered': len(JX_TYPES), 'escapes': []}",
     "C2V9-TOTALITY", "probed no position", False),
    ("narrow the injection probe back to the two types v7 covered",
     "candidate_totality_probe",
     "return {'executedCases': 1, 'namedRejections': 1, 'admissions': 0, "
     "'namedBySkeletonOnly': 0, 'localisedToASubtree': 0, 'typesCovered': 2, "
     "'escapes': []}",
     "C2V9-TOTALITY", "narrower than the data model", False),
    ("stop hashing the document's own shape", "document_skeleton",
     "return []", "C2V9-SKELETON", "does not cover every node", False),
    # IR-C2V8-01 ITSELF, reintroduced into the source: v8's `document_skeleton`
    # verbatim.  It still covers every node and still binds every JSON type; what
    # it stops doing is telling two nodes apart.  The row that catches it reads no
    # published counter, so republishing the digest cannot silence it.
    ("restore v8's joined-text path identity verbatim (IR-C2V8-01's own shape)",
     "document_skeleton",
     "return [[_steps_text(steps), kind] for steps, kind in jx_walk(c)]",
     "C2V9-SKELETON", "not injective", False),
    ("stop executing the path-identity proof", "skeleton_path_identity_probe",
     "return {'pairs': 0, 'collidesUnderTheJoinedText': 0, "
     "'separatesUnderTheCanonicalToken': 0, 'stepPairs': 0, "
     "'stepPairsCollidingUnderTheJoinedText': 0, "
     "'stepPairsSeparatedByTheCanonicalToken': 0, 'nodes': 0, 'pathsInverted': 0, "
     "'distinctPathTokens': 0, 'distinctJoinedTexts': 0, 'escapes': []}",
     "C2V9-SKELETON", "EXISTENCE OF THE INVERSE", False),
    ("stop localising the shape to root subtrees", "document_subtree_skeletons",
     "return {}", "C2V9-SKELETON", "localiser narrower than the document", False),
    ("stop measuring the leaf census against the node walk (OBS-C2V8-01's own "
     "depth-narrowed census)", "census_walk_agreement",
     "walk = jx_walk(c)\n"
     "census = [row for row in jx_leaf_census(c) if len(row[0]) <= 2]\n"
     "leaves = [[list(s), k] for s, k in walk if jx_not_in(k, ['array', 'object'])]\n"
     "return {'walkNodes': len(walk), 'walkLeaves': len(leaves), "
     "'censusLeaves': len(census), 'agreed': len(census), 'escapes': []}",
     "C2V9-CENSUS", "may not be a claim about a walker", False),
    ("stop measuring the RFC productions by parsing the grammar",
     "jx_rfc_production_space",
     "return {'texts': 0, 'productions': 0, 'measured': {}, 'escapes': []}",
     "C2V9-LEAFRULE", "NO JSON text in the grammar corpus realises", False),
    ("collapse the skeleton differential against the pinned v8",
     "skeleton_differential",
     "return dict(_EMPTY_SKELETON_DIFFERENTIAL, "
     "vectors=len(SKELETON_DIFFERENTIAL_VECTORS))",
     "C2V9-SKELDIFF", "unable to see the reparenting", False),
    ("stop requiring a residual to state a measured boundary (OBS-C2V8-02's own "
     "gap)", "_residual_boundary_problems", "return []", "C2V9-RESIDUAL",
     "detects nothing", False),
    ("declare the leaf disposition table without measuring the type space",
     "leaf_rule_findings", "return []", "C2V9-LEAFRULE", "detects nothing", False),
    ("collapse the enumeration differential against the pinned v7",
     "enumeration_differential",
     "return dict(_EMPTY_ENUMERATION, vectors=len(ENUMERATION_DIFFERENTIAL_VECTORS))",
     "C2V9-ENUMERATION", "unable to reach the leaf", False),
    ("stop measuring the depth at which the duplicate-key claim holds",
     "parse_depth_probe",
     "return {'depth': 0, 'named': 0, 'controls': 0, 'escapes': []}",
     "C2V9-PARSE-DEPTH", "any depth", False),
    ("stop counting the syntactic evasions of the parse scan",
     "json_parse_evasion_sites", "return []", "C2V9-PARSE-SCAN",
     "decoder-evasion detector", False),
    ("stop reading the number tokens of the pinned inputs",
     "pinned_number_token_census", "return {'files': 0, 'tokens': 0}",
     "C2V9-PARSE-SCAN", "finds no token at all", False),
    ("stop checking that a declared assertion string exists at all",
     "declared_string_layer",
     "return {'rows': 0, 'findingIds': 0, 'inSource': 0, 'inDocument': 0, "
     "'atEmitSite': 0, 'unresolved': 0, 'namesChecked': 0, 'namesUndefined': 0, "
     "'escapes': []}", "C2V9-DECLARED-STRING", "empty set", False),
    ("let the emit-site half of the declared-string layer go inert",
     "emit_site_pool", "return {}", "C2V9-DECLARED-STRING", "inert", False),
    ("stop reading the candidate's string values into the declared-string corpus",
     "document_string_pool", "return []", "C2V9-DECLARED-STRING",
     "exists nowhere", False),
    ("stop measuring bare truthiness", "bare_truthiness_sites", "return []",
     "C2V9-SCAN-BLIND", "bare-truthiness", False),
)

SOURCE_MUTATIONS = tuple(
    (name, function, body, expected, subject, False)
    for name, function, body, expected, subject in GATE_MUTATIONS) + LAYER_MUTATIONS


def _m_unregister_a_census_position(c):
    for op in c["derivedFrom"]["operations"]:
        if jx_equal(op.get("path"), "planIntent.integerConstantRegisterV8"):
            op["value"]["censusCounterPositions"].pop()
            return
    raise AuthorityLoadError("cannot find the register operation to mutate")


def _m_overstate_the_register(c):
    for op in c["derivedFrom"]["operations"]:
        if jx_equal(op.get("path"), "planIntent.integerConstantRegisterV8"):
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
    c["v4InheritanceProjection"]["fields"]["planIntent.integerConstantRegisterV8"] = None


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
                      if not jx_equal(item.get("id"), "RES-C2V9-03")]


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


def _m_understate_a_v8_counter(c):
    c["v9MeasuredCounters"]["behaviouralExecutedCases"] = 1


def _m_float_a_v8_counter(c):
    counters = c["v9MeasuredCounters"]
    counters["registeredCensusPositions"] = float(counters["registeredCensusPositions"])


def _m_publish_an_unmeasured_counter(c):
    c["v9MeasuredCounters"]["counterNobodyMeasures"] = 7


def _m_soften_the_repro(c):
    c["theDefect"]["minimalReproduction"]["sourceModification"] = "a small patch"


def _m_drop_a_successor_vector(c):
    c["theSuccessorDefect"]["vectors"] = c["theSuccessorDefect"]["vectors"][:1]


def _m_float_a_site_read_count(c):
    site = c["theDefect"]["repairedComparisonSites"][0]
    site["wireIntegerPositionsRead"] = float(site["wireIntegerPositionsRead"])


def _m_overstate_the_residual_count(c):
    """v6 was described as carrying ten residuals and carried seven."""
    c["residualAccounting"]["residuals"] = c["residualAccounting"]["residuals"] + 3


def _m_inject_a_float_leaf(c):
    """OBS-C2V6-01, verbatim: the same key that v6 refused as 17 and admitted
    as 17.0 to a full green run."""
    c["reviewerInjectedLeaf"] = 17.0


def _m_soften_the_parse_repro(c):
    c["theParseDefect"]["minimalReproduction"]["sourceModification"] = "a small patch"


def _m_overclaim_the_parse_repro(c):
    c["theParseDefect"]["minimalReproduction"]["reproducedPerRun"] = "EXHAUSTIVE"


def _m_drop_a_parse_vector(c):
    c["theParseDefect"]["vectors"] = c["theParseDefect"]["vectors"][:1]


def _m_soften_the_parse_disposition(c):
    c["theParseDefect"]["disposition"] = "ADVISORY"


def _m_name_a_primitive_that_does_not_exist(c):
    """OBS-C2V6-02, verbatim: an adoption step naming jx_min and jx_max when
    neither existed.  An adopter following it got a NameError."""
    steps = c["thePrimitive"]["whatAnAdoptingCheckerMustDo"]
    steps.append("Replace every wire-touching lookup with jx_lookup_that_does_not_exist.")


def _m_flip_the_parse_reproduction_claim(c):
    """IR-C2V7-01 VERBATIM: one token, one byte, at the leaf that is this
    document's own claim to have reproduced the finding it discharges.  Against
    v7 this reached exit 0 and a full green banner still reading `with no
    unbound bucket`."""
    c["theParseDefect"]["minimalReproduction"]["reproducedByThisLane"] = False


def _m_flip_the_defect_reproduction_claim(c):
    c["theDefect"]["minimalReproduction"]["reproducedByThisLane"] = False


def _m_flip_the_enumeration_reproduction_claim(c):
    c["theEnumerationDefect"]["minimalReproduction"]["reproducedByThisLane"] = False


def _m_integer_the_reproduction_claim(c):
    """The boolean claim spelled as the integer the host language calls equal."""
    c["theParseDefect"]["minimalReproduction"]["reproducedByThisLane"] = 1


def _m_inject_a_boolean_leaf(c):
    """IR-C2V7-01's added-leaf half, at the root."""
    c["reviewerInjectedBool"] = True


def _m_inject_a_boolean_leaf_at_depth(c):
    c["theDefect"]["reviewerInjectedBoolAtDepth"] = False


def _m_inject_a_null_leaf(c):
    """OBS-C2V7-09's null spelling, which reached a full green run against v7."""
    c["reviewerInjectedNull"] = None


def _m_inject_a_string_leaf(c):
    """OBS-C2V7-09's string spelling.  A string leaf is NARRATIVE by rule, so
    the ledger does not name it; the SHAPE does, which is what the skeleton is
    for and why the two obligations are separate."""
    c["reviewerInjectedString"] = "x"


def _m_inject_an_empty_object(c):
    """An empty container holds no leaf at all and is invisible to any leaf
    census, however total that census is over the type space."""
    c["reviewerInjectedEmptyObject"] = {}


def _m_rename_a_key(c):
    """IR-C2V8-01 VERBATIM, and this is the row v8's suite could not cover.

    v8's version of this row renamed the ROOT key `recordingObligation`, where NO
    `/` collision is constructible, so it passed and gave affirmative assurance
    about a class it did not reach.  This row performs the reviewer\'s own
    +11-byte edit as a structural move: a narrative leaf is relocated out of
    `thePrimitive` and onto a ROOT key named with the literal text of its old
    path, positioned immediately after its old top-level ancestor so the walk
    ORDER is preserved too.  Against v8 this is exit 0, zero findings and a full
    green banner with 945/148/797 byte-identical.
    """
    moved = _skeleton_reparent(c, ["thePrimitive", "theEnumerationIsAGateToo"])
    if moved is None:
        raise KeyError("thePrimitive/theEnumerationIsAGateToo")
    c.clear()
    c.update(moved)


def _m_rename_a_root_key(c):
    """v8's row, RETAINED unchanged.  A root key has no `/` collision available,
    and the class it does cover is still a class."""
    c["recordingObligationRenamed"] = c.pop("recordingObligation")


def _m_reparent_a_narrative_subtree(c):
    """The CONTAINER half of IR-C2V8-01: seven whole subtrees of the v8 document
    could be relocated with a byte-identical skeleton, including a 141-node
    array.  An empty container holds no leaf for any census; a reparented one
    holds all of its leaves at paths whose joined text has not changed."""
    moved = _skeleton_reparent(c, ["theSkeletonDefect", "measuredThisRun"])
    if moved is None:
        raise KeyError("theSkeletonDefect/measuredThisRun")
    c.clear()
    c.update(moved)


def _m_drop_a_root_subtree_digest(c):
    """Remove one root subtree from the localiser table.  The shape of that
    subtree is then bound only by the whole-document digest, which names no
    position -- OBS-C2V8-04\'s collateral rejection, reintroduced."""
    del c["documentSkeleton"]["subtrees"]["theDefect"]


def _m_name_a_root_subtree_that_does_not_exist(c):
    c["documentSkeleton"]["subtrees"]["aSubtreeThisDocumentDoesNotHave"] = "0" * 64


def _m_downgrade_the_open_residual(c):
    """OBS-C2V8-03 verbatim: one edit, RETAINED-OPEN to RETAINED, exit 0 in v8."""
    for item in c["residuals"]:
        if item.get("id") == "RES-C2V9-15":
            item["status"] = "RETAINED"


def _m_open_a_residual_that_is_not_declared_open(c):
    for item in c["residuals"]:
        if item.get("id") == "RES-C2V9-01":
            item["status"] = "RETAINED-OPEN"


def _m_strip_a_measured_boundary(c):
    """OBS-C2V8-02 verbatim: v8 published a residual with no MEASURED BOUNDARY
    clause and no counter at all, under a claim that every residual had one."""
    for item in c["residuals"]:
        if item.get("id") == "RES-C2V9-11":
            item["measuredBoundary"] = "the exposure is small and well understood"


def _m_uncite_the_counters_of_a_boundary(c):
    """The clause survives and the numbers become adjectives."""
    for item in c["residuals"]:
        if item.get("id") == "RES-C2V9-07":
            item["measuredBoundary"] = (
                "MEASURED BOUNDARY: about two thirds of the leaves of this document "
                "are narrative and a small number of edits are needed to add one")


def _m_soften_the_skeleton_repro(c):
    c["theSkeletonDefect"]["minimalReproduction"]["sourceModification"] = "a patch"


def _m_overclaim_the_skeleton_repro(c):
    c["theSkeletonDefect"]["minimalReproduction"]["reproducedPerRun"] = "EXHAUSTIVE"


def _m_drop_a_skeleton_vector(c):
    c["theSkeletonDefect"]["vectors"] = c["theSkeletonDefect"]["vectors"][1:]


def _m_flip_the_skeleton_reproduction_claim(c):
    c["theSkeletonDefect"]["minimalReproduction"]["reproducedByThisLane"] = False


def _m_drift_the_skeleton_mutant_digest(c):
    c["theSkeletonDefect"]["minimalReproduction"]["mutantSha256"] = "0" * 64


def _m_corrupt_the_skeleton_digest(c):
    c["documentSkeleton"]["sha256"] = "0" * 64


def _m_drift_a_skeleton_count(c):
    c["documentSkeleton"]["booleanLeaves"] = c["documentSkeleton"]["booleanLeaves"] + 1


def _m_soften_the_enumeration_repro(c):
    c["theEnumerationDefect"]["minimalReproduction"]["sourceModification"] = "a patch"


def _m_overclaim_the_enumeration_repro(c):
    c["theEnumerationDefect"]["minimalReproduction"]["reproducedPerRun"] = "EXHAUSTIVE"


def _m_drop_an_enumeration_vector(c):
    c["theEnumerationDefect"]["vectors"] = c["theEnumerationDefect"]["vectors"][:1]


def _m_disclaim_the_predecessor(c):
    """OBS-C2V7-05 VERBATIM: the one block whose job is to be accurate about
    what this artifact is not, pointed at somebody else's checker."""
    c["knownLimitations"]["thisIsNotAVerdict"] = (
        "A green run of check-c2-v7.py is authored by the same lane that authored "
        "the repair. It is checker-scope evidence. Independent re-review is REQUIRED.")


def _m_drop_a_layer(c):
    c["guardInventory"]["layers"] = [item for item in c["guardInventory"]["layers"]
                                     if item.get("id") != "L8"]


CONTRACT_MUTATIONS = (
    ("unregister one census counter position", _m_unregister_a_census_position,
     "C2V9-REGISTER", "not registered"),
    ("register a position the measurement does not reach", _m_overstate_the_register,
     "C2V9-REGISTER", "imaginary"),
    ("spell a census counter as a JSON float (the v4 minimal repro)",
     _m_float_census_counter, "C2V9-TYPE", "contractRoot.scalarLeafPaths"),
    ("spell a census counter as a JSON boolean", _m_boolean_census_counter,
     "C2V9-TYPE", "contractRoot.pathsNotRoundTripping"),
    ("spell a census counter as a JSON string", _m_string_census_counter,
     "C2V9-TYPE", "contractRoot.enumeratedPaths"),
    ("drift a census counter by one", _m_drift_census_counter,
     "C2V9-CENSUS", "contractRoot.executedCases"),
    ("widen the inherited-oracle projection beyond the identity fields",
     _m_widen_the_projection, "C2V9-PROJECTION", "integerConstantRegisterV8"),
    ("misdescribe the bytes the derivation is applied to", _m_misdescribe_the_derivation,
     "C2V9-DERIVATION", "verified predecessor holds"),
    ("claim total guard coverage", _m_claim_total_coverage, "C2V9-INVENTORY",
     "blind spot"),
    ("absorb a retained residual", _m_absorb_a_residual, "C2V9-RESIDUAL",
     "RES-C2V9-03"),
    ("drop the record of an executed input", _m_drop_an_input_record, "C2V9-RECORD",
     V4_CHECKER),
    ("spell an adjudicated comparison line as a float (IR-C2V5-01 verbatim)",
     _m_float_the_repro_line, "C2V9-TYPE",
     "theDefect/repairedComparisonSites/0/line"),
    ("drift an adjudicated comparison line by one", _m_drift_the_repro_line,
     "C2V9-CANDIDATE", "theDefect/repairedComparisonSites/0/line"),
    ("spell a per-site read count as a float", _m_float_a_site_read_count,
     "C2V9-TYPE", "wireIntegerPositionsRead"),
    ("spell a whole-document sweep figure as a float", _m_float_a_sweep_figure,
     "C2V9-TYPE", "admittedByPredecessorToAFullGreenRun"),
    ("republish the headline sweep figure as one (the reviewer's own probe)",
     _m_republish_a_sweep_figure, "C2V9-CANDIDATE", "integerLeavesInjected"),
    ("spell the measured false-accept counter as a JSON boolean (the FA-2 spelling)",
     _m_boolean_the_false_accept_counter, "C2V9-TYPE",
     "retainedFalseAcceptVectors/measuredThisRun/predecessorFullyGreenRuns"),
    ("drift the measured false-accept counter to zero",
     _m_drift_the_false_accept_counter, "C2V9-CANDIDATE",
     "retainedFalseAcceptVectors/measuredThisRun/successorRejectedByName"),
    ("understate one of this checker's own published counters",
     _m_understate_a_v8_counter, "C2V9-CANDIDATE", "behaviouralExecutedCases"),
    ("spell one of this checker's own published counters as a float",
     _m_float_a_v8_counter, "C2V9-TYPE", "registeredCensusPositions"),
    ("publish a counter this run does not measure", _m_publish_an_unmeasured_counter,
     "C2V9-UNBOUND", "counterNobodyMeasures"),
    ("soften the recorded minimal reproduction", _m_soften_the_repro, "C2V9-REPRO",
     "no source modification"),
    ("stop retaining one of the v5 blocking vectors", _m_drop_a_successor_vector,
     "C2V9-REPRO", "IR-C2V5"),
    # v8's own obligations.
    ("overstate this document's own residual count (v6 was described as ten and "
     "carried seven)", _m_overstate_the_residual_count, "C2V9-CANDIDATE",
     "residualAccounting/residuals"),
    ("add a JSON NUMBER leaf nobody binds (OBS-C2V6-01 verbatim)",
     _m_inject_a_float_leaf, "C2V9-UNBOUND", "reviewerInjectedLeaf"),
    ("soften the IR-C2V6-01 minimal reproduction", _m_soften_the_parse_repro,
     "C2V9-PARSE-REPRO", "no source modification"),
    ("overclaim how much of the IR-C2V6-01 reproduction an ordinary run recomputes",
     _m_overclaim_the_parse_repro, "C2V9-PARSE-REPRO", "WHICH HALF"),
    ("stop retaining one of the parse vectors", _m_drop_a_parse_vector,
     "C2V9-PARSE-REPRO", "IR-C2V6-01"),
    ("soften the disposition of the finding this successor exists to discharge",
     _m_soften_the_parse_disposition, "C2V9-PARSE-REPRO", "BLOCKING"),
    ("name a primitive entry point that does not exist (OBS-C2V6-02 verbatim)",
     _m_name_a_primitive_that_does_not_exist, "C2V9-DECLARED-STRING",
     "jx_lookup_that_does_not_exist"),
    ("drop the parse-integrity layer from the guard inventory", _m_drop_a_layer,
     "C2V9-INVENTORY", "L8"),
    # v8's own obligations.  IR-C2V7-01 and the ten findings recorded with it.
    ("flip this document's own claim to have reproduced IR-C2V6-01 (IR-C2V7-01 "
     "verbatim: one token, one byte, full green against v7)",
     _m_flip_the_parse_reproduction_claim, "C2V9-CANDIDATE",
     "theParseDefect/minimalReproduction/reproducedByThisLane"),
    ("flip this document's own claim to have reproduced IR-C2V4-01",
     _m_flip_the_defect_reproduction_claim, "C2V9-CANDIDATE",
     "theDefect/minimalReproduction/reproducedByThisLane"),
    ("flip this document's own claim to have reproduced IR-C2V7-01",
     _m_flip_the_enumeration_reproduction_claim, "C2V9-CANDIDATE",
     "theEnumerationDefect/minimalReproduction/reproducedByThisLane"),
    ("spell a boolean reproduction claim as the integer the host language calls "
     "equal to it", _m_integer_the_reproduction_claim, "C2V9-TYPE",
     "theParseDefect/minimalReproduction/reproducedByThisLane"),
    ("add a JSON BOOLEAN leaf nobody binds, at the root (IR-C2V7-01 verbatim)",
     _m_inject_a_boolean_leaf, "C2V9-UNBOUND", "reviewerInjectedBool"),
    ("add the same boolean leaf at depth", _m_inject_a_boolean_leaf_at_depth,
     "C2V9-UNBOUND", "reviewerInjectedBoolAtDepth"),
    ("add a JSON NULL leaf nobody binds (OBS-C2V7-09's null spelling)",
     _m_inject_a_null_leaf, "C2V9-UNBOUND", "reviewerInjectedNull"),
    ("add a JSON STRING leaf nobody binds (OBS-C2V7-09's string spelling)",
     _m_inject_a_string_leaf, "C2V9-SKELETON", "documentSkeleton/sha256"),
    ("add an EMPTY object, which holds no leaf for any census to reach",
     _m_inject_an_empty_object, "C2V9-SKELETON", "documentSkeleton/sha256"),
    ("reparent a narrative LEAF across a `/` boundary onto a root key named with "
     "the text of its old path - IR-C2V8-01's own +11-byte edit, which reached "
     "exit 0 and a full green banner against the pinned v8",
     _m_rename_a_key, "C2V9-SKELETON", "documentSkeleton/sha256"),
    ("reparent a whole narrative SUBTREE the same way - the container half of "
     "IR-C2V8-01", _m_reparent_a_narrative_subtree, "C2V9-SKELETON",
     "documentSkeleton/sha256"),
    ("rename a ROOT key, where no `/` collision is constructible - v8's own row, "
     "retained because the class it does cover is still a class",
     _m_rename_a_root_key, "C2V9-SKELETON", "documentSkeleton/sha256"),
    ("stop localising one root subtree, so its shape is bound only by a digest "
     "over the whole document", _m_drop_a_root_subtree_digest, "C2V9-UNBOUND",
     "documentSkeleton/subtrees/theDefect"),
    ("localise a root subtree this document does not have",
     _m_name_a_root_subtree_that_does_not_exist, "C2V9-SKELETON",
     "aSubtreeThisDocumentDoesNotHave"),
    ("downgrade the one residual this checker declares OPEN (OBS-C2V8-03 verbatim)",
     _m_downgrade_the_open_residual, "C2V9-RESIDUAL", "RES-C2V9-15"),
    ("open a residual this checker does not declare open",
     _m_open_a_residual_that_is_not_declared_open, "C2V9-RESIDUAL", "RES-C2V9-01"),
    ("strip a residual's MEASURED BOUNDARY clause (OBS-C2V8-02 verbatim)",
     _m_strip_a_measured_boundary, "C2V9-RESIDUAL", "RES-C2V9-11"),
    ("keep the clause and state its numbers as adjectives",
     _m_uncite_the_counters_of_a_boundary, "C2V9-RESIDUAL", "RES-C2V9-07"),
    ("soften the IR-C2V8-01 minimal reproduction", _m_soften_the_skeleton_repro,
     "C2V9-SKEL-REPRO", "no source modification"),
    ("overclaim how much of the IR-C2V8-01 reproduction an ordinary run recomputes",
     _m_overclaim_the_skeleton_repro, "C2V9-SKEL-REPRO", "WHICH HALF"),
    ("stop retaining one of the skeleton vectors", _m_drop_a_skeleton_vector,
     "C2V9-SKEL-REPRO", "IR-C2V8-01"),
    ("flip this document's own claim to have reproduced IR-C2V8-01",
     _m_flip_the_skeleton_reproduction_claim, "C2V9-CANDIDATE",
     "theSkeletonDefect/minimalReproduction/reproducedByThisLane"),
    ("drift the recorded digest of the +11-byte mutant",
     _m_drift_the_skeleton_mutant_digest, "C2V9-SKEL-REPRO",
     "nobody recomputes is prose"),
    ("republish the skeleton digest so it no longer describes this document",
     _m_corrupt_the_skeleton_digest, "C2V9-SKELETON", "documentSkeleton/sha256"),
    ("drift this document's own count of its boolean leaves",
     _m_drift_a_skeleton_count, "C2V9-CANDIDATE", "documentSkeleton/booleanLeaves"),
    ("soften the IR-C2V7-01 minimal reproduction", _m_soften_the_enumeration_repro,
     "C2V9-ENUM-REPRO", "no source modification"),
    ("overclaim how much of the IR-C2V7-01 reproduction an ordinary run recomputes",
     _m_overclaim_the_enumeration_repro, "C2V9-ENUM-REPRO", "WHICH HALF"),
    ("stop retaining one of the enumeration vectors", _m_drop_an_enumeration_vector,
     "C2V9-ENUM-REPRO", "IR-C2V7-01"),
    ("point the this-is-not-a-verdict disclaimer at the predecessor "
     "(OBS-C2V7-05 verbatim)", _m_disclaim_the_predecessor, "C2V9-DISCLAIMER",
     "check-c2-v7.py"),
)


def _s_inject_computed_operand_comparison(tree):
    """A wire value against a COMPUTED int -- the shape v4 missed."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v8_computed_probe(row, measured):\n"
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
        "def _c2v8_subset_probe(sites, authority):\n"
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
        "def _c2v8_operator_probe(row, measured):\n"
        "    if ne(row.get('schemaVersion'), measured):\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_dict_key_lookup(tree):
    """`1 in {1.0: x}` is True: the hashes agree."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v8_keylookup_probe(row, table):\n"
        "    if table[row.get('schemaVersion')]:\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_dedup_cardinality(tree):
    """`len({1, 1.0, True})` is 1: three JSON values become one measurement."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v8_dedup_probe(rows):\n"
        "    seen = set(row.get('count') for row in rows)\n"
        "    return list(seen)\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_named_constant_comparison(tree):
    """A wire value against a module-level named integer, not a literal."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "_LAW18_PROBE = 1\n"
        "def _c2v9_named_constant_probe(row):\n"
        "    if row.get('schemaVersion') != _LAW18_PROBE:\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_membership_comparison(tree):
    """`not in (1,)` -- membership in a numeric literal container."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v8_membership_probe(row):\n"
        "    if row.get('schemaVersion') not in (1,):\n"
        "        return ['probe']\n"
        "    return []\n").body)
    return ast.fix_missing_locations(subject)


def _s_inject_sorted_launder(tree):
    """`max` over a mixed set returns whichever the host language reached first."""
    subject = copy.deepcopy(tree)
    subject.body.extend(ast.parse(
        "def _c2v8_sorted_probe(rows):\n"
        "    return max(row.get('count') for row in rows)\n").body)
    return ast.fix_missing_locations(subject)


# Each scan row names the function it injects, so the assertion is on a specific
# finding id AND on the position under test.  v5's three scan rows carried no
# expected id at all and asserted only that a count rose.
SCAN_MUTATIONS = (
    ("inject a wire value compared against a COMPUTED integer",
     _s_inject_computed_operand_comparison, "C2V9-SCAN", "_c2v8_computed_probe"),
    ("inject IR-C2V5-01's comprehension-result subset test verbatim",
     _s_inject_comprehension_subset, "C2V9-SCAN", "_c2v8_subset_probe"),
    ("inject an operator.ne call, which is never an ast.Compare",
     _s_inject_operator_call, "C2V9-SCAN", "_c2v8_operator_probe"),
    ("inject a dict key lookup on a wire key", _s_inject_dict_key_lookup,
     "C2V9-SCAN", "_c2v8_keylookup_probe"),
    ("inject a set() dedup that collapses 1, 1.0 and True",
     _s_inject_dedup_cardinality, "C2V9-SCAN", "_c2v8_dedup_probe"),
    ("inject a wire value compared against a module-level named integer",
     _s_inject_named_constant_comparison, "C2V9-SCAN", "_c2v9_named_constant_probe"),
    ("inject membership in a numeric literal container",
     _s_inject_membership_comparison, "C2V9-SCAN", "_c2v8_membership_probe"),
    ("inject a max() over a wire sequence", _s_inject_sorted_launder,
     "C2V9-SCAN", "_c2v8_sorted_probe"),
)


# L8's retained rows, applied to the CANDIDATE'S OWN BYTES rather than to a
# parsed copy, because that is the only level at which IR-C2V6-01 exists.
# (name, needle, replacement, expected finding id, subject substring)
PARSE_MUTATIONS = (
    ("shadow this document's own version key with a JSON float (IR-C2V6-01 verbatim)",
     '  "version": 9,\n', '  "version": 9.0,\n  "version": 9,\n',
     "C2V9-DUPKEY", "version"),
    ("shadow this document's own supersedes key",
     '  "supersedes": 8,\n', '  "supersedes": 8.0,\n  "supersedes": 8,\n',
     "C2V9-DUPKEY", "supersedes"),
    ("shadow a measured counter three levels down",
     '    "pinnedInputs": ', '    "pinnedInputs": 1.0,\n    "pinnedInputs": ',
     "C2V9-DUPKEY", "v9MeasuredCounters/pinnedInputs"),
    ("shadow a leaf inside an array element - IR-C2V5-01's own position",
     '        "line": 2487,\n', '        "line": 2487.0,\n        "line": 2487,\n',
     "C2V9-DUPKEY", "theDefect/repairedComparisonSites/0/line"),
    ("put a non-RFC constant into the bytes",
     '  "supersedes": 8,\n', '  "supersedes": NaN,\n',
     "C2V9-NONRFC", "NaN"),
    ("respell a number token so the bytes and the value differ",
     '  "supersedes": 8,\n', '  "supersedes": -0,\n',
     "C2V9-NUMBER-TEXT", "-0"),
    ("shadow this document's own SKELETON node count, inside the block that binds "
     "the shape of every node",
     '\n    "nodes": ', '\n    "nodes": 1.0,\n    "nodes": ',
     "C2V9-DUPKEY", "documentSkeleton/nodes"),
    ("CONTROL: eighteen bytes of whitespace, which change nothing", "\n  \"version\"",
     "\n\n  \"version\"", "", ""),
)


def parse_mutation_findings(text, authority):
    """Drive one byte-level mutant through the LIVE parse and the LIVE finding
    function.  Reads BYTES, exactly as `main` does."""
    try:
        _value, problems = jx_loads(text)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return ["C2V9-PARSE: the mutant did not parse (" + type(exc).__name__ + ": " +
                str(exc) + ")"]
    return parse_problem_findings(problems, authority.document_name)


def pinned_v6_over_a_duplicate_key(authority):
    """Execute the PINNED, REJECTED check-c2-v6.py over the eighteen-byte edit.

    This is the one measurement in this artifact that an ordinary invocation
    does NOT recompute, because it costs about eighty seconds and would double
    the cost of every run.  It is recomputed HERE, by the retained suite, on the
    hash-verified bytes of both the predecessor checker and the predecessor
    document, so the claim `the pinned v6 admits it to a FULLY GREEN run` is
    executed rather than carried in prose.  The result is cached on `external`,
    which no mutation of THIS file can invalidate and which `pinned.clear()`
    therefore does not touch.
    """
    cached = jx_get(authority.external, "v6-duplicate-key")
    if cached is not None:
        return cached
    vector, document, needle, insert, position, _note = PARSE_DIFFERENTIAL_VECTORS[0]
    original = authority.snapshots[document].decode("utf-8")
    mutant = original.replace(needle, insert + needle, 1)
    sink = io.StringIO()
    try:
        with redirect_stdout(sink):
            v6 = _execute_snapshot("opensip_c2v9_pinned_v6_checker", V6_CHECKER,
                                   authority.snapshots[V6_CHECKER], authority.directory)
            v6_authority = v6.load_authority(authority.directory)
            findings = v6.check(json.loads(mutant, object_pairs_hook=None), v6_authority)
    except BaseException as exc:                            # noqa: BLE001 - measured
        findings = ["the pinned v6 checker could not be executed: " +
                    type(exc).__name__ + ": " + str(exc)]
    result = {"vector": vector, "document": document, "position": position,
              "bytesAdded": len(mutant.encode("utf-8")) - len(original.encode("utf-8")),
              "v6FindingCount": len(findings),
              "v6FullyGreen": not findings,
              "v6First": "" if not findings else str(findings[0])[:160],
              "v9Findings": parse_mutation_findings(mutant, authority)}
    jx_put(authority.external, "v6-duplicate-key", result)
    return result


def pinned_v7_over_a_boolean_flip(authority):
    """Execute the PINNED, REJECTED check-c2-v7.py over the ONE-BYTE edit.

    IR-C2V7-01's own minimal reproduction, executed rather than described:
    `theParseDefect/minimalReproduction/reproducedByThisLane` in the pinned v7
    document -- that document's own claim that the v7 lane reproduced the single
    finding v7 existed to discharge -- flipped from true to false, one token,
    ONE BYTE, zero bytes of Python.  The pinned v7 must still run FULLY GREEN
    over it.  If it ever stops doing so, the external anchor this repair is
    measured against has changed and the suite says so by name.

    This is the one measurement of the enumeration repair that an ordinary
    invocation does NOT recompute, because it costs about eighty seconds; the
    per-run half is L6d, which recomputes the MECHANISM against the same pinned
    bytes.  RES-C2V9-11.
    """
    cached = jx_get(authority.external, "v7-boolean-flip")
    if cached is not None:
        return cached
    needle, replacement, position = PINNED_V7_BOOLEAN_EDIT
    original = authority.snapshots[V7_CONTRACT].decode("utf-8")
    mutant = original.replace(needle, replacement, 1)
    sink = io.StringIO()
    try:
        with redirect_stdout(sink):
            v7 = _execute_snapshot("opensip_c2v9_pinned_v7_executed", V7_CHECKER,
                                   authority.snapshots[V7_CHECKER],
                                   authority.directory)
            v7_authority = v7.load_authority(authority.directory)
            findings = v7.check(json.loads(mutant, object_pairs_hook=None),
                                v7_authority)
    except BaseException as exc:                            # noqa: BLE001 - measured
        findings = ["the pinned v7 checker could not be executed: " +
                    type(exc).__name__ + ": " + str(exc)]
    census = [row for row in jx_leaf_census(json.loads(mutant,
                                                       object_pairs_hook=jx_refusing_pairs))
              if jx_equal(row[0], list(position))]
    result = {"document": V7_CONTRACT, "position": _steps_text(position),
              "bytesAdded": len(mutant.encode("utf-8")) - len(original.encode("utf-8")),
              "mutantDigest": hashlib.sha256(mutant.encode("utf-8")).hexdigest(),
              "v7FindingCount": len(findings),
              "v7FullyGreen": not findings,
              "v7First": "" if not findings else str(findings[0])[:160],
              "v9CensusReportedIt": bool(census),
              "v9LeafType": census[0][1] if census else ""}
    jx_put(authority.external, "v7-boolean-flip", result)
    return result


def pinned_v8_over_a_path_collision(authority):
    """Execute the PINNED, REJECTED check-c2-v8.py over the +11-BYTE edit.

    IR-C2V8-01's own minimal reproduction, executed rather than described:
    `thePrimitive/theEnumerationIsAGateToo` in the pinned v8 document -- that
    document's own account of why the enumeration is a gate -- relocated to a
    ROOT key named with the literal text of its old path.  ONE contiguous
    replacement, ELEVEN bytes, zero bytes of Python.  The pinned v8 must still
    run FULLY GREEN over it, with documentSkeleton.sha256 and all of
    945/148/797 byte-identical.  If it ever stops doing so, the external anchor
    this repair is measured against has changed and the suite says so by name.

    This is the one measurement of the identity repair that an ordinary
    invocation does NOT recompute, because it costs about eighty seconds; the
    per-run half is L6e, which recomputes the MECHANISM against the same pinned
    bytes.  RES-C2V9-11.
    """
    cached = jx_get(authority.external, "v8-path-collision")
    if cached is not None:
        return cached
    opener, closer, new_open, new_close, position = PINNED_V8_PATH_COLLISION_EDIT
    original = authority.snapshots[V8_CONTRACT].decode("utf-8")
    head = original.index(opener)
    tail = original.index(closer, head)
    mutant = (original[:head] + new_open + original[head + len(opener):tail] +
              new_close + original[tail + len(closer):])
    sink = io.StringIO()
    try:
        with redirect_stdout(sink):
            v8 = _execute_snapshot("opensip_c2v9_pinned_v8_executed", V8_CHECKER,
                                   authority.snapshots[V8_CHECKER],
                                   authority.directory)
            v8_authority = v8.load_authority(authority.directory)
            findings = v8.check(json.loads(mutant, object_pairs_hook=None),
                                v8_authority)
            predecessor_digest = v8.document_skeleton_digest(
                json.loads(mutant, object_pairs_hook=None))
            predecessor_clean = v8.document_skeleton_digest(
                json.loads(original, object_pairs_hook=None))
    except BaseException as exc:                            # noqa: BLE001 - measured
        findings = ["the pinned v8 checker could not be executed: " +
                    type(exc).__name__ + ": " + str(exc)]
        predecessor_digest, predecessor_clean = "unmeasured", "unmeasured-too"
    parsed_mutant, _problems = jx_loads(mutant)
    parsed_clean, _clean_problems = jx_loads(original)
    result = {"document": V8_CONTRACT, "position": _steps_text(position),
              "bytesAdded": len(mutant.encode("utf-8")) - len(original.encode("utf-8")),
              "mutantDigest": hashlib.sha256(mutant.encode("utf-8")).hexdigest(),
              "v8FindingCount": len(findings),
              "v8FullyGreen": not findings,
              "v8First": "" if not findings else str(findings[0])[:160],
              "v8SkeletonUnmoved": jx_equal(predecessor_digest, predecessor_clean),
              "v9SkeletonMoved": jx_ne(document_skeleton_digest(parsed_mutant),
                                       document_skeleton_digest(parsed_clean))}
    jx_put(authority.external, "v8-path-collision", result)
    return result


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


# The parsed-JSON roots that are not objects.  A tuple rather than an inline
# loop so the retained row count below is derived from the tables and never from
# a number somebody typed.
PARSED_ROOT_CASES = (("string", "hostile-root"), ("null", None), ("list", []),
                     ("empty-object", {}))
# Every retained row of the suite, derived.  v6 printed `zero of 96 mutations
# executed` when it refused a dirty base and `109 rows` when it passed, because
# the refusal counted three tables and the pass counted seven groups.  Both were
# honest and a reader comparing them saw thirteen rows go missing.  There is one
# number now, it is derived from the tables, and the suite refuses if the rows it
# actually executed do not equal it.
RETAINED_ROWS = (len(PARSED_ROOT_CASES) + len(CONTRACT_MUTATIONS) +
                 len(SOURCE_MUTATIONS) + len(SCAN_MUTATIONS) + len(PARSE_MUTATIONS) +
                 3 + len(DIFFERENTIAL_VECTORS) + len(SUCCESSOR_DIFFERENTIAL_VECTORS) +
                 len(ENUMERATION_DIFFERENTIAL_VECTORS) +
                 len(SKELETON_DIFFERENTIAL_VECTORS))


def selftest(candidate, authority, path):
    """Always reaches the suite; refuses a dirty base with a distinct code."""
    base_findings = check(candidate, authority)
    total = RETAINED_ROWS
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
    print("C-2 v9 mutation self-test over " + path.name + " - each row must be REJECTED "
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

    for name, root in PARSED_ROOT_CASES:
        findings = check(copy.deepcopy(root), authority)
        named = hit_for(findings, "C2V9-TOTALITY-ROOT", "non-empty JSON object")
        if not named:
            escaped.append("parsed-JSON root " + name + ": no named C2V9-TOTALITY-ROOT "
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
            findings = ["C2V9-SCAN: " + site["function"] + " line " +
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
               "NO C2V9-SCAN finding naming " + subject)

    # ---- L8.  BYTE-LEVEL rows.  Everything above this point mutates a PARSED
    # object; IR-C2V6-01 exists only in the bytes, so these rows edit the
    # candidate's own text and drive it through the live parse.
    try:
        candidate_text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        candidate_text = ""
        escaped.append("the candidate's bytes could not be re-read for the byte-level "
                       "rows (" + type(exc).__name__ + ")")
    for name, needle, replacement, expected, subject in PARSE_MUTATIONS:
        if not jx_int_in_range(candidate_text.count(needle), 1, 1):
            escaped.append(name + ": " + repr(needle) + " does not occur exactly once "
                           "in the candidate's bytes, so the retained byte-level row is "
                           "not executable")
            report(False, name, "the anchor text is not unique in the candidate bytes")
            continue
        mutant = candidate_text.replace(needle, replacement, 1)
        findings = parse_mutation_findings(mutant, authority)
        if not expected:
            ok = not findings
            if not ok:
                escaped.append(name + ": the CONTROL was refused by " + findings[0][:120])
            report(ok, name, "no byte/parse divergence, as required" if ok
                   else findings[0][:180])
            continue
        hit = hit_for(findings, expected, subject)
        if not hit:
            escaped.append(name + ": " + str(len(findings)) + " finding(s) but none is " +
                           expected + " naming " + repr(subject) + " - the bytes and the "
                           "parse were allowed to disagree, which is IR-C2V6-01")
        report(bool(hit), name, hit[0][:180] if hit else
               (str(len(findings)) + " unrelated finding(s); first: " + findings[0][:150]
                if findings else "NO FINDING"))

    # The external anchor: the PINNED, REJECTED check-c2-v6.py executed over the
    # eighteen-byte edit it was rejected for.  Not recomputed by an ordinary
    # invocation; recomputed here.
    external = pinned_v6_over_a_duplicate_key(authority)
    v9_hit = hit_for(external["v9Findings"], "C2V9-DUPKEY", external["position"])
    ok = external["v6FullyGreen"] and bool(v9_hit)
    if not external["v6FullyGreen"]:
        escaped.append("the pinned " + V6_CHECKER + " no longer runs FULLY GREEN over "
                       "the " + str(external["bytesAdded"]) + "-byte duplicate-key edit "
                       "of the pinned " + external["document"] + " (" +
                       str(external["v6FindingCount"]) + " finding(s), first: " +
                       external["v6First"] + "); the external anchor this repair is "
                       "measured against has changed")
    if not v9_hit:
        escaped.append("this checker did NOT name " + external["position"] + " in the "
                       "eighteen-byte duplicate-key edit of the pinned " +
                       external["document"])
    report(ok, "IR-C2V6-01 against the PINNED check-c2-v6.py [" + V6_CHECKER + "]",
           "pinned v6 over the " + str(external["bytesAdded"]) + "-byte edit: " +
           str(external["v6FindingCount"]) + " finding(s), FULLY GREEN: " +
           str(external["v6FullyGreen"]) + "; this checker: " +
           (v9_hit[0][:140] if v9_hit else "NO NAMED FINDING"))

    # The second external anchor: the PINNED, REJECTED check-c2-v7.py executed
    # over the ONE-BYTE boolean edit it was rejected for.  Not recomputed by an
    # ordinary invocation; recomputed here.  IR-C2V7-01.
    flip = pinned_v7_over_a_boolean_flip(authority)
    ok = flip["v7FullyGreen"] and flip["v9CensusReportedIt"] and \
        jx_equal(flip["v9LeafType"], "boolean")
    if not flip["v7FullyGreen"]:
        escaped.append("the pinned " + V7_CHECKER + " no longer runs FULLY GREEN over "
                       "the " + str(flip["bytesAdded"]) + "-byte boolean edit of the "
                       "pinned " + flip["document"] + " (" + str(flip["v7FindingCount"]) +
                       " finding(s), first: " + flip["v7First"] + "); the external "
                       "anchor this repair is measured against has changed")
    if not flip["v9CensusReportedIt"]:
        escaped.append("this checker's own leaf census does NOT report a leaf at " +
                       flip["position"] + " in the one-byte boolean edit of the pinned "
                       + flip["document"] + ", so the repair does not do the thing it "
                       "exists to do")
    report(ok, "IR-C2V7-01 against the PINNED check-c2-v7.py [" + V7_CHECKER + "]",
           "pinned v7 over the " + str(flip["bytesAdded"]) + "-byte edit (sha256:" +
           flip["mutantDigest"] + "): " + str(flip["v7FindingCount"]) +
           " finding(s), FULLY GREEN: " + str(flip["v7FullyGreen"]) +
           "; this checker's census reports a JSON " + repr(flip["v9LeafType"]) +
           " leaf at " + flip["position"])

    # The third external anchor: the PINNED, REJECTED check-c2-v8.py executed
    # over the +11-BYTE reparenting edit it was rejected for.  Not recomputed by
    # an ordinary invocation; recomputed here.  IR-C2V8-01.
    collision = pinned_v8_over_a_path_collision(authority)
    ok = collision["v8FullyGreen"] and collision["v8SkeletonUnmoved"] and \
        collision["v9SkeletonMoved"] and \
        jx_int_in_range(collision["bytesAdded"], 11, 11)
    if not collision["v8FullyGreen"]:
        escaped.append("the pinned " + V8_CHECKER + " no longer runs FULLY GREEN over "
                       "the +" + str(collision["bytesAdded"]) + "-byte reparenting edit "
                       "of the pinned " + collision["document"] + " (" +
                       str(collision["v8FindingCount"]) + " finding(s), first: " +
                       collision["v8First"] + "); the external anchor this repair is "
                       "measured against has changed")
    if not collision["v8SkeletonUnmoved"]:
        escaped.append("the pinned " + V8_CHECKER + "'s own skeleton digest MOVES for "
                       "the reparenting edit, so IR-C2V8-01's mechanism is not what "
                       "this repair is measured against")
    if not collision["v9SkeletonMoved"]:
        escaped.append("this checker's skeleton does NOT move for the reparenting edit "
                       "at " + collision["position"] + ", so the repair does not do the "
                       "thing it exists to do")
    if not jx_int_in_range(collision["bytesAdded"], 11, 11):
        escaped.append("the reparenting edit adds " + str(collision["bytesAdded"]) +
                       " byte(s), not the eleven IR-C2V8-01 was graded under")
    report(ok, "IR-C2V8-01 against the PINNED check-c2-v8.py [" + V8_CHECKER + "]",
           "pinned v8 over the +" + str(collision["bytesAdded"]) + "-byte edit at " +
           collision["position"] + " (sha256:" + collision["mutantDigest"] + "): " +
           str(collision["v8FindingCount"]) + " finding(s), FULLY GREEN: " +
           str(collision["v8FullyGreen"]) + "; its own skeleton digest unmoved: " +
           str(collision["v8SkeletonUnmoved"]) + "; this checker's skeleton moved: " +
           str(collision["v9SkeletonMoved"]))

    for row in authority.skeleton_differential["rows"]:
        ok = row["successorSkeletonMoved"] and \
            jx_equal(row["predecessorSkeletonMoved"], row["predecessorExpectedToMove"])
        if not ok:
            escaped.append(row["vector"] + ": skeleton differential lost")
        report(ok, "retained skeleton vector " + row["vector"] + " at " + row["path"] +
               " (" + row["operation"] + ")",
               "the pinned check-c2-v8.py skeleton moved: " +
               str(row["predecessorSkeletonMoved"]) + " (expected " +
               str(row["predecessorExpectedToMove"]) + "); this checker's skeleton "
               "moved: " + str(row["successorSkeletonMoved"]))

    for row in authority.enumeration_differential["rows"]:
        ok = row["successorEnumeratedIt"] and \
            jx_equal(row["predecessorEnumeratedIt"], row["predecessorExpectedToReachIt"])
        if not ok:
            escaped.append(row["vector"] + ": enumeration differential lost")
        report(ok, "retained enumeration vector " + row["vector"] + " at " +
               row["path"] + " as a JSON " + row["type"],
               "the pinned check-c2-v7.py enumeration reached it: " +
               str(row["predecessorEnumeratedIt"]) + " (expected " +
               str(row["predecessorExpectedToReachIt"]) + "); this checker's leaf "
               "census reached it: " + str(row["successorEnumeratedIt"]))

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
        ok = row["v9NamedThePosition"] and row["v5FullyGreen"]
        if not ok:
            escaped.append(row["vector"] + ": successor differential lost")
        report(ok, "retained v5 blocking vector " + row["vector"] + " at " + row["path"],
               "pinned check-c2-v5.py ran FULLY GREEN over it: " +
               str(row["v5FullyGreen"]) + "; this checker named the analogous position "
               "of its own document: " + str(row["v9NamedThePosition"]))

    print()
    if not jx_int_in_range(rows, RETAINED_ROWS, RETAINED_ROWS):
        escaped.append("the suite executed " + str(rows) + " rows but its tables "
                       "declare " + str(RETAINED_ROWS) + "; a row that stops executing "
                       "is a retained case that has quietly become prose")
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
    print("  " + str(len(PARSE_MUTATIONS)) + " of these rows edit the candidate's OWN "
          "BYTES rather than a parsed copy, because IR-C2V6-01 exists only in the bytes; "
          "and one executes the PINNED, REJECTED check-c2-v6.py over the eighteen-byte "
          "duplicate-key edit it was rejected for, which must still run FULLY GREEN - "
          "that is the one measurement an ordinary invocation does not recompute, and "
          "this is where it is recomputed")
    print("  and one executes the PINNED, REJECTED check-c2-v8.py over the +11-byte "
          "reparenting edit it was rejected for, which must still run FULLY GREEN with "
          "its own skeleton digest UNMOVED - IR-C2V8-01's bright line, recomputed here "
          "rather than transcribed")
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
        print("C2V9-UNSUPPORTED-INVOCATION: " + str(exc), file=sys.stderr)
        return 2
    try:
        authority = load_authority()
    except AuthorityLoadError as exc:
        print("C2V9-PINNED-INPUT-REFUSED: " + type(exc).__name__ + ": " + str(exc),
              file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    # INERT BYTES FIRST, exactly once, and the digest of THOSE bytes is what the
    # banner reports.  `read_text` was a locale decode and a second unrecorded
    # read of the thing the verdict is about; this reads the bytes, records
    # them, and decodes UTF-8 explicitly.
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        print("cannot load C-2 v9 candidate " + str(path) + ": " + type(exc).__name__ +
              ": " + str(exc), file=sys.stderr)
        return 2
    try:
        candidate, problems = jx_loads(text)
    except (json.JSONDecodeError, JxDomainError) as exc:
        print("cannot load C-2 v9 candidate " + str(path) + ": " + type(exc).__name__ +
              ": " + str(exc), file=sys.stderr)
        return 2
    authority.document_name = path.name
    authority.candidate_digest = hashlib.sha256(raw).hexdigest()
    authority.candidate_bytes = len(raw)
    authority.parse_findings = parse_problem_findings(problems, path.name)
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
