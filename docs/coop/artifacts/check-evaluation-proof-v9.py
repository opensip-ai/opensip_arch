#!/usr/bin/env python3
"""Executable design-integrity checker for Evaluation Proof v9.

WHY v9 EXISTS — two structural reasons, neither of them a new proof obligation.
-----------------------------------------------------------------------------
EP9 moves NO proof identity.  Every vector, every ProjectId/PlanIntent/SnapshotId/
PlanId, every raw receipt byte, every RawCasRef, every semantic ref, every derived
requirement and every policy verdict is byte-value identical to EP8.  What changes
is WHICH C-2 BYTES the authority join is verified against, and HOW MUCH of the
delegation closure is inside the pinned, hash-verified, measured window.

REASON 1 — an inherited, propagating defect (LB-C2-01).
    check-c2.py (4f31d57c…) guarded both commitment-bearing schemaVersion fields
    with a bare inequality against the integer 1.  In the host language
    ``True == 1`` and ``1.0 == 1``, so validate_plan_intent ADMITTED a wire
    PlanIntent spelling schemaVersion as JSON true and the encoder then committed
    it to a SECOND digest; a PlanIntent spelling it as JSON 1.0 was likewise
    ADMITTED and then raised an unguarded ValueError inside the encoder.

    check-evaluation-proof-v6.py pins check-c2.py at exactly those bytes and calls
    validate_plan_intent → plan_intent_commitment → canonical_plan_intent at lines
    359-364 of its admit_evaluation_authority.  EP7 loads EP6; EP8 loads EP7.  The
    defect was therefore inherited by the whole evaluation-proof chain.

    This is not a paper inheritance.  Executed on the frozen bytes, a hostile
    PlanIntent spelling schemaVersion as JSON true is ADMITTED end to end by
    check-evaluation-proof-v8.py's own public authorize_evaluation, and EP8 mints
    a complete AdmittedEvaluationAuthorityV1 whose PlanAuthorityReceiptV1 carries
    the SECOND commitment sha256:5d748405… in place of the true
    sha256:7c3174f6….  C-2 v4 rejects that same PlanIntent with C2I-02.  The
    battery that establishes this runs on every invocation of this checker; see
    ``lb_c2_01_battery`` and the ``EP9-NEG-*`` matrix.

    C-2 v4 repairs it and has PASSED independent review with 0 blocking findings.
    v9 re-pins the C-2 join onto the repaired bytes.

REASON 2 — EP8's reviewed window stopped short of its own dependency chain.
    ep8-rt13.review-independent-cold-reconstruction.json names
    check-evaluation-proof-v7.py.  It names check-evaluation-proof-v6.py zero
    times, check-c2.py zero times and c2-plan-stage-schema.v3.json zero times.
    There are no standalone v6 or v7 reviews.  Neither v8 nor v7 mentions
    check-c2 or validate_plan_intent anywhere in its source.  EP8's PASS never
    reached the hop carrying the defect.  v9 brings the whole ten-member
    delegation closure inside one pinned, hash-verified, executed-from-snapshot
    window and records every digest as data, per IMPLEMENTATION-FREEZE §7.2.

WHAT v9 DOES *NOT* CLAIM — read this before reading the green banner.
    v9 does NOT repair check-evaluation-proof-v6.py.  Editing it is out of scope
    and it is pinned by passed work.  EP6's INNER C-2 join still executes against
    the defective v3 bytes underneath EP8.  v9 is a strictly stronger OUTER gate,
    not a replacement of EP6's internals: v9 independently re-validates every
    PlanIntent in the closure through C-2 v4 and REFUSES anything v4 rejects, so
    nothing EP6 would silently admit can survive a v9 run.  The residual is named
    RES-EP9-01 in the candidate and is not absorbed into this banner.

    RES-EP9-05, found by this instrument and MEASURED rather than repaired: the
    LB-C2-01 CLASS is not confined to C-2.  Driving hostile parsed JSON at every
    scalar leaf of the accepted EvaluationAuthorityCandidateV1 shows that EP8's
    own public authorize_evaluation ADMITS a candidate spelling schemaVersion as
    JSON true or JSON 1.0 at four sites — the candidate root,
    planAuthorityReceipt, activationManifest and evaluationAuthoritySeal —
    because those exact-closed-record guards are bare inequalities against the
    integer 1.  On the frozen bytes this moves NO proof identity: every RawCasRef,
    the EvaluationAuthoritySealRef and the admission ref are derived from the
    stored raw CAS bytes rather than from the in-memory record, and every one was
    verified unchanged.  It is nonetheless a false accept of a type-distinct value
    against an exact closed record.  v9 cannot repair it without editing pinned
    predecessors, so it ENUMERATES the exact admitted set and makes any change to
    that set a finding.

    The same class appeared in THIS file's own first draft — `version != 9`
    admits JSON 9.0, and `repairAuthorisedByBlockingFindingCount != 0` admits
    JSON false — and was swept out with exact-type guards, an AST tripwire, a
    declared integer register, and a behavioural battery that injects at every
    integer and boolean scalar leaf and re-runs the whole checking layer.  Two of
    those four devices exist because the battery found sites the scan did not.

THE STANDING REQUIREMENT (IMPLEMENTATION-FREEZE §7).
    Six surfaces in this corpus have shipped a coverage or totality claim that
    quantified over a region their own instrument could not observe — one of them
    is C-2's 4x4 matrix, pinned never to reach a scalar leaf, which is exactly
    where LB-C2-01 lived.  This checker therefore enumerates EVERY position of
    every measured surface — the root, every object key and every array index at
    unlimited depth, CONTAINER AND SCALAR LEAF ALIKE — injects at each, and
    publishes the LIVE MEASURED counts, recomputed and compared on every run.
    check-evidence-v10.py is the reference for the measurement discipline;
    check-c2-v4.py is the reference for combining an AST scan with an independent
    non-AST behavioural census.

    The AST scan here is a TRIPWIRE, not the guard.  EV10-IR-01 and IR-C2V4-01
    both showed this scan class is evadable by module alias, local alias,
    getattr(sys.modules[__name__], …), dispatch table, inner function,
    comprehension, walrus, tuple-unpack and class method.  This checker MEASURES
    that evasion rather than asserting immunity: it builds all nine variants,
    reports how many its own syntactic scan misses, and requires the independent
    behavioural layer — which executes the real join and is indifferent to how a
    call is spelled — to catch every one.  See ``astScanScope`` in the candidate.

Usage: python3 -I -B artifacts/check-evaluation-proof-v9.py [artifact] [--selftest]
Exit:  0 clean or green selftest · 1 findings · 2 unsupported invocation or a
       pinned input that does not hash to its declared digest · 3 --selftest
       REFUSED over a dirty base, which can never be absorbed into a pass.

Scope: checker-scope evidence only.  SPECIFIED / IMPLEMENTABLE_UNEXECUTED.
CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW.  DO-NOT-SEAL.  CD-RT-5
unsigned.  A green run is authored by the same lane that authored the candidate
and is not review, qualification, demonstration, seal, freeze, integration or
product acceptance.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import sys
import types
from contextlib import redirect_stdout

BINDING = "evaluation-proof.v9.json"
DECLARED_FLAGS = ("--selftest",)
HERE = pathlib.Path(__file__).resolve().parent
EXPECTED_VERSION = 9

# --------------------------------------------------------------------------
# Section 0.  The pinned window.
#
# TEN executables form the delegation closure.  Each is read once, verified
# against the digest below, and EXECUTED FROM THAT VERIFIED BYTE STRING via
# _VerifiedSourceLoader — never re-read from disk between verification and
# execution.  The digests below were recomputed on the live bytes by this lane.
# --------------------------------------------------------------------------

EP8 = "check-evaluation-proof-v8.py"
EP7 = "check-evaluation-proof-v7.py"
EP6 = "check-evaluation-proof-v6.py"
EP5 = "check-evaluation-proof.py"
C2V4 = "check-c2-v4.py"
EVIDENCE = "check-evidence.py"
RETENTION = "check-retention-custody.py"
D9 = "check-d9.py"
VERSIONING = "check-versioning.py"
RESOLVED = "check-resolved-inputs.py"

DELEGATION_CLOSURE: dict[str, str] = {
    EP8: "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    EP7: "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4",
    EP6: "0a7ac122a598bb7b9454b1b3c46c586f6fd551a2a1ebcf5584665f875457c5f0",
    EP5: "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    C2V4: "54ff764d155f5582bc66fd7bf8138b7eaed5f90f46b92975c4bc7a85ffb3df17",
    EVIDENCE: "6933d2931912a43e3018dc6037068230af0bbc0c0a00d5d9429c155930bde1af",
    RETENTION: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    D9: "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    VERSIONING: "67a45b275908afc4bd04cee6c15400f5d429f9f209854630c1caf5a43cf13227",
    RESOLVED: "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
}

# The SUPERSEDED encoder.  check-c2.py is not a member of the delegation closure
# — v9 takes no authority from it — but it is pinned and executed as an
# INDEPENDENT ENCODER so that the seven commitments must reproduce under the
# instrument generation that PRECEDED the repair as well as under the repaired
# one.  A repair that moved a commitment cannot pass quietly.
C2V3_CHECKER = "check-c2.py"
C2V3_CHECKER_SHA = "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3"

C2V4_CONTRACT = "c2-plan-stage-schema.v4.json"
C2V3_CONTRACT = "c2-plan-stage-schema.v3.json"
C2V4_REVIEW = "c2-plan-stage-schema.v4.review-independent-prefreeze.json"
EP8_ARTIFACT = "evaluation-proof.v8.json"
EP8_REVIEW = "ep8-rt13.review-independent-cold-reconstruction.json"
FACT_PLANE = "fact-plane.v1.json"

# Data pinned by digest.  Nothing here is executed.  Everything read by this
# checker, and everything the closure members read from disk beneath it, is
# recorded — a count is not a record and a prose assertion is not a record.
PINNED_DATA: dict[str, str] = {
    EP8_ARTIFACT: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    "evaluation-proof.v7.json":
        "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
    "evaluation-proof.v6.json":
        "74f35668afae2efb57070ff9a2897d373a91b42cc1cbbc87f3c673f872ca4bce",
    "evaluation-proof.v5.json":
        "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    C2V4_CONTRACT:
        "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    C2V3_CONTRACT:
        "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    C2V4_REVIEW:
        "c74612ef4519750aa529db543c2f0cc81fce50d57c3d636486fd2f0ddc0c41f3",
    EP8_REVIEW:
        "f4599b32a9f1b93049111b9e86debd19419902c9c5f4fb886f8d0dc9c330567e",
    FACT_PLANE:
        "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "resolved-inputs.v2.json":
        "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "versioning-policy.v4.json":
        "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6",
}

# The three C-2 APIs the evaluation-proof authority join imports.  v9 verifies
# them against the REPAIRED bytes: present, callable, correct arity, and
# behaviourally load-bearing under the LB-C2-01 battery.
C2_IMPORTED_APIS = ("canonical_plan_intent", "plan_intent_commitment",
                    "validate_plan_intent")

# The verdict the C-2 v4 review must actually carry for the re-pin to be
# authorised.  A lane that quietly points at a softened review is refused at
# load rather than reported as a finding.
C2V4_REVIEW_BINDING = {"verdict": "PASS", "blockingFindingCount": 0}

MALFORMED = (AttributeError, IndexError, KeyError, StopIteration, TypeError,
             ValueError, ZeroDivisionError, OverflowError, RecursionError,
             UnicodeError)

EP8_COMMITMENT = "sha256:7c3174f6358f40a36f19b97eab6b247086f7a5411141fb9ee056535904fa7a85"


# --------------------------------------------------------------------------
# The LB-C2-01 guard helpers, applied to THIS checker.
#
# The leaf-inclusive instrument below found the LB-C2-01 class in this file's own
# first draft — `contract.get("version") != 9` admits JSON 9.0, and
# `repairAuthorisedByBlockingFindingCount != 0` admits JSON false.  A checker
# that exists to re-pin away from that defect may not carry it.  Every
# wire-sourced numeric test in this file therefore routes through these helpers,
# `integer_guard_scan` reports any that does not, and
# `own_constant_leaf_battery` measures the property behaviourally without
# reading source at all.
# --------------------------------------------------------------------------

INT64_MAX = 2 ** 63 - 1


def is_wire_int(value) -> bool:
    """True only for a JSON integer.  A JSON boolean is NOT a JSON integer."""
    return isinstance(value, int) and not isinstance(value, bool)


def exact_int(value, constant) -> bool:
    """Exact-type integer constant guard.  Rejects true, false, 1.0 and "1"."""
    return is_wire_int(value) and value == constant


def int_in_range(value, low, high) -> bool:
    """Exact-type integer range guard."""
    return is_wire_int(value) and low <= value <= high


def exact_int_list(value, expected) -> bool:
    """Element-wise exact-type integer list guard."""
    return isinstance(value, list) and len(value) == len(expected) and \
        all(exact_int(item, want) for item, want in zip(value, expected))


class AuthorityLoadError(RuntimeError):
    """A pinned input could not be admitted as authority."""


class PinMismatch(AuthorityLoadError):
    """A pinned byte string does not hash to its declared digest."""


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this checker does not accept."""


class DuplicateKeyError(ValueError):
    """A JSON object carried the same key twice."""


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


class _VerifiedSourceLoader:
    """Execute exactly the bytes that were hash-verified, never a re-read."""

    def __init__(self, filename, source):
        self.filename = filename
        self.source = source

    def create_module(self, _spec):
        return None

    def exec_module(self, module):
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_snapshot(name, filename, source):
    path = (HERE / filename).resolve()
    loader = _VerifiedSourceLoader(path, source)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    if spec is None or spec.loader is None:
        raise AuthorityLoadError(f"cannot construct verified spec for {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Authority:
    """Everything admitted after hash verification, and nothing else."""

    def __init__(self, snapshots, parsed, modules):
        self.snapshots = snapshots
        self.parsed = parsed
        self.modules = modules
        # Non-AST liveness instrumentation.  Every C-2 call this checker makes
        # goes through .c2v4(); the counter is compared against the number of
        # join invocations, so a join rewired to any other module by any
        # spelling whatsoever leaves the counter behind and is reported.
        self.c2v4_accesses = 0
        self.census = None
        self.measurement = None
        # Two pure-function caches.  The own-constant-leaf battery re-runs the
        # FULL checking layer once per injected leaf, so anything that provably
        # does not depend on the injected leaf is computed once.
        #   predecessor_cache: EP8 validation and closure pin agreement depend on
        #     the pinned bytes alone and on no part of the candidate.
        #   vector_cache: the surface matrices, commitment recomputation, the
        #     LB-C2-01 battery, its control and the evasion battery depend only
        #     on positiveVectors and acceptedAuthorityVectorId, and are
        #     recomputed the moment either changes.
        self.predecessor_cache = None
        self.vector_cache = None
        # The leaf-inclusive census layer IS the instrument.  It runs in full on
        # every ordinary invocation.  While the contract-root hostile matrix is
        # driving check() over tens of thousands of mutated copies of the whole
        # document, re-running the instrument inside every case would multiply
        # the cost by two orders of magnitude, so it is disabled for exactly
        # that window and the candidate declares this in scalarLeafTotality.
        self.deep_enabled = True

    def json(self, name):
        return self.parsed.get(name)

    def module(self, name):
        return self.modules.get(name)

    def c2v4(self):
        """The sole admitted route to the repaired C-2 instrument."""
        self.c2v4_accesses += 1
        return self.modules[C2V4]

    def c2v3(self):
        """The superseded encoder, admitted only as an independent cross-check."""
        return self.modules[C2V3_CHECKER]


def load_authority(directory: pathlib.Path = HERE) -> Authority:
    """Hash-before-execution over every pinned transitive input."""
    snapshots: dict[str, bytes] = {}
    errors: list[str] = []
    wanted = dict(DELEGATION_CLOSURE)
    wanted[C2V3_CHECKER] = C2V3_CHECKER_SHA
    wanted.update(PINNED_DATA)
    for name, expected in wanted.items():
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
    for name in wanted:
        if name.endswith(".json"):
            try:
                parsed[name] = json.loads(snapshots[name].decode("utf-8"),
                                          object_pairs_hook=_pairs)
            except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
                raise AuthorityLoadError(
                    f"cannot parse pinned data {name}: {type(exc).__name__}") from exc

    review = parsed.get(C2V4_REVIEW)
    if not isinstance(review, dict):
        raise AuthorityLoadError(f"pinned review {C2V4_REVIEW} is not an object")
    statement = review.get("verdictStatement")
    statement = statement if isinstance(statement, dict) else {}
    if review.get("verdict") != C2V4_REVIEW_BINDING["verdict"] or \
            statement.get("verdict") != C2V4_REVIEW_BINDING["verdict"]:
        raise AuthorityLoadError(
            f"pinned review {C2V4_REVIEW} does not carry verdict "
            f"{C2V4_REVIEW_BINDING['verdict']!r}; the C-2 v4 re-pin is not authorised")
    if review.get("blockingFindingCount") != C2V4_REVIEW_BINDING["blockingFindingCount"] or \
            statement.get("blockingFindingCount") != C2V4_REVIEW_BINDING["blockingFindingCount"]:
        raise AuthorityLoadError(
            f"pinned review {C2V4_REVIEW} does not carry 0 blocking findings; "
            "the C-2 v4 re-pin is not authorised")

    modules: dict[str, types.ModuleType] = {}
    sink = io.StringIO()
    with redirect_stdout(sink):
        for name in DELEGATION_CLOSURE:
            modules[name] = _execute_snapshot(
                "opensip_ep9_closure_" + name.replace("-", "_").replace(".", "_"),
                name, snapshots[name])
        modules[C2V3_CHECKER] = _execute_snapshot(
            "opensip_ep9_superseded_c2v3", C2V3_CHECKER, snapshots[C2V3_CHECKER])
    return Authority(snapshots, parsed, modules)


def closure_pin_agreement(authority) -> list[str]:
    """Every predecessor's own declared pins must agree with v9's, digit for digit.

    This is what makes the window closed rather than assumed.  v9 executes the
    ten from verified snapshots, but EP8/EP7/EP6 additionally load their own
    copies from disk.  Reading their PINNED tables back out of the executed
    module objects proves those internal loads bind the same bytes v9 verified.
    """
    findings: list[str] = []
    known = dict(DELEGATION_CLOSURE)
    known[C2V3_CHECKER] = C2V3_CHECKER_SHA
    known.update(PINNED_DATA)
    for holder, attribute in ((EP8, "PINNED"), (EP7, "PINNED"), (EP6, "PINNED"),
                              (C2V4, "PINS")):
        module = authority.module(holder)
        table = getattr(module, attribute, None)
        if not isinstance(table, dict) or not table:
            findings.append(f"EP9-CLOSURE: {holder} exposes no {attribute} table, so its "
                            "internal loads cannot be shown to bind the verified bytes")
            continue
        for name, digest in table.items():
            if name in known and known[name] != digest:
                findings.append(
                    f"EP9-CLOSURE: {holder}.{attribute} pins {name} at {digest} but v9 "
                    f"verified {known[name]}; the closure is not one window")
    return findings


# --------------------------------------------------------------------------
# Section 1.  The C-2 v4 authority join.  v9 is the authority for this join.
#
# Every C-2 call in this checker routes through these three functions and they
# route through Authority.c2v4().  Nothing else reaches a C-2 API.
# --------------------------------------------------------------------------

def c2_validate_intent(intent, authority):
    """Total.  Returns a findings list; never raises for parsed JSON."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        return list(authority.c2v4().validate_plan_intent(intent, contract, set(relations)))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", f"C-2 v4 validation boundary: "
                                 f"{type(exc).__name__}: {exc}")]


def c2_commit_intent(intent, authority):
    """Total.  Returns (commitment-or-None, findings); never raises."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().plan_intent_commitment(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "PlanIntent admitted by validation cannot be "
                                 f"canonically encoded: {type(exc).__name__}: {exc}")]


def c2_canonical_intent(intent, authority):
    """Total.  Returns (preimage-bytes-or-None, findings); never raises."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().canonical_plan_intent(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "PlanIntent cannot be canonically encoded: "
                                 f"{type(exc).__name__}: {exc}")]


def c2_join(intent, authority):
    """The complete v9 authority join over one PlanIntent.

    Order is load-bearing and matches the seam EP6 exposes at its lines 359-364:
    validate first, and only then commit.  v9 differs from EP6 in exactly one
    respect — the instrument is the REPAIRED one, and the encoder is reached
    through a total boundary so an admitted-then-unencodable PlanIntent is a
    named finding rather than a traceback out of the authority layer.
    """
    findings = list(c2_validate_intent(intent, authority))
    if findings:
        return None, findings
    commitment, encode_errors = c2_commit_intent(intent, authority)
    if encode_errors:
        return None, encode_errors
    preimage, canonical_errors = c2_canonical_intent(intent, authority)
    if canonical_errors:
        return None, canonical_errors
    if not preimage:
        return None, [("C2I-04", "repaired C-2 canonical PlanIntent unexpectedly empty")]
    return commitment, []


def c2_api_surface(authority) -> list[str]:
    """The three imported APIs, verified against the repaired bytes."""
    findings: list[str] = []
    module = authority.c2v4()
    for name in C2_IMPORTED_APIS:
        function = getattr(module, name, None)
        if function is None or not callable(function):
            findings.append(f"EP9-C2-API: {C2V4} does not expose a callable {name}; the "
                            "evaluation-proof authority join cannot be re-pinned onto it")
            continue
        try:
            arity = function.__code__.co_argcount
        except AttributeError:
            findings.append(f"EP9-C2-API: {name} in {C2V4} is not a plain function")
            continue
        expected = 3 if name == "validate_plan_intent" else 2
        if arity != expected:
            findings.append(f"EP9-C2-API: {C2V4}.{name} takes {arity} positional "
                            f"parameters; the imported seam requires {expected}")
    return findings


# --------------------------------------------------------------------------
# Section 2.  The LB-C2-01 battery — the load-bearing, non-AST guard.
#
# Four hostile spellings at each commitment-bearing scalar leaf.  Under the
# DEFECTIVE v3 instrument every one is admitted; under the REPAIRED v4
# instrument every one must be rejected.  This battery is indifferent to how any
# call is spelled, so it survives every evasion class that defeats an AST scan.
# --------------------------------------------------------------------------

# The two leaves LB-C2-01 named, plus the third the C-2 v4 sweep found.
COMMITMENT_BEARING_LEAVES = (
    ("schemaVersion",
     ("schemaVersion",)),
    ("analysis.admissionDescriptor.schemaVersion",
     ("analysis", "admissionDescriptor", "schemaVersion")),
)
# Values that are `== 1` in the host language but are NOT the JSON integer 1.
TYPE_DISTINCT_ONES = (
    ("json-true", True),
    ("json-float-one", 1.0),
    ("json-text-one", "1"),
    ("json-false-at-zero-site", False),
)


def _set_path(value, path, injected):
    node = value
    for part in path[:-1]:
        node = node[part]
    node[path[-1]] = injected


def lb_c2_01_battery(intents, authority):
    """Execute the LB-C2-01 class against the live v9 join.

    Returns measured statistics.  ``admitted`` MUST be zero: a non-zero value
    means the join is reaching an instrument that still carries the defect,
    however that instrument came to be reached.
    """
    stats = {"cases": 0, "admitted": 0, "rejected": 0, "secondDigests": 0,
             "admitThenRaise": 0, "escapes": 0, "admissions": []}
    for intent in intents:
        truth, truth_findings = c2_join(intent, authority)
        if truth_findings or truth is None:
            stats["escapes"] += 1
            continue
        for site, path in COMMITMENT_BEARING_LEAVES:
            for label, injected in TYPE_DISTINCT_ONES:
                hostile = copy.deepcopy(intent)
                try:
                    _set_path(hostile, path, injected)
                except MALFORMED:
                    continue
                stats["cases"] += 1
                try:
                    findings = c2_validate_intent(hostile, authority)
                except BaseException:                      # noqa: BLE001 measured
                    stats["escapes"] += 1
                    continue
                if findings:
                    stats["rejected"] += 1
                    continue
                stats["admitted"] += 1
                stats["admissions"].append(f"{site}={label}")
                commitment, encode_errors = c2_commit_intent(hostile, authority)
                if encode_errors:
                    stats["admitThenRaise"] += 1
                elif commitment != truth:
                    stats["secondDigests"] += 1
    return stats


def expected_control_admissions(intents):
    """How many cases the DEFECT admits, derived from the tables, not asserted.

    LB-C2-01 is a bare ``!= 1``.  It therefore admits exactly those injected
    values that are ``== 1`` in the host language — JSON true and JSON 1.0 — and
    rejects the two that are not, at each commitment-bearing leaf.  Deriving the
    expected count this way makes the positive control falsifiable: if the
    superseded instrument stopped admitting them the battery would be vacuous and
    the repair unfalsifiable, and that is reported rather than absorbed.
    """
    admitting = sum(1 for _label, value in TYPE_DISTINCT_ONES
                    if not isinstance(value, str) and value == 1)
    return admitting * len(COMMITMENT_BEARING_LEAVES) * len(intents)


def lb_c2_01_control(intents, authority):
    """The positive control: the SUPERSEDED instrument must still fail this.

    A battery that no instrument fails proves nothing.  This runs the identical
    cases against the pinned v3 encoder and requires it to admit — if it did not,
    the battery would be vacuous and the repair unfalsifiable.
    """
    v3 = authority.c2v3()
    contract = authority.json(C2V3_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    stats = {"cases": 0, "admitted": 0, "secondDigests": 0, "admitThenRaise": 0}
    for intent in intents:
        try:
            truth = v3.plan_intent_commitment(intent, contract)
        except MALFORMED:
            continue
        for _site, path in COMMITMENT_BEARING_LEAVES:
            for _label, injected in TYPE_DISTINCT_ONES:
                hostile = copy.deepcopy(intent)
                try:
                    _set_path(hostile, path, injected)
                except MALFORMED:
                    continue
                stats["cases"] += 1
                try:
                    findings = v3.validate_plan_intent(hostile, contract, relations)
                except BaseException:                      # noqa: BLE001 measured
                    continue
                if findings:
                    continue
                stats["admitted"] += 1
                try:
                    if v3.plan_intent_commitment(hostile, contract) != truth:
                        stats["secondDigests"] += 1
                except BaseException:                      # noqa: BLE001 measured
                    stats["admitThenRaise"] += 1
    return stats


# --------------------------------------------------------------------------
# Section 3.  Commitment stability.  Recomputed, never copied.
# --------------------------------------------------------------------------

def commitment_stability(contract, authority):
    """Recompute every planIntentCommitment through C-2 v4 and cross-check.

    The declared literal is never trusted.  For each vector the commitment is
    recomputed under the REPAIRED instrument, recomputed again under the
    SUPERSEDED instrument as an independent encoder, and compared against the
    value EP8 committed.  Preimages are compared as BYTES, not merely digests,
    so a collision cannot explain agreement.
    """
    ep8 = authority.json(EP8_ARTIFACT)
    v3 = authority.c2v3()
    v3_contract = authority.json(C2V3_CONTRACT)
    result = {"vectors": 0, "recomputedUnderV4": 0, "reproducedUnderV3": 0,
              "preimageByteIdentical": 0, "distinctCommitments": [],
              "preimageByteLengths": [], "moved": [], "findings": []}
    vectors = contract.get("positiveVectors")
    ep8_vectors = ep8.get("positiveVectors") if isinstance(ep8, dict) else None
    if not isinstance(vectors, list) or not isinstance(ep8_vectors, list) or \
            len(vectors) != len(ep8_vectors):
        result["findings"].append(
            "EP9-STABILITY: the v9 vector list is not the EP8 vector list, so no "
            "commitment can be shown unmoved")
        return result
    for index, vector in enumerate(vectors):
        ident = vector.get("id") if isinstance(vector, dict) else f"[{index}]"
        try:
            candidate = vector["evaluationAuthorityCandidate"]
            intent = candidate["admittedResolvedInputs"]["frozenPlanIntent"]
            declared = candidate["planAuthorityReceipt"]["planIntentCommitment"]
            committed_by_ep8 = ep8_vectors[index]["evaluationAuthorityCandidate"][
                "planAuthorityReceipt"]["planIntentCommitment"]
        except MALFORMED as exc:
            result["findings"].append(
                f"EP9-STABILITY: {ident}: vector shape is not readable: "
                f"{type(exc).__name__}: {exc}")
            continue
        result["vectors"] += 1
        recomputed, join_findings = c2_join(intent, authority)
        if join_findings:
            result["findings"].append(
                f"EP9-STABILITY: {ident}: the repaired C-2 instrument rejects a "
                f"committed PlanIntent: {join_findings[0]}")
            continue
        result["recomputedUnderV4"] += 1
        if recomputed != declared or recomputed != committed_by_ep8:
            result["moved"].append(
                f"{ident}: EP8 committed {committed_by_ep8!r}, v9 declares {declared!r}, "
                f"recomputation under C-2 v4 produced {recomputed!r}")
            continue
        if recomputed not in result["distinctCommitments"]:
            result["distinctCommitments"].append(recomputed)
        preimage, canonical_findings = c2_canonical_intent(intent, authority)
        if canonical_findings or preimage is None:
            result["findings"].append(
                f"EP9-STABILITY: {ident}: repaired canonical encoder produced no preimage")
            continue
        if len(preimage) not in result["preimageByteLengths"]:
            result["preimageByteLengths"].append(len(preimage))
        try:
            independent = v3.plan_intent_commitment(intent, v3_contract)
            independent_preimage = v3.canonical_plan_intent(intent, v3_contract)
        except BaseException as exc:                       # noqa: BLE001 reported
            result["moved"].append(
                f"{ident}: the superseded independent encoder raised "
                f"{type(exc).__name__}: {exc}")
            continue
        if independent != committed_by_ep8:
            result["moved"].append(
                f"{ident}: EP8 committed {committed_by_ep8!r}; the superseded "
                f"independent encoder produced {independent!r}")
            continue
        result["reproducedUnderV3"] += 1
        if independent_preimage == preimage:
            result["preimageByteIdentical"] += 1
        else:
            result["moved"].append(
                f"{ident}: the two encoders agree on the digest but their preimages "
                "differ byte for byte")
    result["preimageByteLengths"].sort()
    return result


# --------------------------------------------------------------------------
# Section 4.  Measured scalar-leaf totality.
#
# Enumerate EVERY position — the root, every object key, every array index, at
# unlimited depth, container AND scalar leaf alike — inject at each, and publish
# the live measured counts.  Understating the space is a finding, not an
# omission.  Recomputed on every run and compared with the declared counts.
# --------------------------------------------------------------------------

HOSTILE_VALUES = (
    ("null", None), ("integer", 0), ("negative", -1), ("float", 1.5),
    ("true", True), ("false", False), ("empty-text", ""), ("text", "x"),
    ("empty-array", []), ("empty-object", {}), ("nested-array", [[]]),
    ("nested-object", [{"unknown": 1}]),
    # The type-distinct-one family.  This is the family that falsified C-2 v3's
    # own published totality claim, and it lives only at scalar leaves.
    ("json-true-at-one", True), ("json-float-one", 1.0), ("json-text-one", "1"),
    ("digest-text", "sha256:" + "0" * 64),
    ("control-text", "a\x00b\x1fc\x7f"),
)

CENSUS_KEYS = ("enumeratedPaths", "containerPaths", "scalarLeafPaths", "dictPaths",
               "pathsNotRoundTripping", "injectionValues", "enumeratedCases",
               "noOpInjections", "executedCases")
# The keys a published surface row must carry.  `enumeratedCases` is the size of
# the enumerated space; the count of cases actually DRIVEN is published
# separately as `executedCases` and compared against the driver, not the
# arithmetic, because the driver skips injections that cannot be applied.
SURFACE_CENSUS_KEYS = ("enumeratedPaths", "containerPaths", "scalarLeafPaths",
                       "dictPaths", "enumeratedCases", "noOpInjections")


def enumerate_positions(base, leaves=True):
    """Root, every key and every index, unlimited depth, containers AND leaves."""
    positions = [("", base)]

    def walk(value, prefix):
        if isinstance(value, dict):
            children = [(f"{prefix}.{key}" if prefix else str(key), value[key])
                        for key in value]
        elif isinstance(value, list):
            children = [(f"{prefix}[{index}]", item)
                        for index, item in enumerate(value)]
        else:
            return
        for child_path, child in children:
            container = isinstance(child, (dict, list))
            if container or leaves:
                positions.append((child_path, child))
            if container:
                walk(child, child_path)

    walk(base, "")
    return positions


def _split(path):
    parts, buffer, index = [], "", 0
    while index < len(path):
        char = path[index]
        if char == ".":
            parts.append(("key", buffer))
            buffer = ""
        elif char == "[":
            if buffer or not parts:
                parts.append(("key", buffer))
            buffer = ""
            close = path.index("]", index)
            parts.append(("index", int(path[index + 1:close])))
            index = close
        else:
            buffer += char
        index += 1
    if buffer:
        parts.append(("key", buffer))
    return [part for part in parts if not (part[0] == "key" and part[1] == "")]


def resolve(base, path):
    node = base
    for kind, step in _split(path):
        node = node[step] if kind == "key" else node[step]
    return node


def assign(base, path, value):
    steps = _split(path)
    node = base
    for kind, step in steps[:-1]:
        node = node[step] if kind == "key" else node[step]
    node[steps[-1][1]] = value


def _round_trips(base, path, value):
    if path == "":
        return True
    try:
        return resolve(base, path) is value
    except MALFORMED:
        return False


def _same_leaf(left, right):
    return type(left) is type(right) and left == right


def node_census(base, values=HOSTILE_VALUES, leaves=True):
    """The live measurement of the enumerated hostile space."""
    containers = scalars = dicts = not_round_tripping = no_ops = 0
    counted = set()
    for path, value in enumerate_positions(base, leaves):
        if path in counted:
            continue
        if not _round_trips(base, path, value):
            not_round_tripping += 1
            continue
        counted.add(path)
        if isinstance(value, dict):
            dicts += 1
            containers += 1
        elif isinstance(value, list):
            containers += 1
        else:
            scalars += 1
        for _label, injected in values:
            if path != "" and _same_leaf(value, injected):
                no_ops += 1
    paths = len(counted)
    enumerated = paths * len(values) + dicts
    return {
        "enumeratedPaths": paths,
        "containerPaths": containers,
        "scalarLeafPaths": scalars,
        "dictPaths": dicts,
        "pathsNotRoundTripping": not_round_tripping,
        "injectionValues": len(values),
        "enumeratedCases": enumerated,
        "noOpInjections": no_ops,
        "executedCases": enumerated - no_ops,
    }


def merge_census(left, right):
    return {key: left.get(key, 0) + right.get(key, 0)
            for key in CENSUS_KEYS if key != "injectionValues"}


def hostile_cases(base, values=HOSTILE_VALUES, leaves=True):
    """Yield (path, label, mutated-copy) for every non-no-op injection."""
    counted = set()
    for path, value in enumerate_positions(base, leaves):
        if path in counted or not _round_trips(base, path, value):
            continue
        counted.add(path)
        injections = list(values)
        if isinstance(value, dict):
            injections.append(("unknown-key", "<insert>"))
        for label, injected in injections:
            if label != "unknown-key" and path != "" and _same_leaf(value, injected):
                continue
            if path == "":
                if label == "unknown-key":
                    candidate = copy.deepcopy(base)
                    if isinstance(candidate, dict):
                        candidate["ep9UnknownRootKey"] = 1
                else:
                    candidate = copy.deepcopy(injected)
            else:
                candidate = copy.deepcopy(base)
                try:
                    if label == "unknown-key":
                        node = resolve(candidate, path)
                        if not isinstance(node, dict):
                            continue
                        node["ep9UnknownNestedKey"] = 1
                    else:
                        assign(candidate, path, copy.deepcopy(injected))
                except MALFORMED:
                    continue
            yield path, label, candidate


def drive_surface(bases, unguarded, guarded, extra=None, leaves=True,
                  values=HOSTILE_VALUES):
    """One leaf-inclusive hostile matrix.  Returns (census, statistics)."""
    census = {}
    stats = {"executedCases": 0, "unguardedEscapes": 0, "guardedEscapes": 0,
             "silentAccepts": 0, "admitThenRaise": 0,
             "typeDistinctConstantAdmissions": 0}
    for base in bases:
        census = merge_census(census, node_census(base, values, leaves))
        for path, label, candidate in hostile_cases(base, values, leaves):
            stats["executedCases"] += 1
            try:
                unguarded(candidate)
            except BaseException:                          # noqa: BLE001 measured
                stats["unguardedEscapes"] += 1
            try:
                findings = guarded(candidate)
            except BaseException:                          # noqa: BLE001 measured
                stats["guardedEscapes"] += 1
                findings = ["guarded boundary raised"]
            if not findings:
                stats["silentAccepts"] += 1
            if extra is not None:
                extra(stats, path, label, candidate, findings)
    census["injectionValues"] = len(values)
    return census, stats


CONSTANT_LEAF_PATHS = ("schemaVersion", "analysis.admissionDescriptor.schemaVersion")


# How each measured surface signals rejection.  Published per surface so
# `unguardedEscapes` cannot be over-read: for a `raises` layer, an unguarded
# raise IS the declared rejection channel and is not a defect.  What must be
# zero on every surface is `guardedEscapes` — a raise that crossed v9's own
# total boundary — and what must be explained on every surface is `silentAccepts`.
SURFACE_REJECTION_MODE = {
    "plan-intent": "findings",
    "plan-descriptor": "findings-or-raises",
    "evaluation-authority-candidate": "raises",
}


def vector_key(contract):
    """Identity of everything the vector-derived measurements depend on."""
    try:
        return hashlib.sha256(json.dumps(
            [contract.get("positiveVectors"),
             contract.get("acceptedAuthorityVectorId")],
            sort_keys=True, default=repr).encode("utf-8")).hexdigest()
    except MALFORMED:
        return None


def vector_measurements(contract, authority):
    """Every measurement that is a pure function of the vectors, computed once."""
    key = vector_key(contract)
    cached = authority.vector_cache
    if key is not None and cached is not None and cached[0] == key:
        return cached[1]
    intents = []
    for vector in contract.get("positiveVectors") or []:
        try:
            intent = vector["evaluationAuthorityCandidate"][
                "admittedResolvedInputs"]["frozenPlanIntent"]
        except MALFORMED:
            continue
        if intent not in intents:
            intents.append(intent)
    value = {
        "intents": intents,
        "stability": commitment_stability(contract, authority),
        "battery": lb_c2_01_battery(intents, authority),
        "control": lb_c2_01_control(intents, authority),
        "evasion": evasion_measurement(intents, authority),
        "surfaces": measure_surfaces(contract, authority),
    }
    if key is not None:
        authority.vector_cache = (key, value)
    return value


def measure_surfaces(contract, authority):
    """Every wire-shaped surface, enumerated at scalar leaves and EXECUTED."""
    surfaces = {}
    intents, plans = [], []
    for vector in contract.get("positiveVectors") or []:
        try:
            resolved = vector["evaluationAuthorityCandidate"]["admittedResolvedInputs"]
            intent = resolved["frozenPlanIntent"]
            plan = resolved["planDescriptor"]
        except MALFORMED:
            continue
        if intent not in intents:
            intents.append(intent)
        if plan not in plans:
            plans.append(plan)

    def intent_extra(stats, path, _label, candidate, findings):
        if findings:
            return
        _commitment, encode_errors = c2_commit_intent(candidate, authority)
        if encode_errors:
            stats["admitThenRaise"] += 1
        if path in CONSTANT_LEAF_PATHS:
            stats["typeDistinctConstantAdmissions"] += 1

    v4 = authority.c2v4()
    c2_contract = authority.json(C2V4_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    census, stats = drive_surface(
        intents,
        lambda x: v4.validate_plan_intent(x, c2_contract, relations),
        lambda x: c2_validate_intent(x, authority),
        intent_extra)
    surfaces["plan-intent"] = {"census": census, "stats": stats}

    ri = authority.module(RESOLVED)
    v3_contract = authority.json(C2V3_CONTRACT)
    census, stats = drive_surface(
        plans,
        lambda x: ri._plan_record_errors(x, v3_contract),
        lambda x: _total(ri._plan_record_errors, x, v3_contract))
    surfaces["plan-descriptor"] = {"census": census, "stats": stats}

    # The authority-admission surface: hostile parsed JSON at every position of
    # the accepted EvaluationAuthorityCandidateV1, driven through EP8's real
    # public authorize_evaluation.  A silent accept here is an admitted forgery.
    ep8 = authority.module(EP8)
    accepted = contract.get("acceptedAuthorityVectorId")
    vector = next((row for row in contract.get("positiveVectors") or []
                   if isinstance(row, dict) and row.get("id") == accepted), None)
    if vector is not None:
        fixture = vector.get("trustedStoreFixture")
        candidate = vector.get("evaluationAuthorityCandidate")

        def authorize(value):
            store = ep8._open_test_project_store(copy.deepcopy(fixture))
            return ep8.authorize_evaluation(store, value)

        def record(stats, path, label, _candidate, findings):
            if not findings:
                stats.setdefault("admitted", []).append(f"{path}={label}")

        census, stats = drive_surface(
            [candidate], authorize, lambda x: _total(authorize, x), record)
        stats.setdefault("admitted", []).sort()
        surfaces["evaluation-authority-candidate"] = {"census": census, "stats": stats}
    return surfaces


def _total(function, *args):
    try:
        result = function(*args)
    except MALFORMED as exc:
        return [f"boundary: {type(exc).__name__}: {exc}"]
    return list(result) if isinstance(result, (list, tuple)) else []


def measure_contract_root(contract, authority, execute):
    """The candidate document itself, driven through the total check() boundary."""
    census = node_census(contract)
    stats = {"executedCases": 0, "unguardedEscapes": 0, "guardedEscapes": 0,
             "guardedExercised": 0, "silentAccepts": 0, "executed": execute}
    if not execute:
        return census, stats
    saved = authority.deep_enabled
    authority.deep_enabled = False
    try:
        seen = set()
        for path, _label, candidate in hostile_cases(contract):
            stats["executedCases"] += 1
            raised = False
            try:
                _check(candidate, authority)
            except BaseException:                          # noqa: BLE001 measured
                stats["unguardedEscapes"] += 1
                raised = True
            if raised or path not in seen:
                seen.add(path)
                stats["guardedExercised"] += 1
                try:
                    findings = check(candidate, authority)
                except BaseException:                      # noqa: BLE001 measured
                    stats["guardedEscapes"] += 1
                    findings = ["guarded boundary raised"]
                if not findings:
                    stats["silentAccepts"] += 1
    finally:
        authority.deep_enabled = saved
    return census, stats


# --------------------------------------------------------------------------
# Section 5.  The AST tripwire — declared as a tripwire, measured as one.
#
# EV10-IR-01 and IR-C2V4-01 both defeated this scan class constructively.  This
# checker therefore MEASURES its own scan's blind spot instead of claiming
# immunity, and requires the independent behavioural layer of Section 2 to catch
# every variant the scan misses.
# --------------------------------------------------------------------------

_SCAN_CACHE: dict[str, object] = {}

# Every function permitted to name a C-2 API directly.  These four ARE the join.
C2_JOIN_CLOSURE = ("c2_validate_intent", "c2_commit_intent", "c2_canonical_intent",
                   "c2_api_surface")
# Functions permitted to name a C-2 API directly because they ARE the
# measurement: the unguarded control side of a matrix, and the cross-checks
# against the superseded encoder.  These take no authority from the call.
C2_MEASUREMENT_CLOSURE = ("commitment_stability", "evasion_measurement",
                          "lb_c2_01_control", "measure_surfaces",
                          "run_source_mutations")


def _own_tree():
    if "tree" not in _SCAN_CACHE:
        _SCAN_CACHE["tree"] = ast.parse((HERE / pathlib.Path(__file__).name).read_bytes())
    return _SCAN_CACHE["tree"]


def _module_functions(tree):
    return {node.name: node for node in tree.body
            if isinstance(node, ast.FunctionDef)}


def c2_join_scan(tree=None):
    """Syntactic tripwire: which functions name a C-2 API at all.

    DECLARED SCOPE, stated so it cannot be over-read: this scan sees an
    ast.Attribute or ast.Name whose identifier is literally one of the three
    imported C-2 API names, inside a top-level ast.FunctionDef.  It does not see
    a call reached through a module alias, a local alias, getattr, a dispatch
    table, an inner function, a comprehension, a walrus, a tuple-unpack or a
    class method.  ``evasion_measurement`` proves that by construction.
    """
    if tree is None and "c2_join_scan" in _SCAN_CACHE:
        return _SCAN_CACHE["c2_join_scan"]
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    sites, outside = 0, []
    authority_routed, direct_module = 0, []
    for name in sorted(functions):
        for node in ast.walk(functions[name]):
            identifier = None
            if isinstance(node, ast.Attribute):
                identifier = node.attr
            elif isinstance(node, ast.Name):
                identifier = node.id
            if identifier not in C2_IMPORTED_APIS:
                continue
            sites += 1
            if name not in C2_JOIN_CLOSURE and name not in C2_MEASUREMENT_CLOSURE:
                outside.append(f"{name} line {getattr(node, 'lineno', 0)}")
            if name in C2_JOIN_CLOSURE:
                # Inside the join, the receiver must be an Authority accessor
                # call, never a bare module reference.
                receiver = getattr(node, "value", None)
                if isinstance(receiver, ast.Call) and \
                        isinstance(receiver.func, ast.Attribute) and \
                        receiver.func.attr in ("c2v4", "c2v3"):
                    authority_routed += 1
                else:
                    direct_module.append(f"{name} line {getattr(node, 'lineno', 0)}")
    result = {
        "scannedFunctions": len(functions),
        "declaredJoinClosure": list(C2_JOIN_CLOSURE),
        "declaredMeasurementClosure": list(C2_MEASUREMENT_CLOSURE),
        "apiReferenceSites": sites,
        "referencesOutsideDeclaredClosure": sorted(set(outside)),
        "authorityRoutedSites": authority_routed,
        "unroutedSitesInsideJoin": sorted(set(direct_module)),
    }
    if tree is None:
        _SCAN_CACHE["c2_join_scan"] = result
    return result


def selftest_reachability_scan(tree=None):
    """The --selftest path must be live, singular and flag-guarded.

    This exists because of the evidence.v8 defect: main() returned at the
    findings branch before the mutation suite, so normal and --selftest produced
    byte-identical output and the suite never ran.
    """
    if tree is None and "selftest_reachability_scan" in _SCAN_CACHE:
        return _SCAN_CACHE["selftest_reachability_scan"]
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    flags = set()
    for node in ast.walk(subject):
        if isinstance(node, ast.Compare):
            for child in ast.walk(node):
                if isinstance(child, ast.Constant) and isinstance(child.value, str) \
                        and child.value.startswith("--"):
                    flags.add(child.value)
    for node in subject.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "DECLARED_FLAGS"
                for target in node.targets):
            flags.update(child.value for child in ast.walk(node.value)
                         if isinstance(child, ast.Constant)
                         and isinstance(child.value, str))
    dispatches = guarded_dispatches = 0

    def visit(node, inside, guard):
        nonlocal dispatches, guarded_dispatches
        if isinstance(node, ast.FunctionDef) and node.name == "selftest":
            inside = True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                node.func.id == "selftest" and not inside:
            dispatches += 1
            if guard is not None:
                guarded_dispatches += 1
        if isinstance(node, ast.If):
            literals = {child.value for child in ast.walk(node.test)
                        if isinstance(child, ast.Constant)
                        and isinstance(child.value, str)}
            declared = literals & set(DECLARED_FLAGS)
            for child in node.body:
                visit(child, inside, sorted(declared)[0] if declared else guard)
            for child in node.orelse:
                visit(child, inside, guard)
            return
        for child in ast.iter_child_nodes(node):
            visit(child, inside, guard)

    visit(subject, False, None)
    main_function = functions.get("main")
    dispatch_index = findings_index = None
    if main_function is not None:
        for index, statement in enumerate(main_function.body):
            text = ast.dump(statement)
            if dispatch_index is None and "Name(id='selftest'" in text:
                dispatch_index = index
            if findings_index is None and "Name(id='findings'" in text and \
                    "Return(" in text:
                findings_index = index
    result = {
        "hasSingleMain": main_function is not None and
                         sum(1 for node in subject.body
                             if isinstance(node, ast.FunctionDef)
                             and node.name == "main") == 1,
        "flags": sorted(flags),
        "dispatchCount": dispatches,
        "guardedDispatchCount": guarded_dispatches,
        "dispatchBeforeFindingsReturn": dispatch_index is not None and
                                        (findings_index is None or
                                         dispatch_index < findings_index),
    }
    if tree is None:
        _SCAN_CACHE["selftest_reachability_scan"] = result
    return result


GUARD_HELPERS = ("exact_int", "exact_int_list", "int_in_range", "is_wire_int")
INTEGER_SCAN_ENTRYPOINTS = ("_check", "_c2_join_findings", "_closure_findings",
                            "_deep_findings")


def _reachable(functions, roots):
    seen, queue = set(), [name for name in roots if name in functions]
    while queue:
        name = queue.pop()
        if name in seen:
            continue
        seen.add(name)
        for node in ast.walk(functions[name]):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                    node.func.id in functions and node.func.id not in seen:
                queue.append(node.func.id)
    return seen


def _is_wire_expression(node, tainted):
    """A value that came from parsed JSON rather than from this checker."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and \
            node.func.attr == "get":
        return True
    if isinstance(node, ast.Subscript):
        return True
    if isinstance(node, ast.Name):
        return node.id in tainted
    return False


def _tainted_names(function):
    tainted = {arg.arg for arg in list(function.args.args) +
               list(function.args.kwonlyargs)}
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                isinstance(node.targets[0], ast.Name) and \
                _is_wire_expression(node.value, tainted):
            tainted.add(node.targets[0].id)
    return tainted


def _numeric_literal(node):
    return isinstance(node, ast.Constant) and \
        isinstance(node.value, (int, float)) and not isinstance(node.value, bool)


def integer_guard_scan(tree=None):
    """Every wire-sourced numeric test must route through a declared guard.

    This is a TRIPWIRE with the same declared blind spot as ``c2_join_scan``.  The
    load-bearing guard for this property is ``own_constant_leaf_battery``, which
    reads no source at all.
    """
    if tree is None and "integer_guard_scan" in _SCAN_CACHE:
        return _SCAN_CACHE["integer_guard_scan"]
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    reached = _reachable(functions, INTEGER_SCAN_ENTRYPOINTS) - set(GUARD_HELPERS)
    missing = [name for name in INTEGER_SCAN_ENTRYPOINTS if name not in functions]
    unguarded, helper_sites = [], 0
    for name in sorted(reached):
        function = functions[name]
        tainted = _tainted_names(function)
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                    node.func.id in GUARD_HELPERS:
                helper_sites += 1
            if not isinstance(node, ast.Compare):
                continue
            operands = [node.left] + list(node.comparators)
            for index, operator in enumerate(node.ops):
                if isinstance(operator, (ast.Is, ast.IsNot, ast.In, ast.NotIn)):
                    continue
                left, right = operands[index], operands[index + 1]
                for first, second in ((left, right), (right, left)):
                    if _numeric_literal(second) and _is_wire_expression(first, tainted):
                        unguarded.append(f"{name} line {getattr(node, 'lineno', 0)}: "
                                         f"{ast.unparse(node)}")
    result = {
        "scannedFunctions": len(reached),
        "guardHelperCallSites": helper_sites,
        "unguardedNumericComparisons": len(unguarded),
        "unguarded": sorted(set(unguarded)),
        "missingEntrypoints": missing,
    }
    if tree is None:
        _SCAN_CACHE["integer_guard_scan"] = result
    return result


# The three spellings of "one" that are `== 1` or `== 0` in the host language but
# are NOT the JSON integer.  These are the values LB-C2-01 turned on.
TYPE_DISTINCT_INJECTIONS = (
    ("json-true", True), ("json-false", False), ("json-float", 1.0),
)


# The battery window, declared rather than implied.  Leaves under
# `positiveVectors` are EXCLUDED here and covered instead by the
# `evaluation-authority-candidate` surface matrix, which drives every one of
# them through EP8's real authorize_evaluation, and by the contract-root matrix.
# The exclusion exists because injecting inside the vectors invalidates the
# vector measurement cache, so covering them here would re-drive three full
# surface matrices per leaf.  Understating this window would be exactly the
# failure IMPLEMENTATION-FREEZE section 7 names, so it is stated, measured and
# published rather than left to inference.
OWN_BATTERY_EXCLUDED_PREFIX = "positiveVectors"

# The declared integer register for the block --selftest produces.  check()
# cannot value-verify these, so it type-verifies them.
OWN_BATTERY_INTEGER_FIELDS = ("intBoolLeaves", "excludedLeaves", "cases",
                              "rejected", "silentlyAdmitted", "escapes")


def own_constant_leaf_battery(contract, authority):
    """MEASURE this checker's own LB-C2-01 exposure, without reading source.

    Every integer or boolean scalar leaf of the candidate outside
    ``OWN_BATTERY_EXCLUDED_PREFIX`` is replaced, in turn, by each type-distinct
    spelling, and the full checking layer is re-run.  A leaf this checker
    constrains must produce a finding.  A leaf it does not constrain is reported
    as a silent admission and the enumerated set is required to match the
    candidate's declaration exactly, so the set can neither grow nor shrink
    silently.  Mutation is in place and restored, so the 636 KB candidate is
    never deep-copied.
    """
    stats = {"intBoolLeaves": 0, "cases": 0, "rejected": 0, "silentlyAdmitted": 0,
             "escapes": 0, "excludedLeaves": 0, "admitted": []}
    leaves = []
    for path, value in enumerate_positions(contract):
        if not path or not isinstance(value, (int, bool)):
            continue
        if path == OWN_BATTERY_EXCLUDED_PREFIX or \
                path.startswith(OWN_BATTERY_EXCLUDED_PREFIX + "["):
            stats["excludedLeaves"] += 1
            continue
        leaves.append(path)
    for path in leaves:
        stats["intBoolLeaves"] += 1
        try:
            original = resolve(contract, path)
        except MALFORMED:
            continue
        for label, injected in TYPE_DISTINCT_INJECTIONS:
            if _same_leaf(original, injected):
                continue
            stats["cases"] += 1
            try:
                assign(contract, path, injected)
            except MALFORMED:
                continue
            try:
                findings = check(contract, authority)
            except BaseException:                          # noqa: BLE001 measured
                stats["escapes"] += 1
                findings = None
            finally:
                assign(contract, path, original)
            if findings is None:
                continue
            if findings:
                stats["rejected"] += 1
            else:
                stats["silentlyAdmitted"] += 1
                stats["admitted"].append(f"{path}={label}")
    stats["admitted"].sort()
    return stats


# The nine indirection classes that defeated the equivalent scan in
# check-evidence-v10.py (EV10-IR-01) and check-c2-v4.py (IR-C2V4-01).  Each
# template reintroduces the SAME semantic defect — the join reaching the
# DEFECTIVE v3 instrument — through a different spelling.
EVASION_TEMPLATES = (
    ("module-alias", """
import sys
_alias = sys.modules[_C2V3_NAME]
def join(intent, contract, relations):
    return _alias.validate_plan_intent(intent, contract, relations)
"""),
    ("local-alias", """
import sys
def join(intent, contract, relations):
    local = sys.modules[_C2V3_NAME]
    return local.validate_plan_intent(intent, contract, relations)
"""),
    ("getattr-modules", """
import sys
def join(intent, contract, relations):
    fn = getattr(sys.modules[_C2V3_NAME], "".join(["validate", "_plan_intent"]))
    return fn(intent, contract, relations)
"""),
    ("dispatch-table", """
import sys
_TABLE = {"v": sys.modules[_C2V3_NAME].validate_plan_intent}
def join(intent, contract, relations):
    return _TABLE["v"](intent, contract, relations)
"""),
    ("inner-function", """
import sys
def join(intent, contract, relations):
    def inner(value):
        return sys.modules[_C2V3_NAME].validate_plan_intent(value, contract, relations)
    return inner(intent)
"""),
    ("comprehension", """
import sys
def join(intent, contract, relations):
    return [sys.modules[_C2V3_NAME].validate_plan_intent(x, contract, relations)
            for x in (intent,)][0]
"""),
    ("walrus", """
import sys
def join(intent, contract, relations):
    return (fn := sys.modules[_C2V3_NAME].validate_plan_intent)(
        intent, contract, relations)
"""),
    ("tuple-unpack", """
import sys
def join(intent, contract, relations):
    fn, _spare = sys.modules[_C2V3_NAME].validate_plan_intent, None
    return fn(intent, contract, relations)
"""),
    ("class-method", """
import sys
class _Join:
    def run(self, intent, contract, relations):
        return sys.modules[_C2V3_NAME].validate_plan_intent(intent, contract, relations)
def join(intent, contract, relations):
    return _Join().run(intent, contract, relations)
"""),
)


def evasion_measurement(intents, authority):
    """Build all nine evasions, MEASURE the scan's blind spot, prove the catch.

    For each variant: (a) what this checker's own syntactic scan reports on the
    evaded tree, and (b) whether the independent behavioural layer — which does
    not read source at all — still detects that the join has reached a defective
    instrument.  Column (b) must be 9/9.  Column (a) is published as measured,
    however unflattering, because refusing to state it is precisely the coverage
    claim over an unobserved region this corpus keeps shipping.
    """
    v3_name = None
    for name, module in sys.modules.items():
        if module is authority.modules.get(C2V3_CHECKER):
            v3_name = name
            break
    contract = authority.json(C2V3_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    intent = intents[0] if intents else None
    result = {"variants": 0, "detectedBySyntacticScan": 0,
              "missedBySyntacticScan": 0, "caughtByBehaviouralLayer": 0,
              "notLive": [], "missed": []}
    if v3_name is None or intent is None:
        result["notLive"].append("the superseded encoder is not resolvable by name")
        return result
    for label, template in EVASION_TEMPLATES:
        result["variants"] += 1
        source = f"_C2V3_NAME = {v3_name!r}\n" + template
        # (a) the syntactic scan, run over the evaded tree
        try:
            report = c2_join_scan(ast.parse(source))
            detected = bool(report["apiReferenceSites"])
        except SyntaxError:
            result["notLive"].append(f"{label}: template does not parse")
            continue
        if detected:
            result["detectedBySyntacticScan"] += 1
        else:
            result["missedBySyntacticScan"] += 1
        # (b) the behavioural layer, which never reads source
        namespace: dict[str, object] = {}
        try:
            exec(compile(source, f"<ep9-evasion-{label}>", "exec"), namespace)
            join = namespace["join"]
        except BaseException:                              # noqa: BLE001 measured
            result["notLive"].append(f"{label}: evaded join is not constructible")
            continue
        caught = False
        for _site, path in COMMITMENT_BEARING_LEAVES:
            for _value_label, injected in TYPE_DISTINCT_ONES:
                hostile = copy.deepcopy(intent)
                try:
                    _set_path(hostile, path, injected)
                    evaded_findings = join(hostile, contract, relations)
                except BaseException:                      # noqa: BLE001 measured
                    continue
                repaired_findings = c2_validate_intent(hostile, authority)
                # The behavioural signal: the evaded join ADMITS what the
                # repaired join REJECTS.  No source is read to observe this.
                if not evaded_findings and repaired_findings:
                    caught = True
        if caught:
            result["caughtByBehaviouralLayer"] += 1
        else:
            result["missed"].append(label)
    return result


# --------------------------------------------------------------------------
# Section 6.  The contract check.
# --------------------------------------------------------------------------

CHANGED_TOP = {
    "version", "author", "date", "role", "supersedesProofObligationsOf",
    "repairs", "knownLimitations", "c2AuthorityJoin",
}
EXPECTED_ADDITIONS = {
    "identityStabilityFromEP8", "c2AuthorityRepairJoin", "delegationClosure",
    "planIntentCommitmentStability", "scalarLeafTotality", "astScanScope",
    "checkerModeContract", "adversarialControlsV9", "repairMutations",
}
REQUIRED_NEGATIVES = {
    "EP9-NEG-C2V3-BOOLEAN-SCHEMA-VERSION-ADMITTED",
    "EP9-NEG-C2V3-FLOAT-SCHEMA-VERSION-ADMIT-THEN-RAISE",
    "EP9-NEG-C2V3-DESCRIPTOR-SCHEMA-VERSION-ADMITTED",
    "EP9-NEG-EP8-MINTS-AUTHORITY-OVER-SECOND-DIGEST",
    "EP9-NEG-CLOSURE-MEMBER-DIGEST-DRIFT",
    "EP9-NEG-CLOSURE-PIN-DISAGREEMENT",
    "EP9-NEG-COMMITMENT-MOVED-BY-REPIN",
    "EP9-NEG-C2V4-REVIEW-VERDICT-SOFTENED",
    "EP9-NEG-CONTAINER-ONLY-ENUMERATION",
    "EP9-NEG-AST-SCAN-AS-SOLE-GUARD",
    "EP9-NEG-DEAD-SELFTEST",
    "EP9-NEG-HOSTILE-ROOT-TRACEBACK",
}


def _check(contract, authority):
    """The UNGUARDED implementation.  check() is its total boundary."""
    findings: list[str] = []
    if not isinstance(contract, dict):
        return ["EP9-ROOT: the contract root is not a JSON object"]
    ep8 = authority.json(EP8_ARTIFACT)

    # ---- identity and posture ------------------------------------------
    if contract.get("artifact") != "opensip.evaluation-proof" or \
            not exact_int(contract.get("version"), EXPECTED_VERSION):
        findings.append("EP9-POSTURE: artifact/version mismatch")
    if contract.get("status") != "CANDIDATE-NOT-APPLIED" or \
            contract.get("sealRecommendation") != "DO-NOT-SEAL":
        findings.append("EP9-POSTURE: candidate/no-seal status drift")
    assurance = contract.get("assurance") or {}
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("candidateState") != "NOT-APPLIED" or \
            assurance.get("qualificationEvidenceIds") != [] or \
            assurance.get("releaseEvidenceIds") != []:
        findings.append("EP9-POSTURE: assurance exceeds specified/implementable-unexecuted")
    residuals = json.dumps(contract.get("knownLimitations") or [])
    for term in ("V10", "CD-RT-5", "G19", "not applied"):
        if term not in residuals:
            findings.append(f"EP9-POSTURE: required residual term {term!r} absent")

    # ---- the pinned EP8 predecessor must still validate -----------------
    if authority.predecessor_cache is None:
        cached = []
        try:
            if authority.module(EP8).check(copy.deepcopy(ep8)):
                cached.append("EP9-PREDECESSOR: the pinned EP8 predecessor no longer "
                              "validates under its own retained checker")
        except MALFORMED as exc:
            cached.append(f"EP9-PREDECESSOR: EP8 validation raised "
                          f"{type(exc).__name__}: {exc}")
        cached.extend(closure_pin_agreement(authority))
        authority.predecessor_cache = cached
    findings.extend(authority.predecessor_cache)

    # ---- inherited surface: everything EP8 carried, unmoved -------------
    if not isinstance(ep8, dict):
        findings.append("EP9-INHERIT: the pinned EP8 artifact is not an object")
    else:
        for key in sorted(set(ep8) - CHANGED_TOP):
            if contract.get(key) != ep8[key]:
                findings.append(f"EP9-INHERIT: EP8 protected surface changed: {key}")
        if set(contract) - set(ep8) != EXPECTED_ADDITIONS:
            findings.append("EP9-INHERIT: v9 top-level additions are not exact/closed; "
                            f"found {sorted(set(contract) - set(ep8))}")
        missing = set(ep8) - set(contract)
        if missing:
            findings.append(f"EP9-INHERIT: v9 drops EP8 top-level keys {sorted(missing)}")

    stability_block = contract.get("identityStabilityFromEP8") or {}
    if stability_block.get("predecessorSha256") != PINNED_DATA[EP8_ARTIFACT] or \
            stability_block.get("predecessorCheckerSha256") != DELEGATION_CLOSURE[EP8]:
        findings.append("EP9-INHERIT: EP8 protected hash window drift")
    if stability_block.get("vectorProjection") != "identity — v9 carries the EP8 " \
            "vectors byte-value unchanged, so no projection function is required":
        findings.append("EP9-INHERIT: the v9 vector projection rule is not the "
                        "identity rule the candidate must carry")

    # ---- the C-2 re-pin -------------------------------------------------
    findings.extend(_c2_join_findings(contract, authority))

    # ---- the delegation closure ----------------------------------------
    findings.extend(_closure_findings(contract, authority))

    # ---- the declared integer register ---------------------------------
    # Every other declared count in this candidate is compared against a live
    # measurement, and an exact_int comparison rejects a type-distinct spelling
    # on the way.  The own-constant-leaf battery block is the exception: it is
    # PRODUCED by --selftest, so check() cannot know its values.  The battery
    # itself found that gap — injecting JSON false at a field whose value is 0
    # preserves the no-op census exactly, so nothing detected it.  These fields
    # are therefore type-registered here: a declared count must be a JSON
    # integer, whatever its value.
    for field in OWN_BATTERY_INTEGER_FIELDS:
        value = ((contract.get("astScanScope") or {}).get(
            "ownConstantLeafBattery") or {}).get(field)
        if not int_in_range(value, 0, INT64_MAX):
            findings.append(
                f"EP9-LB-C2-01-CLASS: astScanScope.ownConstantLeafBattery.{field} is "
                f"{value!r}, which is not a JSON integer; a declared count spelled as "
                "true, false or 1.0 is exactly the defect this candidate re-pins away "
                "from")

    # ---- checker mode contract -----------------------------------------
    modes = contract.get("checkerModeContract") or {}
    exit_codes = modes.get("exitCodes")
    if not isinstance(exit_codes, list) or len(exit_codes) != 4 or \
            not exact_int_list([row.get("code") for row in exit_codes
                                if isinstance(row, dict)], [0, 1, 2, 3]):
        findings.append("EP9-MODE: the exit-code table must declare exactly 0/1/2/3")
    if "can never be absorbed into a pass" not in json.dumps(exit_codes):
        findings.append("EP9-MODE: the dirty-base refusal rule is not declared")

    # ---- deep layers ----------------------------------------------------
    if authority.deep_enabled:
        findings.extend(_deep_findings(contract, authority))

    # ---- adversarial matrix ---------------------------------------------
    negatives = contract.get("adversarialControlsV9")
    if not isinstance(negatives, list) or {
            row.get("id") for row in negatives if isinstance(row, dict)
    } != REQUIRED_NEGATIVES:
        findings.append("EP9-NEGATIVES: the v9 adversarial matrix is incomplete")
    mutations = contract.get("repairMutations")
    repairs = contract.get("repairs")
    if not isinstance(mutations, list) or not isinstance(repairs, list) or \
            len(mutations) != len(repairs):
        findings.append("EP9-MUTATIONS: every declared repair requires exactly one "
                        "mutation proving it load-bearing")
    elif {row.get("repairId") for row in mutations if isinstance(row, dict)} != \
            {row.get("id") for row in repairs if isinstance(row, dict)}:
        findings.append("EP9-MUTATIONS: the mutation set does not cover the repair set")
    return findings


def _c2_join_findings(contract, authority):
    findings: list[str] = []
    join = contract.get("c2AuthorityJoin") or {}
    if join.get("sourceArtifact") != C2V4_CONTRACT or \
            join.get("sourceSha256") != PINNED_DATA[C2V4_CONTRACT]:
        findings.append("EP9-C2-REPIN: c2AuthorityJoin does not bind the repaired "
                        f"{C2V4_CONTRACT} at its verified digest")
    if join.get("checker") != C2V4 or join.get("checkerSha256") != DELEGATION_CLOSURE[C2V4]:
        findings.append("EP9-C2-REPIN: c2AuthorityJoin does not bind the repaired "
                        f"{C2V4} at its verified digest")
    if sorted(join.get("importedCheckerApis") or []) != sorted(C2_IMPORTED_APIS):
        findings.append("EP9-C2-REPIN: the imported C-2 API set is not the exact "
                        f"three-API seam {sorted(C2_IMPORTED_APIS)}")
    if join.get("factPlaneSha256") != PINNED_DATA[FACT_PLANE]:
        findings.append("EP9-C2-REPIN: the fact-plane pin drifted")
    findings.extend(c2_api_surface(authority))

    repair = contract.get("c2AuthorityRepairJoin") or {}
    if repair.get("supersededChecker") != C2V3_CHECKER or \
            repair.get("supersededCheckerSha256") != C2V3_CHECKER_SHA or \
            repair.get("supersededContract") != C2V3_CONTRACT or \
            repair.get("supersededContractSha256") != PINNED_DATA[C2V3_CONTRACT]:
        findings.append("EP9-C2-REPIN: the superseded C-2 bytes are not recorded by "
                        "digest, so the re-pin has no falsifiable subject")
    if repair.get("repairAuthorisedBy") != C2V4_REVIEW or \
            repair.get("repairAuthorisedBySha256") != PINNED_DATA[C2V4_REVIEW] or \
            repair.get("repairAuthorisedByVerdict") != "PASS" or \
            not exact_int(repair.get("repairAuthorisedByBlockingFindingCount"), 0):
        findings.append("EP9-C2-REPIN: the authorising C-2 v4 review is not recorded "
                        "with its verdict and blocking-finding count")
    if repair.get("ep6InnerJoinResidualId") != "RES-EP9-01" or \
            "does not repair" not in repair.get("ep6InnerJoinResidual", ""):
        findings.append("EP9-C2-REPIN: RES-EP9-01 must state plainly that v9 does not "
                        "repair EP6's inner join and is an outer gate over it")
    return findings


def _closure_findings(contract, authority):
    findings: list[str] = []
    closure = contract.get("delegationClosure") or {}
    members = closure.get("executables")
    if not isinstance(members, list) or len(members) != len(DELEGATION_CLOSURE):
        findings.append(f"EP9-CLOSURE: exactly {len(DELEGATION_CLOSURE)} closure "
                        "executables must be declared")
        return findings
    declared = {}
    for row in members:
        if not isinstance(row, dict):
            findings.append("EP9-CLOSURE: a closure member row is not an object")
            continue
        declared[row.get("file")] = row.get("sha256")
    if set(declared) != set(DELEGATION_CLOSURE):
        findings.append("EP9-CLOSURE: the declared closure is not the exact ten-member "
                        f"set; declared {sorted(k for k in declared if k)}")
    for name, digest in DELEGATION_CLOSURE.items():
        if declared.get(name) != digest:
            findings.append(f"EP9-CLOSURE: {name} is declared at {declared.get(name)} "
                            f"but was verified at {digest}")
    if closure.get("verificationRule") != "read once, SHA-256 verified, then executed " \
            "from that verified byte string; no second disk read between verification " \
            "and execution":
        findings.append("EP9-CLOSURE: the hash-before-execution rule is not declared "
                        "verbatim")
    data = closure.get("pinnedData")
    if not isinstance(data, list) or {
            row.get("file") for row in data if isinstance(row, dict)
    } != set(PINNED_DATA):
        findings.append("EP9-CLOSURE: the pinned data record is not the exact verified "
                        "set; a count is not a record")
    else:
        for row in data:
            name = row.get("file")
            if PINNED_DATA.get(name) != row.get("sha256"):
                findings.append(f"EP9-CLOSURE: pinned data {name} digest drift")
    encoder = closure.get("supersededIndependentEncoder") or {}
    if encoder.get("file") != C2V3_CHECKER or encoder.get("sha256") != C2V3_CHECKER_SHA:
        findings.append("EP9-CLOSURE: the superseded independent encoder is not "
                        "recorded by digest")
    return findings


def _deep_findings(contract, authority):
    """The measured layers.  Everything here is recomputed on every run."""
    findings: list[str] = []
    measurement = {}
    measured = vector_measurements(contract, authority)

    # ---- commitments unmoved -------------------------------------------
    stability = measured["stability"]
    measurement["commitmentStability"] = stability
    findings.extend(stability["findings"])
    for message in stability["moved"]:
        findings.append("EP9-COMMITMENT-MOVED: the C-2 v4 re-pin changed a "
                        f"planIntentCommitment. This is a MAJOR finding and must not "
                        f"be absorbed — {message}")
    declared = contract.get("planIntentCommitmentStability") or {}
    if not exact_int(declared.get("vectors"), stability["vectors"]) or \
            not exact_int(declared.get("recomputedUnderV4"),
                          stability["recomputedUnderV4"]) or \
            not exact_int(declared.get("reproducedUnderSupersededEncoder"),
                          stability["reproducedUnderV3"]) or \
            not exact_int(declared.get("preimageByteIdentical"),
                          stability["preimageByteIdentical"]):
        findings.append(
            f"EP9-COMMITMENT: the candidate publishes vectors="
            f"{declared.get('vectors')!r}/recomputedUnderV4="
            f"{declared.get('recomputedUnderV4')!r}/reproducedUnderSupersededEncoder="
            f"{declared.get('reproducedUnderSupersededEncoder')!r}/preimageByteIdentical="
            f"{declared.get('preimageByteIdentical')!r}; this run measured "
            f"{stability['vectors']}/{stability['recomputedUnderV4']}/"
            f"{stability['reproducedUnderV3']}/{stability['preimageByteIdentical']}")
    if declared.get("distinctCommitments") != stability["distinctCommitments"]:
        findings.append("EP9-COMMITMENT: the declared distinct commitment set is not "
                        f"the measured set {stability['distinctCommitments']}")
    if not exact_int_list(declared.get("preimageByteLengths"),
                          stability["preimageByteLengths"]):
        findings.append("EP9-COMMITMENT: the declared canonical preimage byte lengths "
                        f"are not the measured {stability['preimageByteLengths']}")
    if declared.get("unmovedFromEP8") is not True or \
            declared.get("provenBy") != "recomputation through C-2 v4 and independent " \
            "reproduction under the superseded encoder, with byte-identical preimages":
        findings.append("EP9-COMMITMENT: the unmoved claim must be declared as proven "
                        "by recomputation, not by copying the EP8 literal")
    # The named field itself.  It is compared against the value the PINNED EP8
    # artifact carries and against this run's recomputation — never against a
    # literal carried forward from v9's own text.
    join = contract.get("c2AuthorityJoin") or {}
    ep8_doc = authority.json(EP8_ARTIFACT)
    ep8_join = (ep8_doc.get("c2AuthorityJoin") or {}) if isinstance(ep8_doc, dict) else {}
    if ep8_join.get("expectedPlanIntentCommitment") != EP8_COMMITMENT:
        findings.append("EP9-COMMITMENT: the pinned EP8 artifact does not carry the "
                        f"commitment {EP8_COMMITMENT} this checker expects of it")
    for field in ("expectedPlanIntentCommitment", "executionPlanCommitment"):
        if join.get(field) != ep8_join.get(field):
            findings.append(
                f"EP9-COMMITMENT-MOVED: c2AuthorityJoin.{field} is {join.get(field)!r} "
                f"but EP8 committed {ep8_join.get(field)!r}. This is a MAJOR finding "
                "and must not be absorbed.")
        elif join.get(field) not in stability["distinctCommitments"]:
            findings.append(
                f"EP9-COMMITMENT: c2AuthorityJoin.{field} was not reproduced by "
                "recomputation through C-2 v4 over the vectors; it is a copied "
                "literal, which is exactly what this candidate refuses to rely on")
    for field in ("planIntentCanonicalByteLength", "snapshotPreimageByteLength",
                  "planPreimageByteLength"):
        if not exact_int(join.get(field), ep8_join.get(field)):
            findings.append(f"EP9-COMMITMENT-MOVED: c2AuthorityJoin.{field} is "
                            f"{join.get(field)!r} but EP8 recorded "
                            f"{ep8_join.get(field)!r}")
    if not exact_int_list([join.get("planIntentCanonicalByteLength")],
                          stability["preimageByteLengths"]):
        findings.append(
            "EP9-COMMITMENT: the declared canonical preimage length "
            f"{join.get('planIntentCanonicalByteLength')!r} is not the length this run "
            f"measured through the repaired encoder {stability['preimageByteLengths']}")

    intents = measured["intents"]

    # ---- the LB-C2-01 battery and its positive control ------------------
    battery = measured["battery"]
    control = measured["control"]
    measurement["lbC201"] = {"repaired": battery, "superseded": control}
    if battery["admitted"] or battery["escapes"]:
        findings.append(
            f"EP9-LB-C2-01: the repaired join ADMITTED {battery['admitted']} "
            f"type-distinct schemaVersion case(s) {sorted(set(battery['admissions']))} "
            f"and produced {battery['escapes']} boundary escape(s); the C-2 join is "
            "not reaching the repaired instrument")
    expected_admissions = expected_control_admissions(intents)
    if control["admitted"] != expected_admissions or expected_admissions == 0:
        findings.append(
            f"EP9-LB-C2-01: the positive control is not the defect it claims to model "
            f"— the SUPERSEDED instrument admitted {control['admitted']} of "
            f"{battery['cases']} cases where the bare `!= 1` guard predicts exactly "
            f"{expected_admissions}; this battery cannot be relied on to distinguish a "
            "repaired join from a defective one")
    if control["secondDigests"] + control["admitThenRaise"] != control["admitted"]:
        findings.append(
            f"EP9-LB-C2-01: the superseded instrument admitted {control['admitted']} "
            f"case(s) but only {control['secondDigests']} produced a second digest and "
            f"{control['admitThenRaise']} raised inside the encoder; LB-C2-01 predicts "
            "every admission does one or the other")
    declared_repair = (contract.get("c2AuthorityRepairJoin") or {}).get("lbC201Battery") or {}
    if not exact_int(declared_repair.get("cases"), battery["cases"]) or \
            not exact_int(declared_repair.get("rejectedByRepairedJoin"),
                          battery["rejected"]) or \
            not exact_int(declared_repair.get("admittedByRepairedJoin"),
                          battery["admitted"]) or \
            not exact_int(declared_repair.get("admittedBySupersededInstrument"),
                          control["admitted"]) or \
            not exact_int(declared_repair.get("secondDigestsUnderSupersededInstrument"),
                          control["secondDigests"]) or \
            not exact_int(declared_repair.get("admitThenRaiseUnderSupersededInstrument"),
                          control["admitThenRaise"]):
        findings.append(
            "EP9-LB-C2-01: the published battery counts are not this run's "
            f"measurement — measured cases={battery['cases']}, "
            f"rejectedByRepairedJoin={battery['rejected']}, "
            f"admittedByRepairedJoin={battery['admitted']}, "
            f"admittedBySupersededInstrument={control['admitted']}, "
            f"secondDigestsUnderSupersededInstrument={control['secondDigests']}, "
            f"admitThenRaiseUnderSupersededInstrument={control['admitThenRaise']}")

    # ---- the non-AST liveness counter -----------------------------------
    before = authority.c2v4_accesses
    c2_validate_intent(intents[0] if intents else {}, authority)
    if authority.c2v4_accesses <= before:
        findings.append("EP9-C2-LIVENESS: the join did not reach the verified C-2 v4 "
                        "module accessor; it is bound to some other instrument")

    # ---- AST tripwire, declared honestly --------------------------------
    scan = c2_join_scan()
    integers = integer_guard_scan()
    reach = selftest_reachability_scan()
    evasion = measured["evasion"]
    measurement["scan"] = scan
    measurement["integerGuardScan"] = integers
    measurement["selftestReachability"] = reach
    measurement["evasion"] = evasion
    if scan["referencesOutsideDeclaredClosure"]:
        findings.append("EP9-SCAN: a C-2 API is named outside the declared join "
                        f"closure: {scan['referencesOutsideDeclaredClosure'][0]}")
    if scan["unroutedSitesInsideJoin"]:
        findings.append("EP9-SCAN: a C-2 call inside the join does not route through "
                        f"the verified Authority accessor: "
                        f"{scan['unroutedSitesInsideJoin'][0]}")
    if not int_in_range(scan["authorityRoutedSites"], 3, INT64_MAX):
        findings.append(f"EP9-SCAN: only {scan['authorityRoutedSites']} authority-routed "
                        "C-2 call site(s) found; the scan cannot be distinguished from "
                        "a vacuous one")
    for site in integers["unguarded"]:
        findings.append("EP9-LB-C2-01-CLASS: a wire-sourced value is compared to a "
                        "numeric literal outside the declared guard helpers, which is "
                        f"exactly the defect this candidate re-pins away from: {site}")
    if integers["missingEntrypoints"]:
        findings.append("EP9-LB-C2-01-CLASS: the integer-guard scan cannot find "
                        f"validator entrypoint {integers['missingEntrypoints'][0]}")
    if not int_in_range(integers["guardHelperCallSites"], 8, INT64_MAX):
        findings.append(f"EP9-LB-C2-01-CLASS: the integer-guard scan found only "
                        f"{integers['guardHelperCallSites']} guard-helper call site(s), "
                        "so it cannot be distinguished from a vacuous scan")
    if not reach["hasSingleMain"]:
        findings.append("EP9-SELFTEST: this checker does not define exactly one main()")
    if reach["flags"] != sorted(DECLARED_FLAGS):
        findings.append(f"EP9-SELFTEST: command flag literals {reach['flags']} are not "
                        f"the declared entrypoint set {sorted(DECLARED_FLAGS)}")
    if not exact_int(reach["dispatchCount"], 1) or \
            not exact_int(reach["guardedDispatchCount"], reach["dispatchCount"]):
        findings.append(f"EP9-SELFTEST: main() dispatches to selftest() "
                        f"{reach['dispatchCount']} time(s), "
                        f"{reach['guardedDispatchCount']} flag-guarded; exactly one "
                        "flag-guarded dispatch is permitted")
    if not reach["dispatchBeforeFindingsReturn"]:
        findings.append("EP9-SELFTEST: main() can return on findings before reaching "
                        "the selftest suite — this is the evidence.v8 defect")
    if evasion["notLive"]:
        findings.append(f"EP9-SCAN: the evasion battery is not live: "
                        f"{evasion['notLive'][0]}")
    if evasion["missed"]:
        findings.append("EP9-SCAN: the behavioural layer failed to catch evasion "
                        f"variant(s) {evasion['missed']}; an AST scan would then be "
                        "the sole guard, which EV10-IR-01 proved insufficient")
    declared_scan = contract.get("astScanScope") or {}
    if not exact_int(declared_scan.get("evasionVariantsBuilt"), evasion["variants"]) or \
            not exact_int(declared_scan.get("missedBySyntacticScan"),
                          evasion["missedBySyntacticScan"]) or \
            not exact_int(declared_scan.get("detectedBySyntacticScan"),
                          evasion["detectedBySyntacticScan"]) or \
            not exact_int(declared_scan.get("caughtByBehaviouralLayer"),
                          evasion["caughtByBehaviouralLayer"]):
        findings.append(
            "EP9-SCAN: the published evasion measurement is not this run's — measured "
            f"variantsBuilt={evasion['variants']}, "
            f"detectedBySyntacticScan={evasion['detectedBySyntacticScan']}, "
            f"missedBySyntacticScan={evasion['missedBySyntacticScan']}, "
            f"caughtByBehaviouralLayer={evasion['caughtByBehaviouralLayer']}")
    if declared_scan.get("isSoleGuard") is not False or \
            "tripwire" not in declared_scan.get("declaredScope", "") or \
            declared_scan.get("loadBearingGuard") != "the LB-C2-01 behavioural battery " \
            "and the Authority.c2v4 access counter, neither of which reads source":
        findings.append("EP9-SCAN: astScanScope must declare the scan a tripwire that "
                        "is not the sole guard, and must name the load-bearing guard")

    # ---- measured scalar-leaf totality ----------------------------------
    surfaces = measured["surfaces"]
    root_census, root_stats = measure_contract_root(contract, authority, execute=False)
    measurement["surfaces"] = surfaces
    measurement["contractRoot"] = {"census": root_census, "stats": root_stats}
    authority.census = surfaces
    authority.measurement = measurement

    totality = contract.get("scalarLeafTotality") or {}
    declared_surfaces = totality.get("surfaces")
    if not isinstance(declared_surfaces, list) or {
            row.get("surface") for row in declared_surfaces if isinstance(row, dict)
    } != set(surfaces):
        findings.append("EP9-TOTALITY: the declared surface set is not the measured "
                        f"set {sorted(surfaces)}")
    else:
        for row in declared_surfaces:
            name = row.get("surface")
            census = surfaces[name]["census"]
            stats = surfaces[name]["stats"]
            for key in SURFACE_CENSUS_KEYS:
                if not exact_int(row.get(key), census.get(key)):
                    findings.append(
                        f"EP9-TOTALITY: {name} publishes {key}={row.get(key)!r}; this "
                        f"run measured {census.get(key)!r}")
            if not exact_int(row.get("executedCases"), stats["executedCases"]):
                findings.append(
                    f"EP9-TOTALITY: {name} publishes executedCases="
                    f"{row.get('executedCases')!r}; this run DROVE "
                    f"{stats['executedCases']} cases. The published number is the "
                    "count actually executed, never the count arithmetic predicts.")
            if row.get("rejectionMode") != SURFACE_REJECTION_MODE.get(name):
                findings.append(
                    f"EP9-TOTALITY: {name} publishes rejectionMode="
                    f"{row.get('rejectionMode')!r}; the layer's declared channel is "
                    f"{SURFACE_REJECTION_MODE.get(name)!r}, and without it "
                    "unguardedEscapes cannot be read correctly")
            if name == "evaluation-authority-candidate":
                measured_admissions = sorted(stats.get("admitted") or [])
                if row.get("admittedPositions") != measured_admissions:
                    findings.append(
                        "EP9-TOTALITY: the enumerated set of hostile candidates EP8's "
                        "public authorize_evaluation ADMITS is not the declared set; "
                        f"this run measured {measured_admissions}")
            if not exact_int(row.get("guardedEscapes"), stats["guardedEscapes"]) or \
                    not exact_int(row.get("unguardedEscapes"),
                                  stats["unguardedEscapes"]) or \
                    not exact_int(row.get("silentAccepts"), stats["silentAccepts"]):
                findings.append(
                    f"EP9-TOTALITY: {name} publishes guardedEscapes="
                    f"{row.get('guardedEscapes')!r}/unguardedEscapes="
                    f"{row.get('unguardedEscapes')!r}/silentAccepts="
                    f"{row.get('silentAccepts')!r}; this run measured "
                    f"{stats['guardedEscapes']}/{stats['unguardedEscapes']}/"
                    f"{stats['silentAccepts']}")
            if stats["guardedEscapes"]:
                findings.append(f"EP9-TOTALITY: {name} produced "
                                f"{stats['guardedEscapes']} traceback(s) through its "
                                "total boundary; hostile parsed JSON must yield findings")
            if not int_in_range(census.get("scalarLeafPaths"), 1, INT64_MAX):
                findings.append(f"EP9-TOTALITY: {name} reports no scalar leaf position, "
                                "so its claim quantifies over a region the instrument "
                                "cannot observe")
    declared_root = totality.get("contractRoot") or {}
    for key in SURFACE_CENSUS_KEYS:
        if not exact_int(declared_root.get(key), root_census.get(key)):
            findings.append(f"EP9-TOTALITY: contractRoot publishes {key}="
                            f"{declared_root.get(key)!r}; this run measured "
                            f"{root_census.get(key)!r}")
    if not int_in_range(root_census.get("scalarLeafPaths"), 1, INT64_MAX):
        findings.append("EP9-TOTALITY: the contract-root enumeration reaches no scalar "
                        "leaf position")
    if not exact_int(totality.get("injectionValues"), len(HOSTILE_VALUES)):
        findings.append(f"EP9-TOTALITY: the declared injection family size "
                        f"{totality.get('injectionValues')!r} is not the measured "
                        f"{len(HOSTILE_VALUES)}")
    if totality.get("domain") != "the root, every object key and every array index at " \
            "unlimited depth, CONTAINER AND SCALAR LEAF alike" or \
            "recomputed and compared on every run" not in totality.get("result", ""):
        findings.append("EP9-TOTALITY: the totality domain/result rule is not declared "
                        "verbatim")
    if "except the leaf-inclusive measurement layer" not in \
            totality.get("contractRootExecutionRule", ""):
        findings.append("EP9-TOTALITY: the contract-root execution window rule is not "
                        "declared")
    return findings


def check(contract, authority):
    """The total boundary.  Hostile parsed JSON yields findings, never tracebacks."""
    try:
        return _check(contract, authority)
    except RecursionError:
        return ["EP9-BOUNDARY: the contract root exceeded the traversal limit"]
    except MALFORMED as exc:
        return [f"EP9-BOUNDARY: the checking layer refused a malformed contract: "
                f"{type(exc).__name__}: {exc}"]


# --------------------------------------------------------------------------
# Section 7.  Mutations.  One per repair, proving each is load-bearing.
# --------------------------------------------------------------------------

def _mutate(contract, path, value):
    changed = copy.deepcopy(contract)
    try:
        assign(changed, path, value)
    except MALFORMED:
        return None
    return changed


def _drop(contract, path):
    changed = copy.deepcopy(contract)
    steps = _split(path)
    node = changed
    try:
        for _kind, step in steps[:-1]:
            node = node[step]
        if isinstance(node, list):
            del node[steps[-1][1]]
        else:
            node.pop(steps[-1][1], None)
    except MALFORMED:
        return None
    return changed


CONTRACT_MUTATIONS = (
    ("REP-EP9-1 re-pin the C-2 join onto the repaired bytes",
     lambda c: _mutate(c, "c2AuthorityJoin.checkerSha256", C2V3_CHECKER_SHA)),
    ("REP-EP9-1 point the join back at the defective contract",
     lambda c: _mutate(c, "c2AuthorityJoin.sourceArtifact", C2V3_CONTRACT)),
    ("REP-EP9-2 bring the whole delegation closure inside the window",
     lambda c: _drop(c, "delegationClosure.executables[0]")),
    ("REP-EP9-2 misstate a closure member digest",
     lambda c: _mutate(c, "delegationClosure.executables[0].sha256", "0" * 64)),
    ("REP-EP9-2 drop a pinned data record",
     lambda c: _drop(c, "delegationClosure.pinnedData[0]")),
    ("REP-EP9-3 prove the commitment unmoved by recomputation",
     lambda c: _mutate(c, "planIntentCommitmentStability.reproducedUnderSupersededEncoder", 0)),
    ("REP-EP9-3 move a committed planIntentCommitment",
     lambda c: _mutate(
         c, "positiveVectors[0].evaluationAuthorityCandidate.planAuthorityReceipt."
            "planIntentCommitment", "sha256:" + "5" * 64)),
    ("REP-EP9-4 publish MEASURED scalar-leaf totality",
     lambda c: _mutate(c, "scalarLeafTotality.surfaces[0].scalarLeafPaths", 0)),
    ("REP-EP9-4 understate the contract-root space",
     lambda c: _mutate(c, "scalarLeafTotality.contractRoot.enumeratedPaths", 1)),
    ("REP-EP9-5 refuse the AST scan as sole guard",
     lambda c: _mutate(c, "astScanScope.isSoleGuard", True)),
    ("REP-EP9-5 understate the measured evasion blind spot",
     lambda c: _mutate(c, "astScanScope.missedBySyntacticScan", 0)),
    ("REP-EP9-6 keep --selftest genuinely live",
     lambda c: _drop(c, "checkerModeContract.exitCodes[3]")),
    ("REP-EP9-7 keep the hostile-root boundary total",
     lambda c: _mutate(c, "scalarLeafTotality.domain", "containers only")),
    ("REP-EP9-8 stdlib only",
     lambda c: _mutate(c, "delegationClosure.verificationRule", "trust the filenames")),
    ("REP-EP9-9 one mutation per repair",
     lambda c: _drop(c, "repairMutations[0]")),
    ("posture: assurance may not exceed implementable-unexecuted",
     lambda c: _mutate(c, "assurance.evidenceGrade", "DEMONSTRATED")),
    ("posture: the candidate may not recommend a seal",
     lambda c: _mutate(c, "sealRecommendation", "SEAL")),
    ("inherited surface: an EP8 invariant may not be edited",
     lambda c: _mutate(c, "invariants[0].assert", "anything at all")),
    ("inherited surface: a v9 addition must be closed",
     lambda c: _mutate(c, "ep9UndeclaredTopLevelKey", 1)),
    ("RES-EP9-01 must remain stated, not absorbed",
     lambda c: _mutate(c, "c2AuthorityRepairJoin.ep6InnerJoinResidual", "closed")),
    ("the authorising review verdict may not be softened",
     lambda c: _mutate(c, "c2AuthorityRepairJoin.repairAuthorisedByBlockingFindingCount", 2)),
    ("the LB-C2-01 battery counts must be this run's measurement",
     lambda c: _mutate(c, "c2AuthorityRepairJoin.lbC201Battery.admittedBySupersededInstrument", 0)),
)


def _source_module(source, name):
    module = types.ModuleType(name)
    module.__dict__["__file__"] = str(HERE / (name + ".py"))
    exec(compile(source, name, "exec"), module.__dict__)
    return module


SOURCE_MUTATIONS = (
    ("narrow the leaf-inclusive enumeration back to containers only",
     "generator"),
    ("delete the type-distinct-one injection family",
     "injections"),
    ("bypass the Authority accessor and bind the join to the superseded module",
     "join"),
)


def run_source_mutations(contract, authority, report):
    """Prove the instrument itself is load-bearing, not decorative."""
    escaped = []
    intents = []
    for vector in contract.get("positiveVectors") or []:
        try:
            intent = vector["evaluationAuthorityCandidate"][
                "admittedResolvedInputs"]["frozenPlanIntent"]
        except MALFORMED:
            continue
        if intent not in intents:
            intents.append(intent)

    # (1) container-only enumeration must lose every scalar leaf and shrink
    wide = node_census(intents[0])
    narrow = node_census(intents[0], leaves=False)
    ok = narrow["scalarLeafPaths"] == 0 and wide["scalarLeafPaths"] > 0 and \
        narrow["enumeratedPaths"] < wide["enumeratedPaths"]
    if not ok:
        escaped.append("narrowing the generator to container positions did not shrink "
                       "the measured space")
    report(ok, SOURCE_MUTATIONS[0][0],
           f"leaf-inclusive reaches {wide['enumeratedPaths']} paths including "
           f"{wide['scalarLeafPaths']} scalar leaves; container-only reaches "
           f"{narrow['enumeratedPaths']} paths and {narrow['scalarLeafPaths']} "
           "scalar leaves")

    # (2) removing the type-distinct-one family must lose the LB-C2-01 signal
    reduced = tuple(row for row in HOSTILE_VALUES
                    if row[0] not in ("json-true-at-one", "json-float-one",
                                      "json-text-one"))
    v4 = authority.c2v4()
    c2_contract = authority.json(C2V4_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    _census, full_stats = drive_surface(
        intents[:1],
        lambda x: v4.validate_plan_intent(x, c2_contract, relations),
        lambda x: c2_validate_intent(x, authority),
        None, True, HOSTILE_VALUES)
    _census, reduced_stats = drive_surface(
        intents[:1],
        lambda x: v4.validate_plan_intent(x, c2_contract, relations),
        lambda x: c2_validate_intent(x, authority),
        None, True, reduced)
    ok = reduced_stats["executedCases"] < full_stats["executedCases"]
    if not ok:
        escaped.append("deleting the type-distinct-one injection family did not shrink "
                       "the executed space")
    report(ok, SOURCE_MUTATIONS[1][0],
           f"full family executes {full_stats['executedCases']} cases; without the "
           f"three type-distinct-one values it executes {reduced_stats['executedCases']}")

    # (3) a join bound to the superseded module must fail the battery
    class _SupersededAuthority:
        def __init__(self, inner):
            self._inner = inner
            self.c2v4_accesses = 0

        def json(self, name):
            # The superseded encoder is paired with the superseded contract.
            if name == C2V4_CONTRACT:
                return self._inner.json(C2V3_CONTRACT)
            return self._inner.json(name)

        def c2v4(self):
            self.c2v4_accesses += 1
            return self._inner.c2v3()

        def c2v3(self):
            return self._inner.c2v3()

    rewired = lb_c2_01_battery(intents, _SupersededAuthority(authority))
    ok = rewired["admitted"] > 0
    if not ok:
        escaped.append("a join rewired to the superseded instrument still passed the "
                       "LB-C2-01 battery, so the battery is not load-bearing")
    report(ok, SOURCE_MUTATIONS[2][0],
           f"the rewired join ADMITTED {rewired['admitted']} of {rewired['cases']} "
           f"type-distinct cases and produced {rewired['secondDigests']} second "
           f"digest(s) and {rewired['admitThenRaise']} admit-then-raise(s); the live "
           "join admits 0")
    return escaped


TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"), ("null", None), ("list", []), ("empty-object", {}),
    ("integer", 0), ("true", True), ("float", 1.5),
)


def selftest(contract, authority, path):
    """Always reaches the suite; refuses a dirty base with a distinct code."""
    base_findings = check(contract, authority)
    if base_findings:
        print("SELFTEST-REFUSED: the base candidate is not clean, so the mutation "
              "suite is not an oracle over it — every row would echo the pre-existing "
              "failure and report 'all rejected'.")
        print(f"  dirty base: {len(base_findings)} finding(s) in {path.name}")
        for finding in base_findings[:10]:
            print("  base-finding:", finding)
        if len(base_findings) > 10:
            print(f"  ... {len(base_findings) - 10} further base finding(s)")
        print(f"SELFTEST-NOT-RUN: 0 of "
              f"{len(CONTRACT_MUTATIONS) + len(SOURCE_MUTATIONS)} mutations executed. "
              "Exit 3 distinguishes this refusal from a green selftest (0), from "
              "ordinary findings (1) and from a bad invocation (2), and can never be "
              "absorbed into a pass.")
        return 3
    # Captured from the CLEAN base before any mutation runs: every later check()
    # call overwrites the live measurement with a mutated one.
    clean = authority.measurement or {}
    print(f"EP9 mutation self-test over {path.name} — each row must be REJECTED\n")
    escaped, rows = [], 0

    def report(rejected, name, detail):
        nonlocal rows
        rows += 1
        print(f"  {'reject' if rejected else 'ESCAPE':>6}  {name}")
        print(f"          {detail}")

    for label, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), authority)
        if not findings:
            escaped.append(f"parsed-JSON root {label}: NO FINDING")
        report(bool(findings), f"parsed-JSON contract root {label}",
               findings[0] if findings else "NO FINDING — root survived")

    for label, mutate in CONTRACT_MUTATIONS:
        changed = mutate(contract)
        if changed is None:
            escaped.append(f"{label}: mutation could not be applied")
            report(False, label, "NOT APPLICABLE — the mutation path is absent")
            continue
        findings = check(changed, authority)
        if not findings:
            escaped.append(f"{label}: NO FINDING")
        report(bool(findings), label,
               findings[0] if findings else "NO FINDING — mutation survived")

    escaped.extend(run_source_mutations(contract, authority, report))

    # The behavioural counterpart of integer_guard_scan.  This reads no source:
    # it injects the three type-distinct spellings at every integer and boolean
    # scalar leaf of the candidate and re-runs the complete checking layer.
    own = own_constant_leaf_battery(contract, authority)
    declared_own = (contract.get("astScanScope") or {}).get(
        "ownConstantLeafBattery") or {}
    own_ok = (exact_int(declared_own.get("intBoolLeaves"), own["intBoolLeaves"]) and
              exact_int(declared_own.get("excludedLeaves"), own["excludedLeaves"]) and
              declared_own.get("excludedPrefix") == OWN_BATTERY_EXCLUDED_PREFIX and
              exact_int(declared_own.get("cases"), own["cases"]) and
              exact_int(declared_own.get("rejected"), own["rejected"]) and
              exact_int(declared_own.get("silentlyAdmitted"),
                        own["silentlyAdmitted"]) and
              exact_int(declared_own.get("escapes"), own["escapes"]) and
              declared_own.get("silentlyAdmittedPositions") == own["admitted"])
    if own["escapes"]:
        escaped.append(f"own-constant-leaf battery: {own['escapes']} case(s) escaped "
                       "the total boundary as a traceback")
        own_ok = False
    if not own_ok:
        escaped.append(
            "own-constant-leaf battery: the published measurement is not this run's — "
            f"measured intBoolLeaves={own['intBoolLeaves']}, "
            f"excludedLeaves={own['excludedLeaves']}, cases={own['cases']}, "
            f"rejected={own['rejected']}, silentlyAdmitted={own['silentlyAdmitted']}, "
            f"escapes={own['escapes']}, positions={own['admitted']}")
    report(own_ok, "inject the type-distinct-one family at EVERY integer and boolean "
           "scalar leaf of the candidate and re-run the whole checking layer",
           f"{own['intBoolLeaves']} int/bool leaves driven ({own['excludedLeaves']} "
           f"under {OWN_BATTERY_EXCLUDED_PREFIX} excluded and covered by the "
           f"authority-candidate and contract-root matrices), {own['cases']} cases, "
           f"{own['rejected']} rejected, {own['silentlyAdmitted']} silently admitted "
           f"at {len(own['admitted'])} enumerated position(s), {own['escapes']} escapes")

    root_census, root_stats = measure_contract_root(contract, authority, execute=True)
    contract_ok = not root_stats["guardedEscapes"]
    if not contract_ok:
        escaped.append(f"contract-root matrix: {root_stats['guardedEscapes']} case(s) "
                       "escaped the guarded boundary as a traceback")
    report(contract_ok, "hostile parsed JSON at every contract-root position "
           "including scalar leaves",
           f"{root_stats['executedCases']} cases over {root_census['enumeratedPaths']} "
           f"paths ({root_census['scalarLeafPaths']} scalar leaves); "
           f"{root_stats['guardedEscapes']} guarded escapes over "
           f"{root_stats['guardedExercised']} guarded exercises (REQUIRED zero); "
           f"{root_stats['unguardedEscapes']} unguarded inner-reader raises "
           "(REPORTED, not required zero)")

    print()
    if escaped:
        for item in escaped:
            print("SELFTEST-FAIL:", item)
        print(f"{len(escaped)}/{rows} retained cases ESCAPED — the proof path is optional")
        return 1
    print(f"SELFTEST-PASS: all {rows} retained cases rejected — the proof path is "
          "load-bearing")
    for name in sorted(clean.get("surfaces") or {}):
        census = clean["surfaces"][name]["census"]
        stats = clean["surfaces"][name]["stats"]
        print(f"  {name}: {census['enumeratedPaths']} paths "
              f"({census['scalarLeafPaths']} scalar leaves, "
              f"{census['containerPaths']} containers), {stats['executedCases']} "
              f"executed cases, {stats['guardedEscapes']} guarded escapes, "
              f"{stats['unguardedEscapes']} unguarded escapes, "
              f"{stats['silentAccepts']} silent accepts")
    print(f"  contract-root: {root_census['enumeratedPaths']} paths "
          f"({root_census['scalarLeafPaths']} scalar leaves), "
          f"{root_stats['executedCases']} executed cases, "
          f"{root_stats['guardedEscapes']} guarded escapes over "
          f"{root_stats['guardedExercised']} guarded exercises")
    evasion = clean.get("evasion") or {}
    print(f"  AST tripwire blind spot MEASURED: {evasion.get('variants')} evasion "
          f"variants built, {evasion.get('missedBySyntacticScan')} missed by the "
          f"syntactic scan, {evasion.get('caughtByBehaviouralLayer')} caught by the "
          "independent behavioural layer")
    print("  scope: checker-scope evidence only; SPECIFIED / IMPLEMENTABLE_UNEXECUTED; "
          "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW; DO-NOT-SEAL; CD-RT-5 "
          "unsigned; independent re-review REQUIRED")
    return 0


# --------------------------------------------------------------------------
# Section 8.  Entrypoint.
# --------------------------------------------------------------------------

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
        raise UnsupportedInvocation("at most one artifact path may be supplied")
    return flags, (positional[0] if positional else None)


def main(argv):
    try:
        flags, requested = _parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"EP9-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    try:
        authority = load_authority()
    except AuthorityLoadError as exc:
        print(f"EP9-PINNED-INPUT-REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        contract = json.loads(path.read_text(), object_pairs_hook=_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"cannot load EP9 candidate {path}: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in flags:
        return selftest(contract, authority, path)
    findings = check(contract, authority)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for item in findings:
            print("  -", item)
        return 1
    measurement = authority.measurement or {}
    surfaces = measurement.get("surfaces") or {}
    root = (measurement.get("contractRoot") or {}).get("census") or {}
    stability = measurement.get("commitmentStability") or {}
    battery = (measurement.get("lbC201") or {}).get("repaired") or {}
    control = (measurement.get("lbC201") or {}).get("superseded") or {}
    evasion = measurement.get("evasion") or {}
    paths = sum(item["census"]["enumeratedPaths"] for item in surfaces.values())
    leaves = sum(item["census"]["scalarLeafPaths"] for item in surfaces.values())
    cases = sum(item["stats"]["executedCases"] for item in surfaces.values())

    vector = next(row for row in contract["positiveVectors"]
                  if row["id"] == contract["acceptedAuthorityVectorId"])
    ep8_module = authority.module(EP8)
    store = ep8_module._open_test_project_store(vector["trustedStoreFixture"])
    handle = ep8_module.resolve_stored_evaluation(
        store, vector["evaluationAuthorityCandidate"]["evaluationAuthorityAdmission"]
        ["evaluationAuthoritySealRef"])
    raw_rows = ep8_module.derive_raw_proof_requirements(vector["bundle"], handle)
    counts = {capability: sum(row["requiredForCapability"] == capability
                              for row in raw_rows)
              for capability in ("verifiable", "replayable")}

    print(f"EP9 contract OK — {path.name}; {len(contract['positiveVectors'])} cold-"
          f"reconstructed vectors; {len(raw_rows)} unchanged raw refs "
          f"({counts['verifiable']} verifiable/{counts['replayable']} replayable)")
    print(f"  delegation closure: {len(DELEGATION_CLOSURE)} executables + "
          f"{len(PINNED_DATA)} pinned data inputs + 1 superseded independent encoder, "
          "each read once, SHA-256 verified, then executed or parsed from that "
          "verified byte string")
    print(f"  C-2 join RE-PINNED onto {C2V4_CONTRACT} / {C2V4}; the three imported "
          "APIs verified against the repaired bytes")
    print(f"  planIntentCommitment UNMOVED: {stability.get('vectors')} vectors "
          f"recomputed under C-2 v4, {stability.get('reproducedUnderV3')} reproduced "
          f"under the superseded independent encoder, "
          f"{stability.get('preimageByteIdentical')} with BYTE-IDENTICAL preimages; "
          f"distinct commitments {stability.get('distinctCommitments')}")
    print(f"  LB-C2-01 battery: {battery.get('cases')} type-distinct cases; repaired "
          f"join admitted {battery.get('admitted')}; superseded instrument admitted "
          f"{control.get('admitted')} of the same cases "
          f"({control.get('secondDigests')} second digests, "
          f"{control.get('admitThenRaise')} admit-then-raise) — the control is not vacuous")
    print(f"  hostile parsed JSON at EVERY position including scalar leaves: {cases} "
          f"executed cases over {paths} enumerated wire-surface paths of which {leaves} "
          "are scalar leaves; 0 guarded escapes")
    print(f"  contract-root space measured at {root.get('enumeratedPaths')} paths of "
          f"which {root.get('scalarLeafPaths')} are scalar leaves; its execution matrix "
          "runs under --selftest")
    print(f"  AST tripwire blind spot MEASURED, not asserted: "
          f"{evasion.get('variants')} evasion variants built, "
          f"{evasion.get('missedBySyntacticScan')} missed by the syntactic scan, "
          f"{evasion.get('caughtByBehaviouralLayer')} caught by the independent "
          "behavioural layer")
    print("  RES-EP9-01: v9 does NOT repair check-evaluation-proof-v6.py; EP6's inner "
          "C-2 join still runs against the defective v3 bytes and v9 is a strictly "
          "stronger OUTER gate over it")
    print("  scope: checker-scope evidence only; SPECIFIED / IMPLEMENTABLE_UNEXECUTED; "
          "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW; DO-NOT-SEAL; CD-RT-5 "
          "unsigned; no seal, freeze, integration or product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
