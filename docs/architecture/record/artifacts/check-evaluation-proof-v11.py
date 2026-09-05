#!/usr/bin/env python3
"""check-evaluation-proof-v11.py — executable checker for evaluation-proof.v11.json.

v11 is the successor to evaluation-proof.v10.json, which an independent reviewer
REJECTED (ep10.review-independent.json, 1 blocking finding, IR-EP10-01).

============================================================================
THE ONE SENTENCE THAT MATTERS
============================================================================
v10's served-module ledger established WHICH MODULE WAS CALLED.  It did not
establish WHOSE ANSWER THE JOIN USED.  A call can be made, correctly argued and
faithfully recorded, and its result then thrown away.  v11 exists to establish
ANSWER PROVENANCE, and it keeps the call ledger only for what the call ledger
actually shows.

============================================================================
WHAT v11 DOES *NOT* CLAIM — read this before reading the green banner
============================================================================
RES-EP11-01  v11 does NOT repair check-evaluation-proof-v6.py, which is pinned by
             passed work and out of scope for edit.  EP6's INNER C-2 join still
             executes against the DEFECTIVE check-c2.py bytes underneath EP8.
             v11, like v10, is a strictly stronger OUTER gate over that join, not
             a replacement of its internals.  Carried forward unchanged from
             RES-EP10-01; closing it requires a v6 successor.

RES-EP11-02  The answer-provenance guard's declared hostile scope is THE ROUTE
             REGION: the three marked functions through which every C-2 call this
             checker makes for authority is spelled.  A mutation that instead
             rewrites the GUARD — that rebinds a module global the guard uses,
             walks the call stack with sys._getframe to read or (PEP 667) write
             the guard's own locals, or reaches the guard's private repaired
             instance through a wrapper's __closure__ — is instrument tampering,
             not routing, and is NOT closed by this instrument.  A source
             tripwire flags introspection primitives inside the route region and
             a behavioural probe re-checks every module-level binding across the
             drive, but a stack-walking mutation defeats both.  MEASURED, not
             argued: an AX6 frame-walking variant is built and executed on every
             ordinary run and its measured outcome is published, including when
             that outcome is ESCAPED.

RES-EP11-03  Answer provenance is established over the SEVEN PINNED VECTORS,
             which carry ONE distinct PlanIntent.  Over the 1656-case live census
             the join's answers are held only to VALUE equality with an
             independently computed repaired answer, not to object provenance and
             not to sentinel-flow dependence.  The strong property is measured at
             7 points, not everywhere.

RET-EP11-01  v10's repairs[REP-EP10-2] claim to clear IR-EP9-02 is RETRACTED AS
             FALSE.  Its six requirements quantify over CALLS RECORDED IN A
             WINDOW.  Every one of them is satisfiable by a join that calls the
             repaired module correctly and returns the superseded module's
             answer.  v11 rebuilds that evasion (AX2) and three further
             answer-substitution variants and measures them.

Usage:
    python3 -I -B check-evaluation-proof-v11.py [artifact.json]
    python3 -I -B check-evaluation-proof-v11.py --selftest

Exit codes, observed BEHAVIOURALLY in-process, not merely scanned:
    0  candidate accepted / selftest passed
    1  findings
    2  unsupported invocation or refused pinned input
    3  --selftest refused because the base candidate is already dirty
"""

from __future__ import annotations

import ast
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import secrets
import sys
import types
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evaluation-proof.v11.json"
EXPECTED_VERSION = 11
DECLARED_FLAGS = ("--selftest",)

MALFORMED = (TypeError, ValueError, KeyError, IndexError, AttributeError,
             ZeroDivisionError, OverflowError, RecursionError, UnicodeError,
             StopIteration)

EP10 = "check-evaluation-proof-v10.py"
EP8 = "check-evaluation-proof-v8.py"
EP7 = "check-evaluation-proof-v7.py"
EP6 = "check-evaluation-proof-v6.py"
EP5 = "check-evaluation-proof.py"
C2V4 = "check-c2-v4.py"
C2V3 = "check-c2.py"
RI = "check-resolved-inputs.py"

C2V4_CONTRACT = "c2-plan-stage-schema.v4.json"
C2V3_CONTRACT = "c2-plan-stage-schema.v3.json"
FACT_PLANE = "fact-plane.v1.json"
EP10_ARTIFACT = "evaluation-proof.v10.json"
EP10_REVIEW = "ep10.review-independent.json"
EP9_ARTIFACT = "evaluation-proof.v9.json"
EP9_REVIEW = "ep9.review-independent.json"
EP8_ARTIFACT = "evaluation-proof.v8.json"

C2_IMPORTED_APIS = ("validate_plan_intent", "plan_intent_commitment",
                    "canonical_plan_intent")

# --------------------------------------------------------------------------
# Recording obligation, IMPLEMENTATION-FREEZE 7.2: every input this verdict
# depends on is recorded by FILENAME AND SHA-256.  A count is not a record and a
# prose assertion is not a record.  Every digest below was recomputed on the live
# bytes; none was transcribed from a predecessor's table, and each is
# cross-checked against every predecessor pin table that exposes one.
# --------------------------------------------------------------------------

DELEGATED_CHECKER = {
    EP10: "0606eae06088df67bc6cc25cfcff520160cf75f9db47ebde73c4f8962e8e07b1",
}

DELEGATION_CLOSURE = {
    EP8: "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    EP7: "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4",
    EP6: "0a7ac122a598bb7b9454b1b3c46c586f6fd551a2a1ebcf5584665f875457c5f0",
    EP5: "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    C2V4: "54ff764d155f5582bc66fd7bf8138b7eaed5f90f46b92975c4bc7a85ffb3df17",
    "check-evidence.py": "6933d2931912a43e3018dc6037068230af0bbc0c0a00d5d9429c155930bde1af",
    "check-retention-custody.py":
        "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "check-d9.py": "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    "check-versioning.py":
        "67a45b275908afc4bd04cee6c15400f5d429f9f209854630c1caf5a43cf13227",
    RI: "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
}

SUPERSEDED_ENCODER = {
    C2V3: "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3",
}

PINNED_DATA = {
    EP10_ARTIFACT: "ba023d7eab2b9ed5f0aad49b103f77775b748dce1e706cfc46d4eee22b984cb8",
    EP10_REVIEW: "854c3defe17528ed237a3b1185ab61d1fc2a8e33ff9e282f631982a6235a8a55",
    EP9_ARTIFACT: "02f9955f4f90e91afd163a5fa8274eb8832aa5419221da7e9e825a1cbf17430b",
    EP9_REVIEW: "46b244235321c8a36549d0b92ebf843b1561ea6c37a5a7bcc49a498f7899c8cf",
    EP8_ARTIFACT: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    "evaluation-proof.v7.json":
        "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
    "evaluation-proof.v6.json":
        "74f35668afae2efb57070ff9a2897d373a91b42cc1cbbc87f3c673f872ca4bce",
    "evaluation-proof.v5.json":
        "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    C2V4_CONTRACT: "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    C2V3_CONTRACT: "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    "c2-plan-stage-schema.v4.review-independent-prefreeze.json":
        "c74612ef4519750aa529db543c2f0cc81fce50d57c3d636486fd2f0ddc0c41f3",
    "ep8-rt13.review-independent-cold-reconstruction.json":
        "f4599b32a9f1b93049111b9e86debd19419902c9c5f4fb886f8d0dc9c330567e",
    FACT_PLANE: "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "resolved-inputs.v2.json":
        "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "versioning-policy.v4.json":
        "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6",
}

ALL_PINS = {**DELEGATED_CHECKER, **DELEGATION_CLOSURE, **SUPERSEDED_ENCODER,
            **PINNED_DATA}

# The vector source is evaluation-proof.v8.json, which carries a PASSING
# independent review.  v9 and v10 are REJECTED, so v11 takes no vector authority
# from either; both are pinned, parsed, and v9 is required to AGREE with EP8.
VECTOR_SOURCE = EP8_ARTIFACT

# Re-entrancy depth for the in-process behavioural probes.
_NESTED = [0]


class DuplicateKeyError(ValueError):
    pass


class AuthorityLoadError(RuntimeError):
    pass


class UnsupportedInvocation(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def value_fingerprint(value) -> str | None:
    try:
        return sha_bytes(canonical(value))
    except MALFORMED:
        return None


def strict_equal(left, right) -> bool:
    """Recursive TYPE-EXACT equality over host values.

    Plain `==` is exactly the LB-C2-01 defect this chain exists to measure:
    True == 1 and 1.0 == 1 in the host language.  Every published-versus-measured
    and every expected-versus-actual comparison in this checker goes through
    here, so no answer can be accepted because it happens to compare equal to a
    value of a different type.
    """
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            strict_equal(left[key], right[key]) for key in left)
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(
            strict_equal(a, b) for a, b in zip(left, right))
    return left == right


# --------------------------------------------------------------------------
# Section 0.  Trust order.
#
# Every transitive input is read ONCE as inert bytes, SHA-256 verified against
# the pin table above, and thereafter executed or parsed EXCLUSIVELY from that
# verified in-memory byte string.  There is no second disk read between
# verification and execution for anything v11 loads.
#
# Stated so the rule is not over-read, because two predecessors do re-read:
#   * check-evaluation-proof-v10.py's own _own_source() would re-open its own
#     path to feed its AST scans and its evasion battery.  v11 seeds that cache
#     with the VERIFIED bytes before any of it runs, so the delegate never
#     re-reads either.  This is enforced and measured (delegateSourceCacheSeeded).
#   * EP6.admit_evaluation_authority re-reads c2-plan-stage-schema.v3.json and
#     fact-plane.v1.json on every call, and EP8._ep7 sha_file()-verifies then
#     loads from disk.  Both hash-verify what they re-read, so the trust order
#     holds transitively, but the guarantee v11 makes is about what v11 loads.
# --------------------------------------------------------------------------

_MODULE_SERIAL = [0]


class _VerifiedSourceLoader:
    """Executes a module from a verified byte string; never reopens the path."""

    def __init__(self, filename: str, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, spec):  # noqa: D401 - importlib protocol
        return None

    def exec_module(self, module):
        code = compile(self.source, str(HERE / self.filename), "exec",
                       dont_inherit=True)
        exec(code, module.__dict__)  # noqa: S102 - verified bytes only


def _exec_verified(filename: str, source: bytes, prefix: str = "_ep11"):
    _MODULE_SERIAL[0] += 1
    name = f"{prefix}_{_MODULE_SERIAL[0]}_{re.sub(r'[^0-9a-zA-Z]', '_', filename)}"
    loader = _VerifiedSourceLoader(filename, source)
    spec = importlib.util.spec_from_file_location(
        name, str(HERE / filename), loader=loader)
    if spec is None:
        raise AuthorityLoadError(f"cannot build a verified spec for {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001
        raise AuthorityLoadError(
            f"pinned executable {filename} failed to execute from its verified "
            f"bytes: {type(exc).__name__}: {exc}") from exc
    return module


def load_snapshots(directory: pathlib.Path = HERE) -> dict[str, bytes]:
    snapshots: dict[str, bytes] = {}
    for name, expected in ALL_PINS.items():
        try:
            data = (directory / name).read_bytes()
        except OSError as exc:
            raise AuthorityLoadError(f"pinned input {name} unreadable: {exc}") from exc
        actual = sha_bytes(data)
        if actual != expected:
            raise AuthorityLoadError(
                f"pinned input {name} is {actual}, pinned at {expected}; refusing "
                "to execute or parse an input this candidate does not pin")
        snapshots[name] = data
    return snapshots


# --------------------------------------------------------------------------
# Section 1.  Delegation to the REJECTED predecessor's verified bytes.
#
# ep10.review-independent.json UPHELD, by independent re-execution, v10's
# two-regime admitted-set measurement, its admissionDescriptor finding, its
# producer-consistency rejection of the manifest and seal, its differential
# oracle including the finding that the prior review's own recommended remedy
# would not have sufficed, its distinct-intent family, its probe family and its
# call ledger's catch of R1 and R4.  v11 must not regress or rebuild any of
# them, so it does neither: it hash-verifies check-evaluation-proof-v10.py and
# EXECUTES the reviewer-verified measurement functions from that verified
# snapshot.  Nothing is transcribed.  The numbers in this run are produced by
# the same bytes the reviewer re-derived independently, and the pinned v10
# candidate is additionally driven through v10's OWN checking layer here and
# required to produce zero findings, which is what makes "preserved" a
# measurement rather than a promise.
# --------------------------------------------------------------------------

def load_delegate(snapshots: dict[str, bytes]):
    delegate = _exec_verified(EP10, snapshots[EP10], prefix="_ep11_delegate")
    # Trust order: the delegate's self-scan cache is seeded with the VERIFIED
    # bytes so its AST scans and its evasion battery never re-open the path.
    delegate._SCAN_CACHE["source"] = snapshots[EP10]
    delegate._SCAN_CACHE["tree"] = ast.parse(snapshots[EP10])
    return delegate


def delegate_source_is_sealed(delegate, snapshots) -> bool:
    """MEASURED: the delegate's self-source cache holds the verified bytes."""
    return delegate._SCAN_CACHE.get("source") == snapshots[EP10]


class Authority:
    """v11's authority: the delegate's Authority plus v11's own verified bytes.

    The route region receives THIS object.  It deliberately does NOT carry the
    guard's private repaired instance, and it does not carry v11's snapshot
    dictionary; both are threaded to the guards by parameter so that the only
    way the route region could reach them is stack or global introspection,
    which is the declared blind spot RES-EP11-02.
    """

    def __init__(self, snapshots, delegate, inner, parsed):
        self._snapshots = snapshots
        self.delegate = delegate
        self.inner = inner
        self.parsed = parsed
        self.ledger = inner.ledger
        self.modules = inner.modules
        self.cache: dict[str, Any] = {}
        self.measurement: dict[str, Any] = {}

    def json(self, name):
        if name in self.parsed:
            return self.parsed[name]
        return self.inner.json(name)

    def module(self, name):
        return self.inner.module(name)

    def c2v4(self):
        """The declared route to the repaired C-2 instrument."""
        return self.inner.c2v4()

    def c2v3(self):
        """The superseded encoder, admitted only as an independent cross-check."""
        return self.inner.c2v3()


def build_authority(snapshots: dict[str, bytes]) -> Authority:
    delegate = load_delegate(snapshots)
    inner_snapshots = {name: snapshots[name] for name in delegate.ALL_PINS}
    inner = delegate.build_authority(inner_snapshots)
    parsed: dict[str, Any] = {}
    for name in PINNED_DATA:
        if name in delegate.PINNED_DATA:
            continue
        try:
            parsed[name] = json.loads(snapshots[name].decode("utf-8"),
                                      object_pairs_hook=_pairs)
        except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
            raise AuthorityLoadError(
                f"pinned data {name} is not parseable JSON: "
                f"{type(exc).__name__}: {exc}") from exc
    return Authority(snapshots, delegate, inner, parsed)


def load_authority(directory: pathlib.Path = HERE) -> Authority:
    return build_authority(load_snapshots(directory))


# --------------------------------------------------------------------------
# Section 2.  The C-2 v4 authority join.
#
# Every C-2 call this checker makes FOR AUTHORITY is spelled inside the marked
# region below, and the evasion battery rewrites exactly that region.
#
# ONE DIFFERENCE FROM v10 THAT IS LOAD-BEARING: each function returns the
# repaired module's OWN result object rather than a fresh copy of it.  v10 wrote
# `return list(authority.c2v4().validate_plan_intent(...))`, and that `list()`
# is why v10's provenance rule could only ever cover the commitment: the object
# the join returned was never the object the module produced.  Totality is
# preserved by the boundary handler, not by copying.
# --------------------------------------------------------------------------

# ROUTE-REGION-BEGIN

def c2_validate_intent(intent, authority):
    """Total.  Returns the repaired module's own findings list; never raises."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        return authority.c2v4().validate_plan_intent(
            intent, contract, set(relations))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY",
                 f"C-2 v4 validation boundary: {type(exc).__name__}: {exc}")]


def c2_commit_intent(intent, authority):
    """Total.  Returns (commitment-or-None, findings); never raises."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().plan_intent_commitment(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "PlanIntent admitted by validation cannot be "
                                 f"canonically encoded: {type(exc).__name__}: {exc}")]


def c2_canonical_intent(intent, authority):
    """Total.  Returns (preimage-or-None, findings); never raises."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().canonical_plan_intent(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "PlanIntent cannot be canonically encoded: "
                                 f"{type(exc).__name__}: {exc}")]

# ROUTE-REGION-END


C2_JOIN_CLOSURE = ("c2_validate_intent", "c2_commit_intent", "c2_canonical_intent")
# Functions permitted to name a C-2 API for MEASUREMENT.  These take no authority
# from the call: they are the guard's independent recomputation, the unguarded
# control side of a matrix, or the differential oracle.
C2_MEASUREMENT_CLOSURE = ("answer_provenance_guard", "plan_intent_surface",
                          "distinct_answer_probe", "c2_api_surface",
                          "_sentinel_for")


def c2_join(intent, authority):
    """The complete v11 authority join over one PlanIntent.

    Returns the three values the checker ACTS ON, always, including when the
    verdict is a rejection.  v10 returned (None, findings, None) on any finding,
    which is correct behaviour but leaves the verdict — the value the accept /
    reject decision IS — outside anything a provenance rule could bind.
    """
    verdict = c2_validate_intent(intent, authority)
    if verdict:
        return {"verdict": verdict, "commitment": None, "preimage": None,
                "gate": "REJECT"}
    commitment, commit_errors = c2_commit_intent(intent, authority)
    if commit_errors:
        return {"verdict": commit_errors, "commitment": None, "preimage": None,
                "gate": "REJECT"}
    preimage, canonical_errors = c2_canonical_intent(intent, authority)
    if canonical_errors:
        return {"verdict": canonical_errors, "commitment": None, "preimage": None,
                "gate": "REJECT"}
    return {"verdict": verdict, "commitment": commitment, "preimage": preimage,
            "gate": "ACCEPT"}


ANSWER_KEYS = (("validate_plan_intent", "verdict"),
               ("plan_intent_commitment", "commitment"),
               ("canonical_plan_intent", "preimage"))


def c2_api_surface(authority) -> list[str]:
    findings: list[str] = []
    module = authority.c2v4()
    for name in C2_IMPORTED_APIS:
        function = getattr(module, name, None)
        if function is None or not callable(function):
            findings.append(f"EP11-C2-API: {C2V4} does not expose a callable {name}")
            continue
        original = authority.ledger.originals.get((C2V4, name), function)
        try:
            arity = original.__code__.co_argcount
        except AttributeError:
            findings.append(f"EP11-C2-API: {name} in {C2V4} is not a plain function")
            continue
        expected = 3 if name == "validate_plan_intent" else 2
        if arity != expected:
            findings.append(f"EP11-C2-API: {C2V4}.{name} takes {arity} positional "
                            f"parameters; the imported seam requires {expected}")
    return findings


# --------------------------------------------------------------------------
# Section 3.  CALL provenance — v10's ledger rules, restated for what they show.
#
# These are v10's R-1..R-6 in v11's own spelling, driving v11's route region.
# They are RETAINED because they are real and they catch a real family: a join
# that reaches C-2 by a route the ledger cannot observe, one that is served by
# the superseded module, one whose calls are not bound to this vector's
# argument, one that is only partly re-pinned.
#
# WHAT THEY ESTABLISH, stated plainly and not one word more: that the calls the
# join MADE for each pinned vector went into the repaired module.  They do NOT
# establish that the value the join RETURNED came out of it.  A call can be made
# correctly and its result discarded; that is evasion AX2 and every one of these
# six rules is green while it runs.  Answer provenance is Section 4's job.
# --------------------------------------------------------------------------

def call_provenance_guard(named_intents, authority):
    findings: list[str] = []
    rows: list[dict[str, Any]] = []
    observed: set[str] = set()
    superseded_calls = 0
    total_calls = 0

    for vector_id, intent in named_intents:
        want = value_fingerprint(intent)
        with authority.ledger.window(f"authority-join:{vector_id}") as window:
            answer = c2_join(intent, authority)
        entries = window.entries
        outer = [call for call in entries if call.depth == 0]
        tags = sorted({call.tag for call in entries})
        apis = sorted({call.api for call in outer})
        mismatched = [call for call in outer if call.argfp != want]
        total_calls += len(entries)
        superseded_calls += sum(1 for call in entries if call.tag != C2V4)
        observed.update(call.argfp for call in outer if call.argfp)

        if not entries:
            findings.append(
                f"EP11-CALL: vector {vector_id} produced ZERO observed C-2 calls; "
                "the authority join reached a C-2 API by a route the served-module "
                "ledger cannot observe, or made no call at all")
        if tags and tags != [C2V4]:
            findings.append(
                f"EP11-CALL: vector {vector_id}'s authority join was served by "
                f"{tags}; the C-2 join is re-pinned onto {C2V4} and EVERY call for "
                "a pinned vector must be served by the repaired module")
        if mismatched:
            findings.append(
                f"EP11-CALL: vector {vector_id} observed {len(mismatched)} depth-0 "
                "C-2 call(s) over an argument that is NOT this vector's PlanIntent")
        if entries and apis != sorted(C2_IMPORTED_APIS):
            findings.append(
                f"EP11-CALL: vector {vector_id} exercised depth-0 APIs {apis}; all "
                f"three of {sorted(C2_IMPORTED_APIS)} must be served for every "
                "pinned vector or the join is only partly re-pinned")
        if answer["gate"] != "ACCEPT":
            findings.append(
                "EP11-STABILITY: the C-2 join does not accept pinned vector "
                f"{vector_id}: {answer['verdict'][:1]}")
        rows.append({"vectorId": vector_id, "observedCalls": len(entries),
                     "depthZeroCalls": len(outer), "servedBy": tags, "apis": apis,
                     "argumentBound": not mismatched, "gate": answer["gate"]})

    driven = {value_fingerprint(intent) for _id, intent in named_intents}
    if len(observed) != len(driven):
        findings.append(
            f"EP11-CALL: {len(observed)} distinct PlanIntent fingerprint(s) were "
            f"observed at depth 0, but the driven vectors carry {len(driven)}")
    if superseded_calls:
        findings.append(f"EP11-CALL: {superseded_calls} superseded-module call(s) "
                        "occurred inside an authority-join window")

    return findings, {
        "vectorsDriven": len(named_intents),
        "distinctIntentsDriven": len(driven),
        "observedCalls": total_calls,
        "depthZeroCalls": sum(row["depthZeroCalls"] for row in rows),
        "distinctFingerprintsObserved": len(observed),
        "supersededCallsInsideJoin": superseded_calls,
        "allCallsServedByRepaired": superseded_calls == 0 and total_calls > 0,
        "rows": rows,
    }


# --------------------------------------------------------------------------
# Section 4.  ANSWER provenance — the repair of IR-EP10-01.
#
# THE PROPERTY: for every pinned vector, each of the three values the join
# returns and the checker acts on — the VALIDATION VERDICT above all, because
# c2_join's accept / reject gate IS that value and LB-C2-01 lives exactly
# there — is the value the REPAIRED module produced for THAT PlanIntent.
#
# Four rules, each stating what it establishes and what it does not:
#
#   A-1  INDEPENDENT VALUE.  The guard exec's check-c2-v4.py a SECOND time, from
#        the verified byte snapshot, into a module object created inside this
#        function and held only in its frame.  That instance is never installed
#        in the ledger, never stored on the Authority, never bound to a module
#        global and never passed to the route region.  Its answers over a private
#        deep copy of the vector's PlanIntent, a private parse of the pinned
#        contract and a private relation set must equal the join's, TYPE-EXACTLY.
#        Establishes: the VALUE is the repaired module's value.
#        Does not establish: that the value came FROM it.  Two modules that agree
#        on an input satisfy A-1 either way — which is precisely why v10's
#        differential oracle, an A-1-shaped instrument, missed AX2.
#
#   A-2  RETURNED-OBJECT PROVENANCE.  Each returned value must BE, by object
#        identity, the result object of a ledger entry recorded in THIS vector's
#        window, at depth 0, against the REPAIRED tag, for the SAME api, over
#        THIS vector's PlanIntent fingerprint.  v10's R-5 did this for the
#        commitment alone; here it covers the verdict and the canonical preimage
#        as well, which is what the route region returning the module's own
#        object rather than a copy of it makes possible.
#        Establishes: the object returned is the object the repaired module made
#        for this input.  A join that calls and discards returns a foreign
#        object and fails here.
#        Does not establish: anything about a forged ledger entry — see A-3.
#
#   A-3  SENTINEL FLOW, repaired module poisoned.  Every reachable spelling of
#        the repaired module's api — the module attribute AND the ledger's own
#        unwrapped original — is replaced by a function returning a per-run
#        UNPREDICTABLE sentinel, and the join is driven again.  The value the
#        join returns must BECOME the sentinel.
#        Establishes: CAUSAL DEPENDENCE.  The answer flows from the repaired
#        module.  This is the rule a decoy call cannot satisfy: AX2 calls the
#        poisoned api, throws the sentinel away, and returns the superseded
#        module's real answer, which is not the sentinel.  It trusts no record,
#        so no forged ledger entry helps.
#        Does not establish: dependence for inputs other than the pinned vectors.
#
#   A-4  SENTINEL FLOW, superseded module poisoned.  Symmetrically, every
#        reachable spelling of the SUPERSEDED module's api is sentinel-poisoned
#        and the join driven again.  The value must be UNCHANGED and must still
#        equal A-1's independent value.
#        Establishes: NON-dependence on the superseded module.  A join that
#        returns v3's answer returns the sentinel here.
#
#   A-5  THE GATE.  The verdict is measured as its own value for every vector and
#        the accept / reject gate is required to be the gate the independent
#        instance computes.  Stated separately because c2_join returns early on
#        any finding, so a verdict substitution decides admission by itself.
#
#   A-6  AGGREGATE, measured and published: vectors covered, apis covered per
#        vector, and the counts for each rule.  Zero exceptions are permitted to
#        pass as a silent success: a rule that could not be evaluated is a
#        finding, not an omission.
#
# WHAT NONE OF THIS ESTABLISHES.  Provenance is not correctness: if
# check-c2-v4.py is itself wrong, A-1..A-5 certify that its wrong answer is
# faithfully the one used.  And the whole section models a hostile ROUTE REGION,
# not a hostile guard; see RES-EP11-02, which is measured by variant AX6.
# --------------------------------------------------------------------------

def _private_repaired(snapshots):
    """A second, private instance of the repaired module from verified bytes.

    Re-verified here rather than trusted: if the snapshot the guard was handed
    does not hash to the pin, the guard refuses instead of measuring against
    whatever it was given.
    """
    source = snapshots[C2V4]
    if sha_bytes(source) != ALL_PINS[C2V4]:
        raise AuthorityLoadError(
            f"the repaired module bytes handed to the answer-provenance guard "
            f"hash to {sha_bytes(source)}, pinned at {ALL_PINS[C2V4]}")
    return _exec_verified(C2V4, source, prefix="_ep11_private")


class _Witness:
    """A PRIVATE record of which module produced which object.

    Deliberately NOT the shared served-module ledger.  The shared ledger's
    `entries` list and `_provenance` map are reachable through the Authority the
    route region is handed, so a route region can append an entry claiming the
    repaired module produced an object it never saw and set the provenance map to
    match.  v11 builds exactly that (variant forged-ledger-entry-replay) and it
    satisfies v10's R-5.  This record is created inside answer_provenance_guard,
    is bound to no global and to no attribute of anything the route region
    receives, and is reachable only through the installed wrapper's __closure__ —
    which the route-region introspection tripwire names, and which variants AX6
    and AX9 use to demonstrate that the tripwire is then the only guard left.
    """

    __slots__ = ("produced", "depth")

    def __init__(self):
        self.produced: dict[int, tuple] = {}
        self.depth = 0


def _witness_wrapper(witness, inner, tag, api):
    def observed(*args, **kwargs):
        depth = witness.depth
        witness.depth += 1
        try:
            result = inner(*args, **kwargs)
        finally:
            witness.depth -= 1
        # The result object is retained in the record, so its id cannot be
        # recycled by a later allocation while the record still names it.
        witness.produced[id(result)] = (
            tag, api, value_fingerprint(args[0]) if args else None, depth, result)
        return result
    return observed


@contextlib.contextmanager
def _witnessing(witness, tagged_modules):
    saved = []
    for tag, module in tagged_modules:
        for api in C2_IMPORTED_APIS:
            current = getattr(module, api, None)
            if current is None or not callable(current):
                continue
            saved.append((module, api, current))
            setattr(module, api, _witness_wrapper(witness, current, tag, api))
    try:
        yield
    finally:
        for module, api, original in saved:
            setattr(module, api, original)


def _sentinel_for(api: str, token: str):
    """A value of the api's own shape that the repaired module cannot produce."""
    if api == "validate_plan_intent":
        return [("EP11-SENTINEL", token)]
    if api == "plan_intent_commitment":
        return "sha256:" + token
    return b"EP11-SENTINEL\x00" + token.encode("utf-8")


@contextlib.contextmanager
def _poisoned(module, ledger, tag, api, value):
    """Replace EVERY reachable spelling of module.api for the duration."""
    def sentinel(*_args, **_kwargs):
        return value

    saved_attribute = getattr(module, api)
    had_original = (tag, api) in ledger.originals
    saved_original = ledger.originals.get((tag, api))
    setattr(module, api, sentinel)
    if had_original:
        ledger.originals[(tag, api)] = sentinel
    try:
        yield
    finally:
        setattr(module, api, saved_attribute)
        if had_original:
            ledger.originals[(tag, api)] = saved_original


def answer_provenance_guard(named_intents, authority, snapshots):
    findings: list[str] = []
    rows: list[dict[str, Any]] = []
    counts = {"vectors": 0, "apisPerVector": len(ANSWER_KEYS),
              "independentValueAgreements": 0, "objectProvenanceAgreements": 0,
              "sharedLedgerAgreements": 0,
              "repairedSentinelFlowed": 0, "supersededSentinelIgnored": 0,
              "gateAgreements": 0, "evaluationErrors": 0}
    try:
        private = _private_repaired(snapshots)
        contract = json.loads(snapshots[C2V4_CONTRACT].decode("utf-8"),
                              object_pairs_hook=_pairs)
        relations = set(json.loads(snapshots[FACT_PLANE].decode("utf-8"),
                                   object_pairs_hook=_pairs)
                        ["relationRegistry"]["relations"])
    except (AuthorityLoadError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError, *MALFORMED) as exc:
        return ([f"EP11-ANSWER: the guard could not build its independent "
                 f"repaired instance: {type(exc).__name__}: {exc}"], counts, rows)

    repaired_module = authority.module(C2V4)
    superseded_module = authority.module(C2V3)
    ledger = authority.ledger
    witness = _Witness()
    tagged = [(C2V4, repaired_module), (C2V3, superseded_module)]

    for vector_id, intent in named_intents:
        counts["vectors"] += 1
        want = value_fingerprint(intent)
        subject = copy.deepcopy(intent)

        with ledger.window(f"answer-provenance:{vector_id}") as window:
            with _witnessing(witness, tagged):
                answer = c2_join(intent, authority)
        entries = window.entries

        # A-1.  Computed AFTER the drive, on the private instance, from private
        # copies.  Nothing the route region can reach carries this value while
        # the route region is running, because it does not exist yet.
        try:
            expected = {
                "verdict": private.validate_plan_intent(
                    subject, copy.deepcopy(contract), set(relations)),
                "commitment": private.plan_intent_commitment(
                    subject, copy.deepcopy(contract)),
                "preimage": private.canonical_plan_intent(
                    subject, copy.deepcopy(contract)),
            }
        except MALFORMED as exc:
            counts["evaluationErrors"] += 1
            findings.append(
                f"EP11-ANSWER: the independent repaired instance raised on pinned "
                f"vector {vector_id}: {type(exc).__name__}: {exc}")
            continue
        expected_gate = "ACCEPT" if not expected["verdict"] else "REJECT"

        row = {"vectorId": vector_id, "gate": answer["gate"],
               "expectedGate": expected_gate, "perApi": {}}

        # A-5, stated first because it is the one that decides admission.
        if answer["gate"] != expected_gate:
            findings.append(
                f"EP11-ANSWER: vector {vector_id} the join's accept/reject GATE is "
                f"{answer['gate']}; the independently computed repaired instance "
                f"decides {expected_gate}. The gate IS the validation verdict, and "
                "LB-C2-01 lives exactly there")
        else:
            counts["gateAgreements"] += 1
        if expected_gate != "ACCEPT":
            findings.append(
                "EP11-STABILITY: the repaired C-2 instrument does not accept pinned "
                f"vector {vector_id}")

        for api, key in ANSWER_KEYS:
            actual = answer[key]
            token = secrets.token_hex(16)
            sentinel = _sentinel_for(api, token)
            per = {}

            # A-1 independent value.
            per["independentValue"] = strict_equal(actual, expected[key])
            if per["independentValue"]:
                counts["independentValueAgreements"] += 1
            else:
                findings.append(
                    f"EP11-ANSWER: vector {vector_id} {key}: the value the join "
                    "returned is not the value the independent repaired instance "
                    "computed for this PlanIntent (A-1)")

            # A-2 returned-object provenance, against the guard's PRIVATE
            # witness.  The shared ledger's agreement is measured beside it and
            # published, but it is NOT what A-2 tests: the shared ledger is
            # reachable from the route region and can be told a call happened
            # that did not.
            witnessed = (witness.produced.get(id(actual))
                         if actual is not None else None)
            per["objectProvenance"] = bool(
                witnessed and witnessed[0] == C2V4 and witnessed[1] == api
                and witnessed[2] == want and witnessed[3] == 0
                and witnessed[4] is actual)
            per["sharedLedgerAgrees"] = actual is not None and any(
                entry.tag == C2V4 and entry.depth == 0 and entry.api == api
                and entry.argfp == want and entry.result is actual
                for entry in entries)
            if per["sharedLedgerAgrees"]:
                counts["sharedLedgerAgreements"] += 1
            if per["objectProvenance"]:
                counts["objectProvenanceAgreements"] += 1
            else:
                findings.append(
                    f"EP11-ANSWER: vector {vector_id} {key}: the object the join "
                    f"returned is not an object {C2V4} produced for this vector's "
                    "PlanIntent at depth 0 in this window (A-2), as recorded by the "
                    "guard's PRIVATE witness; a call whose result is discarded "
                    "fails here, and a forged ledger entry does not help")

            # A-3 sentinel flow: the repaired module is poisoned and the answer
            # must follow it.
            try:
                with _poisoned(repaired_module, ledger, C2V4, api, sentinel):
                    poisoned_answer = c2_join(intent, authority)
                per["repairedSentinelFlowed"] = strict_equal(
                    poisoned_answer[key], sentinel)
            except Exception as exc:  # noqa: BLE001
                counts["evaluationErrors"] += 1
                per["repairedSentinelFlowed"] = False
                findings.append(f"EP11-ANSWER: vector {vector_id} {key}: A-3 could "
                                f"not be evaluated: {type(exc).__name__}: {exc}")
            if per["repairedSentinelFlowed"]:
                counts["repairedSentinelFlowed"] += 1
            else:
                findings.append(
                    f"EP11-ANSWER: vector {vector_id} {key}: with EVERY reachable "
                    f"spelling of {C2V4}.{api} replaced by a sentinel, the join "
                    "still returned an answer that is not the sentinel (A-3); the "
                    "answer does not FLOW FROM the repaired module, whatever the "
                    "call ledger recorded")

            # A-4 the superseded module is poisoned and the answer must not move.
            try:
                with _poisoned(superseded_module, ledger, C2V3, api,
                               _sentinel_for(api, secrets.token_hex(16))):
                    unaffected = c2_join(intent, authority)
                per["supersededSentinelIgnored"] = strict_equal(
                    unaffected[key], expected[key])
            except Exception as exc:  # noqa: BLE001
                counts["evaluationErrors"] += 1
                per["supersededSentinelIgnored"] = False
                findings.append(f"EP11-ANSWER: vector {vector_id} {key}: A-4 could "
                                f"not be evaluated: {type(exc).__name__}: {exc}")
            if per["supersededSentinelIgnored"]:
                counts["supersededSentinelIgnored"] += 1
            else:
                findings.append(
                    f"EP11-ANSWER: vector {vector_id} {key}: with every reachable "
                    f"spelling of {C2V3}.{api} replaced by a sentinel, the join's "
                    "answer CHANGED (A-4); the answer flows from the superseded "
                    "module")
            row["perApi"][key] = per
        rows.append(row)

    if counts["evaluationErrors"]:
        findings.append(f"EP11-ANSWER: {counts['evaluationErrors']} answer-"
                        "provenance rule(s) could not be evaluated; an unevaluated "
                        "rule is a finding, not an omission")
    expected_total = counts["vectors"] * len(ANSWER_KEYS)
    counts["expectedPerRuleTotal"] = expected_total
    counts["allRulesHeld"] = (
        expected_total > 0
        and counts["independentValueAgreements"] == expected_total
        and counts["objectProvenanceAgreements"] == expected_total
        and counts["repairedSentinelFlowed"] == expected_total
        and counts["supersededSentinelIgnored"] == expected_total
        and counts["gateAgreements"] == counts["vectors"]
        and not counts["evaluationErrors"])
    return findings, counts, rows


# --------------------------------------------------------------------------
# Section 5.  The differential oracle over the live census, RETAINED.
#
# v10's oracle is preserved by delegation and its numbers are republished.  This
# is v11's own instrument over v11's join, and it does two jobs v10's could not:
#   * it computes the repaired answer on the guard's PRIVATE instance rather
#     than through the Authority, so a route region that poisons the reachable
#     module cannot poison the oracle's reference answer as well; and
#   * it ENUMERATES the silently-accepted positions instead of counting them.
#     IR-EP10-NB-03: a count is not a record, and this candidate's own recording
#     obligation says so.
#
# It remains NOT SUFFICIENT ALONE and that is measured, not conceded: its
# discriminating cardinality on this census is published, and the evasion matrix
# shows exactly which variants it misses.
# --------------------------------------------------------------------------

HOSTILE_VALUES = (
    ("json-true", True), ("json-false", False), ("json-float-one", 1.0),
    ("json-text-one", "1"), ("json-zero", 0), ("json-two", 2),
    ("json-null", None), ("json-empty-string", ""), ("json-empty-object", {}),
    ("json-empty-array", []), ("json-negative", -1), ("json-large-int", 2 ** 63),
    ("json-control-char", "a\x01b"), ("json-non-nfc", "e\u0301"),
    ("json-deep-array", [[[[1]]]]), ("json-object-leaf", {"x": 1}),
    ("json-long-text", "z" * 5000),
)


def node_census(value, leaves: bool = True):
    """Root + every object key + every array index at unlimited depth."""
    counts = {"enumeratedPaths": 0, "containerPaths": 0, "scalarLeafPaths": 0,
              "dictPaths": 0, "listPaths": 0}
    paths: list[list[Any]] = []

    def walk(node, path):
        container = isinstance(node, (dict, list))
        if container or leaves:
            counts["enumeratedPaths"] += 1
            paths.append(list(path))
            if container:
                counts["containerPaths"] += 1
                counts["dictPaths"] += isinstance(node, dict)
                counts["listPaths"] += isinstance(node, list)
            else:
                counts["scalarLeafPaths"] += 1
        if isinstance(node, dict):
            for key, child in node.items():
                walk(child, path + [key])
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, path + [index])

    walk(value, [])
    return counts, paths


def _inject(root, path, injected):
    """Deep-copies the INJECTED value as well as the root.

    The predecessor shares the mutable members of its injection table across
    every case, so a guard that mutates what it is handed changes what later
    cases inject and the surface counts become order-dependent.  Measured, not
    supposed: RES-EP11-13.
    """
    value = copy.deepcopy(injected)
    if not path:
        return value
    node = copy.deepcopy(root)
    cursor = node
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return node


def _at(root, path):
    cursor = root
    for key in path:
        cursor = cursor[key]
    return cursor


def _path_text(path):
    text = "$"
    for key in path:
        text += f"[{key}]" if isinstance(key, int) else f".{key}"
    return text


def _same_value(current, injected) -> bool:
    return type(current) is type(injected) and current == injected


def plan_intent_surface(intent, authority, snapshots):
    """v11's differential oracle AND the plan-intent silent-accept enumeration."""
    stats = {"enumeratedCases": 0, "noOpInjections": 0, "executedCases": 0,
             "guardedEscapes": 0, "joinVsRepairedMismatches": 0,
             "supersededDivergentPositions": 0, "silentAccepts": 0}
    mismatches: list[str] = []
    divergent: list[str] = []
    silent: list[str] = []
    census, paths = node_census(intent)
    try:
        private = _private_repaired(snapshots)
        c4 = json.loads(snapshots[C2V4_CONTRACT].decode("utf-8"),
                        object_pairs_hook=_pairs)
        relations = set(json.loads(snapshots[FACT_PLANE].decode("utf-8"),
                                   object_pairs_hook=_pairs)
                        ["relationRegistry"]["relations"])
    except (AuthorityLoadError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError, *MALFORMED) as exc:
        return {"census": census, "stats": stats, "firstMismatches": [],
                "firstDivergent": [], "silentAcceptPositions": [],
                "discriminatingCardinality": 0,
                "error": f"{type(exc).__name__}: {exc}"}
    v3 = authority.module(C2V3)
    c3 = authority.json(C2V3_CONTRACT)

    def answer(module, contract, value):
        try:
            return bool(list(module.validate_plan_intent(value, contract, relations)))
        except MALFORMED:
            return "raised"

    for path in paths:
        try:
            current = _at(intent, path)
        except MALFORMED:
            continue
        for label, injected in HOSTILE_VALUES:
            stats["enumeratedCases"] += 1
            if _same_value(current, injected):
                stats["noOpInjections"] += 1
                continue
            stats["executedCases"] += 1
            mutated = _inject(intent, path, injected)
            try:
                join = bool(c2_validate_intent(mutated, authority))
            except Exception:  # noqa: BLE001
                stats["guardedEscapes"] += 1
                continue
            position = f"{_path_text(path)}={label}"
            if not join:
                stats["silentAccepts"] += 1
                silent.append(position)
            repaired = answer(private, c4, mutated)
            superseded = answer(v3, c3, mutated)
            if join != repaired:
                stats["joinVsRepairedMismatches"] += 1
                if len(mismatches) < 12:
                    mismatches.append(position)
            if superseded != repaired:
                stats["supersededDivergentPositions"] += 1
                if len(divergent) < 12:
                    divergent.append(position)
    return {"census": census, "stats": stats, "firstMismatches": mismatches,
            "firstDivergent": divergent,
            "silentAcceptPositions": sorted(silent),
            "discriminatingCardinality": stats["supersededDivergentPositions"]}


def differential_oracle_findings(result) -> list[str]:
    findings = []
    if result.get("error"):
        findings.append("EP11-DIFF: the differential oracle could not run: "
                        f"{result['error']}")
    if result["stats"]["joinVsRepairedMismatches"]:
        findings.append(
            "EP11-DIFF: the authority join answered differently from the "
            "independently instantiated repaired instrument at "
            f"{result['stats']['joinVsRepairedMismatches']} enumerated position(s), "
            f"e.g. {result['firstMismatches'][:4]}")
    if result["stats"]["guardedEscapes"]:
        findings.append("EP11-DIFF: the join raised out of its total boundary at "
                        f"{result['stats']['guardedEscapes']} position(s)")
    if not result["discriminatingCardinality"]:
        findings.append("EP11-DIFF: the differential oracle has ZERO discriminating "
                        "positions on this census, so it cannot witness a routing "
                        "defect at all; it must not be published as a guard")
    return findings


def plan_descriptor_surface(descriptor, guarded):
    """The second wire surface, with its silent accepts ENUMERATED (IR-EP10-NB-03)."""
    census, paths = node_census(descriptor)
    stats = {"enumeratedCases": 0, "noOpInjections": 0, "executedCases": 0,
             "guardedEscapes": 0, "silentAccepts": 0, "rejections": 0}
    silent: list[str] = []
    for path in paths:
        try:
            current = _at(descriptor, path)
        except MALFORMED:
            continue
        for label, injected in HOSTILE_VALUES:
            stats["enumeratedCases"] += 1
            if _same_value(current, injected):
                stats["noOpInjections"] += 1
                continue
            stats["executedCases"] += 1
            try:
                findings = guarded(_inject(descriptor, path, injected))
            except Exception:  # noqa: BLE001
                stats["guardedEscapes"] += 1
                continue
            if findings:
                stats["rejections"] += 1
            else:
                stats["silentAccepts"] += 1
                silent.append(f"{_path_text(path)}={label}")
    return {"census": census, "stats": stats,
            "silentAcceptPositions": sorted(silent)}


# --------------------------------------------------------------------------
# Section 6.  Source tripwires.  DECLARED SCOPE, so nothing here is over-read.
# --------------------------------------------------------------------------

_SCAN_CACHE: dict[str, Any] = {}


def _own_source() -> bytes:
    if "source" not in _SCAN_CACHE:
        # RES-EP11-05: the instrument's own bytes are by construction not in its
        # own pinned set.  Recorded so the trust-order claim is not over-read.
        _SCAN_CACHE["source"] = (HERE / pathlib.Path(__file__).name).read_bytes()
    return _SCAN_CACHE["source"]


def _own_tree():
    if "tree" not in _SCAN_CACHE:
        _SCAN_CACHE["tree"] = ast.parse(_own_source())
    return _SCAN_CACHE["tree"]


def _module_functions(tree):
    return {node.name: node for node in tree.body
            if isinstance(node, ast.FunctionDef)}


def c2_route_scan(tree=None):
    """Tripwire: which top-level functions name a C-2 API, and how."""
    if tree is None and "route" in _SCAN_CACHE:
        return _SCAN_CACHE["route"]
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    sites = routed = 0
    outside, unrouted = [], []
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
                receiver = getattr(node, "value", None)
                if isinstance(receiver, ast.Call) and \
                        isinstance(receiver.func, ast.Attribute) and \
                        receiver.func.attr in ("c2v4", "c2v3"):
                    routed += 1
                else:
                    unrouted.append(f"{name} line {getattr(node, 'lineno', 0)}")
    result = {"scannedFunctions": len(functions), "apiReferenceSites": sites,
              "referencesOutsideDeclaredClosure": sorted(set(outside)),
              "authorityRoutedSites": routed,
              "unroutedSitesInsideJoin": sorted(set(unrouted))}
    if tree is None:
        _SCAN_CACHE["route"] = result
    return result


# Primitives by which code inside the route region could reach the guard's
# private state.  RES-EP11-02 states plainly that this list is not a defence
# against a determined stack walk; it is a tripwire that makes the cheap
# spellings visible, and its behavioural counterpart is global_binding_probe.
INTROSPECTION_NAMES = frozenset((
    "_getframe", "f_locals", "f_globals", "f_back", "f_code", "__closure__",
    "cell_contents", "__code__", "__globals__", "__traceback__", "tb_frame",
    "tb_next", "gi_frame", "cr_frame", "globals", "vars", "dir", "gc",
    "get_referrers", "get_objects", "getattr", "setattr", "delattr",
    "__getattribute__", "__getattr__", "__class__", "__dict__", "__mro__",
    "__subclasses__", "__base__", "__bases__", "__builtins__", "__import__",
    "exec", "eval", "compile", "importlib", "sys", "exc_info", "produced",
    "_Witness", "_witnessing", "_witness_wrapper", "_private_repaired"))


def route_region_text(source_text: str | None = None) -> str:
    text = _own_source().decode("utf-8") if source_text is None else source_text
    begin, end = _route_region(text)
    return text[begin:end]


def route_introspection_scan(source_text=None):
    """Tripwire: the route region reads its arguments; it does not read the guard.

    Scans the WHOLE region between the markers — every function, helper, class
    body and expression the mutation is permitted to write — not a fixed list of
    function names, because a helper the region defines is region code too.

    DECLARED BLIND SPOT, and it is the important one: this is an ENUMERATION of
    spellings.  A spelling it does not name would reach the guard's private
    witness undetected.  Two tamper variants are built against it and executed on
    every ordinary run (AX6 plain, AX9 obfuscated) and their measured outcome is
    published; that is evidence about those two, not about the class.
    """
    region = route_region_text(source_text)
    try:
        tree = ast.parse(region)
    except SyntaxError as exc:  # pragma: no cover - authoring error
        return {"regionCharacters": len(region),
                "introspectionSites": [f"region does not parse: {exc}"]}
    offenders = []
    for node in ast.walk(tree):
        identifier = None
        if isinstance(node, ast.Attribute):
            identifier = node.attr
        elif isinstance(node, ast.Name):
            identifier = node.id
        if identifier in INTROSPECTION_NAMES:
            offenders.append(f"line {getattr(node, 'lineno', 0)}: {identifier}")
    declared = {node.name for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    missing = [name for name in C2_JOIN_CLOSURE if name not in declared]
    for name in missing:
        offenders.append(f"the route region does not define {name}")
    return {"regionCharacters": len(region),
            "regionDefinitions": len(declared),
            "introspectionSites": sorted(set(offenders))}


def selftest_dispatch_scan(tree=None):
    """Tripwire: exactly one flag-guarded selftest dispatch, before any check."""
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    node = functions.get("main")
    mains = sum(1 for item in subject.body
                if isinstance(item, ast.FunctionDef) and item.name == "main")
    if node is None:
        return {"mainFunctions": mains, "selftestCalls": 0,
                "dispatchBeforeFindings": False}
    calls = 0
    dispatch_line = findings_line = None
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
            if child.func.id == "selftest":
                calls += 1
                dispatch_line = getattr(child, "lineno", 0)
            elif child.func.id == "check" and findings_line is None:
                findings_line = getattr(child, "lineno", 0)
    return {"mainFunctions": mains, "selftestCalls": calls,
            "dispatchBeforeFindings": bool(dispatch_line and findings_line
                                           and dispatch_line < findings_line)}


WIRE_SOURCED_HINTS = frozenset((
    "contract", "candidate", "row", "rows", "intent", "record", "source", "item",
    "vector", "vectors", "published", "declared", "block", "value", "values",
    "parsed", "json", "get"))


def _identifiers(node):
    names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
        elif isinstance(child, ast.Attribute):
            names.add(child.attr)
        elif isinstance(child, ast.Constant) and isinstance(child.value, str):
            names.add(child.value)
    return names


def integer_guard_scan(tree=None):
    """Tripwire: a bare numeric comparison against a literal IS the LB-C2-01 bug."""
    subject = _own_tree() if tree is None else tree
    functions = _module_functions(subject)
    offenders = []
    for name in sorted(functions):
        for node in ast.walk(functions[name]):
            if not isinstance(node, ast.Compare) or len(node.comparators) != 1:
                continue
            if not isinstance(node.ops[0], (ast.Eq, ast.NotEq)):
                continue
            right = node.comparators[0]
            if not isinstance(right, ast.Constant) or \
                    isinstance(right.value, bool) or \
                    not isinstance(right.value, (int, float)):
                continue
            left = node.left
            if isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and \
                    left.func.id in ("len", "sum", "id"):
                continue
            if _identifiers(left) & WIRE_SOURCED_HINTS:
                offenders.append(f"{name} line {getattr(node, 'lineno', 0)}")
    return {"scannedFunctions": len(functions),
            "bareNumericComparisons": sorted(set(offenders))}


_HEX64 = re.compile(rb"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])")


def non_circularity_scan(source: bytes | None = None):
    """MEASURED: this checker's own text carries pins and nothing else.

    A checker that carries the expected commitment, or any durable identity
    digest, as a literal can make a candidate pass out of its own text.  The
    unique 64-hex literals in this file are counted and required to be exactly
    the pin set.
    """
    text = _own_source() if source is None else source
    literals = {match.decode("ascii") for match in _HEX64.findall(text)}
    pins = set(ALL_PINS.values())
    return {"uniqueHexLiterals": len(literals), "pinnedDigests": len(pins),
            "literalsThatAreNotPins": sorted(literals - pins),
            "pinsAbsentFromOwnText": sorted(pins - literals)}


def global_binding_probe(before: dict[str, int]) -> list[str]:
    """Behavioural counterpart of the introspection tripwire.

    Every module-level function binding is fingerprinted by object identity
    before the join is driven and re-checked afterwards.  A route region that
    rebinds a module global — the cheap way to blind a guard from inside the
    region the battery is allowed to rewrite — is reported here without reading
    a single byte of source.
    """
    moved = sorted(name for name, ident in before.items()
                   if id(globals().get(name)) != ident)
    return moved


def module_binding_fingerprint() -> dict[str, int]:
    return {name: id(value) for name, value in globals().items()
            if isinstance(value, types.FunctionType)}


AST_SCAN_REGISTRY = (
    ("c2-route",
     "which top-level functions name a C-2 API and whether every C-2 site inside "
     "the join routes through an Authority accessor",
     "answer_provenance_guard: A-1..A-5 over every pinned vector, reading no "
     "source at all"),
    ("route-introspection",
     "the route region names no primitive by which it could read or rewrite the "
     "guard's private state",
     "global_binding_probe: every module-level function binding fingerprinted by "
     "object identity across the drive"),
    ("selftest-dispatch",
     "exactly one flag-guarded selftest dispatch positioned before any findings "
     "return",
     "exit_matrix_probe: main() driven in-process, observing the declared exit "
     "codes behaviourally"),
    ("integer-guard",
     "no bare numeric comparison between a wire-sourced expression and a numeric "
     "literal",
     "own_constant_leaf_battery: every int/bool scalar leaf of the candidate "
     "replaced by a type-distinct value and the whole checking layer re-run"),
    ("non-circularity",
     "this checker's own text contains no digest literal that is not a pin",
     "the declared commitment is compared against the digest-pinned EP8 artifact "
     "AND required to be a member of the set recomputed on this run"),
)


# --------------------------------------------------------------------------
# Section 7.  The evasion battery.
#
# SOURCE variants rewrite the ROUTE-REGION of this checker's own bytes, exec the
# mutated module, and run ITS join against the REAL pinned vectors through the
# parent's verified authority.  The four that matter are new here:
#
#   AX2   ep10.review-independent.json's blocking evasion, rebuilt: a real,
#         correctly-argumented, LEDGER-RECORDED call into the repaired module
#         whose result is DISCARDED, with the superseded module's answer returned
#         through the ledger's own unwrapped originals.  Under v10 this exits 0
#         with the full green banner.
#   AX3   verdict-only substitution: commit and canonical honest, the gate alone
#         taken from the superseded module.
#   AX4   commitment-only substitution: the gate honest, the commitment alone
#         taken from the superseded module.
#   AX5   family split: the repaired answer for the LB-C2-01 probe family and
#         every position where the two instruments diverge, the superseded
#         answer for the real vectors.  Value equality holds everywhere.
#   AX6   the declared blind spot, built and executed rather than asserted: the
#         route region walks the stack with sys._getframe.  Whatever it measures
#         is published, including ESCAPED.
#
# OBJECT variants attack the Authority and the ledger rather than the source,
# including the four classes ep10.review-independent.json built by hand and
# reported as caught: tag forgery at install, a superseded-backed shim installed
# under the repaired tag, a monkeypatched recorder, and a delegating proxy.
#
# EVERY layer is scored SEPARATELY and the unflattering cells are published.
# --------------------------------------------------------------------------

ROUTE_BEGIN = "\n# ROUTE-REGION-BEGIN\n"
ROUTE_END = "\n# ROUTE-REGION-END\n"


def _route_region(source_text: str) -> tuple[int, int]:
    begin = source_text.index(ROUTE_BEGIN) + len(ROUTE_BEGIN)
    end = source_text.index(ROUTE_END)
    return begin, end


_HONEST_COMMIT_AND_CANONICAL = '''
def c2_commit_intent(intent, authority):
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().plan_intent_commitment(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]


def c2_canonical_intent(intent, authority):
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().canonical_plan_intent(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]
'''

_HONEST_VALIDATE = '''
def c2_validate_intent(intent, authority):
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        return authority.c2v4().validate_plan_intent(
            intent, contract, set(relations))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_PROBE_HELPER = '''
def _is_probe_family(intent):
    """True for the fixed LB-C2-01 probe family and for every position at which
    the two instruments can diverge; False for a real pinned vector."""
    try:
        if type(intent.get("schemaVersion")) is not int:
            return True
        inner = intent["analysis"]["admissionDescriptor"].get("schemaVersion")
        return type(inner) is not int
    except MALFORMED:
        return True
'''

_AX2_VALIDATE = '''
def c2_validate_intent(intent, authority):
    """AX2, ep10.review-independent.json's blocking evasion, rebuilt.

    A real, correctly-argumented, LEDGER-RECORDED call into the repaired module
    is made for every input.  Its result is returned only for the probe family —
    which is exactly the set of positions at which the two instruments diverge,
    so the differential oracle sees agreement everywhere.  For every REAL pinned
    vector the result is DISCARDED and the superseded module's answer is returned
    through the ledger's own unwrapped original, which records nothing.  Commit
    and canonical are left honestly on the repaired module, so v10's R-5 holds by
    construction and all six of its rules stay green.
    """
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        answer = authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        if _is_probe_family(intent):
            return answer
        hidden = authority.ledger.originals[(C2V3, "validate_plan_intent")]
        return hidden(intent, authority.json(C2V3_CONTRACT), relations)
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_DECOY_VALIDATE = '''
def c2_validate_intent(intent, authority):
    """AX3: verdict-only substitution with a decoy call and NO whitelist, so the
    accept/reject gate is the superseded module's for every input."""
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        hidden = authority.ledger.originals[(C2V3, "validate_plan_intent")]
        return hidden(intent, authority.json(C2V3_CONTRACT), relations)
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_AX4_COMMIT = '''
def c2_commit_intent(intent, authority):
    """AX4: commitment-only substitution that leaves NO superseded trace.

    The repaired module is called for the commitment and its answer discarded.
    The commitment returned is derived from the superseded module's UNWRAPPED
    canonical preimage, so no superseded call is recorded at any depth and the
    depth-1 leak that catches a naive commit substitution never happens.
    """
    try:
        authority.c2v4().plan_intent_commitment(
            intent, authority.json(C2V4_CONTRACT))
        hidden = authority.ledger.originals[(C2V3, "canonical_plan_intent")]
        preimage = hidden(intent, authority.json(C2V3_CONTRACT))
        return "sha256:" + hashlib.sha256(preimage).hexdigest(), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]
'''

_HONEST_CANONICAL = '''
def c2_canonical_intent(intent, authority):
    try:
        contract = authority.json(C2V4_CONTRACT)
        return authority.c2v4().canonical_plan_intent(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]
'''

_SPLIT_VALIDATE = '''
def c2_validate_intent(intent, authority):
    """AX5: the repaired answer for every position where the two instruments can
    diverge, the superseded answer for the real pinned vectors, on all three
    APIs at once."""
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        if _is_probe_family(intent):
            return authority.c2v4().validate_plan_intent(
                intent, authority.json(C2V4_CONTRACT), relations)
        authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        hidden = authority.ledger.originals[(C2V3, "validate_plan_intent")]
        return hidden(intent, authority.json(C2V3_CONTRACT), relations)
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_SPLIT_COMMIT = '''
def c2_commit_intent(intent, authority):
    try:
        if _is_probe_family(intent):
            return authority.c2v4().plan_intent_commitment(
                intent, authority.json(C2V4_CONTRACT)), []
        authority.c2v4().plan_intent_commitment(
            intent, authority.json(C2V4_CONTRACT))
        hidden = authority.ledger.originals[(C2V3, "plan_intent_commitment")]
        return hidden(intent, authority.json(C2V3_CONTRACT)), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]


def c2_canonical_intent(intent, authority):
    try:
        if _is_probe_family(intent):
            return authority.c2v4().canonical_plan_intent(
                intent, authority.json(C2V4_CONTRACT)), []
        authority.c2v4().canonical_plan_intent(
            intent, authority.json(C2V4_CONTRACT))
        hidden = authority.ledger.originals[(C2V3, "canonical_plan_intent")]
        return hidden(intent, authority.json(C2V3_CONTRACT)), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]
'''

_POISON_DETECTOR = '''
def c2_validate_intent(intent, authority):
    """AX8: the strongest answer substitution I could build.

    It defeats A-3 and A-4 without any introspection at all, by DETECTING the
    sentinel differentially: it calls both instruments and, whenever they
    disagree — which on a pinned vector means one of them has been poisoned —
    returns the repaired module's answer, so both sentinel-flow rules hold.  When
    they agree it returns the superseded module's object and forges a ledger
    entry and a provenance record for it, so v10's R-5 and the shared ledger both
    say the repaired module produced it.  Only A-2's PRIVATE witness sees it.
    """
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        ledger = authority.ledger
        repaired = authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        hidden = ledger.originals[(C2V3, "validate_plan_intent")]
        answer = hidden(intent, authority.json(C2V3_CONTRACT), relations)
        if repaired != answer:
            return repaired
        forged = authority.delegate.ServedCall(
            len(ledger.entries), C2V4, "validate_plan_intent", 0,
            value_fingerprint(intent), None)
        forged.result = answer
        ledger.entries.append(forged)
        ledger._provenance[id(answer)] = C2V4
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_REPLAY_VALIDATE = '''
def c2_validate_intent(intent, authority):
    """A forged ledger entry replayed for an unwrapped superseded call: the call
    ledger is told a repaired call happened and is handed the superseded object,
    with the provenance map forged to match."""
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        ledger = authority.ledger
        hidden = ledger.originals[(C2V3, "validate_plan_intent")]
        answer = hidden(intent, authority.json(C2V3_CONTRACT), relations)
        forged = authority.delegate.ServedCall(
            len(ledger.entries), C2V4, "validate_plan_intent", 0,
            value_fingerprint(intent), None)
        forged.result = answer
        ledger.entries.append(forged)
        ledger._provenance[id(answer)] = C2V4
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_FRAME_TAMPER = '''
def c2_validate_intent(intent, authority):
    """AX6: AX8 plus a stack walk that forges the guard's PRIVATE witness record.

    This is RES-EP11-02's declared blind spot, built and executed rather than
    asserted.  It defeats every behavioural rule the answer-provenance guard has.
    The introspection tripwire is the only thing left, and it sees this variant
    because this variant is spelled plainly.
    """
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        ledger = authority.ledger
        repaired = authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        hidden = ledger.originals[(C2V3, "validate_plan_intent")]
        answer = hidden(intent, authority.json(C2V3_CONTRACT), relations)
        if repaired != answer:
            return repaired
        frame = sys._getframe(1)
        witness = None
        while frame is not None and witness is None:
            witness = frame.f_locals.get("witness")
            frame = frame.f_back
        if witness is not None:
            witness.produced[id(answer)] = (
                C2V4, "validate_plan_intent", value_fingerprint(intent), 0, answer)
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_OBFUSCATED_TAMPER = '''
def _reach(subject, parts):
    return getattr(subject, "".join(parts))


def c2_validate_intent(intent, authority):
    """AX9: the same tamper as AX6, spelled so that not one identifier the
    introspection tripwire enumerates is written literally — every attribute name
    is assembled at run time and the frame is taken from an exception rather than
    from sys."""
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        ledger = authority.ledger
        repaired = authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        hidden = ledger.originals[(C2V3, "validate_plan_intent")]
        answer = hidden(intent, authority.json(C2V3_CONTRACT), relations)
        if repaired != answer:
            return repaired
        try:
            raise StopIteration("reach")
        except StopIteration as probe:
            frame = _reach(_reach(probe, ("__", "traceback", "__")),
                           ("tb", "_", "frame"))
        seen = None
        while frame is not None and seen is None:
            seen = _reach(frame, ("f", "_", "locals")).get("witness")
            frame = _reach(frame, ("f", "_", "back"))
        if seen is not None:
            _reach(seen, ("produ", "ced"))[id(answer)] = (
                C2V4, "validate_plan_intent", value_fingerprint(intent), 0, answer)
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''


def _region(call, contract="C2V4_CONTRACT", helper="", prelude=""):
    """v10's whole-region shape: all three APIs routed the same way."""
    return f'''
{helper}

def c2_validate_intent(intent, authority):
    try:
        contract = authority.json({contract})
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
{prelude}
        return {call.format(api="validate_plan_intent")}(
            intent, contract, set(relations))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]


def c2_commit_intent(intent, authority):
    try:
        contract = authority.json({contract})
{prelude}
        return {call.format(api="plan_intent_commitment")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]


def c2_canonical_intent(intent, authority):
    try:
        contract = authority.json({contract})
{prelude}
        return {call.format(api="canonical_plan_intent")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]
'''


def _whitelist_region(call, tick=""):
    """R1/R4 shape: probes reach the repaired instrument, real vectors do not."""
    return f'''
{_PROBE_HELPER}

def c2_validate_intent(intent, authority):
    try:
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        if _is_probe_family(intent):
            return authority.c2v4().validate_plan_intent(
                intent, authority.json(C2V4_CONTRACT), set(relations))
{tick}
        contract = authority.json(C2V3_CONTRACT)
        return {call.format(api="validate_plan_intent")}(
            intent, contract, set(relations))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]


def c2_commit_intent(intent, authority):
    try:
        if _is_probe_family(intent):
            return authority.c2v4().plan_intent_commitment(
                intent, authority.json(C2V4_CONTRACT)), []
{tick}
        contract = authority.json(C2V3_CONTRACT)
        return {call.format(api="plan_intent_commitment")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]


def c2_canonical_intent(intent, authority):
    try:
        if _is_probe_family(intent):
            return authority.c2v4().canonical_plan_intent(
                intent, authority.json(C2V4_CONTRACT)), []
{tick}
        contract = authority.json(C2V3_CONTRACT)
        return {call.format(api="canonical_plan_intent")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", "boundary")]
'''


def evasion_variants():
    return (
        ("AX2-decoy-call-superseded-answer",
         "ep10.review-independent.json's BLOCKING evasion, rebuilt: a real, "
         "correctly-argumented, ledger-recorded call into the repaired module "
         "whose result is DISCARDED for every real pinned vector, returning the "
         "superseded module's answer; commit and canonical honest so v10's R-5 "
         "holds and the probe family whitelisted so the oracle sees agreement",
         _PROBE_HELPER + _AX2_VALIDATE + _HONEST_COMMIT_AND_CANONICAL),
        ("AX3-verdict-only-substitution",
         "only the validation verdict — the accept/reject gate — is taken from "
         "the superseded module, for every input; commit and canonical honest",
         _DECOY_VALIDATE + _HONEST_COMMIT_AND_CANONICAL),
        ("AX4-commitment-only-substitution",
         "only the commitment is substituted, derived from the superseded "
         "module's UNWRAPPED canonical preimage so no superseded call is recorded "
         "at any depth; the gate and the preimage are honest",
         _HONEST_VALIDATE + _AX4_COMMIT + _HONEST_CANONICAL),
        ("AX5-probe-family-split-answers",
         "the repaired ANSWER for the probe family and every divergent position, "
         "the superseded answer for the real vectors, on all three APIs",
         _PROBE_HELPER + _SPLIT_VALIDATE + _SPLIT_COMMIT),
        ("AX8-differential-sentinel-detector",
         "detects the sentinel by calling both instruments and following the "
         "repaired one whenever they disagree, so A-3 and A-4 both hold, and "
         "forges a ledger entry and provenance record for the superseded answer "
         "when they agree",
         _POISON_DETECTOR + _HONEST_COMMIT_AND_CANONICAL),
        ("AX6-stack-walking-witness-forgery",
         "RES-EP11-02's declared blind spot, BUILT AND EXECUTED: AX8 plus a "
         "sys._getframe stack walk that forges the guard's PRIVATE witness record",
         _FRAME_TAMPER + _HONEST_COMMIT_AND_CANONICAL),
        ("AX9-obfuscated-witness-forgery",
         "the same tamper as AX6 with every enumerated identifier assembled at "
         "run time and the frame taken from an exception rather than from sys",
         _OBFUSCATED_TAMPER + _HONEST_COMMIT_AND_CANONICAL),
        ("forged-ledger-entry-replay",
         "an unwrapped superseded call with a forged repaired-tagged ledger entry "
         "and a forged provenance record replayed for it",
         _REPLAY_VALIDATE + _HONEST_COMMIT_AND_CANONICAL),
        ("R1-probe-whitelist-direct-module",
         "the ep9 reviewer's R1: route the fixed LB-C2-01 probe family to the "
         "repaired module and every real vector to the superseded module, naming "
         "the module directly",
         _whitelist_region("authority.modules[C2V3].{api}")),
        ("R4-probe-whitelist-accessor-routed",
         "the ep9 reviewer's R4: the same whitelist spelled so every C-2 receiver "
         "is an Authority accessor Call, with the accessor touched on every path",
         _whitelist_region("authority.c2v3().{api}", "        authority.c2v4()")),
        ("accessor-c2v3",
         "route the whole join to the superseded accessor; clean by the route "
         "scan's own rule",
         _region("authority.c2v3().{api}", "C2V3_CONTRACT")),
        ("getattr-indirection",
         "reach the superseded API through getattr so no identifier appears",
         _region('getattr(authority.c2v3(), "{api}")', "C2V3_CONTRACT")),
    )


def _exec_variant(name: str, source_text: str):
    module = types.ModuleType(
        f"_ep11_evasion_{re.sub(r'[^0-9a-zA-Z]', '_', name)}")
    module.__dict__["__file__"] = str(HERE / pathlib.Path(__file__).name)
    exec(compile(source_text, f"<evasion:{name}>", "exec"),  # noqa: S102
         module.__dict__)
    return module


class _AuthorityView:
    def __init__(self, inner):
        self._inner = inner
        self.ledger = inner.ledger
        self.modules = inner.modules
        self.delegate = getattr(inner, "delegate", None)

    def json(self, name):
        return self._inner.json(name)

    def module(self, name):
        return self._inner.module(name)

    def c2v3(self):
        return self._inner.c2v3()

    def c2v4(self):
        return self._inner.c2v4()


class _PoisonedAccessorAuthority(_AuthorityView):
    """Authority.c2v4() returns the superseded module."""

    def c2v4(self):
        return self._inner.c2v3()


class _UnwrappedModuleAuthority(_AuthorityView):
    """The join is handed a module object the ledger never instrumented."""

    def __init__(self, inner):
        super().__init__(inner)
        shadow = types.ModuleType("_ep11_unwrapped_c2v4")
        shadow.__dict__.update(inner.module(C2V4).__dict__)
        for api in C2_IMPORTED_APIS:
            setattr(shadow, api, inner.ledger.originals[(C2V4, api)])
        self._shadow = shadow

    def c2v4(self):
        return self._shadow


class _DeinstalledLedgerAuthority(_AuthorityView):
    """The ledger is replaced by one that observed nothing."""

    def __init__(self, inner):
        super().__init__(inner)
        self.ledger = inner.delegate.ServedLedger()

    def c2v4(self):
        return self._inner.module(C2V4)


class _ProxyAccessorAuthority(_AuthorityView):
    """A __getattr__-delegating proxy stands in for the repaired module."""

    class _Proxy:
        def __init__(self, target):
            self.__dict__["_target"] = target

        def __getattr__(self, name):
            return getattr(self.__dict__["_target"], name)

    def c2v4(self):
        return self._Proxy(self._inner.c2v3())


class _TagForgedAuthority(_AuthorityView):
    """Tag forgery at INSTALL time.

    The install tags are swapped on a fresh ledger: the SUPERSEDED module is
    installed under the repaired tag and the repaired module under the
    superseded tag.  Every ledger entry the join produces then says C2V4 while
    the module that served it is check-c2.py, and the "independent"
    cross-reproduction is really the repaired module.  ep10.review-independent
    .json built this class by hand and reported superseded_cross_check as its
    sole catcher; here it is built, executed, and whichever guards fire is what
    the matrix publishes.
    """

    def __init__(self, inner, snapshots):
        super().__init__(inner)
        delegate = inner.delegate
        self.ledger = delegate.ServedLedger()
        self._v4 = _exec_verified(C2V4, snapshots[C2V4], prefix="_ep11_forge4")
        self._v3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep11_forge3")
        self.ledger.install(self._v3, C2V4)
        self.ledger.install(self._v4, C2V3)
        self.modules = {C2V4: self._v3, C2V3: self._v4}

    def module(self, name):
        return self.modules[name]

    def c2v4(self):
        return self._v3

    def c2v3(self):
        return self._v4


class _ShimAuthority(_AuthorityView):
    """Module substitution BEFORE install: a superseded-backed shim carrying the
    repaired module's name is installed under the repaired tag."""

    def __init__(self, inner, snapshots):
        super().__init__(inner)
        delegate = inner.delegate
        self.ledger = delegate.ServedLedger()
        real3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep11_shim3")
        shim = types.ModuleType("_ep11_shim_c2v4")
        for api in C2_IMPORTED_APIS:
            setattr(shim, api, getattr(real3, api))
        self._shim = shim
        self._v3 = real3
        self.ledger.install(shim, C2V4)
        self.ledger.install(real3, C2V3)
        self.modules = {C2V4: shim, C2V3: real3}

    def module(self, name):
        return self.modules[name]

    def c2v4(self):
        return self._shim

    def c2v3(self):
        return self._v3


class _ForgedRecorderAuthority(_AuthorityView):
    """The ledger's own recorder is monkeypatched so every install is tagged as
    the repaired module, and the join is routed to the superseded one."""

    def __init__(self, inner, snapshots):
        super().__init__(inner)
        delegate = inner.delegate
        ledger = delegate.ServedLedger()
        real_wrap = ledger._wrap
        ledger._wrap = lambda original, api, _tag: real_wrap(original, api, C2V4)
        self.ledger = ledger
        self._v4 = _exec_verified(C2V4, snapshots[C2V4], prefix="_ep11_rec4")
        self._v3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep11_rec3")
        ledger.install(self._v4, C2V4)
        ledger.installed.pop(C2V4, None)
        ledger.install(self._v3, C2V3)
        self.modules = {C2V4: self._v3, C2V3: self._v3}

    def module(self, name):
        return self.modules[name]

    def c2v4(self):
        return self._v3

    def c2v3(self):
        return self._v3


def object_attacks(snapshots):
    return (
        ("poisoned-accessor", "Authority.c2v4() returns the superseded module",
         lambda inner: _PoisonedAccessorAuthority(inner)),
        ("unwrapped-module",
         "the join is handed a module object the ledger never instrumented",
         lambda inner: _UnwrappedModuleAuthority(inner)),
        ("deinstalled-ledger", "the ledger is replaced by one that observed nothing",
         lambda inner: _DeinstalledLedgerAuthority(inner)),
        ("getattr-proxy-accessor",
         "a __getattr__-delegating proxy stands in for the repaired module",
         lambda inner: _ProxyAccessorAuthority(inner)),
        ("tag-forgery-at-install",
         "the ledger install tags are swapped and the join routed to the "
         "superseded-backed module under the repaired tag",
         lambda inner: _TagForgedAuthority(inner, snapshots)),
        ("superseded-backed-shim",
         "a superseded-backed shim is installed under the repaired tag before any "
         "call is made",
         lambda inner: _ShimAuthority(inner, snapshots)),
        ("monkeypatched-recorder",
         "the ledger's own _wrap is patched so every install records the repaired "
         "tag",
         lambda inner: _ForgedRecorderAuthority(inner, snapshots)),
    )


GUARD_IDS = ("answerProvenance", "callProvenance", "differentialOracle",
             "supersededCrossCheck", "c2RouteScan", "introspectionScan")


def _current_module():
    """This module's own guard surface, without depending on how it was loaded."""
    module = sys.modules.get(__name__)
    if module is not None and hasattr(module, "answer_provenance_guard"):
        return module
    return types.SimpleNamespace(
        answer_provenance_guard=answer_provenance_guard,
        call_provenance_guard=call_provenance_guard,
        plan_intent_surface=plan_intent_surface,
        differential_oracle_findings=differential_oracle_findings)


def _score(module, named, hostile, oracle_intent, snapshots, delegate, tree,
           mutated_text=None):
    """Run every declared guard against one hostile configuration."""
    fired = {}
    try:
        answer_findings, _counts, _rows = module.answer_provenance_guard(
            named, hostile, snapshots)
    except Exception as exc:  # noqa: BLE001
        answer_findings = [f"EP11-ANSWER: raised {type(exc).__name__}: {exc}"]
    fired["answerProvenance"] = bool(answer_findings)
    try:
        call_findings, _measure = module.call_provenance_guard(named, hostile)
    except Exception as exc:  # noqa: BLE001
        call_findings = [f"EP11-CALL: raised {type(exc).__name__}: {exc}"]
    fired["callProvenance"] = bool(call_findings)
    try:
        oracle = module.plan_intent_surface(oracle_intent, hostile, snapshots)
        fired["differentialOracle"] = bool(
            module.differential_oracle_findings(oracle))
    except Exception:  # noqa: BLE001
        fired["differentialOracle"] = True
    try:
        cross_findings, _rows = delegate.superseded_cross_check(named, hostile)
        fired["supersededCrossCheck"] = bool(cross_findings)
    except Exception:  # noqa: BLE001
        fired["supersededCrossCheck"] = True
    if tree is None:
        fired["c2RouteScan"] = False
        fired["introspectionScan"] = False
    else:
        scan = c2_route_scan(tree)
        fired["c2RouteScan"] = bool(
            scan["unroutedSitesInsideJoin"]
            or scan["referencesOutsideDeclaredClosure"]
            or scan["authorityRoutedSites"] < len(C2_IMPORTED_APIS))
        fired["introspectionScan"] = bool(
            route_introspection_scan(mutated_text)["introspectionSites"])
    return fired, (answer_findings, call_findings)


def evasion_measurement(named_intents, authority, oracle_intent, snapshots):
    source_text = _own_source().decode("utf-8")
    begin, end = _route_region(source_text)
    delegate = authority.delegate
    rows = []

    for name, why, region in evasion_variants():
        mutated = source_text[:begin] + region + source_text[end:]
        try:
            tree = ast.parse(mutated)
        except SyntaxError as exc:  # pragma: no cover - authoring error
            rows.append({"variant": name, "why": why, "class": "source",
                         "built": False, "error": f"SyntaxError: {exc}"})
            continue
        try:
            module = _exec_variant(name, mutated)
        except Exception as exc:  # noqa: BLE001
            rows.append({"variant": name, "why": why, "class": "source",
                         "built": False, "error": f"{type(exc).__name__}: {exc}"})
            continue
        fired, _detail = _score(module, named_intents, authority, oracle_intent,
                                snapshots, delegate, tree, mutated)
        rows.append({"variant": name, "why": why, "class": "source", "built": True,
                     **{key: fired[key] for key in GUARD_IDS}})

    for name, why, factory in object_attacks(snapshots):
        try:
            hostile = factory(authority)
        except Exception as exc:  # noqa: BLE001
            rows.append({"variant": name, "why": why, "class": "object",
                         "built": False, "error": f"{type(exc).__name__}: {exc}"})
            continue
        fired, _detail = _score(_current_module(), named_intents, hostile,
                                oracle_intent, snapshots, delegate, None)
        rows.append({"variant": name, "why": why, "class": "object", "built": True,
                     **{key: fired[key] for key in GUARD_IDS}})

    built = [row for row in rows if row.get("built")]
    per_guard = {key: sum(1 for row in built if row.get(key)) for key in GUARD_IDS}
    caught_by_any = [row for row in built
                     if any(row.get(key) for key in GUARD_IDS)]
    escaped = sorted(row["variant"] for row in built
                     if not any(row.get(key) for key in GUARD_IDS))
    sole = []
    for row in built:
        catchers = [key for key in GUARD_IDS if row.get(key)]
        if len(catchers) == 1:
            sole.append({"variant": row["variant"], "soleGuard": catchers[0]})
    answer_only = sorted(row["variant"] for row in built
                         if row.get("answerProvenance")
                         and not row.get("callProvenance")
                         and not row.get("differentialOracle")
                         and not row.get("supersededCrossCheck"))
    matrix = [{"variant": row["variant"], "class": row["class"],
               **{key: row.get(key) for key in GUARD_IDS}} for row in built]
    return {
        "variantsDeclared": len(rows),
        "variantsBuilt": len(built),
        "sourceVariantsBuilt": sum(1 for row in built if row["class"] == "source"),
        "objectAttacksBuilt": sum(1 for row in built if row["class"] == "object"),
        "caughtByAtLeastOneGuard": len(caught_by_any),
        "escapedEveryGuard": escaped,
        "perGuardCatchCount": per_guard,
        "soleGuardVariants": sorted(sole, key=lambda row: row["variant"]),
        "answerProvenanceOnlyCatches": answer_only,
        "perVariant": matrix,
    }


# --------------------------------------------------------------------------
# Section 8.  Preserved measurement, by delegation rather than by transcription.
# --------------------------------------------------------------------------

def preserved_measurements(authority, snapshots):
    """Execute the reviewer-verified v10 measurement from its verified bytes."""
    delegate = authority.delegate
    heavy = delegate.heavy_measurements(authority.inner)
    v10_candidate = authority.json(EP10_ARTIFACT)
    # Driven at the DELEGATE's own top level, not nested: v10's behavioural
    # counterparts (its exit matrix and its own constant-leaf battery) only run
    # when its nesting depth is zero, and a run that skipped them would report
    # findings about counterparts that were never executed rather than about the
    # measurements this candidate preserves.
    try:
        v10_findings = delegate.check(copy.deepcopy(v10_candidate), authority.inner)
    except Exception as exc:  # noqa: BLE001
        v10_findings = [f"the delegate's own checking layer raised "
                        f"{type(exc).__name__}: {exc}"]
    return heavy, v10_findings


def distinct_answer_probe(named_intents, authority, snapshots):
    """POSITIVE CONTROL on the guard: it must FAIL when the answer really is the
    superseded module's.

    A guard that has stopped discriminating passes everything, including an
    honest join, and no green banner can tell the difference.  Two deliberately
    substituted joins are driven through the SAME guard here and each is required
    to produce findings.  The second one also shows, in numbers, why the shared
    served-module ledger cannot be what A-2 tests: it forges the ledger entry and
    the provenance record, so the shared ledger agrees for every answer while the
    guard's private witness agrees for none.
    """
    source_text = _own_source().decode("utf-8")
    begin, end = _route_region(source_text)
    rows = {}
    for label, region in (
            ("decoyCall", _PROBE_HELPER + _AX2_VALIDATE
             + _HONEST_COMMIT_AND_CANONICAL),
            ("forgedLedgerEntry", _REPLAY_VALIDATE
             + _HONEST_COMMIT_AND_CANONICAL)):
        mutated = source_text[:begin] + region + source_text[end:]
        module = _exec_variant(f"positive-control-{label}", mutated)
        findings, counts, _rows = module.answer_provenance_guard(
            named_intents, authority, snapshots)
        rows[label] = {
            "producesFindings": bool(findings),
            "findingCount": len(findings),
            "independentValueAgreements": counts["independentValueAgreements"],
            "objectProvenanceAgreements": counts["objectProvenanceAgreements"],
            "sharedLedgerAgreements": counts["sharedLedgerAgreements"],
            "repairedSentinelFlowed": counts["repairedSentinelFlowed"],
            "supersededSentinelIgnored": counts["supersededSentinelIgnored"],
        }
    rows["bothProduceFindings"] = (rows["decoyCall"]["producesFindings"]
                                   and rows["forgedLedgerEntry"]
                                   ["producesFindings"])
    return rows


# --------------------------------------------------------------------------
# Section 9.  Heavy measurement, computed once per verified authority.
# --------------------------------------------------------------------------

def heavy_measurements(authority, snapshots) -> dict[str, Any]:
    if "ep11" in authority.cache:
        return authority.cache["ep11"]
    source = authority.json(VECTOR_SOURCE)
    vectors = source.get("positiveVectors") or []
    named = []
    for vector in vectors:
        try:
            named.append((vector["id"], vector["evaluationAuthorityCandidate"]
                          ["admittedResolvedInputs"]["frozenPlanIntent"]))
        except MALFORMED:
            continue
    if not named:
        heavy = {"named": [], "findings": ["EP11-VECTORS: no PlanIntent could be "
                                           "read from the pinned vector source"]}
        authority.cache["ep11"] = heavy
        return heavy

    delegate_heavy, v10_findings = preserved_measurements(authority, snapshots)

    before = module_binding_fingerprint()
    call_findings, call_measure = call_provenance_guard(named, authority)
    answer_findings, answer_counts, answer_rows = answer_provenance_guard(
        named, authority, snapshots)
    rebound = global_binding_probe(before)

    oracle = plan_intent_surface(named[0][1], authority, snapshots)
    oracle_findings = differential_oracle_findings(oracle)

    ri_module = authority.module(RI)
    v3_contract = authority.json(C2V3_CONTRACT)
    accepted_id = source.get("acceptedAuthorityVectorId")
    descriptor = None
    for vector in vectors:
        try:
            candidate_descriptor = (vector["evaluationAuthorityCandidate"]
                                    ["admittedResolvedInputs"]["planDescriptor"])
        except MALFORMED:
            continue
        if descriptor is None or vector.get("id") == accepted_id:
            descriptor = candidate_descriptor
    def plan_guard(value):
        try:
            return list(ri_module._plan_record_errors(value, v3_contract))
        except MALFORMED as exc:
            return [("RI-BOUNDARY", f"{type(exc).__name__}: {exc}")]

    descriptor_surface = plan_descriptor_surface(descriptor, plan_guard)

    evasion = evasion_measurement(named, authority, named[0][1], snapshots)
    control = distinct_answer_probe(named, authority, snapshots)

    findings = list(call_findings) + list(answer_findings) + list(oracle_findings)
    findings += c2_api_surface(authority)
    if rebound:
        findings.append(f"EP11-BINDING: module-level binding(s) {rebound} changed "
                        "identity across the authority drive; a guard whose own "
                        "globals move underneath it is not measuring the join")
    if v10_findings:
        findings.append(
            "EP11-PRESERVED: the pinned predecessor candidate no longer passes its "
            f"own pinned checking layer on this run ({len(v10_findings)} "
            f"finding(s), first: {str(v10_findings[0])[:160]}); the measurements "
            "this candidate preserves by delegation are not reproduced")
    if not control["bothProduceFindings"]:
        findings.append(
            "EP11-CONTROL: a join that demonstrably returns the superseded "
            "module's answer produced NO answer-provenance finding; the guard has "
            "stopped discriminating and its green result means nothing")

    heavy = {
        "named": named, "vectors": vectors, "findings": findings,
        "callProvenance": call_measure,
        "answerProvenance": answer_counts, "answerRows": answer_rows,
        "rebound": rebound,
        "oracle": oracle, "descriptorSurface": descriptor_surface,
        "evasion": evasion, "control": control,
        "delegate": delegate_heavy, "v10Findings": v10_findings,
        "delegateSourceSealed": delegate_source_is_sealed(
            authority.delegate, snapshots),
    }
    authority.cache["ep11"] = heavy
    return heavy


# --------------------------------------------------------------------------
# Section 10.  Behavioural counterparts of the source tripwires.
# --------------------------------------------------------------------------

def _invoke(argv, override=None):
    buffer, err = io.StringIO(), io.StringIO()
    stdout, stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = buffer, err
    _NESTED[0] += 1
    try:
        code = main(argv, override=override)
    except SystemExit as exc:  # pragma: no cover
        code = exc.code
    finally:
        _NESTED[0] -= 1
        sys.stdout, sys.stderr = stdout, stderr
    return code, buffer.getvalue() + err.getvalue()


def exit_matrix_probe(contract, path, authority, snapshots, full: bool):
    dirty = copy.deepcopy(contract)
    dirty["version"] = EXPECTED_VERSION + 1
    dirty_text = json.dumps(dirty)
    base = {"authority": authority, "snapshots": snapshots}
    rows = [
        ("unknown flag", ["x", "--bogus"], 2, None),
        ("two positional artifacts", ["x", str(path), str(path)], 2, None),
        ("repeated declared flag", ["x", "--selftest", "--selftest"], 2, None),
        ("--selftest over a dirty base", ["x", "--selftest"], 3,
         {**base, "candidateText": dirty_text}),
    ]
    if full:
        rows += [
            ("clean ordinary run", ["x", str(path)], 0, dict(base)),
            ("mutated candidate", ["x"], 1, {**base, "candidateText": dirty_text}),
        ]
    results = []
    for label, argv, expected, override in rows:
        code, output = _invoke(argv, override=override)
        results.append({"invocation": label, "expected": expected, "observed": code,
                        "agrees": code == expected,
                        "outputLines": len(output.splitlines())})
    return results


def own_constant_leaf_battery(contract, authority, snapshots):
    _census, paths = node_census(contract)
    leaves = []
    for path in paths:
        if not path:
            continue
        try:
            current = _at(contract, path)
        except MALFORMED:
            continue
        if isinstance(current, bool) or type(current) is int:
            leaves.append(path)
    cases = rejected = 0
    silent: list[str] = []
    _NESTED[0] += 1
    try:
        for path in leaves:
            current = _at(contract, path)
            for injected in (True, False, 1.0):
                if _same_value(current, injected):
                    continue
                cases += 1
                try:
                    findings = check(_inject(contract, path, injected), authority,
                                     snapshots)
                except Exception:  # noqa: BLE001
                    findings = ["raised"]
                if findings:
                    rejected += 1
                else:
                    silent.append(_path_text(path))
    finally:
        _NESTED[0] -= 1
    return {"intBoolLeaves": len(leaves), "cases": cases, "rejected": rejected,
            "silentlyAdmitted": len(silent),
            "silentlyAdmittedPositions": sorted(set(silent))}


# --------------------------------------------------------------------------
# Section 11.  The checking layer.
# --------------------------------------------------------------------------

def _exact_int(value, label, findings, expected=None) -> bool:
    if type(value) is not int:
        findings.append(f"EP11-TYPE: {label} must be the JSON integer type; got "
                        f"{type(value).__name__}")
        return False
    if expected is not None and value != expected:
        findings.append(f"EP11-TYPE: {label} must be {expected}; got {value}")
        return False
    return True


def _expect(published, key, measured, label, findings) -> None:
    got = published.get(key) if isinstance(published, dict) else None
    if not strict_equal(got, measured):
        findings.append(f"{label} publishes {key}={got!r}; this run measured "
                        f"{measured!r}")


def pin_agreement(contract, authority) -> list[str]:
    findings: list[str] = []
    closure = contract.get("delegationClosure") or {}
    declared: dict[str, str] = {}
    for key in ("delegatedChecker", "executables", "pinnedData",
                "supersededIndependentEncoder"):
        rows = closure.get(key)
        if isinstance(rows, dict):
            rows = [rows]
        if not isinstance(rows, list):
            findings.append(f"EP11-RECORD: delegationClosure.{key} must be an array")
            continue
        for row in rows:
            if not isinstance(row, dict) or "file" not in row or "sha256" not in row:
                findings.append(f"EP11-RECORD: delegationClosure.{key} rows must "
                                "record file AND sha256; a count is not a record")
                continue
            declared[row["file"]] = row["sha256"]
    for name, expected in ALL_PINS.items():
        actual = sha_bytes(authority._snapshots[name])
        if actual != expected:  # pragma: no cover - load_snapshots refuses first
            findings.append(f"EP11-RECORD: {name} recomputes to {actual}, pinned at "
                            f"{expected}")
        if declared.get(name) != expected:
            findings.append(f"EP11-RECORD: the candidate records {name} as "
                            f"{declared.get(name)!r}; this run verified {expected}")
    for name in sorted(set(declared) - set(ALL_PINS)):
        findings.append(f"EP11-RECORD: the candidate records {name}, which this "
                        "checker does not pin or verify")

    checked = 0
    for holder, attribute in ((EP10, "ALL_PINS"), (EP8, "PINNED"), (EP7, "PINNED"),
                              (EP6, "PINNED"), (C2V4, "PINS")):
        module = (authority.delegate if holder == EP10
                  else authority.module(holder))
        table = getattr(module, attribute, None)
        if not isinstance(table, dict):
            continue
        checked += 1
        for name, sha in table.items():
            if name in ALL_PINS and ALL_PINS[name] != sha:
                findings.append(f"EP11-CLOSURE: {holder}.{attribute} pins {name} at "
                                f"{sha}; v11 verified {ALL_PINS[name]}")
    rule = closure.get("pinAgreementRule")
    if not isinstance(rule, str) or "of those that expose one" not in rule:
        findings.append("EP11-CLOSURE: pinAgreementRule must state that the "
                        "cross-check covers only the closure members that expose a "
                        "pin table ('of those that expose one'); six of the eleven "
                        "expose none, and an '11/11' claim would quantify over a "
                        "region the instrument cannot observe")
    _expect(closure, "pinTablesCrossChecked", checked,
            "EP11-CLOSURE: delegationClosure", findings)
    return findings


RETRACTION_MIN_FRAGMENT = 60


def _resolve_json_path(document, path_text):
    """Resolve a $-rooted path of the shape used by this corpus."""
    cursor = document
    for token in re.findall(r"\.([A-Za-z0-9_]+)|\[(\d+)\]", path_text):
        key, index = token
        if key:
            cursor = cursor[key]
        else:
            cursor = cursor[int(index)]
    return cursor


def retraction_checks(contract, authority) -> list[str]:
    """IR-EP10-NB-01: the verbatim fragment must be substantive AND must occur
    inside the NAMED SUBJECT of the pinned predecessor, not merely somewhere in
    it.  A one-character fragment passed v10's test; here it cannot."""
    findings: list[str] = []
    retractions = contract.get("retractions")
    if not isinstance(retractions, list) or not retractions:
        return ["EP11-RETRACT: retractions must be a non-empty array"]
    by_id = {row.get("id"): row for row in retractions if isinstance(row, dict)}

    for retraction_id in REQUIRED_RETRACTIONS:
        row = by_id.get(retraction_id)
        if not isinstance(row, dict):
            findings.append(f"EP11-RETRACT: {retraction_id} is absent")
            continue
        if row.get("disposition") != "RETRACTED-AS-FALSE":
            findings.append(f"EP11-RETRACT: {retraction_id} must be disposed "
                            "RETRACTED-AS-FALSE; a retraction may not be softened "
                            "into a scoping note")
        quoted = row.get("retractedText")
        subject_file = row.get("subjectFile")
        subject_path = row.get("subjectPath")
        if not isinstance(quoted, str) or len(quoted) < RETRACTION_MIN_FRAGMENT:
            findings.append(
                f"EP11-RETRACT: {retraction_id}.retractedText must be a verbatim "
                f"fragment of at least {RETRACTION_MIN_FRAGMENT} characters; a "
                "one-character substring test is not a demonstration that the "
                "retraction targets the real bytes")
            continue
        if subject_file not in ALL_PINS:
            findings.append(f"EP11-RETRACT: {retraction_id}.subjectFile "
                            f"{subject_file!r} is not a pinned input")
            continue
        if subject_file.endswith(".py"):
            haystack = authority._snapshots[subject_file].decode("utf-8",
                                                                 "replace")
            located = "the pinned source"
        else:
            document = authority.json(subject_file)
            try:
                subject = _resolve_json_path(document, subject_path or "$")
            except MALFORMED:
                findings.append(f"EP11-RETRACT: {retraction_id}.subjectPath "
                                f"{subject_path!r} does not resolve in "
                                f"{subject_file}")
                continue
            haystack = subject if isinstance(subject, str) else json.dumps(
                subject, ensure_ascii=False, sort_keys=True)
            located = f"{subject_file} at {subject_path}"
        if quoted not in haystack:
            findings.append(
                f"EP11-RETRACT: {retraction_id}.retractedText is not a verbatim "
                f"fragment of {located}; the retraction does not demonstrably "
                "target the bytes it names")
        statement = row.get("statement") or ""
        if len(statement) < 200:
            findings.append(f"EP11-RETRACT: {retraction_id}.statement must say what "
                            "is false and what this run measured instead")

    for required in RETRACTION_CONTENT:
        row = by_id.get(required) or {}
        statement = row.get("statement") or ""
        for phrase in RETRACTION_CONTENT[required]:
            if phrase not in statement:
                findings.append(f"EP11-RETRACT: {required}.statement must state "
                                f"plainly that {phrase!r}")

    review = authority.json(EP10_REVIEW)
    if not isinstance(review, dict) or review.get("verdict") != "REJECT":
        findings.append("EP11-RETRACT: the pinned predecessor review must carry "
                        "verdict REJECT")
    blockers = review.get("blockers") if isinstance(review, dict) else None
    blocker_ids = sorted(row.get("id") for row in blockers) if isinstance(
        blockers, list) else []
    predecessor = contract.get("predecessor") or {}
    if predecessor.get("blockersAddressed") != blocker_ids:
        findings.append("EP11-RETRACT: predecessor.blockersAddressed is "
                        f"{predecessor.get('blockersAddressed')!r}; the pinned "
                        f"review carries {blocker_ids}")
    if predecessor.get("sha256") != ALL_PINS[EP10_ARTIFACT] or \
            predecessor.get("reviewSha256") != ALL_PINS[EP10_REVIEW]:
        findings.append("EP11-RETRACT: predecessor must record the predecessor and "
                        "its review by SHA-256")
    observations = review.get("nonBlockingObservations")
    observed_ids = sorted(row.get("id") for row in observations) if isinstance(
        observations, list) else []
    if predecessor.get("nonBlockingObservationsAddressed") != observed_ids:
        findings.append("EP11-RETRACT: predecessor.nonBlockingObservationsAddressed "
                        f"is {predecessor.get('nonBlockingObservationsAddressed')!r}; "
                        f"the pinned review carries {observed_ids}")
    return findings


REQUIRED_RETRACTIONS = ("RET-EP11-01", "RET-EP11-02", "RET-EP11-03")

RETRACTION_CONTENT = {
    "RET-EP11-01": ("which module was CALLED", "not whose answer was used",
                    "discarded"),
    "RET-EP11-02": ("call provenance", "answer provenance"),
    "RET-EP11-03": ("ROUTING ESTABLISHED BEHAVIOURALLY", "overstated"),
}

# IR-EP10-NB-02: nine of v10's ten residuals were enforced by ID PRESENCE ONLY,
# and the reviewer gutted two of them to bare identifiers while the checker still
# exited 0.  Here every residual must carry its declared SUBSTANCE.  The anchors
# are the load-bearing phrases of each residual, chosen so that a residual
# hollowed out to its identifier, or softened into a claim of closure, fails.
RESIDUAL_CONTENT = {
    "RES-EP11-01": (320, ("does NOT repair", "check-evaluation-proof-v6.py",
                          "OUTER gate")),
    "RES-EP11-02": (320, ("ROUTE REGION", "sys._getframe", "AX6",
                          "NOT closed")),
    "RES-EP11-03": (240, ("seven pinned vectors", "one distinct PlanIntent",
                          "value equality")),
    "RES-EP11-04": (200, ("tripwire", "behavioural counterpart")),
    "RES-EP11-05": (160, ("own source", "not a verified snapshot")),
    "RES-EP11-06": (240, ("MEASURED, NOT REPAIRED", "canonical unsigned decimal",
                          "EP5 successor")),
    "RES-EP11-07": (240, ("MEASURED, NOT REPAIRED", "durable identity",
                          "byte-identical", "v6/v8 successors")),
    "RES-EP11-08": (200, ("14 intents", "not a proof")),
    "RES-EP11-09": (240, ("rovenance is not correctness", "check-c2-v4.py")),
    "RES-EP11-10": (240, ("cannot re-run itself", "TOP-LEVEL run")),
    "RES-EP11-11": (200, ("pre-exist", "R2-FINAL-03", "rg")),
    "RES-EP11-12": (240, ("superseded_cross_check", "sole")),
    "RES-EP11-13": (240, ("order-dependent", "deep-copies")),
    "RES-EP11-14": (240, ("asymmetric", "validate_plan_intent",
                          "plan_intent_commitment")),
}


def residual_checks(contract) -> list[str]:
    findings: list[str] = []
    limitations = contract.get("knownLimitations")
    if not isinstance(limitations, list):
        return ["EP11-RESIDUAL: knownLimitations must be an array"]
    text_by_id: dict[str, str] = {}
    for item in limitations:
        if not isinstance(item, str):
            findings.append("EP11-RESIDUAL: every knownLimitations entry must be a "
                            "string")
            continue
        for residual_id in RESIDUAL_CONTENT:
            if residual_id in item:
                text_by_id[residual_id] = item
    for residual_id, (minimum, anchors) in RESIDUAL_CONTENT.items():
        body = text_by_id.get(residual_id)
        if body is None:
            findings.append(f"EP11-RESIDUAL: knownLimitations must carry "
                            f"{residual_id}; a declared residual may not be dropped")
            continue
        if len(body) < minimum:
            findings.append(
                f"EP11-RESIDUAL: {residual_id} is {len(body)} characters; a residual "
                f"must carry at least {minimum} characters of SUBSTANCE. Enforcing "
                "the presence of an identifier lets a future lane hollow out the "
                "disclosure while the instrument reports green")
        for anchor in anchors:
            if anchor not in body:
                findings.append(f"EP11-RESIDUAL: {residual_id} must state "
                                f"{anchor!r}; its content, not its id, is the "
                                "disclosure")
    return findings


def verify_answer_provenance(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("answerProvenance") or {}
    counts = heavy["answerProvenance"]
    for key in ("vectors", "apisPerVector", "expectedPerRuleTotal",
                "independentValueAgreements", "objectProvenanceAgreements",
                "sharedLedgerAgreements", "repairedSentinelFlowed",
                "supersededSentinelIgnored", "gateAgreements", "evaluationErrors"):
        _expect(published, key, counts[key], "EP11-ANSWER: answerProvenance",
                findings)
    if not counts.get("allRulesHeld"):
        findings.append("EP11-ANSWER: not every answer-provenance rule held over "
                        "every pinned vector and every imported API")
    rules = published.get("rules")
    if not isinstance(rules, list) or len(rules) != len(ANSWER_RULE_IDS):
        findings.append(f"EP11-ANSWER: answerProvenance.rules must publish "
                        f"{len(ANSWER_RULE_IDS)} rules, each stating the property "
                        "it establishes and the property it does not")
    else:
        declared = [row.get("id") for row in rules if isinstance(row, dict)]
        if declared != list(ANSWER_RULE_IDS):
            findings.append(f"EP11-ANSWER: answerProvenance.rules declares "
                            f"{declared}; this checker enforces "
                            f"{list(ANSWER_RULE_IDS)}")
        for row in rules:
            if not isinstance(row, dict):
                continue
            for field in ("establishes", "doesNotEstablish"):
                if not isinstance(row.get(field), str) or len(row[field]) < 40:
                    findings.append(
                        f"EP11-ANSWER: rule {row.get('id')!r} must state {field}; a "
                        "rule published without what it does NOT establish is the "
                        "defect ep10.review-independent.json found")
    if published.get("readsSource") is not False:
        findings.append("EP11-ANSWER: answerProvenance.readsSource must be false; "
                        "the load-bearing guard may not be a source scan")
    if published.get("establishesCallProvenanceOnly") is not False:
        findings.append("EP11-ANSWER: answerProvenance.establishesCallProvenanceOnly "
                        "must be false; that is the whole distinction from v10")
    if published.get("isSoleGuardForAnswerProvenance") is not True:
        findings.append(
            "EP11-ANSWER: answerProvenance.isSoleGuardForAnswerProvenance must be "
            "TRUE and published as such. It is measured: the answer-substitution "
            "variants are caught by this guard and by nothing else, and an "
            "undisclosed sole guard is exactly IR-EP10-NB-05")

    control = heavy["control"]
    published_control = published.get("positiveControl") or {}
    if not strict_equal(published_control, control):
        findings.append("EP11-ANSWER: answerProvenance.positiveControl differs from "
                        "the control this run measured; the numbers that show the "
                        "guard still discriminates may not be edited")
    if not control["bothProduceFindings"]:
        findings.append("EP11-ANSWER: a deliberately substituted join did not "
                        "produce an answer-provenance finding")
    decoy = control["decoyCall"]
    if decoy["independentValueAgreements"] != counts["expectedPerRuleTotal"]:
        findings.append(
            "EP11-ANSWER: the decoy control's A-1 agreement count is not the full "
            "total; A-1 is published as insufficient alone precisely because a "
            "substituted answer AGREES with it, and the control must show that")
    forged = control["forgedLedgerEntry"]
    if forged["sharedLedgerAgreements"] <= forged["objectProvenanceAgreements"]:
        findings.append(
            "EP11-ANSWER: the forged-ledger control does not show the shared "
            "served-module ledger agreeing where the private witness does not; "
            "without that difference the choice of a private witness for A-2 is "
            "asserted rather than measured")
    return findings


ANSWER_RULE_IDS = ("A-1", "A-2", "A-3", "A-4", "A-5", "A-6")


def verify_call_provenance(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("callProvenance") or {}
    measure = heavy["callProvenance"]
    for key in ("vectorsDriven", "distinctIntentsDriven", "observedCalls",
                "depthZeroCalls", "distinctFingerprintsObserved",
                "supersededCallsInsideJoin"):
        _expect(published, key, measure[key], "EP11-CALL: callProvenance", findings)
    if published.get("readsSource") is not False:
        findings.append("EP11-CALL: callProvenance.readsSource must be false")
    statement = published.get("whatThisEstablishes") or ""
    for phrase in ("which module was CALLED",):
        if phrase not in statement:
            findings.append(f"EP11-CALL: callProvenance.whatThisEstablishes must say "
                            f"{phrase!r} in terms")
    negative = published.get("whatThisDoesNotEstablish") or ""
    for phrase in ("not whose answer was used", "discarded"):
        if phrase not in negative:
            findings.append(
                f"EP11-CALL: callProvenance.whatThisDoesNotEstablish must say "
                f"{phrase!r}. v10 published a whatThisDoesNotEstablish that omitted "
                "exactly this, and the omission was the blocker")
    if published.get("isSufficientAlone") is not False:
        findings.append("EP11-CALL: callProvenance.isSufficientAlone must be false")
    return findings


def verify_guard_inventory(contract, heavy) -> list[str]:
    """IR-EP10-NB-05: publish EVERY guard for EVERY property, and which are sole."""
    findings: list[str] = []
    inventory = contract.get("guardInventory") or {}
    guards = inventory.get("guards")
    if not isinstance(guards, list):
        return ["EP11-INVENTORY: guardInventory.guards must be an array"]
    declared = {row.get("id"): row for row in guards if isinstance(row, dict)}
    if sorted(declared) != sorted(GUARD_IDS):
        findings.append(f"EP11-INVENTORY: guardInventory declares {sorted(declared)}; "
                        f"this checker runs {sorted(GUARD_IDS)}")
    for row in guards:
        if not isinstance(row, dict):
            continue
        for field in ("establishes", "blindSpot", "readsSource"):
            if field not in row:
                findings.append(f"EP11-INVENTORY: guard {row.get('id')!r} must "
                                f"publish {field}")
        expected_source = row.get("id") in SOURCE_READING_GUARDS
        if not strict_equal(row.get("readsSource"), expected_source):
            findings.append(f"EP11-INVENTORY: guard {row.get('id')!r} publishes "
                            f"readsSource={row.get('readsSource')!r}; this checker "
                            f"runs it as readsSource={expected_source}")
        if isinstance(row.get("blindSpot"), str) and len(row["blindSpot"]) < 60:
            findings.append(f"EP11-INVENTORY: guard {row.get('id')!r} publishes a "
                            "blind spot too short to be a disclosure; every guard "
                            "has one and a claim of total coverage is a finding")
    evasion = heavy["evasion"]
    _expect(inventory, "perGuardCatchCount", evasion["perGuardCatchCount"],
            "EP11-INVENTORY: guardInventory", findings)
    _expect(inventory, "soleGuardVariants", evasion["soleGuardVariants"],
            "EP11-INVENTORY: guardInventory", findings)
    _expect(inventory, "answerProvenanceOnlyCatches",
            evasion["answerProvenanceOnlyCatches"],
            "EP11-INVENTORY: guardInventory", findings)
    if inventory.get("claimsTotalCoverage") is not False:
        findings.append("EP11-INVENTORY: guardInventory.claimsTotalCoverage must be "
                        "false; an inventory that claims total coverage is refused")
    sole_guards = {row["soleGuard"] for row in evasion["soleGuardVariants"]}
    for guard_id in sorted(sole_guards):
        row = declared.get(guard_id) or {}
        if row.get("isSoleGuardForSomeClass") is not True:
            findings.append(
                f"EP11-INVENTORY: guard {guard_id!r} is the SOLE catcher for "
                f"{[item['variant'] for item in evasion['soleGuardVariants'] if item['soleGuard'] == guard_id]} "
                "in this run and must publish isSoleGuardForSomeClass=true. An "
                "undisclosed sole guard is IR-EP10-NB-05")
    for guard_id, row in declared.items():
        if not strict_equal(row.get("isSoleGuardForSomeClass"),
                            guard_id in sole_guards):
            findings.append(f"EP11-INVENTORY: guard {guard_id!r} publishes "
                            f"isSoleGuardForSomeClass="
                            f"{row.get('isSoleGuardForSomeClass')!r}; this run "
                            f"measured {guard_id in sole_guards}")
    return findings


SOURCE_READING_GUARDS = ("c2RouteScan", "introspectionScan")


def verify_evasion(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("evasionMeasurement") or {}
    evasion = heavy["evasion"]
    for key in ("variantsDeclared", "variantsBuilt", "sourceVariantsBuilt",
                "objectAttacksBuilt", "caughtByAtLeastOneGuard",
                "escapedEveryGuard"):
        _expect(published, key, evasion[key], "EP11-EVASION: evasionMeasurement",
                findings)
    if not strict_equal(published.get("perVariant"), evasion["perVariant"]):
        findings.append("EP11-EVASION: evasionMeasurement.perVariant differs from "
                        "the per-guard catch matrix this run measured; the "
                        "unflattering per-variant result may not be edited")
    built = {row["variant"] for row in evasion["perVariant"]}
    for required in REQUIRED_EVASIONS:
        if required not in built:
            findings.append(f"EP11-EVASION: the required evasion {required!r} was "
                            "not built")
            continue
        row = next(item for item in evasion["perVariant"]
                   if item["variant"] == required)
        if required in ANSWER_SUBSTITUTION_VARIANTS and not row["answerProvenance"]:
            findings.append(
                f"EP11-EVASION: {required} substitutes the ANSWER and the "
                "answer-provenance guard did not catch it; that is the blocking "
                "finding of ep10.review-independent.json, unrepaired")
    escaped = evasion["escapedEveryGuard"]
    unexpected = [name for name in escaped if name not in DECLARED_ESCAPES]
    if unexpected:
        findings.append(f"EP11-EVASION: variant(s) {unexpected} escaped EVERY "
                        "declared guard and are not among the declared blind spots")
    _expect(published, "declaredBlindSpotVariants", sorted(DECLARED_ESCAPES),
            "EP11-EVASION: evasionMeasurement", findings)
    tamper = []
    for name in GUARD_TAMPER_VARIANTS:
        row = next((item for item in evasion["perVariant"]
                    if item["variant"] == name), None)
        if row is None:
            findings.append(f"EP11-EVASION: the guard-tamper variant {name!r} must "
                            "be BUILT AND EXECUTED, not asserted")
            continue
        tamper.append({"variant": name,
                       "caughtBy": [key for key in GUARD_IDS if row[key]],
                       "defeatedAnswerProvenance": not row["answerProvenance"]})
    _expect(published, "guardTamperOutcome", tamper,
            "EP11-EVASION: evasionMeasurement", findings)
    return findings


REQUIRED_EVASIONS = (
    "AX2-decoy-call-superseded-answer", "AX3-verdict-only-substitution",
    "AX4-commitment-only-substitution", "AX5-probe-family-split-answers",
    "AX6-stack-walking-witness-forgery", "AX8-differential-sentinel-detector",
    "AX9-obfuscated-witness-forgery", "forged-ledger-entry-replay",
    "R1-probe-whitelist-direct-module", "R4-probe-whitelist-accessor-routed",
    "tag-forgery-at-install", "superseded-backed-shim", "monkeypatched-recorder",
    "getattr-proxy-accessor", "unwrapped-module", "deinstalled-ledger",
    "poisoned-accessor",
)

# Variants that substitute the ANSWER while leaving the CALLS honest.  Every one
# of them is green under all six of v10's ledger rules; the answer-provenance
# guard must catch every one or IR-EP10-01 is unrepaired.
ANSWER_SUBSTITUTION_VARIANTS = (
    "AX2-decoy-call-superseded-answer", "AX3-verdict-only-substitution",
    "AX4-commitment-only-substitution", "AX5-probe-family-split-answers",
    "AX8-differential-sentinel-detector", "forged-ledger-entry-replay",
)

# Variants that tamper with the GUARD rather than with the route.  These are
# outside the answer-provenance guard's declared scope (RES-EP11-02); they are
# built and executed anyway and whatever catches them is published.
GUARD_TAMPER_VARIANTS = ("AX6-stack-walking-witness-forgery",
                         "AX9-obfuscated-witness-forgery")

# Variants declared in advance to escape every guard.  Measured; if this set and
# the measured escape set disagree in either direction it is a finding.
DECLARED_ESCAPES = ()


def verify_scans(contract, heavy, counterparts) -> list[str]:
    findings: list[str] = []
    scope = contract.get("astScanScope") or {}
    route = c2_route_scan()
    introspection = route_introspection_scan()
    dispatch = selftest_dispatch_scan()
    integers = integer_guard_scan()
    circular = non_circularity_scan()
    if route["referencesOutsideDeclaredClosure"]:
        findings.append("EP11-SCAN: a C-2 API is named outside the declared join "
                        "and measurement closure: "
                        f"{route['referencesOutsideDeclaredClosure']}")
    if route["unroutedSitesInsideJoin"]:
        findings.append("EP11-SCAN: a C-2 call inside the join does not route "
                        f"through an Authority accessor: "
                        f"{route['unroutedSitesInsideJoin']}")
    if route["authorityRoutedSites"] < len(C2_IMPORTED_APIS):
        findings.append(f"EP11-SCAN: only {route['authorityRoutedSites']} "
                        "accessor-routed C-2 site(s) remain inside the join")
    if introspection["introspectionSites"]:
        findings.append("EP11-SCAN: the route region names an introspection "
                        f"primitive: {introspection['introspectionSites']}; the "
                        "route region reads its arguments, not the guard")
    if dispatch["selftestCalls"] != 1 or dispatch["mainFunctions"] != 1 or \
            not dispatch["dispatchBeforeFindings"]:
        findings.append("EP11-SCAN: the selftest dispatch is not unique, live and "
                        f"positioned before any findings return: {dispatch}")
    if integers["bareNumericComparisons"]:
        findings.append("EP11-SCAN: a bare numeric comparison against a literal "
                        "remains in a wire-sourced position — this is the LB-C2-01 "
                        f"class: {integers['bareNumericComparisons']}")
    if circular["literalsThatAreNotPins"]:
        findings.append("EP11-SCAN: this checker's own text carries 64-hex "
                        f"literal(s) that are not pins: "
                        f"{circular['literalsThatAreNotPins']}; a commitment or "
                        "identity literal in the instrument makes it circular")
    published_circular = scope.get("nonCircularity") or {}
    for key in ("uniqueHexLiterals", "pinnedDigests", "literalsThatAreNotPins"):
        _expect(published_circular, key, circular[key],
                "EP11-SCAN: astScanScope.nonCircularity", findings)

    declared_scans = scope.get("scans")
    if not isinstance(declared_scans, list):
        return findings + ["EP11-SCAN: astScanScope.scans must be an array"]
    declared = {row.get("id"): row for row in declared_scans if isinstance(row, dict)}
    measured_ids = [row[0] for row in AST_SCAN_REGISTRY]
    if sorted(declared) != sorted(measured_ids):
        findings.append(f"EP11-SCAN: astScanScope.scans declares {sorted(declared)}; "
                        f"this checker runs {sorted(measured_ids)}")
    sole_guard = []
    for scan_id, guarded_property, counterpart in AST_SCAN_REGISTRY:
        row = declared.get(scan_id) or {}
        if row.get("isTripwire") is not True:
            findings.append(f"EP11-SCAN: scan {scan_id} must declare isTripwire=true")
        if row.get("guardedProperty") != guarded_property:
            findings.append(f"EP11-SCAN: scan {scan_id} publishes guardedProperty="
                            f"{row.get('guardedProperty')!r}; this checker guards "
                            f"{guarded_property!r}")
        if row.get("behaviouralCounterpart") != counterpart:
            findings.append(f"EP11-SCAN: scan {scan_id} publishes "
                            "behaviouralCounterpart="
                            f"{row.get('behaviouralCounterpart')!r}; this checker "
                            f"runs {counterpart!r}")
        if not counterparts.get(scan_id):
            sole_guard.append(scan_id)
    _expect(scope, "astOnlyProperties", sole_guard, "EP11-SCAN: astScanScope",
            findings)
    if sole_guard:
        findings.append(f"EP11-SCAN: {sole_guard} has NO executed behavioural "
                        "counterpart in this run; no source scan may be the sole "
                        "guard for any property")
    if scope.get("isSoleGuardForAnyProperty") is not False:
        findings.append("EP11-SCAN: astScanScope.isSoleGuardForAnyProperty must be "
                        "false and must be measured, not asserted; a source scan "
                        "with no executed behavioural counterpart is refused")
    if scope.get("routingScanCannotSeeWhichModuleServes") is not True:
        findings.append("EP11-SCAN: astScanScope must declare that the routing scan "
                        "cannot see WHICH MODULE serves a call")
    if scope.get("routingScanCannotSeeWhoseAnswerIsUsed") is not True:
        findings.append("EP11-SCAN: astScanScope must declare that NO source scan "
                        "can see whose ANSWER the join used; that is the property "
                        "the answer-provenance guard exists for")
    return findings


def verify_totality(contract, heavy, root_census) -> list[str]:
    findings: list[str] = []
    published = contract.get("scalarLeafTotality") or {}
    declared = {row.get("surface"): row for row in (published.get("surfaces") or [])
                if isinstance(row, dict)}
    measured = {
        "plan-intent": {"census": heavy["oracle"]["census"],
                        "stats": heavy["oracle"]["stats"],
                        "silent": heavy["oracle"]["silentAcceptPositions"]},
        "plan-descriptor": {"census": heavy["descriptorSurface"]["census"],
                            "stats": heavy["descriptorSurface"]["stats"],
                            "silent":
                                heavy["descriptorSurface"]["silentAcceptPositions"]},
    }
    for name, item in measured.items():
        row = declared.get(name)
        if row is None:
            findings.append(f"EP11-TOTALITY: surface {name} is not published")
            continue
        for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths"):
            _expect(row, key, item["census"][key],
                    f"EP11-TOTALITY: surface {name}", findings)
        for key in ("enumeratedCases", "noOpInjections", "executedCases",
                    "guardedEscapes", "silentAccepts"):
            _expect(row, key, item["stats"][key],
                    f"EP11-TOTALITY: surface {name}", findings)
        # IR-EP10-NB-03: a count is not a record.
        _expect(row, "silentAcceptPositions", item["silent"],
                f"EP11-TOTALITY: surface {name}", findings)
        if len(item["silent"]) != item["stats"]["silentAccepts"]:
            findings.append(f"EP11-TOTALITY: surface {name} enumerated "
                            f"{len(item['silent'])} silently-accepted position(s) "
                            f"but counted {item['stats']['silentAccepts']}")
        if item["stats"]["guardedEscapes"]:
            findings.append(f"EP11-TOTALITY: surface {name} produced "
                            f"{item['stats']['guardedEscapes']} guarded escapes")
    for name in sorted(set(declared) - set(measured)):
        findings.append(f"EP11-TOTALITY: the candidate publishes surface {name}, "
                        "which this run does not measure")
    root = published.get("contractRoot") or {}
    for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths", "dictPaths",
                "listPaths"):
        _expect(root, key, root_census[key], "EP11-TOTALITY: contractRoot", findings)
    _expect(published, "injectionValues", len(HOSTILE_VALUES),
            "EP11-TOTALITY: scalarLeafTotality", findings)
    if published.get("understatingIsAFinding") is not True:
        findings.append("EP11-TOTALITY: scalarLeafTotality.understatingIsAFinding "
                        "must remain true")
    surface = published.get("evaluationAuthorityCandidateSurface") or {}
    _expect(surface, "regimeAScalarLeafPaths",
            heavy["delegate"]["regimeA"]["scalarLeafPaths"],
            "EP11-TOTALITY: evaluationAuthorityCandidateSurface", findings)
    _expect(surface, "regimeBScalarLeafPaths",
            heavy["delegate"]["regimeB"]["scalarLeafPaths"],
            "EP11-TOTALITY: evaluationAuthorityCandidateSurface", findings)
    return findings


def verify_preserved(contract, heavy) -> list[str]:
    """The reviewer-verified v10 measurements, reproduced by EXECUTION."""
    findings: list[str] = []
    published = contract.get("preservedMeasurements") or {}
    delegate_heavy = heavy["delegate"]
    if published.get("method") != PRESERVATION_METHOD:
        findings.append("EP11-PRESERVED: preservedMeasurements.method must state "
                        "that the predecessor's verified bytes are EXECUTED rather "
                        "than transcribed")
    _expect(published, "predecessorCheckingLayerFindings", len(heavy["v10Findings"]),
            "EP11-PRESERVED: preservedMeasurements", findings)
    if heavy["delegateSourceSealed"] is not True:
        findings.append("EP11-PRESERVED: the delegate's self-source cache was not "
                        "seeded with the verified bytes, so the delegate would "
                        "re-read its own path; the trust order is broken")
    _expect(published, "delegateSourceCacheSeeded", heavy["delegateSourceSealed"],
            "EP11-PRESERVED: preservedMeasurements", findings)

    for label in ("A", "B"):
        block = (published.get("regimes") or {}).get(label)
        measured = delegate_heavy["regime" + label]
        if not isinstance(block, dict):
            findings.append(f"EP11-PRESERVED: regime {label} is not published")
            continue
        for key in ("regime", "enumeratedPaths", "containerPaths",
                    "scalarLeafPaths", "executedCases", "noOpInjections",
                    "rejectedCount", "admittedCount"):
            _expect(block, key, measured[key], f"EP11-PRESERVED: regime {label}",
                    findings)
        if not strict_equal(block, measured):
            findings.append(f"EP11-PRESERVED: regime {label} as published is not "
                            "the block this run re-derived by execution")
        if not strict_equal(block.get("admitted"), measured["admitted"]):
            findings.append(f"EP11-PRESERVED: regime {label}'s admitted set differs "
                            "from the set this run re-derived by execution")
        if not strict_equal(block.get("baseline"), measured["baseline"]):
            findings.append(f"EP11-PRESERVED: regime {label} publishes a baseline "
                            "identity set this run did not recompute")
    moving = [row for row in delegate_heavy["regimeB"]["admitted"]
              if row["classification"] == "type-distinct-one" and
              row["movedIdentities"]]
    under_seal = [row for row in moving
                  if "evaluationAuthoritySealRef" not in row["movedIdentities"]]
    _expect(published, "identityMovingPositions", len(moving),
            "EP11-PRESERVED: preservedMeasurements", findings)
    _expect(published, "identityMovingUnderByteIdenticalSeal", len(under_seal),
            "EP11-PRESERVED: preservedMeasurements", findings)
    if not under_seal:
        findings.append("EP11-PRESERVED: no producer-consistent position was "
                        "measured that moves durable identity beneath a "
                        "byte-identical EvaluationAuthoritySealRef")
    admitted_b = {row["position"] for row in delegate_heavy["regimeB"]["admitted"]}
    if ADMISSION_DESCRIPTOR_POSITION not in admitted_b:
        findings.append("EP11-PRESERVED: the admissionDescriptor.schemaVersion "
                        "position the ep10 review independently confirmed is not in "
                        "this run's regime-B admitted set")

    stability = delegate_heavy["stability"]
    published_stability = published.get("planIntentCommitmentStability") or {}
    for key in ("vectors", "recomputedUnderV4", "reproducedUnderSupersededEncoder",
                "preimageByteIdentical", "distinctCommitments",
                "preimageByteLengths", "distinctFrozenPlanIntents",
                "distinctPlanDescriptors"):
        _expect(published_stability, key, stability[key],
                "EP11-PRESERVED: planIntentCommitmentStability", findings)
    family = delegate_heavy["family"]
    published_family = published.get("distinctIntentFamily") or {}
    for key in ("declaredPerturbations", "acceptedByRepairedInstrument",
                "distinctIntentsDriven", "rejectedPerturbations",
                "distinctCommitments", "injective",
                "reproducedUnderSupersededEncoder", "preimageByteIdentical"):
        _expect(published_family, key, family[key],
                "EP11-PRESERVED: distinctIntentFamily", findings)
    if not family["injective"]:
        findings.append("EP11-PRESERVED: the repaired encoder did not map the "
                        "distinct PlanIntent family injectively")
    probe = delegate_heavy["probe"]
    published_probe = published.get("lbC201ProbeFamily") or {}
    for key in ("cases", "repairedAdmitted", "supersededAdmitted", "secondDigests",
                "admitThenRaise", "discriminatingCardinality"):
        _expect(published_probe, key, probe[key],
                "EP11-PRESERVED: lbC201ProbeFamily", findings)
    if probe["repairedAdmitted"]:
        findings.append(f"EP11-PRESERVED: the repaired instrument admitted "
                        f"{probe['repairedAdmitted']} type-distinct case(s)")
    published_v10_evasion = published.get("predecessorEvasionBattery") or {}
    for key in ("caughtByAstTripwire", "missedByAstTripwire",
                "caughtByDifferentialOracle", "missedByDifferentialOracle",
                "caughtByRoutingLedger", "variantsBuilt"):
        _expect(published_v10_evasion, key, delegate_heavy["evasion"][key],
                "EP11-PRESERVED: predecessorEvasionBattery", findings)
    return findings


PRESERVATION_METHOD = (
    "check-evaluation-proof-v10.py is pinned by SHA-256, read once as inert bytes, "
    "verified, and EXECUTED from that verified in-memory snapshot. The measurements "
    "ep10.review-independent.json verified by independent re-derivation are neither "
    "transcribed nor rebuilt: they are produced here by the same bytes, and the "
    "pinned v10 candidate is additionally driven through v10's own checking layer "
    "on this run and required to produce zero findings.")

ADMISSION_DESCRIPTOR_POSITION = (
    "$.admittedResolvedInputs.frozenPlanIntent.analysis.admissionDescriptor."
    "schemaVersion=json-true")


def check(contract: Any, authority: Authority, snapshots) -> list[str]:
    findings: list[str] = []
    if not isinstance(contract, dict):
        return ["EP11-SHAPE: the candidate must be a JSON object"]

    if contract.get("artifact") != "opensip.evaluation-proof":
        findings.append("EP11-SHAPE: artifact must be opensip.evaluation-proof")
    _exact_int(contract.get("version"), "version", findings, EXPECTED_VERSION)
    if contract.get("status") != "CANDIDATE-NOT-APPLIED":
        findings.append("EP11-POSTURE: status must remain CANDIDATE-NOT-APPLIED")
    if contract.get("reviewState") != "AWAITING-INDEPENDENT-REVIEW":
        findings.append("EP11-POSTURE: reviewState must remain "
                        "AWAITING-INDEPENDENT-REVIEW")
    if contract.get("sealRecommendation") != "DO-NOT-SEAL":
        findings.append("EP11-POSTURE: sealRecommendation must remain DO-NOT-SEAL")
    assurance = contract.get("assurance") or {}
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("candidateState") != "NOT-APPLIED":
        findings.append("EP11-POSTURE: assurance must remain SPECIFIED / "
                        "IMPLEMENTABLE_UNEXECUTED / NOT-APPLIED")
    if assurance.get("qualificationEvidenceIds") or \
            assurance.get("releaseEvidenceIds"):
        findings.append("EP11-POSTURE: no qualification or release evidence may be "
                        "claimed by a CANDIDATE-NOT-APPLIED artifact")
    document = json.dumps(contract, sort_keys=True, ensure_ascii=False)
    for forbidden in ("DISCHARGED", "DEMONSTRATED-AND-SEALED", "SIGNED-OFF"):
        if forbidden in document:
            findings.append(f"EP11-POSTURE: the candidate contains {forbidden!r}; "
                            "implementable is not discharged")
    if "CD-RT-5" not in document or "BLOCKED_ON_PHASE_1A" not in document:
        findings.append("EP11-POSTURE: CD-RT-5 must remain named, unsigned and "
                        "recorded as BLOCKED_ON_PHASE_1A")

    repair_join = contract.get("c2AuthorityRepairJoin") or {}
    residual = repair_join.get("ep6InnerJoinResidual")
    if repair_join.get("ep6InnerJoinResidualId") != "RES-EP11-01":
        findings.append("EP11-RESIDUAL: c2AuthorityRepairJoin.ep6InnerJoinResidualId "
                        "must be RES-EP11-01")
    if not isinstance(residual, str) or "does not repair" not in residual or \
            "check-evaluation-proof-v6.py" not in residual:
        findings.append("EP11-RESIDUAL: c2AuthorityRepairJoin.ep6InnerJoinResidual "
                        "must state that v11 does not repair "
                        "check-evaluation-proof-v6.py")
    findings += residual_checks(contract)
    findings += pin_agreement(contract, authority)
    findings += retraction_checks(contract, authority)

    heavy = heavy_measurements(authority, snapshots)
    findings += list(heavy["findings"])
    if not heavy["named"]:
        return findings

    source_artifact = authority.json(VECTOR_SOURCE)
    if (authority.json(EP9_ARTIFACT) or {}).get("positiveVectors") != \
            source_artifact.get("positiveVectors"):
        findings.append("EP11-VECTORS: the rejected evaluation-proof.v9.json's "
                        "positiveVectors differ from the PASSED EP8 artifact's; "
                        "v11 takes its vectors from EP8 and requires them to agree")
    for rejected in (EP9_ARTIFACT, EP10_ARTIFACT):
        declared = ((authority.json(rejected) or {}).get("c2AuthorityJoin")
                    or {}).get("expectedPlanIntentCommitment")
        if declared != (source_artifact.get("c2AuthorityJoin") or {}).get(
                "expectedPlanIntentCommitment"):
            findings.append(f"EP11-VECTORS: {rejected} declares a PlanIntent "
                            "commitment that differs from the PASSED EP8 "
                            "artifact's; the chain's subject has moved")

    findings += verify_answer_provenance(contract, heavy)
    findings += verify_call_provenance(contract, heavy)
    findings += verify_guard_inventory(contract, heavy)
    findings += verify_evasion(contract, heavy)
    findings += verify_preserved(contract, heavy)

    oracle = heavy["oracle"]
    published_oracle = contract.get("differentialOracle") or {}
    _expect(published_oracle, "executedCases", oracle["stats"]["executedCases"],
            "EP11-DIFF: differentialOracle", findings)
    _expect(published_oracle, "joinVsRepairedMismatches",
            oracle["stats"]["joinVsRepairedMismatches"],
            "EP11-DIFF: differentialOracle", findings)
    _expect(published_oracle, "discriminatingCardinality",
            oracle["discriminatingCardinality"], "EP11-DIFF: differentialOracle",
            findings)
    _expect(published_oracle, "discriminatingPositions", oracle["firstDivergent"],
            "EP11-DIFF: differentialOracle", findings)
    if published_oracle.get("isSufficientAlone") is not False:
        findings.append("EP11-DIFF: differentialOracle.isSufficientAlone must be "
                        "false; it is an A-1-shaped instrument and every "
                        "answer-substitution variant agrees with it")
    if published_oracle.get("computedOnPrivateInstance") is not True:
        findings.append("EP11-DIFF: differentialOracle.computedOnPrivateInstance "
                        "must be true; a reference answer taken through the "
                        "Authority can be poisoned by whatever poisoned the join")

    ep8_commitment = (source_artifact.get("c2AuthorityJoin") or {}).get(
        "expectedPlanIntentCommitment")
    join = contract.get("c2AuthorityJoin") or {}
    if join.get("expectedPlanIntentCommitment") != ep8_commitment:
        findings.append("EP11-COMMITMENT-MOVED: c2AuthorityJoin."
                        "expectedPlanIntentCommitment differs from the digest-pinned "
                        "EP8 artifact's value")
    if join.get("expectedPlanIntentCommitment") not in \
            heavy["delegate"]["stability"]["distinctCommitments"]:
        findings.append("EP11-COMMITMENT-MOVED: the declared commitment is not a "
                        "member of the set this run recomputed through C-2 v4")

    if (contract.get("checkerModeContract") or {}).get(
            "exitMatrixIsObservedBehaviourally") is not True:
        findings.append("EP11-EXIT: checkerModeContract must declare the exit "
                        "matrix observed behaviourally")

    counterparts = authority.cache.get("counterparts")
    if counterparts is None:
        counterparts = {}
        authority.cache["counterparts"] = counterparts
    counterparts["c2-route"] = heavy["answerProvenance"]
    counterparts["route-introspection"] = {"rebound": heavy["rebound"],
                                           "executed": True}
    counterparts["non-circularity"] = heavy["delegate"]["stability"]
    if not _NESTED[0]:
        matrix = exit_matrix_probe(contract, HERE / BINDING, authority, snapshots,
                                   full=False)
        counterparts["selftest-dispatch"] = matrix
        for row in matrix:
            if not row["agrees"]:
                findings.append(f"EP11-EXIT: invocation {row['invocation']!r} "
                                f"returned {row['observed']}, expected "
                                f"{row['expected']}")
        counterparts["integer-guard"] = "EXECUTING"
        battery = own_constant_leaf_battery(contract, authority, snapshots)
        counterparts["integer-guard"] = battery
        published_battery = (contract.get("astScanScope") or {}).get(
            "ownConstantLeafBattery") or {}
        for key in ("intBoolLeaves", "cases", "rejected", "silentlyAdmitted",
                    "silentlyAdmittedPositions"):
            _expect(published_battery, key, battery[key],
                    "EP11-BATTERY: ownConstantLeafBattery", findings)

    root_census, _paths = node_census(contract)
    findings += verify_scans(contract, heavy, counterparts)
    findings += verify_totality(contract, heavy, root_census)

    authority.measurement = {**heavy, "contractRoot": root_census,
                             "counterparts": counterparts}
    return findings


# --------------------------------------------------------------------------
# Section 12.  Selftest and entrypoint.
# --------------------------------------------------------------------------

SELFTEST_MUTATIONS = (
    ("version is the JSON float 11.0", ("version",), 11.0),
    ("version is JSON true", ("version",), True),
    ("status silently applied", ("status",), "APPLIED"),
    ("reviewState pre-cleared", ("reviewState",), "REVIEWED"),
    ("sealRecommendation flipped", ("sealRecommendation",), "SEAL"),
    ("assurance state escalated", ("assurance", "state"), "QUALIFIED"),
    ("evidence grade escalated", ("assurance", "evidenceGrade"), "EXECUTED"),
    ("RET-EP11-01 softened into a scoping note",
     ("retractions", 0, "disposition"), "SCOPED"),
    ("RET-EP11-01 retracted text detached from its subject",
     ("retractions", 0, "retractedText"),
     "a fragment that does not occur in the pinned predecessor at all, of "
     "amply sufficient length to pass a bare minimum-length test"),
    ("RET-EP11-01 retracted text reduced to one character",
     ("retractions", 0, "retractedText"), "a"),
    ("a retraction pointed at the wrong subject path",
     ("retractions", 0, "subjectPath"), "$.artifact"),
    ("answer provenance demoted to call provenance",
     ("answerProvenance", "establishesCallProvenanceOnly"), True),
    ("the sole-guard disclosure withdrawn",
     ("answerProvenance", "isSoleGuardForAnswerProvenance"), False),
    ("a sentinel-flow count overstated",
     ("answerProvenance", "repairedSentinelFlowed"), 99),
    ("the object-provenance count understated",
     ("answerProvenance", "objectProvenanceAgreements"), 0),
    ("the positive control's finding claim flipped",
     ("answerProvenance", "positiveControl", "substitutedJoinProducesFindings"),
     False),
    ("call provenance claimed sufficient alone",
     ("callProvenance", "isSufficientAlone"), True),
    ("the call-ledger limitation deleted",
     ("callProvenance", "whatThisDoesNotEstablish"), "nothing further"),
    ("the guard inventory claims total coverage",
     ("guardInventory", "claimsTotalCoverage"), True),
    ("a sole guard's disclosure withdrawn from the inventory",
     ("guardInventory", "soleGuardVariants"), []),
    ("the differential oracle claimed sufficient alone",
     ("differentialOracle", "isSufficientAlone"), True),
    ("the per-variant evasion matrix edited",
     ("evasionMeasurement", "perVariant"), []),
    ("the declared blind-spot outcome flattered",
     ("evasionMeasurement", "ax6Outcome"), "CAUGHT"),
    ("a preserved regime-B admitted set deleted",
     ("preservedMeasurements", "regimes", "B", "admitted"), []),
    ("preserved identity movement beneath an identical seal denied",
     ("preservedMeasurements", "identityMovingUnderByteIdenticalSeal"), 0),
    ("the plan-intent silent-accept enumeration reduced to a count",
     ("scalarLeafTotality", "surfaces", 0, "silentAcceptPositions"), []),
    ("the plan-descriptor silent-accept enumeration emptied",
     ("scalarLeafTotality", "surfaces", 1, "silentAcceptPositions"), []),
    ("contract-root census understated",
     ("scalarLeafTotality", "contractRoot", "scalarLeafPaths"), 1),
    ("a pinned digest edited",
     ("delegationClosure", "executables", 0, "sha256"), "0" * 64),
    ("the pin-agreement scope claim widened",
     ("delegationClosure", "pinAgreementRule"),
     "every predecessor's own declared pin table is cross-checked"),
    ("the RES-EP11-01 residual deleted",
     ("c2AuthorityRepairJoin", "ep6InnerJoinResidual"), "closed"),
    ("RES-EP11-02 gutted to a bare identifier",
     ("knownLimitations", 1), "RES-EP11-02."),
    ("RES-EP11-07 gutted to a bare identifier",
     ("knownLimitations", 6), "RES-EP11-07."),
    ("RES-EP11-12 hollowed of its sole-guard disclosure",
     ("knownLimitations", 11),
     "RES-EP11-12. Everything is guarded by more than one guard and there is no "
     "sole guard anywhere in this instrument, which would be a comfortable thing "
     "to be able to say and is not what this run measured at all."),
    ("the non-circularity measurement understated",
     ("astScanScope", "nonCircularity", "uniqueHexLiterals"), 1),
    ("a source scan reclaimed as free of blind spots",
     ("astScanScope", "routingScanCannotSeeWhoseAnswerIsUsed"), False),
)


def selftest(contract, authority, path, snapshots) -> int:
    base = check(contract, authority, snapshots)
    if base:
        print("SELFTEST-REFUSED: the base candidate is already dirty; a mutation "
              "suite over a dirty base proves nothing")
        for item in base[:5]:
            print("  -", item)
        print(f"SELFTEST-NOT-RUN: 0 of {len(SELFTEST_MUTATIONS)} mutations executed")
        return 3

    print(f"EP11 SELFTEST — {path.name}")
    print()
    escaped: list[str] = []
    for label, mutation_path, injected in SELFTEST_MUTATIONS:
        mutated = copy.deepcopy(contract)
        try:
            cursor = mutated
            for key in mutation_path[:-1]:
                cursor = cursor[key]
            cursor[mutation_path[-1]] = injected
        except MALFORMED:
            escaped.append(f"{label}: the mutation path does not exist")
            print(f"  ESCAPE  {label}: path absent")
            continue
        _NESTED[0] += 1
        try:
            findings = check(mutated, authority, snapshots)
        finally:
            _NESTED[0] -= 1
        if findings:
            print(f"  reject  {label}")
            print(f"            -> {findings[0][:140]}")
        else:
            escaped.append(label)
            print(f"  ESCAPE  {label}")

    print()
    matrix = exit_matrix_probe(contract, path, authority, snapshots, full=True)
    print("  exit matrix, observed BEHAVIOURALLY by driving main() in-process:")
    for row in matrix:
        verdict = "ok " if row["agrees"] else "BAD"
        print(f"    {verdict} {row['invocation']}: expected {row['expected']}, "
              f"observed {row['observed']} ({row['outputLines']} output lines)")
        if not row["agrees"]:
            escaped.append(f"exit matrix: {row['invocation']}")

    measurement = authority.measurement
    evasion = measurement["evasion"]
    print()
    print("  evasion battery, re-stated from this run (guard columns in order "
          f"{list(GUARD_IDS)}):")
    for row in evasion["perVariant"]:
        flags = "".join("Y" if row.get(key) else "." for key in GUARD_IDS)
        print(f"    {flags}  {row['variant']}")
    print(f"  variants that escaped EVERY guard: "
          f"{evasion['escapedEveryGuard'] or 'none'} "
          f"(declared blind spots: {list(DECLARED_ESCAPES)})")
    battery = (measurement.get("counterparts") or {}).get("integer-guard") or {}
    print(f"  own constant-leaf battery: {battery.get('intBoolLeaves')} int/bool "
          f"leaves, {battery.get('cases')} cases, {battery.get('rejected')} "
          f"rejected, {battery.get('silentlyAdmitted')} silently admitted")

    print()
    if escaped:
        for item in escaped:
            print("SELFTEST-FAIL:", item)
        print(f"{len(escaped)} retained case(s) ESCAPED — the proof path is optional")
        return 1
    print(f"SELFTEST-PASS: all {len(SELFTEST_MUTATIONS)} mutations rejected and the "
          "0/1/2/3 exit matrix agrees behaviourally")
    print("  RES-EP11-01: v11 does NOT repair check-evaluation-proof-v6.py; EP6's "
          "inner C-2 join still runs against the DEFECTIVE check-c2.py bytes")
    print("  RES-EP11-02: a route region that walks the call stack is NOT closed by "
          "this instrument; AX6 is built and executed and its outcome is published")
    return 0


def _parse_argv(argv):
    flags, positional, seen = set(), [], []
    for arg in argv[1:]:
        if arg in DECLARED_FLAGS:
            if arg in seen:
                raise UnsupportedInvocation(f"flag {arg!r} repeated")
            seen.append(arg)
            flags.add(arg)
        elif isinstance(arg, str) and arg.startswith("-"):
            raise UnsupportedInvocation(
                f"unknown flag {arg!r}; declared flags are {list(DECLARED_FLAGS)}")
        else:
            positional.append(arg)
    if len(positional) > 1:
        raise UnsupportedInvocation("at most one artifact path may be supplied")
    return flags, (positional[0] if positional else None)


def main(argv, override=None) -> int:
    try:
        flags, requested = _parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"EP11-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    try:
        if override and override.get("authority") is not None:
            authority = override["authority"]
            snapshots = override["snapshots"]
        else:
            snapshots = load_snapshots()
            authority = build_authority(snapshots)
    except AuthorityLoadError as exc:
        print(f"EP11-PINNED-INPUT-REFUSED: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        text = override["candidateText"] if override and "candidateText" in override \
            else path.read_text()
        contract = json.loads(text, object_pairs_hook=_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"cannot load the EP11 candidate {path}: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in flags:
        return selftest(contract, authority, path, snapshots)
    findings = check(contract, authority, snapshots)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for item in findings:
            print("  -", item)
        return 1
    print_banner(contract, authority, path)
    return 0


def print_banner(contract, authority, path) -> None:
    measurement = authority.measurement
    answer = measurement["answerProvenance"]
    call = measurement["callProvenance"]
    evasion = measurement["evasion"]
    oracle = measurement["oracle"]
    delegate_heavy = measurement["delegate"]
    control = measurement["control"]
    root = measurement["contractRoot"]
    descriptor = measurement["descriptorSurface"]
    regime_a, regime_b = delegate_heavy["regimeA"], delegate_heavy["regimeB"]
    moving = [row for row in regime_b["admitted"]
              if row["classification"] == "type-distinct-one" and
              row["movedIdentities"]]
    under_seal = [row for row in moving
                  if "evaluationAuthoritySealRef" not in row["movedIdentities"]]

    print(f"EP11 contract OK — {path.name}")
    print(f"  delegation closure: {len(DELEGATED_CHECKER)} delegated checker + "
          f"{len(DELEGATION_CLOSURE)} executables + {len(PINNED_DATA)} pinned data "
          "inputs + 1 superseded independent encoder, each read ONCE, SHA-256 "
          "verified, then executed or parsed from that verified byte string; every "
          "one recorded by filename and digest")
    print(f"  C-2 join RE-PINNED onto {C2V4_CONTRACT} / {C2V4}")
    print(f"  ANSWER PROVENANCE ESTABLISHED for {answer['vectors']} pinned vectors x "
          f"{answer['apisPerVector']} imported APIs = "
          f"{answer['expectedPerRuleTotal']} answers: "
          f"{answer['independentValueAgreements']} equal the value an INDEPENDENT "
          f"instance of {C2V4} computed (A-1); "
          f"{answer['objectProvenanceAgreements']} ARE the object that module "
          f"produced for this vector (A-2); {answer['repairedSentinelFlowed']} "
          "FOLLOW a sentinel injected into every reachable spelling of the repaired "
          f"api (A-3); {answer['supersededSentinelIgnored']} are UNMOVED by the same "
          f"injection into the superseded module (A-4); {answer['gateAgreements']} "
          "accept/reject gates agree (A-5)")
    print(f"  CALL PROVENANCE, and no more than that: {call['observedCalls']} C-2 "
          f"calls observed per call across {call['vectorsDriven']} vectors, "
          f"{call['distinctFingerprintsObserved']} distinct PlanIntent "
          f"fingerprint(s), {call['supersededCallsInsideJoin']} served by the "
          "superseded module. This establishes WHICH MODULE WAS CALLED, not whose "
          "answer was used — v10 published the second and measured only the first")
    print(f"  positive control on the guard: the decoy-call join produces "
          f"{control['decoyCall']['findingCount']} answer-provenance finding(s) "
          f"while A-1 still agrees "
          f"{control['decoyCall']['independentValueAgreements']}/"
          f"{answer['expectedPerRuleTotal']} times; the forged-ledger join has the "
          f"SHARED ledger agreeing "
          f"{control['forgedLedgerEntry']['sharedLedgerAgreements']} times and the "
          f"guard's PRIVATE witness agreeing "
          f"{control['forgedLedgerEntry']['objectProvenanceAgreements']} times — "
          "which is why A-2 does not read the shared ledger")
    print(f"  evasion battery: {evasion['variantsBuilt']} variants BUILT AND "
          f"EXECUTED ({evasion['sourceVariantsBuilt']} route-region rewrites + "
          f"{evasion['objectAttacksBuilt']} object attacks); per-guard catches "
          f"{evasion['perGuardCatchCount']}; caught by at least one guard "
          f"{evasion['caughtByAtLeastOneGuard']}; ESCAPED EVERY GUARD "
          f"{evasion['escapedEveryGuard'] or '[]'} (declared blind spot "
          f"{list(DECLARED_ESCAPES)}); answer-provenance is the SOLE catcher of "
          f"{evasion['answerProvenanceOnlyCatches']}")
    print(f"  PRESERVED BY EXECUTION, not transcription: {EP10} run from its "
          "verified snapshot; the pinned v10 candidate passes v10's own checking "
          f"layer on this run with {len(measurement['v10Findings'])} finding(s). "
          f"Regime A {regime_a['executedCases']} cases over "
          f"{regime_a['scalarLeafPaths']} scalar leaves -> "
          f"{regime_a['admittedCount']} admitted, 0 moving identity; regime B "
          f"{regime_b['executedCases']} cases over {regime_b['scalarLeafPaths']} "
          f"scalar leaves -> {regime_b['admittedCount']} admitted, {len(moving)} "
          f"moving identity, {len(under_seal)} beneath a BYTE-IDENTICAL "
          "EvaluationAuthoritySealRef")
    print(f"  differential oracle (RETAINED, NOT SUFFICIENT ALONE, computed on the "
          f"guard's PRIVATE instance): {oracle['stats']['executedCases']} executed "
          f"cases, {oracle['stats']['joinVsRepairedMismatches']} join-vs-repaired "
          f"mismatches, discriminating cardinality "
          f"{oracle['discriminatingCardinality']}")
    print("  silent accepts ENUMERATED, not counted (IR-EP10-NB-03): plan-intent "
          f"{len(oracle['silentAcceptPositions'])} position(s), plan-descriptor "
          f"{len(descriptor['silentAcceptPositions'])} position(s), each published "
          "in full and required to match exactly")
    print(f"  contract-root space measured at {root['enumeratedPaths']} paths of "
          f"which {root['scalarLeafPaths']} are scalar leaves")
    print("  RES-EP11-01: v11 does NOT repair check-evaluation-proof-v6.py; EP6's "
          "inner C-2 join still runs against the DEFECTIVE check-c2.py bytes "
          "underneath EP8, and v11 is a strictly stronger OUTER gate over it")
    print("  RES-EP11-02: the answer-provenance guard models a hostile ROUTE "
          "REGION, not a hostile guard. A mutation that walks the call stack to "
          "read or rewrite the guard's own locals is NOT closed here; AX6 is built "
          "and executed and its measured outcome is published")
    print("  RES-EP11-09: provenance is not correctness. These rules establish that "
          f"the answer used is {C2V4}'s answer, not that {C2V4} is right")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; DO-NOT-SEAL; CD-RT-5 unsigned; independent "
          "re-review REQUIRED")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
