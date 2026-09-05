#!/usr/bin/env python3
"""Retained executable checker for the C-2 plan/stage contract, v5.

WHY v5 EXISTS
-------------
c2-plan-stage-schema.v4.json passed independent review at 0 blocking findings.
An independent adjudication of the single MAJOR residual IR-C2V4-01
(c2-plan-stage-schema.v4.adjudication-ir-c2v4-01.json, disposition BLOCKING)
then demonstrated a false accept on the FROZEN bytes of check-c2-v4.py:

    c2-plan-stage-schema.v4.json
      hostileScalarLeafTotality.contractRoot.scalarLeafPaths: 2538 -> 2538.0
    python3 -I -B artifacts/check-c2-v4.py <that file>   ->   exit 0, green banner

ONE JSON edit.  No source modification.  No compensation.  The banner printed
over it contains the phrase `0 type-distinct constant admissions`, which is the
counter whose declared meaning is that no type-distinct spelling of a declared
integer constant may be admitted.  `2538.0 != 2538` is False in the host
language.  That is character-for-character LB-C2-01 -- the defect that made v3 a
REJECT -- living inside the artifact authored to repair LB-C2-01.

Three unguarded sites, all inside check-c2-v4.py `_census_findings`, all inside
the scan's own declared 69-function closure:

    line 2487   if row.get(key) != value:                 (value: a COMPUTED int)
    line 2493   if row.get(key) != measured["stats"][key]:
    line 2517   if root_row.get(key) != value:

48 wire-sourced integer positions are read through them.  16 of those positions
currently hold 0 or 1 and are therefore boolean-exploitable as well.

WHY THE PREDECESSOR'S OWN SCAN COULD NOT SEE IT
-----------------------------------------------
check-c2-v4.py `_numeric_literal` requires `isinstance(node, ast.Constant)`.  The
independent pre-freeze review widened that only to module-level names bound to
numeric constants, and defined its "exhaustive" sweep as every ast.Compare with a
numeric-LITERAL operand.  A wire value compared against a COMPUTED integer
contains no numeric literal, so it is invisible to the instrument AND to the
audit of the instrument.  Both concluded the blind spot was empty.  It was
occupied, and had been since the file was written.

The narrowing is the root cause, so v5 INVERTS the predicate rather than widening
it: a wire operand in an equality, ordering or literal-container membership test
is a finding UNLESS it is routed through a declared type gate.  The burden moves
from "prove this operand is numeric" to "prove this comparison is type-exact".

WHAT THIS CHECKER DOES NOT REBUILD
----------------------------------
The adjudication confirms, by execution, that LB-C2-01 is genuinely repaired at
the wire-validator surface and that the seven pinned planIntentCommitment vectors
are unmoved.  v5 therefore does NOT restate the C-2 contract or reimplement its
validators.  check-c2-v4.py is hash-pinned and EXECUTED from its verified
in-memory snapshot as an inherited oracle, and the effective v5 contract is the
verified v4 document with a short, typed, self-verifying operation list applied.
Nothing is transcribed.  The repair is added; the admission surface is untouched.

THE LAYERS, AND WHAT STANDS BEHIND EACH
---------------------------------------
L0  hash-before-execution over 13 pinned transitive inputs, plus a cross-check
    that this pin table agrees digit-for-digit with the predecessor's own PINS
    at every shared name.
L1  INHERITED.  check-c2-v4.py check() over the v4-identity projection of the
    effective contract.  Everything not in dispute is re-established by
    executing the reviewed bytes, not by restating them.
L2  REPAIR.  A type-exact census comparator with a SINGLE acceptance path,
    `wire_int_equal(published, measured)` -- BOTH operands gated, type before
    content, which is IMPLEMENTATION-FREEZE.md section 6 law 18 as a matter of
    design rather than of coincidence.
L2b DOCUMENT-WIDE TYPE LOCK.  THREE SITES WAS NOT THE COMPLETE SET.  Before
    scoping the repair, a float was substituted at each of the 136 integer
    leaves of the predecessor document in turn and every mutant was driven
    through check-c2-v4.py.  57 of the 136 produced exit 0 and a FULL GREEN
    BANNER, and only 32 of those 57 are census counters.  The other 25 are
    contract-declared bounds, budget maxima, range limits and planDescriptor
    mappings that the three adjudicated sites do not reach -- including the
    upper bound inside the predecessor's OWN integer-constant register, the
    register whose stated purpose is that a fifth site cannot be added
    silently.  A repair scoped to the census block would have closed 32 of 57
    and shipped the rest.  L2b therefore type-locks EVERY integer leaf of the
    document against the verified predecessor, in both directions, and
    float-probes every one of them live on every run: total over the class
    instead of enumerated over its known members.
L3  REGISTER.  The set of positions L2 compares is derived from the live
    measurement, and must equal the contract's declared register exactly, in
    both directions.  The inherited half of that register must equal the
    predecessor's own DECLARED_INTEGER_CONSTANT_IDS, read out of the executed
    module.  This is what makes "a fifth site cannot be added silently" true of
    the census block rather than merely claimed of it.
L4  SCAN.  An inverted, source-reading scan over the whole function universe --
    every FunctionDef, AsyncFunctionDef, nested def, method and lambda, with a
    fixpoint taint model -- that SEES COMPUTED OPERANDS.  Run over the pinned
    predecessor's tree it reports the three adjudicated sites by line number;
    run over this file's tree it must report none.
L5  BEHAVIOURAL.  Does not read source.  Every registered position is spelled in
    every declared hostile JSON type and driven through the live comparator; each
    case must produce a finding whose id is C2V5-TYPE and which NAMES the
    position.  Assertion is on the finding id, never on an exit code.
L6  PREDECESSOR DIFFERENTIAL.  The retained false-accept vectors from the
    adjudication are executed against BOTH checkers.  check-c2-v4.py must still
    admit them (it is pinned; it cannot change) and this checker must reject them
    by name.  If the differential ever collapses to zero the repair has regressed
    to its predecessor, and that is itself a finding.  This is the layer that
    stands behind L2 without trusting anything this file believes about itself:
    it is anchored to external bytes that are known to fail.
L7  SELF-MUTATION.  --selftest breaks L2, L2b, L3, L4 and L5 in copies of this
    file's own syntax tree and requires each break to be detected BY THE LAYER
    IT BREAKS.  Every row -- contract mutation, source mutation, scan mutation
    and retained false accept -- asserts on a specific finding id, never on the
    exit code.  Two rows of this suite were passing on unrelated findings
    before that column existed, which is the adjudication's trap reproduced
    inside the repair itself.

WHAT STANDS BEHIND L7: NOTHING BUT INDEPENDENT REVIEW.  That is stated here
rather than hidden, because the adjudication's finding was precisely that the
predecessor's terminal layer had nothing behind it and did not say so.  L7 is
terminal by construction -- a mutation battery cannot falsify itself -- and is
kept deliberately small and fully printed so a reviewer can audit every row.

EVERY GUARD HAS A BLIND SPOT.  Theirs are enumerated in the contract's
guardInventory block and repeated in knownBlindSpots below; the checker refuses
to report clean if that block claims total coverage.

KNOWN BLIND SPOTS OF THIS INSTRUMENT
------------------------------------
1. L4 is still SYNTACTIC.  Its excusal test is textual: a type gate excuses a
   comparison when a gate call with the same unparsed first argument appears
   earlier in the same statement, in an enclosing if/while test, or in an
   immediately preceding early-return guard.  Textual identity is not a
   dominance proof.  L5 and L6 are carried because of this, and L5 reads no
   source at all.
2. L4 cannot see a comparison constructed at run time (operator.ne, eval, a
   dispatch table of comparators).  It counts and publishes those primitives
   instead: eval/exec/getattr-dispatch counts are measured and must be zero in
   this file.
3. L5 is exhaustive over the REGISTERED positions only.  A published counter
   that is neither measured nor registered is invisible to it -- which is why L3
   derives the position set from the measurement and fails closed on any
   asymmetry.
4. L6 only proves the repair differs from the predecessor where the predecessor
   is known-defective.  A defect this checker introduces at a position the
   predecessor handled correctly is invisible to L6; L5 covers that direction.
5. This file cannot hash-pin itself.  Its own digest is REPORTED, not verified.
6. v5 does not re-run the predecessor's ~24k-case contract-root execution
   matrix; that is check-c2-v4.py --selftest, which is pinned and unchanged.
   Retained as residual RES-C2V5-03 rather than absorbed.
7. The 57-of-136 predecessor sweep is reproduced per run only as a three-vector
   sample.  The SUCCESSOR side of L2b is exhaustive on every run; the
   PREDECESSOR side is sampled, because 136 full predecessor runs cost about
   seventy seconds.  Retained as RES-C2V5-07.
8. This repair covers integer-typed positions.  A closed STRING scalar spelled
   as a different JSON type is caught where the code gates it but is not swept
   exhaustively here; law 18 names strings too, and that half is not claimed.

Usage: python3 -I -B artifacts/check-c2-v5.py [contract]  ·  --selftest
Exit:  0 clean or green selftest · 1 findings · 2 unsupported invocation or a
       pinned input that does not hash to its declared digest · 3 --selftest
       REFUSED over a dirty base, which can never be absorbed into a pass.

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
import types
from contextlib import redirect_stdout

BINDING = "c2-plan-stage-schema.v5.json"
DECLARED_FLAGS = ("--selftest",)
DECLARED_EXIT_CODES = frozenset({"0", "1", "2", "3"})
HERE = pathlib.Path(__file__).resolve().parent
ARTIFACT_ID = "opensip.c2-plan-stage-schema.v5"

V4_CHECKER = "check-c2-v4.py"
V4_CONTRACT = "c2-plan-stage-schema.v4.json"
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

# Freeze section 7.2 recording obligation: filename AND digest for every input
# this artifact depends on.  A count is not a record.  Every entry below is read
# once as inert bytes, verified, and then parsed or executed from that verified
# byte string -- never a second disk read between verification and execution.
PINS: dict[str, str] = {
    V4_CHECKER: "54ff764d155f5582bc66fd7bf8138b7eaed5f90f46b92975c4bc7a85ffb3df17",
    V4_CONTRACT: "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
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

# The adjudication this successor exists to discharge.  A repair lane that
# quietly points at a softened disposition is refused at load, not reported.
ADJUDICATION_BINDING = {
    "findingId": "IR-C2V4-01",
    "disposition": "BLOCKING",
    "artifact": "c2-plan-stage-schema.v4.adjudication-ir-c2v4-01",
}
REVIEW_BINDING = {"verdict": "REJECT", "blockingFindingCount": 2}

MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
    ZeroDivisionError, OverflowError, RecursionError,
)


class AuthorityLoadError(RuntimeError):
    """A pinned input could not be admitted as authority."""


class PinMismatch(AuthorityLoadError):
    """A pinned byte string does not hash to its declared digest."""


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this checker does not accept."""


# ---------------------------------------------------------------------------
# Section 1.  The law-18 guard helpers.
#
# Every integer test in this checker routes through these.  `wire_int_equal` is
# the v5 addition and it is the whole repair: it gates BOTH operands, because
# the defect IR-C2V4-01 names is a wire value compared against a COMPUTED int,
# and a guard that only inspects the wire side would still be trusting that the
# computed side is what the instrument thinks it is.
# ---------------------------------------------------------------------------

GUARD_HELPERS = ("is_wire_int", "exact_int", "int_in_range", "wire_int_equal",
                 "same_json_type")
TYPE_GATES = GUARD_HELPERS + ("isinstance",)
_MAX_SCAN_DEPTH = 6
# The only two exec() sites this file is permitted: the verified-snapshot module
# loader and the self-mutation tree executor.  Both compile bytes that were
# hash-verified or derived from this file's own verified-at-read tree.  L4
# counts them and refuses any third.  Nothing here evaluates caller input.
DECLARED_EXEC_SITES = 2
# isinstance() is a legitimate law-18 gate ONLY against classes that cannot
# admit a numeric spelling.  isinstance(x, int) is NOT a gate: True is an int.
NON_NUMERIC_CLASSES = frozenset({"str", "bytes", "dict", "list", "tuple", "set",
                                 "frozenset", "type(None)"})


def is_wire_int(value) -> bool:
    """True only for a JSON integer.  A JSON boolean is NOT a JSON integer."""
    return isinstance(value, int) and not isinstance(value, bool)


def exact_int(value, constant) -> bool:
    """Exact-type integer constant guard.  Rejects true, false, 1.0 and "1"."""
    return is_wire_int(value) and value == constant


def int_in_range(value, low, high) -> bool:
    """Exact-type integer range guard."""
    return is_wire_int(value) and low <= value <= high


def wire_int_equal(published, measured) -> bool:
    """Law 18 at a published counter: type of BOTH sides before content.

    `published` is parsed JSON.  `measured` is computed by the instrument.  The
    predecessor gated neither and admitted `2538.0 != 2538` as False.
    """
    return is_wire_int(published) and is_wire_int(measured) and published == measured


def same_json_type(left, right) -> bool:
    """Law 18's precondition, as a declared gate: same JSON type, exactly.

    `type(x) is type(y)` says the same thing, but an `is` test is invisible to
    the scan by design, and a gate the instrument cannot see is how IR-C2V4-01
    happened.  This is a NAMED gate so every structural comparison below is
    visibly routed through one.
    """
    return json_type_name(left) == json_type_name(right) and type(left) is type(right)


def json_type_name(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


# ---------------------------------------------------------------------------
# Section 2.  Hash-before-execution, and the inherited predecessor.
# ---------------------------------------------------------------------------


class _VerifiedSourceLoader:
    """Execute exactly the bytes that were hash-verified, never a re-read."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec):
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_snapshot(name: str, filename: str, source: bytes) -> types.ModuleType:
    path = (HERE / filename).resolve()
    loader = _VerifiedSourceLoader(path, source)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    if spec is None or spec.loader is None:
        raise AuthorityLoadError(f"cannot construct verified spec for {filename}")
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
    """Everything admitted after hash verification, and nothing else."""

    def __init__(self, snapshots, parsed, v4, v4_authority):
        self.snapshots = snapshots
        self.parsed = parsed
        self.v4 = v4
        self.v4_authority = v4_authority
        self.measurement = None
        self.scan_self = None
        self.scan_predecessor = None
        self.behavioural = None
        self.differential = None
        self.document_lock = None
        self.effective = None

    def json(self, name):
        return self.parsed.get(name)


def load_authority(directory: pathlib.Path = HERE) -> Authority:
    """Read every pinned input as inert bytes, verify, then execute."""
    snapshots: dict[str, bytes] = {}
    errors: list[str] = []
    for name, expected in PINS.items():
        try:
            source = (directory / name).read_bytes()
        except OSError as exc:
            errors.append(f"{name}: read {type(exc).__name__}: {exc}")
            continue
        actual = hashlib.sha256(source).hexdigest()
        if actual != expected:
            errors.append(f"{name}: {actual} != {expected}")
            continue
        snapshots[name] = source
    if errors:
        raise PinMismatch("; ".join(sorted(errors)))

    parsed: dict[str, object] = {}
    for name in PINS:
        if name.endswith(".json"):
            try:
                parsed[name] = json.loads(snapshots[name].decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise AuthorityLoadError(
                    f"cannot parse pinned data {name}: {type(exc).__name__}") from exc

    _refuse_softened_provenance(parsed)

    # Execute the predecessor from ITS verified snapshot, then immediately seed
    # its own-tree cache from the same snapshot so that nothing it does can
    # re-read check-c2-v4.py from disk behind the verification.
    sink = io.StringIO()
    with redirect_stdout(sink):
        v4 = _execute_snapshot("opensip_c2v5_pinned_v4_checker", V4_CHECKER,
                               snapshots[V4_CHECKER])
        v4._OWN_TREE_CACHE = ast.parse(snapshots[V4_CHECKER])
        v3_module = v4._execute_snapshot("opensip_c2v5_pinned_v3_checker", V3_CHECKER,
                                         snapshots[V3_CHECKER])
    _refuse_pin_table_disagreement(v4)
    v4_authority = v4.Authority(dict(snapshots), dict(parsed), {V3_CHECKER: v3_module})
    return Authority(snapshots, parsed, v4, v4_authority)


def _refuse_softened_provenance(parsed) -> None:
    adjudication = parsed.get(ADJUDICATION)
    if not isinstance(adjudication, dict):
        raise AuthorityLoadError(f"pinned adjudication {ADJUDICATION} is not an object")
    for key, expected in ADJUDICATION_BINDING.items():
        if not isinstance(adjudication.get(key), str) or \
                not same_json_type(adjudication.get(key), expected) or \
                adjudication.get(key) != expected:
            raise AuthorityLoadError(
                f"pinned adjudication {ADJUDICATION} carries {key}="
                f"{adjudication.get(key)!r}, not {expected!r}; this successor exists "
                "only to discharge a BLOCKING disposition and refuses to run against "
                "a softened one")
    review = parsed.get(V3_REVIEW)
    review = review if isinstance(review, dict) else {}
    if not isinstance(review.get("verdict"), str) or \
            review.get("verdict") != REVIEW_BINDING["verdict"] or \
            not exact_int(review.get("blockingFindingCount"),
                          REVIEW_BINDING["blockingFindingCount"]):
        raise AuthorityLoadError(
            f"pinned review {V3_REVIEW} no longer carries the REJECT verdict and the "
            "two blocking findings the C-2 repair chain is anchored to")
    prefreeze = parsed.get(PREFREEZE_REVIEW)
    if not isinstance(prefreeze, dict):
        raise AuthorityLoadError(f"pinned review {PREFREEZE_REVIEW} is not an object")


def _refuse_pin_table_disagreement(v4) -> None:
    """This pin table must agree with the predecessor's, digit for digit."""
    inherited = getattr(v4, "PINS", None)
    if not isinstance(inherited, dict) or not inherited:
        raise AuthorityLoadError("the pinned predecessor exposes no PINS table")
    disagreements = []
    for name, digest in sorted(inherited.items()):
        if name not in PINS:
            continue
        if not isinstance(digest, str) or not same_json_type(PINS[name], digest) or \
                PINS[name] != digest:
            disagreements.append(f"{name}: v4 pins {digest!r}, v5 pins {PINS[name]}")
    if disagreements:
        raise AuthorityLoadError("pin tables disagree — " + "; ".join(disagreements))
    unshared = sorted(name for name in inherited if name not in PINS)
    if unshared:
        raise AuthorityLoadError(
            "the predecessor depends on inputs this successor does not record, which "
            f"would break the recording obligation: {unshared}")


# ---------------------------------------------------------------------------
# Section 3.  The derivation.  The effective v5 contract is the VERIFIED v4
# document with a typed, self-verifying operation list applied.  Nothing is
# transcribed; every `set` op restates the byte it replaces and is refused if
# that byte is not what the verified predecessor actually holds -- type-exactly.
# ---------------------------------------------------------------------------

_STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")
DECLARED_OPS = ("set", "add")
DECLARED_PROJECTION_FIELDS = (
    ("version", 4),
    ("supersedes", 3),
    ("checkerModeContract.checker", "check-c2-v4.py"),
)


def _path_steps(path: str):
    return [int(index) if index else name for index, name in _STEP_RE.findall(path)]


def _resolve(root, path: str):
    node = root
    for step in _path_steps(path):
        node = node[step]
    return node


def _assign(root, path: str, value) -> None:
    steps = _path_steps(path)
    node = root
    for step in steps[:-1]:
        node = node[step]
    node[steps[-1]] = value


def _same_wire_value(left, right) -> bool:
    """Type-exact equality at any JSON depth.  Law 18, applied structurally."""
    if not same_json_type(left, right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and \
            all(_same_wire_value(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and \
            all(_same_wire_value(a, b) for a, b in zip(left, right))
    return left == right


def apply_derivation(base, operations):
    """Return (effective, findings).  Every op is checked against the base."""
    effective = copy.deepcopy(base)
    findings = []
    if not isinstance(operations, list) or not operations:
        return effective, ["C2V5-DERIVATION: derivedFrom.operations must be a non-empty "
                           "array; the effective contract is not derivable"]
    for index, op in enumerate(operations):
        if not isinstance(op, dict):
            findings.append(f"C2V5-DERIVATION: operation {index} is not an object")
            continue
        kind, path = op.get("op"), op.get("path")
        if kind not in DECLARED_OPS or not isinstance(path, str) or not path:
            findings.append(f"C2V5-DERIVATION: operation {index} declares op="
                            f"{kind!r} path={path!r}; the declared ops are "
                            f"{list(DECLARED_OPS)}")
            continue
        if "value" not in op:
            findings.append(f"C2V5-DERIVATION: operation {index} at {path} carries no "
                            "value")
            continue
        try:
            if kind == "set":
                current = _resolve(effective, path)
                if not _same_wire_value(current, op.get("from")):
                    findings.append(
                        f"C2V5-DERIVATION: operation {index} at {path} declares it "
                        f"replaces {op.get('from')!r} ({json_type_name(op.get('from'))}) "
                        f"but the verified predecessor holds {current!r} "
                        f"({json_type_name(current)}); the derivation does not describe "
                        "the bytes it is applied to")
                    continue
                _assign(effective, path, copy.deepcopy(op["value"]))
            else:
                steps = _path_steps(path)
                parent = effective
                for step in steps[:-1]:
                    parent = parent[step]
                if steps[-1] in parent:
                    findings.append(f"C2V5-DERIVATION: operation {index} adds {path}, "
                                    "which already exists in the predecessor")
                    continue
                parent[steps[-1]] = copy.deepcopy(op["value"])
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append(f"C2V5-DERIVATION: operation {index} at {path} does not "
                            f"resolve against the verified predecessor "
                            f"({type(exc).__name__})")
    return effective, findings


def project_to_v4_identity(effective, projection):
    """Restore exactly the identity fields the inherited oracle is pinned to.

    The projection is NOT the candidate's to widen.  check-c2-v4.py is pinned to
    a document that says version 4 / supersedes 3 / checker check-c2-v4.py; the
    projection restores those three bytes so the reviewed predecessor can be
    executed as an oracle, and is refused if it touches anything else.
    """
    projected = copy.deepcopy(effective)
    fields = projection.get("fields") if isinstance(projection, dict) else None
    findings = []
    if not isinstance(fields, dict) or not fields:
        return projected, ["C2V5-PROJECTION: v4InheritanceProjection.fields must be a "
                           "non-empty object"]
    if not _same_wire_value(fields, dict(DECLARED_PROJECTION_FIELDS)):
        findings.append(
            f"C2V5-PROJECTION: the declared projection is {fields!r}; this checker "
            f"admits exactly {dict(DECLARED_PROJECTION_FIELDS)!r} and nothing else, "
            "because a projection that carries any other field is a second contract "
            "the inherited oracle would be validating instead of this one")
        return projected, findings
    for path, value in fields.items():
        try:
            _assign(projected, path, copy.deepcopy(value))
        except MALFORMED_SHAPE_EXCEPTIONS as exc:
            findings.append(f"C2V5-PROJECTION: {path} does not resolve "
                            f"({type(exc).__name__})")
    drift = sorted(_wire_diff_paths(effective, projected))
    declared = sorted(fields)
    if drift != declared:
        findings.append(f"C2V5-PROJECTION: the projection handed to the inherited "
                        f"oracle differs from the effective contract at {drift}, but "
                        f"declares only {declared}; a projection that changes anything "
                        "beyond the declared identity fields is a second contract")
    return projected, findings


def _wire_diff_paths(left, right, prefix=""):
    """Every path at which two parsed documents differ, type-exactly."""
    if not same_json_type(left, right):
        return {prefix}
    if isinstance(left, dict):
        out = set()
        for key in set(left) | set(right):
            here = f"{prefix}.{key}" if prefix else str(key)
            if key not in left or key not in right:
                out.add(here)
            else:
                out |= _wire_diff_paths(left[key], right[key], here)
        return out
    if isinstance(left, list):
        out = set()
        if len(left) != len(right):
            return {prefix}
        for index, (a, b) in enumerate(zip(left, right)):
            out |= _wire_diff_paths(a, b, f"{prefix}[{index}]")
        return out
    return set() if left == right else {prefix}


# ---------------------------------------------------------------------------
# Section 4.  L2/L3 -- the repair and the register.
#
# CENSUS_STAT_KEYS is the predecessor's own published stat block.  The position
# set is DERIVED from the live measurement, never hand-listed, so a counter that
# appears in the measurement without appearing in the register is a finding and
# a counter registered without being measured is a finding.  That symmetry is
# what "a fifth site cannot be added silently" has to mean to be true.
# ---------------------------------------------------------------------------

CENSUS_STAT_KEYS = ("executedCases", "unguardedEscapes", "guardedEscapes",
                    "silentAccepts", "admitThenRaise",
                    "typeDistinctConstantAdmissions")


def measure(effective, authority):
    """The measured side, computed by the PINNED predecessor's instrument.

    v5 authors the comparison; v4 -- reviewed, pinned, and confirmed sound at
    the wire surface by the adjudication -- provides the measurement.  Keeping
    those in different bytes is deliberate.
    """
    v4 = authority.v4
    fp = authority.json(FP)
    relations = set(fp["relationRegistry"]["relations"]) if fp else set()
    values = v4._matrix_values(effective.get("planIntentTotalityMatrix", {}))
    intent_values, _ = v4._intent_fixture_values(effective)
    surfaces = v4.measure_surfaces(effective, relations, fp, values, intent_values)
    root_census, _root_stats = v4.measure_contract_root(
        effective, authority.v4_authority, execute=False)
    return {"surfaces": surfaces, "contractRoot": root_census}


def measured_positions(measurement):
    """(position -> measured value), derived from the measurement itself."""
    positions = {}
    for name in sorted(measurement["surfaces"]):
        entry = measurement["surfaces"][name]
        for key in sorted(entry["census"]):
            positions[f"surfaces[{name}].{key}"] = entry["census"][key]
        for key in CENSUS_STAT_KEYS:
            positions[f"surfaces[{name}].{key}"] = entry["stats"][key]
    for key in sorted(measurement["contractRoot"]):
        positions[f"contractRoot.{key}"] = measurement["contractRoot"][key]
    return positions


def published_value(effective, position):
    """Read one published counter out of the candidate.  May be absent."""
    block = effective.get("hostileScalarLeafTotality", {})
    if not isinstance(block, dict):
        return None, False
    if position.startswith("surfaces["):
        name, _, key = position[len("surfaces["):].partition("].")
        rows = block.get("surfaces")
        rows = rows if isinstance(rows, list) else []
        for row in rows:
            if isinstance(row, dict) and same_json_type(row.get("id"), name) and \
                    row.get("id") == name:
                return row.get(key), key in row
        return None, False
    key = position[len("contractRoot."):]
    root = block.get("contractRoot")
    root = root if isinstance(root, dict) else {}
    return root.get(key), key in root


def census_comparison_findings(effective, measurement):
    """L2.  The repair.  Type before content, at both operands, at 48 positions.

    The predecessor wrote `if row.get(key) != value:` three times, where `value`
    was a computed int, and 2538.0 sailed through all three.
    """
    findings = []
    positions = measured_positions(measurement)
    for position in sorted(positions):
        measured_value = positions[position]
        published, present = published_value(effective, position)
        if not present:
            findings.append(f"C2V5-CENSUS: {position} is measured by this run at "
                            f"{measured_value!r} but the candidate publishes no value "
                            "for it")
            continue
        # The SINGLE acceptance path.  Every branch below is a rejection, so
        # weakening the gate cannot be hidden behind a redundant second test --
        # which is what made the predecessor's inline checks look load-bearing.
        if wire_int_equal(published, measured_value):
            continue
        if not is_wire_int(measured_value):
            findings.append(f"C2V5-INSTRUMENT: the value measured at {position} is "
                            f"{measured_value!r}, whose type is "
                            f"{json_type_name(measured_value)} and not a Python "
                            "integer; the COMPUTED side of the comparison is unsound, "
                            "which is the operand IR-C2V4-01 shows nobody was checking")
        elif not is_wire_int(published):
            findings.append(
                f"C2V5-TYPE: {position} is published as {published!r}, whose JSON type "
                f"is {json_type_name(published)}, not the JSON integer this run "
                f"measured ({measured_value}); freeze section 6 law 18 requires the "
                "type to be rejected before the content is compared, and this is the "
                "exact shape of LB-C2-01 and of IR-C2V4-01")
        else:
            findings.append(f"C2V5-CENSUS: {position} is published as {published!r} but "
                            f"this run measured {measured_value}")
    return findings


def register_findings(effective, measurement, authority):
    """L3.  The register must equal the measurement, in both directions."""
    findings = []
    spec = effective.get("planIntent", {})
    spec = spec.get("integerConstantRegisterV5") if isinstance(spec, dict) else None
    if not isinstance(spec, dict):
        findings.append("C2V5-REGISTER: the effective contract declares no "
                        "planIntent.integerConstantRegisterV5; the census counters the "
                        "adjudication names as the fifth site would be unregistered")
        return findings
    raw_inherited = spec.get("inheritedFromV4")
    declared_inherited = set(raw_inherited) if isinstance(raw_inherited, list) else set()
    predecessor_ids = set(
        getattr(authority.v4, "DECLARED_INTEGER_CONSTANT_IDS", frozenset()))
    if sorted(declared_inherited) != sorted(predecessor_ids):
        findings.append(
            f"C2V5-REGISTER: the inherited half of the register is "
            f"{sorted(declared_inherited)} but the executed predecessor declares "
            f"{sorted(predecessor_ids)}; the v4 register may not be narrowed, widened "
            "or restated by this successor")
    raw_added = spec.get("censusCounterPositions")
    declared_added = set(raw_added) if isinstance(raw_added, list) else set()
    measured = set(measured_positions(measurement))
    missing = sorted(measured - declared_added)
    extra = sorted(declared_added - measured)
    if missing:
        findings.append(f"C2V5-REGISTER: {len(missing)} published counter position(s) "
                        f"are measured and compared but are not registered, so a site "
                        f"could be added silently: {missing[:6]}")
    if extra:
        findings.append(f"C2V5-REGISTER: {len(extra)} registered position(s) are not "
                        f"reached by the measurement, so the register overstates what "
                        f"is observed: {extra[:6]}")
    if not int_in_range(spec.get("censusCounterPositionCount"), 1, 10 ** 6) or \
            not wire_int_equal(spec.get("censusCounterPositionCount"), len(measured)):
        findings.append(f"C2V5-REGISTER: the register publishes "
                        f"censusCounterPositionCount="
                        f"{spec.get('censusCounterPositionCount')!r}; this run measured "
                        f"{len(measured)} positions")
    rule = str(spec.get("rule", ""))
    if "type" not in rule or "before" not in rule:
        findings.append("C2V5-REGISTER: the register does not state plainly that the "
                        "JSON type is rejected before the content is compared")
    return findings


# ---------------------------------------------------------------------------
# Section 5.  L4 -- the inverted wire-comparison scan.
#
# The predecessor asked "is the other operand a numeric LITERAL".  A computed
# integer is not a literal, so three live defects were invisible.  v5 asks the
# opposite question: "is this wire operand gated".  Anything not provably
# non-numeric on the far side is treated as numeric.
# ---------------------------------------------------------------------------

_ORDER_OPS = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)
_LITERAL_CONTAINERS = (ast.Tuple, ast.List, ast.Set)
_NON_NUMERIC_CALLS = frozenset({"str", "repr", "sorted", "set", "frozenset", "list",
                                "tuple", "dict", "json_type_name", "type"})
_WIRE_ACCESSORS = frozenset({"get", "pop", "setdefault"})
_WIRE_CALLS = frozenset({"next", "getattr", "iter"})


def _function_universe(tree):
    """Every function-like node at any depth: defs, methods, nested defs, lambdas.

    The declared type gates themselves are excluded.  Scanning the body of
    `is_wire_int` for the absence of a type gate is circular: it IS the gate.
    The exclusion is not free coverage — it is paid for by L7, which breaks each
    gate in turn (bare comparison, wire-side only, boolean-is-an-integer,
    float-is-an-integer) and requires every break to be detected.
    """
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            and getattr(node, "name", "<lambda>") not in GUARD_HELPERS]


def _bound_names(target):
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
    """A value that came off the wire.

    A subscript into a MODULE-LEVEL LITERAL is not wire-sourced -- it is this
    file's own constant table -- and calling it wire would flood the scan with
    noise that would then have to be excused, which is how a scan stops being
    read.  Every other subscript is wire until proven otherwise.
    """
    if isinstance(node, ast.Subscript):
        return not (isinstance(node.value, ast.Name) and node.value.id in literals)
    if isinstance(node, ast.Starred):
        return _is_wire(node.value, tainted, literals)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute) and node.func.attr in _WIRE_ACCESSORS:
            return True
        if isinstance(node.func, ast.Name) and node.func.id in _WIRE_CALLS:
            return True
        return False
    if isinstance(node, ast.Attribute):
        return _is_wire(node.value, tainted, literals)
    return isinstance(node, ast.Name) and node.id in tainted


def _taint_fixpoint(function, literals=frozenset()):
    """Args, kwonly, vararg, kwarg, every assignment form, walrus, unpack,
    for-targets, comprehension targets and with-targets, to a fixpoint."""
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
            elif isinstance(node, ast.NamedExpr) and _is_wire(node.value, tainted, literals):
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


def _module_constants(tree):
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


def _provably_non_numeric(node, constants, depth=0):
    """Conservative: only SHAPES that cannot possibly equal an int are excused.

    Note that a bool constant is NUMERIC here.  `x != True` is exactly the
    LB-C2-01 shape and must never be excused.
    """
    if not int_in_range(depth, 0, _MAX_SCAN_DEPTH) or node is None:
        return False
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or isinstance(node.value, (int, float, complex)):
            return False
        return node.value is None or isinstance(node.value, (str, bytes)) or \
            node.value is Ellipsis
    if isinstance(node, (ast.JoinedStr, ast.FormattedValue, ast.Dict, ast.DictComp)):
        return True
    if isinstance(node, _LITERAL_CONTAINERS):
        return all(_provably_non_numeric(item, constants, depth + 1) for item in node.elts)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
            node.func.id in _NON_NUMERIC_CALLS:
        return True
    if isinstance(node, ast.Name) and node.id in constants:
        return _provably_non_numeric(constants[node.id], constants, depth + 1)
    return False


def _gate_calls(function):
    """Type-gate calls keyed by the unparsed text of their first argument."""
    gates: dict[str, list] = {}
    for node in ast.walk(function):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id not in TYPE_GATES or not node.args:
            continue
        if node.func.id == "isinstance":
            if len(node.args) < 2 or not _isinstance_is_a_gate(node.args[1]):
                continue
        # Keyed on EVERY argument, not only the first: `wire_int_equal(a, b)`
        # and `same_json_type(a, b)` gate both of their operands.
        for argument in node.args:
            gates.setdefault(ast.unparse(argument), []).append(node)
    return gates


def _isinstance_is_a_gate(classinfo) -> bool:
    """isinstance(x, int) is NOT a law-18 gate: True is an int."""
    nodes = classinfo.elts if isinstance(classinfo, _LITERAL_CONTAINERS) else [classinfo]
    named = set()
    for node in nodes:
        if isinstance(node, ast.Name):
            named.add(node.id)
        else:
            return False
    return bool(named) and named <= NON_NUMERIC_CLASSES


def _parent_map(function):
    parents = {}
    for node in ast.walk(function):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    return parents


def _position(node):
    return (getattr(node, "lineno", 0), getattr(node, "col_offset", 0))


def _enclosing_statements(node, parents):
    chain = []
    current = node
    while current is not None:
        if isinstance(current, ast.stmt):
            chain.append(current)
        current = parents.get(current)
    return chain


def _gate_dominates(compare, wire_node, gates, parents):
    """Textual excusal.  Declared as blind spot 1 -- not a dominance proof."""
    candidates = gates.get(ast.unparse(wire_node), [])
    if not candidates:
        return False
    here = _position(compare)
    chain = _enclosing_statements(compare, parents)
    if not chain:
        return False
    innermost = chain[0]
    inside = set(ast.walk(innermost))
    for gate in candidates:
        if gate in inside and _position(gate) <= here:
            return True
    for statement in chain:
        parent = parents.get(statement)
        while parent is not None and not isinstance(parent, (ast.If, ast.While)):
            parent = parents.get(parent)
        if parent is None:
            continue
        test_nodes = set(ast.walk(parent.test))
        if any(gate in test_nodes for gate in candidates):
            return True
    for statement in chain:
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
            test_nodes = set(ast.walk(sibling.test))
            if any(gate in test_nodes for gate in candidates):
                return True
    return False


def wire_comparison_scan(tree, label="subject"):
    """L4.  Inverted: a wire operand in a numeric-capable comparison is a
    finding unless it is gated.  SEES COMPUTED OPERANDS, because it never asks
    whether the far operand is a literal."""
    constants = _module_constants(tree)
    literals = frozenset(
        name for name, node in constants.items()
        if isinstance(node, (ast.Dict, ast.Tuple, ast.List, ast.Set, ast.Constant)))
    universe = _function_universe(tree)
    sites, gate_sites, seen = [], 0, set()
    for function in universe:
        tainted = _taint_fixpoint(function, literals)
        gates = _gate_calls(function)
        parents = _parent_map(function)
        name = getattr(function, "name", "<lambda>")
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                    node.func.id in GUARD_HELPERS:
                gate_sites += 1
            if not isinstance(node, ast.Compare):
                continue
            operands = [node.left] + list(node.comparators)
            for index, operator in enumerate(node.ops):
                left, right = operands[index], operands[index + 1]
                pairs = ()
                if isinstance(operator, _ORDER_OPS):
                    pairs = ((left, right), (right, left))
                elif isinstance(operator, (ast.In, ast.NotIn)):
                    # Narrowed to LITERAL containers on purpose; `key in row` is
                    # not the evasion shape and flagging it would drown the scan.
                    if isinstance(right, _LITERAL_CONTAINERS) or \
                            (isinstance(right, ast.Name) and
                             isinstance(constants.get(right.id), _LITERAL_CONTAINERS)):
                        pairs = ((left, right),)
                for wire_node, other in pairs:
                    if not _is_wire(wire_node, tainted, literals):
                        continue
                    if _provably_non_numeric(other, constants):
                        continue
                    if _gate_dominates(node, wire_node, gates, parents):
                        continue
                    key = (_position(node), ast.unparse(node), ast.unparse(wire_node))
                    if key in seen:
                        continue
                    seen.add(key)
                    sites.append({
                        "function": name,
                        "line": getattr(node, "lineno", 0),
                        "source": ast.unparse(node),
                        "wireOperand": ast.unparse(wire_node),
                        "farOperand": ast.unparse(other),
                        "farOperandNode": type(other).__name__,
                        "farOperandIsComputed": not isinstance(other, ast.Constant),
                    })
    return {
        "label": label,
        "functionLikeNodes": len(universe),
        "gateCallSites": gate_sites,
        "ungatedWireComparisons": len(sites),
        "ungatedComputedOperandComparisons":
            sum(1 for site in sites if site["farOperandIsComputed"]),
        "sites": sorted(sites, key=lambda site: (site["line"], site["source"])),
        "indirectionPrimitives": _indirection_primitives(tree),
    }


def _indirection_primitives(tree):
    """What L4 structurally cannot see.  Measured, published, must be zero here."""
    evals = execs = getattr_dispatch = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                evals += 1
            elif node.func.id == "exec":
                execs += 1
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Call) and \
                isinstance(node.func.func, ast.Name) and node.func.func.id == "getattr":
            getattr_dispatch += 1
    return {"evalCalls": evals, "execCalls": execs,
            "getattrDispatchCalls": getattr_dispatch}


_OWN_SOURCE_CACHE = None


def own_source() -> bytes:
    """Read this file's bytes ONCE.  A checker cannot hash-pin itself; its own
    digest is reported, never verified.  Blind spot 5."""
    global _OWN_SOURCE_CACHE
    if _OWN_SOURCE_CACHE is None:
        _OWN_SOURCE_CACHE = pathlib.Path(__file__).resolve().read_bytes()
    return _OWN_SOURCE_CACHE


def own_tree():
    return ast.parse(own_source())


def scan_findings(authority, self_tree=None):
    """L4 gate over this file, plus the published evidence over the predecessor."""
    findings = []
    tree = own_tree() if self_tree is None else self_tree
    self_scan = wire_comparison_scan(tree, "check-c2-v5.py")
    predecessor_scan = wire_comparison_scan(
        ast.parse(authority.snapshots[V4_CHECKER]), V4_CHECKER)
    authority.scan_self = self_scan
    authority.scan_predecessor = predecessor_scan
    for site in self_scan["sites"]:
        findings.append(
            f"C2V5-SCAN: {site['function']} line {site['line']} compares the "
            f"wire-sourced {site['wireOperand']} against {site['farOperand']}, which is "
            f"not provably non-numeric and is not routed through a declared type gate: "
            f"{site['source']}")
    if not int_in_range(self_scan["gateCallSites"], 8, 10 ** 6):
        findings.append(f"C2V5-SCAN: only {self_scan['gateCallSites']} guard-helper call "
                        "site(s) were seen in this file, so the scan cannot be "
                        "distinguished from a vacuous one")
    # What L4 structurally cannot follow, measured rather than assumed absent.
    # exec() is permitted at EXACTLY the two verified-snapshot loaders and
    # nowhere else; eval() and getattr-dispatch are permitted nowhere.
    primitives = self_scan["indirectionPrimitives"]
    if not wire_int_equal(primitives["evalCalls"], 0):
        findings.append(f"C2V5-SCAN: this file uses {primitives['evalCalls']} eval() "
                        "call(s), which L4 structurally cannot follow")
    if not wire_int_equal(primitives["getattrDispatchCalls"], 0):
        findings.append(f"C2V5-SCAN: this file uses "
                        f"{primitives['getattrDispatchCalls']} getattr() dispatch "
                        "call(s), which L4 structurally cannot follow")
    if not wire_int_equal(primitives["execCalls"], DECLARED_EXEC_SITES):
        findings.append(f"C2V5-SCAN: this file uses {primitives['execCalls']} exec() "
                        f"call(s); exactly {DECLARED_EXEC_SITES} are declared — the "
                        "verified-snapshot module loader and the self-mutation tree "
                        "executor — and any other is an indirection L4 cannot follow")
    # The scan is load-bearing only if it SEES the defect it was written for.
    adjudicated = _adjudicated_census_lines(authority)
    found = {site["line"] for site in predecessor_scan["sites"]}
    unseen = sorted(line for line in adjudicated if line not in found)
    if unseen:
        findings.append(
            f"C2V5-SCAN-BLIND: run over the pinned predecessor this scan does NOT "
            f"report the adjudicated census comparison(s) at line(s) {unseen}; a scan "
            "that cannot see the defect it exists to catch is decorative")
    if not int_in_range(predecessor_scan["ungatedComputedOperandComparisons"], 1, 10 ** 6):
        findings.append("C2V5-SCAN-BLIND: the scan reports no computed-operand "
                        "comparison anywhere in the predecessor, which contradicts the "
                        "measured adjudication and means the computed-operand model is "
                        "inert")
    return findings


def _adjudicated_census_lines(authority):
    """The line numbers the adjudication names, read from the PINNED document."""
    verdict = authority.json(ADJUDICATION) or {}
    sites = verdict.get("reachabilityVerdict", {}).get("theUnguardedSites", [])
    lines = set()
    for site in sites:
        match = re.search(r"line (\d+)", str(site.get("location", "")))
        if match is not None:
            lines.add(int(match.group(1)))
    return lines


# ---------------------------------------------------------------------------
# Section 6.  L5 -- the behavioural layer.  Reads no source at all.
#
# The adjudication's trap, recorded verbatim so the next author cannot miss it:
# its first 48 mutations exited 1 and looked like a clean defence, but the
# rejections came from unrelated self-referential path-census arithmetic while
# the boolean passed the `!=` silently.  A NON-ZERO EXIT IS NOT EVIDENCE YOUR
# GUARD FIRED.  Every assertion below is on a specific finding id AND on the
# finding naming the position under test.
# ---------------------------------------------------------------------------

HOSTILE_SPELLINGS = (
    ("boolean-true", True),
    ("boolean-false", False),
    ("float-equal", None),        # filled per position: float(measured)
    ("float-one", 1.0),
    ("numeric-string", None),     # filled per position: str(measured)
    ("null", None),
    ("array", []),
    ("object", {}),
)
_PER_POSITION_SPELLINGS = frozenset({"float-equal", "numeric-string"})


def _spelling_value(label, declared, measured_value):
    if label == "float-equal":
        return float(measured_value)
    if label == "numeric-string":
        return str(measured_value)
    return copy.deepcopy(declared)


def _set_published(effective, position, value):
    block = effective["hostileScalarLeafTotality"]
    if position.startswith("surfaces["):
        name, _, key = position[len("surfaces["):].partition("].")
        for row in block["surfaces"]:
            if same_json_type(row.get("id"), name) and row.get("id") == name:
                row[key] = value
                return True
        return False
    block["contractRoot"][position[len("contractRoot."):]] = value
    return True


def behavioural_layer(effective, measurement):
    """L5.  Every registered position x every hostile JSON spelling."""
    positions = measured_positions(measurement)
    cases = named = admitted = misnamed = 0
    escapes = []
    for position in sorted(positions):
        measured_value = positions[position]
        for label, declared in HOSTILE_SPELLINGS:
            value = _spelling_value(label, declared, measured_value)
            if label not in _PER_POSITION_SPELLINGS and \
                    _same_wire_value(value, measured_value):
                continue
            mutant = copy.deepcopy(effective)
            if not _set_published(mutant, position, value):
                escapes.append(f"{position}/{label}: the position could not be reached")
                continue
            cases += 1
            findings = census_comparison_findings(mutant, measurement)
            hit = [item for item in findings
                   if item.startswith("C2V5-TYPE:") and position in item]
            if hit:
                named += 1
                continue
            if not findings:
                admitted += 1
                escapes.append(f"{position}/{label}: ADMITTED — {value!r} was accepted "
                               f"where a JSON integer {measured_value} is declared")
                continue
            misnamed += 1
            escapes.append(f"{position}/{label}: rejected, but by "
                           f"{findings[0].split(':')[0]} rather than a C2V5-TYPE "
                           "finding naming the position — a non-zero result that is "
                           "not evidence the type gate fired")
    # The COMPUTED operand is the one nobody was gating.  Corrupt the
    # MEASUREMENT rather than the document and require the instrument-side gate
    # to fire; without this the computed-side half of wire_int_equal would be
    # unfalsifiable on real data, which is exactly the state IR-C2V4-01 found.
    probes = probes_named = probes_escaped = 0
    for position in sorted(positions):
        measured_value = positions[position]
        corrupt = copy.deepcopy(measurement)
        if not _corrupt_measurement(corrupt, position, float(measured_value)):
            continue
        probes += 1
        findings = census_comparison_findings(effective, corrupt)
        if any(item.startswith("C2V5-INSTRUMENT:") and position in item
               for item in findings):
            probes_named += 1
        else:
            probes_escaped += 1
            escapes.append(f"{position}: a float MEASURED value was not refused by the "
                           "computed-side gate")
    return {"positions": len(positions), "spellings": len(HOSTILE_SPELLINGS),
            "executedCases": cases, "namedTypeRejections": named,
            "admissions": admitted, "rejectedWithoutNamingThePosition": misnamed,
            "instrumentProbes": probes, "instrumentProbesNamed": probes_named,
            "instrumentProbesEscaped": probes_escaped,
            "escapes": escapes}


def _corrupt_measurement(measurement, position, value):
    """Write a non-integer into the MEASURED side, to falsify the computed gate."""
    if position.startswith("surfaces["):
        name, _, key = position[len("surfaces["):].partition("].")
        entry = measurement["surfaces"].get(name)
        if entry is None:
            return False
        if key in entry["census"]:
            entry["census"][key] = value
        if key in entry["stats"]:
            entry["stats"][key] = value
        return True
    key = position[len("contractRoot."):]
    if key not in measurement["contractRoot"]:
        return False
    measurement["contractRoot"][key] = value
    return True


def behavioural_findings(effective, measurement, authority):
    result = behavioural_layer(effective, measurement)
    authority.behavioural = result
    findings = []
    if not int_in_range(result["executedCases"], 1, 10 ** 9):
        findings.append("C2V5-BEHAVIOUR: the behavioural layer executed no case at all")
    if not wire_int_equal(result["admissions"], 0):
        findings.append(f"C2V5-BEHAVIOUR: {result['admissions']} type-distinct spelling(s) "
                        "of a published integer counter were ADMITTED by the repaired "
                        "comparator")
    if not wire_int_equal(result["rejectedWithoutNamingThePosition"], 0):
        findings.append(
            f"C2V5-BEHAVIOUR: {result['rejectedWithoutNamingThePosition']} case(s) were "
            "rejected without a C2V5-TYPE finding naming the position; that is the "
            "adjudication's trap, where a non-zero exit came from unrelated arithmetic")
    if not wire_int_equal(result["namedTypeRejections"], result["executedCases"]):
        findings.append(f"C2V5-BEHAVIOUR: {result['namedTypeRejections']} of "
                        f"{result['executedCases']} cases produced a named type finding")
    if not int_in_range(result["instrumentProbes"], 1, 10 ** 9):
        findings.append("C2V5-BEHAVIOUR: the computed-operand gate was never probed, so "
                        "the half of the repair that guards the instrument's own side "
                        "is unfalsified")
    if not wire_int_equal(result["instrumentProbesEscaped"], 0):
        findings.append(f"C2V5-BEHAVIOUR: {result['instrumentProbesEscaped']} float "
                        "MEASURED value(s) were accepted; the computed side of the "
                        "comparison is ungated, which is the operand type "
                        "IR-C2V4-01 names")
    return findings


# ---------------------------------------------------------------------------
# Section 6b.  L2b -- the document-wide type lock.
#
# MEASURED, NOT ASSUMED.  Before writing this layer the whole predecessor
# document was swept: a float substituted at each of its 136 integer leaves,
# each mutant driven through check-c2-v4.py.  57 of the 136 produced exit 0 and
# a FULL GREEN BANNER.  Only 32 of those 57 are census counters.  The other 25
# are contract-declared bounds, ranges, budget maxima and planDescriptor
# mappings that the adjudication's three named sites do not reach at all.
#
# So three sites was NOT the complete set, and a repair scoped to the census
# block would have shipped a class the next reviewer would rediscover.  This
# layer type-locks EVERY integer leaf of the document against the verified
# predecessor, in both directions, which is total over the class rather than
# enumerated over its known members.
# ---------------------------------------------------------------------------

def _integer_leaf_steps(node, steps=()):
    out = []
    if isinstance(node, dict):
        for key, value in node.items():
            out += _integer_leaf_steps(value, steps + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out += _integer_leaf_steps(value, steps + (index,))
    elif is_wire_int(node):
        out.append(steps)
    return out


def _steps_text(steps):
    return "/".join(str(step) for step in steps)


def _resolve_steps(root, steps):
    node = root
    for step in steps:
        node = node[step]
    return node


def _assign_steps(root, steps, value):
    node = root
    for step in steps[:-1]:
        node = node[step]
    node[steps[-1]] = value


def locked_integer_leaves(base, effective):
    """Every path holding a JSON integer in EITHER document.  Both directions,
    so neither a predecessor leaf that the derivation retypes nor a leaf the
    derivation introduces can escape the lock."""
    locked = {tuple(steps) for steps in _integer_leaf_steps(base)}
    locked |= {tuple(steps) for steps in _integer_leaf_steps(effective)}
    return sorted(locked)


def document_type_findings(effective, locked):
    findings = []
    for steps in locked:
        text = _steps_text(steps)
        try:
            value = _resolve_steps(effective, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            findings.append(f"C2V5-TYPE: {text} holds a JSON integer in the verified "
                            "predecessor but does not resolve in the effective "
                            "contract, so the type lock cannot be applied to it")
            continue
        if not is_wire_int(value):
            findings.append(
                f"C2V5-TYPE: {text} is published as {value!r}, whose JSON type is "
                f"{json_type_name(value)}, where a JSON integer is declared; freeze "
                "section 6 law 18 is not confined to the counters the adjudication "
                "named, and a float substituted here drives the pinned predecessor to "
                "a full green run")
    return findings


def document_type_probe(effective, locked):
    """Behavioural, reads no source.  A float at EVERY locked leaf in turn."""
    cases = named = admitted = 0
    escapes = []
    for steps in locked:
        try:
            current = _resolve_steps(effective, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            continue
        if not is_wire_int(current):
            continue
        _assign_steps(effective, steps, float(current))
        try:
            cases += 1
            text = _steps_text(steps)
            findings = document_type_findings(effective, locked)
            if any(item.startswith("C2V5-TYPE:") and text in item for item in findings):
                named += 1
            else:
                admitted += 1
                escapes.append(f"{text}: a float substitution was ADMITTED")
        finally:
            _assign_steps(effective, steps, current)
    return {"lockedLeaves": len(locked), "executedCases": cases,
            "namedTypeRejections": named, "admissions": admitted,
            "escapes": escapes}


def document_type_lock_findings(base, effective, authority):
    locked = locked_integer_leaves(base, effective)
    findings = document_type_findings(effective, locked)
    probe = document_type_probe(effective, locked)
    authority.document_lock = probe
    findings.extend(f"C2V5-DOCLOCK: {item}" for item in probe["escapes"])
    if not int_in_range(probe["executedCases"], 1, 10 ** 9):
        findings.append("C2V5-DOCLOCK: the document-wide type lock probed no position, "
                        "so it is a claim over an unobserved region")
    if not wire_int_equal(probe["admissions"], 0):
        findings.append(f"C2V5-DOCLOCK: {probe['admissions']} float substitution(s) at "
                        "declared integer leaves were admitted")
    if not wire_int_equal(probe["namedTypeRejections"], probe["executedCases"]):
        findings.append(f"C2V5-DOCLOCK: {probe['namedTypeRejections']} of "
                        f"{probe['executedCases']} probes produced a named finding")
    return findings


# ---------------------------------------------------------------------------
# Section 7.  L6 -- the predecessor differential.
#
# The retained false-accept vectors are the adjudication's own, applied to the
# PINNED v4 document at its verified digest.  check-c2-v4.py must still admit
# them; this checker must reject each by name.  Anchoring to external bytes that
# are known to fail is what keeps this layer honest about the repair being live.
# ---------------------------------------------------------------------------

def _v4_measurement(authority):
    v4 = authority.v4
    contract = copy.deepcopy(authority.json(V4_CONTRACT))
    fp = authority.json(FP)
    relations = set(fp["relationRegistry"]["relations"]) if fp else set()
    values = v4._matrix_values(contract.get("planIntentTotalityMatrix", {}))
    intent_values, _ = v4._intent_fixture_values(contract)
    surfaces = v4.measure_surfaces(contract, relations, fp, values, intent_values)
    root_census, _ = v4.measure_contract_root(contract, authority.v4_authority,
                                              execute=False)
    return contract, {"surfaces": surfaces, "contractRoot": root_census}


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


DOCUMENT_DIFFERENTIAL_VECTORS = (
    ("DOC-1-stage-budget-maximum", ("planIntent", "wireTypes", "stageBudgetV1",
                                    "limit", "maximum"),
     "a declared integer bound OUTSIDE the census block; the adjudication's three "
     "named sites do not reach it"),
    ("DOC-2-descriptor-budget-max-entries", ("planIntent", "admissionDescriptorV1",
                                             "budgets", "maxEntries"),
     "a declared collection bound outside the census block"),
    ("DOC-3-integer-constant-register-range", ("planIntent", "integerConstantFields",
                                               "fields", 4, "range", 1),
     "the upper bound of a range inside the predecessor's OWN integer-constant "
     "register: the register that exists so a fifth site cannot be added silently is "
     "itself float-admissible"),
)


def document_differential(authority):
    """The same measurement as L6, at positions that are NOT census counters."""
    v4 = authority.v4
    contract = copy.deepcopy(authority.json(V4_CONTRACT))
    locked = locked_integer_leaves(contract, contract)
    rows, escapes = [], []
    admitted = rejected = 0
    for vector, steps, note in DOCUMENT_DIFFERENTIAL_VECTORS:
        mutant = copy.deepcopy(contract)
        try:
            current = _resolve_steps(mutant, steps)
        except MALFORMED_SHAPE_EXCEPTIONS:
            escapes.append(f"{vector}: {_steps_text(steps)} does not resolve in the "
                           "pinned predecessor document")
            continue
        if not is_wire_int(current):
            escapes.append(f"{vector}: {_steps_text(steps)} is not a JSON integer in "
                           "the pinned predecessor document")
            continue
        _assign_steps(mutant, steps, float(current))
        try:
            v4_findings = v4.check(copy.deepcopy(mutant), authority.v4_authority)
        except BaseException as exc:                    # noqa: BLE001 - measured
            v4_findings = [f"pinned predecessor raised {type(exc).__name__}: {exc}"]
        v5_findings = document_type_findings(mutant, locked)
        text = _steps_text(steps)
        named = [item for item in v5_findings
                 if item.startswith("C2V5-TYPE:") and text in item]
        if not v4_findings:
            admitted += 1
        if named:
            rejected += 1
        else:
            escapes.append(f"{vector}: this checker did NOT name {text}")
        rows.append({"vector": vector, "path": text, "note": note,
                     "predecessorFindingCount": len(v4_findings),
                     "predecessorFullyGreen": not v4_findings,
                     "successorNamedThePosition": bool(named)})
    return {"vectors": len(DOCUMENT_DIFFERENTIAL_VECTORS), "rows": rows,
            "predecessorFullyGreenRuns": admitted,
            "successorRejectedByName": rejected, "escapes": escapes}


def predecessor_differential(authority):
    """L6.  Executed against BOTH checkers, on the pinned predecessor document."""
    v4 = authority.v4
    contract, measurement = _v4_measurement(authority)
    positions = measured_positions(measurement)
    rows, escapes = [], []
    predecessor_admitted = successor_rejected = 0
    for vector, position, spelling, note in DIFFERENTIAL_VECTORS:
        if position not in positions:
            escapes.append(f"{vector}: {position} is not a measured position of the "
                           "pinned predecessor document")
            continue
        declared = dict(HOSTILE_SPELLINGS).get(spelling)
        value = _spelling_value(spelling, declared, positions[position])
        mutant = copy.deepcopy(contract)
        if not _set_published(mutant, position, value):
            escapes.append(f"{vector}: {position} could not be reached")
            continue
        try:
            v4_findings = v4.check(copy.deepcopy(mutant), authority.v4_authority)
        except BaseException as exc:                    # noqa: BLE001 - measured
            v4_findings = [f"pinned predecessor raised {type(exc).__name__}: {exc}"]
        v4_type_findings = [item for item in v4_findings if position in str(item)]
        v5_findings = census_comparison_findings(mutant, measurement)
        v5_named = [item for item in v5_findings
                    if item.startswith("C2V5-TYPE:") and position in item]
        if not v4_type_findings:
            predecessor_admitted += 1
        if v5_named:
            successor_rejected += 1
        else:
            escapes.append(f"{vector}: this checker did NOT reject {position} spelled "
                           f"{spelling} with a C2V5-TYPE finding naming the position")
        rows.append({
            "vector": vector, "position": position, "spelling": spelling,
            "note": note,
            "predecessorFindingCount": len(v4_findings),
            "predecessorNamedThePosition": bool(v4_type_findings),
            "predecessorFullyGreen": not v4_findings,
            "successorNamedThePosition": bool(v5_named),
        })
    return {"vectors": len(DIFFERENTIAL_VECTORS), "rows": rows,
            "predecessorAdmittedThePosition": predecessor_admitted,
            "successorRejectedByName": successor_rejected,
            "escapes": escapes}


def differential_findings(authority):
    result = predecessor_differential(authority)
    document = document_differential(authority)
    result["document"] = document
    authority.differential = result
    findings = [f"C2V5-DIFFERENTIAL: {item}" for item in result["escapes"]]
    findings.extend(f"C2V5-DIFFERENTIAL: {item}" for item in document["escapes"])
    if not wire_int_equal(document["successorRejectedByName"], document["vectors"]):
        findings.append(f"C2V5-DIFFERENTIAL: {document['successorRejectedByName']} of "
                        f"{document['vectors']} NON-CENSUS document vectors were "
                        "rejected by name; the defect class is wider than the three "
                        "census sites and the repair must cover the width")
    if not int_in_range(document["predecessorFullyGreenRuns"], 1, 10 ** 6):
        findings.append("C2V5-DIFFERENTIAL: no non-census document vector drives the "
                        "pinned predecessor to a fully green run, so the measured "
                        "claim that the class is wider than the census block is no "
                        "longer reproduced")
    if not wire_int_equal(result["successorRejectedByName"], result["vectors"]):
        findings.append(f"C2V5-DIFFERENTIAL: {result['successorRejectedByName']} of "
                        f"{result['vectors']} retained false-accept vectors were "
                        "rejected by name")
    if not int_in_range(result["predecessorAdmittedThePosition"], 1, 10 ** 6):
        findings.append(
            "C2V5-DIFFERENTIAL: the pinned predecessor named every vector position, so "
            "the differential is vacuous; either the predecessor's bytes are not the "
            "adjudicated ones or this layer has stopped measuring anything")
    green = [row for row in result["rows"] if row["predecessorFullyGreen"]]
    if not green:
        findings.append(
            "C2V5-DIFFERENTIAL: no retained vector reproduces the adjudication's "
            "headline — a fully green predecessor run over a defective document — so "
            "the repair is no longer demonstrably load-bearing")
    return findings


# ---------------------------------------------------------------------------
# Section 8.  The candidate's own obligations.
# ---------------------------------------------------------------------------

REQUIRED_RESIDUAL_IDS = frozenset({"RES-C2V5-01", "RES-C2V5-02", "RES-C2V5-03",
                                   "RES-C2V5-04", "RES-C2V5-05", "RES-C2V5-06",
                                   "RES-C2V5-07"})
REQUIRED_LAYER_IDS = frozenset({"L0", "L1", "L2", "L2b", "L3", "L4", "L5", "L6", "L7"})


def _identity_findings(c):
    findings = []
    if str(c.get("artifact")) != ARTIFACT_ID:
        findings.append(f"C2V5: candidate is not {ARTIFACT_ID}")
    if not exact_int(c.get("version"), 5) or not exact_int(c.get("supersedes"), 4):
        findings.append("C2V5: candidate must declare version 5 superseding 4 as JSON "
                        "integers; a float or boolean spelling is refused by the same "
                        "rule this successor exists to enforce")
    status = str(c.get("status"))
    if "CANDIDATE-NOT-APPLIED" not in status or "AWAITING-INDEPENDENT-REVIEW" not in status:
        findings.append("C2V5: candidate status must remain CANDIDATE-NOT-APPLIED / "
                        "AWAITING-INDEPENDENT-REVIEW")
    resolves = c.get("resolves")
    resolves = resolves if isinstance(resolves, dict) else {}
    if "IR-C2V4-01" not in resolves:
        findings.append("C2V5: the candidate does not name the adjudicated finding "
                        "IR-C2V4-01 that it exists to repair")
    return findings


def _inventory_findings(c):
    """Every guard has a blind spot.  A total-coverage claim is refused."""
    findings = []
    inventory = c.get("guardInventory")
    inventory = inventory if isinstance(inventory, dict) else {}
    layers = inventory.get("layers")
    layers = layers if isinstance(layers, list) else []
    seen = set()
    for layer in layers:
        if not isinstance(layer, dict):
            continue
        seen.add(layer.get("id"))
        spots = layer.get("blindSpots")
        if not isinstance(spots, list) or not spots:
            findings.append(f"C2V5-INVENTORY: layer {layer.get('id')!r} publishes no "
                            "blind spot; a guard inventory claiming total coverage is "
                            "refused")
    if seen != REQUIRED_LAYER_IDS:
        findings.append(f"C2V5-INVENTORY: the guard inventory declares layers "
                        f"{sorted(x for x in seen if x is not None)}, not the "
                        f"{sorted(REQUIRED_LAYER_IDS)} this checker carries")
    behind = str(inventory.get("whatStandsBehindTheBackstop", ""))
    if len(behind) < 80:
        findings.append("C2V5-INVENTORY: the inventory does not state what stands "
                        "behind the behavioural backstop, which is the structural "
                        "question the adjudication graded BLOCKING")
    terminal = str(inventory.get("terminalLayerAndWhatStandsBehindIt", ""))
    if "nothing" not in terminal.lower():
        findings.append("C2V5-INVENTORY: the inventory does not state plainly that the "
                        "terminal layer has nothing behind it but independent review")
    return findings


def _residual_findings(c):
    findings = []
    residuals = c.get("residuals")
    residuals = residuals if isinstance(residuals, list) else []
    ids = {item.get("id") for item in residuals if isinstance(item, dict)}
    if not REQUIRED_RESIDUAL_IDS <= ids:
        findings.append(f"C2V5-RESIDUAL: the candidate does not retain "
                        f"{sorted(REQUIRED_RESIDUAL_IDS - ids)}; a residual that is "
                        "absorbed rather than retained is the corpus's dominant failure "
                        "mode")
    for item in residuals:
        if not isinstance(item, dict):
            continue
        if str(item.get("status")) not in ("RETAINED", "RETAINED-OPEN"):
            findings.append(f"C2V5-RESIDUAL: {item.get('id')!r} is not RETAINED")
        if len(str(item.get("whyNotClosed", ""))) < 40:
            findings.append(f"C2V5-RESIDUAL: {item.get('id')!r} does not say why it is "
                            "not closed")
    return findings


def _recording_findings(c):
    """Freeze 7.2: filename AND digest for every input.  A count is not a record."""
    findings = []
    recorded = c.get("recordedInputs")
    recorded = recorded if isinstance(recorded, list) else []
    table = {}
    for item in recorded:
        if isinstance(item, dict) and isinstance(item.get("filename"), str):
            table[item["filename"]] = item.get("sha256")
    missing = sorted(name for name in PINS if name not in table)
    if missing:
        findings.append(f"C2V5-RECORD: {len(missing)} pinned input(s) are executed or "
                        f"parsed by this checker but carry no record: {missing}")
    wrong = []
    for name in sorted(PINS):
        if name not in table:
            continue
        if not isinstance(table[name], str) or \
                not same_json_type(table[name], PINS[name]) or \
                table[name] != PINS[name]:
            wrong.append(f"{name}: recorded {table[name]!r}, verified {PINS[name]}")
    if wrong:
        findings.append(f"C2V5-RECORD: recorded digest does not match the digest this "
                        f"run verified — {wrong}")
    for item in recorded:
        if not isinstance(item, dict) or len(str(item.get("role", ""))) >= 12:
            continue
        findings.append(f"C2V5-RECORD: {item.get('filename')!r} is recorded without a "
                        "role, so the record does not say what it is depended on for")
    return findings


def _mode_findings(c):
    findings = []
    mode = c.get("checkerModeContract")
    mode = mode if isinstance(mode, dict) else {}
    codes = mode.get("exitCodes")
    codes = codes if isinstance(codes, dict) else {}
    if str(mode.get("checker")) != "check-c2-v5.py" or \
            set(codes) != DECLARED_EXIT_CODES or \
            "REFUSED" not in str(codes.get("3")):
        findings.append("C2V5: the checker mode contract does not declare exactly exit "
                        "codes 0/1/2/3 with 3 reserved for the dirty-base selftest "
                        "refusal")
    return findings


def _repro_findings(c, authority):
    """The minimal repro must be RECORDED, and recorded as what it is."""
    findings = []
    defect = c.get("theDefect")
    defect = defect if isinstance(defect, dict) else {}
    repro = defect.get("minimalReproduction")
    repro = repro if isinstance(repro, dict) else {}
    if str(repro.get("sourceModification")) != "NONE":
        findings.append("C2V5-REPRO: the minimal reproduction is not recorded as "
                        "requiring no source modification, which is the whole reason "
                        "IR-C2V4-01 is BLOCKING rather than advisory")
    if str(repro.get("predecessorSha256")) != PINS[V4_CHECKER]:
        findings.append(f"C2V5-REPRO: the reproduction is recorded against "
                        f"{repro.get('predecessorSha256')!r}, not the verified "
                        f"predecessor digest {PINS[V4_CHECKER]}")
    if not exact_int(repro.get("predecessorExitCode"), 0):
        findings.append("C2V5-REPRO: the reproduction does not record that the "
                        "predecessor exited 0 over the defective document")
    sweep = defect.get("wholeDocumentSweep")
    sweep = sweep if isinstance(sweep, dict) else {}
    if not int_in_range(sweep.get("integerLeavesInjected"), 1, 10 ** 6) or \
            not int_in_range(sweep.get("admittedByPredecessorToAFullGreenRun"),
                             1, 10 ** 6) or \
            not int_in_range(sweep.get("ofWhichOutsideTheCensusBlock"), 1, 10 ** 6):
        findings.append("C2V5-REPRO: the candidate does not record a measured "
                        "whole-document sweep, so its claim that three sites is the "
                        "complete set would be an assumption")
    if str(sweep.get("reproducedPerRun")) != "SAMPLED":
        findings.append("C2V5-REPRO: the whole-document sweep must be recorded as "
                        "SAMPLED per run, not as if the checker reproduced all of it "
                        "on every invocation")
    sites = defect.get("repairedComparisonSites")
    sites = sites if isinstance(sites, list) else []
    lines = {item.get("line") for item in sites if isinstance(item, dict)}
    adjudicated = _adjudicated_census_lines(authority)
    if not adjudicated <= lines:
        findings.append(f"C2V5-REPRO: the candidate enumerates comparison sites "
                        f"{sorted(x for x in lines if x is not None)} but the pinned "
                        f"adjudication names {sorted(adjudicated)}")
    if not int_in_range(defect.get("enumeratedComparisonSiteCount"), 1, 10 ** 6) or \
            not wire_int_equal(defect.get("enumeratedComparisonSiteCount"), len(sites)):
        findings.append(f"C2V5-REPRO: enumeratedComparisonSiteCount is published as "
                        f"{defect.get('enumeratedComparisonSiteCount')!r}; the candidate "
                        f"enumerates {len(sites)} site(s)")
    return findings


def _measured_block_findings(c, authority):
    """v5's own published counters, under v5's own law-18 comparator."""
    findings = []
    published = c.get("v5MeasuredCounters")
    published = published if isinstance(published, dict) else {}
    live = {
        "registeredCensusPositions": len(measured_positions(authority.measurement)),
        "behaviouralExecutedCases": authority.behavioural["executedCases"],
        "behaviouralNamedTypeRejections": authority.behavioural["namedTypeRejections"],
        "behaviouralAdmissions": authority.behavioural["admissions"],
        "behaviouralInstrumentProbes": authority.behavioural["instrumentProbes"],
        "behaviouralInstrumentProbesNamed":
            authority.behavioural["instrumentProbesNamed"],
        "scanSelfUngatedWireComparisons": authority.scan_self["ungatedWireComparisons"],
        "scanSelfFunctionLikeNodes": authority.scan_self["functionLikeNodes"],
        "scanPredecessorUngatedWireComparisons":
            authority.scan_predecessor["ungatedWireComparisons"],
        "scanPredecessorUngatedComputedOperandComparisons":
            authority.scan_predecessor["ungatedComputedOperandComparisons"],
        "scanPredecessorFunctionLikeNodes":
            authority.scan_predecessor["functionLikeNodes"],
        "differentialVectors": authority.differential["vectors"],
        "differentialPredecessorAdmitted":
            authority.differential["predecessorAdmittedThePosition"],
        "differentialSuccessorRejectedByName":
            authority.differential["successorRejectedByName"],
        "documentIntegerLeavesTypeLocked": authority.document_lock["lockedLeaves"],
        "documentTypeProbeCases": authority.document_lock["executedCases"],
        "documentTypeProbeNamedRejections":
            authority.document_lock["namedTypeRejections"],
        "documentTypeProbeAdmissions": authority.document_lock["admissions"],
        "documentDifferentialVectors": authority.differential["document"]["vectors"],
        "documentDifferentialPredecessorFullyGreen":
            authority.differential["document"]["predecessorFullyGreenRuns"],
        "documentDifferentialSuccessorRejectedByName":
            authority.differential["document"]["successorRejectedByName"],
    }
    for key in sorted(live):
        measured_value = live[key]
        if key not in published:
            findings.append(f"C2V5-CENSUS: v5MeasuredCounters.{key} is measured at "
                            f"{measured_value} but is not published")
            continue
        value = published[key]
        if not is_wire_int(value):
            findings.append(
                f"C2V5-TYPE: v5MeasuredCounters.{key} is published as {value!r}, whose "
                f"JSON type is {json_type_name(value)}, not the JSON integer this run "
                f"measured ({measured_value}); this checker's own published counters are "
                "held to law 18 exactly as the predecessor's are")
            continue
        if not wire_int_equal(value, measured_value):
            findings.append(f"C2V5-CENSUS: v5MeasuredCounters.{key} is published as "
                            f"{value!r} but this run measured {measured_value}")
    unknown = sorted(set(published) - set(live))
    if unknown:
        findings.append(f"C2V5-REGISTER: v5MeasuredCounters publishes {unknown}, which "
                        "this run does not measure; an unmeasured published counter is "
                        "a coverage claim over an unobservable region")
    return findings


# ---------------------------------------------------------------------------
# Section 9.  The total contract boundary.
# ---------------------------------------------------------------------------

def check(c, authority, self_tree=None):
    """Total boundary: malformed parsed JSON becomes a named finding."""
    if not isinstance(c, dict) or not c:
        return ["C2V5-TOTALITY-ROOT: contract root must be a non-empty object"]
    try:
        return _check(c, authority, self_tree)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"C2V5-TOTALITY: the candidate could not be traversed "
                f"({type(exc).__name__}: {exc})"]


def _check(c, authority, self_tree=None):
    findings = []
    findings.extend(_identity_findings(c))

    derived = c.get("derivedFrom")
    derived = derived if isinstance(derived, dict) else {}
    if str(derived.get("artifact")) != V4_CONTRACT or \
            str(derived.get("sha256")) != PINS[V4_CONTRACT]:
        return findings + [
            f"C2V5-DERIVATION: the candidate must derive from {V4_CONTRACT} at "
            f"{PINS[V4_CONTRACT]}; it names {derived.get('artifact')!r} at "
            f"{derived.get('sha256')!r}, so no effective contract can be materialised"]

    base = copy.deepcopy(authority.json(V4_CONTRACT))
    effective, derivation_findings = apply_derivation(base, derived.get("operations"))
    findings.extend(derivation_findings)
    authority.effective = effective

    projection, projection_findings = project_to_v4_identity(
        effective, c.get("v4InheritanceProjection"))
    findings.extend(projection_findings)

    # ---- L1 inherited: the reviewed predecessor over the projection --------
    try:
        inherited = authority.v4.check(copy.deepcopy(projection), authority.v4_authority)
    except BaseException as exc:                        # noqa: BLE001 - reported
        inherited = [f"the pinned predecessor raised {type(exc).__name__}: {exc}"]
    findings.extend(f"C2V5-INHERITED: {item}" for item in inherited)

    # ---- the measurement, then L2/L3 --------------------------------------
    measurement = measure(effective, authority)
    authority.measurement = measurement
    findings.extend(census_comparison_findings(effective, measurement))
    findings.extend(register_findings(effective, measurement, authority))
    findings.extend(document_type_lock_findings(base, effective, authority))

    # ---- L4, L5, L6 --------------------------------------------------------
    findings.extend(scan_findings(authority, self_tree))
    findings.extend(behavioural_findings(effective, measurement, authority))
    findings.extend(differential_findings(authority))

    # ---- the candidate's own obligations ----------------------------------
    findings.extend(_repro_findings(c, authority))
    findings.extend(_inventory_findings(c))
    findings.extend(_residual_findings(c))
    findings.extend(_recording_findings(c))
    findings.extend(_mode_findings(c))
    findings.extend(_measured_block_findings(c, authority))
    return findings


# ---------------------------------------------------------------------------
# Section 10.  L7 -- self-mutation.  Break each layer, require detection.
#
# Nothing stands behind this layer.  It is terminal by construction and every
# row is printed so that a reviewer, not this file, is the thing behind it.
# ---------------------------------------------------------------------------

def _replace_body(tree, name, source):
    subject = copy.deepcopy(tree)
    replacement = ast.parse(source).body
    for node in ast.walk(subject):
        if isinstance(node, ast.FunctionDef) and isinstance(name, str) and \
                node.name == name:
            node.body = replacement
            return ast.fix_missing_locations(subject)
    raise AuthorityLoadError(f"cannot find {name} to mutate")


def _s_bare_census_comparison(tree):
    """Restore the predecessor's defect verbatim: no type gate at all."""
    return _replace_body(tree, "wire_int_equal", "return published == measured")


def _s_gate_only_the_wire_side(tree):
    """The half-repair: gate the published side, trust the computed side."""
    return _replace_body(tree, "wire_int_equal", "return is_wire_int(published) and "
                                                 "published == measured")


def _s_boolean_is_an_integer(tree):
    """LB-C2-01 at the root: let a JSON boolean count as a JSON integer."""
    return _replace_body(tree, "is_wire_int", "return isinstance(value, int)")


def _s_float_is_an_integer(tree):
    return _replace_body(tree, "is_wire_int",
                         "return isinstance(value, (int, float)) and "
                         "not isinstance(value, bool)")


def _s_narrow_the_numeric_model(tree):
    """The exact narrowing that made IR-C2V4-01 invisible: literals only."""
    return _replace_body(tree, "_provably_non_numeric",
                         "return not isinstance(node, ast.Constant)")


def _s_hand_list_the_positions(tree):
    """Derive the position set from the contract instead of the measurement."""
    return _replace_body(tree, "measured_positions", "return {}")


def _s_disable_the_behavioural_layer(tree):
    return _replace_body(tree, "behavioural_layer",
                         "return {'positions': 0, 'spellings': 0, 'executedCases': 0, "
                         "'namedTypeRejections': 0, 'admissions': 0, "
                         "'rejectedWithoutNamingThePosition': 0, 'instrumentProbes': 0, "
                         "'instrumentProbesNamed': 0, 'instrumentProbesEscaped': 0, "
                         "'escapes': []}")


# Each row declares the finding id that MUST fire.  Asserting on `findings != []`
# is what the adjudication warns against: its first 48 mutations exited 1 on
# unrelated arithmetic while the defect passed silently.  Two rows of this very
# suite did exactly that before this column existed.
def _s_confine_the_lock_to_the_census(tree):
    """Scope the repair to the three adjudicated sites, as the required-repair
    text alone would have allowed.  The 25 non-census positions reopen."""
    return _replace_body(tree, "locked_integer_leaves", "return []")


SOURCE_MUTATIONS = [
    ("restore the predecessor's ungated census comparison", _s_bare_census_comparison,
     "C2V5-BEHAVIOUR"),
    ("gate only the wire operand and trust the computed one",
     _s_gate_only_the_wire_side, "C2V5-BEHAVIOUR"),
    ("let a JSON boolean count as a JSON integer (LB-C2-01)", _s_boolean_is_an_integer,
     "C2V5-BEHAVIOUR"),
    ("let a JSON float count as a JSON integer (LB-C2-01)", _s_float_is_an_integer,
     "C2V5-BEHAVIOUR"),
    ("narrow the numeric model back to ast.Constant (IR-C2V4-01's root cause)",
     _s_narrow_the_numeric_model, "C2V5-SCAN-BLIND"),
    ("stop deriving the register from the live measurement", _s_hand_list_the_positions,
     "C2V5-REGISTER"),
    ("disable the behavioural layer", _s_disable_the_behavioural_layer,
     "C2V5-BEHAVIOUR"),
    ("confine the repair to the census block and reopen the other 25 positions",
     _s_confine_the_lock_to_the_census, "C2V5-DOCLOCK"),
]


def _s_inject_computed_operand_comparison(tree):
    """A wire value against a COMPUTED int — the shape the predecessor missed."""
    subject = copy.deepcopy(tree)
    injected = ast.parse(
        "for _k, _v in measurement['contractRoot'].items():\n"
        "    if effective.get(_k) != _v:\n"
        "        pass\n").body
    for node in subject.body:
        if isinstance(node, ast.FunctionDef) and node.name == "census_comparison_findings":
            node.body = injected + node.body
            return ast.fix_missing_locations(subject)
    raise AuthorityLoadError("cannot find census_comparison_findings to mutate")


def _s_inject_named_constant_comparison(tree):
    """A wire value against a module-level named integer, not a literal."""
    subject = copy.deepcopy(tree)
    injected = ast.parse(
        "_LAW18_PROBE = 1\n"
        "def _c2v5_named_constant_probe(row):\n"
        "    if row.get('schemaVersion') != _LAW18_PROBE:\n"
        "        return ['probe']\n"
        "    return []\n").body
    subject.body.extend(injected)
    return ast.fix_missing_locations(subject)


def _s_inject_membership_comparison(tree):
    """`not in (1,)` — the membership evasion the predecessor's scan skipped."""
    subject = copy.deepcopy(tree)
    injected = ast.parse(
        "def _c2v5_membership_probe(row):\n"
        "    if row.get('schemaVersion') not in (1,):\n"
        "        return ['probe']\n"
        "    return []\n").body
    subject.body.extend(injected)
    return ast.fix_missing_locations(subject)


SCAN_MUTATIONS = [
    ("inject a wire value compared against a COMPUTED integer",
     _s_inject_computed_operand_comparison),
    ("inject a wire value compared against a module-level named integer",
     _s_inject_named_constant_comparison),
    ("inject a wire value tested for membership in a numeric literal container",
     _s_inject_membership_comparison),
]


def _m_unregister_a_census_position(c):
    register = c["derivedFrom"]["operations"]
    for op in register:
        if op.get("path") == "planIntent.integerConstantRegisterV5":
            op["value"]["censusCounterPositions"].pop()
            return
    raise AuthorityLoadError("cannot find the register operation to mutate")


def _m_overstate_the_register(c):
    for op in c["derivedFrom"]["operations"]:
        if op.get("path") == "planIntent.integerConstantRegisterV5":
            op["value"]["censusCounterPositions"].append("surfaces[imaginary].nothing")
            return
    raise AuthorityLoadError("cannot find the register operation to mutate")


def _census_counter_op(c, key):
    for op in c["derivedFrom"]["operations"]:
        if op.get("path") == f"hostileScalarLeafTotality.contractRoot.{key}":
            return op
    raise AuthorityLoadError(f"cannot find the contractRoot.{key} operation")


def _m_float_census_counter(c):
    op = _census_counter_op(c, "scalarLeafPaths")
    op["value"] = float(op["value"])


def _m_boolean_census_counter(c):
    op = _census_counter_op(c, "pathsNotRoundTripping")
    op["value"] = False


def _m_string_census_counter(c):
    op = _census_counter_op(c, "enumeratedPaths")
    op["value"] = str(op["value"])


def _m_drift_census_counter(c):
    op = _census_counter_op(c, "executedCases")
    op["value"] = op["value"] + 1


def _m_widen_the_projection(c):
    c["v4InheritanceProjection"]["fields"]["planIntent.integerConstantRegisterV5"] = None


def _m_misdescribe_the_derivation(c):
    for op in c["derivedFrom"]["operations"]:
        if op.get("op") == "set" and "from" in op:
            op["from"] = "a byte the predecessor does not hold"
            return
    raise AuthorityLoadError("cannot find a set operation to mutate")


def _m_claim_total_coverage(c):
    for layer in c["guardInventory"]["layers"]:
        layer["blindSpots"] = []


def _m_absorb_a_residual(c):
    c["residuals"] = [item for item in c["residuals"] if item.get("id") != "RES-C2V5-03"]


def _m_drop_an_input_record(c):
    c["recordedInputs"] = [item for item in c["recordedInputs"]
                           if item.get("filename") != V4_CHECKER]


def _m_understate_a_v5_counter(c):
    c["v5MeasuredCounters"]["behaviouralExecutedCases"] = 1


def _m_float_a_v5_counter(c):
    c["v5MeasuredCounters"]["registeredCensusPositions"] = \
        float(c["v5MeasuredCounters"]["registeredCensusPositions"])


def _m_soften_the_repro(c):
    c["theDefect"]["minimalReproduction"]["sourceModification"] = "a small patch"


CONTRACT_MUTATIONS = [
    ("unregister one census counter position", _m_unregister_a_census_position,
     "C2V5-REGISTER"),
    ("register a position the measurement does not reach", _m_overstate_the_register,
     "C2V5-REGISTER"),
    ("spell a census counter as a JSON float (the minimal repro)",
     _m_float_census_counter, "C2V5-TYPE"),
    ("spell a census counter as a JSON boolean", _m_boolean_census_counter, "C2V5-TYPE"),
    ("spell a census counter as a JSON string", _m_string_census_counter, "C2V5-TYPE"),
    ("drift a census counter by one", _m_drift_census_counter, "C2V5-CENSUS"),
    ("widen the inherited-oracle projection beyond the identity fields",
     _m_widen_the_projection, "C2V5-PROJECTION"),
    ("misdescribe the bytes the derivation is applied to", _m_misdescribe_the_derivation,
     "C2V5-DERIVATION"),
    ("claim total guard coverage", _m_claim_total_coverage, "C2V5-INVENTORY"),
    ("absorb a retained residual", _m_absorb_a_residual, "C2V5-RESIDUAL"),
    ("drop the record of an executed input", _m_drop_an_input_record, "C2V5-RECORD"),
    ("understate one of this checker's own published counters",
     _m_understate_a_v5_counter, "C2V5-CENSUS"),
    ("spell one of this checker's own published counters as a float",
     _m_float_a_v5_counter, "C2V5-TYPE"),
    ("soften the recorded minimal reproduction", _m_soften_the_repro, "C2V5-REPRO"),
]


def _execute_tree(tree):
    module = types.ModuleType("opensip_c2v5_mutated")
    module.__file__ = str(pathlib.Path(__file__).resolve())
    exec(compile(tree, module.__file__, "exec"), module.__dict__)
    return module


def selftest(candidate, authority, path):
    """Always reaches the suite; refuses a dirty base with a distinct code."""
    base_findings = check(candidate, authority)
    if base_findings:
        print("SELFTEST-REFUSED: the base candidate is not clean, so the mutation suite "
              "is not an oracle over it — every row would echo the pre-existing failure "
              "and report 'all rejected'.")
        print(f"  dirty base: {len(base_findings)} finding(s) in {path.name}")
        for finding in base_findings[:10]:
            print("  base-finding:", finding)
        if len(base_findings) > 10:
            print(f"  ... {len(base_findings) - 10} further base finding(s)")
        total = len(CONTRACT_MUTATIONS) + len(SOURCE_MUTATIONS) + len(SCAN_MUTATIONS)
        print(f"SELFTEST-NOT-RUN: 0 of {total} mutations executed. Exit 3 distinguishes "
              "this refusal from a green selftest (0), from ordinary findings (1) and "
              "from a bad invocation (2), and can never be absorbed into a pass.")
        return 3
    # Captured from the CLEAN base before any mutation runs: every later
    # check() call overwrites the live measurement with a mutated one.
    clean_behaviour = authority.behavioural
    clean_differential = authority.differential
    print(f"C-2 v5 mutation self-test over {path.name} — each row must be REJECTED BY "
          "THE NAMED FINDING, not merely rejected\n")
    escaped, rows = [], 0

    def report(ok, name, detail):
        nonlocal rows
        rows += 1
        print(f"  {'reject' if ok else 'ESCAPE':>6}  {name}")
        print(f"          {detail}")

    for name, root in (("string", "hostile-root"), ("null", None), ("list", []),
                       ("empty-object", {})):
        findings = check(copy.deepcopy(root), authority)
        named = bool(findings) and str(findings[0]).startswith("C2V5-TOTALITY-ROOT:")
        if not named:
            escaped.append(f"parsed-JSON root {name}: no named C2V5-TOTALITY-ROOT finding")
        report(named, f"parsed-JSON contract root {name}",
               findings[0] if findings else "NO FINDING — root survived")

    # ---- contract mutations, asserted on the FINDING ID -------------------
    for name, mutate, expected in CONTRACT_MUTATIONS:
        mutant = copy.deepcopy(candidate)
        try:
            mutate(mutant)
        except Exception as exc:                        # noqa: BLE001 - reported
            escaped.append(f"{name}: mutation could not be applied ({type(exc).__name__})")
            report(False, name, f"mutation could not be applied ({type(exc).__name__})")
            continue
        findings = check(mutant, authority)
        hit = [item for item in findings if item.startswith(expected + ":")]
        if not hit:
            escaped.append(f"{name}: {len(findings)} finding(s) but none is {expected} — "
                           "a non-zero result is not evidence the guard fired")
        report(bool(hit), name,
               hit[0] if hit else (f"{len(findings)} unrelated finding(s); first: "
                                   f"{findings[0]}" if findings else "NO FINDING"))

    # ---- source mutations of this file's own tree -------------------------
    tree = own_tree()
    for name, mutate, expected in SOURCE_MUTATIONS:
        try:
            module = _execute_tree(mutate(tree))
            findings = module.check(copy.deepcopy(candidate), authority, tree)
        except Exception as exc:                        # noqa: BLE001 - reported
            findings = [f"mutated checker raised {type(exc).__name__}: {exc}"]
        hit = [item for item in findings if item.startswith(expected + ":")]
        if not hit:
            escaped.append(
                f"{name}: {len(findings)} finding(s) but none is {expected} — the break "
                "was not detected BY THE LAYER IT BREAKS, and a rejection from "
                "somewhere else is not evidence that layer is load-bearing")
        report(bool(hit), name,
               hit[0] if hit else (f"{len(findings)} unrelated finding(s); first: "
                                   f"{findings[0]}" if findings else "NO FINDING"))

    # ---- scan mutations: the shapes the predecessor's scan could not see ---
    clean = wire_comparison_scan(tree, "clean")["ungatedWireComparisons"]
    for name, mutate in SCAN_MUTATIONS:
        try:
            broken = wire_comparison_scan(mutate(tree), "broken")["ungatedWireComparisons"]
        except Exception as exc:                        # noqa: BLE001 - reported
            broken = f"scan raised {type(exc).__name__}: {exc}"
        detected = is_wire_int(broken) and is_wire_int(clean) and broken > clean
        if not detected:
            escaped.append(f"{name}: the scan reported {broken!r} on the broken tree and "
                           f"{clean!r} on the clean tree")
        report(detected, name,
               f"scan reports {broken} ungated site(s) against {clean} on the "
               "unmutated tree")

    # ---- the retained false-accept vectors, end to end --------------------
    for row in clean_differential["rows"]:
        ok = row["successorNamedThePosition"] and not row["predecessorNamedThePosition"]
        if not ok:
            escaped.append(f"{row['vector']}: differential lost")
        report(ok, f"retained false accept {row['vector']} at {row['position']} "
                   f"spelled {row['spelling']}",
               f"pinned check-c2-v4.py produced {row['predecessorFindingCount']} "
               f"finding(s) and named the position: "
               f"{row['predecessorNamedThePosition']}"
               f"{' (FULLY GREEN)' if row['predecessorFullyGreen'] else ''}; "
               f"this checker named it: {row['successorNamedThePosition']}")

    for row in clean_differential["document"]["rows"]:
        ok = row["successorNamedThePosition"] and row["predecessorFullyGreen"]
        if not ok:
            escaped.append(f"{row['vector']}: non-census differential lost")
        report(ok, f"retained NON-CENSUS false accept {row['vector']} at "
                   f"{row['path']} spelled float",
               f"pinned check-c2-v4.py produced {row['predecessorFindingCount']} "
               f"finding(s)"
               f"{' (FULLY GREEN)' if row['predecessorFullyGreen'] else ''}; "
               f"this checker named it: {row['successorNamedThePosition']}")

    print()
    if escaped:
        for item in escaped:
            print("SELFTEST-FAIL:", item)
        print(f"{len(escaped)}/{rows} retained cases ESCAPED — the proof path is optional")
        return 1
    print(f"SELFTEST-PASS: all {rows} retained cases rejected by their named finding — "
          "the proof path is load-bearing")
    behaviour = clean_behaviour
    print(f"  behavioural layer (reads no source): {behaviour['executedCases']} cases "
          f"over {behaviour['positions']} registered positions x "
          f"{behaviour['spellings']} hostile JSON spellings; "
          f"{behaviour['namedTypeRejections']} named type rejections, "
          f"{behaviour['admissions']} admissions")
    print(f"  L7 is terminal: nothing stands behind this suite but independent review, "
          f"and every one of its {rows} rows is printed above so a reviewer can be that "
          "thing")
    return 0


# ---------------------------------------------------------------------------
# Section 11.  Entry.
# ---------------------------------------------------------------------------

def _parse_argv(argv):
    flags, positional = set(), []
    for arg in argv[1:]:
        if arg in DECLARED_FLAGS:
            flags.add(arg)
        elif isinstance(arg, str) and arg.startswith("-"):
            raise UnsupportedInvocation(f"unknown flag {arg!r}; declared flags are "
                                        f"{list(DECLARED_FLAGS)}")
        else:
            positional.append(arg)
    if len(positional) > 1:
        raise UnsupportedInvocation("at most one contract path may be supplied")
    return flags, (positional[0] if positional else None)


def main(argv):
    try:
        flags, requested = _parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"C2V5-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    try:
        authority = load_authority()
    except AuthorityLoadError as exc:
        print(f"C2V5-PINNED-INPUT-REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        candidate = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"cannot load C-2 v5 candidate {path}: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in flags:
        return selftest(candidate, authority, path)
    findings = check(candidate, authority)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for item in findings:
            print("  -", item)
        return 1
    behaviour = authority.behavioural
    differential = authority.differential
    self_scan = authority.scan_self
    predecessor_scan = authority.scan_predecessor
    positions = len(measured_positions(authority.measurement))
    green = sum(1 for row in differential["rows"] if row["predecessorFullyGreen"])
    print(f"C-2 v5 contract OK — {path.name}; IR-C2V4-01 repaired at the census "
          f"comparison, {len(PINS)} inputs hash-verified before execution, and the "
          f"pinned {V4_CHECKER} executed from its verified snapshot as the inherited "
          "oracle over the v4-identity projection")
    print(f"  L2/L3 law 18: {positions} published counter positions compared with BOTH "
          f"operands type-gated and all {positions} registered; 0 type-distinct "
          "admissions, 0 drifts")
    lock = authority.document_lock
    document = differential["document"]
    print(f"  L2b document-wide type lock: {lock['lockedLeaves']} integer leaves locked "
          f"against the verified predecessor and float-probed live; "
          f"{lock['namedTypeRejections']} named, {lock['admissions']} admitted. Three "
          "sites was NOT the complete set — an authoring-time sweep of all 136 integer "
          "leaves of the predecessor document found 57 that drive it to a full green "
          f"run, only 32 of them census counters; {document['vectors']} non-census "
          f"vectors are re-measured every run and "
          f"{document['predecessorFullyGreenRuns']} still run the predecessor green")
    print(f"  L4 inverted scan: {self_scan['ungatedWireComparisons']} ungated wire "
          f"comparison(s) in this file over {self_scan['functionLikeNodes']} "
          f"function-like nodes; over the pinned predecessor it reports "
          f"{predecessor_scan['ungatedWireComparisons']} ungated site(s) of which "
          f"{predecessor_scan['ungatedComputedOperandComparisons']} have a COMPUTED far "
          "operand — the class the predecessor's ast.Constant model could not see")
    print(f"  L5 behavioural (reads no source): {behaviour['executedCases']} cases over "
          f"{behaviour['positions']} positions x {behaviour['spellings']} hostile JSON "
          f"spellings; {behaviour['namedTypeRejections']} rejected by a C2V5-TYPE "
          f"finding naming the position, {behaviour['admissions']} admitted")
    print(f"  L6 differential: {differential['vectors']} retained false-accept vectors; "
          f"the pinned predecessor admitted {differential['predecessorAdmittedThePosition']} "
          f"of them ({green} to a fully green run) and this checker rejected "
          f"{differential['successorRejectedByName']} by name")
    print(f"  own bytes reported not verified (a checker cannot pin itself): sha256:"
          f"{hashlib.sha256(own_source()).hexdigest()}")
    print("  scope: checker-scope evidence only; SPECIFIED / IMPLEMENTABLE_UNEXECUTED; "
          "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW; independent re-review "
          "REQUIRED; no seal, freeze, integration or product acceptance is declared; "
          "CD-RT-5 remains BLOCKED_ON_PHASE_1A")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
